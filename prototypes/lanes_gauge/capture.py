"""Headless capture of the gauge-board prototypes -> SVG frames + TXT.

    python prototypes/lanes_gauge/capture.py

Two synthetic fixtures (late-skewed and calm) so the dials demo both ends of
their range. The needle sweep is captured as 4 real frames (t = 0, .45, .8, 1)
for the HTML flipbook — every frame is a genuine render, no drawn-over fakery.
"""
from __future__ import annotations

import io
import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rich.console import Console

from taskboard.models import Board

import proto

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

TODAY = date(2026, 8, 17)
OUT = Path(__file__).resolve().parent / "out"
FIX_LATE = ROOT / "prototypes" / "out" / "_fixture_late.json"
FIX_CALM = ROOT / "prototypes" / "out" / "_fixture_calm.json"

FRAMES = (0.0, 0.45, 0.8, 1.0)        # ~out-cubic sweep, 4 frames ≈ 600 ms


def save(text, name: str, title: str, w: int, h: int) -> None:
    # rich 15: Console.size honours _width ONLY when height is set too —
    # without it every >80-col line wraps in the SVG export.
    rec = Console(record=True, width=w + 2, height=h + 10,
                  force_terminal=True, legacy_windows=False,
                  color_system="truecolor", file=io.StringIO())
    rec.print(text)
    rec.save_svg(str(OUT / name), title=title)


def capture() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for fix in (FIX_LATE, FIX_CALM):
        if not fix.exists():
            raise SystemExit(f"FIXTURE MISSING: {fix}")
    late = Board.load(FIX_LATE)
    calm = Board.load(FIX_CALM)
    sel_l = late.visible_tasks(False)[5].id
    sel_c = calm.visible_tasks(False)[5].id

    plain_all: list[str] = []
    GRID_COLS = {"g1": 3, "g2": 2}
    for v, cols in GRID_COLS.items():
        for i, s in enumerate(FRAMES):
            save(proto.render_grid_board(late, False, sel_l, TODAY, 118, 30,
                                         cols, sweep=s),
                 f"grid-{v}-f{i}-118.svg", f"grid {v} frame {i}", 118, 30)
        save(proto.render_grid_board(late, False, sel_l, TODAY, 68, 24, 2),
             f"grid-{v}-68.svg", f"grid {v} narrow", 68, 24)
        save(proto.render_grid_board(calm, False, sel_c, TODAY, 118, 30, cols),
             f"grid-{v}-calm-118.svg", f"grid {v} calm", 118, 30)
        print(f"wrote grid-{v} (4 frames + narrow + calm)")

        text = proto.render_grid_board(late, False, sel_l, TODAY, 118, 30,
                                       cols)
        plain = Console(width=122, height=40, force_terminal=False,
                        legacy_windows=False)
        with plain.capture() as cap:
            plain.print(text)
        plain_all.append(f"{'=' * 118}\n=== GRID {v.upper()} · 118x30\n"
                         f"{'=' * 118}\n" + cap.get())

    (OUT / "lanes-gauge.txt").write_text("\n".join(plain_all),
                                         encoding="utf-8")
    print("wrote lanes-gauge.txt")


if __name__ == "__main__":
    capture()
