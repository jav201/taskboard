"""raster.py -- the 66 frames as PNG at a REAL cell size.  E2, built.

    python -X utf8 prototypes/components/raster.py

WHY THIS FILE EXISTS.  Three rounds of `PROTOTYPE-inheritors*.md` asked for a
raster and three rounds were refused one, so three rounds of legibility
findings are still written as *"planteada"* rather than resolved.  Round four
says it plainly (§8.2): *"un ratio de contraste no es una prueba de
legibilidad, y esta ronda no tiene mas que ratios ... el `.svg` no dice a que
tamanio de celda ni con que fuente se va a renderizar, asi que `⠂` a 1,74:1 a
una altura desconocida es un numero y no una fotografia."*  The `.svg` carries
`fill=` and a nominal 8.4x17 box that no font ever agreed to; it carries no
font, no hinting and no coverage.  A homoglyph pair and a contrast ratio are
therefore both NUMBERS in that artefact and neither is a legibility test.

WHAT THIS FILE IS ALLOWED TO DO.  It renders.  It measures nothing --
`legibility.py` (inc77) is the instrument and this is the film.  The split is
deliberate: a renderer that also scores has an opinion about what it draws.

THE RENDER PATH IS NOT REIMPLEMENTED HERE, TWICE OVER.  The cell grid comes
from `render.frame()`, which is `render.one()` minus its two `write_text`
calls, which is `capture_languages.cell_grid()` -- the same function the 66
`.svg` are exported from.  If the PNG and the SVG disagreed about a cell it
would be because the exporter disagrees with itself, and that is a finding
this file can produce rather than a confound it introduces.

EVERY METRIC BELOW IS DECLARED, NEVER INFERRED, and that is inc63's ruling E4
applied one artefact over.  E4 was written because `cell_grid` took *"the most
common background in the frame"* for its ground and agreed with a mistake that
covered 3200 of 3200 cells.  A raster has the identical failure available to
it: pick the font by scanning the box for "something monospace", and the
measurement silently becomes a measurement of whichever font happened to sort
first.  So the face, its size, its fallback and the exact cells routed to that
fallback are constants in this file, and `_declare()` asserts each one against
the machine before a pixel is drawn.
"""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes"))
sys.path.insert(0, str(HERE))

from PIL import Image, ImageDraw, ImageFont                      # noqa: E402

import render as R                                               # noqa: E402
import screens as S                                              # noqa: E402

OUT = HERE / "png"

#: THE FACE, DECLARED.  Cascadia Mono is Windows Terminal's own default font
#: and it ships in `C:\Windows\Fonts` on this box -- which is the whole reason
#: it is the right face and not merely an available one: the corpus is judged
#: as a terminal design, so the raster should be the picture the terminal this
#: repo is developed on would actually draw.  Consolas and Lucida Console were
#: the alternatives and both were REJECTED BY MEASUREMENT, not by taste
#: (`_declare()` re-checks the first two numbers every run):
#:
#:     Cascadia Mono   4 of the corpus's 206 cells missing
#:     Cascadia Code   4 missing -- the same face WITH ligatures, and a
#:                     ligature is a glyph spanning two cells, which is the
#:                     one thing a cell-grid raster must not be given
#:     Consolas       64 missing  (no braille at all, half the block elements)
#:     Lucida Console 87 missing  (no braille, no rounded box drawing)
#:
#: DejaVu Sans Mono, which the brief also named, is not installed on this
#: machine and was not installed to make it fit.
FONT_NAME = "Cascadia Mono"
FONT_PATH = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts/CascadiaMono.ttf"

#: 16 px = 12 pt at 96 dpi = Windows Terminal's default size.  At this size
#: Cascadia's advance lands on 9.0 px and its ascent/descent on 15/4, so the
#: cell box is 9x19 INTEGER PIXELS and the grid needs no rounding anywhere.
#: That is luck and it is checked rather than relied upon: `_declare()` fails
#: loud if the advance ever comes back fractional, because a fractional
#: advance means every column after the first sits at a different subpixel
#: phase and a per-cell measurement stops meaning one thing.
FONT_PX = 16

