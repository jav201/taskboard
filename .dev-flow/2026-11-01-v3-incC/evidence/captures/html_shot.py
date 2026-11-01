import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
d = Path(sys.argv[1]).resolve()
page_file = next(d.glob("_html/workspace-*.html"))
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 800})
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(page_file.as_uri())
    pg.wait_for_timeout(500)
    loc = pg.get_by_text("ask the vendor for the store list").first
    loc.scroll_into_view_if_needed()
    pg.screenshot(path=str(d / "html-workspace.png"))
    print("visible:", loc.is_visible(), "console errors:", len(errs), errs)
    b.close()
