"""Premise probes for batch 2026-08-06-fastflow-04 (gantt legibility).

Every board here is built IN PROCESS from `Project`/`Task` literals or
`seed_data()`. Nothing reads `~/.taskboard/board.json`.

Run:  python .fast-dev-flow/probes/_probe_premises.py
"""
import sys, os, tempfile, pathlib
from datetime import date, timedelta

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rich.cells import cell_len
from taskboard.models import Board, Project, Task
from taskboard import views
from taskboard.views import render_view, gantt_geometry, FIELD_REACH

TODAY = date(2026, 7, 30)
FRAME = set("╭─╮│╰╯├┤┬┴┼")


def iso(n): return (TODAY + timedelta(days=n)).isoformat()


def mkboard(name, projects, tasks):
    p = pathlib.Path(tempfile.gettempdir()) / f"_probe_{name}.json"
    return Board(projects=projects, tasks=tasks, path=p)


def long_title_board():
    """The operator's reported shape: LONG task titles whose reach starts late."""
    ps = [Project("Machine Learning Platform", "cyan", "on_track",
                  start_date=iso(-20), due_date=iso(40))]
    ts = [Task("Telemetry_Ingestion_Namespace_Migration", ps[0].id, "Doing",
               "normal", start_date=iso(6), due_date=iso(20)),
          Task("Retention_Policy_Rollout_For_Feature_Store", ps[0].id, "Backlog",
               "normal", start_date=iso(10), due_date=iso(30)),
          Task("Short one", ps[0].id, "Doing", "normal",
               start_date=iso(-5), due_date=iso(2))]
    return mkboard("long", ps, ts)


def load(n_proj, n_task, name):
    """test_gantt.py `_load` fixture, reproduced so the census matches."""
    hues = ["lime", "green", "sky", "blue", "indigo", "violet", "fuchsia", "pink"]
    ps, ts, k = [], [], 0
    per = n_task // n_proj
    for i in range(n_proj):
        p = Project(f"Project {i}", hues[i % 8], "on_track",
                    start_date=iso(-20 - i), due_date=iso(6 + i * 5))
        ps.append(p)
        for j in range(per + (1 if i < n_task % n_proj else 0)):
            ts.append(Task(f"Task {i}-{j} something real", p.id,
                           ["Backlog", "Doing", "Done"][j % 3], "normal",
                           start_date=iso(k - 10), due_date=iso(k - 4)))
            k += 1
    return mkboard(name, ps, ts)


def rows(b, w=96, h=30):
    return str(render_view("gantt", b, False, None, TODAY, w, h)).split("\n")


def census(lines):
    ink = chrome = field = dead = 0
    for line in lines:
        for ch in line:
            if ch == " ":
                dead += 1
            elif ch in FRAME:
                chrome += 1
            elif ch == "·":
                field += 1
            else:
                ink += 1
    n = ink + chrome + field + dead
    return {"marked": 100 * (ink + field) / n, "ink": 100 * ink / n,
            "dead": 100 * dead / n, "chrome": 100 * chrome / n}


BARS = set("█▓▒▌▃▅▆▇━◆▬")


def collisions(lines):
    """Rows where a title glyph directly abuts the first bar glyph."""
    out = []
    for i, r in enumerate(lines):
        for j, ch in enumerate(r):
            if ch in BARS:
                prev = r[j - 1] if j else " "
                if prev not in (" ", "·", "┆"):
                    out.append((i, prev, ch, r.strip()[:60]))
                break
    return out


# --------------------------------------------------------------------------- #
print("=" * 78)
print("P1 — geometry at the sizes the laws sweep")
print("=" * 78)
for w, h in [(68, 24), (96, 24), (96, 30), (104, 30), (102, 16), (120, 40), (94, 30)]:
    g = gantt_geometry(w, h)
    tot = g.label_w + g.field_w + 1 + g.figs_w
    print(f"  {w}x{h}: label_w={g.label_w:3d} field_w={g.field_w:3d} figs_w={g.figs_w:3d} "
          f"today_dc={g.today_dc:3d} dot_w={g.dot_w:3d} large={g.large} sum={tot} (inner={w})")

