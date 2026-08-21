"""The grid presentation of the swimlanes view (variant G2).

Ports the prototype in `prototypes/lanes_gauge` into the main renderer and
pins its geometry, sediment bar, mercury spine, navigation, and presentation
cycle.
"""

import re
from datetime import date, timedelta

import pytest

from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.views import nav_model, render_swimlanes

TODAY = date(2026, 8, 19)
WIDTHS = (68, 86, 118)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def grid_board(tmp_path, name="grid.json"):
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


def typical(tmp_path):
    """Four projects: one late task, one healthy, one paused, one overdue project."""
    b = grid_board(tmp_path)
    atlas = Project("Atlas", "lime", "on_track",
                    start_date=iso(-20), due_date=iso(14))
    beacon = Project("Beacon", "sky", "on_track",
                     start_date=iso(-10), due_date=iso(30))
    cinder = Project("Cinder", "violet", "paused",
                     start_date=iso(-5), due_date=iso(45))
    delta = Project("Delta", "pink", "cancelled",
                    start_date=iso(-40), due_date=iso(-5))
    b.projects += [atlas, beacon, cinder, delta]
    b.tasks += [
        Task("Fix the ingest path", atlas.id, "Doing", "high",
             due_date=iso(-5), blocked=True),
        Task("Write the v2 reference", atlas.id, "Backlog", "normal",
             due_date=iso(6)),
        Task("Ship the migration", atlas.id, "Done", "normal",
             due_date=iso(-2)),
        Task("Harden the search index", beacon.id, "Doing", "normal",
             due_date=iso(12), urls=["http://x"]),
        Task("Deprecate v1 endpoints", beacon.id, "Backlog", "normal",
             due_date=iso(3)),
        Task("Retire the old host", cinder.id, "Backlog", "normal"),
        Task("Sunset the legacy host", delta.id, "Backlog", "normal",
             due_date=iso(-2)),
    ]
    b.save()
    return b


def rows_of(b, w=86, h=30, selected=None, line_map=None):
    return str(render_swimlanes(b, False, selected, TODAY, width=w, height=h,
                                line_map=line_map, presentation="grid")).split("\n")


def markup_of(b, w=86, h=30):
    return render_swimlanes(b, False, None, TODAY, width=w, height=h,
                            presentation="grid").markup


# --------------------------------------------------------------------------- #
# geometry
# --------------------------------------------------------------------------- #
def test_every_row_is_exactly_the_requested_width(tmp_path):
    b = typical(tmp_path)
    for w in WIDTHS:
        for h in (24, 30, 44):
            for line in rows_of(b, w, h):
                assert len(line) == w, f"{w}x{h}: {len(line)} != {w}"


def test_header_names_the_mode_and_shows_counts(tmp_path):
    b = typical(tmp_path)
    header = rows_of(b, 86, 30)[0]
    assert "grid" in header
    # 6 open, 2 due (fix ingest + sunset legacy)
    assert "6 open" in header
    assert "2 due" in header


def test_panel_headers_show_project_names_and_open_counts(tmp_path):
    b = typical(tmp_path)
    out = rows_of(b, 86, 30)
    header_rows = [ln for ln in out if "▐ " in ln]
    assert any("Atlas" in ln and "2" in ln for ln in header_rows)
    assert any("Beacon" in ln and "2" in ln for ln in header_rows)
    assert any("Cinder" in ln and "1" in ln for ln in header_rows)


def test_many_projects_stack_into_extra_layers(tmp_path):
    b = grid_board(tmp_path)
    projects = [Project(f"P{i}", "lime", "on_track",
                        start_date=iso(-10), due_date=iso(10))
                for i in range(7)]
    b.projects += projects
    for i, p in enumerate(projects):
        b.tasks.append(Task(f"task {i}", p.id, "Doing", due_date=iso(i)))
    b.save()
    header = rows_of(b, 86, 24)[0]
    # With more than 2 projects the grid stacks extra layers instead of hiding.
    assert "grid 2×" in header


# --------------------------------------------------------------------------- #
# sediment bar
# --------------------------------------------------------------------------- #
def test_sediment_bar_has_today_rule_and_window_labels(tmp_path):
    b = typical(tmp_path)
    out = rows_of(b, 86, 30)
    bar_row = next(ln for ln in out if "╎" in ln)
    # The fill bar carries the today rule; the labels sit on their own row.
    labels_row = next(ln for ln in out if "-7d" in ln and "+21d" in ln)
    assert labels_row is not None


