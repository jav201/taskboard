"""collision_census.py -- which CELL in each language does more than one job.

    python -X utf8 prototypes/collision_census.py [-o OUT]

WHAT THIS IS FOR.  `PROTOTYPE-inheritors.md` judged 42 frames and left sixteen
`rework` findings that are one language's own declaration (`spec.md` §9.4).
Read one at a time they are sixteen taste arguments.  Read together, most of
them are the SAME defect: a language has a small alphabet, spends one glyph on
severity or obligation, and then spends the same glyph on a control's chrome --
so a reader who has learned "this mark means error" meets it opening a button.

The round found five of those by hand.  A census is the version that cannot
miss the sixth, and it is a census of DECLARATIONS rather than of frames: a
collision exists in the kit whether or not the two roles happen to land in the
same 118x34 photograph.

THE TWO SETS, and they are the operator's own words.

  A -- SEVERITY AND OBLIGATION.  `LEVELS[*]`, `DANGER_FORM`, `REQUIRED`, the
       `invalid` mark of every glyph table, and the cursor `CUR`.  These are
       the marks that MEAN something about the state of the work: how bad it
       is, whether it is compulsory, whether it was rejected, where you are.

  B -- CONTROL CHROME.  Every `PART_GLYPHS` slot the registry can reach for
       button, checkbox, radio, switch, textfield and stepper, resolved
       through `Kit.part_glyph` in EVERY state `component_states` derives --
       so the chrome a language actually draws, not the table it happens to
       have typed.  SINCE inc57 IT ALSO READS TWO DECLARED CONSTANTS THAT ARE
       NOT IN `PART_GLYPHS` -- `FIELD_LEAD` (the cells a language's definition
       row leads with) and `IDENT_GLYPHS` (the marks its identity draws).
       Both were literals inside methods until then, which is why `spec.md`
       §13.8 could write "`field_row` is drawn outside `PART_GLYPHS` in all
       eleven, so the census can reach none of the eleven field leaders" and
       §12.7 could write the same of darkside's `(O)` tab.  A mark a language
       DRAWS and this file cannot SEE is this census's own blind spot, and the
       fix is a declaration rather than a bigger reader.

WHAT A CHANNEL IS (ruling D, orchestrator, 2026-09-06, on the operator's
delegation).  Every "these two are told apart by X" argument in this corpus
has to name X, and X may be one of FOUR things:

    COUNT      how many marks -- `◎ ◉` against `· o O`, two concentric
               strokes against one.
    WEIGHT     how much ink one mark spends -- `O` against `▊`.
    POSITION   where the mark stands -- a caret inside a value against chrome
               at an opener.
    DIRECTION  which way it points -- `▪` against `▶`.

DIAMETER ALONE IS NOT A CHANNEL.  Two drawings that differ only in HOW BIG
they are read as one mark at a 12px cell, so `• / ●` is one bullet and
`o / ◦` is one ring.  A language may not tell a MEANING apart from its CHROME
that way.  The pairs this census treats as one drawing are `HOMOGLYPHS`
below, and the moves accepted under the ruling are named there too.

WHAT COUNTS AS A COLLISION, stated so it can be argued with.  A cell collides
when it carries roles from two or more A-families, OR from at least one
A-family and at least one B-family.  A cell ALSO collides through its
HOMOGLYPH -- listed in its own section at the foot of the report and NEVER
folded into the per-language count, because a homoglyph row is a question
about two drawings and the count is a question about one cell.

  * A x B is the operator's question verbatim: instrument's `⠇` is the ERROR
    rung and the opener of a SAFE button.
  * A x A is included because three of the five the round found by hand are
    that shape and would otherwise be missed: swiss's `━` is the cursor AND
    `LEVELS["error"]`; nord's `!` is `warn` AND `DANGER_FORM`.  Two meanings
    is two meanings whether or not a control is involved.
  * B x B is NOT counted, and that is a decision rather than an oversight.  A
    language has an ALPHABET; a button and a text field sharing a wall form is
    how a language reads as one language.  The count of B x B cells is printed
    at the foot of each language so the choice stays visible and can be
    reversed by whoever disagrees.

SELECT AND TEXTAREA DECLARE NO PART TABLE.  `COMPONENT_PARTS` has nine entries
and neither is among them: `Kit.select` (inc16) and `Kit.textarea` (inc30)
COMPOSE from the textfield's slots plus their own literals.  Their chrome
therefore reaches this census through `textfield`, and any mark of their own is
outside it.  Named because the request listed them.

SLIDER, BAR AND SCROLLBAR ARE IN THE B SET SINCE inc67, and the number this
docstring used to print instead ("how many further cells would collide if they
were in") was the whole of `PROTOTYPE-inheritors-3.md`'s K5.  They were out by
the operator's own request, which named six controls; the round found three of
its eight new `rework` verdicts living exactly in the excluded widget, and the
orchestrator's RULING A, AMENDED (2026-09-07) puts them back:

    "the census's B set reaches every quantity widget: slider, bar,
     scrollbar, meter, sparkline, pager, mascot.  Their fill and track cells
     are chrome; a fill cell may not be a meaning mark of its language."

FOUR OF THE SEVEN WERE ALREADY DECLARED and only the reader excluded them --
the slider, the bar and the scroll bar are `COMPONENT_PARTS` entries, and the
PAGER IS THE SCROLL BAR (`screens.s1` calls `k.scrollbar`, so `corgi_S1`'s
`view ██ ░░ ░░ ░░` and `scrollbar.indicator` are one declaration seen twice).
The other three -- the METER, the SPARKLINE and the MASCOT -- are drawn
outside `PART_GLYPHS` in all eleven, so they are DECLARED, at
`Kit.quantity_glyphs()`, and read here exactly as `FIELD_LEAD` and
`IDENT_GLYPHS` have been read since inc57.  A mark a language draws and this
file cannot see is this census's own blind spot; the fix is a declaration
rather than a bigger reader, for the third time.

THIS FIXES NOTHING.  It is the input to the language-level rework, and a cell
appearing here is a question ("did you mean these two to be the same mark?"),
not a verdict.  Several are certainly deliberate.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from taskboard import language as LG                              # noqa: E402

#: not a cell: the ASCII space and U+2800 BRAILLE PATTERN BLANK. The second is
#: an EMPTY braille cell -- instrument and prism pad with it -- and a language
#: that pads two roles with the same nothing has not overloaded anything.
BLANKS = " ⠀"

#: THE NINE, since inc67. The six the request named plus the three quantity
#: widgets ruling A amended puts back in set B. `OTHERS` is empty and kept so
#: the shape of the old boundary stays legible in the diff and so a future
#: exclusion has a seat to sit in rather than being spelled into `CONTROLS`.
CONTROLS = ("button", "checkbox", "radio", "switch", "textfield", "stepper",
            "slider", "bar", "scrollbar")
OTHERS: tuple[str, ...] = ()

#: MARKS A KIT DECLARES OUTSIDE `PART_GLYPHS` (inc57), as
#: `(family, attribute, seat)`. They are B-families -- a leader and a doodle
#: are chrome, not meanings -- so they collide against A and never against
#: each other, exactly like a control's wall.
#:
#: `FIELD_LEAD` is a STRING of the cells the definition row leads with (`""`
#: for the four languages whose answer is air, which is a commitment and not
#: a hole); `IDENT_GLYPHS` is a TUPLE of glyphs, because a moon phase and a
#: tab mark are drawings with handedness and joining them would invent an
#: order that is not there.
#:
#: inc67 ADDS THE THIRD, and it is the same kind of thing for the third time:
#: `PANE_RULE` is the cell a language rules the gap between two panes with,
#: declared on the kit since inc28 and read by nothing but the drawing. It is
#: not a quantity widget and ruling A does not name it -- it is here because
#: `corgi_S1` spent `█`, that kit's error rung and danger form, TWENTY-FIVE
#: rows tall on it, and a fix nothing measures is a fix that can silently
#: come back.
DECLARED_MARKS = (("field", "FIELD_LEAD", "field.leader"),
                  ("identity", "IDENT_GLYPHS", "identity.mark"),
                  ("pane", "PANE_RULE", "pane.rule"))

#: the A-families. One per KIND of meaning, not one per declaration -- two
#: severity rungs sharing a cell is a severity problem, not a collision.
A_FAMILIES = ("severity", "danger", "required", "invalid", "cursor")

#: THE FAMILIES A CELL CAN BELONG TO — ruling D AMENDED (orchestrator,
#: 2026-09-07, on the operator's delegation):
#:
#:     "the homoglyph list is derived, not enumerated: two cells are
#:      homoglyphs when they are the same base shape at a different size or
#:      fill (ring/disc, dot sizes, dash counts within a family), and the
#:      named four join it now: naught `⊙`/`◉` and `○`/`◦`, ledger `†`/`‡`,
#:      blueprint `╌ ┄ ┈`."
#:
#: WHAT REPLACED WHAT. Until inc68 this was a FIXED LIST OF FIVE PAIRS, and
#: `PROTOTYPE-inheritors-3.md` §0d is the objection in one line: the four
#: TIGHTEST pairs in the corpus were not in it, so the instrument that
#: enforces ruling D could only ever enforce it against the pairs somebody
#: had already noticed. A ruling that binds only against the pairs somebody
#: wrote down is not a ruling about SHAPE; it is a list of exceptions read
#: backwards.
#:
#: EACH ROW IS ONE BASE SHAPE, written in its own order of size and fill, and
#: a homoglyph is ANY TWO MEMBERS of one row. That is the amendment's own
#: word ("a different size OR fill") and it reverses inc53's "adjacent sizes
#: only", which was decided when this table was five hand-picked pairs. The
#: cost is published rather than hidden: the roster goes from 1 row to 33 and
#: `HOMOGLYPH_ROSTER` says what every one of them is.
#:
#: TRIANGLES ARE NOT A FAMILY, and that is the ruling's other half. `▶ ▼ ▸`
#: differ by DIRECTION, and the D-addendum (inc55) says direction is a
#: channel wherever a language already spends it: *"Rotation counts as a
#: channel when it is direction the language already spends (opener/closer,
#: up/down), not otherwise."* industrial's `CUR ▶` against its `DISCLOSE ▼`
#: is the case that settled it, and it stays settled.
HOMOGLYPH_FAMILIES = (
    "⋅·∙•●",       # the round FILLED mark: dot operator, middle dot,
                        # bullet operator, bullet, black circle
    "◦o○◎◉⊙⊛O",    # the round HOLLOW mark and what stands inside it:
                        # white bullet, letter o, white circle, bullseye,
                        # fisheye, circled dot, circled asterisk, letter O
    "▫□▪■",          # the SQUARE, hollow and filled, small and full
    "†‡",              # the reference mark and the same mark with a second bar
    "╌┄┈",             # one BROKEN horizontal at two, three and four dashes
)

#: derived, so a family gains a member in ONE place. Both orders of each pair
#: are read by `homoglyph_rows`, so the tuple order here carries no meaning
#: beyond the family's own size/fill order.
HOMOGLYPHS = tuple((a, b) for fam in HOMOGLYPH_FAMILIES
                   for i, a in enumerate(fam) for b in fam[i + 1:])


def _cells(glyph: str) -> list[tuple[str, str]]:
    """`(cell, position)` for each non-blank cell of a declared glyph.

    POSITION IS PART OF THE ROLE and the round's own phrasing says why: the
    finding is not "instrument spends `⠇` on a button", it is that `⠇` is the
    button's OPENER -- the first thing the eye reaches, where an error rung
    has no business being. A one-cell glyph has no handedness and is a mark."""
    if not glyph:
        return []
    n = len(glyph)
    out = []
    for i, ch in enumerate(glyph):
        if ch in BLANKS:
            continue
        pos = "mark" if n == 1 else ("open" if i == 0
                                     else "close" if i == n - 1 else "mid")
        out.append((ch, pos))
    return out


def role_map(lang: str) -> tuple[dict[str, dict[str, set[str]]], dict[str, dict[str, set[str]]]]:
    """cell -> family -> {role phrases}, for the named controls and for the rest.

    Everything is read through the kit's own resolvers -- `part_glyph` walks
    the state chain, so a state a language does not declare is credited to the
    glyph it actually falls back to. What is censused is what gets DRAWN."""
    k = LG.kit(lang)
    named: dict[str, dict[str, set[str]]] = {}
    other: dict[str, dict[str, set[str]]] = {}

    def add(bag, cell, family, phrase):
        bag.setdefault(cell, {}).setdefault(family, set()).add(phrase)

    # ---- A: severity and obligation ------------------------------------
    for level, glyph in k.LEVELS.items():
        for cell, _pos in _cells(glyph):
            add(named, cell, "severity", f"LEVELS[{level}]")
    for side, glyph in zip(("open", "close"), k.DANGER_FORM):
        for cell, _pos in _cells(glyph):
            add(named, cell, "danger", f"DANGER_FORM {side}")
    for cell, _pos in _cells(k.REQUIRED):
        add(named, cell, "required", "REQUIRED")
    for cell, _pos in _cells(k.CUR):
        add(named, cell, "cursor", "CUR")

    # ---- A and B: the glyph tables, state by state ----------------------
    for comp in CONTROLS + OTHERS:
        bag = named if comp in CONTROLS else other
        for part in LG.COMPONENT_PARTS[comp]:
            table = k.PART_GLYPHS[k.part_key(comp, part)]
            for state in LG.component_states(comp):
                if state == "invalid" and "invalid" not in table:
                    # A FALLBACK IS NOT A DECLARATION, and this line is the
                    # difference between a census and a pile. `part_glyph`
                    # walks the state chain, so a part with no `invalid` key
                    # returns its DEFAULT glyph -- and crediting that to the
                    # `INVALID` family made every language's caret "collide
                    # with itself" and every stepper track a rejection mark.
                    # Nine spurious rows in the first run, all of them the
                    # same artefact. A language that says nothing about
                    # invalid for a part has not overloaded anything there.
                    continue
                glyph = k.part_glyph(part, state, comp)
                for cell, pos in _cells(glyph):
                    if state == "invalid":
                        # a DECLARED `invalid` slot is a REJECTION MARK before
                        # it is chrome -- the `INVALID` the request asked for --
                        # so it lives in A, and a field whose invalid wall is
                        # also its default wall shows up here instead of
                        # cancelling itself out inside one family.
                        add(bag, cell, "invalid", f"INVALID {comp}.{part} {pos}")
                    else:
                        add(bag, cell, comp, f"{comp}.{part} {pos} [{state}]")

    # ---- B: the marks declared OUTSIDE the glyph tables (inc57) ---------
    for family, attr, seat in DECLARED_MARKS:
        declared = getattr(k, attr)
        glyphs = (declared,) if isinstance(declared, str) else tuple(declared)
        for glyph in glyphs:
            for cell, pos in _cells(glyph):
                add(named, cell, family, f"{seat} {pos} [declared]")

    # ---- B: the quantity widgets drawn outside `PART_GLYPHS` (inc67) ----
    #
    # ONE FAMILY FOR ALL THREE SEATS, and that is the same decision the six
    # controls get one family each: a meter, a spark and a mascot are one
    # language's QUANTITY VOCABULARY, and splitting them would let a cell
    # spent on the meter's fill and on the spark's peak read as a collision
    # when it is the ramp doing its job in two places. The SEAT is still in
    # the phrase, so a row says which of the three it came from.
    for seat, glyph in k.quantity_glyphs().items():
        for cell, pos in _cells(glyph):
            add(named, cell, "quantity", f"{seat} {pos} [declared]")
    return named, other


def homoglyph_rows(lang: str) -> list[tuple]:
    """`(cell, [A-families], its homoglyph, [B-families])` for every pair in
    `HOMOGLYPHS` where ONE side carries a meaning and the OTHER carries a
    control's chrome.

    MEANING x CHROME, AND SINCE inc68 MEANING x MEANING TOO. The old
    asymmetry came from the ruling's phrasing ("flags a meaning mark whose
    homoglyph is chrome") and it had a hole the amendment names by name.
    This function said that two meanings which are one drawing were "a
    severity/obligation question this file already asks of the cell itself";
    that is TRUE OF ONE CELL AND FALSE OF TWO. `Ledger.REQUIRED` is `†` and
    its INVALID mark is `‡` -- one drawing with a second bar, three cells
    apart on row 6 of `ledger_S2`, which `PROTOTYPE-inheritors-3.md` §2.11
    calls the tightest pair in the corpus -- and because BOTH sides are
    meanings this file read ZERO for ledger through three rounds. Ruling D
    amended names that pair as one that must join, so the clause is widened
    rather than the pair being written into a list.

    A LADDER IS NOT A ROW, by name and with its citation. The D-addendum
    (inc55) rules: *"A ladder is one meaning at monotone intensities and is
    one declaration: industrial's severity `▫▫ ▪▪ ■■` passes from hollow to
    filled (weight) and grows (size) in the same direction, so it stands."*
    So two cells that are BOTH rungs of this kit's own `LEVELS` are one
    declaration seen twice and are skipped -- industrial's three squares and
    darkside's `o`/`O`, four rows in all. Every other meaning x meaning pair
    is a row.

    CHROME x CHROME IS STILL NOT A ROW: two chrome cells that are one drawing
    are an ALPHABET, exactly as B x B is. Both directions of each pair are
    read, so it does not matter which of the two the kit declared first."""
    named, _ = role_map(lang)
    rungs = {ch for g in LG.kit(lang).LEVELS.values() for ch in g
             if ch not in BLANKS}
    out = []
    for a, b in HOMOGLYPHS:
        fa, fb = named.get(a), named.get(b)
        if not fa or not fb:
            continue
        aa = sorted(f for f in fa if f in A_FAMILIES)
        ab = sorted(f for f in fb if f in A_FAMILIES)
        if aa and ab:
            if {a, b} <= rungs:      # one ladder, one declaration (inc55)
                continue
            out.append((a, aa, b, ab))
            continue
        for x, y, ax in ((a, b, aa), (b, a, ab)):
            if not ax:
                continue
            bv = sorted(f for f in named[y] if f not in A_FAMILIES)
            if bv:
                out.append((x, ax, y, bv))
    return out


def collides(fams: dict[str, set[str]]) -> bool:
    """Two A-families, or one A-family and one B-family. Never B x B."""
    a = [f for f in fams if f in A_FAMILIES]
    b = [f for f in fams if f not in A_FAMILIES]
    return len(a) >= 2 or (len(a) >= 1 and len(b) >= 1)


def _phrase(fams: dict[str, set[str]]) -> str:
    """The roles, A-families first, states collapsed so a row stays readable."""
    order = sorted(fams, key=lambda f: (f not in A_FAMILIES,
                                        A_FAMILIES.index(f)
                                        if f in A_FAMILIES else 0, f))
    out = []
    for fam in order:
        seats = sorted(fams[fam])
        if fam in A_FAMILIES:
            out.append(" + ".join(seats))
            continue
        # collapse `comp.part pos [state]` into one seat with its state list
        by_seat: dict[str, list[str]] = {}
        for s in seats:
            head, _, st = s.partition(" [")
            by_seat.setdefault(head, []).append(st.rstrip("]"))
        for head, sts in sorted(by_seat.items()):
            out.append(f"{head} ({','.join(sorted(sts))})")
    return "  ·  ".join(out)


def report() -> list[str]:
    out: list[str] = []
    w = out.append
    w("COLLISION CENSUS — one cell, more than one job")
    w("=" * 78)
    w("")
    w("A cell is listed when it carries roles from two or more A-families")
    w("(severity, danger, required, invalid, cursor), or from an A-family and a")
    w("control's chrome. Chrome-only sharing between two controls is a")
    w("language's alphabet and is counted but not listed. Read the module")
    w("docstring of prototypes/collision_census.py for the argument.")
    w("")

    counts: dict[str, int] = {}
    clean: list[str] = []
    for lang in LG.KITS:
        named, other = role_map(lang)
        hits = {c: f for c, f in named.items() if collides(f)}
        counts[lang] = len(hits)
        also = sum(1 for c, f in other.items()
                   if c in named and collides({**named[c], **f})
                   and not collides(named[c]))
        bxb = sum(1 for c, f in named.items()
                  if not collides(f) and len([x for x in f
                                              if x not in A_FAMILIES]) >= 2)
        w("-" * 78)
        k = LG.kit(lang)
        w(f"{lang.upper()}   {len(hits)} colliding cells"
          f"   (LEVELS {'/'.join(k.LEVELS.values())}"
          f"  DANGER {''.join(k.DANGER_FORM)}"
          f"  REQUIRED {k.REQUIRED}  CUR {k.CUR})")
        w("-" * 78)
        if not hits:
            w("  no cell carries two roles.")
            clean.append(lang)
        for cell in sorted(hits, key=lambda c: (-len(hits[c]), c)):
            fams = hits[cell]
            w(f"  {cell}   [{len(fams)} families]  {_phrase(fams)}")
        w(f"  ... {bxb} further cells are shared between two CONTROLS only "
          f"(alphabet, not counted)")
        if OTHERS:
            w(f"  ... {also} further cells would collide if "
              f"{'/'.join(OTHERS)} were in the B set")
        else:
            w(f"  ... slider, bar, scrollbar, meter, spark and mascot are IN "
              f"the B set (inc67, ruling A amended)")
        w("")

    w("=" * 78)
    w("LANGUAGE x COLLISIONS")
    w("=" * 78)
    w(f"{'language':<14}{'colliding cells':>16}")
    for lang in LG.KITS:
        w(f"{lang:<14}{counts[lang]:>16}")
    w("-" * 30)
    w(f"{'TOTAL':<14}{sum(counts.values()):>16}")
    w("")
    answer = ", ".join(clean) if clean else         "NONE -- all eleven overload at least one cell"
    w(f"zero collisions: {answer}")
    w("")

    w("=" * 78)
    w("HOMOGLYPHS — one drawing at another size or fill (ruling D amended)")
    w("=" * 78)
    w("Ruling D (2026-09-06): a channel is COUNT, WEIGHT, POSITION or")
    w("DIRECTION. Diameter alone is none of them, so a language that tells a")
    w("MEANING apart from its own CHROME -- or from another MEANING -- by")
    w("size or fill alone has told them apart with nothing. Ruling D amended")
    w("(2026-09-07): the pairs are DERIVED from these families, any two")
    w("members of one row being one drawing. Triangles are NOT a family:")
    w("they differ by DIRECTION, which the D-addendum rules a channel.")
    for fam in HOMOGLYPH_FAMILIES:
        w("    " + " ".join(fam))
    w(f"    -> {len(HOMOGLYPHS)} pairs")
    w("These rows are NOT added to the counts above: a homoglyph row is a")
    w("question about two drawings, and the count is a question about one")
    w("cell.")
    w("")
    total = 0
    for lang in LG.KITS:
        rows = homoglyph_rows(lang)
        total += len(rows)
        if not rows:
            continue
        w(f"{lang.upper()}   {len(rows)} row(s)")
        for cell, av, twin, bv in rows:
            kind = ("MEANING" if all(f in A_FAMILIES for f in bv)
                    else "chrome")
            w(f"  {cell} is {' + '.join(av)}   and its homoglyph {twin} is "
              f"{' + '.join(bv)} {kind}")
    w("")
    w(f"{'TOTAL homoglyph rows':<30}{total:>4}")
    w("")
    w("This is the input to the language-level rework, not a verdict. A cell")
    w("here is the question 'did you mean these two to be the same mark?'.")
    return out


#: THE FIVE THE ROUND FOUND BY HAND, as
#: `(language, cell, {families}, closed_by)`. This script's whole claim is
#: that it cannot miss a sixth, and a census that had quietly stopped reading
#: `DANGER_FORM` would still print a confident table. So the five are asserted
#: before anything is reported -- the same bargain `verify_ink.py` makes with
#: its arithmetic self-check.
#:
#: `closed_by` IS THE ONLY WAY A ROW MAY LEAVE THIS ROSTER, and the reason is
#: that the roster is the instrument's teeth: deleting a line once the rework
#: fixes it would leave a census that can no longer prove it still sees
#: anything. So a fixed row STAYS, with the increment that fixed it, and the
#: assertion INVERTS -- the named families must no longer meet on that cell.
#: The check therefore fires in both directions: it goes red if the census
#: stops seeing a live collision AND if a language quietly grows a closed one
#: back.
FOUND_BY_HAND = (
    # STILL LIVE, AND ON PURPOSE (inc46 §1a). The rails mirrored, so `⠇` is
    # the CLOSER now rather than the opener the round photographed -- but the
    # LEFT braille column IS the severity ladder's column, so the only rail
    # that shares no cell with the ladder is the four-dot `⡇`, which is this
    # language's caret. The row stays; the defect at the opener is gone.
    ("instrument", "⠇", {"severity", "button"}, None),   # error rung, button rail
    ("instrument", "⠁", {"required", "switch"}, "inc46"),  # REQUIRED, switch DISABLED
    ("swiss", "━", {"cursor", "severity"}, "inc45"),     # cursor, error
    ("nord", "!", {"severity", "danger"}, "inc45"),      # warn, delete danger
    ("solari", "▁", {"required", "textfield"}, "inc47"),  # one of its nine roles
)


#: THE HOMOGLYPH ROSTER, per language, counted (inc53) — the same bargain the
#: test suite's rosters make: a number is a record only while somebody has to
#: edit it. A row here is NOT a defect; it is the question ruling D asks.
#:
#: inc68 REWROTE EVERY NUMBER IN IT, from 1 row to 30, and NOT ONE KIT GOT
#: WORSE. The table above stopped being five hand-picked pairs and became a
#: derivation over five families (ruling D amended), and `homoglyph_rows`
#: stopped skipping MEANING x MEANING. Both changes are the instrument
#: learning to see, which is the third time in this programme that a roster
#: has jumped because a reader was widened (inc49's knobs, inc67's quantity
#: widgets, this).
#:
#: THE THIRTY, GROUPED BY WHAT CAUSES THEM, because thirty rows read one at a
#: time are thirty taste arguments and grouped they are six facts:
#:
#:   6  THE INVALID RUNE, and this file already knows about it. `spec.md`
#:      §15.5 and §16.4 record the discrepancy by name: the CENSUS counts a
#:      field's paper rune as a rejection mark while the LAW does not
#:      (`_invalid_marks` has excluded the rune since inc52, reading the two
#:      WALLS and not the paper between them). Every one of these six is a
#:      `·` or `⋅` that is a field's paper standing against a filled disc at
#:      another size: corgi, ledger, solari, blueprint and naught (twice).
#:      **The day the census adopts the law's exclusion, all six go at once**
#:      — the same sentence §16.4 wrote about six COLLISION rows, now true of
#:      six homoglyph rows as well.
#:   5  NAUGHT'S GROUND. `◦` is `LEVELS["info"]` (`◦◦`, zero lit dots) and it
#:      is also this language's BLANK — `THE_GROUND_IS_NOT_A_MARK`, one
#:      language, one cell, granted by name in inc61 and priced at
#:      `GROUND_EXEMPTION_IS_WORTH = (7, 2)`. The two SEAT laws subtract it;
#:      this file does not, on the standing decision that a census asks
#:      questions and a law gives verdicts. So five rows are the ground
#:      standing against the rings drawn on it.
#:   4  NAUGHT'S OBLIGATION MARK, and this one is the ruling contradicting
#:      the round. `⊛` is a ring with an asterisk in it, and
#:      `PROTOTYPE-inheritors-3.md` §2.8 calls it the best obligation mark in
#:      the corpus BY NAME ("un asterisco dentro de un anillo no se parece a
#:      nada más en la pantalla"). Ruling D amended puts every ring in one
#:      family, so it is now a homoglyph of `○ ◎ ◉ ⊙`. Recorded exactly as it
#:      is: an instrument and a reader disagreeing, with both positions
#:      written down.
#:   8  DARKSIDE'S RING ALPHABET. `LEVELS` is `· / o / O` and inc49 moved
#:      every control to `◎ ◉` citing COUNT ("two concentric strokes against
#:      one") — a move this file's own docstring listed as ACCEPTED. Under
#:      the amendment a ring is a ring at any fill, so seven rows come back
#:      plus `▪`/`▫` at `REQUIRED` against the radio. Closing them means
#:      re-alphabeting darkside's controls off rings entirely, which is a
#:      language-level increment and not a census edit.
#:   4  ONE PAIR EACH, and each is a real reading:
#:        swiss      `·` (`LEVELS["info"]`) against `•` (`REQUIRED`) — two
#:                   MEANINGS, one filled disc at two sizes.
#:        nord       `·` (`LEVELS["info"]`) against `●` at the radio's knob.
#:        ledger     `†` (`REQUIRED`) against `‡` (INVALID) — **the tightest
#:                   pair in the corpus** (§2.11), one drawing with a second
#:                   bar, three cells apart on row 6 of `ledger_S2`, and
#:                   INVISIBLE to this file until inc68 widened it to
#:                   meaning x meaning. Ruling D amended names it.
#:        naught     `∙` (danger + error) against `●` (`CUR`).
#:   2  BLUEPRINT'S DASH LADDER. `╌` is `LEVELS["warn"]` and `┄`/`┈` are the
#:      dead runs inc60 built. Formally a COUNT channel and formally allowed
#:      by ruling D; the round's objection (§2.7) is that counting dashes in
#:      a 12px cell is not a channel a reader has. E2 — no font metric — is
#:      why it cannot be settled from the artefact.
#:   1  SOLARI, AND IT IS THIS FILE'S OWN FALSE POSITIVE. `LEVELS` here is
#:      three WORDS (`OK ` / `DLY` / `CNX`) and `_cells` splits a word into
#:      letters, so the `O` of `OK` is read as a severity MARK and matches
#:      the `◉` of a radio. A language whose ladder is words declares no
#:      severity cell at all. Named rather than special-cased: the fix is a
#:      reader change and it belongs to whoever rules on it.
#:
#: AND ONE ROW CLOSED, which is why naught reads 12 and not 15: `·` at
#: `scrollbar.main`. See `Naught.PART_GLYPHS` for the whole of it — inc61
#: retired that pixel and could not reach the one seat the census was told
#: not to read.
HOMOGLYPH_ROSTER = {"naught": 12, "corgi": 1, "instrument": 0, "swiss": 1,
                    "industrial": 0, "nord": 1, "darkside": 8, "prism": 0,
                    "ledger": 2, "solari": 2, "blueprint": 3}


def _self_check() -> None:
    for lang, want in HOMOGLYPH_ROSTER.items():
        got = homoglyph_rows(lang)
        assert len(got) == want, (f"HOMOGLYPH ROSTER: {lang} has {len(got)} "
                                  f"row(s), the roster says {want}: {got}")
    assert any(HOMOGLYPH_ROSTER.values()), (
        "HOMOGLYPH SELF-CHECK VACUOUS: the table finds nothing anywhere, so "
        "a broken pair list would look like a clean corpus")
    live = closed = 0
    for lang, cell, want, closed_by in FOUND_BY_HAND:
        named, _ = role_map(lang)
        fams = named.get(cell, {})
        if closed_by is None:
            live += 1
            assert collides(fams), f"CENSUS BROKEN: {lang} {cell} not a collision"
            missing = want - set(fams)
            assert not missing, (f"CENSUS BROKEN: {lang} {cell} lost role "
                                 f"families {sorted(missing)}; "
                                 f"has {sorted(fams)}")
            continue
        closed += 1
        assert not want <= set(fams), (
            f"REGRESSION: {lang} {cell} carries {sorted(want)} again -- "
            f"{closed_by} moved one of them off this cell")
    assert live, "SELF-CHECK VACUOUS: every roster row is marked closed"
    print(f"self-check  {live} of the {len(FOUND_BY_HAND)} collisions the round "
          f"found by hand still come back out of the census; {closed} are "
          "asserted CLOSED and cannot grow back")
    print(f"self-check  the homoglyph roster is exact for all eleven "
          f"({sum(HOMOGLYPH_ROSTER.values())} rows, "
          f"{sum(1 for v in HOMOGLYPH_ROSTER.values() if v)} languages)")


def main() -> int:
    _self_check()
    args = sys.argv[1:]
    dest = ROOT / "prototypes" / "out" / "collision_census.txt"
    if "-o" in args:
        dest = Path(args[args.index("-o") + 1])
    lines = report()
    text = "\n".join(lines) + "\n"
    print(text)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    print(f"  -> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
