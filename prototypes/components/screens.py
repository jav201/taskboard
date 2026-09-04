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
from taskboard.language import (DEFAULT, DISABLED, EDITED, FOCUSED)

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
C_SPLIT = Cand(
    "the vertical divider between the list and the detail pane",
    "evoked", "pane_split",
    "Kit.pane_split(h: int) -> list[str]",
    "the language's own answer to 'two regions side by side' -- a rule, a "
    "grey step, air, or a refusal; COMPOSITION is a per-kit commitment "
    "(COMPONENTS.md: 'composition is the last palette-swap')")

C_INVALID = Cand(
    "the invalid field's mark and its inline message",
    "evoked", "STATES += INVALID  /  Kit.error(msg, w)",
    "LG.INVALID = 'invalid'; Kit.error(self, msg: str, w: int) -> str",
    "a sixth control state, derived in `component_states` like the other "
    "five, reading on GLYPH + STRUCTURE and never on the alert hue alone "
    "(COMPONENTS.md state matrix; NAVIGATION.md 'never colour alone')")

C_REQUIRED = Cand(
    "the required-field marker beside a caption",
    "evoked", "Kit.required()",
    "Kit.required(self) -> str",
    "one mark, in the language's own notation -- corgi numbers, ledger "
    "leaders, blueprint dimensions; it may NOT be a bare '*' in five "
    "languages, which is the palette-swap failure at one glyph")

C_TEXTAREA = Cand(
    "the multi-line notes field",
    "evoked", "Kit.textarea",
    "Kit.textarea(self, lines: list[str], caret: tuple[int,int] | None, "
    "w: int, h: int, state: str = DEFAULT) -> list[str]",
    "the text field's contract over a RECTANGLE: the value comes back byte "
    "for byte, the caret takes a column of its own, and the window moves "
    "in two axes instead of one")

C_SELECT = Cand(
    "the closed select (its value and its disclosure mark)",
    "evoked", "Kit.select",
    "Kit.select(self, options, selected: int, w: int = 0, "
    "state: str = DEFAULT, open_: bool = False) -> str",
    "COMPONENTS.md census: 'the closed-state anatomy and the open overlay's "
    "frame'.  Distinct from `stepper`, which shows the two ways OFF a value; "
    "a select shows the one way INTO a list")

C_MENU = Cand(
    "the open select's list of options",
    "evoked", "Kit.menu",
    "Kit.menu(self, options, selected: int, w: int, "
    "state: str = DEFAULT) -> list[str]",
    "COMPONENTS.md names the context menu 'the biggest historical gap'.  "
    "The frame is the language's overlay answer, and a language that "
    "refuses overlays must say what it does instead")

C_DANGER = Cand(
    "the destructive action and the zone that holds it",
    "evoked", "Kit.button(..., danger=True)",
    "Kit.button(self, label, w=0, state=DEFAULT, danger: bool = False)",
    "severity on a CONTROL, which the contract has never had: it must read "
    "in greyscale (COMPONENTS.md 'severity by the language's reserved hues "
    "AND a glyph, never hue alone') -- and in ledger and corgi the reserved "
    "hue is already spent, so the mechanism cannot be the hue")

C_SCRIM = Cand(
    "the modal's frame and the treatment of the board behind it",
    "evoked", "Kit.overlay",
    "Kit.overlay(self, rows: list[str], w: int, h: int, "
    "under: list[str]) -> list[str]",
    "COMPONENTS.md 'dialog / sheet': frame weight and scrim idiom.  This is "
    "the one component where the five languages' answers are furthest "
    "apart, and three of them are refusals")

C_FIELDROW = Cand(
    "the detail pane's caption -> value rows",
    "evoked", "Kit.field_row",
    "Kit.field_row(self, caption: str, value: str, w: int, "
    "state: str = DEFAULT) -> str",
    "the definition-list row a detail pane, a KPI tile and a settings "
    "summary all are -- COMPONENTS.md's census lists the stat tile and has "
    "no row for this.  It is the single most reused shape in the six "
    "screens and the ONE the contract has no seat for, so all five "
    "languages are currently drawing LEDGER's mechanism (dot leaders): "
    "ledger's own answer generalised into four languages that never chose "
    "it, which is the palette-swap failure with a leader instead of a hue")

