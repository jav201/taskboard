"""THROWAWAY prototype fixture — the capture round's synthetic boards, directories and inbox.

A REAL registry (`boards.json` in the shipped format, read by the shipped
`Registry.load`) in a temporary folder, never `~/.taskboard`:

    <root>/board.json                    "Personal"  (the default board, id `main`)
    <root>/boards/client-a/board.json    "Client A"
    <root>/boards/course/board.json      "Course"
    <root>/people.json, marks.json       the shipped directories
    <root>/inbox.json                    the round's proposed global inbox (D1)
    <root>/<board>/history.jsonl         creation events for SOME tasks (D3)

Creation order (item 2, D3): a task added after the field ships carries
`created` (an ISO datetime, kept by the shipped `Task.extra`, so no code under
`taskboard/` changes); an older one may have a `from: null` history record; the
oldest have neither and only their place in the board file says anything.
TODAY is pinned (a Wednesday). Synthetic people and tasks only.
"""
from __future__ import annotations

import json
import struct
import zlib
from datetime import date, datetime, timedelta
from pathlib import Path

from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task

TODAY = date(2026, 11, 4)
CREATED_SINCE = date(2026, 10, 31)      # the day `created` would ship (D3)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]

PEOPLE = [
    ("ana.ruiz", "Ana Ruiz", "Client A PM", ""),
    ("andres.lima", "Andrés Lima", "Store ops lead", ""),
    ("diego.paz", "Diego Paz", "Client A data engineer", ""),
    ("elena.vidal", "Elena Vidal", "Client A sponsor", ""),
    ("luis.mora", "Luis Mora", "Course TA", ""),
    ("marta.gil", "Marta Gil", "Accountant", ""),
]
MARKS = [("payment", "Payment", "▲", "amber"), ("release", "Release", "★", "cyan")]


def settings() -> dict:
    return {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
            "seen_view_renumber_2026_07": True}


def _d(off):
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


BOARDS = [
    ("main", "Personal", "green", ".", -30),
    ("client-a", "Client A", "sky", "boards/client-a", -2),
    ("course", "Course", "violet", "boards/course", -54),
]

PROJECTS = {
    "main": [("ph", "Home & paperwork", "green", None, None),
             ("pf", "Fitness block", "lime", -14, 30)],
    "client-a": [("ci", "Ingest & index", "sky", -21, 10),
                 ("ce", "Eval harness", "blue", -7, 24),
                 ("cr", "Pilot rollout", "indigo", -3, 32)],
    "course": [("d4", "Module 4 · Volumes", "violet", -10, 5),
               ("d5", "Module 5 · Compose", "fuchsia", 3, 26)],
}

N_CHUNK = ("Waiting on @ana.ruiz to confirm the sample stores\n"
           "- 400-token chunks beat 800 on the golden set\n"
           "- ==send the table to @diego.paz== before the sync")
N_GOLDEN = ("Review the 40 questions with @ana.ruiz in Tuesday's sync\n"
            "- !!12 questions still have no answer key!!\n"
            "- ++rubric draft approved++")
N_STEER = ("Agenda to @elena.vidal by Monday\n"
           "- demo: hybrid search on the pilot stores\n"
           "- ask for the go/no-go criteria")
N_INDEX = "Index rebuild after the chunking choice\n- @diego.paz owns the nightly job"
N_STORES = "Shortlist from @andres.lima\n- 6 stores, 2 per region"
N_INVOICE = "Hours from the tracker; @marta.gil needs it by the 25th"
N_LAB = "@luis.mora reviews it before the publish\n- check on Windows and WSL"
N_VOL = "Bind mounts vs named volumes\n- the oracle prints the inode"
N_SHOES = "Long run Sunday 14 km\n- easy pace, heart rate under 150"
# the multicolour note of item 3 (six pens; today's three markers + three proposed)
N_COLOUR = ("Sync notes, 3 pens\n"
            "- ==decided: 400-token chunks==\n"
            "- !!blocker: 12 questions lack a key!!\n"
            "- ++done: rubric draft++\n"
            "- ::ask @ana.ruiz for the store list::\n"
            "- ^^idea: judge with two models^^\n"
            "- %%later: cost per query%%")

# key, project, title, phase, prio, start, due, milestone, mark, notes, urls, images
TASKS = {
    "main": [
        ("p1", "ph", "Renew passport", "Next", "high", None, 1, False, None, "", [], []),
        ("p2", "ph", "Tax filing papers", "Next", "high", None, -2, False, None,
         "Receipts folder to @marta.gil", [], []),
        ("p3", "pf", "Week 3 plan", "Doing", "normal", -2, 0, False, None, N_SHOES, [], []),
        ("p4", "pf", "10k race", "Backlog", "high", None, 30, True, None, "", [], []),
        ("p5", "ph", "Pay the rent", "Next", "normal", None, 4, True, "payment", "", [], []),
    ],
    "client-a": [
        ("c1", "ci", "Parse catalog PDFs", "Done", "normal", -21, -10, False, None, "", [], []),
        ("c2", "ci", "Chunking experiments", "Review", "normal", -9, -1, False, None, N_CHUNK,
         ["https://example.com/chunking-notes"], []),
        ("c3", "ci", "Hybrid search index", "Doing", "high", -4, 3, False, None, N_INDEX, [], []),
        ("c4", "ce", "Golden question set", "Doing", "high", -6, 0, False, None, N_GOLDEN,
         [], ["golden-sheet.png"]),
        ("c5", "ce", "Judge rubric", "Next", "normal", 1, 9, False, None, "", [], []),
        ("c6", "ce", "Eval report v1", "Backlog", "high", None, 14, True, "release", "", [], []),
        ("c7", "cr", "Steering committee", "Next", "high", 2, 2, False, None, N_STEER, [], []),
        ("c8", "cr", "Pilot store list", "Doing", "normal", -3, 4, False, None, N_STORES, [], []),
        ("c9", "cr", "Invoice October", "Next", "normal", None, 5, True, "payment", N_INVOICE, [], []),
        ("ca", "ce", "Sync notes · Oct 30", "Review", "normal", None, None, False, None, N_COLOUR, [], []),
    ],
    "course": [
        ("k1", "d4", "Bind vs named volumes page", "Done", "normal", -10, -4, False, None, N_VOL, [], []),
        ("k2", "d4", "Volume oracle script", "Review", "high", -3, -2, False, None, N_LAB, [], []),
        ("k3", "d4", "Module 4 publish", "Next", "high", None, 5, True, "release", "", [], []),
        ("k4", "d5", "Compose file anatomy", "Backlog", "normal", 3, 3, False, None, "", [], []),
    ],
}

