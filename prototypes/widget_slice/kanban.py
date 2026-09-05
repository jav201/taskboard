"""The board surface — the widget's widest size class.

Design decisions, each one earned earlier today:

* **Columns are weighted by content, not equal.** On the real board the phase
  distribution is 24/0/2/5; equal columns spend ~60% of the screen on emptiness
  and truncate the one column that has anything in it.
* **A task is a WIDGET, not a line of box-art.** That is what buys focus, hover,
  per-card motion and a real :focus indicator — none of which the shipped
  renderer can express.
* **There is NO parallel nav model.** Movement is derived from the widget tree,
  so the drawn order and the cursor order cannot drift apart. Maintaining a
  second model of "what is on screen" is what produced the cursor bugs in the
  earlier box-art variants: the render was patched, the model was not.
"""
from __future__ import annotations

from datetime import date

from textual.containers import Vertical, VerticalScroll
from textual.widgets import Static

from taskboard.models import parse_iso


def days_left(task, today: date):
    d = parse_iso(task.due_date)
    return None if d is None else (d - today).days


# -- THE BOARD'S ONE MEASURE -------------------------------------------------
# Every surface a phase draws — its head, its cards, its empty seat — stands in
# the same SEAT (the widget width `1fr` resolves to inside the scrolling list)
# and must close on the same cells. Measured apart they cannot: for six
# languages the head's rule, band, axis or span landed one cell off its items'
# and each one grew a private compensation (PENDING item 4).
#
# The CARD is the reference, because it is the surface the reader reads:
#   * Textual hands `TaskCard` a content box of `seat - CARD_BOX`, the two
#     cells `.kb-card { padding: 0 1 }` costs it, and the box starts one cell
#     in from the seat's left edge;
#   * `render_card` then spends that padding a SECOND time (`size.width - 2`)
#     before calling the kit, so a card ROW is `seat - CARD_BOX - CARD_OWN`
#     cells wide. The second spend is slack the card keeps at its right; it is
#     stated here rather than corrected, because the row width it produces is
#     what is already on screen and what every language is drawn against.
# The head and the empty seat are handed the SAME number and carry the SAME
# one-cell left inset (`.col-head`/`.kb-empty { padding-left: 1 }`, the base
# kit's tcss), so the three surfaces share an origin AND an edge by
# construction instead of by arithmetic luck.
CARD_BOX = 2      # `.kb-card { padding: 0 1 }` — what Textual takes off the seat
CARD_OWN = 2      # ... and what `render_card` takes off `size.width` again


def row_width(seat_w: int) -> int:
    """The row width EVERY board surface draws into, given its widget seat."""
    return max(8, seat_w - CARD_BOX - CARD_OWN)


