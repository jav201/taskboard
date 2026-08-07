"""P2 redone + P4 fixed + span-economy baseline.

The operator's shape is a LONG title on a task whose reach starts a few cells LEFT of
today: `over` is then the reach start (not the today cap), so the title runs
right up to the first bar cell with nothing between them.

Boards built in process. Nothing reads ~/.taskboard/board.json.
"""
import sys, os, tempfile, pathlib
from datetime import date, timedelta

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rich.text import Text
from taskboard.models import Board, Project, Task
import taskboard.views as V
from taskboard.views import render_view, gantt_geometry, collapse_runs, _reach_start

TODAY = date(2026, 7, 30)
BARS = set("█▓▒▌▃▅▆▇━◆▬")


def iso(n): return (TODAY + timedelta(days=n)).isoformat()


def mkboard(name, projects, tasks):
    return Board(projects=projects, tasks=tasks,
                 path=pathlib.Path(tempfile.gettempdir()) / f"_pc_{name}.json")


def rows(b, w, h):
    return str(render_view("gantt", b, False, None, TODAY, w, h)).split("\n")


def collisions(lines):
    out = []
    for i, r in enumerate(lines):
        for j, ch in enumerate(r):
            if ch in BARS:
                prev = r[j - 1] if j else " "
                if prev not in (" ", "·", "┆"):
                    out.append((i, prev, ch))
                break
    return out


print("=" * 78)
print("P2' — THE COLLISION: long title, reach STARTING BEFORE TODAY")
print("=" * 78)
ps = [Project("Machine Learning Platform", "cyan", "on_track",
              start_date=iso(-30), due_date=iso(40))]
ts = []
for k, off in enumerate((-4, -8, -12, -20, -2)):
    ts.append(Task(f"Telemetry_Ingestion_Namespace_Migration_{k}", ps[0].id,
                   "Doing", "normal",
                   start_date=iso(off), due_date=iso(off + 6)))
b = mkboard("coll", ps, ts)

for w, h in [(104, 30), (102, 16), (96, 30), (120, 40)]:
    ls = rows(b, w, h)
    g = gantt_geometry(w, h)
    col = collisions(ls)
    print(f"\n  -- {w}x{h}  (label_w={g.label_w}, today_cell={g.today_dc // 2}) --")
    for r in ls[1:7]:
        print(f"    |{r}|")
    print(f"    COLLISIONS: {len(col)}  {col}")
    print("    per-task `over` (title cells stolen from the field):")
    for t in ts:
        rs = _reach_start(t, g, TODAY)
        over = max(0, min(rs, g.today_dc // 2))
        print(f"       reach_start={rs:3d}  over={over:3d}  title_w={g.label_w - 3 + over:3d}"
              f"   <- bar begins at field cell {over}, title ends at field cell {over}")

print()
print("=" * 78)
print("P4' — test_gantt.py:164 pinned widths, matched properly")
print("=" * 78)
ps = [Project("Atlas", "lime", "on_track", start_date=iso(-20), due_date=iso(25))]
ts = [Task("A" * 60, ps[0].id, "Doing", "normal", start_date=iso(9), due_date=iso(16)),
      Task("B" * 60, ps[0].id, "Doing", "normal", start_date=iso(-6), due_date=iso(-2))]
ls = rows(mkboard("pin", ps, ts), 96, 20)
near = max(ls, key=lambda l: l.count("B"))
far = max(ls, key=lambda l: l.count("A"))
print(f"  near.count('B')+1 = {near.count('B') + 1}   (test expects 27)")
print(f"  far.count('A')+1  = {far.count('A') + 1}   (test expects 30)")
print(f"  near |{near}|")
print(f"  far  |{far}|")
print(f"  collisions on this board: {collisions(ls)}")

print()
print("=" * 78)
print("P8 — span-economy baseline, gantt @120x40 (test_span_economy.py:125)")
print("=" * 78)


def board_with_tasks():
    """test_span_economy's fixture, near enough: 3 projects x 4 phases + undated."""
    hues = ["cyan", "pink", "lime"]
    ps, ts = [], []
    for i, hue in enumerate(hues):
        p = Project(f"P{i}", hue, "on_track", start_date=iso(-15), due_date=iso(20 + i * 5))
        ps.append(p)
        for j, ph in enumerate(["Backlog", "Doing", "Review", "Done"]):
            ts.append(Task(f"task {i}{j}", p.id, ph, "normal",
                           start_date=iso(j * 3 - 6), due_date=iso(j * 4 + 2)))
        ts.append(Task(f"undated {i}", p.id, "Backlog", "normal"))
    return mkboard("span", ps, ts)


sink = []
real = V.collapse_runs
V.collapse_runs = lambda m: (sink.append(m), real(m))[1]
try:
    V.render_view("gantt", board_with_tasks(), False, None, width=120, height=40,
                  line_map={}, presentation="grouped", tick=3)
finally:
    V.collapse_runs = real
before = sink[0]
after = real(before)
nb = len(Text.from_markup(before).spans)
na = len(Text.from_markup(after).spans)
print(f"  runs before={nb}  after={na}  ceiling=before/3={nb / 3:.1f}  "
      f"holds={na < nb / 3}")
print(f"  headroom: after may grow to {nb / 3:.1f} before the law reddens "
      f"(x{(nb / 3) / max(1, na):.2f})")
