"""P1 premise probes for batch 2026-10-04-batch-02 (C-43). Run from the repo root:
    python .dev-flow/2026-10-04-batch-02/evidence/p1_premises.py > .dev-flow/2026-10-04-batch-02/evidence/p1-premises.txt
Synthetic boards in a temp dir only; never the operator's board."""
from __future__ import annotations

import asyncio
import json
import subprocess
import sys
import tempfile
from dataclasses import fields
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from taskboard import models, views, keymap, modals  # noqa: E402
from taskboard.models import Board, Project, Task  # noqa: E402

TODAY = date(2026, 10, 4)


def iso(n):
    return (TODAY + timedelta(days=n)).isoformat()


def head(t):
    print(f"\n## {t}")


head("P-1 Task has no milestone field; an unknown 'milestone' key round-trips through extra")
print("Task fields:", [f.name for f in fields(Task)])
t = Task.from_dict({"id": "a", "title": "x", "milestone": True})
print("from_dict({'milestone': True}).extra =", t.extra)
print("_to_dict keeps it:", Board._to_dict(t).get("milestone"))

head("P-2 'M' is unbound: KEYMAP keys and every modal BINDINGS")
bound = [k.keys for k in keymap.KEYMAP]
print("any KEYMAP entry binds 'M':", any("M" in k.split(",") for k in bound))
mods = []
for name in dir(modals):
    obj = getattr(modals, name)
    for b in getattr(obj, "BINDINGS", []) if isinstance(obj, type) else []:
        key = b[0] if isinstance(b, tuple) else b.key
        if "M" in str(key).split(","):
            mods.append(name)
print("modal classes binding 'M':", mods)
print("'m' bound:", any("m" in k.split(",") for k in bound), "· 'c' ->",
      [k.action for k in keymap.KEYMAP if k.keys == "c"])

head("P-3 the shipped gantt draws a one-day task (start == due) as a single ◆ in its priority hue, no label mark")
p = Project("Web", "sky", id="p1", due_date=iso(20))
tasks = [Task("Launch", "p1", "Doing", "high", start_date=iso(6), due_date=iso(6), id="m1"),
         Task("Build", "p1", "Doing", "normal", start_date=iso(0), due_date=iso(4), id="t1")]
b = Board([p], tasks, Path(tempfile.gettempdir()) / "p1probe.json", phases=["Backlog", "Doing", "Done"])
txt = views.render_gantt(b, False, "t1", TODAY, 118, 30)
for ln in txt.plain.split("\n")[:7]:
    print(repr(ln))
cells = views._gantt_bar(tasks[0], b, views.gantt_axis(80, TODAY, *views.gantt_window(
    views.gantt_plan(b, False, "t1", TODAY, 27), TODAY)), set(), 0)
print("one-day bar cells (non-blank):", [c for c in cells if c[0] != " "])

head("P-4 gantt: rest work (done or archived) draws no row; nav walks GanttGroup.open only")
tasks.append(Task("Mock-ups ok", "p1", "Done", start_date=iso(-5), due_date=iso(-5), id="d1"))
groups = views.gantt_plan(b, False, "t1", TODAY, 27)
print("GanttGroup fields:", views.GanttGroup._fields)
print("open:", [x.id for x in groups[0].open], "rest:", [x.id for x in groups[0].rest])
print("nav:", views.nav_model("gantt", b, False, TODAY, 118, 30, selected_id="t1"))
print("'Mock-ups ok' painted:", "Mock-ups ok" in views.render_gantt(b, False, "t1", TODAY, 118, 30).plain)

head("P-5 kanban: header 'N tasks' and the WIP tags count every visible task (phase_buckets over plan.tasks)")
plan = views.kanban_plan(b, False, "t1", TODAY, 118, 30)
print("plan.tasks:", [x.id for x in plan.tasks])
print("buckets:", [[x.id for x in bk] for bk in views.phase_buckets(b, plan.tasks)])
print("header row:", repr(views.render_kanban(b, False, "t1", TODAY, 118, 30).plain.split("\n")[0]))

head("P-6 team push writes every Task field (Board._to_dict); a pulled task goes through Task.from_dict")
import inspect  # noqa: E402
from taskboard import team_sync  # noqa: E402
src = inspect.getsource(team_sync.TeamState.push)
print("push uses board._to_dict:", "board._to_dict(t)" in src)
print("foreign_tasks uses Task.from_dict:", "Task.from_dict(tdict)" in inspect.getsource(team_sync.TeamState.foreign_tasks))

head("P-7 the B1 migration seat: settings['migrations'] dict, links_marked, _create_beside, run_link_migration")
for n in ("links_marked", "_create_beside", "run_link_migration", "LINKS_MIGRATION", "MIGRATION_BACKUP"):
    print(n, hasattr(models, n))
print("links_marked({'migrations': {'links': 1, 'milestones': 1}}) =",
      models.links_marked({"migrations": {"links": 1, "milestones": 1}}))

head("P-8 Board.load on a missing path seeds, saves, and leaves load_report == {} (no 'created' signal today)")
with tempfile.TemporaryDirectory() as d:
    nb = Board.load(Path(d) / "fresh.json")
    print("file written:", (Path(d) / "fresh.json").exists(), "· load_report:", nb.load_report,
          "· settings:", nb.settings)
    one_day = [x.title for x in nb.tasks if x.start_date and x.start_date == x.due_date]
    due_only = [x.title for x in nb.tasks if x.due_date and not x.start_date
                and not nb.is_done(x) and not x.archived]
    print("seed one-day tasks:", one_day, "· seed open due-only tasks:", len(due_only))

head("P-10 the undo snapshot fields (app._UNDO_FIELDS)")
from taskboard.app import TaskboardApp  # noqa: E402
print(TaskboardApp._UNDO_FIELDS)

head("P-12 the editor's one-row chip threshold and its widget ids")
print("TASK_CHIPS_ONE_ROW =", modals.TASK_CHIPS_ONE_ROW)

head("P-13 Textual OptionList bindings (does it claim space / enter?)")
from textual.widgets import OptionList  # noqa: E402
print([(b.key, b.action) for b in OptionList.BINDINGS])
import textual  # noqa: E402
print("textual", textual.__version__)

head("P-14 bump_due moves only due_date")
x = Task("m", start_date=iso(3), due_date=iso(3))
models.bump_due(x, 1, TODAY)
print("after +1: start", x.start_date, "due", x.due_date)

head("P-15 the B1 link-migration toast and undo entry shape (app source)")
src = inspect.getsource(TaskboardApp._migrate_links) + inspect.getsource(TaskboardApp.action_undo)
print('undo entry key "migration":', '"migration"' in src,
      "· undo toast says 'Links migration undone':", "Links migration undone" in src)
print("on_mount order:", [ln.strip() for ln in inspect.getsource(TaskboardApp.on_mount).splitlines()
                          if ln.strip().startswith(("if not self._migrate", "self._"))])
