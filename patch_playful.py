# -*- coding: utf-8 -*-
"""NONIVERUS Playful Studio 0.9.1 — patch non-destructive with dry run, backups and integrity checks."""
from __future__ import annotations
import argparse
import difflib
import hashlib
import os
from pathlib import Path
import sys
import time
import shutil
import py_compile
import tempfile
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE / "payload"
CHANGED = [
    "main.py", "ui/Main.qml", "build_editions.py", "version_info.txt",
    "installer/PosterTile_owner.iss", "installer/PosterTile_preview.iss",
]
ASSETS = [
    "assets/playful/astronaut_demo.png",
    "assets/playful/creative_helper.png",
    "assets/playful/playful_icon.png",
    "assets/playful/playful_icon.svg",
    "tests/test_playful_theme.py",
]
IDS = ("A21297EC-47C8-4A17-8CB9-DA95C70645A9",
       "47FD65E8-338F-45CE-9F74-2DF0B0AB9C41")

def parse_file(path):
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig").replace("\r\n","\n")
    return text, bom

def encode(text, bom):
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")

def merge_hunks(current, baseline, desired, rel):
    if current == desired:
        return current
    if current == baseline:
        return desired
    old = baseline.splitlines(keepends=True)
    new = desired.splitlines(keepends=True)
    matcher = difflib.SequenceMatcher(None,old,new,autojunk=False)
    result = current
    for group in matcher.get_grouped_opcodes(n=4):
        lo,hi=group[0][1],group[-1][2]
        ln,hn=group[0][3],group[-1][4]
        old_fragment="".join(old[lo:hi])
        new_fragment="".join(new[ln:hn])
        # A unique group of contextual lines must match exactly before changing anything.
        count=result.count(old_fragment)
        if count == 1:
            result=result.replace(old_fragment,new_fragment,1)
        elif result.count(new_fragment) == 1:
            continue # already patched, idempotent
        else:
            raise RuntimeError(
                f"{rel}: alterações locais incompatíveis com este hotfix. "
                "Nenhum ficheiro foi modificado. Envia o erro antes de continuar."
            )
    return result


def merge_main_adaptive(current, baseline, desired):
    """Atualiza o tema com âncoras estruturais pequenas e únicas.
    Nunca substitui o main.py completo; mantém código e cores existentes.
    """
    result=current
    # O cabeçalho é informativo: não comprometer a alteração do tema por uma
    # pequena diferença na descrição do módulo.
    lines=result.splitlines(keepends=True)
    for i in range(min(5,len(lines))):
        if "NONIVERUS PosterTile Luxury Studio" in lines[i]:
            lines[i]=lines[i].replace("v0.9.0.2","v0.9.1")
            break
    result="".join(lines)

    # 1. Admissão do tema guardado em QSettings
    p_read = re.compile(
        r'(?m)^(?P<pre>[ \t]*self\._theme\s*=\s*theme\s+if\s+theme\s+in\s*\()'
        r'(?P<opts>[^)\r\n]+)(?P<end>\)\s+else\s+["\']Midnight Sapphire["\'][ \t]*)$'
    )
    m=p_read.search(result)
    if not m or len(p_read.findall(result))!=1:
        raise RuntimeError("main.py: linha self._theme nao identificada. "
                           "Executa o diagnostico indicado no LEIA-ME e envia o resultado.")
    opts=m.group('opts')
    if '"Playful Studio"' not in opts and "'Playful Studio'" not in opts:
        if "Midnight Sapphire" not in opts or "Pearl Titanium" not in opts:
            raise RuntimeError("main.py: temas atuais inesperados; nao aplicar.")
        new_opts=opts.rstrip()+',"Playful Studio"'
        result=result[:m.start('opts')]+new_opts+result[m.end('opts'):]

    # 2. Validação no seletor de temas (apenas setTheme)
    p_set = re.compile(
        r'(?m)^(?P<pre>[ \t]*if\s+theme\s+not\s+in\s*\()'
        r'(?P<opts>[^)\r\n]+)(?P<end>\)\s*:\s*return[ \t]*)$'
    )
    mlist=list(p_set.finditer(result))
    if len(mlist)!=1:
        raise RuntimeError("main.py: linha 'if theme not in' ausente ou repetida; "
                           "nao aplicar. Envia o diagnostico.")
    m=mlist[0]
    opts=m.group('opts')
    if '"Playful Studio"' not in opts and "'Playful Studio'" not in opts:
        if "Midnight Sapphire" not in opts or "Pearl Titanium" not in opts:
            raise RuntimeError("main.py: opcoes de setTheme inesperadas.")
        new_opts=opts.rstrip()+',"Playful Studio"'
        result=result[:m.start('opts')]+new_opts+result[m.end('opts'):]

    # 3. Editor de composição: manter TODAS as cores existentes dos temas
    # antigos, e inserir o novo tema sem modificar a sua lógica.
    if 'if self._theme == "Playful Studio":' not in result:
        lines=result.splitlines(keepends=True)
        candidates=[]
        for i, line in enumerate(lines):
            if re.match(r"^[ \t]*light\s*=\s*self\._theme\s*==\s*['\"]Pearl Titanium['\"][ \t]*\r?\n?$",line):
                candidates.append(i)
        if len(candidates)!=1:
            raise RuntimeError("main.py: bloco da paleta do editor nao encontrado "
                               "univocamente; envia o diagnostico.")
        start=candidates[0]
        names=("bg","panel","ink","muted","bronze")
        for j,name in enumerate(names,1):
            if start+j>=len(lines) or not re.match(rf"^[ \t]*{name}\s*=",lines[start+j]):
                raise RuntimeError("main.py: paleta do editor alterada; "
                                   "nao posso preservar as cores com seguranca.")
        indent=re.match(r"^[ \t]*",lines[start]).group(0)
        old_color_lines=lines[start+1:start+6]
        ending='\r\n' if lines[start].endswith('\r\n') else '\n'
        insert=[
            indent+'light=self._theme in ("Pearl Titanium","Playful Studio")'+ending,
            indent+'if self._theme == "Playful Studio":'+ending,
            indent+'    bg, panel, ink, muted, bronze = "#F1F8FF", "#FFFFFF", "#09265C", "#5875A3", "#FF7651"'+ending,
            indent+'else:'+ending,
        ]
        for line in old_color_lines:
            insert.append('    '+line)  # deslocar a paleta existente para o else
        lines[start:start+6]=insert
        result="".join(lines)
    if result.count('if self._theme == "Playful Studio":')!=1:
        raise RuntimeError("main.py: o tema Playful no editor ficou ambiguo.")

    compile(result,"main.py","exec")
    return result


