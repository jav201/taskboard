# Requirements Document — taskboard — Batch 2026-10-04-batch-01

> Live contract (current state only). Mode `core`. Language `en`. The append-only ledger is
> `01-requirements-ledger.md`. Template: flow `templates/req-template.md` (reserved field
> names kept literal). Ids use a batch-disjoint `5xx` range (`US-501`, `HLR-501`,
> `LLR-501.1`, `AT-501`, `TC-501`): `0xx`..`4xx` are taken in the record and the canon.
> Iteration 2 (P2 iteration 1 folded).

## 1. Introduction

### 1.1 Purpose
Batch B1 of the `kg_mejoras` plan (§Batch B, split per D-501). Today a link exists only through `b` (Blocked), unseen and never released (`DEPS-CONTRACT.md`; P-1, P-2). This batch makes a link mean *waits on*, independent of Blocked, shows it, edits it, guards it, and migrates the links a board already holds.

### 1.2 Scope
In: rules 1–4 and 9′ (the derived waiting state, marks); `L` through the picker (D-B2) and the gantt link mode (D-A), loops refused, undo (rules 5–8); the details section (D-B); the guard on every archive and delete path; the one-time link migration with the operator's safeguard; the README. Out (D-501, `BACKLOG.md`): milestones, moving linked dates, the M-3 offer; batch C (chain map, key `6`); teammates' tasks (never linked, marked or migrated); S-6 (pre-existing).

### 1.3 Definitions
| Term | Definition |
|------|------------|
| link | an id in a task's `depends_on`: the task (the *waiter*) waits on the task with that id (the *predecessor*) |
| board task | a task in `board.tasks`; a teammate's task (team sync) is never one |
| open | a board task neither in the board's last phase nor archived |
| live link | a link whose id names a board task other than the waiter; an id repeated in `depends_on` is one link |
| waiting | an open task with at least one open predecessor over a live link |
| ready | an open task with at least one live link and no open predecessor |
| overlap | the one measure (`cascade.overlap`, plan note a): for a waiter with a start date, `pred.due − waiter.start + 1` days, floored at 0 (both days count); for a waiter with no start, `pred.due − waiter.due` days, floored at 0; 0 when either date it needs is absent |
| conflict | an open predecessor whose overlap with an open waiter is ≥ 1 (rule 9′ under the one measure, D-503, PV-7) |
| external block | the `blocked` flag (`▲`): a block with no task to point at; independent of links |
| migration mark | `settings["migrations"]` is a dict whose `links` value is exactly `1` |

### 1.4 References
`prototypes/kg_mejoras/` (worktree `kg-mejoras`): `IMPLEMENTATION-PLAN.md` §Batch B, `NOTES.md` rounds 3/5/6, `DEPS-CONTRACT.md`, `deps_logic.py`, `cascade.py`, the D-B, D-B2, D-A, D-A2, D-marks frames; the S1 rule of `2026-10-02-batch-04`; `02-review.md`.

## 2. Overall description

### 2.1 Product perspective
`depends_on` (`models.py:783`) is written only by `b` (`app.py:761-822`, `BlockerPicker`) and read by `unblocks_count`, `critical_chain`, `card_cell`, `_card_meta`, `gantt_dep_mark` and the `unblock` sort; `blocked` is written by `b`, the editor's box and the legacy `status` load, and read by `status_glyph`, `_flowing`, the sorts, the lanes and the legend (`views.py:238,2113,4367-4382,4944-4955,989,5559`).

### 2.3 User characteristics
One operator at a terminal (80×24 to full screen, keyboard first).

### 2.4 Constraints
Textual 8.2.8, Rich 15.0.0, Python 3.12; no new dependency; the board file format keeps every
field (`depends_on` and `blocked` keep their names and types; one new settings key).

### 2.5 Assumptions
- A1: only `b` writes `depends_on` (`app.py:806-807`, `819-820`); `blocked` has three writers (§2.1), so the migration's rule names the cases it cannot tell apart (D-515, D-516, §6.3).
- A2: the operator's real board is never opened by this batch; the migration is exercised on synthetic boards only (standing authorization).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-501 | As a taskboard user, I want a task to wait on other tasks without being marked Blocked, and to see on each card how many open tasks it waits on (`◂N`) and how many open tasks wait on it (`▸N`), and to be told once when a task becomes ready, so that I know what can start. | `DEPS-CONTRACT.md` rules 1–4; plan §Batch B row 1 | READY |
| US-502 | As a taskboard user, I want one key, `L`, to say "this task waits on…" — from a picker anywhere, or by pointing at a bar on the gantt — and to have a loop refused with its path, so that linking is quick and never corrupts the plan. | rules 5–7; round-3 verdict (both surfaces); D-B2, D-A | READY |
| US-503 | As a taskboard user opening a task's details, I want to see what it waits on and what it unblocks (direct and down the chain), remove a link, add one, and jump to a linked task, so that I can manage links where I read the task. | D-B; round-3 verdict | READY |
| US-504 | As a taskboard user, I want archiving or deleting an open task that open tasks still wait on to be refused with their names, so that no waiting task is left pointing at nothing. | round-3 ruling | READY |
| US-505 | As the operator with an existing board, I want the links my board already holds migrated once to the new meaning — with a backup taken first, every change logged, a way back, and never a second run — so that work I had unblocked is not silently blocked again. | rounds 3 + 5; `deps_logic.migrate`; operator safeguard "Respaldo automático + deshacer" | READY |

#### Refinement log

| Story | INVEST | Feasibility | Classification |
|---|---|---|---|
| US-501 | I N V E S T ✓ | `models.py` derivations, `views.py` marks, `app.py` keys (increment 002) | READY |
| US-502 | all ✓ (two surfaces, two increments; C-16: prototype interactions verified through real keys) | picker (003), link mode (004) | READY |
| US-503 | all ✓ | `TaskDetails` (003) | READY |
| US-504 | all ✓ | `app.py` / `modals.py` paths (002, 003) | READY |
| US-505 | all ✓ | `models.py` + `app.py` (001) | READY |

B2 — OUT (D-501): milestones, moving linked dates and the M-3 offer → `BACKLOG.md`.

RC-1 (b), already shipped? — none (`evidence/p0-probes.txt` §RC-1 (b)).

### 2.7 Premise evaluation (C-43)

