"""PIXEL BASES — the same artwork, drawn on different kinds of pixel.

A dot-matrix language does not have to be made of squares. The cell can be
subdivided several ways, and each subdivision has a different pixel SHAPE, a
different resolution, and a different safety profile. Swapping the base is the
terminal's equivalent of Material's shape scale: it changes the silhouette of
the smallest mark you can make.

MEASURED East Asian Width (python `unicodedata`), because this decides whether a
base keeps the grid or breaks it in a CJK-configured terminal:

    Braille   U+2800-28FF   256/256 Neutral   <- fully safe, ROUND dots, 2x4
    Sextants  U+1FB00-1FB3B  60/60  Neutral   <- fully safe, 2x3
    Quadrants U+2596-259F     safe (Neutral)  <- safe, 2x2
    Blocks    U+2580-259F   20/32 AMBIGUOUS   <- everyone uses these anyway
    Box draw  U+2500-257F  112/128 AMBIGUOUS  <- so are most frames
    Emoji                    Wide (2 cells)   <- breaks a 1-cell grid by design

"Ambiguous" renders as 1 cell in a Western locale and 2 in a CJK one. The blocks
are therefore safe *by convention*, not by guarantee -- worth knowing before you
claim a design is width-safe.
"""
from __future__ import annotations

# --------------------------------------------------------------------------
# each base maps a bitmap (list of rows of 0/1) to terminal rows
# --------------------------------------------------------------------------
QUAD = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"      # index = tl | tr<<1 | bl<<2 | br<<3
BRAILLE_BITS = {(0, 0): 0x01, (1, 0): 0x02, (2, 0): 0x04, (3, 0): 0x40,
                (0, 1): 0x08, (1, 1): 0x10, (2, 1): 0x20, (3, 1): 0x80}
SHADES = " ░▒▓█"


def _get(bm, r, c):
    return bm[r][c] if 0 <= r < len(bm) and 0 <= c < len(bm[r]) else 0


def block(bm, on="█", off=" ") -> list[str]:
    """1x1 — one square pixel per cell. Chunkiest, lowest resolution."""
    return ["".join(on if v else off for v in row) for row in bm]


def block_wide(bm, on="██", off="  ") -> list[str]:
    """1x1 at 2 cells wide — squares the pixel, since a cell is ~2:1 tall."""
    return ["".join(on if v else off for v in row) for row in bm]


def half(bm, on="█", off=" ") -> list[str]:
    """1x2 — two stacked pixels per cell. Doubles vertical resolution."""
    out = []
    for r in range(0, len(bm), 2):
        row = []
        for c in range(len(bm[r])):
            t, b = _get(bm, r, c), _get(bm, r + 1, c)
            row.append("█" if t and b else "▀" if t else "▄" if b else off)
        out.append("".join(row))
    return out


def quadrant(bm, off=" ") -> list[str]:
    """2x2 — four pixels per cell. Safe (Neutral), squarer pixel than half."""
    out = []
    w = max(len(r) for r in bm)
    for r in range(0, len(bm), 2):
        row = []
        for c in range(0, w, 2):
            i = (_get(bm, r, c) | _get(bm, r, c + 1) << 1
                 | _get(bm, r + 1, c) << 2 | _get(bm, r + 1, c + 1) << 3)
            row.append(QUAD[i] if i else off)
        out.append("".join(row))
    return out


def braille(bm, off="⠀") -> list[str]:
    """2x4 — EIGHT ROUND dots per cell. The terminal's round pixel, the highest
    resolution available, and the only base that is 100% width-safe. Costs all
    its colour: one ink per cell."""
    out = []
    w = max(len(r) for r in bm)
    for r in range(0, len(bm), 4):
        row = []
        for c in range(0, w, 2):
            bits = 0
            for dr in range(4):
                for dc in range(2):
                    if _get(bm, r + dr, c + dc):
                        bits |= BRAILLE_BITS[(dr, dc)]
            row.append(chr(0x2800 + bits) if bits else off)
        out.append("".join(row))
    return out


def shade(bm, cell=2) -> list[str]:
    """Intensity per cell — a soft, anti-aliased pixel instead of a hard one.
    Averages a cell x cell neighbourhood into one of five shade levels."""
    out = []
    w = max(len(r) for r in bm)
    for r in range(0, len(bm), cell):
        row = []
        for c in range(0, w, cell):
            tot = sum(_get(bm, r + dr, c + dc)
                      for dr in range(cell) for dc in range(cell))
            row.append(SHADES[round(tot / (cell * cell) * (len(SHADES) - 1))])
        out.append("".join(row))
    return out


