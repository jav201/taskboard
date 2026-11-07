# Requirements — taskboard — Inc MR-b, the presentation's milestones share one row (dev-flow-v3-beta)

> Strict EARS (five forms only), ISO/IEC/IEEE 29148. One `shall` per requirement, each with a numeric pass
> threshold and a negative control (*NC*). Ids: US-4651, HLR-4651..4654, LLR-4651.n..4654.n, AT-4651..4656.
> **E3 round-1 correction (2026-11-06):** RB-2..RB-6 (`00-e1-rulings.md`) with SEC-B1..SEC-B3 (`03-pdr-security.md`) and
> A-1, A-2, A-4, A-5 (`03-pdr-architect.md`) are applied here and in the graphs: LED-2026-11-06-incMRb.3 to .9.
> Range check (2026-11-06, `grep -rhoE "(HLR|LLR|AT|US)-46[5-9][0-9]" REQUIREMENTS.md .dev-flow/ tests/`): only
> the reservation of `HLR-4651`/`US-4651` in `../2026-11-06-v3-incMR/00-e1-rulings.md` §2. `TC-48nn` is MR-a's,
> so this increment's TCs use `TC-49nn` (0 hits).
> Base: `8ca174c` (MR-a merged to `main`; branch `feat/milestone-row-present`). Commission:
> `.dev-flow/COMMISSION-milestone-row.md` (D1 `si`, D3 `si`, MR-1); rulings R-1, R-2, R-7 in
> `../2026-11-06-v3-incMR/00-e1-rulings.md`.
> **Reuse.** MR-a's design is reused, not restated: the row's field is MR-a's `gantt_milestone_row` and its rules
> (LLR-4602.1–4602.8, LLR-4603.1–4603.5, LLR-4603.11), and its label text is MR-a's (LLR-4603.6, LLR-4603.7).
> Each requirement below cites the MR-a requirement it carries into `R`. MR-a's terms *walk order*, *late*,
> *reached*, *cell*, *fixture MR-F*, `<glyph>` and `<hollow>` hold unchanged.
> **TC numbering:** LLR-4651.n → TC-(4900+n); LLR-4652.n → TC-(4910+n); LLR-4653.n → TC-(4920+n);
> LLR-4654.n → TC-(4930+n). LLR-4652.10 → TC-4920, a number LLR-4653's range (TC-4921 up) does not use.

## 1. Scope

**In:** the presentation `R`, in its three views. View 1 `gantt` and view 2 `split` share `render_present`'s
field (R-1), and view 3 `all` uses `_all_timeline`. In each view, a project's drawn milestones go on one
milestone row: under the span row in views 1 and 2, and under the project's head row in view 3. The cursor
stops at each milestone in turn (R-2). The cursor order is applied to the briefs (view 1), the blocks
(view 2) and the timeline stops (view 3). The deck written by `x` is pinned as unchanged.

**MR-1, which views draw milestones:** all three. At base, each view gives every shown open milestone its own
field row (`_present_task_row`, `views.py:7475`). View 1 also gives it a brief line, and view 2 a block.

**Not in:**
- Any key, binding, hint row or `?` window line (R-2).
- The ruler, the legend strip and the header.
- The rail.
- What is shown or hidden. The `space`, `a` and `u` keys keep their meaning, applied to each milestone.
- The deck's renderers.
- The board gantt (MR-a, merged).

There is no Inbox in `R`: it presents projects only. No new dependency.

**Definitions.**

| Term | Meaning |
|---|---|
| drawn milestones (`R`) | a project's shown open milestones: open, `show_in_present` true, not of a hidden class — the milestones of `present_tasks_m(board, pid)[0]` (reached ones are not drawn in `R` at base, and stay so) |
| milestone row (`R`) | the one field row that draws a project's drawn milestones |
| stop order | for one project: its drawn milestones in walk order, then its other open shown tasks in base order |
| cursor milestone | the drawn milestone the cursor is on, if any |
| present label column | the field row's label cells (`_present_cols`: 30 cells from 100 columns, else 20) |

## 2. Source user story

