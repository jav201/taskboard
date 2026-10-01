"""Kanban priority — K4 band + badges (owner verdict 2026-09-30).

Field report (Javier): "KANBAN necesita algunos cues de color o tamaño (o
algo) para diferenciar tareas con alta prioridad." The shipped cue was one `!`
in the neutral ink tone at the right edge of a card — legible only if you
already knew to look for it. The round offered four answers; the verdict took
two of them:

- K4, the BAND: inside each column the open high-priority cards float to the
  top under a `── high ──` divider closed by a rule. It goes through the one
  ordering seat (`kanban_order`), so the cursor walks exactly what is drawn —
  the F-3 law: nav order IS draw order, and the cursor never rests on a card
  the view does not draw.
- the BADGES from K3, in Javier's words "el uso de insignias, reusando !!, ==
  y ++ para 3 colores": every OPEN card wears a reverse-video badge in the
  notes highlight vocabulary — `!!` red (high), `==` yellow (normal), `++`
  green (low). Done and archived cards wear none: finished work rests.

Batch 2026-09-30-batch-01 · HLR-003 / HLR-004.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from rich.cells import cell_len

from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard import views
from taskboard.views import (_KANBAN_GROUP_MODES, _KANBAN_SORT_MODES, HEX, _strip,
                             card_cell, help_example, kanban_order, legend_entries,
                             nav_model, render_kanban)

# read tolerantly so the base tree reports RED per node, not one import error
KANBAN_BAND = getattr(views, "KANBAN_BAND", "<no band on this tree>")

TODAY = date(2026, 9, 30)
PHASES = ["Backlog", "Doing", "Review", "Done"]
BADGE = {"high": ("!!", "over"), "normal": ("==", "soon"), "low": ("++", "green")}


def _board(path: Path) -> Board:
    """Doing holds two open highs in DIFFERENT projects (board order puts B's
    first, so a band built by walking project groups would order them wrong
    under sort=project), a BLOCKED high, an ARCHIVED high, a normal and a low;
    Done holds a finished high. Dates and phase stamps differ so every sort
    mode actually reorders something."""
    a = Project("Alpha", "sky")
    b = Project("Bravo", "lime")
    tasks = [
        Task("Bravo urgent", b.id, "Doing", "high", due_date="2026-10-09",
             phase_changed="2026-09-20", id="hb"),
        Task("Alpha urgent", a.id, "Doing", "high", due_date="2026-10-01",
             phase_changed="2026-09-28", id="ha"),
        Task("Alpha blocked", a.id, "Doing", "high", blocked=True,
             due_date="2026-10-05", phase_changed="2026-09-25", id="hx"),
        Task("Alpha shelved", a.id, "Doing", "high", archived=True, id="har"),
        Task("Alpha plain", a.id, "Doing", "normal", due_date="2026-10-02",
             phase_changed="2026-09-29", id="na"),
        Task("Bravo someday", b.id, "Doing", "low", id="lb"),
        Task("Loose idea", None, "Backlog", "high", due_date="2026-10-20", id="hi"),
        Task("Loose chore", None, "Backlog", "normal", id="ni"),
        Task("Shipped thing", a.id, "Done", "high", phase_changed="2026-09-27",
             id="hd"),
    ]
    return Board([a, b], tasks, path, phases=PHASES)


def _open_high(board, tasks):
    return [t for t in tasks if t.priority == "high"
            and not board.is_done(t) and not t.archived]


# --------------------------------------------------------------------------- #
# LLR-003.1 — the band lives in the ONE ordering seat
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("sort", _KANBAN_SORT_MODES)
def test_seat_band_holds_the_open_highs_in_the_sorts_order(tmp_path, sort):
    """The band is a group like any other: the column's open high cards, in
    the order the active sort gives a group. Oracle from a DIFFERENT path
    through the seat: the `High` group of group=priority under the same sort,
    minus done/archived. RED: a band assembled by walking the project groups
    orders `Bravo urgent` after `Alpha urgent` under sort=project."""
    b = _board(tmp_path / "b.json")
    doing = [t for t in b.tasks if t.phase == "Doing"]
    for show_archived in (False, True):
        col = [t for t in doing if show_archived or not t.archived]
        groups = kanban_order(b, col, show_archived, sort=sort, band=True)
        assert groups[0][0] == KANBAN_BAND
        oracle = next(items for name, _c, items in
                      kanban_order(b, col, show_archived, group="priority", sort=sort)
                      if name == "High")
        assert [t.id for t in groups[0][2]] == \
            [t.id for t in oracle if not t.archived], (sort, show_archived)
        rest = [t.id for _n, _c, items in groups[1:] for t in items]
        assert not set(rest) & {t.id for t in groups[0][2]}, "a card drawn twice"
        assert sorted(rest + [t.id for t in groups[0][2]]) == sorted(t.id for t in col)


def test_seat_band_skips_done_archived_and_the_priority_grouping(tmp_path):
    """Finished or put-away work does not shout; with group=priority the
    `High` group already IS the band, so a second one would draw every high
    card twice; a collapsed column contributes nothing; no open high, no
    band. RED: build the band from `priority == "high"` alone -> `hd` and
    `har` land in it."""
    b = _board(tmp_path / "b.json")
    done = [t for t in b.tasks if t.phase == "Done"]
    assert kanban_order(b, done, True, band=True)[0][0] != KANBAN_BAND
    doing = [t for t in b.tasks if t.phase == "Doing"]
    band = kanban_order(b, doing, True, band=True)[0][2]
    assert {"hd", "har"}.isdisjoint(t.id for t in band)
    assert "hx" in {t.id for t in band}, "a blocked high is still open work"
    assert all(n != KANBAN_BAND for n, _c, _i in
               kanban_order(b, doing, False, group="priority", band=True))
    assert kanban_order(b, doing, False, band=True, collapsed=True) == []
    plain = [t for t in doing if t.priority != "high"]
    assert all(n != KANBAN_BAND for n, _c, _i in kanban_order(b, plain, False, band=True))


def test_seat_band_respects_the_project_focus(tmp_path):
    """The focus filter runs FIRST: a focused board's band holds only the
    focused project's highs. RED: band taken before the focus filter ->
    `Bravo urgent` floats into Alpha's focused board."""
    b = _board(tmp_path / "b.json")
    alpha = b.projects[0].id
    doing = [t for t in b.tasks if t.phase == "Doing"]
    band = kanban_order(b, doing, False, band=True, focus=alpha)[0][2]
    assert [t.id for t in band] == ["ha", "hx"]


