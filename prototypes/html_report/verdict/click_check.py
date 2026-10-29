"""Click-through for the verdict page: fills fields, clicks «Exportar respuestas»,
asserts the label flips to «Copiado ✓» and that no page errors occur."""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HTML = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else \
    Path(__file__).resolve().parent.parent / "html-report-round.html"


def main() -> None:
    page_errors: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 1366, "height": 900},
            color_scheme="light",
            permissions=["clipboard-read", "clipboard-write"],
        )
        page = ctx.new_page()
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.goto(HTML.as_uri())
        page.check("#choose-b")
        page.check("#choose-general")
        page.fill("#obj-b", "objeción de prueba")
        page.fill("#notes", "nota de prueba")
        page.click("#export")
        page.wait_for_timeout(300)
        label = page.text_content("#export")
        if label != "Copiado ✓":
            raise SystemExit(f"FAIL: label after click = {label!r}")
        clip = page.evaluate(
            "() => navigator.clipboard.readText().catch(() => null)")
        page.wait_for_timeout(2100)
        label2 = page.text_content("#export")
        browser.close()
    if page_errors:
        raise SystemExit(f"FAIL: page errors: {page_errors}")
    if not clip or "Variante B: ELEGIDA" not in clip or '"variant": "b"' not in clip:
        raise SystemExit("FAIL: clipboard content missing expected text/JSON")
    if label2 != "Exportar respuestas":
        raise SystemExit(f"FAIL: label did not revert: {label2!r}")
    print("OK: label='Copiado', clipboard has text+JSON, no page errors, "
          "label reverted")


if __name__ == "__main__":
    main()
