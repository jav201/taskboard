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

import copy
import json
import os
import re
import shutil
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

    def create(self, name: str, color: str, now: datetime, settings: dict) -> BoardEntry:
        """A new board in its own folder `boards/<slug>/` beside the registry:
        an empty board file (no project, no task, the default phases, `settings`),
        never written into a folder that already exists. Raises `ValueError` for
        a name that is empty once cleaned."""
        name = clean_name(name)
        if not name:
            raise ValueError("a board needs a name")
        bid = self.next_id(name)
        folder = self.path.parent / "boards" / bid
        folder.mkdir(parents=True, exist_ok=False)
        try:
            Board([], [], folder / "board.json", dict(settings)).save_atomic()
            entry = BoardEntry(bid, name, color if color in PROJECT_COLORS else "violet",
                               str((folder / "board.json").resolve()),
                               now.isoformat(timespec="minutes"))
            self.entries.append(entry)
            try:
                self.save()
            except OSError:
                self.entries.remove(entry)          # nothing registered (code review F1)
                raise
        except OSError:
            shutil.rmtree(folder, ignore_errors=True)   # the folder this call made, and only it
            raise
        return entry

    def next_id(self, name: str) -> str:
        """The id — and folder name — a board of this name would get: its slug,
        made unique against the registry and the folders already under `boards/`."""
        root = self.path.parent / "boards"
        taken = {p.name.lower() for p in root.iterdir()} if root.is_dir() else set()
        return self._unique_id(slug(clean_name(name)), taken)

    def edit(self, bid: str, name: str, color: str) -> None:
        name = clean_name(name)
        entry = self.get(bid)
        if entry is None or not name:
            return
        before = (entry.name, entry.color)
        entry.name = name
        entry.color = color if color in PROJECT_COLORS else entry.color
        try:
            self.save()
        except OSError:
            entry.name, entry.color = before        # as on disk (code review F1)
            raise

    def archive(self, bid: str) -> None:
        entry = self.get(bid)
        if entry is not None:
            entry.archived = True
            try:
                self.save()
            except OSError:
                entry.archived = False              # as on disk (code review F1)
                raise

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
    data = path.read_bytes()
    n = 1
    while True:
        dest = path.with_name(f"{path.name}.pre-move-{day}" + (f"-{n}" if n > 1 else ""))
        try:
            with open(dest, "xb") as fh:
                fh.write(data)
            return dest
        except FileExistsError:
            n += 1


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
    try:
        if plan.refusal:
            raise OSError(plan.refusal)
        if _stamp(dst.path) != plan.dst_stamp:
            raise OSError("the target board changed since the move was planned")
        new_src, new_dst = copy.deepcopy(src), copy.deepcopy(dst)
        ids = {t.id for t in plan.tasks}
        for b in (src, dst):
            if _backup(b.path, day):
                steps.append(f"copied {b.path.name}")
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
