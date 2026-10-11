# -*- coding: utf-8 -*-
"""NONIVERUS v0.9.1.4 — patch focused on the native Windows title bar.

Never replaces the user's main.py with a packaged version.
"""
from __future__ import annotations

import argparse
import ast
import os
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HELPER = '# NONIVERUS TITLEBAR v0.9.1.4 BEGIN\n# Windows 11 desktop-window-manager integration. This only changes the native\n# title bar; it does not modify the Qt window flags or the Windows taskbar.\n_NATIVE_TITLEBAR_PALETTE = {\n    "Playful Studio": ("#E7F4FF", "#173B75"),\n    "Pearl Titanium": ("#E9E5DE", "#142D4A"),\n    "Midnight Sapphire": ("#101B2C", "#F2F4F6"),\n}\n\ndef _native_titlebar_colorref(hex_color):\n    """Convert #RRGGBB to Win32 COLORREF 0x00BBGGRR."""\n    rgb = hex_color.lstrip("#")\n    return int(rgb[4:6] + rgb[2:4] + rgb[:2], 16)\n\ndef _apply_native_titlebar_colors(window, theme):\n    if sys.platform != "win32":\n        return False\n    try:\n        import ctypes\n        from ctypes import wintypes\n        hwnd = int(window.winId())\n        if not hwnd:\n            return False\n        caption, foreground = _NATIVE_TITLEBAR_PALETTE.get(\n            theme, _NATIVE_TITLEBAR_PALETTE["Midnight Sapphire"])\n        dwm = ctypes.WinDLL("dwmapi").DwmSetWindowAttribute\n        dwm.argtypes = (wintypes.HWND, wintypes.DWORD,\n                        ctypes.c_void_p, wintypes.DWORD)\n        dwm.restype = ctypes.c_long\n\n        # Keep native buttons; only choose the light/dark caption rendering.\n        dark = ctypes.c_int(1 if theme == "Midnight Sapphire" else 0)\n        dwm(wintypes.HWND(hwnd), 20, ctypes.byref(dark),\n            ctypes.sizeof(dark))\n\n        def set_color(attribute, color):\n            value = ctypes.c_uint32(_native_titlebar_colorref(color))\n            return dwm(wintypes.HWND(hwnd), attribute,\n                       ctypes.byref(value), ctypes.sizeof(value)) == 0\n\n        # DWMWA_CAPTION_COLOR=35, DWMWA_TEXT_COLOR=36.\n        # Windows 11 build 22000+; unsupported systems simply keep native UI.\n        return set_color(35, caption) and set_color(36, foreground)\n    except (OSError, AttributeError, ValueError, TypeError):\n        return False\n# NONIVERUS TITLEBAR v0.9.1.4 END\n\n'
HOOK = '    # NONIVERUS TITLEBAR v0.9.1.4 HOOK BEGIN\n    # QML has been loaded; synchronize native Windows caption with the theme.\n    from PySide6.QtCore import QTimer\n    main_window = engine.rootObjects()[0]\n    titlebar_cache = [None]\n    def refresh_native_titlebar(force=False):\n        if sys.platform != "win32":\n            return\n        key = (int(main_window.winId()), bridge.theme)\n        if force or key != titlebar_cache[0]:\n            titlebar_cache[0] = key\n            _apply_native_titlebar_colors(main_window, bridge.theme)\n    bridge.changed.connect(refresh_native_titlebar)\n    if hasattr(main_window, "visibilityChanged"):\n        main_window.visibilityChanged.connect(\n            lambda *_: QTimer.singleShot(0, lambda: refresh_native_titlebar(True)))\n    if hasattr(main_window, "windowStateChanged"):\n        main_window.windowStateChanged.connect(\n            lambda *_: QTimer.singleShot(0, lambda: refresh_native_titlebar(True)))\n    QTimer.singleShot(0, refresh_native_titlebar)\n    # NONIVERUS TITLEBAR v0.9.1.4 HOOK END\n'

MARK1 = "# NONIVERUS TITLEBAR v0.9.1.4 BEGIN"
MARK2 = "# NONIVERUS TITLEBAR v0.9.1.4 HOOK BEGIN"

def prepare(path: Path):
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    if MARK1 in text or MARK2 in text:
        if all(x in text for x in (MARK1, MARK2,
            "# NONIVERUS TITLEBAR v0.9.1.4 END",
            "# NONIVERUS TITLEBAR v0.9.1.4 HOOK END")):
            ast.parse(text, filename=str(path))
            return None
        raise ValueError("Foi detetada uma aplicacao parcial da v0.9.1.4.")

    insertion = newline + "def main():"
    return_line = "    return app.exec()"
    if text.count(insertion) != 1 or text.count(return_line) != 1:
        raise ValueError("Nao foi encontrado um ponto de insercao unico em main.py.")
    if "engine.rootObjects()" not in text or "bridge=Studio()" not in text:
        raise ValueError("Estrutura da aplicacao nao reconhecida; nao alterar.")

    def lines(value):
        return value.replace("\n", newline)

    new = text.replace(insertion, newline + lines(HELPER) + "def main():", 1)
    new = new.replace(return_line, lines(HOOK) + return_line, 1)
    ast.parse(new, filename=str(path))
    binary = new.encode("utf-8")
    return (b"\xef\xbb\xbf" if bom else b"") + binary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="Pasta raiz NONIVERUS_POSTERTILE_DEV")
    parser.add_argument("--check", action="store_true", help="Simulacao sem alterar ficheiros")
    opts = parser.parse_args()
    target = Path(opts.project).resolve() / "main.py"
    if not target.is_file():
        raise ValueError("Nao foi encontrado main.py no projeto DEV.")
    prepared = prepare(target)
    if prepared is None:
        print("JA ATUALIZADO: v0.9.1.4, sem alteracoes.")
        return 0
    if opts.check:
        print("VERIFICACAO PASS: main.py compativel; sintaxe Python valida; nada alterado.")
        return 0

    backup_root = (Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) /
                   "NONIVERUS" / "PosterTile" / "build_backups")
    backup = backup_root / ("TitleBar_v0914_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copy2(target, backup / "main.py")
    print("Copia de seguranca:", backup / "main.py")

    tempname = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", prefix="._titlebar_0914_", suffix=".tmp",
            dir=target.parent, delete=False
        ) as output:
            tempname = output.name
            output.write(prepared)
            output.flush()
            os.fsync(output.fileno())
        shutil.copymode(target, tempname)
        os.replace(tempname, target)
    finally:
        if tempname and os.path.exists(tempname):
            os.unlink(tempname)

    if prepare(target) is not None:
        raise RuntimeError("Verificacao posterior inesperada. Recupera a copia de seguranca.")
    print("SUCESSO: barra de titulo adaptativa v0.9.1.4 instalada.")
    print("Nenhuma chave, licenca, QML ou ferramenta de instalacao foi alterada.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, SyntaxError, ValueError, RuntimeError) as error:
        print("PARADO EM SEGURANCA:", error, file=sys.stderr)
        sys.exit(1)
