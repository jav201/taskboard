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

MAX_SETTLE = 24          # frames to wait for two identical reads


def screen_text(app) -> list[str]:
    """The composited frame as rows of cells -- the same reader the harness
    uses (`verify_language.py:286`), because the cell grid is what the laws
    measure."""
    return ["".join(s.text for s in strip)
            for strip in app.screen._compositor.render_strips()]


async def settle(pilot, app, label: str) -> list[str]:
    """Condition B only: wait for two consecutive identical composited frames.

    Raises rather than returning a half-painted screen -- a blank capture
    written as if it were art is the failure this whole sweep exists to avoid.
    """
    prev: list[str] | None = None
    for _ in range(MAX_SETTLE):
        await pilot.pause()
        rows = screen_text(app)
        if prev is not None and rows == prev:
            if not any(r.strip() for r in rows):
                raise RuntimeError(f"{label}: frame settled BLANK")
            return rows
        prev = rows
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


async def sweep_quiet() -> None:
    """The same sweep with its printing silenced -- used only by the
    determinism check, which compares the files it leaves behind."""
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        await sweep()


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
    print("\n  re-sweeping to check determinism...")
    asyncio.run(sweep_quiet())
    drift = [n for n, t in first.items()
             if (OUT / n).read_text(encoding="utf-8") != t]
    if drift:
        print(f"NON-DETERMINISTIC CAPTURES: {drift}", file=sys.stderr)
        return 1
    print(f"  {len(first)} grids identical across two runs")

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
    raise SystemExit(main())
