"""Tests for increment 3: block-becomes-task flow, ⛓N token, unblock sort."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from rich.cells import cell_len
from rich.text import Text

from taskboard.app import TaskboardApp
from taskboard.keymap import KEYMAP
from taskboard.modals import BlockerPicker, TextPrompt
from taskboard.models import Board, Project, Task, unblocks_count
from taskboard.views import _kanban_cell_order, card_cell, kanban_order


def _key_for(action: str) -> str:
    return next(k for k in KEYMAP if k.action == action).keys.split(",")[0]


def _board(tmp_path, *tasks, phases=None, name="board.json") -> Board:
    p = Project("Alpha", "sky")
    for t in tasks:
        t.project_id = p.id
    board = Board([p], list(tasks), tmp_path / name,
                  phases=phases or ["Backlog", "Doing", "Review", "Done"])
    board.save()
    return board


# --------------------------------------------------------------------------- #
# AT-D1: block flow wires depends_on + blocked, undo restores, blocker persists
# --------------------------------------------------------------------------- #
async def test_block_flow_links_existing_task_and_undo_restores(tmp_path):
    a = Task("A", phase="Doing")
    b = Task("B", phase="Doing")
    board = _board(tmp_path, a, b)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = a.id
        await pilot.press(_key_for("toggle_blocked"))
        await pilot.pause()
        assert isinstance(app.screen, BlockerPicker)
        ol = app.screen.query_one("#blocker-list")
        # option 0 is "(create new blocker)", option 1 is B
        ol.highlighted = 1
        await pilot.press("enter")
        await pilot.pause()

        a_loaded = app.board.task_by_id(a.id)
        assert a_loaded.blocked is True
        assert b.id in a_loaded.depends_on
        # board persisted
        reloaded = Board.load(board.path)
        assert reloaded.task_by_id(a.id).blocked is True
        assert b.id in reloaded.task_by_id(a.id).depends_on

        # undo restores blocked + depends_on
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        a_loaded = app.board.task_by_id(a.id)
        assert a_loaded.blocked is False
        assert a_loaded.depends_on == []
        # the blocker itself persists
        assert app.board.task_by_id(b.id) is not None


async def test_block_flow_creates_new_blocker_and_undo_restores(tmp_path):
    a = Task("A", phase="Doing")
    blocker = Task("B", phase="Doing")  # candidate so picker opens
    board = _board(tmp_path, a, blocker)
    app = TaskboardApp(board_path=str(board.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = a.id
        await pilot.press(_key_for("toggle_blocked"))
        await pilot.pause()
        assert isinstance(app.screen, BlockerPicker)
        ol = app.screen.query_one("#blocker-list")
        ol.highlighted = 0                       # "(create new blocker)"
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, TextPrompt)
        app.screen.query_one("#f-text").value = "New blocker"
        await pilot.press("enter")
        await pilot.pause()

        a_loaded = app.board.task_by_id(a.id)
        assert a_loaded.blocked is True
        assert len(a_loaded.depends_on) == 1
        new_id = a_loaded.depends_on[0]
        new_blocker = app.board.task_by_id(new_id)
        assert new_blocker is not None
        assert new_blocker.title == "New blocker"

        # undo restores A; created blocker persists (modal add is not undoable)
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        a_loaded = app.board.task_by_id(a.id)
        assert a_loaded.blocked is False
        assert a_loaded.depends_on == []
        assert app.board.task_by_id(new_id) is not None


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
        # no candidates except self -> direct flip, no prompt
        assert not isinstance(app.screen, BlockerPicker)
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
    plain = Text.from_markup(card_cell(hub, board, 40, False, today=today)).plain
    assert "⛓2" in plain
    plain_leaf = Text.from_markup(card_cell(d1, board, 40, False, today=today)).plain
    assert "⛓" not in plain_leaf


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
    assert "⛓" not in narrow
    wide = Text.from_markup(card_cell(hub, board, 40, False, today=today)).plain
    assert "⛓5" in wide


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
