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
    """The stacked PROJECT rows — a named lane, not one of the task rows under
    it (those carry the same spine but two spaces before their phase glyph)."""
    return [line for line in out if line.startswith("▎ ") and line[2] != " "]


def resting_rows(out: list[str]) -> list[str]:
    """Lanes with nothing open: the thin spine."""
    return [line for line in out if line.startswith("▏ ")]


def lead_head(out: list[str]) -> str:
    """The leader's band opens with the heavy spine and a shouted name."""
    return next(line for line in out if line.startswith("▌ "))


def project_blocks(out: list[str]) -> int:
    """Every project on screen, in whichever of its three forms it took."""
    return (len(lane_rows(out)) + len(resting_rows(out))
            + sum(1 for line in out if line.startswith("▌ ")))


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
            body = line                       # drop the frame borders
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
    geo = lane_geometry(96, 30)
    col = geo.label_w + geo.today_dc // 2          # +1 for the frame border
    out = rows_of(b, 96, 30)
    fielded = [line for line in out
               if len(line) > col and (line[col] == RULE
                                       or 0x2800 <= ord(line[col]) <= 0x28FF)]
    assert len(fielded) >= 4        # the lead's band rows plus the stacked lanes
    assert len(lane_rows(out)) >= 2
    for line in lane_rows(out):
        ch = line[col]
        assert ch == RULE or 0x2800 <= ord(ch) <= 0x28FF, f"{ch!r} at the today column"
    assert any(line[col] == RULE for line in out)   # the rule shows where uncovered


def test_a_project_whose_work_runs_off_the_window_is_marked_not_crushed(tmp_path):
    """PROPOSAL §4.2 / R3. The window narrows as the widget shrinks; what falls
    outside is FLAGGED at the edge instead of being piled onto the last column."""
    b = board(tmp_path, "far.json")
    near = Project("Near", "sky", "on_track", due_date=iso(-1))
    far = Project("Far", "lime", "on_track", due_date=iso(400))
    b.projects += [near, far]
    b.tasks += [Task("An overdue thing", near.id, "Doing", "normal", due_date=iso(-3)),
                Task("A very distant thing", far.id, "Backlog", "normal",
                     due_date=iso(400))]
    lane = next(line for line in lane_rows(rows_of(b, 40, 20)) if "Far" in line)
    assert "▸" in lane


# --------------------------------------------------------------------------- #
# what the row says
# --------------------------------------------------------------------------- #
def test_a_stacked_row_ends_in_its_due_meter(tmp_path):
    """Was: `0/1` and `+40d`. The whole `n/N !N ▲Nd` group collapsed into the
    six-cell meter — `n/N` because the project's own wave already draws its
    progress, and a figure repeating the field beside it is the duplication this
    edge exists to remove; `!N` moved to the leader's band, where a digit earns
    its cells. LENGTH IS THE TIME THAT REMAINS, so short means act now."""
    b = typical(tmp_path)
    lane = next(line for line in lane_rows(rows_of(b)) if "Beacon" in line)
    assert "0/1" not in lane and "+40d" not in lane
    assert lane[-6:].strip()                 # the six cells are drawn
    assert re.fullmatch(r"·*(▲?\d+d\+?|today|done|—)", lane[-6:]), lane[-6:]


def test_the_leader_is_the_project_under_the_most_pressure(tmp_path):
    """THE ORDER IS THE HIERARCHY: the reader is not asked to scan for the
    project that needs them. The pressured project is added LAST here on
    purpose — insertion order must not be able to fake this."""
    b = board(tmp_path, "rank.json")
    calm1 = Project("Calm one", "sky", "on_track", due_date=iso(60))
    calm2 = Project("Calm two", "blue", "on_track", due_date=iso(70))
    burning = Project("Burning", "lime", "on_track", due_date=iso(5))
    b.projects += [calm1, calm2, burning]
    b.tasks += [
        Task("Something later", calm1.id, "Backlog", "normal", due_date=iso(30)),
        Task("Something else", calm2.id, "Backlog", "normal", due_date=iso(40)),
        Task("The fire", burning.id, "Doing", "normal", due_date=iso(-11)),
    ]
    out = rows_of(b)
    assert "BURNING" in lead_head(out)
    assert "1 open" in lead_head(out)
    assert "▲11d" in lead_head(out)             # severity, worn by a date distance
    assert b.projects.index(burning) == 2       # and it was NOT first in the data


