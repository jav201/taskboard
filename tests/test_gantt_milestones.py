"""The gantt draws milestones as dates, not bars (batch 2026-10-04-batch-02, US-602, HLR-602).

Field report: the operator's one-day "milestones" draw as a single `◆` in a priority hue with no
way to tell them from work, no distance and no history (P-3); the round-5 verdict chose M-1: a
`◆` row with its date and a chip, reached ones in a legible grey (the UXV-5 verdict: the ash
was ~2.4:1, near illegible), the ruler marking the selected project's
milestones (AX-2).

Law: a milestone row is ` ◆ title`, a `◆` on its date with `Mon D` beside it and no bar, a chip
`in Nd` / `today` / `▲Nd` / `✓ done`; reached = `◆✓` in the reached grey, a row among the open rows by date while
its group has open work; the month row marks the selected project's milestones; the legend names
them right after the selection; `]` that leaves a milestone drawn says "reached"; the arrows walk
every drawn row. Boards are synthetic (`tests/kg_board.py`) in memory or in `tmp_path`.

RED on base: no `milestone` field, no `rows`, no milestone row (P-3, P-4).
"""
from __future__ import annotations

from datetime import date, timedelta

import pytest
from rich.text import Text

import kg_board
from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.views import (GANTT_RULER_ROWS, HEX, _md, gantt_axis, gantt_columns,
                             gantt_milestone_cells, gantt_milestone_chip, gantt_plan,
                             gantt_window, help_usage, legend_entries, milestone_tone,
                             nav_model, render_gantt)

RENUMBER = "seen_view_renumber_2026_07"
KT = kg_board.TODAY
ASH, OVER = HEX["ash"].lower(), HEX["over"].lower()
REACHED = HEX["reached"].lower()   # UXV-5 verdict: reached milestones wear a legible grey


def _ms_board():
    return kg_board.milestones(kg_board.build())


def _line(text: Text, needle: str) -> Text:
    for ln in text.split("\n"):
        if needle in ln.plain:
            return ln
    raise AssertionError(f"{needle!r} not drawn")


def _hex_at(line: Text, i: int) -> str | None:
    """The foreground hex painted at cell `i` of a rendered line (last span wins)."""
    hexes = [str(sp.style) for sp in line.spans if sp.start <= i < sp.end]
    for st in reversed(hexes):
        for word in st.split():
            if word.startswith("#"):
                return word.lower()
    return None


def _field(line: Text, w: int) -> str:
    label_w, _chip_w, field_w = gantt_columns(w)
    return line.plain[label_w + 1:label_w + 1 + field_w]


# --------------------------------------------------------------------------- #
# TC-609 — the plan holds the drawn rows (LLR-602.1)
# --------------------------------------------------------------------------- #
def test_TC_609_rows_merge_reached_milestones_by_due_while_open_work_remains():
    """TC-609: Website Redesign's rows are its open tasks with `Mockups approved`
    merged by due (first: −12); Mobile App has no reached milestone, so rows ==
    open; `open` and `rest` keep their meaning. RED: rows = open (P-4), or the
    reached milestone appended instead of merged."""
    b = _ms_board()
    groups = {g.project.id: g for g in gantt_plan(b, False, "tw5", KT, 27)}
    web = groups["pweb"]
    assert [t.id for t in web.rows] == ["tw0", "tw2", "tw3", "tw4", "tw5", "tw6"]
    assert "tw0" not in [t.id for t in web.open] and "tw0" in [t.id for t in web.rest]
    assert list(groups["pmob"].rows) == list(groups["pmob"].open)


def test_TC_609_a_group_with_only_reached_milestones_draws_no_row():
    """TC-609 (empty): a reached milestone is context for open work; with no open
    work its group draws no row (D-606). RED: rows built from the rest alone."""
    p = Project("Done project", "sky", id="p1")
    b = Board([p], [Task("Signed", "p1", "Done", start_date="2026-09-20",
                         due_date="2026-09-20", milestone=True, id="m")],
              kg_board.Path("x.json"), phases=["Backlog", "Done"])
    (g,) = gantt_plan(b, False, None, KT, 27)
    assert g.rows == () and not g.unfolded


@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
def test_TC_609_nav_walks_the_drawn_rows_in_draw_order(size):
    """TC-609: the arrows walk exactly the rows the frame draws, in its order,
    reached milestones included (F-3). RED: nav over `open` misses `tw0`."""
    b = _ms_board()
    lm: dict = {}
    render_gantt(b, False, "tw0", KT, size[0], size[1], line_map=lm)
    drawn = [tid for tid, _row in sorted(lm.items(), key=lambda kv: kv[1])]
    (nav,) = nav_model("gantt", b, False, KT, size[0], size[1], selected_id="tw0")
    assert "tw0" in drawn and "tw0" in nav
    assert [t for t in nav if t in drawn] == drawn


