"""screens.py -- the six canonical screens, composed out of kit primitives.

WHAT THIS FILE IS ALLOWED TO DO.  It calls `taskboard.language` and lays the
results out.  It does not restyle them, it does not reach into a kit, and it
changes nothing in `taskboard/`.  Everything a language can already say is
said by a kit call; everything it cannot is drawn HERE, once, and REGISTERED --
and the registration is not documentation, it is the mechanism: `row()` takes
the candidates that row's hand-drawn elements answer to, and `Sheet.check()`
refuses to hand back a frame whose hand-drawn elements were never declared.
That is the spec's "no hand-drawn element ships unmarked" made unconstructable
rather than remembered.

THE THREE VERDICTS ARE THE SPEC'S, and the vocabulary is closed:

  implemented -- a kit method drew it; the language already had an answer
  evoked      -- drawn here, looks right, NO mechanism behind it
  refused     -- the language's answer is "no", and the reason is a
                 commitment, not a gap (L-33 is one of these)

A refusal still RENDERS: the frame shows what the language does INSTEAD, which
is the whole difference between a design answer and a blank.
"""
from __future__ import annotations

import re
from typing import NamedTuple

import taskboard.language as LG
from taskboard.language import (DEFAULT, DISABLED, EDITED, FOCUSED,
                               INVALID)

import fixture as F

W, H = 100, 32

# ---------------------------------------------------------------------------
# measuring a markup string.  `mark()` escapes a literal `[` as `\[`, so the
# two must be undone in the right order or an escaped bracket is read as a tag.
# ---------------------------------------------------------------------------
_ESC = "\x00"
_TAG = re.compile(r"\[[^\]]*\]")


def vis(s: str) -> str:
    """The CELLS a markup string will occupy, as plain text."""
    return _TAG.sub("", s.replace("\\[", _ESC)).replace(_ESC, "[")


def wid(s: str) -> int:
    return len(vis(s))


def pad(s: str, n: int) -> str:
    """Markup padded to exactly `n` cells (never clipped -- the caller sizes)."""
    return s + " " * max(0, n - wid(s))


def clip(s: str, n: int) -> str:
    """Markup cut to at most `n` CELLS, with every open style closed.

    WHY THIS IS NEEDED AND NOT A CONVENIENCE.  A kit method handed `w` does
    not promise to return `w` cells -- ledger's `sect()` fills its leaders to
    `w` and THEN appends the note, so a header asked for 38 comes back at 50.
    In a `Static` that overflow does not vanish, it WRAPS, and a wrapped row
    pushes every row under it down by one: the first sweep of this file put
    `redirect` and `Web` on lines of their own in three languages and the
    frame still looked plausible.  Clipping is the honest failure, and
    `Sheet.body()` reports every row it had to cut rather than swallowing it.
    """
    out: list[str] = []
    count = depth = i = 0
    while i < len(s) and count < n:
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] == "[":
            out.append("\\[")
            count += 1
            i += 2
            continue
        if s[i] == "[":
            j = s.find("]", i)
            if j == -1:
                out.append(s[i])
                count += 1
                i += 1
                continue
            tag = s[i:j + 1]
            out.append(tag)
            depth = max(0, depth - 1) if tag == "[/]" else depth + 1
            i = j + 1
            continue
        out.append(s[i])
        count += 1
        i += 1
    return "".join(out) + "[/]" * depth


def txt(k, s: str, tone: str = "ink") -> str:
    return f"[{k.c[tone]}]{LG.mark(s)}[/]"


def meta_of(t) -> dict:
    """THE CARD'S META CONTRACT, read off the kits rather than guessed.

    `Corgi._param_values` reads `days` / `prio` / `done` / `blocked`;
    `Blueprint.card_rows` reads `proj` / `phase` / `prio`; the base kit reads
    `proj` / `phase`.  The first sweep passed only the last pair, so corgi's
    three engraved slots came back `DUE -- PR - ST OPEN` on every row and
    blueprint lost its priority field -- two languages judged on a card they
    were never given the data to draw.  A fixture that under-feeds a kit
    flatters the kits that ask for less.
    """
    title, proj, phase, days, prio, status = t
    return {"proj": proj, "phase": phase, "days": days, "prio": prio,
            "done": phase == "done", "blocked": status == "blocked"}


