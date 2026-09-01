"""Tests for batch-12: in-app Setup + per-view help family."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from taskboard.app import TaskboardApp
from taskboard.models import Board
from taskboard.team_sync import TEAM_FILENAME


def _team_config() -> dict:
    return {
        "version": 1,
        "phases": ["Backlog", "Doing", "Review", "Done"],
        "template": {"fields": ["title", "assignee", "due", "priority"]},
        "projects": [
            {"id": "plat", "name": "Platform", "color": "sky", "status": "on_track"},
        ],
        "roster": [
            {"id": "jav", "name": "Javier", "hue": "sky"},
            {"id": "ana", "name": "Ana", "hue": "amber"},
        ],
    }


def _write_team(shared_dir: Path, cfg: dict | None = None) -> None:
    shared_dir.mkdir(parents=True, exist_ok=True)
    data = cfg if cfg is not None else _team_config()
    (shared_dir / TEAM_FILENAME).write_text(json.dumps(data), encoding="utf-8")


# --------------------------------------------------------------------------- #
# US-S1: initial sync on mount
# --------------------------------------------------------------------------- #
async def test_configured_identity_syncs_on_mount(tmp_path):
    """A user whose identity is already configured must see peers immediately,
    without waiting for the daemon's first tick."""
    shared_dir = tmp_path / "shared"
    _write_team(shared_dir)

    # ana has pushed a team task
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    (shared_dir / "board.ana.json").write_text(
        json.dumps({
            "user": "ana",
            "pushed_at": now,
            "tasks": [
                {
                    "id": "t1",
                    "title": "Ana team task",
                    "project_id": "plat",
                    "phase": "Doing",
                    "priority": "normal",
                    "blocked": False,
                    "archived": False,
                    "urls": [],
                    "images": [],
                    "depends_on": [],
                    "notes": "",
                }
            ],
        }),
        encoding="utf-8",
    )

    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.settings["team_shared_dir"] = str(shared_dir)
    board.settings["team_user_id"] = "jav"
    board.save()

    app = TaskboardApp(board_path=str(board_path), team_sync_interval=1800.0)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        # standup view should already show ana's task without a daemon tick
        await pilot.press("8")
        await pilot.pause()
        text = str(app.query_one("#board").render())
        assert "Ana" in text
        assert "Ana team task" in text