C_LOGROW = Cand(
    "the log row's level mark and its severity channel",
    "evoked", "Kit.log_row",
    "Kit.log_row(self, ts: str, level: str, msg: str, w: int) -> str",
    "`ICONS` has six domain kinds and no log level.  The level must read "
    "in greyscale on a glyph, and the alert hue is rationed -- ledger spends "
    "it only on debt, blueprint only on overdue, naught has one red total")

C_TAIL = Cand(
    "the tail marker (the streaming/held state of the log)",
    "evoked", "Kit.tail",
    "Kit.tail(self, held: bool) -> str",
    "an INDETERMINATE indicator, which COMPONENTS.md's state matrix says "
    "must be MOTION and never a frozen half-fill; `spinner(tick)` is the "
    "moving half and this is the held one")

C_MATCH = Cand(
    "the highlighted span of the query inside a result",
    "evoked", "Kit.match",
    "Kit.match(self, text: str, span: tuple[int, int], "
    "state: str = DEFAULT) -> str",
    "the CONTENT law (L-33 / inc12): the result's text comes back byte for "
    "byte and only its NOTATION is the language's -- so a language that "
    "upper-cases titles may not upper-case a match, and the emphasis may "
    "not be the accent alone")

C_HINT = Cand(
    "the key hints along the bottom",
    "evoked", "Kit.keyhint",
    "Kit.keyhint(self, pairs: list[tuple[str, str]], w: int) -> str",
    "inc12 §8.3: 'a mark that encodes a binding belongs to whoever owns the "
    "keymap.  Never the library.'  So the kit owns the NOTATION (corgi's "
    "brackets, ledger's leaders) and the caller supplies every key")


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
    det_hand: list[int] = []
    for line in k.sect("DETAIL", F.TASKS[F.SELECTED][0][:right - 14], right, 3):
        det.append(clip(line, right))
    for cap, val in F.DETAIL:
        room = right - len(cap) - len(val) - 2
        lead = k.LEAD if hasattr(k, "LEAD") else " "
        det.append(f"[{c['mut']}]{LG.mark(cap)}[/] "
                   f"[{c['dim']}]{LG.mark(lead * max(1, room))}[/] "
                   f"[{c['ink']}]{LG.mark(val)}[/]")
        det_hand.append(len(det))
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
    split = f"[{c['dim']}]│[/]"
    for i in range(room):
        l = clip(lst[i] if i < len(lst) else "", left)
        r = clip(det[i] if i < len(det) else "", right)
        cds = [C_SPLIT] + ([C_FIELDROW] if (i + 1) in det_hand else [])
        sh.row(pad(l, left) + " " + split + " " + r, *cds)
    sh.row(pad(f"[{c['dim']}]{LG.mark('view')}[/] " + bar
                + f" [{c['mut']}]{LG.mark(f'{st + 1}-{st + sz} of {tot}')}[/]",
                left))


def s1_blueprint(sh: Sheet) -> None:
    """Blueprint's S1, and the divider is a REFUSAL rather than a rule.

    The language's ten marks are `─ ━ ├ ┤ ╌ ┌ ┐ └ ┘` and the hatch; not one
    of them is a vertical stroke, so a `│` between two panes is not merely
    off-style here, it is unconstructable (LANGUAGES.md #11).  What a drawing
    office does instead is what this does: the second pane is a FIELD at its
    own datum, and the air between them is the division.
    """
    s1(sh)
    # the generic builder drew a `│`; blueprint's frame must not carry one.
    c = sh.k.c
    fixed = []
    for r in sh.rows:
        fixed.append(r.replace(f"[{c['dim']}]│[/]", f"[{c['dim']}] [/]"))
    sh.rows = fixed
    sh.cands.pop(C_SPLIT.name, None)
    sh.note(Cand(
        "the divider between the two panes -- NOT DRAWN",
        "refused", "pane_split",
        "Kit.pane_split(h: int) -> list[str]",
        "'not one element is boxed, at any width' -- the ten marks this "
        "language draws contain no vertical stroke, so a pane rule is "
        "unconstructable.  The division is AIR at a second datum, which is "
        "what a drawing office does with two views on one sheet"))