#: Cascadia ships as a VARIABLE font on Windows and `bold` is a named
#: instance, so `MATCH_STYLE`'s seven bold kits get the real bold face rather
#: than a synthetic one.  The brief allowed `stroke_width=1` as the fallback;
#: it is not taken, and the difference is recorded because it matters to
#: inc77: a stroked glyph gains ink area at its outline and a bold face gains
#: it in the stem, and only one of those is what a terminal shows.
BOLD_INSTANCE = "Bold"

#: THE FOUR CELLS CASCADIA DOES NOT HAVE, and what happens to them.  A
#: terminal does not draw tofu here -- it falls back, and on Windows it falls
#: back to Segoe UI Symbol.  Drawing a missing-glyph box would have made four
#: of the corpus's cells look like a defect of the DESIGN when they are a
#: defect of the FACE, and inc77 measures ink area per glyph: four boxes would
#: have scored as four confident, wrong numbers.
#:
#: The list is exhaustive and asserted both ways: the primary must lack
#: exactly these among the corpus's cells, and the fallback must have all
#: four.  A twelfth kit that reaches for a fifth uncovered cell fails here
#: instead of being drawn as a box nobody looks at.
FALLBACK_NAME = "Segoe UI Symbol"
FALLBACK_PATH = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts/seguisym.ttf"
FALLBACK_CELLS = "⊖⊚⊛⋅"  # codepoint order, which is `corpus_cells()`'s order

#: Segoe UI Symbol is PROPORTIONAL: `⊖` is 13 px wide at 16 px against a 9 px
#: cell.  A terminal fits a fallback glyph to the cell, so the raster does the
#: same and says how: the largest integer pixel size whose advance fits the
#: cell, then centred horizontally, baseline shared with the primary.  The
#: chosen size is written into every sidecar, per glyph, so inc77's ink areas
#: for these four carry their own asterisk instead of pretending to be
#: measured at the same size as the other 118.
UNDERLINE_OFFSET = 2  #: px below the baseline, drawn 1 px thick

#: THE GREYSCALE PASS, DECLARED (inc84, on the greyscale ruling).  Round
#: five's L12 is that three kits carry their MATCH on hue alone (instrument,
#: nord, prism) and that the clause approving them measures LUMINANCE against
#: an achromatic `mut` -- the dimension in which a saturated hue and a grey
#: are least different.  Its §0d says the objection cannot be settled from
#: this repo: *"no hay lector daltonico en este equipo ni captura en escala
#: de grises en este repo"*.  This is the second half of that sentence,
#: built.
#:
#: IT IS NOT `Image.convert("L")`, and the difference is the point.  PIL's
#: `L` applies ITU-R 601-2 coefficients to the ENCODED values, which is a
#: display convenience and not a photometric quantity.  A legibility question
#: needs WCAG's own relative luminance -- linearise sRGB, weight by Rec.709,
#: re-encode -- because then the CONTRAST RATIO between two greys in this
#: image equals the ratio the colour pair had, and "does the match survive
#: greyscale" is answered by the same arithmetic every other number in this
#: programme is answered by.  The coefficients are ruling E4 applied one
#: artefact over: declared, never inferred, and checked against the shipped
#: PNGs by the suite rather than trusted here.
GREY_WEIGHTS = (0.2126, 0.7152, 0.0722)


def _linear(v: int) -> float:
    x = v / 255
    return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4


def _encode(y: float) -> int:
    s = 12.92 * y if y <= 0.0031308 else 1.055 * (y ** (1 / 2.4)) - 0.055
    return max(0, min(255, round(s * 255)))


def grey_of(im: Image.Image) -> Image.Image:
    """The frame with its HUE removed and its luminance kept, exactly.

    A per-COLOUR lookup rather than a per-pixel one: a frame is a few dozen
    declared colours over half a million pixels, so the table is small, and --
    the reason that matters here -- the mapping is a function of the colour
    and therefore cannot pick up a position-dependent rounding, which is the
    kind of confound `check_reproducible` exists to catch and would rather
    not have to.
    """
    table: dict[tuple, tuple] = {}
    for p in set(im.getdata()):
        g = _encode(sum(w * _linear(c) for w, c in zip(GREY_WEIGHTS, p)))
        table[p] = (g, g, g)
    out = Image.new("RGB", im.size)
    out.putdata([table[p] for p in im.getdata()])
    return out


