"""The capture pad's inbox store and the dump / undo of a note into a board (Inc K).

A note is typed in the capture view's pad, split at divider lines, and dumped
into a board as a task (`dump_note`); `alt+u` undoes the last dump (`undo_dump`).
The store (`inbox.json`, beside the registry) holds the pad text, the dumped
entries for 7 days (each undo's record), and the one-time divider-notice flag.
It mirrors `people.Directory`: never raising on load, written atomically under
its lock as a read-modify-write so another taskboard's pad change is never
written over (R0-10), an unreadable file copied aside first (P-S-3), and every
write re-reads the file fresh so a note's text is never dropped silently
(LLR-4407.19, SEC-1). Text shown to the user is never parsed from markup here:
titles are the visible text of the title line (ARCH-8), everything else is kept
verbatim.

G-S owns every write to a board file and to `inbox.json`. It imports only
`taskboard.models`, `taskboard.boards`, `taskboard.history` and `taskboard.views`
— never `app`, never `suggest`, never a Textual module (ARCH-8).
"""

from __future__ import annotations

import collections
import json
import os
import re
import shutil
import stat
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

from . import history, models, views
from .boards import file_lock, keep_aside, peek_board
from .models import (IMAGE_EXTS, PROJECT_COLORS, Board, Project, Task,
                     clean_strings, save_pil_image, strip_controls, write_atomic)

INBOX_NAME = "inbox.json"
IMAGES_NAME = "inbox-images"
KEEP_DAYS = 7
KEEP_SECONDS = 604_800
STORE_MAX_BYTES = 8_388_608
IMAGE_NAME_MAX = 128

#: Windows device names, with the superscript spellings too (SEC-7, defence in
#: depth: Windows 10 still maps `con`, `com1`, `lpt¹`, … to devices).
RESERVED_STEMS = frozenset(
    ["con", "prn", "aux", "nul", "conin$", "conout$"]
    + [f"com{i}" for i in range(10)]
    + [f"lpt{i}" for i in range(10)]
    + [f"com{d}" for d in ("¹", "²", "³")]
    + [f"lpt{d}" for d in ("¹", "²", "³")]
)

DIVIDER_RE = re.compile("_{4,}")
STAMP_RE = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d")
ID_RE = re.compile(r"[A-Za-z0-9_-]{1,64}")

#: the dumped entry's keys in their written order (LLR-4407.3).
DUMPED = (
    ("at", str),
    ("text", str),
    ("task", str),
    ("title", str),
    ("board", str),
    ("project", str),
    ("new_project", bool),
    ("images", list),
)


class Part(NamedTuple):
    start: int
    end: int
    text: str
    is_note: bool


class NoteTask(NamedTuple):
    title: str
    notes: str
    images: list[str]


class DumpTarget(NamedTuple):
    path: Path
    name: str
    live: object


class DumpOutcome(NamedTuple):
    ok: bool
    task: object
    project_id: str
    project_name: str
    new_project: bool
    images: list[str]
    missing: list[str]
    notice: object


class UndoOutcome(NamedTuple):
    state: str
    note_text: str
    notice: object


class WriteResult(NamedTuple):
    written: bool
    pad: str
    union: bool


class AttachResult(NamedTuple):
    names: list[str]
    notice: object


# ---- note parsing ----------------------------------------------------------

def _image_ok(name: str) -> bool:
    """The image-name rule (§1, LLR-4408.18, P-S-10, SEC-7): a bare file name
    1..128 characters, no surrounding whitespace, no `/`, backslash or `:`, no control
    byte, not `.` / `..`, a lower-case suffix in `IMAGE_EXTS`, and no Windows
    device stem. Pure and linear in len(name)."""
    if not isinstance(name, str):
        return False
    if not 1 <= len(name) <= IMAGE_NAME_MAX:
        return False
    if name != name.strip():
        return False
    for ch in name:
        o = ord(ch)
        if ch in "/\\:" or o < 0x20 or o == 0x7F or 0x80 <= o <= 0x9F:
            return False
    if name in (".", ".."):
        return False
    if os.path.splitext(name)[1].lower() not in IMAGE_EXTS:
        return False
    if name.split(".")[0].rstrip(" ").lower() in RESERVED_STEMS:
        return False
    return True


def image_name(line: str) -> str | None:
    """The bare name of an image line (`img: <name>`, the name passing the
    image-name rule), else None. `img:a.png` and `IMG: a.png` are not image
    lines (LLR-4408.18)."""
    s = line.strip()
    if not s.startswith("img: "):
        return None
    name = s[5:]
    return name if _image_ok(name) else None


def is_divider(line: str) -> bool:
    """A divider line: with trailing whitespace removed, 4 or more `_` and
    nothing else; leading whitespace is not allowed (LLR-4402.1, R0-3)."""
    return bool(DIVIDER_RE.fullmatch(line.rstrip()))


def _part(lines: list[str], start: int, end: int) -> Part:
    """One part over `lines[start:end+1]`, outer blank lines dropped."""
    if end < start:
        return Part(start, end, "", False)
    first = next((j for j in range(start, end + 1) if lines[j].strip()), None)
    if first is None:
        return Part(start, end, "", False)
    last = next(j for j in range(end, start - 1, -1) if lines[j].strip())
    return Part(start, end, "\n".join(lines[first:last + 1]), True)


