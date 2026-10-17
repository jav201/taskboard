"""The presentation's date ruler and start–end chips (batch 2026-10-16-batch-01, increment 001).

HLR-1601 / LLR-1601.1, LLR-1601.2 · TC-1601, TC-1602 · AT-1601 (US-1601).

Why these matter: the room reads WHEN each bar is from the presentation. The
shipped PRES-C field drew bars with no calendar; the operator's verdict on
`prototypes/present_rulers/` (2026-10-16) chose variant B — the gantt view's own
month band + tick row above the span row, the cursor task's exact dates echoed on
the tick row — plus both dates on every field row. Today stays ACCENT on the ruler
(«Se ve mejor en acento»), the echo keeps its own tone, and the present field
shades no weekend, so neither does its ruler.

The literals below are written by hand from `tests/present_board.py`'s dates
(TODAY = Wed Sep 30 2026), NOT read back from the renderer: they are what keeps the
re-captured PRES-R oracle honest (01-requirements.md §6.3).
RED on the base tree: no ruler rows, the old due-and-distance chips.
"""
from __future__ import annotations

from datetime import date

import pytest

import present_board as pb
from taskboard import views
from taskboard.views import HEX, WEEKEND_BG


class _Today(date):
    @classmethod
    def today(cls):
        return pb.TODAY


@pytest.fixture
def frozen(monkeypatch):
    """The house seam (`tests/test_present.py`): the screen and the startup
    sweep both read the frozen day."""
    from taskboard import app as app_module
    from taskboard import models

    monkeypatch.setattr(app_module, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)


def _rows(b, w, h, cursor=pb.CURSOR):
    return views.render_present(b, pb.PROJECT_ID, cursor, pb.TODAY, w, h).plain.split("\n")


def _geo(b, w):
    proj = b.project_by_id(pb.PROJECT_ID)
    open_t, _ = views.present_tasks(b, pb.PROJECT_ID)
    wide = w >= 100
    label_w, chip_w, field_w = views._present_cols(w, wide)
    ax = views._present_axis(b, proj, open_t, field_w, pb.TODAY)
    return proj, views._PresentGeo(w, label_w, chip_w, field_w, ax,
                                   set(views.critical_chain(b)), pb.TODAY, wide, proj.color)


def _styled(markup: str, key: str) -> bool:
    return HEX[key] in markup


# --------------------------------------------------------------------------- #
# TC-1601 — the ruler: today accent, the echo in its tone, no weekend shading
# --------------------------------------------------------------------------- #
def test_TC_1601_the_ruler_rows_their_colours_and_no_weekend(tmp_path):
    """TC-1601 (LLR-1601.1). Today's number on the month row and today's cell on
    the tick row wear ACCENT (the gantt view's colour — the operator's choice,
    not the field's bright rule); the oracle cursor `tw3` is past due, so its
    echo wears OVER, and a future cursor's echo wears BRIGHT; the window spans
    several weekends of Sep–Oct 2026 and NOT ONE cell of the frame carries the
    weekend background, while the gantt view's own day row (the default) still
    does — the gantt view's output is unchanged."""
    b = pb.build(tmp_path / "board.json")
    proj, p = _geo(b, 118)
    assert any(d.weekday() >= 5 for d in p.ax.window_days()), "fixture lost its weekends"

    month, ticks = views._present_ruler(proj, b, p, b.task_by_id(pb.CURSOR))
    today_num = views._ruler_cell("3", "accent", True, True)
    assert today_num in month, "today's number is not accent on the month row"
    assert "today Wed Sep 30" in views._strip(month)
    assert _styled(month.split("today Wed Sep 30")[0] + "today", "accent")
    assert views._ruler_cell("⟦", "over", True) in ticks, "a past-due echo must wear over"

    _m, future = views._present_ruler(proj, b, p, b.task_by_id("tw5"))
    assert views._ruler_cell("⟦", "bright", True) in future, "a future echo must wear bright"

    frame = views.render_present(b, pb.PROJECT_ID, pb.CURSOR, pb.TODAY, 118, 30)
    assert not any("on " + WEEKEND_BG.lower() in str(s.style).lower() for s in frame.spans), \
        "the presentation shades a weekend"
    gantt_cells, _meta = views.gantt_day_row(p.ax, pb.TODAY, None)
    assert any(WEEKEND_BG in cell for cell in gantt_cells), "the gantt default lost its shading"


def test_TC_1601_an_echo_too_long_for_the_field_moves_to_the_label(tmp_path):
    """TC-1601 (LLR-1601.1 boundary): a cursor task spanning the whole field
    leaves its dates no free run beside the echo, so the label column carries
    them (`Sep 1 → Oct 14 ▸`) in the echo's tone instead of the scale label —
    the gantt view's own fallback."""
    b = pb.build(tmp_path / "board.json")
    b.task_by_id("tw6").start_date = "2026-09-01"          # Sep 1 → Oct 14, open, future
    for w in (118, 80):
        proj, p = _geo(b, w)
        _month, ticks = views._present_ruler(proj, b, p, b.task_by_id("tw6"))
        label = views._strip(ticks)[:p.label_w]
        assert label.strip() == "Sep 1 → Oct 14 ▸", (w, label)
        assert ticks.startswith("[b " + HEX["bright"] + "]"), (w, ticks[:40])


