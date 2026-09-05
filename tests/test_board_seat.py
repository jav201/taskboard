"""F-17: the BOARD must build at the seat it is about to be drawn at.

WHY THIS FILE EXISTS. `inc22.md` §5 left the F-16 class of defect open for
every other push-painted widget: "`Hero`, `Tile`, `col-head`, `kb-empty` still
repair from `on_resize` and would miss an event the same silent way". inc23
asked each of them, with recorders, and the answers were not the same:

  * `Hero` and `Tile` are repainted by `TaskboardWidget.redraw()`, which the
    12 Hz `tick_fast` calls on every frame. Moved with no resize handler
    running at all, both come right within one tick. Their repair does not
    hang on an event, so there is nothing here to fix.
  * `.col-head` IS composed for a width -- 39 distinct paints over the 48
    board widths the app can reach (columns), 48 (sections), 25 (split) -- and
    `KanbanBoard.on_resize` -> `build()` is its ONLY repair.
  * `.kb-empty` is composed for a width too, but `k.empty(w)` has a single
    threshold (the mascot, at w >= 14) and every width the board can hand it
    sits on one side of it: ONE distinct paint over all 48 widths, in all
    three layouts. It cannot go stale, so it is not separately repaired --
    though the board's rebuild covers it anyway.

WHY THE GUARD IS ON THE BOARD AND NOT ON THE HEAD. `.col-head` is composed in
`build()` for `row_width(column seat)` -- a width derived from the BOARD's
seat, not from the head's own. Measured, columns branch: shrinking the board
24 cells leaves the heads' own seats at 56/32/21, exactly where they were,
because `build()` pinned each column with `col.styles.width = cw`; the heads'
`render()` is never called. A painted-width guard on the head would be blind
there. The board's `render()` sees every one of those changes.

WHAT THIS TEST REPRODUCES, AND WHAT IT DOES NOT. As in `test_card_seat.py`,
the missing POST is a race that needs a fresh interpreter; what the race
LEAVES BEHIND needs none. `deafen()` takes away the board's one event-side
repair, so the resize arrives and rebuilds nothing -- from the board's side
the same hole as an event that was never sent.
"""
from __future__ import annotations

import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes" / "widget_slice"))

from taskboard import language as LG                              # noqa: E402
from kanban import KanbanBoard                                    # noqa: E402

#: the two branches whose heads answer differently. `industrial` is COLUMNS,
#: where a board resize does not move a head's own seat; `ledger` is SECTIONS,
#: where it does. Both are stale by the same mechanism and both are repaired
#: by the same guard, which is the point of running the pair.
COLUMNS = LG.kit("industrial")
SECTIONS = LG.kit("ledger")

WIDE = 110
NARROW = 70


class Task:
    """The fields `build()` and `render_card` read off a task."""
    def __init__(self, title: str, phase: str) -> None:
        self.title = title
        self.phase = phase
        self.due_date = None
        self.priority = "high"
        self.project_id = None
        self.blocked = False
        self.archived = False


TASKS = [Task(f"Design homepage mockups {i}", p)
         for p in ("TODO", "DOING", "DONE") for i in range(3)]


class StubBoard:
    """The board API `build()` reaches for, and nothing else."""
    phases = ("TODO", "DOING", "DONE")

    def visible_tasks(self, show_archived: bool = False) -> list[Task]:
        return TASKS

    def is_done(self, task) -> bool:
        return task.phase == "DONE"

    def project_by_id(self, pid):
        return None

    def phase_index(self, task) -> int:
        return self.phases.index(task.phase)


def deafen(monkeypatch) -> list[int]:
    """Open F-16's hole at the board, without the race: take away its ONE
    event-side repair and record the events it would have repaired on.

    In the wild the `Resize` is never POSTED; here it is never ACTED ON. The
    patch goes on `KanbanBoard` ITSELF and not on a subclass, because Textual
    dispatches the handler of EVERY class in the MRO (measured in
    `test_card_seat.py`: a subclass override still runs the base's). The
    events are recorded rather than dropped so the tests can assert one really
    arrived -- an empty list would mean the fixture stopped exercising
    anything.
    """
    seen: list[int] = []
    monkeypatch.setattr(KanbanBoard, "on_resize",
                        lambda self: seen.append(self.size.width))
    return seen


