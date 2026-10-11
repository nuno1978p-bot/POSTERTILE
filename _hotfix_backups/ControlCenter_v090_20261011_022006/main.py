# -*- coding: utf-8 -*-
"""NONIVERUS PosterTile Luxury Studio v0.9.0.1 — Qt Quick front-end."""
import os, sys, math, tempfile, atexit, shutil
from pathlib import Path
from PySide6.QtCore import QObject, Signal, Property, Slot, QUrl, QSettings
from PySide6.QtGui import QGuiApplication, QIcon, QFont, QFontDatabase, QFontMetrics, QImage, QPainter, QColor, QPen, QPixmap, QPainterPath
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QFormLayout, QTextEdit, QSpinBox, QColorDialog, QDoubleSpinBox, QCheckBox, QScrollArea, QFrame, QSizePolicy, QFontComboBox, QSplitter
from PIL import Image, ImageOps
from poster_framing import framed_thumbnail, MODES
from composition_drag import fitted_image_rect, image_rect_to_view, point_hits_rect, drag_anchor
from postertile_engine import plan, export_pdf
from a3_two_a4 import plan_a3_two, export_a3_two_a4
import printer_calibration as pc

BASE=Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
try:
    from edition_config import EDITION
except ImportError:
    # Normal source checkout remains an unrestricted, explicitly labelled DEV build.
    # Private Preview installers MUST be built with build_editions.py, which embeds
    # edition_config.py containing EDITION='preview'. No user-facing edition toggle.
    EDITION="dev"
if EDITION not in ("dev", "owner", "preview"):
    raise RuntimeError("Edição NONIVERUS desconhecida.")

