"""The kanban carries milestones on the band rule, never as cards (batch 2026-10-04-batch-02,
US-603, HLR-603).

Field report: a one-day "milestone" is a card in a phase column, counted in the header, the
column counts and WIP, though nobody works on it (P-5). The round-5 verdict chose M-2: milestones
leave the columns and ride their project's band rule — late first, then upcoming, then the last
reached one.

Law: no presentation draws, counts or selects a milestone; the grouped project grouping's band rule
carries them in the order late · upcoming · last reached, laid out by the prototype's ladder (titles
of ≥ 8 cells, then dates only, then `+N ◆`; `+N ◆` alone when no date fits). The oracle rows are the
executed prototype rules (`evidence/p1-thresholds.txt`, `p1-thresholds-shipped.txt`). Boards are
synthetic (`tests/kg_board.py`).

RED on base: the milestone is a card and is counted (P-5).
"""
from __future__ import annotations

import ast
import inspect
import re
from datetime import date, timedelta
from pathlib import Path

import pytest
from rich.text import Text

import kg_board
from taskboard import views
from taskboard.app import TaskboardApp
from taskboard.views import (HEX, _md, band_milestone_facts, band_milestones, kanban_work,
                             nav_model, phase_buckets, render_kanban, render_view)

RENUMBER = "seen_view_renumber_2026_07"
KT = kg_board.TODAY
MS_TITLES = ("Launch new homepage", "Beta release to testers", "Partner notice emails",
             "Mockups approved", "Security review sign-off", "Revenue model signed off")


def _ms_board():
    return kg_board.milestones(kg_board.build())


def _presentations() -> set[str]:
    """Derived from `render_kanban`'s own branches (C-31): every string it compares
    `presentation` against, plus its default."""
    tree = ast.parse(inspect.getsource(views.render_kanban))
    found = {n.comparators[0].value for n in ast.walk(tree)
             if isinstance(n, ast.Compare) and isinstance(n.left, ast.Name)
             and n.left.id == "presentation" and isinstance(n.comparators[0], ast.Constant)}
    default = inspect.signature(views.render_kanban).parameters["presentation"].default
    return found | {default}


def test_TC_612_the_presentation_set_is_derived_and_complete():
    """TC-612 (C-31 guard): the swept set holds every branch — grouped, matrix,
    lanes. RED: a hand-listed set missing a presentation."""
    assert _presentations() >= {"grouped", "matrix", "lanes"}


# --------------------------------------------------------------------------- #
# TC-612 — a milestone is not a kanban card (LLR-603.1)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("presentation", sorted({"grouped", "matrix", "lanes"}))
@pytest.mark.parametrize("group", ["project", "priority", "horizon"])
@pytest.mark.parametrize("sort", ["project", "due", "priority"])
def test_TC_612_no_card_count_or_nav_holds_a_milestone(presentation, group, sort):
    """TC-612: in every presentation and mode, 0 milestone ids in the drawn line map
    and the nav; `N tasks` and each column tag count only work. RED: a presentation
    laying out `visible_tasks` unfiltered (base)."""
    b = _ms_board()
    lm: dict = {}
    txt = render_kanban(b, False, "tw3", KT, 118, 60, line_map=lm, presentation=presentation,
                        sort=sort, group=group)
    nav = nav_model("kanban", b, False, KT, 118, 60, selected_id="tw3", kanban_sort=sort,
                    kanban_group=group, presentation=presentation)
    assert not set(lm) & kg_board.MILESTONE_IDS
    assert not {tid for col in nav for tid in col} & kg_board.MILESTONE_IDS
    work = kanban_work(b.visible_tasks(False))
    assert f"{len(work)} tasks" in txt.plain.split("\n")[0]
    counts = [len(bk) for bk in phase_buckets(b, work)]
    head = txt.plain.split("\n")[1]
    for phase, n in zip(b.phases[:-1], counts):
        assert re.search(rf"{phase.upper()}\S*\s+{n}(/\d+)?\b", head), (phase, n, head)


