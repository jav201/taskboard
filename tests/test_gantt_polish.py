"""The gantt says what it is not showing, folds by urgency, shades weekends and
clips its echo honestly (the operator's answers D9, UXV-3, D5 and BACKLOG UXV-7).

Batch 2026-10-02-batch-02 · HLR-205 to HLR-210 · AT-205 to AT-210 · TC-207 to
TC-212.

Field reports: a project with more open tasks than rows showed one page and no
sign of the rest (batch-01 D9); at 80x24 Ops & Security folded although it held
the only task due today (UXV-3); the approved AX-2 frame shaded weekends but the
batch left them out (D5), and its hex vanished at 256 colours (P-4); the ruler's
echo drew `⟦` on the window's edge for a task that started before it (UXV-7).
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

import pytest
from rich.color import Color, ColorSystem

import kg_board
from kg_board import TODAY
from taskboard import app as app_mod
from taskboard import models, views
from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.views import (GanttAxis, WEEKEND_BG, gantt_columns, gantt_plan, gantt_echo,
                             render_gantt)

PHASES = ["Backlog", "Doing", "Done"]


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def render(b, w, h, sel):
    lm: dict = {}
    text = render_gantt(b, False, sel, TODAY, width=w, height=h, line_map=lm)
    return text.plain.split("\n"), lm, text


def big(n: int) -> Board:
    """One project of `n` open tasks, due one a day from today."""
    p = Project("Big", "sky", "on_track", start_date=iso(-3), due_date=iso(n + 5), id="pbig")
    ts = [Task(f"task {i:02d}", "pbig", "Doing", start_date=iso(-2), due_date=iso(i),
               id=f"tb{i}") for i in range(n)]
    return Board([p], ts, Path("never.json"), {}, PHASES)


def task_rows(lines, lm) -> list[str]:
    return [tid for tid, _row in sorted(lm.items(), key=lambda kv: kv[1])]


# =========================================================================== #
# TC-207 — the page hint (LLR-205.1)
# =========================================================================== #
@pytest.mark.parametrize("n,sel,first,last,hint", [
    (30, "tb15", 0, 18, "▼ 11 below"),
    (30, "tb25", 19, 29, "▲ 19 above"),
    (50, "tb25", 19, 37, "▲ 19 above / ▼ 12 below"),
])
def test_TC_207_a_paged_project_says_what_is_above_and_below(n, sel, first, last, hint):
    """TC-207 (LLR-205.1). Panel 80x24, one project (body 21, room 20): pages of
    19 tasks holding the selection, then ONE dim row with the counts — first
    page `▼ below` only, last page `▲ above` only, a middle page both. Every row
    is exactly the width; the hint is never a task row. RED on the base tree:
    pages of 20 and no hint (P-5)."""
    lines, lm, text = render(big(n), 80, 24, sel)
    assert task_rows(lines, lm) == [f"tb{i}" for i in range(first, last + 1)]
    row = max(lm.values()) + 1
    assert lines[row].strip() == hint, lines[row]
    assert all(len(ln) == 80 for ln in lines), [len(ln) for ln in lines]
    at = text.plain.index(hint)
    style = " ".join(str(s.style) for s in text.spans if s.start <= at < s.end)
    assert views.HEX["dim"] in style


def test_TC_207_one_row_left_draws_no_hint_two_rows_draw_it():
    """A room of one row pages as shipped (no hint); a room of two gives a page
    of one task and the hint (the boundary of LLR-205.1)."""
    b = big(10)
    lines, lm, _t = render(b, 80, 5, "tb4")          # body 2: span + 1 row
    assert list(lm) == ["tb4"] and not any("below" in ln or "above" in ln for ln in lines)
    lines, lm, _t = render(b, 80, 6, "tb4")          # body 3: span + task + hint
    assert list(lm) == ["tb4"]
    assert lines[lm["tb4"] + 1].strip() == "▲ 4 above / ▼ 5 below"


# =========================================================================== #
# AT-205 — through the running app (US-203)
# =========================================================================== #
class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def frozen(monkeypatch):
    for mod in (views, app_mod, models):
        monkeypatch.setattr(mod, "date", _Today)


def _app(tmp_path, b=None):
    b = b or kg_board.build(tmp_path / "board.json")
    b.path = Path(tmp_path / "board.json")
    b.save()
    return TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)


def painted(app) -> list[str]:
    return app.query_one("#board").render().plain.split("\n")


async def test_AT_205_a_long_project_says_how_much_is_off_the_page(tmp_path, frozen):
    """AT-205 (HLR-205). A 30-task project at terminal 80x24: walking `down`
    through all 30, the selection is always painted inside the viewport, a
    hint row always says how many tasks are above or below, and the hint row
    never takes the selection. RED on the base tree: no hint is ever painted."""
    b = big(30)
    app = _app(tmp_path, b)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        hints = set()
        for step in range(30):
            out = painted(app)
            sel = app.selected_task_id
            row = app._line_map[sel]
            vp = app.query_one("#viewport")
            assert vp.scroll_offset.y <= row < vp.scroll_offset.y + vp.size.height, (step, sel)
            hint = [ln.strip() for ln in out if re.fullmatch(r"\s*(▲ \d+ above)?( / )?(▼ \d+ below)?\s*", ln)
                    and ln.strip()]
            assert len(hint) == 1, (step, hint)
            hints.add(hint[0])
            assert not out[row].strip().startswith(("▲", "▼")), "the hint took the selection"
            await pilot.press("down")
            await pilot.pause()
        assert any("below" in h for h in hints) and any("above" in h for h in hints), hints


# =========================================================================== #
# TC-209 / AT-208 — urgent groups are offered rows first (HLR-208)
# =========================================================================== #
def urgency_board() -> Board:
    """C (one task, first, takes the selection), A (one late at -3 and four
    later), B (one late at -1, one due today, three later)."""
    ps = [Project("Cee", "violet", "on_track", id="pc"),
          Project("Aye", "sky", "on_track", id="pa"),
          Project("Bee", "lime", "on_track", id="pb")]
    ts = [Task("c only", "pc", "Doing", due_date=iso(9), id="c0")]
    ts += [Task(f"a {i}", "pa", "Doing", due_date=iso(d), id=f"a{i}")
           for i, d in enumerate((-3, 4, 5, 6, 7))]
    ts += [Task(f"b {i}", "pb", "Doing", due_date=iso(d), id=f"b{i}")
           for i, d in enumerate((-1, 0, 5, 6, 7))]
    return Board(ps, ts, Path("never.json"), {}, PHASES)


def unfolded(groups) -> dict[str, bool]:
    return {g.project.name if g.project else "Inbox": g.unfolded for g in groups}


def test_TC_209_due_today_counts_as_urgency():
    """TC-209 (LLR-207.1, urgency half). Body 9 (5 rows after the span rows and
    C): A (1 late) and B (1 late + 1 due today) compete for the 5 rows; B wins
    on urgency weight. RED on the base tree: A wins on the earlier due."""
    g = unfolded(gantt_plan(urgency_board(), False, "c0", TODAY, 9))
    assert g == {"Cee": True, "Aye": False, "Bee": True}, g


def test_TC_209_a_tie_on_weight_goes_to_the_group_due_today():
    """The oracle board at panel 80x22 (terminal 80x24), entry selection `tw2`:
    API Platform (2 late) and Ops & Security (1 late + 1 due today) tie on weight
    2; Ops wins on its due-today task (D-204). RED on the base tree: Ops folds
    (P-6)."""
    g = unfolded(gantt_plan(kg_board.build(), False, "tw2", TODAY, 22 - 3))
    assert g == {"Website Redesign": True, "Mobile App": False, "API Platform": False,
                 "Data Warehouse": True, "Ops & Security": True}, g


async def test_AT_208_urgent_projects_stay_open(tmp_path, frozen):
    """AT-208 (HLR-208). Terminal 80x14 on the urgency board: B (due today) is
    `▾`, A `▸`. Terminal 80x24 on the oracle board: Ops & Security, holding the
    only task due today, is `▾` on entry. RED on the base tree: A open, B
    folded; Ops & Security folded."""
    app = _app(tmp_path, urgency_board())
    async with app.run_test(size=(80, 14)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        out = painted(app)
        assert any(ln.startswith("▾ Bee") for ln in out), out
        assert any(ln.startswith("▸ Aye") for ln in out), out
    app = _app(tmp_path / "o")
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        out = painted(app)
        assert any(ln.startswith("▾ Ops & Sec") for ln in out), out
        assert any(ln.startswith("▸ API Plat") for ln in out), out


# =========================================================================== #
# TC-211 / AT-209 — weekends shaded at a day per cell or finer (HLR-209)
# =========================================================================== #
def bg_columns(text, row: int, x0: int) -> set[int]:
    """Field columns of `row` painted on the weekend background."""
    plain = text.plain
    starts = [0]
    for line in plain.split("\n"):
        starts.append(starts[-1] + len(line) + 1)
    lo, hi = starts[row], starts[row + 1] - 1
    out = set()
    for s in text.spans:
        if WEEKEND_BG in str(s.style).lower() and lo <= s.start < hi:
            out |= {x - lo - x0 for x in range(s.start, s.end)}
    return out


def weekend_cells(ax: GanttAxis) -> set[int]:
    """Recomputed independently of the renderer: cells whose days are all a
    Saturday or a Sunday, at k <= 1."""
    if ax.k > 1:
        return set()
    return {x for x in range(ax.w)
            if all((ax.start + timedelta(days=d)).weekday() >= 5
                   for d in range(int(x * ax.k), max(int((x + 1) * ax.k), int(x * ax.k) + 1)))}


def test_TC_211_weekend_columns_are_shaded_at_one_day_per_cell():
    """TC-211 (LLR-209.1). Oracle board, panel 118x30 (k = 1, window from Sep 14,
    79 cells): the 22 weekend columns carry the background on the day row and
    on every body row's field, and no other cell does. RED on the base tree:
    no background anywhere."""
    lines, lm, text = render(kg_board.build(), 118, 30, "tw3")
    label_w, _c, field_w = gantt_columns(118)
    x0 = label_w + 1
    ax = views.gantt_axis(field_w, TODAY, *views.gantt_window(
        gantt_plan(kg_board.build(), False, "tw3", TODAY, 27), TODAY))
    assert ax.k == 1 and ax.start == date(2026, 9, 14)
    expect = weekend_cells(ax)
    assert len(expect) == 22
    spans = [r for r, ln in enumerate(lines) if ln.startswith(("▾", "▸"))]
    body = sorted(spans + list(lm.values()))
    assert len(spans) == 5 and len(body) >= 20
    assert bg_columns(text, 2, x0) == expect                 # the day row
    assert bg_columns(text, 1, x0) == set()                  # not the month row
    for r in body:                                           # every span and task row
        assert bg_columns(text, r, x0) == expect, (r, lines[r][:30])


def test_TC_211_no_shading_above_a_day_per_cell():
    """Panel 80x24: k = 2 — a cell mixes weekdays and weekend, so nothing is
    shaded."""
    _l, _lm, text = render(kg_board.build(), 80, 24, "tw3")
    assert not any(WEEKEND_BG in str(s.style).lower() for s in text.spans)


def test_TC_211_half_a_day_per_cell_shades_both_cells():
    """k = 0.5: both cells of each weekend day are shaded."""
    ax = GanttAxis(date(2026, 10, 1), 0.5, 20, date(2026, 10, 1))   # a Thursday
    assert ax.weekends() == {4, 5, 6, 7, 18, 19}


def test_TC_211_today_on_a_saturday_keeps_the_accent_rule_on_the_background():
    """A board whose today is a Saturday: the today rule keeps the accent and
    sits on the weekend background (focus role kept, D-201)."""
    sat = date(2026, 10, 3)
    p = Project("P", "sky", "on_track", start_date=(sat - timedelta(days=3)).isoformat(),
                due_date=(sat + timedelta(days=9)).isoformat(), id="pp")
    t = Task("t", "pp", "Doing", start_date=(sat - timedelta(days=2)).isoformat(),
             due_date=(sat + timedelta(days=6)).isoformat(), id="t0")
    b = Board([p], [t], Path("never.json"), {}, PHASES)
    text = render_gantt(b, False, None, sat, width=118, height=12)
    rules = [s for s in text.spans if text.plain[s.start:s.end] in ("╎",)
             and views.HEX["accent"] in str(s.style)]
    assert rules
    for r in rules:
        covering = [s for s in text.spans if s.start <= r.start < s.end
                    and WEEKEND_BG in str(s.style).lower()]
        assert covering, "today's rule lost the weekend background"


def test_TC_211_the_weekend_background_survives_256_colours():
    """The background quantises to a 256-colour index different from the
    screen's (P-4: the prototype's #161d27 did not)."""
    css = Path(app_mod.__file__).with_name("taskboard.tcss").read_text(encoding="utf-8")
    screen = re.search(r"Screen \{[^}]*background: (#[0-9a-fA-F]{6})", css).group(1)
    q = lambda h: Color.parse(h).downgrade(ColorSystem.EIGHT_BIT).number  # noqa: E731
    assert q(WEEKEND_BG) != q(screen), (q(WEEKEND_BG), q(screen))


