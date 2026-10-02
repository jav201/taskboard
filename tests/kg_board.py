"""The kg_mejoras board: the board the gantt/kanban prototype rounds were judged on.

Rebuilt here (not imported) because the prototype directory is throwaway and is
deleted once the rounds are folded into the code. Same five projects, same 28
tasks, same TODAY, so a render of the shipped view at 118x30 / 80x24 can be read
side by side with the frames the operator gave his verdict on
(`prototypes/kg_mejoras/out/*-118x30.txt`).

In memory only: `path` names a scratch file and nothing here calls `save()`.
"""
from __future__ import annotations

import copy
from datetime import date, timedelta
from pathlib import Path

from taskboard.models import Board, Project, Task

TODAY = date(2026, 9, 30)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]


def _d(off: int | None) -> str | None:
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


# (key, name, color, status, start_off, due_off)
PROJECTS = [
    ("web", "Website Redesign", "violet", "on_track", -40, 10),
    ("mob", "Mobile App", "sky", "on_track", -20, 35),
    ("api", "API Platform", "lime", "at_risk", -30, 21),
    ("dwh", "Data Warehouse", "amber", "on_track", -10, 60),
    ("ops", "Ops & Security", "rose", "on_track", -60, 5),
]

# (key, project, title, phase, prio, start_off, due_off, age_days, blocked, deps)
TASKS = [
    ("w1", "web", "Design homepage mockups", "Done", "normal", -38, -20, 18, False, []),
    ("w2", "web", "Build component library", "Review", "normal", -25, -3, 4, False, ["w1"]),
    ("w3", "web", "Fix checkout 500 error", "Doing", "high", -6, -2, 9, False, []),
    ("w4", "web", "Optimize image assets", "Next", "low", None, 6, 12, False, ["w2"]),
    ("w5", "web", "Launch new homepage", "Backlog", "high", 4, 10, 30, False, ["w2", "w4"]),
    ("w6", "web", "SEO redirects map", "Backlog", "normal", None, 14, 22, False, []),
    ("m1", "mob", "Set up CI pipeline", "Done", "normal", -20, -12, 12, False, []),
    ("m2", "mob", "Audit dependencies", "Doing", "normal", -8, 2, 6, False, []),
    ("m3", "mob", "Add push notifications", "Next", "normal", 1, 12, 3, False, ["m2"]),
    ("m4", "mob", "Offline sync", "Backlog", "high", 10, 28, 15, False, ["m3"]),
    ("m5", "mob", "Beta release to testers", "Backlog", "normal", 28, 35, 15, False, ["m4"]),
    ("m6", "mob", "Crash reporting", "Review", "low", -5, 1, 2, False, []),
    ("a1", "api", "Write API reference", "Doing", "normal", -14, -5, 21, False, []),
    ("a2", "api", "Deprecate v1 endpoints", "Backlog", "high", None, 7, 26, True, ["a3"]),
    ("a3", "api", "Partner notice emails", "Next", "high", -2, 3, 8, False, []),
    ("a4", "api", "Rate limiting", "Doing", "high", -9, 4, 10, False, []),
    ("a5", "api", "Plan Q4 roadmap", "Backlog", "normal", None, None, 40, False, []),
    ("a6", "api", "SDK regeneration", "Review", "normal", -6, -1, 7, False, ["a4"]),
    ("d1", "dwh", "Migrate user table", "Done", "low", -10, -4, 6, False, []),
    ("d2", "dwh", "Compress database backups", "Next", "normal", 2, 9, 11, False, []),
    ("d3", "dwh", "Archive old logs", "Backlog", "low", 15, 30, 19, False, []),
    ("d4", "dwh", "Daily revenue model", "Doing", "normal", -3, 18, 2, False, ["d1"]),
    ("d5", "dwh", "BI dashboard cut-over", "Backlog", "normal", 30, 60, 5, False, ["d4"]),
    ("o1", "ops", "Renew TLS certificate", "Doing", "high", -4, -1, 5, False, []),
    ("o2", "ops", "Rotate API keys", "Next", "high", None, 3, 14, False, []),
    ("o3", "ops", "Review pull requests", "Review", "normal", None, 0, 3, False, []),
    ("o4", "ops", "Update onboarding copy", "Backlog", "normal", None, None, 33, False, []),
    ("o5", "ops", "Pen-test findings", "Backlog", "high", 3, 20, 9, False, []),
]


TEAM = {"version": 3, "phases": PHASES,
        "projects": [{"id": "pweb", "name": "Website Redesign", "color": "violet",
                      "status": "on_track"}],
        "roster": [{"id": "jav", "name": "Javier", "hue": "sky"},
                   {"id": "ana", "name": "Ana", "hue": "amber"}]}

# A Setup state for the census: team on, the cursor on the folder row. Its folder
# is a path that does not exist, so a failing check's note never prints a real
# directory (batch 2026-10-02-batch-02, security S-4).
SETUP = {"enabled": True, "shared_dir": "D:/team-never-there", "interval_minutes": 30,
         "user_id": "jav", "projects": [{"id": "pweb", "name": "Website Redesign",
                                         "shared": True, "color": "violet"}],
         "roster": [{"id": "jav", "name": "Javier", "hue": "sky"}],
         "cursor_section": 0, "cursor_row": 1}


def census(tmp: Path):
    """(board, team state, setup state) for the app-wide colour and language
    censuses (batch 2026-10-02-batch-02): the oracle board plus two URL cards
    (`tw6`, and the selection `tw3`), three pinned tasks (the Focus Board draws
    only pinned work), three history records (the flow view), a team directory
    and a Setup state. All under `tmp`."""
    import json
    from datetime import datetime

    from taskboard import history
    from taskboard.team_sync import TEAM_FILENAME, TeamState
    b = build(tmp / "board.json")
    for tid in ("tw6", "tw3"):
        b.task_by_id(tid).urls = ["https://example.org/redirects"]
    for tid in ("tw3", "ta4", "tw6"):
        b.task_by_id(tid).pinned = True
    for i, (tid, frm, to) in enumerate([("tw3", "Next", "Doing"), ("tw2", "Doing", "Review"),
                                        ("tw1", "Review", "Done")]):
        history.append(b.path, {"task": tid, "from": frm, "to": to},
                       at=datetime(2026, 9, 20 + i, 10))
    team_dir = tmp / "team"
    team_dir.mkdir(exist_ok=True)
    (team_dir / TEAM_FILENAME).write_text(json.dumps(TEAM), encoding="utf-8")
    st = TeamState(team_dir, user_id="jav")
    st.load_config()
    return b, st, copy.deepcopy(SETUP)       # tests mutate it; never the shared one


def build(path: Path | str = "kg-board-never-saved.json") -> Board:
    projects = {}
    for key, name, color, status, s, d in PROJECTS:
        projects[key] = Project(name=name, color=color, status=status,
                                start_date=_d(s), due_date=_d(d), id=f"p{key}")
    tasks = []
    for key, pk, title, phase, prio, s, d, age, blocked, deps in TASKS:
        tasks.append(Task(
            title=title, project_id=projects[pk].id, phase=phase, priority=prio,
            start_date=_d(s), due_date=_d(d), blocked=blocked,
            depends_on=[f"t{x}" for x in deps],
            phase_changed=(TODAY - timedelta(days=age)).isoformat(), id=f"t{key}"))
    return Board(list(projects.values()), tasks, Path(path),
                 {"wip_limits": {"Doing": 4, "Review": 3}}, PHASES)
