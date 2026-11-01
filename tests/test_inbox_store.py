"""The capture view's store `inbox.json`, its note parse, the undo of a dump and the image
files of a note (Inc K, dev-flow-v3-beta).

HLR-4402 layer 0 (LLR-4402.1..4402.5, .8; the store side of .14 and .16) · HLR-4405 layer 0
(LLR-4405.1..4405.12 board side, .17, .18, .19) · HLR-4407 all (LLR-4407.1..4407.25,
.27..4407.29, .35..4407.49; layer 0 and pilot) · HLR-4408 layer 0 (LLR-4408.1..4408.3,
.5..4408.7, .10..4408.13, .15..4408.20) · HLR-4409 layer 0 (LLR-4409.2, .3, .5).
AT-4406 and AT-4408 are in tests/test_capture_view.py (the black-box file).

WHY. The owner (`username_subject`) captures notes in a hurry, during a meeting: a note typed
into the pad must NEVER be lost — not to a second window writing the same store (the
note-level union, ARCH-1/SEC-1), not to a failed write (the pad and a dump's record are kept
in memory and retried, ARCH-4), not to a close or an exit (written first), not to a corrupt
file (set aside before anything is written over it). And the store must never corrupt the
boards or the other stores: it is written only under its own lock, atomically, capped in
size, refusing text that will not encode; a dump writes one task into one board file and
leaves every other task's bytes, `people.json` and `marks.json` as they were; an undo
removes only a task that is exactly as its dump wrote it, and only on a known board; image
files are copied from the user's own clipboard file, never moved, and never removed through
a link or a junction.

Layer 0 drives `taskboard.inbox` on fixture S (`capture_fixture.build_s`: Client A and Course
under a temporary folder, new task ids t0000001, …); the pilots drive the shipped app on
fixture F (`capture_fixture.build_f`, `Path.home` redirected) at 118x30 through its keys.

RED on the base revision (545c18a): `taskboard.inbox` does not exist, `TaskboardApp` holds no
`inbox`, and `n` opens nothing. Every new name is reached through `capture_fixture.inbox()` /
`need()`, and every pilot asserts the capture view opened right after `n`
(`capture_fixture.open_capture`), so each test fails on an assertion with a message — never
a collection error. No test of this module is a guard: every one is RED on base.

Synthetic data only; owner `username_subject`. The store's own 7-day keep reads the real
clock, so every dumped entry a write must keep is stamped relative to `datetime.now()`.
"""
from __future__ import annotations

import builtins
import contextlib
import inspect
import io
import json
import os
import shutil
import textwrap
from datetime import datetime, timedelta
from pathlib import Path

import pytest

import capture_fixture as fx
from capture_fixture import home  # noqa: F401
from taskboard import app as app_module, boards, models, views
from taskboard.boards import peek_board
from taskboard.models import Board, Task

NOW = datetime(2026, 11, 1, 10, 2, 0)
CAP = 8_388_608
NOTE_A = "Volume lab fails on WSL\nthe oracle script expects /mnt/c\nimg: board-0938.png"
NOTE_A_TEXT = "Volume lab fails on WSL\nthe oracle script expects /mnt/c"
DIVIDER_NOTICE = ("That ____ line divides notes: the text above and below it dump as two "
                  "tasks. alt+l inserts one.")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _f(name):
    return fx.need("inbox", name)


def _I():
    return _f("Inbox")


def _load(path):
    return _I().load(Path(path))


def _e(text, task, board="S/c/board.json", project="pm", at=None, images=(),
       new_project=False, title=None):
    return fx.entry(text, task, title or text.split("\n")[0], board, project, at=at,
                    new_project=new_project, images=images)


def _store(folder) -> dict:
    return fx.read_store(folder)


def _bytes(path) -> bytes | None:
    p = Path(path)
    return p.read_bytes() if p.exists() else None


def _texts(parts) -> list[str]:
    return [p.text for p in parts if p.is_note]


def _tup(p) -> tuple:
    return (p.start, p.end, p.text, p.is_note)


def _patch_write_atomic(monkeypatch, fn):
    monkeypatch.setattr(models, "write_atomic", fn)
    monkeypatch.setattr(fx.inbox(), "write_atomic", fn, raising=False)


def _fail_store(monkeypatch, times: int = 1, message: str = "disk full") -> dict:
    """`write_atomic` raises OSError for `inbox.json` the next `times` calls (a board's
    `save_atomic` passes through); counts every store write attempt."""
    real = models.write_atomic
    box = {"left": times, "calls": 0}

    def w(path, text):
        if Path(path).name == "inbox.json":
            box["calls"] += 1
            if box["left"] > 0:
                box["left"] -= 1
                raise OSError(message)
        return real(path, text)
    _patch_write_atomic(monkeypatch, w)
    return box


def _spy_store_writes(monkeypatch) -> list:
    """Each `write_atomic` call on `inbox.json`: (path, the store's lock existed then)."""
    real = models.write_atomic
    calls = []

    def w(path, text):
        if Path(path).name == "inbox.json":
            lock = Path(path).resolve()
            calls.append((Path(path), lock.with_name(lock.name + ".lock").exists()))
        return real(path, text)
    _patch_write_atomic(monkeypatch, w)
    return calls


