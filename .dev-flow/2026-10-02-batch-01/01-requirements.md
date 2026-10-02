# Requirements Document — taskboard — Batch 2026-10-02-batch-01

> Live contract (current state only). Mode `core`. Language `en`. The append-only ledger is
> `01-requirements-ledger.md`. Template: flow `templates/req-template.md` (reserved field
> names kept literal). Ids use a batch-disjoint `1xx` range (`US-101`, `HLR-101`,
> `LLR-101.1`, `AT-101`, `TC-101`) because `HLR-001`..`HLR-012` and `AT-001`..`AT-028`
> are already taken in this repository's record and canon.

## 1. Introduction

### 1.1 Purpose
Fold the operator's (Javier) kg_mejoras prototype verdicts (rounds 1–8, `NOTES.md`) into the
shipped app, as **Batch A1** of `IMPLEMENTATION-PLAN.md`: the gantt becomes the whole-board
fitted view **G-A** with the two-row date ruler **AX-2**; the round-7 **colour budget** is
applied to the kanban and the gantt; and the repo `README.md` and `RUN.md` are rewritten from
`README-AUDIT.md`. The readable kanban (**K-A + R-1b**) is Batch A2 (§2.6, US-105 `OUT`).

### 1.2 Scope
In: `render_gantt` and its helpers, the gantt branch of `nav_model`, the gantt's legend
entries / help usage / help example, the gantt branch of the app's selection seat
(`TaskboardApp._select_first`, `taskboard/app.py` — P2 finding Q-2/UX-1), the non-focus
accent uses inside the kanban and gantt renderers (titles, critical chain, horizon group
colour, matrix percent, the card `↗` token, the ≤7-day relative-due token), `README.md`,
`RUN.md`.
Out: the kanban card/column layout (K-A, R-1b — Batch A2), the keybar's key hints and every
other view's title (colour budget beyond kanban+gantt — BACKLOG), weekend shading
(round-5 frames, not in the AX-2 commission — BACKLOG), dependencies / milestones / cascade
(Batch B), forecast (G-B, rejected), any new key or model field.

### 1.3 Definitions
| Term | Definition |
|------|------------|
| open task | a visible task that is not done (`Board.is_done` false) and not archived |
| rest work | a visible task that is done or archived |
| window | the gantt field's date range: `start` plus `field_w` cells of `k` days each |
| `k` | days per field cell, one of `GANTT_SCALES = (0.5, 1, 2, 3, 7)` |
| group | one project of the gantt (or the Inbox: open tasks with no project) |
| folded / unfolded | a group drawn as its span row only (`▸`) / span row plus one row per open task (`▾`) |
| ruler | the two rows pinned under the gantt header: the month row and the day row |
| echo | the selected task's exact start/due drawn on the day row as `⟦━⟧` with its dates |
| cadence | which days get a number on the day row: `daily`, `Mondays`, `1st/15th`, `1st` |
| late | an open task whose due date is before today |
| focus role | what the accent may still paint on the kanban and gantt panels after the colour budget: the field being edited (the `/` filter bar) and today's marks (the today rule, today's number, the no-selection `today …` label — D4). The selection itself is reverse video, as shipped |
| panel size / terminal size | `render_*` takes the PANEL's width × height (the board widget); the app's terminal is larger by the ribbon and keybar. Render-level thresholds are panel sizes; app-level ATs name terminal sizes |

### 1.4 References
`.claude/worktrees/kg-mejoras/prototypes/kg_mejoras/`: `IMPLEMENTATION-PLAN.md` §Batch A,
§Risks; `NOTES.md`; `README-AUDIT.md`; `variants_gantt.py` (`render_ga`, `fit_axis`,
`fold_plan`, `gutter`, `due_chip`); `variants_round5.py` (`cadence`, `day_row`, `month_row`,
`echo_spec`, `_project_marks`); `variants_polish.py` (`BUDGET`); oracle captures
`out/G-A-118x30.txt`, `out/AX-2-118x30.txt` (+ `80x24`).
Code: `taskboard/views.py:2455` (`render_gantt`), `views.py:2070` (`gantt_tasks`),
`views.py:4822` (`nav_model` gantt branch), `views.py:5066` (gantt legend),
`views.py:4922` (gantt help usage), `views.py:4996` (gantt help example).

## 2. Overall description

### 2.1 Product perspective
Textual TUI (`textual 8.2.8`, `rich 15.0.0`). Every view renders rich markup through
`to_text`; `render_view` fills a `line_map` (task id → row) the app scrolls with, and
`nav_model` gives the arrow-key order. F-3 law: the cursor never rests on a task the view
does not draw, and nav order = draw order.

### 2.3 User characteristics
One owner-operator (Javier), keyboard-first, Windows Terminal, from 80×24 to full screen;
the gantt is one of his two most-used views. Task (context of use, UX-14): the weekly
re-plan — spot what is late, read a bar's exact dates, check each project's committed due,
walk the open work with `j`/`k`.

### 2.4 Constraints
≤ 4 source files per increment; no new dependency; `render_gantt`'s signature and
`render_view`/`nav_model` keyword contracts are consumed by `app.py` and existing tests;
prototype code is a design source, not code to paste (`IMPLEMENTATION-PLAN.md` §Risks).