| # | Premise | Tier | Verdict | Executed evidence | Disposition |
|---|---|---|---|---|---|
| P-1 | On base, `b` opens `BlockerPicker`; picking sets `blocked=True` and appends the id; `b` again clears the flag and keeps the id | premise | ✅ TRUE | `evidence/p1-premises.txt` §P-1 | HLR-501, HLR-505 (A1) |
| P-2 | On base, the predecessor's card paints `⛓N`, the waiting card nothing; the gantt gutter marks a task whose only predecessor is ARCHIVED and does not flag a start ON the predecessor's due day | premise | ✅ TRUE | `p1-premises.txt` §P-2 | LLR-501.2, LLR-501.3 |
| P-3 | On base, `x` archives and `d` deletes an open task an open task waits on; the waiter keeps the dangling id | premise | ✅ TRUE | `p1-premises.txt` §P-3 | HLR-504 |
| P-5 | On base, the details view paints no dependency | premise | ✅ TRUE | `p1-premises.txt` §P-5 | HLR-503 |
| P-8 | Textual's `OptionList` paints a two-line `Text` prompt literally and its cursor skips a disabled option | premise | ✅ TRUE | `p1-premises.txt` §P-8 | LLR-502.2, LLR-503.1 |
| P-10 | The undo stack holds one task per entry (`_snapshot` → `task_id`, `fields`) and `depends_on` and `blocked` are in its fields | premise | ✅ TRUE | `p1-premises.txt` §P-10 | LLR-502.1, LLR-505.3 |
| P-11 | `deps_logic.py` re-executed over today's `taskboard` prints output identical to the verdict's `out/deps-logic.txt`; its migration lands L1..L6 on the stated rule and all invariants hold | premise | ✅ TRUE | `evidence/p1-deps-logic-rerun.txt` | LLR-501.1, LLR-505.1 |
| P-12 | Base suite at `0447070`: 2218 passed, exit 0, in 339.95 s | premise | ✅ TRUE | `evidence/base-suite.txt` | test ledger base |
| P-13 | `L`, `m` and `6` are unbound at base; `c` is Clocks | premise | ✅ TRUE | `evidence/p0-probes.txt` §keys | LLR-502.1 |
| P-14 | No `edit bar`, `milestone` or `date_links` exists in `taskboard/` at base | premise | ✅ TRUE | `grep -n -i` over `taskboard/*.py` → 0 lines | D-501 |
| P-15 | The contract's thresholds (counts, overlaps, loop path, chain, releases) executed with the prototype's rule functions over the kg board | premise | ✅ TRUE | `evidence/p1-thresholds.txt` | HLR-502, HLR-503, LLR-501.1, LLR-501.4 |
| P-16 | The TC-503, TC-509, TC-513 oracle tables, generated with the prototype's rule functions (all six timing forms and the loop form reached) | premise | ✅ TRUE | `evidence/p1-tables.txt` sha256 `0583fb00…` (`p1_tables.py`) | LLR-501.1, LLR-502.2, LLR-503.1 |
| P-17 | On base the first app start rewrites the board file before anything else could (renumber notice, old-done sweep) — so the migration must be `on_mount`'s first act | premise | ✅ TRUE | qa P2 probe3 | LLR-505.3 |
| P-18 | The kg board would be changed by the migration at mount (8 tasks), so every app-driven test board that holds links must carry the mark | premise | ✅ TRUE | qa P2 probe2 | §5 fixture seam |

- **Premise evaluation:** 15 premise(s) · ✅ TRUE 15 / ❌ FALSE 0 / ❓ UNDECIDABLE 0

### 2.8 Fork preconditions (C-52)
- **Fork preconditions:** none — this batch runs one lane

## 3. High-level requirements (HLR)

### HLR-501 — A link means "waits on", and the board shows it
- **Traceability:** US-501
- **Ledger:** LED-2026-10-04-batch-01.1, LED-2026-10-04-batch-01.6, LED-2026-10-04-batch-01.11, LED-2026-10-04-batch-01.14
- **Statement:** The system shall treat each live link as "the waiter waits on the predecessor", independent of the external block; shall paint on each open card `◂N` for its N open predecessors and `▸N` for the N open tasks that wait on it, and never `⛓`; shall let `b` toggle only the external block; and when a predecessor reaches the last phase and a task stops waiting because of it, shall say once "‹title› is ready — ‹predecessor› done".
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_links.py`
- **Numeric pass threshold:** on the kg board shifted to today (§5), marked, in kanban grouped and lanes at 118×40 (every band drawn from 33 rows grouped, 20 lanes — `evidence/p2-kanban-height.txt`; guard: cards observed = open tasks): the painted marks are the board's — `◂` 7 of 8 grouped (the high-band `Deprecate v1 endpoints` keeps its tag, A-3), 8 of 8 lanes; `▸` 8 of 8 — tone muted, 0 `⛓`; `b` opens no screen and leaves `depends_on` byte-equal; `]` twice on `Audit dependencies` produces exactly 1 toast "Add push notifications is ready — Audit dependencies done" and `◂` leaves its card; a further `]` on another task adds 0 such toasts; 0 failures.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the cards say who waits and who is waited on; finishing work says what became ready; `b` marks an outside block only.
  - **Shipped surface:** `TaskboardApp` keys `4`, `tab`, `]`, `b` via `App.run_test(notifications=True)`, painted screen.
  - **Acceptance test(s):** AT-501
  - **Boundary catalog (QC-3):** ☑ boundary (a waiter that is also `▲`: "(still ▲ blocked)"; a done predecessor: no `◂`; two predecessors, one done: `◂1`) ☑ invalid (a dangling id and a self id: not counted) ☐ empty — N/A ☐ error — N/A
  - **Negative control:** on base the waiting card paints nothing and the predecessor `⛓1` (P-2); `b` opens the picker (P-1) → RED.

### HLR-502 — `L` links from a picker or from the gantt, and refuses loops
- **Traceability:** US-502
- **Ledger:** LED-2026-10-04-batch-01.2, LED-2026-10-04-batch-01.7
- **Statement:** When `L` is pressed on a selected task, the system shall let the user choose a task it waits on — from a picker that lists open tasks of the same project first, then by due date, filters as the user types, marks an already-linked task as removable and a loop candidate as unavailable with its path, and offers to create a new task to wait on; or, in the gantt, from a link mode that draws the proposed link live with its overlap days in the over tone — and shall add the link, remove it when it already exists, refuse a link that would close a loop naming the loop's path, and make each add or removal one undo step.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_link_picker.py tests/test_gantt_link.py`
- **Numeric pass threshold:** picker over the shifted kg board: candidate order equals TC-509's table; 0 done/archived candidates; the filter `ma` leaves the 4 titles containing it; with `SEO redirects map` waiting on `Launch new homepage`, `L` on `Launch new homepage` shows that row disabled with "⟲ would loop: this → SEO redirects map → this"; ↵ on a candidate adds exactly that id (the saved file re-read); ↵ on a linked row removes it; `u` restores the previous `depends_on`; create adds one task in the waiter's project, first phase, no dates, and links it. Gantt: `L` paints `GANTT · LINK` and "24 candidates · ⟲1 would loop"; ↑/↓ move over the open tasks skipping the loop row; for waiter `tw5` and candidate `tm3` the waiter's row paints `═` in the over tone on exactly the overlap days that fall in the window; 0 connector cells in the label column; ↵ links; esc changes nothing; 0 failures.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** one key links, showing what it means first; loops refused with their path.
  - **Shipped surface:** `TaskboardApp` keys `L`, letters, `backspace`, `↑`/`↓`, `enter`, `escape`, `u` in kanban and gantt via `App.run_test(notifications=True)`.
  - **Acceptance test(s):** AT-502, AT-503
  - **Boundary catalog (QC-3):** ☑ boundary (a candidate with no due; a waiter with no start; a cross-project candidate; an empty filter; a filter matching nothing) ☑ invalid (a loop; the task itself; a done task; S1 payload titles) ☐ empty — N/A ☐ error — N/A
  - **Negative control:** on base `L` is unbound (P-13): nothing opens → RED.