def _hold_lock(path, monkeypatch, wait: float = 0.3) -> Path:
    """A fresh foreign `<file>.lock` (another taskboard holds it); `LOCK_WAIT` cut to `wait`."""
    monkeypatch.setattr(boards, "LOCK_WAIT", wait)
    lock = Path(path).resolve()
    lock = lock.with_name(lock.name + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_bytes(b"0123456789abcdef0123456789abcdef")
    return lock


def _patch_keep_aside_none(monkeypatch):
    monkeypatch.setattr(boards, "keep_aside", lambda path: None)
    monkeypatch.setattr(fx.inbox(), "keep_aside", lambda path: None, raising=False)


def _wrap_read(monkeypatch, raise_times: int = 0) -> dict:
    """Wrap `Inbox._read` (static per graph-proto-S): count its calls, raise OSError the
    first `raise_times` calls."""
    Inbox = _I()
    raw = inspect.getattr_static(Inbox, "_read")
    fn = raw.__func__ if isinstance(raw, (staticmethod, classmethod)) else raw
    box = {"calls": 0, "left": raise_times}

    def w(*a, **k):
        box["calls"] += 1
        if box["left"] > 0:
            box["left"] -= 1
            raise OSError("the file is in use by another process")
        return fn(*a, **k)
    monkeypatch.setattr(Inbox, "_read", staticmethod(w) if isinstance(raw, staticmethod) else w)
    return box


def _store_of_size(n: int) -> str:
    """A VALID store whose UTF-8 text is exactly `n` bytes."""
    base = len(json.dumps({"version": 1, "pad": "", "dumped": []}, indent=2).encode())
    text = json.dumps({"version": 1, "pad": "a" * (n - base), "dumped": []}, indent=2)
    assert len(text.encode()) == n
    return text


def _fail_open(m, times: int, name: str = "inbox.json") -> dict:
    """`open` / `io.open` of a file named `name` raises OSError the next `times` calls (the
    store held open by another process); every other open goes through."""
    real = io.open
    box = {"left": times}

    def failing(file, *a, **k):
        try:
            hit = Path(os.fsdecode(file)).name == name
        except TypeError:
            hit = False
        if hit and box["left"] > 0:
            box["left"] -= 1
            raise OSError("the file is in use by another process")
        return real(file, *a, **k)
    m.setattr(builtins, "open", failing)
    m.setattr(io, "open", failing)
    return box


def _count_reads(m, name: str = "inbox.json") -> dict:
    """Count the bytes read from any file named `name` through `open` / `io.open`
    (`Path.open` and `Path.read_bytes` go through `io.open`)."""
    real = io.open
    box = {"bytes": 0}

    class _Counting:
        def __init__(self, fh):
            self._fh = fh

        def read(self, *a):
            data = self._fh.read(*a)
            box["bytes"] += len(data)
            return data

        def readinto(self, b):
            n = self._fh.readinto(b)
            box["bytes"] += n or 0
            return n

        def __enter__(self):
            self._fh.__enter__()
            return self

        def __exit__(self, *a):
            return self._fh.__exit__(*a)

        def __iter__(self):
            return iter(self._fh)

        def __getattr__(self, a):
            return getattr(self._fh, a)

    def spy(file, *a, **k):
        fh = real(file, *a, **k)
        try:
            hit = Path(os.fsdecode(file)).name == name
        except TypeError:
            hit = False
        return _Counting(fh) if hit else fh
    m.setattr(builtins, "open", spy)
    m.setattr(io, "open", spy)
    return box


def _png(path: Path, data: bytes = b"\x89PNG\r\n\x1a\nsynthetic") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _pil(w=2, h=2):
    try:
        from PIL import Image
    except ImportError:
        pytest.skip("Pillow is not installed here")
    return Image.new("RGB", (w, h), (10, 20, 30))


def _target(s, which="C", live=None):
    name = "Course" if which == "C" else "Client A"
    return _f("DumpTarget")(s[which], name, live)


def _dump(s, note, which="C", project="pm", new_name=None, live=None,
          project_name="Module 4 · Volumes"):
    return _f("dump_note")(_target(s, which, live), None if new_name else project, new_name,
                           note, s["F"], "" if new_name else project_name)


def _entry_of(out, note, board_path):
    return _f("entry_for")(out, note, Path(board_path), datetime.now())


def _task_rec(path, tid) -> dict | None:
    return next((t for t in fx.tasks_of(path) if t["id"] == tid), None)


def _edit_board(path, fn) -> None:
    """Another writer: read the board, change it, save it atomically."""
    b = Board.load(path)
    fn(b)
    b.save_atomic()


def _junction(target: Path, link: Path) -> None:
    try:
        import _winapi
        _winapi.CreateJunction(str(target), str(link))
    except Exception as exc:          # not Windows, or no junction support here
        pytest.skip(f"cannot create a junction here: {exc}")


def _inbox_of(app):
    inb = getattr(app, "inbox", None)
    assert inb is not None, "TaskboardApp holds no `inbox` (not built yet)"
    return inb


async def _capture(pilot, app):
    await fx.leave_home(pilot)
    return await fx.open_capture(pilot, app)


def _one(app, text: str, severity: str | None = "warning"):
    got = fx.notified(app, text)
    assert len(got) == 1, f"expected one notice {text!r}, got {fx.messages(app)}"
    n = got[0]
    assert n.title == "Capture" and n.markup is False, (n.title, n.markup)
    if severity:
        assert n.severity == severity, n.severity
    return n


def _pad(app) -> str:
    return fx.pad_of(app).text


# =========================================================================== #
# HLR-4402 layer 0 — the parse
# =========================================================================== #
def test_TC_4431_a_divider_is_four_or_more_underscores_and_nothing_else():
    """TC-4431 (LLR-4402.1): trailing whitespace allowed, leading not, 4 or more `_` only.
    NC `_{3,}`: the `___` arm RED."""
    is_divider = _f("is_divider")
    for line in ("____", "________", "____  "):
        assert is_divider(line) is True, line
    for line in ("___", " ____", "____x", "__ __"):
        assert is_divider(line) is False, line


def test_TC_4432_the_pad_splits_into_parts_at_divider_lines():
    """TC-4432 (LLR-4402.2): a divider line belongs to no part; two adjacent dividers hold an
    empty part. NC divider lines kept inside parts: RED."""
    parts = _f("note_parts")("a\nb\n____\nc")
    assert [_tup(p) for p in parts] == [(0, 1, "a\nb", True), (3, 3, "c", True)]
    parts = _f("note_parts")("a\n____\n____\nb")
    assert len(parts) == 3
    assert [_tup(p) for p in parts] == [(0, 0, "a", True), (2, 1, "", False), (3, 3, "b", True)]


def test_TC_4433_blank_lines_stay_inside_a_note():
    """TC-4433 (LLR-4402.3): a blank line does not split (NC: the proto's `split_topics`
    gives 3 notes)."""
    parts = _f("note_parts")("a\n\nb\n____\nc")
    assert _texts(parts) == ["a\n\nb", "c"]
    assert [_tup(p) for p in parts] == [(0, 2, "a\n\nb", True), (4, 4, "c", True)]


def test_TC_4434_a_whitespace_only_part_is_not_a_note():
    """TC-4434 (LLR-4402.4): `"____\\n  \\n____\\na"` → 1 note; with a tab the parts are exact.
    NC every part a note: RED."""
    assert _texts(_f("note_parts")("____\n  \n____\na")) == ["a"]
    parts = _f("note_parts")("____\n \t\n____\na")
    assert [_tup(p) for p in parts] == [(0, -1, "", False), (1, 1, "", False),
                                        (3, 3, "a", True)]


def test_TC_4435_a_notes_text_drops_its_outer_blank_lines():
    """TC-4435 (LLR-4402.5): `"\\n\\na\\n\\n____"` → the note's text is `a`. NC no trim: RED."""
    parts = _f("note_parts")("\n\na\n\n____")
    assert _texts(parts) == ["a"]
    assert [_tup(p) for p in parts] == [(0, 3, "a", True), (5, 4, "", False)]


@pytest.mark.parametrize("text, count", [("a\n____", 1), ("a\n____\n", 2),
                                         ("a\n____\n\n____\nb", 2), ("a", 1), ("", 0)])
def test_TC_4438_the_count_adds_the_note_being_started_after_a_final_divider(text, count):
    """TC-4438 (LLR-4402.8): `enter` after a final divider starts a note the head counts;
    an inner empty part is not counted. NC count notes only: the `a\\n____\\n` arm RED."""
    assert _f("note_count")(text) == count


def test_TC_4530b_the_cursors_note_on_a_divider_is_the_note_above():
    """TC-4530b (LLR-4404.30, layer 0 of note_at): row 1 (the divider) → `a`; row 2 → `b`;
    a divider with no note above → None. NC divider → the note below: RED."""
    note_at = _f("note_at")
    assert note_at("a\n____\nb", 1).text == "a"
    assert note_at("a\n____\nb", 2).text == "b"
    assert note_at("____\na", 0) is None


def test_TC_4528b_no_note_under_the_cursor_is_none():
    """TC-4528b (LLR-4404.28, layer 0): an empty pad, a whitespace part after a divider and a
    row outside the pad → None (the view's "No note under the cursor."; NC the proto's
    `cur()` picks the last note)."""
    note_at = _f("note_at")
    assert note_at("", 0) is None
    assert note_at("a\n____\n  ", 2) is None
    assert note_at("a", 5) is None


def test_TC_4506b_a_dumped_note_leaves_with_one_adjacent_divider():
    """TC-4506b (LLR-4404.6, layer 0 of without_note): the divider after the note, else the
    one before; every other line byte-identical. NC leave the divider: RED."""
    parts = _f("note_parts")
    without = _f("without_note")
    text = "a\n____\nb\n____\nc"
    p = {x.text: x for x in parts(text) if x.is_note}
    assert without(text, p["b"])[0] == "a\n____\nc"
    assert without(text, p["c"]) == ("a\n____\nb", 2)
    assert without(text, p["a"]) == ("b\n____\nc", 0)
    text2 = "a\n____\n\nb\n\n____\nc"
    pb = next(x for x in parts(text2) if x.is_note and x.text == "b")
    assert (pb.start, pb.end) == (2, 4)
    assert without(text2, pb)[0] == "a\n____\nc"
    only = next(x for x in parts("solo") if x.is_note)
    assert without("solo", only) == ("", 0)


def test_TC_4543b_a_restored_note_follows_a_new_divider():
    """TC-4543b (LLR-4405.3, layer 0 of with_note, P-S-14): after a new `____` when the pad
    holds text; alone in an empty pad; trailing blank lines dropped; a pad ending in a
    divider takes the note in the part being started. NC no divider: `a\\nb`: RED."""
    with_note = _f("with_note")
    assert with_note("a", "b") == "a\n____\nb"
    assert with_note("", "b") == "b"
    assert with_note("a\n", "b") == "a\n____\nb"
    assert with_note("a\n____\n", "b") == "a\n____\nb"


# --------------------------------------------------------------------------- #
# LLR-4402.14 / LLR-4402.16 — the store side of the divider
# --------------------------------------------------------------------------- #
def test_TC_4444_the_divider_notice_flag_is_written_to_the_store(tmp_path):
    """TC-4444 (LLR-4402.14): mark_notice writes `"divider_notice": true` and keeps the pad
    the FILE holds; P-S-5: when another window changed the file first, this window does not
    adopt its stamp, so its next pad write unions instead of overwriting `z`. NC a session
    flag only: arm 1 RED; NC take the stamp: `z` lost."""
    fx.write_store(tmp_path, pad="a\n____")
    x = _load(tmp_path / "inbox.json")
    x.mark_notice()
    data = _store(tmp_path)
    assert data["divider_notice"] is True and data["pad"] == "a\n____"

    s2 = tmp_path / "w2"
    fx.write_store(s2, pad="")
    x = _load(s2 / "inbox.json")
    y = _load(s2 / "inbox.json")
    y.write_pad("z")
    x.mark_notice()
    assert _store(s2)["pad"] == "z" and _store(s2)["divider_notice"] is True
    res = x.write_pad("a\n____\nb")
    assert res.union is True
    assert _store(s2)["pad"] == "z\n____\na\n____\nb"


def test_TC_4446b_a_divider_is_stored_as_typed(tmp_path):
    """TC-4446b (LLR-4402.16, store side): `______` is written verbatim, not normalised to
    `____`. NC normalise: RED."""
    fx.write_store(tmp_path, pad="")
    x = _load(tmp_path / "inbox.json")
    res = x.write_pad("a\n______\nb")
    assert res.pad == "a\n______\nb"
    assert _store(tmp_path)["pad"] == "a\n______\nb"


# =========================================================================== #
# HLR-4405 layer 0 — the 7-day keep, the newest dump and the undo
# =========================================================================== #
def test_TC_4552_an_entry_older_than_seven_days_or_not_a_stamp_is_dropped(tmp_path):
    """TC-4552 (LLR-4405.12): prune keeps an entry up to 604 800 s old (exactly 7 days kept),
    drops an older one, `garbage`, a date-only and an aware stamp; every store write
    prunes. NC 30 days: the `-60 s` arm RED."""
    prune = _f("prune_dumped")
    e = [_e("one", "t1", at="2026-10-25T10:03:00"), _e("two", "t2", at="2026-10-25T10:01:00"),
         _e("three", "t3", at="garbage")]
    assert [x["task"] for x in prune(e, NOW)] == ["t1"]
    assert prune([_e("d", "t4", at="2026-10-25"),
                  _e("z", "t5", at="2026-10-25T10:03:00+00:00")], NOW) == []
    assert [x["task"] for x in prune([_e("x", "t6", at="2026-10-25T10:02:00")], NOW)] == ["t6"]

    fx.write_store(tmp_path, pad="", dumped=[
        _e("kept", "k1", at=fx.ago(days=7, seconds=-60)),
        _e("old", "o1", at=fx.ago(days=7, seconds=60)),
        _e("bad", "b1", at="garbage")])
    x = _load(tmp_path / "inbox.json")
    x.write_pad("y")
    assert [d["task"] for d in _store(tmp_path)["dumped"]] == ["k1"]


def test_TC_4541b_the_newest_entry_is_undone_first(tmp_path):
    """TC-4541b (LLR-4405.1, layer 0 of last_dump): two entries → the later one; after its
    drop is written → the earlier. NC undo the oldest: RED."""
    e1 = _e("first", "e1", at=fx.ago(seconds=120))
    e2 = _e("second", "e2", at=fx.ago(seconds=60))
    fx.write_store(tmp_path, pad="", dumped=[e1, e2])
    x = _load(tmp_path / "inbox.json")
    assert x.last_dump(datetime.now())["task"] == "e2"
    x.write_pad(x.pad, drop=dict(e2))
    assert x.last_dump(datetime.now())["task"] == "e1"


def test_TC_4547b_nothing_to_undo_is_none(tmp_path):
    """TC-4547b (LLR-4405.7, layer 0): no entry, and only an 8-day-old entry → None (the
    view says `Nothing to undo.`; NC IndexError)."""
    fx.write_store(tmp_path, pad="", dumped=[])
    assert _load(tmp_path / "inbox.json").last_dump(datetime.now()) is None
    s2 = tmp_path / "old"
    fx.write_store(s2, pad="", dumped=[_e("old", "o8", at=fx.ago(days=8))])
    assert _load(s2 / "inbox.json").last_dump(datetime.now()) is None


def test_TC_4544_an_undo_removes_its_entry_from_the_store(tmp_path):
    """TC-4544 (LLR-4405.4): the file's `dumped` loses exactly the dropped entry (NC keep it:
    a second `alt+u` undoes it again)."""
    e1, e2 = _e("first", "e1"), _e("second", "e2")
    fx.write_store(tmp_path, pad="", dumped=[e1, e2])
    x = _load(tmp_path / "inbox.json")
    x.write_pad("", drop=dict(e2))
    tasks = [d["task"] for d in _store(tmp_path)["dumped"]]
    assert tasks == ["e1"] and "e2" not in tasks
    assert [d["task"] for d in x.dumped] == ["e1"]


def test_TC_4557_alt_u_reads_the_files_dumped_list_fresh(tmp_path):
    """TC-4557 (LLR-4405.17, P-S-6): another window undid e2 → this window's newest is e1
    (e2's note is not restored a second time), memory and stamp untouched by the read; an
    unparseable file → the in-memory newest. NC read memory only: e2: RED."""
    e1 = _e("first", "e1", at=fx.ago(seconds=120))
    e2 = _e("second", "e2", at=fx.ago(seconds=60))
    fx.write_store(tmp_path, pad="", dumped=[e1, e2])
    x = _load(tmp_path / "inbox.json")
    stamp = x._stamp
    y = _load(tmp_path / "inbox.json")
    y.write_pad(y.pad, drop=dict(e2))
    assert x.last_dump(datetime.now())["task"] == "e1"
    assert [d["task"] for d in x.dumped] == ["e1", "e2"] and x._stamp == stamp
    (tmp_path / "inbox.json").write_text("{not json", encoding="utf-8")
    assert x.last_dump(datetime.now())["task"] == "e2"


def test_TC_4558_a_pending_record_is_the_newest_undo(tmp_path, monkeypatch):
    """TC-4558 (LLR-4405.18, ARCH-4): a dump whose store write failed is still the newest
    entry for `alt+u`; its pending drop removes it again; a pending record then a drop
    written together leave the pad holding the note once and `dumped` without it. NC pending
    records ignored: e1 undone instead: RED."""
    C = tmp_path / "c" / "board.json"
    e1 = _e("first", "e1", board=C, at=fx.ago(seconds=120))
    eb = _e("b", "e2", board=C)
    fx.write_store(tmp_path, pad="a\n____\nb", dumped=[e1])
    x = _load(tmp_path / "inbox.json")
    _fail_store(monkeypatch, times=2)
    with pytest.raises(OSError):
        x.write_pad("a", record=dict(eb))
    assert [(k, e["task"]) for k, e in x.pending] == [("record", "e2")]
    assert x.last_dump(datetime.now())["task"] == "e2"
    with pytest.raises(OSError):
        x.write_pad("a", drop=dict(eb))
    assert [(k, e["task"]) for k, e in x.pending] == [("record", "e2"), ("drop", "e2")]
    assert x.last_dump(datetime.now())["task"] == "e1"

    s2 = tmp_path / "w2"
    fx.write_store(s2, pad="a\n____\nb", dumped=[e1])
    x2 = _load(s2 / "inbox.json")
    monkeypatch.undo()
    box = _fail_store(monkeypatch, times=1)
    with pytest.raises(OSError):
        x2.write_pad("a", record=dict(eb))
    x2.write_pad("a\n____\nb", drop=dict(eb))
    data = _store(s2)
    assert data["pad"] == "a\n____\nb"
    assert [d["task"] for d in data["dumped"]] == ["e1"]
    assert x2.pending == [] and box["calls"] == 2


# ---- undo_dump on fixture S ------------------------------------------------- #
def test_TC_4542_an_undo_removes_the_task_from_either_board(tmp_path, monkeypatch):
    """TC-4542 (LLR-4405.2): another board is read fresh under its lock — a task another
    writer appended after the dump survives; the open board goes through the live object.
    NC save the other board from a stale read: `tw1` lost: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    out = _dump(s, NOTE_A_TEXT)
    assert out.ok, out.notice
    entry = _entry_of(out, NOTE_A_TEXT, s["C"])
    _edit_board(s["C"], lambda b: b.tasks.append(Task("Other writer", project_id="pm",
                                                       phase="Todo", id="tw1")))
    res = _f("undo_dump")(entry, None, s["F"])
    assert res.state == "undone", res
    assert fx.task_ids(s["C"]) == ["tc1", "tw1"]

    live = Board.load(s["A"])
    out = _dump(s, "Golden set answer key", which="A", project="pe", live=live,
                project_name="Eval harness")
    assert out.ok, out.notice
    tid = out.task.id
    entry = _entry_of(out, "Golden set answer key", s["A"])
    res = _f("undo_dump")(entry, live, s["F"])
    assert res.state == "undone", res
    assert tid not in fx.task_ids(s["A"])
    assert live.task_by_id(tid) is None


def test_TC_4545_an_undone_dump_removes_the_project_it_created(tmp_path, monkeypatch):
    """TC-4545 (LLR-4405.5): the dump made `Contracts pilot`; no other task uses it → gone.
    NC keep the empty project: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    out = _dump(s, "Answer the region chair", new_name="Contracts pilot")
    assert out.ok and out.new_project is True, out.notice
    entry = _entry_of(out, "Answer the region chair", s["C"])
    assert entry["new_project"] is True
    assert _f("undo_dump")(entry, None, s["F"]).state == "undone"
    data = json.loads(s["C"].read_text(encoding="utf-8"))
    assert [p["id"] for p in data["projects"]] == ["pm"]


def test_TC_4546_a_project_another_task_uses_is_kept(tmp_path, monkeypatch):
    """TC-4546 (LLR-4405.6): `tc2` joined the dump's new project → the project stays and
    tc2 keeps it. NC always remove: tc2 loses its project: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    out = _dump(s, "Answer the region chair", new_name="Contracts pilot")
    assert out.ok, out.notice
    pid = out.project_id
    entry = _entry_of(out, "Answer the region chair", s["C"])
    _edit_board(s["C"], lambda b: b.tasks.append(Task("Second", project_id=pid,
                                                       phase="Todo", id="tc2")))
    assert _f("undo_dump")(entry, None, s["F"]).state == "undone"
    data = json.loads(s["C"].read_text(encoding="utf-8"))
    assert pid in [p["id"] for p in data["projects"]]
    assert _task_rec(s["C"], "tc2")["project_id"] == pid


def test_TC_4548_a_task_gone_from_its_board_gives_the_note_back_only(tmp_path, monkeypatch):
    """TC-4548 (LLR-4405.8): the task deleted after the dump → state `gone`, the note text
    returned, the board's bytes unchanged. NC raise on the missing id: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    out = _dump(s, NOTE_A_TEXT)
    entry = _entry_of(out, NOTE_A_TEXT, s["C"])
    _edit_board(s["C"], lambda b: b.tasks.remove(b.task_by_id(out.task.id)))
    before = _bytes(s["C"])
    res = _f("undo_dump")(entry, None, s["F"])
    assert res.state == "gone"
    assert res.note_text == entry["text"] and "Volume lab fails on WSL" in res.note_text
    assert _bytes(s["C"]) == before


_CHANGES = {
    "title": lambda t: setattr(t, "title", "Volume lab fixed"),
    "phase": lambda t: setattr(t, "phase", "Doing"),
    "due": lambda t: setattr(t, "due_date", "2026-11-05"),
    "url": lambda t: t.urls.append("https://example.com/wsl"),
    "image": lambda t: t.images.append(str(Path(t.images[0]).with_name("second.png"))),
}


@pytest.mark.parametrize("change", list(_CHANGES) + ["as dumped"])
def test_TC_4550_a_task_changed_in_any_field_is_left_by_the_undo(tmp_path, monkeypatch, change):
    """TC-4550 (LLR-4405.10, SEC-3): after the AT-4402 dump into Course (save_atomic), each
    of title, phase, due date, URL, image edited → `changed` and the board's bytes unchanged;
    the task as dumped, round-tripped through `peek_board` + `save_atomic` → `undone` (no
    false "changed"). NC title and notes only: the phase arm RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    _png(s["F"] / "board-0938.png")
    out = _dump(s, NOTE_A)
    assert out.ok, out.notice
    entry = _entry_of(out, NOTE_A, s["C"])

    def edit(b):
        t = b.task_by_id(out.task.id)
        if change != "as dumped":
            _CHANGES[change](t)
    b = peek_board(s["C"])
    edit(b)
    b.save_atomic()
    before = _bytes(s["C"])
    res = _f("undo_dump")(entry, None, s["F"])
    if change == "as dumped":
        assert res.state == "undone", res
        assert out.task.id not in fx.task_ids(s["C"])
    else:
        assert res.state == "changed", (change, res)
        assert _bytes(s["C"]) == before


def test_TC_4551_an_undo_whose_board_cannot_be_changed_changes_nothing(tmp_path, monkeypatch):
    """TC-4551 (LLR-4405.11): a held lock on Course → `failed`, the notice holds `is busy`,
    the bytes unchanged; a missing board → `failed` "its file is missing"; the open board's
    save failing → `failed` "disk full", the task back at its index. NC remove the entry
    first / drop the task in memory: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    out = _dump(s, NOTE_A_TEXT)
    entry = _entry_of(out, NOTE_A_TEXT, s["C"])
    before = _bytes(s["C"])
    _hold_lock(s["C"], monkeypatch)
    res = _f("undo_dump")(entry, None, s["F"])
    assert res.state == "failed" and "is busy" in (res.notice or ""), res
    assert _bytes(s["C"]) == before

    gone = dict(entry, board=str(tmp_path / "gone" / "board.json"))
    res = _f("undo_dump")(gone, None, s["F"])
    assert res.state == "failed" and res.notice == "its file is missing", res

    live = Board.load(s["A"])
    out = _dump(s, "Golden set answer key", which="A", project="pe", live=live,
                project_name="Eval harness")
    entry = _entry_of(out, "Golden set answer key", s["A"])
    idx = [t.id for t in live.tasks].index(out.task.id)

    def boom(self):
        raise OSError("disk full")
    monkeypatch.setattr(Board, "save", boom)
    res = _f("undo_dump")(entry, live, s["F"])
    assert res.state == "failed" and res.notice == "disk full", res
    assert [t.id for t in live.tasks].index(out.task.id) == idx


def test_TC_4559_a_task_another_task_depends_on_is_left(tmp_path, monkeypatch):
    """TC-4559 (LLR-4405.19, SEC-3): `tc1.depends_on = ["t0000001"]` after the dump (the
    task itself unchanged) → `needed`, the board's bytes unchanged. NC no dependency check:
    t0000001 deleted and tc1 keeps a dangling id: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    out = _dump(s, NOTE_A_TEXT)
    assert out.task.id == "t0000001"
    entry = _entry_of(out, NOTE_A_TEXT, s["C"])
    _edit_board(s["C"], lambda b: setattr(b.task_by_id("tc1"), "depends_on", ["t0000001"]))
    before = _bytes(s["C"])
    res = _f("undo_dump")(entry, None, s["F"])
    assert res.state == "needed", res
    assert _bytes(s["C"]) == before


# =========================================================================== #
# HLR-4407 — the store
# =========================================================================== #
def test_TC_4581_the_store_sits_beside_the_registry(tmp_path):
    """TC-4581 (LLR-4407.1, layer 0): a missing store creates nothing at load; the first
    write creates `S/inbox.json`; its images folder is `S/inbox-images`, not created."""
    x = _load(tmp_path / "inbox.json")
    assert x.pad == "" and list(tmp_path.iterdir()) == []
    assert Path(x.images_dir) == tmp_path / "inbox-images" and not Path(x.images_dir).exists()
    x.write_pad("x")
    assert (tmp_path / "inbox.json").exists() and _store(tmp_path)["pad"] == "x"


async def test_TC_4581b_the_apps_store_is_the_registrys_folders(home):
    """TC-4581b (LLR-4407.1, pilot): the app's store is `<registry folder>/inbox.json`; after
    the first pad write the file is there and not beside the open board (NC: beside the
    board, in its subfolder: RED)."""
    p = fx.build_f(home)
    app = fx.open_f_app()
    assert Path(_inbox_of(app).path).resolve() == (home / "inbox.json").resolve()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.type_text(pilot, "x")
        await pilot.pause(1.3)
    assert (home / "inbox.json").exists()
    assert not (p["A"].parent / "inbox.json").exists()


def test_TC_4582_the_store_is_written_in_one_exact_shape(tmp_path):
    """TC-4582 (LLR-4407.2): `version`, `pad`, `dumped`, then `divider_notice` only once set,
    `indent=2`, `ensure_ascii=False` (é as C3 A9), no `flagged` key. NC `ensure_ascii=True`:
    `\\u00e9`: RED."""
    x = _load(tmp_path / "inbox.json")
    x.write_pad("é\n____\nb")
    raw = (tmp_path / "inbox.json").read_bytes()
    # models.write_atomic (unchanged on purpose, graph-proto-S) writes platform newlines
    assert raw.decode("utf-8").replace(os.linesep, "\n") == '{\n  "version": 1,\n  "pad": "é\\n____\\nb",\n  "dumped": []\n}'
    assert b"\xc3\xa9" in raw and b"\\u00e9" not in raw
    assert "divider_notice" not in json.loads(raw) and "flagged" not in json.loads(raw)
    x.mark_notice()
    text = (tmp_path / "inbox.json").read_text(encoding="utf-8")
    assert text.endswith(',\n  "divider_notice": true\n}')
    assert list(json.loads(text)) == ["version", "pad", "dumped", "divider_notice"]
    assert "flagged" not in text


def test_TC_4583_a_dumped_entry_has_eight_fields_in_order(tmp_path, monkeypatch):
    """TC-4583 (LLR-4407.3, entry_for): the AT-4402 dump into Course → keys at, text, task,
    title, board, project, new_project, images in that order with those types, at the
    stamp of `now`; written so by write_pad. NC `text` omitted: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    _png(s["F"] / "board-0938.png")
    out = _dump(s, NOTE_A)
    assert out.ok, out.notice
    e = _f("entry_for")(out, NOTE_A, s["C"], NOW)
    keys = ["at", "text", "task", "title", "board", "project", "new_project", "images"]
    assert list(e) == keys
    assert [type(e[k]) for k in keys] == [str, str, str, str, str, str, bool, list]
    assert e["at"] == "2026-11-01T10:02:00" and e["text"] == NOTE_A
    assert (e["task"], e["title"], e["board"], e["project"]) == (
        "t0000001", "Volume lab fails on WSL", str(s["C"]), "pm")
    assert e["new_project"] is False and e["images"] == ["board-0938.png"]
    x = _load(s["store"])
    x.write_pad("", record=_entry_of(out, NOTE_A, s["C"]))
    written = _store(s["S"])["dumped"]
    assert len(written) == 1 and list(written[0]) == keys


def test_TC_4584_each_write_applies_its_change_to_the_file_as_it_is_now(tmp_path, monkeypatch):
    """TC-4584 (LLR-4407.4): Inbox Y adds a dumped entry; X's next pad write keeps it; the
    store's lock exists during the write and is gone after. NC write the in-memory store:
    e1 lost: RED."""
    fx.write_store(tmp_path, pad="")
    x = _load(tmp_path / "inbox.json")
    y = _load(tmp_path / "inbox.json")
    calls = _spy_store_writes(monkeypatch)
    y.write_pad("", record=_e("b", "e1", board=tmp_path / "c" / "board.json"))
    res = x.write_pad("x")
    data = _store(tmp_path)
    assert [d["task"] for d in data["dumped"]] == ["e1"] and data["pad"] == "x"
    assert res.union is False
    assert calls and all(locked for _p, locked in calls)
    assert not (tmp_path / "inbox.json.lock").exists()


async def test_TC_4584b_the_views_write_keeps_another_windows_entry(home):
    """TC-4584b (LLR-4407.4, pilot): a second Inbox records a dump after the view opened; the
    view's next pad write keeps it."""
    p = fx.build_f(home)
    fx.write_store(home, pad="")
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        y = _load(p["store"])
        y.write_pad("", record=_e("b", "e1", board=p["C"], project="pv"))
        await fx.type_text(pilot, "x")
        await pilot.pause(1.3)
    data = _store(home)
    assert [d["task"] for d in data["dumped"]] == ["e1"] and data["pad"] == "x"


def test_TC_4585_the_store_is_written_atomically(tmp_path, monkeypatch):
    """TC-4585 (LLR-4407.5): one `write_atomic` call with the store's path; a failure inside
    it leaves the old bytes and the in-memory pad. NC `Path.write_text`: the spy sees
    nothing: RED."""
    fx.write_store(tmp_path, pad="old")
    x = _load(tmp_path / "inbox.json")
    calls = _spy_store_writes(monkeypatch)
    x.write_pad("new")
    assert [Path(c[0]).resolve() for c in calls] == [(tmp_path / "inbox.json").resolve()]
    before = _bytes(tmp_path / "inbox.json")
    monkeypatch.undo()
    _fail_store(monkeypatch)
    with pytest.raises(OSError, match="disk full"):
        x.write_pad("newer")
    assert _bytes(tmp_path / "inbox.json") == before and x.pad == "new"


def test_TC_4586_a_missing_store_is_an_empty_pad(tmp_path, home):
    """TC-4586 (LLR-4407.6): no file → pad "", no entries, no exception, nothing created —
    neither by `Inbox.load` nor by the app's constructor. NC raise FileNotFoundError: RED."""
    x = _load(tmp_path / "inbox.json")
    assert x.pad == "" and x.dumped == [] and not (tmp_path / "inbox.json").exists()
    fx.build_f(home)
    app = fx.open_f_app()
    assert _inbox_of(app).pad == "" and not (home / "inbox.json").exists()


@pytest.mark.parametrize("bad", ["{not json", "[1, 2]", '{"pad": 5}',
                                 '{"pad": "", "dumped": {}}'])
def test_TC_4587_an_unreadable_store_is_copied_aside_first(tmp_path, bad):
    """TC-4587 (LLR-4407.7): not JSON, not an object, a non-str pad, a non-list dumped →
    `inbox.json.corrupt` byte-equal, the pad empty. NC no copy: RED."""
    fx.write_store(tmp_path, raw=bad)
    x = _load(tmp_path / "inbox.json")
    assert (tmp_path / "inbox.json.corrupt").read_bytes() == bad.encode()
    assert x.pad == "" and x.load_report.get("unreadable") is True
    assert str(x.load_report.get("backup")).endswith("inbox.json.corrupt")


async def test_TC_4588_the_set_aside_store_is_said_once(home):
    """TC-4588 (LLR-4407.8): `{"pad": 5}` → the warning `inbox.json could not be read; it was
    copied to inbox.json.corrupt and the pad starts empty.` (markup False), the pad empty; a
    second `n` → no second notice. NC silent: RED."""
    fx.build_f(home)
    fx.write_store(home, raw='{"pad": 5}')
    app = fx.open_f_app()
    text = ("inbox.json could not be read; it was copied to inbox.json.corrupt and the pad "
            "starts empty.")
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        _one(app, text)
        assert _pad(app) == ""
        await fx.press(pilot, "escape")
        await fx.open_capture(pilot, app)
        assert len(fx.notified(app, text)) == 1


def test_TC_4589_an_unreadable_store_that_cannot_be_kept_is_never_written_over(tmp_path,
                                                                               monkeypatch):
    """TC-4589 (LLR-4407.9): `keep_aside` → None on `{not json` → the write raises an
    OSError holding `was not written`; the bytes stay `{not json`. NC overwrite: RED."""
    fx.inbox()
    _patch_keep_aside_none(monkeypatch)
    fx.write_store(tmp_path, raw="{not json")
    x = _load(tmp_path / "inbox.json")
    with pytest.raises(OSError, match="was not written"):
        x.write_pad("x")
    assert (tmp_path / "inbox.json").read_bytes() == b"{not json"


async def test_TC_4589b_the_view_says_the_store_was_not_written(home, monkeypatch):
    """TC-4589b (LLR-4407.9, pilot): typing + 1.3 s → the file's bytes unchanged and the save
    notice holds `was not written`."""
    fx.build_f(home)
    fx.inbox()
    _patch_keep_aside_none(monkeypatch)
    fx.write_store(home, raw="{not json")
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.type_text(pilot, "x")
        await pilot.pause(1.3)
        assert any("was not written" in m for m in fx.messages(app)), fx.messages(app)
    assert (home / "inbox.json").read_bytes() == b"{not json"


def test_TC_4590_a_bad_dumped_entry_is_skipped_not_the_file(tmp_path):
    """TC-4590 (LLR-4407.10, P-S-4): a list, an int `task`, no `at` → skipped, the good one
    read, the file NOT unreadable; a `task` `../x`, an image `../../a.png`, a blank text and
    `new_project` 1 → each skipped (they form file paths). NC the file unreadable: arm 1
    RED; type check only: `../x` read: arm 2 RED."""
    good = _e("good note", "g1")
    no_at = {k: v for k, v in _e("x", "g2").items() if k != "at"}
    fx.write_store(tmp_path, pad="", dumped=[[1], dict(_e("x", "g3"), task=5), no_at, good])
    x = _load(tmp_path / "inbox.json")
    assert [d["task"] for d in x.dumped] == ["g1"]
    assert not x.load_report.get("unreadable")
    for bad in (dict(_e("x", "g4"), task="../x"), dict(_e("x", "g5"), images=["../../a.png"]),
                dict(_e("x", "g6"), text="  "), dict(_e("x", "g7"), new_project=1)):
        s2 = tmp_path / bad["task"].replace(".", "_").replace("/", "_")
        fx.write_store(s2, pad="", dumped=[bad])
        assert _load(s2 / "inbox.json").dumped == [], bad


def test_TC_4591_control_characters_are_removed_from_what_is_read(tmp_path):
    """TC-4591 (LLR-4407.11): a pad holding `\\x1b[31m` and `\\x07` → neither in the pad.
    NC raw read: RED."""
    fx.write_store(tmp_path, raw=json.dumps({"version": 1, "pad": "a\u001b[31mb\u0007",
                                             "dumped": []}))
    x = _load(tmp_path / "inbox.json")
    assert x.pad == "a[31mb"


@pytest.mark.parametrize("value, shown", [('"yes"', False), ("1", False), ("true", True)])
def test_TC_4592_only_the_boolean_true_marks_the_notice_shown(tmp_path, value, shown):
    """TC-4592 (LLR-4407.12, layer 0): `"yes"`, `1` → not shown; `true` → shown. NC
    truthiness: RED."""
    fx.write_store(tmp_path, raw='{"version": 1, "pad": "", "dumped": [], "divider_notice": '
                                 + value + "}")
    assert _load(tmp_path / "inbox.json").divider_notice is shown


@pytest.mark.parametrize("value", ['"yes"', "1"])
async def test_TC_4592b_a_non_boolean_flag_shows_the_notice(home, value):
    """TC-4592b (LLR-4407.12, pilot): with the flag `"yes"` or `1` the notice shows on the
    first divider drawn as a rule."""
    fx.build_f(home)
    fx.write_store(home, raw='{"version": 1, "pad": "", "dumped": [], "divider_notice": '
                             + value + "}")
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.type_text(pilot, "a\n____\n")
        await pilot.pause(0.3)
        assert len(fx.notified(app, DIVIDER_NOTICE)) == 1, fx.messages(app)


def test_TC_4593_the_store_is_re_read_only_when_it_changed(tmp_path, monkeypatch):
    """TC-4593 (LLR-4407.13, layer 0): a second Inbox wrote `x` → refresh True, pad `x`;
    unchanged → None with 0 parses. NC read once / always: RED."""
    fx.write_store(tmp_path, pad="")
    x = _load(tmp_path / "inbox.json")
    _load(tmp_path / "inbox.json").write_pad("x")
    assert x.refresh() is True and x.pad == "x"
    box = _wrap_read(monkeypatch)
    assert x.refresh() is None and box["calls"] == 0


async def test_TC_4593b_the_view_opens_on_the_fresh_store(home, monkeypatch):
    """TC-4593b (LLR-4407.13, pilot): a second Inbox writes `x` after the app loaded → `n`
    shows `x`; a reopen with the file unchanged → 0 parses."""
    p = fx.build_f(home)
    fx.write_store(home, pad="")
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        _load(p["store"]).write_pad("x")
        await fx.open_capture(pilot, app)
        assert _pad(app) == "x"
        await fx.press(pilot, "escape")
        box = _wrap_read(monkeypatch)
        await fx.open_capture(pilot, app)
        assert box["calls"] == 0


def test_TC_4594_an_unparseable_re_read_keeps_the_pad_as_loaded(tmp_path):
    """TC-4594 (LLR-4407.14, layer 0): the file made `{not json` → refresh False, the pad as
    loaded; again unchanged → None (reported once). NC empty the pad: RED."""
    fx.write_store(tmp_path, pad="kept note")
    x = _load(tmp_path / "inbox.json")
    (tmp_path / "inbox.json").write_text("{not json", encoding="utf-8")
    assert x.refresh() is False and x.pad == "kept note"
    assert x.refresh() is None


async def test_TC_4594b_the_bad_re_read_is_said_once(home):
    """TC-4594b (LLR-4407.14, pilot): `inbox.json could not be read; the pad as loaded is
    kept.` once; the pad as loaded; `esc`, `n` → no second notice."""
    p = fx.build_f(home)
    fx.write_store(home, pad="kept note")
    app = fx.open_f_app()
    text = "inbox.json could not be read; the pad as loaded is kept."
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        p["store"].write_text("{not json", encoding="utf-8")
        await fx.open_capture(pilot, app)
        _one(app, text)
        assert _pad(app) == "kept note"
        await fx.press(pilot, "escape")
        await fx.open_capture(pilot, app)
        assert len(fx.notified(app, text)) == 1


async def test_TC_4595_the_pad_is_written_after_one_idle_second(home, monkeypatch):
    """TC-4595 (LLR-4407.15): type, 1.3 s → stored `abc`; 10 keys 0.05 s apart then 1.3 s →
    exactly 1 write. NC write per keystroke: 10: RED."""
    fx.build_f(home)
    Inbox = _I()
    calls = []
    real = Inbox.write_pad

    def spy(self, *a, **k):
        calls.append(a)
        return real(self, *a, **k)
    monkeypatch.setattr(Inbox, "write_pad", spy)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.type_text(pilot, "abc")
        await pilot.pause(1.3)
        assert _store(home)["pad"] == "abc"
        calls.clear()
        for ch in "defghijklm":
            await pilot.press(ch)
            await pilot.pause(0.05)
        await pilot.pause(1.3)
        assert len(calls) == 1, calls
    assert _store(home)["pad"] == "abcdefghijklm"


async def test_TC_4596_closing_writes_an_unwritten_pad(home):
    """TC-4596 (LLR-4407.16): type `abc` then `esc` at once → stored `abc`. NC rely on the
    debounce: RED."""
    fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.type_text(pilot, "abc")
        await fx.press(pilot, "escape")
        assert not fx.on_capture(app)
        assert _store(home)["pad"] == "abc"


@pytest.mark.parametrize("how", ["exit", "ctrl+q"])
async def test_TC_4597_exiting_writes_an_unwritten_pad(home, how):
    """TC-4597 (LLR-4407.17): type `abc`, then `app.exit()` (or `ctrl+q`) at once → stored
    `abc`. NC no unmount write: RED."""
    fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.type_text(pilot, "abc")
        if how == "exit":
            app.exit()
        else:
            await pilot.press("ctrl+q")
    assert _store(home)["pad"] == "abc"


async def test_TC_4598_an_unchanged_pad_is_never_written(home):
    """TC-4598 (LLR-4407.18, pilot arms): open, move the cursor, 1.3 s, `esc` → the store's
    bytes and mtime unchanged; with no store, no file created. NC write on close always:
    RED."""
    fx.build_f(home)
    store = fx.write_store(home, pad="a\nb")
    before = (store.read_bytes(), store.stat().st_mtime_ns)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.press(pilot, "up", "left")
        await pilot.pause(1.3)
        await fx.press(pilot, "escape")
        assert not fx.on_capture(app)
    assert (store.read_bytes(), store.stat().st_mtime_ns) == before

    store.unlink()
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.press(pilot, "left")
        await pilot.pause(1.3)
        await fx.press(pilot, "escape")
    assert not store.exists()


def test_TC_4598b_a_pending_record_makes_an_unchanged_pad_write(tmp_path, monkeypatch):
    """TC-4598b (LLR-4407.18, layer 0): the same pad, no record, nothing pending → written
    False and the mtime unchanged; with a pending record and the same pad → exactly 1 write.
    NC skip while a record is pending: arm 3 RED."""
    store = fx.write_store(tmp_path, pad="same")
    x = _load(store)
    mtime = store.stat().st_mtime_ns
    assert x.write_pad("same").written is False
    assert store.stat().st_mtime_ns == mtime
    box = _fail_store(monkeypatch, times=1)
    with pytest.raises(OSError):
        x.write_pad("same", record=_e("b", "e1"))
    res = x.write_pad("same")
    assert res.written is True and box["calls"] == 2
    assert [d["task"] for d in _store(tmp_path)["dumped"]] == ["e1"]


def test_TC_4599_a_changed_file_is_merged_note_by_note(tmp_path):
    """TC-4599 (LLR-4407.19, SEC-1, ARCH-1): the typing write unions the fresh pad's notes
    with this window's, less one copy per fresh note and per UNSEEN entry's text (a
    multiset). NC last writer wins: arm 1 RED; exclude every fresh dumped text: arm 3 `x`;
    set membership: arm 4 no copy kept."""
    union = _f("union_pads")
    assert union("a\n____\nc", ["b"], "a\n____\nb\n____\nd") == "a\n____\nc\n____\nd"
    assert union("a\n____\nc", [], "a") == "a\n____\nc"
    assert union("x", [], "x\n____\nfollow up") == "x\n____\nfollow up"
    assert union("x", ["follow up"], "x\n____\nfollow up\n____\nfollow up") == \
        "x\n____\nfollow up"

    C = tmp_path / "c" / "board.json"
    fx.write_store(tmp_path, pad="a\n____\nb")
    x = _load(tmp_path / "inbox.json")
    y = _load(tmp_path / "inbox.json")
    y.write_pad("a\n____\nc", record=_e("b", "eb", board=C))
    res = x.write_pad("a\n____\nb\n____\nd")
    assert res.union is True and res.pad == "a\n____\nc\n____\nd"
    assert _store(tmp_path)["pad"] == "a\n____\nc\n____\nd"

    s2 = tmp_path / "r"
    fx.write_store(s2, pad="", dumped=[_e("follow up", "e0", board=C, at=fx.ago(days=3))])
    x = _load(s2 / "inbox.json")
    _load(s2 / "inbox.json").write_pad("x")
    x.write_pad("x\n____\nfollow up")
    assert _store(s2)["pad"] == "x\n____\nfollow up"


def test_TC_4600_an_unchanged_file_takes_the_pad_verbatim(tmp_path):
    """TC-4600 (LLR-4407.20): `________`, blank lines and trailing spaces byte-identical;
    union False. NC always through the union: RED."""
    fx.write_store(tmp_path, pad="")
    x = _load(tmp_path / "inbox.json")
    pad = "a\n________\n\nb  \n"
    res = x.write_pad(pad)
    assert res.union is False and res.pad == pad
    assert _store(tmp_path)["pad"] == pad


async def test_TC_4600b_the_views_pad_is_stored_verbatim(home):
    """TC-4600b (LLR-4407.20, pilot): the pad `a\\n________\\n\\nb  ` → stored byte-identical."""
    fx.build_f(home)
    fx.write_store(home, pad="", divider_notice=True)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.set_pad(pilot, app, "a\n________\n\nb  ")
        await pilot.pause(1.3)
    assert _store(home)["pad"] == "a\n________\n\nb  "


async def _merged_view(home, pilot, app, p):
    """The TC-4601 scene: a second Inbox recorded `b`'s dump and wrote pad `a|c`; this view
    then holds `a|b|d` with the cursor (4, 1); the next write unions."""
    await _capture(pilot, app)
    _load(p["store"]).write_pad("a\n____\nc", record=_e("b", "eb", board=p["C"], project="pv"))
    await fx.set_pad(pilot, app, "a\n____\nb\n____\nd", cursor=(4, 1))
    await pilot.pause(1.3)


async def test_TC_4601_a_union_replaces_the_pads_text(home):
    """TC-4601 (LLR-4407.21): the pad shows the written union `a|c|d`, the cursor (4, 1)
    clamped into it. NC keep the window's text: the next write unions again: RED."""
    p = fx.build_f(home)
    fx.write_store(home, pad="a\n____\nb", divider_notice=True)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _merged_view(home, pilot, app, p)
        assert _pad(app) == "a\n____\nc\n____\nd"
        assert tuple(fx.pad_of(app).cursor_location) == (4, 1)
    assert _store(home)["pad"] == "a\n____\nc\n____\nd"


async def test_TC_4602_a_union_is_said(home):
    """TC-4602 (LLR-4407.22): `inbox.json changed in another window: its notes were merged
    into the pad.` once. NC silent: RED."""
    p = fx.build_f(home)
    fx.write_store(home, pad="a\n____\nb", divider_notice=True)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _merged_view(home, pilot, app, p)
        _one(app, "inbox.json changed in another window: its notes were merged into the pad.",
             severity=None)


def test_TC_4603_a_failed_write_keeps_the_pad_and_entries(tmp_path, monkeypatch):
    """TC-4603 (LLR-4407.23, layer 0): a held store lock → OSError `inbox.json is busy …`;
    the pad and `dumped` in memory unchanged. NC clear memory: RED."""
    fx.write_store(tmp_path, pad="", dumped=[_e("kept", "e1")])
    x = _load(tmp_path / "inbox.json")
    _hold_lock(tmp_path / "inbox.json", monkeypatch)
    with pytest.raises(OSError, match="inbox.json is busy"):
        x.write_pad("x")
    assert x.pad == "" and [d["task"] for d in x.dumped] == ["e1"]


async def test_TC_4603b_the_view_says_the_save_failed(home, monkeypatch):
    """TC-4603b (LLR-4407.23, pilot): a held lock, `x` typed, LOCK_WAIT + 1.3 s → a notice
    starting `inbox.json could not be saved: ` holding `is busy`; the pad keeps `x`;
    `dumped` unchanged."""
    p = fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        _hold_lock(p["store"], monkeypatch)
        await fx.type_text(pilot, "x")
        await pilot.pause(2.0)
        got = [m for m in fx.messages(app) if m.startswith("inbox.json could not be saved: ")]
        assert got and "is busy" in got[0], fx.messages(app)
        assert _pad(app) == "x" and _inbox_of(app).dumped == []


async def _unsaved_view(pilot, app, p, monkeypatch):
    await _capture(pilot, app)
    _hold_lock(p["store"], monkeypatch)
    await fx.type_text(pilot, "x")


ESC_WARN = "inbox.json could not be saved — esc again closes without saving."
QUIT_WARN = "inbox.json could not be saved — quit again exits without saving."


async def test_TC_4604_esc_after_a_failed_write_keeps_the_view(home, monkeypatch):
    """TC-4604 (LLR-4407.24): a held lock, `x`, `esc` → the view stays on top and warns
    `inbox.json could not be saved — esc again closes without saving.` NC close and lose
    the text: RED."""
    p = fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _unsaved_view(pilot, app, p, monkeypatch)
        await fx.press(pilot, "escape")
        assert fx.on_capture(app)
        _one(app, ESC_WARN)


async def test_TC_4605_a_second_esc_closes_unless_a_key_came_between(home, monkeypatch):
    """TC-4605 (LLR-4407.25): `esc` again → closed; a typed key in between → the next `esc`
    warns again. NC never closes: RED."""
    p = fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _unsaved_view(pilot, app, p, monkeypatch)
        await fx.press(pilot, "escape")
        await fx.type_text(pilot, "y")
        await fx.press(pilot, "escape")
        assert fx.on_capture(app) and len(fx.notified(app, ESC_WARN)) == 2
        await fx.press(pilot, "escape")
        assert not fx.on_capture(app)


async def test_TC_4607_the_view_writes_no_board_and_no_other_store(home):
    """TC-4607 (LLR-4407.27): sha256 of both board files, both histories, `people.json` and
    `marks.json` equal before `n` and after typing + 1.3 s + `esc` (6/6). NC
    `app.board.save()` on open: RED."""
    p = fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        before = fx.shas(p)
        await fx.open_capture(pilot, app)
        await fx.type_text(pilot, "abc")
        await pilot.pause(1.3)
        await fx.press(pilot, "escape")
        assert fx.shas(p) == before
    assert _store(home)["pad"] == "abc"


def _slice(rec: dict) -> str:
    return textwrap.indent(json.dumps(rec, indent=2), "    ")


def test_TC_4608_a_dump_rewrites_no_other_tasks_entry(tmp_path, monkeypatch):
    """TC-4608 (LLR-4407.28): Course saved by `Board.save` with tc1 and tc2 without
    `created` → after a dump each old task's `json.dumps(entry, indent=2)` slice is
    byte-equal in the file. NC back-fill `created`: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    b = Board.load(s["C"])
    b.tasks.append(Task("Second", project_id="pm", phase="Doing", id="tc2"))
    b.save()
    before_text = s["C"].read_text(encoding="utf-8")
    old = fx.tasks_of(s["C"])
    assert all("created" not in r for r in old)
    for r in old:
        assert _slice(r) in before_text
    out = _dump(s, NOTE_A_TEXT)
    assert out.ok, out.notice
    after = s["C"].read_text(encoding="utf-8")
    for r in old:
        assert _slice(r) in after, r["id"]


def _img_patch(monkeypatch, img):
    monkeypatch.setattr(models, "grab_clipboard_image", lambda: img)
    monkeypatch.setattr(app_module, "grab_clipboard_image", lambda: img, raising=False)


async def test_TC_4609_a_dump_an_undo_and_an_attach_write_the_store_at_once(home, monkeypatch):
    """TC-4609 (LLR-4407.29): after `alt+d`, `alt+u` and `alt+i` each, the stored `pad`
    equals the pad text with no wait. NC leave it to the 1.0 s debounce: RED."""
    fx.build_f(home)
    _png(home / "inbox-images" / "board-0938.png")
    fx.write_store(home, pad=fx.N1 + "\n____\n" + fx.N2, divider_notice=True)
    _img_patch(monkeypatch, _pil())
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.cursor_to(pilot, app, 3, 0)
        await fx.press(pilot, "alt+d")
        assert fx.N2 not in _pad(app)
        assert _store(home)["pad"] == _pad(app)
        await fx.press(pilot, "alt+u")
        assert "Volume lab fails on WSL" in _pad(app)
        assert _store(home)["pad"] == _pad(app)
        await fx.cursor_to(pilot, app, 0, 0)
        await fx.press(pilot, "alt+i")
        assert "img: paste-001.png" in _pad(app)
        assert _store(home)["pad"] == _pad(app)


# ---- caps (P-S-3) ------------------------------------------------------------ #
def test_TC_4675_a_store_over_the_cap_is_unreadable_after_cap_plus_one_bytes(tmp_path,
                                                                            monkeypatch):
    """TC-4675 (LLR-4407.35): a VALID store of 8 388 609 bytes → unreadable, pad empty, at
    most 8 388 609 bytes read from it; one of 8 388 608 bytes → read normally. WHY (E5, M48):
    a store far over the cap must cost at most the cap to reject, never a whole-file read, so
    the arm of CAP + 4096 bytes is the one a whole-file read exceeds (at CAP + 1 the two read
    the same bytes). NC `fh.read()` / `read_bytes()` of the whole file: the CAP + 4096 arm RED."""
    assert fx.need("inbox", "STORE_MAX_BYTES") == CAP
    big = tmp_path / "big"
    fx.write_store(big, raw=_store_of_size(CAP + 1))
    with monkeypatch.context() as m:
        box = _count_reads(m)
        x = _load(big / "inbox.json")
    assert x.load_report.get("unreadable") is True and x.pad == ""
    assert box["bytes"] <= CAP + 1, box
    bigger = tmp_path / "bigger"
    fx.write_store(bigger, raw=_store_of_size(CAP + 4096))
    with monkeypatch.context() as m:
        box = _count_reads(m)
        x = _load(bigger / "inbox.json")
    assert x.load_report.get("unreadable") is True and x.pad == ""
    assert box["bytes"] <= CAP + 1, box
    ok = tmp_path / "ok"
    text = _store_of_size(CAP)
    fx.write_store(ok, raw=text)
    x = _load(ok / "inbox.json")
    assert not x.load_report.get("unreadable") and x.pad == json.loads(text)["pad"]


def test_TC_4676_a_store_over_the_cap_is_not_copied_aside_nor_written(tmp_path):
    """TC-4676 (LLR-4407.36): 8 388 609 bytes → no `inbox.json.corrupt`, backup None; a pad
    change → OSError and the file's bytes unchanged. NC `keep_aside` on it: RED."""
    fx.write_store(tmp_path, raw=_store_of_size(CAP + 1))
    before = _bytes(tmp_path / "inbox.json")
    x = _load(tmp_path / "inbox.json")
    assert x.load_report.get("unreadable") is True and x.load_report.get("backup") is None
    assert not (tmp_path / "inbox.json.corrupt").exists()
    with pytest.raises(OSError):
        x.write_pad("x")
    assert _bytes(tmp_path / "inbox.json") == before
    assert not (tmp_path / "inbox.json.corrupt").exists()


def _would_hold(pad: str) -> int:
    """The bytes the store would hold ON DISK (R-E4-1): `write_atomic` writes text mode, so
    each structural newline of the JSON lands as `os.linesep`."""
    text = json.dumps({"version": 1, "pad": pad, "dumped": []}, indent=2, ensure_ascii=False)
    return len(text.replace("\n", os.linesep).encode("utf-8"))


def test_TC_4677_a_write_over_the_cap_changes_nothing(tmp_path, monkeypatch):
    """TC-4677 (LLR-4407.37): pad `a` × 8 400 000 → OSError `inbox.json would hold 8400047
    (LF) / 8400051 (CRLF, the bytes on disk: R-E4-1) bytes, over the 8388608-byte limit, so it was not written`; `write_atomic` 0 calls; the
    file and memory unchanged. NC no write cap: RED."""
    store = fx.write_store(tmp_path, pad="small")
    x = _load(store)
    before = store.read_bytes()
    calls = _spy_store_writes(monkeypatch)
    pad = "a" * 8_400_000
    n = 8_400_047 if os.linesep == "\n" else 8_400_051   # 4 structural lines (R-E4-1)
    assert _would_hold(pad) == n
    with pytest.raises(OSError) as exc:
        x.write_pad(pad)
    assert str(exc.value) == (f"inbox.json would hold {n} bytes, over the 8388608-byte "
                              "limit, so it was not written")
    assert calls == [] and store.read_bytes() == before and x.pad == "small"


def test_TC_4677c_the_cap_holds_on_disk(tmp_path):
    """TC-4677c (LLR-4407.37, R-E4-1, real filesystem): the cap counts the bytes the file
    holds on disk, not the JSON text. The store's own overhead is measured from a real
    one-character write (`os.path.getsize`), so no newline rule is assumed. A pad that makes
    the file exactly CAP bytes is written and the file is CAP bytes; one more character is
    refused with n = CAP + 1 and the file keeps its bytes. WHY: a file over the cap on disk
    is unreadable at the next load (LLR-4407.35) and is not copied aside (LLR-4407.36), so
    the pad would start empty: the note the owner typed would be lost. NC: the cap counts
    `len(text.encode())` (the CR of each Windows CRLF not counted): the CAP + 1 write goes
    through, getsize CAP + 1: RED (on a CRLF platform)."""
    store = fx.write_store(tmp_path, pad="small")
    x = _load(store)
    x.write_pad("a")
    overhead = os.path.getsize(store) - 1
    x.write_pad("a" * (CAP - overhead))
    assert os.path.getsize(store) == CAP
    assert _load(store).pad == "a" * (CAP - overhead)      # read back: not unreadable
    before = store.read_bytes()
    with pytest.raises(OSError) as exc:
        x.write_pad("a" * (CAP - overhead + 1))
    assert str(exc.value) == (f"inbox.json would hold {CAP + 1} bytes, over the 8388608-byte "
                              "limit, so it was not written")
    assert os.path.getsize(store) == CAP and store.read_bytes() == before


async def test_TC_4677b_the_view_says_the_pad_is_over_the_cap(home):
    """TC-4677b (LLR-4407.37, pilot): a pad of 8 400 000 characters (84 000 lines), 1.3 s →
    `inbox.json could not be saved: inbox.json would hold <n> bytes, over the 8388608-byte
    limit, so it was not written`; the file's bytes and `app.inbox.pad` unchanged."""
    fx.build_f(home)
    store = fx.write_store(home, pad="small")
    before = store.read_bytes()
    pad = ("a" * 99 + "\n") * 84_000
    pad = pad[:-1] + "a"
    n = _would_hold(pad)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.set_pad(pilot, app, pad)
        await pilot.pause(1.5)
        _one(app, f"inbox.json could not be saved: inbox.json would hold {n} bytes, over the "
                  "8388608-byte limit, so it was not written")
        assert _inbox_of(app).pad == "small"
    assert store.read_bytes() == before


def test_TC_4678_no_copy_kept_is_reported_with_no_backup(tmp_path, monkeypatch):
    """TC-4678 (LLR-4407.38, layer 0): `keep_aside` → None on `{"pad": 5}`, and a store over
    the cap → load_report {"unreadable": True, "backup": None}."""
    fx.inbox()
    big = tmp_path / "big"
    fx.write_store(big, raw=_store_of_size(CAP + 1))
    r = _load(big / "inbox.json").load_report
    assert r.get("unreadable") is True and r.get("backup") is None
    _patch_keep_aside_none(monkeypatch)
    fx.write_store(tmp_path, raw='{"pad": 5}')
    r = _load(tmp_path / "inbox.json").load_report
    assert r.get("unreadable") is True and r.get("backup") is None


@pytest.mark.parametrize("case", ["keep_aside None", "over the cap"])
async def test_TC_4678b_the_view_says_no_copy_could_be_kept(home, monkeypatch, case):
    """TC-4678b (LLR-4407.38, P-V-6): `inbox.json could not be read and no copy could be
    kept; the pad starts empty.` (warning, markup False), the pad empty. NC the LLR-4407.8
    text with `None` as the backup name: RED."""
    fx.build_f(home)
    fx.inbox()
    if case == "keep_aside None":
        _patch_keep_aside_none(monkeypatch)
        fx.write_store(home, raw='{"pad": 5}')
    else:
        fx.write_store(home, raw=_store_of_size(CAP + 1))
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        _one(app, "inbox.json could not be read and no copy could be kept; the pad starts "
                  "empty.")
        assert _pad(app) == ""


# ---- pending records (ARCH-4) --------------------------------------------------- #
async def _failed_dump(home, pilot, app, monkeypatch, times=1):
    """Pad N1|N2; the store write fails `times` times; `alt+d` in N2 (→ Course)."""
    await _capture(pilot, app)
    box = _fail_store(monkeypatch, times=times)
    await fx.cursor_to(pilot, app, 3, 0)
    await fx.press(pilot, "alt+d")
    return box


def _pilot_store(home):
    p = fx.build_f(home)
    _png(home / "inbox-images" / "board-0938.png")
    fx.write_store(home, pad=fx.N1 + "\n____\n" + fx.N2, divider_notice=True)
    return p


async def test_TC_4679_a_failed_store_write_after_a_dump_keeps_a_pending_record(home,
                                                                               monkeypatch):
    """TC-4679 (LLR-4407.39): the store write failing once, dump N2 → Course holds the task;
    the pad no longer holds N2; `app.inbox.pending` holds 1 record whose task is the new id;
    `inbox.json` bytes unchanged (4/4). NC no pending record: arm 3 RED."""
    p = _pilot_store(home)
    ids0 = fx.task_ids(p["C"])
    store_before = p["store"].read_bytes()
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _failed_dump(home, pilot, app, monkeypatch)
        new = [t for t in fx.task_ids(p["C"]) if t not in ids0]
        assert len(new) == 1
        assert "Volume lab fails on WSL" not in _pad(app)
        pending = _inbox_of(app).pending
        assert [(k, e["task"]) for k, e in pending] == [("record", new[0])]
        assert p["store"].read_bytes() == store_before


async def test_TC_4680_the_failed_store_write_after_a_dump_is_said(home, monkeypatch):
    """TC-4680 (LLR-4407.40): `Module 4 · Volumes · Course got the task, but inbox.json could
    not be saved: <error> — it is retried at the next save.` (warning, markup False). NC the
    generic save notice only: RED."""
    _pilot_store(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _failed_dump(home, pilot, app, monkeypatch)
        got = [n for n in fx.notes_of(app) if str(n.message).startswith(
            "Module 4 · Volumes · Course got the task, but inbox.json could not be saved: ")]
        assert len(got) == 1, fx.messages(app)
        assert str(got[0].message).endswith(" — it is retried at the next save.")
        assert got[0].markup is False and got[0].severity == "warning"


def test_TC_4681_pending_records_are_applied_at_the_next_write(tmp_path, monkeypatch):
    """TC-4681 (LLR-4407.41, layer 0): the failed record of `b` over pad `a|b`, then pad `a|x`
    on the unchanged file → stored `a|x`, `dumped` holds b's entry, pending empty; the same
    after another window added `c` → stored `a|c|x`. NC retry only at the next dump: RED."""
    C = tmp_path / "c" / "board.json"
    eb = _e("b", "eb", board=C)
    for other in (False, True):
        s = tmp_path / ("other" if other else "plain")
        fx.write_store(s, pad="a\n____\nb")
        x = _load(s / "inbox.json")
        before = (s / "inbox.json").read_bytes()
        with monkeypatch.context() as m:
            _patch_write_atomic(m, _raise_on_store(models.write_atomic))
            with pytest.raises(OSError):
                x.write_pad("a", record=dict(eb))
        assert (s / "inbox.json").read_bytes() == before
        assert [(k, e["task"]) for k, e in x.pending] == [("record", "eb")]
        if other:
            _load(s / "inbox.json").write_pad("a\n____\nb\n____\nc")
        x.write_pad("a\n____\nx")
        data = _store(s)
        assert data["pad"] == ("a\n____\nc\n____\nx" if other else "a\n____\nx")
        assert [d["task"] for d in data["dumped"]] == ["eb"]
        assert x.pending == []


def _raise_on_store(real):
    def w(path, text):
        if Path(path).name == "inbox.json":
            raise OSError("disk full")
        return real(path, text)
    return w


async def test_TC_4681b_the_view_retries_the_pending_record(home, monkeypatch):
    """TC-4681b (LLR-4407.41, pilot): after the failed dump of N2, a new note `x` typed and
    1.3 s → the stored pad is N1|x, `dumped` holds N2's entry, `pending` empty."""
    p = _pilot_store(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _failed_dump(home, pilot, app, monkeypatch)
        pad = fx.pad_of(app)
        pad.move_cursor(pad.document.end)
        await pilot.pause()
        await fx.type_text(pilot, "\n____\nx")
        await pilot.pause(1.3)
        data = _store(home)
        assert data["pad"] == _pad(app) == fx.N1 + "\n____\nx"
        assert [d["text"] for d in data["dumped"]] == [fx.N2]
        assert _inbox_of(app).pending == []


def test_TC_4682_the_pad_at_open_lacks_a_pending_records_note(tmp_path, monkeypatch):
    """TC-4682 (LLR-4407.42, layer 0 of pad_now): pad `a|b` with a pending record of `b` →
    `a`; with nothing pending → the pad as held; a refresh keeps the pending record."""
    eb = _e("b", "eb", board=tmp_path / "c" / "board.json")
    fx.write_store(tmp_path, pad="a\n____\nb")
    x = _load(tmp_path / "inbox.json")
    assert x.pad_now() == "a\n____\nb"
    _fail_store(monkeypatch, times=1)
    with pytest.raises(OSError):
        x.write_pad("a", record=dict(eb))
    assert x.pad_now() == "a" and x.pad == "a\n____\nb"
    _load(tmp_path / "inbox.json").write_pad("q")
    assert x.refresh() is True and x.pad == "q"
    assert [(k, e["task"]) for k, e in x.pending] == [("record", "eb")]


async def test_TC_4682b_a_reopened_view_does_not_bring_the_dumped_note_back(home, monkeypatch):
    """TC-4682b (LLR-4407.42, pilot): dump N2 with every store write failing, `esc` twice
    (closed unsaved), `n` → the pad is N1 only. NC fill from the store's pad: N2 back and
    a second `alt+d` makes a duplicate task: RED."""
    _pilot_store(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _failed_dump(home, pilot, app, monkeypatch, times=10**6)
        await fx.press(pilot, "escape")
        await fx.press(pilot, "escape")
        assert not fx.on_capture(app)
        await fx.open_capture(pilot, app)
        assert _pad(app) == fx.N1


# ---- encoding (SEC-2) and failed reads (SEC-4) -------------------------------- #
def test_TC_4683_a_lone_surrogate_in_the_store_makes_it_unreadable(tmp_path):
    """TC-4683 (LLR-4407.43): `{"pad": "a\\ud800b"}` (the JSON escape) → unreadable,
    `.corrupt` byte-equal, pad ""; an entry text holding `\\udfff` → unreadable; then a
    write succeeds with 0 exceptions. NC no encode probe: the first write raises: arm 3
    RED."""
    raw = '{"version": 1, "pad": "a\\ud800b", "dumped": []}'
    fx.write_store(tmp_path, raw=raw)
    x = _load(tmp_path / "inbox.json")
    assert x.load_report.get("unreadable") is True and x.pad == ""
    assert (tmp_path / "inbox.json.corrupt").read_bytes() == raw.encode()
    assert x.write_pad("x").written is True
    assert _store(tmp_path)["pad"] == "x"
    s2 = tmp_path / "entry"
    bad = json.dumps({"version": 1, "pad": "", "dumped": [_e("ok", "e1")]})
    bad = bad.replace('"text": "ok"', '"text": "x\\udfff"')
    fx.write_store(s2, raw=bad)
    assert _load(s2 / "inbox.json").load_report.get("unreadable") is True


async def test_TC_4683b_typing_over_a_surrogate_store_raises_nothing(home):
    """TC-4683b (LLR-4407.43, pilot): such a store, `x` typed, 1.3 s → the app still runs and
    the store holds pad `x`."""
    fx.build_f(home)
    fx.write_store(home, raw='{"version": 1, "pad": "a\\ud800b", "dumped": []}')
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        await fx.type_text(pilot, "x")
        await pilot.pause(1.3)
        assert fx.on_capture(app)
    assert _store(home)["pad"] == "x"


def test_TC_4684_text_that_will_not_encode_is_refused_as_an_oserror(tmp_path, monkeypatch):
    """TC-4684 (LLR-4407.44): write_pad("\\ud800") → OSError `inbox.json holds a character
    that cannot be saved (surrogates not allowed), so it was not written`, not
    UnicodeEncodeError; `write_atomic` 0 calls; no `.inbox.json.*.tmp` left. NC the encode
    error escapes as ValueError: RED."""
    store = fx.write_store(tmp_path, pad="")
    x = _load(store)
    before = store.read_bytes()
    calls = _spy_store_writes(monkeypatch)
    try:
        x.write_pad("\ud800")
    except OSError as exc:
        assert str(exc) == ("inbox.json holds a character that cannot be saved (surrogates "
                            "not allowed), so it was not written")
    except Exception as exc:      # noqa: BLE001 — the NC: any non-OSError escapes callers
        pytest.fail(f"{type(exc).__name__} escaped instead of OSError: {exc}")
    else:
        pytest.fail("write_pad wrote a lone surrogate")
    assert calls == [] and store.read_bytes() == before and x.pad == ""
    assert list(tmp_path.glob(".inbox.json.*.tmp")) == []


def test_TC_4685_a_failed_read_keeps_the_old_stamp(tmp_path, monkeypatch):
    """TC-4685 (LLR-4407.45, SEC-4): `_read` raising OSError at load over pad `p` → pad "",
    stamp None; `q` written → the union `p|q`; a refresh whose read raises after a second
    Inbox wrote `z` → False, stamp kept, the next write holds `z`. NC take the file's stamp
    after the failed read: `p` lost: arm 1 RED.
    Arm 1 fails the OPEN of `inbox.json` (a Windows sharing violation): `load` reads the file
    once itself and parses those bytes (`_parse`, F3 in e4-integration.md), so it no longer
    goes through `_read`; the refresh arms still do."""
    fx.write_store(tmp_path, pad="p")
    _fail_open(monkeypatch, times=1)
    x = _load(tmp_path / "inbox.json")
    assert x.pad == "" and x._stamp is None
    res = x.write_pad("q")
    assert res.union is True and _store(tmp_path)["pad"] == "p\n____\nq"

    monkeypatch.undo()
    s2 = tmp_path / "refresh"
    fx.write_store(s2, pad="")
    x = _load(s2 / "inbox.json")
    stamp = x._stamp
    _load(s2 / "inbox.json").write_pad("z")
    _wrap_read(monkeypatch, raise_times=1)
    assert x.refresh() is False and x._stamp == stamp
    res = x.write_pad("p")
    assert res.union is True and _store(s2)["pad"] == "z\n____\np"

    monkeypatch.undo()
    s3 = tmp_path / "again"
    fx.write_store(s3, pad="")
    x = _load(s3 / "inbox.json")
    _load(s3 / "inbox.json").write_pad("z")
    _wrap_read(monkeypatch, raise_times=1)
    assert x.refresh() is False
    assert x.refresh() is True and x.pad == "z"


async def test_TC_4686_quit_with_an_unsaved_pad_that_cannot_be_written_warns(home,
                                                                            monkeypatch):
    """TC-4686 (LLR-4407.46, SEC-5): a held lock, `x`, `ctrl+q` → the app still runs with the
    capture view on top; `inbox.json could not be saved — quit again exits without saving.`
    (warning, markup False). NC no guard: the app exits and `x` is lost: RED."""
    p = fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _unsaved_view(pilot, app, p, monkeypatch)
        await fx.press(pilot, "ctrl+q")
        assert app._exit is False and fx.on_capture(app)
        _one(app, QUIT_WARN)


async def test_TC_4687_a_second_quit_exits_unless_a_key_came_between(home, monkeypatch):
    """TC-4687 (LLR-4407.47): a key typed between → the next `ctrl+q` warns again; a second
    `ctrl+q` right after the warning → the app exits. NC never exits: RED."""
    p = fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _unsaved_view(pilot, app, p, monkeypatch)
        await fx.press(pilot, "ctrl+q")
        await fx.type_text(pilot, "y")
        await fx.press(pilot, "ctrl+q")
        assert app._exit is False and len(fx.notified(app, QUIT_WARN)) == 2
        await pilot.press("ctrl+q")
        assert app._exit is True


def test_TC_4688_a_dumps_record_removes_its_note_from_the_fresh_pad(tmp_path):
    """TC-4688 (LLR-4407.48, ARCH-1 case D): this window `a|b`, another wrote `a|b|c`; `b`
    dumped here (pad `a`, record e(b)) → stored `a|c`, `dumped` holds e(b); on an unchanged
    file → stored `a`. NC the typing union for the dump: `a|b|c` (b back: a duplicate task
    later): RED."""
    C = tmp_path / "c" / "board.json"
    eb = _e("b", "eb", board=C)
    fx.write_store(tmp_path, pad="a\n____\nb")
    x = _load(tmp_path / "inbox.json")
    _load(tmp_path / "inbox.json").write_pad("a\n____\nb\n____\nc")
    x.write_pad("a", record=dict(eb))
    data = _store(tmp_path)
    assert data["pad"] == "a\n____\nc" and [d["task"] for d in data["dumped"]] == ["eb"]
    s2 = tmp_path / "plain"
    fx.write_store(s2, pad="a\n____\nb")
    _load(s2 / "inbox.json").write_pad("a", record=dict(eb))
    assert _store(s2)["pad"] == "a"


def test_TC_4689_an_undos_drop_appends_its_note_to_the_fresh_pad(tmp_path):
    """TC-4689 (LLR-4407.49, ARCH-1 case U): the file changed to `a|c|d` still holding e(b);
    `b` undone here (pad `a|c|b`, drop e(b)) → stored `a|c|d|b`, `dumped` empty; the entry
    already undone in another window (fresh pad `a|b`, `dumped` empty) → stored `a|b`, b
    once. NC the typing union for the undo: `a|c|d` (b lost): RED."""
    C = tmp_path / "c" / "board.json"
    eb = _e("b", "eb", board=C)
    fx.write_store(tmp_path, pad="a", dumped=[eb])
    x = _load(tmp_path / "inbox.json")
    _load(tmp_path / "inbox.json").write_pad("a\n____\nc\n____\nd")
    x.write_pad("a\n____\nc\n____\nb", drop=dict(eb))
    data = _store(tmp_path)
    assert data["pad"] == "a\n____\nc\n____\nd\n____\nb" and data["dumped"] == []

    s2 = tmp_path / "twice"
    fx.write_store(s2, pad="a", dumped=[eb])
    x = _load(s2 / "inbox.json")
    _load(s2 / "inbox.json").write_pad("a\n____\nb", drop=dict(eb))
    x.write_pad("a\n____\nb", drop=dict(eb))
    data = _store(s2)
    assert data["pad"] == "a\n____\nb" and data["dumped"] == []


# =========================================================================== #
# HLR-4408 layer 0 — images
# =========================================================================== #
_YES = ["img: a.png", "img: console.png", "img: com10.png", "img: A.PNG"]
_NO = ["img: ../a.png", "img: C:\\a.png", "img: sub/a.png", "img: a.svg", "img: a",
       "img: con.png", "img: a\x07.png", "img: " + "a" * 129 + ".png", "img:  a.png",
       "img: con .png", "img: CONIN$.png", "img: com0.png", "img: lpt¹.png",
       "img: conout$.jpg", "img: aux.tar.png", "img: .png", "img:a.png", "IMG: a.png"]


@pytest.mark.parametrize("line", _YES + _NO)
def test_TC_4628_an_image_line_names_only_a_bare_safe_image_file(line):
    """TC-4628 (LLR-4408.18, P-S-10, SEC-7): the 16 arms of the threshold plus the parse
    edges (`img:a.png`, `IMG: a.png`, `.png`, `aux.tar.png`, `conout$.jpg`). NC allow `/`:
    the traversal arm RED; no device-stem check: `con.png` RED; the stem not right-stripped:
    `con .png` RED."""
    got = _f("image_name")(line)
    assert got == (line[5:] if line in _YES else None), (line, got)


def test_TC_4628b_an_image_line_may_carry_outer_spaces():
    """TC-4628b (LLR-4408.18): the line is stripped before the `img: ` prefix is read."""
    assert _f("image_name")("  img: a.png  ") == "a.png"


def test_TC_4611_pad_images_live_beside_the_store(tmp_path):
    """TC-4611 (LLR-4408.1): an attached bitmap lands at `<store dir>/inbox-images/
    paste-001.png`. NC inside a board's `images/`: RED."""
    x = _load(tmp_path / "inbox.json")
    folder = Path(x.images_dir)
    assert folder == tmp_path / "inbox-images"
    res = _f("attach_images")(folder, _pil())
    assert list(res.names) == ["paste-001.png"] and res.notice is None
    assert (tmp_path / "inbox-images" / "paste-001.png").is_file()


def test_TC_4612_a_bitmap_takes_the_next_free_paste_name(tmp_path):
    """TC-4612 (LLR-4408.2): with `paste-001.png` present → `paste-002.png`, the first file's
    bytes unchanged. NC overwrite paste-001: RED."""
    folder = tmp_path / "inbox-images"
    first = _png(folder / "paste-001.png", b"first-bytes")
    res = _f("attach_images")(folder, _pil())
    assert list(res.names) == ["paste-002.png"]
    assert first.read_bytes() == b"first-bytes" and (folder / "paste-002.png").is_file()


def test_TC_4613_a_clipboard_file_is_copied_never_moved(tmp_path):
    """TC-4613 (LLR-4408.3, F-6): `U/shot.png` with `shot.png` taken → `shot-2.png`, then
    `shot-3.png`; the source still exists byte-identical. NC move the user's file: RED."""
    folder = tmp_path / "inbox-images"
    _png(folder / "shot.png", b"older")
    src = _png(tmp_path / "U" / "shot.png", b"the user's own shot")
    res = _f("attach_images")(folder, [str(src)])
    assert list(res.names) == ["shot-2.png"]
    assert src.read_bytes() == b"the user's own shot"
    assert (folder / "shot-2.png").read_bytes() == b"the user's own shot"
    assert list(_f("attach_images")(folder, [str(src)]).names) == ["shot-3.png"]
    fresh = tmp_path / "fresh-images"
    assert list(_f("attach_images")(fresh, [str(src)]).names) == ["shot.png"]


@pytest.mark.parametrize("grabbed", [None, []])
def test_TC_4615_an_empty_clipboard_is_said(tmp_path, grabbed):
    """TC-4615 (LLR-4408.5): None or [] → `No image found in the clipboard.`, no name."""
    res = _f("attach_images")(tmp_path / "inbox-images", grabbed)
    assert list(res.names) == [] and res.notice == "No image found in the clipboard."


def test_TC_4616_files_that_are_not_images_are_not_copied(tmp_path):
    """TC-4616 (LLR-4408.6): a `.txt` and a `.svg` → `Clipboard holds no image files.`, 0
    copies. NC copy the `.svg`: RED."""
    folder = tmp_path / "inbox-images"
    a = _png(tmp_path / "U" / "a.txt", b"text")
    b = _png(tmp_path / "U" / "b.svg", b"<svg/>")
    res = _f("attach_images")(folder, [str(a), str(b)])
    assert list(res.names) == [] and res.notice == "Clipboard holds no image files."
    assert not folder.exists() or list(folder.iterdir()) == []


def test_TC_4617_a_failed_save_or_copy_is_said(tmp_path, monkeypatch):
    """TC-4617 (LLR-4408.7): `shutil.copy2` raising `read-only` → `The image could not be
    saved: read-only`, no name; `save_pil_image` failing → the same prefix. NC a line for a
    missing file: RED."""
    src = _png(tmp_path / "U" / "shot.png")

    def ro(*a, **k):
        raise OSError("read-only")
    with monkeypatch.context() as m:
        m.setattr(shutil, "copy2", ro)
        m.setattr(fx.inbox(), "copy2", ro, raising=False)
        res = _f("attach_images")(tmp_path / "inbox-images", [str(src)])
    assert list(res.names) == [] and res.notice == "The image could not be saved: read-only"
    with monkeypatch.context() as m:
        m.setattr(models, "save_pil_image", ro)
        m.setattr(fx.inbox(), "save_pil_image", ro, raising=False)
        res = _f("attach_images")(tmp_path / "inbox-images", _pil())
    assert list(res.names) == []
    assert (res.notice or "").startswith("The image could not be saved: ")


def test_TC_4629_a_clipboard_file_with_an_unsafe_name_is_saved_as_image(tmp_path):
    """TC-4629 (LLR-4408.19, P-S-10): `con.png` → `image.png` (bytes equal, the source
    unchanged); with `image.png` taken → `image-2.png`. NC copy under its own name: a line
    the dump can never read: RED."""
    folder = tmp_path / "inbox-images"
    src = _png(tmp_path / "U" / "con.png", b"device-named")
    res = _f("attach_images")(folder, [str(src)])
    assert list(res.names) == ["image.png"]
    assert (folder / "image.png").read_bytes() == b"device-named"
    assert src.read_bytes() == b"device-named"
    assert list(_f("attach_images")(folder, [str(src)]).names) == ["image-2.png"]


def _img_dir(s, tid="t0000001") -> Path:
    return s["C"].parent / "images" / tid


def test_TC_4620_a_dump_moves_its_images_into_the_tasks_folder(tmp_path, monkeypatch):
    """TC-4620 (LLR-4408.10): `paste-001.png` and `shot.png` → `C/images/t0000001/`, the
    task's `images` their resolved paths in line order, the outcome the names; the pad
    copies gone (plain folders); bytes equal. NC copy without removing the source: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    _png(s["F"] / "paste-001.png", b"P1")
    _png(s["F"] / "shot.png", b"S1")
    out = _dump(s, "T\nimg: paste-001.png\nimg: shot.png")
    assert out.ok, out.notice
    dest = _img_dir(s)
    assert out.task.images == [str((dest / "paste-001.png").resolve()),
                               str((dest / "shot.png").resolve())]
    assert list(out.images) == ["paste-001.png", "shot.png"]
    assert _task_rec(s["C"], "t0000001")["images"] == out.task.images
    assert not (s["F"] / "paste-001.png").exists() and not (s["F"] / "shot.png").exists()
    assert (dest / "paste-001.png").read_bytes() == b"P1"
    assert (dest / "shot.png").read_bytes() == b"S1"


def test_TC_4621_a_failed_board_save_keeps_every_pad_image(tmp_path, monkeypatch):
    """TC-4621 (LLR-4408.11): `save_atomic` raising → both sources still in the pad images
    folder and no `images/t0000001/` left. NC move before save: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    _png(s["F"] / "a.png", b"A")
    _png(s["F"] / "b.png", b"B")

    def boom(self):
        raise OSError("disk full")
    monkeypatch.setattr(Board, "save_atomic", boom)
    out = _dump(s, "T\nimg: a.png\nimg: b.png")
    assert out.ok is False
    assert (s["F"] / "a.png").read_bytes() == b"A" and (s["F"] / "b.png").read_bytes() == b"B"
    assert not _img_dir(s).exists()


def test_TC_4622_a_missing_image_keeps_its_line_as_text(tmp_path, monkeypatch):
    """TC-4622 (LLR-4408.12, P-S-2): `img: gone.png` → the dump succeeds, the notes keep the
    line, `missing` names it, `task.images` empty; its undo is `undone`, not `changed`. NC
    drop the line silently: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    note = "T\nx\nimg: gone.png"
    out = _dump(s, note)
    assert out.ok, out.notice
    assert out.task.notes == "x\nimg: gone.png"
    assert list(out.missing) == ["gone.png"] and out.task.images == []
    entry = _entry_of(out, note, s["C"])
    assert entry["images"] == []
    assert _f("undo_dump")(entry, None, s["F"]).state == "undone"


def test_TC_4622c_a_symlinked_pad_image_is_not_followed(tmp_path, monkeypatch):
    """TC-4622c (LLR-4408.12): a symlink `link.png` in the pad images folder is "not found"
    (never followed on the move path)."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    real = _png(tmp_path / "elsewhere" / "real.png", b"R")
    s["F"].mkdir(parents=True, exist_ok=True)
    try:
        os.symlink(real, s["F"] / "link.png")
    except OSError as exc:
        pytest.skip(f"cannot create a symlink here (Windows privilege): {exc}")
    out = _dump(s, "T\nimg: link.png")
    assert out.ok and list(out.missing) == ["link.png"]
    assert real.read_bytes() == b"R"


def test_TC_4623_an_image_that_cannot_be_moved_stops_the_dump(tmp_path, monkeypatch):
    """TC-4623 (LLR-4408.13, ARCH-7): `copy2` failing on the 2nd image → `An image could not
    be moved: boom — nothing dumped.`, no `images/t0000001/`, the board and the pad images
    unchanged; a task folder already present (the id source patched to a taken id) → the
    same refusal, the folder and its file untouched. NC dump without the image: arm 1 RED;
    copy into the existing folder: arm 4 RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    _png(s["F"] / "a.png", b"A")
    _png(s["F"] / "b.png", b"B")
    before = _bytes(s["C"])
    real = shutil.copy2
    n = {"k": 0}

    def flaky(*a, **k):
        n["k"] += 1
        if n["k"] == 2:
            raise OSError("boom")
        return real(*a, **k)
    with monkeypatch.context() as m:
        m.setattr(shutil, "copy2", flaky)
        m.setattr(fx.inbox(), "copy2", flaky, raising=False)
        out = _dump(s, "T\nimg: a.png\nimg: b.png")
    assert out.ok is False and out.notice == "An image could not be moved: boom — nothing dumped."
    assert not _img_dir(s).exists() and _bytes(s["C"]) == before
    assert (s["F"] / "a.png").read_bytes() == b"A" and (s["F"] / "b.png").read_bytes() == b"B"

    s2 = fx.build_s(tmp_path / "taken")
    fx.seq_ids(monkeypatch)
    _png(s2["F"] / "a.png", b"A")
    x = _png(_img_dir(s2) / "x.png", b"X")
    before = _bytes(s2["C"])
    out = _dump(s2, "T\nimg: a.png")
    assert out.ok is False
    assert out.notice.startswith("An image could not be moved: ")
    assert out.notice.endswith(" — nothing dumped.")
    assert x.read_bytes() == b"X" and sorted(p.name for p in _img_dir(s2).iterdir()) == ["x.png"]
    assert _bytes(s2["C"]) == before and (s2["F"] / "a.png").exists()


def test_TC_4625_an_image_named_twice_moves_once(tmp_path, monkeypatch):
    """TC-4625 (LLR-4408.15): `img: a.png` twice → `task.images` holds 1 path, 1 file copied.
    NC the second move raises on the gone source: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    _png(s["F"] / "a.png")
    out = _dump(s, "T\nimg: a.png\nimg: a.png")
    assert out.ok, out.notice
    assert len(out.task.images) == 1
    assert [p.name for p in _img_dir(s).iterdir()] == ["a.png"]


def test_TC_4626_an_undone_dump_moves_its_images_back_renamed_when_taken(tmp_path,
                                                                        monkeypatch):
    """TC-4626 (LLR-4408.16): F already holds another `paste-001.png` → the board's copy comes
    back as `paste-001-2.png` (bytes equal) and the restored note names it. NC leave the
    files in the board: the restored lines name missing files: RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    _png(s["F"] / "paste-001.png", b"DUMPED")
    note = "T\nimg: paste-001.png"
    out = _dump(s, note)
    assert out.ok, out.notice
    entry = _entry_of(out, note, s["C"])
    _png(s["F"] / "paste-001.png", b"NEWER")
    res = _f("undo_dump")(entry, None, s["F"])
    assert res.state == "undone"
    assert (s["F"] / "paste-001-2.png").read_bytes() == b"DUMPED"
    assert (s["F"] / "paste-001.png").read_bytes() == b"NEWER"
    assert res.note_text == "T\nimg: paste-001-2.png"
    assert not (_img_dir(s) / "paste-001.png").exists()


def test_TC_4627_an_undone_dump_removes_its_emptied_image_folder(tmp_path, monkeypatch):
    """TC-4627 (LLR-4408.17): after the undo `C/images/t0000001` is gone. NC folder left."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    _png(s["F"] / "paste-001.png")
    note = "T\nimg: paste-001.png"
    out = _dump(s, note)
    assert _img_dir(s).is_dir()
    assert _f("undo_dump")(_entry_of(out, note, s["C"]), None, s["F"]).state == "undone"
    assert not _img_dir(s).exists()


def test_TC_4650_no_source_is_removed_through_a_junction(tmp_path, monkeypatch):
    """TC-4650 (LLR-4408.20, SEC-6): the pad images folder a junction to J holding `a.png`
    → the dump copies (the task's file present) and `J/a.png` stays; a dumped task's
    `images/<id>` a junction to J2 → the undo copies `a.png` into the pad images folder
    and `J2/a.png` stays. Plain folders remove the sources (TC-4620, TC-4626). NC unlink
    with no link check: `J/a.png` gone: arm 1 RED."""
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    J = tmp_path / "J"
    _png(J / "a.png", b"JA")
    _junction(J, s["F"])
    out = _dump(s, "T\nimg: a.png")
    assert out.ok, out.notice
    assert (_img_dir(s) / "a.png").read_bytes() == b"JA"
    assert (J / "a.png").read_bytes() == b"JA"

    s2 = fx.build_s(tmp_path / "undo")
    fx.seq_ids(monkeypatch)
    _png(s2["F"] / "a.png", b"UA")
    note = "T\nimg: a.png"
    out = _dump(s2, note)
    assert out.ok, out.notice
    entry = _entry_of(out, note, s2["C"])
    J2 = tmp_path / "J2"
    _png(J2 / "a.png", b"UA")
    shutil.rmtree(_img_dir(s2))
    _junction(J2, _img_dir(s2))
    # the task's record as the board now resolves it (the expected record of SEC-3 is
    # built from `image_dir(id) / name` resolved, which follows the junction)
    _edit_board(s2["C"], lambda b: setattr(b.task_by_id(out.task.id), "images",
                                           [str((_img_dir(s2) / "a.png").resolve())]))
    res = _f("undo_dump")(entry, None, s2["F"])
    assert res.state == "undone", res
    assert (s2["F"] / "a.png").read_bytes() == b"UA"
    assert (J2 / "a.png").read_bytes() == b"UA"


# =========================================================================== #
# HLR-4409 layer 0 — colour, mentions and control characters
# =========================================================================== #
def test_TC_4632_spans_and_mentions_reach_the_task_byte_for_byte(tmp_path, monkeypatch):
    """TC-4632 (LLR-4409.2): note_task keeps `::b:: x :: @username_subject` verbatim; a dump
    writes the same notes; `views.notes_text` of them colours `x` blue. NC strip the
    markers: RED."""
    from added_list_fixture import colour_at
    nt = _f("note_task")("T\n::b:: x :: @username_subject")
    assert nt.notes == "::b:: x :: @username_subject"
    nt = _f("note_task")("Golden set\n::b:: ask the vendor :: @username_subject")
    assert (nt.title, nt.notes) == ("Golden set", "::b:: ask the vendor :: @username_subject")
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    out = _dump(s, "T\n::b:: x :: @username_subject")
    assert out.ok, out.notice
    assert _task_rec(s["C"], "t0000001")["notes"] == "::b:: x :: @username_subject"
    shown = views.notes_text(out.task.notes)
    assert colour_at(shown, shown.plain.index("x")) == views.HEX["blue"].lower()


def test_TC_4633_control_characters_leave_a_dumped_title_and_notes(tmp_path, monkeypatch):
    """TC-4633 (LLR-4409.3): `\\x1b[2J T` / `a\\x07b` → title `[2J T`, notes `ab`; no C0 but
    tab/newline, no DEL, no C1 remains — in note_task and in the board file. NC raw text:
    RED."""
    nt = _f("note_task")("\x1b[2J T\na\x07b")
    assert (nt.title, nt.notes) == ("[2J T", "ab")
    s = fx.build_s(tmp_path)
    fx.seq_ids(monkeypatch)
    out = _dump(s, "\x1b[2J T\na\x07b\x9b\x7f")
    assert out.ok, out.notice
    rec = _task_rec(s["C"], "t0000001")
    assert (rec["title"], rec["notes"]) == ("[2J T", "ab")
    for text in (nt.title, nt.notes, rec["title"], rec["notes"]):
        assert all(c in "\t\n" or 0x20 <= ord(c) < 0x7f or ord(c) >= 0xa0 for c in text)


def test_TC_4635_the_pad_is_stored_without_control_characters(tmp_path):
    """TC-4635 (LLR-4409.5): a pasted `\\x1b` and `\\x9b` → absent from the stored pad and
    from the result's pad. NC raw write: RED."""
    x = _load(tmp_path / "inbox.json")
    res = x.write_pad("a\x1bb\x9bc")
    assert res.pad == "abc" and _store(tmp_path)["pad"] == "abc"


# =========================================================================== #
# E5 corrective pass (05-corrections.md, LED-2026-11-01-incK.6)
# =========================================================================== #
def test_TC_4444c_a_note_dumped_in_another_window_stays_out_after_the_notice(tmp_path):
    """TC-4444c (LLR-4402.14, SEC-1, CR-1). WHY: a note dumped as a task in one window must
    never come back into the pad through another window — a later `alt+d` on it would make
    a second task. Pad `x|b`, windows X and Y load it; Y dumps `b`; X shows the divider
    notice (`mark_notice`), then writes `x|b|d` → the stored pad `x|d`, union True, `dumped`
    still holds b's entry. NC `mark_notice` holds the file's `dumped` while the file had
    changed (X then counts Y's entry as seen and keeps its stale `b`): `x|b|d`: RED."""
    fx.write_store(tmp_path, pad="x\n____\nb")
    x = _load(tmp_path / "inbox.json")
    y = _load(tmp_path / "inbox.json")
    y.write_pad("x", record=dict(_e("b", "tb", board=tmp_path / "c" / "board.json")))
    x.mark_notice()
    assert _store(tmp_path)["divider_notice"] is True
    res = x.write_pad("x\n____\nb\n____\nd")
    data = _store(tmp_path)
    assert data["pad"] == "x\n____\nd", data["pad"]
    assert res.union is True
    assert [d["task"] for d in data["dumped"]] == ["tb"]


def test_TC_4444d_the_notice_is_not_written_when_the_file_already_holds_it(tmp_path,
                                                                           monkeypatch):
    """TC-4444d (LLR-4402.14, CR-5). WHY: a write the design says does not happen still
    takes the store's lock and moves its stamp, so every other window then merges instead of
    writing its pad as typed. Window X loaded before window Y set the flag; X's
    `mark_notice` → 0 store writes, the file's bytes unchanged, X's flag True. NC always
    `_commit`: 1 write: RED."""
    fx.write_store(tmp_path, pad="a")
    x = _load(tmp_path / "inbox.json")
    _load(tmp_path / "inbox.json").mark_notice()
    before = _bytes(tmp_path / "inbox.json")
    calls = _spy_store_writes(monkeypatch)
    x.mark_notice()
    assert calls == [] and _bytes(tmp_path / "inbox.json") == before
    assert x.divider_notice is True


def _foreign_write_after_read(m, path: Path, text: str) -> dict:
    """The first `open` of `inbox.json` for reading: once that handle is closed, another
    window writes `text` to the file (before the reader can stat it)."""
    real = io.open
    box = {"left": 1}

    class _Then:
        def __init__(self, fh):
            self._fh = fh

        def __enter__(self):
            self._fh.__enter__()
            return self

        def read(self, *a):
            return self._fh.read(*a)

        def __exit__(self, *a):
            r = self._fh.__exit__(*a)
            with real(path, "w", encoding="utf-8") as out:
                out.write(text)
            return r

        def __getattr__(self, a):
            return getattr(self._fh, a)

    def spy(file, *a, **k):
        fh = real(file, *a, **k)
        try:
            hit = Path(os.fsdecode(file)).name == "inbox.json"
        except TypeError:
            hit = False
        mode = a[0] if a else k.get("mode", "r")
        if hit and "r" in mode and box["left"] > 0:
            box["left"] -= 1
            return _Then(fh)
        return fh
    m.setattr(builtins, "open", spy)
    m.setattr(io, "open", spy)
    return box


def test_TC_4599b_the_stamp_is_the_files_as_this_window_last_read_or_wrote_it(tmp_path,
                                                                              monkeypatch):
    """TC-4599b (LLR-4407.19, CR-2). WHY: the stamp decides between writing this window's
    pad as typed and merging; a stamp taken after another window's write makes this window
    overwrite that window's notes silently. Arm 1: right after X's store write releases the
    lock, window Y writes `a|z`; X then writes `a|q` → `a|z|q` (union). The load side is
    TC-4599c. NC the stamp taken after the lock is released: `a|q`, `z` lost: RED."""
    inbox_mod = fx.inbox()
    real_lock = inbox_mod.file_lock
    box = {"left": 0}
    store = tmp_path / "inbox.json"

    @contextlib.contextmanager
    def lock_then_foreign(path, label):
        with real_lock(path, label):
            yield
        if box["left"]:
            box["left"] -= 1
            other = _load(store)
            other.write_pad(other.pad + "\n____\nz")

    monkeypatch.setattr(inbox_mod, "file_lock", lock_then_foreign)
    fx.write_store(tmp_path, pad="")
    x = _load(store)
    box["left"] = 1
    x.write_pad("a")
    assert _store(tmp_path)["pad"] == "a\n____\nz"
    res = x.write_pad("a\n____\nq")
    assert _store(tmp_path)["pad"] == "a\n____\nz\n____\nq", _store(tmp_path)["pad"]
    assert res.union is True


def test_TC_4599c_the_load_stamp_is_taken_before_the_read(tmp_path, monkeypatch):
    """TC-4599c (LLR-4407.19, CR-2). WHY: as TC-4599b, at load: right after X's load read the
    file and before it could stat it, window Y writes pad `p|z`; X writes `p|q` → `p|z|q`
    (union). NC the stamp taken after the read: `p|q`, `z` lost: RED."""
    s2 = tmp_path / "load"
    fx.write_store(s2, pad="p")
    foreign = json.dumps({"version": 1, "pad": "p\n____\nz", "dumped": []}, indent=2)
    with monkeypatch.context() as m:
        _foreign_write_after_read(m, s2 / "inbox.json", foreign)
        x = _load(s2 / "inbox.json")
    assert x.pad == "p" and _store(s2)["pad"] == "p\n____\nz"
    res = x.write_pad("p\n____\nq")
    assert _store(s2)["pad"] == "p\n____\nz\n____\nq", _store(s2)["pad"]
    assert res.union is True


A4_NOTICE = "inbox.json could not be read right now; its notes merge back on the next save."


async def test_TC_4690_a_store_that_cannot_be_read_now_says_its_notes_merge_back(home,
                                                                                 monkeypatch):
    """TC-4690 (LLR-4407.50, A-4, K-SEC-2). WHY: the file is only held by another process
    for a moment — its notes are not gone and merge back at the next save (SEC-4); a notice
    saying "no copy could be kept" makes the owner re-type them (duplicates) or delete the
    file to repair it (real loss). The open of `inbox.json` failing once at start → the A-4
    notice once (warning, markup False), not the LLR-4407.38 one; the pad holds `p` (the
    view's refresh at open re-reads the file, which reads now: nothing lost). NC the
    LLR-4407.38 wording: RED."""
    fx.build_f(home)
    fx.write_store(home, pad="p")
    _fail_open(monkeypatch, times=1)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _capture(pilot, app)
        assert fx.notified(app, "inbox.json could not be read and no copy could be kept; "
                                "the pad starts empty.") == [], fx.messages(app)
        _one(app, A4_NOTICE)
        assert _pad(app) == "p"


@pytest.mark.parametrize("where", ["main", "home"])
@pytest.mark.parametrize("fails", [3, 4])
async def test_TC_4691_quit_retries_a_held_pending_record_once(home, monkeypatch, where,
                                                               fails):
    """TC-4691 (LLR-4407.51, A-3, CR-3, K-SEC-3). WHY: a dump whose store write failed is
    kept only in memory as a pending record; a quit that does not retry it once leaves the
    note's task on the board with no undo entry in the store. The dump of N2 fails its store
    write, and so do the view's two close-time writes (`esc` warns, a second `esc` closes and
    its unmount write fails: the record still pending); then `q` from the board (`main`) or
    from the boards home (`home`, `B`): one more store write is tried; it succeeds (fails=3)
    → `inbox.json` holds N2's entry; it fails (fails=4) → the NC no retry on the home's `q`: 3 writes and no entry: RED (home);
    NC no retry at all: RED (main)."""
    _pilot_store(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        box = await _failed_dump(home, pilot, app, monkeypatch, times=fails)
        await fx.press(pilot, "escape")
        await fx.press(pilot, "escape")
        assert fx.captures_on_stack(app) == 0, fx.screen_names(app)
        assert len(_inbox_of(app).pending) == 1 and box["calls"] == 3, box
        if where == "home":
            await fx.press(pilot, "B")
            assert type(app.screen).__name__ == "BoardsHome", fx.screen_names(app)
        await fx.press(pilot, "q")
        assert app._exit is True
        assert box["calls"] == 4, box
    assert [d["text"] for d in _store(home)["dumped"]] == ([fx.N2] if fails == 3 else [])


def test_TC_4651_an_undo_whose_images_cannot_come_back_still_completes(tmp_path,
                                                                       monkeypatch):
    """TC-4651 (LLR-4408.21, K-SEC-1, RISK-P-S-12). WHY: the board save has already removed
    the task when the image files are moved back; an exception there ends the app with the
    note in neither the board nor the pad (and any pending record lost). `inbox-images` is a
    regular file: a note with no image → undone, the note text back, the task gone; a note
    with `paste-001.png` → undone, the note text as dumped, the task gone, the image left in
    the board's task folder. NC the folder made outside the guard: FileExistsError: RED."""
    undo = _f("undo_dump")
    for sub, note, image in (("plain", "Plain note\nno image here", None),
                             ("image", "T\nimg: paste-001.png", "paste-001.png")):
        s = fx.build_s(tmp_path / sub)
        fx.seq_ids(monkeypatch)
        if image:
            _png(s["F"] / image, b"DUMPED")
        out = _dump(s, note)
        assert out.ok, out.notice
        entry = _entry_of(out, note, s["C"])
        shutil.rmtree(s["F"], ignore_errors=True)
        s["F"].write_bytes(b"a file where the pad images folder belongs")
        res = undo(entry, None, s["F"])
        assert res.state == "undone", res
        assert res.note_text == note
        assert _task_rec(s["C"], "t0000001") is None
        if image:
            assert (_img_dir(s) / image).read_bytes() == b"DUMPED"


def test_TC_4613b_a_renamed_copy_still_passes_the_image_name_rule(tmp_path):
    """TC-4613b (LLR-4408.3, K-SEC-5). WHY: a copy whose name the image-name rule rejects is
    no image line at all — the file sits in `inbox-images/` that nothing manages, and its
    line dumps as text. A 128-character `s…s.png` taken → the copy's name is at most 128
    characters, passes `image_name`, ends `-2.png`, holds the source's bytes. NC no cut:
    `…-2.png` of 130 characters: RED."""
    folder = tmp_path / "F"
    name = "s" * 124 + ".png"
    assert len(name) == 128
    _png(folder / name, b"older")
    src = _png(tmp_path / "U" / name, b"mine")
    (new,) = _f("attach_images")(folder, [str(src)]).names
    assert len(new) <= 128 and new.endswith("-2.png"), (len(new), new)
    assert _f("image_name")("img: " + new) == new
    assert (folder / new).read_bytes() == b"mine"
