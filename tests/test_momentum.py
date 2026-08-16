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



# --------------------------------------------------------------------------- #
# the priority cycle's pure seat (LLR-002.1)
# --------------------------------------------------------------------------- #
def test_next_priority_walks_the_declared_order_with_wraparound():
    """low -> normal -> high -> low, and an unknown (pre-coercion) value
    snaps to the default — a caller can never leave TASK_PRIORITIES."""
    from taskboard.models import next_priority
    assert next_priority("low") == "normal"
    assert next_priority("normal") == "high"
    assert next_priority("high") == "low"
    assert next_priority("bogus") == "normal"



# --------------------------------------------------------------------------- #
# WIP limits — the PURE getter, the ONLY write path, and the rename migration
# (batch-04 R-05, HLR-005 / LLR-005.1, §6.5 AMD-08)
# --------------------------------------------------------------------------- #
def wip_board(tmp_path, settings=None, name="wip.json"):
    return Board([], [], tmp_path / name, settings=settings,
                 phases=["Backlog", "Doing", "Review", "Done"])


def test_wip_limit_reads_settings_then_default_then_none(tmp_path):
    """LLR-005.1's whole precedence chain: an operator-set POSITIVE value wins;
    absent settings fall to the operator-approved default {"Doing": 3}; a phase
    in neither map is unlimited (None). Non-positive, non-numeric and
    unknown-phase entries are IGNORED, never guessed at."""
    b = wip_board(tmp_path)
    assert b.wip_limit("Doing") == 3                # the shipped default
    assert b.wip_limit("Backlog") is None           # in neither map -> unlimited
    assert b.wip_limit("Nope") is None              # not a phase of this board
    b2 = wip_board(tmp_path, {"wip_limits": {"Doing": 2}}, "wip2.json")
    assert b2.wip_limit("Doing") == 2               # the operator's value wins
    b3 = wip_board(tmp_path, {"wip_limits": {"Doing": 0, "Review": -1,
                                             "Nope": 9, "Backlog": "many"}},
                   "wip3.json")
    assert b3.wip_limit("Doing") == 3               # 0 ignored -> default map
    assert b3.wip_limit("Review") is None           # -1 ignored, no default
    assert b3.wip_limit("Nope") is None             # unknown-phase entry ignored
    assert b3.wip_limit("Backlog") is None          # non-numeric ignored


def test_wip_limit_getter_is_pure(tmp_path):
    """§6.5 AMD-08 / arch M-4: the getter has NO write side-effects — calling
    it (twice, for the repeat-read case) leaves board.settings unchanged AND
    writes nothing to disk. A getter that materializes the default map on
    read turns every READ into a board rewrite; that is exactly the defect
    this limb exists to redden (EXECUTED, see increment-007)."""
    import copy
    b = wip_board(tmp_path)
    b.save()
    before_disk = b.path.read_bytes()
    before_settings = copy.deepcopy(b.settings)
    assert b.wip_limit("Doing") == 3
    assert b.wip_limit("Doing") == 3                # the second read reads the same
    assert b.wip_limit("Backlog") is None
    assert b.settings == before_settings            # nothing materialized
    assert b.path.read_bytes() == before_disk       # nothing saved


def test_rename_phase_migrates_the_wip_limit(tmp_path):
    """AMD-08 / D-12: a limit FOLLOWS its phase across a rename, so renaming a
    phase can never orphan an operator-set limit (the pre-ruling drift class:
    the renamed phase silently reading as unlimited)."""
    b = wip_board(tmp_path, {"wip_limits": {"Doing": 2}})
    b.tasks.append(Task("W1", None, "Doing"))
    assert b.rename_phase("Doing", "In Progress") is True
    assert b.wip_limit("In Progress") == 2          # the limit migrated...
    assert "Doing" not in b.settings["wip_limits"]  # ...and left no orphan
    assert b.tasks[0].phase == "In Progress"        # the task rewrite still works
    assert b.rename_phase("Review", "QA") is True   # no entry -> clean rename
    assert b.wip_limit("QA") is None                # ...and still unlimited


