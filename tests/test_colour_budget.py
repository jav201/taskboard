"""The colour budget on the kanban and the gantt (round 7, `variants_polish.BUDGET`).

Batch 2026-10-02-batch-01 · HLR-108 · AT-106 · TC-117, TC-118, TC-119.

Field report (the operator, round 7): "too much green/cyan — the accent
(#2dd4bf) is overloaded (selection, critical path, variables, chips, keys)".
The budget: the accent marks what is being operated on, the critical path is
STRUCTURE (a heavy `━`, bold), not hue, and titles are bold bright. On these two
panels that leaves the accent on the `/` filter field and on today's marks
(decision D4: the today rule, today's number, the no-selection `today …` label);
the selection keeps its reverse video, as shipped. The keybar under the panel is
outside this law (decision D10: the app-wide pass is BACKLOG).

Every census here is over RENDERED spans — the form the terminal paints — and
each one first proves it can find the accent at all.
"""
from __future__ import annotations

import re
from datetime import date

import pytest

import kg_board
from kg_board import TODAY
from taskboard import app as app_mod
from taskboard import models, views
from taskboard.app import TaskboardApp
from taskboard.views import HEX, card_cell, render_view, reldue_token

ACCENT = HEX["accent"].lower()
# the same colour as Textual's `Style` spells it in the running app
ACCENT_RGB = "rgb({},{},{})".format(*(int(ACCENT[i:i + 2], 16) for i in (1, 3, 5)))
PRESENTATIONS = ("grouped", "lanes", "matrix")
GROUPS = ("project", "priority", "horizon")


def oracle():
    """The oracle board plus one card carrying a URL (the `↗` site)."""
    b = kg_board.build()
    b.task_by_id("tw6").urls = ["https://example.org/redirects"]
    return b


def accent_runs(text) -> list[tuple[int, str]]:
    """(row, painted text) of every run whose style carries the accent."""
    plain = text.plain
    starts = [0]
    for line in plain.split("\n"):
        starts.append(starts[-1] + len(line) + 1)
    out = []
    for s in text.spans:
        st = str(s.style).lower().replace(" ", "")
        if ACCENT in st or ACCENT_RGB in st:
            row = max(i for i, st in enumerate(starts) if st <= s.start)
            out.append((row, plain[s.start:s.end]))
    return out


def today_mark(row: int, seg: str) -> bool:
    """A today mark (D4): the today rule, today's number on the month row, the
    day-row tick lit because its cells cover today's column (LLR-102.2; at a
    coarse scale that tick can be another date — code review F2), or the
    no-selection `today …` label."""
    seg = seg.strip()
    return (set(seg) <= {views.RULE}
            or (row == 1 and seg == str(TODAY.day))
            or (row == 2 and seg.isdigit())
            or seg.startswith("today "))


# =========================================================================== #
# TC-119 — the census over every kanban presentation × group mode
# =========================================================================== #
def test_TC_119_the_kanban_paints_no_accent():
    """TC-119 (LLR-103.1, LLR-103.3). Every presentation × group mode is
    rendered — the reached pairs are asserted, not assumed — and none paints
    the accent: not the title, the `+Nd` token, the `↗` link, the horizon
    group's colour nor the matrix percent (P-4's sites)."""
    b = oracle()
    reached = set()
    for pres in PRESENTATIONS:
        for grp in GROUPS:
            for sort in ("project", "due"):
                for focus in (None, "pweb"):
                    for w, h in ((118, 30), (80, 24), (60, 20), (40, 14), (24, 10)):
                        text = render_view("kanban", b, False, "tw3", TODAY, w, h, {},
                                           presentation=pres, kanban_group=grp,
                                           kanban_sort=sort, kanban_focus=focus)
                        assert "KANBAN"[:3] in text.plain
                        reached.add((pres, grp, sort, focus, w))
                        runs = accent_runs(text)
                        assert not runs, (pres, grp, sort, focus, w, runs[:4])
    assert len(reached) == 3 * 3 * 2 * 2 * 5
    assert "↗" in render_view("kanban", b, False, "tw3", TODAY, 118, 30, {}).plain


def test_TC_119_the_census_can_see_the_accent():
    """Non-vacuity: the same detector finds today's rule on the gantt and the
    filter field on a filtered kanban — so an empty census means none."""
    b = oracle()
    gantt = render_view("gantt", b, False, "tw3", TODAY, 118, 30, {})
    assert any(views.RULE in seg for _r, seg in accent_runs(gantt))
    filt = render_view("kanban", b, False, "tw3", TODAY, 118, 30, {},
                       search_query="API")
    assert any(r in (1, 2) for r, _s in accent_runs(filt)), accent_runs(filt)


