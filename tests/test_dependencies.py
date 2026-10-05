"""Tests for increment 3: block-becomes-task flow, ⛓N token, unblock sort."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest
from rich.cells import cell_len
from rich.text import Text

from taskboard.app import TaskboardApp
from taskboard.keymap import KEYMAP
from taskboard.models import Board, Project, Task, critical_chain, unblocks_count
from taskboard.views import HEX, _kanban_cell_order, card_cell, kanban_order, render_gantt


def _key_for(action: str) -> str:
    return next(k for k in KEYMAP if k.action == action).keys.split(",")[0]


def _board(tmp_path, *tasks, phases=None, name="board.json") -> Board:
    p = Project("Alpha", "sky")
    for t in tasks:
        t.project_id = p.id
    board = Board([p], list(tasks), tmp_path / name,
                  settings={"migrations": {"links": 1}},   # new-model data
                  phases=phases or ["Backlog", "Doing", "Review", "Done"])
    board.save()
    return board


# --------------------------------------------------------------------------- #
# AT-D1 (the block-becomes-task flow) is SUPERSEDED by batch 2026-10-04-batch-01
# (D-504, LLR-501.4): `b` is the external block only and no longer links; links
# are made with `L` (tests/test_link_picker.py) and `b` is pinned in
# tests/test_links.py (TC-506).
# --------------------------------------------------------------------------- #
async def test_unblock_on_blocked_task_flips_without_prompt(tmp_path):
    a = Task("A", phase="Doing", blocked=True, depends_on=["nope"])
    board = _board(tmp_path, a)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = a.id
        await pilot.press(_key_for("toggle_blocked"))
        await pilot.pause()
        # `b` never prompts (D-504): no screen is pushed
        assert len(app.screen_stack) == 1
        assert app.board.task_by_id(a.id).blocked is False
        # depends_on is untouched on unblock
        assert app.board.task_by_id(a.id).depends_on == ["nope"]


# --------------------------------------------------------------------------- #
# AT-D2: ⛓N token
# --------------------------------------------------------------------------- #
def test_unblocks_count_direct_open_dependents_only(tmp_path):
    p = Project("P", "sky")
    hub = Task("Hub", project_id=p.id, phase="Doing")
    d1 = Task("D1", project_id=p.id, phase="Backlog", depends_on=[hub.id])
    d2 = Task("D2", project_id=p.id, phase="Backlog", depends_on=[hub.id, "dangling"])
    done = Task("Done", project_id=p.id, phase="Done", depends_on=[hub.id])
    board = Board([p], [hub, d1, d2, done], tmp_path / "board.json")
    board.save()
    assert unblocks_count(board, hub) == 2
    assert unblocks_count(board, d1) == 0


def test_unblocks_token_absent_at_zero_and_present_at_two(tmp_path):
    p = Project("P", "sky")
    today = date(2026, 8, 15)
    hub = Task("Hub", project_id=p.id, phase="Doing",
               due_date=today.isoformat())
    d1 = Task("D1", project_id=p.id, phase="Backlog", depends_on=[hub.id])
    d2 = Task("D2", project_id=p.id, phase="Backlog", depends_on=[hub.id])
    board = Board([p], [hub, d1, d2], tmp_path / "board.json")
    board.save()
    # superseded by batch 2026-10-04-batch-01 (HLR-501): `⛓N` became `▸N` on
    # the predecessor, and the waiting card now says `◂N` (TC-504 in test_links)
    plain = Text.from_markup(card_cell(hub, board, 40, False, today=today)).plain
    assert "▸2" in plain and "⛓" not in plain
    plain_leaf = Text.from_markup(card_cell(d1, board, 40, False, today=today)).plain
    assert "◂1" in plain_leaf and "▸" not in plain_leaf


def test_unblocks_token_keeps_width_contract(tmp_path):
    p = Project("P", "sky")
    today = date(2026, 8, 15)
    hub = Task("Hub", project_id=p.id, phase="Doing",
               due_date=today.isoformat())
    deps = [Task(f"D{i}", project_id=p.id, phase="Backlog", depends_on=[hub.id])
            for i in range(5)]
    board = Board([p], [hub] + deps, tmp_path / "board.json")
    board.save()
    for wc in range(1, 40):
        cell = card_cell(hub, board, wc, False, today=today)
        assert cell_len(Text.from_markup(cell).plain) == wc, f"wc={wc}"
    # the multi-cell token is shed cleanly under pressure
    narrow = Text.from_markup(card_cell(hub, board, 2, False, today=today)).plain
    assert "▸" not in narrow
    wide = Text.from_markup(card_cell(hub, board, 40, False, today=today)).plain
    assert "▸5" in wide


# --------------------------------------------------------------------------- #
# AT-D3: unblock sort
# --------------------------------------------------------------------------- #
def test_unblock_sort_puts_blocked_last_and_orders_by_count(tmp_path):
    p = Project("P", "sky")
    today = date(2026, 8, 15)
    # names chosen so board/project order is A,B,C,D
    a = Task("A", project_id=p.id, phase="Doing")                # unblocks 2
    b = Task("B", project_id=p.id, phase="Doing")                # unblocks 1
    c = Task("C", project_id=p.id, phase="Doing", blocked=True)  # blocked sinks
    d = Task("D", project_id=p.id, phase="Doing")                # unblocks 0
    # make A unblock two, B unblock one
    d1 = Task("D1", project_id=p.id, phase="Backlog", depends_on=[a.id])
    d2 = Task("D2", project_id=p.id, phase="Backlog", depends_on=[a.id])
    d3 = Task("D3", project_id=p.id, phase="Backlog", depends_on=[b.id])
    board = Board([p], [a, b, c, d, d1, d2, d3], tmp_path / "board.json")
    board.save()
    groups = kanban_order(board, [a, b, c, d], False,
                          group="project", sort="unblock", today=today)
    assert len(groups) == 1
    ordered = groups[0][2]
    ids = [t.id for t in ordered]
    assert ids[-1] == c.id, "blocked task must sink"
    # non-blocked order by descending unblock count
    non_blocked = [t for t in ordered if not t.blocked]
    assert [t.id for t in non_blocked] == [a.id, b.id, d.id]


def test_unblock_cell_order_is_distinct_from_other_sorts(tmp_path):
    p = Project("P", "sky")
    today = date(2026, 8, 15)
    a = Task("A", project_id=p.id, phase="Doing")
    b = Task("B", project_id=p.id, phase="Doing", due_date=(today.isoformat()))
    c = Task("C", project_id=p.id, phase="Doing", priority="high")
    d = Task("D", project_id=p.id, phase="Backlog", depends_on=[a.id])
    board = Board([p], [a, b, c, d], tmp_path / "board.json")
    board.save()
    tasks = board.visible_tasks(False)
    orders = {
        mode: [t.id for t in _kanban_cell_order(board, tasks, mode, today)]
        for mode in ("project", "priority", "due", "recent", "unblock")
    }
    # unblock must differ from at least one other mode (palindrome-fixture law)
    assert len(set(tuple(v) for v in orders.values())) >= 2
    # under unblock, the task with a dependent (a) sorts before the one that
    # depends on it (d) because a has an unblock count > 0
    assert orders["unblock"].index(a.id) < orders["unblock"].index(d.id)


# --------------------------------------------------------------------------- #
# AT-D4: critical chain in gantt
# --------------------------------------------------------------------------- #
def test_critical_chain_finds_longest_open_chain(tmp_path):
    p = Project("P", "sky")
    a = Task("A", project_id=p.id, phase="Doing", id="a")
    b = Task("B", project_id=p.id, phase="Doing", depends_on=[a.id], id="b")
    c = Task("C", project_id=p.id, phase="Backlog", depends_on=[b.id], id="c")
    # another length-3 branch from a so the deterministic tie-break is exercised
    d = Task("D", project_id=p.id, phase="Backlog", depends_on=[a.id], id="d")
    e = Task("E", project_id=p.id, phase="Backlog", depends_on=[d.id], id="e")
    board = Board([p], [a, b, c, d, e], tmp_path / "board.json")
    board.save()
    chain = critical_chain(board)
    assert chain == [a.id, b.id, c.id]


def test_critical_chain_ignores_done_archived_and_dangling(tmp_path):
    p = Project("P", "sky")
    a = Task("A", project_id=p.id, phase="Doing")
    b = Task("B", project_id=p.id, phase="Doing", depends_on=[a.id])
    done = Task("Done", project_id=p.id, phase="Done", depends_on=[a.id])
    archived = Task("Archived", project_id=p.id, phase="Doing",
                    archived=True, depends_on=[a.id])
    dangling = Task("Dangling", project_id=p.id, phase="Backlog",
                    depends_on=["missing"])
    board = Board([p], [a, b, done, archived, dangling], tmp_path / "board.json")
    board.save()
    assert critical_chain(board) == [a.id, b.id]


def test_critical_chain_cycle_safe(tmp_path):
    p = Project("P", "sky")
    a = Task("A", project_id=p.id, phase="Doing")
    b = Task("B", project_id=p.id, phase="Doing", depends_on=[a.id])
    # hand-edited back-edge creates a cycle
    a.depends_on = [b.id]
    board = Board([p], [a, b], tmp_path / "board.json")
    board.save()
    # must terminate and must not claim a chain longer than the two nodes
    chain = critical_chain(board)
    assert len(chain) <= 2
    assert not any(chain.count(tid) > 1 for tid in chain)


def test_gantt_critical_chain_highlights_exactly_three_linked_tasks(tmp_path):
    """AT-D4, restated for the colour budget and the gutter (HLR-103, HLR-108,
    batch 2026-10-02-batch-01): the chain is STRUCTURE, not hue — its tasks'
    reaches are the heavy `━` in bold bright and their `↳` marks bold bright;
    a dependency off the chain keeps a muted `↳` and a light reach. The header
    counts it as `chain 3` (the frames' words)."""
    from taskboard.views import CRITICAL_REACH, FIELD_TASK, gantt_columns
    today = date(2026, 8, 15)
    p = Project("P", "sky",
                start_date=(today - timedelta(days=5)).isoformat(),
                due_date=(today + timedelta(days=15)).isoformat())
    a = Task("AChain", project_id=p.id, phase="Doing", id="a",
             start_date=today.isoformat(),
             due_date=(today + timedelta(days=2)).isoformat())
    b = Task("BChain", project_id=p.id, phase="Doing", depends_on=[a.id], id="b",
             start_date=(today + timedelta(days=3)).isoformat(),
             due_date=(today + timedelta(days=5)).isoformat())
    c = Task("CChain", project_id=p.id, phase="Backlog", depends_on=[b.id], id="c",
             start_date=(today + timedelta(days=6)).isoformat(),
             due_date=(today + timedelta(days=8)).isoformat())
    d = Task("DChain", project_id=p.id, phase="Backlog", depends_on=[a.id], id="d",
             start_date=(today + timedelta(days=6)).isoformat(),
             due_date=(today + timedelta(days=8)).isoformat())
    e = Task("EChain", project_id=p.id, phase="Backlog", depends_on=[d.id], id="e",
             start_date=(today + timedelta(days=9)).isoformat(),
             due_date=(today + timedelta(days=11)).isoformat())
    board = Board([p], [a, b, c, d, e], tmp_path / "board.json")
    board.save()
    text = render_gantt(board, False, None, today, width=96, height=20)
    assert "chain 3" in text.plain.split("\n")[0]
    label_w, _c, _f = gantt_columns(96)
    lines = text.plain.split("\n")
    starts = [sum(len(x) + 1 for x in lines[:i]) for i in range(len(lines))]

    def style_at(row, col):
        at = starts[row] + col
        return " ".join(str(s.style) for s in text.spans if s.start <= at < s.end)

    def row_of(title):
        return next(i for i, l in enumerate(lines) if title in l)

    bright = HEX["bright"]
    for title in ("AChain", "BChain", "CChain"):
        assert CRITICAL_REACH in lines[row_of(title)], title
    for title in ("BChain", "CChain"):
        r = row_of(title)
        assert lines[r][label_w] == "↳", lines[r]
        st = style_at(r, label_w)
        assert bright in st and "bold" in st, (title, st)
    r = row_of("DChain")
    assert lines[r][label_w] == "↳" and HEX["mut"] in style_at(r, label_w)
    assert CRITICAL_REACH not in lines[r] and FIELD_TASK in lines[r]


def test_gantt_no_dependencies_has_no_chain_header_or_accent_arrow(tmp_path):
    """No chain → no `chain` count, no heavy reach; a dependency that does not
    resolve to open work draws no mark at all (LLR-101.5, batch
    2026-10-02-batch-01), and nothing on the gantt wears the accent but today."""
    from taskboard.views import CRITICAL_REACH, RULE, gantt_columns
    today = date(2026, 8, 15)
    p = Project("P", "sky",
                start_date=(today - timedelta(days=5)).isoformat(),
                due_date=(today + timedelta(days=15)).isoformat())
    a = Task("A", project_id=p.id, phase="Doing", depends_on=["missing"],
             start_date=today.isoformat(),
             due_date=(today + timedelta(days=2)).isoformat())
    b = Task("B", project_id=p.id, phase="Backlog",
             start_date=(today + timedelta(days=3)).isoformat(),
             due_date=(today + timedelta(days=5)).isoformat())
    board = Board([p], [a, b], tmp_path / "board.json")
    board.save()
    text = render_gantt(board, False, None, today, width=96, height=20)
    assert "chain" not in text.plain.split("\n")[0]
    assert CRITICAL_REACH not in "\n".join(text.plain.split("\n")[3:])
    label_w, _c, _f = gantt_columns(96)
    row = next(l for l in text.plain.split("\n") if l.startswith("  A "))
    assert row[label_w] == " ", row
    accent = HEX["accent"]
    for s in text.spans:
        if accent in str(s.style):
            seg = text.plain[s.start:s.end]
            # the today rule, today's number, the no-selection `today …` label
            assert set(seg) <= {RULE, "1", "5"} or seg.strip() == "today Sat Aug 15", seg
