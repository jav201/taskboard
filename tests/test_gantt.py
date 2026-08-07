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
    body = [l for l in out if l.startswith("▎ ") or l.startswith("▏ ")]
    assert len(body) >= 5
    for line in body:
        edge = line[-METER_W:]
        # a READING now, not a bar. The blank-edge trap the old law caught still
        # applies: an edge of pure ground says nothing and must not pass.
        assert re.fullmatch(r"·*(▲?\d+d\+?|today|done|—)", edge), (
            f"{line[-10:]!r} is not a due reading")
        assert edge.strip("·"), f"{line[-10:]!r} has no reading at all"


def test_finished_work_shows_a_spent_meter_and_rests_in_ash(tmp_path):
    """Active at the top, finished at the tail, and the finished row RESTS: thin
    spine, ash, no chip and no severity."""
    b, _p = fixture(tmp_path)
    line = next(l for l in rows(b, 96, 30) if "Old finished" in l)
    # finished work: the edge SAYS so, in one tone, over the board's ground
    assert line[-METER_W:].strip("·") == "done"
    assert line.startswith("▏ ")               # the thin spine
    assert "▲" not in line


def test_the_project_row_keeps_its_progress_figure(tmp_path):
    b, _p = fixture(tmp_path)
    line = next(l for l in rows(b, 130, 30) if "Atlas" in l)
    assert re.search(r"\d+%", line), line
    assert re.fullmatch(r"·*(▲?\d+d\+?|today|done|—)", line[-METER_W:]), line[-METER_W:]


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
    at the today rule so the one column every row shares survives.

    THE INTENT is the inequality — later reach, wider title — and it is asserted
    first and on its own, because it is the thing that must stay true. The exact
    pair beneath it is a pin, and it moved: `GUTTER` now holds two cells back
    from the title on every row, so both widths dropped by exactly 2 (27 -> 25,
    30 -> 28). The pin is re-measured, not deleted, so the next change to the
    title's reach still has to look a human in the eye."""
    b, p = fixture(tmp_path)
    b.tasks.append(Task("A" * 60, p.id, "Backlog", "normal",
                        start_date=iso(9), due_date=iso(16)))
    b.tasks.append(Task("B" * 60, p.id, "Doing", "normal",
                        start_date=iso(-6), due_date=iso(-2)))
    out = rows(b)
    near = next(l for l in out if "B" * 10 in l)
    far = next(l for l in out if "A" * 10 in l)
    assert far.count("A") > near.count("B")
    # measured: 25 for a task already under way, 28 for one starting later
    assert (near.count("B") + 1, far.count("A") + 1) == (25, 28)


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
    assert not any(set(l) == {"┈"} for l in out)
    assert _census(out)["chrome"] < 10.0


def test_the_span_separates_elapsed_from_remaining(tmp_path):
    """The top band's whole job: ASH for what has already gone, the project's
    own hue for what is left. One tone for the whole span would delete the cut
    the second band is measured against."""
    from taskboard.views import HEX, FIELD_REACH
    b = _load(tmp_path, 2, 6, "span.json")
    text = render_gantt(b, False, None, TODAY, width=96, height=30)
    ash = hue = 0
    for s in text.spans:
        seg = text.plain[s.start:s.end]
        if FIELD_REACH not in seg:
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
    from taskboard.views import FIELD_TASK
    assert long_.count(FIELD_TASK) > short.count(FIELD_TASK) + 3, (
        short.count(FIELD_TASK), long_.count(FIELD_TASK))


# --------------------------------------------------------------------------- #
# THE GAUGE, and the gutter in front of it
#
# The operator's complaint, twice over: "los bloques siguen siendo muy grandes y
# se empalman con el texto", and "no hay gauges de semana y mes". A bar measured
# against nothing is the disorder; a title flush against its own bar is the
# collision. Both are measured here rather than described.
# --------------------------------------------------------------------------- #
BAR_GLYPHS = set("█▓▒▌▃▅▆▇━◆▬")


def gutter_board(tmp_path):
    """The shape that collided: LONG titles on tasks whose reach starts LEFT of
    today. When the reach starts to the right, the today rule already sits
    between title and bar and hides the defect — which is why it survived."""
    b = board(tmp_path, "gutter.json")
    p = Project("Machine Learning Platform Team", "cyan", "on_track",
                start_date=iso(-30), due_date=iso(40))
    b.projects.append(p)
    for k, off in enumerate((-4, -8, -12, -20, -2)):
        b.tasks.append(Task(f"Telemetry_Ingestion_Namespace_Migration_{k}",
                            p.id, "Doing", "normal",
                            start_date=iso(off), due_date=iso(off + 6)))
    return b


def first_bar_gutter(line: str) -> int | None:
    """Cells of non-title ground before the row's first bar glyph, or None when
    the row draws no bar."""
    for j, ch in enumerate(line):
        if ch in BAR_GLYPHS:
            n = 0
            while j - 1 - n >= 0 and line[j - 1 - n] in (" ", "·", "┆"):
                n += 1
            return n
    return None


