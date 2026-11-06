# Requirements — taskboard — Inc MR-a, a project's milestones share one row in the board's gantt (dev-flow-v3-beta)

> Strict EARS (five forms only), ISO/IEC/IEEE 29148. One `shall` per requirement. Each carries a
> numeric pass threshold and a negative control (*NC*: a mutant that turns its test RED). Ids: US-4601,
> HLR-4601..4606, LLR-4601.n..4606.n, AT-4601..4607. Range check (2026-11-06,
> `grep -rhoE "(HLR|LLR|AT|US)-46[0-9]{2}" REQUIREMENTS.md .dev-flow/ tests/`): no hit. `TC-46nn`/`TC-47nn`
> are taken (Inc K, Inc X), so this increment's TCs use `TC-48nn`.
> Base: `5a69634` (branch `feat/milestone-row`, from `main` `222403e`). Commission:
> `.dev-flow/COMMISSION-milestone-row.md` (verdict A, D2 `fila`, D3 `si`; MR-1..MR-3); split and rulings
> R-1..R-3 in `00-e1-rulings.md`. The presentation (D1) is Inc MR-b, not this one.
> **TC numbering:** LLR-4601.n → TC-(4800+n); LLR-4602.n → TC-(4810+n); LLR-4603.n → TC-(4820+n);
> LLR-4604.n → TC-(4830+n); LLR-4605.n → TC-(4840+n); LLR-4606.n → TC-(4850+n). A second test of one LLR
> adds a letter (TC-4803b). One exception: LLR-4603.11 → TC-4820, because TC-4831 is LLR-4604.1's
> (LED-2026-11-06-incMR.5).

## 1. Scope

**In:** the board's gantt view (`3`): each group's drawn milestones on one milestone row under its span row
(variant A); the marks, clash count, labels, label column and chip of that row; `↑↓` stopping on it once and
`←→` walking it; `/` search and hidden classes on it (D3); the Inbox's row (D2); the link mode `L` and the paged
fold with the row (MR-2, R-3).
**Not in:** the presentation `R` (Inc MR-b, R-1); the link mode's own frame, which keeps one row per milestone
(R-3); every other view; normal task rows, their order and the done tail (`f4b53cc`); the head, the ruler and
the legend strip; the milestone data model and editors. No new dependency, no new key.

**Definitions.**

| Term | Meaning |
|---|---|
| board gantt | the main screen's gantt view, as `render_gantt` paints it (not the link mode's frame) |
| drawn milestones | a group's milestones the base board gantt draws as rows: its open milestones and, while the group has open work, its reached, not-archived ones (D-606) |
| milestone row | the one body row that draws a group's drawn milestones |
| walk order | the drawn milestones sorted by due date (no due last), then title, then id |
| share one cell | two or more drawn milestones whose marks fall in the same field cell, an off-window one counted in the edge-side cell it is drawn in (LLR-4602.6); the mark's count, its lead and the label column's ` i/N` all count by this one rule (R-6 F-1, SEC-4) |
| lead | of a mark's cell: its selected member, else its first in walk order; walk order sorts by due first, so the lead's date is the cell's earliest |
| anchor | the milestone `↑↓` lands on: the first in walk order that is open with a due on or after today, else the first open one, else the first |
| late | open with a due before today; its `▲Nd` is `N` = days past due |
| reached | done (`board.is_done`) |
| cell | one column of the gantt field; a milestone's cell is its due date's day cell on the field's axis |
| fixture MR-F | the round's synthetic board (`prototypes/milestone_row/proto.py:70-99`), today 2026-10-20: *Pilot rollout* with m1 reached (−3 d, Payment), m2 late (−1 d, Review), m3 (+4 d, Review), m4 (+4 d, Delivery), m5 (+10 d, Launch) and 4 tasks; *Eval harness* with g1 (+1 d), g2 (+8 d) and 3 tasks; *Docs & handover* with h1 (+15 d, no class) and 2 tasks; the Inbox with i1 (+6 d, Payment) and 1 task |
| `<glyph>` / `<hollow>` | a milestone's class glyph from `milestone_mark`, and its `HOLLOW` twin |

## 2. Source user story

**US-4601.** As the board's owner (`username_subject`), I want all of a project's milestones on one row of the
gantt, each at its date with its class mark, and to step through them with the arrow keys, so that milestones
stop spending a row each and the board's work fits on the screen. (Operator: «los milestones ocupan cada uno una
línea en el gantt... esto gasta mucho espacio. Necesito que queden en una sola línea en el gantt.»)

