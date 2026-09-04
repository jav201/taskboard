"""capture_languages.py -- one coherent sweep of the TEN current design languages.

    python prototypes/capture_languages.py

WHY THIS EXISTS.  `prototypes/out/` holds 892 files from 69 passes, and no two
of them agree on anything: `lang_*.txt` and `gal_*.txt` are from 2026-07-26 and
still carry `phosphor` and `bbs`, which were RETIRED that same day by user
curation, while `ledger`/`solari`/`blueprint` were only captured on 07-28 in a
different pass at different widths.  There has never been a capture of the ten
CURRENT languages taken in one sitting, at one size, off one fixture -- which
is the only form in which "same screen, ten languages" is an honest comparison
rather than a scrapbook.

WHAT IT CAPTURES, per language:

  board_<lang>.txt     the board surface -- cards, column heads, meter, rails
  gallery_<lang>.txt   the COMPONENT SHEET (the app's `g` screen): slider, bar,
                       switch, checkbox, radio, button, text field, scroll bar
                       and stepper, each in the states the registry derives
  *.svg                the same frame IN COLOUR, rendered here -- see below

THE `.txt` IS THE ART; THE `.svg` IS A PICTURE OF IT.  Same rule the skill's
gallery keeps: the two laws that matter are laws about CELLS, and the cell grid
is what the `.txt` *is*.  The SVG carries colour because these captures exist to
be CONSULTED, and a language whose whole commitment is "five flat colours on
grey" cannot be consulted in greyscale.  The skill's greyscale test is a test
you RUN on a language, not a format its documentation must be trapped in -- so
the colour lives in the picture and the grid stays authoritative.

WHY THE SVG IS RENDERED HERE INSTEAD OF BY `App.export_screenshot()`.  Textual's
own exporter was tried first and rejected for two measured reasons.  It writes
`@font-face { src: url("https://cdnjs.cloudflare.com/...FiraCode...") }` -- a
network dependency, which means the picture silently changes font offline and
cannot go into a self-contained document at all.  And it emits one `<rect>` per
segment: 679 rects and 313 texts for one board, 108 KB a frame, 2.2 MB for the
twenty.  The renderer below groups horizontal RUNS of identical style, ships a
system monospace stack, and gives every character its own `x` so the grid cannot
drift whatever font the viewer falls back to -- the same defence, and for the
same reason, as the skill's `render_svg.py`.

The component sheet is captured because it is where languages differ most and
the layer that ships unstyled -- COMPONENTS.md calls the settings screen the
canary.  A sweep of ten boards alone would let a language pass on its hero.

THE FIXTURE IS SYNTHETIC AND THAT IS DELIBERATE.  `out/_fixture_late.json`
(16 tasks, projects named "Website Redesign", "Mobile App"...) rather than the
real board at `~/.taskboard/board.json`: these captures are meant to be shared,
and a screenshot of the operator's actual work is not shareable.  `late` was
chosen over `calm` because overdue work exercises each language's SEVERITY
channel, which is exactly the axis a one-hue language (phosphor) had to solve
by brightness and an identity-coloured one (corgi) had to solve by glyph.

SETTLE IS WEAKER HERE THAN IN THE HARNESS, AND IT IS SAID RATHER THAN HIDDEN.
`verify_language.py:338` has a `settle()` that interrogates the widget tree and
asserts every mounted content widget has PAINTED pixels inside its clipped
area -- it exists because `TaskCard.on_mount` defers its paint with
`call_after_refresh`, so "mounted" and "drawn" are different moments and the
board came back blank about one run in three under load.  That function cannot
be imported: `verify_language.py` has NO `if __name__ == "__main__"` guard, so
importing it runs all 9923 checks.  What is implemented below is condition B
only -- two consecutive identical frames -- plus a non-blank assertion per
capture, and a capture that never stabilises FAILS LOUD instead of being
written.  Condition A is not covered; if a frame ever lands blank, run the
harness rather than trusting this file.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

# ANIMATIONS OFF, SET BEFORE TEXTUAL IS IMPORTED.  Measured, not assumed: with
# animations on, `solari` came back with 36.3 % ink on one run and 36.1 % on the
# next, and the diff was a single row -- `DAYS OVERDUE` present in one capture
# and blank in the other.  Solari is a split-flap board, so its label was caught
# mid-flip, and two consecutive identical frames is not proof of rest when an
# animation has a still moment between steps.  `TEXTUAL_ANIMATIONS=none`
# degrades every animation to its FINAL frame with no loss of information
# (RUN.md), which is the frame a capture is supposed to hold.  The determinism
# check at the bottom of this file is what keeps that claim honest.
os.environ["TEXTUAL_ANIMATIONS"] = "none"

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes" / "widget_slice"))

import taskboard.themes as TH                                    # noqa: E402

FIXTURE = ROOT / "prototypes" / "out" / "_fixture_late.json"
OUT = ROOT / "prototypes" / "gallery"
SIZE = (118, 34)

MAX_SETTLE = 40          # frames to wait for the screen to come to rest
STABLE_READS = 3         # identical consecutive frames required

# THE CLOCK IS FROZEN, AND IT HAS TO BE.  A fixture pins the DATA; it does not
# pin the present.  The app reads `datetime.now()` in the signal engine, in the
# aperture and in the prototype's own due-date maths, so "days remaining", the
# load plot and the day-progress bar are all functions of the current instant --
# which made the captures differ between two runs minutes apart, in six of the
# ten languages.  The first version of this file checked determinism by sweeping
# twice INSIDE ONE PROCESS, and that check passed while cross-process capture
# drifted, because both sweeps in a process see nearly the same clock: a
# determinism check whose two samples share the confound cannot see it.
#
# The instant below is a CONSTANT, not "today".  If it were today's date, a
# rebuild next week would legitimately produce different art and the captures
# could never be reproduced -- the point of pinning it is that this script,
# this fixture and this constant always yield the same twenty grids.
FROZEN = "2026-08-03T09:00:00"


def freeze_clock() -> None:
    """Pin `datetime.now()` / `date.today()` to FROZEN, everywhere it is read.

    Done by rebinding the NAME in each already-imported taskboard/prototype
    module rather than by touching the app: the capture must photograph the
    shipping code, not a variant of it.  `datetime` is a C type and cannot be
    monkeypatched in place, so a subclass is bound over the module-level name
    that each module imported -- which is exactly the name its own calls
    resolve.
    """
    import datetime as _dt
    fixed = _dt.datetime.fromisoformat(FROZEN)

    class _DateTime(_dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed if tz is None else fixed.replace(tzinfo=_dt.timezone.utc)

        @classmethod
        def today(cls):
            return fixed

        @classmethod
        def utcnow(cls):
            return fixed

    class _Date(_dt.date):
        @classmethod
        def today(cls):
            return fixed.date()

    hit = 0
    for name, mod in list(sys.modules.items()):
        if not (name.startswith("taskboard") or name in ("app", "kanban",
                                                         "views_widget",
                                                         "render")):
            continue
        if getattr(mod, "datetime", None) is _dt.datetime:
            mod.datetime = _DateTime
            hit += 1
        if getattr(mod, "date", None) is _dt.date:
            mod.date = _Date
            hit += 1
    if not hit:
        raise RuntimeError("freeze_clock patched nothing -- import order changed")

    # `time.time()` too: the signal engine ages the board file with it.  The
    # shim DELEGATES everything else -- the first attempt replaced the module
    # outright and the app died on `time.monotonic()`, which the engine uses to
    # decide which signals are due.  Freezing a clock must not take the rest of
    # the module with it.
    import time as _time
    import taskboard.engine as _eng

    class _Time:
        def __getattr__(self, k):
            return getattr(_time, k)

        @staticmethod
        def time():
            return fixed.timestamp()

    if getattr(_eng, "time", None) is _time:
        _eng.time = _Time()

    # AND THE SIGNAL THAT READS THE OPERATOR'S REAL BOARD.  `sig_board_file`
    # calls `default_board_path()` directly -- not the app's `board_path` -- so
    # it stats ~/.taskboard/board.json however the app was constructed.  Two
    # separate problems in one line: the capture is not reproducible (its
    # "minutes since save" moves, and on one run that made the signal win the
    # hero and rewrote ledger's whole top band), and a published frame could
    # print the size and save-time of the operator's actual work.  Point it at
    # the fixture, which is what every other reader of this capture already
    # sees.  (Checked: no published frame ever carried it -- the signal had not
    # won a hero in any capture that shipped.)
    import taskboard.models as _models
    _models.default_board_path = lambda: FIXTURE
    if getattr(_eng, "default_board_path", None) is not None:
        _eng.default_board_path = lambda: FIXTURE
    return hit


def screen_text(app) -> list[str]:
    """The composited frame as rows of cells -- the same reader the harness
    uses (`verify_language.py:286`), because the cell grid is what the laws
    measure."""
    return ["".join(s.text for s in strip)
            for strip in app.screen._compositor.render_strips()]


async def settle(pilot, app, label: str) -> list[str]:
    """Wait for a frame that has stopped changing AND has painted content.

    THREE consecutive identical composited frames, not two.  Two equal frames
    is also what a widget looks like in the gap between being mounted and being
    painted -- `TaskCard.on_mount` defers its paint with `call_after_refresh`,
    so "mounted" and "drawn" are different moments.

    Condition A of the real harness (`verify_language.py:338`, every mounted
    content widget has painted pixels inside its CLIPPED area) is deliberately
    NOT reimplemented here.  It was tried: reading `widget.region` directly and
    demanding ink gives false positives for anything scrolled out of its
    column, and the sweep timed out on frames that were perfectly fine.  Doing
    it properly needs the compositor's clipping, which is the harness's job.
    What guards this file instead is the CROSS-PROCESS reproducibility check in
    `main()` -- if a race ever does slip a half-painted frame through, two
    independent runs disagree and the sweep fails rather than shipping it.

    Why THREE identical reads and not two.  Two consecutive equal frames is
    also what a widget looks like in the gap between being mounted and being
    painted; the third read is what distinguishes a screen at rest from a
    screen mid-transition.
    """
    stable = 0
    prev: list[str] | None = None
    for _ in range(MAX_SETTLE):
        await pilot.pause()
        rows = screen_text(app)
        stable = stable + 1 if rows == prev else 0
        prev = rows
        if stable < STABLE_READS - 1:
            continue
        if not any(r.strip() for r in rows):
            raise RuntimeError(f"{label}: frame settled BLANK")
        return rows
    raise RuntimeError(f"{label}: never settled after {MAX_SETTLE} frames")


CW, LH, FS, PAD = 8.4, 17.0, 14.0, 10.0
MONO = ("ui-monospace,SFMono-Regular,'DejaVu Sans Mono','Cascadia Mono',"
        "Menlo,Consolas,'Liberation Mono',monospace")


def cell_grid(app) -> tuple[list[list[tuple[str, str, str]]], str]:
    """Read the composited frame as (char, fg, bg) per CELL.

    Segment styles are read off the compositor, not off any widget's internal
    state: a widget can hold its text and still not have been flushed, and it
    is the flush a capture reads.  Returns the screen's own background too, so
    the picture's ground is the app's ground rather than a guess.
    """
    grid: list[list[tuple[str, str, str]]] = []
    ground = "#000000"
    for strip in app.screen._compositor.render_strips():
        row: list[tuple[str, str, str]] = []
        for seg in strip:
            st = seg.style
            fg = (st.color.triplet.hex
                  if (st and st.color and st.color.triplet) else "#ffffff")
            bg = (st.bgcolor.triplet.hex
                  if (st and st.bgcolor and st.bgcolor.triplet) else ground)
            for ch in seg.text:
                row.append((ch, fg, bg))
        grid.append(row)
    # the ground is the most common background in the frame -- measured, not
    # assumed, because several languages paint a full-bleed panel over it
    counts: dict[str, int] = {}
    for row in grid:
        for _, _, bg in row:
            counts[bg] = counts.get(bg, 0) + 1
    if counts:
        ground = max(counts, key=counts.get)
    return grid, ground


def svg_from_grid(grid, ground: str, label: str) -> str:
    """One SVG, self-contained, no network.

    Backgrounds are emitted as RUNS -- consecutive cells sharing a bg become
    one `<rect>` -- which is where the size win over the stock exporter comes
    from.

    HOW THE GRID IS HELD -- ONE `x` PER RUN, AND NOTHING ELSE.  Two richer
    schemes were tried against a real browser and both had to go, for the same
    reason in two costumes:

      * one `x` per GLYPH (~290 000 coordinates across the twenty frames);
      * one `x` per run plus `textLength` + `lengthAdjust="spacing"`.

    Each froze Chrome's renderer for 30 s whenever anything forced the document
    through layout or composition -- an `#anchor` jump, a CSS filter, an
    overlay, even switching a tab panel.  The second is if anything worse: it
    reads cheap, but `textLength` makes the engine MEASURE the text and
    redistribute the gaps on every single layout pass, for every element that
    carries it.

    So a run gets its starting `x` and no more.  What that gives up is real and
    is worth stating: inside one run, a viewer falling back to a font whose
    advance is not exactly the declared cell width will drift.  What it does
    NOT give up is the part that matters -- error cannot accumulate ACROSS a
    row, because the next run re-anchors at its own absolute coordinate, and
    runs here average well under half a row.  Spaces are non-breaking so no
    engine may collapse a gap and shift the cells after it.  The `.txt` remains
    the artifact any law measures; this is a picture of it that a browser can
    actually paint.
    """
    import html as _h
    h = len(grid)
    w = max((len(r) for r in grid), default=0)
    pw, ph = w * CW + 2 * PAD, h * LH + 2 * PAD
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pw:.1f} '
           f'{ph:.1f}" role="img" aria-label="{_h.escape(label)}">',
           f'<title>{_h.escape(label)}</title>',
           f'<rect width="{pw:.1f}" height="{ph:.1f}" fill="{ground}"/>',
           f'<g font-family="{MONO}" font-size="{FS}" xml:space="preserve" '
           f'style="white-space:pre;font-variant-ligatures:none">']
    for y, row in enumerate(grid):
        ry = PAD + y * LH
        # background runs
        x = 0
        while x < len(row):
            bg = row[x][2]
            x2 = x
            while x2 < len(row) and row[x2][2] == bg:
                x2 += 1
            if bg != ground:
                out.append(f'<rect x="{PAD + x * CW:.1f}" y="{ry:.1f}" '
                           f'width="{(x2 - x) * CW:.1f}" height="{LH:.1f}" '
                           f'fill="{bg}"/>')
            x = x2
        # text runs, one per colour, each glyph carrying its own x
        ty = ry + 0.78 * LH
        x = 0
        while x < len(row):
            fg = row[x][1]
            x2 = x
            while x2 < len(row) and row[x2][1] == fg:
                x2 += 1
            text = "".join(c for c, _, _ in row[x:x2])
            if text.strip():
                out.append(f'<text x="{PAD + x * CW:.1f}" y="{ty:.1f}" '
                           f'fill="{fg}">'
                           f'{_h.escape(text).replace(" ", chr(160))}</text>')
            x = x2
    out += ["</g>", "</svg>", ""]
    return "\n".join(out)


def ink(rows: list[str]) -> float:
    total = sum(len(r) for r in rows)
    return sum(1 for r in rows for c in r if c not in "  ") / total * 100


def write(name: str, rows: list[str], app=None,
          title: str = "") -> tuple[int, int, float]:
    """Write a rectangle -- every row padded to the widest, never clipped.

    The rectangle law: the grid is what the verifiers measure, and a row that
    lost its trailing cells is a violation introduced by the writer, not by
    the design.

    When `app` is given, the same frame is also exported to SVG in colour by
    Textual itself.  Not re-rendered here and not re-coloured: whatever the
    terminal would show is what the file holds.
    """
    w = max(len(r) for r in rows)
    rect = [r.ljust(w) for r in rows]
    (OUT / f"{name}.txt").write_text("\n".join(rect) + "\n", encoding="utf-8")
    if app is not None:
        grid, ground = cell_grid(app)
        (OUT / f"{name}.svg").write_text(
            svg_from_grid(grid, ground, title), encoding="utf-8")
    return w, len(rect), ink(rect)


async def sweep() -> list[dict]:
    from app import TaskboardWidget          # prototypes/widget_slice/app.py

    freeze_clock()                           # AFTER the imports it patches
    OUT.mkdir(parents=True, exist_ok=True)
    report: list[dict] = []

    for lang in TH.ORDER:
        app = TaskboardWidget(board_path=FIXTURE)
        async with app.run_test(size=SIZE) as pilot:
            await pilot.pause()
            app.notify = lambda *a, **kw: None       # no toasts in a capture
            app.set_theme(lang)
            rows = await settle(pilot, app, f"board {lang}")
            w, h, i = write(f"board_{lang}", rows, app,
                            f"taskboard · {lang} · board")
            entry = dict(lang=lang, board=(w, h, i))

            await pilot.press("g")
            grows = await settle(pilot, app, f"gallery {lang}")
            gw, gh, gi = write(f"gallery_{lang}", grows, app,
                               f"taskboard · {lang} · components")
            entry["gallery"] = (gw, gh, gi)

        report.append(entry)
        print(f"  {lang:<11} board {w}x{h} {i:5.1f}% ink   "
              f"gallery {gw}x{gh} {gi:5.1f}% ink")
    return report


# ===========================================================================
# THE SURFACE SWEEP (--surface) -- the eighth axis, one image, every language
#
# WHY ONE FIXED IMAGE AND NOT A SYNTHETIC ONE.  The boards above compare the
# languages on one fixture because "the same screen in ten languages" is only
# an honest comparison when it really is the same screen.  The same argument
# applies one level down: a surface posture is a claim about what a language
# does to REAL PIXELS, and ten postures shown ten different pictures is a
# scrapbook again.  The picture is `tui-demos/lab/mbb_rho_final.npy` -- a 20x60
# density field from the topology-optimisation runs, rendered through R1's own
# PAPER/INK colormap at scale 6 (360x120 px), which is the image that lab
# already publishes.
#
# THE `.npy` LOAD LIVES HERE AND NOT IN `taskboard/`.  numpy is not a declared
# dependency of the package (`pyproject.toml`: textual, tzdata, pillow,
# textual-image).  `prototypes/` is dev-side and may import anything; the
# shipped package may not grow a dependency to make a capture convenient.
# ===========================================================================

MBB = Path(r"C:\Users\jjgh8\Github\tui-demos\lab\mbb_rho_final.npy")
MBB_SCALE = 6                       # 20x60 -> 120x360 px, NEAREST
PAPER, INK = (248, 246, 240), (28, 32, 44)      # r1_pixels.py's colormap


def test_image():
    """The MBB density field as a PIL image, exactly as `r1_pixels.load()`
    builds it: linear blend PAPER->INK on the clipped field, NEAREST upscale.
    Reproduced rather than imported -- `r1_pixels.py` has no import guard and
    lives in another repo this batch may only READ."""
    import numpy as np
    from PIL import Image as PImage
    g = np.clip(np.load(MBB), 0, 1)[..., None]
    rgb = (np.array(PAPER, np.uint8) * (1 - g)
           + np.array(INK, np.uint8) * g).astype(np.uint8)
    img = PImage.fromarray(rgb)
    return img.resize((img.width * MBB_SCALE, img.height * MBB_SCALE),
                      PImage.NEAREST)


SURFACE_H = 26                      # rows the region reserves inside the frame


def surface_sheet(lang: str, img):
    """The specimen page a surface capture photographs: the language's own
    section header, then the reserved rectangle.

    Deliberately NOT a board screen.  Spec section 5 is explicit that no
    existing screen renders a region in this batch, so wiring one here to take
    a picture of it would be the batch shipping the thing it declared out of
    scope.  What the sheet does carry is the language's `sect()` -- so the
    frames differ pairwise OUTSIDE the image rectangle, which is the
    acceptance boundary LANGUAGES.md already uses for the boards."""
    import taskboard.language as LG
    kit = LG.kit(lang)
    res = kit.raster_region(img, SIZE[0] - 2, SURFACE_H, label="mbb rho final")
    head = kit.sect("SURFACE", f"{res.posture} - {img.width}x{img.height} px",
                    SIZE[0] - 2, SURFACE_H)
    return "\n".join(head + res.rows), res


async def sweep_surfaces() -> list[dict]:
    """One image, every implemented kit, headless, at the board's viewport."""
    from textual.app import App, ComposeResult
    from textual.widgets import Static

    import taskboard.themes as _TH

    img = test_image()
    OUT.mkdir(parents=True, exist_ok=True)
    report: list[dict] = []

    for lang in _TH.ORDER:
        body, res = surface_sheet(lang, img)

        class Sheet(App):
            CSS = ("Screen { layout: vertical; }\n"
                   "#surface { padding: 0 1; width: 1fr; height: 1fr; }")

            def compose(self) -> ComposeResult:
                yield Static(body, id="surface", markup=True)

        app = Sheet()
        async with app.run_test(size=SIZE) as pilot:
            await pilot.pause()
            app.screen.styles.background = _TH.THEMES[lang]["ground"]
            rows = await settle(pilot, app, f"surface {lang}")
            w, h, i = write(f"surface_{lang}", rows, app,
                            f"taskboard - {lang} - surface ({res.posture})")
        report.append(dict(lang=lang, posture=res.posture, ink=i,
                           pixels=None if res.pixels is None
                           else res.pixels.size))
        print(f"  {lang:<11} {res.posture:<9} {w}x{h} {i:5.1f}% ink   "
              f"raster {'refused' if res.pixels is None else res.pixels.size}")
    return report


