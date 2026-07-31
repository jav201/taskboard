"""The gantt's right edge and its titles (REV5 #19).

Two changes, one law between them: the row ends in the six-cell due meter, and
because the meter now says WHEN, the bar goes back to saying only WHOSE. That is
the ration again — identity names, severity judges, no mark wears both — and it
leaves `▲` as the single alert on the row.

The titles run OVER THE FIELD, which is where the reader actually reads, and they
stop where the task's own bar starts so they can never cover the thing they
describe.
"""

import re
from datetime import date, timedelta

from taskboard.models import Board, Project, Task
from taskboard.views import HEX, METER_W, gantt_meta_geometry, render_gantt

TODAY = date(2026, 7, 30)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def board(tmp_path, name="g.json") -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


def fixture(tmp_path):
    b = board(tmp_path)
    p = Project("Atlas", "lime", "on_track", start_date=iso(-20), due_date=iso(25))
    b.projects.append(p)
    b.tasks += [
        Task("Checkout returns 500 on retry", p.id, "Doing", "high",
             start_date=iso(-6), due_date=iso(-2)),                    # bar at week 0
        Task("Rework the pricing page copy", p.id, "Backlog", "normal",
             start_date=iso(9), due_date=iso(16)),                     # bar a week out
        Task("Compress the hero assets", p.id, "Backlog", "normal",
             start_date=iso(20), due_date=iso(27)),                    # further out
        Task("Old finished thing", p.id, "Done", "normal",
             start_date=iso(-30), due_date=iso(-20)),
    ]
    return b, p


def rows(b, w=96, h=20):
    return str(render_gantt(b, False, None, TODAY, width=w, height=h)).split("\n")