def note_parts(text: str) -> list[Part]:
    """`text` split at divider lines into parts in order; a divider belongs to
    no part. Each part keeps its first/last line index and its text with outer
    blank lines removed; `is_note` is True when that text holds a non-whitespace
    character (LLR-4402.2..4402.5). Linear in len(text), never raises."""
    lines = text.split("\n")
    parts: list[Part] = []
    start = 0
    i = 0
    while i <= len(lines):
        if i == len(lines) or is_divider(lines[i]):
            parts.append(_part(lines, start, i - 1))
            start = i + 1
        i += 1
    return parts


def note_count(text: str) -> int:
    """The notes of `note_parts`, plus 1 when the last part holds at least one
    line, holds only whitespace and follows a divider line (the note being
    started, R2 F-4, LLR-4402.8)."""
    parts = note_parts(text)
    count = sum(1 for p in parts if p.is_note)
    if parts:
        last = parts[-1]
        if len(parts) > 1 and last.end >= last.start and not last.is_note:
            count += 1
    return count


def note_at(text: str, row: int) -> Part | None:
    """The note part holding `row`; on a divider line the note part directly
    above it, else None (LLR-4404.30, LLR-4404.28). A row outside the pad is
    None; the search never climbs past an empty or whitespace part."""
    lines = text.split("\n")
    if not 0 <= row < len(lines):
        return None
    target = row - 1 if is_divider(lines[row]) else row
    for part in note_parts(text):
        if part.start <= target <= part.end:
            return part if part.is_note else None
    return None


def _visible(line: str) -> str:
    """The visible text of a line: the highlight syntax's markers dropped, from
    `views.highlight_segments` (rich only, no Textual — ARCH-8, LLR-4201.10)."""
    return "".join(seg for seg, _ in views.highlight_segments(line))


def _title_row(lines: list[str]) -> int | None:
    """The first line that is not an image line and whose visible text is not
    blank, else None (LLR-4404.2, LLR-4404.29)."""
    for i, line in enumerate(lines):
        if image_name(line) is None and strip_controls(_visible(line)).strip():
            return i
    return None


def _image_names(text: str) -> list[str]:
    """The image names in line order, each once (first spelling kept; duplicates
    by `os.path.normcase`, LLR-4409.3)."""
    names: list[str] = []
    seen: set[str] = set()
    for line in text.split("\n"):
        name = image_name(line)
        if name is not None:
            key = os.path.normcase(name)
            if key not in seen:
                seen.add(key)
                names.append(name)
    return names


def _task_fields(text: str, moved: set[str]) -> tuple[str, str]:
    """The title and notes a dump writes, given the image names whose files it
    moved (`moved`, compared by `os.path.normcase`). Title = visible text of the
    title line, stripped; notes = every other line except the moved image lines,
    verbatim, outer blank lines removed, controls removed. One function for the
    dump and the undo's changed-check, so a note with a missing image is not seen
    as edited (P-S-2, LLR-4408.12)."""
    lines = text.split("\n")
    r = _title_row(lines)
    title = strip_controls(_visible(lines[r])).strip() if r is not None else ""
    moved_nc = {os.path.normcase(m) for m in moved}
    kept: list[str] = []
    for i, line in enumerate(lines):
        if i == r:
            continue
        name = image_name(line)
        if name is not None and os.path.normcase(name) in moved_nc:
            continue
        kept.append(line)
    first = next((j for j, ln in enumerate(kept) if ln.strip()), None)
    if first is None:
        notes = ""
    else:
        last = next(j for j in range(len(kept) - 1, -1, -1) if kept[j].strip())
        notes = "\n".join(kept[first:last + 1])
    return title, strip_controls(notes)


def note_task(text: str) -> NoteTask:
    """The note read as a task: its title, its notes (image lines left out, as
    written when every image is found) and its image names once each
    (LLR-4404.2, LLR-4404.3, LLR-4404.29, LLR-4409.3)."""
    images = _image_names(text)
    title, notes = _task_fields(text, set(images))
    return NoteTask(title, notes, images)


def without_note(text: str, part: Part) -> tuple[str, int]:
    """The pad without the part's lines and one adjacent divider (the one after,
    else the one before); every other line byte-identical. `row` is where the
    part began, clamped into the new text (LLR-4404.6)."""
    lines = text.split("\n")
    remove = set(range(part.start, part.end + 1))
    if part.end + 1 < len(lines) and is_divider(lines[part.end + 1]):
        remove.add(part.end + 1)
    elif part.start - 1 >= 0 and is_divider(lines[part.start - 1]):
        remove.add(part.start - 1)
    kept = [ln for i, ln in enumerate(lines) if i not in remove]
    row = min(part.start, len(kept) - 1) if kept else 0
    return "\n".join(kept), row


def with_note(text: str, note: str) -> str:
    """`note` appended at the end, after a new divider line when `text` holds
    text; trailing blank lines (and a trailing divider's empty part) are dropped
    first (LLR-4405.3, P-S-14)."""
    lines = text.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return note
    if is_divider(lines[-1]):
        return "\n".join(lines + [note])
    return "\n".join(lines + ["____", note])


