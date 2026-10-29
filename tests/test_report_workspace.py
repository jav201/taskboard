"""The interactive workspace report, driven in headless Chromium (batch 2026-10-29-batch-01,
increment 001: HLR-3102, LLR-3102.1..3, LLR-3106.2's workspace arm, LLR-3101.1's status;
increment 002: HLR-3103, HLR-3104, LLR-3103.1..3, LLR-3104.1 — export this view).

Black-box: the page is written by `report_html.write_reports` (the call the `H` export
makes), opened from disk, and driven by clicks, key presses and typed values; the
assertions read the rows, bars and cards the page shows. Expected sets come from the
fixture's literals or from the truth table of LLR-3102.2 applied in Python to the
extraction — never from the page. Every page also counts console errors, page errors,
dialogs and foreign requests (`report_browser`), which must stay at zero.

One Chromium per module, a fresh context per test, a 10 s default timeout per action.
"""
from __future__ import annotations

import csv
import io
import json
import re
from collections import Counter
from datetime import date

import pytest
import report_fixture as F
from report_browser import (bar_ids, box, chip, controls_state, new_context, open_page,
                            require_browser, shown_ids)

from taskboard import report_html, report_workspace

DEFAULT_STATUS = ("open", "late", "done")


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
    return report_html.extract(F.lanes(), F.PEOPLE, F.MARKS, F.TODAY)


@pytest.fixture(scope="module")
def page_file(tmp_path_factory, data):
    folder = tmp_path_factory.mktemp("reports")
    return report_html.write_reports(data, ("workspace",), folder, F.TODAY)[0]


@pytest.fixture
def ctx(browser):
    c = new_context(browser)
    yield c
    c.close()


def expected(d, p=None, s=DEFAULT_STATUS, u=(), m=(), frm="", to="", q=""):
    """LLR-3102.2's truth table, applied to the extraction in Python."""
    names = {x["key"]: x["name"] for x in d["projects"]}
    out = set()
    for t in d["tasks"]:
        if p is not None and t["project"] not in p:
            continue
        if t["status"] not in s:
            continue
        if u and not set(t["mentions"]) & set(u):
            continue
        if m and t["mark"] not in m:
            continue
        if frm or to:
            a, b = t["start"] or t["due"], t["due"] or t["start"]
            if (frm and to and frm > to) or a is None:
                continue
            lo, hi = min(a, b), max(a, b)
            if (to and lo > to) or (frm and hi < frm):
                continue
        if q and q.lower() not in f'{t["title"]} {t["notes_text"]} {names[t["project"]]}'.lower():
            continue
        out.add(t["key"])
    return out


def sections_ids(page) -> dict:
    return page.evaluate("""() => ({
        notes: [...document.querySelectorAll('#notes-list li')].map(e => e.dataset.key),
        milestones: [...document.querySelectorAll('#ms-list li')].map(e => e.dataset.key),
    })""")


def assert_sections_follow(page, d, keep: set):
    by = {t["key"]: t for t in d["tasks"]}
    assert set(shown_ids(page)) == keep and sum(shown_ids(page).values()) == len(keep)
    assert bar_ids(page) == {k for k in keep if by[k]["start"] or by[k]["due"]}
    got = sections_ids(page)
    assert set(got["notes"]) == {k for k in keep if by[k]["notes_html"]}
    assert set(got["milestones"]) == {k for k in keep if by[k]["milestone"]}


def count(page) -> str:
    return page.text_content("#active-count")


def open_projects(page):
    if not page.eval_on_selector("#f-projects", "e => e.open"):
        page.click("#f-projects-sum")


# ---- AT-3102 -----------------------------------------------------------------------------

def test_AT_3102_filters_and_the_hash_round_trip(ctx, page_file, data):
    """AT-3102 (HLR-3102): each of the five filter kinds, driven by clicks and typing,
    narrows the table, the gantt, the notes and the milestones to exactly the truth
    table's set; the count names the active filters; the view's URL, opened in a fresh
    page, shows the same tasks with the same control states (the unlisted board's
    `#3:` key included); Reset brings the default view back and clears the hash."""
    o = open_page(ctx, page_file)
    page = o.page
    assert set(shown_ids(page)) == F.DEFAULT_SHOWN and count(page) == "0 filters active"
    assert page.evaluate("location.hash") == ""

    open_projects(page)
    page.click("#p-none")
    assert shown_ids(page) == {} and page.is_visible("#tempty")
    box(page, "personal:ptax").check()
    box(page, "#3:pside").check()
    assert set(shown_ids(page)) == F.TAX_OR_SIDE == expected(data, p={"personal:ptax", "#3:pside"})
    assert_sections_follow(page, data, F.TAX_OR_SIDE)
    assert count(page) == "1 filter active"
    page.click("#reset")

    chip(page, "status", "open").click()
    chip(page, "status", "done").click()
    assert set(shown_ids(page)) == F.LATE == expected(data, s=("late",))
    assert_sections_follow(page, data, F.LATE)
    page.click("#reset")

    chip(page, "people", "ana.ruiz").click()
    chip(page, "people", "luis.prado").click()
    assert set(shown_ids(page)) == F.ANA_OR_LUIS == expected(data, u=("ana.ruiz", "luis.prado"))
    page.click("#reset")

    chip(page, "marks", "launch").click()
    chip(page, "marks", "billing").click()
    assert set(shown_ids(page)) == F.LAUNCH_OR_BILLING == expected(data, m=("launch", "billing"))
    assert_sections_follow(page, data, F.LAUNCH_OR_BILLING)
    page.click("#reset")

    page.fill("#f-from", "2026-10-30")
    page.fill("#f-to", "2026-11-02")
    want = expected(data, frm="2026-10-30", to="2026-11-02")
    assert set(shown_ids(page)) == want and "personal:tin1" not in want
    assert_sections_follow(page, data, want)
    page.click("#reset")

    page.fill("#f-q", "faq")
    assert set(shown_ids(page)) == F.FAQ == expected(data, q="faq")
    page.click("#reset")

    # a combined view, then its URL in a fresh page
    open_projects(page)
    page.click("#p-none")
    for k in ("#3:pside", "course:pvid", "client-a:pdocs"):
        box(page, k).check()
    chip(page, "status", "archived").click()
    page.fill("#f-from", "2026-10-25")
    chip(page, "sections", "notes").click()
    chip(page, "zoom", "week").click()
    want = expected(data, p={"#3:pside", "course:pvid", "client-a:pdocs"},
                    s=("open", "late", "done", "archived"), frm="2026-10-25")
    assert set(shown_ids(page)) == want and "#3:tqzK1" in want
    assert count(page) == "3 filters active"
    assert page.is_hidden("#s-notes")
    h = page.evaluate("location.hash")
    assert h.startswith("#v=1&") and "%233%3Apside" in h
    before = controls_state(page)

    fresh = open_page(ctx, page_file, hash=h)
    assert shown_ids(fresh.page) == shown_ids(page)
    assert controls_state(fresh.page) == before
    assert fresh.page.evaluate("location.hash") == h

    fresh.page.click("#reset")
    assert set(shown_ids(fresh.page)) == F.DEFAULT_SHOWN
    assert fresh.page.evaluate("location.hash") == "" and count(fresh.page) == "0 filters active"
    assert o.problems() == [] and fresh.problems() == []


