# Requirements Document — taskboard — Batch 2026-10-04-batch-02

> Live contract (rev100); history in `01-requirements-ledger.md`. Ids `6xx`.

> **Reserved field names** (read literally, never translated): `Validation` · `Acceptance test(s)` · `Boundary catalog` · `Negative control` · `Premise evaluation` · `Fork preconditions` · `Ledger` · `Requirement` · `⏸ DEFER`

## 1. Introduction

### 1.1 Purpose
B2a of the `kg_mejoras` plan: milestones (round 5 "M-1 y M-2"; M-3 a one-time migration). Moving linked dates is B2b (D-601).

### 1.2 Scope
In: the milestone flag (model, `M`, the editor, the details view, team sync, undo); the gantt row
(M-1) and the ruler marks (AX-2); the kanban band rule (M-2) and the milestone's exit from every
kanban card, count and selection; the one-time offer (M-3) with backup, log, `u` revert, run-once and
fail-closed. Out: moving linked dates (US-604 → B2b); the chain map (batch C); flow-template milestone
steps (batch D); a milestone mark in the lanes view, agenda, focus, standup, people, report (BACKLOG).

### 1.3 Definitions
| Term | Definition |
|------|------------|
| milestone | a task whose `milestone` field is the boolean true: one date, its due (its start equals it when written by this app), no duration |
| reached | a milestone in the board's last phase and not archived |
| late | an open milestone whose due is before today |
| open | not in the last phase and not archived (`models.is_open`, B1) |
| candidate | an open board task, not a milestone, whose title is text and whose due is readable: group 1 "one-day" when its readable start equals its due, group 2 "due-only" when its start is empty |
| offer mark | `settings["migrations"]["milestones"]` is the int 1, beside B1's `links` mark |
| band room | the cells a band rule leaves for milestones: width − the band facts' cells − 4 (` ── `) − 2 (the rule tail kept) |

### 1.6 NEW literals and constants (C-36)
Every literal below is NEW — created in Phase 3 — and the requirement naming it owns it.

| Literal / constant | Value | Owner |
|---|---|---|
| `MILESTONE_NEEDS_DATE` | "a milestone needs a date — give it a due date first" | LLR-601.1 |
| `M` / action `milestone_toggle` / label `Milestone` | the key | LLR-601.2 |
| set toast | "‹title› is a milestone · ◆ ‹Mon D›[ · start was ‹Mon D›] · ‹where› · u undo"; ‹where› = "on the ‹project› band" or "shown on the gantt" | LLR-601.2 |
| clear toast | "‹title› is a task again · u undo" | LLR-601.2 |
| title cut | 40 cells in every toast (the shipped `clip(…, 40)` convention) | LLR-601.2 |
| editor refusal toast | "not a milestone — a milestone needs a date (other changes saved)" | LLR-601.3 |
| editor start toast | "milestone: the start follows the due (‹Mon D›)" | LLR-601.3 |
| details suffix | " · ◆ milestone" | LLR-601.3 |
| reached toast | "‹title› reached · ◆✓ · u undo" | LLR-602.1 |
| chips | "in Nd", "today", "▲Nd", "✓ done", "no due" | LLR-602.2 |
| legend items | "◆ milestone", "◆✓ reached" | LLR-602.3 |
| band segment | "◆ ‹Mon D› ‹title› · in Nd" / "· today" / "· Nd late"; reached "◆ ‹Mon D› ‹title› ✓"; separator " ── "; overflow "+N ◆" | LLR-603.2 |
| `MILESTONES_MIGRATION` | 1 | LLR-605.1 |
| `MILESTONE_BACKUP` / `MILESTONE_LOG` | ".pre-milestones" / ".milestones-log" | LLR-605.2 |
| conversion toast | "Milestones: N converted[ · K no longer eligible] · backup ‹name› · u undo" | LLR-605.3 |
| none toast | "Not now — this offer won't show again; M makes any task a milestone." | LLR-605.3 |
| failure toast | "Milestone offer stopped: ‹reason›. The board file was not changed; the offer returns at the next start." | LLR-605.3 |
| undo toast | "Milestone conversion undone — the tasks are back as they were" | LLR-605.3 |
| offer title / count / line | "◆ Milestones · convert one-day tasks?" / "N candidates · shown once" / "Converting keeps the task, its links and its history; it becomes a ◆ date." | LLR-605.4 |
| offer headings | "One-day tasks (start = due)", "Due date, no start" | LLR-605.4 |
| offer keys row | "space toggle  ·  ↵ convert N  ·  esc not now — won't ask again" | LLR-605.4 |

### 1.4 References
The `kg-mejoras` worktree's `prototypes/kg_mejoras/` (`IMPLEMENTATION-PLAN.md` §Batch B, `NOTES.md` rounds 5–6, `variants_round5.py`, frames `out/M-1-*`, `M-2-*`, `M-3-*`, `AX-2-*`); B1's record. Re-derived.

## 2. Overall description

### 2.1 Product perspective
One more `Task` field through the shipped seats (`from_dict`, `_to_dict`, undo, gantt plan, kanban plan); the offer reuses B1's migration seat.

### 2.3 User characteristics (context of use)
- **User:** the operator and teammates, keyboard only.
- **Tasks:** mark a commitment while planning in the gantt; see in the kanban what each project heads
  for; answer the offer once, on the first start after the upgrade.
- **Environment:** a resizable terminal; reference sizes 118×30 and 80×24.
- **The offer:** an unasked-for modal at start, on the real board, which may hold dozens of due-only
  tasks.

### 2.4 Constraints
≤ 4 SOURCE files per increment; Textual 8.2.8 / Rich 15.0.0; no new dependency; S1 Text pieces; colour budget (accent = focus/today); the operator's real board is never opened.

### 2.5 Assumptions
The verdict frames are the visual authority; where open or self-contradictory, the most conservative reversible reading is taken and listed (PLAN.md §PV).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-601 | As a taskboard user, I want to mark a task as a milestone — one date, no duration — with a key or in the editor, and have it saved, synced to my team and undoable like any field, so that a commitment date is a first-class thing on my board. | round 5 verdict ("M-1 y M-2", a flag on Task); plan §Batch B | READY |
| US-602 | As a taskboard user reading the gantt, I want a milestone drawn as a `◆` on its date with a chip saying how far it is, no bar, reached ones in the reached grey (LED .11), and the selected project's milestones marked on the ruler, so that I see commitments, not work spans. | M-1, AX-2 | READY |
| US-603 | As a taskboard user reading the kanban, I want milestones out of the phase columns and counts and riding their project's band rule — late first, then upcoming, then the last reached — so that the columns show work and the band shows what it is for. | M-2 | READY |
| US-604 | As a taskboard user, I want moving a task's dates to move what waits on it (push by default, per-project setting, `m` per move), so that a chain stays consistent. | round 6 verdict | OUT → B2b (D-601) |
| US-605 | As the operator with an existing board, I want to be offered, once, to convert the one-day tasks I already use as milestones — choosing which, with a backup first, a log, a way back and never a second offer — so that my board moves to milestones without me retyping anything. | M-3 verdict (a one-time migration, not a feature); operator safeguard "Sí: respaldo + registro + deshacer" | READY |

