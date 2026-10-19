"""A milestone in the presentation is a `◆` on its date, never a bar.

Batch 2026-10-19-batch-01, increment 001 — HLR-2101 / LLR-2101.1 · TC-2101 ·
AT-2101 (US-2101). The present-portfolio round found it: on `base_ref` a
milestone with no start date ("Cut-over weekend", due in 6 days) is drawn in
views 1/2 as a bar from today to its due — weeks of work where the board's
gantt draws one date. The presentation now draws a milestone as the board's
gantt does (`gantt_milestone_cells`): `◆` on its due and the date beside it,
the chip `due <Mon D>`, `◆` before the title in the label.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from taskboard import views
from taskboard.views import vis

import present_portfolio_board as pf

BAR_GLYPHS = set(views.FIELD_TASK + views.CRITICAL_REACH + "▬" + "".join(views.FIELD_PHASE_TIP))


def _board(tmp_path: Path):
    return pf.build(tmp_path / "board.json")


def _geo(board, pid, width):
    """The frame's own columns and axis, rebuilt from the presentation's helpers
    (the same calls `render_present` makes)."""
    open_t, _ = views.present_tasks(board, pid)
    label_w, chip_w, field_w = views._present_cols(width, width >= 100)
    ax = views._present_axis(board, board.project_by_id(pid), open_t, field_w, pf.TODAY)
    return label_w, chip_w, field_w, ax, open_t


def _row(text, title):
    rows = text.plain.split("\n")
    rule = next(y for y, r in enumerate(rows) if r.startswith("─"))   # field rows sit above it
    hits = [y for y, r in enumerate(rows[:rule]) if title in r and "▎" in r]
    assert len(hits) == 1, (title, rows)
    return hits[0], rows[hits[0]]


def _style_at(text, y, x):
    """The style string of the span covering cell (y, x) of a one-cell-per-char frame."""
    offset = sum(len(r) + 1 for r in text.plain.split("\n")[:y]) + x
    return " ".join(str(s.style) for s in text.spans if s.start <= offset < s.end)


MILESTONES = [(t[0], t[1], t[2]) for t in pf.TASKS if t[8] and t[3] != "Done"]


@pytest.mark.parametrize("view", views.PRESENT_VIEWS)
@pytest.mark.parametrize("width", (36, 80, 118, 160))
def test_TC_2101_a_milestone_row_is_its_date_not_a_bar(tmp_path, view, width):
    """TC-2101 (LLR-2101.1): every open milestone of the round's board, in views
    1 and 2 at four widths, as the cursor and as a plain row: the field holds
    exactly `gantt_milestone_cells` on the frame's axis (no bar glyph anywhere
    else), the chip reads `due <Mon D>`, the label holds `◆`; under the cursor
    the `◆` is painted bright bold (the accent echo of the field), off the cursor
    in the milestone's own tone."""
    board = _board(tmp_path)
    seen = set()
    for key, pk, title in MILESTONES:
        pid, tid = f"p{pk}", f"t{key}"
        label_w, chip_w, field_w, ax, open_t = _geo(board, pid, width)
        other = next(t.id for t in open_t if t.id != tid)
        task = board.task_by_id(tid)
        want = views.gantt_milestone_cells(task, board, ax, pf.TODAY,
                                           views.milestone_tone(task, board, pf.TODAY))
        for cursor in (tid, other):
            text = views.render_present(board, pid, cursor, pf.TODAY, width, 30, view)
            y, row = _row(text, title[:8])
            assert vis(row) == width
            field = row[label_w + 1:label_w + 1 + field_w]
            assert not BAR_GLYPHS & set(field), (title, width, field)
            for x, (glyph, _) in enumerate(want):
                if glyph != " ":
                    assert field[x] == glyph, (title, width, x, field)
            dia = [x for x, ch in enumerate(field) if ch == "◆"]
            assert len(dia) == sum(g == "◆" for g, _ in want), (title, width, field)
            assert row[-chip_w:].strip() == f"due {views._md(date.fromisoformat(task.due_date))}"
            assert "◆" in row[:label_w], (title, row[:label_w])
            assert row[1] == ("⟦" if cursor == tid else " "), (title, row[:label_w])
            if dia:                    # a field under 3 cells holds no `◆` (as the gantt's)
                style = _style_at(text, y, label_w + 1 + dia[0])
                on = cursor == tid
                assert ("bold" in style and views.HEX["bright"] in style) == on, (title, on, style)
                seen.add(on)
    assert seen == ({True, False} if width > 36 else set())


