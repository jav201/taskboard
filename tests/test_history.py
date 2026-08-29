"""Tests for the append-only phase-transition log."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from taskboard import history
from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task


def _history_lines(board_path: Path) -> list[str]:
    path = history.history_path(board_path)
    if not path.exists():
        return []
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# --------------------------------------------------------------------------- #
# AT-A1: phase-move key press appends EXACTLY ONE line with the four fields;
# `at` parses.
async def test_phase_move_appends_one_transition(tmp_path):
    board_path = tmp_path / "board.json"
    project = Project("P", "sky")
    task = Task("T", project_id=project.id, phase="Doing")
    board = Board([project], [task], board_path)
    board.save()

    app = TaskboardApp(board_path=str(board_path))
    # The app reloads the board from disk, so the live task is app.board's copy.
    live_task = app.board.task_by_id(task.id)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")   # kanban view
        await pilot.pause()
        app.selected_task_id = live_task.id
        app.refresh_view()
        await pilot.press("right_square_bracket")   # move selected task forward one phase

    assert live_task.phase == "Done"
    lines = _history_lines(board_path)
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["task"] == live_task.id
    assert record["from"] == "Doing"
    assert record["to"] == "Done"
    assert "at" in record
    datetime.fromisoformat(record["at"])


# AT-A2: add_task appends a creation record (`from`: null).
def test_add_task_appends_creation_record(tmp_path):
    board_path = tmp_path / "board.json"
    board = Board([], [], board_path)
    task = Task("New", phase="Backlog")
    board.add_task(task)

    lines = _history_lines(board_path)
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["task"] == task.id
    assert record["from"] is None
    assert record["to"] == "Backlog"
    assert "at" in record


# AT-A3: a directory at the history path (portable unwritable on Windows)
# -> move still returns True, board saves, no exception, HISTORY_ERROR set;
# notify fires (mocked).
async def test_history_error_is_surfaced_without_aborting_move(tmp_path):
    board_path = tmp_path / "board.json"
    project = Project("P", "sky")
    task = Task("T", project_id=project.id, phase="Doing")
    board = Board([project], [task], board_path)
    board.save()

    # Make the history path a directory so the append cannot create a file.
    history.history_path(board_path).mkdir(parents=True, exist_ok=True)

    app = TaskboardApp(board_path=str(board_path))
    live_task = app.board.task_by_id(task.id)
    notified = []
    app.notify = lambda message, **kwargs: notified.append((message, kwargs))

    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = live_task.id
        app.refresh_view()
        await pilot.press("right_square_bracket")

    assert live_task.phase == "Done"
    assert history.HISTORY_ERROR is not None
    assert board_path.exists()
    history_notifications = [
        (m, kw) for m, kw in notified
        if history.HISTORY_ERROR in m and kw.get("severity") == "warning"
    ]
    assert len(history_notifications) == 1


# AT-A4: file with 2 good + 1 invalid-JSON + 1 wrong-shape line -> 2 records,
# skipped == 2.
def test_read_skips_malformed_lines_and_counts_them(tmp_path):
    board_path = tmp_path / "board.json"
    path = history.history_path(board_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"task": "t1", "from": "Backlog", "to": "Doing", "at": "2026-08-01T10:00:00"}) + "\n"
        "this is not json\n"
        + json.dumps({"task": "t2", "from": None, "to": "Done", "at": "2026-08-02T11:00:00"}) + "\n"
        + json.dumps({"task": 1}) + "\n",
        encoding="utf-8",
    )

    records, skipped = history.read(board_path)
    assert skipped == 2
    assert len(records) == 2
    assert [r["task"] for r in records] == ["t1", "t2"]


def test_read_missing_file_returns_empty_history():
    records, skipped = history.read(Path("/nonexistent/board.json"))
    assert records == []
    assert skipped == 0


def test_append_sets_and_clears_history_error(tmp_path):
    board_path = tmp_path / "board.json"
    path = history.history_path(board_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir(exist_ok=True)  # directory blocks file append

    history.HISTORY_ERROR = None
    result = history.append(board_path, {"task": "t1", "from": "A", "to": "B"})
    assert result is None
    assert history.HISTORY_ERROR is not None

    path.rmdir()
    result = history.append(board_path, {"task": "t1", "from": "A", "to": "B"})
    assert result is not None
    assert history.HISTORY_ERROR is None
