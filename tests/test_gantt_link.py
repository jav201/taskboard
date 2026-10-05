"""`L` in the gantt: the link mode drawn on the chart (batch 2026-10-04-batch-01,
HLR-502, LLR-502.3, D-A).

Field report: linking was a list detached from the dates (DEPS-CONTRACT.md) — nothing
showed what waiting on a task would do to the plan. The operator's verdict frame D-A:
in the gantt, `L` keeps the chart on screen, walks the candidates in the chart's own
order, draws the proposed link where the dates are (a connector from the candidate's
due, the overlap days as `═` on the waiter's row) and marks the rows that would loop.

Law: the overlay writes on the FIELD only (never the label column or the gutter), the
`═` cells are exactly the overlap days (the one measure, D-503), a loop is never a
candidate, and the status rows carry board text as Text pieces (S1). Synthetic boards
only.
"""
from __future__ import annotations

import json
from datetime import date

import pytest
from rich.cells import cell_len

import kg_board
import taskboard.views as views
from kg_board import TODAY
from taskboard.app import TaskboardApp
from taskboard.modals import GanttLinkMode
from taskboard.models import loopers_of

DUE_GLYPHS = set("○◔◑◕●")
BAR_START = set("╌▬")


def _frame(b, waiter, cand, width=118, height=27, *, overlay=True, monkeypatch=None):
    w, c = b.task_by_id(waiter), b.task_by_id(cand) if cand else None
    loops = loopers_of(b, w)
    if not overlay:
        monkeypatch.setattr(views, "gantt_link_overlay",
                            lambda *a, **k: {"overlap": [], "connector": []})
    text, facts = views.gantt_link_frame(b, False, w, c, TODAY, width, height, "r", loops)
    return text.plain.split("\n"), facts


def _row(rows, title):
    hits = [i for i, r in enumerate(rows) if r[2:].startswith(title)]
    assert len(hits) == 1, (title, hits)
    return hits[0]


def test_TC_511_the_overlap_is_exactly_the_overlap_days(monkeypatch):
    """TC-511 (LLR-502.3), threshold: waiter `tw5` (Launch new homepage) and
    candidate `tm3` (due 9 days into tw5 — P1 oracle "◂ overlaps 9d") at 118x30
    (1 cell = 1 day): the `═` cells on tw5's row run from tw5's bar start to the
    column of tm3's due glyph in the SAME frame drawn without the overlay — 9 cells;
    every connector cell is right of the gutter, starts one cell after tm3's due and
    joins tm3's row to tw5's. RED: `═` over one day too many, an overlay into the
    label column."""
    b = kg_board.build()
    plain, _ = _frame(b, "tw5", "tm3", overlay=False, monkeypatch=monkeypatch)
    monkeypatch.undo()
    rows, facts = _frame(b, "tw5", "tm3")
    lw = facts["label_w"]
    rw, rc = _row(plain, "Launch new homepage"), _row(plain, "Add push notifications")
    start = min(i for i, ch in enumerate(plain[rw]) if i > lw and ch in BAR_START)
    due = max(i for i, ch in enumerate(plain[rc]) if i > lw and ch in DUE_GLYPHS)
    assert facts["overlap"] == list(range(start, due + 1))
    assert len(facts["overlap"]) == 9
    assert all(rows[rw][x] == "═" for x in facts["overlap"])
    assert rows[rw][:lw + 1] == plain[rw][:lw + 1]               # label and gutter untouched
    cells = facts["connector"]
    assert cells and all(col > lw for _r, col in cells)
    assert {col for _r, col in cells} == {due + 1}
    assert {r for r, _c in cells} <= set(range(min(rw, rc), max(rw, rc) + 1))
    assert (rc, due + 1) in cells                                 # it leaves the candidate's row
    for r, col in cells:
        assert plain[r][col] in views.LINK_BACKGROUND             # over background only
        assert rows[r][col] in "╮╯│"
    # the tones (qa G-002): `═` in the over tone, the connector in the bright tone
    from rich.console import Console
    text, _ = views.gantt_link_frame(b, False, b.task_by_id("tw5"), b.task_by_id("tm3"),
                                     TODAY, 118, 27, "r", loopers_of(b, b.task_by_id("tw5")))
    lines = text.split("\n")
    def tones(r, glyphs):
        segs = lines[r].render(Console(width=200))
        return {s.style.color.triplet.hex.lower() for s in segs
                if s.style and s.style.color and any(g in s.text for g in glyphs)}
    assert tones(rw, "═") == {views.HEX["over"].lower()}
    assert tones(rc, "╮╯") == {views.HEX["bright"].lower()}


