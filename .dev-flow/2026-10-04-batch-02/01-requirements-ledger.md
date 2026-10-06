# Requirements ledger — taskboard — Batch 2026-10-04-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-04-batch-02.1 — milestones derived from the round-5 verdict (P1, iteration 1)
- **Requirement:** HLR-601, HLR-602, HLR-603, HLR-605, LLR-601.1, LLR-601.2, LLR-601.3, LLR-602.1, LLR-602.2, LLR-602.3, LLR-603.1, LLR-603.2, LLR-605.1, LLR-605.2, LLR-605.3, LLR-605.4
- **Date:** 2026-10-04
- **What changed:** new requirements: the milestone flag on `Task` with `M`, the editor box, the details mark, team sync and undo (HLR-601); the gantt milestone row, reached rows, ruler marks and legend (HLR-602); milestones out of every kanban count and onto the project band rule (HLR-603); the one-time offer with backup, log, `u`, run-once and fail-closed (HLR-605). US-604 (moving linked dates) is not derived: D-601.
- **Why:** round-5 verdict "M-1 y M-2" (a flag on Task), M-3 ruled a one-time upgrade migration; the operator's migration safeguard "Sí: respaldo + registro + deshacer"; P-1..P-17 measured the shipped behaviour each requirement changes; P-16 executed the prototype's rules for every oracle row.
- **Evidence:** `evidence/p0-probes.txt`; `evidence/p1-premises.txt`; `evidence/p1-thresholds.txt`; `evidence/base-suite.txt`; `evidence/p1-offer-census.txt`; frames `out/M-1-118x30.txt`, `out/M-2-118x30.txt`, `out/M-3-118x30.txt`, `out/AX-2-118x30.txt` (worktree `kg-mejoras`).

### LED-2026-10-04-batch-02.2 — P2 iteration-1 findings folded (P1, iteration 2)
- **Requirement:** HLR-601, HLR-602, HLR-603, HLR-605, LLR-601.1, LLR-601.2, LLR-601.3, LLR-602.1, LLR-602.2, LLR-602.3, LLR-603.1, LLR-603.2, LLR-605.1, LLR-605.2, LLR-605.3, LLR-605.4
- **Date:** 2026-10-04
- **What changed:** Before → After, by requirement. HLR-601: the teammate `"yes"` arm (Deleted from AT-601, New in TC-607); toasts `start was`, warning severity (New). HLR-602: ruler arm on `Revenue model signed off`, field-cell date, `↑` from `Build component library`, legend at 80, the reached toast on `]` (New). HLR-603: band `N open`/fold counts and the selection exclude milestones, a milestone-only project draws no band (New); the Website literal "68-cell segment" → the shipped-room segment tokens; Ops at 118×40; `g`, `M`/`]` arms (New). HLR-605: "pre-start bytes" → "the bytes immediately before the conversion"; quit unanswered, ineligible-at-answer, seeded marks (New); "created board" (Deleted) → `Board.load` seeds both marks. LLR-601.1: field position, TC-607 and TC-608 (New). LLR-601.2: `?` Keys threshold replaces "more layer lists". LLR-601.3: the due wins over a typed start (New); 18 widget ids (canon LLR-001.3 amended); fold N−1/N. LLR-602.1: merged by due; the readers listed; `_notify_folded` (New). LLR-602.2: escape + S1 arm (New). LLR-602.3: legend after the selection item. LLR-603.1: `_select_first` (New). LLR-603.2: the band room, `+N ◆` alone, `today` soon, kanban help/legend (New). LLR-605.1: non-text titles excluded. LLR-605.2: candidates re-read, each once, restore before best-effort cleanup, malformed mark forces backup/log (New). LLR-605.3: last step of `on_mount`, silent mark-only failure, the `milestones` undo key (New). LLR-605.4: first-row highlight, heading `space` no-op, ids by option index, 34-candidate 80×24 fit (New). §1.6 NEW literals; §2.3 context of use; P-18, P-19; D-611 rewritten (patch `milestones_marked`); D-612..D-625; §5 seam mechanism and controls.
- **Why:** P2 iteration 1 (`02-review.md`): blockers Q-1 (the literal could not fit the shipped room: P-18) and A-1 (no shipped surface for a foreign milestone); majors Q-2..Q-13, A-2..A-4, UX-1..UX-4; security S-1..S-9 (0 HIGH).
- **Evidence:** `evidence/p1-thresholds-shipped.txt`; `02-review.md` §Findings; `evidence/captures/base-*` re-taken on the shifted board.