## 3. High-level requirements

### HLR-4601 — one milestone row per group
- **Traceability:** US-4601 · verdict A · D2
- **Ledger:** LED-2026-11-06-incMR.1
- **Statement:** The system shall draw a group's drawn milestones on one milestone row of the board gantt.
- **Validation:** `test` — layer 0 over `render_gantt` + pilot
- **Numeric pass threshold:** all LLR-4601.n thresholds; fixture MR-F at 118x30 draws 18 body rows (base 23).
- **Acceptance test(s):** AT-4601, AT-4602
- **Negative control:** base plan (one row per milestone): TC-4801 RED.

### HLR-4602 — the marks on the row
- **Traceability:** US-4601 · verdict A
- **Ledger:** LED-2026-11-06-incMR.1
- **Statement:** The system shall draw each drawn milestone on its row as its class mark at its date.
- **Validation:** `test` — layer 0 (cells and styles of the row)
- **Numeric pass threshold:** all LLR-4602.n thresholds.
- **Acceptance test(s):** AT-4601, AT-4603
- **Negative control:** draw every mark as `◆`: TC-4811 RED.

### HLR-4603 — the row's labels, label column and chip
- **Traceability:** US-4601 · verdict A
- **Ledger:** LED-2026-11-06-incMR.1
- **Statement:** The system shall label the milestone row with the selected milestone's title and the other milestones' dates where they fit.
- **Validation:** `test` — layer 0 at 118 and 80 columns
- **Numeric pass threshold:** all LLR-4603.n thresholds.
- **Acceptance test(s):** AT-4601, AT-4603, AT-4607
- **Negative control:** label every mark with its title: TC-4825 RED.

### HLR-4604 — `↑↓` stop on the row once, `←→` walk it
- **Traceability:** US-4601 · verdict A · R-2 (board half)
- **Ledger:** LED-2026-11-06-incMR.1
- **Statement:** When the cursor is on a milestone row, the system shall let `←` and `→` select its milestones in walk order.
- **Validation:** `test` — pilot (keys)
- **Numeric pass threshold:** all LLR-4604.n thresholds.
- **Acceptance test(s):** AT-4603, AT-4604
- **Negative control:** base `hmove` (a no-op in the gantt): TC-4833 RED.

### HLR-4605 — search and hidden classes reach single milestones (D3)
- **Traceability:** US-4601 · D3
- **Ledger:** LED-2026-11-06-incMR.1
- **Statement:** The system shall draw on the milestone row only the milestones the `/` query and the class filter leave visible.
- **Validation:** `test` — pilot
- **Numeric pass threshold:** all LLR-4605.n thresholds.
- **Acceptance test(s):** AT-4605
- **Negative control:** build the row from the unfiltered board: TC-4841 RED.

### HLR-4606.1 — the link mode keeps one row per milestone (MR-2, R-3)
- **Traceability:** US-4601 · MR-2 · R-3
- **Ledger:** LED-2026-11-06-incMR.2, LED-2026-11-06-incMR.3
- **Statement:** While the link mode is open, the system shall draw each milestone on its own row.
- **Validation:** `test` — pilot (link mode)
- **Numeric pass threshold:** all thresholds of LLR-4606.1, LLR-4606.2, LLR-4606.3.
- **Acceptance test(s):** AT-4606
- **Negative control:** the shared row in the link frame: TC-4851 RED.

### HLR-4606.2 — the milestone row is one row of the board gantt's pages (MR-2)
- **Traceability:** US-4601 · MR-2
- **Ledger:** LED-2026-11-06-incMR.2, LED-2026-11-06-incMR.3
- **Statement:** The system shall count the milestone row as one row of the board gantt's pages.
- **Validation:** `test` — layer 0 (paged frames)
- **Numeric pass threshold:** all thresholds of LLR-4606.4, LLR-4606.5.
- **Acceptance test(s):** AT-4606
- **Negative control:** page by the milestone's base row index: TC-4854 RED.

## 4. Low-level requirements

### 4.1 The row (HLR-4601)

- **LLR-4601.1 — Ubiquitous.** The board gantt shall draw, for every unfolded group with one or more drawn milestones, exactly one milestone row directly under the group's span row.
  Threshold: fixture MR-F at 118x30 → 4 milestone rows, each the line after its span row; no other line holds a milestone mark in the body; 4/4. *NC:* insert the row after the group's last task: RED.
