"""`I` inserts a process template as a linked chain (batch 2026-10-07-batch-07,
increment 001).

HLR-1301 / LLR-1301.2 · AT-1301.

`I` opens the picker — user templates first, then the presets `Simple chain` and
`Bugfix`, each row `name — N tasks`; picking one creates its tasks in the
selected task's project, in the board's FIRST phase, with no dates, linked
exactly as the template declares (a forward-only `wait` index); the whole insert
is ONE undo step; the toast is the pinned literal. v1 edits templates by hand in
the board's JSON (`settings.templates`).
"""
from __future__ import annotations

from pathlib import Path

from taskboard.app import RENUMBER_NOTICE_KEY, TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.modals import TemplatePicker


def _board(tmp_path, settings=None, with_project=True) -> Board:
    if with_project:
        p = Project("Plat", "sky")
        t = Task("Existing task", p.id, "Doing")
        projects, tasks = [p], [t]
    else:
        projects, tasks = [], []
    b = Board(projects, tasks, tmp_path / "board.json",
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


async def test_I_opens_the_picker_listing_presets_with_counts(tmp_path):
    """`I` opens the picker; with no user templates the presets list first, each
    with its task count."""
    path = tmp_path / "board.json"
    _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30)) as pilot:
        await pilot.pause()
        await pilot.press("I")
        await _settle(pilot)
        assert isinstance(app.screen, TemplatePicker)
        assert _plains(app.screen.query_one("#template-list")) == \
            ["New template...", "Simple chain — 3 tasks", "Bugfix — 3 tasks"]


async def test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo(tmp_path):
    """Picking `Simple chain` on a board with a selected task creates 3 tasks in
    that task's project, first phase, no dates, `depends_on` exactly the forward
    chain; the toast equals the pinned literal; one `u` removes all three; a
    second `u` says "Nothing to undo."."""
    path = tmp_path / "board.json"
    _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        t = app.board.tasks[0]
        app.selected_task_id = t.id
        n0 = len(app.board.tasks)
        await pilot.press("I")
        await _settle(pilot)
        await pilot.press("down", "enter")  # past 'New template...' to Simple chain
        await _settle(pilot)
        assert len(app.board.tasks) == n0 + 3
        created = app.board.tasks[n0:]
        assert [c.title for c in created] == ["Plan", "Build", "Ship"]
        for c in created:
            assert (c.project_id, c.phase, c.start_date, c.due_date) == \
                (t.project_id, "Backlog", None, None)
        assert created[0].depends_on == []
        assert created[1].depends_on == [created[0].id]
        assert created[2].depends_on == [created[1].id]
        assert app.selected_task_id == created[0].id
        assert _toast_check(app, "Templates",
                            "Inserted 'Simple chain' — 3 tasks into Plat") is None
        await pilot.press("u")
        await _settle(pilot)
        assert len(app.board.tasks) == n0
        await pilot.press("u")
        await _settle(pilot)
        assert any("Nothing to undo" in t for t in _toasts(app))


async def test_no_project_refuses_with_the_toast(tmp_path):
    """A board with no resolvable project -> the refusal toast, no picker."""
    path = tmp_path / "board.json"
    _board(tmp_path, with_project=False)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("I")
        await _settle(pilot)
        assert not isinstance(app.screen, TemplatePicker)
        assert _toast_check(app, "Templates", "No project to insert into.") is None


async def test_user_template_lists_before_presets_and_inserts_with_links(tmp_path):
    """A user template lists BEFORE the presets and inserts with its links."""
    path = tmp_path / "board.json"
    _board(tmp_path, settings={"templates": [
        {"name": "Deploy", "tasks": [
            {"title": "Build"},
            {"title": "Smoke", "wait": 0},
        ]},
    ]})
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        t = app.board.tasks[0]
        app.selected_task_id = t.id
        n0 = len(app.board.tasks)
        await pilot.press("I")
        await _settle(pilot)
        assert _plains(app.screen.query_one("#template-list")) == \
            ["New template...", "Deploy — 2 tasks",
             "Simple chain — 3 tasks", "Bugfix — 3 tasks"]
        await pilot.press("down", "enter")  # past 'New template...' to Deploy
        await _settle(pilot)
        assert len(app.board.tasks) == n0 + 2
        created = app.board.tasks[n0:]
        assert [c.title for c in created] == ["Build", "Smoke"]
        assert created[0].depends_on == []
        assert created[1].depends_on == [created[0].id]
        assert _toast_check(app, "Templates",
                            "Inserted 'Deploy' — 2 tasks into Plat") is None


async def test_empty_template_toasts_is_empty(tmp_path):
    """An empty template (0 tasks) inserts nothing and toasts `is empty`."""
    path = tmp_path / "board.json"
    _board(tmp_path, settings={"templates": [{"name": "Empty", "tasks": []}]})
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        t = app.board.tasks[0]
        app.selected_task_id = t.id
        n0 = len(app.board.tasks)
        await pilot.press("I")
        await _settle(pilot)
        await pilot.press("down", "enter")  # past 'New template...' to Empty — 0 tasks
        await _settle(pilot)
        assert len(app.board.tasks) == n0
        assert _toast_check(app, "Templates", "Template 'Empty' is empty.") is None