### LED-2026-10-04-batch-02.3 — P2 iteration-2 findings folded (P1, iteration 3)
- **Requirement:** HLR-601, HLR-602, HLR-603, LLR-601.2, LLR-602.1, LLR-603.1, LLR-605.2
- **Date:** 2026-10-04
- **What changed:** HLR-601: AT-601 runs in the gantt (`3`, `↓` to `Rate limiting`) — Before "in the kanban (`4`)"; New: the team arm (the pushed `board.<user>.json` holds `"milestone": true`). HLR-602 / LLR-602.1: "`]` on Launch → one reached toast" → "`]` pressed until Done (four presses) → at the last one reached toast"; New: AT-602's reached arm. HLR-603: New: the `/` filter's counts keep counting milestones. LLR-603.1: the z rule in the presentation's own column order; New: a lanes-window arm. LLR-601.2: ‹where› only when a band will carry it; New: last-open-card and Inbox arms; §1.6 title cut 40. LLR-605.2: New: the log's `note` that a restored backup is offered again. P-18 reworded (render height vs terminal size); §5 census pass condition (≥ 274 suppressed, 0 offers in unmarked nodes); §2.6 refinement log and §5 AT table compacted (V26 budget).
- **Why:** P2 iteration 2 (`02-review.md` §iteration 2): majors A2-1/Q2-2, Q2-1/A2-2, Q-12 (partial); minors A2-3, A2-4, Q-9, Q-11, Q2-3, UX2-1..UX2-4, UX-10, S-7b.
- **Evidence:** `02-review.md` iteration 2; `app.py:735-747` (`]` = one phase), `app.py:386` (the sync interval).