def merge_installer_version(current, rel, guid, edition):
    """Alterar só a versão; nunca tocar em AppId, licenças ou script [Code]."""
    if guid not in current:
        raise RuntimeError(f"{rel}: AppId desconhecido. Nao aplicar.")
    if "UsePreviousAppDir=yes" not in current or "UsePreviousTasks=yes" not in current:
        raise RuntimeError(f"{rel}: as regras de atualização esperadas estão ausentes.")
    expected = "Owner" if edition=="owner" else "PrivatePreview"
    expected_labels=[
        ('#define MyAppVersion "0.9.0.2"', '#define MyAppVersion "0.9.1"'),
        ('VersionInfoVersion=0.9.0.2', 'VersionInfoVersion=0.9.1'),
        (f'OutputBaseFilename=NONIVERUS_PosterTile_{expected}_Setup_v0.9.0.2',
         f'OutputBaseFilename=NONIVERUS_PosterTile_{expected}_Setup_v0.9.1')
    ]
    result=current
    for old,new in expected_labels:
        if result.count(old)==1:
            result=result.replace(old,new,1)
        elif result.count(new)==1 and result.count(old)==0:
            pass
        else:
            raise RuntimeError(f"{rel}: campo de versão ausente ou ambiguo: {old!r}")
    if current.count(guid)!=result.count(guid):
        raise RuntimeError(f"{rel}: AppId alterado inesperadamente.")
    return result

def validate_qml(qml):
    # Basic lexical delimiter check; the real Qt parser must still be validated on Windows.
    stack=[]
    quote=None
    escaped=False
    for char in qml:
        if quote:
            if escaped: escaped=False
            elif char == "\\": escaped=True
            elif char == quote: quote=None
        elif char in ("'", '"'): quote=char
        elif char in "{[(": stack.append(char)
        elif char in "}])":
            if not stack or {"}":"{","]":"[",")":"("}[char] != stack.pop():
                raise RuntimeError("QML: delimitadores desequilibrados.")
    if quote or stack:
        raise RuntimeError("QML: string ou delimitador incompleto.")
    for token in ['property bool playful:', 'studio.setTheme(currentText)',
                  'assets/playful/astronaut_demo.png','assets/playful/creative_helper.png',
                  'studio.framedPreviewUrl']:
        if token not in qml: raise RuntimeError(f"QML: não encontrei {token}")