#: TWO CODEPOINTS NO FACE HAS, used to learn what `.notdef` looks like.
#: Private-use and non-character, and BOTH are asked because one of them
#: landing in some vendor's private-use block would make every glyph on the
#: box look present.  They must agree before the answer is trusted.
_ABSENT = ("", "\U0010fffd")


def uncovered(path: Path, cells: str) -> str:
    """Which of `cells` this face does not have, asked of the RASTERISER.

    Not a `cmap` read, and the difference is the point: a cmap says what the
    face CLAIMS and this asks what FreeType actually draws, which is the thing
    the picture will contain.  A glyph is missing when its bitmap is byte for
    byte the bitmap two absent codepoints produce.  (Checked against a
    `fontTools` cmap read while this was written: identical answer on all four
    faces -- and `fontTools` is not a dependency of this project, so the
    agreement is recorded and the dependency is not taken.)
    """
    f = ImageFont.truetype(str(path), FONT_PX)

    def sig(ch: str):
        m = f.getmask(ch, mode="L")
        return m.size, bytes(m)

    a, b = (sig(c) for c in _ABSENT)
    if a != b:
        raise SystemExit(f"{path.name}: the two absent codepoints draw "
                         f"differently, so `.notdef` cannot be recognised")
    return "".join(c for c in cells if sig(c) == a)


def corpus_cells() -> str:
    """Every distinct cell the 66 `.txt` spend, newline dropped, sorted.

    Read off the ARTEFACTS rather than off the kits, because the question is
    what the raster has to draw and a kit can declare a glyph no screen
    reaches.  inc77 asks the other question and asks it of the kits.
    """
    seen: set[str] = set()
    for p in sorted(HERE.glob("*_S?.txt")):
        seen |= set(p.read_text(encoding="utf-8"))
    seen.discard("\n")
    return "".join(sorted(seen))


class Metrics:
    """The declared box, measured once and checked against the declaration."""

    def __init__(self) -> None:
        self.regular = ImageFont.truetype(str(FONT_PATH), FONT_PX)
        self.bold = ImageFont.truetype(str(FONT_PATH), FONT_PX)
        self.bold.set_variation_by_name(BOLD_INSTANCE)
        self.advance = self.regular.getlength("M")
        self.ascent, self.descent = self.regular.getmetrics()
        self.w = int(self.advance)
        self.h = self.ascent + self.descent
        self.fallback_px: dict[str, int] = {}
        for ch in FALLBACK_CELLS:
            px = FONT_PX
            while px > 1 and ImageFont.truetype(
                    str(FALLBACK_PATH), px).getlength(ch) > self.w:
                px -= 1
            self.fallback_px[ch] = px
        self.fallback = {ch: ImageFont.truetype(str(FALLBACK_PATH), px)
                         for ch, px in self.fallback_px.items()}

    def as_json(self) -> dict:
        return {
            "font": {"name": FONT_NAME, "path": str(FONT_PATH),
                     "px": FONT_PX, "bold_instance": BOLD_INSTANCE},
            "fallback": {"name": FALLBACK_NAME, "path": str(FALLBACK_PATH),
                         "cells": list(FALLBACK_CELLS),
                         "px": self.fallback_px},
            "cell": {"w": self.w, "h": self.h, "advance": self.advance,
                     "ascent": self.ascent, "descent": self.descent,
                     "underline_y": self.ascent + UNDERLINE_OFFSET},
        }