class TaskCard(Static):
    """One task. Focusable, hoverable, and it knows its own coordinates."""
    can_focus = True

    def __init__(self, task, board, col: int, row: int, tokens, **kw):
        super().__init__(**kw)
        # NOTE: `task` is taken — Widget/MessagePump exposes an asyncio task
        # property with no setter. Collides silently until you assign.
        self.item = task
        self.board = board
        self.col = col
        self.row = row
        self.tok = tokens
        # SPLIT only: this card is a row of the driving list, so it renders
        # through the kit's compact `master_row` and can carry the cursor.
        # Both stay False everywhere else, which is why the columns and
        # sections branches render byte-for-byte as before.
        self.compact = False
        self.cursor = False
        # the derived fields the detail pane reads back, defined before the
        # first paint so a focus that lands early has something to read
        self.meta: dict = {}
        self.chip, self.tone = "", tokens["mut"]
        # the seat `render()` last composed at; -1 so the first paint composes
        self._painted_w = -1

    def render(self):
        """Compose at the seat we are ABOUT TO DRAW AT (F-16).

        `on_resize` is not enough, because Textual guarantees the RE-RENDER but
        not the EVENT. `Screen._refresh_layout` calls `_size_updated` on every
        widget in the compositor's layers — which sets `_size` and dirties the
        widget — but posts `Resize` only for the ones its MAP DIFF calls new or
        resized. A lazy `Compositor.full_map` rebuild absorbs the new geometry
        into that map first, so the diff sees nothing and `on_resize` never
        fires. Measured, columns branch, 3 of 30 sweeps: four DOING cards
        mounted at seat 0, both `on_mount` paints spent at the 20-cell
        fallback, `_size` then set 0 -> 33 with no `Resize`, bake held for good.
        """
        if self._painted_w != self.size.width:
            self._painted_w = self.size.width
            self.render_card()
        return super().render()

    def set_cursor(self, on: bool) -> None:
        """Called ONLY by KanbanBoard.on_card_focused, which is the single
        authority for where the cursor is — two writers is how you get two
        cursors on screen."""
        if self.cursor != on:
            self.cursor = on
            self.render_card()

    def on_mount(self) -> None:
        self.render_card()
        # at mount time the layout may not have run yet, so size.width can be
        # the 20-cell fallback; re-render once the real width exists, or a
        # narrow column keeps a card cut mid-row until the next resize
        self.call_after_refresh(self.render_card)

    def render_card(self) -> None:
        """The card's STRUCTURE comes from the active language's kit — marker,
        leaders, numbering and chip treatment all change with the language,
        not only the colours (PENDING.md item 0)."""
        t, b, k = self.item, self.board, self.tok
        today = date.today()
        d = days_left(t, today)
        urgent = False
        if b.is_done(t):
            chip, tone = "done", k["dim"]
        elif getattr(t, "blocked", False):
            chip, tone, urgent = "blk", k["alert"], True
        elif d is None:
            chip, tone = "--", k["dim"]
        elif d < 0:
            chip, tone, urgent = f"{-d}d!", k["alert"], True
        elif d <= 3:
            chip, tone, urgent = f"{d}d", k["warn"], True
        else:
            chip, tone = f"{d}d", k["mut"]

        # width MINUS the card's own horizontal padding (0 1): the row must
        # fit the CONTENT box. With height:1 an overflow was silently clipped;
        # with height:auto (2-row cards) it WRAPS into a phantom row — the
        # done-column chip landed alone on line 2. Seen in the render.
        w = max(8, (self.size.width or 20) - 2)
        # the card is a MINI-WIDGET with per-language anatomy (card_rows):
        # row count, field choice and mechanism are the language's commitment
        # — swiss stays one row on purpose. The kit picks from `meta`.
        proj = b.project_by_id(t.project_id)
        meta = {
            "proj": getattr(proj, "name", "") if proj else "",
            "phase": t.phase,
            "phase_idx": b.phase_index(t),
            "n_phases": max(1, len(b.phases)),
            "days": d,
            "prio": t.priority,
            "blocked": getattr(t, "blocked", False),
            "done": b.is_done(t),
        }
        self.meta = meta
        self.chip, self.tone = chip, tone
        if self.compact:
            self.update(k.master_row(t.title, chip, tone, w, self.cursor))
            return
        self.update("\n".join(k.card_rows(t.title, chip, tone, w,
                                          idx=self.row, urgent=urgent,
                                          meta=meta)))

    def on_resize(self) -> None:
        self.render_card()

    def on_focus(self) -> None:
        self.post_message(CardFocused(self))


from textual.message import Message   # noqa: E402


class CardFocused(Message):
    """Bubbles so the hero can follow the cursor."""
    def __init__(self, card: TaskCard) -> None:
        super().__init__()
        self.card = card


class PhaseColumn(VerticalScroll):
    """One phase. Its width was decided by how much it holds."""

    def __init__(self, name: str, count: int, tokens, width: int = 14,
                 idx: int = 0, **kw):
        super().__init__(**kw)
        self.phase_name = name
        self.count = count
        self.tok = tokens
        self.head_w = width
        self.idx = idx

    def head_widget(self) -> Static:
        """Built explicitly, NOT via compose(): compose runs lazily on mount, so
        children mounted immediately after row.mount(col) would land ABOVE the
        composed header. Verified by looking at the render -- the headers came
        out in a staircase below the first cards.

        The head's MECHANISM is the language's: drawn 3x5 count sprites in
        naught, numbered params over an aluminium rule in corgi, letterspaced
        caps in swiss..."""
        return Static(
            self.tok.head(self.phase_name, self.count, self.head_w, self.idx),
            classes="col-head")