def test_sediment_bar_shows_next_due_hub_and_studs(tmp_path):
    b = typical(tmp_path)
    out = rows_of(b, 86, 30)
    # Atlas next due is -5d -> overdue, hub should show "Aug 14 ▲5d"
    hub_row = next(ln for ln in out if "Aug 14" in ln and "▲5d" in ln)
    assert hub_row is not None
    # The studs row (just below the bar, above the hub) contains landing marks.
    studs_row = next(ln for ln in out if "▄" in ln)
    assert studs_row is not None


def test_sediment_bar_for_project_without_dates(tmp_path):
    b = typical(tmp_path)
    out = rows_of(b, 86, 30)
    hub_row = next(ln for ln in out if "no dates" in ln)
    assert hub_row is not None


# --------------------------------------------------------------------------- #
# mercury spine
# --------------------------------------------------------------------------- #
def test_mercury_spine_for_late_project_is_red_with_cap(tmp_path):
    b = typical(tmp_path)
    out = rows_of(b, 86, 30)
    # Delta is overdue: its mercury spine should show the red cap after the
    # inter-panel separator.
    assert any("│▲│" in ln for ln in out)


def test_mercury_spine_for_inbox_is_bare_rail(tmp_path):
    b = grid_board(tmp_path)
    b.tasks.append(Task("Loose task", None, "Backlog", "normal"))
    b.save()
    out = rows_of(b, 86, 24)
    # The Inbox panel should have a bare │ rail and no mercury fill.
    assert any("│" in ln[:2] for ln in out)


# --------------------------------------------------------------------------- #
# task rows
# --------------------------------------------------------------------------- #
def test_task_row_shows_title_date_chip_and_indicators(tmp_path):
    b = typical(tmp_path)
    out = rows_of(b, 86, 30)
    row = next(ln for ln in out if "Fix the ingest path" in ln)
    assert "Aug 14" in row
    assert "!" in row          # high priority
    assert "▲" in row          # blocked prefix


def test_task_row_shows_url_indicator(tmp_path):
    b = typical(tmp_path)
    out = rows_of(b, 86, 30)
    row = next(ln for ln in out if "Harden the search index" in ln)
    assert "↗" in row


def test_selected_task_is_reversed(tmp_path):
    b = typical(tmp_path)
    task = b.tasks[0]
    markup = markup_of(b, 86, 30)
    assert task.title in markup
    # selecting the task should wrap its title in reverse
    selected = render_swimlanes(b, False, task.id, TODAY, width=86, height=30,
                                presentation="grid").markup
    assert "[reverse]" in selected


def test_line_map_points_to_task_rows(tmp_path):
    b = typical(tmp_path)
    line_map = {}
    render_swimlanes(b, False, None, TODAY, width=86, height=30,
                     line_map=line_map, presentation="grid")
    for t in b.tasks:
        if t.id in line_map:
            idx = line_map[t.id]
            assert t.title in str(rows_of(b, 86, 30)[idx])


# --------------------------------------------------------------------------- #
# navigation
# --------------------------------------------------------------------------- #
def test_nav_model_grid_has_one_column_per_panel_x(tmp_path):
    b = typical(tmp_path)
    cols = nav_model("swimlanes", b, False, TODAY, width=86, height=30,
                     presentation="grid")
    assert len(cols) == 2          # two columns at 86 cells
    all_ids = {t.id for t in b.tasks}
    nav_ids = {tid for col in cols for tid in col}
    assert nav_ids <= all_ids


def test_nav_model_waves_stays_one_column(tmp_path):
    b = typical(tmp_path)
    cols = nav_model("swimlanes", b, False, TODAY, width=86, height=30,
                     presentation="waves")
    assert len(cols) == 1


# --------------------------------------------------------------------------- #
# presentation cycle
# --------------------------------------------------------------------------- #
async def test_tab_cycles_swimlanes_presentations(tmp_path):
    b = typical(tmp_path)
    app = TaskboardApp(board_path=str(b.path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        assert app.view_mode == "swimlanes"
        assert app.lanes_presentation == "grid"
        await pilot.press("tab")
        await pilot.pause()
        assert app.lanes_presentation == "waves"
        await pilot.press("tab")
        await pilot.pause()
        assert app.lanes_presentation == "grid"


# --------------------------------------------------------------------------- #
# waves regression guard
# --------------------------------------------------------------------------- #
def test_waves_presentation_still_renders_classic_lanes(tmp_path):
    b = typical(tmp_path)
    out = str(render_swimlanes(b, False, None, TODAY, width=86, height=30,
                               presentation="waves")).split("\n")
    # Classic lanes draw the shared day-axis scale at the bottom.
    assert any("today" in ln or "+" in ln and "d" in ln for ln in out[-3:])
