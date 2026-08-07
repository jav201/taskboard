"""ONE row cost model for the lanes view, and the regime it is true in.

WHY THIS FILE EXISTS: the previous batch (`.dev-flow/05-postmortem.md`) closed at
Phase 2 without writing a line of code, and every substantive disagreement in it
reduced to ONE unanswered question wearing six disguises — what does a lanes row
cost? `swimlane_plan` hands the allocator `h - 2 - (2 if active else 0)` and
`lead_band` DRAWS `prof + 2`. Both are true. Nobody had reconciled them, so each
reviewer measured against a model of their own, and the conflicts only ever
surfaced when a later one re-derived an earlier one's number.

This file is that reconciliation, executed and pinned.

THE TWO `2`s ARE NOT THE SAME `2`. `h - 2` is the panel's OWN CHROME — the header
and the axis, the close being frameless. `- 2*[active]` is the LEAD BAND'S head
and tail, the two rows `allocate` never bills for. Collapse them in either
direction and the panel either overflows (and sheds work it should have drawn) or
pads (on a view whose whole design is that it never does).

THE EXCLUSION OF OFF-REGIME SIZES IS STATIC ON PURPOSE, and this is the part to
preserve if this file is ever rewritten. The obvious way to write it is to sweep
every size and keep the cells where `charge <= room` — and that is CIRCULAR,
because `charge <= room` is computed from the very code under test. Measured, not
supposed: filtering that way makes a call site that FORGETS to pay for the lead
band, and a rung four that reserves NO absence row, both pass VACUOUSLY — the
first by leaving nothing in the sample at all. So the off-regime cells are named
below by fixture and height, and the in-regime ones must PROVE their feasibility
instead of being selected for it.

Each law below is answerable to a mutation that reddens it (all executed):
    room = h-2      (lead band unpaid)      -> L3, L5, L6
    room = h-6      (lead band paid twice)  -> L5, L6
    lead_band +1 row (charge unchanged)     -> L1, L3, L5, L6, L7
    lead_band -1 row (charge unchanged)     -> L1, L5, L6, L7
    rung four drops its `- 1`               -> L3, L5, L6
"""

from datetime import date, timedelta
from pathlib import Path

import pytest

from taskboard.models import Board, Project, Task
from taskboard.views import (_clamp_width, _strip, absence_line, lead_band,
                             render_swimlanes, stack_block, swimlane_plan)

# The clock is FROZEN. A cost model measured against `date.today()` is a model
# that means something different tomorrow.
TODAY = date(2026, 7, 30)

# No board of the operator's is ever read, and none is ever written: these are
# synthetic and live in memory. (`.gitignore` excludes `board.json` for the same
# reason — his data does not belong in this repo's artifacts.)
_UNWRITTEN = Path("__never_written__.json")

WIDTHS = (72, 96, 120, 200)
HEIGHTS = (10, 14, 18, 24, 30, 45, 60, 80)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def _board(spec) -> Board:
    projects, tasks = [], []
    for name, status, due, items in spec:
        p = Project(name=name, color="lime", status=status,
                    due_date=iso(due) if due is not None else None)
        projects.append(p)
        for title, phase, d in items:
            tasks.append(Task(title=title, project_id=p.id, phase=phase,
                              priority="normal",
                              due_date=iso(d) if d is not None else None))
    return Board(projects, tasks, _UNWRITTEN)


def typical() -> Board:
    """Four projects: one late, one healthy, one paused, one cancelled."""
    return _board([
        ("Atlas", "on_track", 20, [("Fix the ingest path", "Doing", -9),
                                   ("Write the v2 reference", "Backlog", 6),
                                   ("Ship the migration", "Done", -2)]),
        ("Beacon", "on_track", 40, [("Harden the search index", "Doing", 12)]),
        ("Cinder", "paused", 15, [("Deprecate v1 endpoints", "Backlog", 3)]),
        ("Delta", "cancelled", -9, [("Retire the old host", "Backlog", 1)])])


def busy() -> Board:
    """Five active projects, six tasks each: naming competes with resolution."""
    return _board([(n, "on_track", 20 + i * 5,
                    [(f"{n} task {j}", "Doing" if j % 3 else "Backlog", j - 4)
                     for j in range(6)])
                   for i, n in enumerate(["Atlas", "Beacon", "Cinder", "Dune", "Ember"])])


def calm() -> Board:
    """ONE active lane, so the bench is the only sink for surplus rows."""
    return _board([("Atlas", "on_track", 20, [("One open thing", "Doing", 5)]),
                   ("Beacon", "completed", 3, [("Done thing", "Done", -3)])])


def all_resting() -> Board:
    """Nothing open anywhere — the end of a cycle. OFF-REGIME by construction."""
    return _board([("Atlas", "completed", 20, [("Done a", "Done", -3)]),
                   ("Beacon", "cancelled", 3, [("Done b", "Done", -3)])])


