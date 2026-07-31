"""The spend ladder — what the reclaimed cells buy, and in what order.

Removing the frame handed back ~7.6 % of every render and almost all of it became
BLANK. This is the rule that spends it, and the rule came out of counting what
each state still had left to say:

    1. NAME while anything is unnamed — a task the reader cannot see is the most
       expensive absence on the screen.
    2. RESOLVE once naming is exhausted — more field rows draw the same datum at
       higher resolution.
    3. SAY WHAT IS NOT THERE when both are spent.

With a hard prohibition: **the field may not grow while a task is still
unnamed.** Buying resolution with titles starving is decoration paid for with
information the reader never gets to read.

And the finding that made the ladder work: applying it first made `typical`
WORSE, because a title row was nearly blank while a field row is lattice — so
trading field rows for title rows raised dead space. The cure is that a named row
carries the field behind it, which also turns the today boundary into one
continuous vertical line down the whole panel.
"""

import re
from datetime import date, timedelta

from taskboard.models import Board, Project, Task
from taskboard.views import (RULE_PHASES, absence_line, allocate, lane_geometry,
                             lanes_of, render_view)

TODAY = date(2026, 7, 30)
FRAME = set("╭─╮│╰╯├┤┬┴┼")


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def load(tmp_path, projects: int, tasks: int, name: str) -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    hues = ["lime", "green", "sky", "blue", "indigo", "violet", "fuchsia", "pink"]
    per, k = max(1, tasks // projects), 0
    for i in range(projects):
        p = Project(f"Project {i}", hues[i % 8], "on_track",
                    start_date=iso(-20), due_date=iso(6 + i * 5))
        b.projects.append(p)
        for j in range(per):
            b.tasks.append(Task(f"Task {i}-{j} something real", p.id,
                                ["Backlog", "Doing", "Done"][j % 3],
                                "high" if j == 0 else "normal",
                                due_date=iso(k % 30 - 4)))
            k += 1
    return b


def rows(b, mode="swimlanes", w=96, h=30):
    return str(render_view(mode, b, False, None, TODAY, width=w, height=h)).split("\n")


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
    return {"marked": 100 * (ink + field) / n, "dead": 100 * dead / n}


# --------------------------------------------------------------------------- #
# 1 — the prohibition
# --------------------------------------------------------------------------- #
def test_the_field_never_grows_while_a_task_is_unnamed():
    """THE PROHIBITION, checked over the whole allocator space rather than one
    board: for every room and every shape of open-work, if the chosen `titles`
    leaves any task unnamed then `wrows` must still be 1."""
    geo = lane_geometry(96, 30)
    checked = 0
    for room in range(4, 40):
        for opens in ([1], [3, 3], [8], [12, 9, 7], [2, 2, 2, 2, 2], [30, 1]):
            titles, prof, wrows = allocate(geo, opens, 0, room)
            unnamed = sum(max(0, o - titles) for o in opens)
            assert not (wrows > 1 and unnamed > 0), (
                f"room={room} opens={opens}: field grew to {wrows} rows while "
                f"{unnamed} task(s) went unnamed")
            checked += 1
    assert checked > 100


def test_when_naming_is_exhausted_the_cells_buy_resolution():
    """The ladder's second rung is real, not just the absence of the first: with
    little to name and room to spare, the allocator DOES take the extra field."""
    geo = lane_geometry(96, 30)
    titles, prof, wrows = allocate(geo, [2, 1], 0, 30)
    assert titles >= 2                      # everything nameable is named
    assert prof > geo.profile_rows          # and the lead's bench grew


# --------------------------------------------------------------------------- #
# 2 — the cure: a named row carries the field
# --------------------------------------------------------------------------- #
def title_rows(out):
    return [l for l in out if l.startswith("▎  ") and "·" in l]


def test_a_named_row_carries_the_lattice_behind_it(tmp_path):
    """The cure for "naming cost emptiness". Without it a title row is a short
    string and a lot of blank; with it the row is field."""
    out = rows(load(tmp_path, 5, 21, "cure.json"))
    named = title_rows(out)
    assert named, "no named task rows drawn at all"
    for line in named:
        assert line.count("·") > 20, line


def test_the_today_rule_is_one_unbroken_vertical_line(tmp_path):
    """THE ACCEPTANCE SIGN, and it was a gift rather than a request: because
    every row now carries the field, the today boundary runs the full height of
    the panel instead of appearing only on rows that draw a wave."""
    b = load(tmp_path, 5, 21, "rule.json")
    geo = lane_geometry(96, 30)
    col = geo.label_w + geo.today_dc // 2
    out = rows(b)
    body = [l for l in out if l.startswith("▎") or l.startswith("▌")]
    assert len(body) >= 8
    marks = [l[col] for l in body if len(l) > col]
    unbroken = [m for m in marks if m in RULE_PHASES or 0x2800 <= ord(m) <= 0x28FF]
    assert len(unbroken) == len(marks), [m for m in marks if m not in unbroken]
    assert sum(1 for m in marks if m in RULE_PHASES) >= len(marks) // 2


# --------------------------------------------------------------------------- #
# 3 — the line that says what is not there
# --------------------------------------------------------------------------- #
def test_the_absence_line_states_facts_about_the_board(tmp_path):
    b = load(tmp_path, 2, 4, "calm.json")
    line = absence_line(lanes_of(b, False, TODAY), TODAY, 94)
    assert "2 projects" in line
    assert "nothing late" in line or "late" in line


def test_a_quiet_board_says_what_it_does_not_have(tmp_path):
    """A calm board is not an empty screen — it is a board with little to
    report, and the closing line states the difference."""
    b = load(tmp_path, 2, 3, "quiet.json")
    for t in b.tasks:
        t.due_date = iso(40)                       # nothing late, nothing this week
    out = "\n".join(rows(b, "swimlanes", 96, 24))
    assert "nothing late" in out
    assert "nothing due this week" in out


def test_the_absence_line_never_addresses_the_reader(tmp_path):
    b = load(tmp_path, 3, 6, "reg.json")
    line = absence_line(lanes_of(b, False, TODAY), TODAY, 94)
    assert not re.search(r"\b(you|your|we|our)\b", line, re.I)
    for flattery in ("great", "good job", "well done", "keep it up"):
        assert flattery not in line.lower()


def test_the_absence_line_yields_when_rows_were_shed(tmp_path):
    """It is the ladder's THIRD rung: it may not appear while the first is still
    unpaid. If work did not fit, the count of what is missing takes the row."""
    b = load(tmp_path, 8, 44, "shed.json")
    out = "\n".join(rows(b, "swimlanes", 96, 12))
    assert "not shown" in out
    # Look for the LINE's signature, not for one of its clauses. This board HAS
    # late work, so the line would read "12 late" — and a "nothing late" check
    # passes whether or not the line is there. That version was vacuous, and its
    # mutant proved it.
    assert not re.search(r"\d+ projects? ·", out), out


# --------------------------------------------------------------------------- #
# 4 — the measurements this increment is accepted on
# --------------------------------------------------------------------------- #
def test_typical_empty_is_at_or_under_the_ceiling(tmp_path):
    """REV6's acceptance: dead <= 25 % at typical. Measured here: 23.4 %."""
    dead = census(rows(load(tmp_path, 5, 21, "t.json")))["dead"]
    assert dead <= 25.0, dead


def test_ink_stays_monotone_at_extreme(tmp_path):
    """REV6 reported its own violation here — extreme landed 0.5 points BELOW
    typical in marked cells, which is the inversion the whole gantt redesign
    existed to kill. Checked on this implementation: extreme is ABOVE typical,
    so more data still means more marked screen."""
    typical = census(rows(load(tmp_path, 5, 21, "mt.json")))["marked"]
    extreme = census(rows(load(tmp_path, 8, 44, "me.json")))["marked"]
    assert extreme >= typical, (typical, extreme)


def test_the_gantt_spends_its_cells_too(tmp_path):
    b = load(tmp_path, 5, 21, "g.json")
    assert census(rows(b, "gantt"))["dead"] <= 30.0
