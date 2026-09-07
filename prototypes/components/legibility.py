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
    h("E. A FLOOR TO PROPOSE, NOT TO ENFORCE")
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
    w.append("WHY IT IS NOT ENFORCED HERE. Three reasons and they are not")
    w.append("excuses:")
    w.append("")
    w.append("  1. The product has no published precedent. WCAG 1.4.3 is a")
    w.append("     ratio and 1.4.11 is a ratio; nothing in either standard")
    w.append("     multiplies by area. A floor invented inside an increment")
    w.append("     and asserted in the same increment is a number nobody")
    w.append("     argued with.")
    w.append("  2. Half of what it would fail is DECORATION, and this file")
    w.append("     cannot tell which half. That is round four's §8.4 verbatim")
    w.append("     and inc74's `DIM_CLASSIFIES` is the shape the answer takes")
    w.append("     -- a seat list with verdicts, written by somebody who")
    w.append("     decides, not a threshold.")
    w.append("  3. The face is not the terminal. Windows Terminal draws its")
    w.append("     own box and block glyphs, so every row here whose glyph is")
    w.append("     box drawing is a number about Cascadia's version of it.")
    w.append("")
    w.append("WHAT A RULING WOULD NEED TO SAY, in one line each:")
    w.append("")
    w.append("  - is coverage x effective the measure, or coverage AND")
    w.append("    effective as two clauses with two floors?")
    w.append("  - does it bind every meaning mark, or only the ones a")
    w.append("    `DIM_CLASSIFIES`-shaped list says classify?")
    w.append("  - is a mark judged at its worst seat or at its declared one?")
    w.append("    Section D reports the worst; the answer changes which kits")
    w.append("    are in the top ten.")
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
        if line.startswith(("A.", "A1.", "B.", "C.", "D.", "E.")):
            print(f"    {line}")
    print("\n  re-measuring in a fresh process...")
    if not check_reproducible(text):
        print("NON-REPRODUCIBLE REPORT", file=sys.stderr)
        return 1
    print("  the report is byte-identical across two PROCESSES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
