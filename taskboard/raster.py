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

import importlib
import sys
import time

from PIL import Image, ImageOps

# THE PROBE IS GUARDED AND BOUNDED (tui-demos LIMITS L-42; SCOPE inc2 F-4).
#
# The docstring above is right that detection must happen at module load.  What
# it did not say is the price: `textual_image.renderable` runs a Sixel DEVICE
# ATTRIBUTES query at ITS module scope -- write ESC[c to stdout, then read
# stdin until the answer arrives -- gated only by its own
# `is_tty = sys.__stdout__ and sys.__stdout__.isatty()`.
#
# On Windows `NUL` is a CHARACTER DEVICE, so `isatty()` answers True for it.
# A process launched with `stdout=subprocess.DEVNULL` therefore believes it is
# talking to a terminal, writes the query into the void, and waits for an
# answer that cannot come.  Measured on this box, both ways, before the fix:
#
#     stdin=DEVNULL  stdout=DEVNULL -> HUNG (killed at 8s)
#     stdin=inherit  stdout=DEVNULL -> HUNG (killed at 8s)
#
# It cost SCOPE's second increment TWO 600-SECOND RUNS before
# `faulthandler.dump_traceback_later` found the stack, and the hang looks
# exactly like a slow numba compile until someone dumps it.  Every headless
# consumer of a kit inherits it -- a test runner, a bench, a CI job -- because
# the chain is `taskboard.language -> taskboard.raster -> textual_image.widget
# -> textual_image.renderable -> sixel.query_terminal_support`.
#
# So: PROBE ONLY WHEN BOTH ENDS ARE REAL CONSOLES, and bound the wait.
PROBE_BUDGET_S = 0.2                    # the whole answer wait, all reads


def _is_a_real_console(stream) -> bool:
    """True when `stream` is a console this process may hold a conversation
    with -- not merely a character device that answers `isatty()`.

    On Windows the discriminator is **`GetConsoleMode`**: it succeeds on a
    console handle and FAILS on `NUL`, which is the exact distinction
    `isatty()` cannot express there.  Elsewhere `isatty()` is already the
    truth -- `/dev/null` is not a tty on POSIX -- so it is the whole test.

    Both stdout AND stdin have to pass, because the probe writes to one and
    reads from the other, and it is the READ that blocks forever."""
    if stream is None:
        return False
    try:
        if not stream.isatty():
            return False
    except Exception:
        return False
    if sys.platform != "win32":
        return True
    try:
        import ctypes
        import msvcrt
        from ctypes.wintypes import DWORD
        mode = DWORD()
        handle = msvcrt.get_osfhandle(stream.fileno())
        return bool(ctypes.WinDLL("kernel32").GetConsoleMode(
            handle, ctypes.byref(mode)))
    except Exception:
        return False


class _NotATerminal:
    """A stdout stand-in that answers `isatty()` ACCURATELY.

    Not a monkeypatch of library internals -- it is telling `textual_image`
    the one truth `isatty()` cannot carry on Windows.  The library's own
    `is_tty` then comes out False, it selects the unicode renderable without
    querying anything, and `get_cell_size()` skips both of its query branches
    and falls through to the VT340 defaults.  Everything else delegates to the
    real stream, so a library that WRITES to stdout during import still
    writes to stdout."""

    def __init__(self, stream):
        self._stream = stream

    def isatty(self) -> bool:
        return False

    def __getattr__(self, name):
        return getattr(self._stream, name)


def _budgeted(read, budget: float):
    """`textual_image._terminal.read` with a DEADLINE across all its calls.

    The library already passes a 0.1 s per-read timeout; what it has no
    concept of is a TOTAL.  This caps the sum at `budget` and then raises
    `TimeoutError`, which both `query_terminal_support()` and
    `get_cell_size()` already catch and treat as "no answer" -- so the failure
    mode is the correct one (assume no Sixel) rather than an exception
    escaping the import.

    WHAT THIS DOES NOT BOUND, said plainly: a single `os.read()` that blocks
    AFTER `WaitForSingleObject` has returned signalled.  There is no
    non-blocking read behind that call, so bounding it would mean forking the
    library.  The GUARD above is what removes the reported failure; this caps
    the answer wait on the path the guard lets through."""
    deadline = time.monotonic() + budget

    def bounded(fd, length, timeout=None):
        left = deadline - time.monotonic()
        if left <= 0:
            raise TimeoutError("sixel probe budget exhausted")
        return read(fd, length, left if timeout is None else min(timeout, left))

    return bounded


def _import_textual_image():
    """Import the library, probing the terminal only if there is one.

    Returns `(AutoImage, chosen, sixel, tgp)`.  The swap and the budget are
    both undone in `finally`: this module must not leave a process's
    `sys.__stdout__` replaced or another module's function rebound."""
    out, stdin = sys.__stdout__, sys.__stdin__
    may_probe = _is_a_real_console(out) and _is_a_real_console(stdin)

    term = importlib.import_module("textual_image._terminal")
    real_read = term.read
    if may_probe:
        term.read = _budgeted(real_read, PROBE_BUDGET_S)
    elif out is not None:
        sys.__stdout__ = _NotATerminal(out)
    try:
        from textual_image.widget import Image as AutoImage
        from textual_image.renderable import Image as chosen
        from textual_image.renderable.sixel import Image as sixel
        from textual_image.renderable.tgp import Image as tgp
        return AutoImage, chosen, sixel, tgp
    finally:
        term.read = real_read
        sys.__stdout__ = out


def _transport(chosen, sixel, tgp) -> str:
    """WHICH transport the library picked for THIS terminal.  Sixel and TGP
    are real pixels; halfcell and unicode are the glyph path wearing the
    library's name -- which is why "a widget exists" is not the question
    `raster_available()` answers.

    SPELLED OUT RATHER THAN AS A DICT LOOKUP, because the dict was WRONG.  It
    was `{None: "none", _Sixel: "sixel", _TGP: "tgp"}.get(_Chosen, "glyph")`,
    and when the library is absent all four names are `None` -- so the literal
    collapsed to `{None: "tgp"}` and a box with no `textual_image` installed
    reported a TGP transport with `raster_available()` True.  Three `is` tests
    cannot collapse."""
    if chosen is None:
        return "none"
    if chosen is sixel:
        return "sixel"
    if chosen is tgp:
        return "tgp"
    return "glyph"


def _detect():
    """`(widget class, transport)` -- the whole decision, in one re-callable
    function so a test can drive it with the library's answer mocked."""
    try:
        AutoImage, chosen, sixel, tgp = _import_textual_image()
    except Exception:                   # pragma: no cover - declared dependency
        return None, "none"
    return AutoImage, _transport(chosen, sixel, tgp)


AutoImage, TRANSPORT = _detect()

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
