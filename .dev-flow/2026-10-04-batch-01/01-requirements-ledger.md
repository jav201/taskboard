# Requirements ledger — taskboard — Batch 2026-10-04-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-04-batch-01.1 — a link means "waits on"; cards show both directions
- **Requirement:** HLR-501
- **Date:** 2026-10-04
- **What changed:** new requirement: waiting is derived from live links, independent of the external block; cards paint `◂N`/`▸N` in place of `⛓N`; `b` keeps only the external block; the ready toast fires once on the transition.
- **Why:** the operator could not tell whether dependencies existed (`NOTES.md` round 2); `DEPS-CONTRACT.md` rules 1–4 and the round-3 verdict; P-1, P-2 measured the shipped behaviour.
- **Evidence:** `evidence/p1-premises.txt` §P-1, §P-2; `evidence/p1-deps-logic-rerun.txt`.

### LED-2026-10-04-batch-01.2 — `L` in the picker and on the gantt; loops refused
- **Requirement:** HLR-502
- **Date:** 2026-10-04
- **What changed:** new requirement: `L` links through the picker (D-B2) outside the gantt and the live link mode (D-A) in it; a loop is refused with its path; add and remove are one undo step each.
- **Why:** contract rules 5–8; round-3 verdict "`L` in both the picker and the gantt link mode".
- **Evidence:** `out/D-B2-118x30.txt`, `out/D-A-118x30.txt` (worktree `kg-mejoras`); `evidence/p1-thresholds.txt`.

### LED-2026-10-04-batch-01.3 — the details dependency section
- **Requirement:** HLR-503
- **Date:** 2026-10-04
- **What changed:** new requirement: the details view lists waits-on and unblocks (direct and chain) with conflicts, and removes, adds and jumps.
- **Why:** D-B, round-3 verdict; P-5 measured that the details show nothing.
- **Evidence:** `out/D-B-118x30.txt`; `evidence/p1-premises.txt` §P-5.

### LED-2026-10-04-batch-01.4 — the archive/delete guard
- **Requirement:** HLR-504
- **Date:** 2026-10-04
- **What changed:** new requirement: archiving or deleting an open task that open tasks wait on is refused with the waiters named; a done predecessor archives normally.
- **Why:** the operator's round-3 ruling (delete by the orchestrator's reading, `DEPS-CONTRACT.md` Rulings); P-3 measured that both succeed today.
- **Evidence:** `evidence/p1-premises.txt` §P-3.

### LED-2026-10-04-batch-01.5 — the one-time link migration
- **Requirement:** HLR-505
- **Date:** 2026-10-04
- **What changed:** new requirement: the legacy links are migrated once at start by `deps_logic.migrate`'s rule, with a backup before, a log, a mark in the board settings, and `u` to revert.
- **Why:** the new meaning would re-block work the operator had unblocked (A1); the operator's safeguard at kickoff, "Respaldo automático + deshacer".
- **Evidence:** `evidence/p1-deps-logic-rerun.txt` (L1..L6 on the stated rule).

### LED-2026-10-04-batch-01.6 — P2 iteration 1 fold: the waits-on model
- **Requirement:** HLR-501, LLR-501.1, LLR-501.2, LLR-501.3, LLR-501.4
- **Date:** 2026-10-04
- **What changed:** board tasks only (teammates excluded); bounded cost (one id map, iterative searches, hostile-board TC-518); derivations defined on a stored cycle; the full shed order; callers derived; the AT reads every band and the lanes presentation from painted segments; `_flowing` stops for a waiting task and every other `blocked` reader keeps the flag (D-519); ready toasts capped at 3; silent releases named (D-524).
- **Why:** `02-review.md` iteration 1 — A-3, A-6, A-11, A-13, S-5, S-8, Q-4, Q-5, Q-17, UX-16, UX-17, UX-20, Q-16.
- **Evidence:** `02-review.md`; `evidence/p1-tables.txt`.

