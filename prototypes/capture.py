"""Headless capture of the kanban variants -> .txt (for review) + .svg (honest artifact).

    python prototypes/capture.py

Renders every variant at a realistic viewport against the REAL board data, so
the comparison is made on real density, not on lorem ipsum.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rich.console import Console

from taskboard.models import Board, default_board_path

W, H = 118, 30
OUT = ROOT / "prototypes" / "out"


def capture_all(selected: str | None = None) -> None:
    import kanban_variants as KV

    OUT.mkdir(parents=True, exist_ok=True)
    board = Board.load(default_board_path())
    tasks = board.visible_tasks(False)
    # pick a mid-list task so the "selected" state is visible in every variant
    sel = selected or (tasks[len(tasks) // 3].id if tasks else None)

    combined: list[str] = []
    for label, fn in KV.VARIANTS:
        render = fn or KV._BASELINE
        text = render(board, False, sel, None, W, H, {}, "grouped")

        con = Console(record=True, width=W + 2, force_terminal=True,
                      legacy_windows=False, color_system="truecolor")
        with con.capture():
            con.print(text)
        slug = label.split()[1] if " " in label else label
        con.save_svg(str(OUT / f"kanban-{slug}.svg"),
                     title=f"taskboard kanban — {label}")

        plain = Console(width=W + 2, force_terminal=False, legacy_windows=False)
        with plain.capture() as cap:
            plain.print(text)
        combined.append(f"{'=' * W}\n=== {label.upper()}\n{'=' * W}\n"
                        + cap.get())

    (OUT / "variants.txt").write_text("\n".join(combined), encoding="utf-8")
    print(f"wrote {len(KV.VARIANTS)} svg + variants.txt to {OUT}")
    print(f"viewport {W}x{H} | board: {len(tasks)} tasks | selected: {sel}")


if __name__ == "__main__":
    capture_all()
