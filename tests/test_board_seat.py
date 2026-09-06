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


#: the board mounts exactly ONE `.col-head` per phase, in both branches this
#: file drives (columns puts each in its own column, sections puts all three in
#: one flat list). The number the tree must come back to once a build has
#: settled -- and the number `settled_heads` waits for.
NHEADS = len(StubBoard.phases)

#: the bound on a settle. Measured rather than guessed: `_f18_lifetime.py` read
#: every run's second pause at one generation, in 30 of 30. Sixty is two orders
#: of margin over the only number anyone measured, and it is a BOUND and not a
#: budget -- reaching it raises.
SETTLE_FRAMES = 60


def drawn_heads(app, board) -> int:
    """How many `.col-head` the COMPOSITOR says it is drawing, with a clip that
    has area. Asked of `visible_widgets` and not of the widget's own region,
    for the reason `capture_languages._not_at_rest` gives at length: a region
    is in SCREEN space and keeps growing past the fold, so a raw slice reads
    whatever is at those coordinates. The compositor's map holds only what it
    actually draws."""
    vis = app.screen._compositor.visible_widgets
    n = 0
    for w in board.query(".col-head"):
        box = vis.get(w)
        if box is None:
            continue
        area = box[0].intersection(box[1])
        if area.width and area.height:
            n += 1
    return n


async def settled_heads(app, pilot, board, what, also=None) -> list[str]:
    """The tree's `.col-head` row, sampled ONLY once the build has settled.

    F-18. This is the seat the finding lives at. What stood here was one
    `await pilot.pause()` and an immediate read, and one pause after a resize
    is not a settled frame -- measured over 30 runs of both branches
    (`prototypes/out/_f18_lifetime.py`, tree/drawn counts per pause):

        pause 1: the tree held BOTH generations -- six heads where the board
                 has three --  in 2 of 30 runs
        pause 1: the compositor was drawing NO column head at all in 8 of 30
        pause 2: three heads, three drawn, in 30 of 30

    The cause is in `KanbanBoard.build()` and it is not a defect: it calls
    `remove_children()`, which is ASYNCHRONOUS (its own `__init__` comment says
    so and paid for the knowledge), then mounts the new generation -- and
    `build()` cannot await the removal, because its other caller is `render()`.
    So for one beat the DOM holds two generations. **The SCREEN never does**:
    0 of 30 runs ever had the compositor drawing more than three, which is why
    the repair is here and not in `build()`, and
    `test_the_screen_never_shows_two_generations_of_heads` is that fact
    asserted rather than trusted.

    So the wait is for the CONDITION the assertion is about instead of for a
    number of pauses: one generation in the tree, the same one on two
    consecutive reads (which is what rules out sampling the OLD three before
    the new three have landed), and any extra predicate the caller needs.
    Failing the bound raises and names what it was waiting for -- a settle that
    gives up silently would hand back the bad sample this exists to prevent.
    """
    prev: list[str] | None = None
    for _ in range(SETTLE_FRAMES):
        got = heads(board)
        if (len(got) == NHEADS and got == prev
                and (also is None or also())):
            return got
        prev = got
        await pilot.pause()
    raise AssertionError(
        f"the board never settled in {SETTLE_FRAMES} frames: {what}; last "
        f"read {len(prev or [])} heads where the board mounts {NHEADS}: "
        f"{prev!r}")


async def start(app, pilot):
    """Mount, then build once explicitly -- which is what the real app does
    (`app.py:start_widget` calls `kb.build()`); the pre-fix board with a
    deafened `on_resize` would otherwise never build at all and the test would
    be comparing two empty lists."""
    await pilot.pause()
    board = app.query_one(KanbanBoard)
    board.build()
    await settled_heads(app, pilot, board, "the first explicit build")
    return board


async def narrow(app, pilot) -> None:
    """The layout takes 40 cells off the board. Delivering the resize is all
    this does; WAITING for what the resize causes is `settled_heads`."""
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
        after = await settled_heads(app, pilot, board, "the oracle rebuild")
        assert after != wide, (
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
        # F-18: the board's rebuild is what this assertion is ABOUT, so the
        # sample waits for it -- built at the new seat, and one generation of
        # heads in the tree. The predicate is passed rather than asserted
        # after, so a board that rebuilds at the WRONG seat times out here
        # naming the seat instead of failing three lines down on a head row.
        got = await settled_heads(
            app, pilot, board, f"a rebuild at the new seat ({NARROW})",
            also=lambda: board._built_w == NARROW)

        assert seen, "the fixture never delivered the resize it ignores"
        assert board._built_w == NARROW, (
            f"the board is still built for {board._built_w}, seat is {NARROW}")
        assert got != wide, (
            f"the seat lost {WIDE - NARROW} cells and the head did not move: "
            f"{got!r}")
        # and what it shows IS what the present seat composes
        board.build()
        again = await settled_heads(app, pilot, board, "the oracle rebuild")
        assert again == got, (
            f"a rebuild at the same seat composes something else: {got!r} "
            f"vs {again!r}")


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


# ===========================================================================
# F-18 — the DOM's double-generation window, and the screen's absence of one
# ===========================================================================
async def _no_two_generations_on_screen(kit) -> None:
    """The finding asserted rather than trusted: across every frame of a
    resize, the COMPOSITOR never draws more than one generation of heads.

    This is the claim that decides where F-18 gets repaired. `build()` removes
    the old heads asynchronously and mounts the new ones without awaiting the
    removal -- it cannot await it, `render()` is one of its two callers -- so
    the TREE holds six heads for a beat where the board has three. Measured:
    2 of 30 runs at the first pause. If the SCREEN held six too, a user could
    read a duplicated board for a frame and the repair would belong in
    `build()`. It does not: 0 of 30, and this walks every frame of the resize
    rather than the one the probe sampled.

    The tree count is recorded beside it and deliberately NOT asserted -- an
    assertion that the DOM never doubles would be a claim about Textual's
    removal scheduling, which this repo does not own and which the working
    fixture would have to fight.
    """
    app = OneBoardApp(kit, KanbanBoard)
    async with app.run_test(size=(120, 30)) as pilot:
        board = await start(app, pilot)
        app.query_one("#wrap").styles.width = NARROW
        drawn: list[int] = []
        tree: list[int] = []
        for _ in range(SETTLE_FRAMES):
            await pilot.pause()
            drawn.append(drawn_heads(app, board))
            tree.append(len(board.query(".col-head")))
            if len(tree) >= 3 and tree[-3:] == [NHEADS] * 3:
                break
        assert max(drawn) <= NHEADS, (
            f"the compositor drew {max(drawn)} column heads where the board "
            f"has {NHEADS} -- a user could see two generations at once; "
            f"drawn per frame {drawn}, tree per frame {tree}")
        assert board._built_w == NARROW, board._built_w
        assert tree[-1] == NHEADS and drawn[-1] == NHEADS, (drawn, tree)


async def test_the_screen_never_shows_two_generations_of_heads_columns():
    await _no_two_generations_on_screen(COLUMNS)


async def test_the_screen_never_shows_two_generations_of_heads_sections():
    await _no_two_generations_on_screen(SECTIONS)
