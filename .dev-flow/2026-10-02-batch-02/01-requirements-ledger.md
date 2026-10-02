# Requirements ledger — taskboard — Batch 2026-10-02-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-02-batch-02.1 — the colour budget reaches every view
- **Requirement:** HLR-201
- **Date:** 2026-10-02
- **What changed:** batch-01 applied the budget to the kanban and gantt panels only (its D10); the other seven views' titles and non-focus marks now leave the accent.
- **Why:** operator answer D10 "Hacer el pase global pronto"; the commission makes it this batch.
- **Evidence:** `evidence/taskboard-respuestas-a1.json` D10; P-1 census (`evidence/p0-probes.txt`).

### LED-2026-10-02-batch-02.2 — the chrome follows the budget
- **Requirement:** HLR-202
- **Date:** 2026-10-02
- **What changed:** key bar keys, ribbon clocks, modal titles and help headings leave the accent; the focused input keeps it.
- **Why:** answers HELP "Pasarlos a blanco brillante" and D10; BACKLOG UXV-9 (accent outside the panels).
- **Evidence:** P-2 (`evidence/p0-probes.txt`); `variants_polish.BUDGET` "key: bold bright key, muted verb".

### LED-2026-10-02-batch-02.3 — soon in amber, the packet quiet
- **Requirement:** HLR-203
- **Date:** 2026-10-02
- **What changed:** the ≤7-day token returns to `soon` (batch-01 made it `mut`); the packet leaves `bright`.
- **Why:** answers SOON "Volver a marcarlos con ámbar «pronto»" and PKT "Atenuarlo".
- **Evidence:** P-8.

### LED-2026-10-02-batch-02.4 — English everywhere
- **Requirement:** HLR-204
- **Date:** 2026-10-02
- **What changed:** batch-01 D12 kept the help prose Spanish; it and every other painted Spanish string become English.
- **Why:** answer D12 "Todo en inglés".
- **Evidence:** P-3 census.

### LED-2026-10-02-batch-02.5 — the paged-group hint
- **Requirement:** HLR-205
- **Date:** 2026-10-02
- **What changed:** batch-01 D9 drew no hint for a paged group; one dim row now says how many tasks are above and below.
- **Why:** answer D9 "Sí: «▲ 3 above / ▼ 2 below»" ("una fila tenue al borde de la página").
- **Evidence:** P-5.

### LED-2026-10-02-batch-02.6 — the finish toast
- **Requirement:** HLR-206
- **Date:** 2026-10-02
- **What changed:** batch-01 D14 drew no cue when `]` finished a task; a toast now names it.
- **Why:** answer D14 "Sí, un aviso corto" with the example «Fix checkout 500 error done · folded into ✓2 · u undo».
- **Evidence:** P-10.

### LED-2026-10-02-batch-02.7 — sticky visited projects
- **Requirement:** HLR-207
- **Date:** 2026-10-02
- **What changed:** the fold order gains a visited tier between the selected group and the rest.
- **Why:** answer UXV-2 "Mantener abiertos los que ya visité" ("hasta que no quepan; el resaltado no salta").
- **Evidence:** P-7, P-12 (`evidence/p1-fold-simulation.txt`: 3 → 2 upward moves at panel 80×22).

### LED-2026-10-02-batch-02.8 — due today counts
- **Requirement:** HLR-208
- **Date:** 2026-10-02
- **What changed:** the urgency weight counts open tasks due today as well as late ones.
- **Why:** answer UXV-3 "Sí: lo que vence hoy o está atrasado se pliega al final".
- **Evidence:** P-6; decision D-204 (the oracle 80×24 frame still folds Ops & Security).

### LED-2026-10-02-batch-02.9 — weekend shading
- **Requirement:** HLR-209
- **Date:** 2026-10-02
- **What changed:** batch-01 D5 did not ship the round-5 weekend shading; it ships at `k ≤ 1` with a re-measured background.
- **Why:** answer D5 "Agregarlo"; the commission asks the colour to survive 256-colour quantisation.
- **Evidence:** P-4 (`#161d27` → index 16 = the field; `#1a1d22` → 234).

### LED-2026-10-02-batch-02.10 — echo clip arrows
- **Requirement:** HLR-210
- **Date:** 2026-10-02
- **What changed:** a clipped echo end draws `◂`/`▸` instead of a bracket on the window edge.
- **Why:** BACKLOG UXV-7, discharged in this batch by the commission.
- **Evidence:** P-9.

### LED-2026-10-02-batch-02.11 — Setup rows keep their styles
- **Requirement:** HLR-201, LLR-201.3
- **Date:** 2026-10-02
- **What changed:** new: Setup's rows are assembled from styled pieces; before, `str()` of a styled `Text` dropped every style, so the cursor, the on/off chips and the check marks were painted plain.
- **Why:** P2 ux-reviewer UX-1 (blocker): the Setup re-tones and the cursor's kept accent could not be observed.
- **Evidence:** ux-reviewer span dump of the base Setup render (0 spans on body rows); P-13.

