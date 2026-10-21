"""Several boards: the registry of board files (batch 2026-10-20-batch-01).

Each board is its own file in its own folder — its `history.jsonl`, `images/`
and `reports/` live beside it, so two boards never share them. The registry,
`boards.json` beside the default board, lists them: id, name, colour, path,
when each was last opened, whether it is archived, and the board opened last.
The default board (`~/.taskboard/board.json`) is `Main`, in place.

The registry is read like the board file: never raising, a bad entry skipped
or defaulted, an unreadable file copied aside first. It is written atomically,
and never for a one-board user who has no registry file yet. Every write is a
read-modify-write under a lock file (batch 2026-10-20-batch-02), so a second
taskboard's change to the registry is never written over.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import stat
import time
import unicodedata
from contextlib import ExitStack, contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from .models import (PROJECT_COLORS, Board, clean_strings, default_board_path,
                     project_color_on_load, strip_controls, write_atomic)

REGISTRY_NAME = "boards.json"
MAIN_ID = "main"
MAIN_NAME = "Main"
NAME_MAX = 60
LOCK_WAIT = 2.0      # seconds a writer waits for another taskboard's lock
LOCK_STALE = 10.0    # a lock file older than this was left by an instance that died
PRESENCE_STALE = 120.0   # a presence marker not renewed for this long is a dead window's
_PRESENCE_READ = 4096    # a marker's JSON is read from at most this many bytes
_ID = re.compile(r"[A-Za-z0-9_-]+")
# names Windows will not give a folder (`con` spelled in two pieces: the English law
# of tests/test_english.py reads a bare "con" as a Spanish word)
_RESERVED = {"co" + "n", "prn", "aux", "nul"} | {f"{d}{n}" for d in ("com", "lpt")
                                                for n in range(1, 10)}


def registry_path() -> Path:
    return default_board_path().parent / REGISTRY_NAME


def slug(name: str) -> str:
    """`Course · Kubernetes` → `course-kubernetes`; accents folded; `board` when
    nothing is left. Only `a-z`, `0-9` and `-`: a slug names a folder, so it can
    never hold a separator or `..`."""
    folded = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    out = re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-") or "board"
    return out + "-board" if out in _RESERVED else out


def clean_name(name) -> str:
    """A board's name as stored: no control byte, no surrounding blank, at most
    60 characters."""
    return strip_controls(str(name)).strip()[:NAME_MAX].strip()


def keep_aside(path: Path) -> Path | None:
    """A byte copy of an unreadable file — the registry, the people directory — at
    the first free name of `<name>.corrupt`, `.corrupt-2`, …: an earlier copy is
    never replaced and the current bytes always kept. An empty file has nothing to
    keep."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if not data:
        return None
    n = 1
    while True:
        dest = path.with_name(path.name + ".corrupt" + (f"-{n}" if n > 1 else ""))
        try:
            with open(dest, "xb") as fh:
                fh.write(data)
            return dest
        except FileExistsError:
            n += 1
        except OSError:
            return None


def _lock_token(lock: Path) -> bytes | None:
    try:
        with open(lock, "rb") as fh:
            return fh.read(64)
    except OSError:
        return None