def union_pads(fresh_pad: str, unseen: list[str], mine: str) -> str:
    """The note-level union (LLR-4407.19, SEC-1): the fresh pad's notes in their
    order, then each note of `mine` in order, less one copy per fresh-pad note
    and per `unseen` text of equal text (a multiset). Joined by `\\n____\\n`."""
    budget = collections.Counter(p.text for p in note_parts(fresh_pad) if p.is_note)
    budget.update(unseen)
    out: list[str] = [p.text for p in note_parts(fresh_pad) if p.is_note]
    for p in note_parts(mine):
        if not p.is_note:
            continue
        if budget[p.text] > 0:
            budget[p.text] -= 1
        else:
            out.append(p.text)
    return "\n____\n".join(out)


def prune_dumped(entries: list[dict], now: datetime) -> list[dict]:
    """The entries whose `at` is a valid local stamp no more than 604 800 s
    before `now`, in their order (LLR-4405.12). An `at` later than `now` is kept
    (harmless: it is only ever the last undo candidate by position)."""
    kept: list[dict] = []
    for e in entries:
        at = e.get("at")
        if not isinstance(at, str) or not STAMP_RE.fullmatch(at):
            continue
        try:
            when = datetime.fromisoformat(at)
        except ValueError:
            continue
        if (now - when).total_seconds() <= KEEP_SECONDS:
            kept.append(e)
    return kept


def entry_for(outcome: DumpOutcome, note: str, board_path: Path, now: datetime) -> dict:
    """The dumped entry G-V passes to `Inbox.write_pad(record=…)`, in the
    LLR-4407.3 key order (P-S-15)."""
    return {
        "at": models.stamp(now),
        "text": note,
        "task": outcome.task.id,
        "title": outcome.task.title,
        "board": str(board_path),
        "project": outcome.project_id,
        "new_project": outcome.new_project,
        "images": list(outcome.images),
    }


# ---- the store -------------------------------------------------------------

def _remove_first_note(pad: str, text: str) -> str:
    """`pad` without its first note whose text equals `text` (the dump's removal
    of the note from the fresh pad, ARCH-1 / LLR-4407.48)."""
    for part in note_parts(pad):
        if part.is_note and part.text == text:
            return without_note(pad, part)[0]
    return pad


def _same_entry(a: dict, b: dict) -> bool:
    return (a["task"], a["board"]) == (b["task"], b["board"])


def _has_entry(entries: list[dict], e: dict) -> bool:
    return any(_same_entry(x, e) for x in entries)


