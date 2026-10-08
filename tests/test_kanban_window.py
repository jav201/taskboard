"""AT-1202 — The kanban window markers (batch 2026-10-07-batch-06, increment 001).

HLR-1202 / LLR-1202.1 · TC-1202.

When the phase window hides open-phase columns (the shipped `fits`/`start` law),
the phase-head row marks the hidden sides — `◂` at the left edge when any phase
is hidden left, `▸ N` (N exact) at the right when any are hidden right — and
carries no markers when the window shows everything (byte-identical head row to
the pre-batch tree). The `?` kanban help gains the window bullet.

RED on the base tree: the head row wore `◀ N` / `N ▶` (a count on both sides);
`◂` and `▸ N` did not exist.
"""
from __future__ import annotations

import kg_board
from taskboard import views
from taskboard.models import Board, Project, Task


def _fixture(path) -> Board:
    """Four OPEN phases + Done, one task in each — a window that can hide."""
    p = Project("Wide", "violet")
    phases = ["Backlog", "Next", "Doing", "Review", "Done"]
    tasks = [Task(f"task {ph}", p.id, ph, "normal", id=f"t{i}")
             for i, ph in enumerate(phases)]
    return Board([p], tasks, path, phases=phases)


def _head(b, sel, width) -> str:
    """The phase-head row (row 1) of the grouped kanban render."""
    text = views.render_kanban(b, False, sel, kg_board.TODAY, width=width, height=0)
    return text.plain.split("\n")[1]


def test_the_narrow_window_marks_the_hidden_right(tmp_path):
    """LLR-1202.1: at a width fitting 2 of the 4 open phases, with the selection
    at the first phase, the head row names the 2 phases hidden on the right."""
    b = _fixture(tmp_path / "b.json")
    head = _head(b, "t0", 40)
    assert "▸ 2" in head, head
    assert "◂" not in head, head


def test_a_late_selection_marks_the_hidden_left_and_drops_the_count(tmp_path):
    """LLR-1202.1: moving the selection to the last open phase rides the window
    with it — the left marker appears and the right count drops to nothing."""
    b = _fixture(tmp_path / "b.json")
    head = _head(b, "t3", 40)
    assert "◂" in head, head
    assert "▸" not in head, head


def test_the_full_window_carries_no_markers(tmp_path):
    """LLR-1202.1 (negative control): a width that fits all 4 open phases draws
    the head row with no markers — byte-identical to the pre-batch row."""
    b = _fixture(tmp_path / "b.json")
    head = _head(b, "t0", 80)
    assert "◂" not in head and "▸" not in head, head


def test_the_help_names_the_window_bullet():
    """LLR-1202.1: the `?` kanban help carries the window bullet verbatim."""
    usage = [line for _h, lines in views.help_usage("kanban") for line in lines]
    text = " ".join(usage)
    assert "more phases than fit" in text
    assert "the window follows the selection" in text
    assert "◂ ▸ mark the hidden sides" in text