@contextmanager
def file_lock(path, label: str | None = None):
    """Hold `<name>.lock` beside `path` while taskboard reads, changes and writes
    `path`, so two instances take turns (batch 2026-10-20-batch-02). The lock is
    created exclusively and holds a random token; on exit it is removed only while
    it still holds this holder's token. A regular lock file whose time is more than
    `LOCK_STALE` seconds from now is a dead instance's and is taken over; past
    `LOCK_WAIT` seconds an `OSError` says the file — or `label`, the board's name —
    is busy: never a wait without end. Yields a heartbeat that renews the lock's
    time, for a holder that works for longer."""
    lock = Path(path).resolve()
    lock = lock.with_name(lock.name + ".lock")
    token = os.urandom(16).hex().encode("ascii")
    deadline = time.monotonic() + LOCK_WAIT
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except (FileExistsError, PermissionError):
            fd = None   # PermissionError: Windows, while another instance removes it
        if fd is not None:
            try:
                os.write(fd, token)
            except OSError:
                os.close(fd)
                try:
                    os.unlink(lock)     # never a token-less lock left behind (S-6)
                except OSError:
                    pass                # stale in LOCK_STALE; the write's error is the one (S-11)
                raise
            os.close(fd)
            break
        try:
            st = os.lstat(lock)
            if stat.S_ISREG(st.st_mode) and abs(time.time() - st.st_mtime) > LOCK_STALE:
                again = os.lstat(lock)
                if (again.st_mtime_ns, again.st_ino) == (st.st_mtime_ns, st.st_ino):
                    os.unlink(lock)     # not renewed nor replaced meanwhile (S-7)
        except OSError:
            pass        # gone, going or not ours to remove: try again
        if time.monotonic() >= deadline:
            raise OSError(f"{label or Path(path).name} is busy — another taskboard is "
                          f"writing it; try again in a few seconds ({lock})")
        time.sleep(0.05)

    def beat() -> None:
        try:
            os.utime(lock)
        except OSError:
            pass
    try:
        yield beat
    finally:
        if _lock_token(lock) == token:
            try:
                os.unlink(lock)
            except OSError:
                pass    # a stale copy is taken over by the next writer


def expand_home(p) -> Path:
    """`~` read as `Path.home()` (the public name, for `__main__` — architect A-19)."""
    return _expand_home(p)


def _expand_home(p) -> Path:
    """`~` read as `Path.home()` — the home the suite's seam names — never the
    environment `expanduser` reads (G-9); `~user` stays as written."""
    s = str(p)
    if s == "~" or s.startswith(("~/", "~" + os.sep)):
        return Path.home() / s[2:]
    return Path(s)


def _key(path) -> str:
    """One spelling per file: absolute, resolved, case-normalised on Windows."""
    return os.path.normcase(str(_expand_home(path).resolve()))


def _name_for(path) -> str:
    p = Path(path)
    return (p.parent.name if p.stem == "board" else p.stem) or MAIN_NAME


def name_for(path) -> str:
    """The name a registered board of this file gets (batch 2026-10-20-batch-03: an
    unlisted board's chip and notices), its control characters stripped."""
    return strip_controls(_name_for(path))


def _iso_or_none(value) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        when = datetime.fromisoformat(value)
    except ValueError:
        return None
    # a local time only: an offset ("+00:00") is a hand edit the app never writes
    # (code review of increment 002, F1)
    return value if when.tzinfo is None else None


@dataclass
class BoardEntry:
    id: str
    name: str
    color: str
    path: str
    last_opened: str | None = None
    archived: bool = False