@pytest.mark.parametrize("waiter,cand,overlaps", [
    ("tw5", "tw2", False),       # candidate ABOVE the waiter, due before it starts
    ("tw5", "td5", True),        # its due far right (Nov 29)
    ("ta2", "td2", False),       # waiter with no start: no `═` even though it overlaps
    ("tw5", "to4", False),       # candidate with no due: nothing to draw from
])
def test_TC_511_boundaries(waiter, cand, overlaps):
    """TC-511 boundary catalog: above / below, the due off the window, no overlap,
    no start, no due. Every written cell stays right of the gutter."""
    b = kg_board.build()
    rows, facts = _frame(b, waiter, cand)
    lw = facts["label_w"]
    assert bool(facts["overlap"]) is overlaps
    assert all(col > lw for col in facts["overlap"])
    assert all(col > lw for _r, col in facts["connector"])
    assert all(len(r) <= 118 for r in rows)
    if cand == "to4":
        assert facts["connector"] == []


def test_TC_511_loop_rows_wear_the_mark_in_the_gutter():
    """`⟲` sits in the gutter column of each loop row (`tw6` once it waits on
    `tw5`), and the header counts it. RED: the mark dropped, written in the label."""
    b = kg_board.build()
    b.task_by_id("tw6").depends_on.append("tw5")
    w = b.task_by_id("tw5")
    text, facts = views.gantt_link_frame(b, False, w, b.task_by_id("tw2"), TODAY, 118, 27,
                                         "24 candidates · ⟲1 would loop", {"tw6"})
    rows = text.plain.split("\n")
    assert rows[0].startswith("◆ GANTT · LINK") and rows[0].rstrip().endswith("⟲1 would loop")
    r = _row(rows, "SEO redirects map")
    assert rows[r][facts["label_w"]] == "⟲"
    assert sum(row.count("⟲") for row in rows[1:]) == 1


def _painted(app) -> list[str]:
    strips = app.screen._compositor.render_strips(app.screen.size)
    return ["".join(seg.text for seg in s) for s in strips]


def _toasts(app) -> list[str]:
    return [str(t.render()) for t in app.screen.query("Toast")]


async def _link_mode(pilot, app, waiter="tw5"):
    await pilot.press("3")
    app.clear_notifications()
    app.selected_task_id = waiter
    await pilot.press("L")
    await pilot.pause()
    assert isinstance(app.screen, GanttLinkMode)
    return app.screen


def _board(tmp_path, mutate=None):
    path = tmp_path / "board.json"
    b = kg_board.shifted(path)
    b.task_by_id("tw6").depends_on.append("tw5")
    if mutate:
        mutate(b)
    b.save()
    return path


async def test_TC_512_the_cycle_skips_loops_and_follows_the_filter(tmp_path):
    """TC-512 (LLR-502.3): the cursor starts on the first candidate in gantt order;
    ↓ through a full turn visits every open task but the waiter and the loop
    (`tw6`) once each, in gantt order; with the filter `ma` it visits only titles
    holding "ma"; `backspace` widens it again; a filter matching nothing leaves no
    candidate and ↵ does nothing. RED: the loop row reachable, the filter ignored."""
    path = _board(tmp_path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30)) as pilot:
        scr = await _link_mode(pilot, app)
        # the oracle is the shipped gantt's own paint (code review F2): rows top to
        # bottom with every group unfolded (a frame tall enough), open tasks only
        line_map: dict[str, int] = {}
        views._gantt_frame(app.board, False, None, date.today(), 118, 500, line_map)
        drawn = sorted((r, i) for i, r in line_map.items()
                       if app.board.task_by_id(i) is not None)
        want = [i for _r, i in drawn
                if i not in ("tw5", "tw6") and app.board.task_by_id(i).phase != app.board.phases[-1]
                and not app.board.task_by_id(i).archived]
        seen = [scr.candidate.task.id]
        for _ in range(len(want) - 1):
            await pilot.press("down")
            seen.append(scr.candidate.task.id)
        assert seen == want and len(want) == 23
        await pilot.press("down")
        assert scr.candidate.task.id == want[0]                  # it wraps
        await pilot.press("up")
        assert scr.candidate.task.id == want[-1]
        await pilot.press("m", "a")
        hits = set()
        for _ in range(8):
            hits.add(scr.candidate.task.id)
            await pilot.press("down")
        titles = {app.board.task_by_id(i).title for i in hits}
        assert titles and all("ma" in t.lower() for t in titles), titles
        assert titles == {app.board.task_by_id(i).title for i in want
                          if "ma" in app.board.task_by_id(i).title.lower()}
        await pilot.press("backspace", "backspace")
        assert scr.filter == ""
        await pilot.press("z", "z", "z")
        assert scr.candidate is None
        before = json.loads(path.read_text(encoding="utf-8"))
        await pilot.press("enter")
        assert isinstance(app.screen, GanttLinkMode)
        assert "no match" in "\n".join(_painted(app))
        assert json.loads(path.read_text(encoding="utf-8")) == before


