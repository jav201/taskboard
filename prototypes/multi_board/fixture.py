"""THROWAWAY prototype fixture — the multi-board round's synthetic registry.

Four boards, each in its OWN folder (history.jsonl, images/, reports/ live
beside the board file, so two boards in one folder would share them):

    <root>/boards.json                            the registry (new)
    <root>/board.json                             "Main" — today's mixed board, in place
    <root>/boards/personal/board.json             "Personal"
    <root>/boards/client-retail-rag/board.json    "Client · Retail RAG"
    <root>/boards/course-docker/board.json        "Course · Docker"

"Main" is the board to split: it mixes client work (Retail RAG · pilot), course
work (Docker labs), personal admin and the agency's own site, with two links
that cross what would become board lines. Synthetic data only.
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task

TODAY = date(2026, 10, 20)          # a Tuesday
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]
SETTINGS = {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
            "seen_view_renumber_2026_07": True}


def _d(off):
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


# board id -> (name, colour, relative folder, last opened offset in hours)
BOARDS = [
    ("personal", "Personal", "green", "boards/personal", -2),
    ("client-retail-rag", "Client · Retail RAG", "sky", "boards/client-retail-rag", -20),
    ("course-docker", "Course · Docker", "violet", "boards/course-docker", -50),
    ("main", "Main", "fuchsia", ".", -120),
]

# board -> [(key, name, colour, start, due)]
PROJECTS = {
    "personal": [
        ("ph", "Home & paperwork", "green", None, None),
        ("pf", "Fitness block", "lime", -14, 30),
    ],
    "client-retail-rag": [
        ("ci", "Ingest & index", "sky", -21, 10),
        ("ce", "Eval harness", "blue", -7, 24),
    ],
    "course-docker": [
        ("d4", "Module 4 · Volumes", "violet", -10, 5),
        ("d5", "Module 5 · Compose", "indigo", 3, 26),
    ],
    "main": [
        ("mr", "Retail RAG · pilot", "sky", -18, 12),
        ("ml", "Docker labs", "violet", -25, 15),
        ("ma", "Home admin", "green", None, None),
        ("mw", "Agency website", "pink", -12, 28),
        ("mt", "Taxes 2026", "lime", -30, 9),
    ],
}

# board -> [(key, project, title, phase, prio, start, due, deps, milestone)]
TASKS = {
    "personal": [
        ("p1", "ph", "Renew passport", "Next", "high", None, 1, [], False),
        ("p2", "ph", "Car insurance quote", "Backlog", "normal", None, 6, [], False),
        ("p3", "ph", "Fix the balcony door", "Doing", "low", None, -3, [], False),
        ("p4", "pf", "Week 3 plan", "Doing", "normal", -2, 4, [], False),
        ("p5", "pf", "10k race", "Backlog", "high", None, 30, ["p4"], True),
        ("p6", "pf", "Book physio", "Next", "normal", None, 0, [], False),
    ],
    "client-retail-rag": [
        ("c1", "ci", "Parse catalog PDFs", "Done", "normal", -21, -10, [], False),
        ("c2", "ci", "Chunking experiments", "Review", "normal", -9, -1, [], False),
        ("c3", "ci", "Hybrid search index", "Doing", "high", -4, 3, ["c2"], False),
        ("c4", "ci", "Store-ops glossary", "Next", "low", None, 8, [], False),
        ("c5", "ce", "Golden question set", "Doing", "high", -6, 2, [], False),
        ("c6", "ce", "Judge rubric", "Next", "normal", 1, 9, ["c5"], False),
        ("c7", "ce", "Eval report v1", "Backlog", "high", None, 14, ["c6"], True),
        ("c8", "ce", "Latency budget", "Backlog", "normal", 10, 22, [], False),
    ],
    "course-docker": [
        ("k1", "d4", "Bind vs named volumes page", "Done", "normal", -10, -4, [], False),
        ("k2", "d4", "Volume oracle script", "Review", "high", -3, 0, ["k1"], False),
        ("k3", "d4", "Module 4 publish", "Next", "high", None, 5, ["k2"], True),
        ("k4", "d5", "Compose file anatomy", "Backlog", "normal", 3, 12, [], False),
        ("k5", "d5", "Healthcheck lab", "Backlog", "normal", 10, 20, ["k4"], False),
        ("k6", "d5", "Module 5 publish", "Backlog", "high", None, 26, ["k5"], True),
    ],
    "main": [
        ("r1", "mr", "Kick-off notes", "Done", "normal", -18, -15, [], False),
        ("r2", "mr", "Pilot store list", "Done", "normal", -14, -8, ["r1"], False),
        ("r3", "mr", "Demo env on Docker", "Doing", "high", -5, 2, ["l3"], False),
        ("r4", "mr", "Pilot results deck", "Next", "high", 2, 7, ["r3"], False),
        ("r5", "mr", "Pilot sign-off", "Backlog", "high", None, 12, ["r4"], True),
        ("r6", "mr", "Store staff FAQ", "Backlog", "low", 4, 10, [], False),
        ("r7", "mr", "Invoice #2", "Next", "normal", None, -1, [], False),
        ("l1", "ml", "Lab 1 · images", "Done", "normal", -25, -18, [], False),
        ("l2", "ml", "Lab 2 · networks", "Review", "normal", -12, -2, ["l1"], False),
        ("l3", "ml", "Compose template", "Doing", "high", -6, 1, ["l2"], False),
        ("l4", "ml", "Lab 3 · volumes", "Backlog", "normal", 3, 15, ["l3"], False),
        ("a1", "ma", "Dentist", "Next", "normal", None, 3, [], False),
        ("a2", "ma", "Gym membership", "Backlog", "low", None, None, [], False),
        ("a3", "ma", "Utility bill dispute", "Doing", "normal", None, -4, [], False),
        ("w1", "mw", "New services page", "Doing", "normal", -12, 5, [], False),
        ("w2", "mw", "Case study: retail RAG", "Backlog", "normal", 8, 20, ["r4"], False),
        ("w3", "mw", "Site launch", "Backlog", "high", None, 28, ["w1", "w2"], True),
        ("t1", "mt", "Collect receipts", "Doing", "normal", -30, 2, [], False),
        ("t2", "mt", "Accountant call", "Next", "normal", None, 4, ["t1"], False),
        ("t3", "mt", "File quarterly return", "Backlog", "high", None, 9, ["t2"], True),
    ],
}


def board_path(root: Path, bid: str) -> Path:
    rel = next(r for b, _n, _c, r, _h in BOARDS if b == bid)
    return root / rel / "board.json"


def build_board(root: Path, bid: str) -> Board:
    projects = {}
    for key, name, colour, s, d in PROJECTS[bid]:
        projects[key] = Project(name=name, color=colour, start_date=_d(s), due_date=_d(d),
                                id=f"p{key}")
    tasks = []
    for key, pk, title, phase, prio, s, d, deps, ms in TASKS[bid]:
        tasks.append(Task(title=title, project_id=projects[pk].id, phase=phase, priority=prio,
                          start_date=_d(s), due_date=_d(d), depends_on=[f"t{x}" for x in deps],
                          milestone=ms, phase_changed=(TODAY - timedelta(days=2)).isoformat(),
                          id=f"t{key}"))
    path = board_path(root, bid)
    path.parent.mkdir(parents=True, exist_ok=True)
    return Board(list(projects.values()), tasks, path, json.loads(json.dumps(SETTINGS)), PHASES)


def build(root: Path, last: str = "personal") -> Path:
    """Write the four boards and the registry under `root`; return the registry path."""
    from datetime import datetime
    now = datetime(2026, 10, 20, 9, 30)
    entries = []
    for bid, name, colour, rel, hours in BOARDS:
        build_board(root, bid).save()
        entries.append({"id": bid, "name": name, "color": colour,
                        "path": str(board_path(root, bid)),
                        "last_opened": (now + timedelta(hours=hours)).isoformat(timespec="minutes"),
                        "archived": False})
    reg = root / "boards.json"
    reg.write_text(json.dumps({"version": 1, "last": last, "boards": entries}, indent=2),
                   encoding="utf-8")
    return reg
