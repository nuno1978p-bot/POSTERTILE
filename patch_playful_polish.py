#!/usr/bin/env python3
"""NONIVERUS PosterTile Playful Studio v0.9.1.1: narrowly scoped QML visual polish."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

RULES_FILE = Path(__file__).with_name("patch_rules.json")

def patch_qml(original, rules):
    result = original
    states = []
    problems = []
    for item in rules:
        old, new, label = item["old"], item["new"], item["id"]
        count_old = result.count(old)
        count_new = result.count(new)
        if count_new == 1:
            # A rule's older anchor may legitimately remain inside the new block.
            states.append((label, "já atualizado"))
        elif count_old == 1:
            result = result.replace(old, new, 1)
            states.append((label, "a atualizar"))
        else:
            problems.append(f"{label}: trechos encontrados (antigo={count_old}, novo={count_new})")
    if problems:
        raise RuntimeError(
            "Código QML diferente do esperado. Nenhum ficheiro será alterado.\n"
            + "\n".join("  - " + p for p in problems)
            + "\nEnvia ui\\Main.qml para uma adaptação exata; não forces a substituição."
        )
    return result, states

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    project = args.project.expanduser().resolve()
    dest = project / "ui" / "Main.qml"
    required_assets = [
        project / "assets" / "playful" / "astronaut_demo.png",
        project / "assets" / "playful" / "creative_helper.png",
        project / "assets" / "playful" / "playful_icon.png",
    ]
    if not dest.is_file():
        raise RuntimeError(f"Não existe {dest}")
    missing = [str(p) for p in required_assets if not p.is_file()]
    if missing:
        raise RuntimeError("Faltam recursos Playful Studio v0.9.1:\n" + "\n".join(missing))
    raw = dest.read_bytes()
    bom = b"\xef\xbb\xbf"
    had_bom = raw.startswith(bom)
    encoding = "utf-8-sig" if had_bom else "utf-8"
    original_as_stored = raw.decode(encoding)
    line_ending = "\r\n" if "\r\n" in original_as_stored else "\n"
    original = original_as_stored.replace("\r\n", "\n")
    if "Playful Studio" not in original or "studio.framedPreviewUrl" not in original:
        raise RuntimeError("Não parece ser o QML v0.9.1 DEV. Não foi alterado.")
    rules = json.loads(RULES_FILE.read_text(encoding="utf-8"))
    updated, states = patch_qml(original, rules)
    print("NONIVERUS PLAYFUL STUDIO v0.9.1.1 — POLIMENTO VISUAL")
    for label, state in states:
        print(f"  {label}: {state}")
    if args.check:
        print("VERIFICAÇÃO PASS — Nenhum ficheiro modificado.")
        return
    if updated == original:
        print("JÁ ATUALIZADO — Nenhuma alteração necessária.")
        return
    local = os.environ.get("LOCALAPPDATA") or str(Path.home())
    backup_base = Path(local) / "NONIVERUS" / "PosterTile" / "build_backups"
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_dir = backup_base / f"PlayfulPolish_v0911_{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)
    backup = backup_dir / "Main.qml"
    shutil.copy2(dest, backup)
    updated_raw = (bom if had_bom else b"") + updated.replace("\n", line_ending).encode("utf-8")
    fd, tmp = tempfile.mkstemp(prefix="Main.qml.", suffix=".tmp", dir=str(dest.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(updated_raw)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, dest)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    print(f"Cópia de segurança: {backup}")
    print("SUCESSO — Interface QML atualizada. Nenhum Python, motor PDF, licença ou instalador foi alterado.")

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, UnicodeError, RuntimeError) as exc:
        print(f"PARADO EM SEGURANÇA: {exc}", file=sys.stderr)
        sys.exit(1)
