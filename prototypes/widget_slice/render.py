"""Drawn type + meters for the aperture.

The terminal has no type scale (tui-design/HIERARCHY.md), so the hero metric is
DRAWN on a dot grid — the LED-matrix idiom, which is native to a cell grid and
cheap to animate (a 16x8 sprite is ~0.35% of a 60fps frame).

Glyph safety: only width-1 glyphs. U+25CF ● and U+25AA ▪ are East-Asian
*ambiguous* width and would break box alignment in some terminals (the codebase's
M22 trap, views.py:6-11). Block elements U+2580-259F are unambiguously narrow, so
a lit dot is a block and the DOT RHYTHM comes from a space between columns.
"""
from __future__ import annotations

ON, OFF = "█", " "          # U+2588 FULL BLOCK — unambiguous width 1

# 4 wide x 7 tall, the LED-numeral proportion
_GLYPHS = {
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
    "-": ("....", "....", "....", "####", "....", "....", "...."),
    "?": (".##.", "#..#", "...#", "..#.", ".#..", "....", ".#.."),
    "!": (".#..", ".#..", ".#..", ".#..", ".#..", "....", ".#.."),
    " ": ("....", "....", "....", "....", "....", "....", "...."),
}
ROWS = 7


DOT_W = 2        # cells per lit dot. 1 reads as a stray artifact; 2 has mass.
DOT_GAP = 1      # cells between dot columns — this is what makes it read as a
                 # MATRIX rather than as solid block type.


def dot_number(s: str, on: str = ON, off: str = OFF, gap: int = 3,
               dot_w: int = DOT_W) -> list[str]:
    """Render `s` as 7 rows of dot-matrix.

    Each lit dot is `dot_w` cells wide with a 1-cell gap between columns, so the
    numeral carries visual mass while still reading as a grid of dots. A 1-cell
    dot was tried first and rendered as a thin scratch — verified by looking at
    the output, which is the only way this class of failure shows up.
    """
    glyphs = [_GLYPHS.get(ch, _GLYPHS[" "]) for ch in s]
    out = []
    for r in range(ROWS):
        cells = []
        for g in glyphs:
            cells.append((" " * DOT_GAP).join(
                (on if c == "#" else off) * dot_w for c in g[r]))
        out.append((" " * gap).join(cells))
    return out


def dot_width(n_chars: int, gap: int = 3, dot_w: int = DOT_W) -> int:
    """Exact cell width of a dot_number render — needed for layout math."""
    per = 4 * dot_w + 3 * DOT_GAP          # 4 dot columns + 3 inter-dot gaps
    return n_chars * per + max(0, n_chars - 1) * gap


def segmented(done: int, total: int, width: int,
              on: str = "▇", off: str = "░") -> tuple[str, int]:
    """A meter drawn as N discrete blocks. Discrete is honest about the cell
    grid instead of fighting it, and it quantizes perfectly."""
    if width <= 0:
        return "", 0
    if total <= 0:
        return off * width, 0
    filled = max(0, min(width, round(width * done / total)))
    return on * filled + off * (width - filled), filled


def pulse_row(counts: list[int], width: int) -> str:
    """One row encoding relative load across buckets, at any width."""
    if not counts or width <= 0:
        return ""
    hi = max(counts) or 1
    ramp = " ▁▂▃▄▅▆▇█"
    per = max(1, width // len(counts))
    out = []
    for n in counts:
        lvl = 0 if n == 0 else max(1, round((len(ramp) - 1) * n / hi))
        out.append(ramp[lvl] * per)
    return "".join(out)[:width].ljust(width)
