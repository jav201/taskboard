"""Tests for batch-11 increment 1 and 2: team_sync module + app integration."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from taskboard.app import TaskboardApp
from taskboard.modals import TeamIdentityPicker
from taskboard.models import Board, Project, Task
from taskboard.team_sync import TEAM_FILENAME, TeamState, _utc_now_iso, sync_tone


def _team_config() -> dict:
    return {
        "version": 3,
        "phases": ["Backlog", "Doing", "Review", "Done"],
        "template": {"fields": ["title", "assignee", "due", "priority"]},
        "projects": [
            {"id": "plat", "name": "Platform", "color": "sky", "status": "on_track"},
            {"id": "web", "name": "Web", "color": "lime", "status": "on_track"},
        ],
        "roster": [
            {"id": "jav", "name": "Javier", "hue": "sky"},
            {"id": "ana", "name": "Ana", "hue": "amber"},
        ],
    }


def _write_team(shared_dir: Path, cfg: dict | None = None) -> None:
    shared_dir.mkdir(parents=True, exist_ok=True)
    data = cfg if cfg is not None else _team_config()
    (shared_dir / TEAM_FILENAME).write_text(
        __import__("json").dumps(data), encoding="utf-8"
    )


def _board(tmp_path, name="board.json") -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


# --------------------------------------------------------------------------- #
# AT-T1: team mode loading and the personal-task leak law
# --------------------------------------------------------------------------- #
def test_team_state_from_settings_returns_none_when_no_shared_dir():
    assert TeamState.from_settings(None, "jav") is None
    assert TeamState.from_settings("", "jav") is None


def test_load_config_reads_valid_team_json(tmp_path):
    _write_team(tmp_path)
    state = TeamState(tmp_path)
    assert state.load_config() is True
    assert state.config_version == 3
    assert state.team_project_ids() == {"plat", "web"}
    assert {r["id"] for r in state.roster()} == {"jav", "ana"}


def test_load_config_ignores_invalid_and_missing(tmp_path):
    state = TeamState(tmp_path)
    # missing file
    assert state.load_config() is False
    # malformed JSON
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / TEAM_FILENAME).write_text("not json", encoding="utf-8")
    assert state.load_config() is False
    # missing required keys
    (tmp_path / TEAM_FILENAME).write_text(
        __import__("json").dumps({"version": 1, "phases": []}), encoding="utf-8"
    )
    assert state.load_config() is False


def test_push_writes_only_team_project_tasks(tmp_path):
    _write_team(tmp_path)
    state = TeamState(tmp_path, user_id="jav")
    state.load_config()

    b = _board(tmp_path)
    team_task = Task("Team task", project_id="plat", phase="Doing")
    personal_task = Task("Personal task", project_id="personal", phase="Doing")
    b.tasks = [team_task, personal_task]

    assert state.push(b) is True
    written = __import__("json").loads(
        (tmp_path / "board.jav.json").read_text(encoding="utf-8")
    )
    assert len(written["tasks"]) == 1
    assert written["tasks"][0]["title"] == "Team task"
    assert "Personal task" not in __import__("json").dumps(written)


def test_push_includes_pushed_at_and_owner(tmp_path):
    _write_team(tmp_path)
    state = TeamState(tmp_path, user_id="jav")
    state.load_config()
    b = _board(tmp_path)
    b.tasks.append(Task("Team task", project_id="plat", phase="Doing"))

    assert state.push(b) is True
    written = __import__("json").loads(
        (tmp_path / "board.jav.json").read_text(encoding="utf-8")
    )
    assert written["user"] == "jav"
    assert written["tasks"][0]["owner"] == "jav"
    assert "pushed_at" in written
    state.last_push_at = written["pushed_at"]


def test_pull_reads_other_member_files_and_skips_malformed(tmp_path):
    _write_team(tmp_path)
    state = TeamState(tmp_path, user_id="jav")
    state.load_config()

    # ana's file with one valid task
    (tmp_path / "board.ana.json").write_text(
        __import__("json").dumps({
            "user": "ana",
            "pushed_at": "2026-09-01T00:00:00Z",
            "tasks": [{"title": "Ana task", "project_id": "web", "phase": "Doing"}],
        }), encoding="utf-8"
    )
    # malformed file for luis
    (tmp_path / "board.luis.json").write_text("bad", encoding="utf-8")
    # bad schema for maria
    (tmp_path / "board.maria.json").write_text(
        __import__("json").dumps({"user": "maria"}), encoding="utf-8"
    )

    assert state.pull() is True
    assert "ana" in state.others
    assert "luis" not in state.others
    assert "maria" not in state.others
    foreign = state.foreign_tasks()
    assert len(foreign) == 1
    assert foreign[0][0].title == "Ana task"
    assert foreign[0][1] == "ana"


def test_sync_push_then_pull(tmp_path):
    _write_team(tmp_path)
    jav = TeamState(tmp_path, user_id="jav")
    jav.load_config()
    ana = TeamState(tmp_path, user_id="ana")
    ana.load_config()

    b_jav = _board(tmp_path)
    b_jav.tasks.append(Task("Jav task", project_id="plat", phase="Doing"))
    assert jav.push(b_jav) is True

    b_ana = _board(tmp_path, name="ana.json")
    b_ana.tasks.append(Task("Ana task", project_id="web", phase="Doing"))
    assert ana.push(b_ana) is True

    # jav pulls and sees ana's task
    assert jav.pull() is True
    titles = [t.title for t, _ in jav.foreign_tasks()]
    assert "Ana task" in titles
    assert "Jav task" not in titles


def test_foreign_tasks_skip_unparseable_entries(tmp_path):
    _write_team(tmp_path)
    state = TeamState(tmp_path, user_id="jav")
    state.load_config()
    (tmp_path / "board.ana.json").write_text(
        __import__("json").dumps({
            "user": "ana",
            "pushed_at": "2026-09-01T00:00:00Z",
            "tasks": [
                {"title": "Good", "project_id": "web", "phase": "Doing"},
                {"title": 123, "project_id": "web"},  # bad type
            ],
        }), encoding="utf-8"
    )
    state.pull()
    titles = [t.title for t, _ in state.foreign_tasks()]
    assert titles == ["Good"]


# --------------------------------------------------------------------------- #
# AT-T2: team.json inheritance
# --------------------------------------------------------------------------- #
def test_apply_config_updates_phases_and_projects(tmp_path):
    _write_team(tmp_path)
    state = TeamState(tmp_path, user_id="jav")
    state.load_config()

    b = _board(tmp_path)
    b.phases = ["Old", "Phases"]
    b.projects = [Project("Local", "pink", id="local")]

    state.apply_config_to_board(b)
    assert b.phases == ["Backlog", "Doing", "Review", "Done"]
    assert {p.id for p in b.projects} == {"plat", "web", "local"}
    plat = next(p for p in b.projects if p.id == "plat")
    assert plat.name == "Platform"
    assert plat.color == "sky"


def test_apply_config_updates_existing_project_fields(tmp_path):
    cfg = _team_config()
    cfg["projects"][0]["name"] = "Platform Renamed"
    cfg["projects"][0]["color"] = "violet"
    _write_team(tmp_path, cfg)
    state = TeamState(tmp_path, user_id="jav")
    state.load_config()

    b = _board(tmp_path)
    b.projects.append(Project("Platform", "sky", "on_track", id="plat"))
    state.apply_config_to_board(b)

    plat = next(p for p in b.projects if p.id == "plat")
    assert plat.name == "Platform Renamed"
    assert plat.color == "violet"


# --------------------------------------------------------------------------- #
# AT-T3: staleness helper
# --------------------------------------------------------------------------- #
def test_sync_age_computed_from_pushed_at(tmp_path):
    _write_team(tmp_path)
    state = TeamState(tmp_path, user_id="jav")
    state.load_config()

    now = datetime.now(timezone.utc)
    ten_min_ago = (now - timedelta(minutes=10)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    (tmp_path / "board.ana.json").write_text(
        __import__("json").dumps({
            "user": "ana",
            "pushed_at": ten_min_ago,
            "tasks": [],
        }), encoding="utf-8"
    )
    state.pull()
    age = state.sync_age("ana")
    assert age is not None
    assert 9 <= age <= 11


def test_pull_tolerates_missing_shared_dir(tmp_path):
    state = TeamState(tmp_path / "absent")
    assert state.pull() is False


# --------------------------------------------------------------------------- #
# AT-T2/T3: app integration — first-run identity, daemon, staleness tone
# --------------------------------------------------------------------------- #
def _board_with_settings(tmp_path, name="board.json", **settings) -> Board:
    board = Board.load(str(tmp_path / name))
    board.settings.update(settings)
    board.save()
    return board


async def test_first_run_team_mode_prompts_identity_and_syncs(tmp_path):
    shared_dir = tmp_path / "shared"
    _write_team(shared_dir)
    (shared_dir / "board.ana.json").write_text(
        json.dumps({
            "user": "ana",
            "pushed_at": _utc_now_iso(),
            "tasks": [{"title": "Ana task", "project_id": "web", "phase": "Doing"}],
        }), encoding="utf-8"
    )
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.settings["team_shared_dir"] = str(shared_dir)
    board.save()

    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, TeamIdentityPicker)
        ol = app.screen.query_one("#identity-list")
        assert ol.option_count == 2
        ol.highlighted = 0          # select "jav"
        await pilot.press("enter")
        await pilot.pause()

    assert app.board.settings["team_user_id"] == "jav"
    assert app.team_state is not None
    assert app.team_state.user_id == "jav"
    titles = [t.title for t, _ in app.team_state.foreign_tasks()]
    assert "Ana task" in titles


async def test_daemon_sync_pulls_foreign_tasks(tmp_path):
    shared_dir = tmp_path / "shared"
    _write_team(shared_dir)
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.settings["team_shared_dir"] = str(shared_dir)
    board.settings["team_user_id"] = "jav"
    board.save()

    app = TaskboardApp(board_path=str(board_path), team_sync_interval=0.01)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        assert app.team_state is not None
        assert app.team_state.foreign_tasks() == []

        # teammate pushes after the app is already running
        (shared_dir / "board.ana.json").write_text(
            json.dumps({
                "user": "ana",
                "pushed_at": _utc_now_iso(),
                "tasks": [{"title": "Ana task", "project_id": "web", "phase": "Doing"}],
            }), encoding="utf-8"
        )
        await pilot.pause(0.05)
        titles = [t.title for t, _ in app.team_state.foreign_tasks()]
        assert "Ana task" in titles


def test_team_mode_off_when_no_shared_dir(tmp_path):
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.save()
    app = TaskboardApp(board_path=str(board_path))
    assert app.team_state is None


def test_sync_tone_flags_stale_by_config_or_default(tmp_path):
    _write_team(tmp_path)
    state = TeamState(tmp_path, user_id="jav")
    state.load_config()

    now = datetime.now(timezone.utc)
    # fresh -> mut
    fresh = (now - timedelta(minutes=10)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    (tmp_path / "board.ana.json").write_text(
        json.dumps({"user": "ana", "pushed_at": fresh, "tasks": []}), encoding="utf-8"
    )
    state.pull()
    assert sync_tone(state, "ana") == "mut"

    # stale by default 45 min tolerance
    stale = (now - timedelta(minutes=60)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    (tmp_path / "board.ana.json").write_text(
        json.dumps({"user": "ana", "pushed_at": stale, "tasks": []}), encoding="utf-8"
    )
    state.pull()
    assert sync_tone(state, "ana") == "over"

    # config tolerance overrides default (version bump so it is adopted)
    cfg = _team_config()
    cfg["version"] = 4
    cfg["sync_tolerance_minutes"] = 90
    _write_team(tmp_path, cfg)
    state.load_config()
    assert sync_tone(state, "ana") == "mut"