def test_set_wip_limit_is_the_only_write_path_and_round_trips(tmp_path):
    """LLR-005.1: validation and coercion live in the SETTER, never in the
    getter. A positive value persists verbatim through save/load (the existing
    settings seat, P-10); a non-positive value CLEARS the limit instead of
    persisting something the getter would have to guess at. The caller saves
    (the rename_phase precedent). A hand-edited board file loads and reads
    without being rewritten."""
    b = wip_board(tmp_path)
    b.set_wip_limit("Review", "4")                  # coerced at the write
    assert b.settings["wip_limits"] == {"Review": 4}
    b.save()
    again = Board.load(str(b.path))
    assert again.settings["wip_limits"] == {"Review": 4}   # verbatim round-trip
    assert again.wip_limit("Review") == 4
    b.set_wip_limit("Review", 0)                    # clearing, not a bogus write
    assert "wip_limits" not in b.settings
    assert b.wip_limit("Review") is None
    b.save()
    raw = json.loads(b.path.read_text(encoding="utf-8"))
    raw["settings"] = {"wip_limits": {"Doing": 7}}
    b.path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    hand = Board.load(str(b.path))
    assert hand.wip_limit("Doing") == 7             # the hand edit is honored...
    on_disk = json.loads(b.path.read_text(encoding="utf-8"))
    assert on_disk["settings"] == {"wip_limits": {"Doing": 7}}  # ...not rewritten


# ---------------------------------------------------------------------------
# Inc 5 — the `bump_due` seat (HLR-009/LLR-009.1, TC-012)
# ---------------------------------------------------------------------------
def test_bump_due_dated_undated_and_corrupt_base():
    """TC-012 (HLR-009/LLR-009.1): a dated task moves from its OWN date
    (±1, both directions); an undated task bases on today — symmetric, so
    `-` lands on today−1; a CORRUPT stored date reads as None under
    `parse_iso` leniency and bases on today too — never on an invented
    epoch. The `=` alias half lives at the seat (ONE `"+,="` KEYMAP entry
    → the same `due_bump(1)` action; AT-015 drives it end-to-end)."""
    from taskboard.models import bump_due
    dated = Task("D", None, "Doing", due_date=iso(5))
    bump_due(dated, 1, TODAY)
    assert dated.due_date == iso(6)                     # from its own date
    bump_due(dated, -2, TODAY)
    assert dated.due_date == iso(4)
    undated = Task("U", None, "Doing", due_date=None)
    bump_due(undated, 1, TODAY)
    assert undated.due_date == iso(1)                   # undated base today
    undated_minus = Task("V", None, "Doing", due_date=None)
    bump_due(undated_minus, -1, TODAY)
    assert undated_minus.due_date == iso(-1)            # symmetric
    corrupt = Task("C", None, "Doing", due_date="not-a-date")
    bump_due(corrupt, 1, TODAY)
    assert corrupt.due_date == iso(1)                   # corrupt base today


# ---------------------------------------------------------------------------
# Inc 6 — the `standup_query` seat (HLR-011/LLR-011.1, TC-014)
# ---------------------------------------------------------------------------
def _standup_board(tmp_path, *tasks, phases=None):
    """A two-project board for the standup units — TWO projects so grouping
    has to group something and order has to order something."""
    from taskboard.models import Project
    alpha = Project("Alpha", "sky")
    beta = Project("Beta", "lime")
    b = Board([alpha, beta], list(tasks), tmp_path / "sq.json",
              phases=phases or ["Backlog", "Doing", "Review", "Done"])
    return b, alpha, beta


def test_standup_window_seven_days_in_eight_out_none_out(tmp_path):
    """TC-014 boundary pins (LLR-011.1): the stamp EXACTLY today−7 is IN,
    today−8 is OUT, a None stamp is OUT (unknown is not zero), a CORRUPT
    stamp is OUT (`parse_iso` reads it as unknown), and a stamp in the
    FUTURE is OUT (the window closes at today — clock skew is not motion).
    RED counterfactuals: `>` for `>=` → the 7d task drops out → red; an
    8-day window → the 8d task leaks in → red; None unguarded → crash or
    the unstamped task in → red; missing `<= today` → the future stamp in
    → red."""
    from taskboard.models import standup_query
    b, alpha, _beta = _standup_board(
        tmp_path,
        Task("w-today", None, "Doing", phase_changed=iso(0)),
        Task("w-seven", None, "Doing", phase_changed=iso(-7)),
        Task("w-eight", None, "Doing", phase_changed=iso(-8)),
        Task("w-never", None, "Doing", phase_changed=None),
        Task("w-corrupt", None, "Doing", phase_changed="not-a-date"),
        Task("w-future", None, "Doing", phase_changed=iso(1)),
    )
    shown = {t.title for _name, items in standup_query(b, TODAY, False)
             for t, _d in items}
    assert shown == {"w-today", "w-seven"}