### 2.5 Assumptions
- A1: the prototype board (`tests/kg_board.py`, rebuilt from the prototype's `fixture.py`)
  is the oracle board: renders of it are compared with the verdict frames.
- A2: the operator judges TUI work on real renders; captures at 118×30 and 80×24 are owed
  for every changed view (commission).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-101 | As the board owner, I want the gantt to show the whole board fitted to the open work — every project present, the ones I am not looking at folded to one row — so that nothing I own is hidden behind "+N not shown". | NOTES.md rounds 1–2 verdict "Gantt: G-A"; open ruling "unfolds the selected project plus the most-late projects while rows remain" | READY |
| US-102 | As the board owner, I want the gantt to tell me its dates — months and day numbers at the top that never collide, and the selected task's exact start and due on that ruler — so that I can date any bar without counting cells. | NOTES.md round 5 "the bottom axis drops labels"; verdict "Ruler AX-2 (es mejor)" | READY |
| US-103 | As the board owner, I want the accent colour on the kanban and the gantt to stop branding titles, chains and chips, so that what is left in accent — the field I am typing in and today — is what stands out (the selection keeps its reverse video; D4). | NOTES.md round 7 "the accent (#2dd4bf) is overloaded"; colour budget dict, `variants_polish.BUDGET` | READY |
| US-104 | As anyone reading the repository, I want a README and RUN.md that describe the app as it ships today, without personal paths, so that I can install, run and learn it from the page. | operator 2026-09-30 "actualiza el README del repo, está muy desactualizado y tiene errores y problemas estéticos"; `README-AUDIT.md` | READY |
| US-105 | As the board owner, I want readable two-row kanban cards with project bands and one board-wide high band on top, capped with "+N more", so that I can read titles and see urgent work first. | NOTES.md rounds 1–2 (K-A `┈`), R-1 verdict (R-1b + cap) | OUT |

#### Refinement log

**US-101 — whole-board fitted gantt (G-A)**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ (one renderer + its nav seat) · T ✓
- **Functionality:** user = owner · outcome = every project has a row; open work drawn on a window fitted to it; done folded to `✓n` · why = the shipped gantt hides 9 rows at 118×30 (P-1) · out of scope = forecast (G-B rejected), timeline edit (G-C deferred).
- **Feasibility:** re-derive `_Axis`/`fit_axis`/`fold_plan` inside `views.py`; nav seat shared with the renderer.
- **Evaluability:** render the oracle board at 118×30 / 80×24 through `render_view`: 5 project rows, no "+N not shown"; app key walk lands only on drawn rows.
- **Classification:** READY.

**US-102 — the ruler (AX-2)**
- **INVEST:** all ✓ (depends on US-101's axis: implement after it).
- **Functionality:** two pinned rows under the header; bottom axis removed; selection echo; project `◆` on the month row.
- **Evaluability:** ruler rows parsed from the render; the no-drop law over a size sweep; echo moves when the selection moves.
- **Classification:** READY.

**US-103 — colour budget**
- **INVEST:** all ✓ once scoped. **Scope (decided here, D10):** kanban + gantt renderers. App-wide (other views' titles, keybar key hints, ribbon clock, setup hints) is a palette pass over 9 views and the keybar — BACKLOG.
- **Evaluability:** collect the cells painted in `HEX["accent"]` from kanban and gantt renders; each must be a focus-role or today cell.
- **Classification:** READY.

**US-104 — README + RUN.md**
- **INVEST:** all ✓. Docs only (no SOURCE file); 33 audit findings; every fact re-verified against code at writing time.
- **Evaluability:** a test reads `README.md`/`RUN.md` and checks them against the code (views from `VIEW_ORDER`, keys from `KEYMAP`, no personal path).
- **Classification:** READY.

**US-105 — readable kanban (K-A + R-1b)**
- **Classification:** `OUT` — deferred to Batch A2 under the commission's pre-authorized split (D1). Evidence (executed at P0): the grouped kanban and the gantt are each asserted by tests in 14–15 files (`grep -l "render_kanban\|\"kanban\"" tests/*.py` → 14; gantt → 15), the kanban renderer was rewritten one batch ago (K4 band + badges, 1336 → 1535 tests), and the plan's own §Risks names the split. Next action: BACKLOG entry "Batch A2 — readable kanban K-A + R-1b".

### 2.7 Premise evaluation (C-43)

| # | Premise | Tier | Verdict | Executed evidence | Disposition |
|---|---|---|---|---|---|
| P-1 | The shipped gantt hides rows on the oracle board: "+9 not shown" at 118×30, "+15 not shown" at 80×24 | premise | ✅ TRUE | `render_gantt(kg_board.build(), False, "tw3", TODAY, 118, 30)` last row ends `+9 not shown`; at 80×24 `+15 not shown` (P0 probe, `evidence/p0-probes.txt`) | US-101 |
| P-2 | The shipped gantt's nav walks tasks the view does not draw (F-3 gap), including done tasks | premise | ✅ TRUE | same probe: nav 28 ids, drawn 21 (118×30) / 17 (80×24); done ids `tw1 tm1 td1` in nav | fixed by LLR-101.6 |
| P-3 | The shipped bottom axis drops month labels (OCT absent at 118×30) | premise | ✅ TRUE | probe: axis row `-48d SEP today NOV DEC JAN +115d` — October, today's month, unnamed | US-102 |
| P-4 | On the rendered kanban and gantt the accent paints, besides today's rule, these non-focus marks: the gantt title, `cadena crítica N`, `└─►`; the kanban title, the `+Nd` relative-due token, the card `↗`, the horizon group's colour (`This week` label, its `▐`, the lanes `THIS WEEK` label) and the matrix percent | premise | ✅ TRUE | census over RENDERED spans (Q-24), base tree, oracle board + one URL card, every presentation × group mode: `evidence/p0-probes.txt` §P-4 | LLR-103.1..3 |
| P-5 | `README.md` carries the personal OneDrive path 3× and `RUN.md` 1× | premise | ✅ TRUE | `grep -n OneDrive README.md RUN.md` → README 90, 108, 125; RUN 4 | LLR-104.1 |
| P-6 | Nine views ship (`VIEW_ORDER`) and `?` is bound to `legend` (the help modal) | premise | ✅ TRUE | `VIEW_ORDER` len 9; `keymap.py:63` `Key("?", "?", "legend", "Map", …)` | LLR-104.1 |
| P-7 | Base suite is green | premise | ✅ TRUE | `python -m pytest -q` at `57a6075` → 1535 passed in 131.49 s (`evidence/base-suite.txt`) | — |
| P-8 | The critical chain of the oracle board is `tm2 → tm3 → tm4 → tm5` (4 tasks) | premise | ✅ TRUE | `critical_chain(kg_board.build())` → `['tm2','tm3','tm4','tm5']` | AT-106 |

| P-9 | On the base tree `_select_first` keeps a done task selected in the gantt (the first visible task of the oracle board, `tw1`, is done) | premise | ✅ TRUE | qa-reviewer probe (Q-2): `visible_tasks` → `['tw1',…]`, `is_done(tw1)` True; `app.py:563-571` | LLR-101.9 |
| P-10 | 31 existing test nodes in 7 files fail on a scratch copy with the drafted renderer merged (the reverse census, C-39) | premise | ✅ TRUE | full suite on a scratch copy (not a git checkout): 50 failed / 1485 passed, of which 19 are the copy's missing `.git` (`test_no_live_board`, `test_precommit_gate`, `test_scratch_cannot_be_committed`) and 31 are listed in §6.6 | §6.6 |

- **Premise evaluation:** 10 premise(s) · ✅ TRUE 10 / ❌ FALSE 0 / ❓ UNDECIDABLE 0

### 2.8 Fork preconditions (C-52)
- **Fork preconditions:** none — this batch runs one lane

## 3. High-level requirements (HLR)

### HLR-101 — Whole board on a window fitted to the open work
- **Traceability:** US-101
- **Ledger:** LED-2026-10-02-batch-01.1, LED-2026-10-02-batch-01.10, LED-2026-10-02-batch-01.20, LED-2026-10-02-batch-01.26
- **Statement:** When the gantt is drawn, the system shall lay its field on a window of `k` days per cell, `k` being the smallest of 0.5, 1, 2, 3 and 7 whose window holds every open task's due date, the due date of every project holding open work and today (each with two days' margin), shall spend the spare cells on past context back to the earliest open start, and shall draw one span row for every visible project — clipped with `◂`/`▸` where it leaves the window, empty where it has no dates — and one for the Inbox while it holds tasks; an unparsable date shall count as absent.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_board.py -k "AT_101 or window or whole_board"`
- **Numeric pass threshold:** oracle board, panel 118×30 → `k = 1`, panel 80×24 → `k = 2` (the verdict frames' scales); 5 project rows at both; 0 rows of rest work; app at terminal 118×30 and 80×24: every project name painted in the board panel and no `not shown`; a past all-done project and an undated project each keep a span row; AT-109 on the oracle board plus one archived done task `tw7` in Website Redesign: `v` turns `✓1` into `✓2` on its span row; `F` on Website Redesign → one group, window `lo` = Sep 25, `hi` = Oct 16 (its open dues −3..+14 and its due +10, ±2 days); `/` query `API` → nav == the open ids of API Platform in draw order and the ruler at panel rows 3–4 under the filter bar; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** every project is on screen, its open work on a window that fits it.
  - **Shipped surface:** `TaskboardApp` key `3` (painted board panel, read through `App.run_test`).
  - **Acceptance test(s):** AT-101, AT-109, AT-110, AT-111
  - **Boundary catalog (QC-3):** ☑ empty (no projects, no tasks → `(nothing scheduled — press 'a' to add a task)`) ☑ boundary (work inside one day → `k = 0.5`; work spanning more than `7 × field_w` days → `k = 7`, Monday-aligned; a past all-done project; an undated project) ☑ invalid (an unparsable due date counts as absent) ☐ error — N/A: the renderer raises nothing
  - **Negative control:** the base tree paints `+9 not shown` at panel 118×30 → RED (P3).

### HLR-102 — Projects fold; nothing is hidden while folding can hold it
- **Traceability:** US-101
- **Ledger:** LED-2026-10-02-batch-01.2, LED-2026-10-02-batch-01.11
- **Statement:** While the gantt has fewer body rows than its groups' open tasks need, the system shall keep one span row per group, shall unfold the selected task's group first and then each other group in turn — most-late first, then earliest open due — when all of its open rows fit what is left, skipping one that does not fit and trying the next; shall show on the span row of a folded group its open count, and on every span row its late count `▲n` and, where the label is at least 26 cells wide, its rest count `✓n`; shall never draw a row for rest work; and shall say `+N not shown` only when the span rows alone exceed the body rows.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_board.py -k fold`
- **Numeric pass threshold:** oracle board, `tw3` selected: panel 118×30 → `▸ Data Warehouse    4 open ✓1`, the four others `▾`; panel 80×24 → `▸ Mobile App      5` and `▸ Data Warehouse  4`, the others `▾`; no `not shown` at either; a synthetic board where a large group does not fit and a smaller later one does → the smaller one unfolds; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** folded projects read `▸ name  N open` (`▸ name  N` when narrow), unfolded ones list their open tasks, finished work shows only as `✓n`.
  - **Shipped surface:** `TaskboardApp` key `3`.
  - **Acceptance test(s):** AT-101
  - **Boundary catalog (QC-3):** ☑ boundary (selected group taller than the body; span rows > body rows; a larger group skipped, a smaller one unfolded) ☑ empty (a project with no open work: span row only) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** a fold that stops at the first group that does not fit leaves the synthetic smaller group folded → RED (P3 mutation).

### HLR-103 — Rows end in one compact due chip; dependencies live in a gutter
- **Traceability:** US-101
- **Ledger:** LED-2026-10-02-batch-01.3, LED-2026-10-02-batch-01.12
- **Statement:** When a gantt row is drawn, the system shall end it in one right-aligned due chip — `▲Nd` in `over` for late work, `today` in `soon`, the month and day (`Oct 6`) in `mut` otherwise, `no due` in `dim` — and shall draw a task's dependency mark `↳` in a one-cell gutter column between its label and the field, never over a label or a bar: in `over` when the task has a start date earlier than the latest due date of its open dependencies, bold `bright` when the task is on the critical chain, `mut` otherwise, and blank when it waits on no open work.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_board.py -k "AT_103 or chip or gutter"`
- **Numeric pass threshold:** oracle board at panel 118×30: the gutter column (30) holds `↳` exactly on the drawn open tasks with an open dependency (`tw4 tw5 tm3 tm4 tm5 ta6 ta2`; `td5` sits in the folded Data Warehouse), every task title intact left of it; chips `tw3` `▲2d`, `to3` `today`, `ta5` `no due`, `tw4` `Oct 6`; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a short due chip per row; `↳` marks in their own column.
  - **Shipped surface:** `TaskboardApp` key `3`.
  - **Acceptance test(s):** AT-103
  - **Boundary catalog (QC-3):** ☑ boundary (dependency done → no mark; start before dependency due → `over`; no start → never `over`) ☑ empty (no due date → `no due`) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base tree draws `└─►` inside the label column and a `start → due` pair → RED (P3).

### HLR-104 — The cursor walks what the gantt draws
- **Traceability:** US-101
- **Ledger:** LED-2026-10-02-batch-01.4, LED-2026-10-02-batch-01.13, LED-2026-10-02-batch-01.19, LED-2026-10-02-batch-01.21, LED-2026-10-02-batch-01.27
- **Statement:** While the gantt is shown, the arrow-key order shall be the open tasks of every group in draw order (groups in board order, then the Inbox; tasks in `gantt_tasks` order), a key past either end shall do nothing, and the selected task shall always be drawn and scrolled into view: its group unfolds; a group taller than the body draws the page of its open tasks that holds the selection (pages of the rows left, so the rows move once per page) and keeps its `N open` count; when the span rows alone overflow, the drawn span rows are the page (`group index // (body − 2)`) of groups holding the selected group, with only the selected task's row under its span; and whenever the selected task is not open work of the gantt — on entering the view, or after a change makes it done or archived — the selection moves to the open task that followed it in the group's draw order, else the one before it, else the first open task drawn — one row away, so an extra `]` cannot land on a distant task (UX-15).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_board.py -k "AT_102 or AT_108 or nav"`
- **Numeric pass threshold:** app at terminal 80×24 and 118×30 on the oracle board: `down` pressed once per open task (25): after every press the selected title is painted in reverse inside the panel viewport (`scroll_offset.y ≤ line_map[sel] < scroll_offset.y + viewport.height`) and the two ruler rows are the panel's rows 1–2; `down` on the last task leaves the selection; nav ids == open ids in draw order; 0 rest ids in nav; entering the gantt with `tw1` (done) selected lands on `tw2`; `]` moving the selection to done lands on the open task that followed it in its group, and one more `]` advances that task's phase (pinned: the task one row away, not another); `down` then moves; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** walking with `j`/`↓` never parks the cursor on an invisible task; a folded project opens when the cursor enters it.
  - **Shipped surface:** `TaskboardApp` keys `3`, `down`, `up`, `]`.
  - **Acceptance test(s):** AT-102, AT-108, AT-113
  - **Boundary catalog (QC-3):** ☑ boundary (a 30-task project at terminal 80×24; a 30-project board at terminal 80×24 with a task of the last project selected; the last task + `down`) ☑ empty (no open task → empty nav, nothing selected) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base nav includes 7–11 undrawn ids (P-2) and keeps `tw1` (done) selected (P-9) → RED.

### HLR-105 — A two-row date ruler pinned at the top
- **Traceability:** US-102
- **Ledger:** LED-2026-10-02-batch-01.5, LED-2026-10-02-batch-01.14, LED-2026-10-02-batch-01.28
- **Statement:** When the gantt is drawn, the system shall pin two rows directly under the header — a month row with `┃` on the first cell of every month after the window's first, the month's name after it (the full name with the year on the first band and on January, when it fits; else the full name; else the three-letter form), and today's day number lit on or beside the today column; and a day row with day numbers at the cadence the window's scale allows (Mondays at one or two cells per day, the 1st and 15th while those stay at least three cells apart, else the 1st), its label column naming the cadence and the scale (`Mondays · 1 cell = 1 day`; `1st/15th · 2 d/cell` below a 26-cell label) — and shall draw no axis row below the field.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_board.py -k "AT_104 or ruler"`
- **Numeric pass threshold:** oracle board: panel 118×30 → cadence `Mondays`, month row names `September 2026`, `October`, `November`; panel 80×24 → cadence `1st/15th`; `┃` at the cell of every 1st inside the window; today's number `30` within 2 cells of the today column; the label `Mondays · 1 cell = 1 day` / `1st/15th · 2 d/cell`; the last row holds no tick number and no month name; app at terminal 118×30: the panel's rows 1–2 are the ruler; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** months and day numbers at the top; today's date lit; the scale named.
  - **Shipped surface:** `TaskboardApp` key `3`.
  - **Acceptance test(s):** AT-104, AT-112
  - **Boundary catalog (QC-3):** ☑ boundary (each cadence reached by a window of the matching scale; a window crossing a year → `January 2027`; a band too narrow for any name) ☐ empty — N/A: the ruler draws over an empty board as over a full one ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base tree's rows 1–2 are task rows and its last row is the axis → RED.

