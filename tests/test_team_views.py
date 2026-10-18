"""Tests for batch-11 increment 3: V3 standup view + classification filter."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.team_sync import TEAM_FILENAME, TeamState, _utc_now_iso
from taskboard.views import (HEX, _strip, fit, nav_model, render_people, render_standup,
                             render_team_filter_chrome)


def _team_config() -> dict:
    return {
        "version": 3,
        "phases": ["Backlog", "Doing", "Review", "Done"],
        "template": {"fields": ["title", "assignee", "due", "priority"]},
        "projects": [
            {"id": "plat", "name": "Platform", "color": "sky", "status": "on_track"},
        ],
        "roster": [
            {"id": "jav", "name": "username_subject", "hue": "sky"},
            {"id": "ana", "name": "Ana", "hue": "amber"},
        ],
    }


def _write_team(shared_dir: Path, cfg: dict | None = None) -> None:
    shared_dir.mkdir(parents=True, exist_ok=True)
    data = cfg if cfg is not None else _team_config()
    (shared_dir / TEAM_FILENAME).write_text(
        json.dumps(data), encoding="utf-8"
    )


def _board(tmp_path, name="board.json") -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


def _make_state(tmp_path, user_id="jav") -> TeamState:
    _write_team(tmp_path)
    state = TeamState(tmp_path, user_id=user_id)
    state.load_config()
    return state


# --------------------------------------------------------------------------- #
# Filter chrome
# --------------------------------------------------------------------------- #
def test_team_filter_chrome_highlights_active_segment():
    text = render_team_filter_chrome("equipo")     # the STORED value is unchanged
    # the painted labels are English (batch 2026-10-02-batch-02, HLR-204)
    assert "all" in text
    assert "team" in text
    assert "personal" in text
    # the chosen segment is bold bright, never the accent (batch
    # 2026-10-02-batch-02, HLR-201: the accent marks focus, not a chosen value)
    assert HEX["accent"] not in text
    assert text.count(f"b {HEX['bright']}") == 1
    assert f"[b {HEX['bright']}]team[/]" in text     # and it is the active one (F4)


# --------------------------------------------------------------------------- #
# AT-T4: V3 standup
# --------------------------------------------------------------------------- #
SELF_NAME = "username_subject"     # the scrubbed placeholder: 16 cells
NAME_CELLS = 12                    # the standup's name column (render_standup's name_w cap)


def _row_named(lines: list[str], name: str) -> str:
    """The standup row whose name cell is `name` as the standup paints it.

    TC-1901 (LLR-1901.1). The name column is 12 cells, so a longer name is
    painted cut to 11 cells and `…` — the scrub (6bff525) swapped a 6-cell
    roster name for the 16-cell placeholder, and the old substring search for
    the whole name found no row at all. The row is matched on its name cell
    (after the 2-cell spine), never on a substring, so `Ana` cannot match a
    longer name and a header cannot match a member."""
    painted = fit(name, NAME_CELLS)
    rows = [ln for ln in lines if _strip(ln).strip()[2:2 + NAME_CELLS] == painted]
    assert len(rows) == 1, (painted, rows)
    return rows[0]


def test_standup_renders_one_row_per_member_and_own_row_identifiable(tmp_path):
    """TC-1901 (LLR-1901.1): one row per member; the operator's own row is the
    one with the bright spine, a teammate's the muted one."""
    state = _make_state(tmp_path, user_id="jav")
    board = _board(tmp_path)
    text = str(render_standup(board, False, None, team_state=state, width=80, height=0))

    lines = text.splitlines()
    jav_line = _row_named(lines, SELF_NAME)
    ana_line = _row_named(lines, "Ana")
    assert "username_su…" in jav_line, "the 16-cell placeholder is cut to the 12-cell column"
    assert jav_line.strip().startswith("▌ "), "operator row should carry the accent spine"
    assert ana_line.strip().startswith("▎ "), "teammate row should carry the muted spine"