class Inbox:
    """The pad store, in memory as the file held it when read or last written
    here. `pending` holds dump/undo records whose store write failed and is never
    written to the store (ARCH-4); it survives every refresh and is retried by
    the next successful pad write. G-V reads the pad through `pad_now()` and
    changes it only through `write_pad` and `mark_notice`."""

    def __init__(self, path) -> None:
        self.path = Path(path)
        self.images_dir = self.path.parent / IMAGES_NAME
        self.pad = ""
        self.dumped: list[dict] = []
        self.pending: list[tuple[str, dict]] = []
        self.divider_notice = False
        self.load_report: dict = {}
        self._stamp: tuple[int, int] | None = None

    def _hold(self, state: dict) -> None:
        self.pad = state["pad"]
        self.dumped = list(state["dumped"])
        self.divider_notice = state["divider_notice"]

    def _stamped(self) -> None:
        """The file's (st_mtime_ns, st_size) as of the last read or write here;
        None when the file is missing (SEC-4: taken after every load, refresh and
        successful write, never after a read that raised OSError)."""
        try:
            st = self.path.stat()
            self._stamp = (st.st_mtime_ns, st.st_size)
        except OSError:
            self._stamp = None

    # -- reading -------------------------------------------------------------
    @staticmethod
    def _entry(item: object) -> dict | None:
        """One dumped entry re-built in DUMPED key order, or None. None unless it
        is a dict with every field of its exact type (`new_project` is True only
        as the boolean), a `task` fullmatching `[A-Za-z0-9_-]{1,64}` (it names the
        path `images/<task>/`), a non-blank `text`, a non-empty `board`, and every
        `images` item passing the image-name rule — so a hostile store can name no
        path outside `images/<id>/` or the pad images folder (P-S-4)."""
        if not isinstance(item, dict):
            return None
        out: dict = {}
        for key, typ in DUMPED:
            if key not in item:
                return None
            value = item[key]
            if key == "new_project":
                if type(value) is not bool:
                    return None
            elif type(value) is not typ:
                return None
            out[key] = value
        if not ID_RE.fullmatch(out["task"]):
            return None
        if not out["board"].strip():
            return None
        if not out["text"].strip():
            return None
        if not all(isinstance(n, str) and _image_ok(n) for n in out["images"]):
            return None
        return {k: out[k] for k, _ in DUMPED}

    @staticmethod
    def _read(path: Path) -> dict | None:
        """The store as the file holds it now, or None when it cannot be parsed
        or is over `STORE_MAX_BYTES` (read at most the cap + 1 byte). A failed
        read raises OSError (the caller decides). The encode probe at the door
        catches a lone surrogate a later write could never save (SEC-2)."""
        with open(path, "rb") as fh:
            data = fh.read(STORE_MAX_BYTES + 1)
        if len(data) > STORE_MAX_BYTES:
            return None
        try:
            raw = clean_strings(json.loads(data.decode("utf-8")))
            json.dumps(raw, ensure_ascii=False).encode("utf-8")
        except (ValueError, RecursionError):
            return None
        if not isinstance(raw, dict):
            return None
        if "pad" in raw and not isinstance(raw["pad"], str):
            return None
        if "dumped" in raw and not isinstance(raw["dumped"], list):
            return None
        dumped = [e for e in (Inbox._entry(item) for item in raw.get("dumped", []))
                  if e is not None]
        return {"pad": raw.get("pad", ""), "dumped": dumped,
                "divider_notice": raw.get("divider_notice") is True}

    @staticmethod
    def _too_big(path: Path) -> bool:
        try:
            return os.stat(path).st_size > STORE_MAX_BYTES
        except OSError:
            return False

    @classmethod
    def load(cls, path) -> "Inbox":
        """Never raises. Missing or blank → empty (nothing written). Unparseable
        or over the cap → empty, the file copied aside first (never when over the
        cap, P-S-3); a read that raises OSError keeps the stamp None (SEC-4) and
        copies nothing (A-4). The stamp is taken otherwise (LLR-4407.45)."""
        path = Path(path)
        inbox = cls(path)
        read_failed = False
        try:
            if not path.exists():
                inbox._stamped()
                return inbox
            with open(path, "rb") as fh:
                head = fh.read(STORE_MAX_BYTES + 1)
            if not head.strip():
                inbox._stamped()
                return inbox
            state = cls._read(path)
        except OSError:
            state = None
            read_failed = True
        if state is None:
            backup = None
            if not read_failed and not cls._too_big(path):
                backup = keep_aside(path)
            inbox.load_report = {"unreadable": True, "backup": str(backup) if backup else None}
        else:
            inbox._hold(state)
        if not read_failed:
            inbox._stamped()
        return inbox

    def refresh(self) -> bool | None:
        """Re-read on change only: None unchanged · True reloaded · False the
        file could not be parsed (the new stamp is taken, reported once). A read
        that raises OSError keeps state AND the old stamp (SEC-4). `pending` is
        not store state and is never touched (ARCH-4)."""
        try:
            st = self.path.stat()
            stamp = (st.st_mtime_ns, st.st_size)
        except OSError:
            return None
        if stamp == self._stamp:
            return None
        try:
            state = self._read(self.path)
        except OSError:
            return False
        self._stamp = stamp
        if state is None:
            return False
        self._hold(state)
        return True

    def _set_aside(self) -> bool:
        """Whether an unparseable file's bytes are kept: empty, already this
        Inbox's copy, or copied now; never for a file over the cap (P-S-3)."""
        if self._too_big(self.path):
            return False
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

    @staticmethod
    def _shape(state: dict) -> str:
        """The store text: `version`, `pad`, `dumped` (each entry in DUMPED key
        order), then `divider_notice` only when true (no `flagged` key, ARCH-4)."""
        data = {
            "version": 1,
            "pad": state["pad"],
            "dumped": [{k: e[k] for k, _ in DUMPED} for e in state["dumped"]],
        }
        if state["divider_notice"]:
            data["divider_notice"] = True
        return json.dumps(data, indent=2, ensure_ascii=False)

    def _commit(self, change):
        """The read-modify-write shared by `write_pad` and `mark_notice`
        (`people.Directory._commit`'s shape): re-read under the lock, apply
        `change` to the FRESH state (ARCH-1), prune, shape, cap-check, encode
        probe (SEC-2) and `write_atomic`. Any OSError leaves memory unchanged
        (it propagates before the hold); returns (new state, changed)."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with file_lock(self.path, INBOX_NAME):
            before = _file_stamp(self.path)
            fresh = None
            if self.path.exists():
                fresh = self._read(self.path)
                if fresh is None and not self._set_aside():
                    if self._too_big(self.path):
                        raise OSError(
                            "inbox.json is larger than 8388608 bytes, so it was not written")
                    raise OSError("inbox.json cannot be read and could not be "
                                  "copied aside, so it was not written")
            base = dict(fresh) if fresh is not None else {
                "pad": self.pad, "dumped": list(self.dumped),
                "divider_notice": self.divider_notice}
            changed = fresh is not None and before != self._stamp
            new = change(base, changed)
            new["dumped"] = prune_dumped(new["dumped"], datetime.now())
            text = self._shape(new)
            try:
                data = text.encode("utf-8")
            except UnicodeError as exc:
                raise OSError(f"inbox.json holds a character that cannot be saved "
                              f"({exc.reason}), so it was not written")
            if len(data) > STORE_MAX_BYTES:
                raise OSError(f"inbox.json would hold {len(data)} bytes, over the "
                              "8388608-byte limit, so it was not written")
            write_atomic(self.path, text)
        return new, changed

    def write_pad(self, pad: str, record: dict | None = None,
                  drop: dict | None = None) -> WriteResult:
        """The one pad write. `pad` is written verbatim when the file is unchanged
        since this Inbox's last read/write, else it unions with the fresh pad
        (SEC-1). A `record`/`drop` is applied to the FRESH state first (ARCH-1,
        LLR-4407.48 / .49); any failure keeps them as pending records (ARCH-4).
        Raises OSError (lock, cap, encode, write)."""
        pad = strip_controls(pad)
        if pad == self.pad and record is None and drop is None and not self.pending:
            return WriteResult(False, self.pad, False)
        ops = list(self.pending)
        if record is not None:
            ops.append(("record", record))
        if drop is not None:
            ops.append(("drop", drop))

        def change(base, changed):
            p = base["pad"]
            d = list(base["dumped"])
            for kind, e in ops:
                if kind == "record":
                    if _has_entry(d, e):
                        continue
                    p = _remove_first_note(p, e["text"])
                    d.append(dict(e))
                else:
                    held = _has_entry(d, e)
                    d = [x for x in d if not _same_entry(x, e)]
                    if held:
                        p = with_note(p, e["text"])
            self_keys = {(m["task"], m["board"]) for m in self.dumped}
            unseen = [x["text"] for x in base["dumped"]
                      if (x["task"], x["board"]) not in self_keys]
            written = pad if not changed else union_pads(p, unseen, pad)
            base["pad"] = written
            base["dumped"] = d
            base["divider_notice"] = base["divider_notice"] or self.divider_notice
            return base

        try:
            new, changed = self._commit(change)
        except OSError:
            if record is not None:
                self.pending.append(("record", record))
            if drop is not None:
                self.pending.append(("drop", drop))
            raise
        written = new["pad"]
        self._hold(new)
        self.pending = []
        self._stamped()
        return WriteResult(True, written, changed and written != pad)

    def pad_now(self) -> str:
        """The pad as held, with the pending ops applied as `write_pad` applies
        them (a dump whose store write failed does not come back into the pad,
        ARCH-4 / LLR-4407.42). Pure: reads no file, changes nothing."""
        p, d = self.pad, list(self.dumped)
        for kind, e in self.pending:
            if kind == "record":
                if not _has_entry(d, e):
                    p = _remove_first_note(p, e["text"])
                    d.append(dict(e))
            else:
                held = _has_entry(d, e)
                d = [x for x in d if not _same_entry(x, e)]
                if held:
                    p = with_note(p, e["text"])
        return p

    def last_dump(self, now: datetime) -> dict | None:
        """The newest (last by position) kept entry: the store FILE's `dumped`
        read fresh at the call (no state/stamp change), or the in-memory `dumped`
        when the file is missing or unparseable (P-S-6); then each pending record
        not already present is appended and each pending drop removes its entry
        (ARCH-4, LLR-4405.18)."""
        try:
            state = self._read(self.path)
        except OSError:
            state = None
        entries = state["dumped"] if state is not None else self.dumped
        result = prune_dumped(entries, now)
        for kind, e in self.pending:
            if kind == "record":
                if not _has_entry(result, e):
                    result.append(dict(e))
            else:
                result = [x for x in result if not _same_entry(x, e)]
        return result[-1] if result else None

    def mark_notice(self) -> None:
        """Set `divider_notice` true (the pad as the file holds it). Not a pad
        write: no pending op is applied (they wait for the next `write_pad`,
        ARCH-4). Pad and stamp are held only when the file was unchanged before it
        (P-S-5)."""
        if self.divider_notice:
            return

        def change(base, changed):
            base["divider_notice"] = True
            return base

        new, changed = self._commit(change)
        self.divider_notice = new["divider_notice"]
        self.dumped = list(new["dumped"])
        if not changed:
            self.pad = new["pad"]
            self._stamped()


# ---- image helpers ---------------------------------------------------------

def _free_name(folder: Path, name: str) -> str:
    """`name` when free, else the first `<stem>-<k><suffix>` (k = 2, 3, …) that
    is. A dangling symlink counts as taken (never written through). Bounded."""
    if not os.path.lexists(folder / name):
        return name
    stem, suffix = os.path.splitext(name)
    for k in range(2, 10000):
        candidate = f"{stem}-{k}{suffix}"
        if not os.path.lexists(folder / candidate):
            return candidate
    raise OSError(f"no free name for {name}")


def _file_stamp(path: Path) -> tuple | None:
    """`(st_mtime_ns, st_size)` of the file, None on OSError — G-S's own copy of
    boards' private `_stamp` (no private import across modules)."""
    try:
        st = os.stat(path)
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return None


