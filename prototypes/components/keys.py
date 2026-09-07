"""keys.py -- the first round that PRESSES A KEY.  Eleven languages, six frames.

    python -X utf8 prototypes/components/keys.py

WHY THIS FILE EXISTS.  `PROTOTYPE-inheritors-5.md` converged on one sentence:
*"a frame cannot fail on focus because a frame has no focus"*, and
`SESION-PERSONA.md` section 7.3 named the instrument that had been sitting
unused for five rounds -- `App.run_test()` + `Pilot`.  Every artefact this
programme has judged so far is a PHOTOGRAPH of a composed surface: `render.py`
mounts a kit's output in a bare `Static`, `raster.py` paints that same grid at
9x19 px, and `legibility.py` measures the paint.  None of them can press
anything, so five rounds of objections about focus, about a modal, about an
invalid field and about a match run were arguments about pictures of those
states rather than about the states.

THE INSTRUMENT IS THE WIDGET SLICE, NOT THE SHEETS.  `render.py`'s six screens
are the canonical screens every terminal app needs; they are drawn by hand from
kit calls precisely because the app does not have them.  A key needs something
to press, so this file drives `prototypes/widget_slice/app.py` -- the real
`TaskboardWidget`, the one `capture_languages.py` already photographs -- and
reads the result through the SAME `cell_grid` the raster reads.  That is the
whole reason the capture path is imported rather than rewritten: a frame taken
through a second pipeline could not be laid beside the 66.

WHAT THIS FILE MAY NOT DO.  It may not fix anything.  A step that fails is
recorded in the table `main()` prints and nowhere else; the laws that bite live
in `tests/test_components.py`, read off the artefacts, which is the stance this
corpus has taken since inc73.
"""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes"))
sys.path.insert(0, str(ROOT / "prototypes" / "widget_slice"))

from PIL import Image, ImageDraw, ImageFont                     # noqa: E402
from rich.cells import cell_len                                 # noqa: E402

import capture_languages as CAP                                 # noqa: E402
import raster as RA                                             # noqa: E402
import taskboard.language as LG                                 # noqa: E402
import taskboard.themes as TH                                   # noqa: E402

#: THE ROUND'S OWN VIEWPORT, and it is the raster's.  100x32 is the size
#: `PROTOTYPE-inheritors-5.md` judged the 66 at and the one size the human
#: session will show; a key round taken at a different size would not be
#: comparable with either.
SIZE = (100, 32)

#: ALL ELEVEN, read off the theme registry rather than typed -- the same
#: bargain `render.py` makes and for the same reason.
LANGS = list(TH.ORDER)

OUT = HERE / "keys"


class Step(NamedTuple):
    """One press of the script, and the law it is answerable to.

    `keys` is what the Pilot sends BEFORE the frame is read, so a step with
    an empty tuple is the page as it opens.  `law` is prose on purpose: the
    arithmetic lives in `judge()` below and in the suite, and a step whose
    law could be written as a lambda here would be a law nobody could argue
    with in a review.
    """
    n: int
    name: str
    keys: tuple[str, ...]
    law: str


#: THE DATE THE WIDGET HAS NO FIELD FOR.  `12/99/26` is a day-99 month, which
#: `taskboard.models.parse_iso` refuses and which every one of the eleven kits
#: draws a state for (`field_form(INVALID, "textfield")`).  The keys are sent
#: at the screen the app offers for editing -- `c`, the config screen -- and
#: the trailing `tab` is the BLUR, because an invalid state that only appears
#: while the caret is in the field is a state nobody sees.
DATE_KEYS = ("1", "2", "slash", "9", "9", "slash", "2", "6")

#: THE QUERY WITH ONE MATCH.  `refre` hits `Refresh now` and nothing else in
#: the palette `get_system_commands` registers, in all eleven -- the commands
#: are the app's and do not vary by language, which is what makes the frame a
#: comparison of MATCH RENDERING rather than of result sets.
QUERY_KEYS = ("r", "e", "f", "r", "e")

