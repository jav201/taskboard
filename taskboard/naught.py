"""NAUGHT — a dot-matrix language drawn broadly from Nothing OS.

What separates it from a generic "dots + one accent" look, and what the earlier
`instrument` language left out:

* **The unlit grid is visible.** On an LED panel you see the dark dots too. That
  faint background lattice is the signature; without it you have block type that
  happens to be sparse.
* **Labels are drawn too**, not just numerals — a dot alphabet with PER-GLYPH
  metrics (letters on a 3-column box, tabular digits on a 4-column one), so the
  whole surface lives on one grid instead of mixing drawn numbers with cell text.
* **Quantity is a row of discrete dots**, lit and unlit, never a filled bar.
* **Monochrome first; red is RATIONED** — Nothing spends red on ~8 of ~70
  widgets per sheet (REC, over-limit, permissions, alarm states). Decorative
  red was the measured defect here: 70 accent hits in one kit surface
  (user verdict 2026-07-26: "unsettling"). Red now = alarm + focus only.
* **The pixel is ROUND.** Nothing's matrix is small circular dots with air
  between them, never square slabs.

Glyph safety (MEASURED via unicodedata.east_asian_width): the round pair
U+2219 BULLET OPERATOR '∙' and U+25E6 WHITE BULLET '◦' are both **Neutral**
— safer than the block elements they replace (U+2588/U+2591 are Ambiguous,
1-cell by convention only). U+2022/U+00B7/U+25CF are Ambiguous — rejected.
"""
from __future__ import annotations

from taskboard import bases as BS

ON, OFF = "∙", "◦"

# The SECOND dot scale (Nothing mixes large structure dots with small data
# dots — the step counter's tiny rows). Braille dots are round AND sub-cell:
# a column of 0-3 small dots per cell. Distinct from instrument's idiom
# (continuous 2-wide fills ⣀⣤⣿); naught's fine dots stay a SINGLE sparse
# column. All braille is measured EAW-Neutral.
FINE = ("⠂", "⡀", "⡄", "⡇")   # lattice mark · 1 · 2 · 3 sub-dots

# --------------------------------------------------------------------------
# THE METRIC-BEARING ALPHABET
#
# Not a uniform 3x5 box any more. Each glyph declares its own BOX by the width
# of its mask, and the metrics table below is MEASURED off those masks — ink
# extent and advance per glyph, row height derived from the tallest inked row.
#
# Why, measured rather than argued (Bodmer, Font16 as the reference):
#
# * A terminal cell is ~1:2, so a glyph N columns wide by M rows has a visual
#   aspect of N/(2M). The old 3x5 box at the dense standard (sx=2) gives 0.60
#   against Font16's 0.70 — narrow, and the narrowness lands on the COUNTER.
# * At 3 columns a closed glyph's counter is ONE column: 2 cells of a 6-cell
#   glyph at sx=2, 33% of the ink width, against the reference's 71%. Counters
#   are where legibility dies, and integer scaling can never widen one — it
#   multiplies stroke and counter together.
# * So the DIGITS are drawn on a 4-column box: at sx=2 the counter is 4 cells
#   of 8, 50%. Letters stay on 3 (this alphabet's captions are the width
#   budget every drawn-title seat is measured against).
# * ALL TEN DIGITS SHARE ONE ADVANCE, including the `1`, whose ink is 3 wide
#   inside a 4-wide box. That is TABULAR figures — Font16 does exactly this,
#   proportional text with monospaced digits — and it is what a per-glyph
#   table buys that a scale factor cannot: a count that changes from 1 to 8
#   does not move a single cell of the field.
# * Punctuation takes a NARROWER advance than a digit (the period's box is 2
#   columns), so the table is a real table and not a constant in disguise.
GLYPH_GAP = 1          # lattice columns of air between two glyph boxes