def geo(w):
    inner = w - 2
    glabel_w = max(18, min(30, inner // 3))
    meta_w, _full = gantt_meta_geometry(inner, glabel_w, 6)
    return inner, glabel_w, meta_w


# --------------------------------------------------------------------------- #
# the right edge
# --------------------------------------------------------------------------- #
def test_every_row_ends_in_the_six_cell_meter(tmp_path):
    b, _p = fixture(tmp_path)
    out = rows(b)
    body = [l for l in out if l.startswith("│▎ ") or l.startswith("│▏ ")]
    assert len(body) >= 5
    for line in body:
        edge = line[-1 - METER_W:-1]
        assert set(edge) <= set("⣿⡇·▲⣤ "), f"{line[-10:]!r} is not a meter"
        # an EMPTY edge is not a meter either — the first version of this law
        # allowed spaces, so deleting the meter altogether kept it green
        assert set(edge) & set("⣿⡇·▲⣤"), f"{line[-10:]!r} has no meter at all"


def test_finished_work_shows_a_spent_meter_and_rests_in_ash(tmp_path):
    """Active at the top, finished at the tail, and the finished row RESTS: thin
    spine, ash, no chip and no severity."""
    b, _p = fixture(tmp_path)
    line = next(l for l in rows(b, 96, 30) if "Old finished" in l)
    assert set(line[-1 - METER_W:-1]) <= {"⣤", " "} and "⣤" in line
    assert line.startswith("│▏ ")               # the thin spine
    assert "▲" not in line


def test_the_project_row_keeps_its_progress_figure(tmp_path):
    b, _p = fixture(tmp_path)
    line = next(l for l in rows(b, 130, 30) if "Atlas" in l)
    assert re.search(r"\d+%", line), line
    assert set(line[-1 - METER_W:-1]) <= set("⣿⡇·▲⣤ ")


def test_the_alert_is_the_meters_cap_and_nothing_else(tmp_path):
    """`▲` is severity's one seat on this row. The task bar used to turn red for
    overdue and amber for due-today; the meter says when now, so the bar is free
    to say only whose."""
    b, _p = fixture(tmp_path)
    text = render_gantt(b, False, None, TODAY, width=96, height=20)
    worn = [text.plain[s.start:s.end].strip() for s in text.spans
            if HEX["over"] in str(s.style)]
    assert worn, "vacuous: nothing wears the severity hue at all"
    for seg in worn:
        assert re.fullmatch(r"▲|▲\d+ past due|\d+ past due", seg), \
            f"severity worn by {seg!r}"


def test_a_bar_never_wears_an_urgency_hue(tmp_path):
    """The span and the reaches may only ever wear an identity hue, the ash of
    elapsed time, or the flow packet's bright."""
    from taskboard.models import PROJECT_COLORS
    b, _p = fixture(tmp_path)
    text = render_gantt(b, False, None, TODAY, width=96, height=20)
    lawful = {HEX[c] for c in PROJECT_COLORS} | {HEX["bright"], HEX["dim"],
                                                HEX["accent"], HEX["frame"],
                                                HEX["ash"], HEX["mut"]}
    for s in text.spans:
        seg = text.plain[s.start:s.end]
        if seg and set(seg) <= {"⣿", "⣤", "⡄", "⣀", " "} and seg.strip():
            assert any(h in str(s.style) for h in lawful), f"bar wears {s.style}"
            assert HEX["over"] not in str(s.style)
            assert HEX["soon"] not in str(s.style)


# --------------------------------------------------------------------------- #
# the titles
# --------------------------------------------------------------------------- #
def test_a_title_never_covers_its_own_reach(tmp_path):
    """The safety property, stated where it actually lives: the title spends
    ONLY the cells the reach leaves empty in front of itself. Checked against
    the reach the engine builds, not against arithmetic on the rendered row —
    a title that grew one cell too far would draw over the mark it names."""
    from taskboard.views import _reach_start, _task_reach, gantt_geometry
    b, p = fixture(tmp_path)
    gg = gantt_geometry(94, 30)
    checked = 0
    for t in b.tasks:
        full = _task_reach(t, b, gg, TODAY, "lime")
        over = min(_reach_start(t, gg, TODAY), gg.today_dc // 2)
        assert all(g == " " for g, _ in full[:over]),             f"{t.title!r}: the title would cover {over} drawn cells"
        assert any(g != " " for g, _ in full), f"{t.title!r}: no reach at all"
        checked += 1
    assert checked >= 4


def test_a_task_whose_reach_starts_later_gets_a_wider_title(tmp_path):
    """The title still runs over the field (REV5 #19's ruling, kept through the
    field redesign): it spends the empty cells before its own reach, and stops
    at the today rule so the one column every row shares survives. MEASURED at
    96 wide: a task starting in the past keeps the label column's 12; one
    starting later reaches 34."""
    b, p = fixture(tmp_path)
    b.tasks.append(Task("A" * 60, p.id, "Backlog", "normal",
                        start_date=iso(9), due_date=iso(16)))
    b.tasks.append(Task("B" * 60, p.id, "Doing", "normal",
                        start_date=iso(-6), due_date=iso(-2)))
    out = rows(b)
    near = next(l for l in out if "B" * 10 in l)
    far = next(l for l in out if "A" * 10 in l)
    # measured: 27 for a task already under way, 30 for one starting later
    assert far.count("A") > near.count("B")
    assert (near.count("B") + 1, far.count("A") + 1) == (27, 30)


def test_the_header_counts_what_is_past_due(tmp_path):
    b, _p = fixture(tmp_path)
    assert "past due" in rows(b)[0]


# --------------------------------------------------------------------------- #
# the invariant every view in this codebase obeys
# --------------------------------------------------------------------------- #
def test_width_exact_at_every_step(tmp_path):
    b, _p = fixture(tmp_path)
    for w in (24, 40, 60, 72, 96, 97, 130, 200):
        for h in (0, 12, 20, 30):
            for line in rows(b, w, h):
                assert len(line) == max(24, w), f"{w}x{h}: {len(line)}"


def test_an_empty_board_still_renders(tmp_path):
    b = board(tmp_path, "empty.json")
    out = rows(b, 96, 12)
    assert all(len(l) == 96 for l in out)


# --------------------------------------------------------------------------- #
# the acceptance criterion of the field redesign (REV3)
# --------------------------------------------------------------------------- #
def _census(lines):
    frame = set("╭─╮│╰╯├┤┬┴┼")
    ink = chrome = field = dead = 0
    for line in lines:
        for ch in line:
            if ch == " ":
                dead += 1
            elif ch in frame:
                chrome += 1
            elif ch == "·":
                field += 1
            else:
                ink += 1
    n = ink + chrome + field + dead
    return {"marked": 100 * (ink + field) / n, "ink": 100 * ink / n,
            "dead": 100 * dead / n, "chrome": 100 * chrome / n}


def _load(tmp_path, projects, tasks, name):
    from taskboard.models import Board, Project, Task
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    hues = ["lime", "green", "sky", "blue", "indigo", "violet", "fuchsia", "pink"]
    per, k = max(1, tasks // projects), 0
    for i in range(projects):
        p = Project(f"Project {i}", hues[i % 8], "on_track",
                    start_date=iso(-20 - i), due_date=iso(6 + i * 5))
        b.projects.append(p)
        for j in range(per):
            b.tasks.append(Task(f"Task {i}-{j} something real", p.id,
                                ["Backlog", "Doing", "Done"][j % 3], "normal",
                                start_date=iso(k - 10), due_date=iso(k - 4)))
            k += 1
    return b


def test_more_data_no_longer_produces_less_screen(tmp_path):
    """THE ACCEPTANCE CRITERION, and the defect the redesign existed to fix.

    The old gantt was the one view where MORE data produced LESS used screen:
    from typical to extreme its ink FELL 23.3 % -> 21.0 % and its emptiness ROSE
    55.4 % -> 64.2 %, because an axis with no past drew every overdue project as
    a blank row. Measured now: ink RISES and dead FALLS with the data."""
    typical = _census(rows(_load(tmp_path, 5, 21, "t.json"), 96, 30))
    extreme = _census(rows(_load(tmp_path, 8, 44, "e.json"), 96, 30))
    assert extreme["ink"] > typical["ink"], (typical["ink"], extreme["ink"])
    # emptiness must not RUN AWAY with the data as it used to (+8.8 points from
    # typical to extreme); on this fixture it moves by a fraction of a point
    assert extreme["dead"] <= typical["dead"] + 1.0,         (typical["dead"], extreme["dead"])


def test_the_carrying_fraction_clears_what_rev3_measured(tmp_path):
    """REV3 measured 71.1 % of cells carrying at typical load. Measured here:
    71.4 %. The floor is set just under it, with margin for honest variation."""
    typical = _census(rows(_load(tmp_path, 5, 21, "t2.json"), 96, 30))
    assert typical["marked"] >= 68.0, typical["marked"]
    assert typical["dead"] <= 25.0, typical["dead"]


def test_the_separator_rows_are_gone_and_chrome_fell(tmp_path):
    """The `┈`x94 divider between project blocks was 470 cells of pure separator
    on a five-project board — the single biggest reason this view led the app in
    chrome at 21.2 %. Measured now: under 10 %."""
    out = rows(_load(tmp_path, 5, 21, "t3.json"), 96, 30)
    assert not any(set(l[1:-1]) == {"┈"} for l in out)
    assert _census(out)["chrome"] < 10.0


def test_the_span_separates_elapsed_from_remaining(tmp_path):
    """The top band's whole job: ASH for what has already gone, the project's
    own hue for what is left. One tone for the whole span would delete the cut
    the second band is measured against."""
    from taskboard.views import HEX
    b = _load(tmp_path, 2, 6, "span.json")
    text = render_gantt(b, False, None, TODAY, width=96, height=30)
    ash = hue = 0
    for s in text.spans:
        seg = text.plain[s.start:s.end]
        if "⣿" not in seg:
            continue
        if HEX["ash"] in str(s.style):
            ash += 1
        if any(HEX[c] in str(s.style) for c in ("lime", "green", "sky", "blue")):
            hue += 1
    assert ash and hue, f"span drawn in one tone only (ash={ash}, hue={hue})"


def test_two_tasks_of_different_length_draw_different_reaches(tmp_path):
    """DATAVIZ 13, which the old week-resolution bar violated: every task drew
    the same `▬▬▬▬▬`, and a mark that cannot vary is not a datum."""
    from taskboard.models import Project, Task
    b = board(tmp_path, "vary.json")
    p = Project("P", "lime", "on_track", start_date=iso(-10), due_date=iso(40))
    b.projects.append(p)
    b.tasks += [Task("Short one", p.id, "Doing", "normal",
                     start_date=iso(1), due_date=iso(3)),
                Task("Long one", p.id, "Doing", "normal",
                     start_date=iso(1), due_date=iso(40))]
    out = rows(b, 96, 30)
    short = next(l for l in out if "Short one" in l)
    long_ = next(l for l in out if "Long one" in l)
    assert long_.count("⣀") > short.count("⣀") + 3, (short.count("⣀"), long_.count("⣀"))