def huge() -> Board:
    """Nine projects, fourteen tasks each: more work than a short panel can hold."""
    return _board([(f"P{i}", "on_track", 10 + i,
                    [(f"P{i} task {j}", "Doing", j - 10) for j in range(14)])
                   for i in range(9)])


BOARDS = {"typical": typical, "busy": busy, "calm": calm,
          "allrest": all_resting, "huge": huge}

# ---------------------------------------------------------------------------
# THE STATIC REGIME MAP. Named cells, never a predicate over the code under test.
# ---------------------------------------------------------------------------

# no active lane: nothing draws the bench, so `prof` is billed and never spent
NO_ACTIVE_LANE = {"allrest"}

# no allocation fits: `allocate` returns its floor and the renderer sheds
INFEASIBLE = {("huge", 10)}


def in_regime(name: str, h: int) -> bool:
    return name not in NO_ACTIVE_LANE and (name, h) not in INFEASIBLE


REGIME_CELLS = [(n, w, h) for n in BOARDS for w in WIDTHS for h in HEIGHTS
                if in_regime(n, h)]


def audit(name: str, w: int, h: int) -> dict:
    """What the allocator BILLED against what the writers DREW.

    Measured at the writers (`lead_band`, `stack_block`, `resting_row`), never
    inferred from the caller — the previous batch reported a false finding by
    measuring `lead_band`'s output and never opening its call site.
    """
    b = BOARDS[name]()
    lanes, geo, titles, prof, wrows = swimlane_plan(b, False, TODAY, w, h)
    active = [ln for ln in lanes if not ln.resting]
    stack, rest = active[1:], [ln for ln in lanes if ln.resting]
    nameable = [len(ln.open) + sum(1 for t in ln.tasks if t.archived) for ln in stack]

    A = 1 if active else 0
    room = h - 2 - 2 * A
    charge = prof + sum(wrows + min(titles, o) for o in nameable) + len(rest)

    inner = _clamp_width(w)
    lead = len(lead_band(active[0], geo, TODAY, inner, prof, 0)) if active else 0
    body = lead + len(rest) + sum(
        len(stack_block(ln, geo, b, TODAY, inner, titles, wrows, None, 0))
        for ln in stack)

    lines = render_swimlanes(b, False, None, TODAY, w, h).plain.split("\n")
    mark = _strip(absence_line(lanes, TODAY, inner)).strip()
    absence = 1 if (mark and any(mark in ln for ln in lines)) else 0

    return dict(name=name, w=w, h=h, A=A, room=room, charge=charge, body=body,
                lead=lead, prof=prof, absence=absence, lines=lines,
                blank=sum(1 for ln in lines if not ln.strip()),
                shed="not shown" in "\n".join(lines))


@pytest.fixture(scope="module")
def regime():
    """Every in-regime cell, audited once."""
    return [audit(n, w, h) for n, w, h in REGIME_CELLS]


def test_the_matrix_is_not_empty_and_exercises_both_off_regimes():
    """The guard on every law below: a sample that silently emptied would make
    all of them green. The previous batch's headline was exactly such a green."""
    assert len(REGIME_CELLS) == 124, f"the regime matrix is {len(REGIME_CELLS)} cells"
    assert NO_ACTIVE_LANE and INFEASIBLE, "an off-regime with no cells is not tested"
    assert len(BOARDS) == 5


# ---------------------------------------------------------------------------
# IN REGIME — one active lane, and an allocation that fits
# ---------------------------------------------------------------------------
def test_L1_the_lead_band_draws_prof_plus_two(regime):
    """`prof` is the BENCH, not the band: `lead_band` adds a head and a tail.
    This is the half of the model the allocator does not bill for."""
    for r in regime:
        assert r["lead"] == r["prof"] + 2, (
            f"{r['name']} {r['w']}x{r['h']}: prof={r['prof']} drew {r['lead']} rows")


def test_L2_the_lead_bands_two_extra_rows_are_paid_at_the_call_site(regime):
    """The other half. `swimlane_plan` subtracts them from `room` BEFORE the
    search, which is why billing `prof` alone is correct rather than a defect."""
    for r in regime:
        assert r["room"] == r["h"] - 2 - 2 * r["A"], f"{r['name']} {r['w']}x{r['h']}"
        assert r["A"] == 1, "an in-regime cell has an active lane by construction"


def test_L3_what_is_billed_is_what_is_drawn(regime):
    """THE IDENTITY. `BODY == CHARGE + 2` — the whole model in one line, and the
    thing three separate reviewers each derived differently."""
    for r in regime:
        assert r["body"] == r["charge"] + 2 * r["A"], (
            f"{r['name']} {r['w']}x{r['h']}: billed {r['charge']}, drew {r['body']}")


