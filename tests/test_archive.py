"""Auto-archive of long-finished work, and the gantt's task order.

This is the first policy in the app that REMOVES things from view on its own,
so most of these laws are about what it may not do: it may not delete, it may
not lose a field, it may not act on a task whose completion date it does not
know, and it may not be irreversible.
"""

import json
from datetime import date, timedelta

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