@pytest.mark.parametrize("group", _KANBAN_GROUP_MODES)
@pytest.mark.parametrize("sort", _KANBAN_SORT_MODES)
def test_seat_without_band_is_unchanged(tmp_path, group, sort):
    """Preservation: `band` defaults to False and every caller that does not
    ask for it (lanes, matrix) gets exactly the groups it got before. GREEN on
    base by design; RED under the mutation "default band=True"."""
    b = _board(tmp_path / "b.json")
    doing = [t for t in b.tasks if t.phase == "Doing"]
    assert kanban_order(b, doing, False, group=group, sort=sort, today=TODAY) == \
        kanban_order(b, doing, False, group=group, sort=sort, today=TODAY, band=False)
    assert all(n != KANBAN_BAND for n, _c, _i in
               kanban_order(b, doing, False, group=group, sort=sort, today=TODAY))


# --------------------------------------------------------------------------- #
# AT-003 — the band is drawn, and the cursor walks what is drawn
# --------------------------------------------------------------------------- #
def _render(b, **kw):
    lm: dict = {}
    text = render_kanban(b, kw.pop("show_archived", False), None, today=TODAY,
                         width=140, height=0, line_map=lm, **kw)
    return text.plain.split("\n"), lm


@pytest.mark.parametrize("group", _KANBAN_GROUP_MODES)
@pytest.mark.parametrize("sort", _KANBAN_SORT_MODES)
@pytest.mark.parametrize("focus", [False, True])
@pytest.mark.parametrize("show_archived", [False, True])
def test_band_is_drawn_and_nav_walks_the_draw_order(tmp_path, group, sort, focus,
                                                    show_archived):
    """AT-003 (HLR-003). Over EVERY group × sort the seat declares (read from
    the seat's own tuples, C-31) × focus × show_archived, in the grouped
    presentation: (1) every column's nav order is its cards' top-to-bottom
    draw order — the F-3 law; (2) where a column has open highs and the group
    is not `priority`, they come first, under a painted `── high ──` divider;
    (3) no done or archived card sits in the band. RED on base: no divider;
    RED if nav forgets `band=True` while the renderer asks: order mismatch."""
    b = _board(tmp_path / "b.json")
    fid = b.projects[0].id if focus else None
    lines, lm = _render(b, presentation="grouped", sort=sort, group=group,
                        focus=fid, show_archived=show_archived)
    cols = nav_model("kanban", b, show_archived, TODAY, 140, selected_id=None,
                     kanban_sort=sort, kanban_group=group, kanban_focus=fid,
                     presentation="grouped")
    drawn = {tid for col in cols for tid in col}
    assert drawn == set(lm), "nav and draw disagree on WHICH cards exist"
    for col in cols:
        assert col == sorted(col, key=lambda tid: lm[tid]), \
            f"{group}/{sort}: nav order is not draw order: {col}"
    doing = [t for t in b.tasks if t.phase == "Doing"
             and (show_archived or not t.archived)
             and (fid is None or t.project_id == fid)]
    want = _open_high(b, doing)
    doing_col = next(c for c in cols if set(c) & {t.id for t in doing})
    if group == "priority":
        assert not any("── high" in ln for ln in lines)
        return
    assert set(doing_col[:len(want)]) == {t.id for t in want}
    # the divider must be in the DOING column's own cells — Backlog has a band
    # too, and a whole-row search would let its divider answer for Doing's
    hdr = next(ln for ln in lines if all(p.upper() in ln for p in PHASES))
    seps = [-1] + [x for x, ch in enumerate(hdr) if ch == "│"] + [len(hdr)]
    ci = next(i for i in range(len(seps) - 1) if "DOING" in hdr[seps[i] + 1:seps[i + 1]])
    first = lm[doing_col[0]]
    cell = lines[first - 1][seps[ci] + 1:seps[ci + 1]]
    assert "── high" in cell, f"no divider above Doing's band: {cell!r}"
    done_ids = {t.id for t in b.tasks if b.is_done(t) or t.archived}
    assert not done_ids & set(doing_col[:len(want)])


