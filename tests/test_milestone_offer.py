"""The one-time milestone offer (batch 2026-10-04-batch-02, US-605, HLR-605).

Field report: the operator types milestones as one-day tasks (round 5); the verdict made M-3 a
one-time upgrade migration, not a feature. The operator's safeguard ("Sí: respaldo + registro +
deshacer"): the offer converts NOTHING the operator did not choose in the picker; whatever it
converts is backed up first, logged, revertible with `u`, and it is never offered twice. The
operator's real board is never opened: every board here is synthetic in `tmp_path`.

Law: on a readable board with no offer mark, as the last step of start: no candidate → marked
silently; candidates → the offer (one-day rows pre-checked, due-only rows not); `space` toggles,
`↵` converts exactly the checked candidates, `esc` converts none; either answer marks; converting
backs up the bytes as they stand, logs, flags, marks and saves atomically, says so, `u` reverts
in one step (the mark stays); any failure leaves the file untouched and unmarked and says why.

RED on base: no offer exists (the one-day tasks stay plain tasks).
"""
from __future__ import annotations

import builtins
import errno
import json
import os
import shutil
import stat
from datetime import date, timedelta
from pathlib import Path

import pytest

import kg_board
from taskboard.app import TaskboardApp
from taskboard.models import (MILESTONE_BACKUP, MILESTONE_LOG, MILESTONE_LOG_NOTE, Board,
                              Project, Task, milestone_candidates, milestones_marked,
                              run_milestone_offer)
from taskboard.modals import MilestoneOffer
from taskboard.team_sync import TeamState

pytestmark = pytest.mark.milestone_offer

RENUMBER = "seen_view_renumber_2026_07"
KT = kg_board.TODAY
# P-16 (`evidence/p1-thresholds.txt`): the offer's rows, in order — group 1 pre-checked.
ORDER = [("ta3", True), ("tw5", True), ("tm5", True),
         ("to3", False), ("to2", False), ("tw4", False), ("ta2", False), ("tw6", False)]