SCRIPT: tuple[Step, ...] = (
    Step(1, "initial", (),
         "the page as it opens, with the app's own AUTO_FOCUS seat lit"),
    Step(2, "focus", ("tab",) * 3,
         "focus walked three seats: the seat that HOLDS focus at K2 is drawn "
         "differently from the way the same cells were drawn at K1"),
    Step(3, "modal", ("question_mark",),
         "a modal is open: the band exists, and its ground is the kit's own "
         "panel rather than the skeleton's"),
    Step(4, "escape", ("escape",),
         "the band is gone and the page is restored cell for cell to the "
         "frame the modal covered"),
    Step(5, "invalid", ("c",) + DATE_KEYS + ("tab",),
         "the field carries the language's declared INVALID walls "
         "(field_form(INVALID, 'textfield')), painted in the wall tone "
         "field_wall_tone(INVALID) names"),
    Step(6, "match", ("ctrl+p",) + QUERY_KEYS,
         "the run the query found carries the channel MATCH_STYLE declares, "
         "in the ink MATCH_STYLE declares"),
)

#: **THE FOURTH STEP'S LAW IS JUDGED AGAINST K2 AND THE BRIEF SAYS K1.**  The
#: brief's words are *"escape -> the band is gone and the page is
#: byte-identical to K1"*.  Read literally that asks `escape` to undo the three
#: tabs the script itself pressed one step earlier, which no app does and none
#: should.  What a modal owes is that it gives back the page it covered, so the
#: law is judged against **K2 -- the frame the modal was drawn over** -- and
#: the distance from K1 is reported beside it rather than hidden.
RESTORE_AGAINST = 2


class _Reads:
    """A Pilot that COUNTS the reads `settle` spends, and forwards the rest.

    The sidecar has to carry the settle read count -- a frame that needed 8
    reads and a frame that needed 31 are not equally settled, and the second
    one is where a race lives.  `capture_languages.settle` does not return the
    count and must not be forked to add one (it is the shared instrument), so
    the count is taken on this side of the call: `settle`'s only clock is
    `await pilot.pause()`, so wrapping that one method counts exactly what it
    spent.  Everything else falls through to the real Pilot by `__getattr__`.
    """

    def __init__(self, pilot) -> None:
        self._pilot, self.reads = pilot, 0

    async def pause(self, *a, **kw):
        self.reads += 1
        return await self._pilot.pause(*a, **kw)

    def __getattr__(self, k):
        return getattr(self._pilot, k)


#: The continuation cell of a DOUBLE-WIDTH glyph -- see `widen`.
CONT = ""


def widen(grid, ground: str) -> list[list]:
    """One grid entry per terminal COLUMN, not per character.

    `cell_grid` appends one entry per character in a segment, which is right
    for every cell the 66 sheets spend because every one of them is one column
    wide.  **The key round found the first cell in this corpus that is not.**
    Textual's command palette draws its prompt as `SearchIcon`, whose glyph is
    the emoji `U+1F50E` -- two columns in the terminal, one entry in the grid
    -- so the palette row arrives 99 entries long for a 100-column frame and
    everything to the right of the prompt would be painted one cell left of
    where the terminal puts it.

    This is not corrected quietly: the finding is that the app's ONE live
    search seat prints a glyph the corpus's measured face does not cover and
    the corpus's grid cannot hold, and it is in `inc91.md`.  What this
    function does is keep the PICTURE honest while that stands -- the wide
    glyph keeps its own entry and is followed by a continuation cell carrying
    the same ground, so column N of the raster is column N of the terminal.
    """
    out = []
    for row in grid:
        r: list = []
        for cell in row:
            r.append(cell)
            for _ in range(max(1, cell_len(cell[0])) - 1):
                r.append((CONT, cell[1], cell[2], cell[3], cell[4]))
        out.append(r)
    w = max(len(r) for r in out)
    pad = (" ", "#ffffff", ground, False, False)
    return [r + [pad] * (w - len(r)) for r in out]


def key_cells() -> str:
    """Every distinct cell the key frames spend, read off the ARTEFACTS.

    `raster.corpus_cells()` reads `*_S?.txt`; this reads `keys/*_K?.txt`, for
    the same stated reason -- the question is what this raster has to draw,
    and the two corpora are not the same set.
    """
    seen: set[str] = set()
    for p in sorted(OUT.glob("*_K?.txt")):
        seen |= set(p.read_text(encoding="utf-8"))
    seen.discard("\n")
    return "".join(sorted(seen))


