"""P2 iteration-2 architect probe — execute the C-3 toast ladder on the exact AT
boards and check the contract's pinned toast literals against what the ladder
actually yields (the contract claims the ladder is adopted verbatim).

    PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-06-batch-01/evidence/p2_arch_probe.py
"""
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")   # S-14: a stock cp1252 console dies on ▌/◆

ROOT = Path(r"C:\Users\jjgh8\Github\taskboard")
PROTO = ROOT / ".claude" / "worktrees" / "kg-mejoras" / "prototypes" / "kg_mejoras"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(PROTO))

import kg_board
import cascade as C
from taskboard.views import _strip, c, fit, vis

TODAY = date.today()


def md(d):  # variants_round5.py:46, verbatim
    return f"{d:%b} {d.day}"


def _short_title(t: str, n: int) -> str:  # variants_cascade.py:386-393, verbatim
    words = t.split()
    out = words[0]
    for w_ in words[1:]:
        if len(out) + 1 + len(w_) > n:
            break
        out += " " + w_
    return out


VERB = {"flag": "flagged", "push_delta": "pushed", "together": "moved", "push": "pushed"}  # :396


class VC:  # namespace shim so the verbatim closure body reads the same
    _short_title = staticmethod(_short_title)
    VERB = VERB


def board():
    b = kg_board.milestones(kg_board.shifted(Path(tempfile.mkdtemp()) / "board.json"), TODAY)
    for t in b.tasks:
        if t.milestone:
            t.extra["milestone"] = True
    return b


def toast_row(b, tid, sd, dd, mode, width):
    """The render_c3 toast closure, verbatim from variants_cascade.py:421-457,
    minus the kanban render (the toast row is what the contract pins)."""
    p = C.plan_move(b, tid, sd, dd, mode, TODAY)
    me = b.task_by_id(tid)
    pr = b.project_by_id(me.project_id)
    deps = sorted((t for t in p.moved if t != tid), key=lambda t: p.moved[t][1])
    nd = p.moved[tid][1]
    over = p.project_over.get(pr.id, 0)
    shifts = {p.shift[t] for t in deps}

    def toast(title_w, names_w, proj_full, keys):
        title = me.title if title_w is None else fit(me.title, title_w).rstrip()
        lead = c("▌", "soon") + c(f"{title} due {md(nd)} (+{dd}d)", "bright", bold=True)
        n = len(deps)
        if names_w and len(shifts) == 1 and not proj_full:
            names = ", ".join(VC._short_title(b.task_by_id(t).title, names_w) for t in deps)
            mid = f"{VC.VERB[mode]} {names} +{next(iter(shifts))}d each"
        elif names_w:
            names = ", ".join(f"{VC._short_title(b.task_by_id(t).title, names_w)} +{p.shift[t]}d"
                              for t in deps)
            mid = f"{VC.VERB[mode]} {n} dependents ({names})"
        elif len(shifts) == 1:
            mid = f"{VC.VERB[mode]} {n}{' dependents' if proj_full else ''} +{next(iter(shifts))}d each"
        else:
            mid = f"{VC.VERB[mode]} {n} (" + "/".join(f"+{p.shift[t]}d" for t in deps) + ")"
        segs = [lead, c(mid, "soon")]
        if over:
            pn = pr.name if proj_full else pr.name.split()[0]
            segs.append(c(f"{pn} +{over}d past ◆", "over", bold=True))
        ks = [("u", "undo"), ("m", ("change for this move", "change", "")[keys])]
        segs.append(c(" · ", "dim").join(c(k, "accent", bold=True) + (" " + c(v, "mut") if v else "")
                                         for k, v in ks))
        return c(" · ", "dim").join(segs)

    ladder = [(None, 12, True, 0), (None, 12, False, 0), (None, 12, False, 1),
              (None, 8, False, 1), (None, 0, True, 0), (None, 0, True, 1), (None, 0, False, 1),
              (12, 0, False, 1), (6, 0, False, 2)]
    t_row = next((tr for args in ladder if vis(_strip(tr := toast(*args))) <= width),
                 toast(*ladder[-1]))
    if vis(_strip(t_row)) > width:
        t_row = c(fit(_strip(t_row), width), "soon")
    return _strip(t_row), ladder.index(next(a for a in ladder
                                            if vis(_strip(toast(*a))) <= width)) if any(
        vis(_strip(toast(*a))) <= width for a in ladder) else len(ladder) - 1


ARMS = [
    ("AT-607 push_delta tm2 +1", board(), "tm2", 0, 1, "push_delta"),
    ("AT-608 together tm2 +1", board(), "tm2", 0, 1, "together"),
    ("AT-610 together td4 +2", None, "td4", 2, 2, "together"),
    ("AT-610 flag td4 +2", board(), "td4", 2, 2, "flag"),
]
b610 = board()
b610.project_by_id("pdwh").extra["date_links"] = "together"
ARMS[2] = ("AT-610 together td4 +2", b610, "td4", 2, 2, "together")

for title, b, tid, sd, dd, mode in ARMS:
    for width in (118, 80):
        try:
            row, rung = toast_row(b, tid, sd, dd, mode, width)
            print(f"{title} @{width} (rung {rung}): {row!r}  [w={vis(row)}]")
        except Exception as e:
            print(f"{title} @{width}: RAISED {type(e).__name__}: {e}")
    print()

print("--- substring checks the contract pins (iteration-3 literals) ---")
checks = [
    ("AT-607@118 holds 'pushed Add push, Offline sync +1d each'",
     toast_row(board(), "tm2", 0, 1, "push_delta", 118)[0],
     "pushed Add push, Offline sync +1d each"),
    ("AT-607@80 holds 'pushed 2 +1d each'",
     toast_row(board(), "tm2", 0, 1, "push_delta", 80)[0], "pushed 2 +1d each"),
    ("AT-608@118 holds 'Mobile +1d past ◆'",
     toast_row(board(), "tm2", 0, 1, "together", 118)[0], "Mobile +1d past ◆"),
    ("AT-610@118 holds 'Data +2d past ◆'",
     toast_row(b610, "td4", 2, 2, "together", 118)[0], "Data +2d past ◆"),
]
for label, row, needle in checks:
    print(("PASS " if needle in row else "FAIL ") + label)
print()
print("probe done")
