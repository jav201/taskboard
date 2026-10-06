"""P1 thresholds (C-39) for batch 2026-10-04-batch-02, executed with the PROTOTYPE's own rule
functions (`variants_round5`: `candidates`, `_ms_bits`, `ms_chip`, `ms_tone`) over its round-5
boards, inside the prototype worktree (its own `taskboard`). Run:
    cd .claude/worktrees/kg-mejoras/prototypes/kg_mejoras
    python -B <this file> > <evidence>/p1-thresholds.txt
The contract's oracle rows are these lines; the ATs shift the board to today, and every
figure below is relative to TODAY, so it survives the shift."""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(os.getcwd())
sys.path.insert(0, str(HERE))

import fixture  # noqa: E402
import variants_round5 as V  # noqa: E402
from taskboard.models import parse_iso  # noqa: E402
from rich.text import Text  # noqa: E402

TODAY = fixture.TODAY
board = fixture.build()
print("TODAY", TODAY, "· tasks", len(board.tasks), "· phases", board.phases)

print("\n## M-3 candidates over one_day_board (the offer's two groups, in the frame's order)")
od = V.one_day_board(board, TODAY)
for t, why, on in V.candidates(od, TODAY):
    pr = od.project_by_id(t.project_id)
    waiting = sum(1 for x in od.visible_tasks(False) if t.id in x.depends_on)
    print(f"{'▣' if on else '□'} {t.id:4} {t.title:28} {pr.name if pr else 'Inbox':18} "
          f"{V.md(parse_iso(t.due_date))} · {why}" + (f" · {waiting} waits on it" if waiting else ""))
print("one-day:", sum(1 for _, _, on in V.candidates(od, TODAY) if on),
      "due-only:", sum(1 for _, _, on in V.candidates(od, TODAY) if not on))

print("\n## M-1 milestone chips and tones over milestone_board")
mb = V.milestone_board(board, TODAY)
for t in mb.tasks:
    if V.is_ms(t):
        pr = mb.project_by_id(t.project_id)
        chip = Text.from_markup(V.ms_chip(t, mb, TODAY, 8)).plain
        print(f"{t.id:4} {t.title:28} due {t.due_date} phase {t.phase:8} "
              f"tone {V.ms_tone(t, mb, TODAY, pr):7} chip {chip!r}")

print("\n## M-2 band-rule order per project (_ms_bits: late, upcoming by date, last reached)")
for pr in mb.visible_projects(False):
    bits = V._ms_bits(mb, pr, TODAY)
    print(f"{pr.name:18}", " | ".join(f"{t.title} [{tone}] {rel}" for _, t, tone, rel in bits) or "—")

print("\n## M-2 band segments at the frame's room (118 wide)")
for pr in mb.visible_projects(False):
    items = V._ms_bits(mb, pr, TODAY)
    for room in (70, 40, 20):
        segs, n = V._ms_segment(items, room)
        print(f"{pr.name:18} room {room:3}: {''.join(t for t, _ in segs)!r} ({n})")