#### Refinement log

| Story | INVEST | Feasibility | Classification |
|---|---|---|---|
| US-601 | all ✓ | models, app, modals, keymap (001) | READY |
| US-602 | all ✓ (C-16: real app) | views, app (002) | READY |
| US-603 | all ✓ | views, app (003) | READY |
| US-604 | V ✓ · E ✗ · S ✗ | no move mode exists (P-17); ≥ 3 increments alone | OUT → B2b (D-601) |
| US-605 | all ✓ (C-16: real keys) | models, app, modals (004) | READY |

Evaluability: each HLR's acceptance block (§3).
RC-1 (b): none already shipped (`p0-probes.txt`).

### 2.7 Premise evaluation (C-43)

| # | Premise | Tier | Verdict | Executed evidence | Disposition |
|---|---|---|---|---|---|
| P-1 | `Task` has no `milestone` field; an unknown `milestone` key round-trips through `extra` | premise | ✅ TRUE | `p1-premises.txt` §P-1 | LLR-601.1 |
| P-2 | `M`, `m` unbound everywhere; `c` is Clocks | premise | ✅ TRUE | §P-2 | LLR-601.2 |
| P-3 | The gantt draws a one-day task as one `◆` in its priority hue, no label mark | premise | ✅ TRUE | §P-3 | PV-609 |
| P-4 | Gantt rest work draws no row; nav walks `GanttGroup.open` | premise | ✅ TRUE | §P-4 | LLR-602.1 |
| P-5 | Kanban `N tasks` and WIP tags count every visible task | premise | ✅ TRUE | §P-5 | LLR-603.1 |
| P-6 | Team push writes every `Task` field; a pull builds via `Task.from_dict` | premise | ✅ TRUE | §P-6 | LLR-601.1 |
| P-7 | B1's seat exists (`links_marked`, `_create_beside`, `run_link_migration`); `links_marked` ignores other keys | premise | ✅ TRUE | §P-7 | LLR-605.2 |
| P-8 | `Board.load` on a missing path seeds and saves, settings empty; the seed has 11 open due-only tasks | premise | ✅ TRUE | §P-8 | LLR-605.3 |
| P-9 | Of the suite's 541 app starts (372 tests), 274 (251 tests, 27 files) hold a candidate and would open the offer at mount — all through due-only tasks, 0 through a one-day task | premise | ✅ TRUE | `evidence/p1-offer-census.txt` (2306 passed, exit 0) / `p1-offer-census.json` (`p1_offer_census.py`) | §5 seam |
| P-10 | The undo snapshot lacks `start_date`, `milestone` | premise | ✅ TRUE | §P-10 | LLR-601.2 |
| P-11 | Base suite at `4b2c13a`: 2306 passed, exit 0 | premise | ✅ TRUE | `base-suite.txt` | ledger base |
| P-12 | `TASK_CHIPS_ONE_ROW` 122; the date/flags half ~76 cells at 80 | premise | ✅ TRUE | §P-12 | LLR-601.3 |
| P-13 | `OptionList` binds `enter` (select) and the arrows, not `space`; a focused list highlights its first enabled option and `↓` skips a disabled one | premise | ✅ TRUE | `p1-premises.txt` §P-13; qa P2 probe 2 (`seq [1, 2, 3, 5]`) | LLR-605.4 |
| P-14 | `bump_due` moves only the due | premise | ✅ TRUE | §P-14 | LLR-601.1 |
| P-15 | B1's `migration` undo entry restores several tasks in one step; `on_mount` migrates links first | premise | ✅ TRUE | §P-15 | LLR-605.3 |
| P-16 | The prototype's rules over its round-5 boards give the offer's two groups (3 one-day pre-checked, 5 due-only, in order), the six chips, the tones, the band order and the fit ladder | premise | ✅ TRUE | `evidence/p1-thresholds.txt` (`p1_thresholds.py`, in the prototype worktree) | LLR-602.2, LLR-603.2, LLR-605.1 |
| P-17 | No gantt move mode at base | premise | ✅ TRUE | `p0-probes.txt` §US-4 | D-601 |
| P-18 | Shifted milestone board: kanban 31 tasks, 25 without milestones; band rooms 56/62/50/69/59 at 118 and 18/24/12/31/21 at 80; the prototype layout's segments at those rooms; every band drawn from render height 30 at 118 (the kanban panel: a 118×40 terminal; at 118×30 Ops folds below) | premise | ✅ TRUE | `evidence/p1-thresholds-shipped.txt` (`p1_thresholds_shipped.py`) | HLR-603, LLR-603.2 |
| P-19 | While a modal is up, board keys cannot change the board; only timers can | premise | ✅ TRUE | security P2 probe (`probe_modal.py`) | LLR-605.2 |

- **Premise evaluation:** 19 premise(s) · ✅ TRUE 19 / ❌ FALSE 0 / ❓ UNDECIDABLE 0

### 2.8 Fork preconditions (C-52)
- **Fork preconditions:** none — this batch runs one lane

## 3. High-level requirements (HLR)

