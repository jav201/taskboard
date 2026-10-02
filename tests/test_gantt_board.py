"""The whole-board gantt (G-A) and its date ruler (AX-2).

Batch 2026-10-02-batch-01 · HLR-101 to HLR-107 · AT-101 to AT-105, AT-108, AT-109
· TC-101 to TC-116.

Field report, measured on the board the operator judged the prototypes on
(`tests/kg_board.py`): the shipped gantt hid 9 rows at 118x30 ("+9 not shown",
a whole project invisible), its cursor walked 7 tasks it did not draw, and the
axis under the field dropped October — today's month. The operator's verdicts:
G-A (a window fitted to the open work, projects folding, done folding to `✓n`,
one due chip, a dependency gutter) and AX-2 (months and day numbers on two rows
at the top, answering for the selection).

ATs drive the running app (`App.run_test`) at TERMINAL sizes and read the board
widget; TCs drive the renderer and its helpers at PANEL sizes, which is what
the verdict frames were captured at. The app reads `date.today()`, so the app
tests freeze the calendar on the oracle board's TODAY.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

import pytest
from rich.cells import cell_len
from rich.markup import MarkupError

import kg_board
from kg_board import TODAY
from taskboard import app as app_mod
from taskboard import views
from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task, critical_chain
from taskboard.views import (GANTT_SCALES, GanttAxis, gantt_axis, gantt_cadence,
                             gantt_columns, gantt_dep_mark, gantt_due_chip, gantt_echo,
                             gantt_plan, gantt_window, legend_entries, nav_model,
                             render_gantt)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def render(b, w, h, sel="tw3", **kw):
    lm: dict = {}
    text = render_gantt(b, False, sel, TODAY, width=w, height=h, line_map=lm, **kw)
    return text.plain.split("\n"), lm, text


def field(line: str, w: int) -> str:
    label_w, _chip, field_w = gantt_columns(w)
    return line[label_w + 1:label_w + 1 + field_w]


def plan_axis(b, w, h, sel="tw3", focus=None):
    _l, _c, field_w = gantt_columns(w)
    groups = gantt_plan(b, False, sel, TODAY, h - 3, focus)
    return groups, gantt_axis(field_w, TODAY, *gantt_window(groups, TODAY))


# --------------------------------------------------------------------------- #
# the app, on the oracle board, with the calendar frozen on its TODAY
# --------------------------------------------------------------------------- #
class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def frozen(monkeypatch):
    from taskboard import models
    monkeypatch.setattr(views, "date", _Today)
    monkeypatch.setattr(app_mod, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)     # the 20-day auto-archive sweep


def _app(tmp_path, b=None):
    b = b or kg_board.build(tmp_path / "board.json")
    b.path = Path(tmp_path / "board.json")
    b.save()
    return TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)


def painted(app) -> list[str]:
    return str(app.query_one("#board").render()).split("\n")


def viewport(app):
    return app.query_one("#viewport")


async def _open_gantt(pilot, app, sel=None):
    await pilot.pause()
    await pilot.press("3")
    await pilot.pause()
    if sel is not None:
        app.selected_task_id = sel
        app.refresh_view()
        await pilot.pause()


# =========================================================================== #
# AT-101 — every project on screen, folded where rows run out (US-101)
# =========================================================================== #
@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_AT_101_the_whole_board_is_on_screen(tmp_path, frozen, size):
    """AT-101 (HLR-101, HLR-102). At the operator's two sizes every project is
    painted in the board panel — its name on a `▾`/`▸` span row — and nothing
    says `not shown`. RED on the base tree: `+9 not shown` (P-1)."""
    app = _app(tmp_path)
    async with app.run_test(size=size) as pilot:
        await _open_gantt(pilot, app, "tw3")
        out = painted(app)
        spans = [l for l in out if l.startswith(("▾", "▸"))]
        for name in ("Website Re", "Mobile App", "API Platfo", "Data Wareh", "Ops & Secu"):
            assert any(name in l for l in spans), (name, spans)
        assert not any("not shown" in l for l in out)
        assert not any("Design homepage" in l for l in out), "done work drew a row"


# =========================================================================== #
# AT-102 — the cursor walks what is drawn, and it is always on screen (US-101)
# =========================================================================== #
@pytest.mark.parametrize("size", [(80, 24), (118, 30)])
async def test_AT_102_down_walks_the_drawn_open_work(tmp_path, frozen, size):
    """AT-102 (HLR-104, C-12). From the first task row, `down` until the end:
    after EVERY press the selected task is painted in reverse on a row the
    viewport shows (the consumer of `line_map`) and the ruler is still rows 1–2;
    the walk visits every open task exactly once and nothing else; one more
    `down` at the end does nothing. RED on the base tree: the walk reaches done
    tasks and rows the view does not draw."""
    app = _app(tmp_path)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        opened = {t.id for t in app.board.tasks if not app.board.is_done(t) and not t.archived}
        await pilot.press("3")
        await pilot.pause()
        for _ in range(40):
            await pilot.press("up")
        await pilot.pause()
        seen = [app.selected_task_id]
        for _ in range(len(opened) - 1):
            await pilot.press("down")
            await pilot.pause()
            sel = app.selected_task_id
            seen.append(sel)
            text = app.query_one("#board").render()
            plain = text.plain.split("\n")
            title = app.board.task_by_id(sel).title[:8]
            rows = [i for i, ln in enumerate(plain)
                    if title in ln and not ln.startswith(("▾", "▸"))]
            assert len(rows) == 1, (sel, "the selected task is not painted once")
            row = rows[0]
            vp = viewport(app)
            assert vp.scroll_offset.y <= row < vp.scroll_offset.y + vp.size.height, sel
            line_start = sum(len(x) + 1 for x in plain[:row])
            at = text.plain.index(title, line_start)
            assert any(getattr(s.style, "reverse", False) or "reverse" in str(s.style)
                       for s in text.spans if s.start <= at < s.end), (
                sel, "not painted as selected")
            out = painted(app)
            assert re.search(r"(September|October|November|Sep|Oct|Nov)", out[1]), out[1]
        assert len(seen) == len(set(seen)) and set(seen) == opened, seen
        await pilot.press("down")
        await pilot.pause()
        assert app.selected_task_id == seen[-1], "the end of the list is not a no-op"


# =========================================================================== #
# AT-103 — one due chip per row, dependency marks in their own column (US-101)
# =========================================================================== #
async def test_AT_103_chips_and_the_dependency_gutter(tmp_path, frozen):
    """AT-103 (HLR-103). Read off the painted rows: the late task ends `▲2d`,
    the one due today `today`, the undated one `no due`, a future one `Oct 6`;
    `↳` sits after the whole title, exactly on the drawn tasks waiting on open
    work. RED on the base tree: a `start → due` pair and `└─►`."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 34)) as pilot:
        await _open_gantt(pilot, app, "tw3")
        out = painted(app)

        def row(title):
            return next(l for l in out if title in l)

        assert row("Fix checkout 500 error").rstrip().endswith(" ▲2d")
        assert row("Review pull requests").rstrip().endswith(" today")
        assert row("Plan Q4 roadmap").rstrip().endswith(" no due")
        assert row("Optimize image assets").rstrip().endswith(" Oct 6")
        marked = set()
        for t in app.board.tasks:
            line = next((l for l in out if t.title in l), None)
            if line is not None and "↳" in line:
                assert line.index("↳") > line.index(t.title) + len(t.title), line
                marked.add(t.title)
        assert marked == {"Optimize image assets", "Launch new homepage",
                          "Add push notifications", "Offline sync",
                          "Beta release to testers", "SDK regeneration",
                          "Deprecate v1 endpoints"}
        assert "└─►" not in "\n".join(out)


