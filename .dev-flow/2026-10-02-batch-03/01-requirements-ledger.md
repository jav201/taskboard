# Requirements ledger — taskboard — Batch 2026-10-02-batch-03

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-02-batch-03.1 — two-row cards
- **Requirement:** HLR-301
- **Date:** 2026-10-02
- **What changed:** the grouped kanban's one-row card (title cut to ~8 chars, facts on the same row) becomes two rows: the title across the column, the facts on a quiet second row; the shipped badge stays before the title.
- **Why:** verdict round 1 (K-A first) and round 8 (badges stay, owner-accepted, LED .5 of 2026-09-30-batch-01).
- **Evidence:** P-1 (8.1 / 2.3 chars), P-6 (12.2 / 6.7 on the chosen frame) — `evidence/p0-probes.txt`.

### LED-2026-10-02-batch-03.2 — separators and adaptive widths
- **Requirement:** HLR-302
- **Date:** 2026-10-02
- **What changed:** a `┈` row between stacked cards; widths proportional to the longest title per column.
- **Why:** round 2 verdict "K-A con la regla ┈ — se ve menos cargado" (the underline variant K-A2 rejected).
- **Evidence:** `prototypes/kg_mejoras/NOTES.md` round 2.

### LED-2026-10-02-batch-03.3 — one band rule per group
- **Requirement:** HLR-303
- **Date:** 2026-10-02
- **What changed:** the per-column `▐ project` header becomes one rule across the board carrying the project's facts.
- **Why:** K-A (round 1); the base repeats 18 header cells (P-1).
- **Evidence:** P-1; `variants_kanban.k_a` band rule.

### LED-2026-10-02-batch-03.4 — the DONE rail
- **Requirement:** HLR-304
- **Date:** 2026-10-02
- **What changed:** the last phase becomes a 16-cell rail (7 below 100 cells).
- **Why:** K-A (round 1): finished work rests; open work gets the width.
- **Evidence:** `out/R-1b-118x30.txt`, `out/R-1b-80x24.txt`.

### LED-2026-10-02-batch-03.5 — one high band on top
- **Requirement:** HLR-305
- **Date:** 2026-10-02
- **What changed:** HLR-003 (2026-09-30-batch-01)'s per-column `── high ──` band becomes one board-wide band above the project bands, built from the same seat.
- **Why:** verdict R-1 (2026-10-01): R-1b, 9/9 highs visible at both sizes.
- **Evidence:** P-2; `NOTES.md` round 8.

### LED-2026-10-02-batch-03.6 — the cap
- **Requirement:** HLR-306
- **Date:** 2026-10-02
- **What changed:** the high band takes at most half the body, `+N more ↓` per column.
- **Why:** verdict R-1 "plus a cap with +N more … cap rule to be set at P1, e.g. a max row budget for the band with the overflow count per column"; rule D-303.
- **Evidence:** `NOTES.md` R-1 verdict; arithmetic in HLR-306's threshold, executed by TC-309.

### LED-2026-10-02-batch-03.7 — the colour budget on the new marks
- **Requirement:** HLR-307
- **Date:** 2026-10-02
- **What changed:** the new marks join the shipped budget (batches 01/02): no accent, soon amber, reverse selection.
- **Why:** commission item 8; round-7 budget.
- **Evidence:** `2026-10-02-batch-02` HLR-201/203.

### LED-2026-10-02-batch-03.8 — the help says what the board draws
- **Requirement:** HLR-308
- **Date:** 2026-10-02
- **What changed:** the kanban help drops the per-column band and explains the bands, `┈`, the rail and the cap.
- **Why:** the shipped copy ("the top of each column") becomes false with HLR-305.
- **Evidence:** `views.help_usage("kanban")` at `13745f6`.