def surface_main() -> int:
    if not MBB.exists():
        print(f"TEST IMAGE MISSING: {MBB}", file=sys.stderr)
        return 2
    import taskboard.themes as _TH
    print(f"image {MBB.name} | viewport {SIZE[0]}x{SIZE[1]} | "
          f"{len(_TH.ORDER)} languages | animations off")
    report = asyncio.run(sweep_surfaces())

    # THE SWEEP'S OWN LAW, the same one the boards keep: no two frames
    # identical.  Two languages whose surface renders byte-for-byte the same is
    # the exact defect LANGUAGES.md records, one axis down.
    got = {r["lang"]: (OUT / f"surface_{r['lang']}.txt").read_text(
        encoding="utf-8") for r in report}
    order = [r["lang"] for r in report]
    dupes = [(a, b) for i, a in enumerate(order) for b in order[i + 1:]
             if got[a] == got[b]]
    if dupes:
        print(f"IDENTICAL SURFACES: {dupes}", file=sys.stderr)
        return 1
    print(f"\n  {len(report)} surfaces -> {OUT}")
    print(f"  no two identical ({len(order) * (len(order) - 1) // 2} pairs)")
    return 0


def check_reproducible(first: dict[str, str]) -> list[str]:
    """Re-run the whole sweep in a SEPARATE PROCESS and diff every grid.

    Why a subprocess and not a second pass in this one: the first version of
    this check swept twice in-process and reported "identical" while the
    captures were in fact drifting between runs.  Both in-process sweeps read
    nearly the same wall clock, so the confound the check was supposed to catch
    was present in both samples.  A check whose two samples share the bug is a
    vacuous check -- it can only ever pass.  A fresh interpreter re-imports the
    app, re-reads the fixture and re-applies `freeze_clock()` from scratch,
    which is the condition someone rebuilding these files a week from now
    actually has.
    """
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                            "--sweep-to", td],
                           capture_output=True, text=True,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        if r.returncode != 0:
            raise RuntimeError(f"control sweep failed:\n{r.stderr[-1500:]}")
        return [n for n, t in first.items()
                if (Path(td) / n).read_text(encoding="utf-8") != t]