def _legacy(path: Path) -> Path:
    """The AT board: shifted kg board, three one-day tasks, the renumber key and the
    links mark, nothing the sweep would archive, no offer mark (pre-start bytes ==
    pre-conversion bytes, D-612)."""
    b = kg_board.one_day(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    b.save()
    return path


def _toasts(app) -> list[str]:
    return [str(t.render()) for t in app.screen.query("Toast")]


def _painted(app) -> list[str]:
    strips = app.screen._compositor.render_strips(app.screen.size)
    return ["".join(seg.text for seg in s) for s in strips]


def _saved(path: Path) -> dict:
    return {t["id"]: t for t in json.loads(path.read_text(encoding="utf-8"))["tasks"]}


def _beside(path: Path) -> set[str]:
    return {p.name for p in path.parent.iterdir()} - {path.name}


# --------------------------------------------------------------------------- #
# TC-614 — the candidates (LLR-605.1)
# --------------------------------------------------------------------------- #
def test_TC_614_the_candidates_of_the_one_day_board_in_order():
    """TC-614: over the kg one-day board the list equals P-16's 8 rows in order (one-
    day first, then due-only, each by due). RED: a group-by `bool(start)` (a start ≠
    due task as due-only), or board order."""
    b = kg_board.one_day(kg_board.build())
    assert [(t.id, p) for t, p in milestone_candidates(b)] == ORDER


def test_TC_614_what_is_never_a_candidate():
    """TC-614 (exclusions): done, archived, already a milestone, undated, a duration
    (start ≠ due), an unreadable start, a non-text title (security S-9), the second of
    a repeated id. RED: any of them offered."""
    def t(tid, **kw):
        kw.setdefault("due_date", "2026-10-10")
        return Task(kw.pop("title", tid), id=tid, **kw)
    b = Board([], [t("ok", start_date="2026-10-10"), t("done", phase="Done"),
                   t("arch", archived=True), t("ms", milestone=True, start_date="2026-10-10"),
                   t("undated", due_date=None), t("span", start_date="2026-10-01"),
                   t("garbled", start_date="soon"), t("int", title=7), t("ok2"),
                   t("ok", start_date=None)],
              kg_board.Path("x.json"), phases=["Doing", "Done"])
    assert [(x.id, p) for x, p in milestone_candidates(b)] == [("ok", True), ("ok2", False)]


@pytest.mark.parametrize("migrations, marked", [({"milestones": 1}, True),
                                                ({"milestones": 1.0}, False),
                                                ({"milestones": "1"}, False),
                                                ({"milestones": True}, False),
                                                ({"milestones": []}, False),
                                                ([], False), ("x", False), (None, False)])
def test_TC_614_the_mark_is_read_totally(migrations, marked):
    """TC-614: only the int 1 under a dict marks; anything else, of any type, is
    unmarked and never raises. RED: `bool()`, or `== 1` letting True and 1.0 in."""
    assert milestones_marked({"migrations": migrations}) is marked


# --------------------------------------------------------------------------- #
# TC-615 — convert, back up, log, mark, once (LLR-605.2)
# --------------------------------------------------------------------------- #
def _offer_board(tmp_path) -> Board:
    path = _legacy(tmp_path / "board.json")
    return Board.load(path)


def test_TC_615_backup_log_flags_mark_and_never_twice(tmp_path):
    """TC-615: the backup holds the bytes read before the call — after an earlier
    save in the same run — under the next free name; the log lists the conversions,
    the replaced mark (none) and the note; the links key is kept; the converted tasks
    have start = due; a second call returns None and writes nothing. RED: a backup
    after the apply; an overwrite of a taken name; no mark."""
    b = _offer_board(tmp_path)
    b.task_by_id("tw3").notes = "an earlier save in this run"
    b.save()
    raw = b.path.read_bytes()
    taken = b.path.with_name(b.path.name + MILESTONE_BACKUP)
    taken.write_bytes(b"somebody else's file")
    res = run_milestone_offer(b, ["ta3", "to3", "ta3"], KT)
    assert res.error is None and res.ineligible == 0
    assert res.backup == b.path.name + MILESTONE_BACKUP + ".1"
    assert taken.read_bytes() == b"somebody else's file"
    assert (tmp_path / res.backup).read_bytes() == raw
    log = json.loads((tmp_path / res.log).read_text(encoding="utf-8"))
    assert [c["task_id"] for c in log["changes"]] == ["ta3", "to3"]     # each once
    assert log["note"] == MILESTONE_LOG_NOTE and log["replaced_mark"] is None
    saved = json.loads(b.path.read_text(encoding="utf-8"))
    assert saved["settings"]["migrations"] == {"links": 1, "milestones": 1}
    tasks = {t["id"]: t for t in saved["tasks"]}
    for tid in ("ta3", "to3"):
        assert tasks[tid]["milestone"] is True
        assert tasks[tid]["start_date"] == tasks[tid]["due_date"]
    assert tasks["tw5"]["milestone"] is False
    listing, mtime = _beside(b.path), b.path.stat().st_mtime_ns
    assert run_milestone_offer(Board.load(b.path), ["tw5"], KT) is None
    assert _beside(b.path) == listing and b.path.stat().st_mtime_ns == mtime


def test_TC_615_none_chosen_marks_without_backup_and_counts_the_ineligible(tmp_path):
    """TC-615 (empty, S-6): nothing chosen → marked, no backup, no log; a chosen id
    that is not a candidate (done, or unknown) is counted, never converted. RED: a
    backup for nothing; a done task flagged."""
    b = _offer_board(tmp_path)
    b.task_by_id("to3").phase = "Done"
    res = run_milestone_offer(b, ["to3", "nope"], KT)
    assert (res.changes, res.ineligible, res.backup, res.log) == ([], 2, None, None)
    assert _beside(b.path) == set()
    assert milestones_marked(Board.load(b.path).settings)
    assert b.task_by_id("to3").milestone is False


def test_TC_615_a_malformed_mark_is_replaced_backed_up_and_logged(tmp_path):
    """TC-615 (S-7, D-621): a present malformed value is replaced by 1 and, though
    nothing is converted, the backup and the log are written, the log holding the
    old value. RED: the old value lost silently."""
    b = _offer_board(tmp_path)
    b.settings["migrations"]["milestones"] = "later"
    b.save()
    res = run_milestone_offer(b, [], KT)
    assert res.backup and res.log
    log = json.loads((tmp_path / res.log).read_text(encoding="utf-8"))
    assert log["replaced_mark"] == {"links": 1, "milestones": "later"}
    assert milestones_marked(Board.load(b.path).settings)


@pytest.mark.parametrize("fail", ["backup", "log", "save"])
def test_TC_615_any_failure_leaves_the_file_untouched_and_unmarked(tmp_path, monkeypatch, fail):
    """TC-615 (error): a failing backup, log or save leaves the board file
    byte-identical and unmarked, the tasks as before, no file of this run beside it,
    and the reason names a basename only. RED: a partial write, a flag left on."""
    b = _offer_board(tmp_path)
    raw = b.path.read_bytes()
    real_open = builtins.open
    marker = {"backup": MILESTONE_BACKUP, "log": MILESTONE_LOG}.get(fail)

    def failing_open(file, *a, **k):
        if marker and marker in str(file):
            raise PermissionError(errno.EACCES, "Permission denied", str(file))
        return real_open(file, *a, **k)
    monkeypatch.setattr(builtins, "open", failing_open)
    if fail == "save":
        monkeypatch.setattr(Board, "save_atomic",
                            lambda self: (_ for _ in ()).throw(OSError(errno.ENOSPC, "No space left", str(self.path))))
    res = run_milestone_offer(b, ["ta3", "tw5"], KT)
    monkeypatch.undo()
    assert res.error and os.sep not in res.error and "/" not in res.error
    assert b.path.read_bytes() == raw and _beside(b.path) == set()
    assert not milestones_marked(b.settings)
    assert not b.task_by_id("ta3").milestone and not b.task_by_id("tw5").milestone


def test_TC_615_a_failing_cleanup_still_restores_first(tmp_path, monkeypatch):
    """TC-615 (S-4): when the save fails AND removing this run's files fails too,
    the board is still restored and the first error returned. RED: cleanup before
    restore (an unlink error escaping and skipping the restore)."""
    b = _offer_board(tmp_path)
    monkeypatch.setattr(Board, "save_atomic",
                        lambda self: (_ for _ in ()).throw(OSError(errno.ENOSPC, "No space left", "board.json")))
    monkeypatch.setattr(Path, "unlink", lambda self, missing_ok=False: (_ for _ in ()).throw(
        PermissionError(errno.EACCES, "locked", str(self))))
    res = run_milestone_offer(b, ["ta3"], KT)
    monkeypatch.undo()
    assert res.error.startswith("board.json: No space left")
    assert not b.task_by_id("ta3").milestone and not milestones_marked(b.settings)


def test_TC_615_odd_due_spellings_come_back_exactly_on_failure(tmp_path, monkeypatch):
    """TC-615 (security S4-1): converting writes the due in canonical form; a failing
    save puts each task's start AND due back byte-exact, and the log records the start
    actually written. RED: the due left canonicalised in memory (then saved later)."""
    b = _offer_board(tmp_path)
    b.task_by_id("to3").due_date = "20261010"
    b.task_by_id("to2").due_date = " 2026-10-11 "
    b.save()
    monkeypatch.setattr(Board, "save_atomic",
                        lambda self: (_ for _ in ()).throw(OSError(errno.ENOSPC, "No space left", "board.json")))
    res = run_milestone_offer(b, ["to3", "to2"], KT)
    monkeypatch.undo()
    assert res.error
    assert (b.task_by_id("to3").due_date, b.task_by_id("to3").start_date) == ("20261010", None)
    assert b.task_by_id("to2").due_date == " 2026-10-11 "


def test_TC_615_the_log_records_the_start_actually_written(tmp_path):
    """TC-615 (S4-1): the log's `start_after` is the start the board saved. RED: the
    raw due text logged."""
    b = _offer_board(tmp_path)
    b.task_by_id("to3").due_date = "20261010"
    b.save()
    res = run_milestone_offer(b, ["to3"], KT)
    log = json.loads((tmp_path / res.log).read_text(encoding="utf-8"))
    assert log["changes"][0]["start_after"] == _saved(b.path)["to3"]["start_date"] == "2026-10-10"
    assert log["changes"][0]["due_before"] == "20261010"


def test_TC_615_a_team_pull_sees_no_extra_user(tmp_path):
    """TC-615: the backup and the log beside a board in a team folder are never read
    as a teammate's file. RED: a name matching `board.*.json`."""
    b = _offer_board(tmp_path)
    res = run_milestone_offer(b, ["ta3"], KT)
    assert res.backup and res.log
    st = TeamState(tmp_path, user_id="jav")
    st.pull()
    assert st.others == {}


# --------------------------------------------------------------------------- #
# TC-616 — offered once at start, said, undone (LLR-605.3)
# --------------------------------------------------------------------------- #
async def test_TC_616_a_seeded_board_is_marked_and_never_offered(tmp_path):
    """TC-616 (D-617, P-8): a board `Board.load` seeds carries both marks; its 11
    due-only seed tasks are never offered. RED: an unmarked seed (an offer of 11)."""
    path = tmp_path / "fresh.json"
    assert Board.load(path).settings["migrations"] == {"links": 1, "milestones": 1}
    app = TaskboardApp(board_path=str(tmp_path / "other.json"), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert not isinstance(app.screen, MilestoneOffer)


async def test_TC_616_enter_with_nothing_checked_is_not_now(tmp_path):
    """TC-616: `↵` with every row unchecked converts none and says "Not now" — as
    `esc`. RED: an empty conversion with a backup."""
    path = _legacy(tmp_path / "board.json")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.pause()
        for _ in range(3):                               # the three pre-checked rows
            await pilot.press("space")
            await pilot.press("down")
        await pilot.press("enter")
        await pilot.pause()
        assert sum("Not now" in x for x in _toasts(app)) == 1
    assert _beside(path) == set() and milestones_marked(Board.load(path).settings)


async def test_TC_616_a_task_that_stops_being_a_candidate_is_counted_not_converted(tmp_path):
    """TC-616 (security S-6, D-620): while the offer is open a checked task stops being
    a candidate (a sync tick can move a phase); `↵` converts the rest and the toast
    says `· 1 no longer eligible`. RED: the count hidden (battery O12)."""
    path = _legacy(tmp_path / "board.json")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, MilestoneOffer)
        app.board.task_by_id("tm5").phase = app.board.phases[-1]      # done behind the modal
        await pilot.press("enter")
        await pilot.pause()
        said = [x for x in _toasts(app) if "Milestones:" in x]
        assert len(said) == 1 and "Milestones: 2 converted · 1 no longer eligible" in said[0]
    assert _saved(path)["tm5"]["milestone"] is False


async def test_TC_616_u_restores_both_dates_byte_exact(tmp_path):
    """TC-616 (S4-1): after a conversion `u` puts each task's start and due back as
    they were stored, odd spellings included. RED: an undo entry without the due."""
    path = tmp_path / "board.json"
    b = kg_board.one_day(kg_board.shifted(path), date.today())
    b.task_by_id("ta3").due_date = b.task_by_id("ta3").start_date = (
        b.task_by_id("ta3").due_date.replace("-", ""))
    b.settings[RENUMBER] = True
    b.save()
    before = {k: (v["start_date"], v["due_date"]) for k, v in _saved(path).items()}
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        assert _saved(path)["ta3"]["milestone"] is True
        await pilot.press("u")
        await pilot.pause()
    assert {k: (v["start_date"], v["due_date"]) for k, v in _saved(path).items()} == before


async def test_TC_616_the_offer_covers_the_identity_picker_until_answered(tmp_path):
    """TC-616 (D-615, code review O-3): in team mode with no identity yet, the offer
    opens ON TOP of the identity picker; answering it leaves the picker on screen.
    RED: the offer before the team start (the picker on top)."""
    path = _legacy(tmp_path / "board.json")
    team = tmp_path / "team"
    team.mkdir()
    (team / "team.json").write_text(json.dumps(kg_board.TEAM), encoding="utf-8")
    b = Board.load(path)
    b.settings["team_shared_dir"] = str(team)
    b.save()
    from taskboard.modals import TeamIdentityPicker
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40)) as pilot:
        await pilot.pause()
        kinds = [type(s).__name__ for s in app.screen_stack]
        assert kinds[-2:] == ["TeamIdentityPicker", "MilestoneOffer"], kinds
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, TeamIdentityPicker)


