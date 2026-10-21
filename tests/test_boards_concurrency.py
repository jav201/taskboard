"""Two taskboards at once, the move's history copy and `~` in the registry.

Batch 2026-10-20-batch-02: HLR-2301 / LLR-2301.1, LLR-2301.2 · TC-2301 · AT-2301
(US-2301); HLR-2302 / LLR-2302.1 · TC-2302 · AT-2302 (US-2301); HLR-2303 /
LLR-2303.1 · TC-2303 · AT-2303 (US-2302); HLR-2305 / LLR-2305.1 · TC-2305 · AT-2305
(US-2304). "Another taskboard" is the shipped `Registry` or a lock file acting on
the same files from the test — the code a second process runs. Synthetic data
only, under this test's own home.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import threading
import time
from datetime import date, datetime
from pathlib import Path

import pytest
from rich.text import Text

import multi_board_fixture as mb
from taskboard import boards, models, views
from taskboard.boards import Registry, move_plan, move_project, peek_board
from taskboard.models import Board, Project, Task

DAY = "2026-10-20"
NOW = datetime(2026, 10, 20, 9, 30)
SETTINGS = {"migrations": {"links": 1, "milestones": 1}, "seen_view_renumber_2026_07": True}


class _Today(date):
    @classmethod
    def today(cls):
        return mb.TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


@pytest.fixture
def home(tmp_path, monkeypatch):
    from taskboard import app as app_module, modals
    import taskboard.__main__ as entry
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    monkeypatch.setattr(app_module, "datetime", _Now)
    monkeypatch.setattr(entry, "datetime", _Now)
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.2, raising=False)
    return tmp_path / ".taskboard"


def _snap(*folders) -> dict:
    out = {}
    for f in folders:
        for p in sorted(Path(f).rglob("*")):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def _locks(root) -> list:
    return sorted(str(p) for p in Path(root).rglob("*.lock"))


def _age(path: Path, seconds: float) -> None:
    t = time.time() - seconds
    os.utime(path, (t, t))


def _ids(reg_path) -> list:
    return [e["id"] for e in json.loads(Path(reg_path).read_text(encoding="utf-8"))["boards"]]


def _open(board=None):
    from taskboard.__main__ import open_app
    return open_app(board)


async def _press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def _notes(app) -> list:
    return [str(n.message) for n in app._notifications]


# --------------------------------------------------------------------------- #
# TC-2301 — the lock (LLR-2301.1)
# --------------------------------------------------------------------------- #
def test_TC_2301_the_lock_is_exclusive_and_released(tmp_path, monkeypatch):
    """TC-2301: inside `file_lock` its lock file exists and a second taker waits
    `LOCK_WAIT` and is told the file is busy; after the block, or an exception in
    it, no lock file is left."""
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.2, raising=False)
    target = tmp_path / "boards.json"
    lock = tmp_path / "boards.json.lock"
    with boards.file_lock(target):
        assert lock.exists()
        t0 = time.monotonic()
        with pytest.raises(OSError) as err:
            with boards.file_lock(target):
                pass
        waited = time.monotonic() - t0
        assert 0.2 <= waited < 2, waited
        assert str(err.value).startswith("boards.json is busy — another taskboard is writing "
                                         "it; try again in a few seconds"), err.value
        assert lock.exists()                 # the waiter never removed the holder's lock
    assert not lock.exists()
    with pytest.raises(ZeroDivisionError):
        with boards.file_lock(target):
            1 / 0
    assert not lock.exists()
    with boards.file_lock(target, "Client · Retail RAG"):
        with pytest.raises(OSError) as err:
            with boards.file_lock(target, "Client · Retail RAG"):
                pass
    assert str(err.value).startswith("Client · Retail RAG is busy"), err.value


def test_TC_2301_a_stale_lock_is_taken_over_and_a_fresh_one_is_not(tmp_path, monkeypatch):
    """TC-2301: a lock file more than `LOCK_STALE` seconds old (or in the future —
    a skewed clock) is a dead instance's and is taken over at once; one younger
    is busy; a directory at the lock's name is never removed."""
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.2, raising=False)
    target = tmp_path / "board.json"
    lock = tmp_path / "board.json.lock"
    for age in (boards.LOCK_STALE + 1, -(boards.LOCK_STALE + 1)):
        lock.write_bytes(b"dead")
        _age(lock, age)
        t0 = time.monotonic()
        with boards.file_lock(target):
            assert lock.read_bytes() != b"dead"
        assert time.monotonic() - t0 < 0.2
        assert not lock.exists()
    lock.write_bytes(b"alive")
    _age(lock, boards.LOCK_STALE - 1)
    with pytest.raises(OSError):
        with boards.file_lock(target):
            pass
    assert lock.read_bytes() == b"alive"
    lock.unlink()
    lock.mkdir()
    _age(lock, boards.LOCK_STALE + 1)
    with pytest.raises(OSError):
        with boards.file_lock(target):
            pass
    assert lock.is_dir()