### LED-2026-10-02-batch-03.9 — the board folds whole bands and says so
- **Requirement:** HLR-309
- **Date:** 2026-10-02
- **What changed:** NEW at P2 iteration 1: whole bands windowed around the selection with a `▲ N above / ▼ M below` row (D-302 before: the panel scrolls, no cue).
- **Why:** ux-reviewer UX-1 (major): the approved R-1b frame folds whole bands and names them; scrolling with no cue hid Ops & Security, the only task due today.
- **Evidence:** `out/R-1b-118x30.txt` last row; `02-review.md` UX-1.

### LED-2026-10-02-batch-03.10 — the cursor stays on a drawn card
- **Requirement:** HLR-310
- **Date:** 2026-10-02
- **What changed:** NEW at P2 iteration 1: a selection the narrow rail does not draw moves by the `z` rule; `]` posts a notification.
- **Why:** ux-reviewer UX-2 (major): `]` into a count rail left the cursor on an invisible task; the gantt's D14 precedent.
- **Evidence:** `02-review.md` UX-2; `app.py` `_notify_folded`, `_relocate_out_of_collapsed`.

### LED-2026-10-02-batch-03.11 — the high band counts what it draws; the tag tells projects apart
- **Requirement:** HLR-305
- **Date:** 2026-10-02
- **What changed:** the band's counts and `K high ↑` count the drawn cards; the tag extends word by word when two projects share a first word; it may shed at 80 cells.
- **Why:** ux-reviewer UX-5, UX-6, UX-8.
- **Evidence:** `out/R-1b-80x24.txt` (6 of 9 tags shed); `02-review.md`.

### LED-2026-10-02-batch-03.12 — the collapsed rail is narrow
- **Requirement:** HLR-304
- **Date:** 2026-10-02
- **What changed:** with the last phase collapsed the rail is 7 cells at every width; rail titles escaped (security S-1).
- **Why:** collapsing gives the width back to the open columns; S-1.
- **Evidence:** `02-review.md` S-1.

### LED-2026-10-02-batch-03.13 — the readability floors re-measured; the chrome stated
- **Requirement:** HLR-301, LLR-301.3
- **Date:** 2026-10-02
- **What changed:** the metric counts a title only when its whole first word is drawn, over the body rows; the floors move to ≥ 11.0 / ≥ 12 full at 118×30 and ≥ 5.5 at 80×24 (base 7.3 / 1.0, frame 11.8 / 6.2; LED .1's evidence figures 8.1 / 2.3 and 12.2 / 6.7 were the first metric's); the chrome is kept as shipped (LLR-301.3 NEW).
- **Why:** qa-reviewer Q-3 (major): the margin (0.2) was below the metric's noise (~0.46, header and partial hits); Q-4: the chrome was unstated.
- **Evidence:** `evidence/p0-probes.txt` (re-run 2026-10-02), `evidence/readability.py`.

### LED-2026-10-02-batch-03.14 — a stable window, a fold row that keeps both counts
- **Requirement:** HLR-309
- **Date:** 2026-10-02
- **What changed:** the window starts at the earliest band that keeps the selection's band drawn (before: the selection's band first, then below, then above); the fold row always prints both counts.
- **Why:** ux-reviewer iteration 2 UX-14 (major: a `down` into a visible band re-flowed the board) and UX-15 (blocker: at 80 cells the `▼` side was clipped away, hiding Ops & Security again).
- **Evidence:** `02-review.md` §Iteration 2.

### LED-2026-10-02-batch-03.15 — after `]` the cursor takes the neighbour
- **Requirement:** HLR-310
- **Date:** 2026-10-02
- **What changed:** after `]` the cursor lands on the card that took the moved card's place (else the one above); the `z` rule stays for other cases; the HLR and LLR wordings agree.
- **Why:** ux-reviewer iteration 2 UX-13 (major), UX-17 (wording).
- **Evidence:** `02-review.md` §Iteration 2; the gantt's neighbour rule in `app._select_first`.

