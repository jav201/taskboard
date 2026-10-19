"""The portfolio round's OWN synthetic board: six projects, 4-7 tasks each,
dates spread over ~10 weeks around a fixed TODAY. Synthetic data only.

States the round must survive: late work (Billing Migration), milestones
(Mobile Release 3.2, Customer Portal, Billing, Security Audit), waits
(`depends_on` on open work), a project with no dates at all (Brand Refresh),
a project already hidden from the presentation (Security Audit), and two
hidden tasks (Help-center links, Cost dashboards).

The project-level presentation state is prototyped in `Project.extra`
(`show_in_present`, `present_rank`): the shipped loader keeps unknown keys
there and `Board._to_dict` writes them back, so the prototype's flags
round-trip through a real save without touching the model."""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from taskboard.models import Board, Project, Task

TODAY = date(2026, 10, 19)          # a Monday
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]
CURSOR = "tb3"                       # the late, high-priority tax-rules task


def _d(off):
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


# (key, name, color, start_off, due_off)
PROJECTS = [
    ("cp", "Customer Portal", "violet", -35, 18),
    ("bm", "Billing Migration", "pink", -28, 6),
    ("mr", "Mobile Release 3.2", "sky", -14, 32),
    ("dp", "Data Platform", "lime", -21, 40),
    ("sa", "Security Audit", "indigo", -10, 12),
    ("br", "Brand Refresh", "green", None, None),
]
HIDDEN_PROJECTS = {"sa"}

# (key, project, title, phase, prio, start_off, due_off, deps, milestone)
TASKS = [
    ("c1", "cp", "Login redesign", "Done", "normal", -35, -20, [], False),
    ("c2", "cp", "Account settings page", "Doing", "normal", -12, 4, [], False),
    ("c3", "cp", "Invoice download", "Next", "high", -2, 9, ["c2"], False),
    ("c4", "cp", "Accessibility pass", "Backlog", "low", 5, 15, [], False),
    ("c5", "cp", "Portal go-live", "Backlog", "high", None, 18, ["c3"], True),
    ("c6", "cp", "Help-center links", "Next", "low", None, 11, [], False),
    ("b1", "bm", "Map legacy plans", "Done", "normal", -28, -14, [], False),
    ("b2", "bm", "Dual-run reconciliation", "Doing", "high", -10, -3, [], False),
    ("b3", "bm", "Tax rules for new regions", "Doing", "high", -6, -1, [], False),
    ("b4", "bm", "Customer notice emails", "Next", "normal", 0, 4, ["b3"], False),
    ("b5", "bm", "Cut-over weekend", "Backlog", "high", None, 6, ["b4"], True),
    ("b6", "bm", "Decommission old engine", "Backlog", "low", 8, 20, ["b5"], False),
    ("b7", "bm", "Refund edge cases", "Review", "normal", -4, 2, [], False),
    ("m1", "mr", "Feature freeze", "Done", "normal", None, -7, [], True),
    ("m2", "mr", "Offline mode", "Doing", "high", -14, 8, [], False),
    ("m3", "mr", "Push opt-in flow", "Next", "normal", 2, 14, ["m2"], False),
    ("m4", "mr", "Store screenshots", "Backlog", "low", 16, 22, [], False),
    ("m5", "mr", "Beta to testers", "Backlog", "normal", None, 24, ["m3"], True),
    ("m6", "mr", "Release 3.2", "Backlog", "high", None, 32, ["m5"], True),
    ("d1", "dp", "Ingest pipeline v2", "Doing", "normal", -21, 7, [], False),
    ("d2", "dp", "Schema registry", "Next", "normal", 3, 17, [], False),
    ("d3", "dp", "Revenue model", "Backlog", "high", 10, 30, ["d1"], False),
    ("d4", "dp", "Cost dashboards", "Backlog", "low", 25, 40, [], False),
    ("d5", "dp", "Retire nightly batch", "Backlog", "normal", 32, 40, ["d3"], False),
    ("s1", "sa", "Threat model review", "Doing", "high", -10, -2, [], False),
    ("s2", "sa", "Pen-test scheduling", "Next", "normal", 1, 5, [], False),
    ("s3", "sa", "Fix findings", "Backlog", "high", 6, 12, ["s2"], False),
    ("s4", "sa", "Audit report", "Backlog", "normal", None, 12, ["s3"], True),
    ("r1", "br", "Logo explorations", "Doing", "normal", None, None, [], False),
    ("r2", "br", "Type scale", "Next", "low", None, None, [], False),
    ("r3", "br", "Brand book draft", "Backlog", "normal", None, None, ["r1"], False),
    ("r4", "br", "Stakeholder review", "Backlog", "normal", None, None, [], False),
]
HIDDEN_TASKS = {"c6", "d4"}


def build(path: Path, order: list[str] | None = None) -> Board:
    """The board, saved nowhere until the caller saves it. `order` (project
    keys) reorders the BOARD's single project list — the alternative the page
    shows the consequence of."""
    projects = {}
    for key, name, color, s, d in PROJECTS:
        p = Project(name=name, color=color, start_date=_d(s), due_date=_d(d), id=f"p{key}")
        if key in HIDDEN_PROJECTS:
            p.extra["show_in_present"] = False
        projects[key] = p
    tasks = []
    for key, pk, title, phase, prio, s, d, deps, ms in TASKS:
        t = Task(title=title, project_id=projects[pk].id, phase=phase, priority=prio,
                 start_date=_d(s), due_date=_d(d), depends_on=[f"t{x}" for x in deps],
                 milestone=ms, phase_changed=(TODAY - timedelta(days=3)).isoformat(),
                 id=f"t{key}")
        t.show_in_present = key not in HIDDEN_TASKS
        tasks.append(t)
    keys = order or [k for k, *_ in PROJECTS]
    return Board([projects[k] for k in keys], tasks, path,
                 {"migrations": {"links": 1}, "seen_view_renumber_2026_07": True},
                 PHASES)