print()
print("=" * 78)
print("P2 — THE COLLISION, reproduced (long titles, reach starting late)")
print("=" * 78)
b = long_title_board()
for w, h in [(104, 30), (102, 16)]:
    ls = rows(b, w, h)
    print(f"\n  -- {w}x{h} --")
    for r in ls[:8]:
        print(f"    |{r}|")
    col = collisions(ls)
    print(f"    collisions: {len(col)}")
    for c_ in col:
        print(f"      row {c_[0]}: {c_[1]!r} abuts {c_[2]!r}  <- {c_[3]!r}")

print()
print("=" * 78)
print("P3 — census laws, EXECUTED (test_gantt.py:248/249/258, test_spend.py:203)")
print("=" * 78)
for label, (np_, nt_) in [("typical(5/21)", (5, 21)), ("extreme(8/44)", (8, 44))]:
    cen = census(rows(load(np_, nt_, label), 96, 30))
    print(f"  {label:14s} marked={cen['marked']:5.1f}  ink={cen['ink']:5.1f}  "
          f"dead={cen['dead']:5.1f}  chrome={cen['chrome']:5.1f}")
print("  laws: marked>=68.0  dead<=25.0  chrome<10.0  (test_gantt)")
print("        extreme.ink > typical.ink                (test_gantt:238)")
print("        gantt dead<=30.0 on test_spend fixture   (test_spend:203)")

print()
print("=" * 78)
print("P4 — the hard-pinned title widths (test_gantt.py:164 == (27, 30))")
print("=" * 78)
ps = [Project("Atlas", "lime", "on_track", start_date=iso(-20), due_date=iso(25))]
ts = [Task("A" * 60, ps[0].id, "Doing", "normal", start_date=iso(9), due_date=iso(16)),
      Task("B" * 60, ps[0].id, "Doing", "normal", start_date=iso(-6), due_date=iso(-2))]
ls = rows(mkboard("pin", ps, ts), 96, 20)
near = next((l for l in ls if "B" in l), "")
far = next((l for l in ls if "A" in l), "")
print(f"  near.count('B')+1 = {near.count('B') + 1}")
print(f"  far.count('A')+1  = {far.count('A') + 1}")
print(f"  near |{near}|")
print(f"  far  |{far}|")

print()
print("=" * 78)
print("P5 — week/month boundaries in the window (the guide the view lacks)")
print("=" * 78)
for w, h in [(96, 30), (104, 30), (120, 40)]:
    g = gantt_geometry(w, h)
    lo, hi = -g.today_dc, g.dot_w - 1 - g.today_dc
    weeks = [d for d in range(lo, hi + 1)
             if (TODAY + timedelta(days=d)).weekday() == 0]
    months = [d for d in range(lo, hi + 1) if (TODAY + timedelta(days=d)).day == 1]
    wcells = sorted({(g.today_dc + d) // 2 for d in weeks})
    mcells = sorted({(g.today_dc + d) // 2 for d in months})
    print(f"  {w}x{h}: window {lo}..{hi} d ({hi - lo + 1} days), field_w={g.field_w}")
    print(f"      week guides : {len(wcells)} cells, every ~{g.field_w / max(1, len(wcells)):.1f} cells")
    print(f"      month starts: {len(mcells)} at cells {mcells} -> "
          f"{[(TODAY + timedelta(days=d)).strftime('%b').upper() for d in months]}")
    print(f"      today cell = {g.today_dc // 2}; week cell collides with today? "
          f"{g.today_dc // 2 in wcells}")

print()
print("=" * 78)
print("P6 — the today column law (test_app.py:1557)")
print("=" * 78)
g = gantt_geometry(94, 30)
print(f"  gantt_geometry(94,30): label_w={g.label_w} today_dc={g.today_dc} "
      f"-> guarded col = {g.label_w + g.today_dc // 2}")
print(f"  FIELD_REACH is currently {FIELD_REACH!r}")

print()
print("=" * 78)
print("P7 — is '━' free? (agenda swatches must not contain the new FIELD_REACH)")
print("=" * 78)
from taskboard.views import legend_entries, _strip
bb = load(3, 9, "leg")
for mode in ("gantt", "agenda", "swimlanes"):
    sw = [_strip(s) for s, _ in legend_entries(mode, bb, TODAY, 120, 40)]
    print(f"  {mode:10s}: {sw}")
    print(f"      '━' present? {any('━' in s for s in sw)}   "
          f"'┆' present? {any('┆' in s for s in sw)}")