### HLR-503 — The details view shows and edits a task's links
- **Traceability:** US-503
- **Ledger:** LED-2026-10-04-batch-01.3, LED-2026-10-04-batch-01.8
- **Statement:** When the details view of a task is opened, the system shall paint a dependency section listing the tasks it waits on and the open tasks it unblocks — directly and down the chain — with each predecessor in conflict named with its overlap, and shall let the user remove the highlighted direct link, add a link through the picker, and jump to a linked task.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_details_links.py`
- **Numeric pass threshold:** on the shifted kg board, `enter` on `Add push notifications` paints `Waits on` with `Audit dependencies`, "▸1 direct · 2 in chain", `Offline sync` (direct) and `└ Beta release to testers`, and the conflict line naming `Audit dependencies` with "overlaps … by 2d"; `x` on the `Waits on` row removes `tm2` from `tm3.depends_on`, `x` on the `Unblocks` row removes `tm3` from `tm4.depends_on` (board and file); `↵` closes the view and the painted selection is the linked task; `L` opens the picker for the task and, after a link, the section repaints with it; every title painted exactly (the S1 payload set); 0 failures.
- **Priority:** medium
- **Acceptance (black-box):**
  - **Observable outcome:** both directions of every link, editable in place.
  - **Shipped surface:** `TaskboardApp` key `enter`, then `tab`, `x`, `enter`, `L` in the details view via `App.run_test`.
  - **Acceptance test(s):** AT-504
  - **Boundary catalog (QC-3):** ☑ empty (a task with no link: "no links — L adds one") ☑ boundary (a done predecessor listed as done; a dangling id not listed; a waiter with no start: the due form of the conflict line) ☑ invalid (the S1 payloads in titles) ☐ error — N/A
  - **Negative control:** base paints no dependency (P-5) → RED.

### HLR-504 — Work others wait on is not archived or deleted
- **Traceability:** US-504
- **Ledger:** LED-2026-10-04-batch-01.4, LED-2026-10-04-batch-01.9
- **Statement:** When the user archives (`x`, the editor's archived box, or a project's archive) or deletes an open task that open tasks outside what is being archived wait on, the system shall refuse, naming the waiting tasks, and change nothing; a predecessor in the last phase shall archive and delete as before, and the done-only sweeps and the project delete shall be unchanged.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_links.py -k AT_505`
- **Numeric pass threshold:** for `x`, `d` and the editor's archived box on `Partner notice emails` (open; `Deprecate v1 endpoints` waits on it): the task stays unarchived and present, 0 confirm dialogs for `d`, one toast naming `Deprecate v1 endpoints`, the board file unchanged but for the editor's other fields; archiving the project `Mobile App` while `Deprecate v1 endpoints` (API Platform) is made to wait on `Audit dependencies` is refused naming it; `x` on a done predecessor archives it; `X` archives done work as before; 0 failures.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** refused, naming who waits.
  - **Shipped surface:** `TaskboardApp` keys `x`, `d`, `e`, `P` via `App.run_test(notifications=True)`.
  - **Acceptance test(s):** AT-505
  - **Boundary catalog (QC-3):** ☑ boundary (a done predecessor; an archived waiter does not count; a waiter inside the archived project does not count; restoring is never refused) ☑ invalid (two waiters, both named; more than 3: "and N more") ☐ empty — N/A ☐ error — N/A
  - **Negative control:** base archives and deletes (P-3) → RED.

### HLR-505 — An existing board's links are migrated once, safely
- **Traceability:** US-505
- **Ledger:** LED-2026-10-04-batch-01.5, LED-2026-10-04-batch-01.10
- **Statement:** When the app opens a readable board that carries no migration mark, the system shall, before any other write, migrate its links by the legacy rule — first creating a byte-identical backup of the board file and a log of every change, never overwriting a file, then applying the changes, recording the mark and saving atomically — shall say so naming the backup, shall let `u` revert every change as one step, shall never migrate a board that carries the mark, and, if the backup, the log or the save fails, shall leave the board file untouched and stop with the reason.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_link_migration.py`
- **Numeric pass threshold:** a legacy board file holding the eight shapes of §5, without the renumber key and with one done task older than 20 days: after mount the backup's bytes equal the pre-start file's bytes; the saved board holds the rule's result for each shape; the log lists exactly the changed tasks with before and after; exactly one toast starting `Links migrated`; `u` restores every changed task's `blocked` and `depends_on` and the mark stays; a second app start leaves the board, the backup and the log byte-identical and shows no `Links migrated` toast; a board needing no change gets the mark and no backup or log; a backup that cannot be created leaves the file byte-identical and unmarked and the app exits with a one-line reason holding no directory path; 0 failures.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the old board opens migrated once, backup and log beside it — or does not open.
  - **Shipped surface:** `TaskboardApp` started on a board file on disk via `App.run_test(notifications=True)`, key `u`, and a second start (C-12 chain).
  - **Acceptance test(s):** AT-506, AT-507, AT-508
  - **Boundary catalog (QC-3):** ☑ boundary (a released link to a done task kept; a dangling blocker keeps the flag; the backup name already taken) ☑ empty (no links: AT-507) ☑ error (backup fails: AT-508) ☑ invalid (a mark already present; a malformed mark)
  - **Negative control:** on base no migration exists (L2 keeps both ids) → RED.

## 4. Low-level requirements (LLR)

### LLR-501.1 — The waiting state is derived from live links, at bounded cost
- **Traceability:** HLR-501
- **Ledger:** LED-2026-10-04-batch-01.6, LED-2026-10-04-batch-01.13
- **Statement:** `models.py` shall provide (NEW) `is_open`, `open_predecessors`, `open_dependents`, `link_marks`, `dependents_chain`, `link_overlap`, `link_conflicts`, `loop_path` and `waiting_ids` over board tasks only, such that: a predecessor or dependent counts only over a live link and once per id; a closed task has no open predecessors and no open dependents; `link_marks` builds `(◂, ▸)` per task from one reverse index; `dependents_chain` lists the open tasks that wait on the task, directly (depth 1) or down the chain, each once; `link_overlap` is the one measure (§1.3); `loop_path(waiter, pred)` searches every stored live link, closed tasks included, and returns `waiter → pred → … → waiter` or `None`; every derivation looks tasks up through one id map, terminates on a cyclic stored graph and recurses nowhere.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_links.py -k "TC_501 or TC_502 or TC_503 or TC_518"`
- **Numeric pass threshold:** over the kg board and each of the 11 session states of `deps_logic.py` (§5): `waiting(t) == (◂ > 0)` for every task, `Σ◂ == Σ▸`, closed tasks carry `(0, 0)`; `loop_path(tm2, tm5)` = Audit → Beta → Offline → Add push → Audit; `link_overlap` equals TC-503's table row by row; a teammate's task depending on a local id adds no `▸`; on a stored 2-cycle every derivation returns; the hostile boards (a chain of 5000, one task with 100 000 ids, a dense 800-task board) each derive in < 1 s (a dense rotating closed board: < 2 s, D-526) with no `RecursionError` (TC-518); 0 failures.
- **Negative control:** a closed task counted, a duplicate id counted twice, a dangling id counted, `<` in place of `≤` at the due day, a cycle search skipping closed tasks, a recursive search → the named arm RED.
- **Boundary catalog:** ☑ boundary (start on the due day = 1; the day after = 0) ☑ invalid (dangling, self, duplicate ids; a stored cycle) ☑ empty (no links) ☐ error — N/A

