# Requirements Document — taskboard — Batch 2026-10-02-batch-03

> Live contract (current state only). Mode `core`. Language `en`. The append-only ledger is
> `01-requirements-ledger.md`. Template: flow `templates/req-template.md` (reserved field
> names kept literal). Ids use a batch-disjoint `3xx` range (`US-301`, `HLR-301`,
> `LLR-301.1`, `AT-301`, `TC-301`): `0xx`, `1xx` and `2xx` are taken in the record and the canon.

## 1. Introduction

### 1.1 Purpose
Batch A2: make the kanban readable. The shipped grouped presentation repeats a project header
in every column, cuts every title to about eight characters and lifts open highs into a
separate band per column. This batch replaces its body with the layout the operator chose in
the `kg_mejoras` prototype rounds — K-A readable cards with the `┈` rule (rounds 1–2) and the
R-1b arrangement (round 8): one board-wide high band on top, capped with "+N more" (verdict
2026-10-01).

### 1.2 Scope
In: the kanban's grouped presentation (the first `tab` stop, key `4`) — its cards, its group
rows, the separators between stacked cards, the DONE column, the column widths, the high band
and its cap, the arrow-key order over all of it; the kanban help and legend copy that describes
those marks.
Out: the matrix and lanes presentations (unchanged, they keep working); K-B (time rail) and the
chain map (Batch C); the prototype's selected-card detail line (not in the commission's list;
BACKLOG — the band windowing and its fold row ARE in, HLR-309); the age-thickness spine of
the prototype (D-306); any key, model field or dependency. Every other `BACKLOG.md` item.

### 1.3 Definitions
| Term | Definition |
|------|------------|
| open column | a phase column other than the board's last phase (`board.phases[:-1]`) |
| rail | the board's last phase (`board.is_done`), drawn as a narrow column to the right of the open columns |
| group | one of the seat's groups (`kanban_order`): a project (Inbox last) under group mode `project`; High/Normal/Low under `priority`; Overdue/This week/Later/No date/Done under `horizon` |
| band | one group's block of rows across every column: its band rule, then the group's cards per column, then its rail cell |
| band rule | the one row that opens a band and names its group across the full panel width |
| high band | the band drawn first, holding every column's open high cards as the seat lifts them (`kanban_order(..., band=True)`, group `KANBAN_BAND`) |
| cell | the rows of one band in one column |
| card | one task drawn as two rows in a cell |
| panel / terminal size | `render_*` takes the panel's size; the app's terminal is 2 rows taller (ribbon + key bar), same width (`evidence/p1-geometry.txt`). ATs name terminal sizes, TCs panel sizes |

### 1.4 References
Seed: `BACKLOG.md` "Batch A2 — readable kanban K-A + R-1b". Prototype worktree `kg-mejoras`,
`prototypes/kg_mejoras/`: `NOTES.md` (verdicts rounds 1–2, 7, 8), `IMPLEMENTATION-PLAN.md`
§Batch A and §R-1, `variants_kanban.k_a(sep_mode="rule")`, `variants_reconcile.py` (R-1b),
`out/R-1b-118x30.txt`, `out/wt-R-1b-120x32.png` (visual oracle), `capture_kanban.py`
(`readability`). Re-derived, never pasted. Oracle board: `tests/kg_board.py`. Shipped seat:
`views.kanban_order`, `views.card_cell`, `views.PRIORITY_BADGE`.

## 2. Overall description

### 2.1 Product perspective
Textual TUI (`textual 8.2.8`, `rich 15.0.0`). `render_view("kanban", …)` returns a rich `Text`
for the board panel and fills `line_map` (task id → row); `nav_model("kanban", …)` returns the
arrow-key columns; the app scrolls the panel to `line_map[selected]`. The kanban is a scrolling
panel: a render taller than the panel scrolls.

### 2.3 User characteristics
One owner-operator (Javier), keyboard-first, Windows Terminal from 80×24 to full screen, judges
TUI work on real renders. Context of use: the daily read of the kanban (key `4`), moving cards
between phases with `[`/`]`, walking with `j`/`k`/arrows.

### 2.4 Constraints
≤ 4 SOURCE files per increment; no new dependency; `render_view`, `nav_model`,
`legend_entries`, `help_usage`, `help_example` keyword contracts are consumed by `app.py`,
`modals.py` and the tests; the seat `kanban_order` keeps its signature and results (its
callers in lanes and matrix are untouched). The shipped colour budget holds (batches 01/02):
the accent only for focus and today; ≤7-day dues amber; the selection is reverse video.

### 2.5 Assumptions
- A1: the oracle board (`tests/kg_board.py`, 28 tasks, 5 projects, 9 open highs) is the
  measurement board; renders of it at panels 118×30 and 80×24 are the evidence.
- A2: the readability metric is the prototype's (`evidence/readability.py`, re-derived),
  measured on the panel's first `h` rows — what the viewport shows at scroll 0.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-301 | As the board owner, I want each kanban card to show its title across the whole column width with its facts on a quiet second row, and stacked cards separated by a light rule, so that I can read the titles without opening the cards. | verdicts rounds 1–2 (K-A, `┈` rule "se ve menos cargado") | READY |
| US-302 | As the board owner, I want each project named once in a band across all columns, with its open count, risk and due date, and the done work as a narrow rail, so that the board stops repeating itself and spends its width on open work. | verdicts rounds 1–2 (K-A) | READY |
| US-303 | As the board owner, I want every column's open high-priority cards gathered in one band at the top of the board, naming their project, and capped so it never takes over the screen, so that the urgent work is the first thing I read and the rest of the board stays in view. | verdict round 8 (R-1b) + cap "+N more" (2026-10-01) | READY |

#### Refinement log

**US-301 — readable cards**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality:** two-row cards, the shipped badge kept before the title (owner-accepted), a dim meta strip on row 2 (age, dependants, due — due last to drop); `┈` between stacked cards; adaptive column widths. Out of scope: the age-thickness spine (D-306).
- **Feasibility:** one renderer in `views.py` re-derived from `variants_kanban.k_a`; the nav seat is the shipped `kanban_order`.
- **Evaluability:** at terminal 118×32 on the oracle board, key `4`: every drawn open card is two rows; the measured readability rises from 7.3 to ≥ 11 chars per title (P-1, P-6).
- **Classification:** READY.

**US-302 — project bands and the DONE rail**
- **INVEST:** all ✓.
- **Evaluability:** key `4` draws one band rule per project (no per-column header); the last phase is a rail of done titles at width ≥ 100 and `✓N` below.
- **Classification:** READY.

**US-303 — the high band and its cap**
- **INVEST:** all ✓. The cap rule is set here (HLR-306).
- **Evaluability:** key `4` draws the 9 open highs in one band above every project band, each naming its project; on a board with 14 highs in one column at terminal 118×32 the band keeps two thirds of the body at most and says `+N more ↓`, and the overflow cards stay reachable with `down`.
- **Classification:** READY.