def _links_ok(folder: Path, board: Board, task_id: str) -> bool:
    """Whether the pad images folder and the task's image folder are plain folders
    under the board's `images/` (SEC-6, LLR-4408.20): a link or junction is never
    unlinked through. False on any OSError."""
    try:
        img = board.image_dir(task_id)
        if os.path.islink(folder) or folder.is_junction():
            return False
        if os.path.islink(img) or img.is_junction():
            return False
        return img.resolve().parent == (board.path.parent / "images").resolve()
    except OSError:
        return False


def _new_colour(board: Board) -> str:
    """The first `PROJECT_COLORS` hue no project of the board uses, else
    `PROJECT_COLORS[len(projects) % 8]` (LLR-4404.24)."""
    used = {p.color for p in board.projects}
    for colour in PROJECT_COLORS:
        if colour not in used:
            return colour
    return PROJECT_COLORS[len(board.projects) % 8]


def _name_refusal(board: Board, name: str, board_name: str) -> str | None:
    """The duplicate-project notice, or None (LLR-4404.26)."""
    for p in board.projects:
        if p.name.strip().casefold() == name.casefold():
            return f"{board_name} already has a project named {name}."
    return None


def _copy_images(folder: Path, names: list[str],
                 dest_dir: Path) -> tuple[list[str], list[str], list[str]]:
    """Copy each pad image (a regular file only: never a symlink or folder) into
    `dest_dir` (created exclusively); returns the moved names, the missing names
    and the resolved paths in line order. On OSError the folder this call created
    is removed and the error re-raised (LLR-4408.10..4408.13)."""
    moved: list[str] = []
    missing: list[str] = []
    paths: list[str] = []
    created = False
    try:
        for name in names:
            src = folder / name
            try:
                st = os.lstat(src)
            except OSError:
                st = None
            if st is None or not stat.S_ISREG(st.st_mode):
                missing.append(name)
                continue
            if not moved:
                dest_dir.parent.mkdir(parents=True, exist_ok=True)
                dest_dir.mkdir()          # exclusive: a taken folder is refused (ARCH-7)
                created = True
            shutil.copy2(src, dest_dir / name)
            moved.append(name)
            paths.append(str((dest_dir / name).resolve()))
    except OSError:
        if created:
            shutil.rmtree(dest_dir, ignore_errors=True)
        raise
    return moved, missing, paths