async def test_AT_209_weekends_are_painted_in_the_app(tmp_path, frozen):
    """AT-209 (HLR-209). Terminal 118x30, key `3`: the painted day row carries
    the weekend background on exactly the weekend columns. RED on the base tree:
    none."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        content = app.query_one("#board").render()
        lines = content.plain.split("\n")
        starts = [0]
        for ln in lines:
            starts.append(starts[-1] + len(ln) + 1)
        label_w, _c, field_w = gantt_columns(len(lines[0]))
        rgb = "rgb({},{},{})".format(*(int(WEEKEND_BG[i:i + 2], 16) for i in (1, 3, 5)))
        cols = set()
        for s in content.spans:
            st = str(s.style).lower().replace(" ", "")
            if (rgb in st or WEEKEND_BG in st) and starts[2] <= s.start < starts[3]:
                cols |= {x - starts[2] - label_w - 1 for x in range(s.start, s.end)}
        # the weekend cells of the axis the panel was drawn on, recomputed
        height = app.query_one("#viewport").size.height
        groups = gantt_plan(app.board, False, app.selected_task_id, TODAY, height - 3)
        ax = views.gantt_axis(field_w, TODAY, *views.gantt_window(groups, TODAY))
        assert ax.k <= 1, "the fixture must reach a day per cell"
        expect = weekend_cells(ax)
        assert len(expect) >= 20 and cols == expect, (sorted(cols), sorted(expect))


# =========================================================================== #
# TC-212 / AT-210 — the echo's clipped ends (HLR-210)
# =========================================================================== #
def test_TC_212_a_start_before_the_window_draws_the_clip_arrow():
    """TC-212 (LLR-210.1). `tw2` (start Sep 5, window from Sep 14) at 118x30:
    the day row's first field cell is `◂`, no `⟦`, and `Sep 5` is still printed.
    RED on the base tree: `⟦` on cell 0 (P-9)."""
    lines, _lm, _t = render(kg_board.build(), 118, 30, "tw2")
    label_w = gantt_columns(118)[0]
    day = lines[2][label_w + 1:]
    assert day[0] == "◂" and "⟦" not in day, day[:20]
    assert "Sep 5" in lines[2]


def test_TC_212_a_due_past_the_window_draws_the_right_arrow():
    """A `k = 7` window at panel 60x20 holds 224 days (field 32); a task due at
    +230 runs past it: its echo ends in `▸`. RED on the base tree: `⟧` clamped
    on the last cell."""
    p = Project("Long", "sky", "on_track", start_date=iso(0), due_date=iso(20), id="pl")
    ts = [Task("near", "pl", "Doing", start_date=iso(0), due_date=iso(10), id="n0"),
          Task("far", "pl", "Doing", start_date=iso(0), due_date=iso(230), id="f0")]
    b = Board([p], ts, Path("never.json"), {}, PHASES)
    groups = gantt_plan(b, False, "f0", TODAY, 17)
    _l, _c, field_w = gantt_columns(60)
    ax = views.gantt_axis(field_w, TODAY, *views.gantt_window(groups, TODAY))
    assert ax.k == 7 and ax.end_cell(TODAY + timedelta(days=230)) >= ax.w
    cells = gantt_echo(b.task_by_id("f0"), b, ax, TODAY)[0]
    assert cells[ax.w - 1] == "▸" and "⟧" not in cells.values()


def test_TC_212_a_start_on_the_first_day_keeps_its_bracket():
    """The boundary: a task starting exactly on the window's first day is not
    clipped — `⟦` stays."""
    b = kg_board.build()
    groups = gantt_plan(b, False, "tw3", TODAY, 27)
    ax = views.gantt_axis(gantt_columns(118)[2], TODAY, *views.gantt_window(groups, TODAY))
    t = b.task_by_id("tw3")
    t.start_date = ax.start.isoformat()
    cells = gantt_echo(t, b, ax, TODAY)[0]
    assert cells[0] == "⟦"


def test_TC_212_the_one_date_forms_clip_too():
    """The open-ended forms clip like the bracketed one (code review F1): a
    task with only a due past the window ends in `▸`; one with only a start
    before it opens with `◂`; inside the window they keep `⟧` / `⟦`."""
    b = kg_board.build()
    ax = GanttAxis(TODAY, 1, 20, TODAY)
    t = b.task_by_id("tw3")
    t.start_date, t.due_date = None, iso(40)
    assert gantt_echo(t, b, ax, TODAY)[0] == {19: "▸"}
    t.start_date, t.due_date = iso(-9), None
    assert gantt_echo(t, b, ax, TODAY)[0] == {0: "◂"}
    t.start_date, t.due_date = None, iso(5)
    assert gantt_echo(t, b, ax, TODAY)[0] == {5: "⟧"}
    t.start_date, t.due_date = iso(3), None
    assert gantt_echo(t, b, ax, TODAY)[0] == {3: "⟦"}


async def test_AT_210_the_echo_shows_where_the_task_starts_earlier(tmp_path, frozen):
    """AT-210 (HLR-210). Terminal 118x30, key `3`: the entry selection is `tw2`,
    which starts before the window — the painted day row opens with `◂`, not
    `⟦`. RED on the base tree: `⟦`."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        assert app.selected_task_id == "tw2"
        line = painted(app)[2]
        label_w = gantt_columns(len(painted(app)[0]))[0]
        assert line[label_w + 1] == "◂" and "⟦" not in line, line


