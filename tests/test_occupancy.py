"""Occupancy — the measurement the whole lanes rebuild was justified by.

`_tui_prism_proposal/AUDIT.md` measured the OLD lanes view driving the real app
headless, and the numbers are why it was rewritten. At 96x30, typical load:

    16.2 % of cells carried a datum · 13.4 % were frame · 70.4 % were dead,
    and 14 of 28 body rows were `│` + 94 spaces + `│`.

This file measures the SAME thing about the view that replaced it, and fails if
it ever slides back. The thresholds are FLOORS the view is committed to, set
below what it currently achieves so honest variation does not turn them red —
each one carries the measured value it was derived from, so the margin is
visible rather than implied.

Classification, deliberately explicit (a cell is exactly one of four):
  chrome — the box the view is drawn in
  ink    — a cell carrying a datum: text, a figure, a mark, the today rule
  field  — the drawn lattice: the ground that says spent vs still to spend
  dead   — blank
`ink + field` is what the proposal calls "cells with a mark", and it is the
number that matters: the field is drawn, not empty, and it carries a datum.
"""

from datetime import date, timedelta

from taskboard.models import Board, Project, Task
from taskboard.views import LATTICE, render_view

TODAY = date(2026, 7, 30)
W, H = 96, 30                      # the audit's reference size (wezterm.lua ships it)

FRAME_CHARS = set("╭─╮│╰╯├┤┬┴┼")   # every box character views.py draws

# --- AUDIT.md §1, the view this one replaced, same size, same method --------- #
BASELINE = {                       # (ink %, chrome %, dead %, mute body rows)
    "calm":    (6.5, 12.5, 81.0, 20),
    "typical": (16.2, 13.4, 70.4, 14),
    "extreme": (30.2, 14.2, 55.5, 8),
}


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def fixture(tmp_path, name: str, projects: int, tasks: int, late: int) -> Board:
    """The three loads AUDIT.md measured: calm 2/5, typical 5/21, extreme 8/44."""
    b = Board.load(str(tmp_path / f"{name}.json"))
    b.projects.clear()
    b.tasks.clear()
    hues = ["lime", "green", "sky", "blue", "indigo", "violet", "fuchsia", "pink"]
    per, k = tasks // projects, 0
    for i in range(projects):
        status = (["on_track", "on_track", "paused", "cancelled"][i % 4]
                  if projects > 2 else "on_track")
        p = Project(f"Project {i}", hues[i % 8], status, due_date=iso(6 + i * 9))
        b.projects.append(p)
        for j in range(per + (1 if i < tasks % projects else 0)):
            b.tasks.append(Task(
                f"Task {i}-{j} something real", p.id,
                ["Backlog", "Doing", "Done"][j % 3],
                "high" if j == 0 else "normal",
                due_date=iso(-(k % 12) - 1) if k < late else iso((k % 40) + 1),
                blocked=(k % 9 == 0 and k < 20)))
            k += 1
    return b


LOADS = {"calm": (2, 5, 0), "typical": (5, 21, 1), "extreme": (8, 44, 11)}


def census(lines: list[str]) -> dict:
    """Every cell counted exactly once, in one of four buckets."""
    ink = chrome = field = dead = 0
    for line in lines:
        for ch in line:
            if ch == " ":
                dead += 1
            elif ch in FRAME_CHARS:
                chrome += 1
            elif ch == LATTICE:
                field += 1
            else:
                ink += 1
    n = ink + chrome + field + dead
    return {"cells": n, "ink": 100 * ink / n, "chrome": 100 * chrome / n,
            "field": 100 * field / n, "dead": 100 * dead / n,
            "marked": 100 * (ink + field) / n}


def render(tmp_path, load: str, w: int = W, h: int = H) -> list[str]:
    b = fixture(tmp_path, load, *LOADS[load])
    return str(render_view("swimlanes", b, False, None, TODAY,
                           width=w, height=h)).split("\n")


def mute_rows(lines: list[str]) -> int:
    """Body rows that say nothing at all — the audit's headline defect: at
    typical load 14 of 28 rows were the frame and 94 spaces."""
    return sum(1 for line in lines[1:-1]
               if all(ch == " " or ch in FRAME_CHARS for ch in line))


# --------------------------------------------------------------------------- #
# the harness itself must be sound before its numbers mean anything
# --------------------------------------------------------------------------- #
def test_the_census_counts_every_cell_exactly_once(tmp_path):
    for load in LOADS:
        lines = render(tmp_path, load)
        assert len(lines) == H and all(len(line) == W for line in lines)
        cen = census(lines)
        assert cen["cells"] == W * H
        assert abs(cen["ink"] + cen["chrome"] + cen["field"] + cen["dead"] - 100) < 1e-9


def test_every_category_is_actually_populated(tmp_path):
    """Anti-vacuity: a classifier that put everything in one bucket would make
    every floor below meaningless."""
    cen = census(render(tmp_path, "typical"))
    for key in ("ink", "chrome", "field", "dead"):
        assert cen[key] > 0, f"{key} never occurs — the census is not classifying"


