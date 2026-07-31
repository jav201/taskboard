"""Auto-archive of long-finished work, and the gantt's task order.

This is the first policy in the app that REMOVES things from view on its own,
so most of these laws are about what it may not do: it may not delete, it may
not lose a field, it may not act on a task whose completion date it does not
know, and it may not be irreversible.
"""

import json
from datetime import date, timedelta

from textual.widgets import Button

from taskboard.models import (AUTO_ARCHIVE_DAYS, Board, Project, Task,
                              days_in_phase)
from taskboard.views import gantt_tasks, nav_model, render_gantt

TODAY = date(2026, 7, 30)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def board(tmp_path, name="a.json") -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


def done_task(b, title, *, moved_days_ago=None, project=None, due=-30) -> Task:
    """A task sitting in the board's last phase, optionally with a KNOWN date of
    when it got there."""
    t = Task(title, project.id if project else None, b.phases[-1], "normal",
             due_date=iso(due))
    if moved_days_ago is not None:
        t.phase_changed = iso(-moved_days_ago)
    b.tasks.append(t)
    return t


# --------------------------------------------------------------------------- #
# who gets archived
# --------------------------------------------------------------------------- #
def test_work_finished_long_ago_is_archived(tmp_path):
    b = board(tmp_path)
    old = done_task(b, "Ancient win", moved_days_ago=40)
    assert b.auto_archive_done(TODAY) == [old]
    assert old.archived is True


def test_the_boundary_is_inclusive_and_stated(tmp_path):
    b = board(tmp_path)
    exactly = done_task(b, "Exactly at the line", moved_days_ago=AUTO_ARCHIVE_DAYS)
    day_before = done_task(b, "One day short", moved_days_ago=AUTO_ARCHIVE_DAYS - 1)
    moved = b.auto_archive_done(TODAY)
    assert moved == [exactly]
    assert day_before.archived is False


def test_a_done_task_with_no_completion_date_is_NEVER_archived(tmp_path):
    """THE LAW OF THIS INCREMENT. `phase_changed` only exists from the moment
    that field shipped, so an old board's finished work has no completion date.
    A task with no date is not old — it is UNDATED, and archiving it would be
    inventing the history the momentum increment refused to invent."""
    b = board(tmp_path)
    t = done_task(b, "Finished, but when?", moved_days_ago=None)
    assert days_in_phase(t, TODAY) is None
    assert b.auto_archive_done(TODAY) == []
    assert t.archived is False
    # ...and it stays that way however long the app runs
    assert b.auto_archive_done(TODAY + timedelta(days=3650)) == []


def test_unfinished_work_is_never_archived_however_old(tmp_path):
    b = board(tmp_path)
    t = Task("Stalled forever", None, "Doing", "normal", due_date=iso(-400))
    t.phase_changed = iso(-400)
    b.tasks.append(t)
    assert b.auto_archive_done(TODAY) == []
    assert t.archived is False


def test_bouncing_out_of_done_and_back_restarts_the_clock(tmp_path):
    """'Completed 20 days ago' means the LAST time it was completed. A task that
    was reopened last week is not old work, whatever it was before."""
    b = board(tmp_path)
    t = done_task(b, "Reopened then finished again", moved_days_ago=90)
    b.set_task_phase(t, "Doing", TODAY - timedelta(days=5))
    b.set_task_phase(t, b.phases[-1], TODAY - timedelta(days=2))
    assert b.auto_archive_done(TODAY) == []
    assert t.archived is False


def test_the_sweep_is_idempotent(tmp_path):
    b = board(tmp_path)
    done_task(b, "Ancient win", moved_days_ago=40)
    assert len(b.auto_archive_done(TODAY)) == 1
    assert b.auto_archive_done(TODAY) == []          # nothing left to do


