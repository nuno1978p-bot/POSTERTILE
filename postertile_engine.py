# -*- coding: utf-8 -*-
"""NONIVERUS PosterTile v0.5 Studio — impressao de posters em folhas A4."""
import math
import os
from PIL import Image, ImageOps
from printer_calibration import page_transform
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from poster_framing import image_placement

MM=72/25.4
PAPERS={"A4":(210.,297.),"A3":(297.,420.)}
A4=PAPERS["A4"]
SIZES={"A2":(420.,594.),"A1":(594.,841.)}
Image.MAX_IMAGE_PIXELS=250_000_000

def axis_spans(length, usable, minimum_overlap):
    """Preenche a primeira folha; distribui o restante sem faixas residuais."""
    if length<=usable+1e-8:
        return [(0.,length)]
    count=math.ceil((length-usable)/(usable-minimum_overlap)-1e-10)+1
    rest=(length-usable)/(count-1)
    spans=[(0.,usable)]
    for i in range(1,count):
        spans.append((usable+(i-1)*rest-minimum_overlap,rest+minimum_overlap))
    return spans

def plan(width,height,margin,overlap,paper="Auto",assembly="Sobrepor"):
    if not all(math.isfinite(x) for x in (width,height,margin,overlap)):
        raise ValueError("Valores numéricos inválidos.")
    if width<=0 or height<=0 or margin<0 or overlap<0:
        raise ValueError("Dimensões, margem ou sobreposição inválidas.")
    layouts=[]
    choices=(["A4 vertical","A4 horizontal","A3 vertical","A3 horizontal"] if paper=="Auto" else [paper])
    for orientation in choices:
        if orientation not in ("A4 vertical","A4 horizontal","A3 vertical","A3 horizontal"):
            raise ValueError("Formato de papel não suportado.")
        family,direction=orientation.split()
        pw,ph=PAPERS[family]
        if direction=="horizontal":pw,ph=ph,pw
        uw,uh=pw-2*margin,ph-2*margin
        if uw<=0 or uh<=0 or overlap>=min(uw,uh):
            continue
        overlap_use=overlap if assembly=="Sobrepor" else 0.
        xs=axis_spans(width,uw,overlap_use)
        ys=axis_spans(height,uh,overlap_use)
        layouts.append(dict(pw=pw,ph=ph,uw=uw,uh=uh,xs=xs,ys=ys,
                            nx=len(xs),ny=len(ys),orientation=orientation,
                            pages=len(xs)*len(ys),overlap=overlap_use))
    if not layouts: raise ValueError("A margem é excessiva para as folhas escolhidas.")
    return min(layouts,key=lambda v:(v["pages"],
        v["pages"]*v["uw"]*v["uh"]-width*height,
        v["orientation"]!="A4 vertical"))

