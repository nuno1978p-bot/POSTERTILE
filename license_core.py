# -*- coding: utf-8 -*-
"""NONIVERUS license wire format. Public data only; Ed25519 keys are external."""
import re
import secrets
import time

APP_ID = "NVPT1"
REQUEST_ID = "NVREQ1"
HEX_DEVICE = re.compile(r"^[a-f0-9]{64}$")
HEX_NONCE = re.compile(r"^[a-f0-9]{16}$")
HEX_LICENSE = re.compile(r"^[a-f0-9]{32}$")
HEX_SIGNATURE = re.compile(r"^[a-f0-9]{128}$")


def make_request(device_fingerprint: str):
    if not HEX_DEVICE.fullmatch(device_fingerprint):
        raise ValueError("Dispositivo inválido.")
    return f"{REQUEST_ID}|{device_fingerprint}|{secrets.token_hex(8)}"


def parse_request(request: str):
    value = request.strip()
    bits = value.split("|")
    if len(bits) != 3 or bits[0] != REQUEST_ID or not HEX_DEVICE.fullmatch(bits[1]) or not HEX_NONCE.fullmatch(bits[2]):
        raise ValueError("Pedido inválido: esperado NVREQ1|fingerprint|nonce.")
    return bits[1]


def unsigned_license(license_id: str, fingerprint: str, issued: int, expires: int):
    if not HEX_LICENSE.fullmatch(license_id) or not HEX_DEVICE.fullmatch(fingerprint):
        raise ValueError("Identificador ou dispositivo inválido.")
    issued, expires = int(issued), int(expires)
    if issued < 1_600_000_000 or expires < 0 or expires and expires <= issued:
        raise ValueError("Datas de emissão/expiração inválidas.")
    return f"{APP_ID}|{license_id}|{fingerprint}|preview|{issued}|{expires}"


def signed_license(private_key, request: str, days: int = 0, now: int = None):
    fingerprint = parse_request(request)
    days = int(days)
    if days < 0 or days > 3650:
        raise ValueError("Dias devem estar entre 0 e 3650.")
    now = int(time.time()) if now is None else int(now)
    expires = (now + days * 86400) if days else 0
    unsigned = unsigned_license(secrets.token_hex(16), fingerprint, now, expires)
    sig = private_key.sign(unsigned.encode("ascii")).hex()
    return unsigned + "|" + sig


def verify_license_python_for_tests(public_key, certificate: str, fingerprint: str, now: int):
    """Cryptographic test oracle; runtime Preview calls native Rust, never this."""
    from cryptography.exceptions import InvalidSignature
    parts = certificate.strip().split("|")
    if len(parts) != 7 or parts[0] != APP_ID or parts[3] != "preview":
        return False
    if not (HEX_LICENSE.fullmatch(parts[1]) and HEX_DEVICE.fullmatch(parts[2]) and HEX_SIGNATURE.fullmatch(parts[6])):
        return False
    if parts[2] != fingerprint or not parts[4].isdigit() or not parts[5].isdigit():
        return False
    issued, expires = int(parts[4]), int(parts[5])
    if issued > now + 300 or (expires and now > expires):
        return False
    try:
        public_key.verify(bytes.fromhex(parts[6]), "|".join(parts[:6]).encode("ascii"))
        return True
    except (InvalidSignature, ValueError):
        return False
