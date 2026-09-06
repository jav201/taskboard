"""STRUCTURE KITS — the per-language rendering mechanisms.

This module exists because of a measured failure: eight "languages" whose
structural tokens were consumed only by the hero widget, so cards, column
heads, meters, agenda, gantt, lanes, calendar and queue rendered identically
in all eight (PENDING.md item 0). A language that only changes colour is not
a language (tui-design/LANGUAGES.md).

A Kit is the code form of a language's commitments. Every structural token in
`themes.py` is read HERE (or by the hero) — the acceptance check is
`prototypes/verify_language.py`: mutate any structural token and the render
must change; strip colour from any two languages and they must differ.

Kits also carry the language's colour tokens (`kit["ink"]`…), so call sites
that only need colour keep working unchanged.

Mechanism map (each row is a commitment, not a glyph swap — LANGUAGES.md):

  naught      dots on a visible lattice; drawn 3x5 count sprites; no frames
  corgi       hairline aluminium spec-grid; numbered params; LCD segment bars
  instrument  braille sub-cell dots; round-dot scope register; frameless
  swiss       structure by space; typographic counts; airy pitch; the board
              is an EDITORIAL SPREAD on a 3-column type grid under ONE
              hairline (the masthead rule), not one rule per head
  industrial  flat function colour; bracketed [chips]; boxed bar; the board
              is coded FUNCTION PLATES, not framed boxes
  phosphor    one hue; severity/brightness; CRT decay tails; block cursor
  nord        the terminal's own idiom, on purpose — conventional bars/heads;
              the board is a MASTER/DETAIL SPLIT, a compact driving list
              beside one expanded task whose title is the first fixation
  bbs         double-line frames; gradient shoulders; solid CP437 ink
  ledger      PAPER: ruled money columns, dot leaders, tally marks in fives,
              a band every 5th line, and the red pen reserved for debt
  solari      SPLIT-FLAP DEPARTURE BOARD: the board is ONE SCHEDULE — task =
              row, phase = GATE (a reverse-video band), state = a WORD in a
              status column — quantity is DIGITS on flap cells and never a
              bar, and the seam `▁` is the only divider on the surface
  blueprint   CYANOTYPE TECHNICAL DRAWING: the frame stops CONTAINING and
              starts MEASURING — quantity is a DIMENSION SPAN with its figure
              standing on the span, metadata hangs off an EXTENSION LEADER,
              nothing is boxed, held work is HATCHED rather than coloured, and
              the whole frame budget is spent on one TITLE BLOCK in the bottom
              corner whose state cell is the sheet's single KNOCKOUT
"""
from __future__ import annotations

import copy as _copy
from datetime import date
from typing import NamedTuple

from rich.text import Text

from taskboard import bases as BS
from taskboard import naught as NA
from taskboard import raster as RS
from taskboard.themes import THEMES

# The MASCOT mask — one creature, drawn through each language's pixel base
# (Nothing's dot-face idiom; Charm/Claude-Code precedent: a TUI brand has a
# face). 10x6; each language renders it with its own pixel.
MASCOT = [
    ".##....##.",
    ".##....##.",
    "..........",
    "#........#",
    ".#......#.",
    "..######..",
]

# The vertical fill ramp. INDEX 0 IS THE UNLIT TRACK, NOT A SPACE (DATAVIZ
# law 4 — see the block below): level 1 is one eighth of a cell, the lightest
# fill this family has, so the unlit mark has to come from outside it, and the
# leader dot is the faintest mark this module draws.
RAMP = "·▁▂▃▄▅▆▇█"

# ===========================================================================
# COVERAGE -> GLYPH — the shared data-viz primitive (DATAVIZ.md; Bodmer P2)
#
# Anti-aliasing, translated to a cell grid. On a pixel display a coverage of
# 0.4 is a BLEND: 40% of the ink mixed into the ground, and the display has
# 256 steps to spend on it. A CELL HAS NO BLEND. It has a glyph. So coverage
# stops being an alpha and becomes an INDEX into an ordered ramp, and the two
# ends of the range are NAMED rather than interpolated:
#
#     c <= lo    the cell earned nothing -> ramp[0], the ramp's own UNLIT
#                glyph. Never a hard-coded space: DATAVIZ law 4 — a ramp
#                whose index 0 is air renders a flat-zero series as no
#                surface at all, and the law says track. **THE RAMPS BELOW
#                SPENT SIXTY PASSES SATISFYING THE LETTER OF THAT SENTENCE
#                AND NOT ITS CLAIM** — nine of the ten had a SPACE (or
#                braille's U+2800 BLANK, which is the same defect wearing a
#                glyph's clothes) sitting at index 0, so "the law says track"
#                was written directly above ten ramps that drew no track.
#                Cured in the sixty-first pass: every DATA ramp's index 0 is
#                now a mark the language already draws for "this position is
#                empty" on its own meter, and the one exemption is argued
#                where it lives (`shades`).
#     c >= hi    the cell is full -> ramp[-1], the terminal glyph.
#     between    ramp[max(1, round(n*c))] — the ordered middle band, and the
#                `max(1, ...)` is DATAVIZ law 3, the microbar floor.
#
# `lo` DEFAULTS TO 0.0 AND THAT IS A RULING, NOT A PLACEHOLDER. Coverage AA
# is free to drop faint ink below a threshold — that is what the threshold is
# for. Law 3 forbids it for DATA: "we have 1 overdue" may not render as "we
# have none". So on the data axis the only coverage that earns blank is
# exactly zero, and the `lo` seat is left open for STRUCTURE, which carries
# no such law. Where the two collide the skill wins, and this is where.
#
# ORDERED, DETERMINISTIC, AND **NEVER DITHERED**. The obvious next move from
# coverage AA is error diffusion: spread the quantisation residue into the
# next cell, or perturb the index by a hash of the position, and the ramp
# reads smoother. THIS MODULE REFUSES IT, and the refusal is written here so
# that nobody re-adds it as an improvement. Two reasons, both about this
# repo rather than about taste:
#
#   1. A position-dependent glyph makes the SAME VALUE draw differently in
#      two places. Every byte-identity law in `verify_language` becomes
#      unwritable, and a snapshot suite can no longer say what a render
#      should be — it can only say what it happened to be.
#   2. A static surface that re-renders on a tick would CHURN: the dither
#      pattern moves while the data stands still. That is motion with no
#      event behind it, which MOTION.md refuses on its own terms.
#
# One coverage, one ramp, one glyph, forever.
# ===========================================================================
COVER_LO = 0.0                 # at or under this, the cell draws its unlit
COVER_HI = 1.0                 # at or over this, the cell draws its terminal

# The RAMPS. Named by what they ARE, not by who uses them, because two
# mechanisms share `phosphor` and the eighths ramp serves both `_pulse` and
# `plot`. `shades` is here so that this registry and `bases.SHADES` are one
# definition rather than two copies — the suite asserts they agree, which is
# what makes the entry a law and not decoration.
#
# **INDEX 0 IS A TRACK, AND WHICH TRACK IS NOT A TASTE QUESTION.** The rule
# the sixty-first pass applied to all ten: the unlit glyph is the mark the
# language ALREADY DRAWS for an empty position on its own `meter` — so a
# spark's zero and the meter's unrun track are one idiom and not two — and
# where that mark already occupies a LIT level, the ramp's own family
# supplies the step above it rather than a new vocabulary being invented.
# Two ceilings hold it honest: the unlit carries ink (law 4) and it carries
# at most a QUARTER of the cell, because a track heavy enough to read as
# data is worse than no track at all.
COVER_RAMPS = {
    # 9 levels, vertical partial fill. `_pulse`'s zero bucket and `plot`'s
    # partial top cell. See `RAMP` for why the unlit is a leader dot.
    "eighths":   RAMP,
    # 5 levels, area fill (bases.shade). **THE ONE DECLARED LAW-4 EXEMPTION,
    # and it is a semantic one rather than a budget one:** this is the BITMAP
    # ramp, its cell is a pixel of a SPRITE, and a sprite's ground is ABSENCE
    # — not a datum worth zero. Inking index 0 would put texture inside every
    # empty pixel of every mascot. Law 4 is a law about DATA; no `meter`
    # mechanism routes this row, and `bases.py` owns the definition.
    "shades":    BS.SHADES,
    # sub-cell fill — instrument. THIS ROW IS THE DEFINITION of instrument's
    # unlit: `_meter_braille`'s flow row NAMES `[0]` and `[3]` from here
    # (#44). Pass 61 chose the glyph by looking at that meter and said so in
    # this comment, which left the two tied by PROSE and free to drift in
    # either direction; the source is here and the meter reads it. The blank
    # it replaces (U+2800) was a real codepoint with zero ink — the law-4
    # defect wearing a glyph's clothes.
    "braille":   "⠐⣀⣤⣿",
    # sub-cell dots — naught's FINE. The ONE ramp that was already right, and
    # the reason the defect was findable: `⠂` is the lattice mark, and it
    # separates from level 1 by dot POSITION rather than by dot count.
    "fine":      "".join(NA.FINE),
    # the conventional spark — nord (`blocks`) and industrial (`boxed`).
    # `░` is the track both `_meter_blocks` and `_meter_boxed` already draw
    # for the unrun part of the bar one row above the spark. It ties level 1
    # in ink and differs from it in FORM (a texture against a solid foot),
    # which is the distinction the greyscale law actually asks for.
    "blocks":    "░▂▅█",
    # two weights and a BROKEN one — swiss. The meter's track is `─`, but
    # that glyph is this ramp's level 1 (a measured minimum), so the unlit is
    # the same rule DASHED: a hairline chart's zero is not the absence of the
    # rule, it is the rule with nothing standing on it. Levels 2 and 3 still
    # repeat — a declared two-weight idiom, censused, and the milder half of
    # what DATAVIZ law 1 names.
    "hairline":  "┈─━━",
    # segment height + ghost — corgi. **THE CASE DATAVIZ LAW 1 CITES BY
    # NAME**, cured: it was `' ▄▄█'`, whose levels 1 and 2 were the same
    # glyph separated only by TONE, so a third of corgi's range vanished in
    # greyscale. `░` is corgi's own ghost (`plot`'s lcd branch draws exactly
    # that for an unlit segment — an LCD segment is never black, it is
    # faint), and the lit levels now climb in HEIGHT, which is the cure the
    # skill prescribes in the same sentence.
    "lcd":       "░▄▆█",
    # intensity — decay / gradient. The full shade family: a CRT's unlit
    # phosphor still glows, and `_meter_decay` already draws `░` behind the
    # head for exactly that reason.
    "phosphor":  "░▒▓█",
    # flat grey steps — darkside. `▁` is the language's declared track:
    # `_meter_step` fills with `█` against a `▁` rail precisely so that fill
    # and track differ by SHAPE. The step ladder rises above it.
    "step":      "▁▂▄█",
    # the leader/line ladder — blueprint. Four real drafting line types:
    # the leader DOT (which `plot`'s dimension branch already prints, dim,
    # for an unmeasured column), the broken line, the extension line, the
    # heavy dimension line. Nothing is ever filled — a drawing marks a
    # height, it never blocks it in.
    "dimension": "·╌─━",
}

# `meter` token -> ramp name. ONE SEAT: the data-viz family already
# dispatches on `meter`, so this is the same key, not a second vocabulary.
# `blocks` and `boxed` are absent on purpose — neither declares a spark ramp
# of its own, so both inherit the conventional one. `tally` is absent because
# a ledger BUILDS its ramp from its own token (see `Kit.cover_ramp`), and
# `odometer` is absent because a flap board's quantity is a FIGURE, not a
# coverage — it does not route at all.
METER_RAMP = {
    "dotgrid": "fine", "braille": "braille", "hairline": "hairline",
    "lcd": "lcd", "decay": "phosphor", "gradient": "phosphor",
    "step": "step", "dimension": "dimension",
}


def coverage_index(c: float, levels: int,
                   lo: float = COVER_LO, hi: float = COVER_HI) -> int:
    """The index a coverage of `c` earns on a ramp of `levels + 1` glyphs.

    This is the primitive; `coverage_to_glyph` is the lookup on top of it.
    Both exist because the INDEX is the thing — a caller that also picks a
    TONE from the level (every spark in this module does) must read the same
    number the glyph came from, and a second inline quantiser beside the
    first is the defect this pass exists to remove."""
    if c <= lo:
        return 0
    if c >= hi:
        return levels
    return max(1, min(levels, round(levels * c)))


def coverage_to_glyph(c: float, ramp: str,
                      lo: float = COVER_LO, hi: float = COVER_HI) -> str:
    """One cell of coverage `c`, drawn on `ramp`.

    **NEVER DITHERED.** The mapping is ordered, total and deterministic:
    the same coverage draws the same glyph in every cell of every render, in
    every process. This module refuses error diffusion and position-hashed
    perturbation — see the block above `COVER_LO` for the two measured
    reasons — so a value's glyph never depends on WHERE it is drawn."""
    return ramp[coverage_index(c, len(ramp) - 1, lo, hi)]


def visible(s: str) -> str:
    """The CELLS a markup row occupies, as plain text.

    Written here rather than in every caller because four of them had it
    already and one of them (the prototype sweep) had to get the ORDER right
    on its own: `mark()` escapes a literal `[` as `\\[`, so the escape must be
    lifted out before the tags are stripped or an escaped bracket is read as
    a style tag. That is this module's documented pitfall A1, and a caller
    that composes rows out of other rows -- an overlay, a pane, a sheet --
    cannot do width arithmetic without it."""
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] == "[":
            out.append("[")
            i += 2
        elif s[i] == "[":
            j = s.find("]", i)
            if j == -1:
                out.append(s[i])
                i += 1
            else:
                i = j + 1
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def mark(s: str) -> str:
    """Literal text inside a markup string, escaped so that BOTH parsers this
    app is read by agree on it.

    `rich.markup.escape` only escapes a `[` that looks like the start of a
    TAG, and that is where the two disagree: `[ ` and a bare `[` are left
    alone, rich renders them as literal text, and TEXTUAL — whose own markup
    parser is what `Static.update` actually uses — swallows the `[/]` that
    follows as literal text too, so the style never closes and a raw `[/]`
    reaches the glass. It had been doing exactly that on this app's config
    screen for four passes (`[[/]█|]` where a bracketed switch was meant),
    and the suite could not see it because its oracle was rich.

    Escaping EVERY `[` as `\\[` is accepted by both parsers, so this is one
    string that means one thing on both sides.

    **THIS IS THE ONLY ESCAPING THIS MODULE USES.** The fifty-sixth pass swept
    the twenty-three `rich.markup.escape` seats that were left (item #25) and
    dropped the import, so "literal text goes through `mark`" is a rule a grep
    can check rather than a claim each new call site has to remember. What the
    sweep found on the way is worth more than the swap: `escape` was not
    merely leaking a `[/]`, it was DELETING user text. A title typed
    `[urgent] ship it` is escaped by rich (`[u` looks like a tag to it), but
    three languages upper-case their titles, and `[URGENT]` does NOT look like
    a tag to rich — so it went through unescaped and Textual ate it. corgi,
    solari and blueprint were each printing ` SHIP IT`.

    THE ONE CASE NEITHER ESCAPING CAN CURE, measured rather than assumed:
    text ending in a single backslash. `escape` doubles it, `mark` does not,
    and that is the only disagreement between them on text with no `[` in it.
    It does not matter on the glass, because the seat is always
    `f"[tone]{...}[/]"` and TEXTUAL reads the `\\` before a `[` as a literal
    backslash plus an ESCAPED bracket either way — so both escapings print a
    raw `[/]` there, and no encoding of a trailing backslash was found that
    both parsers close the tag after (`prototypes/out/_p56_prove.py` §3b
    searched five). It is a Textual-side limit, it is filed as its own item,
    and it is not made worse by this sweep."""
    return s.replace("[", "\\[")


def _pulse(counts: list[int], width: int) -> str:
    """Relative load across buckets as a ramp row (the conventional idiom —
    nord/industrial keep it; other languages replace the mechanism)."""
    if not counts or width <= 0:
        return ""
    hi = max(counts) or 1
    per = max(1, width // len(counts))
    out = []
    for n in counts:
        out.append(coverage_to_glyph(n / hi, COVER_RAMPS["eighths"]) * per)
    return "".join(out)[:width].ljust(width)


def _fit(title: str, room: int) -> str:
    """Truncate-then-escape. Width math must run BEFORE markup escaping."""
    if room <= 0:
        return ""
    cut = title if len(title) <= room else title[: max(0, room - 1)] + "…"
    return mark(cut)


def _resample(series: list[int], n: int) -> list[int]:
    """REFLOW, never truncate (the Kimi-fork law): when a series is wider
    than its surface, shrink RESOLUTION and keep every sample — bucket-max,
    because load peaks are the datum. `series[:w]` silently lied about the
    tail (the calendar's last week vanished at 21 cells)."""
    if len(series) <= n or n <= 0:
        return list(series)
    step = len(series) / n
    return [max(series[int(i * step): max(int(i * step) + 1,
                                          int((i + 1) * step))])
            for i in range(n)]


def _fit_parts(parts: list[tuple[str, str]], w: int) -> str:
    """Progressive disclosure for metadata rows: `parts` are (markup, plain)
    pairs joined while their PLAIN width still fits w. A fixed-width detail
    row WRAPS in a narrow column and the card grows a phantom third row —
    fields that don't fit are dropped, never folded."""
    out, used = [], 0
    for mk, pl in parts:
        if used + len(pl) > w:
            break
        out.append(mk)
        used += len(pl)
    return "".join(out)


def _span_text(n: int, label: str, fill: str = "─", open_: str = "├",
               close: str = "┤", clipped: bool = False, brk: str = "╌",
               outside: bool = True) -> str:
    """A DIMENSION SPAN: two terminators, a run between them, and the figure
    standing ON the run — `├──── 03D ────┤`.

    Module level rather than a kit method because the `dimension` METER draws
    the same object as the `blueprint` kit does, and two implementations of one
    mechanism is how a language forks its own identity (DATAVIZ.md's dispatch
    law). Exactly `n` cells whenever the figure fits inside the run.

    Below the width its own label needs, the figure steps OUTSIDE the span
    rather than being ellipsed into it — which is what a draftsman does with a
    dimension too small to letter. A caller that reserved an EXACT seat passes
    `outside=False` and the figure is dropped instead, so the seat is kept.

    `clipped` is the CLIP FLAG (DATAVIZ: clip and flag, never clamp): the run's
    first cell becomes a BREAK mark, so an off-scale span says it is off-scale
    and the figure on it stays the truth.
    """
    n = max(2, int(n))
    run = n - 2
    inner = run - (len(label) + 2)
    if inner >= 0:
        left = inner // 2
        body = (open_ + fill * left + " " + label + " "
                + fill * (inner - left) + close)
    elif outside:
        body = open_ + fill * run + close + " " + label
    else:
        body = open_ + fill * run + close
    if clipped and n >= 3:
        body = body[0] + brk + body[2:]
    return body


# ===========================================================================
# THE COMPONENT CONTRACT (tui-design/COMPONENTS.md).
#
# Transcribed from LVGL's own part decomposition, which is the one
# professional corpus that publishes a control's anatomy as DATA rather than
# as a picture. Two claims, and they are the whole track:
#
#   1. PARTS ARE UNIVERSAL. No language may add or remove a part. A language
#      expresses itself in HOW each part is drawn, never in WHICH parts
#      exist. `bar` is EXACTLY `slider` minus the knob — the knob is the
#      affordance of CONTROL, and its absence is what makes a readout.
#   2. STATES FOLLOW FROM PARTS, so they are DERIVED and not a second
#      hand-written list. A component with no knob takes no interactive
#      state: there is nothing to focus, nothing to edit, nothing to press.
#
# The state axis is LVGL's canonical six. EDITED is the one the touch world
# defines and then styles 0 times out of 1848 sampled widgets — "focused AND
# the arrow keys now mutate the value instead of moving focus". In a keyboard
# TUI that state is not exotic, it is the centre of the interaction.
#
# INVALID IS THE SEVENTH ENTRY AND THE SIXTH CONTROL STATE (kits-learn-3,
# operator ruling 1 of 2026-09-04), and it is the one the PROTOTYPE round
# found by rendering a form: five languages marked a rejected value with the
# same red `!`, because the contract had no seat for the state and the frame
# had to invent one. That is the palette-swap failure at a single glyph — the
# exact defect this file exists to make unconstructable — so the state is
# DERIVED like the other five and drawn in SHAPE by each language's own table.
# ===========================================================================
DEFAULT = "default"
FOCUSED = "focused"
EDITED = "edited"
ACTIVE = "active"
CHECKED = "checked"
INVALID = "invalid"
DISABLED = "disabled"
STATES = (DEFAULT, FOCUSED, EDITED, ACTIVE, CHECKED, INVALID, DISABLED)

COMPONENT_PARTS = {
    "slider": ("main", "indicator", "knob"),
    "bar": ("main", "indicator"),
    # THE SWITCH DECLARES THE SAME THREE PARTS AS THE SLIDER, and that is a
    # finding rather than a copy-paste: a switch is a slider whose range is
    # boolean, so its ANATOMY is a range control's anatomy. Run the shipped
    # composer with lo=0, hi=1 and the terminal's conventional switch falls
    # out with no special case — indicator behind the knob when on, track
    # ahead of it when off. The registry cannot tell switch from slider
    # because on the axis the registry measures, they are the same thing.
    # What differs is the RANGE, and the registry states that as CHECKABLE.
    "switch": ("main", "indicator", "knob"),
    # THE CHECKBOX HAS NO INDICATOR, and that absence is the whole increment.
    # An indicator is an EXTENT — the run between an origin and the value —
    # and a box with a mark in it has no origin to run from. So the checkbox
    # is the first component whose value does not choose a POSITION: it
    # chooses whether the mark is THERE. One registry fact ("indicator" in
    # parts) is what the composer, the slot count and the chrome all read.
    "checkbox": ("main", "knob"),
    # THE RADIO ITEM DECLARES WHAT THE CHECKBOX DECLARES, and the registry is
    # right to be unable to tell them apart: an ITEM is a well and a mark, no
    # extent, exactly the checkbox's anatomy. What makes it a radio is not a
    # part — it is that its bit is not its own. The registry describes ONE
    # component's parts and has nothing to say about siblings, so the group
    # invariant lives at `group_states` instead, one level up. Naming that
    # boundary is the finding: the parts registry is a per-component fact and
    # a scope larger than a component needs a seat larger than the registry.
    "radio": ("main", "knob"),
    # THE BUTTON DECLARES ONE PART, and the decision it forced is whether its
    # LABEL is a second one. It is not, and the argument is what a part IS:
    # a slot the LANGUAGE draws, from its own glyph table, in every state.
    # The label's text comes from the CALLER. A language handed a word it did
    # not choose can only "draw" it by mangling it — recasing, letterspacing,
    # bracketing it — and every one of those either destroys the caller's word
    # or moves the field under it. So text stays OUT of the registry, exactly
    # where LVGL puts it (a button has `main`; its label is a CHILD object,
    # never a part), and `main` is the label's GROUND: the walls this language
    # draws and the field they enclose.
    #
    # The falsifiable consequence, which is the reason this is a decision and
    # not a preference: because the label is content, the state cannot ride on
    # it, so it must ride on the cells the language owns. A button therefore
    # spends at least one cell per side on its own walls, the four states are
    # required to differ in the WALLS' shape, and the label is required to
    # come back out of the render byte for byte. Had the label been a part,
    # those two laws would contradict each other.
    #
    # NO INDICATOR AND NO KNOB, and that pair is the whole anatomy: nothing is
    # measured (no extent) and nothing is set (no bit), so there is no value
    # here at all — the first component in this registry with none. What that
    # cost the derivation is stated at `actuator` below.
    "button": ("main",),
    # THE TEXT FIELD, AND `caret` IS THE FIRST NEW PART SINCE THIS REGISTRY
    # WAS WRITTEN. The button ruled that TEXT is not a part; the question a
    # text field asks is the opposite one — the caret is not text, so is it a
    # part, or is it a STATE of `main`? It is a part, and there are three
    # reasons, the third of which is structural rather than aesthetic:
    #
    #   * IT PASSES THE BAR THE LABEL FAILED. A part is a slot the LANGUAGE
    #     draws, from its own glyph table, in every state it applies to. The
    #     caret's glyph is the language's (naught's lit lattice dot, ledger's
    #     pen, instrument's braille tick), never the caller's, and where it
    #     stands is state. All three tests, where the label failed all three.
    #   * A STATE CANNOT PICK OUT ONE CELL. This is the decisive one. In this
    #     renderer a state is a property of the WHOLE component — `part_glyph`
    #     takes (part, state) and answers once — so "main, but in EDITED"
    #     would put a caret in EVERY cell of the field. The only thing that
    #     distinguishes one cell from its neighbours here is its PART TAG.
    #     A mark at one of N seats is a part or it is nothing.
    #   * AND IT IS NOT THE KNOB. Calling it `knob` would have cost no new
    #     part and would have made `("main", "knob")` — the CHECKBOX's exact
    #     tuple — mean two different mechanisms: a mark that is either there
    #     or not, and a mark that is at one of `w` places. Identical parts
    #     with different anatomies is precisely what this registry exists to
    #     make impossible (the slider and the switch share a tuple because
    #     they genuinely share an anatomy).
    #
    # `main` IS THE FIELD'S GROUND, and its glyph carries the walls with it —
    # an ODD string read at three seats: the wall that opens, the RUNE the
    # paper is made of, the wall that closes (`field_form`). One part, one
    # string, one tone, because the walls and the paper are one thing: the
    # ground this language lays under someone else's words. The button's
    # walls are `main` for the same reason; it needs no ground rune because
    # it has no interior to spend one on, and this component does.
    #
    # THE WALLS ARE NOT OPTIONAL, and that is the button's physics again. A
    # value may fill every cell of the field, so a field with no cells of its
    # own would have nowhere to say DISABLED without editing the user's text.
    # The state rides the walls; the value comes back byte for byte.
    "textfield": ("main", "caret"),
    # THE SCROLL BAR DECLARES THE BAR'S EXACT TUPLE, and declaring NO new
    # part is the whole finding. The caret was a new part because a state
    # cannot pick out one cell; a thumb is not a new part because a scroll
    # bar HAS no cell a bar does not have. It is a track and a run on it —
    # `("main", "indicator")`, twice over, and the registry is right to be
    # unable to tell the two apart on their parts, exactly as it cannot tell
    # a slider from a switch or a checkbox from a radio.
    #
    # WHAT DIFFERS IS THE VALUE, AND IT DIFFERS IN ARITY. A bar's value is
    # ONE number and its extent is anchored at the origin: the run measures
    # `val` and always starts at cell 0. A scroll bar's value is TWO — where
    # the view is AND how big it is — and its run is anchored nowhere: it
    # floats, and its LENGTH is the second number made visible. That is the
    # first thing `value_pos` (one value -> one position) cannot answer, and
    # it is answered by `view_pos` below rather than by a fourth part.
    #
    # THE PARTS REGISTRY CANNOT SEE ARITY, and it never could — parts are
    # SLOTS. So the fact is DECLARED, at `VIEWED`, which is the same seat
    # and the same reason CHECKABLE exists: two components sharing a tuple
    # and differing in what their value IS. CHECKABLE says the value's RANGE
    # is boolean; VIEWED says the value's ARITY is two. One family, second
    # member — which is the answer to "a third declared fact is a smell".
    #
    # IT IS A READOUT, and that is the derivation's answer rather than a
    # taste. In THIS keyboard TUI nothing is ever scrolled by grabbing the
    # bar: the keys act on the CONTAINER and the bar reports where the
    # container got to. So there is no grip, and `actuator` therefore returns
    # None, and `component_states` therefore gives DEFAULT and DISABLED and
    # nothing else — the bar's own two states, reached with zero edits to any
    # seat. A `knob` added here to make it feel operable would be the dead
    # metadata this file has refused twice.
    "scrollbar": ("main", "indicator"),
    # THE STEPPER, AND ITS FIRST QUESTION IS WHETHER IT IS A COMPONENT AT
    # ALL. A stepper through a named set and a radio over the same set are
    # THE SAME CHOICE — one option list, one selected index — so the honest
    # opening position is that they are one registry entry with two
    # drawings. They are not, and the reason is the one this registry has
    # been settling since the switch:
    #
    #   * the registry describes ANATOMY. A radio ITEM is a well and a mark
    #     (`("main", "knob")`); a stepper is a WORD BETWEEN TWO STEPS. Those
    #     are different slots, drawn from different glyphs, in different
    #     numbers — a radio set of three draws three wells and a stepper
    #     draws two affordances whatever the set's size.
    #   * so this is the INVERSE of every collision this registry has met.
    #     The switch shares the slider's tuple and differs in its value's
    #     RANGE; the scroll bar shares the bar's and differs in its ARITY;
    #     both were separated by a declared fact. Here the parts DIFFER and
    #     the value model is the SAME — and a shared value model is not a
    #     registry fact at all, because `group_states` already owns it, one
    #     level above the registry, exactly where the radio put it.
    #
    # TWO ENTRIES, ONE CHOICE MODEL, and the falsifiable half is the second
    # one: `Kit.stepper` reaches `group_states` with the set's size and its
    # index, so an out-of-range selection RAISES here for the same reason it
    # raises there, and the state of the option a stepper SHOWS is the state
    # of the item a radio MARKS, byte for byte, at every index. Desynchronise
    # them and the suite says so.
    #
    # `step` IS ONE NEW PART AND THE TWO ENDS ARE ITS TWO HALVES. The caret's
    # argument, re-run and coming out the other way: a state cannot pick out
    # one cell, so a mark at one of N seats must be a part — but the two
    # steps are not at N seats, they are at exactly TWO, and a two-cell part
    # whose glyph is an EVEN string read at its two halves is the convention
    # this file already uses twice (the button's walls, the field's ground).
    # Declaring `less` and `more` would have bought two registry entries for
    # a distinction the cell's POSITION already carries.
    #
    # `main` IS WHERE A STEP IS NOT, which is what `main` means everywhere in
    # this registry — the ground a part stands on. A clamped stepper at its
    # floor has no step down, so that seat draws GROUND, and the end
    # behaviour is therefore visible as a PART TAG and hence as a GLYPH and
    # hence in greyscale. WRAP AND CLAMP DIFFER IN SHAPE, with no new state,
    # no per-cell state and no colour.
    #
    # AND THE SHOWN OPTION IS CONTENT — the button's ruling for the third
    # time (a label, a value, an option). `has_value` is therefore False and
    # nothing is printed beside it: what a stepper reports is standing in the
    # middle of it, in the caller's own bytes.
    "stepper": ("main", "step"),
}

# THE GRIPS — the marks a user MOVES, as a registry fact.
#
# `actuator` used to read "a knob where one is declared". The caret is a grip
# and is not a knob: a knob rides a track and reports a MAGNITUDE, a caret
# rides a field of characters and reports an INDEX. They are different parts
# for the reason stated at `textfield` above, but they are the same thing to
# the hand, and to the accent rule — the part under the finger.
#
# Two entries and no derivation, deliberately: which parts are grips is not
# computable from their names, so it is DECLARED, exactly as CHECKABLE is.
# The alternative was `actuator` growing an `or "caret" in parts`, which
# hides a registry fact inside a derivation and is how a contract starts
# accumulating hand lists at its seats instead of in its registry.
# THE STEPPER ADDED THE THIRD, and it is the cheapest kind of growth this
# registry has: a tuple gained an entry and no derivation was touched. A step
# is pressed, so it is the part under the finger, so the accent belongs on it
# for the reason a knob and a caret get one. `GRIPS` exists precisely so that
# this is a REGISTRY edit rather than an `or "step" in parts` growing inside
# `actuator` — which is the shape a contract rots into.
GRIPS: tuple[str, ...] = ("knob", "caret", "step")

# THE CHECKABLE FACT — one registry entry, two consequences.
#
# For an on/off control the value IS the checked bit: "this switch is on" and
# "this switch's value is hi" are one fact, not two. So declaring a component
# checkable says (a) CHECKED joins its state axis as a BIT that combines with
# the control states — LVGL styles CHECKED|PRESSED as first-class and so must
# we — and (b) it has NO EDITED state, because EDITED means "focused and the
# arrows now range through the value" and a boolean has no interior to range
# through. Pressing toggles instantly; that is ACTIVE, not EDITED.
#
# Both consequences are DERIVED below from this one tuple. Nothing hand-lists
# a switch's states, and the next on/off component (checkbox, radio) lands
# here rather than in a branch.
#
# THE CHECKBOX LANDED HERE AND THE DERIVATION DID NOT MOVE. That is the fact
# the fiftieth pass went looking for: `checkbox` is the first checkable that
# is NOT a boolean slider — no indicator, no travel, a mark that appears
# rather than moves — and adding its name to this tuple gave it the whole
# eight-state product axis with no edit to `component_states`, `control_of`,
# `with_checked`, `is_checked`, `bool_value`, `state_chain` or
# `checked_pairs`. What DID have to grow was the composer, and only where it
# had assumed every component has an extent. The state axis belongs to
# CHECKABLE; reading a boolean as a POSITION belonged to the switch.
# AND THE RADIO LANDED HERE TOO, with the derivation still unmoved. Three
# components now, one axis, zero edits at the seats — but the radio is the
# first one for which that is NOT the whole story, because a radio item's
# checked bit is not a fact about the item. `with_checked` survived contact
# with the invariant by being CALLED FROM `group_states` instead of from a
# caller: the writer of the bit is unchanged, the AUTHOR of it moved.
CHECKABLE: tuple[str, ...] = ("switch", "checkbox", "radio")

# THE VIEWED FACT — the second member of CHECKABLE's family, not a third
# kind of thing.
#
# This registry now carries three declarations beside the parts, and they are
# TWO families rather than three lists. GRIPS is a fact about PARTS (which
# slot the hand moves). CHECKABLE and VIEWED are facts about the VALUE that
# the parts cannot show: CHECKABLE says its RANGE is boolean, VIEWED says its
# ARITY is two — a window is (where the view is, how big it is), and no
# expression over `("main", "indicator")` can tell that from a bar's single
# magnitude, because `bar` declares the same tuple.
#
# That collision is the proof it must be DECLARED. The registry has met it
# twice before and answered the same way both times: the switch shares the
# slider's tuple and is separated by CHECKABLE; the radio shares the
# checkbox's tuple and is separated one level up at `group_states`. A fact
# that no derivation can reach is a registry entry or it is a hand list at a
# seat, and this file has ruled against the second one four times.
#
# The falsifiable consequence, which is why this is a decision and not a
# label: the composer forks on `name in VIEWED` — take the scroll bar out of
# this tuple and it draws as a BAR, an extent anchored at cell 0 whose length
# is its position. Every window law goes red at once, and none of them had to
# name a component to do it.
VIEWED: tuple[str, ...] = ("scrollbar",)

CHECK_SEP = "+"                            # "checked+focused" — LVGL's OR


def is_checked(state: str) -> bool:
    return CHECKED in state.split(CHECK_SEP)


def control_of(state: str) -> str:
    """The control bit of a possibly-combined state: `checked+focused` ->
    `focused`, `checked` -> `default`. Every place that used to compare a
    state for equality asks this instead, so a combination behaves like the
    control state it carries and no call site grows a branch."""
    rest = [b for b in state.split(CHECK_SEP) if b != CHECKED]
    return rest[0] if rest else DEFAULT


def with_checked(state: str, on: bool) -> str:
    """Set or clear the checked bit of a state. This is the only way the bit
    is ever written, which is why a switch cannot end up claiming CHECKED
    while its knob sits at the off position."""
    base = control_of(state)
    if not on:
        return base
    return CHECKED if base == DEFAULT else f"{CHECKED}{CHECK_SEP}{base}"


def bool_value(state: str) -> int:
    """The value a boolean control renders at: its checked bit, as a number
    the shared value model can take. One expression, so the cells and the
    label beside them can never read the same switch differently."""
    return 1 if is_checked(state) else 0


def state_chain(state: str) -> tuple[str, ...]:
    """Glyph-lookup order for a state: the exact combination, then its
    control bit, then CHECKED, then DEFAULT.

    The control bit is tried BEFORE the checked bit on purpose — a focused
    switch must look focused whether it is on or off, and checkedness is
    already carried by the knob's position, which is shape."""
    keys = [state]
    ctl = control_of(state)
    if ctl not in keys:
        keys.append(ctl)
    if is_checked(state) and CHECKED not in keys:
        keys.append(CHECKED)
    if DEFAULT not in keys:
        keys.append(DEFAULT)
    return tuple(keys)


def has_value(name: str) -> bool:
    """Does this component HOLD a value? Derived, from the two registry facts
    that can carry one: an EXTENT measures a number, and CHECKABLE declares a
    bit. A component with neither holds nothing.

    Introduced by the button, which is the first component with no value at
    all, and it is what the label question turns on: a component that holds a
    value has a READOUT standing beside it (`value_label`, `check_label` — a
    slider's number, a switch's `ON`, an option's name), and a component that
    holds none has nothing to report. Its only text is the caller's name for
    the action, and that stands INSIDE the control. So "the word is outside"
    and "the word is inside" are the same rule read at two values of one
    derived fact, rather than two rules with a list of components under
    each.

    THE STEPPER TOOK THE THIRD TERM, and the pair this now makes with
    `has_interior` is worth reading as a pair: an INTERIOR is cells a cursor
    moves between (extent, field, series) and a VALUE is a number or a bit the
    REGISTRY holds (extent, series, bit). The one term in each that is not in
    the other is the whole content ruling — a `caret` indexes cells the CALLER
    fills, so a field has an interior and holds no value; a `step` chooses
    among seats the registry counts, so a stepper holds one. Its WORD is
    content and stands inside it, and nothing is printed beside it, which is
    the button's arrangement reached from the opposite side."""
    parts = COMPONENT_PARTS[name]
    return "indicator" in parts or "step" in parts or name in CHECKABLE


def has_interior(name: str) -> bool:
    """Does this component have CELLS THE ARROWS CAN RANGE THROUGH? That is
    what EDITED requires, and the text field is what forced it to be named.

    The registry declares an interior two ways, and they are two ways of
    measuring the same run: an EXTENT (`indicator`) is a run measured from an
    origin, and a FIELD (`caret`) is a run indexed by a mark. Both are cells
    between which a cursor moves; neither a boolean nor a button has any.

    The button's pass wrote this term as `"indicator" in parts`, and that was
    true of every component that existed then. It is now read as the concept
    it was standing in for — which is the same correction the button itself
    made to `knob` when it meant `the part you grab`. Note what did NOT
    happen: no new registry fact. Both terms are parts already declared.

    THE STEPPER ADDED A THIRD TERM, and the smell is named rather than
    denied. Three ways of saying "there is more than one place the value can
    be": an EXTENT is a run measured from an origin, a FIELD is a run indexed
    by a mark, and a SERIES is seats reached by stepping. Each term is a PART
    already in the registry — nothing here is a component name and nothing
    here is a new declared fact, which is the alternative that was weighed
    and refused: a `RANGED = ("stepper",)` tuple would be a third family with
    one member and no derivation able to reach it, which is the dead metadata
    the fifty-fourth pass warned the next increment about. An enumeration of
    ANATOMIES is bounded by the registry; a list of NAMES is not."""
    parts = COMPONENT_PARTS[name]
    return "indicator" in parts or "caret" in parts or "step" in parts


def actuator(name: str | None = None) -> str | None:
    """THE PART A USER GRABS — `None` for a readout, which has none.

    THE REFINEMENT THE BUTTON FORCED, and it is stated here because it is the
    one law of this contract that moved. Until now "has a knob" and "is a
    control" were the same sentence, and three seats said `knob` when they
    meant *the part you grab*: the state derivation, the tone rule, and four
    languages' overrides of it. A button has no knob and IS a control, so the
    sentence had to be split — and it splits on the registry, with no new
    registry fact and no hand list:

      * a knob is a grip wherever one is declared;
      * a component that holds a VALUE and has no knob is a READOUT — the
        indicator reports a number nobody sets, which is exactly the law that
        made `bar` a readout, unchanged;
      * a component that holds no value and has no knob has nothing to report
        and nothing to grip separately, so the whole control is the grip: its
        ground. That is the button, and it is why `("main",)` takes the
        control states while `("main", "indicator")` still takes none.

    Giving the button a decorative `knob` part instead would have kept the old
    one-line law and bought a lie: a part invented to satisfy a derivation is
    dead metadata, which is the defect this file has cured twice (a hardcoded
    mechanism makes its token dead metadata again).

    THE TEXT FIELD WIDENED THE FIRST CLAUSE AND NOTHING ELSE. "A knob is a
    grip wherever one is declared" is now "a GRIP is a grip", read off the
    `GRIPS` registry tuple — because a caret is a mark the hand moves exactly
    as a knob is, and the accent belongs on it for the same reason. The other
    two clauses are untouched, and every other component's answer is
    byte-identical.

    `None` for `name` is for callers that do not say which component is asking
    — they get `knob`, the grip of every component that has one, which is what
    the rule said before it was refined."""
    if name is None:
        return "knob"
    parts = COMPONENT_PARTS[name]
    for grip in GRIPS:
        if grip in parts:
            return grip
    return None if has_value(name) else parts[0]


def component_states(name: str) -> tuple[str, ...]:
    """Which states apply to `name` — DERIVED from its parts and from
    CHECKABLE, never hand-listed.

    This is the contract's sharpest edge. `bar` is not "a slider we decided
    not to make focusable"; it has no knob, so it has no control affordance,
    so FOCUSED / EDITED / ACTIVE are not states it can be in.

    A CHECKABLE component's axis is the PRODUCT of its control block with the
    checked bit — the base block first, then the same block with CHECKED set.
    EDITED is dropped from a checkable's block for the reason stated at
    CHECKABLE: a boolean has no interior. One seat, and it is the registry.

    TWO EXPRESSIONS, and the button moved both without adding a fact:
    * the control block is gated on the ACTUATOR, not on the knob — see there
      for why a one-part valueless component is its own grip;
    * EDITED is gated on the INTERIOR, positively. It used to read "unless
      checkable", which was true of every component that had a knob at the
      time and silently false for a button: the arrows can only range through
      a value that has an interior. The button read that interior off the
      EXTENT; the TEXT FIELD has an interior and no extent, so the term is
      now `has_interior` — the concept the extent was standing in for. Both
      of its terms are parts already in the registry, and the removal still
      falls out of CHECKABLE for the switch.

    THE TEXT FIELD IS WHERE EDITED FINALLY MEANS WHAT IT SAYS. On a slider it
    is "the arrows now move the value"; here it is "the keystrokes now land
    IN the text", and the caret is the promise of exactly that — which is why
    the caret is drawn in this state and in no other. FOCUSED is the field
    selected; EDITED is the field entered.

    INVALID RIDES EDITED'S OWN CONDITION, and it is one term rather than a
    third expression because it is one sentence: WHAT THE ARROWS CAN CHANGE,
    THE FORM CAN REJECT. A component with an actuator and an interior holds a
    value its user PUT there, and a value that was put there can be wrong; a
    readout was told its number, a button holds none, and neither has anything
    to be wrong about.

    THE EXCLUSION IS THE DECISION, not an oversight, and it is the same
    registry fact that already removed EDITED: a CHECKABLE control's range is
    BOOLEAN, and a boolean cannot be out of range — both of its values are
    legal. "This box is required and unticked" is not a fact about the box, it
    is a fact about the FORM, which is a set of controls and has no seat on a
    per-component state axis. This contract has refused three times to answer
    a scope question with a hand list at a seat, and it refuses a fourth: the
    day a form object exists is the day that state has somewhere to live."""
    parts = COMPONENT_PARTS[name]
    checkable = name in CHECKABLE
    # ONE TERM, TWO USES: a value its user PUT there. EDITED is the putting,
    # INVALID is the answer it got back, and they cannot come apart.
    settable = bool(actuator(name)) and has_interior(name) and not checkable
    base = [DEFAULT]
    if actuator(name):
        base += [FOCUSED]
        if settable:
            base += [EDITED]
        base += [ACTIVE]
        if settable:
            base += [INVALID]
    base.append(DISABLED)
    if not checkable:
        return tuple(base)
    return tuple(base) + tuple(with_checked(s, True) for s in base)


COMPONENT_STATES = {n: component_states(n) for n in COMPONENT_PARTS}


def checked_pairs(name: str) -> tuple[tuple[str, str], ...]:
    """A checkable component's axis as (unchecked, checked) row units.

    The gallery's seat. What is worth seeing about a switch is what the
    CHECKED bit DOES at each control state, and a row per state would have
    cost eight rows in a box that already scrolls (PENDING, forty-eighth
    pass). Four rows, both bits, derived from the registry."""
    return tuple((s, with_checked(s, True))
                 for s in COMPONENT_STATES[name] if not is_checked(s))


def group_states(n: int, selected: int, state: str = DEFAULT,
                 focus: int | None = None) -> tuple[str, ...]:
    """THE GROUP SEAT — the state of every item in a selection set, derived
    from ONE index. The first thing in this contract whose scope is larger
    than a component.

    THE INVARIANT IS STRUCTURAL, not checked. "Exactly one of these is set"
    is not enforced here; it is UNREPRESENTABLE here, because the bit is
    computed from `i == selected` and an integer cannot equal two values or
    none. There is no per-item boolean for a caller to desynchronise, which
    is why `radio()` takes no `on` argument the way `switch(on)` and
    `checkbox(on)` do. That missing argument IS the group scope.

    An out-of-range `selected` is the one way to ask for zero marks, and it
    RAISES rather than clamping: a clamp would silently move the user's
    selection, and a set with nothing set is not a radio set. The suite's
    control drives exactly this.

    FOCUS IS A SEPARATE INDEX, and that separation is the state axis the
    group introduces. The cursor may sit on an item that is not the chosen
    one — both are on screen at once and both must be readable, which is the
    sibling-scoped version of the EDITED-is-not-FOCUSED problem. A DISABLED
    group has no cursor at all: dead controls do not hold focus.

    It names no component, and that is deliberate — a segmented control or a
    tab bar is the same fact about siblings wearing different glyphs."""
    n = int(n)
    if n < 1:
        raise ValueError("a selection group with no items is not a group")
    if not 0 <= int(selected) < n:
        raise ValueError(f"selected {selected} is outside a group of {n}: "
                         f"a set with nothing set is not a selection")
    ctl = control_of(state)
    out = []
    for i in range(n):
        if ctl == DISABLED:
            base = DISABLED
        elif focus is not None and i == int(focus):
            base = ctl
        else:
            base = DEFAULT
        out.append(with_checked(base, i == int(selected)))
    return tuple(out)


def value_pos(val: float, lo: float, hi: float, cells: int) -> int:
    """THE VALUE MODEL — one seat, shared by every language and both
    components. value -> cell index in [0, cells-1].

    `lo > hi` is an INVERTED scale (LVGL's `_invert`) and needs no branch:
    the span goes negative and the fraction runs the other way, which is
    exactly what inversion means. A zero span never divides.

    Ten languages used to carry ten copies of this arithmetic, each with its
    own off-by-one (`w`, `w - 1`, `w - 2`, `w // 3`), which is the fork
    defect this repo has cured twice before at the hero."""
    cells = max(1, int(cells))
    if cells == 1 or hi == lo:
        return 0
    f = (val - lo) / (hi - lo)
    return max(0, min(cells - 1, round((cells - 1) * f)))


def value_at(pos: int, lo: float, hi: float, cells: int) -> float:
    """The inverse of `value_pos` — the value a cell index stands for.

    The round trip that is exact is POSITION -> value -> position; the other
    direction quantizes, and a check that claimed otherwise would be lying
    about what a cell can hold."""
    cells = max(1, int(cells))
    if cells == 1:
        return lo
    return lo + (hi - lo) * (max(0, min(cells - 1, int(pos))) / (cells - 1))


def view_start(total: int, size: int, focus: int | None = None,
               start: int = 0) -> int:
    """THE WINDOW MODEL, half one: WHERE THE VIEW LEGALLY IS.

    `start` is clamped into the range a window of `size` can occupy inside
    `total`, and then moved THE LEAST IT CAN to keep `focus` inside it. A
    window that jumped to centre the focus would throw away the reading the
    user already has; a window that did not move at all would let the focus
    walk off the edge, which is truncation wearing a scroll's clothes.

    THIS EXISTED ALREADY, WITH NO NAME AND NO SEAT. The fifty-third pass
    computed exactly this arithmetic inline in `Kit.textfield` — five lines
    that nothing in the registry declared, that no other component could
    reach, and that the composer alone knew. That is the fork defect this
    repo has cured three times (the hero's metrics, the head's width, the
    switch's frames): a measure with one call site is not a measure yet, it
    is a local variable. The scroll bar is what gave it a second caller, and
    the second caller is what makes it a seat.

    `focus=None` is "no cursor to keep in view" — the scroll bar's case,
    where the window is HANDED a start and only needs clamping.

    The arithmetic is unchanged from the fifty-third pass's inline form, and
    that is asserted rather than asserted-about: the field's window laws are
    older than this function and they pass untouched."""
    total, size = max(0, int(total)), max(1, int(size))
    last = max(0, total - size)
    start = max(0, min(int(start), last))
    if focus is not None:
        f = max(0, min(int(focus), max(0, total - 1)))
        start = min(start, f)                  # focus above the view: pull up
        start = max(start, f - size + 1)       # focus below the view: pull down
    return max(0, min(start, last))


def view_pos(start: int, size: int, total: int,
             cells: int) -> tuple[int, int]:
    """THE WINDOW MODEL, half two: THE VIEW AS CELLS — `(first cell, span)`.

    The seat `value_pos` cannot be. A magnitude is one number and answers
    with one position; a window is two and must answer with two, because the
    span IS the second number made visible — how much of the content you are
    looking at, read off the thumb's LENGTH. Widening `value_pos`'s return
    would have made every one of its six callers carry a span they have no
    use for, so this is a second seat rather than a wider one.

    IT DOES NOT INVENT AN ARITHMETIC, and that is the pass-43 discipline:
    only the SPAN is computed here, and the POSITION is delegated straight to
    `value_pos` on the shortened track the thumb leaves behind. So there is
    still exactly one place in this file that turns a number into a cell
    index, and a scroll bar's thumb sits where a slider's knob would.

    THE ENDS ARE EXACT, which is where a scroll bar is usually wrong: a
    window at `start=0` puts the thumb's first cell at 0, and a window at its
    LAST legal start puts the thumb's last cell at `cells - 1`. The track the
    position runs over is therefore `cells - span + 1` seats, not `cells` —
    the off-by-one that leaves a scroll bar unable to say "you are at the
    bottom" while the content says otherwise.

    A span of at least ONE cell (a thumb that vanishes is not a thumb) and at
    most `cells` (a window showing everything fills its track, which is the
    honest way to say "there is nothing to scroll")."""
    cells = max(1, int(cells))
    total, size = max(0, int(total)), max(1, int(size))
    if total <= size:
        return 0, cells
    span = max(1, min(cells, round(cells * size / total)))
    start = view_start(total, size, None, start)
    return value_pos(start, 0, total - size, cells - span + 1), span


def step_index(i: int, n: int, d: int, wrap: bool) -> int | None:
    """THE END MODEL — the seat a step lands on, or `None` when there is no
    such seat. The first thing in this contract whose question is what
    happens at the END of a range rather than what a range IS.

    WRAP VS CLAMP IS AN ARGUMENT, NOT A REGISTRY FACT, and the codebase
    settled it before this seat existed. A registry fact says something about
    EVERY instance of a component; this is not true of every stepper, it is
    true of every RING. The hours of a day wrap; a set of worker groups does
    not; both are steppers. And the app already holds both readings and
    chooses per call site by what the range MEANS — `action_cycle_theme` and
    `action_move` take `% n` because a list of languages and a column of rows
    are rings, and `action_pick` clamps because "an N-of-M control's ends are
    where the set ends". A `WRAPPING = ("stepper",)` tuple would be declaring
    a property of the CALLER'S DATA in the component's registry.

    CLAMP IS THE DEFAULT, and that is the safe reading rather than a taste: a
    caller who says nothing does not get their choice teleported from the
    last option to the first. The default lives at the two COMPOSING seats
    (`Kit.stepper`, `component_cells`) and NOT here, and that is the vacuity
    prover's finding rather than a preference: this argument had a default
    too, no caller ever reached it, and a value nothing can observe is the
    dead metadata this file has refused four times. The seat that DECIDES an
    end must always be told which end it is deciding.

    ONE SEAT FOR THE RENDER AND THE BEHAVIOUR, which is the whole reason this
    is a function and not two lines in a composer. The renderer asks it
    whether a step EXISTS (and draws ground where one does not); a caller
    asks it where the step GOES. So a stepper cannot draw a live arrow that
    does nothing — not "does not", cannot, by construction, which is the same
    discipline that keeps a switch from rendering CHECKED at the off
    position.

    IT CLAMPS `i` RATHER THAN RAISING, and the raise lives one level up. An
    out-of-range selection is a real defect and `group_states` is where it is
    refused, because that is where the CHOICE lives; this is arithmetic, and
    a renderer that died on a caller's number would take the surface with
    it."""
    n = int(n)
    if n < 1:
        raise ValueError("a stepper with no seats is not a stepper")
    i = max(0, min(n - 1, int(i)))
    j = i + int(d)
    if wrap:
        return j % n
    return j if 0 <= j < n else None


# ===========================================================================
# THE MOTION CONTRACT (tui-design/MOTION.md, and the SquareLine/LVGL corpus:
# 241 published animations, ZERO of which animate a COLOUR).
#
# A MOTION IS A LIST OF RENDER STATES — discrete frames — and not a style
# transition. That is the terminal's medium stated honestly: there is no
# sub-cell position, no fractional weight and no interpolation between two
# glyphs, so anything a spec claims to "ease between" is either quantised to
# whole cells or is not happening at all. What survives translation into this
# medium intact is DISCRETE SUBSTITUTION — one glyph replaced by another —
# which is why the channels are ordered the way they are below.
#
# TWO DISJOINT REGIMES, and the gap between them is ILLEGAL:
#
#   * TRANSITION — one-shot, a state leaving one rest and arriving at
#     another, `<= 400 ms`. (Corpus: median 300 ms, p90 600; the 400 ms
#     ceiling captures 68% of the published one-shots.) Easing biased to
#     DECELERATION — the corpus runs ease_out over ease_in 5:1 — and in a
#     medium with no interpolation deceleration is not a curve, it is WHERE
#     THE TIME IS SPENT: the change happens on the first step and the rest of
#     the budget is the settle. A transition with a dead lead-in is ease_in
#     wearing an ease_out's name, and the law says so.
#   * AMBIENT — looping, period `>= 2000 ms` (corpus median 3000: spinners,
#     breathing, a caret). A loop in the reading path with a shorter period
#     is a distraction with a 100% duty cycle (MOTION.md).
#
# The 400-2000 ms DEAD ZONE is illegal in both directions: a one-shot slower
# than 400 ms makes the user wait on the designer's taste, and a loop faster
# than 2000 ms twitches. A spec that lands there has not decided which regime
# it is in, and the suite refuses it rather than rounding it to the nearer
# one.
#
# THE CHANNELS — THERE ARE TWO, and the third one this comment used to list
# was pass 59's finding, kept here because the deletion IS the ruling:
#   1. GLYPH_FRAME  — discrete substitution. The only continuous-medium
#                     primitive that survives the translation intact.
#   2. CELL_POSITION— a mark at a different row/column. Quantised for free,
#                     because a cell is the only position there is.
#
# `DIM_LEVEL` WAS CHANNEL 3 AND IS NOT A CHANNEL IN THIS MEDIUM. A dim ladder
# has exactly two spellings and neither is its own: written in a 0-255 alpha
# it is a COLOUR animation, which the rule below forbids outright; written as
# a density ramp (`█▓▒░`) it is `glyph_frame` under another name — the same
# discrete substitution, drawn from a ramp that `coverage_to_glyph` now owns.
# Two channels, and the suite counts two.
#
# COLOUR IS NOT A CHANNEL. The corpus is unambiguous — 241 animations, zero
# animate colour — and it agrees with this contract's standing rule that a
# state may never ride colour alone. Read as a law over frames it says: TWO
# CONSECUTIVE FRAMES MUST DIFFER WITH THE COLOUR TAKEN AWAY. Tone may ride
# along (a frame drawn in ACTIVE carries ACTIVE's accent, and the switch's
# flip has done exactly that since pass 49) — what it may not do is BE the
# motion. And no frame builder may name a colour token to pick a frame,
# which is a source-level rule and is asserted as one.
# ===========================================================================
TRANSITION = "transition"
AMBIENT = "ambient"
TRANSITION_MAX_MS = 400                # the one-shot ceiling
AMBIENT_MIN_MS = 2000                  # the loop floor
AMBIENT_BEATS = 16                     # a loop is N beats of the language's
#                                        tempo, taken to the floor

# THE MEDIUM'S OWN FLOOR, and it is the only number here that is not a
# corpus statistic — it is the compositor's refresh period (Textual drives at
# 60 fps). A frame scheduled under it is not a fast frame, it is a frame the
# surface COALESCES: the language pays for it, declares it, and the user
# never sees it. Item #36, filed by the fifty-ninth pass, measured five such
# steps across the ten languages and cured none of them.
#
# IT IS A CEILING ON ELABORATION, NOT ON DURATION, and that split is the
# whole design. A language owns two things about time — its FRAMES
# (`MOTION_STEPS`) and its `tempo`. The frames are a CHOICE and the ceiling
# takes them back where the surface cannot draw them; the tempo is the
# language's own and is never touched. What is left over — a structure that
# is under the floor at ZERO elaboration, which only `travel` can be,
# because only travel's frame count is the DISTANCE's — cannot be trimmed
# and is not lied about either: the step is floored and the pass runs long.
REFRESH_MS = 1000 / 60

# THE REGIME IS A FACT ABOUT THE EVENT, NEVER ABOUT THE LANGUAGE. A press is
# one-shot because pressing is one-shot; a caret loops because a caret has
# nothing to arrive at. Ten languages may not disagree about that any more
# than they may disagree about how many parts a slider has — what a language
# owns is its FRAMES and its TEMPO, which is the same split the parts
# registry made between anatomy and expression.
MOTION_EVENTS = {
    "flip": TRANSITION,                # the switch's knob crossing its track
    "press": TRANSITION,               # the button's ACTIVE flash
    "travel": TRANSITION,              # a mark crossing between SIBLINGS
    "spin": TRANSITION,                # a stepper's option changing
    "blink": AMBIENT,                  # the caret — the first LOOP
}

# TRAVEL IS NOT A COMPONENT EVENT, and that is pass 51's finding arriving on
# the motion axis. The parts registry describes ONE component and has nothing
# to say about siblings, so "the mark moves from that well to this one" can no
# more be derived from `COMPONENT_PARTS["radio"]` than the exactly-one
# invariant could — it is a fact about a SET, and its seat is the group's.
MOTION_GROUP_EVENTS = ("travel",)


def motion_regime(event: str) -> str:
    """One seat, read by the engine and by the suite."""
    return MOTION_EVENTS[event]


def motion_events(name: str) -> tuple[str, ...]:
    """Which motions a COMPONENT can have, DERIVED from the parts registry —
    the same derivation discipline the state axis takes.

    A component that can be pressed has an ACTIVE state; a component whose
    mark crosses a track is the CHECKABLE one with an indicator; a component
    with a `step` part spins; a component with a `caret` blinks. No list, and
    nothing here reads a component's NAME."""
    parts = COMPONENT_PARTS[name]
    out = []
    if ACTIVE in component_states(name):
        out.append("press")
    if name in CHECKABLE and "indicator" in parts:
        out.append("flip")
    if "step" in parts:
        out.append("spin")
    if "caret" in parts:
        out.append("blink")
    return tuple(out)


class Motion(NamedTuple):
    """WHAT A MOTION IS: frames, a regime, and one step's duration.

    `frames[0]` IS THE RENDER THE MOTION LEAVES, and it is in the list so a
    law can measure a motion against its own starting point rather than
    against a picture the oracle drew. A player does not DRAW it for a
    transition — it is already on the glass, which is what makes the
    acknowledgement immediate (MOTION.md: animate the consequence, never the
    acknowledgement). An AMBIENT has no "already there": it cycles, so every
    frame including the first is drawn, and the period divides by the frame
    COUNT rather than by the gaps between them."""
    frames: tuple[str, ...]
    regime: str
    step_ms: float
    # WHAT THE LANGUAGE ACTUALLY GOT, after the refresh ceiling (#36). It is
    # `MOTION_STEPS` wherever the surface can draw that many and less where
    # it cannot, so it is the number every frame-count law must read: a law
    # written against the declared token asserts what the language ASKED
    # FOR, and the frames on the glass are what it was GIVEN.
    elaboration: int = 0

    @property
    def plays(self) -> tuple[str, ...]:
        return self.frames[1:] if self.regime == TRANSITION else self.frames

    @property
    def steps(self) -> int:
        return len(self.plays)

    @property
    def total_ms(self) -> float:
        """One pass for a transition; one PERIOD for an ambient."""
        return self.step_ms * self.steps

    @property
    def step_s(self) -> float:
        return self.step_ms / 1000


#: THE TRANSPARENT CELL. A cell of `chrome` carrying this character is a HOLE:
#: the compositor must leave whatever is already in that cell alone — it is
#: where the glass goes, and painting it would paint over the raster.
#:
#: U+E000 is the first Private Use Area codepoint, chosen for two reasons and
#: not for taste. It is one cell wide by rich's own width table (measured), so
#: punching it into a row cannot move the reserved rectangle. And no kit can
#: ever emit it: every glyph any language draws comes from a declared alphabet
#: (`LATTICE_GLYPHS`, the box constants, `RS.HALF`, the shade ramps), and none
#: of them reaches the PUA. A space would have been the obvious sentinel and is
#: the wrong one — swiss pads its gutter with real spaces and corgi's bars sit
#: next to them, so "space" cannot distinguish a hole from chrome that is blank
#: on purpose, which is exactly the distinction this character exists to carry.
RASTER_HOLE = "\ue000"


def _punch(row: str, x: int, w: int) -> str:
    """One markup row with cells `[x, x+w)` replaced by `RASTER_HOLE`.

    Measured on CELLS, never on characters — a markup row's `len()` counts its
    tags, and this module's rows are markup end to end (the pitfall `mark()`
    documents one level up). `Text` is used as the MEASURING INSTRUMENT here,
    which is the same role it already plays in this axis's tests ("the cells a
    markup row actually draws — measured through rich, not by `len()`").

    THE RE-EMISSION IS SAFE ON BOTH PARSERS, AND THAT WAS MEASURED RATHER THAN
    ASSUMED. This module's markup is read by TEXTUAL, and `mark()` records at
    length that rich and Textual disagree about escaping — so round-tripping a
    row through rich to slice it is exactly the move that had bitten this file
    before. Checked on 2026-09-04 over every row of every language at the
    sweep's own geometry (11 x 26 rows): `Content.from_markup` gives the same
    plain text and the same spans for the original row and for the re-emitted
    one, in every case. A row that ever failed that check would come back as a
    lost style or a swallowed `[/]`, which the region's cell-width assertion
    and the sweep's frames would both see."""
    t = Text.from_markup(row)
    head, _, tail = t.divide([x, x + w])
    return head.markup + RASTER_HOLE * w + tail.markup


class RenderResult(NamedTuple):
    """WHAT A SURFACE POSTURE PRODUCES — both sides of it, from one call.

    `rows` is the GLYPH side: exactly `reserved[1]` markup rows, each drawing
    exactly `reserved[0]` cells. It works on any terminal.

    `pixels` is the TRUE-RASTER side: the same posture applied to the actual
    pixels, ready for `textual_image`. `None` means the posture REFUSED —
    ledger and solari are not missing an implementation, they are exercising
    a commitment, and a caller that draws pixels anyway has overruled the
    language rather than rendered it.

    THE RECTANGLE IS RESERVED, NOT COMPOSITED (CEILINGS §7). `reserved` is
    the opaque cell rectangle the layout must give this region on BOTH paths.
    A raster region is drawn by the terminal, not by the compositor: the
    compositor knows the image's size and never its content, so z-order and
    scroll over it cannot be correct. Nothing may overlap it, and a posture
    that wanted to bleed under a card would be asking for a frame the
    compositor cannot make honest.

    `image_box` is `(col, row, w, h)` — WHERE INSIDE `rows` THE GLASS WENT.
    It exists because `rows` fuses the frame and the image into one rendering,
    and a consumer that draws the true raster then has nothing to draw the
    frame from: corgi's `[1] DISPLAY` box and blueprint's dimension spans are
    IN `rows` and are absent from `pixels` (recorded as F-4, found in the
    captures rather than in the code). `None` means the posture refused, and
    it is `None` rather than a zero-size rectangle on purpose — a refusing
    language has no place to put glass, which is not the same as having a
    place of no size.

    `chrome` is the frame ALONE: `rows` with the `image_box` cells replaced by
    `RASTER_HOLE`. It is DERIVED from `rows` and never the other way round,
    which is what keeps every frame this repo has already captured byte-
    identical — `rows` is still the whole rendering, and `chrome` is a view of
    it. For a refusing posture `chrome` IS `rows`, the same object: there is
    no glass to cut a hole for, so there is nothing to derive.

    `blob()` is what the mutation check (LANGUAGES.md's VERIFY rule) compares.
    It covers BOTH surfaces on purpose: a posture that changed the cells and
    left the pixels alone would pass a glyph-only comparison while breaking
    AC-3's "the same posture applied to the pixels". It deliberately does NOT
    cover `chrome`: `chrome` is a function of `rows` and `image_box`, so
    folding it in would make the mutation check compare the same bytes twice
    and report the redundancy as strength. The chrome limb is its own
    assertion in the test instead."""
    posture: str
    rows: list[str]
    pixels: object | None
    reserved: tuple[int, int]
    image_box: tuple[int, int, int, int] | None = None

    @property
    def chrome(self) -> list[str]:
        """The posture's frame, with a transparent hole where the glass goes.

        A compositor draws this, reserves `image_box`, and puts the raster
        widget in the hole — which is the whole of what F-4 asked for, and the
        reason it is a property rather than a fifth thing a mechanism has to
        remember to build: a mechanism that BUILT its chrome separately could
        build one that disagreed with its own `rows`, and nothing would catch
        it. Derived, they cannot drift."""
        if self.image_box is None:
            return self.rows
        x, y, w, h = self.image_box
        out = list(self.rows)
        for i in range(y, min(y + h, len(out))):
            out[i] = _punch(out[i], x, w)
        return out

    def blob(self) -> bytes:
        pix = self.pixels
        return b"\x00".join([
            self.posture.encode(),
            "\n".join(self.rows).encode(),
            b"" if pix is None else
            f"{pix.mode}{pix.size}".encode() + pix.tobytes()])

    def widget(self):
        """The true-raster widget, or None when there is no raster transport
        or the posture refused. Reuses `modals.py`'s path — one detection,
        made before Textual starts (see `raster.py`'s docstring)."""
        if self.pixels is None or not RS.raster_available():
            return None
        return RS.AutoImage(self.pixels)


class Kit:
    """Base kit = the `nord` language: deliberately the terminal's own
    conventional idiom (base16 doctrine: it inherits the environment and has
    no identity of its own). Every other language overrides mechanisms.

    Subclasses MUST route their mechanisms through the structural tokens they
    declare (`frame`, `numbered`, `dot_w`, `pitch`, `meter`) — a hardcoded
    mechanism makes its token dead metadata again.
    """

    def __init__(self, name: str):
        self.name = name
        self.t = THEMES[name]
        t = self.t
        self.c = {"ink": t["ink"], "mut": t["mut"], "dim": t["dim"],
                  "accent": t["accent"], "warn": t["warn"], "alert": t["alert"]}
        # board MOOD, set by the app each redraw ("clear" / "busy" / "alert");
        # languages with a functional identity element (naught's status face)
        # read it — identity must MEAN something, not float (user verdict)
        self.mood = "clear"

    # colour pass-through, so `kit["ink"]` works everywhere tokens did
    def __getitem__(self, key: str) -> str:
        return self.c[key]

    @property
    def frame(self) -> str:
        return self.t.get("frame", "none")

    @property
    def numbered(self) -> bool:
        return bool(self.t.get("numbered"))

    @property
    def pitch(self) -> int:
        return int(self.t.get("pitch", 1))

    @property
    def layout(self) -> str:
        """The board's INTERNAL structure device (the `layout` token):
        "flow" — cards stand on the ground, which is what every language did
        before this token existed — or "rail", a passive left rail that
        carries the card stack. Base default is "flow", so a language that
        never declares the token renders exactly as it always did."""
        return self.t.get("layout", "flow")

    @property
    def rail_width(self) -> int:
        """Cells the rail column takes OUT OF the content budget. Zero unless
        the language declares `layout="rail"` — a rail that widened the row
        instead of narrowing it would wrap it (VERIFY.md's frame law)."""
        return 0

    def rail_prefix(self) -> str:
        """The rail markup a board row is prefixed with. Empty by default."""
        return ""

    @property
    def rule_color(self) -> str:
        return self.c["dim"]

    @property
    def tick_tone(self) -> str:
        """The colour of a gauge's THRESHOLD tick. Base: the reserved WARN
        hue. A language that rations a semantic hue overrides it — ledger's
        red means debt, and a threshold is not a debt."""
        return self.c["warn"]

    @property
    def tempo_s(self) -> float:
        """Motion pace in seconds (the `tempo` token)."""
        return int(self.t.get("tempo", 140)) / 1000

    @property
    def easing(self) -> str:
        """Motion curve (the `easing` token): linear reads mechanical,
        out_expo reads like phosphor persistence, out_bounce is loud."""
        return self.t.get("easing", "out_cubic")

    def display_cap(self, s: str) -> str:
        """The hero caption's REGISTER — a language commitment, not a token:
        base = letterspaced caps (swiss/industrial's plain read); darkside
        overrides to quiet lowercase."""
        return " ".join(s.upper())

    def rule_line(self, w: int) -> str | None:
        """The language's structure device, driven by the `frame` token so a
        mutated token visibly changes EVERY surface that draws a divider."""
        ch = {"rule": "─", "single": "─", "grid": "─", "double": "═"}.get(self.frame)
        return None if ch is None else f"[{self.rule_color}]{ch * max(1, w - 1)}[/]"

    # -- structural css: what the language does to widget GEOMETRY ---------
    def tcss(self) -> str:
        """Per-language layout rules, appended to the theme stylesheet.
        Pitch is a real commitment: swiss spends rows the others spend on ink."""
        # THE SHARED ORIGIN, for every language. A `.kb-card` pays
        # `padding: 0 1`, so its row starts one cell in from the seat; the head
        # and the empty state pay the same cell here, and `kanban.py.row_width`
        # hands all three the same measure. Before this rule the head was
        # measured apart from its cards and six languages carried a private
        # compensation for the one-cell lie (PENDING item 4).
        rules = [".col-head { height: auto; padding-left: 1; }",
                 ".kb-empty { padding-left: 1; }"]
        if self.pitch > 1:
            rules.append(f".kb-card {{ margin-bottom: {self.pitch - 1}; }}")
        else:
            rules.append(".kb-card { margin-bottom: 0; }")
        # MOTION tokens drive the style-transition feel of every interactive
        # widget: hover/focus fades snap in industrial (60ms linear) and
        # decay in phosphor (400ms out_expo). Style motion is the cheap class.
        ms = int(self.t.get("tempo", 140))
        ease = self.easing
        rules.append(f".kb-card {{ transition: background {ms}ms {ease}; }}")
        rules.append(f".tile {{ transition: background {ms}ms {ease}; }}")
        rules.append(f"#hero {{ transition: background {ms * 2}ms {ease}; }}")
        return ("\n".join(rules) + "\n" + self.surface()
                + "\n" + self.composition())

    # -- COMPOSITION: the layout ITSELF as a language commitment ------------
    def composition(self) -> str:
        """The axis that keeps eight languages from feeling like one app in
        eight skins (COMPONENTS.md axis 6): Nothing composes a GRID of small
        widgets, Swiss one editorial column, TE numbered modules, a CRT lets
        the readout take the screen. Base (nord): the conventional dashboard
        skeleton — which is a composition, not an absence of one."""
        return ""

    # -- SURFACE: what the language does to the GROUND it draws on ----------
    def surface(self) -> str:
        """The texture/fill axis (COMPONENTS.md foundations). Flat ground is
        a decision some languages make (naught: pure black; swiss: emptiness)
        and others must NOT (bbs: solid panels; phosphor: scanlines) — a
        language that never touches its surface is one axis short of a look.
        Base (nord): cool panels behind the columns, the modern-app read."""
        t = self.t
        return (f".kb-col {{ background: {t['panel']}; }}\n"
                f".kb-card {{ background: {t['panel']}; }}")

    # -- board layout: a per-language commitment ---------------------------
    def board_layout(self) -> str:
        """"columns" (the kanban default) or "sections" — a flat vertical
        list of full-width phase sections. Squeezing 6 columns into a narrow
        composition made darkside's tasks illegible (~7 chars of title); its
        faithful form is the flat lowercase list."""
        return "columns"

    # -- column head --------------------------------------------------------
    def head(self, name: str, count: int, w: int, idx: int = 0) -> str:
        c = self.c
        num = f"[{c['accent']}]\\[{idx + 1}][/] " if self.numbered else ""
        room = w - (4 if self.numbered else 0)
        load = "" if count == 0 else RAMP[min(8, 1 + count // 3)]
        line = (num + f"[{c['mut']}]{name.upper()[:max(1, room - 4)]}[/] "
                f"[{c['accent'] if count else c['dim']}]{count}{load}[/]")
        rule = self.rule_line(w)
        return line if rule is None else line + "\n" + rule

    # -- one task card row --------------------------------------------------
    def card_row(self, title: str, chip: str, tone: str, w: int,
                 idx: int = 0, urgent: bool = False) -> str:
        c = self.c
        room = max(1, w - len(chip) - 2)
        body = _fit(title, room)
        pad = " " * max(0, room - min(len(title), room))
        return f"[{c['ink']}]{body}[/]{pad} [{tone}]{chip}[/]"

    # -- the card as a MINI-WIDGET: per-language anatomy --------------------
    def card_rows(self, title: str, chip: str, tone: str, w: int,
                  idx: int = 0, urgent: bool = False,
                  meta: dict | None = None) -> list[str]:
        """VARIETY lives here (user verdict: 'falta variedad'): the card is
        not one layout restyled eight times. Each language commits to its own
        anatomy — how many rows, WHICH fields it chooses to show, and with
        what mechanism. Swiss renounces the second row (space is structure);
        corgi prints a spec line; industrial labels everything; naught stays
        on the lattice. Base (nord): the terminal's two-line list convention
        — title row + dim metadata row (project · phase)."""
        top = self.card_row(title, chip, tone, w, idx, urgent)
        m = meta or {}
        c = self.c
        bits = [x for x in ((m.get("proj") or "")[:max(4, w - 16)],
                            m.get("phase", "")) if x]
        plain = ("  " + " · ".join(bits))[:max(1, w)]
        return [top, f"[{c['dim']}]{mark(plain) if bits else ' '}[/]"]

    # -- one signal tile row ------------------------------------------------
    def tile_row(self, val: str, label: str, tone: str, w: int) -> str:
        c = self.c
        room = w - len(val) - 1
        lab = c["dim"] if room < 6 else c["mut"]
        return f"[{tone}]{val}[/] [{lab}]{label[:max(0, room)]}[/]"

    # -- THE DEFINITION ROW: a caption and the value it names ---------------
    #
    # THE MOST REUSED SHAPE IN SIX SCREENS AND THE ONE WITH NO SEAT. The
    # PROTOTYPE round of 2026-09-04 rendered a detail pane, a KPI summary and
    # a settings readout in five languages, and every one of those rows was
    # drawn BY HAND -- with LEDGER'S mechanism, dot leaders, in four languages
    # that never chose it. One language's signature generalised into four is
    # the palette-swap failure with a leader instead of a hue, which is why
    # this is a SEAT and not a helper each caller writes once.
    #
    # WHAT IS THE CONTRACT'S AND WHAT IS THE LANGUAGE'S:
    #   * the VALUE is CONTENT -- byte for byte, never recased, never cut. It
    #     is the figure the row exists to report.
    #   * the CAPTION is a LABEL, and a label is NOTATION: a language that
    #     letters its legends in capitals letters this one too, exactly as
    #     `tile_row` already does. That asymmetry is the whole ruling, stated
    #     once here so that no language decides it twice.
    #   * the GAP is the MECHANISM, and it is nobody's default: air, leaders,
    #     a dimension, an ember frontier, an unlit lattice.
    #
    # `w` IS A MINIMUM FOR THE FIGURE -- the stepper's rule, for the stepper's
    # reason: a row that truncated its value to fit would be lying about the
    # number, and a caller who wants a narrower row can pass a shorter word.
    #
    # BASE (nord) IS THE TERMINAL'S OWN TWO-COLUMN LIST: the name at the left
    # margin, the figure flushed RIGHT, and AIR between them. No leader --
    # the terminal's convention is a COLUMN, and a column is found by
    # ALIGNMENT rather than followed by a line.
    def field_row(self, caption: str, value: str, w: int) -> str:
        c = self.c
        cap, val = str(caption), str(value)
        gap = max(1, w - len(cap) - len(val))
        return (f"[{c['mut']}]{mark(cap)}[/]" + " " * gap
                + f"[{c['ink']}]{mark(val)}[/]")

    # -- the progress meter (<= 2 rows) -------------------------------------
    def meter(self, done: int, total: int, counts: list[int], w: int) -> str:
        """Dispatched on the `meter` token, so the quantity MECHANISM is a
        swappable commitment (mutating the token swaps the mechanism)."""
        fn = METERS.get(self.t.get("meter", "blocks"), _meter_blocks)
        return fn(self, done, total, counts, w)

    # -- THE SURFACE POSTURE: what the language does with REAL PIXELS -------
    #
    # NAMING, SAID ONCE SO IT IS NOT A TRAP. There is already a `surface()`
    # method on this class and it is a different axis: that one returns TCSS
    # for the GROUND a language draws on (panels, hatch, flat black). The
    # `surface` TOKEN added 2026-09-03 is the raster posture, and it is read
    # here and nowhere else. The property below is called `posture` precisely
    # so no call site has to guess which `surface` it meant.
    @property
    def posture(self) -> str:
        """The `surface` token — the language's answer to "what happens when
        this region can be real pixels" (LANGUAGES.md's eighth axis)."""
        return self.t.get("surface", "untinted")

    def raster_region(self, img, w: int, h: int,
                      label: str = "") -> RenderResult:
        """Dispatched on the `surface` token, exactly as `meter` is dispatched
        on `meter` — mutating the token swaps the mechanism, which is what
        keeps a token alive rather than decorative.

        `img` is a `PIL.Image`; `w`/`h` are the CELLS the layout reserves.
        `label` is what the figure IS, for the postures that caption or audit
        one (swiss's caption, ledger's exhibit, corgi's display legend). It is
        optional because a posture that captions must still be able to render
        without being told — it falls back to the figure's own metrics, which
        is a caption a drawing office would accept and an empty string is
        not."""
        fn = SURFACES.get(self.posture, _surface_untinted)
        return fn(self, img, max(1, w), max(1, h), label)

    # -- per-language hooks the shared mechanisms call ----------------------
    # A mechanism two languages share is one function (AC-2: naught and
    # instrument share `lattice`, corgi and industrial share `display`), and
    # what differs between them is declared HERE, on the kit, rather than by
    # branching on the kit's name inside the mechanism.

    def lattice_grid(self, w: int, h: int) -> tuple[int, int]:
        """Dots the lattice fits in a w x h cell region. Base is the naught
        pitch: `dot_w` cells per dot plus `gap` cells of air, one dot row per
        cell row."""
        per = max(1, int(self.t.get("dot_w", 1)) + int(self.t.get("gap", 0)))
        return max(1, (w + int(self.t.get("gap", 0))) // per), max(1, h)

    def lattice_rows(self, bm, w: int, h: int) -> list[str]:
        """Draw a 0/1 sprite as this language's lattice, unlit grid visible.
        Base uses naught's own full-bleed field — the code that already draws
        its board, so the surface cannot fork the identity."""
        return NA.field(w, h, bm, self.c["ink"], self.c["dim"],
                        dot_w=int(self.t.get("dot_w", 1)),
                        gap=int(self.t.get("gap", 0)), ox=0)

    LATTICE_GLYPHS = frozenset(NA.ON + NA.OFF + " ")

    # (tl, tr, bl, br, top, bottom, left, right) — eight glyphs and not two,
    # because a language whose frame is a STAMPED PLATE has a different top
    # from its bottom (`▀` / `▄`) while a language whose frame is a drawn box
    # does not. Two glyphs would have forced industrial to borrow corgi's box.
    DISPLAY_BOX = "┌┐└┘──││"

    def display_chrome(self) -> tuple[str, str, str]:
        """(box glyphs, screen low colour, screen high colour) for the
        `display` posture. Base: box drawing, ground to ink."""
        return self.DISPLAY_BOX, self.t.get("ground", "#000000"), self.c["ink"]

    def display_label(self, idx: int = 1, label: str = "") -> str:
        """The label beside a display. `numbered` languages number it — the
        token decides, not the class.

        THE LEGEND IS THE CALLER'S AND THE NOTATION IS THE LANGUAGE'S (L-33,
        and SCOPE's F-1 which found it by shipping on it). §3b makes this
        language's numbering FUNCTIONAL — "in a TUI the numbers are the
        keybindings" — and a keybinding belongs to whoever owns the keymap,
        which is never the kit. Hardcoding `[1] DISPLAY` therefore spent a key
        on every consumer's behalf: SCOPE's `[1]` cycles its SOURCE, and the
        legend saying `DISPLAY` over it was that app's luck rather than this
        kit's doing.

        So the caller's `label` supplies BOTH pieces, separated the way a
        keymap is written. `label` is split once on whitespace: an ASCII run
        of digits in front is the BINDING, the rest is the WORD; anything else
        is a word only and the language keeps its own index. A `numbered`
        language letters `[binding] WORD`, one that is not letters `WORD` and
        DROPS the binding — a language with no notation for a keybinding must
        not grow one out of a caller's string, which is L-33's tie working
        rather than a case this forgot.

        `"7 SOURCE"` -> `[7] SOURCE`. `"mbb rho final"` -> `[1] MBB RHO
        FINAL`. No label at all -> `[1] DISPLAY`, byte-identical to before.

        THE KNOWN EDGE, recorded rather than defended against: a legend that
        legitimately opens with a number (`"2 PASS"` meaning two passes) is
        read as a binding. `"3D FIELD"` is safe — `"3D"` is not a run of
        digits — and the word is the caller's, so it can write `"PASS 2"`.

        `isascii()` guards `int()`: `"²".isdigit()` is True and `int("²")`
        raises, and this argument is caller text."""
        head, _, rest = str(label).strip().partition(" ")
        if head.isascii() and head.isdigit():
            idx, word = int(head), rest.strip()
        else:
            word = str(label).strip()
        word = word.upper() or "DISPLAY"
        return f"[{idx}] {word}" if self.numbered else word

    def readout_label(self, label: str = "") -> str:
        """THE NAME OF A PASSIVE READOUT — `display_label` WITH THE BINDING
        REFUSED, and the difference between the two seats is L-33 entire.

        Measured on a real app (emersio-lab, 2026-09-04) and quoted in
        LANGUAGES.md §3b: *"because the numbering IS the keymap, this language
        has no notation for a passive readout. A `[5]` over a chart nobody can
        act on is the decorative numbering §3b defines itself against.
        Readouts are LABELLED; controls are NUMBERED."*

        SO THE REGISTRY IS READ, and reading it is what makes the refusal a
        mechanism: a `numbered` language that is NOT in
        `READOUT_NUMBER_REFUSED` numbers its readout, which is the branch this
        table exists to keep empty. Take ledger out and it spends a key on a
        bar nobody can press — and a test goes red for exactly that reason.

        THE WORD IS THE CALLER'S AND THE REGISTER IS THE LANGUAGE'S, which is
        `display_label`'s ruling and this method is deliberately its twin: a
        readout's legend and a display's legend are the same object, so a
        contract that lettered them differently would be answering one
        question twice. A leading run of ASCII digits is a BINDING and is
        DROPPED here rather than lettered — the same tie `display_label`
        applies to a language with no numbering notation, applied to a
        COMPONENT with no numbering notation."""
        head, _, rest = str(label).strip().partition(" ")
        if head.isascii() and head.isdigit():
            idx, word = int(head), rest.strip()
        else:
            idx, word = None, str(label).strip()
        word = word.upper() or "READOUT"
        if self.numbered and self.name not in READOUT_NUMBER_REFUSED:
            word = f"[{idx if idx is not None else 1}] {word}"
        return f"[{self.c['mut']}]{mark(word)}[/]"

    def depth_ground(self) -> str:
        """The +1 grey STEP the `depth` posture separates on. Read off the
        language's own ladder (`focus`, the rung above `panel`) rather than
        invented as a delta: darkside already declares where its next grey
        step is, and a second ladder beside it would be two answers to one
        question. Only languages with no `focus` fall back to arithmetic."""
        panel = self.t.get("panel", self.t.get("ground", "#000000"))
        return self.t.get("focus") or RS.step(panel, 14)

    def caption(self, img, label: str) -> str:
        """What a captioning posture writes under its figure. The metrics are
        the fallback because a caption is not optional — a figure with no
        caption is a poster, and swiss's posture is explicitly not that."""
        return label or f"{img.size[0]}x{img.size[1]} px"

    def tint_pair(self) -> tuple[str, str]:
        """(low, high) of the `tint` posture's duotone ramp. Base: the
        language's own ground and ink, which is what "one hue" means when the
        language has not named a second one."""
        return self.t.get("ground", "#000000"), self.c["ink"]

    def exhibit(self, img, w: int, h: int, label: str = "") -> list[str]:
        """What a REFUSING language shows instead of the image.

        Base is NOTHING but ground, and that is solari's answer in full: "one
        shape, the row; an image cannot flip. If a board needs a picture it is
        not a departure board." A blank rectangle is the render of that
        sentence, so solari overrides nothing. Ledger overrides with its ruled
        exhibit."""
        return [" " * w for _ in range(h)]

    # -- a view section header (AGENDA / GANTT / SWIMLANES) -----------------
    def sect(self, title: str, note: str, w: int, h: int = 0) -> list[str]:
        """`h` is the surface's ROW BUDGET. Display typography (axis 3) is a
        luxury a surface must afford: languages that draw their titles
        (naught dots, bbs block letters, instrument braille) do so only when
        h pays for it, and fall back to type when it doesn't. Languages that
        RENOUNCE drawn type (swiss, corgi, industrial, phosphor, nord — they
        print, letterspace or label) ignore h: renouncing is a decision.
        Base (nord): the terminal's typographic convention."""
        c = self.c
        return [f"[{c['accent']}]{title}[/]  [{c['mut']}]{note}[/]", ""]

    # -- quantity bar for agenda buckets / lanes ----------------------------
    def bar(self, span: int, head=None, tone: str | None = None) -> str:
        """`head` is the travelling-packet mask (or None when the bar is
        static). The LENGTH is data; only the packet animates."""
        tone = tone or self.c["accent"]
        body = "".join("█" if (head is None or head[i]) else "▓"
                       for i in range(span))
        return f"[{tone}]{body}[/]"

    # -- gantt glyphs: (bar-fill, packet, axis-week, axis-day, due-marker) --
    GANTT = ("▬", "█", "│", "·", "◆")

    # -- calendar day cell (2 cells wide) -----------------------------------
    def cal_cell(self, state: str) -> str:
        c = self.c
        return {"none": f"[{c['dim']}]░░[/]",
                "over": f"[{c['alert']}]██[/]",
                "multi": f"[{c['accent']}]██[/]",
                "one": f"[{c['warn']}]▓▓[/]"}[state]

    # -- queue "UP NEXT" row marker ----------------------------------------
    def queue_marker(self, i: int) -> str:
        c = self.c
        return (f"[{c['accent']}]\\[{i + 1}][/]" if self.numbered
                else f"[{c['dim']}]·[/]")

    # ======================================================================
    # THE COMPONENT LIBRARY (tui-design/COMPONENTS.md). A language whose
    # CONTROLS render identically is still a recolour — these are the parts
    # the user touches. Base = the terminal's own conventions (nord).
    # Anatomy is shared (track / fill / knob / state); mechanism is the
    # language's. Every state must survive greyscale (glyph + colour).
    # ======================================================================
    CUR = "▸"                              # selection cursor

    # THE DISCLOSURE MARK — one cell (or two, in a language that doubles),
    # and it is the whole difference between a value and a WAY IN. A stepper
    # shows the two ways OFF a value; a select shows the one way INTO a list,
    # and the mark that says so is the language's.
    DISCLOSE = "▾"

    # THE DANGER FORM — a pair of marks that bracket the label INSIDE the
    # walls, and never a hue (operator ruling 6). Severity on a control is
    # new to this contract, and the hue was unavailable before it was
    # considered: ledger spends `alert` on literal debt and blueprint on
    # overdue, so a destructive button borrowing it would break the one thing
    # that makes an overdue row legible. The form is therefore the WHOLE
    # channel, which is also what makes it survive greyscale by construction
    # rather than by review.
    #
    # AND IT IS THE ROOT PROMPT, NOT THE SHOUT (inc45). This read `("!", "!")`
    # under "the terminal's own shout", and `!` is also `LEVELS["warn"]` and
    # half of `LEVELS["error"]` — so `[ !Delete all! ]` and a warning row said
    # the same thing with the same cell. `nord_S3`'s objection is verbatim:
    # "decir si `!Delete all!` es «peligroso» o «hay una advertencia sobre
    # esto»" — two correct answers, no cue. The ladder keeps `!` (ruling 8:
    # one width, three shapes, `· ` / `! ` / `!!` counted), because a shout IS
    # what a severity rung is, and the danger form takes the OTHER thing the
    # environment already writes: `#`, the root prompt — the terminal's own
    # mark for the account that can destroy. Nord is the one language whose
    # commitment is to inherit the environment rather than to invent, so its
    # destructive form has to be something the environment already means.
    DANGER_FORM = ("#", "#")               # the root prompt, `$` made `#`
    SPIN = ("▖", "▘", "▝", "▗")            # quadrant spin — matches nord's base

    # ------------------------------------------------------------------
    # THE VALUE FAMILY — slider, bar and switch, from the parts registry.
    #
    # A language declares GLYPHS (`PART_GLYPHS`), a slot separator and
    # optional chrome; the composition, the value model and the state axis
    # are shared. That is the contract: which parts exist is not a language's
    # decision, how they are drawn is nothing else.
    #
    # NAME COLLISION, said out loud: `Kit.bar()` was already taken by the
    # agenda/gantt/lanes quantity SPAN (a run of `span` cells, no value, no
    # scale), which has ten overrides and two view call sites. The registry
    # keeps LVGL's name `bar`; the method that draws it is `readbar()`. One
    # object, two names, and this comment is the only place that hurts.
    # ------------------------------------------------------------------
    SLOT_SEP = ""                          # air between slots
    COMP_CHROME = ("", "")                 # fixed open/close, NOT parts
    PART_GLYPHS = {
        "main": {DEFAULT: "─", DISABLED: "╌"},
        "indicator": {DEFAULT: "█", DISABLED: "▒"},
        "knob": {DEFAULT: "▌", FOCUSED: "▐", EDITED: "◆",
                 ACTIVE: "▓", INVALID: "▚",
                 DISABLED: "╳"},
        # A COMPONENT-SCOPED SEAT: `component.part` wins over the bare
        # `part`. The checkbox needs one because its parts are a BOX and a
        # MARK, not a track and a grip — drawing a box with the slider's `─`
        # would be a picture of a slider. The scope is additive: a component
        # that declares nothing here still draws through the shared parts,
        # which is why nothing in the value family moved.
        #
        # nord is the terminal's own idiom, so its checkbox is the one every
        # terminal already writes: `[ ]` / `[x]`. The BOX carries the control
        # state (bracket weight, nord's own knob vocabulary) and the MARK
        # carries the checked bit — two channels, neither of them colour.
        "checkbox.main": {DEFAULT: "[ ]", FOCUSED: "▐ ▌", ACTIVE: "▓ ▓",
                          DISABLED: "╌ ╌"},
        "checkbox.knob": {DEFAULT: "[x]", FOCUSED: "▐x▌", ACTIVE: "▓x▓",
                          DISABLED: "╌╳╌"},
        # THE RADIO WELL IS ROUND WHERE THE CHECKBOX IS SQUARE — LVGL's own
        # distinction, and the terminal already writes it: `[x]` is a box you
        # tick, `(o)` is one of a set. nord inherits the environment, so it
        # inherits the convention too. The control state rides the bracket
        # weight exactly as it does on the checkbox; what changes is the
        # FAMILY, which is the channel a greyscale eye reads.
        "radio.main": {DEFAULT: "( )", FOCUSED: "< >", ACTIVE: "« »",
                       DISABLED: "(╌)"},
        "radio.knob": {DEFAULT: "(o)", FOCUSED: "<o>", ACTIVE: "«●»",
                       DISABLED: "(╳)"},
        # THE BUTTON'S WALLS — ONE part, ONE slot, and the glyph is BOTH
        # sides of the control: it is split in half and the label stands
        # between them. An even width, so the halves are halves; one width
        # across all four states, so the field cannot move under the word.
        #
        # nord inherits the terminal's own button, `[ Save ]`, and puts the
        # state where its checkbox puts it: the bracket's weight. The PRESS
        # eats the air — `▓▓Save▓▓` — which is a shape event on the two cells
        # that touch the label, and the closest a text cell comes to the
        # inversion a real button flashes.
        "button.main": {DEFAULT: "[  ]", FOCUSED: "▐  ▌", ACTIVE: "▓▓▓▓",
                        DISABLED: "╌  ╌"},
        # THE FIELD'S GROUND — an ODD string: wall, RUNE, wall. nord inherits
        # the terminal's own input, `[ ... ]`, and puts the state where its
        # button puts it: the bracket's weight. EDITED additionally lays a
        # RULED LINE under the paper, so the state a caret lives in is
        # readable even in the instant between two keystrokes.
        #
        # INVALID IS THE SHOUT, NOT THE BRACKET TURNED ROUND (inc39). This
        # entry read `] [`: the terminal's own input with its two walls
        # EXCHANGED, so "this value was rejected" was spelled by the ORDER
        # of two brackets and by nothing else. That is not a terminal
        # convention of any kind -- it reads as a broken render rather than
        # as a state -- and it is the BASE's defect, not nord's: nord
        # declares no `PART_GLYPHS` of its own, so this line is the whole of
        # its answer, and the inheritors round read it off `nord_S2`.
        #
        # Un-flipping alone would give `[ ]`, which is DEFAULT byte for
        # byte, so the walls took `DANGER_FORM` -- the terminal's own shout,
        # the same seat swiss and darkside already spend theirs on.  The
        # paper stays blank, as DEFAULT's is.
        #
        # AND THE REJECTION GETS ITS OWN MARK (inc45). inc39 reached for
        # `DANGER_FORM` because un-flipping alone collided with DEFAULT, not
        # because destruction and rejection are one claim -- and once the
        # danger form stopped being `!` (above) that borrowing would only have
        # moved the overload: `#` would then be "this deletes" AND "this was
        # refused". So the walls take the environment's own mark for a value
        # it cannot read, `?`, which is not spent anywhere else in this kit.
        # inc39's law still holds by construction: the same mark opens and
        # closes, so there is no handedness to read a state off.
        "textfield.main": {DEFAULT: "[ ]", FOCUSED: "▐ ▌", EDITED: "▐▁▌",
                           ACTIVE: "▓ ▓", INVALID: "? ?",
                           DISABLED: "╌╌╌"},
        # the terminal's own bar cursor, in its own column
        "textfield.caret": {DEFAULT: "▏"},
        # THE SHAFT AND THE THUMB, and they are SCOPED for a reason that is
        # not decoration: a slider's track is a SCALE (every cell is a value
        # the knob could take) and a scroll bar's track is a SHAFT (every
        # cell is somewhere the view could be). They are drawn side by side
        # in the gallery, and a language that drew them identically would be
        # claiming the two mean the same thing. TWO STATES ONLY, because a
        # readout has two — the table cannot declare a FOCUSED shaft even by
        # accident, since the composer would never ask for one.
        #
        # nord inherits the environment, so it inherits Textual's own
        # scrollbar vocabulary: a shaded shaft with a solid block riding it.
        "scrollbar.main": {DEFAULT: "░", DISABLED: "╌"},
        "scrollbar.indicator": {DEFAULT: "█", DISABLED: "▒"},
        # THE TWO STEPS AS ONE EVEN STRING — the button's walls convention,
        # read for direction instead of for sides: the first half is the step
        # BACK and the second half is the step FORWARD. One declaration, two
        # cells, and the cell's POSITION is what says which way it goes.
        #
        # `stepper.main` IS THE GROUND WHERE A STEP IS NOT, and it is the
        # whole end-behaviour channel: a clamped stepper at its floor draws
        # this string's left half instead of the step's, so WRAP and CLAMP
        # differ in SHAPE and a greyscale eye can tell a floor from a middle.
        # The two strings are the SAME WIDTH in every state, which is what
        # keeps the word from moving when an end dies (Bodmer T2: reserve the
        # widest form).
        #
        # nord inherits the environment, so it takes the terminal's own spin
        # marks and puts the state where its other controls put it: the
        # weight of the mark under the finger.
        "stepper.main": {DEFAULT: "··", DISABLED: "╌╌"},
        "stepper.step": {DEFAULT: "-+", FOCUSED: "◂▸", EDITED: "◄►",
                         ACTIVE: "◀▶", INVALID: "][",
                         DISABLED: "╳╳"},
    }

    def part_key(self, name: str | None, part: str) -> str:
        """The glyph table a part is drawn from, scoped to its component.

        One lookup, and the fallback is deliberate: a language that declares
        no `checkbox.knob` still renders SOMETHING (its slider's grip) rather
        than raising. The suite is what says that is wrong — a law, not a
        crash, because a crash in a renderer takes the whole surface with it
        and a mutation that kills the suite reports no reds at all."""
        scoped = f"{name}.{part}"
        return scoped if scoped in self.PART_GLYPHS else part

    def comp_chrome(self, name: str) -> tuple[str, str]:
        """Chrome fixes THE ENDS OF A TRACK — industrial's brackets round its
        slider, blueprint's datum terminator opening its dimension. A
        component with no indicator has no track, so it has no ends to fix;
        where such a component has a box, the box is inside its own glyphs.
        Same registry fact as the composer reads, one seat."""
        return self.COMP_CHROME if "indicator" in COMPONENT_PARTS[name] \
            else ("", "")

    def part_glyph(self, part: str, state: str, name: str | None = None) -> str:
        """The slot this language draws for `part` in `state`. Falls back
        along the state's BITS — exact combination, then its control bit,
        then CHECKED, then DEFAULT — so a language declares only the states
        it wants to speak about and a combination behaves like the control
        state it carries.

        No language declares a CHECKED glyph and none needs to: on a switch
        the checked bit is carried by the knob's POSITION, which the shared
        value model moves for free. Shape, in all ten, for nothing."""
        table = self.PART_GLYPHS[self.part_key(name, part)]
        for key in state_chain(state):
            if key in table:
                return table[key]
        return table[DEFAULT]

    def part_tone(self, part: str, state: str, name: str | None = None) -> str:
        """Colour is the SECOND channel and never the only one. The accent is
        spent on the part under the finger — everything passive is grey, which
        is naught's ration and darkside's law at the same time.

        THE PART UNDER THE FINGER IS THE ACTUATOR, not literally the knob.
        This rule said `knob` for four passes because every control had one;
        the button's grip is its own ground, so a focused button would have
        rendered entirely dim — the accent law's letter kept and its meaning
        lost. One word changed, at the seat, and every other component's tones
        are byte-identical (the shipped accent laws are the proof)."""
        c = self.c
        state = control_of(state)
        if state == DISABLED:
            return c["dim"]
        if part == "indicator":
            return c["mut"]
        if part != actuator(name):
            return c["dim"]
        return c["accent"] if state in (FOCUSED, EDITED, ACTIVE) else c["ink"]

    def part_slots(self, name: str, w: int) -> int:
        """How many slots fit in `w` cells. Read by the render AND by the
        acceptance check, so "the parts tile the region" is true by
        construction rather than re-derived in the oracle.

        A component with NO INDICATOR gets exactly ONE slot, and the width
        request dies at that boundary. Cells are what an EXTENT spends; a
        mark needs a seat, not a run. Two slots would be two boxes, and a
        wide box would be a track wearing a checkbox's name — the same
        confusion the parts registry exists to make impossible.

        A component with a CARET is the opposite case and gets exactly `w`:
        its cells are COLUMNS OF TEXT, one character each, and `w` is how
        many of them the caller has room for. That is not an extent's budget
        (cells a value may spend) but a WINDOW (cells the value is seen
        through), and it is the first time this contract has had one.

        A component with a STEP gets exactly TWO, and `w` dies at that
        boundary the way it dies at a checkbox's: the two seats are the two
        DIRECTIONS, and there is no third way out of a range. A stepper's `w`
        is a minimum for the WORD it shows, which is the caller's and is
        measured where the caller's text is measured, not here."""
        if "caret" in COMPONENT_PARTS[name]:
            return max(1, int(w))
        if "step" in COMPONENT_PARTS[name]:
            return 2
        if "indicator" not in COMPONENT_PARTS[name]:
            return 1
        sw = len(self.part_glyph("main", DEFAULT, name))
        sep = len(self.SLOT_SEP)
        o, cl = self.comp_chrome(name)
        room = max(0, w - len(o) - len(cl))
        return max(2, (room + sep) // (sw + sep))

    def field_form(self, state: str, name: str) -> tuple[str, str, str]:
        """A FIELD'S GROUND, as one glyph string read at three seats: the wall
        that opens it, the RUNE its paper is made of, and the wall that closes
        it. An ODD length, so the two walls are halves of what is left when
        the rune is taken out of the middle — the same "the walls are halves"
        convention the button states as an EVEN length, said for a component
        that has an interior between them.

        One string rather than three declarations because it is one decision:
        a language does not choose its walls and its paper separately, it
        chooses the ground it lays under someone else's words."""
        g = self.part_glyph("main", state, name)
        h = len(g) // 2
        return g[:h], g[h], g[h + 1:]

    def component_cells(self, name: str, val: float, lo: float, hi: float,
                        w: int = 10, state: str = DEFAULT,
                        wrap: bool = False,
                        caret: int | None = None,
                        size: int | None = None
                        ) -> list[tuple[str, str, str]]:
        """THE ONE RENDERER: `[(part, glyph, tone)]`, one entry per slot.

        Returning cells TAGGED with their part is what lets the acceptance
        check read a part's extent off the render itself instead of
        recomputing the width arithmetic in the oracle — the duplicated-render
        defect that cost pass 46 a hundred and fifty-eight false mismatches.

        Bodmer T4: the whole region is composed here, including its own
        ground, and written once. Nothing clears and redraws.

        `caret` IS A SECOND PIECE OF STATE, and it is the first one this
        renderer has needed. A slider is one number; a field is a value AND
        an insertion index, and the index is not derivable from the value —
        two identical strings can be under edit at two different places. So
        it arrives as its own argument rather than riding `val`, which is
        also what keeps `has_value` honest: the registry holds no number for
        a text field, because a text field's value is CONTENT.

        `size` IS THE SECOND HALF OF A WINDOW, and it arrives the same way
        and for the same reason: the caret's precedent, applied to the other
        component whose value will not fit in one number. `val` carries where
        the view starts and `hi` carries how long the content is; `size`
        carries how much of it is on screen. A window has no `lo` to choose —
        content starts where it starts and there is no scrolling above the
        top — so the scale is `[0, hi]` and that is stated, not smuggled.

        Omitted, it means THE WHOLE CONTENT IS VISIBLE (a full thumb), which
        is the honest reading of "nobody said" rather than an exception: a
        renderer that raised on a missing number would take the surface down
        with it.

        `wrap` IS A RANGE WORD, NOT A THIRD PIECE OF STATE, and the fifty-
        fourth pass's warning is answered by that distinction rather than by
        ignoring it. `caret` and `size` default to `None` because they are
        STATE the caller may or may not have — where the pen is, how much is
        in view — and a third of those would mean restructuring. `wrap`
        defaults to `False` because it is a fact about the SCALE, standing
        beside `lo` and `hi`: whether the range closes on itself. It says
        nothing about where the value is, and the suite asserts exactly that
        boundary off `inspect.signature` — the optional STATE arguments are
        still the two the text field and the scroll bar bought."""
        if state not in COMPONENT_STATES[name]:
            state = DEFAULT
        if val is None or not has_value(name):
            # A boolean control has no value independent of its checked bit,
            # so `val=None` means READ IT OFF THE STATE. That is the only way
            # `switch()` calls this, and it is why a switch can never render
            # CHECKED with its knob at the off position: there is one source.
            # Motion passes an explicit fraction instead (`flip_frames`),
            # because a frame mid-travel is a FRAME and not a state.
            #
            # NOT guarded by `name in CHECKABLE`, and the mutation table is
            # why: with the guard, taking `switch` out of CHECKABLE made this
            # raise TypeError and KILLED the suite on its first render, so a
            # dead run reported no reds at all. Substituting unconditionally
            # makes that mutation draw a WRONG switch instead of no switch,
            # and the greyscale laws then say so a hundred times over.
            #
            # AND A COMPONENT WITH NO VALUE CANNOT BE HANDED ONE. `has_value`
            # is a registry fact, so a caller passing a number to a button
            # does not move anything: there is no part for a value to reach.
            # The suite drives exactly that, because without this term the
            # value would pick a PRESENCE and the button would grow a mark it
            # never declared.
            val, lo, hi = bool_value(state), 0, 1
        parts = COMPONENT_PARTS[name]
        cells = self.part_slots(name, w)
        out = []
        if "caret" in parts:
            # A WINDOW: the cells are COLUMNS, and the mark is at an INDEX
            # the caller hands in — not a position computed from a value.
            # This is the third anatomy, and the registry is what forks it,
            # exactly as it forks the other two.
            #
            # The mark's glyph is its own; a column with no mark on it is
            # `main` and wears the FORM'S RUNE rather than the whole form,
            # because `main` here is a ground that repeats and the walls are
            # the same string's ends (`field_form`). One part, read twice.
            _, rune, _ = self.field_form(state, name)
            return [("caret", self.part_glyph("caret", state, name),
                     self.part_tone("caret", state, name))
                    if caret is not None and i == int(caret)
                    else ("main", rune, self.part_tone("main", state, name))
                    for i in range(cells)]
        if "step" in parts:
            # A SERIES OF SEATS — the FIFTH anatomy, and the registry forks
            # it the way it forks the other four. Nothing is measured and
            # nothing is indexed: the value picks a SEAT, and what the
            # language draws is the two ways OUT of that seat.
            #
            # THE END BEHAVIOUR IS THE PART TAG. `step_index` is asked
            # whether the step exists, and a seat with no step is GROUND —
            # `main`, the word this registry uses for exactly that everywhere
            # else. So a clamped stepper at its floor draws ground where its
            # step was, a wrapping one never does, and the difference is a
            # GLYPH before it is anything else. No new state, no per-cell
            # state, and no colour.
            #
            # ONE GLYPH STRING, TWO HALVES, and the halves are the two
            # DIRECTIONS — the button's walls convention read for direction
            # instead of for sides. Which half a cell draws is its POSITION,
            # which is the one thing a part tag cannot say and does not have
            # to: there are exactly two seats and no third way out of a
            # range.
            i, n = int(val) - int(lo), int(hi) - int(lo) + 1
            out = []
            for slot, d in ((0, -1), (1, 1)):
                p = "main" if step_index(i, n, d, wrap) is None else "step"
                g = self.part_glyph(p, state, name)
                h = len(g) // 2
                out.append((p, g[:h] if slot == 0 else g[h:],
                            self.part_tone(p, state, name)))
            return out
        if name in VIEWED:
            # A WINDOW ON A TRACK — the FOURTH anatomy, and the registry is
            # what forks it, exactly as it forks the other three. The parts
            # are an extent's parts and the mechanism is not an extent's: the
            # run is anchored NOWHERE (it floats to where the view is) and
            # its LENGTH is the second number, not a repeat of the first.
            #
            # `view_pos` answers both at once because both are the value.
            # Read the branch above it to see the difference stated in code:
            # there, one number picks a position and the run is everything
            # behind it; here, two numbers pick a run and there is ground on
            # BOTH sides of it.
            pos, span = view_pos(val, hi if size is None else size, hi, cells)
            out = ["indicator" if pos <= i < pos + span else "main"
                   for i in range(cells)]
        elif "indicator" in parts:
            # AN EXTENT: the value picks a POSITION, the cells behind it are
            # the measured run, the cells ahead of it are the ground.
            n = value_pos(val, lo, hi, cells)
            knob = "knob" in parts
            for i in range(cells):
                if knob and i == n:
                    out.append("knob")
                elif i < n or (not knob and i == n):
                    out.append("indicator")
                else:
                    out.append("main")
        else:
            # NO EXTENT: nothing runs between an origin and the mark, so the
            # value cannot pick a position — it picks PRESENCE. The same
            # shared value model answers it (top of the range or not), so an
            # inverted scale still inverts and no second arithmetic is born.
            #
            # This branch reads the REGISTRY, not the component's name, which
            # is the difference between the contract growing an anatomy and
            # the composer growing a special case. `checkbox` appears nowhere
            # in it, and the source-level law in the suite says so.
            marked = value_pos(val, lo, hi, 2) == 1
            out = ["knob" if marked and i == 0 else "main"
                   for i in range(cells)]
        return [(p, self.part_glyph(p, state, name),
                 self.part_tone(p, state, name)) for p in out]

    def value_label(self, val, state: str = DEFAULT) -> str:
        """The readout. NOT a part — LVGL's slider has three parts and none of
        them is a number; this is a label standing beside the component, which
        is why the mechanism-invariance law is measured on the cells alone."""
        return f" [{self.c['mut']}]{val}[/]"

    CHECK_WORDS: tuple[str, str] | None = None      # (off, on) printed word

    def check_label(self, on: bool, state: str = DEFAULT) -> str:
        """`value_label`'s boolean seat — the switch's printed WORD.

        Not a part, for the same reason a slider's number is not: it stands
        BESIDE the component. Four languages were already using this seat
        when they shipped `ON`, `--`, `posted` and `OFF` inside their switch
        strings; here it is declared instead of drawn, and the base spends
        nothing, because position already carries the reading."""
        if not self.CHECK_WORDS:
            return ""
        return (f" [{self.check_tone(on, state)}]"
                f"{mark(self.CHECK_WORDS[1 if on else 0])}[/]")

    def check_tone(self, on: bool, state: str) -> str:
        """The tone of a control's WORD — lit when set, muted when not, dim
        when dead. One seat because the components print a word here for
        different reasons: the switch and the checkbox print the language's
        own on/off word, a radio item prints the OPTION'S name, and a button
        prints the caller's name for its action, which is why it asks with
        `on=True` — a button's word is not a state, it is always there. Same
        rule, different text, and the third caller needed no new branch."""
        c = self.c
        return (c["dim"] if control_of(state) == DISABLED
                else c["ink"] if on else c["mut"])

    def _component_body(self, name: str, val, lo, hi, w: int,
                        state: str, size: int | None = None) -> str:
        """The control ITSELF — cells, separators and chrome, no label.

        Split out from `_component` because the label is the one thing a
        radio item cannot inherit: the word beside it is the option's, so
        `check_label` would print `ON` next to `fast`."""
        cells = self.component_cells(name, val, lo, hi, w, state, size=size)
        sep = mark(self.SLOT_SEP)
        body = sep.join(f"[{t}]{mark(g)}[/]" for _, g, t in cells)
        o, cl = self.comp_chrome(name)
        d = self.c["dim"]
        if o:
            body = f"[{d}]{mark(o)}[/]" + body
        if cl:
            body += f"[{d}]{mark(cl)}[/]"
        return body

    def _component(self, name: str, val, lo, hi, w: int, state: str,
                   size: int | None = None) -> str:
        if val is None:                    # the label reads the same value
            val, lo, hi = bool_value(state), 0, 1
        body = self._component_body(name, val, lo, hi, w, state, size)
        if name in VIEWED:
            # NO READOUT, AND IT IS THE ARITY AGAIN — the same fact showing
            # up at the second seat. `value_label` prints ONE number, and a
            # window is two: printing one of them would name the position and
            # hide the size, or name the size and hide the position. There is
            # nothing to append that would not be a half-truth, and the thumb
            # is already saying both at once — this is the first component
            # whose value IS its own readout.
            return body
        if name in CHECKABLE:
            return body + self.check_label(is_checked(state), state)
        return body + self.value_label(val, state)

    def slider(self, val: int, lo: int, hi: int, w: int = 10,
               state: str = DEFAULT) -> str:
        """main + indicator + knob. The knob is the affordance of control."""
        return self._component("slider", val, lo, hi, w, state)

    def readbar(self, val: int, lo: int, hi: int, w: int = 10,
                state: str = DEFAULT) -> str:
        """main + indicator. A slider with the knob taken away is a readout —
        that ONE missing part is the whole difference between operating a
        value and being told one."""
        return self._component("bar", val, lo, hi, w, state)

    def scrollbar(self, start: int, size: int, total: int, w: int = 12,
                  state: str = DEFAULT) -> str:
        """main + indicator, on a value that is a WINDOW — the readout whose
        indicator has a POSITION as well as an extent, which is the first
        time in this contract that either of those has been true.

        THREE NUMBERS IN, TWO OUT. `start` and `size` are the value; `total`
        is its scale, the way `hi` is a slider's. There is no `lo`, and its
        absence is the anatomy: content begins where it begins.

        NO STATE ARGUMENT WORTH FOUR VALUES — the registry gives this
        component DEFAULT and DISABLED and nothing else, because it has no
        grip. In a keyboard TUI the keys scroll the CONTAINER and the bar
        reports where the container got to; nothing here is ever grabbed. A
        FOCUSED scroll bar would be advertising an affordance the app does
        not have, which is the exact defect the bar's missing knob was the
        first cure for.

        AND IT DRAWS ALONG A ROW BECAUSE THE CALLER LAYS IT OUT. What this
        composes is a LIST OF CELLS; which axis they are stacked on is not a
        fact the language owns, any more than `bar` owns one. A vertical
        scroll bar is the same cells down a column. If a language ever wants
        a DIFFERENT glyph vertically it needs an axis fact in the registry
        and none has asked for one — see PENDING, priced rather than built.

        NOT A REPLACEMENT FOR TEXTUAL'S OWN CHROME, said out loud. The
        surfaces that really scroll here (the gallery box) are Textual
        containers that draw and drag their own scrollbars; overriding those
        means fighting the framework's widget, and the only channel a
        language could honestly take from them in TCSS is COLOUR, which is
        the one channel this contract forbids a state to ride alone. So this
        component is GALLERY-ONLY, exactly as the text field is, and for a
        reason that is stated rather than hidden behind a demo."""
        return self._component("scrollbar", int(start), 0, int(total), w,
                               state, size=int(size))

    def switch(self, on: bool, w: int = 3, state: str = DEFAULT) -> str:
        """main + indicator + knob, on a range of exactly two positions.

        The checked bit is written HERE and read by the composer, so `on` and
        `state` cannot disagree: pass `state=FOCUSED` and you get
        `checked+focused` or `focused`, never a checked switch pointing off.

        Ten languages used to carry ten hand-drawn switches; nine of them had
        no knob at all, so the one thing a switch is — a control whose grip
        MOVES — was the one thing the axis was not saying."""
        return self._component("switch", None, 0, 1, w, with_checked(state, on))

    def checkbox(self, on: bool, state: str = DEFAULT) -> str:
        """main + knob, and no track between them: a box, and a mark that is
        either in it or not.

        NO WIDTH ARGUMENT, and that is the anatomy talking rather than a
        convenience. `w` is how many cells an EXTENT may spend; a checkbox
        has no extent, so there is nothing for a caller to budget. Asking for
        a wider one would be asking for a wider box, and a wide box with a
        mark loose in it is a track — which is the switch, one method up.

        The bit is written the same way the switch writes it (`with_checked`,
        one seat), so the same law holds by construction: a checkbox cannot
        render CHECKED with an empty box."""
        return self._component("checkbox", None, 0, 1, 1,
                               with_checked(state, on))

    def button(self, label: str, w: int = 0, state: str = DEFAULT,
               danger: bool = False) -> str:
        """main, and NOTHING else — the control with no value.

        The label is CONTENT, not a part (see the registry entry). The one
        slot this component composes is the language's WALLS; they are split
        in half and the caller's word stands between them, on the field they
        enclose. So the state rides the walls, which the language owns, and
        the word comes back out byte for byte, which the caller owns.

        `w` IS A MINIMUM, not a width. A checkbox took no width argument at
        all because it has no extent to spend cells on; a button has a FIELD,
        and a caller with a row of them needs their fields to agree. Below the
        label's own width it does nothing — a button cannot truncate the word
        it exists to name, because the word is the only thing that says what
        pressing it will do.

        NO READOUT is appended, and that is `has_value` rather than a decision
        taken here: there is no number and no bit to report, so `value_label`
        and `check_label` have nothing to say about a button."""
        (_, walls, tone), = self.component_cells("button", None, 0, 1, 1,
                                                 state)
        half = len(walls) // 2
        word = str(label)
        if danger:
            lo, hi = self.DANGER_FORM
            word = f"{lo}{word}{hi}"
        text = word.center(max(int(w), len(word)))
        return (f"[{tone}]{mark(walls[:half])}[/]"
                f"[{self.check_tone(True, state)}]{mark(text)}[/]"
                f"[{tone}]{mark(walls[half:])}[/]")

    def textfield(self, value: str = "", caret: int | None = None,
                  w: int = 12, state: str = DEFAULT,
                  placeholder: str = "", caret_on: bool = True) -> str:
        """main + caret — the first component with a cursor INSIDE it.

        THE VALUE IS CONTENT, which is the button's ruling applied to a
        value instead of a label: it comes back out of the render byte for
        byte, never recased, never letterspaced, and NEVER SHORTENED. The
        language draws the ground it lies on and the mark that says where the
        next keystroke lands, and nothing else.

        THE CARET TAKES A COLUMN OF ITS OWN, and that is the content law
        choosing the mechanism rather than taste choosing it. A block caret
        sitting ON a character hides that character — so the value would not
        come back whole, and the only way to keep it readable underneath
        would be reverse video, which is COLOUR and this contract's states
        may never ride colour alone. A bar between two columns costs one cell
        and keeps every byte.

        THE WINDOW, and it is where a text field stops being a button. A
        value longer than the field is not truncated: the VIEW moves. The
        window slides the least it can to keep the caret inside, so every
        index of the value is reachable — which is the honest form of "no
        character is ever lost", and it is asked of every index in the suite
        rather than asserted here.

        THE PLACEHOLDER IS CONTENT TOO, and it is separated from the value by
        TONE — the one place in this contract where colour carries the whole
        distinction, said out loud rather than hidden. Shape is not available:
        the placeholder is the caller's words and may not be bracketed or
        recased any more than the value may. And the distinction must exist,
        because a field showing `search` that the user typed and a field
        showing `search` that is merely suggesting are two different states of
        the model. It is not a STATE distinction, which is what the
        "never colour alone" law governs; it is set-versus-unset, and that is
        `check_tone` for the fourth time — lit when the user put it there,
        muted when the field did.

        `caret_on` IS THE BLINK'S OFF FRAME, and it is a MOTION argument on a
        render seat rather than a sixth state. A blink is not a state — the
        field is being edited in both frames — so it may not enter the state
        axis, and the one thing it changes is the GLYPH in the caret's own
        column: the mark, or the rune the field's paper is made of. The
        column stays the caret's, drawn in the caret's tone, so the value
        does not move under the blink and the two frames differ in exactly
        one character. That is the ambient regime's whole channel."""
        text, ph = str(value), str(placeholder)
        w = max(1, int(w))
        editing = control_of(state) == EDITED
        shown = text or ph
        cols: list[str | None] = list(shown)
        cpos = None
        if editing:
            want = len(text) if caret is None else int(caret)
            cpos = 0 if not text else max(0, min(len(text), want))
            cols.insert(cpos, None)        # the caret's own column
        # THE WINDOW IS THE SHARED SEAT'S NOW, not this method's. These five
        # lines used to be computed here, which made them a local variable
        # with a view's name: nothing declared them, and the one other
        # component whose value is a window could not have reached them.
        start = view_start(len(cols), w, cpos)
        view = cols[start:start + w]
        cells = self.component_cells("textfield", None, 0, 1, w, state,
                                     caret=None if cpos is None
                                     else cpos - start)
        op, rune, cl = self.field_form(state, "textfield")
        lit = self.check_tone(bool(text) or not ph, state)
        ground = self.part_tone("main", state, "textfield")
        body = []
        for i, (part, glyph, tone) in enumerate(cells):
            ch = view[i] if i < len(view) else None
            if part == "caret" or ch is None:
                if part == "caret" and not caret_on:
                    glyph = rune
                body.append(f"[{tone}]{mark(glyph)}[/]")
            else:
                body.append(f"[{lit}]{mark(ch)}[/]")
        return (f"[{ground}]{mark(op)}[/]" + "".join(body)
                + f"[{ground}]{mark(cl)}[/]")

    def textarea(self, lines, caret: tuple[int, int] | None = None,
                 w: int = 12, h: int = 3,
                 state: str = DEFAULT) -> list[str]:
        """THE TEXT FIELD'S CONTRACT OVER A RECTANGLE — `h` rows, each the
        same field the one-line seat draws.

        NOTHING PER-LANGUAGE IS DECLARED FOR IT, and that is the finding
        rather than a shortcut. Every mark this needs is already a seat: the
        walls and the paper are `field_form(state, "textfield")`, the caret
        is the `caret` part in the parts registry, the lit and unlit tiers are
        `check_tone` and `part_tone`. A language that answered the one-line
        field has already answered this one, and a second table would have
        been eleven restatements of six existing ones.

        THE CARET TAKES A COLUMN OF ITS OWN, on ONE row. `caret` is
        `(row, col)`: the field has exactly one insertion point, and a mark on
        every row would draw a state the model cannot be in. The column is the
        one-line seat's law for the one-line seat's reason — a block caret ON
        a character hides it, and the only way to keep it readable underneath
        is reverse video, which is colour.

        THE LINE BREAKS ARE THE CALLER'S. It passes `lines`; a kit does not
        know where this app's paragraphs end. What the kit owns is what
        happens when a line does not fit, and the mark for that is the
        language's own `DISCLOSE` — the third component to spend it, on the
        same declaration as the other two: a select points at a list, a log's
        tail at the line that has not arrived, a wrapped row at the text that
        did not fit.

        AND THAT IS THE ONE PLACE THE BYTES STOP. A one-line field can move
        its WINDOW sideways; a rectangle's rows cannot, so an over-long line
        shows its own leading bytes, unrecased and in order, and says with a
        mark that there are more. Nothing is substituted and nothing is
        silently dropped — but "byte for byte" holds for the lines that FIT,
        which is stated here rather than discovered in a frame."""
        w, h = max(1, int(w)), max(1, int(h))
        op, rune, cl = self.field_form(state, "textfield")
        ground = self.part_tone("main", state, "textfield")
        lit = self.check_tone(True, state)
        cg = self.part_glyph("caret", state, "textfield")
        ct = self.part_tone("caret", state, "textfield")
        cr, cc = (int(caret[0]), int(caret[1])) if caret else (-1, 0)
        out = []
        for i in range(h):
            text = str(lines[i]) if i < len(lines) else ""
            cols: list[str | None] = list(text)
            if i == cr:
                cols.insert(max(0, min(len(text), cc)), None)
            more = len(cols) > w
            view = cols[:w - 1] if more else cols[:w]
            body = [f"[{ct}]{mark(cg)}[/]" if ch is None
                    else f"[{lit}]{mark(ch)}[/]" for ch in view]
            if more:
                body.append(f"[{self.c['accent']}]{mark(self.DISCLOSE)}[/]")
            elif len(view) < w:
                body.append(f"[{ground}]"
                            f"{mark(rune * (w - len(view)))}[/]")
            out.append(f"[{ground}]{mark(op)}[/]" + "".join(body)
                       + f"[{ground}]{mark(cl)}[/]")
        return out

    GROUP_SEP = "  "                       # air between a group's items

    def radio_items(self, options, selected: int, state: str = DEFAULT,
                    focus: int | None = None) -> list[str]:
        """A SELECTION SET, one markup string per item: the well, the mark,
        and the option's own name.

        NO `on` ARGUMENT ANYWHERE, and that absence is the increment. The
        switch and the checkbox are handed their bit; a radio item's bit is
        computed by `group_states` from the group's single index, so the two
        ways this render could lie — no item marked, two items marked — are
        not reachable from here. The invariant is upstream of the drawing.

        The word beside an item is the OPTION, not `CHECK_WORDS`: `ON` next
        to `fast` would be the language answering a question nobody asked.
        The tone rule is still the shared one (`check_tone`)."""
        sts = group_states(len(options), selected, state, focus)
        return [self._component_body("radio", None, 0, 1, 1, st)
                + f" [{self.check_tone(is_checked(st), st)}]{mark(o)}[/]"
                for o, st in zip(options, sts)]

    def radio_group(self, options, selected: int, state: str = DEFAULT,
                    focus: int | None = None) -> str:
        """The set as one row. Sibling of `radio_items` the way `switch` is a
        sibling of `checkbox`: a call, not a decision."""
        return self.GROUP_SEP.join(
            self.radio_items(options, selected, state, focus))

    def stepper(self, options, selected: int, w: int = 0,
                state: str = DEFAULT, wrap: bool = False) -> str:
        """main + step — THE SAME CHOICE AS A RADIO, DRAWN THE OTHER WAY.

        A radio shows every option and marks one; a stepper shows the marked
        one and offers the two ways off it. Same option list, same single
        index, and the seat that owns that index is the same one: this
        method reaches `group_states`, so an out-of-range selection RAISES
        here for the reason it raises there, and the state of the option this
        shows is the state of the item a radio would MARK — byte for byte,
        at every index. Two mechanisms, one choice model, and the second half
        of that sentence is a law rather than a claim.

        NO `on` ARGUMENT, for the group's reason: the bit is computed from
        the index, so a stepper cannot show an option that is not the chosen
        one. What it CAN be handed is an index the set does not have, and
        that is where the group seat refuses it.

        THE WORD IS CONTENT — the button's ruling for the third time. It
        comes back out byte for byte, never recased and NEVER SHORTENED, and
        it is centred on a field reserved for the WIDEST option in the set,
        so spinning through the set cannot move the control's edges (Bodmer
        T2: reserve the widest form, then nothing reflows). `w` is a MINIMUM
        under that, exactly as it is on a button.

        WRAP IS THE CALLER'S, and this method does not decide it: what the
        range MEANS is not a fact about steppers. It is passed straight to
        the composer, where it decides whether an end seat has a step or
        GROUND — which is why a clamped stepper at its floor SHOWS its floor
        and a wrapping one shows nothing of the kind."""
        opts = [str(o) for o in options]
        i = int(selected)
        st = group_states(len(opts), i, state, focus=i)[i]
        cells = self.component_cells("stepper", i, 0, len(opts) - 1, 1,
                                     state, wrap=wrap)
        field = max(int(w), max(len(o) for o in opts))
        word = opts[i].center(field)
        return "".join(f"[{t}]{mark(g)}[/]" for _, g, t in cells[:1]) \
            + f"[{self.check_tone(is_checked(st), st)}]{mark(word)}[/]" \
            + "".join(f"[{t}]{mark(g)}[/]" for _, g, t in cells[1:])

    def select(self, options, selected: int, w: int = 0,
               state: str = DEFAULT) -> str:
        """THE CLOSED SELECT — the chosen value among several, and the mark
        that says there are others.

        IT IS NOT A STEPPER, and the operator's ruling 7 says so because the
        PROTOTYPE round drew it as one. The two controls answer different
        questions: a stepper shows THE TWO WAYS OFF a value (its steps are
        the ± of a set you move through in place), a select shows THE ONE WAY
        INTO a list (its disclosure is a door). Drawing the first where the
        second belongs tells the user the arrow keys will change the setting,
        which in a select they do not — they open it.

        THE GROUND IS THE FIELD'S, and that is the anatomy argument rather
        than a shortcut: a select is A FIELD YOU DO NOT TYPE INTO. It holds
        one value, it has walls, it takes the control states — everything the
        text field is except the caret. So it borrows `field_form` and the
        registry grows nothing, which is this contract's rule for a shape
        that is an existing anatomy in a new job.

        THE WORD IS CONTENT, byte for byte, and the field is reserved for the
        WIDEST option in the set (Bodmer T2), so choosing another option
        cannot move the control's edges. `w` is a MINIMUM under that.

        THE INDEX IS THE GROUP'S, so an out-of-range selection RAISES here
        exactly as it does in `stepper` and `radio_group` — one choice model,
        three mechanisms."""
        opts = [str(o) for o in options]
        i = int(selected)
        st = group_states(len(opts), i, state, focus=i)[i]
        c = self.c
        op, _, cl = self.field_form(state, "textfield")
        tone = self.part_tone("main", state, "textfield")
        field = max(int(w), max(len(o) for o in opts))
        return (f"[{tone}]{mark(op)}[/]"
                f"[{self.check_tone(is_checked(st), st)}]"
                f"{mark(opts[i].ljust(field))}[/]"
                f"[{c['dim']}]{mark(self.DISCLOSE)}[/]"
                f"[{tone}]{mark(cl)}[/]")

    def menu(self, options, selected: int, w: int = 0,
             state: str = DEFAULT) -> list[str]:
        """THE OPEN SELECT — every option, one marked, as ROWS.

        A MENU IS A LIST AND NOT A SURFACE, which is the decision that keeps
        this method out of the overlay's argument entirely: no language draws
        a frame here, including the one language whose commitment licenses a
        modal border (prism's borders are reserved for MODALS, and a dropdown
        is not one). What separates the open list from the page behind it is
        the same thing that separates a selected row from its neighbours in
        every other list this contract draws: the language's own cursor and
        its own tones.

        Rows rather than a joined string, for `menu`'s whole reason for
        existing: the caller places them, and a caller that must place a list
        under a control needs to know where each row starts."""
        opts = [str(o) for o in options]
        i = int(selected)
        sts = group_states(len(opts), i, state, focus=i)
        c = self.c
        field = max(int(w), max(len(o) for o in opts))
        out = []
        for j, o in enumerate(opts):
            here = j == i
            cur = self.CUR if here else " " * len(self.CUR)
            tone = c["ink"] if here else c["mut"]
            out.append(f"[{c['accent'] if here else c['dim']}]{mark(cur)}[/] "
                       f"[{tone}]{mark(o.ljust(field))}[/]")
        return out

    # THE LOG LEVELS, and they are a GLYPH LADDER rather than three hues.
    #
    # `ICONS` carries six DOMAIN kinds (deadline, overdue, wip, blocked...)
    # and no log level, which is what the PROTOTYPE round found when it drew
    # a monitor screen: five languages marked ERROR with the same `!!` in the
    # same alert hue, because there was nothing per-language to mark it with.
    #
    # ONE WIDTH PER LANGUAGE, so a column of rows aligns; three shapes, so the
    # level survives the colour being taken away (operator ruling 8).
    LEVELS = {"info": "· ", "warn": "! ", "error": "!!"}

    # THE VALIDATION ROW — what a language does with the rest of the line
    # after it has said what was rejected, and which tier it says it in.
    #
    # `ERROR_FILL` is the NOTATION the PROTOTYPE round asked for by name:
    # "ledger's leaders, corgi's segment legend, blueprint's revision note".
    # Air is a real answer (the terminal writes the message and stops) and it
    # is the base's.
    #
    # `ERROR_TONE` exists because TWO of these languages ration their alert
    # hue by commitment — ledger spends it on literal debt, blueprint on
    # overdue and nothing else ("a calm sheet carries zero alert") — and a
    # validation message reaching for red would break the one mark those two
    # guard. inc18 solved the same problem for the log by taking the hue away
    # from ALL ELEVEN; that was right for a stream of rows and it is too much
    # here, where one row is the whole point. So the tier is a per-language
    # decision, which is what it actually is.
    ERROR_FILL = ""
    ERROR_TONE = "alert"

    def error(self, msg: str, w: int) -> str:
        """THE ROW THAT EXPLAINS A REJECTION.

        THE MESSAGE IS CONTENT and comes back byte for byte — no recasing, no
        truncation, no ellipsis. Three of these languages letter their labels
        in capitals and none of them may letter this: the words are the
        caller's account of what is wrong, and a language that shouted them
        would be editing the complaint.

        THE MARK IS THE LANGUAGE'S SEVERITY LADDER, not a new table. `LEVELS`
        already carries three shapes of one width per language, already
        survives the colour being taken away (operator ruling 8), and already
        says ERROR in this language's own alphabet. A second table beside it
        would be two answers to one question — and an inline validation
        failure and a log line at ERROR are the same claim about the same
        severity, made about a field instead of about an event.

        `w` IS A MINIMUM, `field_row`'s rule: the row is filled out to `w`
        with `ERROR_FILL` and NEVER cut. A validation message trimmed to fit
        is the one string in a form that must not be."""
        c = self.c
        text = str(msg)
        mk = self.LEVELS["error"]
        tone = c.get(self.ERROR_TONE, c["ink"])
        row = (f"[{tone}]{mark(mk)}[/] [{c['ink']}]{mark(text)}[/]")
        gap = w - len(mk) - 1 - len(text)
        if self.ERROR_FILL and gap > 1:
            row += (" " + f"[{c['dim']}]"
                    f"{mark(self.ERROR_FILL * (gap - 1))}[/]")
        return row

    # THE REQUIRED MARK — one cell, and it may NOT be a bare `*` in eleven
    # languages, which is the palette-swap failure at a single glyph. It is a
    # PROPERTY of the field rather than an alert or an action, so the base
    # spends the ink tier on it: one weight step above the `mut` caption it
    # stands beside (HIERARCHY.md's dim/normal/bright ladder), and no rationed
    # hue at all. `*` is the terminal's own convention and the base kit is the
    # terminal; every language with an alphabet of its own answers below.
    REQUIRED = "*"

    def required(self) -> str:
        """The mark beside a caption whose field may not be left empty."""
        return f"[{self.c['ink']}]{mark(self.REQUIRED)}[/]"

    def knockout_cell(self, text: str) -> str:
        """REVERSE VIDEO — a cell that trades ink for ground.

        One seat, because it is one mechanism: blueprint's title block already
        drew it inline, and operator ruling 10 lets that single knockout MOVE
        to a confirm's default answer. A mechanism that can move needs a seat
        to move to.

        EXACTLY ONE PER VIEW IS THE CALLER'S LAW and this method cannot
        enforce it: a kit method is handed one cell at a time and has no
        cross-view knowledge (the same limit that keeps blueprint's knockout
        on the title block rather than on the most overdue item). What the
        kit owns is the INVERSION; what the view owns is how many there are.

        AND IT IS THE ONE MARK IN THIS FILE THAT DOES NOT SURVIVE THE `.txt`:
        an inversion is a background, so a cell grid shows the word and not
        the emphasis. Recorded rather than worked around -- the honest place
        to read a knockout is the SVG."""
        return f"[{self.t['ground']} on {self.c['ink']}]{mark(text)}[/]"

    # THE MATCH STYLE, and it is a STYLE rather than a mark for a reason the
    # content law forces: see `match()`. `bold` and `underline` are not hues,
    # so this is still two channels in a real terminal -- but neither of them
    # survives a cell grid, which is stated at the seat rather than discovered
    # in a frame.
    MATCH_STYLE = "bold {accent}"

    def match(self, text: str, query: str) -> str:
        """THE RESULT ROW OF A SEARCH: the text, and where the query is in it.

        THE TEXT COMES BACK BYTE FOR BYTE (operator ruling 9). Not "contains",
        not "the same words": the same bytes, in the same order, with nothing
        inserted between them. Three of these languages letter their titles in
        capitals; in this row they may not, and that is the ruling. A palette
        that recased its results would be answering a question about
        `redirect` with a row that says `REDIRECT`, and the user could no
        longer see that what they typed is what was found.

        SO THE EMPHASIS CANNOT BE A SHAPE, and this is the one place in the
        contract where that is true. Every other mark this file draws adds a
        cell -- a wall, a dagger, a dot, a terminator -- and adding a cell
        HERE would break the byte identity that is the whole ruling. What is
        left is the STYLE channel: weight, underline, reverse. They are not
        hues, so "never colour alone" is honoured in a real terminal; they are
        also not glyphs, so they do NOT survive a cell grid, and a `.txt` of
        this row is a row with no emphasis in it at all. That is a limit of
        the medium being recorded, not a mechanism being skipped.

        NO MATCH IS A CASE, not an error: the text comes back unmarked, which
        is what a result row that no longer matches should look like while the
        query is still being typed."""
        t, q = str(text), str(query)
        if not q:
            return f"[{self.c['ink']}]{mark(t)}[/]"
        i = t.lower().find(q.lower())
        if i < 0:
            return f"[{self.c['mut']}]{mark(t)}[/]"
        j = i + len(q)
        style = self.MATCH_STYLE.format(**self.c)
        return (f"[{self.c['mut']}]{mark(t[:i])}[/]"
                f"[{style}]{mark(t[i:j])}[/]"
                f"[{self.c['mut']}]{mark(t[j:])}[/]")

    def keyhint(self, pairs, w: int = 0) -> str:
        """THE KEY HINTS: the kit owns the NOTATION, the caller owns every
        KEY.

        inc12 §8.3, learned from a consumer app and paid for once already:
        "a mark that encodes a binding belongs to whoever owns the keymap.
        Never the library." The kit's display legend used to hardcode `[1]`
        and spend a binding on behalf of every app that drew one. So this
        method takes `(key, label)` pairs and prints what it is handed.

        THE LABEL IS A LABEL, which is `field_row`'s ruling: a language that
        letters its legends in capitals letters these too. The KEY is not
        touched at all -- it is the literal thing the user must press."""
        c = self.c
        return "   ".join(f"[{c['accent']}]{mark(str(k_))}[/] "
                          f"[{c['dim']}]{mark(str(v))}[/]"
                          for k_, v in pairs)

    def log_row(self, level: str, time: str, message: str,
                tail: bool = False) -> str:
        """ONE ROW OF A STREAM: when, how bad, and what happened.

        A FULL ROW CONTRACT rather than an `ICONS` entry (operator ruling 8),
        because the three fields are not independent: the level decides the
        weight the message is set in, the time is the only thing in the row
        that is not the message's, and a level mark drawn beside a row the
        caller composed would be a mark with no column to sit in.

        THE LEVEL READS WITH THE COLOUR REMOVED. That is the ruling, and it
        is why `LEVELS` is a glyph ladder: three shapes of one width, so a
        greyscale eye sorts the rows and a column of them still aligns.

        AND THE HUE LADDER IS NEUTRAL — dim, mut, ink — rather than
        info/warn/alert, which is a decision with a cost and a reason. Two of
        these languages ration their alert hue by commitment (ledger spends it
        on literal debt, blueprint on overdue and nothing else: "a calm sheet
        carries zero alert"), so a log that reached for red on every ERROR
        would break the one mark those languages guard. The severity is
        therefore carried by SHAPE plus NEUTRAL WEIGHT, in all eleven, and a
        caller who owns its own palette can still tone the message it passes.

        TIME AND MESSAGE ARE BOTH CONTENT and come back byte for byte. A log
        that recased its messages would be editing the record.

        `tail` IS THE LIVE EDGE — the row the next line will arrive after —
        and it is drawn with the language's own DISCLOSE mark, which is the
        same declaration the select spends: the mark that says THERE IS MORE.
        A select points at a list, a log points at the line that has not
        arrived yet."""
        c = self.c
        mk = self.LEVELS.get(level, self.LEVELS["info"])
        tone = {"info": c["dim"], "warn": c["mut"]}.get(level, c["ink"])
        body = c["mut"] if level == "info" else c["ink"]
        row = (f"[{c['dim']}]{mark(str(time))}[/] "
               f"[{tone}]{mark(mk)}[/] "
               f"[{body}]{mark(str(message))}[/]")
        if tail:
            row += f" [{c['accent']}]{mark(self.DISCLOSE)}[/]"
        return row

    def _split_cell(self, glyph: str, tone: str, w: int) -> str:
        """One row of a pane seat: `glyph` centred in exactly `w` cells.

        The pad is PLAIN and only the glyph is toned, so a language whose
        answer is air spends no markup at all — which is what makes "the
        division is nothing" measurable in the `.txt` rather than merely
        described."""
        g = str(glyph)
        lead = max(0, (w - len(g)) // 2)
        return (" " * lead + (f"[{tone}]{mark(g)}[/]" if g else "")
                + " " * max(0, w - lead - len(g)))

    def pane_split(self, h: int, w: int = 3) -> list[str]:
        """TWO REGIONS SIDE BY SIDE — `h` rows of exactly `w` cells, and what
        stands between them.

        THE LAST COMPOSITION PRIMITIVE, and the one COMPONENTS.md calls "the
        last palette-swap": every other seat in this file draws a THING, and
        this one draws the RELATION between two of them. The prototype round
        drew `│` in five languages at once — the same defect as the red `!`
        and the borrowed dot leader, one cell wide.

        THE REFUSAL REGISTRY IS CONSULTED FIRST, exactly as `overlay` does,
        and consulting it is what makes it a mechanism rather than a note: a
        language whose alphabet cannot construct a vertical stroke never
        reaches the stroke code, whatever it did or did not override.

        `w` IS A SEAT, not a suggestion: every row comes back at exactly `w`
        cells so the two panes stay in their columns on every line. A split
        that varied its width would move the right pane down the page.

        AND NO LANGUAGE OVERRIDES *THIS* METHOD, which is the same shape
        `overlay` has and for the same reason: a language that overrode the
        entry point would never consult the table, so the table would decide
        nothing for it and a false entry against it would go undetected. What
        a language overrides is `pane_split_rule` (it draws) or
        `pane_split_instead` (it refuses). The first version of this seat had
        three languages overriding the entry point and the registry's own
        teeth test found it.

        BASE (nord) IS THE TERMINAL'S OWN: a hairline rule at the dim tier,
        with a cell of air on each side. The environment's convention, and
        the base kit is the environment."""
        if self.name in PANE_SPLIT_REFUSED:
            return self.pane_split_instead(h, w)
        return self.pane_split_rule(h, w)

    #: the mark a language rules a pane seat with. A constant, because for
    #: most languages that is the whole decision; a language whose divider
    #: changes down the page overrides `pane_split_rule` instead.
    PANE_RULE = "│"

    def pane_split_rule(self, h: int, w: int = 3) -> list[str]:
        """The drawing branch — `PANE_RULE`, centred, at the dim tier."""
        return [self._split_cell(self.PANE_RULE, self.c["dim"], w)
                for _ in range(max(0, h))]

    def pane_split_instead(self, h: int, w: int = 3) -> list[str]:
        """WHAT A LANGUAGE DOES WHEN IT MAY NOT DRAW THE RULE.

        The base answer is the mildest one available and it is not a blank:
        it is AIR, which for a language that separates by alignment is the
        whole mechanism. A language in the registry that overrides nothing
        still cannot draw a stroke, which is the registry doing its job even
        where nobody has done the design."""
        return [" " * w for _ in range(max(0, h))]

    def recede(self, row: str) -> str:
        """The page BEHIND something, drawn inactive.

        A per-language seat rather than a constant, because "inactive" is a
        commitment: most languages drop the ink to the dim tier, prism steps
        the BACKGROUND instead (its whole depth mechanism), and naught's dim
        tier IS its lattice going unlit -- the same call, three meanings."""
        return f"[{self.c['dim']}]{mark(visible(row))}[/]"

    def overlay(self, rows: list[str], w: int, h: int,
                under: list[str]) -> list[str]:
        """A QUESTION IN FRONT OF A PAGE — `h` rows of `w` cells, composed.

        BASE (nord) IS THE TERMINAL'S OWN MODAL: a box, centred, over a page
        dropped to the dim tier. That is the environment's convention and the
        base kit is the environment.

        THE REFUSAL REGISTRY IS CONSULTED FIRST, and consulting it is what
        makes it a mechanism rather than a note: a language that has
        committed against boxes never reaches the box code, whatever it did
        or did not override. `MODAL_BORDER_REFUSED` says who, and with what
        commitment; `overlay_instead` is what they do about it.

        THE ROWS ARE THE CALLER'S WORDS. A kit does not know that three tasks
        are about to be deleted; it knows how this language separates a
        question from what the question is about.

        AND NO LANGUAGE OVERRIDES *THIS* METHOD, for the reason `pane_split`
        states at length and this seat learned second: a language that
        overrode the entry point would never consult the table, so a false
        entry against it could not be wrong out loud. What a language
        overrides is `overlay_box` (it draws a lid, in its own chrome) or
        `overlay_instead` (it may not)."""
        if self.name in MODAL_BORDER_REFUSED:
            return self.overlay_instead(rows, w, h, under)
        return self.overlay_box(rows, w, h, under)

    #: The lid a language that may draw one draws, in `DISPLAY_BOX`'s own
    #: order: (tl, tr, bl, br, top, bottom, left, right). EIGHT cells rather
    #: than six, because half-cell chrome has a different glyph at the top of
    #: a box than at the bottom -- and because a language that already
    #: declares a display's frame should be able to hand the same string to
    #: both rather than spell its corners twice.
    MODAL_BOX = "┌┐└┘──││"

    def overlay_box(self, rows: list[str], w: int, h: int,
                    under: list[str]) -> list[str]:
        """The drawing branch: `MODAL_BOX`, centred, over a receded page."""
        c = self.c
        tl, tr, bl, br, top, bot, lt, rt = self.MODAL_BOX
        body = [visible(r) for r in rows]
        dw = min(max(8, w), max(len(b) for b in body) + 4)
        x = max(0, (w - dw) // 2)
        box = [f"[{c['ink']}]{mark(tl + top * (dw - 2) + tr)}[/]"]
        for r, b in zip(rows, body):
            box.append(f"[{c['ink']}]{mark(lt)}[/] " + r
                       + " " * max(0, dw - 3 - len(b))
                       + f"[{c['ink']}]{mark(rt)}[/]")
        box.append(f"[{c['ink']}]{mark(bl + bot * (dw - 2) + br)}[/]")
        y = max(0, (h - len(box)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(box):
                out.append(" " * x + box[i - y])
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out

    def overlay_instead(self, rows: list[str], w: int, h: int,
                        under: list[str]) -> list[str]:
        """WHAT A LANGUAGE DOES WHEN IT MAY NOT DRAW THE BOX.

        The base answer is the mildest one available: the question stands on
        the page with nothing around it, and the page recedes. A language in
        the registry that overrides nothing still cannot draw a lid, which is
        the registry doing its job even where nobody has done the design."""
        y = max(0, (h - len(rows)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(rows):
                out.append(rows[i - y])
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out

    # -- spinner: indeterminate progress, precomputed frames ----------------
    def spinner(self, tick: int) -> str:
        return f"[{self.c['mut']}]{self.SPIN[tick % len(self.SPIN)]}[/]"

    # ======================================================================
    # MOTION — ONE ENGINE, FIVE EVENTS (the motion contract, above).
    #
    # `MOTION_STEPS` is the language's whole motion CHARACTER, and it is one
    # number because the other half of the character is a token it already
    # declares: the frames are what the language elaborates, the `tempo`
    # token is how long they take. Swiss renounces with 0 — and renouncing
    # ELABORATION is not renouncing the event: a transition still has two
    # frames, because a one-frame transition is not a transition, it is a
    # cut. That floor is the engine's, not the language's.
    #
    # This token used to be called `FLIP_STEPS` and belonged to the switch.
    # It governs five events now and the rename is the increment: a language
    # that elaborated its switch and cut its button would be two languages.
    # ======================================================================
    MOTION_STEPS = 1                       # intermediate frames; 0 renounces

    def motion_frames(self, component: str, event: str, *,
                      _steps: int | None = None, **kw) -> Motion:
        """THE ONE MOTION SEAT: a list of RENDERS, its regime, and a step.

        Every frame is a LEGAL RENDER composed by the component seats this
        contract already has — a motion never draws; it asks the same seats
        for the same control at intermediate values. That is what keeps a
        frame from going stale the way the eight hand-authored `flip_frames`
        did (pass 49 deleted them as pictures of a dead switch): a frame that
        is a render cannot animate between two widths a component no longer
        has.

        THE REGIME AND THE DURATION ARE DERIVED, and neither is reachable
        from a language. The regime comes off the EVENT; the duration comes
        off the regime and the language's `tempo` token. A transition's
        WHOLE pass is one tempo, split evenly across the gaps between its
        frames — which is byte-for-byte the arithmetic the config screen has
        driven the switch flip with since pass 49, now stated once instead of
        living in a caller.

        AND THE ELABORATION IS CEILINGED BY THE SURFACE (#36). A transition's
        one tempo is split across the gaps between its frames, so a language
        that elaborates hard at a short tempo derives a step under the
        compositor's own period and schedules frames that will be coalesced.
        The ceiling ASKS THE BUILDER rather than restating each event's gap
        arithmetic here: it drops one step at a time and rebuilds until the
        derived step clears the floor. That is the difference between a
        ceiling and a second copy of the builders' shape — `press` adds one
        gap per step, `travel` adds one per WELL CROSSED, `spin` and `flip`
        one per mid frame, and a closed form would have to know all four and
        go stale the day a fifth event lands.

        AND IT ASKS THROUGH THE TOKEN, NOT THROUGH A PARAMETER. The first
        form of this gave every builder a `steps=` argument and the suite
        stopped at the first mutant: the battery's whole method is to
        SUBCLASS a builder, and a ceiling that makes every override grow an
        argument is a ceiling that taxes the instrument measuring it. What
        the ceiling varies is the language's own `MOTION_STEPS`, so it varies
        exactly that — on a copy, so nothing is mutated — and every builder,
        overridden or not, is asked the question in the only vocabulary it
        already speaks.

        `_steps` is THE MEASUREMENT DOOR and nothing else may use it: it
        forces an elaboration and skips the ceiling, so a law can build the
        frame list the ceiling refused and show that its raw step really is
        under the floor. A ceiling nothing can build the other side of is a
        claim about arithmetic, not a measurement."""
        regime = motion_regime(event)
        if event in MOTION_GROUP_EVENTS:
            fn = self._motion_travel
        else:
            if event not in motion_events(component):
                raise ValueError(f"{component} has no {event!r} motion")
            fn = getattr(self, f"_motion_{event}")
        ms = int(self.t.get("tempo", 140))
        if regime == AMBIENT:
            # AN AMBIENT HAS NO ELABORATION TO CEILING, and that is the
            # regime split doing its work rather than an exemption. A loop's
            # period is floored at 2000 ms and divided by the frame COUNT, so
            # its step clears the refresh floor by two orders of magnitude —
            # and the caret's builder takes no step count at all, because
            # what would a third frame of a blink be. Its elaboration is 0
            # because it HAS none, not because it was taken away.
            frames = fn(component, **kw)
            return Motion(tuple(frames), regime,
                          max(AMBIENT_MIN_MS, ms * AMBIENT_BEATS)
                          / len(frames), 0)
        n = max(0, self.MOTION_STEPS if _steps is None else _steps)

        def build(steps):
            k = _copy.copy(self)
            k.MOTION_STEPS = steps      # an INSTANCE token, shadowing the
            return getattr(k, fn.__name__)(component, **kw)   # language's

        if _steps is None:
            while n and ms / max(1, len(build(n)) - 1) < REFRESH_MS:
                n -= 1
        frames = build(n)
        # THE FLOOR IS ABSOLUTE AND THE CEILING IS NOT ITS ONLY LEG. At zero
        # elaboration what is left is STRUCTURE — travel's wells — and a
        # language cannot renounce those. Where the structure alone is under
        # the floor the pass RUNS LONG rather than claiming a step the
        # surface will not draw. That leg fires for no shipped fixture and
        # for solari at a distance of three wells, which is measured.
        step = max(ms / max(1, len(frames) - 1), REFRESH_MS)
        return Motion(tuple(frames), regime, step, n)

    def _motion_flip(self, name: str, on: bool = True, w: int = 3,
                     state: str = DEFAULT) -> list[str]:
        """The knob CROSSING the track. The mid frames pass an explicit
        fraction, which is the one caller allowed to: a frame in mid-travel
        is a frame, not a state."""
        n = max(0, self.MOTION_STEPS)
        out = [self._component(name, None, 0, 1, w,
                               with_checked(state, not on))]
        for i in range(1, n + 1):
            f = i / (n + 1)
            out.append(self._component(name, f if on else 1 - f,
                                       0, 1, w, ACTIVE))
        return out + [self._component(name, None, 0, 1, w,
                                      with_checked(state, on))]

    def flip_frames(self, on: bool, w: int = 3) -> list[str]:
        """The switch's flip, as the caller that predates the engine wants
        it: the frames it has to DRAW. Kept as a seat because its caller is
        already showing frame 0."""
        return list(self.motion_frames("switch", "flip", on=on, w=w).plays)

    def _motion_press(self, name: str, label: str = "", w: int = 0,
                      state: str = DEFAULT) -> list[str]:
        """THE PRESS: a HOLD and a RELEASE, and the first debt this contract
        owed the motion axis.

        Its anchor and its rest are THE SAME RENDER, which is what a press
        is: nothing survives it. (A flip, a travel and a spin all land
        somewhere else — that difference is a law, not a comment.) So the
        only thing motion can say here is WHEN the control lets go, and the
        deceleration bias says: not at the start. The extreme is reached on
        the first drawn frame — the acknowledgement is immediate — and the
        remaining budget is the hold before the release lands on the last.
        A language with more steps holds longer; swiss, which renounces,
        gets the two-frame minimum, which is a flash and a release. A
        language the refresh ceiling takes down to zero gets the same two
        frames — by measurement rather than by declaration, which is the
        only difference between swiss and solari here (#36)."""
        n = max(0, self.MOTION_STEPS)
        rest = self._press_render(name, label, w, state)
        hot = self._press_render(name, label, w, ACTIVE)
        return [rest] + [hot] * (1 + n) + [rest]

    def _press_render(self, name: str, label: str, w: int, state: str) -> str:
        """A press is asked of the REGISTRY, not of a component's name: a
        component whose only part is `main` is all ground, so the caller's
        word stands between its walls and `button` is how it is composed.
        Anything else is composed as the control it is."""
        if COMPONENT_PARTS[name] == ("main",):
            return self.button(label, w, state)
        return self._component_body(name, None, 0, 1, max(1, int(w) or 1),
                                    state)

    def _motion_travel(self, name: str, options=(), old: int = 0,
                       new: int = 0, state: str = DEFAULT) -> list[str]:
        """THE MARK CROSSING BETWEEN SIBLINGS — a transition whose scope is a
        SET, which no other motion in this contract has.

        THE FRAME COUNT IS THE DISTANCE'S, not the language's, and that is
        the group scope talking: the mark passes every well between the two
        it joins whether or not a language elaborates, because those wells
        are THERE. What the language chooses is whether the mark is ever seen
        OFF a well — the in-transit sample. Renouncing (`MOTION_STEPS = 0`)
        makes the mark hop well to well; elaborating shows it between them.

        THE IN-TRANSIT FRAME MARKS NOTHING, and it does not come out of
        `group_states`. That seat exists to make "exactly one item is marked"
        unreachable-to-violate, and this frame violates it on purpose — which
        is legal for exactly the reason pass 49 gave the switch's mid frames:
        a frame between two states is a FRAME, not a state. The invariant is
        about where a group RESTS.

        THIS IS THE ONE BUILDER THE REFRESH CEILING CANNOT FULLY GOVERN, and
        the reason is the group scope again: the wells are the DISTANCE's, so
        zero elaboration still costs one gap per well crossed. A travel long
        enough at a tempo short enough is under the floor with nothing left
        to renounce — see `motion_frames`, where the step is floored and the
        pass runs long rather than the wells being dropped (#36)."""
        opts = [str(o) for o in options]
        n = max(0, self.MOTION_STEPS)
        st = control_of(state)

        def transit() -> str:
            return self.GROUP_SEP.join(
                self._component_body(name, None, 0, 1, 1, st)
                + f" [{self.check_tone(False, st)}]{mark(o)}[/]" for o in opts)

        old, new = int(old), int(new)
        out = [self.radio_group(opts, old, state, focus=old)]
        d = 1 if new >= old else -1
        for k in range(old + d, new + d, d):
            if n:
                out.append(transit())
            out.append(self.radio_group(opts, k, state, focus=k))
        if len(out) == 1:                  # old == new: nothing travelled
            out.append(out[0])
        return out

    def _motion_spin(self, name: str, options=(), old: int = 0, new: int = 0,
                     w: int = 0, state: str = DEFAULT,
                     wrap: bool = False) -> list[str]:
        """THE OPTION CHANGING, and solari's heritage is the whole design.

        WHAT STANDS BETWEEN THE TWO WORDS IS THE LANGUAGE'S OWN `SPIN` — the
        frame-motion token every language already declares for its spinner.
        Nothing is hand-authored here and nothing is invented: on a split-flap
        board that token is a cell mid-turn, so the in-transit frames ARE the
        riffle; on the terminal's own idiom they are the spinner marks; a
        language that renounces motion never draws one. Each cell takes the
        token one phase further along, so the field reads as a wave rather
        than as ten copies of one glyph.

        THE STEPS ARE DRAWN AT THE DESTINATION, because the value has already
        moved — the key press changed the model, and what is catching up is
        the WORD. So the frame diff is the word's cells and nothing else, and
        the field cannot breathe: the in-transit word is exactly as wide as
        the widest option, which is the width the control already reserved."""
        opts = [str(o) for o in options]
        old, new = int(old), int(new)
        field = max(int(w), max(len(o) for o in opts))
        out = [self.stepper(opts, old, w, state, wrap)]
        for s in range(max(0, self.MOTION_STEPS)):
            blur = "".join(self.SPIN[(s + i) % len(self.SPIN)]
                           for i in range(field))[:field]
            spun = list(opts)
            spun[new] = blur
            out.append(self.stepper(spun, new, w, state, wrap))
        return out + [self.stepper(opts, new, w, state, wrap)]

    def _motion_blink(self, name: str, value: str = "",
                      caret: int | None = None, w: int = 12,
                      state: str = EDITED, placeholder: str = "") -> list[str]:
        """THE CARET — the contract's FIRST AMBIENT, and the one motion here
        with nothing to arrive at.

        TWO FRAMES, and the diff is ONE CELL'S GLYPH: the caret's column
        wears the language's caret mark, then the RUNE its paper is made of.
        The tone does not move — not "does not happen to", cannot: the column
        is drawn from the caret's own tone in both frames, so this motion
        satisfies the strict reading of the colour rule and not merely the
        law's. Which is the point: the corpus animates 241 things and none of
        them is a colour, and the first loop this contract ships had better
        be the proof rather than the exception."""
        return [self.textfield(value, caret, w, state, placeholder,
                               caret_on=on) for on in (True, False)]

    # -- tabs: the view switcher. Active on two channels (cursor + colour) --
    def tabs(self, options: list[str], active: str) -> str:
        c = self.c
        out = []
        for o in options:
            if o == active:
                out.append(f"[{c['accent']}]{self.CUR}{o}[/]")
            else:
                out.append(f"[{c['mut']}] {o}[/]")
        return f"[{c['dim']}] │ [/]".join(out)

    # ======================================================================
    # IDENTITY — mascot, wordmark, voice (COMPONENTS.md). The axis that
    # separates a THEME from a BRAND (Charm, Claude Code, Nothing).
    # ======================================================================
    VOICE = {"empty": "empty", "no_signals": "No signals enabled."}

    def _bitmap(self, mask: list[str]) -> list[list[int]]:
        return [[1 if ch == "#" else 0 for ch in row] for row in mask]

    def mascot(self) -> list[str]:
        """The creature, drawn through this language's pixel base — same
        mask, eight different pixels."""
        base = self.t.get("base", "block")
        if base == "segment":              # digits-only base: fall back chunky
            base = "block"
        sx, sy = BS.BASE_SCALE.get(base, (1, 1))
        rows = BS.render(BS.scale(self._bitmap(MASCOT), sx, sy), base)
        return [f"[{self.c['accent']}]{r}[/]" for r in rows]

    def wordmark(self, text: str) -> list[str]:
        """Display type: a short word drawn through the language's base,
        using the 3x5 dot alphabet. Languages that renounce drawn type
        (swiss, corgi) override with their typographic treatment."""
        base = self.t.get("base", "block")
        if base == "segment":
            base = "block"
        sx, sy = BS.BASE_SCALE.get(base, (1, 1))
        bm = BS.scale(BS.from_font(text.upper(), NA._ALPHA, gap=1), sx, sy)
        return [f"[{self.c['ink']}]{r}[/]" for r in BS.render(bm, base)]

    def empty(self, w: int) -> str:
        """The empty state carries the brand: mascot + this language's voice."""
        rows = self.mascot() if w >= 14 else []
        return "\n".join(rows + [f"[{self.c['dim']}] {self.VOICE['empty']}[/]"])

    # ======================================================================
    # ICONOGRAPHY (COMPONENTS.md axis 4) — one shared vocabulary of domain
    # kinds, one MECHANISM per language. Base (nord): plain ASCII, the
    # terminal-native idiom (htop/lazygit).
    # ======================================================================
    ICONS = {"deadline": "@", "overdue": "!", "wip": "~", "blocked": "x",
             "workday":"$", "boardfile":"#"}

    def icon(self, kind: str) -> str:
        g = self.ICONS.get(kind, "")
        return f"[{self.c['mut']}]{g}[/]" if g else ""

    # ======================================================================
    # DATA-VIZ (axis 7): a sparkline drawn with the language's own QUANTITY
    # mechanism — dispatched on the `meter` token, so the series wears the
    # same family as the meter (dots / braille / hairline / shades / bars).
    # ======================================================================
    def cover_ramp(self) -> str:
        """THE ONE SEAT that says what this language's coverage ramp is.

        **AND EVERY SEAT THAT ASKS THE QUESTION ASKS IT HERE (#45).** Five
        `_meter_*` functions and three of `plot`'s branches used to name a
        `COVER_RAMPS` row directly. That is not a shortcut, it is a second
        answer: a mechanism is REACHED through the `meter` token, so a row
        named inside it is this method's dispatch re-typed by hand, and a
        language that changed mechanism would move its spark and leave its
        meter behind. Byte-identical when it was cured (308 + 120 render
        strings, zero moved) precisely because the two agreed — which is what
        made it hygiene rather than a defect, and is also why nothing but a
        law would ever have kept them agreeing.

        Dispatched on `meter`, like everything else in the data-viz family,
        so a mechanism's ramp is a registry row rather than a literal inside
        each drawing method. `tally` is the one language that BUILDS its
        ramp — a ledger's terminal glyph is the mark it counts with, which
        is a theme token — and that is why this is a method and not a dict
        lookup at the call site.

        THE LEDGER'S UNLIT IS ITS LEADER DOT, and that is where its ramp was
        wrong: `_meter_tally` prints `·` for every position it has not
        counted yet, so the leader is the TRACK — but the ramp had it at
        level 1 and drew air below it. The mark under the terminal is that
        same mark HOLLOW: pencilled in, not posted."""
        mech = self.t.get("meter", "blocks")
        if mech == "tally":
            return "·:▫" + self.t.get("tally", "▪")
        return COVER_RAMPS[METER_RAMP.get(mech, "blocks")]

    def spark(self, series: list[int], w: int, hi: int | None = None) -> str:
        """`hi` is the SHARED ceiling: sibling sparklines must pass the same
        one, or each self-normalizes and the pair is silently incomparable
        (DATAVIZ.md). Tiny nonzero values keep a 1-step floor — a microbar
        must differ from absence in greyscale.

        THE GLYPH IS `coverage_to_glyph`, IN EVERY BRANCH THAT HAS ONE. What
        differs per mechanism below is the TONE, which is a second channel;
        the ramp itself is `cover_ramp()` and no branch names one. The one
        branch with no coverage in it at all is `odometer`, whose quantity is
        a printed FIGURE — see there."""
        c = self.c
        if not series or w <= 0:
            return ""
        pts = _resample(series, w)
        top = hi if hi and hi > 0 else (max(pts) or 1)
        cov = [0.0 if n <= 0 else n / top for n in pts]     # coverage per cell
        lv = [coverage_index(x, 3) for x in cov]            # 4 levels
        mech = self.t.get("meter", "blocks")
        if mech == "odometer":             # DIGITS, never bars: the level is
            # printed on the cell face, so the series is READ rather than
            # estimated and greyscale carries it without help. THE ONE
            # MECHANISM THAT DOES NOT ROUTE — it is asked for a FIGURE, not
            # for a coverage, and it never reaches the ramp at all.
            face = self.t.get("flap")
            on_ = f" on {face}" if face else ""
            return "".join(f"[{(c['ink'] if v else c['dim'])}{on_}]{v}[/]"
                           for v in lv)
        ramp = self.cover_ramp()
        gl = [coverage_to_glyph(x, ramp) for x in cov]
        if mech == "dotgrid":              # the FINE dot scale: a spark is
            # data, so it wears the small sub-cell dots (0-3 per cell) —
            # Nothing mixes dot sizes; the large lattice stays for structure
            return "".join(
                f"[{c['ink'] if v > 1 else (c['mut'] if v else c['dim'])}]"
                f"{g}[/]" for v, g in zip(lv, gl))
        if mech == "braille":              # sub-cell columns
            return "".join(f"[{c['accent'] if v else c['dim']}]"
                           f"{g}[/]" for v, g in zip(lv, gl))
        if mech == "hairline":             # two weights over a BROKEN rule —
            # zero used to be absence here, which is the one thing a data
            # scale may not spend it on (DATAVIZ law 4)
            return "".join(f"[{c['accent'] if v > 1 else c['dim']}]"
                           f"{g}[/]" for v, g in zip(lv, gl))
        if mech == "lcd":                  # segment bars: height + ghost
            s = self.t.get("screen", c["accent"])
            return "".join(f"[{s if v > 1 else c['dim']}]{g}[/]"
                           for v, g in zip(lv, gl))
        if mech in ("decay", "gradient"):  # intensity ramp
            return "".join(f"[{c['accent'] if v else c['dim']}]"
                           f"{g}[/]" for v, g in zip(lv, gl))
        if mech == "step":                 # achromatic grey steps, by SHAPE
            return "".join(f"[{c['mut'] if v else c['dim']}]"
                           f"{g}[/]" for v, g in zip(lv, gl))
        if mech == "dimension":            # the EXTENSION-LINE ladder: a
            # leader dot, a broken line, an extension line, a heavy one. Four
            # SHAPES and not one filled cell — a drawing marks a height, it
            # never blocks it in
            return "".join(
                f"[{c['ink'] if v > 2 else (c['mut'] if v else c['dim'])}]"
                f"{g}[/]" for v, g in zip(lv, gl))
        if mech == "tally":                # a COUNTED series, not a measured
            # one: the ramp climbs in printed WEIGHT (which is a coverage,
            # and routes), from the leader dot the meter leaves on an
            # uncounted position to the tally mark itself. The GROUPS a
            # ledger draws elsewhere are counts and do not route.
            return "".join(f"[{c['ink'] if v > 1 else (c['mut'] if v else c['dim'])}]"
                           f"{g}[/]" for v, g in zip(lv, gl))
        return "".join(f"[{c['accent'] if v else c['dim']}]"
                       f"{g}[/]" for v, g in zip(lv, gl))

    # -- plot: a column chart, h rows tall, in the meter's family -----------
    def plot(self, series: list[int], w: int, h: int = 4,
             hi: int | None = None) -> list[str]:
        """Axis-7, second primitive: a series as h rows of columns, drawn
        with the language's quantity mechanism (same dispatch as meter/spark).
        Nothing's widget sheet is the model — its step counts, screen time and
        week schedule are ALL the same dot lattice: the chart wears the
        language, not a chart library's look. Levels ride on SHAPE (column
        height), never colour alone — the greyscale law applies to data.

        NOT ONE PER-ROW BRANCH DECIDES A LEVEL, and #40d's census is what
        established it. Every branch is handed `v` — the column's height —
        and decides only lit/unlit against its own row index, which is the
        boolean the skill's refusal table already names ("lit/unlit per ROW
        is a boolean, not a coverage"). The LEVEL is decided ONCE per column,
        above the branches, by `coverage_index` — which it used to decide by
        a RE-TYPED COPY of that function in three places. DATAVIZ law 3 names
        exactly that: "nine inline copies are nine chances to lose it, and
        one copy means spending the floor reds this law in every language at
        once." It did not, measured: each copy carried its own `max(1, ...)`,
        so the floor was safe by being in three places rather than by being
        in its seat."""
        c = self.c
        if not series or w <= 0 or h <= 0:
            return []
        series = _resample(series, max(1, w // 2))   # reflow before drawing
        mech = self.t.get("meter", "blocks")
        top = hi if hi and hi > 0 else (max(series) or 1)
        if mech == "braille":
            # columns through the braille base: 4 sub-rows per cell; the
            # unlit lattice stays faintly visible (one ink — braille's cost)
            cells = max(1, w // len(series))
            dh = h * 4
            lv = [coverage_index(v / top, dh) for v in series]
            bm = [[1 if dh - r <= v else 0
                   for v in lv for _ in range(cells * 2)]
                  for r in range(dh)]
            return [f"[{c['accent']}]{row}[/]"
                    for row in BS.render(bm, "braille",
                                         off=self.cover_ramp()[0])]
        per = max(1, w // len(series))
        rows = []
        for r in range(h):
            pos = h - 1 - r                    # 0 = the baseline row
            out = []
            for x in series:
                v = coverage_index(x / top, h)
                if mech == "dotgrid":          # lit dots on the lattice
                    lit = pos < v
                    g = min(int(self.t.get("gap", 1)), max(0, per - 1))
                    cell = (NA.ON if lit else NA.OFF) + " " * g
                    out.append(f"[{c['ink'] if lit else c['dim']}]"
                               f"{cell * max(1, per // (1 + g))}[/]")
                elif mech == "lcd":            # segment stacks with ghosts —
                    # THE SAME TWO GLYPHS `_meter_lcd` DRAWS, from the same
                    # place: the ramp's unlit and its first lit level. This
                    # branch already had the pair right (an unlit stack is
                    # `░░`, never black) and the meter did not; asking the
                    # ONE SEAT is what makes that one definition instead of
                    # two that happen to agree (#40d, the plot half of #45).
                    lit = pos < v
                    r_ = self.cover_ramp()
                    seg = (r_[1] if lit else r_[0]) * 2 + (
                        " " if per > 2 else "")
                    tone = self.t.get("screen", c["accent"]) if lit else c["dim"]
                    out.append(f"[{tone}]{seg * max(1, per // (3 if per > 2 else 2))}[/]")
                elif mech == "hairline":       # the line alone — swiss
                    on = v and pos == v - 1
                    g = ("━" if on else ("─" if pos == 0 else " ")) * per
                    out.append(f"[{c['ink'] if on else c['dim']}]{g}[/]")
                elif mech == "decay":          # bright head, phosphor body
                    if pos < v - 1:
                        out.append(f"[{c['mut']}]{'▓' * per}[/]")
                    elif v and pos == v - 1:
                        out.append(f"[{c['ink']}]{'█' * per}[/]")
                    else:
                        out.append(f"[{c['dim']}]{'░' * per}[/]")
                elif mech == "gradient":       # solid ink, gradient shoulder
                    if pos < v - 1:
                        out.append(f"[{c['accent']}]{'█' * per}[/]")
                    elif v and pos == v - 1:
                        out.append(f"[{c['accent']}]{'▓' * per}[/]")
                    elif pos == v:
                        out.append(f"[{c['dim']}]{'▒' * per}[/]")
                    else:
                        out.append(" " * per)
                elif mech == "boxed":          # block columns on a dot grid
                    lit = pos < v
                    out.append(f"[{c['accent'] if lit else c['dim']}]"
                               f"{('█' if lit else '·') * per}[/]")
                elif mech == "tally":          # printed marks stacked in a
                    # column, standing on a leader-dot baseline — a ledger
                    # counts its columns, it does not fill them
                    mk = self.t.get("tally", "▪")
                    if pos < v:
                        out.append(f"[{c['ink']}]{mk * per}[/]")
                    elif pos == 0:
                        out.append(f"[{c['dim']}]{'·' * per}[/]")
                    else:
                        out.append(" " * per)
                elif mech == "odometer":       # a DIGIT LADDER: the sample's
                    # own figure stands at its height and the cells under it
                    # stay ground. Position ranks the columns, the figure
                    # states the value, and no bar is ever drawn (DATAVIZ law
                    # 5 — position alone is not a reading)
                    face = self.t.get("flap")
                    on_ = f" on {face}" if face else ""
                    if v and pos == v - 1:
                        fig = str(x)
                        if len(fig) > per:
                            fig = "9" * per   # CLIPPED, never clamped
                        out.append(f"[{c['ink']}{on_}]{fig.rjust(per)}[/]")
                    elif not v and pos == 0:
                        out.append(f"[{c['dim']}]{'0'.rjust(per)}[/]")
                    else:
                        out.append(" " * per)
                elif mech == "dimension":      # a DOTTED extension line rising
                    # to the MARK at its measured height. The column is never
                    # filled: on a drawing a height is stated by a mark on a
                    # leader, and the mark is the only ink the sample earns
                    if v and pos == v - 1:
                        out.append(f"[{c['ink']}]{'─' * per}[/]")
                    elif pos < v - 1:
                        out.append(f"[{c['mut']}]{'·' * per}[/]")
                    elif pos == 0:
                        out.append(f"[{c['dim']}]{'·' * per}[/]")
                    else:
                        out.append(" " * per)
                elif mech == "step":           # flat grey columns, a step
                    # baseline, and NO accent — darkside's passive data
                    if pos < v:
                        out.append(f"[{c['mut']}]{'█' * per}[/]")
                    elif pos == 0:
                        out.append(f"[{c['dim']}]{'▁' * per}[/]")
                    else:
                        out.append(" " * per)
                else:                          # blocks: partial-glyph res
                    # the ONE branch of `plot` with a coverage in it: the top
                    # cell of a column is a FRACTION of a cell, which is
                    # exactly what the primitive is for. Every other branch
                    # above decides lit/unlit per ROW — a boolean, not a
                    # coverage — and so does not route.
                    #
                    # AND THE RAMP HERE IS `eighths`, NOT `cover_ramp()`, on
                    # purpose: a fraction of ONE cell needs eight sub-levels
                    # and the language's own ramp has three, so routing this
                    # to the seat would MOVE CELLS (3/8 draws `▃` here and
                    # `▂` there). A refusal named as loudly as the routes.
                    u = coverage_index(x / top, h * 8)
                    full, part = divmod(u, 8)
                    if pos < full:
                        out.append(f"[{c['accent']}]{'█' * per}[/]")
                    elif pos == full and part:
                        g = coverage_to_glyph(part / 8, COVER_RAMPS["eighths"])
                        out.append(f"[{c['accent']}]{g * per}[/]")
                    elif pos == 0:
                        # #40, AND IT WAS ONE BRANCH RATHER THAN THE FOUR THE
                        # item named. Measured across all twelve mechanisms
                        # (`_p62_prove.py` §3): `boxed`, `dotgrid` and
                        # `decay` draw their unlit lattice down the WHOLE
                        # column, six others stand on a baseline, and this
                        # was the only one where a zero column was h rows of
                        # air — `plot([0,0,0,0], …)` in nord drew nothing at
                        # all (DATAVIZ law 4). The mark is the track
                        # `_meter_blocks` draws one row above and the ramp's
                        # own unlit, so the chart's zero and the meter's zero
                        # are one idiom. REACHED ONLY BY A ZERO COLUMN: any
                        # u > 0 lands on `full` or on the partial cell.
                        out.append(f"[{c['dim']}]"
                                   f"{self.cover_ramp()[0] * per}[/]")
                    else:
                        out.append(" " * per)
            rows.append("".join(out))
        return rows

    # -- gauge: a read-only KPI dial — value against its range --------------
    def gauge(self, val: int, lo: int, hi: int, w: int = 10,
              tone: str | None = None, thr: int | None = None) -> str:
        """Track + needle + optional THRESHOLD TICK + readout, in the meter's
        family. The read-only twin of the slider: the slider is input, the
        gauge is a measurement. Laws (DATAVIZ.md): the needle differs from
        the track in GREYSCALE; the tick differs from BOTH; the gauge always
        STATES its value (Nothing prints numerals beside its dot charts —
        the step counter); a zero range never raises."""
        c = self.c
        raw_tone = tone
        tone = tone or c["accent"]
        span = max(1, hi - lo)
        mech = self.t.get("meter", "blocks")

        def pos(x, cells):
            return max(0, min(cells - 1, round((cells - 1) * (x - lo) / span)))

        if mech == "dotgrid":
            g = int(self.t.get("gap", 1))
            cells = max(3, w // (g + 1))
            n, tn = pos(val, cells), (None if thr is None else pos(thr, cells))
            # default needle is INK, not accent — a calm gauge carries no red
            ntone = raw_tone or c["ink"]
            out = []
            for i in range(cells):
                if i == n:
                    out.append(f"[{ntone}]{NA.ON}[/]")
                elif tn is not None and i == tn:
                    # tick in GREY: shape marks it (▝ off-lattice), red is
                    # not spent on a marker — the Nothing ration
                    out.append(f"[{c['mut']}]▝[/]")
                else:
                    out.append(f"[{c['dim']}]{NA.OFF}[/]")
            return (" " * g).join(out) + f" [{c['mut']}]{val}[/]"
        if mech == "lcd":
            segs = max(3, w // 3)
            n, tn = pos(val, segs), (None if thr is None else pos(thr, segs))
            body = []
            for i in range(segs):
                if i == n:
                    body.append(f"[{self.t.get('screen', tone)}]██ [/]")
                elif tn is not None and i == tn:
                    body.append(f"[{c['warn']}]▀▀ [/]")  # top-bar tick segment
                else:
                    body.append(f"[{c['dim']}]▄▄ [/]")
            return "".join(body) + f"[{self.t.get('alu', c['mut'])}]\\[{val:>2}][/]"
        # linear track mechanisms: (track, needle, tick, needle tone, readout)
        LIN = {
            "braille":  ("⠒", "⣿", "⠸", tone, f" [{c['mut']}]{val}[/]"),
            "hairline": ("─", "│", "╷", c["ink"], f"  [{c['mut']}]{val}[/]"),
            "decay":    ("░", "█", "│", c["ink"], f" [{c['mut']}]{val}[/]"),
            "gradient": ("═", "■", "╪", c["warn"], f" [{c['warn']}]{val}[/]"),
            "boxed":    ("·", "▌", "|", tone, f" [{c['mut']}]{val}[/]"),
            "step":     ("─", "O", "╷", c["ink"], f" [{c['mut']}]{val}[/]"),
            "tally":    ("·", self.t.get("tally", "▪"), "|", c["ink"],
                         f"  [{c['mut']}]{val}[/]"),
            # a flap board's gauge is a flap INDICATOR on a dotted track and
            # the figure beside it — never a filled length
            "odometer": ("·", "▼", "|", c["ink"], f" [{c['mut']}]{val}[/]"),
            # a drawing's gauge is an UNMEASURED leader (dots) with the
            # measured point marked by a dimension TERMINATOR, and the
            # threshold by a BREAK. Three shapes, no fill anywhere
            "dimension": ("·", "┤", "╌", c["ink"], f"  [{c['mut']}]{val}[/]"),
        }
        track, needle, tick, ntone, readout = LIN.get(
            mech, ("─", "█", "┼", tone, f" [{c['mut']}]{val}[/]"))
        n, tn = pos(val, w), (None if thr is None else pos(thr, w))
        cells = [(track, c["dim"])] * w
        if mech == "decay":                    # phosphor: the needle trails
            tail = min(n, 3)
            for j, g in enumerate("░▒▓"[3 - tail:] if tail else ""):
                cells[n - tail + j] = (g, c["mut"])
        if tn is not None and tn != n:
            cells[tn] = (tick, self.tick_tone)
        cells[n] = (needle, ntone)
        body = "".join(f"[{t}]{g}[/]" for g, t in cells)
        if mech == "boxed":
            body = f"[{c['dim']}]\\[[/]{body}[{c['dim']}]][/]"
        return body + readout


class Naught(Kit):
    """Everything on one visible dot lattice; quantity is discrete lit dots,
    never a filled bar; the count is a DRAWN 3x5 sprite; no frames at all."""

    DISCLOSE = "◍"                        # a dot with more charge behind it
    DANGER_FORM = ("∙", "∙")               # two lit dots, and not the one red

    @property
    def dot_w(self) -> int:
        return int(self.t.get("dot_w", 2))

    @property
    def gap(self) -> int:
        """Lattice PITCH: cells of air between dots. 0 = dense LED panel —
        the round pixel carries its own air (user: gap-1 felt too sparse)."""
        return max(0, int(self.t.get("gap", 1)))

    @property
    def lattice(self) -> bool:
        """The `layout` token: "lattice" composes the BOARD on the visible dot
        grid — the head's count is a drawn 3x5 sprite standing on unlit dots,
        the card's gap is closed by dot leaders, and the card's second row
        rides the lattice. Anything else (the base default "flow") lets the
        cards stand on the ground as plain typographic rows. Same dispatch
        shape as darkside's rail and ledger's ruling, so the composition
        belongs to the TOKEN and not to the class name — the dots that carry
        QUANTITY (the dotgrid meter, the calendar, the icons) answer to their
        own tokens and stay."""
        return self.layout == "lattice"

    def tcss(self) -> str:
        # drawn count sprites make the head a 5-row region
        return super().tcss() + "\n.col-head { margin-bottom: 0; }"

    def surface(self):
        # pure black IS the surface — plus ONE texture block: the meter
        # panel wears a faint cross-hatch (a texture swatch reads as denser
        # pixels; kept near-black so it grounds, never competes)
        return (".kb-col { background: #000000; }\n"
                ".kb-card { background: #000000; }\n"
                "#meter { hatch: cross #101010 35%; }")

    def composition(self):
        # a grid of small WIDGETS on black — the Nothing home screen: the
        # meter is its own panel BESIDE the hero, not a strip under it
        return """
        Screen.sz-board #top { layout: horizontal; height: 11; }
        Screen.sz-board #top #hero { width: 1fr; }
        Screen.sz-board #top #meter { width: 32; height: auto;
                                      margin-top: 1; margin-left: 2; }
        """

    def head(self, name: str, count: int, w: int, idx: int = 0) -> str:
        if not self.lattice:
            return super().head(name, count, w, idx)
        c = self.c
        cap = f"[{c['mut']}]{name.upper()[:max(1, w - 1)]}[/]"
        # the count as a 3x5 dot sprite on its own visible lattice — the
        # "count chips as dot columns" commitment. THE STROKE (user verdict
        # 2026-07-27: the drawn letters read "hard to read, somewhat
        # separated"): the sprite stands on the CONTINUOUS lattice, so its
        # letters are parted by unlit dots and never by blank cells, and its
        # pixel is x2 — every stroke two cells wide, the 1:2 cell aspect
        # given back. This is the seat the user actually reads; the hero's
        # dense type is the same mechanism at a seat no row budget reaches.
        # PROGRESSIVE, because a sprite wider than its column would WRAP and
        # cost the board a whole card row: x2 where the column pays for it,
        # x1 (the width the sparse form already had) where it does not.
        digits = str(min(99, count))
        dw = max(1, self.dot_w)
        sx = 2 if NA.plain_width(digits, dw, self.gap, 2, True) <= w - 1 else 1
        rows = NA.label(digits, c["ink"] if count else c["dim"], c["dim"],
                        dot_w=dw, gap=self.gap, sx=sx, fill=True)
        rule = self.rule_line(w)
        return "\n".join([cap] + rows + ([] if rule is None else [rule]))

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        if not self.lattice:
            return super().card_row(title, chip, tone, w, idx, urgent)
        c = self.c
        dot = f"[{tone if urgent else c['dim']}]{NA.ON if urgent else NA.OFF}[/] "
        room = max(1, w - len(chip) - 4)
        body = _fit(title, room)
        # dot leaders keep the row on the lattice instead of blank cells
        unit = NA.OFF + " " * self.gap
        lead = unit * ((room - min(len(title), room)) // len(unit) + 1)
        lead = lead[: max(0, room - min(len(title), room))]
        return (dot + f"[{c['ink']}]{body}[/][{c['dim']}]{lead}[/] "
                f"[{tone}]{chip}[/]")

    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        if not self.lattice:
            return super().card_rows(title, chip, tone, w, idx, urgent, meta)
        # row 2 stays ON THE LATTICE: phase progress as lit dots (the drawn
        # 3x5 sprite needs 5 rows — at 2 rows the honest form is the dot
        # meter), plus the state as the language's 2-dot icon
        top = self.card_row(title, chip, tone, w, idx, urgent)
        m = meta or {}
        c = self.c
        n = max(1, min(int(m.get("n_phases", 4)), max(1, (w - 8) // 2)))
        pi = max(0, int(m.get("phase_idx", 0)))
        dots = " ".join(
            f"[{c['ink'] if i <= pi else c['dim']}]"
            f"{NA.ON if i <= pi else NA.OFF}[/]" for i in range(n))
        state = ("blocked" if m.get("blocked")
                 else "overdue" if (m.get("days") is not None
                                    and m["days"] < 0 and not m.get("done"))
                 else "wip")
        return [top, f"  {dots}  {self.icon(state)}"]

    def tile_row(self, val, label, tone, w):
        c = self.c
        return (f"[{tone}]{NA.ON}[/] [{tone}]{val}[/] "
                f"[{c['mut']}]{label[: max(0, w - len(val) - 4)]}[/]")

    def field_row(self, caption, value, w):
        """THE LATTICE IS THE GROUND, so the row's remainder is DRAWN.

        This language has one structure device and it is the grid: "the unlit
        grid is visible -- dark dots render in the dim tier rather than as
        spaces.  That faint lattice IS the signature."  So a definition row
        neither RULES a leader between two marks nor flushes a column: it is
        DENSE (the figure sits beside the name, which is what "dense" means
        when it is a commitment and not an adjective) and what follows is
        lattice, unlit.

        THE FILL IS AFTER THE VALUE AND NEVER BETWEEN, and that is the exact
        structural difference from ledger's leaders: a leader CONNECTS two
        marks, a lattice is a GROUND that was already there.  The charge says
        the rest -- the name unlit, the figure lit."""
        c = self.c
        cap, val = str(caption), str(value)
        room = max(0, w - len(cap) - len(val) - 2)
        return (f"[{c['dim']}]{mark(cap)}[/] [{c['ink']}]{mark(val)}[/] "
                f"[{c['dim']}]{NA.OFF * room}[/]")

    def sect(self, title, note, w, h=0):
        c = self.c
        # DISPLAY TYPE: the title drawn on the lattice in the 3x5 dot
        # alphabet — the same mechanism as the head counts and the wordmark —
        # when the surface's row budget affords its 5 rows. Same progressive
        # stroke as the head: x2 where the measure pays for it, x1 where it
        # does not, and type where even that would not fit.
        if h >= 16:
            for sx in (2, 1):
                if NA.plain_width(title, 1, self.gap, sx, True) <= w - 2:
                    return (NA.label(title, c["ink"], c["dim"], dot_w=1,
                                     gap=self.gap, sx=sx, fill=True)
                            + [f"[{c['mut']}]{note}[/]", ""])
        lattice = ((NA.OFF + " " * self.gap) * w)[: max(1, w - 1)]
        return [f"[{c['ink']}]{title}[/]  [{c['mut']}]{note}[/]",
                self.rule_line(w) or f"[{c['dim']}]{lattice}[/]"]

    def bar(self, span, head=None, tone=None):
        # discrete dots with the lattice rhythm; the packet BRIGHTENS one dot.
        # Default is INK — red arrives only when a caller passes an alarm tone
        c = self.c
        tone = tone or c["ink"]
        pitch = self.gap + 1
        out = []
        for i in range(span):
            if self.gap and i % pitch:     # the rhythm gap between dots
                out.append(" ")
            elif head is not None and head[i]:
                out.append(f"[{c['mut']}]{NA.ON}[/]")
            else:
                out.append(f"[{tone}]{NA.ON}[/]")
        return "".join(out)

    GANTT = ("◦", "∙", "│", " ", "∙")      # lit dot travels the round lattice

    def cal_cell(self, state):
        c = self.c
        # red ONLY on the overdue day — the Nothing calendar's exact ration
        return {"none": f"[{c['dim']}]{NA.OFF} [/]",
                "over": f"[{c['alert']}]{NA.ON} [/]",
                "multi": f"[{c['ink']}]{NA.ON} [/]",
                "one": f"[{c['mut']}]{NA.ON} [/]"}[state]

    def queue_marker(self, i):
        return f"[{self.c['dim']}]{NA.OFF}[/]"

    # icons are 2-dot lattice patterns — ROUND, everything stays on the grid
    ICONS = {"deadline": "∙◦", "overdue": "∙∙", "wip": "◦∙", "blocked": "◦◦",
             "workday":"∙ ", "boardfile":"◦ "}

    # Nothing's toggle is a FILL INVERSION, never a knob (the widget sheet:
    # active pill = solid, off = outline). State = lit vs unlit lattice —
    # monochrome: the shape channel carries it, red is not spent here.
    # THE ROUND PIXEL AT FULL BRIGHTNESS (inc45). This read `NA.ON`, the same
    # lit dot as `LEVELS["warn"]`'s first cell, `LEVELS["error"]`'s two, the
    # `DANGER_FORM` and (until this increment) `REQUIRED` -- five meanings on
    # one pixel. THE LADDER KEEPS THE LIT DOT, because "quantity is a row of
    # discrete lit dots ... how many are lit is the signal" is the first line
    # of this language's own entry and the ladder is that sentence; what moves
    # is everything that is NOT a count. The charge ramp `⋅ · ◦ ∙ ◉ ●` is
    # already declared across `PART_GLYPHS`, so position takes its brightest
    # rung -- where the current is, which is the argument operator ruling 4
    # accepted for this language's overlay.
    CUR = "●"

    @property
    def SPIN(self):                        # dot chase at the lattice pitch
        g = " " * self.gap
        return tuple(g.join(NA.ON if j == i else NA.OFF for j in range(4))
                     for i in range(4))

    # the value family on the lattice: every part is a ROUND dot, and the
    # knob is a dot with an EYE — the old knob was the lit dot in a brighter
    # grey, which is a colour-only knob, and at value 0 there was no knob on
    # the screen at all (COMPONENTS.md's 2-channel law, failed twice).
    def overlay_instead(self, rows, w, h, under):
        """THE LATTICE CHARGE (operator ruling 4), and no overlay at all.

        "No frames at all" is one of four commitments, so there is no box to
        draw and no scrim to lay: what this language has is CHARGE. The page
        keeps every dot it had and loses its charge -- "the unlit grid is
        visible; dark dots render in the dim tier rather than as spaces" --
        and the question is the only region left lit, bounded above and below
        by the lattice at full charge.

        So the separation is not a mark added in front of the page. It is the
        same lattice, at two charges, and the question is where the current
        is."""
        c = self.c
        band = ([f"[{c['ink']}]{NA.ON * w}[/]"] + list(rows)
                + [f"[{c['ink']}]{NA.ON * w}[/]"])
        y = max(0, (h - len(band)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(band):
                out.append(band[i - y])
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out

    # THE PANE SEAT IS THE LATTICE, ONE CHARGE DOWN. "No frames at all"
    # forbids a rule and does not forbid this, because the lattice is not a
    # frame — it is the GROUND, and it was already under both panes before
    # either was drawn. What divides them is a column where the ground stays
    # UNLIT while the panes are lit: the argument operator ruling 4 accepted
    # for this language's overlay, where the separation is charge, not a box.
    # `field_row` fills a row's remainder with the same unlit dot. One ground,
    # two components.
    PANE_RULE = NA.OFF

    # THE VALIDATION ROW, in the lattice. The remainder is the UNLIT ground
    # this language draws everywhere else (`field_row`, `pane_split`), and
    # the mark is two dots at full charge -- the ladder's top rung, already
    # declared. Nothing rations `alert` here, so the tier is the base's.
    ERROR_FILL = NA.OFF
    # THE LIT DOT WITH A RING OF CHARGE STILL AROUND IT (inc45). This read
    # `NA.ON` under "full charge means the seat must carry a value", and the
    # census answered it: one lit dot was `LEVELS[error]`'s cell, the
    # `DANGER_FORM`, the `REQUIRED` mark AND the `CUR` -- the widest single
    # cell in the corpus by family count, and naught had no frame among the
    # sixteen to say so.
    #
    # THE LADDER IS A CHARGE RAMP AND IT WAS ALREADY DECLARED. `⋅ · ◦ ∙ ◉ ●`
    # is this language's own vocabulary, spent across `PART_GLYPHS` from the
    # faintest lattice dot to the pressed key; `◉` is the rung the knob wears
    # ("a dot with an EYE") and the caret wears ("the one LIT dot in the
    # lattice"). Obligation takes the tier ABOVE the plain lit dot the cursor
    # spends, so the two are distinct on the one channel this language
    # declares -- LANGUAGES.md §0, "quantity is a row of discrete lit dots
    # ... HOW MANY ARE LIT is the signal". Charge, not position.
    REQUIRED = "◉"

    LEVELS = {"info": "◦◦", "warn": "∙◦", "error": "∙∙"}

    MATCH_STYLE = "bold {ink}"             # full charge, and no second red

    def keyhint(self, pairs, w=0):
        """The lattice's own bullet between the key and what it does."""
        c = self.c
        return "   ".join(f"[{c['ink']}]{mark(str(k))}[/]"
                          f"[{c['dim']}]{NA.ON}[/]"
                          f"[{c['mut']}]{mark(str(v))}[/]"
                          for k, v in pairs)

    PART_GLYPHS = {
        "main": {DEFAULT: NA.OFF, DISABLED: "·"},
        "indicator": {DEFAULT: NA.ON, DISABLED: NA.OFF},
        "knob": {DEFAULT: "◉", FOCUSED: "◍", EDITED: "◎",
                 ACTIVE: "●", INVALID: "◑",
                 DISABLED: "◌"},
        # THE LATTICE HAS NO CHROME, so this checkbox has no box — ONE dot,
        # hollow or inked. The renunciation is deliberate and it has a
        # measured cost: the containment law ("the mark cannot escape its
        # box") degrades here to span-equality, because a one-cell box has no
        # interior to keep the mark inside of. Wrapping the dot in brackets
        # to satisfy a law would be drawing another language's checkbox.
        "checkbox.main": {DEFAULT: "◦", FOCUSED: "○", ACTIVE: "◌",
                          DISABLED: "·"},
        "checkbox.knob": {DEFAULT: "◉", FOCUSED: "●", ACTIVE: "◍",
                          DISABLED: "◎"},
        # THE ONE LANGUAGE THAT CANNOT AFFORD THE ROUND-VS-SQUARE
        # DISTINCTION, and saying so is the point. Nine languages separate a
        # radio from a checkbox by SHAPE FAMILY — round well, square box.
        # naught's entire vocabulary is the lattice dot: both are round
        # because everything here is round, so the distinction it can afford
        # is WITHIN the family — the checkbox is a dot filled, the radio is a
        # ring with a centre. The per-state pair still differs from the
        # checkbox's in every state, which is the law; the family does not,
        # which is the honest reading.
        "radio.main": {DEFAULT: "○", FOCUSED: "◌", ACTIVE: "◦",
                       DISABLED: "⋅"},
        "radio.knob": {DEFAULT: "⊙", FOCUSED: "⊚", ACTIVE: "●",
                       DISABLED: "⊗"},
        # the key is a LATTICE seat: unlit dots hold the word, and lighting
        # them is the whole language's mechanism. The press fills all four —
        # the round pixel at full brightness, no red anywhere (the ration).
        "button.main": {DEFAULT: "◦  ◦", FOCUSED: "○  ○", ACTIVE: "●●●●",
                        DISABLED: "⋅  ⋅"},
        # A LATTICE SEAT: unlit dots hold the field open and the paper IS the
        # lattice. EDITED tightens the weave, because that is the state the
        # words are landing in.
        "textfield.main": {DEFAULT: "◦·◦", FOCUSED: "○·○", EDITED: "○∙○",
                           ACTIVE: "●·●", INVALID: "◑·◑",
                           DISABLED: "⋅⋅⋅"},
        # the one LIT dot in the lattice — naught marks by lighting, never by
        # colour, and the red ration reaches this seat through the actuator
        "textfield.caret": {DEFAULT: "◉"},
        # THE DOT COLUMN, which is the mechanism the skill names for this
        # language and it is the lattice doing what it already does: the
        # shaft is the lattice at its faintest pitch and the view is the run
        # of pixels at FULL SIZE. Position and extent on one channel — dot
        # size — because that is the only channel this language has and it
        # has never needed a second.
        "scrollbar.main": {DEFAULT: "·", DISABLED: "⋅"},
        "scrollbar.indicator": {DEFAULT: "●", DISABLED: "◦"},
        # THE LANGUAGE THAT CANNOT DRAW AN ARROW, and saying so is the point
        # again. Nine languages point their steps; this vocabulary is one
        # round pixel at a size, and a chevron would be another language's
        # mark. So the DIRECTION is carried by the SEAT — the step on the
        # left is the step back — and the pixel carries the state, which is
        # what this lattice has always done. The end is a dot going out: at a
        # clamped floor the left seat drops to the unlit lattice and the eye
        # reads a wall, not a colour.
        "stepper.main": {DEFAULT: "··", DISABLED: "⋅⋅"},
        "stepper.step": {DEFAULT: "●●", FOCUSED: "○○", EDITED: "◍◍",
                         ACTIVE: "◉◉", INVALID: "◑◑",
                         DISABLED: "◌◌"},
    }

    def part_tone(self, part, state, name=None):
        """THE RATION OVERRULES THE BASE GRIP RULE, and this language's own
        test is what settled it. The base spends `accent` on a knob under
        interaction; naught's accent IS red and red is reserved for alerts,
        and a knob under the finger is not an alert. The switch's ACTIVE
        flip frames are the first cell where the two rules met, and the calm
        surface went red the moment they did.

        Nothing is lost: the knob's five SHAPES (◉ ◍ ◎ ● ◌) carry the state
        on their own, which is the two-channel law satisfied on the channel
        this language can actually afford.

        It asks the ACTUATOR now, so the ration reaches the button too — whose
        grip is its own ground, and which would otherwise have put red back on
        a calm surface the moment a button was focused."""
        if part == actuator(name) and control_of(state) != DISABLED:
            return self.c["ink"]
        return super().part_tone(part, state, name)

    @property
    def SLOT_SEP(self) -> str:
        return " " * self.gap

    def spinner(self, tick):
        return f"[{self.c['ink']}]{self.SPIN[tick % len(self.SPIN)]}[/]"

    # the lattice fills dot by dot — discrete, no easing. THREE steps, not
    # two: at three slots a two-step flip lands the knob on the same cell
    # twice and spends a tick showing the same frame (the pairwise-distinct
    # law caught it).
    MOTION_STEPS = 3

    def tabs(self, options, active):
        c = self.c
        out = []
        for o in options:
            dot = NA.ON if o == active else NA.OFF
            tone = c["ink"] if o == active else c["mut"]
            out.append(f"[{c['ink'] if o == active else c['dim']}]{dot}[/] "
                       f"[{tone}]{o.upper() if o == active else o}[/]")
        return "  ".join(out)

    # ------------------------------------------------------------------
    # IDENTITY with a JOB (user verdict: the generic mascot was "sin fondo
    # y sentido"). Nothing's dot-face reads DEVICE state; this one reads
    # the BOARD: clear (nothing overdue) · busy (open work) · alert
    # (something overdue). Ground = the unlit lattice behind it; the alarm
    # is carried by SHAPE (the expression), not by red.
    # ------------------------------------------------------------------
    FACES = {
        "clear": (".........",
                  "..#...#..",
                  ".........",
                  ".#.....#.",
                  "..#####.."),
        "busy":  (".........",
                  "..#...#..",
                  ".........",
                  "..#####..",
                  "........."),
        "alert": ("..#...#..",
                  ".........",
                  "...###...",
                  "..#...#..",
                  "...###..."),
    }

    def face(self, mood: str | None = None) -> list[str]:
        c = self.c
        g = " " * self.gap
        mask = self.FACES.get(mood or self.mood, self.FACES["clear"])
        return ["".join(
            f"[{c['ink']}]{NA.ON}{g}[/]" if ch == "#" else
            f"[{c['dim']}]{NA.OFF}{g}[/]" for ch in mr).rstrip()
            for mr in mask]

    def mascot(self):
        return self.face()

    def wordmark(self, text):
        # drawn through the LATTICE alphabet — round dots, never block slabs
        c = self.c
        return NA.label(text, c["ink"], c["dim"], dot_w=1, gap=self.gap)


class Corgi(Kit):
    """Teenage-Engineering grammar: hairline aluminium rules with square
    junctions, numbered functional params, all-caps letterspaced labels,
    quantity as LCD SEGMENT BARS (the mark is a bar, not a dot).

    The board is ONE FULL-WIDTH MODE SURFACE (`layout="strip"`): a numbered
    MODE STRIP names every mode and lights the one on screen, and under it the
    board mode is a single spec sheet — full-width numbered param rows whose
    values stand in engraved slots that align down the whole page. Under any
    other `layout` the previous 3-column composition comes back byte for byte
    (`_flow_*`)."""

    DISCLOSE = "▄"                        # the bank below the segment
    # THE SEGMENT DRIVEN ALL THE WAY, and it is the TOP rung (inc45). This
    # read `("▄", "▄")` -- "the key's shoulders swollen, engraved" -- and `▄▄`
    # is `LEVELS["warn"]`, so a destructive key and a warning row were the
    # same cell at the MIDDLE of the ladder. corgi has no frame among the
    # sixteen; the law found it, not the round. `██` is `LEVELS["error"]`, and
    # a danger form that is the ladder's TOP rung set around the label is one
    # claim about one gravity rather than two -- the same seat naught, prism
    # and blueprint already spend theirs on.
    DANGER_FORM = ("█", "█")               # the segment driven to full height

    # ======================================================================
    # THE PARAM STRIP. Every cell position below is computed in ONE place
    # (`slots()`), which the renderer AND every acceptance check read — the
    # `Ledger.cols` / `Swiss.grid` / `Nord.panes` / `Instrument.reticle`
    # precedent, so "every row's values stand in the same cells" is true by
    # construction rather than by coincidence.
    # ======================================================================
    # WHICH PARAMS, and the one that was DELETED. The flow sub-row printed
    # DUE / PH / PR. `PH` is gone here and its absence is the point: under a
    # SECTIONS board the phase is stated by the section head one row above,
    # so `PH BACKLOG` on every row of the BACKLOG section is a CONSTANT — the
    # exact defect the trace pass named in instrument's sub-row. `ST` takes
    # its cells and varies (a blocked task inside DOING reads BLK beside its
    # open siblings). The right-flushed chip is gone too: it said `3d` / `blk`
    # / `done`, which DUE and ST now state in engraved slots instead of in a
    # free position, so no field was lost when the card lost a row.
    PARAMS = (("DUE", 4), ("PR", 4), ("ST", 4))   # (engraved code, value w)
    NUM_W = 4            # the row's `[n] ` param number — TE numbers its rows
    SLOT_GAP = 2         # air between engraved slots. Air is the separator:
                         # a rule glyph here would be `Ledger.RULE_V` (`│`),
                         # whose dispatch check ("money-column rules render
                         # IFF layout=ruled") is what caught instrument
                         # borrowing a divider. Alignment is corgi's grid.
    TITLE_MIN = 24       # the narrowest measure that still holds a task title
                         # intact (swiss's MEASURE_MIN, measured on the same
                         # seeded fixture: its titles run 19-24 characters).
    # The strip's own ceiling. `#tabs` is `width: 1fr` inside `#ap`'s
    # `padding: 1 2`, so its narrowest live seat is the widget class at 46
    # screen cells => 42 (measured at 46/50/60/79/80/96/118). The full strip
    # comes out at 41 for the app's four modes — ONE cell of headroom, which
    # is exactly why the tier ladder below exists rather than a comment.
    STRIP_MAX = 42
    LIT = "▄"            # the tight tier's lit-segment mark. Tier 1 spends
                         # letterspacing on the active mode and cannot afford
                         # this glyph too; tier 2 spends the glyph instead.
                         # Either way the active mode carries a channel that
                         # survives greyscale, never colour alone.

    @property
    def alu(self) -> str:
        return self.t.get("alu", self.c["mut"])

    @property
    def screen(self) -> str:
        return self.t.get("screen", self.c["accent"])

    @property
    def striped(self) -> bool:
        """The `layout` token, dispatched — the same shape as darkside's
        `rail_width`, naught's `lattice` and instrument's `traced`. A
        hardcoded mode strip would make the token dead metadata again
        (PENDING item 0)."""
        return self.layout == "strip"

    @property
    def rule_color(self) -> str:
        return self.alu                    # TE rules are aluminium, always

    def display_chrome(self) -> tuple[str, str, str]:
        """The DISPLAY posture's own frame and glass. Square junctions — TE
        has no rounded corners anywhere, and the display is not the exception
        — and the glass is the SAME green-black `surface()` already puts under
        the hero and the meter, so the raster region lands on the screen this
        language already declared rather than on a second one."""
        return self.DISPLAY_BOX, "#0a120a", self.screen

    def surface(self):
        # the DISPLAY REGION: machine output lives on green-black glass
        return (super().surface()
                + "\n#hero { background: #0a120a; }"
                + "\n#meter { background: #0a120a; }")

    def board_layout(self):
        # "each mode takes over the screen": the board mode is ONE surface,
        # not three scrolling columns. Measured on the seeded fixture at
        # 80x30 — the columns board cut EVERY title ("RENEW TLS CERTIF…3d")
        # and had room for two of the four params; the spec sheet prints all
        # seven backlog titles intact with all three.
        return "sections" if self.striped else super().board_layout()

    def composition(self):
        if not self.striped:
            return self._flow_composition()
        # THE MODE SURFACE TAKES THE SCREEN, and it is paid for out of dead
        # air rather than out of the hero. Two changes, both derived from the
        # same argument — on a TE panel the HAIRLINE is the separator, so a
        # blank row above a rule is a separator drawn twice:
        #   * every module that carries a `border-top` gives up its
        #     `margin-top` (measured: the board region goes 9 rows -> 12 at
        #     30 screen rows, +33%, and that is what lets one section print
        #     all seven of its rows);
        #   * `.col-head` gives up its `margin-bottom` for the same reason —
        #     the head's own aluminium rule already separates it from the
        #     rows under it (instrument's "the reticle pays for itself").
        # `#tabs` is the one module that GAINS a row, and that is a defect
        # fix, not a cost: `widget.tcss` gives it `height: 1` and this
        # composition puts a `border-top` on it, so the border ate the
        # widget's only content row and corgi's tab strip rendered NOWHERE at
        # any size (measured on the 118x30 frame — `[1] B O A R D` was in the
        # renderable and on no screen row). Height 2 = the rule + the strip.
        return """
        #meter { border-top: solid #9a9a9a; margin-top: 0; }
        #tabs { border-top: solid #9a9a9a; margin-top: 0; height: 2; }
        #tiles { border-top: solid #9a9a9a; margin-top: 0; }
        Screen.sz-board #tiles { height: 2; }
        #view { border-top: solid #9a9a9a; margin-top: 0; }
        #kb { border-top: solid #9a9a9a; margin-top: 0; }
        .col-head { margin-bottom: 0; }
        """

    def _flow_composition(self):
        # numbered MODULES divided by aluminium spec-sheet rules
        return """
        #meter { border-top: solid #9a9a9a; }
        #tabs { border-top: solid #9a9a9a; }
        #tiles { border-top: solid #9a9a9a; }
        Screen.sz-board #tiles { height: 2; }
        #view { border-top: solid #9a9a9a; }
        #kb { border-top: solid #9a9a9a; }
        """

    VOICE = {"empty": "\\[0] NO TASKS", "no_signals": "\\[!] NO SIGNAL SOURCES"}

    def head(self, name, count, w, idx=0):
        c = self.c
        num = f"[{c['accent']}]\\[{idx + 1}][/] " if self.numbered else ""
        cap = " ".join(name.upper()[: max(1, (w - 8) // 2)])
        line = (num + f"[{c['ink']}]{cap}[/] "
                f"[{self.screen if count else c['dim']}]{count:>2}[/]")
        rule = self.rule_line(w)
        return line if rule is None else line + "\n" + rule

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        c = self.c
        num = (f"[{self.alu}]\\[{idx + 1}][/]" if self.numbered
               else f"[{self.alu}]│[/]")
        used = 4 if self.numbered else 2
        room = max(1, w - len(chip) - used - 1)
        body = _fit(title.upper(), room)
        pad = " " * max(0, room - min(len(title), room))
        return f"{num} [{c['ink']}]{body}[/]{pad}[{tone}]{chip}[/]"

    def slots(self, w: int) -> list[tuple[int, str, int]]:
        """(origin, engraved code, value width) per param slot on a row of `w`
        content cells — right-flushed, so every row on the page shares one
        geometry and the values read down as columns.

        THE DROP RULE, derived from the constants rather than tabulated: take
        the declared params and, while the title measure would come out under
        `TITLE_MIN`, RENOUNCE the rightmost one — never crush it, never wrap
        it. With every slot renounced there is no strip left, `[]` comes back,
        and the caller falls to the two-row flow card, which is the form the
        strip replaced and can therefore never be worse than it (swiss's grid
        law). The thresholds fall straight out: 56 cells for all three, 47 for
        DUE+PR, 38 for DUE alone."""
        for n in range(len(self.PARAMS), 0, -1):
            fields = self.PARAMS[:n]
            block = (sum(len(lab) + 1 + vw for lab, vw in fields)
                     + self.SLOT_GAP * (n - 1))
            if w - self.NUM_W - self.SLOT_GAP - block >= self.TITLE_MIN:
                out, x = [], w - block
                for lab, vw in fields:
                    out.append((x, lab, vw))
                    x += len(lab) + 1 + vw + self.SLOT_GAP
                return out
        return []

    def _param_values(self, meta: dict) -> dict[str, str]:
        m = meta or {}
        d = m.get("days")
        return {"DUE": "--" if d is None else f"{d}D",
                "PR": (m.get("prio") or "-").upper(),
                "ST": ("DONE" if m.get("done")
                       else "BLK" if m.get("blocked") else "OPEN")}

    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        if not self.striped:
            return self._flow_card_rows(title, chip, tone, w, idx, urgent,
                                        meta)
        sl = self.slots(w)
        if not sl:
            return self._flow_card_rows(title, chip, tone, w, idx, urgent,
                                        meta)
        c = self.c
        vals = self._param_values(meta or {})
        room = max(1, sl[0][0] - self.NUM_W - self.SLOT_GAP)
        body = _fit(title.upper(), room)
        pad = " " * max(0, room - min(len(title), room))
        # the SEVERITY lands on the reading, not on a free-floating chip: DUE
        # is the only param whose value carries a meaning outside the sheet.
        # `numbered` still gates the row number here — the strip is a NEW
        # composition, not a licence to stop reading a token the rest of the
        # language reads. Unnumbered, the slot stays as INDENT: the title
        # column must not shift, or the page loses the alignment it is for.
        num = (f"[{self.alu}]\\[{idx + 1}][/] " if self.numbered
               else " " * self.NUM_W)
        parts = [f"{num}[{c['ink']}]{body}[/]{pad}" + " " * self.SLOT_GAP]
        tones = {"DUE": tone, "PR": c["mut"], "ST": self.screen}
        for i, (_, lab, vw) in enumerate(sl):
            gap = " " * (self.SLOT_GAP if i + 1 < len(sl) else 0)
            parts.append(f"[{self.alu}]{lab}[/] "
                         f"[{tones[lab]}]{vals[lab][:vw].ljust(vw)}[/]{gap}")
        return ["".join(parts)]

    def _flow_card_rows(self, title, chip, tone, w, idx=0, urgent=False,
                        meta=None):
        # the spec-sheet line: engraved 2-letter codes in aluminium, values
        # on the screen-green display — a TE param row, not a subtitle
        top = self.card_row(title, chip, tone, w, idx, urgent)
        m = meta or {}
        c = self.c
        d = m.get("days")
        due = "--" if d is None else f"{d}D"
        ph = (m.get("phase") or "--")[:7].upper()
        pr = (m.get("prio") or "-")[:1].upper()
        sub = _fit_parts([
            ("    ", "    "),
            (f"[{self.alu}]DUE[/] [{self.screen}]{due:<4}[/]", f"DUE {due:<4}"),
            (f"[{self.alu}]PH[/] [{c['ink']}]{ph}[/] ", f"PH {ph} "),
            (f"[{self.alu}]PR[/] [{c['mut']}]{pr}[/]", f"PR {pr}"),
        ], w)
        return [top, sub]

    def tile_row(self, val, label, tone, w):
        c = self.c
        room = max(0, w - len(val) - 3)
        return (f"[{self.screen}]{val}[/] [{self.alu}]│[/]"
                f"[{c['mut']}]{label.upper()[:room]}[/]")

    def field_row(self, caption, value, w):
        """THE SILKSCREEN BESIDE THE READOUT -- no leader, no right column.

        A panel does not rule a line from a legend to its display; it PRINTS
        the legend where the display is.  So the label is engraved in the
        aluminium register and the figure stands in the glass immediately
        after it, left-packed, and the rest of the row is bare panel.

        THE LABEL IS LETTERED IN CAPITALS AND THE FIGURE IS NOT TOUCHED --
        this language's legends are engraved and its readouts are driven, and
        those are two registers on one object.  `tile_row` already draws that
        asymmetry; this row inherits it rather than inventing a second rule.

        AND IT IS NOT NUMBERED (L-33, operator ruling 3): the numbers are the
        parameter keymap, and a caption is a name, not a key."""
        cap, val = str(caption).upper(), str(value)
        room = max(0, w - len(cap) - len(val) - 1)
        return (f"[{self.alu}]{mark(cap)}[/] [{self.screen}]{mark(val)}[/]"
                + " " * room)

    def sect(self, title, note, w, h=0):
        # drawn type RENOUNCED: TE prints and engraves, it does not draw
        c = self.c
        head = (f"[{c['accent']}]\\[{title[0]}][/] [{c['ink']}]"
                f"{' '.join(title)}[/]  [{c['mut']}]{note.upper()}[/]")
        return [head, self.rule_line(w) or ""]

    def bar(self, span, head=None, tone=None):
        tone = tone or self.screen
        out = []
        for i in range(span):
            if i % 3 == 2:
                out.append(" ")
            elif head is not None and head[i]:
                out.append(f"[{self.c['ink']}]▄[/]")
            else:
                out.append(f"[{tone}]▄[/]")
        return "".join(out)

    GANTT = ("▄", "█", "│", "·", "▌")

    def cal_cell(self, state):
        c = self.c
        return {"none": f"[{c['dim']}]▄▄[/]",
                "over": f"[{c['alert']}]▄▄[/]",
                "multi": f"[{self.screen}]▄▄[/]",
                "one": f"[{c['accent']}]▄▄[/]"}[state]

    # TE prints LABELS, not pictograms: engraved 2-letter codes in aluminium
    ICONS = {"deadline": "DL", "overdue": "OV", "wip": "WF", "blocked": "BL",
             "workday":"BD", "boardfile":"FS"}

    def icon(self, kind):
        g = self.ICONS.get(kind, "")
        return f"[{self.alu}]{g}[/]" if g else ""

    # a hardware toggle with a PRINTED label — state is written, not implied
    CUR = "▐"
    SPIN = ("▀", "▐", "▄", "▌")            # segment sweep: bars, not dots

    # the hardware toggle's PRINTED label survives as the declared word —
    # this language states every reading in figures beside the control
    CHECK_WORDS = ("--", "ON")

    # LCD segments: the reading rides on segment HEIGHT, not on lit-vs-ghost.
    # The old slider drew the SAME `▄▄` for the passed segments and the
    # remaining ones and separated them by hue alone — greyscale it and the
    # value disappeared (DATAVIZ.md's note on LCD sparks, exactly).
    SLOT_SEP = " "
    def overlay_instead(self, rows, w, h, under):
        """THE MODE TAKES OVER THE SCREEN, so there is nothing behind.

        "No persistent navigation chrome; its answer to smallness is FEWER
        THINGS AT ONCE." A dialog floating over a board is two modes at once,
        which is the thing this language is built against -- so a confirm is
        a MODE, and the board is not dimmed, it is GONE.

        The backdrop argument is accepted and dropped on purpose, and that is
        the refusal: a panel does not show you the screen you left.

        CENTRED, because a mode is not a dialog that lost its box: it is the
        whole panel, and a panel puts its one question in the middle of the
        glass rather than in the top left corner where a window would be."""
        y = max(0, (h - len(rows)) // 2)
        out = [""] * y + list(rows)
        return (out + [""] * h)[:h]

    # THE PANE SEAT IS THE DISPLAY FRAME — a SOLID BAR, single-cell gutters.
    # LANGUAGES.md §3b, verbatim: "a display REGION, visually separate from
    # the chrome ... framed by SOLID BARS. Everything inside it is machine
    # output; everything outside is a label." Two panes are exactly that
    # boundary — a list the operator drives, a readout the machine writes.
    #
    # AND IT IS NOT `SLOT_GAP`'S ANSWER, which is air. That comment says a
    # rule glyph between slots "would be `Ledger.RULE_V`", and it is right:
    # INSIDE one panel this language separates by air. This is the EDGE of the
    # display, and the edge is a bar. The gutters are the brutalist grid's own
    # ("single-cell gutters, no rounded corners").
    PANE_RULE = "█"

    # THE VALIDATION ROW, on the panel. The remainder is BARE PANEL -- air,
    # because a silkscreen does not rule a line out of a legend (`field_row`
    # makes the same argument for the same reason). The mark is the segment
    # bank fully lit, which is this language's ERROR already.
    ERROR_FILL = ""
    # THE UPPER BANK LIT. `DISCLOSE` is the bank BELOW the segment; a slot
    # that must be filled lights the one above it. Two banks, two meanings,
    # one alphabet -- and not a number, because the numbers are the keymap
    # (L-33) and an obligation is not a key.
    REQUIRED = "▀"

    LEVELS = {"info": "▁▁", "warn": "▄▄", "error": "██"}

    MATCH_STYLE = "bold {ink}"             # the segment driven harder

    def keyhint(self, pairs, w=0):
        """THE ONE PLACE THIS LANGUAGE'S NUMBERING IS ALREADY THE MECHANISM.

        Section 3b: "in a TUI the numbers ARE the keybindings, which makes
        the numbering functional rather than decorative." So the bracket is
        this language's notation and it is spent here -- on a row that says
        which key does what -- and NOT on a button's face, which is operator
        ruling 3: a button is labelled with a word, and the numbers stay the
        parameter keymap.

        EVERY KEY IS STILL THE CALLER'S. The bracket is the kit's; what goes
        inside it is not (inc12 §8.3)."""
        c = self.c
        return "   ".join(f"[{c['accent']}]{mark('[' + str(k) + ']')}[/] "
                          f"[{c['mut']}]{mark(str(v).upper())}[/]"
                          for k, v in pairs)

    PART_GLYPHS = {
        "main": {DEFAULT: "▁▁", DISABLED: "··"},
        "indicator": {DEFAULT: "▄▄", DISABLED: "▁▁"},
        "knob": {DEFAULT: "██", FOCUSED: "▀▀", EDITED: "▓▓",
                 ACTIVE: "▒▒", INVALID: "▀▄",
                 DISABLED: "╳╳"},
        # the LCD's check is a segment DRIVEN, not a tick drawn: the box is
        # the baseline segment, the mark is the same cell at full height.
        # Two segment cells wide, so the containment law is span-equality
        # here too — a two-cell box is a frame with no interior.
        "checkbox.main": {DEFAULT: "▁▁", FOCUSED: "▔▔", ACTIVE: "▂▂",
                          DISABLED: "··"},
        "checkbox.knob": {DEFAULT: "██", FOCUSED: "▛▜", ACTIVE: "▓▓",
                          DISABLED: "▒▒"},
        # THE LED BESIDE THE LABEL, which is what this hardware actually
        # does: a parameter is CHOSEN by a lamp lighting next to its printed
        # name, while a setting is DRIVEN by a segment. Cell one is the
        # segment carrying the control state, cell two is the lamp carrying
        # the choice — so the two channels sit in two different cells and
        # neither is a colour.
        "radio.main": {DEFAULT: "▁◦", FOCUSED: "▔◦", ACTIVE: "▂◦",
                       DISABLED: "·◦"},
        "radio.knob": {DEFAULT: "▁●", FOCUSED: "▔●", ACTIVE: "▂●",
                       DISABLED: "·◌"},
        # an ENGRAVED KEY: this language draws in doubled cells, so both
        # shoulders are two cells wide and the label sits in the milled
        # channel between them. Pressed = the shoulders swell (▄▄), which is
        # the same segment vocabulary its slider and checkbox already speak.
        "button.main": {DEFAULT: "▁▁▁▁", FOCUSED: "▔▔▔▔", ACTIVE: "▄▄▄▄",
                        DISABLED: "····"},
        # FIVE cells, because this language doubles: two cells of wall a side
        # and the rune in the middle. The words sit in a milled channel.
        "textfield.main": {DEFAULT: "▁▁·▁▁", FOCUSED: "▔▔·▔▔",
                           EDITED: "▔▔▁▔▔", ACTIVE: "▄▄·▄▄",
                           INVALID: "▄▀·▀▄",
                           DISABLED: "·····"},
        "textfield.caret": {DEFAULT: "▌"},
        # A SEGMENT BANK, doubled like everything this language draws: the
        # shaft is the GHOST (a segment present but not driven, which is what
        # an LCD shows where nothing is on) and the view is the same cells
        # DRIVEN to full. The reading rides segment presence, never hue —
        # this language's own recorded defect, twice cured.
        "scrollbar.main": {DEFAULT: "░░", DISABLED: "··"},
        "scrollbar.indicator": {DEFAULT: "██", DISABLED: "▒▒"},
        # THE PARAMETER KEYS, and this is the component this language was
        # waiting for: a TE panel spins its numbered parameters with two keys
        # beside the readout, which is a stepper and has never been anything
        # else. Doubled like everything here — two cells a side — and the
        # reading rides SEGMENT HEIGHT, never hue, which is this language's
        # own twice-cured defect.
        #
        # THE DEAD KEY IS A GHOST SEGMENT: present, not driven, exactly what
        # an LCD shows where nothing is on. So a clamped stepper at its floor
        # reads `▁▁ lo ▄▄` — the key is still in the panel and it is plainly
        # not lit, which is what a hardware end stop looks like.
        "stepper.main": {DEFAULT: "▁▁▁▁", DISABLED: "····"},
        "stepper.step": {DEFAULT: "▄▄▄▄", FOCUSED: "▀▀▀▀", EDITED: "▓▓▓▓",
                         ACTIVE: "████", INVALID: "▀▄▄▀",
                         DISABLED: "╳╳╳╳"},
    }

    def part_tone(self, part, state, name=None):
        # the screen hue is the lit segment's own colour, not an accent.
        # `control_of` and not `state`: a COMBINED state (checked+disabled)
        # is still disabled, and comparing the raw string let the lit hue
        # survive a dead control until the switch's laws said so.
        if part == "indicator" and control_of(state) != DISABLED:
            return self.screen
        return super().part_tone(part, state, name)

    def value_label(self, val, state=DEFAULT):
        # a numbered language STATES the parameter, in the aluminium register
        return f"[{self.alu}]\\[{val:>2}][/]"

    def spinner(self, tick):
        return f"[{self.screen}]{self.SPIN[tick % len(self.SPIN)]}[/]"

    # one ghost frame, then the state — a mechanical snap, not a fade
    MOTION_STEPS = 1

    def _strip(self, options, active, spaced: bool) -> tuple[str, int]:
        """One tier of the mode strip, with the PLAIN width it costs.

        The numbers are not decoration: `[1]`..`[4]` are the app's own view
        bindings, so the strip is a picture of the device's numbered buttons
        and pressing the number really does what the strip says."""
        c = self.c
        out, plain = [], []
        for i, o in enumerate(options):
            on = o == active
            lab = " ".join(o.upper()) if (on and spaced) else o.upper()
            mark = "" if spaced else (self.LIT if on else "")
            out.append(f"[{self.screen if on else self.alu}]\\[{i + 1}][/]"
                       f"[{self.screen if on else c['dim']}]{mark}{lab}[/]")
            plain.append(f"[{i + 1}]{mark}{lab}")
        return " ".join(out), len(" ".join(plain))

    def tabs(self, options, active):
        if not self.striped:
            return self._flow_tabs(options, active)
        # THE MODE STRIP. A TE panel shows its buttons at all times and
        # commits ONE SCREEN to the mode they select — the previous form
        # renounced the buttons as well as the screen, which left three of
        # the four modes invisible (NAVIGATION.md tier 1: nothing is
        # discoverable until you show it).
        #
        # THREE TIERS, each keeping TWO channels on "which mode is on screen"
        # so the answer never rides on colour alone: letterspacing while it
        # fits, a lit segment when it does not, and — if even the tight form
        # would overflow its seat — the previous active-only form, which is
        # the composition this one replaced.
        for spaced in (True, False):
            mk, n = self._strip(options, active, spaced)
            if n <= self.STRIP_MAX:
                return mk
        return self._flow_tabs(options, active)

    def _flow_tabs(self, options, active):
        # "each mode takes over the screen" — no persistent nav chrome. The
        # tab strip COMMITS to showing only the active mode, numbered.
        c = self.c
        i = options.index(active) if active in options else 0
        return (f"[{c['accent']}]\\[{i + 1}][/] "
                f"[{c['ink']}]{' '.join(active.upper())}[/]")


class Instrument(Kit):
    """Round-dot scope: braille sub-cell dots carry quantity at 2x4 the cell
    resolution; the unlit lattice stays faintly visible; no frames.

    The board is the SCOPE SCREEN (`layout="trace"`): every phase head carries
    a labelled DAY RETICLE, and every task hangs a braille trace sample off it
    — same origin, same cells, one cell per day. Under any other `layout` the
    previous bench-readout composition comes back byte-for-byte.
    """

    # HALF IS COMPOSED, NOT CHOSEN (#46): the full cell's left sub-column OR
    # the lattice's right one, so a half-filled cell still shows the track it
    # has not reached. Its right sub-column is UNRUN, and the two-unlit
    # verdict's rule is that a half-cell fill inks every ADDRESSABLE
    # sub-column. Asserted as that composition in the suite rather than
    # pinned as a literal — a glyph a law can only compare to itself is a
    # spelling, not a rule.
    BLANK, FULL, HALF, LATT = "⠐", "⣿", "⡗", "⠒"

    # ======================================================================
    # THE SEVEN IT USED TO INHERIT (batch `kits-learn-4`, AC-5). LANGUAGES.md
    # §1: "mono + one accent · dense · WHITESPACE STRUCTURE · drawn dot-matrix
    # type · clinical. Numerals and icons drawn on a coarse dot grid; BORDERS
    # ALMOST ABSENT; one saturated hue for state."
    #
    # Every mark below is braille at this language's own 2x4 sub-cell, which
    # is the reason `lattice_rows` takes a kit hook at all: naught's lattice
    # and this one are the SAME mechanism in two alphabets, and borrowing
    # naught's round dots here would put naught's identity on this screen.
    # ======================================================================
    # `⡇` was the first choice and it is SPOKEN FOR: `verify_language`
    # keeps a three-site census of every `⡇` in this file (five exempt
    # seats, closed against the source), because that glyph is the
    # half-cell fill this repo hunted once. A sixth live one goes red,
    # which is the census doing exactly what it was written for.
    DISCLOSE = "⠿"                        # saturated: there is more beyond
    # THE PANE SEAT — A GRATICULE COLUMN, and this language DRAWS one.
    # LANGUAGES.md §1: "borders almost absent", which is not "no marks": this
    # language already rules a graticule ACROSS a field row (`⠒`), and a
    # graticule is not a border — it was on the glass before either pane
    # arrived. It refuses a modal LID (`MODAL_BORDER_REFUSED`) because a lid
    # ENCLOSES; a graticule MEASURES, and the two are different acts.
    #
    # THE RIGHT COLUMN, DELIBERATELY. `⠇` is the left column and it is this
    # language's ERROR rung (`⠇⠇`); a neutral divider wearing the severity
    # ladder's cell would say "rejected" down the whole gutter to a greyscale
    # reader. `⠸` is the same three dots in the other column and says nothing
    # else in this alphabet.
    PANE_RULE = "⠸"

    # THE REQUIRED MARK — ONE DOT, the least this matrix can light. LANGUAGES
    # .md §1: "numerals and icons DRAWN ON A COARSE DOT GRID ... borders
    # almost absent". Severity in this language is dot COUNT (`⠂⠂ / ⠆⠆ /
    # ⠇⠇`), so an obligation — which is a property and not a severity — is
    # the count's floor: one dot, at the top of the cell, where a trace
    # enters. Not `⡀`: that is prism's dot and it sits at the BOTTOM, on a
    # different reading of the same grid.
    REQUIRED = "⠁"
    DANGER_FORM = ("⠛", "⠛")               # the top row raised, both sides
    # SEVERITY BY DOT COUNT, which is the only ladder a dot-matrix owns:
    # one lit dot, two, three. It must not reach `⠿` (this language's
    # SATURATED mark, spent on `OVER`, on the `wip` icon and on the
    # disclosure above) or the log's worst row and its "there is more"
    # mark would be the same cell.
    LEVELS = {"info": "⠂⠂", "warn": "⠆⠆", "error": "⠇⠇"}
    MATCH_STYLE = "underline {accent}"     # a scope marks a span with a cursor

    def field_row(self, caption, value, w):
        """THE GRATICULE RUNS TO THE FIGURE, and the figure stands at the
        right-hand graticule line.

        This is the SCOPE READOUT, which is what this language's board already
        is (`layout="trace"`): a label at the left, the unlit graticule across
        the field, the reading at the edge. It is NOT a leader — a leader is
        drawn BETWEEN two marks to connect them, and a graticule was on the
        glass before either mark arrived. Naught draws the same distinction
        about its lattice and fills AFTER the figure; this one fills BEFORE
        it, because a scope's reading sits at the trace's end."""
        c = self.c
        cap, val = str(caption), str(value)
        gap = max(1, w - len(cap) - len(val) - 1)
        return (f"[{c['mut']}]{mark(cap)}[/] "
                + f"[{self.t.get('tick', c['dim'])}]{mark(self.LATT * gap)}[/]"
                + f"[{c['ink']}]{mark(val)}[/]")

    def keyhint(self, pairs, w=0):
        """The graticule at one cell, between the key and what it does — the
        same mark the row above spends, and no air at all: this language is
        dense, and air is swiss's divider rather than its own."""
        c = self.c
        return "   ".join(f"[{c['accent']}]{mark(str(k_))}[/]"
                          f"[{c['dim']}]{mark(self.LATT)}[/]"
                          f"[{c['mut']}]{mark(str(v))}[/]"
                          for k_, v in pairs)

    def overlay_instead(self, rows, w, h, under):
        """"Borders almost absent", so the question is not boxed — it is
        BANDED: two full-width graticule rules, the question between them,
        the page unlit behind. Whitespace structure with the dot identity,
        which is the pair of commitments this language leads with."""
        c = self.c
        band = f"[{self.t.get('tick', c['dim'])}]{mark(self.LATT * w)}[/]"
        block = [band] + list(rows) + [band]
        y = max(0, (h - len(block)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(block):
                out.append(block[i - y])
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out

    # -- the LATTICE surface posture, in THIS language's dots ---------------
    # Shared with naught (AC-2 says they share the mechanism) and drawn in a
    # different alphabet, which is the whole reason the mechanism takes a kit
    # hook instead of a kit name. Naught's lattice is `∙`/`◦` at one dot per
    # cell; this one is braille at 2x4, because `base="braille"` is what this
    # language declares and borrowing naught's dots here would put naught's
    # identity on instrument's screen.
    LATTICE_GLYPHS = frozenset(chr(c) for c in range(0x2800, 0x2900)) | {" "}

    def lattice_grid(self, w: int, h: int) -> tuple[int, int]:
        """2x4 sub-cell dots — braille's own sub-grid (`bases.BASES`), which
        is also the maximum resolution any base here reaches."""
        return max(1, w * 2), max(1, h * 4)

    def lattice_rows(self, bm, w: int, h: int) -> list[str]:
        """Lit cells in the ink, cells with no dot drawn as `BLANK` in the
        graticule tone — the same unlit mark this language's own meter uses,
        so the surface does not invent a second "this position is empty".
        `bases.braille` returns U+2800 for an empty cell, which is the defect
        DATAVIZ law 4 names by name (a blank that draws no track)."""
        tick = self.t.get("tick", self.c["dim"])
        out = []
        for row in BS.braille(bm)[:h]:
            line, buf, run = [], [], None
            for ch in row[:w].ljust(w, "⠀"):
                lit = ch != "⠀"
                if run is not None and lit is not run and buf:
                    line.append(f"[{self.c['ink'] if run else tick}]"
                                f"{''.join(buf)}[/]")
                    buf = []
                run = lit
                buf.append(ch if lit else self.BLANK)
            if buf:
                line.append(f"[{self.c['ink'] if run else tick}]"
                            f"{''.join(buf)}[/]")
            out.append("".join(line))
        while len(out) < h:
            out.append(f"[{tick}]{self.BLANK * w}[/]")
        return out

    # ======================================================================
    # THE RETICLE. Every cell position below is computed in ONE place
    # (`reticle()`), which the head, the trace row and the acceptance checks
    # all read — the `Ledger.cols` / `Swiss.grid` / `Nord.panes` precedent, so
    # "the ticks and the samples share the same cells" is true by construction
    # rather than by coincidence.
    # ======================================================================
    # ONE CELL IS ONE DAY, and that scale is a CONSTANT rather than a token.
    # A per-column scale is exactly the "siblings lie" failure DATAVIZ.md law 2
    # names: a 3-day task must be three cells long in the widest column AND in
    # the narrowest. Width buys HORIZON, never resolution. (A `days_per_cell`
    # knob was written and then deleted — it was always 1, nothing asked for
    # it, and its label arithmetic divided where it would have had to multiply,
    # so it was a latent bug wearing a generality's clothes.)
    TICK_EVERY = 7       # the week — the unit a task board is actually read in
    HORIZON = 21         # three weeks, and the same horizon in every column
                         # that can afford it. Beyond it a sample is CLIPPED
                         # and flagged, never clamped onto the last cell.
    IND = 2              # the trace row's indent (the sub-row's existing one)
    VAL_W = 4            # the widest reading the row ever states ("-12d")
    SPAN_MIN = 9         # underflow cell + origin + one whole week + its tick.
                         # Below this there is no SCALE, only a stub, so the
                         # reticle is RENOUNCED and the bench readout returns.
    # THE HEAD/CARD BUDGET MISMATCH IS GONE (PENDING item 4, cured at the
    # source): `kanban.py.row_width` hands the head the card's own measure and
    # `.col-head { padding-left: 1 }` gives it the card's own origin. This
    # language used to need TWO constants here — an origin pad and a length
    # trim of four — because the two jobs had different wrong answers. The
    # axis now takes the whole measure it is given and is indented by the
    # trace's own indent, nothing more.
    # The graticule is DASHED, and that is not taste: a solid `│` is already
    # ledger's money-column rule (`Ledger.RULE_V`), and its dispatch check —
    # "money-column rules render IFF layout=ruled" — went red the moment this
    # field borrowed the glyph. A graticule should read fainter than a divider
    # anyway, so the collision and the correct form point the same way.
    AXIS, ORIGIN, TICK, GRAT = "─", "├", "┴", "┊"
    OVER = "⠿"           # off-scale HIGH. A glyph the fill itself never emits
                         # (the fill knows only FULL / HALF / LATT), so it can
                         # never be confused with a sample that merely reaches
                         # the last cell.

    @property
    def traced(self) -> bool:
        """The `layout` token, dispatched — the same shape as darkside's
        `rail_width` and industrial's `panel`. A hardcoded reticle would make
        the token dead metadata again (PENDING item 0)."""
        return self.layout == "trace"

    @property
    def tick_ink(self) -> str:
        """The graticule's stroke. NOT `tick_tone`, which is Kit's gauge
        THRESHOLD colour and answers a different question."""
        return self.t.get("tick", self.c["dim"])

    @property
    def unit_ink(self) -> str:
        return self.t.get("unit", self.c["mut"])

    def reticle(self, w: int) -> tuple[int, list[int]]:
        """The scope's geometry for a row of `w` content cells: how many cells
        the field takes, and which of them carry a week tick.

        Cell 0 is the UNDERFLOW cell — strictly left of the origin, where an
        overdue sample is flagged. The origin is cell 1, and day `d` lands on
        cell `1 + d`. A field narrower than `SPAN_MIN` returns `(0, [])`: the
        trace is renounced rather than crushed."""
        span = min(w - self.IND - 1 - self.VAL_W, self.HORIZON + 2)
        if span < self.SPAN_MIN:
            return 0, []
        return span, [1 + k * self.TICK_EVERY
                      for k in range(1, self.HORIZON // self.TICK_EVERY + 1)
                      if 1 + k * self.TICK_EVERY < span]

    @staticmethod
    def _runs(cells: list[tuple[str, str]]) -> str:
        """Coalesce a per-cell (glyph, tone) field into markup runs. Emitting
        a tag per cell would triple the markup a 23-cell field costs on every
        card, every redraw."""
        out, buf, tone = [], "", None
        for ch, tn in cells:
            if tn != tone:
                if buf:
                    out.append(f"[{tone}]{buf}[/]")
                buf, tone = "", tn
            buf += ch
        if buf:
            out.append(f"[{tone}]{buf}[/]")
        return "".join(out)

    def axis_row(self, w: int) -> str:
        """The reticle itself: the origin, the week ticks, and each tick's unit
        label right-flushed against it. Empty when the field is renounced."""
        span, ticks = self.reticle(w)
        if not span:
            return ""
        tk, un = self.tick_ink, self.unit_ink
        cells = [(self.AXIS, tk) for _ in range(span)]
        cells[1] = (self.ORIGIN, tk)
        for x in ticks:
            cells[x] = (self.TICK, tk)
            lab = f"{x - 1}d"
            if x - len(lab) >= 2:              # never write over the origin
                for i, ch in enumerate(lab):
                    cells[x - len(lab) + i] = (ch, un)
        return self._runs(cells)

    def trace_row(self, w: int, meta: dict | None = None) -> str | None:
        """One task's sample, hung off the same reticle its head draws.

        MONOTONE FILL FROM A FIXED ORIGIN, never a needle: the bar grows from
        cell 1 rightwards, so length is the reading and the eye compares
        lengths down the column. Out-of-range samples are CLIPPED AND FLAGGED
        at the boundary — clamping an overdue task onto the origin would print
        it as "due today", and clamping a far one onto the last cell would make
        it indistinguishable from a task that really is at the horizon."""
        span, ticks = self.reticle(w)
        if not span:
            return None
        c = self.c
        cells = [(self.LATT, self.tick_ink) for _ in range(span)]
        for x in ticks:
            cells[x] = (self.GRAT, self.tick_ink)
        d = (meta or {}).get("days")
        if d is None:
            read = "--"                        # no signal: the field stays dark
        else:
            read = f"{d}d"
            if d < 0:
                cells[0] = (self.FULL, c["alert"])       # off-scale LOW
            else:
                # microbar floor (DATAVIZ law 3): DUE TODAY is an event, and a
                # zero-length bar would print it as nothing at all
                dots = max(1, 2 * d)
                full, half = divmod(dots, 2)
                last = span - 1
                if 1 + full + (1 if half else 0) > last:  # off-scale HIGH
                    for x in range(1, last):
                        cells[x] = (self.FULL, c["accent"])
                    cells[last] = (self.OVER, c["accent"])
                else:
                    for x in range(1, 1 + full):
                        cells[x] = (self.FULL, c["accent"])
                    if half:
                        cells[1 + full] = (self.HALF, c["accent"])
        return (" " * self.IND + self._runs(cells)
                + f" [{self.unit_ink}]{read}[/]")

    def composition(self):
        # a bench instrument: symmetric, inset, the trace centred
        css = """
        #ap { margin: 0 3; }
        Screen.sz-board #hero { margin: 0 8; }
        """
        if self.traced:
            # THE RETICLE PAYS FOR ITSELF. The axis row costs the head a
            # second row, and the blank row `.col-head` spends below it is
            # what that row is FOR — a reticle already separates a legend from
            # the traces under it. Without this the board lost a card to the
            # fold; with it the vertical cost of the whole composition is zero
            # (measured: 4 complete cards per column before and after).
            css += "\n        .col-head { margin-bottom: 0; }\n        "
        return css

    def head(self, name, count, w, idx=0):
        if not self.traced:
            return self._flow_head(name, count, w, idx)
        # THE SCOPE'S LEGEND: the phase names its channel, STATES its count
        # (DATAVIZ law 5 — position is not a reading), and the reticle runs
        # under it. The flow head's 4-cell spark SATURATES at four, so a phase
        # of 7 and a phase of 4 drew the same four cells; a real axis replaces
        # a bar that could not tell them apart.
        c = self.c
        n = str(count)
        room = max(1, w - len(n) - 1)
        nm = name.upper()[:room]
        line = (f"[{c['mut']}]{nm}[/]{' ' * (room - len(nm))} "
                f"[{c['accent'] if count else c['dim']}]{n}[/]")
        ax = self.axis_row(w)
        # ALWAYS TWO ROWS, even when the scale is renounced. A kanban is read
        # ACROSS its columns, so a head that shrank to one row in the narrow
        # column started that column's card stack a row above its neighbours'
        # — measured on the 80-cell board, and it read as a broken board
        # rather than as a decision. The renounced form is a blank row, not a
        # stub axis: a baseline with no gradations would advertise a scale the
        # samples beside it do not use.
        return line + "\n" + (" " * self.IND + ax if ax else " ")

    def _flow_head(self, name, count, w, idx=0):
        c = self.c
        spark = self.FULL * min(4, count) + self.LATT * max(0, 4 - min(4, count))
        return (f"[{c['mut']}]{name.upper()[:max(1, w - 7)]}[/] "
                f"[{c['accent'] if count else c['dim']}]{count}[/]"
                f"[{c['dim']}]{spark}[/]")

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        c = self.c
        dot = f"[{tone if urgent else c['dim']}]{'⣿' if urgent else '⠂'}[/] "
        room = max(1, w - len(chip) - 4)
        body = _fit(title, room)
        lead = ("·" * max(0, room - min(len(title), room)))
        return (dot + f"[{c['ink']}]{body}[/][{c['dim']}]{lead}[/] "
                f"[{tone}]{chip}[/]")

    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        if not self.traced:
            return self._flow_card_rows(title, chip, tone, w, idx, urgent, meta)
        top = self.card_row(title, chip, tone, w, idx, urgent)
        row = self.trace_row(w, meta)
        if row is None:
            # THE NARROW TIER. Below `SPAN_MIN` there is no scale to hang a
            # sample off, so the reticle is renounced and the bench readout
            # returns — the degrade lands on the form the trace replaced and
            # can therefore never be worse than it (swiss's grid law).
            return self._flow_card_rows(title, chip, tone, w, idx, urgent, meta)
        return [top, row]

    def _flow_card_rows(self, title, chip, tone, w, idx=0, urgent=False,
                        meta=None):
        # a bench readout: phase progress as a braille half-cell bar (sub-cell
        # precision is this language's whole point), due beside it
        top = self.card_row(title, chip, tone, w, idx, urgent)
        m = meta or {}
        c = self.c
        n = max(1, int(m.get("n_phases", 4)))
        pi = max(0, int(m.get("phase_idx", 0)))
        cells = 6
        dots = max(0, min(cells * 2, round(cells * 2 * (pi + 1) / n)))
        full, half = divmod(dots, 2)
        # THE THREE GLYPHS COME OFF THE SEAT, all three. This row read
        # `self.LATT` and re-spelled the other two, which is the #45 shape at
        # one-third strength: #46 had to be applied in three places instead
        # of one, and the third place is a module-level MECHANISM that this
        # language does not own. Two of the three are now the same seat.
        bar = (f"[{c['accent']}]{self.FULL * full}{self.HALF * half}[/]"
               f"[{c['dim']}]{self.LATT * (cells - full - half)}[/]")
        d = m.get("days")
        due = "--" if d is None else f"{d}d"
        sub = _fit_parts([("  ", "  "), (bar, " " * cells),
                          (f" [{c['mut']}]{due}[/]", f" {due}")], w)
        return [top, sub]

    def tile_row(self, val, label, tone, w):
        c = self.c
        return (f"[{tone}]⠿[/] [{tone}]{val}[/] "
                f"[{c['mut']}]{label[: max(0, w - len(val) - 4)]}[/]")

    def sect(self, title, note, w, h=0):
        c = self.c
        # DISPLAY TYPE, clinical register: the title through the braille base
        # UNSCALED — 3x5 dots pack into 2 rows of sub-cell type. Small,
        # precise, cheap enough that h>=10 affords it.
        if h >= 10:
            bm = BS.from_font(title, NA._ALPHA, gap=1)
            if len(bm[0]) // 2 <= w - 10:
                rows = [f"[{c['ink']}]{r}[/]" for r in BS.render(bm, "braille")]
                rows[-1] += f"  [{c['mut']}]{note}[/]"
                return rows + [self.rule_line(w)
                               or f"[{c['dim']}]{self.LATT * max(1, w - 1)}[/]"]
        return [f"[{c['accent']}]⣿[/] [{c['ink']}]{title}[/]  "
                f"[{c['mut']}]{note}[/]",
                self.rule_line(w) or f"[{c['dim']}]{self.LATT * max(1, w - 1)}[/]"]

    def bar(self, span, head=None, tone=None):
        c = self.c
        tone = tone or c["accent"]
        body = "".join(
            f"[{c['ink']}]{self.FULL}[/]" if (head is not None and head[i])
            else f"[{tone}]⠶[/]" for i in range(span))
        return body

    GANTT = ("⠒", "⣿", "⡇", "⠄", "⣿")

    def cal_cell(self, state):
        c = self.c
        return {"none": f"[{c['dim']}]{self.LATT} [/]",
                "over": f"[{c['alert']}]{self.FULL} [/]",
                "multi": f"[{c['accent']}]{self.FULL} [/]",
                "one": f"[{c['warn']}]⠶ [/]"}[state]

    # abstract braille patterns — clinical, dot-coded
    ICONS = {"deadline": "⠙", "overdue": "⠮", "wip": "⠿", "blocked": "⠺",
             "workday":"⠳", "boardfile":"⠋"}

    CUR = "⣿"
    SPIN = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧")     # the round-dot classic

    # the braille register. The old slider had no knob at all — a filled run
    # and nothing to grab — so it was a BAR wearing a slider's name, which is
    # the exact confusion the parts registry exists to make impossible.
    PART_GLYPHS = {
        # THE DEAD RUNG IS `⠄`, NOT `⠁` (inc46). `⠁` is `REQUIRED` -- one dot
        # at the top of the cell, inc35's obligation mark -- and it was also
        # the DISABLED track here, the DISABLED checkbox, the dead field's
        # paper and the stepper's end stop. `instrument_S3` is the frame: a
        # reader who has just learned that `⠁` means "you must fill this"
        # meets it on a switch that says "off, and you may not touch it".
        # `⠄` is the same column's BOTTOM dot and is already this language's
        # dead rung -- the dead button's rails, the dead field's rails and the
        # dead knob all wear it.
        # The dead TRACK cannot take `⠄` either -- that is the dead KNOB, and
        # `verify_language` holds a knob to differing in SHAPE from both the
        # fill and the track. It takes the right column's top dot, the rung
        # this language's dead stepper track already wears (`⠈⠈`).
        "main": {DEFAULT: "⠒", DISABLED: "⠈"},
        "indicator": {DEFAULT: "⣿", DISABLED: "⠶"},
        "knob": {DEFAULT: "⡇", FOCUSED: "⢸", EDITED: "⠿",
                 ACTIVE: "⣤", INVALID: "⠶",
                 DISABLED: "⠄"},
        # one register CELL, sparse or driven. Braille's sub-cell grid is
        # already the box: the eight dots are the interior, so this language
        # needs no bracket to contain a mark. Span-equality carries the
        # containment law here, the same renunciation naught makes.
        "checkbox.main": {DEFAULT: "⠒", FOCUSED: "⠛", ACTIVE: "⠤",
                          DISABLED: "⠄"},
        "checkbox.knob": {DEFAULT: "⣿", FOCUSED: "⣶", ACTIVE: "⣤",
                          DISABLED: "⠿"},
        # A REGISTER READ AS A RING, not as a level. The checkbox drives the
        # cell from the bottom up (a quantity reaching full); the radio sets
        # the cell's OUTER dots and leaves the middle, which in braille is
        # the closest thing to a round well the sub-cell grid can hold. One
        # cell, so the containment law is span-equality here as it is for the
        # checkbox — stated, not smuggled.
        "radio.main": {DEFAULT: "⠐", FOCUSED: "⠰", ACTIVE: "⠘",
                       DISABLED: "⠈"},
        "radio.knob": {DEFAULT: "⠶", FOCUSED: "⠾", ACTIVE: "⠷",
                       DISABLED: "⠦"},
        # RAILS, in the clinical register: a braille column each side, the
        # word between them like a reading between two graticule marks. The
        # press BOTTOMS OUT — the rails gain their lower dots (⣇ ⣸) — which
        # is a travel this language can show without moving the label.
        # THE RAILS MIRROR (inc46), and it is one edit with two arguments.
        # `⠇` is `LEVELS["error"]`'s own cell -- three dots in the LEFT
        # column, the ladder's top rung -- and it was OPENING the SAFE button:
        # `instrument_S4` puts the only severity cell on the screen over
        # `Cancel`, one key away from deleting three tasks. inc36 already made
        # this choice once, for the gutter, and wrote the reason down -- it
        # took `⠸` "because `⠇` is the error rung and a neutral divider with
        # the cell of the ladder would say 'rejected' to a greyscale reader".
        # The rail takes the gutter's column.
        #
        # AND THE INK NOW LOOKS AT THE CONTENT. Read as a pair, `⠇ … ⠸` sets
        # each rail's dots on its OUTER edge, facing away from the word --
        # `] [` in braille. `⠸ … ⠇` faces them in. The handedness is kept
        # (inc39's law bites on this language), it is simply the other way
        # round, and the INVALID declaration below is mirrored with it.
        #
        # `⠇` IS STILL THE CLOSER, and that is a declared cost rather than an
        # oversight: the LEFT braille column IS the severity ladder's column
        # (`⠂` one dot, `⠆` two, `⠇` three), so the only left-column rail that
        # does not share a cell with the ladder is the FOUR-dot `⡇` -- which
        # is this language's caret, its own index mark, and a field whose
        # closing rail is its caret is worse than one whose closing rail is a
        # rung. The batch rule names the OPENER, the switch indicator and the
        # disabled mark; a closer is none of the three.
        "button.main": {DEFAULT: "⠸  ⠇", FOCUSED: "⠼  ⠧", ACTIVE: "⣸⣀⣀⣇",
                        DISABLED: "⠄  ⠄"},
        # braille RAILS with a braille RULE between them, clinical register:
        # the field is a measured span and the words lie along it.
        # INVALID KEEPS THE RAILS AND CHANGES THE PAPER (inc39). It read
        # `⠸⠶⠇`: the same two rails with left and right EXCHANGED, so a
        # rejected field and a good one differed by the ORDER of two braille
        # cells thirty-four columns apart -- unreadable without comparing
        # both ends of the row. The rails go back the way this language sets
        # them in every other state; the full-dot paper `⠶` was already a
        # channel and is now the only one.
        #
        # MIRRORED WITH THE BUTTON (inc46): the opener takes the gutter's
        # column so the error rung stops opening a field, and the dots face
        # the words. INVALID keeps the PAPER as its channel, which is inc39's
        # fix; only the hand of the rails moved. The dead paper is the dead
        # RAIL's own rung now (`⠄`) rather than `⠁`, which is `REQUIRED`.
        "textfield.main": {DEFAULT: "⠸⠒⠇", FOCUSED: "⠼⠒⠧", EDITED: "⠼⠤⠧",
                           ACTIVE: "⣸⠒⣇", INVALID: "⠸⠶⠇",
                           DISABLED: "⠄⠄⠄"},
        # a full-height braille tick — this language's own index mark
        "textfield.caret": {DEFAULT: "⡇"},
        # THE REGISTER READ AS A TRAVERSE: the shaft is the baseline rail
        # (one dot row, the instrument's zero) and the view is the register
        # DRIVEN FULL. Clinical, and it is the same sub-cell channel this
        # language spends on every quantity it has ever drawn.
        # the dead shaft cannot take `⠄` -- that is this shaft's LIVE datum --
        # so it takes the right column's top dot, the rung this language's
        # dead stepper track already wears (`⠈⠈`).
        "scrollbar.main": {DEFAULT: "⠄", DISABLED: "⠈"},
        "scrollbar.indicator": {DEFAULT: "⣿", DISABLED: "⠿"},
        # THE REGISTER'S DETENTS — a braille column each side, weighted to
        # the side it steps toward, so the sub-cell grid carries the
        # direction the way it carries everything else here. The state is how
        # many dot rows are driven; the dead detent is the baseline rail this
        # instrument reads zero as.
        # the end stop is the REGISTER'S BASELINE, `main`'s own datum, and no
        # longer `⠁⠁` -- see the dead-rung note above: `⠁` is `REQUIRED`.
        "stepper.main": {DEFAULT: "⠒⠒", DISABLED: "⠈⠈"},
        "stepper.step": {DEFAULT: "⡄⢠", FOCUSED: "⡆⢰", EDITED: "⡇⢸",
                         ACTIVE: "⣇⣸", INVALID: "⢠⡄",
                         DISABLED: "⠄⠄"},
    }

    def spinner(self, tick):
        return f"[{self.c['accent']}]{self.SPIN[tick % len(self.SPIN)]}[/]"

    # the dots ROLL through the track — braille's half-cell precision
    MOTION_STEPS = 3

    def tabs(self, options, active):
        c = self.c
        return "  ".join(
            f"[{c['accent']}]⣿[/][{c['ink']}]{o.upper()}[/]" if o == active
            else f"[{c['dim']}]⠂[/][{c['mut']}]{o}[/]" for o in options)


class Swiss(Kit):
    """Structure by alignment and emptiness. ONE hairline rule. No boxes, no
    markers, no drawn type — counts are typographic, space is the divider.

    The board is an EDITORIAL SPREAD (`layout="editorial"`): every entry is
    set on a type GRID of `columns` columns — subject · byline · figure — and
    the single hairline is the masthead rule under the LEADING phase, not one
    rule per head. Under any other `layout` the previous full-width flow rows
    come back, byte for byte (`_flow_*`)."""

    # THE GRID. Two constants decide everything, so the drop rule is derived
    # rather than tabulated:
    #   GUTTER      cells of air between columns. Air is this language's
    #               divider, so the gutter is what a rule would have been.
    #   MEASURE_MIN the narrowest column that still holds a task title. Below
    #               it a title is cut mid-phrase, which is what "illegible"
    #               measured as on the darkside board (~7 chars). The seeded
    #               board's titles run 19-24 characters; 24 is the measure at
    #               which none of them is cut.
    GUTTER = 3
    MEASURE_MIN = 24

    # ======================================================================
    # THE SEVEN IT USED TO INHERIT (batch `kits-learn-4`, AC-5). LANGUAGES.md
    # §2: "near-mono + one accent (classically red) · AIRY · single hairline
    # rules · plain cells · clinical-editorial. Strict grid, generous
    # emptiness, FLUSH-LEFT EVERYTHING, NO BOXES — ALIGNMENT DOES THE
    # DIVIDING."
    # ======================================================================
    DISCLOSE = "─"                        # the hairline, at one cell
    # THE REQUIRED MARK — THE LADDER'S OWN MARK AT FULL WEIGHT. §2: "near-
    # mono + one accent (classically red) ... no boxes — ALIGNMENT DOES THE
    # DIVIDING", and this language's severity ladder is a WEIGHT ladder
    # (`· / ─ / ━`). It has no glyph alphabet to reach into — it is the
    # cheapest language here precisely because it draws none — so the mark
    # it can honestly spend is the one shape it already uses, set solid:
    # `•` against the ladder's `·`. Weight, which is the whole method, and
    # not a hue: the accent is rationed and an obligation is not an alarm.
    REQUIRED = "•"
    # THE DIAGONALS THIS LANGUAGE ALREADY REJECTS WITH. `field_form(INVALID)`
    # is `╲ ╱` here, so a destructive control is bracketed by the same pair
    # — one rejection notation, not two. And it is a FORM: this language's
    # accent is its red, and the red is spent on the one thing it accents.
    DANGER_FORM = ("╲", "╱")
    # A WEIGHT LADDER, which is this language's whole hierarchy device
    # ("hierarchy by weight, generous emptiness"): a dot, a hairline, a heavy
    # rule. One cell each, so a column of rows aligns.
    LEVELS = {"info": "·", "warn": "─", "error": "━"}
    MATCH_STYLE = "bold {alert}"           # the classic red, and never alone

    def field_row(self, caption, value, w):
        """FLUSH LEFT, BOTH OF THEM, on the grid.

        Every other language here closes the gap somehow — a leader, a
        lattice, a dimension, an ember. This one does not close it: the
        figure starts at the next COLUMN and the emptiness between is the
        divider, which is the language's whole method stated as one row
        ("no boxes — alignment does the dividing").

        The caption's field is `MEASURE_MIN // 2` wide with the grid's own
        `GUTTER` after it, so two rows of different caption lengths put their
        figures in the SAME cell. A right-flushed figure would put them in
        the same cell too and would be nord's answer; this one is a grid, and
        a grid is read from the left."""
        c = self.c
        cap, val = str(caption), str(value)
        col = self.MEASURE_MIN // 2 + self.GUTTER
        gap = max(self.GUTTER, col - len(cap))
        return (f"[{c['mut']}]{mark(cap)}[/]" + " " * gap
                + f"[{c['ink']}]{mark(val)}[/]"
                + " " * max(0, w - len(cap) - gap - len(val)))

    def keyhint(self, pairs, w=0):
        """AIR, and more of it than anyone else spends. The gutter separates
        a key from its label and twice the gutter separates one pair from the
        next — the same two measures the editorial grid is built on, because
        a language with one divider uses it everywhere."""
        c = self.c
        return (" " * (self.GUTTER * 2)).join(
            f"[{c['accent']}]{mark(str(k_))}[/]" + " " * self.GUTTER
            + f"[{c['mut']}]{mark(str(v))}[/]" for k_, v in pairs)

    def overlay_instead(self, rows, w, h, under):
        """NO BOXES, at any width — so the question is set at the grid's first
        column under the SINGLE HAIRLINE this language allows itself, with the
        page dimmed behind. The rule is the masthead's, not a lid's: it runs
        the full measure and nothing turns a corner."""
        c = self.c
        rule = f"[{self.rule_color}]{mark('─' * w)}[/]"
        block = [rule, ""] + list(rows)
        y = max(0, (h - len(block)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(block):
                out.append(block[i - y])
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out

    @property
    def editorial(self) -> bool:
        """The grid, dispatched on the token — the same shape as
        `Darkside.rail_width`, `Naught.lattice` and `Industrial.panel`. A
        hardcoded grid would make `layout` dead metadata (PENDING item 0)."""
        return self.layout == "editorial"

    def grid(self, w: int) -> list[tuple[int, int]]:
        """(origin, measure) per column at `w` cells — ONE function, read by
        the renderer AND by the acceptance check, so "the elements and the
        columns share the same cells" is true by construction (Ledger.cols'
        precedent).

        THE DROP RULE, stated so it can be disproved: take the declared column
        count, and while a column would come out narrower than MEASURE_MIN,
        RENOUNCE one — 3 -> 2 -> 1. Never wrap, never crush. Which element
        goes with the column is declared in `_entry`."""
        n = max(1, int(self.t.get("columns", 3)))
        while n > 1 and (w - self.GUTTER * (n - 1)) // n < self.MEASURE_MIN:
            n -= 1
        cw = max(1, (w - self.GUTTER * (n - 1)) // n)
        return [(i * (cw + self.GUTTER), cw) for i in range(n)]

    def _spread(self, w: int, placed: list[tuple[int, str, str]]) -> str:
        """Set `placed` — (column index, markup, plain) — on the grid, each
        element flush left at its column's ORIGIN.

        Flush left, not flush right, and that is a decision: the head is given
        a different measure from the cards (kanban.py budgets the head
        `avail - 4` and the card its own content box), so a right-flushed
        figure would land in a different cell in the head than in the entries
        under it. The origins are identical at both measures; the right edges
        are not. Alignment is this language's whole structure, so the grid —
        not the page edge — is what everything is set against."""
        cols = self.grid(w)
        out, x = "", 0
        for ci, mk, pl in placed:
            if not pl or ci >= len(cols):
                continue
            ox, cw = cols[ci]
            if ox < x:                     # never overlap: air is structure
                continue
            out += " " * (ox - x) + mk
            x = ox + min(len(pl), cw)
        return out

    def head(self, name, count, w, idx=0):
        if not self.editorial:
            return self._flow_head(name, count, w, idx)
        c = self.c
        # the leading cell used to be paid HERE, in the markup, because the
        # head was measured apart from its spread. It is the seat's now
        # (`.col-head { padding-left: 1 }`, base tcss) and the masthead simply
        # takes the measure it is given.
        m = max(6, w)
        cols = self.grid(m)
        cnt = f"{count}" if count else ""
        if len(cols) == 1:
            line = self._flow_head_line(name, count, m)
        else:
            cap = " ".join(name.upper())[: cols[0][1]]
            line = self._spread(
                m, [(0, f"[{c['ink']}]{cap}[/]", cap),
                    (len(cols) - 1, f"[{c['mut']}]{cnt}[/]", cnt)])
        # ONE HAIRLINE FOR THE WHOLE SPREAD. The rule is the masthead's, so it
        # is drawn under the LEADING phase and nowhere else — a rule under
        # every head is four rules, which is what this language spent before
        # and what its own note ("one rule") already denied.
        rule = self.rule_line(m) if idx == 0 else None
        return line if rule is None else line + "\n" + rule

    def _flow_head_line(self, name, count, w):
        c = self.c
        cap = " ".join(name.upper()[: max(1, (w - 4) // 2)])
        line = f"[{c['ink']}]{cap}[/]"
        cnt = f"{count}" if count else ""
        gap = max(1, w - len(cap) - len(cnt) - 2)
        return line + " " * gap + f"[{c['mut']}]{cnt}[/]"

    def _flow_head(self, name, count, w, idx=0):
        line = self._flow_head_line(name, count, w)
        rule = self.rule_line(w)
        return line if rule is None else line + "\n" + rule

    def _entry(self, title, chip, tone, w, proj=""):
        """One entry, set on the grid. THE COLUMN ROLES, and the order they
        are renounced in:

          3 columns  subject (the title) · byline (the project) · figure
          2 columns  subject · figure — the BYLINE goes first: it is the only
                     one of the three that is neither the thing named nor its
                     datum (the ledger tile's law: a clipped row keeps its
                     figure)
          1 column   the flow row itself, verbatim — the drop rule degrades
                     towards the form it replaced, so the floor tier can never
                     be worse than what was there before."""
        c = self.c
        cols = self.grid(w)
        n = len(cols)
        if n == 1:
            return self._flow_card_row(title, chip, tone, w)
        t = _fit(title, cols[0][1])
        placed = [(0, f"[{c['ink']}]{t}[/]", title[: cols[0][1]])]
        if n >= 3 and proj:
            p = proj[: cols[1][1]]
            placed.append((1, f"[{c['mut']}]{mark(p)}[/]", p))
        ch = chip[: cols[-1][1]]
        placed.append((n - 1, f"[{tone}]{ch}[/]", ch))
        return self._spread(w, placed)

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        if not self.editorial:
            return self._flow_card_row(title, chip, tone, w, idx, urgent)
        return self._entry(title, chip, tone, w)

    def _flow_card_row(self, title, chip, tone, w, idx=0, urgent=False):
        c = self.c
        room = max(1, w - len(chip) - 2)
        body = _fit(title, room)
        pad = " " * max(0, room - min(len(title), room))
        # flush-left title, flush-right chip, NOTHING between — the space is
        # the structure. Urgency rides the chip alone.
        return f"[{c['ink']}]{body}[/]{pad} [{tone}]{chip}[/]"

    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        # the second row is RENOUNCED: swiss already spends a whole row of
        # space between cards (pitch) — metadata would be ornament. One row,
        # and the renunciation is the commitment (verified as such).
        #
        # The grid is what lets the entry carry its BYLINE anyway: the project
        # takes a COLUMN, not a row. The renunciation is unchanged.
        if not self.editorial:
            return [self._flow_card_row(title, chip, tone, w, idx, urgent)]
        return [self._entry(title, chip, tone, w, (meta or {}).get("proj", ""))]

    def tile_row(self, val, label, tone, w):
        c = self.c
        room = max(0, w - len(val) - 2)
        return f"[{c['mut']}]{label[:room]}[/] [{tone}]{val}[/]"

    def sect(self, title, note, w, h=0):
        # drawn type RENOUNCED: letterspace and weight ARE the display face
        c = self.c
        return ([f"[{c['ink']}]{' '.join(title)}[/]   [{c['mut']}]{note}[/]"]
                + ([self.rule_line(w)] if self.rule_line(w) else []) + [""])

    def bar(self, span, head=None, tone=None):
        tone = tone or self.c["accent"]
        body = "".join("━" if (head is None or head[i]) else "─"
                       for i in range(span))
        return f"[{tone}]{body}[/]"

    GANTT = ("─", "━", "│", " ", "┃")

    def cal_cell(self, state):
        c = self.c
        return {"none": f"[{c['dim']}]· [/]",
                "over": f"[{c['alert']}]━━[/]",
                "multi": f"[{c['accent']}]━━[/]",
                "one": f"[{c['mut']}]──[/]"}[state]

    # typographic controls: weight and space, no boxes, no ornament
    def surface(self):
        return ""                          # emptiness is the surface

    def board_layout(self):
        return "sections"                  # the editorial list, not columns

    def composition(self):
        # the narrow editorial MEASURE is the ambient register (a text
        # column); data surfaces take the full page — the same posture split
        # that made darkside's tasks legible again. Flush-left stays: the
        # margin is the structure.
        # at BOARD size the ambient block YIELDS rows to the data (hero 9,
        # tiles one row): airy chrome that buries the board under the fold
        # is not airiness, it is a broken surface (30-row screens showed
        # zero cards). The tiles-as-list commitment lives at widget size.
        return """
        #ap { margin: 0 0 0 4; }
        #top, #tiles, #tabs, #queue, #ap-panel { max-width: 78; }
        Screen.sz-board #hero { height: 9; }
        Screen.sz-widget #tiles { layout: vertical; height: auto; }
        """

    def mascot(self):
        return []                          # no ornament — swiss renounces it

    def wordmark(self, text):
        c = self.c
        return [f"[{c['ink']}]{' '.join(text.upper())}[/]",
                f"[{c['dim']}]{'─' * max(1, len(text) * 2 - 1)}[/]"]

    MOTION_STEPS = 0                         # motion renounced — a decision

    ICONS = {}                             # no pictograms — the WORD is the icon

    VOICE = {"empty": "nothing here", "no_signals": "no signals enabled"}

    # THE LADDER'S MARK STOOD UPRIGHT (inc45). This read `━`, which is
    # `LEVELS["error"]` -- so a selected column head and a rejected one were
    # the same cell, and `swiss_S1`'s objection is exactly that: "with the
    # colour taken away, say whether DOING is SELECTED or in ERROR".
    #
    # THE SEVERITY LADDER KEEPS THE RULE. A weight ladder of HORIZONTAL rules
    # (`· ─ ━`) is this language's whole hierarchy device and severity is what
    # it was declared for ("hierarchy by weight, generous emptiness"). The
    # cursor takes the same weight on the OTHER AXIS: `▮`, the solid slab this
    # language already spends on its edited knob and on its pressed checkbox
    # mark. It is deliberately NOT a block element and NOT a box-drawing cell
    # -- "no boxes, at any width" is the commitment, and a rule stood on end
    # would have been a wall.
    CUR = "▮"
    SPIN = (".", "..", "...", " ")          # a walking period

    # structure by WEIGHT, which is what a hairline language has instead of
    # ornament: the passed extent is the heavy rule, the rest is the light
    # one. The old slider drew the same `─` on both sides of the knob — a
    # slider with no indicator, i.e. two parts where the registry says three.
    PART_GLYPHS = {
        # THE PASSED EXTENT IS A SLAB, NOT THE ERROR RUNG (inc46). This read
        # `━`, which is `LEVELS["error"]` -- so a switch that is ON and a log
        # row that has failed were the same cell, and the batch rule names
        # that seat by hand: a meaning may not stand at the INDICATOR of a
        # switch. `▀` is the RULE RISEN -- the half-height weight this language
        # already spends on a pressed radio -- so the passed extent is one
        # more step of the only ladder it owns and the top rung stays severity.
        #
        # NOT `▬`, which was the first answer and was wrong for a MEASURED
        # reason: `▬` over `─` is byte for byte darkside's bar, and
        # `verify_language`'s "no two languages draw the same bar either"
        # went red on it. A weight step that lands on another language's is
        # not a weight step this language owns.
        #
        # `main` KEEPS `─`, and the exemption is by EXTENT rather than by
        # silence: a rung is ONE cell at the head of a row, in a column that
        # aligns (ruling 8's whole point), and a track is a RUN of `n` cells
        # under a word. `DISCLOSE` is the same mark for the same reason. It
        # is the weakest of this file's exemptions and it is written down.
        "main": {DEFAULT: "─", DISABLED: "┈"},
        "indicator": {DEFAULT: "▀", DISABLED: "┅"},
        "knob": {DEFAULT: "│", FOCUSED: "┃", EDITED: "▮",
                 ACTIVE: "█", INVALID: "╲",
                 DISABLED: "┆"},
        # WEIGHT is this language's only ornament, so the box is two rules
        # and the state is how heavy they are. The mark is set INSIDE them,
        # which is the containment law non-vacuous: the two rules survive
        # every state and only the interior changes.
        # ONE MARK, ONE SIDE (inc46) -- inc38's answer for the button, taken
        # to the three controls that still enclosed. A wall is a PAIR: it is
        # border-shaped because it ENCLOSES, and this language's commitment is
        # "no boxes, at any width". The rule that led is kept and the rule
        # that closed is not set, so the ladder is unchanged (`│ ┃ █ ┆`, the
        # same four weights) and only the enclosure is gone. Same three cells,
        # same one width across four states, so no caller's row moves.
        #
        # THE MARK NO LONGER CARRIES THE STATE. It read `│▪│ / ┃▪┃ / █▮█ /
        # ┆·┆`: `▮` is now `CUR` and `·` is `LEVELS["info"]`, which put a
        # severity rung at a DISABLED seat -- the batch rule's third named
        # position. The square bullet is the CHECKED bit and nothing else;
        # the leading rule's weight is the control state, which is the one
        # channel this language has.
        "checkbox.main": {DEFAULT: "│  ", FOCUSED: "┃  ", ACTIVE: "█  ",
                          DISABLED: "┆  "},
        "checkbox.knob": {DEFAULT: "│▪ ", FOCUSED: "┃▪ ", ACTIVE: "█▪ ",
                          DISABLED: "┆▪ "},
        # THE TYPOGRAPHIC DISTINCTION, which this language of all ten is
        # entitled to make: a square bullet marks a box, a ROUND bullet marks
        # a choice. The rules shorten to half-height ticks so the well reads
        # lighter than the box beside it — Swiss separates by weight, and it
        # is spending weight here rather than inventing an ornament.
        # ONE MARK, ONE SIDE here too (inc46), on the half-height ticks this
        # control already had. AND THE ROUND BULLET IS `●` IN EVERY STATE:
        # the knob read `•`, which is `REQUIRED` (inc35, "the ladder's mark
        # set solid"), so an obligation beside a caption and a chosen option
        # in a group were one cell -- `swiss_S4` puts that same `•` on the
        # focus ring of an irreversible button. Obligation keeps `•`; the
        # choice takes the solid round bullet this knob already wore when it
        # was pressed. Square marks a box, round marks a choice, unchanged.
        "radio.main": {DEFAULT: "╵  ", FOCUSED: "╹  ", ACTIVE: "▀  ",
                       DISABLED: "╎  "},
        "radio.knob": {DEFAULT: "╵● ", FOCUSED: "╹● ", ACTIVE: "▀● ",
                       DISABLED: "╎● "},
        # THE ONE LANGUAGE THAT RENOUNCES THE WALLS, and the increment that
        # closed `inheritors-2` §8's last debt. This slot used to read
        # `│  │ / ┃  ┃ / █  █ / ┆  ┆` under a comment that said the walls
        # could not go, because "with the walls gone the four states would
        # separate on colour alone". THAT REASONING WAS FALSE, and it was
        # false in one word: it read the choice as WALLS OR NOTHING. A wall
        # is a PAIR — it is border-shaped because it encloses — and the third
        # option is ONE mark, on ONE side, which cannot enclose anything at
        # any width. That is what "no boxes, at any width" leaves standing.
        #
        # THE LADDER IS THIS LANGUAGE'S OWN AND NO GLYPH IS NEW. Swiss's
        # hierarchy device is WEIGHT ("hierarchy by weight, generous
        # emptiness"), and it already spends the dot at three weights:
        # `·` is `LEVELS["info"]` and `stepper.main`, `•` is `REQUIRED` (the
        # ladder's mark set solid, inc35) and `radio.knob`, `●` is that
        # knob's own ACTIVE cell — so a press here wears the cell this
        # language already presses with. Weight is a SHAPE channel, so the
        # four states survive greyscale, which the walls' defence claimed was
        # only reachable through a border.
        #
        # DISABLED IS AIR, and it is the one decision here that is not the
        # ladder. There is nothing lighter than `·` in this alphabet that is
        # not a dashed RULE (`┆ ╎ ┈`), which is the very shape being given
        # up. So the mark is simply not set — `stepper.step`'s own end
        # behaviour, three slots down: "the mark is simply not set, and the
        # word does not move because the field was reserved for it". A
        # control nobody may press is a word, which is what this language
        # would have said anyway.
        #
        # FOUR CELLS, SPLIT IN HALF LIKE EVERY OTHER LANGUAGE'S: the mark and
        # one cell of air lead the field, and the two cells that would have
        # closed it stay air. The seat's arithmetic is untouched — same even
        # count, same one width across four states, same overhead per label —
        # so a caller laying out a row of buttons sees no change and the word
        # still cannot move under the state.
        # THE LADDER LEAVES THE MARKS THAT MEAN SOMETHING (inc46). inc38's
        # ladder was `· • ●` and both of its lower rungs turned out to be
        # declarations: `·` is `LEVELS["info"]` -- `swiss_S3` opens
        # `╲Delete all╱`, the most dangerous control on the screen, with the
        # LOWEST rung of the severity ladder -- and `•` is `REQUIRED`, which
        # `swiss_S4` puts on the focus ring of an irreversible button.
        #
        # SO THE LADDER IS ONE SHAPE AT THREE WEIGHTS, which is what
        # "hierarchy by weight" has meant here all along, and the shape is the
        # square bullet this language already declares for a box: hollow,
        # inked, filled. Neither `▫` nor `■` is a new IDEA -- they are `▪` at
        # its two other weights -- and neither is a box-drawing cell or a
        # block element, so inc38's law (no wall around a button at any width,
        # derived from the codepoint) is untouched and still bites.
        #
        # DISABLED IS STILL AIR, for inc38's stated reason: there is nothing
        # lighter than the hollow square in this alphabet that is not a dashed
        # RULE, which is the shape being given up.
        "button.main": {DEFAULT: "▫   ", FOCUSED: "▪   ", ACTIVE: "■   ",
                        DISABLED: "    "},
        # THE LANGUAGE THAT WOULD RENOUNCE THE WALLS AND CANNOT, a second
        # time. A bare line of words is the honest swiss field — but a value
        # may fill every cell, so a walled-off field is the only place a full
        # one can say DISABLED without colour. It takes the thinnest rule that
        # carries a state, and it leaves the paper BLANK: the only language
        # here that spends nothing at all on its ground.
        # ONE MARK, ONE SIDE (inc46), and the comment above is the claim it
        # disproves. "A walled-off field is the only place a full one can say
        # DISABLED without colour" is the SAME false dichotomy inc38 already
        # took apart on the button: it reads the choice as WALLS OR NOTHING.
        # The LEADING rule says DISABLED whether the field is full or empty --
        # it is the first cell of the row and no value can reach it -- and
        # what the closing rule carried was the field's EXTENT, which in a
        # language whose divider is alignment is the next column's job.
        # Same three cells, same one width across six states.
        #
        # INVALID KEEPS ITS OWN FORM. `╲` is half this language's
        # `DANGER_FORM` and it opens the field the way every other state
        # opens it, so inc39's law is satisfied by construction: the mark
        # that opens a rejected field is a mark this language opens fields
        # with, and there is no closing mark left to turn round.
        "textfield.main": {DEFAULT: "│  ", FOCUSED: "┃  ", EDITED: "┃· ",
                           ACTIVE: "█  ", INVALID: "╲  ",
                           DISABLED: "┆  "},
        "textfield.caret": {DEFAULT: "▏"},
        # WEIGHT, the only ornament this language owns, spent on a shaft this
        # time: the track is the lightest rule it can draw and the view is
        # the heaviest. No box, no shading — a scroll bar here is one rule
        # whose weight changes where you are.
        "scrollbar.main": {DEFAULT: "┄", DISABLED: "·"},
        "scrollbar.indicator": {DEFAULT: "▬", DISABLED: "─"},
        # THE TYPOGRAPHIC MARK AGAIN, which this language of ten is entitled
        # to take: a chevron is a piece of punctuation before it is an
        # ornament, so a stepper here is set the way a printer would set it —
        # the guillemet family, opening under the finger. The end is SPACE
        # doing the work space does everywhere in this language: the mark is
        # simply not set, and the word does not move because the field was
        # reserved for it.
        "stepper.main": {DEFAULT: "··", DISABLED: "╎╎"},
        "stepper.step": {DEFAULT: "‹›", FOCUSED: "◃▹", EDITED: "◂▸",
                         ACTIVE: "██", INVALID: "›‹",
                         DISABLED: "┆┆"},
    }

    def value_label(self, val, state=DEFAULT):
        return f"  [{self.c['mut']}]{val}[/]"

    def spinner(self, tick):
        return f"[{self.c['mut']}]{self.SPIN[tick % len(self.SPIN)]:<3}[/]"

    def tabs(self, options, active):
        c = self.c
        return "   ".join(
            f"[{c['ink']}]{' '.join(o.upper())}[/]" if o == active
            else f"[{c['mut']}]{o}[/]" for o in options)


class Industrial(Kit):
    """Flat functional colour on grey; everything is labelled and bracketed;
    numbered because modes have numbers. Structure is the FUNCTION PLATE
    (`layout="panel"`): the head rule is gone, a phase is a plate legend, and
    every task is a solid plate-toned block stamped with its two-digit code.
    Under any other `layout` the previous boxed composition comes back."""

    # the plate "▐ nn ▌ " and its tight form "▐nn " (the narrow tier). Both
    # come OUT OF the content budget, exactly like the card's padding — a
    # plate that widened the row would wrap it (VERIFY.md's frame law).
    #
    # THE TIGHT TIER STILL CARRIES ITS CODE. The first render renounced the
    # code below the threshold, and the board showed two adjacent columns
    # wearing different plates — which reads as a bug, not a decision. A
    # signature that is only present on the wide columns is not a signature,
    # so the narrow tier gives up three cells of plate, never the number.
    PLATE_W = 7
    SHORT_W = 4

    # ======================================================================
    # THE SEVEN IT USED TO INHERIT (batch `kits-learn-4`, AC-5). LANGUAGES.md
    # §3: "~5 flat colours on grey · dense · BOXED GROUPS · plain cells ·
    # playful-industrial. Everything is NUMBERED AND LABELLED; colour codes
    # FUNCTION, not decoration ... FAILS: WHEN COLOUR MUST CARRY SEVERITY,
    # because the palette already spent colour on identity."
    #
    # That last clause decides three of the seven. A language that cannot put
    # severity on colour has to put it on SHAPE, and the shape it owns is the
    # STAMPED PLATE — the `▐ nn ▌` it already stamps on every card.
    # ======================================================================
    DISCLOSE = "▼"                        # solid, flat, stamped
    # THE STENCILLED BANG (inc48). This read `▐` -- "the plate, opened" --
    # and `▐` is the OPENING half of the plate every button and every field is
    # set in. `industrial_S2` is the frame: `title▐        ▐Fix login…▌`, the
    # obligation and the control's wall eight spaces apart on one row, and the
    # round's criterion is "decir cuál de los dos `▐` es la obligación". The
    # PLATE KEEPS THE CELL, because the plate is this language's whole
    # notation -- §3, "BOXED GROUPS ... EVERYTHING IS NUMBERED AND LABELLED"
    # -- and a control that stopped wearing it would stop being this language.
    #
    # SO OBLIGATION TAKES THE REGISTER'S OWN ATTENTION CODE. This vocabulary
    # is ASCII stencil (`| I X # x _ - . = @ O o`), and §3's own failure
    # clause -- "FAILS WHEN COLOUR MUST CARRY SEVERITY, because the palette
    # already spent colour on identity" -- is what pushed severity onto the
    # square's SIZE (`▫▫ ▪▪ ■■`). That leaves `!` unspent here, and it is what
    # a panel stencils beside a control that must be set before the machine
    # will run. It is not a severity rung in this language, and it is not a
    # number: L-33 rules the digits are the MODES, and an obligation is not a
    # mode.
    REQUIRED = "!"

    def pane_split_rule(self, h: int, w: int = 3) -> list[str]:
        """TWO PLATES, FACING — the one of the eleven whose commitment ASKS
        for a box, ruling a pane seat in its own chrome.

        §3: "boxed groups". This language is documented as the only one here
        whose commitment wants a frame, and inc32 already made it draw its
        modal lid in half-cell plate rather than the terminal's hairline
        (`MODAL_BOX = DISPLAY_BOX`). A gutter is the same claim: the left pane
        CLOSES and the right pane OPENS, each in its own plate.

        THE ORDER IS `keyhint`'S, not a new one. That row plates a key as
        `▐up▌` — the ink faces the CONTENT on both sides — so a gutter closes
        the left pane with `▌` and opens the right with `▐`, and the air
        between is the panes' own separation rather than a second mark. Read
        the two rows together and it is one convention, which is the whole
        argument for a language having an alphabet.

        Below two cells there is no room for two plates and the seat falls
        back to one, because `w` is a seat and a short row would move the
        right pane down the page."""
        rows = max(0, h)
        if w < 2:
            return [self._split_cell(self.DISPLAY_BOX[7], self.c["dim"], w)
                    for _ in range(rows)]
        dim = self.c["dim"]
        row = (f"[{dim}]{mark(self.DISPLAY_BOX[6])}[/]" + " " * (w - 2)
               + f"[{dim}]{mark(self.DISPLAY_BOX[7])}[/]")
        return [row for _ in range(rows)]
    DANGER_FORM = ("╱╱", "╱╱")           # hazard striping, and not a hue
    LEVELS = {"info": "▫▫", "warn": "▪▪", "error": "■■"}
    MATCH_STYLE = "reverse {accent}"       # a plate struck over the run
    # THE BOX THIS LANGUAGE IS ALLOWED, and the only one of the eleven whose
    # commitment ASKS for one: "boxed groups". Drawn in the same half-cell
    # plate chrome `DISPLAY_BOX` already stamps, so the dialog is a plate like
    # everything else here rather than a terminal's hairline lid.

    def field_row(self, caption, value, w):
        """THE CAPTION IS LABELLED; THE FIGURE IS NOT PLATED (inc48).

        This row used to set the value in `▐ … ▌` under the argument that
        "everything is numbered and labelled, and the thing this language
        labels WITH is the stamped plate". The plate half of that is right and
        the argument proved too much: `▐ … ▌` is BYTE FOR BYTE this language's
        DEFAULT button, so `industrial_S3` printed

            DANGER ZONE                       ▐ delete every completed task ▌
            ▐ ╱╱Delete all╱╱ ▌   7 tasks, not recoverable

        -- a sentence describing a consequence, plated exactly like the
        irreversible control on the next row. The round's criterion is
        "señalar los elementos pulsables de las dos últimas filas": there are
        two plates and only one of them is a control.

        THE REFERENCE IS `nord_S3`, the one of the seven that already got this
        right -- bare caption, bracketed button. So the plate goes back to
        meaning what it means everywhere else here: a STAMP on a code, on a
        display, or on a CONTROL. A definition row is none of the three. The
        caption stays UPPERCASE, which is the "labelled" half and costs no
        chrome, and the figure stands in the ink tier on air.

        What is left is the base's composition with this language's register
        laid over it, and that is the honest reading: what industrial had to
        say about a definition row was the capitals, not the walls."""
        c = self.c
        cap, val = str(caption).upper(), str(value)
        gap = max(1, w - len(cap) - len(val))
        return (f"[{c['mut']}]{mark(cap)}[/]" + " " * gap
                + f"[{c['ink']}]{mark(val)}[/]")

    def keyhint(self, pairs, w=0):
        """THE KEY IS ON A PLATE AND THE LABEL IS THE LEGEND BESIDE IT — the
        same two parts every plate on this board has. Corgi brackets its
        keys; this language stamps them, which is the difference between a
        silkscreened panel and a machined one."""
        c = self.c
        return "   ".join(f"[{self.plate}]{mark('▐')}[/]"
                          f"[{c['ink']}]{mark(str(k_))}[/]"
                          f"[{self.plate}]{mark('▌')}[/] "
                          f"[{c['mut']}]{mark(str(v).upper())}[/]"
                          for k_, v in pairs)
    TAB_W = 3                                  # the legend's "▐▌ " tab
    CODE_MIN = 24

    @property
    def panel(self) -> bool:
        """The plate composition, dispatched on the token — the same shape as
        `Darkside.rail_width` and `Naught.lattice`. A hardcoded plate would
        make `layout` dead metadata again (PENDING item 0)."""
        return self.layout == "panel"

    @property
    def plate(self) -> str:
        return self.t.get("plate", self.c["dim"])

    # THE DISPLAY POSTURE, IN THIS LANGUAGE'S FRAME. Shared mechanism with
    # corgi (AC-2), different chrome: corgi's display is a drawn box with
    # square junctions on green-black glass; industrial's is a STAMPED PLATE,
    # so its top edge and its bottom edge are different glyphs and its sides
    # are half-cell walls. And the glass is GREY — LANGUAGES.md is explicit
    # that severity still cannot ride colour inside this display, so the
    # screen's ramp is ground-to-ink with no hue in it at all.
    DISPLAY_BOX = "▛▜▙▟▀▄▌▐"

    # AND THE DIALOG IS ONE TOO (kits-learn-4). This is the only language of
    # the eleven whose commitment ASKS for a box -- "boxed groups" -- and the
    # box it owns is this plate. `MODAL_BOX` takes `DISPLAY_BOX`'s order for
    # exactly this: a language that has already declared its frame should
    # hand the same string to both seats rather than spell its corners twice.
    MODAL_BOX = DISPLAY_BOX

    def display_chrome(self) -> tuple[str, str, str]:
        return self.DISPLAY_BOX, self.t.get("ground", "#000000"), self.c["ink"]

    def plate_w(self, w: int) -> int:
        """How wide the plate WILL be at this measure — asked before it is
        drawn, so a caller can budget the row rather than discover the
        overflow (naught's `plain_width` lesson)."""
        return self.PLATE_W if w >= self.CODE_MIN else self.SHORT_W

    def plate_stamp(self, idx: int, tone: str, w: int) -> str:
        """The plate's left edge, colour-coded by FUNCTION (the tone the card
        already carries: warn for urgent, mut for the rest) and stamped with
        the card's position code. Two digits, so a stack of plates reads as a
        run; the code wraps at 100, which no column reaches."""
        c = self.c
        code = f"[{c['mut']}]{(idx + 1) % 100:02d}[/]"
        if w < self.CODE_MIN:
            return f"[{tone}]▐[/]{code} "
        return f"[{tone}]▐[/] {code} [{tone}]▌[/] "

    def head(self, name, count, w, idx=0):
        if not self.panel:
            return self._flow_head(name, count, w, idx)
        # THE PLATE LEGEND: the phase names its plate stack from a solid band,
        # and the rule that used to divide them is gone — the ground does that
        # job now (HIERARCHY.md ranks a shared background above a rule).
        #
        # The leading cell is the SEAT's now (`.col-head { padding-left: 1 }`,
        # base tcss). It used to be paid here in the markup, because paying it
        # in TCSS while `kanban.py` still measured the head apart from its
        # cards left this legend — which fills its measure exactly — no slack
        # to absorb the narrower box, and it WRAPPED. `row_width` hands the
        # head the card's own measure now, so the box is never the tighter one.
        c = self.c
        w = max(6, w)
        budget = w - self.TAB_W - 5
        # the legend renounces its number before it crushes the phase name:
        # a legend with no name names nothing
        num, nw = ("", 0)
        if self.numbered and budget >= 4:
            num, nw = f"[{c['accent']}]\\[{idx + 1}][/]", 3
        room = max(1, budget - nw)
        nm = name.upper()[:room]
        pad = " " * (room - len(nm))
        return (f"[on {self.plate}][{c['accent']}]▐▌[/] {num}"
                f"[{c['ink']}]{nm}[/]{pad} [{c['mut']}]\\[{count:>2}][/][/]")

    def _flow_head(self, name, count, w, idx=0):
        c = self.c
        num = f"[{c['accent']}]\\[{idx + 1}][/]" if self.numbered else ""
        room = max(1, w - 9)
        line = (num + f"[{c['ink']}]{name.upper()[:room]}[/] "
                f"[{c['mut']}]\\[{count:>2}][/]")
        rule = self.rule_line(w)
        return line if rule is None else line + "\n" + rule

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        if not self.panel:
            return self._flow_card_row(title, chip, tone, w, idx, urgent)
        c = self.c
        pw = self.plate_w(w)
        inner = max(1, w - pw)
        # the chip is DATA and is budgeted first; the title absorbs the loss
        # (app.py's measured lesson: a clipped row keeps its figure)
        tag = chip[: max(0, inner - 4)]
        tail = f" [{tone}]\\[{tag}][/]" if tag else ""
        room = max(0, inner - (len(tag) + 3 if tag else 0))
        body = _fit(title, room)
        pad = " " * (room - min(len(title), room))
        return (f"[on {self.plate}]{self.plate_stamp(idx, tone, w)}"
                f"[{c['ink']}]{body}[/]{pad}{tail}[/]")

    def _flow_card_row(self, title, chip, tone, w, idx=0, urgent=False):
        c = self.c
        mark = f"[{tone}]▪[/] " if urgent else f"[{c['dim']}]▪[/] "
        room = max(1, w - len(chip) - 6)
        body = _fit(title, room)
        pad = " " * max(0, room - min(len(title), room))
        return mark + f"[{c['ink']}]{body}[/]{pad} [{tone}]\\[{chip}][/]"

    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        if not self.panel:
            return self._flow_card_rows(title, chip, tone, w, idx, urgent, meta)
        # the tag row hangs under the plate's right edge and wears the same
        # ground, so a task reads as ONE block rather than two rows
        top = self.card_row(title, chip, tone, w, idx, urgent)
        m = meta or {}
        c = self.c
        pw = self.plate_w(w)
        inner = max(1, w - pw)
        d = m.get("days")
        due = "--" if d is None else f"{d}D"
        ph = (m.get("phase") or "--")[:4].upper()
        pr = (m.get("prio") or "-")[:1].upper()
        sub, used = "", 0
        for mk, pl in ((f"[{c['mut']}]\\[PH:{ph}][/]", f"[PH:{ph}]"),
                       (f"[{c['mut']}]\\[DUE:{due}][/]", f"[DUE:{due}]"),
                       (f"[{c['mut']}]\\[PR:{pr}][/]", f"[PR:{pr}]")):
            if used + len(pl) > inner:
                break
            sub += mk
            used += len(pl)
        return [top, f"[on {self.plate}]{' ' * pw}{sub}"
                     f"{' ' * (inner - used)}[/]"]

    def _flow_card_rows(self, title, chip, tone, w, idx=0, urgent=False,
                        meta=None):
        # everything labelled, everything bracketed — the machine tag row
        top = self.card_row(title, chip, tone, w, idx, urgent)
        m = meta or {}
        c = self.c
        d = m.get("days")
        due = "--" if d is None else f"{d}D"
        ph = (m.get("phase") or "--")[:4].upper()
        pr = (m.get("prio") or "-")[:1].upper()
        sub = _fit_parts([
            ("  ", "  "),
            (f"[{c['mut']}]\\[PH:{ph}][/]", f"[PH:{ph}]"),
            (f"[{c['mut']}]\\[DUE:{due}][/]", f"[DUE:{due}]"),
            (f"[{c['mut']}]\\[PR:{pr}][/]", f"[PR:{pr}]"),
        ], w)
        return [top, sub]

    def tile_row(self, val, label, tone, w):
        c = self.c
        room = max(0, w - len(val) - 5)
        return (f"[{tone}]{val}[/] [{c['dim']}]│[/] "
                f"[{c['mut']}]{label[:room].upper()}[/]")

    def sect(self, title, note, w, h=0):
        # drawn type RENOUNCED: a machine panel labels, it does not draw
        c = self.c
        return [f"[{c['mut']}]\\[[/][{c['ink']}]{title}[/][{c['mut']}]][/]  "
                f"[{c['mut']}]{note}[/]", self.rule_line(w) or ""]

    GANTT = ("▬", "█", "│", "·", "◆")

    def cal_cell(self, state):
        c = self.c
        return {"none": f"[{c['dim']}]░░[/]",
                "over": f"[{c['alert']}]██[/]",
                "multi": f"[{c['accent']}]██[/]",
                "one": f"[{c['warn']}]▓▓[/]"}[state]

    def composition(self):
        # a compact machine panel: nothing floats, the readouts are BOXED
        return """
        #ap { padding: 0 1; }
        Screen.sz-board #hero { height: 7; min-height: 7; }
        #meter { border: solid #4a4a4a; height: 4; }
        Screen.sz-board #tiles { border: solid #4a4a4a; height: 3; }
        """

    # bracketed single-letter codes — labelled, like everything here
    ICONS = {"deadline": "\\[D]", "overdue": "\\[O]", "wip": "\\[W]",
             "blocked": "\\[B]", "workday":"\\[$]", "boardfile":"\\[F]"}

    # everything labelled, everything bracketed
    #
    # THE STAMPED POINTER (inc45). This read `▪`, which is the middle rung of
    # this language's severity ladder (`▫▫ / ▪▪ / ■■`) -- and that ladder is
    # not optional here: LANGUAGES.md §3 says this palette "FAILS WHEN COLOUR
    # MUST CARRY SEVERITY, because the palette already spent colour on
    # identity", so severity has nowhere to go but the square's SIZE. Severity
    # keeps the three squares; the cursor leaves the family altogether and
    # takes `DISCLOSE`'s own form -- "solid, flat, stamped" -- turned ninety
    # degrees, which is the one thing a stamped pointer can be that a size
    # rung cannot be mistaken for.
    CUR = "▶"
    # THE FOURTH MARK IS NOT A BACKSLASH, and that is a measured defect
    # rather than a taste. `\` is the ONE character that cannot stand at the
    # end of a markup string's literal text (PENDING #31): both parsers read
    # it as escaping the `[` of the close tag, so `[tone]\[/]` prints a raw
    # `[/]` and closes nothing — and this spinner is emitted exactly that way
    # (`Kit.spinner`), so industrial's spinner row was putting `[/]` on the
    # gallery and the aperture every fourth frame. Found by the motion pass,
    # which consumes `SPIN` as a language's in-transit glyph and would have
    # inherited it. The rotation is unchanged; only the glyph that carries it
    # is one this app can print.
    SPIN = ("|", "/", "-", "╲")

    # one tick between states — a relay clicking, 60ms
    MOTION_STEPS = 1

    # bracketed and CODED, the way this language labels everything: the knob
    # is an ASCII code, the family of its switch (`[X]` / `[ ]`). The old
    # slider drew a filled run inside brackets and no knob — a boxed BAR.
    COMP_CHROME = ("[", "]")
    PART_GLYPHS = {
        "main": {DEFAULT: "·", DISABLED: "-"},
        "indicator": {DEFAULT: "█", DISABLED: "░"},
        "knob": {DEFAULT: "|", FOCUSED: "I", EDITED: "X",
                 ACTIVE: "#", INVALID: "/",
                 DISABLED: "x"},
        # the ASCII checkbox this language was already quoting when its
        # SWITCH drew `[X]` / `[ ]` — a coded mark in a fixed box, which is
        # what a checkbox IS and what a switch is not. The box loses its
        # square brackets when the control is dead: round brackets are this
        # vocabulary's way of saying "not an input".
        "checkbox.main": {DEFAULT: "[ ]", FOCUSED: "[_]", ACTIVE: "[-]",
                          DISABLED: "(-)"},
        "checkbox.knob": {DEFAULT: "[X]", FOCUSED: "[#]", ACTIVE: "[*]",
                          DISABLED: "(x)"},
        # THE ROTARY SELECTOR, and it could NOT take the round bracket every
        # other language's radio takes: this vocabulary has already spent
        # round brackets on "not an input" (see the checkbox's DISABLED row).
        # A language's own declared law overrules the family convention, so
        # the selector is angled instead — and the DISABLED radio keeps the
        # round bracket, because here that means dead and it still does.
        "radio.main": {DEFAULT: "< >", FOCUSED: "<_>", ACTIVE: "<->",
                       DISABLED: "(-)"},
        "radio.knob": {DEFAULT: "<O>", FOCUSED: "<#>", ACTIVE: "<@>",
                       DISABLED: "(o)"},
        # THE PLATE, which this language already stamps on every card
        # (`▐ nn ▌`) — the button is that plate with a word on it instead of
        # a number. The seat idiom carries the state exactly as the checkbox's
        # does: `_` seated, `#` struck, and the DISABLED plate keeps the round
        # bracket, because in this vocabulary round brackets mean dead.
        "button.main": {DEFAULT: "▐  ▌", FOCUSED: "▐__▌", ACTIVE: "▐##▌",
                        DISABLED: "(--)"},
        # THE PLATE with a machined face — the same ▐ ▌ it stamps on every
        # card. The paper is punched with its own dot; the dead plate keeps
        # the round bracket, because here round brackets mean dead.
        # INVALID IS PUNCHED PAPER, NOT A TURNED PLATE (inc39). It read
        # `▌/▐`: the plate with its ink facing OUT, away from the words it
        # holds, which is the one thing this vocabulary never does -- "the
        # ink looks at the content" is what makes a plate read as a plate.
        # The plate goes back the way it is set in every other state and the
        # hatch `/` in the paper carries the sixth, which is exactly where
        # this table already puts `·`, `_`, `-` and `#`.
        "textfield.main": {DEFAULT: "▐·▌", FOCUSED: "▐_▌", EDITED: "▐-▌",
                           ACTIVE: "▐#▌", INVALID: "▐/▌",
                           DISABLED: "(-)"},
        "textfield.caret": {DEFAULT: "|"},
        # ASCII AND CODED, this language's whole register, and its bracketed
        # chrome fixes the ends of the shaft exactly as it fixes its
        # slider's — the same `comp_chrome` seat, reached by the same
        # registry fact (an indicator is declared, so there is a track with
        # ends). The travelled run is hatched; the view is struck.
        "scrollbar.main": {DEFAULT: "-", DISABLED: "."},
        "scrollbar.indicator": {DEFAULT: "#", DISABLED: "="},
        # ASCII AND CODED, and the ROUND BRACKET LAW reaches this component
        # too: this vocabulary spends `( )` on "not an input", so a dead
        # stepper wears it and a live one is angled. The end stop is the
        # bare seat dot the track is made of — no bracket at all, because a
        # step that does not exist is not a dead control, it is an absent
        # one, and this language distinguishes those.
        "stepper.main": {DEFAULT: "..", DISABLED: "--"},
        "stepper.step": {DEFAULT: "<>", FOCUSED: "{}", EDITED: "[]",
                         ACTIVE: "##", INVALID: "><",
                         DISABLED: "()"},
    }

    def tabs(self, options, active):
        # active mode in caps, the rest lowercase — state readable without
        # colour (the 2-channel law, COMPONENTS.md)
        c = self.c
        return " ".join(
            f"[{c['accent']}]\\[{i + 1}][/]"
            + (f"[{c['ink']}]{o.upper()}[/]" if o == active
               else f"[{c['mut']}]{o}[/]")
            for i, o in enumerate(options))


class Nord(Kit):
    """The terminal's own conventional idiom (base16 doctrine) — everything
    nord renders is inherited from `Kit`, which was WRITTEN as nord, and that
    stays true. This subclass exists for exactly one commitment: the board is
    a MASTER/DETAIL SPLIT (`layout="split"`).

    Why the split, measured rather than asserted: colour-stripped at 118x30
    nord had NO first fixation. Ranked by ink cells and by the weighted
    channel sum 0.2126R+0.7152G+0.0722B, the brightest ink on screen belonged
    to TEN repeated card titles (238.7, 200 cells) and the only isolated
    element — the hero numeral — came FIFTH (117.7, 25 cells) behind the load
    plot standing beside it in the same panel (181.2, 61 cells). Nothing won
    area AND brightness AND isolation, which is HIERARCHY.md's self-check.

    The split gives the eye one subject. HIERARCHY.md's sidebar+detail
    pattern is quoted here because its wording is load-bearing: "a narrow
    list (25-30 %) driving a wide detail pane. THE LIST KEEPS SELECTION
    STATE; the detail pane is the only thing that changes." Selection is
    constitutive of the pattern, so the detail follows the real cursor
    (`KanbanBoard.on_card_focused`) — a static default would have been an
    imitation of the pattern, not the pattern.

    Under any other `layout` every method below falls through to `super()`,
    i.e. the base kit, and nord renders byte-for-byte as it always did."""

    # ======================================================================
    # THE SEVEN THIS LANGUAGE DOES NOT OVERRIDE, AND WHY THAT IS AN ANSWER
    # (batch `kits-learn-4`, AC-5). `field_row`, `DISCLOSE`, `DANGER_FORM`,
    # `LEVELS`, `MATCH_STYLE`, `keyhint` and `overlay` all come from `Kit`
    # here, and for this ONE language that is a commitment rather than a gap.
    #
    # LANGUAGES.md §6 (base16 / theme-native): "the only language here that
    # INHERITS THE USER'S ENVIRONMENT instead of overriding it — the app looks
    # like the rest of their terminal ... Fails: when you need a distinctive
    # identity — BY CONSTRUCTION IT HAS NONE OF ITS OWN."
    #
    # A right-flushed two-column list, a `▾` disclosure, `!` for danger, the
    # `· / ! / !!` level ladder, bold accent on a match, `key label` hints and
    # a `┌─┐` modal are the terminal's own conventions, and the base kit WAS
    # written as nord. Giving this language a mechanism of its own would not
    # be filling a hole; it would be leaving base16 doctrine.
    #
    # AND IT IS ASSERTED RATHER THAN WRITTEN HERE. A block of comments is a
    # promise; `test_nord_declares_the_environment_and_the_declaration_is_
    # checked` walks the MRO for all seven and requires the owner to be `Kit`,
    # so a mechanism landing on nord by accident goes red and one landing on
    # purpose has to delete this paragraph first.
    # ======================================================================

    # HIERARCHY.md's own figure for a driving list. A LAW of the pattern, not
    # a choice this language gets to make — so it is a constant, not a token.
    SHARE = 0.30
    # the gutter is SPACE, not a rule: HIERARCHY.md ranks proximity above a
    # stroke, and nord already spends its one `frame="rule"` under the heads.
    GUTTER = 3

    @property
    def split(self) -> bool:
        return self.layout == "split"

    @property
    def floors(self) -> tuple[int, int]:
        """(master floor, detail floor) in cells, from the `split` token."""
        m, d = self.t.get("split", (28, 34))
        return int(m), int(d)

    def panes(self, w: int) -> tuple[int, int]:
        """THE geometry seat: the renderer and the acceptance checks both read
        this, so "the panes and the checks agree" is true by construction
        rather than by two copies of the arithmetic (the `Ledger.cols` /
        `Swiss.grid` precedent).

        Returns `(master, detail)` where the master owns columns
        `[0, master)`, the gutter `[master, master + GUTTER)`, and the detail's
        CONTENT begins at `master + GUTTER`. `detail == 0` is the degrade:
        below `master_floor + GUTTER + detail_floor` the split is RENOUNCED
        and the master takes the full width. It is never wrapped — a wrapped
        pane costs the board a card row, which is the trap the panel legend
        and the ledger page both sprang."""
        mf, df = self.floors
        if w < mf + self.GUTTER + df:
            return (max(1, w), 0)
        m = max(mf, round(w * self.SHARE))
        d = w - m - self.GUTTER
        if d < df:                     # the detail buys its measure back
            m, d = w - self.GUTTER - df, df
        return (m, d)

    def board_layout(self):
        return "split" if self.split else super().board_layout()

    def composition(self):
        if not self.split:
            return super().composition()        # "" — the byte-exact restore
        mf, df = self.floors
        return f"""
        .kb-split {{ height: 1fr; }}
        .kb-master {{ min-width: {mf}; height: 1fr; }}
        .kb-detail {{ min-width: {df}; height: 1fr; padding: 0 0 0 {self.GUTTER}; }}
        """

    # -- the MASTER row: one task, one row, the cursor on the driven one ----
    def master_row(self, title: str, chip: str, tone: str, w: int,
                   cursor: bool = False) -> str:
        """Compact by commitment: the list is not the subject, so it renounces
        the base kit's second (metadata) row — that field now has a whole pane.

        The brightness ladder is what makes the detail title winnable
        (HIERARCHY.md: dim -> normal -> bright, and stop at three): unselected
        rows are `mut`, the driven row is `ink`, and NOTHING here is bold.
        Bold ink is spent once, in the detail title, and that is the entire
        mechanism behind law 03 holding in this view."""
        c = self.c
        lead = f"[{c['accent']}]{self.CUR}[/] " if cursor else "  "
        room = max(1, w - 2 - len(chip) - 1)
        body = _fit(title, room)
        pad = " " * max(0, room - min(len(title), room))
        hue = c["ink"] if cursor else c["mut"]
        return f"{lead}[{hue}]{body}[/]{pad} [{tone}]{chip}[/]"

    # -- the DETAIL pane: one task, expanded, and the screen's fixation -----
    def detail_rows(self, title: str, chip: str, tone: str, w: int,
                    meta: dict | None = None) -> list[str]:
        """The title is THE first fixation, and it wins all three levers on
        purpose:

          area       — letterspaced through `display_cap()`, the base kit's
                       own display register, so it occupies ~2x the cells of
                       any master row's title
          brightness — the only BOLD ink anywhere on the board
          isolation  — a blank row above and below it, and nothing else in
                       either pane has both

        Quantity below is nord's `meter="blocks"` family (the same filled/
        unfilled block pair `_meter_blocks` draws), because a language that
        shows quantity with a second mechanism has two."""
        c = self.c
        m = meta or {}
        cap = max(1, (w + 1) // 2)          # letterspacing doubles the width
        cut = title if len(title) <= cap else title[: max(1, cap - 1)] + "…"
        rows = ["", f"[{c['ink']} bold]{mark(self.display_cap(cut))}[/]", ""]

        def field(label: str, value: str, hue: str) -> str:
            if not value:
                return ""
            room = max(1, w - 10)
            return (f"[{c['dim']}]{label.upper()[:9]:<9}[/]"
                    f"[{hue}]{mark(value[:room])}[/]")

        idx = int(m.get("phase_idx", 0)) + 1
        n = max(1, int(m.get("n_phases", 1)))
        bar_w = max(4, min(20, w - 16))
        lit = max(0, min(bar_w, round(bar_w * idx / n)))
        state = ("done" if m.get("done") else
                 "blocked" if m.get("blocked") else "open")
        # the chip is a due chip OR a state word ("blk"/"done"/"--"), and a
        # state word printed under a DUE label is a lie the render caught:
        # "DUE  blk" was on screen. The state has its own field below.
        due = "" if chip in ("blk", "done", "--") else chip
        for line in (field("project", m.get("proj", ""), c["mut"]),
                     field("phase", m.get("phase", ""), c["mut"]),
                     field("due", due, tone),
                     field("priority", str(m.get("prio", "")), c["mut"]),
                     field("state", state,
                           c["alert"] if state == "blocked" else c["mut"])):
            if line:
                rows.append(line)
        rows.append("")
        # THE SAME PAIR `_meter_blocks` DRAWS (inc47), and it has to be: the
        # docstring metric this whole layout exists to satisfy was measured on
        # THIS row, not on the frame's. `Nord.__doc__`: "the only isolated
        # element, the hero numeral, came FIFTH behind the LOAD PLOT standing
        # beside it in the same panel". A near-solid block run out-weighs a
        # line of text at any length, and the split cannot give the eye one
        # subject while the pane below it carries a slab. The terminal's own
        # progress bar is two RULES -- Rich draws its own with `━` -- so the
        # complete and the remaining still differ in SHAPE (greyscale holds)
        # at roughly a seventh of the coverage. Two seats, one mechanism.
        rows.append(f"[{c['dim']}]{'PROGRESS':<9}[/]"
                    f"[{c['accent']}]{'━' * lit}[/]"
                    f"[{c['dim']}]{'─' * (bar_w - lit)}[/]"
                    f" [{c['mut']}]{idx}/{n}[/]")
        return rows


class Darkside(Kit):
    """Moonshot's language (ported from the Kimi fork, then held to this
    repo's laws): achromatic greys; the ONE accent (KMBlue) is spent
    EXCLUSIVELY on interactive affordances — the knob, the switch state, the
    active tab. Passive data is grey STEPS whose levels ride on SHAPE (the
    fork's grey-on-grey meter died in greyscale — fixed here). Depth is a
    background grey-step, never a border. Lowercase register; identity is a
    date-driven moon doodle on a deliberately recessive wordmark."""

    PHASES = ("( )", "(.)", "(o)", "(O)", "(o)", "(.)")

    RAIL = "▏"
    RAIL_W = 3                             # the stroke plus two cells of air

    # ======================================================================
    # THE SEVEN IT USED TO INHERIT (batch `kits-learn-4`, AC-5). LANGUAGES.md
    # §8: "achromatic + ONE RESERVED ACCENT · airy · DEPTH BY ±1 GREY STEP,
    # NEVER BORDERS · plain cells · clinical-warm ... the accent marks
    # interactivity, NOTHING ELSE ... hierarchy by WEIGHT AND DIMMING, not
    # size ... BORDERS ARE RESERVED FOR MODALS."
    #
    # The reservation is the interesting half. Prism inherited this doctrine
    # and spends it: it is the one language `MODAL_BORDER_REFUSED` leaves out.
    # So does its parent -- but not in the terminal's hairline. A
    # clinical-warm system rounds its one box, which is the whole difference
    # between the two languages' lids and is why `MODAL_BOX` is a seat.
    # ======================================================================
    DISCLOSE = "▿"                        # hollow: airy, and not the solid ▾
    def pane_split_instead(self, h: int, w: int = 3) -> list[str]:
        """THE STEP, and it is this language's whole structure device.

        §8: "regions separate by a ±1 grey-ramp step of BACKGROUND, not by
        box-drawing ... borders are reserved for modals". Two panes are two
        regions, and this language has exactly one answer to "these are
        different regions" — the same `depth_ground()` its backdrop uses.

        PRISM WRITES THIS METHOD TOO, and the duplication is deliberate.
        Prism is `Kit`'s child, not this class's: it INHERITED the doctrine
        from a borrowed language and then kept it. Making one call the other
        would assert a class relationship the file does not have, to save four
        lines.

        AND IT DOES NOT SURVIVE THE `.txt`: a background is not a cell, so a
        cell grid shows `w` spaces. It DOES survive greyscale, which is the
        law that applies — a grey step is a step with every hue removed."""
        return [f"[{self.c['mut']} on {self.depth_ground()}]{' ' * w}[/]"
                for _ in range(max(0, h))]

    # THE REQUIRED MARK — ONE SOLID CELL, ACHROMATIC. §8: "achromatic + ONE
    # RESERVED ACCENT ... hierarchy by WEIGHT AND DIMMING, not size", and the
    # accent "marks interactivity, NOTHING ELSE". A required field is neither
    # interactive nor an alarm, so the accent is unavailable by commitment and
    # the ladder (`· / o / O`) is spoken for by severity. What is left is the
    # channel this language actually names: weight. `▪` is the heaviest a
    # single achromatic cell gets without becoming a border, and a border is
    # the one thing this language has forbidden itself.
    REQUIRED = "▪"
    DANGER_FORM = ("Ø", "Ø")               # its own INVALID wall, the struck mark
    # A DIMMING LADDER MADE OF ITS OWN CURSOR. `CUR` is `O`; the ladder is
    # that mark losing and gaining weight, which is this language's stated
    # hierarchy device ("weight and dimming, not size") turned into three
    # shapes so the level still sorts with the colour taken away.
    LEVELS = {"info": "· ", "warn": "o ", "error": "O "}
    # THE ACCENT IS RESERVED FOR WHAT IS ACTIONABLE and a search hit is not:
    # it is a place in the text, not a thing to press.
    #
    # AND IT IS A GREY STEP, NOT A WEIGHT (inc48). This read `bold {ink}`, and
    # `darkside_S6` is the round's worst `S6` for a structural reason rather
    # than an exporter one: in a language that has renounced hue BY
    # COMMITMENT, `bold {ink}` is weight and nothing else, and a terminal that
    # renders bold as "brighter" -- the default in a large share of them --
    # leaves this language ZERO channels for the match. The criterion is
    # "circular el `re` que casó", and it was unanswerable in the artefact AND
    # probably in the destination.
    #
    # §8 names the channel this language actually owns: "DEPTH BY ±1 GREY STEP
    # of background, NEVER borders". A matched run is a region of the row, so
    # it takes the same step -- the ground comes up one rung of the ramp and
    # the text sits on it. Not a hue (the ramp is achromatic), not the
    # reserved accent, not weight; so it survives the one terminal
    # configuration `bold` does not.
    MATCH_STYLE = "reverse {mut}"
    MODAL_BOX = "╭╮╰╯──││"     # rounded: the "clinical-WARM" half

    def field_row(self, caption, value, w):
        """QUIET LOWERCASE, AIR, AND THE FIGURE'S OWN SEAT.

        Two of this language's four traits meet in one row. The caption is
        LOWERCASED, which is `tile_row`'s habit here and `display_cap`'s
        override ("quiet lowercase") — hierarchy by register rather than by
        size. And the figure stands on one `RAIL`-weight mark of its own.

        AND THE FIGURE'S SEAT IS AIR (inc48). This row used to set one `▬` in
        front of the value -- "a single cell that says where the figure
        begins" -- and `▬` is BYTE FOR BYTE the opening shoulder of this
        language's DEFAULT button, so `darkside_S3` printed

            danger zone                        ▬ delete every completed task
            ▬ ØDelete allØ ▬   7 tasks, not recoverable

        on consecutive rows: a sentence and an irreversible control opening
        with one cell. The round's criterion is "señalar los pulsables de las
        dos últimas filas", and `nord_S3` is the one language of the seven
        that already answered it -- bare caption, bracketed button.

        THE SEAT BECOMES THE SMALLEST RING THIS ALPHABET DRAWS. `◦` is spent
        on nothing here but an unchosen radio -- it is not a rung, not a
        control's shoulder, not a switch indicator and not a disabled mark --
        and it is the lightest cell available, which is what a seat under a
        figure should be in a language whose second word is AIRY.

        NOT THE RAIL, and the reason is a MEASUREMENT rather than a taste.
        `▏` was the first answer, because this docstring had always claimed
        the mark was "RAIL-weight" -- but `darkside_S1`'s objection is that
        this language "se prohibió el trazo vertical en el único sitio donde
        hacía falta y lo imprime catorce veces donde no", and routing the
        detail pane's six field rows through the rail took that frame from 16
        vertical strokes to 22. A fix that makes the frame it was measured
        against worse is not a fix.

        AND THE ROW MAY NOT SIMPLY GO BARE, which is worth writing down rather
        than discovering twice. Dropping the mark makes this method byte for
        byte `Kit`'s -- `test_no_two_languages_answer_a_mechanism_the_same_way`
        went red on `[["nord", "darkside"]]` -- and "the caption is lowercased"
        is not a difference when the caller's caption is already lowercase. A
        language that answers a mechanism by deleting its answer has not
        answered it."""
        c = self.c
        cap, val = str(caption).lower(), str(value)
        gap = max(1, w - len(cap) - len(val) - 2)
        return (f"[{c['dim']}]{mark(cap)}[/]" + " " * gap
                + f"[{c['dim']}]{mark('◦')}[/] "
                + f"[{c['ink']}]{mark(val)}[/]")

    def keyhint(self, pairs, w=0):
        """Airy, dim, lowercase, and the pairs separated by a middot with air
        on both sides — the calmest divider available that is still a mark.
        The key carries the one accent because the key is the actionable
        thing on the row, which is this language's rule for spending it."""
        c = self.c
        return f"  [{c['dim']}]{mark('·')}[/]  ".join(
            f"[{c['accent']}]{mark(str(k_))}[/] "
            f"[{c['mut']}]{mark(str(v).lower())}[/]" for k_, v in pairs)

    @property
    def rail_width(self):
        return self.RAIL_W if self.layout == "rail" else 0

    def rail_prefix(self):
        """The passive left rail: ONE stroke that groups a phase's card stack
        under its head. It is the third grouping mechanism (a rule), chosen
        over the fourth (a border) on purpose — the border stays reserved for
        focus, so it keeps meaning something. Grey from the `rail` token:
        KMBlue is interaction, and structure is never interaction."""
        if self.layout != "rail":
            return ""
        return (f"[{self.t.get('rail', self.c['dim'])}]{self.RAIL}[/]"
                + " " * (self.RAIL_W - 1))

    def doodle(self) -> str:
        from datetime import date
        return self.PHASES[date.today().day % len(self.PHASES)]

    def display_cap(self, s: str) -> str:
        return s.lower()                   # never letterspaced, never caps

    def head(self, name, count, w, idx=0):
        c = self.c
        # the head rides the rail too, so the stroke runs unbroken from the
        # phase name down through its cards — one group, one edge
        w = max(8, w - self.rail_width)
        line = (self.rail_prefix()
                + f"[{c['ink']}]{name.lower()[:max(1, w - 4)]}[/] "
                f"[{c['mut'] if count else c['dim']}]{count}[/]")
        rule = self.rule_line(w)
        return line if rule is None else line + "\n" + rule

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        c = self.c
        room = max(1, w - len(chip) - 2)
        body = _fit(title.lower(), room)
        pad = " " * max(0, room - min(len(title), room))
        # urgency = FULL INK on the title + the semantic chip; no marker glyph
        return (f"[{c['ink'] if urgent else c['mut']}]{body}[/]{pad} "
                f"[{tone}]{chip}[/]")

    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        # the rail is subtracted from the content budget exactly like the
        # card's own padding: it must narrow the text, never widen the row
        rail = self.rail_prefix()
        w = max(8, w - self.rail_width)
        top = self.card_row(title, chip, tone, w, idx, urgent)
        m = meta or {}
        c = self.c
        d = m.get("days")
        due = "--" if d is None else f"d{d}"
        sub = _fit_parts([
            ("  ", "  "),
            (f"[{c['dim']}]{(m.get('phase') or '--').lower()}[/]",
             (m.get("phase") or "--").lower()),
            (f"[{c['dim']}] · {due}[/]", f" · {due}"),
        ], w)
        return [rail + top, rail + sub]

    def tile_row(self, val, label, tone, w):
        c = self.c
        return (f"[{tone}]{val}[/] [{c['mut']}]"
                f"{label.lower()[: max(0, w - len(val) - 2)]}[/]")

    def sect(self, title, note, w, h=0):
        # drawn type RENOUNCED — quiet lowercase is the whole register
        c = self.c
        return [f"[{c['ink']}]{title.lower()}[/]  [{c['dim']}]{note.lower()}[/]",
                ""]

    def bar(self, span, head=None, tone=None):
        c = self.c
        # passive data never wears the accent — remap it to a grey step
        if tone in (None, c["accent"]):
            tone = c["mut"]
        return "".join(
            f"[{c['ink']}]o[/]" if (head is not None and head[i])
            else f"[{tone}]▄[/]" for i in range(span))

    GANTT = ("─", "O", "│", "·", "o")

    def cal_cell(self, state):
        c = self.c
        return {"none": f"[{c['dim']}]··[/]",
                "over": f"[{c['alert']}]oo[/]",
                "multi": f"[{c['ink']}]oo[/]",
                "one": f"[{c['mut']}]oo[/]"}[state]

    def queue_marker(self, i):
        return f"[{self.c['dim']}]·[/]"

    # lowercase ascii, and the double-bang is the fork's own chip idiom
    ICONS = {"deadline": "d", "overdue": "!!", "wip": "w", "blocked": "x",
             "workday": "$", "boardfile": "f"}

    # THE RAIL AT FULL WEIGHT (inc45). This read `O`, which is
    # `LEVELS["error"]`'s cell -- `darkside_S1` and `darkside_S6` both open on
    # `O redirect to task` and the round's note is verbatim: "el cursor es la
    # celda de error". The ladder keeps the mark, because the class docstring
    # is where severity is committed ("passive data is grey STEPS whose levels
    # ride on SHAPE") and the ladder is that commitment: `· / o / O` is one
    # mark losing and gaining weight.
    #
    # SO THE CURSOR TAKES THE OTHER THING THIS LANGUAGE OWNS. §8: "hierarchy
    # by WEIGHT AND DIMMING, not size" and "DEPTH BY ±1 GREY STEP, NEVER
    # BORDERS". `RAIL` is `▏`, the thinnest stroke this alphabet draws; the
    # cursor is that same stroke at full weight, `▊`. One stroke, two weights
    # -- which is the declared channel, and no border is added because a
    # single mark on one side encloses nothing at any width.
    CUR = "▊"
    SPIN = (".", "o", "O", "o")            # one breathing dot

    def spinner(self, tick):
        c = self.c
        tones = (c["dim"], c["mut"], c["ink"], c["mut"])
        i = tick % len(self.SPIN)
        return f"[{tones[i]}]{self.SPIN[i]}[/]"

    MOTION_STEPS = 3                         # two steps repeat a frame here

    # the port's language keeps its position-first reading — but the passed
    # extent is now a grey STEP rather than the same track, because "no fill"
    # was this language renouncing a part, and a part is not a language's to
    # renounce. The step is achromatic; KMBlue still reaches only the knob.
    PART_GLYPHS = {
        "main": {DEFAULT: "─", DISABLED: "╌"},
        "indicator": {DEFAULT: "▬", DISABLED: "▁"},
        "knob": {DEFAULT: "O", FOCUSED: "◎", EDITED: "◆",
                 ACTIVE: "●", INVALID: "Ø",
                 DISABLED: "x"},
        # the PORT, which is this language's one shape, with the plug in it
        # or the socket empty. The port's walls change with the state and
        # survive it — containment is non-vacuous here.
        "checkbox.main": {DEFAULT: "( )", FOCUSED: "[ ]", ACTIVE: "{ }",
                          DISABLED: "╌ ╌"},
        "checkbox.knob": {DEFAULT: "(O)", FOCUSED: "[◎]", ACTIVE: "{●}",
                          DISABLED: "╌x╌"},
        # THE SECOND LANGUAGE THAT COULD NOT TAKE THE ROUND WELL, for the
        # opposite reason to industrial's: here the round bracket is already
        # the PORT, this language's one shape, and the checkbox is standing
        # in it. So the radio is the port seen edge-on — chevrons that close
        # on the chosen item. Same law, different collision.
        "radio.main": {DEFAULT: "‹ ›", FOCUSED: "« »", ACTIVE: "▶ ◀",
                       DISABLED: "┄ ┄"},
        "radio.knob": {DEFAULT: "‹◦›", FOCUSED: "«◉»", ACTIVE: "▶●◀",
                       DISABLED: "┄▫┄"},
        # FILL INVERSION, this language's declared idiom, run as a ramp: the
        # shoulders go bar -> block as the control comes alive, and the
        # PRESS is the full block. No border is drawn around anything (this
        # language's law) — the shoulders are a weight, not a box — and the
        # accent it spends here is spent on interaction, which is the only
        # thing it spends it on.
        "button.main": {DEFAULT: "▬  ▬", FOCUSED: "▮  ▮", ACTIVE: "█  █",
                        DISABLED: "╌  ╌"},
        # FILL INVERSION as a ramp, bar → block, and no border is drawn (its
        # law) — the ends are a WEIGHT. The paper is unlit; the caret is this
        # language's own EDITED knob, the one mark it spends accent on.
        "textfield.main": {DEFAULT: "▬ ▬", FOCUSED: "▮ ▮", EDITED: "▮·▮",
                           ACTIVE: "█ █", INVALID: "Ø Ø",
                           DISABLED: "╌╌╌"},
        "textfield.caret": {DEFAULT: "◆"},
        # FILL INVERSION, declared idiom, on a shaft: the unseen content is
        # the thinnest seat this language draws and the view is the full
        # block. Nothing is boxed (its law), so the shaft has no ends — the
        # inversion IS the boundary.
        "scrollbar.main": {DEFAULT: "▁", DISABLED: "┄"},
        "scrollbar.indicator": {DEFAULT: "█", DISABLED: "▬"},
        # THE PORT SEEN EDGE-ON, which is the shape this language already
        # gave its radio — and it is the same choice wearing the other
        # mechanism, so it is right that it wears the same mark. FILL
        # INVERSION carries the state (chevron -> block under the press) and
        # NOTHING IS BOXED, its law, which survives the sixth component. The
        # end is the unlit seat: the inversion IS the boundary here too.
        "stepper.main": {DEFAULT: "▁▁", DISABLED: "┄┄"},
        "stepper.step": {DEFAULT: "◂▸", FOCUSED: "◄►", EDITED: "◀▶",
                         ACTIVE: "██", INVALID: "ØØ",
                         DISABLED: "╌╌"},
    }

    def part_tone(self, part, state, name=None):
        """The GRIP is the interaction, so it wears KMBlue in every live
        state — this language spends its one accent on nothing else. But a
        DISABLED grip is not interaction, and `control_of` is what makes a
        COMBINED `checked+disabled` say so; the raw comparison that stood
        here let a dead control keep its accent.

        The grip and not the knob: a button is nothing BUT interaction, and
        this language's one rule would have missed it."""
        if part == actuator(name) and control_of(state) != DISABLED:
            return self.c["accent"]
        return super().part_tone(part, state, name)

    def tabs(self, options, active):
        c = self.c
        return "  ".join(
            f"[{c['accent']}](O)[/][{c['ink']}]{o.lower()}[/]" if o == active
            else f"[{c['dim']}]( )[/][{c['mut']}]{o.lower()}[/]"
            for o in options)

    def surface(self):
        # depth by GREY-STEP background, never a border
        t = self.t
        return (f".kb-col {{ background: {t['panel']}; }}\n"
                f".kb-card {{ background: {t['panel']}; }}\n"
                "#hero { background: #0a0a0a; }")

    def board_layout(self):
        return "sections"                  # the flat lowercase list

    def composition(self):
        # composition PER POSTURE, not one cage: the centred 46-col column
        # is the AMBIENT register (hero/meter/tiles/queue — Moonshot's chat
        # column); data surfaces (the board, the views) get the full width.
        # A global max-width made tasks "casi ilegible" (user verdict).
        # the head carries the rail too, so it must sit on the card's own
        # left padding — one cell out and the "edge" is a zigzag. This
        # language declared that inset itself; it is the BASE kit's rule now
        # (every language needs it), so the local copy is gone.
        return """
        Screen.sz-board #ap, Screen.sz-widget #ap {
            align-horizontal: center; }
        #top, #tiles, #tabs, #queue, #ap-panel {
            max-width: 46; width: 1fr; }
        """

    def mascot(self):
        return []                          # identity is the doodle, recessive

    def wordmark(self, text):
        wm = self.t.get("wordmark", self.c["mut"])
        return [f"[{wm}]{self.doodle()} {text.lower()}[/]"]

    VOICE = {"empty": "nothing here", "no_signals": "no signals — press c"}


class Prism(Kit):
    """Darkside's descendant, and the only language here that was carried by a
    whole app until it had opinions before it was ever written down.

    IT IS NOT DARKSIDE RECOLOURED, and the difference is a mechanism. Darkside
    spends its one accent on interactivity and keeps every other mark grey.
    Prism spends colour TWICE, on two systems, with a BORDER BETWEEN THEM that
    is written down and measured:

      * IDENTITY hues NAME -- which project a mark belongs to (twelve of them);
      * SEVERITY hues JUDGE -- `alert` is overdue, `warn` is due today;
      * the accent CALLS ATTENTION -- today's rule, focus, keys.

    No mark may wear two of those jobs. On main that border is a test, not a
    convention: `tests/test_palette_ration.py` computes euclidean rgb distance
    across the whole palette, so re-adding a colliding hue turns it red
    whatever it is called. It exists because `amber` was once a project colour
    AND the due-today colour AT THE SAME HEX -- one mark meaning two things in
    five views. Priority is a GLYPH here (`!2`) rather than a hue precisely
    because its orange collided with a project's at nine rgb units.

    The second commitment is the EMBER: quantity is a solid field being
    consumed, not a track being filled, with the frontier at half-cell
    precision (`meter="ember"`, and the hero carves its numeral out of the same
    field). Each cell is field or figure and never both, so the
    two-colours-per-cell law is satisfied BY COMPOSITION instead of policed
    afterwards.
    """

    DISCLOSE = "⣶"                        # the field continues
    DANGER_FORM = ("⣿", "⣿")               # nothing left to burn

    # THE COMPONENT SHEET, WRITTEN IN THE LANGUAGE'S OWN MECHANISM.
    #
    # Prism says quantity by consuming a field, so its controls say STATE the
    # same way: by how much of a cell is alight.  The whole table is one ramp
    # -- ⠄ ⣀ ⣤ ⣶ ⣿ -- and that ramp is not decorative, it is the four dot-rows
    # of a braille cell, which is the same sub-cell grid the ember meter and
    # the carved hero are drawn on.  A reader who has understood the meter can
    # already read every control here, which is what a language IS.
    #
    # Two consequences worth naming, because both are laws elsewhere in this
    # file: the ramp is a SHAPE ladder, so every state survives greyscale
    # without spending a hue; and the knob is a HALF-CELL mark (⢸ / ⡇), the
    # only vocabulary here whose grip can sit inside a cell -- the same
    # half-cell precision the meter's frontier needs, said about position.
    def recede(self, row):
        """THE PAGE STEPS BACK BY ONE GREY STEP OF BACKGROUND, which is this
        language's entire depth mechanism ("depth by one grey step, never
        borders") and the reason it is the only one of the five allowed to
        draw the modal box at all: it has a way of saying BEHIND that costs
        no stroke."""
        return (f"[{self.c['mut']} on {self.depth_ground()}]"
                f"{mark(visible(row))}[/]")

    def pane_split_instead(self, h, w=3):
        """THE STEP — no stroke at all, and the whole depth mechanism.

        This language is in `PANE_SPLIT_REFUSED` because "never borders" is
        its structure device and a pane rule is a border. What it draws
        instead is what `recede` draws: ±1 grey step of BACKGROUND, the same
        `depth_ground()` the modal's backdrop uses. Two panes separate the
        way two regions do, because for this language there is only one
        answer to "these are different regions".

        AND IT DOES NOT SURVIVE THE `.txt`, which is stated here rather than
        discovered in a frame. A background is not a cell, so a cell grid
        shows three spaces — the third mark in this contract with that limit,
        after blueprint's knockout and every language's match emphasis. It
        DOES survive greyscale, which is the law that actually applies: a
        grey step is a step with every hue removed."""
        return [f"[{self.c['mut']} on {self.depth_ground()}]{' ' * w}[/]"
                for _ in range(max(0, h))]

    # THE VALIDATION ROW, and this language is airy: the message stands and
    # the line ends. The mark is the ember at full strength, its own ERROR.
    ERROR_FILL = ""
    # THE EMBER'S LEADING CELL -- the frontier `field_row` draws, at one dot.
    # "Quantity is a solid field being CONSUMED": a required seat is a field
    # the value has not reached yet.
    REQUIRED = "⡀"

    LEVELS = {"info": "⣀⣀", "warn": "⣤⣤", "error": "⣿⣿"}

    MATCH_STYLE = "bold {accent}"          # the accent CALLS ATTENTION

    def keyhint(self, pairs, w=0):
        """The ember frontier between the key and its word: the same ramp the
        rows and the controls spend, at one cell."""
        c = self.c
        return "   ".join(f"[{c['ink']}]{mark(str(k))}[/]"
                          f"[{c['dim']}]⣶[/]"
                          f"[{c['mut']}]{mark(str(v))}[/]"
                          for k, v in pairs)

    PART_GLYPHS = {
        "main": {DEFAULT: "⣀", DISABLED: "⠄"},
        "indicator": {DEFAULT: "⣿", DISABLED: "⣤"},
        # THE KNOB IS NEVER THE FILL.  Its first version took `⣿` at focused --
        # the same glyph as `indicator` -- so the grip vanished into the run it
        # was supposed to sit on.  Every state below is a BROKEN field (a dot
        # column missing) precisely so the knob can never be mistaken for a
        # full cell of fire or for an empty cell of track.
        "knob": {DEFAULT: "⢸", FOCUSED: "⢿", EDITED: "⣷",
                 ACTIVE: "⣾", INVALID: "⣹",
                 DISABLED: "⠈"},
        # THE CHECKBOX IS A FIELD WITH A HOLE BURNED IN IT.  Unchecked is an
        # intact field; checked is the field CARVED -- the same figure-as-
        # absence the hero uses for its numeral, at one cell.
        # The WALLS carry the control state and the CENTRE carries the checked
        # bit -- and the walls are identical between `main` and `knob` in every
        # state, so the box survives the mark instead of being redrawn by it.
        "checkbox.main": {DEFAULT: "⣿⣀⣿", FOCUSED: "⣷⣀⣷", ACTIVE: "⣾⣀⣾",
                          DISABLED: "⠄⠄⠄"},
        "checkbox.knob": {DEFAULT: "⣿⠀⣿", FOCUSED: "⣷⠀⣷", ACTIVE: "⣾⠀⣾",
                          DISABLED: "⠄⠀⠄"},
        # THE RADIO IS THE INVERSE: one lit cell in a dim run.  Checkbox
        # carves, radio LIGHTS -- so the two families differ in direction, not
        # in brightness, and a greyscale eye reads which is which.
        "radio.main": {DEFAULT: "⣀⣀⣀", FOCUSED: "⣤⣤⣤", ACTIVE: "⣶⣶⣶",
                       DISABLED: "⠄⠄⠄"},
        "radio.knob": {DEFAULT: "⣀⣿⣀", FOCUSED: "⣤⣿⣤", ACTIVE: "⣶⣿⣶",
                       DISABLED: "⠄⠁⠄"},
        # THE BUTTON'S WALLS ARE FIELD AND ITS AIR IS RESIDUE; the press does
        # not invert, it BREATHES -- the whole control comes alight, which is
        # the one event in this language that adds fire instead of spending it.
        "button.main": {DEFAULT: "⣿⣀⣀⣿", FOCUSED: "⣿⣤⣤⣿", ACTIVE: "⣿⣿⣿⣿",
                        DISABLED: "⠄⠄⠄⠄"},
        # THE FIELD'S GROUND: walls of fire, paper of ash.  EDITED banks the
        # paper up a step, so the state a caret lives in is legible in the
        # instant between two keystrokes.
        "textfield.main": {DEFAULT: "⣿⠀⣿", FOCUSED: "⣿⣀⣿", EDITED: "⣿⣤⣿",
                           ACTIVE: "⣿⣶⣿", INVALID: "⣹⠀⣏",
                           DISABLED: "⠄⠄⠄"},
        # the caret is HALF a cell, which is the finest mark this base owns
        "textfield.caret": {DEFAULT: "⡆"},
        # A SHAFT IS NOT A SCALE.  The slider's track is every value the knob
        # could take, so it is the ramp's floor; the scroll bar's shaft is
        # everywhere the view could BE, so it is drawn as an unlit lattice and
        # the thumb is the only fire on it.
        "scrollbar.main": {DEFAULT: "⠒", DISABLED: "⠄"},
        "scrollbar.indicator": {DEFAULT: "⣿", DISABLED: "⣤"},
        # THE TWO DIRECTIONS AS TWO HALF-CELLS: the step back lights the left
        # dot-column, the step forward the right.  Position says direction --
        # and at an end the ground's half draws instead, so CLAMP and WRAP
        # differ in shape.
        "stepper.main": {DEFAULT: "⣀⣀", DISABLED: "⠄⠄"},
        # ACTIVE stops one dot short of a full column on purpose: `⡇` is a
        # CLOSED seat in this file (#46 census -- five claimed half-cell fills
        # and a sixth would be an unaccounted one), and the step reads the same
        # at ⡆ because what it says is DIRECTION, not extent.
        "stepper.step": {DEFAULT: "⡀⢀", FOCUSED: "⡄⢠", EDITED: "⡆⢰",
                         ACTIVE: "⣇⣸", INVALID: "⢀⡀",
                         DISABLED: "⠁⠈"},
    }

    RAMP = ("⣀", "⣤", "⣶", "⣿")

    # THE SPIN IS THE FIELD BREATHING, not a mark travelling round a ring.
    # Every other language spins something ACROSS positions; Prism has no
    # position to spare on a one-cell seat, so it spends the axis it does own
    # -- density -- and the cell pulses up and down its own ramp.  Colour
    # stripped, it still moves, because the ramp is a shape ladder.
    SPIN = ("⣀", "⣤", "⣶", "⣿", "⣶", "⣤")

    def plot(self, series, w, h=4, hi=None):
        """Load as a FIELD BEING EATEN, drawn on the dot grid the ember and the
        hero share -- so the chart is the same object as the meter, one size up,
        rather than a second vocabulary the reader has to learn."""
        from taskboard import wave as WV
        c = self.c
        if not series or w < 2:
            return []          # nothing to burn is no field, not a blank one
        top = max(1, hi if hi is not None else max(series))
        cols = min(w, len(series))
        bm = WV.Bitmap(cols * WV.DOT_COLS, max(1, h) * WV.DOT_ROWS)
        for i in range(cols):
            v = series[len(series) - cols + i]
            lit = max(1, round(bm.h * v / top)) if v else 0
            for dc in range(WV.DOT_COLS):
                bm.fill_to(i * WV.DOT_COLS + dc, lit)
        rows = ["".join(ch if ch != " " else "·" for ch in r)
                for r in bm.to_braille()]
        return [f"[{c['accent']}]{r}[/]" for r in rows]

    def gauge(self, val, lo, hi, w=10, tone=None, thr=None):
        """The read-only twin of the ember: a field consumed to the reading,
        with the threshold a CARVED gap rather than a second mark -- Prism says
        \"here\" by taking fire away, which is the same move the hero makes."""
        c = self.c
        span = max(1, hi - lo)
        bar_w = max(3, w)
        n = max(0, min(bar_w, round(bar_w * (val - lo) / span)))
        tick = None if thr is None else max(0, min(bar_w - 1,
                                                   round(bar_w * (thr - lo) / span)))
        t = tone or c["accent"]
        cells = []
        for i in range(bar_w):
            if i == tick:
                cells.append(f"[{c['ink']}]⠀[/]")     # the carved gap
            elif i < n:
                cells.append(f"[{t}]⣿[/]")
            else:
                cells.append(f"[{c['dim']}]⡀[/]")
        return "".join(cells) + f" [{c['mut']}]{val}[/]"

    # MOTION: THREE STEPS, AND THE NUMBER IS THE CONTROL'S, NOT THE BASE'S.
    #
    # Four was tried first, reasoning that a braille cell has four dot-rows so
    # a field can be consumed in four stages.  The harness refused it and was
    # right: the switch's knob has THREE SEATS, so a 4-step budget repeats a
    # frame -- `no flip frame repeats`, a tick spent showing nothing new.  Two
    # was then tried and repeats as well, because the engine's rounding lands
    # two of its three moments on the same seat.  Three fills the seats exactly
    # and is the largest budget this control can actually spend.
    #
    # The lesson, worth more than the number: a motion budget is a property of
    # the CONTROL'S EXTENT, not of the pixel base's depth.  Both are about
    # resolution and they are not the same quantity.  Sharing the value 3 with
    # four other languages costs nothing -- what the laws compare is the FRAME
    # LIST, and Prism's is drawn in its own ramp and its own half-cell grip.
    #
    # A custom `flip_frames` travelling by half-cells was written to keep the
    # four, and thrown away: it ended the switch on a moving frame instead of
    # at rest, and it re-implemented an engine whose byte-for-byte
    # reproduction is itself a law here.
    MOTION_STEPS = 3

    # NOT DARKSIDE'S STROKE.  `▏` is that language's rail and the suite holds
    # a NEGATIVE law over it -- no other language may carry it -- because a
    # shared structure device is a shared language wearing two names.  Prism's
    # is a HEAVIER stroke in the project's own hue: darkside's rail is passive
    # grey that groups, this one NAMES while it groups, which is the identity
    # system reaching into structure and the whole reason the ration exists.
    RAIL = "▎"
    RAIL_W = 3

    def board_layout(self) -> str:
        """Sections, like its parent: the rail groups a stack vertically by
        project, and six kanban columns leave ~7 characters of title -- the
        same measurement that sent darkside to a flat list."""
        return "sections"

    # the twelve that NAME, resolved from the `ident` token so mutating the
    # token really does change which hues the board hands out
    def ident_hues(self):
        """The identity ramp, read from the `ident` token.

        Values are hexes, and anything that is not one falls back to the muted
        tier rather than to another identity hue -- a silent substitution here
        would give two projects the same name, which is the collision the whole
        ration exists to prevent.
        """
        out = []
        for v in str(self.t.get("ident", "")).split():
            out.append(v if v.startswith("#") else self.c["mut"])
        return out

    def ident_of(self, idx: int) -> str:
        hues = self.ident_hues()
        return hues[idx % len(hues)] if hues else self.c["mut"]

    @property
    def rail_width(self):
        return self.RAIL_W if self.layout == "rail" else 0

    def rail_prefix(self, idx: int = 0):
        """The rail is the ONE place an identity hue touches structure -- it is
        the project's own stroke, which is what makes a stack of cards read as
        belonging to something without spending a border or a label on it."""
        if self.layout != "rail":
            return ""
        return (f"[{self.ident_of(idx)}]{self.RAIL}[/]"
                + " " * (self.RAIL_W - 1))

    def head(self, name, count, w, idx=0):
        c = self.c
        w = max(8, w - self.rail_width)
        line = (self.rail_prefix(idx)
                + f"[{c['ink']}]{name[:max(1, w - 4)]}[/] "
                f"[{c['mut'] if count else c['dim']}]{count}[/]")
        rule = self.rule_line(w)
        return line if rule is None else line + chr(10) + rule

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        """The chip JUDGES, so it keeps the severity tone it was handed; the
        title never takes one. Urgency is weight, not hue -- the hue budget is
        already spent, and spending it twice is the collision the ration bans.
        """
        c = self.c
        room = max(1, w - len(chip) - 2)
        body = _fit(title, room)
        pad = " " * max(0, room - min(len(title), room))
        return (f"[{c['ink'] if urgent else c['mut']}]{body}[/]{pad} "
                f"[{tone}]{chip}[/]")

    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        rail = self.rail_prefix(idx)
        w = max(8, w - self.rail_width)
        top = self.card_row(title, chip, tone, w, idx, urgent)
        m = meta or {}
        c = self.c
        d = m.get("days")
        due = "--" if d is None else f"{d}d"
        # priority is a GLYPH, never a hue -- see the class docstring
        pri = "!" * min(2, int(m.get("priority") or 0))
        parts = [
            ("  ", "  "),
            (f"[{self.ident_of(idx)}]{m.get('phase') or '--'}[/]",
             str(m.get("phase") or "--")),
            (f"[{c['dim']}] · {due}[/]", f" · {due}"),
        ]
        # the priority mark is OMITTED when there is none, never emitted empty:
        # `_fit_parts` takes (markup, plain) pairs and an empty pair still costs
        # the fitter a part to reason about
        if pri:
            parts.append((f"[{c['ink']}] {pri}[/]", f" {pri}"))
        sub = _fit_parts(parts, w)
        return [rail + top, rail + sub]

    def tile_row(self, val, label, tone, w):
        c = self.c
        return (f"[{tone}]{val}[/] [{c['mut']}]"
                f"{label[: max(0, w - len(val) - 2)]}[/]")

    def field_row(self, caption, value, w):
        """THE EMBER FRONTIER -- this language's second commitment applied to
        a row instead of to a quantity.

        "Quantity is a solid field being CONSUMED, not a track being filled."
        So the space between a name and its figure is neither ruled nor
        dotted: it is a field burning down toward the figure, drawn with the
        same ramp the controls spend.  The frontier ARRIVES at the value --
        the value is where the field ran out.

        NO LEADER AND NO STROKE, and the second half is doctrine: "depth by
        one grey step, never borders."  A leader is not a border, but it is a
        LINE, and this language separates by tone and by consumption."""
        c = self.c
        cap, val = str(caption), str(value)
        ramp = "⡀⡤⣶"
        room = w - len(cap) - len(val) - len(ramp) - 1
        if room < 1:                       # too tight for a frontier: air
            room = max(1, w - len(cap) - len(val))
            return (f"[{c['mut']}]{mark(cap)}[/]" + " " * room
                    + f"[{c['ink']}]{mark(val)}[/]")
        return (f"[{c['mut']}]{mark(cap)}[/]" + " " * room
                + f"[{c['dim']}]{ramp}[/] [{c['ink']}]{mark(val)}[/]")

    def sect(self, title, note, w, h=0):
        c = self.c
        return [f"[{c['ink']}]{title}[/]  [{c['dim']}]{note}[/]", ""]

    def bar(self, span, head=None, tone=None):
        """A span wears its project's identity hue. It is passive data, so it
        must never take the accent -- the accent is attention, and a bar that
        is merely present is not asking for any."""
        c = self.c
        if tone in (None, c["accent"]):
            tone = c["mut"]
        return "".join(
            f"[{c['ink']}]█[/]" if (head is not None and head[i])
            else f"[{tone}]▄[/]" for i in range(span))

    GANTT = ("─", "█", "│", "·", "▄")

    def cal_cell(self, state):
        c = self.c
        return {"none": f"[{c['dim']}]··[/]",
                "over": f"[{c['alert']}]▄▄[/]",
                "multi": f"[{c['ink']}]▄▄[/]",
                "one": f"[{c['mut']}]▄▄[/]"}[state]

    def queue_marker(self, i):
        return f"[{self.ident_of(i)}]▏[/]"

    ICONS = {"deadline": "d", "overdue": "!!", "wip": "w", "blocked": "x",
             "workday": "$", "boardfile": "f"}


class Ledger(Kit):
    """Double-entry bookkeeping — and the ONLY language printed on a LIGHT
    ground, which is what makes it unmistakable once colour is stripped away:
    seven languages glow, this one is read.

    Commitments:

    * structure is RULED MONEY COLUMNS, never boxes. Every rule position is
      computed in ONE place (`cols()`), which both the renderer and the
      acceptance check read — so "the rules and the content share the same
      cells" is true by construction and provable by assertion;
    * every gap between a name and its figure closes with DOT LEADERS. On a
      ledger page space is either earned or filled, because an open gap is
      where a figure could be forged;
    * quantity is TALLY marks in groups of five (`meter="tally"`) — the
      mechanism used when you COUNT rather than measure;
    * every 5th line of the page carries the band tint, the way ruled paper
      is printed: the aid that lets an eye cross 80 cells without losing its
      row;
    * selection is a MARGIN mechanism — the row's tint plus its weight, never
      a border (`sel="none"` spends no border at all, so the page keeps its
      one strongest divider unspent);
    * the RED PEN is literal debt: the alert hue appears on OVERDUE entries
      and nowhere else. A page with nothing owed is ink on paper.
    """

    DISCLOSE = "┊"                        # the column carries on below
    # THE CONTRA ENTRY (operator ruling 6). A ledger writes a reversing
    # figure IN PARENTHESES -- that is the notation, four centuries old,
    # for an amount that takes something away. So a destructive control
    # is not refused here any more and it is not tinted red either: it
    # wears the form its own genre already uses for undoing a posting.
    DANGER_FORM = ("(", ")")

    LEAD = "·"
    RULE_V, RULE_SUB, RULE_HEAD = "│", "─", "═"
    GUTTER = 3                             # folio: two figures and a cell of air

    # THE REFUSAL, WRITTEN OUT. "A figure is audited, not shown. At most one
    # small ruled exhibit with dot leaders to its caption, like a receipt
    # stapled to the page; a full-bleed image on a ledger is a forgery of the
    # genre." So the exhibit STATES the figure — its identity and its
    # metrics, ruled and led — and draws none of it. `pixels` is None on this
    # posture, so there is nothing for a raster transport to overrule.
    EXHIBIT_W = 34                         # a receipt, not a plate

    def exhibit(self, img, w: int, h: int, label: str = "") -> list[str]:
        c = self.c
        ew = min(max(20, self.EXHIBIT_W), w)
        inner = ew - 2
        head = f"{self.RULE_HEAD * inner}"
        entries = [("exhibit", (label or "figure").upper()[:inner - 12]),
                   ("width", f"{img.size[0]} px"),
                   ("height", f"{img.size[1]} px"),
                   ("shown", "no")]
        body = []
        for name, val in entries:
            room = inner - 1 - len(name) - len(val)
            body.append(f"{self.RULE_V} {name}{self.LEAD * max(1, room)}"
                        f"{val}{self.RULE_V}")
        rows = ([f"[{self.rule_color}]{self.RULE_V}{head}{self.RULE_V}[/]"]
                + [f"[{c['ink']}]{mark(r)}[/]" for r in body]
                + [f"[{self.rule_color}]{self.RULE_V}"
                   f"{self.RULE_SUB * inner}{self.RULE_V}[/]"])
        # The exhibit is a RECEIPT on a page, so it is `ew` cells wide and the
        # page pays for the rest. Padded here rather than by the mechanism:
        # only this method knows how many cells its markup actually draws.
        air = " " * (w - ew)
        return [r + air for r in rows[:h]]
    ACCT_W = 10                            # the account column (the phase)
    FIG_W = 6                              # the figure column, right-aligned
    BAND_EVERY = 5                         # every 5th line of the page tints
    ICON_W = 4                             # the printed icon plus its air
    CUR = "▶"                              # the marker in the margin
    SPIN = ("▪···", "▪▪··", "▪▪▪·", "▪▪▪▪")   # the tally being written

    # printed abbreviations, the register a ledger actually uses
    ICONS = {"deadline": "due", "overdue": "o/d", "wip": "w/p",
             "blocked": "hld", "workday": "day", "boardfile": "led"}

    VOICE = {"empty": "nil balance", "no_signals": "no accounts posted"}

    @property
    def tally(self) -> str:
        return self.t.get("tally", "▪")

    @property
    def ruled(self) -> bool:
        """The `layout` token: "ruled" posts the entries between vertical
        money-column rules; anything else (the base default "flow") lets them
        stand on the page as plain leadered text — the same dispatch shape as
        darkside's rail, so the token is the mechanism, not the class name."""
        return self.layout == "ruled"

    @property
    def rule_color(self) -> str:
        return self.t.get("rule", self.c["dim"])

    @property
    def tick_tone(self) -> str:
        return self.c["mut"]               # red is debt; a threshold is not

    def display_cap(self, s: str) -> str:
        # tight caps, never letterspaced: the money columns already do the
        # spacing, and a ledger sets its captions to fit them
        return s.upper()

    # -- THE RULING ---------------------------------------------------------
    def cols(self, w: int) -> tuple[list[int], list[int]]:
        """The page's ruling for a row of `w` cells: the cells the vertical
        rules land on, and the field widths between them. Narrow pages
        RENOUNCE columns rather than crush them — the account goes first, the
        figure second, and the description is never squeezed below 6 cells."""
        w = max(8, w)
        g, acct, fig = self.GUTTER, self.ACCT_W, self.FIG_W
        desc = w - g - acct - fig - 4
        if desc < 8:                       # renounce the account column
            acct = 0
            desc = w - g - fig - 3
        if desc < 6:                       # then the figure column
            fig = 0
            desc = w - g - 2
        fields = [g, max(1, desc)] + ([acct] if acct else []) \
            + ([fig] if fig else [])
        pos, x = [], 0
        for f in fields:
            x += f
            pos.append(x)
            x += 1                         # the rule occupies its own cell
        return pos, fields

    def _banded(self, line: int) -> bool:
        """Ruled paper is printed with a tint every 5th LINE — lines, not
        entries: a posting spends two of them (debit, contra)."""
        return line % self.BAND_EVERY == self.BAND_EVERY - 1

    @staticmethod
    def _cell(text: str, width: int, right: bool = False) -> str:
        """Plain text fitted to `width` cells. Width math runs BEFORE escaping
        (the module's standing rule)."""
        t = text if len(text) <= width else text[: max(0, width - 1)] + "…"
        pad = " " * (width - len(t))
        return (pad + mark(t)) if right else (mark(t) + pad)

    def _leadered(self, text: str, width: int) -> str:
        """`name ···········` — the gap between a name and the rule that
        closes its column is FILLED. This is the language's whole typographic
        argument, so it lives in one function."""
        t = text if len(text) <= width else text[: max(0, width - 1)] + "…"
        room = width - len(t)
        if room >= 2:
            return mark(t) + " " + self.LEAD * (room - 1)
        return mark(t) + " " * room

    def _post(self, w: int, folio: str, desc: str, acct: str, fig: str,
              desc_tone: str, fig_tone: str, acct_tone: str | None = None,
              band: bool = False) -> str:
        """POST one line into the ruling. Every field is placed by `cols()`,
        so a row can never disagree with the rules that divide it."""
        c = self.c
        w = max(8, w)
        _, fields = self.cols(w)
        rule = (f"[{self.rule_color}]{self.RULE_V}[/]" if self.ruled else " ")
        marks = [f"[{c['mut']}]{self._cell(folio, fields[0] - 1, True)} [/]",
                 f"[{desc_tone}] {self._leadered(desc, fields[1] - 1)}[/]"]
        rest = list(fields[2:])
        if len(rest) == 2:                 # the account column survived
            marks.append(f"[{acct_tone or c['mut']}] "
                         f"{self._cell(acct, rest[0] - 1)}[/]")
        if rest:                           # the figure column survived
            marks.append(f"[{fig_tone}] "
                         f"{self._cell(fig, rest[-1] - 1, True)}[/]")
        row = "".join(m + rule for m in marks)
        if band:
            row = f"[on {self.t.get('band', self.t['panel'])}]{row}[/]"
        return row

    def rule_line(self, w):
        """The SUB rule, at FULL width. A ledger's rules run the whole
        measure — a rule that stops short is a rule you can post past."""
        if self.frame != "ruled":
            return super().rule_line(w)
        return f"[{self.rule_color}]{self.RULE_SUB * max(1, w)}[/]"

    def head_rule(self, w: int) -> str | None:
        if self.frame != "ruled":
            return super().rule_line(w)
        return f"[{self.rule_color}]{self.RULE_HEAD * max(1, w)}[/]"

    # -- the account heading ------------------------------------------------
    def head(self, name, count, w, idx=0):
        """A heading is not a posting, so it carries no money columns: the
        account's folio and name, the leaders, its balance as a figure, and
        the `═` head rule under it."""
        c = self.c
        w = max(8, w)
        folio = f"{idx + 1:>2} " if self.numbered else ""
        fig = "nil" if not count else f"{count} entries"
        body = self._leadered(folio + name.upper(), max(1, w - len(fig) - 1))
        line = (f"[{c['ink']}]{body}[/] "
                f"[{c['mut'] if count else c['dim']}]{fig}[/]")
        rule = self.head_rule(w)
        return line if rule is None else line + "\n" + rule

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        return self._post(w, f"{idx + 1}" if self.numbered else "",
                          title, "", chip, self.c["ink"], tone,
                          band=self._banded(2 * idx))

    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        """DOUBLE ENTRY: nothing is posted once. The debit line charges the
        task to its phase account and states the figure; the CONTRA line
        under it carries the counter-account (the project) and the state
        code, indented the way a bookkeeper indents a credit."""
        c = self.c
        m = meta or {}
        overdue = (m.get("days") is not None and m["days"] < 0
                   and not m.get("done"))
        state = ("hld" if m.get("blocked") else "o/d" if overdue
                 else "due" if m.get("days") is not None else "w/p")
        debit = self._post(
            w, f"{idx + 1}" if self.numbered else "", title,
            (m.get("phase") or "").lower(), chip,
            c["ink"], tone, band=self._banded(2 * idx))
        contra = self._post(
            w, "", "  " + (m.get("proj") or "--"),
            (m.get("prio") or "").lower(), state,
            c["mut"], c["alert"] if overdue else c["mut"], c["dim"],
            band=self._banded(2 * idx + 1))
        return [debit, contra]

    def tile_row(self, val, label, tone, w):
        """The figure is posted in the MARGIN and the account name follows it,
        the way a running balance is written. Figure FIRST, against this
        language's own right-hand habit, because a tile is clipped from the
        right (app.py's measured lesson: a 14-char label cropped every value
        off the widest size class) — and a ledger that loses its figure has
        lost the point. The gap that closes is the one after the name.

        The row is built to `w - ICON_W - 1`, not to `w`: this language draws
        a 3-cell printed icon in front of every tile, and filling a row to its
        full width is exactly what makes a prefix WRAP it (measured in the
        aperture, where the tiles are one auto-height Static). Reserving the
        icon's cells is the same move as darkside's rail — a mechanism pays
        for itself out of the content budget, it never widens the row."""
        c = self.c
        room = max(1, w - len(val) - self.ICON_W - 2)
        return (f"[{tone}]{val}[/] "
                f"[{c['mut']}]{self._leadered(label.upper(), room)}[/]")

    def field_row(self, caption, value, w):
        """DOT LEADERS -- and here they are the language's OWN, not a shape
        four other languages borrowed.

        "Every gap between a name and its figure closes with DOT LEADERS."
        `_leadered` is the one function that argument lives in, and this is
        the plainest thing it has ever been asked for: the account name, the
        leader that closes its column, and the figure at the measure's right
        edge where a figure is posted."""
        c = self.c
        cap, val = str(caption).upper(), str(value)
        return (f"[{c['ink']}]{self._leadered(cap, max(1, w - len(val) - 1))}"
                f"[/] [{c['ink']}]{mark(val)}[/]")

    def sect(self, title, note, w, h=0):
        # drawn display type RENOUNCED: a ledger prints, it does not draw
        c = self.c
        w = max(8, w)
        body = self._leadered(title.upper(), max(1, w - len(note) - 1))
        return [f"[{c['ink']}]{body}[/] [{c['mut']}]{mark(note)}[/]",
                self.rule_line(w) or ""]

    def bar(self, span, head=None, tone=None):
        """The bar is a TALLY: marks in groups of five, the group break drawn
        by the air between them. Passive quantity is ink, never the pen."""
        c = self.c
        tone = tone or c["mut"]
        out = []
        for i in range(span):
            if i % 6 == 5:
                out.append(" ")
            elif head is not None and head[i]:
                out.append(f"[{c['ink']}]{self.tally}[/]")
            else:
                out.append(f"[{tone}]{self.tally}[/]")
        return "".join(out)

    GANTT = ("·", "▪", "│", " ", "▪")      # leaders ruled, postings marked

    def cal_cell(self, state):
        c = self.c
        mk = self.tally
        return {"none": f"[{c['dim']}]··[/]",
                "over": f"[{c['alert']}]{mk}{mk}[/]",   # the red pen: debt
                "multi": f"[{c['ink']}]{mk}{mk}[/]",
                "one": f"[{c['mut']}]{mk}·[/]"}[state]

    def queue_marker(self, i):
        # the folio number, TWO cells and no period. HISTORY: this width was
        # once also a dodge — the queue row was built as marker + 1 + (w - 8)
        # + 5, which closes on w only for a 2-cell marker, so any wider one
        # overflowed. The forty-fifth pass CURED THAT AT THE SOURCE:
        # `aperture._queue_markup` now MEASURES the markers (`hero.vis_w`) and
        # the widest in the batch sets the column. Two cells is therefore a
        # free typographic choice now, not a constraint — widen it if the
        # ledger wants three, the row will follow.
        c = self.c
        return (f"[{c['mut']}]{i + 1:>2}[/]" if self.numbered
                else f"[{c['dim']}]{self.LEAD}[/]")

    def icon(self, kind):
        """The ONLY icon that wears the red pen is `overdue` — the rest are
        printed abbreviations in grey ink."""
        g = self.ICONS.get(kind, "")
        if not g:
            return ""
        tone = self.c["alert"] if kind == "overdue" else self.c["mut"]
        return f"[{tone}]{g}[/]"

    # a ledger RECONCILES: an account is posted or it is open, and it says
    # so in words. Two channels — the knob's position and the printed word —
    # and colour carries neither.
    CHECK_WORDS = ("open  ", "posted")

    MOTION_STEPS = 1

    # the unmeasured remainder is LEADERS, the measured extent is RULED, and
    # the mark posted at the value is the tally. The old slider drew leader
    # dots on both sides of the mark in two greys — an indicator separated
    # from the track by hue alone, which is the defect this language's own
    # meter was fixed for two passes ago.
    def overlay_instead(self, rows, w, h, under):
        """A LEDGER HAS NO SURFACE IN FRONT OF THE PAGE, so the question is
        POSTED on it.

        "Nothing is deleted, everything is balanced." A question about
        entries is written where entries are written: at the foot of the
        sheet, under a rule, with the page it concerns still legible above
        it. Nothing is covered and nothing is dimmed -- dimming the page
        would be this language claiming the entries above are less true while
        a question is open, and they are not.

        THE BACKDROP IS KEPT AT FULL STRENGTH, which is the exact opposite of
        every other answer here, and it is the refusal: there is no in front
        of."""
        keep = max(0, h - len(rows) - 1)
        out = [under[i] if i < len(under) else "" for i in range(keep)]
        out.append(self.rule_line(w) or "")
        out += list(rows)
        return out[:h] + [""] * max(0, h - len(out))

    def pane_split_rule(self, h, w=3):
        """A RULED COLUMN, AND THE RULE DESCENDS FROM THE HEAD RULE.

        "Structure is RULED MONEY COLUMNS, never boxes" — so this language
        does own the vertical stroke the other four spend differently, and
        `cols()` already says "the rule occupies its own cell". What makes
        the row `═══` at the top rather than `│` all the way down is
        `cols_frame`'s own order: a ruled page opens a column at the head
        rule and rules DOWN from it. A column rule that started in mid-air
        would be a stroke this page never posted.

        That first row is also the only thing separating this seat from the
        terminal's own `│`, and the difference is the point: nord rules
        because a terminal rules, and this language rules because the column
        was OPENED."""
        rows = [self._split_cell("│", self.rule_color, w)
                for _ in range(max(0, h))]
        if rows:
            rows[0] = f"[{self.rule_color}]{mark(self.RULE_HEAD * w)}[/]"
        return rows

    # THE VALIDATION ROW, on the page. A ledger FOOTNOTES an exception and
    # rules the leader out to the margin, which is the one typographic
    # argument this language is built on -- so the remainder is `LEAD`.
    #
    # AND IT SPENDS NO ALERT. "The alert hue is literal debt and nothing
    # else" is the commitment `log_row` already protects; a rejected form
    # field is not money owed.
    ERROR_FILL = LEAD
    ERROR_TONE = "ink"
    # THE SINGLE DAGGER. Footnote order is the whole notation: `†` marks the
    # entry that must be made, `‡` (this language's ERROR, and the wall its
    # invalid field is daggered with) marks the one that was refused.
    REQUIRED = "†"

    # THE COMPOSITOR'S FIRST MARK, DOUBLED (inc45). This read `† ` / `‡ `,
    # which is the two marks the line above has just spent on OBLIGATION and
    # on REFUSAL -- so `†` meant "this entry must be made" on a caption and
    # "there is a warning about this" on a log row, and `‡` meant "refused"
    # on a field and "error" on a row. Two claims per mark, no channel between
    # them, and ledger had no frame among the sixteen to say so either.
    #
    # REFERENCE MARKS ARE ASSIGNED, NOT RANKED. The printer's order is
    # `* † ‡ § ‖ ¶`; `†` and `‡` are spoken for above, so the ladder takes the
    # FIRST mark of that order and DOUBLES it for the graver note, which is
    # exactly what a compositor does when one mark is not enough. And doubling
    # is not a new channel here: "quantity is TALLY marks in groups of five --
    # the mechanism used when you COUNT rather than measure" is this
    # language's own commitment, so a ladder that counts is the ladder it
    # already believes in. One width, three shapes (ruling 8) as before.
    LEVELS = {"info": "  ", "warn": "* ", "error": "**"}

    # A LEDGER RULES UNDER A REFERENCED FIGURE. Underline is not a hue, and
    # it is the mark this genre already uses to point at an amount without
    # restyling it -- which is exactly what ruling 9 asks for.
    MATCH_STYLE = "underline {ink}"

    def keyhint(self, pairs, w=0):
        """Leaders, like every other gap on the page: the key, the leader
        that closes its column, the entry it posts."""
        c = self.c
        return "   ".join(f"[{c['ink']}]{mark(str(k))}[/]"
                          f"[{c['dim']}]{self.LEAD * 2}[/]"
                          f"[{c['mut']}]{mark(str(v).upper())}[/]"
                          for k, v in pairs)

    PART_GLYPHS = {
        "main": {DEFAULT: "·", DISABLED: "╌"},
        "indicator": {DEFAULT: "─", DISABLED: "┄"},
        "knob": {DEFAULT: "▪", FOCUSED: "▶", EDITED: "◆",
                 ACTIVE: "●", INVALID: "‡",
                 DISABLED: "▫"},
        # a RULED CELL in a column, struck when the line is posted. The
        # focused row grows this language's tally pointer on the left rule —
        # the rules still bracket the mark, so the cross cannot escape them.
        # The printed word (`open` / `posted`) rides beside it through
        # CHECK_WORDS, exactly as it does on the switch: one seat, two
        # components, no second declaration.
        "checkbox.main": {DEFAULT: "│ │", FOCUSED: "▶ │", ACTIVE: "▶·│",
                          DISABLED: "╌ ╌"},
        "checkbox.knob": {DEFAULT: "│×│", FOCUSED: "▶×│", ACTIVE: "▶●│",
                          DISABLED: "╌▫╌"},
        # THE BALLOT COLUMN. A ledger's checkbox is a cell STRUCK; its radio
        # is a cell POSTED — one entry against a ruled column of accounts,
        # exactly one of which can carry the figure. The right rule goes
        # dotted so the two controls are distinguishable at a glance in a
        # column of rows, and the tally pointer still grows on focus.
        #
        # AND THIS IS WHERE `CHECK_WORDS` STOPS. The switch and the checkbox
        # print `open`/`posted` beside them; a radio item prints the OPTION's
        # name instead, so ledger's own word never appears on a radio. That
        # is not a language losing a feature — it is the group scope: the
        # word beside an item names the item, and only the group knows it.
        "radio.main": {DEFAULT: "┊ ┊", FOCUSED: "▶ ┊", ACTIVE: "▶·┊",
                       DISABLED: "╌ ┊"},
        "radio.knob": {DEFAULT: "┊●┊", FOCUSED: "▶●┊", ACTIVE: "▶◉┊",
                       DISABLED: "╌▫┊"},
        # AN ENTRY IN THE LEDGER: the word sits in a ruled cell. The tally
        # pointer arrives when the cursor does (the same ▶ its checkbox and
        # radio grow), and the press CLOSES the entry on both sides — a line
        # posted, which is this language's whole metaphor for an action taken.
        "button.main": {DEFAULT: "│  │", FOCUSED: "▶  │", ACTIVE: "▶  ◀",
                        DISABLED: "╌  ╌"},
        # A RULED COLUMN, and the paper is the DOT LEADER this language rules
        # every gap with. The tally pointer arrives with the cursor and the
        # entry CLOSES on both sides when it is posted.
        #
        # The caret is NOT the gap in the leader, which was the first idea and
        # is wrong for a stated reason: a gap is a SPACE, and a space is the
        # one character the user's own value certainly contains. A mark that
        # can be confused with content is not a mark.
        "textfield.main": {DEFAULT: "│·│", FOCUSED: "▶·│", EDITED: "▶∙│",
                           ACTIVE: "▶·◀", INVALID: "‡·‡",
                           DISABLED: "╌╌╌"},
        "textfield.caret": {DEFAULT: "▏"},
        # THE RULED COLUMN, which is how this language shows a long document
        # already: the pages you are not on are column rules, the pages you
        # are on are the RULED EXTENT it posts every measured thing with. A
        # ledger scrolls through a book of entries and says which leaf.
        "scrollbar.main": {DEFAULT: "┊", DISABLED: "╌"},
        "scrollbar.indicator": {DEFAULT: "▬", DISABLED: "▫"},
        # CARRIED FORWARD AND BROUGHT BACK — a ledger's two directions have
        # names, and they are the rules that close an entry on the side it
        # came from. The tally pointer arrives with the cursor, exactly as it
        # does on this language's checkbox, radio and button; the press posts
        # the figure. An end is a RULED column with nothing to carry into: a
        # dotted rule, which in this vocabulary is a line that is not an
        # entry.
        "stepper.main": {DEFAULT: "┊┊", DISABLED: "▫▫"},
        "stepper.step": {DEFAULT: "▪▪", FOCUSED: "◀▶", EDITED: "◆◆",
                         ACTIVE: "●●", INVALID: "‡‡",
                         DISABLED: "╌╌"},
    }

    def value_label(self, val, state=DEFAULT):
        # a ledger always states the figure
        return f" [{self.c['mut']}]{val}[/]"

    def tabs(self, options, active):
        c = self.c
        return f"[{self.rule_color}] {self.RULE_V} [/]".join(
            f"[{c['ink']}]{self.tally} {o.upper()}[/]" if o == active
            else f"[{c['dim']}]{self.LEAD} {o}[/]" for o in options)

    def mascot(self):
        return []                          # a ledger keeps no pet

    def wordmark(self, text):
        # the LETTERHEAD: the name ruled above and below, the way a bound
        # book prints the account it belongs to
        c = self.c
        cap = " ".join(text.upper())
        n = max(1, len(cap))
        return [f"[{self.rule_color}]{self.RULE_HEAD * n}[/]",
                f"[{c['ink']}]{cap}[/]",
                f"[{self.rule_color}]{self.RULE_SUB * n}[/]"]

    def board_layout(self):
        return "sections"                  # a ledger is a page, not columns

    def surface(self):
        """PAPER — the one light ground in the set. Every surface the board
        touches has to carry it or the dark ambient bleeds through as a
        patch, INCLUDING the scrollbar, which no colour token reaches."""
        t = self.t
        return (f".kb-col, .kb-card, .kb-flat, #ap, #top, #kb, #view,\n"
                f"#meter, #tiles, #tabs, #queue, #cfg-title, #cfg-scroll\n"
                f"    {{ background: {t['ground']}; }}\n"
                f".kb-flat, .kb-col, #cfg-scroll {{\n"
                f"    scrollbar-background: {t['focus']};\n"
                f"    scrollbar-background-hover: {t['focus']};\n"
                f"    scrollbar-background-active: {t['focus']};\n"
                f"    scrollbar-color: {t['rule']};\n"
                f"    scrollbar-color-hover: {t['mut']};\n"
                f"    scrollbar-color-active: {t['ink']}; }}")

    def composition(self):
        """THE PAGE: the head rule tight against the entries it rules, and the
        head sitting on the same left edge as the card content — one cell out
        and the ruling zigzags (darkside's measured lesson).

        It spends NO rule on the page's outer margin, and that is a decision,
        not an omission: changing `#ap`'s padding changes every region's
        WIDTH, and a region that is re-measured a frame after its rows were
        built wraps them. Every row of this language is filled to its full
        measure by leaders, so it is the one language with no slack to absorb
        a stale width — measured in the aperture, where a 3-cell margin
        folded the whole queue.

        The focus rules are structural, not cosmetic: widget.tcss shifts a
        focused row's padding to make room for a focus BORDER, and this
        language spends no border — left alone, the ruling would jump one
        cell sideways on the focused row. Focus is carried by the row's tint
        and its weight instead.

        """
        return """
        .col-head { margin-bottom: 0; }
        .kb-card:focus { padding: 0 1; }
        .tile:focus { padding: 0 1; }
        Screen.sz-board #hero { height: 7; min-height: 7; }
        """


class Solari(Kit):
    """THE SPLIT-FLAP DEPARTURE BOARD. The product becomes ONE SCHEDULE: a
    task is a ROW, a phase is a GATE, and the task's state is a WORD in a
    status column.

    Commitments, each of which is a mechanism below and not a note:

    * **quantity is DIGITS in flap cells, never a bar** (`meter="odometer"`).
      No other language in the set states a figure where the others draw a
      length, and it is the reason a departure board is legible at fifty
      metres: you read `07`, you do not estimate a bar. DATAVIZ.md law 1 is
      satisfied by construction — a 3 and a 7 differ in SHAPE with every
      colour stripped away;
    * **the SEAM is the whole divider vocabulary.** `frame="flaps"` says the
      structure device is the cell FACE a character is flipped onto, so this
      language spends no rule at all: `rule_line()` returns None and every
      schedule row closes with one `▁` in the `seam` tone;
    * **headers are BANDS in reverse video** (`band="reverse"`), EXACTLY as
      wide as the seams under them. Band and seam are both cut from one
      geometry seat (`fields()`), so "the band matches the seam grid" is true
      by construction rather than by inspection;
    * **TABULAR fields, padded to their widest content.** Every column is a
      fixed width and every figure is zero-padded, so nothing on the page
      moves sideways when a value changes (Bodmer T1/T2 — the anti-jiggle
      law, and the reason a flap board can be read while it is flipping);
    * **amber is RATIONED to selection and to values in flight** (a task
      inside its boarding window). A calm page carries none. Red is narrower
      still: it appears on LATE and nowhere else.

    The ITEM field is deliberately the ONE field with no colour tag on it: it
    inherits the widget's colour, which is what lets the selection band invert
    it (`.kb-card:focus` sets ground-on-amber) instead of printing cream on
    amber at 1.8:1.
    """

    SEAM = "▁"

    # ======================================================================
    # THE SEVEN IT USED TO INHERIT (batch `kits-learn-4`, AC-5). LANGUAGES.md
    # §10: "amber on near-black, rationed · dense · THE SEAM IS THE WHOLE
    # DIVIDER VOCABULARY · flap-cell digits · public-signage. The product
    # becomes ONE SCHEDULE: a task is a row, a phase is a gate, A STATE IS A
    # WORD IN A STATUS COLUMN ... headers are BANDS IN REVERSE VIDEO ...
    # tabular fields PADDED TO THEIR WIDEST CONTENT."
    # ======================================================================
    DISCLOSE = "═"                        # the seam doubled: a flap mid-turn
    # THE FLAP STANDING (inc47). This read `▁`, the SEAM, under the argument
    # that "this language HAS one divider and spends it everywhere" -- and the
    # argument is right about the SEAM and wrong about the obligation.
    # `solari_S2` is the measurement: `▁` appears 139 times on that screen and
    # TWO of them are the answer to "point at the required fields". A mark
    # that has to be found by counting from the end of a caption is a
    # POSITION, not a mark, and §9.4's q6 asks that question by name.
    #
    # THE SEAM STAYS THE DIVIDER. It is spent 137 more times on that same
    # screen -- the row seam, the head rule, and the DEFAULT rung of every
    # control's chrome ladder (`▁` default, `▔` focused, `▂` active, `╌` dead)
    # -- and that is ALPHABET, which this batch does not touch. What moves is
    # the one seat where the seam had to carry a MEANING.
    #
    # AND THE MARK IS THE FACE, NOT THE EDGE. §10: "the structure device is
    # the cell FACE a character is flipped onto." `▮` is that face caught
    # UPRIGHT -- the cell standing with nothing flipped onto it yet -- and it
    # is this language's own caret, which is the same claim from the other
    # side: the caret says the next character lands HERE, the obligation says
    # a character MUST land here. One meaning at two seats, which is the
    # inverse of the defect this batch exists to remove.
    #
    # NOT `▔` AND NOT `▂`: those are the FOCUSED and ACTIVE rungs of the
    # chrome ladder, so an obligation would have opened a focused control
    # (inc48's law). Not `═`: that is `DISCLOSE` and the INVALID mark, a
    # meaning already. Not a digit -- the digits are the quantity (DATAVIZ
    # law 1) and an obligation states no quantity.
    REQUIRED = "▮"
    DANGER_FORM = ("▀", "▄")               # the two halves of a turning cell
    # THE ONE LADDER IN THE ELEVEN THAT IS NOT A GLYPH, AND IT IS THIS
    # LANGUAGE'S HEADLINE COMMITMENT: "a state is a WORD in a status column".
    # A departure board does not draw severity, it PRINTS it -- the same
    # argument DATAVIZ law 1 credits it with for quantity ("you read 07, you
    # do not estimate a bar"). Three words of one width, so the column still
    # aligns and the level still sorts with every colour stripped away.
    #
    # `CNX` FOR A REJECTED FIELD IS THE LANGUAGE HAVING AN OPINION, not a
    # borrowed word: on this board an entry that will not run is cancelled,
    # and a form field that will not parse is the same event.
    LEVELS = {"info": "OK ", "warn": "DLY", "error": "CNX"}
    MATCH_STYLE = "reverse {ink}"          # a band, which is this board's mark

    def field_row(self, caption, value, w):
        """THE SEAM CLOSES THE GAP, because the seam is the only divider this
        language owns.

        Every other language here had to choose one; this one had already
        chosen, and `rule_line()` returning None is the same decision seen
        from the other side. The caption is lettered in the board's caps and
        the figure stands at the right of its own field, padded so nothing
        moves sideways when the value changes -- the anti-jiggle law that
        lets a flap board be read WHILE it is flipping."""
        c = self.c
        cap, val = str(caption).upper(), str(value)
        gap = max(1, w - len(cap) - len(val) - 2)
        return (f"[{c['mut']}]{mark(cap)}[/] "
                + f"[{self.seam_tone}]{mark(self.SEAM * gap)}[/] "
                + f"[{c['ink']}]{mark(val)}[/]")

    def keyhint(self, pairs, w=0):
        """The key, the seam, the word -- in caps, because everything on a
        departure board is."""
        c = self.c
        return "   ".join(f"[{c['accent']}]{mark(str(k_))}[/]"
                          f"[{self.seam_tone}]{mark(self.SEAM)}[/]"
                          f"[{c['mut']}]{mark(str(v).upper())}[/]"
                          for k_, v in pairs)

    def schedule_head(self, under: list[str]) -> int:
        """WHERE THE SCHEDULE STARTS: the row after the board's head seam.

        A departure board's announcement takes the head of the SCHEDULE, not
        the head of the screen. The station's own plate — its name, its
        counts, and the seam that closes them — is not a departure, and an
        announcement has never covered it on any board that ever hung in a
        concourse. `MODAL_BORDER_REFUSED` says the same thing from the other
        side: "with the rows still legible under it" is a claim about the
        page surviving, and a page whose masthead is gone has not survived.

        THE PLATE IS FOUND, NOT COUNTED. This language's whole divider
        vocabulary is the seam, so the plate is exactly what stands above the
        first FULL-MEASURE seam — a row that is nothing but `SEAM`, edge to
        edge. Read off the page rather than typed as a row number: a head
        that grows a line does not need this method edited, and a language
        that stopped ruling its masthead would fall back on its own.

        A PAGE WITH NO FULL-MEASURE SEAM HAS NO PLATE TO PROTECT, and the
        band takes the top — which is the pre-inc40 behaviour, kept as the
        honest answer to "nobody said" rather than as a fallback nobody
        chose. `tests/test_components.py`'s synthetic `UNDER` is such a page,
        and it is asserted to stay put."""
        for i, r in enumerate(under):
            body = visible(r).rstrip()
            if body and set(body) == {self.SEAM}:
                return i + 1
        return 0

    def overlay_instead(self, rows, w, h, under):
        """A BOARD HAS NO SURFACE IN FRONT OF IT. "One shape, the row" is the
        commitment that already took this language's pixels ("an image cannot
        flip"), and it takes the dialog for the same reason: a question is
        posted the way a cancellation is, as a BAND IN REVERSE VIDEO across
        the full measure at the head of the board, with the schedule still
        legible under it.

        `band="reverse"` is a token this language already declares, and the
        band is exactly as wide as the seams under it — which is why the
        question sits at the TOP rather than centred: a departure board's
        announcement row is its first row.

        THE HEAD OF THE SCHEDULE, NOT ROW ZERO (inc40). This method used to
        write the block at index 0 and take `under[i]` only below it, so on a
        real page the announcement landed on the mode strip, the masthead and
        the head seam and they were gone — `solari_S4` opened on a blank row
        where every other language keeps the mode strip, and the round could
        not answer "which mode is this?" from the frame. The band still takes
        the head; `schedule_head` is what says which head. The block is
        placed the way the base places its own, `y <= i < y + len(block)`,
        which is also what keeps this an OVERLAY: every row outside the band
        is still `under[i]` at the same index, so nothing shifts."""
        c = self.c
        bar = (f"[{self.t.get('ground', '#000000')} on {c['accent']}]"
               f"{mark(' ' * w)}[/]")
        block = [bar] + list(rows) + [self.seam(w)]
        y = self.schedule_head(under)
        out = []
        for i in range(h):
            if y <= i < y + len(block):
                out.append(block[i - y])
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out
    GAP = 2                                # cells of air between fields
    DUE_W, STAT_W, PROJ_W, PRI_W = 2, 8, 12, 4
    # the priority vocabulary (models.TASK_PRIORITIES), abbreviated to the
    # field rather than ellipsed into it: `NORMAL` truncated at 4 reads
    # `NOR…`, which is a word the board never has to print
    PRIO = {"low": "LOW", "normal": "NORM", "high": "HIGH"}
    ITEM_MIN = 24                          # a title below this is not useful
    # THE DECLARED REFLOW DROP ORDER (the law this language exists to show):
    # a narrower page SHEDS whole columns in this order and never truncates
    # ITEM below its floor, never wraps, never squeezes a fixed field.
    #
    # STATUS is last and it is in the list on purpose. The first draft stopped
    # at `("proj", "pri")` and let the row fall back to the BASE kit below the
    # floor — measured, that made solari render nord's card anatomy at 28
    # cells, which the pairwise check caught. A language may renounce a
    # COLUMN; it may not renounce being itself. DUE (the digits) and the seam
    # survive every tier.
    DROP = ("proj", "pri", "stat")
    CAPS = {"stat": "STATUS", "proj": "PROJ", "pri": "PRI"}

    CUR = "▼"                              # the flap indicator
    SPIN = ("▔", "▀", "▄", "▁")            # one cell falling, a flap turning

    # the board's own vocabulary: departures, not tasks
    ICONS = {"deadline": "DEP", "overdue": "LATE", "wip": "BRD",
             "blocked": "HELD", "workday": "DAY", "boardfile": "SKD"}

    VOICE = {"empty": "NO DEPARTURES", "no_signals": "NO SIGNALS SCHEDULED"}

    # the status column, keyed by the state kanban.py already computed. The
    # widest word is 8 cells and the field is 8 cells: the column is sized to
    # its widest content, not to the value on screen (anti-jiggle).
    STATUS = {"done": "DEPARTED", "blocked": "HELD", "late": "LATE",
              "flight": "BOARDING", "ontime": "ON TIME", "open": "OPEN"}
    BOARDING = 3                           # days: inside this, in flight

    # ---- tokens -----------------------------------------------------------
    @property
    def flap(self) -> str:
        """The cell face. Passive structure, one step off the ground."""
        return self.t.get("flap", self.t["panel"])

    @property
    def seam_tone(self) -> str:
        return self.t.get("seam", self.c["dim"])

    @property
    def flapped(self) -> bool:
        """The `frame` token. "flaps" is not a rule glyph — it is the cell
        face, so this language's frame turns FACES on and rules off."""
        return self.frame == "flaps"

    @property
    def scheduled(self) -> bool:
        """The `layout` token. Anything but "schedule" (the base default
        "flow" included) gives back the generic composition, byte for byte."""
        return self.layout == "schedule"

    @property
    def banded(self) -> bool:
        return self.t.get("band") == "reverse"

    def rule_line(self, w):
        """A flap board has no rules. The seam is the only divider it owns,
        and it is drawn by the row that closes, not by the head."""
        return None if self.flapped else super().rule_line(w)

    # ---- the flap cell ----------------------------------------------------
    def cell(self, text: str, tone: str | None = None,
             face: str | None = None) -> str:
        """One or more characters flipped onto the cell FACE. With the frame
        token off the face goes away and the figures stay — the digits are the
        datum, the face is the structure.

        `face` is how this language spends SEVERITY (see `_tones`)."""
        tone = tone or self.c["ink"]
        bg = face or self.flap
        return f"[{tone}{' on ' + bg if self.flapped else ''}]{mark(text)}[/]"

    def band_row(self, text: str, w: int) -> str:
        """REVERSE VIDEO, exactly `w` cells. Ink is the ground and the ground
        is the ink — the one treatment a flap board uses to head a block, and
        the reason it never needs a rule."""
        w = max(1, w)
        body = text[:w] + " " * max(0, w - len(text))
        return f"[{self.t['ground']} on {self.c['ink']}]{mark(body)}[/]"

    def seam(self, w: int) -> str:
        return f"[{self.seam_tone}]{self.SEAM * max(1, w)}[/]"

    @staticmethod
    def _pad(text: str, n: int, right: bool = False) -> str:
        """Exactly `n` cells. Width math runs BEFORE escaping (module rule)."""
        if n <= 0:
            return ""
        t = text if len(text) <= n else text[: max(0, n - 1)] + "…"
        pad = " " * (n - len(t))
        return (pad + mark(t)) if right else (mark(t) + pad)

    # ---- ONE GEOMETRY SEAT ------------------------------------------------
    def fields(self, w: int) -> list[tuple[int, str, int]]:
        """The schedule's columns for a row of `w` cells: `(origin, code,
        width)`, filling the measure EXACTLY. Read by the row renderer, by the
        band and by every acceptance check — the `Ledger.cols` / `Swiss.grid`
        / `Nord.panes` / `Instrument.reticle` / `Corgi.slots` precedent.

        Narrow pages SHED whole columns in the declared `DROP` order and stop:
        below the floor the schedule is RENOUNCED (returns `[]`) and the row
        degrades to the generic two-line card, which can never be worse than
        the form it replaced (swiss's grid law). ITEM is never cut below
        `ITEM_MIN` and no fixed field is ever squeezed.

        GATE is not a column, deliberately: under a sections board every row
        of a block shares one phase, so a GATE column would print the same
        word down the whole block — the constant-column defect the corgi pass
        deleted. The BAND states the gate once, which is what a real flap
        board does.
        """
        spec = [("due", self.DUE_W), ("item", 0), ("stat", self.STAT_W),
                ("proj", self.PROJ_W), ("pri", self.PRI_W)]
        for dropped in range(len(self.DROP) + 1):
            gone = set(self.DROP[:dropped])
            cols = [(c, n) for c, n in spec if c not in gone]
            fixed = (sum(n for c, n in cols if c != "item")
                     + self.GAP * (len(cols) - 1))
            item = w - fixed
            if item < self.ITEM_MIN:
                continue
            out, x = [], 0
            for c, n in cols:
                n = item if c == "item" else n
                out.append((x, c, n))
                x += n + self.GAP
            return out
        return []

    # ---- the state, read from the chip kanban.py already computed ---------
    @staticmethod
    def _read(chip: str) -> tuple[int | None, str]:
        """`(days, state)` from the chip. One derivation path for the whole
        language: the chip IS the task state (kanban.py computes it from the
        due date, the blocked flag and the done column), so deriving the
        status word from it can never disagree with the row beside it."""
        c = (chip or "").strip()
        if c == "done":
            return None, "done"
        if c == "blk":
            return None, "blocked"
        late = c.endswith("!")
        body = c[:-1] if late else c
        if body.endswith("d") and body[:-1].lstrip("-").isdigit():
            n = int(body[:-1])
            if late:
                return n, "late"
            return n, ("flight" if n <= Solari.BOARDING else "ontime")
        return None, "open"

    def _tones(self, state: str) -> tuple[str, str, str]:
        """`(due FACE, due ink, status ink)`.

        **SEVERITY IS THE CELL FACE, NEVER THE INK.** On a flap board a
        boarding departure LIGHTS UP — it does not print its letters in a
        different colour — and that is not only faithful, it is what makes
        the selection band legible. Measured, and the reason this method
        was rewritten: with severity on the ink, the selected row painted a
        `#f5a300` word on a `#f5a300` ground (1:1, invisible), and the calm
        fields came out at 1.8:1. With severity on the face, every glyph on a
        schedule row is neutral (ink · mut · dim), so inverting the row's
        ground can never hide a word, and the two channels the state needs
        are the LIT FACE and the STATUS WORD — never colour alone.

        Amber therefore appears on exactly two things in this whole language:
        a departure in flight, and the row you have selected.
        """
        c = self.c
        calm, flap = self.t.get("calm", c["ink"]), self.flap
        gnd = self.t["ground"]
        return {"done": (flap, c["dim"], c["dim"]),
                "blocked": (flap, c["mut"], c["mut"]),
                "late": (c["alert"], gnd, c["mut"]),
                "flight": (c["accent"], gnd, c["mut"]),
                "ontime": (flap, calm, c["mut"]),
                "open": (flap, c["mut"], c["mut"])}[state]

    def _due(self, days: int | None) -> str:
        """The odometer figure, DUE_W cells, zero-padded and tabular. CLIPPED,
        never clamped: past the field's range it reads `9+`, a form the normal
        fill can never emit, so a far-off date is never printed as a near
        one. The SIGN is not spent here — the status word carries `LATE`, and
        a two-channel reading beats a minus sign nobody sees."""
        n = self.DUE_W
        if days is None:
            return "-" * n
        d = abs(int(days))
        top = 10 ** n - 1
        return f"{d:0{n}d}" if d <= top else "9" * (n - 1) + "+"

    # ---- the schedule row -------------------------------------------------
    def _sched_row(self, title, chip, tone, w, meta) -> str | None:
        fs = self.fields(w)
        if not fs:
            return None
        c, m = self.c, (meta or {})
        days, state = self._read(chip)
        face, dtone, stone = self._tones(state)
        out = []
        for i, (x, code, n) in enumerate(fs):
            if code == "due":
                out.append(self.cell(self._due(days), dtone, face))
            elif code == "item":
                # THE ONE UNTAGGED FIELD: it inherits the widget's colour, so
                # the selection band inverts it instead of printing cream on
                # amber (see the class docstring)
                out.append(self._pad(title.upper(), n))
            elif code == "stat":
                out.append(f"[{stone}]{self._pad(self.STATUS[state], n)}[/]")
            elif code == "proj":
                out.append(f"[{c['mut']}]"
                           f"{self._pad((m.get('proj') or '--').upper(), n)}[/]")
            else:                          # pri
                raw = (m.get("prio") or "").lower()
                p = self.PRIO.get(raw, (raw or "--").upper()[:n])
                out.append(f"[{c['mut']}]{self._pad(p, n)}[/]")
            if i < len(fs) - 1:
                out.append(" " * self.GAP)
        return "".join(out)

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        if not self.scheduled:
            return super().card_row(title, chip, tone, w, idx, urgent)
        row = self._sched_row(title, chip, tone, w, None)
        return row if row is not None else super().card_row(
            title, chip, tone, w, idx, urgent)

    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        """TWO rows and the second one is the SEAM. A departure board's whole
        grid is the gap between rows — one `▁` the width of the row, and
        nothing else on the page divides anything."""
        if not self.scheduled:
            return super().card_rows(title, chip, tone, w, idx, urgent, meta)
        row = self._sched_row(title, chip, tone, w, meta)
        if row is None:                    # renounced: the generic form back
            return super().card_rows(title, chip, tone, w, idx, urgent, meta)
        return [row, self.seam(w)]

    # ---- the gate band ----------------------------------------------------
    def head(self, name, count, w, idx=0):
        """The phase becomes a GATE and the gate is a BAND: reverse video,
        the gate's name, its load as an odometer figure, and the captions of
        the columns that survived, each standing on its own field origin — so
        the band advertises exactly the geometry the rows under it use."""
        if not (self.scheduled and self.banded):
            return super().head(name, count, w, idx)
        w = max(1, w)
        fs = self.fields(w)
        if not fs:
            return super().head(name, count, w, idx)
        line = [" "] * w
        # the gate's own text stops one cell short of the first CAPTIONED
        # field; when every captioned field has been shed it may run the
        # whole measure
        capped = [x for x, code, _ in fs if code in self.CAPS]
        gate = f" GATE {name.upper()} {min(count, 99):02d} "
        gate = gate[: max(1, (capped[0] - 1) if capped else w)]
        line[:len(gate)] = list(gate)
        for x, code, n in fs:
            cap = self.CAPS.get(code)
            if cap:
                line[x: x + len(cap)] = list(cap[:n])
        return self.band_row("".join(line), w)

    # ---- the view section header -----------------------------------------
    def sect(self, title, note, w, h=0):
        """Drawn display type RENOUNCED — a flap board sets everything in the
        one cell height it owns, so `h` buys nothing and that is a decision."""
        w = max(1, w)
        return [self.band_row(f" {title.upper()}  {note.upper()} ", w),
                self.seam(w)]

    # ---- quantity everywhere else ----------------------------------------
    def bar(self, span, head=None, tone=None):
        """NOT a bar. The bucket's quantity is its FIGURE, flipped onto flap
        cells and then padded out to the slot the caller reserved — the length
        is a seat, never the reading. `head` (the travelling packet) marks the
        figure as a value IN FLIGHT, which is the one other thing amber is
        spent on."""
        c = self.c
        span = max(1, span)
        n = min(span, 99)
        s = f"{n:02d}"[:span]
        lit = head is not None and any(head[:span])
        return (self.cell(s, c["accent"] if lit else (tone or c["ink"]))
                + " " * max(0, span - len(s)))

    GANTT = ("▁", "▀", "│", " ", "▼")      # the seam, a flipping cell, a flag

    def cal_cell(self, state):
        c = self.c
        # severity is the FACE here too, so the calendar and the schedule
        # spend their one loud colour the same way
        return {"none": f"[{c['dim']}]--[/]",
                "over": self.cell("!!", self.t["ground"], c["alert"]),
                "multi": self.cell("2+", c["ink"]),
                "one": self.cell("01", c["mut"])}[state]

    def queue_marker(self, i):
        # TWO cells, tabular, like every other figure on this board. It used
        # to also be the safe width — the queue row's `- 8` arithmetic only
        # closed on a 2-cell marker — but the forty-fifth pass made that row
        # measure its markers (`aperture._queue_markup` via `hero.vis_w`), so
        # the overflow is gone and this width is now pure typography.
        return self.cell(f"{min(i + 1, 99):02d}", self.c["mut"])

    def tile_row(self, val, label, tone, w):
        """The figure is flipped first and the account name follows it: on a
        departure board the number is the thing you look for."""
        c = self.c
        v = (val or "").strip() or "--"
        room = max(1, w - len(v) - 1)
        return (self.cell(v, tone) + " "
                + f"[{c['mut']}]{self._pad(label.upper(), room)}[/]")

    # ---- the components ---------------------------------------------------
    # the flap board STATES the mode; the word is the flap's face
    CHECK_WORDS = ("OFF", "ON ")

    # the flaps SETTLE left to right — three frames, no recompute
    MOTION_STEPS = 3

    # a flap board never draws a filled length, so the indicator is the row
    # of flaps ALREADY TURNED — a seam, not a bar — and the figure is stated
    # on a flap cell the way this board states every quantity. The old
    # slider drew the same dot on both sides of the knob: no indicator.
    PART_GLYPHS = {
        "main": {DEFAULT: "·", DISABLED: "╌"},
        "indicator": {DEFAULT: "▁", DISABLED: "▫"},
        "knob": {DEFAULT: "▼", FOCUSED: "▲", EDITED: "◆",
                 ACTIVE: "█", INVALID: "═",
                 DISABLED: "▽"},
        # ONE FLAP, turned or not. The seams above and below the flap are
        # the box; the character on its face is the mark. A split-flap board
        # never fills a length, and here it does not have to — the checkbox
        # is the one component in the family whose reading is a face.
        "checkbox.main": {DEFAULT: "▁ ▁", FOCUSED: "▔ ▔", ACTIVE: "▁·▁",
                          DISABLED: "╌ ╌"},
        "checkbox.knob": {DEFAULT: "▁▼▁", FOCUSED: "▔▲▔", ACTIVE: "▁█▁",
                          DISABLED: "╌▽╌"},
        # THE WHOLE CARD versus the split one. A checkbox here is a flap with
        # a gap between its seams — the box you look into. A radio is a card
        # whose seam runs UNBROKEN across it, because a departures board does
        # not tick a box, it turns one card in a rank to show the chosen
        # destination. Same three cells, different reading, and the seam is a
        # SHAPE before it is a colour.
        "radio.main": {DEFAULT: "▁▁▁", FOCUSED: "▔▔▔", ACTIVE: "▂▂▂",
                       DISABLED: "╌╌╌"},
        "radio.knob": {DEFAULT: "▁●▁", FOCUSED: "▔◉▔", ACTIVE: "▂█▂",
                       DISABLED: "╌▫╌"},
        # A CARD IN THE ROW, seams top and bottom: the word is printed on the
        # flap. Focus lifts the seam to the card's top edge, and the press is
        # the flap CAUGHT MID-TURN (▂) — this language's one mechanism, spent
        # here on an action instead of on a value.
        "button.main": {DEFAULT: "▁  ▁", FOCUSED: "▔  ▔", ACTIVE: "▂  ▂",
                        DISABLED: "╌  ╌"},
        # A CARD IN THE ROW: seams above and below, and the paper between
        # them. The press is the flap caught mid-turn, exactly as on the
        # button, so the two components read as one mechanism.
        "textfield.main": {DEFAULT: "▁·▁", FOCUSED: "▔·▔", EDITED: "▔▁▔",
                           ACTIVE: "▂·▂", INVALID: "═·═",
                           DISABLED: "╌╌╌"},
        "textfield.caret": {DEFAULT: "▮"},
        # THE RANK OF CARDS, which is the only thing this board has ever
        # drawn: the cards not yet reached are showing their SEAM, and the
        # run you are looking at has TURNED. A split-flap board never fills a
        # length and does not have to here — the window is a block of flaps
        # that have flipped, which is a shape before it is a tone.
        "scrollbar.main": {DEFAULT: "▔", DISABLED: "╌"},
        "scrollbar.indicator": {DEFAULT: "▄", DISABLED: "▫"},
        # THE RANK TURNING, one card either way — which is the only motion
        # this board has and the reason a stepper suits it: a departures
        # board does not show you the whole schedule, it turns to the entry
        # you asked for. The flap points the way it will turn; the press
        # catches it mid-turn (█), this language's one mechanism. At an end
        # there is no card behind the last one, so the seat is the bare SEAM.
        "stepper.main": {DEFAULT: "▁▁", DISABLED: "╌╌"},
        "stepper.step": {DEFAULT: "▲▼", FOCUSED: "▴▾", EDITED: "◆◆",
                         ACTIVE: "██", INVALID: "══",
                         DISABLED: "▽▽"},
    }

    def part_tone(self, part, state, name=None):
        """AMBER is spent on interaction, and the GRIP is the interaction —
        `control_of`, so a COMBINED `checked+disabled` is still dead."""
        if part == actuator(name) and control_of(state) != DISABLED:
            return self.c["accent"]
        return super().part_tone(part, state, name)

    def value_label(self, val, state=DEFAULT):
        return " " + self.cell(f"{max(0, min(99, int(val))):02d}",
                               self.c["ink"])

    def tabs(self, options, active):
        """The mode on screen takes the BAND; the rest are printed small.
        Two channels — reverse video AND case — so it survives greyscale."""
        c = self.c
        return "".join(
            self.band_row(f" {o.upper()} ", len(o) + 2) if o == active
            else f"[{c['mut']}] {o.lower()} [/]" for o in options)

    def icon(self, kind):
        """RED only on LATE. Every other departure code is printed in grey."""
        g = self.ICONS.get(kind, "")
        if not g:
            return ""
        tone = self.c["alert"] if kind == "overdue" else self.c["mut"]
        return f"[{tone}]{g}[/]"

    def display_cap(self, s: str) -> str:
        return s.upper()                   # tight caps: a flap cell is a cell

    def mascot(self):
        return []                          # a departure board keeps no pet

    def wordmark(self, text):
        # the board's own header, in the one treatment it owns
        cap = " ".join(text.upper())
        return [self.band_row(f" {cap} ", len(cap) + 2)]

    # ---- composition ------------------------------------------------------
    def board_layout(self):
        return "sections" if self.scheduled else "columns"

    def surface(self):
        """FLAT. The flap face is drawn per cell in markup, so no region may
        carry a panel of its own — a panelled column behind flap cells is two
        grounds fighting, and the seam stops reading as the only divider."""
        t = self.t
        # the scrollbar is toned to the SEAM on purpose: Textual draws its
        # thumb with the `▁▂▃…` ramp, so a brighter one reads as a stray seam
        # mark standing outside the grid (seen in the render at 118). Hover
        # and drag lift it to full ink, so the affordance is not renounced.
        return (f".kb-col, .kb-card, .kb-flat {{ background: {t['ground']}; }}\n"
                f".kb-flat, .kb-col {{\n"
                f"    scrollbar-background: {t['ground']};\n"
                f"    scrollbar-color: {t['seam']};\n"
                f"    scrollbar-color-hover: {t['ink']};\n"
                f"    scrollbar-color-active: {t['accent']}; }}")

    def composition(self):
        """THE SCHEDULE'S ROW GRID, and every rule here is anti-jiggle.

        The band sits TIGHT on the rows it heads (`margin-bottom: 0`), because
        a blank row under a band is a second divider and this language has
        exactly one. The air goes ABOVE the band instead, where it groups
        gates rather than separating rows.

        THE ROW BUDGET comes from the same law, not from a density wish:
        widget.tcss spends `margin-top: 1` above `#meter`, `#tiles`, `#tabs`
        and `#kb`, and under this language a blank row IS a divider drawn in
        air — which contradicts the one thing solari says about itself. The
        four are reclaimed and exactly ONE row of air is given back, to
        `.col-head`, where it groups GATES instead of separating rows.
        Measured: the board region goes 10 rows to 14 at 30 screen rows, and
        the schedule prints 6 departures instead of 4.

        `.kb-card:focus` is the SELECTION BAND: the row's ground goes amber
        and its ink goes to the ground colour. Its padding is restored to the
        unfocused value on purpose — widget.tcss shifts it to make room for a
        focus BORDER, and a language that spends no border would otherwise
        have every selected row jump one cell sideways, which is the exact
        jiggle a tabular board exists to prevent.
        """
        t = self.t
        return f"""
        #meter, #tiles, #tabs, #kb, #view {{ margin-top: 0; }}
        .col-head {{ margin-top: 1; margin-bottom: 0; }}
        .kb-card:focus {{ background: {t['accent']}; color: {t['ground']};
                          padding: 0 1; }}
        .tile:focus {{ padding: 0 1; }}
        """


class Blueprint(Kit):
    """THE CYANOTYPE TECHNICAL DRAWING. The frame stops CONTAINING and starts
    MEASURING: not one element on this sheet is boxed, and every quantity is a
    DIMENSION SPAN with its figure standing on the span itself.

    Commitments, each of which is a mechanism below and not a note:

    * **quantity is a DIMENSION SPAN** (`meter="dimension"`). `├──── 03D ────┤`
      — the run measures and the figure states, so the reading never depends on
      estimating a length. The scale is a CONSTANT (`SCALE_DAYS` for a due
      span, `SCALE_COUNT` for a head's load), which is what makes DATAVIZ.md
      law 2 true by construction: a kit method sees one row at a time and can
      never be handed its siblings' maximum, so a shared ceiling has to be
      declared rather than derived. Two spans anywhere on the sheet are
      comparable because neither was normalized to itself;
    * **NOTHING IS BOXED, at any width.** `layout="field"` lays items on an
      open field and hangs their metadata off an EXTENSION LEADER
      (`·── PROJ ── BACKLOG ── HIGH`). The only box-drawing glyphs this
      language draws are `─ ━ ├ ┤ ╌` (the dimension vocabulary), `┌ ┐ └ ┘`
      (registration marks) and the hatch — TEN, and not one of them is a
      vertical stroke or a rectangle junction, so a containing box here is not
      merely absent: it is unconstructable. (A terminator may stand alone in a
      two-cell seat — the calendar day — where a span does not fit. That is a
      renunciation, and it is the only place it happens.);
    * **a SERIES is an ORDINATE DIMENSION STACK** (`series()`). A conventional
      chart axis is `│` and `└` and is therefore unconstructable here, but an
      axis is not the only way to draw a trace: a drawing office schedules
      ordinate dimensions from a common datum, and this does the same — every
      sample a run from the sheet's left terminator, its figure standing on
      the run, and **the locus of the closing terminators IS the curve**. The
      vertical a plot appears to need is never drawn; it is the column the
      terminators fall in. The scale is PUBLISHED on the last row as a
      full-width span figured with the ceiling, which is what lets the ceiling
      be derived from the series without breaking DATAVIZ law 2 (found by the
      first app to carry this language, and decided rather than renounced —
      `tui-demos` LIMITS L-34);
    * **the whole frame budget is ONE TITLE BLOCK** (`frame="titleblock"`), a
      3-row stamp docked to the bottom corner carrying the sheet's identity,
      its revision date, its work tally and its state. Its two rules are the
      only strokes on the page, and `stamp()` builds it from ROWS OF CELLS so
      that an app with no mode strip can still have one (L-32);
    * **emphasis is KNOCKOUT** (`knockout=True`): exactly ONE element per view
      reverses to a pale ground with dark ink, and it is the title block's
      STATE cell. That is the first-fixation law here, and it is why chroma
      stays near zero — `ink`, `mut` and `dim` are one cyan family and the
      silhouette is carried by spans, leaders and the block;
    * **held work is HATCHED, never coloured** (`hatch="╱"`), so blocked reads
      with the colour stripped away and costs none of the rationed chroma;
    * **alert is spent on OVERDUE and nothing else.** A calm sheet carries zero
      `alert`.

    **The knockout is the title block's cell rather than the most overdue ITEM,
    and that is a deviation with a mechanical reason.** A kit method is handed
    one card at a time and has no cross-card knowledge, so "the single most
    urgent item" cannot be identified without ranking the cards in `kanban.py`
    (the shape of nord's selection problem). The one seat that DOES see the
    whole board is `Kit.mood`, which the app computes from the real task list,
    and the title block is where it lands. A per-item knockout is the named
    follow-up.
    """

    DISCLOSE = "╌"                        # the break line: it continues off-sheet
    DANGER_FORM = ("━", "━")               # the HEAVY weight, this alphabet's loudest mark

    OPEN, CLOSE = "├", "┤"                 # the dimension terminators
    EXT = "─"                              # the extension / span line
    LEAD = "·"                             # the leader's origin dot
    BREAK = "╌"                            # the CLIP flag: this span is off-scale
    REG = ("┌", "┐", "└", "┘")             # the registration marks
    GAP = 2                                # cells of air between fields
    SPAN_W = 16                            # the dimension field
    SCALE_DAYS = 14                        # THE SHARED CEILING for a due span
    SCALE_COUNT = 12                       # ... and for a head's load span
    ITEM_MIN = 20                          # a title below this is not useful
    TB_ROWS = 3                            # the title block's height
    TB_MIN = 42                            # the narrowest live `#tabs` seat
    # THE TITLE BLOCK'S DECLARED DROP ORDER. STATE never drops: it is the
    # knockout, and the knockout is this sheet's first fixation.
    TB_DROP = ("sheet", "rev", "work")
    SHEET = "TASKBOARD"
    STATE = {"alert": "OVERDUE", "busy": "IN WORK", "clear": "CLEAR"}
    PRIO = {"low": "LOW", "normal": "NORM", "high": "HIGH"}

    CUR = "┌"                              # the registration mark, one corner
    SPIN = ("┌", "┐", "┘", "└")            # a registration mark walking a box

    ICONS = {"deadline": "DIM", "overdue": "OVR", "wip": "WIP",
             "blocked": "", "workday": "DAY", "boardfile": "SHT"}

    VOICE = {"empty": "NO ITEMS ON SHEET", "no_signals": "NO SIGNALS SPECIFIED"}

    # what the title block last learned about the board: `(done, total, w)`.
    # A class default so an un-driven kit renders honestly instead of raising.
    _sheet: tuple[int | None, int | None, int] = (None, None, TB_MIN)

    # ---- tokens -----------------------------------------------------------
    @property
    def hatch(self) -> str:
        """The stroke a HELD span is filled with. A shape, not a hue."""
        return self.t.get("hatch", "╱")

    @property
    def knockout(self) -> bool:
        return bool(self.t.get("knockout"))

    @property
    def titled(self) -> bool:
        """The `frame` token. "titleblock" is not a rule glyph — it moves the
        whole frame budget into the bottom-corner stamp, so this language's
        frame turns the BLOCK on and every other stroke off."""
        return self.frame == "titleblock"

    @property
    def fielded(self) -> bool:
        """The `layout` token. Anything but "field" (the base default "flow"
        included) gives back the generic composition, byte for byte."""
        return self.layout == "field"

    def rule_line(self, w):
        """The sheet rules nothing. The title block owns the only two strokes
        on the page, and a card is never boxed."""
        return None if self.titled else super().rule_line(w)

    @property
    def glyphs(self) -> frozenset[str]:
        """THE TEN, as data rather than as prose.

        The class docstring enumerates this language's whole alphabet and then
        makes a claim about it — *not one of them is a vertical stroke or a
        rectangle junction, so a containing box here is not merely absent: it
        is unconstructable*. A claim that strong is worth a test, and a test
        needs the set; stated only in prose it was checkable by reading and by
        nothing else, which is how `series()` came to be asked for (L-34).

        Each member is read off where it already lives rather than restated:
        `━` is the `dimension` ramp's heavy end, which is where this
        language's meters are drawn from, and the hatch is a token. `·` is the
        leader's ORIGIN DOT and not a box-drawing mark, which is why the
        docstring's count is ten and this set's is ten."""
        return frozenset(self.OPEN + self.CLOSE + self.EXT + self.BREAK
                         + "".join(self.REG) + COVER_RAMPS["dimension"][-1]
                         + self.hatch)

    # ---- the dimension span -----------------------------------------------
    def dimension(self, n: int, label: str, fill: str | None = None,
                  clipped: bool = False, outside: bool = True) -> str:
        """This language's own span, drawn through the shared mechanism."""
        return _span_text(n, label, fill or self.EXT, self.OPEN, self.CLOSE,
                          clipped, self.BREAK, outside)

    @staticmethod
    def _pad(text: str, n: int, right: bool = False) -> str:
        """Exactly `n` cells. Width math runs BEFORE escaping (module rule)."""
        if n <= 0:
            return ""
        t = text if len(text) <= n else text[: max(0, n - 1)] + "…"
        pad = " " * (n - len(t))
        return (pad + mark(t)) if right else (mark(t) + pad)

    @staticmethod
    def _read(chip: str) -> tuple[int | None, str]:
        """`(days, state)` from the chip. One derivation path for the whole
        language: the chip IS the task state (kanban.py computes it from the
        due date, the blocked flag and the done column), so the span and the
        row beside it can never disagree."""
        c = (chip or "").strip()
        if c == "done":
            return None, "done"
        if c == "blk":
            return None, "blocked"
        late = c.endswith("!")
        body = c[:-1] if late else c
        if body.endswith("d") and body[:-1].lstrip("-").isdigit():
            return int(body[:-1]), ("late" if late else "due")
        return None, "none"

    def _cells(self, days: int, ceiling: int | None = None) -> int:
        """Cells the span occupies, on the SHARED scale. The ceiling is a
        CONSTANT and not the siblings' maximum, because a kit method is handed
        one row at a time — declaring the scale is the only way two spans on
        one page can be compared (DATAVIZ.md law 2)."""
        top = ceiling or self.SCALE_DAYS
        d = min(abs(int(days)), top)
        inner = round((self.SPAN_W - 2) * d / top)
        if d and inner == 0:
            inner = 1                      # MICROBAR FLOOR (DATAVIZ law 3):
            # a one-day span must not round down onto the zero-day span
        return inner + 2

    @staticmethod
    def _fig(days: int) -> str:
        d = abs(int(days))
        return f"{d:02d}" if d <= 99 else "99+"

    # ---- the dimensioned trace --------------------------------------------
    # THE LANGUAGE'S ANSWER TO A SERIES, and it is an answer rather than a
    # renunciation (L-34, decided in this batch's spec 6.1).
    #
    # L-34 is right that a conventional chart axis is UNCONSTRUCTABLE here:
    # every terminal plot axis is `│` and `└`, and neither is among the ten
    # marks this language draws. It is also right that `dimension()` is the
    # wrong mechanism for a series — it measures ONE quantity against a
    # declared ceiling, which is a bar.
    #
    # But what is unconstructable is an AXIS, and a series is not an axis. A
    # drawing office does not plot with an axis box; it draws a SCHEDULE OF
    # ORDINATE DIMENSIONS from a common datum — every sample a run from the
    # same left terminator, its length the value, the figure standing on the
    # run. Stack those rows and **the locus of the closing terminators IS the
    # trace**: the curve is drawn in `┤`, the datum in `├`, the run in `─`,
    # the off-scale flag in `╌`. The vertical the plot appears to need is
    # never drawn — it is the column the terminators happen to fall in, which
    # is exactly what an ordinate dimension looks like on paper.
    #
    # Renunciation was the other option and it was rejected because a
    # renunciation has to follow from something the language BELIEVES. Ledger
    # refuses images because "a figure is audited, not shown"; solari because
    # "one shape, the row; an image cannot flip". This language's doctrine
    # points the other way — *the frame stops CONTAINING and starts MEASURING*,
    # *the only language here where the chrome IS the data-viz*, *fits:
    # anything spatial, anything with extents and tolerances* — and a series is
    # a sequence of extents. Renouncing plots would have been the first
    # renunciation here adopted for a short alphabet rather than for a
    # commitment.

    def _trace_cells(self, v: float, top: float, w: int) -> int:
        """Cells one sample occupies in a `w`-cell seat.

        Deliberately NOT `_cells()`, which is the CARD's span: that one takes
        integer days against `SCALE_DAYS` in a `SPAN_W` seat, and widening it
        to floats would have put the board's every due date through a code
        path a convergence curve asked for. Same LAW, twice — including the
        microbar floor — because the law is DATAVIZ's and not this method's.
        """
        run = max(1, w - 2)
        d = min(abs(float(v)), top)
        inner = round(run * d / top)
        if d and inner == 0:
            inner = 1                      # MICROBAR FLOOR (DATAVIZ law 3):
            # a sample that is small must not round onto a sample that is zero
        return inner + 2

    @staticmethod
    def _sample(vals: list[float], n: int) -> list[float]:
        """`n` samples spanning `vals`, ALWAYS including both endpoints.

        A trace's endpoints are its datum — where the run started and where it
        got to — so a subsample that dropped either would be answering a
        different question from the one a convergence curve is asked."""
        if not vals or n < 1:
            return []
        if len(vals) <= n:
            return list(vals)
        if n == 1:
            return [vals[-1]]
        step = (len(vals) - 1) / (n - 1)
        return [vals[round(i * step)] for i in range(n)]

    def series(self, values, w: int, h: int, ceiling: float | None = None,
               label: str = "") -> list[str]:
        """A SERIES AS A DIMENSIONED TRACE — exactly `h` rows of `w` cells.

        Each sample is a span from the sheet's left datum, its run the value,
        its figure standing on the run; the ragged column of closing
        terminators is the trace. Nothing is boxed, no vertical is drawn, and
        every mark is one of this language's ten.

        THE SCALE IS STATED, and that is the half `dimension()` could not do.
        DATAVIZ law 2 forbids normalising a row to itself, and a kit method
        handed ONE row at a time can only obey it by declaring a constant
        (`SCALE_DAYS`). A series is the one case where the siblings are in
        hand — so the ceiling may be derived, and therefore MUST be published:
        the last row is a full-width span figured with the ceiling, which is a
        scale bar and means "this width is that value". Pass `ceiling` to
        compare two traces against a shared scale; leave it out and the trace
        is normalised to itself and says so on the sheet.

        THE DECLARED LADDER when the seat is short: the SCALE row never drops
        — a trace whose scale is unstated is precisely the reading law 2
        exists to prevent — the label goes first, and the samples reduce after
        that (`_sample`, which keeps both endpoints).

        The figure is dropped rather than pushed outside its span
        (`outside=False`): a figure lettered PAST the closing terminator would
        put ink to the right of the value, and the whole reading of this
        mechanism is that nothing stands right of a terminator except the
        terminators of longer samples."""
        c = self.c
        w, h = max(4, int(w)), max(2, int(h))
        vals = [float(v) for v in values]
        head = [str(label).upper()] if (label and h >= 3) else []
        seats = max(1, h - 1 - len(head))
        pts = self._sample(vals, seats)
        # DERIVED FROM THE WHOLE SERIES, NOT FROM THE SEATS THAT FIT. Reading
        # the ceiling off `pts` made the scale depend on the height of the
        # region: the same data in a shorter seat came back drawn against a
        # different ceiling, and at one seat the trace's LAST value rendered
        # full-width — a converged run shown touching full scale. Caught by
        # the ladder test at h=3.
        top = abs(float(ceiling)) if ceiling else max(
            (abs(v) for v in vals), default=0.0)
        top = top or 1.0

        def row(span: str, tone: str) -> str:
            # width math on the plain span, `mark()` on the way out
            return f"[{tone}]{mark(_plain(span, w))}[/]"

        out = [row(self.dimension(w, s, outside=False), c["mut"])
               for s in head]
        calm = self.t.get("calm", c["ink"])
        for v in pts:
            out.append(row(self.dimension(
                self._trace_cells(v, top, w), f"{v:.3g}",
                clipped=abs(v) > top, outside=False), calm))
        # an empty series still states its scale, and the seat it could not
        # fill stays blank rather than being closed up — the sheet says "no
        # samples", not "a shorter trace"
        out += [" " * w] * max(0, h - 1 - len(out))
        out.append(row(self.dimension(w, f"{top:.3g}", outside=False),
                       c["mut"]))
        return out[:h]

    def _span(self, days: int | None, state: str) -> tuple[str, str]:
        """`(the span, exactly SPAN_W cells, its tone)`.

        HELD wears the HATCH and keeps the field's full width: a held item has
        no schedule to measure, so its span states a CONDITION rather than a
        quantity — and the hatch is a SHAPE, so the reading survives greyscale
        and spends none of this language's rationed colour. ALERT appears here
        and only here, on a span that is genuinely past its date."""
        c = self.c
        if state == "blocked":
            return (self._pad(self.dimension(self.SPAN_W, "HELD", self.hatch),
                              self.SPAN_W), c["mut"])
        if state == "done":
            return (self._pad(self.dimension(self.SPAN_W, "DONE"),
                              self.SPAN_W), c["dim"])
        if days is None:
            # an UNDIMENSIONED feature: a leader running to a note, and
            # deliberately not a zero-length span — absence is not a measure
            return (self._pad(f"{self.LEAD}{self.EXT} NO DATE", self.SPAN_W),
                    c["dim"])
        clipped = abs(int(days)) > self.SCALE_DAYS
        late = state == "late"
        lab = self._fig(days) + ("D!" if late else "D")
        tone = (c["alert"] if late
                else (c["warn"] if 0 <= days <= 3 else self.t.get("calm",
                                                                  c["ink"])))
        return (self._pad(self.dimension(self._cells(days), lab,
                                         clipped=clipped), self.SPAN_W), tone)

    # ---- ONE GEOMETRY SEAT -------------------------------------------------
    def field(self, w: int) -> list[tuple[int, str, int]]:
        """The sheet's columns for a row of `w` cells: `(origin, code, width)`,
        filling the measure EXACTLY. Read by the card, by the HEAD and by every
        acceptance check — the `Ledger.cols` / `Swiss.grid` / `Nord.panes` /
        `Instrument.reticle` / `Corgi.slots` / `Solari.fields` precedent, and
        the reason a head's span and its items' spans stand on one column.

        THE DECLARED DEGRADE, in two steps and no more: below
        `ITEM_MIN + GAP + SPAN_W` the DIMENSION FIELD is renounced whole (the
        reading moves onto the extension leader — the sheet loses a dimension,
        never the datum); below `ITEM_MIN` the sheet itself is renounced and
        the row falls back to the generic card, which can never be worse than
        the form it replaced (swiss's grid law). A span is never squeezed:
        a run shorter than its own terminators cannot measure anything.
        """
        item = w - self.SPAN_W - self.GAP
        if item >= self.ITEM_MIN:
            return [(0, "item", item), (item + self.GAP, "span", self.SPAN_W)]
        if w >= self.ITEM_MIN:
            return [(0, "item", w)]
        return []

    # ---- the item on the field --------------------------------------------
    def card_rows(self, title, chip, tone, w, idx=0, urgent=False, meta=None):
        """TWO rows: the item with its dimension, and the EXTENSION LEADER that
        carries its metadata. The leader is where this language's air went —
        a drawing annotates its white space rather than leaving it blank, which
        is why `pitch` is 1 and not the 2 an airy language would take."""
        if not self.fielded:
            return super().card_rows(title, chip, tone, w, idx, urgent, meta)
        fs = self.field(w)
        if not fs:
            return super().card_rows(title, chip, tone, w, idx, urgent, meta)
        c, m = self.c, (meta or {})
        days, state = self._read(chip)
        span, stone = self._span(days, state)
        codes = [code for _, code, _ in fs]
        top = f"[{c['ink']}]{self._pad(title.upper(), fs[0][2])}[/]"
        if "span" in codes:
            top += " " * self.GAP + f"[{stone}]{span}[/]"
        # the leader, with progressive disclosure: fields that do not fit are
        # DROPPED, never folded (a wrapped leader grows the card a phantom row)
        parts: list[tuple[str, str]] = []
        if "span" not in codes:
            sp = span.strip()
            parts.append((f"[{stone}]{mark(sp)}[/]", sp))
        for v in ((m.get("proj") or "").upper(), (m.get("phase") or "").upper(),
                  self.PRIO.get((m.get("prio") or "").lower(), "")):
            if v:
                parts.append((f"[{c['mut']}]{mark(v)}[/]", v))
        lead = f"{self.LEAD}{self.EXT * 2} "
        sep = f" {self.EXT * 2} "
        out, used, room = [], 0, w - len(lead)
        for mk, pl in parts:
            step = len(pl) + (len(sep) if out else 0)
            if used + step > room:
                break
            if out:
                out.append(f"[{c['mut']}]{sep}[/]")
            out.append(mk)
            used += step
        return [top, f"[{c['mut']}]{lead}[/]" + "".join(out)]

    def card_row(self, title, chip, tone, w, idx=0, urgent=False):
        # the guards are repeated rather than delegated: `Kit.card_rows` calls
        # `self.card_row`, so a card_row that answered by calling card_rows
        # would recurse forever on the degraded path
        if not self.fielded or not self.field(w):
            return super().card_row(title, chip, tone, w, idx, urgent)
        return self.card_rows(title, chip, tone, w, idx, urgent, None)[0]

    # ---- the phase head ----------------------------------------------------
    def head(self, name, count, w, idx=0):
        """The phase is a FEATURE on the sheet and its load is DIMENSIONED, on
        the same geometry seat the items under it use — so the head's span and
        the items' spans stand in one column and the page reads as one drawing.

        The two spans carry different QUANTITIES (items vs days) on different
        constants, which is what a drawing does when it dimensions two things
        on one column; what they share is the origin, not the scale."""
        if not (self.fielded and self.titled):
            return super().head(name, count, w, idx)
        fs = self.field(w)
        if not fs:
            return super().head(name, count, w, idx)
        c = self.c
        fig = f"{min(count, 99):02d}"
        tone = c["ink"] if count else c["dim"]
        if len(fs) > 1:
            sp = self.dimension(self._cells(count, self.SCALE_COUNT), fig,
                                clipped=count > self.SCALE_COUNT)
            return (f"[{c['mut']}]{self._pad(name.upper(), fs[0][2])}[/]"
                    + " " * self.GAP
                    + f"[{tone}]{self._pad(sp, self.SPAN_W)}[/]")
        # the DIMENSION is renounced, the COUNT is not: the figure stands tight
        # against the name, which is where a drawing puts a note it has no room
        # to dimension. An empty phase still reads `00`.
        n = fs[0][2]
        return (f"[{c['mut']}]{self._pad(name.upper(), n - len(fig) - 1)}[/] "
                f"[{tone}]{fig}[/]")

    # ---- the view section header ------------------------------------------
    def sect(self, title, note, w, h=0):
        """Drawn display type RENOUNCED — a drawing letters everything at one
        height, so `h` buys nothing and that is a decision. The note hangs off
        the title on a leader, like every other annotation here."""
        c = self.c
        return [f"[{c['ink']}]{mark(title.upper())}[/]  "
                f"[{c['mut']}]{self.LEAD}{self.EXT * 2} "
                f"{mark(note.upper())}[/]", ""]

    # ---- quantity everywhere else -----------------------------------------
    def bar(self, span, head=None, tone=None):
        """NOT a fill — a dimension span exactly as wide as the seat the caller
        reserved, with the count on it. The travelling packet is one cell of
        the run drawn as a BREAK: a drawing animates by moving a mark along a
        line, it never lights the line up."""
        c = self.c
        n = max(1, span)
        if n < 3:
            return f"[{tone or c['ink']}]{(self.OPEN + self.CLOSE)[:n]}[/]"
        body = list(self.dimension(n, f"{min(n, 99):02d}", outside=False))
        if head is not None:
            for i in range(1, n - 1):
                if i < len(head) and head[i] and body[i] == self.EXT:
                    body[i] = self.BREAK
                    break
        return f"[{tone or c['ink']}]{''.join(body)}[/]"

    GANTT = ("─", "╌", "┤", "·", "┐")      # extension line, break, terminator

    def cal_cell(self, state):
        """A calendar day is a TWO-CELL seat, which is narrower than any span
        this language can draw, so the terminator stands alone and the span is
        renounced — the one place that happens, and it is a renunciation, not
        a box. All four states differ in SHAPE: the render at 60 caught an
        earlier draft where `over` and `multi` were the same glyph pair in
        different hues, which is a state readable in colour alone."""
        c = self.c
        return {"none": f"[{c['dim']}]{self.LEAD * 2}[/]",
                "one": f"[{c['mut']}]{self.EXT}{self.CLOSE}[/]",
                "multi": f"[{c['ink']}]{self.OPEN}{self.CLOSE}[/]",
                # a BROKEN span: this day is past its date
                "over": f"[{c['alert']}]{self.BREAK}{self.CLOSE}[/]"}[state]

    def queue_marker(self, i):
        c = self.c
        return (f"[{c['mut']}]{min(i + 1, 99):02d}[/]" if self.numbered
                else f"[{c['mut']}]{self.LEAD}{self.EXT}[/]")

    def field_row(self, caption, value, w):
        """A DIMENSION: the name stands at its datum, the extension line runs
        out of it, and the figure terminates the run.

        This is what a drawing office does with a caption and a value, and it
        is the one mechanism here that is a MEASUREMENT rather than a fill:
        the line does not close a gap, it STATES the distance between the
        thing named and the figure that answers for it.  Both marks it spends
        are already in the ten (`LEAD`, `EXT`) -- no vertical stroke, nothing
        boxed, at any width."""
        c = self.c
        cap, val = str(caption).upper(), str(value)
        room = max(1, w - len(cap) - len(val) - 3)
        return (f"[{c['ink']}]{mark(cap)}[/] "
                f"[{c['dim']}]{self.LEAD + self.EXT * room}[/] "
                f"[{c['ink']}]{mark(val)}[/]")

    def tile_row(self, val, label, tone, w):
        """The reading first, on a leader running to its name."""
        c = self.c
        v = (val or "").strip() or "--"
        room = max(1, w - len(v) - 4)
        return (f"[{tone}]{mark(v)}[/] [{c['dim']}]{self.EXT * 2}[/] "
                f"[{c['mut']}]{self._pad(label.upper(), room)}[/]")

    # ---- the title block ---------------------------------------------------
    def meter(self, done, total, counts, w):
        """THE TITLE BLOCK'S WORK CELL AND ITS MEASURE, learned here.

        A kit method is handed one surface at a time; this is the ONE call the
        app makes with the board's whole tally and with the aperture's content
        width, and `tabs()` (which is handed neither) is updated immediately
        after it in `app._after_hero`. So the block reads its figures from the
        same redraw that drew the meter, and never from the previous one.
        Before the first meter call the cell honestly reads `--/--` and the
        block falls back to its narrowest live seat — the `self.mood`
        precedent: render-pipeline state, declared and degrading."""
        self._sheet = (done, total, max(self.TB_MIN, int(w)))
        return super().meter(done, total, counts, w)

    def _mode_strip(self, options, active) -> tuple[str, str, tuple[int, int]]:
        """`(plain, markup, (left, right))` — the modes, the one on screen in
        caps, and the two cells its REGISTRATION MARKS stand on."""
        c = self.c
        plain, parts, reg = " ", [" "], (-1, -1)
        for i, o in enumerate(options):
            if i:
                plain += "  "
                parts.append("  ")
            word = o.upper() if o == active else o.lower()
            if o == active:
                reg = (len(plain) - 1, len(plain) + len(word))
                parts.append(f"[{c['ink']}]{mark(word)}[/]")
            else:
                parts.append(f"[{c['mut']}]{mark(word)}[/]")
            plain += word
        return plain, "".join(parts), reg

    def _state_cell(self) -> tuple[str, bool]:
        """`(text, knocked)`. The board MOOD is the only board-wide fact a kit
        is given, and the app derives it from the real task list (anything
        overdue and not done).

        TWO CHANNELS, which is why the token owns the SHAPE as well as the
        reverse video: under `knockout` the state is DIMENSIONED — a real span
        with the word riding on it — and reverse video is then spent on
        ATTENTION alone. Reverse video is a ground colour and nothing else, so
        a knockout that carried no shape would be a state readable in colour
        only (COMPONENTS.md's two-channel law), and it would vanish from every
        greyscale check in this suite.

        The reverse fires on `alert` alone, so a sheet with nothing overdue
        carries no reversed cell at all — and still states its condition."""
        word = self.STATE.get(self.mood, "CLEAR")
        if self.knockout:
            return (self.dimension(len(word) + 4, word),
                    self.mood == "alert")
        return (f" {word} ", False)

    def block_cells(self, w: int, strip_w: int) -> list[tuple[str, str, bool]]:
        """The title block's `(caption, value, knocked)` cells at width `w`,
        and the declared order a narrow sheet SHEDS them in."""
        done, total, _ = self._sheet
        work = ("--/--" if total is None
                else f"{min(done, 99):02d}/{min(total, 99):02d}")
        state, knocked = self._state_cell()
        spec = [("sheet", ("SHEET", self.SHEET, False)),
                ("rev", ("REV", date.today().isoformat(), False)),
                ("work", ("WORK", work, False)),
                ("state", ("", state, knocked))]
        for dropped in range(len(self.TB_DROP) + 1):
            gone = set(self.TB_DROP[:dropped])
            cells = [v for code, v in spec if code not in gone]
            if strip_w + self.GAP + self.block_w(cells) <= w:
                return cells
        return [spec[-1][1]]

    def block_w(self, cells) -> int:
        return (sum(len(cap) + 1 + len(val) if cap else len(val)
                    for cap, val, _ in cells)
                + self.GAP * max(0, len(cells) - 1))

    def stamp(self, rows, w: int, strip=None) -> list[str]:
        """THE SHEET'S STAMP — two rules bracketing rows of cells, docked to
        the bottom corner, and the only frame this language spends.

        CONTENT IS DATA, SELECTION IS AN EXTRA, and that is the whole of L-32.
        `rows` is a list of body rows, each a list of `(caption, value,
        knocked)` cells — the same triple `block_cells()` builds, with nothing
        about a taskboard in it. `strip` is `(options, active)` for an app
        that HAS a mode strip and `None` for one that does not.

        The old entry point was `title_block(options, active, w)`, whose first
        two parameters are a MODE STRIP's options and the mode on screen:
        taskboard's content, and a concept a parameter study does not have. So
        this language's single largest frame investment was reachable only
        from an app that happened to have a nav row, and the first outside
        consumer (emersio-lab, 2026-09-04) rebuilt the block out of `EXT` and
        `REG` rather than fake a mode strip to obtain a stamp — re-deriving
        the docking arithmetic below, and standing up a second copy of the
        mark this language is most identified by. **A component whose
        parameters name its first caller's domain has been specialised, not
        generalised**, and that fork was forced by an interface rather than
        chosen. `title_block()` is now a three-line adapter over this.

        The mode on screen is bracketed by REGISTRATION MARKS instead of a
        border, which is the selection mechanism this language owns (`┌ ┐`
        above, `└ ┘` below — four separate corners that never join, so nothing
        here is a box). An app with no strip gets NO registration marks: there
        is nothing selected to register, which is not the same as registering
        nothing.

        THE DECLARED LADDER, when the sheet is too narrow for all of it:
        tier 1 sheds cells — and tier 1 belongs to the CALLER, because which
        cell a sheet can afford to lose is the sheet's own knowledge
        (`block_cells()` is taskboard's answer, in `TB_DROP` order, and the
        lab's rows are the lab's); tier 2 gives up the modes the sheet is NOT
        on (the block is the sheet's identity and may not be cut for a nav
        row); tier 3 renounces the strip entirely and keeps the cells, because
        the state is the knockout.
        """
        c = self.c
        w = max(12, int(w))
        rows = [list(r) for r in rows] or [[]]
        # THE BLOCK IS AS WIDE AS ITS WIDEST ROW. One body row is taskboard's
        # case and the arithmetic never had to know it; the lab's stamp has
        # two, and a block sized to the first of them would dock the second
        # off the edge.
        bw = max(self.block_w(r) for r in rows)
        s, strip_mk, reg = "", "", (-1, -1)
        if strip is not None:
            options, active = strip
            s, strip_mk, reg = self._mode_strip(options, active)
            if len(s) + self.GAP + bw > w:
                s, strip_mk, reg = self._mode_strip([active], active)
            if len(s) + self.GAP + bw > w:
                s, strip_mk, reg = "", "", (-1, -1)
        x = max(0, w - bw)
        if s:
            x = max(x, len(s) + self.GAP)
        # the two rules — from the block's own origin to the sheet's edge —
        # and the registration marks, which never touch them
        top = [" "] * w
        bot = [" "] * w
        for i in range(min(x, w), w):
            top[i] = bot[i] = self.EXT
        lx, rx = reg
        if 0 <= lx and rx < x:
            top[lx], top[rx] = self.REG[0], self.REG[1]
            bot[lx], bot[rx] = self.REG[2], self.REG[3]

        def paint(row: list[str]) -> str:
            out, i = [], 0
            while i < w:
                ch = row[i]
                j = i
                while j < w and row[j] == ch:
                    j += 1
                if ch == " ":
                    out.append(" " * (j - i))
                elif ch == self.EXT:
                    out.append(f"[{c['mut']}]{ch * (j - i)}[/]")
                else:
                    out.append(f"[{c['ink']}]{ch * (j - i)}[/]")
                i = j
            return "".join(out)

        mids = []
        for r, cells in enumerate(rows):
            body = []
            for n, (cap, val, knocked) in enumerate(cells):
                if n:
                    body.append(" " * self.GAP)
                if cap:
                    body.append(f"[{c['mut']}]{cap}[/] "
                                f"[{c['ink']}]{mark(val)}[/]")
                elif knocked:
                    # KNOCKOUT: the cell reverses — pale ground, dark ink.
                    # Exactly one of these exists on a view, and it is the
                    # first fixation. THROUGH `knockout_cell` since inc17, so
                    # that the mark operator ruling 10 lets MOVE to a
                    # confirm's default answer is the same mark, not a
                    # second one spelled the same way.
                    body.append(self.knockout_cell(val))
                else:
                    body.append(f"[{c['mut']}]{mark(val)}[/]")
            # THE STRIP RIDES THE FIRST BODY ROW and the rest are indented to
            # the block's origin. `strip_mk` is "" when there is no strip, so
            # the two branches are one expression rather than a special case.
            pre = (strip_mk + " " * max(0, x - len(s)) if r == 0
                   else " " * x)
            # EXACTLY `w` CELLS, INCLUDING THE SHORT ROWS. On one body row the
            # docking arithmetic lands on `w` by construction (`x = w - bw`,
            # and the narrowing ladder runs until the strip fits beside it), so
            # this pad was zero for the whole life of the board's block and the
            # rectangle was exact by luck rather than by rule. A stamp with a
            # NARROWER second row came back 9 cells short — a ragged frame,
            # which is the one thing a reserved rectangle cannot be. Measured
            # on the plain cells (`block_w`) and never on the markup.
            mids.append(pre + "".join(body)
                        + " " * max(0, w - x - self.block_w(cells)))
        return [paint(top), *mids, paint(bot)]

    def title_block(self, options, active, w: int) -> list[str]:
        """The board's three-row title block — a THIN ADAPTER over `stamp()`.

        It survives with its signature intact so the board's captures stay
        byte-identical, and it now holds exactly what is taskboard's about the
        block: one body row, whose cells `block_cells()` chooses (tier 1 of
        the narrowing ladder, in `TB_DROP` order) against the width the full
        mode strip would want. Everything else — the docking arithmetic, the
        two rules, the registration marks, the knockout — is the mechanism's.
        """
        w = max(12, int(w))
        strip, _, _ = self._mode_strip(options, active)
        return self.stamp([self.block_cells(w, len(strip))], w,
                          strip=(options, active))

    def tabs(self, options, active):
        if not (self.fielded and self.titled):
            return super().tabs(options, active)
        return "\n".join(self.title_block(options, active, self._sheet[2]))

    # ---- the components ----------------------------------------------------
    # the span is DRAWN IN, terminator first
    MOTION_STEPS = 2

    # A DIMENSION BEING SET. The opening terminator is fixed chrome (a datum
    # does not move), the extension line is the measured extent, the closing
    # terminator is the knob, and the unmeasured remainder is leader dots.
    # Nothing is filled and nothing is boxed, which is this sheet's law.
    COMP_CHROME = (OPEN, "")
    def overlay_instead(self, rows, w, h, under):
        """REGISTRATION MARKS, and the four corners NEVER JOIN.

        "Not one element on this sheet is boxed, at any width", and the ten
        marks contain no vertical stroke -- so a dialog box is unconstructable
        twice over. What marks a region on a drawing is the REGISTRATION
        PAIR: `┌   ┐` above and `└   ┘` below, with AIR where a stroke would
        be. Running a rule between them makes a lid however it is spelled,
        which is the correction this language's own prototype needed.

        The sheet behind stays visible and recedes, because a revision note
        does not hide the view it annotates."""
        c = self.c
        body = [visible(r) for r in rows]
        dw = min(max(8, w), max(len(b) for b in body) + 4)
        x = max(0, (w - dw) // 2)
        corners = lambda a, b: (f"[{c['ink']}]{mark(a)}[/]"
                                + " " * (dw - 2)
                                + f"[{c['ink']}]{mark(b)}[/]")
        block = [corners("┌", "┐")] + list(rows) + [corners("└", "┘")]
        y = max(0, (h - len(block)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(block):
                row = block[i - y]
                out.append(" " * x + row)
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out

    def pane_split_instead(self, h, w=3):
        """TWO DATUMS, AND THE AIR BETWEEN THEM.

        This language is in `PANE_SPLIT_REFUSED` on an ALPHABETIC refusal:
        none of its ten marks is a vertical stroke, so a pane rule is
        unconstructable. What a drawing office does with two views on one
        sheet is give each its own datum — so the left field TERMINATES and
        the right field OPENS, once, on the row where the panes begin, and
        the rest is air.

        `┤` and `├` are the two terminators this language already spends on
        every dimension it draws, and they are the marks the whole
        vocabulary is built on. THEY NEVER JOIN: no stroke runs between them,
        which is the same law the registration pair obeys ("four corners that
        never join"). One row of declaration and `h-1` rows of nothing is a
        DIMENSION, not a decoration — it states an extent and then stops.

        AND BELOW TWO CELLS THERE IS NO EXTENT TO STATE, so the declaration
        row is not drawn at all. This was a closure-law defect until inc36's
        width sweep found it: the pair was written unconditionally and at
        `w=1` it returned TWO cells for a one-cell seat, which is the one
        thing `pane_split`'s contract forbids — a row that is not `w` wide
        moves the right pane down the page. The honest degradation for a
        language whose refusal IS air is more air."""
        rows = [" " * w for _ in range(max(0, h))]
        if rows and w >= 2:
            rows[0] = (f"[{self.c['dim']}]{mark('┤')}[/]"
                       + " " * max(0, w - 2)
                       + f"[{self.c['dim']}]{mark('├')}[/]")
        return rows

    # THE VALIDATION ROW IS A REVISION NOTE: lettered on a DASHED extension
    # out of the feature that changed, which is what `╌` is for on this
    # sheet and what its WARN rung already spells.
    #
    # AND IT SPENDS NO ALERT. "A calm sheet carries zero alert" -- the hue is
    # rationed to overdue and nothing else, and `log_row` already guards it.
    ERROR_FILL = "╌"
    ERROR_TONE = "ink"
    # AN OPENING TERMINATOR. On a drawing an unfigured dimension is a
    # REFERENCE and a figured one is required; the mark that says an extent
    # must be given is the terminator that opens it. `━` was the other
    # candidate and it is spent twice already (DANGER_FORM, ERROR).
    REQUIRED = "├"

    LEVELS = {"info": "··", "warn": "╌╌", "error": "━━"}

    MATCH_STYLE = "bold {ink}"             # the heavy weight, in type

    def keyhint(self, pairs, w=0):
        """An extension line from the key to what it does -- the same
        dimension the sheet draws everywhere else, at two cells."""
        c = self.c
        return "   ".join(f"[{c['ink']}]{mark(str(k))}[/]"
                          f"[{c['dim']}]{self.EXT * 2}[/]"
                          f"[{c['mut']}]{mark(str(v).upper())}[/]"
                          for k, v in pairs)

    PART_GLYPHS = {
        "main": {DEFAULT: LEAD, DISABLED: BREAK},
        "indicator": {DEFAULT: EXT, DISABLED: "┄"},
        "knob": {DEFAULT: CLOSE, FOCUSED: "╡", EDITED: "╪",
                 ACTIVE: "┫", INVALID: "├",
                 DISABLED: "╎"},
        # NOTHING IS BOXED ON THIS SHEET, and the checkbox does not get to
        # break that. So it is not a box: it is a DATUM between two
        # terminators, blank until the note is entered. The mark sits between
        # the terminators, which satisfies containment without a box ever
        # being drawn — the law is about the mark staying inside its main,
        # not about brackets.
        "checkbox.main": {DEFAULT: "├ ┤", FOCUSED: "╞ ╡", ACTIVE: "┣ ┫",
                          DISABLED: "╎ ╎"},
        "checkbox.knob": {DEFAULT: "├╪┤", FOCUSED: "╞╪╡", ACTIVE: "┣╪┫",
                          DISABLED: "╎╌╎"},
        # THE DATUM TURNED INWARD. The checkbox's terminators point out (a
        # dimension measured across a gap); the radio's point IN, which on a
        # drawing is a callout selecting one item from a schedule. Nothing is
        # boxed here and nothing is boxed here either — the law survives the
        # new component, which is what a language law is for.
        "radio.main": {DEFAULT: "┤ ├", FOCUSED: "╡ ╞", ACTIVE: "┫ ┣",
                       DISABLED: "╏ ╏"},
        "radio.knob": {DEFAULT: "┤○├", FOCUSED: "╡◉╞", ACTIVE: "┫●┣",
                       DISABLED: "╏╌╏"},
        # A TITLE-BLOCK CELL: two extension lines with the callout between
        # them, which is how this language bounds anything at all — nothing
        # is BOXED here, and two verticals are a dimension, not a box. The
        # datum thickens with the state, its declared weight ramp.
        "button.main": {DEFAULT: "├  ┤", FOCUSED: "╞  ╡", ACTIVE: "┣  ┫",
                        DISABLED: "╎  ╎"},
        # A TITLE-BLOCK CELL between two extension lines — nothing is boxed
        # here, and two verticals are a dimension, not a box. The caret is
        # this language's own EDITED knob, the datum tick.
        # INVALID IS THE DATUM AT ERROR WEIGHT (inc39). It read `┤·├`: the
        # dimension's terminators EXCHANGED. On this sheet that turn is
        # ALREADY SPOKEN FOR -- `radio.main` points its terminators IN on
        # purpose, as a callout selecting one item from a schedule -- so a
        # rejected field and a selected option were drawn with the same
        # turn. Un-flipping alone gives `├·┤`, DEFAULT byte for byte, so
        # the terminators take `DANGER_FORM`: the heavy rule, which is this
        # language's own `LEVELS["error"]` and the ladder S5 already reads.
        "textfield.main": {DEFAULT: "├·┤", FOCUSED: "╞·╡", EDITED: "╞╌╡",
                           ACTIVE: "┣·┫", INVALID: "━·━",
                           DISABLED: "╎╌╎"},
        "textfield.caret": {DEFAULT: "╪"},
        # A DIMENSION ON A LONG SHEET, and NOTHING IS FILLED — this sheet's
        # law survives the new component, which is what a language law is
        # for. The unseen length is the leader this drawing rules every gap
        # with; the length in view is the EXTENSION LINE at drawing weight,
        # and its opening terminator is the datum the chrome already fixes.
        "scrollbar.main": {DEFAULT: LEAD, DISABLED: BREAK},
        "scrollbar.indicator": {DEFAULT: "━", DISABLED: "─"},
        # TERMINATORS TURNED INWARD ON A SCHEDULE — the callout this sheet
        # already uses to pick one item out of a list, given the second
        # direction a stepper needs. NOTHING IS FILLED AND NOTHING IS BOXED,
        # the sheet's law, surviving its sixth component: the weight ramp is
        # the whole state channel. Where the schedule ends there is no
        # terminator to draw, only the LEADER this drawing rules every gap
        # with.
        "stepper.main": {DEFAULT: LEAD + LEAD, DISABLED: BREAK + BREAK},
        "stepper.step": {DEFAULT: "┤├", FOCUSED: "╡╞", EDITED: "╪╪",
                         ACTIVE: "┫┣", INVALID: "├┤",
                         DISABLED: "╏╏"},
    }

    def icon(self, kind):
        """HELD is the HATCH itself — the one icon in this vocabulary that is a
        texture rather than a code.

        NO ICON IS EVER ALERT, and that is the ration taken literally rather
        than loosely. An icon is a LABEL: the `overdue` code captions a tile
        whose count may be zero, and a red `OVR` standing beside `0` is the
        hue meaning "this word is about lateness" instead of "this thing is
        late" — measured on the calm board, where it was the only alert cell
        on the frame. Alert is spent on the SPAN of a row that is genuinely
        past its date, and nowhere else at all."""
        if kind == "blocked":
            return f"[{self.c['mut']}]{self.hatch * 2}[/]"
        g = self.ICONS.get(kind, "")
        return f"[{self.c['mut']}]{g}[/]" if g else ""

    def display_cap(self, s: str) -> str:
        return s.upper()                   # drafting letters everything in caps

    def wordmark(self, text):
        """Display type: the sheet's own title, DIMENSIONED."""
        cap = " ".join(text.upper())
        return [f"[{self.c['ink']}]"
                f"{self.dimension(len(cap) + 4, cap)}[/]"]

    # ---- composition -------------------------------------------------------
    def board_layout(self):
        return "sections" if self.fielded else "columns"

    def surface(self):
        """FLAT. A panel behind a card IS a containing box drawn in background
        (HIERARCHY.md ranks a shared ground as a grouping CONTAINER), and this
        language's whole claim is that nothing on the sheet is contained."""
        if not self.fielded:
            return super().surface()
        t = self.t
        return (f".kb-col, .kb-card, .kb-flat {{ background: {t['ground']}; }}\n"
                f".kb-flat, .kb-col {{\n"
                f"    scrollbar-background: {t['ground']};\n"
                f"    scrollbar-color: {t['dim']};\n"
                f"    scrollbar-color-hover: {t['mut']};\n"
                f"    scrollbar-color-active: {t['ink']}; }}")

    def composition(self):
        """THE SHEET, and the title block DOCKED to its bottom corner.

        `#tabs` is the seat the mode strip already had; under this language it
        becomes the title block, which is where an engineering drawing keeps
        its identity. Docking is what puts it in the CORNER instead of above
        the field.

        THE ROW BUDGET, and it is paid rather than borrowed: the block takes
        `TB_ROWS` where the strip took `margin-top: 1` plus one content row, so
        it is one row dearer. `#kb` gives up its own `margin-top` to pay for
        it, and that is not a density wish — `.col-head` already spends a row
        of air ABOVE itself (where it groups features instead of separating a
        head from its items), so `#kb`'s margin would stack a second blank row
        on the first. A separator drawn twice is corgi's argument, and it is
        the same argument here.

        `.kb-card:focus` restores the unfocused padding on purpose: widget.tcss
        shifts it to make room for a focus BORDER, and a language that spends
        no border (`sel="none"`) would otherwise have every selected row jump
        one cell sideways — the exact jiggle a dimensioned sheet exists to
        prevent (the solari precedent).

        Gated on `frame`, not merely written: the dock IS the title block's
        seat, so a language whose frame is no longer "titleblock" must give the
        generic composition back byte for byte — otherwise the token would be
        half dead metadata, live in the render and dead in the layout.
        """
        if not self.titled:
            return super().composition()
        t = self.t
        return f"""
        #tabs {{ dock: bottom; height: {self.TB_ROWS}; margin-top: 0; }}
        #kb {{ margin-top: 0; }}
        .col-head {{ margin-top: 1; margin-bottom: 0; }}
        .kb-card:focus {{ background: {t['focus']}; padding: 0 1; }}
        .tile:focus {{ padding: 0 1; }}
        """


# ---------------------------------------------------------------------------
# QUANTITY MECHANISMS — dispatched on the `meter` token. Each is a different
# STRUCTURE (discrete dots on a lattice / LCD ghost segments / sub-cell braille
# / one hairline / bracketed box / CRT decay ramp / gradient shoulder /
# conventional blocks), not one bar with different glyph pairs.
# ---------------------------------------------------------------------------
def _pct_n(done, total, bar_w):
    pct = 0 if not total else round(100 * done / total)
    n = 0 if not total else max(0, min(bar_w, round(bar_w * done / total)))
    return pct, n


def _meter_ember(k, done, total, counts, w):
    """PRISM'S QUANTITY: a field that is CONSUMED, with a boundary that moves
    at HALF-CELL precision.

    Every other meter in this registry says an amount by how much of a track
    is *filled*. This one says it by how much of a solid field is *gone* —
    the burnt part is `ash`, the part still alight is the accent, and the
    frontier between them is what carries the datum. That is not a stylistic
    inversion: it is why the mechanism needs braille and a dot bitmap at all.

    Two dot-columns per cell means the boundary can land INSIDE a cell, so a
    reading of 47 % on a 20-cell bar is not rounded to the tenth cell — it is
    drawn at the left half of the tenth. A block meter cannot do that; it
    quantises the frontier to whole cells, which on a 20-cell bar is a 5 %
    step. The half-cell is the resolution the language spends its pixel base
    on ([DENSITY.md] — the base must match the axis that varies).

    `taskboard/wave.py` on main is the engine, ported here unchanged; its own
    REV1 lit whole braille ROWS and was rejected for exactly this reason.
    """
    from taskboard import wave as WV
    c = k.c
    bar_w = max(4, w - 10)
    pct, _ = _pct_n(done, total, bar_w)

    dots_w = bar_w * WV.DOT_COLS
    burnt = 0 if not total else max(0, min(dots_w, round(dots_w * done / total)))

    # ASH IS NOT A SOLID FIELD, AND THAT IS LAW 1, NOT A PREFERENCE.  The first
    # version filled both sides to full height and let the TONE carry the
    # frontier -- so with colour stripped the bar did not move at all, and the
    # harness said `moved=False`.  It is the same defect the Kimi fork's
    # grey-on-grey meter died of.  Burnt cells keep only their bottom dot row:
    # the boundary is a change of SHAPE (solid field -> a residue), and the
    # colour is confirmation rather than the datum.
    ASH_ROWS = 1
    live, ash = WV.Bitmap(dots_w, WV.DOT_ROWS), WV.Bitmap(dots_w, WV.DOT_ROWS)
    for x in range(dots_w):
        if x < burnt:
            ash.fill_to(x, ASH_ROWS)
        else:
            live.fill_to(x, WV.DOT_ROWS)

    lit = live.to_braille()[0]
    spent = ash.to_braille()[0]
    ash_c = k.t.get("ash", c["dim"])
    # one cell is field or figure, never both -- so a cell straddling the
    # frontier is emitted ONCE, in the tier that owns its lit dots
    bar = "".join(
        f"[{ash_c}]{spent[i]}[/]" if spent[i] != " " else
        (f"[{c['accent']}]{lit[i]}[/]" if lit[i] != " " else " ")
        for i in range(bar_w))
    return f"{bar} [{c['mut']}]{pct:>3}%[/]"


def _meter_blocks(k, done, total, counts, w):
    """THE TERMINAL'S OWN PROGRESS BAR (inc47), and the figure leads it.

    This drew `▇`*n + `░`*(bar_w-n) -- twenty-seven near-solid block cells in
    the detail pane -- and `Nord.__doc__` carries the measurement that makes
    that a defect rather than a preference: "colour-stripped at 118x30 nord
    had NO first fixation ... the only isolated element, the hero numeral,
    came FIFTH behind the LOAD PLOT standing beside it in the same panel."
    The split (`layout="split"`) is this language's ONE commitment and it
    exists to give the eye one subject; `nord_S1` reproduced the same failure
    one layout later, with the plot beating the declared subject in the pane
    the split had just created.

    THE FIX IS HERE AND NOT IN A KIT, and that is the whole reason it is
    tractable. Nord declares nothing -- the other ten override `meter` with
    their own token (`dotgrid`, `lcd`, `braille`, `hairline`, `boxed`,
    `step`, `ember`, `tally`, `odometer`, `dimension`) and `blocks` is the
    base's, so this function draws for exactly one language. Proved by frame
    diff rather than by reading: of the 66, exactly ONE moved and it is
    `nord_S1`. (`Nord.detail_rows` draws a SECOND bar inline, which is the one
    the docstring above measured; it moved with this one, and `board_nord` in
    the gallery carries both.)

    WHAT REPLACES IT IS NOT AN INVENTION. Rich -- the library this app is
    built on -- draws its own progress bar with `━`, so a terminal that has a
    bar has that one. The complete run is the heavy rule and the remainder is
    the light one: two SHAPES, so it survives greyscale, and about a seventh
    of the ink COVERAGE, so it stops out-weighing a line of text. The figure
    moves to the FRONT because DATAVIZ law 1 is that a gauge STATES its
    value, and because the first cell of the row is the one the eye reaches
    first -- which is the quantity the docstring measured.

    BLOCK-ELEMENT CELLS IN `nord_S1`: 27 -> 0."""
    c = k.c
    bar_w = max(4, w - 10)
    pct, n = _pct_n(done, total, bar_w)
    bar = "━" * n + "─" * (bar_w - n)
    return (f"[{c['mut']}]{pct:>3}%[/] [{c['accent']}]{bar}[/]\n"
            f"[{c['dim']}]{_pulse(counts, bar_w)}[/] [{c['dim']}]flow[/]")


def _meter_dotgrid(k, done, total, counts, w):
    c = k.c
    dot_w = int(k.t.get("dot_w", 2))
    g = int(k.t.get("gap", 1))
    avail = max(8, w - 8)
    cells = max(4, avail // max(1, dot_w + g))
    pct, _ = _pct_n(done, total, 1)
    return (NA.dot_meter(done, total, cells, c["ink"], c["dim"], gap=g)
            + f" [{c['mut']}]{pct:>3}%[/]\n"
            + NA.dot_heat(counts, max(2, (avail - 6) // max(1, 1 + g)),
                          c["ink"], c["mut"], c["dim"], gap=g)
            + f" [{c['dim']}]flow[/]")


def _meter_lcd(k, done, total, counts, w):
    # LCD ghost segments: unlit segments render faint, never disappear — AND
    # THEY DIFFER FROM THE LIT ONES IN SHAPE. They did not: both were `▄▄` in
    # two tones, which is the case DATAVIZ law 1 cites BY NAME, and colour
    # stripped it made the bar `▄▄ ` * segs at EVERY value — a quantity row
    # carrying no reading at all without colour, for as long as this
    # mechanism has existed.
    #
    # The pair is the `lcd` ramp's own unlit and its first lit level, and the
    # meter asks `cover_ramp()` for it — THE ONE SEAT that answers "which
    # ramp is this language's" (#45). Naming the registry ROW was pass 62's
    # convention and it was one answer too many: a mechanism reached through
    # the `meter` token asking a second question keyed on the same token is
    # two seats for one fact. It still does not ROUTE: a segment is lit or it
    # is not, and a boolean is not a coverage.
    c = k.c
    ramp = k.cover_ramp()
    ghost_g, seg_g = ramp[0], ramp[1]
    screen = k.t.get("screen", c["accent"])
    alu = k.t.get("alu", c["mut"])
    segs = max(4, (w - 12) // 3)
    pct, n = _pct_n(done, total, segs)
    lit = f"[{screen}]" + f"{seg_g * 2} " * n + "[/]"
    ghost = f"[{c['dim']}]" + f"{ghost_g * 2} " * (segs - n) + "[/]"
    flow = " ".join(
        f"[{alu}]\\[{i + 1}][/][{screen if x else c['dim']}]{x}[/]"
        for i, x in enumerate(counts))
    return lit + ghost + f"[{c['mut']}]\\[{pct:>3}%][/]\n" + flow


def _meter_braille(k, done, total, counts, w):
    # 2 dot-columns per cell -> half-cell precision; unlit lattice visible
    c = k.c
    ramp = k.cover_ramp()
    cells = max(4, w - 10)
    pct, _ = _pct_n(done, total, 1)
    dots = 0 if not total else max(0, min(cells * 2,
                                          round(cells * 2 * done / total)))
    full, half = divmod(dots, 2)
    # THE BAR'S UNLIT IS `⠒` (dots 2+5) AND THE FLOW ROW'S IS THE REGISTRY'S
    # (dot 5) — two unlit glyphs one row apart, which looks like the #45
    # disease one level down and is NOT. DECLARED: one unlit idiom at TWO
    # RESOLUTIONS. The bar is a HALF-CELL fill (`⣿` fills both sub-columns of
    # a cell, the half cell only the left), so it addresses two sub-columns
    # per cell and a track that inks one of them leaves the other drawing
    # nothing at the very scale the bar can fill — which is what #46 was, one
    # cell wide, and is cured below. The flow row draws one bucket per cell with
    # no sub-division, so ONE dot is its empty. Checkable rather than
    # rhetorical, and asserted: the bar's unlit IS the flow row's unlit
    # MIRRORED into the other sub-column — dot 5 | its mirror dot 2 == dots
    # 2+5. Both clear law 4's two ceilings (0.250 and 0.125 ink, against a
    # quarter-cell limit).
    #
    # THE GLYPH IS SPELLED BY NUMBER HERE ON PURPOSE. Pass 64's law says this
    # function's source no longer spells the registry's unlit; writing the
    # ARGUMENT for it in a comment would have reddened that law, and the fix
    # for a red is never to narrow the law that found it.
    #
    # WHAT THE SAME ARGUMENT SAYS ABOUT THE HALF CELL (#46, cured here). The
    # half cell's right sub-column is UNRUN, so by the rule above it is track
    # and must carry the track's dot; the glyph that used to sit here carried
    # zero, which made the one cell where the run ends the one cell whose
    # empty sub-column drew nothing. The cured glyph is not CHOSEN, it is
    # COMPOSED out of the two glyphs this mechanism already has — the full
    # cell's left sub-column OR the track's right sub-column — which is why
    # it is spelled by number in the law and not by taste here.
    #
    # ITS TONE IS THE RUN'S, and that is a decision rather than an accident.
    # A cell is one glyph and carries one tone, so the sub-cell resolution
    # the FILL has, the TONE does not: whichever span the half cell joins,
    # one of its two sub-columns is painted in the other's colour. It joins
    # the LIT run, because the lit sub-column is the DATUM and the track dot
    # is chrome, and a fill that under-reads its own quantity by half a cell
    # to keep chrome the right colour has the priority backwards.
    bar = (f"[{c['accent']}]{'⣿' * full}{'⡗' * half}[/]"
           f"[{c['dim']}]{'⠒' * (cells - full - half)}[/]")
    hi = max(counts) if counts else 1
    # THE TWO ENDS OF THIS ROW ARE THE REGISTRY ROW'S TWO ENDS, AND THE
    # COUPLING RAN BACKWARDS: pass 61 chose the braille row's unlit by
    # looking at THIS meter and recorded the fact in a comment, so two
    # literals were tied by prose and either side could drift. The registry
    # is the definition and this row READS it (#44) — through `cover_ramp()`,
    # the one seat, rather than by naming the row (#45). The row name is not
    # spelled here at all, comment included: a source law a COMMENT can walk
    # around is not a source law (pass 61's quote-style finding, one shape on).
    #
    # The MIDDLE level stays this row's own: a 3-level flow row on a 4-level
    # coverage ramp is not a copy of it, and `⠶` is a level the registry does
    # not carry. The BAR above is a different mechanism (a half-cell fill on
    # a lattice track) and keeps its own three glyphs.
    flow = "".join(ramp[3] if n > (hi or 1) * 0.66 else ("⠶" if n else ramp[0])
                   for n in counts)
    return (bar + f" [{c['mut']}]{pct:>3}%[/]\n"
            f"[{c['dim']}]{flow}[/] [{c['dim']}]flow[/]")


def _meter_hairline(k, done, total, counts, w):
    # one hairline; NO flow row — swiss spends the row on emptiness
    c = k.c
    bar_w = max(4, w - 10)
    pct, n = _pct_n(done, total, bar_w)
    return (f"[{c['accent']}]{'━' * n}[/][{c['dim']}]{'─' * (bar_w - n)}[/]"
            f" [{c['mut']}]{pct:>3}[/][{c['dim']}]%[/]\n")


def _meter_boxed(k, done, total, counts, w):
    c = k.c
    bar_w = max(4, w - 12)
    pct, n = _pct_n(done, total, bar_w)
    bar = (f"[{c['dim']}]\\[[/][{c['accent']}]{'█' * n}[/]"
           f"[{c['dim']}]{'░' * (bar_w - n)}][/]")
    return (bar + f" [{c['mut']}]{pct:>3}%[/]\n"
            f"[{c['dim']}]{_pulse(counts, bar_w)}[/] [{c['dim']}]flow[/]")


def _meter_decay(k, done, total, counts, w):
    # CRT persistence: bright at the head, fading behind it
    c = k.c
    ramp = k.cover_ramp()
    bar_w = max(4, w - 10)
    pct, n = _pct_n(done, total, bar_w)
    tail = min(n, 2)
    # THE PERSISTENCE TAIL IS THE PHOSPHOR RAMP, INDEXED BY DISTANCE FROM THE
    # HEAD RATHER THAN BY COVERAGE — so it asks the ONE SEAT for the row (#45;
    # the sixty-first pass's cure gave the two the same four glyphs and the
    # duplicate literal was found by the law that counts them) and it still
    # does not ROUTE, because a position is not a coverage.
    #
    # THE TAIL USED TO REACH THE TRACK'S OWN GLYPH (pass 62's census). It was
    # four cells, so its dimmest was `░` — the very glyph the unrun track
    # draws, separated from it by TONE ALONE, which is DATAVIZ law 1's defect
    # and put a HOLE in the run in greyscale: `▓▓▓░▒▓█`, an ink dip and then
    # a rise. The tail now starts ABOVE the track and the older trace glows
    # one level under it, so the bar is MONOTONE in ink across all three
    # tones: track `░` < trace `▒` < tail `▓█`.
    body = ramp[4 - tail:] if tail else ""
    bar = (f"[{c['mut']}]{ramp[1] * max(0, n - tail)}[/]"
           f"[{c['ink']}]{body}[/]"
           f"[{c['dim']}]{ramp[0] * (bar_w - n)}[/]")
    return (bar + f" [{c['mut']}]{pct:>3}%[/]\n"
            f"[{c['dim']}]{_pulse(counts, bar_w)}[/] [{c['dim']}]flow[/]")


def _meter_gradient(k, done, total, counts, w):
    # THE BAR IS THE PHOSPHOR RAMP READ DOWNWARD: a run of full cells, a
    # shoulder fading out of it, and the ramp's own unlit as the TRACK.
    #
    # The track was literal SPACES — DATAVIZ law 4, the defect pass 61 cured
    # on nine ramps, alive at the mechanism next door: a flat-zero meter
    # rendered as nothing at all. And the shoulder ENDED on the glyph the
    # track now draws, so its last step would have vanished into it; two
    # cells now, because the third step IS the track.
    c = k.c
    ramp = k.cover_ramp()          # the ONE seat, never a second answer
    bar_w = max(4, w - 10)
    pct, n = _pct_n(done, total, bar_w)
    # A FADE OUT OF A RUN OF LENGTH ZERO IS A PHANTOM READING. The shoulder
    # drew `▓▒░` at 0% against a blank track, so the row said "a little" when
    # the datum said "none" — the opposite half of law 4, and the reason the
    # cure for a missing track is not simply "ink the blanks".
    sh = ramp[2:0:-1][: max(0, min(2, bar_w - n))] if n else ""
    bar = (f"[{c['accent']}]{ramp[3] * n}{sh}[/]"
           f"[{c['dim']}]{ramp[0] * max(0, bar_w - n - len(sh))}[/]")
    hi = max(counts) if counts else 1
    # the flow row is the same ramp indexed by relative load. It spelled it
    # BACKWARDS, which is a second definition wearing a disguise the
    # literal-count law cannot see — byte-identical, now named.
    flow = "".join(ramp[min(3, round(3 * x / (hi or 1)))] * 2 for x in counts)
    return (bar + f" [{c['warn']}]{pct:>3}%[/]\n"
            f"[{c['mut']}]{flow}[/] [{c['dim']}]flow[/]")


def _meter_step(k, done, total, counts, w):
    # achromatic: fill vs track differ by SHAPE (█ vs ▁) — the fork's
    # grey-on-grey version vanished in greyscale (DATAVIZ.md law 1)
    c = k.c
    bar_w = max(4, w - 10)
    pct, n = _pct_n(done, total, bar_w)
    bar = f"[{c['mut']}]{'█' * n}[/][{c['dim']}]{'▁' * (bar_w - n)}[/]"
    hi = max(counts) if counts else 1
    # THE FLOW ROW DREW ITS LEVELS AS `. o O` AND THIS ROW'S OWN CAPTION IS
    # THE WORD `flow`. Colour-stripped, `O.oo flow` carries FIVE marks of
    # that ramp for FOUR buckets: a reader scanning the row with the
    # mechanism's own marks reads a PHANTOM level-1 bucket out of the
    # caption — the same family of defect as `gradient`'s phantom shoulder,
    # where a fade out of an empty run said "a little" while the datum said
    # "none". It was the ONE flow row in the twelve whose data alphabet met
    # its own prose, and the space in front of the caption is not a boundary
    # a reader can trust: FIVE of the twelve rows put spaces INSIDE the data
    # run (`dimension`, `dotgrid`, `lcd`, `odometer`, `tally`), so "the run
    # is the first space-free token" is not a rule this family supports.
    #
    # THE COLLISION WAS THE SYMPTOM; the defect under it is that this row
    # had a PRIVATE alphabet at all. `. o O` is darkside's MOTION and
    # IDENTITY family — `SPIN`, the `PHASES` doodle, the port `(o)` — and
    # this language's declared DATA ramp is the step ladder the registry
    # names for it — the row its own `spark` draws, asked for through
    # `cover_ramp()`. The row is data, so it reads the declared row: three
    # levels off a four-level ladder, `[0]` unlit, `[3]` terminal, and the
    # middle band
    # takes the MIDDLE of the cell rather than the step next to the track,
    # because "not empty and not top" should not look nearly empty.
    #
    # The unlit is now the mark the bar one row above already draws for an
    # empty position (pass 61's rule, verbatim), and no level is a LETTER,
    # so no caption this row could ever carry can collide with its data.
    ramp = k.cover_ramp()
    flow = "".join(ramp[3] if x > (hi or 1) * 0.66 else (ramp[2] if x
                                                        else ramp[0])
                   for x in counts)
    return (bar + f" [{c['dim']}]{pct:>3}%[/]\n"
            f"[{c['mut']}]{flow}[/] [{c['dim']}]flow[/]")


def _meter_tally(k, done, total, counts, w):
    # COUNTED, not measured: marks in groups of five, the group break drawn
    # by air. Unlit positions keep a leader dot, so fill and track differ by
    # SHAPE and not by colour (DATAVIZ law 1) — and the leaders are the same
    # mechanism that closes every other gap on the page.
    c = k.c
    mark = k.t.get("tally", "▪")
    lead = "·"
    # five marks + one cell of air per group, and SIX groups is the ceiling:
    # past thirty marks nobody counts, they estimate — and estimating is what
    # a bar is for. A tally that long has stopped being a tally.
    room = max(11, w - 10)
    cells = max(5, min(30, (room // 6) * 5))
    pct, n = _pct_n(done, total, cells)
    body = []
    for i in range(cells):
        if i and i % 5 == 0:
            body.append(" ")
        body.append(f"[{c['ink']}]{mark}[/]" if i < n
                    else f"[{c['dim']}]{lead}[/]")
    # the flow row posts each phase's count as its own tally, between rules
    nb = max(1, min(len(counts) or 1, max(1, (w - 8) // 8)))
    flow = f"[{c['dim']}] │ [/]".join(
        f"[{c['mut']}]{mark * min(5, x)}[/][{c['dim']}]{lead * (5 - min(5, x))}[/]"
        for x in _resample(counts, nb))
    # the figure sits TIGHT against its marks and the rest of the row is
    # margin. Dot leaders exist to bind a name to a DISTANT figure; here the
    # figure is already adjacent, so leaders would be ornament — and filling
    # the gap with the same dot the unlit tally uses would hide where the
    # count ends (measured: the groups of five stopped being readable).
    return ("".join(body) + f" [{c['mut']}]{pct:>3}%[/]\n"
            + flow + f" [{c['dim']}]flow[/]")


def _meter_odometer(k, done, total, counts, w):
    # DIGITS, never bars — the one mechanism in the set that STATES the
    # quantity instead of drawing its length. Every figure is zero-padded to
    # its field's width, so the row never moves sideways as the numbers change
    # (the anti-jiggle law), and greyscale carries the reading for free: a 3
    # and a 7 differ in shape with no colour at all (DATAVIZ law 1).
    c = k.c
    face = k.t.get("flap")
    on_ = f" on {face}" if face else ""

    def od(n, width=3, tone=None):
        s = f"{min(max(0, n), 10 ** width - 1):0{width}d}"
        return "".join(f"[{tone or c['ink']}{on_}]{d}[/]" for d in s)

    pct = 0 if not total else round(100 * done / total)
    first = (f"[{c['mut']}]DONE [/]" + od(done)
             + f"[{c['mut']}] OF [/]" + od(total)
             + f"[{c['mut']}]  [/]" + od(pct) + f"[{c['mut']}]%[/]")
    # the load row posts every phase's count as its own two-cell odometer, the
    # way a board lists the gates it is holding. REFLOWED, never truncated:
    # the last gate must survive a narrow row.
    nb = max(1, min(len(counts) or 1, max(1, (w - 8) // 5)))
    load = f"[{c['dim']}] [/]".join(
        od(x, 2, c["mut"] if x else c["dim"]) for x in _resample(counts, nb))
    return first + "\n" + load + f" [{c['dim']}]LOAD[/]"


def _meter_dimension(k, done, total, counts, w):
    # THE FRAME MEASURES. The run is the quantity and the figure stands ON the
    # run, so the reading never rides on estimating a length — and nothing is
    # ever filled, which is what keeps this mechanism inside a drawing's
    # vocabulary. Written through `_span_text` rather than the kit, so the
    # mechanism belongs to the TOKEN and any theme may adopt it (the dispatch
    # law: a chart wears the language, never a chart library's look).
    c = k.c
    pct = 0 if not total else round(100 * done / total)
    room = max(8, w - 12)
    n = 2 if not total else max(2, min(room, 2 + round((room - 2) * done / total)))
    lab = f"{min(done, 99):02d}/{min(total, 99):02d} {pct:>3}%"
    first = (f"[{c['mut']}]WORK [/][{c['ink']}]{_span_text(n, lab)}[/]")
    # the load row dimensions every phase on ONE shared ceiling, so the phases
    # are comparable to each other and to nothing else (DATAVIZ law 2)
    nb = max(1, min(len(counts) or 1, max(1, (w - 8) // 10)))
    hi = max(counts) if counts else 1
    # `outside=True` is load-bearing here: a span too short to letter would
    # otherwise DROP its figure, and a meter that stops stating its value has
    # stopped being a reading (DATAVIZ.md law 5). The figure steps out; the
    # length still ranks the phases.
    load = " ".join(
        f"[{c['mut'] if x else c['dim']}]"
        f"{_span_text(2 + (0 if not x else max(1, round(6 * x / (hi or 1)))), f'{min(x, 99):02d}')}[/]"
        for x in _resample(counts, nb))
    return first + "\n" + load + f" [{c['dim']}]LOAD[/]"


METERS = {"blocks": _meter_blocks, "dotgrid": _meter_dotgrid,
          "ember": _meter_ember,
          "lcd": _meter_lcd, "braille": _meter_braille,
          "hairline": _meter_hairline, "boxed": _meter_boxed,
          "decay": _meter_decay, "gradient": _meter_gradient,
          "step": _meter_step, "tally": _meter_tally,
          "odometer": _meter_odometer, "dimension": _meter_dimension}


# ===========================================================================
# SURFACE MECHANISMS — the eighth axis, dispatched on the `surface` token
#
# One function per POSTURE, never one per language: naught and instrument
# share `lattice`, corgi and industrial share `display`, ledger and solari
# share `refuse`. What differs between two languages on one posture is
# declared on their kit (`lattice_rows`, `display_chrome`, `exhibit`), which
# is the same split `METERS` uses and for the same reason — a mechanism that
# branched on the kit's NAME would put the commitment back in the renderer.
#
# EVERY MECHANISM RETURNS BOTH SURFACES (AC-3). The pixel transform is
# applied FIRST and the glyph rows are drawn off its result, so the two
# cannot drift: "blueprint tints the pixels" and "blueprint tints the cells"
# are one operation seen twice.
# ===========================================================================


def _plain(s: str, w: int) -> str:
    """A chrome row clipped/padded to exactly `w` cells. Chrome only — never
    called on a half-block row, whose width is exact by construction."""
    return s[:w].ljust(w)


def _surface_untinted(k, img, w, h, label=""):
    """UNTINTED (nord / base16). The one thing the user's colour scheme cannot
    restyle, so it is shown as-is with NO frame — the environment's rules stop
    at the region's edge and the language says so (LANGUAGES.md §6).

    THE IMAGE BOX IS THE WHOLE REGION, and that is this posture's answer
    rather than a missing frame: `chrome` comes back as nothing but holes,
    which is what "there is no chrome" looks like when it is said in the same
    vocabulary every other posture is said in."""
    return RenderResult("untinted", RS.halfblock(img, w, h), img, (w, h),
                        (0, 0, w, h))


def _surface_lattice(k, img, w, h, label=""):
    """LATTICE-IZE (naught, instrument). A photograph would break the one
    thing that makes these languages themselves, so the pixels are quantised
    back onto the language's own dot grid at its `gap` — and the UNLIT grid
    stays visible, which is the commitment that separates an LED panel from
    sparse block type.

    The glyph side is drawn by the kit's own lattice code (naught's full-bleed
    `field`, instrument's braille), so the surface cannot invent a second dot
    vocabulary beside the one the board already draws.

    THE IMAGE BOX IS THE WHOLE REGION. The unlit dots are not chrome around a
    picture, they are the picture's dark half — an LED panel showing black is
    still the panel showing something. Cutting them out as frame would hand a
    compositor a hole with the language's own grid drawn around it, which is
    the one thing this posture exists to refuse."""
    cols, rows = k.lattice_grid(w, h)
    bm = RS.bitmap(img, cols, rows)
    return RenderResult("lattice", k.lattice_rows(bm, w, h)[:h],
                        RS.quantise(img, cols, rows, k.c["ink"], k.c["dim"]),
                        (w, h), (0, 0, w, h))


def _surface_display(k, img, w, h, label=""):
    """DISPLAY REGION (corgi, industrial). Pixels live ONLY inside the
    numbered, boxed display; every control around it stays a label. The bars
    that frame it are where chrome ends and machine output begins — an OP-1
    screen is a raster surface and its aluminium is not.

    The image is tinted to the SCREEN's own two colours before either side is
    drawn: a full-colour photograph inside an LCD is a picture of a different
    device."""
    tl, tr, bl, br, top_g, bot_g, lf, rt = k.display_chrome()[0]
    _, low, high = k.display_chrome()
    pix = RS.duotone(img, low, high)
    iw, ih = max(1, w - 2), max(1, h - 2)
    lab = f" {k.display_label(label=label)} "[:max(0, w - 4)]
    rule = k["accent"] if k.numbered else k.rule_color
    # `mark()` for the label, `len()` for the arithmetic. The label carries a
    # literal `[1]` and this row is markup: escaping changes its CHARACTER
    # count and not its cell count, so the padding is measured on the plain
    # string and the escaped one is what is emitted. Padding an escaped string
    # is how a reserved rectangle silently loses a cell.
    bar_n = max(0, w - 2 - len(lab))
    rows = [f"[{rule}]{tl}{mark(lab)}{top_g * bar_n}{tr}[/]"]
    for line in RS.halfblock(pix, iw, ih):
        rows.append(f"[{rule}]{lf}[/]" + line + f"[{rule}]{rt}[/]")
    rows.append(f"[{rule}]{_plain(bl + bot_g * max(0, w - 2) + br, w)}[/]")
    # the box is the interior the body was drawn into, one cell in from the
    # bars on every side — the same `iw`/`ih` the loop above used, so a frame
    # that moved would move the box with it
    return RenderResult("display", rows[:h], pix, (w, h), (1, 1, iw, ih))


def _surface_tint(k, img, w, h, label=""):
    """TINT + MEASURE (blueprint). Linework at true resolution, cyanotype-
    tinted, WITH DIMENSION SPANS DRAWN OVER IT — the chrome stays the data-viz
    even on pixels, which is the whole reason this language is one of the two
    naturals for an optimiser's field.

    The spans are `_span_text`, the same object the `dimension` meter draws.
    Two implementations of one mechanism is how a language forks its own
    identity (DATAVIZ.md's dispatch law), so there is only ever the one.

    THE LABEL IS A THIRD SPAN, AND WITHOUT IT THIS POSTURE COULD NOT SAY WHAT
    IT WAS MEASURING (L-31). Two spans built from `img.size` state `480px` and
    `160px` — an image's pixel extent, which is a fact about the ENCODER. A
    drawing's dimension is a fact about the THING DRAWN, and on this sheet
    they are different numbers in different units. So a `label` that is given
    is lettered onto its own span above the two: `├─ 60 X 20 CELLS ─┤` over
    `480px` over the glass over `160px` — what the pixels ARE, above what they
    MEASURE. The posture that captions hardest is no longer the one that
    cannot be told what it is captioning.

    It is the CALLER's datum and the LANGUAGE's mark, which is the split that
    made this worth fixing in the kit: emersio-lab drew exactly this row
    itself, correctly, through `dimension()` — and every consumer that draws a
    real figure would have drawn it again. The span is built through
    `_span_text` rather than through `k.dimension()` because a MECHANISM is
    dispatched on a token and may be reached by a kit with no `dimension()`
    method; `dimension()` is a two-line delegation to this same function, so
    the mark is the language's either way and there is still only ever one.

    Lettered in CAPS: this sheet's figures are `03D`, `HELD`, `DONE`, and a
    lowercase callout would be the one piece of typing on the drawing that was
    not drafted. Escaped with `mark()` AFTER the width math, never before."""
    low, high = k.tint_pair()
    pix = RS.duotone(img, low, high)
    iw, ih = max(1, img.size[0]), max(1, img.size[1])
    caption = [_span_text(w, str(label).upper())] if label else []
    span_w = _span_text(w, f"{iw}px")
    span_h = _span_text(w, f"{ih}px")
    body = RS.halfblock(pix, w, max(1, h - 2 - len(caption)))
    rows = ([f"[{k['mut']}]{mark(_plain(s, w))}[/]" for s in caption]
            + [f"[{k['mut']}]{_plain(span_w, w)}[/]"] + body
            + [f"[{k['mut']}]{_plain(span_h, w)}[/]"])
    # the spans are chrome ABOVE and BELOW the glass, never over it: this
    # posture's frame is full-width, so the box is full-width too and only the
    # span rows survive into `chrome`. The caption pushes the glass down one
    # row and shortens it by one — the region is RESERVED, so a third span has
    # to be paid for out of the rectangle rather than added to it.
    return RenderResult("tint", rows[:h], pix, (w, h),
                        (0, 1 + len(caption), w,
                         max(1, h - 2 - len(caption))))


def _surface_refuse(k, img, w, h, label=""):
    """REFUSE (ledger, solari). The posture with no pixels — `pixels` is None
    and that is the commitment being exercised, not a gap in the code.

    Ledger: "a figure is audited, not shown" — at most one small ruled exhibit
    with dot leaders to its caption, a receipt stapled to the page. Solari:
    "one shape, the row; an image cannot flip" — nothing at all.

    Both go through `kit.exhibit()`, because refusing is one posture and what
    a language shows INSTEAD is the language's own business.

    NO IMAGE BOX, AND `None` RATHER THAN AN EMPTY RECTANGLE. There is nowhere
    for glass to go, so `chrome` comes back as `rows` itself — the exhibit and
    the empty page are the whole rendering, with no hole cut in them. A caller
    handed `(0, 0, 0, 0)` here would reserve a degenerate region and composite
    into it; handed `None` it has to decide what refusing means to it, which
    is the decision this posture exists to force."""
    rows = list(k.exhibit(img, w, h, label))[:h]
    rows += [" " * w] * (h - len(rows))
    return RenderResult("refuse", rows, None, (w, h), None)


def _surface_frame(k, img, w, h, label=""):
    """FRAME (neo-brutalist). "A raw image at full strength, hard edge, inside
    a heavy box — no smoothing, no caption softening it."

    So: no tint, no dither, no caption. The pixels are handed on untouched and
    the only thing the posture adds is the box — which is the point, because
    in this language the frame IS the aesthetic rather than an accident.

    NO KIT DECLARES THIS TOKEN. Neo-brutalist is in LANGUAGES.md §7 and has no
    kit in this repo; the mechanism is here because AC-2 requires the posture
    to exist and because a language that adopts it later must not have to
    write it. It is reachable — the mutation test renders every language
    through it."""
    box = "╔╗╚╝══║║"
    tl, tr, bl, br, top_g, bot_g, lf, rt = box
    rows = [f"[{k['ink']}]{_plain(tl + top_g * max(0, w - 2) + tr, w)}[/]"]
    for line in RS.halfblock(img, max(1, w - 2), max(1, h - 2)):
        rows.append(f"[{k['ink']}]{lf}[/]" + line + f"[{k['ink']}]{rt}[/]")
    rows.append(f"[{k['ink']}]{_plain(bl + bot_g * max(0, w - 2) + br, w)}[/]")
    return RenderResult("frame", rows[:h], img, (w, h),
                        (1, 1, max(1, w - 2), max(1, h - 2)))


def _surface_depth(k, img, w, h, label=""):
    """DEPTH STEP (darkside, prism). "A raster region separates from its
    neighbours by ±1 grey step of BACKGROUND, never a border."

    The literal reading, and the only one that is checkable: there is no
    border glyph anywhere in the region. What separates it is an inset of the
    language's next grey rung (`depth_ground()`, read off its own ladder), so
    the region is legible as a distinct plane without a rule being drawn.

    The ambient motion LANGUAGES.md permits here ("the one slow ambient, at
    ~0.25 speed") is NOT implemented: nothing in this batch animates, and a
    still frame is the honest render of a motion nobody plays."""
    g = k.depth_ground()
    pad = f"[on {g}]{' ' * w}[/]"
    body = RS.halfblock(img, max(1, w - 2), max(1, h - 2))
    rows = [pad] + [f"[on {g}] [/]" + line + f"[on {g}] [/]" for line in body]
    rows.append(pad)
    # this posture's chrome is the INSET ITSELF and nothing else — the grey
    # rung around the hole is the whole frame, which is the literal reading of
    # "separates by a step of background, never a border"
    return RenderResult("depth", rows[:h], RS.inset(img, g, 4), (w, h),
                        (1, 1, max(1, w - 2), max(1, h - 2)))


def _surface_figure(k, img, w, h, label=""):
    """EDITORIAL FIGURE (swiss). "One image per screen, hairline rule and a
    caption in plain cells, NEVER FULL-BLEED — the magazine photograph, not
    the poster."

    Never full-bleed is the load-bearing half and it is what the measure
    enforces: the figure is set inside the type grid's gutter, so air stands
    between it and the region's edge, and a reader can see that the image was
    placed on a page rather than used as one. Under it a hairline (the
    language's single rule, from the `frame` token) and a caption in PLAIN
    cells — this language renounces drawn type, so the caption is typed."""
    gut = getattr(k, "GUTTER", 3)
    iw = max(1, w - gut)
    body = RS.halfblock(img, iw, max(1, h - 2))
    pad = " " * (w - iw)
    rows = [line + pad for line in body]
    rule = k.rule_line(iw + 1)
    rows.append((rule or f"[{k.rule_color}]{'─' * iw}[/]") + pad)
    cap = _plain(k.caption(img, label), iw)      # measured plain, emitted safe
    rows.append(f"[{k['mut']}]{mark(cap)}[/]" + pad)
    # the box stops at the gutter, so the air swiss sets the figure in stays in
    # `chrome` as real cells — "never full-bleed" has to survive into the
    # raster path or a compositor would fill the page edge to edge and undo it
    return RenderResult("figure", rows[:h], img, (w, h),
                        (0, 0, iw, max(1, h - 2)))


def _surface_catalogue(posture: str, why: str):
    """AC-7. Phosphor and BBS have postures in LANGUAGES.md and NO kit here.
    They get a registry entry that SAYS SO and refuses, rather than being
    quietly aliased to a posture that happens to look similar — an alias is
    exactly the "dead metadata" failure this axis exists to prevent, and it
    would be undetectable from the outside."""
    def _refuse_catalogue(k, img, w, h, label=""):
        raise NotImplementedError(
            f"surface posture {posture!r} is CATALOGUE-ONLY: {why}. "
            f"No kit in this repo renders it (LANGUAGES.md marks both "
            f"catalogue-only). It is not mapped to another posture on purpose.")
    _refuse_catalogue.__doc__ = f"{posture} — documented, not implemented: {why}"
    return _refuse_catalogue


# THE REGISTRY. Postures, and which languages commit to each:
#
#   lattice    naught, instrument — dither to the language's round-dot grid
#   display    corgi, industrial  — framed screen region, controls stay labels
#   tint       blueprint          — cyanotype + dimension spans over the pixels
#   untinted   nord               — as-is, no frame (the base default)
#   refuse     ledger, solari     — ruled exhibit / nothing at all
#   frame      neo-brutalist      — raw image, hard edge, heavy box. NO KIT
#                                   declares it: LANGUAGES.md §7 has no kit in
#                                   this repo, and the posture is written so a
#                                   language adopting it later inherits it
#   depth      darkside, prism    — ±1 grey step of ground, never a border
#   figure     swiss              — one image, hairline + caption, never bleed
#
# AND TWO THAT ARE DOCUMENTED WITHOUT BEING IMPLEMENTED (AC-7):
#
#   phosphor   one hue, scanlines, bloom on the bright end — a full-colour
#              image is off-language. Catalogue-only: no kit renders phosphor
#              in this repo (retired 2026-07-26 by operator curation).
#   bbs        refuse, or dither to `░▒▓█` — the block gradient IS the shading
#              vocabulary and a true raster is the one thing this language
#              cannot have been drawn with. Catalogue-only, same retirement.
#
# Both raise `NotImplementedError` naming themselves. Mapping either onto
# `tint` or `lattice` would render something plausible and report a posture
# that no code implements, which is the failure mode AC-7 is written against.
SURFACES = {"untinted": _surface_untinted, "lattice": _surface_lattice,
            "display": _surface_display, "tint": _surface_tint,
            "refuse": _surface_refuse, "frame": _surface_frame,
            "depth": _surface_depth, "figure": _surface_figure,
            "phosphor": _surface_catalogue(
                "phosphor", "one hue, scanlines and bloom; a full-colour "
                            "image is off-language"),
            "bbs": _surface_catalogue(
                "bbs", "refuse, or dither to the block gradient ░▒▓█")}

# The postures a mutation test may swap BETWEEN: the implemented ones. The
# two catalogue entries are excluded because refusing is their behaviour —
# swapping into one proves nothing about whether the token is read.
LIVE_SURFACES = ("untinted", "lattice", "display", "tint",
                 "refuse", "frame", "depth", "figure")

# WHO REFUSES THE LABEL, AND ON WHAT COMMITMENT.
#
# `raster_region`'s `label` is documented as "what the figure IS, for the
# postures that caption or audit one". Five postures never read it — and until
# L-31 a posture that had DECIDED not to caption was indistinguishable from one
# that had forgotten to, because both are spelled `label=""` in the signature
# and nothing in the body. `tint` turned out to be the second kind: it captions
# harder than anything else here and could not be told what it was captioning.
#
# So the refusals are declared, and the declaration is what the test checks
# against. An optional argument no implementation reads is a comment; a
# DECLARED refusal is an implementation reading the argument and rejecting it,
# and the difference is that one of them can be wrong out loud.
# RETRACTED 2026-09-04 (kits-learn-2): `"display"` was in this table, excused
# by "the label beside a display belongs to the CONTROL, and the language
# numbers it (`display_label`) rather than letting a caller name it — an OP-1
# screen's legend is the machine's". SCOPE shipped on it and proved that
# commitment HALF WRONG: it is true of the NOTATION and false of the CONTENT.
# The number in `[1] DISPLAY` is a keybinding (§3b: "the numbers ARE the
# keybindings"), and a keybinding is the caller's — so the kit was not keeping
# a mark, it was spending a key. The notation stayed the language's; only the
# legend moved. A declared refusal that can be wrong out loud is the point of
# this table, and this is the table being wrong out loud.
LABEL_REFUSED = {
    "untinted": "the environment's rules stop at the region's edge and this "
                "posture draws no frame at all — there is nowhere to letter",
    "lattice":  "the whole region is the panel and the unlit dots are the "
                "picture's dark half; a caption would be a lit dot that is "
                "not part of the picture",
    "frame":    "\"a raw image at full strength, hard edge, inside a heavy "
                "box — no smoothing, NO CAPTION softening it\"",
    "depth":    "the figure is separated by one grey step and by nothing "
                "else; a caption is chrome, and this posture's whole "
                "commitment is that it draws none",
}

# THE ONE REFUSAL THAT IS A LANGUAGE'S AND NOT A POSTURE'S. `refuse` reads the
# label — ledger letters it on the exhibit's caption — but solari's `exhibit()`
# shows NOTHING, so the label dies inside a posture that generally honours it.
# That is solari's commitment rather than the mechanism's, and it is keyed by
# language for exactly that reason: a table that hid it under "refuse" would be
# reporting ledger's behaviour as solari's.
LABEL_REFUSED_BY_LANGUAGE = {
    "solari": "\"one shape, the row; an image cannot flip\" — there is "
              "nothing on the page to letter, which is the same refusal that "
              "took the pixels",
}


# phosphor and bbs retired 2026-07-26 (user curation); their decay/gradient
# meter mechanisms stay in METERS as library options any theme may adopt
# nord mapped to the bare `Kit` until 2026-07-27: the base class WAS nord, so
# nord was the one language that could not own a composition without changing
# all eight. `Nord(Kit)` overrides nothing but the split, so that inheritance
# is still the truth — it just has a seat now.
# WHO REFUSES A MODAL BORDER, AND ON WHAT COMMITMENT (operator ruling 5,
# 2026-09-04). The `LABEL_REFUSED` pattern, applied to the component where the
# five languages' answers are furthest apart: a dialog.
#
# THIS TABLE IS READ, not printed. `Kit.overlay` consults it before it draws
# anything, and a language named here never gets the box -- it gets
# `overlay_instead`, which is what the language does with the question when it
# may not put a surface in front of the page. So the table is falsifiable in
# BOTH directions, which is the whole point of declaring a refusal rather than
# describing one: delete an entry and that language starts drawing a lid it
# has committed against; add a false one (prism) and the one language whose
# doctrine LICENSES the border stops drawing it. Either way a test goes red.
#
# PRISM IS ABSENT ON PURPOSE. "Depth by one grey step, never borders --
# borders are RESERVED for modals" is the only commitment in the eleven that
# names this component as the exception, so prism draws the box and recedes
# the page behind it by exactly one step of BACKGROUND.
MODAL_BORDER_REFUSED = {
    "corgi": "\"the mode takes over the screen -- no persistent navigation "
             "chrome; its answer to smallness is FEWER THINGS AT ONCE\". A "
             "dialog floating over a board is two modes at once, which is "
             "the thing this language is built against, so a confirm is a "
             "MODE and the board is gone",
    "blueprint": "\"not one element on this sheet is boxed, at any width\" -- "
                 "and the ten marks this language draws contain no vertical "
                 "stroke, so a dialog box is unconstructable twice over. What "
                 "marks the selection is the REGISTRATION PAIR, four corners "
                 "that never join",
    "naught": "\"no frames at all\" is one of this language's four "
              "commitments, so an overlay BOX cannot be built. The separation "
              "is the LATTICE CHARGE: the page drops to unlit and the "
              "question is the only region left lit (operator ruling 4)",
    "ledger": "\"nothing is deleted, everything is balanced\" -- and a ledger "
              "has no surface IN FRONT OF the page. A question is posted on "
              "the sheet like everything else: under a rule, at the foot, "
              "with the page it is about still legible above it",
    # THREE MORE, added by `kits-learn-4` inc32 when the six inheriting
    # languages were asked. Every one of them was already committed against a
    # lid and had been drawing the terminal's since the seat existed.
    "instrument": "\"borders almost absent\" -- this language's whole "
                  "structure device is WHITESPACE and the one mark it draws "
                  "is the dot, so a question is not boxed, it is BANDED: two "
                  "full-width graticule rules with the question between them "
                  "and the page unlit behind",
    "swiss": "\"NO BOXES -- alignment does the dividing\", at any width, and "
             "the language allows itself exactly ONE hairline rule. So the "
             "question is set at the grid's first column under that rule, "
             "which is the masthead's and not a lid's: it runs the full "
             "measure and nothing turns a corner",
    "solari": "\"one shape, the row; an image cannot flip\" -- the commitment "
              "that already took this language's pixels takes its dialog for "
              "the same reason. A board has no surface IN FRONT OF it: a "
              "question is posted the way a cancellation is, as a BAND IN "
              "REVERSE VIDEO at the head of the schedule, with the rows still "
              "legible under it",
}

# WHO REFUSES A PANE RULE, AND ON WHAT COMMITMENT (batch `kits-learn-4`). The
# third table of the same shape, and the same three properties: READ by
# `Kit.pane_split` before it draws anything, falsifiable in BOTH directions
# (delete an entry and that language starts ruling a line it has committed
# against; add a false one and a language that owns a rule stops drawing it),
# and answered by `pane_split_instead` rather than by a blank.
#
# THE TWO REFUSALS ARE NOT THE SAME REFUSAL, which is why a registry and not a
# flag. Blueprint's is ALPHABETIC — the mark does not exist in its ten. Prism's
# is DOCTRINAL — the mark exists and the language has forbidden itself to spend
# it. A language can leave one of these and not the other.
#
# NAUGHT IS ABSENT ON PURPOSE. "No frames at all" is one of its four
# commitments and a lattice column is not a frame, it is the GROUND — the same
# distinction operator ruling 4 already made for its overlay, where the answer
# was the lattice's charge rather than a box.
#
# SWISS, DARKSIDE AND SOLARI JOINED IN `inheritors-2` (inc36). The first two
# were named in this comment as the batch's declared debt, in these words:
# "No boxes — alignment does the dividing" and "depth by ±1 grey step, never
# borders" are the same two commitments this table exists for. Solari was not
# named and had to be decided: its refusal is the third KIND here, neither
# alphabetic nor doctrinal but STRUCTURAL — it has a divider, it is just not
# this one, and it has committed to spending no other.
#
# THREE OF THE FIVE ANSWER WITH AIR AND THAT IS NOT ONE ANSWER. Blueprint's
# air carries a registration pair on its first row, prism's and darkside's is
# a grey STEP of background (which the `.txt` cannot show and the `.svg` can),
# swiss's and solari's is the pad itself. The `.txt` collapses the last three
# to the same three spaces, and that limit is stated here rather than
# discovered: a background is not a cell, the same mark this file already
# carries for the knockout and for every language's match emphasis.
# WHO REFUSES TO NUMBER A READOUT, AND ON WHAT COMMITMENT (L-33, measured on
# emersio-lab 2026-09-04 and quoted verbatim in LANGUAGES.md §3b). The fourth
# table of the shape, and the one whose keys are DERIVABLE: it must name
# exactly the languages whose `numbered` token is set, because a language that
# does not number anything has no numbering to refuse. `Kit.readout_label`
# READS it — a `numbered` language absent from this table numbers its readout,
# which is the branch the table exists to keep empty, and the test that says
# the keys equal the numbered set is what keeps it empty.
#
# THE ONE HONEST LIMIT, stated because the other three tables do not have it:
# this one can only be wrong in ONE direction. Delete an entry and that
# language spends a key on a bar nobody can press (red). Add a false entry for
# a language that numbers nothing and nothing happens, because there was no
# notation there to withhold.
READOUT_NUMBER_REFUSED = {
    "corgi": "\"because the numbering IS the keymap, this language has no "
             "notation for a passive readout. A [5] over a chart nobody can "
             "act on is the decorative numbering §3b defines itself against. "
             "Readouts are LABELLED; controls are NUMBERED\" — and the right "
             "response to wanting a numbered readout is to notice, not to "
             "loosen the tie",
    "ledger": "the folio numbers a POSTING — an entry someone made, that "
              "someone else can trace back. A rate meter is not posted and "
              "cannot be traced, so a number over it would be a reference to "
              "nothing, which is the one thing a ledger may not write",
    "industrial": "\"everything is numbered and labelled\" and the numbers "
                  "are the MODES — the same keymap corgi's are, reached from "
                  "a different product. A plate stamped over a readout "
                  "promises a control that is not there",
}

PANE_SPLIT_REFUSED = {
    "blueprint": "\"not one element on this sheet is boxed, at any width\" — "
                 "and the ten marks this language draws (`─ ━ ├ ┤ ╌ ┌ ┐ └ ┘` "
                 "and the hatch) contain no vertical stroke, so a pane rule "
                 "is unconstructable rather than merely off-style. What a "
                 "drawing office does with two views on one sheet is give "
                 "each its own DATUM, and the air between them is the "
                 "division",
    "swiss": "\"NO BOXES — alignment does the dividing\", and the language "
             "allows itself exactly ONE hairline rule, which the masthead has "
             "already spent. Two panes are two columns of the same grid: the "
             "right one starts at the next column and the emptiness between "
             "them IS the division — the method stated at three cells wide",
    "darkside": "\"depth by ±1 grey step of background, NEVER BORDERS\", and "
                "a pane rule is a border. Prism inherited this doctrine and "
                "the exception written into it (\"borders are RESERVED for "
                "modals\"), so the parent refuses here for the reason the "
                "child does, one generation earlier",
    "solari": "\"the structure device is the cell FACE a character is flipped "
              "onto, so the language SPENDS NO RULE AT ALL and keeps its "
              "strongest divider unspent\" — and \"tabular fields padded to "
              "their widest content\" says what holds two columns apart "
              "instead. A rule between panes would spend the divider this "
              "language is defined by not spending",
    "prism": "\"depth by ±1 grey step of background, never borders\" — the "
             "one language here whose doctrine names the exception ("
             "\"borders are RESERVED for modals\"), which is a licence for "
             "the modal and a prohibition everywhere else. A pane rule is "
             "everywhere else, so the division is a STEP",
}


KITS = {"naught": Naught, "corgi": Corgi, "instrument": Instrument,
        "swiss": Swiss, "industrial": Industrial,
        "nord": Nord, "darkside": Darkside, "prism": Prism, "ledger": Ledger,
        "solari": Solari, "blueprint": Blueprint}


def kit(name: str) -> Kit:
    """The active language's structure kit. Unknown names get the base
    (terminal-conventional) kit rather than raising — lenient like the model."""
    return KITS.get(name, Kit)(name)
