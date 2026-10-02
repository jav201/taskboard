# Requirements Document — taskboard — Batch 2026-10-02-batch-02

> Live contract (current state only). Mode `core`. Language `en`. The append-only ledger is
> `01-requirements-ledger.md`. Template: flow `templates/req-template.md` (reserved field
> names kept literal). Ids use a batch-disjoint `2xx` range (`US-201`, `HLR-201`,
> `LLR-201.1`, `AT-201`, `TC-201`): `0xx` and `1xx` are taken in the record and the canon.

## 1. Introduction

### 1.1 Purpose
Batch P (polish): fold the operator's twelve answers to the questions batch
`2026-10-02-batch-01` carried (`evidence/taskboard-respuestas-a1.json`, exported
2026-10-02 — the requirements source) into the shipped app, and carry the round-7 colour
budget (accent = what is being operated on, plus today; critical = structure) to every view,
the key bar, the ribbon and the dialogs.

### 1.2 Scope
In: the titles and non-focus accent marks of the seven views batch-01 left (lanes, agenda,
focus, flow, standup, people, setup) and their legend swatches; the key bar (`keymap.py`); the
ribbon clocks (`ribbon.py`); the modal titles and help headings (`taskboard.tcss`, the
`HelpScreen` key map in `app.py`); Setup's row styling (its chips and marks are painted plain
today, UX-1); the ≤7-day relative-due tone;
the gantt flow packet's tone; every Spanish string the app paints; the gantt's paged-group
hint, its finish toast, its fold order (the previous project sticky, urgent work last), weekend
shading and the echo's clip arrows (UXV-7).
Out: everything else in `BACKLOG.md` — Batch A2 (K-A + R-1b), the help modal's right-column
layout, `_strip` F5, Setup's sync interval, screenshots, the privacy tools' entity decoding.
Other ways a task finishes (the editor, `x`, `X`) post no toast (UX-6). No new key, no model
field, no new dependency.