- **LLR-4601.2 — Ubiquitous.** The milestone row shall hold exactly the group's drawn milestones.
  Threshold: per group of MR-F, the set of ids on the row = the milestone ids base `gantt_plan` puts in that group's rows (Pilot rollout 5, incl. reached m1; Eval harness 2; Docs 1; Inbox 1); a group with only reached milestones and no open work → no row (D-606); 5/5. *NC:* drop reached milestones: Pilot rollout 4: RED.
- **LLR-4601.3 — Ubiquitous.** The board gantt shall draw a group's non-milestone tasks one per row, in the order base draws them, under its milestone row.
  Threshold: per group of MR-F plus a done, not-archived task → the task ids in line order equal base's non-milestone ids in line order, the done one last; 4/4. *NC:* sort the tasks by title: RED.
- **LLR-4601.4 — Ubiquitous.** The board gantt shall draw the Inbox group's milestones on the Inbox group's own milestone row.
  Threshold: MR-F → i1 on the line after the `Inbox` span row, 0 Inbox milestones on any project's row; 1/1. *NC:* put i1 on the first project's row: RED.
- **LLR-4601.5 — Unwanted.** If none of a group's milestones is drawn, then the board gantt shall draw no milestone row for that group.
  Threshold: a group with no milestone; a group whose every milestone is archived; a group whose only milestones are reached and which has no open work → 0 milestone rows, line count = span + tasks; 3/3. *NC:* always emit the row: RED.
- **LLR-4601.6 — State.** While a group is folded, the board gantt shall draw no milestone row for it.
  Threshold: MR-F at 118x12 → each folded group's span row is followed by the next span row; 1/1 per folded group, ≥ 1 folded. *NC:* draw the row under a folded span: RED.
- **LLR-4601.7 — Ubiquitous.** The board gantt shall count a group's milestone row as one row when it decides which groups unfold.
  Threshold: MR-F at 80x24 → 0 folded groups (base folds ≥ 1); MR-F at 118x30 → 0 folded and 18 body rows; 2/2. *NC:* count each milestone as a row in the budget: 80x24 folds a group: RED.
- **LLR-4601.8 — Ubiquitous.** The milestone row's dependency gutter shall be blank.
  Threshold: MR-F with m3 waiting on the open task `store` → the gutter cell of each of the 4 milestone rows is blank; no `waits` or `early` entry of the frame's `drawn` comes from a milestone row (base adds `waits` for m3's row); 4/4. *NC:* draw the stop's `gantt_dep_mark` (`↳`) in the gutter: RED.

### 4.2 The marks (HLR-4602)

- **LLR-4602.1 — Ubiquitous.** The milestone row shall draw each drawn milestone whose due lies inside the field's window as its `<glyph>` in its class style, in its cell.
  Threshold: MR-F, nothing selected on the row → g1 `▲` cyan, g2 `■` violet, h1 `◆` in `mut` (the seat, `milestone_mark`), i1 `⬢` amber, each at `ax.cell(due)`; 4/4. *NC:* draw `◆` for every class: RED.
- **LLR-4602.2 — Ubiquitous.** The milestone row shall draw two to nine milestones sharing one cell as one `<glyph>` followed by the digit of their count, the glyph being the selected one's among them, else the first's in walk order.
  Threshold: m3 + m4 (Oct 24) → `■2` (m3 first by title `Steering…` vs `Store…`); with m4 selected → `▲2`; 2/2. *NC:* draw only the first glyph, no count: RED.
- **LLR-4602.3 — Unwanted.** If ten or more milestones share one cell, then the milestone row shall draw them as one `<glyph>` followed by `+`.
  Threshold: 10 milestones on one day → `<glyph>+`, 0 cells right of it overwritten beyond 2; 1/1. *NC:* print `10`: RED (3 cells).
- **LLR-4602.4 — Ubiquitous.** The milestone row shall draw a reached milestone alone in its cell as `<hollow>` followed by `✓` in the reached style.
  Threshold: m1 (Payment) → `⬡✓`; 1/1. *NC:* filled glyph: RED.
- **LLR-4602.5 — Ubiquitous.** The milestone row shall draw the selected milestone's mark in reverse video.
  Threshold: m2 selected → its cell's style has `reverse`; every other mark's style lacks it; 2/2. *NC:* no reverse: RED.
