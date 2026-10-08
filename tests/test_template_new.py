"""`I` → `New template...` authors a template from scratch (batch
2026-10-07-batch-09, increment 001).

HLR-1501 / LLR-1501.1 · AT-1501.

The `I` picker lists `New template...` first; choosing it opens the editor — one
name field and one multi-line tasks field (one task per line). Save emits the
LINEAR chain (task i waits on i-1, task 0 waits on nothing; blank lines skipped,
lines trimmed), appends `{"name", "tasks"}` to `settings["templates"]`, saves and
toasts the pinned literal `Template '<name>' saved — <N> tasks`; an all-empty
edit saves nothing and toasts one line saying why; esc writes nothing; a
single-task line works. The saved template then inserts with `I` like any other,
reproducing the chain.
"""
from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, TextArea

from taskboard.app import RENUMBER_NOTICE_KEY, TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.modals import TemplateEditor


def _board(tmp_path, settings=None) -> Board:
    p = Project("Plat", "sky")
    t = Task("Existing task", p.id, "Doing")
    b = Board([p], [t], tmp_path / "board.json",
              {RENUMBER_NOTICE_KEY: True, "migrations": {"links": 1},
               **(settings or {})})
    b.save()
    return b


def _toasts(app) -> list[str]:
    return [str(t.render()) for t in app.screen.query("Toast")]


def _toast_check(app, title: str, message: str) -> str | None:
    """None when a `title` toast's body equals `message` exactly."""
    for t in _toasts(app):
        head, _, body = t.partition("\n")
        if head == title and body == message:
            return None
    return f"no {title!r} toast equal to {message!r}; toasts {_toasts(app)!r}"


def _plains(ol) -> list[str]:
    return [ol.get_option_at_index(i).prompt.plain for i in range(ol.option_count)]


async def _settle(pilot, n=3):
    for _ in range(n):
        await pilot.pause()


async def _open_editor(pilot, app) -> None:
    await pilot.press("I")
    await _settle(pilot)
    await pilot.press("enter")          # the highlighted row is New template...
    await _settle(pilot)
    assert isinstance(app.screen, TemplateEditor)


def _save(app, name: str, tasks: str) -> None:
    app.screen.query_one("#f-name", Input).value = name
    app.screen.query_one("#f-tasks", TextArea).text = tasks
    app.screen.query_one("#save", Button).press()


async def test_picker_lists_new_template_first(tmp_path):
    """The `I` picker lists `New template...` first, ahead of user templates and
    the presets."""
    path = tmp_path / "board.json"
    _board(tmp_path, settings={"templates": [
        {"name": "Deploy", "tasks": [{"title": "Build"}, {"title": "Smoke", "wait": 0}]},
    ]})
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30)) as pilot:
        await pilot.pause()
        await pilot.press("I")
        await _settle(pilot)
        assert _plains(app.screen.query_one("#template-list")) == [
            "New template...", "Deploy — 2 tasks",
            "Simple chain — 3 tasks", "Bugfix — 3 tasks"]


async def test_editor_saves_a_linear_chain_and_round_trips(tmp_path):
    """Save a multi-line edit (blank lines skipped, lines trimmed) toasts the
    pinned literal and stores the linear chain; `I` then inserts it, each task
    waiting on the previous."""
    path = tmp_path / "board.json"
    _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        app.selected_task_id = app.board.tasks[0].id
        await _open_editor(pilot, app)
        _save(app, "  Launch  ", "  Design  \n\nBuild\n  Ship  \n")
        await _settle(pilot)
        assert app.board.settings["templates"] == [{"name": "Launch", "tasks": [
            {"title": "Design"},
            {"title": "Build", "wait": 0},
            {"title": "Ship", "wait": 1},
        ]}]
        assert _toast_check(app, "Templates",
                            "Template 'Launch' saved — 3 tasks") is None
        # the insert round-trip: the saved template lists after New template...,
        # and `I` reproduces the linear chain
        n0 = len(app.board.tasks)
        await pilot.press("I")
        await _settle(pilot)
        assert _plains(app.screen.query_one("#template-list"))[1] == "Launch — 3 tasks"
        await pilot.press("down", "enter")     # New template... → Launch
        await _settle(pilot)
        created = app.board.tasks[n0:]
        assert [c.title for c in created] == ["Design", "Build", "Ship"]
        assert created[0].depends_on == []
        assert created[1].depends_on == [created[0].id]
        assert created[2].depends_on == [created[1].id]


async def test_all_empty_saves_nothing(tmp_path):
    """A blank name and zero task lines save NOTHING: one toast says why, and
    `settings.templates` and the board file stay byte-identical."""
    path = tmp_path / "board.json"
    _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        raw_before = path.read_bytes()
        await _open_editor(pilot, app)
        _save(app, "   ", "\n\n  \n")
        await _settle(pilot)
        assert "templates" not in app.board.settings
        assert path.read_bytes() == raw_before
        assert _toast_check(app, "Templates",
                            "Template not saved — give it a name and at least "
                            "one task.") is None


async def test_name_without_tasks_saves_nothing(tmp_path):
    """A name with zero task lines also saves nothing."""
    path = tmp_path / "board.json"
    _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        await _open_editor(pilot, app)
        _save(app, "Empty", "")
        await _settle(pilot)
        assert "templates" not in app.board.settings


async def test_escape_writes_nothing(tmp_path):
    """Esc cancels: nothing written, the board file untouched."""
    path = tmp_path / "board.json"
    _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        raw_before = path.read_bytes()
        await _open_editor(pilot, app)
        app.screen.query_one("#f-name", Input).value = "Doomed"
        await pilot.press("escape")
        await _settle(pilot)
        assert "templates" not in app.board.settings
        assert path.read_bytes() == raw_before


async def test_single_task_line_works(tmp_path):
    """One task line is a valid template: a single entry with no `wait`."""
    path = tmp_path / "board.json"
    _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        await _open_editor(pilot, app)
        _save(app, "Solo", "One task")
        await _settle(pilot)
        assert app.board.settings["templates"] == [
            {"name": "Solo", "tasks": [{"title": "One task"}]}]
        assert _toast_check(app, "Templates",
                            "Template 'Solo' saved — 1 tasks") is None
