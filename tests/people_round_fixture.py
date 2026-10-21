"""THROWAWAY prototype fixture — the people round's synthetic boards and directory.

A REAL registry (`boards.json` in the shipped format, read by the shipped
`Registry.load`) in a temporary folder, never `~/.taskboard`:

    <root>/board.json                    "Personal"  (the default board, id `main`)
    <root>/boards/client-a/board.json    "Client A"
    <root>/boards/course/board.json      "Course"
    <root>/people.json                   the directory the round proposes (D1)

Mentions are stored in the notes as handles (`@ana.ruiz`, the storage form the
round recommends); the prototype's tokeniser also reads `@[Name](p:id)`.
TODAY is pinned (a Tuesday). Synthetic people and tasks only.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path

from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task

TODAY = date(2026, 10, 20)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]

# handle (the stable id), name, role, note
PEOPLE = [
    ("ana.ruiz", "Ana Ruiz", "Client A PM", "Prefers a written agenda the day before"),
    ("andres.lima", "Andrés Lima", "Store ops lead", ""),
    ("diego.paz", "Diego Paz", "Client A data engineer", ""),
    ("elena.vidal", "Elena Vidal", "Client A sponsor", "Steering committee chair"),
    ("juana.soto", "Juana Soto", "Course student lead", ""),
    ("luis.mora", "Luis Mora", "Course TA", "Reviews every lab before publish"),
    ("marta.gil", "Marta Gil", "Accountant", "Invoices go out by the 25th"),
    ("pablo.ortiz", "Pablo Ortiz", "Physio", ""),
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
    "main": [("ph", "Home & paperwork", "green", None, None),
             ("pf", "Fitness block", "lime", -14, 30)],
    "client-a": [("ci", "Ingest & index", "sky", -21, 10),
                 ("ce", "Eval harness", "blue", -7, 24),
                 ("cr", "Pilot rollout", "indigo", -3, 32),
                 ("cd", "Docs & handover", "cyan", 2, 40)],
    "course": [("d4", "Module 4 · Volumes", "violet", -10, 5),
               ("d5", "Module 5 · Compose", "fuchsia", 3, 26)],
}

N_CHUNK = ("Waiting on @ana.ruiz to confirm the sample stores\n"
           "- 400-token chunks beat 800 on the golden set\n"
           "- ==send the table to @diego.paz== before the sync")
N_GOLDEN = ("Review the 40 questions with @ana.ruiz in Tuesday's sync\n"
            "- @andres.lima adds the store-ops wording\n"
            "- !!12 questions still have no answer key!!")
N_STEER = ("Agenda to @elena.vidal by Monday\n"
           "- demo: hybrid search on the pilot stores\n"
           "- ask @ana.ruiz for the go/no-go criteria")
N_INDEX = ("Index rebuild after the chunking choice\n"
           "- @diego.paz owns the nightly job")
N_EVAL = "Draft with @ana.ruiz; ++sign-off by the sponsor++ (@elena.vidal)"
N_STORES = "Shortlist from @andres.lima\n- 6 stores, 2 per region"
N_INVOICE = "Hours from the tracker; @marta.gil needs it by the 25th"
N_TAX = "Bring the receipts folder to @marta.gil\n- ask about the home-office share"
N_PHYSIO = "@pablo.ortiz · Thursday or Friday morning"
N_LAB = "@luis.mora reviews it before the publish\n- check on Windows and WSL"
N_TALK = "Guest talk by @ana.ruiz: RAG in retail, 20 min\n- @juana.soto collects questions"
N_CANARY = "Roll the new index to one store first\n- rollback plan in the runbook"

# key, project, title, phase, prio, start, due, deps, milestone, notes
TASKS = {
    "main": [
        ("p1", "ph", "Renew passport", "Next", "high", None, 1, [], False, ""),
        ("p2", "ph", "Tax filing papers", "Next", "high", None, -2, [], False, N_TAX),
        ("p3", "ph", "Fix the balcony door", "Doing", "low", None, -3, [], False, ""),
        ("p4", "pf", "Week 3 plan", "Doing", "normal", -2, 0, [], False, ""),
        ("p5", "pf", "10k race", "Backlog", "high", None, 30, ["p4"], True, ""),
        ("p6", "pf", "Book physio", "Next", "normal", None, 5, [], False, N_PHYSIO),
    ],
    "client-a": [
        ("c1", "ci", "Parse catalog PDFs", "Done", "normal", -21, -10, [], False, ""),
        ("c2", "ci", "Chunking experiments", "Review", "normal", -9, -1, [], False, N_CHUNK),
        ("c3", "ci", "Hybrid search index", "Doing", "high", -4, 3, ["c2"], False, N_INDEX),
        ("c4", "ci", "Store-ops glossary", "Next", "low", None, 8, [], False, ""),
        ("c5", "ce", "Golden question set", "Doing", "high", -6, 0, [], False, N_GOLDEN),
        ("c6", "ce", "Judge rubric", "Next", "normal", 1, 9, ["c5"], False, ""),
        ("c7", "ce", "Eval report v1", "Backlog", "high", None, 14, ["c6"], True, N_EVAL),
        ("c8", "cr", "Steering committee", "Next", "high", 2, 2, [], False, N_STEER),
        ("c9", "cr", "Pilot store list", "Doing", "normal", -3, 4, [], False, N_STORES),
        ("ca", "cr", "Canary release plan", "Backlog", "normal", 6, 18, ["c9"], False, N_CANARY),
        ("cb", "cd", "Invoice October", "Next", "normal", None, 5, [], False, N_INVOICE),
        ("cc", "cd", "Handover call", "Backlog", "normal", 21, 21, [], False, ""),
    ],
    "course": [
        ("k1", "d4", "Bind vs named volumes page", "Done", "normal", -10, -4, [], False, ""),
        ("k2", "d4", "Volume oracle script", "Review", "high", -3, -2, ["k1"], False, N_LAB),
        ("k3", "d4", "Module 4 publish", "Next", "high", None, 5, ["k2"], True, ""),
        ("k4", "d5", "Compose file anatomy", "Backlog", "normal", 3, 3, [], False, ""),
        ("k5", "d5", "Guest talk: RAG in retail", "Next", "normal", None, 9, [], False, N_TALK),
        ("k6", "d5", "Module 5 publish", "Backlog", "high", None, 26, ["k5"], True, ""),
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
    for key, pk, title, phase, prio, s, d, deps, ms, notes in TASKS[bid]:
        tasks.append(Task(title=title, project_id=projects[pk].id, phase=phase, priority=prio,
                          start_date=_d(s), due_date=_d(d), depends_on=[f"t{x}" for x in deps],
                          milestone=ms, notes=notes,
                          phase_changed=(TODAY - timedelta(days=2)).isoformat(), id=f"t{key}"))
    path = board_path(root, bid)
    path.parent.mkdir(parents=True, exist_ok=True)
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
    return reg
