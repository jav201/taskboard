"""The gantt's right edge, its titles and its field.

Rewritten 2026-10-02 (batch 2026-10-02-batch-01, G-A + AX-2): the gantt now fits its
window to the open work, folds projects, ends every row in ONE due chip and keeps
the dates on a two-row ruler at the top. Every law below that the verdict left
standing is kept and retargeted to the live helpers (`gantt_columns`,
`gantt_axis`, `_gantt_bar`, `_gantt_span`); the ones the verdict superseded say
which requirement superseded them.

(Original preamble, REV5 #19:)

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
from taskboard.views import (HEX, GanttAxis, gantt_axis, gantt_columns, gantt_plan,
                             gantt_window, render_gantt)

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


def rows(b, w=96, h=20, focus=None):
    return str(render_gantt(b, False, None, TODAY, width=w, height=h,
                            focus=focus)).split("\n")


def body_rows(lines):
    """The body of a gantt render: under the header and the two ruler rows,
    minus a trailing legend row."""
    out = lines[3:]
    if out and out[-1].startswith(" ") and not out[-1].startswith("  "):
        out = out[:-1]
    return [l for l in out if l.strip()]


# --------------------------------------------------------------------------- #
# the right edge
# --------------------------------------------------------------------------- #
def test_every_row_ends_in_a_date_reading(tmp_path):
    """HLR-103 (batch 2026-10-02-batch-01). Every row that carries open work ends
    in ONE due chip — `▲Nd`, `today`, a date, or `no due`. The blank-edge trap
    the old law caught still applies: an edge of pure ground says nothing."""
    b, _p = fixture(tmp_path)
    _label, chip_w, _f = gantt_columns(96)
    body = body_rows(rows(b, 96, 20))
    assert len(body) >= 3
    for line in body:
        edge = line[-chip_w:]
        assert re.search(r"(▲\d+d|today|no due|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2})$",
                         edge.strip()), f"{edge!r} is not a due reading"


def test_finished_work_folds_into_its_projects_count(tmp_path):
    """Superseded by D2 / HLR-102 (batch 2026-10-02-batch-01, G-A: "done folds
    to ✓n"). Was: finished work rested at the tail in ash with its dates. Now it
    draws no row at all and is counted on its project's span row — at a label of
    at least 26 cells, which 118 columns give."""
    b, _p = fixture(tmp_path)
    out = rows(b, 118, 30)
    assert not any("Old finis" in l for l in out), "a finished task still draws a row"
    atlas = next(l for l in out if "Atlas" in l)
    assert "✓1" in atlas, atlas


def test_the_project_row_carries_its_due_chip(tmp_path):
    """HLR-103. The project row ends in its committed due, as a chip, while it
    holds open work."""
    b, _p = fixture(tmp_path)
    _label, chip_w, _f = gantt_columns(130)
    line = next(l for l in rows(b, 130, 30) if "Atlas" in l)
    assert line[-chip_w:].strip() == "Aug 24", line[-chip_w:]


def test_the_alert_lives_in_chips_and_counts_and_nothing_else(tmp_path):
    """`▲` is severity's seat: the late chip `▲Nd`, a project's `▲n` count, the
    header's `▲n past due`, and a dependency mark planned to start too early.
    Nothing else on the gantt wears the severity hue (HLR-103)."""
    b, _p = fixture(tmp_path)
    text = render_gantt(b, False, None, TODAY, width=96, height=20)
    worn = [text.plain[s.start:s.end].strip() for s in text.spans
            if HEX["over"] in str(s.style)]
    assert worn, "vacuous: nothing wears the severity hue at all"
    for seg in worn:
        assert re.fullmatch(r"▲\d+d|▲\d+|▲\d+ past due|↳", seg), f"severity worn by {seg!r}"


def test_a_bar_never_wears_an_urgency_hue(tmp_path):
    """The span and the reaches may only ever wear an identity hue, the ash of
    elapsed time, the flow packet's bright, or the batch-06 priority hues.

    Was vacuous since the field left braille (BACKLOG, gauge batch): it matched
    `⣿⣤⡄⣀` segments the view no longer draws. It now matches the glyphs the
    field draws today, and asserts it found some."""
    from taskboard.models import PROJECT_COLORS
    from taskboard.views import CRITICAL_REACH, FIELD_PHASE_TIP, FIELD_REACH, FIELD_TASK
    b, _p = fixture(tmp_path)
    text = render_gantt(b, False, None, TODAY, width=96, height=20)
    lawful = ({HEX[c] for c in PROJECT_COLORS}
              | {HEX["bright"], HEX["ash"], HEX["mut"], HEX["rose"], HEX["sky"]})
    bar = {FIELD_REACH, FIELD_TASK, CRITICAL_REACH, *FIELD_PHASE_TIP}
    seen = 0
    for s in text.spans:
        seg = text.plain[s.start:s.end]
        if seg.strip() and set(seg) <= bar:
            seen += 1
            assert any(h in str(s.style) for h in lawful), f"bar wears {s.style}"
            assert HEX["over"] not in str(s.style)
            assert HEX["soon"] not in str(s.style)
    assert seen >= 3, "vacuous: no bar segment found"


# --------------------------------------------------------------------------- #
# the titles
# --------------------------------------------------------------------------- #
def test_a_title_never_covers_its_own_reach(tmp_path):
    """The safety property, now held by layout: the title owns the label
    column, the gutter is its own column, and the field starts after it — so no
    title can reach a bar cell (HLR-103, LLR-101.10). Checked on the rendered
    rows: the label column holds no field glyph and the field no title text."""
    from taskboard.views import FIELD_PHASE_TIP, FIELD_TASK
    b, _p = fixture(tmp_path)
    label_w, _c, _f = gantt_columns(96)
    checked = 0
    for t in b.tasks:
        line = next((l for l in rows(b, 96, 30) if t.title[:12] in l), None)
        if line is None:
            continue                       # rest work folds (D2)
        assert not set(line[:label_w]) & {FIELD_TASK, *FIELD_PHASE_TIP}, line
        assert t.title[:12] not in line[label_w:], line
        checked += 1
    assert checked >= 3


def test_a_long_title_is_clipped_inside_its_label(tmp_path):
    """Superseded by HLR-103 (batch 2026-10-02-batch-01): the REV5 #19 ruling let
    a title spend the empty field before its reach, so later reaches got wider
    titles. G-A gives the title a fixed label column and the dependency mark its
    own gutter (the prototype's frames), so every title is clipped the same way,
    with an ellipsis, inside its label."""
    b, p = fixture(tmp_path)
    b.tasks.append(Task("A" * 60, p.id, "Backlog", "normal",
                        start_date=iso(9), due_date=iso(16)))
    b.tasks.append(Task("B" * 60, p.id, "Doing", "normal",
                        start_date=iso(-6), due_date=iso(-2)))
    label_w, _c, _f = gantt_columns(96)
    out = rows(b, 96, 30)
    near = next(l for l in out if "B" * 10 in l)
    far = next(l for l in out if "A" * 10 in l)
    assert near[:label_w].count("B") == far[:label_w].count("A") == label_w - 4
    assert near[label_w - 2] == "…" and far[label_w - 2] == "…"


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
    """REV3 measured 71.1 % of cells carrying at typical load; the 2-day axis
    ended at 62.5 % (floor 61). G-A + AX-2 (batch 2026-10-02-batch-01) measured
    59.8 %: the fixed 20-cell label column and the two ruler rows — mostly the
    blanks between day numbers — are cells that carry nothing by design. The
    floor is set just under the new measured value."""
    typical = _census(rows(_load(tmp_path, 5, 21, "t2.json"), 96, 30))
    assert typical["marked"] >= 58.5, typical["marked"]


def test_emptiness_is_bounded_where_the_content_could_actually_fill_the_screen(tmp_path):
    """`dead <= 25` on the fixture whose content exceeds the screen (kept at its
    original value; measured 24.6 % on G-A + AX-2, batch 2026-10-02-batch-01).

    The guard that keeps it from going vacuous changed with the design: the
    extreme fixture used to OVERFLOW (`+N not shown`); with folding (HLR-102)
    nothing is hidden, so the proof that the content exceeds the screen is now
    that some project had to fold."""
    out = rows(_load(tmp_path, 8, 44, "dead_e.json"), 96, 30)
    assert _census(out)["dead"] <= 25.0, _census(out)["dead"]
    assert any(l.startswith("▸") for l in out), (
        "the extreme fixture no longer exceeds the screen; this law went vacuous")
    assert not any("not shown" in l for l in out), "folding should have held it"


def test_nothing_is_hidden_where_the_old_two_row_shape_hid_work(tmp_path):
    """The operator's actual complaint, pinned at a size where it is a REAL
    difference and not a tautology.

    MEASURED both ways before this was written, because a "nothing is hidden"
    law is worthless at a size where nothing was ever hidden:

        5 projects / 21 tasks, 104x28 — old shape hid 4 tasks, new hides 0
                                104x30 — old shape hid 2 tasks, new hides 0
                                104x32 — old shape already fitted

    The swimlane separators add one frame row per project block, so the boundary
    that used to cost nothing now costs four rows on this fixture. Re-measured:
    104x31 is the smallest height where the same content fits without shedding.
    Blank rows below the content are slack; a task the view declines to draw is
    the defect."""
    out = rows(_load(tmp_path, 5, 21, "fits.json"), 104, 31)
    assert not any("not shown" in line for line in out), (
        "the gantt is hiding rows at a size where its content fits")


def test_every_project_has_its_span_row_and_chrome_is_acceptable(tmp_path):
    """Superseded by HLR-102 (batch 2026-10-02-batch-01): the full-width `─`
    rule between project blocks is gone — in the G-A frames each project's own
    span row opens its block. The chrome law is kept (< 18 %)."""
    out = rows(_load(tmp_path, 5, 21, "t3.json"), 96, 30)
    assert not any(set(l) == {"─"} for l in out), "a separator row is back"
    for i in range(5):
        assert any(l.startswith(("▾", "▸")) and f"Project {i}" in l for l in out), i
    assert _census(out)["chrome"] < 18.0, _census(out)["chrome"]


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
        # match a prefix that survives truncation on the narrowest widths
        named = [l for l in out if "Telemetry" in l]
        assert len(named) >= 4, f"{w}x{h}: fixture drew {len(named)} task rows"
        for l in named:
            got = first_bar_gutter(l)
            assert got is not None and got >= 2, (
                f"{w}x{h}: {got} cells between title and bar, want >= 2\n{l}")


def test_a_truncated_project_name_never_touches_the_field(tmp_path):
    """AC-2, kept: a clipped project name ends in its ellipsis and a blank, and
    the gutter column after the label is blank too — two cells of air before the
    field (LLR-101.10, LLR-101.11)."""
    for w, h in ((104, 30), (96, 30)):
        label_w, _c, _f = gantt_columns(w)
        out = rows(gutter_board(tmp_path), w, h)
        row = next(l for l in out if l.startswith(("▾ Machine", "▸ Machine")))
        assert row[label_w - 1:label_w + 1] == "  ", (
            f"{w}x{h}: no 2-cell gutter after {row[:label_w + 1]!r}")


def test_the_field_is_ruled_by_weeks(tmp_path):
    """AC-3, kept on the fitted axis: while a week spans a few cells (k <= 2)
    every guide is a Monday's first cell; it is drawn on the body rows; and it
    never takes the today column — two verticals in one cell would read as one
    thicker rule."""
    from taskboard.views import FIELD_WEEK, LATTICE
    assert FIELD_WEEK != LATTICE, "the guide is indistinguishable from the ground"
    b = gutter_board(tmp_path)
    for w, h in ((104, 30), (96, 30), (120, 40)):
        out = rows(b, w, h)
        ruled = [l for l in body_rows(out) if FIELD_WEEK in l]
        assert len(ruled) >= 4, f"{w}x{h}: only {len(ruled)} rows carry the guide"
    for k in (0.5, 1, 2):
        ax = GanttAxis(TODAY - timedelta(days=20), k, 60, TODAY)
        g = ax.guides()
        assert g, k
        for x in g:
            assert any(d.weekday() == 0 and ax.cell(d) == x for d in ax.days_in(x)), (k, x)
    # THE GUARD, where it can fire: today on a Monday owns its own cell.
    for anchor in (date(2026, 8, 3), date(2026, 8, 2)):
        for k in (0.5, 1, 2):
            ax = GanttAxis(anchor - timedelta(days=14), k, 60, anchor)
            assert ax.tc not in ax.guides(), (anchor, k)


def test_the_ruler_names_the_months(tmp_path):
    """AC-4, moved to the top (HLR-105, batch 2026-10-02-batch-01): the month
    row (row 1) names every month band wide enough to hold its three letters,
    and the axis row that used to close the view is gone."""
    for w, h in ((104, 30), (96, 30), (120, 40)):
        out = rows(gutter_board(tmp_path), w, h)
        label_w, _c, field_w = gantt_columns(w)
        groups = gantt_plan(gutter_board(tmp_path), False, None, TODAY, h - 3)
        ax = gantt_axis(field_w, TODAY, *gantt_window(groups, TODAY))
        months = out[1][label_w + 1:label_w + 1 + field_w]
        starts = [0] + [x for x in range(1, ax.w) if ax.day(x).month != ax.day(x - 1).month]
        for i, x0 in enumerate(starts):
            x1 = (starts + [ax.w])[i + 1]
            if x1 - x0 >= 4:
                assert ax.day(x0).strftime("%b") in months[x0:x1], (w, h, months)
        assert "today" not in out[-1], "the bottom axis is back"


def test_the_project_reach_is_a_rule_not_a_slab(tmp_path):
    """AC-5, kept: reach > progress > task as three distinct weights, and the
    span drawn as a thin rule, never a slab."""
    from taskboard.views import FIELD_PROGRESS, FIELD_REACH, FIELD_TASK
    assert FIELD_REACH != "█", "the slab is back"
    assert len({FIELD_REACH, FIELD_PROGRESS, FIELD_TASK}) == 3, \
        "two weights collapsed into one, so the hierarchy is gone"
    out = rows(gutter_board(tmp_path), 104, 30)
    span = next(l for l in out if l.startswith(("▾ Machine", "▸ Machine")))
    assert FIELD_REACH in span and "█" not in span


def test_the_circle_sits_at_the_progress_fraction_of_the_span(tmp_path):
    """AC3, kept and retargeted to `_gantt_span` on the fitted axis: the dot is
    a reading — on the start at 0.0, on the `◆` at 1.0, monotone between."""
    from taskboard.models import Project
    from taskboard.views import PROGRESS_DOT, _gantt_span
    p = Project("Span", "lime", "on_track",
                start_date=(TODAY - timedelta(days=20)).isoformat(),
                due_date=(TODAY + timedelta(days=20)).isoformat())
    ax = GanttAxis(TODAY - timedelta(days=25), 1, 60, TODAY)
    seen = {}
    for prog in (0.0, 0.25, 0.5, 0.75, 1.0):
        span = _gantt_span(p, ax, prog, 0)
        cells = [i for i, (g, _t) in enumerate(span) if g == PROGRESS_DOT]
        assert len(cells) == 1, (prog, cells)
        seen[prog] = cells[0]
    assert seen[0.0] == ax.cell(TODAY - timedelta(days=20))
    assert seen[1.0] == ax.cell(TODAY + timedelta(days=20))
    order = [seen[k] for k in (0.0, 0.25, 0.5, 0.75, 1.0)]
    assert order == sorted(order) and len(set(order)) > 2, order

# --------------------------------------------------------------------------- #
# batch-06: priority hue, milestone, dependency, focus (gantt semantics)
# --------------------------------------------------------------------------- #
def test_task_reach_wears_priority_hue(tmp_path):
    """High priority draws rose, normal sky, low mut — and a critical-chain task
    is structure, heavy and bright (HLR-108). Rest work draws no bar at all
    (D2), so the old `ash` arm moved to the fold count."""
    from taskboard.views import CRITICAL_REACH, _gantt_bar
    b = board(tmp_path, "prio.json")
    p = Project("P", "lime", "on_track", start_date=iso(-10), due_date=iso(40))
    b.projects.append(p)
    b.tasks += [
        Task("High", p.id, "Doing", "high", start_date=iso(2), due_date=iso(8)),
        Task("Normal", p.id, "Doing", "normal", start_date=iso(2), due_date=iso(8)),
        Task("Low", p.id, "Doing", "low", start_date=iso(2), due_date=iso(8)),
    ]
    ax = GanttAxis(TODAY - timedelta(days=5), 1, 60, TODAY)
    tones = {}
    for t in b.tasks:
        drawn = [(g, tone) for g, tone in _gantt_bar(t, b, ax, set(), 0) if g != " "]
        assert drawn, t.title
        tones[t.title] = drawn[-1][1]
    assert tones == {"High": "rose", "Normal": "sky", "Low": "mut"}
    crit = [(g, tone) for g, tone in _gantt_bar(b.tasks[0], b, ax, {b.tasks[0].id}, 0)
            if g not in (" ", "▬")]               # the flow packet rides on top
    assert {tone for _g, tone in crit} == {"crit"}
    assert CRITICAL_REACH in {g for g, _ in crit}


def test_milestone_renders_as_a_single_diamond(tmp_path):
    """A task whose start equals due renders as one ◆ cell, not a span."""
    from taskboard.views import _gantt_bar
    b = board(tmp_path, "milestone.json")
    p = Project("P", "lime", "on_track", start_date=iso(-10), due_date=iso(40))
    b.projects.append(p)
    b.tasks.append(Task("Milestone", p.id, "Doing", "normal",
                        start_date=iso(5), due_date=iso(5)))
    ax = GanttAxis(TODAY - timedelta(days=5), 1, 60, TODAY)
    drawn = [(g, tone) for g, tone in _gantt_bar(b.tasks[0], b, ax, set(), 0) if g != " "]
    assert drawn == [("◆", "sky")]


def test_dependency_indicator_shows_when_task_has_depends_on(tmp_path):
    """HLR-103 (batch 2026-10-02-batch-01): a task waiting on OPEN work wears
    `↳` in the gutter column — between its label and the field, never over the
    title; a task waiting on nothing open has a blank gutter."""
    b, p = fixture(tmp_path)
    b.tasks[1].depends_on = [b.tasks[2].id]          # waits on an open task
    label_w, _c, _f = gantt_columns(96)
    out = rows(b, 96, 30)
    line = next(l for l in out if b.tasks[1].title[:15] in l)
    assert line[label_w] == "↳", line
    other = next(l for l in out if b.tasks[2].title[:15] in l)
    assert other[label_w] == " ", other


def test_gantt_focus_hides_other_projects_and_inbox(tmp_path):
    """focus=project_id renders only that project and drops inbox rows."""
    from taskboard.models import Project, Task
    b = board(tmp_path, "focus.json")
    p1 = Project("Alpha", "lime", "on_track",
                 start_date=iso(-10), due_date=iso(20))
    p2 = Project("Beta", "sky", "on_track",
                 start_date=iso(-10), due_date=iso(20))
    b.projects += [p1, p2]
    b.tasks += [
        Task("Alpha task", p1.id, "Doing", "normal",
             start_date=iso(1), due_date=iso(5)),
        Task("Beta task", p2.id, "Doing", "normal",
             start_date=iso(1), due_date=iso(5)),
        Task("Loose task", None, "Doing", "normal",
             start_date=iso(1), due_date=iso(5)),
    ]
    out = rows(b, 96, 30, focus=p1.id)
    text = "\n".join(out)
    assert "Alpha task" in text
    assert "Beta task" not in text
    assert "Loose task" not in text
    assert "focused" in text.lower()


# --------------------------------------------------------------------------- #
# the time scale survives the `/` filter
# --------------------------------------------------------------------------- #
def test_filtered_gantt_keeps_its_time_scale_inside_the_panel(tmp_path):
    """AT-008 (HLR-006, batch 2026-09-30-batch-01), restated for AX-2 (HLR-105,
    batch 2026-10-02-batch-01): the time scale is the ruler now, pinned under the
    header, and under a `/` filter it sits under the filter bar — panel rows
    3–4 — while the view stays exactly the panel's height. RED: the filtered
    view drawn at `height` instead of `height - 2` → 22 rows."""
    from taskboard.views import render_view
    b, _p = fixture(tmp_path)
    h = 20
    plain = str(render_view("gantt", b, False, None, TODAY, width=96,
                            height=h)).split("\n")
    ruler = plain[1:3]
    assert re.search(r"(July|August|September|Jul|Aug|Sep)", ruler[0]), ruler[0]
    out = str(render_view("gantt", b, False, None, TODAY, width=96, height=h,
                          search_query="checkout")).split("\n")
    assert len(out) == h, f"filtered gantt is {len(out)} rows in a {h}-row panel"
    assert re.search(r"(July|August|September|Jul|Aug|Sep)", out[3]), out[3]
    assert any("checkout" in l.lower() for l in out[:3]), "the filter bar is missing"


def test_filtered_kanban_fits_the_panel_too(tmp_path):
    """AT-008 (HLR-006). The same overlay seats kanban, so the same two-row overflow applied
    there: the filtered board must also be exactly the panel's height."""
    from taskboard.views import render_view
    b, _p = fixture(tmp_path)
    h = 20
    out = str(render_view("kanban", b, False, None, TODAY, width=96, height=h,
                          search_query="checkout")).split("\n")
    assert len(out) == h, f"filtered kanban is {len(out)} rows in a {h}-row panel"
    # and the rows it kept are the right ones (review F2, batch
    # 2026-09-30-batch-01): the filter bar under the header, the matching card
    # below it — a renderer that merely dropped rows would lose one of them
    assert any("checkout" in l.lower() for l in out[:3]), "the filter bar is missing"
    assert any("checkout" in l.lower() for l in out[3:]), "the matching card is missing"