# ===========================================================================
# S2 -- FORM WITH VALIDATION
# ===========================================================================
def s2(sh: Sheet) -> None:
    k, c = sh.k, sh.k.c
    chrome(sh, "form")
    header(sh, "NEW TASK", "5 fields  ·  1 invalid")

    lab = 14
    req = f"[{c['alert']}]{LG.mark('*')}[/]"

    def field(caption: str, control: str, required: bool = False,
              *cands: Cand) -> None:
        cap = f"[{c['mut']}]{LG.mark(caption)}[/]"
        head = pad(cap + (req if required else " "), lab)
        sh.row("  " + head + control, *cands)

    # title -- textfield in EDITED, which is the kit's own caret state
    field("title", k.textfield(F.FORM_TITLE, F.FORM_TITLE_CARET, 34, EDITED),
          True, C_REQUIRED)
    sh.blank()

    # due -- the INVALID field.  There is no invalid state in the contract,
    # so the field is drawn in the nearest state the kit HAS and the mark and
    # the message beside it are drawn here and declared.
    bad = k.textfield(F.FORM_DUE_RAW, None, 34, DEFAULT)
    field("due", bad + " " + f"[{c['alert']}]{LG.mark('!')}[/]", True,
          C_REQUIRED, C_INVALID)
    sh.row(" " * (lab + 2) + f"[{c['alert']}]{LG.mark(F.FORM_DUE_ERROR)}[/]",
           C_INVALID)
    sh.blank()

    field("priority", k.radio_group(F.PRIORITIES, F.PRIORITY_SEL))
    sh.blank()

    tags = "  ".join(k.checkbox(on) + " " + f"[{c['mut']}]{LG.mark(t)}[/]"
                     for t, on in F.TAGS)
    field("tags", tags)
    sh.blank()

    # notes -- a rectangle of text the contract has no component for
    field("notes", "", False)
    sh.rows.pop()
    cap = pad(f"[{c['mut']}]{LG.mark('notes')}[/] ", lab)
    op, rune, cl = k.field_form(DEFAULT, "textfield")
    for i, line in enumerate(F.NOTES):
        head = cap if i == 0 else " " * lab
        sh.row("  " + head + f"[{c['dim']}]{LG.mark(op)}[/]"
               + f"[{c['ink']}]{LG.mark(pad(line, 34))}[/]"
               + f"[{c['dim']}]{LG.mark(cl)}[/]", C_TEXTAREA)
    sh.row("  " + " " * lab + f"[{c['dim']}]{LG.mark(op)}[/]"
           + f"[{c['dim']}]{LG.mark(rune * 34)}[/]"
           + f"[{c['dim']}]{LG.mark(cl)}[/]", C_TEXTAREA)
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

    # -- the two selects.  `stepper` is the nearest thing the contract has and
    # it is a DIFFERENT control: it shows the two ways off a value, not the
    # one way into a list.  Drawn as a stepper plus a disclosure mark, and
    # declared as evoked rather than passed off as implemented.
    for label, opts, sel, is_open in F.SELECTS:
        cap = f"[{c['mut']}]{LG.mark(label)}[/]"
        body = k.stepper(opts, sel, 7) + " " + f"[{c['mut']}]{LG.mark('v')}[/]"
        sh.row("  " + pad(cap, lab) + body, C_SELECT)
        if not is_open:
            continue
        for j, o in enumerate(opts):
            mk = k.CUR if j == sel else " "
            tone = c["ink"] if j == sel else c["mut"]
            sh.row("  " + " " * lab + f"[{c['dim']}]{LG.mark('  ')}[/]"
                   + f"[{tone}]{LG.mark(mk + ' ' + pad(o, 7))}[/]",
                   C_SELECT, C_MENU)
    sh.blank()

    sh.row("  " + pad(f"[{c['mut']}]{LG.mark(F.SLIDER_LABEL)}[/]", lab)
           + k.slider(F.SLIDER_VAL, 0, 100, 14))
    sh.blank()

    # -- the danger zone ----------------------------------------------------
    r = k.rule_line(W - 4)
    sh.row("  " + (r if r is not None else ""))
    sh.row("  " + f"[{c['alert']}]{LG.mark('DANGER')}[/]  "
           + f"[{c['mut']}]{LG.mark(F.DANGER_LABEL)}[/]", C_DANGER)
    sh.row("  " + k.button(F.DANGER_ACTION, 12, DEFAULT)
           + "   " + f"[{c['dim']}]{LG.mark('7 tasks, not recoverable')}[/]",
           C_DANGER)


