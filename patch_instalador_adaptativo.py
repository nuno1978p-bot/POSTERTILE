# -*- coding: utf-8 -*-
"""NONIVERUS v0.9.0.2: patch pontual da logica de atualizacao Inno Setup.
Nao usa hashes globais, nao substitui ficheiros inteiros nem acede a chaves privadas.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from datetime import datetime

FILES = ("build_editions.py", "main.py", "ui/Main.qml", "version_info.txt")
EXPECTED_IDS = (
    "A21297EC-47C8-4A17-8CB9-DA95C70645A9",
    "47FD65E8-338F-45CE-9F74-2DF0B0AB9C41",
)

def read_source(path: Path) -> tuple[str, bytes]:
    raw = path.read_bytes()
    mark = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    return raw[len(mark):].decode("utf-8"), mark

def replace_count(src: str, old: str, new: str, count: int, label: str) -> str:
    actual = src.count(old)
    if actual != count:
        raise RuntimeError(
            f"{label}: esperava {count} ocorrencias de {old!r}, encontrei {actual}. "
            "Nao foi alterado qualquer ficheiro."
        )
    return src.replace(old, new)

def replace_version(src: str, old: str, new: str, expected_count: int, label: str) -> str:
    if new in src and old not in src:
        # Already fully updated for this field
        return src
    return replace_count(src, old, new, expected_count, label)

def apply_builder(src: str, fragment: str) -> str:
    if not src.startswith("# -*- coding: utf-8 -*-") and "def make_installer_script" not in src:
        raise RuntimeError("build_editions.py nao corresponde ao compilador NONIVERUS conhecido.")
    if any(x not in src for x in EXPECTED_IDS):
        raise RuntimeError("AppIds diferentes dos originais. Aplicacao recusada para proteger as edicoes.")
    if "def make_installer_script(" not in src or "def compile_native(" not in src:
        raise RuntimeError("Nao encontrei as funcoes esperadas do builder.")
    if "UPDATE_INSTALLER_CODE" in src:
        if "Setup_v0.9.0.2" in src and "contents += UPDATE_INSTALLER_CODE" in src:
            return src
        raise RuntimeError("O builder ja tem outro codigo de atualizacao. Nao vou duplicar.")
    src = replace_count(
        src, "\ndef make_installer_script(edition, exe_name):",
        "\n" + fragment.rstrip() + "\n\ndef make_installer_script(edition, exe_name):",
        1, "Ponto de insercao do [Code]"
    )
    for old in ("0.9.0.1", "0.9.0"):
        if f'Setup_v{old}"' in src:
            src = replace_count(src, f'Setup_v{old}"', 'Setup_v0.9.0.2"', 1, "Nome do Setup")
            break
    else:
        raise RuntimeError("Nome da versao no builder inesperado.")
    for old in ("0.9.0.1", "0.9.0"):
        if f'#define MyAppVersion "{old}"' in src:
            src = replace_count(src, f'#define MyAppVersion "{old}"', '#define MyAppVersion "0.9.0.2"', 1, "MyAppVersion")
            break
    else:
        raise RuntimeError("Versao Inno nao identificada.")
    for old in ("0.9.0.1", "0.9.0.0"):
        if f'VersionInfoVersion={old}' in src:
            src = replace_count(src, f'VersionInfoVersion={old}', 'VersionInfoVersion=0.9.0.2', 1, "VersionInfoVersion")
            break
    else:
        raise RuntimeError("Versao EXE inesperada no builder.")
    if "DisableDirPage=no" not in src:
        raise RuntimeError("Builder sem configuracao de pasta esperada. Nao foi alterado qualquer ficheiro.")
    anchor = '    contents = contents.replace("AppId={{" + appid + "}}", "AppId={{" + appid + "}")'
    addition = (
        '\n    contents = contents.replace(\n'
        '        "DisableDirPage=no",\n'
        '        "DisableDirPage=auto\\nUsePreviousAppDir=yes\\nUsePreviousTasks=yes",\n'
        '    )\n'
        '    contents += UPDATE_INSTALLER_CODE.replace("__APPID__", appid)'
    )
    # This gets expanded in Python code before Inno generation.
    src = replace_count(src, anchor, anchor + addition, 1, "Geracao do instalador")
    compile(src, "build_editions.py", "exec")
    return src

def apply_main(src: str) -> str:
    if "NONIVERUS PosterTile Luxury Studio" not in src:
        raise RuntimeError("main.py inesperado.")
    for old in ("v0.9.0.1", "v0.9.0"):
        if old in src:
            return replace_count(src, old, "v0.9.0.2", 1, "Cabecalho do main.py")
    if "v0.9.0.2" in src:
        return src
    raise RuntimeError("Versao inesperada em main.py.")

def apply_qml(src: str) -> str:
    if "centerDialog" not in src:
        raise RuntimeError("Main.qml nao parece ser o Control Center v0.9.x.")
    # All user-visible v0.9.0(.1) labels only, preserve all layout and styling.
    if "v0.9.0.2" in src and "v0.9.0.1" not in src and "v0.9.0  /" not in src:
        return src
    if "v0.9.0.1" in src:
        return replace_count(src, "v0.9.0.1", "v0.9.0.2", src.count("v0.9.0.1"), "Versao QML")
    if "v0.9.0  /" in src:
        return replace_count(src, "v0.9.0  /", "v0.9.0.2  /", src.count("v0.9.0  /"), "Versao QML")
    raise RuntimeError("Nao encontrei a versao no Main.qml.")

def apply_version_info(src: str) -> str:
    src = re.sub(r"filevers=\(0,9,0,\d+\),prodvers=\(0,9,0,\d+\)",
                 "filevers=(0,9,0,2),prodvers=(0,9,0,2)", src, count=1)
    for label in ("FileVersion", "ProductVersion"):
        pat = r"(StringStruct\('" + label + r"','?)0\.9\.0(?:\.\d+)?('\))"
        src, n = re.subn(pat, lambda m: m.group(1) + "0.9.0.2" + m.group(2), src)
        if n != 1:
            raise RuntimeError(f"version_info.txt: campo {label} inesperado.")
    if "filevers=(0,9,0,2),prodvers=(0,9,0,2)" not in src:
        raise RuntimeError("version_info.txt: nao encontrei FixedFileInfo.")
    return src

def run(project: Path, dry_run: bool) -> None:
    if not project.is_dir():
        raise RuntimeError("Pasta DEV nao encontrada: " + str(project))
    fragment = (Path(__file__).parent / "inno_update_block.pyfrag").read_text(encoding="utf-8")
    funcs = {
        "build_editions.py": lambda x: apply_builder(x, fragment),
        "main.py": apply_main,
        "ui/Main.qml": apply_qml,
        "version_info.txt": apply_version_info,
    }
    old_content: dict[str, bytes] = {}
    new_content: dict[str, bytes] = {}
    print("A verificar a estrutura e a integridade dos ficheiros...")
    for rel in FILES:
        path = project / rel
        if not path.is_file():
            raise RuntimeError("Ficheiro em falta: " + str(path))
        old = path.read_bytes()
        src, bom = read_source(path)
        updated = funcs[rel](src)
        if updated == src:
            print("Ja atualizado:", rel)
            continue
        out = bom + updated.encode("utf-8")
        old_content[rel] = old
        new_content[rel] = out
        print("Pode atualizar:", rel, "(sem substituir o resto do codigo)")
    if not new_content:
        print("Este projeto ja parece atualizado. Nada a fazer.")
        return
    if dry_run:
        print("SIMULACAO OK. Nao foram feitas alteracoes.")
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / \
                  "NONIVERUS" / "PosterTile" / "build_backups" / ("InstallerUpdate_v0902_adaptativo_" + stamp)
    for rel, raw in old_content.items():
        dest = backup_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
    print("Backup dos originais:", backup_root)
    for rel, raw in new_content.items():
        target = project / rel
        temp_file = target.with_name(target.name + ".nvpatch.tmp")
        try:
            temp_file.write_bytes(raw)
            os.replace(temp_file, target)
        finally:
            if temp_file.exists():
                temp_file.unlink()
        print("Atualizado:", rel)
    print("\nSUCESSO: v0.9.0.2 preparada. Nao foram tocadas chaves privadas.")
    print("Para compilar: CONSTRUIR_OWNER_WINDOWS.cmd e CONSTRUIR_PREVIEW_WINDOWS.cmd")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=r"C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        run(Path(a.project), a.dry_run)
    except Exception as exc:
        print("PARADO EM SEGURANCA:", exc, file=sys.stderr)
        sys.exit(1)