def test_TC_2301_a_lock_whose_token_cannot_be_written_is_removed(tmp_path, monkeypatch):
    """TC-2301 (security S-6): a failed token write leaves no lock behind."""
    def full(fd, data):
        raise OSError(28, "No space left on device")
    monkeypatch.setattr(boards.os, "write", full)
    with pytest.raises(OSError):
        with boards.file_lock(tmp_path / "boards.json"):
            pass
    assert not (tmp_path / "boards.json.lock").exists()


def test_TC_2301_a_taken_over_holder_never_removes_the_new_lock(tmp_path, monkeypatch):
    """TC-2301 (security S-2): a holder whose lock was taken over leaves the new
    holder's lock in place on exit."""
    target = tmp_path / "boards.json"
    lock = tmp_path / "boards.json.lock"
    with boards.file_lock(target):
        lock.write_bytes(b"another holder's token")
    assert lock.read_bytes() == b"another holder's token"


# --------------------------------------------------------------------------- #
# TC-2301 — the registry's read-modify-write (LLR-2301.2)
# --------------------------------------------------------------------------- #
def _two(home):
    reg_path = mb.build(home, "personal")
    main = home / "board.json"
    return reg_path, Registry.load(reg_path, main), Registry.load(reg_path, main)


def test_TC_2301_a_stale_registry_keeps_the_other_writers_board(home):
    """TC-2301 (HLR-2301): B loaded before A created a board; every one of B's
    writers keeps A's board and every earlier change, and B ends up holding the
    file's entries, its own objects updated in place."""
    reg_path, a, b = _two(home)
    a.create("From A", "lime", NOW, SETTINGS)
    obj = b.get("course-docker")
    b.edit("course-docker", "Docker course", "blue")
    assert "from-a" in _ids(reg_path) and b.get("course-docker") is obj
    assert obj.name == "Docker course"
    b.archive("client-retail-rag")
    side = b.register(home / "side" / "notes.json")
    made = b.create("From A", "sky", NOW, SETTINGS)
    assert made.id == "from-a-2"
    a.register(home / "ext" / "made-by-a.json")   # an id only the file holds: no folder (F1)
    assert b.create("Made by A", "sky", NOW, SETTINGS).id == "made-by-a-2"   # the file's ids
    b.touch("personal", NOW)
    on_disk = json.loads(reg_path.read_text(encoding="utf-8"))
    by = {e["id"]: e for e in on_disk["boards"]}
    assert set(by) == {"personal", "client-retail-rag", "course-docker", "main", "from-a",
                       "made-by-a", "notes", "from-a-2", "made-by-a-2"}, set(by)
    assert by["course-docker"]["name"] == "Docker course"
    assert by["client-retail-rag"]["archived"] is True
    assert side.id == "notes" and on_disk["last"] == "personal"
    assert [(e.id, e.name, e.archived) for e in b.entries] == \
        [(e["id"], e["name"], e["archived"]) for e in on_disk["boards"]]
    a.edit("from-a", "A's board", "green")       # A, stale in turn, keeps B's changes
    assert set(_ids(reg_path)) == set(by)
    assert {e["id"]: e["archived"] for e in json.loads(
        reg_path.read_text(encoding="utf-8"))["boards"]}["client-retail-rag"] is True
    assert _locks(home) == []


def test_TC_2301_an_entry_only_memory_holds_keeps_its_id_and_file(home):
    """TC-2301 (code review F5): a board registered while memory holds an entry the
    file lacks takes another id, so the entry the app holds keeps its file."""
    reg_path, _a, b = _two(home)
    mine = str(home / "elsewhere" / "notes.json")
    b.entries.append(boards.BoardEntry("notes", "notes", "lime", mine))
    made = b.register(home / "other" / "notes.json")
    assert made.id == "notes-2", made.id
    assert b.get("notes").path == mine
    assert "notes-2" in _ids(reg_path)


