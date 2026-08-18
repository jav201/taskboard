"""Headless capture of the gantt variants -> .txt (for review) + .svg.

    python prototypes/capture_gantt.py

The fixture is synthetic so the generated artifacts are safe to commit/share.
"""
from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rich.console import Console

from taskboard.models import Board
import gantt_variants as GV

W, H = 86, 26
TODAY = date(2026, 8, 17)
OUT = ROOT / "prototypes" / "out"
FIXTURE = OUT / "_fixture_late.json"

VARIANTS = [
    ("A · minimal timeline", GV.render_variant_a),
    ("B · card-style", GV.render_variant_b),
    ("C · compact horizon", GV.render_variant_c),
    ("D · swimlane", GV.render_variant_d),
]


def capture_all() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not FIXTURE.exists():
        raise SystemExit(
            f"FIXTURE MISSING: {FIXTURE}\n"
            "Refusing to fall back to the live board: this script writes "
            "committable artifacts.")
    board = Board.load(FIXTURE)
    tasks = board.visible_tasks(False)
    sel = tasks[len(tasks) // 3].id if tasks else None

    combined: list[str] = []
    for label, fn in VARIANTS:
        text = fn(board, sel, TODAY, W, H)

        con = Console(record=True, width=W + 2, force_terminal=True,
                      legacy_windows=False, color_system="truecolor")
        con.print(text)
        slug = label.split(" · ")[0].lower()
        svg_path = OUT / f"gantt-{slug}.svg"
        con.save_svg(str(svg_path), title=f"taskboard gantt — {label}")

        plain = Console(width=W + 2, force_terminal=False, legacy_windows=False)
        with plain.capture() as cap:
            plain.print(text)
        combined.append(f"{'=' * W}\n=== {label.upper()}\n{'=' * W}\n"
                        + cap.get())
        print(f"wrote {svg_path}")

    txt_path = OUT / "gantt-variants.txt"
    txt_path.write_text("\n".join(combined), encoding="utf-8")
    print(f"wrote {txt_path}")
    print(f"viewport {W}x{H} | board: {len(tasks)} tasks | selected: {sel}")


if __name__ == "__main__":
    capture_all()