@dataclass
class Registry:
    path: Path
    entries: list[BoardEntry]
    last: str | None = None
    load_report: dict = field(default_factory=dict)
    main_path: str | None = None        # the default board's file, never skipped

    # ---- reading -----------------------------------------------------------
    @classmethod
    def load(cls, path, main_path) -> "Registry":
        """Never raises. Missing → the default board alone; unreadable → the
        same, after copying the file to `boards.json.corrupt`."""
        path, main = Path(path), Path(main_path)
        main_entry = BoardEntry(MAIN_ID, MAIN_NAME, "violet", str(main))
        if not path.exists():
            return cls(path, [main_entry], MAIN_ID, main_path=str(main))
        try:
            reg = cls._read(path, str(main))
        except OSError:
            reg = None
        if reg is None:
            backup = keep_aside(path)
            return cls(path, [main_entry], MAIN_ID,
                       {"unreadable": True, "backup": str(backup) if backup else None},
                       main_path=str(main))
        return reg

    @classmethod
    def _read(cls, path: Path, main_path: str | None) -> "Registry | None":
        """The registry as the file holds it now, or None when it cannot be parsed
        (not JSON, or not an object holding a `boards` list); a failed read raises."""
        data = path.read_bytes()
        try:
            raw = clean_strings(json.loads(data.decode("utf-8")))
        except (ValueError, RecursionError):
            raw = None
        if not isinstance(raw, dict) or not isinstance(raw.get("boards"), list):
            return None
        reg = cls(path, [], main_path=main_path)
        seen_paths: set[str] = set()
        for item in raw["boards"]:
            if not isinstance(item, dict):
                continue
            p = item.get("path")
            if not isinstance(p, str) or not p.strip() or not _expand_home(p).is_absolute():
                continue      # a relative path would resolve against wherever the app ran
            try:
                key = _key(p)
            except (OSError, ValueError, RuntimeError):
                continue
            if key in seen_paths:
                continue
            seen_paths.add(key)
            name = item.get("name")
            name = (clean_name(name) if isinstance(name, str) else "") or _name_for(p)
            bid = item.get("id")
            if not (isinstance(bid, str) and _ID.fullmatch(bid)
                    and bid not in {e.id for e in reg.entries}):
                bid = reg._unique_id(slug(name))
            reg.entries.append(BoardEntry(bid, name, project_color_on_load(item.get("color")),
                                          str(_expand_home(p)),     # no `~` past the door
                                          _iso_or_none(item.get("last_opened")),
                                          item.get("archived") is True))
        if not reg.entries and main_path:
            reg.entries = [BoardEntry(MAIN_ID, MAIN_NAME, "violet", main_path)]
        last = raw.get("last")
        reg.last = last if isinstance(last, str) and any(e.id == last for e in reg.entries) \
            else None
        return reg

    @classmethod
    def single(cls, board_path) -> "Registry":
        """The registry of one board, read from nothing: what an app built without
        a registry holds (the suite builds hundreds). Its file would sit beside the
        board, so a board created from it lands there too, never in the home."""
        p = Path(board_path)
        return cls(p.parent / REGISTRY_NAME, [BoardEntry(MAIN_ID, MAIN_NAME, "violet", str(p))],
                   MAIN_ID, main_path=str(p))

    def get(self, bid: str) -> BoardEntry | None:
        return next((e for e in self.entries if e.id == bid), None)

    def active(self) -> list[BoardEntry]:
        return [e for e in self.entries if not e.archived]

    def opening(self) -> BoardEntry:
        """The board a plain start opens: the last one when it is active, else the
        first active one, else the first — skipping a board whose file is missing
        (`Board.load` would seed sample data there), which `load_report`'s
        `missing` then names; the default board is never skipped (ux UX-10)."""
        last = self.get(self.last) if self.last else None
        order = ([last] if last is not None and not last.archived else []) \
            + self.active() + self.entries
        for e in order:
            if self._is_main(e) or Path(e.path).exists():
                if e is not order[0]:
                    self.load_report.setdefault("missing", order[0].path)
                return e
        # nothing openable: the default board, created as a first start does
        self.load_report.setdefault("missing", order[0].path)
        main = next((e for e in self.entries if self._is_main(e)), None)
        if main is None and self.main_path:
            main = BoardEntry(self._unique_id(MAIN_ID), MAIN_NAME, "violet", self.main_path)
            self.entries.append(main)
        return main or order[0]

    def _is_main(self, e: BoardEntry) -> bool:
        return self.main_path is not None and _key(e.path) == _key(self.main_path)

    def entry_for(self, path) -> BoardEntry | None:
        key = _key(path)
        return next((e for e in self.entries if _key(e.path) == key), None)

    # ---- writing -----------------------------------------------------------
    def _unique_id(self, base: str, taken: set[str] | None = None) -> str:
        ids = {e.id for e in self.entries} | (taken or set())
        bid, n = base, 2
        while bid in ids:
            bid, n = f"{base}-{n}", n + 1
        return bid

    def free_color(self) -> str:
        used = {e.color for e in self.active()}
        return next((c for c in PROJECT_COLORS if c not in used), "violet")

    def _commit(self, change):
        """Apply `change` to the registry as the file holds it NOW and write the
        result, under the registry's lock, so another taskboard's change since this
        one read the file is kept; then hold that result here — an entry this
        registry already holds is updated in place, so the app's references to it
        stay live, and one only memory holds stays in memory. A file that cannot be
        read, or cannot be parsed and cannot be copied aside, is never written over;
        a failed write changes nothing here. Returns `change`'s result."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with file_lock(self.path):
            fresh = None
            if self.path.exists():
                fresh = self._read(self.path, self.main_path)   # a failed read raises
                if fresh is None and not self._set_aside():
                    raise OSError(f"{self.path.name} cannot be read and could not be "
                                  "copied aside, so it was not written")
            if fresh is None:
                fresh = copy.deepcopy(self)
            result = change(fresh)
            fresh.save()
        mine = {e.id: e for e in self.entries}
        entries = []
        for e in fresh.entries:
            old = mine.get(e.id)
            if old is not None:
                old.__dict__.update(e.__dict__)
                e = old
            entries.append(e)
        ids = {e.id for e in entries}
        entries += [e for e in self.entries
                    if e.id not in ids and fresh.entry_for(e.path) is None]
        self.entries, self.last = entries, fresh.last
        return result

    def _set_aside(self) -> bool:
        """Whether the unparseable registry's bytes are kept: empty (nothing to
        keep), already the copy this registry's load made, or copied now."""
        try:
            data = self.path.read_bytes()
        except OSError:
            return False
        if not data:
            return True
        backup = self.load_report.get("backup")
        try:
            if backup and Path(backup).read_bytes() == data:
                return True
        except OSError:
            pass
        return keep_aside(self.path) is not None

    def _carry(self, fresh: "Registry", bid: str) -> BoardEntry | None:
        """`bid` in the registry just read: its own entry, or this one's copied in
        when the file lacks it (the default board a start added)."""
        e = fresh.get(bid)
        mine = self.get(bid)
        if e is None and mine is not None and fresh.entry_for(mine.path) is None:
            e = copy.deepcopy(mine)
            fresh.entries.append(e)
        return e

    def register(self, path) -> BoardEntry:
        """The entry for `path`: the existing one (un-archived), or a new one named
        after the file, in the first colour no active board wears."""
        entry = self.entry_for(path)
        if entry is not None and not entry.archived:
            return entry

        def change(r):
            e = r.entry_for(path)
            if e is None:
                p = str(_expand_home(path).resolve())
                name = _name_for(p)
                # unique against memory too: an entry only memory holds keeps its id (F5)
                e = BoardEntry(r._unique_id(slug(name), {x.id for x in self.entries}), name,
                               r.free_color(), p)
                r.entries.append(e)
            e.archived = False
            return e.id
        return self.get(self._commit(change))

    def create(self, name: str, color: str, now: datetime, settings: dict) -> BoardEntry:
        """A new board in its own folder `boards/<slug>/` beside the registry:
        an empty board file (no project, no task, the default phases, `settings`),
        never written into a folder that already exists. Raises `ValueError` for
        a name that is empty once cleaned."""
        name = clean_name(name)
        if not name:
            raise ValueError("a board needs a name")
        made = []

        def change(r):
            root = r.path.parent / "boards"
            taken = {e.id for e in r.entries} | (
                {p.name.lower() for p in root.iterdir()} if root.is_dir() else set())
            bid = self._unique_id(slug(name), taken)    # unique against the file and the disk
            folder = root / bid
            folder.mkdir(parents=True, exist_ok=False)
            made.append(folder)
            Board([], [], folder / "board.json", dict(settings)).save_atomic()
            r.entries.append(BoardEntry(bid, name, color if color in PROJECT_COLORS else "violet",
                                        str((folder / "board.json").resolve()),
                                        now.isoformat(timespec="minutes")))
            return bid
        try:
            return self.get(self._commit(change))
        except OSError:
            for folder in made:     # the folder this call made, and only it (code review F1)
                shutil.rmtree(folder, ignore_errors=True)
            raise

    def next_id(self, name: str) -> str:
        """The id — and folder name — a board of this name would get: its slug,
        made unique against the registry and the folders already under `boards/`."""
        root = self.path.parent / "boards"
        taken = {p.name.lower() for p in root.iterdir()} if root.is_dir() else set()
        return self._unique_id(slug(clean_name(name)), taken)

    def edit(self, bid: str, name: str, color: str) -> None:
        name = clean_name(name)
        if self.get(bid) is None or not name:
            return

        def change(r):
            e = self._carry(r, bid)
            if e is not None:
                e.name = name
                e.color = color if color in PROJECT_COLORS else e.color
        self._commit(change)

    def archive(self, bid: str) -> None:
        if self.get(bid) is None:
            return

        def change(r):
            e = self._carry(r, bid)
            if e is not None:
                e.archived = True
        self._commit(change)

    def touch(self, bid: str, now: datetime) -> None:
        """Record `bid` as the board opened last — on disk only when the registry
        holds more than one board or its file already exists."""
        entry = self.get(bid)
        if entry is None:
            return
        stamp = now.isoformat(timespec="minutes")
        self.last, entry.last_opened = bid, stamp
        if self.load_report.get("unreadable"):
            return      # the unreadable file stays as it was until the operator changes a board
        if len(self.entries) > 1 or self.path.exists():

            def change(r):
                e = self._carry(r, bid)
                if e is not None:
                    r.last, e.last_opened = bid, stamp
            try:
                self._commit(change)
            except OSError as exc:      # bookkeeping: never worth stopping a start
                self.load_report["save_error"] = f"{type(exc).__name__}: {exc}"

    def save(self) -> None:
        """Atomic, as the board file is (`models.write_atomic`)."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {"version": 1, "last": self.last, "boards": [asdict(e) for e in self.entries]}
        write_atomic(self.path, json.dumps(data, indent=2, ensure_ascii=False))


# ---- presence: a board open in another window (batch 2026-10-20-batch-03) --------
def presence_dir() -> Path:
    """`~/.taskboard/open/`: the home's (Main's folder), never another board's."""
    return default_board_path().parent / "open"


