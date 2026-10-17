"""The tick row's label names the selection, never the scale (batch 2026-10-17-batch-01).

HLR-1701 / LLR-1701.1 · AT-1701 · TC-1701.

Why these matter: left of the tick row both the gantt view (`3`) and the
presentation (`R`) used to paint the axis scale — `Mondays · 1 day = 2 cells`,
`Mondays · .5 d/cell`. The operator, 2026-10-17: «Es la etiqueta de Mondays y
cells? Si es así, hay que quitarla. No agrega valor». The bright dates on that
row belong to the selected task, so the label says so: `selected task ▸`; the
echo's own dates when they did not fit the field; `selected: no dates` when the
task has none; nothing at all when nothing is selected. One rule in both views,
so the two cannot drift into two dialects again.

The scale-text pattern is written from what the deleted label produced
(`<cadence> · <scale>`: the cadences `gantt_cadence` names, the scale in cells),
never from the new renderer, and it is case-sensitive; its positive control is
the five strings the old label painted, typed by hand from that rule.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
from rich.text import Text

import kg_board
import present_board as pb
from taskboard import app as app_mod
from taskboard import views
from taskboard.app import TaskboardApp

SCALE_TEXT = re.compile(r"(?:daily|Mondays|1st/15th|1st) · |\bd/cell\b|\bcells?\b")
OLD_SCALE_LABELS = ("Mondays · 1 day = 2 cells", "Mondays · 1 cell = 1 day",
                    "1st/15th · 1 cell = 2 days", "1st · 1 cell = 7 days",
                    "Mondays · .5 d/cell")
NOT_SCALE = ("cancelled", "Daily revenue model", "selected task ▸", "selected: no dates")


def _svg_text(path: Path) -> str:
    """The export's text as a reader sees it: Rich writes each space `&#160;`."""
    return path.read_text(encoding="utf-8").replace("&#160;", " ")


def test_TC_1701_the_scale_pattern_sees_every_old_label(tmp_path):
    """TC-1701 positive control: the pattern matches each label the old renderer
    painted — as plain text and inside an SVG the export path writes — and none
    of the words a frame legitimately paints."""
    for i, text in enumerate(OLD_SCALE_LABELS):
        assert SCALE_TEXT.search(text), text
        svg = views.save_present_svg(Text("  " + text + "  9"), tmp_path / f"{i}.svg", 60, 2)
        assert SCALE_TEXT.search(_svg_text(svg)), ("svg", text)
    for text in NOT_SCALE:
        assert not SCALE_TEXT.search(text), text


# --------------------------------------------------------------------------- #
# the gantt view, renderer level
# --------------------------------------------------------------------------- #
SIZES = [(118, 30), (80, 24)]


def _gantt_rows(b, sel, w, h):
    return views.render_gantt(b, False, sel, kg_board.TODAY, width=w, height=h).plain.split("\n")


def _gantt_tick_markup(b, sel, w, h):
    lines, _drawn, _groups, _ax = views._gantt_frame(b, False, sel, kg_board.TODAY, w, h)
    return lines[2]


