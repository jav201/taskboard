"""Baseline probe for the gantt legibility batch (2026-08-06-fastflow-04).

Builds a SYNTHETIC board from `seed_data()` only -- never reads
`~/.taskboard/board.json`. Prints the geometry, the plain-text render, the
title/bar collision measurement, and the occupancy + span-economy numbers.

Run:  python .fast-dev-flow/probes/_probe_gantt.py [width] [height]
"""
import sys, os
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rich.cells import cell_len
from taskboard.models import Board, seed_data
from taskboard import views

TODAY = date(2026, 7, 30)


def synth_board() -> Board:
    """seed_data() only. Never touches ~/.taskboard/board.json."""
    import tempfile, pathlib
    projects, tasks = seed_data()
    path = pathlib.Path(tempfile.gettempdir()) / "_probe_gantt_never_written.json"
    return Board(projects=projects, tasks=tasks, path=path)


def plain(text) -> list[str]:
    return [seg for seg in text.plain.split("\n")]


def render(w: int, h: int):
    b = synth_board()
    return views.render_view("gantt", b, False, None, TODAY, w, h, {}, 0)


def main():
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 104
    h = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    geo = views.gantt_geometry(w, h)
    print(f"=== gantt_geometry({w}, {h}) ===")
    print(f"label_w={geo.label_w} field_w={geo.field_w} figs_w={geo.figs_w} "
          f"field_x={geo.field_x} today_dc={geo.today_dc} today_cell={geo.today_cell}")
    print(f"sum = label_w + field_w + 1 + figs_w = "
          f"{geo.label_w + geo.field_w + 1 + geo.figs_w} (inner={w})")

    txt = render(w, h)
    rows = plain(txt)
    print(f"\n=== render_gantt plain, {len(rows)} rows ===")
    for i, r in enumerate(rows):
        print(f"{i:3d}|{r}|{cell_len(r)}")

    bad = [(i, cell_len(r)) for i, r in enumerate(rows) if cell_len(r) != w]
    print(f"\ncell-width violations (expect 0): {bad}")

    # collision: for each row, the cell just left of the first bar glyph
    BARS = set("█▓▒▌▃▅▆▇━◆▬")
    print("\n=== title/bar adjacency (cell before first bar glyph) ===")
    for i, r in enumerate(rows):
        for j, ch in enumerate(r):
            if ch in BARS:
                prev = r[j - 1] if j else ""
                flag = "COLLISION" if prev not in (" ", "·", "") else "ok"
                print(f"  row {i:3d}: first bar '{ch}' at col {j}, prev={prev!r} -> {flag}")
                break


if __name__ == "__main__":
    main()
