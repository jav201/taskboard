"""The lanes view — one row per project, all on the same axis of days.

Was: a phase grid that showed the FIRST task of each project/phase cell and
collapsed the rest into "N more" — a lossy copy of the columns view next to it
(`_tui_prism_proposal/AUDIT.md` §3: 29-33 % of tasks hidden). Now the row says
what the project is doing: the field is the work it still owes, today is carved
through it, and the figures on the right say how much is done and how late.

The laws below are the ones `verify_prism.py` states for the lanes composition,
narrowed to what this increment ships (no ranking, no leader's bench, no resting
row — those arrive with the allocator).
"""

import re
from datetime import date, timedelta

from taskboard.models import Board, Project, Task
from taskboard.views import (LANE_TITLES, RULE, STATUS_MARK, HEX, lane_geometry,
                             lane_titles, lanes_of, nav_model, phase_glyph,
                             render_swimlanes)

TODAY = date(2026, 7, 30)
WIDTHS = (24, 25, 31, 32, 40, 63, 72, 96, 97, 130, 201)


def board(tmp_path, name="lanes.json"):
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def typical(tmp_path):
    """Four projects: one late, one healthy, one paused, one cancelled."""
    b = board(tmp_path)
    atlas = Project("Atlas", "lime", "on_track", due_date=iso(20))
    beacon = Project("Beacon", "sky", "on_track", due_date=iso(40))
    cinder = Project("Cinder", "violet", "paused", due_date=iso(15))
    delta = Project("Delta", "pink", "cancelled", due_date=iso(-9))
    b.projects += [atlas, beacon, cinder, delta]
    b.tasks += [
        Task("Fix the ingest path", atlas.id, "Doing", "high", due_date=iso(-9)),
        Task("Write the v2 reference", atlas.id, "Backlog", "normal", due_date=iso(6)),
        Task("Ship the migration", atlas.id, "Done", "normal", due_date=iso(-2)),
        Task("Harden the search index", beacon.id, "Doing", "normal", due_date=iso(12)),
        Task("Deprecate v1 endpoints", cinder.id, "Backlog", "normal", due_date=iso(3)),
        Task("Retire the old host", delta.id, "Backlog", "normal", due_date=iso(1)),
    ]
    b.save()
    return b


def lane_rows(out: list[str]) -> list[str]:
    """The PROJECT rows — a named lane, not one of the task rows under it (those
    carry the same spine but two spaces before their phase glyph)."""
    return [line for line in out if line.startswith("│▎ ") and line[3] != " "]


def rows_of(b, w=96, h=30, selected=None, line_map=None):
    return str(render_swimlanes(b, False, selected, TODAY, width=w, height=h,
                                line_map=line_map)).split("\n")


def markup_of(b, w=96, h=30) -> str:
    from taskboard.views import render_swimlanes as r
    return r(b, False, None, TODAY, width=w, height=h).markup


# --------------------------------------------------------------------------- #
# width — the law every view in this codebase obeys
# --------------------------------------------------------------------------- #
def test_every_row_is_exactly_the_requested_width(tmp_path):
    b = typical(tmp_path)
    for w in WIDTHS:
        for h in (0, 14, 24, 30, 44):
            for line in rows_of(b, w, h):
                assert len(line) == max(24, w), f"{w}x{h}: {len(line)} != {w}"


def test_the_figures_are_flush_right_on_every_lane_row(tmp_path):
    """The chip is the rightmost thing on the row at every width — that is what
    makes a column of chips scannable. Width-exactness alone does not catch a
    figures block that drifted left, because the padding would just move."""
    b = typical(tmp_path)
    for w in (40, 72, 96, 130):
        for line in lane_rows(rows_of(b, w, 30)):
            body = line[1:-1]                       # drop the frame borders
            assert body == body.rstrip(), f"width {w}: figures not flush right"


def test_the_view_fills_the_height_it_is_given(tmp_path):
    b = typical(tmp_path)
    assert len(rows_of(b, 96, 30)) == 30
    assert len(rows_of(b, 96, 44)) == 44


def test_an_empty_board_still_draws_a_frame_and_says_so(tmp_path):
    b = board(tmp_path, "empty.json")
    out = rows_of(b, 96, 12)
    assert all(len(line) == 96 for line in out)
    assert any("no projects" in line for line in out)