class Studio(QObject):
    changed=Signal()
    notice=Signal(str)
    @staticmethod
    def number(v,default):
        try: return float(str(v).strip().replace("cm","").replace("mm","").replace(",","."))
        except (ValueError,TypeError): return default
    def __init__(self):
        super().__init__()
        self._path=""
        self._source_mode="image"
        self._overlay_base=""
        self._overlay_text=""
        self._overlay_font="Arial"
        self._overlay_size=12.0
        self._overlay_x=50.0
        self._overlay_y=50.0
        self._overlay_color="#FFFFFF"
        self._overlay_outline="#152E4B"
        self._overlay_outline_width=2.0
        self._overlay_bold=True
        self._ratio=0.7
        self._width=70.0
        self._height=100.0
        self._margin=8.0
        self._overlap=10.0
        self._assembly="Sobrepor"
        self._paper="A4 vertical"
        self._fit="Ajustar"
        self._focal_x=50.0
        self._focal_y=50.0
        # Ephemeral previews only. The original input and exported PDF remain untouched.
        self._preview_dir=Path(tempfile.mkdtemp(prefix="noniverus_postertile_preview_"))
        atexit.register(shutil.rmtree,self._preview_dir,ignore_errors=True)
        self._preview_key=None
        self._preview_url=""
        self._size="Personalizado"
        self._a3two_orientation=None
        self._a3two_mode="safe"
        self._status="Importa uma imagem para iniciar o teu projeto."
        self._selected_printer=""
        self._settings=QSettings("NONIVERUS","PosterTileLuxuryStudio")
        self._selected_printer=self._settings.value("printer/selected","")
        theme=self._settings.value("appearance/theme","Midnight Sapphire")
        self._theme=theme if theme in ("Midnight Sapphire","Pearl Titanium") else "Midnight Sapphire"
        lang=self._settings.value("appearance/language","pt-PT")
        self._language=lang if lang in ("pt-PT","en","es","fr","it") else "pt-PT"
    @Property(str, notify=changed)
    def supportEmail(self):
        return "contact@noniverus.com"

    @Property(str, constant=True)
    def editionName(self):
        return {"owner":"OWNER", "preview":"PRIVATE PREVIEW", "dev":"DEV"}[EDITION]

    @Property(str,notify=changed)
    def theme(self): return self._theme
    @Slot(str)
    def setTheme(self,theme):
        if theme not in ("Midnight Sapphire","Pearl Titanium"): return
        self._theme=theme
        self._settings.setValue("appearance/theme",theme)
        self._settings.sync()
        self.changed.emit()
    @Property(str,notify=changed)
    def language(self): return self._language
    @Slot(str)
    def setLanguage(self, lang):
        if lang not in ("pt-PT","en","es","fr","it"): return
        self._language=lang
        self._settings.setValue("appearance/language",lang)
        self._settings.sync()
        self.changed.emit()
    @Property(str,notify=changed)
    def imageUrl(self): return QUrl.fromLocalFile(self._path).toString() if self._path else ""
    def _poster_frame_size(self):
        if self._a3two_orientation:
            try:
                p = self._make_plan()
                return p["work_w"],p["work_h"]
            except (ValueError,TypeError):
                pass
        return self._width*10.0,self._height*10.0

    @Property(float,notify=changed)
    def previewRatio(self):
        w,h=self._poster_frame_size()
        return w/max(0.01,h)

    @Property(str,notify=changed)
    def fitMode(self):
        return self._fit

    @Property(float,notify=changed)
    def focalX(self):
        return self._focal_x

    @Property(float,notify=changed)
    def focalY(self):
        return self._focal_y

    @Slot(str)
    def setFitMode(self, mode):
        if mode not in MODES or mode==self._fit: return
        self._fit=mode
        self.changed.emit()

    @Slot(float,float)
    def setFocalPosition(self,x,y):
        x=max(0.0,min(100.0,float(x)))
        y=max(0.0,min(100.0,float(y)))
        if x==self._focal_x and y==self._focal_y: return
        self._focal_x,self._focal_y=x,y
        self.changed.emit()

    @Property(str,notify=changed)
    def framedPreviewUrl(self):
        if not self._path: return ""
        try:
            w,h=self._poster_frame_size()
            stat=Path(self._path).stat()
            key=(str(self._path),stat.st_mtime_ns,w,h,
                 self._fit,self._focal_x,self._focal_y)
            if key!=self._preview_key:
                preview=framed_thumbnail(
                    self._path,w,h,self._fit,
                    self._focal_x,self._focal_y,max_side=1100
                )
                result=self._preview_dir/f"preview_{len(list(self._preview_dir.glob('*.png'))):04d}.png"
                preview.save(result,format="PNG")
                self._preview_url=QUrl.fromLocalFile(str(result)).toString()
                self._preview_key=key
                # Avoid unlimited temporary files during repeated edits.
                previews=sorted(self._preview_dir.glob("preview_*.png"))
                for old in previews[:-35]:
                    try: old.unlink()
                    except OSError: pass
            return self._preview_url
        except Exception:
            return self.imageUrl

    @Property(str,notify=changed)
    def sourceMode(self): return self._source_mode
    @Property(str,notify=changed)
    def filename(self): return Path(self._path).name if self._path else "Nenhuma imagem selecionada"
    @Property(float,notify=changed)
    def widthCm(self):return round(self._width,2)
    @Property(float,notify=changed)
    def heightCm(self):return round(self._height,2)
    @Property(str,notify=changed)
    def summary(self):
        try:
            p=self._make_plan()
            if self._a3two_orientation:
                if self._a3two_mode=="borderless":
                    return f"2 folhas {p['orientation']}  ·  A3 exato  ·  SEM MARGENS"
                rw,rh=p["work_w"],p["work_h"]
                usable_w=min(rw,rh*self._ratio)
                usable_h=usable_w/self._ratio
                return (f"2 folhas {p['orientation']} · imagem {usable_w:.0f} × "
                        f"{usable_h:.0f} mm · A3 reduzido")
            return f"{p['pages']} folhas  ·  {p['nx']} × {p['ny']}  ·  {p['orientation']}"
        except ValueError as ex: return str(ex)
    @Property(int,notify=changed)
    def pageCount(self):
        try:return self._make_plan()["pages"]
        except ValueError:return 0
    @Property(int,notify=changed)
    def columns(self):
        try:return self._make_plan()["nx"]
        except ValueError:return 0
    @Property(int,notify=changed)
    def rows(self):
        try:return self._make_plan()["ny"]
        except ValueError:return 0
    @Property(bool,notify=changed)
    def a3TwoEnabled(self): return self._a3two_orientation is not None
    @Property(str,notify=changed)
    def a3TwoMode(self): return self._a3two_mode
    @Slot(str)
    def setA3TwoMode(self, mode):
        if mode not in ("safe", "borderless"): return
        self._a3two_mode=mode
        self.changed.emit()
    @Property(str,notify=changed)
    def status(self):return self._status
    def _make_plan(self):
        if self._a3two_orientation:
            return plan_a3_two(self._a3two_orientation, self._a3two_mode, self._margin)
        return plan(self._width*10,self._height*10,self._margin,self._overlap,self._paper,self._assembly)
    @Slot()
    def chooseImage(self):
        path,_=QFileDialog.getOpenFileName(None,"Abrir imagem — NONIVERUS",str(Path.home()),"Imagens (*.png *.jpg *.jpeg *.webp *.tif *.tiff *.bmp)")
        if not path:return
        try:
            with Image.open(path) as src:
                im=ImageOps.exif_transpose(src)
                if "A" in im.getbands():
                    mask=im.getchannel("A")
                    bounds=mask.point(lambda a:255 if a>8 else 0).getbbox()
                    if bounds:im=im.crop(bounds)
                iw,ih=im.size
                if iw<=0 or ih<=0:raise ValueError("Imagem sem conteúdo visível.")
                self._ratio=iw/ih
                self._path=path
                self._source_mode="image"
                self._width=self._height*self._ratio
                self._status={"pt-PT":"Imagem importada. Define as medidas finais e exporta o PDF.","en":"Image imported. Set the size and export.","es":"Imagen importada. Define el tamaño y exporta.","fr":"Image importée. Définissez les dimensions et exportez.","it":"Immagine importata. Imposta le dimensioni ed esporta."}[self._language]
                self.changed.emit()
        except Exception as ex:self.notice.emit(f"Não foi possível abrir a imagem:\n{ex}")
    @Slot()
    def createText(self):
        """Composição tipográfica usando apenas famílias instaladas no sistema."""
        tr = {
          "pt-PT": ("NONIVERUS | Texto gigante", "Escreve a frase:", "Fonte instalada:", "Estilo:", "Tamanho base (px):", "Cor do texto:", "Cor do fundo:", "Criar composição", "Cancelar", "Texto gigante", "É necessário escrever uma frase.", "Não foi possível compor o texto:"),
          "en": ("NONIVERUS | Large text", "Enter your text:", "Installed font:", "Style:", "Base size (px):", "Text colour:", "Background colour:", "Create composition", "Cancel", "Large text", "Please enter text.", "Unable to render text:"),
          "es": ("NONIVERUS | Texto gigante", "Escribe el texto:", "Fuente instalada:", "Estilo:", "Tamaño base (px):", "Color del texto:", "Color de fondo:", "Crear composición", "Cancelar", "Texto gigante", "Escribe un texto.", "No se pudo generar el texto:"),
          "fr": ("NONIVERUS | Texte géant", "Saisissez votre texte :", "Police installée :", "Style :", "Taille de base (px) :", "Couleur du texte :", "Couleur de fond :", "Créer la composition", "Annuler", "Texte géant", "Saisissez un texte.", "Impossible de créer le texte :"),
          "it": ("NONIVERUS | Testo gigante", "Inserisci il testo:", "Font installato:", "Stile:", "Dimensione base (px):", "Colore testo:", "Colore sfondo:", "Crea composizione", "Annulla", "Testo gigante", "Inserisci del testo.", "Impossibile creare il testo:")
        }[self._language]
        dialog=QDialog()
        dialog.setWindowTitle(tr[0]);dialog.setMinimumWidth(540)
        layout=QVBoxLayout(dialog);form=QFormLayout()
        content=QTextEdit();content.setPlaceholderText("A MINHA FESTA" if self._language=="pt-PT" else "YOUR MESSAGE")
        content.setPlainText(getattr(self,"_text_value",""))
        content.setMaximumHeight(125)
        families=QFontDatabase.families()
        fontbox=QComboBox();fontbox.addItems(families);fontbox.setEditable(True)
        previous=getattr(self,"_font_family","Arial")
        if previous in families:fontbox.setCurrentText(previous)
        stylebox=QComboBox()
        stylebox.addItems(["Regular","Bold","Italic","Bold Italic"])
        stylebox.setCurrentText(getattr(self,"_text_style","Bold"))
        sizebox=QSpinBox();sizebox.setRange(32,360);sizebox.setValue(getattr(self,"_text_pixels",180))
        text_color=QColor(getattr(self,"_text_color","#152E4B"))
        background=QColor(getattr(self,"_text_background","#FFFFFF"))
        textbtn=QPushButton(text_color.name());backbtn=QPushButton(background.name())
        def pick_text():
            nonlocal text_color
            c=QColorDialog.getColor(text_color,dialog)
            if c.isValid():text_color=c;textbtn.setText(c.name())
        def pick_background():
            nonlocal background
            c=QColorDialog.getColor(background,dialog)
            if c.isValid():background=c;backbtn.setText(c.name())
        textbtn.clicked.connect(pick_text);backbtn.clicked.connect(pick_background)
        for label,widget in ((tr[1],content),(tr[2],fontbox),(tr[3],stylebox),(tr[4],sizebox),(tr[5],textbtn),(tr[6],backbtn)):
            form.addRow(label,widget)
        layout.addLayout(form)
        hint=QLabel("↳ A4 / A3 · 100% · NONIVERUS PosterTile");layout.addWidget(hint)
        controls=QHBoxLayout();applybtn=QPushButton(tr[7]);cancelbtn=QPushButton(tr[8])
        controls.addWidget(cancelbtn);controls.addWidget(applybtn);layout.addLayout(controls)
        cancelbtn.clicked.connect(dialog.reject)
        def make():
            value=content.toPlainText().strip()
            if not value:QMessageBox.warning(dialog,tr[0],tr[10]);return
            try:
                family=fontbox.currentText()
                if family not in QFontDatabase.families():raise ValueError("Font family unavailable")
                font=QFont(family);font.setPixelSize(sizebox.value())
                font.setBold("Bold" in stylebox.currentText())
                font.setItalic("Italic" in stylebox.currentText())
                fm=QFontMetrics(font)
                lines=value.splitlines()
                if len(lines)>30 or len(value)>1500:raise ValueError("Maximum: 30 lines / 1500 characters")
                padding=max(35,int(sizebox.value()*.18))
                w=max(1,max(fm.horizontalAdvance(line or " ") for line in lines))
                h=fm.lineSpacing()*len(lines)
                full_w=w+2*padding;full_h=h+2*padding
                factor=min(1.0,5000/max(full_w,full_h))
                if factor<1:
                    font.setPixelSize(max(8,int(font.pixelSize()*factor)))
                    fm=QFontMetrics(font)
                    padding=max(10,int(padding*factor))
                    w=max(1,max(fm.horizontalAdvance(line or " ") for line in lines))
                    h=fm.lineSpacing()*len(lines);full_w=w+2*padding;full_h=h+2*padding
                canvas=QImage(full_w,full_h,QImage.Format_ARGB32)
                canvas.fill(background)
                painter=QPainter(canvas);painter.setRenderHint(QPainter.Antialiasing,True)
                painter.setRenderHint(QPainter.TextAntialiasing,True)
                painter.setPen(text_color);painter.setFont(font)
                baseline=padding+fm.ascent()
                for line in lines:
                    x=padding+(w-fm.horizontalAdvance(line))/2
                    painter.drawText(int(x),int(baseline),line)
                    baseline+=fm.lineSpacing()
                painter.end()
                folder=Path(os.getenv("LOCALAPPDATA",str(Path.home()))) / "NONIVERUS" / "PosterTile" / "compositions"
                folder.mkdir(parents=True,exist_ok=True)
                from uuid import uuid4
                output=folder / ("text_"+uuid4().hex+".png")
                if not canvas.save(str(output),"PNG"):raise IOError("PNG render failed")
                self._text_value=value;self._font_family=family;self._text_style=stylebox.currentText()
                self._text_pixels=sizebox.value()
                self._text_color=text_color.name();self._text_background=background.name()
                self._ratio=full_w/full_h
                self._path=str(output)
                self._source_mode="text"
                self._width=self._height*self._ratio
                self._status={"pt-PT":"Composição tipográfica criada. Define as medidas finais e exporta.",
                   "en":"Text composition created. Set the final dimensions and export.",
                   "es":"Texto creado. Define las dimensiones finales y exporta.",
                   "fr":"Composition créée. Définissez les dimensions finales et exportez.",
                   "it":"Composizione creata. Imposta le dimensioni finali ed esporta."}[self._language]
                self.changed.emit()
                dialog.accept()
            except Exception as exc:QMessageBox.warning(dialog,tr[0],tr[11]+" "+str(exc))
        applybtn.clicked.connect(make);dialog.exec()

    @Slot()
    def composeImageText(self):
        """Premium editor: live image/font preview, exact shared rendering for PDF export."""
        from PIL.ImageQt import ImageQt
        from PySide6.QtCore import Qt, QTimer, QRectF
        from PySide6.QtWidgets import QGridLayout
        lang=self._language
        labels={
          "pt-PT":("EDITOR DE COMPOSIÇÃO","IMAGEM BASE","Escolher imagem","CONTEÚDO","TIPOGRAFIA","ESTILO","POSIÇÃO","PRÉ-VISUALIZAÇÃO AO VIVO","Aplicar composição","Cancelar","Repor","Fonte instalada","Altura das letras (%)","Posição horizontal (%)","Posição vertical (%)","Contorno (%)","Cor do texto","Cor do contorno","Negrito","Itálico","Sem imagem selecionada","Texto de exemplo"),
          "en":("COMPOSITION EDITOR","BASE IMAGE","Choose image","CONTENT","TYPOGRAPHY","STYLE","POSITION","LIVE PREVIEW","Apply composition","Cancel","Reset","Installed font","Letter height (%)","Horizontal position (%)","Vertical position (%)","Outline (%)","Text colour","Outline colour","Bold","Italic","No image selected","Sample text"),
          "es":("EDITOR DE COMPOSICIÓN","IMAGEN BASE","Elegir imagen","CONTENIDO","TIPOGRAFÍA","ESTILO","POSICIÓN","VISTA PREVIA EN DIRECTO","Aplicar composición","Cancelar","Restablecer","Fuente instalada","Altura de letras (%)","Posición horizontal (%)","Posición vertical (%)","Contorno (%)","Color del texto","Color del contorno","Negrita","Cursiva","Sin imagen","Texto de ejemplo"),
          "fr":("ÉDITEUR DE COMPOSITION","IMAGE DE BASE","Choisir une image","CONTENU","TYPOGRAPHIE","STYLE","POSITION","APERÇU EN DIRECT","Appliquer","Annuler","Réinitialiser","Police installée","Hauteur des lettres (%)","Position horizontale (%)","Position verticale (%)","Contour (%)","Couleur du texte","Couleur du contour","Gras","Italique","Aucune image","Texte d’exemple"),
          "it":("EDITOR DI COMPOSIZIONE","IMMAGINE BASE","Scegli immagine","CONTENUTO","TIPOGRAFIA","STILE","POSIZIONE","ANTEPRIMA DAL VIVO","Applica","Annulla","Ripristina","Font installato","Altezza lettere (%)","Posizione orizzontale (%)","Posizione verticale (%)","Contorno (%)","Colore testo","Colore contorno","Grassetto","Corsivo","Nessuna immagine","Testo di esempio")
        }[lang]
        dlg=QDialog()
        dlg.setObjectName("compositionEditor")
        dlg.setWindowTitle("NONIVERUS | "+labels[0])
        dlg.resize(1180,750);dlg.setMinimumSize(880,570)
        settings=QSettings("NONIVERUS","PosterTile")
        light=self._theme=="Pearl Titanium"
        bg="#E9E5DE" if light else "#101B2C"
        panel="#D9E1E6" if light else "#1A2A3F"
        ink="#142D4A" if light else "#F2F4F6"
        muted="#55708A" if light else "#A8B9CE"
        bronze="#BB7745" if light else "#D29B67"
        dlg.setStyleSheet("""
          QDialog#compositionEditor { background:%s; color:%s; }
          QDialog#compositionEditor QLabel { color:%s; background:transparent; }
          QDialog#compositionEditor QFrame#previewFrame { background:%s; border:1px solid %s; border-radius:12px; }
          QDialog#compositionEditor QLineEdit, QDialog#compositionEditor QTextEdit,
          QDialog#compositionEditor QComboBox, QDialog#compositionEditor QDoubleSpinBox,
          QDialog#compositionEditor QFontComboBox {
            color:%s; background:%s; border:1px solid %s; padding:7px; border-radius:6px;
            selection-background-color:%s;
          }
          QDialog#compositionEditor QPushButton {
            color:%s; background:%s; border:1px solid %s; border-radius:7px;
            padding:10px; font-weight:600;
          }
          QDialog#compositionEditor QPushButton#primary {
            color:#FFFFFF; background:%s; border:0px;
          }
          QDialog#compositionEditor QScrollArea { border:0; background:transparent; }
          QDialog#compositionEditor QCheckBox { color:%s; }
        """%(bg,ink,ink,panel,muted,ink,panel,muted,bronze,ink,panel,muted,bronze,ink))
        main=QVBoxLayout(dlg);main.setContentsMargins(22,17,22,17);main.setSpacing(12)
        heading=QHBoxLayout()
        brand=QLabel("NONIVERUS   /   "+labels[0]);brand.setStyleSheet("font-size:19px;font-family:Georgia;font-weight:600;")
        heading.addWidget(brand);heading.addStretch()
        chip=QLabel("POSTERTILE  •  LUXURY STUDIO");chip.setStyleSheet("color:%s;font-size:10px;letter-spacing:2px;"%muted)
        heading.addWidget(chip);main.addLayout(heading)
        body=QHBoxLayout();body.setSpacing(16);main.addLayout(body,1)
        scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setFixedWidth(410)
        left=QFrame();left.setStyleSheet("background:transparent;")
        controls=QVBoxLayout(left);controls.setContentsMargins(4,4,12,4);controls.setSpacing(9)
        scroll.setWidget(left);body.addWidget(scroll)
        def section(name):
            label=QLabel(name);label.setStyleSheet("color:%s;font-size:11px;font-weight:700;letter-spacing:2px;margin-top:11px;"%muted)
            controls.addWidget(label)
        def line(label,widget):
            text=QLabel(label);controls.addWidget(text);controls.addWidget(widget)
        base=[self._overlay_base];foreground=[QColor(self._overlay_color)];outline=[QColor(self._overlay_outline)]
        section(labels[1])
        image_row=QHBoxLayout()
        image_name=QLabel(Path(base[0]).name if base[0] else labels[20]);image_name.setWordWrap(True)
        image_row.addWidget(image_name,1)
        choose=QPushButton(labels[2]);image_row.addWidget(choose)
        controls.addLayout(image_row)
        section(labels[3])
        content=QTextEdit();content.setPlaceholderText(labels[21]);content.setFixedHeight(78)
        content.setPlainText(self._overlay_text);controls.addWidget(content)
        section(labels[4])
        fonts=QFontComboBox()
        # Qt renders each list entry in its own installed font.
        fonts.setCurrentFont(QFont(self._overlay_font))
        line(labels[11],fonts)
        font_sample=QLabel(self._overlay_text or "NONIVERUS PosterTile")
        font_sample.setMinimumHeight(54);font_sample.setAlignment(Qt.AlignCenter)
        font_sample.setStyleSheet("background:%s;color:%s;border:1px solid %s;border-radius:8px;"%(panel,ink,muted))
        controls.addWidget(font_sample)
        def spin(v,lo,hi):
            w=QDoubleSpinBox();w.setDecimals(1);w.setRange(lo,hi);w.setValue(v);w.setSingleStep(1.0)
            return w
        size=spin(self._overlay_size,1,60);line(labels[12],size)
        style_row=QHBoxLayout()
        bold=QCheckBox(labels[18]);bold.setChecked(self._overlay_bold)
        italic=QCheckBox(labels[19]);italic.setChecked(getattr(self,"_overlay_italic",False))
        style_row.addWidget(bold);style_row.addWidget(italic);controls.addLayout(style_row)
        section(labels[5])
        stroke=spin(self._overlay_outline_width,0,10);line(labels[15],stroke)
        def color_button(ref,name):
            btn=QPushButton()
            def refresh():
                btn.setText(name+"    "+ref[0].name().upper())
                btn.setStyleSheet("QPushButton {text-align:left;border-left:6px solid %s;}"%ref[0].name())
            def pick():
                col=QColorDialog.getColor(ref[0],dlg,name)
                if col.isValid():ref[0]=col;refresh();queue_preview()
            btn.clicked.connect(pick);refresh()
            return btn,refresh
        foreground_button,refresh_foreground=color_button(foreground,labels[16])
        outline_button,refresh_outline=color_button(outline,labels[17])
        controls.addWidget(foreground_button)
        controls.addWidget(outline_button)
        # Quick premium swatches; the existing full colour picker stays available.
        # Colours are user choices, not hard-coded in the exported composition.
        def add_palette(label,ref,palette,refresh_button):
            caption=QLabel(label)
            caption.setStyleSheet("font-size:10px;font-weight:600;color:%s;"%muted)
            controls.addWidget(caption)
            row=QHBoxLayout()
            row.setSpacing(5)
            for hex_color in palette:
                swatch=QPushButton()
                swatch.setFixedSize(30,30)
                swatch.setToolTip(hex_color)
                swatch.setAccessibleName(label+" "+hex_color)
                swatch.setStyleSheet(
                    "QPushButton {background:%s;border:2px solid %s;"
                    "border-radius:8px;padding:0;}"%(hex_color,bronze)
                )
                def choose_color(_checked=False,color=hex_color,destination=ref):
                    destination[0]=QColor(color)
                    refresh_button()
                    queue_preview()
                swatch.clicked.connect(choose_color)
                row.addWidget(swatch)
            row.addStretch(1)
            controls.addLayout(row)
        add_palette(labels[16],foreground,
                    ["#FFFFFF","#142D4A","#0C1426","#C79053",
                     "#D94146","#306AB3","#29765C","#FFE6B2"],
                    refresh_foreground)
        add_palette(labels[17],outline,
                    ["#FFFFFF","#0C1426","#142D4A","#B67945",
                     "#000000","#D94146","#336AB6","#F5D7A0"],
                    refresh_outline)
        section(labels[6])
        xpos=spin(self._overlay_x,0,100);line(labels[13],xpos)
        ypos=spin(self._overlay_y,0,100);line(labels[14],ypos)
        controls.addStretch()
        # Interactive image coordinates are mapped through the aspect-fitted image.
        # This prevents the text from jumping on letterboxed images or on resize.
        hints={
          "pt-PT":("Arrasta o texto sobre a imagem para o posicionar","Guias","Centrar"),
          "en":("Drag the text over the image to position it","Guides","Center"),
          "es":("Arrastra el texto sobre la imagen para colocarlo","Guías","Centrar"),
          "fr":("Faites glisser le texte sur l’image pour le positionner","Repères","Centrer"),
          "it":("Trascina il testo sull’immagine per posizionarlo","Guide","Centra"),
        }[lang]

        class DragPreview(QLabel):
            def __init__(self):
                super().__init__()
                self.setMouseTracking(True)
                self._image_dimensions=None
                self._text_bounds=None
                self._selected=True
                self._dragging=False
                self._press_at=(0.0,0.0)
                self._initial=(50.0,50.0)
                self._snap_x=False
                self._snap_y=False
                self.on_resize=None

            def _fit(self):
                if not self._image_dimensions:
                    return None
                return fitted_image_rect(
                    float(self.width()),float(self.height()),
                    float(self._image_dimensions[0]),float(self._image_dimensions[1])
                )

            def _hit_text(self, point):
                if self._text_bounds is None or self._image_dimensions is None:
                    return False
                fitted=self._fit()
                if not fitted:
                    return False
                b=self._text_bounds
                mapped=image_rect_to_view(
                    (b.x(),b.y(),b.width(),b.height()),
                    fitted,*self._image_dimensions
                )
                return point_hits_rect(point.x(),point.y(),mapped,10)

            def mousePressEvent(self,event):
                if event.button()==Qt.LeftButton:
                    if self._hit_text(event.position()):
                        self._selected=True
                        self._dragging=True
                        self._press_at=(event.position().x(),event.position().y())
                        self._initial=(xpos.value(),ypos.value())
                        self.setCursor(Qt.ClosedHandCursor)
                    else:
                        self._selected=False
                        self._snap_x=self._snap_y=False
                        self.setCursor(Qt.ArrowCursor)
                    queue_preview()
                    event.accept()
                    return
                super().mousePressEvent(event)

            def mouseMoveEvent(self,event):
                if self._dragging:
                    fitted=self._fit()
                    if fitted:
                        px,py,sx,sy=drag_anchor(
                            self._initial[0],self._initial[1],
                            event.position().x()-self._press_at[0],
                            event.position().y()-self._press_at[1],
                            fitted[2],fitted[3],
                        )
                        self._snap_x=sx
                        self._snap_y=sy
                        # These controls also keep the stored export coordinates in sync.
                        xpos.setValue(round(px,1))
                        ypos.setValue(round(py,1))
                        queue_preview()
                    event.accept()
                    return
                self.setCursor(Qt.OpenHandCursor if self._hit_text(event.position()) else Qt.ArrowCursor)
                super().mouseMoveEvent(event)

            def mouseReleaseEvent(self,event):
                if event.button()==Qt.LeftButton and self._dragging:
                    self._dragging=False
                    self.setCursor(Qt.OpenHandCursor if self._hit_text(event.position()) else Qt.ArrowCursor)
                    queue_preview()
                    event.accept()
                    return
                super().mouseReleaseEvent(event)

            def resizeEvent(self,event):
                super().resizeEvent(event)
                if self.on_resize:
                    self.on_resize()

        right=QFrame();right.setObjectName("previewFrame")
        right_layout=QVBoxLayout(right);right_layout.setContentsMargins(15,15,15,15)
        title_row=QHBoxLayout()
        preview_title=QLabel(labels[7]);preview_title.setStyleSheet("font-size:11px;font-weight:700;letter-spacing:2px;color:%s;"%muted)
        title_row.addWidget(preview_title)
        title_row.addStretch()
        guides=QCheckBox(hints[1]);guides.setChecked(True)
        title_row.addWidget(guides)
        center=QPushButton(hints[2]);center.setFixedWidth(88)
        title_row.addWidget(center)
        right_layout.addLayout(title_row)
        preview=DragPreview();preview.setAlignment(Qt.AlignCenter);preview.setMinimumSize(330,250)
        preview.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        right_layout.addWidget(preview,1)
        drag_hint=QLabel(hints[0]);drag_hint.setAlignment(Qt.AlignCenter)
        drag_hint.setStyleSheet("color:%s;font-size:11px;"%muted)
        right_layout.addWidget(drag_hint)
        tip=QLabel("NONIVERUS  /  "+("Vista ilustrativa • exportação pela mesma composição" if lang=="pt-PT" else "Live composition • same rendering used for export"))
        tip.setAlignment(Qt.AlignCenter);tip.setStyleSheet("color:%s;font-size:11px;"%muted)
        right_layout.addWidget(tip)
        body.addWidget(right,1)
        buttons=QHBoxLayout()
        reset=QPushButton(labels[10]);cancel=QPushButton(labels[9]);apply=QPushButton(labels[8]);apply.setObjectName("primary")
        buttons.addWidget(reset);buttons.addStretch();buttons.addWidget(cancel);buttons.addWidget(apply)
        main.addLayout(buttons)
        def render(maxside=1100, with_bounds=False):
            """Render the exact composition. Editor guides are drawn separately."""
            if not base[0] or not Path(base[0]).is_file():
                return (None,None) if with_bounds else None
            with Image.open(base[0]) as src:
                im=ImageOps.exif_transpose(src).convert("RGBA")
                iw,ih=im.size
                ratio=min(1.,maxside/max(iw,ih))
                if ratio<1.:
                    im=im.resize((max(1,round(iw*ratio)),max(1,round(ih*ratio))),Image.Resampling.LANCZOS)
                canvas=QImage(ImageQt(im)).convertToFormat(QImage.Format_ARGB32)
            txt=content.toPlainText().strip()
            if not txt:
                return (canvas,None) if with_bounds else canvas
            font=QFont(fonts.currentFont().family())
            font.setBold(bold.isChecked());font.setItalic(italic.isChecked())
            font.setPixelSize(max(6,round(canvas.height()*size.value()/100)))
            fm=QFontMetrics(font);lines=txt.splitlines()[:5]
            maxwidth=max((fm.horizontalAdvance(line) for line in lines),default=0)
            if maxwidth>canvas.width()*.96:
                font.setPixelSize(max(6,round(font.pixelSize()*canvas.width()*.96/maxwidth)))
                fm=QFontMetrics(font)
            baseline=canvas.height()*ypos.value()/100-fm.lineSpacing()*len(lines)/2+fm.ascent()
            painter=QPainter(canvas);painter.setRenderHints(QPainter.Antialiasing|QPainter.TextAntialiasing)
            pen=QPen(outline[0]);pen.setWidthF(max(.1,canvas.height()*stroke.value()/100))
            pen.setJoinStyle(Qt.RoundJoin)
            glyph_bounds=None
            for line_text in lines:
                x=canvas.width()*xpos.value()/100-fm.horizontalAdvance(line_text)/2
                path=QPainterPath();path.addText(x,baseline,font,line_text)
                if not path.isEmpty():
                    box=path.boundingRect()
                    glyph_bounds=box if glyph_bounds is None else glyph_bounds.united(box)
                if stroke.value()>0:painter.strokePath(path,pen)
                painter.fillPath(path,foreground[0]);baseline+=fm.lineSpacing()
            painter.end()
            if glyph_bounds is not None:
                extra=pen.widthF()/2 if stroke.value()>0 else 0
                glyph_bounds=glyph_bounds.adjusted(-extra,-extra,extra,extra)
            return (canvas,glyph_bounds) if with_bounds else canvas

        timer=QTimer(dlg);timer.setSingleShot(True);timer.setInterval(45)
        def update_preview():
            try:
                samplefont=QFont(fonts.currentFont().family(),21)
                samplefont.setBold(bold.isChecked());samplefont.setItalic(italic.isChecked())
                font_sample.setFont(samplefont)
                text=(content.toPlainText().strip().splitlines() or ["NONIVERUS"])[0]
                font_sample.setText(text[:36] or "NONIVERUS")
                img,bounds=render(1200,with_bounds=True)
                if img is None:
                    preview._image_dimensions=None
                    preview._text_bounds=None
                    preview.setText(labels[20])
                    return
                preview._image_dimensions=(img.width(),img.height())
                preview._text_bounds=bounds
                if abs(xpos.value()-50.0)>0.05:
                    preview._snap_x=False
                if abs(ypos.value()-50.0)>0.05:
                    preview._snap_y=False
                # The source QImage stays untouched: selection marks and guidelines
                # appear only on the displayed copy, never in the export.
                if bounds is not None or guides.isChecked():
                    img=img.copy()
                    painter=QPainter(img)
                    painter.setRenderHint(QPainter.Antialiasing,True)
                    if guides.isChecked():
                        guide_color=QColor("#548BAA" if light else "#83B6D5")
                        guide_color.setAlpha(170 if preview._dragging else 65)
                        guide_pen=QPen(guide_color,1,Qt.DashLine)
                        painter.setPen(guide_pen)
                        painter.drawLine(img.width()//2,0,img.width()//2,img.height())
                        painter.drawLine(0,img.height()//2,img.width(),img.height()//2)
                    if preview._selected and bounds is not None:
                        box=bounds.adjusted(-6,-6,6,6)
                        active=QColor(bronze)
                        selection_pen=QPen(active,2,Qt.DashLine)
                        painter.setPen(selection_pen)
                        painter.setBrush(Qt.NoBrush)
                        painter.drawRoundedRect(box,3,3)
                        painter.setPen(QPen(QColor("#FFFFFF"),1))
                        painter.setBrush(active)
                        for cx,cy in ((box.left(),box.top()),(box.right(),box.top()),
                                      (box.left(),box.bottom()),(box.right(),box.bottom())):
                            painter.drawRect(QRectF(cx-5,cy-5,10,10))
                    if preview._snap_x or preview._snap_y:
                        strong=QPen(QColor("#CC8B43"),2,Qt.SolidLine)
                        painter.setPen(strong)
                        if preview._snap_x:
                            painter.drawLine(img.width()//2,0,img.width()//2,img.height())
                        if preview._snap_y:
                            painter.drawLine(0,img.height()//2,img.width(),img.height()//2)
                    painter.end()
                target=preview.size()
                preview.setPixmap(QPixmap.fromImage(img).scaled(target,Qt.KeepAspectRatio,Qt.SmoothTransformation))
            except Exception as exc:
                preview.setText(str(exc))
        def queue_preview(*_):timer.start()
        preview.on_resize=queue_preview
        timer.timeout.connect(update_preview)
        for widget,signal in ((content,content.textChanged),(fonts,fonts.currentFontChanged),(size,size.valueChanged),
                              (xpos,xpos.valueChanged),(ypos,ypos.valueChanged),(stroke,stroke.valueChanged),
                              (bold,bold.toggled),(italic,italic.toggled),(guides,guides.toggled)):
            signal.connect(queue_preview)
        def center_text():
            preview._selected=True
            preview._snap_x=True
            preview._snap_y=True
            xpos.setValue(50.0)
            ypos.setValue(50.0)
            queue_preview()
        center.clicked.connect(center_text)
        def choose_base():
            path,_=QFileDialog.getOpenFileName(dlg,labels[2],str(Path.home()),"Images (*.png *.jpg *.jpeg *.webp *.tif *.tiff *.bmp)")
            if path:
                base[0]=path;image_name.setText(Path(path).name);queue_preview()
        choose.clicked.connect(choose_base)
        cancel.clicked.connect(dlg.reject)
        def reset_controls():
            content.setPlainText("");size.setValue(12);xpos.setValue(50);ypos.setValue(50)
            stroke.setValue(2);bold.setChecked(True);italic.setChecked(False);queue_preview()
        reset.clicked.connect(reset_controls)
        def save_composition():
            try:
                text=content.toPlainText().strip()
                if not base[0] or not Path(base[0]).is_file():raise ValueError(labels[20])
                if not text or len(text)>250 or len(text.splitlines())>5:
                    raise ValueError("Máximo 250 caracteres e 5 linhas; o texto não pode estar vazio.")
                canvas=render(4000)
                folder=Path(os.getenv("LOCALAPPDATA",str(Path.home())))/"NONIVERUS"/"PosterTile"/"compositions"
                folder.mkdir(parents=True,exist_ok=True)
                from uuid import uuid4
                output=folder/("image_text_"+uuid4().hex+".png")
                if canvas is None or not canvas.save(str(output),"PNG"):raise IOError("Não foi possível guardar a composição.")
                self._overlay_base=base[0];self._overlay_text=text
                self._overlay_font=fonts.currentFont().family();self._overlay_size=size.value()
                self._overlay_x=xpos.value();self._overlay_y=ypos.value()
                self._overlay_color=foreground[0].name();self._overlay_outline=outline[0].name()
                self._overlay_outline_width=stroke.value();self._overlay_bold=bold.isChecked()
                self._overlay_italic=italic.isChecked()
                self._path=str(output);self._source_mode="composition"
                self._ratio=canvas.width()/canvas.height();self._width=self._height*self._ratio
                self._a3two_orientation=None
                self._status={
                  "pt-PT":"Imagem e texto preparados. Confirma as medidas antes de exportar.",
                  "en":"Image and text ready. Check dimensions before exporting.",
                  "es":"Imagen y texto listos. Comprueba las dimensiones antes de exportar.",
                  "fr":"Image et texte prêts. Vérifiez les dimensions avant l’export.",
                  "it":"Immagine e testo pronti. Verifica le dimensioni prima di esportare."
                }[lang]
                self.changed.emit();dlg.accept()
            except Exception as exc:
                QMessageBox.warning(dlg,"NONIVERUS",str(exc))
        apply.clicked.connect(save_composition)
        QTimer.singleShot(100,update_preview)
        dlg.exec()

    @Slot(str)
    def setHeight(self,v):
        h=self.number(v,self._height)
        if not .1<=h<=1000:self.notice.emit("Altura entre 0,1 e 1000 cm.");return
        self._height=h;self._width=h*self._ratio;self._a3two_orientation=None;self.changed.emit()
    @Slot(str)
    def setWidth(self,v):
        w=self.number(v,self._width)
        if not .1<=w<=1000:self.notice.emit("Largura entre 0,1 e 1000 cm.");return
        self._width=w;self._height=w/self._ratio;self._a3two_orientation=None;self.changed.emit()
    @Slot(str)
    def setFormat(self,value):
        sizes={"A3 horizontal (2 A4)":(42.,29.7),
               "A3 vertical (2 A4)":(29.7,42.),
               "A3 horizontal":(42.,29.7),"A3 vertical":(29.7,42.),
               "A2 horizontal":(59.4,42.),"A2 vertical":(42.,59.4),
               "A1 horizontal":(84.1,59.4),"A1 vertical":(59.4,84.1)}
        self._a3two_orientation = ("horizontal" if value=="A3 horizontal (2 A4)"
                                 else "vertical" if value=="A3 vertical (2 A4)" else None)
        if self._a3two_orientation: self._a3two_mode="safe"
        if value in sizes:
            self._width,self._height=sizes[value]
        self.changed.emit()
    @Slot(str,str,str,str)
    def configure(self,paper,assembly,margin,overlap):
        self._paper=paper if paper in ("Auto","A4 vertical","A4 horizontal","A3 vertical","A3 horizontal") else "Auto"
        self._assembly=assembly if assembly in ("Sobrepor","Cortar e unir") else "Sobrepor"
        self._margin=self.number(margin,8)
        self._overlap=self.number(overlap,10)
        self.changed.emit()
    @Property(str,notify=changed)
    def calibrationStatus(self):
        try:
            profile=pc.get(self._selected_printer,self._calibration_paper())
            return ("Calibrada: "+self._selected_printer) if profile else ("Sem calibração: "+self._selected_printer if self._selected_printer else "Calibração não selecionada")
        except Exception:
            return "Perfis indisponíveis"
    def _calibration_paper(self):
        return self._make_plan()["orientation"]
    @Slot()
    def calibrationDialog(self):
        try:
            from PySide6.QtPrintSupport import QPrinterInfo
            printers=[p.printerName() for p in QPrinterInfo.availablePrinters()]
        except Exception: printers=[]
        dlg=QDialog()
        dlg.setWindowTitle("NONIVERUS | Precision Printer Calibration")
        dlg.setMinimumWidth(490)
        layout=QVBoxLayout(dlg)
        layout.addWidget(QLabel("1. Escolhe a impressora e o formato que vais utilizar."))
        form=QFormLayout()
        printer=QComboBox();printer.setEditable(True)
        printer.addItems(printers)
        if self._selected_printer:printer.setCurrentText(self._selected_printer)
        paper=QComboBox();paper.addItems(list(pc.DIMS))
        selected=self._calibration_paper()
        paper.setCurrentText(selected if selected in pc.DIMS else "A4 vertical")
        mx=QLineEdit();my=QLineEdit()
        form.addRow("Impressora:",printer)
        form.addRow("Papel e orientação:",paper)
        form.addRow("X medido (mm):",mx)
        form.addRow("Y medido (mm):",my)
        layout.addLayout(form)
        info=QLabel()
        info.setWordWrap(True)
        layout.addWidget(info)
        def refresh():
            ry=pc.reference_y(paper.currentText())
            profile=pc.get(printer.currentText(),paper.currentText())
            info.setText(f"Imprime a folha de teste a 100%. Mede X = 150,0 mm e Y = {ry:.1f} mm. "
                         "Introduz os valores realmente medidos. "
                         "Cada impressora, papel e orientação têm um perfil independente.")
            if profile:
                mx.setText(str(profile["measured_x"]))
                my.setText(str(profile["measured_y"]))
            else: mx.clear();my.clear()
        paper.currentTextChanged.connect(refresh)
        printer.currentTextChanged.connect(refresh)
        refresh()
        buttons=QHBoxLayout()
        generate=QPushButton("Gerar folha de teste")
        save=QPushButton("Guardar e utilizar perfil")
        buttons.addWidget(generate);buttons.addWidget(save)
        layout.addLayout(buttons)
        def gen():
            name=printer.currentText().strip()
            if not name: QMessageBox.warning(dlg,"NONIVERUS","Indica uma impressora.");return
            dest,_=QFileDialog.getSaveFileName(dlg,"Guardar teste",str(Path.home()/"NONIVERUS_CALIBRACAO.pdf"),"PDF (*.pdf)")
            if dest:
                try:
                    pc.make_test_pdf(dest,paper.currentText(),name)
                    QMessageBox.information(dlg,"NONIVERUS","Imprime este PDF na impressora selecionada, a 100%, sem ajustar à página. Depois mede com régua.")
                except Exception as e: QMessageBox.warning(dlg,"Erro",str(e))
        def store():
            try:
                name=printer.currentText().strip()
                pc.save(name,paper.currentText(),mx.text().replace(",","."),my.text().replace(",","."))
                self._selected_printer=name
                self._settings.setValue("printer/selected",name);self._settings.sync()
                self.changed.emit()
                dlg.accept()
            except Exception as e: QMessageBox.warning(dlg,"Erro no perfil",str(e))
        generate.clicked.connect(gen);save.clicked.connect(store)
        dlg.exec()
    @Slot()
    def export(self):
        # Second independent gate: a license removed/expired while the UI is open
        # must not permit PDF creation. The native Rust verifier is fail-closed.
        if EDITION == "preview":
            from license_runtime import is_activated
            if not is_activated(BASE):
                self.notice.emit("Licença Private Preview inválida ou expirada. Fecha e reabre a aplicação para ativar.")
                return
        if not self._path:self.notice.emit("Primeiro, seleciona uma imagem.");return
        try:
            p=self._make_plan()
            if p["pages"]>150:raise ValueError("O projeto ultrapassa 150 folhas.")
            target,_=QFileDialog.getSaveFileName(None,"Exportar PDF",str(Path(self._path).with_suffix(""))+"_NONIVERUS.pdf","PDF (*.pdf)")
            if not target:return
            if not target.lower().endswith(".pdf"):target+=".pdf"
            calibration=pc.get(self._selected_printer,self._calibration_paper()) if self._selected_printer else None
            if calibration:
                answer=QMessageBox.question(None,"NONIVERUS | Perfil de calibração",
                    f"Perfil: {self._selected_printer} / {self._calibration_paper()}\\n"
                    "A compensação será aplicada ao PDF.\\n\\n"
                    "Imprime nesta mesma impressora, com o mesmo controlador e a 100%. "
                    "Se mudares as opções de redimensionamento, o resultado pode ficar incorreto.\\n\\nContinuar?",
                    QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                if answer!=QMessageBox.Yes:return
            if self._a3two_orientation:
                if self._a3two_mode=="borderless":
                    answer=QMessageBox.warning(None,"NONIVERUS · A3 em 2 A4",
                        "A3 exato com 2 folhas A4 só é possível com impressão "
                        "SEM MARGENS (borderless), a 100%.\\n\\n"
                        "Uma impressora A4 com margens normais deixará faixas "
                        "brancas no centro e nas extremidades.\\n\\n"
                        "Confirmas que a tua impressora suporta A4 sem margens?",
                        QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
                    if answer!=QMessageBox.Yes:return
                p=export_a3_two_a4(self._path,target,self._a3two_orientation,
                                     self._a3two_mode,self._margin,calibration=calibration,
                                     fit=self._fit,focal_x=self._focal_x,
                                     focal_y=self._focal_y)
            else:
                p=export_pdf(self._path,target,self._width*10,self._height*10,
                             margin=self._margin,overlap=self._overlap,
                             paper=self._paper,assembly=self._assembly,
                             fit=self._fit,marks=True,calibration=calibration,language=self._language,
                             focal_x=self._focal_x,focal_y=self._focal_y)
            self._status=f"PDF pronto: {target}"
            self.changed.emit()
            if self._a3two_orientation:
                if self._a3two_mode=="safe":
                    hint=("\\n\\nModo seguro: recorta as duas margens brancas "
                          "interiores e une as áreas de imagem. A montagem "
                          "é ligeiramente menor do que A3.")
                else:
                    hint="\\n\\nExige A4 sem margens (borderless), a 100%."
                self.notice.emit(f"PDF pronto: 2 folhas {p['orientation']}"+hint)
            else:
                self.notice.emit(f"PDF exportado com sucesso.\n\n{p['pages']} folhas de {p['orientation']}\n\nImprime a 100% / Tamanho real. Não uses «Ajustar à página».")
        except Exception as ex:self.notice.emit(f"Erro ao exportar PDF:\n{ex}")

def main():
    app=QApplication(sys.argv)
    app.setOrganizationName("NONIVERUS")
    app.setApplicationName("NONIVERUS PosterTile Luxury Studio")
    app.setApplicationDisplayName("NONIVERUS PosterTile Luxury Studio")
    app.setWindowIcon(QIcon(str(BASE/"assets"/"branding"/"postertile_icon.ico")))
    if EDITION == "preview":
        from license_runtime import activate_interactively, native_path
        if not native_path(BASE).is_file():
            QMessageBox.critical(None, "NONIVERUS Private Preview",
                "Verificador de licença não encontrado. Reinstala a edição Private Preview.")
            return 5
        if not activate_interactively(BASE):
            return 3
    bridge=Studio()
    engine=QQmlApplicationEngine()
    engine.rootContext().setContextProperty("studio",bridge)
    engine.load(QUrl.fromLocalFile(str(BASE/"ui"/"Main.qml")))
    if not engine.rootObjects():
        print("ERRO: Não foi possível carregar ui/Main.qml",file=sys.stderr)
        return 1
    return app.exec()

if __name__=="__main__":sys.exit(main())
