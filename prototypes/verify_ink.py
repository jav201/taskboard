"""Ink-fraction measurement for every visual language x size class.

DENSITY.md defines ink fraction as (non-space cells / total cells) over the
rendered surface, with a floor of ~35% on a glance surface.

    python prototypes\\verify_ink.py [height]      # default height 26

Set PYTHONIOENCODING=utf-8 on Windows or the print() of drawn glyphs dies with
UnicodeEncodeError under cp1252 -- the script fails, not the app.

TWO self-checks run before any measurement is reported, because the first
version of this probe returned 0.0% for every language and that was the PROBE,
not the app (HANDOFF.md: "verify the probe before believing the verdict"):

  1. arithmetic -- known strips must reproduce 0.00 / 1.00 / 0.50
  2. capture    -- a screen that comes back empty must raise, not read as 0%

KNOWN LIMITATION: run-to-run variance of several points has been observed on
the board class (naught measured 38.0% and 44.2% at the same geometry). The
cause is NOT established -- animation phase is the suspicion, not a finding.
Pin it before using these numbers as an acceptance threshold.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes" / "widget_slice"))

import app as APP                                   # noqa: E402
from app import TaskboardWidget                     # noqa: E402
from taskboard import themes as TH                  # noqa: E402

FLOOR = 0.35                                        # DENSITY.md, glance surface
SIZES = (("glance", 40), ("widget", 60), ("board", 110))


def ink_fraction(rows: list[str]) -> tuple[float, int, int]:
    """non-space cells / total cells."""
    total = sum(len(r) for r in rows)
    inked = sum(sum(1 for c in r if c != " ") for r in rows)
    return (inked / total if total else 0.0), inked, total


def _self_check_arithmetic() -> None:
    cases = ((["    ", "    "], 0.0), (["####", "####"], 1.0), (["##  ", "  ##"], 0.5))
    for rows, want in cases:
        got = ink_fraction(rows)[0]
        assert abs(got - want) < 1e-9, f"PROBE BROKEN: {rows} -> {got}, want {want}"
    print("self-check 1/2  arithmetic OK (0.00 / 1.00 / 0.50 reproduced)")


def _capture(app) -> list[str]:
    """Composited screen text. Raises rather than returning a misleading 0%."""
    rows = [s.text for s in app.screen._compositor.render_strips()]
    if not rows:
        raise AssertionError("CAPTURE BROKEN: compositor returned no strips")
    if not any(c != " " for r in rows for c in r):
        raise AssertionError("CAPTURE BROKEN: screen captured completely blank")
    return rows


async def main() -> int:
    height = int(sys.argv[1]) if len(sys.argv) > 1 else 26
    _self_check_arithmetic()

    langs = list(TH.THEMES)
    table: dict[tuple[str, str], float] = {}

    print(f"self-check 2/2  capture verified per measurement (raises on blank)\n")
    print(f"height={height}")
    print(f"{'language':<12}" + "".join(f"{n:>10}" for n, _ in SIZES))
    print("-" * (12 + 10 * len(SIZES)))

    for lang in langs:
        row = []
        for cls_name, w in SIZES:
            APP.apply_theme(lang)
            app = TaskboardWidget()
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
    print(f"\nDENSITY.md floor: {FLOOR * 100:.0f}% on a glance surface.")
    print(f"below floor at glance: {len(below)}/{len(langs)}")
    for lang, frac in below:
        print(f"  {lang:<12} {frac * 100:.1f}%")
    return 0


sys.exit(asyncio.run(main()))