- **LLR-4602.6 — Unwanted.** If a drawn milestone's due lies before or after the field's window, then the milestone row shall draw `◂` (before) or `▸` (after) in the field's edge cell on that side and its mark in the cells next inward.
  Threshold: a reached milestone 40 days back (before `ctx`, the earliest open start); a reached milestone due 90 days ahead (done early), in a group with open work → `◂<hollow>✓` at cells 0–2 and `<hollow>✓▸` at the last three; two reached milestones after the window share the drawn cell → `<glyph>2▸`; 3/3. *NC:* clamp without the edge glyph: RED.
- **LLR-4602.7 — Unwanted.** If a drawn milestone has no due date, then the milestone row shall draw no mark for it.
  Threshold: a milestone with `due_date None` on a row with one dated one → 1 mark in the field; 1/1; 0 exceptions. *NC:* draw it at today's cell: RED.
- **LLR-4602.8 — Unwanted.** If a two-cell mark (`<glyph>N`, `<glyph>+` or `<hollow>✓`) falls in the field's last cell, then the milestone row shall start that mark in the cell before it.
  Threshold: through `render_gantt`, a reached milestone alone with its due on the window's last day; two reached ones sharing that cell → `<hollow>✓` and `<glyph>2` at cells `w-2`–`w-1`; the row is exactly `w` cells; 0 exceptions; 2/2. *NC:* start the mark at `w-1`: an IndexError or a row of `w+1` cells: RED.

### 4.3 Labels, label column, chip (HLR-4603)

- **LLR-4603.1 — Ubiquitous.** The milestone row shall draw the selected milestone's full title after its mark, past one blank cell, when the cells up to the next mark leave room for the whole title, else before its mark when the room there does.
  Threshold: 118x30, m3 selected → `Steering go/no-go` follows `■2 `; m5 (rightmost) selected with no room after → its title ends one cell before its mark; 2/2. *NC:* always after, overflowing into the next mark: RED.
- **LLR-4603.2 — Unwanted.** If neither side of the selected milestone's mark has room for its whole title, then the milestone row shall draw the title cut with `…` on the side with more room when that side has 6 cells or more, and no title in the field otherwise.
  Threshold: 118x30, m2 selected → `Rubric…` between m2 and m3; a cramped row (marks 4 cells apart) → no title cells; 2/2. *NC:* cut to any width (a 2-cell `R…`): RED.
- **LLR-4603.3 — Ubiquitous.** The milestone row shall draw, beside each mark that holds no selected milestone and whose lead is not late, the lead's date `Mon D`, past one blank cell, only where the whole date fits without touching another mark or label.
  Threshold: 118x30, nothing on Pilot rollout's row selected → `Oct 24` (beside `■2`: its lead m3's date), `Oct 30` beside their marks; g1 `Oct 21`, g2 `Oct 28`; 4/4. *NC:* cut a date to fit (`Oct`): RED.
- **LLR-4603.4 — Ubiquitous.** The milestone row shall draw, beside a mark whose lead is late, the lead's `▲Nd` in the over style in place of its date.
  Threshold: m2 not selected → `▲1d` beside its mark, `Oct 19` 0 occurrences on the row; 1/1. *NC:* draw `Oct 19`: RED.
- **LLR-4603.5 — Ubiquitous.** The milestone row shall draw no label over a mark, over another label, or past the field's edges.
  Threshold: every row of AT-4601..AT-4603 scenes at 118 and 80 → every mark cell still holds its mark, labels disjoint; 10/10 frames. *NC:* drop the one-cell gap check: RED.
- **LLR-4603.6 — State.** While no milestone of a row is selected, the row's label column shall read `◆ <N> milestones` (`milestone` when N = 1) at a label width of 24 cells or more and `◆ <N> ms` below, followed by ` ▲<L>` in the over style when L ≥ 1 of them are late.
  Threshold: 118 → `◆ 2 milestones`, `◆ 1 milestone`; 80 → `◆ 5 ms ▲1`; 3/3. *NC:* omit the late count: RED.
- **LLR-4603.7 — State.** While a milestone of a row is selected, the row's label column shall read its `<glyph>`, its title cut to the column, and ` <i>/<N>` when it is the i-th of N milestones in its cell.
  Threshold: m2 → `■ Rubric sign-off`; m4 → `▲ Store list frozen 2/2` (cut at 80, the `2/2` kept); 2/2. *NC:* drop the `i/N` tag: RED.