def ascii_dots(bm, ramp=" .oO@") -> list[str]:
    """Pure ASCII — survives anywhere, including a 7-bit pipe or a log file."""
    return ["".join(ramp[-1] if v else ramp[0] for v in row) for row in bm]


# --------------------------------------------------------------------------
# TWO DISPLAY-TYPE BASES. Neither is a new resolution: both take the SAME 4x7
# bitmap the other bases take and give it a different STROKE LOGIC, which is
# the axis LANGUAGES.md calls the shape scale. `block2` widens every pixel to
# two cells uniformly; these two decide, per pixel, what KIND of mark it is.
# --------------------------------------------------------------------------
SLAB_PAD = 1           # cells of air the serif feet flare into
SLAB_STEM = "█"        # a vertical: full cell, two cells wide
SLAB_HAIR_T = "▀"      # a horizontal above the waist: hugs the top of its row
SLAB_HAIR_B = "▄"      # a horizontal below it: stands on the row's baseline
SLAB_FOOT = "▄"        # the serif, half a pixel wide, on the baseline


def slab(bm, off=" ") -> list[str]:
    """THE ENGRAVED FIGURE — a bookkeeping numeral with stroke CONTRAST.

    Every other base here draws one mark for every lit pixel. This one asks
    what the pixel is FOR, which is the whole difference between a bitmap and
    a typeface:

    * a pixel with ink above or below it is part of a **stem**: two cells of
      solid block, so a vertical reads heavy;
    * a pixel with ink only beside it is a **hairline bar**: a half block, so
      a horizontal reads at half the stem's weight. In a ~1:2 cell one ROW is
      already as thick as two COLUMNS, so drawing the bar full-cell would make
      the horizontals the heaviest strokes in the figure — the opposite of a
      slab. The bar hugs the outside of the glyph (top half above the waist,
      bottom half below it), which keeps the counters as open as the mask
      allows;
    * a stem that lands on the **baseline** grows SERIF FEET: half-pixel
      flares to the left and right of its foot's run, at the baseline. This is
      the pass-35 `1`-serif made a property of the base rather than of one
      glyph — and it is why `0`, `3`, `5`, `6`, `8`, `9` get none: their bowls
      close before the baseline, so they have no stem to stand on, exactly as
      a real slab face does.

    The rows are padded one cell each side so the first glyph's left foot has
    somewhere to land.
    """
    h = len(bm)
    w = max((len(r) for r in bm), default=0)
    mid = h // 2
    out = [[off] * (2 * w + 2 * SLAB_PAD) for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if not _get(bm, r, c):
                continue
            if _get(bm, r - 1, c) or _get(bm, r + 1, c):
                g = SLAB_STEM
            else:
                g = SLAB_HAIR_T if r < mid else SLAB_HAIR_B
            out[r][SLAB_PAD + 2 * c] = g
            out[r][SLAB_PAD + 2 * c + 1] = g
    r = h - 1                                   # the baseline, and only it
    for c in range(w):
        if not (_get(bm, r, c) and _get(bm, r - 1, c)):
            continue                            # not a stem standing on it
        c0 = c
        while c0 > 0 and _get(bm, r, c0 - 1):
            c0 -= 1
        c1 = c
        while c1 + 1 < w and _get(bm, r, c1 + 1):
            c1 += 1
        for x in (SLAB_PAD + 2 * c0 - 1, SLAB_PAD + 2 * c1 + 2):
            if 0 <= x < len(out[r]) and out[r][x] == off:
                out[r][x] = SLAB_FOOT
    return ["".join(row) for row in out]


FLAP_PAD = 1           # cells of FACE beyond the glyph's own box
FLAP_GUTTER = 2        # blank bitmap columns that separate two faces
FLAP_INK = "█"         # the printed numeral, two cells wide
FLAP_SEAM_INK = "▀"    # the hinge where it crosses the numeral
FLAP_SEAM_FACE = "▔"   # the hinge where the face carries no ink


def _face_cols(bm, gutter: int = FLAP_GUTTER) -> list[tuple[int, int]]:
    """Column span of each FACE: the glyph boxes, split on the blank gutters
    `from_font` leaves between them. Inferred from the bitmap rather than
    declared, so one glyph and ten glyphs answer the same way and no caller
    has to restate the font's box width."""
    w = max((len(r) for r in bm), default=0)
    blank = [not any(_get(bm, r, c) for r in range(len(bm))) for c in range(w)]
    spans, start = [], None
    run = 0
    for c in range(w + 1):
        if c < w and blank[c]:
            run += 1
            continue
        if run >= gutter and start is not None:
            spans.append((start, c - run - 1))
            start = None
        run = 0
        if c < w and start is None:
            start = c
    if start is not None:
        spans.append((start, w - 1))
    return spans


def flap(bm, off=" ") -> list[str]:
    """THE SPLIT-FLAP CELL — a numeral printed across a card with a HINGE.

    The mark is a two-cell block, as chunky as `block2`, but the figure is cut
    at its vertical middle by a SEAM row that crosses the whole face: `▔`
    where the face is bare, `▀` where the numeral passes through it. Both
    glyphs hug the top of the seam row, so they form ONE continuous line that
    thickens over the ink — the hinge is physical, it cuts the figure, and it
    does not erase it (a seam drawn as a full rule would take the waist off
    the `8` and leave it identical to the `0`).

    The seam is a SHAPE, not a colour, which is what lets a caller that paints
    no face at all still render a flap board (COMPONENTS.md's two-channel law
    applied to the one element this base exists for).
    """
    h = len(bm)
    w = max((len(r) for r in bm), default=0)
    seam = (h - 1) // 2
    faces = _face_cols(bm)
    out = []
    for r in range(h):
        cells = [off] * (2 * w + 2 * FLAP_PAD)
        if r == seam:
            for c0, c1 in faces:
                for x in range(2 * c0, 2 * c1 + 2 * FLAP_PAD + 2):
                    if 0 <= x < len(cells):
                        cells[x] = FLAP_SEAM_FACE
        for c in range(w):
            if not _get(bm, r, c):
                continue
            g = FLAP_SEAM_INK if r == seam else FLAP_INK
            cells[FLAP_PAD + 2 * c] = g
            cells[FLAP_PAD + 2 * c + 1] = g
        out.append("".join(cells))
    return out


STENCIL_PAD = 0        # the rails hug the glyph box; nothing flares past it
ST_RAIL_W = "▌"        # the WEST rail of a cut stroke
ST_RAIL_E = "▐"        # the EAST rail
ST_EDGE_LO = "▄"       # a horizontal ABOVE the waist shows its lower edge
ST_EDGE_HI = "▀"       # ... and below the waist, its upper edge
ST_HOLLOW = ST_RAIL_W + ST_RAIL_E + ST_EDGE_LO + ST_EDGE_HI


def _outside(bm) -> set[tuple[int, int]]:
    """Every unlit cell reachable from the border (4-connectivity). What is
    NOT in this set and NOT lit is an enclosed COUNTER — the hole a stencil
    would drop on the floor without a bridge."""
    h = len(bm)
    w = max((len(r) for r in bm), default=0)
    seen: set[tuple[int, int]] = set()
    stack = [(r, c) for r in range(h) for c in (0, w - 1) if not _get(bm, r, c)]
    stack += [(r, c) for c in range(w) for r in (0, h - 1) if not _get(bm, r, c)]
    while stack:
        r, c = stack.pop()
        if (r, c) in seen or not (0 <= r < h and 0 <= c < w) or _get(bm, r, c):
            continue
        seen.add((r, c))
        stack += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    return seen


def stencil_bridges(bm) -> list[tuple[int, int]]:
    """The BRIDGE positions: one per enclosed counter, and always the ring
    pixel directly NORTH of that counter's north-west-most cell.

    A stencil is a sheet with the figure cut out of it, so a counter's island
    would fall away; the bridge is the uncut strip that holds it, and what you
    see in the paint is therefore a GAP IN THE STROKE. An outline with no gap
    is not a stencil — it is a defect a real one cannot have.

    The rule is one rule, so the gaps land in the same place on every figure
    (the NW shoulder), which is what makes them read as a property of the
    face rather than as damage to a glyph. The pixel it names is always lit
    and always in bounds: the counter's topmost row is minimal, so the cell
    above it is not in the counter, and a counter that reached the border
    would not be a counter.
    """
    h = len(bm)
    w = max((len(r) for r in bm), default=0)
    out = _outside(bm)
    todo = {(r, c) for r in range(h) for c in range(w)
            if not _get(bm, r, c) and (r, c) not in out}
    cuts = []
    while todo:
        comp: set[tuple[int, int]] = set()
        stack = [min(todo)]
        while stack:
            p = stack.pop()
            if p in comp or p not in todo:
                continue
            comp.add(p)
            r, c = p
            stack += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        todo -= comp
        r, c = min(comp)
        cuts.append((r - 1, c))
    return sorted(cuts)


def stencil(bm, off=" ", bridge: bool = True) -> list[str]:
    """THE STENCILLED DRAWING NUMBER — a HOLLOW figure, cut and bridged.

    Where `slab` asks what a pixel is for and `flap` asks what it is printed
    on, this asks what a pixel's INTERIOR is: on a drawing sheet the figure is
    the cut, so a stroke is its two edges and everything between them is
    ground. Three roles, and the last one is the whole idea:

    * a pixel with ink on all four sides is INTERIOR — it draws NOTHING. In a
      stroke thick enough to afford it (the mascot, a wide mask) that is a
      real cell of ground running down the middle of the stroke;
    * a pixel of a VERTICAL stroke draws a rail on each side that faces
      ground: `▌` west, `▐` east. At the digits' one-pixel strokes that is the
      whole stroke, so the ink hugs the two outer half-cells and a FULL
      cell-width of ground runs between them. The cut is half a cell wide
      there instead of a whole one — the honest reading, and it is the same
      shape of fact as flap's hinge, which is drawn face rather than ink;
    * everything else — a horizontal run, and the side of a stem that has
      ink beside it — draws the row's RAIL: one edge, `▄` above the waist and
      `▀` below it. One edge and not two, because a row is a single cell tall
      and no glyph carries ink at its top AND its bottom with ground between:
      that is the row budget's cost, stated rather than hidden. WHICH edge is
      not a preference. It is the counter-facing one, the inverse of `slab`'s
      rule, and it is what makes the figure CLOSE: the rail lands against the
      stem rails that continue the outline. Hugging the outside instead leaves
      half a cell of ground at every corner and the outline falls apart.

    Nothing this base draws is a solid block, and nothing it draws is a
    box-drawing codepoint — which is not decoration either. Blueprint's own
    law allows the sheet exactly ten box glyphs, none of them a vertical
    stroke or a junction, so a display type built out of `║` and `╬` would
    break the language it was drawn for. The half-block family is what is
    left, and it is enough.
    """
    h = len(bm)
    w = max((len(r) for r in bm), default=0)
    mid = h // 2
    grid = [[_get(bm, r, c) for c in range(w)] for r in range(h)]
    for r, c in (stencil_bridges(grid) if bridge else []):
        grid[r][c] = 0

    def lit(r, c) -> int:
        return 1 if 0 <= r < h and 0 <= c < w and grid[r][c] else 0

    out = []
    for r in range(h):
        cells = [off] * (2 * w + 2 * STENCIL_PAD)
        for c in range(w):
            if not lit(r, c):
                continue
            n, s, e, wst = lit(r - 1, c), lit(r + 1, c), lit(r, c + 1), lit(r, c - 1)
            if n and s and e and wst:
                continue                                   # INTERIOR: the cut
            rail = ST_EDGE_LO if r < mid else ST_EDGE_HI
            vert = n or s
            x = STENCIL_PAD + 2 * c
            cells[x] = ST_RAIL_W if (vert and not wst) else rail
            cells[x + 1] = ST_RAIL_E if (vert and not e) else rail
        out.append("".join(cells))
    return out


BASES = {
    "block":     dict(fn=block,      sub=(1, 1), colors="1 fg", eaw="ambiguous",
                      shape="square", note="chunkiest; one pixel per cell"),
    "block2":    dict(fn=block_wide, sub=(1, 1), colors="1 fg", eaw="ambiguous",
                      shape="square (2 cells)", note="corrects the 2:1 cell aspect"),
    "half":      dict(fn=half,       sub=(1, 2), colors="2 (fg+bg)", eaw="ambiguous",
                      shape="tall rect", note="2x vertical res, keeps 2 colours"),
    "quadrant":  dict(fn=quadrant,   sub=(2, 2), colors="1 fg", eaw="SAFE",
                      shape="square", note="4x density, width-safe"),
    "braille":   dict(fn=braille,    sub=(2, 4), colors="1 fg", eaw="SAFE",
                      shape="ROUND", note="8 round dots/cell; max res; one ink"),
    "shade":     dict(fn=shade,      sub=(2, 2), colors="1 fg", eaw="ambiguous",
                      shape="soft", note="anti-aliased; 5 intensity levels"),
    "ascii":     dict(fn=ascii_dots, sub=(1, 1), colors="1 fg", eaw="SAFE",
                      shape="glyph", note="survives anywhere, even a log file"),
    "slab":      dict(fn=slab,       sub=(1, 1), colors="1 fg", eaw="ambiguous",
                      shape="STEM+HAIRLINE", note="engraved figure; serif feet"),
    "flap":      dict(fn=flap,       sub=(1, 1), colors="1 fg", eaw="ambiguous",
                      shape="CARD (hinged)", note="split-flap cell; seam cuts it"),
    "stencil":   dict(fn=stencil,    sub=(1, 1), colors="1 fg", eaw="ambiguous",
                      shape="HOLLOW (bridged)", note="cut figure; rails + bridges"),
}


def render(bm, base: str, **kw) -> list[str]:
    return BASES[base]["fn"](bm, **kw)


# --------------------------------------------------------------------------
# bitmap sources
# --------------------------------------------------------------------------
def from_font(text: str, font: dict, gap: int = 1) -> list[list[int]]:
    """Turn dot-font glyph masks into a bitmap the bases can consume."""
    glyphs = [font.get(c, font[" "]) for c in text]
    rows = len(glyphs[0])
    out = []
    for r in range(rows):
        row = []
        for gi, g in enumerate(glyphs):
            if gi:
                row += [0] * gap
            row += [1 if ch == "#" else 0 for ch in g[r]]
        out.append(row)
    return out


def wave(width: int, height: int, phase: float = 0.0) -> list[list[int]]:
    """A dot-lattice waveform — the equaliser motif, as a bitmap."""
    import math
    out = []
    amp = [0.15 + 0.85 * abs(math.sin(x * 0.30 + phase)) for x in range(width)]
    for r in range(height):
        row = []
        for c in range(width):
            lit = (height - r) / height <= amp[c]
            row.append(1 if lit else 0)
        out.append(row)
    return out


# --------------------------------------------------------------------------
# SEVEN-SEGMENT — the instrument-panel numeral. A base in its own right: the
# mark is a BAR, not a dot, which is why an LCD reads as machinery rather than
# as pixel art.
# --------------------------------------------------------------------------
_SEG = {           # a b c d e f g
    "0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
    "5": "afgcd", "6": "afgecd", "7": "abc", "8": "abcdefg", "9": "abcdfg",
    "-": "g", " ": "", "?": "abge",
}


def seven_seg(text: str, on: str = "██", bar: str = "▄", low: str = "▀",
              off: str = " ", w: int = 6, ghost: bool = True,
              g_on: str = "▒▒", g_bar: str = "░") -> list[str]:
    """7 rows of LCD numerals, with GHOST segments.

    A real LCD shows its unlit segments faintly, and that is not decoration --
    it is what keeps the digit legible. Without ghosts a '1' renders as two
    disconnected blobs, because the blank a- and g-rows cut the vertical stroke
    in half. Two earlier versions of this function shipped that bug (and one
    docstring claimed it was fixed while it wasn't).

    It is the same idea as Naught's visible lattice: the OFF state is drawn, so
    the silhouette survives and the panel reads as a device.
    """
    rows = [""] * 7
    inner = max(2, w - 4)
    G = (lambda lit, s_on, s_off: s_on if lit else (s_off if ghost else off * len(s_on)))
    for i, ch in enumerate(text):
        s = _SEG.get(ch, "")
        if i:
            rows = [r + "  " for r in rows]
        pad = " " * inner
        rows[0] += ("  " + G("a" in s, bar * inner, g_bar * inner) + "  ")
        vt = (G("f" in s, on, g_on) + pad + G("b" in s, on, g_on))
        rows[1] += vt
        rows[2] += vt
        rows[3] += ("  " + G("g" in s, bar * inner, g_bar * inner) + "  ")
        vb = (G("e" in s, on, g_on) + pad + G("c" in s, on, g_on))
        rows[4] += vb
        rows[5] += vb
        rows[6] += ("  " + G("d" in s, low * inner, g_bar * inner) + "  ")
    return rows


BASES["segment"] = dict(fn=None, sub=(1, 1), colors="1 fg", eaw="ambiguous",
                        shape="BAR (LCD)", note="instrument numerals; bars not dots")


def scale(bm, sx: int = 1, sy: int = 1) -> list[list[int]]:
    """Pixel-replicate a bitmap. Required before a DENSE base: a 4x7 glyph
    pushed through braille (2x4) is 2 rows of mush -- the base must match the
    source resolution (LANGUAGES.md). Scaling first lets every base produce a
    comparably sized mark, which is what makes the base a real design axis
    rather than a resolution accident."""
    out = []
    for row in bm:
        big = [v for v in row for _ in range(sx)]
        for _ in range(sy):
            out.append(list(big))
    return out


# Scale factors are deliberately NOT exact multiples of each base's sub-grid.
# Scaling by exactly the sub-grid cancels it out and every base returns the
# identical shape -- only the glyph changes, which is a recolour in glyph space.
# Over-scaling makes edges fall on PARTIAL sub-cells, so each base contributes
# its own texture: quadrant fragments, braille's rounder curve, shade's
# intermediate levels. Verified by rendering the same numeral through each.
BASE_SCALE = {"block": (1, 1), "block2": (1, 1), "ascii": (1, 1),
              "half": (2, 3), "quadrant": (3, 3), "shade": (3, 3),
              "braille": (3, 5), "slab": (1, 1), "flap": (1, 1),
              "stencil": (1, 1)}

# THE INTER-GLYPH GAP is a property of the BASE, not of the caller. `slab`
# flares a serif foot half a pixel past its stem and `flap` needs bare ground
# between two faces, so both want two blank columns where the dot bases want
# one. Declared here because both call sites — taskboard/hero.py and the
# widget-slice prototype — reach the bases through `draw_numeral` and neither
# knows what a serif is.
BASE_GAP = {"slab": 2, "flap": 2, "stencil": 2}

# THE TABULAR `1`, and the reason it is declared here rather than in the font.
# HERO_FONT's `1` inks 3 of the 4 columns it advances, which is a visual
# aspect of 0.43 at 7 rows — under the 0.55 floor the drawn-type laws hold
# every digit to (PENDING, thirty-fifth pass). Both bases below draw a figure
# whose BOX is the unit (an engraved stem standing on the baseline, a flap
# face), so the `1` takes a full-width base bar and fills the box it already
# advanced. The font itself is shared with instrument and nord, whose heroes
# must not move, so the correction is per-base.
BASE_GLYPH = {
    "slab": {"1": ("..#.", ".##.", "..#.", "..#.", "..#.", "..#.", "####")},
    "flap": {"1": ("..#.", ".##.", "..#.", "..#.", "..#.", "..#.", "####")},
    "stencil": {"1": ("..#.", ".##.", "..#.", "..#.", "..#.", "..#.", "####")},
}


def draw_numeral(text: str, base: str, font: dict, gap: int = 1) -> list[str]:
    """Render a numeral through ANY base at a comparable visual size."""
    if base == "segment":
        return seven_seg(text)
    font = {**font, **BASE_GLYPH[base]} if base in BASE_GLYPH else font
    gap = BASE_GAP.get(base, gap)
    sx, sy = BASE_SCALE.get(base, (1, 1))
    bm = scale(from_font(text, font, gap=gap), sx, sy)
    return render(bm, base)


def flap_faces(text: str, font: dict) -> list[tuple[int, int]]:
    """Inclusive CELL span of each flap face, for a caller that paints the
    face's ground. Reads the same bitmap `draw_numeral` renders, so the
    ground a caller paints and the seam the base draws cannot disagree."""
    bm = from_font(text, {**font, **BASE_GLYPH.get("flap", {})},
                   gap=BASE_GAP.get("flap", 1))
    return [(2 * c0, 2 * c1 + 2 * FLAP_PAD + 1) for c0, c1 in _face_cols(bm)]


def flap_seam(rows: int) -> int:
    """Index of the hinge row in a `flap` render of `rows` rows."""
    return (rows - 1) // 2
