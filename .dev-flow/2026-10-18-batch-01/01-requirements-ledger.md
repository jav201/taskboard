# Requirements ledger — taskboard — Batch 2026-10-18-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-18-batch-01.1 — present v3: the split view, the gantt note's structure, the view keys (P1)
- **Requirement:** HLR-1801, HLR-1802, HLR-1803, LLR-1801.1, LLR-1801.2, LLR-1801.3, LLR-1802.1, LLR-1803.1, LLR-1803.2, LLR-1803.3
- **Date:** 2026-10-18
- **What changed:** new requirements: `R` gains the `split` view (the prototype's D2 · stacked) beside the shipped `gantt` view, one note wrapper keeping line breaks, bullets and numbers for both, the fair share and its cut marks, the notes scroll (the cursor's note, else the whole area), the header's view word, the view keys, the hint row per view and the export of the current view to its own file. They supersede, law-driven: LLR-1001.1's oracle (PRES-R2 → PRES-V3-gantt; TC-1001, TC-1002, AT-1001 repointed), the header row of LLR-1601.1's frames (the view word), LLR-1602.2 (j)'s hint texts (TC-1604's hint arm), and the `_present_note_lines` wrapping of batch 2026-10-07-batch-04 (deleted with `_present_note_row`).
- **Why:** the operator, 2026-10-17: «si las demás tareas tienen texto, me gustaría que todas se vieran al mismo tiempo»; the verdicts of 2026-10-17/18 on `prototypes/present_views/` (round 2, D2); the coordinator's brief of 2026-10-18 (keys, shared state, R opens on gantt, the gantt note fix, the area scroll when every note is down to one line).
- **Evidence:** P-1..P-8 (`01-requirements.md` §2.7); `prototypes/present_views/views_d.py`, `views_proto.py`; `taskboard/views.py:6168-6176` on `base_ref` (the flattening wrapper).

### LED-2026-10-18-batch-01.2 — P2 iteration 1 amendments (P1, iterate-to-refine)
- **Requirement:** HLR-1801, HLR-1802, HLR-1803, LLR-1801.1, LLR-1801.2, LLR-1801.3, LLR-1803.1, LLR-1803.2
- **Date:** 2026-10-18
- **What changed:** Before → After. LLR-1801.3: traced to HLR-1801 → HLR-1803, whose statement now states the paging and the area scroll (A-1); `scroll` read as a ROW offset stepped by `PRESENT_SCROLL_STEP = 5` → a PAGE, the pages tiling the text with no gap (UX-1: at 80×24 a 5-row step skipped rows 3–4 of a 4-row window); Deleted: `PRESENT_SCROLL_STEP`; New: TC-1806's paging-coverage arm. LLR-1801.2: `PRESENT_VIEWS` defined in the statement and `floor_n` named (A-5); a cursor with notes keeps one row even below a row per note, a column's overflow ends on `↓ N more lines` (QA-1); a one-row cut ` … +N` → ` … +N lines` with no second `…` (UX-4, and the brief's wording); no shown open task → nothing under the rule (A-6, UX-5); the page-0 overflow rule worded once (A-7); TC-1802 gains two rows, TC-1804 80×19, the below-floor sizes 80×18 / 118×15 / 80×11, a per-note cut check and the all-hidden arm (QA-4, QA-5, QA-6), TC-1805 asserts `[link=…]` in both views and gains the escape sites of security S-2 (QA-11, S-2). LLR-1801.1: traced to HLR-1801 → HLR-1801, HLR-1802 (A-3). LLR-1803.1: "both reset" → only `_scroll` resets; `_scroll` is a page (A-2). LLR-1803.2: `w` is the screen width; the long wording `w >= 100` → when the whole hint fits `w - 2` cells (found by QA-10's 100-column arm: 107 cells in a 98-cell row); TC-1808 at five widths. HLR-1803: the AT's export arm asserts literal paths, exports both views, checks all seven key words in both SVGs, and compares the last `pgup` with the last page (QA-2, QA-3, QA-9); the `view_mode` read declared a seam (QA-8). HLR-1801: the below-floor and empty outcomes and their boundaries. §1.2: the README and backlog edits declared documentation deliverables (A-8). §6.3: UX-2, UX-3, UX-6, UX-7, S-1, S-3 declared and accepted.
- **Why:** the P2 review of 2026-10-18, iteration 1 (architect, qa-reviewer, ux-reviewer `iterate-to-refine`; security-reviewer `approve`, 3 LOW).
- **Evidence:** the reviewers' returns (`02-review.md` §Findings); the paging-coverage arm and the 100-column hint arm RED on the first draft (`tests/test_present_views.py::test_TC_1806_paging_down_shows_every_row_of_the_note`, `tests/test_present_views_app.py::test_TC_1808_the_hint_row_per_view`), green after the amendment; `evidence/gen-frames-001.txt` (the two 80×24 split frames written after D2).

### LED-2026-10-18-batch-01.3 — P2 iteration 2 minor amendments (P2 gate)
- **Requirement:** HLR-1801, LLR-1801.2, LLR-1801.3
- **Date:** 2026-10-18
- **What changed:** LLR-1801.2 Before: "at page 0 a column whose blocks exceed the room shows its first `room - 1` rows and `↓ N more lines`" → After: the same, or, when that would leave the cursor's block below the window (and the room holds 3 rows), the window ending on the cursor's block under `↑ N lines above` (QA2-1: the cursor's row was kept by the share and then windowed out at 80×18). TC-1804's below-floor arm: `… +` or `more lines` anywhere → the cursor's block on screen with its note's first words, and an edge mark (`more lines` / `lines above`) (QA2-1, QA2-2). TC-1805: the backslash note written `a\[b]` (QA2-3, a test hygiene fix). New mutant M18. LLR-1801.3: its ledger list names this entry because the window helper (`_present_window`) is shared with the paging. Not changed: UX2-1 (a 4-row cursor window pages 2 new rows a press at 80×24 — declared, nothing lost) and UX2-2 (the last page overlaps by one row — correct).
- **Why:** the P2 review of 2026-10-18, iteration 2 (architect `approve` — A2-1 found the README/backlog line already in §1.2; qa-reviewer `approve` with QA2-1..QA2-3; ux-reviewer `approve` with two notices).
- **Evidence:** `tests/test_present_views.py::test_TC_1804_below_a_row_per_note_every_missing_note_is_declared[80-18]` RED on the iteration-1 draft (the cursor's block below the window), green after; the 80×18 frame (`↑ 2 lines above` … `▌ Launch new homepage` / `▌ Go-live plan … … +12 lines`).

### LED-2026-10-18-batch-01.4 — PDR conditions folded into the contract (PDR seal)
- **Requirement:** LLR-1801.2, LLR-1801.3
- **Date:** 2026-10-18
- **What changed:** LLR-1801.3 Before: the whole text pages from its top for `p >= 1` → After: when page 0 windowed the column onto the cursor's block, the pages start at the first block page 0 showed (ux-reviewer PDR PC-1: at 80×18 the first `pgdn` jumped the text back to `Build component library`); New: a TC-1806 arm and mutant M19. LLR-1801.2: TC-1802 gains the room-6 row where the half-room promise binds (qa-reviewer PDR PC-1: M5 survived every other row, the surplus going to the cursor first); TC-1804's "the cursor's note longer as the cursor's" arm relabelled a regression pin, M5 no longer claimed there (qa-reviewer PDR PC-2).
- **Why:** the PDR of 2026-10-18 (architect, qa-reviewer, ux-reviewer: `approved with conditions`).
- **Evidence:** `tests/test_present_views.py::test_TC_1806_the_first_page_down_never_moves_the_text_back` green after the fold; mutant M19 restores the pre-fold paging and reddens it (packet 001's battery); the qa-reviewer's battery in its own scratch copy (`mut001.txt`: M5 SURVIVED the ns1 row and the cursor-gets-more arm).

### LED-2026-10-18-batch-01.5 — a resize resets the page (P3, increment 002)
- **Requirement:** LLR-1803.1
- **Date:** 2026-10-18
- **What changed:** Before: `_scroll` reset to 0 on a view change, a cursor move, `space` and `a` → After: also on a resize. TC-1810 gains the arm (`pgdn`, resize to 80×40, `_scroll == 0`); New: mutant N12. The parent HLR-1803 re-read: its "no row a page skips" and "no dead pages" hold only if a page belongs to the size it was cut for — unchanged in wording, now true across a resize.
- **Why:** code-review F1 (increment 002, MEDIUM): a page kept across a taller resize is clamped to a lower last page, so the next `pgup` presses repaint the same frame — dead pages.
- **Evidence:** `tests/test_present_views_app.py::test_TC_1810_the_bindings_and_the_scroll_state`; mutant N12 in `evidence/mutation-002.txt`.

### LED-2026-10-18-batch-01.6 — notes with wide glyphs wrap by cells (P3, increment 001)
- **Requirement:** LLR-1801.1
- **Date:** 2026-10-18
- **What changed:** Before: "each line wrapped by `textwrap.wrap` at `max(4, w - vis(lead))`" → After: wrapped at that many CELLS — `textwrap.wrap` when every glyph is one cell wide (so every ASCII frame, the PRES-V3 oracle included, is unchanged), else a greedy word wrap measured in cells (`_wrap_cells`). TC-1801 gains a CJK-and-emoji arm; New: mutant M20. Parent HLR-1801 re-read: "text from every shown open task with notes is on screen" and LLR-1801.3's "every wrapped row" now hold for wide glyphs too.
- **Why:** code-review F1 (increment 001, MEDIUM; security-reviewer S-3 at P2 had declared it): `textwrap` counts code points, so a CJK row came back 40 cells wide at w = 20 and `clip` hid half of it behind one `…` that no cut count or page could reveal.
- **Evidence:** `tests/test_present_views.py::test_TC_1801_line_breaks_bullets_and_numbers_are_kept` (the wide arm); `evidence/gen_frames.py` (the 8 frames unchanged); M20 in `evidence/mutation-001.txt`.