- **LLR-4603.8 — Ubiquitous.** The milestone row's chip shall be the selected milestone's `gantt_milestone_chip`, else the anchor's when it is open with a due on or after today, else blank.
  Threshold: m2 selected → `▲1d`; nothing selected on Pilot rollout → `in 4d` (m3); a row whose only milestones are late → blank; 3/3. *NC:* the first milestone's chip: `✓ done`: RED.
- **LLR-4603.9 — Ubiquitous.** The board gantt shall draw no line wider than the terminal.
  Threshold: every frame of AT-4601..AT-4607 at 118x30 and 80x24 → max `cell_len` per line ≤ width; 14/14. *NC:* a label padded to label_w + 1: RED.
- **LLR-4603.10 — Ubiquitous.** The board gantt's legend shall name the milestone mark and the reached mark whenever a milestone row draws them.
  Threshold: MR-F at 118x30 → the legend holds `◆ milestone`; with m1 drawn it holds the reached entry as base does; 2/2. *NC:* the row not adding to the frame's `drawn` set: RED.
- **LLR-4603.11 — Unwanted.** If a label that the milestone row draws in the field holds markup brackets, a backslash, or characters wider or narrower than one cell, then the milestone row shall draw the label's literal text, measured and cut in cells, within the field's width.
  Threshold (TC-4820): the selected milestone's title set in turn to `a]b[/]`, `[@click=app.quit]x`, `x\`, a wide-glyph title `里程碑 frozen` and a combining-mark title (`e` + U+0301 + `tape`), each drawn after its mark, before it, and cut with `…` → 0 exceptions; the row's `plain` holds the exact title or its `fit` cut ending in `…`; no span carries `@click` or any meta; every line's `cell_len` equals the frame width; 15/15. *NC:* lay the title one character per cell, each painted `c(char, tone)` (the oracle's `put`): `a]b[/]` raises `MarkupError`: RED. *NC 2:* measure the room with `len`: the wide title's line is wider than the frame: RED.

### 4.4 Navigation (HLR-4604)

- **LLR-4604.1 — Ubiquitous.** The board gantt's `↑↓` order shall hold, per group, the milestone row as one stop followed by the group's task rows in line order.
  Threshold: MR-F, the cursor on `Pilot store list`, `↑` → a milestone of Pilot rollout; `↑` again → no move (Pilot rollout is the first group); `↓`×2 from the row → `Pilot telemetry`; 3/3. *NC:* one stop per milestone: `↓` from the row lands on another milestone: RED.
- **LLR-4604.2 — Event.** When `↑` or `↓` moves the cursor onto a milestone row, the system shall select the row's anchor.
  Threshold: Pilot rollout → m3 (m1 reached, m2 late); a row of only late ones → the first late one; a row of only reached ones → the first; 3/3. *NC:* select the first in walk order: m1: RED.
- **LLR-4604.3 — Event.** When `→` is pressed while a milestone of a row is selected, the system shall select the next milestone of that row in walk order.
  Threshold: m3 → m4 (same day) → m5; 2/2. *NC:* skip same-day milestones: m3 → m5: RED.
- **LLR-4604.4 — Event.** When `←` is pressed while a milestone of a row is selected, the system shall select the previous milestone of that row in walk order.
  Threshold: m3 → m2 → m1; 2/2. *NC:* `←` moves forward: RED.
- **LLR-4604.5 — Unwanted.** If `←` is pressed on a row's first milestone or `→` on its last, then the system shall keep the selection unchanged.
  Threshold: m1 + `←` → m1; m5 + `→` → m5; 0 exceptions, no other group's milestone selected; 2/2. *NC:* wrap around: RED.
- **LLR-4604.6 — State.** While the selection is not a milestone of a board gantt milestone row, `←` and `→` shall change the selection exactly as at base.
  Threshold: gantt with a task selected → unchanged by `←`/`→`; kanban `←`/`→` → base column jumps; no selection in the gantt → base `_select_first`; 3/3. *NC:* `→` on a task row jumps to its group's row: RED.
- **LLR-4604.7 — Event.** When `enter` is pressed while a milestone of a row is selected, the system shall open the details of that milestone.
  Threshold: m3, `→`, `enter` → `TaskDetails` of m4; 1/1. *NC:* open the anchor's details: m3: RED.