class Cand(NamedTuple):
    """One hand-drawn element and the primitive it proposes."""
    element: str        # what was drawn in the frame
    verdict: str        # evoked | refused   (implemented never lands here)
    name: str           # the proposed primitive's name
    sig: str            # its signature
    commitment: str     # the language commitment it must honour


class Sheet:
    """A frame under construction, and the ledger of what was drawn by hand."""

    def __init__(self, kit, lang: str, screen: str):
        self.k, self.lang, self.screen = kit, lang, screen
        self.rows: list[str] = []
        self.cands: dict[str, tuple[Cand, list[int]]] = {}
        self._used: set[str] = set()
        #: chrome a language DOCKS rather than stacks.  Blueprint's whole
        #: frame budget is "a 3-row stamp docked to the BOTTOM corner"
        #: (LANGUAGES.md #11), so printing its title block at the top --
        #: which the first sweep did -- breaks the one frame commitment the
        #: language has.  `build()` places these last.
        self.chrome_tail: list[str] = []

    def row(self, markup: str = "", *cands: Cand) -> None:
        """Append one row.  Every hand-drawn element in it is declared here."""
        self.rows.append(markup)
        n = len(self.rows)
        for cd in cands:
            if cd.name in self.cands:
                self.cands[cd.name][1].append(n)
            else:
                self.cands[cd.name] = (cd, [n])
            self._used.add(cd.name)

    def note(self, cd: Cand) -> None:
        """Declare a candidate with no row of its own -- a refusal whose whole
        answer is that nothing is drawn.

        A note OVERWRITES a generic candidate of the same name while KEEPING
        the rows already recorded against it.  That is not a convenience: the
        per-language builders exist precisely to replace a shared candidate's
        commitment with the one this language is actually judged against, and
        a `setdefault` here silently kept the generic text and threw the
        sharp one away -- which is how prism's "borders are RESERVED for
        modals" and blueprint's "not one element is boxed" were both lost on
        the first sweep."""
        rows = self.cands[cd.name][1] if cd.name in self.cands else []
        self.cands[cd.name] = (cd, rows)

    def blank(self, n: int = 1) -> None:
        for _ in range(n):
            self.rows.append("")

    def fill(self, upto: int) -> None:
        while len(self.rows) < upto:
            self.rows.append("")

    #: rows this sheet had to CUT to fit the frame, as (row number, cells
    #: asked for).  Read by `render.py` and printed -- a frame that only fits
    #: because it was trimmed is a finding about the language's width
    #: appetite, not a detail of the writer.
    def body(self) -> tuple[str, list[tuple[int, int]]]:
        over = [(i + 1, wid(r)) for i, r in enumerate(self.rows[:H])
                if wid(r) > W]
        return "\n".join(clip(pad(r, W), W) for r in self.rows[:H]), over


# ===========================================================================
# shared pieces every screen uses
# ===========================================================================
def chrome(sh: Sheet, active: str) -> None:
    """The app's mode row, through whatever notation the language has for one.

    `tabs()` is a kit method in every language, so this is IMPLEMENTED
    everywhere -- but it is not the same height everywhere: blueprint's is a
    three-row stamp with registration marks, which is that language's answer
    to "no persistent chrome" and is left at its own size rather than trimmed.

    AND IT DOES NOT SIT IN THE SAME PLACE EVERYWHERE.  Blueprint's whole
    frame budget is one stamp "docked to the bottom corner ... the corner
    where a drawing keeps its identity" (LANGUAGES.md #11).  The first sweep
    of this file printed it at the TOP, which breaks the only frame
    commitment the language has -- so a titleblock language defers its
    chrome here and `build()` docks it.
    """
    lines = sh.k.tabs(F.MODES, active).split("\n")
    if sh.k.frame == "titleblock":
        sh.chrome_tail = lines
        return
    for line in lines:
        sh.row(line)


def header(sh: Sheet, title: str, note: str) -> None:
    for line in sh.k.sect(title, note, W, 4):
        sh.row(line)


def rule(sh: Sheet) -> None:
    r = sh.k.rule_line(W)
    sh.row(r if r is not None else "")


