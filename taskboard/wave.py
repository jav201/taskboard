"""The braille dot engine — everything at 2x4 sub-cell resolution.

A PURE module: no Textual, no rich, no view, no board. It knows dots and how to
pack them into braille characters, nothing else. Later increments draw with it;
it never draws for them.

Every figure is built as a DOT BITMAP (2 dot-columns and 4 dot-rows per cell)
and packed into braille only at the last step. Two consequences, and they are
the reason the engine exists:

  * the LEFT and RIGHT halves of one cell may differ, so a boundary lands at
    HALF-CELL precision and a wave reads as a wave, not as a bar chart;
  * a figure is CARVED — dots removed from a solid field — so each cell is
    field or figure and never both, which satisfies the two-colours-per-cell
    law by composition instead of policing it afterwards.

Ported unchanged (API and semantics) from `_tui_prism_proposal/wave.py` REV2,
which took it in turn from the tui-design skill's `assets/pixel_bases.py`. REV1
lit whole braille ROWS, so a cell carried one value and a drawn edge was a
staircase one cell wide; `tests/test_wave.py` pins the difference by counting
cells whose two dot-columns disagree — a whole-row fill scores zero.
"""
from __future__ import annotations

# dot (row, col) -> bit, for the 2x4 braille cell
BRAILLE_BITS = {(0, 0): 0x01, (1, 0): 0x02, (2, 0): 0x04, (3, 0): 0x40,
                (0, 1): 0x08, (1, 1): 0x10, (2, 1): 0x20, (3, 1): 0x80}

DOT_COLS = 2          # dot columns per cell — the horizontal resolution gain
DOT_ROWS = 4          # dot rows per cell

FONT_4x7 = {
    "0": (".##.", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."),
    "1": ("..#.", ".##.", "..#.", "..#.", "..#.", "..#.", ".###"),
    "2": (".##.", "#..#", "...#", "..#.", ".#..", "#...", "####"),
    "3": ("####", "...#", "..#.", ".##.", "...#", "#..#", ".##."),
    "4": ("...#", "..##", ".#.#", "#..#", "####", "...#", "...#"),
    "5": ("####", "#...", "###.", "...#", "...#", "#..#", ".##."),
    "6": (".##.", "#...", "#...", "###.", "#..#", "#..#", ".##."),
    "7": ("####", "...#", "..#.", "..#.", ".#..", ".#..", ".#.."),
    "8": (".##.", "#..#", "#..#", ".##.", "#..#", "#..#", ".##."),
    "9": (".##.", "#..#", "#..#", ".###", "...#", "...#", ".##."),
    " ": ("....", "....", "....", "....", "....", "....", "...."),
}


class Bitmap:
    """A dot grid.  Origin top-left; `fill_to` works from the BOTTOM up, which
    is what a load curve is."""

    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.px = [[0] * w for _ in range(h)]

    def fill_to(self, x: int, height: int) -> None:
        """Light `height` dots at column x, from the bottom."""
        if not (0 <= x < self.w):
            return
        for k in range(max(0, min(self.h, height))):
            self.px[self.h - 1 - k][x] = 1

    def carve_col(self, x: int) -> None:
        """Remove a whole dot column — the today boundary as an ABSENCE."""
        if 0 <= x < self.w:
            for r in range(self.h):
                self.px[r][x] = 0

    def carve_notch(self, x: int, depth: int = 2) -> None:
        """Bite dots off the TOP of column x's ink — a day that fell due and did
        not land.  The bite is CAPPED so it can never erase the column: at one
        cell tall a 2-dot notch removed the whole 2-dot curve and two projects'
        waves disappeared entirely.  A carve is a figure cut from a field; with
        no field left it is not a carve, it is a deletion."""
        if not (0 <= x < self.w):
            return
        lit = [r for r in range(self.h) if self.px[r][x]]
        if len(lit) <= 1:
            return
        for r in lit[:max(1, min(depth, len(lit) - 1))]:
            self.px[r][x] = 0

    def carve_text(self, text: str, x: int, y: int) -> tuple[int, int]:
        """Carve digits OUT of the field.  Returns the (w, h) it occupied so a
        caller can check the figure actually had field to be carved from."""
        gw = 0
        for i, ch in enumerate(text):
            g = FONT_4x7.get(ch, FONT_4x7[" "])
            for r, line in enumerate(g):
                for c, px in enumerate(line):
                    if px == "#":
                        xx, yy = x + gw + c, y + r
                        if 0 <= xx < self.w and 0 <= yy < self.h:
                            self.px[yy][xx] = 0
            gw += len(g[0]) + 1
        return gw, 7

    def ink_at(self, x: int) -> int:
        return sum(self.px[r][x] for r in range(self.h)) if 0 <= x < self.w else 0

    def lit(self) -> int:
        return sum(sum(r) for r in self.px)

    def to_braille(self) -> list[list[str]]:
        """Pack to cells: (h/4) rows of (w/2) braille chars.  A cell with no
        dots comes back as ' ' so the caller can decide what the unlit ground
        is — the field's own lattice, not a void."""
        out = []
        for r0 in range(0, self.h, DOT_ROWS):
            row = []
            for c0 in range(0, self.w, DOT_COLS):
                bits = 0
                for dr in range(DOT_ROWS):
                    for dc in range(DOT_COLS):
                        r, c = r0 + dr, c0 + dc
                        if r < self.h and c < self.w and self.px[r][c]:
                            bits |= BRAILLE_BITS[(dr, dc)]
                row.append(chr(0x2800 + bits) if bits else " ")
            out.append(row)
        return out


def load_curve(bm: Bitmap, steps: list[int], total: int, edge: int) -> None:
    """Draw a cumulative load curve into `bm`.

    `steps[x]` is how many items are due on or before day x; `total` is the
    STABLE denominator (the project's whole task set, never its shrinking open
    count — REV1 normalised to the open count and painted MORE ink at half the
    load, which the 90/50/10 render-and-count caught).  `edge` is the last day
    the curve may occupy: the project's own due date.  Beyond it the bank stops,
    so a plateau can never run off to the right edge saying nothing.
    """
    for x in range(bm.w):
        if x > edge:
            continue
        v = steps[x] if x < len(steps) else 0
        if v:
            bm.fill_to(x, max(1, round(bm.h * v / max(1, total))))