**Not a story — the coexist-or-replace question (commission item 9):** decision D-301 (replace the grouped presentation's body; `tab` keeps grouped → matrix → lanes).

### 2.7 Premise evaluation (C-43)

| # | Premise | Tier | Verdict | Executed evidence | Disposition |
|---|---|---|---|---|---|
| P-1 | The shipped grouped kanban on the oracle board reads 7.3 title chars on average (0 of 28 in full) at panel 118×30 and 1.0 (0 full) at 80×24, measured on the body rows with the first-word rule (P2 Q-3); it draws 18 project-header cells and 3 per-column `── high` dividers | premise | ✅ TRUE | `evidence/p0-probes.txt` §P-1 | HLR-301 threshold, AT-301 |
| P-2 | `kanban_order(..., band=True)` lifts 9 open highs from 4 projects on the oracle board: Backlog `tw5 tm4 ta2 to5`, Next `ta3 to2`, Doing `tw3 ta4 to1` | premise | ✅ TRUE | `p0-probes.txt` §P-2 | HLR-305 |
| P-3 | The grouped nav returns 5 columns, the last one the Done phase (`tw1 tm1 td1`) | premise | ✅ TRUE | `p0-probes.txt` §P-3 | HLR-304, HLR-305 |
| P-4 | `tab` in the kanban cycles `('grouped', 'matrix', 'lanes')` | premise | ✅ TRUE | `p0-probes.txt` §P-4 (AST of `action_toggle_presentation`) | D-301 |
| P-5 | `board.is_done(t)` is `t.phase == board.phases[-1]` | premise | ✅ TRUE | `p0-probes.txt` §P-5; `models.py` `Board.is_done` | HLR-304 |
| P-6 | The chosen R-1b frame, re-rendered over this tree with the same metric, reads 11.8 chars (13 in full) at 118×30 and 6.2 (3 in full) at 80×24 | premise | ✅ TRUE | `p0-probes.txt` §P-6 (C-39 pre-execution of the readability threshold) | HLR-301 threshold |
| P-7 | The board panel is the terminal's width and 2 rows shorter: terminal 118×30 → panel 118×28, 80×24 → 80×22, 120×32 → 120×30 | premise | ✅ TRUE | `evidence/p1-geometry.txt` | §1.3, AT sizes |
| P-8 | Base suite is green | premise | ✅ TRUE | `python -m pytest -q -p no:cacheprovider` at `13745f6` (`evidence/base-suite.txt`) | — |

- **Premise evaluation:** 8 premise(s) · ✅ TRUE 8 / ❌ FALSE 0 / ❓ UNDECIDABLE 0

### 2.8 Fork preconditions (C-52)
- **Fork preconditions:** none — this batch runs one lane

## 3. High-level requirements (HLR)

### HLR-301 — A card is two rows: the title across the column, the facts beneath
- **Traceability:** US-301
- **Ledger:** LED-2026-10-02-batch-03.1, LED-2026-10-02-batch-03.13
- **Statement:** When the grouped kanban draws a card in an open column, the system shall draw it as exactly two rows of the column's width: row 1 the spine, the shipped priority badge of an open card and the title's head cut on a word boundary at the full remaining width; row 2 the spine, the rest of the title indented under its head and a meta strip of the card's link, image, age, dependants and relative due tokens, shed from the left under width pressure so that the due token is the last to go; the selected card's title shall be drawn in reverse video.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_301 or TC_302 or TC_303"`
- **Numeric pass threshold:** oracle board, the panel's body rows at scroll 0 (`evidence/readability.py` `body`: the head and the fold row dropped, a title counted only when its whole first word is drawn): panel 118×30 average visible title chars ≥ 11.0 and ≥ 12 titles in full (base 7.3 and 0, P-1; the approved frame 11.8 and 13, P-6); panel 80×24 average ≥ 5.5 (base 1.0; frame 6.2); through the app at terminals 118×32, 80×26 and 80×24 (panels 118×30, 80×24, 80×22) every drawn card is two rows; every drawn open card's two rows sit on consecutive lines; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** titles read in full or nearly so; the facts sit quietly under them.
  - **Shipped surface:** `TaskboardApp` key `4` (painted board panel via `App.run_test`).
  - **Acceptance test(s):** AT-301
  - **Boundary catalog (QC-3):** ☑ boundary (a title longer than two rows; a first word wider than the cell; a 12-cell column) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base tree draws one-row cards reading 7.3 chars → RED (P-1).

### HLR-302 — Stacked cards are separated; columns are sized by their content
- **Traceability:** US-301
- **Ledger:** LED-2026-10-02-batch-03.2
- **Statement:** When two cards are stacked in one cell, the system shall draw one row of `┈` in the frame tone between them; the open columns shall share the width left of the rail in proportion to their longest title, none narrower than `MIN_COL`, and when they do not all fit at `MIN_COL` the shown window shall follow the selected card as the shipped window does.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_301 or TC_304 or TC_305"`
- **Numeric pass threshold:** every rendered row is exactly the panel width at widths 24, 40, 60, 80, 100, 118, 160; between two cards of one cell exactly one `┈` row, none after a cell's last card; on the oracle board at 118 the widest-title column is wider than the narrowest (adaptive) and every open column ≥ `MIN_COL`; a board with 8 phases at width 80 shows a window holding the selected card's phase; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** cards in a column read as separate cards; a column of long titles gets more room.
  - **Shipped surface:** `TaskboardApp` key `4`.
  - **Acceptance test(s):** AT-301
  - **Boundary catalog (QC-3):** ☑ boundary (one card in a cell; an empty column; 8 phases at 80) ☑ empty (an empty board) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base tree draws no `┈` and equal columns → RED.

### HLR-303 — Each group is named once, by a band rule across the board
- **Traceability:** US-302
- **Ledger:** LED-2026-10-02-batch-03.3, LED-2026-10-02-batch-03.19
- **Statement:** When the grouped kanban draws a group, the system shall open its band with one band rule across the full panel width — `▐`, the group's name in its hue, its open count and, for a project, the number of its highs lifted into the high band (`N high ↑`), `at risk` when the project is at risk and its due date — and shall draw no per-column group header.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_302 or TC_306"`
- **Numeric pass threshold:** oracle board, unwindowed render: exactly one band rule per project with cards (5), each naming the project once, 0 `▐` inside card cells (the AT counts the rules drawn in the panel, the TC all five); Website Redesign's rule reads `5 open · 2 high ↑ · project due +10d`, API Platform's carries `at risk` (a status the oracle board sets in memory; the shipped model's `PROJECT_STATUSES` holds no `at_risk` and `Project.from_dict` maps it to `on_track`, so through the app the fact cannot appear — D-315, an operator question); under group modes `priority` and `horizon` one rule per non-empty group; the rule's `┼` fall under the column separators past its text; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** each project is named once, with its state, across the board.
  - **Shipped surface:** `TaskboardApp` keys `4`, `g` (to `horizon`: band rules Overdue/This week/…/Done), `v`.
  - **Acceptance test(s):** AT-302
  - **Boundary catalog (QC-3):** ☑ boundary (a project due today, late, in 3 days; a project name with `[b]` brackets; Inbox) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base draws 18 project-header cells → RED (P-1).

### HLR-304 — The last phase is a narrow rail
- **Traceability:** US-302
- **Ledger:** LED-2026-10-02-batch-03.4, LED-2026-10-02-batch-03.12
- **Statement:** The grouped kanban shall draw the board's last phase as a rail right of the open columns: at a panel width of 100 or more, 16 cells holding each band's done tasks most recent first as `✓ title` over `done Nd ago`, as many as the band's rows hold, the rest counted as `+N more`; below 100, 7 cells holding the band's `✓N` and the most recent one's `Nd ago`; with the last phase collapsed (`z`), the narrow form at every width. A done task shall be selectable exactly when its title is drawn.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_302 or TC_307"`
- **Numeric pass threshold:** oracle board at 118×30: the rail head reads `✓ DONE 3`, Website's rail cell `✓ Design homepa…` over `done 18d ago`; at 80×24 the head `✓3` and Website's cell `✓1` over `18d ago`; unwindowed (h 0), nav's last column equals the drawn done ids in draw order at 118 and holds no done id at 80 or when collapsed; a band with 1 card and 3 done tasks shows 1 done title and `+2 more`; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** finished work takes a narrow strip; open work gets the width.
  - **Shipped surface:** `TaskboardApp` keys `4`, `z`, `right`.
  - **Acceptance test(s):** AT-302
  - **Boundary catalog (QC-3):** ☑ boundary (width 99 vs 100; more done tasks than rows; a done task with no phase stamp) ☑ empty (no done task) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base draws Done as a full-width column → RED.

### HLR-305 — Open high cards ride one band on top of the board
- **Traceability:** US-303
- **Ledger:** LED-2026-10-02-batch-03.5, LED-2026-10-02-batch-03.11
- **Statement:** When the group mode is not `priority`, the grouped kanban shall draw, above every other band, one high band holding each open column's open high cards as `kanban_order(..., band=True)` lifts them, opened by the rule `── high  N open · P projects` counting the cards it draws, each card naming its project in the project's hue on row 2 when the row has room for it after the title's rest and the due token (the shortest run of leading words that tells it from the board's other projects); those cards shall not be drawn again in their project bands; the arrow-key order of every column shall be its cards' top-to-bottom draw order.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_303 or TC_308 or TC_301"`
- **Numeric pass threshold:** oracle board at 118×30: the high band is the first band, holds exactly the 9 open highs (P-2) above every project band, its rule reads `9 open · 4 projects` (counts of the cards drawn in the band); at 118×30 the tags drawn are the ones `out/R-1b-118x30.txt` draws (8 of 9; `to1`'s row 2 has no room), each in its project hue, and at 80×24 a tag is drawn exactly when LLR-301.2's shed order (age, tag, `⛓N`, due — from the left) leaves room for it; `!` raising a normal card to high moves it into the band with the cursor; `g` to `priority` draws no high band and `s` reorders the band as the seat orders its group; over every group × sort × focus × show_archived, unwindowed (h 0), the nav columns equal the line-map draw order and name exactly the drawn cards (LLR-301.1 states the windowed form); group `priority` draws no high band; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the urgent cards are the first thing on the board, and the cursor walks them first.
  - **Shipped surface:** `TaskboardApp` keys `4`, `down`, `up`, `!` (priority cycle), `g`, `s`.
  - **Acceptance test(s):** AT-303
  - **Boundary catalog (QC-3):** ☑ boundary (a blocked high; an archived high with `v`; a project focus; an Inbox high) ☑ empty (no open high: no band) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base draws a `── high` divider per column → RED (P-1).

### HLR-306 — The high band takes at most two thirds of the body
- **Traceability:** US-303
- **Ledger:** LED-2026-10-02-batch-03.6, LED-2026-10-02-batch-03.16
- **Statement:** When the panel height `h` is known, the high band's card rows in each column shall not exceed `R = max(5, 2·(h − 3) // 3)`; a column whose open highs need more rows shall draw as many as fit with one `+N more ↓` row under them, and its other N open highs shall be drawn in their own project bands, where they stay selectable.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_304 or TC_309"`
- **Numeric pass threshold:** oracle board (Backlog holds 4 highs, 11 rows) at panels 118×30, 80×24 and 80×22: no `more ↓` row (R = 18, 14, 12 — the approved frames unchanged); at panel 80×19 (R = 10) Backlog caps: 3 highs, `+1 more ↓`, `to5` drawn in the Ops & Security band; a board with 14 open highs in Backlog at panel 118×30 (R = 18): 6 highs in the band, `+8 more ↓`, the other 8 drawn in their project bands and present in nav; at 80×24 (R = 14): 4 and `+10 more ↓`; height 0 (unknown) draws all 14; every column's band rows ≤ R; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a board full of highs still shows its projects; the band says how many it is not showing.
  - **Shipped surface:** `TaskboardApp` keys `4`, `down`.
  - **Acceptance test(s):** AT-304
  - **Boundary catalog (QC-3):** ☑ boundary (exactly R rows needed; R + 1; R at its floor 5) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** an uncapped band draws all 14 highs (41 rows) → RED.

### HLR-307 — The new marks keep the colour budget
- **Traceability:** US-301, US-302, US-303
- **Ledger:** LED-2026-10-02-batch-03.7
- **Statement:** The grouped kanban shall paint no accent (focus and today only — the kanban draws neither as accent), shall paint relative and project due dates one to seven days ahead and today in `soon` and late ones in `over`, the `┈` separators and rules in `frame`, the meta strip in `mut`/`dim` except the due token, and shall show the selection in reverse video.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_305"`
- **Numeric pass threshold:** oracle board at 118×30 and 80×24 with the selection on `to3` (so the Ops & Security band and its `project due +5d` are drawn): 0 accent runs (a regression PIN — true on base too); the selected title's cells reverse (PIN); every `+1d`..`+7d`/`today` token `#fbbf24` (≥ 1 asserted), every `-Nd` `#f43f5e`; Ops & Security's `project due +5d` `#fbbf24`; every `┈` cell `#334154` (gate arms: the project due tone and the separators); 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** teal stays off the kanban; amber still means "soon".
  - **Shipped surface:** `TaskboardApp` key `4`.
  - **Acceptance test(s):** AT-305
  - **Boundary catalog (QC-3):** ☑ boundary (+7 vs +8 days; due today) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** an accent-painted title or a `mut` +4d token → RED.

### HLR-308 — The help and the legend describe the new board
- **Traceability:** US-301, US-302, US-303
- **Ledger:** LED-2026-10-02-batch-03.8
- **Statement:** The kanban help shall describe the band rules, the `┈` separators, the rail, the high band on top and its `+N more ↓` row, and shall no longer describe a per-column `── high ──` band; the legend shall call `▐` the project's band; every help bullet shall fit its 44-cell column.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_306 or TC_310"`
- **Numeric pass threshold:** `help_usage("kanban")` holds `band rule`, `┈`, `rail`, `more ↓` (each absent from the base copy), and not `top of each column`; every bullet ≤ 44 cells; the legend's `▐` entry reads `project band, by colour`; through the app `?` in the kanban paints those words; 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `?` explains what the board draws now.
  - **Shipped surface:** `TaskboardApp` keys `4`, `?`.
  - **Acceptance test(s):** AT-306
  - **Boundary catalog (QC-3):** ☑ boundary (the 44-cell column) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base help says "the top of each column" → RED.

### HLR-309 — The board fits the panel and names what it folds
- **Traceability:** US-302, US-303
- **Ledger:** LED-2026-10-02-batch-03.9, LED-2026-10-02-batch-03.14, LED-2026-10-02-batch-03.18
- **Statement:** When the panel height is known and the project bands do not all fit under the head and the high band, the grouped kanban shall draw whole bands only — from the earliest band that still lets the band holding the selected card be drawn, then as many bands below as fit — and a last row naming the hidden bands with their open counts, `▲ N above: …` and `▼ M below: …` for each side that folds, the count of every folded side always printed; a band taller than the room left shall be drawn alone and cut to the room on card boundaries around the selected card, the last row also counting that band's cards above and below the cut (`▲ k more in NAME`, `▼ m more in NAME`), so that the board is never taller than the panel while a whole card fits.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_307 or TC_311"`
- **Numeric pass threshold:** oracle board, selection `tw3`: at panel 118×30 the render is exactly 30 rows and its last row reads `▼ 2 below: Data Warehouse (4 open), Ops & Security (5 open)` (the approved frame, `out/R-1b-118x30.txt`); selecting `to3` (Ops & Security) draws its band and names the bands above; through the app at terminals 118×30 and 80×24, after every `down` from the first Backlog card to the column's last card, both rows of the selected card and its band rule are inside the viewport, and a `down` into a band already drawn leaves the drawn band set unchanged (UX-14); at panel 80×24 with bands folded on both sides, the fold row prints both `▲ N above` and `▼ M below` (UX-15); the same walk under `g g` (horizon) at terminal 80×24 and on a board of 14 highs at terminals 118×30 and 80×24: the panel never scrolls (the head and the fold row stay on screen) and the selected card is whole (P4 UXV3-1); height 0 draws every band and no fold row; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the board never hides a project silently; the card under the cursor is always fully on screen with the name of its band.
  - **Shipped surface:** `TaskboardApp` keys `4`, `down`, `up`.
  - **Acceptance test(s):** AT-307
  - **Boundary catalog (QC-3):** ☑ boundary (exactly fits; one band taller than the room; the selection in the high band) ☑ empty (no project band) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** an unwindowed render at 118×30 is taller than the panel and names nothing → RED; a band taller than the room drawn whole scrolls the head, the card's row 2 and the fold row out → RED (P4 UXV3-1).

### HLR-310 — The cursor never rests on a done task the board does not draw
- **Traceability:** US-302
- **Ledger:** LED-2026-10-02-batch-03.10, LED-2026-10-02-batch-03.15
- **Statement:** When the selected task is not drawn by the grouped kanban — it reached the last phase while the rail shows counts (below 100 cells, or collapsed) or past the rail's `+N more` — the selection shall move — after a `]`, to the card that took the moved card's place in its column, else the card above it; otherwise (a resize, `z`, a refresh) to the first card of the last non-empty column at or left of its phase (the `z` rule) — and a `]` that caused it shall post the notification `‹title› done · counted in the ✓ rail · u undo` with markup off.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_readable.py -k "AT_308 or TC_312"`
- **Numeric pass threshold:** oracle board at terminal 80×24: selecting `to3` (Review, Ops & Security) and pressing `]` leaves the selection on `SDK regeneration` (`ta6`, the Review card above it — `to3` is the column's last), drawn (in `line_map`), and posts one notification naming `Review pull requests` literally; a title `[b]x[/b]` prints literally; at terminal 118×30 the same `]` keeps the selection on the rail title (no move, no notification); `u` restores the task to Review; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** finishing a card at a narrow width says where it went, and the cursor stays on something visible.
  - **Shipped surface:** `TaskboardApp` keys `4`, `]`, `u`.
  - **Acceptance test(s):** AT-308
  - **Boundary catalog (QC-3):** ☑ boundary (99 / 100 cells; collapsed at 118) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base app keeps the selection on the undrawn task with no notification → RED.

## 4. Low-level requirements (LLR)

### LLR-301.1 — The plan seat
- **Traceability:** HLR-301, HLR-303, HLR-304, HLR-305
- **Ledger:** none
- **Statement:** A function `kanban_plan` (NEW, `taskboard/views.py`) shall compute, from the board, `show_archived`, the selected id, today, the panel width and height and the four kanban modes, the open columns' window and widths, the rail's width and form, the high band's shown and overflow cards per column, and each band's group, cards per column and rail tasks — through `kanban_order` only; `_kanban_grouped` and the grouped branch of `nav_model` shall both read it, and nav shall return one column per open phase plus the rail when its titles are drawn, each holding the cards the board draws when nothing is windowed — so a card in a hidden phase or a folded band is reachable, and the window then follows it (the shipped phase-window rule); the selected card is always drawn.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_301"` (TC-301)
- **Numeric pass threshold:** over `_KANBAN_GROUP_MODES` × `_KANBAN_SORT_MODES` × focus {off, on} × show_archived {off, on} (60 arms, derived from the seat's tuples, asserted `== 60`), on a board guarded to hold archived open and done tasks, Inbox tasks and open highs in two projects (`any(...)` asserted), at 140×0 (unwindowed): nav ids = line-map ids and each nav column is sorted by line-map row; at 80×24, 140×14 (the cap) and an 8-phase board at 80×24: line-map ids ⊆ nav ids, the selection always drawn, the drawn part of each column in nav order; 0 failures.
- **Negative control:** nav built from `kanban_order(band=True)` per column (the shipped grouped nav) while the render draws the board-wide band → RED.
- **Boundary catalog:** ☑ boundary (collapsed; a project focus; a 1-phase board) ☑ empty (empty board) ☐ invalid — N/A ☐ error — N/A

### LLR-301.3 — The chrome as shipped
- **Traceability:** HLR-302, HLR-303
- **Ledger:** LED-2026-10-02-batch-03.13
- **Statement:** The grouped kanban shall keep the shipped chrome: the head row `KANBAN · grouped` naming every non-default sort, group and focus mode with the task count (LLR-003.2 / R-08 of earlier batches), the phase row whose cells end with the WIP tag (HLR-005), `◀ N` / `N ▶` markers counting hidden open phases, the `┼` rule under it (three head rows in all), and the empty-board line `(no tasks — press 'a' to add one)`; the rail's head cell takes the last phase's place in the phase row.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_313"` (TC-313)
- **Numeric pass threshold:** the head names `sort: due`, `group: horizon`, `focus: <name>` when set; the WIP tag `6/4` in `over`; an 8-phase board at width 80 shows `◀`/`▶` counts over the open phases only (the rail is never counted hidden); the shipped nodes `test_kanban_wip_header_*` and `test_kanban_windows_phases_when_they_dont_fit` keep their laws (re-pointed, census); 0 failures.
- **Negative control:** the window markers counting the rail's phase as hidden → RED on the 8-phase arm.
- **Boundary catalog:** ☑ boundary (8 phases at 80; a 1-phase board) ☑ empty (empty board) ☐ invalid — N/A ☐ error — N/A

### LLR-301.2 — The two-row card
- **Traceability:** HLR-301
- **Ledger:** LED-2026-10-02-batch-03.20
- **Statement:** A function `kanban_card` (NEW) shall return `(row1, row2)` markup of exactly `wc` cells each for every `wc ≥ 0`: row 1 = `▲ ` (`over`) for a blocked card else `▊ ` (project hue), the `PRIORITY_BADGE` and one space for an open card when `wc ≥ 9`, then the title's head cut on a word boundary at the remaining width (a first word wider than it is cut with `…`); row 2 = `▊` (project hue), then, when the title has a rest, one space, the badge's indent and the rest cut to leave room for the last meta token, followed by the meta tokens that fit; the meta tokens in order: `↗` `mut` (a valid URL), `▤` `mut` (images), `·Nd` `dim` (open, known stamp), the project tag (high band only), `⛓N` `mut`, the `reldue_token(include_done=True)` token unless archived, `ARCHIVED_MARK` `ash` when archived; title text escaped, linked to its first valid URL, reverse when selected.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_302 or TC_303"` (TC-302, TC-303)
- **Numeric pass threshold:** every task of the oracle board plus a 58-char title, a 24-char single word, the hostile titles `[b]x[/b] [link=http://e]y`, `a [ b c`, `x\ y\`, `\[b]z`, `aaa [/link]` (a closing tag on row 2), each with and without a URL, plus a wide-character title (`日本語 レビュー 🚀 launch`), at `wc` 0..40: both rows exactly `wc` cells, the plain text holds the title's pieces literally; `Beta release to testers` at `wc` 24: row 1 `▊ == Beta release to`, row 2 `▊    testers ·15d +35d` (the frame `out/R-1b-118x30.txt` rows 20–21, `tm5`: normal, 15 days in phase, due +35d, no dependant, no URL); the due token survives every shed (any `wc` ≥ 9 with a due date); 0 failures.
- **Negative control:** a meta order with `⛓N` after the due token sheds the due first at `wc` 14 → RED.
- **Boundary catalog:** ☑ boundary (wc 0, 1, 2, 8, 9) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-302.1 — Separators and widths
- **Traceability:** HLR-302
- **Ledger:** LED-2026-10-02-batch-03.17
- **Statement:** The cell builder shall put one `┈`×`wc` row (`frame`) between consecutive cards of a cell; the widths shall be `room · d_i // Σd` with `d_i = max(MIN_COL, longest card title in the column + 5)` and `room` the open columns' cells, the remainder one cell each to the widest-desired columns first (ties left first) — the approved frames' rule; when that leaves a column under `MIN_COL`, every column gets `MIN_COL` and the rest `room − k·MIN_COL` is split the same way by `d_i − MIN_COL`; the window, when the open columns do not fit at `MIN_COL`, shall be the shipped `_phase_window` rule over the open phases.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_304 or TC_305"` (TC-304, TC-305)
- **Numeric pass threshold:** as HLR-302, plus: widths sum to the room exactly at every width 24..160.
- **Negative control:** equal widths (`distribute`) → the adaptive arm RED.
- **Boundary catalog:** ☑ boundary (room < k·MIN_COL; every column empty) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-303.1 — The band rule
- **Traceability:** HLR-303
- **Ledger:** none
- **Statement:** The band rule shall be laid left to right and clipped at the panel width: `▐ ` and the group's name bold in its hue (escaped), `  N open` (`mut`, the group's non-archived cards in the open columns, lifted highs included), for a project ` · K high ↑` (`mut`, K > 0 of its highs drawn in the high band), ` · at risk` (`over`), ` · project ` + `Nd late` (`over`) / `due today` (`soon`) / `due +Nd` (`soon` when N ≤ 7, else `dim`); then one space and `─` (`frame`) to the width with `┼` at every column separator past the text. The high band's rule: `── ` (`frame`), `high` bold `ink`, `  N open · P project(s)` (`mut`, N the cards it draws, P their projects).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_306"` (TC-306)
- **Numeric pass threshold:** as HLR-303; a project named `[b]Odd[/b]` prints literally; every rule exactly `w` cells at widths 24..160.
- **Negative control:** a `┼` laid at a separator inside the text → RED.
- **Boundary catalog:** ☑ boundary (text longer than `w`; project due ±0, 7, 8 days) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-304.1 — The rail
- **Traceability:** HLR-304
- **Ledger:** none
- **Statement:** The rail's width shall be 16 when the panel width ≥ 100 and the last phase is not collapsed, else 7 (`KANBAN_RAIL_WIDE` / `KANBAN_RAIL_NARROW`, NEW); its head `✓ <LAST PHASE> N` (wide) or `✓N` (narrow), bold `done`; per band, wide and not collapsed: the band's done tasks by `_recent_first`, each `✓ ` (`done`) + title (`mut`, escaped, reverse when selected) over `  done Nd ago` (`dim`, blank when the stamp is unknown); when they need more rows than `max(open rows, 3)` the rail draws `(cap − 1) // 2` of them and `  +N more` (`mut`); narrow or collapsed: `✓N` (`done`) over `Nd ago` (`dim`) of the most recent.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_307"` (TC-307)
- **Truth table (group mode × rail form):** every group mode uses the same rail rules — wide titled when width ≥ 100 and not collapsed, else the count; under `horizon` the done tasks form the `Done` band, whose open cells are empty, so its rail shows `(3 − 1) // 2 = 1` title and `+N more` when it holds more than one.
- **Numeric pass threshold:** as HLR-304, plus a done task titled `[/b]x [link=http://e]y` prints literally and the row stays 16 cells.
- **Negative control:** the rail drawn at 100 in its narrow form (`> 100`) → RED at width 100.
- **Boundary catalog:** ☑ boundary (99 / 100; cap 3) ☑ empty (no done) ☐ invalid — N/A ☐ error — N/A

