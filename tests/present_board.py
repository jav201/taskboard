"""The PRES-C oracle board (batch 2026-10-07-batch-04, increment 001).

The exact fixture the PRES-C oracle frames were rendered from
(`.dev-flow/2026-10-07-batch-04/evidence/frames/PRES-C-*.txt`, captured by
`prototypes/present_e/build.py`): the kg_mejoras prototype board
(`prototypes/kg_mejoras/fixture.py build()`), frozen on its own TODAY, with the
NOTES / URLS overlay the presentation variant adds
(`prototypes/present_e/variants.py`). `path` points at a scratch name; `save()`
must never be called — the presentation is read-only.
"""
from __future__ import annotations

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

# The presentation variant's overlay (prototypes/present_e/variants.py).
NOTES = {
    "tw2": "Design tokens are frozen. Build buttons, inputs and cards from the "
           "approved mockups and publish the storybook before review.",
    "tw3": "The 500 is a missing tax-rate row for new regions. Roll back the "
           "last deploy if the fix is not green by end of day.",
    "tw4": "Convert hero images to AVIF and lazy-load below the fold. Target a "
           "homepage under 1.5 MB.",
    "tw5": "Feature-flag the cut-over, set DNS TTL to 300, and keep the rollback "
           "doc ready. Waits on the library and the asset pass.",
    "tw6": "Build the 301 map from the old URL scheme and submit the new sitemap "
           "after cut-over.",
}
URLS = {
    "tw3": ["https://status.example.com/incident/4821"],
    "tw2": ["https://design-system.example.com/tokens"],
}
PROJECT_ID = "pweb"
CURSOR = "tw3"          # PRES-C's cursor task: the late, high-priority one


def build(path: Path | None = None) -> Board:
    """The frozen oracle board; `path` is a scratch name, never saved."""
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
    b = Board(list(projects.values()), tasks,
              path or Path("PRESENT-oracle-never-saved.json"),
              # marked as migrated: this board is new-model data — its links
              # already speak the shipped storage (the kg_board.py seam); an
              # unmarked board would get run_link_migration at app startup and
              # its depends_on rewritten under the presentation test.
              # seen_view_renumber_2026_07: the one-time renumber notice has
              # been shown — without it app startup writes the mark and the
              # AT's "leaves no trace" net trips on a legitimate mount write.
              {"wip_limits": {"Doing": 4, "Review": 3},
               "migrations": {"links": 1},
               "seen_view_renumber_2026_07": True}, PHASES)
    for t in b.visible_tasks(False):
        if t.id in NOTES:
            t.notes = NOTES[t.id]
        if t.id in URLS:
            t.urls = list(URLS[t.id])
    return b
