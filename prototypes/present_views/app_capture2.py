"""PROTOTYPE round 2 — D with every task's notes, captured FROM THE APP.

    python prototypes/present_views/app_capture2.py

Same method as app_capture.py (its PresentScreen subclass and pilot runner);
only the view set changes: 1 gantt (line breaks fixed) · 2 stacked ·
3 columns · 4 inline. Frames land in out/ as r2-*.svg / .png."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import app_capture as AC  # noqa: E402  (patches PresentScreen + date on import)
import views_d as VD  # noqa: E402

AC.VP = VD


def main() -> None:
    AC.OUT.mkdir(parents=True, exist_ok=True)
    # open order: component library · checkout 500 (cursor) · image assets ·
    # launch (long note) · SEO redirects (empty note)
    big = [("A-gantt", []),
           ("D2-stacked", ["2"]),
           ("D2-stacked-long", ["right", "right"]),       # cursor on Launch
           ("D2-stacked-pgdn", ["pagedown"]),
           ("D2-stacked-hidden", ["left", "space"]),      # hide image assets
           ("D3-columns", ["a", "3", "left", "left"]),    # back on checkout
           ("D3-columns-long", ["right", "right"]),
           ("D3-columns-hidden", ["left", "space"]),
           ("D4-inline", ["a", "4", "left", "left"]),
           ("D4-inline-long", ["right", "right"]),
           ("D4-inline-hidden", ["left", "space"])]
    asyncio.run(AC.run((118, 31), big, "r2-118"))
    small = [("A-gantt", []),
             ("D2-stacked", ["2"]),
             ("D2-stacked-long", ["right", "right"]),
             ("D3-columns", ["3", "left", "left"]),
             ("D3-columns-long", ["right", "right"]),
             ("D4-inline", ["4", "left", "left"]),
             ("D4-inline-long", ["right", "right"]),
             ("D4-inline-hidden", ["left", "space"])]
    asyncio.run(AC.run((80, 25), small, "r2-80"))
    print("wrote", AC.OUT)


if __name__ == "__main__":
    main()
