"""The PRES-V3 oracle frames of batch 2026-10-18-batch-01 (present v3), and their
cross-check against the approved prototype.

    python .dev-flow/2026-10-18-batch-01/evidence/gen_frames.py           # check
    python .dev-flow/2026-10-18-batch-01/evidence/gen_frames.py --write   # write

The frames are the shipped renderer's rows (`views.render_present(...).plain`)
on two synthetic boards: the PRES-C oracle board (`tests/present_board.py`, the
gantt frames TC-1001 / TC-1002 / AT-1001 read) and the same board with the
prototype round's notes (`tests/present_notes_board.py`). Each frame is then
compared, row for row, with what the approved prototype's own renderer
(`prototypes/present_views/views_d.py`: `render_gantt`, `render_stacked` = D2)
paints for the same board, cursor and size — the prototype is the source of
truth for the look (the operator's verdicts of 2026-10-17/18). Declared deltas
are listed in DELTAS; any other difference is a failure (exit 1).

New files only: the PRES-R / PRES-R2 frames of batch 2026-10-16-batch-01 are
never rewritten (their hashes are recorded by that batch's packets).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FRAMES = HERE / "frames"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "prototypes" / "present_views"))

import present_board as pb  # noqa: E402
import present_notes_board as nb  # noqa: E402
from taskboard import views  # noqa: E402

# The prototype imports two helpers the shipped renderer no longer has (this
# batch replaced them with `present_note_lines` / `_present_cut`); its views_d
# renderers never call them. Bind inert names so the import resolves.
views._present_note_lines = lambda *a, **k: []
views._present_note_row = lambda *a, **k: ""
import views_d as VD  # noqa: E402

# name: (board builder, cursor, view, width, height)
CASES = {
    "PRES-V3-gantt-118x30": (pb.build, pb.CURSOR, "gantt", 118, 30),
    "PRES-V3-gantt-80x24": (pb.build, pb.CURSOR, "gantt", 80, 24),
    "PRES-V3-gantt-notes-118x30": (nb.build, nb.LONG, "gantt", 118, 30),
    "PRES-V3-gantt-notes-80x24": (nb.build, nb.LONG, "gantt", 80, 24),
    "PRES-V3-split-118x30": (nb.build, nb.CURSOR, "split", 118, 30),
    "PRES-V3-split-80x24": (nb.build, nb.CURSOR, "split", 80, 24),
    "PRES-V3-split-long-118x30": (nb.build, nb.LONG, "split", 118, 30),
    "PRES-V3-split-long-80x24": (nb.build, nb.LONG, "split", 80, 24),
}
PROTO = {"gantt": VD.render_gantt, "split": VD.render_stacked}

# Declared deltas from the prototype, at scroll 0 (none at the oracle sizes):
# D1 `1. ` item detection also takes `10. `..`999. ` (the prototype: one digit);
#    no fixture note has a 2-digit item, so no frame differs.
# D2 a note kept to one row says ` … +N lines` (the prototype: ` … +N`), and its
#    first line is cut without a second `…` — the brief's "a cut note shows
#    `… +N lines`" and ux-reviewer UX-4 (P2): row 11 of the two 80x24 split frames
#    (`Design tokens are frozen at v2.3. … +4 lines`).
# The scroll deltas (paging, the whole-area scroll) do not reach a scroll-0 frame.
DELTAS: dict[str, set[int]] = {"PRES-V3-split-80x24": {11}, "PRES-V3-split-long-80x24": {11}}


def rows(name: str) -> list[str]:
    build, cur, view, w, h = CASES[name]
    b = build(Path("PRESENT-oracle-never-saved.json"))
    return views.render_present(b, pb.PROJECT_ID, cur, pb.TODAY, w, h, view).plain.split("\n")


def proto_rows(name: str) -> list[str]:
    build, cur, view, w, h = CASES[name]
    b = build(Path("PRESENT-oracle-never-saved.json"))
    return PROTO[view](b, pb.PROJECT_ID, cur, pb.TODAY, w, h).plain.split("\n")


def main(argv: list[str]) -> int:
    write = "--write" in argv
    FRAMES.mkdir(parents=True, exist_ok=True)
    bad = 0
    for name in CASES:
        got, ref = rows(name), proto_rows(name)
        diff = [i for i, (a, r) in enumerate(zip(got, ref)) if a != r]
        if len(got) != len(ref):
            diff.append(-1)
        undeclared = [i for i in diff if i not in DELTAS.get(name, set())]
        path = FRAMES / f"{name}.txt"
        if write:
            if path.exists():
                print(f"{name}: exists, not rewritten")
            else:
                path.write_bytes(("\n".join(got) + "\n").encode("utf-8"))
                print(f"{name}: written")
        on_disk = path.read_text(encoding="utf-8").splitlines() if path.exists() else None
        same = on_disk == got
        bad += (not same) + bool(undeclared)
        print(f"{name}: {len(got)} rows · on disk {'==' if same else '!='} renderer · "
              f"prototype deltas {diff or 'none'}"
              + (f" UNDECLARED {undeclared}" if undeclared else ""))
    print("FAILED" if bad else "OK", f"({len(CASES)} frames)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
