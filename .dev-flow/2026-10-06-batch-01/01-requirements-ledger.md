# Requirements ledger — taskboard — Batch 2026-10-06-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-06-batch-01.1 — moving linked dates derived from the round-6 verdict (P1, iteration 1)
- **Requirement:** HLR-604, LLR-604.1, LLR-604.2, LLR-604.3, LLR-604.4, LLR-604.5
- **Date:** 2026-10-06
- **What changed:** new requirements: the cascade engine (`plan_move`, one overlap measure, snapshot/restore, `resolve_mode`; LLR-604.1); the `+`/`-` bump routed through it with the C-3 toast and one undo entry (LLR-604.2); the editor's date save routed through it (LLR-604.3); `m` re-applies the last move under the next mode (LLR-604.4); the per-project `date_links` setting in the project editor (LLR-604.5). US-604 is the batch's only story (D-601's split).
- **Why:** the round-6 verdict (push_delta default, per-project setting, `m` per move); the prototype's engine proved before the port (`evidence/p1-cascade-logic.txt`); P-1..P-8 executed TRUE (`evidence/p1-premises.txt`) — the write-site census, the editor's missing undo, the `extra` round-trip, the free `m`, the multi-task undo pattern, the sync merge list, the engine's asserts, the milestone-whole rule.
- **Evidence:** `evidence/p0-probes.txt`; `evidence/p1-premises.txt`; `evidence/p1-cascade-logic.txt`; frames `out/C-1a..d-*`, `out/C-2*`, `out/C-3-*` (worktree `kg-mejoras`).

### LED-2026-10-06-batch-01.2 — P2 iteration-1 findings folded (P1, iteration 2)
- **Requirement:** HLR-604, LLR-604.1, LLR-604.2, LLR-604.3, LLR-604.4, LLR-604.5
- **Date:** 2026-10-06
- **What changed:** every AT threshold re-derived by EXECUTING the prototype engine on the exact AT board (`p1-thresholds.txt`): AT-607 moves tm3 AND tm4 (+1d each), tm5 stays; AT-608's together arm gains the tm5 discriminator and the `Mobile +1d past ◆` clause; AT-609 moves tm3 and tm4 (+3d each); AT-610's arms corrected (together: td0/td5 +2d, `Data Warehouse +2d past ◆`; flag: nothing moves, the toast's `flagged` clause with the added days). The ONE overlap measure is now the shipped `link_overlap` applied to planned dates (D-633 — the prototype's milestone carve-out dropped; moved sets identical). The toast grammar adopts the approved C-3 ladder (names when they fit, count when not, the narrowing key suffix `· u undo · m change for this move`); `flagged` is reachable (the flag clause); `m`'s Key entry and the refusal literal pinned. New: D-634 (cascades touching >1 task save through `save_atomic`), the undated-task today base in LLR-604.1 (TC-627), §6.3 reworded (S-3/S-5), D-630/P-6 name the new-project sync path (S-4), RC-1(b) and P-1 evidence pasted (Q-6/A-6), §2.4's no-slow-state line.
- **Why:** P2 iteration 1 — four lenses FAIL (blockers Q-1/A-1/S-1/UX-1 and Q-3/A-2/S-2/UX-2; majors A-3, A-4/UX-3; minors and notices), every disposition in `02-review.md`.
- **Evidence:** `evidence/p1_thresholds.py`, `evidence/p1-thresholds.txt`; `02-review.md` iteration 1.

### LED-2026-10-06-batch-01.3 — P2 iteration-2 findings folded (P1, iteration 3)
- **Requirement:** HLR-604, LLR-604.1, LLR-604.2, LLR-604.5
- **Date:** 2026-10-06
- **What changed:** the toast literals re-pinned to EXECUTED strings (the iteration-2 text had pinned them unexecuted — the same defect class one layer down): the toast ladder is now defined (§1.3) and LLR-604.2 pins AT-607's toast at 118 (`pushed Add push, Offline sync +1d each`) and at 80 (`pushed 2 +1d each`); the project clause carries the full name or the FIRST WORD per the ladder — AT-610's clause corrected to `Data +2d past ◆`; the flag clause's grammar specified (`flagged ‹names› +‹N›d`, ADDED days) and pinned (`flagged Add push +1d` in AT-608, `flagged Revenue +2d` in AT-610). D-633 re-worded: the measures agree in the overlap regime and on every AT arm, they do NOT universally cancel — the slack-boundary behavior is the shipped one and TC-628 pins it (new). `new_conflicts` carries ADDED days, stated (not the prototype's totals). AT-610 pins the editor (the `+`-twice alternative dropped). D-634 extended to the undo's restore. §1.6 gained the refusal and flag-clause rows; §6.3's citation corrected; §5 lists both overlap listings.
- **Why:** P2 iteration 2 — qa PASS-WITH-NOTES (Q-7, Q-8), architect FAIL (A-7, A-8 blockers: the pinned toast literals matched nothing the adopted ladder produces at 118; A-9..A-11 majors), security FAIL (S-6, S-7 HIGH — the same two literals; S-8..S-11 LOW), ux FAIL (UX-8 major — the project-name literals; A-7, S-6, UX-9 minors). Every disposition in `02-review.md` iteration 2.
- **Evidence:** `evidence/p2_arch_probe.py`, `evidence/p2_arch_probe2.py` (the architect's executed ladder and dual-measure re-runs); `evidence/p1-thresholds.txt` (both overlap listings).

### LED-2026-10-06-batch-01.4 — P2 iteration-3 findings folded (P1, iteration 4)
- **Requirement:** LLR-604.2
- **Date:** 2026-10-06
- **What changed:** §1.3's toast-ladder definition corrected — the name budget NARROWS 12 → 8 across the rungs before the count forms (the 8-rung is load-bearing: AT-608's @118 toast lands on it; a fixed-12 reading flips the pinned `Mobile +1d past ◆` to RED — Q-9/A-16, executed). The flag clause gained its count and mixed forms (`flagged 2 +2d each`; `flagged 2 overlaps (‹A› +1d, ‹B› +3d)`) in §1.6 and LLR-604.2. The overlap bullet's agreement claim scoped to moved sets and added deltas (the conflict totals differ by the documented pre-existing 1d). §5 notes AT-608's evidence line shows the prototype's TOTAL (added = 1d). P-9 scoped: the two NEW strings (flag clause, refusal) have executed components and a stated derivation, not executed strings.
- **Why:** P2 iteration 3 — qa FAIL (major Q-9), architect PASS-WITH-NOTES (A-16 = Q-9; A-17, A-18), security PASS-WITH-NOTES (S-12, S-13), ux PASS-WITH-NOTES (UX-10, UX-11); dispositions in `02-review.md` iteration 3.
- **Evidence:** `evidence/p2_arch_probe.py` (checks corrected to the iteration-3 literals), `evidence/p2-arch-probe.txt` (4 PASS), `evidence/p2-arch-probe2.txt` (transcripts captured).