### LED-2026-10-02-batch-02.12 — the meter clause was a phantom
- **Requirement:** HLR-203
- **Date:** 2026-10-02
- **What changed:** deleted the due meter's "week category" (no such seat is painted: `HEAT` has no reader); `+8d` is `dim`, not `mut`; `today` keeps its tone.
- **Why:** P2 qa Q-1, Q-2 and ux UX-2 (C-36: an acceptance value that resolves to no painted constant).
- **Evidence:** P-14, P-15.

### LED-2026-10-02-batch-02.13 — only the previous group is sticky
- **Requirement:** HLR-207
- **Date:** 2026-10-02
- **What changed:** the session-long visited list became the previous group only.
- **Why:** P2 ux UX-4: a growing visited list lets quiet groups outrank urgent ones for the session (against UXV-3) and measured no better.
- **Evidence:** `evidence/p1-fold-simulation.txt` (`llr_207_1` vs `iter2_prev1_today`: 2 upward moves at 80×22 both).

### LED-2026-10-02-batch-02.14 — due today breaks the tie
- **Requirement:** HLR-208
- **Date:** 2026-10-02
- **What changed:** urgency weight ties are broken by the count of tasks due today before the earliest due.
- **Why:** P2 ux UX-3, qa Q-5: under weight alone the frame the operator complained about (Ops & Security folded at 80×24) did not change.
- **Evidence:** `evidence/p1-fold-simulation.txt` row `iter2_prev1_today`: 80×22 entry frame unfolds Website, Data, Ops.

### LED-2026-10-02-batch-02.15 — P2 iteration 2 notes
- **Requirement:** HLR-207, HLR-208, LLR-207.1, LLR-207.2
- **Date:** 2026-10-02
- **What changed:** HLR-208 says urgent groups are "offered rows first" (a group that does not fit is skipped, so a smaller quiet group can take rows); `previous` names the Inbox `INBOX_GROUP` and "no previous" `None`; HLR-207's earlier-visited clause gets a synthetic fixture.
- **Why:** P2 iteration 2: ux UX-11 (the old wording was false mid-walk), qa N-1, N-2.
- **Evidence:** ux-reviewer's walk at 80×24 (Ops folded at `tm6`, `ta1` while Data stays open); qa's probe6.

### LED-2026-10-02-batch-02.16 — `;` reaches the more layer
- **Requirement:** LLR-202.1
- **Date:** 2026-10-02
- **What changed:** LLR-202.1 also requires `;` to switch the key bar's layer; the toggle read Textual's CSS `layer` and never left `primary`.
- **Why:** increment 002 code review F3 (HIGH, pre-existing since 8b73920): HLR-202's "both layers" had no visible `more` half; decision D-218.
- **Evidence:** reviewer probe (`bar_layer` stays `primary` after two `;`); mutant F3 KILLED (`evidence/inc002-mutations.txt`).

### LED-2026-10-02-batch-02.17 — the filter has no key
- **Requirement:** HLR-204
- **Date:** 2026-10-02
- **What changed:** AT-204 cycles the team filter through the app's `team_filter_cycle` action instead of `f`; the help copy names only shipped keys (D-219).
- **Why:** found while translating: `f` is bound to `manage_phases`; `team_filter_cycle` has no key (BACKLOG, README audit #10); the base help also named `p` for pinning (`t` pins).
- **Evidence:** `taskboard/keymap.py` KEYMAP (`f` → `manage_phases`, `t` → `pin_toggle`, `p` → `add_project`).

### LED-2026-10-02-batch-02.18 — the weekend hex is a palette key, in the cell's own tag
- **Requirement:** LLR-209.1
- **Date:** 2026-10-02
- **What changed:** `WEEKEND_BG` is `HEX["weekend"]` and the background rides in each cell's own tag (`_on_weekend`); the helper is `GanttAxis.weekends()` (the name `gantt_weekends` was never built).
- **Why:** increment 004's gate run: two existing laws went RED on a per-cell wrapper with an undeclared hex — `test_prism_laws::test_every_lit_field_cell_carries_a_declared_hue` and `test_span_economy::test_collapse_removes_the_redundant_runs`; code review F4.
- **Evidence:** `evidence/inc004-reverse-census.txt`; mutants G9, G13.

### LED-2026-10-02-batch-02.19 — the soon tone names its seat
- **Requirement:** HLR-203
- **Date:** 2026-10-02
- **What changed:** HLR-203 names `reldue_token` (kanban, the Focus review rail, people, agenda) and declares the Focus view's `date_chip` (the Focus tiles, cards, image and compact cards, the detail pane and the review layout's selected-task line) outside it.
- **Why:** P4: the walkthrough saw `Oct 4 +4d` in slate on the Focus tiles (ux UXV2-1) — "a relative due token" read as every token; the operator's SOON answer named the kanban; qa G-003 asked for the recorded amendment rather than a decision note.
- **Evidence:** `evidence/p4-ux-walkthrough.txt` item 10; `04-validation.md` G-003.
