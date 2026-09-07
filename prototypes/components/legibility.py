"""legibility.py -- what the raster can be asked that the svg could not.

    python -X utf8 prototypes/components/legibility.py

    -> prototypes/out/legibility.txt

FOUR MEASURES, AND EACH ONE ANSWERS AN OBJECTION THAT HAS BEEN OPEN FOR
ROUNDS.  The `.svg` carries `fill=` and a nominal box no font agreed to, so
every legibility question about this corpus has so far been answered with a
contrast ratio -- and round four wrote down exactly why that is not an answer
(§8.2): *"un ratio de contraste no es una prueba de legibilidad ... `⠂` a
1,74:1 a una altura desconocida es un numero y no una fotografia."*

    A  INK AREA, per glyph.  How much of a 9x19 cell the drawing covers.  The
       objection it answers is the one round three raised and round four
       repeated: `⠂` and `·` and `⋅` are "legible" at ratios the law accepts
       and are three pixels of ink.
    B  HOMOGLYPH DISTANCE, per pair.  The XOR area between two drawings over
       the cell area.  Four rounds have argued about `• ●`, `○ ◦`, `◎ ◉` and
       `† ‡` in prose and E2 has ruled every one of them unresolvable from the
       artefact.  They are numbers here.
    C  EFFECTIVE CONTRAST, per cell.  The ratio between the mean colour of the
       pixels a glyph ACTUALLY paints and the ground under them -- which is
       lower than the declared ratio for every glyph that is not solid,
       because antialiasing puts most of a thin glyph's pixels partway to the
       ground.  Reported WITH the coverage, because a 4.5:1 dot at 3% coverage
       is not legible and the corpus has several.
    D  COVERAGE x CONTRAST, per meaning mark.  A floor to PROPOSE.  It is
       tabulated and not enforced, and §5 of the report says why in the
       report's own words.

THIS FILE MEASURES AND DOES NOT RENDER.  Every pixel comes from
`raster.py` -- the canonical white-on-black tiles for A and B, the 66 shipped
PNGs for C and D.  The split is the same one `raster.py`'s own docstring
declares from the other side: a renderer that also scores has an opinion about
what it draws.

AND IT DOES NOT DECIDE WHAT A MEANING MARK IS.  `collision_census.role_map()`
does, through `A_FAMILIES` -- severity, danger, required, invalid, cursor,
which is `LEVELS` / `DANGER_FORM` / `REQUIRED` / `INVALID` / `CUR` exactly as
the brief names them.  A second list here would be a second census, and the
first one already has teeth (`ROSTER`, five rows that may only leave by being
closed).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes"))
sys.path.insert(0, str(HERE))

from PIL import Image                                            # noqa: E402

import collision_census as CC                                    # noqa: E402
import raster as RA                                              # noqa: E402
import screens as S                                              # noqa: E402
import taskboard.language as LG                                  # noqa: E402

PNG = HERE / "png"
OUT = ROOT / "prototypes" / "out" / "legibility.txt"

#: THE PAIRS FOUR ROUNDS ARGUED ABOUT IN PROSE, named in the brief, listed
#: here so the report answers the question that was actually asked rather than
#: the question the families happen to generate.  `╌ ┄ ┈` is three glyphs and
#: therefore three pairs; the rest are two.
ARGUED = (("•", "●"), ("○", "◦"), ("◎", "◉"), ("†", "‡"), ("▪", "■"),
          ("╌", "┄"), ("╌", "┈"), ("┄", "┈"), ("▬", "◦"), ("⠇", "⠸"))

# ===========================================================================
# inc81 -- THE FLOOR STOPS BEING A PROPOSAL.  Q1, Q2 and Q3, as given.
#
# Section E below asked three questions and enforced nothing.  The round
# answered all three and the orchestrator adopted the answers verbatim
# (2026-09-07, on the operator's delegation):
#
#   Q1  the legibility floor is TWO CLAUSES, not a product: coverage >= 15%
#       of the cell AND effective contrast >= 3:1, both at the declared seat.
#   Q2  runs of 1-4 cells carrying an A-family role are bound by the floor;
#       runs of >= 8 cells of one glyph are STRUCTURE, bound only to "not
#       equal to the ground"; 5-7 named per seat like `DIM_CLASSIFIES`.
#   Q3  the floor is judged at the DECLARED seat; the worst seat is reported
#       as a notice, never as a red.
#
# WHY TWO CLAUSES AND NOT THE PRODUCT, in the round's own arithmetic: `prism
# ⡀` holds 16.02:1 and cannot be seen, and `solari ▁` holds 1.20:1 and can.
# The product mixes two failures whose fixes are opposite -- one is answered
# by drawing another cell, the other by nothing at all -- and a single number
# hides which one a row is.
# ===========================================================================

#: Q1, the two clauses.  `COVERAGE` is the share of the cell whose pixels
#: differ from the ground at all; `EFFECTIVE` is the contrast between the
#: MEAN COLOUR of exactly those pixels and the ground under them.  Both are
#: section C's definitions and neither is new here.
COVERAGE_FLOOR = 0.15
EFFECTIVE_FLOOR = 3.0

#: Q2, the run-length classes.  A RUN is the uninterrupted horizontal stretch
#: of ONE glyph the `.txt` draws through the seat -- measured on the artefact,
#: not declared, because §0b of the round is a fact about the picture: the
#: same cell at the same contrast is legible at 55 cells of length and
#: invisible at one.
MEANING_MAX = 4        # 1..4 cells of an A-family glyph: bound by both clauses
STRUCTURE_MIN = 8      # >= 8 cells of one glyph: bound only to "not the ground"

#: THE LINE BELOW WHICH TWO GREYS ARE ONE GREY (inc84, section H).  It is a
#: REPORTING threshold and nothing is gated on it: 1.10:1 is roughly the
#: smallest step this corpus's own tone ladders ever spend deliberately
#: (`solari`'s seam sits at 1.20:1 against its ground and round five found it
#: legible at 100 cells of length), so anything under it is a distinction the
#: language is not making on purpose.  Named so the number in section H is
#: arguable rather than buried in a comparison.
GREY_DISTINCT = 1.10

#: THE 5-7 RUNS, named per seat exactly as `DIM_CLASSIFIES` names its own.
#: The corpus draws THREE of them and all three are naught's `∙`, which is
#: that kit's `DANGER_FORM` and the top two rungs of its severity ladder --
#: so the middle band is not an empty branch and is not a crowd either.
#:
#: A row is `(kit, family, cell, tone) -> (verdict, why)`.  The verdicts are
#: the two the ruling leaves available at this length: `bound` puts the run
#: under Q1's two clauses like a 1-4 run, `structure` puts it under the
#: >= 8 clause.  Nothing may be here without a reason a reader can check.
NAMED_RUNS = {
    ("naught", "severity", "∙", "#8a8a8a"):
        ("bound",
         "the muted severity rung of `naught_S5`, drawn seven cells wide "
         "where a log row spends it as a MARK and not as a rule. Seven "
         "cells of a 14.0%-coverage disc is still a mark: it names the "
         "row's kind and nothing else joins it."),
    ("naught", "severity", "∙", "#f5f5f5"):
        ("bound",
         "the same rung in `ink` on the graver rows. Same seat, same "
         "reading; the tier changed, the job did not."),
    ("naught", "danger", "∙", "#f5f5f5"):
        ("bound",
         "`DANGER_FORM`, which is the mark that says a button is "
         "irreversible. A five- or six-cell stretch of it is the button's "
         "own shoulder and not a rule across the page -- the 100-cell "
         "stretches of the same cell in `naught_S4` are structure and are "
         "classified there, which is the distinction this row exists to "
         "keep."),
}

#: THE A-FAMILY SEATS, DERIVED AND NOT ENUMERATED.  Q3 says the floor is
#: judged at the DECLARED seat, and a declared seat is not a row number: it is
#: the (cell, tone) pair the kit's OWN CONTRACT METHOD paints when the family
#: is exercised.  So the table below is five calls, not fifty-five rows, and a
#: kit that changes the tone of its severity rung moves its own seat.
#:
#: `collision_census.role_map` still decides WHICH FAMILY a cell carries --
#: this file keeps no second list of what a meaning is (the docstring's own
#: standing promise).  These calls only say what the cell is PAINTED IN when
#: it does that job, which is the half a census of declarations cannot have.
A_SEAT_CALLS = (
    ("severity", lambda k: [k.log_row(lv, "09:41", "board loaded")
                            for lv in ("info", "warn", "error")]),
    ("danger", lambda k: [k.button("Delete", danger=True)]),
    ("required", lambda k: [k.required()]),
    ("cursor", lambda k: [k.menu(["a", "b"], 0)[0]]),
    ("invalid", lambda k: [k.textfield("12/09/26", state=LG.INVALID, w=14)]),
)

_TONED = re.compile(r"\[([^\]]+)\]([^\[]*)")


def declared_tones(lang: str) -> dict[str, set[tuple[str, str]]]:
    """`family -> {(cell, tone)}`, read off the kit's own contract methods.

    Only cells `role_map` already credits to that family survive, so a letter
    that happens to sit inside a log message is not promoted to a severity
    rung by being printed next to one.
    """
    k = LG.kit(lang)
    named, _ = CC.role_map(lang)
    out: dict[str, set[tuple[str, str]]] = {}
    for family, call in A_SEAT_CALLS:
        for markup in call(k):
            for tone, body in _TONED.findall(markup):
                tone = tone.split()[-1]
                if not tone.startswith("#"):
                    continue
                for ch in body:
                    if family in named.get(ch, {}):
                        out.setdefault(family, set()).add((ch, tone))
    return out


def match_branch(lang: str) -> tuple[str, str, str]:
    """`(channel, the match ink, the ground it is painted on)`.

    THE SAME DERIVATION THE SUITE USES, restated here rather than imported --
    the standing bargain of this pair of files: `test_the_match_run_is_
    legible_and_distinct_on_its_declared_channel` reads `MATCH_STYLE` the
    same way, and the two can only agree by being right.  The STYLE word
    gives `bold` / `underline` / `reverse`; the TOKEN gives whether the mark
    is a hue of its own or the kit's own ink at another weight.
    """
    k, t = LG.kit(lang), LG.THEMES[lang]
    word, token = (k.MATCH_STYLE.split()[0],
                   k.MATCH_STYLE.strip().split()[-1].strip("{}"))
    value = t.get(token, t["ink"])
    if word == "reverse":
        return "reverse", t["ground"], value
    if token in ("accent", "alert") and value != t["ink"]:
        return "hue", value, t["ground"]
    return word, value, t["ground"]


def _grey(px) -> tuple:
    """One colour with its hue removed, by `raster.grey_of`'s own transform.

    Read through the renderer rather than reimplemented, so a greyscale
    number in this report is a number about the greyscale PNG on disk.
    """
    g = RA._encode(sum(w * RA._linear(c)
                       for w, c in zip(RA.GREY_WEIGHTS, px)))
    return (g, g, g)


class Sheets:
    """The 66 `.txt`, and the run a seat sits in.

    Run length is read off the TEXT and not off the svg's run encoding: the
    exporter splits a run wherever the colour changes, so a hundred cells of
    one glyph in two tiers is two svg runs and one drawn stroke, and it is the
    stroke the eye integrates along.
    """

    def __init__(self) -> None:
        self.rows: dict[tuple[str, str], list[str]] = {}
        for lang in LG.KITS:
            for screen in S.SCREENS:
                self.rows[(lang, screen)] = (
                    HERE / f"{lang}_{screen}.txt").read_text(
                        encoding="utf-8").rstrip("\n").split("\n")

    def run(self, lang: str, screen: str, x: int, y: int, ch: str) -> int:
        row = self.rows[(lang, screen)][y]
        a = b = x
        while a > 0 and row[a - 1] == ch:
            a -= 1
        while b + 1 < len(row) and row[b + 1] == ch:
            b += 1
        return b - a + 1


def run_class(n: int) -> str:
    """Q2 in one function: `meaning` / `named` / `structure`."""
    if n <= MEANING_MAX:
        return "meaning"
    return "structure" if n >= STRUCTURE_MIN else "named"


def blank_runs() -> list[tuple]:
    """K8 / E6 -- every run of BLANK cells painted on a second ground.

    `(kit, screen, row, x, cells, ground, canvas, contrast)`, structure runs
    (>= 8 cells) only, which is the length the ruling classifies them at.

    THE OBJECTION IN ONE SENTENCE: a run of spaces on a rect that is not the
    canvas is INK -- `solari_S4` row 10 is a hundred of them on `#f5a300` and
    is the brightest thing in that kit -- and eleven batches of instruments
    read glyphs, so no census, no family table, no coverage measure and no law
    could name it.  Ruling K8 (orchestrator, 2026-09-07): it is counted, and
    it obeys Q2 as structure, which asks only that it not equal the ground.

    Read off the SIDECAR, which already carries the ground the cell was
    actually painted on -- the same resolution `Cells` reads for glyphs.
    """
    out = []
    for lang in LG.KITS:
        for screen in S.SCREENS:
            side = json.loads((PNG / f"{lang}_{screen}.json").read_text(
                encoding="utf-8"))
            canvas = side["ground"]
            for y, runs in enumerate(side["grid"]):
                for x0, text, fg, bg, bold, und in runs:
                    if bg == canvas or und:
                        continue
                    if len(text) < STRUCTURE_MIN:
                        continue
                    if any(c not in CC.BLANKS for c in text):
                        continue
                    out.append((lang, screen, y, x0, len(text), bg, canvas,
                                contrast(rgb(bg), rgb(canvas))))
    return out

#: WCAG 2.x, the same arithmetic `tests/test_components.py` and four packets
#: use.  Restated rather than imported because the test file is a test file;
#: the two agree by construction and the agreement is asserted there.
def luminance(rgb) -> float:
    ch = []
    for v in rgb:
        v /= 255
        ch.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def contrast(a, b) -> float:
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def rgb(hexed: str):
    return tuple(bytes.fromhex(hexed[1:]))


class Ink:
    """The canonical drawing of every glyph the corpus spends, as coverage.

    WHITE ON BLACK AND NOTHING ELSE, so the number is the DRAWING and not the
    colour it happened to be painted in.  A pixel's value over 255 is how much
    of it the outline covers, which is what FreeType's antialiasing means and
    what makes an XOR area a real area rather than a count of lit pixels.

    Regular and bold are kept apart: seven kits declare `bold` at `MATCH_STYLE`
    and a bold stem is more ink at the same cell, so folding them together
    would report one glyph's area as whichever weight was seen first.
    """

    def __init__(self) -> None:
        self.m = RA.Metrics()
        self.area = self.m.w * self.m.h
        self._cache: dict[tuple[str, bool], tuple[float, ...]] = {}

    def cov(self, ch: str, bold: bool = False) -> tuple[float, ...]:
        key = (ch, bold)
        if key not in self._cache:
            tile = RA.cell_tile(self.m, ch, "#ffffff", "#000000", bold, False)
            b = tile.tobytes()
            self._cache[key] = tuple(b[i] / 255 for i in range(0, len(b), 3))
        return self._cache[key]

    def ink_area(self, ch: str, bold: bool = False) -> float:
        """Share of the cell the drawing covers, 0.0 to 1.0."""
        return sum(self.cov(ch, bold)) / self.area

    def touched(self, ch: str, bold: bool = False) -> float:
        """Share of the cell the drawing TOUCHES at all, ink or fringe."""
        return sum(1 for v in self.cov(ch, bold) if v > 0) / self.area

    def distance(self, a: str, b: str, bold: bool = False) -> float:
        """XOR area over cell area: 0.0 means ONE DRAWING.

        The brief's own words -- *"so 'same drawing' becomes a number"*.  It
        is `sum |cov_a - cov_b| / cell`, so it is symmetric, it is zero only
        when the two rasterise identically, and it is in the same unit as the
        ink areas above, which is what makes "these two differ by 3% of a
        cell" a sentence somebody can act on.
        """
        ca, cb = self.cov(a, bold), self.cov(b, bold)
        return sum(abs(x - y) for x, y in zip(ca, cb)) / self.area


def corpus_glyphs() -> dict[str, int]:
    """`{glyph: how many cells of the 66 sheets it fills}`, blank dropped."""
    n: dict[str, int] = {}
    for p in sorted(HERE.glob("*_S?.txt")):
        for ch in p.read_text(encoding="utf-8"):
            if ch not in ("\n", " "):
                n[ch] = n.get(ch, 0) + 1
    return dict(sorted(n.items(), key=lambda kv: (-kv[1], kv[0])))


class Cells:
    """Every distinct painted cell of the 66 PNGs, measured once.

    A cell is `(glyph, ink, ground, bold, underline)` and the raster composes
    one box at a time, so two cells with that tuple are the same pixels --
    inc76's law asserts exactly that.  So the corpus's 211 200 cells reduce to
    a few thousand distinct drawings, and each is measured once.

    WHAT IS MEASURED, and the definitions matter more than the numbers:

    * `coverage` -- the share of the cell whose pixels differ from the ground
      at all.  This is the "how much of the box does the eye get" number.
    * `effective` -- the contrast between the MEAN COLOUR of exactly those
      pixels and the ground.  For a solid glyph it equals the declared ratio;
      for a hairline it is much lower, because most of a hairline's pixels are
      partway to the ground and the declared ratio describes a colour that
      appears in almost none of them.
    * `declared` -- `contrast(ink, ground)`, which is the only thing four
      rounds of this programme have had.

    THE GROUND IS THE ONE UNDER THE CELL, not the canvas -- ruling K6, and it
    arrives that way already: `cell_grid` resolves `reverse` and the sidecar
    records the ground the cell was actually painted on.
    """

    def __init__(self) -> None:
        self.seats: dict[tuple, list] = {}
        for lang in LG.KITS:
            for screen in S.SCREENS:
                self._read(lang, screen)

    def _read(self, lang: str, screen: str) -> None:
        name = f"{lang}_{screen}"
        side = json.loads((PNG / f"{name}.json").read_text(encoding="utf-8"))
        w, h = side["cell"]["w"], side["cell"]["h"]
        with Image.open(PNG / f"{name}.png") as raw:
            im = raw.convert("RGB")
        for y, runs in enumerate(side["grid"]):
            for x0, text, fg, bg, bold, und in runs:
                for i, ch in enumerate(text):
                    if ch == " " and not und:
                        continue
                    key = (lang, ch, fg, bg, bold, und)
                    if key in self.seats:
                        self.seats[key][-1].append((screen, x0 + i, y))
                        continue
                    x = x0 + i
                    blk = im.crop((x * w, y * h, x * w + w, y * h + h))
                    self.seats[key] = [*self._measure(blk, fg, bg),
                                       [(screen, x, y)]]

    @staticmethod
    def _measure(blk, fg: str, bg: str):
        F, B = rgb(fg), rgb(bg)
        b = blk.tobytes()
        px = [tuple(b[i:i + 3]) for i in range(0, len(b), 3)]
        painted = [p for p in px if p != B]
        n = len(painted)
        if not n:
            return 0.0, 1.0, contrast(F, B)
        mean = tuple(sum(p[c] for p in painted) / n for c in range(3))
        return n / len(px), contrast(mean, B), contrast(F, B)

    def of(self, lang: str, ch: str):
        """Every seat this kit paints this glyph in, worst first."""
        got = [(cov, eff, dec, fg, bg, bold, und, seats)
               for (l, c, fg, bg, bold, und), (cov, eff, dec, seats)
               in self.seats.items() if l == lang and c == ch]
        return sorted(got, key=lambda t: t[0] * t[1])


def _bar(v: float, width: int = 12) -> str:
    """A fixed-width text gauge, so a column of numbers has a shape."""
    n = max(0, min(width, round(v * width)))
    return "#" * n + "." * (width - n)


def report() -> str:
    ink, cells = Ink(), Cells()
    used = corpus_glyphs()
    w = []

    def h(title: str) -> None:
        w.append("")
        w.append("=" * 78)
        w.append(title)
        w.append("=" * 78)

    w.append("legibility.txt -- the 66 frames measured on the RASTER, not on "
             "the svg")
    w.append("")
    w.append(f"  face      {RA.FONT_NAME} {RA.FONT_PX}px  {RA.FONT_PATH}")
    w.append(f"  cell      {ink.m.w}x{ink.m.h} px = {ink.area} pixels")
    w.append(f"  fallback  {RA.FALLBACK_NAME} for {RA.FALLBACK_CELLS} "
             f"(sizes {ink.m.fallback_px})")
    w.append(f"  corpus    {len(used)} distinct painted glyphs, "
             f"{sum(used.values())} painted cells, "
             f"{len(cells.seats)} distinct (kit, glyph, ink, ground, "
             f"weight, decoration) drawings")
    w.append("")
    w.append("  Every number below is an AREA or a RATIO measured on pixels a")
    w.append("  font actually drew. E2 (the svg carries no font metric) is")
    w.append("  what this file exists to close; it does not decide any of the")
    w.append("  objections that were parked behind it -- it gives them")
    w.append("  numbers, which is what four rounds asked for.")

    # ---- A ---------------------------------------------------------------
    h("A. INK AREA -- how much of a 9x19 cell each drawing covers")
    w.append("")
    w.append("`ink` is the antialiasing-weighted area: a pixel half covered")
    w.append("by the outline counts a half. `touch` is the share of the cell")
    w.append("the drawing reaches at all. The gap between them is fringe, and")
    w.append("a glyph whose ink is much smaller than its touch is a glyph")
    w.append("that is mostly edge -- which is section C's whole subject.")
    w.append("")
    w.append(f"{'glyph':>6} {'cells':>7} {'ink':>7} {'touch':>7}  "
             f"{'ink area':<14}")
    w.append("-" * 56)
    for ch, n in sorted(used.items(), key=lambda kv: ink.ink_area(kv[0])):
        w.append(f"{ch:>6} {n:>7} {ink.ink_area(ch):>6.1%} "
                 f"{ink.touched(ch):>6.1%}  {_bar(ink.ink_area(ch))}")
    blank = [ch for ch in used if ink.touched(ch) == 0]
    if blank:
        w.append("")
        w.append(f"A1. {len(blank)} GLYPH(S) IN THIS CORPUS DRAW NOTHING AT "
                 f"ALL: {' '.join(blank)}")
        w.append("")
        for ch in blank:
            who = {L: sum((HERE / f"{L}_{s}.txt").read_text(
                encoding="utf-8").count(ch) for s in S.SCREENS)
                for L in LG.KITS}
            w.append(f"    U+{ord(ch):04X}  "
                     + "  ".join(f"{k} {v}" for k, v in who.items() if v))
        w.append("")
        w.append("    `capture_languages.ink()` counts a cell as ink whenever")
        w.append("    it is not a space or a non-breaking space, so these")
        w.append("    cells are counted as ink by the density measure and")
        w.append("    paint no pixel. That is a fact about the DENSITY")
        w.append("    MEASURE, not about the kits that spend them, and it is")
        w.append("    reported here because this is the first artefact in the")
        w.append("    programme that could see it.")

    # ---- B ---------------------------------------------------------------
    h("B. HOMOGLYPH DISTANCE -- XOR area between two drawings, over the cell")
    w.append("")
    w.append("0.0% means ONE DRAWING. The measure is symmetric and it is in")
    w.append("the same unit as section A, so `2.5%` means the two glyphs")
    w.append("differ by two and a half per cent of a cell -- about four of")
    w.append(f"the cell's {ink.area} pixels.")

    w.append("")
    w.append("B1. THE TEN PAIRS FOUR ROUNDS ARGUED ABOUT, by name")
    w.append("")
    w.append(f"{'pair':>9} {'distance':>10} {'ink a':>7} {'ink b':>7}  "
             f"{'both drawn?':<14}")
    w.append("-" * 60)
    for a, b in ARGUED:
        both = ("yes" if a in used and b in used else
                f"only {a if a in used else b}"
                if (a in used) != (b in used) else "neither")
        w.append(f"{a + ' ' + b:>9} {ink.distance(a, b):>9.2%} "
                 f"{ink.ink_area(a):>6.1%} {ink.ink_area(b):>6.1%}  {both:<14}")

    w.append("")
    w.append("B2. THE TEN SMALLEST IN THE CORPUS -- every pair of distinct")
    w.append("    glyphs the 66 sheets actually draw, not only the declared")
    w.append("    families. This is the sweep no family list can produce.")
    w.append("")
    drawn = sorted(used)
    every = sorted(((ink.distance(a, b), a, b)
                    for i, a in enumerate(drawn) for b in drawn[i + 1:]),
                   key=lambda t: (t[0], t[1], t[2]))
    fams = {frozenset(p) for p in CC.HOMOGLYPHS}
    w.append(f"{'pair':>9} {'distance':>10}  {'in a family?':<16} "
             f"{'cells a':>8} {'cells b':>8}")
    w.append("-" * 60)
    for d, a, b in every[:10]:
        w.append(f"{a + ' ' + b:>9} {d:>9.2%}  "
                 f"{('yes' if frozenset((a, b)) in fams else 'NO'):<16} "
                 f"{used[a]:>8} {used[b]:>8}")

    w.append("")
    w.append(f"B3. THE {len(CC.HOMOGLYPHS)} PAIRS `HOMOGLYPH_FAMILIES` "
             f"DERIVES, smallest first")
    w.append("")
    w.append(f"{'pair':>9} {'distance':>10}  {'drawn':<12}")
    w.append("-" * 40)
    for d, a, b in sorted((ink.distance(a, b), a, b)
                          for a, b in CC.HOMOGLYPHS):
        seen = f"{used.get(a, 0)}/{used.get(b, 0)}"
        w.append(f"{a + ' ' + b:>9} {d:>9.2%}  {seen:<12}")

    w.append("")
    w.append("B4. THE PAIRS THE CENSUS FLAGS, per kit -- a cell whose meaning")
    w.append("    has a homoglyph carrying another meaning. The distance is")
    w.append("    the number `collision_census.py` could not produce.")
    w.append("")
    w.append(f"{'kit':<11} {'pair':>9} {'distance':>10}  {'roles':<44}")
    w.append("-" * 78)
    flagged = 0
    for lang in LG.KITS:
        for cell, av, twin, bv in CC.homoglyph_rows(lang):
            flagged += 1
            w.append(f"{lang:<11} {cell + ' ' + twin:>9} "
                     f"{ink.distance(cell, twin):>9.2%}  "
                     f"{'+'.join(av) + ' vs ' + '+'.join(bv):<44}")
    w.append("-" * 78)
    w.append(f"{flagged} rows, the census's own count")

    # ---- C ---------------------------------------------------------------
    h("C. EFFECTIVE CONTRAST -- the ratio the pixels give, and the coverage")
    w.append("")
    w.append("`declared` is contrast(ink, ground): the number four rounds")
    w.append("have had. `effective` is the contrast between the MEAN COLOUR")
    w.append("of the pixels the glyph actually paints and the ground under")
    w.append("them. They are equal for a solid glyph and far apart for a")
    w.append("hairline, because most of a hairline's pixels are partway to")
    w.append("the ground and the declared ratio describes a colour that")
    w.append("appears in hardly any of them.")
    w.append("")
    w.append("The forty worst cells in the corpus by coverage x effective,")
    w.append("which is the product section D proposes as a floor.")
    w.append("")
    w.append(f"{'kit':<11} {'gl':>3} {'cov':>6} {'eff':>7} {'decl':>7} "
             f"{'cov*eff':>8}  {'seat':<26}")
    w.append("-" * 78)
    rows = sorted(((cov * eff, lang, ch, cov, eff, dec, seats)
                   for (lang, ch, fg, bg, bold, und),
                   (cov, eff, dec, seats) in cells.seats.items()),
                  key=lambda t: (t[0], t[1], t[2]))
    for _, lang, ch, cov, eff, dec, seats in rows[:40]:
        s, x, y = seats[0]
        where = f"{s} r{y} c{x} (+{len(seats) - 1})"
        w.append(f"{lang:<11} {ch:>3} {cov:>5.1%} {eff:>6.2f} {dec:>6.2f} "
                 f"{cov * eff:>8.3f}  {where:<26}")

    # ---- D ---------------------------------------------------------------
    h("D. THE MEANING MARKS -- coverage x effective contrast, every kit")
    w.append("")
    w.append("The families are `collision_census.A_FAMILIES`, which is")
    w.append("LEVELS / DANGER_FORM / REQUIRED / INVALID / CUR exactly as the")
    w.append("brief names them, read through the census's own `role_map` so")
    w.append("this file does not keep a second list of what a meaning is.")
    w.append("")
    w.append("A mark is reported at its WORST seat: the one occurrence in the")
    w.append("kit's six sheets with the smallest coverage x effective. A mark")
    w.append("the corpus never draws says so -- and there are many, which is")
    w.append("a finding about the corpus and not about the marks.")
    w.append("")
    w.append(f"{'kit':<11} {'gl':>3} {'family':<24} {'cov':>6} {'eff':>7} "
             f"{'decl':>7} {'cov*eff':>8}  {'where':<14}")
    w.append("-" * 78)
    table, undeclared = [], []
    for lang in LG.KITS:
        named, _ = CC.role_map(lang)
        for cell in sorted(named):
            fams_here = sorted(f for f in named[cell] if f in CC.A_FAMILIES)
            if not fams_here:
                continue
            roles = "+".join(fams_here)
            seats = cells.of(lang, cell)
            if not seats:
                w.append(f"{lang:<11} {cell:>3} {roles:<24} "
                         f"{'--':>6} {'--':>7} {'--':>7} {'--':>8}  NOT DRAWN")
                continue
            cov, eff, dec, fg, bg, bold, und, where = seats[0]
            sc, x, y = where[0]
            table.append((cov * eff, lang, cell, roles, cov, eff, dec))
            if dec < 3.0:
                undeclared.append((lang, cell, roles, dec))
            w.append(f"{lang:<11} {cell:>3} {roles:<24} {cov:>5.1%} "
                     f"{eff:>6.2f} {dec:>6.2f} {cov * eff:>8.3f}  "
                     f"{sc + ' r' + str(y):<14}")

    w.append("")
    w.append("D1. THE TEN WORST MEANING MARKS IN THE CORPUS")
    w.append("")
    w.append(f"{'rank':>4} {'kit':<11} {'gl':>3} {'family':<24} {'cov':>6} "
             f"{'eff':>7} {'decl':>7} {'cov*eff':>8}")
    w.append("-" * 78)
    for i, (prod, lang, cell, roles, cov, eff, dec) in enumerate(
            sorted(table)[:10], 1):
        w.append(f"{i:>4} {lang:<11} {cell:>3} {roles:<24} {cov:>5.1%} "
                 f"{eff:>6.2f} {dec:>6.2f} {prod:>8.3f}")

    # ---- E ---------------------------------------------------------------
    h("E. THE PRODUCT, AND WHY THE RULING DID NOT TAKE IT")
    w.append("")
    lo = sorted(table)
    w.append(f"The {len(table)} meaning marks the corpus draws span "
             f"{lo[0][0]:.3f} to {lo[-1][0]:.3f} on coverage x effective.")
    w.append("")
    w.append(f"AND {len(undeclared)} OF THEM ARE UNDER 3:1 ON DECLARED")
    w.append("CONTRAST AT THE SEAT REPORTED HERE. That number is NOT a count")
    w.append("of violations and must not be read as one. `worst seat` is this")
    w.append("report's own choice of where to look, and inc74 judged seats one")
    w.append("at a time: `DIM_CLASSIFIES` has eight seats and three verdicts,")
    w.append("and a mark that is a severity rung on a log row and a decorative")
    w.append("leader in a masthead is legitimately two things. The count is")
    w.append("here because nobody has taken it before, and because it is the")
    w.append("size of the question a ruling would be answering.")
    w.append("")
    w.append("WHY THIS PRODUCT AND NOT A RATIO. A ratio cannot say that a mark")
    w.append("holding 4.5:1 is three pixels. Section C's worst rows are the")
    w.append("proof: they are not contrast failures, they are AREA failures")
    w.append("wearing a passing ratio -- and four rounds of this programme had")
    w.append("no way to tell the two apart, because the svg carries a colour")
    w.append("and not a drawing.")
    w.append("")
    w.append("AND THE ROUND DID NOT TAKE THE PRODUCT. The three questions")
    w.append("this section left open were answered on 2026-09-07 and section")
    w.append("F is the answer, enforced. The product stays here because it is")
    w.append("what produced the question -- and because the round's own §7")
    w.append("says why it is a bad ranking: `naught ◦` at 13.5% coverage is")
    w.append("found by eye and `instrument ⠇` at 15.8% is not, so the order")
    w.append("the product gives is not the order a reader sees. A threshold")
    w.append("that separates `found` from `not found` is defensible; a league")
    w.append("table is not.")
    w.append("")
    w.append("WHAT SURVIVES UNCHANGED as a limit of the whole instrument: the")
    w.append("face is not the terminal. Windows Terminal draws its own box and")
    w.append("block glyphs, so every row in this file whose glyph is box")
    w.append("drawing is a number about Cascadia's version of it.")

    # ---- F ---------------------------------------------------------------
    h("F. THE FLOOR AS LAW -- Q1, Q2 and Q3, at the declared seat")
    w.append("")
    w.append(f"Q1  coverage >= {COVERAGE_FLOOR:.0%} of the cell AND effective "
             f"contrast >= {EFFECTIVE_FLOOR:.0f}:1,")
    w.append("    two clauses, both at the declared seat. Not a product.")
    w.append(f"Q2  a run of 1..{MEANING_MAX} cells carrying an A-family role "
             f"is bound; a run of")
    w.append(f"    >= {STRUCTURE_MIN} cells of one glyph is STRUCTURE and owes "
             f"only `not equal to")
    w.append(f"    the ground`; {MEANING_MAX + 1}..{STRUCTURE_MIN - 1} is "
             f"named per seat in `NAMED_RUNS`.")
    w.append("Q3  judged at the DECLARED seat. Section D's worst seat is a")
    w.append("    NOTICE and is never a red.")
    w.append("")
    w.append("THE DECLARED SEAT IS DERIVED, NOT LISTED. It is the (cell, tone)")
    w.append("pair the kit's own contract method paints when the family is")
    w.append("exercised -- `log_row`, `button(danger=True)`, `required`,")
    w.append("`menu`, `textfield(INVALID)` -- intersected with the census's")
    w.append("`role_map`, so this file still keeps no second list of what a")
    w.append("meaning is. Five calls, not fifty-five rows.")
    w.append("")

    sheets = Sheets()
    floor_rows, notice_rows, mid_rows = [], [], []
    for lang in LG.KITS:
        dec = declared_tones(lang)
        for family in CC.A_FAMILIES:
            for ch, tone in sorted(dec.get(family, ())):
                for cov, eff, dc, fg, bg, bold, und, seats in cells.of(lang, ch):
                    if fg != tone:
                        continue
                    lens = [sheets.run(lang, sc, x, y, ch)
                            for sc, x, y in seats]
                    classes = {run_class(n) for n in lens}
                    key = (lang, family, ch, tone)
                    if "named" in classes:
                        mid_rows.append((key, sorted(
                            n for n in lens if run_class(n) == "named")))
                    bound = "meaning" in classes or (
                        key in NAMED_RUNS and NAMED_RUNS[key][0] == "bound")
                    if not bound:
                        continue
                    miss = ("COV" if cov < COVERAGE_FLOOR else "") + \
                           ("EFF" if eff < EFFECTIVE_FLOOR else "")
                    sc, x, y = seats[0]
                    floor_rows.append((lang, family, ch, tone, cov, eff, dc,
                                       min(lens), max(lens), miss,
                                       f"{sc} r{y}", bg))

    w.append(f"{'kit':<11} {'family':<9} {'gl':>3} {'tone':<8} {'cov':>6} "
             f"{'eff':>6} {'decl':>6} {'run':>7}  {'seat':<9} {'verdict':<8}")
    w.append("-" * 78)
    for (lang, family, ch, tone, cov, eff, dc, lo_n, hi_n, miss, where,
         bg) in floor_rows:
        span = f"{lo_n}" if lo_n == hi_n else f"{lo_n}-{hi_n}"
        w.append(f"{lang:<11} {family:<9} {ch:>3} {tone:<8} {cov:>5.1%} "
                 f"{eff:>6.2f} {dc:>6.2f} {span:>7}  {where:<9} "
                 f"{('FAIL ' + miss) if miss else 'pass':<8}")
    bad = [r for r in floor_rows if r[9]]
    w.append("-" * 78)
    w.append(f"F1. {len(floor_rows)} BOUND SEATS, "
             f"{len(floor_rows) - len(bad)} PASS, {len(bad)} FAIL")
    w.append("")
    w.append(f"    coverage only    "
             f"{sum(1 for r in bad if r[9] == 'COV')}")
    w.append(f"    effective only   "
             f"{sum(1 for r in bad if r[9] == 'EFF')}")
    w.append(f"    both clauses     "
             f"{sum(1 for r in bad if r[9] == 'COVEFF')}")
    w.append("")

    w.append("F2. THE ELEVEN OBLIGATIONS, which is the row the round predicted")
    w.append("")
    w.append(f"{'kit':<11} {'gl':>3} {'cov':>6} {'eff':>6} {'decl':>7} "
             f"{'verdict':<12}")
    w.append("-" * 52)
    req = [r for r in floor_rows if r[1] == "required"]
    for lang, family, ch, tone, cov, eff, dc, lo_n, hi_n, miss, where, bg in req:
        w.append(f"{lang:<11} {ch:>3} {cov:>5.1%} {eff:>6.2f} {dc:>6.2f} "
                 f"{('FAIL ' + miss) if miss else 'pass':<12}")
    req_bad = [r for r in req if r[9]]
    w.append("-" * 52)
    w.append(f"{len(req)} obligations, {len(req_bad)} under the floor: "
             + ", ".join(f"{r[0]} {r[2]}" for r in req_bad))
    w.append("")
    w.append("    ALL ELEVEN CLEAR THE CONTRAST CLAUSE and always did: the")
    w.append("    two the round sent back held the two BEST declared ratios")
    w.append("    of the eleven while failing to be visible, which is the")
    w.append("    whole reason Q1 is two clauses and not a product.")
    w.append("")
    w.append("    inc81 MEASURED THREE COVERAGE FAILURES WHERE THE ROUND")
    w.append("    PREDICTED TWO. inc82 fixed the two it named -- instrument")
    w.append("    `⠁` 5.8% -> `⣉` 23.4%, prism `⡀` 5.3% -> `⣆` 21.6%, both by")
    w.append("    AREA out of each language's own alphabet, with the contrast")
    w.append("    untouched. The third, swiss `•` at 14.0%, is one point under")
    w.append("    a floor the round set at 15% and is a mark the same round")
    w.append("    recorded as visible (`swiss_S2`: *\"`•` obligatorio ... se")
    w.append("    ve\"*). It is NAMED AND NOT ADJUSTED: a floor moved to fit")
    w.append("    the corpus it was written for is not a floor, and a mark")
    w.append("    changed to fit a floor nobody re-argued is not a fix.")
    w.append("")

    w.append(f"F3. THE {MEANING_MAX + 1}-{STRUCTURE_MIN - 1} RUNS, named per "
             f"seat")
    w.append("")
    seen_mid = sorted({k for k, _ in mid_rows})
    for key in seen_mid:
        lens = sorted({n for k, ns in mid_rows if k == key for n in ns})
        verdict, why = NAMED_RUNS[key]
        w.append(f"    {key[0]} {key[1]} {key[2]} {key[3]}  "
                 f"run {lens}  -> {verdict}")
    w.append("")
    w.append(f"    {len(seen_mid)} seats in the middle band, all of them "
             f"naught's `∙`.")
    w.append("    Every one is NAMED in `NAMED_RUNS` with a reason; an")
    w.append("    unnamed middle run is a hole in the ruling and the law")
    w.append("    below goes red on it rather than choosing a side.")
    w.append("")

    w.append("F4. THE WORST SEAT, AS A NOTICE (Q3)")
    w.append("")
    w.append("    Section D reports every mark at its WORST seat and 45 of 79")
    w.append("    sit under 3:1 declared there. Under Q3 that is a notice and")
    w.append("    not a verdict: the worst seat of a mark is almost always its")
    w.append("    DECORATIVE one -- `instrument ·` in a masthead, `ledger ·`")
    w.append("    in a leader -- so a kit judged by its worst seat is a kit")
    w.append("    failed for its decoration. The declared seat is above.")

    # ---- G ---------------------------------------------------------------
    h("G. THE GLYPHLESS RUN -- K8 / E6, the ink no instrument could see")
    w.append("")
    w.append("A run of BLANK cells painted on a rect that is not the canvas is")
    w.append("INK. `solari_S4` row 10 is a hundred of them on `#f5a300` and is")
    w.append("the brightest thing that kit draws; it is the OPENER of the")
    w.append("band whose closer round four called the only mark there.")
    w.append("Eleven batches of instruments read glyphs, so no census, no")
    w.append("family table, no coverage measure and no law in this programme")
    w.append("could name it. Ruling K8 (2026-09-07): it is counted.")
    w.append("")
    blanks = blank_runs()
    w.append(f"{'kit':<11} {'sheet':<6} {'row':>4} {'x':>4} {'cells':>6} "
             f"{'surface':<9} {'canvas':<9} {'ratio':>7}")
    w.append("-" * 66)
    for lang, screen, y, x0, n, bg, canvas, ratio in blanks:
        w.append(f"{lang:<11} {screen:<6} {y:>4} {x0:>4} {n:>6} "
                 f"{bg:<9} {canvas:<9} {ratio:>6.2f}")
    w.append("-" * 66)
    kits = sorted({r[0] for r in blanks})
    w.append(f"{len(blanks)} runs of {STRUCTURE_MIN} cells or more, in "
             f"{len(kits)} kits: {', '.join(kits)}")
    w.append("")
    w.append("EVERY ONE IS STRUCTURE UNDER Q2 and therefore owes exactly one")
    w.append("thing -- not to equal the ground it is painted on. All "
             f"{len(blanks)} clear")
    w.append("it. That is a weak clause and it is the right one: a plate is")
    w.append("not a mark and a coverage floor has nothing to say about a")
    w.append("surface with no drawing in it.")
    w.append("")
    w.append("WHAT IS STILL NOT COUNTED, said out loud: "
             "`collision_census.py` reads")
    w.append("DECLARATIONS and not frames, so its TOTAL cannot move for a run")
    w.append("that exists only in a picture. The frame-side count is here and")
    w.append("in the suite; the census's 28 is unchanged and means what it")
    w.append("always meant.")

    # ---- H ---------------------------------------------------------------
    h("H. THE MATCH IN GREYSCALE -- L12, on the pixels and not on a token")
    w.append("")
    w.append("Round five's L12: in three kits the ONLY channel the match run")
    w.append("has is HUE (instrument, nord, prism), and the clause that")
    w.append("approves them measures LUMINANCE against an achromatic `mut` --")
    w.append("the dimension in which a saturated hue and a grey are least")
    w.append("different. Its §0d says the objection cannot be settled from")
    w.append("this repo because there is no greyscale capture in it. There is")
    w.append("now: `raster.py` writes `<name>.grey.png` beside every frame,")
    w.append("WCAG relative luminance, so a contrast ratio measured on the")
    w.append("grey is the same arithmetic measured on one dimension.")
    w.append("")
    w.append("A MATCH THAT VANISHES IN GREY IS RECORDED AS A LIMIT OF THE")
    w.append("LANGUAGE AND IS NOT FIXED (the ruling's own words). This")
    w.append("section is the record.")
    w.append("")
    w.append("THE QUESTION IS DISTINCTNESS, NOT LEGIBILITY, and that is where")
    w.append("the measurement has to point. A match run is legible against its")
    w.append("GROUND and distinct against the BODY it stands in -- the six")
    w.append("`re` of `nord_S6` are teal among slate words. So the number that")
    w.append("answers L12 is the match ink against `mut` and against `ink`,")
    w.append("in grey. A run that is 1.00:1 from the body it sits in is a run")
    w.append("nobody can pick out, whatever it does against the page.")
    w.append("")
    w.append(f"{'kit':<11} {'channel':<10} {'v ground':>9} {'v mut':>7} "
             f"{'v ink':>7} | {'grey mut':>9} {'grey ink':>9}  {'verdict':<9}")
    w.append("-" * 78)
    limits = []
    for lang in LG.KITS:
        t = LG.THEMES[lang]
        branch, ink_hex, ground = match_branch(lang)
        pair = (rgb(ink_hex), rgb(ground))
        col_g = contrast(*pair)
        c_mut = contrast(rgb(ink_hex), rgb(t["mut"]))
        c_ink = contrast(rgb(ink_hex), rgb(t["ink"]))
        g_mut = contrast(_grey(rgb(ink_hex)), _grey(rgb(t["mut"])))
        g_ink = contrast(_grey(rgb(ink_hex)), _grey(rgb(t["ink"])))
        flat = max(g_mut, g_ink) < GREY_DISTINCT
        if branch in ("bold", "underline", "reverse"):
            verdict = "carried"        # a second, non-colour channel exists
        elif flat:
            verdict = "VANISHES"
            limits.append((lang, round(g_mut, 2), round(g_ink, 2)))
        else:
            verdict = "holds"
        w.append(f"{lang:<11} {branch:<10} {col_g:>8.2f} {c_mut:>7.2f} "
                 f"{c_ink:>7.2f} | {g_mut:>8.2f} {g_ink:>8.2f}  {verdict:<9}")
    w.append("-" * 78)
    hue = [l for l in LG.KITS if match_branch(l)[0] == "hue"]
    w.append(f"{len(hue)} kits carry the match on HUE ALONE: "
             f"{', '.join(hue)}")
    w.append(f"{len(limits)} of them lose it in grey at the "
             f"{GREY_DISTINCT:.2f}:1 line"
             + (": " + ", ".join(f"{l} ({m}/{i})" for l, m, i in limits)
                if limits else ""))
    w.append("")
    w.append("EACH ROW ABOVE IS A LIMIT OF THE LANGUAGE AND IS NOT FIXED --")
    w.append("the ruling's own instruction. A kit whose match is BOLD,")
    w.append("UNDERLINED or REVERSED is `carried`: it has a second channel")
    w.append("that survives by construction and the grey column is a")
    w.append("courtesy, not a verdict.")
    w.append("")
    w.append("AND THE MEASUREMENT DOES NOT SAY WHAT L12 SAID. Round five wrote")
    w.append("*\"en escala de grises no queda nada\"* about three kits and")
    w.append("could not check it. Checked: NONE of the four hue kits goes to")
    w.append("1.00:1. What survives is a LUMINANCE STEP the accent happens to")
    w.append("carry along with its hue -- nord 1.34, swiss 1.52, prism 1.59,")
    w.append("instrument 2.34 against `mut` -- so the objection is real in")
    w.append("SHAPE and wrong in DEGREE: the channel is thin, not absent.")
    w.append("Three of the four are under 3:1 against the body they stand in,")
    w.append("which is a small number and now a number. **L12 is amended by")
    w.append("this table and not closed by it**: a step nobody chose is not a")
    w.append("channel a language may claim, and no ruling has said which of")
    w.append("the two readings the corpus is held to.")
    w.append("")
    w.append("WHAT THIS MEASURES AND WHAT IT DOES NOT. It measures the ratio")
    w.append("a match run keeps against the body it stands in once hue is")
    w.append("gone, which is what a greyscale monitor and a monochrome")
    w.append("printout show. It does NOT model colour vision deficiency: a")
    w.append("deuteranope does not see this image, and simulating one would")
    w.append("be a fourth instrument this programme has not built and has no")
    w.append("reader for. Written here so the number is not spent on a claim")
    w.append("it cannot support.")
    w.append("")
    return "\n".join(w) + "\n"


def check_reproducible(text: str) -> bool:
    """Re-measure in a SEPARATE PROCESS and diff the report byte for byte.

    The brief's first law -- *"the measure is deterministic"* -- taken the way
    `capture_languages` and `raster.py` take theirs, in a fresh interpreter.
    This instrument has a confound a second in-process pass would sail through
    and it is not hypothetical: `Ink` CACHES a coverage map per
    `(glyph, weight)`, so a bug that returned the previous glyph's map would be
    perfectly consistent inside one run and different in the next.
    """
    import os
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "control.txt"
        r = subprocess.run([sys.executable, "-X", "utf8",
                            str(Path(__file__).resolve()),
                            "--report-to", str(out)],
                           capture_output=True, text=True,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        if r.returncode != 0:
            raise RuntimeError(f"control run failed:\n{r.stderr[-1500:]}")
        return out.read_text(encoding="utf-8") == text


def main(argv: list[str]) -> int:
    text = report()
    if "--report-to" in argv:  # the control arm: measure, write, say nothing
        Path(argv[argv.index("--report-to") + 1]).write_text(
            text, encoding="utf-8")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    lines = text.split("\n")
    print(f"  {len(lines)} lines -> {OUT}")
    for line in lines:
        if line.startswith(("A.", "A1.", "B.", "C.", "D.", "E.", "F.", "F1.",
                            "G.", "H.")):
            print(f"    {line}")
    print("\n  re-measuring in a fresh process...")
    if not check_reproducible(text):
        print("NON-REPRODUCIBLE REPORT", file=sys.stderr)
        return 1
    print("  the report is byte-identical across two PROCESSES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
