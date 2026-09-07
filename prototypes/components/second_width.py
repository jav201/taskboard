"""second_width.py -- the same six screens at 80x24.  The other half of E2.

    python -X utf8 prototypes/components/second_width.py

    -> prototypes/components/w80/<lang>_S<n>.txt / .svg / .png / .json

WHY.  Every commitment in `LANGUAGES.md` that says *"at any width"* has been
judged at exactly one width for eleven batches.  Round four's §8.5 is one
sentence long: *«Un solo ancho. Los 66 estan a 100x32. Los compromisos que
dicen "at any width" siguen juzgados a un ancho, e inc54 declaro por escrito
que el asiento destructivo de blueprint paso de 8 a 12 celdas y que nada en
este repo renderiza `S4` por debajo de 100.»*  §9c.2 costs it at *"one line of
`render.py`"*.  It was one line, and the line is `size`.

WHAT THIS FILE IS ALLOWED TO DO.  Set `screens.W, screens.H` and call the
three functions the 100x32 corpus is already made of: `render.frame()` for the
composited grid, `capture_languages.svg_from_grid()` for the picture,
`raster.png_of()` for the raster.  **Nothing is re-implemented and no law is
re-stated here.**  The judging happens in `tests/test_components.py`, where
the laws live, by pointing `FRAMES` at this directory and running them; this
file only produces the frames to point at.

AND IT FIXES NOTHING.  The brief is explicit -- *"Do not fix languages here;
the round judges."*  A frame that comes out worse at 80x24 comes out worse and
is written down.
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes"))
sys.path.insert(0, str(HERE))

import capture_languages as CAP                                  # noqa: E402
import raster as RA                                              # noqa: E402
import render as R                                               # noqa: E402
import screens as S                                              # noqa: E402

#: 80x24 is the VT100's, and it is the width every terminal emulator still
#: opens at when nothing tells it otherwise.  It is also the narrowest width
#: worth asking about: below it a two-pane board stops being a two-pane board
#: and the question becomes "should this language reflow", which is a design
#: question nobody has put.
SIZE = (80, 24)
OUT = HERE / "w80"


async def sweep(size, out: Path) -> list:
    """The 66, at `size`, into `out` -- txt, svg, png and the raster sidecar.

    `screens.W`/`H` are module globals that every sheet builder reads at CALL
    time, which is why a second width costs an assignment and not a rewrite.
    They are set once here and left set: this process renders one width and
    exits, so there is no state to restore and nothing that could half-restore
    it.
    """
    S.W, S.H = size
    out.mkdir(parents=True, exist_ok=True)
    m = RA.Metrics()
    report = []
    for lang in R.LANGS:
        for screen in S.SCREENS:
            sh, rect, grid, ground, over = await R.frame(lang, screen, size)
            name = f"{lang}_{screen}"
            title = f"taskboard · {lang} · {screen} {S.TITLES[screen]}"
            (out / f"{name}.txt").write_text("\n".join(rect) + "\n",
                                             encoding="utf-8")
            (out / f"{name}.svg").write_text(
                CAP.svg_from_grid(grid, ground, title), encoding="utf-8")
            img = RA.png_of(m, grid)
            img.save(out / f"{name}.png", "PNG", optimize=True)
            (out / f"{name}.json").write_text(
                json.dumps({"lang": lang, "screen": screen, "ground": ground,
                            "cols": max(len(r) for r in grid),
                            "rows": len(grid),
                            "image": {"w": img.width, "h": img.height},
                            "txt": {"cols": len(rect[0]),
                                    "rows": len(rect)},
                            **m.as_json(), "grid": RA.runs_of(grid)},
                           ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8")
            report.append(dict(lang=lang, screen=screen, w=len(rect[0]),
                               h=len(rect), ink=CAP.ink(rect), over=over))
    return report


def main() -> int:
    w, h = SIZE
    print(f"{len(R.LANGS)} languages x {len(S.SCREENS)} screens | "
          f"viewport {w}x{h} cells")
    report = asyncio.run(sweep(SIZE, OUT))
    if len(report) != len(R.LANGS) * len(S.SCREENS):
        print("INCOMPLETE SWEEP", file=sys.stderr)
        return 1

    # THE RECTANGLE, and it is a finding rather than a gate: a sheet that
    # asked for more cells than the frame has is CLIPPED, and `Sheet.body()`
    # has reported that since the first sweep.  At 100x32 the number is zero.
    clipped = [(r["lang"], r["screen"], r["over"]) for r in report if r["over"]]
    short = [(r["lang"], r["screen"], r["w"], r["h"]) for r in report
             if (r["w"], r["h"]) != SIZE]
    print(f"\n  rows the sheets had to CUT: "
          f"{sum(len(r[2]) for r in clipped)} in {len(clipped)} frames")
    for lang, screen, over in clipped:
        print(f"    {lang}_{screen}  {over}")
    if short:
        print(f"  frames that did not fill the viewport: {short}")

    # the sweep's own law, unchanged at the new width
    bad = []
    for screen in S.SCREENS:
        got = {L: (OUT / f"{L}_{screen}.txt").read_text(encoding="utf-8")
               for L in R.LANGS}
        for i, a in enumerate(R.LANGS):
            for b in R.LANGS[i + 1:]:
                if got[a] == got[b]:
                    bad.append((screen, a, b))
    if bad:
        print(f"IDENTICAL FRAMES AT {w}x{h}: {bad}", file=sys.stderr)
        return 1
    print(f"  no two frames identical within a screen "
          f"({len(S.SCREENS) * len(R.LANGS) * (len(R.LANGS) - 1) // 2} pairs)")
    print(f"\n  {len(report)} .txt + .svg + .png + .json -> {OUT}")
    lo = min(r["ink"] for r in report)
    hi = max(r["ink"] for r in report)
    print(f"  ink {lo:.1f}% .. {hi:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
