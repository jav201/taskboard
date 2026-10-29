"""The deck report, and board text shown never run in BOTH reports (batch 2026-10-29-batch-01,
increment 003: HLR-3105, HLR-3106, LLR-3105.1, LLR-3105.2, LLR-3106.1, LLR-3106.2, and
LLR-3101.3's import probe re-run over `report_deck`).

The deck is a server-rendered page: every board string is escaped by `report_deck` before it
reaches HTML or SVG text. Expected slides, titles and counts are the fixture's literals, typed
from `report_fixture.py`, never read back from the code under test. Browser nodes open the
files `report_html.write_reports` wrote (the call the `H` export makes) in headless Chromium
and count console errors, page errors, dialogs and foreign requests (`report_browser`).

One Chromium per module, a fresh context per test, a 10 s default timeout per action.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import pytest
import report_fixture as F
from report_browser import new_context, open_page, require_browser
from test_report_html import _imports, renderer_offences

from taskboard import report_deck, report_html, report_workspace
from taskboard.models import Board

PKG = Path(report_html.__file__).parent
ARCH = " · "

# (title, footer count) per project slide, in board-then-project order — typed from the fixture:
# Legacy site (archived project) and Someday ideas (no task) have no slide; Old campaign's only
# task is archived, so it reads "0 tasks · 1 archived".
SLIDES = [
    ("Move apartment", "5 tasks"),
    ("Taxes 2026", "2 tasks" + ARCH + "1 archived"),
    ("Docs", "1 task"),
    ("Inbox", "1 task"),
    ("Storefront relaunch", "11 tasks" + ARCH + "1 archived"),
    ("Docs", "3 tasks"),
    ("Old campaign", "0 tasks" + ARCH + "1 archived"),
    ("Video module 3", "6 tasks"),
    ("Community forum", "2 tasks"),
    (F.HOSTILE_NAME, "1 task"),
    ("Hidden qzP1", "1 task"),
]
N = 2 + len(SLIDES)
SLIDE_OF = {"Storefront relaunch": 6, "Video module 3": 9, "Community forum": 10,
            F.HOSTILE_NAME: 11, "Hidden qzP1": 12}   # 0-based
BAD_URLS = ["javascript:alert(1)", "data:text/html,<b>x</b>", "JAVASCRIPT:alert(2)",
            " javascript:alert(3)", "https://example.test/ok"]
SENTINEL = "window.__x = 'untouched';"
BREAKOUT_URL = 'https://x.example/"onmouseover="window.__x=1'
BREAKOUT_NAME = 'Forum" onmouseover="window.__x=5" x="'


def _d(project=None, lanes=None):
    return report_html.extract(lanes or F.lanes(), F.PEOPLE, F.MARKS, F.TODAY, project=project)


def slides_of(page: str) -> list:
    """(title, footer) per project slide, read from the emitted bytes."""
    out = []
    for sec in re.findall(r'<section class="slide" data-project=.*?</section>', page, re.S):
        name = re.search(r'<span class="pname">(.*?)</span>', sec).group(1)
        foot = re.search(r'<p class="foot">(.*?)</p>', sec).group(1)
        out.append((html.unescape(name), html.unescape(foot)))
    return out


def sections(page: str) -> int:
    return page.count('<section class="slide')


# ---- TC-3113 / TC-3104 (unit) ---------------------------------------------------------------

def test_TC_3113_one_slide_per_project(tmp_path):
    """TC-3113 (LLR-3105.1, D12, R1): a cover, an overview and one slide per non-archived
    project holding a task of any status, in board-then-project order, each printing its
    non-archived count and, when any, its archived count. The archived project and the
    task-less project get none; an all-archived project or Inbox reads `0 tasks · k
    archived`. The deck READS each task's status: edited in the dict, the count follows."""
    d = _d()
    page = report_deck.render(d)
    assert sections(page) == N == 13
    assert slides_of(page) == SLIDES
    assert ">Legacy site<" not in page and "Someday ideas" not in page
    assert f'<p class="scope">{html.escape(F.SCOPE_LINE)}</p>' in page
    path = report_html.write_reports(d, ("deck",), tmp_path / "reports", F.TODAY)[0]
    assert path.name == "deck-2026-10-29.html" and path.read_text(encoding="utf-8") == page

    one = report_deck.render(_d("client-a:prel"))
    assert sections(one) == 3 and slides_of(one) == [SLIDES[4]]
    assert '<p class="scope">Project Storefront relaunch on Client A</p>' in one
    gone = report_deck.render(_d("client-a:pold"))
    assert sections(gone) == 3 and slides_of(gone) == [("Old campaign", "0 tasks · 1 archived")]

    shelf = Board([], [F._t("ib1", None, "Shelved idea", "Done", "low", -9, -8, 8, archived=True)],
                  Path("rf-shelf-never-saved.json"), {}, F.PHASES)
    inbox = report_deck.render(_d(lanes=[("shelf", "Shelf", "pink", shelf)]))
    assert sections(inbox) == 3 and slides_of(inbox) == [("Inbox", "0 tasks · 1 archived")]
    empty = Board([], [], Path("rf-empty-never-saved.json"), {}, F.PHASES)
    assert sections(report_deck.render(_d(lanes=[("empty", "Empty", "pink", empty)]))) == 2

    edited = json.loads(json.dumps(d))
    for t in edited["tasks"]:
        if t["key"] == "personal:tmv3":
            t["status"] = "archived"
    assert slides_of(report_deck.render(edited))[0] == ("Move apartment", "4 tasks · 1 archived")