def test_TC_2301_a_failed_write_changes_nothing(home, monkeypatch):
    """TC-2301: a busy lock or a failing save leaves memory and disk as they were;
    `create` removes the folder it made, and only it."""
    reg_path, _a, b = _two(home)
    before = [(e.id, e.name, e.color, e.archived) for e in b.entries]
    old = reg_path.read_bytes()
    (home / "boards.json.lock").write_bytes(b"x")
    assert boards.LOCK_WAIT == 0.2
    for name, call in (("create", lambda: b.create("Late", "lime", NOW, SETTINGS)),
                       ("edit", lambda: b.edit("course-docker", "Other", "blue")),
                       ("archive", lambda: b.archive("client-retail-rag")),
                       ("register", lambda: b.register(home / "x" / "board.json"))):
        with pytest.raises(OSError) as err:
            call()
        assert "boards.json is busy" in str(err.value), (name, err.value)
        assert reg_path.read_bytes() == old, name
        assert [(e.id, e.name, e.color, e.archived) for e in b.entries] == before, name
        assert not (home / "boards" / "late").exists(), name
    (home / "boards.json.lock").unlink()
    real = Registry.save

    def boom(self):
        raise PermissionError("locked")
    monkeypatch.setattr(Registry, "save", boom)
    with pytest.raises(OSError):
        b.create("Late", "lime", NOW, SETTINGS)
    assert not (home / "boards" / "late").exists()
    monkeypatch.setattr(Registry, "save", real)
    assert [(e.id, e.name, e.color, e.archived) for e in b.entries] == before
    assert reg_path.read_bytes() == old and _locks(home) == []


def test_TC_2301_an_unreadable_registry_is_never_written_over_without_a_copy(home, monkeypatch):
    """TC-2301 (security S-1): unparseable since this registry read it → the bytes
    copied aside first, then written; a read that fails, or a copy that cannot be
    made → nothing written."""
    reg_path, _a, b = _two(home)
    reg_path.write_bytes(b"{not json")
    b.edit("course-docker", "Docker course", "blue")
    assert (home / "boards.json.corrupt").read_bytes() == b"{not json"
    assert b.get("course-docker").name == "Docker course" and "personal" in _ids(reg_path)
    reg_path.write_bytes(b"[1, 2")
    monkeypatch.setattr(boards, "keep_aside", lambda path: None)
    with pytest.raises(OSError):
        b.edit("course-docker", "Again", "blue")
    assert reg_path.read_bytes() == b"[1, 2"
    reg_path.write_text(json.dumps({"boards": []}), encoding="utf-8")
    real = Path.read_bytes

    def denied(self):
        if self.name == "boards.json":
            raise PermissionError("sharing violation")
        return real(self)
    monkeypatch.setattr(Path, "read_bytes", denied)
    with pytest.raises(OSError):
        b.archive("course-docker")
    monkeypatch.setattr(Path, "read_bytes", real)
    assert json.loads(reg_path.read_text(encoding="utf-8")) == {"boards": []}


def test_TC_2301_a_one_board_start_takes_no_lock_and_writes_nothing(home):
    """TC-2301: the one-board user with no registry file gets neither `boards.json`
    nor a lock file at an opening."""
    main = home / "board.json"
    reg = Registry.load(home / "boards.json", main)
    reg.touch("main", NOW)
    assert not home.exists() or sorted(p.name for p in home.iterdir()) == []


def test_TC_2301_a_busy_registry_at_start_is_a_message_not_a_traceback(home, monkeypatch,
                                                                     capsys):
    """TC-2301 (ux UX-4, architect A-4): `taskboard --board PATH` while the
    registry is busy exits with the reason, no traceback."""
    from taskboard import __main__ as entry
    mb.build(home, "personal")
    (home / "boards.json.lock").write_bytes(b"x")
    old = (home / "boards.json").read_bytes()
    monkeypatch.setattr(sys, "argv", ["taskboard", "--board", str(home / "new" / "b.json")])
    from taskboard.app import TaskboardApp
    monkeypatch.setattr(TaskboardApp, "run", lambda self, *a, **k: None)   # never a live TUI
    with pytest.raises(SystemExit) as err:
        entry.main()
    assert err.value.code == 1
    out = capsys.readouterr().err
    assert out.startswith("taskboard: boards.json is busy"), out
    assert "Traceback" not in out
    assert (home / "boards.json").read_bytes() == old