def test_TC_1601_a_project_with_no_open_task_still_paints_its_ruler(tmp_path):
    """TC-1601 (LLR-1601.1, HLR-1601 empty boundary): every task done — the two
    ruler rows still paint (today in the label, the month on the band, the day
    ticks on the tick row, whose label is blank: there is no cursor to echo and
    the scale label is gone — HLR-1701, batch 2026-10-17-batch-01)."""
    b = pb.build(tmp_path / "board.json")
    for t in b.tasks:
        if t.project_id == pb.PROJECT_ID:
            t.phase = "Done"
    rows = _rows(b, 118, 30)
    assert "today Wed Sep 30" in rows[1], rows[1]
    assert "October" in rows[1], rows[1]                 # a month band (the window narrows)
    assert rows[2][:30].strip() == "", rows[2]                     # no echo, no label
    assert any(ch.isdigit() for ch in rows[2][31:]), rows[2]      # the ticks paint
    for r in rows:
        assert views.vis(r) == 118


# --------------------------------------------------------------------------- #
# TC-1602 — the start–end chips
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("start, due, label", [
    (date(2026, 9, 24), date(2026, 9, 28), "Sep 24–28"),          # one month
    (date(2026, 8, 21), date(2026, 10, 10), "Aug 21–Oct 10"),     # across months
    (date(2026, 12, 28), date(2027, 1, 3), "Dec 28–Jan 3"),       # across years, no year
    (None, date(2026, 10, 14), "due Oct 14"),                     # no start
    (date(2026, 10, 6), date(2026, 10, 6), "Oct 6"),              # start == due
    (date(2026, 9, 3), None, "from Sep 3"),                       # no due
    (None, None, "no dates"),
])
def test_TC_1602_the_span_label_cases(start, due, label):
    """TC-1602 (LLR-1601.2): both dates, no arithmetic for the room."""
    assert views.present_span_label(start, due) == label


def test_TC_1602_the_chip_tones_and_an_unparseable_date():
    """TC-1602 (LLR-1601.2): over once the due has passed, dim with no dates, mut
    otherwise; an unparseable date reads as absent (`parse_iso`)."""
    t = pb.TODAY
    assert HEX["over"] in views._present_chip("2026-09-24", "2026-09-28", t, 13)
    assert HEX["dim"] in views._present_chip(None, None, t, 13)
    assert HEX["mut"] in views._present_chip("2026-10-04", "2026-10-10", t, 13)
    assert views._strip(views._present_chip("not-a-date", "2026-10-14", t, 13)) == "   due Oct 14"


def test_TC_1602_the_oracle_boards_chips_whole_at_both_sizes(tmp_path):
    """TC-1602 (LLR-1601.2): every field row ends with its start–end, written here
    by hand from the fixture — the span row `Aug 21–Oct 10` (13 cells: a 12-cell
    chip clips it), then the open tasks by due. Columns: label 30 / chip 13 at
    118, label 20 / chip 13 at 80."""
    b = pb.build(tmp_path / "board.json")
    want = ["Aug 21–Oct 10", "Sep 5–27", "Sep 24–28", "due Oct 6", "Oct 4–10", "due Oct 14"]
    assert views._present_cols(118, True) == (30, 13, 73)
    assert views._present_cols(80, False) == (20, 13, 45)
    for w, h in ((118, 30), (80, 24)):
        field = _rows(b, w, h)[3:9]
        assert [r[-13:].strip() for r in field] == want, (w, field)


# --------------------------------------------------------------------------- #
# AT-1601 — `R` shows the calendar, and the dates follow the cursor
# --------------------------------------------------------------------------- #
async def test_AT_1601_R_paints_the_ruler_and_the_dates_follow_the_cursor(tmp_path, frozen):
    """AT-1601 (US-1601, HLR-1601), through the shipped surface: on the oracle
    board, `R` → the second painted row names today and September, the third
    carries the cursor task's dates (`Sep 24`…`Sep 28`), every field row ends in
    its chip; `→` moves the cursor to `Optimize image assets` (no start, due
    Oct 6) and the tick row now carries `due Oct 6`, not `Sep 24`."""
    from textual.widgets import Static

    from taskboard.app import TaskboardApp

    path = tmp_path / "board.json"
    pb.build(path).save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 31)) as pilot:
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                break
            await pilot.pause()
        app.selected_task_id = pb.CURSOR
        await pilot.press("R")
        await pilot.pause()
        frame = app.screen.query_one("#present-frame", Static)

        def painted():
            content = frame.content
            return (content.plain if hasattr(content, "plain") else str(content)).split("\n")

        rows = painted()
        assert "today Wed Sep 30" in rows[1] and "September" in rows[1], rows[1]
        assert "Sep 24" in rows[2] and "Sep 28" in rows[2], rows[2]
        assert rows[3].rstrip().endswith("Aug 21–Oct 10"), rows[3]
        assert rows[5].rstrip().endswith("Sep 24–28"), rows[5]

        await pilot.press("right")
        await pilot.pause()
        rows = painted()
        assert "due Oct 6" in rows[2], rows[2]
        assert "Sep 24" not in rows[2], rows[2]
