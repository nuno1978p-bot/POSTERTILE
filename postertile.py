# -*- coding: utf-8 -*-
"""NONIVERUS PosterTile v0.3 — impressao de posters em folhas A4."""
import math
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

MM=72/25.4
A4=(210.,297.)
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
    for orientation in (["A4 vertical","A4 horizontal"] if paper=="Auto" else [paper]):
        pw,ph=A4 if orientation=="A4 vertical" else A4[::-1]
        uw,uh=pw-2*margin,ph-2*margin
        if uw<=0 or uh<=0 or overlap>=min(uw,uh):
            continue
        overlap_use=overlap if assembly=="Sobrepor" else 0.
        xs=axis_spans(width,uw,overlap_use)
        ys=axis_spans(height,uh,overlap_use)
        layouts.append(dict(pw=pw,ph=ph,uw=uw,uh=uh,xs=xs,ys=ys,
                            nx=len(xs),ny=len(ys),orientation=orientation,
                            pages=len(xs)*len(ys),overlap=overlap_use))
    if not layouts: raise ValueError("A margem é excessiva para as folhas A4.")
    return min(layouts,key=lambda v:(v["pages"],
        v["pages"]*v["uw"]*v["uh"]-width*height,
        v["orientation"]!="A4 vertical"))

def export_pdf(image_path,output,w,h,margin=8,overlap=10,fit="Ajustar",
               paper="Auto",assembly="Sobrepor",marks=True):
    p=plan(w,h,margin,overlap,paper,assembly)
    if p["pages"]>150: raise ValueError("Mais de 150 folhas; ajusta o formato.")
    with Image.open(image_path) as source:
        im=ImageOps.exif_transpose(source).convert("RGB")
    iw,ih=im.size
    factor=min(w/iw,h/ih) if fit=="Ajustar" else max(w/iw,h/ih)
    dw,dh=iw*factor,ih*factor
    ox,oy=(w-dw)/2,(h-dh)/2
    pdf=canvas.Canvas(output,pagesize=(p["pw"]*MM,p["ph"]*MM),pageCompression=1)
    pdf.setTitle("NONIVERUS PosterTile v0.3 | impressao A4")
    reader=ImageReader(im)
    for r,(y,span_h) in enumerate(p["ys"]):
        for col,(x,span_w) in enumerate(p["xs"]):
            pw,ph,uw,uh=p["pw"],p["ph"],p["uw"],p["uh"]
            left=margin*MM
            bottom=margin*MM
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
            # Guia de montagem v0.3. As marcas ficam fora da imagem.
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
                if col>0: note.append("ESQ: CORTAR SO MARGEM BRANCA")
                if r>0: note.append("CIMA: CORTAR SO MARGEM BRANCA")
                if col==0 and r==0: note.append("BASE: MANTER FAIXAS DIREITA/BAIXO")
            else:
                if col>0: note.append("UNIR COM FOLHA DA ESQUERDA")
                if r>0: note.append("UNIR COM FOLHA DE CIMA")
            if margin>=6 and note:
                pdf.drawCentredString(pw*MM/2,(ph-3.8)*MM," | ".join(note))
            pdf.setFont("Helvetica",7)
            pdf.setFillColorRGB(.24,.24,.24)
            pdf.drawString(margin*MM,3.2*MM,
                f"NONIVERUS | L{r+1} C{col+1} | {r*p['nx']+col+1}/{p['pages']}")
            pdf.drawRightString((pw-margin)*MM,3.2*MM,"IMPRIMIR A 100%")
            pdf.showPage()
    pdf.save()
    return p

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NONIVERUS | PosterTile v0.3")
        self.geometry("1080x760")
        self.minsize(850,650)
        self.configure(bg="#121820")
        self.image_path=None;self.thumb=None;self.tkimage=None
        self.size=tk.StringVar(value="A2")
        self.orientation=tk.StringVar(value="Horizontal")
        self.paper=tk.StringVar(value="Auto")
        self.fit=tk.StringVar(value="Ajustar")
        self.assembly=tk.StringVar(value="Sobrepor")
        self.margin=tk.StringVar(value="8")
        self.overlap=tk.StringVar(value="10")
        self.correction=tk.StringVar(value="100")
        self.custom_w=tk.StringVar(value="594")
        self.custom_h=tk.StringVar(value="420")
        self.marks=tk.BooleanVar(value=True)
        self.status=tk.StringVar(value="Escolhe uma imagem para começar.")
        self._build()
        for v in (self.size,self.orientation,self.paper,self.fit,self.assembly,
                  self.margin,self.overlap,self.correction,self.custom_w,self.custom_h):
            v.trace_add("write",lambda *a:self.refresh())
        self.refresh()

    def _build(self):
        style=ttk.Style(self);style.theme_use("clam")
        style.configure("TCombobox",padding=4)
        container=tk.Frame(self,bg="#121820")
        container.pack(fill="both",expand=True,padx=18,pady=12)
        tk.Label(container,text="NONIVERUS  /  POSTERTILE v0.3",
                 font=("Segoe UI",20,"bold"),bg="#121820",fg="#f1f5f9").pack(anchor="w")
        tk.Label(container,text="A2 · A1 · A4 | cortes equilibrados | dimensões reais em milímetros",
                 bg="#121820",fg="#bac8d6").pack(anchor="w",pady=(0,9))
        body=tk.Frame(container,bg="#121820")
        body.pack(fill="both",expand=True)
        left=tk.Frame(body,bg="#1e2936",width=320,padx=14,pady=9)
        left.pack(side="left",fill="y",padx=(0,12));left.pack_propagate(False)
        tk.Button(left,text="ABRIR IMAGEM",command=self.open_image,
            bg="#37b7a2",fg="#0b1d24",relief="flat",font=("Segoe UI",10,"bold"),
            pady=8).pack(fill="x",pady=(0,6))
        self._combo(left,"Tamanho final",self.size,["A2","A1","Personalizado"])
        self._combo(left,"Orientação do poster",self.orientation,["Horizontal","Vertical"])
        self._combo(left,"Folhas A4",self.paper,["Auto","A4 vertical","A4 horizontal"])
        self._combo(left,"Montagem",self.assembly,["Sobrepor","Cortar e unir"])
        self._combo(left,"Enquadramento",self.fit,["Ajustar","Preencher"])
        self._entry(left,"Largura personalizada (mm)",self.custom_w)
        self._entry(left,"Altura personalizada (mm)",self.custom_h)
        self._entry(left,"Margem de segurança (mm)",self.margin)
        self._entry(left,"Sobreposição mínima (mm)",self.overlap)
        self._entry(left,"Correção de escala (%)",self.correction)
        tk.Checkbutton(left,text="Marcas exteriores de referência",variable=self.marks,
              bg="#1e2936",fg="#ebf3fa",selectcolor="#334155",
              activebackground="#1e2936").pack(anchor="w",pady=(7,7))
        tk.Button(left,text="GERAR PDF A4",command=self.generate,
            bg="#37b7a2",fg="#0b1d24",relief="flat",font=("Segoe UI",11,"bold"),
            pady=9).pack(fill="x")
        self.info=tk.Label(left,text="",justify="left",anchor="nw",wraplength=285,
                            bg="#1e2936",fg="#b9dbdf",font=("Segoe UI",9))
        self.info.pack(fill="x",pady=9)
        wrapper=tk.Frame(body,bg="#1e2936")
        wrapper.pack(side="left",fill="both",expand=True)
        self.canvas=tk.Canvas(wrapper,bg="#253442",highlightthickness=0)
        self.canvas.pack(fill="both",expand=True,padx=11,pady=11)
        self.canvas.bind("<Configure>",lambda e:self.draw_preview())
        tk.Label(container,textvariable=self.status,bg="#121820",fg="#b9d3de",
                 anchor="w").pack(fill="x",pady=(6,0))

    def _combo(self,parent,label,var,vals):
        tk.Label(parent,text=label,bg="#1e2936",fg="#c5d5e3",
                 font=("Segoe UI",9)).pack(anchor="w",pady=(4,1))
        ttk.Combobox(parent,textvariable=var,values=vals,state="readonly").pack(fill="x")

    def _entry(self,parent,label,var):
        tk.Label(parent,text=label,bg="#1e2936",fg="#c5d5e3",
                 font=("Segoe UI",9)).pack(anchor="w",pady=(4,1))
        tk.Entry(parent,textvariable=var,bg="#e9f0f4",relief="flat").pack(fill="x",ipady=2)

    def values(self):
        if self.size.get()=="Personalizado":
            w=float(self.custom_w.get().replace(",","."));h=float(self.custom_h.get().replace(",","."))
        else:
            a,b=SIZES[self.size.get()]
            w,h=(b,a) if self.orientation.get()=="Horizontal" else (a,b)
        correction=float(self.correction.get().replace(",","."))
        if not 50<=correction<=150:raise ValueError("Correção de escala entre 50 e 150%.")
        w*=correction/100;h*=correction/100
        if not (10<=w<=3000 and 10<=h<=3000):
            raise ValueError("Dimensões entre 10 e 3000 mm.")
        margin=float(self.margin.get().replace(",","."))
        overlap=float(self.overlap.get().replace(",","."))
        p=plan(w,h,margin,overlap,self.paper.get(),self.assembly.get())
        if p["pages"]>150:raise ValueError("Mais de 150 folhas.")
        return w,h,margin,overlap,p

    def open_image(self):
        path=filedialog.askopenfilename(title="Abrir imagem",
            filetypes=[("Imagens","*.png *.jpg *.jpeg *.webp *.bmp *.tif *.tiff")])
        if not path:return
        try:
            with Image.open(path) as src:
                im=ImageOps.exif_transpose(src)
                self.thumb=im.convert("RGB");self.thumb.thumbnail((1400,1400))
            self.image_path=path
            self.status.set("Imagem: "+os.path.basename(path))
            self.refresh()
        except Exception as exc:messagebox.showerror("Imagem inválida",str(exc))

    def refresh(self):
        try:
            w,h,m,o,p=self.values()
            self.info.config(text=(f"Poster: {w:.1f} × {h:.1f} mm\n"
                f"{p['nx']} colunas × {p['ny']} linhas = {p['pages']} folhas\n"
                f"Orientação A4: {p['orientation']}\n"
                f"Área útil A4: {p['uw']:.0f} × {p['uh']:.0f} mm\n"
                f"Montagem: {self.assembly.get()}\n"
                "Laranja: sobreposição. Azul: ordem das folhas."))
        except Exception as exc:
            self.info.config(text="Verifica os parâmetros: "+str(exc))
        self.draw_preview()

    def draw_preview(self):
        c=self.canvas;c.delete("all")
        cw,ch=c.winfo_width(),c.winfo_height()
        if cw<50 or ch<50:return
        try:w,h,m,o,p=self.values()
        except Exception:
            c.create_text(cw/2,ch/2,text="Verifica os parâmetros",fill="white")
            return
        scale=min((cw-65)/w,(ch-85)/h)
        if scale<=0:return
        X=(cw-w*scale)/2;Y=(ch-h*scale)/2
        c.create_rectangle(X,Y,X+w*scale,Y+h*scale,fill="white",outline="#dbeafe")
        if self.thumb is not None:
            iw,ih=self.thumb.size
            fact=min(w/iw,h/ih) if self.fit.get()=="Ajustar" else max(w/iw,h/ih)
            dw,dh=iw*fact,ih*fact
            view=Image.new("RGB",(max(1,round(w*scale)),max(1,round(h*scale))),"white")
            tile=self.thumb.resize((max(1,round(dw*scale)),max(1,round(dh*scale))),Image.Resampling.LANCZOS)
            view.paste(tile,(round((w-dw)/2*scale),round((h-dh)/2*scale)))
            self.tkimage=ImageTk.PhotoImage(view)
            c.create_image(X,Y,anchor="nw",image=self.tkimage)
        # Representa cada folha e destaca as faixas duplas.
        for i,(x,sw) in enumerate(p["xs"]):
            if i:
                xx=X+x*scale
                c.create_line(xx,Y,xx,Y+h*scale,fill="#ff8d40",width=2)
        for i,(y,sh) in enumerate(p["ys"]):
            if i:
                yy=Y+y*scale
                c.create_line(X,yy,X+w*scale,yy,fill="#ff8d40",width=2)
        for row,(y,sh) in enumerate(p["ys"]):
            for col,(x,sw) in enumerate(p["xs"]):
                cx=X+(x+sw/2)*scale
                cy=Y+(y+sh/2)*scale
                c.create_text(cx,cy,text=f"{row*p['nx']+col+1}",
                              fill="#f97316",font=("Segoe UI",11,"bold"))
        c.create_text(cw/2,19,text=f"PRÉ-VISUALIZAÇÃO · {p['pages']} FOLHAS A4",
                      fill="#edf2f7",font=("Segoe UI",11,"bold"))
        c.create_text(cw/2,ch-14,text="Laranja = sobreposição | cortar só as margens brancas indicadas",
                      fill="#c4d5e3")

    def generate(self):
        if not self.image_path:
            messagebox.showwarning("Sem imagem","Abre primeiro uma imagem.");return
        try:w,h,m,o,p=self.values()
        except Exception as exc:messagebox.showerror("Parâmetros",str(exc));return
        dst=filedialog.asksaveasfilename(defaultextension=".pdf",
            filetypes=[("Ficheiro PDF","*.pdf")],initialfile="NONIVERUS_Poster_A4_v0_3.pdf")
        if not dst:return
        try:
            self.status.set("A gerar PDF...");self.update_idletasks()
            export_pdf(self.image_path,dst,w,h,m,o,self.fit.get(),
                       self.paper.get(),self.assembly.get(),self.marks.get())
            self.status.set("PDF criado: "+dst)
            messagebox.showinfo("PDF criado",
                f"{p['pages']} folhas A4 ({p['nx']} × {p['ny']}).\n"
                "Imprime em A4, a 100% / Tamanho real.\n"
                "Desativa 'Ajustar à página'.\n"
                "Verifica uma medição com régua antes de imprimir tudo.\n\n"
                "A precisão final depende das margens e da escala da impressora.")
        except Exception as exc:
            self.status.set("Falha na criação do PDF.")
            messagebox.showerror("Erro",str(exc))

if __name__=="__main__":
    App().mainloop()