def _drop_pad_copies(folder: Path, names: list[str], unlink_ok: bool) -> None:
    """Remove the pad copies after a successful board save, only when `unlink_ok`
    (SEC-6); a copy that cannot be removed (a viewer holds it) is left as a plain
    file — nothing is lost (P-S-12)."""
    if not unlink_ok:
        return
    for name in names:
        try:
            (folder / name).unlink()
        except OSError:
            pass


# ---- dump ------------------------------------------------------------------

def _refuse(project_id: str | None, project_name: str, new_project: bool,
            notice: str) -> DumpOutcome:
    return DumpOutcome(False, None, project_id or "", project_name, new_project,
                       [], [], notice)


def dump_note(target: DumpTarget, project_id: str | None, new_name: str | None,
              note: str, folder: Path, project_name: str = "") -> DumpOutcome:
    """Dump `note` into a project of `target` as a new task. Exactly one of
    `project_id` / `new_name`; `project_name` words the LLR-4404.12 refusal only.
    The note is encode-probed before any board write (SEC-2, LLR-4404.34)."""
    if (project_id is None) == (new_name is None):
        raise ValueError("exactly one of project_id and new_name")
    new_project = new_name is not None
    try:
        note.encode("utf-8")
        if new_name is not None:
            new_name.encode("utf-8")
    except UnicodeEncodeError:
        return _refuse(project_id, project_name, new_project,
                       "This note holds a character that cannot be saved — nothing dumped.")
    nt = note_task(note)
    if not nt.title:
        return _refuse(project_id, project_name, new_project,
                       "This note has no text line for a title.")
    clean = None
    if new_name is not None:
        clean = strip_controls(new_name).strip()
        if not clean:
            return _refuse(project_id, project_name, new_project, "A project needs a name.")
    if not target.path.exists():
        return _refuse(project_id, project_name, new_project,
                       f"{target.name}'s file is missing — nothing dumped.")
    if target.live is not None:
        return _dump_open(target, nt, note, project_id, clean, project_name, folder)
    return _dump_other(target, nt, note, project_id, clean, project_name, folder)


def _dump_open(target: DumpTarget, nt: NoteTask, note: str, project_id: str | None,
               clean_name: str | None, project_name: str, folder: Path) -> DumpOutcome:
    """The dump into the open board, through `live.add_task` + the app's save path
    (R0-8, S-a: no lock, no stamp). Both checks on both paths (P-S-9)."""
    live = target.live
    name = target.name
    new_project = clean_name is not None
    if live.load_report.get("file_unreadable"):
        return _refuse(project_id, project_name, new_project,
                       f"{name}'s file cannot be read — nothing dumped.")
    if project_id is not None and live.project_by_id(project_id) is None:
        return _refuse(project_id, project_name, new_project,
                       f"{project_name} is no longer on {name} — nothing dumped.")
    if clean_name is not None:
        refusal = _name_refusal(live, clean_name, name)
        if refusal:
            return _refuse(project_id, project_name, new_project, refusal)
    tid = models._new_id()
    try:
        moved, missing, paths = _copy_images(folder, nt.images, live.image_dir(tid))
    except OSError as exc:
        return _refuse(project_id, project_name, new_project,
                       f"An image could not be moved: {exc} — nothing dumped.")
    title, notes = _task_fields(note, set(moved))
    project_obj = None
    if clean_name is not None:
        project_obj = Project(clean_name, color=_new_colour(live))
        live.projects.append(project_obj)          # NOT add_project: one save (LLR-4404.23)
        pid = project_obj.id
    else:
        pid = project_id
    task = Task(title, project_id=pid, phase=live.phases[0], notes=notes,
                images=paths, id=tid)
    try:
        live.add_task(task)
    except OSError as exc:
        if task in live.tasks:
            live.tasks.remove(task)
        if project_obj is not None and project_obj in live.projects:
            live.projects.remove(project_obj)
        shutil.rmtree(live.image_dir(tid), ignore_errors=True)
        return _refuse(project_id, project_name, new_project,
                       f"{name} could not be saved: {exc} — nothing dumped.")
    _drop_pad_copies(folder, moved, _links_ok(folder, live, tid))
    return DumpOutcome(True, task, pid, clean_name or project_name, new_project,
                       moved, missing, None)