### LLR-305.1 — The high band
- **Traceability:** HLR-305
- **Ledger:** none
- **Statement:** For each open column, the high band's cards shall be the `KANBAN_BAND` group of `kanban_order(bucket, …, band=True)`; the project bands shall be built from `kanban_order(bucket minus the band's shown cards, …, band=False)`, the bands ordered as the seat orders the groups of the whole board; each high card's project tag shall be the shortest run of leading words of its project's name that is not the leading words of any other visible project's name (word-wise: `API` is not taken by `APIx`; the whole name when none is shorter; `Inbox` with no project), escaped, in `project_color`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_308"` (TC-308)
- **Numeric pass threshold:** as HLR-305; the band's per-column order equals the shipped `KANBAN_BAND` group's order under every sort mode; projects `API Platform` and `API Gateway` tag `API Platform` / `API Gateway`; a project named `[b]Odd[/b] Co` tags `[b]Odd[/b]` literally.
- **Negative control:** project bands built without removing the shown highs → a high drawn twice → RED.
- **Boundary catalog:** ☑ boundary (group `priority`; `horizon`) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-306.1 — The cap
- **Traceability:** HLR-306
- **Ledger:** none
- **Statement:** With `h > 0`, the high band's room shall be `R = max(5, 2·(h − 3) // 3)`; a column with `m` open highs shall show all when `3m − 1 ≤ R`, else `K = R // 3` of them (seat order) and one `+(m − K) more ↓` row (`mut`) directly under the last one, with no `┈` before it (`3K ≤ R` rows); the overflow cards return to the `band=False` grouping of their column; with `h = 0` every high is shown.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_309"` (TC-309)
- **Numeric pass threshold:** as HLR-306; executed table over h ∈ {0, 11, 12, 13, 14, 19, 20, 22, 24, 30} (R = –, 5, 6, 6, 7, 10, 11, 12, 14, 18 — the floor 5 at h 11; K for 14 highs = 14, 1, 2, 2, 2, 3, 3, 4, 4, 6; the oracle Backlog's 4 highs cap at h ≤ 19 and fit from h = 20); boundary `3m − 1 = R` shows all, `R + 1` caps.
- **Truth table (C-36 rider):**

  | Count | Shown highs | Overflow highs |
  |---|---|---|
  | high rule `N open · P projects` | counted | not counted |
  | project band `K high ↑` | counted | not counted |
  | project band `N open` | counted | counted (drawn in the band) |
  | column `+N more ↓` | — | counted |
- **Negative control:** `K = R // 3 + 1` → the band exceeds R → RED.
- **Boundary catalog:** ☑ boundary (h 0; h 11, the floor R = 5; h 19 / 20, the oracle Backlog capped / not) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-308.1 — Help and legend copy
- **Traceability:** HLR-308
- **Ledger:** none
- **Statement:** `help_usage("kanban")` shall describe the band rule, `┈`, the rail, the high band and `+N more ↓`; `help_example("kanban")` shall show a card's meta order (`⛓N` before the due token); `legend_entries("kanban")` shall label `▐` `project band, by colour`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_310"` (TC-310)
- **Numeric pass threshold:** as HLR-308.
- **Negative control:** base copy → RED.
- **Boundary catalog:** ☑ boundary (44 cells) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-309.1 — Band windowing and the fold row
- **Traceability:** HLR-309
- **Ledger:** none
- **Statement:** With `h > 0`, when the head, the high band and every band exceed `h` rows, `_kanban_grouped` shall, with `room = h − head − high band − 1` and `s` the band holding the selection (the first band when the selection is in the high band or absent), start at the smallest band index `i ≤ s` whose bands `i..s` fit `room` (`s` itself when band `s` alone does not), then add bands below `s` while they fit; the last row shall be `▲ N above: name (k open), …` then three spaces and `▼ M below: …` (`mut`, names escaped, `k` the band rule's open count), pinned to the panel's bottom; when it does not fit `w`, the `▲` side keeps only `▲ N above` and the `▼` side is clipped after its count, so both counts always print.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_311"` (TC-311)
- **Numeric pass threshold:** as HLR-309, plus: with every task of the oracle board as the selection at panels 118×30 and 80×24, the selection's card is drawn and the render is exactly `h` rows; a project named `[b]Odd[/b]` hidden below prints literally.
- **Negative control:** windowing around the first band always (ignoring the selection) → `to3` undrawn → RED; the prototype's selection-first rule → the UX-14 arm RED.
- **Boundary catalog:** ☑ boundary (a band taller than the room; h 0) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-309.2 — A band taller than the room is cut
- **Traceability:** HLR-309
- **Ledger:** LED-2026-10-02-batch-03.18, LED-2026-10-02-batch-03.21
- **Statement:** With `h > 0` and `room = h − head − high band − 1 ≥ 3`, when the window holds one band whose rows exceed `room` (`room + 1` when every band is kept, the fold row's line being free then), `_kanban_grouped` shall draw its rule and the largest number of WHOLE card rows that fits (`3j + 2` rows: cards sit every 3 rows), starting at the smallest card boundary that keeps both rows of the selected card — and no later than the selected row itself (a rail title sits every 2 rows) — (the first rows when the selection is outside the band); the fold row shall add `▲ k more in NAME` / `▼ m more in NAME`, k and m the band's OPEN cards (not its rail titles) wholly above and below the cut, and shall be drawn whenever a cut happened; every count shall print: when the row does not fit, the `▲` names go first, then — if even the bare counts overflow — the cut band's name, and only then is the `▼` list clipped. Below a room of 6 rows (3–5: one card) a rail-title selection may show a card's first row alone — a declared boundary (code review F11 of increment 003).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "taller_than or keeps_every_count"` (TC-311)
- **Numeric pass threshold:** oracle board, group `horizon`, panel 80×22: `td3` → 22 rows, `▲ 3 more in Later` and `▼ 1 more in Later`; `td5` → `▲ 5 more in Later`; h 0 → nothing cut, 25 cards drawn; a single band exactly the panel's height is not cut, one row less is; with the cut band last and with a 34-character band name between folded bands every count prints; no lone first row at a cut's bottom (80×24, 80×23, 118×22); with rail titles selected the cut still starts on a card's first row; the counts plus the drawn cards equal the band's open cards; AT-307's horizon and 14-high arms (code review round 1 of increment 003: F1, F2, F3, F5).
- **Negative control:** the cut off → the render 25+ rows at h 22 → RED.
- **Boundary catalog:** ☑ boundary (room < 3: drawn alone, the panel scrolls — declared) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-310.1 — Relocation and the done notification
- **Traceability:** HLR-310
- **Ledger:** none
- **Statement:** `TaskboardApp.action_phase_move` (`taskboard/app.py`) shall, in the kanban's grouped presentation, note the moved task's nav column and row before the move and, when the task is absent from the nav columns after it, select that column's card at the same row (the one that took its place), else the row above, and notify; `_select_first` shall move any other visible selection absent from the nav columns to the first card of the last non-empty nav column at or left of its phase (the `z` rule); the notification is `f"{title} done · counted in the ✓ rail · u undo"` with `markup=False`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_readable.py -k "TC_312"` (TC-312)
- **Numeric pass threshold:** as HLR-310.
- **Negative control:** relocation off → the selection is a task absent from `line_map` → RED.
- **Boundary catalog:** ☑ boundary (collapsed; a capped rail) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

## 4b. Information Flow Contract (IFC)

Part A always. Part B: the kanban panel's rows are addressed by row index (`line_map`) and its
cards by nav column position; this batch changes both for the grouped presentation.

```
FLOW: readable kanban
  SOURCE : Board + show_archived + selected_id + today + panel size + kanban modes (sort, group, collapsed, focus)
  NODES  :
    - fn    : kanban_order
      owner : LLR-305.1
      in    : one column's tasks, modes, band flag
      out   : ordered groups (the high band first when asked)
    - fn    : kanban_plan
      owner : LLR-301.1
      in    : board, modes, selected_id, width, height
      out   : window, widths, rail form, high band (shown, overflow), bands
    - fn    : kanban_card
      owner : LLR-301.2
      in    : task, cell width, selected, tag
      out   : two rows of markup
    - fn    : the cell builder and widths
      owner : LLR-302.1
      in    : a cell's cards, widths
      out   : cell rows with separators
    - fn    : the band rule
      owner : LLR-303.1
      in    : group facts, separator positions, width
      out   : one rule row
    - fn    : the rail
      owner : LLR-304.1
      in    : a band's done tasks, rows, width, collapsed
      out   : rail cells
    - fn    : the high band cap
      owner : LLR-306.1
      in    : column highs, panel height
      out   : shown, overflow count
    - fn    : header, _windowed_header (the chrome)
      owner : LLR-301.3
      in    : modes, phases, the window, the visible tasks
      out   : the head row, the phase row with WIP tags and window markers, the rule
    - fn    : _kanban_grouped
      owner : LLR-301.1
      in    : the plan
      out   : rows + line_map
    - fn    : nav_model (kanban, grouped)
      owner : LLR-301.1
      in    : the plan
      out   : arrow-key columns
    - fn    : the band window and fold row
      owner : LLR-309.1
      in    : bands, their heights, the selection, the panel height
      out   : the drawn bands, the fold row
    - fn    : the band cut
      owner : LLR-309.2
      in    : the one band drawn, the selection, the room
      out   : the band's rows around the selection, the in-band fold counts
    - fn    : TaskboardApp._select_first / action_phase_move (kanban)
      owner : LLR-310.1
      in    : the selection, the nav columns
      out   : a drawn selection, the done notification
    - fn    : help_usage / help_example / legend_entries (kanban)
      owner : LLR-308.1
      in    : view mode, board
      out   : help and legend copy
  SINK   : the painted kanban panel and the cursor
```

```
COMPONENT: kanban-grouped-body
  PARENT : SYSTEM
  SURFACE: kanban view (key 4), grouped presentation
  INPUTS : board: Board ; selected_id: str ; width: int ; height: int ; kanban modes
  OUTPUTS:
    - id          : card-rows
      value       : row 1 of each drawn card; separators, band rules, rail rows are not addressed
      address     : line_map[task_id] = row index in the rendered Text
      cardinality : drawn cards (open columns and rail titles)
      consumers   : taskboard/app.py::_scroll_selected_into_view ; taskboard/views.py::render_view
      owner       : LLR-301.1
    - id          : nav-columns
      value       : one list of task ids per open phase, then the rail when drawn, each in draw order
      address     : the nav model's return value for the kanban's grouped presentation, INDEXED POSITIONALLY
      cardinality : open phases (+1 when the rail titles are drawn)
      consumers   : taskboard/app.py::_nav_columns
      owner       : LLR-301.1
```

## 5. Validation strategy
Layer A (`TC-301`..`TC-313`) and Layer B (`AT-301`..`AT-308`, one node each — C-18) are pytest
nodes in `tests/test_kanban_readable.py` (NEW — created in Phase 3; node ids provisional until
P3, V-5), each carrying its id in its docstring. ATs drive `TaskboardApp` through
`App.run_test()` at terminal sizes; TCs drive `render_kanban`, `nav_model` and the helpers at
panel sizes. Existing nodes that pin the grouped kanban (`tests/test_kanban_priority.py` and the
others the reverse census finds) are rewritten in place or retired with a reason, per increment.
Captures (SVG + text) of the kanban at panels 118×30 and 80×24 come from the oracle board only,
into `evidence/captures/`; the readability table before/after is `evidence/readability-*.txt`.
Full suite `python -m pytest -q -p no:cacheprovider` at close.

| AT | Story | Drives |
|---|---|---|
| AT-301 | US-301 | key `4` at terminals 118×32, 80×26 and 80×24: two-row cards, `┈`, adaptive widths, readability ≥ threshold |
| AT-302 | US-302 | keys `4`, `z`, `right`, `g` (horizon), `v`: one band rule per group; the rail at 118 and 80; collapse |
| AT-303 | US-303 | keys `4`, `down`, `!`, `g` (priority), `s`: the high band first, project tags, the walk in draw order |
| AT-304 | US-303 | key `4`, `down` on a 14-high board at terminal 118×32: the cap, `+8 more ↓`, overflow reachable |
| AT-305 | US-301..303 | key `4`: no accent painted, soon amber, selection reverse |
| AT-306 | US-301..303 | keys `4`, `?`: the help describes the new board |
| AT-307 | US-302, US-303 | keys `4`, `down` at terminals 118×30 and 80×24 (and `g g` at 80×24; a 14-high board at both): whole bands or a cut band, the fold row and the head on screen, the selected card fully in view |
| AT-308 | US-302 | keys `4`, `]`, `u` at terminals 80×24 and 118×30: the selection stays drawn, the notification |

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion shown RED on the base tree or by a recorded mutation.
- each existing node the batch changes is listed in its increment's reverse census with its disposition.
- `tab` still cycles grouped → matrix → lanes and matrix/lanes render unchanged (their nodes stay green).
- full suite: 0 failures.

## 6. Appendices

### 6.1 Verification beyond automation
- expert inspection: ux-reviewer walkthrough on the captures and the app at P4 — `planned`.
- user evaluation: the operator reads the captures before the push — `planned` (outside the batch).

### 6.2 Relevant design decisions
- D-301: **Replace**, not coexist: the grouped presentation's body becomes the readable board; `tab` still cycles grouped → matrix → lanes (P-4) and the presentation keeps its name. Reasons: the verdict made K-A *the* kanban ("K-A first, then K-B as an extra `tab` presentation"); one grouped renderer keeps one nav seat (the F-3 law); a fourth presentation would keep the per-column band the operator replaced. Cost: the grouped nodes of `test_kanban_priority.py` (HLR-003's per-column band) and others are rewritten or retired — reverse census per increment (B1).
- D-302: Whole bands are windowed around the selection with the `▲ N above / ▼ M below` fold row, as in the approved frame (P2 UX-1: the frame settles it, and dropping the cue would hide Ops & Security, the only task due today, silently); the frame's selected-card detail line, drawn there when nothing is folded, is not drawn (not in the commission). Provisional visual decision PV-1 (no detail line).
- D-303: The cap is two thirds of the body: `R = max(5, 2·(h − 3) // 3)` rows — chosen so the approved frames stay uncapped at both sizes and at terminal 80×24 (the oracle Backlog's 4 highs need 11 rows ≤ 18 / 14 / 12; a half-body cap capped the approved 80×24 frame, P2 qa N-1) while a third of the body is always left to the project bands; overflow cards stay reachable in their project bands (the alternative, hiding them, would leave cards no key reaches). The row reads `+N more ↓`. Provisional visual decision PV-2.
- D-304: The rail lists done tasks most recent first (the prototype's order), not by the sort mode: `done Nd ago` is what it is for and the cap keeps the newest. Sort modes keep ordering the open columns.
- D-305: Below 100 cells (and when collapsed) done tasks are a count, so they are not selectable there — nav walks what is drawn (F-3); a selection that lands there moves by the `z` rule and `]` says so (HLR-310, the gantt's D14 precedent; P2 UX-2). They stay reachable at ≥ 100 cells and in the agenda. Provisional visual decision PV-3.
- D-306: The spine stays the shipped `▊` (project hue) / `▲` (blocked, row 1 only); the prototype's age-thickness ramp (`▏▎▍▌▊`) is not taken — it repeats the `·Nd` token and is not in the commission. Provisional visual decision PV-4.
- D-307: The project tag on a high card is the project name's first word, as in the oracle frame (`Website`, `API`, `Ops`), extended word by word only when another project shares it (P2 UX-8). Provisional visual decision PV-5.
- D-308: The meta strip keeps the age token at every width and sheds it first under pressure (the prototype dropped age below 100 cells by rule). Provisional visual decision PV-6.
- D-309: The `▐` group rows of the other group modes become band rules too (High/Normal/Low; Overdue/This week/Later/No date/Done), facts limited to the open count and `K high ↑`. Provisional visual decision PV-7 (captures of `g` → priority and horizon).
- D-314: The band window starts at the earliest band that keeps the selection's band drawn (P2 UX-14: the prototype's selection-first rule re-flowed the board on a `down` into a band already on screen); it gives the approved frame for the oracle selection. The fold row always prints both counts (UX-15). After `]` the cursor takes the card that took the moved card's place (UX-13, the gantt's neighbour precedent), not the top of the column.
- D-311: The high band's counts and `K high ↑` count the cards drawn in the band; overflow highs are counted by their column's `+N more ↓` (P2 UX-6).
- D-312: Under a `/` filter the render is two rows shorter; the app asks the nav for the same height so the cap agrees (`app._nav_columns`, kanban only — the gantt's same latent gap goes to BACKLOG).
- D-313: This batch also supersedes, besides HLR-003/LLR-003.2 (the per-column band), the `✓ N` summary row of batch-04's HLR-007 (R-07; the narrow rail reads `✓N`) and qualifies the "the kanban shows every task" law: the rail counts done work below 100 cells and past `+N more`, and folded bands are named, not drawn — `test_kanban_shows_every_task_in_its_phase` still holds as written because it renders unwindowed at 160 cells (h 0), where every card and done title is drawn (P4 qa G-004). The canon rows are marked at close; the nodes are rewritten with reasons in the increments' censuses (P2 Q-9).
- D-314b: A band taller than the room is cut around the selection with in-band counts in the fold row (P4 UXV3-1; HLR-309 amended, LED .18) — the conservative reading that keeps the head and the fold row on screen; the alternative (clip without counts, or scroll) left projects hidden silently. Provisional visual decision PV-9.
- D-315: `at risk` cannot reach the screen through the app (P4 UXV3-2): the band rule keeps the fact for a status the model does not offer; whether to add the status, derive "at risk", or drop the fact is the operator's question (BACKLOG). The head row stays the shipped chrome (LLR-301.3), not the frame's `KANBAN · high on top … over WIP: …` — provisional visual decision PV-10 (P4 UXV3-7).
- D-310: Trigger family A is judged not fired: the `taskboard` package is one module (no module map exists), as batches 01/02 ruled (D-215); increment 002 also edits `app.py`, which consumes `nav_model` and `line_map` with their shipped signatures (re-judged at P2 iteration 2, qa N-3).

### 6.3 Open risks
- The grouped kanban is pinned by about 30 nodes (qa P2 census in `02-review.md`): `test_kanban_priority.py`, `test_app.py` (parity, groups, collapse, window, WIP), `test_gantt.py`, `test_vertical_fill.py`, `test_span_economy.py`, `test_prism_laws.py`, `test_cells.py`, `test_emoji_picker.py`, `test_palette_ration.py`, `test_legend.py` — rewritten or retired per increment, with reasons (D-313).
- A band taller than the panel is cut around the selection (HLR-309, LLR-309.2); below a room of 3 rows it is drawn alone and the panel scrolls (declared).
- `left`/`right` land on the next column's first card, which may re-window the bands (UX-11) — P4 walkthrough.
- `]` on a high card into a capped column sends it to its project band (UX-9) — P4 walkthrough on the 14-high board.

### 6.4 Security questions (scan `devflow-scan-spec.py`: `security_required: true`, flags `token`, `form` — `evidence/p1-security-scan.txt`)
- The two flags are vocabulary hits — "token" (the meta/due token), "form" (the rail's narrow form); the batch adds no credential, auth, network, storage or input surface.
- Real surfaces, answered: (1) **markup over file-derived text (C-17)** — the band rule prints project names and the high band prints their first word; titles are split and re-escaped: every piece is escaped after its width is measured; a bracket title and a bracket project name are hostile-input arms (TC-302, TC-306). (2) **existing BACKLOG L1** — control characters in titles and project names reach the terminal; this batch prints project names in two more places (the band rule, the tag); not widened here (P2 S-4). (3) **width math over user text** — no row holding escaped user text is measured with `vis(_strip(...))`; pieces are measured plain (P2 S-3, an increment review check). (4) **record hygiene** — captures come from `tests/kg_board.py` only; transcripts redact the home path; the privacy sweep runs over `evidence/` at close.

### 6.5 Requirement amendments (Before / After · Deleted / New)
- P4 iteration 1 → `iterate-to-refine` + `iterate-to-fix` (ux FAIL UXV3-1; qa PASS-WITH-NOTES, G-001/G-003a/G-004). HLR-309 **Before:** "a band taller than the room left shall be drawn alone and the panel shall scroll." **After:** "a band taller than the room left shall be drawn alone and cut to the room on card boundaries around the selected card, the last row also counting that band's cards above and below the cut (`▲ k more in NAME`, `▼ m more in NAME`), so that the board is never taller than the panel while a whole card fits." **Deleted:** the scroll. **New:** LLR-309.2; AT-307's horizon and 14-high arms; TC-311's cut node (LED .18). HLR-303's `at risk` annotated (D-315, LED .19). HLR-307's threshold names `to3` (P4 qa G-003b — `tw3` folds the Ops band); LLR-301.2's sample titles are 58 and 24 characters (G-003b). The shared `title_markup` seat writes through `_literal` since increment 001 — LLR-301.2's escaping now covers it, with a regression node per seat (P4 qa G-003a, LED .20). Parent stories re-read: unchanged (US-302 "spends its width on open work", US-303 "stays in view" — the cut serves both). Increment 003 owns them (C-21).
- P3 increment 001 (LED .17) — LLR-302.1 **Before:** "the widths shall be `MIN_COL + extra·(d_i − MIN_COL) // Σ(d − MIN_COL)` … an even split when every `d_i = MIN_COL`" **After:** the proportional rule above, with the `MIN_COL` floor as its fallback. **Deleted:** the floor-first split as the main rule. **New:** the fallback clause. Why: the floor-first split measured 5.3 chars at 80×24 (< the 5.5 floor) where the frame's proportional split measures 6.2 — executed, `evidence/inc001-widths.txt`. Parent HLR-302 re-read: unchanged ("in proportion to their longest title, none narrower than `MIN_COL`"). TC-305 re-derived on the new rule.
- P2 iteration 2 (qa FAIL — N-1 the cap capped the approved 80×24 frame; ux FAIL — UX-15 the fold row clipped the `▼` side): the cap → two thirds (LED .16, D-303); the window starts at the earliest band that keeps the selection drawn and the fold row keeps both counts (LED .14, D-314); after `]` the neighbour takes the cursor (LED .15); nav claims scoped to h 0 (N-2); §1.2 and D-310 re-judged (N-3); the tag cites the shed order and is asserted exactly (N-4, N-6); §5 updated (N-5); word-wise tags (N-7). Parent stories re-read: US-303 "never takes over the screen" holds (a third is always left). Increment plan unchanged (no AT added or split).
- P2 iteration 1 (qa FAIL — Q-1 tag rule, Q-2 phantom `+` key; ux and security PASS-WITH-NOTES; `02-review.md`) → `iterate-to-refine`, folded here. qa: the readability metric counts only drawn titles and the floors are re-measured (Q-3, LED .13); LLR-301.3 the chrome (Q-4, LED .13); nav across a window (Q-5); AT-302/303 drive `g`, `s`, `v`, `!` (Q-2, Q-7); the guarded 60-arm board and the capped arm (Q-8); D-313 supersessions (Q-9); the overflow row and the truth tables (Q-10, Q-11, Q-16); pins labelled (Q-12, Q-13); literals (Q-14, Q-18); wide characters (Q-17). **New:** HLR-309 / LLR-309.1 band windowing and the fold row (UX-1, LED .9); HLR-310 / LLR-310.1 relocation and the done notification (UX-2, LED .10); AT-307, AT-308; terminal 80×24 arms (UX-4); hostile arms (S-1, S-2). **Before → After:** D-302 "bands are not windowed and no `▼ N below` footer" → windowed with the fold row; HLR-305 "each card naming its project" → the shortest distinguishing word run, may shed at 80 (UX-5, UX-8, LED .11); counts → the cards drawn (UX-6, LED .11); LLR-304.1 the collapsed rail is 7 cells (LED .12). Parent stories re-read: unchanged. Increment plan re-cut (C-21).
