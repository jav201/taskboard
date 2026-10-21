"""The backlog round's synthetic boards, copied from
`prototypes/backlog_round/fixture.py` for the suite (batch 2026-10-20-batch-03), its
boards and registry unchanged, so no test imports a prototype.

A REAL registry (`boards.json` in the shipped format, read by the shipped
`Registry.load`) under the folder a test names, never `~/.taskboard` itself:

    <root>/board.json                    "Personal"  (the default board, id `main`)
    <root>/boards/client-a/board.json    "Client A"
    <root>/boards/course/board.json      "Course"
    <root>/elsewhere/board-copy.json     a copy of Client A, for `--open` / `--board`

TODAY is pinned (a Tuesday); the agenda's "rest of the week" runs to Sunday 25.
Synthetic data only.
"""
from __future__ import annotations

import json
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path

from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task

TODAY = date(2026, 10, 20)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]


def settings(offer: bool = False) -> dict:
    mig = {"links": LINKS_MIGRATION}
    if not offer:
        mig["milestones"] = MILESTONES_MIGRATION
    return {"migrations": mig, "seen_view_renumber_2026_07": True}


def _d(off):
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


# id, name, colour, relative folder, last opened (hours before now)
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
                 ("cr", "Pilot rollout", "indigo", -3, 32),
                 ("cd", "Docs & handover", "cyan", 2, 40)],
    "course": [("d4", "Module 4 · Volumes", "violet", -10, 5),
               ("d5", "Module 5 · Compose", "fuchsia", 3, 26)],
}

NOTE = ("Owner: username_subject\n- agree the sample with the store team\n"
        "- numbers by Friday\nRisk: the catalog export is late")

# key, project, title, phase, prio, start, due, deps, milestone, notes
TASKS = {
    "main": [
        ("p1", "ph", "Renew passport", "Next", "high", None, 1, [], False, ""),
        ("p2", "ph", "Car insurance quote", "Backlog", "normal", None, 4, [], False, ""),
        ("p3", "ph", "Fix the balcony door", "Doing", "low", None, -3, [], False, ""),
        ("p4", "pf", "Week 3 plan", "Doing", "normal", -2, 0, [], False, ""),
        ("p5", "pf", "10k race", "Backlog", "high", None, 30, ["p4"], True, ""),
        ("p6", "pf", "Book physio", "Next", "normal", None, 5, [], False, ""),
    ],
    "client-a": [
        ("c1", "ci", "Parse catalog PDFs", "Done", "normal", -21, -10, [], False, ""),
        ("c2", "ci", "Chunking experiments", "Review", "normal", -9, -1, [], False, NOTE),
        ("c3", "ci", "Hybrid search index", "Doing", "high", -4, 3, ["c2"], False, NOTE),
        ("c4", "ci", "Store-ops glossary", "Next", "low", None, 8, [], False, ""),
        ("c5", "ce", "Golden question set", "Doing", "high", -6, 0, [], False, NOTE),
        ("c6", "ce", "Judge rubric", "Next", "normal", 1, 9, ["c5"], False, ""),
        ("c7", "ce", "Eval report v1", "Backlog", "high", None, 14, ["c6"], True, ""),
        ("c8", "cr", "Steering committee", "Next", "high", 2, 2, [], False, ""),
        ("c9", "cr", "Pilot store list", "Doing", "normal", -3, 4, [], False, ""),
        ("ca", "cr", "Staff training", "Backlog", "normal", 6, 18, ["c9"], False, ""),
        ("cb", "cd", "Runbook draft", "Backlog", "normal", 2, 20, [], False, ""),
        ("cc", "cd", "Handover call", "Backlog", "normal", 21, 21, ["cb"], False, ""),
    ],
    "course": [
        ("k1", "d4", "Bind vs named volumes page", "Done", "normal", -10, -4, [], False, ""),
        ("k2", "d4", "Volume oracle script", "Review", "high", -3, -2, ["k1"], False, ""),
        ("k3", "d4", "Module 4 publish", "Next", "high", None, 5, ["k2"], True, ""),
        ("k4", "d5", "Compose file anatomy", "Backlog", "normal", 3, 3, [], False, ""),
        ("k5", "d5", "Healthcheck lab", "Backlog", "normal", 10, 20, ["k4"], False, ""),
        ("k6", "d5", "Module 5 publish", "Backlog", "high", None, 26, ["k5"], True, ""),
    ],
}


def board_path(root: Path, bid: str) -> Path:
    rel = next(r for b, _n, _c, r, _h in BOARDS if b == bid)
    return root / rel / "board.json"


def build_board(root: Path, bid: str, offer: bool = False) -> Board:
    projects = {}
    for key, name, colour, s, d in PROJECTS[bid]:
        projects[key] = Project(name=name, color=colour, start_date=_d(s), due_date=_d(d),
                                id=f"p{key}")
    tasks = []
    for key, pk, title, phase, prio, s, d, deps, ms, notes in TASKS[bid]:
        tasks.append(Task(title=title, project_id=projects[pk].id, phase=phase, priority=prio,
                          start_date=_d(s), due_date=_d(d), depends_on=[f"t{x}" for x in deps],
                          milestone=ms, notes=notes,
                          phase_changed=(TODAY - timedelta(days=2)).isoformat(), id=f"t{key}"))
    path = board_path(root, bid)
    path.parent.mkdir(parents=True, exist_ok=True)
    return Board(list(projects.values()), tasks, path, settings(offer and bid == "client-a"),
                 PHASES)


def build(root: Path, last: str = "client-a", offer: bool = False,
          with_copy: bool = False) -> Path:
    """Write the boards and the registry under `root`; return the registry path.
    `offer`: Client A has not answered the milestone offer yet (item 7).
    `with_copy`: a copy of Client A's file sits in `elsewhere/`, and the registry
    lists it as `taskboard --board elsewhere/board-copy.json` left it (item 9)."""
    now = datetime.now()
    entries = []
    for bid, name, colour, _rel, hours in BOARDS:
        build_board(root, bid, offer).save()
        entries.append({"id": bid, "name": name, "color": colour,
                        "path": str(board_path(root, bid).resolve()),
                        "last_opened": (now + timedelta(hours=hours)).isoformat(timespec="minutes"),
                        "archived": False})
    copy = copy_path(root)
    copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(board_path(root, "client-a"), copy)
    if with_copy:
        entries.append({"id": "board-copy", "name": "board-copy", "color": "pink",
                        "path": str(copy.resolve()),
                        "last_opened": (now - timedelta(minutes=40)).isoformat(timespec="minutes"),
                        "archived": False})
    reg = root / "boards.json"
    reg.write_text(json.dumps({"version": 1, "last": last, "boards": entries}, indent=2),
                   encoding="utf-8")
    return reg


def copy_path(root: Path) -> Path:
    return root / "elsewhere" / "board-copy.json"