# --------------------------------------------------------------------------- #
# nothing is lost
# --------------------------------------------------------------------------- #
def test_archiving_conserves_every_task_and_every_field(tmp_path):
    """It uses the board's ONE archive — the `archived` flag `x` toggles — so a
    swept task is still in the file, whole. The only difference permitted is
    that flag."""
    b = board(tmp_path, "conserve.json")
    p = Project("Alpha", "lime", "on_track", due_date=iso(10))
    b.projects.append(p)
    # the SWEPT task is the one that must arrive intact, so it is the one
    # carrying content — a fixture whose archived task is blank cannot notice a
    # field being dropped on the way out
    swept = done_task(b, "Ancient win", moved_days_ago=40, project=p)
    swept.notes = "what we learned, worth keeping"
    swept.urls = ["https://example.com/postmortem"]
    swept.images = ["./shots/before.png"]
    swept.priority = "high"
    swept.start_date = iso(-60)
    done_task(b, "Recent win", moved_days_ago=2, project=p)
    b.tasks.append(Task("Live work", p.id, "Doing", "high", due_date=iso(4),
                        notes="keep me", urls=["https://example.com/x"]))
    b.save()
    before = {t["id"]: t for t in json.loads(
        (tmp_path / "conserve.json").read_text(encoding="utf-8"))["tasks"]}

    b.auto_archive_done(TODAY)
    b.save()
    after = {t["id"]: t for t in json.loads(
        (tmp_path / "conserve.json").read_text(encoding="utf-8"))["tasks"]}

    assert set(before) == set(after)                  # nothing added, nothing lost
    for tid, row in after.items():
        differing = {k for k in set(row) | set(before[tid])
                     if row.get(k) != before[tid].get(k)}
        assert differing <= {"archived"}, f"{tid} changed {differing}"


def test_an_archived_task_is_hidden_but_reachable_and_reversible(tmp_path):
    b = board(tmp_path)
    t = done_task(b, "Ancient win", moved_days_ago=40)
    b.auto_archive_done(TODAY)
    assert t.id not in [x.id for x in b.visible_tasks(False)]
    assert t.id in [x.id for x in b.visible_tasks(True)]      # `v` shows it
    t.archived = False                                        # `x` brings it back
    assert t.id in [x.id for x in b.visible_tasks(False)]


def test_the_sweep_survives_a_save_and_load(tmp_path):
    b = board(tmp_path, "round.json")
    done_task(b, "Ancient win", moved_days_ago=40)
    b.auto_archive_done(TODAY)
    b.save()
    again = Board.load(str(tmp_path / "round.json"))
    assert [t.archived for t in again.tasks] == [True]
    assert again.tasks[0].title == "Ancient win"


# --------------------------------------------------------------------------- #
# the rollout, explained rather than sprung
# --------------------------------------------------------------------------- #
def test_the_report_says_what_the_sweep_can_and_cannot_know(tmp_path):
    """On a board written before `phase_changed` existed, EVERY finished task is
    unknown-age, so the sweep does nothing at all — it starts biting only as work
    is completed from now on. This report is how that is explained."""
    b = board(tmp_path)
    done_task(b, "Old, dated", moved_days_ago=40)
    done_task(b, "Recent, dated", moved_days_ago=3)
    done_task(b, "Undated one", moved_days_ago=None)
    done_task(b, "Undated two", moved_days_ago=None)
    assert b.archivable_report(TODAY) == {
        "done_on_board": 4, "archivable": 1, "too_recent": 1, "unknown_age": 2}
    assert len(b.auto_archive_done(TODAY)) == 1


def test_a_legacy_board_loses_nothing_to_the_sweep(tmp_path):
    p = tmp_path / "legacy.json"
    p.write_text(json.dumps({
        "phases": ["Backlog", "Doing", "Done"],
        "projects": [{"id": "p1", "name": "Old", "color": "sky"}],
        "tasks": [{"id": f"t{i}", "title": f"Finished {i}", "project_id": "p1",
                   "phase": "Done"} for i in range(5)],
        "settings": {},
    }, indent=2), encoding="utf-8")
    b = Board.load(p)
    assert b.auto_archive_done(TODAY) == []
    assert b.archivable_report(TODAY)["unknown_age"] == 5
    assert all(not t.archived for t in b.tasks)