def _presence_stem(path) -> str:
    return hashlib.sha256(_key(path).encode("utf-8")).hexdigest()[:16]


def announce(path, now: datetime) -> Path | None:
    """This window's marker for the board at `path`: `<file hash>-<token>.json`,
    created exclusively, holding `{"since", "pid"}`; a failed write removes it. None
    when it cannot be made — presence never stops a start."""
    try:
        folder = presence_dir()
        folder.mkdir(parents=True, exist_ok=True)
        marker = folder / f"{_presence_stem(path)}-{os.urandom(16).hex()}.json"
        fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except OSError:
        return None
    try:
        os.write(fd, json.dumps({"since": now.isoformat(timespec="minutes"),
                                 "pid": os.getpid()}).encode("utf-8"))
    except OSError:
        os.close(fd)
        try:
            os.unlink(marker)       # never an empty marker that reads as a window (S-7)
        except OSError:
            pass
        return None
    os.close(fd)
    return marker


def renew(marker: Path | None) -> bool:
    """Renew the marker's time; False when it is gone."""
    if marker is None:
        return False
    try:
        os.utime(marker)
        return True
    except OSError:
        return False


def withdraw(marker: Path | None) -> None:
    """Remove this window's own marker; errors ignored."""
    if marker is None:
        return
    try:
        os.unlink(marker)
    except OSError:
        pass