### HLR-601 — A task can be a milestone
- **Traceability:** US-601
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.3, LED-2026-10-04-batch-02.4
- **Statement:** The system shall let a task be a milestone — one date, its due: `M` on the selected task and the editor's milestone box shall set and clear the flag; setting it on a task with dates shall make the start equal the due (the start becomes the due, or the due becomes the start when only a start exists); setting it on a task with no date shall be refused with `MILESTONE_NEEDS_DATE` and change nothing; `+`/`-` on a milestone shall move its start and due together; each `M` and bump shall be one `u` step; the flag shall be saved, loaded only as the boolean true, carried by team sync, and kept by search, archive, links and undo like any field.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_milestones.py`
- **Numeric pass threshold:** on the shifted kg board in the app, in the gantt (`3`, `↓` until `Rate limiting` is selected): `M` on `Rate limiting` (start ≠ due) → the saved file holds `"milestone": true` and `start_date == due_date ==` its due; one toast starting `Rate limiting is a milestone · ◆ ` and holding `start was`; `M` again → `"milestone": false`, the dates unchanged, toast `is a task again`; `M` on `Plan Q4 roadmap` (no date) → exactly one warning toast holding "a milestone needs a date", the file byte-identical; `+` on the milestone → start and due both +1 day; `u` → the dates before `+`; the editor's box ticked with a new due and Save → the flag set and start = that due; team arm: started with a tmp team folder and a sync interval of 0.2 s, `M` → the pushed `board.<user>.json`, polled for at most 5 s, holds `"milestone": true` for that task; 0 failures.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** a task becomes a milestone, keeps one date, and the change is saved, undoable, said and pushed.
  - **Shipped surface:** `TaskboardApp` keys `3`, `↓`, `M`, `+`, `u`, `e` (editor, the box, Save) via `App.run_test(notifications=True)`; the board file and the pushed team file re-read.
  - **Acceptance test(s):** AT-601
  - **Boundary catalog (QC-3):** ☑ boundary (start only; due only; start = due already; clearing) ☑ invalid (no date: refused) ☐ empty — N/A ☐ error — N/A
  - **Negative control:** on base `M` is unbound (P-2): the file is unchanged → RED.

### HLR-602 — The gantt draws milestones as dates, not bars
- **Traceability:** US-602
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.3, LED-2026-10-04-batch-02.11
- **Statement:** In the gantt, the system shall draw a milestone's row as its label prefixed by `◆`, a `◆` on its date with the date written beside it and no bar, and a chip `in Nd`, `today`, `▲Nd` or `✓ done`; a late milestone in the over tone, an upcoming one in its project's hue, a reached one as `◆✓` with its label and date in the reached grey (LED .11), drawn among its group's open rows by date while the group has open work; the dependency gutter `↳` for a milestone as for any task; the ruler's month row shall mark the selected task's project's milestones with `◆` in the same tones; the one-line legend shall name `◆ milestone` and `◆✓ reached` when the frame draws them; `]` that leaves a milestone drawn shall say it was reached, not folded; and the arrow keys shall walk every drawn row.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt_milestones.py`
- **Numeric pass threshold:** on the shifted kg milestone board (§5) at 118×30, `3`, `Launch new homepage` selected: its row's label starts ` ◆ Launch new homepage`, its field cells hold `◆` and the `Mon D` of today+10 and no `╌`, chip `in 10d`; `Mockups approved`'s row holds `◆✓` and chip `✓ done`, its `◆`, `✓`, label and date in the reached grey (LED .11); `Security review sign-off`'s chip `▲2d` in the over colour; the month row holds a reached-grey `◆` at `Mockups approved`'s column; with `Revenue model signed off` selected the month row holds a `◆` in Data Warehouse's hue at its column (today+18, not the project due's); the legend row holds `◆ milestone` and `◆✓ reached` at 118×30 and 80×24; `↑` from `Build component library` selects `Mockups approved` and `↓` returns; `]` pressed on `Launch new homepage` until it reaches Done → at the last press one toast holding `reached` and none holding `folded`, and its row then holds `◆✓`; at 80×24 the selected milestone row is drawn with its chip; 0 failures.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** milestones read as dates with a distance, reached ones quiet, the ruler marks them.
  - **Shipped surface:** `TaskboardApp` keys `3`, `↓`/`↑` via `App.run_test`, painted screen segments.
  - **Acceptance test(s):** AT-602
  - **Boundary catalog (QC-3):** ☑ boundary (today; late; reached; off the window; no project; a group with only reached milestones and no open work) ☑ invalid (a milestone with no due: no `◆`, chip `no due`; S1 payload titles) ☐ empty — N/A ☐ error — N/A
  - **Negative control:** on base the milestone row draws as a plain task (P-3/P-4): no `◆` label prefix, no `in 10d`, no reached row → RED.

### HLR-603 — The kanban carries milestones on the band rule, never as cards
- **Traceability:** US-603
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.3, LED-2026-10-04-batch-02.4, LED-2026-10-04-batch-02.7, LED-2026-10-04-batch-02.8
- **Statement:** In the kanban, the system shall not draw a milestone as a card in any presentation, shall not count it in the header's `N tasks`, the `/` filter's `N/M tasks`, the column counts, the WIP tags, a band's `N open` / `N high ↑` or the fold row's counts, and shall never leave the selection on a milestone; in the grouped presentation with the project grouping, a project's band rule shall carry its milestones after its facts — the late ones first in the over tone, then the upcoming ones by date in the project's hue, then the most recently reached one with `✓` in the reached grey (LED .11) — each as `◆ ‹Mon D› ‹title› · ‹in Nd | today | Nd late›` (the reached one `◆ ‹Mon D› ‹title› ✓`), separated by `──`, cutting titles before dropping them, dropping titles before dates, and counting what does not fit as `+N ◆` (reached ones never counted); a project with no card in the kanban, open or done, draws no band.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_milestones.py`
- **Numeric pass threshold:** on the shifted kg milestone board (§5): at 118×30 grouped the header holds `25 tasks`, every column count and WIP tag equals the non-milestone cards in it, 0 milestone titles in any card cell; Website Redesign's rule holds, in order, `◆ ‹today+10›`, a prefix of `Launch new homepage` (cut with `…` as the room requires: the cut depends on the date's width that day), `· in 10d`, `──`, `◆ ‹today−12›`, a prefix of `Mockups approved`, `✓`, and its facts `4 open`; at 118×40 Ops & Security's rule holds `Security review sign-off · 2d late` in the over colour; `g` (priority grouping): no `◆` on any rule, the header still `25 tasks`; `tab` (matrix) and `tab` (lanes): no milestone in any cell, header `25 tasks`; nav walks no milestone; `M` on the selected card leaves the selection on a drawn card, and the next `]` moves that card; at 80×24 Website Redesign's rule holds `◆ ‹today+10› · in 10d`; 0 failures.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the columns hold only work; the band says what is coming and what was reached.
  - **Shipped surface:** `TaskboardApp` keys `4`, `tab`, `g`, `M`, `]`, arrows via `App.run_test`, painted screen segments.
  - **Acceptance test(s):** AT-603
  - **Boundary catalog (QC-3):** ☑ boundary (no room: dates only, `+N ◆`; a project with only a reached milestone; priority grouping; a high-priority milestone) ☑ invalid (an archived milestone: never shown; a milestone with no due: not on the rule; S1 payload title) ☐ empty — N/A ☐ error — N/A
  - **Negative control:** on base the milestone is a card in its column and counted → RED.