def _dump_other(target: DumpTarget, nt: NoteTask, note: str, project_id: str | None,
                clean_name: str | None, project_name: str, folder: Path) -> DumpOutcome:
    """The dump into another board, `move_project`'s pattern (R1-3): fresh read
    under the lock, stamp checks, `save_atomic`, birth record after the save."""
    name = target.name
    path = target.path
    new_project = clean_name is not None
    try:
        with file_lock(path, name):
            if not path.exists():
                return _refuse(project_id, project_name, new_project,
                               f"{name}'s file is missing — nothing dumped.")
            s0 = _file_stamp(path)
            try:
                fresh = peek_board(path)
            except OSError:
                return _refuse(project_id, project_name, new_project,
                               f"{name}'s file cannot be read — nothing dumped.")
            s1 = _file_stamp(path)
            if fresh.load_report.get("file_unreadable"):
                return _refuse(project_id, project_name, new_project,
                               f"{name}'s file cannot be read — nothing dumped.")
            if s1 != s0:
                return _refuse(project_id, project_name, new_project,
                               f"{name} changed while dumping — nothing dumped.")
            if project_id is not None and fresh.project_by_id(project_id) is None:
                return _refuse(project_id, project_name, new_project,
                               f"{project_name} is no longer on {name} — nothing dumped.")
            if clean_name is not None:
                refusal = _name_refusal(fresh, clean_name, name)
                if refusal:
                    return _refuse(project_id, project_name, new_project, refusal)
            now = datetime.now()
            tid = models._new_id()
            try:
                moved, missing, paths = _copy_images(folder, nt.images, fresh.image_dir(tid))
            except OSError as exc:
                return _refuse(project_id, project_name, new_project,
                               f"An image could not be moved: {exc} — nothing dumped.")
            title, notes = _task_fields(note, set(moved))
            if clean_name is not None:
                fresh.projects.append(Project(clean_name, color=_new_colour(fresh)))
                pid = fresh.projects[-1].id
            else:
                pid = project_id
            task = Task(title, project_id=pid, phase=fresh.phases[0], notes=notes,
                        images=paths, created=models.stamp(now), id=tid)
            fresh.tasks.append(task)
            if _file_stamp(path) != s0:
                shutil.rmtree(fresh.image_dir(tid), ignore_errors=True)
                return _refuse(project_id, project_name, new_project,
                               f"{name} changed while dumping — nothing dumped.")
            try:
                fresh.save_atomic()
            except OSError as exc:
                shutil.rmtree(fresh.image_dir(tid), ignore_errors=True)
                return _refuse(project_id, project_name, new_project,
                               f"{name} could not be saved: {exc} — nothing dumped.")
            history.append(path, {"task": tid, "from": None, "to": task.phase}, at=now)
    except OSError as exc:
        return _refuse(project_id, project_name, new_project, str(exc))
    _drop_pad_copies(folder, moved, _links_ok(folder, fresh, tid))
    return DumpOutcome(True, task, pid, clean_name or project_name, new_project,
                       moved, missing, None)


# ---- undo ------------------------------------------------------------------

def _unchanged(board: Board, task: Task, entry: dict, title: str, notes: str) -> bool:
    """Whether `task` is the whole record its dump wrote (SEC-3): every field at
    its default except title, project, phase, notes, images, id and created."""
    expected = Task(
        title=title,
        project_id=entry["project"],
        phase=board.phases[0],
        notes=notes,
        images=[str((board.image_dir(entry["task"]) / n).resolve()) for n in entry["images"]],
        id=entry["task"],
        created=task.created,
    )
    return asdict(task) == asdict(expected)


def _needed(board: Board, task_id: str) -> bool:
    """Whether another task depends on `task_id` (LLR-4405.19, state "needed")."""
    return any(task_id in t.depends_on for t in board.tasks if t.id != task_id)


def undo_dump(entry: dict, live: Board | None, folder: Path) -> UndoOutcome:
    """Undo the dump `entry` records. The entry is re-shaped (`Inbox._entry`) so
    its task id and image names pass the strict rules (P-S-4). `live` is the open
    board when the entry's board is its file, else None."""
    entry = Inbox._entry(entry)
    if entry is None:
        return UndoOutcome("failed", "", "not a valid dump record")
    title, notes = _task_fields(entry["text"], set(entry["images"]))
    if live is not None:
        outcome, board = _undo_open(entry, live, title, notes)
    else:
        outcome, board = _undo_other(entry, title, notes)
    if outcome.state == "undone":
        renames = _images_back(board.image_dir(entry["task"]), folder, entry["images"],
                               _links_ok(folder, board, entry["task"]))
        try:
            os.rmdir(board.image_dir(entry["task"]))
        except OSError:
            pass                        # a folder holding other files stays (LLR-4408.17)
        return UndoOutcome("undone", _renamed(entry["text"], renames), None)
    return outcome


