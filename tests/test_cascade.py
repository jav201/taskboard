"""The cascade engine: moving a task's dates moves what waits on it (batch 2026-10-06-batch-01,
US-604, HLR-604, LLR-604.1).

Law (the round-6 verdict + the contract): `plan_move` plans, writes nothing; `push_delta`
(default) pushes a dependent later by only the overlap the move ADDED — slack absorbs, a
pre-existing overlap is tolerated, zero/earlier pulls nothing; `together` shifts the whole open
downstream by the due delta, both directions; `flag` moves nothing else; done/archived never
move and stop the chain; a milestone moves whole; the overlap measure is the shipped
`link_overlap`'s (D-633); an undated moved task bases on today. Boards are synthetic
(`tests/kg_board.py`) in memory.

RED on base: no `plan_move` in `taskboard.models` (the engine does not exist).
"""
from __future__ import annotations

import json
from datetime import date, timedelta

import kg_board
from taskboard.models import (Board, Task, apply_plan, link_overlap, plan_move, parse_iso,
                              restore, resolve_mode, snapshot)

KT = kg_board.TODAY


def _b() -> Board:
    return kg_board.milestones(kg_board.build())


def _d(off: int) -> date:
    return KT + timedelta(days=off)


def _dates(t: Task):
    s, d = parse_iso(t.start_date), parse_iso(t.due_date)
    if t.milestone and d:
        s = d
    return s, d


def _dump(b: Board) -> str:
    return json.dumps([Board._to_dict(t) for t in b.tasks]
                      + [Board._to_dict(p) for p in b.projects], sort_keys=True)


# --------------------------------------------------------------------------- #
# TC-618/619 — push_delta moves the ADDED overlap; zero/earlier pull nothing
# --------------------------------------------------------------------------- #
def test_TC_618_push_delta_moves_the_added_overlap_never_the_strict_repair():
    """TC-618 (LLR-604.1): tm2 +3 pushes tm3 +3 (its overlap 2d -> 5d) and tm4 +3
    (3d -> 6d), tm5 untouched (7d of slack); strict push on the same move slips
    the project past its due — the contrast the verdict rejected. RED on base:
    plan_move does not exist."""
    b = _b()
    p = plan_move(b, "tm2", 3, 3, "push_delta", KT)
    assert {k: p.shift[k] for k in p.moved} == {"tm2": 3, "tm3": 3, "tm4": 3}
    assert p.moved["tm3"] == (_d(4), _d(15))
    assert p.moved["tm4"] == (_d(13), _d(31))
    assert "tm5" not in p.moved
    assert p.new_conflicts == []
    strict = plan_move(b, "tm2", 3, 3, "push", KT)
    assert "tm5" in strict.moved
    assert strict.project_over.get("pmob", 0) > p.project_over.get("pmob", 0)


def test_TC_619_zero_and_earlier_moves_pull_nothing_together_pulls_back_and_keeps_gaps():
    """TC-619: a zero move and an earlier move move nobody under push_delta; under
    together every open transitive dependent shifts by the due delta, both ways,
    every gap kept."""
    b = _b()
    z = plan_move(b, "tm2", 0, 0, "push_delta", KT)
    assert set(z.moved) == {"tm2"}
    e = plan_move(b, "tm2", -1, -1, "push_delta", KT)
    assert set(e.moved) == {"tm2"}
    t = plan_move(b, "tm2", -1, -1, "together", KT)
    assert {k: t.shift[k] for k in t.moved} == {"tm2": -1, "tm3": -1, "tm4": -1, "tm5": -1}
    for tid in ("tm3", "tm4", "tm5"):
        (s0, d0), (s1, d1) = _dates(b.task_by_id(tid)), t.moved[tid]
        assert (d1 - s1) == (d0 - s0)                      # durations preserved
    assert t.moved["tm5"][0] == t.moved["tm5"][1]          # the milestone stays whole
    f = plan_move(b, "tm2", -1, -1, "flag", KT)
    assert set(f.moved) == {"tm2"}
    f2 = plan_move(b, "tm2", 1, 1, "flag", KT)
    assert f2.new_conflicts == [("tm3", "tm2", 1)]      # ADDED days (2d -> 3d), never the total


# --------------------------------------------------------------------------- #
# TC-620/621 — chain honesty: done/archived stop; a milestone moves whole
# --------------------------------------------------------------------------- #
def test_TC_620_done_and_archived_dependents_never_move_and_stop_the_chain():
    """TC-620: with tm3 Done (or archived), tm2 +3 moves tm2 alone — the cascade
    stops at the closed task (its dependents' wait is satisfied)."""
    for close in ("done", "archived"):
        b = _b()
        t3 = b.task_by_id("tm3")
        if close == "done":
            t3.phase = b.phases[-1]
        else:
            t3.archived = True
        p = plan_move(b, "tm2", 3, 3, "push_delta", KT)
        assert set(p.moved) == {"tm2"}, close