- **LLR-4604.8 — Ubiquitous.** A task key pressed while a milestone of a row is selected shall act on that milestone.
  Threshold: m3, `→`, `]` → m4's phase moves one forward, m3's unchanged; `e` → the editor holds m4's title; 2/2. *NC:* the row's stop id stays the anchor: RED.

### 4.5 Search and hidden classes (HLR-4605, D3)

- **LLR-4605.1 — State.** While a `/` query is set, the milestone row shall draw only the milestones the query matches.
  Threshold: `/store` `enter` → Pilot rollout's row draws only m4, `◆ 1 milestone` / its title; the other groups draw no row; 2/2. *NC:* the row from the unfiltered board: 5 marks: RED.
- **LLR-4605.2 — Unwanted.** If a milestone's class is hidden, then the milestone row shall not draw it.
  Threshold: class Review hidden in `#` → Pilot rollout's row draws m1, m4, m5; m4's cell `▲` with no count; 2/2. *NC:* the row built before the class filter: RED.
- **LLR-4605.3 — Unwanted.** If a milestone is not drawn on its row (a `/` query does not match it, or its class is hidden), then the system shall leave it out of the `←→` walk.
  Threshold: Review hidden, m1 selected, `→`, `→` → m4, m5; `/store` + `←`/`→` → m4 stays; 2/2. *NC:* walk the unfiltered milestones: RED.

### 4.6 Link mode and the paged fold (HLR-4606.1: LLR-4606.1–.3; HLR-4606.2: LLR-4606.4, .5; MR-2)

- **LLR-4606.1 — State.** While the link mode is open, the system shall draw each milestone on its own row.
  Threshold: MR-F, a task selected, `L` → the link frame draws m1..m5 on 5 rows (reached m1 kept while the group has open work, as base), each named in `line_map`; byte-equal to base's link frame; 1/1. *NC:* the shared row in the link frame: RED.
- **LLR-4606.2 — Event.** When `L` is pressed while a milestone of a row is selected, the system shall open the link mode with that milestone as the waiting task.
  Threshold: m3, `→` (m4), `L` → the link frame's waiter is m4; 1/1. *NC:* the anchor as waiter: m3: RED.
- **LLR-4606.3 — Event.** When the link mode closes, the system shall draw the board gantt's milestone rows again.
  Threshold: `L`, `esc` → the frame equals the frame before `L`; `L`, a candidate, `enter` → 4 milestone rows again; 2/2. *NC:* a flag left set by the link frame: RED.
- **LLR-4606.4 — Event.** When a milestone of a paged group is selected, the board gantt shall draw the page that holds the group's milestone row.
  Threshold: a group of 1 milestone row + 20 tasks at 118x14, the cursor on the last task, `↑` until the row → the page shows the row and `▼ <n> below`, the count of task rows off the page; 2/2. *NC:* page by the milestone's base row index: RED.
- **LLR-4606.5 — State.** While the body holds only the span rows and the selected row, the board gantt shall draw the selected milestone's milestone row as the selected row.
  Threshold: groups = body rows (D8) and body ≤ 2, a milestone selected → the row drawn is the milestone row (its mark reverse, its label `<glyph> <title>`); 2/2. *NC:* base `task_row(sel)`: RED.

## 5. Acceptance tests (black-box, through keys)

- **AT-4601** — the row at rest. Fixture MR-F at 118x30 and 80x24, `3`, the cursor on `Pilot store list` → one milestone row under each of the 4 span rows; Pilot rollout's row reads `⬡✓`, `■ ▲1d`, `■2 Oct 24`, `★ Oct 30` (at 118); body 18 rows at 118x30 (base 23); 0 folded groups at 80x24; a blank gutter on every milestone row; no line wider than the terminal. (LLR-4601.1–.4, .7, .8; LLR-4602.1, .2, .4; LLR-4603.3, .4, .6, .9)
- **AT-4602** — folding. MR-F at 118x12 → folded groups show only their span row; a group with no milestone shows none. (LLR-4601.5, .6)
- **AT-4603** — onto the row and along it. From `Pilot store list`: `↑` → m3 selected, its title beside `■2`, the label column `■ Steering go/no-go 1/2`, chip `in 4d`; `→` → m4 (`▲2`, `2/2`); `→` → m5; `→` → m5; `←`×4 → m1; `←` → m1. (LLR-4602.2, .5; LLR-4603.1, .7, .8; LLR-4604.1–.5)
- **AT-4604** — acting on the walked one. m3, `→`, `enter` → details of m4; `esc`, `]` → m4 one phase on. `↓` → `Pilot store list`; `←`/`→` → no change. (LLR-4604.6–.8)
- **AT-4605** — D3. `/store` `enter` → Pilot rollout's row holds m4 only; `→` keeps m4. `esc` the query; hide class Review in `#` → the row holds m1, m4, m5; `→` from m1 → m4. (LLR-4605.1–.3)
- **AT-4606** — MR-2. m3, `→`, `L` → the link frame: one row per drawn milestone (m1..m5), byte-equal to base, waiter m4; `esc` → milestone rows back, m4 selected. A paged group: `↑` onto its row → the page holding the row. (LLR-4606.1–.4)
- **AT-4607** — edges. On one row, in a group with open work: a reached milestone due 90 days ahead (done early), one with no due, and 10 on one day → `<hollow>✓▸` in the field's last three cells, no mark for the undated one, `<glyph>+`; no line wider than the terminal at 118x30 and 80x24. (LLR-4602.3, .6, .7; LLR-4603.9)