def test_the_leader_gets_a_drawn_field_that_ends_at_its_own_due_date(tmp_path):
    """The bench is the one figure on this screen ≥ 4 rows tall, and it STOPS at
    the project's own date: the air left above the curve before that `◆` is the
    work that cannot land in time."""
    b = typical(tmp_path)
    out = rows_of(b, 96, 30)
    head = out.index(lead_head(out))
    # Take the bench the ALLOCATOR actually granted. A hardcoded window was a
    # constant pretending to be a law: once the wave ceiling became room-aware
    # the lead's bench shortened, and the fixed slice spilled into the next
    # lane's curve — failing this test with another project's ink.
    from taskboard.views import swimlane_plan
    _l, _g, _t, prof, _w = swimlane_plan(b, False, TODAY, 96, 30)
    band = out[head + 1:head + 1 + prof]
    drawn = [line for line in band if any(0x2800 <= ord(ch) <= 0x28FF for ch in line)]
    assert len(drawn) >= 4

    # the diamond marks Atlas's OWN date (+20d), so it must sit near today, far
    # from the right edge — a bench that ran to the edge would also show a ◆
    from taskboard.views import lane_geometry, lanes_of, wave_edge
    geo = lane_geometry(96, 30)
    lane = next(ln for ln in lanes_of(b, False, TODAY) if ln.name == "Atlas")
    want = geo.label_w + min(geo.field_w - 1, wave_edge(lane, geo, TODAY) // 2 + 1)
    row = next(line for line in band if "◆" in line)
    assert row.index("◆") == want
    assert want < geo.label_w + geo.field_w - 3         # not pinned to the edge
    # and nothing of the bench is drawn beyond it
    for line in drawn:
        assert not any(0x2800 <= ord(ch) <= 0x28FF and ch != "⠀"
                       for ch in line[want + 1:])


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
    assert "▲" not in delta                    # nothing about it may be judged
    assert "⣤" in delta or "·" in delta[-7:]    # a spent or unmeasured edge


def test_the_lane_names_its_next_due_work_soonest_first(tmp_path):
    b = typical(tmp_path)
    b.tasks.append(Task("Rotate the signing keys", b.projects[1].id, "Backlog",
                        "normal", due_date=iso(4)))
    out = rows_of(b)
    i_lane = next(i for i, line in enumerate(out) if "Beacon" in line)
    i_soon = next(i for i, line in enumerate(out) if "Rotate the signing keys" in line)
    i_late = next(i for i, line in enumerate(out) if "Harden the search index" in line)
    assert i_lane < i_soon < i_late              # +4d named before +12d
    assert not any("Ship the migration" in line for line in out)   # done work is not named


def test_a_named_task_carries_its_phase_as_a_climbing_dot(tmp_path):
    """One cell, and the dot CLIMBS as the task advances — the second variable
    goes to the glyph, never to a second hue."""
    b = typical(tmp_path)
    b.tasks.append(Task("Rotate the signing keys", b.projects[1].id, "Doing",
                        "normal", due_date=iso(4)))
    out = rows_of(b)
    doing = next(line for line in out if "Rotate the signing keys" in line)
    backlog = next(line for line in out if "Deprecate v1 endpoints" in line)
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
        # a date distance, the header's count, or the meter's ONE alert glyph
        assert re.fullmatch(r"▲\d+d|\d+ due|▲", seg), f"severity worn by {seg!r}"


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
        for w, h in ((96, 30), (72, 24)):
            cols = nav_model("swimlanes", b, False, TODAY, width=w, height=h)
            assert len(cols) == 1
            out = rows_of(b, w, h)
            for tid in cols[0]:
                title = b.task_by_id(tid).title
                assert any(title[:12] in line for line in out), \
                    f"{w}x{h}: nav points at {title!r}, which is not drawn"
            # every NAMED task is reachable — nothing drawn is unselectable
            named = [t.id for t in b.tasks
                     if any(t.title[:12] in line for line in out)
                     and not b.is_done(t)]
            assert set(cols[0]) <= set(named)
        if make is extreme:      # the view names fewer than it holds open, so
            lanes = lanes_of(b, False, TODAY)   # "walks what is drawn" is a
            cols = nav_model("swimlanes", b, False, TODAY, width=96, height=30)
            assert len(cols[0]) < sum(len(l.open) for l in lanes)   # real claim


def test_the_line_map_points_at_the_row_that_names_the_task(tmp_path):
    b = typical(tmp_path)
    lm = {}
    out = rows_of(b, line_map=lm)
    assert lm
    for tid, idx in lm.items():
        assert b.task_by_id(tid).title[:12] in out[idx]


def test_the_selected_task_is_marked_in_its_own_row(tmp_path):
    b = typical(tmp_path)
    target = next(t for t in b.tasks if t.title == "Harden the search index")
    text = render_swimlanes(b, False, target.id, TODAY, width=96, height=30)
    reversed_spans = [text.plain[s.start:s.end] for s in text.spans
                      if "reverse" in str(s.style)]
    assert any("Harden the search index" in seg for seg in reversed_spans)


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
            assert project_blocks(out) == n_projects, f"{make.__name__} {w}x{h}"


def test_nothing_is_ever_dropped_in_silence(tmp_path):
    """When the height cannot hold every project, the ones that did not fit are
    COUNTED. A view that silently shows fewer rows tells the reader there is
    less work than there is."""
    b = extreme(tmp_path)
    tall, short = rows_of(b, 96, 44), rows_of(b, 96, 12)
    assert project_blocks(short) < project_blocks(tall)
    assert any("not shown" in line for line in short)
    assert not any("not shown" in line for line in tall)


def test_a_project_with_nothing_open_rests(tmp_path):
    """The resting row is DESIGNED, not inherited: one row, a thin spine, the
    quiet step, and it still says what it is and what it finished."""
    b = typical(tmp_path)
    p = Project("Done and dusted", "green", "completed", due_date=iso(-3))
    b.projects.append(p)
    b.tasks.append(Task("Finished", p.id, "Done", "normal", due_date=iso(-5)))
    out = rows_of(b, 96, 30)
    rest = resting_rows(out)
    assert len(rest) == 1
    assert "Done and" in rest[0]
    assert "1/1 done" in rest[0]
    assert "completed" in rest[0]
    assert "▎" not in rest[0]           # the thin spine, not the lane spine


def test_resting_lanes_sink_below_the_working_ones(tmp_path):
    b = typical(tmp_path)
    p = Project("Done and dusted", "green", "completed", due_date=iso(-3))
    b.projects.append(p)
    b.tasks.append(Task("Finished", p.id, "Done", "normal", due_date=iso(-5)))
    out = rows_of(b, 96, 30)
    assert out.index(resting_rows(out)[0]) > out.index(lane_rows(out)[-1])


def test_the_allocator_spends_the_height_it_is_given(tmp_path):
    """Space is information-proportional in BOTH directions: a taller widget
    names more work and draws a taller bench, and it never overflows."""
    b = extreme(tmp_path)
    from taskboard.views import swimlane_plan
    # SAME width and same size step (both >= 26 rows, so the geometry's own
    # floors are identical) — only the allocator's search can differ here.
    short = swimlane_plan(b, False, TODAY, 96, 28)
    tall = swimlane_plan(b, False, TODAY, 96, 44)
    assert short[1].large and tall[1].large
    assert (tall[2], tall[3]) >= (short[2], short[3])       # titles, lead rows
    assert tall[2] > short[2] or tall[3] > short[3]
    for h in range(12, 46):
        assert len(rows_of(b, 96, h)) == h


# --------------------------------------------------------------------------- #
# the due meter — the right edge (REV4/REV5 #18)
# --------------------------------------------------------------------------- #
def test_the_edge_states_the_distance_exactly(tmp_path):
    """REVERSED DELIBERATELY, and the reason is measurable.

    This law used to read: "LENGTH IS THE TIME THAT REMAINS, so a SHORT bar means
    act now. Triage is pre-attentive: nobody reads a number to tell overdue from
    distant." The bar was kept for a while on that argument and then failed the
    only test that matters, which is use: it stood for a BAND, so four days and
    five days drew the SAME two cells. The one column whose whole job is "how
    long have I got" was answering in buckets.

    A number costs the same six cells and separates them. What survives from the
    old law is everything that was actually load-bearing: the edge is exactly
    METER_W wide whatever it says, and severity still gets one seat."""
    from taskboard.views import METER_W, due_meter

    def read(days, done=False):
        return "".join(g for g, _ in due_meter(days, done=done)).strip("·")

    assert read(4) == "4d" and read(5) == "5d"     # the band drew these the same
    assert read(0) == "today"
    assert read(-3) == "▲3d"
    assert read(None, done=True) == "done"
    assert read(None) == "—"

    # the alert cap keeps its single seat, and the count beside it stays neutral
    overdue = due_meter(-3, done=False)
    assert overdue[-3] == ("▲", "over")
    assert {tone for g, tone in overdue[-2:]} == {"mut"}

    # and the edge spends exactly its width, so the right margin never goes ragged
    for days in (None, -999999, -3, 0, 1, 7, 40, 400, 999999):
        assert len(due_meter(days, done=False)) == METER_W, days



def test_the_meter_is_categorical_not_linear(tmp_path):
    """REVERSED, and this is the law that changed hands. It used to read: "a
    linear scale would spend all its resolution on a distant future where
    nothing is decided — so two dates in the same band draw the same mark." The
    banding was the point, and the cost only shows up in use: the edge could not
    tell THIS Thursday from NEXT Thursday, which is the distinction the column
    exists to make. It now says the count, so every distance is its own reading."""
    from taskboard.views import due_meter
    assert due_meter(3, done=False) != due_meter(7, done=False)        # was equal
    assert due_meter(40, done=False) != due_meter(300, done=False)     # was equal
    assert due_meter(3, done=False) != due_meter(20, done=False)


def test_finished_work_is_the_whole_meter_in_ash_and_wordless(tmp_path):
    from taskboard.views import due_meter
    # ONE TONE still, ground included — finished work must not read as live work.
    # It is no longer wordless: the edge says what it is, which is the change.
    assert {t for _g, t in due_meter(-99, done=True)} == {"ash"}
    assert "".join(g for g, _t in due_meter(-99, done=True)).strip("·") == "done"


def test_undated_work_is_measured_as_nothing_not_as_late(tmp_path):
    from taskboard.views import due_meter
    assert {t for _g, t in due_meter(None, done=False)} == {"dim"}


def test_overdue_lights_the_one_alert_glyph_and_nothing_else(tmp_path):
    """Severity keeps its single seat: the `▲` cap, the same glyph the chip used."""
    from taskboard.views import HEX, due_meter
    cells = due_meter(-5, done=False)
    # the reading is right-aligned now, so the cap sits before the count rather
    # than at cell 0 — what the law is about is that there is exactly ONE seat
    assert ("▲", "over") in cells
    assert [t for _g, t in cells].count("over") == 1
    for days in (0, 3, 20, 200, None):
        assert "over" not in [t for _g, t in due_meter(days, done=False)]


def test_the_meter_answers_when_never_whose(tmp_path):
    """The census caught the first version painting it in each project's hue:
    the right edge went from 6 tones to 8 because it carried one per project.
    Identity already travels in the spine at the other end of the same row, so
    the edge stays neutral however many projects the board holds."""
    from taskboard.models import PROJECT_COLORS
    from taskboard.views import HEX, due_meter
    neutral = {"ash", "mut", "accent", "over", "dim"}
    tones = set()
    for days in (-30, -1, 0, 1, 7, 8, 31, 32, 400, None):
        for done in (False, True):
            tones |= {t for _g, t in due_meter(days, done=done)}
    assert tones <= neutral
    assert not (tones & set(PROJECT_COLORS))


def test_the_edge_keeps_its_tone_count_whatever_the_board_holds(tmp_path):
    """Three projects or thirty, the right band draws the same few tones."""
    import re
    from taskboard.models import PROJECT_COLORS
    from taskboard.views import HEX, _figures, lane_geometry, lanes_of
    def edge_tones(n):
        b = board(tmp_path, f"edge{n}.json")
        for i in range(n):
            p = Project(f"P{i}", PROJECT_COLORS[i % len(PROJECT_COLORS)],
                        "on_track", due_date=iso(i * 3 - 10))
            b.projects.append(p)
            b.tasks.append(Task(f"T{i}", p.id, "Doing", "normal", due_date=iso(i - 5)))
        geo = lane_geometry(96, 30)
        tones = set()
        for lane in lanes_of(b, False, TODAY):
            tones |= set(re.findall(r"#[0-9a-f]{6}", _figures(lane, geo.figs_w)))
        return tones
    few, many = edge_tones(3), edge_tones(24)
    # A bigger board reaches more of the FIVE fixed tones — it never invents a
    # sixth, and it never reaches for an identity hue. That is the whole claim:
    # the edge's palette is a constant, not a function of how many projects
    # exist. (The first version of the meter made it one, and the census caught
    # it going 6 tones -> 8.)
    neutral = {HEX[k] for k in ("ash", "mut", "accent", "over", "dim")}
    assert few <= neutral and many <= neutral
    assert len(many) <= 5
    assert not (many & {HEX[c] for c in PROJECT_COLORS})


def test_the_lane_row_ends_in_the_meter_at_every_width(tmp_path):
    b = typical(tmp_path)
    for w in (48, 72, 96, 130):
        for line in lane_rows(rows_of(b, w, 30)):
            edge = line[-6:]
            assert re.fullmatch(r"·*(▲?\d+d\+?|today|done|—)", edge), f"{w}: {edge!r}"


def test_the_freed_band_went_to_the_field(tmp_path):
    """The measured outcome of this increment, stated as a number: the port's
    figures band reserved 13 (L) / 11 (S) for a group the meter replaced with
    six cells, and the field took the difference."""
    from taskboard.views import field_geometry, lane_geometry
    for w, h, gain in ((96, 30, 6), (72, 24, 4)):
        port, view = field_geometry(w - 2, h), lane_geometry(w - 2, h)
        assert view.figs_w == 7
        assert view.field_w - port.field_w == gain