# how each task's creation is known (D3): ("c", when) = the new `created` field,
# ("h", when) = a `from: null` record in history.jsonl, absent = unknown (board order only).
# The board file order above is the append order.
CREATION = {
    "tc4": ("h", "2026-10-21T09:12:00"), "tc5": ("h", "2026-10-22T16:40:00"),
    "tc6": ("h", "2026-10-22T16:41:00"), "tc7": ("h", "2026-10-27T11:05:00"),
    "tc8": ("h", "2026-10-28T10:30:00"), "tc9": ("c", "2026-11-02T08:55:00"),
    "tca": ("c", "2026-10-31T18:20:00"),
    "tk3": ("h", "2026-10-25T20:02:00"), "tk4": ("c", "2026-11-03T21:47:00"),
    "tp3": ("h", "2026-10-26T07:30:00"), "tp4": ("h", "2026-10-26T07:31:00"),
    "tp5": ("c", "2026-11-04T08:10:00"),
}

# the inbox (D1: one global file): notes captured during meetings, not yet dumped.
# A topic is the text between blank lines; `img:` lines are attached images.
INBOX = [
    ("n1", "2026-11-04T09:31:00",
     "Golden set: 12 questions still have no answer key\n"
     "ask @ana.ruiz which stores count"),
    ("n2", "2026-11-04T09:38:00",
     "Volume lab fails on WSL\n"
     "the oracle script expects /mnt/c\n"
     "img: whiteboard-0938.png"),
    ("n3", "2026-11-04T09:44:00",
     "Quote for the new client: contracts Q&A\n"
     "two weeks, fixed price"),
]
INBOX_LIVE = "Steering deck: demo the hybrid search on pilot stores"   # typed live in the scenes


def board_path(root: Path, bid: str) -> Path:
    rel = next(r for b, _n, _c, r, _h in BOARDS if b == bid)
    return root / rel / "board.json"


def tiny_png(path: Path, rgb=(45, 212, 191)) -> None:
    """A 24x16 solid PNG (stdlib only) so an attached image is a real file."""
    w, h = 24, 16
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def build_board(root: Path, bid: str) -> Board:
    projects = {}
    for key, name, colour, s, d in PROJECTS[bid]:
        projects[key] = Project(name=name, color=colour, start_date=_d(s), due_date=_d(d),
                                id=f"p{key}")
    path = board_path(root, bid)
    path.parent.mkdir(parents=True, exist_ok=True)
    tasks, hist = [], []
    for key, pk, title, phase, prio, s, d, ms, mark, notes, urls, imgs in TASKS[bid]:
        tid = f"t{key}"
        extra = {}
        how = CREATION.get(tid)
        if how and how[0] == "c":
            extra["created"] = how[1]
        if how and how[0] in "ch":
            hist.append({"task": tid, "from": None, "to": phase, "at": how[1]})
        images = []
        for im in imgs:
            p = path.parent / "images" / tid / im
            tiny_png(p)
            images.append(str(p))
        tasks.append(Task(title=title, project_id=projects[pk].id, phase=phase, priority=prio,
                          start_date=_d(s), due_date=_d(d), milestone=ms, mark=mark, notes=notes,
                          urls=list(urls), images=images,
                          phase_changed=(TODAY - timedelta(days=2)).isoformat(), id=tid,
                          extra=extra))
    if hist:
        hist.sort(key=lambda r: r["at"])
        (path.parent / "history.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in hist), encoding="utf-8")
    return Board(list(projects.values()), tasks, path, settings(), PHASES)


def build(root: Path, last: str = "client-a") -> Path:
    now = datetime.now()
    entries = []
    for bid, name, colour, _rel, hours in BOARDS:
        build_board(root, bid).save()
        entries.append({"id": bid, "name": name, "color": colour,
                        "path": str(board_path(root, bid).resolve()),
                        "last_opened": (now + timedelta(hours=hours)).isoformat(timespec="minutes"),
                        "archived": False})
    reg = root / "boards.json"
    reg.write_text(json.dumps({"version": 1, "last": last, "boards": entries}, indent=2),
                   encoding="utf-8")
    (root / "people.json").write_text(json.dumps(
        {"version": 1, "people": [{"id": h, "name": n, "role": r, "note": note}
                                  for h, n, r, note in PEOPLE]}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    (root / "marks.json").write_text(json.dumps(
        {"version": 1, "marks": [{"id": i, "name": n, "shape": s, "colour": c, "hidden": False}
                                 for i, n, s, c in MARKS]}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    tiny_png(root / "inbox" / "images" / "n2" / "whiteboard-0938.png", (251, 191, 36))
    (root / "inbox.json").write_text(json.dumps(
        {"version": 1, "notes": [{"id": i, "at": at, "text": t, "dumped": None}
                                 for i, at, t in INBOX]}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    return reg
