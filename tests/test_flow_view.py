"""Tests for the flow view (key 7): cycle time, heatmap, throughput."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from taskboard import history
from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.views import nav_model, render_flow


def _write_history(board_path: Path, records: list[dict]) -> None:
    path = history.history_path(board_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
        encoding="utf-8",
    )


def _fixture_board(tmp_path):
    """A board with three tasks and a hand-crafted history."""
    board_path = tmp_path / "board.json"
    p = Project("P", "sky")
    a = Task("Alpha", project_id=p.id, phase="Done")
    b = Task("Beta", project_id=p.id, phase="Done")
    c = Task("Gamma", project_id=p.id, phase="Doing")
    board = Board([p], [a, b, c], board_path)
    board.save()
    _write_history(board_path, [
        {"task": a.id, "from": None, "to": "Backlog", "at": "2026-08-01T10:00:00"},
        {"task": a.id, "from": "Backlog", "to": "Doing", "at": "2026-08-03T10:00:00"},
        {"task": a.id, "from": "Doing", "to": "Done", "at": "2026-08-06T10:00:00"},
        {"task": b.id, "from": None, "to": "Backlog", "at": "2026-08-02T10:00:00"},
        {"task": b.id, "from": "Backlog", "to": "Doing", "at": "2026-08-04T10:00:00"},
        {"task": b.id, "from": "Doing", "to": "Done", "at": "2026-08-07T10:00:00"},
        {"task": c.id, "from": None, "to": "Backlog", "at": "2026-08-10T10:00:00"},
        {"task": c.id, "from": "Backlog", "to": "Doing", "at": "2026-08-12T10:00:00"},
    ])
    return board, (a, b, c)


# AT-B1: fixture history with known intervals -> the three artifacts carry
# the computed values.
def test_flow_renders_cycle_heatmap_and_throughput(tmp_path):
    board, (a, b, c) = _fixture_board(tmp_path)
    today = date(2026, 8, 15)
    text = str(render_flow(board, False, None, today=today, width=80, height=0))

    # cycle time: median whole days per closed interval
    assert "Backlog" in text
    assert "Doing" in text
    assert "2d" in text          # Backlog median
    assert "3d" in text          # Doing median (two closed 3-day intervals)

    # heatmap glyphs present
    assert any(ch in text for ch in "░▒▓█")

    # throughput: two tasks reached Done in week 32
    assert "THROUGHPUT" in text
    assert "total 2" in text


# AT-B2: empty history -> the sentence, no metric glyphs.
def test_flow_empty_history_shows_sentence_and_no_ramp(tmp_path):
    board_path = tmp_path / "board.json"
    board = Board([], [Task("T")], board_path)
    board.save()

    text = str(render_flow(board, False, None, today=date(2026, 8, 15),
                           width=80, height=0))
    assert "sin historia aún — se construye desde hoy" in text
    assert not any(ch in text for ch in "░▒▓█")
    assert "CYCLE" not in text
    assert "HEATMAP" not in text
    assert "THROUGHPUT" not in text


# AT-B3: single transition -> renders without error and "en curso n=1".
def test_flow_single_transition_renders_and_shows_open(tmp_path):
    board_path = tmp_path / "board.json"
    t = Task("Only", phase="Doing")
    board = Board([], [t], board_path)
    board.save()
    _write_history(board_path, [
        {"task": t.id, "from": None, "to": "Backlog", "at": "2026-08-10T10:00:00"},
        {"task": t.id, "from": "Backlog", "to": "Doing", "at": "2026-08-11T10:00:00"},
    ])

    text = str(render_flow(board, False, None, today=date(2026, 8, 15),
                           width=80, height=0))
    assert "FLOW" in text
    assert "en curso n=1" in text


# AT-B4: width sweep cell-exact (1..120) + keymap contains key 7 -> view('flow').
@pytest.mark.parametrize("width", range(1, 121))
def test_flow_width_sweep_is_cell_exact(width, tmp_path):
    from taskboard.views import MIN_WIDTH
    board, _ = _fixture_board(tmp_path)
    text = render_flow(board, False, None, today=date(2026, 8, 15),
                       width=width, height=0)
    from rich.cells import cell_len
    expected = max(MIN_WIDTH, width)
    for line in text.plain.split("\n"):
        assert cell_len(line) == expected, f"width {width}: {line!r}"


async def test_key_7_switches_to_flow_view(tmp_path):
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("7")
        assert app.view_mode == "flow"
        text = str(app.query_one("#board").render())
        assert "FLOW" in text


def test_flow_nav_model_has_no_selectable_rows(tmp_path):
    board, _ = _fixture_board(tmp_path)
    assert nav_model("flow", board, False, today=date(2026, 8, 15)) == []