### HLR-106 — No tick is dropped except under the echo, and no two labels touch
- **Traceability:** US-102
- **Ledger:** LED-2026-10-02-batch-01.6, LED-2026-10-02-batch-01.15
- **Statement:** The day row shall draw every day number its cadence schedules inside the window — except one that overlaps the selection echo or its date labels by one cell or less — each starting on its own cell (ending on it at the right edge), with at least one blank cell between any two labels; with nothing selected, every scheduled number shall be drawn.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_board.py -k no_drop`
- **Numeric pass threshold:** over panel widths 60..160 step 4, one board per (width, scale) built so that each of the five scales is reached (asserted: the set of scales seen == `GANTT_SCALES`, and every arm checks ≥ 1 tick), ticks recomputed independently from the window's days: no selection → drawn == scheduled; a selection → every missing tick overlaps the echo zone (echo cells ± 1); every gap ≥ 1 cell; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the ruler never loses a date it promised, except under the selection's own dates.
  - **Shipped surface:** `TaskboardApp` key `3`, day row; `render_view("gantt", …)` for the sweep.
  - **Acceptance test(s):** AT-104
  - **Boundary catalog (QC-3):** ☑ boundary (a tick at the right edge; today's tick lit; ticks yielding to the echo) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** a tick placement with no gap check → labels touch at 3 days/cell (1st/15th) → RED (P3 mutation).

### HLR-107 — The ruler answers for the selection
- **Traceability:** US-102
- **Ledger:** LED-2026-10-02-batch-01.7, LED-2026-10-02-batch-01.16
- **Statement:** While a task is selected in the gantt, the day row shall bracket its start and due as `⟦━⟧` (a single date as `◆`, an open end as one bracket with `no start · due …` / `starts … · no due`) with its exact dates printed beside the bracket — or, when no slot beside it is free, in the day row's label column in its place, followed by `▸` — in `over` when the task is late and bold `bright` otherwise; and the month row shall mark the selected task's project's committed due date with `◆` in the project's colour, its label column reading `◆ dates · <project>`; with nothing selected the month row's label reads `today <weekday> <month> <day>`.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_board.py -k "AT_105 or echo"`
- **Numeric pass threshold:** oracle board at panel 118×30, `tw3` selected: day row `⟦` at the cell of Sep 24, `⟧` at Sep 28, text `Sep 24` and `Sep 28` beside them; month row `◆` at Oct 10; app: select `tw3` through the keys, then `tm4` → `⟦` no longer at Sep 24, bracket at Oct 10 → Oct 28, `◆` at Nov 4, label `◆ dates · Mobile App`; a fallback case prints the full `<start> → <due>` text untruncated in a 20-cell label; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the selected bar's exact dates read on the ruler and follow the cursor.
  - **Shipped surface:** `TaskboardApp` keys `3`, `down`.
  - **Acceptance test(s):** AT-105
  - **Boundary catalog (QC-3):** ☑ boundary (single-date task → `◆`; no start; no due; no free slot → label column) ☑ empty (no selection → no echo, `today …` label) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** an echo that ignores the selection change keeps `⟦` at Sep 24 → RED (C-10: the AT drives a non-default selection).

