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
       have typed.

WHAT COUNTS AS A COLLISION, stated so it can be argued with.  A cell collides
when it carries roles from two or more A-families, OR from at least one
A-family and at least one B-family.

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

SLIDER, BAR AND SCROLLBAR ARE OUT OF THE B SET by the same request, which named
six controls.  How many further cells would collide if they were in is printed
per language, so the boundary is a number rather than a silence.

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

#: the six the request named. `bar`, `slider` and `scrollbar` are measured too,
#: but only to print how much the boundary costs (see the module docstring).
CONTROLS = ("button", "checkbox", "radio", "switch", "textfield", "stepper")
OTHERS = ("slider", "bar", "scrollbar")

#: the A-families. One per KIND of meaning, not one per declaration -- two
#: severity rungs sharing a cell is a severity problem, not a collision.
A_FAMILIES = ("severity", "danger", "required", "invalid", "cursor")


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
    return named, other


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
        w(f"  ... {also} further cells would collide if slider/bar/scrollbar "
          f"were in the B set")
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
    ("instrument", "⠇", {"severity", "button"}, None),   # error rung, button opener
    ("instrument", "⠁", {"required", "switch"}, None),   # REQUIRED, switch DISABLED
    ("swiss", "━", {"cursor", "severity"}, "inc45"),     # cursor, error
    ("nord", "!", {"severity", "danger"}, "inc45"),      # warn, delete danger
    ("solari", "▁", {"required", "textfield"}, None),    # one of its nine roles
)


def _self_check() -> None:
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
