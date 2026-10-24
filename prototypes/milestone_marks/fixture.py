"""THROWAWAY prototype fixture — the milestone-marks round's synthetic boards.

A REAL registry (`boards.json`, read by the shipped `Registry.load`) in a
temporary folder, never `~/.taskboard`:

    <root>/board.json                    "Personal"  (the default board, id `main`)
    <root>/boards/client-a/board.json    "Client A"  (the gantt the round is about)
    <root>/boards/course/board.json      "Course"
    <root>/marks.json                    the global class directory the round proposes (D2)

A milestone's class is stored as the task's `mark` key (`"mark": "payment"`):
the shipped `Task.extra` already keeps unknown keys, so the format needs no
migration and an older taskboard round-trips it untouched. TODAY is pinned (a
Tuesday). Synthetic data only.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path

from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task

TODAY = date(2026, 10, 20)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]

# id, name, shape (filled), hollow twin, colour key (views.HEX)
CLASSES = [
    ("delivery", "Delivery", "▲", "△", "cyan"),
    ("payment", "Payment", "⬢", "⬡", "amber"),
    ("review", "Review", "■", "□", "violet"),
    ("launch", "Launch", "★", "☆", "pink"),
]


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
    "main": [("ph", "Home & paperwork", "green", -5, 25),
             ("pf", "Fitness block", "lime", -14, 30)],
    "client-a": [("ci", "Ingest & index", "sky", -21, 10),
                 ("ce", "Eval harness", "blue", -7, 24),
                 ("cr", "Pilot rollout", "indigo", -3, 32),
                 ("cd", "Docs & handover", "green", 2, 40)],
    "course": [("d4", "Module 4 · Volumes", "violet", -10, 5),
               ("d5", "Module 5 · Compose", "fuchsia", 3, 26)],
}

# key, project, title, phase, prio, start, due, deps, milestone, mark, done
TASKS = {
    "main": [
        ("p1", "ph", "Renew passport", "Next", "high", None, 1, [], False, None),
        ("p2", "ph", "Tax filing papers", "Next", "high", None, -2, [], False, None),
        ("p3", "ph", "Deposit back from landlord", "Next", "normal", None, 4, [], True, "payment"),
        ("p4", "pf", "Week 3 plan", "Doing", "normal", -2, 0, [], False, None),
        ("p5", "pf", "10k race", "Backlog", "high", None, 30, ["p4"], True, None),
    ],
    "client-a": [
        ("c1", "ci", "Catalog parsed", "Done", "normal", None, -10, [], True, "delivery"),
        ("c2", "ci", "Chunking experiments", "Review", "normal", -9, -1, [], False, None),
        ("c3", "ci", "Hybrid search index", "Doing", "high", -4, 3, ["c2"], False, None),
        ("c4", "ci", "Index v1 delivered", "Next", "high", None, 6, ["c3"], True, "delivery"),
        ("c5", "ce", "Golden question set", "Doing", "high", -6, 0, [], False, None),
        ("c6", "ce", "Rubric sign-off", "Review", "normal", None, -2, ["c5"], True, "review"),
        ("c7", "ce", "Eval report v1", "Backlog", "high", None, 14, [], True, "review"),
        ("c8", "cr", "Kickoff invoice paid", "Done", "normal", None, -15, [], True, "payment"),
        ("c9", "cr", "Steering go/no-go", "Next", "high", None, 0, [], True, "review"),
        ("ca", "cr", "Pilot store list", "Doing", "normal", -3, 4, [], False, None),
        ("cb", "cr", "Pilot launch", "Backlog", "high", None, 18, ["ca"], True, "launch"),
        ("cc", "cr", "Milestone 2 invoice", "Backlog", "normal", None, 21, [], True, "payment"),
        ("cd", "cd", "Handover call", "Backlog", "normal", None, 27, [], True, None),
        ("ce", "cd", "Final payment", "Backlog", "normal", None, 38, [], True, "payment"),
    ],
    "course": [
        ("k1", "d4", "Bind vs named volumes page", "Done", "normal", -10, -4, [], False, None),
        ("k2", "d4", "Lab review with the TA", "Next", "high", None, 1, [], True, "review"),
        ("k3", "d4", "Module 4 publish", "Next", "high", None, 5, ["k2"], True, "launch"),
        ("k4", "d5", "Compose file anatomy", "Backlog", "normal", 3, 9, [], False, None),
        ("k6", "d5", "Module 5 publish", "Backlog", "high", None, 26, [], True, "launch"),
    ],
}


def board_path(root: Path, bid: str) -> Path:
    rel = next(r for b, _n, _c, r, _h in BOARDS if b == bid)
    return root / rel / "board.json"


def build_board(root: Path, bid: str, marks: bool = True) -> Board:
    projects = {}
    for key, name, colour, s, d in PROJECTS[bid]:
        projects[key] = Project(name=name, color=colour, start_date=_d(s), due_date=_d(d),
                                id=f"p{key}")
    tasks = []
    for key, pk, title, phase, prio, s, d, deps, ms, mark in TASKS[bid]:
        tasks.append(Task(title=title, project_id=projects[pk].id, phase=phase, priority=prio,
                          start_date=_d(s), due_date=_d(d), depends_on=[f"t{x}" for x in deps],
                          milestone=ms, extra=({"mark": mark} if (mark and marks) else {}),
                          phase_changed=(TODAY - timedelta(days=2)).isoformat(), id=f"t{key}"))
    path = board_path(root, bid)
    path.parent.mkdir(parents=True, exist_ok=True)
    return Board(list(projects.values()), tasks, path, settings(), PHASES)


def build(root: Path, last: str = "client-a", marks: bool = True) -> Path:
    now = datetime.now()
    entries = []
    for bid, name, colour, _rel, hours in BOARDS:
        build_board(root, bid, marks).save()
        entries.append({"id": bid, "name": name, "color": colour,
                        "path": str(board_path(root, bid).resolve()),
                        "last_opened": (now + timedelta(hours=hours)).isoformat(timespec="minutes"),
                        "archived": False})
    reg = root / "boards.json"
    reg.write_text(json.dumps({"version": 1, "last": last, "boards": entries}, indent=2),
                   encoding="utf-8")
    (root / "marks.json").write_text(json.dumps(
        {"version": 1, "marks": [{"id": i, "name": n, "shape": s, "colour": k}
                                 for i, n, s, _h, k in CLASSES]}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    return reg
