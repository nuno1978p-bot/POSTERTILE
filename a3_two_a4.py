# -*- coding: utf-8 -*-
"""A3 em exactamente duas folhas A4: modo seguro e modo sem margens.

A3 = 297 x 420 mm. A3 horizontal usa duas A4 verticais lado a lado.
A3 vertical usa duas A4 horizontais uma por cima da outra.

O modo seguro não promete imagem A3 à escala 1:1: une áreas imprimíveis
das duas folhas depois de cortar as duas margens internas.
"""
import math
from PIL import Image, ImageOps
from printer_calibration import page_transform
from poster_framing import image_placement
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

MM = 72.0 / 25.4

def plan_a3_two(orientation="horizontal", mode="safe", margin=8.0):
    if orientation not in ("horizontal", "vertical"):
        raise ValueError("Orientação A3 inválida.")
    if mode not in ("safe", "borderless"):
        raise ValueError("Modo de impressão A3 inválido.")
    if not math.isfinite(margin) or margin < 0 or margin > 20:
        raise ValueError("Margem deve estar entre 0 e 20 mm.")
    if mode == "safe" and margin < 3:
        raise ValueError("Modo com margens exige pelo menos 3 mm de margem.")
    if orientation == "horizontal":
        pw, ph, nx, ny = 210.0, 297.0, 2, 1
        poster_w, poster_h = 420.0, 297.0
        pap = "A4 vertical"
    else:
        pw, ph, nx, ny = 297.0, 210.0, 1, 2
        poster_w, poster_h = 297.0, 420.0
        pap = "A4 horizontal"
    m = margin if mode == "safe" else 0.0
    cw, ch = pw - 2*m, ph - 2*m
    if cw <= 0 or ch <= 0:
        raise ValueError("Margem demasiado grande.")
    return dict(pw=pw, ph=ph, nx=nx, ny=ny, pages=2,
                orientation=pap, m=m, cw=cw, ch=ch,
                work_w=cw*nx, work_h=ch*ny,
                poster_w=poster_w, poster_h=poster_h,
                assembled_width=poster_w - (2*m if nx==2 else 0),
                assembled_height=poster_h - (2*m if ny==2 else 0),
                mode=mode)

def export_a3_two_a4(image_path, output, orientation="horizontal",
                      mode="safe", margin=8.0, calibration=None,
                      fit="Ajustar", focal_x=50.0, focal_y=50.0):
    p = plan_a3_two(orientation, mode, margin)
    # Respeitar EXIF e transparência tal como o motor principal.
    with Image.open(image_path) as source:
        raw=ImageOps.exif_transpose(source).convert("RGBA")
        if source.mode in ("RGBA","LA","P"):
            alpha=raw.getchannel("A")
            bounds=alpha.point(lambda v: 255 if v>8 else 0).getbbox()
            if bounds:
                raw=raw.crop(bounds)
        img=Image.new("RGBA",raw.size,"white")
        img=Image.alpha_composite(img,raw).convert("RGB")
    iw, ih=img.size
    dw,dh,ox,oy=image_placement(
        iw,ih,p["work_w"],p["work_h"],fit,focal_x,focal_y
    )
    p["image_width"]=dw
    p["image_height"]=dh
    reader=ImageReader(img)
    pdf=canvas.Canvas(str(output),pagesize=(p["pw"]*MM,p["ph"]*MM),pageCompression=1)
    pdf.setTitle("NONIVERUS PosterTile 0.8.12 - A3 em 2 folhas A4")
    pdf.setAuthor("NONIVERUS")
    for row in range(p["ny"]):
        for col in range(p["nx"]):
            pw,ph=p["pw"],p["ph"]
            m,cw,ch=p["m"],p["cw"],p["ch"]
            pdf.saveState()
            if calibration: page_transform(pdf,pw,ph,calibration["scale_x"],calibration["scale_y"])
            pdf.saveState()
            clip=pdf.beginPath()
            clip.rect(m*MM,m*MM,cw*MM,ch*MM)
            pdf.clipPath(clip,stroke=0,fill=0)
            # A imagem é uma composição lógica única; as duas páginas
            # apresentam metades contíguas sem duplicação nem distorção.
            x = (m + ox - col*cw)*MM
            y = (m + ch - (oy - row*ch) - dh)*MM
            pdf.drawImage(reader,x,y,dw*MM,dh*MM,preserveAspectRatio=False,mask='auto')
            pdf.restoreState()
            # Nada é desenhado nas margens da imagem. A montagem segura
            # pede cortar as margens brancas interiores, pelo limite visível.
            pdf.restoreState()
            pdf.showPage()
    pdf.save()
    return p