async def test_TC_616_no_offer_on_an_unreadable_load(tmp_path):
    """TC-616: an unreadable board file gets no offer and no offer mark; its bytes
    survive in the shipped `.corrupt` quarantine. (The shipped renumber notice then
    saves an empty board over it — security S-13 of batch 2026-10-04-batch-01, in
    BACKLOG, not this batch's.) RED: an offer over the empty in-memory board."""
    path = tmp_path / "board.json"
    path.write_text("{not json", encoding="utf-8")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert not isinstance(app.screen, MilestoneOffer)
    assert path.with_name(path.name + ".corrupt").read_text(encoding="utf-8") == "{not json"
    assert not milestones_marked(Board.load(path).settings)


async def test_TC_616_both_migrations_on_one_start_undo_the_offer_first(tmp_path):
    """TC-616 (qa Q-20): a board needing the link migration AND the offer: two
    toasts, two undo entries; the first `u` reverts the conversion, the second the
    links. RED: one shared entry, or the wrong order."""
    path = tmp_path / "board.json"
    b = kg_board.legacy(path, old_done=False)
    d = (date.today() + timedelta(days=3)).isoformat()
    b.tasks.append(Task("One-day launch", start_date=d, due_date=d, id="od"))
    b.settings[RENUMBER] = True
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, MilestoneOffer)
        await pilot.press("enter")
        await pilot.pause()
        said = _toasts(app)
        assert any("Links migrated" in x for x in said) and any("Milestones:" in x for x in said)
        assert [next(iter(e)) for e in app._undo_stack[-2:]] == ["migration", "milestones"]
        app.clear_notifications()
        await pilot.press("u")
        await pilot.pause()
        assert any("Milestone conversion undone" in x for x in _toasts(app))
        await pilot.press("u")
        await pilot.pause()
        assert any("Links migration undone" in x for x in _toasts(app))