def _since(marker: Path) -> datetime | None:
    """A marker's `since`, read from at most its first 4096 bytes; anything but a JSON
    object holding a parseable string `since` is None (S-2)."""
    try:
        with open(marker, "rb") as fh:
            data = json.loads(fh.read(_PRESENCE_READ).decode("utf-8"))
        since = datetime.fromisoformat(data["since"]) if isinstance(data.get("since"), str) \
            else None
        # a local time only, as taskboard writes it: an offset could not be ordered
        # beside the others (security S-13)
        return since if since is None or since.tzinfo is None else None
    except (OSError, ValueError, TypeError, AttributeError, KeyError, RecursionError):
        return None


def open_elsewhere(path, mine: Path | None = None) -> list[datetime | None]:
    """The `since` (or None) of every fresh marker of the board at `path` but `mine`. A
    marker is read only as a regular file (`lstat`) whose whole name is this board's
    pattern; one more than `PRESENCE_STALE` seconds from now (its mtime, never its
    `since`) is a dead window's and is removed once a second `lstat` shows it
    unchanged. Nothing raises."""
    stem = _presence_stem(path)
    pattern = re.compile(re.escape(stem) + r"-[0-9a-f]{32}\.json")
    try:
        names = os.listdir(presence_dir())
    except OSError:
        return []
    out = []
    for name in sorted(names):
        if not pattern.fullmatch(name):
            continue
        marker = presence_dir() / name
        if mine is not None and marker == mine:
            continue
        try:
            st = os.lstat(marker)
        except OSError:
            continue
        if not stat.S_ISREG(st.st_mode):
            continue
        if abs(time.time() - st.st_mtime) > PRESENCE_STALE:
            try:
                again = os.lstat(marker)
                if (again.st_mtime_ns, again.st_ino) == (st.st_mtime_ns, st.st_ino):
                    os.unlink(marker)       # a dead window's (S-5: unchanged meanwhile)
            except OSError:
                pass
            continue
        out.append(_since(marker))
    return out