@pytest.mark.parametrize("size", [(118, 7), (80, 6)])
def test_TC_609_a_selected_reached_milestone_is_drawn_when_rows_are_scarce(size):
    """TC-609 (code review G-1): when the body has room for little more than the
    span rows, the frame pages by the drawn rows — a selected REACHED milestone is
    still drawn. RED: the frame's selection test reading `open` (mutant R)."""
    lm: dict = {}
    render_gantt(_ms_board(), False, "tw0", KT, size[0], size[1], line_map=lm)
    assert "tw0" in lm


def test_TC_609_a_selected_reached_milestone_unfolds_its_group():
    """TC-609: selecting a reached milestone unfolds its group (it is a row)."""
    b = _ms_board()
    groups = {g.project.id: g for g in gantt_plan(b, False, "tw0", KT, 8)}
    assert groups["pweb"].unfolded


# --------------------------------------------------------------------------- #
# TC-610 — the milestone row (LLR-602.2)
# --------------------------------------------------------------------------- #
CHIPS = {"tw5": ("in 10d", None), "tm5": ("in 35d", None), "ta3": ("in 3d", None),
         "tw0": ("✓ done", "reached"), "to0": ("▲2d", "over"), "td0": ("in 18d", None)}


@pytest.mark.parametrize("tid", sorted(CHIPS))
def test_TC_610_tone_and_chip_equal_the_verdicts_rule(tid):
    """TC-610: the six kg milestones' chips and tones equal the prototype's rule
    executed in P-16 (`p1-thresholds.txt`). RED: a reached milestone in its hue,
    `▲` on a due of today."""
    b = _ms_board()
    t = b.task_by_id(tid)
    chip, tone = CHIPS[tid]
    assert Text.from_markup(gantt_milestone_chip(t, b, KT, 8)).plain.strip() == chip
    want = tone or b.project_by_id(t.project_id).color
    assert milestone_tone(t, b, KT) == want


def test_TC_610_today_no_due_and_the_inbox():
    """TC-610 boundary: due today → `today` (soon); no due → `no due`, no `◆`; an
    Inbox milestone's tone is dim. RED: `▲0d`."""
    b = Board([], [Task("t", start_date=KT.isoformat(), due_date=KT.isoformat(),
                        milestone=True, id="a"),
                   Task("n", milestone=True, id="b")], kg_board.Path("x.json"))
    a, n = b.tasks
    assert Text.from_markup(gantt_milestone_chip(a, b, KT, 8)).plain.strip() == "today"
    assert Text.from_markup(gantt_milestone_chip(n, b, KT, 8)).plain.strip() == "no due"
    assert milestone_tone(a, b, KT) == "dim"
    ax = gantt_axis(60, KT, KT - timedelta(days=5), KT + timedelta(days=20), KT)
    assert all(g == " " for g, _ in gantt_milestone_cells(n, b, ax, KT, "dim"))


@pytest.mark.parametrize("off", [-40, 0, 6, 25, 400])
def test_TC_610_cells_hold_one_diamond_and_its_date_and_never_a_bar(off):
    """TC-610: exactly one `◆` (`◆✓` reached), the date `Mon D` adjacent (after, or
    before at the right edge), 0 bar or tip glyphs; off the window the edge glyph
    and the `◆` beside it. RED: the shipped `_gantt_bar`'s `╌`/tip."""
    d = KT + timedelta(days=off)
    b = Board([], [Task("m", start_date=d.isoformat(), due_date=d.isoformat(),
                        milestone=True, id="m")], kg_board.Path("x.json"))
    ax = gantt_axis(60, KT, KT - timedelta(days=5), KT + timedelta(days=30), KT)
    glyphs = "".join(g for g, _ in gantt_milestone_cells(b.tasks[0], b, ax, KT, "sky"))
    assert glyphs.count("◆") == 1
    assert not set(glyphs) & set("╌━○◔◑◕▬─")
    if 0 <= ax.cell(d) < ax.w:
        assert f"◆ {_md(d)}" in glyphs or f"{_md(d)} ◆" in glyphs, glyphs
    else:
        assert ("◂◆" in glyphs) if off < 0 else ("◆▸" in glyphs), glyphs


def test_TC_610_a_reached_milestone_on_the_last_column_keeps_its_day():
    """TC-610 (code review G-2): a reached milestone due on the field's last cell
    draws its `◆` ON that cell; the `✓` it has no room for is dropped (the chip says
    `✓ done`). RED: the pair clamped one cell (one day) early."""
    ax = gantt_axis(60, KT, KT - timedelta(days=5), KT + timedelta(days=30), KT)
    d = next(KT + timedelta(days=n) for n in range(400) if ax.cell(KT + timedelta(days=n)) == ax.w - 1)
    b = Board([], [Task("m", "", "Done", start_date=d.isoformat(), due_date=d.isoformat(),
                        milestone=True, id="m")], kg_board.Path("x.json"), phases=["Doing", "Done"])
    cells = gantt_milestone_cells(b.tasks[0], b, ax, KT, "ash")
    assert cells[ax.w - 1][0] == "◆"


