"""The view-survival law.

The 2026-09-05 hotfix (`people` nav crashed with team mode off — PLAN.md,
batch-11) fixed one cell of a much bigger table: a renderer/nav seat that
assumes a data source the current regime does not provide. That defect class
is not specific to "no team" or to `people` — it can hide behind ANY view,
under ANY degraded regime.

This is the parametrized law over that table: for every view in
`VIEW_ORDER`, in three degraded regimes, boot the real app, enter the view by
its key, and drive every cursor/select key. No exception, and the board
still renders width-exact lines when we come back to rest on it.

Regimes:
  - no_team_small_board: a real-shaped seeded board (the hotfix's own
    fixture shape), no team configured.
  - empty_board: zero tasks, zero projects.
  - archived_only: tasks exist but all are archived, `show_archived` is off
    (the app default), so every view's visible-task set is empty even
    though the board is not literally empty.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from rich.cells import cell_len

from taskboard.app import VIEW_KEYS, VIEW_ORDER, TaskboardApp
from taskboard.models import Board, Project, Task

CURSOR_KEYS = ["down", "up", "right", "left", "enter"]

# Every view except `setup` draws a rectangle: every line is exactly the
# requested width (the "rectangle law", `test_prism_laws.py` MANIFEST, homed
# in `test_swimlanes.py` and reused by the width-sweep tests in
# `test_flow_view.py` / `test_team_views.py`). `setup` is a free-form editor
# screen — header, blank separator lines, and `fit()`-padded columns narrower
# than the frame — and carries no such contract anywhere in the repo; for it
# we only guard against overflow (a line wider than the frame, which would
# visually corrupt the screen), not exact width.
WIDTH_EXACT_VIEWS = frozenset(VIEW_ORDER) - {"setup"}


def _key_for(view: str) -> str:
    return next(k for k, v in VIEW_KEYS.items() if v == view)


def _no_team_small_board(tmp_path: Path) -> Path:
    """The hotfix's own fixture: a real-shaped seeded board, no team."""
    path = tmp_path / "board.json"
    Board.load(str(path))          # no file yet -> seeds demo data and saves
    return path


def _empty_board(tmp_path: Path) -> Path:
    path = tmp_path / "board.json"
    board = Board.load(str(path))  # seeds, then we strip it bare
    board.projects.clear()
    board.tasks.clear()
    board.save()
    return path


def _archived_only_board(tmp_path: Path) -> Path:
    path = tmp_path / "board.json"
    board = Board.load(str(path))
    board.projects.clear()
    board.tasks.clear()
    proj = Project("Solo Project", "sky", "on_track")
    board.projects.append(proj)
    board.tasks.append(
        Task("Old done thing", proj.id, "Done", "normal", archived=True))
    board.tasks.append(
        Task("Old backlog thing", proj.id, "Backlog", "normal", archived=True))
    board.save()
    return path


REGIMES = {
    "no_team_small_board": _no_team_small_board,
    "empty_board": _empty_board,
    "archived_only": _archived_only_board,
}


async def _drive(tmp_path: Path, view: str, build_board) -> None:
    board_path = build_board(tmp_path)
    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press(_key_for(view))
        await pilot.pause()
        assert app.view_mode == view, f"{view}: key did not switch view"

        for key in CURSOR_KEYS:
            await pilot.press(key)
            await pilot.pause()
            # `enter`/details may open a read-only modal; dismiss it (every
            # modal in this app binds `escape`) so the next key still drives
            # the board, and so we can inspect the board's own render below.
            if len(app.screen_stack) > 1:
                await pilot.press("escape")
                await pilot.pause()

        assert len(app.screen_stack) == 1, f"{view}: a modal was left open"

        board_widget = app.query_one("#board")
        width = board_widget.size.width
        text = str(board_widget.render())
        expected = max(24, width)   # MIN_WIDTH floor, mirrors views._clamp_width
        for line in text.split("\n"):
            if view in WIDTH_EXACT_VIEWS:
                assert cell_len(line) == expected, f"{view}: uneven line {line!r}"
            else:
                assert cell_len(line) <= expected, f"{view}: overflowing line {line!r}"


@pytest.mark.parametrize("regime", sorted(REGIMES))
@pytest.mark.parametrize("view", VIEW_ORDER)
async def test_view_survives_cursor_keys_in_degraded_regime(view, regime, tmp_path):
    await _drive(tmp_path, view, REGIMES[regime])