def _label(row: str, w: int) -> str:
    return row[:views.gantt_columns(w)[0]].strip()


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1701_gantt_names_the_selected_task(w, h):
    """TC-1701 (a), gantt: `tw3` (past due: `over`) has an echo that fits, so
    the label reads `selected task ▸` in the echo's tone, bold — the row's lit
    dates (`Sep 24`) are that task's."""
    b = kg_board.build()
    row = _gantt_rows(b, "tw3", w, h)[2]
    assert _label(row, w) == "selected task ▸", row
    assert "Sep 24" in row, row
    assert _gantt_tick_markup(b, "tw3", w, h).startswith("[b " + views.HEX["over"] + "]")


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1701_gantt_too_long_echo_keeps_its_dates(w, h):
    """TC-1701 (a), gantt: a selection spanning the whole window leaves its
    dates no room on the row, so the label carries them, `▸` after."""
    b = kg_board.build()
    t = b.task_by_id("tw1")
    t.start_date, t.due_date = "2026-07-01", "2026-12-31"
    assert _label(_gantt_rows(b, "tw1", w, h)[2], w) == "Jul 1 → Dec 31 ▸"


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1701_gantt_selection_before_the_window(w, h):
    """TC-1701 (a), gantt boundary: `tw1` ends before the fitted window — its
    echo sits at the window's edge (`◂`) and the label still names it."""
    b = kg_board.build()
    row = _gantt_rows(b, "tw1", w, h)[2]
    assert _label(row, w) == "selected task ▸", row
    assert views.OFF_LEFT in row and "Aug 23–Sep 10" in row, row


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1701_gantt_dateless_and_no_selection(w, h):
    """TC-1701 (a), gantt: `ta5` has no date — `selected: no dates`, dim; with
    nothing selected the label column is blank."""
    b = kg_board.build()
    assert _label(_gantt_rows(b, "ta5", w, h)[2], w) == "selected: no dates"
    assert _gantt_tick_markup(b, "ta5", w, h).startswith("[" + views.HEX["dim"] + "]")
    assert _label(_gantt_rows(b, None, w, h)[2], w) == ""


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1701_gantt_search_that_hides_the_selection(w, h):
    """TC-1701 (a), gantt boundary: a search that keeps tasks but not the
    selected one — the frame has no selection to name, so the label is blank."""
    b = kg_board.build()
    fb = views.filtered_board(b, b.task_by_id("tm1").title, False)
    assert fb.visible_tasks(False) and fb.task_by_id("tw3") is None
    assert _label(_gantt_rows(fb, "tw3", w, h)[2], w) == ""


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1701_link_mode_names_the_candidate(w, h):
    """TC-1701 (a), link mode: the candidate is the selection — `selected task
    ▸`; with no candidate the label is blank."""
    b = kg_board.build()
    waiter = b.task_by_id("tw5")
    text, _ = views.gantt_link_frame(b, False, waiter, b.task_by_id("tm3"), kg_board.TODAY,
                                     w, h, "r", set())
    assert _label(text.plain.split("\n")[2], w) == "selected task ▸"
    text, _ = views.gantt_link_frame(b, False, waiter, None, kg_board.TODAY, w, h, "r", set())
    assert _label(text.plain.split("\n")[2], w) == ""


def test_TC_1701_gantt_at_48_columns_cuts_as_painted():
    """TC-1701 (a), the 16-cell label at 48 columns: `selected task ▸` fits
    whole; `selected: no dates` is cut by `fit` (accepted)."""
    b = kg_board.build()
    assert _label(_gantt_rows(b, "tw3", 48, 20)[2], 48) == "selected task ▸"
    assert _label(_gantt_rows(b, "ta5", 48, 20)[2], 48) == "selected: no d…"


# --------------------------------------------------------------------------- #
# the presentation, renderer level
# --------------------------------------------------------------------------- #
def _present_label(b, cursor, w, h):
    row = views.render_present(b, pb.PROJECT_ID, cursor, pb.TODAY, w, h).plain.split("\n")[2]
    return row[:views._present_cols(w, w >= 100)[0]].strip()


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1701_present_follows_the_same_rule(tmp_path, w, h):
    """TC-1701 (a), presentation: the oracle cursor → `selected task ▸`; a
    whole-window echo → its own dates; a dateless cursor → `selected: no
    dates`; no open task, so no cursor → blank (it was the scale)."""
    b = pb.build(tmp_path / "board.json")
    assert _present_label(b, pb.CURSOR, w, h) == "selected task ▸"
    b.task_by_id("tw6").start_date = "2026-09-01"
    assert _present_label(b, "tw6", w, h) == "Sep 1 → Oct 14 ▸"
    nodate = b.task_by_id("tw6")
    nodate.start_date = nodate.due_date = None
    assert _present_label(b, "tw6", w, h) == "selected: no dates"
    for t in b.tasks:
        if t.project_id == pb.PROJECT_ID:
            t.phase = "Done"
    assert _present_label(b, None, w, h) == ""


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1701_present_every_task_hidden_is_blank(tmp_path, w, h):
    """TC-1701 (a), presentation empty boundary: every task hidden from the
    presentation (the `space` route) leaves no cursor — the label is blank."""
    b = pb.build(tmp_path / "board.json")
    for t in b.tasks:
        if t.project_id == pb.PROJECT_ID:
            t.show_in_present = False
    assert views.present_tasks(b, pb.PROJECT_ID)[0] == []
    assert _present_label(b, None, w, h) == ""