# =========================================================================== #
# TC-209 / TC-210 / AT-207 — the project just left stays open (HLR-207)
# =========================================================================== #
def sticky_board(inbox: bool = False) -> Board:
    """S (selected, one task), A (three quiet tasks), U (three tasks, one late);
    optionally an Inbox of three quiet tasks instead of A."""
    ps = [Project("Ess", "violet", "on_track", id="ps"),
          Project("Aye", "sky", "on_track", id="pa"),
          Project("You", "lime", "on_track", id="pu")]
    ts = [Task("s only", "ps", "Doing", due_date=iso(9), id="s0")]
    ts += [Task(f"u {i}", "pu", "Doing", due_date=iso(d), id=f"u{i}")
           for i, d in enumerate((-2, 6, 7))]
    if inbox:
        ps = [p for p in ps if p.id != "pa"]
        ts += [Task(f"x {i}", None, "Doing", due_date=iso(d), id=f"x{i}")
               for i, d in enumerate((5, 6, 7))]
    else:
        ts += [Task(f"a {i}", "pa", "Doing", due_date=iso(d), id=f"a{i}")
               for i, d in enumerate((5, 6, 7))]
    return Board(ps, ts, Path("never.json"), {}, PHASES)


def test_TC_209_the_previous_group_is_offered_rows_before_urgency():
    """TC-209 (LLR-207.1, `previous`). Body 7 (three span rows, S's one task,
    three rows left): with no previous group U (late) takes the rows; with A as
    the previous group A keeps them and U folds. RED with `previous` ignored."""
    b = sticky_board()
    assert unfolded(gantt_plan(b, False, "s0", TODAY, 7)) == {"Ess": True, "Aye": False,
                                                               "You": True}
    assert unfolded(gantt_plan(b, False, "s0", TODAY, 7, previous="pa")) == {
        "Ess": True, "Aye": True, "You": False}