def test_TC_3104_the_deck_reads_the_dict_only():
    """TC-3104 re-run with `report_deck.py` added (LLR-3101.3, R7): the AST walk finds no
    package import in the deck but `report_html` (no dynamic import either), and the same
    dict renders to the same bytes."""
    assert renderer_offences(PKG / "report_deck.py") == []
    assert renderer_offences(PKG / "report_workspace.py") == []
    assert "taskboard.report_html" in {m for m, _, _ in _imports(PKG / "report_deck.py")}
    assert report_deck.render(_d()) == report_deck.render(_d())


# ---- browser ----------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def browser():
    api = require_browser()
    pw = api.sync_playwright().start()
    b = pw.chromium.launch()
    yield b
    b.close()
    pw.stop()


@pytest.fixture(scope="module")
def data():
    return _d()


@pytest.fixture(scope="module")
def both(tmp_path_factory, data):
    """`H a`'s writer call: the workspace and the deck from one dict."""
    folder = tmp_path_factory.mktemp("reports")
    ws, deck = report_html.write_reports(data, ("workspace", "deck"), folder, F.TODAY)
    return ws, deck


@pytest.fixture
def ctx(browser):
    c = new_context(browser)
    yield c
    c.close()


def open_deck(ctx, path):
    return open_page(ctx, path, ready="#cnt")


def counter(page) -> str:
    return page.text_content("#cnt")


def shown(page) -> list:
    return page.evaluate("[...document.querySelectorAll('.slide')]"
                         ".map((s, i) => s.getClientRects().length ? i : -1).filter(i => i >= 0)")


def goto_slide(page, i: int):
    page.keyboard.press("Home")
    for _ in range(i):
        page.keyboard.press("ArrowRight")
    assert counter(page) == f"{i + 1} / {N}"


# ---- TC-3114 ----------------------------------------------------------------------------------

