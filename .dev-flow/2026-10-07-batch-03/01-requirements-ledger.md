# Requirements ledger — taskboard — Batch 2026-10-07-batch-03

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-07-batch-03.1 — the cleanup batch derived (P1)
- **Requirement:** HLR-901, HLR-902, HLR-903, LLR-901.1, LLR-902.1, LLR-903.1
- **Date:** 2026-10-07
- **What changed:** new requirements for the six BACKLOG items — S-4 (restore-first/best-effort cleanup, increment 001), S-9 (non-text title coercion, increment 001), K2-1 + D-623 + UX2-2 + milestones-in-views (increment 002). AT-901/902/903, TC-901/902.
- **Why:** the operator's 'HAz ambas, paraleliza' — this batch is the loose-items half; the items were filed by the security reviews (S-4, S-9) and the batch reviews (K2-1, D-623); batch E's prototype round runs in the present-e worktree in parallel.
- **Evidence:** `.dev-flow/BACKLOG.md` · the S-4/S-9 findings in batch 2026-10-04-batch-01's review record.

### LED-2026-10-07-batch-03.2 — P2 findings folded (P1, iteration 2)
- **Requirement:** HLR-901, HLR-902, HLR-903, LLR-901.1, LLR-902.1, LLR-903.1
- **Date:** 2026-10-07
- **What changed:** CL-1 — S-4's failure surfaces via `result.error` (the offer's error-as-data convention; nothing raises past the function), the contract's "re-raises" refuted by its own reference AND the already-implemented increment (the order — restore board, restore mark, nested best-effort cleanup — was already right); CL-2/CL-4 — AT-901/902/903 DEFINED (were pointers to nothing): AT-903's four arms, each reading the painted frame (C-32), with the shared drawn-band computation (CL-7), the D-623 head's `N open` text, the UX2-2 marker `▾ N more · ▲1 ◆` with "late" = due before today (per `milestone_tone`), the marker-only scope for the three views (CL-9), and the swimlanes legend collision arm (CL-5); CL-3 — S-9's containers read `Untitled` (the safer rule the lenses preferred; a repr is not a title and can blow cell widths), TC-902's exact expected strings for all five shapes (5/`["x"]`/`{"a": 1}`/null/true); the stale team_sync test's expectation folded (the foreign task with a coerced title is now kept, `["Good", "123"]`). NOTE: increment 001 was implemented DURING P2 (the agent ran in parallel), so S-4/S-9 land as implemented-and-reviewed rather than contract-then-code; the reconciliation is this entry.
- **Why:** P2 — qa FAIL, ux FAIL, architect/security PASS-WITH-NOTES; the convergent blockers were contract-wording (the re-raise), the circular AT-903, and the undiscriminating container arm.
- **Evidence:** the lenses' CL-1..CL-9 · `taskboard/models.py:1619-1633,782-791` (the increment) · `tests/test_team_sync.py` (the folded expectation).

### LED-2026-10-07-batch-03.3 — the fold-canon ruling (P3→P5, the increment-002 reconciliation)
- **Requirement:** HLR-903, LLR-903.1
- **Date:** 2026-10-07
- **What changed:** the canonical fold literal is pinned: the fold row reads `▼ N below` (LLR-309.1's shipped shape, `taskboard/views.py:5161`) with the late-milestone suffix ` · ▲N ◆` appended BEFORE the final fit (`views.py:5179-5181`, the late count at `:5122-5127`) — HLR-903's arm-3 threshold was amended from the BACKLOG's `▾ N more · ▲1 ◆`, the pre-shipped note that predated the `▼ N below` law ("the BACKLOG's `▾ N more` note predated it and loses", the `_fold_row` docstring). The literal is pinned by 7 of the 9 TC-311 census nodes (`tests/test_kanban_readable.py:66` FOLD regex; `:480`, `:574`, `:607` ×4 params, `:1221`) and AT-903 arm 3's `▼.*▲1 ◆` (`tests/test_cleanup.py:339`); the surviving `▾` seats in views.py are the gantt/group unfold heads (:2847, :2863, :6463, :6548) — a different seat, census-clean. THE MEASURED ORIGIN: increment 002's agent renamed the down seat `▼ N below` → `▾ N more`; the full suite reddened exactly those 7 census nodes (`2514 passed, 27 failed`, of which 20 the declared environmental subprocess crashes); the coordinator reverted the rename and re-fitted the suffix onto the canonical literal; the kill is re-executed at close-out as mutant M1 (`7 failed, 2 passed` on the census + AT-903[3_fold] RED, restore by sha256 `e2dec784…a66f`) and the suffix separately as M2.
- **Why:** the rename showed a cleanup batch can break a pinned shipped law while "improving" it toward the backlog's older wording — the contract now carries the canonical literal, the census is its executable pin, and the BACKLOG's UX2-2 line is marked done with the shipped shape named.
- **Evidence:** `evidence/inc002-run.log` (the reddening + the environmental-20 declaration) · `evidence/inc002-mutations.log` (M1/M2, transcripts + restores) · `taskboard/views.py:5151-5181` · the emitted fold row `'▼ 2 below: Data Warehouse (4 open), Ops & Security (5 open) · ▲1 ◆'` (the C-42 emitted-form assertion in `03-increments/increment-002.md`).