@pytest.mark.parametrize("title", ["[b]x[/b]", "[/]", "ends in \\"])
def test_TC_610_a_milestone_title_paints_literally(title):
    """TC-610 (S1, security S-1): a title that looks like markup is painted as
    typed, with no exception. RED: an unescaped title in the label."""
    b = _ms_board()
    b.task_by_id("tw5").title = title
    txt = render_gantt(b, False, "tw5", KT, 118, 30)
    assert f" ◆ {title}" in txt.plain


# --------------------------------------------------------------------------- #
# TC-611 — the ruler marks, the legend and the help (LLR-602.3)
# --------------------------------------------------------------------------- #
def _month_marks(b, sel, w=118, h=30):
    txt = render_gantt(b, False, sel, KT, w, h)
    month = txt.split("\n")[1]
    label_w = gantt_columns(w)[0]
    return {i - label_w - 1: _hex_at(month, i) for i, ch in enumerate(month.plain)
            if ch == "◆" and i > label_w}


def _cell(b, sel, d, w=118, h=30):
    body = h - 1 - GANTT_RULER_ROWS
    ax = gantt_axis(gantt_columns(w)[2], KT, *gantt_window(gantt_plan(b, False, sel, KT,
                                                                      body), KT))
    return ax.cell(d)


def test_TC_611_the_month_row_marks_the_selected_projects_milestones():
    """TC-611: with `Launch new homepage` selected the month row's `◆` cells are
    the project due's, Launch's and Mockups' (ash); with `Revenue model signed off`
    selected its own cell carries a `◆` in Data Warehouse's hue. RED: only the
    project due (base), or every project's milestones."""
    b = _ms_board()
    marks = _month_marks(b, "tw5")
    want = {_cell(b, "tw5", date.fromisoformat(b.task_by_id(t).due_date)) for t in ("tw5", "tw0")}
    want.add(_cell(b, "tw5", date.fromisoformat(b.project_by_id("pweb").due_date)))
    assert set(marks) == want
    assert marks[_cell(b, "tw5", date.fromisoformat(b.task_by_id("tw0").due_date))] == REACHED
    marks = _month_marks(b, "td0")
    x = _cell(b, "td0", date.fromisoformat(b.task_by_id("td0").due_date))
    assert marks.get(x) == HEX[b.project_by_id("pdwh").color].lower()


def test_TC_611_a_project_without_milestones_marks_only_its_due():
    """TC-611: no milestone → only the project's due is marked. RED: marks taken
    from every project."""
    b = _ms_board()
    b.task_by_id("tm5").milestone = False
    due = _cell(b, "tm2", date.fromisoformat(b.project_by_id("pmob").due_date))
    want = {due} if 0 <= due < gantt_columns(118)[2] else set()
    assert set(_month_marks(b, "tm2")) == want      # code review G-3: exact


@pytest.mark.parametrize("w, h", [(118, 30), (80, 24)])
def test_TC_611_the_legend_names_milestones_right_after_the_selection(w, h):
    """TC-611 (D-624): `◆ milestone · ◆✓ reached` follow the selection item, so they
    survive at 80 (the M-1 frames' order); a board with no milestone names none.
    RED: the items appended last (shed first at 80)."""
    legend = render_gantt(_ms_board(), False, "tw5", KT, w, h).plain.split("\n")[-1]
    assert "selected, exact dates · ◆ milestone · ◆✓ reached" in legend, legend
    plain = render_gantt(kg_board.build(), False, "tw5", KT, w, h).plain.split("\n")[-1]
    assert "milestone" not in plain and "reached" not in plain


def test_TC_611_the_map_and_the_help_name_milestones():
    """TC-611: the `?` map lists both marks when the frame draws them; the gantt
    help names `◆ title` and `M` in ≤ 44 cells."""
    b = _ms_board()
    entries = [d for _sw, d in legend_entries("gantt", b, KT, selected_id="tw5")]
    assert "a milestone: one date, no bar" in entries and "a milestone reached" in entries
    bullets = [x for _h, xs in help_usage("gantt") for x in xs]
    hit = [x for x in bullets if "◆ title = a milestone" in x]
    assert hit and len(hit[0]) <= 44