def s3_ledger(sh: Sheet) -> None:
    """Ledger's settings, and the danger zone is where the GENRE answers.

    'Nothing is deleted, everything is balanced' (LANGUAGES.md #9) is a rule
    about the product, not about the palette -- so a button that destroys
    seven rows is not a control this language may draw at all.  What it draws
    instead is the entry that REVERSES them, which is what a ledger does when
    something must go away.
    """
    s3(sh)
    k, c = sh.k, sh.k.c
    # replace the two danger rows with the language's own answer
    sh.rows = sh.rows[:-2]
    sh.cands.pop(C_DANGER.name, None)
    sh.row("  " + f"[{c['ink']}]{LG.mark('CLOSING')}[/]  "
           + f"[{c['mut']}]{LG.mark('7 completed entries')}[/]")
    sh.row("  " + k.button("Post closing entry", 20, DEFAULT)
           + "   " + f"[{c['dim']}]{LG.mark('reverses, never deletes')}[/]")
    sh.note(Cand(
        "the destructive action -- NOT DRAWN",
        "refused", "Kit.button(..., danger=True)",
        "Kit.button(self, label, w=0, state=DEFAULT, danger: bool = False)",
        "'nothing is deleted, everything is balanced' rules out silent "
        "deletion as a DESIGN, so this language has no destructive control "
        "to style -- it has a closing entry.  And the red pen is literal "
        "debt: spending alert on a button would break the one thing that "
        "makes an overdue row legible"))


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
    """The default answer: a bordered dialog over a dimmed board.

    Only prism is entitled to this by its own commitment ('borders are
    reserved for modals'); the other four override below.
    """
    k, c = sh.k, sh.k.c
    under, back = _under(sh)
    dw, dh = 52, 9
    x = (W - dw) // 2
    y = 10

    box_t = "┌" + "─" * (dw - 2) + "┐"
    box_b = "└" + "─" * (dw - 2) + "┘"

    lines: list[str] = []
    lines.append(f"[{c['ink']}]{LG.mark(box_t)}[/]")
    lines.append(f"[{c['ink']}]{LG.mark('│')}[/]"
                 + f"[{c['ink']}]{LG.mark(' ' + pad(F.MODAL_TITLE, dw - 3))}[/]"
                 + f"[{c['ink']}]{LG.mark('│')}[/]")
    lines.append(f"[{c['ink']}]{LG.mark('│')}[/]"
                 + f"[{c['dim']}]{LG.mark(' ' * (dw - 2))}[/]"
                 + f"[{c['ink']}]{LG.mark('│')}[/]")
    for b in F.MODAL_BODY:
        lines.append(f"[{c['ink']}]{LG.mark('│')}[/]"
                     + f"[{c['mut']}]{LG.mark(' ' + pad(b, dw - 3))}[/]"
                     + f"[{c['ink']}]{LG.mark('│')}[/]")
    lines.append(f"[{c['ink']}]{LG.mark('│')}[/]"
                 + f"[{c['dim']}]{LG.mark(' ' * (dw - 2))}[/]"
                 + f"[{c['ink']}]{LG.mark('│')}[/]")
    btns = (k.button("Delete", 10, FOCUSED) + "   "
            + k.button("Cancel", 10, DEFAULT))
    lines.append(f"[{c['ink']}]{LG.mark('│')}[/]"
                 + pad(" " + btns, dw - 2)
                 + f"[{c['ink']}]{LG.mark('│')}[/]")
    lines.append(f"[{c['ink']}]{LG.mark(box_b)}[/]")

    # the board behind, DIMMED -- the one channel a text frame has for
    # "inactive" without a real compositor is tone, so every row is redrawn
    # in the dim tier.  That is the scrim, and it is declared.
    for i in range(H):
        base = under[i] if i < len(under) else ""
        if y <= i < y + len(lines):
            j = i - y
            sh.row(" " * x + lines[j], C_SCRIM)
        else:
            sh.row(f"[{c['dim']}]{LG.mark(vis(base))}[/]", C_SCRIM)


