from __future__ import annotations

import json
from pathlib import Path
import shutil

from inneros_act3.judge_console import VERIFIED_RECEIPT, WEB_ROOT, _assert_no_secret_material


def build(destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    for asset in ("styles.css", "final.css", "app.js"):
        shutil.copy2(WEB_ROOT / asset, destination / asset)
    _assert_no_secret_material(VERIFIED_RECEIPT)
    data = "window.INNEROS_STATIC_REPLAY = " + json.dumps(VERIFIED_RECEIPT, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (destination / "replay-data.js").write_text(data, encoding="utf-8")
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    html = html.replace('href="assets/styles.css"', 'href="styles.css"')
    html = html.replace('href="assets/final.css"', 'href="final.css"')
    html = html.replace('<script src="assets/app.js"></script>', '<script src="replay-data.js"></script>\n  <script src="app.js"></script>')
    (destination / "index.html").write_text(html, encoding="utf-8")
    (destination / ".nojekyll").write_text("", encoding="utf-8")
    return destination


if __name__ == "__main__":
    build(Path("_site"))
