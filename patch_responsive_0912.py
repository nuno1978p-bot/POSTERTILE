#!/usr/bin/env python3
"""NONIVERUS PosterTile v0.9.1.2 — focused responsive window QML hotfix.

Preserves all other code. Safe --check and --apply, creates external backup.
"""
import argparse
import datetime
import os
from pathlib import Path
import sys
import tempfile
import shutil


def replace_once(source: str, old: str, new: str, name: str) -> tuple[str, str]:
    # Testa primeiro a assinatura antiga: alguns destinos começam pelo mesmo texto.
    if source.count(old) == 1:
        return source.replace(old, new, 1), "a atualizar"
    if source.count(old) == 0 and source.count(new) == 1:
        return source, "já atualizado"
    raise ValueError(f"{name}: não foi encontrado um ponto único e seguro "
                     f"(antigo={source.count(old)}, novo={source.count(new)}). Nenhum ficheiro alterado.")


def upgrade(source: str) -> tuple[str, list[str]]:
    messages = []
    if 'id: win' not in source or 'property bool playful:' not in source:
        raise ValueError("Não parece ser o Main.qml Playful Studio v0.9.1.")

    source, state = replace_once(
        source,
        "    visible: true\n    title:",
        "    visible: true\n"
        "    // v0.9.1.2: janela nativa maximizada, não em ecrã inteiro.\n"
        "    // Respeita a barra de tarefas; permite minimizar e restaurar.\n"
        "    Component.onCompleted: win.showMaximized()\n"
        "    title:",
        "Arranque maximizado")
    messages.append(f"Janela: {state}")

    source, state = replace_once(
        source,
        "    minimumWidth: 1100; minimumHeight: 700",
        "    minimumWidth: 1100; minimumHeight: 600",
        "Altura mínima com barra de tarefas")
    messages.append(f"Limites da janela: {state}")

    source, state = replace_once(
        source,
        "Layout.preferredWidth: win.playful ? 365 : 356; Layout.fillHeight: true",
        "Layout.preferredWidth: win.playful ? (win.width < 1270 ? 300 : "
        "(win.width < 1450 ? 335 : 365)) : 356; Layout.fillHeight: true",
        "Sidebar adaptativa")
    messages.append(f"Sidebar: {state}")

    source, state = replace_once(
        source,
        "font.pixelSize: win.playful ? 25 : 23",
        "font.pixelSize: win.playful ? (win.width < 1270 ? 20 : 25) : 23",
        "Título da área de pré-visualização")
    messages.append(f"Título: {state}")

    old_comment = "            // Playful dashboard companion: compact guidance and enlarged mascot."
    new_comment = (
        "            // v0.9.1.2: o painel direito adapta-se e não desaparece ao redimensionar.\n"
        "            // Em altura reduzida, o conteúdo pode ser deslocado com a roda do rato."
    )
    source, state = replace_once(source, old_comment, new_comment, "Comentário do painel")
    messages.append(f"Painel direito: {state}")

    start = source.find(new_comment)
    if start < 0:
        raise ValueError("Não foi possível localizar o painel direito.")
    end_marker = (
        "        RowLayout {\n"
        "            Layout.fillWidth: true; Layout.preferredHeight: 18"
    )
    end = source.find(end_marker, start)
    if end < 0:
        raise ValueError("Não foi possível localizar o rodapé a seguir ao painel.")
    right = source[start:end]

    rules = [
        ("visible: win.playful && win.width >= 1430 && win.height >= 840",
         "visible: win.playful", "Visibilidade"),
        ("Layout.preferredWidth: visible ? 236 : 0",
         "Layout.preferredWidth: visible ? (win.width < 1270 ? 178 : "
         "(win.width < 1450 ? 204 : 236)) : 0\n"
         "                Layout.minimumWidth: visible ? 165 : 0\n"
         "                Layout.maximumWidth: visible ? 236 : 0", "Largura"),
        (
            "                ColumnLayout {\n"
            "                    anchors.fill: parent\n"
            "                    anchors.margins: 12\n"
            "                    spacing: 10\n"
            "                    RowLayout {",
            "                Flickable {\n"
            "                    id: playfulHelpScroll\n"
            "                    anchors.fill: parent\n"
            "                    anchors.margins: win.width < 1270 ? 8 : 12\n"
            "                    clip: true\n"
            "                    contentWidth: width\n"
            "                    contentHeight: playfulHelpContent.height\n"
            "                    boundsBehavior: Flickable.StopAtBounds\n"
            "                    ScrollBar.vertical: ScrollBar {\n"
            "                        policy: ScrollBar.AsNeeded\n"
            "                    }\n"
            "                    ColumnLayout {\n"
            "                        id: playfulHelpContent\n"
            "                        width: playfulHelpScroll.width\n"
            "                        height: Math.max(implicitHeight, playfulHelpScroll.height)\n"
            "                        spacing: win.width < 1270 ? 7 : 10\n"
            "                    RowLayout {",
            "Área deslocável",
        ),
        ("color: \"#103676\"; font.pixelSize: 17; font.bold: true",
         "color: \"#103676\"; font.pixelSize: win.width < 1270 ? 14 : 17; font.bold: true",
         "Texto compacto"),
        (
            '                    PlayfulBenefit { benefit: win.playfulCopy("d"); accent: "#FF6285" }\n'
            '                    Image {',
            '                    PlayfulBenefit { benefit: win.playfulCopy("d"); accent: "#FF6285" }\n'
            '                    Item { Layout.fillHeight: true; Layout.minimumHeight: 0 }\n'
            '                    Image {',
            "Alinhamento ilustração",
        ),
        (
            "                        Layout.fillHeight: true\n"
            "                        Layout.minimumHeight: 190\n"
            "                        Layout.maximumHeight: 355",
            "                        Layout.preferredHeight: win.width < 1270 ? 170 : "
            "(win.height < 850 ? 205 : 255)\n"
            "                        Layout.minimumHeight: 125\n"
            "                        Layout.maximumHeight: 355",
            "Dimensões ilustração",
        ),
    ]
    changed = False
    for old, new, label in rules:
        right, current = replace_once(right, old, new, label)
        if current == "a atualizar":
            changed = True
        messages.append(f"  {label}: {current}")

    # Add one closing brace for the Flickable. Never duplicate it.
    tail_old = (
        "                        asynchronous: true\n"
        "                    }\n"
        "                }\n"
        "            }\n"
        "        }\n"
    )
    tail_new = (
        "                        asynchronous: true\n"
        "                    }\n"
        "                    }\n"
        "                }\n"
        "            }\n"
        "        }\n"
    )
    right, state = replace_once(right, tail_old, tail_new, "Fecho do painel deslocável")
    messages.append(f"  Estrutura QML: {state}")
    source = source[:start] + right + source[end:]

    if source.count('Component.onCompleted: win.showMaximized()') != 1:
        raise ValueError("Arranque maximizado duplicado ou ausente.")
    if 'visible: win.playful && win.width >= 1430' in source:
        raise ValueError("Ainda existe a condição que oculta o painel.")
    if 'id: playfulHelpScroll' not in source:
        raise ValueError("Falta o painel adaptativo.")
    return source, messages


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--apply", action="store_true")
    options = parser.parse_args()
    target = options.project / "ui" / "Main.qml"
    if not target.is_file():
        raise ValueError(f"Ficheiro não encontrado: {target}")
    data = target.read_bytes()
    bom = data.startswith(b"\xef\xbb\xbf")
    original = data.decode("utf-8-sig" if bom else "utf-8")
    crlf = "\r\n" in original
    normalized = original.replace("\r\n", "\n")
    updated, messages = upgrade(normalized)
    print("NONIVERUS PLAYFUL STUDIO — RESPONSIVO v0.9.1.2")
    for message in messages:
        print("  " + message)
    if options.check:
        print("VERIFICAÇÃO PASS — nenhum ficheiro modificado.")
        return
    if normalized == updated:
        print("JÁ ATUALIZADO — nenhuma alteração necessária.")
        return
    backup_base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) \
        / "NONIVERUS" / "PosterTile" / "build_backups"
    backup = backup_base / ("Responsive_v0912_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copy2(target, backup / "Main.qml")
    payload = updated.replace("\n", "\r\n" if crlf else "\n")
    new_bytes = (b"\xef\xbb\xbf" if bom else b"") + payload.encode("utf-8")
    fd, name = tempfile.mkstemp(prefix="Main.qml.", suffix=".tmp", dir=str(target.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(new_bytes)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, target)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    print("BACKUP: " + str(backup / "Main.qml"))
    print("SUCESSO — QML atualizado. Sem alterações a Python, PDFs, instaladores ou licenças.")


if __name__ == "__main__":
    try:
        run()
    except (OSError, ValueError, UnicodeError) as exc:
        print("PARADO EM SEGURANÇA: " + str(exc), file=sys.stderr)
        sys.exit(1)
