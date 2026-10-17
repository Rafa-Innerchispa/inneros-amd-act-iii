from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.build_static_demo import build


class StaticDemoTests(unittest.TestCase):
    def test_static_build_is_explicit_replay_and_self_contained(self):
        with tempfile.TemporaryDirectory() as raw:
            destination = build(Path(raw))
            html = (destination / "index.html").read_text(encoding="utf-8")
            data = (destination / "replay-data.js").read_text(encoding="utf-8")
            self.assertIn("Governed AI Operations on AMD", html)
            self.assertIn('src="replay-data.js"', html)
            self.assertIn('src="app.js"', html)
            self.assertNotIn('/assets/', html)
            self.assertIn("LIVE_VERIFIED_REPLAY", data)
            self.assertNotIn('"api_key"', data.lower())
            self.assertTrue((destination / "styles.css").is_file())
            self.assertTrue((destination / "final.css").is_file())


if __name__ == "__main__":
    unittest.main()