def test_TC_119_the_shared_card_tokens_left_the_accent_everywhere():
    """`card_cell` and `reldue_token` are shared: the Focus review rail, People
    and Agenda call them too (D10), so the two tokens leave the accent there as
    well — a `+4d` due within the week and a card's `↗` read `mut`."""
    b = oracle()
    t = b.task_by_id("tw6")
    t.due_date = "2026-10-04"
    assert reldue_token(t, TODAY, b) == ("+4d", "mut")
    cell = card_cell(t, b, 40, False, today=TODAY)
    assert "↗" in cell and ACCENT not in cell.lower() and HEX["mut"] in cell
    agenda = render_view("agenda", b, False, None, TODAY, 118, 30, {})
    assert not any("+4d" in seg or "↗" in seg for _r, seg in accent_runs(agenda))


# =========================================================================== #
# TC-117 / TC-118 — titles and the chain
# =========================================================================== #
@pytest.mark.parametrize("mode,pres", [("kanban", "grouped"), ("kanban", "lanes"),
                                       ("kanban", "matrix"), ("gantt", "grouped")])
def test_TC_117_the_title_is_bold_bright(mode, pres):
    """TC-117 (LLR-103.1). The view title is bold `bright`, not the accent."""
    text = render_view(mode, oracle(), False, "tw3", TODAY, 118, 30, {}, presentation=pres)
    word = "KANBAN" if mode == "kanban" else "GANTT"
    at = text.plain.index(word)
    styles = " ".join(str(s.style).lower() for s in text.spans if s.start <= at < s.end)
    assert HEX["bright"].lower() in styles and "bold" in styles, styles
    assert ACCENT not in styles


def test_TC_118_the_critical_chain_is_structure_not_hue():
    """TC-118 (LLR-103.2). The four chain tasks' reaches are `━` in bold
    bright (a flow packet may ride one cell); the header counts `chain 4` in
    `hd`; no chain cell wears the accent."""
    b = oracle()
    text = render_view("gantt", b, False, "tw3", TODAY, 118, 30, {})
    lines = text.plain.split("\n")
    assert re.search(r"\bchain 4\b", lines[0]) and "━ chain" not in lines[0]
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line) + 1)
    for tid in ("tm2", "tm3", "tm4", "tm5"):
        title = b.task_by_id(tid).title
        row = next(i for i, l in enumerate(lines) if title in l)
        cells = [starts[row] + x for x, ch in enumerate(lines[row]) if ch == "━"]
        assert cells, title
        for at in cells:
            st = " ".join(str(s.style).lower() for s in text.spans if s.start <= at < s.end)
            assert HEX["bright"].lower() in st and "bold" in st and ACCENT not in st, (title, st)


# =========================================================================== #
# AT-106 — the painted panels, through the app (US-103)
# =========================================================================== #
class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def frozen(monkeypatch):
    for mod in (views, app_mod, models):
        monkeypatch.setattr(mod, "date", _Today)


async def test_AT_106_the_panels_paint_the_accent_only_for_today_and_the_filter(
        tmp_path, frozen):
    """AT-106 (HLR-108). In the running app, the kanban panel (every layout)
    and the gantt panel paint the accent only on today's marks; with a `/`
    filter it also lights the filter field, and nothing else. RED on the base
    tree: the kanban title, the `+Nd` tokens and the gantt's `└─►` are accent."""
    b = oracle()
    b.path = tmp_path / "board.json"
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 34)) as pilot:
        await pilot.pause()
        for key in ("4", "tab", "tab", "3"):
            await pilot.press(key)
            await pilot.pause()
            text = app.query_one("#board").render()
            for row, seg in accent_runs(text):
                assert today_mark(row, seg), (app.view_mode, row, seg)
        assert any(views.RULE in seg for _r, seg in accent_runs(app.query_one("#board").render()))
        await pilot.press("/")
        await pilot.pause()
        for ch in "API":
            await pilot.press(ch)
        await pilot.press("enter")
        await pilot.pause()
        runs = accent_runs(app.query_one("#board").render())
        assert any(r in (1, 2) for r, _s in runs), "the filter field lost its accent"
        for row, seg in runs:
            assert row in (1, 2) or today_mark(row - 2, seg), (row, seg)


@pytest.mark.parametrize("w,h", [(118, 30), (80, 24), (60, 20), (40, 14), (24, 10)])
def test_TC_119_the_gantt_paints_only_today_and_the_filter(w, h):
    """TC-119 (code review F1, F2). The gantt at every width, with and without
    a focus and a filter: every accent run is a today mark or the filter field
    — including the clipped title of a narrow panel, which used to fall back to
    the accent."""
    b = oracle()
    for focus in (None, "pweb"):
        for query in (None, "e"):
            text = render_view("gantt", b, False, "tw3", TODAY, w, h, {},
                               gantt_focus=focus, search_query=query)
            for row, seg in accent_runs(text):
                if query and row in (1, 2):
                    continue                      # the filter field
                assert today_mark(row - (2 if query else 0), seg), (w, focus, query, row, seg)