### LLR-501.2 — Cards paint `◂N` and `▸N`, never `⛓`
- **Traceability:** HLR-501
- **Ledger:** LED-2026-10-04-batch-01.6, LED-2026-10-04-batch-01.14, LED-2026-10-04-batch-01.21, LED-2026-10-04-batch-01.23
- **Statement:** `card_cell` and `_card_meta` (`views.py`) shall take the `link_marks` map in place of the unblock count and paint, for an open task, `▸M` then `◂N` (each only when ≥ 1) in the muted tone where `⛓M` stood, and nothing for a closed task or a task absent from the map; the meta tokens shall shed from the left in the order `↗`, `▤`, age, `▸`, `◂`, project tag, due; every caller (derived: every call of `card_cell` / `kanban_card` in `views.py`) shall pass one map per render; `help_usage` and `help_example` for the kanban shall say what `◂N`, `▸N` and `L` mean. In lanes the title keeps 6 cells (or its whole length) before any token (A-10): the age sheds first, then `▸`, then the rest from the left, and `◂` last (A-12, operator D-533).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_links.py -k TC_504`
- **Numeric pass threshold:** for every task of the kg board, `kanban_card` and `card_cell` at widths 9, 12, 24 and 40 paint `◂N`/`▸M` equal to `link_marks`, 0 `⛓`; under width pressure `▸` is shed before `◂` and `◂` before the due token; the derived caller set is ≥ 4 and every caller passes the map (AST); the kanban help names `◂N`, `▸N` and `L`; 0 failures.
- **Negative control:** a caller still passing the unblock count → that caller's arm RED; `▸` on a done task → RED.
- **Boundary catalog:** ☑ boundary (widths 9, 12, 24; a task with both marks; a teammate's task) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-501.3 — The gantt gutter and the flow packet read the same rule
- **Traceability:** HLR-501
- **Ledger:** LED-2026-10-04-batch-01.6
- **Statement:** `gantt_dep_mark` shall mark a task only when it has an open predecessor (archived ones excluded) and shall paint the mark in the over tone exactly when `link_conflicts` is non-empty; `_flowing` shall be false for a waiting task as for a blocked one; `status_glyph`, the lanes `▲`, the sorts' blocked-first order and the legend shall keep reading the external flag only (D-519).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_links.py -k TC_505`
- **Numeric pass threshold:** `ta2` with `ta3` archived → blank; `tw5` starting on `tw4`'s due day → over; one day later → not over; the critical-chain and muted arms as base; a waiting task in a middle phase → `_flowing` false, the same task once its predecessor is done → true; 0 failures.
- **Negative control:** base `gantt_dep_mark` → the archived and due-day arms RED (P-2).
- **Boundary catalog:** ☑ boundary (start on / after the due day) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-501.4 — `b` is the external block; done releases waiters once
- **Traceability:** HLR-501
- **Ledger:** LED-2026-10-04-batch-01.6
- **Statement:** `action_toggle_blocked` shall flip `blocked` on the selected task, push one undo snapshot and save, opening no screen and leaving `depends_on` unchanged; `action_phase_move` and `_on_task_edited` shall compute `waiting_ids` before and after the mutation and, for each task that stopped waiting while a predecessor entered the last phase in that mutation, notify `markup=False` "‹title› is ready — ‹pred› done" (predecessors joined by ", ", titles clipped to 40), with " (still ▲ blocked)" appended when the task is blocked — at most 3 such toasts, then one "+K more ready"; a link removed by hand, an undo and a phase rename or delete release silently (D-508, D-524).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_links.py -k TC_506`
- **Numeric pass threshold:** `b` twice on a linked task: `depends_on` unchanged, `blocked` True then False, 0 screens pushed; `]` on `Audit dependencies` (Doing → Review) → 0 toasts, then `]` (→ Done) → 1 toast "Add push notifications is ready — Audit dependencies done"; finishing `Build component library` → exactly 1 toast, for `Optimize image assets`, none for `Launch new homepage`; the editor moving a predecessor to the last phase → the same toast; a blocked waiter → the suffix; 5 waiters released at once → 3 toasts + "+2 more ready"; `u` after a release → 0 toasts; 0 failures.
- **Negative control:** base `b` opens `BlockerPicker` (P-1) → RED; a toast on every `]` → the count arm RED.
- **Boundary catalog:** ☑ boundary (a waiter with two predecessors finishing the second; 5 released at once) ☑ invalid (a hand-removed link: silent) ☐ empty — N/A ☐ error — N/A

### LLR-502.1 — `L`, link, unlink, undo
- **Traceability:** HLR-502
- **Ledger:** LED-2026-10-04-batch-01.7
- **Statement:** The keymap shall bind `L` to `link` (label `Link`, group `task`, primary layer, views lanes, agenda, gantt, kanban, focus); `action_link` shall do nothing without a selected task and otherwise open the gantt link mode in the gantt and the picker elsewhere; the app shall add a link only when `link_refusal` (NEW) returns `None` — refusing the task itself, a closed predecessor and a loop with "would create a loop: ‹path›" (titles clipped to 40, a path longer than 6 shortened in the middle with "…") — and remove an existing one, each as one undo snapshot of the waiter, saving and notifying `markup=False` "‹waiter› waits on ‹pred› · u undo" / "‹waiter› no longer waits on ‹pred› · u undo"; `BlockerPicker` shall be removed.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_link_picker.py -k "TC_507 or TC_508"`
- **Numeric pass threshold:** `L` bound once, no other row changed (keymap diff = one row); `L` painted in the primary key bar at 80×24 in kanban and gantt, any key it pushes off counted in the reverse census; link then `u` → `depends_on` equal to before; unlink then `u` → equal; a loop refused with its path and `depends_on` unchanged; `grep BlockerPicker taskboard/` → 0; 0 failures.
- **Negative control:** a link written before the refusal check → the loop arm RED; base: `L` unbound → RED.
- **Boundary catalog:** ☑ invalid (self, closed, loop; no selection) ☑ boundary (re-link after unlink; a 9-task loop path shortened) ☐ empty — N/A ☐ error — N/A