def s4_prism(sh: Sheet) -> None:
    """Prism is the one language whose commitment PERMITS this box.

    'Depth by ±1 grey step, never borders.  Borders are reserved for modals.'
    So the dialog is the single place a border is legal here, and the board
    behind it recedes by exactly one grey step of BACKGROUND rather than by
    being greyed out -- which is `depth_ground()`, a method the kit has.
    """
    k, c = sh.k, sh.k.c
    under, back = _under(sh)
    ground = k.depth_ground()
    dw = 52
    x = (W - dw) // 2
    y = 10

    lines = [f"[{c['ink']}]{LG.mark('┌' + '─' * (dw - 2) + '┐')}[/]",
             f"[{c['ink']}]{LG.mark('│ ' + pad(F.MODAL_TITLE, dw - 3))}│[/]",
             f"[{c['ink']}]{LG.mark('│' + ' ' * (dw - 2) + '│')}[/]"]
    for b in F.MODAL_BODY:
        lines.append(f"[{c['ink']}]{LG.mark('│')}[/]"
                     + f"[{c['mut']}]{LG.mark(' ' + pad(b, dw - 3))}[/]"
                     + f"[{c['ink']}]{LG.mark('│')}[/]")
    lines.append(f"[{c['ink']}]{LG.mark('│' + ' ' * (dw - 2) + '│')}[/]")
    lines.append(f"[{c['ink']}]{LG.mark('│')}[/]"
                 + pad(" " + k.button("Delete", 10, FOCUSED) + "   "
                       + k.button("Cancel", 10, DEFAULT), dw - 2)
                 + f"[{c['ink']}]{LG.mark('│')}[/]")
    lines.append(f"[{c['ink']}]{LG.mark('└' + '─' * (dw - 2) + '┘')}[/]")

    for i in range(H):
        base = under[i] if i < len(under) else ""
        if y <= i < y + len(lines):
            sh.row(" " * x + lines[i - y], C_SCRIM)
        else:
            # the recede is a BACKGROUND step, not a dimming of the ink
            sh.row(f"[{c['mut']} on {ground}]{LG.mark(pad(vis(base), W))}[/]")
    for cd in back:
        sh.note(cd)
    sh.note(Cand(
        "the modal's border and the board's ±1 grey step behind it",
        "evoked", "Kit.overlay",
        "Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]",
        "'depth by ±1 grey step, never borders -- borders are RESERVED for "
        "modals'.  This language is the only one of the five whose "
        "commitment licenses the box, and the recede is `depth_ground()`, "
        "which the kit already computes.  The primitive is missing; the "
        "MECHANISM is not"))


def s4_corgi(sh: Sheet) -> None:
    """Corgi refuses the overlay: 'the mode takes over the screen'.

    'No persistent navigation chrome.  Its answer to smallness is FEWER
    THINGS AT ONCE, not smaller things.'  A dialog floating over a board is
    two modes at once, which is the thing this language is built against --
    so a confirm is a MODE, numbered like every other, and the board is gone.
    """
    k, c = sh.k, sh.k.c
    chrome(sh, "board")
    header(sh, "CONFIRM", "MODE 5  ·  DESTRUCTIVE")
    sh.blank()
    for line in k.wordmark("DELETE")[:6]:
        sh.row("  " + line)
    sh.blank()
    sh.row("  " + f"[{c['ink']}]{LG.mark(str(F.MODAL_COUNT) + ' TASKS')}[/]  "
           + f"[{c['mut']}]{LG.mark('WILL BE REMOVED FROM BACKLOG')}[/]")
    sh.row("  " + f"[{c['mut']}]{LG.mark('THIS CANNOT BE UNDONE')}[/]")
    sh.blank()
    sh.row("  " + k.button("DELETE", 12, FOCUSED) + "   "
           + k.button("CANCEL", 12, DEFAULT))
    sh.blank()
    sh.row("  " + f"[{c['accent']}]{LG.mark('[1]')}[/] "
           + f"[{c['mut']}]{LG.mark('DELETE')}[/]   "
           + f"[{c['accent']}]{LG.mark('[2]')}[/] "
           + f"[{c['mut']}]{LG.mark('CANCEL')}[/]", C_HINT)
    sh.note(Cand(
        "the overlay and the dimmed board -- NOT DRAWN",
        "refused", "Kit.overlay",
        "Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]",
        "'the mode takes over the screen -- no persistent navigation "
        "chrome; its answer to smallness is fewer things at once'.  A "
        "dialog over a board is two modes at once.  The confirm is a MODE, "
        "and because the numbers ARE the keybindings (§3b) its two answers "
        "are numbered rather than trapped in a focus ring"))


