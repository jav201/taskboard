# Requirements ledger — taskboard — Batch 2026-10-21-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-21-batch-01.1 — the people round's four items and five decisions (P1)
- **Requirement:** HLR-2501, HLR-2502, HLR-2503, HLR-2504, HLR-2505, HLR-2506, HLR-2507, LLR-2501.1, LLR-2501.2, LLR-2501.3, LLR-2502.1, LLR-2503.1, LLR-2503.2, LLR-2504.1, LLR-2504.2, LLR-2504.3, LLR-2505.1, LLR-2505.2, LLR-2506.1, LLR-2506.2, LLR-2507.1
- **Date:** 2026-10-21
- **What changed:** new requirements: the people directory `~/.taskboard/people.json` (HLR-2501), the mention as `@handle` (HLR-2502), the `@` picker in the editor's notes (HLR-2503), the people view on `@` — A's panes with C's quote under each task and B's progress box, titled `PEOPLE · directory` apart from view 9 (HLR-2504), the person filter in `/` (HLR-2505), `@Name` in pink in the details, the card and the presentation (HLR-2506), team sync carrying handles only (HLR-2507). They extend the modal-keys law of batch 2026-10-20-batch-03 (HLR-2407) to `PersonForm` and `SearchPrompt`, a modal's buttons now read along its package bases.
- **Why:** the operator's commission and the round's verdict (`01-requirements.md` §1.4), item 1's objection composed as HLR-2504 states.
- **Evidence:** P-1..P-8 (`01-requirements.md` §2.7, `evidence/premises.txt`); `evidence/scan-p1.txt`; `prototypes/people_round/people-round.html`.

### LED-2026-10-21-batch-01.2 — the P2/PDR review amendments (P2, approve with conditions)
- **Requirement:** HLR-2501, HLR-2502, HLR-2503, HLR-2504, HLR-2505, HLR-2506, HLR-2507, LLR-2501.1, LLR-2501.2, LLR-2501.3, LLR-2502.1, LLR-2503.1, LLR-2503.2, LLR-2504.1, LLR-2504.2, LLR-2504.3, LLR-2505.1, LLR-2505.2, LLR-2506.1, LLR-2506.2, LLR-2507.1
- **Date:** 2026-10-21
- **What changed:** Before → After. HLR-2501/LLR-2501.1: an empty file → empty with no notice (architect A-6); the notice says `no copy could be kept` when the copy failed; `boards._keep_aside` → the public `boards.keep_aside` (A-3); the no-registry location marked a test seam (A-8); another window's adds shown after a restart (A-7, accepted); thresholds for the caps (qa QA-7) and another board drawing the people (QA-9). HLR-2502: AT-2502, the rename arm, and the US→HLR→AT map (A-4). HLR-2503/LLR-2503.2: `tab` closes the list; the list's keys act only while the notes hold the focus (A-5); the flip-up at 80×24 reached by `tab` (ux UX-3, QA-2); `up` with the list closed (QA-11). HLR-2504/LLR-2504.x: the key row per pane `↵ their tasks` / `↵ open task`, whole at 80 (UX-1, UX-4); `tasks read-only` and the 80-column head (UX-10); the dimmed cursor of the other pane (UX-6); whole-task scrolling and `↓ N more below` (UX-5); `PersonForm`'s labels and `⇥ next field` (UX-8); thresholds for `@` from the home and the main screen, the presentation, the errors, the strings, the seat keys' state and the tones (QA-3, QA-5, QA-6, QA-8, UX-2, A-11). HLR-2505: «at most 6 … all of them» → the first 6 by name (QA-1); `alt+p their page`, `↵ / alt+s filter` (UX-7); the gantt arm (QA-4). HLR-2507/LLR-2502.1: the link form's name bounded to 60, no scan without `@`, the linear-time threshold (security S-1). §6.3: S-2, S-3 accepted and logged; S-4, S-5 accepted; A-7.
- **Why:** the P2 review and the PDR of 2026-10-21 (architect: ARQ, P2 and PDR approve with conditions; qa-reviewer: P2 and PDR approve with conditions; ux-reviewer: P2 and PDR approve with conditions; security-reviewer: approve with conditions on S-1).
- **Evidence:** the reviewers' returns (`02-review.md` §Findings); security's timing probe (100 000 characters ≈ 25 s unbounded); qa's mutants M2, M3, M4, M6 (SURVIVED before, killed by the new arms).

### LED-2026-10-21-batch-01.3 — increments 001 and 002's code-review drifts (P3)
- **Requirement:** HLR-2501, HLR-2502, HLR-2506, HLR-2507, LLR-2501.2, LLR-2502.1, LLR-2506.1, LLR-2506.2, LLR-2507.1
- **Date:** 2026-10-21
- **What changed:** Before → After. HLR-2507's timing threshold: «under 0.5 s» (wall-clock) → under 2 s of CPU time, with a 40 000-distinct-handle craft added (increment 001's code review CR-1, CR-2: a quadratic dedupe at ~6 s, a wall-clock bound flaky under load) and the full note through the presentation's lines and colouring (security N-2 / test gap). LLR-2501.2: `edit` refuses a non-handle and writes back a person the file lost (CR-5). HLR-2506/LLR-2506.x: an empty directory draws as none in the preview too (increment 002's CR-1); a mark only at a whole mention (CR-3); the one-row cut painted (CR-4); the marks' pattern compiled once (security N-2).
- **Why:** increment 001's and 002's independent reviews (code-reviewer OK to advance both, with notes; security-reviewer APPROVE on S-1, N-1 accepted, N-2 fixed).
- **Evidence:** `03-increments/increment-001.md`, `03-increments/increment-002.md` §4b; `evidence/mutation-001.txt`, `evidence/mutation-002.txt`.

### LED-2026-10-21-batch-01.4 — increment 003's code-review drifts (P3)
- **Requirement:** HLR-2503, LLR-2503.2
- **Date:** 2026-10-21
- **What changed:** Before → After. «`tab` with the list open closes it; the list's keys act only while the notes hold the focus» → the focus leaving the picker by any path closes it (the list or the form), typing in the notes closes an open form, the mention replaces only the still-standing `@<typed>` span (code review CR-1, HIGH: the form's `enter` added a person and replaced the operator's text after `shift+tab`); a held handle with sentence punctuation opens nothing (CR-2, HIGH: `@ana.ruiz.` created `ana.ruiz2`); `enter` with no one listed is a new line (CR-4).
- **Why:** increment 003's independent review (code-reviewer FIX FIRST on CR-1, CR-2).
- **Evidence:** `03-increments/increment-003.md` §4b; `evidence/mutation-003.txt` (M3, M12, M13, M14).