### LLR-502.2 — The picker (D-B2)
- **Traceability:** HLR-502
- **Ledger:** LED-2026-10-04-batch-01.7, LED-2026-10-04-batch-01.16
- **Statement:** `LinkPicker` (NEW, `modals.py`) shall paint the title "‹waiter› waits on…", a filter input (`#link-filter`), the count "N of M open", the line "linked now: …", a create row ("+ create “‹filter›” as a new task it waits on", or "+ create a new task it waits on" with an empty filter), then the candidates of `link_candidates` (NEW, `models.py`) under "Same project" and "Other projects" as two-line options of `#link-list` — the title, the phase and due (with the project name for other projects), and a hint: "✓ linked (↵ removes) · ‹timing›" for a linked one, "⟲ would loop: this → … → this" (disabled) for a loop, else the timing hint of `link_hint` (NEW): "◂ overlaps Nd: due ‹date›, this starts ‹date›", "◂ overlaps Nd: due ‹date›, this is due ‹date›", "ok — due Nd before this starts", "ok — due on or before the day this is due", "no due date — timing can't be checked" or "this has no dates — timing can't be checked"; candidates are the open board tasks but the waiter, the waiter's project first, then by due (undated last), then title; the loop set is computed once per open; the filter keeps titles containing it, case-insensitively; the highlight starts on the first candidate; ↑/↓ move, ↵ chooses, esc cancels; ↵ on the create row with an empty filter asks for a title; a created task is in the waiter's project, first phase, no dates, its title through `strip_controls` and non-empty; every user text is a Text piece.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_link_picker.py -k "TC_509 or TC_510"`
- **Numeric pass threshold:** for waiters `tw5`, `ta2`, `to4` (precondition `tw6` waits on `tw5`) the candidate order and every hint equal TC-509's table (`evidence/p1-tables.txt`), each of the six timing forms and the loop form reached (derived, guard == 7); the filter `ma` leaves 4 of 24; the S1 payloads in titles painted exactly; 0 failures.
- **Negative control:** a candidate list including a done task, an unsorted list, a loop row selectable → RED.
- **Boundary catalog:** ☑ boundary (empty filter; filter matching nothing: only the create row) ☑ invalid (S1 payloads; a control-only created title) ☐ empty — N/A ☐ error — N/A

### LLR-502.3 — The gantt link mode (D-A)
- **Traceability:** HLR-502
- **Ledger:** LED-2026-10-04-batch-01.7, LED-2026-10-04-batch-01.18, LED-2026-10-04-batch-01.19, LED-2026-10-04-batch-01.20
- **Statement:** `GanttLinkMode` (NEW, `modals.py`) shall paint the gantt for the board with the candidate as its selection (so its group unfolds) and the waiter's group as the previous one, the header `GANTT · LINK` with "N candidates · ⟲K would loop" (N = the open tasks the gantt draws, but the waiter; one the view hides is reached from the picker — A-7, D-527), `⟲` in each loop row's gutter, and three status rows built as Text pieces (A-7): "LINK ‹waiter› waits on… ‹candidate›" with "filter: ‹text›▏" when one is typed ("✓ linked" for a linked candidate; "no match" with `↵` doing nothing when the filter matches nothing), the candidate's `link_hint`, and the keys (with "‹waiter› is folded — a taller terminal draws the link", or "waiter row folded" where the row is short, when the frame cannot draw an open waiter's row — A-8) "↑↓ choose · type to filter · ↵ link · esc cancel" ("↵ unlink" for a linked candidate) followed, room permitting, by the legend "⟲ loop: this → ‹path› → this" for the first loop; at 80 columns titles are clipped before any key is dropped; the cursor starts on the first non-loop candidate in gantt order; ↑/↓ shall move over the open tasks in gantt order, skipping loop candidates and, with a filter, tasks whose title does not contain it; every printable key is filter text and `backspace` edits it; `gantt_link_overlay` (NEW, `views.py`) shall draw on the field only — never in the label or gutter columns — a connector from the cell after the candidate's due toward the waiter's row in the bright tone over background cells only, and, for a waiter with a start, the overlap days on its row as `═` in the over tone (none for a waiter with no start); ↵ links or unlinks through the app's path, esc cancels; the frame repaint is the census's one new EXEMPT entry (the views seat, D-405). The waiter's group is pinned open in the fold allocation and paged to the waiter; when the candidate's and the waiter's groups cannot both be drawn whole they share the rows left; the folded-row note is the fallback only (A-9).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt_link.py -k "TC_511 or TC_512"`
- **Numeric pass threshold:** for waiter `tw5` and candidate `tm3` on the kg board at 118×30: the `═` cells on `tw5`'s row are exactly the columns of the overlap days inside the window; every connector cell lies right of the gutter; the cycle skips the loop row; all four keys painted at 80×24; 0 failures.
- **Negative control:** an overlay writing into the label column, `═` over one day too many → RED.
- **Boundary catalog:** ☑ boundary (candidate above / below the waiter; the due off the window; no overlap; no start) ☑ invalid (S1 payload titles in the status rows) ☐ empty — N/A ☐ error — N/A

### LLR-502.4 — The README says it
- **Traceability:** HLR-502
- **Ledger:** LED-2026-10-04-batch-01.7
- **Statement:** `README.md` shall list `L` in its key table, describe `b` as the external block, and describe links (`◂N`, `▸N`, the picker, link mode, the details section, the guard, the one-time migration with its backup, its log and the restore-the-backup path) with no `⛓`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_readme.py tests/test_keymap.py`
- **Numeric pass threshold:** the README key table equals the keymap (the shipped check); 0 `⛓` in `README.md`; 0 failures.
- **Negative control:** `L` bound with the README unchanged → the shipped README/keymap check RED.
- **Boundary catalog:** ☐ boundary — N/A ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-503.1 — The details dependency section (D-B)
- **Traceability:** HLR-503
- **Ledger:** LED-2026-10-04-batch-01.8, LED-2026-10-04-batch-01.11, LED-2026-10-04-batch-01.16, LED-2026-10-04-batch-01.17
- **Statement:** `TaskDetails` shall paint, after the info grid, the heading `Dependencies` (with "◂ waiting", "ready" or nothing), `Waits on` with "◂N open of M", one row per live predecessor (title, phase, due, and the predecessor's own state `open`/`done`/`archived`; the count over those states; no `waiting`/`ready` note on a closed task — A-6), `Unblocks` with "▸N direct · K in chain" (K counting direct and chain), one row per open direct dependent and one `└` row per further chain task, one conflict line per conflict — "◂ starts ‹date›, overlaps ‹pred› by Nd (due ‹date›)" or, for a waiter with no start, "◂ due ‹date›, overlaps ‹pred› by Nd (due ‹date›)" — and the empty text "no links — L adds one"; the direct rows are the options of `#deps-list`, chain rows disabled; the section's heading shall carry "L link · tab links · x remove · ↵ jump" (`tab`, `x`, `↵` only when a link exists), the title row kept as accepted (A-5); the box keeps focus as today and `tab` moves focus to the list and back, leaving the board's layout unchanged; `x` removes the highlighted direct link through the app's unlink path (a `Waits on` row edits this task, an `Unblocks` row the dependent) and repaints; `↵` dismisses, clears focus and search, and selects the linked task (an archived one with archived hidden: "‹title› is archived — v shows it"); `L` opens the picker for the task and repaints after it; every user text a Text piece.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_details_links.py -k TC_513`
- **Numeric pass threshold:** the section's rows for `tm3`, `tw5`, `ta2` and `to4` equal TC-513's table (`evidence/p1-tables.txt`); a no-start waiter paints the due form; after `x` the section is repainted without the row; 0 failures.
- **Negative control:** a chain row selectable, a dangling id listed, `x` removing the wrong direction → RED.
- **Boundary catalog:** ☑ empty (no links) ☑ boundary (done predecessor; a waiter that is also blocked; no start) ☑ invalid (S1 payload titles) ☐ error — N/A

