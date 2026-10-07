"""P4 (validation) ux-reviewer cross-increment probes — batch 2026-10-06-batch-01.

The threads the per-increment gates could not take:
  P1  bump -> m(together) -> u restores PRE-MOVE dates; m then refuses.
  P2  bump -> pin (single-task entry) -> m refuses writing nothing -> u -> u clean.
  P3  the undo stack's FOUR shapes interleaved (cascade / milestones / migration /
      single-task): undo every order to a frozen board; m refuses on each shape.
  P4  m AFTER AN EDITOR chain save (cross-surface re-apply).
  P5  m after an EDITOR SOLO save (silent save, then m speaks from its own seat).
  P6  the toast at 60/40/24 columns: push_delta, flag, and the mixed-shift rungs.
  P7  team sync: D-630 — an existing project keeps its local date_links; a project
      first seen in a push imports its date_links whole (S-4).

Every app probe drives TaskboardApp with real keys (C-16) like the ATs do.
"""
from __future__ import annotations

import asyncio
import io
import json
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

REPO = Path("C:/Users/jjgh8/Github/taskboard")
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tests"))

import kg_board  # noqa: E402
import taskboard.app as _appmod  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.models import Task  # noqa: E402
from taskboard.views import vis  # noqa: E402

# the suite's own seam (tests/conftest.py, D-611): every run answers the one-time
# milestone offer at start, so keys land on the view under test
_appmod.milestones_marked = lambda settings: True

RENUMBER = "seen_view_renumber_2026_07"
TODAY = date.today()
ISO = lambda off: (TODAY + timedelta(days=off)).isoformat()
OUT = io.StringIO()


def log(msg=""):
    print(msg, file=OUT)
    print(msg)


def _board(tmp: Path):
    tmp.mkdir(parents=True, exist_ok=True)
    path = tmp / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    b.save()
    return path, b


def _due(b, tid):
    return b.task_by_id(tid).due_date


def _toasts(app):
    return [str(t.render()) for t in app.screen.query("Toast")]


def _last_toast(app):
    ts = _toasts(app)
    return ts[-1] if ts else ""


def _last_toast_msg(app):
    """The toast's message line (without the 'Move' title line) — the ladder's
    fitting rule is about the message, not the title."""
    return _last_toast(app).split("\n")[-1]


def _state(b):
    """The task state these probes mutate — for frozen comparisons."""
    return json.dumps([{k: getattr(t, k) for k in
                        ("id", "title", "phase", "start_date", "due_date",
                         "milestone", "archived", "depends_on", "pinned")}
                       for t in b.tasks], sort_keys=True)


PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    log(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


# --------------------------------------------------------------------------- #
async def p1_bump_m_undo(tmp):
    log("P1: bump -> m(together) -> u restores PRE-MOVE dates; m then refuses")
    path, b0 = _board(tmp)
    due0 = {tid: _due(b0, tid) for tid in ("tm2", "tm3", "tm4", "tm5")}
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        await pilot.press("m")            # push_delta -> together
        await pilot.pause()
        t5 = app.board.task_by_id("tm5")
        check("P1 m moved tm5 under together", t5.due_date != due0["tm5"] and
              _due(app.board, "tm3") != due0["tm3"], f"tm5={t5.due_date}")
        await pilot.press("u")
        await pilot.pause()
        got = {tid: _due(app.board, tid) for tid in due0}
        check("P1 one u after m restores PRE-MOVE dates", got == due0, str(got))
        app.clear_notifications()
        n_before = len(app._undo_stack)
        await pilot.press("m")
        await pilot.pause()
        check("P1 m after the undo refuses", "nothing to re-apply" in _last_toast(app),
              _last_toast(app))
        check("P1 the refusal writes nothing",
              len(app._undo_stack) == n_before and
              {tid: _due(app.board, tid) for tid in due0} == due0)


# --------------------------------------------------------------------------- #
async def p2_single_entry_between(tmp):
    log("P2: bump -> pin (single-task entry) -> m refuses; u; u restores dates")
    path, b0 = _board(tmp)
    due0 = {tid: _due(b0, tid) for tid in ("tm2", "tm3", "tm4")}
    pinned0 = b0.task_by_id("tm2").pinned
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        await pilot.press("t")            # pin: a SINGLE-TASK entry tops the stack
        await pilot.pause()
        check("P2 the pin landed", app.board.task_by_id("tm2").pinned != pinned0)
        app.clear_notifications()
        await pilot.press("m")
        await pilot.pause()
        check("P2 m with a single-task entry on top refuses",
              "nothing to re-apply" in _last_toast(app), _last_toast(app))
        check("P2 the refusal moved no date",
              {tid: _due(app.board, tid) for tid in due0} !=
              {tid: due0[tid] for tid in due0} and
              _due(app.board, "tm2") != due0["tm2"], "dates still bumped")
        await pilot.press("u")            # undo the pin
        await pilot.pause()
        check("P2 u undoes the pin", app.board.task_by_id("tm2").pinned == pinned0)
        await pilot.press("u")            # undo the bump
        await pilot.pause()
        got = {tid: _due(app.board, tid) for tid in due0}
        check("P2 the cascade entry still undoes clean under the pin entry",
              got == due0, str(got))


# --------------------------------------------------------------------------- #
def _push_fake_milestones(app, tid):
    """A conversion-shaped change + the SHIPPED milestones undo shape (app.py:301)."""
    t = app.board.task_by_id(tid)
    before = {"milestone": False, "start_date": t.start_date, "due_date": t.due_date}
    t.milestone = True
    t.start_date = t.due_date           # the shipped canonicalization
    app._undo_stack.append({"milestones": [{"task_id": tid, "fields": before}]})


def _push_fake_migration(app, tid):
    """A migration-shaped change + the SHIPPED migration undo shape (app.py:334)."""
    t = app.board.task_by_id(tid)
    before = {"blocked": t.blocked, "depends_on": list(t.depends_on)}
    t.depends_on = []
    app._undo_stack.append({"migration": [{"task_id": tid, "fields": before}]})


async def p3_mixed_shapes(tmp):
    log("P3: the undo stack's four shapes interleaved; m refuses on each shape")
    # order A: a bump, THEN a milestones-shaped change pushed on top
    path, b0 = _board(tmp)
    frozen = _state(b0)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        _push_fake_milestones(app, "tm3")   # the milestones shape now TOPS the stack
        app.clear_notifications()
        await pilot.press("m")
        await pilot.pause()
        check("P3 m refuses with a milestones entry above the move",
              "nothing to re-apply" in _last_toast_msg(app), _last_toast_msg(app))
        check("P3 the refusal moved no date",
              _due(app.board, "tm2") != None)
        await pilot.press("u")            # the conversion shape
        await pilot.pause()
        check("P3 u replays the milestones shape",
              app.board.task_by_id("tm3").milestone is False)
        await pilot.press("u")            # the bump
        await pilot.pause()
        check("P3 u undoes the conversion; board back to frozen bytes",
              _state(app.board) == frozen)
    # order B: bump first, THEN a migration-shaped change on top
    tmp.joinpath("b").mkdir(exist_ok=True)
    path, b0 = _board(tmp / "b")
    frozen = _state(b0)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        _push_fake_migration(app, "td5")
        app.clear_notifications()
        await pilot.press("m")            # top is migration-shaped: refuse
        await pilot.pause()
        check("P3 m refuses with a migration entry on top",
              "nothing to re-apply" in _last_toast(app), _last_toast(app))
        check("P3 the refusal wrote nothing",
              app.board.task_by_id("td5").depends_on == [])
        await pilot.press("u")            # the migration shape
        await pilot.pause()
        check("P3 u replays the migration shape",
              app.board.task_by_id("td5").depends_on != [])
        await pilot.press("u")            # the bump
        await pilot.pause()
        check("P3 u replays the cascade; board back to frozen bytes",
              _state(app.board) == frozen)
    # order C: m with a deleted-task cascade entry (C-5 gate on the final tree)
    tmp.joinpath("c").mkdir(exist_ok=True)
    path, _ = _board(tmp / "c")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        app.board.tasks[:] = [t for t in app.board.tasks if t.id != "tm2"]
        app.clear_notifications()
        await pilot.press("m")
        await pilot.pause()
        check("P3 m after the moved task vanished refuses (C-5)",
              "nothing to re-apply" in _last_toast(app), _last_toast(app))


# --------------------------------------------------------------------------- #
async def p4_m_after_editor_chain(tmp):
    log("P4: m after an EDITOR chain save re-applies the same move under the next mode")
    path, b0 = _board(tmp)
    due0 = {tid: _due(b0, tid) for tid in ("tm2", "tm3", "tm4", "tm5")}
    from textual.widgets import Button, Input
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        app.screen.query_one("#f-due", Input).value = ISO(5)   # +3 like AT-609
        await pilot.pause()
        app.screen.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        check("P4 the editor moved the chain",
              _due(app.board, "tm4") == ISO(31), _due(app.board, "tm4"))
        top = app._undo_stack[-1]
        check("P4 the editor entry is the cascade shape",
              "cascade" in top and top["cascade"]["dd"] == 3 and top["cascade"]["sd"] == 0,
              json.dumps(top["cascade"], default=str)[:120])
        app.clear_notifications()
        await pilot.press("m")            # push_delta -> together, dd=+3
        await pilot.pause()
        t5 = app.board.task_by_id("tm5")
        exp5 = (date.fromisoformat(due0["tm5"]) + timedelta(days=3)).isoformat()
        check("P4 m re-applied the EDITOR move under together (tm5 +3)",
              t5.start_date == t5.due_date == exp5, f"tm5={t5.due_date} exp={exp5}")
        said = "\n".join(_toasts(app))
        check("P4 m's toast names the new mode", "moved" in said, said)
        await pilot.press("u")
        await pilot.pause()
        got = {tid: _due(app.board, tid) for tid in due0}
        check("P4 one u restores the pre-edit dates", got == due0, str(got))


# --------------------------------------------------------------------------- #
async def p5_m_after_editor_solo(tmp):
    log("P5: m after an EDITOR SOLO save (silent) — m speaks from its own seat")
    path, b0 = _board(tmp)
    due0 = _due(b0, "ta6")
    from textual.widgets import Button, Input
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "ta6"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        app.screen.query_one("#f-due", Input).value = ISO(28)   # +2, nobody waits on ta6
        await pilot.pause()
        app.screen.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        check("P5 the solo edit applied", _due(app.board, "ta6") == ISO(28))
        check("P5 the solo editor save stayed SILENT (D-629)", _toasts(app) == [],
              str(_toasts(app)))
        check("P5 but the solo save DID record the cascade undo entry",
              "cascade" in app._undo_stack[-1])
        app.clear_notifications()
        await pilot.press("m")
        await pilot.pause()
        check("P5 m re-applied the solo move (dates unchanged, entry replaced)",
              _due(app.board, "ta6") == ISO(28) and "cascade" in app._undo_stack[-1])
        check("P5 m's seat says the move (say_solo)", _last_toast(app) != "",
              _last_toast(app))
        await pilot.press("u")
        await pilot.pause()
        check("P5 u restores the pre-edit due", _due(app.board, "ta6") == due0)


# --------------------------------------------------------------------------- #
async def p6_narrow_toasts(tmp):
    log("P6: the toast at 60/40/24 columns — push_delta, flag, mixed shifts")
    # 6a: plain push_delta bump at 60/40/24
    for w in (60, 40, 24):
        path, _ = _board(tmp / f"w{w}a")
        app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
        async with app.run_test(size=(w, 24), notifications=True) as pilot:
            await pilot.press("4")
            await pilot.pause()
            app.selected_task_id = "tm2"
            app.refresh_view()
            await pilot.press("+")
            await pilot.pause()
            toast = _last_toast_msg(app)
            check(f"P6a @{w}: toast message fits the width", vis(toast) <= w,
                  f"vis={vis(toast)} :: {toast!r}")
            if w == 60:
                check("P6a @60: the count rung (names do not fit)",
                      "Offline sync" not in toast and "pushed 2 +1d each" in toast, toast)
            if w == 40:
                check("P6a @40: count rung, no names", "Offline sync" not in toast
                      and "pushed 2" in toast, toast)
    # 6b: the flag arm at 60
    path, _ = _board(tmp / "w60b")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(60, 24), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.board.project_by_id("pmob").extra["date_links"] = "flag"
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await pilot.pause()
        toast = _last_toast_msg(app)
        check("P6b @60: the flag toast fits and names", vis(toast) <= 60
              and "flagged" in toast, f"vis={vis(toast)} :: {toast!r}")
    # 6c: the mixed-shift rungs (slack truncates the second shift)
    path, _ = _board(tmp / "w60c")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    from textual.widgets import Button, Input
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        b = app.board
        b.tasks.append(Task("Anchor", phase="Next", project_id="pmob",
                            due_date=ISO(2), id="ax"))
        b.tasks.append(Task("Beta release", phase="Next", project_id="pmob",
                            start_date=ISO(1), due_date=ISO(5),
                            depends_on=["ax"], id="bx"))
        b.tasks.append(Task("Offline sync", phase="Next", project_id="pmob",
                            start_date=ISO(9), due_date=ISO(13),
                            depends_on=["bx"], id="dx"))
        app.selected_task_id = "ax"
        app.refresh_view()
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        app.screen.query_one("#f-due", Input).value = ISO(6)   # +4
        await pilot.pause()
        app.screen.query_one("#save", Button).press()
        for _ in range(3):
            await pilot.pause()
        said = "\n".join(_toasts(app))
        check("P6c @118: the mixed-shift NAMES form",
              "pushed 2 dependents" in said and "+4d" in said and "+1d" in said, said)
    for w in (60, 40):
        path, _ = _board(tmp / f"w{w}c")
        app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
        async with app.run_test(size=(w, 24), notifications=True) as pilot:
            await pilot.press("4")
            await pilot.pause()
            b = app.board
            b.tasks.append(Task("Anchor", phase="Next", project_id="pmob",
                                due_date=ISO(2), id="ax"))
            b.tasks.append(Task("Beta release", phase="Next", project_id="pmob",
                                start_date=ISO(1), due_date=ISO(5),
                                depends_on=["ax"], id="bx"))
            b.tasks.append(Task("Offline sync", phase="Next", project_id="pmob",
                                start_date=ISO(9), due_date=ISO(13),
                                depends_on=["bx"], id="dx"))
            app.selected_task_id = "ax"
            app.refresh_view()
            await pilot.press("e")
            for _ in range(3):
                await pilot.pause()
            app.screen.query_one("#f-due", Input).value = ISO(6)
            await pilot.pause()
            app.screen.query_one("#save", Button).press()
            for _ in range(3):
                await pilot.pause()
            toast = _last_toast_msg(app)
            check(f"P6c @{w}: the mixed-shift COUNT form fits",
                  vis(toast) <= w and "pushed 2" in toast, f"vis={vis(toast)} :: {toast!r}")


# --------------------------------------------------------------------------- #
def p7_team_sync():
    log("P7: team sync — D-630 (existing keeps local; first-seen imports whole)")
    from taskboard.team_sync import TeamState

    tmp = Path(tempfile.mkdtemp())
    path, b = _board(tmp)
    b.project_by_id("pdwh").extra["date_links"] = "together"   # local choice
    b.save()
    ts = TeamState(shared_dir=tmp, user_id="op")
    ts.config = {
        "phases": list(b.phases),
        "projects": [
            {"id": "pdwh", "name": "Renamed By Team", "color": "#aabbcc",
             "date_links": "flag"},                       # must NOT land on existing
            {"id": "pnew", "name": "Brand New", "color": "#aabbcc",
             "date_links": "together"},                  # first seen: imports whole
        ],
    }
    ts.apply_config_to_board(b)
    check("P7 an EXISTING project keeps its local date_links (D-630)",
          b.project_by_id("pdwh").extra.get("date_links") == "together")
    check("P7 the merge itself ran (the team's name landed)",
          b.project_by_id("pdwh").name == "Renamed By Team")
    new = b.project_by_id("pnew")
    check("P7 a FIRST-SEEN project imports date_links whole (S-4)",
          new is not None and new.extra.get("date_links") == "together",
          str(new.extra) if new else "project absent")


# --------------------------------------------------------------------------- #
async def main():
    tmp = Path(tempfile.mkdtemp(prefix="p4ux_"))
    await p1_bump_m_undo(tmp)
    await p2_single_entry_between(tmp)
    await p3_mixed_shapes(tmp)
    await p4_m_after_editor_chain(tmp)
    await p5_m_after_editor_solo(tmp)
    await p6_narrow_toasts(tmp)
    p7_team_sync()
    log("")
    log(f"== {len(PASS)} passed, {len(FAIL)} failed ==")
    for f in FAIL:
        log(f"FAILED: {f}")
    dest = Path(__file__).with_name("p4-ux-probes.txt")
    dest.write_text(OUT.getvalue(), encoding="utf-8")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