# --- the candidates that recur across screens ------------------------------
# `C_SPLIT` was here until inc28.  `Kit.pane_split` seats it, and the whole
# `s1_blueprint` builder went with it -- that override existed only to strip
# the `│` this file had no business printing in blueprint's frame.

# `C_ERROR` and `C_REQUIRED` were here until inc29.  `Kit.error` seats the
# message row -- the mark is the language's own `LEVELS["error"]`, the words
# come back byte for byte, and the remainder is the language's (leaders, unlit
# lattice, a dashed revision extension, bare panel).  `Kit.required` seats the
# marker: the `*` this file printed in five languages at once was the
# palette-swap failure at one glyph, which is what its own commitment said.

# `C_TEXTAREA` was here until inc30.  `Kit.textarea` seats it and declares
# nothing per-language: the walls, the paper, the caret's own column and the
# lit/unlit tiers are all seats `textfield` already had, and the wrap mark is
# `DISCLOSE` -- the third component to spend the same declaration.


# ===========================================================================
# S1 -- LIST + DETAIL
# ===========================================================================
def s1(sh: Sheet) -> None:
    k, c = sh.k, sh.k.c
    chrome(sh, "board")
    header(sh, "BOARD", f"{sum(n for _, n in F.COLUMNS)} tasks  ·  4 projects")

    # the separator seat is THREE cells (` │ `), not two -- the first sweep
    # budgeted two and every pane row came out at 101 cells and wrapped.
    left, sep_w = 60, 3
    right = W - left - sep_w

    # -- the detail pane's rows, built first so the two panes can be zipped --
    det: list[str] = []
    for line in k.sect("DETAIL", F.TASKS[F.SELECTED][0][:right - 14], right, 3):
        det.append(clip(line, right))
    # THE DEFINITION ROWS, through the kit (inc15).  This loop used to draw
    # ledger's dot leaders in five languages -- one language's typographic
    # argument generalised into four that never chose it.  Each language now
    # answers for itself: air to a right column, an engraved silkscreen, a
    # dimension, an ember frontier, an unlit lattice, dot leaders.
    for cap, val in F.DETAIL:
        det.append(clip(k.field_row(cap, val, right), right))
    det.append("")
    det.append(k.meter(F.WORK[0], F.WORK[1], F.COUNTS, right).split("\n")[0])

    # -- the list pane ------------------------------------------------------
    lst: list[str] = []
    for ci, (name, n) in enumerate(F.COLUMNS):
        focus = ci == F.FOCUS_COL
        for line in k.head(name, n, left - 2, ci).split("\n"):
            lst.append("  " + line if not focus else
                       f"[{c['accent']}]{k.CUR}[/] " + line)
        if n == 0:
            for line in k.empty(left - 4).split("\n"):
                lst.append("    " + line)
            lst.append("")
            continue
        for ti, t in enumerate(F.TASKS):
            if t[2] != name.lower():
                continue
            sel = focus and ti == F.SELECTED
            tone = (c["alert"] if t[3] is not None and t[3] < 0
                    else c["warn"] if t[3] is not None and t[3] <= 3
                    else c["mut"])
            chip = "--" if t[3] is None else (f"{t[3]}d" if t[3] > 0
                                              else f"{-t[3]}d!")
            cur = f"[{c['accent']}]{k.CUR}[/] " if sel else "  "
            for j, line in enumerate(k.card_rows(t[0], chip, tone, left - 4,
                                                 ti, t[3] is not None
                                                 and t[3] < 0, meta_of(t))):
                lst.append((cur if j == 0 else "  ") + "  " + line)
        lst.append("")

    # -- the scroll indication ---------------------------------------------
    st, sz, tot = F.SCROLL
    bar = k.scrollbar(st, sz, tot, 12)

    top = len(sh.rows)
    room = H - top - 2
    # THE DIVIDER, through the kit (inc28).  This loop printed `│` in five
    # languages at once -- the terminal's own convention generalised into four
    # that never chose it, which is the red `!` and the borrowed dot leader at
    # one cell.  Each language answers for itself now: a solid display bar, an
    # unlit lattice column, a ruled money column opened at its head rule, a
    # grey step of background, two datums that never join.
    #
    # AND `s1_blueprint` IS GONE WITH IT -- the fifth per-language builder this
    # sweep has deleted.  It existed to REPLACE a `│` this file should not have
    # printed, which is the shape every one of the five had.
    split = k.pane_split(room, sep_w)
    for i in range(room):
        l = clip(lst[i] if i < len(lst) else "", left)
        r = clip(det[i] if i < len(det) else "", right)
        sh.row(pad(l, left) + split[i] + r)
    sh.row(pad(f"[{c['dim']}]{LG.mark('view')}[/] " + bar
                + f" [{c['mut']}]{LG.mark(f'{st + 1}-{st + sz} of {tot}')}[/]",
                left))


