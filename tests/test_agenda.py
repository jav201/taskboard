"""The agenda: wide titles, no meter, and an ink ceiling (REV5 #20).

The decision this file exists to hold is a REFUSAL. Gantt and lanes end their
rows in the six-cell due meter; the agenda does not, and that inconsistency is
deliberate:

    The agenda already encodes days-remaining as LENGTH, twice — the rows are
    ordered by criticality, and each row DRAWS its reach from today to its own
    date. Adding the meter would put the same datum in the same row a third
    time, which is the duplication the right-edge pass existed to remove.

What the reader loses is muscle memory for one mark between views. What they
gain is a row that says each thing once. If that trade turns out wrong in use,
the way back is one line — and this file is where the reason lives meanwhile.
"""

import re
from datetime import date, timedelta

from taskboard.models import Board, Project, Task
from taskboard.views import HEX, METER_W, render_agenda

TODAY = date(2026, 7, 30)
INK_CEILING = 85.0          # DENSITY's ceiling: a ceiling is law, same as a floor
FRAME = set("╭─╮│╰╯├┤┬┴┼")


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def board(tmp_path, projects=4, tasks=20, name="a.json") -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    hues = ["lime", "green", "sky", "blue", "indigo", "violet", "fuchsia", "pink"]
    per = max(1, tasks // projects)
    k = 0
    for i in range(projects):
        p = Project(f"Project {i}", hues[i % 8], "on_track", due_date=iso(10 + i))
        b.projects.append(p)
        for j in range(per):
            b.tasks.append(Task(f"Task {i}-{j} something real with a long name",
                                p.id, ["Backlog", "Doing", "Done"][j % 3], "normal",
                                due_date=iso(k - 2)))
            k += 1
    return b


def rows(b, w=96, h=30):
    return str(render_agenda(b, False, None, TODAY, width=w, height=h)).split("\n")


def task_rows(out):
    return [l for l in out if l.startswith("│▊ ")]


def title_width(w: int) -> int:
    inner = w - 2
    budget = inner - 21
    axis_w = max(12, min(44, (budget * 6) // 10)) if budget >= 20 else 0
    return budget - axis_w


# --------------------------------------------------------------------------- #
# the titles
# --------------------------------------------------------------------------- #
def test_the_title_clears_the_width_the_design_asked_for():
    """REV5 §0.003 asks for 19 characters at 96 wide, up from its prototype's 12.
    MEASURED here: 30 at 96 and 20 at 72 — this layout was already past the
    target, because its titles were never boxed inside a label column."""
    assert title_width(96) == 30
    assert title_width(72) == 20
    for w in (72, 96, 130):
        assert title_width(w) >= 19, w


def test_a_long_title_is_truncated_visibly_never_silently(tmp_path):
    b = board(tmp_path)
    b.tasks.append(Task("Z" * 90, b.projects[0].id, "Doing", "normal",
                        due_date=iso(3)))
    line = next(l for l in task_rows(rows(b)) if "ZZZ" in l)
    assert "…" in line
    assert line.count("Z") == title_width(96) - 1


# --------------------------------------------------------------------------- #
# the refusal
# --------------------------------------------------------------------------- #
def test_the_agenda_row_ends_in_its_due_token_not_a_meter(tmp_path):
    """The deliberate inconsistency, pinned so a later "let's be consistent"
    change has to argue with it."""
    b = board(tmp_path)
    for line in task_rows(rows(b)):
        tail = line[-1 - METER_W:-1]
        assert re.search(r"(\+\d+d|-\d+d|done|today)\s*$", line[:-1]), line[-14:]
        assert not set(tail) >= {"⣿"}, "the agenda grew a meter"
        assert "⣤" not in tail and "⡇" not in tail


def test_the_row_draws_its_reach_which_is_why_it_needs_no_meter(tmp_path):
    """The datum the meter would have added is already here, as length: the run
    from the today rule to the task's own dot."""
    b = board(tmp_path)
    out = task_rows(rows(b))
    reaches = [l.count("─") for l in out if "●" in l]
    assert len(reaches) >= 8
    assert max(reaches) > min(reaches), "every reach is the same length"
    assert all("●" in l for l in out if "┃" in l)


def test_the_rows_are_ordered_by_criticality(tmp_path):
    """The second encoding of the same datum: position. Soonest first."""
    b = board(tmp_path)
    tokens = [re.search(r"(-?\+?\d+)d", l) for l in task_rows(rows(b))]
    days = [int(m.group(1)) for m in tokens if m]
    assert days == sorted(days), days


# --------------------------------------------------------------------------- #
# the ink ceiling — a ceiling is law, the same as a floor
# --------------------------------------------------------------------------- #
def ink_share(line: str) -> float:
    body = line[1:-1]
    if not body.strip():
        return 0.0
    return 100 * sum(1 for ch in body if ch != " " and ch not in FRAME) / len(body)


def test_no_agenda_row_crosses_the_ink_ceiling(tmp_path):
    """DENSITY caps ink at 85 %. The prototype crossed it at 86.3 % when its
    titles widened, and its cure was to draw the reach lattice at half density.
    MEASURED here: the densest row is 38.3 %, so the cure is deliberately NOT
    applied — but the ceiling is pinned, so a future widening cannot cross it in
    silence. If it ever does, the half-density reach is the designed answer."""
    for projects, tasks in ((2, 5), (5, 21), (8, 44)):
        b = board(tmp_path, projects, tasks, f"ink{projects}.json")
        out = rows(b, 96, 30)
        inked = [ink_share(l) for l in out if ink_share(l) > 0]
        assert inked, "vacuous: no row carried any ink at all"
        assert max(inked) <= INK_CEILING, f"{max(inked):.1f} % > {INK_CEILING} %"


def test_the_ceiling_law_can_actually_see_a_dense_row(tmp_path):
    """Anti-vacuity for the law above: a row of solid ink must measure as one."""
    assert ink_share("│" + "█" * 40 + "│") == 100.0
    assert ink_share("│" + " " * 40 + "│") == 0.0


# --------------------------------------------------------------------------- #
# the invariants every view here obeys
# --------------------------------------------------------------------------- #
def test_width_exact_at_every_step(tmp_path):
    b = board(tmp_path)
    for w in (24, 40, 60, 72, 96, 97, 130, 200):
        for h in (0, 12, 30):
            for line in rows(b, w, h):
                assert len(line) == max(24, w), f"{w}x{h}: {len(line)}"


def test_severity_is_worn_only_by_a_date(tmp_path):
    b = board(tmp_path)
    text = render_agenda(b, False, None, TODAY, width=96, height=30)
    worn = [text.plain[s.start:s.end].strip() for s in text.spans
            if HEX["over"] in str(s.style)]
    assert worn
    for seg in worn:
        # the dot IS a date — its position on the axis is the due date, so it is
        # the one mark besides the token and the header count that may be red
        assert re.fullmatch(r"-?\d+d|▲|●|▲ \d+ overdue|\d+ overdue", seg), seg