def metrics_for(cells: str) -> RA.Metrics:
    """The raster's own `Metrics`, with a fallback entry per uncovered cell.

    `raster.Metrics` builds its fallback table from `raster.FALLBACK_CELLS`,
    which is the 66 sheets' four.  The key corpus has its own uncovered set
    and it is DECLARED (`FALLBACK_CELLS` below) rather than discovered at run
    time, so a sixth cell arriving from a framework upgrade fails loud instead
    of being drawn in whatever font happens to have it.
    """
    m = RA.Metrics()
    for ch in cells:
        if ch in m.fallback:
            continue
        px = RA.FONT_PX
        while px > 1 and ImageFont.truetype(
                str(RA.FALLBACK_PATH), px).getlength(ch) > m.w * cell_len(ch):
            px -= 1
        m.fallback_px[ch] = px
        m.fallback[ch] = ImageFont.truetype(str(RA.FALLBACK_PATH), px)
    return m


#: THE CELLS THIS CORPUS SPENDS THAT CASCADIA MONO DOES NOT HAVE, and it is
#: **not** the 66 sheets' set.  `raster.FALLBACK_CELLS` is `⊖⊚⊛⋅`; the live app
#: spends `⊖⊚` and `⊙` and neither `⊛` nor `⋅`, which is itself a reading: two
#: cells the sheets draw are drawn by no screen the app HAS.  The fourth is the
#: command palette's prompt `U+1F50E`, the corpus's first double-width cell and
#: the only one of the four that is not a kit's choice -- it is Textual's.
#: Declared here in codepoint order, which is `key_cells()`'s order, so a fifth
#: fails the run rather than reaching a picture in whatever font happens to
#: have it.
FALLBACK_CELLS = "⊖⊙⊚\U0001f50e"


def cell_tile(m: RA.Metrics, ch: str, fg: str, bg: str,
              bold: bool, under: bool, span: int):
    """ONE CELL of the key raster, clipped to `span` columns.

    `span == 1` is `raster.cell_tile` and is DELEGATED to it, so the 66 sheets
    and the 66 key frames are painted by one function wherever they can be.
    `span == 2` is the branch that function does not have and must not grow
    for one caller: a glyph two columns wide gets a box two columns wide, and
    the continuation cell after it paints its ground and nothing else.
    """
    if span == 1 and ch != CONT:
        return RA.cell_tile(m, ch, fg, bg, bold, under)
    tile = Image.new("RGB", (m.w * span, m.h), bg)
    if ch == CONT:
        return tile                      # the wide glyph already covered it
    d = ImageDraw.Draw(tile)
    f = m.fallback.get(ch, m.bold if bold else m.regular)
    d.text(((m.w * span - f.getlength(ch)) / 2, m.ascent), ch,
           font=f, fill=fg, anchor="ls")
    if under:
        y = m.ascent + RA.UNDERLINE_OFFSET
        d.line([(0, y), (m.w * span - 1, y)], fill=fg, width=1)
    return tile


def png_of(m: RA.Metrics, grid) -> Image.Image:
    """`raster.png_of` with the wide-cell branch -- see `cell_tile`."""
    cols = max(len(r) for r in grid)
    img = Image.new("RGB", (cols * m.w, len(grid) * m.h), "#000000")
    for y, row in enumerate(grid):
        for x, (ch, fg, bg, bold, under) in enumerate(row):
            span = max(1, cell_len(ch)) if ch else 1
            img.paste(cell_tile(m, ch, fg, bg, bold, under, span),
                      (x * m.w, y * m.h))
    return img


def _region(w) -> list[int] | None:
    """A widget's SCREEN rectangle as `[x, y, w, h]`, or `None`.

    Recorded in the sidecar because two of the six laws are about WHERE:
    "the seat that holds focus is drawn differently" needs the seat's cells,
    and "the band exists" needs the band's.  A law that had to re-drive
    Textual to find out where a widget was would be a second instrument.
    """
    if w is None:
        return None
    try:
        r = w.region
    except Exception:
        return None
    return [r.x, r.y, r.width, r.height]