### HLR-605 — An existing board is offered milestones once, safely
- **Traceability:** US-605
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2
- **Statement:** When the app opens a readable board that carries no offer mark, as the last step of its start, the system shall: on a board with no candidate, record the mark and show nothing; otherwise open the offer — group "One-day tasks (start = due)" pre-checked, group "Due date, no start" unchecked, each row naming its project, its date and how many open tasks wait on it — where `space` toggles the highlighted row, `↵` converts exactly the checked rows that are still candidates and `esc` converts none; either answer shall record the mark, so the offer never shows again; quitting without an answer shall leave the board unmarked; converting shall first create, beside the board file, a backup holding the file's bytes as they stand immediately before the conversion and then a log of every conversion, never overwriting a file, then set each picked task's flag (start = due), record the mark and save atomically, say so naming the backup, and let `u` revert the conversion as one step (the mark stays); if the backup, the log or the save fails, the board file shall be left untouched and unmarked, the board in memory restored, and the reason said. A board `Board.load` seeds is created with the mark.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_milestone_offer.py`
- **Numeric pass threshold:** a one-day legacy board file (the shifted kg board with the three one-day tasks of §5, the renumber key, the links mark, no sweepable task, no offer mark): the offer paints 2 headings and 8 rows in the P-16 order, 3 `▣` and 5 `□`, `Partner notice emails` with `1 waits on it`, keys row `↵ convert 3`; `space` (on `Partner notice emails`) → `↵ convert 2`; `↓ ↓ ↓` `space` (on `Review pull requests`) → `↵ convert 3`; `↵` → the backup's bytes equal the file's bytes read before `↵`; the saved board holds exactly `tw5`, `tm5`, `to3` as milestones with start = due and `ta3` unchanged; the log lists exactly those 3; one toast starting `Milestones: 3 converted`; a fresh app on that file shows no offer and its gantt labels ` ◆ Launch new homepage`; on a second copy `↵` then `u` → the 3 back as before, the mark kept, and a fresh app shows no offer; `esc` instead → marked, 0 converted, no backup, no log, one toast starting `Not now`; a board with no candidate and a seeded board → marked, no offer; a backup that cannot be created → the board file byte-identical and unmarked, one error toast starting `Milestone offer stopped`, the app still running, and the next start offers again; 0 failures.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the old board is offered once; only what was picked is converted, backed up and logged — or nothing changes.
  - **Shipped surface:** `TaskboardApp` started on a board file on disk via `App.run_test(notifications=True)`, keys `↓`, `space`, `enter`, `escape`, `u`, `3`, and fresh starts on the written file (C-12 chain).
  - **Acceptance test(s):** AT-604, AT-605, AT-606
  - **Boundary catalog (QC-3):** ☑ boundary (nothing checked + `↵`; a pre-checked row unchecked; the backup name taken: `.1`; quit unanswered) ☑ empty (no candidate; a seeded board) ☑ error (backup fails: AT-606) ☑ invalid (a mark already present; a malformed mark; a chosen task no longer a candidate)
  - **Negative control:** on base no offer exists: the one-day tasks stay plain → RED.

## 4. Low-level requirements (LLR)

### LLR-601.1 — The flag in the model
- **Traceability:** HLR-601
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2
- **Statement:** `Task` shall carry a field `milestone: bool = False` (NEW), placed after `phase_changed` and before `extra`, serialized under the key `"milestone"` (every saved and pushed task carries it) and listed in `_TASK_KEYS`; `Task.from_dict` shall set it only when the stored value is the boolean `True` and shall never rewrite a stored start or due; `set_milestone(task, on)` (NEW, `models.py`) shall, for `on` true on a task with a readable due, set the flag and the start to the due; with only a readable start, set the flag and the due to the start; with neither, change nothing and return `MILESTONE_NEEDS_DATE`; for `on` false, clear the flag and nothing else; `bump_due` on a milestone shall set the start to the moved due.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_milestones.py -k "TC_601 or TC_602 or TC_603 or TC_607 or TC_608"`
- **Numeric pass threshold:** `from_dict` over `True`, `"true"`, `1`, `"yes"`, `[]`, `None`, absent → flag only for `True`; a stored milestone with start ≠ due loads with both dates unchanged; load → save → load keeps the flag; `set_milestone` over (start ≠ due, start only, due only, both equal, neither, unreadable text, clear) equals TC-602's table; `bump_due(+1)` on a milestone moves both dates, on a task only the due; TC-607: a team push writes `"milestone": true`, a teammate's `true` is pulled as a milestone and `"yes"` is not; TC-608: archive and unarchive (`x`), the `/` filter and a link (`depends_on`) leave the flag as it was; 0 failures.
- **Negative control:** `bool(value)` in place of `is True` → the `"yes"` arm RED; the due set from the start when both exist → the start ≠ due arm RED.
- **Boundary catalog:** ☑ boundary (start only; due only) ☑ invalid (non-boolean stored values; unreadable date text) ☑ empty (no date) ☐ error — N/A