def test_standup_flags_stale_member_in_over_tone(tmp_path):
    """TC-1901 (LLR-1901.1): a teammate whose push is past the stale window
    wears `over`; the operator's fresh row does not."""
    state = _make_state(tmp_path, user_id="jav")
    board = _board(tmp_path)

    now = datetime.now(timezone.utc)
    stale = (now - timedelta(minutes=60)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    (tmp_path / "board.ana.json").write_text(
        json.dumps({"user": "ana", "pushed_at": stale, "tasks": []}),
        encoding="utf-8",
    )
    state.pull()

    markup = render_standup(board, False, None, team_state=state, width=80, height=0).markup
    lines = markup.splitlines()
    ana_line = _row_named(lines, "Ana")
    assert HEX["over"] in ana_line, "stale row should wear the over tone"
    jav_line = _row_named(lines, SELF_NAME)
    assert HEX["over"] not in jav_line, "fresh operator row should not wear over"


def test_TC_1901_the_name_column_cuts_at_twelve_cells(tmp_path):
    """TC-1901 (HLR-1901's boundary): a 12-cell name is painted whole, a
    13-cell name cut to 11 cells and `…`, each found in its own row only."""
    cfg = _team_config()
    cfg["roster"] = [{"id": "jav", "name": SELF_NAME, "hue": "sky"},
                     {"id": "twl", "name": "twelve_cells", "hue": "amber"},
                     {"id": "thr", "name": "thirteen_cell", "hue": "green"}]
    _write_team(tmp_path, cfg)
    state = TeamState(tmp_path, user_id="jav")
    state.load_config()
    lines = str(render_standup(_board(tmp_path), False, None, team_state=state,
                               width=80, height=0)).splitlines()
    assert "twelve_cells" in _row_named(lines, "twelve_cells")
    assert "thirteen_ce…" in _row_named(lines, "thirteen_cell")
    assert "username_su…" in _row_named(lines, SELF_NAME)


def test_standup_filter_changes_top_task_source(tmp_path):
    state = _make_state(tmp_path, user_id="jav")
    board = _board(tmp_path)
    today_str = datetime.now(timezone.utc).date().isoformat()

    team_task = Task("Team task", project_id="plat", phase="Doing",
                     due_date=(datetime.now(timezone.utc).date() + timedelta(days=1)).isoformat())
    personal_task = Task("Personal task", project_id="personal", phase="Doing",
                         due_date=today_str)
    board.tasks = [team_task, personal_task]

    # default: equipo -> team task (only shared projects count)
    text = str(render_standup(board, False, None, team_state=state,
                              team_filter="equipo", width=80, height=0))
    assert "Team task" in text
    assert "Personal task" not in text

    # personal -> personal task
    text = str(render_standup(board, False, None, team_state=state,
                              team_filter="personal", width=80, height=0))
    assert "Personal task" in text
    assert "Team task" not in text

    # todo -> all visible tasks; personal is due sooner so it is the top task
    text = str(render_standup(board, False, None, team_state=state,
                              team_filter="todo", width=80, height=0))
    assert "Personal task" in text
    assert "Team task" not in text


@pytest.mark.parametrize("width", range(1, 121))
def test_standup_width_sweep_is_cell_exact(width, tmp_path):
    from rich.cells import cell_len
    from taskboard.views import MIN_WIDTH

    state = _make_state(tmp_path, user_id="jav")
    board = _board(tmp_path)
    text = render_standup(board, False, None, team_state=state,
                          width=width, height=0)
    expected = max(MIN_WIDTH, width)
    for line in text.plain.split("\n"):
        assert cell_len(line) == expected, f"width {width}: {line!r}"


def test_standup_nav_model_has_no_selectable_rows(tmp_path):
    state = _make_state(tmp_path, user_id="jav")
    board = _board(tmp_path)
    assert nav_model("standup", board, False, team_state=state) == []


async def test_standup_key_8_switches_view(tmp_path):
    shared_dir = tmp_path / "shared"
    _write_team(shared_dir)
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.settings["team_shared_dir"] = str(shared_dir)
    board.settings["team_user_id"] = "jav"
    board.save()

    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("8")
        assert app.view_mode == "standup"
        text = str(app.query_one("#board").render())
        assert "STANDUP" in text


async def test_AT_1901_the_standup_marks_the_operators_own_row(tmp_path):
    """AT-1901 (US-1901, HLR-1901): `8` opens the standup; the operator's row
    (the 16-cell placeholder, painted cut to the 12-cell name column) carries
    the bright spine and the teammate's the muted one."""
    shared_dir = tmp_path / "shared"
    _write_team(shared_dir)
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.settings["team_shared_dir"] = str(shared_dir)
    board.settings["team_user_id"] = "jav"
    board.save()

    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("8")
        rows = [r.strip() for r in str(app.query_one("#board").render()).splitlines()]
        own = [r for r in rows if "username_su…" in r]
        mate = [r for r in rows if r[2:15] == "Ana          "]
        assert len(own) == 1 and own[0].startswith("▌ username_su… "), rows
        assert len(mate) == 1 and mate[0].startswith("▎ Ana "), rows


async def test_action_team_filter_cycle(tmp_path):
    shared_dir = tmp_path / "shared"
    _write_team(shared_dir)
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.settings["team_shared_dir"] = str(shared_dir)
    board.settings["team_user_id"] = "jav"
    board.save()

    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("8")
        assert app.team_filter == "equipo"
        app.action_team_filter_cycle()
        assert app.team_filter == "personal"
        app.action_team_filter_cycle()
        assert app.team_filter == "todo"
        app.action_team_filter_cycle()
        assert app.team_filter == "equipo"


# --------------------------------------------------------------------------- #
# AT-T5: V2 people lanes
# --------------------------------------------------------------------------- #
def test_people_lanes_render_by_person_with_readonly_marks(tmp_path):
    state = _make_state(tmp_path, user_id="jav")
    board = _board(tmp_path)

    team_task = Task("Jav team task", project_id="plat", phase="Doing")
    personal_task = Task("Jav personal task", project_id="personal", phase="Doing")
    board.tasks = [team_task, personal_task]

    (tmp_path / "board.ana.json").write_text(
        json.dumps({
            "user": "ana",
            "pushed_at": _utc_now_iso(),
            "tasks": [{"title": "Ana team task", "project_id": "plat", "phase": "Doing"}],
        }),
        encoding="utf-8",
    )
    state.pull()

    text = str(render_people(board, False, None, team_state=state,
                             team_filter="equipo", width=80, height=0))
    assert "username_subject" in text
    assert "Ana" in text
    assert "Jav team task" in text
    assert "Ana team task" in text

    lines = text.splitlines()
    ana_task_line = next(line for line in lines if "Ana team task" in line)
    jav_task_line = next(line for line in lines if "Jav team task" in line)
    assert "◦" in ana_task_line, "foreign card should carry the read-only mark"
    assert "◦" not in jav_task_line, "operator card should not carry the read-only mark"


def test_people_filter_changes_visible_tasks(tmp_path):
    state = _make_state(tmp_path, user_id="jav")
    board = _board(tmp_path)

    team_task = Task("Team task", project_id="plat", phase="Doing")
    personal_task = Task("Personal task", project_id="personal", phase="Doing")
    board.tasks = [team_task, personal_task]

    text = str(render_people(board, False, None, team_state=state,
                             team_filter="equipo", width=80, height=0))
    assert "Team task" in text
    assert "Personal task" not in text

    text = str(render_people(board, False, None, team_state=state,
                             team_filter="personal", width=80, height=0))
    assert "Personal task" in text
    assert "Team task" not in text


def test_people_nav_model_has_selectable_rows(tmp_path):
    state = _make_state(tmp_path, user_id="jav")
    board = _board(tmp_path)
    task = Task("Team task", project_id="plat", phase="Doing")
    board.tasks = [task]

    rows = nav_model("people", board, False, team_state=state, team_filter="equipo")
    assert rows == [[task.id]], "people nav should return one selectable column"


async def test_key_9_switches_to_people_view(tmp_path):
    shared_dir = tmp_path / "shared"
    _write_team(shared_dir)
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.settings["team_shared_dir"] = str(shared_dir)
    board.settings["team_user_id"] = "jav"
    board.save()

    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("9")
        assert app.view_mode == "people"
        text = str(app.query_one("#board").render())
        assert "PEOPLE" in text


@pytest.mark.parametrize("width", range(1, 121))
def test_people_width_sweep_is_cell_exact(width, tmp_path):
    from rich.cells import cell_len
    from taskboard.views import MIN_WIDTH

    state = _make_state(tmp_path, user_id="jav")
    board = _board(tmp_path)
    board.tasks = [Task("Team task", project_id="plat", phase="Doing")]
    text = render_people(board, False, None, team_state=state,
                         width=width, height=0)
    expected = max(MIN_WIDTH, width)
    for line in text.plain.split("\n"):
        assert cell_len(line) == expected, f"width {width}: {line!r}"


# --------------------------------------------------------------------------- #
# people WITHOUT a team: key 9 is ungated, so this is a reachable state
# --------------------------------------------------------------------------- #
def test_people_nav_model_survives_team_mode_off(tmp_path):
    """Key `9` enters people unconditionally (`app.VIEW_KEYS`, no team gate) and
    `render_people` answers team-mode-off with a body that says so. The nav model
    is the third seat on that same entry point and must agree: no roster means
    nothing selectable, NOT an AttributeError on the operator's first cursor key.

    This is the crash of 2026-09-05: `team_state=None` reached
    `for member in team_state.roster()`.
    """
    board = _board(tmp_path)
    board.tasks = [Task("Solo task", project_id="personal", phase="Doing")]

    rows = nav_model("people", board, False, team_state=None, team_filter="equipo")
    assert rows == [], "no team means no selectable rows, not a crash"


async def test_cursor_in_people_without_a_team_does_not_crash(tmp_path):
    """The operator's reproduction: a board with tasks, NO team configured,
    switch to people, press a cursor key. The app must survive and still draw
    the honest team-mode-off body."""
    board_path = tmp_path / "board.json"
    board = Board.load(str(board_path))
    board.save()
    assert not board.settings.get("team_shared_dir"), "fixture must have no team"

    app = TaskboardApp(board_path=str(board_path))
    async with app.run_test(size=(202, 39)) as pilot:
        await pilot.press("9")
        assert app.view_mode == "people"
        assert app.team_state is None, "no shared dir means team mode is off"
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("up")
        text = str(app.query_one("#board").render())
        assert "PEOPLE" in text
        assert "team mode off" in text, "the view must say why it is empty"
