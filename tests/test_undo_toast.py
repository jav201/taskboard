"""`u` on a single-task change names the task it brought back (HLR-1103).

Field report (ux UXV-3): after `M` in the kanban the card leaves or rejoins the
columns with no message, so the operator scans the board for what changed. The
single-task undo branch of `action_undo` — the fall-through after the cascade /
milestones / migration branches — restored the task's fields (or re-inserted a
deleted task), saved and refreshed in SILENCE. Law (LLR-1103.1): that branch
toasts ONE line naming the task whose change came back, `markup=False`, before
the save; the cascade / milestones / migration branches and the stale-skip stay
exactly as shipped.

Method: the house pilot pattern — a real `TaskboardApp` in `run_test`, a single-
task mutation driven with keys (`t` pins the selected task, pushing a one-task
field snapshot), then `u`, and the toast is read off the painted `Toast` (like
`test_markup_sites.py`'s `_toast_check`). The negative arm purges the task after
the snapshot (the one destructive route undo does not cover) and asserts the
naming toast stays absent — the skip branch is untouched, so only the
"Nothing to undo." notice survives.
"""
from __future__ import annotations

from taskboard.app import RENUMBER_NOTICE_KEY, TaskboardApp
from taskboard.models import Board, Project, Task

TITLE = "Write the migration guide"
UNDONE = f"Undone — {TITLE} is back as it was."


def _board(tmp_path) -> Board:
    """One project, one task; the renumber notice already seen so its toast
    does not crowd the one under test."""
    p = Project("Plat", "sky")
    t = Task(TITLE, p.id, "Doing")
    b = Board([p], [t], tmp_path / "board.json", {RENUMBER_NOTICE_KEY: True})
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


async def _settle(pilot, n=3):
    for _ in range(n):
        await pilot.pause()


async def test_AT_1103_undo_names_the_single_task(tmp_path):
    """AT-1103 (HLR-1103, US-1103) — `u` after `t` names the task exactly.

    `t` pins the selected task, which is a one-task mutation (a field snapshot
    with no `task` object), so the undo walks the single-task fall-through and
    toasts the pinned literal with the task's title, exactly."""
    board = _board(tmp_path)
    app = TaskboardApp(board_path=str(board.path), team_sync_interval=1e9)
    async with app.run_test(size=(80, 24), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("t")                 # a one-task mutation
        await _settle(pilot)
        assert app.board.tasks[0].pinned is True
        await pilot.press("u")
        await _settle(pilot)
        assert _toast_check(app, "Undo", UNDONE) is None
        assert app.board.tasks[0].pinned is False


async def test_AT_1103_purged_entry_stays_silent(tmp_path):
    """The negative control (LLR-1103.1) — a stale entry skips in silence.

    The task is purged after the `t` snapshot (the destructive route undo does
    not cover), so `u` hits the `task_by_id(...) is None` / no-`task`-object
    skip and falls through to "Nothing to undo." — the naming toast is absent,
    and it is the skip branch (not the notify) that stays untouched."""
    board = _board(tmp_path)
    app = TaskboardApp(board_path=str(board.path), team_sync_interval=1e9)
    async with app.run_test(size=(80, 24), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("t")                 # snapshot the task
        await _settle(pilot)
        app.board.delete_task(app.board.tasks[0].id)   # purged since the snapshot
        await pilot.press("u")
        await _settle(pilot)
        for t in _toasts(app):
            assert UNDONE not in t
        assert any("Nothing to undo" in t for t in _toasts(app))