# --------------------------------------------------------------------------- #
# the gantt's order
# --------------------------------------------------------------------------- #
def _mixed(tmp_path):
    b = board(tmp_path, "gantt.json")
    p = Project("Alpha", "lime", "on_track", start_date=iso(-20), due_date=iso(20))
    b.projects.append(p)
    # deliberately interleaved in board order: done, active, done, active
    b.tasks += [
        Task("Done early", p.id, "Done", "normal", due_date=iso(-14)),
        Task("Active late", p.id, "Doing", "normal", due_date=iso(9)),
        Task("Done later", p.id, "Done", "normal", due_date=iso(-3)),
        Task("Active soon", p.id, "Backlog", "normal", due_date=iso(2)),
        Task("Active undated", p.id, "Backlog", "normal", start_date=iso(1)),
    ]
    return b, p


def test_open_work_comes_first_and_finished_work_sinks_to_the_tail(tmp_path):
    """Javier: "lo que ya está hecho... que se muestren hasta el final de la
    lista (del proyecto mismo) y las que aún están activas... al tope"."""
    b, p = _mixed(tmp_path)
    order = [t.title for t in gantt_tasks(b, b.visible_tasks(False), p.id)]
    assert order == ["Active soon", "Active late", "Active undated",
                     "Done early", "Done later"]


def test_within_each_group_the_soonest_due_comes_first(tmp_path):
    b, p = _mixed(tmp_path)
    order = [t.title for t in gantt_tasks(b, b.visible_tasks(False), p.id)]
    assert order.index("Active soon") < order.index("Active late")     # +2d before +9d
    assert order.index("Active late") < order.index("Active undated")  # undated last
    assert order.index("Done early") < order.index("Done later")       # -14d before -3d


def test_the_rendered_gantt_shows_that_order(tmp_path):
    b, p = _mixed(tmp_path)
    out = str(render_gantt(b, False, None, TODAY, width=120, height=30)).split("\n")
    rows = {}
    for i, line in enumerate(out):
        for title in ("Active soon", "Active late", "Done early", "Done later"):
            if title in line:
                rows[title] = i
    assert rows["Active soon"] < rows["Active late"] < rows["Done early"] < rows["Done later"]


def test_navigation_walks_the_order_the_gantt_draws(tmp_path):
    b, p = _mixed(tmp_path)
    ids = nav_model("gantt", b, False, TODAY)[0]
    drawn = [t.id for t in gantt_tasks(b, b.visible_tasks(False), p.id)
             if t.start_date or t.due_date]
    assert [i for i in ids if i in set(drawn)] == drawn


def test_the_gantt_never_lists_an_archived_task_by_default(tmp_path):
    b, p = _mixed(tmp_path)
    swept = b.tasks[0]
    swept.phase_changed = iso(-40)
    assert b.auto_archive_done(TODAY) == [swept]
    out = str(render_gantt(b, False, None, TODAY, width=120, height=30))
    assert "Done early" not in out
    assert "Done early" in str(render_gantt(b, True, None, TODAY, width=120, height=30))


# --------------------------------------------------------------------------- #
# the DELIBERATE one-time archive, for work that predates the stamp
#
# Javier's board is the case increment 10 predicted: every finished task on it
# was done before `phase_changed` existed, so the standing 20-day sweep moves
# NOTHING and the feature reads as absent. The timer cannot fix that without
# inventing dates. A human decision can.
# --------------------------------------------------------------------------- #
def test_it_finds_exactly_the_work_the_timer_can_never_reach(tmp_path):
    """AC1's precondition. The standing sweep skips undated work forever, by
    design; this is the only thing that can move it, so it must target that set
    precisely — no dated work, no open work."""
    b = board(tmp_path, "purge.json")
    old1 = done_task(b, "Ancient, undated", moved_days_ago=None)
    old2 = done_task(b, "Also undated", moved_days_ago=None)
    dated = done_task(b, "Finished last week", moved_days_ago=6)
    live = Task("Still going", None, "Doing", "normal", due_date=iso(3))
    b.tasks.append(live)
    assert {t.id for t in b.unstamped_done()} == {old1.id, old2.id}
    assert dated.id not in {t.id for t in b.unstamped_done()}
    assert live.id not in {t.id for t in b.unstamped_done()}