def test_TC_3114_keys_page_and_print_splits(ctx, both):
    """TC-3114 (LLR-3105.2): real key presses page the deck — End, ArrowRight held at the
    last slide, Home, PageDown/PageUp, ArrowLeft held at the first — and the on-screen
    buttons do the same; the keys do nothing while focus is in a text field, nor with Ctrl,
    Alt or Meta held (those combinations stay the browser's). Printed, every
    slide shows with a page break after it, in the light palette, one slide per PDF page."""
    o = open_deck(ctx, both[1])
    page = o.page
    assert counter(page) == f"1 / {N}" and shown(page) == [0]
    steps = [("End", N), ("ArrowRight", N), ("Home", 1), ("PageDown", 2), ("ArrowRight", 3),
             ("PageUp", 2), ("ArrowLeft", 1), ("ArrowLeft", 1)]
    for key, n in steps:
        page.keyboard.press(key)
        assert counter(page) == f"{n} / {N}", key
        assert shown(page) == [n - 1], key
    assert page.is_disabled("#prev") and page.is_enabled("#next")
    page.click("#next")
    assert counter(page) == f"2 / {N}"
    page.click("#prev")
    assert counter(page) == f"1 / {N}"
    for tag in ("input", "textarea"):
        page.evaluate("tag => { const e = document.createElement(tag); e.id = 'typing';"
                      " document.body.prepend(e); e.focus(); }", tag)
        for key in ("End", "ArrowRight", "PageDown"):
            page.keyboard.press(key)
            assert counter(page) == f"1 / {N}", (tag, key)
        page.evaluate("document.getElementById('typing').remove()")
    for combo in ("Control+End", "Alt+PageDown", "Meta+ArrowRight", "Control+ArrowRight"):
        page.keyboard.press(combo)
        assert counter(page) == f"1 / {N}", combo
    page.keyboard.press("End")
    assert counter(page) == f"{N} / {N}"

    page.emulate_media(media="print", color_scheme="dark")
    st = page.evaluate("""() => {
        const ss = [...document.querySelectorAll('.slide')];
        return {shown: ss.filter(s => getComputedStyle(s).display !== 'none').length,
                breaks: ss.filter(s => getComputedStyle(s).breakAfter === 'page').length,
                nav: getComputedStyle(document.querySelector('.bar-nav')).display,
                bg: getComputedStyle(document.body).backgroundColor,
                ink: getComputedStyle(document.querySelector('svg text.t')).fill};
    }""")
    assert st == {"shown": N, "breaks": N, "nav": "none", "bg": "rgb(255, 255, 255)",
                  "ink": "rgb(31, 35, 40)"}
    pdf = page.pdf(format="A4", print_background=True)
    assert len(re.findall(rb"/Type\s*/Page[^s]", pdf)) == N
    assert o.problems() == []


# ---- TC-3116 ----------------------------------------------------------------------------------

LINKS = """() => [...document.querySelectorAll('a[href]')]
    .map(a => [a.getAttribute('href'), a.getAttribute('rel'), a.getAttribute('target')])"""


def test_TC_3116_offline_themes_and_phone_width(browser, both, data, tmp_path):
    """TC-3116 (LLR-3106.2, SI1): both files fetch nothing; at 390x844 in light and dark every
    deck slide lays out with no horizontal page scroll (the 120-character and the Unicode
    titles on their slide, drawn by the narrow chart), and the two schemes paint different
    backgrounds. Links: a dict EDITED to hold `javascript:`/`data:` URLs (what reaches a
    renderer if the extraction's filter ever slips) still yields no anchor but http(s) in
    either report — the deck's server check and the workspace's `safeHref` — and every task
    anchor carries `rel="noopener noreferrer"`."""
    backgrounds = {}
    for scheme in ("light", "dark"):
        ctx = new_context(browser, scheme=scheme, viewport=(390, 844))
        try:
            o = open_deck(ctx, both[1])
            page = o.page
            for i in range(N):
                assert page.evaluate("document.documentElement.scrollWidth <= "
                                     "document.documentElement.clientWidth"), (scheme, i)
                page.keyboard.press("ArrowRight")
            goto_slide(page, SLIDE_OF["Video module 3"])
            texts = page.eval_on_selector_all(".slide.on svg text.t", "ts => ts.map(t => t.textContent)")
            assert F.UNICODE_TITLE in texts and F.LONG_TITLE[:63] + "…" in texts
            assert page.eval_on_selector_all(
                ".slide.on svg.g", "gs => gs.filter(g => g.getClientRects().length)"
                ".map(g => g.classList.contains('g-narrow'))") == [True]
            backgrounds[scheme] = page.evaluate("getComputedStyle(document.body).backgroundColor")
            assert o.problems() == []
        finally:
            ctx.close()
    assert backgrounds["light"] != backgrounds["dark"]

    edited = json.loads(json.dumps(data))
    for t in edited["tasks"]:
        if t["key"] == "client-a:tst8":
            t["urls"] = list(BAD_URLS)
    deck_html = report_deck.render(edited)
    assert "javascript:" not in deck_html.lower() and "data:text" not in deck_html
    (tmp_path / "deck.html").write_text(deck_html, encoding="utf-8")
    (tmp_path / "ws.html").write_text(report_workspace.render(edited), encoding="utf-8")
    ctx = new_context(browser)
    try:
        o = open_deck(ctx, tmp_path / "deck.html")
        links = o.page.evaluate(LINKS)
        w = open_page(ctx, tmp_path / "ws.html")
        w.page.click('#tbody tr[data-key="client-a:tst8"]')
        assert w.page.is_visible("#card")
        wlinks = w.page.evaluate(LINKS)
        assert o.problems() == [] and w.problems() == []
    finally:
        ctx.close()
    for found in (links, wlinks):
        assert ["https://example.test/ok", "noopener noreferrer", "_blank"] in found
        assert [h for h, _, _ in found if not re.match(r"https?://", h, re.I)] == []
        assert {r for _, r, _ in found} == {"noopener noreferrer"}