async def test_AT_2301_a_board_another_taskboard_made_survives(home):
    """AT-2301 (US-2301): while the app runs another taskboard adds `Other desk`;
    the operator creates `Fresh` from the home; both are in `boards.json` and on
    the home. With the registry busy, the create says so and writes nothing."""
    reg_path = mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45), notifications=True) as pilot:
        await pilot.pause()
        Registry.load(reg_path, home / "board.json").create("Other desk", "sky", NOW, SETTINGS)
        await _press(pilot, "n")
        await _press(pilot, *"Fresh")                 # typed (qa QA-11)
        await _press(pilot, "tab", "enter")
        assert {"other-desk", "fresh", "personal", "client-retail-rag", "course-docker",
                "main"} <= set(_ids(reg_path)), _ids(reg_path)
        await _press(pilot, "B")
        titles = [Text.from_markup(c.border_title).plain.lstrip("▶ ")
                  for c in app.screen.query("BoardCard")]
        assert "Other desk" in titles and "Fresh" in titles, titles
        (home / "boards.json.lock").write_bytes(b"another taskboard")
        old = reg_path.read_bytes()
        await _press(pilot, "n")
        await _press(pilot, *"Late")
        await _press(pilot, "tab", "enter")
        assert any(m.startswith("The board was not created: boards.json is busy")
                   for m in _notes(app)), _notes(app)
        assert reg_path.read_bytes() == old and not (home / "boards" / "late").exists()
        assert (home / "boards.json.lock").read_bytes() == b"another taskboard"
        (home / "boards.json.lock").unlink()
    assert _locks(home) == []


# --------------------------------------------------------------------------- #
# TC-2302 — the move holds its target (LLR-2302.1)
# --------------------------------------------------------------------------- #
def _pair(home):
    mb.build(home, "main")
    return home / "board.json", home / "boards" / "client-retail-rag" / "board.json"


def test_TC_2302_a_busy_target_stops_the_move_before_anything(home):
    src_p, dst_p = _pair(home)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    dst_p.with_name("board.json.lock").write_bytes(b"x")
    before = _snap(home)
    with pytest.raises(OSError) as err:
        move_project(src, dst, "pmr", plan, DAY, ("Main", "Client · Retail RAG"))
    assert str(err.value).startswith("Client · Retail RAG is busy"), err.value
    assert err.value.steps == [] and err.value.board is None
    assert _snap(home) == before


def test_TC_2302_a_target_rewritten_while_the_move_waited_is_refused(home, monkeypatch):
    """TC-2302 (qa QA-8): another taskboard holds the target's lock and rewrites
    the target; the move, waiting for the lock, sees the change once it holds it
    and refuses — the other's write kept, nothing written, no lock left."""
    src_p, dst_p = _pair(home)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    held = threading.Event()
    monkeypatch.setattr(boards, "LOCK_WAIT", 2.0)   # room for the other's hold on a loaded host (F2)

    def other():
        with boards.file_lock(dst_p):
            held.set()
            time.sleep(0.05)
            data = json.loads(dst_p.read_text(encoding="utf-8"))
            data["projects"].append({"id": "pzz", "name": "Written by the other"})
            dst_p.write_text(json.dumps(data), encoding="utf-8")
            time.sleep(0.1)
    t = threading.Thread(target=other)
    t.start()
    held.wait(1)
    with pytest.raises(OSError) as err:
        move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    t.join()
    assert "changed since the move was planned" in str(err.value), err.value
    assert err.value.steps == [] and err.value.board is None
    ids = [p["id"] for p in json.loads(dst_p.read_text(encoding="utf-8"))["projects"]]
    assert "pzz" in ids and "pmr" not in ids
    assert not list(home.rglob("*.pre-move-*")) and _locks(home) == []


def test_TC_2302_the_lock_is_held_for_the_target_save_only(home, monkeypatch):
    src_p, dst_p = _pair(home)
    lock = dst_p.with_name("board.json.lock")
    seen = {}
    real = Board.save_atomic

    def spy(self):
        seen[self.path] = lock.exists()
        real(self)
    monkeypatch.setattr(Board, "save_atomic", spy)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert seen == {dst_p: True, src_p: False}, seen
    assert _locks(home) == []


