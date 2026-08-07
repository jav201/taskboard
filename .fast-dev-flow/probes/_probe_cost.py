"""PROBE: the lanes row cost model, measured at the WRITERS (C-15.1).

Deterministic: fixed TODAY, boards built in-process, never reads a real board.
"""
import sys, tempfile, os
from datetime import date, timedelta

from taskboard.models import Board, Project, Task
from taskboard import views as V

TODAY = date(2026, 7, 30)


def iso(n):
    return (TODAY + timedelta(days=n)).isoformat()


def mk(path, spec):
    """spec: list of (project_name, status, due_offset, [(title, phase, due_off)])"""
    b = Board.load(path)
    b.projects.clear(); b.tasks.clear()
    for name, status, dd, tasks in spec:
        p = Project(name, "lime", status, due_date=iso(dd) if dd is not None else None)
        b.projects.append(p)
        for t, ph, d in tasks:
            b.tasks.append(Task(t, p.id, ph, "normal",
                                due_date=iso(d) if d is not None else None))
    b.save()
    return b


def typical(path):
    return mk(path, [
        ("Atlas", "on_track", 20, [("Fix the ingest path", "Doing", -9),
                                   ("Write the v2 reference", "Backlog", 6),
                                   ("Ship the migration", "Done", -2)]),
        ("Beacon", "on_track", 40, [("Harden the search index", "Doing", 12)]),
        ("Cinder", "paused", 15, [("Deprecate v1 endpoints", "Backlog", 3)]),
        ("Delta", "cancelled", -9, [("Retire the old host", "Backlog", 1)]),
    ])


def busy(path):
    spec = []
    for pi, pname in enumerate(["Atlas", "Beacon", "Cinder", "Dune", "Ember"]):
        tasks = [(f"{pname} task {i}", "Doing" if i % 3 else "Backlog", i - 4)
                 for i in range(6)]
        spec.append((pname, "on_track", 20 + pi * 5, tasks))
    return mk(path, spec)


def calm(path):
    return mk(path, [("Atlas", "on_track", 20, [("One open thing", "Doing", 5)]),
                     ("Beacon", "completed", 3, [("Done thing", "Done", -3)])])


def measure(b, w, h, label, show_archived=False):
    """Recompute the allocator's charge and the renderer's actual spend."""
    lanes, geo, titles, prof, wrows = V.swimlane_plan(b, show_archived, TODAY, w, h)
    active = [ln for ln in lanes if not ln.resting]
    resting = [ln for ln in lanes if ln.resting]
    stack = active[1:]
    nameable = [len(ln.open) + sum(1 for t in ln.tasks if t.archived) for ln in stack]
    n_rest = len(resting)
    room = h - 2 - (2 if active else 0)
    charged = prof + sum(wrows + min(titles, o) for o in nameable) + n_rest

    inner = V._clamp_width(w)
    drawn_lead = len(V.lead_band(active[0], geo, TODAY, inner, prof, 0)) if active else 0
    drawn_stack = [len(V.stack_block(ln, geo, b, TODAY, inner, titles, wrows, None, 0))
                   for ln in stack]
    drawn_rest = n_rest
    drawn_body = drawn_lead + sum(drawn_stack) + drawn_rest

    out = V.render_swimlanes(b, show_archived, None, TODAY, w, h)
    lines = out.plain.split("\n")
    blank = sum(1 for ln in lines if not ln.strip())

    print(f"{label:10s} w={w:4d} h={h:3d} | room={room:4d} charged={charged:4d} "
          f"| lead={drawn_lead:3d} (prof={prof}) stack={sum(drawn_stack):3d} "
          f"rest={drawn_rest:2d} body={drawn_body:4d} "
          f"| charged+2a={charged + (2 if active else 0):4d} "
          f"MATCH={'OK ' if drawn_body == charged + (2 if active else 0) else 'NO!'} "
          f"| room-charged={room - charged:3d} "
          f"| lines={len(lines):3d} h={h} blank={blank} "
          f"| titles={titles} wrows={wrows}")
    return dict(room=room, charged=charged, body=drawn_body, lines=len(lines),
                blank=blank, prof=prof, lead=drawn_lead, h=h)


def main():
    d = tempfile.mkdtemp()
    boards = {"typical": typical(os.path.join(d, "t.json")),
              "busy": busy(os.path.join(d, "b.json")),
              "calm": calm(os.path.join(d, "c.json"))}
    print("=== P1: charge vs draw, and panel fit ===")
    rows = []
    for name, b in boards.items():
        for w in (72, 96, 120):
            for h in (24, 30, 45, 60):
                rows.append(measure(b, w, h, name))
    print()
    print("=== P2: does the body ever exceed the shed budget h-2? ===")
    bad = [r for r in rows if r["body"] > r["h"] - 2]
    print(f"body > h-2 : {len(bad)} of {len(rows)}")
    print("=== P3: does the rendered panel ever differ from h? ===")
    off = [(r['lines'], r['h']) for r in rows if r["lines"] != r["h"]]
    print(f"lines != h : {len(off)} of {len(rows)}   samples={off[:5]}")
    print("=== P4: blank rows (the never-pads law) ===")
    print(f"total blank rows across {len(rows)} renders: {sum(r['blank'] for r in rows)}")
    print("=== P5: charge == draw - 2*active, universally? ===")
    print(f"mismatches: {sum(1 for r in rows if r['body'] != r['charged'] + 2)}")
    print("=== P6: slack (room - charged) distribution ===")
    from collections import Counter
    print(Counter(r["room"] - r["charged"] for r in rows))
    print("=== P7: lead_band arity across prof ===")
    b = boards["typical"]
    lanes, geo, titles, prof, wrows = V.swimlane_plan(b, False, TODAY, 96, 30)
    active = [ln for ln in lanes if not ln.resting]
    for p in (3, 5, 8, 12, 19, 33):
        print(f"  prof={p:3d} -> len(lead_band)={len(V.lead_band(active[0], geo, TODAY, 94, p, 0))}")


main()