**US-4651.** As the board's owner (`username_subject`), I want the presentation to draw a project's milestones on
one row, as the board's gantt now does, and to keep stepping through them one by one with the keys I already
use, so that the room I present in sees the work, not a row per milestone, and nothing I learned changes.
(Verdict D1: «si» — the presentation `R` follows the board's gantt.)

## 3. High-level requirements

### HLR-4651 — one milestone row per project in `R`
- **Traceability:** US-4651 · D1 · MR-1 · R-1 · carries HLR-4601
- **Ledger:** LED-2026-11-06-incMRb.1, LED-2026-11-06-incMRb.7, LED-2026-11-06-incMRb.9
- **Statement:** The system shall draw a presented project's drawn milestones on one milestone row of the presentation's field.
- **Validation:** `test` — layer 0 over `render_present` / `render_present_all` + pilot
- **Numeric pass threshold:** all LLR-4651.n thresholds; MR-F's *Pilot rollout* in view 1 at 118x30 draws 5 field body rows (base 8).
- **Acceptance test(s):** AT-4651, AT-4652, AT-4653
- **Negative control:** base field (one row per milestone): TC-4901 RED.

### HLR-4652 — the row looks as MR-a's row does
- **Traceability:** US-4651 · D1 · R-7 · RB-2 · RB-3 · carries HLR-4602, HLR-4603
- **Ledger:** LED-2026-11-06-incMRb.1, LED-2026-11-06-incMRb.3, LED-2026-11-06-incMRb.4, LED-2026-11-06-incMRb.5
- **Statement:** The system shall draw the presentation's milestone row with the board gantt's milestone-row marks and labels.
- **Validation:** `test` — layer 0 (cells, styles, label column, chip) at 118 and 80
- **Numeric pass threshold:** all LLR-4652.n thresholds.
- **Acceptance test(s):** AT-4651, AT-4655
- **Negative control:** base `_present_task_row` per milestone: TC-4911 RED.

### HLR-4653 — the cursor stops at each milestone, and no key changes (R-2)
- **Traceability:** US-4651 · R-2
- **Ledger:** LED-2026-11-06-incMRb.1
- **Statement:** When `↑` or `↓` moves the presentation's cursor, the system shall stop at each drawn milestone in stop order.
- **Validation:** `test` — pilot (keys)
- **Numeric pass threshold:** all LLR-4653.n thresholds.
- **Acceptance test(s):** AT-4651, AT-4653, AT-4654
- **Negative control:** one stop for the whole row (MR-a's board rule): TC-4921 RED.

### HLR-4654 — the `x` deck is unaffected
- **Traceability:** US-4651 · the orchestrator's MR-b scope ("the deck follows what `R` draws, or state that it is unaffected")
- **Ledger:** LED-2026-11-06-incMRb.2, LED-2026-11-06-incMRb.8
- **Statement:** The system shall write the same deck from `x` as at base.
- **Validation:** `test` — bytes against a base oracle
- **Numeric pass threshold:** LLR-4654.1.
- **Acceptance test(s):** AT-4656
- **Negative control:** the deck's proxy holds a different set of tasks — `present_deck_boards` takes `present_stop_order(present_tasks_m(board, p.id)[0])` in place of `present_tasks_m(board, p.id)[1]`, which drops the reached `tm1` — so the deck's sha256 differs from the `8ca174c` oracle: TC-4931 RED. (A mutant of the order alone is undone by the deck's own board-order sort, so it cannot fail; A-1.)

## 4. Low-level requirements

### 4.1 The row (HLR-4651)

- **LLR-4651.1 — Ubiquitous.** Views 1 and 2 shall draw, for a presented project with one or more drawn milestones, exactly one milestone row directly under the project's span row.
  Threshold: MR-F *Pilot rollout*, views 1 and 2 at 118x30 → the field line after the span row holds m2..m5's marks; no other field line holds a milestone mark; 2/2. *NC:* row after the last task: RED. (carries LLR-4601.1)
- **LLR-4651.2 — Ubiquitous.** View 3 shall draw, for every unfolded shown project with one or more drawn milestones, exactly one milestone row directly under the project's head row.
  Threshold: MR-F, `3`, 118x30 → 3 milestone rows (Pilot rollout, Eval harness, Docs & handover), each the line after its head; 3/3. *NC:* no row in view 3 (per-task rows kept): RED.
- **LLR-4651.3 — Ubiquitous.** The presentation's milestone row shall hold exactly the project's drawn milestones.
  Threshold: Pilot rollout → {m2, m3, m4, m5} (m1 reached: absent as at base); class Review hidden in `#` → {m4, m5}; m3 hidden with `space` → {m2, m4, m5}; views 1 and 3; 6/6. *NC:* include the reached m1: RED. (carries LLR-4601.2, LLR-4605.2)
- **LLR-4651.4 — Ubiquitous.** The presentation shall draw a project's open shown non-milestone tasks one per field row, in their base order, under its milestone row.
  Threshold: Pilot rollout's 4 tasks in base field order under the row, views 1, 2, 3; 3/3. *NC:* sort by title: RED. (carries LLR-4601.3)
- **LLR-4651.5 — Unwanted.** If a presented project has no drawn milestone, then the presentation shall draw no milestone row for it.
  Threshold: *Docs & handover* with h1 hidden by `space` → view 1 field = span + 2 task rows; view 3 likewise; a project with no milestone; 3/3. *NC:* always emit the row: RED. (carries LLR-4601.5)
- **LLR-4651.6 — State.** While a project is folded in view 3, by `enter` or by the overflow rule, view 3 shall draw no milestone row for it.
  Threshold: `enter` on *Eval harness*'s head → its head followed by the next head; 80x14 overflow-folded project likewise; 2/2. *NC:* draw the row under a folded head: RED. (carries LLR-4601.6)
- **LLR-4651.7 — Ubiquitous.** View 3 shall count a project's milestone row as one row when it decides which projects the overflow rule folds.
  Threshold: MR-F at 118x18 → base folds ≥ 1 project, new folds fewer; the layout's row count = heads + milestone rows + task rows; 2/2. *NC:* count one row per milestone in `need`: RED. (carries LLR-4601.7)
- **LLR-4651.8 — Ubiquitous.** The presentation's milestone row shall draw a blank in its dependency gutter.
  Threshold: MR-F, m3 waiting on the open task `store`; views 1 and 3 at 118x30 and 80x24, the cursor on m3 → the milestone row's gutter cell (the cell after the present label column) is a blank, and no line of the frame shows the `↳` base draws in m3's own row's gutter; 4/4. *NC:* draw the cursor milestone's `gantt_dep_mark` in the gutter: RED. (carries LLR-4601.8; RB-5)

### 4.2 The row's drawing (HLR-4652)

- **LLR-4652.1 — Ubiquitous.** The presentation's milestone row shall draw, in its field, the cells the board gantt's milestone row draws for the same milestones, axis, day and selection, the selection being the cursor milestone, else none.
  Threshold: views 1 and 3 at 118 and 80, cursor on m3, on m4, on a task → field cells equal `gantt_milestone_row(lane, sel, board, ax, today)` painted over the presentation's field ground; `■2`, `▲2`, `▲1d`, `Oct 30` present as LLR-4602.2 and LLR-4603.3/.4 say; 8/8. *NC:* select the anchor instead of the cursor milestone: RED. (carries LLR-4602.1–4602.8, LLR-4603.1–4603.5)
- **LLR-4652.2 — Ubiquitous.** The presentation's field shall paint a reversed mark and a covered label cell the way the board gantt's field paints them.
  Threshold: the cursor on m2 → its cell is reverse video in its class style; a title run covers its cells once, no doubled glyph, no stray tone name; 2/2. *NC:* `_present_field` unchanged (reads `rev:…` as a style name): RED.
- **LLR-4652.3 — State.** While the cursor is not on one of a row's milestones, the row's present label column shall read the project's hue bar `▎` followed by the text LLR-4603.6 gives.
  Threshold: view 1 on a task → `▎ ◆ 4 milestones ▲1` at 118 and `▎ ◆ 4 ms ▲1` at 80; 2/2. *NC:* drop the late count: RED. (carries LLR-4603.6)
- **LLR-4652.4 — State.** While the cursor is on one of a row's milestones, the row's present label column shall read `⟦`, the hue bar `▎` and the text LLR-4603.7 gives for that milestone.
  Threshold: cursor m4 → ` ⟦▎ ▲ Store list frozen   2/2` at 118 and ` ⟦▎ ▲ Store li… 2/2` at 80 (cut by cell width with `…`, tag kept); cursor m2 → ` ⟦▎ ■ Rubric sign-off` at 118 and ` ⟦▎ ■ Rubric sign-…` at 80; 4/4. *NC:* the lead `⟦` absent: RED. (carries LLR-4603.7; the R-7 cut at every width, RB-3)
- **LLR-4652.5 — Ubiquitous.** The presentation's milestone row's chip shall be the chip base draws for the cursor milestone's row, else for the first drawn milestone in walk order with a due on or after today, else blank.
  Threshold: cursor m2 → m2's base chip; cursor on a task → m3's base chip; a row of only late ones, cursor elsewhere → 13 blanks; 3/3. *NC:* the first milestone's chip (m2's) with the cursor elsewhere: RED. (carries LLR-4603.8)
- **LLR-4652.6 — Unwanted.** If a milestone's title on the presentation's milestone row holds markup brackets, a backslash or characters wider or narrower than one cell, then the presentation shall draw it as literal text within the row's cells and raise no exception.
  Threshold: titles `a]b[/]`, `[@click=app.quit]x`, `\`, `日本語のタイトル` each as the cursor milestone, views 1 and 3 → the plain text holds the title (or its `…` cut) literally, line `cell_len` = width, 0 exceptions, 0 live tags; 8/8. *NC:* build the label column with `c(title)` unescaped: RED. (carries LLR-4603.11, R-7)
- **LLR-4652.7 — Ubiquitous.** The presentation shall draw no line wider than the terminal.
  Threshold: views 1, 2, 3 × {118x30, 100x30, 80x24} on MR-F, the cursor on m3 → max `cell_len` per line ≤ width; 9/9. *NC:* pass the board gantt's label width (30 at 80): RED. (carries LLR-4603.9)
- **LLR-4652.8 — Ubiquitous.** The presentation shall draw its header, ruler rows, legend strip and hint row as at base.
  Threshold: views 1, 2, 3 × {118x30, 80x24} on MR-F → those rows' plain text equal base's; 6/6. *NC:* count the milestone row in the header's open count: RED.
- **LLR-4652.9 — Unwanted.** If a presented task's title holds a backslash, then view 1 shall draw the title in its brief line as literal text, each backslash once, within the terminal's width.
  Threshold: titles `\`, `x\` and `a\[b]`, each the cursor task, view 1 at 118x30 and 80x24 → measured on the rendered frame (`cell_len` of each line of `render_present(…).plain`, after `to_text`; never `_strip` of the markup, SEC-B2): the brief holds `⟦\⟧`, `⟦x\⟧`, `⟦a\[b]⟧` (or the `…` cut) literally, and every line is exactly the width; 6/6. RED on base: `\` and `x\` give a 119 / 81-cell line reading `\\`, and `a\[b]` reads `a[b]`. *NC 1:* the brief keeps `escape` (base): RED. *NC 2:* the measure-only fix, `escape` kept and the line padded or cut by its rendered width: RED on the literal check (`x\\`). (RB-2, SEC-B1: the fix is R-7's `_literal`)
- **LLR-4652.10 — Unwanted.** If a presented task's title holds a backslash before a `[`, then view 2 shall draw that backslash in the title of the task's block.
  Threshold: titles `a\[b]`, `\[x` and `ab\[` followed by 60 `x` (cut after the `\[`), each once as the cursor task, view 2 at 118x30 and 80x24 → the block's first row, measured on the rendered frame after `to_text`, holds `a\[b]`, `\[x`, `ab\[x…` literally, and every line is exactly the width; 6/6. RED on base: `\[x` reads `[x` and `ab\[`+60 `x` reads `ab[x…`; `a\[b]` already reads `a\[b]` on base (rich's `escape` escapes the tag-shaped `[b]`), so it is kept as a positive case. *NC:* the block heading keeps `escape` (base): RED on `\[x` (`▌ [x`). (SEC-B3; ledger LED-2026-11-06-incMRb.10)

### 4.3 The cursor (HLR-4653, R-2)

- **LLR-4653.1 — Event.** When `↑`, `↓`, `←` or `→` moves the cursor in views 1 and 2, the system shall move it one place along the presented project's stop order.
  Threshold: Pilot rollout, the cursor on m2, `↓`×4 → m3, m4, m5, `Pilot store list`; `↑` → m5; `→` → `Pilot store list` (`side` = move, base); 3/3. *NC:* base order (by due, milestones among tasks): RED.
- **LLR-4653.2 — Event.** When `↑` or `↓` moves the cursor in view 3, the system shall move it one place along the drawn stops: per project, its head, then its drawn milestones in walk order, then its task rows.
  Threshold: on *Pilot rollout*'s head, `↓`×5 → m2, m3, m4, m5, `Pilot store list`; 1/1 per step (5/5). *NC:* one stop per milestone row: RED.
- **LLR-4653.3 — Unwanted.** If the cursor task of views 1 and 2 is not drawn, then the system shall put the cursor on the first place of the stop order.
  Threshold: open `R` with no cursor → m2; cursor task hidden by `space` → the stop order's first; 2/2. *NC:* the first by due among all open tasks (base `open_t[0]`): RED in a fixture where a task is due before every milestone.
- **LLR-4653.4 — Event.** When `space` is pressed with the cursor on a drawn milestone, the system shall hide that milestone alone.
  Threshold: cursor m3, `space` → m3's `show_in_present` false; m2, m4, m5 still on the row; m4 alone in its cell `▲`, no count; 3/3. *NC:* hide every milestone of the cell: RED.
- **LLR-4653.5 — Ubiquitous.** View 1 shall draw its briefs, and view 2 its blocks, in the presented project's stop order.
  Threshold: view 1 briefs read m2, m3, m4, m5, then the 4 tasks; view 2 blocks in the same order (two columns from 100 wide, filled in order); 2/2. *NC:* briefs in base order: RED.
- **LLR-4653.6 — Ubiquitous.** The presentation shall bind exactly the keys it binds at base, and its `?` window shall list exactly the rows it lists at base.
  Threshold: `PresentScreen` binding set = base; `PresentKeys` window text = base; 2/2. *NC:* bind `←→` to a row walk: RED.

### 4.4 The deck (HLR-4654)

- **LLR-4654.1 — Event.** When `x` is pressed in any view, the system shall write a deck byte-identical to the deck base writes for the same board, view, scope and day.
  Threshold: MR-F, views 1, 2 and 3 → sha256 equal to a base oracle captured on `8ca174c` from the same fixture; 3/3. *NC:* `present_deck_boards` holds `present_stop_order(present_tasks_m(board, p.id)[0])` in place of `present_tasks_m(board, p.id)[1]`: `ppr`'s proxy drops the reached `tm1` (and any done task), so the sha256 of MR-F's deck differs from the oracle: RED, 3/3. (RB-6, A-1: the NC changes WHICH tasks the deck holds, not their order, which the deck re-sorts by board position)

## 5. Acceptance tests (black-box, through keys)

- **AT-4651** — view 1. Fixture MR-F, `R` on *Pilot rollout*, at 118x30 and 80x24. The field shows the span row, one milestone row, then 4 task rows. The cursor starts on m2: the row shows m2 reversed with `Rubric…`, and the label column reads ` ⟦▎ ■ Rubric sign-off` at 118x30 and ` ⟦▎ ■ Rubric sign-…` at 80x24 (RB-3). `↓` → m3 (title beside `■2`). `↓` → m4 (`▲2`, `2/2`). `↓` → m5. `↓` → `Pilot store list`. The briefs follow the same order. The milestone row's gutter is blank. No line is wider than the terminal. (LLR-4651.1, .3, .4, .8; LLR-4652.1–.5, .7, .8; LLR-4653.1, .3, .5)
- **AT-4652** — view 2. `2`: the same field and cursor walk; the blocks in stop order. (LLR-4651.1; LLR-4653.1, .5)
- **AT-4653** — view 3. `3` at 118x30: under each head, one milestone row, then the tasks. `↓` from *Pilot rollout*'s head walks m2..m5, then the tasks. `enter` on *Eval harness* folds it: no milestone row. `←` → the rail on *Pilot rollout* (base). At 118x18 (room 15, need 15) the overflow folds no project, where base folds 2 (*Eval harness*, *Docs & handover*) (RB-4). (LLR-4651.2, .6, .7; LLR-4653.2)
- **AT-4654** — hiding. View 1, cursor m3, `space` → the row holds m2, m4, m5. `u` lists m3. `a` → m3 back on the row. Hide class Review in `#`, then `R` → the row holds m4, m5. Hide h1 → *Docs & handover* draws no row. (LLR-4651.3, .5; LLR-4653.4)
- **AT-4655** — hostile titles. Milestones titled `a]b[/]`, `[@click=app.quit]x`, `\`, `x\`, `a\[b]` and a wide-glyph title, each walked onto in views 1, 2 and 3 at 80x24 → literal text in the row, the brief and the block, each backslash once and none dropped; 0 exceptions; the app still running; every line of the rendered frame (after `to_text`) exactly 80 cells. `?` → the window is as at base. (LLR-4652.6, .9, .10; LLR-4653.6)
- **AT-4656** — the deck. `x` in views 1, 2 and 3 → each file's sha256 equals the base oracle. (LLR-4654.1)

## 6. Slice of functions to change (named and counted)

| # | File | Unit | Change | Requirements |
|---|---|---|---|---|
| 1 | views.py | `present_stop_order(open_t)` | new: drawn milestones in walk order, then the other open tasks in base order | LLR-4653.1–.3, .5 |
| 2 | views.py | `milestone_walk_key` | lifted from `gantt_plan`'s nested `walk_key` to module scope, so `R` and the board share one walk order; `gantt_plan` calls it (MR-a behaviour byte-unchanged) | LLR-4653.1, .2 |
| 3 | views.py | `_present_lane_row` | new: the present label column (`⟦`, `▎`, `gantt_lane_label` text), the field from `gantt_milestone_row`, the present chip | LLR-4651.1–.3, LLR-4652.1, .3–.6 |
| 4 | views.py | `_present_field` | changed: paints `rev:<style>` and covered (`""`) label cells as `_gantt_field` does | LLR-4652.2, .6 |
| 5 | views.py | `render_present` | changed: span, milestone row, task rows; cursor, briefs and blocks in stop order | LLR-4651.1, .4, .5, LLR-4653.3, .5 |
| 6 | views.py | `_all_plan` | changed: each project's open list in stop order | LLR-4653.2 |
| 7 | views.py | `_all_layout` | changed: one row per milestone row; each milestone stop mapped to that row | LLR-4651.6, .7, LLR-4653.2 |
| 8 | views.py | `_all_timeline` | changed: the head row, the milestone row, the task rows | LLR-4651.2, .3, .6 |
| 9 | app.py | `PresentScreen._shown_ids` | changed: the stop order (`present_stop_order`) | LLR-4653.1, .3 |
| 10 | views.py | `_present_brief` | changed (RB-2, SEC-B1): the title is `_literal(txt)` in place of `escape(txt)`, cut first by `clip` as now | LLR-4652.9 |
| 11 | views.py | `_present_heading` | changed (SEC-B3): the title is `_literal(clip(…))` in place of `escape(clip(…))` | LLR-4652.10 |
| 12 | views.py | `_present_task_row` | changed (A-2): the `if task.milestone:` branch is removed; both callers pass only non-milestones | LLR-4651.1, .4 |
| — | views.py | `present_tasks`, `present_tasks_m`, `present_deck_boards` | unchanged on purpose: the deck reads `[1]` in board order | LLR-4654.1 |
| — | keymap.py | `PRESENT_KEYS` | unchanged on purpose (R-2) | LLR-4653.6 |

**Count: 12 units in 2 source files** (views.py, app.py): 3 new or lifted, 9 changed (rows 10–12 added by RB-2, SEC-B3 and A-2). That is within the 4-source-file
budget. The oracle frames that pin one row per milestone in `R` (PRES-V3, PRES-V4, the `tests/test_present*.py`
family, `tests/test_legend.py`, `tests/test_milestone_marks.py`) are re-baselined one by one in E4. The base deck
oracle for LLR-4654.1 is captured on `8ca174c` before E4 edits anything.

## 7. Counts

US 1 · HLR 4 · LLR 25 (4651: 8, 4652: 10, 4653: 6, 4654: 1) · AT 6.