# ===========================================================================
# S2 -- FORM WITH VALIDATION
# ===========================================================================
def s2(sh: Sheet) -> None:
    k, c = sh.k, sh.k.c
    chrome(sh, "form")
    header(sh, "NEW TASK", "5 fields  ·  1 invalid")

    lab = 14
    # THE REQUIRED MARK, through the kit (inc29).  This was `*` in the alert
    # hue, in five languages at once.
    req = k.required()

    def field(caption: str, control: str, required: bool = False,
              *cands: Cand) -> None:
        cap = f"[{c['mut']}]{LG.mark(caption)}[/]"
        head = pad(cap + (req if required else " "), lab)
        sh.row("  " + head + control, *cands)

    # title -- textfield in EDITED, which is the kit's own caret state
    field("title", k.textfield(F.FORM_TITLE, F.FORM_TITLE_CARET, 34, EDITED),
          True)
    sh.blank()

    # due -- the INVALID field, drawn in the kit's own sixth state (inc14).
    # The mark is the LANGUAGE's ground -- ledger daggers it, corgi mis-seats
    # the segment bank, blueprint reverses the dimension -- and the `!` this
    # file used to add is gone, because that `!` in five languages at once was
    # the finding the round reported.
    bad = k.textfield(F.FORM_DUE_RAW, None, 34, INVALID)
    field("due", bad, True)
    # THE MESSAGE ROW, through the kit (inc29).  The words are the caller's and
    # come back byte for byte; the mark and the remainder are the language's.
    sh.row(" " * (lab + 2) + k.error(F.FORM_DUE_ERROR, W - lab - 4))
    sh.blank()

    field("priority", k.radio_group(F.PRIORITIES, F.PRIORITY_SEL))
    sh.blank()

    tags = "  ".join(k.checkbox(on) + " " + f"[{c['mut']}]{LG.mark(t)}[/]"
                     for t, on in F.TAGS)
    field("tags", tags)
    sh.blank()

    # notes -- the rectangle, through the kit (inc30).  The walls, the paper
    # and the caret's column are the one-line field's own seats, so a language
    # that answered `textfield` has already answered this.  DRAWN IN `DEFAULT`
    # AND WITH NO CARET, because the caret is in `title` on this frame and a
    # form with two insertion points is a state the model cannot be in -- the
    # caret row is exercised in `tests/test_components.py` instead.
    cap = pad(f"[{c['mut']}]{LG.mark('notes')}[/] ", lab)
    for i, line in enumerate(k.textarea(F.NOTES, None, 34,
                                        len(F.NOTES) + 1, DEFAULT)):
        sh.row("  " + (cap if i == 0 else " " * lab) + line)
    sh.blank()

    # the two buttons -- Save DISABLED because `due` is invalid.  Both states
    # are the kit's own, so this row is fully implemented.
    save = k.button("Save", 10, DISABLED if not F.SAVE_ENABLED else FOCUSED)
    cancel = k.button("Cancel", 10, DEFAULT)
    sh.row("  " + " " * lab + save + "   " + cancel)
    sh.row("  " + " " * lab
           + f"[{c['dim']}]{LG.mark('Save is held until due parses')}[/]")