async def test_TC_512_keys_are_painted_at_80_columns(tmp_path):
    """TC-512 threshold: at 80x24 all four keys are painted, for a candidate and for
    a linked one ("↵ unlink", "✓ linked"); titles clip first. RED: keys on the title
    row, dropped past the edge."""
    path = _board(tmp_path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(80, 24)) as pilot:
        scr = await _link_mode(pilot, app)
        assert scr.candidate.linked                               # tw2: tw5 waits on it
        screen = "\n".join(_painted(app))
        for key in ("↑↓ choose", "type to filter", "↵ unlink", "esc cancel"):
            assert key in screen, key
        assert "✓ linked" in screen
        while scr.candidate.linked:
            await pilot.press("down")
        screen = "\n".join(_painted(app))
        for key in ("↑↓ choose", "type to filter", "↵ link", "esc cancel"):
            assert key in screen, key
        assert all(len(r) <= 80 for r in _painted(app))


@pytest.mark.parametrize("arm", ["wide-title", "long-filter"])
async def test_TC_512_keys_survive_wide_titles_and_a_long_filter(tmp_path, arm):
    """TC-512, code review F1: at 80x24 a waiter titled in wide glyphs (each two
    cells) or a filter longer than the screen still leaves the keys row painted —
    titles and the filter clip to cells, not characters. RED: a clip by `len()`, an
    unclipped filter (the first row wraps and pushes the keys out)."""
    def mutate(b):
        if arm == "wide-title":
            b.task_by_id("tw5").title = "🚀" * 15 + " 新しいホームページを公開する"
            b.task_by_id("tw2").title = "Pick a component library for the whole redesign team"
    path = _board(tmp_path, mutate)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(80, 24)) as pilot:
        scr = await _link_mode(pilot, app)
        if arm == "long-filter":
            await pilot.press(*("p" * 90))
            assert scr.filter == "p" * 90
        rows = _painted(app)
        assert any("↑↓ choose · type to filter" in r and "esc cancel" in r for r in rows), rows[-4:]
        link_rows = [r for r in rows if r.startswith(" LINK ")]
        assert len(link_rows) == 1
        # the row still says what is linked: the filter clips before the titles do,
        # and a wide title is measured in cells, so "✓ linked" is not cut away
        assert "waits on…" in link_rows[0]
        if arm == "wide-title":
            assert "✓ linked" in link_rows[0] and "Pick a" in link_rows[0], link_rows[0]
        # whatever the glyphs and however narrow, the first status row is one row
        for width in (24, 40):
            first = scr._status(scr.candidate, width).plain.split("\n")[0]
            assert cell_len(first) <= width - 1, (width, first)