def peek_board(path) -> Board:
    """A board read without writing: `Board.load` for a file that exists (it
    writes nothing then), an empty unsaved board for one that does not —
    `Board.load` would seed and SAVE sample data there."""
    p = Path(path)
    if not p.exists():
        return Board([], [], p)
    try:
        readable = isinstance(json.loads(p.read_text(encoding="utf-8")), dict)
    except (OSError, ValueError, RecursionError):
        readable = False
    if not readable:
        board = Board([], [], p)
        board._load_report = {"file_unreadable": True, "backup": None,
                              "projects_rescued": 0, "tasks_rescued": 0}
        return board
    return Board.load(p)


# ---- moving a project to another board (HLR-2206) ---------------------------
@dataclass
class MovePlan:
    tasks: list                          # every task of the project, in board order
    kept: int                            # links between two of them
    crossing: list                       # (waiter, waits on) pairs that cross the boards
    refusal: str | None = None
    dst_stamp: tuple | None = None       # the target file's (mtime, size) when planned


def _inside(child: Path, parent: Path) -> bool:
    try:
        c, p = child.resolve(), parent.resolve()
    except (OSError, RuntimeError):
        return False
    return os.path.normcase(str(c)).startswith(os.path.normcase(str(p)) + os.sep)


def move_plan(src: Board, dst: Board, project_id: str, src_team: set | None,
              dst_team: set | None) -> MovePlan:
    """What a move would do, and whether it may (a refusal reason, or None)."""
    mine = [t for t in src.tasks if t.project_id == project_id]
    ids = {t.id for t in mine}
    by = {t.id: t for t in src.tasks}
    crossing_in, crossing_out, kept = [], [], 0
    for t in src.tasks:
        for dep in t.depends_on:
            if t.id in ids and dep in ids:
                kept += 1
            elif t.id in ids and dep in by:
                crossing_out.append((t, by[dep]))
            elif t.id not in ids and dep in ids:
                crossing_in.append((t, by[dep]))
    plan = MovePlan(mine, kept, crossing_in + crossing_out)
    plan.dst_stamp = _stamp(dst.path)
    plan.refusal = _refusal(src, dst, project_id, mine, src_team, dst_team)
    return plan


def _samefile(a, b) -> bool:
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


def _stamp(path: Path) -> tuple | None:
    """What a stale plan is checked against: the file's mtime and size."""
    if not path.exists():
        return None
    st = path.stat()
    return (st.st_mtime_ns, st.st_size)