def test_TC_612_the_band_counts_and_the_high_band_hold_no_milestone():
    """TC-612: the band's `N open` and `N high ↑` and the high band exclude
    milestones (`Launch new homepage` is a high-priority milestone). RED: counted."""
    b = _ms_board()
    plan = views.kanban_plan(b, False, "tw3", KT, 118, 60)
    assert not {t.id for col in plan.high for t in col} & kg_board.MILESTONE_IDS
    web = next(x for x in plan.bands if x.name == "Website Redesign")
    assert web.n_open == 4


def test_TC_612_the_filter_counts_only_work():
    """TC-612 (LED .4, LED .7): `/` matching only a milestone paints `0/25 tasks`
    in the kanban — the filter bar's emitted form. RED: the filter counting
    `visible_tasks` (`1/31 tasks`)."""
    b = _ms_board()
    txt = render_view("kanban", b, False, "tw3", KT, width=118, height=30,
                      search_query="partner notice")
    assert " 0/25 tasks " in txt.plain.split("\n")[1], txt.plain.split("\n")[:3]


@pytest.mark.parametrize("presentation, keys, width, ms", [
    ("grouped", ["4"], 118, "ta3"), ("matrix", ["4", "tab"], 118, "ta3"),
    ("lanes", ["4", "tab", "tab"], 118, "ta3"),
    ("lanes", ["4", "tab", "tab"], 60, "tw0")])     # a window starting at Doing
async def test_TC_612_a_milestone_selection_moves_to_a_drawn_card(tmp_path, presentation,
                                                                 keys, width, ms):
    """TC-612 (D-614, architect A2-3): entering the kanban with a milestone selected,
    the selection moves to the first card of the nearest drawn column at or left of
    its phase — in each presentation, including a lanes window at 60 columns that
    does not start at the first phase. RED: `_select_first` keeping the milestone."""
    path = tmp_path / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(width, 30)) as pilot:
        await pilot.press("3")
        await pilot.pause()
        for k in keys:
            await pilot.press(k)
            await pilot.pause()
        assert app.kanban_presentation == presentation
        app.selected_task_id = ms                        # a milestone, in THIS presentation
        app.refresh_view()
        await pilot.pause()
        sel = app.selected_task_id
        assert sel not in kg_board.MILESTONE_IDS
        cols = [col for col in app._nav_columns() if col]
        assert any(sel in col for col in cols)
        ph = app.board.phase_index(app.board.task_by_id(ms))
        heads = [app.board.phase_index(app.board.task_by_id(col[0])) for col in cols]
        assert app.board.phase_index(app.board.task_by_id(sel)) == max(
            h for h in heads if h <= ph)                 # the NEAREST column at or left


# --------------------------------------------------------------------------- #
# TC-613 — the band rule's milestones (LLR-603.2)
# --------------------------------------------------------------------------- #
ORDER = {"pweb": [("ahead", "Launch new homepage"), ("reached", "Mockups approved")],
         "pmob": [("ahead", "Beta release to testers")],
         "papi": [("ahead", "Partner notice emails")],
         "pdwh": [("ahead", "Revenue model signed off")],
         "pops": [("late", "Security review sign-off")]}