_ALPHA = {
    "A": (".#.", "#.#", "###", "#.#", "#.#"),
    "B": ("##.", "#.#", "##.", "#.#", "##."),
    "C": (".##", "#..", "#..", "#..", ".##"),
    "D": ("##.", "#.#", "#.#", "#.#", "##."),
    "E": ("###", "#..", "##.", "#..", "###"),
    "F": ("###", "#..", "##.", "#..", "#.."),
    "G": (".##", "#..", "#.#", "#.#", ".##"),
    "H": ("#.#", "#.#", "###", "#.#", "#.#"),
    "I": ("###", ".#.", ".#.", ".#.", "###"),
    "J": ("..#", "..#", "..#", "#.#", ".#."),
    "K": ("#.#", "#.#", "##.", "#.#", "#.#"),
    "L": ("#..", "#..", "#..", "#..", "###"),
    "M": ("#.#", "###", "###", "#.#", "#.#"),
    "N": ("#.#", "##.", "#.#", ".##", "#.#"),
    "O": (".#.", "#.#", "#.#", "#.#", ".#."),
    "P": ("##.", "#.#", "##.", "#..", "#.."),
    "Q": (".#.", "#.#", "#.#", "##.", ".##"),
    "R": ("##.", "#.#", "##.", "#.#", "#.#"),
    "S": (".##", "#..", ".#.", "..#", "##."),
    "T": ("###", ".#.", ".#.", ".#.", ".#."),
    "U": ("#.#", "#.#", "#.#", "#.#", ".#."),
    "V": ("#.#", "#.#", "#.#", ".#.", ".#."),
    "W": ("#.#", "#.#", "###", "###", "#.#"),
    "X": ("#.#", "#.#", ".#.", "#.#", "#.#"),
    "Y": ("#.#", "#.#", ".#.", ".#.", ".#."),
    "Z": ("###", "..#", ".#.", "#..", "###"),
    # THE NUMERALS — one 4-column box each, one shared advance. The closed
    # counters (0 4 6 8 9) are two columns wide, which is 50% of the ink at
    # the sx=2 dense standard; the `1` keeps its flag and its BASE SERIF (a
    # bare stem reads as a rule, not a figure) on 3 columns of ink inside the
    # same 4-column box, so it steps like its siblings without looking fat.
    "0": (".##.", "#..#", "#..#", "#..#", ".##."),
    "1": (".#..", "##..", ".#..", ".#..", "###."),
    "2": (".##.", "#..#", "..#.", ".#..", "####"),
    "3": ("###.", "...#", ".##.", "...#", "###."),
    "4": ("#..#", "#..#", "####", "...#", "...#"),
    "5": ("####", "#...", "###.", "...#", "###."),
    "6": (".##.", "#...", "###.", "#..#", ".##."),
    "7": ("####", "...#", "..#.", ".#..", ".#.."),
    "8": (".##.", "#..#", ".##.", "#..#", ".##."),
    "9": (".##.", "#..#", ".###", "...#", ".##."),
    "-": ("...", "...", "###", "...", "..."),
    "?": ("###", "..#", ".#.", "...", ".#."),
    "!": (".#.", ".#.", ".#.", "...", ".#."),
    " ": ("...", "...", "...", "...", "..."),
    # narrow punctuation: a period is a dot, and it is not owed a digit's box
    ".": ("..", "..", "..", "..", "#."),
}


def _metrics(font: dict, gap: int = GLYPH_GAP) -> dict:
    """`{glyph: (ink_rows, ink_cols, advance)}`, MEASURED off the masks.

    `ink_rows` / `ink_cols` are the extent of the lit pixels; `advance` is the
    glyph's own box plus the inter-glyph gap — the distance from this glyph's
    origin to the next one's. Ink and advance are separate numbers on purpose:
    the `1` inks 3 columns and advances 5, which is what keeps the numerals
    tabular, and it is the one thing a uniform box cannot say.
    """
    out = {}
    for ch, mask in font.items():
        lit = [(r, c) for r, row in enumerate(mask)
               for c, v in enumerate(row) if v == "#"]
        rs = [r for r, _ in lit]
        cs = [c for _, c in lit]
        out[ch] = (max(rs) - min(rs) + 1 if lit else 0,
                   max(cs) - min(cs) + 1 if lit else 0,
                   len(mask[0]) + gap)
    return out


