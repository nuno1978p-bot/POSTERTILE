#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NONIVERUS PosterTile — seletor de tema + Definições no cabeçalho dos 3 temas.

Modificação delimitada a ui/Main.qml. Faz preflight e backup antes de escrita.
Não toca em main.py, licenciamento, instaladores, recursos ou exportação PDF.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
from pathlib import Path
import shutil
import sys
import tempfile


THEMES = '["Midnight Sapphire", "Pearl Titanium", "Playful Studio"]'
OLD_HEADER = """\
            LuxuryCombo {
                visible: win.playful
                Layout.preferredWidth: 172
                model: ["Midnight Sapphire", "Pearl Titanium", "Playful Studio"]
                currentIndex: studio.theme === "Midnight Sapphire" ? 0 : (studio.theme === "Pearl Titanium" ? 1 : 2)
                onActivated: studio.setTheme(currentText)
            }
            ActionButton { visible: !win.playful; text: "⚙  " + win.centerLabel("settings"); onClicked: centerDialog.open() }
            ActionButton { visible: win.playful; text: "⚙"; onClicked: centerDialog.open() }
"""

NEW_HEADER = """\
            // v0.9.1.5 — Mesmo conjunto de comandos nos três temas.
            // O ComboBox conserva os valores de tema reais e usa setTheme
            // (QSettings), sem interferir com as licenças ou a exportação PDF.
            LuxuryCombo {
                id: headerThemeSelector
                headerTheme: true
                Layout.preferredWidth: win.width < 1250 ? 174 : 196
                Layout.minimumWidth: 174
                model: ["Midnight Sapphire", "Pearl Titanium", "Playful Studio"]
                currentIndex: studio.theme === "Midnight Sapphire" ? 0 : (studio.theme === "Pearl Titanium" ? 1 : 2)
                onActivated: studio.setTheme(currentText)
            }
            ActionButton {
                id: headerSettingsButton
                Layout.preferredWidth: 46
                Layout.preferredHeight: 44
                Layout.minimumWidth: 46
                text: "⚙"
                onClicked: { win.centerPage = 0; centerDialog.open() }
                ToolTip.visible: hovered
                ToolTip.text: win.centerLabel("settings")
                Accessible.name: win.centerLabel("settings")
            }
"""

RULES = [
    ("Propriedade do seletor de tema",
     "        property bool localizeChoices: false\n",
     "        property bool localizeChoices: false\n"
     "        property bool headerTheme: false\n"),
    ("Espaço para ícone do tema",
     "        contentItem: Text { leftPadding: 14; rightPadding: 28; text: cb.localizeChoices",
     "        contentItem: Text { leftPadding: cb.headerTheme ? 37 : 14; rightPadding: 28; text: cb.localizeChoices"),
    ("Ícone contextual no seletor",
     '        indicator: Text { text: "⌄"; color:',
     """        Text {
            visible: cb.headerTheme
            text: win.playful ? "✿" : (win.light ? "✧" : "☾")
            color: win.playful ? "#FF648B" : (win.light ? "#B97543" : "#E9BA88")
            font.pixelSize: 18
            z: 2
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.verticalCenter: parent.verticalCenter
        }
        indicator: Text { text: "⌄"; color:"""),
    ("Cabeçalho: seletor e definições separados",
     OLD_HEADER, NEW_HEADER),
    ("Marcador decorativo em janelas pequenas",
     '            Rectangle { width: 7; height: 7; radius: 4; color: win.playful ?',
     '            Rectangle { visible: win.width >= 1250; width: 7; height: 7; radius: 4; color: win.playful ?'),
    ("Slogan da impressão em janelas pequenas",
     '            Text { text: win.playful ? "IMPRESSÃO DE ALTA QUALIDADE"',
     '            Text { visible: win.width >= 1250; text: win.playful ? "IMPRESSÃO DE ALTA QUALIDADE"'),
    ("Separador visual em janelas pequenas",
     '            Rectangle { width: 1; height: 26; color: line; Layout.leftMargin:',
     '            Rectangle { visible: win.width >= 1250; width: 1; height: 26; color: line; Layout.leftMargin:'),
    ("Ícone da aplicação no cabeçalho dos três temas",
     '            Image { visible: win.playful; source: "../assets/playful/playful_icon.png"; Layout.preferredWidth:',
     '            Image { visible: win.width >= 1250; source: win.playful ? "../assets/playful/playful_icon.png" : "../assets/branding/postertile_icon.png"; Layout.preferredWidth:'),
]