### HLR-108 — On the kanban and gantt panels the accent means the edit field and today
- **Traceability:** US-103
- **Ledger:** LED-2026-10-02-batch-01.8, LED-2026-10-02-batch-01.17
- **Statement:** When the kanban or the gantt panel is drawn, the system shall paint `HEX["accent"]` only on the focus role — the `/` filter field — and on today's marks (the today rule, today's number and the no-selection `today …` label), shall draw the view title in bold `bright`, shall keep the selection in reverse video, and shall mark the critical chain by structure — a heavy `━` reach in bold `bright` and a bold `bright` `↳` — with its header count `chain N` in `hd`. The keybar under the panel is outside this requirement.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_colour_budget.py`
- **Numeric pass threshold:** oracle board + one URL card, panel 118×30 and 80×24, kanban (grouped, lanes, matrix × group project, priority, horizon — each pairing asserted reached) and gantt: every accent-painted span is a today mark or inside the filter bar (0 others); the detector is non-vacuous (it finds the today rule on the gantt, and the filter bar when a query is set); the title span is `bright` + bold; the four chain tasks' reach cells are `━` bright bold; app at terminal 118×30 (keys `3`, `4`): the board panel's painted strips carry 0 non-today accent cells; 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** nothing teal on the kanban or gantt panel except today and the filter field.
  - **Shipped surface:** `TaskboardApp` keys `3`, `4`, `/`.
  - **Acceptance test(s):** AT-106
  - **Boundary catalog (QC-3):** ☑ boundary (a filtered view keeps its bar's accent; a board with no chain; a card with a URL; a due in 1..7 days) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base kanban title and `+Nd` tokens are accent → RED.

### HLR-109 — README and RUN.md describe the shipped app
- **Traceability:** US-104
- **Ledger:** LED-2026-10-02-batch-01.9, LED-2026-10-02-batch-01.18
- **Statement:** The repository's `README.md` and `RUN.md` shall describe the app as shipped — its nine views and their keys, `?` as the per-view help, the install from a clone, the data files, team mode, the CLI flags — and shall carry no absolute path into a user's home or a personal drive.
- **Validation:** `test` + `inspection`
- **Executed verification:** `python -m pytest -q tests/test_readme.py`; security-reviewer privacy pass on the doc diff
- **Numeric pass threshold:** 0 matches of one home-path pattern in either file (`[A-Za-z]:[\\/]+Users[\\/]+[^\\/<%~\s]+`, `/(mnt/)?c/Users/`, `/home/<name>`, `/Users/<name>`, `OneDrive`, `My Drive`), placeholders like `<you>` / `%USERPROFILE%` / `~` allowed; every view in `VIEW_ORDER` named with its key from `VIEW_KEYS`; every key in the README's key table bound in `KEYMAP` or a modal's bindings; the `?` row says help; security verdict 0 HIGH; 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the README matches the app and leaks nothing.
  - **Shipped surface:** the files `README.md`, `RUN.md` at the repository root.
  - **Acceptance test(s):** AT-107
  - **Boundary catalog (QC-3):** ☑ invalid (a personal path in any of the listed forms; a stale view count) ☐ empty — N/A ☐ boundary — N/A ☐ error — N/A
  - **Negative control:** the base README carries the personal path 3× and "Four switchable views" → RED.

## 4. Low-level requirements (LLR)

### LLR-101.1 — The fitted axis
- **Traceability:** HLR-101
- **Ledger:** LED-2026-10-02-batch-01.22
- **Statement:** `gantt_axis` (NEW — `taskboard/views.py`) shall return the axis for a field of `field_w` cells holding `[lo, hi]`: `k` = the first of `GANTT_SCALES` (NEW) with `(hi − lo).days + 1 ≤ field_w × k` (else 7); `start = lo − min(spare, (lo − ctx).days)` days with `spare = ⌊field_w × k⌋ − ((hi − lo).days + 1)`; at `k = 7` the start moves back to its Monday and, when that shift would put `hi` past the field's last cell, to `lo`'s Monday instead; a date maps to cell `⌊(d − start).days / k⌋`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k axis` (TC-101)
- **Numeric pass threshold:** one case per scale (5), the spare/context case and the Monday alignment; 0 failures.
- **Negative control:** choosing the largest fitting scale → the 0.5 and 1 cases RED.
- **Boundary catalog:** ☑ boundary (need exactly `field_w × k`) ☑ empty (`lo == hi`) ☐ invalid — N/A ☐ error — N/A