# =========================================================================== #
# AT-104 — the ruler at the top; no tick lost but under the echo (US-102)
# =========================================================================== #
async def test_AT_104_the_ruler_is_at_the_top(tmp_path, frozen):
    """AT-104 (HLR-105, HLR-106). With nothing selected, painted rows 1–2 are
    the month row (names, `┃` between months, today's `30`) and the day row
    (its label naming the cadence and scale; Monday numbers seven days apart,
    none touching); the last row is no axis. RED on the base tree: rows 1–2
    are project and task rows."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 34)) as pilot:
        await _open_gantt(pilot, app, None)
        app.selected_task_id = None
        app.refresh_view()
        await pilot.pause()
        out = painted(app)
        assert "September 2026" in out[1] and "October" in out[1] and "┃" in out[1]
        assert re.search(r"\b30\b", out[1])
        assert "Mondays · 1 cell = 1 day" in out[2]
        days = [int(x) for x in re.findall(r"(?<!\S)(\d{1,2})(?!\S)", out[2][30:])]
        assert len(days) >= 8, out[2]
        for a, b in zip(days, days[1:]):
            assert b - a == 7 or (a > 20 and b <= 7), (days, out[2])
        assert not re.search(r"\d\d\d", out[2][30:]), "two labels touch"
        assert not re.search(r"\btoday\b.*\b(SEP|OCT|NOV)\b", out[-1])


def assert_no_drop(b, w, h, sel):
    """THE NO-DROP LAW, from its statement: the ticks are recomputed from the
    window's days and the cadence rule, independently of the renderer; every
    one is drawn on its cell (ending on it at the right edge) unless it
    overlaps the echo zone (± 1 cell); labels never touch."""
    lines, _lm, _t = render(b, w, h, sel)
    groups, ax = plan_axis(b, w, h, sel)
    day = field(lines[2], w)
    cpd = 1 / ax.k
    days = ax.window_days()
    if cpd >= 3:
        pred = lambda d: True                                    # noqa: E731
    elif cpd >= 1:
        pred = lambda d: d.weekday() == 0                        # noqa: E731
    else:
        xs = [ax.cell(d) for d in days if d.day in (1, 15)]
        if all(b2 - a >= 3 for a, b2 in zip(xs, xs[1:])):
            pred = lambda d: d.day in (1, 15)                    # noqa: E731
        else:
            pred = lambda d: d.day == 1                          # noqa: E731
    echo = set()
    if sel is not None:
        spec = gantt_echo(b.task_by_id(sel), b, ax, TODAY)
        if spec is not None:
            cells = set(spec[0])
            for opt in spec[2]:
                for p, txt in opt:
                    cells |= set(range(p, p + len(txt)))
            echo = {x + d for x in cells for d in (-1, 0, 1)}
    ticks = [(d, ax.cell(d)) for d in days if pred(d)]
    assert ticks, "vacuous: the window schedules no tick"
    spans = []
    for d, x in ticks:
        lab = str(d.day)
        p = x if x + len(lab) <= ax.w else ax.w - len(lab)
        if day[p:p + len(lab)] == lab:
            spans.append((p, p + len(lab)))
        else:
            assert sel is not None and set(range(p, p + len(lab))) & echo, (
                f"{w}x{h} k={ax.k}: tick {d} dropped at cell {x}: {day!r}")
    for (a0, a1), (b0, _b1) in zip(sorted(spans), sorted(spans)[1:]):
        assert b0 >= a1 + 1, f"labels touch at {a1}/{b0}: {day!r}"
    months = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
    assert all(len(n) <= 2 for n in re.findall(rf"(?:{months}) (\d+)", day)), (
        f"a tick touches the echo's date label: {day!r}")
    assert not re.search(rf"\d(?:{months})", day), day
    return ax.k, len(ticks)


def _span_board(days: int) -> Board:
    """One project whose open work spans `days`, so the window lands on the
    scale that span asks for at a given field width."""
    p = Project("Span", "sky", "on_track", start_date=iso(-2), due_date=iso(days - 4),
                id="pspan")
    t = Task("reach", p.id, "Doing", start_date=iso(-2), due_date=iso(days - 4), id="tsp")
    return Board([p], [t], Path("never-saved.json"), {}, ["Backlog", "Doing", "Done"])


def test_TC_113_no_drop_law_over_every_scale_and_width():
    """TC-113 (HLR-106, LLR-102.2). Panel widths 60..160 step 4, one board per
    scale (sized from the field it lands in), with and without a selection:
    the set of scales reached is all five, and each arm checks ≥ 1 tick."""
    reached = set()
    for w in range(60, 161, 4):
        _l, _c, fw = gantt_columns(w)
        for k in GANTT_SCALES:
            span = max(1, int(fw * k) - 4)
            b = _span_board(span)
            for sel in (None, "tsp"):
                got_k, n = assert_no_drop(b, w, 24, sel)
                reached.add(got_k)
                assert n >= 1
    assert reached == set(GANTT_SCALES), reached


def test_TC_113_a_tick_never_touches_the_echo_label():
    """TC-113 (HLR-106, G10's arm). A selection due on a Monday at one cell per
    day prints its due label `Oct 5` ending one cell before the next Monday's
    tick: that tick must yield (it is inside the echo zone) rather than print
    `Oct 512`. RED: the tick placement without its one-cell gap."""
    p = Project("Mon", "sky", "on_track", start_date=iso(-20), due_date=iso(40), id="pm")
    t = Task("mon", "pm", "Doing", start_date="2026-09-28", due_date="2026-10-05", id="tm")
    b = Board([p], [t, Task("late", "pm", "Doing", due_date=iso(38), id="tl")],
              Path("never.json"), {}, ["A", "Doing", "B"])
    k, _n = assert_no_drop(b, 118, 30, "tm")
    assert k == 1
    lines, _lm, _t = render(b, 118, 30, "tm")
    assert "Oct 5" in lines[2] and not re.search(r"Oct 5\d", lines[2]), lines[2]


# =========================================================================== #
# AT-105 — the ruler answers for the selection (US-102)
# =========================================================================== #
async def test_AT_105_the_echo_follows_the_selection(tmp_path, frozen):
    """AT-105 (HLR-107, C-10: a non-default selection, then another). Walking
    to `tw3` brackets Sep 24 → Sep 28 on the day row and marks Website
    Redesign's due on the month row; walking on to `tm4` moves both. RED: an
    echo that ignores the selection keeps `Sep 24 ⟦` on the day row."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 34)) as pilot:
        await _open_gantt(pilot, app, "tw2")
        while app.selected_task_id != "tw3":
            await pilot.press("down")
            await pilot.pause()
        out = painted(app)
        assert re.search(r"Sep 24 ⟦━*⟧ Sep 28", out[2]), out[2]
        assert "◆ dates · Website Redesign" in out[1] and out[1].count("◆") == 2
        while app.selected_task_id != "tm4":
            await pilot.press("down")
            await pilot.pause()
        out = painted(app)
        assert "Sep 24" not in out[2]
        assert re.search(r"Oct 10 ⟦━*⟧ Oct 28", out[2]), out[2]
        assert "◆ dates · Mobile App" in out[1]


# =========================================================================== #
# AT-108 — a done selection never strands the cursor (US-101)
# =========================================================================== #
async def test_AT_108_entering_on_a_done_task_lands_on_drawn_work(tmp_path, frozen):
    """AT-108 (HLR-104, LLR-101.9). Enter the gantt with `tw1` (done) selected:
    the selection lands on `tw2`, the open task after it in Website Redesign's
    draw order, and `down` moves. RED on the base tree: `tw1` stays selected
    and `down` does nothing (P-9)."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 34)) as pilot:
        await pilot.pause()
        app.selected_task_id = "tw1"
        await pilot.press("3")
        await pilot.pause()
        assert app.selected_task_id == "tw2"
        await pilot.press("down")
        await pilot.pause()
        assert app.selected_task_id == "tw3"


async def test_AT_113_finishing_a_task_moves_one_row_and_an_extra_key_is_local(
        tmp_path, frozen):
    """AT-113 (HLR-104, UX-15). `]` until `tw3` is done: it leaves the gantt (`✓2` on
    its project) and the cursor moves to `tw4`, the open task that followed it
    — one row away. One more `]` advances THAT task, and only that task: no
    distant task changes phase."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 34)) as pilot:
        await _open_gantt(pilot, app, "tw3")
        before = {t.id: t.phase for t in app.board.tasks}
        while app.board.task_by_id("tw3").phase != "Done":
            await pilot.press("]")
            await pilot.pause()
        assert app.selected_task_id == "tw4"
        assert any("Website Redesign" in l and "✓2" in l for l in painted(app))
        await pilot.press("]")
        await pilot.pause()
        after = {t.id: t.phase for t in app.board.tasks}
        changed = {k for k in after if after[k] != before[k]}
        assert changed == {"tw3", "tw4"}, changed
        assert after["tw4"] == "Doing"
        await pilot.press("down")
        await pilot.pause()
        assert app.selected_task_id == "tw5"


# =========================================================================== #
# AT-109 — the operator's inputs, each driven off its default (US-101, C-10a)
# =========================================================================== #
async def test_AT_109_show_archived_grows_the_rest_count(tmp_path, frozen):
    """AT-109 (HLR-101, C-10a), `v`: an archived finished task in Website Redesign is counted —
    `✓1` becomes `✓2` — and is never drawn as a row (D2)."""
    b = kg_board.build(tmp_path / "board.json")
    b.tasks.append(Task("Archived launch checklist", "pweb", "Done", start_date=iso(-30),
                        due_date=iso(-25), archived=True, id="tw7"))
    app = _app(tmp_path, b)
    async with app.run_test(size=(118, 34)) as pilot:
        await _open_gantt(pilot, app, "tw3")
        web = lambda: next(l for l in painted(app) if "Website Redesign" in l  # noqa: E731
                           and l.startswith(("▾", "▸")))
        assert "✓1" in web()
        await pilot.press("v")
        await pilot.pause()
        assert "✓2" in web()
        assert not any("Archived launch" in l for l in painted(app))


async def test_AT_110_focus_narrows_to_one_group_and_its_window(tmp_path, frozen):
    """AT-110 (HLR-101, C-10a), `F`: focusing Website Redesign draws only that group and the
    header says so; the window fits it (Sep 25 to Oct 16), so the ruler no
    longer reaches November, as the whole board's (to Dec 1) does."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 34)) as pilot:
        await _open_gantt(pilot, app, "tw3")
        assert "November" in painted(app)[1]
        await pilot.press("F")
        await pilot.pause()
        out = painted(app)
        spans = [l for l in out if l.startswith(("▾", "▸"))]
        assert len(spans) == 1 and "Website Redesign" in spans[0]
        assert "(focused: Website Redesign)" in out[0]
        assert "November" not in out[1] and "October" in out[1]


async def test_AT_111_a_filter_narrows_nav_and_keeps_the_ruler(tmp_path, frozen):
    """AT-111 (HLR-101, C-10a), `/`: filtering on `API` leaves only matching open work to walk
    — API Platform's and `Rotate API keys` — and the ruler sits under the
    two-row filter bar (rows 3–4)."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 34)) as pilot:
        await _open_gantt(pilot, app, "ta1")
        await pilot.press("/")
        await pilot.pause()
        for ch in "API":
            await pilot.press(ch)
        await pilot.press("enter")
        await pilot.pause()
        for _ in range(20):
            await pilot.press("up")
        await pilot.pause()
        seen = {app.selected_task_id}
        for _ in range(20):
            await pilot.press("down")
            await pilot.pause()
            seen.add(app.selected_task_id)
        want = {t.id for t in app.board.tasks
                if not app.board.is_done(t) and ("API" in t.title or t.project_id == "papi")}
        assert seen == want, (seen, want)
        out = painted(app)
        assert "September 2026" in out[3] or "October" in out[3], out[3]


# =========================================================================== #
# TC-101 … TC-111 — the G-A seats
# =========================================================================== #
def test_TC_101_the_axis_takes_the_smallest_scale_that_fits():
    """TC-101 (LLR-101.1). Field 10 cells: a need of 1..5 days → 0.5, 6..10 →
    1, 11..20 → 2, 21..30 → 3, more → 7 (Monday-aligned). Spare cells buy past
    context back to `ctx` and no further. RED: the largest fitting scale."""
    d = date(2026, 9, 30)                     # a Wednesday
    for need, k in ((1, 0.5), (5, 0.5), (6, 1), (10, 1), (11, 2), (20, 2),
                    (21, 3), (30, 3), (31, 7), (70, 7)):
        ax = gantt_axis(10, d, d, d + timedelta(days=need - 1), d)
        assert ax.k == k, (need, ax.k)
    assert gantt_axis(10, d, d, d + timedelta(days=60), d).start.weekday() == 0
    ax = gantt_axis(10, d, d, d + timedelta(days=5), d - timedelta(days=2))
    assert ax.start == d - timedelta(days=2)
    ax = gantt_axis(10, d, d, d + timedelta(days=5), d - timedelta(days=10))
    assert ax.start == d - timedelta(days=4)
    ax = GanttAxis(d, 0.5, 10, d)
    assert (ax.cell(d), ax.end_cell(d), ax.cell(d + timedelta(days=1))) == (0, 1, 2)


def test_TC_102_the_window_is_fitted_to_the_open_work():
    """TC-102 (LLR-101.2). Oracle board: lo Sep 23 (earliest open due −2),
    hi Dec 1 (Data Warehouse's due Nov 29 +2); start Sep 14 at 118 columns.
    RED: without project dues `hi` stops at the latest task due."""
    b = kg_board.build()
    groups, ax = plan_axis(b, 118, 30)
    lo, hi, _ctx = gantt_window(groups, TODAY)
    assert (lo, hi) == (date(2026, 9, 23), date(2026, 12, 1))
    assert ax.start == date(2026, 9, 14) and ax.k == 1
    _g, ax80 = plan_axis(b, 80, 24)
    assert ax80.k == 2
    # a project's committed due beyond its tasks' dues moves `hi` (G2's arm: on the
    # oracle board the latest task due IS its project's due, so it cannot tell)
    p = Project("Late due", "sky", "on_track", start_date=iso(-5), due_date=iso(40), id="pl")
    one = Board([p], [Task("t", "pl", "Doing", start_date=iso(-1), due_date=iso(5), id="t")],
                Path("never.json"), {}, ["A", "Doing", "B"])
    lo, hi, _ = gantt_window(gantt_plan(one, False, None, TODAY, 20), TODAY)
    assert hi == TODAY + timedelta(days=42), hi
    empty = Board([], [], Path("never.json"), {}, ["A", "B"])
    lo, hi, _ = gantt_window(gantt_plan(empty, False, None, TODAY, 20), TODAY)
    assert (lo, hi) == (TODAY - timedelta(days=2), TODAY + timedelta(days=2))


def _folds(b, w, h, sel="tw3"):
    lines, _lm, _t = render(b, w, h, sel)
    return [l for l in lines if l.startswith(("▾", "▸"))]


def test_TC_103_the_fold_rule_matches_the_verdict_frames():
    """TC-103 (LLR-101.3, HLR-102). The frames' own strings at both sizes."""
    b = kg_board.build()
    big = _folds(b, 118, 30)
    assert [l[:31] for l in big if l.startswith("▸")] == ["▸ Data Warehouse    4 open ✓1  "]
    assert len([l for l in big if l.startswith("▾")]) == 4
    small = _folds(b, 80, 24)
    assert [l[:20] for l in small if l.startswith("▸")] == ["▸ Mobile App      5 ",
                                                           "▸ Data Warehouse  4 "]


def test_TC_103_a_group_that_does_not_fit_is_skipped_not_the_end():
    """TC-103 (Q-5). Body 8: two groups leave 6 rows; the most-late group needs
    10 and is skipped; the next needs 2 and unfolds. RED: stopping at the
    first group that does not fit leaves the small one folded."""
    ps = [Project("Big", "sky", id="pb"), Project("Small", "lime", id="ps")]
    ts = [Task(f"b{i}", "pb", "Doing", due_date=iso(-1), id=f"b{i}") for i in range(10)]
    ts += [Task("s0", "ps", "Doing", due_date=iso(-1), id="s0"),
           Task("s1", "ps", "Doing", due_date=iso(5), id="s1")]
    b = Board(ps, ts, Path("never.json"), {}, ["Backlog", "Doing", "Done"])
    plan = {g.project.name: g.unfolded for g in gantt_plan(b, False, None, TODAY, 8)}
    assert plan == {"Big": False, "Small": True}


def test_TC_103_a_late_tie_unfolds_the_earlier_due_first_and_height_0_unfolds_all():
    """TC-103. Equal late counts → earliest open due first; `height = 0` is an
    unbounded render: every group unfolds."""
    ps = [Project("Later", "sky", id="pl"), Project("Sooner", "lime", id="pn")]
    ts = [Task("l0", "pl", "Doing", due_date=iso(9), id="l0"),
          Task("l1", "pl", "Doing", due_date=iso(9), id="l1"),
          Task("n0", "pn", "Doing", due_date=iso(2), id="n0"),
          Task("n1", "pn", "Doing", due_date=iso(2), id="n1")]
    b = Board(ps, ts, Path("never.json"), {}, ["Backlog", "Doing", "Done"])
    plan = {g.project.name: g.unfolded for g in gantt_plan(b, False, None, TODAY, 4)}
    assert plan == {"Later": False, "Sooner": True}
    lines, lm, _t = render(kg_board.build(), 118, 0, "tw3")
    assert not any(l.startswith("▸") for l in lines) and len(lm) == 25


def test_TC_104_the_due_chip():
    """TC-104 (LLR-101.4). Four forms, exact width, no zero-padding."""
    assert gantt_due_chip(iso(-3), TODAY, 7) == views.c("    ▲3d", "over")
    assert views._strip(gantt_due_chip(iso(0), TODAY, 6)) == " today"
    assert views._strip(gantt_due_chip("2026-10-06", TODAY, 7)) == "  Oct 6"
    assert views._strip(gantt_due_chip(None, TODAY, 6)) == "no due"
    assert views._strip(gantt_due_chip("not-a-date", TODAY, 6)) == "no due"
    for w in (6, 7):
        for due in (iso(-30), iso(0), iso(5), None):
            assert cell_len(views._strip(gantt_due_chip(due, TODAY, w))) == w


def test_TC_105_the_dependency_mark():
    """TC-105 (LLR-101.5). over: starts before an open dependency is due; bold
    bright: on the critical chain; mut: otherwise; blank: nothing open waited
    on (done or missing); a task with no start is never `over`."""
    p = Project("P", "sky", id="p")
    dep = Task("dep", "p", "Doing", due_date=iso(5), id="dep")
    done = Task("done", "p", "Done", due_date=iso(5), id="dn")
    early = Task("early", "p", "Doing", start_date=iso(2), due_date=iso(9),
                 depends_on=["dep"], id="e")
    later = Task("later", "p", "Doing", start_date=iso(6), due_date=iso(9),
                 depends_on=["dep"], id="l")
    nostart = Task("nostart", "p", "Doing", due_date=iso(9), depends_on=["dep"], id="ns")
    on_done = Task("on_done", "p", "Doing", start_date=iso(1), depends_on=["dn"], id="od")
    missing = Task("missing", "p", "Doing", depends_on=["nope"], id="m")
    same_day = Task("same", "p", "Doing", start_date=iso(5), depends_on=["dep"], id="sd")
    b = Board([p], [dep, done, early, later, nostart, on_done, missing, same_day],
              Path("never.json"), {}, ["Backlog", "Doing", "Done"])
    assert gantt_dep_mark(early, b, set()) == views.c("↳", "over")
    assert gantt_dep_mark(later, b, set()) == views.c("↳", "mut")
    assert gantt_dep_mark(later, b, {"l"}) == views.c("↳", "bright", bold=True)
    assert gantt_dep_mark(nostart, b, set()) == views.c("↳", "mut")
    assert gantt_dep_mark(same_day, b, set()) == views.c("↳", "mut")
    assert gantt_dep_mark(on_done, b, set()) == " "
    assert gantt_dep_mark(missing, b, set()) == " "


def test_TC_106_nav_is_the_plans_open_work_and_every_selection_is_drawn():
    """TC-106 (LLR-101.6). Nav == the plan's open ids in order (25 on the oracle
    board, no rest work); selecting each in turn at panel 80x24 draws it."""
    b = kg_board.build()
    nav = nav_model("gantt", b, False, TODAY, 80, 24)[0]
    groups = gantt_plan(b, False, None, TODAY, 21)
    assert nav == [t.id for g in groups for t in g.open] and len(nav) == 25
    assert not {"tw1", "tm1", "td1"} & set(nav)
    for tid in nav:
        _lines, lm, _t = render(b, 80, 24, tid)
        assert tid in lm, tid


def test_TC_106_a_tall_group_pages_and_keeps_its_count():
    """TC-106 (UX-9). A 30-task project at panel 80x24: the rows move once per
    page, the selection is always drawn, and the span row keeps `N open`.
    Pages are 19 rows since batch 2026-10-02-batch-02 (HLR-205): the 20th row
    of the room is the `▲ above / ▼ below` hint under the page."""
    p = Project("Tall", "sky", "on_track", start_date=iso(-3), due_date=iso(40), id="pt")
    ts = [Task(f"task {i:02d}", "pt", "Doing", start_date=iso(-2), due_date=iso(i),
               id=f"u{i}") for i in range(30)]
    b = Board([p], ts, Path("never.json"), {}, ["Backlog", "Doing", "Done"])
    tops = []
    for i in range(30):
        lines, lm, _t = render(b, 80, 24, f"u{i}")
        assert f"u{i}" in lm
        tops.append(min(lm, key=lm.get))
        assert "30" in lines[3][:20], lines[3]
    assert tops == ["u0"] * 19 + ["u19"] * 11


def test_TC_106_span_overflow_draws_the_page_holding_the_selection():
    """TC-106 (Q-7, N-4). 30 projects at panel 80x24 (body 21): the drawn
    groups are the page of 19 (`index // 19`) holding the selected one — P19
    to P29 — its task under it, and `+19 not shown` for the rest."""
    ps = [Project(f"P{i:02d}", "sky", "on_track", start_date=iso(-5), due_date=iso(10),
                  id=f"p{i}") for i in range(30)]
    ts = [Task(f"task {i}", f"p{i}", "Doing", start_date=iso(-2), due_date=iso(4),
               id=f"t{i}") for i in range(30)]
    b = Board(ps, ts, Path("never.json"), {}, ["Backlog", "Doing", "Done"])
    lines, lm, _t = render(b, 80, 24, "t29")
    assert "t29" in lm
    assert any(l.startswith("▾ P29") for l in lines)
    assert any("+19 not shown" in l for l in lines)
    assert any(l.startswith("▸ P19") for l in lines)
    assert not any(l.startswith("▸ P18") for l in lines)


def test_TC_108_board_text_is_never_parsed_as_markup():
    """TC-108 (LLR-101.8, S-1, S-2). Hostile names as a project and a task,
    selected and not, and the project focused (the header's seat). The render
    succeeds and paints the payload — or, where a seat clips, its fitted
    prefix and `…`. RED on the base tree: the focused header with `[/]` raises
    `MarkupError`."""
    payloads = ["[bold]x", "[/]", "a[b", "[link=http://e]y[/link]", "x\\",
                "y" * 26 + "[b]" + "z" * 11]
    for pay in payloads:
        p = Project(pay, "sky", "on_track", start_date=iso(-3), due_date=iso(9), id="ph")
        t = Task(pay, "ph", "Doing", start_date=iso(-1), due_date=iso(4), id="th")
        b = Board([p], [t], Path("never.json"), {}, ["Backlog", "Doing", "Done"])
        for sel in ("th", None):
            for focus in (None, "ph"):
                try:
                    lines, _lm, _t = render(b, 118, 30, sel, focus=focus)
                except MarkupError as exc:          # pragma: no cover - the RED
                    pytest.fail(f"{pay!r} sel={sel} focus={focus}: {exc}")
                plain = "\n".join(lines)
                for seat_w in (len(pay), 26, 17):
                    if pay[:seat_w] in plain:
                        break
                else:
                    pytest.fail(f"{pay!r} sel={sel} focus={focus} not painted")


@pytest.mark.parametrize("w", [24, 39, 40, 59, 60, 80, 99, 100, 118, 160])
def test_TC_110_every_row_is_exactly_the_width(w):
    """TC-110 (LLR-101.10). Label + gutter + field + chip == width, from the
    narrowest panel to the widest."""
    for h in (0, 3, 12, 24, 30):
        lines, _lm, _t = render(kg_board.build(), w, h)
        assert {cell_len(l) for l in lines} == {max(24, w)}, (w, h)


def test_TC_110_the_vertical_split():
    """TC-110 (LLR-101.10). 118x30: header, ruler, 26 body rows, legend.
    80x24: header, ruler, 21 body rows, no legend."""
    lines, _lm, _t = render(kg_board.build(), 118, 30)
    assert len(lines) == 30 and "↳ waits on open work" in lines[-1]
    assert len([l for l in lines[3:-1] if l.strip()]) == 26
    lines, _lm, _t = render(kg_board.build(), 80, 24)
    assert len(lines) == 24 and lines[-1].startswith(("  ", "▾", "▸"))
    assert gantt_columns(118) == (30, 7, 79) and gantt_columns(80) == (20, 6, 52)


def test_TC_111_the_group_label_forms():
    """TC-111 (LLR-101.11). Wide: `N open ▲n ✓n`; narrow (< 26): `N ▲n`."""
    big = {l[:31] for l in _folds(kg_board.build(), 118, 30)}
    assert "▾ Website Redesign      ▲2 ✓1  " in big
    assert "▾ Mobile App               ✓1  " in big
    small = {l[:20] for l in _folds(kg_board.build(), 80, 24)}
    assert "▾ Website Redes… ▲2 " in small


# =========================================================================== #
# TC-112 … TC-116 — the AX-2 seats
# =========================================================================== #
def test_TC_112_the_cadence_rule():
    """TC-112 (LLR-102.1). 0.5 → Mondays (2 cells/day); 1 → Mondays; 2, 3 →
    1st/15th; 7 → 1st; a synthetic 1/3 day per cell → daily."""
    d = date(2026, 9, 1)
    got = {k: gantt_cadence(GanttAxis(d, k, 60, d))[0] for k in GANTT_SCALES}
    assert got == {0.5: "Mondays", 1: "Mondays", 2: "1st/15th", 3: "1st/15th", 7: "1st"}
    assert gantt_cadence(GanttAxis(d, 1 / 3, 60, d))[0] == "daily"


def test_TC_114_the_month_row():
    """TC-114 (LLR-102.3). `┃` on every 1st after the first band; names in
    each band ≥ 4 cells; the project's `◆` never covered; today's number lit
    within 2 cells of the today column; a year boundary names January 2027."""
    b = kg_board.build()
    lines, _lm, _t = render(b, 118, 30)
    groups, ax = plan_axis(b, 118, 30)
    month = field(lines[1], 118)
    for x in range(1, ax.w):
        if ax.day(x).month != ax.day(x - 1).month:
            assert month[x] == "┃", (x, month)
    assert month[ax.cell(date(2026, 10, 10))] == "◆"
    p = month.find("30")
    assert p >= 0 and abs(p - ax.tc) <= 2
    xmas = Board([Project("Y", "sky", "on_track", start_date="2026-12-01",
                          due_date="2027-01-20", id="py")],
                 [Task("t", "py", "Doing", start_date="2026-12-01", due_date="2027-01-18",
                       id="ty")], Path("never.json"), {}, ["A", "B"])
    out = render_gantt(xmas, False, None, date(2026, 12, 10), width=118,
                       height=20).plain.split("\n")
    assert "January 2027" in out[1] or "January" in out[1], out[1]


def test_TC_115_the_echo_carries_exact_dates():
    """TC-115 (LLR-102.4). Both dates, a single date, no start, no due; dates
    are exact, never a cell's rounded date (k = 2)."""
    b = kg_board.build()
    ax = GanttAxis(date(2026, 9, 5), 2, 52, TODAY)
    cells, tone, options, full = gantt_echo(b.task_by_id("tw3"), b, ax, TODAY)
    assert full == "Sep 24 → Sep 28" and tone == "over"
    assert [t for _p, t in options[0]] == ["Sep 24", "Sep 28"]
    assert options[1][0][1] == "Sep 24–28"
    one = Task("one", "pweb", "Doing", start_date=iso(3), due_date=iso(3))
    assert gantt_echo(one, b, ax, TODAY)[3] == "◆ Oct 3"
    nostart = Task("ns", "pweb", "Doing", due_date=iso(3))
    assert gantt_echo(nostart, b, ax, TODAY)[3] == "no start · due Oct 3"
    nodue = Task("nd", "pweb", "Doing", start_date=iso(3))
    assert gantt_echo(nodue, b, ax, TODAY)[3] == "starts Oct 3 · no due"
    assert gantt_echo(Task("x", "pweb", "Doing"), b, ax, TODAY) is None


def test_TC_115_the_echo_falls_back_to_the_label_column_untruncated():
    """TC-115 (UX-4). When no slot beside the bracket is free the full text
    replaces the day row's label, untruncated at a 20-cell label."""
    p = Project("P", "sky", "on_track", start_date=iso(-60), due_date=iso(60), id="p")
    t = Task("wide", "p", "Doing", start_date=iso(-58), due_date=iso(58), id="tw")
    b = Board([p], [t], Path("never.json"), {}, ["A", "Doing", "B"])
    lines, _lm, _t = render(b, 80, 24, "tw")
    assert "Aug 3 → Nov 27 ▸" in lines[2][:20], lines[2]


def test_TC_116_the_legend_names_what_the_gantt_draws():
    """TC-116 (LLR-102.5). The ruler's month mark and the chain are named; the
    old axis and the due meter are not."""
    b = kg_board.build()
    entries = [txt for _sw, txt in legend_entries("gantt", b, TODAY, 118, 30)]
    assert any("month starts" in t for t in entries)
    assert any("critical chain" in t for t in entries)
    assert any("folded project" in t for t in entries)
    assert not any("axis" in t or "counting down" in t for t in entries)
    assert critical_chain(b) == ["tm2", "tm3", "tm4", "tm5"]


# =========================================================================== #
# code review, increment 001: the edges the first battery did not reach
# =========================================================================== #
def test_TC_106_every_selection_is_drawn_at_every_height():
    """TC-106 (code review F1, F2). The oracle board at every panel height from
    4 to 30, every open task selected in turn: it is drawn, and no row spills
    past the panel. RED before the fix: at height 8 the five groups exactly
    fill the body and the last group's selected task was cut; at heights 4
    and 5 no selection was drawn."""
    b = kg_board.build()
    order = nav_model("gantt", b, False, TODAY, 80, 24)[0]
    for h in range(4, 31):
        for tid in order:
            lines, lm, _t = render(b, 80, h, tid)
            assert tid in lm, (h, tid)
            assert len(lines) == h, (h, tid, len(lines))


def test_TC_106_groups_exactly_filling_the_body_keep_every_span_and_the_selection():
    """TC-106 (code review F1). 21 projects in a 21-row body: with the
    selection in the first or the last project the selected task is drawn and
    the projects that do not fit are counted, never silently dropped; with no
    selection all 21 span rows fit."""
    ps = [Project(f"P{i:02d}", "sky", "on_track", start_date=iso(-5), due_date=iso(10),
                  id=f"p{i}") for i in range(21)]
    ts = [Task(f"task {i}", f"p{i}", "Doing", start_date=iso(-2), due_date=iso(4),
               id=f"t{i}") for i in range(21)]
    b = Board(ps, ts, Path("never.json"), {}, ["Backlog", "Doing", "Done"])
    for sel in ("t0", "t20"):
        lines, lm, _t = render(b, 80, 24, sel)
        assert sel in lm, sel
        drawn = sum(1 for ln in lines if ln.startswith(("▾", "▸")))
        m = re.search(r"\+(\d+) not shown", "\n".join(lines))
        assert m and drawn + int(m.group(1)) == 21, (sel, drawn, m)
    lines, lm, _t = render(b, 80, 24, None)
    assert sum(1 for ln in lines if ln.startswith(("▾", "▸"))) == 21


def test_TC_110_a_narrow_label_sheds_its_counts_before_it_overflows():
    """TC-110 (code review F4). Two-digit open and late counts in a narrow
    label: the label sheds `✓n`, then `▲n`, then `N`, and every row stays
    exactly the width."""
    p = Project("Busy", "sky", "on_track", start_date=iso(-30), due_date=iso(20), id="pb")
    ts = [Task(f"late {i}", "pb", "Doing", start_date=iso(-20), due_date=iso(-3), id=f"l{i}")
          for i in range(12)]
    other = Project("Other", "lime", "on_track", start_date=iso(-3), due_date=iso(9), id="po")
    ts.append(Task("o", "po", "Doing", start_date=iso(-1), due_date=iso(4), id="o1"))
    b = Board([p, other], ts, Path("never.json"), {}, ["Backlog", "Doing", "Done"])
    for w in (24, 30, 40, 60, 80):
        for h in (6, 8, 12):
            lines, _lm, _t = render(b, w, h, "o1")
            assert {cell_len(ln) for ln in lines} == {max(24, w)}, (w, h)


def test_TC_101_a_week_window_keeps_its_latest_due_inside():
    """TC-101 (code review F6). At seven days per cell the start moves back to
    a Monday; when that shift would push the latest due past the right edge,
    the past context gives the days back."""
    lo = date(2026, 10, 1)                      # a Thursday
    checked = 0
    for w in range(10, 70, 7):
        for need in range(7 * w - 12, 7 * w + 1):
            hi = lo + timedelta(days=need - 1)
            ax = gantt_axis(w, lo, lo, hi, lo - timedelta(days=60))
            if ax.k == 7:
                assert ax.cell(hi) < w, (w, need, ax.start)
                if need + lo.weekday() <= 7 * w:
                    assert ax.start.weekday() == 0
                checked += 1
    assert checked >= 20


def test_TC_116_the_gantt_legend_reads_the_frame_on_screen():
    """TC-116 (code review F3). The legend is asked of the frame the screen
    shows: with a selection it names the ruler's `⟦━⟧`; with work beyond the
    window it names `◂▸`; with no selection there is no echo entry; under a
    focus it describes the focused frame (nothing folded)."""
    b = kg_board.build()
    with_sel = [t for _s, t in legend_entries("gantt", b, TODAY, 118, 30, selected_id="tw3")]
    assert any("exact dates" in t for t in with_sel)
    assert any("beyond the window" in t for t in with_sel)
    without = [t for _s, t in legend_entries("gantt", b, TODAY, 118, 30)]
    assert not any("exact dates" in t for t in without)
    small = [t for _s, t in legend_entries("gantt", b, TODAY, 80, 24, selected_id="tw3")]
    assert any("folded project" in t for t in small)
    focused = [t for _s, t in legend_entries("gantt", b, TODAY, 80, 24, selected_id="tw3",
                                             gantt_focus="pweb")]
    assert not any("folded project" in t for t in focused)


async def test_AT_112_the_legend_under_a_filter_describes_the_filtered_frame(tmp_path, frozen):
    """AT-112 (HLR-105, LLR-102.5; code review F12). With a `/` filter on, the help's
    legend is asked of the frame the screen shows — two rows shorter than the
    panel — so it names exactly what that frame draws. RED: the legend asked of
    the full panel height lists the marks of a taller frame."""
    from taskboard.modals import HelpModal
    app = _app(tmp_path)
    async with app.run_test(size=(118, 34)) as pilot:
        await _open_gantt(pilot, app, "tw3")
        app.search_query = "e"
        app.refresh_view()
        await pilot.pause()
        await pilot.press("question_mark")
        await pilot.pause()
        modal = app.screen
        assert isinstance(modal, HelpModal)
        w, h = modal._dims
        panel = app.query_one("#viewport").size.height
        assert h == panel - 2, (h, panel)
        fb = views.filtered_board(app.board, "e", False)
        want = legend_entries("gantt", fb, TODAY, w, panel - 2, selected_id="tw3")
        got = legend_entries("gantt", modal._board, TODAY, w, h, selected_id="tw3")
        assert got == want


def test_TC_108_the_focused_header_paints_a_trailing_backslash_as_typed():
    """TC-108 (code review of increment 002, F3). A focused project named `x\\`
    reads `(focused: x\\)` in the header — one backslash, as typed. RED: escaping
    the name alone doubles a backslash that is followed by `)`, not a tag."""
    p = Project("x\\", "sky", "on_track", id="px")
    b = Board([p], [], Path("never.json"), {}, ["A", "B"])
    head = render_gantt(b, False, None, TODAY, width=118, height=10, focus="px").plain
    assert head.split("\n")[0].startswith("◆ GANTT (focused: x\\)"), head.split("\n")[0]


# =========================================================================== #
# increment 004 — the P4 walkthrough's findings (ux-reviewer UXV-1, UXV-5, UXV-6)
# =========================================================================== #
@pytest.mark.parametrize("size", [(118, 34), (80, 24)])
async def test_TC_116_the_gantt_help_fits_its_column(tmp_path, frozen, size):
    """TC-116 (LLR-102.5, UXV-1). In the running app the gantt's help prints
    every usage line whole: no label is wider than the help column it sits in
    (the walkthrough found 7 of 11 lines cut mid-word). RED: the increment-003
    wording, whose bullets ran to 51 cells in a 48-cell column."""
    from textual.widgets import Label
    app = _app(tmp_path)
    async with app.run_test(size=size) as pilot:
        await _open_gantt(pilot, app, "tw3")
        await pilot.press("question_mark")
        await pilot.pause()
        left = app.screen.query_one("#help-left")
        labels = list(left.query(Label))
        assert len(labels) >= 8
        for lab in labels:
            assert lab.size.width <= left.content_region.width, str(lab.render())
        if size == (118, 34):     # the legend column (code review R1); at 80x24 the
            right = app.screen.query_one("#help-right")   # modal's own layout leaves
            for lab in right.query(Label):                # it 22 cells — BACKLOG
                assert lab.size.width <= right.content_region.width, str(lab.render())


def test_TC_110_the_scale_label_fits_at_half_a_day_per_cell():
    """TC-110 (LLR-101.10, UXV-6). At 80 columns a window of half a day per cell
    names its scale whole — `Mondays · .5 d/cell` — not clipped with `…`."""
    lines, _lm, _t = render(kg_board.build(), 80, 24, "tw3", focus="pweb")
    _groups, ax = plan_axis(kg_board.build(), 80, 24, "tw3", focus="pweb")
    assert ax.k == 0.5
    assert "Mondays · .5 d/cell" in lines[2] and "…" not in lines[2][:20], lines[2]


def test_TC_107_the_motions_ride_the_fitted_axis_and_clear_the_clip_marker():
    """TC-107 (LLR-101.7; UXV-5). The flow packet moves one cell per tick along
    an in-progress task's reach; on the critical chain its glyph differs from
    the reach's `━`; and it never covers the `◂` that says the reach began
    before the window. RED: a packet started at cell 0 of a clipped reach."""
    from taskboard.views import CRITICAL_REACH, _gantt_bar
    p = Project("P", "sky", "on_track", start_date=iso(-40), due_date=iso(20), id="pp")
    t = Task("long", "pp", "Doing", start_date=iso(-30), due_date=iso(9), id="tl")
    b = Board([p], [t], Path("never.json"), {}, ["Backlog", "Doing", "Done"])
    ax = GanttAxis(TODAY - timedelta(days=5), 1, 40, TODAY)
    seen = set()
    for tick in range(8):
        cells = _gantt_bar(t, b, ax, {"tl"}, tick)
        assert cells[0][0] == "◂", (tick, cells[:3])
        packet = [x for x, (g, _k) in enumerate(cells) if g == "▬"]
        assert len(packet) == 1 and packet[0] > 0
        seen.add(packet[0])
        assert "▬" != CRITICAL_REACH and CRITICAL_REACH in {g for g, _ in cells}
    assert len(seen) == 8, seen


def test_TC_108_a_focus_the_filter_empties_still_says_focused():
    """D7 (ux-reviewer UXV-12). With a project focus and a `/` filter that
    leaves the focused project off the filtered board, the header still says
    the view is focused — the base wording ` (focused)` — so an empty gantt
    explains itself. RED: the increment-001 header dropped the fallback."""
    from taskboard.views import render_view
    head = render_view("gantt", kg_board.build(), False, "tw3", TODAY, 118, 30, {},
                       gantt_focus="pweb", search_query="API").plain.split("\n")[0]
    assert "(focused)" in head, head
