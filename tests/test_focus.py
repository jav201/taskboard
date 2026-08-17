"""Focus Board: pinned tasks, pinned projects, and the three presentations."""

from __future__ import annotations

import pytest

from taskboard.app import TaskboardApp
from taskboard.models import Board
from taskboard.views import focus_tasks, render_focus


def _make_app(tmp_path) -> TaskboardApp:
    return TaskboardApp(board_path=str(tmp_path / "board.json"))


def _board_text(app) -> str:
    return str(app.query_one("#board").render())


async def test_pin_task_persists_and_appears_in_focus(tmp_path):
    board_path = str(tmp_path / "board.json")
    app = _make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        target = next(t for t in app.board.tasks if t.title == "Audit dependencies")
        app.selected_task_id = target.id
        await pilot.press("t")
        await pilot.pause()
        assert target.pinned is True
        await pilot.press("5")
        await pilot.pause()
        assert app.view_mode == "focus"
        text = _board_text(app)
        assert "FOCUS" in text
        assert "Audit dependencies" in text
    reloaded = Board.load(board_path)
    assert any(t.title == "Audit dependencies" and t.pinned for t in reloaded.tasks)


async def test_project_pin_includes_all_its_tasks(tmp_path):
    app = _make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        # pick a task from Website Redesign
        target = next(t for t in app.board.tasks
                      if t.title == "Fix checkout 500 error")
        app.selected_task_id = target.id
        await pilot.press("T")
        await pilot.pause()
        proj = app.board.project_by_id(target.project_id)
        assert proj is not None and proj.pinned is True
        await pilot.press("5")
        await pilot.pause()
        text = _board_text(app)
        # all Website Redesign tasks should appear, not just the selected one
        assert "Fix checkout 500 error" in text
        assert "Design homepage mockups" in text
        assert "Optimize image assets" in text


async def test_focus_tab_cycles_presentations(tmp_path):
    app = _make_app(tmp_path)
    async with app.run_test(size=(140, 40)) as pilot:
        target = next(t for t in app.board.tasks if t.title == "Audit dependencies")
        app.selected_task_id = target.id
        await pilot.press("t")
        await pilot.press("5")
        await pilot.pause()
        assert app.focus_presentation == "cards"
        text1 = _board_text(app)
        assert "FOCUS" in text1
        await pilot.press("tab")
        await pilot.pause()
        assert app.focus_presentation == "inspector"
        text2 = _board_text(app)
        assert "Notes" in text2
        await pilot.press("tab")
        await pilot.pause()
        assert app.focus_presentation == "images"
        text3 = _board_text(app)
        assert "with images" in text3 or "without images" in text3


async def test_focus_respects_archived_toggle(tmp_path):
    app = _make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        archived = next(t for t in app.board.tasks if t.title == "Archive old logs")
        archived.pinned = True
        app.board.save()
        await pilot.press("5")
        await pilot.pause()
        assert "Archive old logs" not in _board_text(app)
        await pilot.press("v")
        await pilot.press("5")
        await pilot.pause()
        assert "Archive old logs" in _board_text(app)


async def test_inbox_task_project_pin_is_no_op_and_notifies(tmp_path):
    app = _make_app(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        inbox_task = next(t for t in app.board.tasks if t.project_id is None)
        app.selected_task_id = inbox_task.id
        notes = []
        app.notify = lambda *a, **k: notes.append(k.get("title", ""))
        await pilot.press("T")
        await pilot.pause()
        assert "Pin project" in notes
        # board still switches to focus cleanly
        await pilot.press("5")
        await pilot.pause()
        assert app.view_mode == "focus"


def test_focus_tasks_union_is_unique():
    """focus_tasks returns each task once: individually pinned + project pinned."""
    from taskboard.models import Project, Task
    p1 = Project("P1", "sky")
    p2 = Project("P2", "violet", pinned=True)
    t1 = Task("t1", p1.id, pinned=True)
    t2 = Task("t2", p2.id)
    t3 = Task("t3", p2.id, pinned=True)
    board = Board([p1, p2], [t1, t2, t3], path=__import__("pathlib").Path("/dev/null"))
    found = focus_tasks(board, show_archived=False)
    assert len(found) == 3
    assert {t.title for t in found} == {"t1", "t2", "t3"}


def test_render_focus_presentations_smoke():
    from taskboard.models import Project, Task
    from datetime import date
    p = Project("P1", "sky")
    t = Task("task with note", p.id, due_date=date.today().isoformat(),
             pinned=True,
             notes="- [ ] todo\n- [x] done", images=["a.png"], urls=["https://x.co"])
    board = Board([p], [t], path=__import__("pathlib").Path("/dev/null"))
    for pres in ("cards", "inspector", "images"):
        text = str(render_focus(board, False, t.id, today=date.today(),
                                width=80, height=24, presentation=pres))
        assert "FOCUS" in text
        assert "task with note" in text
