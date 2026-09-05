"""F-16: a `TaskCard` must compose at the seat it is ABOUT TO BE DRAWN AT.

WHY THIS FILE EXISTS. `prototypes/capture_languages.py`'s settle failed loud on
3 of 30 cross-process sweeps -- always the COLUMNS branch (`board instrument`,
`board industrial`, `board naught`), always the four DOING-column cards, always
holding a paint composed at the 20-cell fallback while their real seat was 31
or 33 (`.fast-dev-flow/03-increments/inc20.md` §5). It never came right: a
probe kept the loop alive 640 iterations / 19.5 s past the bound and the cards
still read `Design home...` where their seat draws `Design homepage moc...`.

THE MECHANISM, MEASURED (Textual 8.2.8). `on_resize` was the card's only
repair once its two mount-time paints were spent, and Textual guarantees the
RE-RENDER but not the EVENT:

  * `Screen._refresh_layout` (`screen.py:1360`) calls `_size_updated` on every
    widget in the compositor's layers -- which sets `_size` and dirties the
    widget -- but posts `Resize` only for `shown | resized`, both derived from
    a DIFF of the new compositor map against the previous one;
  * `Compositor.full_map` (`_compositor.py:485`) rebuilds that map LAZILY when
    `update_widgets` has invalidated it, which is what a freshly mounted widget
    causes. The rebuild writes the new geometry into the map and posts nothing.

When the lazy rebuild lands first, the next reflow's diff sees no change, no
`Resize` is posted, `_size` moves anyway, and `on_resize` never fires. The
card's own timeline at a real wedge, from the instrumented probe:

    on_mount           seat=0  -> w=18
    render             seat=0  -> w=18      (the `call_after_refresh` repair,
                                             spent before the layout ran)
    GEO[LAZY-full_map] None -> (33, 2)
    _size_updated      0x0 -> 33x2  ret=True
    (nothing, ever again)

WHAT THESE TESTS REPRODUCE, AND WHAT THEY DO NOT. The missing POST is a race:
it needs a fresh interpreter and it lands about one sweep in ten, so driving it
here would be a test that fails for the wrong reason nine times out of ten.
What the race leaves behind is not a race -- it is a card whose seat moved with
no repair on the other end of the event -- and `DeafCard` below reaches that
state in one class: it hears the `Resize` and does nothing with it, which from
the card's side is the same hole. `PreFixCard` then quotes the paint path as it
stood at `2817550`, so assertion (a) keeps proving the hole is real long after
that commit stops being anyone's memory.
"""
from __future__ import annotations

import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes" / "widget_slice"))

from taskboard import language as LG                              # noqa: E402
from kanban import TaskCard                                       # noqa: E402

#: industrial is one of the three COLUMNS languages the wedge was measured on,
#: and its `card_rows` truncates the title with the same `…` the capture's diff
#: pointed at.
KIT = LG.kit("industrial")

TITLE = "Design homepage mockups"
NARROW_SEAT = 20            # the seat a column gives a card: the title truncates
WIDER = 13                  # ... and how much wider the next layout makes it


class Task:
    """The fields `render_card` reads off a task. `due_date=None` keeps the
    chip at `--`, so nothing here depends on today's date."""
    title = TITLE
    due_date = None
    phase = "DOING"
    priority = "high"
    project_id = None
    blocked = False


class StubBoard:
    """The four calls `render_card` makes into the board, and nothing else."""
    phases = ("TODO", "DOING", "DONE")

    def is_done(self, task) -> bool:
        return False

    def project_by_id(self, pid):
        return None

    def phase_index(self, task) -> int:
        return 1


def deafen(monkeypatch) -> list[int]:
    """Open the hole F-16 opens, without the race: take away the card's ONE
    event-side repair and record the events it would have repaired on.

    In the wild the `Resize` is never POSTED; here it is never ACTED ON, and a
    card cannot tell the two apart. The patch goes on `TaskCard` ITSELF and not
    on a subclass, because Textual dispatches the handler of EVERY class in the
    MRO -- a subclass overriding `on_resize` still runs the base's, measured.
    The events are recorded rather than dropped so the tests can assert one
    really arrived; an empty list would mean the fixture stopped exercising
    anything.
    """
    seen: list[int] = []
    monkeypatch.setattr(TaskCard, "on_resize",
                        lambda self: seen.append(self.size.width))
    return seen