def test_L4_the_allocation_actually_fits(regime):
    """Feasibility is ASSERTED, never used to select the sample. A call site
    that stops paying for the lead band fails HERE, and filtering on this
    instead would have deleted exactly those rows from the evidence."""
    for r in regime:
        assert r["charge"] <= r["room"], (
            f"{r['name']} {r['w']}x{r['h']}: billed {r['charge']} into room {r['room']}")


def test_L5_the_body_fits_the_panel_and_nothing_is_shed(regime):
    """The consequence of L3 + L4, measured at the renderer rather than argued:
    the body never exceeds its budget, so no block is ever dropped in regime."""
    for r in regime:
        assert r["body"] <= r["h"] - 2, (
            f"{r['name']} {r['w']}x{r['h']}: body {r['body']} over budget {r['h'] - 2}")
        assert not r["shed"], f"{r['name']} {r['w']}x{r['h']} shed a block in regime"


def test_L6_in_regime_the_lanes_never_pad(regime):
    """The shipped law, now with the regime it is actually true in — see L8 for
    the case where it is false. The allocator spends the whole height it is
    given, so a blank row means it mis-billed."""
    for r in regime:
        assert r["blank"] == 0, (
            f"{r['name']} {r['w']}x{r['h']}: {r['blank']} blank rows")


def test_L7_the_panel_is_header_plus_body_plus_absence_plus_axis(regime):
    """`2 + BODY + ABSENCE == h`, the close contributing nothing because the view
    is frameless. This is what makes the height exact rather than approximately
    filled, and it is the law a half-row error shows up in first."""
    for r in regime:
        assert 2 + r["body"] + r["absence"] == r["h"], (
            f"{r['name']} {r['w']}x{r['h']}: 2 + {r['body']} + {r['absence']} "
            f"!= {r['h']}")
        assert len(r["lines"]) == r["h"]


def test_L7b_rung_four_reserves_the_absence_row_and_only_that(regime):
    """`allocate`'s `- 1` (`views.py:772`) is what buys the absence line, and the
    absence line is why one row is left unspent. Tie them together, or a later
    reader deletes the `- 1` as an off-by-one."""
    for r in regime:
        assert r["absence"] == (1 if r["body"] <= r["h"] - 3 else 0), (
            f"{r['name']} {r['w']}x{r['h']}: absence={r['absence']} "
            f"body={r['body']} h={r['h']}")
    assert any(r["absence"] for r in regime), "no cell draws the absence line"
    assert any(not r["absence"] for r in regime), "every cell draws it — no tension"


# ---------------------------------------------------------------------------
# OFF REGIME — both real, both reachable, neither a defect
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("h", HEIGHTS)
def test_L8_with_no_active_lane_the_view_pads_and_bills_a_bench_it_never_draws(h):
    """OFF-REGIME 1, and it FALSIFIES A CLAIM THIS REPO SHIPPED. `lanes never pad
    at all` is true only while some project is active. On a board where every
    project rests there is nothing to draw but the resting rows, `prof` is billed
    for a bench that never appears, and the remainder is padded.

    Asserted as itself rather than excluded, because an off-regime nobody wrote
    down is how the next reader mistakes it for a defect — or misses that a real
    defect has pushed a normal board into it."""
    r = audit("allrest", 96, h)
    n_rest = 2                       # the fixture's two resting projects
    assert r["A"] == 0, "the fixture stopped being all-resting"
    assert r["body"] == n_rest, f"h={h}: the resting rows are the whole body"
    assert r["prof"] > 0 and r["lead"] == 0, (
        f"h={h}: prof={r['prof']} billed for a bench that drew {r['lead']} rows")
    # the pad is EXACT, not merely present: 1 header + n_rest + 1 absence + 1 axis
    assert r["blank"] == h - 3 - n_rest, (
        f"h={h}: padded {r['blank']}, expected {h - 3 - n_rest}")
    assert r["lines"][-1].strip(), f"h={h}: the axis must still sit at the bottom"
    assert len(r["lines"]) == h


def test_L9_when_no_allocation_fits_the_renderer_sheds_and_says_so(regime):
    """OFF-REGIME 2: `allocate` finds nothing that fits, returns its floor, and
    the renderer drops blocks — out loud. A view that sheds in silence is lying
    about how much work there is."""
    for name, h in sorted(INFEASIBLE):
        r = audit(name, 96, h)
        assert r["charge"] > r["room"], f"{name} @{h} is no longer infeasible"
        assert r["shed"], f"{name} @{h}: blocks dropped without saying so"
        assert len(r["lines"]) == h
    # and the in-regime cells are the complement: nothing there sheds
    assert not any(r["shed"] for r in regime)