METRICS = _metrics(_ALPHA)

# DERIVED, not declared: the raster is exactly as tall as the tallest inked
# row in the set. A declared constant is a second source of truth that a new
# glyph can silently contradict.
ALPHA_ROWS = max((r + 1 for mask in _ALPHA.values()
                  for r, row in enumerate(mask) if "#" in row), default=0)


def advance(ch: str) -> int:
    """Columns from this glyph's origin to the next glyph's. Every digit
    answers the same number — that IS the tabular contract."""
    return METRICS.get(ch.upper(), METRICS[" "])[2]


def _runs(mask_row: str, on_c: str, off_c: str, dot_w: int,
          gap: int = 1) -> str:
    """Group consecutive lit/unlit cells into markup runs, so the UNLIT lattice
    renders in its own colour instead of disappearing into spaces. `gap` is
    the lattice PITCH: cells of air between dots (0 = dense LED panel — round
    glyphs carry their own air, so adjacency stays legible)."""
    out, i = [], 0
    while i < len(mask_row):
        ch = mask_row[i]
        j = i
        while j < len(mask_row) and mask_row[j] == ch:
            j += 1
        n = j - i
        cell = ((ON if ch == "#" else OFF) * dot_w + " " * gap) * n
        cell = cell[: len(cell) - gap] if gap else cell
        out.append(f"[{on_c if ch == '#' else off_c}]{cell}[/]")
        i = j
    return (" " * gap).join(out) if gap else "".join(out)


def label(text: str, on_c: str, off_c: str, dot_w: int = 1,
          gap: int = 1, sx: int = 1, fill: bool = False) -> list[str]:
    """A dot-drawn uppercase caption — 5 rows, unlit lattice visible.

    Two forms, and the second is the cure for a MEASURED defect. The default
    (`sx=1, fill=False`) draws one cell per pixel and parts the letters with a
    BLANK cell, so every stroke is a single cell in a 1:2 aspect — user verdict
    2026-07-27: the drawn letters were "hard to read, somewhat separated".

    `fill=True` puts the word on the CONTINUOUS lattice instead: the letters
    are parted by unlit dots rather than by void, and no cell of the band is a
    plain space. `sx` is the horizontal pixel — at 2 every stroke is two cells
    wide, which gives the cell's aspect back. Same mechanism the hero's
    `hero.dense_type` draws through, so the two seats cannot fork.
    """
    if sx == 1 and not fill:
        glyphs = [_ALPHA.get(c, _ALPHA[" "]) for c in text.upper()]
        sep = " " * max(1, gap + 1)         # letters always keep separation
        rows = []
        for r in range(ALPHA_ROWS):
            rows.append(sep.join(_runs(g[r], on_c, off_c, dot_w, gap)
                                 for g in glyphs))
        return rows
    sprite = BS.scale(BS.from_font(text.upper(), _ALPHA, gap=GLYPH_GAP), sx, 1)
    return field(plain_width(text, dot_w, gap, sx, fill), ALPHA_ROWS, sprite,
                 on_c, off_c, dot_w=dot_w, gap=gap, ox=0)


def numeral(s: str, on_c: str, off_c: str, font, dot_w: int = 2,
            gap: int = 3) -> list[str]:
    """The hero numeral on a visible lattice, using the 4x7 font from render.py."""
    glyphs = [font.get(c, font[" "]) for c in s]
    rows = []
    for r in range(7):
        rows.append((" " * gap).join(
            _runs(g[r], on_c, off_c, dot_w) for g in glyphs))
    return rows


