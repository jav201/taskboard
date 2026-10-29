"""The shared headless-browser helper of the HTML-report tests (batch 2026-10-29-batch-01).

`require_browser()` is the ONE guard: Playwright missing is a skip, except when
`TASKBOARD_REQUIRE_BROWSER=1`, where it is a FAILURE (this machine and the P4 run
set it, so a browser node can never pass by skipping there).

`open_page` attaches the collectors every browser node reads: console errors, page
errors, dialogs, and every request that is not the page itself. The request rule
(PDR PQ5): ignore `about:`, `blob:` and `data:`; count everything else — http(s),
ws(s), and any `file:` URL other than the page's own (`as_uri()`, hash stripped).
"""
from __future__ import annotations

import os
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pytest

TIMEOUT_MS = 10_000
IGNORED_SCHEMES = ("about:", "blob:", "data:")


def require_browser():
    """`playwright.sync_api`, or skip / fail per `TASKBOARD_REQUIRE_BROWSER`."""
    try:
        return pytest.importorskip("playwright.sync_api")
    except pytest.skip.Exception:
        if os.environ.get("TASKBOARD_REQUIRE_BROWSER") == "1":
            pytest.fail("playwright is not installed and TASKBOARD_REQUIRE_BROWSER=1")
        raise


@dataclass
class Opened:
    page: object
    own: str
    console_errors: list = field(default_factory=list)
    page_errors: list = field(default_factory=list)
    requests: list = field(default_factory=list)
    dialogs: list = field(default_factory=list)

    def problems(self) -> list:
        return self.console_errors + self.page_errors + self.requests + self.dialogs


def foreign(url: str, own: str) -> bool:
    if url.startswith(IGNORED_SCHEMES):
        return False
    return url.split("#")[0] != own


def new_context(browser, *, scheme: str = "dark", viewport=(1366, 900)):
    ctx = browser.new_context(viewport={"width": viewport[0], "height": viewport[1]},
                              color_scheme=scheme, accept_downloads=True)
    ctx.set_default_timeout(TIMEOUT_MS)
    ctx.set_default_navigation_timeout(TIMEOUT_MS)
    return ctx


def open_page(ctx, path: Path, *, hash: str = "", ready: str = "#tbody") -> Opened:
    own = Path(path).resolve().as_uri()
    page = ctx.new_page()
    o = Opened(page=page, own=own)
    page.on("console", lambda m: o.console_errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: o.page_errors.append(str(e)))
    page.on("request", lambda r: o.requests.append(r.url) if foreign(r.url, own) else None)
    page.on("websocket", lambda w: o.requests.append(w.url))

    def on_dialog(d):
        o.dialogs.append(d.message)
        d.dismiss()
    page.on("dialog", on_dialog)
    page.goto(own + (("#" + hash.lstrip("#")) if hash else ""))
    page.wait_for_selector(ready, state="attached")
    return o


def shown_ids(page) -> Counter:
    """The table's rows by task key, as a multiset."""
    return Counter(page.eval_on_selector_all("#tbody tr", "rs => rs.map(r => r.dataset.key)"))


def bar_ids(page) -> set:
    return set(page.eval_on_selector_all("#gantt .gbar", "bs => bs.map(b => b.dataset.key)"))


def controls_state(page) -> dict:
    """Every control's visible state, for comparing two pages."""
    return page.evaluate("""() => ({
        chips: [...document.querySelectorAll('nav button[aria-pressed]')]
            .map(b => [b.dataset.group, b.dataset.value, b.getAttribute('aria-pressed')]),
        boxes: [...document.querySelectorAll('#f-projects input[type=checkbox]')]
            .map(b => [b.dataset.key, b.checked]),
        inputs: ['f-from', 'f-to', 'f-q'].map(i => document.getElementById(i).value),
        count: document.getElementById('active-count').textContent,
        summary: document.getElementById('view-summary').textContent,
        sections: ['gantt', 'table', 'notes', 'milestones']
            .map(s => document.getElementById('s-' + s).hidden),
    })""")


def chip(page, group: str, value: str):
    return page.locator(f'nav button[data-group="{group}"][data-value="{value}"]')


def box(page, key: str):
    return page.locator(f'#f-projects input[type=checkbox][data-key="{key}"]')
