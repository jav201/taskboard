"""raster.py -- the PIXEL side of the `surface` axis.

WHAT THIS IS.  `language.py` owns the postures (what a language DOES when a
region can be real pixels); this file owns the arithmetic they all share --
resampling into a cell rectangle, the half-block glyph pass, an ordered
dither, and the duotone ramps a tint posture applies.  Nothing here knows what
a Kit is, and nothing here decides anything: a mechanism that lived in this
file would be a mechanism no token dispatches, which is the failure the whole
batch exists to avoid (LANGUAGES.md, "a language definition is code").

PIL ONLY, ON PURPOSE.  `pyproject.toml` declares pillow and textual-image;
it does NOT declare numpy.  The test image is a `.npy` grid, but the loading
of it belongs to `prototypes/`, which is dev-side and may import anything.
The shipped package stays on its declared dependencies.

TWO SURFACES, ONE POSTURE (AC-3).  Every posture must render on the glyph side
(any terminal) and, where a raster transport exists, through `textual_image`
with the SAME posture applied to the pixels.  So the functions below come in
pairs: one that returns markup rows, one that returns a `PIL.Image` -- and a
posture applies its pixel transform FIRST, then draws both sides off the
transformed image, so the two sides cannot drift.

THE TRANSPORT IS DETECTED AT MODULE LOAD, and that is not a style choice.
`textual_image` decides which protocol the terminal speaks by QUERYING the
terminal, which only works before Textual seizes it -- the same reason
`modals.py` imports its widget at module scope with a comment saying so.  A
lazy import inside a render would run after app start, detection would fail,
and the region would silently fall back to half-cells while claiming a raster
transport.  This module reuses that path rather than opening a second one.
"""
from __future__ import annotations

from PIL import Image, ImageOps

try:                                    # see the module docstring: NOT lazy
    from textual_image.widget import Image as AutoImage
    from textual_image.renderable import Image as _Chosen
    from textual_image.renderable.sixel import Image as _Sixel
    from textual_image.renderable.tgp import Image as _TGP
except Exception:                       # pragma: no cover - declared dependency
    AutoImage = _Chosen = _Sixel = _TGP = None

# WHICH transport the library picked for THIS terminal, decided at its import
# (`textual_image.widget` calls `get_cell_size()` at module scope for exactly
# that reason).  Sixel and TGP are real pixels; halfcell and unicode are the
# glyph path wearing the library's name -- which is why "a widget exists" is
# not the question `raster_available()` answers.
TRANSPORT = {None: "none", _Sixel: "sixel", _TGP: "tgp"}.get(_Chosen, "glyph")

# ORDERED 4x4 BAYER, in 1/16ths.  An ordered dither and not Floyd-Steinberg:
# error diffusion is content-dependent and therefore not reproducible cell for
# cell across a resize, and every capture in this repo is a byte-comparison.
BAYER4 = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))

HALF = "▀"                         # UPPER HALF BLOCK: fg is the top pixel


def raster_available() -> bool:
    """True when `textual_image` reported a real graphics transport.

    Honest by construction: it reads the renderable `textual_image` itself
    selected, the same one `modals.image_block` renders through.  On a
    terminal with no transport the library still gives a widget -- one that
    draws half-cells -- so "a widget exists" is NOT the question."""
    return TRANSPORT in ("sixel", "tgp")