def dot_meter(done: int, total: int, cells: int, on_c: str, off_c: str,
              gap: int = 1) -> str:
    """Quantity as discrete lit dots on a visible lattice — never a filled bar."""
    if cells <= 0:
        return ""
    n = 0 if total <= 0 else max(0, min(cells, round(cells * done / total)))
    lit = (ON + " " * gap) * n
    dark = (OFF + " " * gap) * (cells - n)
    return f"[{on_c}]{lit.rstrip()}[/] [{off_c}]{dark.rstrip()}[/]"


def dot_heat(counts: list[int], cells: int, on_c: str, mid_c: str,
             off_c: str, gap: int = 1) -> str:
    """The Nothing 'Progress' card idiom, on the FINE dot scale: intensity is
    the COUNT of sub-cell dots (0-3 per cell) — denser pixels for data, the
    large lattice stays for structure."""
    if not counts or cells <= 0:
        return ""
    hi = max(counts) or 1
    per = max(1, cells // len(counts))
    out = []
    for n in counts:
        frac = n / hi
        lvl = 3 if frac > 0.66 else (2 if frac > 0.33 else (1 if frac > 0 else 0))
        col = on_c if lvl >= 3 else (mid_c if lvl else off_c)
        out.append(f"[{col}]{(FINE[lvl] + ' ' * gap) * per}[/]")
    return "".join(out)


def plain_width(text: str, dot_w: int = 1, gap: int = 1, sx: int = 1,
                fill: bool = False) -> int:
    """Visible cell width of a dot-drawn label (markup excluded). The `sx` and
    `fill` arguments mean what they mean in `label`.

    Both forms read the SAME metrics table, so the answer stays true now that
    a glyph's advance is its own: a digit steps 5 columns, a letter 4, the
    period 3. The old form multiplied a constant 4 by the character count,
    which was exact only while every glyph shared one box."""
    text = text.upper()
    if sx == 1 and not fill:
        cells = sum(max(0, (advance(ch) - GLYPH_GAP) * (dot_w + gap) - gap)
                    for ch in text)
        return cells + max(0, len(text) - 1) * max(1, gap + 1)
    cols = sx * (sum(advance(ch) for ch in text) - GLYPH_GAP)
    return max(0, cols * (dot_w + gap) - gap)


def field(width: int, rows: int, sprite: list[list[int]], on_c: str, off_c: str,
          dot_w: int = 2, gap: int = 1, ox: int | None = None, oy: int = 0
          ) -> list[str]:
    """A FULL-BLEED lattice: the unlit grid spans the whole region edge to edge,
    with the sprite lit on top of it.

    This is what separates an LED panel from "text with a dotty number". The
    earlier version drew the unlit grid only inside the glyph's bounding box, so
    a 12-column lattice floated in 106 columns of void — the surface read as
    text, and 77% of it was blank. On a real panel the dark dots cover the whole
    device.

    Cost: glyph detail only, i.e. the cheap axis (BUDGET.md). The lattice is
    rebuilt per resize, not per tick.
    """
    per = dot_w + gap
    cols = max(1, (width + gap) // per)
    sh = len(sprite)
    sw = max((len(r) for r in sprite), default=0)
    if ox is None:
        ox = max(0, (cols - sw) // 2)
    out = []
    for r in range(rows):
        runs, cur, start = [], None, 0
        for c in range(cols):
            sr, sc = r - oy, c - ox
            lit = (0 <= sr < sh and 0 <= sc < len(sprite[sr])
                   and sprite[sr][sc] == 1)
            if lit != cur:
                if cur is not None:
                    runs.append((cur, c - start))
                cur, start = lit, c
        runs.append((cur, cols - start))
        line = "".join(
            f"[{on_c if lit else off_c}]"
            f"{((ON if lit else OFF) * dot_w + ' ' * gap) * n}[/]"
            for lit, n in runs)
        out.append(line.rstrip())
    return out
