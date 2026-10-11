# -*- coding: utf-8 -*-
"""Offline tests: authority, signing, tampering, machine binding, build staging."""
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

import license_core as lc
import license_runtime as lr
import license_authority as la
import build_editions as be


class TestPreviewSecurity(unittest.TestCase):
    def setUp(self):
        self.key = Ed25519PrivateKey.generate()
        self.fp = "a" * 64
        self.now = 1_800_000_000
        self.request = "NVREQ1|" + self.fp + "|" + "f"*16

    def test_signed_license(self):
        signed=lc.signed_license(self.key,self.request,days=31,now=self.now)
        self.assertTrue(lc.verify_license_python_for_tests(self.key.public_key(),signed,self.fp,self.now))
        self.assertFalse(lc.verify_license_python_for_tests(self.key.public_key(),signed,"b"*64,self.now))
        self.assertFalse(lc.verify_license_python_for_tests(self.key.public_key(),signed,self.fp,self.now+32*86400))

    def test_tampered_certificate(self):
        s=lc.signed_license(self.key,self.request,days=1,now=self.now)
        changes=[
            s.replace("|preview|","|owner|"),
            s.replace("|preview|","|preview|",1).replace("|"+self.fp+"|","|"+"b"*64+"|"),
            s[:-1]+("a" if s[-1] != "a" else "b"),
            s.replace("|"+str(self.now)+"|","|"+str(self.now+1000)+"|"),
        ]
        for tampered in changes:
            self.assertFalse(lc.verify_license_python_for_tests(
                self.key.public_key(),tampered,self.fp,self.now),tampered)

    def test_wrong_signer(self):
        cert=lc.signed_license(self.key,self.request,now=self.now)
        self.assertFalse(lc.verify_license_python_for_tests(
            Ed25519PrivateKey.generate().public_key(),cert,self.fp,self.now))

    def test_no_expiration(self):
        cert=lc.signed_license(self.key,self.request,days=0,now=self.now)
        self.assertTrue(lc.verify_license_python_for_tests(
            self.key.public_key(),cert,self.fp,self.now+5*365*86400))

    def test_invalid_request(self):
        for request in ("", "NVREQ1|x", "NVREQ1|"+"a"*64+"|abc",
                        "NVPT1|"+"a"*64+"|"+"f"*16):
            with self.assertRaises(ValueError):
                lc.parse_request(request)

    def test_missing_native_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            cert=lc.signed_license(self.key,self.request,now=self.now)
            self.assertFalse(lr.validate_certificate(cert,t,fingerprint=self.fp,now=self.now))

    def test_authority_key_outside_project_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as root:
            with patch.dict(os.environ, {"LOCALAPPDATA":root}):
                path=la.init_key()
                self.assertTrue(path.is_file())
                self.assertNotIn(str(be.ROOT),str(path))
                self.assertEqual(la.public_key_path().stat().st_size,32)
                with self.assertRaises(FileExistsError):
                    la.init_key()
                cert=la.issue(self.request,days=7)
                pub=la.load_key().public_key()
                self.assertTrue(lc.verify_license_python_for_tests(
                    pub,cert,self.fp,int(time.time())))
                self.assertTrue((la.authority_dir()/"issued_licenses.jsonl").is_file())

    def test_separate_build_stages(self):
        for ed in ("owner","preview"):
            stage=be.prepare_stage(ed)
            self.assertEqual((stage/"edition_config.py").read_text().split("EDITION = ")[1].strip(),repr(ed))
            self.assertFalse((stage/"license_authority.py").exists())
            self.assertFalse((stage/"native_license").exists())
            self.assertFalse((stage/".git").exists())
            iss,_=be.make_installer_script(ed,be.APP_NAMES[ed])
            self.assertIn("AppId={{",iss.read_text('utf-8-sig'))
        self.assertNotEqual(be.APPIDS['owner'],be.APPIDS['preview'])


if __name__=="__main__":
    unittest.main()