def export_pdf(image_path,output,w,h,margin=8,overlap=10,fit="Ajustar",
               paper="Auto",assembly="Sobrepor",marks=True,calibration=None,
               language="pt-PT",focal_x=50.0,focal_y=50.0):
    guidance={
      "pt-PT":("ESQ: CORTAR SO MARGEM BRANCA","CIMA: CORTAR SO MARGEM BRANCA","BASE: MANTER FAIXAS DIREITA/BAIXO","UNIR COM FOLHA DA ESQUERDA","UNIR COM FOLHA DE CIMA","IMPRIMIR A 100%"),
      "en":("LEFT: TRIM WHITE MARGIN ONLY","TOP: TRIM WHITE MARGIN ONLY","BASE: KEEP RIGHT/BOTTOM STRIPS","JOIN TO SHEET ON LEFT","JOIN TO SHEET ABOVE","PRINT AT 100%"),
      "es":("IZQ.: CORTAR SOLO MARGEN BLANCO","ARRIBA: CORTAR SOLO MARGEN BLANCO","BASE: MANTENER FRANJAS DERECHA/ABAJO","UNIR A HOJA IZQUIERDA","UNIR A HOJA SUPERIOR","IMPRIMIR AL 100%"),
      "fr":("GAUCHE : COUPER LA MARGE BLANCHE","HAUT : COUPER LA MARGE BLANCHE","BASE : CONSERVER DROITE/BAS","JOINDRE A LA FEUILLE GAUCHE","JOINDRE A LA FEUILLE DU HAUT","IMPRIMER A 100 %"),
      "it":("SIN.: TAGLIA SOLO MARGINE BIANCO","ALTO: TAGLIA SOLO MARGINE BIANCO","BASE: MANTIENI STRISCE DESTRA/BASSO","UNISCI AL FOGLIO A SINISTRA","UNISCI AL FOGLIO SUPERIORE","STAMPA AL 100%")
    }.get(language, None)
    if guidance is None:guidance=("ESQ: CORTAR SO MARGEM BRANCA","CIMA: CORTAR SO MARGEM BRANCA","BASE: MANTER FAIXAS DIREITA/BAIXO","UNIR COM FOLHA DA ESQUERDA","UNIR COM FOLHA DE CIMA","IMPRIMIR A 100%")
    p=plan(w,h,margin,overlap,paper,assembly)
    if p["pages"]>150: raise ValueError("Mais de 150 folhas; ajusta o formato.")
    with Image.open(image_path) as source:
        raw=ImageOps.exif_transpose(source).convert("RGBA")
        if source.mode in ("RGBA","LA","P"):
            alpha=raw.getchannel("A")
            bounds=alpha.point(lambda a: 255 if a>8 else 0).getbbox()
            if bounds: raw=raw.crop(bounds)
        # Transparência torna-se fundo branco no PDF, não preto.
        bg=Image.new("RGBA",raw.size,"white")
        im=Image.alpha_composite(bg,raw).convert("RGB")
    iw,ih=im.size
    dw,dh,ox,oy=image_placement(iw,ih,w,h,fit,focal_x,focal_y)
    pdf=canvas.Canvas(output,pagesize=(p["pw"]*MM,p["ph"]*MM),pageCompression=1)
    pdf.setTitle("NONIVERUS PosterTile v0.8.12 | impressao multipagina")
    reader=ImageReader(im)
    for r,(y,span_h) in enumerate(p["ys"]):
        for col,(x,span_w) in enumerate(p["xs"]):
            pw,ph,uw,uh=p["pw"],p["ph"],p["uw"],p["uh"]
            left=margin*MM
            bottom=margin*MM
            pdf.saveState()
            if calibration: page_transform(pdf,pw,ph,calibration["scale_x"],calibration["scale_y"])
            pdf.saveState()
            clip=pdf.beginPath()
            # Clip tanto a zona imprimivel como a dimensao real do poster.
            visible_w=span_w
            visible_h=span_h
            clip.rect(left,bottom+(uh-visible_h)*MM,visible_w*MM,visible_h*MM)
            pdf.clipPath(clip,stroke=0,fill=0)
            pdf.drawImage(reader,left+(ox-x)*MM,
                 bottom+(uh-(oy-y)-dh)*MM,dw*MM,dh*MM,
                 preserveAspectRatio=False)
            pdf.restoreState()
            if marks:
                pdf.saveState()
                pdf.setStrokeColorRGB(.15,.35,.65)
                pdf.setLineWidth(.5)
                # Pequenos tracos de referencia junto aos limites da imagem,
                # fora da area impressa, sem estragar o desenho.
                stroke=2.4*MM
                x0=left; x1=left+visible_w*MM
                ytop=bottom+uh*MM; ybot=ytop-visible_h*MM
                for xx in (x0,x1):
                    if margin>=3:
                        pdf.line(xx,ytop,xx,min(ph*MM-0.8*MM,ytop+stroke))
                        pdf.line(xx,ybot,xx,max(0.8*MM,ybot-stroke))
                for yy in (ytop,ybot):
                    if margin>=3:
                        pdf.line(x0,yy,max(0.8*MM,x0-stroke),yy)
                        pdf.line(x1,yy,min(pw*MM-0.8*MM,x1+stroke),yy)
                pdf.restoreState()
            # Guia de montagem v0.5 Studio. As marcas ficam fora da imagem.
            # A sobreposição é conteúdo duplicado: não cortar essa faixa nas
            # DUAS folhas. Cortar apenas a margem branca das folhas superiores.
            if assembly=="Sobrepor":
                pdf.saveState()
                pdf.setStrokeColorRGB(.95,.37,.07)
                pdf.setLineWidth(.8)
                pdf.setDash(2*MM,1*MM)
                x0=left; x1=left+visible_w*MM
                top=bottom+uh*MM
                y0=top-visible_h*MM
                if col>0:
                    # Limite ESQUERDO da imagem da folha superior: cortar margem
                    # branca até aqui, sem remover a zona de imagem repetida.
                    pdf.line(x0,y0,x0,top)
                if r>0:
                    # Limite SUPERIOR da imagem da folha inferior.
                    pdf.line(x0,top,x1,top)
                pdf.setDash()
                pdf.restoreState()
            pdf.setFont("Helvetica-Bold",6.5)
            pdf.setFillColorRGB(.76,.25,.07)
            # Texto curto dentro da margem superior de segurança, sem tocar
            # na fotografia nem nos cantos de registo.
            note=[]
            if assembly=="Sobrepor":
                if col>0: note.append(guidance[0])
                if r>0: note.append(guidance[1])
                if col==0 and r==0: note.append(guidance[2])
            else:
                if col>0: note.append(guidance[3])
                if r>0: note.append(guidance[4])
            if margin>=6 and note:
                pdf.drawCentredString(pw*MM/2,(ph-3.8)*MM," | ".join(note))
            pdf.setFont("Helvetica",7)
            pdf.setFillColorRGB(.24,.24,.24)
            pdf.drawString(margin*MM,3.2*MM,
                f"NONIVERUS | L{r+1} C{col+1} | {r*p['nx']+col+1}/{p['pages']}")
            pdf.drawRightString((pw-margin)*MM,3.2*MM,guidance[5])
            pdf.restoreState()
            pdf.showPage()
    pdf.save()
    return p