@pytest.mark.parametrize("presentation", ["lanes", "matrix"])
def test_lanes_and_matrix_draw_no_band(tmp_path, presentation):
    """D1: the band belongs to the grouped presentation. Lanes already group
    on their own axis (a band there would be a pseudo-lane named by a
    sentinel — the prototype's `\\x00high` lane), and matrix draws counts, not
    cards. RED: the seat applies the band for every caller -> lanes grow a
    lane for it."""
    b = _board(tmp_path / "b.json")
    lines, _lm = _render(b, presentation=presentation)
    assert not any("── high" in ln or "\x00" in ln for ln in lines)


async def test_the_cursor_walks_the_band_first_in_the_app(tmp_path):
    """AT-003 through the keys (Q-6): in the running app, from the top of the
    Doing column, `down` visits the open highs first — in the band's order —
    then the rest; it never lands on the archived high it does not draw."""
    b = _board(tmp_path / "b.json")
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        app.view_mode = "kanban"
        app.selected_task_id = "hb"
        app.refresh_view()
        await pilot.pause()
        for _ in range(4):
            await pilot.press("up")
        seen = [app.selected_task_id]
        for _ in range(4):
            await pilot.press("down")
            await pilot.pause()
            seen.append(app.selected_task_id)
        assert seen[:3] == ["hb", "ha", "hx"], seen
        assert "har" not in seen


async def test_a_card_raised_to_high_joins_the_band_and_keeps_the_cursor(tmp_path):
    """AT-006 (HLR-003, UX-5): raising the selected card to high with the
    priority key moves it INTO the band and the cursor goes with it; cycling
    on to low moves it OUT again, cursor still on it."""
    from taskboard.keymap import KEYMAP
    key = next(k for k in KEYMAP if k.action == "prio_cycle").keys.split(",")[0]
    b = _board(tmp_path / "b.json")
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        app.view_mode = "kanban"
        app.selected_task_id = "na"
        app.refresh_view()
        await pilot.pause()
        await pilot.press(key)                       # normal -> high
        await pilot.pause()
        assert app.selected_task_id == "na"
        lines, lm = _render(app.board, presentation="grouped")
        band_rows = sorted(lm[t] for t in ("hb", "ha", "hx", "na"))
        assert band_rows == list(range(band_rows[0], band_rows[0] + 4)), \
            "the raised card is not inside the band"
        await pilot.press(key)                       # high -> low
        await pilot.pause()
        assert app.selected_task_id == "na"
        lines, lm = _render(app.board, presentation="grouped")
        assert lm["na"] > lm["hx"] + 1, "the lowered card is still in the band"


