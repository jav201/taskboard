# Requirements ledger — taskboard — Batch 2026-10-17-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-17-batch-01.1 — the tick row's label, one rule, no scale text (P1)
- **Requirement:** HLR-1701, LLR-1701.1
- **Date:** 2026-10-17
- **What changed:** new requirements: the gantt view labels its tick row by the rule the presentation ships (`selected task ▸` / the echo's own text / `selected: no dates` / blank), through one function both views call; the presentation's no-cursor fallback becomes blank; `_gantt_scale_label` is deleted. They supersede the scale-label clauses of HLR-105 ("its label column naming the cadence and the scale") and LLR-101.10 ("the day row's scale label shall fit its column whole") of batch 2026-10-02-batch-01, and LLR-1601.1's clause "with the scale label in dim only when there is no cursor task" of batch 2026-10-16-batch-01. Their pinned tests change law-driven: AT-104 (`tests/test_gantt_board.py`, the label assertion), TC-110 (deleted with the function), TC-1601 (`tests/test_present_rulers.py`, the no-echo label), TC-1608 (c) (`tests/test_present_room.py`, the no-selection arm).
- **Why:** the operator, 2026-10-17: «Es la etiqueta de Mondays y cells? Si es así, hay que quitarla. No agrega valor»; the coordinator's decisions (PLAN §Key decisions): one rule in both views avoids two dialects.
- **Evidence:** `taskboard/views.py:2849-2853` (the scale text), `:3001-3006`, `:6224-6231` (the two sites); P-1..P-4 (`01-requirements.md` §2.7).

### LED-2026-10-17-batch-01.2 — P2 iteration 1 amendments (P1, iterate-to-refine)
- **Requirement:** HLR-1701, LLR-1701.1
- **Date:** 2026-10-17
- **What changed:** HLR-1701: the statement names link mode (the candidate is the selection), a selection a search hides (no selection to the frame; the app re-selects a drawn task or none) and a selection outside the window (UX-1, UX-2, UX-3); AT-1701's five arms are named with their key paths and board files, the "none" state reached through a board with no task and a search that draws none (QA-1); the negative control re-cited to the base code path, its RED to be captured at increment 001 (QA-4); the boundary catalog gains the hide-all route and the new boundaries (A-6). LLR-1701.1: every TC-1701 case written out with its fixture (`tw1` Jul 1 → Dec 31 for the gantt "does not fit" arm — QA-3; off-window `tw1`; the search-hidden `tw3`; link mode with and without a candidate — A-4, QA-6; hide-all — A-6; the 48-column texts pinned, `selected: no d…` accepted — UX-4); the scale-text pattern stated case-sensitive, its five positive-control strings written from the rule, plain and inside an exported SVG, with a false-match guard (QA-2, QA-5, QA-7); tone mutations in the negative control (QA-4). §1.2: the README hero image is Out, with its reason (A-3). §2.3: the user's task (UX-5). §2.7: premises P-5..P-8. §5.2: two more capture steps (UX-6). §6.3: the supersession reaches LLR-102.2 and LLR-1602.2 as well (A-1) — five canon rows in all.
- **Why:** the P2 review of 2026-10-17, iteration 1 (architect, qa-reviewer, ux-reviewer — all `iterate-to-refine`).
- **Evidence:** `02-review.md` §Findings; probes for P-5..P-8 on the patched scratch worktree (`01-requirements.md` §2.7); `REQUIREMENTS.md:47` (LLR-102.2), `:204` (LLR-1602.2); `docs/taskboard-gantt.svg:157`; the SVG escape measured on the base tree (54 × `&#160;`, 0 × `&amp;#160;`).

### LED-2026-10-17-batch-01.3 — P2 iteration 2 minor amendments (P2 gate)
- **Requirement:** HLR-1701, LLR-1701.1
- **Date:** 2026-10-17
- **What changed:** §2.7: the premise table rejoined (a blank line had cut P-5..P-8 off it — A2-1); P-7's evidence re-measured at both widths: the off-window echo paints `Aug 23–Sep 10` whole (UX2-1, which read a truncated probe print). §1.3: the gantt view's label column below 60 columns (A2-2). HLR-1701 arm (3): its two queries named (`Daily`, `zzqx`) and the re-select half driven — a search that keeps one open task leaves the label naming the app's new selection (QA2-2, the ux notice). LLR-1701.1: the off-window arm pins `Aug 23–Sep 10`; the sweep proves each frame painted before counting matches (QA2-5). QA2-3 and QA2-4 were run, not amended: AT-1701 arms (2) and (4) pass on the patched scratch tree. QA2-1 (the dead-cell law `tests/test_gantt.py:287`, missed by the census and found by the pre-executed full suite) is an implementation finding owned by increment 001: rebaselined there to `<= 25.5` = 25 + 100 · 15 / 2880 (the cells `Mondays · 1 d/cell` inked at 96×30), law-driven per the qa-reviewer and the architect.
- **Why:** the P2 review of 2026-10-17, iteration 2 (architect `approve`, qa-reviewer `approve`, ux-reviewer `approve`); every item a minor wording, evidence or arm fix changing no obligation.
- **Evidence:** `02-review.md` §Iteration 2; the patched scratch tree's runs of `tests/test_tick_label.py` (30 passed).