# ===========================================================================
# S3 -- SETTINGS  (COMPONENTS.md's canary)
# ===========================================================================
def s3(sh: Sheet) -> None:
    k, c = sh.k, sh.k.c
    chrome(sh, "cfg")
    header(sh, "SETTINGS", "5 switches  ·  2 selects  ·  1 slider")

    lab = 26
    for i, (label, on, dis) in enumerate(F.SWITCHES):
        st = DISABLED if dis else DEFAULT
        cap = f"[{c['dim'] if dis else c['mut']}]{LG.mark(label)}[/]"
        sh.row("  " + pad(cap, lab) + k.switch(on, 3, st)
               + ("   " + f"[{c['dim']}]{LG.mark('(no remote configured)')}[/]"
                  if dis else ""))
    sh.blank()

    # -- the two selects, through the kit (inc16).  `select` is its own
    # primitive now: a stepper shows the two ways OFF a value, a select shows
    # the one way INTO a list, and the disclosure mark is the language's.
    for label, opts, sel, is_open in F.SELECTS:
        cap = f"[{c['mut']}]{LG.mark(label)}[/]"
        sh.row("  " + pad(cap, lab) + k.select(opts, sel, 7))
        if not is_open:
            continue
        for line in k.menu(opts, sel, 7):
            sh.row("  " + " " * lab + "  " + line)
    sh.blank()

    sh.row("  " + pad(f"[{c['mut']}]{LG.mark(F.SLIDER_LABEL)}[/]", lab)
           + k.slider(F.SLIDER_VAL, 0, 100, 14))
    sh.blank()

    # -- the danger zone, through the kit (inc16).  The severity is a SHAPE
    # the control itself carries (`danger=True`), so the zone no longer needs
    # a hand-drawn red word to announce it -- which is all that word was.
    r = k.rule_line(W - 4)
    sh.row("  " + (r if r is not None else ""))
    sh.row("  " + k.field_row("danger zone", F.DANGER_LABEL, W - 4))
    sh.row("  " + k.button(F.DANGER_ACTION, 12, DEFAULT, danger=True)
           + "   " + f"[{c['dim']}]{LG.mark('7 tasks, not recoverable')}[/]")


# ===========================================================================
# S4 -- MODAL DIALOG
# ===========================================================================
def _under(sh: Sheet) -> tuple[list[str], list[Cand]]:
    """The board, as the thing the dialog stands in front of.

    IT MUST BE **THIS LANGUAGE'S** BOARD, not the generic one.  The first
    sweep called `s1` directly, so blueprint's backdrop carried the `│` pane
    rule that `s1_blueprint` exists to refuse -- the language was shown
    drawing a mark its own alphabet cannot construct, in a frame meant to
    judge exactly that.  Going through the dispatch table also carries the
    backdrop's own candidates forward, which is why they are returned: a
    hand-drawn element does not stop being hand-drawn because it was drawn
    behind something else.
    """
    tmp = Sheet(sh.k, sh.lang, "S1")
    BUILDERS["S1"].get(sh.lang, s1)(tmp)
    return tmp.rows, [cd for cd, _ in tmp.cands.values()]


def s4(sh: Sheet) -> None:
    """ONE builder, five compositions (inc17).

    The five per-language S4 builders this file used to carry are gone, and
    that is the increment: every one of them existed to draw a FRAME the kit
    had no seat for, and four of them existed to draw the ABSENCE of one. The
    rows below are the caller's words -- a title, two lines, two answers --
    and what separates them from the board behind them is now the language's,
    read out of `MODAL_BORDER_REFUSED` and composed by `Kit.overlay`.
    """
    k, c = sh.k, sh.k.c
    under, back = _under(sh)
    rows = [f"[{c['ink']}]{LG.mark(F.MODAL_TITLE)}[/]", ""]
    rows += [f"[{c['mut']}]{LG.mark(b)}[/]" for b in F.MODAL_BODY]
    rows += ["", answers(sh)]
    out = k.overlay(rows, W, H, under)
    for line in out:
        sh.row(line)
    carry(sh, out, under, back)


def answers(sh: Sheet) -> str:
    """The two answers, with the destructive one carrying its own severity
    (inc16's `danger=True`) and the focus ring on it because it is the
    default."""
    k = sh.k
    return (k.button("Delete", 10, FOCUSED, danger=True) + "   "
            + k.button("Cancel", 10, DEFAULT))


