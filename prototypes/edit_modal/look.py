"""THROWAWAY: rasterize captured SVGs to PNG (headless Chrome) so they can be LOOKED at.
    python prototypes/edit_modal/look.py <svg> [<svg> ...]   -> out/_look/<name>.png"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "out" / "_look"
OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1500, "height": 1000})
    for f in sys.argv[1:]:
        f = Path(f).resolve()
        pg.goto(f.as_uri())
        el = pg.query_selector("svg")
        el.screenshot(path=str(OUT / (f.stem + ".png")))
        print(OUT / (f.stem + ".png"))
    b.close()
