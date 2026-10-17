"""The PRES-R2 oracle frames (batch 2026-10-16-batch-01, increment 004) and their cross-check.

Increment 001 wrote PRES-R-*.txt (kept on disk as its evidence); increment 004
writes PRES-R2-*.txt, the frame after the operator's verdict of 2026-10-17.

    python .dev-flow/2026-10-16-batch-01/evidence/gen_frames.py           # cross-check only
    python .dev-flow/2026-10-16-batch-01/evidence/gen_frames.py --write   # (re)write the frames

The frames are the shipped `views.render_present` on the PRES-C oracle board
(`tests/present_board.py`, frozen on its TODAY, cursor `tw3`) at 118x30 and 80x24.
Because they come from the shipped renderer, every row is cross-checked against the
APPROVED prototype's renderer, `render_b2` in `prototypes/present_rulers/app_capture.py`
(variant B + start-end chips, the operator's verdict of 2026-10-16), at both sizes.

Criterion: every row equal, except one declared delta —
  D3 row 2's LABEL column only (the first label_w cells): the shipped tick row reads
     `selected task ▸` (the operator's verdict of 2026-10-17, increment 004) where
     render_b2 wrote `cursor's dates ▸`. The field and chip cells must match.
Increment 004 retired the former deltas D1 (the header's ` — hybrid` suffix) and D2
(the in-frame keys row): the shipped frame no longer carries either, so those rows
now match the prototype byte for byte.
Exit 0 when the criterion holds (and, with --write, the frames are written), else 1.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "prototypes" / "present_rulers"))

import present_board as pb  # noqa: E402
from taskboard import views  # noqa: E402

FRAMES = HERE / "frames"
SIZES = [(118, 30), (80, 24)]


def shipped(board, w: int, h: int) -> list[str]:
    return views.render_present(board, pb.PROJECT_ID, pb.CURSOR, pb.TODAY, w, h).plain.split("\n")


def prototype(board, w: int, h: int) -> list[str]:
    import app_capture  # noqa: E402  (imported late: it patches the app module on import)
    return app_capture.render_b2(board, pb.PROJECT_ID, pb.CURSOR, pb.TODAY, w, h).plain.split("\n")


def crosscheck(ship: list[str], proto: list[str], label_w: int) -> list[str]:
    """The rows that differ beyond D3, as readable lines; empty = criterion holds."""
    bad = []
    if len(ship) != len(proto):
        bad.append(f"row count: shipped {len(ship)}, proto {len(proto)}")
    for i, (a, b) in enumerate(zip(ship, proto)):
        if i == 2:                                                       # D3
            if a[:label_w].strip() != "selected task ▸":
                bad.append(f"row 2 label: {a[:label_w]!r}")
            a, b = a[label_w:], b[label_w:]
        if a != b:
            bad.append(f"row {i}:\n  shipped {a!r}\n  proto   {b!r}")
    return bad


def main(argv: list[str]) -> int:
    board = pb.build(Path(tempfile.mkdtemp()) / "board.json")
    ok = True
    for w, h in SIZES:
        ship, proto = shipped(board, w, h), prototype(board, w, h)
        bad = crosscheck(ship, proto, views._present_cols(w, w >= 100)[0])
        print(f"{w}x{h}: {len(ship)} rows · cross-check vs render_b2: "
              + ("HOLDS (delta D3 only)" if not bad else f"FAILS ({len(bad)})"))
        for line in bad:
            print("  " + line)
        ok = ok and not bad
        if "--write" in argv and not bad:
            FRAMES.mkdir(parents=True, exist_ok=True)
            out = FRAMES / f"PRES-R2-{w}x{h}.txt"
            out.write_text("\n".join(ship) + "\n", encoding="utf-8", newline="\n")
            print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