# `evidence/p1-thresholds.txt` (rooms 70/40/20) and `p1-thresholds-shipped.txt` (the
# shipped rooms at 118 and 80), the prototype's `_ms_segment` executed; API at 12 is
# D-619's `+N ◆` fallback (the prototype draws nothing there).
SEGMENTS = {
    ("pweb", 70): "◆ Oct 10 Launch new homepage · in 10d ── ◆ Sep 18 Mockups approved ✓",
    ("pweb", 40): "◆ Oct 10 Launch new homepage · in 10d",
    ("pweb", 20): "◆ Oct 10 · in 10d",
    ("pweb", 56): "◆ Oct 10 Launch new hom… · in 10d ── ◆ Sep 18 Mockups… ✓",
    ("pweb", 18): "◆ Oct 10 · in 10d",
    ("pmob", 70): "◆ Nov 4 Beta release to testers · in 35d",
    ("pmob", 62): "◆ Nov 4 Beta release to testers · in 35d",
    ("pmob", 24): "◆ Nov 4 · in 35d",
    ("pmob", 20): "◆ Nov 4 · in 35d",
    ("papi", 50): "◆ Oct 3 Partner notice emails · in 3d",
    ("papi", 20): "◆ Oct 3 · in 3d",
    ("papi", 12): "+1 ◆",
    ("pdwh", 69): "◆ Oct 18 Revenue model signed off · in 18d",
    ("pdwh", 40): "◆ Oct 18 Revenue model signed … · in 18d",
    ("pdwh", 31): "◆ Oct 18 Revenue mode… · in 18d",
    ("pdwh", 20): "◆ Oct 18 · in 18d",
    ("pops", 70): "◆ Sep 28 Security review sign-off · 2d late",
    ("pops", 59): "◆ Sep 28 Security review sign-off · 2d late",
    ("pops", 40): "◆ Sep 28 Security review sign… · 2d late",
    ("pops", 21): "◆ Sep 28 · 2d late",
    ("pops", 20): "◆ Sep 28 · 2d late",
}


@pytest.mark.parametrize("pid", sorted(ORDER))
def test_TC_613_the_order_is_late_upcoming_then_the_last_reached(pid):
    """TC-613: the per-project order equals the prototype's `_ms_bits` (P-16). RED:
    late after upcoming; every reached milestone listed."""
    b = _ms_board()
    got = [(kind, t.title) for kind, t in band_milestones(b, b.project_by_id(pid), KT)]
    assert got == ORDER[pid]


def test_TC_613_one_project_with_every_kind_orders_them_and_keeps_one_reached():
    """TC-613 (C-31: the kg board has no project holding a late AND an upcoming
    milestone, nor two reached ones — battery K7, K8 survived): late first, then
    upcoming, then ONLY the reached one with the latest due. RED: late after
    upcoming (K7); every reached listed (K8)."""
    p = kg_board.Project("Mixed", "sky", id="pm")

    def ms(tid, phase, off):
        d = (KT + timedelta(days=off)).isoformat()
        return kg_board.Task(tid, "pm", phase, start_date=d, due_date=d, milestone=True,
                             id=tid)
    b = kg_board.Board([p], [ms("up", "Backlog", 4), ms("late", "Doing", -3),
                             ms("old", "Done", -20), ms("new", "Done", -6)],
                       kg_board.Path("x.json"), phases=["Backlog", "Doing", "Done"])
    got = [(kind, t.id) for kind, t in band_milestones(b, p, KT)]
    assert got == [("late", "late"), ("ahead", "up"), ("reached", "new")]


@pytest.mark.parametrize("pid, room", sorted(SEGMENTS))
def test_TC_613_the_layout_equals_the_executed_rule(pid, room):
    """TC-613: at every room the segment text equals the executed prototype rule.
    RED: reached counted in `+N`, titles dropped before cut, no fallback."""
    b = _ms_board()
    p = b.project_by_id(pid)
    facts = band_milestone_facts(band_milestones(b, p, KT), room, p.color, KT)
    assert "".join(f[0] for f in facts) == SEGMENTS[(pid, room)]


def test_TC_613_tones_follow_the_kind():
    """TC-613: late in over (◆, date, relative), upcoming `◆` in the project hue
    and `today` in soon, reached all in the reached grey (UXV-5). RED: an upcoming `◆` in over."""
    b = _ms_board()
    late = band_milestone_facts(band_milestones(b, b.project_by_id("pops"), KT), 70, "rose", KT)
    assert [f[1] for f in late] == ["over", "over", "hd", "over"]
    web = band_milestone_facts(band_milestones(b, b.project_by_id("pweb"), KT), 70, "violet", KT)
    assert web[0] == ("◆ ", "violet") and web[-1] == (" ✓", "reached")
    assert [f[1] for f in web[5:]] == ["reached", "reached", "reached", "reached"]
    b.task_by_id("tw5").start_date = b.task_by_id("tw5").due_date = KT.isoformat()
    today = band_milestone_facts(band_milestones(b, b.project_by_id("pweb"), KT), 70, "violet", KT)
    assert (" · today", "soon") in today


