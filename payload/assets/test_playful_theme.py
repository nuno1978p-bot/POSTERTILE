# -*- coding: utf-8 -*-
"""Regression checks for Playful Studio; no Qt runtime required."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PlayfulThemeTests(unittest.TestCase):
    def test_playful_is_supported_and_persisted(self):
        src = (ROOT / "main.py").read_text(encoding="utf-8")
        self.assertIn('"Playful Studio"', src)
        self.assertIn('self._settings.setValue("appearance/theme",theme)', src)

    def test_ui_theme_switcher_has_all_three_themes(self):
        ui = (ROOT / "ui/Main.qml").read_text(encoding="utf-8")
        self.assertGreaterEqual(ui.count('["Midnight Sapphire", "Pearl Titanium", "Playful Studio"]'), 2)
        self.assertIn('studio.setTheme(currentText)', ui)

    def test_sample_is_ui_only(self):
        ui = (ROOT / "ui/Main.qml").read_text(encoding="utf-8")
        self.assertIn('property bool playfulDemo: win.playful && studio.imageUrl.length === 0', ui)
        self.assertIn('visible: win.playfulDemo', ui)
        self.assertIn('studio.framedPreviewUrl', ui)
        self.assertNotIn('assets/playful/', (ROOT / "postertile_engine.py").read_text(encoding="utf-8"))

    def test_demo_assets(self):
        for name in ("astronaut_demo.png", "creative_helper.png", "playful_icon.png"):
            p = ROOT/"assets"/"playful"/name
            self.assertTrue(p.is_file())
            self.assertGreater(p.stat().st_size, 5000)

    def test_owner_preview_appids_unchanged(self):
        builder = (ROOT/"build_editions.py").read_text(encoding="utf-8-sig")
        self.assertIn("A21297EC-47C8-4A17-8CB9-DA95C70645A9", builder)
        self.assertIn("47FD65E8-338F-45CE-9F74-2DF0B0AB9C41", builder)
        self.assertIn('contents += UPDATE_INSTALLER_CODE.replace("__APPID__", appid)', builder)

    def test_version(self):
        for p in ("ui/Main.qml", "build_editions.py", "version_info.txt"):
            self.assertIn("0.9.1", (ROOT/p).read_text(encoding="utf-8-sig"))

if __name__ == "__main__":
    unittest.main()