def s4_naught(sh: Sheet) -> None:
    """Naught has NO FRAMES AT ALL -- so there is no box to draw.

    'Mono + one red · dense · no frames at all · everything on one dot
    lattice.'  What separates the question from the board is that the board's
    lattice goes UNLIT and the question's stays lit: the lattice is the
    scrim, which is the one structure device this language owns.
    """
    k, c = sh.k, sh.k.c
    under, back = _under(sh)

    # THE QUESTION IS A LIT BAND ON THE LATTICE.  The board keeps every dot
    # it had and loses only its CHARGE -- which is the whole mechanism: "the
    # unlit grid is visible; dark dots render in the dim tier rather than as
    # spaces.  That faint lattice IS the signature."  A box would be a frame,
    # and this language has none; what it has is a row that is lit and rows
    # that are not, and the lattice rule above and below the band is the
    # edge.  Drawn with `rule_line()`, which is naught's own lattice row.
    # the band edge: the lattice at FULL CHARGE.  `rule_line()` returns
    # None here (naught spends no rule), so the lit row is drawn and
    # declared rather than borrowed from a method that has no answer.
    lat = k.CUR * W
    band_y, band_h = 12, 9

    def unlit(i: int) -> str:
        base = vis(under[i]) if i < len(under) else ""
        return f"[{c['dim']}]{LG.mark(base)}[/]"

    for i in range(band_y):
        sh.row(unlit(i))

    lines: list[str] = [clip(f"[{c['ink']}]{lat}[/]", W)]
    sprite = k.wordmark(str(F.MODAL_COUNT))[:5]
    for j, line in enumerate(sprite):
        tail = ("   " + f"[{c['ink']}]{LG.mark('tasks will be deleted')}[/]"
                if j == 2 else "")
        lines.append("      " + line + tail)
    lines.append("      " + k.button("delete", 10, FOCUSED) + "   "
                 + k.button("cancel", 10, DEFAULT))
    lines.append(clip(f"[{c['ink']}]{lat}[/]", W))
    for l in lines[:band_h]:
        sh.row(l)

    for i in range(band_y + band_h, H):
        sh.row(unlit(i))
    sh.rows = sh.rows[:H]
    for cd in back:
        sh.note(cd)
    sh.note(Cand(
        "the modal's frame -- NOT DRAWN",
        "refused", "Kit.overlay",
        "Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]",
        "'no frames at all' is one of this language's four commitments, so "
        "an overlay BOX is unconstructable.  The separation is the lattice "
        "going unlit behind a lit question, and the count is a DRAWN sprite "
        "because a count is exactly what this language draws"))
    sh.note(Cand(
        "the inactive board, drawn as an unlit lattice",
        "evoked", "Kit.recede",
        "Kit.recede(self, rows: list[str]) -> list[str]",
        "'the unlit grid is visible -- dark dots render in the dim tier "
        "rather than as spaces.  That faint lattice IS the signature.'  So "
        "this language's scrim is the one it was already drawing"))


