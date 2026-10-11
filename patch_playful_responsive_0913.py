#!/usr/bin/env python3
"""NONIVERUS v0.9.1.3 — compact Playful panel + Qt Quick Controls Basic.
Only main.py and ui/Main.qml. Safe preflight, idempotence and external backup.
"""
import argparse
import datetime as dt
import os
import shutil
import sys
import tempfile
from pathlib import Path

def substitute_once(text, old, new, label):
    if text.count(new) == 1:
        return text, f"{label}: já atualizado"
    if text.count(old) != 1:
        raise ValueError(f"{label}: ponto de alteração ausente ou ambíguo "
                         f"(encontrado {text.count(old)} vezes). Nada foi modificado.")
    return text.replace(old, new, 1), f"{label}: pronto a atualizar"


def patch_main(main):
    if "QQuickStyle.setStyle(\"Basic\")" in main:
        if main.count("QQuickStyle.setStyle(\"Basic\")") != 1:
            raise ValueError("Estilo Qt Basic aparece mais do que uma vez.")
        return main, ["Estilo Qt Basic: já atualizado"]
    main, status = substitute_once(
        main,
        "def main():\n    app=QApplication(sys.argv)",
        "def main():\n"
        "    # v0.9.1.3: Qt Quick Controls Basic suporta indicator/contentItem\n"
        "    # dos controlos QML personalizados (evita avisos do estilo nativo).\n"
        "    # Deve ser configurado ANTES de criar o motor QQmlApplicationEngine.\n"
        "    from PySide6.QtQuickControls2 import QQuickStyle\n"
        "    QQuickStyle.setStyle(\"Basic\")\n"
        "    app=QApplication(sys.argv)",
        "Estilo Qt Quick Controls")
    return main, [status]


def patch_qml(source):
    if "id: playfulHelpScroll" not in source or "Component.onCompleted: win.showMaximized()" not in source:
        raise ValueError("É necessário aplicar primeiro a v0.9.1.2 responsiva.")
    if "component PlayfulBenefit: RowLayout {" not in source:
        raise ValueError("Não foi identificado o componente PlayfulBenefit.")
    messages = []
    a = source.index("    component PlayfulBenefit: RowLayout {")
    b = source.index("    Gradient {\n", a)
    benefit = source[a:b]
    # Constrain text's layout minimum so long messages wrap inside the compact panel.
    rules_benefit = [
        ('        Layout.fillWidth: true\n        spacing: 9\n',
         '        Layout.fillWidth: true\n        Layout.minimumWidth: 0\n        spacing: 9\n',
         'Layout do benefício'),
        ('            Layout.fillWidth: true\n            text: pb.benefit\n',
         '            Layout.fillWidth: true\n            Layout.minimumWidth: 0\n            text: pb.benefit\n',
         'Quebra de texto do benefício'),
        ('            font.pixelSize: 12\n            lineHeight: 1.12\n',
         '            font.pixelSize: win.width < 1270 ? 11 : 12\n            lineHeight: 1.12\n',
         'Letra dos benefícios'),
    ]
    for old,new,label in rules_benefit:
        benefit,state = substitute_once(benefit,old,new,label);messages.append(state)
    source = source[:a]+benefit+source[b:]

    a = source.index("            // v0.9.1.2: o painel direito adapta-se")
    b = source.index("        RowLayout {\n            Layout.fillWidth: true; Layout.preferredHeight: 18",a)
    panel = source[a:b]
    rules_panel = [
        ('Layout.preferredWidth: visible ? (win.width < 1270 ? 178 : (win.width < 1450 ? 204 : 236)) : 0',
         'Layout.preferredWidth: visible ? (win.width < 1270 ? 205 : (win.width < 1450 ? 216 : 236)) : 0',
         'Largura do painel compacto'),
        ('Layout.minimumWidth: visible ? 165 : 0',
         'Layout.minimumWidth: visible ? 192 : 0',
         'Largura mínima'),
        ('anchors.margins: win.width < 1270 ? 8 : 12',
         'anchors.margins: win.width < 1270 ? 10 : 12',
         'Margens'),
        ('                    ScrollBar.vertical: ScrollBar {\n'
         '                        policy: ScrollBar.AsNeeded\n'
         '                    }',
         '                    ScrollBar.vertical: ScrollBar {\n'
         '                        policy: ScrollBar.AsNeeded\n'
         '                        width: 6\n'
         '                    }',
         'ScrollBar discreta'),
        ('                        width: playfulHelpScroll.width\n',
         '                        // Reserva 10 px para a barra de deslocação.\n'
         '                        width: Math.max(0, playfulHelpScroll.width - 10)\n',
         'Espaço reservado à ScrollBar'),
        ('                        Layout.fillWidth: true; spacing: 6\n'
         '                        Rectangle {\n'
         '                            Layout.preferredWidth: 34; Layout.preferredHeight: 34',
         '                        Layout.fillWidth: true; Layout.minimumWidth: 0; spacing: 6\n'
         '                        Rectangle {\n'
         '                            Layout.preferredWidth: win.width < 1270 ? 28 : 34\n'
         '                            Layout.preferredHeight: win.width < 1270 ? 28 : 34',
         'Cabeçalho compacto'),
        ('                            Layout.fillWidth: true\n'
         '                            text: win.playfulCopy("header")',
         '                            Layout.fillWidth: true\n'
         '                            Layout.minimumWidth: 0\n'
         '                            text: win.playfulCopy("header")',
         'Quebra do título da ajuda'),
        ('                        Layout.fillWidth: true; wrapMode: Text.WordWrap\n'
         '                        text: win.playfulCopy("intro")',
         '                        Layout.fillWidth: true; Layout.minimumWidth: 0\n'
         '                        wrapMode: Text.WordWrap\n'
         '                        text: win.playfulCopy("intro")',
         'Quebra da descrição'),
        ('font.pixelSize: win.width < 1270 ? 14 : 17; font.bold: true',
         'font.pixelSize: win.width < 1270 ? 12 : (win.width < 1450 ? 15 : 17); font.bold: true',
         'Tamanho responsivo da descrição'),
    ]
    for old,new,label in rules_panel:
        panel,state = substitute_once(panel,old,new,label);messages.append(state)
    source=source[:a]+panel+source[b:]
    return source,messages