def test_TC_2101_a_start_date_does_not_make_a_milestone_a_bar(tmp_path):
    """TC-2101 (LLR-2101.1 boundary): a milestone given a start date is still one
    date — the field is `gantt_milestone_cells`, the chip its due alone; a
    milestone with no due draws an empty field and the chip `no dates`."""
    board = _board(tmp_path)
    golive = board.task_by_id("tc5")
    golive.start_date = "2026-10-05"
    label_w, chip_w, field_w, ax, _ = _geo(board, "pcp", 118)
    text = views.render_present(board, "pcp", "tc2", pf.TODAY, 118, 30)
    _, row = _row(text, "Portal go-live")
    field = row[label_w + 1:label_w + 1 + field_w]
    assert not BAR_GLYPHS & set(field), field
    assert field.count("◆") == 1
    assert row[-chip_w:].strip() == "due Nov 6"
    golive.start_date = None
    golive.due_date = None
    text = views.render_present(board, "pcp", "tc2", pf.TODAY, 118, 30)
    _, row = _row(text, "Portal go-live")
    field = row[label_w + 1:label_w + 1 + field_w]
    assert "◆" not in field and not BAR_GLYPHS & set(field), field
    assert row[-chip_w:].strip() == "no dates"


def test_TC_2101_a_late_milestone_is_painted_over(tmp_path):
    """TC-2101 (LLR-2101.1; code review F2): a milestone past its due is painted in
    `over` — the one tone the branch takes that is not the project's hue — on its
    `◆` in the field and in the label; under the cursor the field's `◆` is the
    bright echo instead."""
    board = _board(tmp_path)
    board.task_by_id("tb5").due_date = "2026-10-16"
    label_w, _, field_w, _, _ = _geo(board, "pbm", 118)
    over = views.HEX["over"]
    for cursor, field_over in (("tb3", True), ("tb5", False)):
        text = views.render_present(board, "pbm", cursor, pf.TODAY, 118, 30)
        y, row = _row(text, "Cut-over weekend")
        assert over in _style_at(text, y, row.index("◆")), row
        x = label_w + 1 + row[label_w + 1:label_w + 1 + field_w].index("◆")
        assert (over in _style_at(text, y, x)) == field_over, (cursor, row)
        assert row.rstrip().endswith("due Oct 16"), row


def test_TC_2101_other_rows_are_drawn_as_shipped(tmp_path):
    """TC-2101 (LLR-2101.1): a task that is not a milestone keeps its bar — the
    branch is the milestone's alone (`Customer notice emails`, 0..+4 days, still
    a bar ending on its phase tip)."""
    board = _board(tmp_path)
    label_w, _, field_w, _, _ = _geo(board, "pbm", 118)
    text = views.render_present(board, "pbm", "tb3", pf.TODAY, 118, 30)
    _, row = _row(text, "Customer notice emails")
    field = row[label_w + 1:label_w + 1 + field_w]
    assert BAR_GLYPHS & set(field) and "◆" not in field, field


async def test_AT_2101_the_cut_over_weekend_reads_as_a_milestone(tmp_path, monkeypatch):
    """AT-2101 (US-2101, HLR-2101): the round's board saved to disk, the app at
    118x31, the selected task `Tax rules for new regions`, `R` → in the frame the
    `Cut-over weekend` row holds one `◆`, in the column of the project row's own
    `◆` (the project's due, Oct 25, is the milestone's day), no bar glyph, and
    its chip reads `due Oct 25`; `2` (the split view) → the same row."""
    from taskboard import app as app_module
    from taskboard import models
    from taskboard.app import TaskboardApp

    class _Today(date):
        @classmethod
        def today(cls):
            return pf.TODAY

    monkeypatch.setattr(app_module, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)
    path = tmp_path / "board.json"
    pf.build(path).save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 31)) as pilot:
        await pilot.pause()
        app.selected_task_id = pf.CURSOR
        await pilot.press("R")
        await pilot.pause()
        for key in ("", "2"):
            if key:
                await pilot.press(key)
                await pilot.pause()
            frame = app.screen.query_one("#present-frame").content.plain.split("\n")
            span = next(r for r in frame if r.startswith("▌ BILLING MIGRATION"))
            row = next(r for r in frame if "Cut-over weekend" in r and "▎" in r)
            field = row[31:118 - 14]
            assert field.count("◆") == 1, row
            assert not BAR_GLYPHS & set(field), row
            assert row.index("◆", 31) == span.index("◆", 31), (span, row)
            assert row.rstrip().endswith("due Oct 25"), row