def s4_blueprint(sh: Sheet) -> None:
    """Blueprint cannot box the dialog either -- and its emphasis is a
    KNOCKOUT, which is exactly one element per sheet.

    So the dialog is a REVISION NOTE on the sheet: registration marks around
    what is selected (the language's own selection mechanism, four corners
    that never join), the question as a field, and the knockout spent on the
    default answer instead of on the title block's STATE cell -- which is the
    one place a sheet's single knockout is allowed to move.
    """
    k, c = sh.k, sh.k.c
    chrome(sh, "board")            # deferred: the stamp docks at the bottom
    under, back = _under(sh)
    y, dh = 11, 8
    keep = [vis(under[i]) if i < len(under) else "" for i in range(H)]
    for i in range(y):
        sh.row(f"[{c['dim']}]{LG.mark(keep[i])}[/]")
    # THE FOUR CORNERS NEVER JOIN.  The first sweep ran a `─` between them,
    # which makes a box lid however this language spells it -- and "not one
    # element on this sheet is boxed, AT ANY WIDTH" is the commitment being
    # tested.  `tabs()` shows the shipped form: `┌   ┐` above, `└   ┘`
    # below, with air where a stroke would be.  This registers the same way.
    x, span = 22, 54
    reg = (f"[{c['ink']}]{LG.mark('┌')}[/]" + " " * (span - 2)
           + f"[{c['ink']}]{LG.mark('┐')}[/]")
    reg_b = (f"[{c['ink']}]{LG.mark('└')}[/]" + " " * (span - 2)
             + f"[{c['ink']}]{LG.mark('┘')}[/]")
    sh.row(" " * x + reg)
    sh.row(" " * x + f"[{c['ink']}]{LG.mark(' REVISION  ' + F.MODAL_TITLE.upper())}[/]")
    sh.row(" " * x + f"[{c['mut']}]{LG.mark(' ·── ' + F.MODAL_BODY[0].upper())}[/]")
    sh.row(" " * x + f"[{c['mut']}]{LG.mark(' ·── ' + F.MODAL_BODY[1].upper())}[/]")
    sh.row("")
    ko = (f"[{k.t.get('ground', '#0d2b45')} on {c['ink']}]"
          f"{LG.mark(' DELETE ')}[/]")
    sh.row(" " * x + " " + ko + "   "
           + k.button("CANCEL", 8, DEFAULT), C_SCRIM)
    sh.row(" " * x + reg_b)
    for i in range(y + dh, H):
        sh.row(f"[{c['dim']}]{LG.mark(keep[i])}[/]")
    for cd in back:
        sh.note(cd)
    sh.note(Cand(
        "the modal's box -- NOT DRAWN; registration marks instead",
        "refused", "Kit.overlay",
        "Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]",
        "'not one element on this sheet is boxed' and the ten marks contain "
        "no vertical stroke and no rectangle junction, so a dialog box is "
        "unconstructable.  What marks the selection is the REGISTRATION "
        "PAIR (`┌ ┐` above, `└ ┘` below -- four corners that never join), "
        "which is this language's selection mechanism already"))
    sh.note(Cand(
        "the knockout on the default answer",
        "evoked", "Kit.knockout_cell",
        "Kit.knockout_cell(self, text: str) -> str",
        "'exactly ONE element per view reverses to a pale ground with dark "
        "ink, and it is the hero.'  On a board that cell is the title "
        "block's STATE; on a confirm the hero is the answer, so the "
        "knockout MOVES -- and the sheet must still carry exactly one"))


def s4_ledger(sh: Sheet) -> None:
    """Ledger refuses the QUESTION, not just the frame.

    'Nothing is deleted, everything is balanced' (LANGUAGES.md #9) rules out
    silent deletion as a design.  So 'delete 3 tasks?' is not a dialog this
    language can render honestly -- what it renders is the REVERSING ENTRY
    the genre requires, posted in the same ruled columns as everything else,
    with the folio and the leaders it always has.
    """
    k, c = sh.k, sh.k.c
    chrome(sh, "board")
    header(sh, "CLOSING ENTRY", "3 postings to reverse")
    sh.blank()
    for i, t in enumerate(F.TASKS[:3]):
        sh.row("  " + k.card_rows(t[0], "rev", c["alert"], W - 6, i, False,
                                  meta_of(t))[0])
    sh.blank()
    r = k.rule_line(W - 4)
    sh.row("  " + (r if r is not None else ""))
    sh.row("  " + f"[{c['ink']}]{LG.mark('3 entries reversed, 0 deleted')}[/]")
    sh.blank()
    sh.row("  " + k.button("Post reversal", 16, FOCUSED) + "   "
           + k.button("Cancel", 16, DEFAULT))
    sh.note(Cand(
        "the delete dialog -- REFUSED AT THE CONTENT, not the frame",
        "refused", "Kit.overlay",
        "Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]",
        "'nothing is deleted, everything is balanced' -- the genre rules "
        "out silent deletion as a design (LANGUAGES.md #9, 'what the genre "
        "obligates').  A confirm-to-destroy is therefore not a dialog this "
        "language may style; the honest screen is the reversing entry, and "
        "it is a PAGE rather than an overlay because a ledger has no "
        "surface in front of the page"))


