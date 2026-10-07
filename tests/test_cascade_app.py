"""The date move routes through the cascade (batch 2026-10-06-batch-01, US-604,
LLR-604.2/.4): the `+`/`-` bump plans and applies the chain's move with the C-3
toast and ONE undo entry; `m` re-applies the last move under the next mode.

The ATs drive `TaskboardApp` with real keys (C-16) over a board file in `tmp_path`
— the shifted kg milestones board, every number executed in
`evidence/p1-thresholds.txt`. RED on base: the bump moves only the due date, no
toast, no `m`.
"""
from __future__ import annotations

import json
from datetime import date, timedelta

from textual.widgets import Button, Checkbox, Input, OptionList, Select

import kg_board
from taskboard.app import TaskboardApp

RENUMBER = "seen_view_renumber_2026_07"


def _board(tmp_path):
    path = tmp_path / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    b.save()
    return path, b


def _toasts(app):
    return [str(t.render()) for t in app.screen.query("Toast")]


def _due(b, tid):
    return b.task_by_id(tid).due_date


# --------------------------------------------------------------------------- #
# AT-607 — the bump moves the chain and says who moved; one `u` takes it back
# --------------------------------------------------------------------------- #
async def test_AT_607_the_bump_moves_the_chain_and_says_so(tmp_path):
    """AT-607 (US-604): `+` on tm2 moves tm3 AND tm4 +1d (tm5's slack absorbs),
    the toast at 118 names them (`pushed Add push, Offline sync +1d each`), at 80
    it counts (`pushed 2 +1d each`), and ONE `u` restores all three dates."""
    path, b0 = _board(tmp_path)
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    due0 = {tid: _due(b0, tid) for tid in ("tm2", "tm3", "tm4", "tm5")}
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        b = app.board
        assert _due(b, "tm2") == iso(3) and _due(b, "tm3") == iso(13)
        assert _due(b, "tm4") == iso(29) and _due(b, "tm5") == due0["tm5"]
        said = "\n".join(_toasts(app))
        assert "pushed Add push, Offline sync +1d each" in said, said
        assert "m change for this move" in said, said
        await pilot.press("u")
        await pilot.pause()
        assert {tid: _due(app.board, tid) for tid in ("tm2", "tm3", "tm4")} == \
               {tid: due0[tid] for tid in ("tm2", "tm3", "tm4")}, "one u restores all three"
    app2 = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app2.run_test(size=(80, 24), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app2.selected_task_id = "tm2"
        app2.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        said = "\n".join(_toasts(app2))
        assert "pushed 2 +1d each" in said, said
        assert "Offline sync" not in said, said          # names do not fit at 80


# --------------------------------------------------------------------------- #
# AT-608 — `m` re-applies the last move under the next mode; the refusal
# --------------------------------------------------------------------------- #
async def test_AT_608_m_reapplies_the_last_move_under_the_next_mode(tmp_path):
    """AT-608 (US-604): after `+` on tm2 (push_delta: tm3/tm4 +1d), `m` re-applies
    under together — tm3, tm4 AND the milestone tm5 +1d, the toast holding `moved`
    and `Mobile +1d past ◆`; `m` again re-applies under flag — tm3/tm4/tm5 back,
    tm2 +1d alone, the toast holding `flagged Add push +1d`; `m` with no move on
    top toasts the refusal and writes nothing."""
    path, b0 = _board(tmp_path)
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    due0 = {tid: _due(b0, tid) for tid in ("tm2", "tm3", "tm4", "tm5")}
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        await pilot.press("m")                            # push_delta -> together
        await pilot.pause()
        b = app.board
        assert _due(b, "tm3") == iso(13) and _due(b, "tm4") == iso(29)
        t5 = b.task_by_id("tm5")
        assert t5.start_date == t5.due_date == iso(36), "the milestone moves whole"
        said = "\n".join(_toasts(app))
        assert "moved" in said and "Mobile +1d past ◆" in said, said
        await pilot.press("m")                            # together -> flag
        await pilot.pause()
        b = app.board
        assert _due(b, "tm3") == due0["tm3"] and _due(b, "tm4") == due0["tm4"]
        t5 = b.task_by_id("tm5")
        assert (t5.start_date, t5.due_date) == (due0["tm5"], due0["tm5"])
        assert _due(b, "tm2") == iso(3), "tm2 keeps its move under flag"
        said = "\n".join(_toasts(app))
        assert "flagged Add push +1d" in said, said
        # the refusal: a fresh board, nothing moved yet
    app2 = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app2.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        before = {tid: _due(app2.board, tid) for tid in ("tm2", "tm3", "tm4", "tm5")}
        await pilot.press("m")
        await pilot.pause()
        said = "\n".join(_toasts(app2))
        assert "m re-applies the last date move — nothing to re-apply" in said, said
        assert {tid: _due(app2.board, tid) for tid in before} == before, "m wrote nothing"


async def test_TC_631_an_undated_dependent_under_together_toasts_never_crashes(tmp_path):
    """TC-631 (code review 1-1): a moved task with an UNDATED dependent under
    `together` — the planned due is None and the toast's dependents sort must
    tolerate it; the toast names the count, no TypeError, the move persists."""
    from taskboard.models import Task as _Task
    path, _b = _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        undated = _Task("Undated follower", phase="Next", depends_on=["tm2"], id="u9")
        dated = _Task("Dated follower", phase="Next", start_date=(
            date.today() + timedelta(days=20)).isoformat(),
            due_date=(date.today() + timedelta(days=24)).isoformat(),
            depends_on=["tm2"], id="u8")
        app.board.tasks += [undated, dated]
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("m")            # nothing moved yet: refusal, not a crash
        await pilot.pause()
        await pilot.press("+")            # push_delta: dated follower moves
        await pilot.pause()
        await pilot.press("m")            # together: the undated one joins
        await pilot.pause()
        said = "\n".join(_toasts(app))
        assert "moved" in said, said
        assert app.board.task_by_id("u9") is not None    # the board is intact


# --------------------------------------------------------------------------- #
# AT-609 — the editor's date save routes through the cascade
# --------------------------------------------------------------------------- #
async def test_AT_609_the_editor_date_save_routes_through_the_cascade(tmp_path):
    """AT-609 (US-604): `e` on tm2, change ONLY the due to today+5 (tm2's due is
    today+2; +3 like the executed probe), save — tm2 due today+5, tm3 due
    today+15 AND tm4 due today+31 (both +3d); the toast holds `pushed`; ONE `u`
    restores tm2/tm3/tm4. Second arm: a title-only save writes no undo entry and
    no toast."""
    path, b0 = _board(tmp_path)
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    due0 = {tid: _due(b0, tid) for tid in ("tm2", "tm3", "tm4")}
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        scr.query_one("#f-due", Input).value = iso(5)
        await pilot.pause()
        scr.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        b = app.board
        assert _due(b, "tm2") == iso(5)
        assert _due(b, "tm3") == iso(15)
        assert _due(b, "tm4") == iso(31)
        said = "\n".join(_toasts(app))
        assert "pushed" in said, said
        await pilot.press("u")
        await pilot.pause()
        assert {tid: _due(app.board, tid) for tid in ("tm2", "tm3", "tm4")} == \
               {tid: due0[tid] for tid in ("tm2", "tm3", "tm4")}, "one u restores all three"
        # second arm: a save touching only the title writes nothing to undo/toast
        app.clear_notifications()
        stack_before = len(app._undo_stack)
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        scr.query_one("#f-title", Input).value = "Audit dependencies (renamed)"
        await pilot.pause()
        scr.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        assert app.board.task_by_id("tm2").title == "Audit dependencies (renamed)"
        assert len(app._undo_stack) == stack_before, "a title-only save records no undo"
        assert _toasts(app) == [], _toasts(app)


# --------------------------------------------------------------------------- #
# AT-610 — the per-project `Linked dates` setting decides the editor cascade
# --------------------------------------------------------------------------- #
async def test_AT_610_the_project_date_links_setting_decides_the_cascade(tmp_path):
    """AT-610 (US-604): set Data Warehouse to `together` (P -> e -> f-date-links),
    edit td4 start AND due +2d in the TASK editor — the milestone td0 (start==due,
    today+20) and td5 (today+32) move +2d, the toast holds `moved` and
    `Data +2d past ◆`; set `flag`, the same edit moves nothing else, the toast
    holds `flagged Revenue +2d`. Third arm: a board hand-edited to
    `"date_links": 5` loads, behaves as push_delta on a bump, and the junk value
    survives a save untouched."""
    path, b0 = _board(tmp_path)
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    idx = b0.projects.index(b0.project_by_id("pdwh"))
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        # set the rule to `together` through the real project editor (P -> e);
        # the Select is driven on the mounted widget, saved via its own path
        await pilot.press("P")
        await pilot.pause()
        app.screen.query_one("#proj-list", OptionList).highlighted = idx
        await pilot.press("e")
        await pilot.pause()
        app.screen.query_one("#f-date-links", Select).value = "together"
        app.screen.query_one("#save", Button).press()
        await pilot.pause()
        assert app.board.project_by_id("pdwh").extra["date_links"] == "together"
        await pilot.press("escape")
        await pilot.pause()
        # edit td4 in the TASK editor: start AND due +2d
        app.selected_task_id = "td4"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        scr.query_one("#f-start", Input).value = iso(-1)    # -3 + 2
        scr.query_one("#f-due", Input).value = iso(20)      # +18 + 2
        await pilot.pause()
        scr.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        b = app.board
        t0 = b.task_by_id("td0")
        assert (t0.start_date, t0.due_date) == (iso(20), iso(20)), "the milestone moves whole"
        assert b.task_by_id("td5").start_date == iso(32)
        said = "\n".join(_toasts(app))
        assert "moved" in said and "Data +2d past ◆" in said, said
        # set the rule to `flag`, repeat the same edit: nothing else moves
        app.clear_notifications()
        await pilot.press("P")
        await pilot.pause()
        app.screen.query_one("#proj-list", OptionList).highlighted = idx
        await pilot.press("e")
        await pilot.pause()
        app.screen.query_one("#f-date-links", Select).value = "flag"
        app.screen.query_one("#save", Button).press()
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        app.selected_task_id = "td4"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        scr.query_one("#f-start", Input).value = iso(1)     # -1 + 2
        scr.query_one("#f-due", Input).value = iso(22)      # +20 + 2
        await pilot.pause()
        scr.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        b = app.board
        t0 = b.task_by_id("td0")
        assert (t0.start_date, t0.due_date) == (iso(20), iso(20)), "flag moves nothing else"
        assert b.task_by_id("td5").start_date == iso(32)
        said = "\n".join(_toasts(app))
        assert "flagged Revenue +2d" in said, said
    # third arm: a hand-edited junk `date_links` reads as push_delta, never repaired
    path3 = tmp_path / "board3.json"
    b3 = kg_board.milestones(kg_board.shifted(path3), date.today())
    b3.settings[RENUMBER] = True
    b3.save()
    raw = json.loads(path3.read_text(encoding="utf-8"))
    for p in raw["projects"]:
        if p["id"] == "pdwh":
            p["date_links"] = 5
    path3.write_text(json.dumps(raw), encoding="utf-8")
    app3 = TaskboardApp(board_path=str(path3), team_sync_interval=1e9)
    async with app3.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app3.selected_task_id = "td4"
        app3.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        assert _due(app3.board, "td4") == iso(19)
        assert _due(app3.board, "td0") == iso(19), "push_delta pushes the milestone"
        assert _due(app3.board, "td5") == iso(60), "together would have moved it"
        assert app3.board.project_by_id("pdwh").extra["date_links"] == 5
        saved = json.loads(path3.read_text(encoding="utf-8"))
        dwh = next(p for p in saved["projects"] if p["id"] == "pdwh")
        assert dwh["date_links"] == 5, "the junk value survives a save untouched"


# --------------------------------------------------------------------------- #
# AT-611 — chain honesty through the real keys (the contract's fifth AT)
# --------------------------------------------------------------------------- #
async def test_AT_611_chain_honesty_through_the_app(tmp_path):
    """AT-611 (US-604): a done dependent stops the chain; a milestone moves whole;
    an earlier move pulls nothing; a cross-project link follows the MOVED task's
    project rule."""
    path, b0 = _board(tmp_path)
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    due0 = {tid: _due(b0, tid) for tid in ("tm2", "tm3", "tm4", "ta4", "td2", "td0", "td5")}

    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        # a done dependent stops the chain: tm3 Done, + on tm2 moves tm2 alone
        app.board.task_by_id("tm3").phase = app.board.phases[-1]
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        assert _due(app.board, "tm2") == iso(3)
        assert _due(app.board, "tm4") == due0["tm4"], "the chain stops at the done task"
        await pilot.press("u")
        await pilot.pause()
        # an earlier move pulls nothing under push_delta
        app.board.task_by_id("tm3").phase = "Next"
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("-")
        await pilot.pause()
        assert _due(app.board, "tm3") == due0["tm3"], "earlier pulls nothing"
        await pilot.press("u")
        await pilot.pause()
        # the cross-project arm: td2 waits on ta4; the MOVED task's project decides
        app.board.task_by_id("td2").depends_on = ["ta4"]
        app.board.project_by_id("papi").extra["date_links"] = "together"
        app.selected_task_id = "ta4"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        assert _due(app.board, "td2") == (today + timedelta(days=10)).isoformat(), \
            "api's together moves the dwh waiter"
        await pilot.press("u")
        await pilot.pause()
    # a milestone moves whole: td0 in the gantt (+ ignores any start, start == due)
    app2 = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app2.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("3")
        await pilot.pause()
        app2.selected_task_id = "td0"
        app2.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        t0 = app2.board.task_by_id("td0")
        assert t0.start_date == t0.due_date == iso(19), "the milestone moves whole"
        assert _due(app2.board, "td5") == due0["td5"], "slack absorbs its waiter"


# --------------------------------------------------------------------------- #
# TC-632 — the reporting layer's hostile inputs (DeepSeek review DS-1/DS-2)
# --------------------------------------------------------------------------- #
async def test_TC_632_the_toast_survives_an_empty_title_and_the_editor_stays_silent(tmp_path):
    """TC-632: an empty task title does not kill the bump toast (DS-1: _short_title
    used to raise IndexError while the move persisted); a solo editor date change
    that moves nobody stays SILENT (LLR-604.3/D-629, code review J — the toast
    seat's start-arm for a None planned due remains as defense-in-depth)."""
    from taskboard.models import Task as _Task
    path, _b = _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    iso = lambda off: (date.today() + timedelta(days=off)).isoformat()
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.board.tasks.append(_Task("", phase="Next", project_id="pmob",
                                     start_date=date.today().isoformat(),
                                     due_date=(date.today() + timedelta(days=8)).isoformat(),
                                     id="tx"))
        app.selected_task_id = "tx"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        assert app.board.task_by_id("tx").due_date == (date.today() + timedelta(days=9)).isoformat()
        said = "\n".join(_toasts(app))
        assert "due" in said, said                     # the toast lived
        # DS-1 live path: an EMPTY-TITLED DEPENDENT named by the cascade clause
        app.clear_notifications()
        app.board.tasks.append(_Task("", phase="Next", project_id="pmob",
                                     start_date=iso(1), due_date=iso(3),
                                     depends_on=["tm2"], id="ty"))
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        assert _due(app.board, "ty") == iso(4), "the empty-titled waiter moved"
        said = "\n".join(_toasts(app))
        assert "pushed" in said, said                  # naming it did not kill the toast
        await pilot.press("u")
        await pilot.pause()
        # DS-2: a start move on a task with NO due — the planned due is None and
        # the toast's lead must survive it (an in-test task: start, no due)
        app.clear_notifications()
        app.board.tasks.append(_Task("Start only", phase="Next", project_id="pweb",
                                     start_date=iso(1), id="t7"))
        app.selected_task_id = "t7"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        scr.query_one("#f-start", Input).value = iso(4)   # +3 on the start
        await pilot.pause()
        scr.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        t7 = app.board.task_by_id("t7")
        assert t7.start_date == iso(4)
        assert t7.due_date is None
        assert _toasts(app) == [], _toasts(app)   # LLR-604.3/D-629: nobody moved -> silent


async def test_TC_633_undo_restores_a_freshly_dated_field_to_untouched(tmp_path):
    """TC-633 (increment 003's own report flag): when one date field gains its
    FIRST date (None -> date, delta 0 — the cascade does not move it) while the
    other field moves, `u` must still restore the untouched field to None."""
    from taskboard.models import Task as _Task
    path, _b = _board(tmp_path)
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.board.tasks.append(_Task("Waiting item", phase="Next", project_id="pweb",
                                     start_date=iso(8), due_date=iso(12),
                                     depends_on=["tw4"], id="w9"))
        app.selected_task_id = "tw4"                   # no start, due today+6
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        scr.query_one("#f-start", Input).value = iso(4)   # its FIRST start date
        scr.query_one("#f-due", Input).value = iso(9)     # grows the overlap 0d -> 2d
        await pilot.pause()
        scr.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        b = app.board
        assert b.task_by_id("tw4").start_date == iso(4)
        assert b.task_by_id("w9").start_date == iso(10), "the added overlap pushed the waiter"
        await pilot.press("u")
        await pilot.pause()
        b = app.board
        assert b.task_by_id("tw4").start_date is None, "u takes the first date back"
        assert _due(b, "tw4") == iso(6), "and the moved due"
        assert b.task_by_id("w9").start_date == iso(8), "and its pushed waiter"


async def test_TC_634_the_milestone_box_and_a_start_edit_in_one_save(tmp_path):
    """TC-634 (code review K): ticking the milestone box while editing the START
    of a task that has no due must not lose the edit nor ship a milestone with
    start != due: set_milestone canonicalizes (start == the typed date), the
    zero-due-delta cascade is skipped, and the normal save persists it."""
    from taskboard.models import Task as _Task
    path, _b = _board(tmp_path)
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.board.tasks.append(_Task("Start only", phase="Next", project_id="pweb",
                                     start_date=iso(1), id="t7"))
        app.selected_task_id = "t7"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        scr.query_one("#f-start", Input).value = iso(4)
        scr.query_one("#f-milestone", Checkbox).value = True
        await pilot.pause()
        scr.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        t7 = app.board.task_by_id("t7")
        assert t7.milestone is True
        assert t7.start_date == t7.due_date == iso(4), \
            "the box canonicalizes to the typed date; the edit survives"
        assert _toasts(app) == [], _toasts(app)   # no date MOVED: the editor stays silent


async def test_TC_635_a_milestone_due_edit_that_moves_nobody_stays_silent(tmp_path):
    """TC-635 (code review J, residual): an editor due edit on a milestone whose
    cascade moves nobody (slack absorbs its waiter) still applies and pushes its
    undo entry — but toasts nothing: the editor's silence clause (D-629) covers
    the milestone path too."""
    path, b0 = _board(tmp_path)
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("3")                     # the gantt selects milestones
        await pilot.pause()
        app.selected_task_id = "td0"               # due today+18; td5 slack absorbs
        app.refresh_view()
        stack_before = len(app._undo_stack)
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        scr.query_one("#f-due", Input).value = iso(19)
        await pilot.pause()
        scr.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        t0 = app.board.task_by_id("td0")
        assert t0.start_date == t0.due_date == iso(19), "the whole move applied"
        assert _due(app.board, "td5") == iso(60), "slack absorbed the waiter"
        assert _toasts(app) == [], _toasts(app)     # D-629: nobody moved -> silent
        assert len(app._undo_stack) == stack_before + 1, "the undo entry is there"
        await pilot.press("u")
        await pilot.pause()
        t0 = app.board.task_by_id("td0")
        assert t0.start_date == t0.due_date == iso(18), "one u takes it back"


# --------------------------------------------------------------------------- #
# P4 pins — the validation gate's coverage folds (QA4-1, ARCH4-5/6, SEC4-4)
# --------------------------------------------------------------------------- #
async def test_TC_636_a_multi_task_move_saves_atomically_apply_and_undo(tmp_path):
    """TC-636 (P4 QA4-1/SEC4-2): D-634 promises save_atomic on the apply AND on
    the undo's restore; a spy on Board.save_atomic pins both writers."""
    from unittest.mock import patch
    path, b0 = _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        with patch.object(app.board, "save_atomic", wraps=app.board.save_atomic) as spy:
            await pilot.press("+")
            await pilot.pause()
            assert spy.call_count == 1, "the apply of a 3-task move is atomic"
            assert _due(app.board, "tm3") != _due(b0, "tm3")
            await pilot.press("u")
            await pilot.pause()
        assert spy.call_count == 2, f"apply + restore, got {spy.call_count}"
        assert {tid: _due(app.board, tid) for tid in ("tm2", "tm3", "tm4")} == \
               {tid: _due(b0, tid) for tid in ("tm2", "tm3", "tm4")}, "undo restored"


async def test_TC_637_m_works_after_an_editor_save_and_refuses_after_an_action(tmp_path):
    """TC-637 (P4 ARCH4-5/6): `m` re-applies an EDITOR save's move under the next
    mode (LLR-604.4 names both surfaces); after an intervening non-cascade
    action the refusal is verbatim and writes nothing."""
    path, b0 = _board(tmp_path)
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    due0 = {tid: _due(b0, tid) for tid in ("tm2", "tm3", "tm4", "tm5")}
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        scr.query_one("#f-due", Input).value = iso(5)
        await pilot.pause()
        scr.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        await pilot.press("m")                       # the editor's move, together
        await pilot.pause()
        t5 = app.board.task_by_id("tm5")
        assert t5.start_date == t5.due_date == iso(38), "m re-applies the editor's +3 under together"
        said = "\n".join(_toasts(app))
        assert "moved" in said and "Mobile +3d past ◆" in said, said
        await pilot.press("m")                       # flag: the chain comes back
        await pilot.pause()
        assert _due(app.board, "tm2") == iso(5) and _due(app.board, "tm4") == due0["tm4"]
        # the refusal after an intervening action: a pin toggle evicts the entry
        await pilot.press("t")
        await pilot.pause()
        before = {tid: _due(app.board, tid) for tid in due0}
        await pilot.press("m")
        await pilot.pause()
        said = "\n".join(_toasts(app))
        assert "m re-applies the last date move — nothing to re-apply" in said, said
        assert {tid: _due(app.board, tid) for tid in before} == before, "m wrote nothing"


async def test_TC_638_the_select_shows_the_default_for_an_unset_rule(tmp_path):
    """TC-638 (P4 SEC4-4): a project with no date_links opens the editor with the
    select on `push` (the default shown, never a blank)."""
    path, _b = _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("P")
        await pilot.pause()
        app.screen.query_one("#proj-list", OptionList).highlighted = 0   # the first project
        await pilot.press("e")                       # the picker's edit binding
        for _ in range(3):
            await pilot.pause()
        sel = app.screen.query_one("#f-date-links", Select)
        assert sel.value == "push_delta", sel.value


# --------------------------------------------------------------------------- #
# TC-701/702 — the C-5 stale-entry refusal and the toast ladder's degrade (GAP-3)
# --------------------------------------------------------------------------- #
async def test_TC_701_the_c5_gate_refuses_when_the_moved_task_vanished(tmp_path):
    """TC-701 (LLR-604.4, C-5): `m` refuses when the top cascade entry names a
    task no longer on the board. The UI cannot reach this (a delete pushes its
    own undo entry), so the stale entry is synthesized by hand: after a real `+`
    on tm2, the entry's `task_id` is pointed at a task that does not exist while
    its `tasks` list is kept — `m` toasts the verbatim refusal and no date moves."""
    path, _b = _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        moved = {tid: _due(app.board, tid) for tid in ("tm2", "tm3", "tm4", "tm5")}
        app._undo_stack[-1]["cascade"]["task_id"] = "gone"   # the C-5 stale entry
        await pilot.press("m")
        await pilot.pause()
        said = "\n".join(_toasts(app))
        assert "m re-applies the last date move — nothing to re-apply" in said, said
        assert {tid: _due(app.board, tid) for tid in moved} == moved, "m wrote nothing"


async def test_TC_702_the_toast_fits_and_degrades_below_80(tmp_path):
    """TC-702 (GAP-3): at 118x30 a real `+` on tm2 toasts; re-rendering that move
    through the ladder at 80/60/40/24 keeps the toast within the width (the
    degrade-by-design contract), and at 24 the final fit never collapses to an
    empty string."""
    from taskboard.models import plan_move, resolve_mode
    from taskboard.views import vis
    path, _b = _board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        assert _toasts(app), "the real bump toasts"
        plan = plan_move(app.board, "tm2", 0, 1, resolve_mode(app.board, "tm2"), date.today())
        for width in (80, 60, 40, 24):
            await pilot.resize_terminal(width, 24)
            await pilot.pause()
            text = app._cascade_toast(app.board.task_by_id("tm2"), plan, 0)
            assert vis(text) <= width, (width, vis(text), text)
            if width == 24:
                assert text, "the fit never collapses to nothing at 24"
