# -*- coding: utf-8 -*-
"""NONIVERUS PosterTile Studio v0.5 — Windows desktop interface."""
import sys, os, math
from pathlib import Path
from PIL import Image, ImageOps
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPixmap, QImage, QFont, QLinearGradient, QPolygonF
from PySide6.QtWidgets import (
    QApplication,QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QLabel,QPushButton,
    QFrame,QComboBox,QSpinBox,QDoubleSpinBox,QLineEdit,QFileDialog,QMessageBox,
    QScrollArea,QCheckBox,QGridLayout,QGraphicsDropShadowEffect,QButtonGroup,
)
from postertile_engine import plan, export_pdf, SIZES

CSS = """
QWidget { background:#071423; color:#E8F1FF; font-family:'Segoe UI'; font-size:13px; }
QFrame#side,QFrame#stage,QFrame#info {background:#10243A; border:1px solid #24415F;border-radius:20px;}
QFrame#mini {background:#15304A;border:1px solid #2B4A69;border-radius:14px;}
QPushButton {background:#1D3B59; border:1px solid #355675; border-radius:11px; color:#EAF4FF;
 padding:10px 12px; font-weight:600;}
QPushButton:hover {background:#285175;border-color:#75B8F8;}
QPushButton:pressed {background:#142D46;}
QPushButton#primary {background:#FF9C42; color:#132037;border:0;font-weight:800;padding:14px;}
QPushButton#primary:hover {background:#FFB76A;}
QPushButton#mode {padding:14px 7px;background:#17334F;}
QPushButton#mode:checked {background:#2763A0;border:1px solid #FFB15A;color:white;}
QComboBox,QDoubleSpinBox,QSpinBox,QLineEdit {background:#091B2C;border:1px solid #38536C;
border-radius:9px;min-height:31px;padding:3px 10px;selection-background-color:#2775C2;}
QComboBox QAbstractItemView {background:#10243A;selection-background-color:#28659D;}
QCheckBox {spacing:9px;}
QScrollArea {border:0;background:transparent;}
QScrollBar:vertical {background:#10243A;width:9px;}
QScrollBar::handle:vertical {background:#3C617F;border-radius:4px;}
"""

def label(text,color="#AFC4DA",size=12,bold=False):
    w=QLabel(text);w.setStyleSheet(f"background:transparent;color:{color};font-size:{size}px;font-weight:{'800' if bold else '400'};")
    w.setWordWrap(True)
    return w

def section(parent,title):
    parent.addWidget(label(title,"#FFAF69",11,True))

def shadow(w):
    effect=QGraphicsDropShadowEffect(w)
    effect.setBlurRadius(35);effect.setOffset(0,12);effect.setColor(QColor(0,0,0,90));w.setGraphicsEffect(effect)

def image_preview(path):
    with Image.open(path) as original:
        im=ImageOps.exif_transpose(original).convert("RGBA")
        if original.mode in ("RGBA","LA","P"):
            b=im.getchannel("A").point(lambda v:255 if v>8 else 0).getbbox()
            if b:im=im.crop(b)
        im.thumbnail((1250,1250))
        bg=Image.new("RGBA",im.size,"white")
        return Image.alpha_composite(bg,im).convert("RGB"),im.size