def test_TC_621_a_milestone_moves_whole_and_its_waiters_compare_dues():
    """TC-621: td0 (milestone, start == due) +5 moves whole (start == due after),
    start_delta ignored; td5's slack absorbs the move (it stays). A bump on td4
    that grows td0's overlap pushes the milestone whole by the added days, and
    apply_plan stores it whole."""
    b = _b()
    p = plan_move(b, "td0", 0, 5, "push_delta", KT)
    assert p.moved["td0"] == (_d(23), _d(23))
    assert "td5" not in p.moved                                 # slack absorbs
    q = plan_move(b, "td0", 3, 5, "push_delta", KT)             # start delta ignored
    assert q.moved["td0"] == p.moved["td0"]
    r = plan_move(b, "td4", 0, 1, "push_delta", KT)             # overlap 1d -> 2d
    assert r.moved["td0"] == (_d(19), _d(19)) and r.shift["td0"] == 1
    snap = snapshot(b, r)
    apply_plan(b, r)
    x = b.task_by_id("td0")
    assert x.start_date == x.due_date                           # stored whole
    restore(b, snap)


# --------------------------------------------------------------------------- #
# TC-622 — resolve_mode: default, per-project, per-move override, cross-project
# --------------------------------------------------------------------------- #
def test_TC_622_resolve_mode_and_the_moved_tasks_project_decides():
    """TC-622: default push_delta; a project's date_links wins; a per-move override
    wins over both; a cross-project link follows the MOVED task's project."""
    b = _b()
    assert resolve_mode(b, "tm2") == "push_delta"
    b.project_by_id("pdwh").extra["date_links"] = "together"
    assert resolve_mode(b, "td4") == "together"
    assert resolve_mode(b, "td4", override="flag") == "flag"
    b.task_by_id("td2").depends_on = ["ta4"]
    b.project_by_id("papi").extra["date_links"] = "together"
    p = plan_move(b, "ta4", 5, 5, resolve_mode(b, "ta4"), KT)
    assert "td2" in p.moved and p.shift["td2"] == 5
    q = plan_move(b, "ta4", 5, 5, resolve_mode(b, "ta4", override="flag"), KT)
    assert set(q.moved) == {"ta4"}


# --------------------------------------------------------------------------- #
# TC-623 — snapshot/apply/restore
# --------------------------------------------------------------------------- #
def test_TC_623_apply_then_restore_round_trips_byte_identically_and_touches_only_planned():
    """TC-623: apply_plan mutates exactly the planned tasks; restore brings the
    board back byte-identically (the undo's promise)."""
    b = _b()
    before = _dump(b)
    dates0 = {t.id: (t.start_date, t.due_date) for t in b.tasks}
    p = plan_move(b, "tm2", 3, 3, "push_delta", KT)
    snap = snapshot(b, p)
    apply_plan(b, p)
    changed = {t.id for t in b.tasks if (t.start_date, t.due_date) != dates0[t.id]}
    assert changed <= set(p.moved), changed
    restore(b, snap)
    assert _dump(b) == before


# --------------------------------------------------------------------------- #
# TC-624 — the ONE measure: the engine's overlap IS link_overlap's (D-633)
# --------------------------------------------------------------------------- #
def test_TC_624_the_engines_overlap_equals_link_overlap_on_every_arm():
    """TC-624 (D-633): the shipped measure, both arms plus the absent-date cases —
    the engine pushes exactly what the screen flags. A milestone's start IS its
    due, so it takes the start arm: 1d when dues coincide."""
    b = _b()
    assert link_overlap(b.task_by_id("tm3"), b.task_by_id("tm2")) == 2   # dated start arm
    assert link_overlap(b.task_by_id("td0"), b.task_by_id("td4")) == 1   # milestone: start arm
    undated = Task("no dates", id="u1")
    assert link_overlap(undated, b.task_by_id("tm2")) == 0               # no dates: 0
    nodue_pred = Task("x", id="u2")
    assert link_overlap(b.task_by_id("tm3"), nodue_pred) == 0            # pred undated: 0
    only_due = Task("y", due_date=_d(1).isoformat(), id="u3")
    assert link_overlap(only_due, b.task_by_id("tm2")) == 1              # no-start arm: dues
    p = plan_move(b, "tm2", 1, 1, "push_delta", KT)                      # engine agrees: +1, not +2
    assert p.shift.get("tm3") == 1


