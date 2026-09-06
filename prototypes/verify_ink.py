"""Ink-fraction measurement — TWO SUBJECTS, AND THEY ARE NOT THE SAME NUMBER.

DENSITY.md defines ink fraction as (non-blank cells / total cells) over the
rendered surface, with a floor of ~35% on a glance surface.

    python -X utf8 prototypes/verify_ink.py [height]   # LIVE widget, 11x3
    python -X utf8 prototypes/verify_ink.py --frames    # the 66 .txt, static

WHY THE TWO MODES EXIST AND WHY EVERY LINE NAMES ITS SUBJECT.  This script
printed a bare table of percentages, and those percentages were then quoted as
though they described `prototypes/components/*.txt` -- the 66 frames a design
round actually judges.  They never did.  The default mode drives the LIVE
`TaskboardWidget` against the late fixture at three widths; the frames are
composed kit sheets photographed at one size and written to disk.  Different
surface, different content, different geometry.  So:

  * the live mode's headline is `glance ink, 11x3, live` -- eleven languages by
    three size classes, off a running widget;
  * `--frames` says `frame ink, 66 frames, static`, and it is the one that can
    be compared with a frame.

NEITHER IS A GATE and neither returns non-zero on a low number.  The floor is
printed as a reading, not as a verdict: DENSITY.md's 35% is a design target for
a glance surface, and a script that failed a build on it would be asserting
that the target had been agreed as a threshold.  It has not.

THE LIVE MODE DRIFTS AND THE DRIFT IS NOT UNDERSTOOD.  Two runs at the same
geometry with nothing changed do not agree.  Measured 2026-09-06, back to back:
`industrial board` 50.8% then 51.5% (0.7 points) and `nord board` 29.2% then
29.3%, with the other 31 cells identical -- so the drift is real, it is small,
and on that pair of runs it stayed out of the `glance` column that DENSITY.md's
floor is read off.  Several points have been seen on the board class before
(naught 38.0% and 44.2%).  The cause is NOT established; animation phase is the
suspicion, not a finding.  `--frames` exists partly because it has no such
problem: it reads files.

Set PYTHONIOENCODING=utf-8 on Windows, or run with `-X utf8`, or the print() of
drawn glyphs dies with UnicodeEncodeError under cp1252 -- the script fails, not
the app.

TWO self-checks run before any measurement is reported, because the first
version of this probe returned 0.0% for every language and that was the PROBE,
not the app (HANDOFF.md: "verify the probe before believing the verdict"):

  1. arithmetic -- known strips must reproduce 0.00 / 1.00 / 0.50, a strip of
     braille blanks must reproduce 0.00, and a drawn braille cell must read as
     ink
  2. capture    -- a screen that comes back empty must raise, not read as 0%
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes" / "widget_slice"))

FLOOR = 0.35                                        # DENSITY.md, glance surface
SIZES = (("glance", 40), ("widget", 60), ("board", 110))
FRAMES = ROOT / "prototypes" / "components"

#: WHAT IS NOT INK.  The ASCII space, and U+2800 BRAILLE PATTERN BLANK.  The
#: second is the whole reason this constant is written down: instrument draws in
#: braille and prism borrows the cell, so `BRAILLE PATTERN BLANK` appears 422
#: times across the 66 frames -- and it is an EMPTY braille cell, a space that
#: happens to live in the braille block.  Counting it as ink hands those two
#: languages a density they do not have.  Measured: only these two blank
#: characters occur in the 66 `.txt` at all.
BLANKS = " ⠀"


# The live board is not this measurement's input. Ink fraction is a number that
# gets PUBLISHED in a table, so measuring it against the operator's tasks makes
# the table both unreproducible and a disclosure. See tests/test_no_live_board.py.
FIXTURE = ROOT / "prototypes" / "out" / "_fixture_late.json"


def ink_fraction(rows: list[str]) -> tuple[float, int, int]:
    """non-blank cells / total cells. ONE formula, both modes."""
    total = sum(len(r) for r in rows)
    inked = sum(sum(1 for c in r if c not in BLANKS) for r in rows)
    return (inked / total if total else 0.0), inked, total


def _self_check_arithmetic() -> None:
    cases = ((["    ", "    "], 0.0), (["####", "####"], 1.0),
             (["##  ", "  ##"], 0.5), (["⠀⠀⠀⠀"], 0.0),
             (["⡀⠀##"], 0.75))
    for rows, want in cases:
        got = ink_fraction(rows)[0]
        assert abs(got - want) < 1e-9, f"PROBE BROKEN: {rows} -> {got}, want {want}"
    print("self-check 1/2  arithmetic OK (0.00 / 1.00 / 0.50 reproduced; a "
          "braille blank reads 0.00, a drawn braille cell reads as ink)")


def _capture(app) -> list[str]:
    """Composited screen text. Raises rather than returning a misleading 0%."""
    rows = [s.text for s in app.screen._compositor.render_strips()]
    if not rows:
        raise AssertionError("CAPTURE BROKEN: compositor returned no strips")
    if not any(c not in BLANKS for r in rows for c in r):
        raise AssertionError("CAPTURE BROKEN: screen captured completely blank")
    return rows


def frames_mode() -> int:
    """`frame ink, 66 frames, static` -- the number that CAN be quoted at a frame.

    Deterministic by construction: it reads `prototypes/components/*_S?.txt`
    off disk with the same `ink_fraction` the live mode uses, so two runs
    cannot disagree and every number here belongs to a NAMED frame."""
    _self_check_arithmetic()
    files = sorted(FRAMES.glob("*_S?.txt"))
    if not files:
        raise AssertionError(f"NO FRAMES: nothing matched {FRAMES}/*_S?.txt")

    got: dict[str, float] = {}
    for f in files:
        rows = f.read_text(encoding="utf-8").rstrip("\n").split("\n")
        got[f.stem], _, _ = ink_fraction(rows)

    langs = sorted({n.rsplit("_", 1)[0] for n in got})
    screens = sorted({n.rsplit("_", 1)[1] for n in got})
    print(f"\nframe ink, {len(got)} frames, static "
          f"({len(langs)} languages x {len(screens)} screens, read from "
          f"{FRAMES.name}/*.txt)\n")
    print(f"{'language':<12}" + "".join(f"{s:>9}" for s in screens))
    print("-" * (12 + 9 * len(screens)))
    for lang in langs:
        print(f"{lang:<12}"
              + "".join(f"{got[f'{lang}_{s}'] * 100:>8.1f}%" for s in screens))

    lo = min(got, key=got.get)
    hi = max(got, key=got.get)
    print(f"\nfloor    {lo:<26} {got[lo] * 100:>6.1f}%")
    print(f"ceiling  {hi:<26} {got[hi] * 100:>6.1f}%")
    print(f"\nDENSITY.md's {FLOOR * 100:.0f}% floor is a GLANCE-surface target "
          "and these are not glance surfaces. Printed above as a reading, not "
          "a verdict; nothing here fails.")
    return 0


async def live_mode() -> int:
    """`glance ink, 11x3, live` -- the running widget at three widths."""
    import app as APP
    from app import TaskboardWidget
    from taskboard import themes as TH

    height = int(sys.argv[1]) if len(sys.argv) > 1 else 26
    _self_check_arithmetic()

    langs = list(TH.THEMES)
    table: dict[tuple[str, str], float] = {}

    print("self-check 2/2  capture verified per measurement (raises on blank)")
    print(f"\nglance ink, {len(langs)}x{len(SIZES)}, live "
          f"(the running TaskboardWidget on the late fixture, height={height}; "
          "widths " + ", ".join(f"{n} {w}" for n, w in SIZES) + ")\n")
    print(f"{'language':<12}" + "".join(f"{n:>10}" for n, _ in SIZES))
    print("-" * (12 + 10 * len(SIZES)))

    for lang in langs:
        row = []
        for cls_name, w in SIZES:
            APP.apply_theme(lang)
            app = TaskboardWidget(board_path=str(FIXTURE))
            async with app.run_test(size=(w, height)) as pilot:
                await pilot.pause()
                APP.apply_theme(lang)          # re-apply: mount resets globals
                app.redraw()
                await pilot.pause()
                frac, _, _ = ink_fraction(_capture(app))
            table[(lang, cls_name)] = frac
            row.append(frac)
        print(f"{lang:<12}" + "".join(f"{f * 100:>9.1f}%" for f in row))

    below = sorted(((l, table[(l, "glance")]) for l in langs
                    if table[(l, "glance")] < FLOOR), key=lambda x: x[1])
    print(f"\nDENSITY.md floor: {FLOOR * 100:.0f}% on a GLANCE surface -- the "
          "`glance` column only, and a reading rather than a gate.")
    print(f"below floor at glance: {len(below)}/{len(langs)}")
    for lang, frac in below:
        print(f"  {lang:<12} {frac * 100:.1f}%")
    print("\nTHIS TABLE DRIFTS between runs with nothing changed (0.6 points "
          "measured 2026-09-06). Cause not established. It describes the LIVE "
          "WIDGET and not the 66 frames -- for those, `--frames`.")
    return 0


if "--frames" in sys.argv[1:]:
    sys.exit(frames_mode())
sys.exit(asyncio.run(live_mode()))