### LLR-101.2 — The window bounds
- **Traceability:** HLR-101
- **Ledger:** none
- **Statement:** The gantt's window shall be `lo = min(open dues ∪ {today}) − 2 days`, `hi = max(open dues ∪ dues of projects with open work ∪ {today}) + 2 days`, `ctx = min(open starts ∪ {lo})`, over the groups the view draws (a project focus or a filter narrows them).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k window` (TC-102)
- **Numeric pass threshold:** oracle board → `lo` Sep 23, `hi` Dec 1; window start Sep 14 at panel 118×30; 0 failures.
- **Negative control:** dropping project dues from `hi` → Data Warehouse's `◆` (Nov 29) leaves the window → RED.
- **Boundary catalog:** ☑ empty (no open work → `[today − 2, today + 2]`) ☐ boundary — covered by LLR-101.1 ☐ invalid — N/A ☐ error — N/A

### LLR-101.3 — The fold rule
- **Traceability:** HLR-102
- **Ledger:** none
- **Statement:** `gantt_plan` (NEW) shall return the groups in draw order with their open and rest tasks, late count and an `unfolded` flag: rows left = body rows − groups; the selected task's group unfolds and spends its open count; each other group, ordered by (−late count, earliest open due), unfolds when it has open work and its open count ≤ rows left (spending it), else is skipped; a render with `height = 0` (unbounded) unfolds every group; heights 1–3 leave a body of 0 rows (header and ruler only).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k fold` (TC-103)
- **Numeric pass threshold:** the two oracle sizes as in HLR-102; the skip-and-continue synthetic board; a late-count tie broken by earliest due; `height = 0` → all unfolded; 0 failures.
- **Negative control:** ordering by +late (fewest first) unfolds Mobile App before API Platform at panel 80×24 → RED.
- **Boundary catalog:** ☑ boundary (selected group alone exceeds the rows; height 0; heights 1–3) ☑ empty (no selection) ☐ invalid — N/A ☐ error — N/A

### LLR-101.4 — The due chip
- **Traceability:** HLR-103
- **Ledger:** none
- **Statement:** `gantt_due_chip` (NEW) shall return exactly `width` cells, right-aligned: `▲Nd` / `over` (due before today), `today` / `soon`, `<Mon> <day>` (`Oct 6`, no zero-padding) / `mut` (later), `no due` / `dim` (none or unparsable); a project's chip shows its committed due the same way while it holds open work and is blank otherwise.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k chip` (TC-104)
- **Numeric pass threshold:** the four forms; width exact for widths 6 and 7; 0 failures.
- **Negative control:** `▲Nd` for a future date → RED.
- **Boundary catalog:** ☑ boundary (due == today) ☑ empty (no due) ☑ invalid (unparsable due) ☐ error — N/A