### LLR-504.1 — The guard, on every path
- **Traceability:** HLR-504
- **Ledger:** LED-2026-10-04-batch-01.9, LED-2026-10-04-batch-01.15
- **Statement:** `archive_refusal` (NEW, `models.py`) shall return, for an open task with open dependents outside a given set, "can't ‹archive|delete› ‹title› — N open task(s) wait on it (‹up to 3 titles›[ and K more]). Finish it, or remove the link in its details (↵, then x)." with real singular and plural forms, and `None` otherwise; `action_archive` (when archiving), `action_delete` (before its confirm and again in `_on_delete`), `_on_task_edited` (when the edit, its phase applied first, would archive: the other fields are applied and the toast adds "— other changes saved") and the project archive (outside waiters of any of its open tasks) shall notify it with `markup=False`, severity warning, and leave the task or project as it was; in the Setup view `x` removes a setup row and never touches a task (A-4); the sweep, `X` and the project delete are unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_links.py -k TC_517`
- **Numeric pass threshold:** the refusal text for one, two and five waiters; `None` for a done predecessor, for a task whose only waiter is archived, for a waiter inside the archived set, and for an unarchive; 0 undo snapshots pushed by a refusal; 0 failures.
- **Negative control:** base: archive and delete succeed (P-3) → RED.
- **Boundary catalog:** ☑ boundary (done predecessor; archived waiter; waiter inside the project) ☑ invalid (two and five waiters) ☐ empty — N/A ☐ error — N/A

### LLR-505.1 — The legacy rule
- **Traceability:** HLR-505
- **Ledger:** LED-2026-10-04-batch-01.10, LED-2026-10-04-batch-01.11
- **Statement:** `migrate_links` (NEW, `models.py`) shall return, without changing the board, one change per board task whose links or flag the rule changes, processing tasks in board order: drop dangling and self ids and duplicates; a blocked task whose last stored id is live and OPEN keeps that link and loses the flag (logged "flag cleared — press b if this was an outside block", A2-1); a blocked task whose last stored id is live and CLOSED keeps the flag (D-515); a blocked task whose last stored id is not live keeps the flag; every other id pointing at an open task is dropped; ids pointing at a closed task are kept; any link that would close a loop over the links already kept is dropped, and a blocker so dropped leaves the flag kept (D-516); each change carries the task id, title, before and after `blocked` and `depends_on`, and a note.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_link_migration.py -k TC_514`
- **Numeric pass threshold:** the eight shapes of §5 land as listed there (L1..L6 as `deps_logic.py` asserts, L7/L8 by D-516/D-515); the board unchanged by the call; 0 failures.
- **Negative control:** keeping released links to open tasks, clearing the flag of L5 or L8, keeping both links of L7 → RED.
- **Boundary catalog:** ☑ boundary (released link to a done task; last link done) ☑ invalid (dangling, self, duplicate; a 2-cycle) ☑ empty (no tasks) ☐ error — N/A

### LLR-505.2 — Backup, log, mark, once, atomically
- **Traceability:** HLR-505
- **Ledger:** LED-2026-10-04-batch-01.10, LED-2026-10-04-batch-01.11, LED-2026-10-04-batch-01.12, LED-2026-10-04-batch-01.13, LED-2026-10-04-batch-01.22
- **Statement:** `run_link_migration` (NEW, `models.py`) shall do nothing on a board whose load was unreadable or that carries the migration mark (§1.3; any other `migrations` value is unmarked, replaced, and recorded in the log); otherwise, when `migrate_links` returns changes, it shall resolve the board path once and create, beside the resolved file, the backup `<board file name>.pre-links-migration` (`.1`, `.2`, … when taken, by exclusive create, never through an existing name) holding the board file's bytes, then the log `<board file name>.links-migration-log` (numbered the same way) holding the date, the backup's name and the changes as JSON, then apply the changes, set the mark and save by writing a random exclusive `.<board file name>.<random>.tmp` beside it and replacing the resolved file with it; with no change it shall set the mark and save the same way without a backup or log, unless a malformed mark was replaced, which forces both; any failure shall undo the in-memory changes, remove the files this run created, leave the board file untouched and unmarked, and return the failure (basename and `strerror` only); a repeated task id is left as it is. A read-only board file is refused before anything is written, the error naming the board, and the save's temp file never outlives a failure (A-11).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_link_migration.py -k TC_515`
- **Numeric pass threshold:** backup bytes == pre-call file bytes; an existing backup and log name untouched, `.1` used; a dangling symlink at the name counts as taken; the log's records equal the change list; mark set; a second call returns `None` and writes nothing; a marked board, a `migrations` of list / str / `{"links": 0}`: the first is untouched, the others migrate; an unreadable load: nothing written; a failing backup, log or save each leave the file byte-identical and unmarked; a team pull over the board's folder holding the backup and the log sees no extra user; 0 failures.
- **Negative control:** a backup taken after the apply (bytes differ) → RED; no mark → the second call migrates → RED; a backup named `board.pre-links-migration.json` → the team-pull arm RED.
- **Boundary catalog:** ☑ error (backup, log, save fail) ☑ boundary (names taken; symlink) ☑ empty (no change) ☑ invalid (mark present; malformed mark; unreadable load)

### LLR-505.3 — Migrated first at start, said once, undone with `u`
- **Traceability:** HLR-505
- **Ledger:** LED-2026-10-04-batch-01.10, LED-2026-10-04-batch-01.11, LED-2026-10-04-batch-01.12
- **Statement:** The first act of `TaskboardApp.on_mount` shall be `run_link_migration`, before any other board write; when it changed tasks the app shall push one undo entry holding every changed task and notify `markup=False`, timeout 30 s, "Links migrated: N task(s) · backup ‹basename› · u undo" (real singular and plural); `action_undo` shall restore every task of a multi-task entry (skipping a task purged since), keep the mark, and notify "Links migration undone — the old links now read as waits"; on a failure the app shall exit, printing after the terminal is restored "Link migration stopped: ‹reason›. The board file was not changed. Free space or write access in the board's folder, or run taskboard --board on a copy." holding no directory path (D-518: exit rather than open unmigrated).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_link_migration.py -k TC_516`
- **Numeric pass threshold:** exactly one `Links migrated` toast; `u` once restores every changed task's `blocked` and `depends_on` and saves, the mark stays; a purged task in the entry skipped; the failure exit message holds the basename and no separator-bearing path; 0 failures.
- **Negative control:** an undo entry per task (N steps) → the one-step arm RED; the migration after the renumber save → the backup-bytes arm RED.
- **Boundary catalog:** ☑ boundary (one changed task; eight) ☑ error (backup fails) ☐ empty — N/A ☐ invalid — N/A

## 4b. Information Flow Contract (IFC)

Part A always (each node's in/out is named by its owning LLR). Part B: yes — `#link-list`, `#link-filter`, `#deps-list` are NEW addressable widgets; each block is added by the increment that creates it, as a §6.5 amendment (D-514, `V14`).

```
FLOW: links, from the board file to the screen and back
  SOURCE : the board file on disk (depends_on, blocked, settings); the user's keys
  NODES  :
    - fn    : run_link_migration (backup, log, mark, atomic save)
      owner : LLR-505.2
    - fn    : migrate_links
      owner : LLR-505.1
    - fn    : TaskboardApp.on_mount migration, its toast and the multi-task undo
      owner : LLR-505.3
    - fn    : is_open / open_predecessors / open_dependents / link_marks / dependents_chain / link_overlap / link_conflicts / loop_path / waiting_ids
      owner : LLR-501.1
    - fn    : card_cell / _card_meta and their callers
      owner : LLR-501.2
    - fn    : gantt_dep_mark / _flowing
      owner : LLR-501.3
    - fn    : action_toggle_blocked / action_phase_move / _on_task_edited (ready)
      owner : LLR-501.4
    - fn    : action_link / link_refusal / link and unlink with undo
      owner : LLR-502.1
    - fn    : LinkPicker / link_candidates / link_hint
      owner : LLR-502.2
    - fn    : GanttLinkMode / gantt_link_overlay
      owner : LLR-502.3
    - fn    : README.md key table and links section
      owner : LLR-502.4
    - fn    : TaskDetails dependency section
      owner : LLR-503.1
    - fn    : archive_refusal and its four callers
      owner : LLR-504.1
  SINK   : the painted screen, the saved board file, its backup and its log
```