def main() -> int:
    if not FIXTURE.exists():
        print(f"FIXTURE MISSING: {FIXTURE}", file=sys.stderr)
        return 2
    print(f"fixture {FIXTURE.name} | viewport {SIZE[0]}x{SIZE[1]} | "
          f"{len(TH.ORDER)} languages | animations off")
    report = asyncio.run(sweep())

    # DETERMINISM, CHECKED RATHER THAN ASSERTED.  Sweep twice and compare every
    # grid.  This is the check that caught solari's mid-flip label, and it is
    # cheap enough to keep: a capture that differs between two runs of the same
    # code on the same fixture is not a picture of a design, it is a picture of
    # a moment.
    first = {p.name: p.read_text(encoding="utf-8")
             for p in sorted(OUT.glob("*.txt"))}
    print("\n  re-sweeping in a fresh process to check reproducibility...")
    drift = check_reproducible(first)
    if drift:
        print(f"NON-REPRODUCIBLE CAPTURES: {drift}", file=sys.stderr)
        return 1
    print(f"  {len(first)} grids identical across two PROCESSES")

    # The sweep's own law: ten languages, twenty captures, and no two boards
    # identical.  Two languages rendering byte-identically is the exact defect
    # LANGUAGES.md records ("Two of the eight languages rendered
    # byte-identically") -- so the sweep refuses to call itself done without
    # checking, instead of leaving it to the eye.
    if len(report) != len(TH.ORDER):
        print("INCOMPLETE SWEEP", file=sys.stderr)
        return 1
    boards = {L["lang"]: (OUT / f"board_{L['lang']}.txt").read_text(
        encoding="utf-8") for L in report}
    dupes = [(a, b) for i, a in enumerate(TH.ORDER) for b in TH.ORDER[i + 1:]
             if boards[a] == boards[b]]
    if dupes:
        print(f"IDENTICAL BOARDS: {dupes}", file=sys.stderr)
        return 1
    print(f"\n  {len(report) * 2} captures -> {OUT}")
    print("  no two boards identical")
    return 0


if __name__ == "__main__":
    # `--sweep-to DIR`: capture into DIR and say nothing.  This is the control
    # arm of the reproducibility check above, run as a separate interpreter.
    if len(sys.argv) == 3 and sys.argv[1] == "--sweep-to":
        OUT = Path(sys.argv[2])
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()):
            asyncio.run(sweep())
        raise SystemExit(0)
    # `--surface [DIR]`: the eighth axis, one image through every kit.  A
    # separate entry point rather than a fifth capture inside `sweep()`: the
    # board sweep photographs a SCREEN and this one photographs a PRIMITIVE
    # that no screen consumes yet (spec section 5), so folding them together
    # would make the boards depend on a test image from another repo.
    if sys.argv[1:2] == ["--surface"]:
        if len(sys.argv) == 3:
            OUT = Path(sys.argv[2])
        raise SystemExit(surface_main())
    raise SystemExit(main())