def patch_qml(source: str) -> tuple[str, list[str]]:
    if "property bool playful:" not in source or 'model: ' + THEMES not in source:
        raise ValueError("Não é reconhecida a estrutura Playful Studio v0.9.1.")
    states: list[str] = []
    result = source
    for name, old, new in RULES:
        count_new = result.count(new)
        count_old = result.count(old)
        if count_new == 1 and (count_old == 0 or (old in new and count_old == 1)):
            states.append(f"{name}: já aplicado")
        elif count_old == 1 and count_new == 0:
            result = result.replace(old, new, 1)
            states.append(f"{name}: a aplicar")
        else:
            raise ValueError(
                f"{name}: âncora ambígua ou alterada (antigo={count_old}, novo={count_new}). "
                "Nenhum ficheiro foi alterado. É necessário analisar ui/Main.qml."
            )

    if result.count('id: headerThemeSelector') != 1:
        raise ValueError("Falhou a unicidade do seletor do cabeçalho.")
    if result.count('id: headerSettingsButton') != 1:
        raise ValueError("Falhou a unicidade do botão de Definições.")
    if 'ActionButton { visible: !win.playful; text: "⚙' in result:
        raise ValueError("O botão antigo ainda aparece no cabeçalho.")
    if result.count('model: ' + THEMES) < 2:
        raise ValueError("Não foram encontradas as escolhas de tema no Control Center.")
    return result, states


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", type=Path, required=True)
    action = ap.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dest = args.project.expanduser().resolve() / "ui" / "Main.qml"
    if not dest.is_file():
        raise ValueError("Ficheiro ui/Main.qml não encontrado. Verifica a pasta DEV.")

    raw = dest.read_bytes()
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    source = raw[len(bom):].decode("utf-8")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    normalized = source.replace("\r\n", "\n")
    result, states = patch_qml(normalized)

    print("NONIVERUS PosterTile v0.9.1.5 — seleção de temas em todos os temas")
    print("Destino:", dest)
    for item in states:
        print(" -", item)
    if result == normalized:
        print("JÁ ATUALIZADO. Nenhuma alteração necessária.")
        return 0
    if args.check:
        print("VERIFICAÇÃO PASS. Nenhum ficheiro foi modificado.")
        return 0

    # Confirmar que nada alterou o ficheiro depois da leitura.
    if hashlib.sha256(dest.read_bytes()).digest() != hashlib.sha256(raw).digest():
        raise RuntimeError("O QML foi alterado durante a verificação. Operação cancelada.")

    backup_root = (
        Path(os.getenv("LOCALAPPDATA", str(Path.home())))
        / "NONIVERUS" / "PosterTile" / "build_backups"
    )
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = backup_root / ("ThemeHeader_v0915_" + stamp) / "Main.qml"
    backup.parent.mkdir(parents=True, exist_ok=False)
    shutil.copy2(dest, backup)
    print("Backup seguro:", backup)

    output = bom + result.replace("\n", newline).encode("utf-8")
    fd, temporary = tempfile.mkstemp(
        prefix=".Main_theme_header_", suffix=".tmp", dir=dest.parent
    )
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(output)
            stream.flush()
            os.fsync(stream.fileno())
        shutil.copystat(dest, temporary)
        os.replace(temporary, dest)
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)
    print("SUCESSO: seleção de tema e botão Definições disponíveis nos três temas.")
    print("Não foram modificados main.py, PDF, chaves, edição ou instaladores.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError, UnicodeError) as exc:
        print("PARADO EM SEGURANÇA:", exc, file=sys.stderr)
        sys.exit(2)
