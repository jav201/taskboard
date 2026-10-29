"""Screenshot + headless verification for the HTML-report prototype round.

Usage:  python prototypes/html_report/shot.py <file.html> <prefix>

Writes <prefix>-desktop-light.png, <prefix>-desktop-dark.png,
<prefix>-phone-light.png, <prefix>-phone-dark.png, and <prefix>-verify.json.

The JSON records, per viewport+theme: console errors, page errors, and every
request that was NOT served from the local file — a report that fetches a CDN
is a failed report. Exits 1 if any console/page error or external request is
found.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

VIEWPORTS = {
    "desktop": {"width": 1366, "height": 900},
    "phone": {"width": 390, "height": 844},
}
THEMES = ("light", "dark")


def verify_and_shoot(html: Path, prefix: Path) -> dict:
    results = {}
    problems = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp_name, vp in VIEWPORTS.items():
            for theme in THEMES:
                ctx = browser.new_context(viewport=vp,
                                          color_scheme=theme)  # type: ignore[arg-type]
                page = ctx.new_page()
                console, external, page_errors = [], [], []
                page.on("console", lambda m: console.append(m.text)
                        if m.type == "error" else None)
                page.on("pageerror", lambda e: page_errors.append(str(e)))
                page.on("request", lambda r: external.append(r.url)
                        if r.url[:7] not in ("file://", "data:") and
                        not r.url.startswith("about:") else None)
                page.goto(html.resolve().as_uri())
                page.wait_for_timeout(400)
                overflow = page.evaluate(
                    "document.documentElement.scrollWidth > "
                    "document.documentElement.clientWidth + 1")
                shot = f"{prefix}-{vp_name}-{theme}.png"
                page.screenshot(path=shot, full_page=True)
                results[f"{vp_name}-{theme}"] = {
                    "console_errors": console,
                    "page_errors": page_errors,
                    "external_requests": external,
                    "horizontal_overflow": overflow,
                    "height": page.evaluate("document.body.scrollHeight"),
                }
                problems += (len(console) + len(page_errors) +
                             len(external) + (1 if overflow else 0))
                ctx.close()
        browser.close()
    results["_ok"] = problems == 0
    Path(f"{prefix}-verify.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    return results


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    res = verify_and_shoot(Path(sys.argv[1]), Path(sys.argv[2]))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    sys.exit(0 if res["_ok"] else 1)