def test_the_one_time_archive_never_touches_dated_work(tmp_path):
    """AC3, and the law that keeps the two paths separate: work with a known
    completion date belongs to the timer, whatever its age. A purge that swept
    it too would pull forward a decision the timer had not made."""
    b = board(tmp_path, "sep.json")
    fresh = done_task(b, "Finished yesterday", moved_days_ago=1)
    old = done_task(b, "Finished long ago", moved_days_ago=400)
    undated = done_task(b, "No date at all", moved_days_ago=None)
    moved = b.archive_unstamped_done()
    assert [t.id for t in moved] == [undated.id]
    assert fresh.archived is False and old.archived is False


def test_the_one_time_archive_invents_no_date(tmp_path):
    """AC4. It stamps NOTHING: the board still does not know when this work was
    finished, and writing a date now would make that unknowable forever — the
    same fabrication the momentum increment refused."""
    b = board(tmp_path, "nostamp.json")
    t = done_task(b, "Ancient", moved_days_ago=None)
    b.archive_unstamped_done()
    assert t.archived is True
    assert t.phase_changed is None
    assert days_in_phase(t, TODAY) is None


def test_the_one_time_archive_conserves_every_task_and_field(tmp_path):
    """AC5. Same conservation the timer obeys: nothing is deleted and no field
    changes but the flag."""
    b = board(tmp_path, "conserve2.json")
    t = done_task(b, "Ancient with content", moved_days_ago=None)
    t.notes = "worth keeping"
    t.urls = ["https://example.com/x"]
    t.priority = "high"
    b.tasks.append(Task("Live", None, "Doing", "normal", due_date=iso(2)))
    b.save()
    before = {x["id"]: x for x in json.loads(
        (tmp_path / "conserve2.json").read_text(encoding="utf-8"))["tasks"]}
    b.archive_unstamped_done()
    b.save()
    after = {x["id"]: x for x in json.loads(
        (tmp_path / "conserve2.json").read_text(encoding="utf-8"))["tasks"]}
    assert set(before) == set(after)
    for tid, row in after.items():
        differing = {k for k in set(row) | set(before[tid])
                     if row.get(k) != before[tid].get(k)}
        assert differing <= {"archived"}, f"{tid} changed {differing}"


def test_the_purge_is_reversible_like_any_archive(tmp_path):
    """AC6. It lands in the ordinary archive — no second store, no new path."""
    b = board(tmp_path, "rev.json")
    t = done_task(b, "Ancient", moved_days_ago=None)
    b.archive_unstamped_done()
    assert t.id not in [x.id for x in b.visible_tasks(False)]
    assert t.id in [x.id for x in b.visible_tasks(True)]      # `v` shows it
    t.archived = False                                         # `x` brings it back
    assert t.id in [x.id for x in b.visible_tasks(False)]


def test_after_the_purge_the_timer_owns_the_future(tmp_path):
    """AC7, and the point of the whole design: ONE deliberate sweep for the past,
    and the 20-day rule from then on, because work stamps itself when it moves."""
    b = board(tmp_path, "future.json")
    done_task(b, "Ancient", moved_days_ago=None)
    b.archive_unstamped_done()
    assert b.unstamped_done() == []
    t = Task("New work", None, "Doing", "normal", due_date=iso(1))
    b.tasks.append(t)
    b.set_task_phase(t, b.phases[-1], TODAY - timedelta(days=AUTO_ARCHIVE_DAYS))
    assert b.auto_archive_done(TODAY) == [t]


async def test_the_purge_says_the_count_before_it_moves_anything(tmp_path):
    """AC1. It must state what it is about to do, with the RIGHT number, and wait
    for a yes — an archive that just happens is what erodes trust in one."""
    from taskboard.app import TaskboardApp
    from taskboard.modals import ConfirmModal
    b = board(tmp_path, "flow.json")
    for i in range(3):
        done_task(b, f"Ancient {i}", moved_days_ago=None)
    done_task(b, "Dated", moved_days_ago=2)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "flow.json"))
    async with app.run_test(size=(100, 30)) as pilot:
        await pilot.press("X")
        await pilot.pause()
        assert isinstance(app.screen, ConfirmModal)
        assert "3 finished task" in app.screen.message, app.screen.message
        assert "'v'" in app.screen.message and "'x'" in app.screen.message
        assert all(not t.archived for t in app.board.tasks)   # nothing moved yet
        await pilot.press("escape")
        await pilot.pause()
        assert all(not t.archived for t in app.board.tasks)   # cancel moves nothing