### LED-2026-10-04-batch-01.7 — P2 iteration 1 fold: `L`, the picker, link mode, README
- **Requirement:** HLR-502, LLR-502.1, LLR-502.2, LLR-502.3, LLR-502.4
- **Date:** 2026-10-04
- **What changed:** `L` in the primary layer of group `task`, scoped to the views with a selection; toasts end "· u undo"; loop paths shortened; the picker's six timing forms and loop form tabled (TC-509, three waiters), start highlight, create branches; link mode: filter echo, backspace, no-match, `⟲` rows and loop legend, linked-candidate unlink, start candidate, status rows as Text pieces with one EXEMPT repaint, 80-column rule; NEW LLR-502.4 (README).
- **Why:** `02-review.md` iteration 1 — Q-7, Q-8, Q-11, Q-14, S-9, S-10, UX-3..UX-7, UX-10..UX-13, UX-19, UX-21.
- **Evidence:** `evidence/p1-tables.txt`; `02-review.md`.

### LED-2026-10-04-batch-01.8 — P2 iteration 1 fold: the details section
- **Requirement:** HLR-503, LLR-503.1
- **Date:** 2026-10-04
- **What changed:** "K in chain" counts direct and chain; the no-start conflict form; focus stays on the box, `tab` reaches the list, keys in the title row; `x` on either direction; the jump clears focus and search and names an archived target.
- **Why:** `02-review.md` iteration 1 — Q-13, A-10, UX-1, UX-2, UX-8, UX-18.
- **Evidence:** `evidence/p1-tables.txt` (TC-513).

### LED-2026-10-04-batch-01.9 — P2 iteration 1 fold: the guard on every path
- **Requirement:** HLR-504, LLR-504.1
- **Date:** 2026-10-04
- **What changed:** the project archive guarded (outside waiters, D-523); `d` checked again in `_on_delete`; the editor judged after its phase; refusal text capped at 3 names with real plurals; TC-517 (was a second TC-507).
- **Why:** `02-review.md` iteration 1 — A-1 (blocker), A-12, S-7, S-10, Q-10, UX-14, UX-15.
- **Evidence:** `02-review.md`.

### LED-2026-10-04-batch-01.10 — P2 iteration 1 fold: the migration's safety
- **Requirement:** HLR-505, LLR-505.1, LLR-505.2, LLR-505.3
- **Date:** 2026-10-04
- **What changed:** the migration is `on_mount`'s first write; two rulings for ambiguous legacy shapes (D-515 last link done → flag kept; D-516 a loop-closing blocker dropped, flag kept); backup and log by exclusive create with numbered names outside team pull's pattern (D-520, D-521); an atomic save; a total read of the mark; unreadable boards skipped; fail closed (D-518); `u` keeps the mark (D-517); the toast short with a 30 s timeout and no path; three ATs (AT-506..508); the fixture seam that marks the kg board.
- **Why:** `02-review.md` iteration 1 — Q-1 (blocker), Q-2, Q-9, Q-15, A-2, A-4, A-5, A-7, A-8, A-9, A-14, S-1..S-4, S-11..S-13, UX-9.
- **Evidence:** P-17, P-18 (qa probes); `02-review.md`.

### LED-2026-10-04-batch-01.11 — P2 iteration 2 minors folded at the gate
- **Requirement:** HLR-501, LLR-503.1, LLR-505.1, LLR-505.2, LLR-505.3
- **Date:** 2026-10-04
- **What changed:** the AT height measured (118×40); every kept migration link loop-checked; "last stored id"; the press-`b` log note; the resolved board path and the named temporary file; a replaced malformed mark forces backup and log; the exit message names the way out; real plurals; the details keys on their own row; `tab` leaves the layout unchanged; AT-507/508 wording.
- **Why:** `02-review.md` iteration 2 — A2-1..A2-5, S2-1..S2-3, UX-14, UX-22, UX2-1..UX2-3, Q2-1..Q2-5.
- **Evidence:** `evidence/p2-kanban-height.txt`.