def carry(sh: Sheet, out: list[str], under: list[str],
          back: list[Cand]) -> None:
    """Carry the BACKDROP's candidates forward -- but only if the backdrop is
    still on the screen.

    A hand-drawn element does not stop being hand-drawn because it was drawn
    behind something else; it DOES stop being on the frame when the language's
    answer is that there is nothing behind (corgi's mode takes the screen).
    Decided by looking at the composed rows rather than by a list of language
    names, so a language that changes its mind changes this too."""
    seen = "\n".join(vis(r) for r in out)
    keep = any(vis(u).strip() and vis(u).strip() in seen for u in under)
    if not keep:
        return
    for cd in back:
        sh.note(cd)


def s4_blueprint(sh: Sheet) -> None:
    """Blueprint's confirm, and the ONE thing this language changes: operator
    ruling 10 lets its single knockout MOVE from the title block to the
    default answer.

    It is affordable exactly here. `_state_cell` spends the reverse on the
    `alert` mood alone, and this sheet's mood is calm -- so the sheet's one
    knockout is UNSPENT and the confirm may take it without the title block
    losing anything. "Exactly one element per view" holds by arithmetic, not
    by promise.

    The knockout is also the one mark in this file that does NOT survive the
    `.txt`: an inversion is a background, so the cell grid shows the word and
    not the emphasis. Read it in the `.svg`.
    """
    k, c = sh.k, sh.k.c
    chrome(sh, "board")                # deferred: the stamp docks at the foot
    under, back = _under(sh)
    rows = [f"[{c['ink']}]{LG.mark(F.MODAL_TITLE.upper())}[/]", ""]
    rows += [f"[{c['mut']}]{LG.mark(k.LEAD + k.EXT * 2 + ' ' + b.upper())}[/]"
             for b in F.MODAL_BODY]
    rows += ["", k.knockout_cell(" DELETE ") + "   "
             + k.button("CANCEL", 8, DEFAULT)]
    out = k.overlay(rows, W, H - len(sh.chrome_tail), under)
    for line in out:
        sh.row(line)
    carry(sh, out, under, back)


# ===========================================================================
# S5 -- LIVE MONITOR / LOG
# ===========================================================================
def s5(sh: Sheet) -> None:
    k, c = sh.k, sh.k.c
    chrome(sh, "log")
    header(sh, "MONITOR", "8 events  ·  held")

    # -- the readout.  `readbar` IS the passive-readout primitive (a slider
    # with the knob taken away), so the BAR is implemented everywhere.  What
    # differs is the LEGEND, and corgi's is a refusal (L-33).
    legend(sh)
    sh.blank()

    # -- the sparkline, on a SHARED ceiling so two traces stay comparable
    sh.row("  " + f"[{c['mut']}]{LG.mark(pad('rate  ', 8))}[/]"
           + k.spark(F.RATE_SERIES, 40, F.RATE_CEILING)
           + f"  [{c['dim']}]{LG.mark('ceiling ' + str(F.RATE_CEILING))}[/]")
    sh.blank()
    r = k.rule_line(W - 4)
    sh.row("  " + (r if r is not None else ""))

    # -- the log, through the kit (inc18).  The level is a GLYPH LADDER in
    # each language -- lit dots, segment height, the ember ramp, the margin
    # dagger, the drawing's weights -- so the row sorts with the colour taken
    # away.  The `!!` in the alert hue that five languages shared is gone.
    for ts, lvl, msg in F.LOG:
        sh.row("  " + k.log_row(lvl, ts, msg))

    # -- the tail: the live edge is the last row's own mark, not a widget
    last_ts, last_lvl, last_msg = F.LOG[-1]
    sh.rows[-1] = "  " + k.log_row(last_lvl, last_ts, last_msg,
                                   tail=not F.PAUSED)
    sh.row("  " + f"[{c['dim']}]{LG.mark('        ')}[/]"
           + (f"[{c['mut']}]{LG.mark('held -- space resumes')}[/]"
              if F.PAUSED
              else k.spinner(2) + f" [{c['mut']}]{LG.mark('live')}[/]"))