# ---- finished work is never late (requirement amendment, increment 003) ----------------------

def test_finished_work_is_never_late_in_either_report(ctx, both):
    """A done task 30 days past its due date (`Stakeholder interviews`) reads the plain
    distance `-30d`, never `30d overdue`: in the workspace's task card and on the deck's
    gantt row. Both read the dict's `due_word`."""
    w = open_page(ctx, both[0])
    w.page.click('#tbody tr[data-key="client-a:tst1"]')
    fields = w.page.eval_on_selector_all("#c-fields dt, #c-fields dd", "es => es.map(e => e.textContent)")
    assert fields[fields.index("Due") + 1] == "2026-09-29 · -30d"
    o = open_deck(ctx, both[1])
    goto_slide(o.page, SLIDE_OF["Storefront relaunch"])
    texts = o.page.eval_on_selector_all(".slide.on svg.g-wide text", "ts => ts.map(t => t.textContent)")
    assert texts[texts.index("✓ Stakeholder interviews") + 1] == "Done · -30d · 20d in phase"
    assert w.problems() == [] and o.problems() == []


# ---- AT-3106 ----------------------------------------------------------------------------------

def hostile_pair(folder: Path) -> tuple[Path, Path]:
    """`H a` over the hostile fixture plus SC1's attribute breakouts: a task URL and a project
    name that close a quoted attribute and open `onmouseover=`."""
    lanes = F.lanes()
    client, course = lanes[1][3], lanes[2][3]
    next(t for t in client.tasks if t.id == "tst8").urls.append(BREAKOUT_URL)
    next(p for p in course.projects if p.id == "pcom").name = BREAKOUT_NAME
    d = report_html.extract(lanes, F.PEOPLE, F.MARKS, F.TODAY)
    ws, deck = report_html.write_reports(d, ("workspace", "deck"), folder, F.TODAY)
    return ws, deck


