"""Milestones as a task flag (batch 2026-10-04-batch-02, US-601, HLR-601).

Field report: the operator types milestones as one-day tasks (start == due) because the
board has no other way to say "this is a date, not work" (prototype round 5). The verdict
("M-1 y M-2") made it a flag on Task: one date, its due, no duration.

Law: `M` and the editor's box set and clear the flag; setting it makes the start equal the
due (or the due equal the start when only a start exists); a task with no date is refused
and nothing is written; `+`/`-` move a milestone whole; `u` undoes each step; only the
boolean true is read from a file or a teammate; search, archive and links keep the flag.
Every board here is synthetic (`tests/kg_board.py`) in `tmp_path`.

RED on base: `Task` has no `milestone` field, `set_milestone` does not exist and `M` is
unbound (P-1, P-2).
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import pytest
from textual.widgets import Checkbox, Input

import kg_board
from taskboard import keymap
from taskboard.app import TaskboardApp
from taskboard.models import (MILESTONE_NEEDS_DATE, Board, Project, Task, bump_due,
                              set_milestone)
from taskboard.modals import TaskDetails, TaskModal
from taskboard.team_sync import TEAM_FILENAME, TeamState
from taskboard.views import filtered_board

RENUMBER = "seen_view_renumber_2026_07"
T = date.today()


def _iso(n: int) -> str:
    return (T + timedelta(days=n)).isoformat()


def _toasts(app) -> list[str]:
    return [str(t.render()) for t in app.screen.query("Toast")]


def _saved(path: Path, tid: str) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return next(t for t in data["tasks"] if t["id"] == tid)


def _board(tmp_path: Path) -> Path:
    b = kg_board.shifted(tmp_path / "board.json")
    b.settings[RENUMBER] = True
    b.save()
    return b.path


async def _select(app, pilot, tid: str) -> None:
    """Walk the view with the real arrow key until `tid` is the selection."""
    for _ in range(80):
        if app.selected_task_id == tid:
            return
        await pilot.press("down")
        await pilot.pause()
    raise AssertionError(f"{tid} never selected by ↓")


# --------------------------------------------------------------------------- #
# TC-601 — the flag is read only as the boolean true (LLR-601.1)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("stored, flag", [(True, True), ("true", False), (1, False),
                                          ("yes", False), ([], False), (None, False),
                                          ("absent", False)])
def test_TC_601_only_the_boolean_true_is_a_milestone(stored, flag):
    """TC-601: a hand-edited or synced value that merely LOOKS true is not a
    milestone — the flag changes what every view draws, so it is read like the
    other synced flags. RED: `bool(value)` (the "yes" and 1 arms)."""
    d = {"id": "a", "title": "x", "due_date": "2026-10-10"}
    if stored != "absent":
        d["milestone"] = stored
    t = Task.from_dict(d)
    assert t.milestone is flag
    assert "milestone" not in t.extra          # a modelled field, never an unknown key


def test_TC_601_the_flag_round_trips_and_load_never_rewrites_dates(tmp_path):
    """TC-601: save → load keeps the flag; a stored milestone whose start differs
    from its due (an older app bumped only the due) loads with BOTH dates as stored —
    the views read its due; nothing normalises on load (D-613). RED: a load that
    re-derives the start."""
    path = tmp_path / "b.json"
    b = Board([], [Task("m", start_date="2026-10-01", due_date="2026-10-09",
                        milestone=True, id="m")], path)
    b.save()
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["tasks"][0]["milestone"] is True
    t = Board.load(path).task_by_id("m")
    assert (t.milestone, t.start_date, t.due_date) == (True, "2026-10-01", "2026-10-09")


# --------------------------------------------------------------------------- #
# TC-602 — set_milestone: one date, its due, never invented (LLR-601.1)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("start, due, on, want", [
    ("2026-10-01", "2026-10-09", True, (True, "2026-10-09", "2026-10-09", None)),
    ("2026-10-05", None, True, (True, "2026-10-05", "2026-10-05", None)),
    (None, "2026-10-09", True, (True, "2026-10-09", "2026-10-09", None)),
    ("2026-10-09", "2026-10-09", True, (True, "2026-10-09", "2026-10-09", None)),
    (None, None, True, (False, None, None, MILESTONE_NEEDS_DATE)),
    ("not a date", "", True, (False, "not a date", "", MILESTONE_NEEDS_DATE)),
    ("2026-10-09", "2026-10-09", False, (False, "2026-10-09", "2026-10-09", None)),
])
def test_TC_602_set_milestone_table(start, due, on, want):
    """TC-602 (D-605): the due is the date; with only a start the due follows it;
    with no readable date nothing changes and the reason comes back; clearing
    touches the flag only. RED: the due set from the start when both exist (row
    1), a date invented for an undated task (row 5)."""
    t = Task("x", start_date=start, due_date=due, milestone=not on and True)
    err = set_milestone(t, on)
    assert (t.milestone, t.start_date, t.due_date, err) == want


# --------------------------------------------------------------------------- #
# TC-603 — a milestone moves whole (LLR-601.1)
# --------------------------------------------------------------------------- #
def test_TC_603_bump_moves_a_milestone_whole_and_a_task_by_its_due():
    """TC-603: `+` on a milestone moves its one date (start and due); on a task it
    moves only the due, as shipped. RED: the shipped due-only bump (P-14) leaves a
    milestone with start ≠ due."""
    m = Task("m", start_date="2026-10-09", due_date="2026-10-09", milestone=True)
    w = Task("w", start_date="2026-10-01", due_date="2026-10-09")
    for t in (m, w):
        bump_due(t, 1, date(2026, 10, 4))
    assert (m.start_date, m.due_date) == ("2026-10-10", "2026-10-10")
    assert (w.start_date, w.due_date) == ("2026-10-01", "2026-10-10")


# --------------------------------------------------------------------------- #
# TC-604 — `M`, its toasts and its undo (LLR-601.2)
# --------------------------------------------------------------------------- #
async def test_TC_604_M_sets_with_one_undo_step_and_refuses_an_undated_task(tmp_path):
    """TC-604: one snapshot taken BEFORE the change, `u` restores flag and start;
    an undated task: no snapshot, no save, one warning toast; no selection:
    nothing. RED: snapshot after the change, `start_date` not in the undo fields."""
    path = _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("3")
        await pilot.pause()
        app.clear_notifications()
        await _select(app, pilot, "ta4")               # Rate limiting: start ≠ due
        task = app.board.task_by_id("ta4")
        start, due = task.start_date, task.due_date
        depth = len(app._undo_stack)
        await pilot.press("M")
        await pilot.pause()
        assert len(app._undo_stack) == depth + 1
        assert (task.milestone, task.start_date, task.due_date) == (True, due, due)
        await pilot.press("u")
        await pilot.pause()
        assert (task.milestone, task.start_date, task.due_date) == (False, start, due)
        await _select(app, pilot, "ta5")               # Plan Q4 roadmap: no date
        app.clear_notifications()
        before = path.read_bytes()
        depth = len(app._undo_stack)
        await pilot.press("M")
        await pilot.pause()
        assert len(app._undo_stack) == depth and path.read_bytes() == before
        toasts = _toasts(app)
        assert len(toasts) == 1 and "a milestone needs a date" in toasts[0]
        app.selected_task_id = None
        await pilot.press("M")                          # no selection: nothing
        await pilot.pause()
        assert path.read_bytes() == before


@pytest.mark.parametrize("view", keymap.VIEWS + ("flow", "standup", "people", "setup"))
def test_TC_604_M_is_listed_where_a_task_is_selected(view):
    """TC-604 (UX-7): `M  Milestone` is in the keys of the five task views and of
    no other; each of those bars shows `M` or counts it in `+N` (the bar's own
    contract). RED: `M` scoped nowhere or everywhere."""
    listed = [(k.show, k.label) for k in keymap.bar_keys(view, "more")]
    if view in ("swimlanes", "agenda", "gantt", "kanban", "focus"):
        assert ("M", "Milestone") in listed
        shown, dropped = keymap.fit_bar(118, view, "more")
        assert any(s == "M" for s, _ in shown) or dropped >= 1
    else:
        assert ("M", "Milestone") not in listed


@pytest.mark.parametrize("case, where", [("band", "on the Website Redesign band"),
                                         ("last-card", "shown on the gantt"),
                                         ("inbox", "shown on the gantt")])
async def test_TC_604_the_toast_says_where_the_milestone_shows(tmp_path, case, where):
    """TC-604 (UX-8, UX2-1): in the grouped kanban by project the toast says the
    milestone rides its project's band only when that band is drawn — the project
    keeps an open card that is not a milestone — else "shown on the gantt" (the
    project's last open card; an Inbox task). RED: "on the band" for every
    project task."""
    path = tmp_path / "board.json"
    web = Project("Website Redesign", "violet", id="pweb")
    tasks = [Task("Ship it", "pweb", "Doing", due_date=_iso(5), id="a"),
             Task("Other", "pweb", "Doing", due_date=_iso(6), id="b"),
             Task("Loose", None, "Doing", due_date=_iso(7), id="c")]
    if case == "last-card":
        # the other card is CLOSED, not gone (code review F-2): the rule is the
        # project's last OPEN card
        tasks[1].phase = "Done"
    b = Board([web], tasks, path, {RENUMBER: True}, ["Backlog", "Doing", "Done"])
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.clear_notifications()
        app.selected_task_id = "c" if case == "inbox" else "a"
        await pilot.press("M")
        await pilot.pause()
        toasts = _toasts(app)
        assert len(toasts) == 1 and where in toasts[0], toasts


# --------------------------------------------------------------------------- #
# TC-605 — the editor's box (LLR-601.3)
# --------------------------------------------------------------------------- #
async def _edit(app, pilot, tid, **fields):
    app.selected_task_id = tid
    await pilot.press("e")
    for _ in range(3):
        await pilot.pause()
    scr = app.screen
    assert isinstance(scr, TaskModal)
    for wid, value in fields.items():
        node = scr.query_one(f"#{wid.replace('_', '-')}")
        node.value = value
    await pilot.pause()
    scr.query_one("#save").press()
    for _ in range(3):
        await pilot.pause()


@pytest.mark.parametrize("arm", ["dated", "start-differs", "undated", "new-task",
                                 "cleared", "due-only", "tick-only"])
async def test_TC_605_the_editor_box_applies_after_the_dates(tmp_path, arm):
    """TC-605: the box is applied AFTER every other field, so a new due in the same
    save is the milestone's date; a typed start that differs is replaced by the due
    and said; ticked on an undated task the other edits are saved and the task stays
    a task, said; a new task saved ticked with a due is a milestone. RED: the flag
    applied before the edited dates (start = the old due)."""
    path = _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(120, 36), notifications=True) as pilot:
        await pilot.press("3")
        await pilot.pause()
        app.clear_notifications()
        if arm == "dated":
            await _edit(app, pilot, "ta1", f_milestone=True, f_due=_iso(9), f_start="")
            t = app.board.task_by_id("ta1")
            assert (t.milestone, t.start_date, t.due_date) == (True, _iso(9), _iso(9))
            assert not any("start follows" in x for x in _toasts(app))
        elif arm == "start-differs":
            await _edit(app, pilot, "ta1", f_milestone=True, f_start=_iso(2), f_due=_iso(9))
            t = app.board.task_by_id("ta1")
            assert (t.milestone, t.start_date, t.due_date) == (True, _iso(9), _iso(9))
            assert sum("milestone: the start follows the due" in x for x in _toasts(app)) == 1
        elif arm == "undated":
            await _edit(app, pilot, "ta5", f_milestone=True, f_title="Plan Q5 roadmap")
            t = app.board.task_by_id("ta5")
            assert (t.title, t.milestone) == ("Plan Q5 roadmap", False)
            assert sum("not a milestone — a milestone needs a date" in x
                       for x in _toasts(app)) == 1
        elif arm == "cleared":
            # an existing milestone saved with both dates cleared and the box still
            # ticked stops being one, said (code review F-1)
            ms = app.board.task_by_id("ta4")
            set_milestone(ms, True)
            app.board.save()
            await _edit(app, pilot, "ta4", f_start="", f_due="")
            t = app.board.task_by_id("ta4")
            assert (t.milestone, t.start_date, t.due_date) == (False, None, None)
            assert sum("not a milestone — a milestone needs a date" in x
                       for x in _toasts(app)) == 1
        elif arm == "due-only":
            # editing only a milestone's due: its start field still shows the old
            # date, which the user did not touch — no start toast (code review F-4)
            ms = app.board.task_by_id("ta4")
            set_milestone(ms, True)
            app.board.save()
            await _edit(app, pilot, "ta4", f_due=_iso(20))
            t = app.board.task_by_id("ta4")
            assert (t.milestone, t.start_date, t.due_date) == (True, _iso(20), _iso(20))
            assert not any("start follows" in x for x in _toasts(app))
        elif arm == "tick-only":
            # a TASK becoming a milestone with its start untouched loses that start:
            # said, as `M` says it (code review F2-1, a regression of the F-4 fold)
            await _edit(app, pilot, "ta4", f_milestone=True)
            t = app.board.task_by_id("ta4")
            assert (t.milestone, t.start_date) == (True, t.due_date)
            assert sum("milestone: the start follows the due" in x for x in _toasts(app)) == 1
        else:
            await pilot.press("a")
            for _ in range(3):
                await pilot.pause()
            scr = app.screen
            scr.query_one("#f-title", Input).value = "Go live"
            scr.query_one("#f-due", Input).value = _iso(12)
            scr.query_one("#f-milestone", Checkbox).value = True
            await pilot.pause()
            scr.query_one("#save").press()
            for _ in range(3):
                await pilot.pause()
            t = next(x for x in app.board.tasks if x.title == "Go live")
            assert (t.milestone, t.start_date, t.due_date) == (True, _iso(12), _iso(12))
        assert _saved(path, {"dated": "ta1", "start-differs": "ta1", "undated": "ta5",
                             "cleared": "ta4", "due-only": "ta4",
                             "tick-only": "ta4"}.get(arm, t.id)
                      )["milestone"] is t.milestone


async def test_TC_605_the_box_reflects_the_task_and_unticking_clears(tmp_path):
    """TC-605: the editor opens with the box as the task is; unticked and saved, the
    flag clears and the single date stays. RED: a box that always opens unticked."""
    path = tmp_path / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), T)
    b.settings[RENUMBER] = True
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(120, 36)) as pilot:
        await pilot.press("3")
        await pilot.pause()
        app.selected_task_id = "tw5"
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        box = app.screen.query_one("#f-milestone", Checkbox)
        assert box.value is True
        box.value = False
        await pilot.pause()
        app.screen.query_one("#save").press()
        for _ in range(3):
            await pilot.pause()
        t = app.board.task_by_id("tw5")
        assert (t.milestone, t.start_date) == (False, t.due_date)


# --------------------------------------------------------------------------- #
# TC-606 — the details view says it (LLR-601.3)
# --------------------------------------------------------------------------- #
async def test_TC_606_details_phase_row_names_the_milestone(tmp_path):
    """TC-606: the phase row ends ` · ◆ milestone` for a milestone and not for a
    task. RED: no mark (base)."""
    path = tmp_path / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), T)
    b.settings[RENUMBER] = True
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        for tid, want in (("tw5", True), ("tw3", False)):
            await pilot.press("3")
            await pilot.pause()
            app.selected_task_id = tid
            await pilot.press("enter")
            for _ in range(3):
                await pilot.pause()
            assert isinstance(app.screen, TaskDetails)
            phase_row = [str(lbl.render()) for lbl in app.screen.query("Label")][4]
            assert phase_row.endswith(" · ◆ milestone") is want, phase_row
            await pilot.press("escape")
            await pilot.pause()


# --------------------------------------------------------------------------- #
# TC-607 — team sync carries the flag, validated (LLR-601.1)
# --------------------------------------------------------------------------- #
def test_TC_607_push_writes_the_flag_and_pull_reads_only_true(tmp_path):
    """TC-607: a pushed record carries `"milestone": true`; a teammate's `true` is
    pulled as a milestone and their `"yes"` is not. RED: a push dropping the field,
    `bool()` on pull."""
    team = tmp_path / "team"
    team.mkdir()
    (team / TEAM_FILENAME).write_text(json.dumps(kg_board.TEAM), encoding="utf-8")
    b = Board([Project("Website Redesign", "violet", id="pweb")],
              [Task("Launch", "pweb", due_date="2026-10-10", start_date="2026-10-10",
                    milestone=True, id="m1")], tmp_path / "b.json")
    me = TeamState(team, user_id="jav")
    me.load_config()
    assert me.push(b)
    pushed = json.loads((team / "board.jav.json").read_text(encoding="utf-8"))
    assert pushed["tasks"][0]["milestone"] is True
    (team / "board.ana.json").write_text(json.dumps({"user": "ana", "tasks": [
        {"id": "x1", "title": "real", "project_id": "pweb", "milestone": True},
        {"id": "x2", "title": "fake", "project_id": "pweb", "milestone": "yes"}]}),
        encoding="utf-8")
    me.pull()
    got = {t.id: t.milestone for t, _uid in me.foreign_tasks()}
    assert got == {"x1": True, "x2": False}


# --------------------------------------------------------------------------- #
# TC-608 — search, archive and links keep the flag (LLR-601.1)
# --------------------------------------------------------------------------- #
async def test_TC_608_archive_search_and_links_keep_the_flag(tmp_path):
    """TC-608: the flag is a field like any other — archive and unarchive (`x`) and
    a link added to it leave it as it was; the `/` filter finds a milestone by its
    title. RED: a path that rebuilds the task without the field."""
    path = tmp_path / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), T)
    b.settings[RENUMBER] = True
    b.task_by_id("tw5").depends_on = []          # nothing waits-on blocks the archive
    b.save()
    assert "tw5" in {t.id for t in filtered_board(b, "launch", False).tasks}
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("1")
        await pilot.pause()
        app.selected_task_id = "tm5"             # nothing open waits on it
        t = app.board.task_by_id("tm5")
        await pilot.press("x")                   # archive …
        await pilot.pause()
        assert (t.archived, t.milestone) == (True, True)     # code review F-3
        app.selected_task_id = "tm5"
        await pilot.press("x")                   # … and bring it back
        await pilot.pause()
        assert (t.archived, t.milestone) == (False, True)
        t.depends_on.append("tm4")               # a link, as `L` writes it
        app.board.save()
    assert Board.load(path).task_by_id("tm5").milestone is True


# --------------------------------------------------------------------------- #
# AT-601 — a task becomes a milestone, through the shipped surface (HLR-601)
# --------------------------------------------------------------------------- #
async def test_AT_601_a_task_becomes_a_milestone_saved_undoable_said_and_pushed(tmp_path):
    """AT-601 (US-601): in the gantt, `M` on `Rate limiting` (start ≠ due) writes
    `"milestone": true` with start = due and says so; `M` again clears it; `M` on the
    undated `Plan Q4 roadmap` is refused and the file is byte-identical; `+` on the
    milestone moves both dates and `u` puts them back; the editor's box with a new due
    makes that due the date; in team mode the pushed `board.<user>.json` carries the
    flag. RED on base: `M` is unbound — nothing changes."""
    path = _board(tmp_path)
    team = tmp_path / "team"
    team.mkdir()
    cfg = dict(kg_board.TEAM, projects=[{"id": "papi", "name": "API Platform",
                                         "color": "lime", "status": "at_risk"}])
    (team / TEAM_FILENAME).write_text(json.dumps(cfg), encoding="utf-8")
    b = Board.load(path)
    b.settings.update({"team_shared_dir": str(team), "team_user_id": "jav"})
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=0.2)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("3")
        await pilot.pause()
        app.clear_notifications()
        await _select(app, pilot, "ta4")
        due = _saved(path, "ta4")["due_date"]
        await pilot.press("M")
        await pilot.pause()
        rec = _saved(path, "ta4")
        assert (rec["milestone"], rec["start_date"], rec["due_date"]) == (True, due, due)
        said = _toasts(app)
        assert len(said) == 1 and "Rate limiting is a milestone · ◆ " in said[0]
        assert "start was" in said[0]
        pushed = team / "board.jav.json"            # the team arm: polled ≤ 5 s
        for _ in range(50):
            await pilot.pause(0.1)
            if pushed.exists() and any(
                    t["id"] == "ta4" and t.get("milestone") is True for t in
                    json.loads(pushed.read_text(encoding="utf-8"))["tasks"]):
                break
        else:
            raise AssertionError("the pushed file never carried the milestone")
        app.clear_notifications()
        await pilot.press("M")
        await pilot.pause()
        rec = _saved(path, "ta4")
        assert (rec["milestone"], rec["start_date"], rec["due_date"]) == (False, due, due)
        assert any("Rate limiting is a task again" in x for x in _toasts(app))
        await pilot.press("M")
        await pilot.pause()
        await pilot.press("plus")
        await pilot.pause()
        nxt = (date.fromisoformat(due) + timedelta(days=1)).isoformat()
        rec = _saved(path, "ta4")
        assert (rec["start_date"], rec["due_date"], rec["milestone"]) == (nxt, nxt, True)
        await pilot.press("u")
        await pilot.pause()
        rec = _saved(path, "ta4")
        assert (rec["start_date"], rec["due_date"]) == (due, due)
        await _select(app, pilot, "ta5")
        app.clear_notifications()
        before = path.read_bytes()
        await pilot.press("M")
        await pilot.pause()
        assert path.read_bytes() == before
        said = _toasts(app)
        assert len(said) == 1 and "a milestone needs a date" in said[0]
        await _edit(app, pilot, "ta1", f_milestone=True, f_due=_iso(9))
        rec = _saved(path, "ta1")
        assert (rec["milestone"], rec["start_date"], rec["due_date"]) == (True, _iso(9), _iso(9))