### 1.3 Definitions
| Term | Definition |
|------|------------|
| focus role | what the accent may paint: today's marks (a today rule, today's date or number, the word `today` where a view already paints it in accent, a mark drawn because its date is today), the field being edited (the `/` filter bar, a focused input's border), and the cursor mark of a list (the Focus review rail's `▸`, Setup's `>`). The selection itself stays reverse video (D4) |
| urgent group | a gantt group holding an open task due today or earlier |
| previous group | the gantt group the selection was in before its current group (UX-4: only that one is sticky) |
| urgency weight | a gantt group's open tasks due today or earlier |
| paged group | a gantt group drawn as one page of its open tasks because they do not all fit (batch-01 D9) |
| panel / terminal size | `render_*` takes the panel's size; the app's terminal is 2 rows taller (ribbon + key bar). ATs name terminal sizes, TCs panel sizes |

### 1.4 References
Answers: `evidence/taskboard-respuestas-a1.json`. Context: `BACKLOG.md` entries "Colour budget,
app-wide", "Operator questions, gantt", "Weekend shading", "P4 walkthrough", UXV-7, UXV-9;
`2026-10-02-batch-01/01-requirements.md` §6.2 D4–D14 and `04-validation.md` UXV-*. Prototypes
(worktree `kg-mejoras`, `prototypes/kg_mejoras/`): `variants_polish.py` `BUDGET`,
`variants_round5.py` `weekend_cols` / `WEEKEND_BG`, `build_questions.py` (each question's
options as shown to the operator). Oracle board: `tests/kg_board.py`.

## 2. Overall description

### 2.1 Product perspective
Textual TUI (`textual 8.2.8`, `rich 15.0.0`). Views render rich markup through `render_view`;
the key bar is generated from `KEYMAP`; the ribbon is one `Static`; modal styling lives in
`taskboard.tcss`.

### 2.3 User characteristics
One owner-operator (Javier), keyboard-first, Windows Terminal from 80×24 to full screen,
judges TUI work on real renders; Windows Terminal renders truecolor, while the commission
asks every new background to survive 256-colour quantisation as well (UX-10). Context of use: the daily read of every view; the weekly
re-plan in the gantt (walk with `j`/`↓`, finish with `]`).

### 2.4 Constraints
≤ 4 SOURCE files per increment; no new dependency; `render_view`, `nav_model`,
`legend_entries` keyword contracts are consumed by `app.py`, `modals.py` and the tests; new
keywords are optional with the shipped default.

### 2.5 Assumptions
- A1: the oracle board (`tests/kg_board.py`) plus a scratch team directory and history file
  is the census board; renders of it are the evidence (captures 118×30 and 80×24).
- A2: 256-colour quantisation is rich's `Color.downgrade(ColorSystem.EIGHT_BIT)`, the mapping
  the app's renderer uses.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-201 | As the board owner, I want the accent on every view, the key bar, the ribbon and the dialogs to mean only what I am operating on and today, with soon-due work in amber and the moving packet quiet, so that teal points at one thing wherever I look. | answers D10 "soon" (commission: now), HELP "bright", SOON "amber", PKT "dim", D4 "keep"; BACKLOG UXV-9 | READY |
| US-202 | As the board owner, I want every word the app shows in English, the help included, so that the screen reads in one language. | answer D12 "en" | READY |
| US-203 | As the board owner, I want the gantt to tell me what it is not showing — tasks above or below a paged project, and a task that just finished and left — so that nothing disappears silently. | answers D9 "hint", D14 "toast" | READY |
| US-204 | As the board owner, I want the project I just left to stay open while it fits, and projects with work due today or late to fold last, so that the highlight moves as little as possible and urgent work stays on screen. | answers UXV-2 "sticky", UXV-3 "yes" | READY |
| US-205 | As the board owner, I want weekends shaded on the gantt field when a cell is at most a day, and the ruler's echo to show a clip arrow where the task runs past the window, so that I can read the calendar and the dates honestly. | answer D5 "ship"; BACKLOG UXV-7 | READY |

#### Refinement log

**US-201 — colour budget, app-wide**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ (two increments: panels, then chrome) · T ✓
- **Functionality:** accent census over every view's rendered spans, the key bar, the ribbon and the modal CSS; out of scope: the HTML report (`report.py`), the task editor's focus bars (already focus role).
- **Evaluability:** collect accent-painted runs across 9 views × presentations; each is a focus-role mark; key bar and ribbon carry no accent; modal titles bold bright.
- **Classification:** READY.

**US-202 — English**
- **INVEST:** all ✓. Census of string literals (P-3: 176 hits over 5 files, many internal keys).
- **Evaluability:** the help modal, the flow view, Setup and the team filter render without Spanish words; internal keys (`todo`/`equipo`/`personal`, check keys) unchanged.
- **Classification:** READY.

**US-203 — what the gantt is not showing**
- **INVEST:** all ✓; D14 depends on `]` (shipped).
- **Evaluability:** a 30-task project at terminal 80×24 shows `▼ N below` / `▲ N above`; `]` finishing `tw2` posts a toast naming it and `✓2`.
- **Classification:** READY.

**US-204 — fold order**
- **INVEST:** all ✓. Feasibility: the visited order is app state passed to `gantt_plan`.
- **Evaluability:** walking from Website Redesign into Mobile App at terminal 80×24 keeps Website unfolded (base folds it, P-7); at terminal 80×24 Ops & Security, holding the only task due today, unfolds (P-6).
- **Classification:** READY.

**US-205 — weekend shading and clip arrows**
- **INVEST:** all ✓. The prototype's `#161d27` quantises to the field background (P-4), so the hex is re-chosen and measured.
- **Classification:** READY.

**Not a story — D13** (`━` shared by the chain and the echo): answer "keep" — no change (decision D-202).

### 2.7 Premise evaluation (C-43)

| # | Premise | Tier | Verdict | Executed evidence | Disposition |
|---|---|---|---|---|---|
| P-1 | Besides today's marks, the accent paints the titles of lanes, agenda, focus, flow, standup, people; Setup's section names and hint keys; the operator spine `▌`; the team filter's active segment; the agenda status `◐`; the flow throughput bar; and the matching legend swatches | premise | ✅ TRUE | `evidence/p0-probes.txt` §P-1 (census over rendered spans, 118×30) | HLR-201 |
| P-2 | The key bar paints keys in accent (primary) or in eight group hues (more); the ribbon paints its clocks in accent; `.modal-title` is `#2dd4bf`; `HelpScreen` writes `#2dd4bf` twice; the palette input's focus border is accent | premise | ✅ TRUE | `p0-probes.txt` §P-2 | HLR-202 |
| P-3 | The app paints Spanish in the help modal (headings, usage, example, footer), the flow view, Setup and the team filter labels | premise | ✅ TRUE | `p0-probes.txt` §P-3: AST census, 176 literals in `app.py` 13, `keymap.py` 1, `modals.py` 6, `team_sync.py` 31, `views.py` 125 (internal keys and English false positives included — sorted at P3) | HLR-204 |
| P-4 | The prototype's weekend background `#161d27` and the field background `#0d1117` quantise to the same 256-colour index (16); `#1a1d22` quantises to 234 | premise | ✅ TRUE | `p0-probes.txt` §P-4 | LLR-209.1 |
| P-5 | A 30-task project at panel 80×24 draws 20 of its rows and no above/below hint | premise | ✅ TRUE | `p0-probes.txt` §P-5 | HLR-205 |
| P-6 | At panel 80×22 (terminal 80×24) Ops & Security folds while holding the only task due today | premise | ✅ TRUE | `p0-probes.txt` §P-6 (`to3`, late 1) | HLR-208 |
| P-7 | Walking `down` through the gantt at panel 80×22 moves the highlight up on 3 steps (`tm6`, `td2`, `to1`) | premise | ✅ TRUE | `p0-probes.txt` §P-7 | HLR-207 |
| P-8 | The flow packet is `bright` (`#e6edf7`, the chain's tone) and `reldue_token` gives `+4d` in `mut` | premise | ✅ TRUE | `p0-probes.txt` §P-8 | HLR-203 |
| P-9 | Selecting `tw2` (start Sep 5, before the window) draws `⟦` on the day row's first cell with no `◂` | premise | ✅ TRUE | `p0-probes.txt` §P-9 | HLR-210 |
| P-10 | `]` finishing `tw2` in the gantt posts no notification | premise | ✅ TRUE | `p0-probes.txt` §P-10 | HLR-206 |
| P-11 | Base suite is green | premise | ✅ TRUE | `python -m pytest -q -p no:cacheprovider` at `a0e7d9a` → 1611 passed in 176.37 s (`evidence/base-suite.txt`) | — |
| P-12 | Under the iteration-2 fold order (previous group sticky; weight, then due-today count, then earliest due) the oracle walk moves the highlight up on 2 steps at panel 80×22 (`ta1`, `td2`; base 3) and 1 at 118×28 (`ta1`; base 1), and the 80×22 entry frame unfolds Website Redesign, Data Warehouse and Ops & Security | premise | ✅ TRUE | C-39 pre-execution: `evidence/p1-fold-simulation.txt` row `iter2_prev1_today` | HLR-207, HLR-208 thresholds |
| P-13 | `render_setup` paints its body rows with no style spans: each row is built from `str()` of styled `Text`, which drops the styles (the `>` cursor, the on/off chips, the check marks) | premise | ✅ TRUE | ux-reviewer span dump of `render_view("setup")` 118×30 (P2 UX-1); `views.py` `render_setup.row` | LLR-201.3 |
| P-14 | `HEAT` (`views.py`, the only `week ▒ accent` table) has no reader; `due_meter` paints today in accent and every later day in `mut` | premise | ✅ TRUE | `grep -rn "HEAT" taskboard/ tests/` → the definition only; `views.py` `due_meter` | HLR-203 scope (Q-1, UX-2) |
| P-15 | `reldue_token` gives `+8d` in `dim` and `today` in `soon` | premise | ✅ TRUE | qa-reviewer probe (Q-2); `views.py` `reldue_token` | HLR-203 |

- **Premise evaluation:** 15 premise(s) · ✅ TRUE 15 / ❌ FALSE 0 / ❓ UNDECIDABLE 0

### 2.8 Fork preconditions (C-52)
- **Fork preconditions:** none — this batch runs one lane

## 3. High-level requirements (HLR)

### HLR-201 — Every view paints the accent only for its focus roles
- **Traceability:** US-201
- **Ledger:** LED-2026-10-02-batch-02.1, LED-2026-10-02-batch-02.11
- **Statement:** When any of the nine views is drawn, the system shall paint `HEX["accent"]` only on focus-role marks, shall draw every view title bold in `bright`, shall draw the matching legend swatches in the same tones as the marks they explain, and shall paint Setup's rows with their styles (the cursor, the chosen option, the check marks).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_colour_budget_app.py`
- **Numeric pass threshold:** census board (oracle + a URL card, two pinned tasks, a team directory, a history file, a Setup state) at panels 118×30, 80×24, 40×14, every view × presentation — 16 pairs, derived from `VIEW_ORDER` and the presentation tuples parsed out of `app.py` (`action_toggle_presentation`), asserted `== 16`: every accent run is a focus-role mark (0 others) — rule glyphs and the agenda `┃` all in ONE column per view (the today column), today's date text, at most one today stud/rail per task due today, the filter-bar rows, the cursor row; the detector finds today's rule on lanes, the filter bar and Setup's `>` (non-vacuity), and an accent `╎` placed off the today column turns it RED (mutation arm); every title span bold `bright`; Setup with team mode on: the `on` chip bold `bright`, `off` `mut` (and the reverse when off); app at terminal 118×30 with a team directory, keys `1`–`5`, `7`–`9`, `0`, `tab` cycled through every presentation of lanes, kanban and focus: 0 non-focus accent runs in the painted board; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** teal on any view means today, the field being typed in, or the list cursor — nothing else.
  - **Shipped surface:** `TaskboardApp` keys `1`, `2`, `3`, `4`, `5`, `7`, `8`, `9`, `0`, `tab` (painted board panel via `App.run_test`).
  - **Acceptance test(s):** AT-201
  - **Boundary catalog (QC-3):** ☑ boundary (a task due today; a URL card; team mode on and off; 40×14) ☑ empty (no history → flow's one-line message) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base tree paints `◆ TASKBOARD`, `AGENDA`, `◐`, the operator spine and Setup's hints in accent, and Setup's chips plain → RED (P-1, P-13).

### HLR-202 — The chrome spends no accent outside the edited field
- **Traceability:** US-201
- **Ledger:** LED-2026-10-02-batch-02.2
- **Statement:** The key bar shall draw every key bold in `bright` and its word in `mut` in both layers; the ribbon shall draw the local time bold in `bright`, each city's name in `mut` and its time in `hd`; every modal title and help heading shall be bold in `bright`; the help key map's keys shall be bold `bright`; a focused input's border shall keep the accent.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_colour_budget_app.py -k chrome`
- **Numeric pass threshold:** `render_key_bar` at widths 24, 60, 80, 118, 160 × every view × both layers: the hexes in the markup ⊆ {`bright`, `mut`, `dim`} (`dim` only for the overflow note), every key bold `bright`; `key_bar_plain` equal to the base strings frozen in the test; ribbon markup 0 accent, local time `b #e6edf7`; app at terminal 118×30: the key bar and ribbon strips carry 0 accent runs, the help modal's `Help ·` title and `Usage` heading paint `#e6edf7` bold, the `/` prompt's focused input border stays `#2dd4bf`; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the key bar, the clock and the dialog titles are white; teal stays only on the box being typed in.
  - **Shipped surface:** `TaskboardApp` key bar, ribbon, keys `?`, `m`, `/`.
  - **Acceptance test(s):** AT-202
  - **Boundary catalog (QC-3):** ☑ boundary (bar at 24 cells: words dropped, keys kept; the `more` layer) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base key bar paints 18 accent tags (primary) and the ribbon 3 → RED (P-2).

### HLR-203 — Soon-due work wears amber; the moving packet is quiet
- **Traceability:** US-201
- **Ledger:** LED-2026-10-02-batch-02.3, LED-2026-10-02-batch-02.12, LED-2026-10-02-batch-02.19
- **Statement:** The relative due token (`reldue_token` — the kanban card, the Focus review rail, people, agenda) one to seven days ahead shall be drawn in `soon`, its other tones unchanged; the gantt's flow packet `▬` shall be drawn in `mut`. The Focus view's `date_chip` (the Focus tiles, cards, image and compact cards, the detail pane and the review layout's selected-task line) is outside this requirement (BACKLOG).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_colour_budget_app.py -k "soon or packet"`
- **Numeric pass threshold:** `reldue_token` for +1, +4, +7 days → `soon`, +8 → `dim`, 0 → `soon` (unchanged), −1 → `over`; the kanban (grouped) of the oracle board paints every `+1d`…`+7d` token `#fbbf24` (≥ 1 asserted); the gantt at ticks 0..7 paints ≥ 12 `▬` cells in all, every one `#8b98a5`, none `#e6edf7`; 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** cards due within a week read amber; the moving packet no longer looks like the critical chain.
  - **Shipped surface:** `TaskboardApp` keys `4` and `3`.
  - **Acceptance test(s):** AT-203
  - **Boundary catalog (QC-3):** ☑ boundary (+7 vs +8 days; a packet on a chain reach) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base `+4d` is `mut` and the packet `bright` → RED (P-8).

### HLR-204 — The app speaks English
- **Traceability:** US-202
- **Ledger:** LED-2026-10-02-batch-02.4, LED-2026-10-02-batch-02.17
- **Statement:** Every string the app paints — the help modal's headings, usage, example and footer, the flow view, Setup's sections, labels, hints and check notes, and the team filter's labels — shall be English; stored values and internal keys shall not change.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_english.py`
- **Numeric pass threshold:** the help modal of each of the nine views, the flow view with and without history, Setup with its checks passing and failing, standup and people under each of the three filter modes (cycled through the app's `team_filter_cycle` action — no key is bound to it, BACKLOG): 0 hits of the Spanish lexicon (whole words chosen not to occur in English, plus accented letters outside the fixture's own data) in the painted text; the lexicon is guarded: on the base tree it flags at least the number of distinct painted strings measured at P3 and frozen in the test; the filter labels read `all`, `team`, `personal` while the stored values `todo`/`equipo`/`personal` still work; every help bullet of every view fits its 44-cell column; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** no Spanish word anywhere on screen.
  - **Shipped surface:** `TaskboardApp` key `?` in every view; keys `7`, `8`, `9`, `0`; the `team_filter_cycle` action.
  - **Acceptance test(s):** AT-204
  - **Boundary catalog (QC-3):** ☑ boundary (Setup checks failing and passing; flow with no history) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base help modal paints `Uso`, `para qué es` → RED (P-3).

### HLR-205 — A paged project says what is above and below
- **Traceability:** US-203
- **Ledger:** LED-2026-10-02-batch-02.5
- **Statement:** While a gantt group is paged, the system shall draw directly under its page one row in `dim` reading `▲ N above / ▼ M below` — each part only when its count is not zero — and shall size the page to the rows left after that row.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_polish.py -k paged`
- **Numeric pass threshold:** a one-project board of 30 open tasks at panel 80×24 (body 21, page 19): `tb15` selected → 19 task rows `tb0..tb18` then `▼ 11 below`; `tb25` → `tb19..tb29` then `▲ 19 above`; a 50-task board, `tb25` → `tb19..tb37` then `▲ 19 above / ▼ 12 below`; every row exactly 80 cells; the selection always in `line_map`; app at terminal 80×24 walking `down` 30 times: the selection is painted after every key and the hint row is never selected; 0 failures (counts computed from the rule — confirmed at P3).
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a long project shows how many of its tasks are off the page, and on which side.
  - **Shipped surface:** `TaskboardApp` key `3`, `down`.
  - **Acceptance test(s):** AT-205
  - **Boundary catalog (QC-3):** ☑ boundary (first page: below only; last page: above only; a middle page: both; one row left: no hint) ☑ empty (no paged group: no hint row) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base draws 20 rows and no hint (P-5) → RED.

### HLR-206 — Finishing a task in the gantt says where it went
- **Traceability:** US-203
- **Ledger:** LED-2026-10-02-batch-02.6
- **Statement:** When `]` moves the selected task to the board's last phase while the gantt is shown, the system shall post a short notification reading `<title> done · folded into ✓N · u undo`, `N` being the `✓n` its group's span row shows after the move (rest work: done, plus archived while `v` shows it), with the title shown literally.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_polish.py -k toast`
- **Numeric pass threshold:** app at terminal 118×30 on the oracle board: `tw2` selected, `]` → one notification `Build component library done · folded into ✓2 · u undo`; in a fresh app `tw3` (Doing) `]` → no notification (Review), a second `]` → `Fix checkout 500 error done · folded into ✓2 · u undo`; `]` in the kanban → no notification; titles `[b]x[/b]`, `[/]` and `[@click=app.quit]q[/]` are shown literally and the app keeps running; 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a short message names the finished task and where it folded.
  - **Shipped surface:** `TaskboardApp` keys `3`, `]`.
  - **Acceptance test(s):** AT-206
  - **Boundary catalog (QC-3):** ☑ boundary (a move that does not reach the last phase; the last phase already: `]` is a no-op) ☑ invalid (a markup-shaped title) ☐ empty — N/A ☐ error — N/A
  - **Negative control:** base posts 0 notifications (P-10) → RED.

### HLR-207 — The project just left stays open while it fits
- **Traceability:** US-204
- **Ledger:** LED-2026-10-02-batch-02.7, LED-2026-10-02-batch-02.13, LED-2026-10-02-batch-02.15
- **Statement:** While the gantt has fewer body rows than its groups' open tasks need, the system shall unfold the selected task's group first, then the previous group while all its open rows fit, then the other groups by urgency (HLR-208).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_polish.py -k sticky`
- **Numeric pass threshold:** app at terminal 80×24 on the oracle board: from `tw6` (Website Redesign's last open task) `down` into `tm6` (Mobile App's first) → Website Redesign stays `▾` (base: `▸`, P-7) and the highlight's row does not move up; continuing into API Platform (`ta1`) → Mobile App (now the previous group) stays `▾`; over the whole 25-step walk the highlight moves up on at most 2 steps (base 3; P-12) and at terminal 118×30 on at most 1 (base 1); a group visited two moves ago is ordered as never visited (TC on a synthetic four-group board, rows computed at P3; on the oracle walk the `ta1` step folds Website Redesign); 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** moving down into the next project keeps the one you just left open while there is room.
  - **Shipped surface:** `TaskboardApp` keys `3`, `down`.
  - **Acceptance test(s):** AT-207
  - **Boundary catalog (QC-3):** ☑ boundary (rows run out: the previous group folds; unbounded height: all unfold) ☑ empty (no previous group yet: the urgency order alone) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base folds Website Redesign on `tm6` → RED.

### HLR-208 — Work due today counts as urgent in the fold order
- **Traceability:** US-204
- **Ledger:** LED-2026-10-02-batch-02.8, LED-2026-10-02-batch-02.14, LED-2026-10-02-batch-02.15
- **Statement:** Among groups that are neither selected nor the previous group, the system shall unfold first the groups with the greatest urgency weight, then the most open tasks due today, then the earliest open due date, so that urgent groups — and among them those due today — are offered rows first; a group that does not fit is skipped and the next tried, so a smaller quiet group can take rows an urgent group cannot fit.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_polish.py -k urgent`
- **Numeric pass threshold:** a synthetic board — group C first in board order with one open task (the app selects it on entry), group A: one late task (due −3) plus four later, group B: one late task (due −1), one due today plus three later — at terminal 80×14 (panel 80×12, body 9, rows left after the span rows and C: 5): B `▾`, A `▸` (base: A by the earlier due); oracle board at terminal 80×24 on entry (`tw2` selected): Website Redesign, Data Warehouse and Ops & Security `▾`, Mobile App and API Platform `▸` (base: Ops & Security `▸`, P-6; P-12); 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the project holding the task due today stays open at 80×24.
  - **Shipped surface:** `TaskboardApp` key `3`.
  - **Acceptance test(s):** AT-208
  - **Boundary catalog (QC-3):** ☑ boundary (equal weights → earliest due; a group that does not fit is skipped and the next tried) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base unfolds A (counts late only) and folds Ops & Security → RED.

### HLR-209 — Weekends are shaded on the gantt field at a day per cell or finer
- **Traceability:** US-205
- **Ledger:** LED-2026-10-02-batch-02.9
- **Statement:** While the gantt's scale is at most one day per cell, the system shall paint the background of every field cell whose days are all Saturday or Sunday in `WEEKEND_BG` on the day row and on every body row; `WEEKEND_BG` shall quantise to a 256-colour index different from the screen background's.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_polish.py -k weekend`
- **Numeric pass threshold:** oracle board, panel 118×30 (`k = 1`, window Sep 14 + 79 cells): exactly the 22 weekend columns carry the background on the day row and on every body row's field, 0 other cells; panel 80×24 (`k = 2`): 0 shaded cells; a `k = 0.5` board: both cells of each weekend day shaded; a board whose today is a Saturday: the today rule keeps the accent and gains the background; `Color.parse(WEEKEND_BG)` 256-index ≠ that of the `Screen` background in `taskboard.tcss`; app at terminal 118×30: the painted panel carries the background on the weekend columns; 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** Saturdays and Sundays read as faint bands down the field.
  - **Shipped surface:** `TaskboardApp` key `3`.
  - **Acceptance test(s):** AT-209
  - **Boundary catalog (QC-3):** ☑ boundary (`k = 1`; `k = 0.5`; `k = 2` → none; a weekend cell holding the today rule) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base paints no background on the field → RED.

### HLR-210 — The echo shows where the selected task runs past the window
- **Traceability:** US-205
- **Ledger:** LED-2026-10-02-batch-02.10
- **Statement:** When the selected task's start lies before the window, the day row's echo shall draw `◂` on its first cell in place of `⟦`; when its due lies past the window, `▸` on its last cell in place of `⟧`; the printed dates stay exact.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_polish.py -k clip`
- **Numeric pass threshold:** oracle board at panel 118×30, `tw2` selected (start Sep 5, window from Sep 14): day row field cell 0 is `◂`, no `⟦` on the row, `Sep 5` printed; a synthetic board at panel 60×20 (`field_w` 32, `k = 7`, 224 days) with a long open task from today to +230 days: its echo ends in `▸` (base: `⟧` clamped on the last cell); a task starting on the window's first day (start computed from the axis) keeps `⟦`; `tw3` (inside) keeps `⟦`/`⟧`; 0 failures.
- **Priority:** low
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a bracket that would sit on the window edge becomes an arrow saying "it starts earlier".
  - **Shipped surface:** `TaskboardApp` keys `3`, `down`.
  - **Acceptance test(s):** AT-210
  - **Boundary catalog (QC-3):** ☑ boundary (start exactly the window's first day → `⟦`; the right branch on the synthetic `k = 7` board) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** base draws `⟦` on cell 0 (P-9) → RED.

## 4. Low-level requirements (LLR)

### LLR-201.1 — View titles
- **Traceability:** HLR-201
- **Ledger:** none
- **Statement:** `header` (`taskboard/views.py`) shall default its title tone to `bright`, and the lanes (`◆ TASKBOARD`), agenda, focus (every presentation), flow, standup, people and Setup titles shall be bold `bright`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_colour_budget_app.py -k title` (TC-201)
- **Numeric pass threshold:** every view × presentation at 118×30 and 24×10: the title span bold `#e6edf7`; 0 failures.
- **Negative control:** base lanes title accent → RED.
- **Boundary catalog:** ☑ boundary (a 24-cell panel: the clipped title) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-201.2 — Non-focus marks leave the accent
- **Traceability:** HLR-201
- **Ledger:** none
- **Statement:** The in-progress status `◐` shall be `hd`; the lanes grid and focus URL marks (`↗`, URL counts, URL lines) `mut`; the operator's spine `▌` in standup and people `bright`; the flow throughput bar `hd`; the team filter's active segment bold `bright`; Setup's section names bold `bright`, its passing check `done`, its chosen option chip (`on`/`off`, `shared`) bold `bright` and the other `mut`, its folder spine and stepper `mut`, and its hint keys bold `bright`; Setup's cursor `>`, the Focus review rail's `▸`, today's marks and the `/` filter bar keep the accent; each legend swatch takes its mark's new tone.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_colour_budget_app.py -k census` (TC-202)
- **Numeric pass threshold:** per HLR-201; the census set derived from `VIEW_ORDER` and the presentation tuples, guarded `== 16`; dropping one pair from the set → the guard RED; 0 failures.
- **Negative control:** any one site reverted to accent → its arm RED (mutation battery at P3).
- **Boundary catalog:** ☑ boundary (pinned task with a URL; team on/off; Setup cursor on each section) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-201.3 — Setup rows keep their styles
- **Traceability:** HLR-201
- **Ledger:** LED-2026-10-02-batch-02.11
- **Statement:** `render_setup`'s rows shall be assembled from styled `Text` pieces fitted on their plain text (label 24, control 30, check 4 cells), never from `str()` of a styled `Text`, so the cursor, the chosen chip and the check marks keep their tones.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_colour_budget_app.py -k setup` (TC-213)
- **Numeric pass threshold:** every body row of `render_setup` (team on and off, cursor on each section) carries ≥ 1 style span; the row's plain text equals the base plain text, frozen in the test as expected strings (columns unchanged); the `>` row's cursor in accent; 0 failures.
- **Negative control:** the base rows carry 0 spans (P-13) → RED.
- **Boundary catalog:** ☑ boundary (a label longer than 24 cells; a 40-cell panel) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-202.1 — Key bar
- **Traceability:** HLR-202
- **Ledger:** LED-2026-10-02-batch-02.16
- **Statement:** `render_key_bar` (`taskboard/keymap.py`) shall draw every key show bold `bright` and its label `mut` in both layers; `GROUP_HUE` shall no longer colour keys; `;` (`TaskboardApp.action_layer_toggle`) shall switch the bar between its two layers.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_colour_budget_app.py -k keybar` (TC-203)
- **Numeric pass threshold:** per HLR-202; plain text unchanged (`key_bar_plain` equal before/after at every width); 0 failures.
- **Negative control:** a group hue left on one key → RED.
- **Boundary catalog:** ☑ boundary (24 cells; overflow note) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-202.2 — Ribbon, modal titles, help key map
- **Traceability:** HLR-202
- **Ledger:** none
- **Statement:** `Ribbon.update_clock` shall draw the local time bold `bright`, each city's name `mut` and its time `hd`; `.modal-title` in `taskboard.tcss` shall be `#e6edf7` bold; `HelpScreen` shall draw its `KEYS` heading `#e6edf7` bold and each key bold `#e6edf7`; `.modal Input:focus` and `#palette-input:focus` keep `#2dd4bf`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_colour_budget_app.py -k "ribbon or modal"` (TC-204)
- **Numeric pass threshold:** ribbon markup 0 accent, local time `b #e6edf7`; the parsed `.modal-title` color `#e6edf7`; `HelpScreen` composed text 0 `#2dd4bf`; 0 failures.
- **Negative control:** base ribbon 3 accent tags → RED.
- **Boundary catalog:** none — one style read-back per seat

### LLR-203.1 — Soon tone and packet tone
- **Traceability:** HLR-203
- **Ledger:** none
- **Statement:** `reldue_token` shall return `soon` for 1 ≤ days ≤ 7 (other tones unchanged); `_gantt_bar` shall draw the flow packet in `mut`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_colour_budget_app.py -k "soon or packet"` (TC-205)
- **Numeric pass threshold:** per HLR-203; 0 failures.
- **Negative control:** `<= 7` written `< 7` → the +7 arm RED.
- **Boundary catalog:** ☑ boundary (+7/+8; 0) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-204.1 — English copy
- **Traceability:** HLR-204
- **Ledger:** none
- **Statement:** `help_usage`, `help_example`, the flow view's messages and cycle labels, the flow legend, `render_setup`'s header, sections, labels, chips and hints (`taskboard/views.py`), `probe_setup_health`'s notes (`taskboard/team_sync.py`) and `HelpModal`'s headings and footer (`taskboard/modals.py`) shall be English; `render_team_filter_chrome` shall label the modes `all · team · personal` while `TEAM_FILTER_MODES` keeps `todo`, `equipo`, `personal`; every help bullet of every view shall stay within 44 cells.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_english.py` (TC-206)
- **Numeric pass threshold:** per HLR-204; `help_usage(mode)` returns the same section count per view as base; every bullet of every view ≤ 44 cells (the TC-116 law widened, qa Q-11); 0 failures.
- **Negative control:** one Spanish heading left → RED.
- **Boundary catalog:** ☑ boundary (the 44-cell help column) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-205.1 — The page hint row
- **Traceability:** HLR-205
- **Ledger:** none
- **Statement:** In `_gantt_frame`, a group taller than the rows left (`room ≥ 2`) shall be paged in pages of `room − 1` tasks holding the selection, followed by one row `  ▲ N above / ▼ M below` (zero parts omitted) in `dim`, padded to the width; with `room = 1` it shall be paged as shipped with no hint row; the hint row is never in `line_map`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_polish.py -k paged` (TC-207)
- **Numeric pass threshold:** per HLR-205; 0 failures.
- **Negative control:** a page of `room` tasks plus the hint → the frame is one row taller than the panel → RED.
- **Boundary catalog:** ☑ boundary (room 1, 2; first/last/middle page) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-206.1 — The finish toast
- **Traceability:** HLR-206
- **Ledger:** none
- **Statement:** `TaskboardApp.action_phase_move` (`taskboard/app.py`) shall, when the view is the gantt and the move made the task done, call `notify` with the message of HLR-206, the title passed raw (not escaped) with `markup=False`, `N` counted over its group's rest work after the move (`v` respected).
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_gantt_polish.py -k toast` (TC-208)
- **Numeric pass threshold:** per HLR-206; 0 failures.
- **Negative control:** notifying on every move → the Review step posts one → RED.
- **Boundary catalog:** ☑ invalid (markup title) ☑ boundary (Inbox task: its count over the Inbox's rest work) ☐ empty — N/A ☐ error — N/A

### LLR-207.1 — The fold order
- **Traceability:** HLR-207, HLR-208
- **Ledger:** LED-2026-10-02-batch-02.15
- **Statement:** `gantt_plan` shall take `previous` (NEW keyword: the previous group's project id, `INBOX_GROUP` (NEW constant, `""`) for the Inbox, `None` for no previous group — the default) and order the non-selected groups by (not the previous group, −urgency weight, −open tasks due today, earliest open due), unfolding each in turn whose open count fits the rows left; `render_view`, `render_gantt`, `_gantt_frame` and `legend_entries` shall thread a `gantt_previous` keyword to it.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_polish.py -k "sticky or urgent"` (TC-209)
- **Numeric pass threshold:** per HLR-207 and HLR-208; 0 failures.
- **Negative control:** ignoring `previous` → the sticky arm RED; counting late only → the urgent arm RED; dropping the due-today tie-break → the oracle 80×24 arm RED.
- **Boundary catalog:** ☑ boundary (a previous id with no group; the Inbox as previous — its own TC arm) ☑ empty (`None`) ☐ invalid — N/A ☐ error — N/A

### LLR-207.2 — The app remembers the previous group
- **Traceability:** HLR-207
- **Ledger:** LED-2026-10-02-batch-02.15
- **Statement:** `TaskboardApp` shall keep the selected task's group and the group before it (a project id, or `INBOX_GROUP` for the Inbox), updating them each time the gantt is rendered with a selection in a new group, and shall pass the previous one as `gantt_previous` to every gantt render and to `HelpModal`'s legend.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_gantt_polish.py -k sticky` (TC-210)
- **Numeric pass threshold:** per HLR-207; the legend opened after the walk names the frame's fold marks (no-ghost law green); 0 failures.
- **Negative control:** the list never updated → AT-207 RED.
- **Boundary catalog:** ☑ empty (no selection) ☐ boundary — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-209.1 — Weekend columns and their background
- **Traceability:** HLR-209
- **Ledger:** LED-2026-10-02-batch-02.18
- **Statement:** `WEEKEND_BG` (NEW, = `HEX["weekend"]`, `#1a1d22`, a declared palette key) and `GanttAxis.weekends()` (NEW) shall give the field cells whose days are all Saturday or Sunday when `ax.k ≤ 1` (empty otherwise); `_gantt_field` and `gantt_day_row` shall give those cells the background in the cell's own tag (`_on_weekend`: `[style on #1a1d22]`, so `collapse_runs` still merges runs); only constant glyph cells are tagged, never board text (security P2 note on HLR-209).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_polish.py -k weekend` (TC-211)
- **Numeric pass threshold:** per HLR-209; 0 failures.
- **Negative control:** `k < 1` instead of `≤ 1` → the 118×30 arm shades nothing → RED.
- **Boundary catalog:** ☑ boundary (k 0.5, 1, 2) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-210.1 — Echo clip arrows
- **Traceability:** HLR-210
- **Ledger:** none
- **Statement:** `gantt_echo` shall put `OFF_LEFT` at the clipped open end when `ax.cell(start) < 0` and `OFF_RIGHT` at the clipped close end when `ax.end_cell(due) ≥ ax.w`, for the two-date and the one-date-open forms.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_polish.py -k clip` (TC-212)
- **Numeric pass threshold:** per HLR-210; 0 failures.
- **Negative control:** `<= 0` instead of `< 0` → a task starting on the window's first day loses `⟦` → RED.
- **Boundary catalog:** ☑ boundary (start on cell 0 exactly) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

## 4b. Information Flow Contract (IFC)

Part A always. Part B: the gantt panel's task rows are addressed by row index (`line_map`), and
this batch inserts a hint row into that panel and a new input into its fold.

```
FLOW: polish
  SOURCE : Board + selected_id + today + panel size + app state (gantt_previous)
  NODES  :
    - fn    : header
      owner : LLR-201.1
      in    : title markup, right markup, width
      out   : head row
    - fn    : render_key_bar
      owner : LLR-202.1
      in    : width, view, layer
      out   : key bar markup
    - fn    : Ribbon.update_clock
      owner : LLR-202.2
      in    : now, clock cities
      out   : ribbon markup
    - fn    : status_glyph and the other re-toned marks
      owner : LLR-201.2
      in    : task, board / view state
      out   : glyph, tone outside the accent
    - fn    : reldue_token
      owner : LLR-203.1
      in    : task, today, board
      out   : token, tone
    - fn    : help_usage
      owner : LLR-204.1
      in    : view mode
      out   : sections of English bullets
    - fn    : gantt_plan
      owner : LLR-207.1
      in    : board, selected_id, today, body rows, focus, previous
      out   : groups with unfolded flags
    - fn    : GanttAxis.weekends
      owner : LLR-209.1
      in    : axis
      out   : weekend cell set
    - fn    : gantt_echo
      owner : LLR-210.1
      in    : task, axis
      out   : bracket cells with clip arrows
    - fn    : _gantt_frame
      owner : LLR-205.1
      in    : the nodes above
      out   : rows + line_map
    - fn    : TaskboardApp gantt group memory
      owner : LLR-207.2
      in    : the selected task's group on each gantt render
      out   : the previous group's project id
    - fn    : action_phase_move
      owner : LLR-206.1
      in    : selected task, view mode
      out   : notification
  SINK   : the painted app (board panel, key bar, ribbon, modals)
```

```
COMPONENT: gantt-body
  PARENT : SYSTEM
  SURFACE: gantt view (key 3)
  INPUTS : board: Board ; selected_id: str ; width: int ; height: int ; gantt_previous: str
  OUTPUTS:
    - id          : task-rows
      value       : one row per drawn open task; a paged group's hint row is not addressed
      address     : line_map[task_id] = row index in the rendered Text
      cardinality : drawn open tasks
      consumers   : taskboard/app.py::_scroll_selected_into_view ; taskboard/views.py::render_view
      owner       : LLR-205.1
```

## 5. Validation strategy
Layer A (`TC-201`..`TC-213`) and Layer B (`AT-201`..`AT-210`, one node each — C-18) are pytest
nodes in `tests/test_colour_budget_app.py`, `tests/test_english.py` and
`tests/test_gantt_polish.py` (NEW — created in Phase 3; node ids provisional until P3, V-5),
each carrying its id in its docstring. The census fixtures (team directory, history file,
Setup state, pinned tasks) extend `tests/kg_board.py`. ATs drive `TaskboardApp` through
`App.run_test()` at terminal sizes; TCs drive `render_view` and the helpers at panel sizes.
Captures (SVG + text) of every changed view at 118×30 and 80×24 come from the oracle board
only, into `evidence/captures/`; `tools/privacy_sweep.py` and the entity-decoded sweep run over
`evidence/` at each gate. Full suite `python -m pytest -q -p no:cacheprovider` at close; base
1611 passed.

| AT | Story | Drives |
|---|---|---|
| AT-201 | US-201 | keys `1`–`5`, `7`–`9`, `0`, `tab` through every presentation, team mode on: painted accent runs are focus-role marks only; Setup's chosen chip distinct |
| AT-202 | US-201 | key bar, ribbon, `?`, `m`, `/`: chrome without accent except the focused input |
| AT-203 | US-201 | keys `4`, `3`: soon tokens amber, packet `mut` |
| AT-204 | US-202 | `?` in every view, keys `7`–`0`, the three filter modes: no Spanish painted |
| AT-205 | US-203 | key `3` on a 30-task project, `down` ×30: the hint and the selection |
| AT-206 | US-203 | keys `3`, `]`: the toast |
| AT-207 | US-204 | keys `3`, `down` from `tw6` into `tm6` and `ta1`: the previous group stays open |
| AT-208 | US-204 | key `3` on the synthetic urgency board (terminal 80×14) and on the oracle board (terminal 80×24) |
| AT-209 | US-205 | key `3`: weekend columns shaded |
| AT-210 | US-205 | key `3`, select `tw2`: `◂` on the echo |

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion shown RED on the base tree or by a recorded mutation.
- each existing node the batch changes is listed in its increment's reverse census with its disposition.
- full suite: 0 failures.

## 6. Appendices

### 6.1 Verification beyond automation
- expert inspection: ux-reviewer walkthrough on the captures and the app at P4 — `planned`.
- user evaluation: the operator reads the captures — `planned` (outside the batch).

### 6.2 Relevant design decisions
- D-201: Today keeps the accent and the selection keeps reverse video (answer D4 "keep").
- D-202: `━` stays shared by the critical chain (field) and the echo (ruler) (answer D13 "keep"); no change.
- D-203: Only the previous group is sticky (ux UX-4): a session-long visited list let quiet groups outrank urgent ones for the rest of the session, against UXV-3, and measured no better (2 upward moves at 80×22 either way). The residual — the highlight still moves up when rows run out (2 steps at 80×22, base 3) — is for the operator (qa Q-6).
- D-204: "Due today counts" is read as an urgency weight of late + due-today tasks, ties broken by the most tasks due today (ux UX-3, qa Q-5): the frame the operator complained about changes — at terminal 80×24 Ops & Security unfolds and API Platform (late 2) folds instead, its `▲2` still on its span row.
- D-205: `WEEKEND_BG = #1a1d22`: the prototype's `#161d27` quantises to the field background's index 16 at 256 colours (P-4); `#1a1d22` → 234, the same luminance, a neutral grey instead of a blue tint. A 16-colour terminal shows no shading (both map to black) — declared limit. Provisional: before/after captures go to the operator (ux UX-5).
- D-206: Shaded rows follow the prototype: the day row and the body field; not the month row, the labels or the chips.
- D-207: Focus roles kept in accent: today marks, the `/` filter bar and focused input borders (UXV-9's input border is this role), the Focus review rail's `▸`, Setup's `>` cursor (painted once its row keeps its styles, LLR-201.3).
- D-208: Non-focus re-tones: `◐` → `hd`; `↗`/URL marks → `mut`; operator spine → `bright`; throughput bar → `hd`; filter chip and Setup sections/hint keys → bold `bright`; Setup's passing check → `done`; Setup's chosen chip → bold `bright` against `mut` (not reverse: reverse is the selection's sign, ux UX-5); folder spine and stepper → `mut`. Provisional for the operator's verdict on captures.
- D-209: The ≤7-day token `reldue_token` is shared (kanban, the Focus review rail, people, agenda): all turn amber. The Focus tiles/cards/stale layouts draw their due through a different helper, `date_chip`, whose week tone stays `later` (slate) — outside HLR-203 and the SOON answer (kanban); found by the P4 walkthrough (UXV2-1), for the operator (BACKLOG). The word `today` keeps each view's shipped tone (`soon` in `reldue_token` and the gantt chip, accent on the lanes meter) — unifying it is a question for the operator (BACKLOG); the dead `HEAT` table is left alone (BACKLOG).
- D-210: The packet takes `mut` ("a quieter tone").
- D-211: Ribbon: local time bold `bright`; city names `mut` and times `hd`, so the local clock still stands apart (ux UX-5). The key bar loses its eight group hues as the commission names them; P4 checks the `more` layer still reads.
- D-212: Internal keys stay Spanish where they are data (`todo`/`equipo`/`personal` filter values, Setup's check keys); only what is painted changes. The prototype copy (`prototypes/team_sync/generate.py`) is not edited.
- D-213: The hint row text is the operator's chosen wording, `▲ N above / ▼ M below`, in one row directly under the page ("una fila tenue al borde de la página" read as the page's lower edge, qa Q-16); `▲` also means late — accepted, the row is `dim` and worded. Pages stay fixed (a page flip moves the highlight up) — P4 shows it to the operator (ux UX-7).
- D-214: The toast fires only for `]` in the gantt reaching the last phase; markup is off so a title is literal (the title is not escaped, S-1). After `u` the toast stays until its timeout (P4, ux UX-6).
- D-217: "Fold last" is read as "offered rows first" with the shipped skip-and-continue fill (ux UX-11): during the walk at 80×24 Ops & Security (5 rows) can fold while Data Warehouse (4, nothing urgent) stays open; the alternative — stop at the first urgent group that does not fit — leaves rows blank. For the operator.
- D-218: `;` never reached the key bar's `more` layer (`action_layer_toggle` read Textual's CSS `layer`, always `"default"`; since commit 8b73920) — found by code review of increment 002 (F3); fixed in that increment (one token, `app.py` already in its file set) because HLR-202's "both layers" is otherwise invisible. The operator now sees the `more` layer on `;` for the first time since that commit.
- D-219: The help copy names only shipped keys: the focus help said `p` pins (`t` does; `p` adds a project) and the people help said `f` cycles the filter (no key is bound to `team_filter_cycle`, BACKLOG) — the English copy says `t pins the task` and `filter: all · team · personal`.
- D-216: All twelve answers are the options marked recommended, with empty notes (ux UX-9): they carry no nuance to read the un-asked decisions against, so D-203, D-204, D-205, D-208, D-211 and D-217 are flagged for the operator's verdict on the captures.
- D-215: Trigger family A is judged not fired: the `taskboard` package is one module (no module map exists), as batch-01 ruled.

### 6.3 Open risks
- Sticky unfolding reduces, not removes, upward moves (P-12): when rows run out the previous group folds, and it is above the cursor on a downward walk.
- Re-toning shared helpers moves marks other tests pin (reverse census per increment).

### 6.4 Security questions (scan `devflow-scan-spec.py`: `security_required: true`, flags `token`, `role`)
- The two flags are vocabulary hits — "token" (the relative-due token), "role" (the focus role); the batch adds no credential, auth, network, storage or input surface.
- Real surfaces, answered: (1) **markup over file-derived text (C-17)** — the toast prints a task title through `notify`, which parses markup by default: LLR-206.1 turns markup off, AT-206 drives a `[b]x[/b]` title. The hint row and the English copy print counts and constants only. (2) **record hygiene** — transcripts are written with the home path redacted; captures come from `tests/kg_board.py` only; `tools/privacy_sweep.py` plus the entity-decoded sweep run over `evidence/` (BACKLOG S-8). security-reviewer at P2 and over the toast increment.

### 6.5 Requirement amendments (Before / After · Deleted / New)
- P2 iteration 1 → `iterate-to-refine` (qa PASS-WITH-NOTES, ux FAIL, security PASS-WITH-NOTES; `02-review.md`). Before → After: HLR-203 named a due-meter week tone (a phantom, Q-1/UX-2) → Deleted; +8d `mut` → `dim` (Q-2). HLR-207 visited list → the previous group only (UX-4, LED .13). HLR-208 weight → weight, then due-today count (UX-3/Q-5, LED .14). New: LLR-201.3 Setup rows keep their styles (UX-1, LED .11); P-13..P-15. HLR-201 census derived and guarded `== 16` with a position-based detector (Q-7..Q-9); HLR-204 lexicon guarded, filter modes cycled, fit law on every view (Q-10, Q-11); HLR-205 middle page (Q-13); HLR-206 `✓n` semantics and hostile titles (Q-13, S-1); HLR-209 the reverse-video clause Deleted (no field cell is reverse) and a today-on-Saturday arm New; HLR-210 the right branch's synthetic board New (Q-3). Parent stories re-read: US-204 reworded ("the project I just left"). Every changed AT re-cut into the increment plan (C-21). P2 iteration 2 (LED .15): HLR-208 "offered rows first" (UX-11, D-217); `INBOX_GROUP` (N-1); the earlier-visited fixture (N-2); frozen Setup strings (N-3); the `k = 7` fixture pinned at +230 days.
- P4 → P3 `iterate-to-fix` (increment 006; qa P4 FAIL G-001..G-003): AT-207's two functions are ONE parametrised node (C-18); its 118×30 arm's fold checks are RED on base, its ≤ 1 up-move bound alone is a pin (G-006). HLR-203 (G-003, ux UXV2-1, D-209; LED .19) — **Before:** "A relative due token one to seven days ahead shall be drawn in `soon`, its other tones unchanged; the gantt's flow packet `▬` shall be drawn in `mut`." **After:** "The relative due token (`reldue_token` — the kanban card, the Focus review rail, people, agenda) one to seven days ahead shall be drawn in `soon`, its other tones unchanged; the gantt's flow packet `▬` shall be drawn in `mut`. The Focus view's `date_chip` (the Focus tiles, cards, image and compact cards, the detail pane and the review layout's selected-task line) is outside this requirement (BACKLOG)." **Deleted:** "A relative due token" (read as every seat). **New:** the `reldue_token` seat list; the `date_chip` exclusion. **Re-derived:** AT-203 and TC-205 unchanged (their threshold already named `reldue_token` and the kanban). Parent US-201 re-read: unchanged ("soon-due work in amber" — the `date_chip` seats go to the operator via BACKLOG).