### LLR-601.2 — `M`, its toasts and its undo
- **Traceability:** HLR-601
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.3
- **Statement:** `KEYMAP` shall bind `M` to `milestone_toggle`, label `Milestone`, group `task`, live in the lanes, agenda, gantt, kanban and focus views, in the more layer; `TaskboardApp.action_milestone_toggle` (NEW) shall, on the selected task, call `set_milestone(task, not task.milestone)`; when refused, notify the refusal (`severity="warning"`, `markup=False`) and write nothing; otherwise push one undo snapshot taken before the change, save, refresh and notify the set or clear toast of §1.6 (`markup=False`, the title cut at 40; `start was` only when the start moved; ‹where› "on the ‹project› band" only when a band will carry it — the kanban's grouped project grouping and a project with an open non-milestone card — else "shown on the gantt"); `_UNDO_FIELDS` shall include `start_date` and `milestone`; `milestone_toggle` is a board action.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_milestones.py -k TC_604`
- **Numeric pass threshold:** `M` on a dated task: one snapshot, flag set, saved; `u` restores flag and start; `M` on an undated task: 0 snapshots, 0 saves, one warning toast; `M` with no selection: nothing; ‹where› on a project's last open card and on an Inbox task is "shown on the gantt"; the `?` Keys section lists `M  Milestone` in those five views and not in flow, standup, people, setup; each of those five bars shows `M` or counts it in its `+N`; 0 failures.
- **Negative control:** a snapshot taken after the change → the `u` arm RED; `start_date` absent from `_UNDO_FIELDS` → the start-restore arm RED.
- **Boundary catalog:** ☑ boundary (no selection; clearing; the start moved or not) ☑ invalid (no date) ☐ empty — N/A ☐ error — N/A

### LLR-601.3 — The editor and the details view
- **Traceability:** HLR-601
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.5, LED-2026-10-04-batch-02.6, LED-2026-10-04-batch-02.9
- **Statement:** `TaskModal` shall add a `milestone` checkbox (`#f-milestone`, NEW) in the project/phase/priority half of the chip row and return it as the payload key `"milestone"` (the editor's widget ids become 18: canon LLR-001.3 amended); the app's edit handler shall apply every other field first and then, when the box is ticked, `set_milestone(task, True)` — the due is the date, so a start ≠ the due is replaced by the due, and the editor start toast says so when the task becomes a milestone or the user changed the start field — and when the box is unticked `set_milestone(task, False)`; a ticked box on a task with no date shall leave the task not a milestone and notify the editor refusal toast (`markup=False`); the add handler shall remove the key before building the task and apply it the same way; `TASK_CHIPS_ONE_ROW` shall be re-measured so every chip stays fully visible from 80 to 140 columns (`assumed — verify in Phase 3`); `TaskDetails` shall paint the phase row as `‹phase›[ · blocked][ · ◆ milestone]`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_milestones.py -k "TC_605 or TC_606"` and `pytest tests/test_edit_window.py`
- **Numeric pass threshold:** the box reflects the task; ticked + Save on a dated task → flag and start = due; ticked with a typed start ≠ due → start = due and one start toast; a milestone's due alone edited → no start toast; a task's box ticked alone (start ≠ due) → one start toast; a milestone saved with both dates cleared → not a milestone, one refusal toast; ticked on an undated task → the other edits saved, flag false, one refusal toast; a new task saved ticked with a due → created as a milestone; every chip's region inside the screen at 80, 100, 140 and the re-measured threshold N−1 and N; the details phase row of a milestone ends ` · ◆ milestone`; 0 failures.
- **Negative control:** the flag applied before the edited dates → the ticked-with-new-due arm RED (start = the old due).
- **Boundary catalog:** ☑ boundary (the fold width ±1) ☑ invalid (no date; a typed start ≠ due) ☐ empty — N/A ☐ error — N/A

### LLR-602.1 — The gantt plan holds the drawn rows
- **Traceability:** HLR-602
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.3
- **Statement:** `GanttGroup` shall gain `rows` (NEW): the group's open tasks and its reached milestones merged by due (`sort_by_due`, stable), the reached ones only when the group has open work; these readers shall move to `rows`: `gantt_plan`'s unfold budget, `_gantt_frame`'s selection test, span-row-only page, pin share and paging, and `nav_model("gantt")`; these stay on `open`: `gantt_window` (a reached row may draw off the window), the span row's chip, `_gantt_group_label`'s counts (a reached milestone counts in `✓n`, an open one in `N open`), `gantt_link_order` and the legend's fold test; `TaskboardApp._notify_folded` shall, for a milestone that `]` leaves drawn, notify the reached toast of §1.6 instead of "folded".
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_milestones.py -k TC_609`
- **Numeric pass threshold:** on the kg milestone board, Website Redesign's `rows` = its open tasks with `Mockups approved` merged by due (first); Mobile App (no reached milestone) `rows == open`; a group of only reached milestones has `rows == []`; nav order equals the painted row order at 118×30 and 80×24; with a reached milestone selected its group unfolds; `]` pressed on `Launch new homepage` until it reaches Done (four presses) → at the last one `reached` toast, no `folded` toast; 0 failures.
- **Negative control:** nav still walking `open` → the reached-row arm RED; `rows` unsorted → the date-order arm RED.
- **Boundary catalog:** ☑ boundary (selection on a reached milestone; paging) ☑ empty (no open work) ☐ invalid — N/A ☐ error — N/A

### LLR-602.2 — The milestone row
- **Traceability:** HLR-602
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.11
- **Statement:** `views.py` shall provide (NEW) `milestone_tone(task, board, today)` — the reached grey (`reached`) once reached (LED .11), `over` late, else the project's hue (`dim` with no project) — `gantt_milestone_cells(task, board, ax, today, tone)` — `◆` at the due's cell (`◆✓` when reached), the due written as `Mon D` one cell after it, or before it when it does not fit after, in `reached` / `over` / `mut`; an off-window due draws `◂`/`▸` at the edge and `◆` beside it; no due draws nothing — and `gantt_milestone_chip(task, board, today, width)` — `✓ done` reached, `▲Nd` over, `today` soon, `in Nd` mut, `no due` dim — and `_gantt_frame` shall label a milestone row ` ◆ ‹title›` (the `◆` in its tone, the title through the views' escape) with the shipped gutter.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_milestones.py -k TC_610`
- **Numeric pass threshold:** the tone and chip of the six kg milestones equal P-16's lines (`in 10d`, `in 35d`, `in 3d`, `✓ done`, `▲2d`, `in 18d`); today → `today`; cells: exactly one `◆` (two cells `◆✓` when reached), the date text adjacent, 0 `╌`/`━`/tip glyphs; off-window both sides; titles `[b]x[/b]`, `[/]` and one ending in `\` paint literally with no exception; 0 failures.
- **Negative control:** a reached milestone drawn in its project hue → the tone arm RED; `▲` for a due of today → the today arm RED; an unescaped title → the S1 arm RED.
- **Boundary catalog:** ☑ boundary (today; off-window left/right; label at the right edge) ☑ invalid (no due; S1 titles) ☐ empty — N/A ☐ error — N/A

### LLR-602.3 — The ruler marks, the legend and the help
- **Traceability:** HLR-602
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2
- **Statement:** `_gantt_frame` shall add to the month row's marks, after the project's due, a `◆` in `milestone_tone` at the cell of every visible milestone of the selected task's project whose due is in the window; `_gantt_legend` shall place `◆ milestone` and `◆✓ reached` (each only when drawn) right after the selection item, as the M-1 frames do; `legend_entries("gantt")` and `help_usage("gantt")` shall name them (each help bullet ≤ 44 cells).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_milestones.py -k TC_611`
- **Numeric pass threshold:** with `Launch new homepage` selected the month row's `◆` cells equal {project due, Launch, Mockups} ∩ window; with `Revenue model signed off` selected its cell holds a `◆` in Data Warehouse's hue; selecting a task of a project with no milestone adds none; the legend lists the two items only on a frame drawing them, at 118 and 80 (`assumed — verify in Phase 3`: the 80-column legend width); 0 failures.
- **Negative control:** marks taken from every project → the no-milestone-project arm RED; the items appended last → the 80-column arm RED.
- **Boundary catalog:** ☑ boundary (a milestone on the project due's cell; out of window; 80 columns) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-603.1 — A milestone is not a kanban card
- **Traceability:** HLR-603
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.3, LED-2026-10-04-batch-02.4, LED-2026-10-04-batch-02.7
- **Statement:** `kanban_plan`, `_kanban_matrix`, `_kanban_lanes` and the kanban branches of `nav_model` shall drop milestones from the tasks they lay out (one helper, `kanban_work`, NEW), so no card, `N tasks`, `/` filter count (`render_view`'s kanban branch), column count, WIP tag, band `N open`/`N high ↑` or fold-row count includes a milestone; `TaskboardApp._select_first` shall, in the kanban (every presentation), never keep a milestone selected: it moves to the first card of the nearest drawn column at or left of its phase, in the presentation's own column order (the grouped `z` rule).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_milestones.py -k TC_612`
- **Numeric pass threshold:** in the three presentations and every sort/group mode: 0 milestone ids in `line_map` and nav; `N tasks` and each column tag equal the non-milestone counts; the high band holds no milestone; a milestone selected on entering the kanban (from the gantt) is replaced by a drawn card in each presentation, including a lanes window that does not start at the first phase; `/` with a term matching only a milestone paints `0/25 tasks` and no card; 0 failures.
- **Negative control:** one presentation not filtering → its arm RED (the set of presentations is derived from `render_kanban`'s branches, C-31); `_select_first` unchanged → the matrix arm RED.
- **Boundary catalog:** ☑ boundary (a high-priority milestone; a blocked one; focus on its project) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-603.2 — The band rule's milestones
- **Traceability:** HLR-603
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.8, LED-2026-10-04-batch-02.11
- **Statement:** `band_milestones(board, project, today, show_archived)` (NEW) shall return the project's visible, non-archived, dated milestones in the order late (by due), upcoming (by due), then the one reached milestone with the latest due; `_band_facts` shall append them, after ` ── `, through a layout (NEW) that in the band room gives as many as possible a title of ≥ 8 cells — the first ones whole first — then shows dates only, then `── +N ◆` for the open ones left out, and when not even one date fits, `+N ◆` alone if it fits; tones: late `◆`, date and relative in over; upcoming `◆` in the project hue, date ink, relative mut (`today` in soon); reached all in the reached grey (LED .11); titles `hd` (the reached grey when reached); every title a literal piece (S1); only bands whose project is a `Project` (the project grouping) carry them; `band_rule_facts` (NEW) is the one seat for a rule's facts, read by the renderer and by `legend_entries("kanban")`, which names `◆` exactly when a rule draws one (it takes the kanban's presentation, grouping and focus); `help_usage("kanban")` names it.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_milestones.py -k TC_613`
- **Numeric pass threshold:** the order per project equals P-16's `_ms_bits` lines; over the unshifted kg milestone board the segment text at rooms 70, 40, 20 equals `p1-thresholds.txt` and at the shipped rooms 56/62/50/69/59 and 18/24/31/21 equals `p1-thresholds-shipped.txt`; API Platform at room 12 → `+1 ◆`; a `[b]x[/b]` title paints literally; 0 failures.
- **Negative control:** reached counted in `+N` → RED; late after upcoming → RED.
- **Boundary catalog:** ☑ boundary (the rooms above; zero room) ☑ invalid (S1 payload title; no due) ☐ empty — N/A ☐ error — N/A

### LLR-605.1 — The candidates
- **Traceability:** HLR-605
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2
- **Statement:** `milestone_candidates(board)` (NEW) shall return `(task, preset)` for every board task (the first of a repeated id) that is a candidate (§1.3): `preset` true for group 1, false for group 2; ordered group 1 first, then by due, then board order; `milestones_marked(settings)` (NEW) shall read the offer mark totally (any non-dict `migrations` or a non-int or other value is unmarked).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_milestone_offer.py -k TC_614`
- **Numeric pass threshold:** over the kg one-day board the list equals P-16's 8 rows in order; done, archived, milestone, undated, start ≠ due, unreadable-start and non-text-title tasks excluded; `milestones_marked` over `{"milestones": 1}` true, over `1.0`, `"1"`, `True`, `[]`, a list `migrations` false; 0 failures.
- **Negative control:** `bool(start)` grouping a start ≠ due task as due-only → RED.
- **Boundary catalog:** ☑ boundary (start = due; due today) ☑ invalid (malformed marks; repeated id; a non-text title) ☑ empty (no candidate) ☐ error — N/A

### LLR-605.2 — Convert, back up, log, mark, once
- **Traceability:** HLR-605
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.3, LED-2026-10-04-batch-02.4, LED-2026-10-04-batch-02.10
- **Statement:** `run_milestone_offer(board, chosen, today)` (NEW) shall return `None` on an unreadable load or a marked board; otherwise re-read the candidates and convert, each at most once, the candidates whose id is in `chosen`, counting the chosen ids no longer candidates; when there are conversions, or when a present non-1 mark value is replaced, it shall first read the resolved board file's bytes once and create beside it the backup `<board file name>` + `MILESTONE_BACKUP`, then the log `<board file name>` + `MILESTONE_LOG` (each `.1`, `.2`, … when taken, by exclusive create — B1's `_create_beside`), the log holding the date, the backup's name, the replaced mark value, a `note` that restoring the backup brings back an unmarked board which is offered again, and per conversion the id, title, start before and after; then set each one's flag through `set_milestone`, set the mark (keeping the `migrations` dict's other keys) and `save_atomic`; otherwise set the mark and save without a backup or log; on any `OSError` it shall first restore each converted task's flag and start and the previous `migrations` value, then remove the files this run created on a best-effort basis (their errors swallowed), leave the file untouched, and return the first error (basename and `strerror` only).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_milestone_offer.py -k TC_615`
- **Numeric pass threshold:** backup bytes == the file's bytes read before the call (also after an earlier save in the same run); names taken → `.1`; the log's records equal the conversions; the `links` key kept; a repeated chosen id → one record; a chosen task no longer a candidate → not converted, counted; a second call returns `None` and writes nothing; a failing backup, log or save each leave the file byte-identical, unmarked and the tasks as before; a failing cleanup `unlink` still restores and returns the first error; a malformed mark replaced → backup and log written, the log holding the old value; every log holds the `note` (a restored backup is offered again); a team pull over the folder sees no extra user; 0 failures.
- **Negative control:** backup after the apply → the bytes arm RED; no mark → the second-call arm RED; cleanup before restore → the failing-unlink arm RED.
- **Boundary catalog:** ☑ error (backup, log, save, cleanup fail) ☑ boundary (names taken) ☑ empty (none chosen) ☑ invalid (marked; malformed mark; unreadable; repeated id; ineligible id)

### LLR-605.3 — Offered once at start, said, undone
- **Traceability:** HLR-605
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.10
- **Statement:** `Board.load` shall seed a new board carrying both marks (`{"links": 1, "milestones": 1}`); the last step of `TaskboardApp.on_mount` (after the team start, whose identity picker it covers until answered) shall be the offer step: nothing on an unreadable load or a marked board; `run_milestone_offer(board, [])` when there is no candidate (a failure here is silent: no offer was shown); otherwise push the offer and on its answer run `run_milestone_offer(board, answer)`; on conversions push one undo entry under its own key `milestones`, holding every converted task's flag, start and due as stored, and notify the conversion toast (`markup=False`, timeout 30 s, `· K no longer eligible` when K > 0); with none converted, the none toast (timeout 30 s); on a failure the failure toast (severity error, `markup=False`) and keep running; `action_undo` shall restore every task of a `milestones` entry, keep the mark, and notify the undo toast; teammates see conversions at the next push.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_milestone_offer.py -k TC_616`
- **Numeric pass threshold:** exactly one `Milestones:` toast; `u` once restores all and saves, mark kept; the failure toast holds the basename and no separator-bearing path; a seeded board has the mark and shows no offer; `↵` with nothing checked = `esc`; an unreadable load: no offer; a board needing the link migration and the offer: two toasts, two undo entries, `u` reverts the offer first; quitting with the offer open leaves the board unmarked; a read-only board with no candidate: no toast; 0 failures.
- **Negative control:** an undo entry per task → the one-step arm RED; an unmarked seed → the seeded arm RED (an offer of 11 due-only rows).
- **Boundary catalog:** ☑ boundary (one conversion; three; quit unanswered) ☑ error (backup fails; read-only, silent) ☑ empty (seeded; no candidate) ☑ invalid (unreadable load)

### LLR-605.4 — The offer screen
- **Traceability:** HLR-605
- **Ledger:** LED-2026-10-04-batch-02.1, LED-2026-10-04-batch-02.2, LED-2026-10-04-batch-02.9, LED-2026-10-04-batch-02.10
- **Statement:** `MilestoneOffer` (NEW, `modals.py`) shall paint a centred box inside the screen: the offer title with the count, the explanation line, an option list `#offer-list` (NEW) holding the group-1 heading (disabled), its rows, the group-2 heading (disabled), its rows — each row `▣`/`□` (only the box coloured), the title cut with `…` to the cells the row leaves, then `‹project or Inbox› · ‹Mon D›[ · N wait(s) on it]` in the dim tone, every user string (titles and project names) a Text piece — and the keys row (§1.6) with `N` the checked count; the first row is highlighted at open and the list scrolls the highlighted row into view; `space` toggles the highlighted row and repaints it and the keys row (on a heading it does nothing); `↵` dismisses with the checked candidates' own ids, taken by option index; `esc` dismisses with none.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_milestone_offer.py -k TC_617`
- **Numeric pass threshold:** over the kg one-day board: 2 headings + 8 rows in P-16's order, 3 `▣`; `space` on a row flips it and `N`; `↵` returns exactly the checked ids (an int id returned as the int); `esc` returns `[]`; a title and a project name `[b]x[/b]` paint literally; at 80×24 with 34 candidates the box is inside the screen, the title and the keys row are painted in full and `↓` to the last row brings it into view; 0 failures.
- **Negative control:** the row prompt built with markup → the payload arm RED; `↵` returning every row → RED.
- **Boundary catalog:** ☑ boundary (one group empty; 80×24 with 34 candidates) ☑ invalid (S1 payload title and project name; a non-string id) ☐ empty — N/A ☐ error — N/A

## 4b. Information Flow Contract (IFC)

Part A always. Part B: yes — `#f-milestone` and `#offer-list` are NEW addressable widgets; each block
is added by the increment that creates it, as a ledger amendment (B1 D-514, `V14`).

```
FLOW: milestones, from the board file to the screen and back
  SOURCE : the board file on disk and teammates' board.<user>.json (milestone, start_date, due_date, settings); the user's keys
  NODES  :
    - fn    : Task.milestone / Task.from_dict / set_milestone / bump_due
      owner : LLR-601.1
    - fn    : KEYMAP M / action_milestone_toggle / _UNDO_FIELDS
      owner : LLR-601.2
    - fn    : TaskModal milestone box / the add and edit handlers / TaskDetails phase row
      owner : LLR-601.3
    - fn    : GanttGroup.rows / gantt_plan / nav_model gantt / _notify_folded
      owner : LLR-602.1
    - fn    : milestone_tone / gantt_milestone_cells / gantt_milestone_chip
      owner : LLR-602.2
    - fn    : month-row marks / _gantt_legend / legend_entries gantt / help_usage gantt
      owner : LLR-602.3
    - fn    : kanban_work and its callers / _select_first kanban
      owner : LLR-603.1
    - fn    : band_milestones / the band-rule layout / kanban help and legend
      owner : LLR-603.2
    - fn    : milestone_candidates / milestones_marked
      owner : LLR-605.1
    - fn    : run_milestone_offer (backup, log, mark, atomic save)
      owner : LLR-605.2
    - fn    : Board.load seeded marks / on_mount offer step / toasts / the milestones undo entry
      owner : LLR-605.3
    - fn    : MilestoneOffer
      owner : LLR-605.4
  SINK   : the painted screen, the saved board file, its backup and its log, the pushed board.<user>.json
```

```
COMPONENT: editor-milestone
  PARENT : SYSTEM
  SURFACE: the task editor (key e)
  INPUTS : board: Board ; task: Task
  OUTPUTS:
    - id          : milestone-box
      value       : the task's milestone flag, as the payload key "milestone"
      address     : "#f-milestone"
      consumers   : taskboard/modals.py::TaskModal ; taskboard/app.py::TaskboardApp ; tests/test_milestones.py ; tests/test_edit_window.py
      owner       : LLR-601.3
```

```
COMPONENT: milestone-offer
  PARENT : SYSTEM
  SURFACE: the one-time offer at start
  INPUTS : board: Board ; candidates: list
  OUTPUTS:
    - id          : offer-rows
      value       : the group headings and the candidate rows, in candidate order
      address     : "#offer-list"
      cardinality : 2 headings at most + the candidates, INDEXED POSITIONALLY
      consumers   : taskboard/modals.py::MilestoneOffer ; tests/test_milestone_offer.py
      owner       : LLR-605.4
```

## 5. Validation strategy

Layer A (`TC-601` through `TC-617`) and Layer B (`AT-601` through `AT-606`, one node each — C-18) are
pytest nodes carrying their id in docstring and name, in `tests/test_milestones.py` (TC-601..608,
AT-601), `tests/test_gantt_milestones.py` (TC-609..611, AT-602), `tests/test_kanban_milestones.py`
(TC-612, TC-613, AT-603), `tests/test_milestone_offer.py` (TC-614..617, AT-604..606). The ATs drive
`TaskboardApp` with real keys (C-16) over a board file in `tmp_path`.

**The boards.** `tests/kg_board.py` gains `one_day(board)` and `milestones(board)`, re-derived from
`variants_round5.one_day_board` / `milestone_board`, relative to the board's own today: `tw5` (+10),
`tm5` (+35), `ta3` (+3) one-day; `milestones` flags them and adds `tw0` "Mockups approved" (done,
−12, waits on `tw1`), `to0` "Security review sign-off" (Next, −2), `td0` "Revenue model signed off"
(Backlog, +18, waits on `td4`; `td5` waits on it). The AT board is the shifted board
(`kg_board.shifted`) so transformed, carrying the renumber key and saved; TC-613's exact segments use
the unshifted board (the prototype's own TODAY).

**The fixture seam (P-9, D-611).** The offer is a modal at mount: 274 app starts in 251 tests would
open it. `tests/conftest.py` (NEW) holds one autouse fixture that patches the app module's reference
`taskboard.app.milestones_marked` to answer True unless the test carries the marker
`milestone_offer` (registered there); every node of `test_milestone_offer.py` carries it. Unmarked
tests therefore start as if the board had already answered the offer, and the base suite's file I/O is
unchanged. Two seam controls in `test_milestone_offer.py`: an unmarked node on a candidate board sees
no offer and no file write by the offer step; a marked node on the same board sees the offer. After
increment 004 the census is re-run: ≥ 274 suppressed starts, 0 offer screens in unmarked nodes.

**Captures:** 118×30 and 80×24, base and close, shifted board (`capture_b2.py`, PLAN.md PV).

| AT | Story | Drives (the HLR's threshold) |
|---|---|---|
| AT-601 | US-601 | `3` `↓` `M` `+` `u` `e`; the pushed team file |
| AT-602 | US-602 | `3` `↑` `↓` `]` at 118×30 and 80×24 |
| AT-603 | US-603 | `4` `tab` `g` `M` `]`; Ops at 118×40 |
| AT-604 | US-605 | the offer, `space` `↓` `↵`; fresh apps; `u` (C-12) |
| AT-605 | US-605 | `esc`; no candidate; a seeded board |
| AT-606 | US-605 | a failing backup (stdlib `open` refusing `.pre-milestones`); the next start |

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion shown RED on the base tree or by a recorded mutation.
- each existing node the batch changes is listed in its increment's reverse census.
- full suite: 0 failures other than a declared environment flake.

## 6. Appendices

### 6.2 Relevant design decisions

| Id | Decision | Why |
|---|---|---|
| D-601 | B2a only; US-604 → BACKLOG as B2b | pre-authorized split; P-17 |
| D-602 | family A judged not fired | no module created or moved; the synced format: D-603 |
| D-603 | the flag is a `Task` field after `phase_changed`, not `extra`; every saved and pushed task now carries `"milestone": false` — additive: older apps keep it as an unknown key and write it back, so no schema version | one typed seat read by every view (P-1) |
| D-604 | key `M` (shifted, like `L`), more layer, task group | `m` stays free for B2b's dependents mode; `c` is Clocks (P-2) |
| D-605 | the due is the date; no date → refused; clearing keeps start = due | round 5 |
| D-606 | every reached milestone is a row while its group has open work; it counts in `✓n`; open milestones count in the gantt's `N open` | M-1 frame |
| D-607 | a milestone is never a kanban card or selection; only the project grouping's band rule carries it | M-2 |
| D-608 | the offer opens when either group has a candidate | commission |
| D-609 | a failed conversion keeps the app running; the offer returns next start | nothing misread (cf. D-518) |
| D-610 | `u` keeps the mark | B1 D-517 |
| D-611 | the test seam patches `taskboard.app.milestones_marked` (`tests/conftest.py`), opted out by `milestone_offer` | P-9; A-10 |
| D-612 | the offer's backup holds the bytes immediately before the conversion | A-2 |
| D-613 | date writers: `set_milestone`, `bump_due`, the editor/add handlers; load and pull never normalize; a milestone is read by its due | A-3 |
| D-614 | `]` on a drawn milestone says "reached"; the kanban never selects a milestone | A-4, UX-1 |
| D-615 | the offer is `on_mount`'s last step; quitting unanswered leaves the board unmarked | A-7, UX-14 |
| D-616 | a mark-only write that fails with no offer shown is silent | A-8, S-8 |
| D-617 | `Board.load` seeds a new board with both marks | A-9 |
| D-618 | the keys row says `esc not now — won't ask again` | UX-2 |
| D-619 | a band rule with no room for one date shows `+N ◆` alone when it fits | P-18: API Platform at 80 has 12 cells |
| D-620 | candidates re-read at answer time; the toast counts the converted and the ineligible | S-5, S-6 |
| D-621 | replacing a malformed mark forces the backup and the log (old value kept) | S-7 |
| D-622 | the kanban header excludes milestones (the M-2 frame's header reads 31, its columns 25) | Q-10, UX-5 — PV-610 |
| D-623 | a project with no card, open or done, draws no band | A-11, UX-11; BACKLOG |
| D-624 | the legend items sit after the selection item | UX-4: the M-1 frames' order, kept at 80 |
| D-625 | a task whose title is not text is never a candidate | S-9 (the shipped crash → BACKLOG) |

### 6.3 Open risks
The scan's flags (`evidence/p1-security-scan*.txt`) are answered by: backup first, exclusive create, atomic save, restore before cleanup, fail-closed, `u`, run-once (C5: LLR-605.2/3); the flag read only as boolean true, teammates' tasks never in the offer (C6: LLR-601.1); Text pieces and S1 payload arms on every new surface (C8: LLR-602.2, LLR-603.2, LLR-605.4); basename-only failure text (LLR-605.3).