def legend(sh: Sheet) -> None:
    """The passive readout's label -- and the one place L-33 bites.

    Every language here gets the same BAR (`readbar`, the kit's own readout).
    What they do not share is how the readout is NAMED: a numbered language
    that numbers a readout is spending a keybinding on something nobody can
    act on, which is the decorative numbering §3b defines itself against.
    """
    k, c = sh.k, sh.k.c
    bar = k.readbar(F.RATE_VALUE, 0, F.RATE_CEILING, 14)
    if k.numbered:
        # corgi and ledger number their CONTROLS.  A readout is labelled.
        sh.row("  " + f"[{c['mut']}]{LG.mark(pad(F.RATE_LABEL, 12))}[/]"
               + bar)
        sh.note(Cand(
            "the readout's label -- LABELLED, never numbered",
            "refused", "Kit.readout_label",
            "Kit.readout_label(self, label: str) -> str",
            "L-33: 'because the numbering IS the keymap, this language has "
            "no notation for a passive readout.  A [5] over a chart nobody "
            "can act on is the decorative numbering §3b defines itself "
            "against.  Readouts are LABELLED; controls are NUMBERED.'  The "
            "right response to wanting a numbered readout is to notice"))
    else:
        sh.row("  " + f"[{c['mut']}]{LG.mark(pad(F.RATE_LABEL, 12))}[/]"
               + bar)


# ===========================================================================
# S6 -- COMMAND PALETTE
# ===========================================================================
def s6(sh: Sheet) -> None:
    k, c = sh.k, sh.k.c
    chrome(sh, "board")
    header(sh, "COMMAND", f"query '{F.QUERY}'  ·  6 results")

    sh.row("  " + f"[{c['accent']}]{LG.mark('> ')}[/]"
           + k.textfield(F.QUERY, len(F.QUERY), 40, EDITED))
    sh.blank()

    # THE RESULT ROWS, through the kit (inc19).  `match` finds the query in
    # the text and marks it WITHOUT touching a byte of it -- the three
    # languages here that letter their titles in capitals may not letter
    # these (operator ruling 9).  The span the frame used to compute by hand
    # is the kit's business now, which is also why `F.RESULTS`' precomputed
    # span is no longer read.
    for i, (label, _span, hint) in enumerate(F.RESULTS):
        sel = i == F.RESULT_SEL
        cur = f"[{c['accent']}]{k.CUR}[/] " if sel else "  "
        body = k.match(label, F.QUERY)
        keyc = (f"[{c['dim']}]{LG.mark(hint)}[/]" if hint else "")
        sh.row("  " + cur + pad(body, 44) + keyc)
    sh.blank()
    r = k.rule_line(W - 4)
    sh.row("  " + (r if r is not None else ""))

    # -- the no-match state -------------------------------------------------
    sh.row("  " + f"[{c['accent']}]{LG.mark('> ')}[/]"
           + k.textfield(F.QUERY_EMPTY, len(F.QUERY_EMPTY), 40, EDITED))
    sh.blank()
    for line in k.empty(40).split("\n"):
        sh.row("    " + line)
    sh.blank()

    # the hint row: the kit owns the notation, the fixture owns every key
    sh.row("  " + k.keyhint(F.HINTS, W - 4))


# ===========================================================================
# the dispatch table -- per-language overrides, named rather than guessed
# ===========================================================================
BUILDERS = {
    "S1": {},
    "S2": {},
    "S3": {},
    "S4": {"blueprint": s4_blueprint},
    "S5": {},
    "S6": {},
}
BASE = {"S1": s1, "S2": s2, "S3": s3, "S4": s4, "S5": s5, "S6": s6}
SCREENS = ["S1", "S2", "S3", "S4", "S5", "S6"]
TITLES = {"S1": "list + detail", "S2": "form with validation",
          "S3": "settings", "S4": "modal dialog",
          "S5": "live monitor / log", "S6": "command palette"}


def build(lang: str, screen: str) -> Sheet:
    kit = LG.kit(lang)
    sh = Sheet(kit, lang, screen)
    fn = BUILDERS[screen].get(lang, BASE[screen])
    fn(sh)
    if sh.chrome_tail:
        n = len(sh.chrome_tail)
        sh.rows = sh.rows[:H - n]
        while len(sh.rows) < H - n:
            sh.rows.append("")
        sh.rows += sh.chrome_tail
    sh.rows = sh.rows[:H]
    return sh