### LED-2026-10-04-batch-02.4 — P2 iteration-3 minors folded at the gate
- **Requirement:** HLR-601, HLR-603, LLR-603.1, LLR-605.2
- **Date:** 2026-10-04
- **What changed:** HLR-603: Deleted "the `/` filter's counts keep counting milestones"; New: the kanban's `/` filter `N of M` excludes milestones like every other kanban count (LLR-603.1 names `render_view`'s kanban branch; TC-612 arm `0 of 25`). HLR-601: the team arm polls the pushed file for at most 5 s. LLR-605.2: the threshold asserts the log's `note`.
- **Why:** P2 iteration 3: qa Q3-1, Q3-2, Q3-3; ux UX3-1 (the clause contradicted the statement's own exclusion list); security S-7b (the note had no threshold arm). All minor; architect PASS, ux PASS.
- **Evidence:** `views.py` `render_view` kanban branch (`total = len(board.visible_tasks(...))`); `02-review.md` iteration 3.

### LED-2026-10-04-batch-02.5 — the editor start toast only for a start the user changed (increment 001)
- **Requirement:** LLR-601.3
- **Date:** 2026-10-04
- **What changed:** Before: "a typed start ≠ the due is replaced by the due and the editor start toast says so". After: "a start ≠ the due is replaced by the due, and the editor start toast says so when the user changed the start field". New threshold arms: a milestone's due alone edited → no start toast; a milestone saved with both dates cleared → not a milestone, one refusal toast. Parent HLR-601 re-read: unchanged (the due is the date; the toast is wording).
- **Why:** increment 001 code review F-4 (the start field is pre-filled with the old date, so editing a milestone's due always toasted) and F-1 (the cleared-dates refusal branch had no arm). RED-first: `evidence/inc001-f4-red.txt` (the due-only arm failed on the r1 product), green `inc001-f4-green.txt`.
- **Evidence:** `03-increments/increment-001.md` §4b.

### LED-2026-10-04-batch-02.6 — the start toast also when a task becomes a milestone (increment 001, F2-1)
- **Requirement:** LLR-601.3
- **Date:** 2026-10-04
- **What changed:** Before (LED .5): "the editor start toast says so when the user changed the start field". After: "… says so when the task becomes a milestone or the user changed the start field". New threshold arm: a task's box ticked alone (start ≠ due) → one start toast. Parent HLR-601 re-read: unchanged.
- **Why:** increment 001 r2 code review F2-1 (HIGH, product, the increment under construction): the LED .5 fold silenced the toast when an ordinary task became a milestone with its start untouched, so an editor save (no undo) dropped the start without a word. Fixed without stopping under the standing authorization's second exception; RED-first `evidence/inc001-f2-1-red.txt` (the tick-only arm failed on r2), green `inc001-f2-1-green.txt`.
- **Evidence:** `03-increments/increment-001.md` §4b.

### LED-2026-10-04-batch-02.7 — the filter count's emitted form (increment 003, C-36 / C-42)
- **Requirement:** HLR-603, LLR-603.1
- **Date:** 2026-10-04
- **What changed:** Before: "the `/` filter's `N of M`" and the TC-612 arm "paints `0 of 25`". After: "the `/` filter's `N/M tasks`" and "paints `0/25 tasks`". Parent HLR-603 re-read: the obligation is unchanged (milestones not counted); only the literal was wrong.
- **Why:** the literal folded at the P2 gate (LED .4) named no defined form: the filter bar emits `‹hits›/‹total› tasks · esc clears` (`views.filter_bar`). Asserting the emitted form (C-42) exposed the phantom (C-36) at increment 003's first run.
- **Evidence:** the rendered kanban filter row, `render_view("kanban", …, search_query=…)` → `/ mockups▌ … 1/25 tasks · esc clears`.

### LED-2026-10-04-batch-02.8 — the band exists with done cards; the legend reads the drawing seat (increment 003, K-1)
- **Requirement:** HLR-603, LLR-603.2
- **Date:** 2026-10-04
- **What changed:** HLR-603 / D-623: Before "a project whose only open items are milestones draws no band". After "a project with no card in the kanban, open or done, draws no band" (a project with only done cards keeps the shipped done-rail band, and its rule carries its milestones). LLR-603.2: New `band_rule_facts`, the one seat for a rule's facts, read by the renderer and by `legend_entries("kanban")`, which now takes the presentation, grouping and focus and names `◆` exactly when a rule draws one. Parent HLR-603 re-read: unchanged in obligation.
- **Why:** increment 003 code review K-1 (MEDIUM, product): the legend entry was keyed on a different rule from the drawing — listed in matrix, lanes and other groupings where no rule carries `◆`, and silent for a done-cards-only band that does; the reviewer's decision note: the band exists because of the shipped done rail, so the requirement's wording was wrong, not the code. K-2: no node pinned the help and legend.
- **Evidence:** `evidence/inc003-k-red.txt` (5 of 6 new arms RED on the r1 product, restored byte-exact); `03-increments/increment-003.md` §4b.

### LED-2026-10-04-batch-02.9 — IFC Part B: the editor's milestone box and the offer's list (increment 004)
- **Requirement:** LLR-601.3, LLR-605.4
- **Date:** 2026-10-05
- **What changed:** New COMPONENT blocks in §4b: `editor-milestone` (`#f-milestone`, owner LLR-601.3, created by increment 001) and `milestone-offer` (`#offer-list`, owner LLR-605.4, created by increment 004). §6.2's "why" column shortened (V26 budget); the decisions are unchanged.
- **Why:** §4b says each NEW addressable widget's block is added by the increment that creates it (B1 D-514). Increment 001 did not add its block — added here, late, and said so.
- **Evidence:** `taskboard/modals.py` `TaskModal.compose` (`id="f-milestone"`) and `MilestoneOffer.compose` (`id="offer-list"`).

### LED-2026-10-04-batch-02.10 — the offer's dates, row and undo wording (increment 004 review)
- **Requirement:** LLR-605.2, LLR-605.3, LLR-605.4
- **Date:** 2026-10-05
- **What changed:** LLR-605.2/605.3: Before "the undo entry holds every converted task's flag and start". After "… flag, start and due as stored"; the failure path restores the due too and the log records `due_before` and the start actually written. LLR-605.4: Before "the title (cut with `…` before the meta)". After "(only the box coloured), the title cut with `…` to the cells the row leaves". §1.6 undo toast: Before "they are one-day tasks again". After "the tasks are back as they were".
- **Why:** increment 004 security S4-1 (LOW): converting canonicalises an oddly spelled due that `u` and a failure did not put back; code review O-1 (MEDIUM, product): a long title pushed the project and date off the row with no `…`; O-2 (LOW): the box's colour was the row's base style; NIT: a converted due-only task does not become a one-day task again. RED-first `evidence/inc004-r2-red.txt` → `inc004-r2-green.txt`.
- **Evidence:** `03-increments/increment-004.md` §4b.

### LED-2026-10-04-batch-02.11 — the reached milestone's tone (the operator's visual verdict, UXV-5)
- **Requirement:** HLR-602, LLR-602.2, LLR-603.2 (the reached arms), AT-602
- **Date:** 2026-10-06
- **What changed:** Every "ash" that meant a REACHED milestone now means the reached grey — a new palette tone `reached` `#7a828c` (4.9:1 on `#0d1117`, measured). Before: "a reached one as `◆✓` with its label and date in ash" (HLR-602), "reached all ash" (LLR-603.2), "`ash` reached" (`milestone_tone`, LLR-602.3), "its `◆`, `✓`, label and date in the ash colour" (AT-602). After: the reached grey in every one of those seats. The consumed FIELD keeps `ash` `#6b4a3f` (spent days, elapsed span, archived marks) — its quietness was never the finding, and the operator accepted the field in the PV-601/605 captures.
- **Why:** the operator's visual verdict on batch B2a (`taskboard-veredicto-b2a.json`, 2026-10-06): PV-601..PV-611 all **accepted**; UXV-5 decided **"Aclararlo a un gris legible (~4.5:1)"** — the reached ash `#6b4a3f` on `#0d1117` measured ~2.4:1, near illegible. UXV-2, UXV-4, UXV-7, UX-12 carried no change request (their questions ride on the accepted PV-611/604/603/609).
- **Evidence:** RED-first — `tests/test_gantt_milestones.py` and `tests/test_kanban_milestones.py` asserted the new tone against the old code (4 RED: TC-610[tw0], TC-611, AT-602, TC-613), then the eight seats moved (`milestone_tone`, `gantt_milestone_cells` ×2, `gantt_milestone_chip`, `_gantt_legend`, the gantt row title, the band-rule piece, the help map). Retaken captures: `evidence/captures/close-gantt-*`, `close-kanban-*`, `close-legend-gantt-*`, `close-gantt-reached-*`.
