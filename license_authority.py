# -*- coding: utf-8 -*-
"""NONIVERUS License Authority, OFFLINE. Owner only. Never ship its private key."""
import argparse
import json
import os
from pathlib import Path
import time
from datetime import datetime, timezone

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from license_core import parse_request, signed_license

def authority_dir():
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        raise RuntimeError("LOCALAPPDATA não definido. Usar no teu Windows.")
    return Path(local) / "NONIVERUS" / "PosterTile" / "owner_private"

def private_key_path():
    return authority_dir() / "license_signer_ed25519.pem"

def public_key_path():
    return authority_dir() / "license_signer_public.bin"

def load_key():
    p = private_key_path()
    if not p.is_file():
        raise FileNotFoundError(
            "Falta a chave privada. Executa 'python license_authority.py init' no PC Owner.")
    obj = serialization.load_pem_private_key(p.read_bytes(), password=None)
    if not isinstance(obj, Ed25519PrivateKey):
        raise ValueError("A chave guardada não é Ed25519.")
    return obj

def init_key():
    private = private_key_path()
    if private.exists() or public_key_path().exists():
        raise FileExistsError("Já existe uma chave. NUNCA substituir: invalida licenças emitidas.")
    private.parent.mkdir(parents=True, exist_ok=True)
    key = Ed25519PrivateKey.generate()
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption())
    # Exclusive create; never overwrite the signing secret.
    with private.open("xb") as f:
        f.write(pem)
    public_key_path().write_bytes(
        key.public_key().public_bytes(
            serialization.Encoding.Raw,
            serialization.PublicFormat.Raw))
    return private

def record_issued(request, cert, days):
    # Local owner audit log. This file is never packaged.
    record = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "request": request,
        "license_id": cert.split("|")[1],
        "fingerprint": cert.split("|")[2],
        "valid_days": int(days),
    }
    path = authority_dir() / "issued_licenses.jsonl"
    with path.open("a", encoding="utf8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def issue(request, days=0):
    request = request.strip()
    parse_request(request)
    cert = signed_license(load_key(), request, days=days)
    record_issued(request, cert, days)
    return cert

def gui():
    from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPlainTextEdit, QPushButton, QSpinBox, QMessageBox)
    import sys
    app = QApplication.instance() or QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("NONIVERUS  /  LICENSE AUTHORITY  ·  OWNER ONLY")
    w.resize(760, 510)
    w.setStyleSheet("""
        QWidget { background:#111E31; color:#ECEFF5; font-size:13px; }
        QLabel { color:#E6E8F0; }
        QPlainTextEdit { background:#1F3049; border:1px solid #506078;
          border-radius:8px; padding:8px; color:#F2E7D3; }
        QPushButton {background:#C29B69; color:#102037; border:0;
          border-radius:8px; padding:12px; font-weight:700;}
        QSpinBox {background:#23354F; color:white; padding:6px;}
    """)
    layout = QVBoxLayout(w)
    headline = QLabel("NONIVERUS  ·  LICENSE AUTHORITY")
    headline.setStyleSheet("font-weight:700; font-size:20px; color:#D7B77D;")
    layout.addWidget(headline)
    layout.addWidget(QLabel("Ferramenta privada do proprietário · Não distribuir."))
    layout.addWidget(QLabel("PEDIDO DE ATIVAÇÃO recebido por WhatsApp"))
    incoming = QPlainTextEdit()
    incoming.setPlaceholderText("NVREQ1|…")
    incoming.setMaximumHeight(92)
    layout.addWidget(incoming)
    row = QHBoxLayout()
    row.addWidget(QLabel("Validade em dias (0 = sem expiração):"))
    days = QSpinBox()
    days.setRange(0, 3650)
    row.addWidget(days)
    layout.addLayout(row)
    create = QPushButton("GERAR LICENÇA ASSINADA")
    layout.addWidget(create)
    layout.addWidget(QLabel("LICENÇA A ENVIAR AO UTILIZADOR"))
    outgoing = QPlainTextEdit()
    outgoing.setReadOnly(True)
    layout.addWidget(outgoing)
    copy = QPushButton("COPIAR LICENÇA PARA O WHATSAPP")
    layout.addWidget(copy)
    copy.clicked.connect(lambda: QApplication.clipboard().setText(outgoing.toPlainText()))
    def make():
        try:
            cert = issue(incoming.toPlainText(), days.value())
            outgoing.setPlainText(cert)
        except Exception as exc:
            QMessageBox.warning(w, "Não foi possível emitir", str(exc))
    create.clicked.connect(make)
    w.show()
    return app.exec()

def main():
    p = argparse.ArgumentParser(description="NONIVERUS License Authority — OWNER ONLY")
    p.add_argument("operation", nargs="?", default="gui", choices=["init", "gui", "issue", "status"])
    p.add_argument("--request", default="")
    p.add_argument("--days", type=int, default=0)
    args = p.parse_args()
    if args.operation == "init":
        print("Chave criada:", init_key())
        print("A chave privada NUNCA deve entrar em Git, ZIP ou instaladores.")
    elif args.operation == "issue":
        if not args.request:
            p.error("--request obrigatório")
        print(issue(args.request, args.days))
    elif args.operation == "gui":
        if not private_key_path().exists():
            from PySide6.QtWidgets import QApplication, QMessageBox
            import sys
            app = QApplication.instance() or QApplication(sys.argv)
            result = QMessageBox.question(None, "NONIVERUS License Authority",
                "Ainda não existe uma chave privada de licenças neste computador.\\n\\n"
                "Criar uma chave Ed25519 exclusiva? Precisas de guardar uma cópia de "
                "segurança segura: sem esta chave não poderás reemitir licenças com "
                "a mesma identidade.",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result != QMessageBox.Yes:
                return 2
            init_key()
            QMessageBox.information(None, "NONIVERUS License Authority",
                "Chave criada na área privada do Windows.\\n"
                "Nunca coloques a chave privada no GitHub nem nos instaladores.")
        return gui()
    else:
        print("Chave privada:", "SIM" if private_key_path().exists() else "NÃO")
        print("Chave pública:", "SIM" if public_key_path().exists() else "NÃO")
        print("Emissões:", authority_dir() / "issued_licenses.jsonl")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