async def test_TC_616_quitting_unanswered_leaves_the_board_unmarked(tmp_path):
    """TC-616 (D-615): closing the app with the offer open is no answer: the board
    stays unmarked and the next start offers again. RED: a mark written on push."""
    path = _legacy(tmp_path / "board.json")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40)) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, MilestoneOffer)
    assert not milestones_marked(Board.load(path).settings)


async def test_TC_616_a_read_only_board_without_candidates_says_nothing(tmp_path):
    """TC-616 (D-616): a mark-only write that fails when no offer was shown is
    silent (no "offer stopped" for an offer the user never saw). RED: the failure
    toast at every start of a read-only board."""
    path = tmp_path / "board.json"
    b = Board([], [Task("busy", start_date="2026-10-01", due_date="2026-10-09", id="a")],
              path, {"migrations": {"links": 1}, RENUMBER: True})
    b.save()
    os.chmod(path, stat.S_IREAD)
    if os.access(path, os.W_OK):
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
        pytest.skip("this account writes through a read-only bit")
    try:
        app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
        async with app.run_test(size=(118, 30), notifications=True) as pilot:
            await pilot.pause()
            assert not any("offer" in x.lower() for x in _toasts(app))
    finally:
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)


# --------------------------------------------------------------------------- #
# TC-617 — the offer screen (LLR-605.4)
# --------------------------------------------------------------------------- #
async def test_TC_617_rows_order_marks_and_keys(tmp_path):
    """TC-617: 2 headings + 8 rows in P-16's order, 3 `▣`; `space` on a row flips it
    and the keys row's N; on a heading it does nothing (the cursor never rests
    there). RED: rows in board order; a stale N."""
    path = _legacy(tmp_path / "board.json")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40)) as pilot:
        await pilot.pause()
        scr = app.screen
        assert isinstance(scr, MilestoneOffer)
        painted = "\n".join(_painted(app))
        titles = [app.board.task_by_id(tid).title for tid, _ in ORDER]
        at = [painted.index(t) for t in titles]
        assert at == sorted(at)
        assert painted.index("One-day tasks (start = due)") < at[0]
        assert at[2] < painted.index("Due date, no start") < at[3]
        assert painted.count("▣") == 3 and painted.count("□") == 5
        assert "↵ convert 3" in painted
        assert "Partner notice emails" in painted and "1 waits on it" in painted
        await pilot.press("space")
        await pilot.pause()
        painted = "\n".join(_painted(app))
        assert painted.count("▣") == 2 and "↵ convert 2" in painted