# ---- TC-3105 -----------------------------------------------------------------------------

def _tab_order(page, n: int) -> list:
    seen = []
    for _ in range(n * 4):
        page.keyboard.press("Tab")
        d = page.evaluate("""() => { const e = document.activeElement;
            return [e.tagName, e.dataset.group ? e.dataset.group + ':' + e.dataset.value
                                               : (e.dataset.key || e.id)]; }""")
        if not seen or seen[-1] != d:
            seen.append(d)
        if len(seen) == n:
            break
    return seen


def test_TC_3105_the_bar_is_native_and_counted(ctx, page_file):
    """TC-3105 (LLR-3102.1, PDR C10/C12): Tab from the top of the page reaches exactly the
    hand-enumerated controls, in order (each a native button / input / summary); every
    chip's `aria-pressed` is its filter state; a pressed chip differs by more than hue
    (a check mark and a heavier border); the count follows five actions; the header
    states the scope."""
    o = open_page(ctx, page_file)
    page = o.page
    assert page.text_content("#scope-line") == F.SCOPE_LINE
    page.evaluate("document.getElementById('f-projects').open = true")
    want = ([["BUTTON", "reset"], ["SUMMARY", "f-projects-sum"], ["BUTTON", "p-all"],
             ["BUTTON", "p-none"]]
            + [["INPUT", k] for k in F.PROJECT_KEYS]
            + [["BUTTON", f"status:{s}"] for s in ("open", "late", "done", "archived")]
            + [["BUTTON", f"people:{p}"] for p in F.PEOPLE_IDS]
            + [["BUTTON", f"marks:{m}"] for m in F.CLASS_KEYS]
            + [["INPUT", "f-from"], ["INPUT", "f-to"], ["INPUT", "f-q"]]
            + [["BUTTON", f"sections:{s}"] for s in ("gantt", "table", "notes", "milestones")]
            + [["BUTTON", f"zoom:{z}"] for z in ("fit", "day", "week", "month")]
            + [["BUTTON", "print"], ["BUTTON", "dl-view"], ["BUTTON", "dl-csv"],
               ["BUTTON", "dl-json"]])
    assert len(want) == 45
    assert _tab_order(page, len(want)) == want

    def pressed():
        return {(g, v): p == "true" for g, v, p in controls_state(page)["chips"]}
    start = pressed()
    assert {k for k, on in start.items() if on} == {
        ("status", "open"), ("status", "late"), ("status", "done"), ("zoom", "fit"),
        ("sections", "gantt"), ("sections", "table"), ("sections", "notes"),
        ("sections", "milestones")}

    on = chip(page, "status", "open")
    off = chip(page, "status", "archived")
    before_on = on.evaluate("e => getComputedStyle(e, '::before').content")
    before_off = off.evaluate("e => getComputedStyle(e, '::before').content")
    assert "✓" in before_on and "✓" not in before_off
    width = "e => getComputedStyle(e).borderTopWidth"
    assert on.evaluate(width) != off.evaluate(width)

    open_projects(page)
    box(page, "personal:pmove").uncheck()
    assert count(page) == "1 filter active"
    assert page.text_content("#f-projects-sum") == "Projects 12/13"
    on.click()
    assert count(page) == "2 filters active" and pressed()[("status", "open")] is False
    chip(page, "people", "carmen.vega").click()
    assert count(page) == "3 filters active" and pressed()[("people", "carmen.vega")] is True
    chip(page, "marks", "delivery").click()
    assert count(page) == "4 filters active"
    page.fill("#f-q", "module")
    assert count(page) == "5 filters active"
    page.fill("#f-to", "2026-12-01")
    assert count(page) == "6 filters active"
    chip(page, "sections", "gantt").click()
    chip(page, "zoom", "day").click()
    assert count(page) == "6 filters active"           # sections and zoom are display
    assert page.text_content("#view-summary").startswith("Projects 12/13: Taxes 2026")
    assert o.problems() == []


# ---- TC-3106 -----------------------------------------------------------------------------

def _projects(page):
    open_projects(page)
    page.click("#p-none")
    box(page, "personal:ptax").check()
    box(page, "#3:pside").check()


def _status(page):
    chip(page, "status", "open").click()
    chip(page, "status", "done").click()


def _people(page):
    chip(page, "people", "ana.ruiz").click()
    chip(page, "people", "luis.prado").click()


def _classes(page):
    chip(page, "marks", "launch").click()
    chip(page, "marks", "billing").click()


def _dates(page):
    page.fill("#f-from", "2026-10-31")
    page.fill("#f-to", "2026-11-01")


def _search(page):
    page.fill("#f-q", "faq")


TRUTH_ARMS = {
    "projects": (_projects, dict(p={"personal:ptax", "#3:pside"}), F.TAX_OR_SIDE),
    "status": (_status, dict(s=("late",)), F.LATE),
    "people": (_people, dict(u=("ana.ruiz", "luis.prado")), F.ANA_OR_LUIS),
    "classes": (_classes, dict(m=("launch", "billing")), F.LAUNCH_OR_BILLING),
    # DQ5: every dated open span that touches Oct 31..Nov 1, listed by hand from the fixture;
    # to == mv4's start (Nov 1) and from == mv3's due (Oct 31): both shown
    "dates": (_dates, dict(frm="2026-10-31", to="2026-11-01"),
              {"personal:tmv3", "personal:tmv4", "personal:ttx1", "client-a:tsp1",
               "client-a:tst2", "client-a:tst8", "client-a:tst10", "course:tvd3",
               "course:tvd5", "course:tvd6"}),
    "search": (_search, dict(q="faq"), F.FAQ),
}


@pytest.mark.parametrize("arm", list(TRUTH_ARMS))
def test_TC_3106_filters_follow_the_truth_table(ctx, page_file, data, arm):
    """TC-3106 (LLR-3102.2): one arm per row of the truth table; the shown set equals the
    table's rule applied in Python, and equals the arm's literal task set (the dates arm:
    a span touching `to` with its start and `from` with its due both show)."""
    assert len(TRUTH_ARMS) == 6
    act, rule, literal = TRUTH_ARMS[arm]
    o = open_page(ctx, page_file)
    act(o.page)
    got = set(shown_ids(o.page))
    assert got == expected(data, **rule)
    assert got == literal
    assert count(o.page) == "1 filter active"
    assert o.problems() == []


def test_TC_3106_the_edges_of_the_table(ctx, page_file, data):
    """TC-3106's boundary arms: every status chip off shows nothing and still counts the
    filter; `from` after `to` shows nothing; a lone `from` hides every undated task."""
    o = open_page(ctx, page_file)
    page = o.page
    for s in DEFAULT_STATUS:
        chip(page, "status", s).click()
    assert shown_ids(page) == {} and count(page) == "1 filter active"
    assert page.is_visible("#tempty")
    page.click("#reset")
    page.fill("#f-from", "2026-11-05")
    page.fill("#f-to", "2026-11-01")
    assert shown_ids(page) == {} and count(page) == "1 filter active"
    page.click("#reset")
    page.fill("#f-from", "2026-10-01")
    got = set(shown_ids(page))
    assert got == expected(data, frm="2026-10-01")
    assert not {"personal:tin1", "client-a:tst12", "course:tcm1"} & got
    assert o.problems() == []


# ---- TC-3107 -----------------------------------------------------------------------------

