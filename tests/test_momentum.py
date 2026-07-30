"""Momentum — the one figure the board could not answer, and what it costs.

`views.py` ruled for the gantt that "we store no phase-transition timestamps,
so a velocity/ETA is not computable and must not be invented". This increment
makes the board record them from now on. The whole point of these tests is the
HONESTY of the gap: a board written before the field existed knows nothing
about its own history, and every one of its tasks must read as UNKNOWN — never
as fresh, never as zero.
"""

import json
from datetime import date, timedelta

from taskboard.models import Board, Project, Task, days_in_phase
from taskboard.views import lanes_of, render_swimlanes, sitting

TODAY = date(2026, 7, 30)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def board(tmp_path, name="m.json"):
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


# --------------------------------------------------------------------------- #
# the model
# --------------------------------------------------------------------------- #
def test_a_task_that_never_moved_has_no_age(tmp_path):
    """UNKNOWN IS NOT ZERO. This is the state every task on every existing board
    is in the moment this ships."""
    assert days_in_phase(Task("Old thing"), TODAY) is None


def test_moving_a_task_dates_the_move(tmp_path):
    b = board(tmp_path)
    t = Task("Thing", None, "Backlog")
    b.tasks.append(t)
    assert b.set_task_phase(t, "Doing", TODAY) is True
    assert t.phase == "Doing"
    assert t.phase_changed == TODAY.isoformat()
    assert days_in_phase(t, TODAY) == 0
    assert days_in_phase(t, TODAY + timedelta(days=6)) == 6


def test_saving_a_task_without_moving_it_does_not_reset_its_clock(tmp_path):
    """Otherwise every edit would make stale work look fresh — the figure would
    measure how recently you opened the editor, not how long the work has sat."""
    b = board(tmp_path)
    t = Task("Thing", None, "Backlog")
    b.tasks.append(t)
    b.set_task_phase(t, "Doing", TODAY - timedelta(days=20))
    assert b.set_task_phase(t, "Doing", TODAY) is False
    assert days_in_phase(t, TODAY) == 20


def test_the_stamp_survives_a_save_and_load(tmp_path):
    b = board(tmp_path, "round.json")
    t = Task("Thing", None, "Backlog")
    b.tasks.append(t)
    b.set_task_phase(t, "Doing", TODAY - timedelta(days=3))
    b.save()
    again = Board.load(str(tmp_path / "round.json"))
    assert days_in_phase(again.tasks[0], TODAY) == 3


def test_an_old_board_loads_and_stays_honestly_unknown(tmp_path):
    """The field is additive: an old file has no `phase_changed`, and loading it
    must not back-fill one. A guessed date is a fabricated measurement."""
    p = tmp_path / "old.json"
    p.write_text(json.dumps({
        "phases": ["Backlog", "Doing", "Done"],
        "projects": [{"id": "p1", "name": "Old", "color": "sky"}],
        "tasks": [{"id": "t1", "title": "Ancient", "project_id": "p1",
                   "phase": "Doing"}],
        "settings": {},
    }, indent=2), encoding="utf-8")
    b = Board.load(p)
    assert b.tasks[0].phase_changed is None
    assert days_in_phase(b.tasks[0], TODAY) is None
    b.save()
    assert json.loads(p.read_text(encoding="utf-8"))["tasks"][0]["phase_changed"] is None


def test_a_garbage_stamp_reads_as_unknown_not_as_a_crash(tmp_path):
    t = Task("Thing", phase_changed="not-a-date")
    assert days_in_phase(t, TODAY) is None


def test_a_stamp_in_the_future_never_reports_negative_age(tmp_path):
    t = Task("Thing", phase_changed=iso(5))
    assert days_in_phase(t, TODAY) == 0


# --------------------------------------------------------------------------- #
# what the view is allowed to say
# --------------------------------------------------------------------------- #
def _lane(b, name):
    return next(ln for ln in lanes_of(b, False, TODAY) if ln.name == name)


def test_the_view_says_unaged_when_the_board_knows_nothing(tmp_path):
    b = board(tmp_path)
    p = Project("Alpha", "lime", "on_track", due_date=iso(10))
    b.projects.append(p)
    b.tasks.append(Task("Untouched", p.id, "Doing", "normal", due_date=iso(-2)))
    assert sitting(_lane(b, "Alpha"), TODAY) == "unaged"
    out = str(render_swimlanes(b, False, None, TODAY, width=96, height=30))
    assert "unaged" in out
    assert "0d in phase" not in out          # the lie this test exists to prevent


def test_the_view_reports_the_most_stagnant_task_once_it_is_dated(tmp_path):
    b = board(tmp_path)
    p = Project("Alpha", "lime", "on_track", due_date=iso(10))
    b.projects.append(p)
    fresh = Task("Fresh", p.id, "Backlog", "normal", due_date=iso(3))
    stale = Task("Stale", p.id, "Backlog", "normal", due_date=iso(-2))
    b.tasks += [fresh, stale]
    b.set_task_phase(fresh, "Doing", TODAY - timedelta(days=1))
    b.set_task_phase(stale, "Doing", TODAY - timedelta(days=17))
    assert sitting(_lane(b, "Alpha"), TODAY) == "17d in phase"
    assert "17d in phase" in str(render_swimlanes(b, False, None, TODAY,
                                                  width=96, height=30))


def test_a_partly_dated_project_reports_both_halves(tmp_path):
    """The mixed state is the REAL state of any board that has been running a
    while: some work has moved since the stamp existed, some never has. Reporting
    only the known half would quietly shrink the project's age."""
    b = board(tmp_path)
    p = Project("Alpha", "lime", "on_track", due_date=iso(10))
    b.projects.append(p)
    moved = Task("Moved", p.id, "Backlog", "normal", due_date=iso(3))
    never = Task("Never moved", p.id, "Backlog", "normal", due_date=iso(4))
    b.tasks += [moved, never]
    b.set_task_phase(moved, "Doing", TODAY - timedelta(days=9))
    assert sitting(_lane(b, "Alpha"), TODAY) == "9d in phase · 1 unaged"


def test_a_project_with_nothing_open_says_nothing_about_momentum(tmp_path):
    b = board(tmp_path)
    p = Project("Alpha", "lime", "on_track", due_date=iso(10))
    b.projects.append(p)
    b.tasks.append(Task("Done", p.id, "Done", "normal", due_date=iso(-2)))
    assert sitting(_lane(b, "Alpha"), TODAY) == ""


def test_momentum_never_wears_a_judging_hue(tmp_path):
    """Stagnation is not urgency: severity's one seat is the date chip, and this
    figure is neither identity nor severity, so it stays on the quiet step."""
    from taskboard.views import HEX
    b = board(tmp_path)
    p = Project("Alpha", "lime", "on_track", due_date=iso(10))
    b.projects.append(p)
    t = Task("Stale", p.id, "Backlog", "normal", due_date=iso(5))
    b.tasks.append(t)
    b.set_task_phase(t, "Doing", TODAY - timedelta(days=30))
    text = render_swimlanes(b, False, None, TODAY, width=96, height=30)
    worn = [(str(s.style), text.plain[s.start:s.end]) for s in text.spans
            if "in phase" in text.plain[s.start:s.end]]
    assert worn
    for style, _seg in worn:
        assert HEX["dim"] in style
        assert HEX["over"] not in style and HEX["soon"] not in style
