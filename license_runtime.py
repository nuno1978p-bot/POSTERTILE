# -*- coding: utf-8 -*-
"""Private Preview activation. Never contains any signing secret."""
import ctypes
import hashlib
import os
from pathlib import Path
import sys
import time

from license_core import make_request, HEX_DEVICE

APP_NAMESPACE = b"NONIVERUS:PosterTile:private-preview:v1:"

def device_fingerprint():
    """Stable per Windows installation. Hash raw MachineGuid; never expose the GUID."""
    if sys.platform != "win32":
        raise RuntimeError("Private Preview permite ativação apenas em Windows.")
    import winreg
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                        r"SOFTWARE\Microsoft\Cryptography",
                        0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
        raw = winreg.QueryValueEx(key, "MachineGuid")[0]
    if not isinstance(raw, str) or len(raw.strip()) < 10:
        raise RuntimeError("Identificador do Windows indisponível.")
    return hashlib.sha256(APP_NAMESPACE + raw.strip().lower().encode("utf-8")).hexdigest()


def license_path():
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        raise RuntimeError("LOCALAPPDATA indisponível.")
    return Path(local) / "NONIVERUS" / "PosterTile" / "licenses" / "private_preview.lic"


def native_path(base):
    return Path(base) / "native" / "nv_license_native.dll"


def validate_certificate(data, base, fingerprint=None, now=None):
    """Strict: no native library == no preview access."""
    fp = fingerprint if fingerprint is not None else device_fingerprint()
    if not HEX_DEVICE.fullmatch(fp):
        return False
    dll_path = native_path(base)
    if not dll_path.is_file():
        return False
    if isinstance(data, str):
        try:
            data = data.strip().encode("ascii")
        except UnicodeEncodeError:
            return False
    if not isinstance(data, bytes) or len(data) > 2048:
        return False
    try:
        dll = ctypes.CDLL(str(dll_path))
        fn = dll.nv_verify_license
        fn.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_uint64)
        fn.restype = ctypes.c_int
        buf = ctypes.create_string_buffer(data)
        stamp = int(time.time()) if now is None else int(now)
        return fn(buf, len(data), fp.encode("ascii"), stamp) == 0
    except (OSError, ValueError, AttributeError, TypeError):
        return False


def is_activated(base):
    try:
        path = license_path()
        if not path.is_file() or path.stat().st_size > 2048:
            return False
        return validate_certificate(path.read_bytes(), base)
    except (OSError, ValueError, RuntimeError):
        return False


def install_license(value, base):
    value = value.strip()
    if not validate_certificate(value, base):
        raise ValueError("Licença inválida, caducada ou emitida para outro computador.")
    path = license_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(value + "\n", encoding="ascii")
    tmp.replace(path)
    return path


def activate_interactively(base):
    """A preview has NO interface/project/export unless activation passes."""
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (QDialog, QLabel, QVBoxLayout, QPushButton,
        QTextEdit, QApplication, QHBoxLayout, QMessageBox)
    if is_activated(base):
        return True
    try:
        fingerprint = device_fingerprint()
        request = make_request(fingerprint)
    except Exception as exc:
        QMessageBox.critical(None, "NONIVERUS Private Preview", str(exc))
        return False
    dlg = QDialog()
    dlg.setWindowTitle("NONIVERUS · Ativação Privada")
    dlg.resize(680, 480)
    dlg.setStyleSheet("""
        QDialog {background:#101E32; color:#E8EDF7;}
        QLabel {color:#E8EDF7; font-size:13px;}
        QTextEdit {background:#1A2B43; color:#F2E7D3; border:1px solid #41536C;
          border-radius:8px; padding:8px; font-size:12px;}
        QPushButton {background:#C29B69; color:#101E32; border:0; border-radius:7px;
          padding:11px 18px; font-weight:600;}
    """)
    layout = QVBoxLayout(dlg)
    title = QLabel("NONIVERUS  /  POSTERTILE PRIVATE PREVIEW")
    title.setStyleSheet("font-size:17px; font-weight:700; color:#D7B77D;")
    layout.addWidget(title)
    info = QLabel("1. Copia o pedido e envia-o por WhatsApp ao responsável NONIVERUS.\n"
                  "2. Cola abaixo a licença assinada que receberes.\n"
                  "3. A licença só funciona neste computador. Não requer internet.")
    info.setWordWrap(True)
    layout.addWidget(info)
    req = QTextEdit()
    req.setReadOnly(True)
    req.setMaximumHeight(78)
    req.setPlainText(request)
    layout.addWidget(req)
    copy = QPushButton("COPIAR PEDIDO DE ATIVAÇÃO")
    copy.clicked.connect(lambda: QApplication.clipboard().setText(request))
    layout.addWidget(copy)
    layout.addWidget(QLabel("Licença assinada NONIVERUS"))
    text = QTextEdit()
    text.setPlaceholderText("NVPT1|…")
    text.setMaximumHeight(112)
    layout.addWidget(text)
    actions = QHBoxLayout()
    cancel = QPushButton("SAIR")
    activate = QPushButton("ATIVAR PREVIEW")
    actions.addWidget(cancel)
    actions.addWidget(activate)
    layout.addLayout(actions)
    cancel.clicked.connect(dlg.reject)
    def apply():
        try:
            install_license(text.toPlainText(), base)
        except Exception as exc:
            QMessageBox.warning(dlg, "Licença não aceite", str(exc))
            return
        dlg.accept()
    activate.clicked.connect(apply)
    return dlg.exec() == QDialog.Accepted and is_activated(base)