def _refusal(src, dst, pid, mine, src_team, dst_team) -> str | None:
    if _key(src.path) == _key(dst.path) or _samefile(src.path, dst.path):
        return "the target is this board"
    if _key(src.path.parent) == _key(dst.path.parent):
        # history.jsonl and images/ live beside the board file: one folder, one
        # history — moving lines inside it would erase them (code review F1)
        return "the two boards share a folder (their history and images are one)"
    if not dst.path.exists():
        return "the target board's file is missing"
    if dst.load_report.get("file_unreadable"):
        return "the target board's file cannot be read"
    if src_team is None or dst_team is None:
        return "a board is in team mode and its team configuration cannot be read"
    if pid in src_team or pid in dst_team:
        return "the project is shared in team mode"
    for x in [pid] + [t.id for t in mine]:
        if not (isinstance(x, str) and _ID.fullmatch(x)):
            return f"the id {x!r} cannot name a folder"
    dst_ids = {p.id for p in dst.projects} | {t.id for t in dst.tasks}
    clash = [x for x in [pid] + [t.id for t in mine] if x in dst_ids]
    if clash:
        return f"the target already holds the id {clash[0]}"
    for t in mine:
        if dst.image_dir(t.id).exists():
            return f"the target already holds images/{t.id}"
    phases = {p.strip().lower() for p in dst.phases}
    missing = sorted({t.phase for t in mine if t.phase.strip().lower() not in phases})
    if missing:
        return f"the target has no phase {missing[0]!r} — add it there first (f)"
    return None


def _backup(path: Path, day: str) -> Path | None:
    """A byte copy beside `path`, created exclusively: an earlier copy is never
    replaced (`-2`, `-3`… instead)."""
    if not path.exists():
        return None
    n = 1
    while True:
        dest = path.with_name(f"{path.name}.pre-move-{day}" + (f"-{n}" if n > 1 else ""))
        try:
            out = open(dest, "xb")
        except FileExistsError:
            n += 1
            continue
        try:
            with out, open(path, "rb") as src:
                shutil.copyfileobj(src, out)
        except BaseException:
            dest.unlink(missing_ok=True)    # never a partial copy that looks whole (S-5)
            raise
        return dest


def _log(folder: Path, day: str, entry: dict) -> None:
    """Append `entry` to the list in `move-<day>.json`; a file that does not hold
    a list is left alone and the next free `move-<day>-N.json` takes it."""
    n = 1
    while True:
        p = folder / (f"move-{day}" + (f"-{n}" if n > 1 else "") + ".json")
        if not p.exists():
            items = []
            break
        try:
            items = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError, RecursionError):
            items = None
        if isinstance(items, list):
            break
        n += 1
    write_atomic(p, json.dumps(items + [entry], indent=2, ensure_ascii=False))