# --------------------------------------------------------------------------- #
# layer 0 — the one function, every branch
# --------------------------------------------------------------------------- #
def test_TC_1701_the_label_function_branches():
    """TC-1701 layer 0: `_gantt_tick_label` over each branch — fits, does not
    fit, no date, no selection — exact text, tone and width."""
    sel = object()
    echo = ({}, "over", [], "Sep 24 → Sep 28")
    fits = views._gantt_tick_label(sel, echo, {"echo_label": None}, 20)
    assert fits == views.c(" " * 4 + "selected task ▸" + " ", "over", bold=True)
    long_ = views._gantt_tick_label(sel, echo, {"echo_label": "Sep 24 → Sep 28"}, 30)
    assert long_ == views.c(" " * 12 + "Sep 24 → Sep 28 ▸" + " ", "over", bold=True)
    assert views._gantt_tick_label(sel, None, {"echo_label": None}, 20) == views.c(
        " " + "selected: no dates" + " ", "dim")
    assert views._gantt_tick_label(None, None, {"echo_label": None}, 20) == ""


def test_TC_1701_the_scale_label_is_gone():
    """TC-1701 (c): the scale label's function no longer exists."""
    assert not hasattr(views, "_gantt_scale_label")


# --------------------------------------------------------------------------- #
# the sweep — no frame ever paints the scale
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("w, h", [(118, 30), (80, 24), (60, 20), (48, 20)])
def test_TC_1701_no_gantt_frame_paints_the_scale(w, h):
    """TC-1701 (b): every visible task of the oracle board as the selection,
    and none, and link mode with three candidates and none — no row of any
    frame holds the scale text."""
    b = kg_board.build()
    sels = [t.id for t in b.visible_tasks(False)] + [None]
    assert len(sels) == 29
    label_w = views.gantt_columns(w)[0]
    for sel in sels:
        rows = _gantt_rows(b, sel, w, h)
        assert len(rows) == h and re.search(r"\d", rows[2][label_w:]), (sel, rows[2])
        for i, row in enumerate(rows):
            assert not SCALE_TEXT.search(row), (sel, i, row)
    waiter = b.task_by_id("tw5")
    for cand in ("tm3", "td2", "ta1", None):
        text, _ = views.gantt_link_frame(b, False, waiter, cand and b.task_by_id(cand),
                                         kg_board.TODAY, w, h, "r", set())
        for i, row in enumerate(text.plain.split("\n")):
            assert not SCALE_TEXT.search(row), ("link", cand, i, row)


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1701_no_present_frame_or_export_paints_the_scale(tmp_path, w, h):
    """TC-1701 (b): every open task as the cursor, a dateless cursor and no
    cursor — no row of the frame and nothing in its `x` SVG holds the scale
    text."""
    b = pb.build(tmp_path / "board.json")
    open_t, _ = views.present_tasks(b, pb.PROJECT_ID)
    cases = [t.id for t in open_t]
    assert len(cases) >= 5

    def check(cursor, tag):
        text = views.render_present(b, pb.PROJECT_ID, cursor, pb.TODAY, w, h)
        rows = text.plain.split("\n")
        label_w = views._present_cols(w, w >= 100)[0]
        assert "today" in rows[1] and re.search(r"\d", rows[2][label_w:]), (tag, rows[2])
        for i, row in enumerate(rows):
            assert not SCALE_TEXT.search(row), (tag, i, row)
        svg = _svg_text(views.save_present_svg(text, tmp_path / f"{tag}.svg", w, h))
        assert "PRESENT" in svg and "Redesign" in svg, "probe cannot read the SVG"
        assert not SCALE_TEXT.search(svg), tag

    for tid in cases:
        check(tid, tid)
    nodate = b.task_by_id(cases[0])
    nodate.start_date = nodate.due_date = None
    check(nodate.id, "nodate")
    for t in b.tasks:
        if t.project_id == pb.PROJECT_ID:
            t.phase = "Done"
    check(None, "none")


