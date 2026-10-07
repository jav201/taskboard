"""The presentation's unit + acceptance layer (batch 2026-10-07-batch-04, increment 001).

HLR-1001 / LLR-1001.1 · TC-1001, TC-1002, TC-1003, TC-1004 · AT-1001.

The oracle is PRES-C (the operator's verdict 2026-10-07 on the prototype round):
the exact rows the shipped renderer must paint, byte-faithful at 118x30 and
80x24, are `.dev-flow/2026-10-07-batch-04/evidence/frames/PRES-C-*.txt`. The
fixture is the PRES-C oracle board (`tests/present_board.py`), frozen on its own
TODAY; the frames carry the `tw3` cursor and its notes expansion.

RED on the base tree: `views.render_present` does not exist yet (the renderer
landed in this batch's increment 001).
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

import present_board as pb
from taskboard import views
from taskboard.models import Board

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / ".dev-flow" / "2026-10-07-batch-04" / "evidence" / "frames"


class _Today(date):
    @classmethod
    def today(cls):
        return pb.TODAY


@pytest.fixture
def frozen(monkeypatch):
    """Freeze the calendar on the oracle board's TODAY: `PresentScreen` takes
    its `_today` from `app.date`, the startup done-sweep from `models.date` —
    both must see the frozen day or the sweep archives `tw1` (18d old, real
    clock >20d) and the painted frame no longer is the oracle's (the house
    seam of `test_chainmap.py`)."""
    from taskboard import app as app_module
    from taskboard import models

    monkeypatch.setattr(app_module, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)


def _frame(name: str) -> list[str]:
    """The oracle rows, universal-newline split (the frames ship CRLF)."""
    return (FRAMES / name).read_text(encoding="utf-8").splitlines()


def _render(b, w: int, h: int, cursor: str | None = pb.CURSOR) -> list[str]:
    """The shipped renderer's painted rows at a panel size, on the frozen
    calendar (the fixture's own TODAY — `render_present` takes `today`)."""
    text = views.render_present(b, pb.PROJECT_ID, cursor, pb.TODAY, w, h)
    return text.plain.split("\n")


def _plain(widget) -> str:
    """The text a Static now holds (a Rich Text or a Textual Content)."""
    content = widget.content
    return content.plain if hasattr(content, "plain") else str(content)


# --------------------------------------------------------------------------- #
# TC-1001 / TC-1002 — the exact PRES-C rows at both operator sizes
# --------------------------------------------------------------------------- #
def test_TC_1001_the_exact_presc_frame_at_118x30(tmp_path):
    """TC-1001 (LLR-1001.1): on the oracle board, the rendered frame at
    118x30 equals PRES-C-118x30.txt, line for line."""
    b = pb.build(tmp_path / "board.json")
    assert _render(b, 118, 30) == _frame("PRES-C-118x30.txt")


def test_TC_1002_the_exact_presc_frame_at_80x24(tmp_path):
    """TC-1002 (LLR-1001.1): the same board at 80x24 equals PRES-C-80x24.txt."""
    b = pb.build(tmp_path / "board.json")
    assert _render(b, 80, 24) == _frame("PRES-C-80x24.txt")


# --------------------------------------------------------------------------- #
# TC-1003 — S1: a hostile title and notes render escaped, the width holds
# --------------------------------------------------------------------------- #
def test_TC_1003_a_hostile_title_and_notes_render_escaped(tmp_path):
    """TC-1003 (LLR-1001.1, S1): a title holding markup (`[bold]x[/bold]`) and
    notes holding a lone close tag (`[/]`) are painted LITERALLY — never parsed —
    and every row still spends exactly the frame width (no phantom cells)."""
    b = pb.build(tmp_path / "board.json")
    b.task_by_id("tw3").title = "[bold]x[/bold]"
    b.task_by_id("tw3").notes = "[/] boom"
    rows = _render(b, 118, 30)
    joined = "\n".join(rows)
    assert "[bold]x" in joined, joined          # escaped, not interpreted
    assert joined.count("[bold]x") == 2, joined  # the gantt-row label AND the brief
    assert "[/] boom" in joined, joined
    for r in rows:
        assert views.vis(r) == 118, (views.vis(r), r)


# --------------------------------------------------------------------------- #
# TC-1004 — the empty boundaries: no open tasks, no projects at all
# --------------------------------------------------------------------------- #
def test_TC_1004_the_empty_boundaries_still_paint(tmp_path):
    """TC-1004 (HLR-1001, boundary): a project whose tasks are all done still
    presents the project (header, span row, keys row — no task rows, no crash);
    a board with no visible projects paints the `no project to present` line."""
    b = pb.build(tmp_path / "board.json")
    for t in b.tasks:
        if t.project_id == pb.PROJECT_ID:
            t.phase = "Done"
    rows = _render(b, 118, 30)
    joined = "\n".join(rows)
    assert "Website Redesign" in joined, joined
    assert "Fix checkout 500 error" not in joined, joined
    for r in rows:
        assert views.vis(r) == 118, (views.vis(r), r)

    empty = Board([], [], tmp_path / "empty.json", {}, pb.PHASES)
    rows = views.render_present(empty, None, None, pb.TODAY, 118, 30).plain.split("\n")
    assert "no project to present" in "\n".join(rows), rows


# --------------------------------------------------------------------------- #
# AT-1001 — `R` presents, the cursor expands, `x` exports, `esc` leaves no trace
# --------------------------------------------------------------------------- #
async def test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle(
        tmp_path, monkeypatch, frozen):
    """AT-1001 (US-1001, HLR-1001): on the oracle board saved to disk,
    pressing `R` paints the PRES-C-118x30 frame through the shipped surface;
    moving the cursor expands another task's notes; `x` writes the SVG (+ the
    PNG where Microsoft Edge renders it); `esc` leaves without a trace — the
    board untouched (no save, same mtime) and no HTML report written. The
    startup milestone offer stays open underneath the presentation: unanswered,
    it writes nothing (D-615/616)."""
    from textual.widgets import Static

    from taskboard.app import PresentScreen, TaskboardApp

    path = tmp_path / "board.json"
    b = pb.build(path)
    b.save()
    saves = []
    monkeypatch.setattr(Board, "save", lambda self: saves.append(self.path))
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 31)) as pilot:
        # the one-time milestone offer (HLR-605) opens on startup — wait for it
        # so `R` layers the presentation OVER it; unanswered it writes nothing
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                break
            await pilot.pause()
        before_mtime = path.stat().st_mtime_ns
        app.selected_task_id = pb.CURSOR
        await pilot.press("R")
        await pilot.pause()
        assert isinstance(app.screen, PresentScreen)
        frame = app.screen.query_one("#present-frame", Static)
        painted = _plain(frame).split("\n")
        assert painted == _frame("PRES-C-118x30.txt")
        assert "The 500 is a missing tax-rate row" in "\n".join(painted)

        # the cursor moves and another task's notes expand
        open_ids = [t.id for t in views.present_tasks(app.board, pb.PROJECT_ID)[0]]
        nxt = app.board.task_by_id(open_ids[open_ids.index(pb.CURSOR) + 1])
        await pilot.press("l")
        await pilot.pause()
        moved = _plain(frame)
        assert nxt.notes[:40] in moved, (nxt.id, moved)

        # x exports what it shows; SVG always, PNG where Edge renders it
        await pilot.press("x")
        await pilot.pause()
        svg, png = views.present_paths(app.board, "Website Redesign", pb.TODAY)
        assert svg.is_file(), svg
        toasts = [str(t.render()) for t in app.screen.query("Toast")]
        if not png.is_file():
            assert any("PNG needs Microsoft Edge" in t for t in toasts), toasts

        # esc leaves; the board is untouched, no HTML report written
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(app.screen, PresentScreen)
    assert saves == [], f"the presentation saved the board: {saves}"
    assert path.stat().st_mtime_ns == before_mtime
    assert not list((tmp_path / "reports").glob("*.html"))
