"""Tests for batch-12: in-app Setup + per-view help family."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from taskboard.app import TaskboardApp
from taskboard.models import Board
from taskboard.team_sync import TEAM_FILENAME, probe_setup_health


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


# --------------------------------------------------------------------------- #
# US-S2: Setup view scaffold
# --------------------------------------------------------------------------- #
async def test_setup_key_0_switches_view(tmp_path):
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        assert app.view_mode == "swimlanes"
        await pilot.press("0")
        await pilot.pause()
        assert app.view_mode == "setup"
        text = str(app.query_one("#board").render())
        assert "SETUP" in text


async def test_setup_renders_grid_with_sections(tmp_path):
    shared_dir = tmp_path / "shared"
    _write_team(shared_dir)
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.settings["team_shared_dir"] = str(shared_dir)
    board.settings["team_user_id"] = "jav"
    board.save()

    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("0")
        await pilot.pause()
        text = str(app.query_one("#board").render())
        assert "equipo" in text
        assert "proyectos del equipo" in text
        assert "roster" in text
        assert "Javier" in text



async def test_setup_esc_returns_to_previous_view(tmp_path):
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("4")   # kanban
        await pilot.pause()
        assert app.view_mode == "kanban"
        await pilot.press("0")   # setup
        await pilot.pause()
        assert app.view_mode == "setup"
        await pilot.press("escape")
        await pilot.pause()
        assert app.view_mode == "kanban"


async def test_setup_save_writes_team_json_and_settings(tmp_path):
    shared_dir = tmp_path / "shared"
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.save()

    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("0")
        await pilot.pause()
        # enable team mode and set shared dir
        app._setup_state["enabled"] = True
        app._setup_state["shared_dir"] = str(shared_dir)
        app._setup_state["interval_minutes"] = 15
        app._setup_state["user_id"] = "jav"
        app._setup_state["roster"] = [
            {"id": "jav", "name": "Javier", "hue": "sky"},
        ]
        await pilot.press("ctrl+s")
        await pilot.pause()

        assert app.view_mode == "swimlanes"
        assert app.board.settings.get("team_shared_dir") == str(shared_dir)
        assert app.board.settings.get("team_user_id") == "jav"
        assert app.board.settings.get("team_sync_interval") == 15
        assert (shared_dir / "team.json").exists()
        data = json.loads((shared_dir / "team.json").read_text(encoding="utf-8"))
        assert data["version"] == 1
        assert data["sync_tolerance_minutes"] == 15
        assert [r["id"] for r in data["roster"]] == ["jav"]


async def test_setup_esc_leaves_files_unchanged(tmp_path):
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.save()

    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        # capture bytes after the app has done its initial saves
        before = board_path.read_bytes()
        await pilot.press("0")
        await pilot.pause()
        app._setup_state["shared_dir"] = "/some/path"
        app._setup_state["roster"] = [{"id": "x", "name": "X", "hue": "mut"}]
        await pilot.press("escape")
        await pilot.pause()

        assert board_path.read_bytes() == before


def test_setup_stepper_clamps_interval():
    from pathlib import Path
    app = TaskboardApp(board_path=str(Path("/tmp/nonexistent_board_for_test.json")))
    assert app._clamp_interval("3") == 5
    assert app._clamp_interval("200") == 120
    assert app._clamp_interval("45") == 45
    assert app._clamp_interval("abc") is None


# --------------------------------------------------------------------------- #
# US-S2 parte 2: health checks
# --------------------------------------------------------------------------- #
def test_probe_setup_health_flags_unwritable_shared_path(tmp_path):
    # point shared dir at an existing file: it exists but is not a writable dir
    shared_path = tmp_path / "not_a_dir.txt"
    shared_path.write_text("i am a file", encoding="utf-8")
    staged = {
        "enabled": True,
        "shared_dir": str(shared_path),
        "interval_minutes": 30,
        "user_id": "jav",
        "projects": [],
        "roster": [{"id": "jav", "name": "Javier", "hue": "sky"}],
    }
    checks = probe_setup_health(staged, None)
    ok, note = checks["carpeta"]
    assert not ok
    assert "directorio" in note.lower() or "directory" in note.lower()


# --------------------------------------------------------------------------- #
# US-S3: per-view help family
# --------------------------------------------------------------------------- #
def _label_texts(screen) -> list[str]:
    from textual.widgets import Label
    return [str(label.render()) for label in screen.query(Label)]


async def test_question_mark_opens_per_view_help_modal(tmp_path):
    from taskboard.app import TaskboardApp
    from taskboard.modals import HelpModal
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("4")           # kanban
        await pilot.pause()
        await pilot.press("question_mark")
        await pilot.pause()
        assert isinstance(app.screen, HelpModal)
        assert app.screen._mode == "kanban"
        texts = _label_texts(app.screen)
        assert any("Help · kanban" in t for t in texts)


async def test_help_modal_shows_usage_legend_example_and_keys(tmp_path):
    from taskboard.app import TaskboardApp
    from taskboard.modals import HelpModal
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("question_mark")
        await pilot.pause()
        assert isinstance(app.screen, HelpModal)
        texts = _label_texts(app.screen)
        assert any("Uso" in t for t in texts)
        assert any("Leyenda" in t for t in texts)
        assert any("Ejemplo" in t for t in texts)
        assert any("Teclas" in t for t in texts)
        # the usage copy comes from the per-view register
        assert any("para qué es" in t for t in texts)


async def test_help_modal_m_opens_full_keymap(tmp_path):
    from taskboard.app import TaskboardApp, HelpScreen
    from taskboard.modals import HelpModal
    from textual.widgets import Static
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("question_mark")
        await pilot.pause()
        assert isinstance(app.screen, HelpModal)
        await pilot.press("m")
        await pilot.pause()
        assert isinstance(app.screen, HelpScreen)
        static = app.screen.query_one("#help-box Static", Static)
        text = str(static.render())
        assert "ON THIS SCREEN" in text
        # the full map contains both primary and alias keys
        assert "Map" in text
        assert "Quit" in text
        assert "Down" in text


async def test_help_modal_question_mark_opens_command_palette(tmp_path):
    from taskboard.app import TaskboardApp
    from taskboard.modals import CommandPalette, HelpModal
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("question_mark")
        await pilot.pause()
        assert isinstance(app.screen, HelpModal)
        await pilot.press("question_mark")
        await pilot.pause()
        assert isinstance(app.screen, CommandPalette)
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, HelpModal)


# --------------------------------------------------------------------------- #
# US-S2 parte 3: setup commands are executable
# --------------------------------------------------------------------------- #
async def test_setup_enter_edits_shared_directory(tmp_path):
    """Pressing Enter on the shared-directory row opens a TextPrompt and the
    edited value is written back into staged state."""
    from textual.widgets import Input
    from taskboard.app import TaskboardApp
    from taskboard.modals import TextPrompt
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("0")
        await pilot.pause()
        app._setup_state["cursor_row"] = 1   # carpeta compartida
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, TextPrompt)
        inp = app.screen.query_one("#f-text", Input)
        inp.value = "D:/equipo/shared"
        await pilot.press("enter")
        await pilot.pause()
        assert app._setup_state["shared_dir"] == "D:/equipo/shared"


async def test_setup_enter_edits_sync_interval(tmp_path):
    """Pressing Enter on the sync-interval row edits the staged interval."""
    from textual.widgets import Input
    from taskboard.app import TaskboardApp
    from taskboard.modals import TextPrompt
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("0")
        await pilot.pause()
        app._setup_state["cursor_row"] = 3   # sync cada
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, TextPrompt)
        inp = app.screen.query_one("#f-text", Input)
        inp.value = "45"
        await pilot.press("enter")
        await pilot.pause()
        assert app._setup_state["interval_minutes"] == 45


async def test_setup_space_toggles_team_mode_enabled(tmp_path):
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("0")
        await pilot.pause()
        app._setup_state["cursor_row"] = 0   # modo equipo
        before = app._setup_state.get("enabled", False)
        await pilot.press("space")
        await pilot.pause()
        assert app._setup_state["enabled"] is not before


async def test_setup_a_adds_project_row(tmp_path):
    from textual.widgets import Input
    from taskboard.app import TaskboardApp
    from taskboard.modals import TextPrompt
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("0")
        await pilot.pause()
        # move to proyectos section
        app._setup_state["cursor_section"] = 1
        app._setup_state["cursor_row"] = 0
        await pilot.press("a")
        await pilot.pause()
        assert isinstance(app.screen, TextPrompt)
        inp = app.screen.query_one("#f-text", Input)
        inp.value = "mobile"
        await pilot.press("enter")
        await pilot.pause()
        assert any(p.get("id") == "mobile" for p in app._setup_state["projects"])


async def test_setup_x_removes_roster_row(tmp_path):
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        await pilot.press("0")
        await pilot.pause()
        app._setup_state["cursor_section"] = 2
        app._setup_state["roster"] = [
            {"id": "jav", "name": "Javier", "hue": "sky"},
            {"id": "ana", "name": "Ana", "hue": "amber"},
        ]
        app._setup_state["cursor_row"] = 1   # ana
        await pilot.press("x")
        await pilot.pause()
        assert [r["id"] for r in app._setup_state["roster"]] == ["jav"]
        assert app._setup_state["cursor_row"] == 0