### LED-2026-10-04-batch-01.12 — increment 001 code review folded (amendment A-1)
- **Requirement:** LLR-505.2, LLR-505.3
- **Date:** 2026-10-04
- **What changed:** the exit message reads "The board file was not changed" (the shipped law forbids second-person literals in the app); the save's temporary file is created exclusively, never written through or removed when it was not this run's; a failed run removes the backup and log it created; a repeated task id is left untouched; the loop check walks back once per task.
- **Why:** increment 001 code review F1, F2, F4, F5, F7; `tests/test_prism_laws.py` second-person law.
- **Evidence:** `03-increments/increment-001.md`; `evidence/inc001-mutations-r2.txt`.

### LED-2026-10-04-batch-01.13 — increment 001 security check folded (amendment A-2)
- **Requirement:** LLR-505.2, LLR-501.1
- **Date:** 2026-10-04
- **What changed:** the save's temporary file has a random exclusive name (`.<board file name>.<random>.tmp`) so a crash leftover never blocks a start; a malformed `migrations` dict keeps its other keys; only a link to an already-processed task triggers the loop walk; a dense rotating closed board is bounded at 2 s (D-526).
- **Why:** security check of increment 001 — S3-1 (MEDIUM), S3-2, S3-3 (LOW); code review round 2 R2-F1 (the hub board's order).
- **Evidence:** `evidence/inc001-r2f1-red.txt`; `03-increments/increment-001.md`.

### LED-2026-10-04-batch-01.14 — the marks shed before the project tag (amendment A-3)
- **Requirement:** HLR-501, LLR-501.2
- **Date:** 2026-10-04
- **What changed:** the meta shed order is `↗`, `▤`, age, `▸`, `◂`, project tag, due (was: tag before the marks); HLR-501's threshold states the measured painted counts (grouped `◂` 7 of 8 — the high-band card `Deprecate v1 endpoints` keeps its project tag; lanes 8 of 8; `▸` 8 of 8).
- **Why:** with the P1 order a waiting card in the board-wide high band lost its project tag — an accepted visual of batch 2026-10-02-batch-03 (R-1b) — to `◂1` (`test_kanban_readable.py` TC-308 RED); the conservative reading keeps the accepted mark (PV-1).
- **Evidence:** `03-increments/increment-002.md`.

### LED-2026-10-04-batch-01.15 — `x` in Setup never touches a task (amendment A-4)
- **Requirement:** LLR-504.1
- **Date:** 2026-10-04
- **What changed:** `action_archive` handles the Setup branch first: in Setup `x` removes a setup row only — no task snapshot, no archive, no save of a task; security S-7 (pre-existing) is closed in this batch instead of being routed to the backlog.
- **Why:** increment 002 code review F2 (HIGH, product: the guard's Setup exclusion left the hidden board selection archivable past the guard); asked at the gate, operator 2026-10-04: "Corregir en el 002".
- **Evidence:** `evidence/inc002-f2-red.txt`.

### LED-2026-10-04-batch-01.16 — the details keys on the section heading; IFC Part B (amendment A-5)
- **Requirement:** LLR-503.1, LLR-502.2
- **Date:** 2026-10-04
- **What changed:** the details view's link keys sit on the dependency section's heading row; the title row ("‹title› — o open raw · esc close") stays as the operator accepted it in batch 2026-10-02-batch-04 (UX-3/UX-4); the IFC Part B blocks `link-picker` and `details-links` are written now that the widgets exist (D-514).
- **Why:** a new row under the title would move the details layout the operator accepted (the most conservative reversible reading, PV-4); `V14` resolves consumers only once the files exist.
- **Evidence:** `03-increments/increment-003.md`.

### LED-2026-10-04-batch-01.17 — the details rows carry each predecessor's own state (amendment A-6)
- **Requirement:** LLR-503.1
- **Date:** 2026-10-04
- **What changed:** each `Waits on` row shows the predecessor's own state (open / done / archived), the "◂N open of M" count counts those states, and a closed task's heading carries neither "waiting" nor "ready".
- **Why:** increment 003 code review F1 (HIGH, product: a closed task's open predecessors were painted `done`); asked at the gate, operator 2026-10-04: "Corregir en el 003".
- **Evidence:** `evidence/inc003-f1-red.txt`.

### LED-2026-10-04-batch-01.18 — the link mode's keys on a row of their own (amendment A-7)
- **Requirement:** LLR-502.3
- **Date:** 2026-10-04
- **What changed:** the link mode's status is three rows — what is linked (titles clip), the candidate's timing, the keys — and the loop legend follows the keys in the picker's form "this → ‹path› → this", clipped to the room left. The candidate count and the cycle are the open tasks the gantt draws (a task in a hidden archived project stays reachable from the picker, D-527); the first row clips titles and the filter by cells and never wraps (code review F1).
- **Why:** with the keys on the title row, 80 columns left four cells for both titles (probe during increment 004); the keys are never clipped and the titles get the row (PV-5).
- **Evidence:** `03-increments/increment-004.md`.

### LED-2026-10-04-batch-01.19 — the link mode says a folded waiter row (amendment A-8)
- **Requirement:** LLR-502.3
- **Date:** 2026-10-04
- **What changed:** when the gantt cannot unfold the waiter's group beside the candidate's, the hint row adds "‹waiter› is folded — a taller terminal draws the link" (the title clips first; "waiter row folded" where the row is short); a closed waiter, never drawn, gets no note (code review 005 N1, N2).
- **Why:** ux-reviewer P4 F4 (MED): the overlay vanished in silence at 118×20, and at 118×30 on boards with larger projects; the shared fold rule stays as shipped (D-528).
- **Evidence:** `03-increments/increment-005.md`.

### LED-2026-10-04-batch-01.20 — link mode pins the waiter's group (amendment A-9)
- **Requirement:** LLR-502.3
- **Date:** 2026-10-04
- **What changed:** `gantt_plan` takes an optional pinned group, unfolded like the selection; link mode pins the waiter's group and the frame pages it to the waiter; when the selected and pinned groups cannot both be drawn whole they share the rows left (the pinned group half). The A-8 note remains only where even that leaves no row for the waiter. Outside link mode nothing is pinned and the fold rule is the shipped one.
- **Why:** the operator's visual verdict, D-528 "Corregirlo antes del push".
- **Evidence:** `03-increments/increment-006.md`.

### LED-2026-10-04-batch-01.21 — the lanes' title floor (amendment A-10)
- **Requirement:** LLR-501.2
- **Date:** 2026-10-04
- **What changed:** in lanes a card's title keeps 6 cells (or its whole length) before any indicator: `▸` then `◂` are shed first, then the other meta from the left. Other `card_cell` callers keep the shipped law.
- **Why:** the operator's visual verdict, D-529 "Corregirlo antes del push" (ux U-2: two lanes cards painted no title).
- **Evidence:** `03-increments/increment-006.md`.

### LED-2026-10-04-batch-01.22 — a read-only board leaves nothing beside it (amendment A-11)
- **Requirement:** LLR-505.2
- **Date:** 2026-10-04
- **What changed:** `save_atomic` refuses a read-only board before creating its temp file (the error names the board); on any failure the temp file is removed, a copied read-only bit cleared first, and a cleanup error never masks the save's own.
- **Why:** the operator's visual verdict, D-530 "Corregirlo antes del push" (security close F1).
- **Evidence:** `03-increments/increment-006.md`.

### LED-2026-10-04-batch-01.23 — the lanes keep `◂` (amendment A-12)
- **Requirement:** LLR-501.2
- **Date:** 2026-10-04
- **What changed:** under the lanes' title floor the shed order is the age `·Nd` first, then `▸`, then the other meta from the left, and `◂` (waits on N open) last; every other view and `card_cell` caller unchanged (byte-identical, `evidence/inc007-identity.txt`).
- **Why:** asked at the gate — D-533, operator 2026-10-04: "Dejar ◂ solo, quitar la edad antes".
- **Evidence:** `03-increments/increment-007.md`.