## 6. Slice of functions to change (named and counted)

| # | File | Unit | Change | Requirements |
|---|---|---|---|---|
| 1 | views.py | `GanttGroup` | changed: a `lane` field (the group's drawn milestones in walk order); `rows` holds one stop for them, the anchor or the selected one, first | LLR-4601.1–.3, LLR-4604.1, .2 |
| 2 | views.py | `gantt_plan` | changed: under the board-gantt flag, the class filter first (`_hide`, N-5: its one seat), then milestones leave `rows` for `lane`; the stop rule; the fold budget counts 1 | LLR-4601.1–.7, LLR-4604.1, .2, LLR-4605.1, .2 |
| 3 | views.py | `gantt_milestone_row` | new: the row's field cells — marks, clash count, hollow `✓`, reverse, edges, the last-cell shift — and the field labels, each cut in cells and escaped once as a whole before it is laid into cells (R-7) | LLR-4602.1–.8, LLR-4603.1–.5, .11 |
| 4 | views.py | `gantt_lane_label` | new: the row's label column | LLR-4603.6, .7 |
| 5 | views.py | `gantt_lane` | new: the lane that holds the selection, for `action_hmove` (F-4) | LLR-4604.3–.6, LLR-4605.3 |
| 6 | views.py | `_gantt_frame` | changed: draws the row in the stop's place with a blank gutter, maps every lane id to its line in `line_map`, adds to `drawn`, the chip; the paged and D8 branches | LLR-4601.1, .6, .8, LLR-4603.8–.10, LLR-4606.4, .5 |
| 7 | views.py | `_gantt_field` | changed: one `rev:<style>` branch; its invariant names the escaped label run, painted as given (R-7) | LLR-4602.5, LLR-4603.11 |
| 8 | views.py | `nav_model` (gantt branch) | changed: builds the plan with `done_rows=True`, so the column reads the class-filtered board the frame draws (R-4, N-5) | LLR-4604.1, LLR-4605.3 |
| 9 | app.py | `TaskboardApp.action_hmove` | changed: in the gantt, a selected lane milestone walks its lane over the view's (filtered, class-hidden) board; else base | LLR-4604.3–.6, LLR-4605.3 |
| — | views.py | `render_gantt`, the legend's `_gantt_frame` call (`views.py:8718`) | call sites pass `done_rows=True` | LLR-4601.1, LLR-4603.10 |
| — | views.py | `gantt_link_frame`, `gantt_link_order` | unchanged on purpose: they never set the flag | LLR-4606.1 |

**Count: 9 units in 2 source files** (views.py, app.py) — 3 new, 6 changed — plus 2 call-site edits
(LED-2026-11-06-incMR.4, R-6 F-4). Within the 4-source-file budget. Tests that pin one row per milestone in the
board gantt (`tests/test_gantt.py`, `test_gantt_board.py`, `test_gantt_milestones.py`, `test_milestone_marks.py`,
`test_hotfix_2026_11_05.py`, `test_app.py`) are re-baselined one by one in E4, from the instrumented run's
`g` tags, not from this list (`e3-addenda.md` A-4).

## 7. Counts

US 1 · HLR 7 (HLR-4606 split into .1 and .2, LED-2026-11-06-incMR.3) · LLR 43 (4601: 8, 4602: 8, 4603: 11, 4604: 8, 4605: 3, 4606: 5; LED-2026-11-06-incMR.4, .5, .6) · AT 7.