def run(project, dry):
    if project.name != "NONIVERUS_POSTERTILE_DEV":
        raise RuntimeError("Este patch só pode ser aplicado à pasta NONIVERUS_POSTERTILE_DEV.")
    if not project.is_dir():raise RuntimeError(f"Pasta inexistente: {project}")
    if not (project / "license_runtime.py").is_file() or not (project / "native_license" / "src" / "lib.rs").is_file():
        raise RuntimeError("Não encontrei a versão Owner/Private Preview v0.9.x. Nada foi alterado.")
    planned={}
    for rel in CHANGED:
        p=project/rel
        if not p.is_file():raise RuntimeError("Falta o ficheiro: " + str(p))
        old,bom=parse_file(p)
        base,_=parse_file(ROOT/"baseline"/rel)
        new,_=parse_file(ROOT/"updated"/rel)
        if "0.9.1" in old and old == new:
            print("Já atualizado:",rel)
            continue
        if rel=="main.py":
            result=merge_main_adaptive(old,base,new)
        elif rel.startswith("installer/"):
            edition="owner" if rel.endswith("PosterTile_owner.iss") else "preview"
            guid=IDS[0] if edition=="owner" else IDS[1]
            result=merge_installer_version(old,rel,guid,edition)
        else:
            result=merge_hunks(old,base,new,rel)
        if result != old:
            planned[rel]=encode(result,bom)
            print("Preparado:",rel)
        else:
            print("Sem alterações:",rel)
    # keep identifiers independent so updates preserve edition and valid licenses
    builder=(planned.get("build_editions.py") or (project/"build_editions.py").read_bytes()).decode("utf-8-sig")
    if not all(k in builder for k in IDS):
        raise RuntimeError("AppId inesperado. O instalador não será modificado.")
    qml=(planned.get("ui/Main.qml") or (project/"ui/Main.qml").read_bytes()).decode("utf-8-sig")
    validate_qml(qml)
    main=(planned.get("main.py") or (project/"main.py").read_bytes()).decode("utf-8-sig")
    compile(main,"main.py","exec")
    compile(builder,"build_editions.py","exec")
    for rel in ASSETS:
        src=(ROOT/"assets"/"test_playful_theme.py") if rel=="tests/test_playful_theme.py" else ROOT/rel
        dest=project/rel
        if not src.is_file():raise RuntimeError("Recurso em falta: "+str(src))
        if not dest.exists() or dest.read_bytes()!=src.read_bytes():
            planned[rel]=src.read_bytes()
            print("Recurso preparado:",rel)
    print("Ficheiros para atualizar:",len(planned))
    if dry:
        print("SIMULAÇÃO OK: nenhum ficheiro alterado.")
        return
    if not planned:
        print("SUCESSO: Playful Studio v0.9.1 já está aplicado.")
        return
    stamp=time.strftime("%Y%m%d_%H%M%S")
    backup=Path(os.environ.get("LOCALAPPDATA",str(Path.home()))) / "NONIVERUS" / "PosterTile" / "build_backups" / ("Playful_v091_"+stamp)
    backup.mkdir(parents=True,exist_ok=False)
    for rel in planned:
        src=project/rel
        if src.exists():
            dest=backup/rel
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(src,dest)
    print("Cópias de segurança:",backup)
    for rel,data in planned.items():
        dest=project/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        # atomic individual writes, and all files were checked before writing
        with tempfile.NamedTemporaryFile(dir=dest.parent,delete=False) as f:
            temp=Path(f.name)
            f.write(data)
        try:os.replace(temp,dest)
        finally:
            if temp.exists():temp.unlink()
        print("Atualizado:",rel)
    print("SUCESSO: Playful Studio v0.9.1 aplicado. As chaves privadas não foram tocadas.")
    print("Para compilar: CONSTRUIR_OWNER_WINDOWS.cmd / CONSTRUIR_PREVIEW_WINDOWS.cmd")

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--project", default=r"C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV")
    ap.add_argument("--apply",action="store_true")
    a=ap.parse_args()
    try:run(Path(a.project),dry=not a.apply)
    except Exception as e:
        print("PARADO EM SEGURANÇA:",e,file=sys.stderr)
        sys.exit(1)
