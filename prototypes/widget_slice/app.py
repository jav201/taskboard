"""taskboard — WIDGET SLICE prototype.

The thesis: taskboard's own README calls it a "frameless desktop widget", but it
is built as a full-screen dashboard. A widget is an APERTURE, not a scope — the
surface is small, what stands behind it need not be (engine.py).

What this slice demonstrates, all of it absent from the shipped app:
  * size-CLASS routing — the app adapts to its own width instead of a view key
  * a DRAWN dot-matrix hero (taskboard/hero.py) — it renders, it doesn't label
  * real widgets: can_focus, :hover, :focus with border + weight (two channels)
  * TCSS transitions + one level="basic" state-change animation
  * monochrome + ONE accent, plus reserved semantic hues
  * curated Footer, "?" keymap, command palette with every action registered
  * loading / empty / error states
  * two cadences in SEPARATE worker groups (fast hero, slow filesystem)

Run:  python prototypes/widget_slice/app.py
Keys: every key is on the footer legend; `?` is the full map. No key needs shift.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from textual import work
from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.color import Color
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.keys import format_key
from textual.screen import ModalScreen, Screen
from textual.widgets import Footer, Static

# Textual's Footer collapses a group into "keys… GroupLabel" and DROPS every
# per-key description (textual 8.2.8 _footer.py:269 passes ""). `combine_groups`
# is dead metadata there — compose() never reads it. So a group is only ever
# spent where the keys are a numbered family the label can honestly name; the
# letter keys carry their own words instead, which is what the user was missing.
G_VIEW = Binding.Group("Views")


def key_of(binding: Binding) -> str:
    """EVERY key a user may press for this binding, in the form it prints.

    All of them, not the first: `escape,q` printed as "esc" is how a working
    key ends up indicated nowhere.

    `format_key` is Textual's own name->glyph table (question_mark -> `?`,
    escape -> `esc`); a legend that printed the raw binding name told the user
    to type "question_mark". It has no entry for the brackets, so those bindings
    carry an explicit `key_display` — see ConfigScreen."""
    if binding.key_display:                # one display for the whole binding,
        return binding.key_display         # not one per alias ("space / space")
    return " / ".join(format_key(k) for k in binding.key.split(","))


def hint_row(bindings, sep: str = " · ") -> str:
    """A screen's printed hint line, DERIVED from its own BINDINGS.

    The defect this exists to prevent: the gallery printed `t language · esc
    close` while `t` was dead there (a ModalScreen shadows the App's bindings),
    so the one on-screen legend the modals had was a lie. A hand-written hint
    drifts the moment a binding moves; this one cannot."""
    return sep.join(f"{key_of(b)} {b.description.lower()}"
                    for b in bindings if isinstance(b, Binding) and b.show)


# rich's OWN definition of a tag: a bracket is markup only when the next
# character is `[a-z#/@]` (rich.markup.RE_TAGS). `[ ]` and `[X]` are literal
# text on screen, so a width measured with a looser pattern reads nord's and
# industrial's checkbox as zero cells wide and says any row fits.
_TAG = re.compile(r"\[[a-z#/@][^\[]*?\]")


def plain_len(markup: str) -> int:
    """The cells a markup string actually costs. Used to CHOOSE a layout, so
    it has to agree with what renders — `verify_language.grey_is_rich` is the
    law that holds this pattern to rich's parser."""
    return len(_TAG.sub("", markup.replace("\\[", "\x00")))


sys.path.insert(0, str(Path(__file__).resolve().parent))
from taskboard.engine import ALERT, CALM, NOTICE, WARN, Engine   # noqa: E402
from taskboard import hero as HERO                               # noqa: E402
from taskboard import language as LG                             # noqa: E402
from taskboard import motion as MO                               # noqa: E402
import views_widget as VW                                        # noqa: E402
from kanban import CardFocused, KanbanBoard, TaskCard, days_left as kb_days  # noqa: E402
from taskboard.models import Board, default_board_path         # noqa: E402

# --------------------------------------------------------------------------
# tokens — monochrome + ONE accent, plus RESERVED semantic hues.
# every hue verified above the HLS s=0.15 cliff, not HSV (CEILINGS.md).
# --------------------------------------------------------------------------
# The visual LANGUAGE is a user choice, not the medium's verdict
# (tui-design/LANGUAGES.md). These globals are rebound by apply_theme().
from taskboard import themes as TH                              # noqa: E402

THEME = "instrument"
GROUND = INK = MUT = DIM = ACCENT = WARN_HUE = ALERT_HUE = "#000000"


def apply_theme(name: str) -> None:
    global GROUND, INK, MUT, DIM, ACCENT, WARN_HUE, ALERT_HUE, TONE, KIT, THEME
    th = TH.THEMES[name]
    THEME = name
    GROUND, INK, MUT = th["ground"], th["ink"], th["mut"]
    DIM, ACCENT = th["dim"], th["accent"]
    WARN_HUE, ALERT_HUE = th["warn"], th["alert"]
    # `calm` token: a language may refuse to spend its accent on calm
    # severities (naught: red is rationed to alarm — the Nothing sheets)
    calm = th.get("calm", ACCENT)
    TONE = {CALM: calm, NOTICE: calm, WARN: WARN_HUE, ALERT: ALERT_HUE}
    # the language's STRUCTURE kit — every non-hero surface renders through it
    KIT = LG.kit(name)


apply_theme("instrument")

# THE WORKER GROUPS — the app's one N-of-M, and the config screen's live
# radio set. Every signal runs in exactly one of these loops: `tick_fast` and
# `tick_slow` below call `Engine.run_group` with these names and `run_all`
# iterates them, so a signal moved into a group no worker runs would simply
# stop being computed. That is the consequence that makes this a real seat
# and not a demo — and it is a SELECTION, not a setting, which is the
# distinction the checkbox honestly could not find a seat for (PENDING, the
# fiftieth pass).
#
# ONE DECLARATION, held against the engine's own source by verify_language
# so this tuple and `run_all`'s cannot drift apart.
WORKER_GROUPS = ("fast", "slow")




class Hero(Static):
    """The aperture's signature: a drawn dot-matrix metric. RENDERS, not labels."""
    can_focus = True

    def __init__(self, **kw):
        super().__init__(**kw)
        self._sev = CALM
        self._sig_id = ""

    def show(self, signal, reading, width: int, series=None) -> None:
        """Gather this seat's inputs and hand them to the ONE drawing seat.

        There is no hero drawing in this file. `taskboard/hero.py` holds every
        style branch, the dead-columns load, the flap faces and the visual-row
        trim; this prototype and the shipped aperture are two CALLERS of it.
        The fork this replaces had drifted four ways in eleven passes (a
        metrics-blind caption wrap, its own `naught7` dispatch, a `dot` branch
        that drew flap FIGURES on unpainted faces, and no reader for
        `hero_plot`/`hero_fit`) — each one invisible until someone diffed two
        renders of the same language. A seat that cannot be forked cannot
        drift, so the adapter is all that may live here.

        What this seat OWNS, because it is the widget and hero.py is not:
        the widget's real width and height, and the severity flash.
        """
        tone = TONE[reading.severity]
        # Frames must be built from the widget's OWN width, not the caller's
        # estimate: an over-wide frame WRAPS and every line doubles. Caught by
        # looking at the render, invisible in the code.
        width = min(width, self.size.width or width)
        # ROW BUDGET: a drawn hero that exceeds the widget's height clips
        # mid-glyph (glance) or starves every other region off-screen (widget).
        # The vertical twin of the wrapped-frame bug, and just as invisible in
        # the source. hero.draw trims VISUAL rows, not list entries.
        max_rows = max(5, (self.size.height or 12))
        self.update(HERO.draw(KIT, str(reading.value), reading.caption,
                              reading.detail, tone, width, max_rows,
                              series=series, source=signal.id))

        if reading.severity != self._sev and self._sig_id:
            # the flash decays at the LANGUAGE's pace and curve
            self.styles.background = Color.parse(tone).with_alpha(0.22)
            self.styles.animate("background", Color.parse(GROUND),
                                duration=KIT.tempo_s * 3.5, easing=KIT.easing,
                                level="basic")
        self._sev, self._sig_id = reading.severity, signal.id


class Tile(Static):
    """A small signal readout. Focusable and hoverable — real widgets, not box-art."""
    can_focus = True

    def __init__(self, signal, **kw):
        super().__init__(**kw)
        self.signal = signal

    def refresh_tile(self) -> None:
        s = self.signal
        r = s.last
        if r is None:
            # pending state = the language's SPINNER, not three dots
            tick = getattr(self.app, "ticker", None)
            self.update(KIT.spinner(tick.n if tick else 0)
                        + f" [{DIM}]{s.label[:14]}[/]")
            return
        if not r.ok:
            self.update(f"[{ALERT_HUE}]{s.label[:14]:<14} err[/]")
            self.tooltip = s.last_error
            return
        tone = TONE[r.severity]
        # At board size a tile gets ~19 cells; a 14-char label plus padding
        # cropped EVERY value off, so the widest size class showed six chrome
        # labels and no data. Value first, label to whatever room is left —
        # the row's structure (marker, separator, case) is the language's.
        w = max(8, (self.size.width or 24) - 2)
        ic = KIT.icon(s.id)                # the language's icon mechanism
        # the KPI GAUGE (data-viz axis): the value read against its own
        # threshold, in the language's meter family — needle at the midpoint
        # means "at threshold". Only when the row has room for it.
        g = ""
        try:
            num = int(r.value)
        except (TypeError, ValueError):
            num = None
        if num is not None and s.threshold and w >= 40:
            # the threshold TICK marks where "fine" ends on the same track
            g = " " + KIT.gauge(num, 0, max(num, s.threshold * 2), 10, tone,
                                thr=s.threshold)
        self.update((ic + " " if ic else "")
                    + KIT.tile_row(f"{r.value:>3}", s.label, tone,
                                   w - (14 if g else 0)) + g)
        self.tooltip = f"{s.help}  (every {s.cadence:g}s, {s.group} group)"


class Meter(Static):
    """Progress as discrete segments — honest about the cell grid."""

    def show(self, done: int, total: int, width: int, counts: list[int]) -> None:
        """Quantity is drawn with the language's OWN mechanism (language.METERS,
        dispatched on the `meter` token): discrete dots on a lattice, LCD ghost
        segments, sub-cell braille, one hairline, a boxed bar, a CRT decay
        ramp, a gradient — a MECHANISM each, not one bar recoloured.

        Width comes from the widget's own size: overflowing wraps line 1 and
        silently pushes the flow row out of a height:2 widget."""
        w = self.size.width or width
        self.update(KIT.meter(done, total, counts, w))


def checkable_block(k, w: int) -> list[str]:
    """THE CHECKABLE FAMILY as gallery rows: switch and checkbox, every state.

    They share the ROW UNIT — one control state per row, both bits side by
    side — because they share the AXIS. `checked_pairs` returns the same four
    pairs for both, derived from the registry, so this block is not written
    twice and cannot fall out of step with the state list.

    WHETHER THEY SHARE THE ROW IS MEASURED, and that is the gallery question
    passes 48 and 49 both deferred. Paired, two components cost FIVE rows;
    stacked they cost eight. Seven languages fit the paired block in the
    box's 52 columns. corgi, ledger and solari PRINT A WORD beside the
    control (`ON`, `posted`, `OFF`) and reach 54, 68 and 56 — so they stack.
    Reflow, never truncate; and never assume, because a row measured wrong
    wraps, and a wrapped row puts the caption under the wrong control, which
    is exactly what happened the first time the slider states were tried
    side by side.

    ONE SEAT, read by the screen AND by the acceptance check — the check
    asks this function for the block instead of rebuilding the arithmetic,
    which is the duplicated-oracle defect that cost pass 46 a hundred and
    fifty-eight false mismatches."""
    def lab(name):
        return f"[{MUT}]{name:<11}[/]"

    def duo(fn, ctl):
        return fn(False, ctl) + "  " + fn(True, ctl)

    def a_switch(on, st):
        return k.switch(on, 3, st)

    ctls = [c for c, _ in LG.checked_pairs("checkbox")]
    together = [
        lab("checkable")
        + f"[{DIM}]{'switch':<{plain_len(duo(a_switch, LG.DEFAULT)) + 2}}"
        + f"checkbox[/]  [{DIM}]off·on[/]",
        *[lab("") + duo(a_switch, c) + "  " + duo(k.checkbox, c)
          + f"   [{DIM}]{LG.control_of(c)}[/]" for c in ctls],
    ]
    if max(plain_len(r) for r in together) <= w:
        return together
    return [lab(nm if i == 0 else "") + duo(fn, c)
            + f"   [{DIM}]{LG.control_of(c)}[/]"
            + (f"  [{DIM}]off·on[/]" if i == 0 else "")
            for nm, fn in (("switch", a_switch), ("checkbox", k.checkbox))
            for i, c in enumerate(ctls)]


RADIO_OPTS = ("lo", "mid", "hi")
RADIO_SEL = 1                              # the CHECKED item
RADIO_FOCUS = 2                            # the item under the cursor


def radio_block(k, w: int) -> list[str]:
    """THE GROUP as gallery rows, and the one thing it exists to show is that
    the cursor and the choice are DIFFERENT ITEMS.

    Every row draws the same set with the same selection (`mid`) and the same
    cursor (`hi`), and only the group's control state changes down the block.
    So the reading the eye has to survive is not "what does focused look
    like" but "which of these three is chosen, while a different one is under
    the cursor" — the sibling-scoped version of the EDITED-is-not-FOCUSED
    problem the state axis was built for. A group that drew its cursor with
    the mark would be readable here and wrong.

    ONE SEAT, read by the screen AND by the acceptance check, exactly as
    `checkable_block` is: a block that "fits" in the oracle and wraps on the
    screen is a check measuring its own arithmetic.

    Reflow, never truncate — the same three-column set stacks one control
    state per row when the row does not fit, and the OPTIONS are never
    dropped, because a selection set missing an option is a different set."""
    def lab(name):
        return f"[{MUT}]{name:<11}[/]"

    ctls = [c for c, _ in LG.checked_pairs("radio")]
    tag = (f"[{DIM}]set={RADIO_OPTS[RADIO_SEL]} "
           f"cursor={RADIO_OPTS[RADIO_FOCUS]}[/]")
    rows = [lab("radio") + f"[{DIM}]{'·'.join(RADIO_OPTS)}  [/]" + tag] + [
        lab("") + k.radio_group(RADIO_OPTS, RADIO_SEL, c, RADIO_FOCUS)
        + f"   [{DIM}]{LG.control_of(c)}[/]" for c in ctls]
    if max(plain_len(r) for r in rows) <= w:
        return rows
    # stacked: the head drops the option list (every item row prints its own
    # option, so the list was the redundant half) and the set goes down the
    # page one item per row
    return [lab("radio") + tag] + [
        lab(LG.control_of(c) if i == 0 else "") + item
        for c in ctls
        for i, item in enumerate(
            k.radio_items(RADIO_OPTS, RADIO_SEL, c, RADIO_FOCUS))]


BTN_LABELS = ("ok", "Refresh")             # a short word and a long one


def button_block(k, w: int) -> list[str]:
    """THE BUTTON as gallery rows, and what it exists to show is that the
    LABEL IS CONTENT AND THE WALLS ARE THE LANGUAGE.

    Two labels per row, one short and one long. The pair is the point: the
    field grows with the word while the walls stay exactly what they were, so
    the eye can see that the language is drawing the ground and the caller is
    supplying the text. A row per control state, because a button's states are
    the only thing it has — there is no value to show, which is the whole
    reason this component is in the contract.

    THE STATES ARE THE DERIVATION'S, not a list written here: four of them,
    and if the registry ever gave a button a fifth this block would grow a row
    without being touched.

    ONE SEAT, read by the screen AND by the acceptance check, exactly as
    `checkable_block` and `radio_block` are. Reflow, never truncate: the pair
    goes one per row when the pair does not fit."""
    def lab(name):
        return f"[{MUT}]{name:<11}[/]"

    sts = LG.COMPONENT_STATES["button"]
    head = f"[{DIM}]{'·'.join(BTN_LABELS)}  label INSIDE[/]"
    rows = [lab("button") + head] \
        + [lab("") + k.button(BTN_LABELS[0], 0, st) + "  "
           + k.button(BTN_LABELS[1], 0, st) + f"   [{DIM}]{st}[/]"
           for st in sts]
    if max(plain_len(r) for r in rows) <= w:
        return rows
    return [lab("button") + f"[{DIM}]label INSIDE[/]"] + [
        lab(st if i == 0 else "") + k.button(l_, 0, st)
        for st in sts for i, l_ in enumerate(BTN_LABELS)]


TF_VALUE, TF_CARET = "task", 2         # the caller's word, and where the pen is
TF_PLACE = "title"                     # what the field says when it has none
TF_LONG = "a long title that windows"  # longer than any field drawn here


GAL_FPS = 8                            # the gallery's own repaint rate, and
#                                        the clock the caret's blink is
#                                        phased against — ONE seat, so a
#                                        faster gallery cannot desynchronise
#                                        the loop from the surface drawing it


def textfield_block(k, w: int, tick: int | None = None) -> list[str]:
    """THE TEXT FIELD as gallery rows, and what it exists to show is the
    CARET — the registry's first new part since the contract was written.

    A row per control state, derived; then the two rows that are this
    component's own questions and nobody else's. The PLACEHOLDER row shows
    what the field says when the value is empty, which must read differently
    from the same word typed in. The WINDOW row hands it a value longer than
    the field: the view moves and the caret stays inside, because a control
    that shortened the words in it would be lying about what it holds.

    REFLOW BY NARROWING THE WINDOW, which is a move only this component can
    make honestly: the field is a VIEW, so a smaller one shows less of the
    value without losing any of it. Every other block reflows by stacking,
    because a shorter button would be a shorter word.

    `tick` IS THE BLINK, AND IT IS GALLERY-ONLY BECAUSE THE FIELD IS. Pass 53
    read this app for a live text seat and found none — nothing in the engine
    is TYPED — and refused to invent one. That ruling stands, so the
    contract's first AMBIENT motion runs where its component already lives:
    the caret's column alternates between the language's mark and the rune
    its paper is made of, on the language's own period. Called without a
    tick (which is how every acceptance check calls it) the caret is simply
    ON, so the blink cannot move a single law that measured this block
    before it existed."""
    def lab(name):
        return f"[{MUT}]{name:<11}[/]"

    sts = LG.COMPONENT_STATES["textfield"]

    def lit(fw: int) -> bool:
        """WHICH FRAME OF THE LOOP IS DUE, from the engine's own period
        rather than from a number typed here — a blink whose rate was a
        constant at this call site would be the gallery's motion and not the
        language's."""
        if tick is None:
            return True
        m = k.motion_frames("textfield", "blink", value=TF_VALUE,
                            caret=TF_CARET, w=fw)
        return int(tick * (1000 / GAL_FPS) / m.step_ms) % len(m.frames) == 0

    def build(fw: int, cap: bool) -> list[str]:
        def tail(t):
            return f"   [{DIM}]{t}[/]" if cap else ""
        on = lit(fw)
        rows = [lab("textfield")
                + f"[{DIM}]{TF_VALUE}·caret {TF_CARET}[/]"]
        rows += [lab("") + k.textfield(TF_VALUE, TF_CARET, fw, st,
                                       caret_on=on) + tail(st)
                 for st in sts]
        rows.append(lab("")
                    + k.textfield("", None, fw, LG.DEFAULT,
                                  placeholder=TF_PLACE) + tail("placeholder"))
        rows.append(lab("")
                    + k.textfield(TF_LONG, len(TF_LONG), fw, LG.EDITED,
                                  caret_on=on)
                    + tail("window"))
        return rows

    for fw, cap in ((10, True), (10, False), (6, False)):
        rows = build(fw, cap)
        if max(plain_len(r) for r in rows) <= w:
            return rows
    return build(4, False)


SB_TOTAL = 40                          # the content, in rows
SB_SIZE = 8                            # what the container shows — small thumb
SB_BIG = 24                            # a window that shows most of the content
SB_W = 16                              # the shaft, in cells


def scrollbar_block(k, w: int) -> list[str]:
    """THE SCROLL BAR as gallery rows, and what it exists to show is the two
    numbers: the thumb's PLACE and the thumb's LENGTH, moving independently.

    Three rows walk the same window from top to bottom so the eye can check
    the ENDS — a scroll bar that cannot touch its first and last cell is
    lying about where you are, and it is the classic off-by-one in this
    component. A fourth row keeps the position and QUADRUPLES the view, so
    the only thing that changes is the thumb's length: that is the second
    number, and no other component in this contract has one.

    THE STATE ROWS ARE DERIVED and there are not many, which is the ruling
    made visible: this component has no grip, so the registry gives it
    DEFAULT and DISABLED and the block draws exactly that. If the contract
    ever gave a scroll bar an actuator, this block would grow rows without
    being touched — and if it hand-listed them, it would keep drawing two
    while the registry said four.

    Reflow by NARROWING THE SHAFT, the text field's move rather than the
    button's: a shorter track still shows a position and an extent, because
    both are fractions. Nothing is lost, only resolution."""
    def lab(name):
        return f"[{MUT}]{name:<11}[/]"

    last = SB_TOTAL - SB_SIZE
    others = [s for s in LG.COMPONENT_STATES["scrollbar"] if s != LG.DEFAULT]

    def build(cw: int, cap: bool) -> list[str]:
        def tail(t):
            return f"   [{DIM}]{t}[/]" if cap else ""
        rows = [lab("scrollbar")
                + f"[{DIM}]{SB_TOTAL} rows · {SB_SIZE} shown[/]"]
        rows += [lab("") + k.scrollbar(s, SB_SIZE, SB_TOTAL, cw) + tail(t)
                 for s, t in ((0, "top"), (last // 2, "middle"),
                              (last, "bottom"))]
        rows.append(lab("") + k.scrollbar(0, SB_BIG, SB_TOTAL, cw)
                    + tail(f"{SB_BIG} shown"))
        rows += [lab("") + k.scrollbar(last // 2, SB_SIZE, SB_TOTAL, cw, st)
                 + tail(st) for st in others]
        return rows

    for cw, cap in ((SB_W, True), (SB_W, False), (10, False)):
        rows = build(cw, cap)
        if max(plain_len(r) for r in rows) <= w:
            return rows
    return build(8, False)


STEP_OPTS = ("lo", "mid", "high")      # DIFFERENT WIDTHS on purpose — see below


def stepper_block(k, w: int) -> list[str]:
    """THE STEPPER as gallery rows, and what it exists to show is WRAP VS
    CLAMP — the first component whose question is what happens at the END of
    a range rather than what a range is.

    SIX ROWS IN A GRID THE BLOCK DOES NOT CHOOSE: floor, middle and ceiling
    of the same set, once clamped and once wrapping. The reading is the
    corners — a clamped stepper at its floor must SHOW its floor (the step
    back is not drawn at all; it is ground) and a wrapping one must not, and
    those two rows sit one above the other so the eye can do the comparison
    the laws do.

    THE OPTIONS HAVE DIFFERENT WIDTHS ON PURPOSE. `lo` is two cells and
    `high` is four, so a stepper that did not reserve the widest form would
    visibly breathe as it spun — Bodmer T2, and the one defect this component
    can have that no other in the contract can. Every row here is the same
    number of cells wide and that is the point of the block.

    THE STATE ROWS ARE THE DERIVATION'S: five, because a stepper has a grip
    AND an interior, which is the combination that finally makes EDITED mean
    what it says — the arrows are ranging through the value, and here that is
    the whole component.

    ONE SEAT, read by the screen AND by the acceptance check, exactly as
    every block since `checkable_block`. Reflow by stacking, the button's
    move: a stepper cannot narrow, because its width is the widest word in
    the caller's set and shortening that would be a different set."""
    def lab(name):
        return f"[{MUT}]{name:<11}[/]"

    last = len(STEP_OPTS) - 1
    ends = ((0, "floor"), (last // 2, "middle"), (last, "ceiling"))
    sts = LG.COMPONENT_STATES["stepper"]

    def build(cap: bool) -> list[str]:
        def tail(t):
            return f"   [{DIM}]{t}[/]" if cap else ""
        rows = [lab("stepper")
                + f"[{DIM}]{'·'.join(STEP_OPTS)}  one of the set[/]"]
        rows += [lab("") + k.stepper(STEP_OPTS, i, 0, LG.DEFAULT, wrap)
                 + tail(f"{t} · {'wrap' if wrap else 'clamp'}")
                 for wrap in (False, True) for i, t in ends]
        rows += [lab("") + k.stepper(STEP_OPTS, 1, 0, st) + tail(st)
                 for st in sts if st != LG.DEFAULT]
        return rows

    for cap in (True, False):
        rows = build(cap)
        if max(plain_len(r) for r in rows) <= w:
            return rows
    return build(False)


class GalleryScreen(ModalScreen):
    """The COMPONENT GALLERY (tui-design/COMPONENTS.md): every component of
    the active language on one surface — the language's style guide. `t`
    still cycles languages here, so this is where a language is judged.

    A ModalScreen shadows the App's bindings, so `t` has to be re-bound HERE —
    it was dead for as long as the docstring and the hint row claimed it worked.
    `q` closes rather than quitting: on a pushed surface the thing in front of
    you is the modal, and a `q` that does nothing is what sent the user hunting
    for ctrl+q."""
    # one binding for all three close keys, with a key_display that names them
    # ALL: Textual's Footer prints only the first key of a multi-key binding,
    # so `escape,q,g` would have advertised esc and hidden the other two.
    BINDINGS = [
        Binding("escape,q,g", "dismiss", "Close", key_display="esc/q/g"),
        Binding("t", "app.cycle_theme", "Language"),
    ]

    def compose(self) -> ComposeResult:
        # the guide outgrew a 30-row screen (plot + 2-row card): the box
        # SCROLLS instead of clipping its bottom sections off the fold
        with VerticalScroll(id="gallery-box"):
            yield Static("", id="gallery-body")
        # its OWN footer: a modal floats over the aperture's, and the aperture's
        # advertises the app keys this screen shadows — visible keys that do
        # nothing here. The legend must belong to the surface in front.
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#gallery-box").styles.max_height = "90%"
        self._t = 0                        # this surface's OWN clock, so the
        #                                    caret's loop is phased against
        #                                    the rate that actually repaints
        #                                    it (GAL_FPS) and not against a
        #                                    ticker running at another one
        self.rerender()
        # the spinner row must MOVE — frames ride the app ticker
        self.set_interval(1 / GAL_FPS, self.rerender)

    def rerender(self) -> None:
        k = KIT
        tick = self.app.ticker.n
        self._t = getattr(self, "_t", 0) + 1
        w = 52

        def lab(name):
            return f"[{MUT}]{name:<11}[/]"

        # brand first: the wordmark drawn through THIS language's pixel base,
        # and the mascot beside the label (COMPONENTS.md identity axis)
        rows = list(k.wordmark("GAL"))
        rows.append(f"[{MUT}]{TH.THEMES[THEME]['label']}[/]")
        rule = k.rule_line(w)
        if rule and rule not in rows:      # sects that already rule, don't twice
            rows.append(rule)
        rows += k.mascot()
        rows += [
            *checkable_block(k, w),
            *radio_block(k, w),
            *button_block(k, w),
            # THE TEXT FIELD IS GALLERY-ONLY, AND THAT IS SAID RATHER THAN
            # FAKED. The button found a real press target on the config
            # screen (`r`, the engine's own refresh); this component was read
            # for one and there is none. Nothing in the engine is TYPED: a
            # signal's label and help are written by `default_signals()` and
            # rebuilt at every start, so a rename would edit a string no
            # restart keeps and no behaviour reads — a demo wearing a seat's
            # clothes. The gallery draws all five states; the live surface
            # gets a text field the day the app has text to take.
            *textfield_block(k, w, self._t),
            # THE SCROLL BAR IS GALLERY-ONLY TOO, and for a different reason
            # than the text field's — this surface HAS a live seat and it is
            # TEXTUAL'S. `#gallery-box` is a `VerticalScroll` that draws and
            # drags its own scrollbar; replacing it means overriding a
            # framework widget, and the only channel a language could take
            # from it in TCSS is colour, which is the one channel this
            # contract forbids a state to ride alone. So ours documents that
            # chrome instead of fighting it, and says so here.
            *scrollbar_block(k, w),
            # THE STEPPER IS NOT GALLERY-ONLY, and it is the last component
            # of the contract and the third with a live seat. The config
            # screen's worker group is ONE CHOICE with two mechanisms: wide,
            # it is a radio set with every option named; narrow, it is this,
            # one option with the two ways off it. The narrow form used to
            # renounce the control entirely and print the group as a word —
            # that fallback is what a stepper is FOR, and the gallery draws
            # what the live seat cannot: a wrapping one, beside the clamped
            # one the app actually has.
            *stepper_block(k, w),
            # THE COMPONENT CONTRACT (COMPONENTS.md / language.py): the state
            # axis, ONE STATE PER ROW so the knob column lines up and the
            # states can be compared by eye. Side by side was tried first and
            # WRAPPED at this box's 52 columns, which turned three rows into
            # six and put the caption under the wrong control.
            *[lab("slider" if i == 0 else "")
              + k.slider(8, 0, 10, 12, st) + f"   [{DIM}]{st}[/]"
              for i, st in enumerate(LG.COMPONENT_STATES["slider"])],
            *[lab("bar" if i == 0 else "")
              + k.readbar(8, 0, 10, 12, st) + f"   [{DIM}]{st}[/]"
              + (f"  [{DIM}]— no knob[/]" if i == 0 else "")
              for i, st in enumerate(LG.COMPONENT_STATES["bar"])],
            lab("spinner") + k.spinner(tick) + f"  [{DIM}]live[/]"
            + f"   [{MUT}]cursor[/] [{ACCENT}]{k.CUR}[/]",
            lab("tabs") + k.tabs(["board", "lanes", "agenda"], "lanes"),
            "",
            lab("meter") + "",
            k.meter(3, 8, [4, 0, 2, 2], w - 4),
            # NOT the `bar` component: this is the agenda/gantt quantity SPAN,
            # which shares a word with the registry and nothing else
            lab("span") + k.bar(12, None, None),
            lab("calendar") + " ".join(
                k.cal_cell(s) for s in ("none", "one", "multi", "over"))
            + f"  [{DIM}]none·one·multi·over[/]",
            lab("icons") + " ".join(
                x for x in (k.icon(i) for i in
                            ("deadline", "overdue", "wip", "blocked")) if x)
            + (f"  [{DIM}]dl·ov·wf·bl[/]" if k.ICONS else f"[{DIM}]renounced[/]"),
            lab("spark") + k.spark([1, 3, 2, 5, 4, 6, 2, 7, 3, 5, 1, 4], 12),
            lab("gauge") + k.gauge(7, 0, 10, 10, thr=8)
            + f"  [{DIM}]needle · thr tick[/]",
            lab("plot") + f"[{DIM}]meter family · 4 rows[/]",
            *k.plot([2, 5, 3, 7, 4, 8, 6, 9], 24, 4),
            "",
            lab("card") + "",
            *k.card_rows("An urgent task", "2d!", ALERT_HUE, w - 4, 0, True,
                         {"proj": "Web", "phase": "Doing", "phase_idx": 1,
                          "n_phases": 4, "days": 2, "prio": "high",
                          "blocked": False, "done": False}),
            lab("empty") + f"[{DIM}]{k.VOICE['empty']}[/]",
            lab("head") + "",
            k.head("BACKLOG", 5, w - 4, 0),
            "",
            f"[{DIM}]{hint_row(self.BINDINGS)}[/]",
        ]
        self.query_one("#gallery-body", Static).update("\n".join(rows))


class HelpScreen(ModalScreen):
    """The `?` tier of discoverability: the full keymap, GROUPED.

    It used to skip every `show=False` binding, which meant the keys that only
    lived here — the motion keys, ctrl+q, the palette — were indicated on NO
    surface at all. The footer carries the actions; this carries everything,
    which is the only reason the footer is allowed to carry less."""
    BINDINGS = [Binding("escape,question_mark,q", "dismiss", "Close",
                        key_display="esc/?/q")]

    # keys Textual itself binds on the App, which no BINDINGS list here owns.
    # They work, so they are printed; unprinted working keys are the defect.
    SYSTEM = [("ctrl+q", "Quit anywhere"), ("ctrl+p", "Palette")]

    # TWO COLUMNS because one column of the FULL map is 32 rows and the modal
    # runs on a 30-row screen: the hidden keys were the ones scrolled off, which
    # is the defect again. Paired sections, widest first in each column.
    COLUMNS = (("Views", "actions"), ("motion", "system"))

    def compose(self) -> ComposeResult:
        groups: dict[str, list[str]] = {}

        def line(key: str, desc: str, kw: int, dw: int) -> str:
            return f"[{INK}]{key:<{kw}}[/] [{MUT}]{desc[:dw]:<{dw}}[/]"

        for b in TaskboardWidget.BINDINGS:
            if not isinstance(b, Binding):
                continue
            gname = b.group.description if b.group else (
                "actions" if b.show else "motion")
            groups.setdefault(gname, []).append((key_of(b), b.description))
        groups["system"] = list(self.SYSTEM)

        cols, widths = [], []
        for sections in self.COLUMNS:
            pairs = [p for s in sections for p in groups[s]]
            kw = max(len(k) for k, _ in pairs)
            dw = max(len(d) for _, d in pairs)   # no description is truncated:
            widths.append(kw + dw + 1)           # a clipped word is a new lie
            out = []
            for s in sections:
                out.append(f"[{MUT}]{s.upper()}[/]")
                out += [line(k, d, kw, dw) for k, d in groups[s]]
                out.append("")
            cols.append(out)
        h = max(len(c) for c in cols)
        left = cols[0] + [" " * widths[0]] * (h - len(cols[0]))
        right = cols[1] + [""] * (h - len(cols[1]))
        pad = " " * widths[0]
        rows = [f"[{ACCENT}]KEYS[/]", ""]
        for a, b in zip(left, right):
            # section titles carry markup but no padding, so pad on the STRIPPED
            # length or the right column walks left under every heading
            plain = a.replace(f"[{MUT}]", "").replace(f"[{INK}]", "") \
                     .replace("[/]", "")
            rows.append(f"  {a}{pad[len(plain):]}   {b}")
        rows.append(f"  [{DIM}]{hint_row(self.BINDINGS)}[/]")
        yield Static("\n".join(rows), id="help-box")
        yield Footer()                     # same reason as GalleryScreen


class ConfigScreen(Screen):
    """The deep half made editable — the user changes what the engine tracks.

    This is the point of the widget thesis: the aperture is one line of output
    from a system the user can reconfigure and extend.
    """
    BINDINGS = [
        # `q` closes the surface in front of you on every pushed screen. Before
        # this it fell through to the App and KILLED the app from here.
        Binding("escape,q", "app.pop_screen", "Back", key_display="esc/q"),
        Binding("space,enter", "toggle", "Toggle", key_display="space"),
        Binding("up,k", "move(-1)", "Up", show=False),
        Binding("down,j", "move(1)", "Down", show=False),
        # the raw key names read "bracketleft" on the footer — not a key anyone
        # can type. `format_key` has no entry for them, so they carry their own.
        Binding("bracketleft", "bump(-1)", "Threshold -", key_display="["),
        Binding("bracketright", "bump(1)", "Threshold +", key_display="]"),
        # THE LIVE PRESS TARGET. `r` is the app's own refresh key and it was
        # already reaching this screen through the App; binding it HERE is
        # what gives the press a place to be SEEN, and the action below is
        # the same one the aperture runs. No key was invented for a demo.
        Binding("r", "press_refresh", "Refresh"),
    ]

    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.idx = 0
        # ONE MOTION SLOT FOR THE WHOLE SCREEN — `(kind, row, frames, i,
        # step_s)` — and it is one because MOTION.md's hardest rule is that
        # only ONE thing may move at a time: two concurrent animations
        # compete and the eye resolves neither. Two slots (`_flip` and
        # `_pressed`) is how a surface grows a second moving element without
        # anyone deciding to.
        self._motion = None
        # AND A GENERATION, because a key can be pressed again while its own
        # motion is still playing. The timer chain of the motion that was
        # interrupted is still armed, and without this it would advance the
        # NEW motion as well — two chains driving one index, so a transition
        # plays at double speed and lands early. The stale chain checks its
        # generation and returns. (The same race was latent when only the
        # switch animated; driving four motions from three keys is what made
        # it reachable.)
        self._gen = 0

    def compose(self) -> ComposeResult:
        yield Static("", id="cfg-title")
        yield VerticalScroll(Static("", id="cfg-body"), id="cfg-scroll")
        yield Footer()

    def on_mount(self) -> None:
        self.redraw()

    def redraw(self) -> None:
        """The most component-dense surface in the app, so every control is
        the LANGUAGE's (COMPONENTS.md): its switch, its slider, its cursor.
        This screen rendering identically across languages is what made the
        axis still read as a recolour."""
        w = max(40, (self.size.width or 60) - 6)
        # the config screen is full-height, so it can AFFORD the language's
        # display typography (drawn titles: naught dots, bbs block letters,
        # instrument braille caps — the renouncing languages just print)
        self.query_one("#cfg-title", Static).update(
            "\n".join(KIT.sect("SIGNALS", "what the widget watches", w,
                               self.size.height or 24)))
        rows = self._rows(self._group_radio if self._wide()
                          else self._group_stepper)
        # REFLOW, NEVER TRUNCATE, and measured on the assembled block the way
        # `radio_block` and `checkable_block` are. A selection set costs this
        # row 13 cells over the printed word it replaces (ledger, the widest:
        # 66 -> 79), which is more than the `widget` size class has. Rather
        # than wrap a row — a wrapped row puts the threshold slider under the
        # wrong signal — the narrow screen CHANGES MECHANISM. ONE decision for
        # the whole screen, not one per row, so the column cannot jitter.
        #
        # AND THE FALLBACK IS NO LONGER A RENUNCIATION. It used to be the
        # group printed as a word — the control given up, honestly, because
        # nothing here could show a set in one option's worth of cells. A
        # stepper is exactly that thing, so the narrow screen now keeps a
        # control: same set, same index, same key, one option on screen.
        rows.append("")
        rows.append(self._action_row())
        rows.append("")
        rows.append(f" [{DIM}]{LG.mark(hint_row(self.BINDINGS))}[/]")
        self.query_one("#cfg-body", Static).update("\n".join(rows))

    def _wide(self) -> bool:
        """WHICH MECHANISM THIS SCREEN IS DRAWING, asked in one place because
        two things now need the answer: the redraw, and the PICK's motion — a
        set with every option on screen moves its MARK between siblings, and
        a set showing one option changes its WORD. Same choice, two
        mechanisms, and therefore two motions."""
        rows = self._rows(self._group_radio)
        return max(plain_len(r) for r in rows) <= (self.size.width or 80)

    def _action_row(self) -> str:
        """THE LIVE BUTTON, and it is a real one: `r` recomputes every enabled
        signal right now, which is the same action the aperture's `r` runs.

        ITS DISABLED STATE IS THE ENGINE'S, not a demo toggle. With every
        signal switched off there is nothing to recompute, so the button is
        dead — and the action refuses in the same breath, so the render and
        the behaviour cannot disagree.

        WHAT THIS SEAT HONESTLY DOES NOT HAVE IS **FOCUSED**, and it is said
        here rather than faked: this screen's cursor ring is the signal list,
        and putting a button in it would mean inventing a row for the cursor
        to land on. Default, ACTIVE (the press flash) and DISABLED are live;
        the gallery is where FOCUSED is drawn — the same split the radio's
        uncommitted cursor was given by the pass before this one."""
        live = any(s.enabled for s in self.engine.signals)
        note = ("recompute every signal now" if live
                else "nothing is enabled — nothing to recompute")
        # THE PRESS IS A FRAME LIST NOW, not a boolean. `_pressed` was a
        # second state living beside the real one: it could only ever say
        # "flashing or not", so the flash had no intermediate frames and no
        # way to grow any. The motion slot holds the language's own render
        # for this instant, and when it empties the row goes back to being
        # derived — a pressed state that outlives its frames is not
        # reachable from here.
        btn = (self._motion[2][self._motion[3]]
               if self._motion and self._motion[0] == "press"
               else KIT.button("Refresh", 0,
                               LG.DEFAULT if live else LG.DISABLED))
        return f"   {btn}  [{DIM}]{note}[/]"

    def _group_stepper(self, s, sel: bool) -> str:
        """THE SAME CHOICE, THE OTHER MECHANISM — and this seat is what the
        stepper is for.

        What stood here before was `_group_word`: the group printed as text,
        no control at all, because below the board size class the radio's
        three columns do not fit and a set drawn with two of its options
        missing is a different set. That renunciation was honest and it was
        also the exact shape of a stepper — ONE option shown, the arrows
        spinning through the rest. So the narrow screen no longer gives up
        the control; it changes mechanism, and the model underneath does not
        move: same `WORKER_GROUPS`, same single index, same `action_pick`.

        IT CLAMPS, and not by preference — `action_pick` clamps, and has said
        why since the pass that wrote it: an N-of-M control's ends are where
        the set ends. The render is handed the same `wrap=False`, so the seat
        this screen draws and the keys it answers to cannot disagree about
        whether there is a step. A wrapping stepper is drawn in the GALLERY,
        which is where this app draws the states its surfaces do not have."""
        return KIT.stepper(WORKER_GROUPS, WORKER_GROUPS.index(s.group), 0,
                           LG.DISABLED if not s.enabled
                           else LG.EDITED if sel else LG.DEFAULT)

    def _group_radio(self, s, sel: bool) -> str:
        """THE LIVE SELECTION SEAT. Which worker loop recomputes this signal
        is a choice of exactly one of `WORKER_GROUPS` — the first thing on
        this screen whose state is a fact about a SET, so the first thing
        drawn with `radio_group`. The bit is never handed in: the group is
        given one INDEX and derives every item's state from it, which is why
        no sequence of key presses can leave this row in two groups or none.

        FOCUS FOLLOWS THE SELECTION HERE, and that is the standard radio
        behaviour rather than a shortcut: the arrows commit as they cross
        (WAI-ARIA's auto-select; LVGL's roving focus does the same). The
        contract can hold focus APART from the checked item — `group_states`
        takes them as two arguments — and the gallery is where that case is
        drawn, because this screen would have to invent an uncommitted cursor
        to show it."""
        gi = WORKER_GROUPS.index(s.group)
        return KIT.radio_group(WORKER_GROUPS, gi,
                               LG.DISABLED if not s.enabled
                               else LG.FOCUSED if sel else LG.DEFAULT,
                               focus=gi)

    def _rows(self, group_cell) -> list[str]:
        rows = []
        for i, s in enumerate(self.engine.signals):
            sel = i == self.idx
            cur = f"[{ACCENT}]{KIT.CUR}[/]" if sel else " "
            # THE LIVE CHECKED SEAT. `space` toggles THIS row, so the switch
            # carries the checked bit and the row's control state at once —
            # `checked+focused` when the cursor is on an enabled signal. The
            # switch is never DISABLED here and that is not an omission: a
            # signal you can still switch on is operable by definition. It is
            # the THRESHOLD that goes unreachable, and that slider says so.
            #
            # AND THE CHECKBOX DOES NOT GO HERE. This row has exactly one
            # boolean and the switch already owns it honestly; two controls
            # for one bit would be a demo, not a seat. The distinction is
            # real — a switch is a setting that acts at once, a checkbox is a
            # SELECTION within a set — and the set this screen has is the
            # WORKER GROUP, which the radio below now owns. The checkbox
            # itself still has no live seat here and still says so.
            sw = KIT.switch(s.enabled, 3, LG.FOCUSED if sel else LG.DEFAULT)
            if self._motion and self._motion[:2] == ("flip", i):
                sw = self._motion[2][self._motion[3]]
            # THE STATE AXIS, wired to what is actually true of this row
            # (language.py's contract). `[`/`]` mutate the SELECTED row's
            # value, so a selected threshold is EDITED, not merely focused —
            # that is LVGL's definition of the state and it is the normal
            # case on a keyboard surface. A signal that is switched off owns
            # a value nothing can reach: DISABLED.
            st = (LG.DISABLED if not s.enabled
                  else LG.EDITED if sel else LG.DEFAULT)
            thr = ("" if s.threshold is None
                   else KIT.slider(s.threshold, 0, max(10, s.threshold * 2), 8,
                                   st))
            val = "—" if s.last is None else s.last.value
            ic = KIT.icon(s.id)
            name = (f"{ic} " if ic else "") \
                + f"[{INK if sel else MUT}]{s.label[:20]:<20}[/]"
            grp = (self._motion[2][self._motion[3]]
                   if self._motion and self._motion[:2] == ("pick", i)
                   else group_cell(s, sel))
            rows.append(f" {cur} {sw} {name} {grp} "
                        f"[{DIM}]{s.cadence:>4.0f}s[/] [{MUT}]{val:>3}[/] {thr}")
            if sel:
                rows.append(f"     [{DIM}]{s.help}[/]")
                if s.last_error:
                    rows.append(f"     [{ALERT_HUE}]{s.last_error}[/]")
        return rows

    def action_move(self, d: int) -> None:
        self.idx = (self.idx + d) % len(self.engine.signals)
        self.redraw()

    def action_toggle(self) -> None:
        """The flip is the language's: frames + tempo. A state change, so it
        must DEGRADE to the final frame when animations are off (MOTION.md) —
        the frames are skipped, never the state."""
        s = self.engine.signals[self.idx]
        s.enabled = not s.enabled
        self._play("flip", self.idx,
                   KIT.motion_frames("switch", "flip", on=s.enabled, w=3))

    def _play(self, kind: str, row: int, m) -> None:
        """THE ONE PLAYER for every motion this screen has, and its whole job
        is to advance an INDEX — frame motion, MOTION.md's cheap class, never
        a recompute per tick. The engine already decided how many frames
        there are and how long a step lasts; nothing here divides anything.

        A motion with one frame to draw is a CUT and is played as one, which
        is how a language renounces (swiss) without the caller knowing it
        has. Animations switched off take the same road: the frames are
        skipped, never the state, because the last frame IS the state."""
        self._gen += 1
        if m.steps <= 1 or self.app.animation_level == "none":
            self._motion = None
            self.redraw()
            return
        self._motion = (kind, row, m.plays, 0, m.step_s)
        self._advance(self._gen)

    def _advance(self, gen: int) -> None:
        if self._motion is None or gen != self._gen:
            return                         # a superseded motion's stale timer
        kind, row, frames, i, step = self._motion
        self.redraw()
        if i >= len(frames) - 1:
            self._motion = None
            self.redraw()                  # land on the DERIVED resting row
            return
        self._motion = (kind, row, frames, i + 1, step)
        self.set_timer(step, lambda: self._advance(gen))

    def action_pick(self, d: int) -> None:
        """Cross the selected row's worker-group set. CLAMPS at both ends
        rather than wrapping, the same decision the threshold slider makes
        one method down: a set the arrows can spin through is a stepper, and
        an N-of-M control's ends are where the set ends.

        AND THE MOTION IS THE MECHANISM'S, not the key's. Wide, this row is a
        radio and the mark TRAVELS between wells; narrow, it is a stepper and
        the WORD spins. One choice, two mechanisms, two motions — and a press
        that changes nothing (the clamped end) plays nothing, because a
        motion with no distance is not a motion."""
        s = self.engine.signals[self.idx]
        i = WORKER_GROUPS.index(s.group)
        j = max(0, min(len(WORKER_GROUPS) - 1, i + d))
        s.group = WORKER_GROUPS[j]
        if j == i:
            self.redraw()
            return
        self._play("pick", self.idx, self._pick_motion(s, i, j))

    def _pick_motion(self, s, old: int, new: int):
        """The pick's frames, composed at the SAME state the resting render
        is composed at — so the motion's last frame and the redraw that
        follows it are the same string, and a motion cannot land somewhere
        the screen would not have drawn."""
        if self._wide():
            return KIT.motion_frames(
                "radio", "travel", options=WORKER_GROUPS, old=old, new=new,
                state=LG.DISABLED if not s.enabled else LG.FOCUSED)
        return KIT.motion_frames(
            "stepper", "spin", options=WORKER_GROUPS, old=old, new=new,
            state=LG.DISABLED if not s.enabled else LG.EDITED)

    def action_press_refresh(self) -> None:
        """The press: run the engine, flash, release. A DEAD button does
        nothing at all — the same condition the render reads, so a disabled
        control that still fires is not reachable from here.

        THE FLASH HAS FRAMES NOW. It used to be a boolean held for one tempo
        — the render event this screen could afford before there was an
        engine to ask. What plays here is the language's own press: the
        extreme on the first drawn frame (the acknowledgement is never
        animated), the hold, and the release landing on the last."""
        if not any(s.enabled for s in self.engine.signals):
            return
        self.engine.run_all()
        self._play("press", -1,
                   KIT.motion_frames("button", "press", label="Refresh"))

    def action_bump(self, d: int) -> None:
        s = self.engine.signals[self.idx]
        if s.threshold is not None:
            s.threshold = max(0, s.threshold + d)
            self.redraw()


class Aperture(Screen):
    """The widget surface. Its CONTENT is decided by its own width."""

    def compose(self) -> ComposeResult:
        with Vertical(id="ap"):
            # hero+meter share a region whose LAYOUT belongs to the language:
            # stacked by default, side-by-side widgets in naught's grid
            with Vertical(id="top"):
                yield Hero(id="hero")
                yield Meter(id="meter")
            yield Static("", id="tabs")    # the view switcher, per-language
            with Vertical(id="tiles"):
                pass
            yield Static("", id="queue")   # kanban mounts here
            yield Static("", id="view")    # lanes / agenda / gantt
        yield Footer()

    def on_mount(self) -> None:
        # The App's own on_mount fires BEFORE the default screen's children
        # exist, so the wiring has to start here, where compose() has run.
        self.app.start_widget()


class TaskboardWidget(App):
    CSS_PATH = str(Path(__file__).resolve().parent / "widget.tcss")
    ENABLE_COMMAND_PALETTE = True
    AUTO_FOCUS = "#hero"

    BINDINGS = [
        # 1-4 are the one honest group: a numbered family whose label names all
        # four. Every letter key keeps its OWN word, because a group eats the
        # descriptions and `c ? V r t g q Widget` is what the user got lost in.
        Binding("1", "view('board')", "Board", group=G_VIEW),
        Binding("2", "view('lanes')", "Lanes", group=G_VIEW),
        Binding("3", "view('agenda')", "Agenda", group=G_VIEW),
        Binding("4", "view('gantt')", "Gantt", group=G_VIEW),
        Binding("c", "configure", "Signals"),
        Binding("question_mark", "help", "Keys", key_display="?"),
        # was "V": the only key in the app that needed shift, and the footer
        # showed it as a bare capital. `v` is unclaimed, so no key needs shift.
        Binding("v", "cycle_size", "Size",
                tooltip="Force a size class to preview glance / widget / board"),
        Binding("r", "refresh_now", "Refresh"),
        # DERIVED from themes.ORDER (PENDING #24): the hand-written list named
        # seven languages for four passes after the tenth was added, which is
        # the same drift the legend law forbids one surface further out.
        Binding("t", "cycle_theme", "Language",
                tooltip="Cycle the visual language: " + " / ".join(TH.ORDER)),
        Binding("g", "gallery", "Gallery",
                tooltip="Every component of the active language on one screen"),
        Binding("q", "quit", "Quit"),
        Binding("left,h", "nav(-1,0)", "Left", show=False, priority=True),
        Binding("right,l", "nav(1,0)", "Right", show=False, priority=True),
        Binding("up,k", "nav(0,-1)", "Up", show=False, priority=True),
        Binding("down,j", "nav(0,1)", "Down", show=False, priority=True),
        Binding("tab", "focus_next", "Next", show=False),
        Binding("shift+tab", "focus_previous", "Prev", show=False),
    ]

    SIZE_CLASSES = ("glance", "widget", "board")

    def __init__(self, board_path=None, forced: str | None = None):
        super().__init__()
        self.board = Board.load(board_path or default_board_path())
        self.engine = Engine(self.board)
        self.size_class = "widget"
        self.forced = forced
        self._tiles: dict[str, Tile] = {}
        self.focused_task = None
        self.ticker = MO.Ticker()
        self.view = 'board'

    # actions that only mean anything on the aperture. On a pushed screen they
    # still FIRED — `1` switched a view nobody could see — and they still took
    # footer width, pushing the screen's own keys off the right edge at 118.
    # FALSE, not None: Textual drops a binding from `active_bindings` only on
    # `is False` (screen.py); None leaves it listed and merely disabled, which
    # would keep the dead key on the legend — the defect, one layer down.
    APERTURE_ONLY = frozenset({"view", "cycle_size", "refresh_now", "gallery",
                               "configure"})   # `c` on the config screen
                                               # pushed a SECOND config screen

    def check_action(self, action: str, parameters) -> bool | None:
        if action in self.APERTURE_ONLY and not isinstance(self.screen, Aperture):
            return False
        return True

    def get_default_screen(self) -> Screen:
        return Aperture()

    # -- discoverability tier 3: every action is a command ------------------
    def get_system_commands(self, screen):
        yield from super().get_system_commands(screen)
        yield SystemCommand("Configure signals",
                            "Enable, disable or retune what the widget watches",
                            self.action_configure)
        yield SystemCommand("Show keys", "The full keymap, grouped", self.action_help)
        yield SystemCommand("Refresh now", "Recompute every signal immediately",
                            self.action_refresh_now)
        for s in self.engine.signals:
            yield SystemCommand(
                f"Toggle: {s.label}", s.help,
                (lambda sig=s: self._toggle(sig)), discover=False)

    def _toggle(self, sig) -> None:
        sig.enabled = not sig.enabled
        self.notify(f"{sig.label}: {'on' if sig.enabled else 'off'}", timeout=1.5)
        self.redraw()

    def start_widget(self) -> None:
        """Called from Aperture.on_mount, once the screen's children exist."""
        hero = self.query_one("#hero", Hero)
        hero.loading = True                      # a real loading state
        self.apply_size_class()
        self.mount_tiles()
        kb = KanbanBoard(self.board, KIT, id='kb')
        self.query_one('#ap').mount(kb)
        kb.build()
        self.engine.run_all()
        hero.loading = False
        # apply the FULL language (stylesheet: surface + composition), not
        # just the colour globals — before this, the initial theme skipped
        # set_theme and launched on the base skeleton
        self.set_theme(THEME)
        # TWO CADENCES, SEPARATE GROUPS (ARCHITECTURE.md): the slow filesystem
        # signal can never cancel or stall the fast hero.
        # the animation cadence is FAST and cheap (index lookup + restyle);
        # the data cadences stay slow. One ticker for the whole app.
        self.set_interval(1.0 / MO.FPS, self.tick_fast)
        self.set_interval(5.0, self.tick_slow)

    def mount_tiles(self) -> None:
        box = self.query_one("#tiles", Vertical)
        for s in self.engine.signals:
            t = Tile(s, id=f"t-{s.id}", classes="tile")
            self._tiles[s.id] = t
            box.mount(t)

    @work(group="fast", exclusive=True)
    async def tick_fast(self) -> None:
        self.ticker.advance()
        self.engine.run_group("fast")
        self.redraw()

    @work(group="slow", exclusive=True)
    async def tick_slow(self) -> None:
        if self.engine.run_group("slow"):
            self.redraw()

    # -- size classes: the widget adapts to ITSELF, not to a view key -------
    def on_resize(self, event) -> None:
        self.apply_size_class()
        self.redraw()

    def class_for_width(self, w: int) -> str:
        if self.forced:
            return self.forced
        if w < 46:
            return "glance"
        if w < 80:
            return "widget"
        return "board"

    def apply_size_class(self) -> None:
        w = self.size.width or 80
        new = self.class_for_width(w)
        if new == self.size_class and self.screen.has_class(f"sz-{new}"):
            return
        self.size_class = new
        for c in self.SIZE_CLASSES:
            self.screen.set_class(c == new, f"sz-{c}")

    def action_cycle_size(self) -> None:
        i = self.SIZE_CLASSES.index(self.size_class)
        self.forced = self.SIZE_CLASSES[(i + 1) % len(self.SIZE_CLASSES)]
        self.apply_size_class()
        self.redraw()
        self.notify(f"size class: {self.forced}", timeout=1.5)

    def on_card_focused(self, msg: CardFocused) -> None:
        """The hero follows the cursor: the drawn numeral becomes THIS task's
        countdown. One signature element, two jobs, no second panel."""
        self.focused_task = msg.card.item
        self.redraw()

    def action_nav(self, dcol: int, drow: int) -> None:
        # The app's arrow bindings are priority=True (an ancestor
        # VerticalScroll eats arrows otherwise), and Textual resolves
        # priority bindings APP-FIRST — so any screen with its own cursor
        # must be DELEGATED to, or its arrows are dead. The config screen's
        # cursor was unnavigable for three passes; the drive-check caught it.
        scr = self.screen
        if drow and hasattr(scr, "action_move"):
            scr.action_move(drow)
            return
        # AND THE SAME DELEGATION SIDEWAYS, for the same reason. A radio set
        # is navigated with the arrows that cross it — that is what makes it
        # a set and not a stack of switches — and those arrows are bound here
        # with priority, so a screen that owns a selection group must be
        # handed them or its group is inert.
        if dcol and hasattr(scr, "action_pick"):
            scr.action_pick(dcol)
            return
        try:
            kb = self.query_one('#kb', KanbanBoard)
        except Exception:
            return
        cur = self.focused if isinstance(self.focused, TaskCard) else None
        nxt = kb.move(dcol, drow, cur)
        if nxt is not None:
            nxt.focus()

    def action_cycle_theme(self) -> None:
        i = TH.ORDER.index(THEME)
        nxt = TH.ORDER[(i + 1) % len(TH.ORDER)]
        self.set_theme(nxt)

    def set_theme(self, name: str) -> None:
        apply_theme(name)
        # palette rules + the kit's STRUCTURAL rules (pitch, head height)
        self.stylesheet.add_source(TH.tcss(name) + "\n" + KIT.tcss(),
                                   read_from=("theme", ""))
        self.stylesheet.reparse()
        self.stylesheet.update(self)
        kb = self.query("#kb")
        if kb:
            kb.first().tok = KIT
            kb.first().build()
        self.redraw()
        th = TH.THEMES[name]
        self.notify(f"{th['label']} — {th['note']}", timeout=3)

    def action_view(self, name: str) -> None:
        """Switching view is a STATE change, so its motion is level='basic' —
        it must survive TEXTUAL_ANIMATIONS=basic, and it must degrade to the
        final frame rather than being the only cue that the view changed."""
        self.view = name
        panel = self.query_one("#view", Static)
        board = self.query_one("#kb")
        show_board = name == "board"
        board.display = show_board and self.size_class == "board"
        panel.display = not show_board
        target = board if show_board else panel
        target.styles.opacity = 0.0
        target.styles.animate("opacity", 1.0, duration=KIT.tempo_s * 1.6,
                              easing=KIT.easing, level="basic")
        self.redraw()
        self.notify(f"view: {name}", timeout=1.2)

    def action_configure(self) -> None:
        self.push_screen(ConfigScreen(self.engine))

    def action_help(self) -> None:
        self.push_screen(HelpScreen())

    def action_gallery(self) -> None:
        if not isinstance(self.screen, GalleryScreen):
            self.push_screen(GalleryScreen())

    def action_refresh_now(self) -> None:
        self.engine.run_all()
        self.redraw()

    # -- render -------------------------------------------------------------
    def redraw(self) -> None:
        try:
            hero = self.query_one("#hero", Hero)
        except Exception:
            return
        w = max(10, (self.size.width or 40) - 4)
        # the 8-week load series feeds the hero's dead columns at board size
        series = self._load_series() if self.size_class == 'board' else None
        ft = self.focused_task
        if ft is not None and self.size_class == 'board':
            from taskboard.engine import Reading, Signal, sig_deadline
            d = kb_days(ft, datetime.now().date())
            if self.board.is_done(ft):
                val, cap, sev = '0', 'done', CALM
            elif d is None:
                val, cap, sev = '?', 'no due date', CALM
            elif d < 0:
                val, cap, sev = str(min(99, -d)), 'days overdue', ALERT
            elif d == 0:
                val, cap, sev = '0', 'due today', ALERT
            else:
                val, cap, sev = (str(min(99, d)), 'days left',
                                 WARN if d <= 3 else CALM)
            fake = Signal('focus', 'Focused task', '', 0, sig_deadline)
            hero.show(fake, Reading(val, cap, ft.title, sev), w, series)
            self._after_hero()
            return
        h = self.engine.hero
        if h is None:                              # a real empty state
            hero.update(f"[{MUT}]No signals enabled.[/]\n\n"
                        f"[{DIM}]Press  c  to turn one on.[/]")
        else:
            hero.show(h[0], h[1], w, series)

        self._after_hero()

    def _after_hero(self) -> None:
        w = max(10, (self.size.width or 40) - 4)
        b = self.board
        tasks = b.visible_tasks(False)
        done = sum(1 for t in tasks if b.is_done(t))
        from taskboard.views import phase_buckets
        counts = [len(x) for x in phase_buckets(b, tasks)]
        self.query_one("#meter", Meter).show(done, len(tasks), w, counts)

        # the board MOOD feeds identity elements with a job (naught's face):
        # alert = something overdue · busy = open work · clear = nothing due
        from taskboard.models import parse_iso
        today = datetime.now().date()
        over = any((d := parse_iso(t.due_date)) is not None and d < today
                   and not b.is_done(t) for t in tasks)
        KIT.mood = "alert" if over else ("busy" if done < len(tasks) else "clear")

        for sid, tile in self._tiles.items():
            tile.display = self.engine.by_id(sid).enabled
            tile.refresh_tile()

        try:
            self.query_one("#tabs", Static).update(
                KIT.tabs(["board", "lanes", "agenda", "gantt"], self.view))
        except Exception as exc:
            self.log.warning(f"tabs: {exc!r}")

        try:
            q = self.query_one("#queue", Static)
            if self.size_class == "widget":
                q.display = True
                q.update(self._calendar_markup(w) + chr(10) * 2
                         + self._queue_markup(w))
            else:
                q.display = False
        except Exception as exc:                      # never swallow silently:
            self.log.warning(f"queue panel: {exc!r}")  # this hid a NameError
        try:
            board = self.query_one("#kb")
            panel = self.query_one("#view", Static)
            on_board = self.view == "board"
            board.display = on_board and self.size_class == "board"
            panel.display = (not on_board) and self.size_class in ("widget", "board")
            if not on_board:
                fn = VW.VIEWS[self.view]
                h = max(4, (self.size.height or 30) - 16)
                panel.update(fn(self.board, KIT, w, h, self.ticker,
                                self.focused_task.id if self.focused_task else None))
        except Exception:
            pass

    def _load_series(self, weeks: int = 8) -> list[int]:
        """Open-task due count per week, 8 weeks out from Monday. The data the
        calendar already walks — recomputed here at board size (no calendar)."""
        from taskboard.models import parse_iso
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday())
        out = [0] * weeks
        for t in self.board.visible_tasks(False):
            if self.board.is_done(t):
                continue
            d = parse_iso(t.due_date)
            if d is None:
                continue
            wk = (d - start).days // 7
            if 0 <= wk < weeks:
                out[wk] += 1
        return out

    def _calendar_markup(self, w: int, weeks: int = 4) -> str:
        """A due-date dot calendar: 7 columns (days) x N rows (weeks), one mark
        per day, lit by how many tasks fall due. Uses data the engine already
        derives -- the cheapest density available (DENSITY.md)."""
        from taskboard.models import parse_iso
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday())
        counts = {}
        for t in self.board.visible_tasks(False):
            d = parse_iso(t.due_date)
            if d is None or self.board.is_done(t):
                continue
            counts[d] = counts.get(d, 0) + 1
        rows = [f"[{MUT}]{'M  T  W  T  F  S  S':<21}[/]  [{DIM}]due[/]"]
        for wk in range(weeks):
            cells = []
            for dy in range(7):
                d = start + timedelta(days=wk * 7 + dy)
                n = counts.get(d, 0)
                # the day-cell mark is the language's (kit.cal_cell): lattice
                # dots in naught, LCD segments in corgi, brightness in phosphor
                if n == 0:
                    cells.append(KIT.cal_cell("none"))
                elif d < today:
                    cells.append(KIT.cal_cell("over"))
                elif n > 1:
                    cells.append(KIT.cal_cell("multi"))
                else:
                    cells.append(KIT.cal_cell("one"))
            mark = "◀" if wk == 0 else " "
            rows.append(" ".join(cells) + f"  [{DIM}]{mark}[/]")
        # the 4-week LOAD as a sparkline in the language's quantity mechanism
        # (data-viz axis): due-count per day, already computed above
        series = [counts.get(start + timedelta(days=i), 0)
                  for i in range(weeks * 7)]
        rows.append(KIT.spark(series, 21) + f" [{DIM}]load[/]")
        return chr(10).join(rows)

    def _queue_markup(self, w: int) -> str:
        from taskboard.models import parse_iso
        today = datetime.now().date()
        rows = [f"[{MUT}]UP NEXT[/]"]
        open_t = [t for t in self.board.visible_tasks(False)
                  if not self.board.is_done(t)]

        def key(t):
            d = parse_iso(t.due_date)
            return (0 if getattr(t, "blocked", False) else 1,
                    0 if d else 1, (d - today).days if d else 9999)
        for i, t in enumerate(sorted(open_t, key=key)[:8]):
            d = parse_iso(t.due_date)
            days = (d - today).days if d else None
            chip = "--" if days is None else (f"{-days}d!" if days < 0 else f"{days}d")
            tone = ALERT_HUE if (days is not None and days < 0) else MUT
            rows.append(f"{KIT.queue_marker(i)} "
                        f"[{MUT}]{LG.mark(t.title)[:w-8]:<{max(1,w-8)}}[/]"
                        f"[{tone}]{chip:>5}[/]")
        return "\n".join(rows)


if __name__ == "__main__":
    forced = sys.argv[1] if len(sys.argv) > 1 else None
    TaskboardWidget(forced=forced).run()