def _declare(m: Metrics) -> list[str]:
    """Every declaration above, checked against this machine.

    Returned as lines rather than printed, so the caller decides where they go
    and so a test can read them.  Anything that fails RAISES: a raster whose
    font is not the declared font is a picture of something else.
    """
    lines = []
    cells = corpus_cells()
    missing = uncovered(FONT_PATH, cells)
    if missing != FALLBACK_CELLS:
        raise SystemExit(
            f"the corpus's uncovered cells are {missing!r}, declared "
            f"{FALLBACK_CELLS!r} -- update FALLBACK_CELLS and say why")
    still = uncovered(FALLBACK_PATH, FALLBACK_CELLS)
    if still:
        raise SystemExit(f"{FALLBACK_NAME} does not cover {still!r}")
    if m.advance != float(m.w):
        raise SystemExit(f"advance {m.advance} is not an integer number of "
                         f"pixels; the cell grid would drift")
    if m.regular.getlength("i") != m.advance or \
            m.bold.getlength("M") != m.advance:
        raise SystemExit("the face is not monospaced at this size")
    lines.append(f"  face      {FONT_NAME} {FONT_PX}px  {FONT_PATH}")
    lines.append(f"  bold      variable instance {BOLD_INSTANCE!r} "
                 f"(not a synthetic stroke)")
    lines.append(f"  cell      {m.w}x{m.h} px  "
                 f"(advance {m.advance}, ascent {m.ascent}, "
                 f"descent {m.descent})")
    lines.append(f"  underline baseline+{UNDERLINE_OFFSET} px, 1 px thick")
    lines.append(f"  corpus    {len(cells)} distinct cells, "
                 f"{len(cells) - len(FALLBACK_CELLS)} in the face")
    lines.append(f"  fallback  {FALLBACK_NAME} for {FALLBACK_CELLS} "
                 f"at {m.fallback_px} px, centred")
    return lines


def cell_tile(m: Metrics, ch: str, fg: str, bg: str,
              bold: bool, under: bool) -> Image.Image:
    """ONE CELL, drawn into its own box and therefore CLIPPED to it.

    A terminal clips to the cell and this is where that gets honoured.  It is
    not cosmetic: Cascadia's `█` measures 10x20 against a 9x19 box, so drawing
    the frame as text would let every full block bleed a column right and a
    row up, and inc77's per-cell coverage would then be reading its
    neighbour's ink.  Composing per cell makes the cell the unit of the
    measurement as well as of the picture.
    """
    tile = Image.new("RGB", (m.w, m.h), bg)
    d = ImageDraw.Draw(tile)
    if ch in m.fallback:
        f = m.fallback[ch]
        x = (m.w - f.getlength(ch)) / 2
        d.text((x, m.ascent), ch, font=f, fill=fg, anchor="ls")
    elif ch.strip():
        d.text((0, m.ascent), ch, font=(m.bold if bold else m.regular),
               fill=fg, anchor="ls")
    if under:
        y = m.ascent + UNDERLINE_OFFSET
        d.line([(0, y), (m.w - 1, y)], fill=fg, width=1)
    return tile


def png_of(m: Metrics, grid) -> Image.Image:
    cols = max(len(r) for r in grid)
    img = Image.new("RGB", (cols * m.w, len(grid) * m.h), "#000000")
    for y, row in enumerate(grid):
        for x, (ch, fg, bg, bold, under) in enumerate(row):
            img.paste(cell_tile(m, ch, fg, bg, bold, under),
                      (x * m.w, y * m.h))
    return img


def runs_of(grid) -> list[list]:
    """The grid, run-encoded on `(fg, bg, bold, underline)`.

    The sidecar carries the grid so inc77 can read a cell's DECLARED colours
    beside the pixels it actually got without re-driving Textual, and so a law
    can compare the two without importing the renderer.  Run encoding because
    a per-cell list of 3200 five-tuples is a 300 KB file that says the same
    thing.
    """
    out = []
    for row in grid:
        runs, cur, buf, x0 = [], None, "", 0
        for x, (ch, fg, bg, bold, under) in enumerate(row):
            key = (fg, bg, bold, under)
            if key != cur:
                if buf:
                    runs.append([x0, buf, *cur])
                cur, buf, x0 = key, "", x
            buf += ch
        if buf:
            runs.append([x0, buf, *cur])
        out.append(runs)
    return out


