"""P1 iteration-2 thresholds (C-39, qa Q-1/Q-2/Q-21) against the SHIPPED kanban, base tree.
    python -B .dev-flow/2026-10-04-batch-02/evidence/p1_thresholds_shipped.py > .../p1-thresholds-shipped.txt
The board: `kg_board.shifted` + the §5 milestone set (the flag carried in `extra` on the base tree,
which has no field). "After the batch" the kanban lays out the board WITHOUT its milestones
(LLR-603.1), so the band facts are measured on that board with the shipped `_band_facts`. The
segments are laid by the PROTOTYPE's own `_ms_segment` / `_ms_bits` (run in the kg-mejoras worktree
in a subprocess, since both trees ship a `taskboard` package) at each band's shipped room:
room = width − facts − 4 (" ── ") − 2 (the rule tail kept)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
import kg_board  # noqa: E402
from taskboard import views  # noqa: E402
from taskboard.models import Task  # noqa: E402

PROTO = ROOT / ".claude/worktrees/kg-mejoras/prototypes/kg_mejoras"
T = date.today()


def board(tmp):
    b = kg_board.shifted(Path(tmp) / "board.json")
    for tid, off in (("tw5", 10), ("tm5", 35), ("ta3", 3)):
        t = b.task_by_id(tid)
        t.start_date = t.due_date = (T + timedelta(days=off)).isoformat()
        t.extra["milestone"] = True
    for tid, pid, title, ph, off, deps in (
            ("tw0", "pweb", "Mockups approved", "Done", -12, ["tw1"]),
            ("to0", "pops", "Security review sign-off", "Next", -2, []),
            ("td0", "pdwh", "Revenue model signed off", "Backlog", 18, ["td4"])):
        d = (T + timedelta(days=off)).isoformat()
        b.tasks.append(Task(title, pid, ph, start_date=d, due_date=d, depends_on=deps,
                            phase_changed=d, extra={"milestone": True}, id=tid))
    b.task_by_id("td5").depends_on = ["td0"]
    return b


with tempfile.TemporaryDirectory() as tmp:
    b = board(tmp)
    vis = b.visible_tasks(False)
    ms = [t for t in vis if t.extra.get("milestone")]
    print("today", T, "· visible", len(vis), "· milestones", len(ms), "· kanban N tasks after", len(vis) - len(ms))
    work = [t for t in b.tasks if not t.extra.get("milestone")]
    b.tasks = work                      # the kanban's input after LLR-603.1
    rooms = {}
    for w in (118, 80):
        plan = views.kanban_plan(b, False, None, T, w, 30)
        for band in plan.bands:
            facts = views._band_facts(band, T)
            fw = sum(views.vis(f[0]) for f in facts)
            room = w - fw - 4 - 2
            rooms.setdefault(band.name, {})[w] = room
            print(f"w {w} · {band.name:18} facts {''.join(f[0] for f in facts)!r} = {fw} cells · room {room}")
    print("\n## the height at 118 at which every band is drawn (no fold row)")
    first = views.kanban_nav(views.kanban_plan(b, False, None, T, 118, 30))[0][0]
    for h in range(18, 61):
        txt = views.render_kanban(b, False, first, T, 118, h).plain
        if all(f"▐ {p}" in txt for p in rooms) and "below" not in txt and "above" not in txt:
            print("all bands drawn from height", h)
            break

code = r'''
import json, sys
sys.path.insert(0, ".")
import fixture, variants_round5 as V
rooms = json.loads(sys.argv[1])
mb = V.milestone_board(fixture.build(), fixture.TODAY)
for pr in mb.visible_projects(False):
    items = V._ms_bits(mb, pr, fixture.TODAY)
    for w, room in sorted(rooms.get(pr.name, {}).items()):
        segs, n = V._ms_segment(items, room)
        print(f"w {w} · {pr.name:18} room {room:3}: {''.join(t for t, _ in segs)!r} ({n})")
'''
print("\n## the segments, by the prototype's layout, at the shipped rooms")
r = subprocess.run([sys.executable, "-B", "-c", code, json.dumps(rooms)], cwd=PROTO,
                   capture_output=True, text=True, encoding="utf-8",
                   env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8",
                        "PYTHONDONTWRITEBYTECODE": "1"})
print(r.stdout.rstrip() or r.stderr[-800:])