# --------------------------------------------------------------------------- #
# AT-1701 — the shipped surface: keys and board files only
# --------------------------------------------------------------------------- #
class _Today(kg_board.TODAY.__class__):
    @classmethod
    def today(cls):
        return kg_board.TODAY


@pytest.fixture
def frozen(monkeypatch):
    from taskboard import models
    monkeypatch.setattr(views, "date", _Today)
    monkeypatch.setattr(app_mod, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)


def _app(tmp_path, b):
    b.path = Path(tmp_path / "board.json")
    b.save()
    return TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)


def _rows(widget) -> list[str]:
    return str(widget.render()).split("\n")


def _no_scale(rows, tag):
    for i, row in enumerate(rows):
        assert not SCALE_TEXT.search(row), (tag, i, row)


@pytest.mark.parametrize("size", [(118, 31), (80, 25)])
async def test_AT_1701_the_tick_row_names_the_selection(tmp_path, frozen, size):
    """AT-1701 (HLR-1701) arms 1-3 and 5, keys only: `3` — the app selects the
    first drawn task — the tick row's label reads `selected task ▸`; `L` (link
    mode) names its candidate the same way; `esc`, `/` `Daily` `enter` — the
    search keeps one open task and the app selects it: the label still names
    the selection; `/` `zzqx` `enter` — a query no task holds: nothing drawn,
    nothing selected, the label is blank and the month row still holds
    `today`; a fresh run presses `R` — the presentation's tick row reads
    `selected task ▸`. No painted row of any arm holds the scale text. RED on
    the base tree: the label was the scale."""
    w = size[0]
    app = _app(tmp_path, kg_board.build())
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        rows = _rows(app.query_one("#board"))
        assert rows[2].lstrip().startswith("selected task ▸"), rows[2]
        _no_scale(rows, "gantt")
        await pilot.press("L")
        await pilot.pause()
        link = _rows(app.screen.query_one("#glink-frame"))
        assert link[2].lstrip().startswith("selected task ▸"), link[2]
        _no_scale(link, "link")
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("slash")
        await pilot.pause()
        await pilot.press(*"Daily")
        await pilot.press("enter")
        await pilot.pause()
        rows = _rows(app.query_one("#board"))
        assert rows[1].startswith("/ Daily") and "1/28 tasks" in rows[1], rows[1]
        assert any(r.startswith("  Daily revenue mo") for r in rows), rows
        tick = rows[3 + 1]                     # header, bar (2 rows), month row
        assert tick.lstrip().startswith("selected task ▸"), tick
        _no_scale(rows, "search-one")
        await pilot.press("slash")
        await pilot.pause()
        for _ in range(5):
            await pilot.press("backspace")
        await pilot.press(*"zzqx")
        await pilot.press("enter")
        await pilot.pause()
        rows = _rows(app.query_one("#board"))
        ruler = next(i for i, r in enumerate(rows) if "today" in r)
        assert rows[ruler + 1][:views.gantt_columns(w)[0]].strip() == "", rows[ruler + 1]
        _no_scale(rows, "search")
    app = _app(tmp_path, kg_board.build())
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("R")
        await pilot.pause()
        frame = _rows(app.screen.query_one("#present-frame"))
        assert frame[2].lstrip().startswith("selected task ▸"), frame[2]
        _no_scale(frame, "present")


@pytest.mark.parametrize("size", [(118, 31), (80, 25)])
async def test_AT_1701_a_board_with_no_task_has_a_blank_label(tmp_path, frozen, size):
    """AT-1701 (HLR-1701) arm 4, empty boundary: a board file with projects and
    no task — nothing can be selected — `3` paints the ruler (`today` on the
    month row) with a blank tick label and no scale text anywhere."""
    b = kg_board.build()
    b.tasks.clear()
    app = _app(tmp_path, b)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        rows = _rows(app.query_one("#board"))
        assert "today" in rows[1], rows[1]
        assert rows[2][:views.gantt_columns(size[0])[0]].strip() == "", rows[2]
        _no_scale(rows, "empty")