# --------------------------------------------------------------------------- #
# AT-602 — through the shipped surface (HLR-602)
# --------------------------------------------------------------------------- #
def _painted(app):
    strips = app.screen._compositor.render_strips(app.screen.size)
    rows = []
    for s in strips:
        cells = []
        for seg in s:
            hx = (seg.style.color.triplet.hex.lower()
                  if seg.style and seg.style.color and seg.style.color.triplet else None)
            cells += [(ch, hx) for ch in seg.text]
        rows.append(cells)
    return rows


def _row(rows, needle):
    for r in rows:
        if needle in "".join(ch for ch, _ in r):
            return r
    raise AssertionError(f"{needle!r} not painted")


def _toasts(app):
    return [str(t.render()) for t in app.screen.query("Toast")]


async def test_AT_602_milestones_read_as_dates_reached_ones_quiet_the_ruler_marks_them(tmp_path):
    """AT-602 (US-602): at 118×30 in the gantt, `Launch new homepage` is a ` ◆` row
    with its date in the field and `in 10d`, no bar; `Mockups approved` is `◆✓`
    with `✓ done`, all in the reached grey; `Security review sign-off`'s chip `▲2d` is over; the
    month row holds a reached-grey `◆`; with `Revenue model signed off` selected its column
    holds a Data Warehouse `◆`; the legend names both marks at 118×30 and 80×24;
    `↑` from `Build component library` selects `Mockups approved`, `↓` returns;
    `]` pressed on `Launch new homepage` until Done says "reached", never
    "folded", and its row becomes `◆✓`. RED on base: plain task rows (P-3/P-4)."""
    path = tmp_path / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    b.save()
    today = date.today()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("3")
        await pilot.pause()
        for _ in range(80):
            if app.selected_task_id == "tw5":
                break
            await pilot.press("down")
            await pilot.pause()
        rows = _painted(app)
        launch = _row(rows, " ◆ Launch new homepage")
        text = "".join(ch for ch, _ in launch)
        label_w, _cw, field_w = gantt_columns(118)
        field = text[label_w + 1:label_w + 1 + field_w]
        assert f"◆ {_md(today + timedelta(days=10))}" in field and "╌" not in field
        assert text.rstrip().endswith("in 10d")
        mock = _row(rows, " ◆ Mockups approved")
        mtext = "".join(ch for ch, _ in mock)
        assert "◆✓" in mtext and mtext.rstrip().endswith("✓ done")
        i = mtext.index("◆✓", label_w)
        assert mock[i][1] == REACHED and mock[i + 1][1] == REACHED
        assert mock[mtext.index("Mockups")][1] == REACHED
        assert mock[mtext.index(_md(today - timedelta(days=12)), label_w)][1] == REACHED
        sec = _row(rows, " ◆ Security review sign-off")
        stext = "".join(ch for ch, _ in sec)
        assert stext.rstrip().endswith("▲2d") and sec[stext.rindex("▲2d")][1] == OVER
        month = rows[1]
        assert any(ch == "◆" and hx == REACHED for ch, hx in month)
        assert "◆ milestone · ◆✓ reached" in "".join("".join(c for c, _ in r) for r in rows)
        # the ruler on another project's milestone
        app.selected_task_id = "td0"
        app.refresh_view()
        await pilot.pause()
        rows = _painted(app)
        dwh = HEX[app.board.project_by_id("pdwh").color].lower()   # as loaded
        # two marks in its hue: the project due AND the milestone (qa F-2; one = only the due)
        assert sum(ch == "◆" and hx == dwh for ch, hx in rows[1][gantt_columns(118)[0]:]) == 2
        # ↑ / ↓ over the reached row
        app.selected_task_id = "tw2"
        app.refresh_view()
        await pilot.pause()
        await pilot.press("up")
        await pilot.pause()
        assert app.selected_task_id == "tw0"
        await pilot.press("down")
        await pilot.pause()
        assert app.selected_task_id == "tw2"
        # `]` until Done: reached, not folded
        app.selected_task_id = "tw5"
        app.refresh_view()
        await pilot.pause()
        app.clear_notifications()
        for _ in range(4):
            await pilot.press("right_square_bracket")
            await pilot.pause()
        said = _toasts(app)
        assert sum("Launch new homepage reached · ◆✓" in x for x in said) == 1, said
        assert not any("folded" in x for x in said)
        assert "◆✓" in "".join(ch for ch, _ in _row(_painted(app), " ◆ Launch new homepage"))
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("3")
        await pilot.pause()
        app.selected_task_id = "ta3"
        app.refresh_view()
        await pilot.pause()
        rows = ["".join(ch for ch, _ in r) for r in _painted(app)]
        assert any("◆ milestone · ◆✓ reached" in r for r in rows)
        sel = next(r for r in rows if " ◆ Partner notice" in r)
        assert sel.rstrip().endswith("in 3d")