HOSTILE_HASH = "v=1&p=<img src=x onerror=alert(1)>&s=bogus&q=%3Cb%3Ex%3C%2Fb%3E"


def test_TC_3107_a_hostile_hash_is_dropped(ctx, page_file, data):
    """TC-3107 (LLR-3102.3): a hash carrying markup and unknown values runs nothing,
    creates no element and moves no control: the unknown `p` and `s` values are dropped
    (the view stays the default), and `q` lands only as the search box's text."""
    clean = open_page(ctx, page_file)
    default = controls_state(clean.page)
    o = open_page(ctx, page_file, hash=HOSTILE_HASH)
    page = o.page
    assert o.dialogs == [] and page.evaluate("document.querySelectorAll('img').length") == 0
    assert page.input_value("#f-q") == "<b>x</b>"
    state = controls_state(page)
    assert state["chips"] == default["chips"] and state["boxes"] == default["boxes"]
    assert state["inputs"] == ["", "", "<b>x</b>"]
    assert state["count"] == "1 filter active"
    assert state["summary"] == 'Search: "<b>x</b>"'
    assert set(shown_ids(page)) == expected(data, q="<b>x</b>") == {"client-a:tst8"}
    assert page.evaluate("location.hash") == "#v=1&q=%3Cb%3Ex%3C%2Fb%3E"
    assert o.problems() == []
    stale = open_page(ctx, page_file, hash="v=2&s=late")
    assert controls_state(stale.page) == default


# ---- TC-3108 -----------------------------------------------------------------------------

def test_TC_3108_reset_restores_the_defaults(ctx, page_file):
    """TC-3108 (LLR-3102.1): one Reset returns every control to its default, the default
    rows, a zero count and an empty hash."""
    clean = open_page(ctx, page_file)
    default = controls_state(clean.page)
    o = open_page(ctx, page_file, hash="v=1&s=late&u=ana.ruiz&q=a&sec=table&z=month")
    page = o.page
    assert count(page) == "3 filters active"
    page.click("#reset")
    assert controls_state(page) == default
    assert set(shown_ids(page)) == F.DEFAULT_SHOWN
    assert page.evaluate("location.hash") == "" and count(page) == "0 filters active"
    assert o.problems() == []


# ---- TC-3116 (workspace arm, PDR PA7) ---------------------------------------------------------

def test_TC_3116_offline_themes_and_phone_width(browser, page_file):
    """TC-3116's workspace arm (LLR-3106.2, PDR PA7/C11): at 390x844 in light and dark the
    page has no horizontal scroll (the 120-character and the Unicode titles included), the
    count and Reset sit in the first viewport, nothing is fetched, and the two schemes
    paint different backgrounds."""
    backgrounds = {}
    for scheme in ("light", "dark"):
        ctx = new_context(browser, scheme=scheme, viewport=(390, 844))
        o = open_page(ctx, page_file)
        page = o.page
        assert page.evaluate("document.documentElement.scrollWidth <= "
                             "document.documentElement.clientWidth")
        titles = page.eval_on_selector_all("#tbody tr td:first-child", "ts => ts.map(t => t.textContent)")
        assert F.LONG_TITLE in titles and F.UNICODE_TITLE in titles
        for sel in ("#active-count", "#reset"):
            assert page.eval_on_selector(sel, "e => e.getBoundingClientRect().bottom") <= 844
        backgrounds[scheme] = page.evaluate("getComputedStyle(document.body).backgroundColor")
        assert o.problems() == []
        ctx.close()
    assert backgrounds["light"] != backgrounds["dark"]


# ---- TC-3125 (behavioural arm, PDR PQ8) -----------------------------------------------------------

def test_TC_3125_the_page_follows_the_status_field(ctx, tmp_path, data):
    """TC-3125's behavioural arm (D19, PDR PQ8): the page READS each task's `status`.
    Edited in the embedded data — the due-today task marked late, a late task marked
    open — the `late` chip alone shows the edited set, not one re-derived from dates."""
    d = json.loads(json.dumps(data))
    for t in d["tasks"]:
        if t["key"] == "personal:tdc1":
            t["status"] = "late"
        if t["key"] == "personal:tmv2":
            t["status"] = "open"
    path = tmp_path / "edited.html"
    path.write_text(report_workspace.render(d), encoding="utf-8")
    o = open_page(ctx, path)
    _status(o.page)
    assert set(shown_ids(o.page)) == (F.LATE - {"personal:tmv2"}) | {"personal:tdc1"}
    assert o.problems() == []


def test_the_page_shell_holds_no_board_text(page_file):
    """D2 (LLR-3102.1): outside the data element the page carries no board-derived text —
    every control and label is built by the script from the data."""
    html = page_file.read_text(encoding="utf-8")
    shell = re.sub(r'<script id="board-data" type="application/json">.*?</script>', "", html,
                   flags=re.S)
    for word in ("Personal", "Storefront relaunch", "Ana Ruiz", "Launch", "qzT1", "qzP1",
                 "Pack kitchen"):
        assert word not in shell, word



# ==== increment 002: export this view (HLR-3103, HLR-3104) ======================================
#
# The downloads are caught with `expect_download` and saved under `tmp_path`; the oracle reads
# the SAVED bytes. Every dropped item is searched for in its raw and its JSON-escaped form
# (the form the page's script writes: a JSON string with `<`, `>`, `&` as \u escapes).

PRINT_CAPTION = "Print / Save as PDF — a PDF of what is shown; this HTML file still holds every task"
VIEW_CAPTION = "Download this view — a new HTML file with only these tasks"
TOKENS = ("qzP1", "qzB1", "qzU1", "qzM1", "qzT1", "qzL1", "qzN1", "qzK1")
CARMEN_VIEW = {"client-a:tst9", "client-a:tsp2", "course:tvd1", "course:tcm1"}
NOT_SIDE = F.DEFAULT_SHOWN - {"#3:tqzK1"}
DATA_RE = re.compile(r'<script id="board-data" type="application/json">(.*?)</script>', re.S)
STUB_PRINT = "(() => { window.__prints = 0; window.print = () => { window.__prints += 1; }; })()"


