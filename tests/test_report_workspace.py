"""The interactive workspace report, driven in headless Chromium (batch 2026-10-29-batch-01,
increment 001: HLR-3102, LLR-3102.1..3, LLR-3106.2's workspace arm, LLR-3101.1's status).

Black-box: the page is written by `report_html.write_reports` (the call the `H` export
makes), opened from disk, and driven by clicks, key presses and typed values; the
assertions read the rows, bars and cards the page shows. Expected sets come from the
fixture's literals or from the truth table of LLR-3102.2 applied in Python to the
extraction — never from the page. Every page also counts console errors, page errors,
dialogs and foreign requests (`report_browser`), which must stay at zero.

One Chromium per module, a fresh context per test, a 10 s default timeout per action.
"""
from __future__ import annotations

import json
import re

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
            + [["BUTTON", "dl-csv"], ["BUTTON", "dl-json"]])
    assert len(want) == 43
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
    # to == mv4's start (Nov 1) and from == mv3's due (Oct 31): both shown
    "dates": (_dates, dict(frm="2026-10-31", to="2026-11-01"),
              {"personal:tmv3", "personal:tmv4"}),
    "search": (_search, dict(q="faq"), F.FAQ),
}


@pytest.mark.parametrize("arm", list(TRUTH_ARMS))
def test_TC_3106_filters_follow_the_truth_table(ctx, page_file, data, arm):
    """TC-3106 (LLR-3102.2): one arm per row of the truth table; the shown set equals the
    table's rule applied in Python, and contains the arm's literal tasks (the dates arm:
    a span touching `to` with its start and `from` with its due both show)."""
    assert len(TRUTH_ARMS) == 6
    act, rule, literal = TRUTH_ARMS[arm]
    o = open_page(ctx, page_file)
    act(o.page)
    got = set(shown_ids(o.page))
    assert got == expected(data, **rule)
    assert literal <= got if arm == "dates" else got == literal
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