# --------------------------------------------------------------------------- #
# TC-625/626 — bump/bar equivalence; lenient setting read
# --------------------------------------------------------------------------- #
def test_TC_625_a_due_only_bump_and_a_whole_bar_move_land_the_same_followers():
    """TC-625: under push_delta and together, a due-only bump (+4) and a whole-bar
    move (+4) of tm3 move the same followers by the same days."""
    for mode in ("push_delta", "together"):
        bump = plan_move(_b(), "tm3", 0, 4, mode, KT)
        bar = plan_move(_b(), "tm3", 4, 4, mode, KT)
        assert set(bump.moved) == set(bar.moved), mode
        for tid in set(bump.moved) - {"tm3"}:
            assert bump.shift[tid] == bar.shift[tid], (mode, tid)


def test_TC_626_a_junk_date_links_reads_as_the_default_and_never_raises():
    """TC-626 (the lenient model): extra['date_links'] = 5 / 'junk' / [] all read
    as push_delta — the value arrives from a file."""
    for junk in (5, "junk", [], None):
        b = _b()
        b.project_by_id("pmob").extra["date_links"] = junk
        assert resolve_mode(b, "tm2") == "push_delta", junk


# --------------------------------------------------------------------------- #
# TC-627/628 — the undated base; the slack-boundary milestone
# --------------------------------------------------------------------------- #
def test_TC_627_an_undated_moved_task_bases_on_today_and_cascades_from_there():
    """TC-627: an undated task bumped +1 reads as today+1 (the bump's own rule) and
    the cascade computes on the resulting dates — a waiter starting today is
    pushed, one starting tomorrow is not."""
    b = _b()
    undated = Task("Undated chore", phase="Next", id="u1")
    w1 = Task("Starts today", phase="Next", start_date=KT.isoformat(),
              due_date=_d(5).isoformat(), depends_on=["u1"], id="w1")
    w2 = Task("Starts later", phase="Next", start_date=_d(2).isoformat(),
              due_date=_d(9).isoformat(), depends_on=["u1"], id="w2")
    b.tasks += [undated, w1, w2]
    p = plan_move(b, "u1", 0, 1, "push_delta", KT)
    assert p.moved["u1"] == (None, _d(1))
    assert p.shift.get("w1") == 2 and "w2" not in p.moved


def test_TC_628_the_slack_boundary_milestone_moves_one_day_sooner_the_shipped_measure():
    """TC-628 (D-633): a milestone waiter with exactly 1 day of slack, its
    predecessor +1 — the shipped measure moves the milestone +1 (RED against the
    prototype's carve-out, which moves nothing): the engine clears the overlap
    the screen would paint."""
    b = _b()
    pred = Task("Predecessor", phase="Next", start_date=_d(1).isoformat(),
                due_date=_d(5).isoformat(), id="p1")
    ms = Task("Sign-off", phase="Next", start_date=_d(6).isoformat(),
              due_date=_d(6).isoformat(), depends_on=["p1"], milestone=True, id="m1")
    b.tasks += [pred, ms]
    p = plan_move(b, "p1", 1, 1, "push_delta", KT)
    assert p.shift.get("m1") == 1 and p.moved["m1"] == (_d(7), _d(7))


def test_TC_629_a_move_that_creates_a_first_overlap_reports_it_never_crash():
    """TC-629 (code review C-1): when a move creates an overlap pair that never
    existed (flag on a first overlap; together pulled back onto a static open
    predecessor), the plan reports the ADDED days — no KeyError on the absent
    before-pair."""
    b = _b()
    p1 = Task("Predecessor", phase="Next", start_date=_d(1).isoformat(),
              due_date=_d(3).isoformat(), id="p1")
    p2 = Task("Static open", phase="Next", start_date=_d(1).isoformat(),
              due_date=_d(5).isoformat(), id="p2")
    w1 = Task("Waiter", phase="Next", start_date=_d(4).isoformat(),
              due_date=_d(9).isoformat(), depends_on=["p1"], id="w1")   # overlap 0 today
    b.tasks += [p1, p2, w1]
    f = plan_move(b, "p1", 0, 2, "flag", KT)
    assert f.new_conflicts == [("w1", "p1", 2)]
    assert ("w1", "p1", 2) in f.conflicts            # totals cover the whole board
    w1.depends_on = ["p1", "p2"]
    w1.start_date = _d(6).isoformat()                # 1d clear of p2's due today
    t = plan_move(b, "p1", 0, -2, "together", KT)    # w1 shifts with p1 onto p2
    assert t.new_conflicts == [("w1", "p2", 2)]


def test_TC_630_a_planned_task_vanished_between_apply_and_restore_never_raises():
    """TC-630 (code review C-2): the user deletes a moved task before `u`; the
    restore skips the vanished ids — never an AttributeError."""
    b = _b()
    p = plan_move(b, "tm2", 3, 3, "push_delta", KT)
    snap = snapshot(b, p)
    apply_plan(b, p)
    b.tasks = [t for t in b.tasks if t.id != "tm4"]
    restore(b, snap)                                # tm4 is gone: skipped, no raise
    assert b.task_by_id("tm3").due_date == _d(12).isoformat()