def escaped(s: str) -> str:
    return (json.dumps(s, ensure_ascii=False)[1:-1]
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def absent(raw: str, s: str) -> bool:
    return s not in raw and escaped(s) not in raw


def fetch(page, selector, folder):
    """Press a download control; the saved file and the name the page suggested."""
    with page.expect_download() as info:
        page.click(selector)
    dl = info.value
    path = folder / f"{len(list(folder.iterdir()))}-{dl.suggested_filename}"
    dl.save_as(path)
    return path, dl.suggested_filename


def embedded(raw: str) -> tuple:
    found = DATA_RE.findall(raw)
    assert len(found) == 1, f"{len(found)} data elements"
    return found[0], json.loads(found[0])


def dropped_strings(d: dict, keep: set) -> list:
    """Every board-derived string of an item the view drops — task keys (quoted), titles,
    URLs and notes, and the keys and names of projects, boards, people and classes no kept
    task uses — minus any string a kept item or the page's constant text also holds."""
    kept = [t for t in d["tasks"] if t["key"] in keep]
    used = {"projects": {t["project"] for t in kept}, "boards": {t["board"] for t in kept},
            "people": {h for t in kept for h in t["mentions"]},
            "marks": {t["mark"] for t in kept if t["mark"]}}
    blob = [report_workspace.CSS, report_workspace.JS, report_workspace.SHELL]
    out = []
    for t in d["tasks"]:
        if t["key"] in keep:
            blob.append(json.dumps(t, ensure_ascii=False))
        else:
            out += [f'"{t["key"]}"', t["title"], t["notes_text"], *t["urls"]]
    for kind, idk in (("projects", "key"), ("boards", "key"), ("people", "id"), ("marks", "key")):
        for x in d[kind]:
            if x[idk] in used[kind]:
                blob.append(json.dumps(x, ensure_ascii=False))
            else:
                out += [f'"{x[idk]}"', x["name"]]
    text = "\n".join(blob)
    return [s for s in out if s and s not in text]


def dangling(d2: dict) -> list:
    keys = {t["key"] for t in d2["tasks"]}
    return [k for t in d2["tasks"] for k in t["deps"] + t["chain"] if k not in keys]


def open_card_and_tip(page, key: str):
    page.click(f'#tbody tr[data-key="{key}"]')
    page.dispatch_event(f'#gantt .gbar[data-key="{key}"]', "mousemove",
                        {"clientX": 200, "clientY": 200})
    assert page.is_visible("#card")
    assert page.eval_on_selector("#tt", "e => getComputedStyle(e).display") == "block"


PRINT_STATE = """() => {
    const cs = e => getComputedStyle(e);
    const controls = [...document.querySelectorAll('button, input, select, textarea, summary')]
        .filter(e => !e.closest('thead'));
    const wrap = document.querySelector('.gantt-wrap').getBoundingClientRect();
    return {
        visible: controls.filter(e => e.getClientRects().length > 0)
            .map(e => e.id || (e.dataset.group + ':' + e.dataset.value)),
        total: controls.length,
        nav: cs(document.querySelector('nav')).display,
        card: cs(document.getElementById('card')).display,
        tt: cs(document.getElementById('tt')).display,
        header: cs(document.getElementById('view-header')).display,
        headerText: document.getElementById('view-header').innerText,
        rows: [...document.querySelectorAll('#tbody tr')].map(e => cs(e).breakInside),
        cards: [...document.querySelectorAll('.note, .ms')].map(e => cs(e).breakInside),
        bodyPad: cs(document.body).paddingTop,
        text: document.body.innerText,
        docWidth: document.documentElement.scrollWidth,
        gantt: document.getElementById('gantt').getBoundingClientRect().width,
        bars: document.querySelectorAll('#gantt .gbar').length,
        barsOut: [...document.querySelectorAll('#gantt .gbar')]
            .filter(b => b.getBoundingClientRect().right > wrap.right + 1).length,
        tblOverflow: cs(document.querySelector('.tbl-wrap')).overflowX,
        tblRight: document.querySelector('#s-table table').getBoundingClientRect().right,
        cellsRight: Math.max(...[...document.querySelectorAll('#s-table th, #s-table td')]
            .map(c => c.getBoundingClientRect().right)),
        lastHead: [...document.querySelectorAll('#thead-row th')].map(th => ({text: th.innerText,
            right: th.getBoundingClientRect().right, width: th.getBoundingClientRect().width})).pop(),
    };
}"""

# DU3/O3: the axis labels' boxes, left to right; a pair closer than 1 px collides
TICK_COLLISIONS = """() => {
    const r = [...document.querySelectorAll('#gantt text.gtick')]
        .map(e => e.getBoundingClientRect()).sort((a, b) => a.left - b.left);
    let n = 0;
    for(let i = 0; i < r.length; i++) for(let j = i + 1; j < r.length; j++)
        if(r[j].left < r[i].right + 1 && r[i].left < r[j].right + 1) n++;
    return {labels: r.length, collisions: n};
}"""

# DQ1 follow-up: in print every header and every date / priority / phase / age cell is ONE
# line (its text's height < 1.5 x its line-height); the wrapping cells (task, board, project,
# status) break a line only at a space, unless the word itself is wider than the column
TABLE_LINES = """() => {
    const lines = e => { const r = document.createRange(); r.selectNodeContents(e);
        const cs = getComputedStyle(e);
        const lh = cs.lineHeight === 'normal' ? parseFloat(cs.fontSize) * 1.2 : parseFloat(cs.lineHeight);
        return r.getBoundingClientRect().height / lh; };
    const one = [...document.querySelectorAll('#thead-row th button, #tbody td[data-col=start], '
        + '#tbody td[data-col=due], #tbody td[data-col=priority], #tbody td[data-col=phase], '
        + '#tbody td[data-col=age]')];
    const splits = new Set();
    for(const td of document.querySelectorAll('#tbody td[data-col=title], #tbody td[data-col=board], '
            + '#tbody td[data-col=project], #tbody td[data-col=status]')){
        const walk = document.createTreeWalker(td, NodeFilter.SHOW_TEXT);
        for(let n; (n = walk.nextNode());){
            const s = n.textContent; let top = null;
            for(let i = 0; i < s.length; i++){
                const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 1);
                const rc = r.getClientRects()[0];
                if(!rc) continue;
                if(top !== null && rc.top > top + 2 && s[i - 1] !== ' ' && s[i] !== ' ')
                    splits.add(s.slice(0, i).split(' ').pop() + s.slice(i).split(' ')[0]);
                top = rc.top;
            }
        }
    }
    return {checked: one.length, multi: one.filter(e => lines(e) >= 1.5).map(e => e.textContent),
            splits: [...splits]};
}"""
# the fixture's words wider than any print column: the only words a print line may split
OVERLONG = {F.HOSTILE_TITLE, "onerror=window.__x=2>", F.LONG_TITLE.split()[-1]}

PRINT_RULES = """() => {
    const out = [];
    const walk = (rules, print) => { for(const r of rules){
        if(r.media){ walk(r.cssRules, print || r.media.mediaText === 'print'); continue; }
        if(print) out.push(r.cssText); } };
    for(const s of document.styleSheets) walk(s.cssRules, false);
    return out;
}"""


# ---- AT-3103 -----------------------------------------------------------------------------------

def test_AT_3103_download_this_view_holds_only_the_filtered_tasks(ctx, page_file, data, tmp_path):
    """AT-3103 (HLR-3103): with the hidden board's project unchecked and one person filter
    on, "Download this view" saves a file whose data holds exactly the shown tasks; no
    dropped project, board, person, class, task, URL, note or key is in its bytes, raw or
    JSON-escaped; a kept task's dependency on a dropped one is cut; re-opened, the file
    shows the same rows (as a multiset) on the same view, says it is a filtered view with
    its export date, and logs no error and fetches nothing."""
    o = open_page(ctx, page_file)
    page = o.page
    open_projects(page)
    box(page, "#3:pside").uncheck()
    chip(page, "people", "carmen.vega").click()
    shown = shown_ids(page)
    assert set(shown) == CARMEN_VIEW == expected(
        data, p=set(F.PROJECT_KEYS) - {"#3:pside"}, u=("carmen.vega",))
    path, name = fetch(page, "#dl-view", tmp_path)
    assert re.fullmatch(r"workspace-view-\d{4}-\d{2}-\d{2}\.html", name)
    raw = path.read_text(encoding="utf-8")
    _, d2 = embedded(raw)

    assert Counter(t["key"] for t in d2["tasks"]) == shown
    for token in TOKENS:
        assert token not in raw, token
    gone = dropped_strings(data, CARMEN_VIEW)
    assert len(gone) > 80
    literals = ["Personal", "Taxes 2026", "Move apartment", "Ana Ruiz", "Luis Prado",
                F.HOSTILE_PERSON, F.HOSTILE_NAME, F.HOSTILE_TITLE, F.SIDE_BOARD_NAME,
                "FAQ rewrite", "Delivery", "Billing", "Launch", "ana.ruiz",
                "https://staging.example.test/storefront", '"client-a:tsp1"']
    for s in gone + literals:
        assert absent(raw, s), s
    assert dangling(d2) == []
    before = next(t for t in data["tasks"] if t["key"] == "client-a:tsp2")
    after = next(t for t in d2["tasks"] if t["key"] == "client-a:tsp2")
    assert before["deps"] == ["client-a:tsp1"] and after["deps"] == []
    assert [t["title"] for t in d2["tasks"]].count(F.DOLLAR_TITLE) == 1
    assert d2["meta"]["scope"]["boards"] == ["Client A", "Course"]
    assert [p["id"] for p in d2["people"]] == ["carmen.vega"] and d2["marks"] == []

    again = open_page(ctx, path)
    rp = again.page
    assert shown_ids(rp) == shown
    assert chip(rp, "people", "carmen.vega").get_attribute("aria-pressed") == "true"
    assert rp.text_content("#view-summary") == d2["meta"]["view"]["summary"] == "People: Carmen Vega"
    origin = rp.text_content("#view-origin")
    assert rp.is_visible("#view-origin") and origin.startswith("A filtered view, exported ")
    assert d2["meta"]["view"]["exported"] in origin
    assert rp.text_content("#scope-line") == "Boards in this view (2): Client A, Course"
    assert o.problems() == [] and again.problems() == []


# ---- TC-3109 -----------------------------------------------------------------------------------

def test_TC_3109_the_download_keeps_only_used_entries(ctx, page_file, data, tmp_path):
    """TC-3109 (LLR-3103.1, D2/D3): the downloaded data holds the shown tasks and only the
    projects, boards, people and classes they use (0 unused, 0 dangling keys); the JSON
    holds no raw `<`, `>`, `&`; the `$&` / `$'` title arrives once, as text, and the data is
    still exactly the kept set (a `String.replace` composition would re-insert the shell)."""
    o = open_page(ctx, page_file)
    page = o.page
    open_projects(page)
    box(page, "#3:pside").uncheck()
    assert set(shown_ids(page)) == NOT_SIDE
    path, _ = fetch(page, "#dl-view", tmp_path)
    raw = path.read_text(encoding="utf-8")
    text, d2 = embedded(raw)
    assert not {"<", ">", "&"} & set(text)
    ids = [t["key"] for t in d2["tasks"]]
    assert len(ids) == len(NOT_SIDE) == 32 and set(ids) == NOT_SIDE
    tasks = d2["tasks"]
    assert [p["key"] for p in d2["projects"]] == [
        k for k in F.PROJECT_KEYS if k in {t["project"] for t in tasks}]
    assert {t["project"] for t in tasks} == {p["key"] for p in d2["projects"]}
    assert [b["key"] for b in d2["boards"]] == ["personal", "client-a", "course"]
    assert [p["id"] for p in d2["people"]] == ["ana.ruiz", "luis.prado", "carmen.vega", "zed.hostile"]
    assert {h for t in tasks for h in t["mentions"]} == {p["id"] for p in d2["people"]}
    assert [m["key"] for m in d2["marks"]] == ["delivery", "billing", "launch"]
    assert {t["mark"] for t in tasks if t["mark"]} == {m["key"] for m in d2["marks"]}
    assert dangling(d2) == []
    for token in TOKENS:
        assert token not in raw, token
    for s in dropped_strings(data, NOT_SIDE):
        assert absent(raw, s), s
    assert [t["title"] for t in tasks].count(F.DOLLAR_TITLE) == 1
    assert raw.count(escaped(F.DOLLAR_TITLE)) == 1 and raw.count('id="board-data"') == 1
    assert d2["meta"]["scope"] == {"kind": "all", "project": None,
                                   "boards": ["Personal", "Client A", "Course"]}
    # every kept project keeps all its non-archived tasks here, so its counts equal the
    # extraction's; worst and momentum (server-derived) leave the download
    source = {p["key"]: p for p in data["projects"]}
    assert d2["projects"]
    for p in d2["projects"]:
        assert p["worst"] is None and p["momentum"] is None
        assert {**p, "worst": 0, "momentum": 0} == {**source[p["key"]], "worst": 0, "momentum": 0}

    # a view hiding part of each kept project: its facts describe the kept tasks only
    f = open_page(ctx, page_file, hash="v=1&s=open,late&u=ana.ruiz,luis.prado")
    fpath, _ = fetch(f.page, "#dl-view", tmp_path)
    _, d3 = embedded(fpath.read_text(encoding="utf-8"))
    assert {t["key"] for t in d3["tasks"]} == {
        "personal:tmv2", "personal:ttx1", "client-a:tst2", "client-a:tsp1"}
    facts = ("open", "late", "done", "high", "worst", "momentum")
    got = {p["key"]: tuple(p[k] for k in facts) for p in d3["projects"]}
    assert got == {
        "personal:pmove": (1, 1, 0, 1, None, None),
        "personal:ptax": (1, 0, 0, 0, None, None),
        "client-a:prel": (1, 0, 0, 1, None, None),
        "client-a:pdocs": (1, 0, 0, 0, None, None),
    }
    assert tuple(source["client-a:prel"][k] for k in facts)[:4] == (10, 2, 1, 4)
    assert tuple(source["personal:pmove"][k] for k in facts)[:4] == (4, 1, 1, 2)
    assert o.problems() == [] and f.problems() == []


# ---- TC-3110 -----------------------------------------------------------------------------------

def test_TC_3110_notes_off_strips_the_notes(ctx, page_file, tmp_path):
    """TC-3110 (LLR-3103.1, PDR C2/PA2, security SD1): with the notes section on, the notes
    and their mentions travel (the kept hidden-board task's `qzN1` note included); with it
    off, every `notes_html` AND every `notes_text` is empty and no note text is in the file,
    the tasks all stay; the mentions go too, but for the pressed people filter's own, and
    `people` keeps only the persons still referenced (the CSV/JSON mentions follow)."""
    o = open_page(ctx, page_file)
    page = o.page
    path, _ = fetch(page, "#dl-view", tmp_path)
    raw_on = path.read_text(encoding="utf-8")
    _, on = embedded(raw_on)
    assert sum(1 for t in on["tasks"] if t["notes_html"]) == 13
    assert sum(1 for t in on["tasks"] if t["notes_text"]) == 13 and "qzN1" in raw_on
    chip(page, "sections", "notes").click()
    path, _ = fetch(page, "#dl-view", tmp_path)
    raw = path.read_text(encoding="utf-8")
    _, off = embedded(raw)
    assert len(off["tasks"]) == len(F.DEFAULT_SHOWN) == 33
    assert [t for t in off["tasks"] if t["notes_html"] or t["notes_text"]] == []
    for s in ("qzN1", "narrates once the script settles", "still missing boxes", "scanner app works"):
        assert absent(raw, s), s
    assert sum(len(t["mentions"]) for t in on["tasks"]) > 0 and len(on["people"]) == 5
    assert [t for t in off["tasks"] if t["mentions"]] == [] and off["people"] == []
    for s in ("Ana Ruiz", "Luis Prado", "Una qzU1", F.HOSTILE_PERSON, "ana.ruiz", "una.qz"):
        assert absent(raw, s), s

    pressed = open_page(ctx, page_file, hash="v=1&u=ana.ruiz&sec=gantt,table,milestones")
    path, _ = fetch(pressed.page, "#dl-view", tmp_path)
    raw = path.read_text(encoding="utf-8")
    _, ana = embedded(raw)
    assert {t["key"]: t["mentions"] for t in ana["tasks"]} == {
        "personal:ttx1": ["ana.ruiz"], "client-a:tst2": ["ana.ruiz"], "client-a:tsp1": ["ana.ruiz"]}
    assert [p["id"] for p in ana["people"]] == ["ana.ruiz"]
    assert absent(raw, "Luis Prado") and absent(raw, "luis.prado")
    again = open_page(ctx, path)
    assert chip(again.page, "people", "ana.ruiz").get_attribute("aria-pressed") == "true"
    assert set(shown_ids(again.page)) == {"personal:ttx1", "client-a:tst2", "client-a:tsp1"}
    cpath, _ = fetch(pressed.page, "#dl-csv", tmp_path)
    jpath, _ = fetch(pressed.page, "#dl-json", tmp_path)
    assert {r["mentions"] for r in read_csv(cpath)} == {"'@ana.ruiz"}
    assert {r["mentions"] for r in json.loads(jpath.read_text(encoding="utf-8"))["tasks"]} == {"@ana.ruiz"}
    assert "luis.prado" not in cpath.read_text(encoding="utf-8")
    assert o.problems() == [] and pressed.problems() == [] and again.problems() == []


# ---- TC-3111 -----------------------------------------------------------------------------------

VIEW_HASH = ("v=1&p=client-a%3Apdocs,course%3Apvid,course%3Apcom&s=open,late,done,archived"
             "&sec=gantt,table&z=week")
VIEW_SET = {"client-a:tsp1", "client-a:tsp2", "client-a:tsp3", "course:tvd1", "course:tvd2",
            "course:tvd3", "course:tvd4", "course:tvd5", "course:tvd6", "course:tcm1",
            "course:tcm2"}


def test_TC_3111_the_view_file_reopens_on_its_view(ctx, page_file, data, tmp_path):
    """TC-3111 (LLR-3103.2, D5): the saved file is `workspace-view-<date>.html`; opened,
    it shows the source's rows as a multiset, its controls built once (no duplicate chip
    or box) in the source's states, its header names the summary and the export date;
    downloading again from it gives the same data; a `meta.view` edited to name an unknown
    project is whitelisted on restore; a view keeping nothing opens and says so; the file's
    scope line reads "Boards in this view (N): …" naming only its own boards (DU5)."""
    o = open_page(ctx, page_file, hash=VIEW_HASH)
    page = o.page
    shown = shown_ids(page)
    assert set(shown) == VIEW_SET == expected(
        data, p={"client-a:pdocs", "course:pvid", "course:pcom"},
        s=("open", "late", "done", "archived"))
    path, name = fetch(page, "#dl-view", tmp_path)
    assert re.fullmatch(r"workspace-view-\d{4}-\d{2}-\d{2}\.html", name)
    assert name == f"workspace-view-{date.today().isoformat()}.html"
    raw = path.read_text(encoding="utf-8")
    _, d2 = embedded(raw)
    mv = d2["meta"]["view"]
    assert mv["exported"] == date.today().isoformat()
    assert mv["state"] == "v=1&s=open,late,done,archived&sec=gantt,table&z=week"

    again = open_page(ctx, path)
    rp = again.page
    assert shown_ids(rp) == shown
    st = controls_state(rp)
    want_chips = 4 + len(d2["people"]) + len(d2["marks"]) + 4 + 4
    assert len(st["chips"]) == want_chips == 4 + 0 + 1 + 4 + 4    # notes off, no people filter: no person (SD1)
    assert st["boxes"] == [["client-a:pdocs", True], ["course:pvid", True], ["course:pcom", True]]
    pressed = {(g, v) for g, v, p in st["chips"] if p == "true"}
    assert ("status", "archived") in pressed and ("zoom", "week") in pressed
    assert ("sections", "notes") not in pressed and st["sections"] == [False, False, True, True]
    assert st["summary"] == mv["summary"] == "Status: open, late, done, archived"
    assert mv["exported"] in rp.text_content("#view-origin")
    # DU5: a filtered file names the boards IT holds, never "All loaded boards"
    assert rp.text_content("#scope-line") == "Boards in this view (2): Client A, Course"
    rp.evaluate("location.hash = ''")          # CR2-2: back to the file's own view
    rp.wait_for_function("location.hash !== ''")
    assert shown_ids(rp) == shown
    assert ("status", "archived") in {(g, v) for g, v, p in controls_state(rp)["chips"] if p == "true"}

    path3, _ = fetch(rp, "#dl-view", tmp_path)
    _, d3 = embedded(path3.read_text(encoding="utf-8"))
    for k in ("tasks", "projects", "boards", "people", "marks"):
        assert d3[k] == d2[k], k
    assert d3["meta"]["view"]["state"] == mv["state"]

    edited = json.loads(json.dumps(d2))
    edited["meta"]["view"]["state"] = "v=1&p=ghost%3Aqq,course%3Apcom&s=open,late,done,archived"
    text, _ = embedded(raw)
    path4 = tmp_path / "edited-view.html"
    path4.write_text(raw.replace(text, report_html.embed_json(edited)), encoding="utf-8")
    ed = open_page(ctx, path4)
    assert set(shown_ids(ed.page)) == {"course:tcm1", "course:tcm2"}
    assert [b for b in controls_state(ed.page)["boxes"] if b[1]] == [["course:pcom", True]]

    empty = open_page(ctx, page_file, hash="v=1&s=")
    path5, _ = fetch(empty.page, "#dl-view", tmp_path)
    _, d5 = embedded(path5.read_text(encoding="utf-8"))
    assert d5["tasks"] == [] and d5["people"] == [] and d5["boards"] == []
    nothing = open_page(ctx, path5)
    assert shown_ids(nothing.page) == {} and nothing.page.is_visible("#tempty")
    assert nothing.page.is_visible("#view-origin")
    assert nothing.page.text_content("#scope-line") == "Boards in this view (0)"
    for x in (o, again, ed, empty, nothing):
        assert x.problems() == []


def test_TC_3111_the_export_captions_show_without_hover(browser, page_file):
    """TC-3111's label arm (LLR-3103.2/3103.3, PDR C6): at 1366 and 390 px, light and dark,
    each export control's caption is on the page verbatim and visible beside it with no
    hover, inside the viewport's width; the CSV and JSON labels say "visible rows only"."""
    for width, scheme in ((1366, "dark"), (1366, "light"), (390, "dark"), (390, "light")):
        ctx = new_context(browser, scheme=scheme, viewport=(width, 900))
        try:
            o = open_page(ctx, page_file)
            page = o.page
            assert page.text_content("#f-export .lbl") == "Export this view"
            for sel, caption in (("#x-print", PRINT_CAPTION), ("#x-view", VIEW_CAPTION)):
                assert page.text_content(sel) == caption
                assert page.inner_text(sel) == caption
                cap = page.locator(f"{sel} .cap")
                assert cap.is_visible()
                b = cap.bounding_box()
                assert b["width"] > 0 and b["x"] + b["width"] <= width
            for sel in ("#dl-csv", "#dl-json"):
                assert page.text_content(sel).endswith("visible rows only")
                assert page.locator(sel).is_visible()
            assert o.problems() == []
        finally:
            ctx.close()


# ---- AT-3104 -----------------------------------------------------------------------------------

def test_AT_3104_print_hides_the_controls_and_shows_the_filter_header(ctx, page_file):
    """AT-3104 (HLR-3104): with no filter the header says "all tasks"; with one filter on,
    the task card and the tooltip open and `beforeprint` dispatched, in print media every
    control, the card and the tooltip are gone (0 visible), the header shows the filter
    summary, the generated date and the printed date, rows and cards never split, the
    gantt fits the printed page (794 px, DQ4); "Print / Save as PDF" calls `window.print`
    once per press."""
    o = open_page(ctx, page_file)
    page = o.page
    assert "all tasks" in page.text_content("#view-summary")
    chip(page, "people", "ana.ruiz").click()
    page.evaluate(STUB_PRINT)
    page.click("#print")
    assert page.evaluate("window.__prints") == 1
    page.click("#print")
    assert page.evaluate("window.__prints") == 2
    page.evaluate("(() => { const e = document.getElementById('print-line');"
                  " e.hidden = true; e.textContent = ''; })()")
    open_card_and_tip(page, "client-a:tst2")
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    page.set_viewport_size({"width": 794, "height": 1123})    # an A4 page's CSS width
    page.emulate_media(media="print")
    st = page.evaluate(PRINT_STATE)
    assert st["total"] >= 45 and st["visible"] == []
    assert st["nav"] == st["card"] == st["tt"] == "none"
    assert st["header"] == "block"
    head = st["headerText"]
    assert "People: Ana Ruiz" in head and "Generated 2026-10-29" in head
    assert f"Printed {date.today().isoformat()}" in head
    assert st["rows"] and set(st["rows"]) == {"avoid"}
    assert st["cards"] and set(st["cards"]) == {"avoid"}
    assert st["gantt"] <= 794 and st["docWidth"] <= 794
    assert o.problems() == []


# ---- TC-3112 -----------------------------------------------------------------------------------

def test_TC_3112_the_print_rules_hold(browser, page_file):
    """TC-3112 (LLR-3104.1, PDR C7/C14): the print stylesheet holds the three full-gantt rules
    and `@page { margin: 0 }` with a body padding; at a printed-page viewport of 794 px, on
    the day zoom (a timeline far wider than the page), the gantt's width and the page's
    scroll width are <= 794 and every bar lies inside the printed figure; the task table
    shows every column inside the page, STATUS last (DQ1/DU2); with a project hidden, the
    printed text names it nowhere and every printed count is over kept tasks, the printed
    header included: no "/<total>" (DQ2/DU1)."""
    ctx = new_context(browser, viewport=(794, 1123))
    try:
        o = open_page(ctx, page_file, hash="v=1&z=day")
        page = o.page
        open_projects(page)
        box(page, "personal:ptax").uncheck()
        page.evaluate(STUB_PRINT)
        page.click("#print")
        assert page.evaluate("window.__prints") == 1
        assert page.is_hidden("#print-line")    # the stamp is beforeprint's, not the button's
        assert page.eval_on_selector("#gantt", "e => e.scrollWidth") > 794 * 2
        open_card_and_tip(page, "client-a:tst2")
        page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        page.emulate_media(media="print")

        rules = page.evaluate(PRINT_RULES)
        gantt_rules = [
            any(r.startswith(".gantt-wrap {") and "overflow: visible" in r for r in rules),
            any(r.startswith("#gantt {") and "min-width: 0px !important" in r for r in rules),
            any(r.startswith("#gantt svg {") and "width: 100%" in r and "height: auto" in r
                for r in rules)]
        assert gantt_rules == [True, True, True]
        assert sum(1 for r in rules if r.startswith("@page") and "margin: 0px" in r) == 1
        st = page.evaluate(PRINT_STATE)
        assert st["bodyPad"] != "0px"
        assert st["visible"] == [] and st["card"] == st["tt"] == "none"
        assert st["docWidth"] <= 794 and st["gantt"] <= 794
        assert st["bars"] == 28 and st["barsOut"] == 0     # 31 kept, 3 undated
        # DQ1/DU2: no scroll window clips the table; its last column ends inside the page
        assert st["tblOverflow"] == "visible"
        assert st["tblRight"] <= 794 and st["cellsRight"] <= 794
        assert st["lastHead"]["text"] == "STATUS" and 0 < st["lastHead"]["width"]
        assert st["lastHead"]["right"] <= 794
        # ...and splits no header, date, priority, phase or age, and no word that fits
        tl = page.evaluate(TABLE_LINES)
        assert tl["checked"] == 9 + 5 * 31 and tl["multi"] == []
        assert set(tl["splits"]) <= OVERLONG, tl["splits"]
        # DQ2: the printed summary names the shown projects and counts no file total
        assert re.search(r"/\d", st["headerText"]) is None
        assert ("Projects: Move apartment, Docs, Inbox, Storefront relaunch, Docs, Legacy site, "
                "Old campaign, Video module 3, Community forum, Someday ideas, "
                f"{F.HOSTILE_NAME}, Hidden qzP1") in st["headerText"]
        text = st["text"]
        assert "Taxes 2026" not in text and "Gather deduction receipts" not in text
        assert "Showing 31 tasks" in text and "of 37" not in text
        tiles = sum(int(page.text_content(f"#tile-{s}")) for s in ("open", "late", "done", "archived"))
        assert tiles == 31
        assert st["headerText"].count(f"Printed {date.today().isoformat()}") == 1
        page.evaluate("window.dispatchEvent(new Event('afterprint'))")
        assert page.is_hidden("#print-line")
        assert o.problems() == []
    finally:
        ctx.close()


def test_TC_3112_the_printed_header_names_only_the_shown_boards(browser, page_file):
    """TC-3112's header arm (LLR-3104.1, PDR criterion 2, DQ2/DU1): the PDF is what a
    recipient gets. With the side board's one project hidden, the screen keeps the file's
    own scope line and "Projects 12/13", while the printed header names only the three
    boards a shown task is on, names no hidden board or project, and prints no "/<total>"."""
    total = len(F.PROJECT_KEYS)
    ctx = new_context(browser, viewport=(794, 1123))
    try:
        o = open_page(ctx, page_file)
        page = o.page
        open_projects(page)
        box(page, "#3:pside").uncheck()
        assert set(shown_ids(page)) == NOT_SIDE
        assert page.text_content("#scope-line") == F.SCOPE_LINE
        assert page.text_content("#view-summary").startswith(f"Projects {total - 1}/{total}: ")
        page.emulate_media(media="print")
        st = page.evaluate(PRINT_STATE)
        head = st["headerText"]
        assert "Boards in this view (3): Personal, Client A, Course" in head
        for gone in ("All loaded boards", "qzB1", "qzP1", F.SIDE_BOARD_NAME):
            assert gone not in head and gone not in st["text"], gone
        assert re.search(r"/\d", head) is None
        assert f"Projects {total - 1}" not in head and "Projects: " in head
        assert o.problems() == []
    finally:
        ctx.close()


def test_TC_3112_a_project_file_with_its_project_hidden_prints_no_name(browser, tmp_path):
    """TC-3112's project-scope arm (CR5-1): a workspace written for one project (Storefront
    relaunch on Client A), that project unchecked: the printed header reads "Boards in this
    view (0)" and names neither the project nor its board."""
    d = report_html.extract(F.lanes(), F.PEOPLE, F.MARKS, F.TODAY, project="client-a:prel")
    path = report_html.write_reports(d, ("workspace",), tmp_path, F.TODAY)[0]
    ctx = new_context(browser, viewport=(794, 1123))
    try:
        o = open_page(ctx, path)
        page = o.page
        assert page.text_content("#scope-line") == "Project Storefront relaunch on Client A"
        open_projects(page)
        box(page, "client-a:prel").uncheck()
        assert shown_ids(page) == {}
        page.emulate_media(media="print")
        head = page.evaluate(PRINT_STATE)["headerText"]
        assert "Boards in this view (0)" in head
        assert "Storefront relaunch" not in head and "Client A" not in head
        assert o.problems() == []
    finally:
        ctx.close()


def test_TC_3112_the_gantt_axis_labels_never_collide(browser, page_file):
    """DU3/O3 (LLR-3104.1's printed gantt, LLR-3102.1's screen one): on the day zoom, where
    a month label ("Nov 1") would sit on the next days' numbers, and on the default zoom,
    the axis labels' boxes never touch: 0 pairs closer than 1 px at 1366 px on screen and
    at the 794 px printed page; the month labels survive the skipping."""
    for width, media in ((1366, "screen"), (794, "print")):
        for hash_ in ("v=1&z=day", "v=1"):
            ctx = new_context(browser, viewport=(width, 1123))
            try:
                o = open_page(ctx, page_file, hash=hash_)
                page = o.page
                page.emulate_media(media=media)
                got = page.evaluate(TICK_COLLISIONS)
                assert got["labels"] >= 10 and got["collisions"] == 0, (width, hash_, got)
                if hash_ == "v=1&z=day":
                    lbls = page.eval_on_selector_all("#gantt text.gtick", "es => es.map(e => e.textContent)")
                    assert {"Oct 1", "Nov 1", "Dec 1"} <= set(lbls)
                assert o.problems() == []
            finally:
                ctx.close()


# ---- TC-3122 -----------------------------------------------------------------------------------

def guarded(v) -> str:
    """LLR-3103.3's CSV rule, the oracle side: `'` before a formula-leading cell, except a
    plain number."""
    s = "" if v is None else str(v)
    if re.match(r"[=+\-@\t\r]", s) and not re.fullmatch(r"-?\d+(\.\d+)?", s):
        return "'" + s
    return s


def read_csv(path) -> list:
    return list(csv.DictReader(io.StringIO(path.read_bytes().decode("utf-8"), newline="")))


def test_TC_3122_csv_and_json_hold_the_visible_rows_only(ctx, page_file, data, tmp_path):
    """TC-3122 (LLR-3103.3, D7, PDR C13): with the hidden board's project unchecked, the CSV
    and the JSON hold exactly the shown rows and none of its tokens; titles starting with
    `=`, `+`, `-`, `@` reach the CSV `'`-prefixed, a `-3d`, TAB and CR cell too, while the
    `due_in` number `-1` stays a number; a kept task's dependency on a dropped one leaves
    no title; notes off empties every notes cell; an empty view writes the header only."""
    o = open_page(ctx, page_file)
    page = o.page
    for sel in ("#dl-csv", "#dl-json"):
        assert "visible rows only" in page.text_content(sel)
    open_projects(page)
    box(page, "#3:pside").uncheck()
    cpath, _ = fetch(page, "#dl-csv", tmp_path)
    jpath, _ = fetch(page, "#dl-json", tmp_path)
    craw, jraw = cpath.read_text(encoding="utf-8"), jpath.read_text(encoding="utf-8")
    rows, jrows = read_csv(cpath), json.loads(jraw)["tasks"]
    bn = {b["key"]: b["name"] for b in data["boards"]}
    pn = {p["key"]: p["name"] for p in data["projects"]}
    kept = [t for t in data["tasks"] if t["key"] in NOT_SIDE]
    assert len(rows) == len(jrows) == 32
    assert Counter((r["board"], r["project"], r["task"]) for r in rows) == Counter(
        (guarded(bn[t["board"]]), guarded(pn[t["project"]]), guarded(t["title"])) for t in kept)
    assert Counter((r["board"], r["project"], r["task"]) for r in jrows) == Counter(
        (bn[t["board"]], pn[t["project"]], t["title"]) for t in kept)
    for token in TOKENS + ("una.qz",):
        assert token not in craw and token not in jraw, token
    titles = {r["task"] for r in rows}
    assert {"'=1+1 sanity check", "'+1 follow-up call", "'-draft- outline", "'@home prep"} <= titles
    pack = next(r for r in rows if r["task"] == "Pack kitchen")
    assert pack["due_in"] == "-1" and pack["mentions"] == "'@luis.prado"
    assert next(r for r in rows if r["task"] == "API reference")["depends_on"] == "Homepage build"
    assert any(r["notes"] for r in rows) and any(r["notes"] for r in jrows)
    assert page.evaluate("csvCell('-3d')") == "'-3d"
    assert page.evaluate("csvCell('\\tx')") == "'\tx"
    assert page.evaluate("csvCell('\\rx')") == "\"'\rx\""
    assert page.evaluate("[csvCell(-1), csvCell('-1.5'), csvCell('12')]") == ["-1", "-1.5", "12"]

    second = open_page(ctx, page_file, hash="v=1&u=carmen.vega&sec=gantt,table,milestones")
    c2, _ = fetch(second.page, "#dl-csv", tmp_path)
    j2, _ = fetch(second.page, "#dl-json", tmp_path)
    rows2, jrows2 = read_csv(c2), json.loads(j2.read_text(encoding="utf-8"))["tasks"]
    by = {t["key"]: t for t in data["tasks"]}
    assert sorted(r["task"] for r in rows2) == sorted(by[k]["title"] for k in CARMEN_VIEW)
    assert next(r for r in rows2 if r["task"] == "Tutorial videos")["depends_on"] == ""
    for raw2 in (c2.read_text(encoding="utf-8"), j2.read_text(encoding="utf-8")):
        assert "FAQ rewrite" not in raw2
    assert all(r["notes"] == "" for r in rows2) and all(r["notes"] == "" for r in jrows2)
    assert {r["mentions"] for r in rows2} == {"'@carmen.vega"}

    third = open_page(ctx, page_file, hash="v=1&s=")
    c3, _ = fetch(third.page, "#dl-csv", tmp_path)
    j3, _ = fetch(third.page, "#dl-json", tmp_path)
    assert c3.read_text(encoding="utf-8") == craw.split("\n")[0]
    assert json.loads(j3.read_text(encoding="utf-8"))["tasks"] == []
    for x in (o, second, third):
        assert x.problems() == []