```
COMPONENT: link-picker
  PARENT : SYSTEM
  SURFACE: the picker `L` opens
  INPUTS : board: Board ; waiter: Task
  OUTPUTS:
    - id          : candidates
      value       : the create row, then the candidates by section, in rule order
      address     : "#link-list"
      cardinality : 1 + headings + open tasks but the waiter, INDEXED POSITIONALLY
      consumers   : taskboard/modals.py::LinkPicker ; tests/test_link_picker.py ; tests/test_markup_sites.py
      owner       : LLR-502.2
    - id          : filter
      value       : the typed filter
      address     : "#link-filter"
      consumers   : taskboard/modals.py::LinkPicker
      owner       : LLR-502.2
```

```
COMPONENT: details-links
  PARENT : SYSTEM
  SURFACE: the task details view (key enter)
  INPUTS : task: Task ; board: Board
  OUTPUTS:
    - id          : link-rows
      value       : headings, direct rows, disabled chain rows
      address     : "#deps-list"
      cardinality : the task's links, INDEXED POSITIONALLY
      consumers   : taskboard/modals.py::TaskDetails ; tests/test_details_links.py
      owner       : LLR-503.1
```

## 5. Validation strategy

Layer A (`TC-501`..`TC-518`) and Layer B (`AT-501`..`AT-508`, one node each — C-18) are pytest
nodes carrying their id in their docstring and name. The ATs drive `TaskboardApp` with real keys (C-16) over a board file in `tmp_path`.

**The fixture seam (Q-1, Q-3).** `tests/kg_board.build` marks its board (`settings["migrations"] =
{"links": 1}`: it is new-model data). The AT board is that board shifted to today — every date and
`phase_changed` moved by `date.today() − TODAY` — and saved. Only AT-506..508 start on an unmarked
file. The migration increment re-censuses every test that starts `TaskboardApp` over a board holding
a link or a blocked task, and marks or re-derives it (named in its packet).

**The legacy board (AT-506, TC-514).** The prototype's shapes over the kg board's tasks `tm2`,
`to1`, `to2`, `ta1`, `td1` (unmarked, no renumber key, one done task stamped 30 days ago):

| Shape | Stored | Lands as (`blocked`, `depends_on`) |
|---|---|---|
| L1 | blocked, `[tm2]` | `(False, [tm2])` |
| L2 | blocked, `[to1, to2]` | `(False, [to2])` |
| L3 | `[ta1]` (released, open) | `(False, [])` |
| L4 | `[td1]` (released, done) | `(False, [td1])` — no change record |
| L5 | blocked, `[gone1]` (dangling) | `(True, [])` |
| L6 | blocked, `[]` | `(True, [])` — no change record |
| L7 | `L7a` blocked `[L7b]`, `L7b` blocked `[L7a]` (both open) | `L7a (False, [L7b])`, `L7b (True, [])` (D-516) |
| L8 | blocked, `[td1]` (last link done) | `(True, [td1])` — no change record (D-515) |

**The oracle tables (Q-6, Q-7, Q-13)** are `evidence/p1-tables.txt` (sha256 `0583fb00…`), generated
by `p1_tables.py` with the prototype's own rule functions over the unshifted kg board; each TC
holds its rows as literals. TC-503 (the one measure):

| Case | waiter start | waiter due | pred due | overlap |
|---|---|---|---|---|
| start before the due day | 10-08 | 10-20 | 10-10 | 3 |
| start ON the due day | 10-10 | 10-20 | 10-10 | 1 |
| start the day after | 10-11 | 10-20 | 10-10 | 0 |
| no start, due before pred due | — | 10-07 | 10-10 | 3 |
| no start, due ON pred due | — | 10-10 | 10-10 | 0 |
| no start, due after | — | 10-12 | 10-10 | 0 |
| pred has no due | 10-01 | — | — | 0 |
| waiter has no dates | — | — | 10-10 | 0 |