async def sweep(m: Metrics, out: Path, size=None) -> dict[str, bytes]:
    """Render the 66 and return `{name: png bytes}`, having written them."""
    out.mkdir(parents=True, exist_ok=True)
    made: dict[str, bytes] = {}
    for lang in R.LANGS:
        for screen in S.SCREENS:
            _, rect, grid, ground, _ = await R.frame(lang, screen, size)
            name = f"{lang}_{screen}"
            img = png_of(m, grid)
            path = out / f"{name}.png"
            img.save(path, "PNG", optimize=True)
            made[name] = path.read_bytes()
            # THE SAME FRAME WITH ITS HUE REMOVED (inc84). Written beside the
            # colour one and checked for determinism with it, because a
            # second artefact that is not in the reproducibility bargain is a
            # second artefact nobody has to keep honest.
            grey = out / f"{name}.grey.png"
            grey_of(img).save(grey, "PNG", optimize=True)
            made[f"{name}.grey"] = grey.read_bytes()
            side = {"lang": lang, "screen": screen, "ground": ground,
                    "cols": max(len(r) for r in grid), "rows": len(grid),
                    "image": {"w": img.width, "h": img.height},
                    "txt": {"cols": len(rect[0]), "rows": len(rect)},
                    **m.as_json(), "grid": runs_of(grid)}
            (out / f"{name}.json").write_text(
                json.dumps(side, ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8")
    return made


def check_reproducible(first: dict[str, bytes]) -> list[str]:
    """Re-render in a SEPARATE PROCESS and diff every PNG byte for byte.

    The same bargain `capture_languages.check_reproducible` makes and for the
    same reason it makes it: two passes in one interpreter share whatever
    state the confound lives in.  A raster has two candidate confounds that a
    second in-process pass would sail through -- a font object cached across
    calls and a variation axis left set by a previous frame -- and both are
    exactly the kind of thing that reproduces perfectly until someone else
    runs the script.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([sys.executable, "-X", "utf8",
                            str(Path(__file__).resolve()), "--raster-to", td],
                           capture_output=True, text=True,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        if r.returncode != 0:
            raise RuntimeError(f"control raster failed:\n{r.stderr[-1500:]}")
        missing = [n for n in first if not (Path(td) / f"{n}.png").exists()]
        if missing:
            raise RuntimeError(
                f"the control raster did not write {missing} -- the two arms "
                f"disagree about what a raster produces")
        return [n for n, b in first.items()
                if (Path(td) / f"{n}.png").read_bytes() != b]


def main(argv: list[str]) -> int:
    m = Metrics()
    if "--raster-to" in argv:  # the control arm: render, write, say nothing
        asyncio.run(sweep(m, Path(argv[argv.index("--raster-to") + 1])))
        return 0
    print(f"{len(R.LANGS)} languages x {len(S.SCREENS)} screens | "
          f"viewport {S.W}x{S.H} cells")
    for line in _declare(m):
        print(line)
    made = asyncio.run(sweep(m, OUT))
    frames = len(R.LANGS) * len(S.SCREENS)
    if len(made) != frames * 2:          # a colour PNG and a grey one each
        print("INCOMPLETE RASTER", file=sys.stderr)
        return 1

    # THE RASTER'S OWN LAW, and it is the one thing this file can check that
    # no test can check more cheaply: the picture has as many cells as the
    # text artefact has characters.  A raster that quietly drew 99 columns
    # would still look like a taskboard.
    bad = []
    for name in made:
        if name.endswith(".grey"):
            # the grey pass is the colour frame's own pixels with the hue
            # taken out, so its law is that it is the SAME PICTURE at the
            # same size; the colour arm's cell count answers for both.
            if (Image.open(OUT / f"{name}.png").size
                    != Image.open(OUT / f"{name[:-5]}.png").size):
                bad.append((name, "grey size disagrees with colour"))
            continue
        rows = (HERE / f"{name}.txt").read_text(
            encoding="utf-8").rstrip("\n").split("\n")
        want = (len(rows[0]) * m.w, len(rows) * m.h)
        got = Image.open(OUT / f"{name}.png").size
        if want != got:
            bad.append((name, want, got))
    if bad:
        print(f"CELL COUNT DISAGREES WITH THE TXT: {bad}", file=sys.stderr)
        return 1

    print("\n  re-rendering in a fresh process to check determinism...")
    drift = check_reproducible(made)
    if drift:
        print(f"NON-REPRODUCIBLE RASTERS: {drift}", file=sys.stderr)
        return 1
    kb = sum(len(b) for b in made.values()) / 1024
    print(f"  {len(made)} PNGs identical across two PROCESSES "
          f"({frames} colour + {frames} grey)")
    print(f"\n  {frames} .png + {frames} .grey.png + {frames} .json -> {OUT}")
    print(f"  every raster is {len(rows[0])}x{len(rows)} cells of "
          f"{m.w}x{m.h} px  ({kb:.0f} KB total)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
