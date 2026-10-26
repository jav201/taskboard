# Real-app captures — batch 2026-10-26-batch-01 (the `fix/gantt-done-visible` change, f4b53cc)

The SHIPPED `TaskboardApp` at `f4b53cc` (done, non-archived tasks keep their
rows on the board's gantt: quiet dimmed title, reached-tone bar, `✓` chip, never
late; only archived work disappears), unpatched, in real Windows Terminal windows
(truecolor, `NO_COLOR` cleared), by `shoot_ga.ps1` / `shoot_ga.py` — the method of
batch 2026-10-21-batch-01's harness, adapted. Every window had a unique `ga-*`
title, was closed right after its shot (WM_CLOSE by title, Windows Terminal
windows only — no process ever killed, no other window touched) and verified
gone; each run ended with `no ga-* window left open` (`png/capture-log.txt`), and
the run's end-state line `OK Screen view=gantt` (written by the app itself)
asserts the capture ended on the gantt view. Every shot passed the colour check
(>= 8 sampled colours, none black) on its first try; distinct colours counted
from the saved PNGs are listed per capture below. The calendar is pinned to
TODAY = 2026-10-26 inside the scene process; nothing touched the real home
(every scene runs against a `TEMP\ga-cap-*` folder, removed after its shot).

| PNG | Window | Fixture | What it proves |
|---|---|---|---|
| `png/gantt_118x30.png` | 118x30, `ga-gantt-118x30-53691` | ga-mix (built by `shoot_ga.py`): Website Redesign (2 open, 2 done, 1 done+archived), Mobile App (1 open, 1 done), Ops & Security (3 done, no open), 1 loose Inbox task | **G1+G2**: done rows stay on the board, quiet — dimmed titles, `◂` reached-tone bars, right-hand `✓` chip, no `▲Nd` late colouring, no flow packet; Ops & Security (zero open work) still shows all 3 done rows; the archived "Old promo landing page" appears NOWHERE while spans still count the visible done work (`✓2` / `✓1` / `✓3`). Distinct colours: 458. |
| `png/gantt_80x24.png` | 80x24, `ga-gantt-80x24-51232` | ga-mix, same board | Same content fits the small window: done rows still visible and quiet at 80 cols (titles ellipsize, as every row's does). Distinct colours: 433. |
| `png/busy_80x24.png` | 80x24, `ga-busy-80x24-16529` | ga-busy: 8 projects × (2 open + 3 done), all done recent (1–5d ago) | **G3, flag ON (shipped)**: done rows consume fold room — only 2 of 8 groups unfold (Website Redesign, API Platform, 5 rows each incl. 3 done rows at the tail); the other 6 stay folded to their span row. Matches the read-only render oracle in `busy_flagoff_80x24.txt` (done_rows=True half). Distinct colours: 374. |
| `png/busyoff_80x24.png` | 80x24, `ga-busyoff-80x24-94633` | ga-busy with every DONE task archived (open work untouched) — the flag-off seat | **G3, comparison**: with done work gone, 6 of 8 groups unfold (2 open rows each) and only 2 stay folded — the fold the pre-change rule (G-A) would give. Matches the oracle's `done_rows=False` half prediction (6 unfolded / 2 folded). Distinct colours: 359. |

Notes and limits:

- `busy_flagoff_80x24.txt` is a capture-adjacent note, not a capture: the exact
  same ga-busy board rendered read-only through the shipped `_gantt_frame` at
  80x24 twice (`done_rows=True` = shipped board gantt; `done_rows=False` = the
  flag-off seat = pre-change folding). It is the oracle the two busy PNGs match.
- The `busyoff` PNG approximates the old fold with archived done tasks instead of
  unwritten code: identical row geometry (archived work draws no rows and is not
  counted in `✓n`), differing only in the span's `✓n` chip, which the old rule
  showed and this seat cannot. Fold counts are unaffected by that difference.
- A first-run "View keys renumbered" notice overlays the bottom-right corner in
  every capture (each scene gets a fresh temp home). It covers part of the gantt
  field but never the group labels, fold arrows, done-row `✓` chips or the
  unfolded/folded structure the captures are evidence for.
- The presentation (G4, byte-identity) and the keyboard walk to a done row
  (`↓` reaches it) are not UX-capture claims here — they belong to the QA lens's
  seat; these captures are the painted surface for G1–G3 only.
- Window-cleanup assertion: PASS — `no ga-* window left open` at the end of each
  of the three runs (`png/capture-log.txt`), re-verified after the last run.