async def test_TC_512_link_mode_keeps_the_waiters_group_open(tmp_path):
    """TC-512, operator D-528 "Corregirlo antes del push" (ux F4): in link mode the
    waiting task's project group is pinned open in the fold allocation, so at
    118x20 — where the greedy fold used to fold it for a candidate in another
    project — its row is drawn with the `═` overlap on it and no fold note; a
    group with nothing to do with the link folds instead. Outside link mode the
    gantt's fold rule is unchanged: the same frame without the pin still folds
    the waiter's group. RED: the waiter's group folded at 118x20 (A-8's note)."""
    path = _board(tmp_path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 20)) as pilot:
        await _link_mode(pilot, app)
        await pilot.press(*"push")
        rows = _painted(app)
        waiter = [r for r in rows if r.startswith("  Launch new homepage")]
        assert len(waiter) == 1 and "═" in waiter[0], rows
        assert not any("folded" in r for r in rows)
        assert any(r.startswith("  Add push notifications") for r in rows)
        board = app.board
    # shorter still (118x14: two rows left for both groups' tasks) the two groups
    # SHARE them — each paged to its own task — rather than both folding
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 14)) as pilot:
        await _link_mode(pilot, app)
        await pilot.press(*"push")
        rows = _painted(app)
        assert any(r.startswith("  Launch new homepage") for r in rows), rows
        assert any(r.startswith("  Add push notifications") for r in rows), rows
        assert not any("folded" in r for r in rows)
    groups = views.gantt_plan(board, False, "tm3", date.today(), 14)
    website = [g for g in groups if g.project is not None and g.project.name == "Website Redesign"]
    assert website and not website[0].unfolded                  # the shipped rule, untouched


async def test_TC_512_a_folded_waiter_row_is_said(tmp_path):
    """TC-512, ux F4 (P4), kept as the FALLBACK after D-528: the waiter's group is
    pinned open, but where the rows are genuinely too few to draw it beside the
    candidate's (118x12: one row left for both groups' tasks, the selection
    takes it) the overlay has no row to draw on — the hint row says so instead
    of the link vanishing in silence; when both rows fit nothing is said. RED:
    the overlay gone and no word (candidate `Add push notifications`)."""
    path = _board(tmp_path)
    app = TaskboardApp(board_path=str(path))
    note = "Launch new homepage is folded — a taller terminal draws the link"
    async with app.run_test(size=(118, 12)) as pilot:
        await _link_mode(pilot, app)
        await pilot.press(*"push")
        rows = _painted(app)
        assert not any(r.startswith("  Launch new homepage") for r in rows)
        assert any(note in r for r in rows), rows[-3:]
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30)) as pilot:
        await _link_mode(pilot, app)
        await pilot.press(*"push")
        rows = _painted(app)
        assert any(r.startswith("  Launch new homepage") for r in rows)
        assert not any(note in r for r in rows)
    # at 80 columns the reason stays, in its short form, whatever the title (code review 005 N1)
    def long_title(b):
        b.task_by_id("tw5").title = "🚀" * 12 + " 新しいホームページを公開する and more words"
    (tmp_path / "long").mkdir()
    path = _board(tmp_path / "long", long_title)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 12)) as pilot:
        await _link_mode(pilot, app)
        await pilot.press(*"push")
        hint = [r for r in _painted(app) if r.startswith(" ◂ overlaps")]
        assert len(hint) == 1 and hint[0].rstrip().endswith(
            "is folded — a taller terminal draws the link"), hint     # the title clipped, not the reason
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(80, 12)) as pilot:
        await _link_mode(pilot, app)
        await pilot.press(*"push")
        rows = _painted(app)
        assert any("· waiter row folded" in r for r in rows), rows[-3:]   # the short form
        assert any("↑↓ choose · type to filter" in r and "esc cancel" in r for r in rows)
        # a closed waiter is never drawn at any height: no note (code review 005 N2)
        await pilot.press("escape")
        done = app.board.task_by_id("tw1")
        app.push_screen(GanttLinkMode(app.board, done, False, date.today()))
        await pilot.pause()
        await pilot.press(*"push")
        assert not any("folded" in r for r in _painted(app))