### LLR-101.5 — The dependency gutter
- **Traceability:** HLR-103, HLR-108
- **Ledger:** none
- **Statement:** `gantt_dep_mark` (NEW) shall return `↳` in `over` when the task has a start date earlier than the latest due date of its open dependencies, bold `bright` when the task is on `critical_chain`, `mut` otherwise, and a blank when every dependency is done or missing; the renderer shall place it at column `label_w` of the row.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k gutter` (TC-105)
- **Numeric pass threshold:** the four outcomes plus the no-start case; on the oracle board 7 drawn marks at column 30; 0 failures.
- **Negative control:** marking done dependencies → `tw4` keeps its mark when `tw2` is done → RED.
- **Boundary catalog:** ☑ boundary (dependency due == start → not `over`; no start → never `over`) ☑ empty (no dependency) ☑ invalid (an unknown dependency id counts as missing) ☐ error — N/A

### LLR-101.6 — One seat for draw order and nav order
- **Traceability:** HLR-104
- **Ledger:** LED-2026-10-02-batch-01.23
- **Statement:** `render_gantt` and the gantt branch of `nav_model` shall both read `gantt_plan`; `nav_model` shall return the open task ids of every group in its order; the renderer shall draw a group taller than the rows left as the page (`index // rows_left`) of its open tasks holding the selected task, with its `N open` count on the span row; when the span rows fill the body — more groups than body rows, or exactly as many while an open task is selected — it shall draw the page (`index // (body − 2)`) of `body − 2` consecutive groups that holds the selected group (the selected group's span row followed by the selected task's row) and `+N not shown` for the rest; a body of one row draws only the selected task's row, of two rows its span row and its row; a selected rest-work task in a group whose open rows have no room draws no task row (the group shows its `N open`).
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k nav` (TC-106)
- **Numeric pass threshold:** nav == concatenated open ids of the plan's groups; for every open id selected in turn at panel 80×24 the id is in `line_map`; on a 30-task project page boundaries move the rows once per page; on a 30-project board the selected last-project task is in `line_map`; 0 failures.
- **Negative control:** nav including rest work → done ids appear → RED.
- **Boundary catalog:** ☑ boundary (30-task project; 30-project board) ☑ empty (no open tasks) ☐ invalid — N/A ☐ error — N/A

### LLR-101.7 — The shipped motion rides the fitted axis
- **Traceability:** HLR-101
- **Ledger:** LED-2026-10-02-batch-01.30
- **Statement:** On the fitted axis the gantt shall keep its two shipped motions: the flow packet (`▬`, `bright`) crossing an in-progress task's reach one cell per tick, and the progress dot breathing (`PULSE_PHASES`) only on a project whose work sits left of today on its span; on a critical-chain reach the packet's glyph differs from the reach glyph, and the packet never covers the `◂` of a reach that began before the window.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_flow.py tests/test_motion.py -k gantt` (TC-107)
- **Numeric pass threshold:** the existing motion laws green on the new renderer; 0 failures.
- **Negative control:** tick ignored → the frames for tick 0..3 are identical → RED.
- **Boundary catalog:** ☑ boundary (blocked / done / first-phase task: no packet) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-101.8 — Board text is never parsed as markup in the gantt's seats
- **Traceability:** HLR-101, HLR-107
- **Ledger:** none
- **Statement:** Every project name and task title the gantt draws — span labels, task labels, the focus label in the header, the month row's project label, the echo — shall be fitted or clipped on plain text first, then passed through `rich.markup.escape`, then wrapped in style (never `fit(escape(…))`), so a name holding `[`, `]` or a trailing `\` is painted literally.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k hostile` (TC-108)
- **Numeric pass threshold:** payloads `[bold]x`, `[/]`, `a[b`, `[link=http://e]y[/link]`, `x\`, and a 40-character name with `[b]` at the clip column — each as a project name and as a task title, the task selected and not selected, and the project focused (header): the render succeeds and the plain text holds the payload, or for a clipped seat its fitted prefix followed by `…`; 0 failures.
- **Negative control:** the base tree's focused header with project `[/]` raises `MarkupError` (S-1, reproduced) → RED.
- **Boundary catalog:** ☑ invalid (markup-shaped names, trailing backslash, a tag at the clip column) ☐ empty — N/A ☐ boundary — N/A ☐ error — N/A

### LLR-101.9 — The app keeps the gantt's selection on drawn open work
- **Traceability:** HLR-104
- **Ledger:** none
- **Statement:** `TaskboardApp._select_first` (`taskboard/app.py`) shall, in the gantt, keep the selection when it is in the gantt's nav order and otherwise select the neighbour it had in its group's draw order — the group's open tasks with the selected task re-inserted by `sort_by_due` order: the one after it, else the one before it — else the first id of the order, else nothing.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k AT_108` (TC-109)
- **Numeric pass threshold:** per HLR-104's entry and `]` arms; 0 failures.
- **Negative control:** the base `_select_first` keeps `tw1` → `down` does nothing → RED.
- **Boundary catalog:** ☑ boundary (the group's last open task becomes done → first open task elsewhere) ☑ empty (no open work → nothing selected) ☐ invalid — N/A ☐ error — N/A

### LLR-101.10 — Columns and vertical split
- **Traceability:** HLR-101, HLR-105
- **Ledger:** LED-2026-10-02-batch-01.31
- **Statement:** `gantt_columns` (NEW) shall give label 30 / chip 7 cells at panel width ≥ 100, label 20 / chip 6 at ≥ 60, and below 60 a label of `max(6, width // 3)` with a 6-cell chip from width 40 (none below); every row shall be label + gutter (1) + field + (space + chip) = width exactly; the body shall be `height − 3` rows (header + two ruler rows); the day row's scale label shall fit its column whole (`.5 d/cell` at half a day per cell below 26 cells); the in-view legend row shall be drawn only when a row is spare after the body, never at the cost of an unfold, naming only marks the frame draws.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k columns` (TC-110)
- **Numeric pass threshold:** every rendered row exactly `width` cells for widths 24..160; oracle board panel 118×30 → 26 body rows + legend; panel 80×24 → 21 body rows, no legend; 0 failures.
- **Negative control:** a chip one cell wider than its column → rows of `width + 1` → RED.
- **Boundary catalog:** ☑ boundary (widths 24, 39, 40, 59, 60, 99, 100) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-101.11 — Group label forms
- **Traceability:** HLR-102
- **Ledger:** LED-2026-10-02-batch-01.24
- **Statement:** A group's span label shall be `▾ ` (unfolded) or `▸ ` (folded) in its colour, the name bold in its colour fitted to the cells left, then the counts: at a label ≥ 26 cells `N open` (folded or paged), `▲n`, `✓n`; below 26 `N` (folded or paged) and `▲n`; a label too narrow for its counts sheds `✓n`, then `▲n`, then `N`, so the label stays its width; the Inbox is named `Inbox` in `dim`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k label` (TC-111)
- **Numeric pass threshold:** the oracle strings of HLR-102 at both sizes; 0 failures.
- **Negative control:** `✓n` kept below 26 cells → the 80×24 string differs → RED.
- **Boundary catalog:** ☑ boundary (label 25 vs 26) ☑ empty (Inbox) ☐ invalid — N/A ☐ error — N/A

### LLR-102.1 — The cadence rule
- **Traceability:** HLR-105, HLR-106
- **Ledger:** none
- **Statement:** `gantt_cadence` (NEW) shall return `daily` at ≥ 3 cells per day, `Mondays` at ≥ 1, `1st/15th` when every gap between consecutive 1st/15th ticks in the window is ≥ 3 cells, else `1st`, with the ticks `(date, cell)` of every window day the cadence keeps. (No shipped scale gives ≥ 3 cells per day, so `daily` is reached only by a synthetic axis.)
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k cadence` (TC-112)
- **Numeric pass threshold:** k = 0.5 → `Mondays`; k = 1 → `Mondays`; k = 2, 3 → `1st/15th`; k = 7 → `1st`; a synthetic k = 1/3 → `daily`; 0 failures.
- **Negative control:** `>= 1` written `> 1` → k = 1 becomes `1st/15th` → RED.
- **Boundary catalog:** ☑ boundary (each threshold) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-102.2 — The day row
- **Traceability:** HLR-105, HLR-106, HLR-107
- **Ledger:** none
- **Statement:** The day row shall place, in this order, the echo (LLR-102.4), then each tick label at its cell (or ending at the right edge) only where it and one blank cell either side are free; where the today column is blank it shall continue the today rule, and a tick covering today shall be lit; week guides `┆` (the field's) shall fill empty cells not beside a label; its label column shall name the cadence and the scale, or carry the echo's full text in its fallback.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k "no_drop or ruler"` (TC-113)
- **Numeric pass threshold:** per HLR-105 and HLR-106; 0 failures.
- **Negative control:** gap 0 instead of 1 → labels touch → RED.
- **Boundary catalog:** ☑ boundary (right edge; echo fallback) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-102.3 — The month row
- **Traceability:** HLR-105, HLR-107
- **Ledger:** none
- **Statement:** The month row shall draw `┃` (`frame`) on each month's first cell after the window's first, then the project marks (never covered), then today's number in reverse bold accent at the first free of: the today column, ending on it, right of it, left of it; then each band's name — full with the year on the first band and on January, full, then three-letter — in the first free run of its band, `ink` for today's month and `hd` otherwise; its label column shall read `◆ dates · <project>` for a selection and `today <weekday> <month> <day>` otherwise.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k ruler` (TC-114)
- **Numeric pass threshold:** per HLR-105; every band at least 4 cells wide carries its name; 0 failures.
- **Negative control:** marks placed after the names → a name covers the `◆` → RED.
- **Boundary catalog:** ☑ boundary (a 2-cell band: no name fits) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-102.4 — The echo
- **Traceability:** HLR-107
- **Ledger:** none
- **Statement:** `gantt_echo` (NEW) shall return, for the selected task, the bracket cells, its tone and the label options in preference order — `<start>` left and `<due>` right; both left; both right — with exact dates (`Sep 24`), the joined form shortening the second date to its day when both share a month (`Sep 24–28`), and the full text `<start> → <due>` for the label-column fallback.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_board.py -k echo` (TC-115)
- **Numeric pass threshold:** the four task shapes (both dates, single date, no start, no due); 0 failures.
- **Negative control:** cell-rounded dates instead of exact ones → `Sep 24` wrong at k = 2 → RED.
- **Boundary catalog:** ☑ boundary (bracket clipped at an edge) ☑ empty (no dates → no echo) ☐ invalid — N/A ☐ error — N/A

### LLR-102.5 — Legend and help say what the gantt draws
- **Traceability:** HLR-105, HLR-102, HLR-103
- **Ledger:** LED-2026-10-02-batch-01.25, LED-2026-10-02-batch-01.29
- **Statement:** The gantt's `legend_entries` shall be asked of the frame the screen shows — the same selection, archive toggle, focus and panel size (`legend_entries(..., selected_id=, gantt_focus=)`, threaded through `HelpModal` from the app) — and shall name, each only while that frame draws it, the span, progress dot, committed `◆`, today, week guide, task reach, critical `━`, `↳` (waits / starts early), the fold marks and `✓n`, `◂▸`, the ruler's month `┃` and the echo `⟦━⟧`, and shall no longer name the bottom axis or the due meter; the gantt help usage and example shall describe the fitted, folded board and the ruler, each line whole in the help column (44 cells after its bullet).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_legend.py tests/test_gantt_board.py -k legend` (TC-116)
- **Numeric pass threshold:** the existing no-ghost law green over the gantt; the `┃` and `⟦` entries present on the oracle board with a selection; 0 failures.
- **Negative control:** keeping the meter entries → ghost marks → RED (existing law).
- **Boundary catalog:** ☑ empty (no selection → no echo entry) ☐ boundary — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-103.1 — Kanban and gantt titles
- **Traceability:** HLR-108
- **Ledger:** none
- **Statement:** The kanban (grouped, lanes, matrix) and gantt header titles shall be drawn bold in `bright`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_colour_budget.py -k title` (TC-117)
- **Numeric pass threshold:** 4 title spans styled `bright` + bold; 0 failures.
- **Negative control:** base accent title → RED.
- **Boundary catalog:** none — one style read-back per title

### LLR-103.2 — The critical chain as structure
- **Traceability:** HLR-108
- **Ledger:** none
- **Statement:** The gantt shall draw a critical-chain task's reach with `━` in bold `bright` (its phase tip in the same style) and its header count as `chain N` in `hd`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_colour_budget.py -k chain` (TC-118)
- **Numeric pass threshold:** oracle board: every in-window reach cell of `tm2..tm5` is `━` bright bold, except a packet cell; header text `chain 4`; 0 accent cells on them; 0 failures.
- **Negative control:** accent chain tone → RED.
- **Boundary catalog:** ☑ empty (no chain → no `━`, no `chain` count) ☐ boundary — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-103.3 — The kanban's other accent sites
- **Traceability:** HLR-108
- **Ledger:** none
- **Statement:** The kanban's horizon group "This week" shall wear `hd`, the matrix percent `hd`, the card's `↗` link token (`card_cell`) `mut`, and the relative-due token within seven days (`reldue_token`) `mut`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_colour_budget.py -k kanban` (TC-119)
- **Numeric pass threshold:** the accent census of HLR-108 over every kanban presentation × group mode, plus the Focus review rail, People and Agenda arms for the two shared tokens; 0 failures.
- **Negative control:** any one site reverted to accent → its arm RED.
- **Boundary catalog:** ☑ boundary (a card with a URL; a due in 1..7 days) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-104.1 — README content
- **Traceability:** HLR-109
- **Ledger:** none
- **Statement:** `README.md` shall follow the audit's outline (`README-AUDIT.md` §Proposed outline), state each fact as re-read from the code at writing time, install from `git clone https://github.com/jav201/taskboard.git`, and name each view with its key from `VIEW_KEYS`.
- **Validation:** `test` + `inspection`
- **Executed verification:** `pytest tests/test_readme.py` (TC-120); security-reviewer diff pass
- **Numeric pass threshold:** per HLR-109; security verdict with 0 HIGH.
- **Negative control:** base README → RED.
- **Boundary catalog:** ☑ invalid (personal path) ☐ empty — N/A ☐ boundary — N/A ☐ error — N/A

### LLR-104.2 — RUN.md content
- **Traceability:** HLR-109
- **Ledger:** none
- **Statement:** `RUN.md` shall give the run/test/develop commands relative to a clone, name no `6` view key and no retired worktree flow, and carry no personal path.
- **Validation:** `test` + `inspection`
- **Executed verification:** `pytest tests/test_readme.py -k run_md` (TC-121)
- **Numeric pass threshold:** 0 matches of HLR-109's home-path pattern (the same regex object `tests/test_readme.py` uses for `README.md`); no `6` view key; 0 failures.
- **Negative control:** base RUN.md (personal path, key `6`) → RED.
- **Boundary catalog:** ☑ invalid (personal path) ☐ empty — N/A ☐ boundary — N/A ☐ error — N/A

## 4b. Information Flow Contract (IFC)

Part A (always) and Part B: the gantt is a panel whose task rows a consumer addresses by row
index (`line_map`), so its addressable outputs are declared.

```
FLOW: gantt-board
  SOURCE : Board (projects, tasks, critical_chain) + selected_id + today + panel width/height
  NODES  :
    - fn    : gantt_plan
      owner : LLR-101.3
      in    : board, show_archived, selected_id, today, body rows, focus
      out   : groups in draw order (open, rest, late, unfolded)
    - fn    : gantt_axis
      owner : LLR-101.1
      in    : field_w, today, lo, hi, ctx
      out   : axis (start, k, cell mapping)
    - fn    : gantt_columns
      owner : LLR-101.10
      in    : panel width
      out   : label_w, chip_w, field_w
    - fn    : gantt_cadence
      owner : LLR-102.1
      in    : axis
      out   : cadence name + ticks
    - fn    : gantt_echo
      owner : LLR-102.4
      in    : selected task, axis
      out   : bracket cells + label options
    - fn    : gantt_due_chip
      owner : LLR-101.4
      in    : due date, today, width
      out   : chip markup
    - fn    : gantt_dep_mark
      owner : LLR-101.5
      in    : task, board, chain
      out   : one-cell gutter markup
    - fn    : render_gantt
      owner : LLR-101.6
      in    : the nodes above
      out   : rich Text + line_map
    - fn    : _select_first
      owner : LLR-101.9
      in    : nav order, selected id
      out   : selected id on drawn open work
  SINK   : BoardView (app.py refresh_view / _repaint_flow) and nav_model's gantt branch
```

```
COMPONENT: gantt-panel
  PARENT : SYSTEM
  SURFACE: gantt view (key 3)
  INPUTS : board: Board ; selected_id: str ; width: int ; height: int
  OUTPUTS:
    - id          : task-rows
      value       : one row per drawn open task
      address     : line_map[task_id] = row index in the rendered Text (header 0, ruler 1-2, body from 3; under a / filter render_view inserts the 2-row filter bar under the header, so ruler 3-4 and body from 5)
      cardinality : drawn open tasks (<= height - 3)
      consumers   : taskboard/app.py::_scroll_selected_into_view ; taskboard/views.py::render_view
      owner       : LLR-101.6
    - id          : nav-order
      value       : open task ids in draw order
      address     : nav_model("gantt", ...)[0], INDEXED POSITIONALLY
      cardinality : open tasks of the drawn groups
      consumers   : taskboard/app.py::_nav_columns ; taskboard/app.py::_select_first
      owner       : LLR-101.6
```

## 5. Validation strategy
Layer A (`TC-101` through `TC-121`, one per LLR as named above) and Layer B (`AT-101`
through `AT-113`, one node each — C-18; the two size arms of AT-101 and AT-102 are one parametrised node) are pytest nodes in `tests/test_gantt_board.py`, `tests/test_colour_budget.py`
and `tests/test_readme.py` (NEW — created in Phase 3; node ids provisional until P3, V-5),
each carrying its id in its docstring. The oracle board is `tests/kg_board.py`. ATs drive
`TaskboardApp` through `App.run_test()` at named terminal sizes and read the painted board
panel; TCs drive `render_view` / the helpers at panel sizes. Captures (SVG + text, 118×30
and 80×24 panels) of the gantt and kanban are produced from `tests/kg_board.py` only — never
from `~/.taskboard` — into `evidence/`, and `tools/privacy_sweep.py` runs over `evidence/`
at each increment gate and at close, together with HLR-109's home-path pattern grepped over
the whole batch folder (0 hits outside the word-only premise lines; security N-1). Full suite `python -m pytest -q` at close; base 1535
passed.

| AT | Story | Drives |
|---|---|---|
| AT-101 | US-101 | key `3` at terminal 118×30 and 80×24: every project painted, no `not shown`, folds as HLR-102 |
| AT-102 | US-101 | key `3` then `down` ×25: the selection painted in reverse inside the viewport after each key; end no-op |
| AT-103 | US-101 | key `3`: chips and `↳` gutter read off the painted rows |
| AT-104 | US-102 | key `3`: rows 1–2 are the ruler; cadence label; no bottom axis; no-drop over the painted day row |
| AT-105 | US-102 | keys to `tw3`, then to `tm4`: the echo and `◆` follow |
| AT-106 | US-103 | keys `3`, `4`, `/`: painted accent cells are today marks or the filter bar only |
| AT-107 | US-104 | the files `README.md`, `RUN.md` |
| AT-108 | US-101 | enter the gantt on a done selection: it lands on drawn open work; `down` moves |
| AT-109 | US-101 | `v` (show archived): `✓n` grows, no archived row |
| AT-110 | US-101 | `F` (focus): one group, its own window |
| AT-111 | US-101 | `/` (filter): nav follows the filtered board, the ruler under the bar |
| AT-112 | US-102 | `?` under a `/` filter: the legend describes the filtered frame |
| AT-113 | US-101 | `]` to done: the cursor moves one row; one more `]` stays local |

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new test that asserts NEW behaviour shown RED on the base tree; preservation laws (motion, legend no-ghost, width exactness) green on the new renderer.
- each node of §6.6 dispositioned as listed there: rewritten in place with the HLR that supersedes it, or kept green by the code.
- full suite: 0 failures.

## 6. Appendices

### 6.1 Verification beyond automation (UX-14)
- automated walkthrough: AT-102, AT-108 (keys through the real app) — `planned`.
- expert inspection: ux-reviewer on the 118×30 / 80×24 captures at P4 — `planned`.
- user evaluation: the operator's own reading of the captures — `planned` (outside this batch; he judges TUI work on real renders).

### 6.2 Relevant design decisions
- D1: Scope = Batch A1 (gantt G-A + AX-2, colour budget on kanban/gantt, README/RUN.md); K-A + R-1b = Batch A2, BACKLOG (pre-authorized split; evidence in US-105).
- D2: Rest work (done or archived) never draws a gantt row and is not navigable there; it is counted as `✓n` on its group's span row (G-A: "done folds to ✓n"). Archived tasks count only when `v` shows them.
- D3: The shipped motions (flow packet, behind-schedule pulse) are kept on the fitted axis — the verdict frames are stills and say nothing against them.
- D4: Today keeps the accent (the rule, today's number, the no-selection `today …` label); the selection keeps reverse video. **Operator question (UX-7):** today in accent or a quieter tone, and should the selection take the accent?
- D5: Weekend shading (round-5 frames) is not shipped: it is not in the commission's AX-2 list and needs a background hex outside the palette — BACKLOG.
- D6: The Inbox (tasks without a project) is a group named `Inbox`, dim, with no span, after the projects, hidden under a project focus (the shipped "the inbox is not lost" law).
- D7: The project focus (`F`) keeps narrowing the gantt to one group, the header keeps its shipped `(focused: <name>)` wording, and the window fits that group.
- D8: When the span rows alone exceed the body, the run of groups holding the selection is drawn and the last row says `+N not shown` (LLR-101.6).
- D9: A selected group taller than the rows left draws the page of its open tasks holding the selection and keeps `N open`. **Operator question (UX-9):** an above/below hint for a paged group (none drawn — no frame covers it).
- D10: The colour budget's scope is the kanban and gantt panels plus the two shared helpers they paint cards with (`card_cell`'s `↗`, `reldue_token`'s ≤7-day tone — which the Focus rail, People and Agenda also call); other views' titles, the keybar hints, the ribbon clock and the setup hints are BACKLOG (the commission's fallback). **Operator question (UX-6):** a title colour that differs per view until the app-wide pass — acceptable for one batch?
- D11: "This week" in the horizon grouping takes `hd`, the neutral header ink (UX-12): the budget gives no hue to a non-focus group.
- D12: View text follows the verdict frames (`chain 4`, `past due`); the help modal's prose stays Spanish like the rest of `help_usage`. **Operator question (UX-12):** the gantt header in English beside Spanish help prose.
- D14: When `]` finishes the selected task it leaves the gantt (folded into `✓n`) and the cursor moves one row (UX-15); no extra cue is drawn. **Operator question (ux iteration 2):** a cue (e.g. a toast) when a finished task leaves the gantt — no prototype covers it.
- D13: The `━` glyph means both the critical chain (field) and the selection echo (ruler) — both approved frames use it. **Operator question (UX-11b).**

### 6.3 Open risks
- `k = 0.5` cannot reach the `daily` cadence (2 cells/day): at that scale the ruler shows Mondays — the rule as stated, measured.
- The app's painted panel is shorter than the terminal: fold outcomes asserted at panel sizes may differ at the same terminal size; ATs assert relative properties (all projects painted, selection visible), TCs the exact frames.

### 6.4 Security questions (scan `devflow-scan-spec.py`: `security_required: true`, flags `token`, `role`, `form`)
- The three flags are vocabulary hits — "token" (the relative-due token, a badge token), "role" (the accent's focus role), "form" (the form of a date label); this batch adds no credential, auth, network, storage or input surface.
- Real surfaces, answered: (1) **markup over file-derived text (C-17)** — LLR-101.8, with the header focus label (S-1, a live `MarkupError` on the base tree) and the fit-then-escape order (S-2). (2) **privacy of the docs** — LLR-104.1/104.2 and one home-path pattern (S-4). (3) **evidence and record hygiene** — transcripts and the batch record are written with home paths redacted (S-3, `p0-probes.txt`, `base-suite.txt`, `PLAN.md`); captures come from `tests/kg_board.py` only and `tools/privacy_sweep.py` runs over `evidence/` (S-6). (4) The username path already public in older tracked files (S-5) is an accepted, recorded risk — BACKLOG.

### 6.6 Reverse census — existing nodes the batch changes (C-26, measured: P-10)

The measured table (31 nodes in 7 files, each with the law it guarded and its disposition)
is the increment-001 packet's `Reverse census` section, where the rewrites it describes were
made: `03-increments/increment-001.md` §4 *Reverse census table*.

### 6.5 Requirement amendments (Before / After · Deleted / New)
- P4 → P3 `iterate-to-fix` (increment 004): AT registry re-cut so each AT is one node (qa G-001, C-18/C-21: AT-108 split into AT-108 and AT-113; AT-109 into AT-109 through AT-112) — LED .26, .27, .28; LLR-102.5 help lines fit the column (ux UXV-1, LED .29); LLR-101.7 the packet clears `◂` (UXV-5, LED .30); LLR-101.10 the scale label fits (UXV-6, LED .31). Parent HLRs re-read: unchanged in substance. RED for each new node: `evidence/inc004-red.txt`.
- P3 increment 001, code review (`03-increments/increment-001.md` §4b): LLR-101.1 (F6, LED .22) · LLR-101.6 (F1, F2, LED .23) · LLR-101.11 (F4, LED .24) · LLR-102.5 (F3, LED .25). Before / After text in each ledger entry; parent HLRs re-read (HLR-101, HLR-104, HLR-102, HLR-105): unchanged; TCs re-derived: TC-101, TC-106, TC-110, TC-116 each gained the node that went RED on the frozen pre-review snapshot (`evidence/inc001-review-red.txt`).
