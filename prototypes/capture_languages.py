"""capture_languages.py -- one coherent sweep of the TEN current design languages.

    python prototypes/capture_languages.py

WHY THIS EXISTS.  `prototypes/out/` holds 892 files from 69 passes, and no two
of them agree on anything: `lang_*.txt` and `gal_*.txt` are from 2026-07-26 and
still carry `phosphor` and `bbs`, which were RETIRED that same day by user
curation, while `ledger`/`solari`/`blueprint` were only captured on 07-28 in a
different pass at different widths.  There has never been a capture of the ten
CURRENT languages taken in one sitting, at one size, off one fixture -- which
is the only form in which "same screen, ten languages" is an honest comparison
rather than a scrapbook.

WHAT IT CAPTURES, per language:

  board_<lang>.txt     the board surface -- cards, column heads, meter, rails
  gallery_<lang>.txt   the COMPONENT SHEET (the app's `g` screen): slider, bar,
                       switch, checkbox, radio, button, text field, scroll bar
                       and stepper, each in the states the registry derives
  *.svg                the same frame IN COLOUR, rendered here -- see below

THE `.txt` IS THE ART; THE `.svg` IS A PICTURE OF IT.  Same rule the skill's
gallery keeps: the two laws that matter are laws about CELLS, and the cell grid
is what the `.txt` *is*.  The SVG carries colour because these captures exist to
be CONSULTED, and a language whose whole commitment is "five flat colours on
grey" cannot be consulted in greyscale.  The skill's greyscale test is a test
you RUN on a language, not a format its documentation must be trapped in -- so
the colour lives in the picture and the grid stays authoritative.

WHY THE SVG IS RENDERED HERE INSTEAD OF BY `App.export_screenshot()`.  Textual's
own exporter was tried first and rejected for two measured reasons.  It writes
`@font-face { src: url("https://cdnjs.cloudflare.com/...FiraCode...") }` -- a
network dependency, which means the picture silently changes font offline and
cannot go into a self-contained document at all.  And it emits one `<rect>` per
segment: 679 rects and 313 texts for one board, 108 KB a frame, 2.2 MB for the
twenty.  The renderer below groups horizontal RUNS of identical style, ships a
system monospace stack, and gives every character its own `x` so the grid cannot
drift whatever font the viewer falls back to -- the same defence, and for the
same reason, as the skill's `render_svg.py`.

The component sheet is captured because it is where languages differ most and
the layer that ships unstyled -- COMPONENTS.md calls the settings screen the
canary.  A sweep of ten boards alone would let a language pass on its hero.

THE FIXTURE IS SYNTHETIC AND THAT IS DELIBERATE.  `out/_fixture_late.json`
(16 tasks, projects named "Website Redesign", "Mobile App"...) rather than the
real board at `~/.taskboard/board.json`: these captures are meant to be shared,
and a screenshot of the operator's actual work is not shareable.  `late` was
chosen over `calm` because overdue work exercises each language's SEVERITY
channel, which is exactly the axis a one-hue language (phosphor) had to solve
by brightness and an identity-coloured one (corgi) had to solve by glyph.

SETTLE HERE NOW ASKS THE SAME THREE QUESTIONS THE HARNESS ASKS, AND IT HAD TO.
This paragraph used to say the opposite -- that only condition B (identical
consecutive frames) was implemented, that condition A was "not covered", and
that a reader who saw a blank frame should go run the harness instead.  That
was an honest description of the code and a bad bargain, and
`.fast-dev-flow/03-increments/race-probe.md` is the measurement that closed it:
over **30 fresh-interpreter sweeps** of this file, **6 of the 22 frames drifted**
and **two independent sweeps disagreed 58.9 % of the time** -- which is the
number the operator sees, because `main()`'s determinism check compares one
sweep against one control sweep.  A capture that is a coin flip is not a
capture.

The probe's §5 says WHICH cells moved, and the answer is why B alone could
never have been enough: a widget waiting on a deferred re-render produces a
genuinely static frame WHILE IT WAITS, so B is satisfied by the very state it
exists to exclude.  Three families showed up -- the **hero band** composed at a
seat it no longer had (the load bar 46 cells wide where the settled frame draws
37, the value and caption not yet landed), the DOING column's **stale card
bake** (`TaskCard.render_card` falling back to an 18-cell row before its first
layout), and solari's **unpainted** split-flap label.

So `settle()` below implements A, B and C, with A widened by one seat:

  A  every content widget the compositor SAYS it is drawing carries ink inside
     its own clipped area -- the four classes `KanbanBoard.build()` mounts,
     PLUS `#hero`.  The hero is not a `BOARD_CONTENT` widget, which is exactly
     how a frame could pass the harness's own A and still be wrong here.
  B  eight identical composited reads, not three (measured: 3 -> 8 alone takes
     the drift from 6 frames to 2, and both survivors were card bakes).
  C  no `TaskCard` THE COMPOSITOR IS DRAWING holds a paint composed at a seat
     it no longer has, asked as a SHADOW render with `update` intercepted so
     the check measures the app and never repairs it.  "Drawing" is load-
     bearing: the DOM is wider than the frame and asking every card in the
     tree made the sweep fail loud on a good screen -- see `_not_at_rest`.

A+B+C measured **0 of 22 frames drifting and 0.0 % pairwise** over 30 sweeps.
The cost is stated rather than buried, both halves of it: a sweep goes from
~7.9 s to ~11.7 s, and **3 of those 30 sweeps FAILED LOUD instead of finishing**
-- always on the columns branch, always four DOING-column cards holding a paint
composed at a narrower seat, and measured to be PERMANENT (still stale 640
iterations / 19.5 s later).  That frame is one the old condition used to write.
Refusing it is the change working; the wedge itself is F-1's remainder and it
lives in `kanban.py`.
`verify_language.py`'s settle is still the fuller instrument and still cannot
be imported (no `if __name__ == "__main__"` guard, so importing it runs all
9923 checks); `_stale_paint` below is lifted from it verbatim in behaviour
rather than shared, and that duplication is the price of the missing guard.
A capture that never stabilises still FAILS LOUD, and now names the widgets
that never came to rest.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

# ANIMATIONS OFF, SET BEFORE TEXTUAL IS IMPORTED.  Measured, not assumed: with
# animations on, `solari` came back with 36.3 % ink on one run and 36.1 % on the
# next, and the diff was a single row -- `DAYS OVERDUE` present in one capture
# and blank in the other.  Solari is a split-flap board, so its label was caught
# mid-flip, and two consecutive identical frames is not proof of rest when an
# animation has a still moment between steps.  `TEXTUAL_ANIMATIONS=none`
# degrades every animation to its FINAL frame with no loss of information
# (RUN.md), which is the frame a capture is supposed to hold.  The determinism
# check at the bottom of this file is what keeps that claim honest.
#
# AND IT DID NOT CURE THE STALL.  This comment used to stop at the line above,
# which reads as if the setting settled the matter.  It did not, and the check
# that was supposed to keep the claim honest is what said so: `board_solari.txt`
# drifted intermittently on the SAME row this note is about (`DAYS OVERDUE`),
# and `gallery_blueprint.txt` on a switch caught at `▅▅` vs `▁▁`.  Both were
# observed on control sweeps with every `surface` token popped, so neither was
# caused by the batch that recorded them.  That was F-1, and it made this sweep
# exit red about one run in three.
#
# F-1 IS CLOSED BY `settle()`, NOT BY THIS LINE -- which is the point worth
# keeping.  The setting is still correct and still worth having; it was simply
# never sufficient, because turning animations off cannot make a widget that is
# waiting on a deferred re-render look any different from a widget at rest.
# Only the widget tree can answer that, which is what conditions A and C ask.
# Numbers: `.fast-dev-flow/03-increments/race-probe.md`.
os.environ["TEXTUAL_ANIMATIONS"] = "none"

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes" / "widget_slice"))

import taskboard.themes as TH                                    # noqa: E402

FIXTURE = ROOT / "prototypes" / "out" / "_fixture_late.json"
OUT = ROOT / "prototypes" / "gallery"
SIZE = (118, 34)

MAX_SETTLE = 40          # frames to wait for the screen to come to rest
# EIGHT, AND THE 3 IT REPLACES WAS MEASURED WRONG RATHER THAN ARGUED WRONG.
# 30 cross-process sweeps per arm (race-probe.md §6): at 3 reads, 4 of 22 frames
# drift and two sweeps disagree 58.9 % of the time; at 8 reads, 2 of 22 and
# 13.1 %; at 8 reads plus condition C, 0 and 0.0 %.  Raising the count alone
# leaves exactly the two frames condition C exists to catch, which is why both
# levers are here and neither is here alone.
STABLE_READS = 8         # identical consecutive frames required

# THE CLOCK IS FROZEN, AND IT HAS TO BE.  A fixture pins the DATA; it does not
# pin the present.  The app reads `datetime.now()` in the signal engine, in the
# aperture and in the prototype's own due-date maths, so "days remaining", the
# load plot and the day-progress bar are all functions of the current instant --
# which made the captures differ between two runs minutes apart, in six of the
# ten languages.  The first version of this file checked determinism by sweeping
# twice INSIDE ONE PROCESS, and that check passed while cross-process capture
# drifted, because both sweeps in a process see nearly the same clock: a
# determinism check whose two samples share the confound cannot see it.
#
# The instant below is a CONSTANT, not "today".  If it were today's date, a
# rebuild next week would legitimately produce different art and the captures
# could never be reproduced -- the point of pinning it is that this script,
# this fixture and this constant always yield the same twenty grids.
FROZEN = "2026-08-03T09:00:00"

# AND THE FIXTURE'S OWN TIMESTAMP, WHICH IS THE OTHER HALF OF THAT SUBTRACTION.
# `taskboard/engine.py:sig_board_file` ages the board file with
# `(time.time() - p.stat().st_mtime) / 60`.  FROZEN pins the first term; the
# CHECKOUT pins the second, and git does not carry mtimes -- so the signal reads
# whatever minute the fixture happened to land on this disk.  The committed
# frames were taken at `f -98`; this tree renders `f -46982`, deterministically,
# in every run, because the file was checked out again.  A capture that is a
# function of a timestamp git does not carry cannot be reproduced by anyone who
# clones the repo, which defeats the whole `.txt`-is-the-art contract.
#
# 450 SECONDS, AND NOT 420.  `int(age_min)` is what reaches the frame, so a pin
# landing exactly on a minute boundary can be flipped to the minute below by the
# sub-microsecond error of a float timestamp round-tripping through the
# filesystem's own resolution.  Seven and a HALF minutes renders `7` from either
# side of that error.
FIXTURE_AGE_S = 450


def freeze_clock() -> None:
    """Pin `datetime.now()` / `date.today()` to FROZEN, everywhere it is read.

    Done by rebinding the NAME in each already-imported taskboard/prototype
    module rather than by touching the app: the capture must photograph the
    shipping code, not a variant of it.  `datetime` is a C type and cannot be
    monkeypatched in place, so a subclass is bound over the module-level name
    that each module imported -- which is exactly the name its own calls
    resolve.
    """
    import datetime as _dt
    fixed = _dt.datetime.fromisoformat(FROZEN)

    class _DateTime(_dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed if tz is None else fixed.replace(tzinfo=_dt.timezone.utc)

        @classmethod
        def today(cls):
            return fixed

        @classmethod
        def utcnow(cls):
            return fixed

    class _Date(_dt.date):
        @classmethod
        def today(cls):
            return fixed.date()

    hit = 0
    for name, mod in list(sys.modules.items()):
        if not (name.startswith("taskboard") or name in ("app", "kanban",
                                                         "views_widget",
                                                         "render")):
            continue
        if getattr(mod, "datetime", None) is _dt.datetime:
            mod.datetime = _DateTime
            hit += 1
        if getattr(mod, "date", None) is _dt.date:
            mod.date = _Date
            hit += 1
    if not hit:
        raise RuntimeError("freeze_clock patched nothing -- import order changed")

    # `time.time()` too: the signal engine ages the board file with it.  The
    # shim DELEGATES everything else -- the first attempt replaced the module
    # outright and the app died on `time.monotonic()`, which the engine uses to
    # decide which signals are due.  Freezing a clock must not take the rest of
    # the module with it.
    import time as _time
    import taskboard.engine as _eng

    class _Time:
        def __getattr__(self, k):
            return getattr(_time, k)

        @staticmethod
        def time():
            return fixed.timestamp()

    if getattr(_eng, "time", None) is _time:
        _eng.time = _Time()

    # AND THE SIGNAL THAT READS THE OPERATOR'S REAL BOARD.  `sig_board_file`
    # calls `default_board_path()` directly -- not the app's `board_path` -- so
    # it stats ~/.taskboard/board.json however the app was constructed.  Two
    # separate problems in one line: the capture is not reproducible (its
    # "minutes since save" moves, and on one run that made the signal win the
    # hero and rewrote ledger's whole top band), and a published frame could
    # print the size and save-time of the operator's actual work.  Point it at
    # the fixture, which is what every other reader of this capture already
    # sees.  (Checked: no published frame ever carried it -- the signal had not
    # won a hero in any capture that shipped.)
    import taskboard.models as _models
    _models.default_board_path = lambda: FIXTURE
    if getattr(_eng, "default_board_path", None) is not None:
        _eng.default_board_path = lambda: FIXTURE

    # AND THE FIXTURE'S MTIME, PINNED BY SETTING IT RATHER THAN BY DERIVING
    # THE SIGNAL FROM CONTENT.  Both cures were on the table.  Deriving
    # "minutes since save" from the file's bytes would make `sig_board_file`
    # a different signal wearing the same label -- it watches for edits made
    # OUTSIDE this process, and a content hash cannot say when one happened.
    # This function's own contract is the other way round: it pins the
    # capture's INPUTS (the present, the board path) and photographs the
    # shipping code unaltered.  A file's timestamp is an input like the clock
    # is, so it is pinned here, where every other input already is, and
    # `sig_board_file` is left exactly as it ships.
    #
    # What this buys: `age_min` becomes FIXTURE_AGE_S / 60 on every machine,
    # so the committed frames reproduce on a fresh clone.  What it costs: the
    # capture WRITES metadata (not content) to the fixture.  That is the same
    # file this function already repoints every reader at, it is idempotent,
    # and git carries neither the before nor the after.
    _t = fixed.timestamp() - FIXTURE_AGE_S
    os.utime(FIXTURE, (_t, _t))
    return hit


def screen_text(app) -> list[str]:
    """The composited frame as rows of cells -- the same reader the harness
    uses (`verify_language.py:286`), because the cell grid is what the laws
    measure."""
    return ["".join(s.text for s in strip)
            for strip in app.screen._compositor.render_strips()]


#: The classes `KanbanBoard.build()` attaches to the content it mounts, quoted
#: from `verify_language.py:319` rather than re-derived, because the renderer
#: writes these strings and a second list would drift from it silently.
BOARD_CONTENT = ("kb-card", "col-head", "kb-empty", "kb-detail")

#: AND THE ONE SEAT THE HARNESS'S OWN LIST DOES NOT COVER.  The hero is not a
#: `BOARD_CONTENT` widget -- it is `Hero(id="hero")`, mounted beside the board,
#: not inside it -- so neither the harness's condition A nor its condition C
#: has ever watched it.  race-probe.md §5 is the bill for that: the frame that
#: drifted most on darkside differed ONLY in rows 3-12, the hero band, with the
#: load bar composed 46 cells wide where the settled frame draws 37 and the
#: value and caption not yet landed.  A capture must wait for it like any other
#: content, so it is named here and condition A reads both.
HERO_ID = "hero"


def _not_at_rest(app, rows: list[str]) -> list[str]:
    """CONDITIONS A AND C, asked ONLY of the widgets the compositor DRAWS.

    Returns names, not a boolean, so a timeout can point at the widget instead
    of at "the board" -- the same reason `verify_language.py`'s settle collects
    a `stuck` list rather than short-circuiting on the first one.

    `visible_widgets` is what makes A sound, and the naive alternative was
    tried and is wrong: a widget's `region` is in SCREEN space and keeps
    growing past the fold, so a raw region slice reads whatever is at those
    coordinates (for a card at y=29, the Footer -- whose text scores as
    "painted").  The compositor's map holds only the widgets it actually
    draws, each with its clip, so anything scrolled away drops out of the
    question instead of answering it wrongly.

    **AND THE SAME MAP IS WHY CONDITION C IS ASKED HERE AND NOT OVER
    `app.query(TaskCard)`.**  The first version of this file asked every card
    in the tree, and that made the sweep FAIL LOUD on a perfectly good screen
    in 3 of 30 cross-process runs (all three on the COLUMNS branch --
    `board naught`, `board instrument` x2 -- with four cards reported stale at
    one uniform seat and never coming right inside `MAX_SETTLE`).  The tree is
    wider than the frame: measured on this fixture, 3 to 9 of the 15 cards are
    in the DOM but not drawn in every one of the eleven languages, at seats
    that belong to a layout that is no longer on screen (50, 55, 107, 111).
    `KanbanBoard.build()` says why in its own comment -- `remove_children()`
    is ASYNCHRONOUS, so for a beat the board holds the previous build's
    widgets too, and a columns-to-columns theme switch leaves them at a seat
    close to but not equal to the new one.  A card the compositor is not
    drawing contributes no cells, so it cannot make the capture wrong, and
    refusing to settle on it is a false positive by construction.

    Where a screen mounts none of these -- the `--surface` sheets, which are a
    bare `Static` -- the list is empty, A and C are vacuously true and B
    settles the frame by itself.  One condition, no special case.
    """
    from textual.widgets import Static
    from kanban import TaskCard
    drawn = app.screen._compositor.visible_widgets
    h = len(rows)
    waiting: list[str] = []
    for w in app.query(Static):
        if not (w.id == HERO_ID
                or any(w.has_class(c) for c in BOARD_CONTENT)):
            continue
        box = drawn.get(w)
        if box is None:
            continue                      # clipped away: evidence of nothing
        area = box[0].intersection(box[1])
        if not (area.width and area.height):
            continue
        name = f"{w.id or '.'.join(sorted(w.classes))}@{area.x},{area.y}"
        if not any(rows[y][area.x: area.x + area.width].strip()
                   for y in range(area.y, min(area.y + area.height, h))):
            waiting.append(f"{name} {area.width}x{area.height} BLANK")
        elif isinstance(w, TaskCard) and _stale_paint(w):
            waiting.append(f"{name} STALE PAINT (composed at a seat it no "
                           f"longer has; seat is now {w.size.width})")
    return waiting


def _stale_paint(card) -> bool:
    """CONDITION C: was this card's paint composed at a seat it no longer has?

    Lifted verbatim in behaviour from `verify_language.py:322`, which cannot be
    imported (that file has no `if __name__ == "__main__"` guard, so importing
    it runs all 9923 checks).  Ask the card what it would draw RIGHT NOW and
    compare it to what it is already showing, with `update` intercepted so the
    answer is collected and never applied: this REPORTS, it does not repair.
    A settle that silently re-rendered the board would mask the exact class of
    bug it exists to catch.
    """
    got: list = []
    card.update = got.append
    try:
        card.render_card()
    finally:
        del card.update            # drop the shim, restore the class method
    return bool(got) and got[0] != card.content


async def settle(pilot, app, label: str) -> list[str]:
    """Wait for a frame the app has actually finished composing.

    Three conditions, all of which must hold on the SAME read:

      A  every content widget the compositor says it is drawing carries ink
         inside its own clipped area -- the four classes `build()` mounts and
         `#hero`
      B  `STABLE_READS` identical composited frames
      C  no DRAWN `TaskCard` holds a paint composed at a seat it no longer has

    A and C are one pass over the compositor's own map (`_not_at_rest`); B is
    the read counter below.

    **B ALONE WAS THE DEFECT, AND B ALONE CANNOT BE FIXED BY WAITING LONGER.**
    This docstring used to argue that condition A was deliberately not
    reimplemented here, that a naive region slice gave false positives, and
    that the cross-process check in `main()` would catch anything that slipped
    through.  The first two were true of the naive version; the third was the
    mistake.  `main()` DID catch it -- it caught it 58.9 % of the time
    (`.fast-dev-flow/03-increments/race-probe.md` §4b, 30 fresh-interpreter
    sweeps) -- and a check that fails on more than half of all runs is not a
    guard, it is a coin flip that has to be re-run until it agrees.

    The reason B is not merely SHORT is worth stating, because it is the whole
    mechanism: a widget waiting on a deferred re-render produces a genuinely
    static frame while it waits.  `TaskCard.on_mount` defers its paint with
    `call_after_refresh`; `Hero.show` is driven by a worker; the split branch
    fills its detail pane from `_seed_detail`, also deferred.  Every one of
    those makes "mounted" and "drawn" different moments in which nothing
    changes between reads.  No number of identical reads can distinguish that
    state from rest -- only asking the widget tree can, which is A and C.

    The false-positive worry that kept A out is answered by
    `visible_widgets` -- see `_not_at_rest`, which uses the compositor's own
    clip rather than the widget's screen-space region, and which is also why
    C is asked about the cards on screen rather than every card in the tree.
    Validated on the only evidence that can settle it: 30 cross-process sweeps
    of all 22 frames, **0 drifting, 0.0 % pairwise** (was 6 and 58.9 %).

    **AND IT NOW FAILS LOUD ON A FRAME THE OLD SETTLE USED TO WRITE.**  Three
    of those 30 sweeps did not finish: `board instrument`, `board industrial`
    and `board naught` -- the COLUMNS branch -- raised the timeout below with
    four DOING-column cards holding a paint composed at a narrower seat.  That
    is not this function being impatient, and it was measured rather than
    assumed: kept running for **640 iterations / 19.5 s** past the bound, the
    same four cards still read `Design home...` where their present seat draws
    `Design homepage moc...`.  The app WEDGES, and nothing corrects it.  The
    old condition WROTE that frame, and it is the drift race-probe.md §5 named
    for exactly these three languages, character for character.  A sweep that
    stops rather than shipping it is the whole point of the change -- but the
    ~10 % loud failure is F-1's remainder, it lives in `kanban.py` and not
    here, and a caller who sees this timeout on a columns language is looking
    at that defect rather than at a slow machine.
    """
    stable = 0
    prev: list[str] | None = None
    waiting: list[str] = []
    for _ in range(MAX_SETTLE):
        await pilot.pause()
        rows = screen_text(app)
        stable = stable + 1 if rows == prev else 0
        prev = rows
        if stable < STABLE_READS - 1:
            continue
        if not any(r.strip() for r in rows):
            raise RuntimeError(f"{label}: frame settled BLANK")
        # A and C are asked only once B is otherwise satisfied: they cost a
        # widget walk and a shadow render per drawn card, and a frame that is
        # still changing is going to be re-read anyway.
        waiting = _not_at_rest(app, rows)
        if waiting:
            # NOT a settled frame, however still it looks -- keep waiting.
            #
            # AND `stable` IS NOT RESET HERE, WHICH WAS MEASURED RATHER THAN
            # REASONED.  The first version of this did reset it, on the theory
            # that the frame must be stable AFTER the last widget comes to
            # rest.  It is -- but the run of identical reads already delivers
            # that for free, because a widget that finishes painting CHANGES
            # the composited frame and `stable` drops to 0 on the next read by
            # itself.  Resetting as well only spends the MAX_SETTLE budget:
            # every failed check threw away a seven-read run-up, and with A
            # watching the hero (which waits on a worker) `board industrial`
            # timed out in 1 of 3 sweeps -- a settle that fails LOUD on a
            # perfectly good screen, which is its own kind of wrong.
            continue
        return rows
    raise RuntimeError(
        f"{label}: never settled after {MAX_SETTLE} frames; not settled: "
        + (", ".join(waiting[:4]) + (" ..." if len(waiting) > 4 else "")
           if waiting else "nothing -- the FRAME never stopped changing"))


CW, LH, FS, PAD = 8.4, 17.0, 14.0, 10.0
MONO = ("ui-monospace,SFMono-Regular,'DejaVu Sans Mono','Cascadia Mono',"
        "Menlo,Consolas,'Liberation Mono',monospace")


#: one cell of a composited frame.  The last two are the STYLE tier, added in
#: inc43 -- see `cell_grid`.
Cell = tuple[str, str, str, bool, bool]


def cell_grid(app) -> tuple[list[list[Cell]], str]:
    """Read the composited frame as (char, fg, bg, bold, underline) per CELL.

    Segment styles are read off the compositor, not off any widget's internal
    state: a widget can hold its text and still not have been flushed, and it
    is the flush a capture reads.  Returns the screen's own background too, so
    the picture's ground is the app's ground rather than a guess.

    THE STYLE TIER, AND WHY `reverse` IS RESOLVED HERE RATHER THAN IN THE
    EXPORTER.  `Kit.match` is the one contract seat whose emphasis may not add
    a cell (operator ruling 9 -- the result text comes back byte for byte), so
    every one of the eleven kits spells `MATCH_STYLE` as a STYLE over a hue:
    seven `bold`, two `underline`, and `industrial`/`solari` `reverse`.  Until
    inc43 this function returned three fields and the whole tier was dropped:
    66 declared runs across the eleven S6 sheets, none painted.

    `bold` and `underline` are carried out as flags because they are a
    property of the TEXT and the exporter emits them as text attributes.
    `reverse` is not -- it is a GROUND channel wearing a style word's costume,
    which is exactly why it went missing.  Rich hands it over as
    `Style.reverse` with `color` and `bgcolor` STILL IN THEIR DECLARED ORDER
    (measured: industrial's run arrives `#ff4b1f` on `#121212`, flag set), so
    an exporter looking only at `bgcolor` sees the page's own ground and paints
    nothing.  Swapping the pair HERE turns the run back into what it actually
    is -- ink on a ground -- and the exporter's existing background-run code
    then paints it with no new branch and no second notion of what a ground is.
    """
    grid: list[list[Cell]] = []
    ground = "#000000"
    for strip in app.screen._compositor.render_strips():
        row: list[Cell] = []
        for seg in strip:
            st = seg.style
            fg = (st.color.triplet.hex
                  if (st and st.color and st.color.triplet) else "#ffffff")
            bg = (st.bgcolor.triplet.hex
                  if (st and st.bgcolor and st.bgcolor.triplet) else ground)
            if st and st.reverse:
                fg, bg = bg, fg
            bold, under = bool(st and st.bold), bool(st and st.underline)
            for ch in seg.text:
                row.append((ch, fg, bg, bold, under))
        grid.append(row)
    # the ground is the most common background in the frame -- measured, not
    # assumed, because several languages paint a full-bleed panel over it
    counts: dict[str, int] = {}
    for row in grid:
        for cell in row:
            counts[cell[2]] = counts.get(cell[2], 0) + 1
    if counts:
        ground = max(counts, key=counts.get)
    return grid, ground


def svg_from_grid(grid, ground: str, label: str) -> str:
    """One SVG, self-contained, no network.

    Backgrounds are emitted as RUNS -- consecutive cells sharing a bg become
    one `<rect>` -- which is where the size win over the stock exporter comes
    from.

    THE STYLE TIER (inc43).  A text run now breaks on WEIGHT and DECORATION as
    well as on colour, and carries `font-weight="bold"` / `text-decoration=
    "underline"` when it has them.  `reverse` needs nothing here: `cell_grid`
    resolves it into the (ink, ground) pair it always was, so it arrives as a
    background run and is painted by the loop above.  That is the whole reason
    the swap lives there and not here -- this function has exactly one idea of
    what a ground is, and teaching it a second one would have been a way to
    disagree with itself later.

    WHAT IS STILL DROPPED, said out loud: `italic`, `strike`, `dim`, `blink`.
    No kit declares any of them, and the law over these frames is a comparison
    of DECLARED runs against PAINTED ones -- so the day a kit reaches for one,
    that law goes red rather than this docstring going quietly out of date.

    HOW THE GRID IS HELD -- ONE `x` PER RUN, AND NOTHING ELSE.  Two richer
    schemes were tried against a real browser and both had to go, for the same
    reason in two costumes:

      * one `x` per GLYPH (~290 000 coordinates across the twenty frames);
      * one `x` per run plus `textLength` + `lengthAdjust="spacing"`.

    Each froze Chrome's renderer for 30 s whenever anything forced the document
    through layout or composition -- an `#anchor` jump, a CSS filter, an
    overlay, even switching a tab panel.  The second is if anything worse: it
    reads cheap, but `textLength` makes the engine MEASURE the text and
    redistribute the gaps on every single layout pass, for every element that
    carries it.

    So a run gets its starting `x` and no more.  What that gives up is real and
    is worth stating: inside one run, a viewer falling back to a font whose
    advance is not exactly the declared cell width will drift.  What it does
    NOT give up is the part that matters -- error cannot accumulate ACROSS a
    row, because the next run re-anchors at its own absolute coordinate, and
    runs here average well under half a row.  Spaces are non-breaking so no
    engine may collapse a gap and shift the cells after it.  The `.txt` remains
    the artifact any law measures; this is a picture of it that a browser can
    actually paint.
    """
    import html as _h
    h = len(grid)
    w = max((len(r) for r in grid), default=0)
    pw, ph = w * CW + 2 * PAD, h * LH + 2 * PAD
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pw:.1f} '
           f'{ph:.1f}" role="img" aria-label="{_h.escape(label)}">',
           f'<title>{_h.escape(label)}</title>',
           f'<rect width="{pw:.1f}" height="{ph:.1f}" fill="{ground}"/>',
           f'<g font-family="{MONO}" font-size="{FS}" xml:space="preserve" '
           f'style="white-space:pre;font-variant-ligatures:none">']
    for y, row in enumerate(grid):
        ry = PAD + y * LH
        # background runs
        x = 0
        while x < len(row):
            bg = row[x][2]
            x2 = x
            while x2 < len(row) and row[x2][2] == bg:
                x2 += 1
            if bg != ground:
                out.append(f'<rect x="{PAD + x * CW:.1f}" y="{ry:.1f}" '
                           f'width="{(x2 - x) * CW:.1f}" height="{LH:.1f}" '
                           f'fill="{bg}"/>')
            x = x2
        # text runs, one per (colour, weight, decoration)
        ty = ry + 0.78 * LH
        x = 0
        while x < len(row):
            key = (row[x][1], row[x][3], row[x][4])
            x2 = x
            while x2 < len(row) and (row[x2][1], row[x2][3], row[x2][4]) == key:
                x2 += 1
            fg, bold, under = key
            text = "".join(cell[0] for cell in row[x:x2])
            if text.strip():
                attr = (' font-weight="bold"' if bold else "") +                        (' text-decoration="underline"' if under else "")
                out.append(f'<text x="{PAD + x * CW:.1f}" y="{ty:.1f}" '
                           f'fill="{fg}"{attr}>'
                           f'{_h.escape(text).replace(" ", chr(160))}</text>')
            x = x2
    out += ["</g>", "</svg>", ""]
    return "\n".join(out)


def ink(rows: list[str]) -> float:
    total = sum(len(r) for r in rows)
    return sum(1 for r in rows for c in r if c not in "  ") / total * 100


def write(name: str, rows: list[str], app=None,
          title: str = "") -> tuple[int, int, float]:
    """Write a rectangle -- every row padded to the widest, never clipped.

    The rectangle law: the grid is what the verifiers measure, and a row that
    lost its trailing cells is a violation introduced by the writer, not by
    the design.

    When `app` is given, the same frame is also exported to SVG in colour by
    Textual itself.  Not re-rendered here and not re-coloured: whatever the
    terminal would show is what the file holds.
    """
    w = max(len(r) for r in rows)
    rect = [r.ljust(w) for r in rows]
    (OUT / f"{name}.txt").write_text("\n".join(rect) + "\n", encoding="utf-8")
    if app is not None:
        grid, ground = cell_grid(app)
        (OUT / f"{name}.svg").write_text(
            svg_from_grid(grid, ground, title), encoding="utf-8")
    return w, len(rect), ink(rect)


#: the sheets `sweep()` writes for each language, in the order it writes them.
#: This is the BOARD sweep's own output and nothing else -- the `--surface`
#: entry point writes `surface_*` into the same directory, from a separate run,
#: and the reproducibility check below must not confuse the two (F-5).
#:
#: It has to match the `write()` names in `sweep()`.  It is not derived from
#: them because they are produced inside a Textual session that has to run to
#: produce anything, and a check that had to sweep in order to learn what a
#: sweep produces could not be used to decide whether the sweep was complete.
#: A rename that forgets this constant fails LOUD on the next run -- `main()`
#: reads these names directly, so a missing one raises there rather than
#: quietly narrowing the check to the files that happen to exist.
BOARD_SHEETS = ("board", "gallery")


def board_frames() -> list[str]:
    """Every `.txt` one `sweep()` produces, named rather than discovered."""
    return [f"{sheet}_{lang}.txt"
            for lang in TH.ORDER for sheet in BOARD_SHEETS]


async def sweep() -> list[dict]:
    from app import TaskboardWidget          # prototypes/widget_slice/app.py

    freeze_clock()                           # AFTER the imports it patches
    OUT.mkdir(parents=True, exist_ok=True)
    report: list[dict] = []

    for lang in TH.ORDER:
        app = TaskboardWidget(board_path=FIXTURE)
        async with app.run_test(size=SIZE) as pilot:
            await pilot.pause()
            app.notify = lambda *a, **kw: None       # no toasts in a capture
            app.set_theme(lang)
            rows = await settle(pilot, app, f"board {lang}")
            w, h, i = write(f"board_{lang}", rows, app,
                            f"taskboard · {lang} · board")
            entry = dict(lang=lang, board=(w, h, i))

            await pilot.press("g")
            grows = await settle(pilot, app, f"gallery {lang}")
            gw, gh, gi = write(f"gallery_{lang}", grows, app,
                               f"taskboard · {lang} · components")
            entry["gallery"] = (gw, gh, gi)

        report.append(entry)
        print(f"  {lang:<11} board {w}x{h} {i:5.1f}% ink   "
              f"gallery {gw}x{gh} {gi:5.1f}% ink")
    return report


# ===========================================================================
# THE SURFACE SWEEP (--surface) -- the eighth axis, one image, every language
#
# WHY ONE FIXED IMAGE AND NOT A SYNTHETIC ONE.  The boards above compare the
# languages on one fixture because "the same screen in ten languages" is only
# an honest comparison when it really is the same screen.  The same argument
# applies one level down: a surface posture is a claim about what a language
# does to REAL PIXELS, and ten postures shown ten different pictures is a
# scrapbook again.  The picture is `tui-demos/lab/mbb_rho_final.npy` -- a 20x60
# density field from the topology-optimisation runs, rendered through R1's own
# PAPER/INK colormap at scale 6 (360x120 px), which is the image that lab
# already publishes.
#
# THE `.npy` LOAD LIVES HERE AND NOT IN `taskboard/`.  numpy is not a declared
# dependency of the package (`pyproject.toml`: textual, tzdata, pillow,
# textual-image).  `prototypes/` is dev-side and may import anything; the
# shipped package may not grow a dependency to make a capture convenient.
# ===========================================================================

MBB = Path(r"C:\Users\jjgh8\Github\tui-demos\lab\mbb_rho_final.npy")
MBB_SCALE = 6                       # 20x60 -> 120x360 px, NEAREST
PAPER, INK = (248, 246, 240), (28, 32, 44)      # r1_pixels.py's colormap


def test_image():
    """The MBB density field as a PIL image, exactly as `r1_pixels.load()`
    builds it: linear blend PAPER->INK on the clipped field, NEAREST upscale.
    Reproduced rather than imported -- `r1_pixels.py` has no import guard and
    lives in another repo this batch may only READ."""
    import numpy as np
    from PIL import Image as PImage
    g = np.clip(np.load(MBB), 0, 1)[..., None]
    rgb = (np.array(PAPER, np.uint8) * (1 - g)
           + np.array(INK, np.uint8) * g).astype(np.uint8)
    img = PImage.fromarray(rgb)
    return img.resize((img.width * MBB_SCALE, img.height * MBB_SCALE),
                      PImage.NEAREST)


SURFACE_H = 26                      # rows the region reserves inside the frame
#: WHAT THE FIGURE IS, handed to every posture that captions or audits one.
#: Named rather than inlined because two other files have to agree with it and
#: neither may import this one (it pulls in a Textual app and numpy):
#: `export_to_skill.py` prints each posture's image box beside the frame this
#: label produced, and `tests/test_surface.py` renders against the shipped
#: frame. Both repeat the string with this line cited; the test fails loudly
#: if it drifts, which is the check the exporter does not have (F-12).
SURFACE_LABEL = "mbb rho final"


def surface_sheet(lang: str, img):
    """The specimen page a surface capture photographs: the language's own
    section header, then the reserved rectangle.

    Deliberately NOT a board screen.  Spec section 5 is explicit that no
    existing screen renders a region in this batch, so wiring one here to take
    a picture of it would be the batch shipping the thing it declared out of
    scope.  What the sheet does carry is the language's `sect()` -- so the
    frames differ pairwise OUTSIDE the image rectangle, which is the
    acceptance boundary LANGUAGES.md already uses for the boards."""
    import taskboard.language as LG
    kit = LG.kit(lang)
    res = kit.raster_region(img, SIZE[0] - 2, SURFACE_H, label=SURFACE_LABEL)
    head = kit.sect("SURFACE", f"{res.posture} - {img.width}x{img.height} px",
                    SIZE[0] - 2, SURFACE_H)
    return "\n".join(head + res.rows), res


async def sweep_surfaces() -> list[dict]:
    """One image, every implemented kit, headless, at the board's viewport."""
    from textual.app import App, ComposeResult
    from textual.widgets import Static

    import taskboard.themes as _TH

    img = test_image()
    OUT.mkdir(parents=True, exist_ok=True)
    report: list[dict] = []

    for lang in _TH.ORDER:
        body, res = surface_sheet(lang, img)

        class Sheet(App):
            CSS = ("Screen { layout: vertical; }\n"
                   "#surface { padding: 0 1; width: 1fr; height: 1fr; }")

            def compose(self) -> ComposeResult:
                yield Static(body, id="surface", markup=True)

        app = Sheet()
        async with app.run_test(size=SIZE) as pilot:
            await pilot.pause()
            app.screen.styles.background = _TH.THEMES[lang]["ground"]
            rows = await settle(pilot, app, f"surface {lang}")
            w, h, i = write(f"surface_{lang}", rows, app,
                            f"taskboard - {lang} - surface ({res.posture})")
        report.append(dict(lang=lang, posture=res.posture, ink=i,
                           pixels=None if res.pixels is None
                           else res.pixels.size))
        print(f"  {lang:<11} {res.posture:<9} {w}x{h} {i:5.1f}% ink   "
              f"raster {'refused' if res.pixels is None else res.pixels.size}")
    return report


def surface_main() -> int:
    if not MBB.exists():
        print(f"TEST IMAGE MISSING: {MBB}", file=sys.stderr)
        return 2
    import taskboard.themes as _TH
    print(f"image {MBB.name} | viewport {SIZE[0]}x{SIZE[1]} | "
          f"{len(_TH.ORDER)} languages | animations off")
    report = asyncio.run(sweep_surfaces())

    # THE SWEEP'S OWN LAW, the same one the boards keep: no two frames
    # identical.  Two languages whose surface renders byte-for-byte the same is
    # the exact defect LANGUAGES.md records, one axis down.
    got = {r["lang"]: (OUT / f"surface_{r['lang']}.txt").read_text(
        encoding="utf-8") for r in report}
    order = [r["lang"] for r in report]
    dupes = [(a, b) for i, a in enumerate(order) for b in order[i + 1:]
             if got[a] == got[b]]
    if dupes:
        print(f"IDENTICAL SURFACES: {dupes}", file=sys.stderr)
        return 1
    print(f"\n  {len(report)} surfaces -> {OUT}")
    print(f"  no two identical ({len(order) * (len(order) - 1) // 2} pairs)")
    return 0


def check_reproducible(first: dict[str, str]) -> list[str]:
    """Re-run the whole sweep in a SEPARATE PROCESS and diff every grid.

    Why a subprocess and not a second pass in this one: the first version of
    this check swept twice in-process and reported "identical" while the
    captures were in fact drifting between runs.  Both in-process sweeps read
    nearly the same wall clock, so the confound the check was supposed to catch
    was present in both samples.  A check whose two samples share the bug is a
    vacuous check -- it can only ever pass.  A fresh interpreter re-imports the
    app, re-reads the fixture and re-applies `freeze_clock()` from scratch,
    which is the condition someone rebuilding these files a week from now
    actually has.
    """
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                            "--sweep-to", td],
                           capture_output=True, text=True,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        if r.returncode != 0:
            raise RuntimeError(f"control sweep failed:\n{r.stderr[-1500:]}")
        # A FILE THE CONTROL ARM DID NOT WRITE IS A DISAGREEMENT ABOUT WHAT A
        # SWEEP PRODUCES, and it is reported as one rather than as whatever
        # error `read_text` happens to raise.  That is how F-5 presented: a
        # bare FileNotFoundError traceback, which reads like a missing input
        # and was in fact the two arms sweeping different things.
        missing = [n for n in first if not (Path(td) / n).exists()]
        if missing:
            raise RuntimeError(
                f"the control sweep did not write {missing} -- the two arms "
                f"disagree about what a sweep produces. If a sheet was renamed "
                f"or added, BOARD_SHEETS is the place that says so.")
        return [n for n, t in first.items()
                if (Path(td) / n).read_text(encoding="utf-8") != t]


