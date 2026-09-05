"""The LANGUAGE-AXIS acceptance test (PENDING.md item 0).

The user's verdict, 2026-07-25: switching language felt like a palette swap —
only the hero changed. The fix is only real if it survives these two checks,
which are the ones VERIFY.md prescribes for design tokens:

  1. GREYSCALE PAIR TEST — strip colour from every pair of languages and diff
     the rendered text. Any identical pair is a recolour, not a language.
     Run at kit level (fast, exhaustive) AND at app level with the HERO REGION
     MASKED OUT — "the axis is still fake" if only the hero differs.
  2. TOKEN MUTATION — flip each structural token a language declares and the
     render must change. A token whose mutation renders identically is dead
     metadata (LANGUAGES.md: a language definition is code, not a manifest).

Probe discipline (BACKGROUND.md §5: test-selection bugs outnumbered app bugs):
the instrument self-checks its own markup stripping and its hero mask before
believing any verdict.

Data-viz laws are specified in tui-design/DATAVIZ.md (shared-hi normalization,
microbar floor, empty/flat safety, gauge-states-its-value, threshold tick) —
hardened from a sibling fork's bench (the Kimi harvest, PENDING.md).
"""
import asyncio
import importlib.util
import inspect
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

W = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(W))
sys.path.insert(0, str(W / "prototypes" / "widget_slice"))

from taskboard import language as LG      # noqa: E402
from taskboard import themes as TH        # noqa: E402
from taskboard import hero as HE          # noqa: E402
from taskboard import bases as BS         # noqa: E402
from app import checkable_block           # noqa: E402  (the gallery's seat)
from app import radio_block, RADIO_OPTS, RADIO_SEL, RADIO_FOCUS  # noqa: E402
from app import WORKER_GROUPS             # noqa: E402  (the live group set)
from app import button_block, BTN_LABELS  # noqa: E402  (the gallery's seat)
from app import textfield_block, TF_VALUE, TF_CARET  # noqa: E402
from app import TF_PLACE, TF_LONG          # noqa: E402
from app import scrollbar_block            # noqa: E402  (the gallery's seat)
from app import stepper_block, STEP_OPTS  # noqa: E402  (the gallery's seat)
from app import SB_TOTAL, SB_SIZE, SB_BIG, SB_W  # noqa: E402
from taskboard import engine as EN         # noqa: E402

# THE SUITE STOPS READING THE USER'S LIVE BOARD FILE, and this is a defect
# found rather than a preference. `sig_board_file` stats the REAL
# `default_board_path()` — it ignores the fixture every capture is given —
# and below one hour it reports MINUTES SINCE SAVE. Two captures in the same
# run are minutes apart, so the moment the user had actually saved their
# board recently, a check comparing two board renders started reporting a
# render difference that was a CLOCK difference: `# 36 Board file` against
# `# 37 Board file`. It had been silent for fifty passes only because the
# file happened to be old enough to be reported in whole hours.
#
# Stubbed here rather than in `engine.py`: the app is not wrong to watch the
# file, the INSTRUMENT is wrong to let an uncontrolled clock into a byte
# comparison. `default_signals()` resolves this name when an Engine is built,
# so patching the module attribute reaches every capture.
EN.sig_board_file = lambda ctx: EN.Reading("2", "min since save",
                                           "36 KB on disk", EN.CALM)

fails = []


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


# -- THE TWO SEATS THAT LET A LAW GO RED INSTEAD OF RAISING ------------------
# THE NAMED TRAP (VERIFY.md, and four separate instances in this suite's own
# history — passes 52, 53, 55, 64): `r.index(label)` raises PRECISELY when
# the label is missing or mangled, which is the mutation the law exists to
# catch. A raised law reports NOTHING; the interpreter unwinds and the run
# dies with every remaining check unspoken, which on a mutation driver is
# indistinguishable from a mutant nothing catches. The sixty-sixth pass's
# sweep found 48 such constructs at 31 sites still standing, and these two
# seats are what replaced every one of them: 52 constructs at 34 sites —
# 48 at 31 found by the first census, and 4 more at 3 sites that the census
# MISSED because it read assignments and not returns. Mutant M3a found those
# by dying on one.
#
# `at` RETURNS -1, and -1 is a value a comparison can be red about. The rule
# at each call site is that -1 must not accidentally SATISFY the law: where
# both sides of an equality could be -1, the site carries an explicit
# `>= 0` leg, because `-1 == -1` is the same vacuity wearing a different hat.


def at(hay, needle, last=False):
    """WHERE `needle` sits in `hay` — or -1, and never a raise.

    One seat for strings and for sequences: `find`/`rfind` semantics for the
    first, membership-guarded `index` for the second."""
    if isinstance(hay, str):
        return hay.rfind(needle) if last else hay.find(needle)
    # NO `.index` IN THE SEAT THAT EXISTS TO REPLACE `.index`, even a guarded
    # one. The first draft guarded it with `if needle not in seq` and was
    # correct — and it forced the standing law below to carry an EXEMPTION
    # for two lines of its own file, which is the shape a maintainer widens
    # to make a red go away. An absolute law with no exemptions is worth
    # three lines.
    hit = [i for i, x in enumerate(hay) if x == needle]
    return (hit[-1] if last else hit[0]) if hit else -1


def nth(seq, i, default):
    """`seq[i]` when that item exists, else `default` — never an IndexError.

    THE THIRD SEAT, and the one pass 66 refused to write. `at()` has ONE
    right answer for every `.index` site (-1), so its cure was a single
    decision applied 52 times. A `[0]` on an empty list has NO such answer:
    the sentinel has to make THAT law go red, and "" reds a containment law
    while satisfying a `not ...strip()` one. So `default` is POSITIONAL AND
    REQUIRED — there is deliberately no fallback for a site to inherit by
    accident, and every call below names the value it argued for.

    AND A SEAT IS NOT A LAW. `nth` guarantees the run continues; it does not
    guarantee the law goes red. Where the emptiness IS the defect the law
    hunts, the site carries an explicit non-emptiness leg as well — see the
    blueprint registration corners (`len(xs) == 2 and ...`), where an empty
    slice would have satisfied the negative claim vacuously."""
    return seq[i] if -len(seq) <= i < len(seq) else default


def first_of(it, default=-1):
    """The first item of `it`, or `default` — never a `StopIteration`.

    `next(g)` on an exhausted generator is the same trap in the setup lines:
    it does not fail the law that reads it, it kills the file. Named
    `first_of` and not `first` because two law bodies already bind `first`
    as a local — a helper that a section can shadow is a helper that fails
    9000 checks into the run, which is exactly what it did."""
    return next(iter(it), default)


# card metadata fixtures: B differs from A in EVERY field a language might
# choose to show, so any 2-row language must render them differently
META_A = {"proj": "Web", "phase": "Doing", "phase_idx": 1, "n_phases": 4,
          "days": 3, "prio": "high", "blocked": False, "done": False}
META_B = {"proj": "API", "phase": "Review", "phase_idx": 3, "n_phases": 5,
          "days": -2, "prio": "low", "blocked": True, "done": False}

# -- the greyscale instrument ------------------------------------------------
# RICH'S OWN DEFINITION OF A TAG, not one that resembles it. rich reads a
# bracket as markup only when the next character is `[a-z#/@]`
# (rich.markup.RE_TAGS); `[ ]`, `[X]`, `[-]` and `[◎]` are LITERAL TEXT on
# screen. The regex that stood here was `\[[^\[\]]*\]` — it ate all four, and
# the moment a checkbox drew `[ ]` / `[x]` the instrument measured a
# three-cell box as ZERO cells wide. It would have certified an invisible
# control and a gallery row that fits.
#
# Why a regex at all and not `Text.from_markup(...).plain`: that was tried
# first and DIED — the hero hands this function single ROWS of a block whose
# tags span lines, and rich's parser raises `MarkupError` on a fragment with
# an orphan `[/]`. So the projection stays fragment-safe, and `grey_is_rich`
# below proves it agrees with the real parser on every string it is asked
# about. One definition, borrowed; one implementation, checked against it.
_TAG = re.compile(r"\[[a-z#/@][^\[]*?\]")

from rich.text import Text            # noqa: E402  (the real markup parser)


def grey(markup: str) -> str:
    """Strip rich colour tags, keep literal (escaped) brackets as text.

    The tag definition is rich's (see `_TAG` above); this is the fragment-safe
    implementation of it, and `grey_is_rich` is the law that they agree."""
    return _TAG.sub("", markup.replace("\\[", "\x00")).replace("\x00", "[")


def grey_is_rich(markup: str) -> bool:
    """Does the projection agree with the thing that actually renders?

    Probe discipline (BACKGROUND.md §5: test-selection bugs outnumbered app
    bugs): the instrument checks itself before any verdict is believed. This
    is asked of every component string the contract laws measure, so the
    cheap projection cannot drift from rich's semantics without a red line —
    which is exactly how the `[ ]` hazard surfaced."""
    return grey(markup) == Text.from_markup(markup).plain


def kit_sig(k) -> str:
    """One language's structural fingerprint: every kit primitive at fixed
    inputs, colour stripped. Colour is the one thing this must NOT contain."""
    parts = [
        k.head("BACKLOG", 5, 20, 0),
        k.head("DONE", 0, 14, 3),
        k.card_row("Fix the wrapped frame", "3d", k["warn"], 28, 2, True),
        k.card_row("Write the handoff", "12d", k["mut"], 28, 0, False),
        "\n".join(k.card_rows("Fix the wrapped frame", "3d", k["warn"], 28, 2,
                              True, META_A)),
        k.tile_row(" 12", "overdue", k["alert"], 20),
        k.meter(3, 8, [4, 0, 2, 2], 44),
        k.bar(9, None, None),
        "\n".join(k.sect("AGENDA", "12 open", 50)),
        "\n".join(k.sect("AGENDA", "12 open", 50, 20)),   # the DISPLAY form
        "".join(k.cal_cell(x) for x in ("none", "over", "multi", "one")),
        k.queue_marker(2),
        # the COMPONENT LIBRARY (COMPONENTS.md) — the parts the user touches
        k.switch(True), k.switch(False),
        k.slider(4, 0, 10, 10),
        # the value family across its state axis, and its knobless twin —
        # a language that draws one identically to another has not restyled
        # the parts, which is the only place a language is allowed to speak
        k.slider(4, 0, 10, 10, LG.EDITED),
        k.readbar(4, 0, 10, 10),
        "".join(k.spinner(t) for t in range(4)),
        k.tabs(["board", "lanes", "agenda", "gantt"], "board"),
        k.CUR,
        # identity: mascot + wordmark through the language's own base + voice
        "\n".join(k.mascot()),
        "\n".join(k.wordmark("AB")),
        k.empty(16),
        "|".join(k.flip_frames(True)) + "|".join(k.flip_frames(False)),
        # iconography + data-viz (axes 4 and 7)
        " ".join(k.icon(i) for i in
                 ("deadline", "overdue", "wip", "blocked", "workday")),
        k.spark([1, 3, 2, 5, 4, 6, 2, 7], 8),
        "\n".join(k.plot([2, 5, 3, 7, 4, 8, 6, 9], 24, 4)),
        k.gauge(7, 0, 10, 10),
        k.display_cap("Days Left"),
        k.tcss(),
    ]
    # strip hex from the stylesheet part too: surface/composition css carries
    # colours, and a pairwise diff must never ride on a colour alone
    return re.sub(r"#[0-9a-fA-F]{6}", "#", grey("\n".join(parts)))


def mut_sig(name: str) -> str:
    """The mutation fingerprint adds the theme stylesheet, so tokens that live
    in TCSS (`sel`) are covered too, and the card markup WITH ITS COLOUR, so
    a structural token that carries a colour (darkside's `rail`) is provable
    too — colour-stripped, a recoloured rail is invisible and the token would
    read as dead metadata. Same-language comparisons only — both additions
    contain hex values, which would trivialise a pairwise diff."""
    k = LG.kit(name)
    coloured = "\n".join(k.card_rows("Fix the wrapped frame", "3d", k["warn"],
                                     28, 2, True, META_A)) + k.head("BACKLOG", 5, 20, 0)
    # ... and the BOARD MEASURE. Every width in kit_sig is column-sized
    # (14-50), which is the whole surface a columns language ever gets — but a
    # SECTIONS language composes a full-width spread, and a token that only
    # acts there (swiss's `columns`: 3 columns need 78 cells) was invisible to
    # this fingerprint and read as dead metadata. Measured: swiss.columns
    # mutated 3 -> 2 with no change at all until this line existed.
    wide = ("\n".join(k.card_rows("Shut down legacy servers", "8d", k["mut"],
                                  105, 0, False, META_A))
            + "\n".join(k.head("BACKLOG", 7, 106, i) for i in range(3)))
    return kit_sig(k) + TH.tcss(name) + coloured + wide


# a distinct alternative for every structural token a language may declare
ALT = {
    "frame": lambda v: "double" if v != "double" else "rule",
    "numbered": lambda v: not v,
    "dot_w": lambda v: 1 if v != 1 else 2,
    "gap": lambda v: 0 if v else 1,
    "pitch": lambda v: 1 if v != 1 else 2,
    "meter": lambda v: "blocks" if v != "blocks" else "gradient",
    "sel": lambda v: "double" if v != "double" else "solid",
    "layout": lambda v: "flow" if v != "flow" else "rail",
    "columns": lambda v: 2 if v != 2 else 3,
    "split": lambda v: (20, 20) if tuple(v) != (20, 20) else (28, 34),
    "rail": lambda v: "#ff00ff" if v != "#ff00ff" else "#00ff00",
    "plate": lambda v: "#ff00ff" if v != "#ff00ff" else "#00ff00",
    "rule": lambda v: "#ff00ff" if v != "#ff00ff" else "#00ff00",
    "band": lambda v: "#ff00ff" if v != "#ff00ff" else "#00ff00",
    "tick": lambda v: "#ff00ff" if v != "#ff00ff" else "#00ff00",
    "flap": lambda v: "#ff00ff" if v != "#ff00ff" else "#00ff00",
    "seam": lambda v: "#ff00ff" if v != "#ff00ff" else "#00ff00",
    "unit": lambda v: "#ff00ff" if v != "#ff00ff" else "#00ff00",
    "tally": lambda v: "•" if v != "•" else "▪",
    "hatch": lambda v: "╲" if v != "╲" else "╱",
    "knockout": lambda v: not v,
    "tempo": lambda v: v + 37,
    "easing": lambda v: "linear" if v != "linear" else "out_cubic",
}


def screen_text(app):
    return ["".join(s.text for s in strip)
            for strip in app.screen._compositor.render_strips()]


def masked_board(app, rows):
    """The board with the hero region blanked — item 0's acceptance boundary:
    languages must differ OUTSIDE the hero."""
    r = app.query_one("#hero").region
    out = []
    for y, row in enumerate(rows):
        if r.y <= y < r.y + r.height:
            row = row[: r.x] + " " * min(r.width, max(0, len(row) - r.x)) \
                + row[r.x + r.width:]
        out.append(row)
    return "\n".join(out)


SETTLE_MAX = 40
# iterations each settle() actually consumed. A gate that passes because its
# bound is generous is a gate about to rot: if the suite starts settling near
# SETTLE_MAX, the next increment's load will push it over and the reds will
# read as app bugs. Reported as headroom at the end of the run.
SETTLE_USED: list[int] = []

# Every content widget `KanbanBoard.build()` mounts, named by the class the
# build attaches — which is the only enumeration that cannot drift from the
# renderer, because the renderer writes these strings. All three branches
# mount cards as `.kb-card`; the columns and split branches mount phase heads
# as `.col-head` and the empty-state seat as `.kb-empty`; the split mounts the
# detail pane as `.kb-detail`. Grep-verified: nothing outside build() mounts
# any of the four. A widget in this set that the compositor is drawing is a
# widget expected to carry ink.
BOARD_CONTENT = ("kb-card", "col-head", "kb-empty", "kb-detail")


def _stale_paint(card) -> bool:
    """Was this card's paint composed at a seat it no longer has?

    Asks the card what it would draw RIGHT NOW and compares that to what it is
    already showing. `update` is intercepted, so the answer is collected
    without ever being applied: this reports, it does not repair. See settle()
    condition C for why the distinction is the whole point."""
    got: list = []
    card.update = got.append
    try:
        card.render_card()
    finally:
        del card.update            # drop the shim, restore the class method
    return bool(got) and got[0] != card.content


async def settle(app, pilot, label: str) -> bool:
    """Wait for a frame that is actually PAINTED, not merely produced.

    The old recipe was a fixed number of pauses, which is a guess about
    timing. Under full-suite load the guess was wrong about one run in three:
    the board came back with its cards mounted but BLANK, and the checks that
    read the board failed while the checks that read the section head passed
    (PENDING: the darkside capture race). `TaskCard.on_mount` defers its own
    paint with `call_after_refresh`, so "the widget exists" and "the widget
    has been drawn" are two different moments.

    The condition is deliberately generic — it interrogates the widget tree,
    not any one language's glyphs:

      A. every content widget the board mounts and the compositor SAYS it is
         drawing has painted pixels inside its own clipped area
      B. the rendered frame is identical on two consecutive reads

    A is asserted against the composited frame, not the widget's internal
    state: a card can hold its text and still not have been flushed, and it
    is the flush the captures read. B alone is what the old recipe
    approximated, and B alone is what failed.

    **A USED TO SAY "every CARD", and that was too narrow — PENDING's
    twenty-ninth-pass hypothesis, now measured.** The split branch mounts its
    detail pane as an EMPTY `Static` and fills it from `_seed_detail`, which
    `build()` defers with `call_after_refresh`. Cards are their own deferral,
    so they can finish first; the frame then repeats identically for a beat
    with the pane still blank, and the old condition signed it off. Measured
    in isolation before the fix — 30 nord captures, the shipped condition,
    `_probe30.py` — **4 of 30 fired on a frame whose detail pane had ZERO
    painted rows**, which is the observed red verbatim. The condition now
    interrogates every class `build()` mounts (`BOARD_CONTENT`), so the pane
    is waited on the same way a card is. Not a nord special case: the list is
    the renderer's own class names, and it covers the sections and columns
    branches too (their heads and empty seats were never waited on either).

    The widget's own `renderable` is deliberately NOT consulted. It reads
    empty on this Textual version even for a pane that HAS painted (measured:
    `renderable chars=0` on all 30 probe runs, painted and blank alike), so
    widget state cannot say what content is expected. The composited frame is
    the only sound oracle here, which is the same reason A exists at all.

    `visible_widgets` is what makes A sound. A card's `region` is in SCREEN
    space and keeps growing past the fold, so a naive region slice reads
    whatever is at those coordinates — for the card at y=29 that is the
    Footer, whose text scored as "painted". That false positive would have
    masked the exact bug this function exists to catch. The compositor's map
    holds only the widgets it actually draws, each with its clip, so cards
    scrolled under the fold drop out instead of lying.

    Where a size class shows no board there are no such widgets, A is
    vacuously true, and B settles the frame by itself — one condition, no
    special case for the 60-column regime.

    **C — a card's paint must have been composed at the seat it currently
    HAS. This is the darkside capture race, diagnosed in the forty-sixth
    pass.** `TaskCard.render_card` takes its row width from `self.size.width`
    and falls back to 20 when the layout has not run yet (kanban.py), so a
    card mounted a beat before its first layout bakes an **18-cell** row and
    holds that string until the post-layout re-render lands. That bake is
    INK, so A is satisfied; and the frame is genuinely static in the gap
    before the re-render, so B is satisfied too. A and B together therefore
    signed off on a board whose four titles read `renew tls … 3d` instead of
    `renew tls certificate` — which is the intermittent legibility red
    verbatim, and why pass 30 could positively exclude an unpainted widget
    and a settle timeout: settle did not time out, it SUCCEEDED on the wrong
    frame. The saved failing frame (`_race_darkside.txt`) matches a forced
    18-cell render byte for byte on the card rows.

    Measured, not theorised. With the corrective re-render delayed 50 ms the
    shipped A+B condition produced **17 illegible frames in 30 captures**, all
    carrying the 18-cell bake; with no delay, **0 in 30**. The 18 is pinned:
    only `size.width == 0` yields `max(8, (0 or 20) - 2)`.

    C is asked as a SHADOW render (`_stale_paint`): the card is asked what it
    would draw at its present seat with `update` intercepted, so the check
    MEASURES the app and never repairs it — a settle that silently re-rendered
    the board would mask the very class of bug it exists to catch. Validated
    both ways before it was shipped: **0 false positives** over all ten
    languages at 118, 80 and 60 in the settled state, and **0 misses** on the
    amplified narrow frames.

    Bounded, because an unbounded settle loop once hung a 600 s run.
    """
    from textual.widgets import Static
    from kanban import TaskCard
    prev = None
    stuck: list[str] = []
    for i in range(SETTLE_MAX):
        rows = screen_text(app)
        h = len(rows)
        drawn = app.screen._compositor.visible_widgets
        stuck = []
        for c in app.query(Static):
            if not any(c.has_class(cl) for cl in BOARD_CONTENT):
                continue               # not the board's content: not ours
            box = drawn.get(c)
            if box is None:
                continue               # clipped away: evidence of nothing
            area = box[0].intersection(box[1])
            if not (area.width and area.height):
                continue
            if not any(rows[y][area.x: area.x + area.width].strip()
                       for y in range(area.y, min(area.y + area.height, h))):
                stuck.append(f"{'.'.join(sorted(c.classes))}@"
                             f"{area.x},{area.y} {area.width}x{area.height}")
            elif isinstance(c, TaskCard) and _stale_paint(c):
                stuck.append(f"{'.'.join(sorted(c.classes))}@"
                             f"{area.x},{area.y} STALE PAINT (composed at a "
                             f"seat it no longer has; seat is now "
                             f"{c.size.width})")
        cur = "\n".join(rows)
        if not stuck and cur == prev:
            SETTLE_USED.append(i + 1)
            return True
        prev = cur
        await pilot.pause()
    # A TIMEOUT IS A FAIL. Never proceed quietly with an unpainted frame: a
    # capture that silently returns a blank board turns every check reading
    # it into a lie. Recorded (so the run exits non-zero and names itself)
    # and then allowed to continue, because the cascade is the diagnosis.
    #
    # The detail NAMES THE WIDGETS THAT NEVER PAINTED, because a timeout that
    # only says "the board" sends the next reader hunting. The whole list is
    # collected rather than short-circuited on the first blank — one extra
    # pass over widgets already in hand, and it is what turns this FAIL into
    # a pointer. `stuck` empty here means condition B alone never settled:
    # the frame kept changing, which is a different failure and reads as one.
    check(f"capture settle timeout: board never painted ({label})", False,
          f"gave up after {SETTLE_MAX} iterations; not settled: "
          + (", ".join(stuck[:4]) + (" ..." if len(stuck) > 4 else "")
             if stuck else "nothing — the FRAME never stopped changing"))
    return False


def body_rows(board: str) -> list[str]:
    """The board WITHOUT its last row. Textual's Footer draws its own `▏`
    key separator, so a naive `RAIL in board` search finds the footer in
    every language and proves nothing."""
    return board.split("\n")[:-1]


async def capture(name: str, mutate=None, board_path=None, size=(118, 30)):
    """Fresh app, language applied, one board-size frame. `mutate` is a
    (token, value) applied to THEMES[name] before the theme is set.
    `board_path` swaps in a deterministic fixture board (Board.load seeds
    demo data on a missing path — tasks with due dates across weeks).
    `size` exists because one width hides a whole regime (VERIFY.md): an
    identity mechanism has to survive the narrow board, not only 118.

    `board_path` is REQUIRED. The default stays on the signature only so no
    call site changes shape; passing nothing raises. Falling back to
    `default_board_path()` would open the user's live board.json, which the
    desktop app rewrites underneath a running suite — that made every
    app-level comparison a race and produced reds that never reproduced."""
    if board_path is None:
        raise ValueError(
            "capture() requires an explicit fixture board_path; probing the "
            "live board.json is forbidden")
    from app import TaskboardWidget
    old = None
    if mutate:
        tok, val = mutate
        old = TH.THEMES[name].get(tok)
        TH.THEMES[name][tok] = val
    try:
        app = TaskboardWidget(board_path=board_path)
        async with app.run_test(size=size) as pilot:
            await pilot.pause()
            app.notify = lambda *a, **kw: None      # the toast names the theme
            app.set_theme(name)
            await pilot.pause()
            # capture a SETTLED frame: the theme's composition can resize the
            # hero, and Hero.show reads its own height — one redraw behind on
            # the switch frame. Settling is a CONDITION, not a pause count:
            # see settle() for why the count was wrong 1 run in 3.
            app.redraw()
            await settle(app, pilot, f"{name} @{size[0]}x{size[1]}")
            rows = screen_text(app)
            hero_r = app.query_one("#hero").region
            hero = "\n".join(rows[hero_r.y: hero_r.y + hero_r.height])
            board = masked_board(app, rows)
            # region GEOMETRY: composition is a language commitment (axis 6)
            geo = {wid: tuple(app.query_one(wid).region)
                   for wid in ("#hero", "#meter", "#ap")}
            geo["row0"] = rows[app.query_one("#ap").region.y]
            # the config screen: the component-dense surface (switch, slider,
            # cursor). No hero here — the whole frame must differ.
            await pilot.press("c")
            await pilot.pause()
            config = "\n".join(screen_text(app))
            return board, hero, config, geo
    finally:
        if mutate:
            if old is None:
                TH.THEMES[name].pop(mutate[0], None)
            else:
                TH.THEMES[name][mutate[0]] = old


def chan_lum(hx: str) -> float:
    """The weighted channel sum 0.2126R+0.7152G+0.0722B on the 0-255 sRGB
    values. A perceptual PROXY, not relative luminance (the WCAG transform
    lives in `lum()` inside main and is used where a ratio is claimed) —
    named for what it is, and used only to RANK the ink on one screen."""
    return sum(w * int(hx[i:i + 2], 16)
               for w, i in ((0.2126, 1), (0.7152, 3), (0.0722, 5)))


async def capture_styled(name: str, board_path: str, size=(118, 30),
                         mutate=None):
    """`capture()` returns text, and text cannot answer law 03 — "brightest"
    is a property of the STYLE, not the glyph. This returns the frame plus a
    per-cell (colour, bold) map and the board widget's own region, so the
    first-fixation checks measure the render instead of trusting the markup.

    Same guarded recipe as `capture()`: explicit fixture path, `settle()`."""
    from app import TaskboardWidget
    from kanban import KanbanBoard
    old = None
    if mutate:
        tok, val = mutate
        old = TH.THEMES[name].get(tok)
        TH.THEMES[name][tok] = val
    try:
        return await _styled(name, board_path, size)
    finally:
        if mutate:
            if old is None:
                TH.THEMES[name].pop(mutate[0], None)
            else:
                TH.THEMES[name][mutate[0]] = old


async def _styled(name, board_path, size):
    from app import TaskboardWidget
    from kanban import KanbanBoard
    app = TaskboardWidget(board_path=board_path)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        app.set_theme(name)
        await pilot.pause()
        app.redraw()
        await settle(app, pilot, f"{name} styled @{size[0]}x{size[1]}")
        rows = screen_text(app)
        # cell -> (hex colour, bold); only painted cells appear
        style: dict[tuple[int, int], tuple[str, bool]] = {}
        for y, strip in enumerate(app.screen._compositor.render_strips()):
            x = 0
            for seg in strip:
                st = seg.style
                col = st.color.triplet.hex if (st and st.color
                                               and st.color.triplet) else ""
                for i, ch in enumerate(seg.text):
                    if ch.strip():
                        style[(y, x + i)] = (col, bool(st and st.bold))
                x += len(seg.text)
        kb = app.query_one(KanbanBoard)
        return rows, style, tuple(kb.region)


async def capture_bg(name: str, board_path: str, size=(118, 30),
                     focus_card: bool = False, mutate=None):
    """`capture_styled` records a FOREGROUND colour and only for cells that
    carry a glyph. Neither answers a REVERSE-VIDEO question: a band's evidence
    is the ground it paints, and most of a band's cells are blank. This
    returns the frame plus a per-cell `(fg, bg)` map over EVERY cell, so
    "where does the band actually start and stop" is a measurement.

    Same guarded recipe as the others: explicit fixture path, `settle()`.
    `mutate` is the same (token, value) contract `capture()` carries, restored
    in a `finally` — a token left mutated poisons every capture after it."""
    old = None
    if mutate:
        tok, val = mutate
        old = TH.THEMES[name].get(tok)
        TH.THEMES[name][tok] = val
    try:
        return await _bg(name, board_path, size, focus_card)
    finally:
        if mutate:
            if old is None:
                TH.THEMES[name].pop(mutate[0], None)
            else:
                TH.THEMES[name][mutate[0]] = old


async def _bg(name, board_path, size, focus_card):
    from app import TaskboardWidget
    from kanban import KanbanBoard
    from kanban import TaskCard
    app = TaskboardWidget(board_path=board_path)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        app.set_theme(name)
        await pilot.pause()
        app.redraw()
        await settle(app, pilot, f"{name} bg @{size[0]}x{size[1]}")
        if focus_card:
            # focus is DRIVEN, not assumed: the app auto-focuses #hero, so a
            # selection law asserted on the default frame would be asserted on
            # a frame with no selection in it
            cards = list(app.query(TaskCard))
            if cards:
                cards[0].focus()
                await pilot.pause()
                await settle(app, pilot, f"{name} bg focused")
        rows = screen_text(app)
        cellmap: dict[tuple[int, int], tuple[str, str]] = {}
        for y, strip in enumerate(app.screen._compositor.render_strips()):
            x = 0
            for seg in strip:
                st = seg.style
                fg = (st.color.triplet.hex if (st and st.color
                                               and st.color.triplet) else "")
                bg = (st.bgcolor.triplet.hex if (st and st.bgcolor
                                                 and st.bgcolor.triplet)
                      else "")
                for i in range(len(seg.text)):
                    cellmap[(y, x + i)] = (fg, bg)
                x += len(seg.text)
        kb = app.query_one(KanbanBoard)
        return rows, cellmap, tuple(kb.region)


async def capture_ap_bg(name: str, board_path: str, size=(96, 30)):
    """The REAL app's aperture (`6`), with the same per-cell (fg, bg) map
    `capture_bg` builds, plus the `#hero` region.

    Why this seat exists, stated because it is the one place this suite leaves
    the widget-slice prototype: `taskboard/aperture.py` is what SHIPS, and its
    row budget, its composition and its panel are its own. Since pass 44 both
    seats render through `taskboard/hero.py` — the prototype's `Hero.show` is
    a nine-line adapter now — so a hero MECHANISM can be measured at either;
    what only this capture can answer for is the shipped SURFACE around it.
    `capture_bg` still answers for everything the board draws.

    Same guarded recipe as the others: explicit fixture path, `settle()`."""
    from taskboard.app import TaskboardApp
    app = TaskboardApp(board_path=board_path)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        await pilot.press("6")
        await pilot.pause()
        scr = app.screen
        scr.set_language(name)
        scr.engine.run_all()
        scr.redraw()
        await pilot.pause()
        await settle(app, pilot, f"aperture {name} @{size[0]}x{size[1]}")
        rows = screen_text(app)
        cellmap: dict[tuple[int, int], tuple[str, str]] = {}
        for y, strip in enumerate(app.screen._compositor.render_strips()):
            x = 0
            for seg in strip:
                st = seg.style
                fg = (st.color.triplet.hex if (st and st.color
                                               and st.color.triplet) else "")
                bg = (st.bgcolor.triplet.hex if (st and st.bgcolor
                                                 and st.bgcolor.triplet)
                      else "")
                for i in range(len(seg.text)):
                    cellmap[(y, x + i)] = (fg, bg)
                x += len(seg.text)
        return rows, cellmap, tuple(scr.query_one("#hero").region)


# -- THE LEGEND LAW ----------------------------------------------------------
# The user's defect, 2026-07-26: "I got lost with the bindings — now it's ctrl+q
# to quit and shift+binding to use the app, and there was no indication
# sustaining this." Measured, all three halves were true:
#   * `V` (cycle size) was the one binding that needed SHIFT.
#   * `q` quit from the aperture but was DEAD on both modals, where only the
#     priority ctrl+q survived — so the modals really did demand ctrl+q.
#   * the footer spent every description on group labels: `c ? V r t g q Widget`
#     showed seven keys and told the user what none of them did.
# The law those three collapse into, and what this section holds:
#   every key that fires an action on a surface is printed on that surface, and
#   every key printed on a surface fires there. No shown key needs shift.
LEGEND_SHIFT = re.compile(r"(^|,)(shift\+|[A-Z](,|$))")


def legend_row(rows: list[str]) -> str:
    """The footer is the last composited row of any of this app's screens."""
    return rows[-1]


def shown_bindings(node) -> list:
    from textual.binding import Binding
    return [b for b in node.BINDINGS if isinstance(b, Binding) and b.show]


def legend_tokens(row: str) -> list[str]:
    """The words on a footer row. The command-palette key is docked right
    behind a `vkey` border glyph that abuts it (`▏^p`), so the rail is stripped
    before splitting or every row would carry one phantom token."""
    return row.replace("▏", " ").split()


def active_shown(app) -> list:
    """The bindings the CURRENT screen actually offers and marks shown — the
    one source both halves of the law read. Taken from `active_bindings` rather
    than from any BINDINGS list, because that is what Textual resolved after
    modal shadowing and `check_action`, which is what the user meets."""
    return [ab.binding for ab in app.screen.active_bindings.values()
            if ab.binding.show]


def legend_vocabulary(bindings, extra=()) -> set[str]:
    """Every word a truthful legend may contain: the key displays, the words of
    the descriptions, the group labels. Anything else on the row is a legend
    entry with no binding behind it — which is the half of the law that a
    "does every key appear" check cannot see."""
    import app as APPMOD
    vocab = {"palette", "^p"}
    for b in bindings:
        vocab.update(APPMOD.key_of(b).split(" / "))
        vocab.update(b.description.split())
        if b.group:
            vocab.add(b.group.description)
    vocab.update(extra)
    return vocab


def legend_violations(row: str, bindings, extra=()) -> list[str]:
    """The words on the row that no binding accounts for. Returned rather than
    asserted so the failure detail NAMES the phantom key."""
    vocab = legend_vocabulary(bindings, extra)
    return [w for w in legend_tokens(row) if w not in vocab]


async def drive(lang: str, board_path: str, size=(118, 30)):
    """One app, one language, ready to be driven by REAL key presses.

    Returns the app and the pilot inside a context manager the caller closes;
    written as an async generator so every check below runs on a settled frame
    without each of them re-paying the boot."""
    from app import TaskboardWidget
    app = TaskboardWidget(board_path=board_path)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        app.set_theme(lang)
        await pilot.pause()
        app.redraw()
        await settle(app, pilot, f"legend {lang} @{size[0]}x{size[1]}")
        yield app, pilot


async def press(pilot, key: str, n: int = 4) -> None:
    """A key press plus enough pauses for the action AND the recompose the
    footer does on `bindings_updated_signal` — a legend read one frame early
    reads the previous screen's."""
    await pilot.press(key)
    for _ in range(n):
        await pilot.pause()


async def main():
    print("== PROBE SELF-CHECK (verify the instrument before the verdict)")
    check("grey() strips colour tags and keeps escaped brackets",
          grey("[#ff6600]x[/] \\[1] [bold]y[/]") == "x [1] y")
    base = kit_sig(LG.kit("naught"))
    check("kit_sig is stable (same language twice -> identical)",
          base == kit_sig(LG.kit("naught")))
    check("kit_sig carries no hex colour",
          not re.search(r"#[0-9a-f]{6}", base))
    # the guard that keeps the live board out of this suite must itself be
    # tested — an unfired guard is a comment
    try:
        await capture("naught")
        fired = False
    except ValueError:
        fired = True
    check("capture() refuses to probe the live board (the guard fires)", fired)

    print("\n== KIT LEVEL: greyscale pair test (all 8, colour stripped)")
    sigs = {n: kit_sig(LG.kit(n)) for n in TH.ORDER}
    for i, a in enumerate(TH.ORDER):
        for b in TH.ORDER[i + 1:]:
            check(f"{a} != {b}", sigs[a] != sigs[b])

    print("\n== KIT LEVEL: components — the 2-channel law and living spinners")
    for name in TH.ORDER:
        k = LG.kit(name)
        check(f"{name}: switch on/off differ in GREYSCALE (not colour-only)",
              grey(k.switch(True)) != grey(k.switch(False)))
        check(f"{name}: slider moves with the value",
              grey(k.slider(2, 0, 10, 10)) != grey(k.slider(8, 0, 10, 10)))
        frames = {grey(k.spinner(t)) for t in range(8)}
        check(f"{name}: spinner frames change across ticks", len(frames) > 1)
        check(f"{name}: tabs mark the active view",
              grey(k.tabs(["board", "lanes"], "board"))
              != grey(k.tabs(["board", "lanes"], "lanes")))
    spinners = {n: "".join(grey(LG.kit(n).spinner(t)) for t in range(8))
                for n in TH.ORDER}
    check("no two languages share a spinner",
          len(set(spinners.values())) == len(spinners))
    for name in TH.ORDER:
        k = LG.kit(name)
        fl = k.flip_frames(True)
        # GUARDED, and the fifty-ninth pass is why. This line indexed an
        # unchecked list for ten passes, which was safe only because nothing
        # could make `flip_frames` return an empty one. The motion engine can
        # — a mutant that shortens a transition to a single frame does — and
        # the IndexError killed the whole run at check 90, so the mutation
        # reported ZERO reds and looked like a suite that had nothing to say.
        # A dead run is not a green run and it is not a red one either.
        check(f"{name}: flip ends on the final state",
              bool(fl) and fl[-1] == k.switch(True))
        if name == "swiss":
            check("swiss: flip renounced (single frame, a decision)",
                  len(fl) == 1)
            check("swiss: icons renounced (the word is the icon)",
                  k.icon("deadline") == "")
        else:
            check(f"{name}: flip has intermediate frames", len(fl) >= 2)
            check(f"{name}: icons exist for the signal vocabulary",
                  all(k.icon(i) for i in ("deadline", "overdue", "blocked")))
        check(f"{name}: spark rises with the data",
              grey(k.spark([0, 0, 0, 0], 4)) != grey(k.spark([1, 5, 2, 9], 4)))
        # the PLOT and GAUGE (axis 7, second wave): levels and needle must
        # ride on SHAPE — greyscale the two states and they must differ
        p = k.plot([2, 5, 3, 7, 4, 8, 6, 9], 24, 4)
        check(f"{name}: plot is exactly h rows tall", len(p) == 4)
        check(f"{name}: plot responds to the data in greyscale",
              "\n".join(grey(r) for r in p)
              != "\n".join(grey(r) for r in k.plot([1] * 8, 24, 4)))
        check(f"{name}: gauge needle moves with the value",
              grey(k.gauge(2, 0, 10, 10)) != grey(k.gauge(8, 0, 10, 10)))
    plots = {n: "\n".join(grey(r) for r in
                          LG.kit(n).plot([2, 5, 3, 7, 4, 8, 6, 9], 24, 4))
             for n in TH.ORDER}
    check("no two languages share a plot",
          len(set(plots.values())) == len(TH.ORDER))
    gauges = {n: grey(LG.kit(n).gauge(7, 0, 10, 10)) for n in TH.ORDER}
    check("no two languages share a gauge",
          len(set(gauges.values())) == len(TH.ORDER))

    # =====================================================================
    print("\n== KIT LEVEL: THE COMPONENT CONTRACT — parts registry + states")
    # The track's thesis, stated so it can go red: a design language is a
    # component library, and a component library is a CONTRACT before it is a
    # look. Which parts exist is fixed for everyone; how each part is drawn is
    # the only thing a language may say. LVGL publishes that decomposition as
    # data, and it also publishes the failure this section exists to prevent:
    # EDITED — "focused AND the arrows now mutate the value" — is styled in 0
    # of 1848 sampled widgets, because on a touch surface it never happens. On
    # a keyboard surface it is the normal case, so every state here must
    # survive greyscale.
    CS = LG.COMPONENT_STATES
    WC = 12                                # the contract bench width

    def cells_of(k, comp, val, state=LG.DEFAULT, lo=0, hi=10, w=WC):
        return k.component_cells(comp, val, lo, hi, w, state)

    def shape(cells):
        """The render with colour REMOVED at the source — the cells carry
        their own tone, so greyscale here is a projection, not a regex."""
        return "".join(g for _, g, _ in cells)

    def knob_at(cells):
        for i, (p, _, _) in enumerate(cells):
            if p == "knob":
                return i
        return -1

    def diff_idx(a, b):
        return [i for i in range(min(len(a), len(b))) if a[i] != b[i]]

    def main_changed(a, b):
        """THE MECHANISM-INVARIANCE VIOLATION: a cell that is track in BOTH
        renders and changed anyway. Returned as indices rather than a bool so
        the failure names its own cells."""
        return [i for i in diff_idx(a, b)
                if a[i][0] == "main" and b[i][0] == "main"]

    # -- the registry itself ----------------------------------------------
    check("registry: slider declares exactly (main, indicator, knob)",
          LG.COMPONENT_PARTS["slider"] == ("main", "indicator", "knob"))
    check("registry: bar declares exactly (main, indicator)",
          LG.COMPONENT_PARTS["bar"] == ("main", "indicator"))
    check("registry: bar IS slider minus the knob — one missing part is the "
          "whole difference between operating a value and being told one",
          set(LG.COMPONENT_PARTS["slider"]) - set(LG.COMPONENT_PARTS["bar"])
          == {"knob"}
          and set(LG.COMPONENT_PARTS["bar"]) < set(LG.COMPONENT_PARTS["slider"]))
    check("registry: the state axis is LVGL's canonical six plus INVALID, "
          "in order — the seventh entry and the sixth CONTROL state, added "
          "by kits-learn-3 because a form screen had no seat in the contract "
          "and five languages invented the same red `!` to fill it",
          LG.STATES == ("default", "focused", "edited", "active", "checked",
                        "invalid", "disabled"))
    check("registry: a slider takes FOCUSED, EDITED and ACTIVE",
          all(s in CS["slider"] for s in (LG.FOCUSED, LG.EDITED, LG.ACTIVE)))
    check("registry: a bar takes NONE of them — no knob, no affordance of "
          "control, so no interactive state exists to be in",
          not any(s in CS["bar"] for s in (LG.FOCUSED, LG.EDITED, LG.ACTIVE)))
    check("registry: CHECKED reaches the CHECKABLE components and nothing "
          "else — the REGISTRY says so, not a comment",
          all(any(LG.is_checked(s) for s in v) == (n in LG.CHECKABLE)
              for n, v in CS.items()))
    check("registry: neither slider nor bar takes CHECKED — a value is not a "
          "boolean and the value family says so by not being CHECKABLE",
          not any(LG.is_checked(s)
                  for s in CS["slider"] + CS["bar"]))
    check("registry: every component keeps DEFAULT and DISABLED",
          all({LG.DEFAULT, LG.DISABLED} <= set(v) for v in CS.values()))

    LG.COMPONENT_PARTS["_probe_knobbed"] = ("main", "indicator", "knob")
    LG.COMPONENT_PARTS["_probe_flat"] = ("main", "indicator")
    try:
        check("control: the state set is DERIVED from the parts — a NEW "
              "component with a knob gets the interactive states with nothing "
              "hand-listed anywhere",
              LG.component_states("_probe_knobbed") == CS["slider"])
        check("control: ... and a new component WITHOUT one gets none of them. "
              "A hand-written state table cannot do this, which is the reason "
              "there isn't one",
              LG.component_states("_probe_flat") == CS["bar"])
    finally:
        del LG.COMPONENT_PARTS["_probe_knobbed"]
        del LG.COMPONENT_PARTS["_probe_flat"]

    # -- THE SWITCH: the registry entry, argued ---------------------------
    # The decision this pass had to make and could get wrong: does a switch
    # declare (main, knob) or (main, indicator, knob)? It declares THREE, and
    # the argument is the composer itself — run it with lo=0, hi=1 and the
    # terminal's conventional switch falls out with no special case. A switch
    # is a slider whose range is boolean, so its anatomy IS a range control's
    # anatomy. What actually differs is the RANGE, and the registry states
    # that as CHECKABLE rather than as a fourth part.
    check("registry: switch declares exactly (main, indicator, knob)",
          LG.COMPONENT_PARTS["switch"] == ("main", "indicator", "knob"))
    check("registry: switch declares the SAME parts as slider — the registry "
          "cannot tell them apart because on the axis it measures they ARE "
          "the same thing, and pretending otherwise would be a picture",
          LG.COMPONENT_PARTS["switch"] == LG.COMPONENT_PARTS["slider"])
    check("registry: switch is CHECKABLE and slider and bar are not — one "
          "registry fact, and it is what makes them different components",
          "switch" in LG.CHECKABLE
          and not {"slider", "bar"} & set(LG.CHECKABLE))
    check("registry: the switch's axis is the PRODUCT of its control block "
          "with the checked bit, not a hand list",
          CS["switch"]
          == (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE, LG.DISABLED,
              "checked", "checked+focused", "checked+active",
              "checked+disabled"),
          f"{CS['switch']}")
    check("registry: every checked state of the switch is a base state with "
          "the bit set — the two halves of the axis are the same block twice",
          tuple(LG.control_of(s) for s in CS["switch"] if LG.is_checked(s))
          == tuple(s for s in CS["switch"] if not LG.is_checked(s)))
    check("registry: a switch has NO EDITED state — EDITED means the arrows "
          "now RANGE through the value, and a boolean has no interior to "
          "range through; the press toggles at once, which is ACTIVE",
          LG.EDITED not in CS["switch"]
          and not any(LG.EDITED in s for s in CS["switch"]))
    check("registry: ... and the slider KEEPS it, so the removal is derived "
          "from CHECKABLE and not from the component's name",
          LG.EDITED in CS["slider"])
    check("registry: the switch still takes FOCUSED and ACTIVE — it has a "
          "knob, and the knob is the affordance of control",
          LG.FOCUSED in CS["switch"] and LG.ACTIVE in CS["switch"])
    check("registry: CHECKED|DISABLED and CHECKED|ACTIVE are FIRST-CLASS "
          "states, which is LVGL's own model and the reason the axis is a "
          "product rather than a sixth entry in a flat list",
          "checked+disabled" in CS["switch"]
          and "checked+active" in CS["switch"])

    # -- the state ALGEBRA: the bit is written in exactly one place --------
    check("state algebra: control_of strips the checked bit",
          LG.control_of("checked+focused") == LG.FOCUSED
          and LG.control_of("checked") == LG.DEFAULT
          and LG.control_of(LG.DISABLED) == LG.DISABLED)
    check("state algebra: with_checked SETS and CLEARS, and round-trips",
          LG.with_checked(LG.FOCUSED, True) == "checked+focused"
          and LG.with_checked("checked+focused", False) == LG.FOCUSED
          and LG.with_checked(LG.DEFAULT, True) == LG.CHECKED
          and LG.with_checked(LG.CHECKED, False) == LG.DEFAULT)
    check("state algebra: is_checked reads the bit and is not a substring "
          "match — `unchecked` would pass a substring test",
          LG.is_checked("checked+active") and not LG.is_checked(LG.ACTIVE)
          and not LG.is_checked("unchecked"))
    check("state algebra: the glyph chain tries the combination, then the "
          "CONTROL bit, then checked, then default — a focused switch must "
          "look focused whether it is on or off",
          LG.state_chain("checked+focused")
          == ("checked+focused", LG.FOCUSED, LG.CHECKED, LG.DEFAULT)
          and LG.state_chain(LG.FOCUSED) == (LG.FOCUSED, LG.DEFAULT))
    check("state algebra: every derived state resolves through the chain to "
          "a key the base table actually declares",
          all(any(k in LG.Kit.PART_GLYPHS["knob"] for k in LG.state_chain(s))
              for s in CS["switch"]))
    check("registry: checked_pairs is DERIVED from the axis and covers it "
          "exactly once — the gallery's four rows are eight states",
          [s for p in LG.checked_pairs("switch") for s in p]
          == list(CS["switch"][:4]) + list(CS["switch"][4:])
          or sorted(s for p in LG.checked_pairs("switch") for s in p)
          == sorted(CS["switch"]))

    LG.COMPONENT_PARTS["_probe_check"] = ("main", "indicator", "knob")
    _saved_checkable = LG.CHECKABLE
    LG.CHECKABLE = LG.CHECKABLE + ("_probe_check",)
    try:
        check("control: a NEW component declared CHECKABLE derives exactly "
              "the switch's axis — combinations included — with nothing "
              "hand-listed. A hand table cannot do this",
              LG.component_states("_probe_check") == CS["switch"])
        LG.CHECKABLE = _saved_checkable + ("_probe_check", "slider")
        check("control: declaring the SLIDER checkable takes its EDITED away "
              "and gives it the checked combinations — the derivation is "
              "reading CHECKABLE and not the component's name",
              LG.EDITED not in LG.component_states("slider")
              and "checked+focused" in LG.component_states("slider"))
    finally:
        LG.CHECKABLE = _saved_checkable
        del LG.COMPONENT_PARTS["_probe_check"]
    check("control: ... and the registry is put back — a control that leaks "
          "state into the suite behind it is worse than no control",
          LG.CHECKABLE == _saved_checkable
          and LG.component_states("slider") == CS["slider"]
          and "_probe_check" not in LG.COMPONENT_PARTS)

    # -- the VALUE MODEL: one seat, inverted scales included ---------------
    for cn in (4, 7, 12):
        check(f"value model: the ends are the ends ({cn} cells)",
              LG.value_pos(0, 0, 10, cn) == 0
              and LG.value_pos(10, 0, 10, cn) == cn - 1)
        check(f"value model: out-of-range CLAMPS — never wraps, never raises "
              f"({cn} cells)",
              LG.value_pos(-99, 0, 10, cn) == 0
              and LG.value_pos(99, 0, 10, cn) == cn - 1)
        check(f"value model: an INVERTED scale (min > max, LVGL's `_invert`) "
              f"runs the other way with NO branch — the span goes negative "
              f"and the fraction does the work ({cn} cells)",
              LG.value_pos(0, 10, 0, cn) == cn - 1
              and LG.value_pos(10, 10, 0, cn) == 0)
        check(f"value model: position -> value -> position is EXACT in all "
              f"four orientations ({cn} cells). The other direction quantizes, "
              f"and a round-trip check claiming otherwise would be lying about "
              f"what a cell can hold",
              all(LG.value_pos(LG.value_at(p, a, b, cn), a, b, cn) == p
                  for p in range(cn)
                  for a, b in ((0, 10), (10, 0), (-5, 5), (5, -5))))
        up = [LG.value_pos(v, 0, 10, cn) for v in range(11)]
        dn = [LG.value_pos(v, 10, 0, cn) for v in range(11)]
        check(f"value model: monotone UP on a normal scale and DOWN on an "
              f"inverted one, across the whole domain ({cn} cells)",
              all(x <= y for x, y in zip(up, up[1:]))
              and all(x >= y for x, y in zip(dn, dn[1:]))
              and up == dn[::-1])
    check("value model: a zero span never divides and never raises",
          LG.value_pos(3, 7, 7, 9) == 0 and LG.value_pos(-3, 7, 7, 1) == 0)

    LANG_SRC = (W / "taskboard" / "language.py").read_text(encoding="utf-8")
    PROTO = (W / "prototypes" / "widget_slice" / "app.py").read_text(
        encoding="utf-8")
    check("one seat: `value_pos` is defined exactly once",
          LANG_SRC.count("def value_pos(") == 1,
          f"{LANG_SRC.count('def value_pos(')} definitions")
    check("one seat: so is `slider` — nine languages used to carry their own "
          "copy of the arithmetic, each with its own off-by-one (`w`, `w-1`, "
          "`w-2`, `w//3`), which is the fork defect the hero was cured of twice",
          LANG_SRC.count("def slider(") == 1,
          f"{LANG_SRC.count('def slider(')} definitions")
    check("one seat: and so are `readbar` and the composer they both call",
          LANG_SRC.count("def readbar(") == 1
          and LANG_SRC.count("def component_cells(") == 1)
    check("one seat: the forked line is GONE — `span = max(1, hi - lo)` "
          "followed by a clamped round() was copied verbatim into every kit",
          "span = max(1, hi - lo)\n        n = max(0, min(w" not in LANG_SRC)
    check("one seat: ... and the law is not passing on a renamed string — the "
          "composer really does call the shared model",
          "n = value_pos(val, lo, hi, cells)" in LANG_SRC)
    check("one seat: the prototype CALLS the contract and owns no control of "
          "its own (a file that merely stopped drawing would pass the greps "
          "above and render nothing)",
          "KIT.slider(" in PROTO and "def slider(" not in PROTO
          and "k.readbar(" in PROTO)

    # -- per language ------------------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        cn = k.part_slots("slider", WC)
        # (a) PART COMPLETENESS
        for comp in ("slider", "bar"):
            declared = set(LG.COMPONENT_PARTS[comp])
            seen = set()
            for v in range(11):
                seen |= {p for p, _, _ in cells_of(k, comp, v)}
            check(f"{name}: {comp} draws only its declared parts "
                  f"{LG.COMPONENT_PARTS[comp]}",
                  seen <= declared, f"drew {sorted(seen)}")
            check(f"{name}: {comp} draws ALL of them somewhere in its domain "
                  f"(a part that never appears is a part in name only)",
                  seen == declared, f"drew {sorted(seen)}")
        knobs = {sum(1 for p, _, _ in cells_of(k, "slider", v) if p == "knob")
                 for v in range(11)}
        check(f"{name}: the slider carries EXACTLY ONE knob at every value "
              f"including both ends — one language's knob disappeared at zero",
              knobs == {1}, f"knob counts {sorted(knobs)}")
        check(f"{name}: the bar carries NONE at any value — a bar with a knob "
              f"is a control lying about being a readout",
              not any(p == "knob" for v in range(11)
                      for p, _, _ in cells_of(k, "bar", v)))
        sl, br = cells_of(k, "slider", 7), cells_of(k, "bar", 7)
        check(f"{name}: bar == slider minus the knob, cell for cell — the "
              f"knob's cell becomes indicator and nothing else moves",
              len(sl) == len(br)
              and all(b[0] == ("indicator" if a[0] == "knob" else a[0])
                      for a, b in zip(sl, br)))
        for st in CS["slider"]:
            gk = k.part_glyph("knob", st)
            check(f"{name}: the {st} knob differs in SHAPE from both the fill "
                  f"and the track — a knob drawn like the fill is not a knob, "
                  f"it is where two languages here had no knob at all",
                  gk != k.part_glyph("indicator", st)
                  and gk != k.part_glyph("main", st), repr(gk))
            check(f"{name}: the {st} indicator differs in SHAPE from the "
                  f"track. An extent separated from its range by hue alone is "
                  f"the colour-only defect one cell in — and it is what three "
                  f"of these languages were shipping",
                  k.part_glyph("indicator", st) != k.part_glyph("main", st),
                  repr(k.part_glyph("indicator", st)))

        # (b) MECHANISM INVARIANCE
        a = cells_of(k, "slider", LG.value_at(cn // 4, 0, 10, cn))
        b = cells_of(k, "slider", LG.value_at((3 * cn) // 4, 0, 10, cn))
        bad = main_changed(a, b)
        check(f"{name}: value 0.25 -> 0.75 changes ONLY indicator and knob "
              f"cells. The track is the MECHANISM: it states the range, and a "
              f"range does not move when the value does",
              not bad, f"track cells changed at {bad}" if bad else "")
        check(f"{name}: ... and something DID change (without this the line "
              f"above passes on a slider that never moves)", diff_idx(a, b))

        # (c) THE STATE LAWS, after colour is stripped
        g = {st: shape(cells_of(k, "slider", 5, st)) for st in CS["slider"]}
        check(f"{name}: all {len(CS['slider'])} slider states are pairwise "
              f"distinct AFTER COLOUR IS STRIPPED",
              len(set(g.values())) == len(CS["slider"]),
              f"{len(set(g.values()))} distinct of {len(CS['slider'])}")
        check(f"{name}: FOCUSED differs from DEFAULT on a non-colour channel",
              g[LG.FOCUSED] != g[LG.DEFAULT])
        check(f"{name}: EDITED differs from FOCUSED — this is the state the "
              f"touch corpus styles 0 times in 1848, and the one a keyboard "
              f"surface cannot do without: the arrows now change the VALUE",
              g[LG.EDITED] != g[LG.FOCUSED])
        check(f"{name}: ACTIVE differs from both (the momentary keypress; the "
              f"motion that rides it comes later, the STATE is here now)",
              g[LG.ACTIVE] not in (g[LG.EDITED], g[LG.FOCUSED]))
        check(f"{name}: DISABLED is SHAPE-marked, not merely dimmed",
              g[LG.DISABLED] != g[LG.DEFAULT])
        check(f"{name}: ... and dimmed as well — every part of a disabled "
              f"slider wears the dim tone. Two channels, both spent",
              {t for _, _, t in cells_of(k, "slider", 5, LG.DISABLED)}
              == {k["dim"]})
        gb = {st: shape(cells_of(k, "bar", 5, st)) for st in CS["bar"]}
        check(f"{name}: the bar's two states are distinct in greyscale too",
              len(set(gb.values())) == len(CS["bar"]))
        check(f"{name}: an out-of-contract state falls back to DEFAULT rather "
              f"than raising — a bar asked to be FOCUSED has no such state",
              shape(cells_of(k, "bar", 5, LG.FOCUSED)) == gb[LG.DEFAULT])

        # (d) THE ANTI-JIGGLE LAW
        widths = {len(shape(cells_of(k, "slider", v, st)))
                  for st in CS["slider"] for v in range(11)}
        check(f"{name}: the cell region is ONE width across every value and "
              f"every state — a control that resizes when you touch it is the "
              f"jiggle the dimensioned languages exist to prevent",
              len(widths) == 1, f"widths {sorted(widths)}")

        # (e) THE SHARED VALUE MODEL, measured on the render
        check(f"{name}: the knob lands where the SHARED model says, at every "
              f"cell of the scale — this is the behavioural half of `one "
              f"seat`, and it cannot rot the way a grep can",
              all(knob_at(cells_of(k, "slider",
                                   LG.value_at(i, 0, 10, cn))) == i
                  for i in range(cn)))
        check(f"{name}: an INVERTED scale mirrors it with no per-language "
              f"branch anywhere",
              all(knob_at(k.component_cells("slider",
                                            LG.value_at(i, 10, 0, cn),
                                            10, 0, WC)) == i
                  for i in range(cn)))

        # (f) SINGLE-WRITE PAINT (Bodmer T4)
        c0 = cells_of(k, "slider", LG.value_at(1, 0, 10, cn))
        c1 = cells_of(k, "slider", LG.value_at(2, 0, 10, cn))
        d = diff_idx(c0, c1)
        check(f"{name}: a one-step move writes ONE contiguous region holding "
              f"the old knob AND the new one — compose the whole region and "
              f"assign it once, never clear-then-draw (Bodmer T4)",
              d and set(d) <= {1, 2} and knob_at(c0) == 1 and knob_at(c1) == 2,
              f"diff {d}, knob {knob_at(c0)}->{knob_at(c1)}")

    sliders = {n: shape(cells_of(LG.kit(n), "slider", 5)) for n in TH.ORDER}
    check("no two languages draw the same slider in greyscale — the contract "
          "fixes WHICH parts exist precisely so HOW is free",
          len(set(sliders.values())) == len(TH.ORDER),
          f"{len(set(sliders.values()))} distinct of {len(TH.ORDER)}")

    # =====================================================================
    print("\n== KIT LEVEL: THE SWITCH — CHECKED enters the contract")
    # The first CHECKED-bearing component, and the test of whether the state
    # derivation generalises past the value family. Everything below reads
    # the registry; nothing restates it. Ten languages shipped a hand-drawn
    # switch and NINE OF TEN had no knob at all — the one thing a switch is,
    # a control whose grip MOVES, was the one thing the axis was not saying.
    SW = 3                                 # the switch bench width
    CTL = [c for c, _ in LG.checked_pairs("switch")]

    def swcells(k, on, state=LG.DEFAULT, w=SW):
        return k.component_cells("switch", None, 0, 1, w,
                                 LG.with_checked(state, on))

    for name in TH.ORDER:
        k = LG.kit(name)
        sn = k.part_slots("switch", SW)

        # (a) PART COMPLETENESS, boolean-flavoured. At either position ONE of
        # {main, indicator} has zero extent — that is what a two-position
        # range means, and it is the "collapse" the brief predicted. Over the
        # PAIR, all three declared parts must appear; a switch that never
        # draws its indicator has renounced a part, which is not a language's
        # to renounce (nine of them had renounced the knob).
        both = set(p for on in (0, 1) for p, _, _ in swcells(k, on))
        check(f"{name}: the switch draws all THREE declared parts across its "
              f"two positions — indicator when on, track when off, knob "
              f"always. A part is not a language's to renounce",
              both == set(LG.COMPONENT_PARTS["switch"]), f"{sorted(both)}")
        check(f"{name}: and at EITHER position exactly one of main/indicator "
              f"has zero extent — a boolean range has no interior, which is "
              f"the whole difference from the slider",
              all(len({p for p, _, _ in swcells(k, on)} & {"main",
                                                           "indicator"}) == 1
                  for on in (0, 1)))
        for st in CS["switch"]:
            check(f"{name}: exactly one knob in the {st} switch",
                  sum(1 for p, _, _ in
                      k.component_cells("switch", None, 0, 1, SW, st)
                      if p == "knob") == 1)

        # (b) THE HEADLINE: checked vs unchecked on SHAPE, not colour. It is
        # carried by the knob's POSITION, which the shared value model moves
        # for free — no language declares a CHECKED glyph and none needs to.
        for ctl in CTL:
            a, b = shape(swcells(k, 0, ctl)), shape(swcells(k, 1, ctl))
            check(f"{name}: checked vs unchecked differ in SHAPE at {ctl} — "
                  f"greyscale them and the reading survives",
                  a != b, f"{a!r} vs {b!r}")
            check(f"{name}: ... and it is the KNOB'S POSITION that carries "
                  f"it, at the two ENDS of a two-position range",
                  {knob_at(swcells(k, 0, ctl)),
                   knob_at(swcells(k, 1, ctl))} == {0, sn - 1},
                  f"{knob_at(swcells(k, 0, ctl))} -> "
                  f"{knob_at(swcells(k, 1, ctl))}")

        # (c) THE KNOB DOES NOT DRIFT. A switch whose grip wanders as the
        # control state changes is a switch you cannot read at a glance.
        for on in (0, 1):
            pos = {knob_at(swcells(k, on, ctl)) for ctl in CTL}
            check(f"{name}: the knob position is STABLE across every control "
                  f"state at {'on' if on else 'off'} — a drifting knob fails "
                  f"here even though every state would still look distinct",
                  len(pos) == 1, f"positions {sorted(pos)}")

        # (d) the state axis, pairwise, colour stripped — combinations too
        g = {st: shape(k.component_cells("switch", None, 0, 1, SW, st))
             for st in CS["switch"]}
        check(f"{name}: all {len(CS['switch'])} switch states are pairwise "
              f"distinct with colour REMOVED, combinations included",
              len(set(g.values())) == len(CS["switch"]),
              f"{len(set(g.values()))} distinct of {len(CS['switch'])}")
        # `in CS` is part of the CONDITION, not a guard around it: if the
        # registry ever stops declaring the combination, this law must go RED
        # rather than quietly skip. A skipped law is a law that cannot fail.
        check(f"{name}: checked+disabled reads as neither `checked` nor "
              f"`disabled` alone — a combination LVGL styles first-class and "
              f"a flat six-entry axis could not express",
              "checked+disabled" in CS["switch"]
              and g["checked+disabled"] != g[LG.CHECKED]
              and g["checked+disabled"] != g[LG.DISABLED])
        for st in CS["switch"]:
            gk = k.part_glyph("knob", st)
            check(f"{name}: the {st} knob differs in SHAPE from both the fill "
                  f"and the track",
                  gk != k.part_glyph("indicator", st)
                  and gk != k.part_glyph("main", st))
            check(f"{name}: the {st} indicator differs in SHAPE from the "
                  f"track — the two-channel law one cell in",
                  k.part_glyph("indicator", st) != k.part_glyph("main", st))
        for st in (LG.DISABLED, "checked+disabled"):
            rest = LG.with_checked(LG.DEFAULT, LG.is_checked(st))
            check(f"{name}: the {st} switch is shape-marked AND dimmed — two "
                  f"channels, both spent",
                  st in CS["switch"] and rest in CS["switch"]
                  and shape(k.component_cells("switch", None, 0, 1, SW, st))
                  != g[rest]
                  and {t for _, _, t in
                       k.component_cells("switch", None, 0, 1, SW, st)}
                  == {k["dim"]})

        # (e) ANTI-JIGGLE: one width across every state AND both positions,
        # printed word included — corgi, ledger and solari print one.
        widths = {len(grey(k.switch(bool(on), SW, st)))
                  for st in CTL for on in (0, 1)}
        check(f"{name}: the switch holds ONE width across every state and "
              f"both positions, printed word included",
              len(widths) == 1, f"widths {sorted(widths)}")
        if k.CHECK_WORDS:
            check(f"{name}: its two printed words are the same width — a word "
                  f"that changes length moves the row it sits in",
                  len(k.CHECK_WORDS[0]) == len(k.CHECK_WORDS[1]),
                  f"{k.CHECK_WORDS}")

        # (f) SINGLE-WRITE PAINT: the region is composed once and tiles
        # exactly, in every state — no clear-then-draw, no gaps.
        check(f"{name}: every state composes exactly {sn} slots — one write "
              f"of the whole region including its ground (Bodmer T4)",
              all(len(k.component_cells("switch", None, 0, 1, SW, st)) == sn
                  for st in CS["switch"]))

        # (g) the CHECKED bit cannot disagree with the knob. This is the one
        # thing a two-source design gets wrong, so it is asked directly.
        check(f"{name}: `switch(on)` and the state agree by CONSTRUCTION — "
              f"asking for a checked render at the off position is not "
              f"expressible, because the bit is written in one place",
              grey(k.switch(True, SW, LG.FOCUSED))
              == grey(k.switch(True, SW, "checked+focused"))
              and grey(k.switch(False, SW, "checked+focused"))
              == grey(k.switch(False, SW, LG.FOCUSED)))

        # (h) MOTION: the flip is derived, so its frames cannot be a picture
        # of a switch this language no longer draws.
        for on in (True, False):
            fl = [grey(f) for f in k.flip_frames(on, SW)]
            check(f"{name}: every flip frame ({'on' if on else 'off'}) is the "
                  f"same width as the resting switch — eight languages "
                  f"carried a hardcoded picture here and it went stale the "
                  f"instant the switch entered the registry",
                  bool(fl) and len({len(f) for f in fl}) == 1
                  and len(fl[0]) == len(grey(k.switch(on, SW))))
            check(f"{name}: the flip ends ON the state ({'on' if on else 'off'})",
                  bool(fl) and fl[-1] == grey(k.switch(on, SW)))
            check(f"{name}: no flip frame repeats — a repeated frame spends a "
                  f"tick showing nothing new",
                  len(set(fl)) == len(fl), f"{fl}")

        # (i) THE ACCENT LAWS OF PASS 48 STILL HOLD, on the new component.
        # Where a language spends its accent on the slider is where it must
        # spend it on the switch: same rule, same seat, no second opinion.
        for st in (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE, LG.DISABLED):
            sl = {p for p, _, t in cells_of(k, "slider", 5, st)
                  if t == k["accent"]}
            sw = {p for p, _, t in swcells(k, 1, st) if t == k["accent"]}
            check(f"{name}: the {st} switch spends the accent on exactly the "
                  f"parts its slider does — one tone rule, two components",
                  sl == sw, f"slider {sorted(sl)} vs switch {sorted(sw)}")

    switches = {n: "|".join(shape(swcells(LG.kit(n), on, st))
                            for st in CTL for on in (0, 1))
                for n in TH.ORDER}
    check("no two languages draw the same switch in greyscale — ten "
          "hand-drawn switches became ten glyph tables and stayed ten",
          len(set(switches.values())) == len(TH.ORDER),
          f"{len(set(switches.values()))} distinct of {len(TH.ORDER)}")

    # THE GALLERY FITS. Pass 48 warned that the next component would turn the
    # scrolling gallery box into a defect; the fix was to spend FOUR rows on
    # eight states instead of eight, and the width is MEASURED here rather
    # than assumed — that assumption is what wrapped the slider rows first.
    for name in TH.ORDER:
        k = LG.kit(name)
        rows = [f"{'switch' if i == 0 else '':<11}"
                + grey(k.switch(False, 3, ctl)) + "  "
                + grey(k.switch(True, 3, ctl))
                + f"   {LG.control_of(ctl)}"
                + ("  off·on" if i == 0 else "")
                for i, ctl in enumerate(CTL)]
        check(f"{name}: the gallery's switch block fits the 52-column box "
              f"without wrapping, and costs 4 rows for 8 states",
              len(rows) == 4 and max(len(r) for r in rows) <= 52,
              f"widest {max(len(r) for r in rows)}")

    # -- CONTROLS for the switch laws, driven red on purpose ---------------
    class _StuckKnob(LG.Kit):
        """A switch whose knob does not move: position taken from nothing."""
        PART_GLYPHS = {"main": {LG.DEFAULT: "─"},
                       "indicator": {LG.DEFAULT: "━"},
                       "knob": {LG.DEFAULT: "│", LG.FOCUSED: "┃"}}

        def component_cells(self, name, val, lo, hi, w=10, state=LG.DEFAULT):
            cells = super().component_cells(name, val, lo, hi, w, state)
            if name != "switch":
                return cells
            return [(("knob" if i == 0 else "main"),
                     self.part_glyph("knob" if i == 0 else "main", state),
                     self.part_tone("knob" if i == 0 else "main", state))
                    for i in range(len(cells))]

    sk = _StuckKnob("nord")
    check("control: a switch whose knob never moves reads IDENTICALLY checked "
          "and unchecked, and the shape law goes red",
          shape(swcells(sk, 0)) == shape(swcells(sk, 1)))
    check("control: ... and it also never draws its indicator, so the "
          "part-completeness law fires too — two laws, one defect, which is "
          "how you know they are not the same law twice",
          set(p for on in (0, 1) for p, _, _ in swcells(sk, on))
          != set(LG.COMPONENT_PARTS["switch"]))

    class _ColourChecked(LG.Kit):
        """Checked separated from unchecked by TONE alone — the defect the
        touch corpus ships and the one the greyscale law exists for."""
        PART_GLYPHS = {"main": {LG.DEFAULT: "─"},
                       "indicator": {LG.DEFAULT: "─"},
                       "knob": {LG.DEFAULT: "│"}}

    cc = _ColourChecked("nord")
    check("control: a language whose indicator is drawn like its track loses "
          "one of the switch's two shape signals, and the indicator-vs-track "
          "law goes red (the gap pass 48 found, now guarded on the switch)",
          cc.part_glyph("indicator", LG.DEFAULT)
          == cc.part_glyph("main", LG.DEFAULT))
    check("control: ... while the KNOB still moves, so the headline shape "
          "law survives — the two laws separate a weak switch from a broken "
          "one instead of collapsing into each other",
          shape(swcells(cc, 0)) != shape(swcells(cc, 1)))

    _saved_words = LG.Ledger.CHECK_WORDS
    LG.Ledger.CHECK_WORDS = ("off", "posted")
    try:
        lw = {len(grey(LG.kit("ledger").switch(bool(on), SW)))
              for on in (0, 1)}
        check("control: printed words of unequal length make the switch "
              "CHANGE WIDTH between its positions, and the anti-jiggle law "
              "goes red",
              len(lw) > 1, f"widths {sorted(lw)}")
    finally:
        LG.Ledger.CHECK_WORDS = _saved_words
    check("control: ... and the words are put back",
          LG.Ledger.CHECK_WORDS == ("open  ", "posted")
          and len({len(grey(LG.kit("ledger").switch(bool(on), SW)))
                   for on in (0, 1)}) == 1)
    # =====================================================================
    print("\n== KIT LEVEL: THE CHECKBOX — is CHECKABLE a registry fact, or "
          "was it co-designed with the switch's geometry?")
    # The question this component was chosen to answer. A switch is a slider
    # whose range is boolean: same three parts, same track, the checked bit
    # read as a POSITION. If CHECKABLE only worked because of that, then the
    # first checkable with NO extent — a box and a mark that appears rather
    # than travels — has to break it. Every law below is asked so that the
    # answer can be read off which seats had to change.
    CBS = CS["checkbox"]

    def cbcells(k, on, state=LG.DEFAULT):
        return k.component_cells("checkbox", None, 0, 1, 1,
                                 LG.with_checked(state, on))

    def knobs_in(cells):
        return [i for i, (p, _, _) in enumerate(cells) if p == "knob"]

    # -- (1) THE REGISTRY: what was declared, and what fell out of it -------
    check("registry: the checkbox declares TWO parts — a box and a mark — "
          "and NO indicator, because there is no extent between an origin "
          "and a mark",
          LG.COMPONENT_PARTS["checkbox"] == ("main", "knob")
          and "indicator" not in LG.COMPONENT_PARTS["checkbox"])
    check("registry: it is CHECKABLE, and that is the ONLY thing it and the "
          "switch were both told",
          "checkbox" in LG.CHECKABLE and "switch" in LG.CHECKABLE)
    check("registry: THE GENERALISATION — the checkbox's state axis is "
          "IDENTICAL to the switch's, eight states with the checked bit "
          "combining, derived from CHECKABLE with no edit at the derivation "
          "seat. Different anatomy, same axis: that is the fact",
          CBS == CS["switch"] and len(CBS) == 8, f"{CBS}")
    check("registry: ... and it has no EDITED either — a box has no interior "
          "to range through, which is CHECKABLE's second consequence "
          "arriving for a component that was never considered when it was "
          "written",
          LG.EDITED not in CBS and not any(LG.EDITED in s for s in CBS))
    check("registry: checked_pairs gives the checkbox the same four row "
          "units it gives the switch — the gallery seat generalises too",
          LG.checked_pairs("checkbox") == LG.checked_pairs("switch"))

    # -- (2) THE SOURCE-LEVEL LAW (pass 44's discipline): a shared seat is
    # only shared if the CODE has no component name in it. A derivation that
    # says `if name == "switch"` passes every behavioural law above and is
    # still a special case wearing a contract's clothes.
    def code_of(fn):
        """The function's CODE: docstring and comment lines removed, because
        prose is allowed to name examples and code is not."""
        src = inspect.getsource(fn)
        if fn.__doc__:
            src = src.replace(fn.__doc__, "")
        return "\n".join(ln for ln in src.splitlines()
                         if not ln.strip().startswith("#"))

    NAMES = tuple(LG.COMPONENT_PARTS)
    for fn in (LG.component_states, LG.checked_pairs, LG.control_of,
               LG.with_checked, LG.is_checked, LG.bool_value, LG.state_chain):
        hits = [n for n in NAMES if f'"{n}"' in code_of(fn)
                or f"'{n}'" in code_of(fn)]
        check(f"source: `{fn.__name__}` names NO component in its code — the "
              f"state axis is derived from the registry, so the checkbox "
              f"inherited it rather than being granted it",
              not hits, f"names {hits}")
    for fn in (LG.Kit.component_cells, LG.Kit.part_slots, LG.Kit.comp_chrome,
               LG.Kit._component, LG.Kit.part_glyph, LG.Kit.part_key):
        hits = [n for n in NAMES if f'"{n}"' in code_of(fn)
                or f"'{n}'" in code_of(fn)]
        check(f"source: `Kit.{fn.__name__}` names NO component in its code "
              f"either — the composer grew a second ANATOMY (extent / no "
              f"extent), not a second component. One seat per decision",
              not hits, f"names {hits}")
    check("source: and the branch it grew is on the REGISTRY — the composer "
          "asks whether an indicator is declared, which is a fact about "
          "parts, not a fact about who is asking",
          '"indicator" in parts' in code_of(LG.Kit.component_cells)
          and '"indicator" not in COMPONENT_PARTS[name]'
          in code_of(LG.Kit.part_slots))

    # -- (3) NO EXTENT means no cells to spend and no ends to fix ----------
    for name in TH.ORDER:
        k = LG.kit(name)
        check(f"{name}: the checkbox is ONE slot at every width a caller "
              f"could ask for — cells are what an EXTENT spends, and a mark "
              f"needs a seat, not a run",
              {k.part_slots("checkbox", w) for w in (1, 3, 8, 20)} == {1},
              f"{sorted({k.part_slots('checkbox', w) for w in (1, 3, 8, 20)})}")
        check(f"{name}: and it takes NO chrome — chrome fixes the ends of a "
              f"track, and there is no track. industrial and blueprint would "
              f"otherwise double-box their own boxes",
              k.comp_chrome("checkbox") == ("", ""))
        check(f"{name}: while its slider KEEPS the chrome it declares — the "
              f"gate is the registry, not a blanket removal",
              k.comp_chrome("slider") == k.COMP_CHROME)

    # -- (4) PER LANGUAGE: the mark, the box, and the two channels ---------
    for name in TH.ORDER:
        k = LG.kit(name)

        check(f"{name}: declares its OWN checkbox glyphs for both parts — a "
              f"box drawn with the slider's track glyph is a picture of a "
              f"slider, and the scoped seat is what makes that expressible",
              k.part_key("checkbox", "main") == "checkbox.main"
              and k.part_key("checkbox", "knob") == "checkbox.knob")

        # (a) PART COMPLETENESS, mark-flavoured — and it is a DIFFERENT law
        # from the switch's. A switch shows its knob always and collapses an
        # extent; a checkbox has no extent to collapse, so what it collapses
        # is the MARK ITSELF. Unchecked: zero knobs. Checked: exactly one.
        for st in CBS:
            cells = k.component_cells("checkbox", None, 0, 1, 1, st)
            want = 1 if LG.is_checked(st) else 0
            check(f"{name}: the {st} checkbox draws {want} mark — presence "
                  f"IS the reading, where the switch's reading is position",
                  len(knobs_in(cells)) == want)
            check(f"{name}: ... and never an indicator, in any state — a part "
                  f"it does not declare is a part it cannot draw",
                  not any(p == "indicator" for p, _, _ in cells))
        both = {p for on in (0, 1) for p, _, _ in cbcells(k, on)}
        check(f"{name}: across the pair BOTH declared parts appear — the "
              f"same 'zero extent at an instant, whole over the pair' the "
              f"switch's indicator taught, now with the knob doing it",
              both == set(LG.COMPONENT_PARTS["checkbox"]), f"{sorted(both)}")

        # (b) THE HEADLINE: shape, never colour alone.
        for ctl in CTL:
            a, b = shape(cbcells(k, 0, ctl)), shape(cbcells(k, 1, ctl))
            check(f"{name}: checked vs unchecked differ in SHAPE at {ctl} — "
                  f"greyscale it and the reading survives",
                  a != b, f"{a!r} vs {b!r}")

        # (c) THE MARK IS IN THE BOX. A mark that escapes its main is a mark
        # standing beside a control, not in it. Width equality is the clause
        # every language can answer; the FRAME clause is only expressible
        # where a language's box has an interior, and the count of languages
        # it is non-vacuous for is printed rather than assumed.
        framed = 0
        for st in CBS:
            mg = k.part_glyph("main", st, "checkbox")
            kg = k.part_glyph("knob", st, "checkbox")
            check(f"{name}: the {st} mark occupies exactly the box's span — "
                  f"a mark that grows the control has escaped it",
                  len(mg) == len(kg), f"{mg!r} vs {kg!r}")
            if len(mg) >= 3:
                framed += 1
                check(f"{name}: ... and the box SURVIVES the mark at {st} — "
                      f"first and last cell unchanged, the difference "
                      f"strictly interior",
                      mg[0] == kg[0] and mg[-1] == kg[-1]
                      and mg[1:-1] != kg[1:-1], f"{mg!r} vs {kg!r}")
        check(f"{name}: the containment clause is {'non-vacuous' if framed else 'SPAN-ONLY'} "
              f"here ({framed} of {len(CBS)} states carry a framed box) — "
              f"a one-cell box has no interior to keep a mark inside of, and "
              f"saying so is better than a law that cannot fail",
              framed in (0, len(CBS)), f"framed {framed}")

        # (d) the state axis, pairwise, colour stripped
        g = {st: shape(k.component_cells("checkbox", None, 0, 1, 1, st))
             for st in CBS}
        check(f"{name}: all {len(CBS)} checkbox states are pairwise distinct "
              f"with colour REMOVED, combinations included",
              len(set(g.values())) == len(CBS),
              f"{len(set(g.values()))} distinct of {len(CBS)}")
        check(f"{name}: checked+disabled reads as neither `checked` nor "
              f"`disabled` alone — the product axis is visible, not just "
              f"declared",
              "checked+disabled" in CBS
              and g["checked+disabled"] != g[LG.CHECKED]
              and g["checked+disabled"] != g[LG.DISABLED])
        for st in (LG.DISABLED, "checked+disabled"):
            check(f"{name}: the {st} checkbox is shape-marked AND dimmed — "
                  f"two channels, both spent",
                  st in CBS
                  and {t for _, _, t in
                       k.component_cells("checkbox", None, 0, 1, 1, st)}
                  == {k["dim"]})

        # (e) NO JIGGLE ACROSS THE PAIR: one width for every state and both
        # bits, printed word included — and the mark does not TRAVEL, which
        # is the checkbox's version of the switch's stable-knob law.
        widths = {len(grey(k.checkbox(bool(on), st)))
                  for st in CTL for on in (0, 1)}
        check(f"{name}: the checkbox holds ONE width across every state and "
              f"both bits, printed word included",
              len(widths) == 1, f"widths {sorted(widths)}")
        # TUPLES, not `[0]`. Indexing the first knob is how this law CRASHED
        # under the first mutation instead of going red — a checkbox with no
        # checked bit draws no mark, and a law that raises reports nothing at
        # all. The presence of the seat is part of the CONDITION now.
        seats = {tuple(knobs_in(cbcells(k, 1, ctl))) for ctl in CTL}
        check(f"{name}: the mark does not TRAVEL — one seat in every control "
              f"state, and it is THERE in every one. A checkbox whose mark "
              f"wanders is a switch nobody asked for",
              seats == {(0,)}, f"seats {sorted(seats)}")

        # (f) SINGLE-WRITE PAINT, and the bit written in one place.
        check(f"{name}: every state composes exactly one slot — one write of "
              f"the whole region including its ground (Bodmer T4)",
              all(len(k.component_cells("checkbox", None, 0, 1, 1, st)) == 1
                  for st in CBS))
        check(f"{name}: `checkbox(on)` and the state agree by CONSTRUCTION — "
              f"a checked render with an empty box is not expressible, "
              f"because `with_checked` is the only writer",
              grey(k.checkbox(True, LG.FOCUSED))
              == grey(k.checkbox(True, "checked+focused"))
              and grey(k.checkbox(False, "checked+focused"))
              == grey(k.checkbox(False, LG.FOCUSED)))

        # (g) the ACCENT laws of pass 48, asked a third time. Where a
        # language spends its accent on the slider is where it spends it
        # here — restricted to the parts a checkbox HAS.
        for st in (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE, LG.DISABLED):
            sl = {p for p, _, t in cells_of(k, "slider", 5, st)
                  if t == k["accent"]} & {"main", "knob"}
            cb = {p for p, _, t in
                  k.component_cells("checkbox", None, 0, 1, 1,
                                    LG.with_checked(st, True))
                  if t == k["accent"]}
            check(f"{name}: the {st} checkbox spends the accent on exactly "
                  f"the parts its slider does — one tone rule, three "
                  f"components, no second opinion",
                  sl == cb, f"slider {sorted(sl)} vs checkbox {sorted(cb)}")

        # (h) PROBE DISCIPLINE: the projection this whole section measures
        # with must agree with rich on every string it is handed. This is
        # the law that would have caught `[ ]` measuring zero cells wide.
        check(f"{name}: the greyscale projection agrees with rich's own "
              f"parser on every checkbox string — literal `[ ]` is not a "
              f"tag, and an instrument that thinks it is measures an "
              f"invisible control",
              all(grey_is_rich(k.checkbox(bool(on), st))
                  for st in CTL for on in (0, 1)))

    boxes = {n: "|".join(shape(cbcells(LG.kit(n), on, st))
                         for st in CTL for on in (0, 1))
             for n in TH.ORDER}
    check("no two languages draw the same checkbox in greyscale — the "
          "contract fixes WHICH parts exist precisely so HOW is free",
          len(set(boxes.values())) == len(TH.ORDER),
          f"{len(set(boxes.values()))} distinct of {len(TH.ORDER)}")
    for n in TH.ORDER:
        k = LG.kit(n)
        check(f"{n}: its checkbox is not its switch — same axis, different "
              f"anatomy, and the render says so",
              grey(k.checkbox(True)) != grey(k.switch(True, SW))
              and grey(k.checkbox(False)) != grey(k.switch(False, SW)))

    # -- THE GALLERY DECISION, and it is a DECISION this time --------------
    # Passes 48 and 49 both deferred the layout question. It is answered here
    # by asking the SCREEN'S OWN seat for its rows rather than rebuilding the
    # arithmetic in the oracle — `checkable_block` is read by the gallery and
    # by this check, so "the block fits" cannot be true of a block the user
    # never sees.
    GAL_W = 52                                # the box's interior, measured
    for name in TH.ORDER:
        k = LG.kit(name)
        block = checkable_block(k, GAL_W)
        check(f"{name}: the gallery's checkable block FITS the {GAL_W}-column "
              f"box without wrapping — a wrapped row puts the caption under "
              f"the wrong control",
              max(len(grey(r)) for r in block) <= GAL_W,
              f"widest {max(len(grey(r)) for r in block)}, "
              f"{len(block)} rows")
        check(f"{name}: ... and it PAIRS when there is room — at 200 columns "
              f"two components cost five rows, not eight",
              len(checkable_block(k, 200)) == 5)
        check(f"{name}: ... and STACKS when there is not — at 20 columns it "
              f"reflows to eight rows rather than truncating. The choice is "
              f"the MEASUREMENT's, which is why it is right for a language "
              f"nobody measured by hand",
              len(checkable_block(k, 20)) == 8)
        for w_ in (GAL_W, 200, 20):
            body = "\n".join(grey(r) for r in checkable_block(k, w_))
            check(f"{name}: the block at w={w_} shows all {len(CBS)} states "
                  f"of BOTH checkables — a layout that fits by dropping a "
                  f"state is not a layout, it is a truncation",
                  all(grey(k.switch(LG.is_checked(st), SW, st)) in body
                      and grey(k.checkbox(LG.is_checked(st), st)) in body
                      for st in CBS))

    # -- CONTROLS for the checkbox laws, driven red on purpose -------------
    class _EscapedMark(LG.Kit):
        """A mark wider than its box — the failure the containment law is
        for: a tick standing BESIDE a control instead of in it."""
        PART_GLYPHS = dict(LG.Kit.PART_GLYPHS,
                           **{"checkbox.main": {LG.DEFAULT: "[ ]"},
                              "checkbox.knob": {LG.DEFAULT: "[x]!"}})

    em = _EscapedMark("nord")
    check("control: a mark wider than its box breaks containment AND width, "
          "and both clauses go red",
          len(em.part_glyph("main", LG.DEFAULT, "checkbox"))
          != len(em.part_glyph("knob", LG.DEFAULT, "checkbox"))
          and len({len(grey(em.checkbox(bool(on)))) for on in (0, 1)}) > 1)

    class _ColourMark(LG.Kit):
        """Checked and unchecked drawn with the SAME glyph — separated by
        tone alone, which is the defect the greyscale law exists for."""
        PART_GLYPHS = dict(LG.Kit.PART_GLYPHS,
                           **{"checkbox.main": {LG.DEFAULT: "[o]"},
                              "checkbox.knob": {LG.DEFAULT: "[o]"}})

    cm = _ColourMark("nord")
    check("control: a checkbox whose mark is its box reads IDENTICALLY "
          "checked and unchecked, and the shape law goes red",
          shape(cbcells(cm, 0)) == shape(cbcells(cm, 1)))
    check("control: ... while its TONES still differ, which is how such a "
          "defect passes a colour-blind eye and would pass a colour-blind "
          "check that only asked about tone",
          {t for _, _, t in cbcells(cm, 0)}
          != {t for _, _, t in cbcells(cm, 1)})

    class _AlwaysMarked(LG.Kit):
        """A mark that ignores the bit — the checkbox equivalent of pass
        49's pinned knob."""

        def component_cells(self, name, val, lo, hi, w=10, state=LG.DEFAULT):
            cells = super().component_cells(name, val, lo, hi, w, state)
            if name != "checkbox":
                return cells
            return [("knob", self.part_glyph("knob", state, name),
                     self.part_tone("knob", state)) for _ in cells]

    am = _AlwaysMarked("nord")
    check("control: a checkbox that is always marked draws a knob in an "
          "UNCHECKED state, so the presence law fires",
          len(knobs_in(cbcells(am, 0))) == 1)
    check("control: ... and it never draws its box, so part-completeness "
          "fires too — two laws, one defect, which is how you know they are "
          "not the same law twice",
          {p for on in (0, 1) for p, _, _ in cbcells(am, on)}
          != set(LG.COMPONENT_PARTS["checkbox"]))

    # =====================================================================
    print("\n== KIT LEVEL: THE RADIO — can this contract hold a state whose "
          "SCOPE is larger than one component?")
    # Every component so far answers from its own value. A radio item is
    # `checked` because a SIBLING is not, so the question is whether the
    # invariant "exactly one of these is set" can live at one seat and be
    # law — and whether `with_checked` survives contact with a fact no single
    # component owns. The anatomy is deliberately the checkbox's, so anything
    # that had to change is the GROUP talking and nothing else.
    RDS = CS["radio"]
    OPTS = ("lo", "mid", "hi")

    def gstates(n=3, sel=1, ctl=LG.DEFAULT, foc=None):
        return LG.group_states(n, sel, ctl, foc)

    def n_checked(sts):
        """The invariant, as ONE predicate — read by the laws AND by the
        controls, so a control that goes red proves the law would have."""
        return sum(1 for s in sts if LG.is_checked(s))

    def item_cells(k, st):
        return k.component_cells("radio", None, 0, 1, 1, st)

    def marks(k, sts):
        return sum(1 for st in sts for p, _, _ in item_cells(k, st)
                   if p == "knob")

    def raises(fn, *a):
        try:
            fn(*a)
        except ValueError:
            return True
        except Exception:
            return False
        return False

    # -- (1) THE REGISTRY still cannot tell it from a checkbox, correctly ---
    check("registry: a radio ITEM declares exactly what a checkbox does — a "
          "well and a mark, no indicator. The registry describes ONE "
          "component's parts, and 'my sibling is set' is not a part",
          LG.COMPONENT_PARTS["radio"] == LG.COMPONENT_PARTS["checkbox"]
          == ("main", "knob"))
    check("registry: it is CHECKABLE, and the axis arrived unchanged for the "
          "THIRD component — eight states, the checked bit combining",
          "radio" in LG.CHECKABLE and RDS == CS["checkbox"] == CS["switch"]
          and len(RDS) == 8, f"{RDS}")
    check("registry: ... and no EDITED here either — the third component to "
          "inherit CHECKABLE's second consequence without being named",
          LG.EDITED not in RDS and not any(LG.EDITED in s for s in RDS))
    check("registry: checked_pairs gives the radio the same four row units",
          LG.checked_pairs("radio") == LG.checked_pairs("checkbox"))

    # -- (2) SOURCE: the derivation did not move, and the NEW seat is
    # component-blind too. `group_states` is where the scope lives; if it
    # named a component it would be a radio feature, not a contract one — a
    # segmented control and a tab bar are the same fact about siblings.
    for fn in (LG.group_states,):
        hits = [n for n in NAMES if f'"{n}"' in code_of(fn)
                or f"'{n}'" in code_of(fn)]
        check(f"source: `{fn.__name__}` names NO component — the group scope "
              f"is a fact about SIBLINGS, not about radios", not hits,
              f"names {hits}")
    for fn in (LG.Kit._component_body, LG.Kit.check_tone):
        hits = [n for n in NAMES if f'"{n}"' in code_of(fn)
                or f"'{n}'" in code_of(fn)]
        check(f"source: `Kit.{fn.__name__}` names NO component — the two "
              f"seats the radio split out of `_component` stayed shared",
              not hits, f"names {hits}")
    check("source: the BIT IS STILL WRITTEN BY `with_checked` — the writer of "
          "the checked bit did not change, its AUTHOR moved. That is the "
          "whole claim about the group scope, and it is read off the code",
          "with_checked(" in code_of(LG.group_states))
    check("source: and `radio_items` derives every item's state from "
          "`group_states` rather than from an argument — there is no `on` "
          "parameter anywhere in the radio's API, which is what makes a "
          "desynchronised group unreachable rather than merely unlikely",
          "group_states(" in code_of(LG.Kit.radio_items)
          and "on" not in inspect.signature(LG.Kit.radio_items).parameters,
          f"{list(inspect.signature(LG.Kit.radio_items).parameters)}")
    check("source: ... while `switch` and `checkbox` DO take one, which is "
          "the contrast the group scope is measured against",
          all("on" in inspect.signature(f).parameters
              for f in (LG.Kit.switch, LG.Kit.checkbox)))

    # -- (3) THE INVARIANT: exactly one, and the other two counts are not
    # merely wrong, they are UNREPRESENTABLE.
    for n in range(1, 7):
        for sel in range(n):
            for ctl in CTL:
                for foc in [None] + list(range(n)):
                    sts = LG.group_states(n, sel, ctl, foc)
                    check(f"group(n={n}, sel={sel}, {ctl}, focus={foc}): "
                          f"EXACTLY ONE item carries the checked bit, and it "
                          f"is the selected one",
                          len(sts) == n and n_checked(sts) == 1
                          and LG.is_checked(sts[sel]))
    check("group: a selection outside the set RAISES rather than clamping — "
          "zero marks is the one way to ask for an invalid group and it is "
          "refused at the seat. A clamp would silently move the user's choice",
          all(raises(LG.group_states, 3, s) for s in (-1, 3, 4, 99)))
    check("group: ... and a group with no items is refused too",
          raises(LG.group_states, 0, 0))
    check("group: a DISABLED group holds its selection and drops its cursor — "
          "a dead control does not hold focus, and the checked item is still "
          "the checked item",
          LG.group_states(3, 2, LG.DISABLED, 0)
          == (LG.DISABLED, LG.DISABLED, "checked+disabled"))
    check("group: focus is INDEPENDENT of selection — moving the cursor over "
          "every item never moves the mark",
          all(LG.group_states(4, 1, LG.FOCUSED, f)[1] == "checked"
              or f == 1 for f in range(4))
          and all(n_checked(LG.group_states(4, 1, LG.FOCUSED, f)) == 1
                  for f in range(4)))

    # -- (3b) CONTROLS: the invariant law driven red, both ways -------------
    check("control: a hand-built group with TWO items set fails the same "
          "predicate the laws above pass — the invariant is a measurement, "
          "not a description",
          n_checked((LG.CHECKED, "checked+focused", LG.DEFAULT)) == 2)
    check("control: ... and one with NONE set fails it too, so the law has "
          "teeth on both sides of 'exactly one'",
          n_checked((LG.DEFAULT, LG.FOCUSED, LG.DISABLED)) == 0)
    check("control: and a language RENDERS those broken groups without "
          "complaint — two marks and zero marks both draw. The invariant is "
          "kept by the seat, never by the drawing, which is exactly why it "
          "has to live where a caller cannot reach it",
          marks(LG.kit("nord"), (LG.CHECKED, "checked+focused", LG.DEFAULT))
          == 2
          and marks(LG.kit("nord"), (LG.DEFAULT, LG.FOCUSED, LG.DISABLED))
          == 0)

    # -- (4) PER LANGUAGE ---------------------------------------------------
    r_framed = {}
    for name in TH.ORDER:
        k = LG.kit(name)

        check(f"{name}: declares its OWN radio glyphs for both parts — a "
              f"radio drawn with the checkbox's box is a checkbox",
              k.part_key("radio", "main") == "radio.main"
              and k.part_key("radio", "knob") == "radio.knob")

        # (a) the mark is the selection, and there is exactly ONE of it on
        # the row — read off the RENDER, not off the states.
        for sel in range(len(OPTS)):
            for ctl in CTL:
                for foc in (None, 0, 1, 2):
                    sts = gstates(len(OPTS), sel, ctl, foc)
                    check(f"{name}: the rendered group draws ONE mark "
                          f"(sel={sel}, {ctl}, focus={foc}) — the invariant "
                          f"survives the composer, not just the derivation",
                          marks(k, sts) == 1)
                    check(f"{name}: ... and it is on item {sel}, never on the "
                          f"cursor's item",
                          [i for i, st in enumerate(sts)
                           if any(p == "knob" for p, _, _
                                  in item_cells(k, st))] == [sel])

        # (a2) THE SAME COUNT, READ OFF THE SEAT THE SCREEN CALLS. The laws
        # above compose `group_states` and `component_cells` themselves,
        # which measures the derivation and NOT `radio_items` — and a
        # mutation that made `radio_items` ignore the group entirely was
        # caught by exactly one source-level law because of it (PENDING, the
        # fifty-first pass, M8). This one strips the rendered item strings
        # and counts wells against marks, so the thing the config screen and
        # the gallery actually call is the thing under test.
        wells = {k.part_glyph("main", st, "radio") for st in RDS}
        markg = {k.part_glyph("knob", st, "radio") for st in RDS}
        check(f"{name}: no well glyph is also a mark glyph — the two-channel "
              f"law restated at the group, and the precondition that makes "
              f"counting marks off a render meaningful at all",
              not (wells & markg), f"shared {sorted(wells & markg)}")
        span = len(k.part_glyph("main", LG.DEFAULT, "radio"))
        for sel in range(len(OPTS)):
            for ctl in CTL:
                for foc in (None, 0, 2):
                    heads = [grey(it)[:span]
                             for it in k.radio_items(OPTS, sel, ctl, foc)]
                    check(f"{name}: the RENDERED items carry exactly one mark "
                          f"and it is on item {sel} ({ctl}, focus={foc}) — "
                          f"measured on `radio_items`, the seat the app calls",
                          [i for i, h in enumerate(heads) if h in markg]
                          == [sel]
                          and all(h in wells | markg for h in heads),
                          f"{heads}")

        # (b) THE HEADLINE OF THIS INCREMENT: the cursor and the choice are
        # different items, both on screen, both readable with colour gone.
        for ctl in (LG.FOCUSED, LG.ACTIVE):
            sts = gstates(3, RADIO_SEL, ctl, RADIO_FOCUS)
            sh = [shape(item_cells(k, st)) for st in sts]
            check(f"{name}: at {ctl} the FOCUSED item and the CHECKED item "
                  f"are visibly different things — greyscale it and the "
                  f"cursor is still not the choice",
                  sh[RADIO_FOCUS] != sh[RADIO_SEL], f"{sh}")
            check(f"{name}: ... and the focused item is distinct from its "
                  f"UNTOUCHED sibling too, or the cursor is invisible and "
                  f"only the mark is doing any work",
                  sh[RADIO_FOCUS] != sh[0], f"{sh}")
            check(f"{name}: ... and the checked item is distinct from that "
                  f"sibling as well — three items, three readings, one row",
                  sh[RADIO_SEL] != sh[0], f"{sh}")
        rest = gstates(3, RADIO_SEL, LG.DEFAULT, RADIO_FOCUS)
        check(f"{name}: a group AT REST draws no cursor — the untouched "
              f"siblings are identical, which is what makes the focused "
              f"reading above a signal rather than a decoration",
              shape(item_cells(k, rest[0])) == shape(item_cells(k, rest[2])))
        dead = gstates(3, RADIO_SEL, LG.DISABLED, RADIO_FOCUS)
        check(f"{name}: a DISABLED group draws no cursor either, and every "
              f"item is dimmed — two channels on the whole set",
              shape(item_cells(k, dead[0])) == shape(item_cells(k, dead[2]))
              and {t for st in dead for _, _, t in item_cells(k, st)}
              == {k["dim"]})

        # (c) IT IS NOT A CHECKBOX. LVGL's one constraint on this component
        # (COMPONENTS.md: "distinct from switch: N-of-M vs on/off"), asked at
        # every control state and then asked of the whole signature.
        framed = 0
        for st in RDS:
            mg = k.part_glyph("main", st, "radio")
            kg = k.part_glyph("knob", st, "radio")
            cb = (k.part_glyph("main", st, "checkbox"),
                  k.part_glyph("knob", st, "checkbox"))
            check(f"{name}: the {st} radio's (well, mark) is not the "
                  f"checkbox's (box, mark) — a set you choose from must not "
                  f"read as a box you tick",
                  (mg, kg) != cb, f"radio {(mg, kg)} vs checkbox {cb}")
            check(f"{name}: the {st} mark occupies exactly the well's span",
                  len(mg) == len(kg), f"{mg!r} vs {kg!r}")
            if len(mg) >= 3:
                framed += 1
                check(f"{name}: ... and the well SURVIVES the mark at {st}",
                      mg[0] == kg[0] and mg[-1] == kg[-1]
                      and mg[1:-1] != kg[1:-1], f"{mg!r} vs {kg!r}")
        r_framed[name] = framed
        check(f"{name}: the radio's containment clause is "
              f"{'non-vacuous' if framed else 'SPAN-ONLY'} "
              f"({framed} of {len(RDS)} states carry a framed well) — a "
              f"one-cell well has no interior, and the languages that cannot "
              f"afford the shape-FAMILY distinction are named, not hidden",
              framed in (0, len(RDS)), f"framed {framed}")

        # (d) the state axis, pairwise, colour stripped
        g = {st: shape(item_cells(k, st)) for st in RDS}
        check(f"{name}: all {len(RDS)} radio states are pairwise distinct with "
              f"colour REMOVED, combinations included",
              len(set(g.values())) == len(RDS),
              f"{len(set(g.values()))} distinct of {len(RDS)}")
        check(f"{name}: checked+disabled reads as neither half alone",
              g["checked+disabled"] != g[LG.CHECKED]
              and g["checked+disabled"] != g[LG.DISABLED])

        # (e) NO JIGGLE ACROSS SELECTIONS — the row must not move when the
        # user crosses it, or every sibling appears to shift under the
        # cursor. Asked over every selection AND every cursor position.
        widths = {len(grey(k.radio_group(OPTS, sel, ctl, foc)))
                  for sel in range(len(OPTS)) for ctl in CTL
                  for foc in (None, 0, 1, 2)}
        check(f"{name}: the group holds ONE width across every selection, "
              f"every cursor position and every control state",
              len(widths) == 1, f"widths {sorted(widths)}")
        # PER ITEM the claim is narrower and it is the one that matters: an
        # item's width may differ from its sibling's because its WORD does
        # (`mid` is a cell wider than `lo`, and padding that away would put
        # dead air inside a row). What must never move is one item under the
        # cursor — measured per option index, across every selection, every
        # cursor position and every control state.
        for i in range(len(OPTS)):
            iw = {len(grey(k.radio_items(OPTS, sel, ctl, foc)[i]))
                  for sel in range(len(OPTS)) for ctl in CTL
                  for foc in (None, 0, 1, 2)}
            check(f"{name}: item {i} (`{OPTS[i]}`) holds ONE width whatever "
                  f"is selected and wherever the cursor is — a set whose "
                  f"items resize as you cross it is a set that jiggles",
                  len(iw) == 1, f"widths {sorted(iw)}")
        ww = {len(k.part_glyph(p, st, "radio")) for p in ("main", "knob")
              for st in RDS}
        check(f"{name}: ... and the WELL is one width across every state and "
              f"both parts, so a stacked set's options line up in a column",
              len(ww) == 1, f"well widths {sorted(ww)}")

        # (f) SINGLE-WRITE PAINT, per item row.
        check(f"{name}: every item composes exactly ONE slot — one write of "
              f"its whole region including its ground (Bodmer T4)",
              all(len(item_cells(k, st)) == 1 for st in RDS))
        check(f"{name}: and a group of n emits exactly n item rows, so the "
              f"set cannot lose an option to a layout",
              all(len(k.radio_items(OPTS[:n], 0)) == n for n in (1, 2, 3)))

        # (g) THE PRINTED WORD IS THE OPTION'S, never CHECK_WORDS. Three
        # languages print `ON`/`posted`/`OFF` beside a switch; a radio item
        # names ITSELF, because only the group knows what the item is.
        row = grey(k.radio_group(OPTS, RADIO_SEL, LG.FOCUSED, RADIO_FOCUS))
        check(f"{name}: every option's own word is printed — all three at "
              f"once, which is the whole difference from a switch: a set "
              f"shows its alternatives, a boolean shows its state",
              all(o in row for o in OPTS), f"{row!r}")
        if k.CHECK_WORDS:
            check(f"{name}: ... and its CHECK_WORDS do NOT appear on a radio "
                  f"— `{k.CHECK_WORDS[1].strip()}` beside `mid` would be the "
                  f"language answering a question nobody asked",
                  not any(wd.strip() and wd.strip() in row
                          for wd in k.CHECK_WORDS), f"{row!r}")

        # (h) the accent laws of pass 48, asked a FOURTH time.
        for st in (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE, LG.DISABLED):
            sl = {p for p, _, t in cells_of(k, "slider", 5, st)
                  if t == k["accent"]} & {"main", "knob"}
            rd = {p for p, _, t in item_cells(k, LG.with_checked(st, True))
                  if t == k["accent"]}
            check(f"{name}: the {st} radio spends the accent on exactly the "
                  f"parts its slider does — one tone rule, four components",
                  sl == rd, f"slider {sorted(sl)} vs radio {sorted(rd)}")

        # (i) PROBE DISCIPLINE.
        check(f"{name}: the greyscale projection agrees with rich's own "
              f"parser on every radio string — `( )` and `< >` are literal "
              f"text, and an instrument that reads them as tags measures an "
              f"invisible control",
              all(grey_is_rich(k.radio_group(OPTS, sel, ctl, foc))
                  for sel in range(len(OPTS)) for ctl in CTL
                  for foc in (None, 2)))

    sigs = {n: "|".join(shape(item_cells(LG.kit(n), st)) for st in RDS)
            for n in TH.ORDER}
    check("no two languages draw the same radio in greyscale",
          len(set(sigs.values())) == len(TH.ORDER),
          f"{len(set(sigs.values()))} distinct of {len(TH.ORDER)}")
    cbsig = {n: "|".join(shape(LG.kit(n).component_cells(
        "checkbox", None, 0, 1, 1, st)) for st in RDS) for n in TH.ORDER}
    check("and no language's radio signature equals its own checkbox's — the "
          "ONE constraint the skill puts on this component, ten times over",
          all(sigs[n] != cbsig[n] for n in TH.ORDER))
    print("  radio containment, per language: "
          + "  ".join(f"{n}={'framed' if r_framed[n] else 'span'}"
                      for n in TH.ORDER))
    for n in TH.ORDER:
        k = LG.kit(n)
        check(f"{n}: its radio is not its switch either — a set of three with "
              f"one chosen is not a boolean, and the render says so",
              shape(item_cells(k, LG.CHECKED))
              != shape(cells_of(k, "switch", 1, LG.CHECKED, 0, 1, SW)))

    # -- (5) THE GALLERY SEAT ----------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        block = radio_block(k, GAL_W)
        check(f"{name}: the gallery's radio block FITS the {GAL_W}-column box",
              max(len(grey(r)) for r in block) <= GAL_W,
              f"widest {max(len(grey(r)) for r in block)}, {len(block)} rows")
        check(f"{name}: ... and it lays the set ACROSS when there is room — "
              f"five rows for four control states",
              len(radio_block(k, 200)) == 5)
        check(f"{name}: ... and DOWN when there is not — thirteen rows, and "
              f"the widest drops from 45 to 28. Reflow, never truncate",
              len(radio_block(k, 20)) == 13
              and max(len(grey(r)) for r in radio_block(k, 20))
              < max(len(grey(r)) for r in radio_block(k, 200)))
        for w_ in (GAL_W, 200, 20):
            body = "\n".join(grey(r) for r in radio_block(k, w_))
            check(f"{name}: the block at w={w_} shows every OPTION at every "
                  f"control state — a set that fits by dropping an option is "
                  f"a different set",
                  all(grey(it) in body for c in CTL
                      for it in k.radio_items(RADIO_OPTS, RADIO_SEL, c,
                                              RADIO_FOCUS)))

    # -- (6) THE LIVE SEAT'S SET is the engine's, not a second declaration --
    run_all_src = inspect.getsource(EN.Engine.run_all)
    named = tuple(re.findall(r'"(\w+)"', run_all_src))
    check("the config screen's radio offers exactly the worker groups the "
          "engine actually runs — one declaration, held against `run_all`'s "
          "own source, so a third loop cannot appear with no way to choose it",
          named == WORKER_GROUPS, f"run_all names {named}, app has "
          f"{WORKER_GROUPS}")
    check("... and every shipped signal already sits in one of them, so the "
          "live group is a SELECTION over a real set and not an invented one",
          {s.group for s in EN.default_signals()} <= set(WORKER_GROUPS))
    check("the live set is N=2, and that is stated rather than dressed up: it "
          "is the weakest honest N-of-M in this app, and what makes it a "
          "radio and not a switch is that BOTH options are named on screen "
          "with exactly one marked",
          len(WORKER_GROUPS) == 2)

    bars = {n: shape(cells_of(LG.kit(n), "bar", 5)) for n in TH.ORDER}
    check("no two languages draw the same bar either",
          len(set(bars.values())) == len(TH.ORDER),
          f"{len(set(bars.values()))} distinct of {len(TH.ORDER)}")

    # -- CONTROLS: every law above, driven red on purpose ------------------
    class _ColourOnly(LG.Kit):
        """States separated by colour alone — the defect LVGL's own corpus
        carries 1848 times out of 1848."""
        PART_GLYPHS = {"main": {LG.DEFAULT: "─"},
                       "indicator": {LG.DEFAULT: "━"},
                       "knob": {LG.DEFAULT: "│"}}

    co = _ColourOnly("nord")
    cog = {st: shape(cells_of(co, "slider", 5, st)) for st in CS["slider"]}
    check("control: a language whose knob is ONE glyph in every state fails "
          "the greyscale state law (the law has teeth)",
          len(set(cog.values())) == 1)
    check("control: ... while its TONES still differ, which is exactly how "
          "such a defect passes a colour-blind eye and a colour-blind check",
          len({t for st in CS["slider"]
               for _, _, t in cells_of(co, "slider", 5, st)}) > 1)

    class _FatKnob(LG.Kit):
        PART_GLYPHS = {"main": {LG.DEFAULT: "─"},
                       "indicator": {LG.DEFAULT: "█"},
                       "knob": {LG.DEFAULT: "<>", LG.FOCUSED: "|"}}

    fk = _FatKnob("nord")
    fw = {len(shape(cells_of(fk, "slider", 5, st)))
          for st in (LG.DEFAULT, LG.FOCUSED)}
    check("control: a knob two cells wide makes the region CHANGE WIDTH "
          "between states, and the anti-jiggle law goes red",
          len(fw) > 1, f"widths {sorted(fw)}")

    ok = [("main", "─", "d"), ("indicator", "█", "m"), ("knob", "▌", "i")]
    moved_track = [("main", "╌", "d"), ("indicator", "█", "m"),
                   ("knob", "▌", "i")]
    check("control: the mechanism-invariance predicate REPORTS a track cell "
          "that changed — it is not a `not []` that can never fire",
          main_changed(ok, moved_track) == [0] and main_changed(ok, ok) == [])
    check("control: ... and it stays silent when only the indicator moves, so "
          "it is not merely a diff wearing a law's name",
          main_changed(ok, [ok[0], ("indicator", "▒", "m"), ok[2]]) == [])

    _saved_bar = LG.COMPONENT_PARTS["bar"]
    LG.COMPONENT_PARTS["bar"] = ("main", "indicator", "knob")
    try:
        rogue = LG.kit("nord").component_cells("bar", 5, 0, 10, WC)
        check("control: a bar GIVEN a knob grows one on the screen and takes "
              "the interactive states with it — the registry is the law, and "
              "the checks above read the registry rather than restating it",
              any(p == "knob" for p, _, _ in rogue)
              and LG.FOCUSED in LG.component_states("bar"))
    finally:
        LG.COMPONENT_PARTS["bar"] = _saved_bar
    check("control: ... and the registry is put back — a control that leaks "
          "state into the suite behind it is worse than no control",
          LG.COMPONENT_PARTS["bar"] == ("main", "indicator")
          and LG.component_states("bar") == (LG.DEFAULT, LG.DISABLED)
          and not any(p == "knob" for p, _, _
                      in LG.kit("nord").component_cells("bar", 5, 0, 10, WC)))

    # =====================================================================
    print("\n== KIT LEVEL: THE BUTTON — the control with NO VALUE, and the "
          "first component whose LABEL is inside it")
    # Two questions, and the second one is the increment. (a) Does the state
    # axis still fall out of the registry when there is nothing to be EDITED
    # or CHECKED? (b) What are a button's PARTS, given that its label stands
    # INSIDE it where every other component's word stands beside it — the
    # first time this registry has had to decide whether text is a part.
    #
    # The answers are asked here so they can go red: the label is NOT a part,
    # so the state must ride the cells the LANGUAGE owns and the caller's word
    # must come back out of the render byte for byte. Those two laws are only
    # both satisfiable if the label is content, which is what makes this a
    # decision under test rather than a preference.
    from textual.content import Content     # the parser the APP renders with
    BTS = CS["button"]
    BFOUR = (LG.DEFAULT, LG.FOCUSED, LG.ACTIVE, LG.DISABLED)
    BLAB = "Save"

    def bcells(k, st=LG.DEFAULT, val=None):
        return k.component_cells("button", val, 0, 1, 1, st)

    def walls(k, st):
        return k.part_glyph("main", st, "button")

    def bplain(k, label=BLAB, w=0, st=LG.DEFAULT):
        """The button as the SCREEN gets it — rich's parse of the markup."""
        return Text.from_markup(k.button(label, w, st)).plain

    # -- (1) THE REGISTRY: one part, and what fell out of it ---------------
    check("registry: the button declares exactly ONE part — `main`, its own "
          "ground. LVGL gives it the same one, and its LABEL is a child "
          "object there for the same reason it is content here",
          LG.COMPONENT_PARTS["button"] == ("main",))
    check("registry: no INDICATOR — nothing is measured, so there is no "
          "extent; and no KNOB — nothing is set, so there is no separate grip",
          "indicator" not in LG.COMPONENT_PARTS["button"]
          and "knob" not in LG.COMPONENT_PARTS["button"])
    check("registry: it is NOT checkable, so no CHECKED anywhere in its axis "
          "— a button has no bit to carry",
          "button" not in LG.CHECKABLE
          and not any(LG.is_checked(s) for s in BTS))
    check("registry: THE ANSWER TO (a) — the axis is exactly "
          "default / focused / active / disabled, four states and nothing "
          "else, and it is DERIVED. A hand-written control list is what this "
          "check exists to make impossible",
          BTS == BFOUR, f"{BTS}")
    check("registry: no EDITED — the arrows have nothing to range through, "
          "and that is now read off the EXTENT rather than off CHECKABLE, "
          "which is the term the button had to add",
          LG.EDITED not in BTS and not any(LG.EDITED in s for s in BTS))

    # THE VALUE FACT, which both answers turn on.
    check("registry: `has_value` is FALSE for the button and for the TEXT "
          "FIELD, and TRUE for the five that hold a number or a bit. The "
          "button holds nothing; the field holds CONTENT, which the registry "
          "cannot read any more than it can read a label — same ruling, read "
          "at the value instead of at the word",
          not LG.has_value("button") and not LG.has_value("textfield")
          and all(LG.has_value(n) for n in NAMES
                  if n not in ("button", "textfield")),
          str({n: LG.has_value(n) for n in NAMES}))
    check("registry: ... and it is DERIVED from the three facts that can "
          "carry a value — an extent MEASURES a number, a step CHOOSES among "
          "seats, CHECKABLE declares a bit. The caret is deliberately not "
          "among them: a field's cells are the CALLER's, which is the same "
          "ruling read at the value instead of at the word",
          all(LG.has_value(n)
              == ("indicator" in LG.COMPONENT_PARTS[n]
                  or "step" in LG.COMPONENT_PARTS[n] or n in LG.CHECKABLE)
              for n in NAMES))

    # THE ONE LAW OF THIS CONTRACT THAT MOVED, stated as a table.
    check("registry: the ACTUATOR — a knob where one is declared, `main` for "
          "a valueless one-part control (the whole thing IS the grip), and "
          "NONE for a readout. That table is the refinement (a) forced: "
          "`knob in parts` was standing in for `there is something to grab`",
          {n: LG.actuator(n) for n in NAMES}
          == {"slider": "knob", "bar": None, "switch": "knob",
              "checkbox": "knob", "radio": "knob", "button": "main",
              "textfield": "caret", "scrollbar": None, "stepper": "step"},
          str({n: LG.actuator(n) for n in NAMES}))
    check("registry: the control states exist for exactly the components "
          "with an actuator — the bar still has none, which is the law the "
          "refinement had to leave standing",
          all((LG.FOCUSED in CS[n]) == bool(LG.actuator(n)) for n in NAMES))
    check("registry: EDITED exists for exactly the components with an "
          "INTERIOR that is not a boolean — one expression, asked of all "
          "seven. The button read that interior off the EXTENT; the text "
          "field has one and no extent, so the term is the concept the "
          "extent was standing in for",
          all((LG.EDITED in CS[n])
              == bool(LG.actuator(n) and LG.has_interior(n)
                      and n not in LG.CHECKABLE) for n in NAMES),
          str({n: LG.EDITED in CS[n] for n in NAMES}))
    check("registry: ... and `has_interior` is DERIVED from three parts that "
          "were already declared — an extent is a run measured from an "
          "origin, a field is a run indexed by a mark, a series is seats "
          "reached by stepping, and all three are cells a cursor moves "
          "between. No new registry FACT bought EDITED at any of them",
          all(LG.has_interior(n)
              == ("indicator" in LG.COMPONENT_PARTS[n]
                  or "caret" in LG.COMPONENT_PARTS[n]
                  or "step" in LG.COMPONENT_PARTS[n]) for n in NAMES)
          and {n: LG.has_interior(n) for n in NAMES}
          == {"slider": True, "bar": True, "switch": True, "checkbox": False,
              "radio": False, "button": False, "textfield": True,
              "scrollbar": True, "stepper": True},
          str({n: LG.has_interior(n) for n in NAMES}))
    check("registry: and the button keeps DEFAULT and DISABLED like every "
          "other component — the two states nothing can take away",
          {LG.DEFAULT, LG.DISABLED} <= set(BTS))

    # -- (2) CONTROLS on the derivation: new components, no hand lists -----
    LG.COMPONENT_PARTS["_probe_target"] = ("main",)
    LG.COMPONENT_PARTS["_probe_grip"] = ("main", "knob")
    try:
        check("control: a NEW component declaring only `main` gets the "
              "button's four states with nothing hand-listed — the "
              "derivation, not the button, is what knows this",
              LG.component_states("_probe_target") == BTS)
        check("control: ... and a knobbed component with NO extent gets the "
              "same four, so the missing EDITED is the extent talking and "
              "not CHECKABLE. The checkbox's removal was over-attributed",
              LG.component_states("_probe_grip") == BTS)
        _saved_ck = LG.CHECKABLE
        LG.CHECKABLE = _saved_ck + ("_probe_grip",)
        try:
            check("control: declaring THAT probe checkable gives it the "
                  "eight-state product — the checkable axis is still a "
                  "registry fact and the button did not disturb it",
                  LG.component_states("_probe_grip")
                  == CS["checkbox"] == CS["switch"])
        finally:
            LG.CHECKABLE = _saved_ck
    finally:
        del LG.COMPONENT_PARTS["_probe_target"]
        del LG.COMPONENT_PARTS["_probe_grip"]
    check("control: ... and the registry is put back — a control that leaks "
          "state into the suite behind it is worse than no control",
          "_probe_target" not in LG.COMPONENT_PARTS
          and "_probe_grip" not in LG.COMPONENT_PARTS
          and LG.component_states("button") == BTS)

    _saved_bparts = LG.COMPONENT_PARTS["button"]
    LG.COMPONENT_PARTS["button"] = ("main", "indicator")
    try:
        check("control: GIVE the button an extent and it stops being a "
              "control altogether — it becomes a readout, exactly as the bar "
              "is. The four states are the registry's, not the component's",
              LG.component_states("button") == CS["bar"]
              and LG.has_value("button"))
    finally:
        LG.COMPONENT_PARTS["button"] = _saved_bparts
    check("control: ... registry restored again",
          LG.COMPONENT_PARTS["button"] == ("main",)
          and LG.component_states("button") == BTS)

    # -- (3) SOURCE: the refinement lives on the REGISTRY, names nobody ----
    for fn in (LG.has_value, LG.actuator, LG.component_states, LG.Kit.button,
               LG.Kit.part_tone):
        nm = getattr(fn, "__name__", "?")
        hits = [n for n in NAMES if f'"{n}"' in code_of(fn)
                or f"'{n}'" in code_of(fn)]
        allowed = {"button"} if nm == "button" else set()
        hits = [h for h in hits if h not in allowed]
        check(f"source: `{nm}` names NO component in its code — the button "
              f"inherited the axis and the tone rule rather than being "
              f"granted them"
              + (" (its own name, at its own seat, is the one exception a "
                 "component method is allowed)" if allowed else ""),
              not hits, f"names {hits}")
    check("source: the state derivation gates the control block on the "
          "ACTUATOR and EDITED on the INTERIOR — read off the code, because "
          "'derived' is a claim about the source and not about the output",
          "if actuator(name):" in code_of(LG.component_states)
          and "has_interior(name) and not checkable"
          in code_of(LG.component_states))
    check("source: and the ACTUATOR reads the GRIPS registry rather than "
          "listing them at its seat — which is where the caret entered, and "
          "the difference between a registry that grew and a derivation that "
          "grew a special case",
          "for grip in GRIPS:" in code_of(LG.actuator)
          and "caret" not in code_of(LG.actuator))
    check("source: the TONE rule asks the actuator too — the same word "
          "changed at both seats, which is what makes this one refinement "
          "rather than two special cases",
          "actuator(name)" in code_of(LG.Kit.part_tone))
    check("source: and the composer refuses a value it cannot hold on the "
          "registry fact, not on a name",
          "not has_value(name)" in code_of(LG.Kit.component_cells))
    check("source: the button appends NO readout — `value_label` and "
          "`check_label` are not reachable from it, because a component with "
          "no value has nothing to report beside itself",
          "value_label" not in code_of(LG.Kit.button)
          and "check_label" not in code_of(LG.Kit.button))
    check("source: it is `check_TONE` it does reuse — one tone rule for a "
          "control's word, three components deep now",
          "check_tone(" in code_of(LG.Kit.button))

    # -- (4) PER LANGUAGE ---------------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)

        check(f"{name}: declares its OWN button glyph — a button drawn with "
              f"the slider's track is a picture of a track",
              k.part_key("button", "main") == "button.main")
        check(f"{name}: ONE slot at every width a caller could ask for — the "
              f"walls need a seat, and the FIELD between them is not made of "
              f"parts",
              {k.part_slots("button", w_) for w_ in (1, 3, 8, 20)} == {1})
        check(f"{name}: and NO chrome — chrome fixes the ends of a track, and "
              f"a button has no track; its ends are its own glyph",
              k.comp_chrome("button") == ("", ""))

        # (a) THE WALLS: even, one width, four shapes.
        # Keyed by the four states LITERALLY and not by the derived axis: what
        # a language DECLARES is independent of what the registry derives, and
        # a mutation that shrinks the axis must go red at the derivation laws
        # rather than take this loop down with a KeyError. A raised law
        # reports nothing (PENDING, the fiftieth pass's driver lesson).
        ws = {st: walls(k, st) for st in BFOUR}
        check(f"{name}: the walls are an EVEN number of cells, so the halves "
              f"the label stands between really are halves",
              all(len(v) % 2 == 0 and len(v) >= 2 for v in ws.values()),
              str({s: len(v) for s, v in ws.items()}))
        check(f"{name}: ONE wall width across all four states — the field "
              f"cannot move under the word (anti-jiggle, at the source)",
              len({len(v) for v in ws.values()}) == 1,
              f"{sorted({len(v) for v in ws.values()})}")
        check(f"{name}: all four states are pairwise distinct in SHAPE — with "
              f"the label constant and colour stripped, the walls are the "
              f"only thing left to say which state this is",
              len(set(ws.values())) == 4, f"{ws}")
        check(f"{name}: the PRESS differs from FOCUS in shape, not in colour "
              f"— ACTIVE is the one state this component exists for, and a "
              f"button that only changes hue when pressed says nothing",
              ws[LG.ACTIVE] != ws[LG.FOCUSED])
        check(f"{name}: DISABLED is shape-marked too, against DEFAULT",
              ws[LG.DISABLED] != ws[LG.DEFAULT])
        check(f"{name}: its walls are not its own checkbox's box — a word in "
              f"a tick box is not a button",
              all(ws[st] != k.part_glyph("main", st, "checkbox")
                  for st in BFOUR))

        # (b) THE COMPOSER: one part, one slot, no value reachable.
        for st in BTS:
            cells = bcells(k, st)
            check(f"{name}: the {st} button composes exactly ONE slot — one "
                  f"write of its whole region including its ground (T4)",
                  len(cells) == 1)
            check(f"{name}: ... drawing only the part it declares, in every "
                  f"state — a part it does not declare is a part it cannot "
                  f"draw",
                  {p for p, _, _ in cells} == {"main"})
        check(f"{name}: HANDED A VALUE, it ignores it. There is no part for a "
              f"value to reach, and without that term the shared model would "
              f"pick a PRESENCE and grow the button a mark it never declared",
              all({p for p, _, _ in bcells(k, st, val=v)} == {"main"}
                  for st in BTS for v in (0, 1, 5, -3)))
        check(f"{name}: asked for a state it does not have, it renders "
              f"DEFAULT rather than raising — EDITED and CHECKED are not "
              f"errors here, they are simply not this component's states",
              bplain(k, st=LG.EDITED) == bplain(k)
              and bplain(k, st=LG.CHECKED) == bplain(k))

        # (c) THE LABEL IS CONTENT — the answer to (b), asked so it can fail.
        # BFOUR again, and for the same reason as the walls: this reads the
        # language's own declaration, and a derivation defect must go red at
        # the derivation laws instead of taking this loop down with it.
        for st in BFOUR:
            r = bplain(k, st=st)
            check(f"{name}: the {st} button gives the caller's word back "
                  f"VERBATIM — one occurrence, unrecased, unspaced. A "
                  f"language that restyled it would be drawing text it did "
                  f"not choose, which is exactly what a PART is",
                  r.count(BLAB) == 1, repr(r))
            check(f"{name}: ... and the word never escapes the control: the "
                  f"render opens with this state's left wall and closes with "
                  f"its right, with the label strictly between them",
                  r.startswith(ws[st][:len(ws[st]) // 2])
                  and r.endswith(ws[st][len(ws[st]) // 2:])
                  and r.find(BLAB) >= len(ws[st]) // 2, repr(r))
            check(f"{name}: ... and no READOUT is printed — a button has no "
                  f"value, so the words the checkables print have nothing to "
                  f"say about it",
                  not (k.CHECK_WORDS
                       and any(w_.strip() and w_.strip() in r
                               for w_ in k.CHECK_WORDS)), repr(r))
        widths = {len(bplain(k, st=st)) for st in BTS}
        check(f"{name}: ONE rendered width across every state for one label — "
              f"the anti-jiggle law read off the render, not off the table",
              len(widths) == 1, f"widths {sorted(widths)}")
        grew = {len(bplain(k, l_, st=LG.DEFAULT)) - len(l_)
                for l_ in ("a", "ok", "Refresh", "A much longer caption")}
        check(f"{name}: the FIELD grows exactly with the word and by nothing "
              f"else — the walls are a constant, which is what 'the label is "
              f"content on the language's ground' means arithmetically",
              len(grew) == 1, f"overheads {sorted(grew)}")
        check(f"{name}: `w` is a MINIMUM: asked for 20 it pads to 20 and "
              f"centres, asked for less than the word it does NOT truncate — "
              f"a button cannot shorten the word that says what it does",
              len(bplain(k, "ok", 20)) == 20 + len(ws[LG.DEFAULT])
              and BLAB in bplain(k, BLAB, 1))
        check(f"{name}: a padded button still holds its word once and whole",
              bplain(k, "ok", 20).count("ok") == 1)

        # (d) THE TONE RULE, generalised to the actuator (pass 48's law, a
        # fifth time). What must hold is that the button's GROUND wears
        # exactly what this language gives its slider's KNOB — same rule,
        # different grip — including naught, whose ration overrules it.
        for st in BTS:
            bt = {t for _, _, t in bcells(k, st)}
            kt = {t for p, _, t in cells_of(k, "slider", 5, st) if p == "knob"}
            check(f"{name}: the {st} button's ground wears exactly what this "
                  f"language gives its slider's KNOB — one tone rule, five "
                  f"components, and the word `knob` in it was only ever "
                  f"standing in for `the part under the finger`",
                  bt == kt, f"button {sorted(bt)} vs knob {sorted(kt)}")
        check(f"{name}: a DISABLED button is dim everywhere, walls and word — "
              f"the second channel, under the first",
              {t for _, _, t in bcells(k, LG.DISABLED)} == {k["dim"]}
              and k.check_tone(True, LG.DISABLED) == k["dim"])

        # (e) PROBE DISCIPLINE, and this pass had to grow it: the suite's
        # oracle was rich, and the APP renders with Textual's own markup
        # parser. They disagree about a `[` that does not open a tag — which
        # is exactly what a bracketed button is made of.
        for st in BTS:
            s_ = k.button(BLAB, 0, st)
            check(f"{name}: the {st} button parses IDENTICALLY under rich and "
                  f"under Textual — the app is rendered by the second one, "
                  f"and a suite that only asks the first cannot see a `[/]` "
                  f"reaching the glass",
                  Text.from_markup(s_).plain == Content.from_markup(s_).plain,
                  f"rich {Text.from_markup(s_).plain!r} vs textual "
                  f"{Content.from_markup(s_).plain!r}")
            check(f"{name}: ... and the cheap greyscale projection agrees "
                  f"with both",
                  grey_is_rich(s_)
                  and grey(s_) == Content.from_markup(s_).plain)

    # -- (5) THE SAME PARSER LAW over every component the contract owns.
    # The defect it found is older than this component (see the control
    # below), so it is asked of the whole family and not just the newcomer.
    for name in TH.ORDER:
        k = LG.kit(name)
        strings = ([k.slider(5, 0, 10, WC, st) for st in CS["slider"]]
                   + [k.readbar(5, 0, 10, WC, st) for st in CS["bar"]]
                   + [k.switch(LG.is_checked(st), SW, st)
                      for st in CS["switch"]]
                   + [k.checkbox(LG.is_checked(st), st)
                      for st in CS["checkbox"]]
                   + [k.radio_group(OPTS, 1, ctl, 2) for ctl in CTL]
                   + [k.button(BLAB, 0, st) for st in BTS]
                   + [k.textfield("[x]y", 2, 8, st, placeholder="[p]")
                      for st in CS["textfield"]])
        bad = [s_ for s_ in strings
               if Text.from_markup(s_).plain != Content.from_markup(s_).plain]
        check(f"{name}: EVERY component string means the same thing to both "
              f"parsers. This went red on the day it was written for the "
              f"bracketed languages — a `[` that opens no tag left the "
              f"following `[/]` unclosed under Textual and printed it",
              not bad, f"{len(bad)} diverge, first {bad[0]!r}" if bad else "")

    check("control: the parser law CAN fire — a raw bracketed glyph, escaped "
          "the way rich's own `escape` leaves it, is read differently by the "
          "two parsers. That is the defect, reproduced on this run",
          Text.from_markup("[#aaa][ [/]x").plain
          != Content.from_markup("[#aaa][ [/]x").plain)
    check("control: ... and `mark` is what makes them agree, which is why it "
          "exists at the component seats",
          Text.from_markup(f"[#aaa]{LG.mark('[ ')}[/]x").plain
          == Content.from_markup(f"[#aaa]{LG.mark('[ ')}[/]x").plain
          == "[ x")

    # -- (6) CROSS-LANGUAGE: ten buttons, ten mechanisms -------------------
    bsig = {n: "|".join(walls(LG.kit(n), st) for st in BTS) for n in TH.ORDER}
    check("no two languages draw the same button in greyscale",
          len(set(bsig.values())) == len(TH.ORDER),
          f"{len(set(bsig.values()))} distinct of {len(TH.ORDER)}")
    print("  button walls, per language: "
          + "  ".join(f"{n}={bsig[n].split('|')[0]!r}" for n in TH.ORDER))

    # -- (7) CONTROLS: the per-language laws, driven red on purpose --------
    class _FlatButton(LG.Kit):
        """A button whose walls never change — the LVGL defect, on this
        component: four states separated by colour alone."""
        PART_GLYPHS = dict(LG.Kit.PART_GLYPHS,
                           **{"button.main": {LG.DEFAULT: "[  ]"}})

    fb = _FlatButton("nord")
    check("control: a language whose button walls are ONE glyph in every "
          "state fails the four-state shape law (the law has teeth)",
          len({fb.part_glyph("main", st, "button") for st in BTS}) == 1)

    class _ShoutingButton(LG.Kit):
        """A language that RESTYLES the caller's word — the exact thing the
        label-is-not-a-part decision forbids."""
        def button(self, label, w=0, state=LG.DEFAULT):
            return super().button(str(label).upper(), w, state)

    sb = _ShoutingButton("nord")
    check("control: a language that recases the label fails the verbatim law "
          "— which is the law that says the word is the caller's and the "
          "ground is the language's",
          Text.from_markup(sb.button(BLAB)).plain.count(BLAB) == 0)

    class _WideActive(LG.Kit):
        PART_GLYPHS = dict(LG.Kit.PART_GLYPHS,
                           **{"button.main": {LG.DEFAULT: "[  ]",
                                              LG.ACTIVE: "[[  ]]"}})

    wa = _WideActive("nord")
    check("control: a press that grows the walls makes the render CHANGE "
          "WIDTH between states, and the anti-jiggle law goes red",
          len({len(Text.from_markup(wa.button(BLAB, 0, st)).plain)
               for st in BTS}) > 1)

    # -- (8) THE GALLERY SEAT ----------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        block = button_block(k, GAL_W)
        check(f"{name}: the gallery's button block FITS the {GAL_W}-column "
              f"box",
              max(len(grey(r)) for r in block) <= GAL_W,
              f"widest {max(len(grey(r)) for r in block)}, {len(block)} rows")
        check(f"{name}: ... it pairs the two labels ACROSS when there is room "
              f"— five rows for four control states",
              len(button_block(k, 200)) == 5)
        check(f"{name}: ... and stacks them DOWN when there is not, nine "
              f"rows, narrower. Reflow, never truncate",
              len(button_block(k, 20)) == 9
              and max(len(grey(r)) for r in button_block(k, 20))
              < max(len(grey(r)) for r in button_block(k, 200)))
        for w_ in (GAL_W, 200, 20):
            body = "\n".join(grey(r) for r in button_block(k, w_))
            check(f"{name}: the block at w={w_} draws every state with BOTH "
                  f"labels — the pair is what shows the field growing while "
                  f"the walls hold still",
                  all(grey(k.button(l_, 0, st)) in body
                      for st in BTS for l_ in BTN_LABELS))

    print("\n== KIT LEVEL: THE TEXT FIELD — the CARET enters the registry, "
          "and the value is CONTENT")
    # The headline question, and it is a registry question rather than a
    # drawing one: is the caret a PART? It is, and the decisive reason is
    # structural — in this renderer a STATE is a property of the whole
    # component (`part_glyph` answers once per part per state), so "main, but
    # in EDITED" would put a caret in EVERY cell of the field. The only thing
    # that tells one cell from its neighbours here is its PART TAG. The laws
    # below are written so that ruling can go red: the caret must be tagged,
    # must be at the index it was handed, must appear in EDITED and nowhere
    # else — while the VALUE comes back byte for byte, which is the button's
    # content ruling read at the value instead of at the label.
    TF = CS["textfield"]
    TFP = LG.COMPONENT_PARTS["textfield"]
    TFS = (LG.DEFAULT, LG.FOCUSED, LG.EDITED, LG.ACTIVE, LG.INVALID,
           LG.DISABLED)
    LONG = "abcdefghijklmnopqrstuvwxyz"
    FW = 8                                  # the field's columns in these laws

    def tplain(k, value="", caret=None, w=FW, st=LG.DEFAULT, ph=""):
        """The field as the SCREEN gets it, colour stripped."""
        return Text.from_markup(
            k.textfield(value, caret, w, st, placeholder=ph)).plain

    def form(k, st):
        return k.part_glyph("main", st, "textfield")

    def rune(k, st):
        return k.field_form(st, "textfield")[1]

    def carg(k, st=LG.EDITED):
        return k.part_glyph("caret", st, "textfield")

    def inner(k, s_, st):
        """The FIELD, with the two walls taken off — the cells the caller's
        value and the language's paper share."""
        o, _, c = k.field_form(st, "textfield")
        return s_[len(o):len(s_) - len(c)]

    # -- (1) THE REGISTRY: the first new part since the contract ------------
    check("registry: the text field declares `main` and `caret`, and CARET "
          "IS THE FIRST NEW PART THIS REGISTRY HAS TAKEN since it was "
          "written. It passes the bar the button's LABEL failed: the "
          "language draws it, from its own glyph table, and where it stands "
          "is state — none of which is true of the caller's words",
          TFP == ("main", "caret"))
    check("registry: `caret` is genuinely new — no component that came "
          "before declares it, so this is a part entering rather than a name "
          "being reused",
          all("caret" not in LG.COMPONENT_PARTS[n]
              for n in NAMES if n != "textfield"))
    check("registry: AND IT IS NOT THE KNOB, which is the alternative that "
          "would have cost no new part. `(main, knob)` is the CHECKBOX's "
          "tuple; letting a field wear it would make one tuple mean two "
          "anatomies — a mark that is either there or not, and a mark at one "
          "of w places. Identical parts with different mechanisms is what "
          "this registry exists to make impossible",
          "knob" not in TFP and LG.COMPONENT_PARTS["checkbox"] != TFP)
    check("registry: no INDICATOR — a field measures nothing. Its interior "
          "is INDEXED, not measured, which is the distinction `has_interior` "
          "had to name",
          "indicator" not in TFP and LG.has_interior("textfield"))
    check("registry: it is NOT checkable — a field's value is neither a "
          "number nor a bit",
          "textfield" not in LG.CHECKABLE
          and not any(LG.is_checked(s) for s in TF))
    check("registry: THE GRIPS are a declared registry fact, not a list "
          "hidden inside `actuator`. A knob rides a track and reports a "
          "magnitude; a caret rides characters and reports an index. "
          "Different parts, one thing to the hand — and a STEP is a third, "
          "which is the point of a declared tuple: it grew and `actuator` "
          "did not",
          LG.GRIPS == ("knob", "caret", "step")
          and "caret" not in code_of(LG.actuator)
          and "step" not in code_of(LG.actuator))
    check("registry: ... and every grip named there is a part some component "
          "actually declares — a grip nobody declares is dead metadata, "
          "which is the defect the button refused",
          all(any(g in LG.COMPONENT_PARTS[n] for n in NAMES)
              for g in LG.GRIPS))
    check("registry: the ACTUATOR of a text field is its CARET, so the "
          "accent lands on the mark under the finger exactly as it lands on "
          "a slider's knob",
          LG.actuator("textfield") == "caret")
    check("registry: the axis is default / focused / EDITED / active / "
          "INVALID / disabled — six states, DERIVED, and the pair EDITED and "
          "INVALID is what this component was chosen to test: what the "
          "arrows can change, the form can reject",
          TF == TFS, f"{TF}")
    check("registry: EDITED IS PRESENT AND IT MEANS WHAT IT SAYS HERE. On a "
          "slider it is 'the arrows now move the value'; here it is 'the "
          "keystrokes now land IN the text', and the caret is the promise of "
          "exactly that. FOCUSED is the field selected, EDITED is the field "
          "entered",
          LG.EDITED in TF and LG.FOCUSED in TF)
    check("registry: only the slider, the text field and the STEPPER take "
          "EDITED — the three components with a grip, an interior and no "
          "boolean. Every one of them arrived by derivation",
          {n for n in NAMES if LG.EDITED in CS[n]}
          == {"slider", "textfield", "stepper"},
          str({n for n in NAMES if LG.EDITED in CS[n]}))
    check("registry: `has_value` is FALSE — and that is the RULING, not an "
          "omission. The registry holds no value for a field because a "
          "field's value is CONTENT, which is what the button said about a "
          "label. It is also why no readout is printed beside it: the value "
          "is already visible IN the control",
          not LG.has_value("textfield"))

    # -- (2) CONTROLS on the derivation: no hand lists ---------------------
    LG.COMPONENT_PARTS["_probe_field"] = ("main", "caret")
    LG.COMPONENT_PARTS["_probe_both"] = ("main", "indicator", "caret")
    try:
        check("control: a NEW component declaring `(main, caret)` gets the "
              "text field's six states with nothing hand-listed — the "
              "derivation, not the text field, is what knows this",
              LG.component_states("_probe_field") == TFS)
        check("control: ... and its actuator is the caret, off GRIPS alone",
              LG.actuator("_probe_field") == "caret"
              and not LG.has_value("_probe_field"))
        check("control: a component with BOTH an extent and a field still "
              "gets six states — an interior counted twice is one interior, "
              "and the knobless grip is still the caret",
              LG.component_states("_probe_both") == TFS
              and LG.actuator("_probe_both") == "caret")
        _sv = LG.CHECKABLE
        LG.CHECKABLE = _sv + ("_probe_field",)
        try:
            check("control: declaring the field probe CHECKABLE takes EDITED "
                  "away again — a boolean has no interior to range through, "
                  "and that rule did not move when the caret arrived",
                  LG.EDITED not in LG.component_states("_probe_field")
                  and not any(LG.EDITED in s
                              for s in LG.component_states("_probe_field")))
        finally:
            LG.CHECKABLE = _sv
    finally:
        del LG.COMPONENT_PARTS["_probe_field"]
        del LG.COMPONENT_PARTS["_probe_both"]
    check("control: ... and the registry is put back",
          "_probe_field" not in LG.COMPONENT_PARTS
          and "_probe_both" not in LG.COMPONENT_PARTS
          and LG.component_states("textfield") == TFS)

    _sp = LG.COMPONENT_PARTS["textfield"]
    LG.COMPONENT_PARTS["textfield"] = ("main",)
    try:
        check("control: TAKE THE CARET AWAY and the field collapses into a "
              "button — four states, no EDITED, `main` as its own grip. The "
              "caret is carrying the whole difference",
              LG.component_states("textfield") == CS["button"]
              and LG.actuator("textfield") == "main")
    finally:
        LG.COMPONENT_PARTS["textfield"] = _sp
    check("control: ... registry restored again",
          LG.COMPONENT_PARTS["textfield"] == ("main", "caret")
          and LG.component_states("textfield") == TFS)

    # -- (3) SOURCE: the new fork is on the REGISTRY, names nobody ---------
    for fn in (LG.has_interior, LG.actuator, LG.component_states,
               LG.Kit.field_form, LG.Kit.component_cells, LG.Kit.part_slots,
               LG.Kit.part_tone):
        nm = getattr(fn, "__name__", "?")
        hits = [n for n in NAMES if f'"{n}"' in code_of(fn)
                or f"'{n}'" in code_of(fn)]
        check(f"source: `{nm}` names NO component in its code — the text "
              f"field inherited the axis, the tone rule and the composer's "
              f"third anatomy rather than being granted them",
              not hits, f"names {hits}")
    hits = [n for n in NAMES
            if (f'"{n}"' in code_of(LG.Kit.textfield)
                or f"'{n}'" in code_of(LG.Kit.textfield))
            and n != "textfield"]
    check("source: `Kit.textfield` names only ITSELF — its own name at its "
          "own seat is the one exception a component method is allowed, and "
          "the button set that precedent",
          not hits, f"names {hits}")
    check("source: the composer's THIRD anatomy forks on the REGISTRY — "
          "`caret in parts`, a fact about parts and not about who is asking. "
          "Extent / field / presence, three branches, three registry facts",
          '"caret" in parts' in code_of(LG.Kit.component_cells)
          and '"caret" in COMPONENT_PARTS[name]'
          in code_of(LG.Kit.part_slots))
    check("source: `has_interior` is the OR of declared PARTS and nothing "
          "else — every term is a slot in the registry, and no new declared "
          "FACT bought EDITED for any component that has it",
          '"indicator" in parts or "caret" in parts'
          in code_of(LG.has_interior)
          and not any(f'"{n}"' in code_of(LG.has_interior) for n in NAMES))
    check("source: the text field appends NO readout — `value_label` and "
          "`check_label` are not reachable from it, because its value is "
          "already visible inside it and printing it twice would be a lie "
          "about where the value lives",
          "value_label" not in code_of(LG.Kit.textfield)
          and "check_label" not in code_of(LG.Kit.textfield))
    check("source: it is `check_TONE` it reuses, for the FOURTH component — "
          "and here it answers set-versus-unset, which is what separates a "
          "typed value from a placeholder",
          "check_tone(" in code_of(LG.Kit.textfield))
    check("source: and the walls come out of the SAME glyph string as the "
          "paper (`field_form`), because a language does not choose them "
          "separately — it chooses the ground it lays under someone's words",
          "field_form(" in code_of(LG.Kit.textfield)
          and "field_form(" in code_of(LG.Kit.component_cells))

    # -- (4) PER LANGUAGE ---------------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        forms = {st: form(k, st) for st in TF}
        car = carg(k)
        runes = {rune(k, st) for st in TF}

        check(f"{name}: declares its OWN scoped field glyphs — a field drawn "
              f"with the slider's track would be a picture of a slider",
              k.part_key("textfield", "main") == "textfield.main"
              and k.part_key("textfield", "caret") == "textfield.caret")
        check(f"{name}: the field's ground is an ODD string in every state — "
              f"wall, RUNE, wall. The button states the same 'the walls are "
              f"halves' rule as an EVEN length; this component has an "
              f"interior to put between them",
              all(len(g_) % 2 == 1 and len(g_) >= 3 for g_ in forms.values()),
              str({s_: len(g_) for s_, g_ in forms.items()}))
        check(f"{name}: ONE length across every state — the frame may not "
              f"move under the words",
              len({len(g_) for g_ in forms.values()}) == 1)
        check(f"{name}: the grounds are pairwise DISTINCT with colour "
              f"stripped — a field separated by hue alone says nothing to a "
              f"greyscale eye, and the value may fill every other cell. "
              f"COUNTED off the derivation, never numbered here: the axis "
              f"grew by one in kits-learn-3 and this check had to be edited, "
              f"which is a literal earning its keep",
              len(set(forms.values())) == len(forms),
              str(sorted(set(forms.values()))))
        check(f"{name}: the caret is exactly ONE cell wide — a mark that "
              f"spent two would push the value under itself",
              len(car) == 1, repr(car))
        check(f"{name}: the caret is NOT A SPACE and differs from the paper's "
              f"rune in every state. A space is the one character the "
              f"caller's own value certainly contains, and a mark that can "
              f"be confused with content is not a mark",
              car != " " and car not in runes, f"{car!r} vs runes {runes}")
        check(f"{name}: the caret has NO CHROME to hide behind — its walls "
              f"are its `main` glyph, not the slider's track terminators",
              k.comp_chrome("textfield") == ("", ""))
        check(f"{name}: the field is `w` COLUMNS wide, exactly, at every "
              f"width asked — `w` is a window, not a budget",
              all(k.part_slots("textfield", w_) == w_
                  for w_ in (1, 3, 8, 20, 40)))

        # THE CARET IS TAGGED, AND IT IS AT THE INDEX IT WAS HANDED.
        for st in TF:
            cells = k.component_cells("textfield", None, 0, 1, FW, st,
                                      caret=3)
            check(f"{name}: the {st} field composes exactly {FW} cells, one "
                  f"per column, and draws only its declared parts",
                  len(cells) == FW
                  and {p for p, _, _ in cells} <= set(TFP))
            check(f"{name}: ... with the caret tagged at the index it was "
                  f"given and nowhere else — one cell, index 3",
                  [i for i, (p, _, _) in enumerate(cells)
                   if p == "caret"] == [3])
        cells0 = k.component_cells("textfield", None, 0, 1, FW, LG.EDITED,
                                   caret=None)
        check(f"{name}: and with NO caret handed in, no cell is tagged one — "
              f"the mark is state the caller owns, not decoration the "
              f"language adds",
              not any(p == "caret" for p, _, _ in cells0))

        # THE CARET IS DRAWN IN EDITED AND IN NO OTHER STATE.
        drawn = {st: tplain(k, TF_VALUE, 2, FW, st).count(car) for st in TF}
        check(f"{name}: the caret is drawn in EDITED and in NO other state — "
              f"a field showing an insertion point while the keyboard is "
              f"somewhere else is lying about where the next keystroke lands",
              drawn.get(LG.EDITED) == 1
              and all(v == 0 for s_, v in drawn.items() if s_ != LG.EDITED),
              str(drawn))
        # `find`, NOT `index`, and this is pass 52's lesson arriving again on
        # a new component: `index` RAISES when the caret is absent, which is
        # exactly the mutation this law exists to catch, and a raised law
        # takes the whole run down reporting nothing. It cost two DEAD RUNs
        # in round one of this pass's mutation table (M8, M9) before it was
        # written this way. `find` returns -1 and goes red like a law.
        idx_ok = all(
            inner(k, tplain(k, TF_VALUE, i, FW, LG.EDITED),
                  LG.EDITED).find(car) == i
            for i in range(len(TF_VALUE) + 1))
        check(f"{name}: THE CARET IS AT THE CELL THE MODEL SAYS — caret at "
              f"index i renders at column i, asked at every index of the "
              f"value including both ends",
              idx_ok)
        check(f"{name}: an out-of-range caret CLAMPS rather than raising or "
              f"escaping the field — the index is a caller's number and a "
              f"renderer that dies on one takes the surface with it",
              inner(k, tplain(k, TF_VALUE, 99, FW, LG.EDITED),
                    LG.EDITED).find(car) == len(TF_VALUE)
              and inner(k, tplain(k, TF_VALUE, -5, FW, LG.EDITED),
                        LG.EDITED).find(car) == 0)

        # THE FORM, READ STRAIGHT OFF THE GLYPH TABLE. Every law above that
        # touches the paper asks `field_form`, which is the code under test —
        # an oracle that calls what it is testing moves with it, and round
        # one proved it: the mutation that made the rune come out of the WALL
        # instead of the middle scored 2 red across ten languages, because
        # nine tenths of the laws were reading the mutated form. This one
        # re-derives the convention (odd string, middle is the paper) from
        # the declared string and composes the whole expected render.
        for st in TF:
            g_ = form(k, st)
            h_ = len(g_) // 2
            paper = (car + g_[h_] * (FW - 1) if st == LG.EDITED
                     else g_[h_] * FW)
            check(f"{name}: the {st} EMPTY field is exactly its DECLARED "
                  f"string composed — opening wall, the middle character "
                  f"across the whole field, closing wall (and the caret in "
                  f"the first column when it is being edited). Read off the "
                  f"glyph table, not through the code under test",
                  tplain(k, "", None, FW, st) == g_[:h_] + paper + g_[h_ + 1:],
                  f"{tplain(k, '', None, FW, st)!r} vs declared {g_!r}")

        # THE VALUE IS CONTENT.
        for st in TF:
            r_ = tplain(k, TF_VALUE, 2, FW, st)
            # THE LAW IS ASKED WITH THE CARET LIFTED OUT, and that is the
            # content ruling choosing the mechanism rather than a weakening.
            # The caret takes a COLUMN OF ITS OWN precisely so that no
            # character is hidden under it — a block cursor would hide one,
            # and keeping it readable underneath would mean reverse video,
            # which is colour. So the rendered value is the caller's bytes
            # with one language-owned cell BETWEEN two of them, and asking
            # for the substring verbatim would be asking the caret not to
            # exist. This wording is what the first run of these laws taught.
            v_ = r_.replace(car, "")
            check(f"{name}: the {st} field gives the caller's value back "
                  f"BYTE FOR BYTE once the caret's own cell is lifted out — "
                  f"never recased, never letterspaced, never bracketed. The "
                  f"state rides the walls the language owns",
                  TF_VALUE in v_, f"{r_!r} -> {v_!r}")
            check(f"{name}: ... exactly once, and NOTHING is printed after "
                  f"the closing wall — a field has no readout, because its "
                  f"value is already visible inside it",
                  v_.count(TF_VALUE) == 1
                  and r_.endswith(k.field_form(st, "textfield")[2]))
        long_r = tplain(k, LONG, len(LONG), FW, LG.EDITED)
        check(f"{name}: a value LONGER than the field is never SHORTENED — "
              f"the field is full, and the characters not shown are behind "
              f"the window rather than gone",
              len(inner(k, long_r, LG.EDITED)) == FW
              and car in long_r)

        # THE WINDOW.
        starts = []
        for i in range(len(LONG) + 1):
            body = inner(k, tplain(k, LONG, i, FW, LG.EDITED), LG.EDITED)
            starts.append(body)
        check(f"{name}: the caret stays INSIDE the field at every index of a "
              f"long value — the view moves, which is what windowing IS",
              all(b.count(car) == 1 for b in starts))
        check(f"{name}: the character just BEFORE the caret is always visible "
              f"— what you just typed never falls off the edge",
              all(LONG[i - 1] in starts[i] for i in range(1, len(LONG) + 1)))
        check(f"{name}: EVERY index of the value is reachable — move the "
              f"caret to it and the character is on screen. That is the "
              f"honest form of 'nothing is lost'",
              all(LONG[i] in starts[i] or LONG[i] in starts[i + 1]
                  for i in range(len(LONG))))
        slices = []
        for b in starts:
            run = "".join(ch for ch in b.replace(car, "") if ch in LONG)
            slices.append(run)
        check(f"{name}: what the window shows is a CONTIGUOUS SLICE of the "
              f"value — nothing reordered, and no ellipsis eating bytes to "
              f"buy itself a cell",
              all(s_ and s_ in LONG for s_ in slices))
        check(f"{name}: the window MOVES with the caret rather than sitting "
              f"still — a field that never scrolled would be truncating",
              len(set(slices)) > 1, f"{len(set(slices))} distinct views")

        # ANTI-JIGGLE: the frame holds while the caret walks.
        widths = {len(tplain(k, v_, c_, FW, st, ph=TF_PLACE))
                  for v_ in ("", TF_VALUE, LONG)
                  for c_ in (0, 2, 99) for st in TF}
        check(f"{name}: ONE rendered width across every state, every value "
              f"and every caret position — the walls do not move when the "
              f"words do",
              len(widths) == 1, f"{sorted(widths)}")
        moves = []
        for i in range(len(TF_VALUE)):
            a_ = inner(k, tplain(k, TF_VALUE, i, FW, LG.EDITED), LG.EDITED)
            b_ = inner(k, tplain(k, TF_VALUE, i + 1, FW, LG.EDITED),
                       LG.EDITED)
            moves.append(sum(1 for x, y in zip(a_, b_) if x != y))
        check(f"{name}: moving the caret one place changes at most TWO cells "
              f"— the caret's seat and the character it swapped with. A "
              f"single write, and the frame is not one of them",
              all(m <= 2 for m in moves), f"{moves}")

        # THE PLACEHOLDER.
        empty = tplain(k, "", None, FW, LG.DEFAULT, ph=TF_PLACE)
        typed = tplain(k, TF_PLACE, None, FW, LG.DEFAULT, ph=TF_PLACE)
        full = tplain(k, TF_VALUE, None, FW, LG.DEFAULT, ph=TF_PLACE)
        check(f"{name}: the placeholder is shown when the value is empty",
              TF_PLACE in empty, repr(empty))
        check(f"{name}: ... and is GONE the moment the value is not — a "
              f"field showing both would be showing two answers",
              TF_PLACE not in full and TF_VALUE in full, repr(full))
        check(f"{name}: ... and the placeholder is TONED apart from the same "
              f"word typed in. This is the one place in this contract where "
              f"colour carries the whole distinction, and it is said out "
              f"loud: shape is unavailable because the hint is the caller's "
              f"words too. It is not a STATE distinction, which is what the "
              f"'never colour alone' law governs",
              k.textfield("", None, FW, LG.DEFAULT, placeholder=TF_PLACE)
              != k.textfield(TF_PLACE, None, FW, LG.DEFAULT,
                             placeholder=TF_PLACE)
              and empty == typed)
        check(f"{name}: ... and the placeholder is CONTENT too — byte for "
              f"byte, never restyled, exactly like the value",
              TF_PLACE in empty and empty.count(TF_PLACE) == 1)

        # THE STATE CHANNELS, colour stripped.
        # KEYED BY THE STATES THE REGISTRY ACTUALLY DECLARES, and asked with
        # `in` before `[]`. Pass 52 cured this exact shape after a mutation
        # GREW the axis and a per-language dict threw KeyError; round one of
        # this pass hit the mirror image — M8 SHRANK it (a field declared
        # with a knob has no EDITED) and the dead run reported nothing. A
        # derivation defect must go red at the derivation laws, not take the
        # loop down on its way past.
        greys = {st: tplain(k, TF_VALUE, 2, FW, st) for st in TF}
        check(f"{name}: DISABLED is SHAPE-marked — a dead field must read "
              f"dead with the colour taken away",
              {LG.DISABLED, LG.DEFAULT} <= set(greys)
              and greys[LG.DISABLED] != greys[LG.DEFAULT])
        check(f"{name}: EDITED differs from FOCUSED in shape — the caret is "
              f"exactly that difference, which is what makes 'the field "
              f"selected' and 'the field entered' two readable states",
              {LG.EDITED, LG.FOCUSED} <= set(greys)
              and greys[LG.EDITED] != greys[LG.FOCUSED])
        check(f"{name}: all states are pairwise distinct in greyscale "
              f"with a value in the field — INVALID included, which is the "
              f"one a fallback along the state chain would silently pass",
              len(set(greys.values())) == len(greys),
              str(sorted(set(greys.values()))))

        # THE ACCENT LAW, a sixth time.
        for st in (LG.FOCUSED, LG.EDITED, LG.ACTIVE, LG.DEFAULT,
                   LG.DISABLED):
            ct = k.part_tone("caret", st, "textfield")
            kt = k.part_tone("knob", st, "slider")
            check(f"{name}: the {st} caret wears exactly what this language "
                  f"gives its slider's KNOB — one accent rule, and the caret "
                  f"reaches it as a GRIP rather than as a special case",
                  ct == kt, f"caret {ct} vs knob {kt}")

        # THE TWO-PARSER LAW.
        for st in TF:
            s_ = k.textfield(TF_VALUE, 2, FW, st, placeholder=TF_PLACE)
            check(f"{name}: the {st} field parses IDENTICALLY under rich and "
                  f"under Textual — the app renders with the second one",
                  Text.from_markup(s_).plain == Content.from_markup(s_).plain,
                  f"rich {Text.from_markup(s_).plain!r} vs textual "
                  f"{Content.from_markup(s_).plain!r}")
        brack = k.textfield("[urgent]", 3, FW, LG.EDITED)
        check(f"{name}: a value carrying a BRACKET survives both parsers and "
              f"reaches the glass as itself — user text is where the "
              f"two-parser hazard actually bites",
              Text.from_markup(brack).plain == Content.from_markup(brack).plain
              and "[/]" not in Content.from_markup(brack).plain)

    # -- (5) CROSS-LANGUAGE ------------------------------------------------
    tsig = {n: "|".join(form(LG.kit(n), st) for st in TF) + "/"
            + carg(LG.kit(n)) for n in TH.ORDER}
    check("no two languages draw the same text field in greyscale",
          len(set(tsig.values())) == len(TH.ORDER),
          f"{len(set(tsig.values()))} distinct of {len(TH.ORDER)}")
    print("  field grounds, per language: "
          + "  ".join(f"{n}={tsig[n].split('|')[0]!r}" for n in TH.ORDER))

    # -- (6) CONTROLS: the per-language laws, driven red on purpose --------
    class _ShoutingField(LG.Kit):
        """A language that RESTYLES the caller's value — the exact thing the
        content ruling forbids, moved from the label to the value."""
        def textfield(self, value="", caret=None, w=12, state=LG.DEFAULT,
                      placeholder=""):
            return super().textfield(str(value).upper(), caret, w, state,
                                     placeholder)

    sf = _ShoutingField("nord")
    check("control: a language that recases the VALUE fails the verbatim law "
          "— which is the law that says the words are the caller's and the "
          "ground is the language's",
          TF_VALUE not in Text.from_markup(sf.textfield(TF_VALUE, 2, FW)).plain)

    class _TruncField(LG.Kit):
        """A field that CUTS instead of windowing — the defect the window
        exists to prevent, and the one a user meets as lost text."""
        def textfield(self, value="", caret=None, w=12, state=LG.DEFAULT,
                      placeholder=""):
            return super().textfield(str(value)[:max(1, int(w)) - 1], caret,
                                     w, state, placeholder)

    tf_ = _TruncField("nord")
    reach = [i for i in range(len(LONG))
             if LONG[i] not in Text.from_markup(
                 tf_.textfield(LONG, i + 1, FW, LG.EDITED)).plain]
    check("control: a field that TRUNCATES puts most of the value out of "
          "reach — the window law has teeth, and this is what it catches",
          len(reach) > 10, f"{len(reach)} indices unreachable")

    class _BlindCaret(LG.Kit):
        """A caret drawn as the paper's own rune — a mark you cannot see is
        not a mark, and it is the mutation a language could make by taste."""
        PART_GLYPHS = dict(LG.Kit.PART_GLYPHS,
                           **{"textfield.caret": {LG.DEFAULT: " "}})

    bc = _BlindCaret("nord")
    check("control: a caret drawn as a SPACE collides with the one character "
          "a value certainly contains, and the caret-glyph law goes red",
          bc.part_glyph("caret", LG.EDITED, "textfield") == " ")

    class _EvenForm(LG.Kit):
        """An EVEN ground string — the walls are no longer halves of what is
        left when the rune is taken out of the middle."""
        PART_GLYPHS = dict(LG.Kit.PART_GLYPHS,
                           **{"textfield.main": {LG.DEFAULT: "[  ]"}})

    ef = _EvenForm("nord")
    check("control: an EVEN ground string fails the odd-length law, and the "
          "rune it hands back is a WALL rather than paper",
          len(ef.part_glyph("main", LG.DEFAULT, "textfield")) % 2 == 0
          and ef.field_form(LG.DEFAULT, "textfield")[1] == " ")

    class _FlatField(LG.Kit):
        """One ground for every state — five states separated by colour."""
        PART_GLYPHS = dict(LG.Kit.PART_GLYPHS,
                           **{"textfield.main": {LG.DEFAULT: "[ ]"}})

    ff = _FlatField("nord")
    check("control: a language whose field ground is ONE string in every "
          "state fails the five-state shape law",
          len({ff.part_glyph("main", st, "textfield") for st in TF}) == 1)

    # -- (7) THE GALLERY SEAT ----------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        block = textfield_block(k, GAL_W)
        check(f"{name}: the gallery's text-field block FITS the {GAL_W}-"
              f"column box",
              max(len(grey(r)) for r in block) <= GAL_W,
              f"widest {max(len(grey(r)) for r in block)}, {len(block)} rows")
        check(f"{name}: ... it draws EVERY state the registry declares, plus "
              f"the placeholder and the window — the rows are derived, so a "
              f"sixth state would grow one without this block being touched",
              len(block) == len(TF) + 3)
        body = "\n".join(grey(r) for r in block)
        check(f"{name}: ... every control state is drawn with the same value "
              f"and the same caret, which is what makes the states "
              f"comparable by eye",
              all(grey(k.textfield(TF_VALUE, TF_CARET, 10, st)) in body
                  for st in TF))
        check(f"{name}: ... and the placeholder row and the window row are "
              f"both there — the two questions only this component asks",
              grey(k.textfield("", None, 10, LG.DEFAULT,
                               placeholder=TF_PLACE)) in body
              and grey(k.textfield(TF_LONG, len(TF_LONG), 10,
                                   LG.EDITED)) in body)
        narrow = textfield_block(k, 20)
        check(f"{name}: ... it REFLOWS BY NARROWING THE WINDOW, which only "
              f"this component can do honestly: a smaller view shows less of "
              f"the value and loses none of it. Every other block stacks",
              max(len(grey(r)) for r in narrow)
              < max(len(grey(r)) for r in textfield_block(k, 200))
              and len(narrow) == len(block))
        check(f"{name}: ... and the narrow form still holds a caret and a "
              f"frame — it renounced view, not mechanism",
              carg(k) in "\n".join(grey(r) for r in narrow))

    print("\n== KIT LEVEL: THE SCROLL BAR — the value that is a WINDOW, and "
          "the SECOND SEAT beside `value_pos`")
    # The headline question, and it is a MECHANISM question where the text
    # field's was a registry one: a scroll bar renders TWO numbers — where
    # the view is and how big it is — and `value_pos` answers with ONE
    # position. Either the registry grows a fact or the mechanism grows a
    # seat, and the answer taken here is BOTH, because they answer different
    # halves: `VIEWED` says which components have a two-number value (no
    # expression over parts can, since `bar` declares the same tuple), and
    # `view_pos` is what turns two numbers into (first cell, span).
    #
    # ORACLE INDEPENDENCE, stated where it is spent (pass 53's defect 3):
    # the seat `view_pos` is pinned below by PROPERTY laws — exact ends,
    # monotonicity, proportionality — that recompute nothing. The RENDER laws
    # then compose their expectation from the DECLARED glyph table and that
    # pinned seat, and the ends are additionally asserted with no arithmetic
    # at all (first cell / last cell), so a mutation inside the seat cannot
    # move the oracle and the render together.
    SB = CS["scrollbar"]
    SBP = LG.COMPONENT_PARTS["scrollbar"]
    SW = 12                                # the shaft's cells in these laws
    STOT, SSZ, SBIG = 40, 8, 24            # content, window, a bigger window
    SLAST = STOT - SSZ                     # the last legal start

    def sb_cells(k, start, size=SSZ, total=STOT, w=SW, st=LG.DEFAULT):
        return k.component_cells("scrollbar", start, 0, total, w, st,
                                 size=size)

    def sb_tags(k, *a, **kw):
        return [p for p, _, _ in sb_cells(k, *a, **kw)]

    def sb_run(tags):
        """`(first cell, span)` of the thumb, READ OFF THE RENDER's own part
        tags — the pass-46 cure: a part's extent comes back from the render
        instead of being recomputed in the oracle."""
        idx = [i for i, p in enumerate(tags) if p == "indicator"]
        return (idx[0], len(idx)) if idx else (-1, 0)

    def sbp(k, start, size=SSZ, total=STOT, w=SW, st=LG.DEFAULT):
        return Text.from_markup(k.scrollbar(start, size, total, w, st)).plain

    # -- (1) THE REGISTRY: no new part, and a new VALUE FACT ---------------
    check("registry: the scroll bar declares the BAR'S EXACT TUPLE and adds "
          "NO new part. The caret was a new part because a state cannot pick "
          "out one cell; a thumb is not, because a scroll bar has no cell a "
          "bar does not have — a track and a run on it",
          SBP == ("main", "indicator") == LG.COMPONENT_PARTS["bar"])
    check("registry: ... so every part it names was already declared — this "
          "increment grew the registry's FACTS and not its anatomy",
          all(p in {q for n in NAMES for q in LG.COMPONENT_PARTS[n]
                    if n != "scrollbar"} for p in SBP))
    check("registry: and THAT COLLISION is the proof the difference must be "
          "DECLARED. Two components share a tuple and differ in what their "
          "value IS — the registry has met this twice (switch/slider, "
          "radio/checkbox) and answered with a fact both times",
          LG.COMPONENT_PARTS["scrollbar"] == LG.COMPONENT_PARTS["bar"]
          and ("scrollbar" in LG.VIEWED) != ("bar" in LG.VIEWED))
    check("registry: `VIEWED` is CHECKABLE's family, not a third kind of "
          "thing — CHECKABLE says the value's RANGE is boolean, VIEWED says "
          "its ARITY is two. Both are facts about a VALUE that parts cannot "
          "show; GRIPS is the one fact about parts",
          LG.VIEWED == ("scrollbar",)
          and all(n in LG.COMPONENT_PARTS for n in LG.VIEWED))
    check("registry: NO GRIP OF ITS OWN — the scroll bar declares not one "
          "of the parts `GRIPS` names, which is the answer to 'a third "
          "declared fact is a smell': its pass added a fact and took none of "
          "the seats a grip would have moved. (The tuple has grown SINCE, at "
          "the stepper, and this component was untouched by that too)",
          not any(g in SBP for g in LG.GRIPS)
          and "step" not in SBP and LG.actuator("scrollbar") is None)
    check("registry: and CHECKABLE did not move either — a window is not a "
          "bit and does not join the product axis",
          LG.CHECKABLE == ("switch", "checkbox", "radio")
          and "scrollbar" not in LG.CHECKABLE)

    # THE READOUT RULING, and its consequences are DERIVED.
    check("registry: THE SCROLL BAR IS A READOUT — `actuator` is None. In "
          "this keyboard TUI the keys scroll the CONTAINER and the bar "
          "reports where the container got to; nothing here is ever grabbed, "
          "so there is no grip and the derivation says so without being told",
          LG.actuator("scrollbar") is None
          and LG.actuator("scrollbar") == LG.actuator("bar"))
    check("registry: ... so its axis is DEFAULT and DISABLED and nothing "
          "else, and it is the BAR'S axis byte for byte. A FOCUSED scroll "
          "bar would advertise an affordance this app does not have — the "
          "same defect the bar's missing knob was the first cure for",
          SB == (LG.DEFAULT, LG.DISABLED) == CS["bar"],
          f"{SB}")
    check("registry: ... and that is a CONSEQUENCE, not a preference — no "
          "control state is reachable, because the control block is gated on "
          "the actuator and there is none",
          not any(s in SB for s in (LG.FOCUSED, LG.EDITED, LG.ACTIVE))
          and not any(LG.is_checked(s) for s in SB))
    check("registry: it HOLDS a value (an extent is declared) — which is why "
          "it is a readout and not a button: there is something to report, "
          "and no way to set it here",
          LG.has_value("scrollbar"))
    check("registry: it HAS an interior and still gets no EDITED — the "
          "interior term alone would have granted one, and the ACTUATOR gate "
          "is what refuses it. Two terms, and this component is the first to "
          "separate them",
          LG.has_interior("scrollbar") and LG.EDITED not in SB)
    check("registry: the state axis is unchanged for every OTHER component — "
          "a new fact that moved an old component's axis would be a "
          "refactor wearing an increment's clothes",
          {n: CS[n] for n in NAMES if n != "scrollbar"}
          == {n: LG.component_states(n) for n in NAMES if n != "scrollbar"})

    # -- (2) CONTROLS on the registry fact ---------------------------------
    LG.COMPONENT_PARTS["_probe_view"] = ("main", "indicator")
    LG.COMPONENT_STATES["_probe_view"] = LG.component_states("_probe_view")
    _sv = LG.VIEWED
    try:
        nk = LG.kit("nord")
        LG.VIEWED = _sv + ("_probe_view",)
        wtags = sb_tags(nk, SLAST)
        ptags = [p for p, _, _ in nk.component_cells(
            "_probe_view", SLAST, 0, STOT, SW, LG.DEFAULT, size=SSZ)]
        check("control: a NEW component declaring `(main, indicator)` and "
              "named in VIEWED gets the WINDOW mechanism with zero edits at "
              "any seat — the fourth anatomy is the registry's, not the "
              "scroll bar's",
              ptags == wtags, f"{sb_run(ptags)} vs {sb_run(wtags)}")
        LG.VIEWED = _sv
        btags = [p for p, _, _ in nk.component_cells(
            "_probe_view", SLAST, 0, STOT, SW, LG.DEFAULT, size=SSZ)]
        check("control: ... and taken OUT of VIEWED the SAME component draws "
              "as a BAR — an extent anchored at cell 0 whose length is its "
              "position. One tuple, two mechanisms, and the fact is what "
              "chooses between them",
              sb_run(btags)[0] == 0 and sb_run(wtags)[0] > 0,
              f"bar {sb_run(btags)} vs window {sb_run(wtags)}")
        LG.VIEWED = ()
        dead = sb_tags(nk, SLAST)
        check("control: with the scroll bar itself out of VIEWED its thumb "
              "leaves the bottom of the track and anchors at the top — the "
              "window laws below all fail at once, which is what makes this "
              "a fact and not a label",
              sb_run(dead)[0] == 0 and sb_run(wtags)[0] == SW - sb_run(wtags)[1],
              f"{sb_run(dead)} vs {sb_run(wtags)}")
        check("control: ... and it grows a READOUT it has no business having "
              "— one number printed beside a two-number value",
              sbp(nk, SLAST) != Text.from_markup(
                  nk._component_body("scrollbar", SLAST, 0, STOT, SW,
                                     LG.DEFAULT, SSZ)).plain)
    finally:
        LG.VIEWED = _sv
        del LG.COMPONENT_PARTS["_probe_view"]
        del LG.COMPONENT_STATES["_probe_view"]
    check("control: the registry is restored after the probes",
          LG.VIEWED == ("scrollbar",) and "_probe_view" not in NAMES
          and "_probe_view" not in LG.COMPONENT_PARTS)

    # -- (3) THE SEAT: `view_pos` / `view_start`, with no language in sight -
    # PROPERTY laws. None of them recomputes the arithmetic; every one of
    # them states something the contract PROMISES, so a mutation inside the
    # seat cannot satisfy them by moving with them.
    for cells in (7, 12, 20):
        spans = [LG.view_pos(0, s, STOT, cells)[1]
                 for s in (1, 4, 8, 16, 24, 32)]
        # nth-exempt: `spans` two lines up is a six-element comprehension
        # with NO `if` over a literal tuple, so it has exactly six items on
        # every input and `spans[0]` cannot raise. The sweep flags it because
        # its name resolution is one-hop and whole-file: another `spans` at
        # L11256 IS a filtered comprehension, and the detector cannot tell
        # the two apart without dataflow it does not have. A dataflow
        # heuristic that quietly stops reporting is strictly worse than a
        # listed exemption, because nothing measures a heuristic.
        check(f"seat: THE THUMB'S LENGTH IS THE SECOND NUMBER — at {cells} "
              f"cells the span rises with the view size and never falls. "
              f"That is the whole thing `value_pos` could not say",
              spans == sorted(spans) and spans[0] < spans[-1], f"{spans}")
        check(f"seat: ... with a FLOOR of one cell at {cells} — a thumb that "
              f"vanished would leave a scroll bar with nothing on it, which "
              f"is the microbar defect this repo already cured for sparks",
              LG.view_pos(0, 1, 100000, cells)[1] == 1)
        check(f"seat: ... and a CAP of the whole track at {cells}: a window "
              f"showing everything fills its shaft, which is the honest way "
              f"to say there is nothing to scroll",
              LG.view_pos(0, STOT, STOT, cells)[1] == cells
              and LG.view_pos(0, STOT * 2, STOT, cells) == (0, cells))
        pos0, span0 = LG.view_pos(0, SSZ, STOT, cells)
        posL, spanL = LG.view_pos(SLAST, SSZ, STOT, cells)
        check(f"seat: THE ENDS ARE EXACT at {cells} cells — start 0 puts the "
              f"thumb's FIRST cell at 0, and the last legal start puts its "
              f"LAST cell at {cells - 1}. This is the classic off-by-one in "
              f"this component and it is asserted as cells, not as a ratio",
              pos0 == 0 and posL + spanL == cells,
              f"top {(pos0, span0)} bottom {(posL, spanL)}")
        check(f"seat: ... and the length does NOT change while the window "
              f"travels at {cells} — position and extent are two numbers and "
              f"neither is allowed to leak into the other",
              len({LG.view_pos(s, SSZ, STOT, cells)[1]
                   for s in range(SLAST + 1)}) == 1)
        poss = [LG.view_pos(s, SSZ, STOT, cells)[0] for s in range(SLAST + 1)]
        check(f"seat: the thumb only ever moves FORWARD as the view does "
              f"({cells} cells) — a scroll bar that backed up would be "
              f"reporting a scroll that did not happen",
              poss == sorted(poss) and poss[0] < poss[-1])
        check(f"seat: the thumb is ALWAYS WHOLLY ON THE TRACK at {cells}, at "
              f"every start including the illegal ones a caller may hand in",
              all(0 <= p and p + sp <= cells
                  for p, sp in (LG.view_pos(s, SSZ, STOT, cells)
                                for s in range(-9, STOT + 9))))
        check(f"seat: an out-of-range start CLAMPS at {cells} rather than "
              f"raising or running off — the start is a caller's number and "
              f"a renderer that dies on one takes the surface with it",
              LG.view_pos(-99, SSZ, STOT, cells)
              == LG.view_pos(0, SSZ, STOT, cells)
              and LG.view_pos(999, SSZ, STOT, cells)
              == LG.view_pos(SLAST, SSZ, STOT, cells))
    check("seat: a zero or negative track, size or total is SAFE — the "
          "degenerate cases a container hands a bar during layout",
          LG.view_pos(0, 0, 0, 0) == (0, 1)
          and LG.view_pos(-1, -1, -1, 1) == (0, 1))

    check("seat: `view_start` LEAVES A WINDOW ALONE when the focus is "
          "already inside it — the least move is no move, and a window that "
          "recentred would throw away the reading the user has",
          all(LG.view_start(STOT, SSZ, f, 10) == 10 for f in range(10, 18)))
    check("seat: ... pulls UP to exactly the focus when the focus is above "
          "the window",
          LG.view_start(STOT, SSZ, 3, 10) == 3
          and LG.view_start(STOT, SSZ, 0, 30) == 0)
    check("seat: ... and pulls DOWN by exactly the shortfall when the focus "
          "is below it — one cell of travel per cell of overshoot",
          LG.view_start(STOT, SSZ, 20, 10) == 20 - SSZ + 1
          and LG.view_start(STOT, SSZ, 21, 10) == 21 - SSZ + 1)
    check("seat: ... the focus always lands INSIDE the window it returns, "
          "asked at every index of the content from every starting view",
          all(LG.view_start(STOT, SSZ, f, s) <= f
              < LG.view_start(STOT, SSZ, f, s) + SSZ
              for f in range(STOT) for s in (0, 7, 19, SLAST)))
    check("seat: ... and it is IDEMPOTENT — settling a settled window moves "
          "nothing, which is what makes it a fixed point and not a nudge",
          all(LG.view_start(STOT, SSZ, f,
                            LG.view_start(STOT, SSZ, f, s))
              == LG.view_start(STOT, SSZ, f, s)
              for f in range(STOT) for s in (0, 11, SLAST)))
    check("seat: with NO focus it only clamps — the scroll bar's case, where "
          "the window is handed a start and has no cursor to keep in view",
          LG.view_start(STOT, SSZ, None, 12) == 12
          and LG.view_start(STOT, SSZ, None, 999) == SLAST
          and LG.view_start(STOT, SSZ, None, -3) == 0)
    check("seat: content that FITS is not scrollable — the window is pinned "
          "at 0 whatever it is asked for, which is the same fact the full "
          "thumb reports at the other seat",
          all(LG.view_start(5, 9, f, s) == 0
              for f in (None, 0, 4) for s in (0, 3, 99)))

    # -- (4) SOURCE: the fork is on the registry, the seat is delegated ----
    check("source: `view_pos` DELEGATES THE POSITION to `value_pos` — it "
          "computes the SPAN and nothing else, so there is still exactly one "
          "place in this file that turns a number into a cell index. That is "
          "the pass-43 'one measure' discipline surviving a second seat",
          "value_pos(" in code_of(LG.view_pos))
    check("source: ... and it clamps through `view_start`, so the legal "
          "range of a window is stated once and both halves of the model "
          "read it",
          "view_start(" in code_of(LG.view_pos))
    for fn in (LG.view_pos, LG.view_start, LG.Kit._component,
               LG.Kit.component_cells, LG.Kit._component_body):
        nm = getattr(fn, "__name__", "?")
        hits = [n for n in NAMES if f'"{n}"' in code_of(fn)
                or f"'{n}'" in code_of(fn)]
        check(f"source: `{nm}` names NO component in its code — the window "
              f"is a fourth ANATOMY the registry forks, not a scroll bar "
              f"feature. One seat per decision",
              not hits, f"names {hits}")
    check("source: the composer's FOURTH anatomy forks on the REGISTRY — "
          "`name in VIEWED`, a declared fact and not a question about who is "
          "asking. Window / extent / field / presence, four branches, four "
          "registry facts",
          "if name in VIEWED:" in code_of(LG.Kit.component_cells)
          and "view_pos(" in code_of(LG.Kit.component_cells))
    check("source: and the READOUT forks on the same fact — a two-number "
          "value has no one-number label, and that is decided at the "
          "registry beside CHECKABLE rather than at a component's method",
          "if name in VIEWED:" in code_of(LG.Kit._component)
          and "if name in CHECKABLE:" in code_of(LG.Kit._component))
    hits = [n for n in NAMES
            if (f'"{n}"' in code_of(LG.Kit.scrollbar)
                or f"'{n}'" in code_of(LG.Kit.scrollbar)) and n != "scrollbar"]
    check("source: `Kit.scrollbar` names only ITSELF — its own name at its "
          "own seat, the exception the button set and the text field kept",
          not hits, f"names {hits}")

    # -- (5) THE TEXT FIELD ROUTES THROUGH THE SHARED SEAT -----------------
    # SOURCE first, then BEHAVIOUR. The source law says the window arithmetic
    # left this method; the behavioural one says the seat is actually REACHED
    # with the field's own numbers, which a source law cannot see.
    check("source: `Kit.textfield` computes NO window of its own any more — "
          "the five lines the fifty-third pass wrote inline were a measure "
          "with one call site, which is a local variable wearing a view's "
          "name",
          "view_start(" in code_of(LG.Kit.textfield)
          and "- w + 1" not in code_of(LG.Kit.textfield)
          and "len(cols) - w" not in code_of(LG.Kit.textfield))
    _vs, _vp = LG.view_start, LG.view_pos
    scalls, pcalls = [], []
    try:
        LG.view_start = lambda *a, **kw: (scalls.append(a), _vs(*a, **kw))[1]
        LG.view_pos = lambda *a, **kw: (pcalls.append(a), _vp(*a, **kw))[1]
        nk = LG.kit("nord")
        nk.textfield(LONG, 5, FW, LG.EDITED)
        tf_calls, scalls[:] = list(scalls), []
        nk.scrollbar(16, SSZ, STOT, SW)
        sb_calls = list(scalls)
    finally:
        LG.view_start, LG.view_pos = _vs, _vp
    check("behaviour: RENDERING A TEXT FIELD REACHES `view_start`, with the "
          "field's own numbers — the caret's column count, the field's width "
          "and the caret's index. A source law can be satisfied by a call "
          "that is never made; this one cannot",
          tf_calls == [(len(LONG) + 1, FW, 5)], f"{tf_calls}")
    check("behaviour: and RENDERING A SCROLL BAR REACHES BOTH HALVES — "
          "`view_pos` for the cells and `view_start` underneath it for the "
          "clamp. Two components, one window model, and the coupling is "
          "observed rather than asserted",
          pcalls == [(16, SSZ, STOT, SW)] and sb_calls == [(STOT, SSZ, None,
                                                            16)],
          f"pos {pcalls} start {sb_calls}")
    check("behaviour: and the seat is restored — an instrument that left a "
          "recorder installed would carry it into every law after this one",
          LG.view_start is _vs and LG.view_pos is _vp)

    # -- (6) PER LANGUAGE ---------------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        n_cells = k.part_slots("scrollbar", SW)
        trk = k.part_glyph("main", LG.DEFAULT, "scrollbar")
        thb = k.part_glyph("indicator", LG.DEFAULT, "scrollbar")
        check(f"{name}: the shaft and the thumb are SCOPED to this component "
              f"— a slider's track is a SCALE (every cell is a value the "
              f"knob could take) and a scroll bar's is a SHAFT (every cell "
              f"is somewhere the view could be), and they stand side by side "
              f"in the gallery",
              k.part_key("scrollbar", "main") == "scrollbar.main"
              and k.part_key("scrollbar", "indicator")
              == "scrollbar.indicator")
        check(f"{name}: the thumb differs from the shaft in EVERY declared "
              f"state, colour stripped — the two-channel law, and on this "
              f"component it is the whole reading",
              all(k.part_glyph("main", st, "scrollbar")
                  != k.part_glyph("indicator", st, "scrollbar")
                  for st in SB))
        check(f"{name}: the shaft declares EXACTLY the two states a readout "
              f"has — a table with a FOCUSED shaft in it would be dead "
              f"metadata, because the composer would never ask for one",
              set(k.PART_GLYPHS["scrollbar.main"]) <= set(SB)
              and set(k.PART_GLYPHS["scrollbar.indicator"]) <= set(SB))
        check(f"{name}: the parts TILE the shaft — one cell per slot, no gap "
              f"and no overlap, read off the render rather than recomputed",
              len(sb_cells(k, 0)) == n_cells
              and all(len(sb_cells(k, s)) == n_cells
                      for s in (0, SLAST // 2, SLAST)))
        check(f"{name}: every cell is a declared part and nothing else — no "
              f"third glyph creeps into a two-part component",
              all(p in SBP for s in (0, SLAST // 2, SLAST)
                  for p in sb_tags(k, s)))
        runs = {s: sb_run(sb_tags(k, s)) for s in (0, SLAST // 2, SLAST)}
        check(f"{name}: THE THUMB IS ONE CONTIGUOUS RUN at every position — "
              f"a window split in two would be reporting two views",
              all(sb_tags(k, s)[p:p + sp] == ["indicator"] * sp
                  and "indicator" not in sb_tags(k, s)[:p]
                  and "indicator" not in sb_tags(k, s)[p + sp:]
                  for s, (p, sp) in runs.items()), f"{runs}")
        check(f"{name}: THE ENDS ARE REACHABLE — at start 0 the FIRST cell "
              f"of the shaft is thumb, and at the last legal start the LAST "
              f"cell is. Asserted as cells and with no arithmetic in the "
              f"oracle at all, because off-by-one is this component's "
              f"classic defect",
              sb_tags(k, 0)[0] == "indicator"
              and sb_tags(k, 0)[-1] == "main"
              and sb_tags(k, SLAST)[-1] == "indicator"
              and sb_tags(k, SLAST)[0] == "main")
        check(f"{name}: THE THUMB MOVES WITH THE START — three windows, "
              f"three different places, and the middle one is between the "
              f"other two. A bar's extent could not do this: it is anchored",
              runs[0][0] < runs[SLAST // 2][0] < runs[SLAST][0], f"{runs}")
        check(f"{name}: ... and its LENGTH does not move while it travels — "
              f"the two numbers are independent, which is the claim the "
              f"whole seat exists to make",
              len({sp for _, sp in runs.values()}) == 1, f"{runs}")
        big = sb_run(sb_tags(k, 0, size=SBIG))
        check(f"{name}: THE THUMB'S LENGTH IS THE VIEW SIZE — the same "
              f"position with three times the window gives a longer thumb, "
              f"and that is the second number nothing else in this contract "
              f"has",
              big[1] > runs[0][1] and big[0] == 0,
              f"{SSZ}->{runs[0][1]} cells, {SBIG}->{big[1]}")
        check(f"{name}: ... and a window that covers the whole content FILLS "
              f"the shaft — 'there is nothing to scroll', said in shape",
              sb_tags(k, 0, size=STOT) == ["indicator"] * n_cells)
        # THE DECLARED COMPOSITION — the oracle builds the whole expected
        # string from the glyph table and the pinned seat, never from the
        # composer under test (pass 53's third defect, cured at the seat it
        # was cured for and applied here from the start).
        for st in SB:
            g_trk = k.part_glyph("main", st, "scrollbar")
            g_thb = k.part_glyph("indicator", st, "scrollbar")
            o_, c_ = k.comp_chrome("scrollbar")
            for s_ in (0, SLAST // 3, SLAST):
                p_, sp_ = LG.view_pos(s_, SSZ, STOT, n_cells)
                want = o_ + k.SLOT_SEP.join(
                    g_thb if p_ <= i < p_ + sp_ else g_trk
                    for i in range(n_cells)) + c_
                check(f"{name}: the {st} scroll bar at start {s_} is exactly "
                      f"its DECLARED glyphs composed — shaft everywhere, "
                      f"thumb across the window, this language's own "
                      f"separator and chrome. Read off the table, not "
                      f"through the code under test",
                      sbp(k, s_, st=st) == want,
                      f"{sbp(k, s_, st=st)!r} vs declared {want!r}")
        # THE READING ITSELF, in greyscale — added in round two of this
        # pass's mutation table, because a thumb drawn as its own shaft
        # scored ONE red across ten languages and one red is not a law with
        # teeth. The laws above read PART TAGS, which survive a language
        # drawing both parts the same; these read what the eye gets.
        pgreys = [sbp(k, s) for s in (0, SLAST // 2, SLAST)]
        check(f"{name}: the three POSITIONS are three different strings with "
              f"the colour taken away — a scroll bar whose thumb cannot be "
              f"told from its shaft reports nothing, however correctly its "
              f"cells are tagged",
              len(set(pgreys)) == 3, f"{pgreys}")
        check(f"{name}: ... and a bigger WINDOW reads differently from a "
              f"smaller one at the same position, greyscale — the second "
              f"number reaches the eye and not only the tags",
              sbp(k, 0) != sbp(k, 0, size=SBIG))
        greys = {st: sbp(k, SLAST // 2, st=st) for st in SB}
        check(f"{name}: DISABLED is SHAPE-marked — a dead scroll bar must "
              f"read dead with the colour taken away",
              len(set(greys.values())) == len(SB)
              and greys[LG.DISABLED] != greys[LG.DEFAULT], str(greys))
        check(f"{name}: NOTHING IS PRINTED BESIDE IT — a readout that "
              f"printed one number would name the position and hide the "
              f"size, or name the size and hide the position. This is the "
              f"first component whose value IS its own readout",
              sbp(k, 8) == Text.from_markup(
                  k._component_body("scrollbar", 8, 0, STOT, SW,
                                    LG.DEFAULT, SSZ)).plain
              and len(sbp(k, 8)) == len(sbp(k, 0)))
        check(f"{name}: NO ACCENT ANYWHERE ON IT — the accent is spent on "
              f"the part under the finger and there is no finger here. The "
              f"tone rule reached that answer as a READOUT, with no special "
              f"case: every tone is byte-identical to the bar's",
              all(k.part_tone(p, st, "scrollbar")
                  == k.part_tone(p, st, "bar") for p in SBP for st in SB)
              and k.c["accent"] not in {k.part_tone(p, st, "scrollbar")
                                        for p in SBP for st in SB})
        for st in SB:
            s_ = k.scrollbar(SLAST // 2, SSZ, STOT, SW, st)
            check(f"{name}: the {st} scroll bar parses IDENTICALLY under "
                  f"rich and under Textual — the app renders with the second",
                  Text.from_markup(s_).plain == Content.from_markup(s_).plain
                  and "[/]" not in Content.from_markup(s_).plain,
                  f"rich {Text.from_markup(s_).plain!r}")
        check(f"{name}: a NARROWER shaft still carries a position and an "
              f"extent — both are fractions, so it renounces resolution and "
              f"never the reading. This is the text field's reflow, not the "
              f"button's",
              sb_run(sb_tags(k, SLAST, w=6))[1] >= 1
              and sb_tags(k, SLAST, w=6)[-1] == "indicator"
              and sb_tags(k, 0, w=6)[0] == "indicator")

    # -- (7) CROSS-LANGUAGE -------------------------------------------------
    ssig = {n: "|".join(sbp(LG.kit(n), s, st=st)
                        for st in SB for s in (0, SLAST // 2, SLAST))
            for n in TH.ORDER}
    check("no two languages draw the same scroll bar in greyscale",
          len(set(ssig.values())) == len(TH.ORDER),
          f"{len(set(ssig.values()))} distinct of {len(TH.ORDER)}")
    check("and NO LANGUAGE draws its scroll bar the way it draws its BAR — "
          "same parts, same states, and the shaft is not the scale",
          all(sbp(LG.kit(n), SLAST // 2)
              != Text.from_markup(LG.kit(n).readbar(5, 0, 10, SW)).plain
              for n in TH.ORDER))
    print("  shafts and thumbs, per language: "
          + "  ".join(f"{n}={LG.kit(n).part_glyph('main', LG.DEFAULT, 'scrollbar')}"
                      f"{LG.kit(n).part_glyph('indicator', LG.DEFAULT, 'scrollbar')}"
                      for n in TH.ORDER))

    # -- (8) CONTROLS: the per-language laws, driven red on purpose --------
    class _FlatShaft(LG.Kit):
        """A language whose thumb IS its shaft — the window disappears, and
        the whole two-channel reading with it."""
        PART_GLYPHS = dict(LG.Kit.PART_GLYPHS,
                           **{"scrollbar.indicator":
                              dict(LG.Kit.PART_GLYPHS["scrollbar.main"])})

    fs = _FlatShaft("nord")
    check("control: a thumb drawn as the shaft fails the two-channel law, "
          "and the three positions become ONE string — which is what a "
          "colour-only scroll bar actually is",
          fs.part_glyph("indicator", LG.DEFAULT, "scrollbar")
          == fs.part_glyph("main", LG.DEFAULT, "scrollbar")
          and len({Text.from_markup(fs.scrollbar(s, SSZ, STOT, SW)).plain
                   for s in (0, SLAST // 2, SLAST)}) == 1)

    class _AnchoredBar(LG.Kit):
        """A scroll bar that renders its start as a bar would — anchored at
        cell 0, length carrying the position. The exact confusion `VIEWED`
        exists to make impossible."""
        def scrollbar(self, start, size, total, w=12, state=LG.DEFAULT):
            return self._component("bar", start, 0, total, w, state)

    ab = _AnchoredBar("nord")
    check("control: a scroll bar drawn as a BAR cannot reach the bottom of "
          "its own track — the ends law has teeth, and this is what it "
          "catches",
          Text.from_markup(ab.scrollbar(SLAST, SSZ, STOT, SW)).plain[-1]
          != Text.from_markup(ab.scrollbar(SLAST, SSZ, STOT, SW)).plain[0])

    class _FixedThumb(LG.Kit):
        """A thumb whose length ignores the view size — one cell, always.
        The second number, silently dropped."""
        def scrollbar(self, start, size, total, w=12, state=LG.DEFAULT):
            return super().scrollbar(start, 1, total, w, state)

    ft = _FixedThumb("nord")
    check("control: a thumb of fixed length says nothing about HOW MUCH is "
          "in view — the size law goes red, and a small window and a huge "
          "one draw the same bar",
          Text.from_markup(ft.scrollbar(0, SSZ, STOT, SW)).plain
          == Text.from_markup(ft.scrollbar(0, SBIG, STOT, SW)).plain)

    # -- (9) THE GALLERY SEAT ----------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        block = scrollbar_block(k, GAL_W)
        check(f"{name}: the gallery's scroll-bar block FITS the {GAL_W}-"
              f"column box",
              max(len(grey(r)) for r in block) <= GAL_W,
              f"widest {max(len(grey(r)) for r in block)}, {len(block)} rows")
        check(f"{name}: ... it draws a head, three POSITIONS, one bigger "
              f"WINDOW and one row per non-default state the registry "
              f"declares — derived, so a scroll bar that ever grew an "
              f"actuator would grow rows here without this block being "
              f"touched",
              len(block) == 5 + len(SB) - 1, f"{len(block)} rows")
        body = "\n".join(grey(r) for r in block)
        check(f"{name}: ... the three position rows are the SAME window at "
              f"top, middle and bottom — the ends and the middle, which is "
              f"what the block exists to show",
              all(grey(k.scrollbar(s, SB_SIZE, SB_TOTAL, SB_W)) in body
                  for s in (0, (SB_TOTAL - SB_SIZE) // 2,
                            SB_TOTAL - SB_SIZE)))
        check(f"{name}: ... and the fourth row keeps the position and grows "
              f"the WINDOW, so the only thing that changes is the thumb's "
              f"length",
              grey(k.scrollbar(0, SB_BIG, SB_TOTAL, SB_W)) in body)
        narrow = scrollbar_block(k, 24)
        check(f"{name}: ... it REFLOWS BY NARROWING THE SHAFT — a shorter "
              f"track still carries both fractions, so it renounces "
              f"resolution and never the reading",
              max(len(grey(r)) for r in narrow)
              < max(len(grey(r)) for r in scrollbar_block(k, 200))
              and len(narrow) == len(block))

    print("\n== KIT LEVEL: the COMPONENT CONTRACT — the STEPPER (wrap vs clamp)")
    # THE EIGHTH AND LAST COMPONENT, and its question is the first one in this
    # contract that is not about what a range IS but about what happens at its
    # END. Two rulings carry the increment and both are falsifiable:
    #
    #   (1) A STEPPER AND A RADIO ARE ONE CHOICE WITH TWO MECHANISMS. Two
    #       registry entries, because their ANATOMIES differ (a well and a
    #       mark, N times, versus a word between two steps); ONE choice model,
    #       because `group_states` already owns "one index into a set" and the
    #       stepper reaches it. That is the INVERSE of every collision this
    #       registry has met — switch/slider and scrollbar/bar shared a tuple
    #       and differed in the value, and were separated by a declared fact.
    #   (2) WRAP VS CLAMP IS AN ARGUMENT, NOT A FACT. A registry fact would say
    #       something about every stepper; wrap is true of every RING, and this
    #       app holds both readings already (`action_cycle_theme` wraps because
    #       a list of languages is a ring, `action_pick` clamps because a set
    #       of worker groups is not). It is visible in SHAPE: a seat with no
    #       step draws GROUND, so the ends of a clamped stepper differ from a
    #       wrapping one's with the colour taken away.
    #
    # ORACLE INDEPENDENCE, designed in as the scroll bar's was: `step_index` is
    # pinned by PROPERTY laws that recompute nothing, and the render laws then
    # compose their whole expectation from the DECLARED glyph table plus that
    # pinned seat.
    ST = CS["stepper"]
    STP = LG.COMPONENT_PARTS["stepper"]
    SOPTS = ("lo", "mid", "high")          # DIFFERENT widths: the jiggle bench
    SN = len(SOPTS)

    def st_cells(k, i, st=LG.DEFAULT, wrap=False, n=SN):
        return k.component_cells("stepper", i, 0, n - 1, 1, st, wrap=wrap)

    def st_tags(k, *a, **kw):
        return [p for p, _, _ in st_cells(k, *a, **kw)]

    def stp(k, i, st=LG.DEFAULT, wrap=False, opts=SOPTS, w=0):
        return Text.from_markup(k.stepper(opts, i, w, st, wrap)).plain

    def walk(n, d, wrap, steps=None):
        """Every seat a stepper actually reaches, by STEPPING — the
        reachability claim asked by walking rather than asserted."""
        i, seen = (0 if d > 0 else n - 1), []
        for _ in range(n + 4 if steps is None else steps):
            seen.append(i)
            nxt = LG.step_index(i, n, d, wrap)
            if nxt is None:
                break
            i = nxt
        return seen

    # -- (1) THE REGISTRY: a new anatomy, and NO new declared fact ----------
    check("registry: the stepper declares `(main, step)` — a word between two "
          "steps. It is the first tuple in this registry that is not a track, "
          "a box or a field, and the one new PART is what makes it one",
          STP == ("main", "step") and "step" not in
          {p for n in NAMES if n != "stepper"
           for p in LG.COMPONENT_PARTS[n]})
    check("registry: and NO NEW DECLARED FACT — `CHECKABLE` and `VIEWED` are "
          "byte-identical to what the scroll bar left them. The fifty-fourth "
          "pass warned that a third family would be a smell; this component "
          "answered by growing the ANATOMY instead, which is what the parts "
          "registry is for",
          LG.CHECKABLE == ("switch", "checkbox", "radio")
          and LG.VIEWED == ("scrollbar",)
          and "stepper" not in LG.CHECKABLE and "stepper" not in LG.VIEWED)
    check("registry: `GRIPS` grew instead, and that is the CHEAP kind of "
          "growth — a step is pressed, so it is the part under the finger, "
          "and `actuator` did not gain a term to learn that",
          LG.GRIPS == ("knob", "caret", "step")
          and LG.actuator("stepper") == "step")
    check("registry: THE PARTS DIFFER FROM THE RADIO'S, which is why this is "
          "two entries and not one. A radio ITEM is a well and a mark drawn N "
          "times; a stepper is two affordances whatever the set's size — the "
          "same choice cannot be one anatomy",
          STP != LG.COMPONENT_PARTS["radio"]
          and STP != LG.COMPONENT_PARTS["checkbox"])
    check("registry: ... and no OTHER component's tuple is `(main, step)` — "
          "the collision this registry refuses is identical parts with "
          "different anatomies, and it has not made one here",
          [n for n in NAMES if LG.COMPONENT_PARTS[n] == STP] == ["stepper"])
    check("registry: it HOLDS a value — the seat it is at is a number the "
          "registry can read, which a text field's content is not. That is "
          "the third term `has_value` took, and the pair it makes with "
          "`has_interior` is the whole content ruling: a caret indexes cells "
          "the CALLER fills, a step chooses among seats the registry counts",
          LG.has_value("stepper") and not LG.has_value("textfield")
          and LG.has_interior("stepper") and LG.has_interior("textfield"))
    check("registry: EDITED IS THE STEPPER'S HOME, and it is derived and not "
          "granted — a grip AND an interior AND not a boolean. On a slider "
          "EDITED means the arrows now move the value; here the arrows ARE "
          "the component, so this is the state the axis was built for",
          ST == (LG.DEFAULT, LG.FOCUSED, LG.EDITED, LG.ACTIVE, LG.INVALID,
                 LG.DISABLED) == CS["slider"], f"{ST}")
    check("registry: ... and no OTHER component's axis moved — a new part "
          "that changed an old component's states would be a refactor "
          "wearing an increment's clothes",
          {n: CS[n] for n in NAMES if n != "stepper"}
          == {n: LG.component_states(n) for n in NAMES if n != "stepper"})
    sig_cc = inspect.signature(LG.Kit.component_cells)
    opt_state = [p for p, v in sig_cc.parameters.items() if v.default is None]
    check("registry: THE COMPOSER'S OPTIONAL STATE ARGUMENTS ARE STILL TWO — "
          "`caret` and `size`, the ones that default to 'nobody said'. `wrap` "
          "defaults to False because it is a RANGE word standing beside `lo` "
          "and `hi`: whether the scale closes on itself, which says nothing "
          "about where the value is. That is the fifty-fourth pass's warning "
          "answered by a distinction rather than ignored",
          opt_state == ["caret", "size"]
          and sig_cc.parameters["wrap"].default is False
          and 0 <= at(list(sig_cc.parameters), "wrap")
          < at(list(sig_cc.parameters), "caret"), f"{opt_state}")

    # -- (2) CONTROLS on the registry: a new component, no hand lists -------
    LG.COMPONENT_PARTS["_probe_step"] = ("main", "step")
    try:
        LG.COMPONENT_STATES["_probe_step"] = LG.component_states("_probe_step")
        check("control: a NEW component declaring `(main, step)` gets the "
              "stepper's whole axis, its grip and its interior with zero "
              "edits at any seat — the fifth anatomy belongs to the REGISTRY, "
              "not to the stepper",
              LG.component_states("_probe_step") == ST
              and LG.actuator("_probe_step") == "step"
              and LG.has_interior("_probe_step")
              and LG.has_value("_probe_step"))
        class _ProbeKit(LG.Kit):
            """The probe's OWN glyph table, scoped to the probe. A component
            with no scoped entry falls back to the bare part name, and no
            language declares a bare `step` — the same deliberate fallback
            the caret has, and the same reason it is never exercised."""
            PART_GLYPHS = dict(LG.Kit.PART_GLYPHS, **{
                "_probe_step.main":
                    dict(LG.Kit.PART_GLYPHS["stepper.main"]),
                "_probe_step.step":
                    dict(LG.Kit.PART_GLYPHS["stepper.step"])})

        ptags = [p for p, _, _ in _ProbeKit("nord").component_cells(
            "_probe_step", 0, 0, SN - 1, 1, LG.DEFAULT)]
        check("control: ... and it draws GROUND at the floor it cannot step "
              "off, exactly as the stepper does. One tuple, one mechanism",
              ptags == st_tags(LG.kit("nord"), 0) == ["main", "step"])
    finally:
        del LG.COMPONENT_PARTS["_probe_step"]
        LG.COMPONENT_STATES.pop("_probe_step", None)
    _sg = LG.GRIPS
    try:
        LG.GRIPS = ("knob", "caret")
        check("control: take `step` OUT of GRIPS and the stepper stops being "
              "a control — no grip, a value, therefore a READOUT with two "
              "states. The affordance is the registry's claim, and this is "
              "what it is worth",
              LG.actuator("stepper") is None
              and LG.component_states("stepper") == CS["bar"])
    finally:
        LG.GRIPS = _sg
    check("control: GRIPS is restored", LG.GRIPS == ("knob", "caret", "step")
          and LG.actuator("stepper") == "step")

    # -- (3) THE SEAT: `step_index`, with no language in sight -------------
    # PROPERTY laws. None recomputes the arithmetic; each states something the
    # contract PROMISES, so a mutation inside the seat cannot move with them.
    for sn in (1, 2, 3, 7):
        check(f"seat: CLAMPED, the ends have NO STEP OFF at n={sn} — the "
              f"floor cannot go back and the ceiling cannot go on. That is "
              f"what a clamp IS, and it is `None` rather than a repeat of the "
              f"seat you are already at, because 'nothing happened' and 'you "
              f"moved to where you were' are different claims",
              LG.step_index(0, sn, -1, False) is None
              and LG.step_index(sn - 1, sn, 1, False) is None)
        check(f"seat: ... and every INTERIOR seat has both at n={sn} — a "
              f"clamp takes away exactly two steps and no others",
              all(LG.step_index(i, sn, -1, False) == i - 1
                  and LG.step_index(i, sn, 1, False) == i + 1
                  for i in range(1, sn - 1)))
        check(f"seat: WRAPPING, EVERY seat has both at n={sn} — a ring has no "
              f"end, which is the whole difference and the only one",
              all(LG.step_index(i, sn, d, True) is not None
                  for i in range(sn) for d in (-1, 1)))
        check(f"seat: ... and the ends JOIN at n={sn}: the ceiling steps on "
              f"to the floor and the floor steps back to the ceiling",
              LG.step_index(sn - 1, sn, 1, True) == 0
              and LG.step_index(0, sn, -1, True) == sn - 1)
        check(f"seat: a step of ZERO is the seat you are on, wrapped or not "
              f"at n={sn} — the identity, which is what makes 'no step' mean "
              f"something",
              all(LG.step_index(i, sn, 0, w) == i
                  for i in range(sn) for w in (False, True)))
        check(f"seat: a step LANDS INSIDE the set at n={sn}, from every seat, "
              f"in both directions, both readings — a stepper that stepped "
              f"out of its own set would be the out-of-range selection the "
              f"group seat refuses",
              all(j is None or 0 <= j < sn
                  for i in range(sn) for d in (-3, -1, 1, 4) for w in (0, 1)
                  for j in (LG.step_index(i, sn, d, bool(w)),)))
        check(f"seat: WALKING the set one step at a time reaches every seat "
              f"at n={sn} and STOPS at the ceiling — the reachability claim, "
              f"asked by walking rather than asserted",
              walk(sn, 1, False) == list(range(sn))
              and walk(sn, -1, False) == list(range(sn - 1, -1, -1)))
        check(f"seat: ... and WRAPPING it returns to where it started after "
              f"exactly n steps at n={sn}, never sooner — a ring with a short "
              f"circuit would be a set with a repeat in it",
              walk(sn, 1, True, sn + 1) == list(range(sn)) + [0]
              and len(set(walk(sn, 1, True, sn))) == sn)
    check("seat: an out-of-range seat CLAMPS rather than raising — the RAISE "
          "lives at `group_states`, which is where the CHOICE lives, and a "
          "renderer that died on a caller's number would take the surface "
          "with it. Two seats, one refusal, and it is at the one that owns "
          "the invariant",
          LG.step_index(-9, SN, 1, False) == LG.step_index(0, SN, 1, False)
          and LG.step_index(99, SN, -1, False)
          == LG.step_index(SN - 1, SN, -1, False))
    try:
        LG.step_index(0, 0, 1, False)
        raised = False
    except ValueError:
        raised = True
    check("seat: ... but a set with NO SEATS raises, exactly as a group with "
          "no items does. A stepper through nothing is not a stepper", raised)
    check("seat: `step_index` TAKES NO DEFAULT for wrap, and the vacuity "
          "prover is what found that: it had one, no caller ever reached it "
          "(both composing seats state their reading), and a value nothing "
          "can observe is dead metadata. The seat that DECIDES an end is "
          "always told which end it is deciding; the DEFAULT lives at the "
          "two seats a caller actually omits it at",
          inspect.signature(LG.step_index).parameters["wrap"].default
          is inspect.Parameter.empty
          and inspect.signature(LG.Kit.stepper).parameters["wrap"].default
          is False
          and inspect.signature(
              LG.Kit.component_cells).parameters["wrap"].default is False)
    check("seat: `step_index` is the ONLY place wrap is decided — it names no "
          "component and no language, so a ring is a property of a caller's "
          "range and never of a control",
          not any(f'"{n}"' in code_of(LG.step_index) for n in NAMES)
          and "wrap" in code_of(LG.step_index))
    check("source: the composer asks THE SAME SEAT whether a step exists — "
          "one function for the render and for the behaviour, so a stepper "
          "cannot draw a live arrow that does nothing. Not 'does not': "
          "cannot, by construction",
          "step_index(" in code_of(LG.Kit.component_cells))
    check("source: the composer's FIFTH anatomy forks on the REGISTRY — "
          "`step in parts`, a fact about parts and not about who is asking. "
          "Series / window / field / extent / presence, five branches, five "
          "registry facts",
          '"step" in parts' in code_of(LG.Kit.component_cells)
          and '"step" in COMPONENT_PARTS[name]' in code_of(LG.Kit.part_slots))
    for fn in (LG.step_index, LG.has_value, LG.has_interior, LG.actuator,
               LG.component_states, LG.Kit.component_cells, LG.Kit.part_slots,
               LG.Kit.part_tone):
        nm = getattr(fn, "__name__", "?")
        hits = [n for n in NAMES if f'"{n}"' in code_of(fn)
                or f"'{n}'" in code_of(fn)]
        check(f"source: `{nm}` names NO component in its code — the stepper "
              f"inherited the axis, the tone rule and the composer's fifth "
              f"anatomy rather than being granted them",
              not hits, f"names {hits}")
    hits = [n for n in NAMES
            if (f'"{n}"' in code_of(LG.Kit.stepper)
                or f"'{n}'" in code_of(LG.Kit.stepper)) and n != "stepper"]
    check("source: `Kit.stepper` names only ITSELF — its own name at its own "
          "seat, the exception the button set and every component since has "
          "kept", not hits, f"names {hits}")
    check("source: and it appends NO readout — `value_label` is unreachable "
          "from it, because what a stepper reports is standing in the middle "
          "of it, in the caller's own bytes",
          "value_label" not in code_of(LG.Kit.stepper)
          and "check_label" not in code_of(LG.Kit.stepper))

    # -- (4) THE CHOICE MODEL: one seat, two mechanisms ---------------------
    # SOURCE first, then BEHAVIOUR, then the UNIFICATION itself. The source
    # law says the group seat is named; the call recorder says it is REACHED
    # with the set's own numbers, because a source law can be satisfied by a
    # call that is never made (pass 54's M9, and the lesson is kept).
    check("source: `Kit.stepper` reaches `group_states` — the radio's seat, "
          "and the stepper does not get a second one. A stepper through a "
          "named set and a radio over it are ONE CHOICE",
          "group_states(" in code_of(LG.Kit.stepper))
    check("source: ... and it takes NO `on` argument, exactly as the group "
          "render does not — the bit is computed from the index, so a "
          "stepper cannot show an option that is not the chosen one",
          "on" not in inspect.signature(LG.Kit.stepper).parameters
          and "with_checked(" not in code_of(LG.Kit.stepper))
    _gs = LG.group_states
    gcalls = []
    try:
        LG.group_states = lambda *a, **kw: (gcalls.append((a, kw)),
                                            _gs(*a, **kw))[1]
        LG.kit("nord").stepper(SOPTS, 2, 0, LG.FOCUSED)
    finally:
        LG.group_states = _gs
    check("behaviour: RENDERING A STEPPER REACHES `group_states`, with the "
          "set's own size and its own index — the coupling is observed, not "
          "asserted, and the seat is restored afterwards",
          gcalls == [((SN, 2, LG.FOCUSED), {"focus": 2})]
          and LG.group_states is _gs, f"{gcalls}")
    for i in range(SN):
        for ctl in (LG.DEFAULT, LG.FOCUSED, LG.EDITED, LG.ACTIVE,
                    LG.DISABLED):
            want = LG.group_states(SN, i, ctl, focus=i)[i]
            k = LG.kit("nord")
            check(f"unification: at seat {i} in {ctl} the option a STEPPER "
                  f"shows carries the state of the item a RADIO would MARK — "
                  f"one seat, so the two mechanisms cannot disagree about "
                  f"what is chosen, and the WORD's tone is that answer",
                  LG.is_checked(want)
                  and f"[{k.check_tone(True, want)}]"
                  in k.stepper(SOPTS, i, 0, ctl))
    for i in range(SN):
        k = LG.kit("nord")
        item = Text.from_markup(k.radio_items(SOPTS, i, LG.DEFAULT)[i]).plain
        check(f"unification: ... and BOTH mechanisms print the same OPTION "
              f"for the same index ({i}) — the radio beside its mark, the "
              f"stepper between its steps. Same set, same index, same word",
              SOPTS[i] in item and SOPTS[i] in stp(k, i))
    for bad in (-1, SN, SN + 4):
        # THE EXCEPTION TYPE IS PART OF THE CLAIM, and catching only the right
        # one would let a WRONG one kill the run instead of failing it — the
        # dead-run defect this file has now paid for twice. What is asserted
        # is that it raised AND that it was the group seat's ValueError; an
        # IndexError out of a list lookup is a different bug and reads red.
        try:
            LG.kit("nord").stepper(SOPTS, bad)
            err = None
        except Exception as e:                 # noqa: BLE001 — see above
            err = type(e).__name__
        check(f"unification: an out-of-range selection ({bad}) RAISES, and it "
              f"raises from the GROUP seat — a stepper showing no option is "
              f"the same defect as a set with nothing set, refused in the "
              f"same place and by the same expression. A stepper that indexed "
              f"its own list first would raise an IndexError instead, which "
              f"is this check's negative reading",
              err == "ValueError", f"raised {err}")

    # -- (5) PER LANGUAGE ---------------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        check(f"{name}: the step and the ground are SCOPED to this component "
              f"— a stepper's ground is not a slider's track, and a language "
              f"drawing them from one table would be claiming a seat and a "
              f"scale are the same thing",
              k.part_key("stepper", "main") == "stepper.main"
              and k.part_key("stepper", "step") == "stepper.step")
        check(f"{name}: BOTH GLYPH STRINGS ARE EVEN in every declared state — "
              f"the halves are the two directions, and an odd string would "
              f"have no halves to be",
              all(len(g) % 2 == 0
                  for key in ("stepper.main", "stepper.step")
                  for g in k.PART_GLYPHS[key].values()))
        check(f"{name}: ... and the STEP and the GROUND are the SAME WIDTH in "
              f"every state — the anti-jiggle reservation at the glyph table "
              f"itself, because a dead end that was narrower would move the "
              f"word the moment you reached a floor",
              len({len(k.part_glyph(p, st, "stepper"))
                   for p in STP for st in ST}) == 1,
              str({p: {st: k.part_glyph(p, st, "stepper") for st in ST}
                   for p in STP}))
        check(f"{name}: the step differs from the ground in EVERY state, "
              f"colour stripped — the two-channel law, and on this component "
              f"it is the entire end-behaviour channel",
              all(k.part_glyph("main", st, "stepper")
                  != k.part_glyph("step", st, "stepper") for st in ST))
        check(f"{name}: the tables declare only states this component HAS — a "
              f"glyph for a state the composer can never ask for is dead "
              f"metadata",
              set(k.PART_GLYPHS["stepper.main"]) <= set(ST)
              and set(k.PART_GLYPHS["stepper.step"]) <= set(ST))
        check(f"{name}: it composes exactly TWO cells — the two ways out of a "
              f"seat, and `w` dies at that boundary the way it dies at a "
              f"checkbox's. There is no third direction",
              all(len(st_cells(k, i, st, wr)) == 2 for i in range(SN)
                  for st in ST for wr in (False, True))
              and k.part_slots("stepper", 40) == 2)
        check(f"{name}: every cell is a declared part and nothing else",
              all(p in STP for i in range(SN) for wr in (False, True)
                  for p in st_tags(k, i, wrap=wr)))
        check(f"{name}: CLAMPED, THE FLOOR SHOWS ITS FLOOR — the seat where "
              f"the step back would be is GROUND, and the ceiling's forward "
              f"seat is too. Read off the render's own part tags",
              st_tags(k, 0) == ["main", "step"]
              and st_tags(k, SN - 1) == ["step", "main"]
              and st_tags(k, 1) == ["step", "step"])
        check(f"{name}: WRAPPING, NO SEAT IS EVER GROUND — a ring has no end "
              f"to draw, at any index, which is the whole visible difference "
              f"between the two readings",
              all(st_tags(k, i, wrap=True) == ["step", "step"]
                  for i in range(SN)))
        check(f"{name}: and the two readings DIFFER IN GREYSCALE at the ends "
              f"and AGREE in the middle — the end behaviour reaches the eye, "
              f"not only the tags, and it changes nothing where there is no "
              f"end to change",
              stp(k, 0) != stp(k, 0, wrap=True)
              and stp(k, SN - 1) != stp(k, SN - 1, wrap=True)
              and stp(k, 1) == stp(k, 1, wrap=True))
        for st in ST:
            g_m = k.part_glyph("main", st, "stepper")
            g_s = k.part_glyph("step", st, "stepper")
            h = len(g_s) // 2
            field = max(len(o) for o in SOPTS)
            for wr in (False, True):
                for i in range(SN):
                    back = LG.step_index(i, SN, -1, wr) is not None
                    fwd = LG.step_index(i, SN, 1, wr) is not None
                    want = ((g_s if back else g_m)[:h] + SOPTS[i].center(field)
                            + (g_s if fwd else g_m)[h:])
                    check(f"{name}: the {st} stepper at seat {i} "
                          f"({'wrap' if wr else 'clamp'}) is exactly its "
                          f"DECLARED glyphs composed around the caller's "
                          f"word — read off the table, not through the code "
                          f"under test",
                          stp(k, i, st, wr) == want,
                          f"{stp(k, i, st, wr)!r} vs declared {want!r}")
        for i, o in enumerate(SOPTS):
            check(f"{name}: the option `{o}` comes back BYTE FOR BYTE — never "
                  f"recased, never letterspaced, never shortened. The steps "
                  f"are the language's and the word is the caller's, which is "
                  f"the button's ruling at its third component",
                  o in stp(k, i) and o in stp(k, i, LG.DISABLED)
                  and o in stp(k, i, LG.EDITED, True))
        widths = {len(stp(k, i, st, wr)) for i in range(SN) for st in ST
                  for wr in (False, True)}
        check(f"{name}: ONE WIDTH ACROSS THE WHOLE SET — every option, every "
              f"state, both readings. The field is reserved for the WIDEST "
              f"option (`lo` is two cells and `high` is four), so spinning "
              f"the set cannot move the control's edges. Bodmer T2, and the "
              f"one defect only this component can have",
              len(widths) == 1, f"widths {widths}")
        check(f"{name}: ... and a `w` BELOW the widest word does nothing — a "
              f"stepper cannot truncate the word that says what it is set "
              f"to, so `w` is a minimum exactly as it is on a button",
              stp(k, 2, w=1) == stp(k, 2) == stp(k, 2, w=len("high")))
        check(f"{name}: ... and a `w` ABOVE it grows the field and keeps the "
              f"word whole — a caller with a column of steppers can line them "
              f"up without any of them lying",
              len(stp(k, 2, w=9)) == len(stp(k, 2)) + (9 - len("high"))
              and "high" in stp(k, 2, w=9))
        greys = {st: stp(k, 1, st) for st in ST}
        check(f"{name}: all five states are pairwise distinct with the colour "
              f"taken away, and EDITED is not FOCUSED — the state this "
              f"component exists for, and the one a touch corpus styles 0 "
              f"times in 1848",
              len(set(greys.values())) == len(ST)
              and {LG.EDITED, LG.FOCUSED} <= set(greys)
              and greys[LG.EDITED] != greys[LG.FOCUSED], str(greys))
        check(f"{name}: DISABLED is SHAPE-marked at every seat of the set — a "
              f"dead stepper must read dead with the colour stripped",
              all(stp(k, i, LG.DISABLED) != stp(k, i) for i in range(SN)))
        # A DICT KEYED BY THE DERIVED AXIS IS INDEXED WITH `in` FIRST, always.
        # Pass 52's mutation GREW the axis and pass 53's SHRANK it; both threw
        # KeyError out of an oracle and both cost a DEAD RUN, where a raised
        # law reports nothing at all. Here the membership IS the claim, so a
        # mutation that takes EDITED away reads red instead of killing the
        # suite.
        grip_tone = {st: k.part_tone("knob", st, "slider") for st in ST}
        live = (LG.FOCUSED, LG.EDITED, LG.ACTIVE)
        check(f"{name}: THE STEP WEARS THIS LANGUAGE'S OWN GRIP TONE — "
              f"whatever that language spends on the part under the finger, "
              f"reached through `actuator` with no special case. Asserted "
              f"against the SLIDER'S KNOB rather than against `accent`, "
              f"because one language rations its red and overrules the base "
              f"rule, and the ration must reach this component too",
              all(k.part_tone("step", st, "stepper") == grip_tone[st]
                  for st in ST) and set(live) <= set(ST)
              and k.part_tone("step", LG.DISABLED, "stepper") == k.c["dim"])
        check(f"{name}: ... and the GROUND never wears it — a dead end is not "
              f"a live one in a different colour, and the two seats differ in "
              f"TONE as well as in shape in every live state",
              set(live) <= set(ST)
              and all(k.part_tone("main", st, "stepper") != grip_tone[st]
                      for st in live))
        check(f"{name}: ... so at a clamped floor the grip tone is spent on "
              f"ONE side only, and on BOTH when the range is a ring. The "
              f"tone rule agreeing with the shape rule, which is what two "
              f"channels means",
              LG.FOCUSED in grip_tone
              and [t for _, _, t in st_cells(k, 0, LG.FOCUSED)].count(
                  grip_tone[LG.FOCUSED]) == 1
              and [t for _, _, t in st_cells(k, 1, LG.FOCUSED, True)].count(
                  grip_tone[LG.FOCUSED]) == 2)
        for st in ST:
            s_ = k.stepper(SOPTS, 1, 0, st)
            check(f"{name}: the {st} stepper parses IDENTICALLY under rich "
                  f"and under Textual — the app renders with the second",
                  Text.from_markup(s_).plain == Content.from_markup(s_).plain
                  and "[/]" not in Content.from_markup(s_).plain,
                  f"rich {Text.from_markup(s_).plain!r}")
        marks = set("".join(k.PART_GLYPHS["stepper.step"].values())
                    + "".join(k.PART_GLYPHS["stepper.main"].values()))
        check(f"{name}: NOTHING IS PRINTED BESIDE IT — no number and no word "
              f"of the language's own. Take the two seats away and what is "
              f"left is the caller's option and nothing else, which is "
              f"`has_value` reaching the button's arrangement from the other "
              f"side",
              stp(k, 1).strip("".join(marks)).strip() == "mid",
              f"{stp(k, 1)!r}")

    # -- (6) CROSS-LANGUAGE -------------------------------------------------
    stsig = {n: "|".join(stp(LG.kit(n), i, st, wr) for st in ST
                         for wr in (False, True) for i in range(SN))
             for n in TH.ORDER}
    check("no two languages draw the same stepper in greyscale",
          len(set(stsig.values())) == len(TH.ORDER),
          f"{len(set(stsig.values()))} distinct of {len(TH.ORDER)}")
    check("and NO LANGUAGE draws its stepper the way it draws its RADIO — "
          "one choice, two mechanisms, and a language that drew them alike "
          "would be saying the mechanisms are the same",
          all(stp(LG.kit(n), 1)
              != Text.from_markup(LG.kit(n).radio_group(SOPTS, 1)).plain
              for n in TH.ORDER))
    print("  steps and grounds, per language: "
          + "  ".join(
              f"{n}={LG.kit(n).part_glyph('step', LG.DEFAULT, 'stepper')}"
              f"/{LG.kit(n).part_glyph('main', LG.DEFAULT, 'stepper')}"
              for n in TH.ORDER))

    # -- (7) CONTROLS: the per-language laws, driven red on purpose --------
    class _FlatStep(LG.Kit):
        """A language whose step IS its ground — the end behaviour vanishes
        and the whole reading with it."""
        PART_GLYPHS = dict(LG.Kit.PART_GLYPHS,
                           **{"stepper.step":
                              dict(LG.Kit.PART_GLYPHS["stepper.main"])})

    fs = _FlatStep("nord")
    check("control: a step drawn as its ground fails the two-channel law, and "
          "a clamped floor becomes indistinguishable from a wrapping one — "
          "which is what an end behaviour riding colour alone actually is",
          fs.part_glyph("step", LG.DEFAULT, "stepper")
          == fs.part_glyph("main", LG.DEFAULT, "stepper")
          and Text.from_markup(fs.stepper(SOPTS, 0)).plain
          == Text.from_markup(fs.stepper(SOPTS, 0, wrap=True)).plain)

    class _AlwaysStep(LG.Kit):
        """A stepper that ignores the end: both affordances at every seat,
        whatever the range says."""
        def component_cells(self, name, val, lo, hi, w=10, state=LG.DEFAULT,
                            wrap=False, caret=None, size=None):
            cells = super().component_cells(name, val, lo, hi, w, state,
                                            wrap=wrap, caret=caret, size=size)
            if name != "stepper":
                return cells
            g = self.part_glyph("step", state, name)
            h = len(g) // 2
            t = self.part_tone("step", state, name)
            return [("step", g[:h], t), ("step", g[h:], t)]

    asx = _AlwaysStep("nord")
    check("control: a stepper that draws a live step at a CLAMPED floor is "
          "advertising a key that does nothing — the ends law has teeth, and "
          "this is what it catches",
          Text.from_markup(asx.stepper(SOPTS, 0)).plain
          == Text.from_markup(asx.stepper(SOPTS, 0, wrap=True)).plain
          and Text.from_markup(asx.stepper(SOPTS, 0)).plain
          != stp(LG.kit("nord"), 0))

    class _JigglyField(LG.Kit):
        """A stepper whose field is the CURRENT option's width — the control
        breathes as it spins, which is exactly what T2 forbids."""
        def stepper(self, options, selected, w=0, state=LG.DEFAULT,
                    wrap=False):
            return LG.Kit.stepper(self, [str(options[int(selected)])], 0, w,
                                  state, wrap)

    jf = _JigglyField("nord")
    check("control: a field measured on the CURRENT option instead of the "
          "widest makes the control breathe as it spins — the anti-jiggle "
          "law is what stands between a stepper and a row that reflows every "
          "time the user presses a key",
          len({len(Text.from_markup(jf.stepper(SOPTS, i)).plain)
               for i in range(SN)}) > 1)

    # -- (8) THE GALLERY SEAT ----------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        block = stepper_block(k, GAL_W)
        check(f"{name}: the gallery's stepper block FITS the {GAL_W}-column "
              f"box", max(len(grey(r)) for r in block) <= GAL_W,
              f"widest {max(len(grey(r)) for r in block)}, {len(block)} rows")
        check(f"{name}: ... it draws a head, THREE SEATS TWICE (clamped and "
              f"wrapping) and one row per non-default state the registry "
              f"declares — derived, so a stepper that ever lost EDITED would "
              f"lose a row here without this block being touched",
              len(block) == 1 + 2 * len(STEP_OPTS) + len(ST) - 1,
              f"{len(block)} rows")
        body = "\n".join(grey(r) for r in block)
        check(f"{name}: ... and the CORNERS are both there: a clamped floor "
              f"and a wrapping floor, one above the other, which is the "
              f"comparison this block exists to let the eye make",
              grey(k.stepper(STEP_OPTS, 0, 0, LG.DEFAULT, False)) in body
              and grey(k.stepper(STEP_OPTS, 0, 0, LG.DEFAULT, True)) in body
              and grey(k.stepper(STEP_OPTS, len(STEP_OPTS) - 1)) in body)
        check(f"{name}: ... and every stepper in it is ONE WIDTH — the "
              f"anti-jiggle law seen on the surface rather than asserted at "
              f"the seat",
              len({len(grey(k.stepper(STEP_OPTS, i, 0, st, wr)))
                   for i in range(len(STEP_OPTS)) for st in ST
                   for wr in (False, True)}) == 1)

    # -- (9) THE LIVE SEAT: the render and the KEYS are one reading --------
    # THE HOLE ROUND ONE FOUND, and it is the one that mattered: a live seat
    # drawn with `wrap=True` while `action_pick` CLAMPS survived every law
    # above, because every law above asks the LANGUAGE what it draws and none
    # of them asked the SCREEN. A stepper whose steps disagree with its keys
    # is the exact defect one shared seat exists to prevent, so it is asserted
    # against the app's own action rather than against a constant.
    import app as _AP
    _CFG = _AP.ConfigScreen
    _kit_at_entry = _AP.KIT

    class _Sig:
        """The two fields the group cell reads. A stub, so the law is about
        the SEAT and not about the engine's state."""

        def __init__(self, group, enabled=True):
            self.group, self.enabled = group, enabled

    src_pick = code_of(_CFG.action_pick)
    check("live seat: `action_pick` CLAMPS — it holds the index inside the "
          "set instead of taking it round, which is the reading the render "
          "must agree with. Read off the action's own source, so the law "
          "cannot drift from the behaviour it is about",
          "max(0, min(" in src_pick and "%" not in src_pick)
    for name in TH.ORDER:
        _AP.KIT = k = LG.kit(name)
        n = len(WORKER_GROUPS)
        first = _CFG._group_stepper(None, _Sig(WORKER_GROUPS[0]), True)
        last = _CFG._group_stepper(None, _Sig(WORKER_GROUPS[-1]), True)
        dead = _CFG._group_stepper(None, _Sig(WORKER_GROUPS[0], False), False)
        check(f"{name}: THE LIVE ROW DRAWS THE SAME READING ITS KEYS OBEY — "
              f"clamped, byte for byte what this language's stepper draws "
              f"with `wrap=False`. A screen that wrapped while the arrows "
              f"clamped would be advertising a key that does nothing",
              first == k.stepper(WORKER_GROUPS, 0, 0, LG.EDITED, False)
              and last == k.stepper(WORKER_GROUPS, n - 1, 0, LG.EDITED,
                                    False))
        check(f"{name}: ... and it is NOT the wrapping one — the two differ "
              f"at the ends, which is what makes the previous check a claim "
              f"about WRAP and not merely about the glyph table",
              first != k.stepper(WORKER_GROUPS, 0, 0, LG.EDITED, True)
              and last != k.stepper(WORKER_GROUPS, n - 1, 0, LG.EDITED, True))
        tags_first = [p for p, _, _ in k.component_cells(
            "stepper", 0, 0, n - 1, 1, LG.EDITED, wrap=False)]
        check(f"{name}: ... so at the FIRST worker group the step back is "
              f"GROUND on the live screen, which is the end the user actually "
              f"hits when they hold the left arrow down",
              tags_first == ["main", "step"])
        check(f"{name}: ... a signal that is switched off draws the row DEAD, "
              f"and that state is the ENGINE's rather than a demo toggle",
              dead == k.stepper(WORKER_GROUPS, 0, 0, LG.DISABLED, False)
              and dead != first)
    _AP.KIT = _kit_at_entry
    check("live seat: the app's KIT is restored after the probes — an "
          "instrument that left a language installed would recolour every "
          "capture behind it",
          _AP.KIT is _kit_at_entry)

    print("\n== KIT LEVEL: THE MOTION CONTRACT — two regimes, four debts, "
          "and no colour")
    # THE MOTION AXIS, and the increment that pays four tempo debts at once
    # (PENDING #27). What is asserted here is the CONTRACT, not a feeling:
    #
    #   * A MOTION IS A LIST OF RENDERS. Every frame is composed by the
    #     component seats this contract already has, so the "no pictures"
    #     ruling pass 49 made when it deleted eight hand-authored
    #     `flip_frames` is enforced rather than remembered — the source law
    #     below says no motion builder holds a drawn glyph at all.
    #   * TWO DISJOINT REGIMES, and the 400-2000 ms gap between them is
    #     ILLEGAL. Derived from the EVENT, never from the language: ten
    #     languages may not disagree about whether pressing is one-shot.
    #   * COLOUR IS NOT A CHANNEL. Read over frames that is: two consecutive
    #     frames may not differ ONLY in colour, and the list must MOVE with
    #     the colour taken away. Tone may ride along — the switch's flip has
    #     drawn its mid frames in ACTIVE since pass 49 — what it may not do
    #     is BE the motion.
    #   * EVERY FRAME IS A LEGAL RENDER, which is asked the way the rest of
    #     this contract asks it: the frame must be a string one of the
    #     shipped seats actually produces, it must not jiggle, and it must
    #     mean the same thing to BOTH markup parsers.
    #
    # THE LAST OF THOSE FOUND A LIVE DEFECT, and it is worth reading before
    # the checks: industrial's `SPIN[3]` was `\`, `Kit.spinner` emits
    # `f"[tone]{glyph}[/]"`, and a backslash in front of a `[` escapes it in
    # BOTH parsers (PENDING #31) — so industrial's spinner row was printing a
    # raw `[/]` on the gallery and the aperture every fourth frame, and had
    # been for as long as that spinner has existed. The motion engine
    # consumes `SPIN` as a language's in-transit glyph, so it would have
    # inherited the defect at a second seat. The glyph is now `╲` and the
    # law below is what keeps any future one honest.
    from textual.content import Content as _MC          # the OTHER parser

    MOB = dict(label="Refresh")
    MOG = ("api", "web", "ops")                # the sibling set
    MOS = ("lo", "mid", "high")                # DIFFERENT widths: the bench
    MOT = dict(value="name", caret=2, w=8)
    # (event, component, kwargs) — the four debts, plus the one motion this
    # contract already had, so the engine is asked to reproduce it too.
    DEBTS = (("press", "button", MOB),
             ("travel", "radio", dict(options=MOG, old=0, new=2)),
             ("spin", "stepper", dict(options=MOS, old=0, new=1)),
             ("blink", "textfield", MOT),
             ("flip", "switch", dict(on=True, w=3)))

    def mgrey(m):
        return [grey(f) for f in m.frames]

    _MTONE = re.compile(r"\[([^\[\]/][^\[\]]*)\]")

    def _tone_set(s):
        """Every colour token a frame names. The no-colour law is about what
        MOVES, so the strict form — a motion whose tone set never changes —
        is measured where it is claimed rather than everywhere."""
        return set(_MTONE.findall(s))

    def _raises(fn):
        try:
            fn()
        except Exception as e:                       # noqa: BLE001
            return type(e).__name__
        return None

    # -- THE PREDICATES, written ONCE and read by the LAWS and by the
    # CONTROLS. A predicate a control cannot fail is a sentence, not a law.
    def m_realizable(m):
        """A transition expands to at least two discrete frames and leaves at
        least one to draw. A one-frame transition is not a transition, it is
        a state change — and a spec that presumes something continuous
        happens between two renders has nothing to hand a player."""
        return len(m.frames) >= 2 and m.steps >= 1

    def m_in_regime(m):
        return (m.total_ms <= LG.TRANSITION_MAX_MS
                if m.regime == LG.TRANSITION
                else m.total_ms >= LG.AMBIENT_MIN_MS)

    def m_dead_zone(m):
        return LG.TRANSITION_MAX_MS < m.total_ms < LG.AMBIENT_MIN_MS

    def m_no_colour(m):
        """The corpus finding as a law: the frames must MOVE in greyscale,
        and no consecutive pair may differ only in their colour tokens. A
        repeated frame is legal — that is a HOLD, and a hold is how a
        discrete medium spells a dwell."""
        g = mgrey(m)
        return (len(set(g)) >= 2
                and all(a == b for a, b in zip(m.frames, m.frames[1:])
                        if grey(a) == grey(b)))

    def m_no_jiggle(m):
        """Bodmer T2 over TIME. A control that changes width as it animates
        reflows the row it stands in, which is the one defect motion can
        introduce that a still render cannot have."""
        return len({len(x) for x in mgrey(m)}) == 1

    def m_decelerates(m):
        """The corpus runs ease_out over ease_in 5:1, and in a medium with no
        interpolation that is not a curve — it is WHERE THE TIME IS SPENT. So
        the law is the falsifiable half: no drawn frame before the last may
        be the render the motion LEFT. A transition that sits still and then
        moves is ease_in wearing the other one's name."""
        return (m.regime != LG.TRANSITION
                or all(p != m.frames[0] for p in m.plays[:-1]))

    def m_parses(m):
        """Every frame means the same thing to rich and to Textual, and none
        of them puts a close tag on the glass. This is the escape sweep's law
        (items #25/#31) asked of a frame list."""
        return all(grey_is_rich(f)
                   and Text.from_markup(f).plain == _MC.from_markup(f).plain
                   and "[/]" not in _MC.from_markup(f).plain
                   for f in m.frames)

    # -- (1) THE CONTRACT: regimes and events, DERIVED --------------------
    check("contract: the two regimes are DISJOINT and their two numbers are "
          "the corpus's — a one-shot ceiling of 400 ms (median 300, p90 600; "
          "the ceiling captures 68%) and a loop floor of 2000 ms (median "
          "3000). Pinned here so an edit to either is a red line rather than "
          "a quiet re-tuning",
          LG.TRANSITION_MAX_MS == 400 and LG.AMBIENT_MIN_MS == 2000
          and LG.TRANSITION != LG.AMBIENT)
    check("contract: the REGIME IS A FACT ABOUT THE EVENT — pressing is "
          "one-shot because pressing is one-shot, and a caret loops because "
          "a caret has nothing to arrive at. One table, five events, four "
          "one-shots and the contract's first loop",
          {e: LG.motion_regime(e) for e in LG.MOTION_EVENTS}
          == {"flip": LG.TRANSITION, "press": LG.TRANSITION,
              "travel": LG.TRANSITION, "spin": LG.TRANSITION,
              "blink": LG.AMBIENT})
    check("contract: WHICH MOTIONS A COMPONENT HAS IS DERIVED FROM THE PARTS "
          "REGISTRY, the way its states are — a component with an ACTIVE "
          "state can be pressed, one with a `step` spins, one with a `caret` "
          "blinks, and the CHECKABLE one with an indicator flips. Nothing "
          "here reads a component's name",
          LG.motion_events("button") == ("press",)
          and LG.motion_events("stepper") == ("press", "spin")
          and LG.motion_events("textfield") == ("press", "blink")
          and LG.motion_events("switch") == ("press", "flip")
          and LG.motion_events("bar") == () and LG.motion_events("scrollbar") == (),
          f"stepper {LG.motion_events('stepper')}")
    check("contract: ... and TRAVEL IS NOT IN THAT DERIVATION, which is pass "
          "51's finding arriving on the motion axis. The registry describes "
          "ONE component and has nothing to say about siblings, so 'the mark "
          "moves from that well to this one' can no more be derived from "
          "`COMPONENT_PARTS['radio']` than the exactly-one invariant could — "
          "it is a fact about a SET and its seat is the group's",
          "travel" not in LG.motion_events("radio")
          and LG.MOTION_GROUP_EVENTS == ("travel",)
          and LG.motion_regime("travel") == LG.TRANSITION)
    check("contract: a component may not be asked for a motion it has no "
          "anatomy for — a readout with no grip does not flash, and a button "
          "has no option to spin. The refusal is the derivation's, so it "
          "cannot be argued with per language",
          _raises(lambda: LG.kit("nord").motion_frames("bar", "press"))
          == "ValueError"
          and _raises(lambda: LG.kit("nord").motion_frames("button", "spin"))
          == "ValueError"
          and _raises(lambda: LG.kit("nord").motion_frames("button", "press",
                                                           **MOB)) is None)
    # -- (2) THE SOURCE LAW: no pictures, no palette ----------------------
    _builders = {n: getattr(LG.Kit, n) for n in dir(LG.Kit)
                 if n.startswith("_motion_")}
    check("source: the engine has FIVE builders and they are the five "
          "events — a sixth would be a motion nothing declared",
          set(_builders) == {f"_motion_{e}" for e in LG.MOTION_EVENTS},
          f"{sorted(_builders)}")
    for _bn, _bf in sorted(_builders.items()):
        _lits = [c for c in _bf.__code__.co_consts
                 if isinstance(c, str) and c != _bf.__doc__]
        check(f"source: `{_bn}` holds NO DRAWN GLYPH — every literal in it is "
              f"ASCII plumbing. This is pass 49's deletion made permanent: "
              f"eight languages once kept a hand-drawn picture of their "
              f"switch here and every one went stale the instant the switch "
              f"entered the registry",
              all(c.isascii() for c in _lits), f"{_lits}")
        check(f"source: `{_bn}` names NO COLOUR TOKEN — it never reaches into "
              f"the palette to pick a frame, which is the source-level half "
              f"of 'colour is not a channel'",
              "self.c[" not in inspect.getsource(_bf)
              and "self.t[" not in inspect.getsource(_bf))
    for _name in TH.ORDER:
        # ASKED OF THE NAMESPACE, NOT OF THE SOURCE TEXT, and that is a
        # measured correction rather than a preference: the first form of
        # this law grepped the class source for `AMBIENT`, and darkside's
        # composition comment calls its centred column "the AMBIENT
        # register" — a word about a REGISTER, not about a regime. A law
        # that reads prose reports on prose.
        _own = set(vars(type(LG.kit(_name))))
        check(f"source: {_name} declares NO REGIME AND NO DURATION — the "
              f"only motion name in its own namespace is `MOTION_STEPS`. A "
              f"language owns its FRAMES and its `tempo` token and nothing "
              f"else about time; one that could name its own regime could "
              f"put a loop in the one-shot budget",
              not (_own & {"MOTION_EVENTS", "MOTION_GROUP_EVENTS",
                           "TRANSITION", "AMBIENT", "TRANSITION_MAX_MS",
                           "AMBIENT_MIN_MS", "AMBIENT_BEATS", "REFRESH_MS",
                           "motion_frames", "motion_regime", "tempo_s"})
              and {a for a in _own if "MOTION" in a} <= {"MOTION_STEPS"},
              f"{sorted(a for a in _own if 'MOTION' in a)}")
    _appsrc = {p.name: p.read_text(encoding="utf-8")
               for p in sorted(Path(LG.__file__).resolve().parent.glob("*.py"))}
    _engine_src = inspect.getsource(LG.Kit.motion_frames)
    check("source: `_steps` IS THE MEASUREMENT DOOR AND NOTHING ELSE'S — the "
          "ceiling's escape hatch exists so a LAW can build the frame list "
          "the ceiling refused, and an app that reached through it would be "
          "a language declaring its own frame count past the surface's "
          "limit. Stated as SCOPE rather than as a count: it lives in the "
          "one function that defines it and in no other app file at all. "
          "(The first form of this law pinned the number of occurrences, "
          "got it wrong, and would have gone red on a comment)",
          "_steps" in _engine_src
          and all("_steps" not in src for n, src in _appsrc.items()
                  if n != "language.py")
          and _appsrc["language.py"].count("_steps")
          == _engine_src.count("_steps"),
          f"engine={_engine_src.count('_steps')} "
          f"file={_appsrc['language.py'].count('_steps')} "
          f"others={[n for n, s in _appsrc.items() if n != 'language.py' and '_steps' in s]}")
    check("source: and the ENGINE IS ONE SEAT — `motion_frames` is defined "
          "exactly once, on the base kit, so there is no per-language door "
          "into the derivation",
          "motion_frames" in vars(LG.Kit)
          and not [n for n in TH.ORDER
                   if "motion_frames" in vars(type(LG.kit(n)))])

    # -- (3) EVERY LANGUAGE, EVERY MOTION: the standing laws --------------
    for name in TH.ORDER:
        k = LG.kit(name)
        for ev, comp, kw in DEBTS:
            m = k.motion_frames(comp, ev, **kw)
            check(f"{name}.{ev}: REALIZABLE — it expands to {len(m.frames)} "
                  f"discrete frames, {m.steps} of them to draw. Nothing here "
                  f"asks the terminal to interpolate, because the terminal "
                  f"cannot",
                  m_realizable(m), f"{len(m.frames)} frames")
            check(f"{name}.{ev}: the REGIME is the event's and the duration "
                  f"is derived from it and the language's `tempo` — "
                  f"{m.regime}, {m.total_ms:.0f} ms over {m.steps} steps",
                  m.regime == LG.MOTION_EVENTS[ev] and m_in_regime(m),
                  f"{m.total_ms:.0f} ms")
            check(f"{name}.{ev}: it is NOT IN THE DEAD ZONE — a one-shot "
                  f"slower than 400 ms makes the user wait on the designer's "
                  f"taste and a loop faster than 2000 ms twitches, and a "
                  f"spec between the two has not decided which it is",
                  not m_dead_zone(m), f"{m.total_ms:.0f} ms")
            check(f"{name}.{ev}: NO COLOUR — the frames move with the colour "
                  f"taken away, and no consecutive pair differs only in "
                  f"tone. 241 published animations in the reference corpus, "
                  f"zero of them animate a colour",
                  m_no_colour(m), f"{len(set(mgrey(m)))} distinct greys")
            check(f"{name}.{ev}: NO JIGGLE — every frame is the same number "
                  f"of cells, so a motion cannot reflow the row it stands in",
                  m_no_jiggle(m), f"{sorted({len(x) for x in mgrey(m)})}")
            check(f"{name}.{ev}: it DECELERATES — the change lands on the "
                  f"first drawn frame and the budget after it is the settle. "
                  f"No dead lead-in, which is the falsifiable half of an "
                  f"ease_out bias in a medium with no curves",
                  m_decelerates(m))
            check(f"{name}.{ev}: every frame is a LEGAL RENDER — it parses "
                  f"the same way in rich and in Textual and puts no close "
                  f"tag on the glass. This is the law that caught "
                  f"industrial's backslash spinner",
                  m_parses(m))

    # -- (4) THE FOUR DEBTS, one at a time --------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        BST = LG.COMPONENT_STATES["button"]
        m = k.motion_frames("button", "press", **MOB)
        legal = {k.button("Refresh", 0, st) for st in BST}
        check(f"{name}.press: EVERY FRAME IS A BUTTON THIS LANGUAGE ALREADY "
              f"DRAWS — the frame list is a subset of the component's own "
              f"state renders, which is what 'a frame is a render' means "
              f"when it is asserted instead of asserted about",
              set(m.frames) <= legal)
        check(f"{name}.press: its ANCHOR AND ITS REST ARE THE SAME RENDER, "
              f"and that is what a press IS — nothing survives it. A flip, a "
              f"travel and a spin all land somewhere else, and this is the "
              f"line between them",
              m.frames[0] == m.frames[-1] == k.button("Refresh", 0,
                                                      LG.DEFAULT))
        # INDEXED DEFENSIVELY, and that is the pass-49 lesson rather than
        # timidity: a mutation that makes a renderer return one frame would
        # take this oracle down with an IndexError, and a dead run reports NO
        # REDS AT ALL. The check has to survive the mutant to convict it.
        check(f"{name}.press: the EXTREME is reached on the first drawn "
              f"frame — the acknowledgement is never animated (MOTION.md: "
              f"animate the consequence) — and it is the language's own "
              f"ACTIVE walls, not a flash invented here",
              bool(m.plays)
              and m.plays[0] == k.button("Refresh", 0, LG.ACTIVE)
              and m.plays[-1] == k.button("Refresh", 0, LG.DEFAULT))
        check(f"{name}.press: and the label comes back BYTE FOR BYTE out of "
              f"every frame — the button's content ruling does not lapse "
              f"because the control is moving",
              all("Refresh" in grey(f) for f in m.frames))

        m = k.motion_frames("radio", "travel", options=MOG, old=0, new=2)
        wells = [grey(k._component_body("radio", None, 0, 1, 1, st))
                 for st in (LG.DEFAULT, LG.FOCUSED)]
        marked = grey(k._component_body("radio", None, 0, 1, 1,
                                        LG.with_checked(LG.DEFAULT, True)))
        check(f"{name}.travel: THE FRAME COUNT IS THE DISTANCE'S, not the "
              f"language's — the mark passes every well between the two it "
              f"joins because those wells are THERE. What the language "
              f"chooses is whether it is ever seen OFF one, and since #36 "
              f"what it GETS is that choice under the refresh ceiling: the "
              f"count is derived from `elaboration`, never from the token",
              len(m.frames) == 3 + 2 * (1 if m.elaboration else 0),
              f"{len(m.frames)} frames, elaboration={m.elaboration} of "
              f"steps={k.MOTION_STEPS}")
        check(f"{name}.travel: it ARRIVES — the last frame is the group at "
              f"its new index, byte for byte the render the screen draws "
              f"when the motion is over",
              m.frames[-1] == k.radio_group(list(MOG), 2, LG.DEFAULT, focus=2)
              and m.frames[0] == k.radio_group(list(MOG), 0, LG.DEFAULT,
                                               focus=0))
        check(f"{name}.travel: it PASSES THE MIDDLE WELL — a mark that "
              f"teleported across a sibling would be a cut with extra "
              f"frames, not a travel",
              any(f == k.radio_group(list(MOG), 1, LG.DEFAULT, focus=1)
                  for f in m.frames[1:-1]))
        transit = [f for f in m.frames if marked not in grey(f)]
        check(f"{name}.travel: the IN-TRANSIT frame marks NOTHING, and it is "
              f"the language's choice whether there is one — swiss hops well "
              f"to well. It does not come out of `group_states`, because "
              f"that seat exists to make 'exactly one is marked' unreachable "
              f"and a frame between two states is a FRAME, not a state. "
              f"industrial and solari arrive here through the REFRESH "
              f"CEILING rather than through a declaration — they ask for the "
              f"in-transit sample and the surface cannot draw it (#36)",
              (len(transit) == 2 if m.elaboration else not transit)
              and all(grey(f).count(wells[0]) == len(MOG) for f in transit)
              and all(grey(f).count(marked) == 1
                      for f in m.frames if f not in transit),
              f"{len(transit)} transit frame(s), {len(m.frames)} total")

        m = k.motion_frames("stepper", "spin", options=MOS, old=0, new=1)
        field = max(len(o) for o in MOS)
        check(f"{name}.spin: it STARTS AT THE OLD WORD AND RESTS AT THE NEW, "
              f"and both ends are the shipped stepper render — the word the "
              f"user chose comes back byte for byte",
              m.frames[0] == k.stepper(MOS, 0) and m.frames[-1] == k.stepper(MOS, 1)
              and "mid" in grey(m.frames[-1]))
        mids = m.frames[1:-1]
        check(f"{name}.spin: THE IN-TRANSIT WORD IS THE LANGUAGE'S OWN "
              f"`SPIN` — the frame-motion token it already declares for its "
              f"spinner, one phase further along per cell. Nothing is "
              f"hand-authored: on a split-flap board that token is a cell "
              f"mid-turn, so solari's in-transit frames ARE the riffle",
              len(mids) == m.elaboration
              and all(any(g in grey(f) for g in k.SPIN) for f in mids),
              f"{len(mids)} mid(s), elaboration={m.elaboration} of "
              f"steps={k.MOTION_STEPS}")
        check(f"{name}.spin: ... and the FIELD DOES NOT BREATHE while it "
              f"spins — the in-transit word is exactly as wide as the widest "
              f"option, which is the width the control already reserved "
              f"(Bodmer T2, over time)",
              all(len(grey(f)) == len(grey(k.stepper(MOS, 1))) for f in m.frames)
              and len(grey(k.stepper(MOS, 1))) >= field)

        m = k.motion_frames("textfield", "blink", **MOT)
        on = grey(m.frames[0]) if m.frames else ""
        off = grey(m.frames[1]) if len(m.frames) > 1 else ""
        rune = k.field_form(LG.EDITED, "textfield")[1]
        check(f"{name}.blink: TWO FRAMES, and the diff is EXACTLY ONE CELL — "
              f"the caret's column wears the language's mark, then the RUNE "
              f"its paper is made of. The contract's first AMBIENT, and its "
              f"channel is a glyph",
              len(m.frames) == 2 and len(on) == len(off)
              and sum(a != b for a, b in zip(on, off)) == 1,
              f"{sum(a != b for a, b in zip(on, off))} cell(s)")
        check(f"{name}.blink: ... and the cell that changes goes to the "
              f"field's own RUNE, so the off frame is the field with nothing "
              f"in that column but paper",
              [b for a, b in zip(on, off) if a != b] == [rune],
              f"{[b for a, b in zip(on, off) if a != b]!r} vs {rune!r}")
        check(f"{name}.blink: the TONE DOES NOT MOVE — the caret's column is "
              f"drawn from the caret's own tone in BOTH frames. This motion "
              f"satisfies the strict reading of the colour rule and not "
              f"merely the law's, which is the point: the first loop this "
              f"contract ships had better be the proof",
              len(m.frames) == 2
              and _tone_set(m.frames[0]) == _tone_set(m.frames[1])
              and m.frames[0].count("[") == m.frames[1].count("["),
              f"{len(_tone_set(m.frames[0])) if m.frames else 0} tone "
              f"token(s), unmoved")
        check(f"{name}.blink: its PERIOD is {m.total_ms:.0f} ms — sixteen "
              f"beats of the language's own tempo, taken to the 2000 ms "
              f"floor. A loop in the reading path faster than that is a "
              f"distraction with a 100% duty cycle",
              m.total_ms >= LG.AMBIENT_MIN_MS
              and abs(m.total_ms - max(LG.AMBIENT_MIN_MS,
                                       int(k.t.get("tempo", 140))
                                       * LG.AMBIENT_BEATS)) < 1e-6,
              f"{m.total_ms:.0f} ms")
        check(f"{name}.blink: an AMBIENT DRAWS EVERY FRAME, including its "
              f"first — a loop has no 'already on the glass', so its period "
              f"divides by the frame COUNT and not by the gaps between them. "
              f"That difference is the two regimes' arithmetic, and it is "
              f"derived from the regime rather than passed in",
              m.plays == m.frames and m.steps == len(m.frames)
              and abs(m.step_ms * len(m.frames) - m.total_ms) < 1e-6)

        m = k.motion_frames("switch", "flip", on=True, w=3)
        check(f"{name}.flip: THE ENGINE REPRODUCES THE MOTION THIS CONTRACT "
              f"ALREADY HAD, byte for byte — `flip_frames` is now a caller "
              f"of the engine that drops frame 0, because ITS caller is "
              f"already showing it. A refactor that moved a single glyph "
              f"would be visible here",
              bool(m.plays) and list(m.plays) == k.flip_frames(True, 3)
              and m.frames[0] == k.switch(False, 3)
              and m.plays[-1] == k.switch(True, 3))
        check(f"{name}.flip: ... and the step the engine derives is the one "
              f"the config screen has been dividing by hand since pass 49 — "
              f"one whole tempo across the gaps between the frames",
              bool(k.flip_frames(True, 3))
              and abs(m.step_ms
                      - k.tempo_s * 1000 / len(k.flip_frames(True, 3)))
              < 1e-9, f"{m.step_ms:.1f} ms")

    # -- (5) PER-LANGUAGE CHARACTER: motion is a language commitment ------
    for ev, comp, kw in DEBTS:
        sigs = {n: tuple(mgrey(LG.kit(n).motion_frames(comp, ev, **kw)))
                for n in TH.ORDER}
        check(f"character: all TEN languages' `{ev}` frame lists differ with "
              f"the colour stripped — a motion axis on which two languages "
              f"animate identically is the recolour this whole track exists "
              f"to refuse, said about time instead of about shape",
              len(set(sigs.values())) == len(TH.ORDER),
              f"{len(set(sigs.values()))} of {len(TH.ORDER)}")
    _sol = LG.kit("solari").motion_frames("stepper", "spin", options=MOS,
                                          old=0, new=1)
    _nor = LG.kit("nord").motion_frames("stepper", "spin", options=MOS,
                                        old=0, new=1)
    _swi = LG.kit("swiss").motion_frames("stepper", "spin", options=MOS,
                                         old=0, new=1)
    check("character: SOLARI'S RIFFLE IS NOT THE BASELINE SUBSTITUTION, and "
          "it costs the language nothing to declare — the flap board's "
          "in-transit frame is its own falling-cell token where the "
          "terminal's own idiom shows its quadrant marks and swiss, which "
          "renounces motion, shows a CUT. IT IS ONE FLAP NOW AND NOT THREE "
          "(#36), and the frame COUNT has stopped separating solari from "
          "nord — the GLYPH still does, which was always the stronger half "
          "of this claim and is now the only half being made",
          len(_sol.frames) == 3 and len(_nor.frames) == 3
          and len(_swi.frames) == 2
          and mgrey(_sol)[1:-1] != mgrey(_nor)[1:-1]
          and not mgrey(_swi)[1:-1],
          f"solari {len(_sol.frames)} · nord {len(_nor.frames)} · "
          f"swiss {len(_swi.frames)}")
    check("character: ... AND THE TRIM IS NOT A LOSS OF CHARACTER, which is "
          "the judgement this pass owes and measures rather than asserts. "
          "Three mid frames at a 40 ms tempo derived a 10 ms step: the "
          "compositor drew ONE of the three and chose which by coalescing, "
          "so the riffle a user saw was already a single frame picked at "
          "random. It is one DETERMINISTIC frame now — and what makes solari "
          "SNAP is its tempo, which no ceiling touches and which is still "
          "the shortest of the ten",
          _sol.step_ms >= LG.REFRESH_MS
          and 40 / (5 - 1) < LG.REFRESH_MS            # the PRE step, 10 ms
          and int(LG.kit("solari").t["tempo"]) == 40
          and min(int(LG.kit(n).t.get("tempo", 140)) for n in TH.ORDER) == 40,
          f"PRE 10.0 ms/frame (coalesced) -> POST {_sol.step_ms:.1f} ms")
    check("character: RENOUNCING ELABORATION IS NOT RENOUNCING THE EVENT. "
          "swiss declares `MOTION_STEPS = 0` and still gets two frames from "
          "every transition, because a one-frame transition is not a "
          "transition — that floor is the ENGINE's, and a language cannot "
          "reach it",
          LG.kit("swiss").MOTION_STEPS == 0
          and all(len(LG.kit("swiss").motion_frames(c, e, **w).frames) >= 2
                  for e, c, w in DEBTS))
    # THE TABLE IS A PIN AND IT HAS TO BE TYPED, which is why it rotted (F-14).
    # It went red the day PRISM arrived as the eleventh language and stayed red
    # for six increments, carried forward as "pre-existing, unchanged" because
    # the check printed no DETAIL to say WHICH entry disagreed — a `==` between
    # two eleven-key dicts whose failure message was the sentence above.
    #
    # THE CHECK WAS WRONG, NOT THE KIT. Prism's own `MOTION_STEPS = 3` is
    # argued at its definition (`language.py`): four was tried and repeats a
    # frame because the switch's knob has three seats, two repeats as well, and
    # "sharing the value 3 with four other languages costs nothing -- what the
    # laws compare is the FRAME LIST". So the language's commitment stands and
    # the table was simply never extended.
    #
    # AND THE NUMBER IS NOT DERIVABLE, so it is not derived. Every other rotted
    # literal in this file became `len(...)` off its own derivation; this one
    # cannot, because the whole point is that a re-tune of any language's
    # motion budget is a RED LINE a human has to walk up to. What is added is
    # the detail string, so the next language costs one reading instead of six
    # packets.
    MOTION_PIN = {"naught": 3, "corgi": 1, "instrument": 3, "swiss": 0,
                  "industrial": 1, "nord": 1, "darkside": 3, "prism": 3,
                  "ledger": 1, "solari": 3, "blueprint": 2}
    _mot = {n: LG.kit(n).MOTION_STEPS for n in TH.ORDER}
    _off = [f"{n}: pinned {MOTION_PIN.get(n, '<unpinned>')}, declares {v}"
            for n, v in _mot.items() if MOTION_PIN.get(n) != v]
    _gone = sorted(set(MOTION_PIN) - set(_mot))
    check("character: the token is `MOTION_STEPS` and it governs FIVE "
          "events, which is why it is no longer called `FLIP_STEPS` — a "
          "language that elaborated its switch and cut its button would be "
          "two languages",
          not hasattr(LG.Kit, "FLIP_STEPS") and _mot == MOTION_PIN,
          f"off the pin: {_off} · pinned but gone: {_gone}")

    # -- (5b) THE REFRESH FLOOR (#36) -------------------------------------
    # A transition's one tempo is split across the gaps between its frames,
    # so a language that elaborates hard at a short tempo derives a step
    # under the compositor's own period and schedules frames the surface
    # COALESCES. The fifty-ninth pass measured five such steps and cured
    # none; this is the cure and its measurement.
    #
    # THE CEILING IS ON ELABORATION, THE FLOOR IS ON THE STEP, and they are
    # two laws because they are two claims. A language may not elaborate
    # faster than the surface draws (the ceiling, which takes frames back);
    # no step may be under the refresh period (the floor, which is absolute
    # and which STRUCTURE — travel's wells — can violate with nothing left
    # to renounce). The second leg is the one a closed-form cure would have
    # missed, and it is measured firing below.
    check("floor: the refresh period is the MEDIUM'S number and not a corpus "
          "statistic — the other two constants here are the published "
          "durations of 241 animations, this one is what the compositor can "
          "draw (60 fps). Pinned so a re-tune is a red line",
          abs(LG.REFRESH_MS - 1000 / 60) < 1e-9
          and LG.REFRESH_MS < LG.TRANSITION_MAX_MS < LG.AMBIENT_MIN_MS,
          f"{LG.REFRESH_MS:.3f} ms")
    check("floor: EVERY LANGUAGE'S TEMPO CAN AFFORD A TRANSITION AT ALL, "
          "which is the law that keeps realizability and the floor from "
          "contradicting each other. A transition is at least two frames, so "
          "at least one gap, so a tempo under the refresh period could not "
          "be drawn at any elaboration — the honest outcome there is not a "
          "renunciation (a cut is not a transition) but a TEMPO the language "
          "may not have. The shortest of the ten is solari's 40 ms, which "
          "affords two gaps",
          all(int(LG.kit(n).t.get("tempo", 140)) >= LG.REFRESH_MS
              for n in TH.ORDER),
          f"min tempo {min(int(LG.kit(n).t.get('tempo', 140)) for n in TH.ORDER)}"
          f" ms, floor {LG.REFRESH_MS:.1f} ms")
    _trimmed = []
    for name in TH.ORDER:
        k = LG.kit(name)
        _ms_ = int(k.t.get("tempo", 140))
        for ev, comp, kw in DEBTS:
            m = k.motion_frames(comp, ev, **kw)
            if m.regime == LG.AMBIENT:
                check(f"{name}.{ev}: an AMBIENT HAS NO ELABORATION TO CEILING "
                      f"and that is the regime split working, not an "
                      f"exemption — its period is floored at 2000 ms and "
                      f"divided by the frame COUNT, so it clears the refresh "
                      f"floor by two orders of magnitude and its builder "
                      f"takes no step count at all",
                      m.elaboration == 0
                      and m.step_ms > 30 * LG.REFRESH_MS,
                      f"{m.step_ms:.0f} ms = {m.step_ms / LG.REFRESH_MS:.0f}x "
                      f"the floor")
                continue
            # THE RAW QUOTIENT IS WHAT THIS LAW MEASURES, and the reason is
            # that `step_ms` is a `max(..., REFRESH_MS)`: a law reading it
            # would be reading the seat's own clamp and could not go red
            # while the clamp is there. What is FALSIFIABLE is that the
            # CEILING left a frame count the tempo can pay for — the frames
            # actually built, divided into the language's own tempo, with
            # nothing protecting the answer.
            _raw0 = _ms_ / max(1, len(m.frames) - 1)
            check(f"{name}.{ev}: NO STEP UNDER THE REFRESH PERIOD — a frame "
                  f"scheduled under it is not a fast frame, it is a frame "
                  f"the surface coalesces and the user never sees. The "
                  f"language pays for it, declares it, and gets nothing. "
                  f"Measured on the RAW quotient, because `step_ms` is a "
                  f"clamp and a law that reads a clamp cannot fail",
                  _raw0 >= LG.REFRESH_MS - 1e-9,
                  f"{_raw0:.2f} ms raw vs {LG.REFRESH_MS:.2f} ms floor")
            check(f"{name}.{ev}: the ceiling only ever TAKES — the "
                  f"elaboration it grants is never more than the language "
                  f"declared, so a language cannot be given frames it did "
                  f"not ask for by a rule about the surface",
                  0 <= m.elaboration <= k.MOTION_STEPS,
                  f"{m.elaboration} of {k.MOTION_STEPS}")
            if m.elaboration == k.MOTION_STEPS:
                continue
            _trimmed.append((name, ev, k.MOTION_STEPS, m.elaboration))
            _plus = k.motion_frames(comp, ev, _steps=m.elaboration + 1, **kw)
            _raw = _ms_ / max(1, len(_plus.frames) - 1)
            check(f"{name}.{ev}: ... and where it takes, it takes the LEAST "
                  f"it can. One more step is BUILT through the measurement "
                  f"door and its raw step measured: {_raw:.1f} ms, under the "
                  f"floor. A ceiling nothing can build the other side of is "
                  f"a claim about arithmetic rather than a measurement",
                  _raw < LG.REFRESH_MS
                  and len(_plus.frames) > len(m.frames),
                  f"{m.elaboration}+1 -> {len(_plus.frames)} frames at "
                  f"{_raw:.2f} ms")
    check("floor: THE FIVE STEPS THE FIFTY-NINTH PASS MEASURED ARE THE FIVE "
          "THE CEILING TRIMMED — pinned as a table so a sixth trim, or a "
          "trim that stops happening, is a red line rather than a quiet "
          "re-tuning. solari elaborates hardest at the shortest tempo and "
          "pays for it four times; industrial pays once, on the event whose "
          "frame count is the DISTANCE's",
          sorted(_trimmed) == sorted([
              ("industrial", "travel", 1, 0),
              ("solari", "press", 3, 0), ("solari", "travel", 3, 0),
              ("solari", "spin", 3, 1), ("solari", "flip", 3, 1)]),
          f"{sorted(_trimmed)}")
    _far = LG.kit("solari").motion_frames("radio", "travel",
                                          options=("a", "b", "c", "d"),
                                          old=0, new=3)
    check("floor: AND THE CEILING IS NOT THE FLOOR'S ONLY LEG, which is the "
          "part a closed-form `tempo // refresh` cure would have missed. "
          "travel's frame count is the DISTANCE's, so at ZERO elaboration a "
          "long enough travel is still under the floor with nothing left to "
          "renounce — the wells are THERE. The step is floored and the pass "
          "RUNS LONG rather than the mark skipping a sibling: solari across "
          "three wells takes 50 ms against its 40 ms tempo",
          _far.elaboration == 0 and len(_far.frames) == 4
          and _far.step_ms >= LG.REFRESH_MS - 1e-9
          and _far.total_ms > int(LG.kit("solari").t["tempo"])
          and _far.total_ms <= LG.TRANSITION_MAX_MS,
          f"{len(_far.frames)} frames, {_far.step_ms:.2f} ms/step, "
          f"{_far.total_ms:.1f} ms total vs 40 ms tempo")
    check("floor: ... and that leg is the EXCEPTION rather than the rule — "
          "no shipped fixture reaches it. Every one of the ten languages' "
          "four transitions lands on exactly one tempo once the ceiling has "
          "run, so 'a transition's whole pass is one tempo' is still true "
          "everywhere it is drawn, and the stretch is reserved for the "
          "structure that cannot be trimmed",
          all(abs(LG.kit(n).motion_frames(c, e, **w).total_ms
                  - int(LG.kit(n).t.get("tempo", 140))) < 1e-6
              for n in TH.ORDER for e, c, w in DEBTS
              if LG.motion_regime(e) == LG.TRANSITION))

    # -- (6) THE CONTROLS: every predicate above, failed on purpose -------
    _kn = LG.kit("nord")
    _tempo0 = _kn.t.get("tempo")
    try:
        _kn.t["tempo"] = 800
        _md = _kn.motion_frames("button", "press", **MOB)
        check("control: a language whose tempo puts a one-shot at 800 ms "
              "lands in the DEAD ZONE, and both halves of the regime law say "
              "so — this is the number the two regimes exist to make "
              "unsayable",
              m_dead_zone(_md) and not m_in_regime(_md),
              f"{_md.total_ms:.0f} ms")
    finally:
        if _tempo0 is None:
            _kn.t.pop("tempo", None)
        else:
            _kn.t["tempo"] = _tempo0
    check("control: ... and the token is RESTORED — a probe that left a "
          "theme mutated poisons every render behind it",
          abs(_kn.motion_frames("button", "press", **MOB).total_ms
              - _tempo0) < 1e-6)

    _amin0 = LG.AMBIENT_MIN_MS
    try:
        LG.AMBIENT_MIN_MS = 500
        _mf = LG.kit("solari").motion_frames("textfield", "blink", **MOT)
        check("control: drop the ambient floor and solari's caret blinks "
              "every 640 ms — three times a second in the reading path, "
              "which is the distraction the floor exists to forbid. The law "
              "reads the constant, so the constant is pinned above",
              _mf.total_ms < 2000 and m_in_regime(_mf),
              f"{_mf.total_ms:.0f} ms at a 500 ms floor")
    finally:
        LG.AMBIENT_MIN_MS = _amin0

    class _MOneFrame(LG.Kit):
        """A press cut down to one frame — the state change wearing a
        motion's name."""
        def _motion_press(self, name, label="", w=0, state=LG.DEFAULT):
            return LG.Kit._motion_press(self, name, label, w, state)[:1]

    check("control: a transition that expands to ONE frame fails "
          "realizability — there is nothing to play, and a spec that "
          "presumed something continuous happened between two renders would "
          "hand a player exactly this",
          not m_realizable(_MOneFrame("nord").motion_frames("button", "press",
                                                            **MOB)))

    class _MColourOnly(LG.Kit):
        """A press whose two frames differ ONLY in their tone — the animation
        the reference corpus never once publishes."""
        def _motion_press(self, name, label="", w=0, state=LG.DEFAULT):
            rest = self.button(label, w, state)
            return [rest, rest.replace(self.c["ink"], self.c["accent"]), rest]

    _mc = _MColourOnly("nord").motion_frames("button", "press", **MOB)
    check("control: a press whose frames differ ONLY in colour fails the "
          "no-colour law while passing every other one — it is realizable, "
          "in regime, unjiggling and legal, and it is still not a motion",
          not m_no_colour(_mc) and m_realizable(_mc) and m_no_jiggle(_mc)
          and m_in_regime(_mc), f"{len(set(mgrey(_mc)))} distinct greys")

    class _MSkipTransit(LG.Kit):
        """A travel that cuts straight from well to well while the language
        declares steps — the mark teleports."""
        def _motion_travel(self, name, options=(), old=0, new=0,
                           state=LG.DEFAULT):
            o = list(options)
            return [self.radio_group(o, int(old), state, focus=int(old)),
                    self.radio_group(o, int(new), state, focus=int(new))]

    _ms = _MSkipTransit("nord").motion_frames("radio", "travel", options=MOG,
                                              old=0, new=2)
    check("control: a travel that SKIPS THE BETWEEN-FRAME while its language "
          "declares steps is caught by the frame-count law and by the "
          "passes-the-middle-well law at once — two frames where the "
          "distance demands five, and a middle sibling never crossed",
          len(_ms.frames) != 3 + 2 * (1 if _ms.elaboration else 0)
          and not any(f == LG.kit("nord").radio_group(list(MOG), 1,
                                                      LG.DEFAULT, focus=1)
                      for f in _ms.frames[1:-1]))

    class _MNoCeiling(LG.Kit):
        """The tree as it shipped before this pass: the elaboration is the
        language's token and the derived step is whatever the division
        gives. This is not an invented defect — it is `motion_frames` with
        item #36 still open, and it is the arm that says the floor law above
        can go red."""
        MOTION_STEPS = 3

        def motion_frames(self, component, event, **kw):
            m = LG.Kit.motion_frames(self, component, event,
                                     _steps=self.MOTION_STEPS, **kw)
            ms = int(self.t.get("tempo", 140))
            return LG.Motion(m.frames, m.regime,
                             ms / max(1, len(m.frames) - 1), m.elaboration)

    _mn = _MNoCeiling("solari")
    _mnc = [(e, _mn.motion_frames(c, e, **w))
            for e, c, w in DEBTS if LG.motion_regime(e) == LG.TRANSITION]
    check("control: REMOVE THE CEILING AND THE FLOOR GOES RED FOUR TIMES — "
          "solari's own tempo and its own token, with `motion_frames` doing "
          "what it did before this pass. Every one of its four transitions "
          "derives a step under the refresh period, which is the shipped, "
          "green, per-language behaviour item #36 named and this pass took "
          "away. A floor law no arm can redden is a sentence",
          all(m.step_ms < LG.REFRESH_MS for _e, m in _mnc)
          and len(_mnc) == 4,
          f"{[(e, round(m.step_ms, 1)) for e, m in _mnc]}")
    check("control: ... and the same arm is REALIZABLE, IN REGIME, "
          "colourless and unjiggling — the defect is invisible to every "
          "motion law that predates this pass, which is the argument for "
          "spending an increment on a cure that trims five shipped frame "
          "counts",
          all(m_realizable(m) and m_in_regime(m) and not m_dead_zone(m)
              and m_no_colour(m) and m_no_jiggle(m) and m_decelerates(m)
              for _e, m in _mnc))
    check("control: and a language whose TEMPO cannot afford one gap fails "
          "the tempo law — 12 ms is under the refresh period, so its "
          "transition cannot be drawn at ANY elaboration and the floor and "
          "realizability would contradict each other. The honest outcome is "
          "a tempo the language may not have, and this is the arm that says "
          "so rather than the prose above",
          not (12 >= LG.REFRESH_MS)
          and LG.Kit.motion_frames(_mn, "switch", "flip", on=True,
                                   w=3).step_ms >= LG.REFRESH_MS)

    class _MLeadIn(LG.Kit):
        """A press that sits still at its starting render before it moves."""
        def _motion_press(self, name, label="", w=0, state=LG.DEFAULT):
            f = LG.Kit._motion_press(self, name, label, w, state)
            return [f[0]] + f

    check("control: a transition that DWELLS at the render it left before it "
          "changes is ease_IN wearing ease_out's name, and the deceleration "
          "law is what tells them apart. The corpus runs out over in 5:1",
          not m_decelerates(_MLeadIn("nord").motion_frames("button", "press",
                                                           **MOB)))

    class _MBackslash(LG.Kit):
        """The defect this pass found, re-armed: a spin whose in-transit
        glyph is a backslash, standing where a close tag follows it."""
        SPIN = ("|", "/", "-", "\\")

    _mb = _MBackslash("nord").motion_frames("stepper", "spin", options=MOS,
                                            old=0, new=1)
    check("control: a language whose SPIN carries a `\\` puts a raw `[/]` on "
          "the glass, and the parser law catches it — this is exactly what "
          "industrial's spinner had been doing every fourth frame, at a seat "
          "no `[/]` check ever ran over",
          not m_parses(_mb)
          and any("[/]" in _MC.from_markup(f).plain for f in _mb.frames))
    check("control: ... and the shipped languages are clean at BOTH seats — "
          "no motion frame and no spinner frame puts a close tag on the "
          "glass, in any of the ten",
          not [(n, t) for n in TH.ORDER
               for t in range(len(LG.kit(n).SPIN))
               if "[/]" in _MC.from_markup(LG.kit(n).spinner(t)).plain])

    print("\n== KIT LEVEL: card anatomy — the VARIETY law (2-row cards)")
    cards = {}
    for name in TH.ORDER:
        k = LG.kit(name)
        ra = k.card_rows("Fix the wrapped frame", "3d", k["warn"], 28, 2,
                         True, META_A)
        rb = k.card_rows("Fix the wrapped frame", "3d", k["warn"], 28, 2,
                         True, META_B)
        cards[name] = "\n".join(grey(r) for r in ra)
        if name == "swiss":
            check("swiss: the second row is renounced (1 row, a decision)",
                  len(ra) == 1)
        elif name == "solari":
            # solari spends row 2 on the SEAM, which is a CONSTANT by design —
            # it is the language's entire divider vocabulary. So the generic
            # "row 2 carries the metadata" assertion is asked of row 1
            # instead, at a width that BOUGHT the metadata columns, and row 2
            # is held to the stronger claim: it is the divider and nothing
            # else. Neither half of this is a weakening; both can fail.
            check("solari: card is a 2-row mini-widget", len(ra) == 2)
            seam = grey(ra[1])
            check("solari: row 2 is the SEAM and nothing else (a constant)",
                  seam and set(seam) == {LG.Solari.SEAM}
                  and grey(ra[1]) == grey(rb[1]), repr(seam[:6]))
            wa = k.card_rows("Fix the wrapped frame", "3d", k["warn"], 60, 2,
                             True, META_A)
            wb = k.card_rows("Fix the wrapped frame", "3d", k["warn"], 60, 2,
                             True, META_B)
            check("solari: the schedule row carries the metadata (@60)",
                  grey(wa[0]) != grey(wb[0]))
            # and the narrow card answers with LESS on purpose: at 28 the
            # declared drop order has shed proj/pri/status, so the row is the
            # departure figure and the item. That is the law, not an omission,
            # and the geometry seat is asked rather than the pixels.
            check("solari: at 28 the drop law has shed the metadata columns",
                  [c for _, c, _ in k.fields(28)] == ["due", "item"]
                  and grey(ra[0]) == grey(rb[0]))
        else:
            check(f"{name}: card is a 2-row mini-widget", len(ra) == 2)
            check(f"{name}: row 2 responds to the metadata in greyscale",
                  grey(ra[1]) != grey(rb[1]))
    check("no two languages share a card anatomy",
          len(set(cards.values())) == len(TH.ORDER))
    check("row counts diverge across languages (variety, not one skeleton)",
          len({c.count("\n") for c in cards.values()}) >= 2)

    print("\n== KIT LEVEL: data-viz laws (DATAVIZ.md — the Kimi harvest)")
    for name in TH.ORDER:
        k = LG.kit(name)
        check(f"{name}: spark honours a SHARED hi (siblings comparable)",
              grey(k.spark([3, 3, 3, 3], 4, hi=3))
              != grey(k.spark([3, 3, 3, 3], 4, hi=30)))
        check(f"{name}: plot honours a SHARED hi",
              [grey(r) for r in k.plot([3, 3], 8, 4, hi=3)]
              != [grey(r) for r in k.plot([3, 3], 8, 4, hi=30)])
        check(f"{name}: microbar floor (tiny nonzero != zero, greyscale)",
              grey(k.spark([1, 0, 1, 0], 4, hi=99))
              != grey(k.spark([0, 0, 0, 0], 4, hi=99)))
        check(f"{name}: spark REFLOWS a wide series (the tail survives)",
              grey(k.spark([0] * 49 + [9], 10))
              != grey(k.spark([0] * 50, 10)))
        check(f"{name}: empty series is safe and empty",
              k.spark([], 8) == "" and k.plot([], 8, 4) == [])
        # UPGRADED IN PASS 61, SAME NAME, BECAUSE THE OLD FORM PINNED THE
        # DEFECT. It asserted `plot` returns 4 rows — which four rows of
        # SPACES satisfy, and four rows of spaces is exactly what DATAVIZ law
        # 4 forbids and what nine of ten languages drew. The claim the name
        # always made is that a flat-zero series HAS a surface: the spark's
        # every cell is the ramp's own unlit glyph (solari prints figures, and
        # a figure is a surface too), and the plot still stands h rows tall.
        _z = grey(k.spark([0, 0, 0, 0], 8))
        _mech = k.t.get("meter", "blocks")
        check(f"{name}: flat-zero series still renders the track",
              len(k.plot([0, 0, 0, 0], 8, 4)) == 4 and _z.strip() != ""
              and (set(_z) == {"0"} if _mech == "odometer"
                   else set(_z) == {k.cover_ramp()[0]}),
              f"{_z!r}")
        try:
            k.gauge(0, 0, 0, 8)
            zero_ok = True
        except Exception:
            zero_ok = False
        check(f"{name}: gauge survives a zero range", zero_ok)
        check(f"{name}: gauge STATES its value",
              "7" in grey(k.gauge(7, 0, 10, 10)))
        with_tick = grey(k.gauge(2, 0, 10, 10, thr=8))
        check(f"{name}: threshold tick renders (with != without)",
              with_tick != grey(k.gauge(2, 0, 10, 10)))
        check(f"{name}: threshold tick MOVES with the threshold",
              with_tick != grey(k.gauge(2, 0, 10, 10, thr=5)))

    # =====================================================================
    # KIT LEVEL: COVERAGE -> GLYPH (pass 60 — the shared DATAVIZ primitive)
    #
    # Coverage anti-aliasing translated to a cell grid: alpha is not a blend,
    # it is an INDEX into an ordered glyph ramp. What this section defends is
    # not that the primitive exists but that every coverage-shaped seat in
    # the module GOES THROUGH IT and that the mapping cannot drift — because
    # a ramp is exactly the kind of thing that gets a glyph swapped in a
    # hurry, and a swapped glyph in the middle of a ramp is a chart that
    # reads backwards with nothing on screen to say so.
    #
    # THE GREYSCALE HALF NEEDS AN INSTRUMENT AND THE INSTRUMENT NEEDS A
    # PROVENANCE. Ink density is DERIVED wherever the codepoint carries it
    # (braille is a popcount, the block eighths are an offset, the shade
    # blocks are ordered by their own Unicode names) and DECLARED only for
    # the eight glyphs Unicode gives no ordering to — box-drawing weight and
    # punctuation. The split is asserted, so the derived half cannot quietly
    # become a table somebody typed.
    #
    # THE SIXTY-FIRST PASS TURNED THE TWO CENSUSES INSIDE OUT. They were
    # written to pin defects pass 60 measured and declined to cure: nine of
    # ten ramps drew AIR at index 0 (DATAVIZ law 4) and two repeated a glyph,
    # one of them the LCD case the skill cites by name (law 1). Both are
    # cured, so the same laws are restated as the CURE — every data ramp's
    # unlit glyph carries ink, under a quarter-cell ceiling, with ONE argued
    # exemption; and the repeat census is down to the declared two-weight
    # idiom, pinned at the exact INDEX PAIR allowed to repeat. A census earns
    # its place only by going red in both directions, so these go red if the
    # air comes back AND if the exemption list grows.
    # =====================================================================
    print("\n== KIT LEVEL: coverage -> glyph (the shared DATAVIZ primitive)")
    import os as _os
    import subprocess as _sub
    import unicodedata as _ud

    _SHADE_INK = {"LIGHT SHADE": 0.25, "MEDIUM SHADE": 0.50,
                  "DARK SHADE": 0.75}
    # ORDERED BY DENSITY, and the three new rows are the sixty-first pass's
    # cure vocabulary: a rule BROKEN carries less ink than the rule (four
    # dashes and three gaps < two dashes and two gaps < the solid rule), and
    # a mark HOLLOW carries less than the same mark filled.
    _DECLARED_INK = {"·": 0.10, "┈": 0.15, ":": 0.20, "╌": 0.22, "─": 0.30,
                     "▫": 0.35, "━": 0.55, "▪": 0.60}

    def ink(g):
        """Ink density of one glyph in [0, 1]."""
        if g == " ":
            return 0.0
        cp = ord(g)
        if 0x2800 <= cp <= 0x28FF:                   # braille: count the dots
            return bin(cp - 0x2800).count("1") / 8
        if 0x2581 <= cp <= 0x2588:                   # lower N eighths block
            return (cp - 0x2580) / 8
        nm = _ud.name(g, "")
        if nm in _SHADE_INK:
            return _SHADE_INK[nm]
        return _DECLARED_INK[g]                      # KeyError = a new glyph

    def ink_derived(g):
        cp = ord(g)
        return (g == " " or 0x2800 <= cp <= 0x28FF or 0x2581 <= cp <= 0x2588
                or _ud.name(g, "") in _SHADE_INK)

    # every ramp the registry can produce, plus the one each language
    # actually draws with — a registry that agrees with itself and disagrees
    # with the kits would pass every law below and still be wrong
    COV = dict(LG.COVER_RAMPS)
    for nm_ in TH.ORDER:
        k_ = LG.kit(nm_)
        if k_.t.get("meter", "blocks") != "odometer":
            COV[f"kit:{nm_}"] = k_.cover_ramp()

    # THE CENSUSES, AFTER THE CURE (pass 61). Pass 60 listed the ramps that
    # broke the laws; these list the ONLY ramps allowed to, and both are still
    # two-directional — red if a cured ramp reverts, red if a new exemption is
    # taken in silence.
    #
    # `shades` IS `bases.SHADES`: the BITMAP ramp, whose cell is a pixel of a
    # SPRITE. A sprite's ground is ABSENCE, not a datum worth zero, and
    # inking index 0 would put texture inside every empty pixel of every
    # mascot — so law 4, which is a law about DATA, does not reach it. That
    # argument is the exemption; `bases.py` being outside pass 61's file
    # budget is not.
    AIR_EXEMPT = {"shades"}
    # WHICH INDEX PAIR may repeat, not merely THAT one does. `hairline` is
    # '┈─━━' — a broken rule, a rule, and a heavy rule held for the top two
    # levels, which is a DECLARED two-weight idiom rather than the colour-only
    # step law 1 forbids. Pinning the pair is what stops a future edit from
    # repeating a DIFFERENT pair and passing a census that only counted.
    REPEAT_AT = {"hairline": {(2, 3)}, "kit:swiss": {(2, 3)}}
    # THE TRACK CEILING. A visible unlit glyph fixes law 4, and a HEAVY one
    # replaces it with a worse defect: a zero row that reads as data. A
    # quarter of the cell is the ceiling, and every cured ramp sits on or
    # under it.
    TRACK_MAX = 0.25

    grid = [i / 400 for i in range(-40, 460)]        # dense, and out of range

    check("cover: every registry glyph has an ink density",
          all(isinstance(ink(g), float)
              for r in COV.values() for g in r))
    check("cover: the ink instrument is DERIVED except for 8 declared glyphs",
          {g for r in COV.values() for g in r if not ink_derived(g)}
          == set(_DECLARED_INK))
    check("cover: the registry and bases.SHADES are ONE definition",
          LG.COVER_RAMPS["shades"] == BS.SHADES)
    check("cover: the registry and RAMP are ONE definition",
          LG.COVER_RAMPS["eighths"] == LG.RAMP)
    check("cover: the thresholds are the declared ruling (lo=0 -> law 3)",
          LG.COVER_LO == 0.0 and LG.COVER_HI == 1.0)
    check("cover: every METER_RAMP row names a registry ramp",
          set(LG.METER_RAMP.values()) <= set(LG.COVER_RAMPS))
    check("cover: the ANTI-DITHER refusal is in the docstring",
          "NEVER DITHERED" in (LG.coverage_to_glyph.__doc__ or ""))
    # SCOPED TO THE BLOCK, NOT TO A CHARACTER WINDOW. This was written as
    # "in the last 4000 characters before `def coverage_index`", which is a
    # proxy for "in the coverage block" that any comment edit can walk out of
    # — pass 61's registry argument pushed the sentence past the window and
    # redded a law about DITHERING by writing a paragraph about ramps. Same
    # lesson as pass 60's quote-style leak: a source law a formatting change
    # can defeat is not a source law. The block is now named at both ends.
    _cov_block = inspect.getsource(LG).split("def coverage_index")[0]
    _cov_i = at(_cov_block, "# COVERAGE -> GLYPH")
    _cov_block = _cov_block[_cov_i:] if _cov_i >= 0 else ""
    check("cover: the ANTI-DITHER refusal is in the module block",
          "NEVER DITHERED" in _cov_block)
    check("cover: ... and the block the law reads is the coverage block "
          "(the probe is scoped, not a character window)",
          "COVER_RAMPS = {" in _cov_block and len(_cov_block) > 2000)

    # -- per ramp ---------------------------------------------------------
    for rn, r in sorted(COV.items()):
        idx = [LG.coverage_index(c, len(r) - 1) for c in grid]
        gl = [LG.coverage_to_glyph(c, r) for c in grid]
        dens = [ink(g) for g in r]
        check(f"cover[{rn}]: MONOTONE — c1 < c2 => index(c1) <= index(c2)",
              all(a <= b for a, b in zip(idx, idx[1:])))
        check(f"cover[{rn}]: MONOTONE in ink — the ramp never gets lighter",
              all(a <= b for a, b in zip(dens, dens[1:])))
        check(f"cover[{rn}]: GREYSCALE-SAFE — the two ends differ in ink",
              dens[0] < dens[-1])
        check(f"cover[{rn}]: THRESHOLD — at or under lo draws the unlit glyph",
              all(g == r[0] for c, g in zip(grid, gl) if c <= LG.COVER_LO))
        check(f"cover[{rn}]: THRESHOLD — at or over hi draws the terminal",
              all(g == r[-1] for c, g in zip(grid, gl) if c >= LG.COVER_HI))
        # STATED AS AN INDEX, not as a glyph set, and the first draft of this
        # law got it wrong in a way worth keeping: `hairline` is '┈─━━', so
        # its TERMINAL glyph is also its level-2 glyph and "no middle GLYPH
        # outside the band" is unaskable of it — the sets overlap. The claim
        # was always about the INDEX (only the two ends are reachable outside
        # the band); the glyph is what the ramp does with it.
        check(f"cover[{rn}]: THRESHOLD — only the two END indices outside "
              f"[lo, hi]",
              all(LG.coverage_index(c, len(r) - 1) in (0, len(r) - 1)
                  for c in grid if c <= LG.COVER_LO or c >= LG.COVER_HI))
        check(f"cover[{rn}]: DETERMINISTIC — 100 calls, one glyph per cell",
              all(len({LG.coverage_to_glyph(c, r) for _ in range(100)}) == 1
                  for c in (0.0, 1e-9, 0.13, 0.5, 0.87, 1.0, 4.0)))
        check(f"cover[{rn}]: MICROBAR FLOOR — a nonzero coverage is not blank",
              LG.coverage_to_glyph(1e-9, r) != r[0])
        # DATAVIZ LAW 4, AS THE CURE. The claim is not "index 0 is not a
        # space" — braille's U+2800 BLANK passed that for sixty passes while
        # drawing nothing — it is that the glyph carries INK.
        check(f"cover[{rn}]: law-4 — the unlit glyph carries ink (or is the "
              f"one declared exemption)",
              (ink(r[0]) > 0.0) == (rn not in AIR_EXEMPT),
              f"{r[0]!r} ink={ink(r[0]):.3f}")
        check(f"cover[{rn}]: law-4 — the track stays under a quarter cell "
              f"(a track that reads as data is worse than none)",
              rn in AIR_EXEMPT or ink(r[0]) <= TRACK_MAX,
              f"{ink(r[0]):.3f} <= {TRACK_MAX}")
        check(f"cover[{rn}]: law-4 — the unlit glyph is none of the LIT ones",
              rn in AIR_EXEMPT or r[0] not in r[1:])
        # DATAVIZ LAW 1: a level that exists only in TONE is not a level.
        check(f"cover[{rn}]: law-1 census — only the DECLARED index pair "
              f"repeats",
              {(i, i + 1) for i in range(len(r) - 1) if r[i] == r[i + 1]}
              == REPEAT_AT.get(rn, set()))

    # -- THE TWO NAMED CASES, asserted by name rather than by census --------
    # DATAVIZ law 1 cites ONE example: "an LCD spark whose lit and ghost
    # segments share a glyph is invisible in greyscale; it needed segment
    # HEIGHT". It was live in corgi from the first pass to the sixtieth. This
    # is the law that says it is not live now, and it is written against the
    # skill's sentence rather than against a set, so a future census edit
    # cannot retire it by dropping a name from a list.
    _lcd = LG.COVER_RAMPS["lcd"]
    check("cover: THE SKILL'S OWN CASE — the lcd ramp's four levels are four "
          "GLYPHS (colour stripped, no level exists only in tone)",
          len(set(_lcd)) == len(_lcd), f"{_lcd!r}")
    check("cover: ... and they climb in HEIGHT, which is the cure that "
          "sentence names",
          all(ink(a) < ink(b) for a, b in zip(_lcd, _lcd[1:])),
          " < ".join(f"{ink(g):.2f}" for g in _lcd))
    # DATAVIZ law 4's trap: a flat-zero series drawing nothing at all. Nine of
    # ten ramps did exactly that, and the ONE that did not is the reason it
    # was findable.
    check("cover: law-4 — every DATA ramp draws a track at coverage 0 "
          "(the exemption list is exactly the BITMAP row)",
          {rn for rn, r in COV.items() if ink(r[0]) == 0.0} == AIR_EXEMPT,
          f"air: {sorted(rn for rn, r in COV.items() if ink(r[0]) == 0.0)}")
    check("cover: ... and the exempt row IS bases.SHADES, not a ramp of its "
          "own (the argument is 'a sprite's ground is absence')",
          all(LG.COVER_RAMPS[rn] == BS.SHADES for rn in AIR_EXEMPT))
    # A WIDE GLYPH IN A RAMP WOULD BREAK EVERY WIDTH LAW IN THE SUITE, and
    # the cure introduced three glyphs, so the check is cheap insurance
    # rather than ceremony.
    check("cover: no ramp glyph is DOUBLE WIDTH (EAW W/F would jiggle every "
          "row it lands in)",
          all(_ud.east_asian_width(g) not in ("W", "F")
              for r in COV.values() for g in r))

    # -- the quantiser ORACLES: the primitive reproduces the arithmetic the
    # routed seats used to do inline. This is the byte-identity claim written
    # as a law — the PRE/POST render diff lives in `_p60_prove.py` §1, but a
    # diff run once proves nothing about tomorrow, and this does.
    ok4 = ok8 = okp = True
    for top in (1, 3, 7, 20, 99, 1000):
        for n in range(-3, top * 2 + 2):
            was = 0 if n <= 0 else max(1, min(3, round(3 * n / top)))
            ok4 &= LG.coverage_index(0.0 if n <= 0 else n / top, 3) == was
        for n in range(0, top + 1):
            was = 0 if n == 0 else max(1, round(8 * n / top))
            ok8 &= (LG.coverage_to_glyph(n / top, LG.COVER_RAMPS["eighths"])
                    == LG.RAMP[was])
    for part in range(1, 8):
        okp &= (LG.coverage_to_glyph(part / 8, LG.COVER_RAMPS["eighths"])
                == LG.RAMP[part])
    check("cover: ORACLE — the 4-level index reproduces spark's arithmetic",
          ok4)
    check("cover: ORACLE — the 9-level ramp reproduces _pulse's arithmetic",
          ok8)
    check("cover: ORACLE — the eighths ramp reproduces plot's partial cell",
          okp)

    # -- DETERMINISM ACROSS PROCESSES. A dither keyed off `hash()` would be
    # perfectly stable inside one run and unstable between two, which is the
    # failure a 100-call loop cannot see.
    _code = ("import sys, hashlib; sys.path.insert(0, r'%s');"
             "from taskboard import language as L;"
             "s=''.join(L.coverage_to_glyph(i/499, r)"
             " for r in sorted(L.COVER_RAMPS.values()) for i in range(500));"
             "print(hashlib.sha256(s.encode('utf-8')).hexdigest())"
             % Path(LG.__file__).resolve().parents[1])
    _mine = __import__("hashlib").sha256("".join(
        LG.coverage_to_glyph(i / 499, r)
        for r in sorted(LG.COVER_RAMPS.values())
        for i in range(500)).encode("utf-8")).hexdigest()
    _seen = []
    for _seed in ("0", "1", "271828"):
        _p = _sub.run([sys.executable, "-c", _code], capture_output=True,
                      text=True, encoding="utf-8",
                      env={**_os.environ, "PYTHONHASHSEED": _seed,
                           "PYTHONIOENCODING": "utf-8"})
        _seen.append(_p.stdout.strip())
    check("cover: DETERMINISTIC across processes (3 fresh PYTHONHASHSEEDs)",
          all(s == _mine for s in _seen), f"{_mine[:12]}…")
    check("cover: the cross-process probe actually ran (not 3 empty strings)",
          all(len(s) == 64 for s in _seen))

    # -- SOURCE LAWS ------------------------------------------------------
    # The source rule and the call-recorder are BOTH here on purpose: a
    # method can satisfy "contains no ramp literal" by importing one, and it
    # can satisfy "calls the primitive" while still drawing from a literal.
    _routed = "".join(inspect.getsource(getattr(LG.Kit, m))
                      for m in ("spark", "plot", "cover_ramp"))
    _routed += inspect.getsource(LG._pulse)
    check("cover: no routed method INDEXES a ramp (RAMP[ / NA.FINE[)",
          "RAMP[" not in _routed and "NA.FINE[" not in _routed)
    check("cover: no routed method carries a ramp LITERAL to index",
          not any(f'"{r}"[' in _routed or f"'{r}'[" in _routed
                  for r in LG.COVER_RAMPS.values()))
    # `eighths`, `shades` and `fine` are registry rows that NAME another
    # definition (`RAMP`, `BS.SHADES`, `NA.FINE`) rather than spelling one,
    # so there is no literal of theirs to count — the two "ONE definition"
    # checks above are what guards those three.
    # BOTH QUOTE STYLES, and that is the mutation battery talking. M3 reverts
    # instrument's spark to `f"{'⠀⣀⣤⣿'[v]}"` — SINGLE-quoted, because it sits
    # inside a double-quoted f-string — and the first draft of this law
    # counted only `"..."`, so it saw one occurrence and stayed green. A
    # source law that a quote character can walk around is not a source law.
    check("cover: each spelled ramp literal appears ONCE (in the registry)",
          all(inspect.getsource(LG).count(f'"{r}"')
              + inspect.getsource(LG).count(f"'{r}'") == 1
              for rn, r in LG.COVER_RAMPS.items()
              if rn not in ("eighths", "shades", "fine")))
    # THE HONESTY GATE, ASSERTED. `Kit.head` indexes RAMP by a COUNT bucket
    # and must keep doing so: a count is not a coverage, the primitive is not
    # its seat, and the next reader who greps `RAMP[` should find this law
    # before they "finish the routing".
    check("cover: the COUNT seat in Kit.head is deliberately NOT routed",
          "RAMP[min(8, 1 + count // 3)]" in inspect.getsource(LG.Kit.head))
    # The pass-59 rider: two channels, and the comment says two.
    _mo = inspect.getsource(LG).split("TRANSITION = \"transition\"")[0]
    # NAMED FOR WHAT IT READS, and that is the sixty-sixth pass's sweep
    # answering itself. This law is satisfied by a COMMENT — correctly, the
    # comment IS its subject — but its name said "the motion channel list",
    # which reads as a law about the code, so the sweep's shape-4 detector
    # (which discriminates documentation laws by what the law CALLS itself)
    # reported it as vacuous. The law did not change; the name now says
    # which of the two things it is, which is what it should have said.
    check("cover/rider: the module comment enumerating the motion channels "
          "says TWO, not three",
          "THE CHANNELS — THERE ARE TWO" in _mo
          and "3. DIM_LEVEL" not in _mo)
    check("cover/rider: and it says WHY dim_level is not a third channel",
          "is `glyph_frame` under another name" in _mo)

    # -- CALL RECORDER + per-language routing -----------------------------
    _real = LG.coverage_to_glyph
    calls = []
    rets = []

    def _rec(c, ramp, lo=LG.COVER_LO, hi=LG.COVER_HI):
        calls.append((c, ramp))
        rets.append(_real(c, ramp, lo, hi))
        return rets[-1]

    SER = [0, 1, 2, 3, 5, 8, 13, 21]
    try:
        LG.coverage_to_glyph = _rec
        for name in TH.ORDER:
            k = LG.kit(name)
            mech = k.t.get("meter", "blocks")
            calls.clear()
            rets.clear()
            out = k.spark(SER, 8)
            n_expected = 0 if mech == "odometer" else len(LG._resample(SER, 8))
            check(f"cover[{name}]: spark CALLS the primitive {n_expected}x",
                  len(calls) == n_expected, f"got {len(calls)}")
            if mech == "odometer":
                check(f"cover[{name}]: odometer draws FIGURES, not a ramp",
                      set(grey(out)) <= set("0123"))
                check(f"cover[{name}]: odometer never reaches the registry",
                      not calls)
                continue
            check(f"cover[{name}]: cover_ramp() is the registry row for "
                  f"'{mech}'",
                  k.cover_ramp() == ("·:▫" + k.t.get("tally", "▪")
                                     if mech == "tally" else
                                     LG.COVER_RAMPS[
                                         LG.METER_RAMP.get(mech, "blocks")]))
            check(f"cover[{name}]: every spark glyph comes from that ramp",
                  set(grey(out)) <= set(k.cover_ramp()))
            check(f"cover[{name}]: every call was handed THAT ramp",
                  {r for _, r in calls} == {k.cover_ramp()})
            # THE GLASS IS THE PRIMITIVE'S OWN RETURNS, in order. "It was
            # called" and "what it returned is what got drawn" are two
            # claims, and only the second one refuses a branch that calls
            # the primitive and then draws something else.
            check(f"cover[{name}]: the glyphs ON THE GLASS are its returns",
                  grey(out) == "".join(rets))
        calls.clear()
        LG.kit("nord").plot([1, 3, 2, 5], 8, 4)
        check("cover: plot's PARTIAL CELL reaches the primitive (blocks)",
              calls and all(r == LG.COVER_RAMPS["eighths"] for _, r in calls),
              f"{len(calls)} call(s)")
        calls.clear()
        LG._pulse([4, 0, 2, 2], 44)
        check("cover: _pulse reaches the primitive once per bucket",
              len(calls) == 4)
    finally:
        LG.coverage_to_glyph = _real
    check("cover: the recorder was removed again",
          LG.coverage_to_glyph is _real)

    # =====================================================================
    # KIT LEVEL: THE METER FAMILY'S TWO DEFECTS (pass 62 — item #41)
    #
    # Pass 61 cured the coverage RAMPS and measured the SAME two defects
    # alive at the mechanism next door, where no ramp law can reach them:
    # the meters do not route, so `cover[...]` says nothing about them.
    #
    #   law 1 — `_meter_lcd` drew its lit and its ghost segment with the same
    #           `▄▄` in two tones. Colour-stripped, `▄▄ `*n + `▄▄ `*(segs-n)
    #           is `▄▄ `*segs at EVERY value: the bar carried NO reading
    #           without colour, and it is the case DATAVIZ law 1 cites by
    #           name. The census also found it a second time on `_meter_decay`
    #           — the persistence tail's dimmest cell was the track's own
    #           glyph, a hole in the run in greyscale.
    #   law 4 — `_meter_gradient`'s unrun track was literal SPACES, and its
    #           shoulder drew `▓▒░` at ZERO against that blank track, which
    #           is law 4's opposite half: a phantom reading.
    #
    # FOUR INSTRUMENTS, TWO PER LAW, run over all twelve mechanisms rather
    # than over the ten languages — because `decay` and `gradient` are worn
    # by no shipped language (phosphor and bbs were retired) and a
    # language-indexed law renders them zero times.
    # =====================================================================
    print("\n== KIT LEVEL: the METER family (pass 62 — DATAVIZ laws 1 and 4)")

    # THE INK INSTRUMENT, WIDENED ON PURPOSE. The ramp census's `ink` raises
    # on an unknown glyph, because a RAMP may contain only declared marks.
    # A meter row also carries letters and figures, and those are full cells
    # of ink: a printed quantity is how `odometer` satisfies law 4 without
    # ever drawing a track.
    _M_DECL = {"·": 0.10, "┈": 0.15, ":": 0.20, "╌": 0.22, "─": 0.30,
               "▫": 0.35, "━": 0.55, "▪": 0.60, "∙": 0.20, "◦": 0.15,
               "│": 0.30, "├": 0.35, "┤": 0.35}

    def mink(ch):
        if ch == " ":
            return 0.0
        cp = ord(ch)
        if 0x2800 <= cp <= 0x28FF:
            return bin(cp - 0x2800).count("1") / 8
        if 0x2581 <= cp <= 0x2588:
            return (cp - 0x2580) / 8
        nm = _ud.name(ch, "")
        if nm in _SHADE_INK:
            return _SHADE_INK[nm]
        return _M_DECL.get(ch, 1.0)

    def m_ink_cells(s):
        return sum(1 for ch in s if mink(ch) > 0.0)

    def tone_runs(markup):
        """[(tone, text), ...]; `[/]` closes back to the untagged ground.
        The tag pattern is `_TAG`, which is rich's own — one definition."""
        out, stack, buf = [], [], []
        i, s = 0, markup.replace("\\[", "\x00")
        while i < len(s):
            m = _TAG.match(s, i)
            if m:
                if buf:
                    out.append((stack[-1] if stack else "-",
                                "".join(buf).replace("\x00", "[")))
                    buf = []
                if m.group(0) == "[/]":
                    if stack:
                        stack.pop()
                else:
                    stack.append(m.group(0)[1:-1])
                i = m.end()
            else:
                buf.append(s[i])
                i += 1
        if buf:
            out.append((stack[-1] if stack else "-",
                        "".join(buf).replace("\x00", "[")))
        return out

    def bar_only(markup):
        """The quantity row with its printed FIGURE dropped.

        Every mechanism STATES its value (DATAVIZ law 5) in its own tone run,
        so a right-aligned `{pct:>3}%` turns '  0' into '100' and moves the
        row's ink by two cells at zero — which says nothing about whether the
        TRACK is drawn. Dropping the digit-bearing runs is what makes the
        law-4 comparison a claim about the BAR."""
        return "".join(t for _, t in tone_runs(markup)
                       if not re.search(r"\d", t))

    def collisions(markup):
        """The glyphs drawn under TWO tones in one row — law 1's defect as an
        instrument: a level that exists only in tone.

        Spaces are structure. LETTERS AND FIGURES are not levels either: a
        printed quantity is a STATED value (law 5), which is why `odometer`'s
        digits and the word `flow` beside a spark are excluded. What is left
        is drawn marks, and a drawn mark under two tones is the defect."""
        by = {}
        for tone, text in tone_runs(markup):
            by.setdefault(tone, set()).update(
                ch for ch in text if ch != " " and not ch.isalnum())
        bad, tones = set(), sorted(by)
        for a in range(len(tones)):
            for b in range(a + 1, len(tones)):
                bad |= by[tones[a]] & by[tones[b]]
        return bad

    def host(mech, lang="nord"):
        """A kit wearing `mech`. `Kit.t` is the SHARED `THEMES` dict, so this
        REBINDS the attribute — mutating it would corrupt every later law."""
        k = LG.kit(lang)
        k.t = {**k.t, "meter": mech}
        return k

    def m_rows(k, done, total, counts, w=44):
        return k.meter(done, total, counts, w).split("\n")

    MECHS = sorted(LG.METERS)
    CS = [4, 0, 2, 2]
    # THE CENSUSES, WRITTEN AS THE CURE (pass 61's pattern). Both go red in
    # BOTH directions: red if a defect comes back, red if an exemption is
    # claimed and not used.
    #
    # `odometer` states its quantity as a FIGURE and never draws a length, so
    # "the bar moves colour-stripped" is unaskable of it — the digits ARE the
    # response, and they are the cure law 1 prescribes for a tone-only level.
    FIG_MECH = {"odometer"}
    # `odometer` and `dimension` draw no TRACK: a span's LENGTH is its
    # quantity and a drawing never fills anything in. Law 4 reaches them
    # through the ink law below plus their own "STATES its value" laws, and
    # the track comparison is VACUOUS for them — which is why they are named
    # here instead of quietly passing it.
    NO_TRACK = {"odometer", "dimension"}
    # EMPTY, AND THAT IS THE POINT. Pass 62 found `decay` here and cured it
    # rather than filing it; a mechanism added to this set is a mechanism
    # somebody decided to ship with a tone-only level.
    TONE_COLLIDE = set()

    check("meter: every mechanism in METERS is censused below",
          set(MECHS) == set(LG.METERS) and len(MECHS) == 13,
          f"{len(MECHS)} mechanisms")
    for m in MECHS:
        k = host(m)
        lo_r, hi_r = m_rows(k, 1, 8, CS), m_rows(k, 7, 8, CS)
        z_r, f_r = m_rows(k, 0, 8, [0, 0, 0, 0]), m_rows(k, 8, 8, [1, 1, 1, 1])
        moved = (re.sub(r"[0-9]", "#", grey(lo_r[0]))
                 != re.sub(r"[0-9]", "#", grey(hi_r[0])))
        coll = collisions(lo_r[0])
        zi = m_ink_cells(bar_only(z_r[0]))
        fi = m_ink_cells(bar_only(f_r[0]))
        # LAW 1, FIRST LEG: the DRAWING responds to the value, not only the
        # figure beside it. `lcd` failed this from the first pass to the
        # sixty-second: its bar was byte-identical at 0% and at 100%.
        check(f"meter[{m}]: law-1 — the bar RESPONDS to the value colour"
              f"-stripped (the figure masked), or is the declared FIGURES "
              f"mechanism",
              moved == (m not in FIG_MECH), f"moved={moved}")
        # LAW 1, SECOND LEG: and the response is a SHAPE. The census is
        # two-directional — a mechanism that starts drawing its run and its
        # track with one glyph reds here even if the bar still moves.
        check(f"meter[{m}]: law-1 — no drawn mark appears under TWO tones "
              f"(a level that exists only in tone is not a level)",
              bool(coll) == (m in TONE_COLLIDE),
              f"{''.join(sorted(coll)) or '-'}")
        # LAW 4, FIRST LEG: a flat-zero meter is not a blank row.
        check(f"meter[{m}]: law-4 — a flat-zero meter draws INK", zi > 0,
              f"ink={zi}")
        # LAW 4, SECOND LEG: and the track occupies the cells the run would.
        # `gradient` drew three shoulder cells and then SPACES.
        check(f"meter[{m}]: law-4 — the track occupies the run's cells "
              f"(or the mechanism declares it has no track)",
              (zi >= fi) if m not in NO_TRACK else True,
              f"track {zi} vs run {fi}"
              + ("  [VACUOUS — declared no-track]" if m in NO_TRACK else ""))

    # -- THE NAMED CASES, asserted by name rather than by census -----------
    # DATAVIZ law 1's example, at the SECOND seat it was alive on. The ramp
    # census (pass 61) says corgi's spark is cured; this says its METER is.
    _lcd = LG.COVER_RAMPS["lcd"]
    _crow = LG.kit("corgi").meter(3, 8, CS, 44).split("\n")[0]
    _by = {}
    for _t, _x in tone_runs(_crow):
        _by.setdefault(_t, set()).update(ch for ch in _x
                                         if ch != " " and not ch.isalnum())
    _seg = {ch for t, s in _by.items() for ch in s if ch in _lcd}
    check("meter: THE SKILL'S OWN CASE — corgi's lcd METER draws its lit and "
          "its ghost segment with TWO glyphs, not one in two tones",
          _seg == {_lcd[0], _lcd[1]}, f"{sorted(_seg)}")
    check("meter: ... and the two differ in INK, which is the cure that "
          "sentence names (segment HEIGHT, not a tone)",
          mink(_lcd[0]) < mink(_lcd[1]),
          f"{mink(_lcd[0]):.2f} < {mink(_lcd[1]):.2f}")
    # ONE DEFINITION, not two that happen to agree. `plot`'s lcd branch had
    # the pair right while the meter had it wrong, for sixty-two passes.
    _cplot = "".join(grey(r) for r in LG.kit("corgi").plot([0, 3], 8, 4))
    check("meter: the lcd METER and `plot`'s lcd branch draw the SAME pair "
          "(both READ THE ONE SEAT)",
          set(_cplot) - {" "} == {_lcd[0], _lcd[1]}, f"{sorted(set(_cplot))}")
    # THE SPELLING, not the mention: the method's PROSE names the old pair
    # (that is what the comment is for), so the law reads the string literal
    # the code used to carry — `"▄▄ "` — and not the glyph. #45 moved the
    # OTHER half: naming the registry ROW was pass 62's cure and it was one
    # answer too many, so the law now demands the SEAT and refuses the row.
    check("meter: the lcd meter reads `cover_ramp()` — not the registry row "
          "by name (#45), and not the pair spelled out (pass 62)",
          "k.cover_ramp()" in inspect.getsource(LG._meter_lcd)
          and "COVER_RAMPS[" not in inspect.getsource(LG._meter_lcd)
          and '"▄▄ "' not in inspect.getsource(LG._meter_lcd))
    # THE TRACK CURE, by name. `gradient`'s unrun cells were spaces.
    _ph = LG.COVER_RAMPS["phosphor"]
    _grow = host("gradient").meter(0, 8, [0, 0, 0, 0], 44).split("\n")[0]
    check("meter: gradient's TRACK is the phosphor ramp's own unlit glyph",
          set(bar_only(_grow)) - {" "} == {_ph[0]},
          f"{sorted(set(bar_only(_grow)))}")
    # AND THE OPPOSITE HALF OF LAW 4, which making a track visible invites:
    # the shoulder is a fade OUT OF a run, so a run of length zero has none.
    check("meter: gradient draws NO shoulder at zero (a fade out of nothing "
          "is a phantom reading, which is worse than a missing track)",
          _ph[1] not in _grow and _ph[2] not in _grow)
    check("meter: gradient's shoulder still exists where there IS a run",
          _ph[2] in host("gradient").meter(3, 8, CS, 44))
    # DECAY: monotone in ink across all three of its tones, which is the
    # form its law-1 cure takes — the tail no longer reaches the track.
    _drow = bar_only(host("decay").meter(5, 8, CS, 44).split("\n")[0])
    _dseq = [mink(ch) for ch in _drow if ch != " "]
    # THE RUN RISES TO THE HEAD AND THE TRACK IS UNDER ALL OF IT. Stated in
    # two halves because the row is not one monotone sequence — the track
    # follows the head, so a single `a <= b` sweep is the wrong claim (it was
    # the first draft of this law, and it went red on correct code).
    _hd = at(_dseq, max(_dseq), last=True)                  # the head cell
    _run, _trk = _dseq[:_hd + 1], _dseq[_hd + 1:]
    check("meter: decay's RUN rises monotonically to the head — the "
          "persistence tail no longer dips to the track's own glyph",
          all(a <= b for a, b in zip(_run, _run[1:])), f"{_run}")
    check("meter: ... and every TRACK cell is lighter than every run cell, "
          "so the run's extent is readable with the colour stripped",
          _trk and _run and max(_trk) < min(_run), f"{max(_trk)} < {min(_run)}")
    check("meter: decay and gradient READ THE SEAT for the phosphor row (one "
          "definition; gradient's flow row spelled it BACKWARDS, which the "
          "literal-count law cannot see)",
          '"█▓▒░"' not in inspect.getsource(LG._meter_gradient)
          and "k.cover_ramp()" in inspect.getsource(LG._meter_decay)
          and "k.cover_ramp()" in inspect.getsource(LG._meter_gradient))

    # -- #45: THE FAMILY READS ONE SEAT ------------------------------------
    # Five `_meter_*` functions and three of `plot`'s branches named a
    # `COVER_RAMPS` row directly, bypassing `Kit.cover_ramp()` — the one seat
    # documented to answer "which ramp is this language's". It is not a
    # shortcut, it is a SECOND ANSWER: a mechanism is reached through the
    # `meter` token, so a row named inside it is that dispatch re-typed by
    # hand. Byte-identical when cured (308 + 120 render strings, zero moved)
    # because the two agreed — and nothing but a law would keep them agreeing.
    _SEAT_45 = {"lcd": LG._meter_lcd, "braille": LG._meter_braille,
                "decay": LG._meter_decay, "gradient": LG._meter_gradient,
                "step": LG._meter_step}
    for _m, _fn in sorted(_SEAT_45.items()):
        _s = inspect.getsource(_fn)
        check(f"#45[{_m}]: the meter asks `cover_ramp()` and names NO "
              f"registry row",
              "k.cover_ramp()" in _s and "COVER_RAMPS[" not in _s,
              f"seat={'k.cover_ramp()' in _s} row={'COVER_RAMPS[' in _s}")
        # AND THE SEAT MUST ANSWER WHAT THE LITERAL DID, at every kit the
        # mechanism is ever drawn on — the shipped languages that wear it and
        # the two hosts the mechanism grid uses. This is the byte-identity
        # argument written as standing law: if a future `METER_RAMP` edit
        # forked the seat from the mechanism, the render would move silently
        # and only this leg would say so.
        _lit = LG.COVER_RAMPS[LG.METER_RAMP.get(_m, "blocks")]
        _seats = [LG.kit(n) for n in TH.ORDER
                  if LG.kit(n).t.get("meter", "blocks") == _m]
        _seats += [host(_m, h) for h in ("nord", "corgi")]
        check(f"#45[{_m}]: ... and the seat returns the row the literal named,"
              f" on all {len(_seats)} kits that draw it",
              all(_k.cover_ramp() == _lit for _k in _seats), f"{_lit!r}")
    # `plot`'s THREE bypasses are the same defect inside the other primitive,
    # and they are #40d's half of it. `off=` was the third seat that spelled
    # the registry's braille unlit; the census below is narrower by exactly
    # that one.
    _psrc = inspect.getsource(LG.Kit.plot)
    check("#45/plot: no branch names a registry ROW — the lcd pair, the "
          "blocks baseline and braille's `off=` all read the seat",
          _psrc.count("COVER_RAMPS[") == 1
          and 'COVER_RAMPS["eighths"]' in _psrc
          and _psrc.count("self.cover_ramp()") == 3,
          f"rows={_psrc.count('COVER_RAMPS[')} "
          f"seat={_psrc.count('self.cover_ramp()')}")
    # THE ONE REFUSAL, NAMED AS LOUDLY AS THE ROUTES (the skill's rule). The
    # partial TOP CELL is a fraction of ONE cell and needs eight sub-levels;
    # the language's own ramp has three, so routing it to the seat would MOVE
    # CELLS rather than tidy a name. Asserted as a DIFFERENCE, so a
    # maintainer who "finishes the routing" reds here first.
    _kn = LG.kit("nord")
    check("#45/plot: the partial TOP CELL keeps `eighths` — routing it to "
          "the seat would move cells, which is why the refusal is measured "
          "and not merely stated",
          _kn.cover_ramp() != LG.COVER_RAMPS["eighths"]
          and any(LG.coverage_to_glyph(i / 8, LG.COVER_RAMPS["eighths"])
                  != LG.coverage_to_glyph(i / 8, _kn.cover_ramp())
                  for i in range(1, 8)),
          f"{_kn.cover_ramp()!r} vs {LG.COVER_RAMPS['eighths']!r}")

    # -- #40: `plot`'s ZERO COLUMN ----------------------------------------
    # The item claimed FOUR branches printed air for a zero column. Measured
    # (`_p62_prove.py` §3), it was ONE: `boxed`, `dotgrid`, `decay`, `braille`
    # and `lcd` draw their unlit lattice down the WHOLE column, six others
    # stand on a baseline, and only `blocks` — the `else` branch, nord's —
    # drew h rows of nothing. The census records which is which, so the two
    # families cannot silently swap.
    FULL_COLUMN = {"boxed", "braille", "decay", "dotgrid", "lcd"}
    for m in MECHS:
        k = host(m)
        _rs = [grey(r) for r in k.plot([0, 0, 0, 0], 8, 4)]
        check(f"plot[{m}]: law-4 — a ZERO COLUMN stands on a baseline row",
              m_ink_cells(_rs[-1]) > 0, f"{_rs[-1]!r}")
        check(f"plot[{m}]: ... and the rows ABOVE it are air unless the "
              f"mechanism DECLARES a full-column lattice",
              (sum(m_ink_cells(r) for r in _rs[:-1]) > 0)
              == (m in FULL_COLUMN))
    check("plot: nord's zero column draws the `blocks` ramp's own unlit "
          "(the track `_meter_blocks` draws one row above)",
          set(grey(LG.kit("nord").plot([0, 0, 0, 0], 8, 4)[-1]))
          == {LG.COVER_RAMPS["blocks"][0]})
    # AND THE CURE MAY NOT REACH A NON-ZERO COLUMN. The baseline branch is
    # guarded by `pos == 0` inside the `else`, which is reachable only when
    # the column's eighths total is zero — this is that claim, measured.
    check("plot: the baseline cure cannot reach a column with data in it "
          "(a full-height column is still all run, no track under it)",
          grey(LG.kit("nord").plot([9], 4, 4)[-1]).strip("█") == "")

    # =====================================================================
    # #40d — `plot`'s PER-ROW BRANCHES, GOVERNED
    #
    # The census question was never "do they route" — the skill REFUSES
    # routing here ("lit/unlit per ROW is a boolean, not a coverage") — but
    # "what decides the LEVEL, and is that seat lawful". The answer, measured
    # (`_p65_prove.py` §1): NOT ONE per-row branch decides a level. Every
    # branch is handed `v`, the column's height, and decides only lit/unlit
    # against its own row index. The level is decided ONCE per column, above
    # the branches — and it was decided by a RE-TYPED COPY of
    # `coverage_index`, in THREE places (`v`, braille's `lv`, blocks' `u`).
    #
    # DATAVIZ law 3 names exactly that defect in the sentence that appoints
    # the primitive's seat: "nine inline copies are nine chances to lose it,
    # and one copy means spending the floor reds this law in every language
    # at once." It did not. Each copy carried its own `max(1, ...)`, so the
    # floor was safe by being in three places rather than by being in its
    # seat — which is the property law 3 refuses, not the one it wants.
    #
    # The legs below are asked of the COLUMN each branch composes, and every
    # one of them reads the RENDERED string. Pass 63's finding is the reason:
    # a law that sweeps a re-typed copy of the arithmetic is not a law about
    # the mechanism. The model survives as exactly ONE law, the equality.
    _PLOT_H = 4
    # The FILL family draws a run whose ink GROWS with the level; the MARK
    # family states the level by the POSITION of one mark and spends the same
    # ink at every level (law 5 is what blesses that: the mark is read against
    # the baseline the branch always draws). Two claims, so the monotone leg
    # is asked of the first and refused BY NAME for the second — and the
    # census bites both ways, so widening the list to silence a red costs
    # more reds than it buys.
    #
    # THE FIRST DRAFT OF THIS SET HAD THREE MEMBERS AND THE MEASUREMENT SENT
    # ONE BACK. `dimension` looks like a mark family — one `─` at the
    # measured height, never a filled column — but it stands that mark on a
    # LEADER of dots that grows with the level, so its ink is strictly
    # monotone and it belongs with the fills. Same correction #43's "four
    # collisions" and #40's "four branches" took: a declaration is a claim
    # until a census makes it a fact.
    PLOT_MARK_FAMILY = {"hairline", "odometer"}
    import unicodedata as _U40

    def _col(k, x, h=_PLOT_H, top=_PLOT_H, w=6):
        return tuple(grey(r) for r in k.plot([x], w, h, top))

    _flat = set()
    for m in MECHS:
        k = host(m)
        _cols = [_col(k, x) for x in range(_PLOT_H + 1)]
        check(f"plot40d[{m}]: INJECTIVE — the {_PLOT_H + 1} levels draw "
              f"{_PLOT_H + 1} DISTINCT columns with the colour stripped "
              f"(law 1 + law 13: a level that draws what another draws is "
              f"not data)",
              len(set(_cols)) == _PLOT_H + 1,
              f"{len(set(_cols))} distinct")
        check(f"plot40d[{m}]: the MICROBAR FLOOR survives the composition — "
              f"level 1 does not draw level 0 (law 3, on the glass)",
              _cols[0] != _cols[1], f"{_cols[1]}")
        _inks = [sum(mink(ch) for r in c for ch in r) for c in _cols]
        _mono = all(a < b for a, b in zip(_inks, _inks[1:]))
        if not _mono:
            _flat.add(m)
        if m not in PLOT_MARK_FAMILY:
            check(f"plot40d[{m}]: FILL family — the column's ink grows "
                  f"strictly with the level",
                  _mono, f"{[round(i, 2) for i in _inks]}")
        else:
            check(f"plot40d[{m}]: MARK family (declared) — the ink is FLAT "
                  f"and the mark MOVES; injectivity above is what holds it",
                  not _mono and len({tuple(c) for c in _cols})
                  == _PLOT_H + 1, f"{[round(i, 2) for i in _inks]}")
        check(f"plot40d[{m}]: DETERMINISTIC — 50 renders of one input are "
              f"one string",
              len({_col(k, 2) for _ in range(50)}) == 1)
        check(f"plot40d[{m}]: no DOUBLE-WIDTH glyph on any column",
              not any(_U40.east_asian_width(ch) in ("W", "F")
                      for c in _cols for r in c for ch in r))
    # THE CENSUS, BOTH WAYS. A maintainer who adds a mechanism to the mark
    # family to make a monotone red go away takes a red here instead, and one
    # who lets a mark family's ink start growing takes one too.
    check("plot40d: the MARK family is exactly the set whose column ink is "
          "flat — the declaration is a census, not a preference",
          _flat == PLOT_MARK_FAMILY,
          f"measured={sorted(_flat)} declared={sorted(PLOT_MARK_FAMILY)}")

    # -- THE LEVEL SEAT, and the drive-check that proves it is one ---------
    # A source grep says the copies are gone; it cannot say the seat is
    # REACHED. This does: spend the floor AT ITS SEAT and watch `plot`'s
    # microbar column change. Before this pass it would not have — which is
    # the whole of what the cure bought, stated as the one thing that can
    # fail if it is undone.
    _psrc40 = inspect.getsource(LG.Kit.plot)
    check("plot40d: the level is decided by `coverage_index`, THREE times "
          "(the column, braille's sub-rows, the eighths cell) and by no "
          "re-typed copy of it",
          _psrc40.count("coverage_index(") == 3
          and "max(1, min(" not in _psrc40,
          f"calls={_psrc40.count('coverage_index(')}")
    _real40 = LG.coverage_index
    _floor_moved, _floor_ran = [], []
    try:
        def _spent(c, levels, lo=1 / 32, hi=1.0):
            _floor_ran.append(1)
            return _real40(c, levels, lo, hi)
        _before = {m: _col(host(m), 1, 4, 100) for m in MECHS}
        LG.coverage_index = _spent
        _after = {m: _col(host(m), 1, 4, 100) for m in MECHS}
    finally:
        LG.coverage_index = _real40
    _floor_moved = [m for m in MECHS if _before[m] != _after[m]]
    check("plot40d: the FLOOR IS IN ITS SEAT — spending `COVER_LO` at the "
          "primitive moves `plot`'s 1-in-100 column in every mechanism, "
          "which is DATAVIZ law 3's own sentence and was FALSE for `plot` "
          "until the three copies were retired",
          set(_floor_moved) == set(MECHS),
          f"moved {len(_floor_moved)}/{len(MECHS)}: "
          f"{sorted(set(MECHS) - set(_floor_moved))} held")
    check("plot40d: ... and the floor probe actually ran (a patch nothing "
          "calls would report the same green)",
          bool(_floor_ran), f"{len(_floor_ran)} calls")
    # THE MODEL, kept as EXACTLY ONE law. This is the equality that made the
    # cure byte-identical; it is stated once, off to the side, and no other
    # leg above depends on it.
    check("plot40d: the retired inline form and the seat agree at every "
          "point of a domain that runs OUTSIDE [0, top] at both ends (the "
          "byte-identity argument, kept as ONE law and not re-typed into the "
          "legs above)",
          all((0 if _x <= 0 else
               max(1, min(_lv, round(_lv * _x / _tp))))
              == LG.coverage_index(_x / _tp, _lv)
              for _lv in (1, 4, 16, 32) for _tp in (1, 3, 7, 10, 100)
              for _x in (-3, -1, 0, 1, 2, 5, 9, 11, 99, 999)))

    # =====================================================================
    # KIT LEVEL: THE SECOND QUANTISER FAMILY (pass 63 — item #39)
    #
    # Pass 60 built the coverage primitive and DEFERRED the band-threshold
    # seats on render-risk grounds — "routing would move cells" — not on
    # proven compliance. That is a grandfathering shadow: an exemption whose
    # whole argument is that curing it is expensive. This section removes it
    # by asking the only question that settles an exemption — does the
    # mechanism AS SHIPPED satisfy the laws? — and the answer is written as
    # standing law either way, so the exemption can never again rest on
    # nobody having measured.
    #
    # THE ROUTING QUESTION IS CLOSED AND STAYS CLOSED. Pass 60 rejected
    # routing because it moves real cells on a shipped surface; nothing here
    # reopens it. What is asserted is COMPLIANCE, and the call recorder below
    # asserts the seats reach the primitive ZERO times — so "does not route"
    # is a measured fact rather than an omission.
    #
    # THE ITEM'S OWN CENSUS OF THE FAMILY WAS SHORT BY ONE SEAT. #39 named
    # `naught.dot_heat` and `_meter_braille`'s flow row. A grep for the band
    # constants finds THREE: `_meter_step`'s flow row is the same 3-level
    # band quantiser wearing `. o O`. Pass 62 saw that ROW (item #43, the
    # ungoverned flow rows) and did not recognise the QUANTISER. Same shape
    # as pass 62's finding that #40's own measurement was wrong — an item's
    # description is a claim, not a census, and this one is now a census.
    #
    # SEAT C COULD NOT HAVE BEEN AUDITED WITHOUT OPENING THE INSTRUMENT.
    # `mink` returns 1.0 for any letter, because a printed FIGURE is a full
    # cell of stated value (law 5) — so `.`, `o` and `O` all weighed the
    # same and no ink law could ORDER them. Three declarations, argued on
    # the existing table's own logic, are what make C measurable at all.
    # =====================================================================
    print("\n== KIT LEVEL: the BAND quantiser family (pass 63 — item #39)")

    # THE INK INSTRUMENT, EXTENDED FOR SEAT C ONLY. Kept LOCAL rather than
    # folded into `_M_DECL`: `mink` is read by the pass-62 meter laws, and a
    # glyph's weight changing under those laws to serve this section is
    # exactly the kind of silent coupling this suite exists to refuse.
    # `·` is one dot at 0.10 and `:` is two at 0.20, so a FULL STOP was
    # 0.10; a hollow mark sat at 0.35 (`▫`) so a small ring was 0.35; a
    # large ring took the heavy slot at 0.55 (`━`).
    #
    # PASS 64 EMPTIED THIS TABLE, AND THAT IS THE MEASURABLE HALF OF #43'S
    # CURE. Seat C's ramp WAS `. o O` — three letters, which `mink` weighs
    # 1.0 apiece, so an ORDER over them had to be declared into existence
    # and the seat was un-auditable without it. The cure gave the row
    # darkside's DECLARED coverage ramp instead of a private alphabet, and
    # a ladder of lower-eighth blocks is weighed by the SHARED instrument
    # natively. **A local declaration that stops being NEEDED is the right
    # way for one to go away** — widening `_M_DECL` to serve this section
    # would have been the silent coupling this suite exists to refuse, and
    # the table is kept (empty) so that widening it still reds.
    _BAND_DECL = {}

    def bink(ch):
        return _BAND_DECL.get(ch, mink(ch))

    check("band: the ink instrument is now `mink` ALONE — the three ASCII "
          "declarations seat C needed to be measurable at all are gone with "
          "the letters they weighed (#43's cure, stated as an instrument)",
          _BAND_DECL == {}, f"{sorted(_BAND_DECL)}")

    # -- THE FAMILY CENSUS, run over the SOURCE rather than over a list ----
    # Two-directional by construction: a fourth band seat reds this (it is
    # un-audited), and deleting one reds it too (the audit below would go
    # vacuous). The item said two; the source says three.
    _band_hits = []
    for _py in sorted((Path(LG.__file__).resolve().parent).glob("*.py")):
        for _i, _ln in enumerate(_py.read_text(encoding="utf-8").splitlines(),
                                 1):
            if "0.66" in _ln or "0.33" in _ln:
                _band_hits.append(f"{_py.name}:{_i}")
    check("band: the package holds EXACTLY three band-threshold seats — #39 "
          "named two, and `_meter_step`'s flow row is the third",
          len(_band_hits) == 3, f"{_band_hits}")

    # THE SEATS, each pinned to its source anchor. A seat that moves ABORTS
    # the audit into a red rather than quietly measuring nothing — pass 60's
    # deferral survived three passes on exactly that kind of silence.
    _A_SRC = inspect.getsource(LG.NA.dot_heat)
    _B_SRC = inspect.getsource(LG._meter_braille)
    _C_SRC = inspect.getsource(LG._meter_step)
    check("band[A dot_heat]: the seat is where the audit says it is",
          "lvl = 3 if frac > 0.66 else (2 if frac > 0.33 else "
          "(1 if frac > 0 else 0))" in _A_SRC)
    # THE TWO FLOW SEATS MOVED IN PASS 64 AND THEIR ANCHORS MOVED WITH THEM:
    # B now NAMES the registry's two ends (#44) and C's middle level is `◦`
    # (#43). An anchor that still matched the old spelling would be an audit
    # measuring a mechanism that no longer exists.
    check("band[B braille]: the seat is where the audit says it is",
          'ramp[3] if n > (hi or 1) * 0.66 else ("⠶" if n else ramp[0])'
          in _B_SRC)
    check("band[C step]: the seat is where the audit says it is",
          "ramp[3] if x > (hi or 1) * 0.66 else (ramp[2] if x" in _C_SRC
          and "else ramp[0])" in _C_SRC)

    _FINE = tuple(LG.NA.FINE)
    _FLOWB = ("⠐", "⠶", "⣿")
    _FLOWC = ("▁", "▄", "█")

    # -- THE READERS: every level below is read OFF THE RENDERED STRING ----
    # An audit that sweeps a re-typed copy of the arithmetic proves nothing
    # about the mechanism that ships, so the pure model is PROVED equal to
    # the glass before it is trusted (the `glass == pure` law per seat).
    #
    # THE SWEEP RIDES EXACT RATIONALS. The first draft built
    # `counts=[round(c * 1e6), 1e6]`, which turns a coverage of 1e-9 into
    # ZERO counts and reported a MICROBAR-FLOOR failure that belonged to the
    # probe. A `counts` list is integers; asking a seat about a coverage it
    # cannot be handed is measuring the instrument.
    def _row1(lang, nd):
        """The flow row's DRAWN glyphs, cut before the caption.

        The cut is not cosmetic: `_meter_step` draws its middle level as `o`
        and its caption is the word `flow`, so a reader that scans the whole
        row picks the `o` out of the LABEL — item #43's tone-collision
        finding, read as a measurement hazard."""
        # SENTINEL "": a meter that stopped drawing its SECOND row has no
        # flow row at all, and "" carries no glyph — so `_idx` below returns
        # -1 for it and every level law in this band goes red naming the
        # level it could not find, instead of the file dying on `[1]`.
        return grey(nth(LG.kit(lang).meter(3, 8, list(nd), 44).split("\n"),
                        1, "")).split(" ")[0]

    def _idx(ramp, drawn):
        """The level a drawn glyph names, or -1 when the row draws something
        this audit does not know.

        IT RETURNS RATHER THAN RAISES, and pass 64's battery is why. Reverting
        `_meter_step`'s cure made this reader hit a glyph outside `_FLOWC`;
        the reader raised, the SUITE DIED at 7591 checks, and a mutant that
        kills the run is indistinguishable from a mutant nothing catches. -1
        reds MONOTONE, both THRESHOLD legs and the model equality at once,
        which is what "the seat moved" should look like."""
        return ramp.index(drawn) if drawn in ramp else -1

    def _gA(nd):
        out = LG.NA.dot_heat(list(nd), 2, "on", "mid", "off", gap=0)
        seen = [g for g in grey(out) if g in _FINE]
        return at(_FINE, seen[0]) if seen else -1

    def _gB(nd):
        return _idx(_FLOWB, _row1("instrument", nd)[0])

    def _gC(nd):
        return _idx(_FLOWC, _row1("darkside", nd)[0])

    def _pA(f):
        return 3 if f > 0.66 else (2 if f > 0.33 else (1 if f > 0 else 0))

    def _pBC(f):
        return 2 if f > 0.66 else (1 if f > 0 else 0)

    BAND_SEATS = (("A dot_heat", _gA, _pA, _FINE, 1372),
                  ("B braille", _gB, _pBC, _FLOWB, 359),
                  ("C step", _gC, _pBC, _FLOWC, 359))
    # dense, and it LANDS on every band edge — a sweep that steps over 0.33
    # says nothing about the boundary that decides the level
    _BG = [(i, 4000) for i in range(4001)]
    _BE = [(0, 1), (1, 10 ** 9), (33, 100), (330001, 10 ** 6),
           (66, 100), (660001, 10 ** 6), (999999, 10 ** 6), (1, 1)]
    # SORTED BY COVERAGE, and the first draft was not — the edge points were
    # appended after the sweep, so the MONOTONE law read the grid out of
    # order and went red on three correct seats. Third pass running: a law
    # that reds on correct code is the law being wrong.
    _BALL = sorted(set(_BG + _BE), key=lambda nd: (nd[0] / nd[1], nd[1]))
    _BCV = {nd: nd[0] / nd[1] for nd in _BALL}

    for _tag, _glass, _pure, _ramp, _ndiv in BAND_SEATS:
        _top = len(_ramp) - 1
        _dens = [bink(g) for g in _ramp]
        # EVERY LAW BELOW READS THIS LIST, AND IT COMES OFF THE GLASS.
        # The first draft swept the RE-TYPED model instead, and the mutation
        # battery caught it: M1 inverts a band in `naught.py` and the
        # MONOTONE law stayed GREEN, because a mutation to the code cannot
        # reach a copy of the arithmetic living in the suite. A law that
        # cannot fail when the mechanism changes is not a law about the
        # mechanism. The pure model survives as ONE law — the equality below
        # — and everything else is measured on the render.
        _gmap = {nd: _glass(nd) for nd in _BALL}
        _lv = [_gmap[nd] for nd in _BALL]
        check(f"band[{_tag}]: the arithmetic swept IS the arithmetic RENDERED "
              f"({len(_BALL)} exact rational coverages, band edges included)",
              all(_gmap[nd] == _pure(_BCV[nd]) for nd in _BALL))
        # -- the four laws the coverage primitive carries ------------------
        check(f"band[{_tag}]: MONOTONE — c1 < c2 => level(c1) <= level(c2)",
              all(a <= b for a, b in zip(_lv, _lv[1:])))
        check(f"band[{_tag}]: MONOTONE in ink — the ramp never gets lighter",
              all(a <= b for a, b in zip(_dens, _dens[1:])),
              " ".join(f"{d:.3f}" for d in _dens))
        check(f"band[{_tag}]: DETERMINISTIC — 50 renders of one coverage give "
              f"ONE glyph",
              all(len({_glass(nd) for _ in range(50)}) == 1
                  for nd in ((0, 1), (33, 100), (34, 100), (1, 2), (67, 100),
                             (1, 1))))
        check(f"band[{_tag}]: THRESHOLD — coverage 0 draws the unlit glyph "
              f"({_ramp[0]!r})",
              _gmap[(0, 1)] == 0)
        check(f"band[{_tag}]: THRESHOLD — coverage 1 draws the TERMINAL "
              f"({_ramp[-1]!r})",
              _gmap[(1, 1)] == _top)
        check(f"band[{_tag}]: THRESHOLD — only the two END indices are "
              f"reachable outside [lo, hi]",
              LG.COVER_LO == 0.0 and LG.COVER_HI == 1.0
              and _gmap[(0, 1)] == 0 and _gmap[(1, 1)] == _top)
        # DATAVIZ law 3, which is where `lo = 0.0` came from: "we have 1
        # overdue" may not render as "we have none". One item in a BILLION
        # still draws a mark.
        check(f"band[{_tag}]: MICROBAR FLOOR — a nonzero coverage is not the "
              f"unlit glyph (law 3: a 1 may not render as a 0)",
              _gmap[(1, 10 ** 9)] >= 1)
        # NO DEAD BAND, NO UNREACHABLE LEVEL — and level 0's preimage is the
        # single point {0}, which is exactly what `lo = 0.0` means.
        _pre = {}
        for nd in _BG:
            _pre[_gmap[nd]] = _pre.get(_gmap[nd], 0) + 1
        check(f"band[{_tag}]: every level is REACHABLE and no band is dead "
              f"(each of {len(_ramp)} levels owns part of [0,1])",
              set(_pre) == set(range(len(_ramp))) and all(v > 0
                                                          for v in _pre.values()),
              f"{dict(sorted(_pre.items()))}")
        # `.get`, not `[0]`: when a seat is mutated so that level 0 is never
        # reached, the subscript RAISED and killed the run — pass 64's M1
        # took the suite down at 7640 lines with six reds already printed.
        # A law that cannot report its own failure is not a law.
        check(f"band[{_tag}]: ... and level 0 is the single point c=0 — the "
              f"`lo = 0.0` ruling, not a band",
              _pre.get(0) == 1, f"{_pre.get(0)}")
        # -- DATAVIZ law 1: a level that exists only in TONE is not a level -
        check(f"band[{_tag}]: GREYSCALE — the levels are pairwise DISTINCT "
              f"colour-stripped",
              len(set(_ramp)) == len(_ramp), f"{_ramp}")
        check(f"band[{_tag}]: GREYSCALE — the two ends differ in INK",
              _dens[0] < _dens[-1], f"{_dens[0]:.3f} -> {_dens[-1]:.3f}")
        # -- pass 61's two ceilings ----------------------------------------
        check(f"band[{_tag}]: law-4 — the unlit level carries INK "
              f"({_ramp[0]!r})",
              _dens[0] > 0.0, f"ink={_dens[0]:.3f}")
        check(f"band[{_tag}]: law-4 — ... and at most a QUARTER of the cell "
              f"(a track that reads as data is worse than none)",
              _dens[0] <= TRACK_MAX, f"{_dens[0]:.3f} <= {TRACK_MAX}")
        check(f"band[{_tag}]: law-4 — the unlit glyph is none of the LIT ones",
              _ramp[0] not in _ramp[1:])
        check(f"band[{_tag}]: no DOUBLE-WIDTH glyph (EAW W/F would jiggle "
              f"every row it lands in)",
              all(_ud.east_asian_width(g) not in ("W", "F") for g in _ramp))
        # -- THE DIVERGENCE, MEASURED AND PINNED ---------------------------
        # #39's whole content was "they disagree". They do. The record has to
        # say WHETHER that is a violation, and it is not: two quantisers that
        # are each monotone, deterministic, threshold-honouring and
        # greyscale-separable may put their level changes in different
        # places. The laws constrain the SHAPE of a quantiser, they do not
        # appoint one band layout. Pinned as a NUMBER so the claim stays a
        # measurement — red if a band edge moves in either direction.
        _div = sum(1 for nd in _BG
                   if _gmap[nd] != LG.coverage_index(_BCV[nd], _top))
        check(f"band[{_tag}]: DIVERGENCE from nearest-index is measured, not "
              f"asserted — and it is a DIFFERENCE, not a law violation "
              f"(both quantisers pass every law above)",
              _div == _ndiv,
              f"{_div} of {len(_BG)} grid points "
              f"({100 * _div / len(_BG):.1f}%)")
        # -- AND ON THE SHIPPED SURFACE ------------------------------------
        # The ceilings are a claim about the GLASS, so a flat-zero row of the
        # language that actually wears the seat has to carry ink. `dot_heat`
        # is reached through naught's meter, not called directly.
        _lang = {"A dot_heat": "naught", "B braille": "instrument",
                 "C step": "darkside"}[_tag]
        # SENTINEL "": the law below counts DRAWN cells and demands > 0, so
        # a missing flow row scores 0 and reds the law with the row printed
        # beside it. That is the claim exactly — "the ceiling is a claim
        # about the render" is false the moment there is no render.
        _zrow = grey(nth(LG.kit(_lang).meter(0, 8, [0, 0, 0, 0],
                                             44).split("\n"), 1, ""))
        _zink = sum(1 for ch in _zrow if ch != " " and not ch.isalnum())
        check(f"band[{_tag}]: law-4 ON THE GLASS — {_lang}'s flat-zero flow "
              f"row draws INK (the ceiling is a claim about the render)",
              _zink > 0, f"{_zink} drawn cells  {_zrow!r}")

    # -- pass 60's three named disagreements, kept by name -----------------
    # READ OFF THE GLASS, like everything else — `_pA` is the model, and the
    # model is only ever allowed to answer the one equality law above.
    _NAMED = ((34, 100), (40, 100), (67, 100))
    check("band: pass 60's measured disagreements are still the three it "
          "named (c = 0.34, 0.40, 0.67)",
          all(_gA(nd) != LG.coverage_index(nd[0] / nd[1], 3)
              for nd in _NAMED),
          " ".join(f"{nd[0] / nd[1]}: band={_gA(nd)} "
                   f"nearest={LG.coverage_index(nd[0] / nd[1], 3)}"
                   for nd in _NAMED))

    # -- WHAT THE EXEMPTION RESTS ON, pinned so an edit cannot move it -----
    # A's greyscale leg passes because its ramp separates level 0 from level
    # 1 by dot POSITION, not by dot COUNT — both are one dot, so the ink
    # MASSES tie. That tie is lawful exactly where it is: at the (unlit,
    # first-lit) boundary, which is the track/data boundary and not a step
    # between two data levels. Move it to (1,2) and two DATA levels become
    # indistinguishable in ink — a real defect no existing law would see,
    # because the registry's monotone law is `<=`.
    _fine_ties = {(i, i + 1) for i in range(len(_FINE) - 1)
                  if bink(_FINE[i]) == bink(_FINE[i + 1])}
    check("band: the `fine` ramp's ink TIE is at exactly the (unlit, "
          "first-lit) pair — a tie between two DATA levels would be a defect "
          "the registry's `<=` monotone law cannot see",
          _fine_ties == {(0, 1)},
          f"{sorted(_fine_ties)}  inks="
          + " ".join(f"{bink(g):.3f}" for g in _FINE))
    check("band: ... and the pair separates by dot POSITION, which is the "
          "argument the registry already declares for this ramp",
          _FINE[0] != _FINE[1] and ord(_FINE[0]) != ord(_FINE[1]),
          f"{_FINE[0]!r} U+{ord(_FINE[0]):04X} vs "
          f"{_FINE[1]!r} U+{ord(_FINE[1]):04X}")
    # A CANNOT FORK FROM THE REGISTRY: `dot_heat` indexes `NA.FINE`, and the
    # `fine` registry row IS that tuple joined. One definition.
    check("band[A]: its ramp IS the routed `fine` registry row — so the seat "
          "that does not route still cannot draw a different ramp",
          "".join(_FINE) == LG.COVER_RAMPS["fine"],
          f"{''.join(_FINE)!r}")
    # B COULD, AND AFTER PASS 64 IT CANNOT SPELL A SECOND COPY — but this
    # law does not change, because it is the STRONGER of the two: naming
    # stops the METER drifting, and a VALUE law reds whichever side moves.
    # #44 is the naming; this is the guard that survives it.
    check("band[B]: its two ends ARE the `braille` registry row's two ends "
          "(a VALUE law, kept after #44's naming: it reds whichever "
          "side drifts)",
          _FLOWB[0] == LG.COVER_RAMPS["braille"][0]
          and _FLOWB[-1] == LG.COVER_RAMPS["braille"][-1],
          f"{_FLOWB[0]!r}/{_FLOWB[-1]!r} vs "
          f"{LG.COVER_RAMPS['braille'][0]!r}/"
          f"{LG.COVER_RAMPS['braille'][-1]!r}")
    check("band[B]: ... and its MIDDLE level is its own — a 3-level row on a "
          "4-level ramp is not a copy of it",
          _FLOWB[1] not in LG.COVER_RAMPS["braille"], f"{_FLOWB[1]!r}")

    # -- "DOES NOT ROUTE" IS A MEASURED FACT, NOT AN OMISSION -------------
    # The exemption is now compliance-based, so the thing it is an exemption
    # FROM has to be asserted too. If somebody routes these seats later, this
    # reds and the record gets updated deliberately.
    _real_c2g = LG.coverage_to_glyph
    _bcalls = []

    def _brec(c, ramp, lo=LG.COVER_LO, hi=LG.COVER_HI):
        _bcalls.append((c, ramp))
        return _real_c2g(c, ramp, lo, hi)

    try:
        LG.coverage_to_glyph = _brec
        LG.NA.dot_heat([4, 0, 2, 2], 8, "on", "mid", "off", gap=0)
        _n_a = len(_bcalls)
        _bcalls.clear()
        LG.kit("instrument").meter(3, 8, [4, 0, 2, 2], 44)
        LG.kit("darkside").meter(3, 8, [4, 0, 2, 2], 44)
        _n_bc = len(_bcalls)
    finally:
        LG.coverage_to_glyph = _real_c2g
    check("band: the three seats reach the primitive ZERO times — the "
          "exemption is COMPLIANCE, and what it exempts them from is stated",
          _n_a == 0 and _n_bc == 0, f"A={_n_a}  B+C={_n_bc}")
    check("band: the recorder was removed again",
          LG.coverage_to_glyph is _real_c2g)

    # -- DETERMINISM ACROSS PROCESSES -------------------------------------
    # Same reason as the registry's: a dither keyed off `hash()` is perfectly
    # stable inside one run and unstable between two, and a 50-call loop
    # cannot see it. Run over all three seats through their RENDERED rows.
    _bcode = (
        "import sys, hashlib, re; sys.path.insert(0, r'%s');"
        "from taskboard import language as L; from taskboard import naught "
        "as N; T=re.compile(r'\\[[a-z#/@][^\\[]*?\\]'); g=lambda s: T.sub('', s);"
        "h=lambda i: [x for x in g(N.dot_heat([i,399],2,'a','b','c',gap=0))"
        " if x in N.FINE][0];"
        "p=lambda nm,i: g(L.kit(nm).meter(3,8,[i,399],44)"
        ".split(chr(10))[1]).split(' ')[0][0];"
        "s=''.join(h(i)+p('instrument',i)+p('darkside',i) for i in range(400));"
        "print(hashlib.sha256(s.encode('utf-8')).hexdigest())"
        % Path(LG.__file__).resolve().parents[1])
    _bmine = __import__("hashlib").sha256("".join(
        _FINE[_pA(i / 399)] + _FLOWB[_pBC(i / 399)] + _FLOWC[_pBC(i / 399)]
        for i in range(400)).encode("utf-8")).hexdigest()
    _bseen = []
    for _seed in ("0", "1", "271828"):
        _bp = _sub.run([sys.executable, "-c", _bcode], capture_output=True,
                       text=True, encoding="utf-8",
                       env={**_os.environ, "PYTHONHASHSEED": _seed,
                            "PYTHONIOENCODING": "utf-8"})
        _bseen.append(_bp.stdout.strip())
    check("band: DETERMINISTIC across processes (3 fresh PYTHONHASHSEEDs, "
          "400 coverages x 3 seats, read off the rendered rows)",
          all(s == _bmine for s in _bseen), f"{_bmine[:12]}…")
    check("band: the cross-process probe actually ran (not 3 empty strings)",
          all(len(s) == 64 for s in _bseen))

    # =====================================================================
    # KIT LEVEL: THE METER'S FLOW / LOAD ROW (pass 64 — items #43 and #44)
    #
    # Pass 62 wrote four laws on the meter's BAR row and left the second row
    # censused and UNGOVERNED, on honest grounds: telling a declared idiom
    # from a defect needs a per-mechanism argument, and pass 62 declined to
    # pretend it had made one. This section makes it, one verdict per
    # collision, and the cure the argument condemns has moved cells.
    #
    # THE ITEM'S OWN COUNT WAS A CLAIM, THE THIRD IN A ROW. #43 states FOUR
    # tone collisions on row 1. The instrument it cites — pass 62's
    # `collisions`, which DROPS letters and figures because a printed
    # quantity is a stated value (DATAVIZ law 5) — reports ONE. The four
    # exist only under an alnum-INCLUSIVE reading the item described and
    # never ran. Both readings are asserted below, because which one is
    # right IS the question, and a suite that quietly picks one has decided
    # the thing it was supposed to prove. (#40's four air-printing branches
    # were one; #39's two band seats were three; #43's four were one under
    # its own instrument.)
    #
    # THE DISCRIMINATING RULE, one sentence, four applications:
    #
    #   A tone collision on a flow row is a DECLARED IDIOM when the two
    #   sides of it state the SAME datum twice (a FIGURE — law 5) or when
    #   one side is CHROME that delimits rather than measures. It is a
    #   DEFECT when a LEVEL MARK collides with something that is not a
    #   level, because then the colour-stripped row carries more marks than
    #   it has buckets and the extra ones read as data.
    #
    # Three defend, one is cured. `dimension`'s `├┤` bound every span in
    # both tones (chrome; the quantity is the span's LENGTH and the figure
    # standing on it). `lcd`'s and `odometer`'s collisions are entirely
    # FIGURES — the solari precedent, where the digit IS the datum. And
    # `_meter_step` drew its middle level as the letter `o` in a row whose
    # own caption is the word `flow`: five marks of its ramp for four
    # buckets, colour-stripped.
    # =====================================================================
    print("\n== KIT LEVEL: the METER's FLOW row (pass 64 — items #43, #44)")

    def flow_markup(k, counts=CS, done=1, total=8, w=44):
        """Row 1 as markup, or None when the mechanism spends the row.

        `hairline` has none — swiss buys emptiness with it — and a law that
        passes silently on a row that does not exist is the vacuous shape
        this suite sweeps for, so it is returned as None and NAMED."""
        r = k.meter(done, total, counts, w).split("\n")
        return None if len(r) < 2 or not r[1].strip() else r[1]

    def flow_collisions(markup, alnum):
        """`collisions`, with the letters-and-figures cut made a PARAMETER.

        Pass 62 hard-coded `alnum=False` and was right to on the BAR row: a
        printed quantity is a stated value, not a level. On a row whose
        LEVEL MARKS are themselves letters, that same cut drops the defect."""
        by = {}
        for tone, text in tone_runs(markup):
            by.setdefault(tone, set()).update(
                ch for ch in text
                if ch != " " and (alnum or not ch.isalnum()))
        bad, tones = set(), sorted(by)
        for a in range(len(tones)):
            for b in range(a + 1, len(tones)):
                bad |= by[tones[a]] & by[tones[b]]
        return bad

    def flow_ramp(k):
        """The flow row's level ramp, READ OFF THE GLASS — never declared.

        Three counts pick the three levels of a band quantiser in one
        render: with `hi = 10`, a bucket of 0 is unlit, 1 is the middle band
        (1 <= 6.6) and 10 is the terminal. Pass 63's finding applied one
        section later — a law that sweeps a RE-TYPED copy of the mechanism
        cannot fail when the mechanism changes, so the ramp comes off the
        render and a mutation to `language.py` moves it."""
        r = flow_markup(k, counts=[0, 1, 10])
        if r is None:
            return None
        drawn = grey(r).split(" ")[0]
        return (tuple(drawn) if len(drawn) == 3 and len(set(drawn)) == 3
                else None)

    def flow_caption(k):
        """The row's trailing PROSE: the last tone run that is pure letters.
        `lcd` has none — it spends the row on channel numbers."""
        r = flow_markup(k)
        if r is None:
            return ""
        for _, text in reversed(tone_runs(r)):
            if text.strip() and text.strip().isalpha():
                return text.strip()
        return ""

    # THE SEMANTIC EXEMPTIONS, one per verdict, each a PREDICATE over the
    # colliding glyphs rather than a literal set. A literal set would pin
    # THIS FIXTURE's digits (`2` and `4` collide only because there is a
    # channel 2 and a count of 2) and would say nothing about the mechanism.
    # DATAVIZ: "Exemptions are SEMANTIC, and they must be claimed AND used."
    FLOW_DECLARED = {
        # a span's ends are CHROME: they bound every span in both tones, and
        # what measures is the span's LENGTH plus the figure standing on it.
        "dimension": lambda ch: ch in "├┤" or ch.isdigit(),
        # the channel index and its count are both STATED VALUES, walled
        # apart by brackets that never appear around a count.
        "lcd": lambda ch: ch.isdigit(),
        # the flap board's digits ARE the datum (law 5). The tone only
        # repeats what `00` against `02` already says.
        "odometer": lambda ch: ch.isdigit(),
    }
    # `ember` states its quantity as a FIELD BEING CONSUMED on one row: the
    # frontier between fire and ash is the whole datum, and a second row would
    # have to carry buckets the mechanism does not have. Declared here rather
    # than left to pass quietly, which is what this set is for.
    FLOW_NO_ROW = {"hairline", "ember"}
    # the two rows that draw ONE CELL PER BUCKET off a level ramp — pass
    # 63's band seats B and C. The other rows either state figures or draw
    # multi-cell buckets, where "one glyph is one bucket" is not the grammar.
    FLOW_RAMPED = {"braille", "step"}

    check("flow: every mechanism in METERS is censused on row 1",
          set(MECHS) == set(LG.METERS) and len(MECHS) == 13,
          f"{len(MECHS)} mechanisms")
    _n_excl = _n_incl = 0
    for m in MECHS:
        k = host(m)
        r = flow_markup(k)
        check(f"flow[{m}]: the mechanism draws a second row, or DECLARES "
              f"that it spends it",
              (r is None) == (m in FLOW_NO_ROW),
              "no second row" if r is None else f"|{grey(r)}|")
        if r is None:
            continue
        excl, incl = flow_collisions(r, False), flow_collisions(r, True)
        _n_excl += bool(excl)
        _n_incl += bool(incl)
        # THE CENSUS, two-directional: red if a defect appears, red if an
        # exemption is claimed and NOT USED (pass 61's shape, pass 62's
        # pattern — the maintainer who widens the list takes reds for the
        # widening itself).
        check(f"flow[{m}]: a drawn mark under two tones is DECLARED or it is "
              f"absent (letters and figures KEPT — the reading item #43's "
              f"four cases come from)",
              bool(incl) == (m in FLOW_DECLARED),
              f"{''.join(sorted(incl)) or '-'}")
        if m in FLOW_DECLARED:
            pred = FLOW_DECLARED[m]
            check(f"flow[{m}]: ... and EVERY colliding glyph fits the "
                  f"declared class — a semantic exemption, not a glyph list",
                  all(pred(ch) for ch in incl),
                  f"{''.join(sorted(incl))}")
        # AND THE SHIPPED READING, pinned beside it. The difference between
        # the two instruments is now a measured fact rather than a silent
        # choice: `excl` is blind to a level mark that is a LETTER.
        check(f"flow[{m}]: the letters-and-figures cut CHANGES the reading "
              f"here, or it does not — pinned either way",
              (excl == incl) == (m not in FLOW_DECLARED),
              f"excl={''.join(sorted(excl)) or '-'}  "
              f"incl={''.join(sorted(incl)) or '-'}")
        # THE RAMP-SCAN: the reader's position stated as a number. A row with
        # more of its OWN ramp marks than it has buckets carries a phantom
        # datum — the same family of defect as `gradient`'s phantom shoulder.
        ramp = flow_ramp(k)
        check(f"flow[{m}]: the row draws one cell per bucket off a level "
              f"ramp, or it DECLARES another grammar",
              (ramp is not None) == (m in FLOW_RAMPED),
              f"{''.join(ramp) if ramp else '-'}")
        if ramp:
            for _cs in ([4, 0, 2, 2], [0, 0, 0, 0], [1, 1, 1, 1], [9, 1, 0]):
                _r = flow_markup(k, counts=_cs)
                _n = sum(1 for ch in grey(_r) if ch in ramp)
                check(f"flow[{m}]: RAMP-SCAN at {_cs} — the colour-stripped "
                      f"row carries EXACTLY one ramp mark per bucket (a "
                      f"phantom datum reads as data)",
                      _n == len(_cs), f"{_n} marks for {len(_cs)} buckets")
            check(f"flow[{m}]: ... and its ramp is disjoint from its own "
                  f"CAPTION, which is what makes the scan exact",
                  not (set(ramp) & set(flow_caption(k))),
                  f"ramp={''.join(ramp)}  caption={flow_caption(k)!r}")
            # the pass-61/63 ceilings, on the flow row's ramp specifically
            _fd = [bink(g) for g in ramp]
            check(f"flow[{m}]: its ramp is MONOTONE in ink and its unlit "
                  f"spends at most a QUARTER of the cell",
                  all(a <= b for a, b in zip(_fd, _fd[1:]))
                  and _fd[0] <= TRACK_MAX,
                  " ".join(f"{d:.3f}" for d in _fd))
    check("flow: the two readings of the instrument disagree by EXACTLY the "
          "three declared mechanisms — #43's 'four cases' were one under the "
          "instrument the item cited",
          (_n_excl, _n_incl) == (1, 3), f"excl={_n_excl}  incl={_n_incl}")

    # -- THE FOUR VERDICTS, asserted BY NAME rather than by census ---------
    # A census can be widened by hand; a named law about a named mechanism
    # cannot be retired without deleting a sentence somebody has to defend.
    _dim = flow_markup(host("dimension"))
    check("flow: THE DIMENSION VERDICT — `├┤` are CHROME. Every span in the "
          "row is bounded by them in BOTH tones, and what carries the "
          "quantity is the span's LENGTH",
          len({len(t) for _, t in tone_runs(_dim)
               if "├" in t}) > 1
          and all(("├" in t and "┤" in t) or "├" not in t
                  for _, t in tone_runs(_dim)),
          f"|{grey(_dim)}|")
    check("flow: ... and the span STATES its value too (law 5), so the "
          "reading never rides on estimating a length",
          all(f"{x:02d}" in grey(_dim) for x in (0, 2)), f"|{grey(_dim)}|")
    _lcd = flow_markup(host("lcd"))
    check("flow: THE LCD VERDICT — every colliding glyph is a FIGURE, and "
          "the channel index is WALLED by brackets that never appear around "
          "a count",
          all(ch.isdigit() for ch in flow_collisions(_lcd, True))
          and grey(_lcd).count("[") == grey(_lcd).count("]") == 4
          and all(f"[{i}]" in grey(_lcd) for i in (1, 2, 3, 4)),
          f"|{grey(_lcd)}|")
    _odo = flow_markup(LG.kit("solari"))
    check("flow: THE ODOMETER VERDICT — the digits ARE the datum (law 5), "
          "so the tone only repeats what `00` against `02` already says",
          all(ch.isdigit() for ch in flow_collisions(_odo, True))
          and "00" in grey(_odo) and "02" in grey(_odo),
          f"|{grey(_odo)}|")
    # THE ONE DEFECT, and its cure asserted where a revert would show.
    # `or ()` on every read: a mutant that collapses the ramp to two distinct
    # glyphs makes the reader return None, and `set(None)` RAISED — the run
    # died at 7671 checks with nine reds already printed (pass 64's M6). A
    # law that cannot report its own failure is not a law; third instance
    # this pass, all three found by the battery rather than by review.
    _kd = LG.kit("darkside")
    _stp = flow_markup(_kd)
    _kdr = flow_ramp(_kd) or ()
    check("flow: THE STEP VERDICT — a LEVEL MARK collided with PROSE. This "
          "row's levels were `. o O` and its own caption is the word "
          "`flow`: five ramp marks for four buckets, colour-stripped",
          bool(_kdr) and not flow_collisions(_stp, True)
          and not (set(_kdr) & set("flow")),
          f"|{grey(_stp)}|  ramp={''.join(_kdr) or '(unreadable)'}")
    # THE CURE IS STRUCTURAL, NOT A WORD CHOICE. Renaming the caption would
    # have cured THIS caption; a ramp with no letter in it cannot collide
    # with ANY caption this row could ever carry.
    check("flow: ... and the cure is STRUCTURAL — not one level of step's "
          "ramp is a letter, so no caption this row could carry can collide "
          "with its data (a caption rename would have cured only `flow`)",
          bool(_kdr) and not any(ch.isalnum() for ch in _kdr),
          f"{''.join(_kdr) or '(unreadable)'}")
    # AND IT IS THE LANGUAGE'S OWN DECLARED DATA RAMP, not a new alphabet.
    # `. o O` is darkside's MOTION family (`SPIN`, the `PHASES` doodle); the
    # registry names `▁▂▄█` as its COVERAGE ramp and its `spark` draws it.
    check("flow: ... read off darkside's DECLARED coverage ramp — the row "
          "had a PRIVATE alphabet, and that was the defect under the "
          "collision",
          _kdr == (LG.COVER_RAMPS["step"][0], LG.COVER_RAMPS["step"][2],
                   LG.COVER_RAMPS["step"][3])
          and _kd.cover_ramp() == LG.COVER_RAMPS["step"],
          f"{''.join(_kdr) or '(unreadable)'} off "
          f"{LG.COVER_RAMPS['step']!r}")
    check("flow: ... and `. o O` stays where it belongs — darkside's "
          "SPINNER and its doodle are motion and identity, never data",
          LG.KITS["darkside"].SPIN == (".", "o", "O", "o")
          and "(o)" in LG.KITS["darkside"].PHASES)
    # PASS 61'S UNLIT RULE, VERBATIM, one mechanism later: the unlit glyph is
    # the mark the language ALREADY DRAWS for an empty position on its own
    # meter — and the bar one row above draws exactly this.
    check("flow: step's unlit is the mark its own BAR row draws for an "
          "unrun cell (pass 61's rule, applied to the second row)",
          bool(_kdr) and _kdr[0] == LG.COVER_RAMPS["step"][0]
          and _kdr[0] in grey(_kd.meter(0, 8, CS, 44).split("\n")[0]),
          f"{(_kdr or ['(unreadable)'])[0]!r}")
    # THE CURE THIS PASS REFUSED, recorded as a law so the refusal survives.
    # `◦` moved ONE level and was the smaller diff — and it is `NA.OFF`,
    # naught's own unlit pixel, which no other language's board may draw.
    # Weakening THAT law to fit this cure is the exact move pass 62's M3
    # mutant exists to catch, one level up.
    check("flow: the ONE-LEVEL cure was refused on a law, not on taste — "
          "`◦` is `NA.OFF`, and naught's pixel pair is exclusive to naught "
          "on the board",
          LG.NA.OFF == "◦"
          and "◦" not in "".join(_kdr)
          and "◦" not in grey(_kd.meter(3, 8, CS, 44)))

    # -- #44: THE BRAILLE COUPLING, TURNED THE RIGHT WAY ROUND -------------
    # The registry row is the DEFINITION; pass 61 chose its unlit by looking
    # at this meter and recorded that in a comment, which left two literals
    # tied by prose and free to drift in either direction. The value law
    # above is kept — it is the stronger guard — and this is the naming.
    _bsrc = inspect.getsource(LG._meter_braille)
    # the second offset is measured INSIDE the first slice, exactly as the
    # chained `.index` calls did — the `return` this looks for is the one
    # after `flow = `, not the first one in the file
    _bi = at(_bsrc, "    flow = ")
    _bflow = _bsrc[_bi:] if _bi >= 0 else ""
    _bj = at(_bflow, "\n    return")
    _bflow = _bflow[:_bj] if _bj >= 0 else ""
    check("#44: `_meter_braille`'s flow row NAMES the registry row's two "
          "ends instead of spelling them — and #45 moved WHERE it names "
          "them from: `cover_ramp()`, the one seat, not the row",
          "k.cover_ramp()" in _bsrc
          and "ramp[0]" in _bflow and "ramp[3]" in _bflow,
          f"{_bflow.strip()!r}")
    check("#44: ... and the flow statement spells NO braille glyph except "
          "its own middle level — a 3-level row on a 4-level ramp is not a "
          "copy of it",
          {ch for ch in _bflow if 0x2800 <= ord(ch) <= 0x28FF} == {"⠶"},
          f"{sorted(ch for ch in _bflow if 0x2800 <= ord(ch) <= 0x28FF)}")
    # AND THE CLAIM IS EXACTLY AS WIDE AS THE CURE. It was FOUR seats at pass
    # 64 (the registry, `Instrument.BLANK`, its `radio.main` and `plot`'s
    # `off=`); #40d cured `plot`'s, so it is THREE — the registry that defines
    # it and the KIT's own vocabulary, which is not this family. The count is
    # the law: a seat re-appearing anywhere reds, and so does the meter
    # spelling it again, IN A COMMENT INCLUDED (this pass wrote the two-unlit
    # argument in dot NUMBERS for exactly that reason — the fix for a red is
    # never to narrow the law that found it).
    _dots = [(p.name, i)
             for p in sorted(Path(LG.__file__).resolve().parent.glob("*.py"))
             for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(),
                                    1) if "⠐" in ln]
    _blines, _bfirst = inspect.getsourcelines(LG._meter_braille)
    _brange = range(_bfirst, _bfirst + len(_blines))
    check("#44: the METER no longer spells the registry's unlit — and the "
          "claim goes exactly that far: TWO other seats still do "
          "(`Instrument.BLANK`, its `radio.main`) and they are the KIT's "
          "vocabulary, not this family. `plot`'s `off=` left at #40d",
          len(_dots) == 3
          and not any(f == "language.py" and i in _brange for f, i in _dots),
          f"{[f'{f}:{i}' for f, i in _dots]}  meter={_brange.start}-"
          f"{_brange.stop - 1}")

    # -- THE TWO-UNLIT VERDICT: DECLARED, and the argument is an identity ---
    # `_meter_braille` draws one unlit on its BAR row and another on its FLOW
    # row, one row apart. That is the #45 disease's shape and it is not the
    # disease: the two rows are two RESOLUTIONS of one idiom. The bar is a
    # HALF-CELL fill — `⣿` fills both sub-columns of a cell, `⡇` only the
    # left — so it addresses two sub-columns per cell, and a track that inks
    # one of them leaves the other drawing nothing at the scale the bar fills.
    # The flow row draws one bucket per cell, undivided, so one dot is its
    # empty. Written as an IDENTITY rather than as prose, because prose is
    # what tied the registry to this meter for three passes (#44).
    _LCOL = 0b01000111          # braille dots 1,2,3,7 — the left sub-column
    _RCOL = 0b10111000          # braille dots 4,5,6,8 — the right sub-column
    _MIR = {0: 3, 1: 4, 2: 5, 6: 7}     # dot 1<->4, 2<->5, 3<->6, 7<->8

    def _mirror(ch):
        """The same dots, moved to the other sub-column."""
        b, out = ord(ch) - 0x2800, 0
        for _a, _c in _MIR.items():
            if b & (1 << _a):
                out |= 1 << _c
            if b & (1 << _c):
                out |= 1 << _a
        return chr(0x2800 + out)

    _ki = LG.kit("instrument")
    _bar0 = grey(_ki.meter(0, 8, [0, 0, 0], 44).split("\n")[0])
    _btrack = sorted({ch for ch in _bar0 if 0x2800 <= ord(ch) <= 0x28FF})
    _funlit = _ki.cover_ramp()[0]
    # SENTINEL " " FOR THE BAR'S UNLIT, and the FIRST draft of it was "",
    # which would have moved the crash rather than cured it: `mink("")` calls
    # `ord("")` and raises TypeError. A sentinel has to be TOTAL for every
    # function the site hands it to, and that is the per-site argument this
    # class needs and the `.index` class did not.
    #
    # A space is total (`ord` and `mink` both take it), it is NOT a braille
    # glyph so both identity laws below go red on it, and `mink(" ")` is 0.0
    # so the "ink at all" ceiling reds too — each printing `bar=' '`, which
    # is the emptiness, named. The laws keep their own `len(_btrack) == 1`
    # legs: those are what SAY the row draws exactly one glyph, and a seat
    # that cannot raise is not the same thing as a law that goes red.
    _bunlit = nth(_btrack, 0, " ")
    check("two-unlit: the bar row at 0% draws exactly ONE braille glyph, and "
          "it is not the flow row's unlit (the observation, restated as the "
          "measurement that produced it)",
          len(_btrack) == 1 and _bunlit != _funlit,
          f"bar={_btrack} flow={_funlit!r}")
    check("two-unlit: DECLARED — the bar's unlit IS the flow row's unlit "
          "mirrored into the other sub-column, so it is one idiom at two "
          "RESOLUTIONS and not two vocabularies",
          _bunlit == chr(0x2800 + ((ord(_funlit) - 0x2800)
                                   | (ord(_mirror(_funlit)) - 0x2800))),
          f"{_funlit!r} | mirror = {_bunlit!r}")
    # -- #46: THE HALF CELL'S TRACK DOT, and the glyph is COMPOSED ---------
    # The two-unlit verdict's rule is that a half-cell fill inks every
    # ADDRESSABLE sub-column. Its own half cell used to ink none of the
    # right one — the sixty-fifth pass declared the rule and filed the
    # defect in the same paragraph. The cure is not a nicer glyph: it is the
    # rule APPLIED, so the law spells the composition and never the answer.
    _bhalf = LG.kit("instrument").HALF
    _bfull, _blatt = LG.kit("instrument").FULL, LG.kit("instrument").LATT
    check("two-unlit: ... and the resolution claim is true of the FILL, not "
          "asserted about it — the bar's lit marks address TWO sub-columns "
          "per cell (a full cell, and a half cell that fills the left one "
          "and TRACKS the right)",
          bin((0x28FF - 0x2800) & _LCOL).count("1") == 4
          and bin((0x28FF - 0x2800) & _RCOL).count("1") == 4
          and _bhalf in _ki.meter(1, 68, [0], 44)     # an ODD dot count
          and bin((ord(_bhalf) - 0x2800) & _LCOL).count("1") == 4
          and bin((ord(_bhalf) - 0x2800) & _RCOL).count("1") > 0,
          f"half={_bhalf!r}")
    check("#46: THE HALF CELL IS COMPOSED, NOT CHOSEN — the full cell's LEFT "
          "sub-column OR the track's RIGHT one, which is the two-unlit "
          "rule applied to the one cell it had not reached. Written as the "
          "composition rather than as the glyph: a law that compares a "
          "literal to itself is a spelling, and the sixty-fifth pass filed "
          "this defect in the same paragraph that declared the rule it "
          "violates",
          ord(_bhalf) - 0x2800 == (((ord(_bfull) - 0x2800) & _LCOL)
                                   | ((ord(_blatt) - 0x2800) & _RCOL)),
          f"{_bfull!r} left | {_blatt!r} right = {_bhalf!r}")
    check("#46: THE CONTROL — the composition REFUSES the glyph that "
          "shipped for sixty-seven passes, so the law can go red. `⡇` is "
          "the same left sub-column with nothing in the right one, which is "
          "the one cell in the whole bar whose empty half drew nothing",
          _bhalf != "⡇"
          and ord("⡇") - 0x2800 != (((ord(_bfull) - 0x2800) & _LCOL)
                                    | ((ord(_blatt) - 0x2800) & _RCOL))
          and bin((ord("⡇") - 0x2800) & _RCOL).count("1") == 0)
    # THE CENSUS, BOTH DIRECTIONS (the sixty-seventh pass's discipline). A
    # cure applied at one of three sites is a cure that drifts, and a census
    # that flags every `⡇` in the file is a detector that cannot read what
    # it is looking at: this glyph is a half-cell FILL in three places and a
    # MARK in four, and the identity is only a rule about the first kind.
    _half_fills = [
        ("_meter_braille bar", LG.kit("instrument").meter(1, 68, [0], 44)),
        ("Instrument._flow_card_rows",
         LG.kit("instrument")._flow_card_rows(
             "T", "9d", LG.kit("instrument")["mut"], 34, 0, False,
             {"phase_idx": 0, "n_phases": 4, "days": 9})[1]),
        ("Instrument.trace_row", LG.kit("instrument").trace_row(
            34, {"days": 0})),
    ]
    check("#46 census: ALL THREE HALF-CELL FILL SITES draw the cured glyph "
          "and none draws the old one — the meter mechanism, the bench "
          "readout and the scope trace. Three copies of one literal is the "
          "#45 shape at one-third strength; two of them now read the "
          "`Instrument.HALF` seat and the third is a module-level MECHANISM "
          "that this language does not own, which is why it is a law here "
          "rather than a fourth reader",
          all(_bhalf in grey(s) and "⡇" not in grey(s)
              for _n, s in _half_fills),
          f"{[(n, _bhalf in grey(s), '⡇' in grey(s)) for n, s in _half_fills]}")
    # THE EXEMPTIONS, CLAIMED AND USED. Each is a `⡇` this pass did NOT
    # touch, with the reason it is not a half-cell fill — and each is
    # ASSERTED to still be there, so an exemption cannot quietly become a
    # site nobody checks.
    _exempt = {
        # a MARK on a track, not a fill of it: the sub-column carries the
        # knob's STATE (left/right is DEFAULT/FOCUSED), not a quantity, so
        # inking the other one would collapse the pair into one glyph
        "instrument slider knob":
            LG.kit("instrument").PART_GLYPHS["knob"][LG.DEFAULT],
        # a CARET: one cell, no track behind it, nothing unrun to ink
        "instrument textfield caret":
            LG.kit("instrument").PART_GLYPHS["textfield.caret"][LG.DEFAULT],
        # a gantt TODAY LINE — a rule, the `│` every other language draws
        "instrument gantt rule": LG.kit("instrument").GANTT[2],
        # a stepper's ARROW PAIR — `⡇⢸` point at each other across the word.
        # The sub-column IS the direction; a track dot in the other one makes
        # both arrows point both ways
        "instrument stepper.step EDITED":
            LG.kit("instrument").PART_GLYPHS["stepper.step"][LG.EDITED][0],
        # naught's FINE is a four-level HEIGHT ramp in the left sub-column;
        # `⡇` is its TOP level, not a half of anything. A right-column dot
        # would make the ramp non-monotone in ink and change its alphabet
        "naught FINE top": LG.NA.FINE[3],
    }
    check("#46 census, THE OTHER DIRECTION: FIVE `⡇` seats are NOT half-cell "
          "fills and keep the glyph — a knob whose sub-column is STATE, a "
          "caret with no track behind it, a gantt today-LINE, a stepper "
          "ARROW whose sub-column is DIRECTION, and naught's FINE ramp where "
          "it is the TOP of four heights. Claimed AND used: each is read off "
          "the shipped seat, so an exemption cannot decay into a site nobody "
          "looks at. (The first draft of this list had FOUR — the stepper "
          "arrow was missed, and a census that undercounts its own "
          "exemptions is the detector failing to read the file)",
          all(v == "⡇" for v in _exempt.values()) and len(_exempt) == 5,
          f"{ {k: v for k, v in _exempt.items() if v != '⡇'} }")
    # AND THE COUNT IS CLOSED AGAINST THE SOURCE, not just listed. Every `⡇`
    # left in the language module is either one of the five exempt seats or a
    # comment about the cure — a sixth live one means a fill site this pass
    # did not find.
    _live = [i for i, ln in enumerate(
        Path(LG.__file__).read_text(encoding="utf-8").splitlines(), 1)
        if "⡇" in ln and not ln.lstrip().startswith("#")]
    check("#46 census: ... and the list is CLOSED against the source — every "
          "`⡇` still in `language.py` outside a comment is one of the five "
          "claimed seats. A sixth would be a half-cell fill this pass never "
          "found, which is the failure mode the three-site census exists to "
          "make impossible",
          len(_live) == 4,      # 4 LINES carry the 5 seats (stepper pairs)
          f"{len(_live)} line(s): {_live}")
    check("#46: and the RENDER GRID COULD NOT HAVE CAUGHT THIS — pass 62's "
          "428 fixture strings contain no odd dot count for the braille "
          "bar, so all five instrument meter fixtures draw whole cells and "
          "the grid is `cmp`-clean across a cure that moves every half cell "
          "in the language. A detector reporting zero because it did not "
          "look is the same failure as a law that cannot go red, and this "
          "pass had it happen to its own diff",
          not any(_bhalf in grey(LG.kit("instrument").meter(d, t, cs, w))
                  or "⡇" in grey(LG.kit("instrument").meter(d, t, cs, w))
                  for d, t, cs, w in ((3, 8, [4, 0, 2, 2], 44),
                                      (0, 8, [0, 0, 0, 0], 44),
                                      (8, 8, [1, 1, 1, 1], 44),
                                      (1, 99, [0, 1, 0], 30),
                                      (0, 0, [], 24))))
    check("two-unlit: both unlits clear law 4's two ceilings — ink at all, "
          "and at most a QUARTER of the cell",
          0 < mink(_bunlit) <= 0.25 and 0 < mink(_funlit) <= 0.25,
          f"bar={mink(_bunlit):.3f} flow={mink(_funlit):.3f}")
    # THE CONTROL: the identity is not true of just any braille pair, which
    # is what makes it an argument rather than a coincidence.
    check("two-unlit: the mirror identity FAILS for a different unlit (the "
          "predicate can go red)",
          len(_btrack) == 1
          and chr(0x2800 + ((ord("⠁") - 0x2800)
                            | (ord(_mirror("⠁")) - 0x2800))) != _bunlit,
          f"bar={_bunlit!r}")

    print("\n== KIT LEVEL: naught re-grounded in Nothing (round · red-rationed)")
    import unicodedata as U
    check("naught: the pixel pair is ROUND and measured width-safe (EAW N)",
          LG.NA.ON == "∙" and LG.NA.OFF == "◦"
          and U.east_asian_width(LG.NA.ON) == "N"
          and U.east_asian_width(LG.NA.OFF) == "N")
    kn = LG.kit("naught")
    red = TH.THEMES["naught"]["accent"]
    calm_meta = {"proj": "Web", "phase": "Doing", "phase_idx": 1, "n_phases": 4,
                 "days": 9, "prio": "normal", "blocked": False, "done": False}
    calm_surface = "\n".join([
        kn.head("BACKLOG", 5, 20, 0),
        "\n".join(kn.card_rows("Steady work", "9d", kn["mut"], 28, 0, False,
                               calm_meta)),
        kn.tile_row("  4", "work in flight", kn["ink"], 20),
        kn.meter(3, 8, [4, 0, 2, 2], 44),
        kn.bar(9, None, None),
        "\n".join(kn.sect("AGENDA", "12 open", 50, 20)),
        kn.cal_cell("none") + kn.cal_cell("one") + kn.cal_cell("multi"),
        kn.switch(True) + kn.switch(False),
        kn.slider(4, 0, 10, 10),
        "".join(kn.spinner(t) for t in range(4)),
        kn.tabs(["board", "lanes"], "board"),
        "\n".join(kn.wordmark("AB")),
        "\n".join(kn.face("clear")), "\n".join(kn.face("busy")),
        "|".join(kn.flip_frames(True)),
        kn.spark([1, 3, 2, 5], 4),
        "\n".join(kn.plot([2, 5, 3, 7], 16, 4)),
        kn.gauge(4, 0, 10, 10, thr=8),
    ])
    check("naught: a CALM surface carries ZERO red (the Nothing ration)",
          red not in calm_surface)
    check("naught: alarm still bleeds red (urgent card, overdue day)",
          red in kn.card_row("Fix it", "2d!", kn["alert"], 28, 0, True)
          and red in kn.cal_cell("over"))
    faces = {m: "\n".join(grey(r) for r in kn.face(m))
             for m in ("clear", "busy", "alert")}
    check("naught: the face READS state (3 moods, 3 expressions)",
          len(set(faces.values())) == 3)
    check("naught: the face is GROUNDED on the unlit lattice",
          all("◦" in f for f in faces.values()))
    kn.mood = "alert"
    check("naught: mascot follows the board mood",
          "\n".join(grey(r) for r in kn.mascot()) == faces["alert"])
    # TWO DOT SCALES (Nothing mixes them): structure on the large lattice
    # (∙/◦), data on fine sub-cell dots (braille column, still round)
    sp = grey(kn.spark([1, 3, 2, 5], 4))
    check("naught: data wears the FINE dot scale (sub-cell, round)",
          any(g in sp for g in LG.NA.FINE[1:]))
    check("naught: structure keeps the LARGE lattice (plot columns)",
          LG.NA.ON in "\n".join(grey(r) for r in kn.plot([2, 5], 8, 4)))
    check("naught: the two scales are different pixels",
          not any(g in sp for g in (LG.NA.ON, LG.NA.OFF)))

    print("\n== KIT LEVEL: naught's LATTICE composition (the `layout` token)")
    # naught's identity IS the round-dot lattice, and until this pass the
    # board composition was hardcoded in the class — the exact defect
    # PENDING item 0 names (a mechanism the token does not own is a mechanism
    # the language only appears to have chosen).
    OFF, ON = LG.NA.OFF, LG.NA.ON
    check("naught declares the token it renders (layout=lattice)",
          TH.THEMES["naught"].get("layout") == "lattice" and kn.lattice)
    lat_head = grey(kn.head("BACKLOG", 5, 20, 0))
    lat_card = [grey(r) for r in kn.card_rows("Shut down legacy servers", "8d",
                                              kn["mut"], 40, 0, False, META_A)]
    # THE SIGNATURE, asserted as three separate commitments — "there are some
    # dots" would pass on the meter alone and prove nothing about composition
    check("naught: the head's count is a DRAWN sprite on the lattice (5 rows)",
          lat_head.count("\n") + 1 >= LG.NA.ALPHA_ROWS + 1 and OFF in lat_head,
          f"{lat_head.count(chr(10)) + 1} rows")
    check("naught: the card's gap is closed by dot LEADERS, not blank cells",
          OFF * 2 in lat_card[0])
    check("naught: the card's second row rides the lattice (lit + unlit)",
          ON in lat_card[1] and OFF in lat_card[1])
    check("naught: the lattice is DENSE — gap=0, the dots are adjacent",
          TH.THEMES["naught"]["gap"] == 0 and OFF * 2 in lat_head)
    # DISPATCH: the composition follows the token, not the class name — the
    # same law the rail and the ruling are already held to
    for name in TH.ORDER:
        k = LG.kit(name)
        rows = (k.card_rows("Shut down legacy servers", "8d", k["mut"], 40, 0,
                            False, META_A) + [k.head("BACKLOG", 5, 40, 0)])
        check(f"{name}: the board rides the dot lattice IFF layout=lattice",
              any(OFF in grey(r) for r in rows)
              == (TH.THEMES[name].get("layout") == "lattice"))
    # DEGRADE: back to the base default and the composition must go. What the
    # token owns is the BOARD's composition; the dots that carry QUANTITY
    # (the dotgrid meter) answer to `meter` and are asserted to STAY.
    old_layout = TH.THEMES["naught"]["layout"]
    TH.THEMES["naught"]["layout"] = "flow"
    try:
        kfl = LG.kit("naught")
        fl_head = grey(kfl.head("BACKLOG", 5, 20, 0))
        fl_card = [grey(r) for r in kfl.card_rows("Shut down legacy servers",
                                                  "8d", kfl["mut"], 40, 0,
                                                  False, META_A)]
        fl_meter = grey(kfl.meter(3, 8, [4, 0, 2, 2], 44))
    finally:
        TH.THEMES["naught"]["layout"] = old_layout
    check("naught.layout=flow drops the drawn count sprite (head is 1 row)",
          fl_head.count("\n") + 1 < LG.NA.ALPHA_ROWS,
          f"{fl_head.count(chr(10)) + 1} rows")
    check("naught.layout=flow leaves the lattice (no unlit dots on the card)",
          not any(OFF in r for r in fl_card))
    check("naught.layout=flow still renders the board — it degrades, not dies",
          "BACKLOG" in fl_head and "Shut down legacy servers" in fl_card[0])
    check("naught.layout=flow keeps the METER's dots (they answer to `meter`)",
          OFF in fl_meter and ON in fl_meter)
    check("naught: the lattice composition is restored after the mutation",
          grey(kn.head("BACKLOG", 5, 20, 0)) == lat_head)

    print("\n== DRAW LEVEL: naught's DENSE display type (the `naught7` base)")
    # User verdict 2026-07-27: "the pixels of the larger letters should be a
    # bit denser — I find them hard to read, they're somewhat separated". The
    # old drawn caption put BLANK cells between letters and drew one cell per
    # pixel, so every stroke was a single cell. The cure is a declared BASE,
    # so it has to be dispatched and disprovable — a token no renderer reads
    # is PENDING item 0's exact defect.
    def hero_rows(w, h, name="naught", cap="DAYS OVERDUE", val="12",
                  det="backlog - 3 open"):
        k = LG.kit(name)
        return HE.draw(k, val, cap, det, k.t.get("calm", k["ink"]),
                       w, h).split("\n")

    def dot_band(rows):
        """The GLYPH FIELD: the rows made of lattice dots. The typographic
        caption and the detail line are cell text, not part of the field."""
        return [r for r in (grey(x) for x in rows) if ON in r or OFF in r]

    THIN = re.compile(f"(?<!{ON}){ON}(?!{ON})")     # a one-cell lit stroke
    band = dot_band(hero_rows(118, 20))
    check("naught declares the base it renders (hero=naught7)",
          TH.THEMES["naught"]["hero"] == "naught7")
    check("naught7: the numeral stands 7 rows where the budget allows",
          len(dot_band(hero_rows(118, 12))) >= 7,
          f"{len(dot_band(hero_rows(118, 12)))} rows at h=12")
    check("naught7: the glyph field carries NO plain cell (the DENSITY law)",
          bool(band) and all(" " not in r for r in band), f"{len(band)} rows")
    check("naught7: every cell is a ROUND dot, lit or unlit (EAW-Neutral)",
          set("".join(band)) == {ON, OFF})
    check("naught7: no stroke is one cell wide (what 'separated' meant)",
          not THIN.search("\n".join(band)))
    check("naught7: the caption is DRAWN on the same field (numeral + band)",
          len(band) >= 7 + 1 + LG.NA.ALPHA_ROWS, f"{len(band)} rows")
    check("naught7: the band separator is an UNLIT lattice row, not a blank",
          any(set(r) == {OFF} for r in band))
    # the mechanism, stated against the form it replaced: the narrow label
    # draws one cell per pixel and separates letters with blank cells
    thin_rows = [grey(r) for r in LG.NA.label("A", "#fff", "#111",
                                              dot_w=1, gap=0)]
    check("naught7: the form it replaced DID have one-cell strokes (control)",
          bool(THIN.search("\n".join(thin_rows))))
    check("naught7: a letter is twice the cells it was (x2 horizontal pixel)",
          len(grey(HE.dense_type("A", "#fff", "#111", 40)[0]).replace(" ", ""))
          >= 2 * len(thin_rows[0]))

    # PROGRESSIVE: a band costs 6 rows; where they do not fit the caption is
    # typographic and NOTHING wraps (the aperture's row budget, hero <= 12)
    small = hero_rows(46, 12)
    check("naught7: a short surface falls back to typographic type",
          len(dot_band(small)) == 7 and "DAYS OVERDUE" in "\n".join(small))
    check("naught7: the fallback keeps the surface inside its budget",
          len(small) <= 12 and max(len(grey(r)) for r in small) <= 46)
    # ALL OR NOTHING: at 92 cells the caption wraps to two bands at pixel x2;
    # drawing only the first would silently print "DAYS", a different fact —
    # so the tier drops to x1, which fits the whole caption on one band
    mid = hero_rows(92, 16)
    check("naught7: a caption that cannot be fully drawn is not half-drawn",
          len(dot_band(mid)) == 9 + 1 + LG.NA.ALPHA_ROWS,
          f"{len(dot_band(mid))} rows")
    check("naught7: the x1 tier draws where x2 will not fit (progressive)",
          len(dot_band(hero_rows(54, 13))) == 7 + 1 + LG.NA.ALPHA_ROWS)
    check("naught7: the x1 tier still stands on the lattice (no plain cell)",
          all(" " not in r for r in dot_band(hero_rows(54, 13))))
    # THE REACHABILITY FACT, recorded so it cannot rot silently: a drawn band
    # costs 6 rows on top of the 7-row numeral, and every composition gives
    # naught's hero 7 (board) or 11 (widget) CONTENT rows. So no seat in the
    # app reaches the drawn caption today — it is renounced to type, and that
    # renunciation is the honest answer, not a bug. Raising it needs the hero's
    # row budget (widget.tcss / language.composition), outside this file set.
    check("naught7: at the app's real hero budget the caption is TYPE, "
          "not a clipped band (11 content rows < 7 + 6)",
          len(dot_band(hero_rows(54, 11))) == 7
          and "DAYS OVERDUE" in "\n".join(hero_rows(54, 11)))
    for w, h in ((46, 12), (60, 8), (92, 16), (118, 20), (118, 12)):
        rr = hero_rows(w, h)
        check(f"naught7: nothing wraps or overruns at {w}x{h}",
              len(rr) <= h and max(len(grey(r)) for r in rr) <= w)

    # LIVE TOKENS: the fill is drawn in `dim` and the numeral in the tone, so
    # a colour change must reach the markup. Colour-stripped, a recoloured
    # fill is invisible and `dim` would read as dead metadata (the rail lesson)
    raw = "\n".join(hero_rows(118, 20))
    old_dim = TH.THEMES["naught"]["dim"]
    TH.THEMES["naught"]["dim"] = "#ff00ff"
    try:
        muted = "\n".join(hero_rows(118, 20))
    finally:
        TH.THEMES["naught"]["dim"] = old_dim
    check("naught7: the unlit fill is drawn in `dim` (mutation reaches it)",
          muted != raw and "#ff00ff" in muted)
    check("naught7: the fill restores cleanly",
          "\n".join(hero_rows(118, 20)) == raw)
    check("naught7: the lit numeral wears the severity tone, not the fill",
          TH.THEMES["naught"]["alert"] in "\n".join(
              HE.draw(kn, "12", "DAYS OVERDUE", "", TH.THEMES["naught"]["alert"],
                      118, 20).split("\n")))
    check("naught7: a CALM hero carries ZERO red (the Nothing ration holds)",
          red not in raw)
    # DISPATCH: the dense type follows the token, not the class name
    old_hero = TH.THEMES["naught"]["hero"]
    TH.THEMES["naught"]["hero"] = "plain"
    try:
        plainly = hero_rows(118, 20)
    finally:
        TH.THEMES["naught"]["hero"] = old_hero
    check("naught.hero=plain drops the dense type (dispatch, not class name)",
          not dot_band(plainly))
    check("naught.hero=plain still renders a hero — it degrades, not dies",
          any(r.strip() for r in plainly))
    check("naught7: the dense type is restored after the mutation",
          "\n".join(hero_rows(118, 20)) == raw)
    for name in TH.ORDER:
        if name == "naught":
            continue
        check(f"{name}: its hero draws no naught fill (the base is naught's)",
              not dot_band(hero_rows(118, 20, name)))

    print("\n== DRAW LEVEL: ledger `slab` · solari `flap` · blueprint `stencil`")
    # All three languages shipped `hero="plain"`. The tokens they declare now
    # have to RENDER, and the render has to LEAVE when the token does — that is
    # PENDING item 0's law, and it is the only thing separating a display type
    # from a line in a manifest. With blueprint's stencil every language's hero
    # posture is either DRAWN or a deliberate renunciation (swiss).
    SLAB_MARK, FLAP_MARK, ST_MARK = "▄", BS.FLAP_SEAM_FACE, BS.ST_RAIL_W
    DRAWN_HERO = ("ledger", "solari", "blueprint")

    def fig_rows(name, w=76, h=9, val="12", cap="DAYS OVERDUE",
                 det="backlog - 3 open", tone=None):
        k = LG.kit(name)
        t = tone or k.t.get("calm", k["ink"])
        return HE.draw(k, val, cap, det, t, w, h).split("\n")

    def blocks(rows):
        # the rail glyphs joined this predicate with the stencil: a HOLLOW
        # figure's stem rows carry `▌▐` and no block at all, so the old filter
        # counted 5 rows of a 7-row figure and the height check would have
        # gone red for the right reason at the wrong seat
        return [r for r in (grey(x) for x in rows)
                if any(c in r for c in ("█", "▀", "▄", FLAP_MARK,
                                        BS.ST_RAIL_W, BS.ST_RAIL_E))]

    for lang, mark in (("ledger", SLAB_MARK), ("solari", FLAP_MARK),
                       ("blueprint", ST_MARK)):
        base_rows = fig_rows(lang)
        check(f"{lang}: the hero DRAWS a figure (7 rows of it), where it used "
              f"to print a typographic value",
              len(blocks(base_rows)) >= 7, f"{len(blocks(base_rows))} rows")
        check(f"{lang}: the figure carries this base's own signature mark",
              any(mark in r for r in blocks(base_rows)))
        check(f"{lang}: the caption is still there and still typographic — "
              f"declared, because a drawn caption costs rows no composition "
              f"gives (the naught precedent)",
              "DAYS OVERDUE" in "\n".join(grey(r) for r in base_rows))
        # DISPATCH on the `hero` token
        old_h = TH.THEMES[lang]["hero"]
        TH.THEMES[lang]["hero"] = "plain"
        try:
            plainly = fig_rows(lang)
        finally:
            TH.THEMES[lang]["hero"] = old_h
        check(f"{lang}.hero=plain drops the drawn figure (dispatch, not class "
              f"name)", not blocks(plainly))
        check(f"{lang}.hero=plain still renders a hero — it degrades, not dies",
              any(r.strip() for r in (grey(x) for x in plainly)))
        # ... and on the `base` token, which is where the TYPE actually lives
        old_b = TH.THEMES[lang]["base"]
        TH.THEMES[lang]["base"] = "block2"
        try:
            flat = fig_rows(lang)
        finally:
            TH.THEMES[lang]["base"] = old_b
        check(f"{lang}.base=block2 keeps a drawn figure but loses this base's "
              f"signature — `base` IS the display type, not a resolution knob",
              blocks(flat) and not any(mark in r for r in blocks(flat)))
        check(f"{lang}: the figure is restored after both mutations",
              fig_rows(lang) == base_rows)
        # SEVERITY: a calm hero spends none of the rationed hue
        raw = "\n".join(fig_rows(lang))
        for tok in ("alert", "warn", "accent"):
            hexv = TH.THEMES[lang][tok]
            # `mut` joined this skip set with blueprint, and it is DECLARED
            # rather than quietly widened: that language's near-due step is
            # BRIGHTNESS, so its `warn` IS the cyan grey the caption is set in
            # (themes.py says so). A ration check on a hue the language also
            # spends on passive type would be asserting the caption away.
            if hexv in (TH.THEMES[lang].get("calm"), TH.THEMES[lang]["ink"],
                        TH.THEMES[lang]["mut"]):
                continue
            check(f"{lang}: a CALM hero carries ZERO {tok} ({hexv}) — the "
                  f"ration holds on the new display type too",
                  hexv not in raw)
        alert = TH.THEMES[lang]["alert"]
        check(f"{lang}: the FIGURE wears the severity tone when the reading "
              f"is late (the ration is spent where it means something)",
              alert in "\n".join(fig_rows(lang, tone=alert)))
        # GEOMETRY: one width hides a whole regime (VERIFY.md)
        for w, h in ((46, 12), (54, 9), (76, 9), (92, 12), (118, 20)):
            rr = fig_rows(lang, w, h)
            check(f"{lang}: nothing wraps or overruns at {w}x{h}",
                  len(rr) <= h and max(len(grey(r)) for r in rr) <= w,
                  f"{len(rr)} rows, widest {max(len(grey(r)) for r in rr)}")
    # NO MECHANISM LEAKS. Each drawn base owns a mark no other hero may carry,
    # and the stencil's is the pair of RAILS — which is also why the hollow law
    # is stated as a vocabulary and not as a glyph: `▌` alone is reachable
    # through `quadrant`, the rails PLUS the absence of any solid block is not.
    for name in TH.ORDER:
        if name != "solari":
            check(f"{name}: its hero carries no flap hinge (the mechanism is "
                  f"solari's)",
                  FLAP_MARK not in "\n".join(grey(r) for r in fig_rows(name)))
        if name != "blueprint":
            fg = set("".join(blocks(fig_rows(name)))) - {" "}
            # the two halves are DIFFERENT claims and the message says which
            # one was made — a language that renounces drawing cannot leak the
            # cut, and passing that silently is how a vacuous check hides
            claim = ("draws a figure that is NOT hollow (a solid mark stands "
                     "in it), so the cut mechanism stays blueprint's"
                     if fg else
                     "DRAWS NO FIGURE AT ALL, so there is nothing for the cut "
                     "to leak into — the renunciation, stated")
            check(f"{name}: its hero {claim}",
                  (not fg <= set(BS.ST_HOLLOW)) if fg
                  else not blocks(fig_rows(name)),
                  f"{sorted(fg)}")

    # THE FACE IS A GROUND, and a ground is the one claim markup can carry
    # that a glyph cannot. Asserted on the markup here and on the COMPOSITED
    # frame later (capture_bg / the real aperture) — the two must agree.
    st_s = TH.THEMES["solari"]
    fl = fig_rows("solari")
    face_rows = [r for r in fl if f"on {st_s['flap']}" in r]
    seam_rows = [r for r in fl if f"on {st_s['seam']}" in r]
    # SENTINEL "<NO ROW>" for both. Every law beneath asks whether a MARKUP
    # SPAN is IN the row, so any string that cannot contain `[#rrggbb on
    # #rrggbb]` reds all four of them — and this one says WHY on the FAIL
    # line instead of leaving a bare `''` for a maintainer to interpret.
    # "" was rejected for exactly that: it reds correctly and diagnoses
    # nothing, and the DETAIL argument is evaluated on every call.
    _NOROW = "<NO ROW: the figure drew none in this tone>"
    seam0 = nth(seam_rows, 0, _NOROW)
    face0 = nth(face_rows, 0, _NOROW)
    check("solari: the flap FACE is painted as a background, on 6 of the "
          "figure's 7 rows", len(face_rows) == 6, f"{len(face_rows)} row(s)")
    check("solari: the hinge row is a BAND in the `seam` tone — exactly one "
          "row, and it is the row the base put the hinge on",
          len(seam_rows) == 1 and FLAP_MARK in seam0,
          f"{len(seam_rows)} row(s)")
    check("solari: the hinge LINE is `mut`, not `seam` — measured, because "
          "`seam` (#1f1f22) on the face (#17171a) is 1.06:1 and would be an "
          "invisible token pretending to render",
          f"[{st_s['mut']} on {st_s['seam']}]" in seam0,
          seam0[:80])
    check("solari: the numeral keeps the severity tone ON the hinge band — "
          "the hinge cuts the figure, it does not repaint it",
          f"[{st_s['calm']} on {st_s['seam']}]" in seam0)
    check("solari: the ground BETWEEN two cards is not painted (a bank of "
          "cards, not one wide card)",
          f"[{st_s['calm']}]" in face0, face0[:100])
    # ... and the face must LEAVE with the token, or `flap`/`seam` would read
    # as dead metadata on this seat
    for tok in ("flap", "seam"):
        old_v = st_s[tok]
        st_s[tok] = "#ff00ff"
        try:
            muted = "\n".join(fig_rows("solari"))
        finally:
            st_s[tok] = old_v
        check(f"solari: mutating `{tok}` reaches the drawn hero",
              "#ff00ff" in muted and old_v not in muted.replace(
                  f"[{old_v}]", ""))
    for lang, why in (("ledger", "the figure is ink on the paper ground, "
                       "which is what makes a light-ground language read as "
                       "print"),
                      ("blueprint", "a drawing sheet has one ground and the "
                       "figure is a CUT in it — a painted face would be a "
                       "containing box in background")):
        check(f"{lang}: its hero paints NO face — {why}",
              " on " not in "\n".join(fig_rows(lang)))

    # THE DIFF CANNOT REACH THE OTHER SEVEN, and that is measured rather than
    # argued. `BASE_GLYPH` and `BASE_GAP` are the only new state on the shared
    # `draw_numeral` seat; empty them and every language whose base is not
    # slab/flap/stencil must render BYTE-IDENTICALLY, while the three drawn
    # ones must move. (There was no stored hero baseline to diff against —
    # pass 35's `_sig35_post.txt` is a KIT dump — so unreachability IS the
    # evidence.)
    before = {n: "\n".join(fig_rows(n)) for n in TH.ORDER}
    og, oa = BS.BASE_GLYPH, BS.BASE_GAP
    BS.BASE_GLYPH, BS.BASE_GAP = {}, {}
    try:
        after = {n: "\n".join(fig_rows(n)) for n in TH.ORDER}
    finally:
        BS.BASE_GLYPH, BS.BASE_GAP = og, oa
    for name in TH.ORDER:
        moved = after[name] != before[name]
        check(f"{name}: the per-base font/gap state is "
              f"{'REACHED' if name in DRAWN_HERO else 'UNREACHABLE'}"
              f" from its hero (byte-identity for the seven that did not "
              f"change)",
              moved == (name in DRAWN_HERO))
    check("the unreachability probe restores the module state it borrowed",
          {n: "\n".join(fig_rows(n)) for n in TH.ORDER} == before)

    print("\n== KIT LEVEL: the column head's COUNT sprite takes the STROKE")
    # The naught7 pass built the cure and then MEASURED where the user's
    # defect actually sits: not in the hero — whose drawn caption no
    # composition's row budget reaches — but in the board's column-head count
    # sprites, which every screen shows. Same laws as the hero's, mirrored at
    # the seat that is seen, with the same negative controls.
    HEAD_W = (14, 20, 28, 40, 60)
    # x2 costs 18 cells for two digits (the metric-bearing alphabet: a digit
    # advances 5 columns, so 2 * (5 + 5 - 1) = 18) and needs w - 1. It was 14
    # while every glyph shared a 3-column box; the exact flip is asserted below.
    SX2_MIN = 19

    def head_rows(w, count=12, name="naught"):
        return [grey(r) for r in
                LG.kit(name).head("BACKLOG", count, w, 0).split("\n")]

    def head_sprite(w, count=12):
        return head_rows(w, count)[1:]

    wide = head_sprite(40)
    check("head: the count sprite is drawn at all (probe self-check)",
          len(wide) == LG.NA.ALPHA_ROWS
          and all(ON in r or OFF in r for r in wide), f"{len(wide)} rows")
    check("head: no stroke is one cell wide where the column pays for x2 "
          "(the user's own words, at the seat they read)",
          not THIN.search("\n".join(wide)))
    check("head: the sprite field carries NO plain cell — letters are parted "
          "by unlit dots, not by void",
          all(" " not in r for r in wide))
    check("head: every cell is a ROUND dot, lit or unlit (EAW-Neutral)",
          set("".join(wide)) == {ON, OFF})
    # NEGATIVE CONTROLS: the form this replaces must FAIL both laws, or the
    # laws are decoration (an assert that cannot fail proves nothing)
    thin_head = [grey(r) for r in LG.NA.label("12", "#fff", "#111", 1, 0)]
    check("head: the form it replaced DID have one-cell strokes (control)",
          bool(THIN.search("\n".join(thin_head))))
    check("head: the form it replaced DID part letters with a blank (control)",
          any(" " in r for r in thin_head))
    check("head: the sprite is twice the cells it was (x2 horizontal pixel)",
          len(wide[0]) == 2 * len(thin_head[0]),
          f"{len(wide[0])} vs {len(thin_head[0])}")
    # THE WIDTH BUDGET: x2 roughly doubles the sprite, and a sprite wider than
    # its column WRAPS — which would cost the board a card row. Progressive,
    # and the head's ROW COUNT must not move at any size class.
    for w in HEAD_W:
        rows = head_rows(w)
        check(f"head fits its column at w={w} (no wrap, no truncation, "
              f"row count unchanged)",
              len(rows) == 1 + LG.NA.ALPHA_ROWS
              and max(len(r) for r in rows) <= w,
              f"{len(rows)} rows, widest {max(len(r) for r in rows)}")
        check(f"head: plain_width predicts the drawn width at w={w}",
              len(rows[1]) == LG.NA.plain_width(
                  "12", 1, 0, 2 if w >= SX2_MIN else 1, True))
    check("head: the x1 fallback ENGAGES where x2 will not fit (w=14)",
          len(head_sprite(14)[0]) == LG.NA.plain_width("12", 1, 0, 1, True))
    check("head: the x1 fallback still stands on the continuous lattice",
          all(" " not in r and set(r) <= {ON, OFF} for r in head_sprite(14)))
    check("head: x2 is taken as soon as the column pays for it (w=20)",
          len(head_sprite(20)[0]) == LG.NA.plain_width("12", 1, 0, 2, True))
    check("head: a ONE-digit count takes the stroke too",
          not THIN.search("\n".join(head_sprite(40, 7))))
    check("head: an EMPTY column still draws its zero on the lattice",
          all(" " not in r for r in head_sprite(40, 0)))
    # the no-wrap law is not naught's alone: a head that overruns its column
    # costs any language a row, so every one of the eight is held to it
    for name in TH.ORDER:
        got = [(w, max(len(r) for r in head_rows(w, 12, name))) for w in HEAD_W]
        check(f"{name}: the column head fits its column at every size class",
              all(m <= w for w, m in got), f"{got}")
    # THE STROKE IS A PROPERTY OF THE LATTICE COMPOSITION, not of the class:
    # under the base default the generic typographic head must come back
    old_lat = TH.THEMES["naught"]["layout"]
    TH.THEMES["naught"]["layout"] = "flow"
    try:
        flow_head = grey(LG.kit("naught").head("BACKLOG", 12, 40, 0))
    finally:
        TH.THEMES["naught"]["layout"] = old_lat
    check("naught.layout=flow: the head is the generic one — no sprite, the "
          "count is cell text",
          ON not in flow_head and OFF not in flow_head and "12" in flow_head)
    check("head: the drawn sprite is restored after the mutation",
          head_sprite(40) == wide)
    # sect()'s drawn titles are the same mechanism at another seat, so they
    # take the same cure under the same progressive rule
    sect_wide = [grey(r) for r in LG.kit("naught").sect("AGENDA", "12 open",
                                                        50, 20)]
    sw_band = [r for r in sect_wide if ON in r or OFF in r]
    check("sect: the drawn title takes the stroke (no one-cell stroke)",
          bool(sw_band) and not THIN.search("\n".join(sw_band)))
    check("sect: the drawn title stands on the continuous lattice",
          bool(sw_band) and all(" " not in r for r in sw_band))
    check("sect: the drawn title stays inside its measure",
          max(len(r) for r in sect_wide) <= 50)
    sect_nar = [grey(r) for r in LG.kit("naught").sect("AGENDA", "12 open",
                                                       30, 20)]
    check("sect: a narrow measure falls back to x1 rather than wrapping",
          max(len(r) for r in sect_nar) <= 30
          and any(ON in r for r in sect_nar))
    check("sect: the x1 title is still on the continuous lattice",
          all(" " not in r for r in sect_nar if ON in r or OFF in r))

    print("\n== TYPE LEVEL: the METRIC-BEARING numeral alphabet")
    # The alphabet stopped being a uniform 3x5 box: every glyph declares its
    # own, and the table is MEASURED off the masks. The reason is one number —
    # at 3 columns a closed figure's COUNTER is a single column, 2 cells of 6
    # at the sx=2 dense standard, 33% of the ink width against Font16's 71%,
    # and a counter is where legibility dies. Integer scaling cannot cure it:
    # it multiplies stroke and counter together. Every law below has a
    # negative control, because a metrics table nobody measures is the
    # dead-token defect in typographic clothing.
    NM = LG.NA
    DIGITS = "0123456789"
    CLOSED = "04689"                      # the glyphs with an enclosed counter
    INNER = re.compile(f"(?<={ON})({OFF}+)(?={ON})")

    def dense(text, sx=2):
        """The rendered form at naught's dense standard: sx, dot_w=1, gap=0."""
        return [grey(r) for r in NM.label(text, "#fff", "#111", 1, 0, sx, True)]

    def counter(rows):
        """The widest INTERIOR unlit run — unlit cells with ink on both sides
        in the same row. This is the hole the eye reads a closed figure by."""
        return max((len(m.group(1)) for r in rows for m in INNER.finditer(r)),
                   default=0)

    # 1. THE TABLE IS REAL — one advance for all ten digits, a different one
    #    for glyphs that are not digits. A table whose every entry is equal is
    #    a constant wearing a table's clothes.
    check("alphabet: all ten digits share ONE advance (TABULAR figures)",
          len({NM.advance(d) for d in DIGITS}) == 1,
          f"advance {sorted({NM.advance(d) for d in DIGITS})}")
    check("alphabet: a non-digit advances DIFFERENTLY — the table is not a "
          "constant (letter 4, period 3, digit 5)",
          NM.advance("A") != NM.advance("0")
          and NM.advance(".") != NM.advance("A"),
          f"A={NM.advance('A')} '.'={NM.advance('.')} 0={NM.advance('0')}")
    check("alphabet: the `1` inks NARROWER than it advances — ink and step "
          "are separate numbers, which a scale factor cannot express",
          NM.METRICS["1"][1] < NM.METRICS["0"][1]
          and NM.advance("1") == NM.advance("0"),
          f"ink {NM.METRICS['1'][1]} in an advance of {NM.advance('1')}")
    # nth-exempt: `m` here is the LOOP VARIABLE of the comprehension on the
    # next line, ranging over `NM.METRICS.values()` — tuples, not sequences
    # that can be empty. It shadows an unrelated `m = SW_RULE.search(...)`
    # elsewhere in this file, and that is the assignment the sweep resolves
    # it to. Same one-hop name resolution as the exemption at L3434, and the
    # same argument for listing it rather than out-clevering it.
    check("alphabet: the row height is DERIVED from the tallest inked glyph, "
          "not declared",
          NM.ALPHA_ROWS == max(m[0] for m in NM.METRICS.values())
          and NM.ALPHA_ROWS == max(len(g) for g in NM._ALPHA.values()),
          f"{NM.ALPHA_ROWS} rows")
    check("alphabet: every mask is rectangular (the metrics read mask[0], so "
          "a ragged glyph would lie about its advance)",
          all(len({len(r) for r in g}) == 1 for g in NM._ALPHA.values()))

    # 2. THE COUNTER — the measurement the whole change exists for.
    for d in CLOSED:
        ink, cnt = NM.METRICS[d][1] * 2, counter(dense(d))
        check(f"alphabet: '{d}' keeps an OPEN counter at sx=2 "
              f"(counter/ink >= 0.40)",
              cnt / ink >= 0.40, f"{cnt}/{ink} cells = {cnt / ink:.2f}")

    def old3(mask):
        """The 3-wide form this replaced, drawn through the same route."""
        bm = [[1 if ch == "#" else 0 for ch in row for _ in range(2)]
              for row in mask]
        return [grey(r) for r in NM.field(6 * 2, 5, bm, "#fff", "#111",
                                          dot_w=1, gap=0, ox=0)]

    for d, mask in (("0", ("###", "#.#", "#.#", "#.#", "###")),
                    ("8", ("###", "#.#", "###", "#.#", "###"))):
        cnt = counter(old3(mask))
        check(f"alphabet: the 3-wide '{d}' it replaced FAILED that floor "
              f"(control — the predicate can go red)",
              cnt / 6 < 0.40, f"{cnt}/6 cells = {cnt / 6:.2f}")

    # 3. THE VISUAL ASPECT — a cell is ~1:2, so a glyph N columns by M rows
    #    reads as N/(2M). Font16's reference is 0.70; the old 3x5 box gave
    #    0.60. The bracket's ceiling is exactly what a 4-column box produces,
    #    so this check is also "no digit is wider than its box".
    for d in DIGITS:
        ir, ic, _ = NM.METRICS[d]
        asp = (ic * 2) / (2 * ir)
        check(f"alphabet: '{d}' visual aspect at sx=2 lands in [0.55, 0.80]",
              0.55 <= asp <= 0.80, f"{asp:.2f}")

    # 4. ANTI-JIGGLE — what tabular actually buys: a count that changes from
    #    1 to 8 must not move a cell of what follows it.
    STEP = NM.advance("0") * 2
    tails = {d: "\n".join(r[STEP:] for r in dense(d + "8")) for d in DIGITS}
    check("alphabet: the glyph that FOLLOWS is byte-identical whichever digit "
          "precedes it (no jiggle)",
          len(set(tails.values())) == 1, f"{len(set(tails.values()))} form(s)")
    check("alphabet: ten digits drawn alone share one field width",
          len({len(dense(d)[0]) for d in DIGITS}) == 1)
    check("alphabet: the anti-jiggle probe CAN see a shift (control: a period "
          "advances 3, so it moves the glyph after it)",
          "\n".join(r[STEP:] for r in dense(".8")) != tails["0"])

    # 5. THE `1`'s BASE SERIF — a bare stem reads as a rule, not a figure.
    one = NM._ALPHA["1"]
    check("alphabet: the `1` stands on a BASE SERIF (bottom row inks wider "
          "than the stem)",
          one[-1].count("#") > one[2].count("#"),
          f"serif {one[-1].count('#')} vs stem {one[2].count('#')}")
    # the control is the SAME predicate on a footless stem, not on another
    # digit: 2 and 3 also end on a wide bar, so "the bottom row is widest"
    # would have been a claim about bars rather than about serifs
    bare = (".#..", "##..", ".#..", ".#..", ".#..")
    check("alphabet: a serif-less stem FAILS that same test (control — the "
          "predicate can go red)",
          not (bare[-1].count("#") > bare[2].count("#")))

    # 6. THE PASS-23/24 DENSITY LAWS, now held PER GLYPH rather than on one
    #    sample word — a new digit could regress either of them alone.
    check("alphabet: no digit has a one-cell stroke at sx=2 (the density law)",
          not THIN.search("\n".join("\n".join(dense(d)) for d in DIGITS)))
    check("alphabet: no digit puts a plain cell in its field (full bleed)",
          all(" " not in r for d in DIGITS for r in dense(d)))

    # 7. THE CONSUMER'S EXACT CELL — the digits are wider, so the head's x2
    #    tier costs more column. Asserted where it flips, not described.
    SX2_CELLS = NM.plain_width("12", 1, 0, 2, True)
    check("head: the x2 two-digit sprite costs exactly what the metrics say",
          SX2_CELLS == 2 * (NM.advance("1") + NM.advance("2") - NM.GLYPH_GAP)
          and SX2_CELLS == 18, f"{SX2_CELLS} cells")
    check("head: x2 is bought at w=19 and refused at w=18 (the exact cell)",
          len(head_sprite(19)[0]) == SX2_CELLS
          and len(head_sprite(18)[0]) == NM.plain_width("12", 1, 0, 1, True),
          f"19 -> {len(head_sprite(19)[0])}, 18 -> {len(head_sprite(18)[0])}")
    check("head: every TWO-digit count draws the same width — the board's "
          "heads never reflow because a count changed",
          len({len(head_sprite(40, n)[0]) for n in (10, 11, 18, 88, 99)}) == 1)
    check("head: every ONE-digit count draws the same width",
          len({len(head_sprite(40, n)[0]) for n in range(10)}) == 1)

    print("\n== TYPE LEVEL: the DRAWN DISPLAY BASES (`slab` · `flap` · `stencil`)")
    # Ledger and solari shipped `hero="plain"` — the honest borrowed posture,
    # never a placeholder. Both now DRAW, and both draw through a new pixel
    # BASE rather than a new hero branch, because the difference between them
    # and `block2` is a STROKE LOGIC, not a resolution (LANGUAGES.md: the base
    # is a language's shape scale). Every law the metric-bearing alphabet
    # earned above is re-asserted here on the RENDERED form, per glyph, with a
    # negative control each — a display type nobody measures is the dead-token
    # defect wearing a typeface.
    #
    # THE UNLIT VOCABULARY IS PER BASE and that is the load-bearing subtlety:
    # `slab` leaves bare ground where there is no ink, but `flap` DRAWS its
    # unlit hinge (`▔`) across the whole face, exactly as naught's lattice
    # draws its dark dots. A counter measured with the hinge counted as INK
    # reads 0.20 on the `4` — the hole is still a hole, and the measurement
    # has to say so.
    BASE_OF = {"slab": "ledger", "flap": "solari", "stencil": "blueprint"}
    UNLIT = {"slab": " ", "flap": " " + BS.FLAP_SEAM_FACE, "stencil": " "}
    # THE INK VOCABULARY IS PER BASE TOO, and it had to become one when the
    # stencil arrived: `hole()` used to derive its ink from a hardcoded
    # `{█ ▀ ▄}`, which is every mark slab and flap make but NONE of the two
    # RAILS a hollow figure's stems are built from — a `0`'s counter would
    # have measured 0 through a predicate that simply could not see its walls.
    # The slab and flap entries below are exactly the sets that expression
    # produced, so neither base's numbers move.
    INK = {"slab": "█▀▄", "flap": "█▀▄",
           "stencil": BS.ST_HOLLOW}
    # the glyphs with a hole the eye reads them by, DECLARED rather than found
    # by a predicate (pass 35's reason: the measurement is horizontal and does
    # not prove a counter is enclosed vertically)
    SLAB_CLOSED = FLAP_CLOSED = STENCIL_CLOSED = "02345689"
    NARROW3 = {"0": ("###", "#.#", "#.#", "#.#", "###"),
               "8": ("###", "#.#", "###", "#.#", "###")}

    def drawn(text, base):
        return BS.draw_numeral(text, base, HE.HERO_FONT)

    def ink_span(rows, base):
        cols = [i for r in rows for i, ch in enumerate(r)
                if ch not in UNLIT[base]]
        return (max(cols) - min(cols) + 1) if cols else 0

    def hole(rows, base):
        """The widest INTERIOR unlit run — the hole the eye reads a closed
        figure by. `unlit` and `ink` are the base's own vocabulary, not just a
        space and a block."""
        pat = re.compile(f"(?<=[{INK[base]}])([{UNLIT[base]}]+)"
                         f"(?=[{INK[base]}])")
        return max((len(m.group(1)) for r in rows for m in pat.finditer(r)),
                   default=0)

    check("the ink vocabulary of each base is the one it actually draws "
          "(probe self-check: a predicate blind to a base's marks measures "
          "zero and passes nothing)",
          all(set("".join("".join(drawn(d, b)) for d in DIGITS))
              - set(UNLIT[b]) <= set(INK[b]) for b in BASE_OF),
          str({b: sorted(set("".join("".join(drawn(d, b)) for d in DIGITS))
                         - set(UNLIT[b])) for b in BASE_OF}))

    for base, lang in BASE_OF.items():
        closed = SLAB_CLOSED
        check(f"{lang} declares the base it renders "
              f"(hero='dot', base='{base}')",
              TH.THEMES[lang]["hero"] == "dot"
              and TH.THEMES[lang]["base"] == base)
        check(f"{base}: the base is registered and dispatches by NAME, not by "
              f"an if in the hero",
              base in BS.BASES and callable(BS.BASES[base]["fn"]))
        # 1. THE FIGURE IS A FIGURE — rows, and the same rows for every digit
        heights = {len(drawn(d, base)) for d in DIGITS}
        check(f"{base}: every digit stands the same number of rows, and it is "
              f">= 5 (a display figure, not a glyph)",
              heights == {7}, f"{sorted(heights)} rows")
        # 2. TABULAR — one advance for all ten, and the proof is that the
        #    glyph AFTER a digit cannot move. This is what a hero buys from a
        #    per-glyph table: a value ticking 9 -> 10 does not slide the card.
        step = len(drawn("8", base)[0])
        pairs = {d: len(drawn(d + "8", base)[0]) for d in DIGITS}
        check(f"{base}: all ten digits share ONE advance (TABULAR figures)",
              len(set(pairs.values())) == 1, f"widths {sorted(set(pairs.values()))}")
        tails = {d: "\n".join(r[step:] for r in drawn(d + "8", base))
                 for d in DIGITS}
        check(f"{base}: the glyph that FOLLOWS is byte-identical whichever "
              f"digit precedes it (no jiggle)",
              len(set(tails.values())) == 1,
              f"{len(set(tails.values()))} form(s)")
        # ... and the probe CAN see a shift: the base declares its own
        # inter-glyph gap (BASE_GAP), so composing at the caller's default
        # moves everything after the first glyph
        shifted = BS.render(BS.from_font("08", HE.HERO_FONT, gap=1), base)
        check(f"{base}: the anti-jiggle probe CAN see a shift (control: the "
              f"caller's default gap of 1 moves the second glyph)",
              "\n".join(r[step:] for r in shifted) != tails["0"])
        # 3. THE COUNTER, on the RENDERED form, per closed glyph
        for d in closed:
            rows_d = drawn(d, base)
            ink, cnt = ink_span(rows_d, base), hole(rows_d, base)
            check(f"{base}: '{d}' keeps an OPEN counter (counter/ink >= 0.40)",
                  ink and cnt / ink >= 0.40,
                  f"{cnt}/{ink} cells = {cnt / ink if ink else 0:.2f}")
        # ... with the 3-column form the alphabet pass retired as the control
        for d, mask in NARROW3.items():
            rows_n = BS.render([[1 if ch == "#" else 0 for ch in r]
                                for r in mask], base)
            ink, cnt = ink_span(rows_n, base), hole(rows_n, base)
            check(f"{base}: a 3-column '{d}' FAILS that floor through the "
                  f"same base (control — the predicate can go red)",
                  not (ink and cnt / ink >= 0.40),
                  f"{cnt}/{ink} cells = {cnt / ink if ink else 0:.2f}")
        # 4. THE VISUAL ASPECT — a cell is ~1:2, so N ink cells over M rows
        #    reads as N/(2M). Unlike the alphabet's, this bracket has real
        #    spread on `slab` (0.57 to 0.71), because a serif foot widens the
        #    figure and a bowl does not.
        for d in DIGITS:
            rows_d = drawn(d, base)
            asp = ink_span(rows_d, base) / (2 * len(rows_d))
            check(f"{base}: '{d}' visual aspect lands in [0.55, 0.80]",
                  0.55 <= asp <= 0.80, f"{asp:.2f}")
        check(f"{base}: the tabular `1` inks the box it advances — the one "
              f"glyph the stroke logic cannot widen, corrected per BASE so "
              f"the font instrument and nord share does not move",
              "1" in BS.BASE_GLYPH[base]
              and ink_span(drawn("1", base), base)
              >= ink_span(drawn("0", base), base))

    # 5. SLAB — STROKE CONTRAST and SERIF FEET, the two things that make it a
    #    bookkeeping figure rather than a fat bitmap.
    for d in DIGITS:
        rows_d = drawn(d, "slab")
        stems = [(r, c) for r, row in enumerate(rows_d)
                 for c, ch in enumerate(row) if ch == "█"]
        hairs = [ch for row in rows_d for ch in row if ch in "▀▄"]
        check(f"slab: '{d}' draws its verticals HEAVY and its horizontals "
              f"HAIR (both weights present, and the stem is 2 cells)",
              bool(stems) and bool(hairs)
              and all(row.count("█") % 2 == 0 for row in rows_d),
              f"{len(stems)} stem cells, {len(hairs)} hairline cells")
    # THE FEET, asserted where a slab face actually puts them: on the stems
    # that reach the BASELINE. `0 3 5 6 8 9` close their bowls above it and
    # get none — which is the typographic claim AND the control that the
    # flare is conditional rather than sprayed on every glyph.
    FOOTED, BOWLED = "1247", "035689"
    for d in FOOTED + BOWLED:
        slab_base = drawn(d, "slab")[-1].strip()
        flat_base = drawn(d, "block2")[-1].strip()
        wider = len(slab_base) > len(flat_base)
        check(f"slab: '{d}' {'STANDS ON SERIF FEET' if d in FOOTED else 'has a BOWL, so no foot'}"
              f" — its baseline is {'wider' if d in FOOTED else 'no wider'} "
              f"than the footless base draws it",
              wider == (d in FOOTED),
              f"slab {len(slab_base)} vs block2 {len(flat_base)} cells")
    check("slab: the foot is drawn at the BASELINE (a half block), never a "
          "full stem cell — a serif that weighs what a stem weighs is a bar",
          all(drawn(d, "slab")[-1].lstrip()[0] == "▄" for d in "12"),
          repr([drawn(d, "slab")[-1] for d in "12"]))
    check("slab: two figures never touch — the feet of '18' leave bare "
          "ground between them (the base declares its own gap)",
          "  " in drawn("18", "slab")[-1])

    # 6. FLAP — the HINGE. It must cross the whole face, sit where the base
    #    says it sits, and NOT erase what it cuts.
    SEAM_ROW = BS.flap_seam(7)
    check("flap: the hinge is at the asserted row (row 4 of 7, the card's "
          "vertical middle)", SEAM_ROW == 3, f"row {SEAM_ROW}")
    for d in DIGITS:
        rows_d = drawn(d, "flap")
        faces = BS.flap_faces(d, HE.HERO_FONT)
        seam = rows_d[SEAM_ROW]
        on_face = [seam[a:b + 1] for a, b in faces]
        check(f"flap: '{d}' — the hinge crosses the ENTIRE face, ink included",
              all(f and set(f) <= {BS.FLAP_SEAM_FACE, BS.FLAP_SEAM_INK}
                  for f in on_face), repr(on_face))
        check(f"flap: '{d}' — no OTHER row carries the hinge glyph",
              not any(BS.FLAP_SEAM_FACE in r or BS.FLAP_SEAM_INK in r
                      for i, r in enumerate(rows_d) if i != SEAM_ROW))
    check("flap: the hinge does NOT erase the figure it cuts — '8' still "
          "differs from '0' on the seam row (a full rule would have merged "
          "them, and the counter law would not have seen it)",
          drawn("8", "flap")[SEAM_ROW] != drawn("0", "flap")[SEAM_ROW],
          f"{drawn('8', 'flap')[SEAM_ROW]!r} vs "
          f"{drawn('0', 'flap')[SEAM_ROW]!r}")
    check("flap: a numeral crossing the hinge marks it with a DIFFERENT glyph "
          "than bare face — the hinge is two-channel before any colour",
          BS.FLAP_SEAM_INK != BS.FLAP_SEAM_FACE
          and BS.FLAP_SEAM_INK in drawn("8", "flap")[SEAM_ROW]
          and BS.FLAP_SEAM_FACE in drawn("8", "flap")[SEAM_ROW])
    fa = BS.flap_faces("12", HE.HERO_FONT)
    check("flap: ONE face per digit, all the same width, none overlapping — "
          "a BANK of cells, and the faces align to the seam grid",
          len(fa) == 2 and len({b - a for a, b in fa}) == 1
          and fa[0][1] < fa[1][0], f"{fa}")
    check("flap: bare GROUND stands between two faces (the cards do not "
          "merge into one card)",
          fa[1][0] - fa[0][1] - 1 >= 1, f"{fa[1][0] - fa[0][1] - 1} cell(s)")
    check("flap: every face is fully inside the render (a face span that ran "
          "past the row would paint the ground)",
          fa[-1][1] < len(drawn("12", "flap")[0]),
          f"face ends {fa[-1][1]}, row {len(drawn('12', 'flap')[0])} cells")
    check("flap: one digit draws ONE face (the bank is the value's own "
          "length, not a fixed cabinet)",
          len(BS.flap_faces("7", HE.HERO_FONT)) == 1)

    # 7. STENCIL — the two claims that make it a stencil rather than a light
    #    bitmap: the figure is HOLLOW (a stroke is its edges, the inside is
    #    ground) and every closed outline is BRIDGED (an unbroken ring is the
    #    one thing a real stencil cannot have). Both with controls that go red.
    HOLLOW = set(BS.ST_HOLLOW)

    def st_bm(text):
        """The exact bitmap `draw_numeral` hands the base — same font patch,
        same gap — so a bridge measured here is the bridge that renders."""
        return BS.from_font(text, {**HE.HERO_FONT, **BS.BASE_GLYPH["stencil"]},
                            gap=BS.BASE_GAP["stencil"])

    for d in DIGITS:
        rows_d = drawn(d, "stencil")
        marks = set("".join(rows_d)) - {" "}
        check(f"stencil: '{d}' is drawn ENTIRELY out of hollow marks — not one "
              f"cell of it is a solid block",
              marks <= HOLLOW and "█" not in marks, f"{sorted(marks)}")
    # ... and the control, which is the whole point of stating it as a
    # vocabulary: the same digit through the three OTHER drawn bases is solid,
    # so "no block" is a property this base earns and not one every base has
    for b in ("block2", "slab", "flap"):
        solid = set("".join("".join(drawn(d, b)) for d in DIGITS))
        check(f"stencil: ... and '{b}' FAILS that same test (control — every "
              f"other drawn base puts a solid block on the screen)",
              "█" in solid)
    check("stencil: the two RAILS are what a one-pixel stem is made of — the "
          "ink hugs the outer half-cells and a full cell-width of ground runs "
          "between them (the cut is HALF a cell there, stated because the row "
          "budget cannot afford a whole one: the same honest reading flap's "
          "hinge gets)",
          all(BS.ST_RAIL_W + BS.ST_RAIL_E in r
              for r in drawn("0", "stencil")[1:6]),
          repr(drawn("0", "stencil")[2]))
    check("stencil: a rail is never a solid stroke — `▐▌` (ink filling the "
          "middle) appears nowhere in the specimen",
          not any(BS.ST_RAIL_E + BS.ST_RAIL_W in r
                  for d in DIGITS for r in drawn(d, "stencil")))
    # THE CUT IS A REAL CELL OF GROUND wherever the stroke can afford one, and
    # that is measured on a mask thick enough to have an interior — the digits'
    # one-pixel strokes cannot, which is exactly why this control exists.
    th = BS.stencil([[1] * 6 for _ in range(5)])
    check("stencil: a stroke thick enough to afford it is cut with REAL cells "
          "of ground — an interior pixel draws nothing at all",
          any(" " in r for r in th[1:-1]) and th[0].strip() and th[-1].strip(),
          repr(th))
    check("stencil: ... and the thick figure still CLOSES — every row of it "
          "carries ink at both ends (an outline with an open side is a leak)",
          all(r[0] != " " and r[-1] != " " for r in th), repr(th))
    solid_th = BS.block_wide([[1] * 6 for _ in range(5)])
    check("stencil: ... and the control — the same mask through `block2` has "
          "no ground in it anywhere (the cut is this base's, not the mask's)",
          " " not in "".join(solid_th))
    # THE BRIDGES. One per enclosed counter, always the ring pixel N of that
    # counter's NW-most cell, and the bridgeless render is kept as the control
    # that the law can go red.
    RINGED, UNRINGED = "04689", "12357"
    for d in RINGED + UNRINGED:
        cuts = BS.stencil_bridges(st_bm(d))
        want = 2 if d == "8" else (1 if d in RINGED else 0)
        check(f"stencil: '{d}' is bridged {want}x — one gap per CLOSED "
              f"outline, none where there is no ring to break",
              len(cuts) == want, f"{cuts}")
    for d in RINGED:
        bm = st_bm(d)
        out = BS._outside(bm)
        counters = [(r, c) for r in range(len(bm)) for c in range(len(bm[0]))
                    if not bm[r][c] and (r, c) not in out]
        nw = min(counters)
        check(f"stencil: '{d}' places its bridge CONSISTENTLY — N of the "
              f"north-west-most cell of the counter, the same rule on every "
              f"figure", (nw[0] - 1, nw[1]) in BS.stencil_bridges(bm),
              f"counter NW {nw}, cuts {BS.stencil_bridges(bm)}")
        # the bridge must actually OPEN the ring: after the cut the counter is
        # reachable from the border, which is what "the island would fall out"
        # means mechanically
        cut = [[v for v in row] for row in bm]
        for r, c in BS.stencil_bridges(bm):
            cut[r][c] = 0
        check(f"stencil: '{d}' — the bridge OPENS the counter (it is reachable "
              f"from the sheet's edge afterwards, so the island is held)",
              nw in BS._outside(cut))
        check(f"stencil: '{d}' — the BRIDGELESS control leaves it CLOSED, so "
              f"that predicate can go red", nw not in out)
        check(f"stencil: '{d}' — and the two renders differ (a bridge that "
              f"changed no cell would be a comment)",
              BS.stencil(bm) != BS.stencil(bm, bridge=False))
    check("stencil: a value of two digits is bridged per FIGURE, not per "
          "render — '18' breaks the 8's two rings and leaves the 1 alone",
          len(BS.stencil_bridges(st_bm("18"))) == 2
          and all(c >= 6 for _, c in BS.stencil_bridges(st_bm("18"))),
          f"{BS.stencil_bridges(st_bm('18'))}")
    check("stencil: NOT ONE box-drawing codepoint is drawn — blueprint's own "
          "law allows the sheet ten box glyphs and none of them is a vertical "
          "stroke or a junction, so a display type made of `║` and `╬` would "
          "break the language it was drawn for",
          not re.search(r"[─-╿]",
                        "".join("".join(drawn(d, "stencil")) for d in DIGITS)))

    print("\n== KIT LEVEL: darkside — accent is INTERACTION-ONLY (the port's law)")
    kd = LG.kit("darkside")
    blue = TH.THEMES["darkside"]["accent"]
    passive = "\n".join([
        kd.head("BACKLOG", 5, 20, 0),
        kd.card_row("Steady work", "9d", kd["mut"], 28, 0, False),
        "\n".join(kd.card_rows("Steady work", "9d", kd["mut"], 28, 0, False,
                               calm_meta)),
        kd.tile_row("  4", "flight", kd["ink"], 20),
        kd.meter(3, 8, [4, 0, 2, 2], 44),
        kd.bar(9, None, kd["accent"]),     # callers pass accent; darkside remaps
        "\n".join(kd.sect("agenda", "12 open", 50, 20)),
        kd.spark([1, 3, 2, 5], 4),
        "\n".join(kd.plot([2, 5, 3, 7], 16, 4)),
        kd.gauge(4, 0, 10, 10, thr=8),
        "".join(kd.spinner(t) for t in range(4)),
        "\n".join(kd.wordmark("tb")),
    ])
    check("darkside: passive data carries ZERO accent (KMBlue = interaction)",
          blue not in passive)
    check("darkside: interaction wears the accent (switch on · active tab · knob)",
          blue in kd.switch(True) and blue in kd.tabs(["a", "b"], "a")
          and blue in kd.slider(4, 0, 10, 10))
    check("darkside: the moon doodle rides the recessive wordmark",
          any(p in grey("".join(kd.wordmark("tb"))) for p in kd.PHASES))
    check("darkside: lowercase register (head, caption)",
          "backlog" in grey(kd.head("BACKLOG", 5, 20, 0))
          and kd.display_cap("Days Left") == "days left")
    check("darkside: step meter survives greyscale (fill vs track by SHAPE)",
          grey(kd.meter(1, 8, [1], 30)) != grey(kd.meter(7, 8, [1], 30)))

    print("\n== KIT LEVEL: the passive RAIL — structure that is not interaction")
    RAIL = LG.KITS["darkside"].RAIL
    check("darkside: the rail wears the `rail` grey, never KMBlue",
          TH.THEMES["darkside"]["rail"] in kd.rail_prefix()
          and blue not in kd.rail_prefix())
    # DISPATCH: the mechanism must follow the token, not the class name —
    # a hardcoded rail would make `layout` dead metadata (VERIFY.md)
    #
    # AND THE GLYPH IS THE LANGUAGE'S OWN (F-14). This loop asked all eleven
    # languages for DARKSIDE's `▏` and compared the answer to their own
    # `layout` token, so it went red the day prism declared `layout: rail` and
    # drew `▎`. That is the same "one class stands for the axis" defect the
    # line above warns about, committed by the CHECKER instead of by a kit —
    # and prism's commitment is explicit at its `RAIL` in `language.py`: "NOT
    # DARKSIDE'S STROKE. `▏` is that language's rail and the suite holds a
    # NEGATIVE law over it -- no other language may carry it". So the kit is
    # right, the check was wrong, and the negative law it names is the half
    # this loop must keep.
    #
    # Both halves are now asserted over the SET of declared rails: a language
    # that declares `layout=rail` draws its OWN stroke and no other's, and a
    # language that does not draws NONE of them. The old form could only see
    # darkside's — prism's `▎` could have appeared on any of the other ten
    # rows and nothing here would have said so.
    RAILS = {g for g in (getattr(LG.KITS.get(n, LG.Kit), "RAIL", None)
                         for n in TH.ORDER) if g}
    check("the rail is a set of DECLARED strokes, one per rail language "
          "(probe self-check — an empty set would pass the loop below "
          "vacuously for all eleven)",
          len(RAILS) == sum(TH.THEMES[n].get("layout") == "rail"
                            for n in TH.ORDER),
          f"{sorted(RAILS)}")
    for name in TH.ORDER:
        k = LG.kit(name)
        rows = (k.card_rows("Shut down legacy servers", "8d", k["mut"], 40, 0,
                            False, META_A) + [k.head("BACKLOG", 5, 40, 0)])
        own = getattr(LG.KITS.get(name, LG.Kit), "RAIL", None)
        drawn = {g for g in RAILS if any(g in r for r in rows)}
        want = {own} if TH.THEMES[name].get("layout") == "rail" else set()
        check(f"{name}: rail renders IFF the language declares layout=rail — "
              f"and it is the language's OWN stroke, never another's",
              drawn == want,
              f"drawn={sorted(drawn)} want={sorted(want)} "
              f"layout={TH.THEMES[name].get('layout')!r}")
    # the rail is paid for out of the CONTENT budget, exactly like padding:
    # a rail that widened the row would wrap it at every width
    for w in (20, 28, 40, 96):
        rows = kd.card_rows("Shut down legacy servers", "8d", kd["mut"], w, 0,
                            False, META_A) + [kd.head("BACKLOG", 5, w, 0)]
        widest = max(len(grey(r)) for r in rows)
        check(f"darkside: the rail comes out of the budget, not the row (w={w})",
              widest <= w, f"widest={widest}")

    print("\n== KIT LEVEL: industrial's function PLATES (the `layout` token)")
    # The external spec claimed industrial "reads as corgi" once colour is
    # stripped, and prescribed plates as the cure for a law-01 failure. THE
    # CLAIM WAS PROBED FIRST AND IS FALSE — see the app-level section, which
    # measures the two boards against each other. The plates land anyway, as
    # identity DEEPENING rather than a rescue: until this pass industrial's
    # board was the base skeleton plus a rule, i.e. a composition its tokens
    # did not own, which is PENDING item 0's exact defect.
    ki = LG.kit("industrial")
    PLATE = re.compile(r"▐ ?\d\d ?▌?")          # the coded plate, either tier
    check("industrial declares the tokens it renders (layout=panel + plate)",
          TH.THEMES["industrial"].get("layout") == "panel" and ki.panel
          and bool(TH.THEMES["industrial"].get("plate")))
    codes = [PLATE.search(grey(ki.card_rows(f"Task {i}", "3d", ki["mut"], 40,
                                            i, False, META_A)[0]))
             for i in range(4)]
    check("industrial: every card row is stamped with a plate code",
          all(codes), f"{[c.group(0) if c else None for c in codes]}")
    digits = [re.search(r"\d\d", c.group(0)).group(0) for c in codes if c]
    check("industrial: the codes are two digits, sequential and unique",
          digits == ["01", "02", "03", "04"], f"{digits}")
    lg_head = grey(ki.head("BACKLOG", 7, 40, 0))
    # the leading cell the legend used to pay in its markup is the SEAT's now
    # (`.col-head { padding-left: 1 }`), so the band opens on cell 0 of the
    # measure it is given — the same cell a plate opens on (PENDING item 4)
    check("industrial: the head is a plate LEGEND (the tab leads the band, "
          "on the measure's own first cell)",
          lg_head.startswith("▐▌ "), repr(lg_head[:16]))
    check("industrial: the legend fills the measure it is handed EXACTLY — "
          "the plates under it are drawn to the same number, so a legend "
          "short or long of it is a band that does not head its own stack",
          all(len(grey(ki.head("BACKLOG", 7, w, 0))) == w
              for w in (20, 27, 40, 43, 109)),
          f"{[len(grey(ki.head('BACKLOG', 7, w, 0))) for w in (20, 27, 40, 43, 109)]}")
    # THE BOX FRAME IS THE THING THAT WENT: `frame="single"` used to hang a
    # rule under every head, and a rule is a second row. Its absence is the
    # recomposition, so it is asserted — with the flow degrade below as the
    # negative control that proves the assert can fail.
    check("industrial: the box frame is GONE — no rule under the legend",
          "─" not in lg_head and "\n" not in lg_head)
    # THE PLATE IS A SOLID BLOCK, and the code comes OUT OF the content
    # budget: a plate that widened the row would wrap it at every measure
    for w in HEAD_W:
        rows = (ki.card_rows("Shut down legacy servers", "8d", ki["mut"], w,
                             0, False, META_A) + [ki.head("BACKLOG", 7, w, 0)])
        widths = [len(grey(r)) for r in rows]
        check(f"industrial: the plate is a SOLID block at w={w} (every row "
              f"exactly {w} cells, nothing wraps)",
              set(widths) == {w}, f"{widths}")
        check(f"industrial: the code survives the budget at w={w}",
              bool(PLATE.search(grey(rows[0]))))
    # PROGRESSIVE, and the tight tier keeps its NUMBER: the first render
    # renounced the code below the threshold and the board showed adjacent
    # columns wearing different plates, which reads as a bug
    check("industrial: the WIDE plate is taken where the column pays for it",
          grey(ki.card_row("x", "3d", ki["mut"], ki.CODE_MIN, 0)
               ).startswith("▐ 01 ▌ ")
          and ki.plate_w(ki.CODE_MIN) == ki.PLATE_W)
    check("industrial: the TIGHT plate engages one cell below, code intact",
          grey(ki.card_row("x", "3d", ki["mut"], ki.CODE_MIN - 1, 0)
               ).startswith("▐01 ")
          and ki.plate_w(ki.CODE_MIN - 1) == ki.SHORT_W)
    check("industrial: plate_w PREDICTS the drawn plate at every size class",
          all(at(grey(ki.card_row("x", "3d", ki["mut"], w, 0)), "x")
              == ki.plate_w(w) for w in HEAD_W))
    floor = grey(ki.card_row("Shut down legacy servers", "8d", ki["mut"], 11, 0))
    check("industrial: a floor-width plate keeps its CHIP (data over "
          "decoration — the ledger tile's lesson)",
          "[8d]" in floor and len(floor) == 11, repr(floor))
    coloured = ki.card_rows("Shut down legacy servers", "8d", ki["mut"], 40,
                            0, False, META_A)
    ground = f"on {TH.THEMES['industrial']['plate']}"
    check("industrial: BOTH card rows are stamped on the `plate` ground (one "
          "block, not two rows)",
          all(ground in r for r in coloured))
    check("industrial: the legend wears the plate ground too",
          ground in ki.head("BACKLOG", 7, 40, 0))
    check("industrial: the plate survives greyscale on SHAPE (the code), not "
          "on its ground alone (the 2-channel law)",
          bool(PLATE.search(grey(coloured[0])))
          and TH.THEMES["industrial"]["plate"] not in grey(coloured[0]))
    # DISPATCH: the composition follows the token, not the class name — the
    # same law the rail, the ruling and the lattice are already held to
    for name in TH.ORDER:
        k = LG.kit(name)
        rows = (k.card_rows("Shut down legacy servers", "8d", k["mut"], 40, 0,
                            False, META_A) + [k.head("BACKLOG", 5, 40, 0)])
        check(f"{name}: the board wears function plates IFF layout=panel",
              any(PLATE.search(grey(r)) for r in rows)
              == (TH.THEMES[name].get("layout") == "panel"))
    # DEGRADE: the previous BOXED composition is preserved as the flow path,
    # not deleted. What the token owns is the board's head and card rows; the
    # boxed METER answers to `meter` and is asserted to survive untouched.
    old_layout = TH.THEMES["industrial"]["layout"]
    TH.THEMES["industrial"]["layout"] = "flow"
    try:
        kfl = LG.kit("industrial")
        fl_head = grey(kfl.head("BACKLOG", 7, 40, 0))
        fl_card = [grey(r) for r in kfl.card_rows("Shut down legacy servers",
                                                  "8d", kfl["mut"], 40, 0,
                                                  False, META_A)]
        fl_meter = grey(kfl.meter(3, 8, [4, 0, 2, 2], 44))
    finally:
        TH.THEMES["industrial"]["layout"] = old_layout
    check("industrial.layout=flow brings the BOX FRAME back (the head rule)",
          "─" in fl_head and fl_head.count("\n") == 1,
          f"{fl_head.count(chr(10)) + 1} rows")
    check("industrial.layout=flow drops the plates (no code, the ▪ mark back)",
          not any(PLATE.search(r) for r in fl_card)
          and fl_card[0].startswith("▪ "))
    check("industrial.layout=flow still renders the board — it degrades, "
          "not dies",
          "BACKLOG" in fl_head and "Shut down legacy servers" in fl_card[0])
    check("industrial.layout=flow leaves the BOXED meter alone (it answers "
          "to `meter`, not to `layout`)",
          fl_meter == grey(ki.meter(3, 8, [4, 0, 2, 2], 44)))
    check("industrial: the plate composition is restored after the mutation",
          grey(ki.head("BACKLOG", 7, 40, 0)) == lg_head)

    print("\n== KIT LEVEL: swiss's EDITORIAL TYPE GRID (the `layout` token)")
    # Until this pass swiss's board was full-width flow rows plus a rule under
    # EVERY head — a composition its tokens did not own (PENDING item 0's
    # shape), and one that contradicted the language's own note ("one rule").
    # Measured on the 118 board before the change: ~70% of every entry's
    # measure was empty and the spread carried one hairline per phase.
    ks = LG.kit("swiss")
    SW_RULE = re.compile("─{10,}")
    TITLE = "Shut down legacy servers"
    SW_W = (14, 28, 51, 68, 105)       # the five size classes of the grid
    SW_N = (1, 1, 2, 2, 3)             # ... and the tier each one lands in

    def sw_entry(w, k=None, proj=True):
        k = k or ks
        return grey(k.card_rows(TITLE, "8d", k["mut"], w, 0, False,
                                META_A if proj else None)[0])

    check("swiss declares the tokens it renders (layout=editorial + columns)",
          TH.THEMES["swiss"].get("layout") == "editorial" and ks.editorial
          and int(TH.THEMES["swiss"].get("columns", 0)) == 3)
    g105 = ks.grid(105)
    check("swiss: the board measure takes the full 3 columns",
          len(g105) == 3, f"{g105}")
    check("swiss: the columns are EQUAL and gutter-separated (a GRID, not a "
          "table of ad-hoc stops)",
          len({cw for _, cw in g105}) == 1
          and all(g105[i + 1][0] - (g105[i][0] + g105[i][1]) == ks.GUTTER
                  for i in range(len(g105) - 1)), f"{g105}")
    # THE FACT THE WHOLE ALIGNMENT RESTS ON: kanban.py budgets the head
    # `avail - 4` and the card its own content box, so the two surfaces are
    # measured a cell or two apart. Flush-LEFT placement on shared origins is
    # what survives that; a flush-right figure would not.
    check("swiss: head and entry measures land the SAME column origins even "
          "when kanban.py budgets them apart",
          [c[0] for c in ks.grid(105)] == [c[0] for c in ks.grid(107)],
          f"{[c[0] for c in ks.grid(105)]} vs {[c[0] for c in ks.grid(107)]}")
    entry = sw_entry(105)
    got = [at(entry, s) for s in ("Shut", "Web", "8d")]
    check("swiss: the entry sets subject, byline and figure on the grid's own "
          "column origins",
          got == [c[0] for c in g105], f"{got} vs {[c[0] for c in g105]}")
    hd0 = grey(ks.head("BACKLOG", 7, 106, 0))
    hl0 = hd0.split("\n")[0]
    check("swiss: the masthead sets its name and its count on that same grid "
          "— on the grid's OWN origins now, where it used to sit one cell in "
          "because the head was measured apart from the spread (item 4)",
          at(hl0, "B A C") == g105[0][0]
          and at(hl0, "7", last=True) == g105[-1][0],
          f"{[at(hl0, 'B A C'), at(hl0, '7', last=True)]}")
    # ONE HAIRLINE FOR THE WHOLE SPREAD — the law that makes it editorial
    ruled = [bool(SW_RULE.search(grey(ks.head("BACKLOG", 7, 106, i))))
             for i in range(4)]
    check("swiss: ONE hairline rules the whole spread (1 of 4 heads, not 4)",
          sum(ruled) == 1, f"{ruled}")
    check("swiss: and it is the MASTHEAD's — under the LEADING phase, a seat "
          "chosen rather than repeated",
          ruled[0] and not any(ruled[1:]))
    # THE BYLINE TOOK A COLUMN, NOT A ROW: the renunciation of the second row
    # is untouched, and the project it had nowhere to put now has a seat
    check("swiss: the byline took a COLUMN, not a ROW (one row per entry, "
          "the renunciation stands)",
          len(ks.card_rows(TITLE, "8d", ks["mut"], 105, 0, False, META_A)) == 1)
    check("swiss: the byline is information the flow row had nowhere to put",
          "Web" in entry
          and "Web" not in grey(ks._flow_card_row(TITLE, "8d", ks["mut"], 105)))
    # THE DROP RULE at five size classes: 3 -> 2 -> 1, never a wrap
    for w, want in zip(SW_W, SW_N):
        cols = ks.grid(w)
        rows = [ks.head("BACKLOG", 7, w, 0), ks.head("DONE", 0, w, 2),
                ks.card_row(TITLE, "8d", ks["mut"], w),
                *ks.card_rows(TITLE, "8d", ks["mut"], w, 0, False, META_A)]
        widest = max(len(ln) for r in rows for ln in grey(r).split("\n"))
        check(f"swiss @w={w}: the grid drops to {want} column(s) and nothing "
              f"wraps (every line <= {w})",
              len(cols) == want and widest <= w,
              f"n={len(cols)} widest={widest}")
        check(f"swiss @w={w}: the FIGURE survives the drop (data over "
              f"decoration — the ledger tile's law)",
              "8d" in sw_entry(w))
    # the thresholds are DERIVED from the two constants, not tabulated
    check("swiss: the 3rd column is taken exactly where it is paid for "
          "(3*MEASURE_MIN + 2*GUTTER = 78), and dropped one cell below",
          len(ks.grid(78)) == 3 and len(ks.grid(77)) == 2,
          f"{len(ks.grid(78))} / {len(ks.grid(77))}")
    check("swiss: the 2nd column likewise (2*MEASURE_MIN + GUTTER = 51)",
          len(ks.grid(51)) == 2 and len(ks.grid(50)) == 1,
          f"{len(ks.grid(51))} / {len(ks.grid(50))}")
    check("swiss: no column is ever narrower than a legible title measure "
          "(that is what the drop rule buys)",
          all(min(cw for _, cw in ks.grid(w)) >= ks.MEASURE_MIN
              for w in (51, 78, 105, 200)))
    check("swiss: the 1-column tier IS the flow row, verbatim — the drop rule "
          "degrades towards the form it replaced, never below it",
          ks.card_row(TITLE, "8d", ks["mut"], 28)
          == ks._flow_card_row(TITLE, "8d", ks["mut"], 28))
    # FIRST FIXATION is won on ISOLATION alone (HIERARCHY.md): the largest
    # element must not also be the brightest or the loudest
    hd_c = ks.head("BACKLOG", 7, 106, 0)
    en_c = ks.card_rows(TITLE, "8d", ks["mut"], 105, 0, False, META_A)[0]
    check("swiss: the masthead (the largest element) takes the SAME ink as "
          "the entries — isolation, not brightness",
          f"[{TH.THEMES['swiss']['ink']}]" in hd_c
          and f"[{TH.THEMES['swiss']['ink']}]" in en_c)
    check("swiss: ... and no accent either (the largest is not also the "
          "loudest)",
          TH.THEMES["swiss"]["accent"] not in hd_c)
    urg = ks.card_rows("Renew TLS certificate", "2d!", ks["alert"], 105, 0,
                       True, META_A)[0]
    check("swiss: the loudest element (the alert figure) is the SMALLEST — no "
          "element wins two channels at once",
          TH.THEMES["swiss"]["alert"] in urg
          and len(grey(urg).split()[-1]) < len("B A C K L O G"))
    # `columns` MUTATION: the grid must follow the token
    old_cols = TH.THEMES["swiss"]["columns"]
    TH.THEMES["swiss"]["columns"] = 2
    try:
        k2 = LG.kit("swiss")
        n2, e2 = len(k2.grid(105)), sw_entry(105, k2)
    finally:
        TH.THEMES["swiss"]["columns"] = old_cols
    check("swiss.columns=2 takes a column OUT of the grid at board measure",
          n2 == 2, f"{n2} columns")
    check("swiss.columns=2 renounces the BYLINE first (the declared order)",
          "Web" not in e2 and "8d" in e2)
    check("swiss: the 3-column grid is restored after the mutation",
          len(ks.grid(105)) == 3)
    # DISPATCH: the composition follows the token, not the class name. The
    # signature is behavioural — a rule under the LEADING head alone — so it
    # is asked of all eight without knowing any of their glyphs.
    for name in TH.ORDER:
        k = LG.kit(name)
        r = [bool(SW_RULE.search(grey(k.head("BACKLOG", 7, 106, i))))
             for i in range(4)]
        check(f"{name}: the rule stands under the LEADING phase ALONE IFF "
              f"layout=editorial",
              (r == [True, False, False, False])
              == (TH.THEMES[name].get("layout") == "editorial"), f"{r}")
    # DEGRADE: the previous full-width flow composition is preserved as the
    # flow path, not deleted. What the token owns is the board's head and
    # entries; `sect`, the hairline METER and the calendar answer to their own
    # tokens and are asserted to survive untouched.
    old_layout = TH.THEMES["swiss"]["layout"]
    TH.THEMES["swiss"]["layout"] = "flow"
    try:
        kfl = LG.kit("swiss")
        fl_heads = [grey(kfl.head("BACKLOG", 7, 106, i)) for i in range(4)]
        fl_entry = sw_entry(105, kfl)
        fl_sect = "\n".join(grey(r) for r in kfl.sect("AGENDA", "12 open", 50))
        fl_meter = grey(kfl.meter(3, 8, [4, 0, 2, 2], 44))
        fl_cal = "".join(grey(kfl.cal_cell(x))
                         for x in ("none", "over", "multi", "one"))
    finally:
        TH.THEMES["swiss"]["layout"] = old_layout
    check("swiss.layout=flow rules EVERY head again (the negative control: "
          "the ONE-hairline check CAN fail)",
          all(SW_RULE.search(h) for h in fl_heads),
          f"{[bool(SW_RULE.search(h)) for h in fl_heads]}")
    check("swiss.layout=flow drops the grid (the byline has nowhere to go)",
          "Web" not in fl_entry)
    check("swiss.layout=flow still renders the board — it degrades, not dies",
          "BACKLOG" in fl_heads[0].replace(" ", "") and TITLE in fl_entry)
    check("swiss.layout=flow leaves `sect` alone (it answers to `frame`, the "
          "same boundary the plate, the rail and the ruling draw)",
          fl_sect == "\n".join(grey(r) for r in ks.sect("AGENDA", "12 open", 50)))
    check("swiss.layout=flow leaves the HAIRLINE METER alone (it answers to "
          "`meter`)",
          fl_meter == grey(ks.meter(3, 8, [4, 0, 2, 2], 44)))
    check("swiss.layout=flow leaves the calendar cells alone",
          fl_cal == "".join(grey(ks.cal_cell(x))
                            for x in ("none", "over", "multi", "one")))
    check("swiss: the editorial composition is restored after the mutation",
          grey(ks.head("BACKLOG", 7, 106, 0)) == hd0)

    print("\n== KIT LEVEL: nord's MASTER/DETAIL SPLIT (the `layout` token)")
    # nord had NO first fixation: colour-stripped at 118x30 the brightest ink
    # belonged to TEN repeated card titles and the only ISOLATED element (the
    # hero numeral) came fifth, out-inked 61 cells to 25 by the load plot in
    # its own panel. The split gives the eye one subject. HIERARCHY.md's
    # sidebar+detail is the pattern, and its wording is load-bearing: "the
    # list keeps selection state" — so the detail follows the real cursor.
    kn = LG.kit("nord")
    ND_T = "Renew TLS certificate"
    ND_INK = TH.THEMES["nord"]["ink"]
    NW = (14, 28, 64, 65, 118)         # five classes, straddling the threshold

    check("nord has a KIT of its own at last (it was the bare base class, "
          "which is why it could own no composition)",
          isinstance(kn, LG.Nord) and LG.KITS["nord"] is LG.Nord)
    check("nord declares the tokens it renders (layout=split + split floors)",
          TH.THEMES["nord"].get("layout") == "split" and kn.split
          and kn.floors == (28, 34), f"floors={kn.floors}")
    check("nord: `Kit` is still the truth underneath — the subclass overrides "
          "the split and NOTHING else",
          all(getattr(LG.Nord, m, None) is getattr(LG.Kit, m, None)
              for m in ("head", "card_row", "card_rows", "meter", "sect",
                        "tile_row", "bar", "cal_cell", "surface", "empty")))
    mf, df = kn.floors
    # THE ONE GEOMETRY SEAT: renderer and checks read `panes()`, so "the panes
    # and the assertions agree" is true by construction (Ledger.cols precedent)
    m118, d118 = kn.panes(114)
    check("nord: the panes TILE the width exactly (master + gutter + detail)",
          m118 + kn.GUTTER + d118 == 114, f"{m118}+{kn.GUTTER}+{d118}")
    check("nord: the master is HIERARCHY.md's driving list (25-30% of the "
          "width) and never below its own floor",
          mf <= m118 and 0.25 <= m118 / 114 <= 0.32,
          f"{m118}/114 = {m118 / 114:.0%}")
    check("nord: the detail is the WIDE pane — the subject, not the list",
          d118 > m118, f"detail {d118} vs master {m118}")
    # THE DEGRADE, asserted at the exact cell it is bought
    thr = mf + kn.GUTTER + df
    check(f"nord: the split is bought exactly at w={thr} "
          f"(master_floor + gutter + detail_floor) and RENOUNCED one cell "
          f"below — master-only, never a wrap",
          kn.panes(thr) == (mf, df) and kn.panes(thr - 1) == (thr - 1, 0),
          f"{kn.panes(thr)} / {kn.panes(thr - 1)}")
    check("nord: below the threshold the master takes the WHOLE width (the "
          "degrade spends nothing on a pane it cannot fill)",
          all(kn.panes(w)[0] == w and kn.panes(w)[1] == 0
              for w in (10, 28, 50, thr - 1)))
    for w in NW:
        mw, dw = kn.panes(w)
        rows = [kn.master_row(ND_T, "3d", kn["warn"], mw, True),
                kn.master_row("Shut down legacy servers", "8d", kn["mut"],
                              mw, False)]
        if dw:
            rows += kn.detail_rows(ND_T, "3d", kn["warn"], dw, META_A)
        widest = max(len(grey(r)) for r in rows)
        lim = max(mw, dw)
        check(f"nord @w={w}: {'split' if dw else 'master-only'} and NOTHING "
              f"wraps (every line <= its own pane)",
              widest <= lim and mw + (kn.GUTTER + dw if dw else 0) == w,
              f"widest={widest} lim={lim} panes={(mw, dw)}")
    # THE CURSOR: exactly one row can carry it, and it is the driven one
    cur_on = kn.master_row(ND_T, "3d", kn["warn"], 34, True)
    cur_off = kn.master_row(ND_T, "3d", kn["warn"], 34, False)
    check("nord: the master row carries the cursor EXACTLY when it is driven",
          grey(cur_on).count(kn.CUR) == 1 and kn.CUR not in grey(cur_off))
    check("nord: the driven row also brightens (2 channels, so the cursor "
          "survives greyscale AND colour-blindness)",
          f"[{ND_INK}]" in cur_on and f"[{ND_INK}]" not in cur_off)
    check("nord: the master row is COMPACT — one row per task, the base kit's "
          "metadata row renounced because that field has a whole pane now",
          "\n" not in cur_on
          and len(kn.card_rows(ND_T, "3d", kn["warn"], 34, 0, False,
                               META_A)) == 2)
    # LAW 03, ENCODED: one element wins area AND brightness AND isolation
    det = kn.detail_rows(ND_T, "3d", kn["warn"], 77, META_A)
    mrows = [kn.master_row(t, c, kn["mut"], 34, i == 0) for i, (t, c) in
             enumerate(((ND_T, "3d"), ("Write API reference", "5d"),
                        ("Shut down legacy servers", "8d")))]
    TTL = 1                             # det = ["", title, "", fields..., bar]

    def isolated(rs, i):
        above = i > 0 and not grey(rs[i - 1]).strip()
        below = i + 1 < len(rs) and not grey(rs[i + 1]).strip()
        return above and below

    # AREA is measured as EXTENT — the cells an element COMMANDS, first
    # painted to last. Painted-cell COUNT was tried first and is the wrong
    # instrument: it ranks a dense dim block above a heading, i.e. backwards,
    # and it scores letterspacing at zero when letterspacing is precisely how
    # a terminal enlarges type. The count is still reported beside it so the
    # weaker number is not hidden.
    def span(s: str) -> int:
        t = grey(s)
        return 0 if not t.strip() else len(t.rstrip()) - (len(t) - len(t.lstrip()))

    ink_of = [span(r) for r in det]
    check("nord: the detail title is the WIDEST single element in the split "
          "(AREA — letterspaced through the base kit's own display register)",
          ink_of[TTL] == max(ink_of + [span(r) for r in mrows]),
          f"title spans {ink_of[TTL]} cells "
          f"({len(grey(det[TTL]).replace(' ', ''))} inked) vs "
          f"{max(ink_of[TTL + 1:] + [span(r) for r in mrows])}")
    check("nord: the detail title is the ONLY bold ink in the split "
          "(BRIGHTNESS — bold ink is spent once, and here)",
          f"[{ND_INK} bold]" in det[TTL]
          and not any("bold" in r for i, r in enumerate(det) if i != TTL)
          and not any("bold" in r for r in mrows))
    check("nord: the detail title is ISOLATED — a blank row above and below",
          isolated(det, TTL))
    check("nord: ... and no MASTER row is (the list is contiguous by design, "
          "so isolation is the detail pane's alone)",
          not any(isolated(mrows, i) for i in range(len(mrows))))
    winners = [i for i in range(len(det))
               if isolated(det, i) and ink_of[i] == max(ink_of)
               and "bold" in det[i]]
    check("nord: EXACTLY ONE element wins area AND brightness AND isolation "
          "— which is HIERARCHY.md's self-check, and what nord failed",
          winners == [TTL], f"winners at {winners}")
    # the negative control: the check CAN fail. A detail pane drawn the way
    # the base kit draws a card wins none of the three.
    # the counterfactual is the base card AT THE MASTER'S OWN WIDTH — the form
    # the board showed before this pass. Drawn at the DETAIL's 77 cells it
    # spans 76 (the chip is flushed right), which is a configuration the split
    # never renders; the first version of this control asked that and went red.
    flat = kn.card_rows(ND_T, "3d", kn["warn"], 34, 0, False, META_A)
    check("nord: that check CAN fail — the base kit's card, at the width the "
          "master actually gives it, wins none of the three levers "
          "(negative control)",
          not any("bold" in r for r in flat)
          and max(span(r) for r in flat) < ink_of[TTL],
          f"card spans {max(span(r) for r in flat)} vs title {ink_of[TTL]}")
    # the DETAIL's content: the fields, and the quantity mechanism
    dg = "\n".join(grey(r) for r in det)
    check("nord: the detail expands the task — the fields the compact row "
          "renounced are all there",
          all(f in dg for f in ("PROJECT", "PHASE", "DUE", "PRIORITY",
                                "STATE", "PROGRESS")), )
    check("nord: quantity in the detail is nord's OWN meter family (the "
          "filled/unfilled block pair `_meter_blocks` draws), not a second "
          "mechanism",
          "▇" in dg and "░" in dg
          and "▇" in grey(kn.meter(3, 8, [4, 0, 2, 2], 44)))
    # a state word under a DUE label was on screen and is a lie — the render
    # caught it, so it becomes a check
    blk = "\n".join(grey(r) for r in
                    kn.detail_rows(ND_T, "blk", kn["alert"], 77, META_B))
    check("nord: a STATE word never prints under the DUE label (the render "
          "caught 'DUE  blk'; the state has its own field)",
          "DUE" not in blk and "blocked" in blk)
    # DISPATCH: the composition follows the TOKEN, asked of all eight
    for name in TH.ORDER:
        k = LG.kit(name)
        check(f"{name}: the board is a MASTER/DETAIL split IFF layout=split",
              (k.board_layout() == "split")
              == (TH.THEMES[name].get("layout") == "split"),
              k.board_layout())
    # `split` MUTATION: the geometry must follow the token
    old_sp = TH.THEMES["nord"]["split"]
    TH.THEMES["nord"]["split"] = (20, 20)
    try:
        k2 = LG.kit("nord")
        # measured INSIDE the mutation: a kit holds a live reference to its
        # theme dict, so anything computed after the restore reads the
        # original token — which is how the first version of this check
        # compared two identical lists and went red.
        c2 = k2.composition()
        p2_bind = [k2.panes(w) for w in (44, 50, 64)]
        p2_44 = k2.panes(44)
    finally:
        TH.THEMES["nord"]["split"] = old_sp
    # the floors do NOT bind at 114 (30% of 114 already clears both), so a
    # single wide width proves nothing about this token — the first version of
    # this check compared (34,77) with (34,77) and went red. The token acts
    # where the floors bind, and that is where it is asked.
    check("nord.split=(20,20) moves the pane geometry where the floors "
          "actually bind (a wide board is the wrong place to ask: 30% of 114 "
          "already clears both floors, so the token is invisible there)",
          p2_bind != [kn.panes(w) for w in (44, 50, 64)],
          f"{p2_bind} vs {[kn.panes(w) for w in (44, 50, 64)]}")
    check("nord.split=(20,20) also moves the DEGRADE threshold (the split is "
          "bought earlier when its floors are cheaper)",
          p2_44[1] > 0 and kn.panes(44)[1] == 0, f"{p2_44} vs {kn.panes(44)}")
    check("nord.split=(20,20) also moves the min-widths the STYLESHEET "
          "declares (one token, both seats — never two sources of a width)",
          "min-width: 20" in c2 and f"min-width: {mf}" in kn.composition())
    check("nord: the geometry is restored after the mutation",
          kn.panes(114) == (m118, d118))
    # DEGRADE: the base (flow) composition is preserved byte-exactly
    old_l = TH.THEMES["nord"]["layout"]
    TH.THEMES["nord"]["layout"] = "flow"
    try:
        kfl = LG.kit("nord")
        fl_layout, fl_comp, fl_tcss = (kfl.board_layout(), kfl.composition(),
                                       kfl.tcss())
        fl_card = "\n".join(kfl.card_rows(ND_T, "3d", kfl["warn"], 34, 0,
                                          False, META_A))
    finally:
        TH.THEMES["nord"]["layout"] = old_l
    kbase = LG.Kit("nord")
    check("nord.layout=flow returns the board to the columns skeleton",
          fl_layout == "columns" and fl_comp == "")
    check("nord.layout=flow restores the BASE KIT byte-exactly — the previous "
          "composition is preserved, not deleted",
          fl_tcss == kbase.tcss() and fl_card == "\n".join(
              kbase.card_rows(ND_T, "3d", kbase["warn"], 34, 0, False, META_A)))
    check("nord: the split composition is restored after the mutation",
          kn.board_layout() == "split" and kn.composition() != "")

    print("\n== KIT LEVEL: instrument's SCOPE RETICLE (the `layout` token)")
    # instrument is the polish benchmark, so the bar here is "is this MORE
    # instrument", not "does it pass". What the trace REPLACED is the argument:
    # the flow sub-row drew phase progress, which is a property of the COLUMN —
    # every card in a phase rendered the identical bar, four times over, and
    # then restated the due chip beside it. The reticle spends the same two
    # rows on a quantity that actually varies down the column.
    ki = LG.kit("instrument")
    IT = "Renew TLS certificate"
    IW = (13, 16, 21, 39, 105)         # five classes, straddling the threshold

    def imeta(days):
        return dict(META_A, days=days)

    def itrace(w, days):
        return ki.trace_row(w, imeta(days))

    check("instrument declares the tokens it renders (layout=trace + the "
          "reticle's own ink)",
          TH.THEMES["instrument"].get("layout") == "trace" and ki.traced
          and ki.tick_ink == TH.THEMES["instrument"]["tick"]
          and ki.unit_ink == TH.THEMES["instrument"]["unit"])
    # ONE GEOMETRY SEAT: the head, every trace row and every check below read
    # `reticle()` (the Ledger.cols / Swiss.grid / Nord.panes precedent), so
    # "the ticks and the samples share the same cells" is true by construction
    sp39, tk39 = ki.reticle(39)
    check("instrument: the reticle's ticks stand on the WEEK grid — cell "
          "1 + k*7, recomputed from the constants rather than tabulated",
          tk39 == [1 + k * ki.TICK_EVERY
                   for k in range(1, ki.HORIZON // ki.TICK_EVERY + 1)
                   if 1 + k * ki.TICK_EVERY < sp39] and tk39 == [8, 15, 22],
          f"span={sp39} ticks={tk39}")
    check("instrument: the HORIZON is capped, so a wide column shows the same "
          "three weeks a narrow one shows — width buys horizon, never a "
          "different scale",
          ki.reticle(105)[0] == ki.HORIZON + 2 == sp39,
          f"reticle(105)={ki.reticle(105)[0]} reticle(39)={sp39}")
    # THE DEGRADE, asserted at the exact cell the scale is bought
    ITHR = ki.SPAN_MIN + ki.IND + 1 + ki.VAL_W
    check(f"instrument: the scale is bought exactly at w={ITHR} and RENOUNCED "
          f"one cell below — the reticle is never squeezed",
          ki.reticle(ITHR)[0] == ki.SPAN_MIN and ki.reticle(ITHR - 1) == (0, []),
          f"{ki.reticle(ITHR)} / {ki.reticle(ITHR - 1)}")
    check("instrument: the narrow tier IS the bench readout the trace "
          "replaced, verbatim — the degrade lands on the previous form and "
          "can therefore never be worse than it",
          ki.card_rows(IT, "3d", ki["warn"], ITHR - 1, 0, False, META_A)
          == ki._flow_card_rows(IT, "3d", ki["warn"], ITHR - 1, 0, False,
                                META_A))
    for w in IW:
        sp, tks = ki.reticle(w)
        rows = ki.card_rows(IT, "3d", ki["warn"], w, 0, False, META_A) \
            + ki.head("BACKLOG", 7, w, 0).split("\n")
        widest = max(len(grey(r)) for r in rows)
        check(f"instrument @w={w}: {'reticle' if sp else 'renounced'} and "
              f"NOTHING wraps (every line <= its own measure)",
              widest <= w, f"widest={widest} span={sp} ticks={tks}")
    # THE HEAD IS THE SPINE, and it is two rows in every regime
    ihead = ki.head("BACKLOG", 7, 43, 0).split("\n")
    # one cell BELOW the width that buys a scale — the head no longer pays a
    # 4-cell trim, so the renouncing width is the card's own (PENDING item 4)
    inarrow = ki.head("DONE", 2, ki.SPAN_MIN + ki.IND + ki.VAL_W, 2).split("\n")
    check("instrument: the head carries the reticle IFF the token, and the "
          "flow head's SATURATING 4-cell spark is gone with it (a phase of 7 "
          "and a phase of 4 drew the identical four cells)",
          ki.ORIGIN in grey(ihead[1]) and len(ihead) == 2
          and ki.ORIGIN not in grey(ki._flow_head("BACKLOG", 7, 43, 0))
          and (grey(ki._flow_head("BACKLOG", 7, 43, 0))
               == grey(ki._flow_head("BACKLOG", 4, 43, 0)).replace("4", "7")))
    check("instrument: the head is ALWAYS two rows, even where the scale is "
          "renounced — a kanban is read ACROSS its columns, and a one-row head "
          "started the narrow column's stack a row above its neighbours'",
          len(inarrow) == 2 and not grey(inarrow[1]).strip(),
          f"narrow head rows={len(inarrow)}")
    # EXACT AGREEMENT (PENDING item 4, cured at the source). The head and its
    # cards are handed the SAME measure by `kanban.py.row_width` and share the
    # seat's one-cell inset, so the axis and the samples are one geometry
    # function at one argument. Both of these used to be inexact — an origin
    # pad and a length trim of four, this language's private compensation for
    # a head measured 3-4 cells wide of the card's box.
    def iaxis(w):
        # SENTINEL "": a head that stopped drawing a SECOND row has no axis,
        # and "" carries no ORIGIN, no TICK and no unit label — so every
        # reticle law below reds on a count of 0 and `at(...)` returns -1,
        # rather than the file dying inside a helper two hundred lines from
        # the law that reads it. This is mutant M3a's shape exactly: the trap
        # in a helper's RETURN, one `split` index to the right of the one
        # pass 66 excluded wholesale as safe.
        return grey(nth(ki.head("BACKLOG", 7, w, 0).split("\n"), 1, ""))

    def isample(w, days=3):
        rows = [grey(r) for r in ki.card_rows(IT, "3d", ki["warn"], w, 0,
                                              False, imeta(days))]
        return first_of((r for r in rows if ki.LATT in r), "")

    IWR = [w for w in IW if ki.reticle(w)[0]]
    check("instrument: the probe reaches the reticle at more than one width "
          "class (self-check — an empty list would pass the two laws below "
          "vacuously)",
          len(IWR) >= 3, f"reticled widths {IWR}")
    check("instrument: the head's axis origin lands on the very cell every "
          "sample grows from, at EVERY width class — the same measure, the "
          "same seat inset, so the origins agree by construction",
          all(min(at(iaxis(w), ki.ORIGIN), at(isample(w), ki.LATT)) >= 0
              and at(iaxis(w), ki.ORIGIN) == at(isample(w), ki.LATT) + 1
              for w in IWR),
          f"{[(at(iaxis(w), ki.ORIGIN), at(isample(w), ki.LATT) + 1) for w in IWR]}")
    check("instrument: the axis and the samples under it tick the SAME cells "
          "and run the SAME length — EXACT, where this was `head <= card` "
          "while the two surfaces were measured apart",
          all([i for i, ch in enumerate(iaxis(w)) if ch == ki.TICK]
              == [i for i, ch in enumerate(isample(w)) if ch == ki.GRAT]
              and ki.IND + ki.reticle(w)[0] == len(iaxis(w))
              for w in IWR),
          f"{[(len(iaxis(w)), ki.IND + ki.reticle(w)[0]) for w in IWR]}")
    # DATA, not decoration — DATAVIZ law 1: shape carries it, in GREYSCALE
    check("instrument: the trace is DATA — a 3-day sample and a 9-day sample "
          "differ in GREYSCALE, where the flow sub-row drew phase progress and "
          "so rendered the IDENTICAL bar for every card in a column",
          grey(itrace(39, 3)) != grey(itrace(39, 9))
          and (grey(ki._flow_card_rows(IT, "3d", ki["mut"], 39, 0, False,
                                       imeta(3))[1])
               == grey(ki._flow_card_rows("x", "9d", ki["mut"], 39, 0, False,
                                          imeta(9))[1]).replace("9d", "3d")))
    check("instrument: SHARED SCALE (DATAVIZ law 2) — one cell is one day in "
          "EVERY column, so a 3-day task is the same length in the widest "
          "column and the narrowest; width buys horizon, not resolution",
          (at(grey(itrace(39, 3)).strip(), ki.LATT + ki.FULL) >= 0
           and at(grey(itrace(39, 3)).strip(), ki.LATT + ki.FULL)
           == at(grey(itrace(21, 3)).strip(), ki.LATT + ki.FULL))
          and grey(itrace(39, 3)).count(ki.FULL)
          == grey(itrace(21, 3)).count(ki.FULL) == 3)
    check("instrument: MICROBAR FLOOR (DATAVIZ law 3) — DUE TODAY lights a "
          "half cell, so it can never be read as 'nothing due'",
          ki.HALF in grey(itrace(39, 0))
          and ki.HALF not in grey(itrace(39, None))
          and grey(itrace(39, 0)) != grey(itrace(39, None)))
    # CLIPPING, NEVER CLAMPING (the Bodmer law) — at BOTH boundaries
    lo, at_hi, over = itrace(39, -2), itrace(39, ki.HORIZON), itrace(39, 40)
    check("instrument: off-scale LOW is CLIPPED AND FLAGGED at the boundary, "
          "never clamped onto the origin — a clamped overdue task would print "
          "as 'due today'",
          grey(lo)[ki.IND] == ki.FULL and grey(lo)[ki.IND + 1] == ki.LATT
          and f"[{ki['alert']}]" in lo and grey(lo) != grey(itrace(39, 0))
          and "-2d" in grey(lo))
    check("instrument: off-scale HIGH is CLIPPED AND FLAGGED too — a 40-day "
          "task is distinguishable from one that really sits AT the horizon, "
          "and the reading still states the true number",
          ki.OVER in grey(over) and ki.OVER not in grey(at_hi)
          and grey(over) != grey(at_hi) and "40d" in grey(over)
          and len(grey(over)) == len(grey(at_hi)))
    check("instrument: the off-scale flag is a glyph the FILL never emits, so "
          "it can never be mistaken for a sample reaching the last cell",
          ki.OVER not in {ki.FULL, ki.HALF, ki.LATT}
          and not any(ki.OVER in grey(itrace(39, d)) for d in range(0, 22)))
    # UNITS — the clinical register, and its own tone
    check("instrument: the reading and the axis labels are UNITS, in the unit "
          "tone, and the graticule is in the tick tone — a label is not a "
          "datum and a gridline is not a signal",
          f"[{ki.unit_ink}]3d[/]" in itrace(39, 3)
          and f"[{ki.unit_ink}]7d[/]" in ihead[1]
          and f"[{ki.tick_ink}]" in ihead[1]
          and all(f"{d}d" in grey(ihead[1]) for d in (7, 14, 21)))
    check("instrument: the trace itself is the ACCENT — instrument spends one "
          "hue on the live signal, and the graticule under it never takes it",
          f"[{ki['accent']}]" in itrace(39, 3)
          and ki.tick_ink != ki["accent"] and ki.unit_ink != ki["accent"])
    # THE DISPATCH LAW: the reticle appears IFF instrument declares the token.
    #
    # THE PREDICATE WAS WIDENED 2026-07-27 (the blueprint pass) AND THE OLD ONE
    # WAS WRONG, not merely narrow. It asked for `Instrument.ORIGIN` — `├` —
    # and nothing else, which made it a test for ONE GLYPH rather than for the
    # reticle. `├` is also a DIMENSION TERMINATOR, and blueprint draws one on
    # every row of its sheet; the old check went red on a language that has no
    # scope, no axis and no trace in it. A reticle is an ORIGIN CARRYING WEEK
    # TICKS (or a trace hanging its graticule off one), so that is what is
    # asked now — and it still fails on anything that does not draw one, which
    # the loop proves on nine languages every run.
    for nm in TH.ORDER:
        kk = LG.kit(nm)
        rows = kk.head("BACKLOG", 7, 43, 0).split("\n") \
            + kk.card_rows(IT, "3d", kk["warn"], 39, 0, False, META_A)
        has = any(LG.Instrument.ORIGIN in grey(r)
                  and LG.Instrument.TICK in grey(r) for r in rows) \
            or any(LG.Instrument.GRAT in grey(r) for r in rows)
        check(f"dispatch: {nm} draws a reticle IFF it declares layout=trace",
              has == (nm == "instrument"))
    check("dispatch: the reticle predicate is not a bare `├` test — blueprint "
          "draws that glyph as a dimension terminator and carries no scope "
          "(the collision this check was widened for)",
          LG.Instrument.ORIGIN in grey(LG.kit("blueprint").head("BACKLOG", 7,
                                                                43, 0))
          and LG.Instrument.TICK not in grey(
              LG.kit("blueprint").head("BACKLOG", 7, 43, 0)))
    # DEGRADE: everything OUTSIDE the token's boundary is left alone
    old_il = TH.THEMES["instrument"]["layout"]
    TH.THEMES["instrument"]["layout"] = "flow"
    try:
        kifl = LG.kit("instrument")
        fl = dict(
            head=kifl.head("BACKLOG", 7, 43, 0),
            card="\n".join(kifl.card_rows(IT, "3d", kifl["warn"], 39, 0,
                                          False, META_A)),
            sect="\n".join(kifl.sect("AGENDA", "12 open", 50, 20)),
            meter=kifl.meter(3, 8, [4, 0, 2, 2], 44),
            cal="".join(kifl.cal_cell(x) for x in ("none", "over", "multi")),
            tile=kifl.tile_row(" 12", "overdue", kifl["alert"], 20),
            comp=kifl.composition())
    finally:
        TH.THEMES["instrument"]["layout"] = old_il
    check("instrument.layout=flow restores the bench readout byte-exactly — "
          "the previous composition is preserved as `_flow_*`, not deleted",
          fl["head"] == ki._flow_head("BACKLOG", 7, 43, 0)
          and fl["card"] == "\n".join(
              ki._flow_card_rows(IT, "3d", ki["warn"], 39, 0, False, META_A)))
    check("instrument.layout=flow leaves `sect`, the braille meter, the "
          "calendar and the tile alone — the token owns the HEAD and the "
          "TRACE ROW, and nothing else",
          fl["sect"] == "\n".join(ki.sect("AGENDA", "12 open", 50, 20))
          and fl["meter"] == ki.meter(3, 8, [4, 0, 2, 2], 44)
          and fl["cal"] == "".join(ki.cal_cell(x)
                                   for x in ("none", "over", "multi"))
          and fl["tile"] == ki.tile_row(" 12", "overdue", ki["alert"], 20))
    check("instrument.layout=flow gives the head's blank row BACK to "
          "`.col-head` — the reticle pays for its own row, so the composition "
          "costs the board nothing vertically",
          "margin-bottom: 0" in ki.composition()
          and "margin-bottom: 0" not in fl["comp"])
    check("instrument: the reticle composition is restored after the mutation",
          ki.traced and ki.board_layout() == "columns")

    print("\n== KIT LEVEL: corgi's MODE SURFACE + PARAM STRIP (the `layout` "
          "token)")
    kc = LG.kit("corgi")
    MODES = ["board", "lanes", "agenda", "gantt"]
    CG_T = "Shut down legacy servers"      # 24 chars — the fixture's longest
    check("corgi declares layout=strip and DISPATCHES on it (not on the "
          "class name)",
          TH.THEMES["corgi"].get("layout") == "strip" and kc.striped)
    # -- the geometry seat -------------------------------------------------
    check("corgi: `slots` is right-flushed and never runs past its row",
          all(sl[-1][0] + len(sl[-1][1]) + 1 + sl[-1][2] == w
              for w in (56, 74, 90, 112)
              for sl in [kc.slots(w)] if sl))
    check("corgi: every declared param has a slot on a full-width row",
          [lab for _, lab, _ in kc.slots(112)] == [l for l, _ in kc.PARAMS])
    # THE DROP RULE, at the EXACT cell it is derived to fall on — a threshold
    # asserted a few cells either side of the truth is a threshold nobody can
    # disprove (the swiss/instrument precedent)
    for w, n in ((56, 3), (55, 2), (47, 2), (46, 1), (38, 1), (37, 0)):
        check(f"corgi: at w={w} the strip carries {n} slot(s) (the drop rule "
              f"is derived from TITLE_MIN, not tabulated)",
              len(kc.slots(w)) == n, f"{len(kc.slots(w))}")
    check("corgi: the title measure never falls under TITLE_MIN while a "
          "strip is drawn (that is what the drop rule is FOR)",
          all(sl[0][0] - kc.NUM_W - kc.SLOT_GAP >= kc.TITLE_MIN
              for w in range(38, 121) for sl in [kc.slots(w)] if sl))
    # FIVE WIDTH CLASSES, and nothing may wrap at any of them
    for w in (30, 40, 56, 74, 112):
        rows = kc.card_rows(CG_T, "8d", kc["mut"], w, 0, False, META_A)
        plain = [grey(r) for r in rows]
        check(f"corgi @w={w}: the row fits its measure (no wrap)",
              all(len(p) <= w for p in plain), f"{[len(p) for p in plain]}")
    # -- the card is ONE row, and the degrade lands on the form it replaced --
    strip_rows = kc.card_rows(CG_T, "8d", kc["mut"], 74, 0, False, META_A)
    check("corgi: under strip the card is ONE full-width param row (it was "
          "two)", len(strip_rows) == 1
          and len(kc._flow_card_rows(CG_T, "8d", kc["mut"], 74, 0, False,
                                     META_A)) == 2)
    narrow = kc.card_rows(CG_T, "8d", kc["mut"], 30, 0, False, META_A)
    check("corgi: below the threshold the strip is RENOUNCED and the two-row "
          "flow card comes back, byte for byte",
          narrow == kc._flow_card_rows(CG_T, "8d", kc["mut"], 30, 0, False,
                                       META_A))
    # -- ONE geometry, shared by every row on the page ----------------------
    def slot_cells(plain: str) -> list[int]:
        # `plain` is ALREADY colour-stripped: greying it twice would strip the
        # row's own `[1]` param number as if it were a markup tag and shift
        # every cell by four (found by this check going red on a correct
        # render — the instrument lying about the subject, BACKGROUND.md §5)
        return [i for lab, _ in kc.PARAMS
                for i in [plain.find(lab + " ")] if i >= 0]

    rows74 = [grey(kc.card_rows(t, c, kc["mut"], 74, i, False, m)[0])
              for i, (t, c, m) in enumerate(
                  ((CG_T, "8d", META_A), ("Fix it", "3d", META_B),
                   ("A" * 40, "--", META_A)))]
    check("corgi: every param row on the page shares ONE slot geometry "
          "(identical cells, whatever the title)",
          len({tuple(slot_cells(r)) for r in rows74}) == 1,
          f"{ {tuple(slot_cells(r)) for r in rows74} }")
    check("corgi: the slot cells are the ones `slots()` computed (the "
          "renderer and the check read the SAME seat)",
          tuple(slot_cells(rows74[0]))
          == tuple(x for x, _, _ in kc.slots(74)))
    # -- what the strip DROPPED, and what it must not have dropped ----------
    check("corgi: `PH` is GONE from the strip row — under a sections board "
          "the phase is the head's job, so it was a CONSTANT down the page",
          "PH " not in grey(strip_rows[0])
          and "PH " in grey(kc._flow_card_rows(CG_T, "8d", kc["mut"], 74, 0,
                                               False, META_A)[1]))
    check("corgi: no field was lost with the row — the chip's OWN readings "
          "survive in engraved slots (blocked -> ST BLK, days -> DUE)",
          "BLK" in grey(kc.card_rows("x", "blk", kc["alert"], 74, 0, True,
                                     META_B)[0])
          and "-2D" in grey(kc.card_rows("x", "blk", kc["alert"], 74, 0, True,
                                         META_B)[0])
          and "DONE" in grey(kc.card_rows(
              "x", "done", kc["dim"], 74, 0, False,
              dict(META_A, done=True))[0]))
    check("corgi: the SEVERITY lands on the reading — the DUE value carries "
          "the row's tone, which the free-floating chip used to carry",
          f"[{kc['alert']}]-2D" in kc.card_rows("x", "blk", kc["alert"], 74,
                                                0, True, META_B)[0])
    check("corgi: the strip row still reads `numbered` (a new composition is "
          "not a licence to stop reading a token)",
          grey(strip_rows[0]).startswith("[1] "))
    # -- THE MODE STRIP -----------------------------------------------------
    strip = kc.tabs(MODES, "board")
    check("corgi: the mode strip NAMES EVERY MODE, numbered by the key that "
          "really switches it (it showed only the active one before)",
          all(f"[{i + 1}]" in grey(strip) for i in range(4))
          and all(m.upper() in grey(strip).replace(" ", "")
                  for m in MODES))
    check("corgi: the strip marks the mode on screen on a channel that "
          "survives GREYSCALE (letterspacing), never colour alone",
          grey(kc.tabs(MODES, "board")) != grey(kc.tabs(MODES, "agenda")))
    check("corgi: ... and the LETTERSPACING is that channel (tier 1)",
          " ".join("BOARD") in grey(kc.tabs(MODES, "board"))
          and " ".join("BOARD") not in grey(kc.tabs(MODES, "lanes")))
    for a in MODES:
        n = len(grey(kc.tabs(MODES, a)))
        check(f"corgi: the strip fits its narrowest seat with active={a} "
              f"(<= STRIP_MAX {kc.STRIP_MAX} — the measured 42-cell widget "
              f"seat)", n <= kc.STRIP_MAX, f"{n} cells")
    # TIER 2: a list whose labels no longer leave room for the letterspacing.
    # `timeline` is 8 cells against `gantt`'s 5, which is exactly enough to
    # push the spaced form over the seat and not enough to push the tight one
    # over — the ladder's middle rung, exercised at the cell it turns on.
    LONG = ["board", "lanes", "agenda", "timeline"]
    t2 = {a: kc.tabs(LONG, a) for a in ("board", "agenda", "timeline")}
    check("corgi: tier 2 — a list too long to letterspace still fits the "
          "seat, and still marks the active mode in GREYSCALE (the lit "
          "segment takes the channel over)",
          all(len(grey(v)) <= kc.STRIP_MAX for v in t2.values())
          and len({grey(v) for v in t2.values()}) == 3
          and kc.LIT in grey(t2["board"]),
          f"{sorted(len(grey(v)) for v in t2.values())} cells")
    check("corgi: tier 2 really IS the tight form (the letterspacing is what "
          "was given up — the negative control for the tier above)",
          " ".join("BOARD") not in grey(t2["board"])
          and len(grey(kc._strip(LONG, "timeline", True)[0])) > kc.STRIP_MAX)
    HUGE = [f"mode{i}" for i in range(9)]
    check("corgi: tier 3 — a list too long for even the tight form falls "
          "back to the ACTIVE-ONLY form, which is the composition the strip "
          "replaced (it can never be worse than what it replaced)",
          kc.tabs(HUGE, HUGE[2]) == kc._flow_tabs(HUGE, HUGE[2]))
    # -- DISPATCH + no leakage ---------------------------------------------
    for name in TH.ORDER:
        k = LG.kit(name)
        striped = TH.THEMES[name].get("layout") == "strip"
        rows = k.card_rows(CG_T, "8d", k["mut"], 74, 0, False, META_A)
        check(f"{name}: the ONE-row param strip renders IFF layout=strip",
              (len(rows) == 1 and "ST " in grey(rows[0])) == striped)
    check("corgi is the only language declaring layout=strip (no leakage)",
          [n for n in TH.ORDER
           if TH.THEMES[n].get("layout") == "strip"] == ["corgi"])
    # -- the FLOW degrade, at kit level, on every seat the token touches ----
    _old = TH.THEMES["corgi"].pop("layout")
    try:
        kf = LG.kit("corgi")
        fl = {"rows": kf.card_rows(CG_T, "8d", kf["mut"], 74, 0, False,
                                   META_A),
              "tabs": kf.tabs(MODES, "board"), "comp": kf.composition(),
              "layout": kf.board_layout(),
              "head": kf.head("BACKLOG", 7, 74, 0),
              "meter": kf.meter(3, 8, [4, 0, 2, 2], 44),
              "sect": "\n".join(kf.sect("AGENDA", "12 open", 50)),
              "tile": kf.tile_row(" 12", "overdue", kc["alert"], 20)}
    finally:
        TH.THEMES["corgi"]["layout"] = _old
    check("corgi.layout=flow restores the TWO-ROW spec card, byte for byte",
          fl["rows"] == kc._flow_card_rows(CG_T, "8d", kc["mut"], 74, 0,
                                           False, META_A))
    check("corgi.layout=flow restores the ACTIVE-ONLY tab strip, byte for "
          "byte", fl["tabs"] == kc._flow_tabs(MODES, "board"))
    check("corgi.layout=flow names ONLY the mode on screen — the negative "
          "control for 'the strip names every mode': that check CAN fail",
          sum(f"[{i + 1}]" in grey(fl["tabs"]) for i in range(4)) == 1)
    check("corgi.layout=flow restores the previous composition, byte for "
          "byte, and gives the board back to COLUMNS",
          fl["comp"] == kc._flow_composition() and fl["layout"] == "columns")
    check("corgi.layout=flow leaves the seats OUTSIDE the token's boundary "
          "untouched (head, meter, sect, tile)",
          fl["head"] == kc.head("BACKLOG", 7, 74, 0)
          and fl["meter"] == kc.meter(3, 8, [4, 0, 2, 2], 44)
          and fl["sect"] == "\n".join(kc.sect("AGENDA", "12 open", 50))
          and fl["tile"] == kc.tile_row(" 12", "overdue", kc["alert"], 20))
    check("corgi: the strip composition RECLAIMS the dead air the hairlines "
          "already separate (margins) and pays the tab strip its own row",
          "margin-top: 0" in kc.composition()
          and "height: 2" in kc.composition()
          and "margin-top: 0" not in fl["comp"])
    check("corgi: the strip composition is restored after the mutation",
          kc.striped and kc.board_layout() == "sections")

    print("\n== KIT LEVEL: ledger — paper, the ruling, and the RED PEN")

    def lum(hx: str) -> float:
        """Relative luminance (WCAG). The one measurement that decides
        whether a ground is light or dark, rather than whether it looks it."""
        def ch(u):
            u /= 255
            return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
        r, g_, b = (ch(int(hx[i:i + 2], 16)) for i in (1, 3, 5))
        return 0.2126 * r + 0.7152 * g_ + 0.0722 * b

    grounds = {n: lum(TH.THEMES[n]["ground"]) for n in TH.ORDER}
    others = max(v for n, v in grounds.items() if n != "ledger")
    check("ledger is the ONLY light-ground language (unmistakable in greyscale)",
          grounds["ledger"] > 0.5 > others,
          f"ledger={grounds['ledger']:.2f} · brightest other={others:.2f}")
    contrast = ((grounds["ledger"] + 0.05)
                / (lum(TH.THEMES["ledger"]["ink"]) + 0.05))
    check("ledger: ink reads ON that paper (contrast >= 7:1)",
          contrast >= 7, f"{contrast:.1f}:1")

    kl = LG.kit("ledger")
    pen = TH.THEMES["ledger"]["alert"]
    od_meta = {"proj": "API", "phase": "Review", "phase_idx": 3, "n_phases": 5,
               "days": -2, "prio": "low", "blocked": False, "done": False}
    calm_page = "\n".join([
        kl.head("BACKLOG", 6, 80, 0),
        "\n".join(kl.card_rows("Renew TLS certificate", "9d", kl["mut"], 80,
                               0, False, calm_meta)),
        kl.tile_row("  4", "work in flight", kl["ink"], 24),
        kl.meter(6, 10, [4, 0, 2, 2], 44),
        kl.bar(11, None, None),
        "\n".join(kl.sect("AGENDA", "12 open", 50, 20)),
        kl.cal_cell("none") + kl.cal_cell("one") + kl.cal_cell("multi"),
        kl.switch(True) + kl.switch(False),
        kl.slider(4, 0, 10, 10),
        "".join(kl.spinner(t) for t in range(4)),
        kl.tabs(["board", "lanes"], "board"),
        kl.queue_marker(2),
        " ".join(kl.icon(i) for i in ("deadline", "wip", "blocked", "workday")),
        "\n".join(kl.wordmark("TB")),
        kl.empty(20),
        kl.spark([1, 3, 2, 5], 4),
        "\n".join(kl.plot([2, 5, 3, 7], 16, 4)),
        kl.gauge(4, 0, 10, 10, thr=8),
    ])
    check("ledger: a page with nothing overdue carries ZERO red (debt only)",
          pen not in calm_page)
    overdue_entry = "\n".join(kl.card_rows("Fix checkout 500", "2d!",
                                           kl["alert"], 80, 0, True, od_meta))
    check("ledger: an OVERDUE posting IS written in the red pen",
          pen in overdue_entry and pen in kl.cal_cell("over")
          and pen in kl.icon("overdue"))
    check("ledger: the red pen is the ONLY icon exception (the rest are grey)",
          all(pen not in kl.icon(i) for i in
              ("deadline", "wip", "blocked", "workday", "boardfile")))

    # THE TALLY: counted in fives, and the mark follows its token
    def groups(markup):
        return grey(markup).split("\n")[0].split()[:-1]      # drop the % cell
    check("ledger: the tally counts in FIVES (five marks, then air)",
          groups(kl.meter(6, 10, [4, 0, 2, 2], 44))
          and all(len(g) == 5 for g in groups(kl.meter(6, 10, [4, 0, 2, 2], 44))),
          f"{groups(kl.meter(6, 10, [4, 0, 2, 2], 44))}")
    old_tally = TH.THEMES["ledger"]["tally"]
    TH.THEMES["ledger"]["tally"] = "•"
    try:
        mutated = LG.kit("ledger").meter(6, 10, [4, 0, 2, 2], 44)
    finally:
        TH.THEMES["ledger"]["tally"] = old_tally
    check("ledger: the tally MARK follows its token (mutation)",
          "•" in grey(mutated) and old_tally not in grey(mutated))
    check("ledger: groups of five survive the mutation",
          all(len(g) == 5 for g in groups(mutated)))
    check("ledger: the mark is NOT mistakable for the rule beside it",
          kl.tally != kl.RULE_V and kl.tally != kl.LEAD)

    # THE RULING: computed once, asserted against the render
    for w in (40, 80, 118):
        pos, _ = kl.cols(w)
        rows = kl.card_rows("Shut down legacy servers", "8d", kl["mut"], w,
                            0, False, META_A)
        rows.append(kl.card_row("Renew TLS certificate", "3d", kl["mut"], w, 4))
        for j, r in enumerate(rows):
            g_ = grey(r)
            check(f"ledger @{w}: row {j} fills the measure exactly",
                  len(g_) == w, f"len={len(g_)}")
            check(f"ledger @{w}: row {j} lands every rule on its computed cell",
                  [i for i, ch in enumerate(g_) if ch == kl.RULE_V] == pos,
                  f"{[i for i, ch in enumerate(g_) if ch == kl.RULE_V]} vs {pos}")
    # SENTINEL "": the claim is an EQUALITY against 80 rule glyphs, and "" is
    # not that string at any width — a head that lost its rule row reds here
    # instead of killing the rest of the ledger section
    _lgr = nth(grey(kl.head("BACKLOG", 6, 80, 0)).split("\n"), 1, "")
    check("ledger: the head rule spans the FULL measure, unbroken",
          _lgr == kl.RULE_HEAD * 80, f"{_lgr[:24]!r} ({len(_lgr)} cells)")
    check("ledger: the sub rule spans the full measure too",
          grey(kl.rule_line(80)) == kl.RULE_SUB * 80)
    check("ledger: a narrow page RENOUNCES columns, it does not crush them",
          len(kl.cols(120)[1]) > len(kl.cols(28)[1]) > len(kl.cols(14)[1]),
          f"fields at 120/28/14 = {[len(kl.cols(x)[1]) for x in (120, 28, 14)]}")

    # DOT LEADERS: every gap between a name and its figure is closed
    pos, _ = kl.cols(80)
    desc_field = grey(kl.card_row("Renew TLS", "3d", kl["mut"], 80,
                                  0))[pos[0] + 1: pos[1]]
    check("ledger: the description gap is CLOSED by leaders (no open space)",
          kl.LEAD in desc_field and "  " not in desc_field,
          repr(desc_field[-14:]))
    head_line = grey(kl.head("BACKLOG", 6, 80, 0)).split("\n")[0].lstrip()
    check("ledger: the account heading closes its gap too",
          kl.LEAD in head_line and "  " not in head_line)
    tile = grey(kl.tile_row("  4", "in flight", kl["ink"], 30))
    check("ledger: a tile closes its trailing gap with leaders", kl.LEAD in tile)
    # a tile is CLIPPED FROM THE RIGHT (app.py's measured lesson: a 14-char
    # label cropped every value off the widest size class). With this
    # language's 4-cell icon prefix in front, the FIGURE must still be on
    # screen — leaders may be lost, data may not.
    clipped = (grey(kl.icon("wip")) + " "
               + grey(kl.tile_row("  4", "work in flight", kl["ink"], 14)))[:14]
    check("ledger: a clipped tile keeps its FIGURE (leaders go, data stays)",
          "4" in clipped, repr(clipped))

    # THE BAND: every 5th LINE of the page, counted per account
    band = TH.THEMES["ledger"]["band"]
    page = []
    for i in range(5):
        page += kl.card_rows("Renew TLS certificate", "3d", kl["mut"], 60, i,
                             False, META_A)
    check("ledger: the band tints every 5th LINE of the page",
          [n for n, r in enumerate(page) if f"on {band}" in r] == [4, 9],
          f"{[n for n, r in enumerate(page) if f'on {band}' in r]}")
    check("ledger: the band is a GROUND tint, never ink",
          all("on " + band in r for r in (page[4], page[9]))
          and f"[{band}]" not in "".join(page))

    # SELECTION is a MARGIN mechanism: no border is spent, anywhere
    borders = re.findall(r"border(?:-left)?:\s*(\w+)", TH.tcss("ledger"))
    check("ledger: selection spends NO border (every focus border is `none`)",
          bool(borders) and all(b == "none" for b in borders),
          f"{sorted(set(borders))}")
    check("that check can fail (naught DOES spend a border — control)",
          any(b != "none" for b in
              re.findall(r"border(?:-left)?:\s*(\w+)", TH.tcss("naught"))))
    check("ledger: the margin marker is a glyph in the gutter, not a rule",
          kl.CUR == "▶" and kl.CUR != kl.RULE_V)

    # DISPATCH: the ruling follows the `layout` token, not the class name
    for name in TH.ORDER:
        k = LG.kit(name)
        rows = k.card_rows("Shut down legacy servers", "8d", k["mut"], 60, 0,
                           False, META_A)
        check(f"{name}: money-column rules render IFF layout=ruled",
              any(LG.Ledger.RULE_V in grey(r) for r in rows)
              == (TH.THEMES[name].get("layout") == "ruled"))

    print("\n== KIT LEVEL: solari — the SCHEDULE, the seam, and digits-not-bars")
    ks = LG.kit("solari")
    SEAM = LG.Solari.SEAM
    AMBER = TH.THEMES["solari"]["accent"]
    RED = TH.THEMES["solari"]["alert"]
    # the glyph families this language forbids ITSELF. `▁` is deliberately NOT
    # in BARS: it is the seam, this language's one divider, and a divider is
    # not a quantity. Braille is a range, not a list.
    RULES = "─━│┃═║┼┬┴┤├╪╷╵┊┆▏▕╌╎"
    BARS = "█▓▒░▄▀▌▐▬▂▃▅▆▇⣿⡇⠒"

    def has_bar(s: str) -> bool:
        return any(ch in BARS or 0x2800 <= ord(ch) <= 0x28FF for ch in s)

    # the surfaces that carry DATA. The component library (switch, spinner,
    # slider, flip frames) is deliberately out: a flap TURNING is motion, not
    # a reading, and this law is about what a quantity may be drawn with.
    calm_meta_s = {"proj": "Web", "phase": "Doing", "days": 9, "prio": "high",
                   "blocked": False, "done": False}
    data_surfaces = [
        ks.head("BACKLOG", 7, 80, 0),
        "\n".join(ks.card_rows("Renew TLS certificate", "9d", ks["mut"], 80,
                               0, False, calm_meta_s)),
        "\n".join(ks.sect("AGENDA", "12 open", 60, 20)),
        ks.meter(3, 8, [4, 0, 2, 2], 44),
        ks.bar(9, None, None),
        ks.tile_row(" 12", "in flight", ks["ink"], 24),
        "".join(ks.cal_cell(x) for x in ("none", "over", "multi", "one")),
        ks.queue_marker(2),
        ks.spark([1, 3, 2, 5, 4, 6, 2, 7], 8),
        "\n".join(ks.plot([2, 5, 3, 7, 4, 8, 6, 9], 24, 4)),
        ks.gauge(7, 0, 10, 10, thr=3),
    ]
    page = "\n".join(grey(s) for s in data_surfaces)
    check("solari: NO bar or braille glyph on any data surface (digits, "
          "never bars)", not has_bar(page),
          repr([ch for ch in set(page) if has_bar(ch)]))
    check("that check CAN fail — every other language draws one somewhere "
          "(negative control)",
          any(has_bar(grey(LG.kit(n).meter(3, 8, [4, 0, 2, 2], 44))
                     + "\n".join(grey(r) for r in
                                 LG.kit(n).plot([2, 5, 3, 7], 16, 4)))
              for n in TH.ORDER if n != "solari"))
    check("solari: the SEAM is the only divider (no rule glyph anywhere)",
          not any(ch in RULES for ch in page),
          repr([ch for ch in set(page) if ch in RULES]))
    check("solari: and the seam is actually PRESENT (probe self-check)",
          SEAM in page)
    check("solari: the meter STATES its figures as digits",
          all(d in grey(ks.meter(3, 8, [4, 0, 2, 2], 44)) for d in "38"))

    # -- THE BAND / SEAM GRID: one geometry seat, asserted to the cell -------
    for w in (28, 38, 44, 58, 76, 109, 118):
        band = grey(ks.head("BACKLOG", 7, w, 0))
        seam = grey(ks.card_rows("Renew TLS certificate", "9d", ks["mut"], w,
                                 0, False, calm_meta_s)[1])
        row = grey(ks.card_rows("Renew TLS certificate", "9d", ks["mut"], w,
                                0, False, calm_meta_s)[0])
        check(f"solari @{w}: the band is EXACTLY as wide as the seam",
              len(band) == len(seam) == w, f"band={len(band)} seam={len(seam)}")
        check(f"solari @{w}: the schedule row fills the same measure exactly",
              len(row) == w, f"len={len(row)}")
        check(f"solari @{w}: the seam is one glyph and only that glyph",
              set(seam) == {SEAM})
        check(f"solari @{w}: nothing wraps (one line per row)",
              "\n" not in row and "\n" not in band and "\n" not in seam)
    # THE FAILURE THE LAW EXISTS TO CATCH, run as a control: a band built one
    # cell wider than its seam must not pass the predicate above
    off = grey(ks.band_row(" GATE BACKLOG 07 ", 80 + 1))
    check("solari: a band ONE CELL wider than the seam FAILS that predicate "
          "(the check can fail)",
          len(off) != len(grey(ks.card_rows("x", "9d", ks["mut"], 80, 0,
                                            False, calm_meta_s)[1])))
    # REVERSE VIDEO, read off the markup: ground is the ink and ink is the
    # ground. Measured on the RENDER at app level; asserted here so the
    # mechanism is pinned in one place.
    band_mk = ks.head("BACKLOG", 7, 80, 0)
    check("solari: the band is REVERSE VIDEO (ground on ink)",
          f"[{TH.THEMES['solari']['ground']} on {ks['ink']}]" in band_mk)
    check("solari: and it is never ruled (no rule under the band)",
          "\n" not in band_mk and ks.rule_line(80) is None)

    # -- TABULAR: the anti-jiggle law (Bodmer T1/T2) ------------------------
    def bounds(w, chip, meta):
        """The cell each field starts on, read off the RENDER — not off the
        geometry seat, so the two can disagree and be caught."""
        r = grey(ks.card_rows("Renew TLS certificate", chip, ks["mut"], w, 0,
                              False, meta)[0])
        return [(x, c) for x, c, _ in ks.fields(w)], r

    ref_fields, ref_row = bounds(109, "9d", calm_meta_s)
    for chip, meta in (("12d", calm_meta_s),
                       ("3d", dict(calm_meta_s, days=3)),
                       ("2d!", dict(calm_meta_s, days=-2, prio="low")),
                       ("blk", dict(calm_meta_s, blocked=True, prio="normal")),
                       ("done", dict(calm_meta_s, done=True, proj="A")),
                       ("--", dict(calm_meta_s, days=None, proj=""))):
        f2, r2 = bounds(109, chip, meta)
        check(f"solari: field origins never move with the value ({chip!r})",
              f2 == ref_fields, f"{f2[:3]} vs {ref_fields[:3]}")
        check(f"solari: the row keeps its measure with the value ({chip!r})",
              len(r2) == len(ref_row) == 109)
        # and the FIELDS themselves are padded to their widest content: the
        # status word may change and the columns to its right may not move
        for x, code, n in ks.fields(109):
            if code in ("stat", "proj", "pri"):
                check(f"solari: the {code} field is fixed-width with {chip!r}",
                      len(r2[x: x + n]) == n and
                      (x + n == 109 or r2[x + n: x + n + LG.Solari.GAP]
                       == " " * LG.Solari.GAP))

    # -- THE DECLARED DROP ORDER, at the exact cell -------------------------
    LADDER = [(58, ["due", "item", "stat", "proj", "pri"]),
              (57, ["due", "item", "stat", "pri"]),
              (44, ["due", "item", "stat", "pri"]),
              (43, ["due", "item", "stat"]),
              (38, ["due", "item", "stat"]),
              (37, ["due", "item"]),
              (28, ["due", "item"]),
              (27, [])]
    for w, want in LADDER:
        got = [c for _, c, _ in ks.fields(w)]
        check(f"solari @{w}: the drop order buys exactly {want}",
              got == want, f"{got}")
    check("solari: the drop order is DECLARED, not tabulated (the constant "
          "is what the ladder reads)",
          LG.Solari.DROP == ("proj", "pri", "stat"), f"{LG.Solari.DROP}")
    for w, _ in LADDER:
        fs = ks.fields(w)
        if not fs:
            continue
        item = first_of(n for _, c, n in fs if c == "item")
        check(f"solari @{w}: ITEM is never cut below its floor",
              item >= LG.Solari.ITEM_MIN, f"item={item}")
        check(f"solari @{w}: the fields fill the measure exactly",
              fs[-1][0] + fs[-1][2] == w)
    check("solari: below the floor the schedule is RENOUNCED, not crushed",
          ks.fields(27) == [] and ks.fields(28) != [])
    # ... and the degrade lands on this language's own form, never on the
    # base kit's. The first draft fell through to `super()` and rendered
    # NORD's card anatomy at 28 cells — caught by the pairwise check.
    narrow = ks.card_rows("Renew TLS certificate", "9d", ks["mut"], 28, 0,
                          False, calm_meta_s)
    base_narrow = LG.Kit.card_rows(ks, "Renew TLS certificate", "9d",
                                   ks["mut"], 28, 0, False, calm_meta_s)
    check("solari: the narrow card is still SOLARI (seam kept, not the base "
          "kit's metadata row)",
          set(grey(narrow[1])) == {SEAM} and grey(narrow[1])
          != grey(base_narrow[1]))

    # -- THE RATION: amber for flight and selection, red for LATE -----------
    calm_page = "\n".join([
        ks.head("BACKLOG", 6, 80, 0),
        "\n".join(ks.card_rows("Renew TLS certificate", "9d", ks["mut"], 80,
                               0, False, calm_meta_s)),
        "\n".join(ks.card_rows("Plan Q3 roadmap", "--", ks["dim"], 80, 1,
                               False, dict(calm_meta_s, days=None))),
        "\n".join(ks.card_rows("Ship the docs", "done", ks["dim"], 80, 2,
                               False, dict(calm_meta_s, done=True))),
        ks.tile_row("  4", "work in flight", ks["ink"], 24),
        ks.meter(6, 10, [4, 0, 2, 2], 44),
        ks.bar(11, None, None),
        "\n".join(ks.sect("AGENDA", "12 open", 50, 20)),
        ks.cal_cell("none") + ks.cal_cell("one") + ks.cal_cell("multi"),
        ks.queue_marker(2),
        " ".join(ks.icon(i) for i in ("deadline", "wip", "blocked", "workday")),
        "\n".join(ks.wordmark("TB")),
        ks.spark([1, 3, 2, 5], 4),
        "\n".join(ks.plot([2, 5, 3, 7], 16, 4)),
    ])
    check("solari: a CALM page carries ZERO amber (the ration)",
          AMBER not in calm_page)
    check("solari: a calm page carries ZERO red either",
          RED not in calm_page)
    flight = "\n".join(ks.card_rows("Renew TLS certificate", "3d", ks["warn"],
                                    80, 0, False, dict(calm_meta_s, days=3)))
    check("solari: a value IN FLIGHT is amber (BOARDING)",
          AMBER in flight and "BOARDING" in grey(flight))
    late = "\n".join(ks.card_rows("Fix checkout 500", "2d!", ks["alert"], 80,
                                  0, True, dict(calm_meta_s, days=-2)))
    check("solari: LATE is the RED, and it says so in a word too",
          RED in late and "LATE" in grey(late))
    check("solari: LATE is never amber and BOARDING is never red",
          AMBER not in late and RED not in flight)
    # ... and severity is the FACE, not the ink — the decision that made the
    # selection band legible. A bare `[#f5a300]` tag anywhere on a schedule
    # row is the regression this pins.
    check("solari: severity is the CELL FACE, never the ink",
          f"on {AMBER}" in flight and f"[{AMBER}]" not in flight
          and f"on {RED}" in late and f"[{RED}]" not in late)
    every_state = "".join(
        "".join(ks.card_rows("Renew TLS certificate", ch, ks["mut"], 80, 0,
                             False, calm_meta_s))
        for ch in ("12d", "3d", "2d!", "blk", "done", "--"))
    check("solari: NO schedule row prints a loud FOREGROUND in any state "
          "(every glyph is ink · mut · dim · ground)",
          f"[{AMBER}]" not in every_state and f"[{RED}]" not in every_state)
    for chip, word in (("done", "DEPARTED"), ("blk", "HELD"), ("--", "OPEN"),
                       ("12d", "ON TIME"), ("3d", "BOARDING"),
                       ("2d!", "LATE")):
        row = grey(ks.card_rows("Renew TLS certificate", chip, ks["mut"], 80,
                                0, False, calm_meta_s)[0])
        check(f"solari: chip {chip!r} states the status word {word!r}",
              word in row, repr(row[-24:]))
    check("solari: RED reaches exactly ONE icon (overdue) and no other",
          RED in ks.icon("overdue")
          and all(RED not in ks.icon(i) for i in
                  ("deadline", "wip", "blocked", "workday", "boardfile")))
    check("solari: AMBER is spent on interaction — the selected tab and the "
          "slider knob",
          AMBER in ks.slider(4, 0, 10, 10)
          and AMBER in TH.tcss("solari") + ks.tcss())

    # -- THE ODOMETER: clipped, never clamped, and zero-padded --------------
    fills = {ks._due(d) for d in range(0, 100)}
    check("solari: the DUE field is zero-padded and tabular (always 2 cells)",
          all(len(f) == LG.Solari.DUE_W for f in fills)
          and ks._due(3) == "03")
    check("solari: past its range DUE is CLIPPED, never clamped ('9+' is a "
          "form the normal fill never emits)",
          ks._due(140) == "9+" and "9+" not in fills)
    check("solari: an undated row reads as absent, not as zero",
          ks._due(None) == "--" and ks._due(0) == "00")
    check("solari: the overdue MAGNITUDE is stated (the sign rides the word)",
          ks._due(-2) == "02")
    check("solari: the odometer meter is dispatched on the token, not the "
          "class", "odometer" in LG.METERS
          and TH.THEMES["solari"]["meter"] == "odometer")

    # -- DISPATCH: everything above is the `layout` token, not the class ----
    old_layout = TH.THEMES["solari"]["layout"]
    TH.THEMES["solari"]["layout"] = "flow"
    try:
        kf = LG.kit("solari")
        flow_rows = kf.card_rows("Renew TLS certificate", "9d", kf["mut"], 80,
                                 0, False, calm_meta_s)
        base_rows = LG.Kit.card_rows(kf, "Renew TLS certificate", "9d",
                                     kf["mut"], 80, 0, False, calm_meta_s)
        check("solari.layout=flow gives back the GENERIC composition, byte "
              "for byte", flow_rows == base_rows)
        check("solari.layout=flow drops the seam with it",
              SEAM not in "".join(grey(r) for r in flow_rows))
        check("solari.layout=flow gives up the sections board too",
              kf.board_layout() == "columns")
    finally:
        TH.THEMES["solari"]["layout"] = old_layout
    for name in TH.ORDER:
        k = LG.kit(name)
        rows = k.card_rows("Shut down legacy servers", "8d", k["mut"], 60, 0,
                           False, META_A)
        check(f"{name}: the seam grid renders IFF layout=schedule",
              any(set(grey(r)) == {SEAM} for r in rows)
              == (TH.THEMES[name].get("layout") == "schedule"))

    print("\n== KIT LEVEL: blueprint — the frame MEASURES, and nothing is boxed")
    kb = LG.kit("blueprint")
    BP = LG.Blueprint
    HATCH = TH.THEMES["blueprint"]["hatch"]
    INK_B = TH.THEMES["blueprint"]["ink"]
    GND_B = TH.THEMES["blueprint"]["ground"]
    ALERT_B = TH.THEMES["blueprint"]["alert"]
    MODES = ["board", "lanes", "agenda", "gantt"]
    bp_meta = {"proj": "API Platform", "phase": "Backlog", "prio": "high",
               "days": 3, "blocked": False, "done": False}

    # THE VOCABULARY, declared precisely so "no containing boxes" is a
    # MEASUREMENT and not an impression. Every box-drawing codepoint is in
    # scope; this language is allowed exactly ten of them — the extension line
    # at two weights, the two dimension terminators, the clip BREAK, the four
    # registration corners and the hatch. None of the ten is a vertical run and
    # none is a junction, and a rectangle needs one or the other, so a
    # containing box here is not merely absent: it is unconstructable.
    BOXCHARS = {chr(c) for c in range(0x2500, 0x2580)} | set("▏▕│┃║╎┆┊")
    BP_OK = ({BP.EXT, "━", BP.OPEN, BP.CLOSE, BP.BREAK, HATCH}
             | set(BP.REG))
    check("blueprint: the allowed vocabulary is TEN glyphs, none of them a "
          "vertical or a junction (the law, stated before it is used)",
          len(BP_OK) == 10
          and not (BP_OK & set("│┃║╎┆┊▏▕┼┬┴╪╫╬┤├".replace("┤", "")
                               .replace("├", ""))),
          f"{sorted(BP_OK)}")

    def bp_sheet(w: int) -> str:
        """Every surface the SHEET draws at width `w`, colour stripped."""
        parts = [kb.head("Backlog", 7, w, 0), kb.head("Done", 0, w, 3)]
        for chip, m in (("3d", bp_meta), ("9d", bp_meta),
                        ("2d!", dict(bp_meta, days=-2)),
                        ("blk", dict(bp_meta, blocked=True)),
                        ("done", dict(bp_meta, done=True)),
                        ("--", dict(bp_meta, days=None)),
                        ("40d", dict(bp_meta, days=40))):
            parts += kb.card_rows("Renew TLS certificate", chip, kb["mut"], w,
                                  0, False, m)
        parts += kb.sect("AGENDA", "12 open", w, 20)
        parts.append(kb.meter(4, 15, [7, 6, 2], w))
        parts.append(kb.bar(9, None, None))
        parts.append(kb.tile_row(" 12", "overdue", kb["alert"], min(w, 24)))
        parts += [kb.cal_cell(x) for x in ("none", "over", "multi", "one")]
        parts.append(kb.queue_marker(2))
        parts += kb.title_block(MODES, "board", w)
        parts.append(kb.spark([1, 3, 2, 5, 4, 6, 2, 7], 8))
        parts += kb.plot([2, 5, 3, 7, 4, 8, 6, 9], 24, 4)
        parts.append(kb.gauge(7, 0, 10, 10, thr=3))
        return "\n".join(grey(p) for p in parts)

    for w in (118, 80, 60, 44, 38, 28, 20):
        page = bp_sheet(w)
        stray = sorted({ch for ch in page if ch in BOXCHARS} - BP_OK)
        check(f"blueprint @{w}: not one box-drawing glyph outside the declared "
              f"vocabulary (no vertical, no junction, no box)",
              not stray, f"stray={stray}")
    check("blueprint: that scan CAN fail — the same predicate names glyphs on "
          "every other language's sheet (negative control)",
          any(({ch for ch in "\n".join(
              [grey(LG.kit(n).head("Backlog", 7, 80, 0))]
              + [grey(r) for r in LG.kit(n).card_rows(
                  "Renew TLS certificate", "3d", LG.kit(n)["mut"], 80, 0,
                  False, bp_meta)])
               if ch in BOXCHARS} - BP_OK)
              for n in TH.ORDER if n != "blueprint"))
    # ... and the vocabulary is really USED, or the scan above is vacuous
    used = {ch for ch in bp_sheet(118) if ch in BOXCHARS}
    check("blueprint: the sheet really draws spans and registration marks "
          "(probe self-check — the box scan is not vacuous)",
          {BP.OPEN, BP.CLOSE, BP.EXT} <= used and set(BP.REG) & used,
          f"{sorted(used)}")

    # -- THE DIMENSION SPAN: it MEASURES ------------------------------------
    def bp_span(days, chip=None, w=110):
        """The span field of one card row, read off the RENDER."""
        m = dict(bp_meta, days=days)
        c = chip if chip is not None else (
            "--" if days is None else f"{days}d" if days >= 0
            else f"{-days}d!")
        row = grey(kb.card_rows("Renew TLS certificate", c, kb["mut"], w, 0,
                                False, m)[0])
        x = first_of(o for o, code, _ in kb.field(w) if code == "span")
        return row[x:].rstrip() if x >= 0 else ""

    def bp_len(s: str) -> int:
        """The span's EXTENT in cells — terminator to terminator. Measured off
        the render rather than recomputed from `_cells`, so the seat and the
        drawing can disagree and be caught.

        -1 WHEN A TERMINATOR IS MISSING, never a raise: mutant M3a renamed
        blueprint's span field code, this helper's `.index` raised, and the
        run died at 8598 checks having reported ZERO reds — the sixty-sixth
        pass's own sweep had missed it because it read assignments and not
        RETURNS."""
        i, j = at(s, BP.OPEN), at(s, BP.CLOSE)
        return j - i + 1 if 0 <= i < j else -1

    lens = {d: bp_len(bp_span(d)) for d in (0, 1, 3, 6, 9, 14)}
    check("blueprint: the span LENGTH is the measurement (it grows with the "
          "days, monotonically)",
          all(lens[a] <= lens[b] for a, b in
              ((0, 1), (1, 3), (3, 6), (6, 9), (9, 14)))
          and lens[0] < lens[14], f"{lens}")
    check("blueprint: MICROBAR FLOOR — one day is not zero days, and neither "
          "is absence (three distinguishable readings)",
          len({bp_span(0), bp_span(1), bp_span(None)}) == 3,
          f"{[bp_span(0), bp_span(1), bp_span(None)]}")
    check("blueprint: the figure RIDES ON the span when the run affords it",
          bp_span(9).startswith(f"{BP.OPEN}{BP.EXT}")
          and "09D" in bp_span(9).split(BP.CLOSE)[0],
          repr(bp_span(9)))
    check("blueprint: and steps OUTSIDE it when it does not — the draftsman's "
          "rule, not an ellipsis",
          # SENTINEL "": THIS IS WHERE MUTANT M3a DIED. `[1]` on a split
          # asserts the terminator is PRESENT, which is precisely what the
          # mutant removes — rename the span field code and `bp_span(1)`
          # comes back without a CLOSE, the split is one element long, and
          # the run ended at 8598 checks having reported three reds and no
          # verdict line. "" reds the equality against "01D" and the detail
          # prints the span that had no terminator, which is the diagnosis.
          nth(bp_span(1).split(BP.CLOSE), 1, "").strip() == "01D",
          repr(bp_span(1)))
    # THE SHARED SCALE. The ceiling is a CONSTANT, so the same quantity draws
    # the same length at every width — which is the whole content of DATAVIZ
    # law 2 for a mechanism whose caller cannot pass a `hi`.
    check("blueprint: the day scale is SHARED — one quantity, one length, at "
          "every width (DATAVIZ law 2, by construction)",
          len({bp_span(9, w=w) for w in (118, 96, 60, 44, 38)}) == 1,
          f"{sorted({bp_span(9, w=w) for w in (118, 96, 60, 44, 38)})}")
    check("blueprint: the scale is DECLARED, not tabulated (the constant is "
          "what the spans read)",
          BP.SCALE_DAYS == 14 and BP.SCALE_COUNT == 12 and BP.SPAN_W == 16)
    # CLIP AND FLAG, never clamp
    check("blueprint: past its scale a span is CLIPPED and FLAGGED — the run "
          "stops, the BREAK says so, and the figure stays the truth",
          BP.BREAK in bp_span(40) and BP.BREAK in bp_span(90)
          and BP.BREAK not in bp_span(9)
          and "40D" in bp_span(40) and "90D" in bp_span(90),
          f"{bp_span(40)!r} / {bp_span(90)!r}")
    check("blueprint: a clipped span is never printed as a near one (the two "
          "clipped lengths agree, their figures do not)",
          len(bp_span(40)) == len(bp_span(90)) and bp_span(40) != bp_span(90))
    check("blueprint: the figure itself clips rather than overflowing its "
          "field", BP._fig(140) == "99+" and BP._fig(9) == "09")
    # GREYSCALE: every reading above survives the colour being stripped, which
    # is the only channel the terminal is guaranteed to keep
    check("blueprint: the whole span mechanism reads in GREYSCALE (shape, "
          "never hue)",
          len({bp_span(d) for d in (0, 1, 3, 9, 14, 40)}) == 6)

    # -- HATCH: held is a TEXTURE, and it is the token's -----------------------
    held = grey(kb.card_rows("Fix checkout 500", "blk", kb["alert"], 110, 0,
                             True, dict(bp_meta, blocked=True))[0])
    open_ = grey(kb.card_rows("Fix checkout 500", "9d", kb["mut"], 110, 0,
                              False, bp_meta)[0])
    check("blueprint: a HELD item's span is hatched", HATCH in held
          and "HELD" in held)
    check("blueprint: an unblocked item's span carries no hatch at all",
          HATCH not in open_)
    check("blueprint: the hatch is a SHAPE — held and open differ with the "
          "colour stripped away", held != open_)
    old_h = TH.THEMES["blueprint"]["hatch"]
    TH.THEMES["blueprint"]["hatch"] = "╲"
    try:
        kh = LG.kit("blueprint")
        held2 = grey(kh.card_rows("Fix checkout 500", "blk", kh["alert"], 110,
                                  0, True, dict(bp_meta, blocked=True))[0])
        check("blueprint: the hatch GLYPH is the token's (mutation reaches "
              "the span and the icon)",
              "╲" in held2 and HATCH not in held2
              and "╲" in grey(kh.icon("blocked")))
    finally:
        TH.THEMES["blueprint"]["hatch"] = old_h

    # -- ALERT: overdue and nothing else --------------------------------------
    calm_page_b = "\n".join([
        kb.head("Backlog", 7, 110, 0),
        "\n".join(kb.card_rows("Renew TLS certificate", "9d", kb["mut"], 110,
                               0, False, bp_meta)),
        "\n".join(kb.card_rows("Plan Q3 roadmap", "--", kb["dim"], 110, 1,
                               False, dict(bp_meta, days=None))),
        "\n".join(kb.card_rows("Fix checkout 500", "blk", kb["alert"], 110, 2,
                               True, dict(bp_meta, blocked=True))),
        "\n".join(kb.card_rows("Ship the docs", "done", kb["dim"], 110, 3,
                               False, dict(bp_meta, done=True))),
        "\n".join(kb.card_rows("Design homepage", "3d", kb["warn"], 110, 4,
                               True, dict(bp_meta, days=3))),
        kb.meter(4, 15, [7, 6, 2], 110),
        kb.bar(9, None, None),
        "\n".join(kb.sect("AGENDA", "12 open", 60, 20)),
        kb.cal_cell("none") + kb.cal_cell("one") + kb.cal_cell("multi"),
        kb.queue_marker(2),
        "\n".join(kb.title_block(MODES, "board", 110)),
        " ".join(kb.icon(i) for i in ("deadline", "wip", "blocked", "workday")),
    ])
    check("blueprint: a CALM sheet carries ZERO alert — including a HELD row, "
          "which is the one this ration exists to keep grey",
          ALERT_B not in calm_page_b)
    late_b = "\n".join(kb.card_rows("Fix the wrapped frame", "2d!",
                                    kb["alert"], 110, 0, True,
                                    dict(bp_meta, days=-2)))
    check("blueprint: an OVERDUE span is the alert, and it says so in a figure "
          "too", ALERT_B in late_b and "02D!" in grey(late_b))
    # THE RATION, TAKEN LITERALLY, and the render is what forced it: an icon is
    # a LABEL, and the `overdue` code captions a tile whose count may be zero.
    # A red `OVR` beside `0` was the ONLY alert cell on the calm board — the
    # hue meaning "this word is about lateness" rather than "this thing is
    # late". No icon is alert now; the span of a genuinely late row is.
    check("blueprint: NOT ONE icon is alert — a label is not a datum",
          all(ALERT_B not in kb.icon(i) for i in
              ("deadline", "overdue", "wip", "blocked", "workday",
               "boardfile")))
    check("blueprint: ... and the hue is not simply unused — a span past its "
          "date wears it (negative control for the check above)",
          ALERT_B in late_b)
    # THE TWO-CHANNEL LAW on the one seat too narrow for a span. The render at
    # 60 caught the draft where `over` and `multi` were the same glyph pair in
    # different hues — a state readable in colour alone (COMPONENTS.md).
    cals = {s: grey(kb.cal_cell(s)) for s in ("none", "one", "multi", "over")}
    check("blueprint: all four calendar states differ in SHAPE, not only in "
          "hue (a two-cell seat is still two channels)",
          len(set(cals.values())) == 4, f"{cals}")
    check("blueprint: ... and every one of them stays inside the declared "
          "vocabulary",
          not ({ch for ch in "".join(cals.values()) if ch in BOXCHARS}
               - BP_OK))

    # -- THE KNOCKOUT: exactly one, and it is the first fixation ---------------
    def knock_runs(rows: list[str]) -> int:
        """Reversed cell RUNS in the markup — `[ground on ink]` is the whole
        mechanism, so counting the tag counts the knockouts."""
        return "\n".join(rows).count(f"[{GND_B} on {INK_B}]")

    for mood, want in (("clear", 0), ("busy", 0), ("alert", 1)):
        kb.mood = mood
        tb = kb.title_block(MODES, "board", 110)
        check(f"blueprint: mood={mood!r} puts exactly {want} knockout on the "
              f"view", knock_runs(tb) == want, f"{knock_runs(tb)}")
        check(f"blueprint: ... and the sheet still STATES its condition at "
              f"mood={mood!r}",
              BP.STATE[mood] in grey("\n".join(tb)))
    kb.mood = "alert"
    tb_alert = kb.title_block(MODES, "board", 110)
    check("blueprint: the knockout is the STATE cell and it is DIMENSIONED — "
          "two channels, so it survives greyscale as well as attention",
          f"[{GND_B} on {INK_B}]" in "\n".join(tb_alert)
          and f"{BP.OPEN} OVERDUE {BP.CLOSE}" in grey("\n".join(tb_alert)))
    kb.mood = "clear"
    calm_ref = grey("\n".join(kb.title_block(MODES, "board", 110)))
    kb.mood = "alert"
    old_k = TH.THEMES["blueprint"]["knockout"]
    TH.THEMES["blueprint"]["knockout"] = False
    try:
        kk2 = LG.kit("blueprint")
        kk2.mood = "alert"
        tb_off = kk2.title_block(MODES, "board", 110)
        check("blueprint.knockout=False removes the reverse video AND the "
              "dimension (the token owns both channels — mutation-tested at "
              "the mood the generic ALT loop cannot reach)",
              knock_runs(tb_off) == 0
              and f"{BP.OPEN} OVERDUE {BP.CLOSE}" not in grey("\n".join(tb_off))
              and "OVERDUE" in grey("\n".join(tb_off)))
        kk2.mood = "clear"
        check("blueprint.knockout=False is live at a CALM mood too (which is "
              "what keeps it out of dead metadata in `kit_sig`, where every "
              "kit is fresh and every mood is 'clear')",
              grey("\n".join(kk2.title_block(MODES, "board", 110)))
              != calm_ref)
    finally:
        TH.THEMES["blueprint"]["knockout"] = old_k
    kb.mood = "clear"

    # -- REGISTRATION: corners, never a border --------------------------------
    for active in MODES:
        tb = [grey(r) for r in kb.title_block(MODES, active, 110)]
        marks = [(i, x) for i, r in enumerate(tb)
                 for x, ch in enumerate(r) if ch in BP.REG]
        check(f"blueprint: the mode on screen ({active}) is marked by FOUR "
              f"registration corners, one of each",
              len(marks) == 4
              and {tb[i][x] for i, x in marks} == set(BP.REG),
              f"{marks}")
        xs = sorted({x for _, x in marks})
        # THE ONE SITE IN THIS CLASS WHERE NO SENTINEL CAN WORK, and it is
        # the reason `nth` is a seat and not a law. The second check is a
        # NEGATIVE claim — "the cells between the corners are blank" — so an
        # empty slice SATISFIES it. Any sentinel that keeps the run alive
        # (0, -1, len(tb[0])) hands it an empty or reversed span and it
        # passes VACUOUSLY on the exact input it exists to refuse: a title
        # block that drew no corners at all. A cure that turns a crash into
        # a silent green has moved the defect, not fixed it.
        #
        # So this pair carries the explicit leg instead. `len(xs) == 2` is
        # what the first law already says out loud; the second one was
        # BORROWING it through the loop and is now made to say it itself,
        # which is also what makes the two independent. The DETAIL is the
        # `nth` half: it is evaluated on every call, pass or fail, so it
        # needs to survive the empty case that the condition reds on.
        x0, x1 = nth(xs, 0, 0), nth(xs, 1, 0)
        check(f"blueprint: ... and they BRACKET the active word ({active}), "
              f"never touch it", len(xs) == 2
              and tb[1][x0 + 1: x1].strip() == active.upper(),
              f"{tb[1][x0: x1 + 1]!r}  ({len(xs)} corner column(s))")
        check(f"blueprint: ... and nothing joins them into a box ({active}) — "
              f"the cells between the corners are blank on both rows",
              len(xs) == 2
              and not tb[0][x0 + 1: x1].strip()
              and not tb[2][x0 + 1: x1].strip(),
              f"{len(xs)} corner column(s)")
    check("blueprint: the marks MOVE with the selection (they are the "
          "selection, not decoration)",
          {tuple(sorted({x for r in [grey(z) for z in
                                     kb.title_block(MODES, a, 110)]
                         for x, ch in enumerate(r) if ch in BP.REG}))
           for a in MODES}.__len__() == 4)
    check("blueprint: selection spends NO border (`sel` is emitted verbatim "
          "as a Textual border style, and a registration mark is not one)",
          TH.THEMES["blueprint"]["sel"] == "none"
          and "border" not in LG.kit("blueprint").composition())

    # -- ONE GEOMETRY SEAT, and its declared degrade --------------------------
    BP_LADDER = [(118, ["item", "span"]), (38, ["item", "span"]),
                 (37, ["item"]), (20, ["item"]), (19, [])]
    for w, want in BP_LADDER:
        got = [c for _, c, _ in kb.field(w)]
        check(f"blueprint @{w}: the field seat buys exactly {want}",
              got == want, f"{got}")
    check("blueprint: the drop rule is DERIVED from the declared floors, not "
          "tabulated",
          BP.ITEM_MIN + BP.GAP + BP.SPAN_W == 38 and BP.ITEM_MIN == 20)
    for w, _ in BP_LADDER:
        fs = kb.field(w)
        if not fs:
            continue
        check(f"blueprint @{w}: the fields fill the measure exactly",
              fs[-1][0] + fs[-1][2] == w)
        rows = kb.card_rows("Renew TLS certificate", "9d", kb["mut"], w, 0,
                            False, bp_meta)
        check(f"blueprint @{w}: nothing wraps (every row is <= {w} cells)",
              all(len(grey(r)) <= w and "\n" not in r for r in rows),
              f"{[len(grey(r)) for r in rows]}")
        check(f"blueprint @{w}: the head fills the measure exactly too",
              len(grey(kb.head("Backlog", 7, w, 0))) == w)
    check("blueprint: when the DIMENSION is renounced the READING is not — it "
          "moves onto the extension leader",
          "09D" in grey(kb.card_rows("Renew TLS certificate", "9d", kb["mut"],
                                     30, 0, False, bp_meta)[1]))
    check("blueprint: ... and the head keeps its count too (an empty phase "
          "still reads 00)",
          grey(kb.head("Done", 0, 30, 3)).rstrip().endswith("00")
          and grey(kb.head("Backlog", 7, 30, 0)).rstrip().endswith("07"))
    check("blueprint: below the item floor the sheet is RENOUNCED, not "
          "crushed", kb.field(19) == [] and kb.field(20) != [])
    narrow_b = kb.card_rows("Renew TLS certificate", "9d", kb["mut"], 19, 0,
                            False, bp_meta)
    check("blueprint: and the renounced form is the GENERIC card, byte for "
          "byte (it can never be worse than what it replaced)",
          narrow_b == LG.Kit.card_rows(kb, "Renew TLS certificate", "9d",
                                       kb["mut"], 19, 0, False, bp_meta))
    # the head's span and the items' spans stand on ONE origin — the seat is
    # shared, which is what makes the page read as one drawing
    for w in (118, 80, 60, 44, 38):
        hx = at(grey(kb.head("Backlog", 7, w, 0)), BP.OPEN)
        cx = at(grey(kb.card_rows("Renew TLS certificate", "9d", kb["mut"],
                                  w, 0, False, bp_meta)[0]), BP.OPEN)
        seat = first_of(o for o, c, _ in kb.field(w) if c == "span")
        check(f"blueprint @{w}: head span and item span stand on the SEAT's "
              f"own origin (one geometry seat, not two)",
              hx >= 0 and hx == cx == seat, f"head@{hx} item@{cx} seat@{seat}")

    # -- THE TITLE BLOCK, and its declared ladder ------------------------------
    TB_LADDER = [(114, 4), (76, 3), (56, 2), (42, 1)]
    for w, want in TB_LADDER:
        kb._sheet = (4, 15, w)
        cells = kb.block_cells(w, len(kb._mode_strip(MODES, "board")[0]))
        rows = kb.title_block(MODES, "board", w)
        check(f"blueprint titleblock @{w}: the declared drop order buys "
              f"exactly {want} cell(s)", len(cells) == want,
              f"{[cap or val.strip() for cap, val, _ in cells]}")
        check(f"blueprint titleblock @{w}: exactly {BP.TB_ROWS} rows, each "
              f"exactly {w} cells (it can never wrap its seat)",
              len(rows) == BP.TB_ROWS
              and {len(grey(r)) for r in rows} == {w},
              f"{[len(grey(r)) for r in rows]}")
        check(f"blueprint titleblock @{w}: the STATE cell never drops (it is "
              f"the knockout)", cells[-1][0] == "" and cells[-1][1].strip())
    check("blueprint: the title block's drop order is DECLARED",
          BP.TB_DROP == ("sheet", "rev", "work"))
    kb._sheet = (4, 15, 114)
    tb114 = [grey(r) for r in kb.title_block(MODES, "board", 114)]
    check("blueprint: the block's cells carry REAL board data (the tally the "
          "meter handed it, and today's revision date)",
          "04/15" in tb114[1] and date.today().isoformat() in tb114[1]
          and BP.SHEET in tb114[1])
    check("blueprint: ... and it says so honestly before the meter has run "
          "(`--/--`, never a stale figure)",
          "--/--" in grey(LG.kit("blueprint").title_block(MODES, "board",
                                                          114)[1]))
    kb2 = LG.kit("blueprint")
    kb2.meter(9, 15, [7, 6, 2], 114)
    check("blueprint: the WORK cell follows the METER call that fills it (the "
          "one seat handed the board's whole tally)",
          "09/15" in grey(kb2.title_block(MODES, "board", 114)[1]))
    check("blueprint: the block's two rules bracket the cells and stop where "
          "they start (one stroke above, one below, nothing vertical)",
          set(tb114[0]) - {" "} == {BP.EXT, BP.REG[0], BP.REG[1]}
          and set(tb114[2]) - {" "} == {BP.EXT, BP.REG[2], BP.REG[3]}
          and at(tb114[0], BP.EXT) >= 0
          and at(tb114[0], BP.EXT) == at(tb114[2], BP.EXT))

    # -- the meter is a DIMENSION, and it states its value ---------------------
    mtr = grey(kb.meter(4, 15, [7, 6, 2], 110)).split("\n")
    check("blueprint: the meter MEASURES with a span and STATES its figure",
          mtr[0].count(BP.OPEN) == 1 and "04/15" in mtr[0] and "27%" in mtr[0])
    check("blueprint: the meter's load row dimensions every phase, and every "
          "phase keeps its figure (DATAVIZ law 5)",
          all(f"{n:02d}" in mtr[1] for n in (7, 6, 2)))
    check("blueprint: the meter draws no fill at all (not one block glyph)",
          not any(ch in "█▓▒░▄▀▌▐▬" for ch in "\n".join(mtr)))
    check("blueprint: the dimension meter is dispatched on the TOKEN, not the "
          "class", "dimension" in LG.METERS
          and TH.THEMES["blueprint"]["meter"] == "dimension")

    # -- DISPATCH: everything above is the `layout`/`frame` tokens -------------
    old_bl = TH.THEMES["blueprint"]["layout"]
    TH.THEMES["blueprint"]["layout"] = "flow"
    try:
        kfb = LG.kit("blueprint")
        flow_rows = kfb.card_rows("Renew TLS certificate", "9d", kfb["mut"],
                                  110, 0, False, bp_meta)
        base_rows = LG.Kit.card_rows(kfb, "Renew TLS certificate", "9d",
                                     kfb["mut"], 110, 0, False, bp_meta)
        check("blueprint.layout=flow gives back the GENERIC composition, byte "
              "for byte", flow_rows == base_rows)
        check("blueprint.layout=flow drops the dimension span with it",
              BP.OPEN not in "".join(grey(r) for r in flow_rows))
        check("blueprint.layout=flow gives up the sections board too",
              kfb.board_layout() == "columns")
    finally:
        TH.THEMES["blueprint"]["layout"] = old_bl
    old_bf = TH.THEMES["blueprint"]["frame"]
    TH.THEMES["blueprint"]["frame"] = "double"
    try:
        kfr = LG.kit("blueprint")
        check("blueprint.frame=double gives the title block's seat back to "
              "the generic tab strip",
              kfr.tabs(MODES, "board") == LG.Kit.tabs(kfr, MODES, "board"))
        check("blueprint.frame=double gives the generic COMPOSITION back too "
              "(the dock is the block's seat — the token owns both, or half "
              "of it is dead metadata)",
              kfr.composition() == LG.Kit.composition(kfr)
              and "dock" not in kfr.tcss())
    finally:
        TH.THEMES["blueprint"]["frame"] = old_bf
    for name in TH.ORDER:
        k = LG.kit(name)
        rows = (k.card_rows("Shut down legacy servers", "8d", k["mut"], 60, 0,
                            False, META_A) + [k.head("BACKLOG", 5, 60, 0)])
        has_span = any(BP.OPEN in grey(r) and BP.CLOSE in grey(r)
                       for r in rows)
        check(f"{name}: dimension spans render IFF layout=field",
              has_span == (TH.THEMES[name].get("layout") == "field"))

    print("\n== KIT LEVEL: display typography (axis 3) — drawn vs renounced")
    DRAWERS = {"naught": 5, "instrument": 3}   # min drawn rows
    for name in TH.ORDER:
        k = LG.kit(name)
        short = "\n".join(grey(r) for r in k.sect("AGENDA", "12 open", 50, 0))
        tall = "\n".join(grey(r) for r in k.sect("AGENDA", "12 open", 50, 20))
        if name in DRAWERS:
            check(f"{name}: tall surfaces draw the title "
                  f"(>= {DRAWERS[name]} rows)",
                  tall.count("\n") + 1 >= DRAWERS[name])
            check(f"{name}: display type is progressive (short form differs)",
                  tall != short)
        else:
            check(f"{name}: drawn display type renounced (h changes nothing)",
                  tall == short)
    drawn = {n: "\n".join(grey(r)
                          for r in LG.kit(n).sect("AGENDA", "12 open", 50, 20))
             for n in DRAWERS}
    check("each drawing language has its own mechanism",
          len(set(drawn.values())) == len(DRAWERS))

    print("\n== KIT LEVEL: mutate every declared structural token")
    for name in TH.ORDER:
        t = TH.THEMES[name]
        for tok, alt in ALT.items():
            if tok not in t:
                continue
            before = mut_sig(name)
            old = t[tok]
            t[tok] = alt(old)
            try:
                changed = mut_sig(name) != before
            finally:
                t[tok] = old
            check(f"{name}.{tok} is live ({old!r} -> mutated)", changed)
            check(f"{name}.{tok} restores cleanly", mut_sig(name) == before)

    # THE FIXTURE, seeded once for every app-level capture below. Board.load
    # seeds deterministic demo tasks on a missing path (models.seed_data,
    # today-anchored). It is created HERE, before the first capture, because
    # the alternative is the user's live board.json — which the desktop app
    # rewrites underneath a running suite, making every app-level comparison
    # a race. That race is the standing suspect for the intermittent
    # legibility reds (PENDING: darkside capture-race watch).
    fx = W / "prototypes" / "out" / "_fixture_board.json"
    fx.parent.mkdir(exist_ok=True)
    if fx.exists():
        fx.unlink()                        # force a fresh, today-anchored seed

    print("\n== APP LEVEL: THE ONE MEASURE — head, card and empty seat agree")
    # PENDING item 4, cured at the source and asserted on the COMPOSITOR, not
    # on the arithmetic that produced it. Two independent facts per language
    # and per width, both read off the live widget tree:
    #
    #   ORIGIN — `.col-head` and `.kb-card` open their content on the SAME
    #            screen column. That is what `.col-head { padding-left: 1 }`
    #            buys, and six languages used to fake it (or not) one at a
    #            time: instrument's HEAD_PAD, industrial's and swiss's leading
    #            markup cell, darkside's and ledger's own TCSS copies.
    #   MEASURE — the number `row_width` hands the head, re-derived from the
    #            head's OWN seat, is the number the card draws into. This
    #            fails the moment a language restyles either seat: it compares
    #            what Textual actually gave the card against what the law
    #            predicts from the head beside it.
    #
    # Together they pin both edges. Before the cure the closing edges agreed
    # only by arithmetic luck (110 cells drawn from x, 109 from x + 1) and the
    # opening edges did not agree at all.
    import kanban as KB                                          # noqa: E402
    from kanban import TaskCard                                  # noqa: E402

    async def seats(name, size):
        """(head content x, card content x, row width the law hands the head,
        row width the card actually draws) — off a settled render."""
        from app import TaskboardWidget
        from textual.widgets import Static
        app = TaskboardWidget(board_path=str(fx))
        async with app.run_test(size=size) as pilot:
            await pilot.pause()
            app.notify = lambda *a, **kw: None
            app.set_theme(name)
            await pilot.pause()
            app.redraw()
            await settle(app, pilot, f"seats {name} @{size[0]}")
            hd = next((s for s in app.query(Static) if s.has_class("col-head")),
                      None)
            cd = next(iter(app.query(TaskCard)), None)
            if hd is None or cd is None:
                return None
            return (hd.content_region.x, cd.content_region.x,
                    KB.row_width(hd.outer_size.width),
                    max(8, cd.size.width - KB.CARD_OWN))

    for name in TH.ORDER:
        for size in ((118, 30), (80, 30)):
            got = await seats(name, size)
            check(f"{name} @{size[0]}: the board mounts a head AND a card "
                  f"(probe self-check — no widgets, no law)", got is not None)
            if got is None:
                continue
            hx, cx, law, drawn = got
            check(f"{name} @{size[0]}: head and card OPEN on the same screen "
                  f"column", hx == cx, f"head x={hx} card x={cx}")
            check(f"{name} @{size[0]}: and the measure the head is handed is "
                  f"the one the card draws", law == drawn,
                  f"head {law} card {drawn}")

    print("\n== APP LEVEL: the item-0 boundary — board frame, HERO MASKED")
    boards, heroes, configs, geos = {}, {}, {}, {}
    for name in TH.ORDER:
        boards[name], heroes[name], configs[name], geos[name] = \
            await capture(name, board_path=str(fx))
    check("hero mask removed real content (probe self-check)",
          all(h.strip() for h in heroes.values()))
    # a permanent render dump, like ledger_{w}.txt: the lattice is a
    # composition, and a composition is judged by LOOKING at it
    (W / "prototypes" / "out" / "lattice_naught.txt").write_text(
        boards["naught"], encoding="utf-8")
    (W / "prototypes" / "out" / "panel_industrial_118.txt").write_text(
        boards["industrial"], encoding="utf-8")
    for i, a in enumerate(TH.ORDER):
        for b in TH.ORDER[i + 1:]:
            check(f"outside the hero, {a} != {b}", boards[a] != boards[b])

    print("\n== APP LEVEL: the CONFIG screen — controls, not colours")
    # the title may be letterspaced OR DRAWN (display type) — probe the hint
    # line instead, which every language prints as text
    check("config screen renders the controls (probe self-check)",
          all("space toggle" in cfg for cfg in configs.values()))
    for i, a in enumerate(TH.ORDER):
        for b in TH.ORDER[i + 1:]:
            check(f"config: {a} != {b}", configs[a] != configs[b])

    print("\n== APP LEVEL: COMPOSITION — layout geometry is per-language")
    hero_r = {n: g["#hero"] for n, g in geos.items()}
    check("region geometries are not one skeleton (>=5 distinct hero regions)",
          len(set(hero_r.values())) >= 5, f"{len(set(hero_r.values()))} distinct")
    check("naught: meter sits BESIDE the hero (widget grid)",
          geos["naught"]["#meter"][0] > geos["naught"]["#hero"][0]
          and geos["naught"]["#meter"][1]
          < geos["naught"]["#hero"][1] + geos["naught"]["#hero"][3])
    check("swiss: the ambient block keeps the editorial measure (hero <= 78)",
          geos["swiss"]["#hero"][2] <= 78, f"w={geos['swiss']['#hero'][2]}")
    check("industrial: compact readout (hero height <= 8)",
          geos["industrial"]["#hero"][3] <= 8, f"h={geos['industrial']['#hero'][3]}")
    check("instrument: symmetric inset (ap narrower than screen)",
          geos["instrument"]["#ap"][2] < 118)

    print("\n== APP LEVEL: the hero's dead columns carry the load plot")
    # same fixture as every capture above — seeded once at the top of the
    # app-level run and NOT re-seeded here: an unlink mid-suite would reset
    # state between captures, which is the very race this section relies on
    # not having
    for name in ("nord", "naught", "industrial"):
        _, fh, _, _ = await capture(name, board_path=str(fx))
        check(f"{name}: the load plot renders inside the hero (caption)",
              "LOAD" in fh and "8 WK" in fh)
    # LEGIBILITY is a law, not taste (user: darkside tasks were "casi
    # ilegible" at 6-columns-in-46): the sections board must show a long
    # title INTACT at board width (deterministic fixture, not the live board)
    db, _, _, _ = await capture("darkside", board_path=str(fx))
    check("darkside: sections board keeps titles legible (long title intact)",
          "shut down legacy servers" in db.lower())
    sb, _, _, _ = await capture("swiss", board_path=str(fx))
    # pitch=2 puts the 3rd card under the fold at 30 rows — legibility is
    # judged on what IS on screen: the first full title, intact
    check("swiss: sections board keeps titles legible (long title intact)",
          "Renew TLS certificate" in sb)

    print("\n== APP LEVEL: naught's LATTICE on the live board (`layout`)")
    LAT_TITLE = "Shut down legacy servers"

    def lat_rows(board: str) -> list[str]:
        return [r for r in body_rows(board) if LAT_TITLE in r]

    nb_rows = lat_rows(boards["naught"])
    check("naught: the fixture card is on screen (probe self-check)",
          len(nb_rows) == 1, f"{len(nb_rows)} row(s)")
    check("naught: the card row on the board wears its dot LEADERS",
          bool(nb_rows) and LG.NA.OFF * 2 in nb_rows[0])
    check("naught: the head's drawn count reaches the board (sprite rows)",
          sum(LG.NA.OFF in r or LG.NA.ON in r
              for r in body_rows(boards["naught"])) >= 6)

    # THE STROKE ON THE REAL BOARD — the seat the user actually reads. The
    # band is located by its caption row, not by "rows that look dotty":
    # the cards carry dots too (leaders, phase pips), and a probe that
    # cannot tell them apart would judge the wrong rows.
    def head_band(board: str) -> list[str]:
        rows = body_rows(board)
        i = next((j for j, r in enumerate(rows) if "BACKLOG" in r), -1)
        return [] if i < 0 else rows[i + 1: i + 1 + LG.NA.ALPHA_ROWS]

    def sprite_runs(band: list[str]) -> list[str]:
        return [m for r in band for m in re.findall(f"[{ON}{OFF}]+", r)]

    nb_band = head_band(boards["naught"])
    nb_runs = sprite_runs(nb_band)
    check("naught: the head band is on screen (probe self-check)",
          len(nb_band) == LG.NA.ALPHA_ROWS
          and all(ON in r or OFF in r for r in nb_band),
          f"{len(nb_band)} rows")
    check("naught: no one-cell stroke survives to the BOARD's head sprites",
          not THIN.search("\n".join(nb_band)))
    check("naught: the rendered head sprites are round dots only",
          set("".join(nb_runs)) == {ON, OFF})
    check("naught: each head sprite is one solid field (>= one x2 glyph, so "
          "no letter was drawn a cell at a time)",
          bool(nb_runs) and min(len(x) for x in nb_runs) >= 6,
          f"shortest run {min(len(x) for x in nb_runs) if nb_runs else 0}")
    check("naught: three columns head the board, one sprite each",
          len(nb_runs) == 3 * LG.NA.ALPHA_ROWS, f"{len(nb_runs)} sprite rows")
    # CARDS PER COLUMN IS UNCHANGED: the stroke widened the sprite, it did
    # not lengthen it. Measured two ways — the head still costs 6 rows
    # (caption + 5), and the third card still has its seat on the board.
    nrows = body_rows(boards["naught"])
    icap = first_of(i for i, r in enumerate(nrows) if "BACKLOG" in r)
    icard = first_of(i for i, r in enumerate(nrows) if "Renew TLS" in r)
    check("naught: the head costs the board 6 rows, exactly as before",
          icard - icap == 1 + LG.NA.ALPHA_ROWS, f"{icard - icap} rows")
    check("naught: the third card keeps its seat (cards per column unchanged)",
          len(nb_rows) == 1)
    # a NARROWER board is its own regime: one width hides a whole one
    nb80, _, _, _ = await capture("naught", board_path=str(fx), size=(80, 30))
    (W / "prototypes" / "out" / "lattice_naught_80.txt").write_text(
        nb80, encoding="utf-8")
    b80 = head_band(nb80)
    r80 = sprite_runs(b80)
    check("naught @80x30: the head band still renders (probe self-check)",
          len(b80) == LG.NA.ALPHA_ROWS)
    check("naught @80x30: the stroke holds in a narrow column",
          not THIN.search("\n".join(b80))
          and bool(r80) and min(len(x) for x in r80) >= 6)
    check("naught @80x30: three sprites, none run together (no overflow into "
          "the next column)",
          len(r80) == 3 * LG.NA.ALPHA_ROWS, f"{len(r80)} sprite rows")
    check("naught @80x30: the board still seats three cards per column",
          "Shut down legacy" in nb80)
    for name in TH.ORDER:
        if name == "naught":
            continue
        check(f"{name}: board carries no dot lattice (it is naught's)",
              LG.NA.OFF not in "\n".join(body_rows(boards[name]))
              and LG.NA.ON not in "\n".join(body_rows(boards[name])))
    # the lattice must DISPATCH: back to the base default and the composition
    # has to leave the REAL board, not merely the kit
    nf, _, _, _ = await capture("naught", mutate=("layout", "flow"),
                                board_path=str(fx))
    (W / "prototypes" / "out" / "lattice_naught_flow.txt").write_text(
        nf, encoding="utf-8")
    nf_rows = lat_rows(nf)
    check("naught.layout=flow keeps the board itself (probe self-check)",
          len(nf_rows) == 1, f"{len(nf_rows)} row(s)")
    check("naught.layout=flow strips the leaders from that same card row",
          bool(nf_rows) and LG.NA.OFF not in nf_rows[0])
    check("naught.layout=flow changes the board outside the hero",
          nf != boards["naught"])

    print("\n== APP LEVEL: the DENSE display type on the rendered hero")
    # `heroes[name]` holds FULL screen rows over the hero's band, so slice the
    # widget's own columns out of them — otherwise the meter that sits BESIDE
    # naught's hero would be judged as part of the glyph field.

    def hero_cells(name: str) -> list[str]:
        x, _, w, _ = (geos[name]["#hero"][0], 0, geos[name]["#hero"][2], 0)
        return [r[x: x + w] for r in heroes[name].split("\n")]

    def glyph_field(row: str) -> str:
        """One row's GLYPH FIELD: from its first dot to the load plot's
        2-cell gutter. The focus border (`sel="outer"`) sits to the left of
        it and the plot to the right; neither is display type, and the field
        itself never holds two spaces."""
        i = min([row.index(c) for c in (ON, OFF) if c in row] or [0])
        return row[i:].split("  ")[0]

    nh = [r for r in hero_cells("naught") if ON in r or OFF in r]
    (W / "prototypes" / "out" / "naught7_hero.txt").write_text(
        "\n".join(hero_cells("naught")), encoding="utf-8")
    check("naught: the hero renders its dot band (probe self-check)",
          len(nh) >= 7, f"{len(nh)} rows")
    nf_fields = [glyph_field(r) for r in nh]
    check("naught: the RENDERED glyph field carries no plain cell",
          all(f and " " not in f for f in nf_fields))
    check("naught: the rendered field is round dots only (∙ and ◦)",
          set("".join(nf_fields)) == {ON, OFF})
    check("naught: no one-cell stroke survives to the screen",
          not THIN.search("\n".join(nf_fields)))
    for name in TH.ORDER:
        if name == "naught":
            continue
        cells = "\n".join(hero_cells(name))
        check(f"{name}: its hero carries no naught fill (no lattice leak)",
              OFF not in cells and ON not in cells)
    # DISPATCH on the LIVE hero, not only in draw()
    # What the token owns, stated precisely: the DISPLAY TYPE — the full-bleed
    # field that reaches the hero's own left edge. It does NOT own the dots of
    # the dead-columns load plot on the right; those are the dotgrid METER's
    # mechanism, and they are asserted to STAY (the boundary `layout` draws).
    def dots_at_left(cells, margin=3):
        return any(any(c in row[:margin] for c in (ON, OFF)) for row in cells)

    check("naught7: the field is FULL-BLEED (it reaches the hero's left edge)",
          dots_at_left(hero_cells("naught")))
    _, hp, _, gp = await capture("naught", mutate=("hero", "plain"),
                                 board_path=str(fx))
    x, _, w, _ = gp["#hero"]
    hp_cells = [r[x: x + w] for r in hp.split("\n")]
    check("naught.hero=plain removes the display type from the live hero",
          not dots_at_left(hp_cells))
    check("naught.hero=plain keeps the load plot's dots (they answer to "
          "`meter`, not to `hero`)",
          any(ON in r for r in hp_cells))
    check("naught.hero=plain still paints a hero — it degrades, not dies",
          any(r.strip(" ▌▐") for r in hp_cells))

    print("\n== APP LEVEL (the SHIPPED aperture): slab on paper, flap on cards")
    # The one section that drives `taskboard/app.py` rather than the
    # widget-slice prototype, and it is not a preference: the prototype's Hero
    # forks the style dispatch, so `taskboard/hero.py` — the code the product
    # runs — has no other composited seat. A face is a GROUND, and only a
    # composited frame can say what ground a cell was painted on.
    ap_rows, ap_cells, ap_hero = await capture_ap_bg("solari", str(fx))
    (W / "prototypes" / "out" / "aperture_solari_hero.txt").write_text(
        "\n".join(r[ap_hero[0]: ap_hero[0] + ap_hero[2]]
                  for r in ap_rows[ap_hero[1]: ap_hero[1] + ap_hero[3]]),
        encoding="utf-8")
    S = TH.THEMES["solari"]

    def hero_bgs(rows, cells, reg, y):
        return [cells.get((reg[1] + y, x), ("", ""))[1]
                for x in range(reg[0], reg[0] + reg[2])]

    def hero_row(rows, reg, y):
        return rows[reg[1] + y][reg[0]: reg[0] + reg[2]]

    fig_h = min(7, ap_hero[3])
    check("solari: the drawn figure is on the shipped aperture (probe "
          "self-check — the checks below can fail)",
          any(BS.FLAP_INK in hero_row(ap_rows, ap_hero, y)
              for y in range(fig_h)), f"hero region {ap_hero}")
    face_counts = [hero_bgs(ap_rows, ap_cells, ap_hero, y).count(S["flap"])
                   for y in range(fig_h)]
    seam_counts = [hero_bgs(ap_rows, ap_cells, ap_hero, y).count(S["seam"])
                   for y in range(fig_h)]
    check("solari: every row of the figure but one stands on a `flap` GROUND "
          "— the cards are painted, not implied",
          sum(1 for n in face_counts if n) == fig_h - 1, f"{face_counts}")
    check("solari: exactly ONE row of the figure is the `seam` band, and it "
          "is the hinge row the base declared",
          [i for i, n in enumerate(seam_counts) if n] == [BS.flap_seam(7)],
          f"{seam_counts}")
    check("solari: the face and the band are the SAME WIDTH — a hinge one "
          "cell wider than its card is the defect this measures",
          max(face_counts) == max(seam_counts),
          f"face {max(face_counts)} vs band {max(seam_counts)}")
    check("solari: the face is a real STEP off the screen's ground (a face "
          "that matched the ground would be a token doing nothing)",
          S["flap"] != S["ground"]
          and S["ground"] in hero_bgs(ap_rows, ap_cells, ap_hero, 0),
          f"face {S['flap']} ground {S['ground']}")
    hinge = hero_row(ap_rows, ap_hero, BS.flap_seam(7))
    check("solari: the hinge row is a CONTINUOUS line across each card — "
          "every cell of it is hinge glyph or numeral, no bare face",
          BS.FLAP_SEAM_FACE in hinge and BS.FLAP_SEAM_INK in hinge,
          repr(hinge.strip()))
    amber = {S["accent"], S["warn"]}
    calm_fg = {ap_cells.get((ap_hero[1] + y, x), ("", ""))[0]
               for y in range(fig_h)
               for x in range(ap_hero[0], ap_hero[0] + ap_hero[2])}
    hero_bg = {b for y in range(fig_h)
               for b in hero_bgs(ap_rows, ap_cells, ap_hero, y)}
    hinge_fg = {ap_cells.get((ap_hero[1] + BS.flap_seam(7), x), ("", ""))[0]
                for x in range(ap_hero[0], ap_hero[0] + ap_hero[2])
                if hero_row(ap_rows, ap_hero, BS.flap_seam(7))
                [x - ap_hero[0]] == BS.FLAP_SEAM_FACE}
    check("solari: the ration never reaches PASSIVE STRUCTURE — no card face "
          "and no hinge band is amber, whatever the reading's severity",
          not (hero_bg & amber) and not (hinge_fg & amber),
          f"grounds {sorted(hero_bg)}, hinge {sorted(hinge_fg)}")
    check("solari: the hinge line is `mut` on the shipped frame too (the "
          "markup and the composited render agree)",
          hinge_fg == {S["mut"]}, f"{sorted(hinge_fg)}")

    lg_rows, lg_cells, lg_hero = await capture_ap_bg("ledger", str(fx))
    (W / "prototypes" / "out" / "aperture_ledger_hero.txt").write_text(
        "\n".join(r[lg_hero[0]: lg_hero[0] + lg_hero[2]]
                  for r in lg_rows[lg_hero[1]: lg_hero[1] + lg_hero[3]]),
        encoding="utf-8")
    L = TH.THEMES["ledger"]
    lg_text = "\n".join(hero_row(lg_rows, lg_hero, y)
                        for y in range(lg_hero[3]))
    check("ledger: the engraved figure reaches the shipped aperture",
          "█" in lg_text and "▄" in lg_text, repr(lg_text.split("\n")[0]))
    lg_bgs = {b for y in range(lg_hero[3])
              for b in hero_bgs(lg_rows, lg_cells, lg_hero, y)}
    check("ledger: the figure stands on the PAPER — one ground under the "
          "whole hero, no cell faces anywhere",
          lg_bgs == {L["ground"]}, f"{sorted(lg_bgs)}")
    lg_fg = {lg_cells.get((lg_hero[1] + y, x), ("", ""))[0]
             for y in range(lg_hero[3])
             for x in range(lg_hero[0], lg_hero[0] + lg_hero[2])}
    # SEVERITY, and the probe had this backwards on its first run — which is
    # the finding, not an inconvenience. `_fixture_board.json` is genuinely
    # overdue (its queue reads `2d!`), so the ledger headline IS debt and the
    # red pen is CORRECT there. The law is a pair, and both halves are
    # asserted against fixtures that differ in exactly that fact.
    check("ledger: the figure wears the RED PEN when the headline is overdue "
          "debt — which is the only thing that hue is allowed to mean",
          L["alert"] in lg_fg, f"{sorted(lg_fg)}")
    # The CALM half of that pair is asserted at DRAW level, where the tone is
    # an argument. It is NOT asserted here, and the reason is measured rather
    # than assumed: the engine picks the hero signal from the board, so the
    # severity of a rendered aperture is the fixture's property, and
    # `_verify_calm.json` (built for the blueprint pass: nothing overdue)
    # still drives this hero to WARN. What the shipped frame CAN answer is
    # that the figure's ink comes from the severity ladder and nowhere else —
    # a stray hue on a hero is exactly the defect the ration exists to stop.
    LADDER_L = {L["calm"], L["warn"], L["alert"], L["ink"], ""}
    check("ledger: every ink on the figure comes from the severity ladder — "
          "no fourth colour reaches the drawn type",
          lg_fg <= LADDER_L, f"{sorted(lg_fg - LADDER_L)}")
    LADDER_S = {S["calm"], S["warn"], S["alert"], S["ink"], S["mut"], ""}
    check("solari: every ink on the cards comes from the severity ladder plus "
          "the hinge's `mut` — and nothing else",
          calm_fg <= LADDER_S, f"{sorted(calm_fg - LADDER_S)}")
    # THE COST, MEASURED AND NAMED rather than discovered later: ledger's own
    # composition pins `#hero` to 7 rows (language.py, `Screen.sz-board #hero
    # { height: 7 }`) and the drawn figure is exactly 7 rows tall, so at the
    # BOARD seat the caption is renounced — the same shape of fact as naught's
    # drawn caption, which no composition's row budget reaches either. It is
    # recorded here so it cannot rot into a silent loss, and the widget seat
    # is asserted to bring the caption back.
    check("ledger: at the BOARD seat the hero is the FIGURE and the caption "
          "is renounced (its own composition pins 7 rows; curing this needs "
          "language.py, outside this pass's file set)",
          lg_hero[3] == 7 and "DAYS" not in lg_text,
          f"hero h={lg_hero[3]}")
    nar_rows, _, nar_hero = await capture_ap_bg("ledger", str(fx),
                                                size=(70, 30))
    nar_text = "\n".join(r[nar_hero[0]: nar_hero[0] + nar_hero[2]]
                         for r in nar_rows[nar_hero[1]:
                                           nar_hero[1] + nar_hero[3]])
    check("ledger: at the WIDGET seat the caption comes back with the figure "
          "— the renunciation is one composition's, not the base's",
          "█" in nar_text and any(c.isalpha() for c in nar_text),
          f"hero h={nar_hero[3]}")

    bp_rows, bp_cells, bp_hero = await capture_ap_bg("blueprint", str(fx))
    (W / "prototypes" / "out" / "aperture_blueprint_hero.txt").write_text(
        "\n".join(r[bp_hero[0]: bp_hero[0] + bp_hero[2]]
                  for r in bp_rows[bp_hero[1]: bp_hero[1] + bp_hero[3]]),
        encoding="utf-8")
    B = TH.THEMES["blueprint"]
    bp_text = "\n".join(hero_row(bp_rows, bp_hero, y)
                        for y in range(bp_hero[3]))
    check("blueprint: the CUT figure reaches the shipped aperture",
          BS.ST_RAIL_W in bp_text and BS.ST_RAIL_E in bp_text,
          # SENTINEL "": a DETAIL argument, evaluated on every call whether
          # the law passes or fails — so a one-row hero would have killed the
          # run from the reporting side, on the line that exists to explain
          # the failure. The condition already reds on its own containments.
          repr(nth(bp_text.split("\n"), 1, "")))
    check("blueprint: and it is hollow ON THE COMPOSITED FRAME — not one cell "
          "of the hero band is a solid block (the markup claim and the render "
          "agree, which is the pair the flap pass made a rule)",
          "█" not in bp_text)
    bp_fig = [hero_row(bp_rows, bp_hero, y) for y in range(min(7, bp_hero[3]))]
    check("blueprint: every mark in the figure band belongs to the HOLLOW "
          "vocabulary — nothing typographic survived into the seat where the "
          "old `plain` hero printed its value as text",
          set("".join(bp_fig)) - {" "} <= set(BS.ST_HOLLOW),
          f"{sorted(set(''.join(bp_fig)) - {' '})}")
    bp_bgs = {b for y in range(bp_hero[3])
              for b in hero_bgs(bp_rows, bp_cells, bp_hero, y)}
    check("blueprint: the figure stands on the SHEET — one ground under the "
          "whole hero, no face and no plate anywhere (a painted face is a "
          "containing box drawn in background, which this language forbids)",
          bp_bgs == {B["ground"]}, f"{sorted(bp_bgs)}")
    check("blueprint: the hero puts NO KNOCKOUT on the sheet — the one "
          "reverse-video element per view is the title block's STATE cell, "
          "and a second one is the defect that law exists to name",
          not any(bg and bg != B["ground"]
                  for y in range(bp_hero[3])
                  for bg in hero_bgs(bp_rows, bp_cells, bp_hero, y)))
    bp_fg = {bp_cells.get((bp_hero[1] + y, x), ("", ""))[0]
             for y in range(bp_hero[3])
             for x in range(bp_hero[0], bp_hero[0] + bp_hero[2])}
    # SEVERITY, and the fixture's truth was checked before the law was written
    # (the thirty-sixth pass's lesson: the first ledger probe asserted "calm"
    # against a board that is genuinely overdue and went red for being wrong).
    LADDER_B = {B["calm"], B["warn"], B["alert"], B["ink"], B["mut"],
                B["dim"], ""}
    check("blueprint: every ink on the figure comes from the severity ladder "
          "and the caption's own greys — no fourth colour reaches the drawn "
          "type", bp_fg <= LADDER_B, f"{sorted(bp_fg - LADDER_B)}")
    check("blueprint: `warn` IS the cyan grey, DECLARED — the near-due step "
          "in this language is BRIGHTNESS, which is why the calm-ration check "
          "at draw level skips it rather than asserting the caption away",
          B["warn"] == B["mut"], f"warn {B['warn']} mut {B['mut']}")
    # The CALM half of that pair is asserted at DRAW level, where the tone is
    # an argument (`calm` tone -> zero alert). It is deliberately NOT asserted
    # here: the engine picks the hero's severity from the board, so a rendered
    # aperture's tone is the FIXTURE's property, and `_verify_calm.json` is
    # not built until the sheet section further down — asserting against a file
    # a previous run left behind is a check that measures its own history.
    check("blueprint: the hero fits the aperture's row budget with its caption "
          "(no composition pins it, so the figure and the caption both land)",
          bp_hero[3] <= 12 and any(c.isalpha() for c in bp_text),
          f"hero h={bp_hero[3]}")
    print("\n== APP LEVEL: the RAIL on the live board (the `layout` token)")
    check("the footer owns a `▏` of its own (probe self-check: it must be "
          "dropped, or every language would 'have a rail')",
          RAIL in db.split("\n")[-1] and "palette" in db.split("\n")[-1])
    db_body = body_rows(db)
    titles = [r for r in db_body if "shut down legacy servers" in r]
    heads = [r for r in db_body if "backlog" in r and "·" not in r]
    if len(titles) != 1:
        # EVIDENCE, not just a verdict: this probe has failed intermittently
        # across four sessions (PENDING: the darkside capture race) and every
        # diagnosis so far had to reconstruct the frame from memory. Dump it.
        (W / "prototypes" / "out" / "_race_darkside.txt").write_text(
            db, encoding="utf-8")
    check("darkside: the fixture card is on screen (probe self-check)",
          len(titles) == 1, f"{len(titles)} row(s)")
    check("darkside: the rail LEADS the card row",
          bool(titles) and titles[0].lstrip().startswith(RAIL))
    check("darkside: the rail runs through the section head too",
          bool(heads) and heads[0].lstrip().startswith(RAIL))
    # lstrip() would hide a one-cell zigzag between head and cards, which is
    # exactly what the first render had: the edge is only an edge if every
    # row puts the stroke in the SAME column
    rail_cols = sorted({r.index(RAIL) for r in db_body if RAIL in r})
    check("darkside: the rail is ONE unbroken edge (same column every row)",
          len(rail_cols) == 1, f"columns={rail_cols}")
    check("darkside: the title survives the rail INTACT (legibility law)",
          "shut down legacy servers" in db)
    for name in TH.ORDER:
        if name == "darkside":
            continue
        # PENDING #48, CURED AT THIS ADDRESS AND NOT AT THE ONE IT WAS FILED
        # AT. The item's shape is right — a NEGATIVE law over a derived
        # sequence that nothing asserts is non-empty — and this is where the
        # suite really has it: `body_rows` comes back empty and the join is
        # "", `RAIL not in ""` is True, and the law passes on a language
        # whose board rendered NOTHING, which is the one input it must not
        # reason about. Its darkside sibling is anchored (three laws above
        # measure that board's rows); the other eight languages are not
        # anchored by anything. `bool(_brows)` is the leg, and it can fire:
        # an empty capture reds it and names the count.
        _brows = body_rows(boards[name])
        check(f"{name}: board carries no rail (the mechanism is darkside's)",
              bool(_brows) and RAIL not in "\n".join(_brows),
              f"{len(_brows)} body row(s)")
    # NARROW REGIME: an identity mechanism that only survives at 118 is not
    # an identity mechanism (VERIFY.md: one width hides a whole regime)
    for w in (60, 80, 118):
        nb, _, _, _ = await capture("darkside", board_path=str(fx),
                                    size=(w, 30))
        bad = [len(r) for r in nb.split("\n") if len(r) != w]
        check(f"darkside @{w}: the frame never wraps (every row is {w} cells)",
              not bad, f"bad={bad[:3]}")
        # below the board size class the app shows no board at all, so no
        # rail is the CORRECT render. The law is that the rail is present
        # wherever the board is — not that it is present at every width.
        body = body_rows(nb)
        on_screen = any("shut down legacy servers" in r for r in body)
        check(f"darkside @{w}: rail present wherever the board is",
              (sum(RAIL in r for r in body) >= 2) == on_screen,
              f"board={'yes' if on_screen else 'no'}")

    print("\n== APP LEVEL: industrial's PLATES on the live board (`layout`)")
    RULE_RUN = re.compile("─{10,}")
    ib_rows = body_rows(boards["industrial"])
    ip_cards = [r for r in ib_rows if PLATE.search(r)]
    check("industrial: the fixture card is on screen (probe self-check)",
          any("Renew TLS certificate" in r for r in ib_rows))
    check("industrial: the card rows on the board wear their plate codes",
          len(ip_cards) >= 4, f"{len(ip_cards)} plated row(s)")
    check("industrial: one plate legend bands each phase (3 on the fixture)",
          "\n".join(ib_rows).count("▐▌") == 3,
          f"{chr(10).join(ib_rows).count('▐▌')} legends")
    # read the LEADING column only: `str.index` on a shared board row would
    # return whichever column happens to have a card on that row
    x0 = min((at(r, "▐") for r in ip_cards if at(r, "▐") >= 0), default=-1)
    first_codes = [re.search(r"\d\d", r[x0: x0 + 7]).group(0)
                   for r in ip_cards if x0 >= 0 and r[x0] == "▐"]
    check("industrial: the leading column's codes are sequential and unique",
          first_codes == ["01", "02", "03", "04"], f"{first_codes}")
    ihead = next((i for i, r in enumerate(ib_rows) if "▐▌" in r), -1)
    # a legend one cell off its own plates is not an edge, it is a zigzag —
    # the first render had exactly that (`.kb-card` pays `padding: 0 1`,
    # `.col-head` pays none). Same instrument darkside's rail is held to.
    check("industrial: the legend stands on the plates' own left edge (ONE "
          "unbroken column, not a zigzag)",
          x0 >= 0 and ihead >= 0 and all(r[x0] == "▐" for r in ip_cards)
          and ib_rows[ihead][x0] == "▐", f"edge column {x0}")
    check("industrial: the BOX FRAME is gone from the real board — no rule "
          "row under the legends",
          ihead >= 0 and not RULE_RUN.search(ib_rows[ihead + 1]),
          repr(ib_rows[ihead + 1][:34]) if ihead >= 0 else "no legend row")
    bad118 = [len(r) for r in boards["industrial"].split("\n") if len(r) != 118]
    check("industrial @118x30: the frame never wraps (every row is 118 cells)",
          not bad118, f"bad={bad118[:3]}")
    # the plate must DISPATCH: back to the base default and the previous
    # BOXED composition has to return to the REAL board, not merely the kit
    ifl, _, _, _ = await capture("industrial", mutate=("layout", "flow"),
                                 board_path=str(fx))
    (W / "prototypes" / "out" / "panel_industrial_flow.txt").write_text(
        ifl, encoding="utf-8")
    fl_rows = body_rows(ifl)
    jhead = next((i for i, r in enumerate(fl_rows) if "BACKLOG" in r), -1)
    check("industrial.layout=flow keeps the board itself (probe self-check)",
          "Renew TLS certificate" in ifl and jhead >= 0)
    check("industrial.layout=flow brings the rule row BACK (the negative "
          "control: the check above CAN fail)",
          jhead >= 0 and bool(RULE_RUN.search(fl_rows[jhead + 1])))
    check("industrial.layout=flow strips the plates from the live board",
          not any(PLATE.search(r) for r in fl_rows)
          and "▐▌" not in "\n".join(fl_rows))
    check("industrial.layout=flow changes the board outside the hero",
          ifl != boards["industrial"])
    for name in TH.ORDER:
        if name == "industrial":
            continue
        body = "\n".join(body_rows(boards[name]))
        check(f"{name}: board carries no function plates (they are "
              f"industrial's)",
              not PLATE.search(body) and "▐▌" not in body)
    # THE COLLISION CLAIM, MEASURED. The external spec said these two read as
    # each other once colour is stripped. They do not: the metric is the
    # fraction of BOARD CELLS that differ, which a real collision would drive
    # towards zero. Pre-change it was 47.5%; the plates cost 2.2 points
    # (both languages now indent their card rows) and it is still nowhere
    # near a collision — the claim was false before this pass and after it.

    def cell_diff(a: str, b: str) -> float:
        n = t = 0
        for x, y in zip(a.split("\n"), b.split("\n")):
            m = max(len(x), len(y))
            n += sum(1 for p, q in zip(x.ljust(m), y.ljust(m)) if p != q)
            t += m
        return n / t if t else 0.0

    ic = cell_diff(boards["industrial"], boards["corgi"])
    check("industrial vs corgi: nameable apart in greyscale (the spec's "
          "collision claim, PROBED — it is false)",
          ic > 0.30, f"{ic:.1%} of board cells differ")
    # NARROW REGIME: an identity mechanism that only survives at 118 is not
    # an identity mechanism (VERIFY.md: one width hides a whole regime)
    ib80, _, _, _ = await capture("industrial", board_path=str(fx),
                                  size=(80, 30))
    (W / "prototypes" / "out" / "panel_industrial_80.txt").write_text(
        ib80, encoding="utf-8")
    bad80 = [len(r) for r in ib80.split("\n") if len(r) != 80]
    check("industrial @80x30: the frame never wraps (every row is 80 cells)",
          not bad80, f"bad={bad80[:3]}")
    c80 = [r for r in body_rows(ib80) if PLATE.search(r)]
    check("industrial @80x30: every card row still carries its code (the "
          "tight tier engages, the number does not)",
          len(c80) >= 4, f"{len(c80)} plated row(s)")
    check("industrial @80x30: the plate legends still band the phases",
          "\n".join(body_rows(ib80)).count("▐▌") == 3)

    print("\n== APP LEVEL: swiss's EDITORIAL SPREAD on the live board")
    # THE HEIGHT IS PART OF THE PROBE. At 118x30 swiss's sections board shows
    # ONE phase head, so "exactly one hairline" would pass on the fold rather
    # than on the law. 44 rows put a second masthead on screen, which is what
    # makes the check — and its flow negative control — mean anything.
    sw44, _, _, _ = await capture("swiss", board_path=str(fx), size=(118, 44))
    (W / "prototypes" / "out" / "editorial_swiss_118.txt").write_text(
        sw44, encoding="utf-8")

    def spread_of(board: str) -> list[str]:
        """The SPREAD, and only it: the chrome above carries a hairline of its
        own (the `hairline` meter), so a naive rule count measures the meter
        and proves nothing. The spread begins at the leading masthead."""
        rows = body_rows(board)
        i = next((j for j, r in enumerate(rows) if "B A C K L O G" in r), -1)
        return [] if i < 0 else rows[i:]

    sp = spread_of(sw44)
    check("swiss @118x44: TWO mastheads are on screen (probe self-check — the "
          "one-hairline law is vacuous with only one head)",
          bool(sp) and sum(1 for r in sp if "D O I N G" in r) == 1,
          f"{len(sp)} spread rows")
    check("swiss: exactly ONE hairline rules the whole spread",
          sum(1 for r in sp if SW_RULE.search(r)) == 1,
          f"{sum(1 for r in sp if SW_RULE.search(r))} rule row(s)")
    sw_ent = [r for r in sp if TITLE in r]
    check("swiss: the fixture entry is on screen (probe self-check)",
          len(sw_ent) == 1, f"{len(sw_ent)} row(s)")
    # the MEASURE is read off the render (the masthead rule is `m - 1` cells),
    # so the grid check needs no second-hand knowledge of kanban.py's budget
    rule_row = first_of((r for r in sp if SW_RULE.search(r)), "")
    _rule_m = SW_RULE.search(rule_row)
    m118 = len(_rule_m.group(0)) + 1 if _rule_m else 0
    g118 = LG.kit("swiss").grid(m118) if m118 else []
    row = sw_ent[0] if sw_ent else ""
    x0 = at(row, TITLE)
    off = ([at(row, "Legacy Sunset") - x0, at(row, "8d") - x0]
           if row and "Legacy Sunset" in row else [])
    check("swiss @118: the entry's three elements stand on the grid's own "
          "column origins (subject · byline · figure)",
          len(g118) == 3 and off == [g118[1][0], g118[2][0]],
          f"{off} vs {[c[0] for c in g118[1:]]} at measure {m118}")
    mh = next((r for r in sp if "B A C K L O G" in r), "")
    check("swiss: the masthead stands on the entries' own left edge (ONE "
          "unbroken column, not a zigzag)",
          bool(mh) and x0 >= 0 and at(mh, "B") == x0,
          f"{at(mh, 'B')} vs {x0}")
    check("swiss: the masthead's COUNT stands in the same column as the "
          "figures below it — alignment is the structure",
          bool(mh) and at(row, "8d") >= 0
          and at(mh, "7", last=True) == at(row, "8d"),
          f"{at(mh, '7', last=True)} vs {at(row, '8d')}")
    # AIR: the grid filled the measure, it must not have filled the ROWS
    doi = next((i for i, r in enumerate(sp) if "D O I N G" in r), len(sp))
    band = sp[:doi]
    n_blank = sum(1 for r in band if not r.strip())
    n_entry = sum(1 for r in band if re.search(r"\S", r)
                  and not SW_RULE.search(r) and "B A C K L O G" not in r)
    check("swiss: the air rows survive the grid (a blank row between every "
          "entry — `pitch` is spent, not reclaimed)",
          n_blank >= n_entry, f"{n_blank} blank / {n_entry} entry row(s)")

    def ink_frac(s: str) -> float:
        rows = s.split("\n")
        tot = sum(len(r) for r in rows) or 1
        return sum(1 for r in rows for ch in r if ch != " ") / tot

    si = ink_frac("\n".join(body_rows(boards["swiss"])))
    ii = ink_frac("\n".join(body_rows(boards["industrial"])))
    check("swiss stays the AIRY language — its board's ink fraction is under "
          "the flat one's (air is a commitment, not leftovers)",
          si < ii, f"swiss {si:.1%} vs industrial {ii:.1%}")
    check("swiss: the board's ink fraction stays inside its airy band "
          "(< 20% — the grid spends measure, not ink)",
          si < 0.20, f"{si:.1%}")
    bad118 = [len(r) for r in sw44.split("\n") if len(r) != 118]
    check("swiss @118x44: the frame never wraps (every row is 118 cells)",
          not bad118, f"bad={bad118[:3]}")
    # DISPATCH on the REAL board: back to the base default and the previous
    # full-width flow composition must return to the screen, not just the kit
    swfl, _, _, _ = await capture("swiss", mutate=("layout", "flow"),
                                  board_path=str(fx), size=(118, 44))
    (W / "prototypes" / "out" / "editorial_swiss_flow.txt").write_text(
        swfl, encoding="utf-8")
    fl_sp = spread_of(swfl)
    check("swiss.layout=flow keeps the board itself (probe self-check)",
          TITLE in swfl and bool(fl_sp))
    check("swiss.layout=flow rules EVERY masthead again (the negative "
          "control: the ONE-hairline check CAN fail)",
          sum(1 for r in fl_sp if SW_RULE.search(r)) == 2,
          f"{sum(1 for r in fl_sp if SW_RULE.search(r))} rule row(s)")
    check("swiss.layout=flow strips the bylines from the live spread",
          "Legacy Sunset" not in swfl)
    check("swiss.layout=flow changes the board outside the hero",
          swfl != sw44)
    # the `columns` token must reach the RENDER too, not only the kit
    sw2, _, _, _ = await capture("swiss", mutate=("columns", 2),
                                 board_path=str(fx), size=(118, 44))
    check("swiss.columns=2 drops the byline column on the live board (the "
          "grid follows the token)",
          "Legacy Sunset" not in sw2 and TITLE in sw2 and sw2 != sw44)
    # NARROW REGIME: the declared drop is only real if it fires on a real
    # board, not only in the kit (VERIFY.md — one width hides a whole regime)
    sw80, _, _, _ = await capture("swiss", board_path=str(fx), size=(80, 30))
    (W / "prototypes" / "out" / "editorial_swiss_80.txt").write_text(
        sw80, encoding="utf-8")
    bad80 = [len(r) for r in sw80.split("\n") if len(r) != 80]
    check("swiss @80x30: the frame never wraps (every row is 80 cells)",
          not bad80, f"bad={bad80[:3]}")
    sp80 = spread_of(sw80)
    r80 = next((r for r in sp80 if TITLE in r), "")
    rule80 = next((r for r in sp80 if SW_RULE.search(r)), "")
    m80 = len(SW_RULE.search(rule80).group(0)) + 1 if rule80 else 0
    g80 = LG.kit("swiss").grid(m80)
    check("swiss @80x30: the entry is on screen and the drop FIRED — two "
          "columns, the byline renounced, the figure kept",
          bool(r80) and len(g80) == 2 and "8d" in r80
          and "Legacy Sunset" not in sw80,
          f"{len(g80)} columns at measure {m80}")
    check("swiss @80x30: the figure stands on the second column's origin",
          bool(r80) and len(g80) == 2
          and min(at(r80, "8d"), at(r80, TITLE)) >= 0
          and at(r80, "8d") - at(r80, TITLE) == g80[1][0],
          f"{at(r80, '8d') - at(r80, TITLE)} vs "
          f"{g80[1][0] if len(g80) > 1 else -1}")
    mh80 = next((r for r in sp80 if "B A C K L O G" in r), "")
    check("swiss @80x30: masthead count and entry figures still share the "
          "column (the grid holds at the narrow measure)",
          bool(mh80) and bool(r80) and at(r80, "8d") >= 0
          and at(mh80, "7", last=True) == at(r80, "8d"))
    check("swiss @80x30: still exactly ONE hairline",
          sum(1 for r in sp80 if SW_RULE.search(r)) == 1,
          f"{sum(1 for r in sp80 if SW_RULE.search(r))} rule row(s)")

    print("\n== APP LEVEL: nord's MASTER/DETAIL SPLIT on the live board")
    nrows, nstyle, nreg = await capture_styled("nord", str(fx), (118, 30))
    (W / "prototypes" / "out" / "split_nord_118.txt").write_text(
        "\n".join(nrows), encoding="utf-8")

    def pane_xs(style, y, a, b):
        """The painted COLUMNS of one row inside one pane. The two panes share
        every screen row, so any row-level measurement measures both at once
        and means nothing — every span below is per-pane for that reason."""
        return [x for x in range(a, b) if (y, x) in style]

    def pane_cells(style, y, a, b):
        return [style[(y, x)] for x in range(a, b) if (y, x) in style]

    def pane_span(style, y, a, b):
        """AREA as EXTENT: first painted cell to last. See the kit-level note
        — painted-cell COUNT ranks a dense dim block above a heading and
        scores letterspacing at zero, which is backwards."""
        xs = pane_xs(style, y, a, b)
        return 0 if not xs else xs[-1] - xs[0] + 1

    def split_geometry(reg, kit):
        """Every span below comes from `panes()` — the SAME function the
        renderer read. The check cannot drift from the render without one of
        them being wrong."""
        x, y, w, h = reg
        mw, dw = kit.panes(w)
        return (x, y, h, mw, dw, x + mw, x + mw + kit.GUTTER)

    nx, ny, nh, nmw, ndw, m_end, d_x0 = split_geometry(nreg, kn)
    nband = range(ny, min(ny + nh, len(nrows)))
    check("nord @118: the board really is in the SPLIT regime (probe "
          "self-check — every check below is vacuous in the degrade)",
          ndw > 0 and nmw >= mf, f"panes={(nmw, ndw)} board w={nreg[2]}")
    check("nord @118: the fixture task is on screen (probe self-check)",
          any(ND_T in nrows[y] for y in nband), )
    # THE PANE BOUNDARY, at the cell the shared function computes
    over = [y for y in nband if pane_cells(nstyle, y, m_end, d_x0)]
    check("nord @118: the GUTTER is empty — no master row crosses the "
          f"boundary at x={m_end} and no detail row starts before x={d_x0}",
          not over, f"{len(over)} row(s) painting the gutter")
    det_rows = [y for y in nband if pane_cells(nstyle, y, d_x0, nx + nreg[2])]
    check("nord @118: the detail pane paints, and only right of the boundary",
          bool(det_rows), f"{len(det_rows)} detail row(s)")
    # THE CURSOR: exactly once, in the master, on the row the detail expands
    cur_rows = [y for y in nband if kn.CUR in nrows[y][nx:m_end]]
    check("nord @118: the cursor marks EXACTLY ONE master row",
          len(cur_rows) == 1, f"{len(cur_rows)} row(s)")
    cur_text = nrows[cur_rows[0]][nx:m_end] if cur_rows else ""
    ttl_rows = [y for y in nband
                if any(b for _, b in pane_cells(nstyle, y, d_x0,
                                                nx + nreg[2]))]
    check("nord @118: exactly one BOLD row in the detail pane — the title",
          len(ttl_rows) == 1, f"{len(ttl_rows)} bold row(s)")
    ttl_text = nrows[ttl_rows[0]][d_x0:] if ttl_rows else ""
    check("nord @118: the cursor sits on the row the DETAIL expands (the two "
          "panes name the same task, which is the whole pattern)",
          bool(cur_text) and bool(ttl_text)
          and ttl_text.replace(" ", "").upper().startswith(
              cur_text.replace(kn.CUR, "").strip().split("  ")[0]
              .replace(" ", "").upper()[:12]),
          f"{cur_text.strip()!r} vs {ttl_text.strip()!r}")
    # LAW 03 ON THE RENDER: one element wins area AND brightness AND isolation
    PANES = {"m": (nx, m_end), "d": (d_x0, nx + nreg[2])}
    area, bold, iso = {}, {}, {}
    for y in nband:
        for tag, (a, b) in PANES.items():
            area[(tag, y)] = pane_span(nstyle, y, a, b)
            bold[(tag, y)] = any(bd for _, bd in pane_cells(nstyle, y, a, b))
    for (tag, y) in area:
        a, b = PANES[tag]
        up = y - 1 >= ny and not pane_xs(nstyle, y - 1, a, b)
        dn = y + 1 < ny + nh and not pane_xs(nstyle, y + 1, a, b)
        iso[(tag, y)] = up and dn
    top = max(area.values())
    wins = [k2 for k2 in area if area[k2] == top and bold[k2] and iso[k2]]
    check("nord @118: EXACTLY ONE element on the board wins AREA and "
          "BRIGHTNESS and ISOLATION — law 03, which nord failed before this "
          "pass",
          len(wins) == 1, f"winners={wins} (widest element {top} cells)")
    check("nord @118: ... and it is the DETAIL TITLE",
          bool(wins[:1]) and bool(ttl_rows) and wins[0][0] == "d"
          and wins[0][1] == ttl_rows[0],
          f"{wins[:1]} vs title row {ttl_rows[:1]}")
    m_top = max(v for k2, v in area.items() if k2[0] == "m")
    check("nord @118: the title out-spans every MASTER row (measured per "
          "pane, because the two panes share every screen row)",
          top > m_top, f"{top} vs {m_top}")
    # brightness measured as a RANK on the RENDER, not read off the markup
    # `ttl_rows` is EMPTY when the detail pane comes back unpainted — the
    # capture race, in the `capture_styled` path (PENDING's twenty-eighth-pass
    # watch). Unguarded this raised IndexError and KILLED the run, hiding every
    # check after it; the race is now what it should always have been, a loud
    # FAIL that the run continues past. Same discipline `settle()`'s timeout
    # carries: record it, name it, and let the cascade be the diagnosis.
    ttl_hex = {c for c, _ in pane_cells(nstyle, ttl_rows[0], d_x0,
                                        nx + nreg[2]) if c} if ttl_rows else set()
    others = {c for k2 in area if k2 not in wins
              for c, _ in pane_cells(nstyle, k2[1], *PANES[k2[0]]) if c}
    check("nord @118: the title's ink is the brightest on the board",
          bool(ttl_hex) and max(chan_lum(c) for c in ttl_hex)
          >= max([chan_lum(c) for c in others] or [0]),
          f"title={max([chan_lum(c) for c in ttl_hex] or [0]):.0f} vs "
          f"{max([chan_lum(c) for c in others] or [0]):.0f}")
    check("nord @118: nothing wraps — every board row fits its own pane",
          all(len(nrows[y].rstrip()) <= nx + nreg[2] for y in nband))
    # NO LEAKAGE: the split is nord's alone
    for name in TH.ORDER:
        if name == "nord":
            continue
        check(f"{name}: no split on the live board (its layout is untouched)",
              LG.kit(name).board_layout() != "split")
    # THE NARROW REGIME — a real screen, not a hypothetical
    n80, s80, r80 = await capture_styled("nord", str(fx), (80, 30))
    (W / "prototypes" / "out" / "split_nord_80.txt").write_text(
        "\n".join(n80), encoding="utf-8")
    x8, y8, h8, mw8, dw8, me8, dx8 = split_geometry(r80, kn)
    band8 = range(y8, min(y8 + h8, len(n80)))
    check("nord @80: the split still holds at the narrow board, at its own "
          "computed geometry", dw8 > 0 and mw8 + kn.GUTTER + dw8 == r80[2],
          f"panes={(mw8, dw8)} of {r80[2]}")
    check("nord @80: the gutter is still empty (the boundary moved with the "
          "function, not with a hardcoded number)",
          not [y for y in band8 if pane_cells(s80, y, me8, dx8)])
    n_cur8 = sum(1 for y in band8 if kn.CUR in n80[y][x8:me8])
    n_bold8 = sum(1 for y in band8
                  if any(b for _, b in pane_cells(s80, y, dx8, x8 + r80[2])))
    check("nord @80: still exactly one cursor in the master",
          n_cur8 == 1, f"{n_cur8} row(s)")
    check("nord @80: still exactly one bold row in the detail (the title)",
          n_bold8 == 1, f"{n_bold8} row(s)")
    check("nord @80: nothing wraps at the narrow board",
          all(len(n80[y].rstrip()) <= x8 + r80[2] for y in band8))
    # THE FLOW DEGRADE on the LIVE board: the columns skeleton comes back.
    # Measured in the BOARD REGION, because `▸` is also the base kit's tab
    # marker ("▸board │ lanes …") — a whole-frame search finds the tab row in
    # every language and proves nothing. That is `body_rows`' own lesson,
    # applied to a second glyph.
    fl_rows, fl_style, fl_reg = await capture_styled(
        "nord", str(fx), (118, 30), mutate=("layout", "flow"))
    (W / "prototypes" / "out" / "split_nord_flow.txt").write_text(
        "\n".join(fl_rows), encoding="utf-8")
    fx0, fy0, fw0, fh0 = fl_reg
    fband = [fl_rows[y][fx0: fx0 + fw0]
             for y in range(fy0, min(fy0 + fh0, len(fl_rows)))]
    check("nord.layout=flow keeps the board itself (probe self-check)",
          any(ND_T in r for r in fband))
    check("nord.layout=flow removes the cursor from the BOARD REGION — the "
          "split goes with the token (the negative control: the checks above "
          "CAN fail)",
          not any(kn.CUR in r for r in fband),
          f"{sum(1 for r in fband if kn.CUR in r)} cursor row(s)")
    check("nord.layout=flow brings the COLUMNS skeleton back — the three "
          "phase heads share ONE row, which the split stacks",
          any(all(ph in r for ph in ("BACKLOG", "DOING", "DONE"))
              for r in fband))
    check("nord.layout=flow changes the rendered board",
          fl_rows != nrows)
    # NAVIGATION must survive the third branch (a new container tree is
    # exactly where a cursor model breaks — and there is no second model here)
    from app import TaskboardWidget as _TW
    from kanban import KanbanBoard as _KB
    napp = _TW(board_path=str(fx))
    async with napp.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        napp.notify = lambda *a, **kw: None
        napp.set_theme("nord")
        await pilot.pause()
        napp.redraw()
        await settle(napp, pilot, "nord nav")
        kb = napp.query_one(_KB)
        # THIS CHECK USED TO READ `kb._cursor is not None`, and that made it
        # VACUOUS: `_drive` sets the cursor on the line BEFORE it writes the
        # pane, so through the whole thirtieth-pass bug the cursor was set and
        # the pane was blank — a check named "the pane is never blank" that
        # could not fail when the pane was blank. It now reads the PIXELS of
        # the pane's own region on the composited frame, which is the thing it
        # is named for. Mutation-tested: with `_seed_detail` neutered in a
        # throwaway probe it reports `0 painted row(s)` and FAILS.
        def detail_ink() -> int:
            """Painted rows inside the detail pane's region. The region comes
            from the widget, so the measure follows a recomposition instead of
            hard-coding the boundary."""
            pane = napp.query("#kb-detail")
            if not pane:
                return 0
            r = pane.first().region
            fr = screen_text(napp)
            return sum(bool(fr[y][r.x: r.x + r.width].strip())
                       for y in range(r.y, min(r.y + r.height, len(fr))))

        seeded = detail_ink()
        check("nord nav: the detail is driven at rest, before any key (probe "
              "self-check — the pane is never blank, READ OFF THE FRAME)",
              seeded > 0 and kb._cursor is not None,
              f"{seeded} painted row(s), cursor="
              + (kb._cursor.item.title if kb._cursor else "None"))

        def cursor_rows():
            """Restricted to the MASTER pane of the board region: `▸` is also
            the tab row's marker, so a whole-frame count is always >= 1."""
            x, y, w, h = kb.region
            mw = kn.panes(w)[0]
            return [r for r in screen_text(napp)[y: y + h]
                    if kn.CUR in r[x: x + mw]]

        # the FIRST `down` moves focus off the hero and onto the board, which
        # is app-level behaviour this pass did not touch; the move under test
        # is the one after that. Measured, not assumed: the check below names
        # the row index it started from.
        await pilot.press("down")
        await settle(napp, pilot, "nord nav enter")
        first = kb._cursor
        await pilot.press("down")
        await settle(napp, pilot, "nord nav down")
        d1 = kb._cursor
        check("nord nav: `down` moves the cursor to the next master row",
              d1 is not None and first is not None and d1 is not first
              and d1.col == first.col and d1.row == first.row + 1,
              f"row {first.row if first else None} -> "
              f"{d1.row if d1 else None} ({d1.item.title if d1 else None!r})")
        after = "\n".join(screen_text(napp))
        check("nord nav: ... and the DETAIL followed it (the list drives the "
              "pane — HIERARCHY.md's pattern, not a static pick)",
              " ".join(d1.item.title.upper()[:8]) in after,
              f"{' '.join(d1.item.title.upper()[:8])!r}")
        check("nord nav: still exactly ONE cursor after the move (one writer, "
              "so two cursors are impossible by construction)",
              len(cursor_rows()) == 1, f"{len(cursor_rows())} row(s)")
        await pilot.press("right")
        await settle(napp, pilot, "nord nav right")
        d2 = kb._cursor
        check("nord nav: `right` still crosses to the next PHASE in the "
              "stacked tree (the geometry-based lateral move survived the "
              "third branch)",
              d2 is not None and d1 is not None and d2.col > d1.col,
              f"col {d1.col if d1 else None} -> {d2.col if d2 else None}")
        check("nord nav: and STILL exactly one cursor after the lateral move",
              len(cursor_rows()) == 1, f"{len(cursor_rows())} row(s)")

    print("\n== APP LEVEL: instrument's SCOPE on the live board (`layout`)")
    (W / "prototypes" / "out" / "trace_instrument_118.txt").write_text(
        boards["instrument"], encoding="utf-8")
    ib = body_rows(boards["instrument"])
    IORG, ITICK, IGRAT, IOVER = (LG.Instrument.ORIGIN, LG.Instrument.TICK,
                                 LG.Instrument.GRAT, LG.Instrument.OVER)
    iax = [i for i, r in enumerate(ib) if IORG in r]
    itr = [i for i, r in enumerate(ib) if IGRAT in r]
    # SENTINEL "" FOR THE AXIS ROW ITSELF, hoisted to the top of the block so
    # ONE fetch serves every law and setup line under it. THIS IS WHERE M2a
    # DIED — not here, but sixteen lines down, in an ASSIGNMENT rather than
    # in a law. The law immediately below went red exactly as it should
    # ("one axis row" — 0 is not 1) and `check` REPORTS AND RETURNS, which is
    # what it is for; the setup line then ran anyway on an empty `iax` and
    # took the remaining 600-odd checks with it. A check above a setup line
    # is not a guard, and eleven sites in this file sat behind that comfort.
    #
    # Hoisting the ROW is what makes "" usable at all: a sentinel INDEX into
    # `ib` has no right value, because every integer indexes SOME row — so
    # `ib[-1]` would have measured the wrong row silently, which is a worse
    # outcome than the crash. "" carries no ORIGIN, no TICK and no label, so
    # every count is 0 and every `at()` is -1, which are the red values.
    iaxrow = nth([ib[i] for i in iax], 0, "")
    check("instrument: the fixture is on screen (probe self-check)",
          any("Renew TLS certificate" in r for r in ib)
          and any("Fix checkout 500 error" in r for r in ib))
    check("instrument @118: the reticle reaches the REAL board — one axis row, "
          "carrying its week ticks and their unit labels",
          len(iax) == 1 and iaxrow.count(IORG) == 3
          and iaxrow.count(ITICK) >= 5 and "7d" in iaxrow
          and "21d" in iaxrow,
          f"{len(iax)} axis row(s), {iaxrow.count(ITICK)} ticks")
    # a board ROW is shared by all three columns, so four cards per column is
    # four trace ROWS carrying three fields each — counting rows as fields is
    # the mistake the first version of this check made
    check("instrument @118: every task hangs a trace off it — four trace rows, "
          "each carrying the field of every column that bought a scale",
          len(itr) >= 4 and all(ib[j].count(IGRAT) >= 4 for j in itr[:4]),
          f"{len(itr)} trace row(s), "
          f"{[ib[j].count(IGRAT) for j in itr[:4]]} graticule marks each")
    # THE ORIGIN COLUMN, read off the COMPOSITED FRAME rather than inferred
    # from the TCSS: the seat inset is a claim about kanban.py's budget and
    # about the base kit's `.col-head` rule, and a kit-level check can only
    # prove the kit is self-consistent (the ONE MEASURE block above asserts
    # the seats themselves, for every language and both widths).
    ax_cols = sorted(i for i, ch in enumerate(iaxrow) if ch == IORG)
    kI = LG.kit("instrument")

    # SENTINEL "" again, and for the same reason: `itr` is the trace rows,
    # `lead` is indexed by column below, and "" is shorter than every column
    # so `lead[c]` cannot be reached — the `all()` over an EMPTY `ax_cols`
    # is what the added leg below refuses.
    lead = nth([ib[j] for j in itr], 0, "")
    check("instrument @118: the head's axis origin and its samples' origin "
          "share a SCREEN COLUMN — the ticks a card hangs off are the ticks "
          "its head drew, proved on the render and not on the stylesheet",
          # THE LEG `ax_cols and` IS NEW AND IT IS PART OF THIS CURE, not a
          # bonus. Both halves are `all(...)` over `ax_cols`, and `all([])`
          # is True — so on the input this whole block exists to refuse (an
          # axis that drew no origin) the law did not raise, it PASSED. That
          # is the sibling defect of the crash below it, found by reading
          # what M2a would report once the crash was gone. `gr_cols and ...`
          # four lines down is the same leg, already written.
          bool(ax_cols)
          and all(nth(lead, c, "") in (kI.LATT, kI.FULL, kI.HALF)
                  for c in ax_cols[:1])
          and all(any(r[c] in (kI.LATT, kI.FULL, kI.HALF)
                      for r in (ib[j] for j in itr) if len(r) > c)
                  for c in ax_cols),
          f"origin columns {ax_cols}")
    # the week ticks fall on the SAME cells in the axis and in every trace
    ax_ticks = [i for i, ch in enumerate(iaxrow) if ch == ITICK]
    gr_cols = sorted({i for j in itr for i, ch in enumerate(ib[j])
                      if ch == IGRAT})
    check("instrument @118: every graticule line stands on a cell the axis "
          "ticked (one geometry function, two renderers)",
          gr_cols and set(gr_cols) <= set(ax_ticks),
          f"graticule at {gr_cols[:6]}… ticks at {ax_ticks[:6]}…")
    # DATA, ON THE RENDER. The four backlog tasks are 3/5/8/9 days out, so the
    # four traces must be four DIFFERENT lengths. The flow sub-row they replace
    # drew phase progress and was identical for all four — that is the whole
    # argument for this pass, so it is asserted on the frame, not on the kit.
    # SENTINEL -1 for the LEADING COLUMN, argued the other way round from
    # the row above. A column index has no impossible value, so -1 is
    # chosen for what the SLICE beneath does with it: `ib[j][-1: -1 + H]`
    # is the empty string for every trace row, so every fill counts 0,
    # `lead_fills` is all-zeros and the law reds on `len(set(...)) == 4`
    # printing `fills=[0, 0, 0, 0]`. An axis with no origin has no
    # leading column, and that is what the FAIL line then says.
    lead_x = nth(ax_cols, 0, -1)
    lead_fills = [len([1 for ch in ib[j][lead_x: lead_x + kI.HORIZON + 2]
                       if ch in (kI.FULL, kI.HALF)]) for j in itr]
    check("instrument @118: the traces down the leading column are FOUR "
          "DIFFERENT lengths (3/5/8/9 days) — the sub-row they replaced drew "
          "phase progress and was identical for every card in the phase",
          len(set(lead_fills)) == len(lead_fills) >= 4, f"fills={lead_fills}")
    check("instrument @118: the overdue task is CLIPPED AND FLAGGED at the "
          "boundary, not clamped onto the origin — its reading still states "
          "the negative number",
          any("-2d" in r for r in ib) and any("-1d" in r for r in ib))
    bad_i118 = [len(r) for r in boards["instrument"].split("\n") if len(r) != 118]
    check("instrument @118x30: the frame never wraps (every row is 118 cells)",
          not bad_i118, f"bad={bad_i118[:3]}")
    # THE VERTICAL COST, measured rather than claimed
    ifl_i, _, _, _ = await capture("instrument", mutate=("layout", "flow"),
                                   board_path=str(fx))
    (W / "prototypes" / "out" / "trace_instrument_flow.txt").write_text(
        ifl_i, encoding="utf-8")
    fl_i = body_rows(ifl_i)
    n_titles = sum(1 for r in ib if "···" in r)
    n_titles_fl = sum(1 for r in fl_i if "···" in r)
    check("instrument: the reticle costs the board NOTHING vertically — the "
          "axis row is paid for by `.col-head`'s margin, and the same number "
          "of cards reach the screen as before",
          n_titles == n_titles_fl, f"{n_titles} card rows vs {n_titles_fl}")
    check("instrument.layout=flow keeps the board itself (probe self-check)",
          "Renew TLS certificate" in ifl_i)
    check("instrument.layout=flow strips the reticle from the LIVE board and "
          "brings the bench readout back (the negative control: the checks "
          "above CAN fail)",
          not any(IORG in r or IGRAT in r for r in fl_i)
          and any("⣿⣿⠒⠒⠒⠒" in r for r in fl_i))
    check("instrument.layout=flow changes the board outside the hero",
          ifl_i != boards["instrument"])
    # SAME WIDENING as the kit-level dispatch law above, and for the same
    # reason: `IORG` alone is a glyph test, and blueprint's dimension spans own
    # that glyph in a different mechanism. The leak this must catch is a
    # RETICLE — an origin carrying its week ticks, or a trace's graticule — so
    # that is the predicate. Its negative control is one line below.
    for name in TH.ORDER:
        if name == "instrument":
            continue
        body = "\n".join(body_rows(boards[name]))
        check(f"{name}: board carries no reticle (the scope is instrument's)",
              IGRAT not in body and IOVER not in body
              and not any(IORG in r and ITICK in r
                          for r in body_rows(boards[name])))
    check("... and that predicate CAN fail: instrument's own board satisfies "
          "it (negative control for the widened reticle test)",
          any(IORG in r and ITICK in r for r in ib) and any(IGRAT in r
                                                            for r in ib))
    # THE COLLISION CLAIM, MEASURED. The external spec assigned this token by
    # saying instrument "collides with darkside in greyscale". The darkside-rail
    # pass already refuted it with zero silhouette overlap; re-measured here so
    # the number moves with the code instead of being quoted from a past pass.
    idk = cell_diff(boards["instrument"], boards["darkside"])
    idk_fl = cell_diff(ifl_i, boards["darkside"])
    check("instrument vs darkside: nameable apart in greyscale (the spec's "
          "collision claim, RE-PROBED after the trace — still false, and the "
          "flow baseline is reported beside it so the movement is not hidden)",
          idk > 0.20, f"{idk:.1%} of board cells differ "
                      f"(under flow it was {idk_fl:.1%})")
    # NARROW REGIME: the drop rule is a real regime here, not a hypothetical —
    # at 80 the DONE column falls under the threshold and renounces its scale
    ib80, _, _, _ = await capture("instrument", board_path=str(fx),
                                  size=(80, 30))
    (W / "prototypes" / "out" / "trace_instrument_80.txt").write_text(
        ib80, encoding="utf-8")
    bad_i80 = [len(r) for r in ib80.split("\n") if len(r) != 80]
    check("instrument @80x30: the frame never wraps (every row is 80 cells)",
          not bad_i80, f"bad={bad_i80[:3]}")
    r80 = body_rows(ib80)
    ax80 = [i for i, r in enumerate(r80) if IORG in r]
    check("instrument @80x30: the reticle survives the narrow board, and the "
          "DROP RULE fires — two columns keep a scale, the third renounces it",
          len(ax80) == 1 and r80[ax80[0]].count(IORG) == 2,
          f"{r80[ax80[0]].count(IORG) if ax80 else 0} axis origin(s) of 3 columns")
    check("instrument @80x30: the renounced column falls back to the bench "
          "readout, never to a squeezed axis",
          any("⣿⣿⣿⣿⣿⣿" in r for r in r80))
    # ...and the heads stay TWO rows everywhere, so the columns' card stacks
    # start on one line. This is what the first render got wrong.
    hd80 = first_of(i for i, r in enumerate(r80) if "BACKLOG" in r)
    check("instrument @80x30: every column's first card starts on the SAME "
          "row — the head is two rows even where the scale is renounced",
          hd80 >= 0
          and len([1 for r in r80[hd80 + 2: hd80 + 3]
                   if r.count("…") >= 3]) == 1,
          repr(r80[hd80 + 2][:60]) if 0 <= hd80 + 2 < len(r80) else "no head")

    print("\n== APP LEVEL: corgi's MODE SURFACE on the live board (`layout`)")
    CG_TITLE = "Shut down legacy servers"

    def param_rows(board: str) -> list[str]:
        """The spec sheet's own rows, and only those: every declared code
        present, in `slots()` order. The tiles row also prints `DL`/`OV`
        pairs, so a search for one code would measure the chrome."""
        labs = [lab for lab, _ in LG.Corgi.PARAMS]
        out = []
        for r in body_rows(board):
            pos = [r.find(lab + " ") for lab in labs]
            if all(p >= 0 for p in pos) and pos == sorted(pos):
                out.append(r)
        return out

    cg_geo = {}
    for w in (118, 80):
        cb, _, _, _ = await capture("corgi", board_path=str(fx), size=(w, 30))
        (W / "prototypes" / "out" / f"strip_corgi_{w}.txt").write_text(
            cb, encoding="utf-8")
        bad = [len(r) for r in cb.split("\n") if len(r) != w]
        check(f"corgi @{w}: the frame never wraps (every row is {w} cells)",
              not bad, f"bad={bad[:3]}")
        rows = param_rows(cb)
        check(f"corgi @{w}: the spec sheet is on screen (probe self-check)",
              len(rows) >= 4, f"{len(rows)} param row(s)")
        # THE LEGIBILITY LAW, and the measured reason this token exists: the
        # 3-column board cut EVERY title at 80 cells ("RENEW TLS CERTIF…3d").
        # One full-width surface prints the fixture's longest title intact at
        # BOTH widths — which is the same claim swiss and darkside must make.
        check(f"corgi @{w}: the full-width surface keeps titles INTACT "
              f"(the columns board cut them at 80)",
              CG_TITLE.upper() in cb)
        # ONE GEOMETRY for the whole page (the ledger-ruling check's shape)
        geo = {tuple(r.find(lab + " ") for lab, _ in LG.Corgi.PARAMS)
               for r in rows}
        check(f"corgi @{w}: every param row shares ONE slot geometry "
              f"(identical cells down the page)",
              len(geo) == 1, f"{len(geo)} distinct geometries")
        cg_geo[w] = sorted(geo)[0] if geo else ()
        check(f"corgi @{w}: those cells are the ones `slots()` computed — "
              f"the renderer and the check read the SAME seat",
              bool(cg_geo[w]),
              f"cells={cg_geo[w]}")
    # ONE CELL IS ONE CELL: the slots are right-flushed, so a wider board buys
    # a longer TITLE MEASURE and nothing else — the values do not re-space
    check("corgi: width buys title measure, not a re-spaced sheet (the slot "
          "block is the same size at 118 and at 80)",
          bool(cg_geo[118]) and bool(cg_geo[80])
          and ([b - a for a, b in zip(cg_geo[118], cg_geo[118][1:])]
               == [b - a for a, b in zip(cg_geo[80], cg_geo[80][1:])]),
          f"118={cg_geo[118]} 80={cg_geo[80]}")

    # -- THE MODE STRIP ON THE FRAME — and the defect it fixes --------------
    # This is not a cosmetic assertion. `widget.tcss` gives `#tabs`
    # `height: 1` and corgi's composition puts a `border-top` on it, so under
    # the previous composition the border ate the widget's only content row:
    # `[1] B O A R D` was in the renderable and on NO screen row, at any size.
    # Both facts are asserted, because "it renders" and "the user can see it"
    # are different claims (the twenty-third pass's reachability lesson).
    async def strip_row(mutate=None):
        from app import TaskboardWidget as _TWc
        old = None
        if mutate:
            old = TH.THEMES["corgi"].get(mutate[0])
            TH.THEMES["corgi"][mutate[0]] = mutate[1]
        try:
            app_ = _TWc(board_path=str(fx))
            async with app_.run_test(size=(118, 30)) as pilot:
                await pilot.pause()
                app_.notify = lambda *a, **kw: None
                app_.set_theme("corgi")
                await pilot.pause()
                app_.redraw()
                await settle(app_, pilot, "corgi tabs")
                fr = screen_text(app_)
                # the CONTENT region, not `region`: the aluminium border-top
                # is inside the widget's outer box and always paints, so the
                # outer box can never answer "did the strip get a row?"
                r = app_.query_one("#tabs").content_region
                band = [fr[y][r.x: r.x + r.width]
                        for y in range(r.y, min(r.y + r.height, len(fr)))]
                return band, str(app_.query_one("#tabs").render())
        finally:
            if mutate:
                if old is None:
                    TH.THEMES["corgi"].pop(mutate[0], None)
                else:
                    TH.THEMES["corgi"][mutate[0]] = old

    band, renderable = await strip_row()
    painted = [r for r in band if r.strip()]
    check("corgi: the mode strip REACHES A SCREEN ROW (its seat used to be "
          "one row tall with a border-top on it, so the border ate the strip "
          "and it rendered nowhere)",
          len(painted) == 1, f"{len(painted)} painted row(s) of {len(band)}")
    check("corgi: the strip on the frame names EVERY mode, numbered by the "
          "key that switches it",
          bool(painted) and all(f"[{i + 1}]" in painted[0] for i in range(4))
          and all(m in painted[0].replace(" ", "")
                  for m in ("BOARD", "LANES", "AGENDA", "GANTT")),
          repr(painted[0] if painted else ""))
    check("corgi: the MODE ON SCREEN is the one lit, and it says so in "
          "GREYSCALE (the board mode is the letterspaced one)",
          bool(painted) and " ".join("BOARD") in painted[0]
          and " ".join("LANES") not in painted[0])
    check("corgi: the strip fits its seat — ONE content row, so nothing can "
          "wrap out of sight under it",
          len(band) == 1, f"{len(band)} content row(s)")
    fband, frenderable = await strip_row(mutate=("layout", "flow"))
    check("corgi.layout=flow: the strip goes back to naming ONLY the active "
          "mode — AND its seat has NO CONTENT ROW AT ALL, so that markup "
          "reaches no screen row. This is the defect the token fixes, "
          "asserted rather than described",
          "[1] B O A R D" in frenderable and len(fband) == 0,
          f"renderable={frenderable!r} content rows={len(fband)}")

    # -- THE VERTICAL TRADE, measured rather than argued --------------------
    from app import TaskboardWidget as _TWv
    from kanban import KanbanBoard as _KBv

    async def board_geo(mutate=None):
        old = None
        if mutate:
            old = TH.THEMES["corgi"].get(mutate[0])
            TH.THEMES["corgi"][mutate[0]] = mutate[1]
        try:
            a = _TWv(board_path=str(fx))
            async with a.run_test(size=(118, 30)) as pilot:
                await pilot.pause()
                a.notify = lambda *aa, **kw: None
                a.set_theme("corgi")
                await pilot.pause()
                a.redraw()
                await settle(a, pilot, "corgi geo")
                kb = a.query_one(_KBv)
                fr = screen_text(a)
                # TASK ROWS ON SCREEN, asked of the compositor rather than of
                # the text: under `flow` three columns share a screen row and
                # under `strip` they do not, so any row-counting heuristic
                # would compare two different things. A card the compositor
                # is drawing, whose clipped area carries ink, is on screen.
                from kanban import TaskCard as _TC
                drawn = a.screen._compositor.visible_widgets
                seen = 0
                for c in a.query(_TC):
                    box = drawn.get(c)
                    if box is None:
                        continue
                    ar = box[0].intersection(box[1])
                    if ar.width and ar.height and any(
                            fr[y][ar.x: ar.x + ar.width].strip()
                            for y in range(ar.y,
                                            min(ar.y + ar.height, len(fr)))):
                        seen += 1
                return tuple(kb.region), "\n".join(fr), seen
        finally:
            if mutate:
                if old is None:
                    TH.THEMES["corgi"].pop(mutate[0], None)
                else:
                    TH.THEMES["corgi"][mutate[0]] = old

    sreg, sframe, sseen = await board_geo()
    freg, fframe, fseen = await board_geo(mutate=("layout", "flow"))
    (W / "prototypes" / "out" / "strip_corgi_flow.txt").write_text(
        fframe, encoding="utf-8")
    check("corgi: the mode surface is BIGGER than the composition it "
          "replaced — the reclaimed margins are what pay for the sheet",
          sreg[3] > freg[3], f"strip {sreg[3]} rows vs flow {freg[3]} rows")
    # THE TRADE, and it is a TRADE, not a win. A sections board cannot
    # amortize its phase heads across three columns the way a columns board
    # does, so the reclaimed rows buy back almost — not quite — what the
    # stacking costs. The bound is stated as "no worse than one row", which
    # is a claim that CAN fail, rather than as "more", which would be false.
    check("corgi: the sheet costs at most ONE task row against the 3-column "
          "board (the reclaimed margins pay for the stacking, nearly)",
          sseen >= fseen - 1,
          f"strip {sseen} card(s) on screen vs flow {fseen}")
    check("corgi: and every row it does print is WHOLE — the columns cut "
          "titles at 80 cells, the sheet cuts none at either width",
          len(param_rows(sframe)) >= 7,
          f"{len(param_rows(sframe))} param rows on screen")
    check("corgi.layout=flow brings the COLUMNS skeleton back — the three "
          "phase heads share ONE row, which the sheet stacks (the negative "
          "control: the checks above CAN fail)",
          any(all(p in r for p in ("B A C K L O G", "D O I N G", "D O N E"))
              for r in body_rows(fframe))
          and not any(all(p in r for p in ("B A C K L O G", "D O I N G"))
                      for r in body_rows(sframe)))
    check("corgi.layout=flow removes the param strip from the live board",
          not param_rows(fframe))
    check("corgi.layout=flow keeps the board itself (probe self-check)",
          CG_TITLE.upper() in fframe)
    # NO LEAKAGE: the spec sheet is corgi's alone
    for name in TH.ORDER:
        if name == "corgi":
            continue
        check(f"{name}: board carries no param strip (the sheet is corgi's)",
              not param_rows(boards[name]))

    print("\n== APP LEVEL: the LEDGER page — one ruling, unbroken, legible")
    RULE_V, RULE_H = LG.Ledger.RULE_V, LG.Ledger.RULE_HEAD

    def page_of(board: str):
        """The POSTINGS, and only those. The tabs row and the meter's flow row
        also carry `│`, so a naive `│`-search measures the chrome and proves
        nothing — the page begins at the first head rule."""
        rows = body_rows(board)
        heads = [i for i, r in enumerate(rows) if RULE_H * 20 in r]
        if not heads:
            return [], None
        return ([r for r in rows[heads[0]:] if r.count(RULE_V) >= 2],
                rows[heads[0]])

    for w in (118, 80):
        lb, _, _, _ = await capture("ledger", board_path=str(fx), size=(w, 30))
        (W / "prototypes" / "out" / f"ledger_{w}.txt").write_text(
            lb, encoding="utf-8")
        bad = [len(r) for r in lb.split("\n") if len(r) != w]
        check(f"ledger @{w}: the frame never wraps (every row is {w} cells)",
              not bad, f"bad={bad[:3]}")
        entries, hrule = page_of(lb)
        check(f"ledger @{w}: the page is on screen (probe self-check)",
              len(entries) >= 4 and hrule is not None,
              f"{len(entries)} posting row(s)")
        ruling = {tuple(i for i, ch in enumerate(r) if ch == RULE_V)
                  for r in entries}
        check(f"ledger @{w}: every posting shares ONE ruling (identical cells)",
              len(ruling) == 1, f"{len(ruling)} distinct rulings")
        cells = sorted(ruling)[0] if ruling else ()
        run = max(re.findall(f"{RULE_H}+", hrule or ""), key=len, default="")
        start = at(hrule or "", run) if run else -1
        check(f"ledger @{w}: the head rule is ONE unbroken run",
              len(run) >= w - 12, f"{len(run)} of {w}")
        check(f"ledger @{w}: the head rule starts where the postings start",
              start == cells[0] - LG.Ledger.GUTTER if cells else False,
              f"rule@{start} first-rule@{cells[0] if cells else '-'}")
        # EXACT (PENDING item 4, cured): head and postings are handed one
        # measure on one seat, so the rule CLOSES on the closing rule — this
        # was `<=2` while the head was budgeted apart and the rule overshot.
        check(f"ledger @{w}: the head rule closes ON the closing rule, to the "
              f"cell",
              cells and start + len(run) - 1 == cells[-1],
              f"rule ends {start + len(run) - 1}, closing rule {cells[-1] if cells else '-'}")
        check(f"ledger @{w}: titles survive the ruling INTACT (legibility law)",
              "Shut down legacy servers" in lb)
    for name in TH.ORDER:
        if name == "ledger":
            continue
        check(f"{name}: board carries no money columns (the ruling is ledger's)",
              not page_of(boards[name])[0])
    # the ruling must DISPATCH: back to the base default and it must vanish
    # from the real board, not merely from the kit
    fl, _, _, _ = await capture("ledger", mutate=("layout", "flow"),
                                board_path=str(fx))
    check("ledger.layout=flow removes the ruling from the live board",
          not page_of(fl)[0])
    check("ledger.layout=flow keeps the page itself (probe self-check)",
          "Shut down legacy servers" in fl)
    check("ledger: the margin marker reaches a rendered surface (the cursor)",
          LG.Ledger.CUR in configs["ledger"])

    print("\n== APP LEVEL: solari's DEPARTURE BOARD — bands, seams, no bars")
    INK_S = TH.THEMES["solari"]["ink"]
    GND_S = TH.THEMES["solari"]["ground"]

    def runs_of(cells: dict, y: int, w: int, want_bg: str):
        """The contiguous columns on row `y` whose GROUND is `want_bg`. This
        is the only sound way to measure a reverse-video band: most of a
        band's cells are blank, so a text search finds nothing and a
        foreground map finds only the caption."""
        xs = [x for x in range(w) if cells.get((y, x), ("", ""))[1] == want_bg]
        return (min(xs), max(xs)) if xs else None

    for w in (118, 80):
        rows, cells, kbr = await capture_bg("solari", str(fx), size=(w, 30))
        (W / "prototypes" / "out" / f"schedule_solari_{w}.txt").write_text(
            "\n".join(rows), encoding="utf-8")
        bad = [len(r) for r in rows if len(r) != w]
        check(f"solari @{w}: the frame never wraps (every row is {w} cells)",
              not bad, f"bad={bad[:3]}")
        board_ys = range(kbr[1], min(kbr[1] + kbr[3], len(rows)))
        seams = [y for y in board_ys
                 if set(rows[y].strip()) == {LG.Solari.SEAM}]
        bands = [y for y in board_ys if runs_of(cells, y, w, INK_S)]
        check(f"solari @{w}: the schedule is on screen (probe self-check)",
              len(seams) >= 3 and len(bands) >= 1,
              f"{len(seams)} seam(s), {len(bands)} band(s)")
        sx = {(min(i for i, ch in enumerate(rows[y])
                   if ch == LG.Solari.SEAM),
               max(i for i, ch in enumerate(rows[y])
                   if ch == LG.Solari.SEAM)) for y in seams}
        check(f"solari @{w}: every seam shares ONE extent (the grid)",
              len(sx) == 1, f"{sorted(sx)}")
        bx = {runs_of(cells, y, w, INK_S) for y in bands}
        check(f"solari @{w}: every band shares ONE extent too",
              len(bx) == 1, f"{sorted(bx)}")
        # SENTINEL (-1, -1) FOR BOTH EXTENTS, and it is chosen against the
        # three laws that read them: two are equalities between the extents
        # and one compares their opening cells. A shared sentinel would make
        # all three PASS by making both sides equal — the `-1 == -1` trap
        # pass 66 named for `at()`, in its other clothing. So the pair is
        # DIFFERENT on each side: a seam that drew nothing is (-1, -1) and a
        # band that drew nothing is (-2, -2), so `band_ex == seam_ex` reds,
        # `band_ex[1] == seam_ex[1]` reds, and the detail prints both.
        # `sx` and `bx` are set comprehensions over `seams` / `bands`, so
        # they are empty exactly when those are — which the probe self-check
        # above reports and does not prevent.
        seam_ex = nth(sorted(sx), 0, (-1, -1))
        band_ex = nth(sorted(bx), 0, (-2, -2))
        check(f"solari @{w}: band and seam CLOSE on the same cell — the "
              f"columns ride that edge",
              band_ex[1] == seam_ex[1], f"band {band_ex} seam {seam_ex}")
        # ... and they no longer disagree on the left edge either. That cell
        # was kanban.py's, not solari's — the head was handed `avail - 4` and
        # took no seat inset while a card sized itself from its own content
        # box (PENDING item 4, cured at the source). The closing edges used to
        # agree by ARITHMETIC LUCK (110 drawn from x, 109 drawn from x+1); the
        # band and the seam are now one measure on one origin, so BOTH edges
        # are exact and the agreement survives a board with no scrollbar.
        check(f"solari @{w}: the band OPENS on the seam's own cell too — the "
              f"grid is one measure, not two that happen to meet",
              seam_ex[0] == band_ex[0],
              f"band starts {band_ex[0]}, seam starts {seam_ex[0]} "
              f"(delta {seam_ex[0] - band_ex[0]})")
        check(f"solari @{w}: band and seam are the SAME extent, cell for cell",
              band_ex == seam_ex, f"band {band_ex} seam {seam_ex}")
        # REVERSE VIDEO, measured: ground is the ink and ink is the ground
        # SENTINEL -1 FOR THE BAND ROW, and it works because of what the
        # law beneath asks: `fgs == {GND_S}`. With no band, `band_ex` is
        # (-2, -2), `range(-2, -2)` is empty, `fgs` is the EMPTY SET, and
        # `set() != {GND_S}` — red, with `fg(s) on the band: []` printed.
        # -1 never reaches `rows[by]` because the range never yields.
        by = nth(bands, 0, -1)
        fgs = {cells[(by, x)][0] for x in range(*band_ex)
               if rows[by][x].strip()}
        check(f"solari @{w}: the band is REVERSE VIDEO on the render "
              f"(bg={INK_S}, ink={GND_S})",
              fgs == {GND_S}, f"fg(s) on the band: {sorted(fgs)}")
        check(f"solari @{w}: no OTHER row on the board wears that ground "
              f"(the band is the head's alone)",
              all(y in bands or not runs_of(cells, y, w, INK_S)
                  for y in board_ys))
        # DIGITS, NEVER BARS — asked of the seam grid's own columns, so the
        # footer's `▏` and the scroll bar's thumb (which lives outside the
        # grid) cannot answer for the language
        strip_ = "\n".join(rows[y][seam_ex[0]: seam_ex[1] + 1]
                           for y in board_ys)
        check(f"solari @{w}: not one bar or braille glyph inside the grid",
              not has_bar(strip_),
              repr([ch for ch in set(strip_) if has_bar(ch)]))
        check(f"solari @{w}: and not one rule glyph either",
              not any(ch in RULES for ch in strip_),
              repr([ch for ch in set(strip_) if ch in RULES]))
        check(f"solari @{w}: a title survives INTACT (legibility law)",
              "RENEW TLS CERTIFICATE" in "\n".join(rows))
        check(f"solari @{w}: the status column is on screen and reads as a "
              f"word", "ON TIME" in "\n".join(rows) or "BOARDING" in
              "\n".join(rows))
        check(f"solari @{w}: departures reach the screen (density, printed "
              f"rather than claimed)", len(seams) >= 3,
              f"{len(seams)} departure row(s) on {w}x30")

    # 60 CELLS IS A DIFFERENT REGIME, and the honest thing is to say so
    # rather than assert a board there: `app.size_class()` calls anything
    # under 80 the WIDGET posture and widget.tcss gives `#kb` `display: none`,
    # so at 60 there IS no board — for every language. What must still hold is
    # that solari's widget posture renders without wrapping a single row.
    rows60, cells60, kbr60 = await capture_bg("solari", str(fx), size=(60, 30))
    (W / "prototypes" / "out" / "schedule_solari_60.txt").write_text(
        "\n".join(rows60), encoding="utf-8")
    check("solari @60: the frame never wraps (every row is 60 cells)",
          not [len(r) for r in rows60 if len(r) != 60])
    check("solari @60: the WIDGET posture is what renders — there is no "
          "board under 80 cells, for any language (stated, not asserted "
          "around)", kbr60[3] == 0 or kbr60[2] == 0, f"kb region {kbr60}")
    check("solari @60: the odometer meter still reads (the identity survives "
          "the narrow posture)",
          any("LOAD" in r for r in rows60)
          and any(ch.isdigit() for r in rows60 for ch in r))
    # REPLACED, not weakened, by the thirty-sixth pass. This used to scan the
    # WHOLE 60-cell frame for bar glyphs — sound while solari's hero was
    # `plain`, and wrong the moment it DREW: a numeral built out of block
    # glyphs is TYPE, not a bar, and the board-region form of this same law
    # (above) already scopes itself to the seam grid for exactly that reason.
    # The law is about the QUANTITY mechanism, so it is now asserted with the
    # display type taken away — and then the type is held to being the ONLY
    # source of block glyphs on the posture, which is the stronger claim.
    plain60, _, _ = await capture_bg("solari", str(fx), size=(60, 30),
                                     mutate=("hero", "plain"))
    check("solari @60: with the display type taken away, not one bar or "
          "braille glyph survives — the QUANTITY mechanism draws digits",
          not has_bar("\n".join(plain60)),
          repr([ch for ch in set("".join(plain60)) if has_bar(ch)]))
    FLAP_TYPE = {BS.FLAP_INK, BS.FLAP_SEAM_INK, BS.FLAP_SEAM_FACE}
    bars60 = {ch for ch in set("".join(rows60)) if has_bar(ch)}
    check("solari @60: and every bar-family glyph on the real posture belongs "
          "to the flap DISPLAY TYPE — nothing else on the screen drew one",
          bars60 and bars60 <= FLAP_TYPE, repr(sorted(bars60)))
    check("solari @60: the display type is really on that frame (probe "
          "self-check — the two checks above can fail)",
          BS.FLAP_INK in "".join(rows60))

    # THE SELECTION BAND, driven rather than assumed
    rows, cells, kbr = await capture_bg("solari", str(fx), size=(118, 30),
                                        focus_card=True)
    board_ys = range(kbr[1], min(kbr[1] + kbr[3], len(rows)))
    amber_rows = [y for y in board_ys if runs_of(cells, y, 118, AMBER)]
    check("solari: the SELECTED row inverts to amber (the band mechanism)",
          len(amber_rows) >= 1, f"{len(amber_rows)} amber row(s)")
    check("solari: and it is exactly ONE row of departures, not the page",
          len(amber_rows) <= 2, f"{amber_rows}")
    if amber_rows:
        ay = amber_rows[0]
        ax = runs_of(cells, ay, 118, AMBER)
        inks = {cells[(ay, x)][0] for x in range(ax[0], ax[1] + 1)
                if rows[ay][x].strip()}
        check("solari: the selected row's ITEM inverts to the GROUND colour "
              "(it is the one untagged field, which is what makes the band "
              "legible instead of cream-on-amber)",
              GND_S in inks, f"{sorted(inks)}")
        # LEGIBILITY ON THE BAND is the law that rewrote this language's
        # severity mechanism, so it is asserted rather than trusted: every
        # painted glyph on the selected row against the ground it actually
        # sits on. The first draft printed `#f5a300` on `#f5a300` here.
        worst, where = 99.0, ""
        for x in range(ax[0], ax[1] + 1):
            fg, bg = cells[(ay, x)]
            if not rows[ay][x].strip() or not fg or not bg:
                continue
            r = ((max(lum(fg), lum(bg)) + 0.05)
                 / (min(lum(fg), lum(bg)) + 0.05))
            if r < worst:
                worst, where = r, f"{rows[ay][x]!r} {fg} on {bg}"
        check("solari: every glyph on the SELECTED row clears 2.5:1 against "
              "its own ground (the defect that moved severity onto the cell "
              "face)", worst >= 2.5, f"worst {worst:.2f}:1 — {where}")
    unfocused, ucells, ukbr = await capture_bg("solari", str(fx),
                                               size=(118, 30))
    u_ys = range(ukbr[1], min(ukbr[1] + ukbr[3], len(unfocused)))
    # WITHOUT a selection the only amber ground left on the board is a LIT
    # DEPARTURE CELL — never a row. Measured as runs, so a whole row going
    # amber (the old selection mechanism leaking) fails here.
    lit = []
    for y in u_ys:
        xs = [x for x in range(118)
              if ucells.get((y, x), ("", ""))[1] == AMBER]
        if xs:
            lit.append((y, min(xs), max(xs) - min(xs) + 1))
    check("solari: with no selection, amber survives ONLY as lit departure "
          "cells (never a row)",
          all(n <= LG.Solari.DUE_W for _, _, n in lit),
          f"{lit}")
    check("solari: ... and every lit cell stands on the DUE field's own "
          "origin (the geometry seat, not a stray tint)",
          len({x for _, x, _ in lit}) <= 1, f"{sorted({x for _, x, _ in lit})}")
    check("solari: a lit cell is really on screen (probe self-check — this "
          "section can fail)", bool(lit), f"{len(lit)} lit cell run(s)")

    # DISPATCH on the live board, both directions
    for name in TH.ORDER:
        if name == "solari":
            continue
        check(f"{name}: board carries no seam grid (the schedule is solari's)",
              not any(set(r.strip()) == {LG.Solari.SEAM}
                      for r in body_rows(boards[name]) if r.strip()))
    sf, _, _, _ = await capture("solari", mutate=("layout", "flow"),
                                board_path=str(fx))
    check("solari.layout=flow removes the seam grid from the live board",
          not any(set(r.strip()) == {LG.Solari.SEAM}
                  for r in body_rows(sf) if r.strip()))
    check("solari.layout=flow keeps the board itself (probe self-check)",
          "Shut down legacy servers" in sf)
    check("solari.layout=flow brings the COLUMNS skeleton back (the negative "
          "control: the sections checks above CAN fail)",
          "Renew TLS certificate" in sf)

    print("\n== APP LEVEL: the BLUEPRINT sheet — spans, leaders, one knockout")

    def knock_of(cells: dict, rows: list[str], w: int, bg: str):
        """Contiguous RUNS of cells wearing `bg` as their ground, over the whole
        frame. A knockout's evidence is the ground it paints and most of its
        cells may be blank, so text and foreground maps both answer nothing —
        and RUNS, not rows, because "exactly one knockout" is a claim about
        distinct reversed blocks."""
        out = []
        for y in range(len(rows)):
            x = 0
            while x < w:
                if cells.get((y, x), ("", ""))[1] == bg:
                    x0 = x
                    while x < w and cells.get((y, x), ("", ""))[1] == bg:
                        x += 1
                    out.append((y, x0, x - 1))
                else:
                    x += 1
        return out

    # TWO MORE FIXTURES, and they exist because the standard seed cannot prove
    # two of this language's laws. Its only past-due tasks are ALSO blocked, so
    # `kanban.py` chips them `blk` and the sheet hatches them — the alert hue
    # reaches no row at all, and both held rows sit in DOING, below the fold at
    # 30 screen rows. Stated rather than asserted around.
    #
    # AND THEY ARE THIS HARNESS'S OWN FILES, WHICH IS THE WHOLE OF F-17.
    # The late one was written to `_fixture_late.json` — the ONE name under
    # `prototypes/out/` that `.gitignore` names back in, because it is the
    # committed fixture all 22 frames in `prototypes/gallery/` were swept
    # from. Two different artefacts wore one filename: a tracked INPUT that
    # must never move, and a derived PROBE rebuilt on every run. So running
    # the language harness silently re-dated the capture's fixture (measured:
    # +33 days on 12 of 16 tasks — `date.today()` minus `FROZEN`) and every
    # frame in the gallery stopped reproducing. That is the symptom
    # `export_to_skill.py:copy_captures` already describes in its docstring
    # without naming the culprit.
    #
    # THE CURE IS THE PRIVATE PATH, NOT A FROZEN CLOCK, and the choice is
    # between the two `inc21.md` §4g put on the table. Pinning `date.today()`
    # to `capture_languages.FROZEN` would make the WRITE idempotent and leave
    # the COLLISION in place: this harness would still own a tracked file it
    # has no business owning, one edit to either concept away from the same
    # defect. It would also drag `freeze_clock()` — which repoints
    # `default_board_path` and stamps an mtime — across 10854 checks measured
    # against a live clock, to fix a name. These two are PROBES; probes belong
    # in the scratch yard under names nothing else reads.
    # `_fixture_late.json` keeps its bytes and loses its writer.
    fl = W / "prototypes" / "out" / "_verify_late.json"
    fc = W / "prototypes" / "out" / "_verify_calm.json"
    late_seed = json.loads(fx.read_text(encoding="utf-8"))
    calm_seed = json.loads(fx.read_text(encoding="utf-8"))
    today = date.today()
    past = [t for t in late_seed["tasks"]
            if t.get("due_date") and t["due_date"] < today.isoformat()
            and not t.get("archived")]
    check("the late fixture starts from two past-due tasks (probe self-check)",
          len(past) >= 2, f"{len(past)}")
    for i, t in enumerate(past):
        t["phase"] = "Backlog"             # onto the first page of the sheet
        t["blocked"] = (i == 0)            # ONE held, the rest genuinely late
    fl.write_text(json.dumps(late_seed), encoding="utf-8")
    for t in calm_seed["tasks"]:
        t["blocked"] = False
        if t.get("due_date") and t["due_date"] <= today.isoformat():
            t["due_date"] = (today + timedelta(days=7)).isoformat()
    fc.write_text(json.dumps(calm_seed), encoding="utf-8")
    # `<= today`, not `< today`: a task due TODAY is ALERT to `app.redraw`'s
    # own hero severity, which is the app's ration and not this language's. The
    # calm fixture has to clear both or the whole-frame alert check below would
    # be measuring the hero instead of the sheet.
    check("the calm fixture really leaves nothing overdue, nothing due today "
          "and nothing held",
          not any(t.get("blocked") for t in calm_seed["tasks"])
          and not any(t.get("due_date") and t["due_date"] <= today.isoformat()
                      for t in calm_seed["tasks"]))

    for w in (118, 80):
        rows, cells, kbr = await capture_bg("blueprint", str(fl), size=(w, 30))
        (W / "prototypes" / "out" / f"sheet_blueprint_{w}.txt").write_text(
            "\n".join(rows), encoding="utf-8")
        frame = "\n".join(rows)
        bad = [len(r) for r in rows if len(r) != w]
        check(f"blueprint @{w}: the frame never wraps (every row is {w} cells)",
              not bad, f"bad={bad[:3]}")
        # THE SHEET's own cells: the board region minus the column a vertical
        # scroll bar takes, which stands outside the drawing
        sheet = [r[kbr[0]: kbr[0] + max(0, kbr[2] - 1)]
                 for r in rows[kbr[1]: kbr[1] + kbr[3]]]
        spans = [r for r in sheet if BP.OPEN in r and BP.CLOSE in r]
        leads = [r for r in sheet if r.strip().startswith(BP.LEAD + BP.EXT)]
        check(f"blueprint @{w}: the sheet is on screen (probe self-check — "
              f"spans and extension leaders both drawn)",
              len(spans) >= 4 and len(leads) >= 3,
              f"{len(spans)} span row(s), {len(leads)} leader row(s)")
        stray = sorted({ch for ch in "\n".join(sheet) if ch in BOXCHARS}
                       - BP_OK)
        check(f"blueprint @{w}: NOT ONE containing box on the sheet — no "
              f"vertical, no junction, nothing outside the ten declared glyphs",
              not stray, f"stray={stray}")
        # the head's span and its items' spans stand in ONE column — EXACTLY,
        # since kanban.py hands both surfaces one measure on one seat
        # (PENDING item 4, cured). This was bounded to a cell while the head
        # was budgeted `avail - 4` and a card sized itself from its own box.
        heads = [r for r in sheet if r.strip().split(" ")[0] in
                 ("BACKLOG", "DOING", "REVIEW", "DONE") and BP.OPEN in r]
        check(f"blueprint @{w}: the phase head carries its own dimension span",
              bool(heads), f"{len(heads)} head span row(s)")
        if heads and spans:
            hx = at(heads[0], BP.OPEN)
            ix = [at(r, BP.OPEN) for r in spans if r not in heads]
            check(f"blueprint @{w}: every item's span stands on ONE column",
                  len(set(ix)) == 1, f"{sorted(set(ix))}")
            check(f"blueprint @{w}: and the head's span opens on THAT column, "
                  f"to the cell — one measure, one seat",
                  # THE CONDITION WAS ALREADY RIGHT (`ix and ...`) AND THE
                  # DETAIL WAS NOT, which is the half of this class that is
                  # easiest to write and hardest to see: a DETAIL argument is
                  # evaluated on every call, pass or fail, so a correct
                  # condition guarding an unguarded detail is a law that
                  # kills the run while REPORTING PASS. Sentinel -2 because
                  # `at()` already owns -1 for "not found", and the two
                  # emptinesses are different facts: -1 is a span row with no
                  # opener, -2 is no item span rows at all.
                  ix and hx == nth(ix, 0, -2),
                  f"head@{hx} items@{nth(ix, 0, -2)}")
        check(f"blueprint @{w}: a title survives INTACT (legibility law — the "
              f"sheet letters in caps, it never cuts)",
              "COMPRESS DATABASE BACKUPS" in frame
              and "RENEW TLS CERTIFICATE" in frame)
        check(f"blueprint @{w}: the extension leader carries real metadata",
              any(BP.LEAD + BP.EXT in r and "DATA WAREHOUSE" in r
                  for r in sheet)
              and any(BP.LEAD + BP.EXT in r and "HIGH" in r for r in sheet))
        # THE KNOCKOUT: exactly one reversed run on the WHOLE frame
        ko = knock_of(cells, rows, w, INK_B)
        check(f"blueprint @{w}: EXACTLY ONE knockout on the view — the "
              f"first-fixation law, measured as reversed cell runs",
              len(ko) == 1, f"{ko}")
        check(f"blueprint @{w}: and it is the title block's STATE cell "
              f"(it reads OVERDUE, and the sheet has something overdue)",
              bool(ko) and "OVERDUE" in rows[ko[0][0]][ko[0][1]: ko[0][2] + 1],
              f"{rows[ko[0][0]][ko[0][1]: ko[0][2] + 1]!r}" if ko else "")
        # HATCH and ALERT, both on the sheet, both on the rows they belong to
        check(f"blueprint @{w}: a HELD row is HATCHED on the sheet",
              any(HATCH in r and "HELD" in r for r in sheet))
        overdue = [r for r in sheet if "D!" in r]
        check(f"blueprint @{w}: an OVERDUE row states its figure with the "
              f"overdue flag", bool(overdue), f"{len(overdue)} row(s)")
        if overdue:
            y = first_of(y for y, r in enumerate(sheet) if "D!" in r)
            xs = [x for x, ch in enumerate(sheet[y]) if ch == "!"]
            gy = kbr[1] + y
            # SENTINEL -1: `xs` is the `!` columns of a row already known
            # to contain "D!", so it is non-empty whenever the sheet is what
            # the law above just asserted. -1 is chosen anyway and chosen to
            # MISS: `cells.get((gy, gx), ("", ""))[0] == ALERT_B` is False
            # for a column off the sheet, so a row that lost its flag reds
            # on the hue law instead of raising inside the setup.
            gx = kbr[0] + nth(xs, 0, -1)
            check(f"blueprint @{w}: ... and the ALERT hue is on that span and "
                  f"nowhere else on the sheet — measured on the render",
                  cells.get((gy, gx), ("", ""))[0] == ALERT_B,
                  f"{cells.get((gy, gx))}")

    # THE CALM SHEET: zero knockout, zero alert, zero hatch — the mutation that
    # clears the urgency, run as a real board rather than as a kit call
    crows, ccells, ckbr = await capture_bg("blueprint", str(fc), size=(118, 30))
    (W / "prototypes" / "out" / "sheet_blueprint_calm.txt").write_text(
        "\n".join(crows), encoding="utf-8")
    csheet = "\n".join(r[ckbr[0]: ckbr[0] + max(0, ckbr[2] - 1)]
                       for r in crows[ckbr[1]: ckbr[1] + ckbr[3]])
    check("blueprint calm: ZERO knockouts when nothing is overdue (the "
          "knockout means attention, so a calm sheet carries none)",
          not knock_of(ccells, crows, 118, INK_B),
          f"{knock_of(ccells, crows, 118, INK_B)}")
    check("blueprint calm: ... and the sheet still STATES its condition",
          any("IN WORK" in r or "CLEAR" in r for r in crows))
    check("blueprint calm: not one ALERT cell anywhere on the frame",
          not [1 for v in ccells.values() if v[0] == ALERT_B])
    check("blueprint calm: and not one hatch — held is what the hatch means",
          HATCH not in csheet)
    check("blueprint calm: the calm board is really a board (probe "
          "self-check — these three checks can fail)",
          "RENEW TLS CERTIFICATE" in csheet and BP.OPEN in csheet)

    # THE TITLE BLOCK's SEAT and its ROW COST, measured on the real widget tree
    bt = _TW(board_path=str(fl))
    async with bt.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        bt.notify = lambda *a, **kw: None
        bt.set_theme("blueprint")
        await pilot.pause()
        bt.redraw()
        await settle(bt, pilot, "blueprint titleblock")
        tabs_r = tuple(bt.query_one("#tabs").region)
        ap_r = tuple(bt.query_one("#ap").region)
        kb_r = tuple(bt.query_one("#kb").region)
        brows = screen_text(bt)
        check("blueprint: the title block is DOCKED to the sheet's bottom "
              "corner — it closes on `#ap`'s last CONTENT row (widget.tcss "
              "gives `#ap` `padding: 1 2`, so one row of sheet margin is "
              "below it, which is where a drawing's border lives)",
              tabs_r[1] + tabs_r[3] == ap_r[1] + ap_r[3] - 1,
              f"block ends {tabs_r[1] + tabs_r[3]}, sheet ends "
              f"{ap_r[1] + ap_r[3]}")
        check("blueprint: ... and it stands BELOW the field, not above it",
              tabs_r[1] >= kb_r[1] + kb_r[3],
              f"block@{tabs_r[1]}, field ends {kb_r[1] + kb_r[3]}")
        check(f"blueprint: the block is exactly {LG.Blueprint.TB_ROWS} rows",
              tabs_r[3] == LG.Blueprint.TB_ROWS, f"{tabs_r[3]}")
        block = brows[tabs_r[1]: tabs_r[1] + tabs_r[3]]
        check("blueprint: every cell of the block is FILLED with real board "
              "data — the sheet, the revision date, the work tally, the state",
              all(s in block[1] for s in (LG.Blueprint.SHEET,
                                          date.today().isoformat(), "/",
                                          "OVERDUE")),
              repr(block[1][-60:]))
        # ONE FIGURE, ONE DERIVATION: the block learns its tally inside the
        # very `meter()` call that drew the meter, so a disagreement between
        # the two rows would mean the block is a redraw behind.
        m_row = next((r for r in brows if "WORK " + BP.OPEN in r), "")
        m1 = re.search(r"(\d+)/(\d+)", block[1])
        m2 = re.search(r"(\d+)/(\d+)", m_row)
        check("blueprint: the block's tally agrees with the METER's own row "
              "(they are the same call, so a stale block would show here)",
              bool(m1) and bool(m2) and m1.groups() == m2.groups(),
              f"block {m1.groups() if m1 else None} vs meter "
              f"{m2.groups() if m2 else None}")
        check("blueprint: the mode on screen is bracketed by REGISTRATION "
              "MARKS on the real render, and by no border at all",
              LG.Blueprint.REG[0] in block[0]
              and LG.Blueprint.REG[2] in block[2]
              and "BOARD" in block[1])
    # THE COST, stated as a number: the block is one row dearer than the strip
    # it replaced, and `#kb`'s reclaimed margin pays for it exactly.
    _, _, kb_block = await capture_styled("blueprint", str(fl), (118, 30))
    _, _, kb_plain = await capture_styled("blueprint", str(fl), (118, 30),
                                          mutate=("frame", "double"))
    # THE COST, as a number rather than a claim. The block is THREE rows where
    # the strip it replaced was two (`margin-top: 1` plus one content row), so
    # it is one row dearer — and `#kb`'s reclaimed margin pays for exactly that
    # one row. The comparison is real because the mutated run genuinely puts
    # the strip back in the flow (asserted at kit level: `dock` leaves the
    # stylesheet with the token).
    check("blueprint: the title block costs the field NOTHING — the same "
          "board rows as the generic composition, measured both ways",
          kb_block[3] == kb_plain[3],
          f"titleblock {kb_block[3]} rows, generic {kb_plain[3]} rows")

    # 60 CELLS: the widget posture, for the same reason it is for solari
    rows60b, _, kbr60b = await capture_bg("blueprint", str(fl), size=(60, 30))
    (W / "prototypes" / "out" / "sheet_blueprint_60.txt").write_text(
        "\n".join(rows60b), encoding="utf-8")
    check("blueprint @60: the frame never wraps (every row is 60 cells)",
          not [len(r) for r in rows60b if len(r) != 60])
    check("blueprint @60: the WIDGET posture is what renders — there is no "
          "board under 80 cells, for any language",
          kbr60b[3] == 0 or kbr60b[2] == 0, f"kb region {kbr60b}")
    check("blueprint @60: the title block sheds cells rather than wrapping "
          "(the declared ladder, on the real seat)",
          any("WORK" in r and "OVERDUE" in r for r in rows60b)
          and not any(LG.Blueprint.SHEET in r for r in rows60b))

    # DISPATCH on the live board, both directions
    def bp_span_rows(board: str) -> list[str]:
        """The SHEET's own span rows, and only those. The `dimension` METER
        draws spans too and answers to its own token, so a naive span search
        measures the chrome and would call the flow degrade a failure."""
        return [r for r in body_rows(board)
                if BP.OPEN in r and BP.CLOSE in r
                and "WORK " not in r and "LOAD" not in r]

    check("blueprint: the sheet's own span rows are on the live board (probe "
          "self-check — the dispatch checks below can fail)",
          len(bp_span_rows(boards["blueprint"])) >= 4,
          f"{len(bp_span_rows(boards['blueprint']))} row(s)")
    for name in TH.ORDER:
        if name == "blueprint":
            continue
        check(f"{name}: board carries no dimension span (the sheet is "
              f"blueprint's)", not bp_span_rows(boards[name]))
    bfl, _, _, _ = await capture("blueprint", mutate=("layout", "flow"),
                                 board_path=str(fx))
    check("blueprint.layout=flow removes the dimension spans from the live "
          "board", not bp_span_rows(bfl))
    check("blueprint.layout=flow leaves the METER alone — the quantity "
          "mechanism answers to `meter`, not to `layout`, and a token that "
          "took a surface it does not own would be over-reaching",
          any("WORK " + BP.OPEN in r for r in body_rows(bfl)))
    check("blueprint.layout=flow keeps the board itself (probe self-check)",
          "Shut down legacy servers" in bfl)
    check("blueprint.layout=flow brings the COLUMNS skeleton back (the "
          "negative control: the sheet checks above CAN fail)",
          "Renew TLS certificate" in bfl)

    print("\n== APP LEVEL: the EMPTY COLUMN speaks (mascot + VOICE)")
    # a second fixture: the same seed with one phase emptied. This restores
    # app-path coverage of `empty()` that was lost when the suite stopped
    # opening the live board (which sometimes had an empty phase and
    # sometimes did not — coverage by luck is not coverage).
    # ALL THREE BRANCHES of `KanbanBoard.build()` now mount the seat (PENDING
    # item 7, closed the thirty-eighth pass). Until then the sections branch
    # was the one that never did, and six languages showed NOTHING for an
    # empty phase. The columns languages are asked at PIXEL level below; the
    # sections and split languages are asked of the widget TREE and then
    # scrolled to, because their lists stack and the emptied phase is last.
    fe = W / "prototypes" / "out" / "_fixture_empty.json"
    seed = json.loads(fx.read_text(encoding="utf-8"))
    check("the empty fixture starts from the seeded board (probe self-check)",
          bool(seed["tasks"]) and "Done" in seed["phases"])
    seed["tasks"] = [t for t in seed["tasks"] if t.get("phase") != "Done"]
    fe.write_text(json.dumps(seed), encoding="utf-8")
    check("the empty fixture really leaves a phase with nothing in it",
          not any(t.get("phase") == "Done" for t in seed["tasks"]))
    # nord left this set 2026-07-27 (it took `layout="split"`), so the count
    # was 4. Its empty-state seat did NOT go with it: the split branch mounts
    # `k.empty()` too, and the loop below is widened to prove that rather
    # than let a language quietly lose a surface it used to have.
    #
    # CORGI left it 2026-07-27 too (`layout="strip"`), and its seat DID go
    # with it — until the thirty-eighth pass, when the sections branch got
    # one. It is back, and it is asserted in the sections loop below.
    column_langs = [n for n in TH.ORDER if LG.kit(n).board_layout() == "columns"]
    check("three languages are left on the COLUMNS branch — the seat they "
          "have always had is asked of the pixels here",
          len(column_langs) == 3
          and not ({"nord", "corgi"} & set(column_langs)),
          f"{column_langs}")
    # nord is asked SEPARATELY, below: its split master is a scrolling list,
    # so a phase far down the board is off-screen at 30 rows and a
    # pixel-search for the voice would go red on the FOLD, not on the seat.
    for name in column_langs:
        k = LG.kit(name)
        # the LONGEST word of the voice, because a narrow empty column wraps
        # it (corgi's "[0] NO TASKS" comes out as "[0] NO" / "TASKS")
        word = max(grey(k.VOICE["empty"]).split(), key=len)
        eb, _, _, _ = await capture(name, board_path=str(fe))
        check(f"{name}: the empty column speaks its own VOICE ({word!r})",
              word in eb)
        # the assert must be ABLE to fail: the same word must be absent when
        # every phase holds tasks (VERIFY.md — mutation-test every assert)
        check(f"{name}: that voice is absent when no phase is empty",
              word not in boards[name])

    # nord's empty-state seat SURVIVED the recomposition. Asked of the widget
    # TREE, not the pixels: the split master scrolls, so the empty phase can
    # be below the fold and still be mounted. Both facts are asserted, because
    # "it exists" and "the user can see it" are different claims (the
    # twenty-third pass's reachability lesson).
    ne = _TW(board_path=str(fe))
    async with ne.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        ne.notify = lambda *a, **kw: None
        ne.set_theme("nord")
        await pilot.pause()
        ne.redraw()
        await settle(ne, pilot, "nord empty")
        seats = ne.query(".kb-empty")
        painted = "empty" in "\n".join(screen_text(ne))
        check("nord: the split branch still MOUNTS the empty state — a "
              "recomposition must not silently take a surface away",
              len(seats) == 1, f"{len(seats)} seat(s)")
        check("nord: the empty seat speaks nord's own VOICE",
              bool(seats) and "empty" in grey(str(seats.first().render())))
        check("nord: ... and it is BELOW THE FOLD at 118x30 (the master is a "
              "scrolling list — stated, not hidden behind a green check)",
              not painted)

    # ---- THE SECTIONS SEAT (PENDING item 7, closed the thirty-eighth pass) --
    # Six languages showed NOTHING for an empty phase because the sections
    # branch of `kanban.py` was the one branch that never mounted `k.empty()`.
    # It does now, and every claim about it is asked at the level that can
    # answer it:
    #
    #   * MOUNTED and what it CONTAINS — of the widget tree, because a
    #     sections list stacks its phases and the emptied one ("Done") is
    #     last, so at 118x30 it starts below the fold;
    #   * REACHABLE — of the PIXELS, after scrolling the flat list to its end.
    #     "It exists" and "the user can see it" are different claims (the
    #     twenty-third pass's reachability lesson), and this pass makes both;
    #   * ABSENT when nothing is empty — of the widget tree on the NORMAL
    #     fixture. That zero is also the byte-identity argument for every
    #     other render in the suite: the added branch is UNREACHABLE unless a
    #     bucket is empty, so no board captured on `fx` can have moved.
    #
    # The MASCOT is the surface a weighted column often cannot afford:
    # `empty()` draws the creature only at w>=14, and a sections row is the
    # full board width, so this seat ALWAYS clears the gate. What it draws
    # there is still the language's own commitment, and the split is measured
    # rather than assumed — **corgi and blueprint draw the creature; swiss,
    # darkside, ledger and solari override `mascot()` to nothing on purpose**
    # ("no ornament", "identity is the doodle, recessive", "a ledger keeps no
    # pet", "a departure board keeps no pet"). Both halves are asserted, in
    # the direction each language declares, so a renunciation can never be
    # confused with the seat failing to draw.
    section_langs = [n for n in TH.ORDER if LG.kit(n).board_layout() == "sections"]
    check("the sections branch carries SEVEN languages — the reach PENDING "
          "item 7 claims for this seat, plus prism",
          len(section_langs) == 7
          and set(section_langs) == {"corgi", "swiss", "darkside", "prism",
                                     "ledger", "solari", "blueprint"},
          f"{section_langs}")
    for name in section_langs:
        k = LG.kit(name)
        voice = grey(k.VOICE["empty"])
        masc = [grey(r) for r in k.mascot()]
        if masc:
            check(f"{name}: the mascot GATE is real — w=13 draws the voice "
                  "alone and w=14 brings the creature, so a seat that shows "
                  "it had to earn its width",
                  len(grey(k.empty(13)).split("\n")) == 1
                  and len(grey(k.empty(14)).split("\n")) == len(masc) + 1)
        else:
            check(f"{name}: RENOUNCES the mascot — `mascot()` is overridden "
                  "to nothing, so this seat is one row at ANY width, and the "
                  "absence is the language's decision, not a failure to draw",
                  len(grey(k.empty(13)).split("\n")) == 1
                  and len(grey(k.empty(400)).split("\n")) == 1
                  and type(k).mascot is not LG.Kit.mascot)
        se = _TW(board_path=str(fe))
        async with se.run_test(size=(118, 30)) as pilot:
            await pilot.pause()
            se.notify = lambda *a, **kw: None
            se.set_theme(name)
            await pilot.pause()
            se.redraw()
            await settle(se, pilot, f"{name} empty")
            seats = se.query(".kb-empty")
            check(f"{name}: the SECTIONS branch mounts the empty state "
                  "(PENDING item 7)",
                  len(seats) == 1, f"{len(seats)} seat(s)")
            # `Static.render()` hands back a `Content`, and `str()` of it is
            # ALREADY plain — the markup was resolved on the way in. Running
            # `grey()` over it a second time is not a no-op and the render
            # caught it: corgi's voice is `\[0] NO TASKS`, whose escape is
            # gone by this point, so the blunt tag regex ate the `[0]` and
            # the check went red on a seat that was drawing correctly. Only
            # the VOICE literal is grey'd here, because that one IS markup.
            rows = str(seats.first().render()).split("\n") if seats else []
            check(f"{name}: the empty seat speaks its own VOICE ({voice!r})",
                  bool(rows) and voice in rows[-1], repr(rows[-1:]))
            if masc:
                check(f"{name}: the MASCOT is SEATED, byte for byte — a "
                      "full-width sections row clears the w>=14 gate that a "
                      "weighted column often cannot afford",
                      rows[:-1] == masc,
                      f"{len(rows) - 1} of {len(masc)} rows")
            else:
                check(f"{name}: the seat is the VOICE ALONE — this language "
                      "renounces the mascot, and the seat honours that "
                      "even at full board width",
                      len(rows) == 1, f"{len(rows)} rows")
            seat_w = seats.first().size.width if seats else 0
            widest = max((len(r) for r in rows), default=0)
            check(f"{name}: nothing WRAPS — the widest row fits the seat's "
                  "own content box",
                  bool(rows) and 0 < widest <= seat_w,
                  f"{widest} cells in {seat_w}")
            # REACHABILITY: scroll the flat list to its end and read the
            # screen. The seat starts below the fold — measured, and reported
            # rather than hidden — but the user can get to it.
            below = voice not in "\n".join(screen_text(se))
            flat = se.query_one(".kb-flat")
            flat.scroll_end(animate=False)
            await pilot.pause()
            await settle(se, pilot, f"{name} empty scrolled")
            check(f"{name}: ... and the user can REACH it — the voice is on "
                  "SCREEN once the flat list is scrolled to its end "
                  f"(it starts below the fold: {below})",
                  voice in "\n".join(screen_text(se)))
        # the seat must be ABSENT when every phase holds tasks: the negative
        # control for all of the above, and the unreachability proof that no
        # render on the normal fixture moved.
        sf = _TW(board_path=str(fx))
        async with sf.run_test(size=(118, 30)) as pilot:
            await pilot.pause()
            sf.notify = lambda *a, **kw: None
            sf.set_theme(name)
            await pilot.pause()
            sf.redraw()
            await settle(sf, pilot, f"{name} full")
            n_seats = len(sf.query(".kb-empty"))
            check(f"{name}: NO seat is mounted when no phase is empty — the "
                  "negative control, and the reason every other capture in "
                  "this suite is byte-identical",
                  n_seats == 0, f"{n_seats} seat(s)")
        check(f"{name}: that voice is absent from the normal board too "
              "(pixel-level negative control)",
              voice not in boards[name])

    # CORGI's head keeps stating the count, which is what it had while it had
    # no seat. Asserted still, because the seat coming back must not be paid
    # for by the number going away.
    ce = _TW(board_path=str(fe))
    async with ce.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        ce.notify = lambda *a, **kw: None
        ce.set_theme("corgi")
        await pilot.pause()
        ce.redraw()
        await settle(ce, pilot, "corgi empty")
        heads = [grey(str(h.render())) for h in ce.query(".col-head")]
        done = [h for h in heads if "D O N E" in h]
        check("corgi: the emptied phase reports itself TWICE now — its head "
              "still states the count, and the seat is back beneath it",
              len(done) == 1 and done[0].split("\n")[0].rstrip().endswith("0")
              and len(ce.query(".kb-empty")) == 1,
              repr(done[0].split("\n")[0][-20:] if done else heads))
    check("corgi: that count check CAN fail — the same head reads 2 when the "
          "phase holds tasks (negative control)",
          "2" in grey(LG.kit("corgi").head("DONE", 2, 110, 2)).split("\n")[0]
          and grey(LG.kit("corgi").head("DONE", 0, 110, 2)
                   ).split("\n")[0].rstrip().endswith("0"))

    print("\n== APP LEVEL: drive the components — they must WORK, not just render")
    from app import TaskboardWidget
    app = TaskboardWidget(board_path=str(fx))
    # freeze the engine's recomputes so captures compare only what WE actuate
    for s in app.engine.signals:
        s.cadence = 10 ** 9
    async with app.run_test(size=(96, 30)) as pilot:
        await pilot.pause()
        app.notify = lambda *a, **kw: None
        check("focus lands at mount (the cheapest check in the skill)",
              app.focused is not None)
        await pilot.press("c")
        await pilot.pause()

        def cfg():
            return "\n".join(screen_text(app))

        before = cfg()
        await pilot.press("space")            # actuate the first switch
        await pilot.pause(0.9)                # let the flip frames settle
        check("space ACTUATES the switch (render moved)", cfg() != before)
        scr = app.screen
        want = first_of(i for i, s in enumerate(app.engine.signals)
                        if s.threshold is not None)
        # BOUNDED walk (an unbounded while hung a whole run when the arrows
        # were dead — the probe must fail loud, not spin)
        for _ in range(len(app.engine.signals) + 2):
            if scr.idx == want:
                break
            await pilot.press("down")
            await pilot.pause()
        check("arrow keys navigate the config cursor (was DEAD: app-level "
              "priority nav ate them)", scr.idx == want)
        base = cfg()
        await pilot.press("bracketright")      # slider up
        await pilot.pause()
        check("] moves the threshold slider", cfg() != base)
        for _ in range(30):                    # hammer past the floor
            await pilot.press("bracketleft")
        await pilot.pause()
        at_floor = cfg()
        await pilot.press("bracketleft")
        await pilot.pause()
        check("the slider CLAMPS at its floor (no wrap, no crash)",
              cfg() == at_floor)

        # -- THE LIVE RADIO. A group that renders and cannot be crossed is a
        # picture of a control. These press REAL keys on the shipped screen
        # and read the engine, not the render, for the consequence.
        # SETTLED, NOT RACED, and the fifty-ninth pass is why. This block
        # compares two RENDERS across a key press, and since that pass the
        # arrow keys start a MOTION — so a capture taken one `pause()` after
        # a press can land on an in-transit frame while the capture it is
        # compared against landed on a resting one. It went red once in three
        # runs, which is worse than always-red: an intermittent law is a law
        # people learn to re-run. One whole transition is the language's own
        # `tempo`, so that plus slack is the settle, taken from the token
        # rather than from a number typed here.
        import app as APPMOD_R
        mo_settle = APPMOD_R.KIT.tempo_s * 2
        sig = app.engine.signals[scr.idx]
        start = sig.group
        await pilot.press("left")
        await pilot.pause(mo_settle)
        await pilot.press("right")
        await pilot.pause(mo_settle)
        check("left/right CROSS the live worker-group radio — the app's "
              "priority arrows are delegated sideways the way they already "
              "were downwards, or a screen's own group is inert",
              sig.group == WORKER_GROUPS[1], f"{start} -> {sig.group}")
        moved = cfg()
        await pilot.press("right")
        await pilot.pause(mo_settle)
        check("the set CLAMPS at its last option — an N-of-M control's ends "
              "are where the set ends. (THE SENTENCE THIS CHECK USED TO CARRY "
              "— 'a group that wraps is a stepper' — IS WRONG AND THE FIFTY-"
              "FIFTH PASS RETIRED IT: what makes a control a stepper is "
              "showing ONE option, not wrapping. Wrap belongs to the RANGE "
              "and is the caller's, and this app's own stepper clamps at "
              "exactly this seat, on exactly this key)",
              sig.group == WORKER_GROUPS[-1] and cfg() == moved)
        for _ in range(len(WORKER_GROUPS) + 3):
            await pilot.press("left")
        await pilot.pause(mo_settle)
        check("... and at its first, after being hammered past it",
              sig.group == WORKER_GROUPS[0])
        check("and the SELECTION SURVIVES every one of those presses — the "
              "signal is in exactly one worker group, which is the invariant "
              "the whole increment is about, read off the model rather than "
              "off the drawing",
              sum(sig.group == g for g in WORKER_GROUPS) == 1)
        sig.group = start

        # -- THE LIVE BUTTON. A press target that renders and cannot be
        # pressed is a picture of a control, so this drives the REAL key and
        # reads the ENGINE for the consequence — `Signal.runs` is a counter
        # the app increments and nothing here writes.
        import app as APPMOD_B
        kb = APPMOD_B.KIT
        cfg_row = next((r for r in screen_text(app) if "Refresh" in r), "")
        check("the config screen carries a rendered button, drawn with THIS "
              "language's walls — the live seat is the language's, not a "
              "bracket hardcoded at the call site",
              kb.part_glyph("main", LG.DEFAULT, "button")[:1] in cfg_row
              and "Refresh" in cfg_row, repr(cfg_row.strip()))
        on_ = [s.enabled for s in app.engine.signals]
        runs_before = [s.runs for s in app.engine.signals]
        # THE FLASH IS TIMED, so the probe pins the clock instead of racing
        # it: a language's own tempo runs from 60 ms up, and reading the
        # screen "just after" a 60 ms flash is a coin toss, not a law. The
        # token is restored below — a probe that leaves a theme mutated
        # poisons every render behind it.
        _tempo = kb.t.get("tempo")
        kb.t["tempo"] = 900
        await pilot.press("r")
        await pilot.pause()
        runs_after = [s.runs for s in app.engine.signals]
        check("`r` PRESSES it — EXACTLY the enabled signals are recomputed, "
              "read off the engine's own run counters and not off the render. "
              "The one switched off earlier in this drive stays untouched, "
              "which is what makes this a consequence and not a repaint",
              all((a > b) == e
                  for b, a, e in zip(runs_before, runs_after, on_))
              and not all(on_),
              f"{runs_before} -> {runs_after}, enabled {on_}")
        flashed = next((r for r in screen_text(app) if "Refresh" in r), "")
        check("... and the press SHOWS: the walls under the word are the "
              "ACTIVE ones for the length of the language's own tempo, which "
              "is the state this component exists for",
              kb.part_glyph("main", LG.ACTIVE, "button")[:1] in flashed
              and flashed != cfg_row, repr(flashed.strip()))
        await pilot.pause(kb.tempo_s * 2)
        released = next((r for r in screen_text(app) if "Refresh" in r), "")
        check("... and it RELEASES — a flash that never ends is a state, and "
              "a pressed state that outlives the press is a lie",
              released == cfg_row, repr(released.strip()))
        if _tempo is None:
            kb.t.pop("tempo", None)
        else:
            kb.t["tempo"] = _tempo

        for s in app.engine.signals:
            s.enabled = False
        app.screen.redraw()
        await pilot.pause()
        dead_row = next((r for r in screen_text(app) if "Refresh" in r), "")
        check("with every signal switched off the button goes DISABLED, and "
              "that is the ENGINE's condition, not a demo toggle — there is "
              "nothing left to recompute",
              kb.part_glyph("main", LG.DISABLED, "button")[:1] in dead_row,
              repr(dead_row.strip()))
        runs_dead = [s.runs for s in app.engine.signals]
        kb.t["tempo"] = 900            # pin the clock again: the law below is
        await pilot.press("r")         # about a flash that must NOT appear,
        await pilot.pause()            # about a flash that must NOT appear,
        check("... and pressing a DEAD button recomputes nothing",
              [s.runs for s in app.engine.signals] == runs_dead,
              f"{runs_dead} -> {[s.runs for s in app.engine.signals]}")
        # AND THE ACTION ITSELF REFUSES, asked directly. The counters above
        # cannot see this: with every signal off, `run_all` recomputes nothing
        # WHETHER OR NOT the guard is there, and the render's own `and live`
        # hides the flash — so a mutant that deletes the guard changed the
        # code and not one observable thing (PENDING, the fifty-first pass's
        # M5). The state the guard actually writes is the one to ask about.
        calls_ = []
        _run_all = app.engine.run_all
        app.engine.run_all = lambda *a, **k: (calls_.append(1),
                                              _run_all(*a, **k))[1]
        await pilot.press("r")
        await pilot.pause()
        app.engine.run_all = _run_all
        check("... and the ACTION refuses rather than merely achieving "
              "nothing — a dead control that still runs its handler is a "
              "control whose render and behaviour disagree. Counted at the "
              "engine's own door, because a timer-driven flag would be a "
              "race and a race is not a law",
              not calls_, f"{len(calls_)} call(s)")
        check("... and the dead button does not FLASH under the finger "
              "either — the render after a refused press is the render "
              "before it, which is the half of this a user could actually "
              "see if both guards ever went",
              next((r for r in screen_text(app) if "Refresh" in r), "")
              == dead_row)
        if _tempo is None:
            kb.t.pop("tempo", None)
        else:
            kb.t["tempo"] = _tempo
        for s in app.engine.signals:
            s.enabled = True
        app.screen.redraw()
        await pilot.pause()

        # ==================================================================
        # THE MOTION SEAT, DRIVEN (PENDING #27). A frame list no key ever
        # plays is a picture of an animation, which is exactly the thing this
        # contract keeps finding: the button's flash was a BOOLEAN held for
        # one tempo, and the pick had no motion at all. So these press the
        # real keys and read the SCREEN'S OWN SLOT against the ENGINE — not
        # against a frame list retyped in the oracle.
        #
        # THE CLOCK IS PINNED, not raced. A language's tempo runs from 40 ms
        # up; reading "which frame is on the glass" just after a 40 ms
        # transition is a coin toss, not a law.
        # ==================================================================
        import app as APPMOD_M
        km = APPMOD_M.KIT
        _mtempo = km.t.get("tempo")
        km.t["tempo"] = 900
        sigm = app.engine.signals[scr.idx]
        sigm.group = WORKER_GROUPS[0]
        scr.redraw()
        await pilot.pause()
        check("the config screen is drawing the RADIO mechanism at this "
              "size, so the pick's motion is a TRAVEL — the two mechanisms "
              "are one choice and they are two motions, and the screen is "
              "asked which one it has rather than told",
              scr._wide())
        await pilot.press("right")
        await pilot.pause()
        want = km.motion_frames("radio", "travel", options=WORKER_GROUPS,
                                old=0, new=1, state=LG.FOCUSED)
        check("`right` PLAYS THE MARK'S TRAVEL — the screen's motion slot "
              "holds the engine's own frames for this language, byte for "
              "byte. A caller that built its own frame list would be a "
              "second motion vocabulary, which is what `flip_frames` used to "
              "be before pass 49 derived it",
              scr._motion is not None and scr._motion[0] == "pick"
              and list(scr._motion[2]) == list(want.plays)
              and len(want.plays) >= 1,
              f"{scr._motion[0] if scr._motion else None}, "
              f"{len(want.plays)} frame(s)")
        check("... and the SELECTION IS ALREADY THE NEW ONE while the mark "
              "is still travelling — the model moves on the key press and "
              "the render catches up, which is why an in-transit frame is a "
              "frame and not a state",
              sigm.group == WORKER_GROUPS[1])
        await pilot.pause(km.tempo_s * 2)
        # THE SELECTED ROW, not the first row that mentions a group name —
        # every signal's row carries every option's word, so `"slow" in r`
        # finds whichever row is topmost and reports on a control nobody
        # touched. The label is what identifies the row the keys reached.
        rest_row = next((r for r in screen_text(app)
                         if sigm.label[:20] in r), "")
        check("... and it ARRIVES: the slot empties and the row is the "
              "resting render, which is the motion's LAST FRAME and not a "
              "second code path",
              scr._motion is None
              and grey(km.radio_group(WORKER_GROUPS, 1, LG.FOCUSED,
                                      focus=1)) in rest_row
              and grey(want.frames[-1]) in rest_row, repr(rest_row.strip()))
        await pilot.press("left")
        await pilot.pause()
        await pilot.pause(km.tempo_s * 2)
        for _ in range(len(WORKER_GROUPS) + 2):        # BOUNDED: hammer the
            await pilot.press("left")                  # clamped end
            await pilot.pause()
        check("a pick that changes NOTHING plays nothing — at the clamped "
              "end the arrow is honest about having nowhere to go, and a "
              "motion with no distance is not a motion",
              scr._motion is None and sigm.group == WORKER_GROUPS[0])

        await pilot.press("r")
        await pilot.pause()
        pm = km.motion_frames("button", "press", label="Refresh")
        pressed_row = next((r for r in screen_text(app) if "Refresh" in r), "")
        check("`r` PLAYS A FRAME LIST NOW, not a boolean — the press has "
              "intermediate frames at last (PENDING #27's first debt), and "
              "they are the engine's",
              scr._motion is not None and scr._motion[0] == "press"
              and list(scr._motion[2]) == list(pm.plays)
              and len(pm.plays) >= 2, f"{len(pm.plays)} frames")
        check("... and the frame ON THE GLASS is the extreme, reached on the "
              "FIRST drawn frame — the acknowledgement is never animated",
              bool(pm.plays) and grey(pm.plays[0]) in pressed_row
              and pm.plays[0] == km.button("Refresh", 0, LG.ACTIVE),
              repr(pressed_row.strip()))
        await pilot.pause(km.tempo_s * 2)
        released_row = next((r for r in screen_text(app)
                             if "Refresh" in r), "")
        check("... and the RELEASE lands on the list's last frame, which is "
              "the render the screen would have drawn anyway — a pressed "
              "state that outlives its frames is not reachable from here, "
              "because there is no second flag to outlive them",
              scr._motion is None and bool(pm.plays)
              and pm.plays[-1] == km.button("Refresh", 0, LG.DEFAULT)
              and grey(pm.plays[-1]) in released_row,
              repr(released_row.strip()))
        check("ONE MOTION SLOT, and therefore one moving element — "
              "MOTION.md's hardest rule, held by construction rather than by "
              "discipline: two slots is how a surface grows a second moving "
              "element without anyone deciding to",
              [a for a in vars(scr) if a.startswith("_")
               and a in ("_flip", "_pressed", "_motion")] == ["_motion"],
              f"{[a for a in vars(scr) if a in ('_flip', '_pressed', '_motion')]}")
        if _mtempo is None:
            km.t.pop("tempo", None)
        else:
            km.t["tempo"] = _mtempo

        # -- THE CARET'S BLINK, AND IT IS GALLERY-ONLY, SAID OUT LOUD.
        # Pass 53 read this app for a live text seat and found none — nothing
        # in the engine is TYPED — and refused to invent one. That ruling
        # stands, so the contract's first AMBIENT runs where its component
        # already lives. What is asserted is that it RUNS: the gallery hands
        # the block its own clock, and the block's caret changes on the
        # engine's period.
        #
        # DRIVEN BY INDEX, NEVER BY WALL CLOCK. A loop whose period is two
        # seconds cannot be waited on inside an acceptance suite, and a probe
        # that slept for one would be a probe that times out. The screen's
        # tick is set directly and the frames are read off the block.
        from app import GalleryScreen as _MGal
        _seen_ticks = []
        _real_tb = APPMOD_M.textfield_block
        APPMOD_M.textfield_block = lambda k_, w_, tick=None: (
            _seen_ticks.append(tick), _real_tb(k_, w_, tick))[1]
        try:
            app.push_screen(_MGal())
            await pilot.pause()
            gal = app.screen
            gal.rerender()
            await pilot.pause()
            check("the gallery hands the text-field block ITS OWN CLOCK — "
                  "the block is not blinking on a number typed at the call "
                  "site, and it is not blinking on nothing",
                  _seen_ticks and _seen_ticks[-1] == gal._t
                  and all(t is not None for t in _seen_ticks),
                  f"tick {_seen_ticks[-1]} == _t {gal._t}")
            n0 = gal._t
            gal.rerender()
            gal.rerender()
            check("... and that clock ADVANCES on the surface's own repaint, "
                  "which is the rate the loop is phased against (GAL_FPS) "
                  "and not a ticker running at another one",
                  gal._t == n0 + 2, f"{n0} -> {gal._t}")
            bm = km.motion_frames("textfield", "blink",
                                  value=APPMOD_M.TF_VALUE,
                                  caret=APPMOD_M.TF_CARET, w=10)
            per = int(bm.total_ms / (1000 / APPMOD_M.GAL_FPS)) + 2

            def blk(t):
                return [grey(r) for r in _real_tb(km, GAL_W, t)]

            base = blk(0)
            flip_at = next((i for i in range(1, per) if blk(i) != base), None)
            check("the caret BLINKS: driven tick by tick across one period "
                  "the block changes, and it changes WHEN the engine says it "
                  "does — the moment is read off the render and compared to "
                  "the engine's step, so nothing here re-derives the phase",
                  flip_at is not None
                  and abs(flip_at * (1000 / APPMOD_M.GAL_FPS) - bm.step_ms)
                  < (1000 / APPMOD_M.GAL_FPS),
                  f"flipped at tick {flip_at}, step {bm.step_ms:.0f} ms")
            moved = [i for i, (a, b) in enumerate(zip(base, blk(flip_at)))
                     if a != b]
            check("... and what changes is ONE CELL of the rows that HAVE a "
                  "caret — the EDITED state and the window row. A blink that "
                  "moved a second character would be moving the user's value",
                  moved and all(sum(x != y for x, y in
                                    zip(base[i], blk(flip_at)[i])) == 1
                                for i in moved)
                  and all(len(base[i]) == len(blk(flip_at)[i]) for i in moved),
                  f"{len(moved)} row(s)")
            check("... and calling the block WITHOUT a tick leaves the caret "
                  "simply ON, which is why the blink could not move a single "
                  "law that measured this block before it existed",
                  blk(None) == base)
            check("the blink is AMBIENT and its period is the language's — "
                  "and it is GALLERY-ONLY, which is stated rather than faked: "
                  "pass 53 read this app for a live text seat and found none, "
                  "so the first loop this contract ships runs where its "
                  "component already lives",
                  bm.regime == LG.AMBIENT
                  and bm.total_ms >= LG.AMBIENT_MIN_MS
                  and not [w for w in (getattr(APPMOD_M, "ConfigScreen"),)
                           if "textfield" in inspect.getsource(w)],
                  f"{bm.total_ms:.0f} ms")
            app.pop_screen()
            await pilot.pause()
        finally:
            APPMOD_M.textfield_block = _real_tb

        # THE CHEAPEST LAW THIS SUITE OWNS, and it is here because the defect
        # it catches had been on this screen for four passes: a closing tag
        # that reaches the glass never closed anything.
        for scr_name, rows_ in (("config", screen_text(app)),):
            leaked = [r for r in rows_ if "[/]" in r]
            check(f"no row of the {scr_name} screen carries a literal `[/]` — "
                  f"a tag on the glass is a style that never closed, and "
                  f"`[[/]█|]` is what the bracketed languages were printing",
                  not leaked, f"{leaked[:1]}")

    # ======================================================================
    # THE ESCAPE SWEEP — PENDING item #25, and the law widened with it
    #
    # Pass 52 cured the COMPONENT seats with `mark` and left twenty-three
    # `rich.markup.escape` call sites carrying user text. This section is the
    # sweep's evidence, and it is written in four parts because the swap alone
    # is not the finding.
    #
    # WHAT THE SWEEP ACTUALLY FIXED, measured before it was made
    # (`prototypes/out/_p56_prove.py`, PRE dump): the defect was not the
    # predicted `[/]` leak. It was SILENT DELETION. A task titled
    # `[urgent] ship it` is escaped correctly by rich — `[u` looks like a tag
    # to it — but corgi, solari and blueprint UPPER-CASE their titles, and
    # `[URGENT]` does not look like a tag to rich, so it went out unescaped
    # and Textual ate it. Those three languages were each printing
    # ` SHIP IT`, with no leak, no error and nothing on the glass to see. The
    # config screen's `[/]` law could never have caught it: there was no `[/]`.
    #
    # SO THE LAW IS TWO LAWS. `[/]` on the glass is a style that never closed;
    # a row that shows a title's TAIL without its bracketed HEAD is user text
    # the parser deleted. The second is the one that fires today.
    #
    # THE CASE COMPARISON IS DELIBERATE and it is an instrument fix, not a
    # convenience: darkside LOWER-cases titles and blueprint UPPER-cases them,
    # so a case-sensitive head/tail pair reported darkside's perfectly intact
    # `[urgent] rotate keys` as eaten. Measured, seen, corrected here.
    #
    # SCOPE, stated rather than implied: board, config and gallery are the
    # screens whose text comes out of `language.py`. The shipped APERTURE is
    # NOT asserted here — `taskboard/aperture.py:386` still escapes
    # `t.title` rich's way and is outside this increment's file budget. It is
    # measured in the prover (§5: all three languages driven EAT `[URGENT]`
    # out of the queue) and filed as its own item rather than left implied.
    # ======================================================================
    print("\n== THE ESCAPE SWEEP: one escaping, and the law on every screen")
    from rich.markup import escape as _rich_escape
    from textual.content import Content as _C

    # -- (1) THE RULE IS GREP-ABLE ----------------------------------------
    # "this literal happens to have no bracket in it" is a claim about every
    # call site forever; "this module does not call rich's escape" is a claim
    # one search settles. That is why the sweep took the internal literals
    # too, and why the import is gone rather than merely unused.
    lang_src = (W / "taskboard" / "language.py").read_text(encoding="utf-8")
    check("`language.py` calls rich's `escape` at ZERO sites — the sweep took "
          "all twenty-three, so the rule is one grep and not a promise per "
          "call site", "escape(" not in lang_src,
          f"{lang_src.count('escape(')} left")
    check("... and it does not IMPORT it either — an unused import is a seat "
          "the next edit sits back down in",
          "from rich.markup import" not in lang_src)
    _marks = len(re.findall(r"(?<![\w.])mark\(", lang_src))
    check("... and `mark` is what took the seats (26 calls at 23 sites, plus "
          "the component seats pass 52 cured)", _marks >= 26, f"{_marks} calls")

    # -- (2) BYTE IDENTITY, MEASURED --------------------------------------
    # The swap is only a no-op for today's data if the two functions agree on
    # text with no `[` in it. They agree on everything except ONE string, and
    # that exception is asserted rather than waved at, because if a future
    # rich or Textual changes it this law is where it surfaces.
    _BS = "\\"
    FREE = ["plain text", "UPPER CASE", "ends in space ", "1/2 · 3d",
            "inner" + _BS + "slash", "double" + _BS + _BS, "no brackets here"]
    _split = [s for s in FREE if _rich_escape(s) != LG.mark(s)]
    check("BYTE IDENTITY: on bracket-free text `mark` and rich's `escape` "
          "produce the SAME string, so the sweep changes no render the app "
          "has today — measured over the corpus, not assumed",
          not _split, f"diverge: {_split!r}")
    _tail = "path ends in a slash" + _BS
    check("... with exactly ONE exception, and it is stated: text ending in a "
          "single backslash. rich doubles it, `mark` does not",
          _rich_escape(_tail) != LG.mark(_tail))
    _both = {lbl: _C.from_markup(f"[#aaaaaa]{fn(_tail)}[/]|").plain
             for lbl, fn in (("escape", _rich_escape), ("mark", LG.mark))}
    check("... and that exception is GLASS-NEUTRAL, which is why the sweep "
          "ran anyway: under Textual — the parser that renders this app — "
          "BOTH escapings print a raw `[/]` there, because a `\\` in front of "
          "a `[` escapes the bracket whether or not another `\\` precedes it. "
          "No encoding of a trailing backslash closes the tag under both "
          "parsers (five searched, `_p56_prove.py` §3b). Its own item",
          all("[/]" in v for v in _both.values()), f"{_both!r}")

    # -- (3) THE CONTROLS: what `escape` does that `mark` does not ---------
    # Pure functions, no app, so these run on every suite and cost nothing.
    # A sweep whose two escapings behave identically on the hazard would be a
    # sweep worth reverting; these are the three shapes that differ.
    for _txt, _what in (("[URGENT] SHIP IT", "an upper-cased bracket"),
                        ("[ x]", "a bracket followed by a space"),
                        ("x[y", "an unclosed bracket")):
        _e = _C.from_markup(f"[#aaaaaa]{_rich_escape(_txt)}[/]|").plain
        _m = _C.from_markup(f"[#aaaaaa]{LG.mark(_txt)}[/]|").plain
        check(f"control: {_what} ({_txt!r}) is MANGLED by rich's escape under "
              f"Textual and survives `mark` — the defect and the cure, "
              f"reproduced on this run",
              _e != _txt + "|" and _m == _txt + "|",
              f"escape -> {_e!r}, mark -> {_m!r}")

    # -- (4) EVERY SCREEN THE SUITE DRIVES, WITH HAZARD TEXT ON IT ---------
    # The fixture is the whole point: the old fixture's titles have no bracket
    # in them, so the old `[/]` law was asserting something no data could
    # violate. Every user-controlled string here carries a bracket, and the
    # three forms are chosen from the two-parser measurement: `[urgent]`
    # (safe under rich until a language upper-cases it), `[URGENT]` (typed
    # that way — unsafe immediately) and `[BLOCKED]` on a done task.
    HZ_T = (("[urgent] ship it", "[urgent]", "ship it"),
            ("[URGENT] rotate keys", "[URGENT]", "rotate keys"),
            ("[BLOCKED] audit keys", "[BLOCKED]", "audit keys"))
    hz = W / "prototypes" / "out" / "_fixture_hazard.json"
    hz.write_text(json.dumps({
        "projects": [{"id": "p1", "name": "[QA] Web", "color": "#88c0d0",
                      "status": "active"}],
        "tasks": [{"id": f"t{i}", "title": t, "project_id": "p1",
                   "phase": ph, "priority": pr,
                   "due_date": date.today().isoformat(),
                   "notes": "note [x] with a bracket" if i == 1 else "",
                   "urls": []}
                  for i, ((t, _, _), ph, pr) in enumerate(
                      zip(HZ_T, ("Doing", "Backlog", "Done"),
                          ("high", "low", "med")), start=1)],
        "phases": ["Backlog", "Doing", "Done"],
    }), encoding="utf-8")

    def _mangled(rows):
        """(leaked rows, eaten (head, row) pairs). CASE-INSENSITIVE, because
        the languages disagree about case and an intact title is intact in
        whatever case its language prints it."""
        leaked = [r for r in rows if "[/]" in r]
        eaten = []
        for _, head, tail in HZ_T:
            for r in rows:
                low = r.lower()
                if tail.lower() in low and head.lower() not in low:
                    eaten.append((head, r.strip()[:60]))
        return leaked, eaten

    from app import TaskboardWidget as _TWH
    for name in TH.ORDER:
        hzapp = _TWH(board_path=str(hz))
        async with hzapp.run_test(size=(118, 30)) as pilot:
            await pilot.pause()
            hzapp.notify = lambda *a, **kw: None
            hzapp.set_theme(name)
            await pilot.pause()
            hzapp.redraw()
            await settle(hzapp, pilot, f"hazard {name}")
            screens = [("board", screen_text(hzapp),
                        type(hzapp.screen).__name__)]
            for label, key in (("config", "c"), ("gallery", "g")):
                await pilot.press("escape")
                await pilot.pause()
                await press(pilot, key)
                screens.append((label, screen_text(hzapp),
                                type(hzapp.screen).__name__))
            for label, rows_, cls_ in screens:
                leaked, eaten = _mangled(rows_)
                check(f"{name}/{label}: no row carries a literal `[/]` — a "
                      f"tag on the glass is a style that never closed",
                      not leaked, f"{leaked[:1]}")
                check(f"{name}/{label}: and no bracketed head is EATEN — a "
                      f"row showing a title's tail without its head is user "
                      f"text the markup parser deleted, which is what three "
                      f"languages were doing to `[urgent] ship it`",
                      not eaten, f"{eaten[:1]}")
                check(f"{name}/{label}: probe self-check — the screen driven "
                      f"is the screen named", cls_ in (
                          "Aperture" if label == "board"
                          else "ConfigScreen" if label == "config"
                          else "GalleryScreen",), cls_)
            # AND THE LAW IS NOT VACUOUS ON THE BOARD: the hazard has to be ON
            # the glass for "it is intact" to mean anything. Only the board
            # carries board data — config and gallery draw their own literals,
            # and their leg of this law is a REGRESSION guard on the component
            # seats pass 52 cured, which is stated here rather than pretended.
            board_blob = "\n".join(screens[0][1]).lower()
            on_glass = [h for _, h, _ in HZ_T if h.lower() in board_blob]
            check(f"{name}/board: the hazard is actually ON the glass "
                  f"(vacuity guard — a no-leak law over text that never "
                  f"rendered is a law that cannot fail)",
                  len(on_glass) >= 2, f"heads found: {on_glass}")

    # ======================================================================
    # THE HERO PANEL'S FIRST FIXATION — nord, PENDING item 0e
    #
    # The twenty-eighth pass measured nord's board and cured it with the
    # split; INSIDE the hero panel above it nothing had changed. This section
    # is that measurement re-scoped to the panel, and it is written as a PAIR:
    # the pre-cure render is CAPTURED (the two tokens taken away at runtime)
    # rather than remembered, so every claim below has a control that shows it
    # failing. The instrument is pass 28's own — ink cells grouped by
    # foreground hex, ranked by the weighted channel sum `chan_lum`.
    #
    # THE SEAT. `taskboard/hero.py` is reached by exactly one composited
    # surface, the SHIPPED aperture, because the widget-slice prototype still
    # forks `Hero.show` (PENDING, thirty-fifth pass open item 3). Pass 36 made
    # the same call for the flap faces and named the reason: the aperture is
    # the seat that ships. The prototype's copy of this panel is NOT cured by
    # this pass, and that fact is asserted below rather than left implicit.
    # ======================================================================
    print("\n== THE HERO PANEL: nord's first fixation (PENDING item 0e)")
    HP_TOK = ("hero_fit", "hero_plot")

    def _clear_hp(name, fn):
        """Run `fn` with the hero-panel tokens taken off `name` and restored
        in a `finally` — the same mutate-and-restore contract every capture in
        this suite carries, at draw level. A token left mutated poisons every
        render after it."""
        saved = {k: TH.THEMES[name].get(k) for k in HP_TOK}
        for k in HP_TOK:
            TH.THEMES[name].pop(k, None)
        try:
            return fn()
        finally:
            for k, v in saved.items():
                if v is not None:
                    TH.THEMES[name][k] = v

    def _with(kit, tok, val, fn):
        """One token swapped for the duration of one render. `kit.t` IS the
        theme dict, so this is the draw-level twin of `capture(mutate=...)`."""
        saved = kit.t.get(tok)
        kit.t[tok] = val
        try:
            return fn()
        finally:
            if saved is None:
                kit.t.pop(tok, None)
            else:
                kit.t[tok] = saved

    async def ap_panel(path, size=(118, 30), off=False):
        """The shipped hero panel. `off` takes the two tokens away for the
        duration of the capture, which is how the PRE-CURE render is measured
        on this run instead of quoted from a previous one."""
        saved = {k: TH.THEMES["nord"].get(k) for k in HP_TOK}
        if off:
            for k in HP_TOK:
                TH.THEMES["nord"].pop(k, None)
        try:
            return await capture_ap_bg("nord", str(path), size=size)
        finally:
            for k, v in saved.items():
                if v is None:
                    TH.THEMES["nord"].pop(k, None)
                else:
                    TH.THEMES["nord"][k] = v

    def panel_inks(rows, cells, reg):
        """Pass 28's table, scoped to the hero panel: painted cells grouped by
        foreground hex, each group carrying its cell count, the panel rows it
        occupies and its bounding-box EXTENT. Both area measures are kept
        because the two disagree for a sparse wide element, and pass 28 stated
        its finding in CELLS (25 against 61)."""
        x0, y0, w, h = reg
        g: dict[str, dict] = {}
        for y in range(y0, min(y0 + h, len(rows))):
            line = rows[y]
            for x in range(x0, x0 + w):
                if x >= len(line) or not line[x].strip():
                    continue
                fg = cells.get((y, x), ("", ""))[0]
                if not fg:
                    continue
                d = g.setdefault(fg, {"cells": 0, "rows": set(), "xs": []})
                d["cells"] += 1
                d["rows"].add(y - y0)
                d["xs"].append(x - x0)
        for fg, d in g.items():
            d["lum"] = chan_lum(fg)
            d["extent"] = ((max(d["xs"]) - min(d["xs"]) + 1)
                           * (max(d["rows"]) - min(d["rows"]) + 1))
        return g

    def isolated(g):
        """ISOLATION, computed and not eyeballed: a group is isolated when no
        other group paints any panel row it paints. HIERARCHY.md ranks empty
        space as a lever, and a row of its own is the cheapest form the panel
        has."""
        return sorted(fg for fg, d in g.items()
                      if not any(d["rows"] & o["rows"]
                                 for f2, o in g.items() if f2 != fg))

    def panel_table(tag, g):
        lines = [f"-- {tag}", f"   {'ink':<10}{'lum':>8}{'cells':>8}"
                 f"{'extent':>8}  rows"]
        for fg, d in sorted(g.items(), key=lambda kv: -kv[1]["lum"]):
            lines.append(f"   {fg:<10}{d['lum']:>8.1f}{d['cells']:>8}"
                         f"{d['extent']:>8}  {sorted(d['rows'])}")
        return "\n".join(lines)

    N = TH.THEMES["nord"]
    PANEL_LOG = []
    # -- the PRE-CURE control: the defect, reproduced on this run ------------
    pre_rows, pre_cells, pre_reg = await ap_panel(fx, off=True)
    pre_g = panel_inks(pre_rows, pre_cells, pre_reg)
    PANEL_LOG.append(panel_table("PRE-CURE  overdue  118x30", pre_g))
    pre_num = pre_g.get(N["alert"], {"cells": 0, "extent": 0})
    pre_plot = pre_g.get(N["accent"], {"cells": 0, "extent": 0})
    check("nord PRE-CURE: the load chart is drawn in the ACCENT and the "
          "headline numeral in the severity tone (probe self-check — every "
          "claim below is vacuous if the control is not the old render)",
          pre_plot["cells"] > 0 and pre_num["cells"] > 0,
          f"accent={pre_plot['cells']} alert={pre_num['cells']} cells")
    check("nord PRE-CURE: the numeral LOSES AREA to the chart standing beside "
          "it in the same panel — the mood-independent half of the "
          "twenty-eighth pass's verdict, re-measured",
          pre_num["cells"] < pre_plot["cells"],
          f"numeral {pre_num['cells']} cells vs chart {pre_plot['cells']}")
    check("nord PRE-CURE: the numeral is also OUT-SHONE by the chart",
          pre_num.get("lum", 0) < pre_plot.get("lum", 0),
          f"{pre_num.get('lum', 0):.1f} vs {pre_plot.get('lum', 0):.1f}")
    check("nord PRE-CURE: NOTHING in the panel is isolated — no element wins "
          "area AND brightness AND isolation, so the hero has no fixation",
          not isolated(pre_g), f"isolated={isolated(pre_g)}")
    pre_fig = BS.draw_numeral("2", "quadrant", HE.HERO_FONT)
    check("nord PRE-CURE: and the figure did not even FIT — quadrant's global "
          "(3, 3) scale draws 11 cell rows into a 9-row hero, so the trim cut "
          "its own baseline off",
          len(pre_fig) == 11 and len(pre_fig) > pre_reg[3],
          f"{len(pre_fig)} rows into {pre_reg[3]}")
    check("nord PRE-CURE: ... which is why the caption never drew at this seat",
          not any("OVERDUE" in r[pre_reg[0]: pre_reg[0] + pre_reg[2]]
                  for r in pre_rows[pre_reg[1]: pre_reg[1] + pre_reg[3]]))

    # -- the CURED panel, on BOTH fixtures ----------------------------------
    # THE FIXTURES' TRUTH IS CHECKED BEFORE THE LAW IS WRITTEN (pass 36's
    # lesson: the first ledger probe asserted "calm" against a board that is
    # genuinely overdue and went red for being right about the wrong thing).
    fit = N["hero_fit"]
    fig = BS.render(BS.scale(BS.from_font("2", HE.HERO_FONT, gap=1), *fit),
                    "quadrant")
    check("nord: `hero_fit` draws the figure INSIDE the panel's row budget, "
          "with its blank row and its caption under it",
          len(fig) + 2 <= 9, f"{len(fig)} rows + 2")
    check("nord: ... and the figure it draws is COMPLETE — its baseline row "
          "carries ink INSIDE the budget, where the (3, 3) figure's baseline "
          "sat two rows below the panel and was trimmed away",
          bool(fig[-1].strip()) and len(fig) <= 7 and len(pre_fig) > 7,
          f"fitted {len(fig)} rows, pre-cure {len(pre_fig)}")
    check("nord: the fitted figure's visual aspect lands in the drawn-type "
          "bracket the display-type passes hold every digit to (a cell is "
          "~1:2, so the aspect is width / 2*rows)",
          0.55 <= max(len(r) for r in fig) / (2 * len(fig)) <= 0.80,
          f"{max(len(r) for r in fig) / (2 * len(fig)):.2f} "
          f"(was {max(len(r) for r in pre_fig) / (2 * len(pre_fig)):.2f})")

    for tag, path, over in (("overdue", fx, True), ("calm", fc, False)):
        seed = json.loads(Path(path).read_text(encoding="utf-8"))
        late = [t for t in seed["tasks"]
                if t.get("due_date") and t["due_date"] < date.today().isoformat()
                and not t.get("archived") and not t.get("done")]
        check(f"nord/{tag}: the fixture's own truth is checked before the law "
              f"is written — it {'IS' if over else 'is NOT'} overdue",
              bool(late) == over, f"{len(late)} past-due task(s)")
        rows, cells, reg = await ap_panel(path)
        g = panel_inks(rows, cells, reg)
        PANEL_LOG.append(panel_table(f"CURED  {tag}  118x30", g))
        iso = isolated(g)
        tone = N["alert"] if over else N["warn"]
        top_a = max(g.values(), key=lambda d: d["cells"])
        top_e = max(g.values(), key=lambda d: d["extent"])
        num = g.get(tone, {"cells": 0, "extent": 0, "lum": 0, "rows": set()})
        # every "vs" number below comes from the OTHER groups only; empty-safe
        # so a panel that came back with one ink fails loudly instead of
        # raising and killing the run (the twenty-eighth pass's lesson about
        # the capture race, applied to this section's arithmetic)
        oth = [d for f2, d in g.items() if f2 != tone] or [
            {"cells": 0, "extent": 0, "lum": 0.0}]
        check(f"nord/{tag}: the headline numeral wears the severity tone "
              f"(probe self-check)", num["cells"] > 0,
              f"{tone} {num['cells']} cells")
        check(f"nord/{tag}: EXACTLY ONE element in the hero panel is ISOLATED "
              f"— it owns rows nothing else paints", len(iso) == 1,
              f"isolated={iso}")
        check(f"nord/{tag}: ... and it is the NUMERAL",
              iso[:1] == [tone], f"{iso[:1]} vs {tone}")
        check(f"nord/{tag}: the numeral wins AREA in cells — the measure pass "
              f"28 stated its defect in (25 against 61)",
              top_a is num, f"{num['cells']} cells vs "
              f"{max(d['cells'] for d in oth)}")
        check(f"nord/{tag}: the numeral wins AREA as EXTENT too, so the two "
              f"area measures agree and the verdict does not rest on which "
              f"one was chosen", top_e is num,
              f"{num['extent']} vs {max(d['extent'] for d in oth)}")
        check(f"nord/{tag}: the ACCENT — this language's identity and "
              f"interaction hue — is spent NOWHERE in the panel; ambient data "
              f"is drawn one rank down", N["accent"] not in g,
              f"{sorted(g)}")
        check(f"nord/{tag}: the caption is BACK (the fitted figure leaves it "
              f"room, which the 11-row one did not)",
              any(("OVERDUE" if over else "DAYS") in
                  r[reg[0]: reg[0] + reg[2]]
                  for r in rows[reg[1]: reg[1] + reg[3]]))
        check(f"nord/{tag}: nothing wraps — every panel row fits its region",
              all(len(rows[y].rstrip()) <= reg[0] + reg[2]
                  for y in range(reg[1], min(reg[1] + reg[3], len(rows)))))
        check(f"nord/{tag}: the panel's total ink FELL — the fixation is "
              f"bought with empty space, not with more marks "
              f"(empty-space-earned)",
              sum(d["cells"] for d in g.values())
              < sum(d["cells"] for d in pre_g.values()),
              f"{sum(d['cells'] for d in g.values())} cells vs "
              f"{sum(d['cells'] for d in pre_g.values())} pre-cure")
        if not over:
            check("nord/calm: the numeral's ink is the BRIGHTEST in the panel "
                  "— the strict form of law 03's third axis, asserted on the "
                  "fixture whose severity does not fight it",
                  num["lum"] == max(d["lum"] for d in g.values()),
                  f"{num['lum']:.1f} vs {max(d['lum'] for d in oth):.1f}")
        else:
            # DECLARED, not skipped quietly, and the reason is itself a check:
            # nord's alert red is DARKER than its label grey under the channel
            # sum, so a strict "brightest" claim on an overdue board would be
            # asserting the caption away. The same shape of fact as
            # blueprint's `warn == mut` (pass 37).
            check("nord/overdue: `alert` really is DARKER than `mut` in this "
                  "palette — which is why the strict brightest-ink claim is "
                  "made on the calm fixture and this one asserts the ladder",
                  chan_lum(N["alert"]) < chan_lum(N["mut"]),
                  f"alert {chan_lum(N['alert']):.1f} < "
                  f"mut {chan_lum(N['mut']):.1f}")
            check("nord/overdue: the numeral wears a RESERVED SEMANTIC hue and "
                  "no PASSIVE element in the panel is brighter than the label "
                  "tier — the boldness is spent once, on the metric",
                  max(d["lum"] for d in oth) <= chan_lum(N["mut"]),
                  f"brightest passive {max(d['lum'] for d in oth):.1f}")
    (W / "prototypes" / "out" / "_panel39.txt").write_text(
        "\n\n".join(PANEL_LOG), encoding="utf-8")

    # -- the demoted load must still be DATA, not decoration -----------------
    kn2 = LG.kit("nord")
    SER_A, SER_B = [2, 5, 3, 7, 4, 8, 6, 9], [9, 1, 8, 2, 7, 3, 6, 4]

    def hp(series, name="nord", w=113, rows=9, val="12"):
        k = LG.kit(name)
        return HE.draw(k, val, "DAYS OVERDUE", "backlog - 3 open",
                       k.t.get("calm", k["ink"]), w, rows, series=series)

    check("nord: the ambient load still CARRIES DATA — a different series "
          "renders a different row (a decoration would not move)",
          hp(SER_A) != hp(SER_B))
    check("nord: ... and it moves in GREYSCALE, so level rides on SHAPE and "
          "not on colour (DATAVIZ law 1 survives the demotion)",
          grey(hp(SER_A)) != grey(hp(SER_B)))
    check("nord: the microbar floor survives the demotion — one tiny nonzero "
          "week does not render as absence (DATAVIZ law 3)",
          grey(hp([0] * 7 + [1])) != grey(hp([0] * 8)))
    check("nord: the ambient row is still the language's own QUANTITY family "
          "— it dispatches on `meter`, so mutating that token moves it",
          grey(hp(SER_A)) != grey(_with(kn2, "meter", "dotgrid",
                                        lambda: hp(SER_A))))
    check("nord: the ambient tone is the DECLARED one and not the accent",
          N["mut"] in hp(SER_A) and N["accent"] not in hp(SER_A))
    check("nord: the load row RESERVES its caption too, so the panel never "
          "wraps at the seat where the old chart's caption had a row of its "
          "own", HE.load_width(kn2, SER_A)
          >= len(SER_A) * 2 + 1 + len(HE.PLOT_CAP),
          f"reserved {HE.load_width(kn2, SER_A)}")

    # -- ISOLATION OF THE CHANGE: nine languages and one prototype ----------
    # The pass-36 form, and the stronger one: rather than diffing against a
    # stored baseline, the tokens are TAKEN AWAY at runtime and every language
    # that does not declare them must render byte-identically either way.
    for name in TH.ORDER:
        k = LG.kit(name)
        if name == "nord":
            check("nord: it is the ONE language declaring the hero-panel "
                  "tokens", all(t in k.t for t in HP_TOK))
            continue
        check(f"{name}: declares neither hero-panel token (its hero and its "
              f"panel are untouched by this pass)",
              not any(t in k.t for t in HP_TOK))
        check(f"{name}: renders byte-identically with the tokens force-"
              f"cleared — unreachability, not a remembered baseline",
              hp(SER_A, name) == _clear_hp(name, lambda: hp(SER_A, name)))
    check("nord: and nord MOVES when they are cleared (the control that keeps "
          "the nine checks above from passing for the wrong reason)",
          hp(SER_A) != _clear_hp("nord", lambda: hp(SER_A)))
    # THE PROTOTYPE SEAT IS CURED TOO, since pass 44 folded its forked
    # `Hero.show` onto `taskboard/hero.py`. Passes 39-43 asserted the opposite
    # here — that the prototype was IDENTICAL with and without both tokens,
    # because the fork read neither — and that check is replaced in place by
    # its cured twin rather than deleted, so the arithmetic is visible: one
    # check out, one check in. nord's BOARD must still be identical, because
    # the board never renders through the hero seat at all.
    saved_hp = {k: TH.THEMES["nord"].get(k) for k in HP_TOK}
    for k in HP_TOK:
        TH.THEMES["nord"].pop(k, None)
    try:
        proto_b_off, proto_h_off, _, _ = await capture("nord",
                                                       board_path=str(fx))
    finally:
        for k, v in saved_hp.items():
            TH.THEMES["nord"][k] = v
    check("the widget-slice prototype's HERO MOVES when the hero-panel tokens "
          "are taken away — pass 44 folded its forked `Hero.show` onto "
          "`taskboard/hero.py`, so the prototype now READS them and the "
          "pass-28 fixation defect is cured at both seats, not one",
          heroes["nord"] != proto_h_off)
    check("... and nord's BOARD is identical either way — the board never "
          "renders through the hero seat, so `nord board render otherwise "
          "unchanged` is proved by unreachability rather than by a diff",
          boards["nord"] == proto_b_off)

    print("\n== THE FOLD: ONE drawing seat for heros, asserted on the SOURCE")
    # Pass 13 extracted the hero into `taskboard/hero.py` and left the
    # prototype's copy standing. Over eleven passes the copy drifted FOUR ways
    # — a metrics-blind caption wrap (`4 * sx`, deleted from the seat in pass
    # 35), its own `naught7` dispatch (pass 23), a `dot` branch that drew flap
    # FIGURES onto faces it never painted (pass 36's finding 1), and no reader
    # for `hero_plot`/`hero_fit` (pass 39's residual). Not one of them was
    # visible except by diffing two renders of the same language, which is
    # exactly the class of defect a SOURCE law can make impossible. So: the
    # prototype may CALL the seat and may not BE one.
    #
    # Every mark is paired with its negative control on `hero.py` itself. A
    # grep law that passes because the symbol was renamed everywhere is a
    # vacuous law; asserting the owning seat still holds the symbol is what
    # keeps this from rotting into a pair of `not in` on dead strings.
    PROTO_SRC = (W / "prototypes" / "widget_slice" / "app.py").read_text(
        encoding="utf-8")
    HERO_SRC = (W / "taskboard" / "hero.py").read_text(encoding="utf-8")
    for mark, what in (("HERO_FONT", "the 4x7 numeral font"),
                       ("draw_numeral", "the base's numeral renderer"),
                       ("seven_seg", "corgi's display"),
                       ("dense_type", "naught7's display type"),
                       ("dense_rule", "naught7's band separator"),
                       ("flap_faces", "solari's card geometry"),
                       ("_beside_plot", "the dead-columns join"),
                       ('"naught7"', "the naught7 branch"),
                       ('"corgi"', "the corgi branch"),
                       ('"framed"', "the framed branch")):
        check(f"the prototype draws no hero of its own: `{mark}` ({what}) "
              f"does not appear in widget_slice/app.py",
              mark not in PROTO_SRC)
        check(f"... and `{mark}` IS in taskboard/hero.py — the seat that owns "
              f"it still does (the law is not passing on a dead string)",
              mark in HERO_SRC)
    check("the prototype's hero CALLS the seat — a file that merely stopped "
          "drawing would pass every check above and render nothing",
          "HERO.draw(" in PROTO_SRC)

    # THE FOLD, MEASURED ON THE FRAME: solari's card FACES. The deleted `dot`
    # branch wrapped the flap figure in one colour and called no painter, so
    # the prototype rendered a bank of cards with unlit faces (pass 36's
    # finding 1). `seam` is the discriminating token — solari's `flap` hex is
    # also the hero widget's own TCSS ground, so the face alone cannot tell
    # the two renders apart, while the hinge BAND can and does.
    async def hero_bgs(name: str) -> set:
        from app import TaskboardWidget
        a = TaskboardWidget(board_path=str(fx))
        async with a.run_test(size=(96, 30)) as pl:
            await pl.pause()
            a.notify = lambda *x, **kw: None
            a.set_theme(name)
            await pl.pause()
            a.redraw()
            await settle(a, pl, f"{name} hero bg")
            r = a.query_one("#hero").region
            got = set()
            for y, strip in enumerate(
                    a.screen._compositor.render_strips()):
                if not (r.y <= y < r.y + r.height):
                    continue
                x = 0
                for seg in strip:
                    st = seg.style
                    bg = (st.bgcolor.triplet.hex
                          if (st and st.bgcolor and st.bgcolor.triplet)
                          else "")
                    for i in range(len(seg.text)):
                        if r.x <= x + i < r.x + r.width and bg:
                            got.add(bg.lower())
                    x += len(seg.text)
            return got

    sol_bg = await hero_bgs("solari")
    check("solari: the PROTOTYPE's hero now paints the hinge band — the fold "
          "gave its card faces the `flap_paint` channel the fork never called",
          TH.THEMES["solari"]["seam"].lower() in sol_bg, ' '.join(sorted(sol_bg)))
    _saved_fp = HE.flap_paint
    HE.flap_paint = lambda rows, *a: rows
    try:
        sol_off = await hero_bgs("solari")
    finally:
        HE.flap_paint = _saved_fp
    check("solari: ... and the band LEAVES with `flap_paint` — the control "
          "that keeps the check above from passing on the widget's own ground",
          TH.THEMES["solari"]["seam"].lower() not in sol_off, ' '.join(sorted(sol_off)))
    check("solari: the painter restores cleanly",
          TH.THEMES["solari"]["seam"].lower() in await hero_bgs("solari"))
    for lang in ("ledger", "blueprint", "nord"):
        bgs = await hero_bgs(lang)
        check(f"{lang}: its prototype hero still paints NO face — the fold "
              f"moved the mechanism, it did not spread it",
              len(bgs) <= 1, ' '.join(sorted(bgs)))

    print("\n== APP LEVEL: token mutation reaches the rendered board")
    for name, tok, val, region in (
            ("naught", "dot_w", 2, "board"),
            ("corgi", "numbered", False, "board"),
            ("swiss", "frame", "none", "board"),
            ("ledger", "tally", "•", "board"),
            ("nord", "base", "block2", "hero")):
        # MUST be the same fixture the baseline was captured on: comparing a
        # mutated fixture render against a live-board baseline would pass on
        # the task list differing, not on the token — a vacuous check
        mb, mh, _, _ = await capture(name, mutate=(tok, val),
                                     board_path=str(fx))
        if region == "board":
            check(f"mutating {name}.{tok} changes the board outside the hero",
                  mb != boards[name])
        else:
            check(f"mutating {name}.{tok} changes the hero", mh != heroes[name])
    # the rail must DISPATCH: set the token back to the base default and the
    # mechanism has to disappear from the real board, not merely from the kit
    fb, _, _, _ = await capture("darkside", mutate=("layout", "flow"),
                                board_path=str(fx))
    check("darkside.layout=flow removes the rail from the live board",
          not any(RAIL in r for r in body_rows(fb)))
    check("darkside.layout=flow keeps the board itself (probe self-check)",
          "shut down legacy servers" in fb)

    print("\n== THE LEGEND LAW: every shown key works, every working key shown")
    import app as APPMOD
    from app import (Aperture, ConfigScreen, GalleryScreen, HelpScreen,
                     TaskboardWidget)
    from textual.binding import Binding

    app_shown = shown_bindings(TaskboardWidget)
    PAL = ("^p", "palette")

    # the instrument first: a law that cannot go red is a decoration
    real = " 1 2 3 4 Views  c Signals  q Quit  ▏^p palette "
    check("probe self-check: the vocabulary accepts a legend built from the "
          "real bindings", legend_violations(real, app_shown, PAL) == [])
    check("probe self-check: a phantom legend entry is caught by name",
          legend_violations(real + " z Zap", app_shown, PAL) == ["z", "Zap"])
    check("probe self-check: a legend that renames a real key is caught",
          legend_violations(" Q Quit ", app_shown, PAL) == ["Q"])
    check("probe self-check: the rail glyph is not itself a phantom",
          "▏^p" not in legend_tokens(real))

    # -- register: nothing the legend shows may need shift ------------------
    for b in app_shown:
        check(f"register: `{APPMOD.key_of(b)}` ({b.description}) is typed "
              f"without shift",
              not LEGEND_SHIFT.search(b.key),
              f"key={b.key!r}")

    # -- per language: the rendered legend, on the composited frame ---------
    legend_rows = {}
    for lang in TH.ORDER:
        async for app, pilot in drive(lang, str(fx)):
            row = legend_row(screen_text(app))
            legend_rows[lang] = row
            shown = active_shown(app)
            toks = legend_tokens(row)
            missing = [APPMOD.key_of(b) for b in shown
                       if APPMOD.key_of(b) not in toks]
            check(f"{lang}: every shown binding's key is ON the legend",
                  not missing, f"missing {missing}" if missing else "")
            phantom = legend_violations(row, shown, PAL)
            check(f"{lang}: the legend promises nothing that is not bound",
                  not phantom, f"unaccounted {phantom}" if phantom else "")
            check(f"{lang}: the legend names what each key DOES "
                  f"(a group label instead of the descriptions is what the "
                  f"user got lost in)",
                  all(w in toks for w in ("Quit", "Language", "Gallery",
                                          "Signals", "Size", "Refresh")))
    base_lang = TH.ORDER[0]
    for lang in TH.ORDER[1:]:
        check(f"{lang}: promises the SAME key set as {base_lang} — a language "
              f"may restyle the legend, it may not change the keymap",
              legend_tokens(legend_rows[lang])
              == legend_tokens(legend_rows[base_lang]))

    # -- drive: press EXACTLY the key the legend prints, no shift -----------
    async for app, pilot in drive("instrument", str(fx)):
        before = APPMOD.THEME
        await press(pilot, "t")
        check("drive `t`: cycles the language", APPMOD.THEME != before)

        forced = app.forced
        await press(pilot, "V")
        check("drive `V`: the SHIFTED form is gone (the defect was that this "
              "was the only way in)", app.forced == forced)
        await press(pilot, "v")
        check("drive `v`: cycles the size class", app.forced != forced)

        calls = []
        engine_run_all = app.engine.run_all
        app.engine.run_all = lambda *a, **k: (calls.append(1),
                                              engine_run_all(*a, **k))[1]
        await press(pilot, "r")
        check("drive `r`: refreshes every signal", len(calls) == 1)
        app.engine.run_all = engine_run_all

        for key, view in (("2", "lanes"), ("3", "agenda"), ("4", "gantt"),
                          ("1", "board")):
            await press(pilot, key)
            check(f"drive `{key}`: switches to the {view} view",
                  app.view == view)

        for key, screen in (("g", GalleryScreen), ("c", ConfigScreen),
                            ("?", HelpScreen)):
            await press(pilot, key)
            check(f"drive `{key}`: opens {screen.__name__}",
                  isinstance(app.screen, screen))
            # -- the modal half of the law, on the surface in front ---------
            row = legend_row(screen_text(app))
            shown = active_shown(app)
            toks = legend_tokens(row)
            missing = [APPMOD.key_of(b) for b in shown
                       if APPMOD.key_of(b) not in toks]
            check(f"{screen.__name__}: its own legend shows its own keys",
                  not missing, f"missing {missing}" if missing else "")
            phantom = legend_violations(row, shown, PAL)
            check(f"{screen.__name__}: shows no key the aperture owns and this "
                  f"screen shadows (the dimmed footer underneath was "
                  f"advertising dead keys)",
                  not phantom, f"unaccounted {phantom}" if phantom else "")
            await press(pilot, "q")
            check(f"{screen.__name__}: `q` — the key the user pressed and had "
                  f"to fall back to ctrl+q for — leaves the screen",
                  isinstance(app.screen, Aperture))

        # the `?` tier is the ONLY surface the hidden keys have, which is the
        # whole reason the footer is allowed to carry less than everything
        await press(pilot, "?")
        helpframe = "\n".join(screen_text(app))
        for b in TaskboardWidget.BINDINGS:
            if not isinstance(b, Binding):
                continue
            check(f"`?` map lists {APPMOD.key_of(b)} ({b.description})"
                  + ("" if b.show else " — hidden from the footer, so this is "
                                      "its only surface"),
                  APPMOD.key_of(b) in helpframe and b.description in helpframe)
        for sys_key in ("ctrl+q", "ctrl+p"):
            check(f"`?` map lists {sys_key}, which Textual binds and no "
                  f"BINDINGS list here owns", sys_key in helpframe)
        await press(pilot, "q")

    # -- the printed hint rows are DERIVED, so they cannot drift ------------
    async for app, pilot in drive("darkside", str(fx)):
        await press(pilot, "c")
        cfg = "\n".join(screen_text(app))
        want = APPMOD.hint_row(ConfigScreen.BINDINGS)
        check("the config screen's printed hint row is the derived one",
              want in cfg, want)
        check("... and it prints the bracket keys as `[` and `]`, not as "
              "`bracketleft` (a key name nobody can type)",
              "bracketleft" not in cfg and "[ threshold" in cfg)
        await press(pilot, "q")
        gal = APPMOD.hint_row(GalleryScreen.BINDINGS)
        check("the gallery's hint row claims only bound keys — it claimed "
              "`t language` for three passes while a ModalScreen shadowed it",
              gal == "esc/q/g close · t language", gal)

    # -- the quit path, on its own app: pressing it ENDS the process --------
    from app import TaskboardWidget as _TW
    quit_app = _TW(board_path=str(fx))
    async with quit_app.run_test(size=(118, 30)) as quit_pilot:
        await quit_pilot.pause()
        quit_app.notify = lambda *a, **kw: None
        await settle(quit_app, quit_pilot, "quit path")
        await press(quit_pilot, "q", 6)
        check("drive `q` on the aperture: plain `q` quits, so ctrl+q is a "
              "fallback and not the only door", not quit_app.is_running)

    # =====================================================================
    # THE SUITE'S OWN LAW — the sixty-sixth pass's oracle sweep, standing
    # =====================================================================
    # Every law above is about the app. This one is about the LAWS, and it
    # exists because three passes in a row (61, 63, 65) each found a standing
    # law that could not fail — by accident, one per pass, while doing
    # something else. A base rate of one vacuous law per pass is a backlog,
    # not a finding.
    #
    # THE DETECTOR IS IMPORTED, NOT RE-TYPED, and that is the whole argument:
    # re-typing `_p66_sweep`'s trap census inside this file would BE the
    # defect its shape 2 describes — a law sweeping its own copy of the
    # thing, which the mutation cannot reach. One definition, imported,
    # exactly as pass 65 imported pass 62's prover rather than re-typing it.
    #
    # THE IMPORT'S SUCCESS IS PART OF THE CONDITION (VERIFY.md: "make the
    # thing's existence part of the law's CONDITION so a missing state goes
    # red instead of skipping"). A deleted or broken sweep reds here; it does
    # not quietly skip.
    print("\n== THE SUITE'S OWN LAW: the oracle sweep, standing (pass 66)")
    # THE BINDING HAPPENS AFTER THE EXEC, and that is mutant M5's finding.
    # The first draft bound `_sweep` to `module_from_spec(...)` first, so a
    # DELETED instrument left a non-None EMPTY module — the presence law went
    # red correctly and the trap law then died on `AttributeError`, taking
    # the run with it. The law that exists to say "a raised law reports
    # nothing" had that exact defect on its second line.
    _sweep, _sweep_err = None, ""
    try:
        _sp = importlib.util.spec_from_file_location(
            "_p66_sweep", Path(__file__).parent / "out" / "_p66_sweep.py")
        _m = importlib.util.module_from_spec(_sp)
        _sp.loader.exec_module(_m)
        _sweep = _m
    except Exception as e:                        # noqa: BLE001
        _sweep_err = f"{type(e).__name__}: {e}"
    check("sweep: the oracle sweep is present and runs on this suite "
          "(a law whose instrument is missing must RED, not skip)",
          _sweep is not None and hasattr(_sweep, "raise_trap"),
          _sweep_err or "imported")
    # THE NAMED TRAP, ZERO. `.index` where `find` was meant, `.rindex`, and
    # `next()` with no default — in a law's condition, in its DETAIL (which
    # is evaluated on every call, pass or fail), and in the setup lines that
    # feed it. The sweep found 52 of these still standing at 34 sites in this
    # file, in a law's condition, in its DETAIL (evaluated on every call, pass
    # or fail) and in every helper and setup line between them; every one is
    # now `at()` or `first_of()`, and this is what keeps them that way. A
    # raised law reports NOTHING — it is not one red, it is the rest of the
    # file unspoken.
    _trap = (_sweep.raise_trap() if hasattr(_sweep, "raise_trap")
             else [(0, "THE SWEEP ITSELF IS MISSING", "")])
    check("sweep: NO law and NO setup line in this suite can RAISE where it "
          "should go red — the named trap, swept to zero",
          _trap == [],
          f"{len(_trap)} construct(s)"
          + (f"; first at L{_trap[0][0]}: {_trap[0][2][:48]}" if _trap
             else ""))
    # AND THE DETECTOR MUST BE ABLE TO SEE. A sweep reporting zero on a
    # broken detector reads exactly like a clean suite — this is the
    # detector's own planted control, asserted here rather than trusted.
    check("sweep: ... and the shape-2 detector is not blind (a planted "
          "alpha-renamed copy of `coverage_index`'s clamp is seen)",
          bool(getattr(_sweep, "D2_SELFTEST", False)))
    # THE `[n]` CLASS, ZERO — PENDING #47, and a SECOND law rather than a
    # wider tuple on the first, because the two need different cures. The
    # named trap has one right answer everywhere (-1) and its law is
    # absolute. `[0]` on an empty list has none: the sentinel has to red
    # THAT law, and for a negative claim no sentinel can, so those sites
    # carry an explicit non-emptiness leg instead. 33 constructs at 24 sites
    # were standing when this was written — 31 cured through the `nth()`
    # seat or a leg, 2 exempted below with their arguments.
    #
    # AND THE COUNT IS `laws + SETUP LINES`, which is the half pass 66's
    # census could not see. Mutant M2a died on `ib[iax[0]]` in an ASSIGNMENT
    # three lines under the law that proves `len(iax) == 1` — a `check()`
    # reports and the run CONTINUES, so a check above a setup line is not a
    # guard, and eleven sites in this file sat behind exactly that comfort.
    _nth = (_sweep.nth_trap() if hasattr(_sweep, "nth_trap")
            else [(0, "THE SWEEP ITSELF IS MISSING", "")])
    check("sweep: NO law and NO setup line in this suite can raise on a "
          "`[n]` into a POSSIBLY-EMPTY sequence — PENDING #47, swept to zero",
          _nth == [],
          f"{len(_nth)} construct(s)"
          + (f"; first at L{_nth[0][0]}: {_nth[0][2][:48]}" if _nth else ""))
    # THE EXEMPTIONS, CLAIMED **AND USED**. Two sites index a sequence the
    # detector calls possibly-empty and that is non-empty by construction —
    # both are its one-hop whole-file name resolution being coarse, and both
    # are LISTED rather than out-clevered, because a dataflow heuristic that
    # quietly stops reporting is worse than an exemption something measures.
    #
    # THIS IS THE MEASUREMENT THAT MAKES THE LIST HONEST: an exemption is a
    # claim, and a claim nothing checks is where a red goes to die. Each
    # `# nth-exempt:` marker must sit on a line the detector really does
    # flag. The moment a cure makes one unnecessary, or a maintainer widens
    # one past its evidence to silence a red, it stops being USED and this
    # goes red — which is the whole difference between an exemption and a
    # hole.
    _nx = (_sweep.nth_exemptions() if hasattr(_sweep, "nth_exemptions")
           else [(0, "THE SWEEP ITSELF IS MISSING", False)])
    _nx_dead = [(ln, why) for ln, why, used in _nx if not used]
    check("sweep: ... and every `# nth-exempt:` claim is USED — an exemption "
          "no hit sits under is an exemption widened past its evidence",
          _nx_dead == [] and len(_nx) == 2,
          f"{len(_nx)} claimed, {len(_nx_dead)} unused"
          + (f" (first L{_nx_dead[0][0]})" if _nx_dead else ""))

    print("\n== THE GATE ITSELF: settle headroom")
    worst = max(SETTLE_USED) if SETTLE_USED else 0
    check("settle() keeps headroom under its bound (a gate near its limit "
          "is a gate about to rot)",
          worst * 2 <= SETTLE_MAX,
          f"worst {worst} of {SETTLE_MAX} over {len(SETTLE_USED)} captures")

    print("\n" + ("ALL PASSED" if not fails
                  else f"{len(fails)} FAILURE(S): {fails}"))
    sys.exit(1 if fails else 0)


asyncio.run(main())