def test_TC_209_the_inbox_can_be_the_previous_group():
    """The Inbox as the previous group (`INBOX_GROUP`, never confused with "no
    previous group", qa P2 N-1)."""
    b = sticky_board(inbox=True)
    assert unfolded(gantt_plan(b, False, "s0", TODAY, 7)) == {"Ess": True, "You": True,
                                                               "Inbox": False}
    assert unfolded(gantt_plan(b, False, "s0", TODAY, 7, previous=views.INBOX_GROUP)) == {
        "Ess": True, "You": False, "Inbox": True}


async def test_TC_210_only_the_group_just_left_is_remembered(tmp_path, frozen):
    """TC-210 (LLR-207.2). The app remembers the group the selection was in
    before its current one — not every group visited: after A then U then S,
    the previous group is U, and A gains nothing (qa P2 N-2)."""
    b = sticky_board()
    app = _app(tmp_path, b)
    async with app.run_test(size=(80, 30)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        for tid in ("a0", "u1", "s0"):
            app.selected_task_id = tid
            app.refresh_view()
            await pilot.pause()
        assert app._gantt_group == "ps" and app._gantt_previous == "pu"
        app.selected_task_id = "s0"         # the same group again: nothing moves
        app.refresh_view()
        await pilot.pause()
        assert app._gantt_previous == "pu"


async def test_TC_210_the_legend_asks_the_same_frame(tmp_path, frozen, monkeypatch):
    """The help's legend reads the frame the screen shows, previous group
    included: after walking into Mobile App at 80x24, a folded project is on
    screen exactly when the legend explains `▸` (the no-ghost law)."""
    app = _app(tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        for _ in range(5):                  # tw2 .. tw6, then tm6
            await pilot.press("down")
            await pilot.pause()
        assert app.selected_task_id == "tm6"
        folded_on_screen = any(ln.startswith("▸") for ln in painted(app))
        assert folded_on_screen, "the fixture must fold something for the check to bite"
        assert app._gantt_previous == "pweb"
        asked = []
        real_legend = views.legend_entries

        def legend_spy(*a, **k):
            asked.append(k.get("gantt_previous"))
            return real_legend(*a, **k)
        monkeypatch.setattr(views, "legend_entries", legend_spy)
        await pilot.press("question_mark")
        await pilot.pause()
        # the modal asks the legend of the SAME frame the screen was drawn with
        assert asked == ["pweb"], asked
        text = "\n".join(w.render().plain for w in app.screen.query("Label"))
        assert ("a folded project" in text) == folded_on_screen
    # and `legend_entries` threads it into the frame it asks (a spy on the frame)
    seen = []
    real = views._gantt_frame

    def spy(*a, **k):
        seen.append(a[9] if len(a) > 9 else k.get("previous"))
        return real(*a, **k)
    views._gantt_frame = spy
    try:
        views.legend_entries("gantt", sticky_board(), TODAY, 80, 10, selected_id="s0",
                             gantt_previous="pa")
    finally:
        views._gantt_frame = real
    assert seen == ["pa"], seen


@pytest.mark.parametrize("size,max_up", [((80, 24), 2), ((118, 30), 1)])
async def test_AT_207_the_project_just_left_stays_open(tmp_path, frozen, size, max_up):
    """AT-207 (HLR-207) — ONE node over the two terminal sizes (C-18, qa P4
    G-001). Walking `down` from the entry selection through all 25 open tasks:
    stepping from `tw6` into Mobile App (`tm6`) keeps Website Redesign `▾` and
    the highlight does not move up; at API Platform (`ta1`) Mobile App — now the
    group just left — is `▾`; the highlight moves up at most twice at 80x24
    (base: three times, P-7) and at most once at 118x30. RED on the base tree at
    80x24: Website Redesign folds on `tm6`; at 118x30 the fold checks are RED on
    base too, while its up-move bound alone is only a regression PIN — the base
    also moves up once there (qa P4 G-002, G-006)."""
    app = _app(tmp_path)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        walk = [(app.selected_task_id, app._line_map[app.selected_task_id])]
        for _ in range(24):
            await pilot.press("down")
            await pilot.pause()
            sel = app.selected_task_id
            walk.append((sel, app._line_map[sel]))
            if sel == "tm6":
                assert any(ln.startswith("▾ Website") for ln in painted(app)), painted(app)
                assert walk[-1][1] >= walk[-2][1], walk[-2:]
            if sel == "ta1":
                assert any(ln.startswith("▾ Mobile") for ln in painted(app)), painted(app)
        ids = [t for t, _r in walk]
        assert "tm6" in ids and "ta1" in ids and len(set(ids)) == 25
        ups = [(a, b) for a, b in zip(walk, walk[1:]) if b[1] < a[1]]
        assert len(ups) <= max_up, ups


# =========================================================================== #
# TC-208 / AT-206 — finishing a task in the gantt says where it went (HLR-206)
# =========================================================================== #
def toasts(app) -> list[str]:
    return [n.message for n in app._notifications]


async def test_AT_206_a_finished_task_says_where_it_folded(tmp_path, frozen):
    """AT-206 (HLR-206). Terminal 118x30, key `3`: the entry selection `tw2`
    (Review) and `]` → exactly one notice, `Build component library done ·
    folded into ✓2 · u undo`. RED on the base tree: no notice (P-10)."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        assert app.selected_task_id == "tw2"
        before = len(toasts(app))
        await pilot.press("]")
        await pilot.pause()
        assert toasts(app)[before:] == ["Build component library done · folded into ✓2 · u undo"]


async def test_TC_208_only_the_move_that_finishes_notifies(tmp_path, frozen):
    """TC-208 (LLR-206.1). `tw3` (Doing): one `]` → Review, no notice; a second
    → Done, the notice; `]` in the kanban never notifies."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        await pilot.press("down")
        await pilot.pause()
        assert app.selected_task_id == "tw3"
        n = len(toasts(app))
        await pilot.press("]")
        await pilot.pause()
        assert len(toasts(app)) == n
        await pilot.press("]")
        await pilot.pause()
        assert toasts(app)[n:] == ["Fix checkout 500 error done · folded into ✓2 · u undo"]
    app = _app(tmp_path / "k")
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tw2"        # Review: one `]` finishes it, in the kanban
        app.refresh_view()
        await pilot.pause()
        n = len(toasts(app))
        await pilot.press("]")
        await pilot.pause()
        assert app.board.is_done(app.board.task_by_id("tw2")), "the move must happen"
        assert len(toasts(app)) == n


async def test_TC_208_the_count_is_the_groups_own_with_v_on(tmp_path, frozen):
    """The count is the `✓n` of the finished task's OWN group, archived work
    included while `v` shows it (code review F1): Mobile App, one done task
    archived, `v` on, `tm6` (Review) finished → `✓2`."""
    b = kg_board.build(tmp_path / "board.json")
    b.task_by_id("tm1").archived = True
    app = _app(tmp_path, b)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        await pilot.press("v")
        await pilot.pause()
        app.selected_task_id = "tm6"
        app.refresh_view()
        await pilot.pause()
        await pilot.press("]")
        await pilot.pause()
        assert toasts(app)[-1] == "Crash reporting done · folded into ✓2 · u undo"


async def test_TC_208_the_count_follows_the_filter(tmp_path, frozen):
    """Under a `/` filter the count is the filtered group's (code review F1):
    filtering on "Build", `tw2` finished → `✓1` (the filter hides the other
    finished task)."""
    app = _app(tmp_path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        await pilot.press("slash")
        await pilot.pause()
        for ch in "Build":
            await pilot.press(ch)
        await pilot.press("enter")
        await pilot.pause()
        assert app.selected_task_id == "tw2"
        await pilot.press("]")
        await pilot.pause()
        assert toasts(app)[-1] == "Build component library done · folded into ✓1 · u undo"


def test_TC_209_the_filtered_view_keeps_the_previous_group_too():
    """`render_view`'s filtered branch passes the previous group on (code
    review F2): on the sticky board under a filter that keeps every group,
    A is open with `gantt_previous="pa"` and folded without it."""
    b = sticky_board()

    def heads(prev):
        lines = views.render_view("gantt", b, False, "s0", TODAY, 80, 12, {},
                                  search_query="y", gantt_previous=prev).plain.split("\n")
        return {ln[2:5]: ln[0] for ln in lines if ln.startswith(("▾", "▸"))}
    assert heads("pa")["Aye"] == "▾" and heads(None)["Aye"] == "▸", (heads("pa"), heads(None))


@pytest.mark.parametrize("title", ["[b]x[/b]", "[/]", "[@click=app.quit]q[/]"])
async def test_TC_208_a_markup_title_is_shown_literally(tmp_path, frozen, title):
    """A board title that looks like markup is shown as typed — markup is off,
    the title is not escaped (security S-1) — and the app keeps running (a
    `[@click=app.quit]` payload must not quit it)."""
    b = kg_board.build(tmp_path / "board.json")
    b.task_by_id("tw2").title = title
    app = _app(tmp_path, b)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:   # paint the toast
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        await pilot.press("]")
        await pilot.pause()
        assert toasts(app)[-1] == f"{title} done · folded into ✓2 · u undo"
        await pilot.pause()
        painted_toasts = [str(t.render()) for t in app.screen.query("Toast")]
        assert any(title in p for p in painted_toasts), painted_toasts
        assert app.is_running