async def test_confirming_the_purge_archives_and_says_so(tmp_path):
    """AC2."""
    from taskboard.app import TaskboardApp
    b = board(tmp_path, "flow2.json")
    for i in range(2):
        done_task(b, f"Ancient {i}", moved_days_ago=None)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "flow2.json"))
    said = []
    async with app.run_test(size=(100, 30)) as pilot:
        app.notify = lambda *a, **k: said.append(a[0] if a else "")
        await pilot.press("X")
        await pilot.pause()
        app.screen.query_one("#yes", Button).press()
        await pilot.pause()
        assert sum(t.archived for t in app.board.tasks) == 2
        assert any("2 finished task" in m for m in said), said
    reloaded = Board.load(str(tmp_path / "flow2.json"))
    assert sum(t.archived for t in reloaded.tasks) == 2        # persisted


async def test_the_purge_says_so_when_there_is_nothing_to_do(tmp_path):
    """AC8. Silence would read as a broken key."""
    from taskboard.app import TaskboardApp
    from taskboard.modals import ConfirmModal
    b = board(tmp_path, "empty2.json")
    done_task(b, "Dated", moved_days_ago=3)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "empty2.json"))
    said = []
    async with app.run_test(size=(100, 30)) as pilot:
        app.notify = lambda *a, **k: said.append(k.get("title", ""))
        await pilot.press("X")
        await pilot.pause()
        assert any("Nothing to archive" in t for t in said), said
        assert not isinstance(app.screen, ConfirmModal)


async def test_the_edit_modal_can_archive_the_task_it_has_open(tmp_path):
    """AC9. The capability where he looked for it — IN ADDITION to `x`, not
    instead of it."""
    from textual.widgets import Checkbox

    from taskboard.app import TaskboardApp
    b = board(tmp_path, "edit.json")
    t = Task("A task", None, "Doing", "normal", due_date=iso(4))
    b.tasks.append(t)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "edit.json"))
    async with app.run_test(size=(100, 40)) as pilot:
        app.selected_task_id = t.id
        await pilot.press("e")
        await pilot.pause()
        box = app.screen.query_one("#f-archived", Checkbox)
        assert box.value is False
        box.value = True
        app.screen.query_one("#save", Button).press()
        await pilot.pause()
        assert app.board.task_by_id(t.id).archived is True
    assert Board.load(str(tmp_path / "edit.json")).tasks[0].archived is True


async def test_x_still_toggles_the_archive_from_the_board(tmp_path):
    """AC9's other half: the editor control is an ADDITION. `x` keeps working."""
    from taskboard.app import TaskboardApp
    b = board(tmp_path, "xkey.json")
    t = Task("A task", None, "Doing", "normal", due_date=iso(4))
    b.tasks.append(t)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "xkey.json"))
    async with app.run_test(size=(100, 30)) as pilot:
        app.selected_task_id = t.id
        await pilot.press("x")
        await pilot.pause()
        assert app.board.task_by_id(t.id).archived is True
        # and back: an archived task is HIDDEN, so `x` alone cannot undo itself —
        # `v` reveals it first. That two-step is exactly what the purge's confirm
        # text tells the reader ("'v' shows them, 'x' brings one back").
        await pilot.press("v")
        await pilot.pause()
        app.selected_task_id = t.id
        await pilot.press("x")
        await pilot.pause()
        assert app.board.task_by_id(t.id).archived is False


def test_the_purge_key_is_in_the_seat_and_on_the_bar():
    """AC10. The key-bar contract reaches this feature too: a capability whose
    key is not on screen does not exist."""
    from taskboard.keymap import KEYMAP, fit_bar
    entry = next(k for k in KEYMAP if k.action == "purge_done")
    assert entry.show == "X"
    shown = {show for show, _label in fit_bar(400, "swimlanes")[0]}
    assert "X" in shown