def test_a_truncated_title_never_touches_its_own_bar(tmp_path):
    """AC-1. Before the gutter this measured 0 on 5 of 5 rows at every width:
    `Telemetry_Ingestion_Name…▬▒▒▅`, the ellipsis flush against the reach."""
    # the literal 2 is deliberate: `>= GUTTER` would be trivially true when
    # GUTTER is 0, so the predicate could not fail on the very mutation it
    # exists to catch
    for w, h in ((104, 30), (102, 16), (96, 30), (120, 40)):
        out = rows(gutter_board(tmp_path), w, h)
        named = [l for l in out if "Telemetry_Ingestion" in l]
        assert len(named) >= 4, f"{w}x{h}: fixture drew {len(named)} task rows"
        for l in named:
            got = first_bar_gutter(l)
            assert got is not None and got >= 2, (
                f"{w}x{h}: {got} cells between title and bar, want >= 2\n{l}")


def test_a_truncated_project_name_never_touches_the_field(tmp_path):
    """AC-2. The project row has no borrowed field cells to give back — its
    label is exactly `label_w` wide — so its gutter comes out of the name's own
    clip. It read `▎ Data Warehou…◂████` before."""
    from taskboard.views import gantt_geometry
    for w, h in ((104, 30), (96, 30)):
        out = rows(gutter_board(tmp_path), w, h)
        g = gantt_geometry(w, h)
        row = next(l for l in out if l.startswith("▎ Machine"))
        # everything from the name's last glyph to the field's first cell.
        # literal 2 again — `" " * GUTTER` is the empty string when GUTTER is 0
        # and `endswith("")` is true of every string alive
        tail = row[:g.label_w]
        assert tail.endswith("  "), (
            f"{w}x{h}: project label {tail!r} has no 2-cell gutter")


def test_the_field_is_ruled_by_weeks(tmp_path):
    """AC-3. The gauge the view never had. Every guide is a monday, it is drawn
    on the body rows and not just once, and it never takes the today column —
    two verticals in one cell would read as one thicker rule, a third meaning
    nobody declared."""
    from taskboard.views import FIELD_WEEK, LATTICE, gantt_gauge, gantt_geometry
    # a guide that IS the lattice rules nothing, and every check below would
    # still pass on the lattice's own dots
    assert FIELD_WEEK != LATTICE, "the guide is indistinguishable from the ground"
    b = gutter_board(tmp_path)
    for w, h in ((104, 30), (96, 30), (120, 40)):
        g = gantt_geometry(w, h)
        weeks, _ = gantt_gauge(g, TODAY)
        assert weeks, f"{w}x{h}: no week guide at all"
        # every guide cell really is a monday, by the view's own day axis
        for cell in weeks:
            days = {TODAY + timedelta(days=dc - g.today_dc)
                    for dc in (cell * 2, cell * 2 + 1)}
            assert any(d.weekday() == 0 for d in days), f"cell {cell} is no monday"
        assert g.today_dc // 2 not in weeks, "a guide took the today column"
        out = rows(b, w, h)
        ruled = [l for l in out if FIELD_WEEK in l]
        assert len(ruled) >= 4, f"{w}x{h}: only {len(ruled)} rows carry the guide"

    # THE GUARD, on a date where it can actually fire. `TODAY` is a Thursday, so
    # the today cell (which spans today and tomorrow) can never hold a monday and
    # the assertion above is vacuous on its own — deleting the guard leaves it
    # green. These two anchors are the cases that make it bite.
    for anchor in (date(2026, 8, 3),      # a MONDAY: today's own cell
                   date(2026, 8, 2)):     # a SUNDAY: tomorrow's half of the cell
        g = gantt_geometry(104, 30)
        weeks, _ = gantt_gauge(g, anchor)
        assert g.today_dc // 2 not in weeks, (
            f"{anchor} ({anchor:%A}): the week guide took the today column")


def test_the_axis_names_the_months(tmp_path):
    """AC-4. The operator chose to put the months on the axis the day figures already
    own, so this asserts BOTH scales survive on that one row: a month name that
    could not stand clear was dropped whole, but at least one is drawn and the
    day figures are untouched."""
    from taskboard.views import gantt_gauge, gantt_geometry, _scale_cells
    for w, h in ((104, 30), (96, 30), (120, 40)):
        g = gantt_geometry(w, h)
        _, months = gantt_gauge(g, TODAY)
        body, cols = _scale_cells(g, months)
        assert cols, f"{w}x{h}: no month name reached the axis"
        drawn = "".join(body)
        assert "today" in drawn, f"{w}x{h}: the day scale lost its anchor"
        # whole names only — never a half-printed month, which is a wrong date
        for at in sorted(months):
            if at in cols:
                assert drawn[at:at + 3] == months[at], (
                    f"{w}x{h}: {months[at]} came out as {drawn[at:at + 3]!r}")
        axis = rows(gutter_board(tmp_path), w, h)[-1]
        assert any(months[at] in axis for at in sorted(months) if at in cols)


def test_the_project_reach_is_a_rule_not_a_slab(tmp_path):
    """AC-5. `█` is what the operator saw as "bloques muy grandes": it buried
    the guide under it and shouted over every task bar. The three weights still
    rank reach > progress > task; the top one stopped shouting."""
    from taskboard.views import FIELD_PROGRESS, FIELD_REACH, FIELD_TASK
    assert FIELD_REACH != "█", "the slab is back"
    assert len({FIELD_REACH, FIELD_PROGRESS, FIELD_TASK}) == 3, \
        "two weights collapsed into one, so the hierarchy is gone"
    out = rows(gutter_board(tmp_path), 104, 30)
    span = next(l for l in out if l.startswith("▎ Machine"))
    assert FIELD_REACH in span and "█" not in span
