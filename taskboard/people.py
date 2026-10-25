"""The people directory and the `@` mentions (batch 2026-10-21-batch-01).

One directory for every board, `people.json` beside the boards registry
(`~/.taskboard/people.json`): a person is a handle, a name, a role and an
optional one-line note. The handle is the person's stable id and the form a
mention takes in the notes — `@ana.ruiz` — derived from the name when the
person is added and never changed, so renaming someone changes only how their
mentions are drawn. A note's people are read from its text; nothing else holds
them.

The file is read like the registry: never raising, a bad entry skipped, an
unreadable file copied aside first. It is written atomically, under its lock
file, as a read-modify-write, so another taskboard's change is never written
over (the registry's pattern, batch 2026-10-20-batch-02). It never leaves the
home: team sync pushes board tasks, and a mention travels in a note as its
handle text only.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

from .boards import file_lock, keep_aside
from .models import clean_strings, strip_controls, write_atomic

PEOPLE_NAME = "people.json"
NAME_MAX = 60
ROLE_MAX = 60
NOTE_MAX = 200

#: a handle: lowercase letters and digits in words joined by `.`, `_` or `-` (one
#: spelling, so a handle is always a mention; code review CR-4)
_H = r"[a-z0-9]+(?:[._-][a-z0-9]+)*"
_HANDLE = re.compile(_H)
#: a mention: `@handle` at a word start (never inside `ana@x.com`), or the link form
#: `@[Name](p:handle)`, read too so an imported note is understood
#  (the link's name is bounded: an unbounded one rescans the line at every `@[` — a
#  crafted note of `@[` repeated took seconds per render; security S-1)
MENTION_RE = re.compile(r"(?<![\w.@])@(?:\[([^\]\n]{1,60})\]\(p:(" + _H + r")\)|(" + _H + r"))")


@dataclass
class Person:
    id: str          # the handle: `ana.ruiz`
    name: str
    role: str = ""
    note: str = ""


def fold(s: str) -> str:
    """Lower case, accents dropped: `Andrés` → `andres`."""
    return "".join(ch for ch in unicodedata.normalize("NFKD", s.lower())
                   if not unicodedata.combining(ch))


def _clean(value, cap: int) -> str:
    """One line of text as stored: no control byte, no line break, at most `cap`."""
    if not isinstance(value, str):
        return ""
    return " ".join(strip_controls(value).split())[:cap].strip()


def mention_ids(text: str) -> list[str]:
    """The handles a text mentions, first mention first, each once."""
    if "@" not in (text or ""):
        return []
    # a dict keeps the first-seen order in linear time (code review CR-1)
    return list(dict.fromkeys(m.group(2) or m.group(3) for m in MENTION_RE.finditer(text)))


def split_mentions(text: str) -> list[tuple[str, str | None]]:
    """`text` as (piece, handle) pairs: a mention's raw text with its handle, the
    text between with None."""
    if "@" not in text:
        return [(text, None)] if text else []
    out: list[tuple[str, str | None]] = []
    last = 0
    for m in MENTION_RE.finditer(text):
        if m.start() > last:
            out.append((text[last:m.start()], None))
        out.append((m.group(0), m.group(2) or m.group(3)))
        last = m.end()
    if last < len(text):
        out.append((text[last:], None))
    return out


def mention_line(notes: str, handle: str) -> str:
    """The first note line that mentions `handle`, its list mark dropped: what was
    written about the person there. Empty when no line does."""
    for ln in (notes or "").splitlines():
        if handle in mention_ids(ln):
            return ln.strip().lstrip("-*• ").strip()
    return ""


class Directory:
    """The people of every board, in memory as the file held them when read or
    last written here. `people` is one live dict (handle → Person) the app hands
    to every board it opens, so a person added or renamed shows at once."""

    def __init__(self, path, people: list[Person] | None = None,
                 load_report: dict | None = None) -> None:
        self.path = Path(path)
        self.people: dict[str, Person] = {}
        self.load_report = load_report or {}
        self._stamp: tuple[int, int] | None = None
        self._hold(people or [])

    def _hold(self, people: list[Person]) -> None:
        self.people.clear()
        self.people.update((p.id, p) for p in people)

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
        file to `people.json.corrupt`."""
        path = Path(path)
        try:
            if not path.exists() or not path.read_bytes().strip():
                directory = cls(path)       # nothing written yet, or nothing to keep
                directory._stamped()
                return directory
            people = cls._read(path)
        except OSError:
            people = None
        if people is None:
            backup = keep_aside(path)
            directory = cls(path, [], {"unreadable": True,
                                       "backup": str(backup) if backup else None})
        else:
            directory = cls(path, people)
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
            people = self._read(self.path)  # None when unparseable; may raise OSError
        except OSError:
            people = None
        self._stamp = stamp                 # a bad file is not re-parsed and re-reported on every open
        if people is None:
            return False
        self._hold(people)
        return True

    @staticmethod
    def _read(path: Path) -> list[Person] | None:
        """The people the file holds now, or None when it cannot be parsed (not
        JSON, or not an object with a `people` list); a failed read raises. An
        entry without a valid unique handle or a name is skipped."""
        data = path.read_bytes()
        try:
            raw = clean_strings(json.loads(data.decode("utf-8")))
        except (ValueError, RecursionError):
            return None
        if not isinstance(raw, dict) or not isinstance(raw.get("people"), list):
            return None
        out: list[Person] = []
        seen: set[str] = set()
        for item in raw["people"]:
            if not isinstance(item, dict):
                continue
            pid, name = item.get("id"), _clean(item.get("name"), NAME_MAX)
            if not (isinstance(pid, str) and _HANDLE.fullmatch(pid)) or pid in seen or not name:
                continue
            seen.add(pid)
            out.append(Person(pid, name, _clean(item.get("role"), ROLE_MAX),
                              _clean(item.get("note"), NOTE_MAX)))
        return out

    def get(self, handle: str) -> Person | None:
        return self.people.get(handle)

    def find(self, q: str) -> list[Person]:
        """Every person, by name; with `q`, those whose name has a word starting
        with it first, then those whose name holds it, then those whose role does."""
        q = fold(q.strip())
        people = sorted(self.people.values(), key=lambda p: (fold(p.name), p.id))
        if not q:
            return people
        start = [p for p in people if any(w.startswith(q) for w in fold(p.name).split())]
        inside = [p for p in people if q in fold(p.name) and p not in start]
        role = [p for p in people if q in fold(p.role) and p not in start and p not in inside]
        return start + inside + role

    def named(self, name: str) -> Person | None:
        """The person whose name is `name`, ignoring case and accents."""
        key = fold(_clean(name, NAME_MAX))
        return next((p for p in self.people.values() if fold(p.name) == key), None)

    # ---- writing -----------------------------------------------------------
    def _commit(self, change) -> object:
        """Apply `change` to the people as the file holds them NOW and write the
        result, under the file's lock; then hold that result here. A file that
        cannot be parsed and cannot be copied aside is never written over; a
        failed write raises `OSError` and changes nothing here."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with file_lock(self.path):
            people = None
            if self.path.exists():
                people = self._read(self.path)          # a failed read raises
                if people is None and not self._set_aside():
                    raise OSError(f"{self.path.name} cannot be read and could not be "
                                  "copied aside, so it was not written")
            fresh = {p.id: p for p in (people if people is not None
                                       else list(self.people.values()))}
            result = change(fresh)
            data = {"version": 1, "people": [asdict(p) for p in fresh.values()]}
            write_atomic(self.path, json.dumps(data, indent=2, ensure_ascii=False))
        self._hold(list(fresh.values()))
        self._stamped()
        return result

    def _set_aside(self) -> bool:
        """Whether the unparseable file's bytes are kept: empty (nothing to keep),
        already the copy this directory's load made, or copied now."""
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

    def add(self, name: str, role: str = "", note: str = "") -> Person:
        """A new person: the handle comes from the name (`Ana Ruiz` → `ana.ruiz`,
        `ana.ruiz2` when taken — in the file or here). Raises `ValueError` for a
        name with nothing left once cleaned, `OSError` when it cannot be saved."""
        name = _clean(name, NAME_MAX)
        if not name:
            raise ValueError("a person needs a name")

        def change(fresh: dict[str, Person]) -> Person:
            p = Person(handle_for(name, set(fresh) | set(self.people)), name,
                       _clean(role, ROLE_MAX), _clean(note, NOTE_MAX))
            fresh[p.id] = p
            return p
        return self._commit(change)

    def edit(self, handle: str, name: str, role: str, note: str) -> Person:
        """A person's name, role and note; the handle never changes. A person the
        file no longer holds is written back. Raises like `add`."""
        name = _clean(name, NAME_MAX)
        if not name:
            raise ValueError("a person needs a name")
        if not _HANDLE.fullmatch(handle):               # code review CR-5
            raise ValueError(f"not a handle: {handle!r}")

        def change(fresh: dict[str, Person]) -> Person:
            p = Person(handle, name, _clean(role, ROLE_MAX), _clean(note, NOTE_MAX))
            fresh[handle] = p
            return p
        return self._commit(change)


def handle_for(name: str, taken) -> str:
    """The handle a new person gets: the name's letters and digits, accents
    folded, words joined by `.` (`Andrés Lima` → `andres.lima`; `person` when
    nothing is left), then `2`, `3`, … until it is not in `taken`."""
    base = ".".join(re.findall(r"[a-z0-9]+", fold(name))) or "person"
    h, n = base, 2
    while h in taken:
        h, n = f"{base}{n}", n + 1
    return h
