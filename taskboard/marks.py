"""The milestone-class directory (batch 2026-10-24-batch-01).

One directory for every board, `marks.json` beside the boards registry
(`~/.taskboard/marks.json`): a class is an id, a name, a shape, a colour and a
hidden flag. The id is a slug of the name, made as `people.handle_for` makes
handles, and never changes when the class is renamed. A task's `mark` names a
class; the directory is the one source of names, shapes and colours, and it
never leaves the home — team sync pushes the id inside the task, nothing of
the directory.

The file is read like the people directory: never raising, a bad entry
skipped, an unreadable file copied aside first. It is written atomically,
under its lock file, as a read-modify-write, so another taskboard's change is
never written over (the people directory's pattern, its byte-level sibling).
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from .boards import file_lock, keep_aside
from .models import clean_strings, write_atomic
from .people import _HANDLE, _clean, handle_for

MARKS_NAME = "marks.json"
NAME_MAX = 60

#: the manager's one-cell shape set (the round's glyph sheet, proto.py:85).
#: `◆` stands apart as the unclassified mark's glyph — it is NOT a member, so
#: no class saved through `add`/`edit` can fail the load validation below.
SHAPES = ["▲", "■", "⬢", "★", "⬟", "▼", "✦", "⚑"]
#: the class colours, the app's named tones (views.HEX) the round's swatch uses.
COLOURS = ["cyan", "amber", "violet", "pink", "green", "orange", "sky", "lime"]


@dataclass
class Mark:
    id: str          # the slug: `payment` — stable on rename (MM-D2)
    name: str
    shape: str
    colour: str
    hidden: bool = False


class Directory:
    """The milestone classes of every board, in memory as the file held them
    when read or last written here. `marks` is one live dict (id → Mark) the
    app hands to every board it opens, so a class added or renamed shows at
    once. The file starts empty — nothing is written until a class is added."""

    def __init__(self, path, marks: list[Mark] | None = None,
                 load_report: dict | None = None) -> None:
        self.path = Path(path)
        self.marks: dict[str, Mark] = {}
        self.load_report = load_report or {}
        self._stamp: tuple[int, int] | None = None
        self._hold(marks or [])

    def _hold(self, marks: list[Mark]) -> None:
        self.marks.clear()
        self.marks.update((m.id, m) for m in marks)

    def _stamped(self) -> None:
        """Best-effort: the file's (mtime, size) as of the last read or write here."""
        try:
            stat = self.path.stat()
            self._stamp = (stat.st_mtime_ns, stat.st_size)
        except OSError:
            pass

    # ---- reading -----------------------------------------------------------
    @classmethod
    def load(cls, path) -> "Directory":
        """Never raises. Missing → empty; unreadable → empty, after copying the
        file to `marks.json.corrupt` (the first free name — an earlier copy is
        never replaced)."""
        path = Path(path)
        try:
            if not path.exists() or not path.read_bytes().strip():
                directory = cls(path)       # nothing written yet, or nothing to keep
                directory._stamped()
                return directory
            marks = cls._read(path)
        except OSError:
            marks = None
        if marks is None:
            backup = keep_aside(path)
            directory = cls(path, [], {"unreadable": True,
                                       "backup": str(backup) if backup else None})
        else:
            directory = cls(path, marks)
        directory._stamped()
        return directory

    def refresh(self) -> bool | None:
        """The file another window may have changed, re-read on change only:
        None unchanged · True reloaded · False the file could not be parsed —
        the in-memory directory is kept, the caller says so once (HD-5)."""
        try:
            stat = self.path.stat()
            stamp = (stat.st_mtime_ns, stat.st_size)
        except OSError:
            return None                     # gone or unreadable metadata: keep what we hold
        if stamp == self._stamp:
            return None
        try:
            marks = self._read(self.path)   # None when unparseable; may raise OSError
        except OSError:
            marks = None
        self._stamp = stamp                 # a bad file is not re-parsed and re-reported on every open
        if marks is None:
            return False
        self._hold(marks)
        return True

    @staticmethod
    def _read(path: Path) -> list[Mark] | None:
        """The classes the file holds now, or None when it cannot be parsed (not
        JSON, or not an object with a `marks` list); a failed read raises. An
        entry with a malformed or repeated id, no name, an unknown shape or
        colour, or a field of the wrong type is skipped; `hidden` is coerced
        to bool; every whitespace run in the name becomes one space."""
        data = path.read_bytes()
        try:
            raw = clean_strings(json.loads(data.decode("utf-8")))
        except (ValueError, RecursionError):
            return None
        if not isinstance(raw, dict) or not isinstance(raw.get("marks"), list):
            return None
        out: list[Mark] = []
        seen: set[str] = set()
        for item in raw["marks"]:
            if not isinstance(item, dict):
                continue
            mid, name = item.get("id"), _clean(item.get("name"), NAME_MAX)
            shape, colour = item.get("shape"), item.get("colour")
            if not (isinstance(mid, str) and _HANDLE.fullmatch(mid)) or mid in seen or not name:
                continue
            if not (isinstance(shape, str) and shape in SHAPES):
                continue
            if not (isinstance(colour, str) and colour in COLOURS):
                continue
            seen.add(mid)
            out.append(Mark(mid, name, shape, colour, bool(item.get("hidden"))))
        return out

    def find(self, q: str) -> Mark | None:
        """The class whose name starts with `q`, lower case — a prefix only,
        never a match inside the name (the round's `find_class`, proto.py:500;
        the manager and the `/#cls` search use it)."""
        q = q.strip().lower()
        return next((m for m in sorted(self.marks.values(),
                                       key=lambda m: (m.name.lower(), m.id))
                     if m.name.lower().startswith(q)), None)

    # ---- writing -----------------------------------------------------------
    def _commit(self, change) -> object:
        """Apply `change` to the classes as the file holds them NOW and write
        the result, under the file's lock; then hold that result here. A file
        that cannot be parsed and cannot be copied aside is never written over;
        a failed write raises `OSError` and changes nothing here."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with file_lock(self.path):
            marks = None
            if self.path.exists():
                marks = self._read(self.path)           # a failed read raises
                if marks is None and not self._set_aside():
                    raise OSError(f"{self.path.name} cannot be read and could not be "
                                  "copied aside, so it was not written")
            fresh = {m.id: m for m in (marks if marks is not None
                                       else list(self.marks.values()))}
            result = change(fresh)
            data = {"version": 1, "marks": [asdict(m) for m in fresh.values()]}
            write_atomic(self.path, json.dumps(data, indent=2, ensure_ascii=False))
        self._hold(list(fresh.values()))
        self._stamped()
        return result

    def _set_aside(self) -> bool:
        """Whether the unparseable file's bytes are kept: empty (nothing to
        keep), already the copy this directory's load made, or copied now."""
        try:
            data = self.path.read_bytes()
        except OSError:
            return False
        backup = self.load_report.get("backup")
        try:
            if not data or (backup and Path(backup).read_bytes() == data):
                return True
        except OSError:
            pass
        return keep_aside(self.path) is not None

    def add(self, name: str, shape: str, colour: str) -> Mark:
        """A new class: the id comes from the name (`Payment` → `payment`,
        `payment2` when taken — in the file or here), `hidden` False. Raises
        `ValueError` for a name with nothing left once cleaned or a shape or
        colour outside the sets, `OSError` when it cannot be saved."""
        name = _clean(name, NAME_MAX)
        if not name:
            raise ValueError("a class needs a name")
        if shape not in SHAPES:
            raise ValueError(f"not a shape: {shape!r}")
        if colour not in COLOURS:
            raise ValueError(f"not a colour: {colour!r}")

        def change(fresh: dict[str, Mark]) -> Mark:
            m = Mark(handle_for(name, set(fresh) | set(self.marks)), name, shape, colour)
            fresh[m.id] = m
            return m
        return self._commit(change)

    def edit(self, cls_id: str, name: str, shape: str, colour: str) -> Mark:
        """A class's name, shape and colour; the id never changes and its
        hidden flag is kept. A class the file no longer holds is written back.
        Raises like `add`."""
        name = _clean(name, NAME_MAX)
        if not name:
            raise ValueError("a class needs a name")
        if not _HANDLE.fullmatch(cls_id):
            raise ValueError(f"not a class id: {cls_id!r}")
        if shape not in SHAPES:
            raise ValueError(f"not a shape: {shape!r}")
        if colour not in COLOURS:
            raise ValueError(f"not a colour: {colour!r}")

        def change(fresh: dict[str, Mark]) -> Mark:
            held = fresh.get(cls_id) or self.marks.get(cls_id)
            m = Mark(cls_id, name, shape, colour, bool(held.hidden) if held else False)
            fresh[cls_id] = m
            return m
        return self._commit(change)

    def set_hidden(self, cls_id: str, hidden: bool) -> Mark:
        """The class's hidden flag, persisted like any other write; nothing else
        of the class changes. Raises `ValueError` for an id the directory does
        not hold, `OSError` when it cannot be saved."""
        if not _HANDLE.fullmatch(cls_id):
            raise ValueError(f"not a class id: {cls_id!r}")

        def change(fresh: dict[str, Mark]) -> Mark:
            held = fresh.get(cls_id) or self.marks.get(cls_id)
            if held is None:
                raise ValueError(f"no such class: {cls_id!r}")
            m = Mark(cls_id, held.name, held.shape, held.colour, bool(hidden))
            fresh[cls_id] = m
            return m
        return self._commit(change)