### LED-2026-10-06-batch-01.5 — increment 001 code-review folds (LLR-604.1)
- **Requirement:** LLR-604.1
- **Date:** 2026-10-06
- **What changed:** TC-629 and TC-630 added (the range becomes TC-618..TC-630): a move creating a FIRST overlap pair reports the added days, never a `KeyError` (C-1, HIGH); a planned task vanished before the restore is skipped, never an `AttributeError` (C-2, MEDIUM). `link_overlap` delegates to `_cascade_overlap` on the STORED dates — one rule implementation, the screen's exact semantics untouched (C-3, MEDIUM; C-4 accepted as stated: the milestone start==due collapse stays engine-only).
- **Why:** the code-reviewer's BLOCK-UNTIL on revision 1, fixed RED-first under the standing authorization's second exception (the increment was under construction), re-reviewed clean on revision 2 (PASS-WITH-NOTES). C-5 carried: `plan_move` stays strict on a missing moved-task id — the app gates before re-applying (`m`).
- **Evidence:** `evidence/inc001-c1-red.txt` (KeyError RED) · `evidence/inc001-mutations-r3.txt` (10 KILLED · 1 BAD · 0 SURVIVED) · `evidence/inc001-gate.txt` (2499 passed).

### LED-2026-10-06-batch-01.6 — increment 002 code-review folds (LLR-604.2, LLR-604.4)
- **Requirement:** LLR-604.2, LLR-604.4
- **Date:** 2026-10-06
- **What changed:** TC-631 added (an undated dependent under `together` — the toast's dependents sort must tolerate a planned `None` due; the original code raised `TypeError`, code review 1-1, HIGH). The project clause now fires when the project slips FURTHER past its due (`over > project_over_before`), not on any past-due state (1-2, MEDIUM). The flag clause's count form says `each` only when the added days are equal, else `overlaps (+1d/+3d)` (1-3, LOW). The toast is PLAIN TEXT with `markup=False` — the shipped TC-401 law (no Textual sink parses markup) reddened the prototype-coloured version; the contract pins only the text literals, so no threshold moved. The README keybinding table carries `m`; the key bar's more layer keeps every key with `m` added (KEYBAR_BASE re-derived, executed).
- **Why:** the code-reviewer's BLOCK-UNTIL on revision 1, fixed RED-first under the standing authorization's second exception, re-verified clean on revision 2 (PASS-WITH-NOTES, "OK to advance"). 1-4 nits: the restore loops stay hand-rolled (entry shape is a list, not the engine's snap dict); the mixed-shift pushed count form `pushed 2 (+3d/+6d)` stays unpinned by the contract, consistent with the flag form.
- **Evidence:** `evidence/inc002-red-on-inc001.txt` (AT RED on the increment-001 tree) · `evidence/inc002-mutations-r4.txt` (8 KILLED · 1 BAD · 0 SURVIVED) · the increment's gate transcript.

### LED-2026-10-06-batch-01.7 — the IFC Part B block for #f-date-links (increment 003)
- **Requirement:** LLR-604.5
- **Date:** 2026-10-06
- **What changed:** §4b gains the `project-date-links` COMPONENT block (added by the increment that created `#f-date-links`, per B1 D-514): the select's value rides the payload key `date_links`, consumed by ProjectModal, ProjectPicker, the app, and the AT. A note records that the editor's `#f-start`/`#f-due` are SHIPPED addresses rerouted, not new components.
- **Why:** B4 — a new addressable widget owes its boundary declaration in the same act that creates it.
- **Evidence:** `taskboard/modals.py` (`#f-date-links`) · `tests/test_cascade_app.py` AT-610.

### LED-2026-10-06-batch-01.8 — increment 003 reviews folded (LLR-604.2, LLR-604.3, LLR-604.4, LLR-604.5)
- **Requirement:** LLR-604.2, LLR-604.3, LLR-604.4, LLR-604.5
- **Date:** 2026-10-06
- **What changed:** increment 003 (the editor's date save routes through the cascade; the `Linked dates` select in the project editor) was implemented by an external agent (DeepSeek V4 Pro via OpenCode) under the coordinator's brief and verified by the coordinator. Folded: the independent second review's DS-1 (empty-title IndexError in `_short_title`; guard + TC-632's empty-titled-dependent arm), DS-2 (crash on a None planned due in the toast lead; the start-arm, kept as defense-in-depth), DS-3 (undated dependents no longer counted as "moved"), DS-6 (`bump_due` import dropped), DS-7 (`CASCADE_VERB["push"]`); the code-review's J (the toast seat gained `say_solo`; the editor passes False — D-629's silence clause; TC-632's silence arm + TC-635's milestone path), K (the milestone's cascade gate uses the POST-canonicalization due delta; a zero there skips the cascade — TC-634's RED is `evidence/inc003-k-red.txt`), L (the lead's due arm only when the due moved), M (a new project stores the rule only when chosen), N (empty project name); AT-611 (chain honesty through the app — the DS-4 gap); TC-633 (the undo entry holds the TRUE pre-edit dates for delta-0 fields). The IFC Part B `project-date-links` block (LED .7). The select sits OUTSIDE the pinned `.modal-grid` (test_details_grid TC-411) — declared for the P4 visual verdict alongside D-627.
- **Why:** the code-reviewer's BLOCK-UNTIL J+K on revision 1, fixed RED-first under the standing authorization's second exception; revision 2 verified K/L/M/N and narrowed J to its milestone sub-case (one keyword), fixed and pinned by TC-635; the DeepSeek Flash second review's findings folded by the coordinator. 9/9 increment-003 mutants KILLED (1 BAD harness proof).
- **Evidence:** `evidence/inc003-k-red.txt` · `evidence/inc003-mutations-r3.txt` (9 KILLED · 1 BAD · 0 SURVIVED) · `evidence/inc001-002-deepseek-review.md` · the increment's gate transcript.
