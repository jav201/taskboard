"""The one-time link migration (batch 2026-10-04-batch-01, HLR-505).

Field report: until this batch the only writer of `depends_on` was `b` — blocking
appended the picked id, unblocking cleared the flag and KEPT the id. Under the new
meaning (a link = "waits on") every kept id is a live wait, so an existing board
would re-block work its owner had unblocked. The operator's safeguard: a backup of
the board file BEFORE anything changes, every change logged, a way back, never a
second run (standing authorization, "Respaldo automático + deshacer").

Law: the migration is the app's first write; it backs up the file's own bytes by
exclusive create, logs, applies, marks and saves atomically, or — on any failure —
leaves the file byte-identical and unmarked and stops the app. Every board here is
synthetic (`tests/kg_board.py`) in `tmp_path`; no user data directory is touched.

RED on base: none of `migrate_links`, `run_link_migration` or the mark exists, and
the app starts on a legacy board without touching its links.
"""
from __future__ import annotations

import builtins
import errno
import json
import os
import stat
import time
from pathlib import Path

import pytest

import kg_board
from taskboard.app import TaskboardApp
from taskboard.models import (MIGRATION_BACKUP, MIGRATION_LOG, Board,
                              Task, links_marked, migrate_links, run_link_migration)
from taskboard.team_sync import TeamState


def _toasts(app) -> list[str]:
    return [str(t.render()) for t in app.screen.query("Toast")]


