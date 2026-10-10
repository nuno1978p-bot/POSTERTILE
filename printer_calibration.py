# -*- coding: utf-8 -*-
"""NONIVERUS - perfis locais por impressora, papel e orientação."""
import json, math, os, re
from pathlib import Path
from datetime import datetime, timezone
from reportlab.pdfgen import canvas

MM=72/25.4
REF_X=150.0
REF_Y=200.0
DIMS={"A4 vertical":(210,297),"A4 horizontal":(297,210),
      "A3 vertical":(297,420),"A3 horizontal":(420,297)}
def storage_path():
    root=Path(os.getenv("LOCALAPPDATA") or Path.home()/".noniverus")
    return root/"NONIVERUS"/"PosterTile"/"printer_profiles.json"
def _key(printer,paper):
    return printer.casefold().strip()+"|"+paper
def load():
    p=storage_path()
    if not p.is_file(): return {}
    data=json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data,dict) or data.get("version") != 1: raise ValueError("Ficheiro de perfis inválido")
    return data.get("profiles",{})
def reference_y(paper):
    return min(REF_Y, DIMS[paper][1]-35)

def save(printer,paper,measured_x,measured_y):
    if not printer.strip() or paper not in DIMS: raise ValueError("Impressora e papel obrigatórios")
    x,y=float(measured_x),float(measured_y)
    if not all(math.isfinite(v) for v in (x,y)) or x<=0 or y<=0: raise ValueError("Medições inválidas")
    sx,sy=REF_X/x,reference_y(paper)/y
    if not .97<=sx<=1.03 or not .97<=sy<=1.03:
        raise ValueError("Desvio superior a 3%. Verifica impressão a 100%, papel e régua antes de guardar.")
    data=load()
    data[_key(printer,paper)]={"printer":printer.strip(),"paper":paper,"measured_x":x,"measured_y":y,
      "scale_x":sx,"scale_y":sy,"updated_utc":datetime.now(timezone.utc).isoformat()}
    p=storage_path(); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(".tmp")
    tmp.write_text(json.dumps({"version":1,"profiles":data},indent=2,ensure_ascii=False),encoding="utf-8")
    os.replace(tmp,p)
    return data[_key(printer,paper)]
def get(printer,paper):
    return load().get(_key(printer,paper))
def make_test_pdf(output,paper,printer):
    if paper not in DIMS: raise ValueError("Papel inválido")
    pw,ph=DIMS[paper]
    # Referências cabem em A4 horizontal: X 150 e Y 160; vertical X 150 e Y 200.
    ry=reference_y(paper)
    c=canvas.Canvas(str(output),pagesize=(pw*MM,ph*MM))
    c.setTitle("NONIVERUS | Calibração | "+printer)
    c.setFont("Helvetica-Bold",12)
    c.drawString(15*MM,(ph-14)*MM,"NONIVERUS | CALIBRACAO DE IMPRESSORA")
    c.setFont("Helvetica",9)
    c.drawString(15*MM,(ph-20)*MM,"Imprimir a 100% / Tamanho real. Sem ajustar a pagina.")
    c.drawString(15*MM,(ph-26)*MM,f"Papel: {paper} - Perfil: {printer[:45]}")
    x0,y0=20*MM,15*MM
    c.setStrokeColorRGB(.1,.25,.45);c.setLineWidth(.7)
    c.line(x0,y0,x0+REF_X*MM,y0)
    c.line(x0,y0,x0,y0+ry*MM)
    for val in range(0,151,10):
        xx=x0+val*MM;c.line(xx,y0-2*MM,xx,y0+2*MM)
    for val in range(0,int(ry)+1,10):
        yy=y0+val*MM;c.line(x0-2*MM,yy,x0+2*MM,yy)
    c.setFont("Helvetica",8)
    c.drawString(x0+45*MM,y0+5*MM,"X: 150.0 mm")
    c.drawString(x0+5*MM,y0+ry*MM-4*MM,f"Y: {ry:.1f} mm")
    c.showPage();c.save()
    return ry
def page_transform(c,pw_mm,ph_mm,sx,sy):
    """Aplica compensação em cada página; centro fixo, escala indep. X/Y."""
    if (sx,sy)==(1.,1.): return
    # Transformação de todo o conteúdo, preservando a caixa de página.
    cx,cy=pw_mm*MM/2,ph_mm*MM/2
    c.translate(cx,cy);c.scale(sx,sy);c.translate(-cx,-cy)