### LED-2026-10-02-batch-03.16 — the cap at two thirds; nav claims scoped
- **Requirement:** HLR-306
- **Date:** 2026-10-02
- **What changed:** `R = max(5, (h − 3) // 2)` → `R = max(5, 2·(h − 3) // 3)`; the h-table re-derived; the 14-high arms become 6 / `+8` at 118×30 and 4 / `+10` at 80×24; the oracle arms state Backlog's 4 highs (11 rows) and the capping height (h ≤ 19).
- **Why:** qa-reviewer iteration 2 N-1 (blocker): Backlog holds 4 highs, not 3; the half-body cap capped the approved 80×24 frame (R = 10 < 11) — the operator approved that frame uncapped.
- **Evidence:** `evidence/p0-probes.txt` §P-2 (Backlog `tw5 tm4 ta2 to5`); arithmetic in LLR-306.1, executed by TC-309.

### LED-2026-10-02-batch-03.17 — widths by the frames' proportional rule
- **Requirement:** LLR-302.1
- **Date:** 2026-10-02
- **What changed:** the width split is proportional to the wants (the prototype's rule) with the floor-first split only as the fallback when a column would fall under `MIN_COL`.
- **Why:** P3 measurement: the floor-first split reads 5.3 chars at panel 80×24 (floor 5.5); the proportional split reproduces the approved frames exactly (11.75 / 13 full at 118×30, 6.2 / 3 at 80×24).
- **Evidence:** `evidence/inc001-widths.txt`.

### LED-2026-10-02-batch-03.18 — a band taller than the room is cut, not scrolled
- **Requirement:** HLR-309, LLR-309.2
- **Date:** 2026-10-02
- **What changed:** a band taller than the room is cut on card boundaries around the selection and the fold row counts the cards cut off (LLR-309.2 NEW); before: drawn alone, the panel scrolled.
- **Why:** P4 ux-reviewer UXV3-1 (blocker): scrolling took the head, the card's row 2 and the fold row out of the panel — under `g g` at 80×24 on the oracle board and on a 14-high board.
- **Evidence:** `evidence/p4-ux-walkthrough.txt`; `evidence/inc003-red.txt`.

### LED-2026-10-02-batch-03.19 — `at risk` cannot reach the screen
- **Requirement:** HLR-303
- **Date:** 2026-10-02
- **What changed:** the threshold notes that the shipped model offers no `at_risk` status (D-315).
- **Why:** P4 ux-reviewer UXV3-2: `PROJECT_STATUSES` has no `at_risk`; `Project.from_dict` maps it to `on_track`.
- **Evidence:** `taskboard/models.py` `PROJECT_STATUSES`; `evidence/p4-ux-walkthrough.txt`.

### LED-2026-10-02-batch-03.20 — the shared title seat
- **Requirement:** LLR-301.2
- **Date:** 2026-10-02
- **What changed:** the escaping clause covers `title_markup`, which writes through `_literal` since increment 001; one regression node per title seat (agenda, matrix, lanes, Focus inspector and review); the sample titles are 58 and 24 characters.
- **Why:** P4 qa-reviewer G-003a (a shared helper changed outside the declared scope, with no regression node) and G-003b.
- **Evidence:** `evidence/inc003-red-on-base.txt` (the seat nodes RED on `13745f6`).

### LED-2026-10-02-batch-03.21 — the cut keeps whole cards and every count
- **Requirement:** LLR-309.2
- **Date:** 2026-10-02
- **What changed:** the cut skips a single band that exactly fits; draws whole cards only (`3j + 2` rows); holds the band's end; counts open cards, not rail titles; and the fold row drops the `▲` names, then the cut band's name, before clipping the `▼` list.
- **Why:** code-reviewer round 1 of increment 003: F1 (HIGH, an exact fit cut), F2 (HIGH, counts clipped), F3, F5, F6, F7.
- **Evidence:** `evidence/inc003-red-r1.txt`; `evidence/inc003-mutations-r2.txt`.
