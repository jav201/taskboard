"""The PRES-R oracle frames (batch 2026-10-16-batch-01) and their cross-check.

    python .dev-flow/2026-10-16-batch-01/evidence/gen_frames.py           # cross-check only
    python .dev-flow/2026-10-16-batch-01/evidence/gen_frames.py --write   # (re)write the frames

The frames are the shipped `views.render_present` on the PRES-C oracle board
(`tests/present_board.py`, frozen on its TODAY, cursor `tw3`) at 118x30 and 80x24.
Because they come from the shipped renderer, every row is cross-checked against the
APPROVED prototype's renderer, `render_b2` in `prototypes/present_rulers/app_capture.py`
(variant B + start-end chips, the operator's verdict of 2026-10-16), at both sizes.

Criterion: every row equal, except the three declared deltas —
  D1 row 0, the header: the shipped title keeps its ` — hybrid` suffix;
  D2 the shipped in-frame keys row (`←→  move the cursor · ...`), absent in render_b2,
     which shifts nothing above it (it is the last content row);
  D3 row 2's LABEL column only (the first label_w cells): the commission (decision 1)
     labels the tick row with the scale unless the echo did not fit in the field;
     render_b2 wrote `cursor's dates ▸` there. The field and chip cells must match.
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
KEYS_ROW = " ←→  move the cursor · the cursor'd task's notes expand"


def shipped(board, w: int, h: int) -> list[str]:
    return views.render_present(board, pb.PROJECT_ID, pb.CURSOR, pb.TODAY, w, h).plain.split("\n")


def prototype(board, w: int, h: int) -> list[str]:
    import app_capture  # noqa: E402  (imported late: it patches the app module on import)
    return app_capture.render_b2(board, pb.PROJECT_ID, pb.CURSOR, pb.TODAY, w, h).plain.split("\n")


def crosscheck(ship: list[str], proto: list[str], label_w: int) -> list[str]:
    """The rows that differ beyond D1/D2/D3, as readable lines; empty = criterion holds."""
    bad = []
    body = [r for r in ship if r.rstrip() != KEYS_ROW.rstrip()]          # D2
    removed = len(ship) - len(body)
    if removed != 1:
        bad.append(f"D2: expected exactly one in-frame keys row, found {removed}")
    body += [" " * len(ship[0])] * removed                               # the pad it displaced
    for i, (a, b) in enumerate(zip(body, proto)):
        if i == 0:                                                       # D1
            if a.replace(" — hybrid", "", 1).split() != b.split():
                bad.append(f"row 0 differs beyond D1:\n  shipped {a!r}\n  proto   {b!r}")
            continue
        if i == 2:                                                       # D3
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
              + ("HOLDS (deltas D1, D2, D3 only)" if not bad else f"FAILS ({len(bad)})"))
        for line in bad:
            print("  " + line)
        ok = ok and not bad
        if "--write" in argv and not bad:
            FRAMES.mkdir(parents=True, exist_ok=True)
            out = FRAMES / f"PRES-R-{w}x{h}.txt"
            out.write_text("\n".join(ship) + "\n", encoding="utf-8", newline="\n")
            print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