def test_TC_2302_a_stale_target_lock_is_taken_over(home):
    src_p, dst_p = _pair(home)
    lock = dst_p.with_name("board.json.lock")
    lock.write_bytes(b"dead")
    _age(lock, boards.LOCK_STALE + 1)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert "pmr" in {p["id"] for p in json.loads(dst_p.read_text(encoding="utf-8"))["projects"]}
    assert _locks(home) == []


async def test_AT_2302_a_move_into_a_busy_board_stops_before_writing(home):
    """AT-2302 (US-2301): the target's lock held by another taskboard → the move
    stops at `enter`, names the board as busy, claims no backup and writes
    nothing; once free, the same keys move the project and leave no lock."""
    src_p, dst_p = _pair(home)
    lock = dst_p.with_name("board.json.lock")
    app = _open()
    async with app.run_test(size=(160, 45), notifications=True) as pilot:
        await pilot.pause()
        await _press(pilot, "escape", "P", "down", "m", "down", "enter")
        assert type(app.screen).__name__ == "MoveConfirm"
        lock.write_bytes(b"another taskboard")
        before = _snap(home)
        await _press(pilot, "y")               # y confirms (batch-03, ux UX-2)
        msg = next(m for m in _notes(app) if m.startswith("The move stopped"))
        assert msg.startswith("The move stopped: Client · Retail RAG is busy"), msg
        assert "Done: nothing." in msg and "backups" not in msg, msg
        assert _snap(home) == before
        lock.unlink()
        await _press(pilot, "m", "down", "enter", "y")   # y confirms (batch-03)
        assert any(m.startswith("Moved Retail RAG · pilot to Client · Retail RAG")
                   for m in _notes(app)), _notes(app)
    assert len([p for p in json.loads(dst_p.read_text(encoding="utf-8"))["tasks"]
                if p["project_id"] == "pmr"]) == 7
    assert _locks(home) == []


# --------------------------------------------------------------------------- #
# TC-2303 — the history copy (LLR-2303.1)
# --------------------------------------------------------------------------- #
HIST = b'{"task": "tr3", "to": "Doing"}\n\xff\xfe kept\n'


def test_TC_2303_the_history_is_copied_with_the_board_files(home):
    src_p, dst_p = _pair(home)
    hist = src_p.parent / "history.jsonl"
    hist.write_bytes(HIST)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    _new, steps = move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert steps[:3] == ["copied board.json", "copied board.json", "copied history.jsonl"]
    assert hist.with_name(f"history.jsonl.pre-move-{DAY}").read_bytes() == HIST
    assert b"tr3" not in hist.read_bytes()                       # rewritten after the copy
    assert not list(dst_p.parent.glob("history.jsonl.pre-move-*"))
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pma", set(), set())
    move_project(src, dst, "pma", plan, DAY, ("Main", "Client"))
    assert hist.with_name(f"history.jsonl.pre-move-{DAY}").read_bytes() == HIST
    assert hist.with_name(f"history.jsonl.pre-move-{DAY}-2").exists()


def test_TC_2303_no_history_no_copy_and_a_failed_save_keeps_the_copy(home, monkeypatch):
    src_p, dst_p = _pair(home)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    _new, steps = move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert "copied history.jsonl" not in steps
    assert not list(src_p.parent.glob("history.jsonl*"))
    hist = src_p.parent / "history.jsonl"
    hist.write_bytes(HIST)
    real = Board.save_atomic

    def fail_dst(self):
        if self.path == dst_p:
            raise OSError("disk full")
        real(self)
    monkeypatch.setattr(Board, "save_atomic", fail_dst)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pma", set(), set())
    with pytest.raises(OSError):
        move_project(src, dst, "pma", plan, DAY, ("Main", "Client"))
    assert hist.read_bytes() == HIST
    assert hist.with_name(f"history.jsonl.pre-move-{DAY}").read_bytes() == HIST
    assert _locks(home) == []