def move_project(src: Board, dst: Board, project_id: str, plan: MovePlan, day: str,
                 names: tuple[str, str]) -> tuple[Board, list[str]]:
    """Carry the project out on COPIES of both boards; return the new source
    board and the steps done. Order: the byte copies, the target saved, the
    source saved — the live boards are never changed, so a failure before the
    source is saved leaves the open board as its file — then the image folders,
    the history lines and the move logs. An `OSError` carries `.steps`, and
    `.board`: the new source once it was saved (the caller adopts it), else None."""
    steps: list[str] = []
    saved = None
    held = ExitStack()
    try:
        if plan.refusal:
            raise OSError(plan.refusal)
        # the target is held from the stale-plan check to its save, so another
        # taskboard's move cannot write it in between (batch 2026-10-20-batch-02)
        beat = held.enter_context(file_lock(dst.path, names[1]))
        if _stamp(dst.path) != plan.dst_stamp:
            raise OSError("the target board changed since the move was planned")
        new_src, new_dst = copy.deepcopy(src), copy.deepcopy(dst)
        ids = {t.id for t in plan.tasks}
        for b in (src, dst):
            if _backup(b.path, day):
                steps.append(f"copied {b.path.name}")
            beat()      # a copy can take a while on a slow drive (security S-2, S-8)
        if _backup(src.path.parent / "history.jsonl", day):
            steps.append("copied history.jsonl")    # rewritten below (security N1)
        beat()
        proj = new_src.project_by_id(project_id)
        proj.present_rank = None
        moving = [t for t in new_src.tasks if t.id in ids]
        images = (src.path.parent / "images").resolve()
        # the folders that move: a task's own, directly under the source's images/
        # (a junction or link elsewhere stays, and so do the references into it)
        img_src = {t.id: src.image_dir(t.id) for t in moving
                   if src.image_dir(t.id).is_dir()
                   and src.image_dir(t.id).resolve().parent == images}
        for t in moving:
            t.depends_on = [d for d in t.depends_on if d in ids]
            old_dir, new_dir = img_src.get(t.id), dst.image_dir(t.id)
            refs = []
            for ref in t.images:
                r = Path(ref)
                if old_dir is not None and r.is_absolute() and _inside(r, old_dir):
                    refs.append(str(new_dir / r.resolve().relative_to(old_dir.resolve())))
                else:
                    refs.append(ref)
            t.images = refs
        new_src.tasks = [t for t in new_src.tasks if t.id not in ids]
        for t in new_src.tasks:
            t.depends_on = [d for d in t.depends_on if d not in ids]
        new_src.projects = [p for p in new_src.projects if p.id != project_id]
        new_dst.projects.append(proj)
        new_dst.tasks.extend(moving)
        new_dst.path.parent.mkdir(parents=True, exist_ok=True)
        new_dst.save_atomic()
        steps.append("saved the target")
        held.close()
        new_src.save_atomic()
        saved = new_src
        steps.append("saved the source")
        for tid, old_dir in img_src.items():
            target = dst.image_dir(tid)
            target.parent.mkdir(parents=True, exist_ok=True)
            tmp = target.parent / f".{tid}.moving"
            shutil.rmtree(tmp, ignore_errors=True)
            try:
                shutil.copytree(old_dir, tmp, symlinks=True)
                os.replace(tmp, target)
            except OSError:
                shutil.rmtree(tmp, ignore_errors=True)
                raise
            shutil.rmtree(old_dir)
            steps.append(f"moved images/{tid}")
        hist = src.path.parent / "history.jsonl"
        if hist.exists():
            keep, moved = [], []
            for line in hist.read_text(encoding="utf-8", errors="replace").splitlines():
                try:
                    rec = json.loads(line)
                except (ValueError, RecursionError):
                    rec = None
                task = rec.get("task") if isinstance(rec, dict) else None
                (moved if isinstance(task, str) and task in ids else keep).append(line)
            if moved:
                target_hist = dst.path.parent / "history.jsonl"
                # F6: never glue the first moved line onto a hand-edited last one
                lead = ("\n" if target_hist.exists() and target_hist.stat().st_size
                        and not target_hist.read_bytes().endswith(b"\n") else "")
                with open(target_hist, "a", encoding="utf-8") as fh:
                    fh.write(lead)
                    fh.writelines(x + "\n" for x in moved)
                write_atomic(hist, "".join(x + "\n" for x in keep))
                steps.append("moved the history lines")
        entry = {"date": day, "project": proj.name, "from": names[0], "to": names[1],
                 "tasks": len(moving), "links_kept": plan.kept,
                 "links_dropped": [{"task": a.title, "waits_on": b.title}
                                   for a, b in plan.crossing]}
        for b in (src, dst):
            _log(b.path.parent, day, entry)
        steps.append("wrote the move logs")
        return new_src, steps
    except OSError as exc:
        exc.steps = steps
        exc.board = saved      # past the source save: the caller must adopt it
        raise
    except Exception as exc:   # any other failure is reported the same way (F2)
        err = OSError(f"{type(exc).__name__}: {exc}")
        err.steps, err.board = steps, saved
        raise err from exc
    finally:
        held.close()       # a no-op once released after the target's save