class PreFixCard(TaskCard):
    """`TaskCard`'s paint path as it stood at `2817550`: repaired from EVENTS
    only. Quoted here rather than reached for through git, because assertion
    (a)'s whole job is to keep proving the fixture has teeth."""
    render = Static.render


class OneCardApp(App):
    """One card in a column of a fixed width -- the columns branch, minus the
    board. `.kb-card`'s rule is quoted from `widget_slice/widget.tcss`: the two
    cells its padding costs are what makes the column `NARROW_SEAT + 2` wide.
    """
    CSS = ("#col { width: auto; }\n"
           ".kb-card { width: 1fr; height: auto; max-height: 3; padding: 0 1; }")

    def __init__(self, card_cls=TaskCard) -> None:
        super().__init__()
        self.card_cls = card_cls

    def compose(self) -> ComposeResult:
        col = Vertical(id="col")
        col.styles.width = NARROW_SEAT + 2
        with col:
            yield self.card_cls(Task(), StubBoard(), 1, 0, KIT, classes="kb-card")


def stale(card) -> bool:
    """CONDITION C's oracle, the shipped one (`capture_languages._stale_paint`):
    ask the card what it would draw at its PRESENT seat with `update`
    intercepted, and compare that with what it is showing. Copied rather than
    imported because importing `capture_languages` sets `TEXTUAL_ANIMATIONS`
    for the whole process."""
    got: list = []
    card.update = got.append
    try:
        card.render_card()
    finally:
        del card.update
    return bool(got) and got[0] != card.content


async def widen(app, pilot) -> None:
    """The layout hands the card 13 more cells."""
    app.query_one("#col").styles.width = NARROW_SEAT + 2 + WIDER
    await pilot.pause()


async def test_a_card_repaired_only_from_events_keeps_the_narrow_bake(monkeypatch):
    """(a) The fixture has teeth: the pre-fix paint path wedges.

    Its two mount-time paints are spent, the resize arrives and is ignored, and
    nothing else in the card looks at the seat again -- so it holds a bake
    composed 13 cells narrower for as long as it lives. If a future change
    makes the shipped card repair from somewhere else, THIS goes red first and
    (b) below stops being evidence.
    """
    seen = deafen(monkeypatch)
    app = OneCardApp(PreFixCard)
    async with app.run_test(size=(60, 10)) as pilot:
        await pilot.pause()
        card = app.query_one(PreFixCard)
        narrow = card.render_line(0).text
        assert card.size.width == NARROW_SEAT, card.size
        assert "…" in narrow, f"the title must truncate at {NARROW_SEAT}: {narrow!r}"

        await widen(app, pilot)

        assert card.size.width == NARROW_SEAT + WIDER, card.size
        assert seen, "the fixture never delivered the resize it ignores"
        assert stale(card), (
            "the pre-fix card repaired itself -- the wedge is no longer what "
            "this file reproduces")
        assert card.render_line(0).text.rstrip() == narrow.rstrip(), (
            f"still the narrow bake: {card.render_line(0).text!r}")


async def test_the_next_paint_composes_at_the_new_seat(monkeypatch):
    """(b) And the shipped card repairs at its next paint, which is the fix.

    `render()` is the one hook Textual DOES guarantee on a seat change:
    `_size_updated` dirties the widget, so the compositor asks it for its
    content again whether or not an event was posted. Composing there makes the
    stale bake unreachable instead of unlikely -- and the card here is deaf to
    `Resize` by construction, so the repair cannot have come from `on_resize`.
    """
    seen = deafen(monkeypatch)
    app = OneCardApp(TaskCard)
    async with app.run_test(size=(60, 10)) as pilot:
        await pilot.pause()
        card = app.query_one(TaskCard)
        narrow = card.render_line(0).text

        await widen(app, pilot)
        wide = card.render_line(0).text

        assert seen, "the fixture never delivered the resize it ignores"
        assert not stale(card), (
            "the card is drawing a paint composed at a seat it no longer has: "
            f"content {str(card.content)[:80]!r}")
        assert wide.rstrip() != narrow.rstrip(), (
            f"the seat moved {WIDER} cells and the drawn row did not -- the "
            f"fixture is not exercising truncation: {wide!r}")
        assert "Design homepage" in wide, wide