# ===========================================================================
# S5 -- LIVE MONITOR / LOG
# ===========================================================================
LEVEL_MARK = {"info": " ", "warn": "!", "error": "!!"}


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

    # -- the log ------------------------------------------------------------
    for ts, lvl, msg in F.LOG:
        tone = (c["alert"] if lvl == "error"
                else c["warn"] if lvl == "warn" else c["mut"])
        mkr = LEVEL_MARK[lvl]
        sh.row("  " + f"[{c['dim']}]{LG.mark(ts)}[/] "
               + f"[{tone}]{LG.mark(pad(mkr, 3))}[/]"
               + f"[{c['dim'] if lvl == 'info' else tone}]"
               f"{LG.mark(lvl.upper()[:5].ljust(6))}[/]"
               + f"[{c['ink'] if lvl != 'info' else c['mut']}]"
               f"{LG.mark(msg)}[/]", C_LOGROW)

    # -- the tail marker ----------------------------------------------------
    held = f"[{c['warn']}]{LG.mark('|| HELD')}[/]" if F.PAUSED else \
        k.spinner(2) + f" [{c['mut']}]{LG.mark('live')}[/]"
    sh.row("  " + f"[{c['dim']}]{LG.mark('        ')}[/]" + held
           + f"  [{c['dim']}]{LG.mark('space resumes')}[/]", C_TAIL)


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

    for i, (label, span, hint) in enumerate(F.RESULTS):
        sel = i == F.RESULT_SEL
        cur = f"[{c['accent']}]{k.CUR}[/] " if sel else "  "
        a, b = span
        pre, mid, post = label[:a], label[a:b], label[b:]
        tone = c["ink"] if sel else c["mut"]
        body = (f"[{tone}]{LG.mark(pre)}[/]"
                f"[{c['accent']}]{LG.mark(mid)}[/]"
                f"[{tone}]{LG.mark(post)}[/]")
        keyc = (f"[{c['dim']}]{LG.mark(hint)}[/]" if hint else "")
        sh.row("  " + cur + pad(body, 44) + keyc, C_MATCH)
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

    hints = "   ".join(f"[{c['accent']}]{LG.mark(kk)}[/] "
                       f"[{c['dim']}]{LG.mark(vv)}[/]" for kk, vv in F.HINTS)
    sh.row("  " + hints, C_HINT)


def s6_corgi(sh: Sheet) -> None:
    """Corgi's key hints are the one place its numbering is already the
    mechanism -- '[1] BOARD [2] LOG' IS the hint row.  So the hints are
    IMPLEMENTED here and evoked everywhere else."""
    s6(sh)
    sh.cands.pop(C_HINT.name, None)
    k, c = sh.k, sh.k.c
    sh.rows[-1] = "  " + "   ".join(
        f"[{c['accent']}]{LG.mark('[' + str(i + 1) + ']')}[/] "
        f"[{c['mut']}]{LG.mark(vv.upper())}[/]"
        for i, (kk, vv) in enumerate(F.HINTS))
    sh.note(Cand(
        "the key hint row",
        "evoked", "Kit.keyhint",
        "Kit.keyhint(self, pairs: list[tuple[str, str]], w: int) -> str",
        "§3b: 'in a TUI the numbers ARE the keybindings, which makes the "
        "numbering functional rather than decorative.'  This language "
        "already HAS the notation -- what is missing is the seat, and the "
        "caller must still supply every key (inc12 §8.3)"))


# ===========================================================================
# the dispatch table -- per-language overrides, named rather than guessed
# ===========================================================================
BUILDERS = {
    "S1": {"blueprint": s1_blueprint},
    "S2": {},
    "S3": {"ledger": s3_ledger},
    "S4": {"prism": s4_prism, "corgi": s4_corgi, "naught": s4_naught,
           "blueprint": s4_blueprint, "ledger": s4_ledger},
    "S5": {},
    "S6": {"corgi": s6_corgi},
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
