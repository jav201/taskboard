# Requirements ledger — taskboard — Batch 2026-09-30-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape below, and nothing above this line is ever edited._

### LED-2026-09-30-batch-01.1 — kanban badges supersede the AC5 / Prism priority-hue law
- **Requirement:** HLR-004
- **Date:** 2026-09-30
- **What changed:** before this batch the law (`tests/test_palette_ration.py` AC5 block) read "a judging hue (`over`, `soon`) is never worn by a priority mark; kanban marks priority with `!` in `ink`". For kanban cards it now reads: priority is a reverse-video badge in the highlight tones (`!!` over, `==` soon, `++` green). Every other view keeps the old law.
- **Why:** owner verdict 2026-09-30 ("el uso de insignias, reusando !!, == y ++ para 3 colores"), after seeing the conflict documented in `prototypes/kanban_priority/NOTES.md`.
- **Evidence:** test nodes whose expectation changes (P3 discharges each): `test_palette_ration.py::test_high_priority_is_a_glyph_and_wears_no_judging_hue` (card_cell default call keeps `!` — expected unchanged, verify), `::test_a_judging_hue_is_never_worn_by_a_name_or_a_priority_mark` (kanban badge exempted by token+reverse), `::test_every_view_that_marks_priority_marks_it_with_the_glyph` (`marks["kanban"]` becomes the `!!` badge).

### LED-2026-09-30-batch-01.2 — P2 fold into HLR-001 (UX-1, UX-2, UX-3, Q-10)
- **Requirement:** HLR-001
- **Date:** 2026-09-30
- **What changed:** the statement gained the tab order, keyboard Save, escape-discards and painted key hints; the threshold gained the preview floor (≥ 20 cols, rows ≥ notes rows − 2) and the 17-stop tab order; AT-005 added.
- **Why:** the P2 UX lens: visibility is not reachability, and focus/tab is the navigation model.
- **Evidence:** `02-review.md` findings UX-1, UX-2, UX-3, Q-10.

### LED-2026-09-30-batch-01.3 — P2 fold into HLR-002 (Q-3, UX-4)
- **Requirement:** HLR-002
- **Date:** 2026-09-30
- **What changed:** the preview renders on open (not only after an edit) and keeps the cursor's line in view; threshold rewritten to check both.
- **Why:** with only "updates after each edit" an empty-on-open preview passed; at 80×24 a top-anchored preview hides the line being typed.
- **Evidence:** `02-review.md` Q-3, UX-4.

### LED-2026-09-30-batch-01.4 — P2 fold into HLR-003 (Q-4, Q-5, Q-9, UX-5)
- **Requirement:** HLR-003
- **Date:** 2026-09-30
- **What changed:** band semantics stated (after focus filter, blocked included, ordered by the active sort, priority change moves the card and keeps the cursor); the AT matrix is derived from the seat's mode tuples × focus × show_archived; the fixture minimum is stated; AT-006 added.
- **Why:** the catalog listed the cases without expected values, and a hand-listed default-mode fixture would pass vacuously.
- **Evidence:** `02-review.md` Q-4, Q-5, Q-9, UX-5.

### LED-2026-09-30-batch-01.5 — the owner accepts all three badge colours, green included
- **Requirement:** HLR-004
- **Date:** 2026-09-30
- **What changed:** the green-vs-project-hue conflict (`++` in `green`, also an offered project hue), recorded at P2 as "not separately ruled", is now owner-accepted; THE GLYPH HOUSE comment in `taskboard/views.py` says so.
- **Why:** owner verdict 2026-09-30 on the batch report: "he APPROVES the priority colors, including green vs project color".
- **Evidence:** the verdict relayed by the coordinator; `views.py` GLYPH HOUSE comment.