def test_TC_613_a_title_that_looks_like_markup_paints_literally():
    """TC-613 (S1): a milestone title `[b]x[/b]` on the band rule paints as typed.
    RED: a fact built with markup."""
    b = _ms_board()
    b.task_by_id("tm5").title = "[b]x[/b]"
    txt = render_kanban(b, False, "tw3", KT, 118, 60)
    assert "◆ Nov 4 [b]x[/b] · in 35d" in txt.plain


def test_TC_613_the_kanban_help_names_the_band_milestone():
    """TC-613 (code review K-2): the kanban help says what `◆` on a band rule is, in
    ≤ 44 cells. RED: the bullet deleted."""
    bullets = [x for _h, xs in views.help_usage("kanban") for x in xs]
    hit = [x for x in bullets if "◆ on a band rule" in x]
    assert hit and len(hit[0]) <= 44


@pytest.mark.parametrize("presentation, group, want", [("grouped", "project", True),
                                                       ("matrix", "project", False),
                                                       ("lanes", "project", False),
                                                       ("grouped", "priority", False)])
def test_TC_613_the_legend_names_the_band_milestone_exactly_when_drawn(presentation, group,
                                                                       want):
    """TC-613 (code review K-1, K-2; the no-ghost law): the `?` entry "a milestone on
    its project's band rule" is listed exactly where a rule draws a `◆` — the grouped
    project grouping — and nowhere else. RED: an entry blind to the presentation and
    the grouping (r1), or deleted."""
    entries = [d for _s, d in views.legend_entries("kanban", _ms_board(), KT, 118, 60,
                                                    kanban_presentation=presentation,
                                                    kanban_group=group)]
    assert ("a milestone on its project's band rule" in entries) is want


def test_TC_613_a_band_of_done_cards_carries_its_milestone_and_the_legend_says_so():
    """TC-613 (code review K-1 b; D-623 as amended, LED .8): a project whose cards are
    all done still draws its band (the done rail) and that rule carries its upcoming
    milestone — and the legend names it. RED: a legend keyed on an OPEN card (r1)."""
    p = kg_board.Project("Closed", "sky", id="pc")
    d = (KT + timedelta(days=5)).isoformat()
    b = kg_board.Board([p], [kg_board.Task("Shipped", "pc", "Done", id="s"),
                             kg_board.Task("Review", "pc", "Backlog", start_date=d,
                                           due_date=d, milestone=True, id="m")],
                       kg_board.Path("x.json"), phases=["Backlog", "Done"])
    txt = render_kanban(b, False, None, KT, 118, 30)
    assert any(ln.startswith("▐ Closed") and "◆" in ln for ln in txt.plain.split(chr(10)))
    entries = [e for _s, e in views.legend_entries("kanban", b, KT, 118, 30)]
    assert "a milestone on its project's band rule" in entries


def test_TC_613_only_the_project_grouping_carries_milestones():
    """TC-613: in priority grouping no rule carries a `◆`. RED: milestones on every
    rule."""
    b = _ms_board()
    txt = render_kanban(b, False, "tw3", KT, 118, 60, group="priority")
    assert not any("◆" in ln for ln in txt.plain.split("\n")[3:])


# --------------------------------------------------------------------------- #
# AT-603 — through the shipped surface (HLR-603)
# --------------------------------------------------------------------------- #
def _painted(app):
    strips = app.screen._compositor.render_strips(app.screen.size)
    out = []
    for s in strips:
        cells = []
        for seg in s:
            hx = (seg.style.color.triplet.hex.lower()
                  if seg.style and seg.style.color and seg.style.color.triplet else None)
            cells += [(ch, hx) for ch in seg.text]
        out.append(cells)
    return out


def _text(rows):
    return ["".join(ch for ch, _ in r) for r in rows]


def _cards(rows):
    """The card cells: every painted row that is not a band rule, head or fold."""
    return [r for r in _text(rows)[3:] if not r.startswith(("▐", "──", "▲ ", "▼ "))]


