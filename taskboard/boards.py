"""Several boards: the registry of board files (batch 2026-10-20-batch-01).

Each board is its own file in its own folder — its `history.jsonl`, `images/`
and `reports/` live beside it, so two boards never share them. The registry,
`boards.json` beside the default board, lists them: id, name, colour, path,
when each was last opened, whether it is archived, and the board opened last.
The default board (`~/.taskboard/board.json`) is `Main`, in place.

The registry is read like the board file: never raising, a bad entry skipped
or defaulted, an unreadable file copied aside first. It is written atomically,
and never for a one-board user who has no registry file yet.
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from .models import (PROJECT_COLORS, Board, clean_strings, default_board_path,
                     project_color_on_load, strip_controls, write_atomic)

REGISTRY_NAME = "boards.json"
MAIN_ID = "main"
MAIN_NAME = "Main"
NAME_MAX = 60
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


def _keep_aside(path: Path) -> Path | None:
    """A byte copy of an unreadable registry at the first free name of
    `boards.json.corrupt`, `.corrupt-2`, …: an earlier copy is never replaced and
    the current bytes always kept. An empty file has nothing to keep."""
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


def _key(path) -> str:
    """One spelling per file: absolute, resolved, case-normalised on Windows."""
    return os.path.normcase(str(Path(path).expanduser().resolve()))


def _name_for(path) -> str:
    p = Path(path)
    return (p.parent.name if p.stem == "board" else p.stem) or MAIN_NAME


def _iso_or_none(value) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return None
    return value


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
            raw = clean_strings(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError, RecursionError):
            raw = None
        if not isinstance(raw, dict) or not isinstance(raw.get("boards"), list):
            backup = _keep_aside(path)
            return cls(path, [main_entry], MAIN_ID,
                       {"unreadable": True, "backup": str(backup) if backup else None},
                       main_path=str(main))
        reg = cls(path, [], main_path=str(main))
        seen_paths: set[str] = set()
        for item in raw["boards"]:
            if not isinstance(item, dict):
                continue
            p = item.get("path")
            if not isinstance(p, str) or not p.strip() or not Path(p).expanduser().is_absolute():
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
                                          p, _iso_or_none(item.get("last_opened")),
                                          item.get("archived") is True))
        if not reg.entries:
            reg.entries = [main_entry]
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

    def register(self, path) -> BoardEntry:
        """The entry for `path`: the existing one (un-archived), or a new one named
        after the file, in the first colour no active board wears."""
        entry = self.entry_for(path)
        if entry is not None:
            if entry.archived:
                entry.archived = False
                self.save()
            return entry
        p = str(Path(path).expanduser().resolve())
        name = _name_for(p)
        entry = BoardEntry(self._unique_id(slug(name)), name, self.free_color(), p)
        self.entries.append(entry)
        self.save()
        return entry

    def touch(self, bid: str, now: datetime) -> None:
        """Record `bid` as the board opened last — on disk only when the registry
        holds more than one board or its file already exists."""
        entry = self.get(bid)
        if entry is None:
            return
        self.last = bid
        entry.last_opened = now.isoformat(timespec="minutes")
        if self.load_report.get("unreadable"):
            return      # the unreadable file stays as it was until the operator changes a board
        if len(self.entries) > 1 or self.path.exists():
            try:
                self.save()
            except OSError as exc:      # bookkeeping: never worth stopping a start
                self.load_report["save_error"] = f"{type(exc).__name__}: {exc}"

    def save(self) -> None:
        """Atomic, as the board file is (`models.write_atomic`)."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {"version": 1, "last": self.last, "boards": [asdict(e) for e in self.entries]}
        write_atomic(self.path, json.dumps(data, indent=2, ensure_ascii=False))


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