def _undo_open(entry: dict, live: Board, title: str, notes: str) -> tuple[UndoOutcome, Board]:
    """The undo on the open board (the app's save path, LLR-4405.2)."""
    task = live.task_by_id(entry["task"])
    if task is None:
        return UndoOutcome("gone", entry["text"], None), live
    if not _unchanged(live, task, entry, title, notes):
        return UndoOutcome("changed", entry["text"], None), live
    if _needed(live, entry["task"]):
        return UndoOutcome("needed", entry["text"], None), live
    i = live.tasks.index(task)
    live.tasks.pop(i)
    project_obj = None
    proj_index = None
    if entry["new_project"] and not any(t.project_id == entry["project"] for t in live.tasks):
        for j, p in enumerate(live.projects):
            if p.id == entry["project"]:
                project_obj = p
                proj_index = j
                break
        if proj_index is not None:
            live.projects.pop(proj_index)
    try:
        live.save()
    except OSError as exc:
        live.tasks.insert(i, task)
        if proj_index is not None:
            live.projects.insert(proj_index, project_obj)
        return UndoOutcome("failed", "", str(exc)), live
    return UndoOutcome("undone", entry["text"], None), live


def _undo_other(entry: dict, title: str, notes: str) -> tuple[UndoOutcome, Board | None]:
    """The undo on another board, under its lock with the stamp check and
    `save_atomic`; no history line is written."""
    path = Path(entry["board"])
    if not path.exists():
        return UndoOutcome("failed", "", "its file is missing"), None
    try:
        with file_lock(path, path.parent.name):
            s0 = _file_stamp(path)
            try:
                fresh = peek_board(path)
            except OSError:
                return UndoOutcome("failed", "", "its file cannot be read"), None
            s1 = _file_stamp(path)
            if fresh.load_report.get("file_unreadable"):
                return UndoOutcome("failed", "", "its file cannot be read"), None
            if s1 != s0:
                return UndoOutcome("failed", "", "it changed while it was read"), None
            task = fresh.task_by_id(entry["task"])
            if task is None:
                return UndoOutcome("gone", entry["text"], None), None
            if not _unchanged(fresh, task, entry, title, notes):
                return UndoOutcome("changed", entry["text"], None), None
            if _needed(fresh, entry["task"]):
                return UndoOutcome("needed", entry["text"], None), None
            fresh.tasks.remove(task)
            if entry["new_project"] and not any(t.project_id == entry["project"]
                                                for t in fresh.tasks):
                fresh.projects = [p for p in fresh.projects if p.id != entry["project"]]
            if _file_stamp(path) != s0:
                return UndoOutcome("failed", "", "it changed while undoing"), None
            try:
                fresh.save_atomic()
            except OSError as exc:
                return UndoOutcome("failed", "", str(exc)), None
    except OSError as exc:
        return UndoOutcome("failed", "", str(exc)), None
    return UndoOutcome("undone", entry["text"], None), fresh


def _images_back(src_dir: Path, folder: Path, names: list[str],
                 unlink_ok: bool) -> dict[str, str]:
    """Copy the board's image copies back into the pad images folder (renaming
    when taken), unlinking the board copies only when `unlink_ok` (SEC-6).
    Returns {old name: new name} for every file moved. An OSError stops the loop
    (the file stays in the board; P-S-12)."""
    folder.mkdir(parents=True, exist_ok=True)
    renames: dict[str, str] = {}
    for name in names:
        src = src_dir / name
        try:
            st = os.lstat(src)
        except OSError:
            st = None
        if st is None or not stat.S_ISREG(st.st_mode):
            continue                    # its line keeps its name
        free = _free_name(folder, name)
        try:
            shutil.copy2(src, folder / free)
            renames[name] = free
            if unlink_ok:
                src.unlink()
        except OSError:
            break
    return renames


def _renamed(text: str, renames: dict[str, str]) -> str:
    """Each image line whose name was renamed becomes `img: <new>`; every other
    line byte-identical (LLR-4408.16)."""
    out = []
    for line in text.split("\n"):
        name = image_name(line)
        if name is not None and name in renames and renames[name] != name:
            out.append(f"img: {renames[name]}")
        else:
            out.append(line)
    return "\n".join(out)


# ---- attach ----------------------------------------------------------------

def attach_images(folder: Path, grabbed: object) -> AttachResult:
    """The clipboard's image(s) saved into the pad images folder: a PIL image as
    the next `paste-NNN.png`, a list of paths each COPIED (never moved; a failing
    source name saves as `image<suffix>`, LLR-4408.19). The source is only read."""
    if grabbed is None:
        return AttachResult([], "No image found in the clipboard.")
    if isinstance(grabbed, list):
        if not grabbed:
            return AttachResult([], "No image found in the clipboard.")
        candidates = [p for p in grabbed
                      if isinstance(p, str)
                      and Path(p).suffix.lower() in IMAGE_EXTS
                      and os.path.isfile(p)]
        if not candidates:
            return AttachResult([], "Clipboard holds no image files.")
        names: list[str] = []
        for p in candidates:
            base = Path(p).name
            if not _image_ok(base):
                base = "image" + Path(p).suffix.lower()
            try:
                name = _free_name(folder, base)
                folder.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, folder / name)
            except OSError as exc:
                return AttachResult(names, f"The image could not be saved: {exc}")
            names.append(name)
        return AttachResult(names, None)
    if hasattr(grabbed, "mode"):
        try:
            dest = save_pil_image(folder, grabbed)
            return AttachResult([dest.name], None)
        except Exception as exc:
            return AttachResult([], f"The image could not be saved: {exc}")
    return AttachResult([], "No image found in the clipboard.")