def _state(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {t["id"]: (t["blocked"], t["depends_on"]) for t in data["tasks"]}


def _beside(path: Path) -> set[str]:
    return {p.name for p in path.parent.iterdir()} - {path.name}


# --------------------------------------------------------------------------- #
# TC-514 — the legacy rule (LLR-505.1)
# --------------------------------------------------------------------------- #
def test_TC_514_the_legacy_shapes_land_on_the_rule(tmp_path):
    """TC-514 (LLR-505.1): each shape of §5 lands as tabled, the change list holds
    exactly the changed tasks, and the board is untouched by the call. RED: a rule
    keeping released links to open tasks (L3), clearing L5's or L8's flag, keeping
    both links of the L7 loop, or applying while it computes."""
    b = kg_board.legacy(tmp_path / "board.json")
    before = {t.id: (t.blocked, list(t.depends_on)) for t in b.tasks}
    changes = migrate_links(b)
    assert {t.id: (t.blocked, list(t.depends_on)) for t in b.tasks} == before
    assert {ch.task_id for ch in changes} == kg_board.LEGACY_CHANGED
    got = dict(before)
    for ch in changes:
        assert ch.before == before[ch.task_id]
        got[ch.task_id] = (ch.after[0], list(ch.after[1]))
    for tid, want in kg_board.LEGACY_AFTER.items():
        assert got[tid] == (want[0], want[1]), tid
    notes = {ch.task_id: ch.note for ch in changes}
    assert "press b" in notes["L1"]                   # A2-1: the way back is said
    assert "loop" in notes["L7b"]


def test_TC_514_no_kept_link_closes_a_loop(tmp_path):
    """TC-514 (D-516, architect A2-2): links kept because their target is CLOSED
    are loop-checked too. Y is done and was blocked on Z; Z blocked on X; X keeps
    a released link to the done Y. Without the check all three are kept and
    reopening Y surfaces a live loop. RED: a check on open blockers only."""
    x = Task("X", phase="Doing", depends_on=["Y"], id="X")
    y = Task("Y", phase="Done", blocked=True, depends_on=["Z"], id="Y")
    z = Task("Z", phase="Doing", blocked=True, depends_on=["X"], id="Z")
    b = Board([], [x, y, z], tmp_path / "b.json", phases=["Doing", "Done"])
    after = {t.id: list(t.depends_on) for t in b.tasks}
    for ch in migrate_links(b):
        after[ch.task_id] = list(ch.after[1])
    # exactly the loop-closing link goes (code review F8: "drop everything"
    # would also leave no loop)
    assert after == {"X": ["Y"], "Y": ["Z"], "Z": []}


def test_TC_514_a_repeated_task_id_is_left_as_it_is(tmp_path):
    """TC-514 (code review F4): two tasks with one id (a hand edit) — the first is
    migrated, the second untouched, and no change names the second. RED: a rule
    keyed by a dict where the LAST copy wins while the apply hits the first."""
    a1 = Task("A one", blocked=True, depends_on=["B"], id="A")
    a2 = Task("A two", blocked=True, depends_on=["B"], id="A")
    bt = Task("B", id="B")
    b = Board([], [a1, a2, bt], tmp_path / "b.json")
    changes = migrate_links(b)
    assert [(ch.task_id, ch.title) for ch in changes] == [("A", "A one")]


def test_TC_514_an_empty_board_has_nothing_to_change(tmp_path):
    """TC-514 boundary: no tasks, no change records."""
    assert migrate_links(Board([], [], tmp_path / "b.json")) == []


# --------------------------------------------------------------------------- #
# TC-515 — backup, log, mark, once, atomically (LLR-505.2)
# --------------------------------------------------------------------------- #
def test_TC_515_backup_is_the_files_own_bytes_and_names_are_never_reused(tmp_path):
    """TC-515: the backup holds the board file's bytes as they were BEFORE the
    call; a taken name is left untouched and `.1` used; the log lists exactly the
    changes; the mark is set and saved; a second call does nothing. RED: a backup
    written after the apply, an overwrite of the taken name, no mark."""
    path = tmp_path / "board.json"
    b = kg_board.legacy(path)
    raw = path.read_bytes()
    taken = path.with_name(path.name + MIGRATION_BACKUP)
    taken.write_bytes(b"somebody else's file")
    result = run_link_migration(b)
    assert result is not None and result.error is None
    assert result.backup == path.name + MIGRATION_BACKUP + ".1"
    assert taken.read_bytes() == b"somebody else's file"
    assert (tmp_path / result.backup).read_bytes() == raw
    log = json.loads((tmp_path / result.log).read_text(encoding="utf-8"))
    assert log["backup"] == result.backup
    assert [c["task_id"] for c in log["changes"]] == [ch.task_id for ch in result.changes]
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["settings"]["migrations"] == {"links": 1}
    assert _state(path)["L2"] == (False, ["to2"])
    listing, mtime = _beside(path), path.stat().st_mtime_ns
    again = run_link_migration(Board.load(path))
    assert again is None
    assert _beside(path) == listing and path.stat().st_mtime_ns == mtime


def test_TC_515_a_board_needing_no_change_is_marked_without_backup(tmp_path):
    """TC-515 (empty branch): nothing to change → marked and saved, no backup,
    no log. RED: a backup or log written for nothing."""
    path = tmp_path / "board.json"
    b = Board([], [Task("lone", blocked=True)], path)
    b.save()
    result = run_link_migration(b)
    assert result is not None and result.changes == [] and result.backup is None
    assert _beside(path) == set()
    assert links_marked(Board.load(path).settings)


@pytest.mark.parametrize("mark", [[1], "1", {"links": 0}, {"links": True}, {"links": "1"}])
def test_TC_515_a_malformed_mark_never_raises_and_forces_the_backup(tmp_path, mark):
    """TC-515 (S-4, S2-2): any `migrations` value but `{"links": 1}` is unmarked —
    read without raising — and replacing it forces the backup and the log, which
    records the old value. RED: indexing a list or str; trusting `True == 1`."""
    path = tmp_path / "board.json"
    b = Board([], [Task("lone")], path, settings={"migrations": mark})
    b.save()
    assert not links_marked(b.settings)
    result = run_link_migration(b)
    assert result.error is None and result.backup and result.log
    log = json.loads((tmp_path / result.log).read_text(encoding="utf-8"))
    assert log["replaced_mark"] == mark
    assert links_marked(Board.load(path).settings)


def test_TC_515_a_marked_or_unreadable_board_is_left_alone(tmp_path):
    """TC-515 (invalid branches): a marked board and an unreadable file → None,
    nothing written. RED: a migration that ignores the mark or saves over a
    quarantined file (S-13)."""
    path = tmp_path / "board.json"
    b = kg_board.legacy(path)
    b.settings["migrations"] = {"links": 1}
    b.save()
    raw = path.read_bytes()
    assert run_link_migration(Board.load(path)) is None
    assert path.read_bytes() == raw and _beside(path) == set()
    bad = tmp_path / "bad" / "board.json"
    bad.parent.mkdir()
    bad.write_text("{not json", encoding="utf-8")
    loaded = Board.load(bad)
    assert run_link_migration(loaded) is None
    assert bad.read_text(encoding="utf-8") == "{not json"


@pytest.mark.parametrize("fail", ["backup", "log", "save"])
def test_TC_515_any_failure_leaves_the_file_untouched_and_unmarked(tmp_path, monkeypatch, fail):
    """TC-515 (error branches, S-3, D-518): a backup, a log or a save that fails
    leaves the board file byte-identical and unmarked, the board in memory as it
    was, and no temporary file behind; the reason names a file, never a folder.
    The fault is injected at the stdlib boundary (open / os.replace). RED: a
    rollback that forgets the links or the mark; a save in place."""
    path = tmp_path / "board.json"
    b = kg_board.legacy(path)
    raw = path.read_bytes()
    before = {t.id: (t.blocked, list(t.depends_on)) for t in b.tasks}
    real_open, real_replace = builtins.open, os.replace
    suffix = {"backup": MIGRATION_BACKUP, "log": MIGRATION_LOG}.get(fail)

    def failing_open(file, *a, **k):
        if suffix and suffix in str(file):
            raise PermissionError(errno.EACCES, "Permission denied", str(file))
        return real_open(file, *a, **k)

    def failing_replace(src, dst):
        raise PermissionError(errno.EACCES, "Permission denied", str(dst))

    monkeypatch.setattr(builtins, "open", failing_open)
    if fail == "save":
        monkeypatch.setattr(os, "replace", failing_replace)
    result = run_link_migration(b)
    monkeypatch.setattr(builtins, "open", real_open)
    monkeypatch.setattr(os, "replace", real_replace)
    assert result.error and "Permission denied" in result.error
    assert os.sep not in result.error and "/" not in result.error
    assert path.read_bytes() == raw
    assert {t.id: (t.blocked, list(t.depends_on)) for t in b.tasks} == before
    assert "migrations" not in b.settings
    assert not any(n.endswith(".tmp") for n in _beside(path))
    # code review F5: a failed run leaves none of the files it made
    assert _beside(path) == set()


def test_TC_515_a_leftover_temp_file_never_blocks_the_save(tmp_path):
    """TC-515 (code review F2, security S3-1): files a crash could have left
    beside the board — the old fixed temp name and a random-style one — are
    neither written through nor removed, and the migration still saves. RED: a
    fixed temp name created exclusively (every later start exits "File
    exists"), or one opened for plain writing (written through)."""
    path = tmp_path / "board.json"
    b = kg_board.legacy(path)
    stale = [path.with_name(path.name + ".tmp-links-migration"),
             path.with_name(f".{path.name}.leftover.tmp")]
    for f in stale:
        f.write_text("not yours", encoding="utf-8")
    result = run_link_migration(b)
    assert result.error is None
    assert all(f.read_text(encoding="utf-8") == "not yours" for f in stale)
    assert links_marked(Board.load(path).settings) and not path.is_symlink()
    assert {n for n in _beside(path) if n.endswith(".tmp")} == {stale[1].name}


def test_TC_515_a_malformed_dict_mark_keeps_its_other_keys(tmp_path):
    """TC-515 (security S3-3): `{"other": 7, "links": 0}` becomes
    `{"other": 7, "links": 1}`. RED: the dict replaced whole."""
    path = tmp_path / "board.json"
    b = Board([], [Task("lone")], path, settings={"migrations": {"other": 7, "links": 0}})
    b.save()
    run_link_migration(b)
    assert Board.load(path).settings["migrations"] == {"other": 7, "links": 1}


def test_TC_515_team_pull_never_reads_the_backup_or_the_log(tmp_path):
    """TC-515 (S-1, D-521): with the board in the team's shared folder, a pull
    sees no extra member for the backup or the log. RED: a backup named
    `board.pre-links-migration.json` (it matches team pull's `board.*.json`)."""
    path = tmp_path / "board.json"
    b = kg_board.legacy(path)
    result = run_link_migration(b)
    assert result.backup and result.log
    st = TeamState(tmp_path, user_id="me")
    assert st.pull()
    assert st.others == {}


def test_TC_515_a_dangling_symlink_at_the_backup_name_counts_as_taken(tmp_path):
    """TC-515 (code review F3, LLR-505.2): a dangling symlink at the backup's name
    is left alone and `.1` is used — nothing is written through it. Skipped where
    the OS refuses symlinks (declared). RED: the symlink check removed."""
    path = tmp_path / "board.json"
    b = kg_board.legacy(path)
    link = path.with_name(path.name + MIGRATION_BACKUP)
    try:
        link.symlink_to(tmp_path / "nowhere")
    except OSError:
        pytest.skip("symlinks unavailable on this host")
    result = run_link_migration(b)
    assert result.backup == link.name + ".1"
    assert link.is_symlink() and not (tmp_path / "nowhere").exists()


def test_TC_515_a_symlinked_board_keeps_its_link(tmp_path):
    """TC-515 (S2-1): the backup, log and swap work on the RESOLVED file, so a
    symlinked board keeps its link and its target is migrated. Skipped where the
    OS refuses symlinks (declared)."""
    real = tmp_path / "real" / "board.json"
    real.parent.mkdir()
    kg_board.legacy(real)
    link = tmp_path / "board.json"
    try:
        link.symlink_to(real)
    except OSError:
        pytest.skip("symlinks unavailable on this host")
    result = run_link_migration(Board.load(link))
    assert result.error is None
    assert link.is_symlink()
    assert (real.parent / result.backup).exists()
    assert links_marked(Board.load(real).settings)


def test_TC_518_migration_cost_is_bounded_on_hostile_boards(tmp_path):
    """TC-518, the migration's arm (S-5): a chain of 5000 blocked tasks, one task
    holding 100 000 ids, and a dense 800-task board each migrate in < 1 s with no
    RecursionError. RED: a linear `x not in list` dedupe (quadratic on 100 000
    ids) or a loop search on every link."""
    chain = [Task(f"c{i}", blocked=True, depends_on=[f"c{i - 1}"] if i else [], id=f"c{i}")
             for i in range(5000)]
    many = [Task("hub", blocked=True, depends_on=[f"c{i % 5000}" for i in range(100_000)],
                 id="hub")]
    dense = [Task(f"d{i}", blocked=True, depends_on=[f"d{j}" for j in range(800) if j != i][:400],
                  id=f"d{i}") for i in range(800)]
    # code review F1: a done hub linked to N done tasks, each linked forward,
    # listed in reverse — every link is kept (closed targets), so a search per
    # link costs links × graph; one walk back per task does not
    n = 400
    hub = [Task("hub", phase="Done", depends_on=[f"h{i}" for i in range(n)], id="hub")]
    spokes = [Task(f"h{i}", phase="Done", id=f"h{i}",
                   depends_on=[f"h{j}" for j in range(i + 1, min(n, i + 150))])
              for i in range(n)][::-1]
    for tasks in (chain, chain + many, dense, hub + spokes):
        b = Board([], tasks, tmp_path / "h.json")
        t0 = time.process_time()
        migrate_links(b)
        assert time.process_time() - t0 < 1.0
    # security S3-2: closed tasks linked FORWARD in board order. A chain stays
    # under 1 s (only a link to an already-processed task can close a loop); a
    # dense rotating board of 800 closed tasks × 400 links is the declared
    # exception, bounded at 2 s (D-526: paid once, at start)
    closed_chain = [Task(f"k{i}", phase="Done", id=f"k{i}",
                         depends_on=[f"k{i + 1}"] if i < 4999 else []) for i in range(5000)]
    rotating = [Task(f"r{i}", phase="Done", id=f"r{i}",
                     depends_on=[f"r{(i + k) % 800}" for k in range(1, 401)])
                for i in range(800)]
    for tasks, bound in ((closed_chain, 1.0), (rotating, 2.0)):
        b = Board([], tasks, tmp_path / "h.json", phases=["Doing", "Done"])
        t0 = time.process_time()
        migrate_links(b)
        assert time.process_time() - t0 < bound


# --------------------------------------------------------------------------- #
# TC-516 — at start, said once, undone with u (LLR-505.3)
# --------------------------------------------------------------------------- #
async def test_TC_516_one_toast_one_undo_step_mark_kept(tmp_path):
    """TC-516: one `Links migrated` toast in the house style; `u` once restores
    EVERY changed task (one step, D-517) and saves, and the mark stays; a task
    deleted since is skipped. RED: one undo entry per task; an undo that clears
    the mark (the migration would run again)."""
    path = tmp_path / "board.json"
    kg_board.legacy(path)
    stored = _state(path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        toasts = [t for t in _toasts(app) if "Links migrated" in t]
        assert len(toasts) == 1 and "6 tasks" in toasts[0] and "u undo" in toasts[0]
        app.board.tasks = [t for t in app.board.tasks if t.id != "L3"]   # gone since
        await pilot.press("u")
        await pilot.pause()
        for tid in kg_board.LEGACY_CHANGED - {"L3"}:
            t = app.board.task_by_id(tid)
            assert (t.blocked, t.depends_on) == (stored[tid][0], stored[tid][1]), tid
        assert any("migration undone" in t for t in _toasts(app))
    assert links_marked(Board.load(path).settings)
    assert _state(path)["L2"] == (True, ["to1", "to2"])


# --------------------------------------------------------------------------- #
# Layer B — the user's view of it
# --------------------------------------------------------------------------- #
async def test_AT_506_an_old_board_opens_migrated_once_with_its_backup(tmp_path):
    """AT-506 (US-505): a board file as the shipped app left it — no mark, no
    renumber key, an old done task the sweep will archive — opens migrated: the
    backup holds the file's bytes from BEFORE the start (its first name taken,
    so `.1`), the log lists the changed tasks, one toast names the backup; `u`
    reverts; a fresh app on the file the first one wrote (C-12) migrates nothing,
    shows no `Links migrated` toast and leaves the board, backup and log bytes as
    they were. RED on base: no migration — L2 keeps both ids and its flag."""
    path = tmp_path / "board.json"
    kg_board.legacy(path)
    raw = path.read_bytes()
    taken = path.with_name(path.name + MIGRATION_BACKUP)
    taken.write_bytes(b"x")
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        assert sum("Links migrated" in t for t in _toasts(app)) == 1
        backup = path.with_name(path.name + MIGRATION_BACKUP + ".1")
        assert backup.read_bytes() == raw
        after = _state(path)
        for tid, want in kg_board.LEGACY_AFTER.items():
            assert after[tid] == (want[0], want[1]), tid
        logs = [n for n in _beside(path) if MIGRATION_LOG in n]
        assert len(logs) == 1
        log = json.loads((tmp_path / logs[0]).read_text(encoding="utf-8"))
        assert {c["task_id"] for c in log["changes"]} == kg_board.LEGACY_CHANGED
        await pilot.press("u")
        await pilot.pause()
    assert _state(path)["L2"] == (True, ["to1", "to2"])
    listing = {n: (tmp_path / n).read_bytes() for n in _beside(path)}
    board_bytes = path.read_bytes()
    app2 = TaskboardApp(board_path=str(path))
    async with app2.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        assert not any("Links migrated" in t for t in _toasts(app2))
    assert path.read_bytes() == board_bytes
    assert {n: (tmp_path / n).read_bytes() for n in _beside(path)} == listing


async def test_AT_507_a_board_needing_no_change_is_only_marked(tmp_path):
    """AT-507 (US-505, empty branch): an old board whose links already read right
    (a released link to done work; a blocked task with no link) is marked and
    left — no backup, no log, no `Links migrated` toast. RED: a backup for
    nothing, or a toast that cries wolf."""
    path = tmp_path / "board.json"
    b = kg_board.legacy(path, old_done=False)
    b.tasks = [t for t in b.tasks if t.id in {"td1", "L4", "L6"}]
    b.save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        assert not any("Links migrated" in t for t in _toasts(app))
    assert not any(MIGRATION_BACKUP in n or MIGRATION_LOG in n for n in _beside(path))
    assert links_marked(Board.load(path).settings)
    assert _state(path)["L4"] == (False, ["td1"])


async def test_AT_508_a_backup_that_cannot_be_made_stops_the_app(tmp_path, monkeypatch, capsys):
    """AT-508 (US-505, error branch, D-518): when the backup cannot be created
    (the stdlib `open` refuses only names holding `.pre-links-migration`), the
    board file stays byte-identical and unmarked and the app exits, its message
    naming the file and the way out, no folder path. RED: a migration that goes
    on without its backup, or an app that opens on unmigrated links."""
    path = tmp_path / "board.json"
    kg_board.legacy(path)
    raw = path.read_bytes()
    real_open = builtins.open

    def failing_open(file, *a, **k):
        if MIGRATION_BACKUP in str(file):
            raise PermissionError(errno.EACCES, "Permission denied", str(file))
        return real_open(file, *a, **k)

    monkeypatch.setattr(builtins, "open", failing_open)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
    monkeypatch.setattr(builtins, "open", real_open)
    assert app.return_code == 1
    message = " ".join(capsys.readouterr().err.split())     # what the user reads
    assert "Link migration stopped" in message and "Permission denied" in message
    assert "--board" in message and str(tmp_path) not in message
    assert path.read_bytes() == raw
    assert not links_marked(Board.load(path).settings)


def _read_only(path: Path) -> None:
    os.chmod(path, stat.S_IREAD)
    if os.access(path, os.W_OK):            # e.g. root on POSIX: the bit binds nothing
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
        pytest.skip("this account writes through a read-only bit")


def test_TC_515_a_read_only_board_leaves_no_file_beside_it(tmp_path):
    """TC-515 (security close F1, operator D-530 "Corregirlo antes del push"): a
    read-only board file — on Windows the bit made the swap AND the temp file's
    cleanup fail, so every launch left a read-only `.board.json.<random>.tmp`
    copy and the error named the temp file. Law: the save is refused before
    anything is written; the backup and log this run made are removed; the board
    stays byte-identical and unmarked; the error names the BOARD; a second run
    leaves nothing more. RED: a temp file left per run; the temp file named."""
    path = tmp_path / "board.json"
    kg_board.legacy(path)
    raw = path.read_bytes()
    _read_only(path)
    try:
        for _ in range(2):
            result = run_link_migration(Board.load(path))
            assert result is not None and result.error is not None
            assert result.error.startswith("board.json:"), result.error
            assert _beside(path) == set(), _beside(path)
            assert path.read_bytes() == raw
    finally:
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
    assert not links_marked(Board.load(path).settings)


async def test_AT_508_a_read_only_board_stops_the_app_and_leaves_nothing(tmp_path, capsys):
    """AT-508 (D-530): starting on a read-only unmigrated board still fails closed —
    the app exits naming the board file and the way out — and leaves no temp,
    backup or log file beside it. RED: a temp file per launch."""
    path = tmp_path / "board.json"
    kg_board.legacy(path)
    raw = path.read_bytes()
    _read_only(path)
    try:
        app = TaskboardApp(board_path=str(path))
        async with app.run_test(size=(118, 30), notifications=True) as pilot:
            await pilot.pause()
        assert app.return_code == 1
        message = " ".join(capsys.readouterr().err.split())
        assert "Link migration stopped" in message and "board.json" in message
        assert str(tmp_path) not in message
        assert _beside(path) == set(), _beside(path)
        assert path.read_bytes() == raw
    finally:
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)


def test_TC_515_a_failed_swap_never_leaves_its_temp_file(tmp_path, monkeypatch):
    """TC-515 (D-530, the second guard): if the read-only bit is missed by the
    check (patched here to say "writable"), the swap fails and the temp file —
    which carries the copied read-only bit — is still removed, and the save's own
    error is the one reported. RED: a cleanup that cannot unlink a read-only temp
    file, or that masks the save's error."""
    if os.name != "nt":
        pytest.skip("only Windows refuses a swap onto a read-only file")
    path = tmp_path / "board.json"
    kg_board.legacy(path)
    raw = path.read_bytes()
    _read_only(path)
    monkeypatch.setattr(os, "access", lambda *a, **k: True)
    try:
        result = run_link_migration(Board.load(path))
        assert result is not None and result.error is not None
        assert _beside(path) == set(), _beside(path)
        assert path.read_bytes() == raw
    finally:
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