async def test_AT_503_link_in_the_gantt(tmp_path):
    """AT-503 (US-502): in the gantt, `L` on `Launch new homepage` paints the link
    mode — header, "24 candidates · ⟲1 would loop", `⟲` on `SEO redirects map`, the
    legend with the loop's path, the waiter and the candidate on the status row; ↵ on
    a free candidate saves the link (board file) with the toast; `L` again and ↵ on
    the linked one removes it; esc changes nothing."""
    path = _board(tmp_path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        scr = await _link_mode(pilot, app)
        screen = _painted(app)
        assert screen[0].startswith("◆ GANTT · LINK")
        assert "24 candidates · ⟲1 would loop" in screen[0]
        seo = [r for r in screen if r.startswith("  SEO redirects map")]
        assert len(seo) == 1 and "⟲" in seo[0]
        joined = "\n".join(screen)
        assert "⟲ loop: this → SEO redirects map → this" in joined
        while scr.candidate.linked:
            await pilot.press("down")
        pred = scr.candidate.task
        assert f"LINK Launch new homepage waits on… {pred.title}" in "\n".join(_painted(app))
        await pilot.press("enter")
        await pilot.pause()
        saved = {t["id"]: t for t in json.loads(path.read_text(encoding="utf-8"))["tasks"]}
        assert pred.id in saved["tw5"]["depends_on"]
        assert any(f"Launch new homepage waits on {pred.title} · u undo" in t
                   for t in _toasts(app)), _toasts(app)
        scr = await _link_mode(pilot, app)
        while scr.candidate.task.id != pred.id:
            await pilot.press("down")
        assert "↵ unlink" in "\n".join(_painted(app))
        await pilot.press("enter")
        await pilot.pause()
        saved = {t["id"]: t for t in json.loads(path.read_text(encoding="utf-8"))["tasks"]}
        assert pred.id not in saved["tw5"]["depends_on"]
        before = path.read_bytes()
        await _link_mode(pilot, app)
        await pilot.press("down", "escape")
        await pilot.pause()
        assert not isinstance(app.screen, GanttLinkMode)
        assert path.read_bytes() == before


async def test_AT_503_board_text_is_painted_as_text(tmp_path):
    """AT-503 (S1): a waiter titled with markup and a candidate titled with a
    bracketed tag are painted literally in the status row and the frame; no markup
    error, no style taken from them. RED: a title fed to a markup parser."""
    def mutate(b):
        b.task_by_id("tw5").title = "[bold red]w[/] home"
        b.task_by_id("tw2").title = "[link=x]lib[/link]"
    path = _board(tmp_path, mutate)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30)) as pilot:
        await _link_mode(pilot, app)
        screen = "\n".join(_painted(app))
        assert "LINK [bold red]w[/] home waits on… [link=x]lib[/link]" in screen
        assert "[link=x]lib[/link]" in screen.split("\n", 3)[3]   # the frame's label too


async def test_R2_2_create_on_a_one_phase_board_is_refused(tmp_path):
    """Code review R2-2 (increment 003's F4): on a one-phase board the first phase
    is the last, so a created task would be closed and its link refused — the create
    path says so and adds no task. RED: a closed task added and a silent refusal."""
    path = _board(tmp_path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        app.clear_notifications()
        n = len(app.board.tasks)
        app.board.phases = app.board.phases[:1]
        app._create_and_link(app.board.task_by_id("tw5"), "new prerequisite")
        await pilot.pause()
        assert len(app.board.tasks) == n
        assert any("a one-phase board has no open phase to create it in" in t
                   for t in _toasts(app)), _toasts(app)


def test_TC_512_one_page_holds_both_when_it_can():
    """TC-512, operator D-528 / code review 006 M1: when the waiter and the
    candidate are in the SAME over-tall group, the page is chosen to hold both
    whenever they are closer than a page — the fold note is for a page that
    genuinely cannot. Oracle: the full gantt's own row order (every group
    unfolded) and the number of the group's rows the frame drew; the waiter may be
    missing only if its distance to the candidate is at least that page.
    RED: a page aligned on the candidate alone (52 such frames at 118×14..16)."""
    b = kg_board.build()
    full: dict[str, int] = {}
    views._gantt_frame(b, False, None, TODAY, 118, 500, full)
    groups: dict[str, list[str]] = {}
    for tid in sorted(full, key=full.get):
        t = b.task_by_id(tid)
        if t is not None and t.phase != b.phases[-1] and not t.archived:
            groups.setdefault(views.gantt_group_key(b, t), []).append(tid)
    checked = 0
    for height in (11, 12, 13):
        for order in groups.values():
            for w in order:
                for c in order:
                    if w == c:
                        continue
                    _t, facts = views.gantt_link_frame(b, False, b.task_by_id(w), b.task_by_id(c),
                                                       TODAY, 118, height, "r", set())
                    drawn = [x for x in order if x in facts["line_map"]]
                    assert c in drawn
                    if w not in drawn:
                        assert abs(order.index(w) - order.index(c)) >= len(drawn), (height, w, c)
                    checked += 1
    assert checked > 100