def test_standup_groups_visible_projects_order_inbox_last_no_ghosts(tmp_path):
    """TC-014 grouping pins (LLR-011.1): groups follow `visible_projects`
    order — NOT board.tasks order — with the Inbox (project-less, and any
    mover whose project is not visible) LAST; a project with no movers gets
    NO section (an empty group header is a ghost mark); an archived TASK is
    out with show_archived=False and in with True. RED counterfactuals:
    groups emitted in task order → the order limb red; empty groups kept →
    the ghost limb red; the inbox placed first → the order limb red."""
    from taskboard.models import standup_query
    b, alpha, beta = _standup_board(
        tmp_path,
        Task("g-inbox", None, "Doing", phase_changed=iso(-1)),
        Task("g-beta", None, "Doing", phase_changed=iso(-1)),
        Task("g-alpha", None, "Doing", phase_changed=iso(-1)),
        Task("g-archived", None, "Doing", phase_changed=iso(-1),
             archived=True),
    )
    b.tasks[1].project_id = beta.id            # listed before alpha's mover
    b.tasks[2].project_id = alpha.id           #   on purpose: order must
    groups = standup_query(b, TODAY, False)    #   come from the projects
    assert [name for name, _items in groups] == ["Alpha", "Beta", "Inbox"]
    assert [t.title for t, _d in groups[2][1]] == ["g-inbox"]
    assert all(t.title != "g-archived" for _n, items in groups
               for t, _d in items)
    again = standup_query(b, TODAY, True)
    assert any(t.title == "g-archived" for _n, items in again
               for t, _d in items)
    # a project with no movers is NOT a section — no ghost header
    quiet = _standup_board(tmp_path / "q", Task("g2", None, "Doing",
                                                phase_changed=iso(-1)))[0]
    quiet.tasks[0].project_id = quiet.projects[1].id
    assert [name for name, _i in standup_query(quiet, TODAY, False)] == ["Beta"]


def test_standup_done_mark_is_the_terminal_phase_not_a_done_name(tmp_path):
    """TC-014 done-mark pins (LLR-011.1: annotated via `board.is_done`):
    the mover in the LAST phase is the closed one — including a board whose
    terminal phase is NOT called "Done" — and the count arithmetic the
    modal folds is exactly (members with the mark) over (members in the
    group), recomputed here by the stated rule. RED counterfactuals: done
    read as the literal string "Done" → the renamed-terminal limb red;
    done read off the stamp alone (every mover "closed") → the moved limb
    red; archived membership leaking into the count → the fraction red."""
    from taskboard.models import standup_query
    b, alpha, _beta = _standup_board(
        tmp_path,
        Task("d-moved", None, "Review", phase_changed=iso(-2)),
        Task("d-closed", None, "Done", phase_changed=iso(-3)),
        Task("d-other", None, "Backlog", phase_changed=iso(-1)),
    )
    for t in b.tasks:
        t.project_id = alpha.id
    (_name, items), = standup_query(b, TODAY, False)
    marks = {t.title: d for t, d in items}
    assert marks == {"d-moved": False, "d-closed": True, "d-other": False}
    closed = sum(1 for _t, d in items if d)    # the modal's fraction,
    assert (closed, len(items)) == (1, 3)      # recomputed by the rule
    custom, _, _ = _standup_board(
        tmp_path / "c", Task("d-shipped", None, "Shipped",
                             phase_changed=iso(-1)),
        phases=["Open", "Shipped"])
    custom.tasks[0].project_id = custom.projects[0].id
    (_n2, items2), = standup_query(custom, TODAY, False)
    assert items2[0][1] is True, "a renamed terminal phase is not 'done'"


def test_standup_empty_week_is_an_empty_query(tmp_path):
    """TC-014 empty pin (HLR-011 boundary catalog): with nothing in the
    window the query returns NO groups — the seat the modal's one honest
    line ("Nothing moved this week.") is driven from, asserted end-to-end
    in AT-018. RED counterfactual: None read as 0 → the unstamped task
    forms a group → red."""
    from taskboard.models import standup_query
    b, _a, _b = _standup_board(
        tmp_path,
        Task("e-old", None, "Done", phase_changed=iso(-30)),
        Task("e-never", None, "Doing", phase_changed=None),
    )
    assert standup_query(b, TODAY, False) == []