# --------------------------------------------------------------------------- #
# LLR-004.1 / AT-004 — the badges
# --------------------------------------------------------------------------- #
def test_card_badge_per_priority_and_none_when_finished(tmp_path):
    """LLR-004.1. One vocabulary with the notes: `!!` over, `==` soon, `++`
    green, in reverse video, before the title; the old `!` ink token is gone
    from a badged card; done and archived cards wear nothing. RED: badge a
    done card -> `Shipped thing` shouts."""
    b = _board(tmp_path / "b.json")
    by = {t.id: t for t in b.tasks}
    for tid, prio in (("ha", "high"), ("na", "normal"), ("lb", "low")):
        token, tone = BADGE[prio]
        m = card_cell(by[tid], b, 40, False, prefix="▊ ", today=TODAY, badge=True)
        assert f"reverse {HEX[tone]}]{token}[/]" in m, (tid, m)
        assert _strip(m).startswith(f"▊ {token} "), _strip(m)
        assert _strip(m).count("!") == (2 if prio == "high" else 0), m
    for tid in ("hd", "har"):
        m = card_cell(by[tid], b, 40, False, prefix="▊ ", today=TODAY, badge=True)
        assert not any(tok in _strip(m)[2:4] for tok, _t in BADGE.values()), m
        assert "reverse" not in m


@pytest.mark.parametrize("wc", range(0, 41))
def test_badged_cards_are_exactly_their_width(tmp_path, wc):
    """The width law every card obeys: a badge never pushes a row past its
    column, at any width down to 0 (the badge sheds before the cell lies)."""
    b = _board(tmp_path / "b.json")
    for t in b.tasks:
        m = card_cell(t, b, wc, wc % 3 == 0, prefix="▲ " if t.blocked else "▊ ",
                      today=TODAY, badge=True)
        assert cell_len(_strip(m)) == wc, (t.id, wc, _strip(m))


def test_unknown_priority_wears_the_normal_badge(tmp_path):
    """The seat ranks an unknown priority as normal (`_PRIO_RANK.get(.., 1)`);
    the badge agrees instead of inventing a fourth mark."""
    b = _board(tmp_path / "b.json")
    t = Task("Odd", None, "Doing", "urgent")
    b.tasks.append(t)
    assert "==" in _strip(card_cell(t, b, 30, False, prefix="▊ ", badge=True))


def _painted_badges(app):
    """(token, hex, reverse) for every painted 2-cell badge on screen."""
    out = []
    for strip in app.screen._compositor.render_strips(app.screen.size):
        for seg in strip:
            if seg.text in ("!!", "==", "++") and seg.style is not None:
                col = seg.style.color
                out.append((seg.text,
                            col.triplet.hex.lower() if col and col.triplet else None,
                            bool(seg.style.reverse)))
    return out


@pytest.mark.parametrize("presentation", ["grouped", "lanes"])
async def test_the_app_paints_a_badge_on_every_open_card(tmp_path, presentation):
    """AT-004 (HLR-004) through the running app, in both presentations that
    draw cards: one reverse badge per open card in the right tone, none for
    done or archived work. The fixture's visible open cards: 4 high (hb, ha,
    hx, hi), 2 normal (na, ni), 1 low (lb). RED on base: `!` ink and no
    `==`/`++` at all."""
    b = _board(tmp_path / "b.json")
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app.run_test(size=(160, 40)) as pilot:
        await pilot.pause()
        app.view_mode = "kanban"
        app.kanban_presentation = presentation
        app.refresh_view()
        await pilot.pause()
        badges = _painted_badges(app)
        counts = {tok: sum(1 for t, _h, _r in badges if t == tok) for tok in ("!!", "==", "++")}
        assert counts == {"!!": 4, "==": 2, "++": 1}, (presentation, badges)
        for tok, hexv, rev in badges:
            want = {"!!": "over", "==": "soon", "++": "green"}[tok]
            assert rev and hexv == HEX[want], (tok, hexv, rev)


# --------------------------------------------------------------------------- #
# LLR-004.2 — the legend and the help say what is drawn
# --------------------------------------------------------------------------- #
def test_legend_lists_the_badges_that_are_on_the_board(tmp_path):
    """The no-ghost law, on the new marks: each badge is explained only when
    a visible open card of that priority exists, and the retired `!` entry is
    gone. RED: keep the `!` entry -> it explains a mark no kanban card draws."""
    b = _board(tmp_path / "b.json")
    swatches = [_strip(s) for s, _m in legend_entries("kanban", b, TODAY, 140, 40)]
    assert {"!!", "==", "++"} <= set(swatches)
    assert "!" not in swatches
    b.tasks[:] = [t for t in b.tasks if t.priority != "low"]
    swatches = [_strip(s) for s, _m in legend_entries("kanban", b, TODAY, 140, 40)]
    assert "++" not in swatches and "==" in swatches


def test_help_example_shows_a_badge_and_says_the_band_is_grouped_only():
    from taskboard.views import help_usage
    line, meaning = help_example("kanban")
    assert line.startswith("▊ !!") and " ! " not in line, line
    assert "!!" in meaning
    usage = " ".join(" ".join(b) for _h, b in help_usage("kanban"))
    assert "high" in usage and "grouped" in usage
