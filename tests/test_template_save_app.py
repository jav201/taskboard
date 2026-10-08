"""` , ` saves the selected chain as a template (batch 2026-10-07-batch-08, increment 001).

HLR-1401 / LLR-1401.2 · AT-1401.

On the chain map, `,` with a selected tile opens the one-line name prompt
(prefilled with the chain's first task title); typing a name and pressing enter
appends `{"name", "tasks"}` to `settings["templates"]` (creating the list), saves
the board, and toasts the pinned literal `Template '<name>' saved — <N> tasks`;
`I` then lists it; esc (or an empty name) cancels and leaves `settings.templates`
byte-identical; an unlinked `○` tile saves a one-task template. The batch-06
frozen-calendar seam is not needed (no date math); the conftest milestone seam
still applies.
"""
from __future__ import annotations

from pathlib import Path

from textual.widgets import Input

from taskboard.app import RENUMBER_NOTICE_KEY, TaskboardApp
from taskboard.models import Board, Project, Task


def _chain(tmp_path) -> Path:
    """A three-task chain Alpha→Beta→Gamma, on the chain map."""
    p = Project("Plat", "sky")
    a = Task("Alpha", p.id, "Doing", id="a")
    b = Task("Beta", p.id, "Doing", id="b")
    c = Task("Gamma", p.id, "Doing", id="c")
    b.depends_on = ["a"]
    c.depends_on = ["b"]
    path = tmp_path / "board.json"
    Board([p], [a, b, c], path,
          {RENUMBER_NOTICE_KEY: True, "migrations": {"links": 1}}).save()
    return path


def _lone(tmp_path) -> Path:
    """One unlinked open task — an `○` tile on the chain map."""
    p = Project("Plat", "sky")
    path = tmp_path / "board.json"
    Board([p], [Task("Lone task", p.id, "Doing", id="lone")], path,
          {RENUMBER_NOTICE_KEY: True, "migrations": {"links": 1}}).save()
    return path


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


async def test_comma_opens_the_name_prompt_prefilled(tmp_path):
    """`,` on a selected chain tile opens the one-line prompt, prefilled with the
    chain's first task title (Alpha), not the selected tile's own title."""
    path = _chain(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("6")
        await pilot.pause()
        app.selected_task_id = "b"          # a MID-chain tile
        app.refresh_view()
        await pilot.pause()
        await pilot.press(",")
        await _settle(pilot)
        from taskboard.modals import TextPrompt
        assert isinstance(app.screen, TextPrompt)
        assert app.screen.query_one("#f-text", Input).value == "Alpha"
        await pilot.press("escape")


async def test_type_a_name_and_enter_saves_and_lists_in_the_picker(tmp_path):
    """Typing a name and pressing enter appends the entry, saves, toasts the
    pinned literal, and `I` lists it first."""
    path = _chain(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("6")
        await pilot.pause()
        app.selected_task_id = "b"
        app.refresh_view()
        await pilot.pause()
        await pilot.press(",")
        await _settle(pilot)
        await pilot.press(*"Release")
        await pilot.press("enter")
        await _settle(pilot)
        assert app.board.settings["templates"] == [{"name": "Release", "tasks": [
            {"title": "Alpha"},
            {"title": "Beta", "wait": 0},
            {"title": "Gamma", "wait": 1},
        ]}]
        assert _toast_check(app, "Templates", "Template 'Release' saved — 3 tasks") is None
        await pilot.press("I")
        await _settle(pilot)
        from taskboard.modals import TemplatePicker
        assert isinstance(app.screen, TemplatePicker)
        assert _plains(app.screen.query_one("#template-list"))[1] == "Release — 3 tasks"


async def test_escape_cancels_and_writes_nothing(tmp_path):
    """Esc leaves `settings.templates` byte-identical (absent), and the board file
    untouched."""
    path = _chain(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("6")
        await pilot.pause()
        app.selected_task_id = "b"
        app.refresh_view()
        await pilot.pause()
        assert "templates" not in app.board.settings
        raw_before = path.read_bytes()
        await pilot.press(",")
        await _settle(pilot)
        await pilot.press("escape")
        await _settle(pilot)
        assert "templates" not in app.board.settings
        assert path.read_bytes() == raw_before


async def test_an_unlinked_tile_saves_a_one_task_template(tmp_path):
    """An unlinked `○` tile saves a one-task template (the degenerate case)."""
    path = _lone(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(100, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("6")
        await pilot.pause()
        app.selected_task_id = "lone"
        app.refresh_view()
        await pilot.pause()
        await pilot.press(",")
        await _settle(pilot)
        await pilot.press(*"Solo")
        await pilot.press("enter")
        await _settle(pilot)
        assert app.board.settings["templates"] == [
            {"name": "Solo", "tasks": [{"title": "Lone task"}]}]
        assert _toast_check(app, "Templates", "Template 'Solo' saved — 1 tasks") is None
