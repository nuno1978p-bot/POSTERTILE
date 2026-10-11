//! Native, fail-closed NONIVERUS Private Preview verification.
//! The public key is generated into ../public_key.bin at owner build time.
//! The secret key must NEVER be included in this crate or in any distributable.
use ed25519_dalek::{Signature, Verifier, VerifyingKey};
use std::os::raw::c_char;
use std::ffi::CStr;

const PUBLIC_KEY: &[u8; 32] = include_bytes!("../public_key.bin");

fn decode_hex(s: &str, expected_bytes: usize) -> Option<Vec<u8>> {
    if s.len() != expected_bytes * 2 || !s.is_ascii() { return None; }
    let mut out = Vec::with_capacity(expected_bytes);
    for pair in s.as_bytes().chunks_exact(2) {
        let digit = |b: u8| -> Option<u8> {
            match b {
                b'0'..=b'9' => Some(b - b'0'),
                b'a'..=b'f' => Some(b - b'a' + 10),
                _ => None,
            }
        };
        out.push((digit(pair[0])? << 4) | digit(pair[1])?);
    }
    Some(out)
}

fn verify_inner(raw: &[u8], device: &str, now: u64) -> bool {
    if raw.is_empty() || raw.len() > 2048 || !raw.is_ascii() { return false; }
    let text = match std::str::from_utf8(raw) {
        Ok(v) => v.trim(),
        Err(_) => return false,
    };
    let bits: Vec<&str> = text.split('|').collect();
    if bits.len() != 7 || bits[0] != "NVPT1" || bits[3] != "preview" { return false; }
    if decode_hex(bits[1], 16).is_none() || decode_hex(bits[2], 32).is_none()
        || decode_hex(device, 32).is_none() || bits[2] != device { return false; }
    if bits[4].is_empty() || bits[5].is_empty() ||
        !bits[4].bytes().all(|b| b.is_ascii_digit()) ||
        !bits[5].bytes().all(|b| b.is_ascii_digit()) { return false; }
    let issued: u64 = match bits[4].parse() { Ok(v) => v, Err(_) => return false };
    let expires: u64 = match bits[5].parse() { Ok(v) => v, Err(_) => return false };
    if issued < 1_600_000_000 || issued > now.saturating_add(300) { return false; }
    if expires != 0 && (expires <= issued || expires < now) { return false; }
    let sig_raw = match decode_hex(bits[6], 64) { Some(v) => v, None => return false };
    let sig: [u8; 64] = match sig_raw.try_into() { Ok(v) => v, Err(_) => return false };
    let signature = Signature::from_bytes(&sig);
    let vk = match VerifyingKey::from_bytes(PUBLIC_KEY) { Ok(v) => v, Err(_) => return false };
    let payload = bits[..6].join("|");
    vk.verify(payload.as_bytes(), &signature).is_ok()
}

#[no_mangle]
pub unsafe extern "C" fn nv_verify_license(
    cert: *const u8, cert_len: usize, fingerprint: *const c_char, now: u64
) -> i32 {
    // 0 valid; nonzero invalid. Fail closed on every parsing/runtime error.
    if cert.is_null() || fingerprint.is_null() || cert_len == 0 || cert_len > 2048 { return 1; }
    let raw = std::slice::from_raw_parts(cert, cert_len);
    let device = match CStr::from_ptr(fingerprint).to_str() { Ok(v) => v, Err(_) => return 2 };
    if verify_inner(raw, device, now) { 0 } else { 3 }
}