def read_source(path):
    raw=path.read_bytes()
    bom=raw.startswith(b"\xef\xbb\xbf")
    value=raw.decode("utf-8-sig" if bom else "utf-8")
    newline="\r\n" if "\r\n" in value else "\n"
    return value.replace("\r\n","\n"),bom,newline


def encode_source(value,bom,newline):
    return (b"\xef\xbb\xbf" if bom else b"")+value.replace("\n",newline).encode("utf-8")


def atomic_write(path,raw):
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=str(path.parent))
    try:
        with os.fdopen(fd,"wb") as handle:
            handle.write(raw);handle.flush();os.fsync(handle.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def run(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--project",required=True,type=Path)
    action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check",action="store_true")
    action.add_argument("--apply",action="store_true")
    opts=parser.parse_args(args)
    project=opts.project.expanduser().resolve()
    targets=[project/"ui"/"Main.qml",project/"main.py"]
    if any(not p.is_file() for p in targets):
        raise ValueError("Não foram encontrados main.py e ui/Main.qml na pasta DEV.")
    planned=[]
    for target, fn in zip(targets,(patch_qml,patch_main)):
        original,bom,newline=read_source(target)
        updated,report=fn(original)
        for line in report: print(" - "+line)
        planned.append((target, original,updated,bom,newline))
    print("VERIFICAÇÃO PASS — ambos os ficheiros compatíveis.")
    if opts.check:
        print("Modo simulação: não foi alterado qualquer ficheiro.")
        return
    changed=[record for record in planned if record[1]!=record[2]]
    if not changed:
        print("JÁ ATUALIZADO — sem alterações adicionais.")
        return
    backupbase=Path(os.environ.get("LOCALAPPDATA") or Path.home())/"NONIVERUS"/"PosterTile"/"build_backups"
    backup=backupbase/("PlayfulResponsive_v0913_"+dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    backup.mkdir(parents=True,exist_ok=False)
    for target,*_ in changed:
        shutil.copy2(target,backup/target.name)
    written=[]
    try:
        for target,old,new,bom,newline in changed:
            atomic_write(target,encode_source(new,bom,newline))
            written.append(target)
    except Exception:
        for target in reversed(written):
            shutil.copy2(backup/target.name,target)
        raise
    print("Backup seguro: "+str(backup))
    print("SUCESSO — painel compacto e estilo Qt Basic preparados.")
    print("Não alterou o motor PDF, licenças, chaves ou instaladores.")


if __name__=="__main__":
    try:
        run()
    except (OSError,ValueError,UnicodeError) as exc:
        print("PARADO EM SEGURANÇA: "+str(exc),file=sys.stderr)
        sys.exit(1)