async def test_AT_603_the_columns_hold_only_work_and_the_band_says_what_is_coming(tmp_path):
    """AT-603 (US-603): at 118×30 grouped the header says 25 tasks, every column tag
    counts work only, no milestone title is in a card; Website Redesign's rule reads
    `◆ ‹today+10›` Launch… `· in 10d ── ◆ ‹today−12›` Mockups… `✓` with `4 open`;
    at 118×40 Ops & Security's rule holds `Security review sign-off · 2d late` in
    over; `g` (priority) puts no `◆` on any rule; matrix and lanes paint no milestone
    and say 25 tasks; the nav walks none; `M` on a card leaves the selection on a
    drawn card and the next `]` moves THAT card; at 80×24 the Website rule holds
    `◆ ‹today+10› · in 10d`. RED on base: the milestones are cards and counted."""
    path = tmp_path / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    b.save()
    original = path.read_bytes()                 # the later arms read the board unmoved
    today = date.today()
    work = kanban_work(b.visible_tasks(False))
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        rows = _painted(app)
        text = _text(rows)
        assert text[0].rstrip().endswith("25 tasks")
        counts = [len(bk) for bk in phase_buckets(app.board, work)]
        for phase, n in zip(app.board.phases[:-1], counts):
            assert re.search(rf"{phase.upper()}\S*\s+{n}(/\d+)?\b", text[1]), (phase, text[1])
        assert not any(t in "".join(_cards(rows)) for t in MS_TITLES)
        web = next(r for r in text if r.startswith("▐ Website Redesign"))
        want = [f"◆ {_md(today + timedelta(days=10))}", "Launch", "· in 10d", "──",
                f"◆ {_md(today - timedelta(days=12))}", "Mockups", "✓"]
        at = web.index("project due")
        for token in want:
            at = web.index(token, at)
        assert "4 open" in web
        assert not {t for col in app._nav_columns() for t in col} & kg_board.MILESTONE_IDS
        await pilot.press("g")                    # priority grouping
        await pilot.pause()
        text = _text(_painted(app))
        assert app.kanban_group == "priority"
        assert not any("◆" in r for r in text[3:])
        assert text[0].rstrip().endswith("25 tasks")
        for _ in range(2):                        # back to the project grouping
            await pilot.press("g")
            await pilot.pause()
        for name in ("matrix", "lanes"):
            await pilot.press("tab")
            await pilot.pause()
            assert app.kanban_presentation == name
            text = _text(_painted(app))
            assert text[0].rstrip().endswith("25 tasks")
            assert not any(t in "\n".join(text[1:]) for t in MS_TITLES), name
        await pilot.press("tab")                  # back to grouped
        await pilot.pause()
        app.selected_task_id = "tw6"              # SEO redirects map (Backlog)
        app.refresh_view()
        await pilot.pause()
        await pilot.press("M")
        await pilot.pause()
        assert app.board.task_by_id("tw6").milestone is True
        nxt = app.selected_task_id
        assert nxt not in kg_board.MILESTONE_IDS | {"tw6"}
        assert any(nxt in col for col in app._nav_columns())
        before = app.board.phase_index(app.board.task_by_id(nxt))
        await pilot.press("right_square_bracket")
        await pilot.pause()
        assert app.board.phase_index(app.board.task_by_id(nxt)) == before + 1
        assert app.board.task_by_id("tw6").phase == "Backlog"
    path.write_bytes(original)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        rows = _painted(app)
        ops = next(r for r in rows if "".join(c for c, _ in r).startswith("▐ Ops & Security"))
        line = "".join(c for c, _ in ops)
        i = line.index("Security review sign-off · 2d late")
        assert ops[line.index("2d late", i)][1] == HEX["over"].lower()
        assert ops[line.index("◆", i - 12)][1] == HEX["over"].lower()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        web = next(r for r in _text(_painted(app)) if r.startswith("▐ Website Redesign"))
        assert f"◆ {_md(today + timedelta(days=10))} · in 10d" in web