async def run_lang(lang: str, out: Path, m: RA.Metrics | None) -> list[dict]:
    """The six frames of one language, in one app session.

    ONE SESSION AND NOT SIX, because the script is a SEQUENCE: step 4 is only
    a law about restoration if the modal it dismisses is the one step 3
    opened, and step 2's focus walk is only a walk if it starts where step 1
    left the ring.  Six sessions would have measured six first frames.
    """
    from app import TaskboardWidget

    ground = TH.THEMES[lang]["ground"]
    side: list[dict] = []
    app = TaskboardWidget(board_path=CAP.FIXTURE)
    async with app.run_test(size=SIZE) as pilot:
        await pilot.pause()
        # a toast is a TIMED overlay: it would put the capture's content on a
        # clock, which is the one thing `freeze_clock` exists to prevent.
        app.notify = lambda *a, **kw: None
        app.set_theme(lang)
        for st in SCRIPT:
            for k in st.keys:
                await pilot.press(k)
            counter = _Reads(pilot)
            rows = await CAP.settle(counter, app, f"{lang} K{st.n}")
            grid, _g = CAP.cell_grid(app, ground)
            wide = widen(grid, ground)
            w = max(len(r) for r in rows)
            rect = [r.ljust(w) for r in rows]
            name = f"{lang}_K{st.n}"
            (out / f"{name}.txt").write_text("\n".join(rect) + "\n",
                                             encoding="utf-8")
            # THE SVG TAKES THE RAW GRID AND THE PNG TAKES THE WIDE ONE, and
            # the split is the wide glyph again: the SVG's own renderer
            # advances two columns for a two-column glyph, so handing it a
            # continuation cell would push the rest of that row one cell
            # right.  The picture that has to agree with the terminal is the
            # raster, and it is the one that gets the correction.
            (out / f"{name}.svg").write_text(
                CAP.svg_from_grid(grid, ground,
                                  f"taskboard - {lang} - K{st.n} {st.name}"),
                encoding="utf-8")
            if m is not None:
                png_of(m, wide).save(out / f"{name}.png", "PNG", optimize=True)
            focused = app.screen.focused
            band = None
            for sel in ("#help-box", "#gallery-box"):
                try:
                    band = _region(app.screen.query_one(sel))
                    break
                except Exception:
                    continue
            side.append({
                "lang": lang, "step": st.n, "name": st.name,
                "keys": list(st.keys), "law": st.law,
                "screen": type(app.screen).__name__,
                "focus": {"id": getattr(focused, "id", None),
                          "cls": type(focused).__name__ if focused else None,
                          "region": _region(focused)},
                "band": band,
                "settle_reads": counter.reads,
                "ground": ground,
                "cols": max(len(r) for r in wide), "rows": len(wide),
                "txt": {"cols": len(rect[0]), "rows": len(rect)},
                "grid": RA.runs_of(wide),
            })
            (out / f"{name}.json").write_text(
                json.dumps(side[-1], ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8")
    return side


async def sweep(out: Path, m: RA.Metrics | None) -> list[dict]:
    from app import TaskboardWidget                         # noqa: F401
    CAP.freeze_clock()                       # AFTER the imports it patches
    out.mkdir(parents=True, exist_ok=True)
    got: list[dict] = []
    for lang in LANGS:
        got += await run_lang(lang, out, m)
    return got


# ---------------------------------------------------------------------------
# THE SIX LAWS, judged off the artefacts and REPORTED.
#
# Nothing here fixes anything and nothing here raises.  inc91's whole brief is
# to run the script and say which language fails which step BEFORE a fix, so a
# failure is a row in a table.  The laws that BITE are in the suite, read off
# these same sidecars.
# ---------------------------------------------------------------------------

def cells_of(side: dict) -> list[list]:
    """The sidecar's run encoding unpacked back to `(ch, fg, bg, bold, u)`."""
    out = []
    for row in side["grid"]:
        r: list = []
        for x0, text, fg, bg, bold, under in row:
            while len(r) < x0:
                r.append((" ", "#ffffff", side["ground"], False, False))
            if text:
                for ch in text:
                    r.append((ch, fg, bg, bold, under))
            else:
                r.append((CONT, fg, bg, bold, under))
        out.append(r)
    return out


def _box(cells, region) -> list[tuple]:
    x, y, w, h = region
    return [tuple(row[x:x + w]) for row in cells[y:y + h] if row]


def _at(row, x: int, glyph: str, tone: str) -> bool:
    """Is `glyph` drawn at column `x` of this row, all of it in `tone`?"""
    if x + len(glyph) > len(row):
        return False
    return all(row[x + i][0] == ch and row[x + i][1].lower() == tone.lower()
               for i, ch in enumerate(glyph))


def field_seats(cells, op: str, cl: str, tone: str) -> list[tuple[int, int]]:
    """Every place a FIELD is drawn: an opening wall, paper, a closing wall.

    **THE FIRST VERSION OF THIS LAW WAS A CHARACTER SCAN AND IT PASSED TWICE
    ON A SCREEN THAT HAS NO FIELD.**  It asked whether any cell anywhere
    carried the wall glyph in the wall tone, and instrument (5 cells) and
    industrial (2) said yes -- instrument because `⠶` is that kit's chrome as
    well as its wall, industrial because `▐` and `▌` are half blocks it spends
    everywhere.  That is spec.md section 23.3.1 exactly, one instrument
    further out: `role_map` keyed by CHARACTER credited darkside's prose `o`
    to its severity family, and inc87 fixed it by asking what the CONTRACT
    PAINTS instead.  A law written the old way here would have shipped two
    green cells for a state neither kit draws.

    So the seat is the SHAPE `field_form` declares -- wall, one or more cells
    of paper, wall -- with both walls in `field_wall_tone`'s tier and the
    paper in a different one, which is that method's own doctrine ("the
    field's PAPER is still drawn in `dim` ... what changes is the tier of two
    cells per field").  Returned as `(row, column)` pairs so a caller can say
    WHERE, not merely how many.
    """
    out: list[tuple[int, int]] = []
    for y, row in enumerate(cells):
        for x in range(len(row)):
            if not _at(row, x, op, tone):
                continue
            i = x + len(op)
            j = i
            while j < len(row) and row[j][1].lower() != tone.lower():
                j += 1
            if j > i and _at(row, j, cl, tone):
                out.append((y, x))
    return out


def judge(lang: str, sides: dict[int, dict]) -> dict[int, tuple[bool, str]]:
    """The six laws for one language: `{step: (passed, what was measured)}`."""
    k = LG.kit(lang)
    t = TH.THEMES[lang]
    cells = {n: cells_of(s) for n, s in sides.items()}
    v: dict[int, tuple[bool, str]] = {}

    # K1 -- the page opens with the app's declared AUTO_FOCUS seat lit.
    f1 = sides[1]["focus"]
    v[1] = (f1["id"] is not None,
            f"focus {f1['id'] or 'NONE'} ({f1['cls']})")

    # K2 -- the seat that holds focus is DRAWN differently than it was when it
    # did not hold it.  Judged on the focused widget's own region, so a change
    # somewhere else on the page cannot pass this.
    f2 = sides[2]["focus"]
    if f2["region"] is None:
        v[2] = (False, "nothing holds focus after three tabs")
    else:
        a, b = _box(cells[1], f2["region"]), _box(cells[2], f2["region"])
        n = sum(1 for ra, rb in zip(a, b) for ca, cb in zip(ra, rb)
                if ca != cb)
        v[2] = (n > 0, f"{f2['id'] or f2['cls']} region {f2['region']}: "
                       f"{n} cells differ from K1")

    # K3 -- the band exists, and its ground is the kit's own panel.
    band = sides[3]["band"]
    if band is None:
        v[3] = (False, f"no modal box on {sides[3]['screen']}")
    else:
        inside = _box(cells[3], band)
        grounds = {c[2] for row in inside for c in row}
        v[3] = (t["panel"] in grounds,
                f"band {band} on {sides[3]['screen']}, "
                f"{'panel' if t['panel'] in grounds else 'NOT panel'} "
                f"({t['panel']})")

    # K4 -- restoration, cell for cell, against the frame the modal covered.
    same = cells[4] == cells[RESTORE_AGAINST]
    d1 = sum(1 for ra, rb in zip(cells[4], cells[1])
             for ca, cb in zip(ra, rb) if ca != cb)
    v[4] = (same, f"K4 {'==' if same else '!='} K{RESTORE_AGAINST} cell for "
                  f"cell; {d1} cells from K1 (the focus walk)")

    # K5 -- the language's declared INVALID field, drawn as a SEAT and not as
    # a loose character: see `field_seats`.
    op, _rune, cl = k.field_form(LG.INVALID, "textfield")
    tone = k.field_wall_tone(LG.INVALID, "textfield")
    seats = field_seats(cells[5], op, cl, tone)
    loose = sum(1 for row in cells[5] for c in row
                if c[0] in (op, cl) and c[1].lower() == tone.lower())
    v[5] = (bool(seats), f"field {op!r}..{cl!r} in {tone} on "
                         f"{sides[5]['screen']}: {len(seats)} seats "
                         f"({loose} loose cells carry a wall glyph)")

    # K6 -- the run the query found, on the channel the kit declares.
    #
    # REVERSE IS READ OFF THE BACKGROUND, and it has to be.  `cell_grid`
    # resolves `Style.reverse` into the (ink, ground) pair it always was, so a
    # reverse match run arrives with the match ink in the BG field -- reading
    # `fg` for those three kits would have asked darkside, industrial and
    # solari a question about the wrong half of the cell.
    style = k.MATCH_STYLE
    word, token = style.split()[0], style.strip().split()[-1].strip("{}")
    ink = t.get(token, t["ink"])
    found = []
    for row in cells[6]:
        for c in row:
            if not c[0].strip():
                continue
            if word == "reverse":
                if c[2].lower() == ink.lower():
                    found.append(c)
            elif c[1].lower() == ink.lower() and c[3 if word == "bold" else 4]:
                found.append(c)
    v[6] = (bool(found), f"{style} -> {word} {ink}: {len(found)} cells "
                         f"on {sides[6]['screen']}")
    return v


#: THE ONE SIDECAR FIELD THAT IS NOT REPRODUCIBLE, and it is named rather than
#: quietly dropped.  `settle_reads` is how many reads the harness spent before
#: the frame stopped changing; it lands on 8 (the floor `STABLE_READS` sets) or
#: 9 depending on where the event loop was when the key arrived.  The FRAME is
#: deterministic -- 198 artefacts byte for byte across two processes -- and the
#: number of looks it took to get there is not, because it is a fact about the
#: scheduler and not about the picture.  Both are in the sidecar; only one is
#: in the bargain, and this constant is the difference written down.
UNPINNED = ("settle_reads",)


def check_reproducible(out: Path) -> tuple[list[str], set[int]]:
    """Re-run the whole script in a SEPARATE PROCESS and diff every artefact.

    The same bargain `raster.check_reproducible` makes.  It matters more here
    than there: this file drives a live app with timers, workers and a focus
    ring, and every one of those is a candidate for a frame that reproduces
    perfectly inside one interpreter and not across two.

    The sidecars are diffed too, with `UNPINNED` masked out, so the grid the
    laws are judged on is in the bargain and not only the pictures.  Returns
    `(drift, the read counts both arms spent)`.
    """
    import tempfile
    reads: set[int] = set()
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([sys.executable, "-X", "utf8",
                            str(Path(__file__).resolve()), "--keys-to", td],
                           capture_output=True, text=True,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        if r.returncode != 0:
            raise RuntimeError(f"control run failed:\n{r.stderr[-1500:]}")
        drift = []
        for lang in LANGS:
            for st in SCRIPT:
                for ext in ("txt", "svg", "png"):
                    a = out / f"{lang}_K{st.n}.{ext}"
                    b = Path(td) / f"{lang}_K{st.n}.{ext}"
                    if not b.exists():
                        drift.append(f"{lang}_K{st.n}.{ext} MISSING")
                    elif a.read_bytes() != b.read_bytes():
                        drift.append(f"{lang}_K{st.n}.{ext}")
                pair = []
                for p in (out, Path(td)):
                    d = json.loads(
                        (p / f"{lang}_K{st.n}.json").read_text(
                            encoding="utf-8"))
                    reads.add(d["settle_reads"])
                    pair.append({k: v for k, v in d.items()
                                 if k not in UNPINNED})
                if pair[0] != pair[1]:
                    drift.append(f"{lang}_K{st.n}.json")
    return drift, reads


def main(argv: list[str]) -> int:
    if "--keys-to" in argv:              # the control arm: run, write, be quiet
        d = Path(argv[argv.index("--keys-to") + 1])
        asyncio.run(sweep(d, metrics_for(FALLBACK_CELLS)))
        return 0

    print(f"{len(LANGS)} languages x {len(SCRIPT)} key steps | "
          f"viewport {SIZE[0]}x{SIZE[1]} cells | the widget slice, driven")
    for st in SCRIPT:
        print(f"  K{st.n} {st.name:<8} "
              + ("(no key)" if not st.keys else " ".join(st.keys)))

    OUT.mkdir(parents=True, exist_ok=True)
    # PASS ONE writes the text so `key_cells()` has a corpus to read; the
    # metrics that cover it are built from that corpus and PASS TWO paints.
    # Two passes rather than a guess, because the declaration below is the
    # thing that has to be checkable.
    asyncio.run(sweep(OUT, None))
    cells = key_cells()
    missing = RA.uncovered(RA.FONT_PATH, cells)
    if missing != FALLBACK_CELLS:
        print(f"the key corpus's uncovered cells are {missing!r}, declared "
              f"{FALLBACK_CELLS!r} -- update FALLBACK_CELLS and say why",
              file=sys.stderr)
        return 1
    still = RA.uncovered(RA.FALLBACK_PATH, FALLBACK_CELLS)
    if still:
        print(f"{RA.FALLBACK_NAME} does not cover {still!r}", file=sys.stderr)
        return 1
    m = metrics_for(FALLBACK_CELLS)
    print(f"\n  face      {RA.FONT_NAME} {RA.FONT_PX}px, cell {m.w}x{m.h} px")
    print(f"  corpus    {len(cells)} distinct cells, "
          f"{len(cells) - len(FALLBACK_CELLS)} in the face")
    print(f"  fallback  {RA.FALLBACK_NAME} for {FALLBACK_CELLS} "
          f"at {m.fallback_px} px")
    got = asyncio.run(sweep(OUT, m))
    if len(got) != len(LANGS) * len(SCRIPT):
        print("INCOMPLETE SWEEP", file=sys.stderr)
        return 1

    by: dict[str, dict[int, dict]] = {}
    for s in got:
        by.setdefault(s["lang"], {})[s["step"]] = s

    print(f"\n  {'language':<11} " + " ".join(f"K{s.n}" for s in SCRIPT)
          + "   settle reads")
    fails: list[tuple[str, int, str]] = []
    verdicts = {lang: judge(lang, by[lang]) for lang in LANGS}
    for lang in LANGS:
        v = verdicts[lang]
        row = " ".join(" ok" if v[s.n][0] else "  X" for s in SCRIPT)
        reads = ",".join(str(by[lang][s.n]["settle_reads"]) for s in SCRIPT)
        print(f"  {lang:<11} {row}   {reads}")
        for s in SCRIPT:
            if not v[s.n][0]:
                fails.append((lang, s.n, v[s.n][1]))

    print()
    for lang in LANGS:
        for s in SCRIPT:
            ok, why = verdicts[lang][s.n]
            print(f"  {lang:<11} K{s.n} {'ok  ' if ok else 'FAIL'} {why}")

    print("\n  re-running the script in a fresh process to check "
          "determinism...")
    drift, reads = check_reproducible(OUT)
    if drift:
        print(f"NON-DETERMINISTIC KEY FRAMES: {drift}", file=sys.stderr)
        return 1
    n = len(LANGS) * len(SCRIPT)
    kb = sum((OUT / f"{lang}_K{s.n}.png").stat().st_size
             for lang in LANGS for s in SCRIPT) / 1024
    print(f"  {n * 4} artefacts identical across two PROCESSES "
          f"({n} .txt + {n} .svg + {n} .png + {n} .json)")
    print(f"  settle reads {sorted(reads)} -- {UNPINNED[0]} is the one field "
          f"NOT in the bargain, and it is masked, not dropped")
    print(f"\n  {n} .png + {n} .json -> {OUT}   ({kb:.0f} KB of PNG)")
    print(f"  LAWS: {n - len(fails)} of {n} hold, {len(fails)} FAIL "
          f"-- recorded, not fixed here")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