class PreFixBoard(KanbanBoard):
    """`KanbanBoard`'s paint path as it stood at `4f05649`: rebuilt from the
    EVENT only. Quoted here rather than reached for through git, because
    assertion (a)'s whole job is to keep proving the fixture has teeth."""
    render = Vertical.render


class OneBoardApp(App):
    """One board in a wrapper whose width the test moves. The board rule is
    quoted from `widget_slice/widget.tcss`."""
    CSS = ("#wrap { width: auto; height: 1fr; }\n"
           ".col-head { padding-left: 1; }\n"
           ".kb-empty { padding-left: 1; }\n"
           ".kb-card { width: 1fr; height: auto; max-height: 3; padding: 0 1; }")

    def __init__(self, kit, board_cls=KanbanBoard) -> None:
        super().__init__()
        self.kit = kit
        self.board_cls = board_cls

    def compose(self) -> ComposeResult:
        wrap = Vertical(id="wrap")
        wrap.styles.width = WIDE
        with wrap:
            yield self.board_cls(StubBoard(), self.kit, id="kb")


def heads(board) -> list[str]:
    return [str(w.content) for w in board.query(".col-head")]


async def start(app, pilot):
    """Mount, then build once explicitly -- which is what the real app does
    (`app.py:start_widget` calls `kb.build()`); the pre-fix board with a
    deafened `on_resize` would otherwise never build at all and the test would
    be comparing two empty lists."""
    await pilot.pause()
    board = app.query_one(KanbanBoard)
    board.build()
    await pilot.pause()
    return board


async def narrow(app, pilot) -> None:
    """The layout takes 40 cells off the board."""
    app.query_one("#wrap").styles.width = NARROW
    await pilot.pause()


async def _stale_when_deaf(monkeypatch, kit) -> None:
    """(a) The fixture has teeth: the pre-fix board holds the wide build."""
    seen = deafen(monkeypatch)
    app = OneBoardApp(kit, PreFixBoard)
    async with app.run_test(size=(120, 30)) as pilot:
        board = await start(app, pilot)
        wide = heads(board)
        assert wide and all(h.strip() for h in wide), wide

        await narrow(app, pilot)

        assert seen, "the fixture never delivered the resize it ignores"
        assert board.size.width == NARROW, board.size
        assert heads(board) == wide, (
            "the pre-fix board repaired itself -- the wedge is no longer what "
            "this file reproduces")
        # ... and it SHOULD have moved: the rebuild is the oracle.
        board.build()
        await pilot.pause()
        assert heads(board) != wide, (
            f"the head does not depend on the board's seat under {kit.name!r}, "
            f"so this fixture proves nothing: {wide!r}")


async def _repaired_at_next_paint(monkeypatch, kit) -> None:
    """(b) And the shipped board rebuilds at its next paint, which is the fix."""
    seen = deafen(monkeypatch)
    app = OneBoardApp(kit, KanbanBoard)
    async with app.run_test(size=(120, 30)) as pilot:
        board = await start(app, pilot)
        wide = heads(board)

        await narrow(app, pilot)
        got = heads(board)

        assert seen, "the fixture never delivered the resize it ignores"
        assert board._built_w == NARROW, (
            f"the board is still built for {board._built_w}, seat is {NARROW}")
        assert got != wide, (
            f"the seat lost {WIDE - NARROW} cells and the head did not move: "
            f"{got!r}")
        # and what it shows IS what the present seat composes
        board.build()
        await pilot.pause()
        assert heads(board) == got, (
            f"a rebuild at the same seat composes something else: {got!r}")


async def test_a_board_rebuilt_only_from_events_keeps_the_wide_build_columns(
        monkeypatch):
    await _stale_when_deaf(monkeypatch, COLUMNS)


async def test_a_board_rebuilt_only_from_events_keeps_the_wide_build_sections(
        monkeypatch):
    await _stale_when_deaf(monkeypatch, SECTIONS)


async def test_the_next_paint_builds_at_the_new_seat_columns(monkeypatch):
    await _repaired_at_next_paint(monkeypatch, COLUMNS)


async def test_the_next_paint_builds_at_the_new_seat_sections(monkeypatch):
    await _repaired_at_next_paint(monkeypatch, SECTIONS)