def test_TC_2303_a_copy_failing_midway_leaves_no_copy(home, monkeypatch):
    """TC-2303 (security S-5): the copy is streamed; one that fails midway is
    removed, so no partial file looks like a whole copy."""
    src_p, dst_p = _pair(home)
    hist = src_p.parent / "history.jsonl"
    hist.write_bytes(HIST)

    def half(src, out):
        out.write(src.read(5))
        raise OSError(28, "No space left on device")
    monkeypatch.setattr(boards.shutil, "copyfileobj", half)
    with pytest.raises(OSError):
        boards._backup(hist, DAY)
    assert not list(src_p.parent.glob("history.jsonl.pre-move-*"))


async def test_AT_2303_a_move_keeps_the_source_history_bytes(home):
    """AT-2303 (US-2302): after a move by keys the source folder keeps the
    history's original bytes, the undecodable ones too."""
    src_p, dst_p = _pair(home)
    (src_p.parent / "history.jsonl").write_bytes(HIST)
    app = _open()
    async with app.run_test(size=(160, 45), notifications=True) as pilot:
        await pilot.pause()
        await _press(pilot, "escape", "P", "down", "m", "down", "enter", "y")   # y confirms (batch-03)
        assert any(m.startswith("Moved Retail RAG · pilot") for m in _notes(app)), _notes(app)
    assert (src_p.parent / f"history.jsonl.pre-move-{DAY}").read_bytes() == HIST
    assert not list(dst_p.parent.glob("history.jsonl.pre-move-*"))


# --------------------------------------------------------------------------- #
# TC-2305 — `~` through Path.home() (LLR-2305.1)
# --------------------------------------------------------------------------- #
@pytest.fixture
def env_home(tmp_path, monkeypatch):
    """The environment's home, somewhere else than `Path.home()`."""
    other = tmp_path / "env-home"
    other.mkdir()
    for var in ("HOME", "USERPROFILE"):
        monkeypatch.setenv(var, str(other))
    return other


def test_TC_2305_tilde_is_the_seam_home(home, env_home):
    seam = Path.home()
    assert seam != env_home
    assert boards._expand_home("~") == seam
    assert boards._expand_home("~/a/b") == seam / "a" / "b"
    if os.name == "nt":
        assert boards._expand_home("~\\a") == seam / "a"
    assert boards._expand_home("~user/a") == Path("~user/a")
    assert boards._key("~/x") == os.path.normcase(str((seam / "x").resolve()))
    reg_path = home / "boards.json"
    home.mkdir(parents=True)
    reg_path.write_text(json.dumps({"boards": [
        {"id": "main", "name": "Main", "path": str(home / "board.json")},
        {"id": "side", "name": "Side", "path": "~/side/board.json"},
        {"id": "other", "name": "Other", "path": "~user/board.json"}]}), encoding="utf-8")
    reg = Registry.load(reg_path, home / "board.json")
    assert [e.id for e in reg.entries] == ["main", "side"]       # `~user` is relative
    assert reg.get("side").path == str(seam / "side" / "board.json")
    assert reg.entry_for(seam / "side" / "board.json") is reg.get("side")
    made = reg.register("~/n.json")
    assert Path(made.path) == (seam / "n.json").resolve()
    src = (Path(boards.__file__)).read_text(encoding="utf-8")
    assert ".expanduser(" not in src


async def test_AT_2305_a_tilde_board_opens_from_the_seam_home(home, env_home):
    """AT-2305 (US-2304): a `~` board on the home opens the seam home's file,
    never the environment's."""
    seam = Path.home()
    for root, word in ((seam, "Seam"), (env_home, "Env")):
        p = root / ".taskboard" / "side" / "board.json"
        p.parent.mkdir(parents=True)
        Board([Project(f"{word} board", id="ps")],
              [Task(f"{word} task", id="ts", project_id="ps", phase="Next")], p,
              dict(SETTINGS)).save()
    Board([Project("Main work", id="pm")], [Task("Main task", id="tm", project_id="pm")],
          home / "board.json", dict(SETTINGS)).save()
    (home / "boards.json").write_text(json.dumps({"last": "main", "boards": [
        {"id": "main", "name": "Main", "path": str(home / "board.json")},
        {"id": "side", "name": "Side", "path": "~/.taskboard/side/board.json"}]}),
        encoding="utf-8")
    env_before = _snap(env_home)
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        for _ in range(3):
            await pilot.pause()
        assert type(app.screen).__name__ == "BoardsHome"
        await _press(pilot, "right", "enter")
        body = app.query_one("#board").content.plain
        assert "Seam task" in body and "Env task" not in body, body
    assert _snap(env_home) == env_before