async def test_TC_617_enter_returns_the_checked_candidates_own_ids(tmp_path):
    """TC-617 (S-5): `↵` returns the checked candidates' own ids — an int id as the
    int, never a re-parsed string; `esc` returns []. RED: string ids; every row."""
    got = {}
    b = Board([], [Task("A", start_date="2026-10-09", due_date="2026-10-09", id=7),
                   Task("B", due_date="2026-10-12", id="b")], tmp_path / "x.json")
    from textual.app import App

    class Host(App):
        def on_mount(self):
            self.push_screen(MilestoneOffer(b, milestone_candidates(b), KT),
                             lambda r: got.setdefault("r", r))
    async with Host().run_test(size=(100, 24)) as pilot:
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
    assert got["r"] == [7]
    got.clear()
    async with Host().run_test(size=(100, 24)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
    assert got["r"] == []


async def test_TC_617_user_text_paints_literally(tmp_path):
    """TC-617 (S1, security S-2): a title and a project name that look like markup
    paint as typed. RED: a row built with markup."""
    b = Board([Project("[b]p[/b]", "sky", id="p")],
              [Task("[b]x[/b]", "p", start_date="2026-10-09", due_date="2026-10-09", id="a")],
              tmp_path / "x.json")
    from textual.app import App

    class Host(App):
        def on_mount(self):
            self.push_screen(MilestoneOffer(b, milestone_candidates(b), KT))
    host = Host()
    async with host.run_test(size=(100, 24)) as pilot:
        await pilot.pause()
        painted = "\n".join(_painted(host))
        assert "[b]x[/b]" in painted and "[b]p[/b]" in painted


async def test_TC_617_a_long_title_is_cut_before_its_project_and_date(tmp_path):
    """TC-617 (code review O-1, O-2): at 80×24 a 90-character title is cut with `…` and
    the row still shows its project and date; the title is not painted in the accent
    (the colour marks the box only). RED: the row cut at its end (no project, no date,
    no `…`); the box's colour as the row's base style."""
    from taskboard.views import HEX
    long = "A very long candidate title that keeps going well past the width of the row " * 2
    b = Board([Project("Website Redesign", "violet", id="p")],
              [Task(long.strip(), "p", due_date="2026-10-09", start_date="2026-10-09", id="a"),
               Task("short", "p", due_date="2026-10-09", id="b")], tmp_path / "x.json")
    from textual.app import App

    class Host(App):
        def on_mount(self):
            self.push_screen(MilestoneOffer(b, milestone_candidates(b), KT))
    host = Host()
    async with host.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        strips = host.screen._compositor.render_strips(host.screen.size)
        rows = ["".join(seg.text for seg in s) for s in strips]
        row = next(r for r in rows if "A very long" in r)
        assert "…" in row and "Website Redesign · Oct 9" in row, row
        i = rows.index(row)
        accent = HEX["accent"].lower()
        title_hex = {seg.style.color.triplet.hex.lower() for seg in strips[i]
                     if "very long" in seg.text and seg.style and seg.style.color
                     and seg.style.color.triplet}
        assert accent not in title_hex, title_hex


async def test_TC_617_thirty_four_candidates_fit_80x24(tmp_path):
    """TC-617 (ux UX-3): at 80×24 with 34 candidates the box is inside the screen,
    the title and the keys row are painted in full, and `↓` to the last row brings it
    into view. RED: a box taller than the screen pushing the keys row off."""
    tasks = [Task(f"Long candidate title number {i:02d} with many words", None,
                  start_date=(KT + timedelta(days=i)).isoformat() if i % 2 == 0 else None,
                  due_date=(KT + timedelta(days=i)).isoformat(), id=f"c{i}") for i in range(34)]
    b = Board([], tasks, tmp_path / "x.json")
    from textual.app import App

    class Host(App):
        def on_mount(self):
            self.push_screen(MilestoneOffer(b, milestone_candidates(b), KT))
    host = Host()
    async with host.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        painted = _painted(host)
        assert any("◆ Milestones · convert one-day tasks?" in r for r in painted)
        assert any("space toggle  ·  ↵ convert 17  ·  esc not now — won't ask again" in r
                   for r in painted)
        last = milestone_candidates(b)[-1][0].title[:20]
        for _ in range(40):
            await pilot.press("down")
        await pilot.pause()
        assert any(last in r for r in _painted(host))


# --------------------------------------------------------------------------- #
# AT-604, AT-605, AT-606 — through the shipped surface (HLR-605)
# --------------------------------------------------------------------------- #
async def test_AT_604_only_what_was_picked_is_converted_backed_up_logged_and_undoable(tmp_path):
    """AT-604 (US-605, C-12): uncheck `Partner notice emails`, check `Review pull
    requests`, `↵`: the backup equals the bytes before `↵` (its first name taken →
    `.1`); exactly `tw5`, `tm5`, `to3` become milestones with start = due, `ta3`
    stays a one-day task; the log lists those 3; one toast; a FRESH app on that file
    shows no offer and labels ` ◆ Launch new homepage` in the gantt. On a second copy,
    `↵` then `u` restores all, the mark stays, and a fresh app shows no offer. RED on
    base: no offer."""
    (tmp_path / "a").mkdir()
    path = _legacy(tmp_path / "a" / "board.json")
    second = tmp_path / "b"
    second.mkdir()
    shutil.copy2(path, second / "board.json")
    path.with_name(path.name + MILESTONE_BACKUP).write_bytes(b"taken")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, MilestoneOffer)
        await pilot.press("space")                      # Partner notice emails: off
        for _ in range(3):
            await pilot.press("down")                   # … over the heading to Review PRs
        await pilot.press("space")
        await pilot.pause()
        assert "↵ convert 3" in "\n".join(_painted(app))
        before = path.read_bytes()
        await pilot.press("enter")
        await pilot.pause()
        said = [x for x in _toasts(app) if "Milestones:" in x]
        assert len(said) == 1 and "Milestones: 3 converted" in said[0]
        assert MILESTONE_BACKUP + ".1" in said[0]
    backup = path.with_name(path.name + MILESTONE_BACKUP + ".1")
    assert backup.read_bytes() == before
    assert path.with_name(path.name + MILESTONE_BACKUP).read_bytes() == b"taken"
    saved = _saved(path)
    assert {k for k, v in saved.items() if v["milestone"]} == {"tw5", "tm5", "to3"}   # qa F-1
    for tid in ("tw5", "tm5", "to3"):
        assert saved[tid]["milestone"] is True
        assert saved[tid]["start_date"] == saved[tid]["due_date"]
    assert saved["ta3"]["milestone"] is False
    assert saved["ta3"]["start_date"] == saved["ta3"]["due_date"]        # untouched
    log = json.loads(path.with_name(path.name + MILESTONE_LOG).read_text(encoding="utf-8"))
    assert sorted(c["task_id"] for c in log["changes"]) == ["tm5", "to3", "tw5"]
    fresh = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with fresh.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert not isinstance(fresh.screen, MilestoneOffer)
        await pilot.press("3")
        await pilot.pause()
        assert any(" ◆ Launch new homepage" in r for r in _painted(fresh))
    other = second / "board.json"
    app = TaskboardApp(board_path=str(other), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.pause()
        original = {k: (v["milestone"], v["start_date"]) for k, v in _saved(other).items()}
        await pilot.press("enter")                      # the defaults: the 3 one-day tasks
        await pilot.pause()
        assert {k for k, v in _saved(other).items() if v["milestone"]} == {"ta3", "tw5", "tm5"}
        await pilot.press("u")
        await pilot.pause()
        assert {k: (v["milestone"], v["start_date"]) for k, v in _saved(other).items()} == original
        assert any("Milestone conversion undone" in x for x in _toasts(app))
    assert milestones_marked(Board.load(other).settings)
    fresh = TaskboardApp(board_path=str(other), team_sync_interval=1e9)
    async with fresh.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert not isinstance(fresh.screen, MilestoneOffer)


async def test_AT_605_not_now_and_no_candidate_mark_and_convert_nothing(tmp_path):
    """AT-605 (US-605): `esc` → marked, 0 converted, no backup, no log, one `Not now`
    toast, and the next start shows nothing; a board with no candidate and a seeded
    board → marked, no offer. RED: an offer that comes back, or a write beside."""
    path = _legacy(tmp_path / "board.json")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, MilestoneOffer)
        await pilot.press("escape")
        await pilot.pause()
        assert sum("Not now" in x for x in _toasts(app)) == 1
    assert _beside(path) == set()
    assert not any(t["milestone"] for t in _saved(path).values())
    assert milestones_marked(Board.load(path).settings)
    again = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with again.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert not isinstance(again.screen, MilestoneOffer)
    none = tmp_path / "none.json"
    Board([], [Task("busy", start_date="2026-10-01", due_date="2026-10-09", id="a")], none,
          {"migrations": {"links": 1}, RENUMBER: True}).save()
    app = TaskboardApp(board_path=str(none), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert not isinstance(app.screen, MilestoneOffer)
    assert milestones_marked(Board.load(none).settings)
    seeded = tmp_path / "seeded.json"
    app = TaskboardApp(board_path=str(seeded), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert not isinstance(app.screen, MilestoneOffer)
    assert milestones_marked(Board.load(seeded).settings)


async def test_AT_606_a_backup_that_cannot_be_made_changes_nothing(tmp_path, monkeypatch):
    """AT-606 (US-605, error branch, D-609): when the backup cannot be created (the
    stdlib `open` refuses only names holding `.pre-milestones`), the board file stays
    byte-identical and unmarked, one error toast names the failure, the app keeps
    running, and the next start offers again. RED: a conversion without its backup,
    or a mark that hides the offer."""
    path = _legacy(tmp_path / "board.json")
    raw = path.read_bytes()
    real_open = builtins.open

    def failing_open(file, *a, **k):
        if MILESTONE_BACKUP in str(file):
            raise PermissionError(errno.EACCES, "Permission denied", str(file))
        return real_open(file, *a, **k)

    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.pause()
        monkeypatch.setattr(builtins, "open", failing_open)
        await pilot.press("enter")
        await pilot.pause()
        monkeypatch.setattr(builtins, "open", real_open)
        said = [x for x in _toasts(app) if "Milestone offer stopped" in x]
        assert len(said) == 1 and "Permission denied" in said[0]
        assert str(tmp_path) not in said[0]
        assert app.is_running
    assert path.read_bytes() == raw and _beside(path) == set()
    again = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with again.run_test(size=(118, 40)) as pilot:
        await pilot.pause()
        assert isinstance(again.screen, MilestoneOffer)
