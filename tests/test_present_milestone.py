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
GROUND = set("·┆╎┃│")


# Inc MR-b re-baseline (LLR-4651.1, LLR-4652.1, LLR-4652.5): a project's milestones
# share ONE field row, directly under the span row, drawn by the board gantt's
# milestone row (`gantt_milestone_row`). HLR-2101's claim — a milestone is its date,
# never a bar — is asserted on that row; the per-milestone row it was first read on
# no longer exists. The helpers find the row by its place, not by a title (an
# unselected milestone's title is no longer painted, MR-a LLR-4603.1).
def _ms_row(text):
    rows = text.plain.split("\n")
    span = next(y for y, r in enumerate(rows) if r.startswith("▌ "))
    return span + 1, rows[span + 1]


def _lane(board, pid):
    """The project's drawn milestones in walk order (SEAM-1's rule, restated)."""
    ms = [t for t in views.present_tasks_m(board, pid)[0] if t.milestone]
    return tuple(sorted(ms, key=lambda t: (t.due_date is None, t.due_date or "9999-12-31",
                                           t.title, t.id)))


def _plain_field(cells) -> str:
    return "".join(" " if g == " " else g for g, _ in cells)


@pytest.mark.parametrize("view", views.PRESENT_VIEWS)
@pytest.mark.parametrize("width", (36, 80, 118, 160))
def test_TC_2101_a_milestone_row_is_its_date_not_a_bar(tmp_path, view, width):
    """TC-2101 (LLR-2101.1), re-baselined by Inc MR-b (LLR-4651.1, LLR-4652.1,
    LLR-4652.5): every open milestone of the round's board, in views 1 and 2 at four
    widths, as the cursor and with the cursor on a task: the project's ONE milestone
    row (under the span) holds no bar glyph anywhere and exactly
    `gantt_milestone_row`'s cells on the frame's axis; the label holds `◆` and the
    lead `⟦` only on the cursor; the chip is the cursor milestone's `due <Mon D>`,
    else the first upcoming one's; under the cursor its `◆` is painted reverse (the
    shared row's selection, MR-a SEAM-8), off the cursor not."""
    board = _board(tmp_path)
    seen = set()
    for key, pk, title in MILESTONES:
        pid, tid = f"p{pk}", f"t{key}"
        label_w, chip_w, field_w, ax, open_t = _geo(board, pid, width)
        other = next(t.id for t in open_t if not t.milestone)
        task = board.task_by_id(tid)
        lane = _lane(board, pid)
        upcoming = next((m for m in lane if m.due_date and
                         date.fromisoformat(m.due_date) >= pf.TODAY), None)
        for cursor in (tid, other):
            on = cursor == tid
            text = views.render_present(board, pid, cursor, pf.TODAY, width, 30, view)
            y, row = _ms_row(text)
            assert vis(row) == width
            field = row[label_w + 1:label_w + 1 + field_w]
            assert not BAR_GLYPHS & set(field), (title, width, field)
            want = _plain_field(views.gantt_milestone_row(lane, tid if on else None, board,
                                                          ax, pf.TODAY))
            got = "".join(" " if ch in GROUND else ch for ch in field)
            assert got == want, (title, width, on, got, want)
            chip_task = task if on else upcoming
            chip = (f"due {views._md(date.fromisoformat(chip_task.due_date))}"
                    if chip_task is not None else "")
            assert row[-chip_w:].strip() == chip, (title, on, row[-chip_w:])
            assert "◆" in row[:label_w], (title, row[:label_w])
            assert row[1] == ("⟦" if on else " "), (title, row[:label_w])
            x = ax.cell(date.fromisoformat(task.due_date))
            if field_w >= 3 and 0 <= x < field_w and want[x] == "◆":
                style = _style_at(text, y, label_w + 1 + x)
                assert ("reverse" in style) == on, (title, on, style)
                seen.add(on)
    assert seen == ({True, False} if width > 36 else set())


def test_TC_2101_a_start_date_does_not_make_a_milestone_a_bar(tmp_path):
    """TC-2101 (LLR-2101.1 boundary), re-baselined by Inc MR-b (LLR-4652.5): a
    milestone given a start date is still one date — the cursor on it, its project's
    milestone row holds one `◆` and no bar glyph, the chip its due alone; a milestone
    with no due draws no mark and the chip `no dates`. The cursor moves from `tc2`
    to the milestone: an unselected milestone's chip is the row's, not its own."""
    board = _board(tmp_path)
    golive = board.task_by_id("tc5")
    golive.start_date = "2026-10-05"
    label_w, chip_w, field_w, ax, _ = _geo(board, "pcp", 118)
    text = views.render_present(board, "pcp", "tc5", pf.TODAY, 118, 30)
    _, row = _ms_row(text)
    field = row[label_w + 1:label_w + 1 + field_w]
    assert not BAR_GLYPHS & set(field), field
    assert field.count("◆") == 1
    assert row[-chip_w:].strip() == "due Nov 6"
    golive.start_date = None
    golive.due_date = None
    text = views.render_present(board, "pcp", "tc5", pf.TODAY, 118, 30)
    _, row = _ms_row(text)
    field = row[label_w + 1:label_w + 1 + field_w]
    assert "◆" not in field and not BAR_GLYPHS & set(field), field
    assert row[-chip_w:].strip() == "no dates"


def test_TC_2101_a_late_milestone_is_painted_over(tmp_path):
    """TC-2101 (LLR-2101.1; code review F2) — as amended by batch 2026-10-24-batch-01
    (MM-D1, one seat) and re-baselined by Inc MR-b (LLR-4652.1, LLR-4652.5; MR-a
    LLR-4603.3): a late milestone's mark itself stays `◆` in `mut` (this board has no
    classes); the lateness rides the late tag beside it (`▲3d`) in `over`, and the row
    shows no chip (no member is upcoming). Under the cursor the `◆` is reverse and the
    chip its own `due Oct 16` in `over`."""
    board = _board(tmp_path)
    board.task_by_id("tb5").due_date = "2026-10-16"
    label_w, chip_w, field_w, ax, _ = _geo(board, "pbm", 118)
    over, mut = views.HEX["over"], views.HEX["mut"]
    x0 = label_w + 1 + ax.cell(date(2026, 10, 16))
    text = views.render_present(board, "pbm", "tb3", pf.TODAY, 118, 30)
    y, row = _ms_row(text)
    assert row[x0] == "◆", row
    style = _style_at(text, y, x0)
    assert mut in style and "reverse" not in style, style
    tag = row.index("▲3d", label_w + 1)
    assert over in _style_at(text, y, tag)                 # the late tag says late
    assert row[-chip_w:].strip() == "", row
    text = views.render_present(board, "pbm", "tb5", pf.TODAY, 118, 30)
    y, row = _ms_row(text)
    assert row[x0] == "◆" and "reverse" in _style_at(text, y, x0), row
    assert row.rstrip().endswith("due Oct 16"), row
    assert over in _style_at(text, y, len(row.rstrip()) - 1)


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
            at = next(y for y, r in enumerate(frame) if r.startswith("▌ BILLING MIGRATION"))
            span = frame[at]
            # Inc MR-b re-baseline (LLR-4651.1): the milestone is drawn on the project's
            # one milestone row, the line under the span; with the cursor on a task its
            # title is not painted there (MR-a LLR-4603.1), so the row is found by place
            row = frame[at + 1]
            field = row[31:118 - 14]
            assert field.count("◆") == 1, row
            assert not BAR_GLYPHS & set(field), row
            assert row.index("◆", 31) == span.index("◆", 31), (span, row)
            assert row.rstrip().endswith("due Oct 25"), row