# --------------------------------------------------------------------------- #
# the floors the view is committed to
# --------------------------------------------------------------------------- #
# (marked floor, dead ceiling) — measured 2026-07-30, margin ~5 points each way
# Re-measured after the due meter freed 6 cells per row into the field (REV5 #18).
FLOORS = {
    "calm":    (29.0, 63.0),      # measured: marked 34.5, dead 57.9 (was 31.8/60.6)
    "typical": (43.0, 49.0),      # measured: marked 48.7, dead 43.7 (was 45.4/47.0)
    "extreme": (42.0, 50.0),      # measured: marked 47.4, dead 45.0 (was 44.7/47.8)
}


def test_the_view_holds_its_occupancy_floors(tmp_path):
    for load, (marked_floor, dead_ceiling) in FLOORS.items():
        cen = census(render(tmp_path, load))
        assert cen["marked"] >= marked_floor, \
            f"{load}: {cen['marked']:.1f} % marked, floor {marked_floor}"
        assert cen["dead"] <= dead_ceiling, \
            f"{load}: {cen['dead']:.1f} % dead, ceiling {dead_ceiling}"


def test_the_frame_is_the_only_chrome_and_it_stays_small(tmp_path):
    """The proposal's target was 0 % chrome, which is unreachable while the box
    survives — no increment was ever allocated to removing it. What IS committed
    is that chrome never grows back: it was 12.5-14.2 % and is now ~7.6 %."""
    for load in LOADS:
        cen = census(render(tmp_path, load))
        assert cen["chrome"] <= 10.0, f"{load}: chrome {cen['chrome']:.1f} %"
        assert cen["chrome"] < min(BASELINE[load][1] for load in BASELINE)


def test_no_row_of_the_working_view_says_nothing(tmp_path):
    """The defect this rebuild exists to fix. At typical load the old view spent
    14 of its 28 body rows on `fill_height` padding — a hole with a border
    around it, not the emptiness that isolates a hero."""
    assert mute_rows(render(tmp_path, "typical")) == 0
    assert mute_rows(render(tmp_path, "extreme")) == 0
    # calm is allowed to breathe, but not to be mostly hole (old: 20 of 28)
    assert mute_rows(render(tmp_path, "calm")) <= 14


# --------------------------------------------------------------------------- #
# the comparison that is the whole point
# --------------------------------------------------------------------------- #
def test_the_rebuild_beats_the_view_it_replaced_on_every_axis(tmp_path):
    """Against AUDIT.md's own numbers, at its own reference size, by its own
    method. This is the claim the rewrite was approved on, kept executable."""
    for load, (base_ink, base_chrome, base_dead, base_mute) in BASELINE.items():
        cen = census(render(tmp_path, load))
        assert cen["marked"] > base_ink, \
            f"{load}: {cen['marked']:.1f} % marked vs {base_ink} % before"
        assert cen["dead"] < base_dead, \
            f"{load}: {cen['dead']:.1f} % dead vs {base_dead} % before"
        assert cen["chrome"] < base_chrome, \
            f"{load}: {cen['chrome']:.1f} % chrome vs {base_chrome} % before"
        assert mute_rows(render(tmp_path, load)) < base_mute


# AUDIT.md §1 at the SMALL step (72x24): (ink %, chrome %, dead %)
BASELINE_SMALL = {"calm": (9.7, 16.0, 74.3), "typical": (23.0, 17.4, 59.5),
                  "extreme": (41.5, 18.9, 39.6)}


def test_growing_the_widget_costs_far_less_dead_space_than_it_used_to(tmp_path):
    """AUDIT.md §1's third reading: "wider is worse" — the old layout had no way
    to spend width, so stepping 72x24 -> 96x30 RAISED dead space at every load,
    by +6.7 (calm), +10.9 (typical) and +15.9 (extreme) points.

    It is NOT fully cured, and this test says so rather than hiding it: the field
    spends width, but the named-task rows are short strings that only gain blanks,
    so typical and extreme still drift up a little. What is committed is that the
    drift is strictly smaller than the old view's at every load."""
    for load in LOADS:
        small = census(render(tmp_path, load, 72, 24))["dead"]
        large = census(render(tmp_path, load, 96, 30))["dead"]
        was = BASELINE[load][2] - BASELINE_SMALL[load][2]
        now = large - small
        assert now < was, (f"{load}: dead grew {now:+.1f} points stepping up "
                           f"(the view this replaced grew {was:+.1f})")


def test_a_calm_board_now_gets_better_as_it_widens(tmp_path):
    """The inversion worth naming: on a quiet board the extra width goes into
    field, so growing the widget makes it emptier-looking no longer."""
    narrow = census(render(tmp_path, "calm", 72, 30))["dead"]
    wide = census(render(tmp_path, "calm", 130, 30))["dead"]
    assert wide < narrow, f"calm: {narrow:.1f} % -> {wide:.1f} % dead"


def test_the_proposals_own_45_percent_floor_is_now_met_at_both_loads(tmp_path):
    """PROPOSAL.md §4.3 sets "cells with a mark, typical/extreme load: >= 45 %".

    This test used to record a MISS: extreme sat at 44.7 %, 0.3 points short.
    The due meter cured it without anyone aiming at it — collapsing the 13-cell
    figures band to a 6-cell mark gave the field six more cells per row, and
    extreme rose to 47.4 %. The law is now the floor itself, not the shortfall."""
    assert census(render(tmp_path, "typical"))["marked"] >= 45.0
    assert census(render(tmp_path, "extreme"))["marked"] >= 45.0
