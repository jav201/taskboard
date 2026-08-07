"""PROBE 2: the FULL panel identity, the shed path, and the C-40 mutations.

Identity under test:
    2 + BODY + ABSENCE == h            (1 header + body + absence + 1 axis + 0 frameless close)
    BODY == CHARGE + 2*[active]
    CHARGE <= ROOM,  ROOM == h - 2 - 2*[active]
    ABSENCE == 1  <=>  ROOM - CHARGE == 1
"""
import tempfile, os, importlib
from datetime import date, timedelta
from collections import Counter

from taskboard.models import Board, Project, Task
from taskboard import views as V

TODAY = date(2026, 7, 30)
iso = lambda n: (TODAY + timedelta(days=n)).isoformat()


def mk(path, spec):
    b = Board.load(path); b.projects.clear(); b.tasks.clear()
    for name, status, dd, tasks in spec:
        p = Project(name, "lime", status, due_date=iso(dd) if dd is not None else None)
        b.projects.append(p)
        for t, ph, d in tasks:
            b.tasks.append(Task(t, p.id, ph, "normal", due_date=iso(d) if d is not None else None))
    b.save(); return b


def boards(d):
    return {
      "typical": mk(os.path.join(d, "t.json"), [
        ("Atlas", "on_track", 20, [("Fix ingest", "Doing", -9), ("Write v2", "Backlog", 6),
                                   ("Ship migration", "Done", -2)]),
        ("Beacon", "on_track", 40, [("Harden index", "Doing", 12)]),
        ("Cinder", "paused", 15, [("Deprecate v1", "Backlog", 3)]),
        ("Delta", "cancelled", -9, [("Retire host", "Backlog", 1)])]),
      "busy": mk(os.path.join(d, "b.json"),
        [(n, "on_track", 20 + i * 5, [(f"{n} t{j}", "Doing" if j % 3 else "Backlog", j - 4)
                                      for j in range(6)])
         for i, n in enumerate(["Atlas", "Beacon", "Cinder", "Dune", "Ember"])]),
      "calm": mk(os.path.join(d, "c.json"), [
        ("Atlas", "on_track", 20, [("One open thing", "Doing", 5)]),
        ("Beacon", "completed", 3, [("Done thing", "Done", -3)])]),
      "allrest": mk(os.path.join(d, "r.json"), [
        ("Atlas", "completed", 20, [("Done a", "Done", -3)]),
        ("Beacon", "cancelled", 3, [("Done b", "Done", -3)])]),
      "huge": mk(os.path.join(d, "h.json"),
        [(n, "on_track", 10 + i, [(f"{n} t{j}", "Doing", j - 10) for j in range(14)])
         for i, n in enumerate(["P%d" % k for k in range(9)])]),
    }


def audit(b, w, h, name, sa=False):
    lanes, geo, titles, prof, wrows = V.swimlane_plan(b, sa, TODAY, w, h)
    active = [ln for ln in lanes if not ln.resting]
    stack = active[1:]
    rest = [ln for ln in lanes if ln.resting]
    nameable = [len(ln.open) + sum(1 for t in ln.tasks if t.archived) for ln in stack]
    A = 1 if active else 0
    room = h - 2 - 2 * A
    charge = prof + sum(wrows + min(titles, o) for o in nameable) + len(rest)

    inner = V._clamp_width(w)
    lead = len(V.lead_band(active[0], geo, TODAY, inner, prof, 0)) if active else 0
    body = lead + sum(len(V.stack_block(ln, geo, b, TODAY, inner, titles, wrows, None, 0))
                      for ln in stack) + len(rest)

    txt = V.render_swimlanes(b, sa, None, TODAY, w, h).plain
    lines = txt.split("\n")
    # the absence line as ACTUALLY DRAWN, not as inferred
    al = V._strip(V.absence_line(lanes, TODAY, inner)).strip()
    absence = 1 if (al and any(al in l for l in lines)) else 0
    # did the allocator find a feasible solution at all?
    feasible = charge <= room
    # did the render actually SHED?
    shed = "not shown" in txt
    return dict(name=name, w=w, h=h, A=A, room=room, charge=charge, body=body,
                lead=lead, prof=prof, titles=titles, wrows=wrows,
                lines=len(lines), absence=absence, shed=shed, feasible=feasible,
                blank=sum(1 for l in lines if not l.strip()),
                slack=room - charge)