# --------------------------------------------------------------------------- #
# the shared axis
# --------------------------------------------------------------------------- #
def test_today_sits_in_the_same_column_on_every_lane(tmp_path):
    """The whole point of a SHARED axis: a day is a column, so two projects'
    marks are comparable by eye. If each row scaled itself, they would not be."""
    b = typical(tmp_path)
    geo = lane_geometry(94, 30)
    col = 1 + geo.label_w + geo.today_dc // 2          # +1 for the frame border
    lanes = lane_rows(rows_of(b, 96, 30))
    assert len(lanes) >= 4
    marks = {line[col] for line in lanes}
    for ch in marks:
        assert ch == RULE or 0x2800 <= ord(ch) <= 0x28FF, f"{ch!r} at the today column"
    assert RULE in marks          # at least one lane shows the rule uncovered


def test_a_project_whose_work_runs_off_the_window_is_marked_not_crushed(tmp_path):
    """PROPOSAL §4.2 / R3. The window narrows as the widget shrinks; what falls
    outside is FLAGGED at the edge instead of being piled onto the last column."""
    b = board(tmp_path, "far.json")
    p = Project("Far", "lime", "on_track", due_date=iso(400))
    b.projects.append(p)
    b.tasks.append(Task("A very distant thing", p.id, "Backlog", "normal",
                        due_date=iso(400)))
    lane = [line for line in rows_of(b, 40, 20) if line.startswith("│▎ ")][0]
    assert "▸" in lane


# --------------------------------------------------------------------------- #
# what the row says
# --------------------------------------------------------------------------- #
def test_the_row_names_the_project_and_shows_its_figures(tmp_path):
    b = typical(tmp_path)
    lane = [line for line in rows_of(b) if "Atlas" in line][0]
    assert "1/3" in lane            # done / total
    assert "!1" in lane             # one high-priority open task
    assert "▲9d" in lane            # its worst late distance


def test_a_stopped_project_is_visibly_stopped(tmp_path):
    """AUDIT §4's headline defect: a cancelled project was drawn exactly like a
    healthy one. `on_track` stays unmarked so the marked ones are the exception."""
    b = typical(tmp_path)
    out = rows_of(b)
    assert any(STATUS_MARK["paused"] in line for line in out if "Cinder" in line)
    assert any(STATUS_MARK["cancelled"] in line for line in out if "Delta" in line)
    assert not any(m in line for line in out if "Atlas" in line
                   for m in STATUS_MARK.values())


def test_a_closed_project_is_never_judged(tmp_path):
    """Nothing is expected of a cancelled or completed project, so nothing about
    it can be late — its chip is a plain distance in the neutral tone."""
    b = typical(tmp_path)
    delta = [line for line in rows_of(b) if "Delta" in line][0]
    assert "▲" not in delta
    assert "-9d" in delta


def test_the_lane_names_its_next_due_work_soonest_first(tmp_path):
    b = typical(tmp_path)
    out = rows_of(b)
    i_late = next(i for i, line in enumerate(out) if "Fix the ingest path" in line)
    i_next = next(i for i, line in enumerate(out) if "Write the v2 reference" in line)
    i_atlas = next(i for i, line in enumerate(out) if "Atlas" in line)
    assert i_atlas < i_late < i_next
    assert not any("Ship the migration" in line for line in out)   # done work is not named


def test_a_named_task_carries_its_phase_as_a_climbing_dot(tmp_path):
    """One cell, and the dot CLIMBS as the task advances — the second variable
    goes to the glyph, never to a second hue."""
    b = typical(tmp_path)
    out = rows_of(b)
    doing = next(line for line in out if "Fix the ingest path" in line)
    backlog = next(line for line in out if "Write the v2 reference" in line)
    assert phase_glyph({1}) in doing
    assert phase_glyph({0}) in backlog
    assert phase_glyph({0}) != phase_glyph({1})


# --------------------------------------------------------------------------- #
# the ration, inside this view
# --------------------------------------------------------------------------- #
def test_severity_has_exactly_one_seat_and_a_date_wears_it(tmp_path):
    """verify_prism MANDATE: every span painted in `over` must be a date
    distance. Painting a project's name or its field red turns this red."""
    b = typical(tmp_path)
    text = render_swimlanes(b, False, None, TODAY, width=96, height=30)
    worn = [text.plain[s.start:s.end].strip() for s in text.spans
            if HEX["over"] in str(s.style)]
    assert worn, "vacuous: nothing was painted in the severity hue"
    for seg in worn:
        assert re.fullmatch(r"▲\d+d|\d+ due", seg), f"severity worn by {seg!r}"


def test_the_field_behind_today_is_ash_and_the_lattice_is_never_void(tmp_path):
    b = typical(tmp_path)
    m = markup_of(b)
    assert HEX["ash"] in m
    assert "·" in m