def test_AT_3106_board_text_is_escaped_in_both_reports(browser, tmp_path):
    """AT-3106 (HLR-3106): both reports written from the hostile fixture — a `<script>` title,
    a note closing `</script>`, an `<img onerror>` person, project, board, class and phase
    name, tasks holding `javascript:`/`data:` URLs, and (SC1) a URL and a project name that
    break out of a quoted attribute into `onmouseover=` — show that text as literal text and
    run nothing: 0 dialogs while loaded, paged, opened and hovered, the `window.__x` sentinel
    untouched, only the template's own `<script>` elements, 0 injected elements, 0 elements
    carrying `onmouseover`, 0 anchors but http(s), and none of the hostile markup in the bytes."""
    ws, deck = hostile_pair(tmp_path)
    for path, scripts in ((ws, 2), (deck, 1)):
        raw = path.read_text(encoding="utf-8")
        assert raw.count("<script") == scripts, path.name
        for bad in ("<script>alert(1)", "javascript:alert(1)", "data:text/html,<b>x</b>",
                    "<img src=x", "</script><b>", '"onmouseover="', '" onmouseover="'):
            assert bad not in raw, (path.name, bad)

    ctx = new_context(browser)
    ctx.add_init_script(SENTINEL)
    try:
        o = open_deck(ctx, deck)
        page = o.page
        for _ in range(N):
            page.keyboard.press("ArrowRight")
        assert counter(page) == f"{N} / {N}"
        page.keyboard.press("Home")
        assert page.text_content(".slide.on .scope") == F.SCOPE_LINE
        cells = page.eval_on_selector_all(".slide.on tbody td:first-child", "ts => ts.map(t => t.textContent)")
        assert F.SIDE_BOARD_NAME in cells
        assert F.HOSTILE_MARK in page.text_content(".slide.on .legend")
        goto_slide(page, SLIDE_OF["Storefront relaunch"])
        titles = page.eval_on_selector_all(".slide.on svg.g-wide text.t", "ts => ts.map(t => t.textContent)")
        assert F.HOSTILE_TITLE in titles
        note = page.locator(".slide.on .note", has_text="alert(1)")
        assert note.locator(".nt").text_content() == F.HOSTILE_TITLE and note.is_visible()
        assert "@" + F.HOSTILE_PERSON in note.text_content()
        assert '</script><b>x</b> & "q"' in note.text_content()
        link = note.locator("a", has_text="onmouseover")
        assert link.get_attribute("href") == BREAKOUT_URL
        link.hover()
        goto_slide(page, SLIDE_OF["Community forum"])
        assert page.text_content(".slide.on .pname") == BREAKOUT_NAME
        page.hover(".slide.on .pname")
        goto_slide(page, SLIDE_OF[F.HOSTILE_NAME])
        assert page.text_content(".slide.on .pname") == F.HOSTILE_NAME
        goto_slide(page, SLIDE_OF["Hidden qzP1"])
        meta = page.eval_on_selector_all(".slide.on svg.g-wide tspan", "ts => ts.map(t => t.textContent)")
        assert "◆ " + F.HOSTILE_MARK in meta
        legend = page.text_content(".slide.on .legend")
        assert F.HOSTILE_PHASE in legend and F.HOSTILE_MARK in legend
        deck_state = page.evaluate(INERT)

        w = open_page(ctx, ws)
        wp = w.page
        assert wp.text_content('#tbody tr[data-key="client-a:tst8"] td:first-child') == F.HOSTILE_TITLE
        assert wp.text_content("#scope-line") == F.SCOPE_LINE
        wp.click('#tbody tr[data-key="client-a:tst8"]')
        assert "@" + F.HOSTILE_PERSON in wp.text_content("#c-notes")
        wlink = wp.locator("#c-urls a", has_text="onmouseover")
        assert wlink.get_attribute("href") == BREAKOUT_URL
        wlink.hover()
        assert F.HOSTILE_NAME in wp.text_content("#f-projects")
        assert BREAKOUT_NAME in wp.text_content("#f-projects")
        assert F.HOSTILE_MARK in wp.text_content("nav")
        ws_state = wp.evaluate(INERT)
        assert o.problems() == [] and w.problems() == []
    finally:
        ctx.close()
    clean = {"x": "untouched", "injected": 0, "hover": 0, "bad_links": 0}
    assert deck_state == dict(clean, scripts=1)
    assert ws_state == dict(clean, scripts=2)


INERT = """() => ({
    x: window.__x,
    scripts: document.scripts.length,
    injected: document.querySelectorAll('img, iframe, object, embed, b, svg script').length,
    hover: document.querySelectorAll('[onmouseover]').length,
    bad_links: [...document.querySelectorAll('a[href]')]
        .filter(a => !/^https?:\\/\\//i.test(a.getAttribute('href'))).length,
})"""