def sweep():
    d = tempfile.mkdtemp()
    out = []
    for nm, b in boards(d).items():
        for w in (72, 96, 120, 200):
            for h in (10, 14, 18, 24, 30, 45, 60, 80):
                out.append(audit(b, w, h, nm))
    return out


def report(rows, tag):
    print(f"\n===== {tag} : {len(rows)} renders =====")
    checks = {
        "I1  BODY == CHARGE + 2*A":        lambda r: r["body"] == r["charge"] + 2 * r["A"],
        "I2  CHARGE <= ROOM":              lambda r: r["charge"] <= r["room"],
        "I3  BODY <= h-2":                 lambda r: r["body"] <= r["h"] - 2,
        "I4  lines == h":                  lambda r: r["lines"] == r["h"],
        "I5  0 blank rows":                lambda r: r["blank"] == 0,
        "I6  lead == prof + 2 (if active)": lambda r: r["lead"] == (r["prof"] + 2 if r["A"] else 0),
    }
    for label, fn in checks.items():
        bad = [r for r in rows if not fn(r)]
        print(f"  {label:36s} {'PASS' if not bad else 'FAIL %d/%d' % (len(bad), len(rows))}"
              + ("" if not bad else "  e.g. " + str({k: bad[0][k] for k in
                 ('name','w','h','room','charge','body','lines','prof','slack','shed')})))
    print(f"  slack distribution: {dict(Counter(r['slack'] for r in rows))}")
    print(f"  shed renders: {sum(1 for r in rows if r['shed'])}")
    unshed = [r for r in rows if not r["shed"]]
    print(f"  among UNSHED: 2+body+absence==h : "
          f"{sum(1 for r in unshed if 2 + r['body'] + (1 if r['slack'] >= 1 and r['absence'] else 0) == r['h'])}"
          f"/{len(unshed)}")




def main():
    base = sweep()
    report(base, "ALL RENDERS")
    report([r for r in base if r["A"] and r["feasible"]], "REGIME: active lane + allocator feasible")
    report([r for r in base if not r["A"]], "OFF-REGIME: no active lane")
    report([r for r in base if not r["feasible"]], "OFF-REGIME: allocator infeasible (shed)")

    print("\n===== PANEL IDENTITY  2 + BODY + ABSENCE == h =====")
    for tag, sel in (("in regime", lambda r: r["A"] and r["feasible"]),
                     ("no active", lambda r: not r["A"]),
                     ("infeasible", lambda r: not r["feasible"])):
        rs = [r for r in base if sel(r)]
        ok = sum(1 for r in rs if 2 + r["body"] + r["absence"] == r["h"])
        print(f"  {tag:12s} {ok}/{len(rs)}")

    print("\n===== ABSENCE FIRES  <=>  BODY <= h-3 ? =====")
    rs = [r for r in base if r["A"] and r["feasible"]]
    print(f"  agreement: {sum(1 for r in rs if r['absence'] == (1 if r['body'] <= r['h'] - 3 else 0))}/{len(rs)}")
    print(f"  absence==1 & slack==1: {sum(1 for r in rs if r['absence'] and r['slack'] == 1)}"
          f" | absence==1 total: {sum(1 for r in rs if r['absence'])}"
          f" | slack==1 total: {sum(1 for r in rs if r['slack'] == 1)}")

    print("\n===== A=0 BRANCH: is `prof` charged but undrawn? =====")
    for r in [r for r in base if not r["A"]][:3]:
        print(f"  {r['name']} h={r['h']}: room={r['room']} charge={r['charge']} "
              f"prof={r['prof']} (CHARGED) lead={r['lead']} (DRAWN) body={r['body']} blank={r['blank']}")



if __name__ == "__main__":
    main()