# --------------------------------------------------------------------------- #
# navigation follows what is drawn
# --------------------------------------------------------------------------- #
def test_navigation_walks_exactly_the_tasks_the_view_names(tmp_path):
    """A cursor that can land on something the view does not draw is a bug the
    user experiences as 'the selection vanished'."""
    for make in (typical, extreme):
        b = make(tmp_path)
        cols = nav_model("swimlanes", b, False, TODAY)
        assert len(cols) == 1
        drawn = [t.id for lane in lanes_of(b, False, TODAY)
                 for t in lane_titles(lane, LANE_TITLES)]
        assert cols[0] == drawn
        # and the view really does name FEWER tasks than the lanes hold open,
        # so "walks what is drawn" is a different claim from "walks everything"
        if make is extreme:
            assert len(drawn) < sum(len(l.open) for l in lanes_of(b, False, TODAY))
        out = rows_of(b)
        for tid in cols[0]:
            assert any(b.task_by_id(tid).title[:12] in line for line in out)


def test_the_line_map_points_at_the_row_that_names_the_task(tmp_path):
    b = typical(tmp_path)
    lm = {}
    out = rows_of(b, line_map=lm)
    assert lm
    for tid, idx in lm.items():
        assert b.task_by_id(tid).title[:12] in out[idx]


def test_the_selected_task_is_marked_in_its_own_row(tmp_path):
    b = typical(tmp_path)
    target = next(t for t in b.tasks if t.title == "Write the v2 reference")
    text = render_swimlanes(b, False, target.id, TODAY, width=96, height=30)
    reversed_spans = [text.plain[s.start:s.end] for s in text.spans
                      if "reverse" in str(s.style)]
    assert any("Write the v2 reference" in seg for seg in reversed_spans)


def test_the_inbox_is_a_lane_of_its_own(tmp_path):
    """Tasks with no project were in the old view and must not fall out of the
    new one (PROPOSAL R6 left this open; the port keeps them)."""
    b = typical(tmp_path)
    b.tasks.append(Task("Loose thing", None, "Backlog", "normal", due_date=iso(2)))
    out = rows_of(b)
    assert any("Inbox" in line for line in out)
    assert any("Loose thing" in line for line in out)


def test_lanes_and_titles_do_not_change_between_two_identical_renders(tmp_path):
    b = typical(tmp_path)
    assert rows_of(b) == rows_of(b)


# --------------------------------------------------------------------------- #
# the three loads the audit measured — calm, typical, extreme
# --------------------------------------------------------------------------- #
def calm(tmp_path):
    b = board(tmp_path, "calm.json")
    p = Project("Quiet", "sky", "on_track", due_date=iso(30))
    b.projects.append(p)
    b.tasks.append(Task("One thing", p.id, "Backlog", "normal", due_date=iso(9)))
    return b


def extreme(tmp_path):
    b = board(tmp_path, "extreme.json")
    for i in range(8):
        p = Project(f"Project {i}", ["lime", "green", "sky", "blue", "indigo",
                                     "violet", "fuchsia", "pink"][i],
                    ["on_track", "paused", "cancelled", "completed"][i % 4],
                    due_date=iso(i * 7 - 14))
        b.projects.append(p)
        for k in range(5):
            b.tasks.append(Task(f"Task {i}-{k}", p.id,
                                ["Backlog", "Doing", "Done"][k % 3],
                                "high" if k == 0 else "normal",
                                due_date=iso(k * 6 - 12)))
    return b


def test_all_three_loads_render_width_exact_and_lose_no_project(tmp_path):
    """The three fixtures AUDIT.md measured. Every project keeps a row at every
    step — the old view's `N more` collapse is gone, and nothing may replace it
    with a silent drop."""
    for make, n_projects in ((calm, 1), (typical, 4), (extreme, 8)):
        b = make(tmp_path)
        for w, h in ((72, 24), (96, 30), (130, 44)):
            out = rows_of(b, w, h)
            assert all(len(line) == w for line in out), f"{make.__name__} {w}x{h}"
            assert len(lane_rows(out)) == n_projects, f"{make.__name__} {w}x{h}"


def test_a_project_with_no_open_work_still_gets_its_row(tmp_path):
    """The resting state is DESIGNED in the next increment; until then it must
    at least not vanish."""
    b = board(tmp_path, "rest.json")
    p = Project("Done and dusted", "green", "completed", due_date=iso(-3))
    b.projects.append(p)
    b.tasks.append(Task("Finished", p.id, "Done", "normal", due_date=iso(-5)))
    out = rows_of(b, 96, 30)
    assert len(lane_rows(out)) == 1
    assert any("Done and" in line for line in out)      # clipped, with a visible …
    assert any("…" in line for line in lane_rows(out))