def weighted_widths(counts: list[int], total_w: int, floor: int = 13) -> list[int]:
    """Width proportional to content, with a floor so an empty phase still shows
    its (informative) emptiness. Never returns a negative width — the earlier
    box-art variant did, and broke the frame at 24 columns."""
    n = len(counts)
    if n == 0:
        return []
    floor = min(floor, max(3, total_w // n))
    free = max(0, total_w - floor * n)
    total = max(1, sum(counts))
    out = [floor + (round(free * c / total) if free else 0) for c in counts]
    drift = total_w - sum(out)
    out[-1] = max(3, out[-1] + drift)          # absorb rounding, never below 3
    return out


class KanbanBoard(Vertical):
    """The board. Rebuilt only when the task set changes, not on every tick."""

    def __init__(self, board, tokens, **kw):
        super().__init__(**kw)
        self.board = board
        self.tok = tokens
        self.cards: list[list[TaskCard]] = []
        self._built_w = -1
        self._cursor: TaskCard | None = None      # split: the driven row
        self._detail_w = 0                        # split: 0 = degraded away
        self._detail: Static | None = None        # split: the pane THIS build
        # mounted. Held as a REFERENCE and not looked up by id, because
        # `build()`'s `remove_children()` is asynchronous: for a beat the board
        # holds the previous build's `#kb-detail` too, and a lookup answers
        # with THAT one — the write lands in a widget about to be removed and
        # the live pane stays blank for good. Measured, not theorised
        # (PENDING, thirtieth pass: 4-7 permanent blanks in 30 runs).
        # the seat `render()` last checked; -1 so the first paint checks
        self._painted_w = -1

    def render(self):
        """Rebuild at the seat we are ABOUT TO DRAW AT (F-16, one level up).

        `on_resize` alone is not enough, for the reason `TaskCard.render`
        gives: Textual guarantees the RE-RENDER on a seat change but not the
        EVENT. The board's PUSH-PAINTED rows are the exposure. `.col-head` and
        `.kb-empty` are composed once, in `build()`, for a width derived from
        the BOARD's seat and NOT from their own — measured: in the columns
        branch a board resize does not move a head's own seat at all and the
        head's `render()` is never called, so a guard on the head could not see
        the change. The board's `render()` can, and it repairs every surface
        the build composes at once.
        """
        if self._painted_w != self.size.width:
            self._painted_w = self.size.width
            self._rebuild_if_seat_moved()
        return super().render()

    def build(self, show_archived: bool = False) -> None:
        from textual.containers import Horizontal
        from taskboard.views import phase_buckets

        self.remove_children()
        self.cards = []
        self._cursor = None
        self._detail_w = 0
        self._detail = None
        b, k = self.board, self.tok
        tasks = b.visible_tasks(show_archived)
        buckets = phase_buckets(b, tasks)
        counts = [len(x) for x in buckets]
        avail = max(20, (self.size.width or self.container_size.width or 100))
        self._built_w = avail

        # SECTIONS: a flat vertical list — full-width phase headers and
        # full-width cards (darkside's faithful form; 6 columns in a narrow
        # composition left ~7 chars of title, user-verdict "casi ilegible")
        if k.board_layout() == "sections":
            sc = VerticalScroll(classes="kb-flat")
            self.mount(sc)
            today = date.today()
            # the SEAT: the flat list reserves one cell for its scroll bar
            # (`scrollbar-size: 1 1`). Reserved whether or not the list
            # overflows — the safe direction, since a surface is never told it
            # is wider than it is. Head, card and empty seat all measure from
            # it through `row_width`, so they close on one cell.
            seat = avail - 1
            rw = row_width(seat)
            for ci, (name, bucket) in enumerate(zip(b.phases, buckets)):
                sc.mount(Static(k.head(name, len(bucket), rw, ci),
                                classes="col-head"))
                col_cards: list[TaskCard] = []
                if not bucket:
                    # the empty state carries the language: mascot + its voice.
                    # A sections row is FULL WIDTH, so `rw` clears `empty()`'s
                    # w>=14 mascot threshold at every board size — these six
                    # languages get the creature a narrow column cannot afford.
                    sc.mount(Static(k.empty(rw), classes="kb-empty"))
                else:
                    ordered = sorted(
                        bucket,
                        key=lambda t: (b.is_done(t),
                                       (days_left(t, today) if days_left(t, today)
                                        is not None else 9999)))
                    for ri, t in enumerate(ordered):
                        c = TaskCard(t, b, ci, ri, k, classes="kb-card")
                        sc.mount(c)
                        col_cards.append(c)
                self.cards.append(col_cards)
            return

        # SPLIT: a narrow driving list beside one expanded task (nord).
        # HIERARCHY.md's sidebar+detail — and its wording is why the detail
        # follows the REAL cursor rather than a fixed pick: "the list keeps
        # selection state; the detail pane is the only thing that changes".
        if k.board_layout() == "split":
            master_w, self._detail_w = k.panes(avail)
            row = Horizontal(classes="kb-split")
            self.mount(row)
            master = VerticalScroll(classes="kb-master")
            master.styles.width = master_w
            row.mount(master)
            if self._detail_w:
                detail = Static("", classes="kb-detail", id="kb-detail")
                detail.styles.width = avail - master_w
                row.mount(detail)
                self._detail = detail
            today = date.today()
            # the driving list's SEAT (its padding + the scrollbar's cell),
            # then the one measure every surface in it draws into
            hw = row_width(max(6, master_w - 3))
            for ci, (name, bucket) in enumerate(zip(b.phases, buckets)):
                master.mount(Static(k.head(name, len(bucket), hw, ci),
                                    classes="col-head"))
                col_cards: list[TaskCard] = []
                if not bucket:
                    # nord HAS an empty-state seat in the columns branch; the
                    # split must not silently take it away (PENDING item 7 is
                    # about languages that never had one, not about losing one)
                    master.mount(Static(k.empty(hw), classes="kb-empty"))
                else:
                    ordered = sorted(
                        bucket,
                        key=lambda t: (b.is_done(t),
                                       (days_left(t, today) if days_left(t, today)
                                        is not None else 9999)))
                    for ri, t in enumerate(ordered):
                        c = TaskCard(t, b, ci, ri, k, classes="kb-card")
                        c.compact = True
                        master.mount(c)
                        col_cards.append(c)
                self.cards.append(col_cards)
            self._cursor = None
            self.call_after_refresh(self._seed_detail)
            return

        widths = weighted_widths(counts, avail)

        row = Horizontal(classes="kb-row")
        self.mount(row)
        today = date.today()
        for ci, (name, bucket, cw) in enumerate(zip(b.phases, buckets, widths)):
            # the column's SEAT: its width minus its right padding and the cell
            # a vertical scrollbar takes when the column overflows (reserved
            # always — an exact-fit rule WRAPS in a scrolled column and doubles
            # the head row). Then the one measure, as in the other two branches.
            cseat = max(6, cw - 2)
            crw = row_width(cseat)
            col = PhaseColumn(name, len(bucket), k, width=crw,
                              idx=ci, classes="kb-col")
            col.styles.width = cw
            row.mount(col)
            col.mount(col.head_widget())
            col_cards: list[TaskCard] = []
            if not bucket:
                # the empty state carries the language: mascot + its voice
                col.mount(Static(k.empty(crw), classes="kb-empty"))
            else:
                ordered = sorted(
                    bucket,
                    key=lambda t: (b.is_done(t),
                                   (days_left(t, today) if days_left(t, today)
                                    is not None else 9999)))
                for ri, t in enumerate(ordered):
                    c = TaskCard(t, b, ci, ri, k, classes="kb-card")
                    col.mount(c)
                    col_cards.append(c)
            self.cards.append(col_cards)

    # -- SPLIT: the detail pane, and the ONE place the cursor is written -----
    def _first_card(self) -> TaskCard | None:
        for col in self.cards:
            if col:
                return col[0]
        return None

    def _seed_detail(self) -> None:
        """The pane must never be blank. If nothing has taken focus yet the
        leading row drives it — and it is named for what it is (the first row
        of the first non-empty phase), not "the most urgent task", which is a
        claim this seat cannot make."""
        if self._cursor is None:
            card = self._first_card()
            if card is not None:
                self._drive(card)

    def _drive(self, card: TaskCard) -> None:
        if self._cursor is card:
            return
        if self._cursor is not None:
            self._cursor.set_cursor(False)
        self._cursor = card
        card.set_cursor(True)
        pane = self._detail
        if not self._detail_w or pane is None:
            return                          # degraded to master-only
        pane.update("\n".join(self.tok.detail_rows(
            card.item.title, card.chip, card.tone, self._detail_w,
            card.meta)))

    def on_card_focused(self, msg: CardFocused) -> None:
        """Deliberately does NOT stop the message: the hero follows the cursor
        too (app.py's own handler), and swallowing it here would silently
        freeze the hero on the split."""
        if self.tok.board_layout() == "split":
            self._drive(msg.card)

    def on_resize(self) -> None:
        """The event, when it comes. It is not guaranteed — see `render`."""
        self._rebuild_if_seat_moved()

    def _rebuild_if_seat_moved(self) -> None:
        """Rebuild only when the width actually changed — a rebuild is
        content-cold work and must not ride every resize event."""
        w = max(20, self.size.width or 0)
        if w != self._built_w and w > 20:
            self.build()

    # -- movement derived from the tree; there is no second model ------------
    def move(self, dcol: int, drow: int, current: TaskCard | None) -> TaskCard | None:
        if not any(self.cards):
            return None
        if current is None:
            for col in self.cards:
                if col:
                    return col[0]
            return None
        ci, ri = current.col, current.row
        if drow:
            col = self.cards[ci]
            if col:
                return col[max(0, min(len(col) - 1, ri + drow))]
            return current
        if dcol:
            step = 1 if dcol > 0 else -1
            j = ci + step
            while 0 <= j < len(self.cards):
                if self.cards[j]:
                    col = self.cards[j]
                    # land on the VISUALLY adjacent card: match the SCREEN
                    # row, not the index — index parity lied when columns
                    # scroll or hold different counts (user-reported: "no se
                    # mueve como esperaría uno")
                    cy = current.region.y
                    vis = [c for c in col if c.region.height]
                    pool = vis or col
                    return min(pool, key=lambda c: abs(c.region.y - cy))
                j += step
        return current