TC-509 (72 rows) and TC-513 (titles, states, counts, conflict text; `tw5` without TC-509's precondition) are in the evidence verbatim, unshifted; the ATs compare order, counts and day counts.

**The session states (Q-17)** — TC-501's input set (guard ≥ 11) is the 11 steps of `deps_logic.py`'s session (`evidence/p1-deps-logic-rerun.txt`).

Captures: 118×30 and 80×24, base and close, every changed surface (`PLAN.md` PV table); colour claims are asserted from painted segments.

| AT | Story | Drives |
|---|---|---|
| AT-501 | US-501 | marks painted in grouped and lanes; `b` toggles `▲` with no picker; `]` to done → one ready toast, `◂` gone |
| AT-502 | US-502 | `L` → picker: order, exclusions, filter, loop row disabled with its path, ↵ link (file re-read), ↵ unlink, create (both branches), `u` |
| AT-503 | US-502 | gantt `L` → link mode: header and counts, `⟲` rows, candidate cycle, filter echo and no-match, connector and `═` in the field only, linked candidate, ↵ link, esc cancel, S1 payload titles |
| AT-504 | US-503 | `enter` → section rows and conflict line; `tab`, `x` on each direction; `↵` jumps (painted selection); `L` from details repaints |
| AT-505 | US-504 | `x`, `d`, the editor's archived box and the project archive refused with the waiter named; a done predecessor archives |
| AT-506 | US-505 | legacy file → backup byte-equal (its first name taken: `.1`), migrated board, log, one toast; `u` reverts; a second start changes nothing (C-12: the file the app wrote, re-read by a fresh app) |
| AT-507 | US-505 | a board needing no change → marked, no backup, no log, no `Links migrated` toast |
| AT-508 | US-505 | backup creation fails (a stdlib `open` patched to raise only for names holding `.pre-links-migration`) → file byte-identical, unmarked, the app exits (its exit message read) |

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion shown RED on the base tree or by a recorded mutation.
- each existing node the batch changes is listed in its increment's reverse census.
- full suite: 0 failures other than a declared environment flake.

## 6. Appendices

### 6.2 Relevant design decisions
- D-501: Run B1 only; B2 → `BACKLOG.md` (pre-authorized split; P-14).
- D-502: Trigger family A judged not fired: the dependency logic stays in `models.py` beside `unblocks_count` / `critical_chain`, no module created (as D-401).
- D-503: One overlap measure (`cascade.overlap`): a start on the predecessor's due day is a 1-day conflict (P-2); one wording "overlaps Nd" (PV-7).
- D-504: `b` is the external block only; `BlockerPicker` is retired, its "create a new blocker" living on as the picker's create row.
- D-505: The gantt keeps its one-cell `↳` gutter (the A1 verdict) on the open-predecessor rule; `◂N`/`▸N` are card marks (PV-2).
- D-506: Card marks muted like `⛓`, `▸` shed before `◂`; on cards `◂` always carries a count (PV-1).
- D-507: The dependency section lives in `TaskDetails` (`enter`); the full-screen editor (TaskModal C) is unchanged (PV-4).
- D-508: Only reaching the last phase releases a waiter with a toast; at most 3 toasts, then "+K more ready".
- D-509: ↵ on an already-linked picker row removes it without a second confirm.
- D-510: The link-mode filter narrows the candidate cycle; no gantt row is hidden.
- D-511: The migration runs once, as the first act at start; backup and log only when it changes something; the mark is set either way.
- D-512: Loops are judged over every stored live link, closed tasks included.
- D-513: The kanban `unblock` sort keeps `unblocks_count`.
- D-514: IFC Part B blocks for the NEW addressable widgets are written by the increments that create them (`V14`).
- D-515 (operator: "Sí, conservarla"): a blocked task whose last live link is closed keeps its flag — the flag may have been set by the editor after that link was done; the link is kept as satisfied.
- D-516: In the migration a current blocker whose kept link would close a loop is dropped and the flag kept.
- D-517 (operator: "Sí, no vuelve a correr"): `u` restores every changed task and keeps the mark, so the migration never re-runs on its own; the old links then read as waits (said in its toast). A restored backup file is unmarked and migrates at the next start (README).
- D-518: Fail closed: a failed backup, log or save leaves the file untouched and the app exits with the reason.
- D-519: every `blocked` reader keeps the external flag; `_flowing` also stops for a waiting task (unchanged motion: such a task was blocked before).
- D-520: Backup and log by exclusive create, numbered names; an atomic save.
- D-521: The backup and log names put the suffix after the full board file name, so team pull's `board.*.json` never matches them.
- D-522: Bounded cost: one id map, iterative searches, one reverse-reachability pass for the picker's loop set.
- D-523: The project archive is refused when an open task outside the project waits on one of its open tasks.
- D-524: A phase rename or delete releases waiters without a toast.
- D-526: A dense rotating closed board (800 × 400 links) migrates in < 2 s, once at start.
- D-525: The details box keeps focus; `tab` reaches the links list; the keys sit in the title row.
- D-527: The gantt link mode offers the open tasks the gantt draws; a task the view hides (a hidden archived project) is linked from the picker (code review 004 F3).
- D-528 (operator: "Corregirlo antes del push"): link mode pins the waiter's group open in the fold allocation and pages it to the waiter; where the rows left cannot hold both groups' tasks they share them; A-8's note stays only as the fallback when even that is too few (A-9). The fold rule outside link mode is unchanged.
- D-529 (operator: "Corregirlo antes del push"): in lanes a card's title keeps 6 cells (5 characters and `…`, the readability floor: a title counts once its first word shows; the kg board's median first word is 5) — `▸` then `◂` shed first, then the other meta from the left (A-10). Scoped to the lanes' call, so `card_cell`'s shipped law elsewhere (an indicator kept the moment its cells fit) and its two width tests stand; AT-501's lanes arm follows the new law.
- D-530 (operator: "Corregirlo antes del push"): `save_atomic` refuses a read-only board before writing anything (the error names the board), and its temp file goes on every failure path, a copied read-only bit cleared first; the migration still fails closed (A-11).
- D-532: D-530's read-only refusal is cross-platform on purpose: on Linux/macOS a read-only board in a writable folder used to be replaced silently (a rename needs only the folder); now it is refused and the app fails closed, matching the file's read-only intent (code review 006 M3, security N4). Root is not stopped by the check. Operator, 2026-10-04: "Sí, en todas las plataformas" — ruled.
- D-533: consequence of D-529, stated for the operator: at 118 columns every lanes cell is 19 cells wide, so lanes paint no `◂`/`▸` at all; the marks appear from about 160 columns (TC-504 pins every title readable at 118×30, 80×24 and 118×40 and the exact counts at 160×40; the 0 marks at 118 are read off the `close2-kanban-lanes-*` captures, qa G-008). Waiting stays visible in the grouped kanban, the gantt gutter and the details section. Operator, 2026-10-04: "Dejar ◂ solo, quitar la edad antes" — superseded by A-12: in lanes the age sheds first, then `▸`, then other meta; `◂` stays while the title keeps its floor.
- D-534: when the waiter and the candidate share one over-tall group, link mode chooses the page that holds both whenever one can (code review 006 M1); the fold note remains for a page that cannot.

### 6.3 Open risks
- An older app version on a migrated board writes legacy shapes again (A-14, accepted).
- `critical_chain` is recursive and exponential on dense boards (S-6, BACKLOG).
- A legacy blocked task whose flag was set in the editor after its last link was released reads as waiting on that link (A2-1): its log note says to press `b`.
- Security questions (scan `devflow-scan-spec.py`, iteration 2: `security_required: true`, flags `token`, `session`, `hash`, `migration`, `form`, `escape` — `evidence/p1-security-scan-iter2.txt`). `token` = a card's text token; `session` = the app session's undo stack; `hash` = evidence digests and byte-equality checks; `form` = the editor's archived box; `escape` = the esc key and the S1 rule; none names a credential or auth surface. `migration` = a data migration of the user's board — answered by HLR-505's safeguard (backup by exclusive create before any change, no overwrite, names outside team pull's pattern, a log, a mark read totally, an atomic save, `u` revert, fail closed) and synthetic test boards only. New surfaces paint user text as Text pieces / `markup=False` (S1); every derivation bounded (D-522); teammates' tasks never counted; `security-reviewer` at P2, at the migration increment and at close.

### 6.4 Phase-1 reconciliation log
- Iteration 2 (2026-10-04): P2 iteration 1 folded (`02-review.md`; ledger LED .6–.10).

### 6.5 Requirement amendments (Before / After · Deleted / New)
**A-1 (P3, increment 001)** — LLR-505.2/505.3. *After:* "The board file was not changed"; a failed run removes its own files; a repeated id untouched (LED .12). **A-2** — LLR-505.2, LLR-501.1. *After:* a random exclusive temp name; a malformed mark dict keeps its keys; D-526 (LED .13). **A-3** — LLR-501.2, HLR-501. *Before:* tag shed before the marks. *After:* marks before the tag (the high band's tag, A2's R-1b); measured AT counts (LED .14). **A-4** — LLR-504.1: Setup `x` never touches a task (F2, S-7 closed; LED .15). **A-5** — LLR-503.1, IFC: keys on the section heading, the accepted title row kept; Part B blocks added (LED .16). **A-6** — LLR-503.1, LLR-502.2: each row the predecessor's own state (F1); new texts "‹title› is not drawn in this view", "a one-phase board has no open phase to create it in" (LED .17). **A-7** — LLR-502.3: three status rows, keys on their own row, legend after them as "this → ‹path› → this"; N and the cycle are the tasks the gantt draws (D-527); titles and filter clip by cells (LED .18). **A-8** — LLR-502.3: a folded waiter row is said on the hint row (ux F4; LED .19). **A-9** — LLR-502.3: link mode pins the waiter's group; A-8 is the fallback (D-528; LED .20). **A-10** — LLR-501.2: the lanes' title floor (D-529; LED .21). **A-11** — LLR-505.2: a read-only board leaves nothing beside it (D-530; LED .22). **A-12** — LLR-501.2: the lanes' shed order under the floor — age, `▸`, other meta, `◂` last (operator D-533; LED .23).