def main() -> int:
    if not FIXTURE.exists():
        print(f"FIXTURE MISSING: {FIXTURE}", file=sys.stderr)
        return 2
    print(f"fixture {FIXTURE.name} | viewport {SIZE[0]}x{SIZE[1]} | "
          f"{len(TH.ORDER)} languages | animations off")
    report = asyncio.run(sweep())

    # DETERMINISM, CHECKED RATHER THAN ASSERTED.  Sweep twice and compare every
    # grid.  This is the check that caught solari's mid-flip label, and it is
    # cheap enough to keep: a capture that differs between two runs of the same
    # code on the same fixture is not a picture of a design, it is a picture of
    # a moment.
    #
    # THE SET IS NAMED, NOT GLOBBED, AND THAT WAS A BUG (F-5).  This line read
    # `OUT.glob("*.txt")` and therefore meant "every text capture in the output
    # directory" -- which stopped being this sweep's output the moment the
    # `--surface` entry point started writing `surface_*.txt` beside it.  The
    # control arm below runs `sweep()` alone, so it never writes those, and the
    # comparison demanded a control file that could not exist: the DOCUMENTED
    # command died in its own determinism check with a FileNotFoundError on
    # `surface_blueprint.txt`.  Naming the frames makes the two arms agree by
    # construction instead of by whatever happens to be on disk.
    first = {n: (OUT / n).read_text(encoding="utf-8") for n in board_frames()}
    print("\n  re-sweeping in a fresh process to check reproducibility...")
    drift = check_reproducible(first)
    if drift:
        print(f"NON-REPRODUCIBLE CAPTURES: {drift}", file=sys.stderr)
        return 1
    print(f"  {len(first)} grids identical across two PROCESSES")

    # The sweep's own law: ten languages, twenty captures, and no two boards
    # identical.  Two languages rendering byte-identically is the exact defect
    # LANGUAGES.md records ("Two of the eight languages rendered
    # byte-identically") -- so the sweep refuses to call itself done without
    # checking, instead of leaving it to the eye.
    if len(report) != len(TH.ORDER):
        print("INCOMPLETE SWEEP", file=sys.stderr)
        return 1
    boards = {L["lang"]: (OUT / f"board_{L['lang']}.txt").read_text(
        encoding="utf-8") for L in report}
    dupes = [(a, b) for i, a in enumerate(TH.ORDER) for b in TH.ORDER[i + 1:]
             if boards[a] == boards[b]]
    if dupes:
        print(f"IDENTICAL BOARDS: {dupes}", file=sys.stderr)
        return 1
    print(f"\n  {len(report) * 2} captures -> {OUT}")
    print("  no two boards identical")
    return 0


if __name__ == "__main__":
    # `--sweep-to DIR`: capture into DIR and say nothing.  This is the control
    # arm of the reproducibility check above, run as a separate interpreter.
    if len(sys.argv) == 3 and sys.argv[1] == "--sweep-to":
        OUT = Path(sys.argv[2])
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()):
            asyncio.run(sweep())
        raise SystemExit(0)
    # `--surface [DIR]`: the eighth axis, one image through every kit.  A
    # separate entry point rather than a fifth capture inside `sweep()`: the
    # board sweep photographs a SCREEN and this one photographs a PRIMITIVE
    # that no screen consumes yet (spec section 5), so folding them together
    # would make the boards depend on a test image from another repo.
    if sys.argv[1:2] == ["--surface"]:
        if len(sys.argv) == 3:
            OUT = Path(sys.argv[2])
        raise SystemExit(surface_main())
    raise SystemExit(main())