class Preview(QWidget):
    dropped=Signal(str)
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(340);self.setAcceptDrops(True)
        self.details=None;self.pix=None;self.perspective=True
    def dragEnterEvent(self,e):
        if e.mimeData().hasUrls() and any(u.isLocalFile() for u in e.mimeData().urls()):e.acceptProposedAction()
    def dropEvent(self,e):
        for u in e.mimeData().urls():
            if u.isLocalFile():self.dropped.emit(u.toLocalFile());break
    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.Antialiasing);p.fillRect(self.rect(),QColor("#0A2036"))
        ww=self.width();hh=self.height()
        grad=QLinearGradient(0,0,ww,hh);grad.setColorAt(0,QColor("#123653"));grad.setColorAt(1,QColor("#071A2E"))
        p.fillRect(self.rect(),grad)
        if not self.details:
            p.setPen(QColor("#9FC0DA"));p.setFont(QFont("Segoe UI",15, QFont.Weight.DemiBold))
            p.drawText(self.rect(),Qt.AlignCenter,"ARRASTA UMA IMAGEM PARA AQUI\nou utiliza «Abrir imagem»")
            return
        w,h,tile=self.details
        if w<=0 or h<=0:return
        scale=min((ww-110)/w,(hh-110)/h)
        if scale<=0:return
        x=(ww-w*scale)/2;y=(hh-h*scale)/2
        p.save()
        if self.perspective:
            p.translate(ww/2,hh/2)
            p.rotate(-5)
            p.shear(-0.085,0.0)
            p.translate(-ww/2,-hh/2)
        target=QRectF(x,y,w*scale,h*scale)
        p.fillRect(target.translated(9,13),QColor(0,0,0,95))
        p.fillRect(target,QColor("#FBFDFF"))
        if self.pix:
            iw,ih=self.pix.width(),self.pix.height()
            f=min(w/iw,h/ih)
            aw,ah=iw*f,ih*f
            imgrect=QRectF(x+(w-aw)*scale/2,y+(h-ah)*scale/2,aw*scale,ah*scale)
            p.save();p.setClipRect(target);p.drawPixmap(imgrect,self.pix,QRectF(self.pix.rect()));p.restore()
        for r,(yy,sh) in enumerate(tile["ys"]):
            for c,(xx,sw) in enumerate(tile["xs"]):
                tile_rect=QRectF(x+xx*scale,y+yy*scale,sw*scale,sh*scale)
                p.setPen(QPen(QColor("#FEA44C"),1.4,Qt.DashLine));p.setBrush(Qt.NoBrush)
                p.drawRect(tile_rect)
                p.setPen(QColor("#102B45"));p.setFont(QFont("Segoe UI",10,QFont.Weight.Bold))
                p.drawText(tile_rect.adjusted(5,4,-5,-5),Qt.AlignTop|Qt.AlignLeft,str(r*tile["nx"]+c+1))
        p.restore()
        p.setPen(QColor("#B9D2E8"));p.setFont(QFont("Segoe UI",10))
        p.drawText(QRectF(0,hh-30,ww,20),Qt.AlignCenter,
                   "Pré-visualização visual · o PDF mantém a geometria exata")
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NONIVERUS | PosterTile Studio v0.5")
        self.resize(1360,870);self.setMinimumSize(990,690)
        self.image_path=None;self.image_size=None;self.current_plan=None
        self.setStyleSheet(CSS)
        shell=QWidget();self.setCentralWidget(shell)
        root=QVBoxLayout(shell);root.setContentsMargins(22,18,22,18);root.setSpacing(13)
        head=QHBoxLayout()
        word=label("◈  NONIVERUS", "#E8F5FF",24,True)
        head.addWidget(word)
        head.addWidget(label("POSTERTILE  /  PREMIUM STUDIO", "#FFAD62",12,True))
        head.addStretch()
        head.addWidget(label("v0.5 • WINDOWS DESKTOP","#85A8C5",11))
        root.addLayout(head)
        modes=QHBoxLayout();modes.setSpacing(9);self.modebuttons={}
        for key,desc in [("Kids","✦  KIDS · Bonecos gigantes"),("Maker","▧  MAKER · Moldes"),("Pro","◈  PRO · Posters")]:
            btn=QPushButton(desc);btn.setObjectName("mode");btn.setCheckable(True)
            btn.clicked.connect(lambda checked,k=key:self.set_mode(k))
            modes.addWidget(btn);self.modebuttons[key]=btn
        modes.addStretch();root.addLayout(modes)
        content=QHBoxLayout();content.setSpacing(14);root.addLayout(content,1)
        scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setFixedWidth(365)
        self.side=QFrame();self.side.setObjectName("side")
        left=QVBoxLayout(self.side);left.setContentsMargins(18,18,18,18);left.setSpacing(9)
        self.open_btn=QPushButton("＋  1 · Abrir imagem / personagem")
        self.open_btn.clicked.connect(self.open_image);left.addWidget(self.open_btn)
        self.filename=label("Nenhuma imagem selecionada","#91AFCB",11);left.addWidget(self.filename)
        section(left,"DIMENSÕES REAIS")
        self.height_label=label("Altura do boneco (cm)","#E6F2FC")
        left.addWidget(self.height_label)
        self.height=QDoubleSpinBox();self.height.setRange(10,300);self.height.setValue(120);self.height.setDecimals(0);self.height.setSuffix(" cm")
        left.addWidget(self.height)
        self.poster_size=QComboBox();self.poster_size.addItems(["A2","A1","Personalizado"])
        self.orient=QComboBox();self.orient.addItems(["Horizontal","Vertical"])
        self.custom_w=QDoubleSpinBox();self.custom_w.setRange(10,3000);self.custom_w.setValue(594);self.custom_w.setSuffix(" mm")
        self.custom_h=QDoubleSpinBox();self.custom_h.setRange(10,3000);self.custom_h.setValue(420);self.custom_h.setSuffix(" mm")
        self.poster_fields=[]
        for name,widget in [("Formato",self.poster_size),("Orientação",self.orient),("Largura",self.custom_w),("Altura",self.custom_h)]:
            l=label(name);left.addWidget(l);left.addWidget(widget);self.poster_fields.extend([l,widget])
        section(left,"IMPRESSÃO E MONTAGEM")
        self.paper=QComboBox();self.paper.addItems(["Auto","A4 vertical","A4 horizontal"])
        self.assembly=QComboBox();self.assembly.addItems(["Sobrepor","Cortar e unir"])
        self.fit=QComboBox();self.fit.addItems(["Ajustar","Preencher"])
        self.margin=QDoubleSpinBox();self.margin.setRange(0,30);self.margin.setValue(8);self.margin.setSuffix(" mm")
        self.overlap=QDoubleSpinBox();self.overlap.setRange(0,30);self.overlap.setValue(10);self.overlap.setSuffix(" mm")
        self.correction=QDoubleSpinBox();self.correction.setRange(50,150);self.correction.setValue(100);self.correction.setSuffix(" %")
        for name,widget in [("Folhas A4",self.paper),("Montagem",self.assembly),("Sobreposição",self.overlap),
                            ("Margem de segurança",self.margin),("Enquadramento",self.fit),("Calibração de escala",self.correction)]:
            left.addWidget(label(name));left.addWidget(widget)
        self.marks=QCheckBox("Marcas de registo");self.marks.setChecked(True);left.addWidget(self.marks)
        self.export_btn=QPushButton("✦  2 · Gerar PDF A4");self.export_btn.setObjectName("primary")
        self.export_btn.clicked.connect(self.export);left.addWidget(self.export_btn)
        scroll.setWidget(self.side);content.addWidget(scroll)
        right=QVBoxLayout();right.setSpacing(12);content.addLayout(right,1)
        self.stage=QFrame();self.stage.setObjectName("stage")
        st=QVBoxLayout(self.stage);st.setContentsMargins(13,12,13,12)
        toolbar=QHBoxLayout();toolbar.addWidget(label("ESTÚDIO DE MONTAGEM","#FFFFFF",15,True));toolbar.addStretch()
        self.toggle=QPushButton("◈  Perspetiva 3D");self.toggle.setCheckable(True);self.toggle.setChecked(True)
        self.toggle.clicked.connect(self.toggle_3d);toolbar.addWidget(self.toggle)
        st.addLayout(toolbar)
        self.preview=Preview();self.preview.dropped.connect(self.load_image)
        st.addWidget(self.preview,1);right.addWidget(self.stage,1)
        self.info=QFrame();self.info.setObjectName("info")
        summary=QVBoxLayout(self.info)
        summary.addWidget(label("PLANO DE IMPRESSÃO","#FFAD62",12,True))
        self.stats=label("Escolhe uma imagem para gerar o plano.","#E8F3FF",14,True)
        summary.addWidget(self.stats)
        self.details=label("Imprimir sempre a 100% / Tamanho real. Nunca ajustar à página.","#ACC6DF",11)
        summary.addWidget(self.details)
        right.addWidget(self.info)
        self.statusBar().showMessage("NONIVERUS Studio · Pronto")
        for obj in [self.height,self.poster_size,self.orient,self.custom_w,self.custom_h,self.paper,
                    self.assembly,self.fit,self.margin,self.overlap,self.correction]:
            (obj.currentIndexChanged if isinstance(obj,QComboBox) else obj.valueChanged).connect(self.refresh)
        self.set_mode("Kids")
    def set_mode(self,mode):
        self.mode=mode
        for key,btn in self.modebuttons.items():btn.setChecked(key==mode)
        kids=mode=="Kids"
        self.height_label.setVisible(kids);self.height.setVisible(kids)
        for w in self.poster_fields:w.setVisible(not kids)
        self.refresh()
    def toggle_3d(self):
        self.preview.perspective=self.toggle.isChecked();self.preview.update()
    def open_image(self):
        f,_=QFileDialog.getOpenFileName(self,"Escolher imagem","","Imagens (*.png *.jpg *.jpeg *.webp *.bmp *.tif *.tiff)")
        if f:self.load_image(f)
    def load_image(self,path):
        try:
            im,size=image_preview(path)
            buf=im.tobytes("raw","RGB")
            q=QImage(buf,im.width,im.height,im.width*3,QImage.Format_RGB888).copy()
            self.preview.pix=QPixmap.fromImage(q)
            self.image_path=path;self.image_size=size
            self.filename.setText(Path(path).name)
            self.statusBar().showMessage("Imagem carregada: "+Path(path).name)
            self.refresh()
        except Exception as exc:QMessageBox.critical(self,"Imagem inválida",str(exc))
    def settings(self):
        if self.mode=="Kids":
            h=self.height.value()*10
            ratio=(self.image_size[0]/self.image_size[1]) if self.image_size else .6
            w=h*ratio
        elif self.poster_size.currentText()=="Personalizado":
            w=self.custom_w.value();h=self.custom_h.value()
        else:
            a,b=SIZES[self.poster_size.currentText()]
            w,h=(b,a) if self.orient.currentText()=="Horizontal" else (a,b)
        factor=self.correction.value()/100
        w*=factor;h*=factor
        if w>3000 or h>3000:raise ValueError("Tamanho máximo: 300 cm por eixo.")
        p=plan(w,h,self.margin.value(),self.overlap.value(),
               self.paper.currentText(),self.assembly.currentText())
        if p["pages"]>150:raise ValueError("Máximo de 150 folhas.")
        return w,h,p
    def refresh(self,*args):
        try:
            w,h,p=self.settings()
            self.current_plan=p
            self.preview.details=(w,h,p)
            self.stats.setText(f"{w/10:.1f} × {h/10:.1f} cm     •     {p['pages']} folhas A4")
            self.details.setText(f"{p['nx']} colunas × {p['ny']} linhas · {p['orientation']} · {self.assembly.currentText()} · Margem {self.margin.value():g} mm")
        except Exception as exc:
            self.current_plan=None;self.preview.details=None;self.stats.setText(str(exc))
        self.preview.update()
    def export(self):
        if not self.image_path:
            QMessageBox.information(self,"Abrir imagem","Escolhe uma imagem antes de exportar.");return
        try:w,h,p=self.settings()
        except Exception as exc:QMessageBox.warning(self,"Configuração inválida",str(exc));return
        filename=f"NONIVERUS_{self.mode}_{int(h/10)}cm_A4.pdf"
        dest,_=QFileDialog.getSaveFileName(self,"Guardar PDF",str(Path.home()/filename),"PDF (*.pdf)")
        if not dest:return
        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            export_pdf(self.image_path,dest,w,h,self.margin.value(),self.overlap.value(),
                       self.fit.currentText(),self.paper.currentText(),self.assembly.currentText(),self.marks.isChecked())
            QApplication.restoreOverrideCursor()
            self.statusBar().showMessage("PDF criado: "+dest)
            QMessageBox.information(self,"PDF pronto",
               f"PDF criado com {p['pages']} folhas A4.\n\nImprimir a 100% / Tamanho real.\n"
               "Desativar «Ajustar à página».\n\nAntes de imprimir tudo, testar duas folhas adjacentes.")
        except Exception as exc:
            QApplication.restoreOverrideCursor();QMessageBox.critical(self,"Erro ao gerar PDF",str(exc))

if __name__=="__main__":
    app=QApplication(sys.argv);app.setStyle("Fusion")
    window=Main();window.show()
    sys.exit(app.exec())