def rgb(hexstr: str) -> tuple[int, int, int]:
    h = hexstr.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def hexs(c: tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % c


def fit(img: Image.Image, w: int, h: int) -> Image.Image:
    """Resample to exactly w x h pixels, NEAREST.

    NEAREST and not LANCZOS: a density field is a field of samples, and a
    smoothed sample is a value that was never measured.  Every posture that
    then dithers or quantises would be quantising an interpolation."""
    return img.convert("RGB").resize((max(1, w), max(1, h)), Image.NEAREST)


def luma(img: Image.Image) -> Image.Image:
    return img.convert("L")


def halfblock(img: Image.Image, w: int, h: int) -> list[str]:
    """`h` markup rows of `w` cells: one cell = two vertically stacked pixels.

    Runs of identical (fg, bg) are coalesced into ONE markup tag.  Not an
    optimisation for its own sake -- Textual's markup path cannot coalesce
    runs itself (tui-demos LIMITS L-1), so a per-cell tag is a per-cell style
    object for the whole life of the frame.

    An empty cell is a SPACE, never a half-block in the default colours: a
    miss drawn as a glyph inherits the terminal's light default foreground and
    draws a white stripe (LIMITS L-24, found only by looking at a capture)."""
    px = fit(img, w, h * 2).load()
    rows: list[str] = []
    for r in range(h):
        out: list[str] = []
        run_top = run_bot = None
        n = 0
        for c in range(w):
            top, bot = px[c, 2 * r], px[c, 2 * r + 1]
            if (top, bot) != (run_top, run_bot):
                if n:
                    out.append(f"[{hexs(run_top)} on {hexs(run_bot)}]"
                               f"{HALF * n}[/]")
                run_top, run_bot, n = top, bot, 0
            n += 1
        if n:
            out.append(f"[{hexs(run_top)} on {hexs(run_bot)}]{HALF * n}[/]")
        rows.append("".join(out))
    return rows


def bitmap(img: Image.Image, cols: int, rows: int) -> list[list[int]]:
    """Ordered-dither to a 0/1 sprite of exactly `cols` x `rows`.

    1 = LIT.  The source is a density field where 1.0 is material, and the
    colormap paints material DARK on light paper -- so a lit dot is a dark
    pixel, and the threshold is against inverted luma."""
    src = luma(fit(img, cols, rows)).load()
    return [[1 if (255 - src[c, r]) > (BAYER4[r % 4][c % 4] + 0.5) * 16 else 0
             for c in range(cols)] for r in range(rows)]


def duotone(img: Image.Image, low: str, high: str) -> Image.Image:
    """Map luminance onto the ramp `low` -> `high`, in RGB.

    This is what a TINT posture does to the pixels, and the glyph side is then
    drawn off the RESULT -- so "blueprint tints the pixels" and "blueprint
    tints the cells" are one operation seen twice, not two implementations
    that can disagree.

    THE FIRST IMPLEMENTATION WAS WRONG AND SILENTLY SO, which is why it is
    named here: it built a 256-entry palette and called `luma(img).convert("P")`
    to index it. `convert("L" -> "P")` does not index -- it RE-QUANTISES to a
    palette of its own choosing, so the putpalette() call decorated a mapping
    that had already been thrown away and the output came back near-greyscale.
    It read correct and rendered the source. `ImageOps.colorize` is the
    operation that was meant."""
    return ImageOps.colorize(luma(img), black=rgb(low), white=rgb(high))


def quantise(img: Image.Image, cols: int, rows: int,
             on: str, off: str) -> Image.Image:
    """The LATTICE posture's pixel side: the image reduced to the same 0/1
    lattice the glyph side draws, painted back up to the region's pixel size.

    Same `bitmap()` call the glyph side makes, so a lattice dot that is lit in
    the cells is lit in the pixels.  Nearest-neighbour on the way back up: the
    dots must stay hard-edged, a smoothed dot is not a dot."""
    bm = bitmap(img, cols, rows)
    small = Image.new("RGB", (cols, rows))
    small.putdata([rgb(on) if v else rgb(off) for row in bm for v in row])
    return small.resize(img.size, Image.NEAREST)


def inset(img: Image.Image, ground: str, pad: int) -> Image.Image:
    """The DEPTH posture's pixel side: the image standing on `pad` pixels of
    stepped ground on every side, same overall size.

    The separation is a GROUND, never a border, so it is painted and not
    stroked -- the whole commitment is that no rule is drawn."""
    out = Image.new("RGB", img.size, rgb(ground))
    w, h = img.size
    out.paste(fit(img, max(1, w - 2 * pad), max(1, h - 2 * pad)), (pad, pad))
    return out


def step(hexstr: str, delta: int) -> str:
    """One grey STEP of a colour -- `delta` per channel, clamped.

    The depth posture's whole mechanism (LANGUAGES.md, Darkside: "separates
    from its neighbours by +/-1 grey step of BACKGROUND, never a border")."""
    return hexs(tuple(max(0, min(255, v + delta)) for v in rgb(hexstr)))
