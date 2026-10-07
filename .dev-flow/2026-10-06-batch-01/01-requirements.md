# Requirements Document — taskboard — Batch 2026-10-06-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> This batch's language: **en** (see `.dev-flow/state.json`).

## 1. Introduction

### 1.1 Purpose

This document is the live contract of batch 2026-10-06-batch-01 — **Batch B2b of the kg_mejoras
plan**: moving a task's dates moves what waits on it (US-604, carried out of
2026-10-04-batch-02 by D-601, the pre-authorized B2a/B2b split). It exists for its gates:
P2 reviews it, P3 implements it, P4 validates against it.

### 1.2 Scope

**In:** the cascade engine in the model (`plan_move`, ONE overlap measure — the shipped one;
snapshot/restore); the two shipped date-moving surfaces routed through it (`+`/`-` and the
editor's date save); `m` re-applies the last move under the next mode; the per-project
`date_links` setting in the project editor; one cascade = one undo entry; an atomic save when a
cascade writes or restores more than one task.

**Out:** the gantt ⇧←→ edit-preview mode the C-1 frames imagine (no gantt move/edit mode exists
— P-17 of batch 2026-10-04-batch-02; D-626); the chain map and its per-chain switch (kg_mejoras
batch C); strict `push` as a user-facing mode (the round-6 verdict rejected it; the engine keeps
the name); pulling dependents EARLIER under `push_delta` (slack absorbs the move; only
`together` pulls back); syncing `date_links` to teammates (D-630).

### 1.3 Definitions

- **Cascade** — the dependent moves that follow one task's date move, computed as a `Plan`
  before anything is written.
- **Overlap (the ONE measure)** — the shipped one, `link_overlap` (`models.py:1812-1824`), which
  the engine calls on the planned dates: of a waiter `w` on a predecessor `p`, `max(0, p.due −
  w.start + 1)` days when `w` has a readable start (both days count), else `max(0, p.due −
  w.due)`. A milestone's start IS its due (the shipped invariant, `set_milestone`
  `models.py:687`), so a milestone waiter whose due lands on its predecessor's due overlaps by
  1 — the same day the painted `↳` counts. The two candidate measures agree in the overlap
  regime, and on every AT arm's MOVED SET and ADDED delta (the conflict TOTALS differ by the
  documented pre-existing 1d; `p1-thresholds.txt`, re-run under both measures in
  `p2_arch_probe2.py`); where a move crosses a milestone waiter's slack boundary, the shipped
  measure moves the milestone one day sooner — by design, clearing the overlap the screen would
  paint (D-633; TC-628 pins it).
- **flag / push_delta / together** — the three modes, stored strings: `flag` moves nothing else
  (the shipped `↳` early-start mark is the flag — D-632); `push_delta` pushes a dependent later
  by only the overlap the move ADDED (the default); `together` shifts every open transitive
  dependent by the moved task's due delta, both directions (all gaps kept). On screen they read
  **stay / push / together** (D-631).
- **downstream** — the open tasks that transitively wait on the moved task, through open tasks
  only. Done and archived tasks never move and stop the cascade.
- **milestone** — the shipped `Task.milestone` (batch 2026-10-04-batch-02): one date, its due
  authoritative, its start follows (D-605); a milestone always moves whole.
- **The toast ladder** — the C-3 frame's fitting rule (`variants_cascade.py` `render_c3`):
  rungs tried in order until the toast fits the width; a moved task's name is
  `_short_title(·, N)` (words added while the total fits N cells), N narrowing **12 → 8**
  across the rungs before the count forms (the 8-rung is load-bearing: AT-608's @118 toast
  lands on it); the project clause carries the project's FULL name when the rung affords it,
  else its FIRST WORD; the key suffix narrows `m change for this move` → `m change` → `m`;
  the lead's title clips at the narrowest rungs (the `@80` rows show it).

### 1.4 References

- Round-6 verdict (operator, 2026-10-01): push_delta default, per-project setting (C-2), `m`
  per move — `prototypes/kg_mejoras/NOTES.md` §Round 6 (worktree `kg-mejoras`).
- The proved engine: `prototypes/kg_mejoras/cascade.py`; its executed scenarios:
  `evidence/p1-cascade-logic.txt` ("all asserts passed"; re-run green under the shipped measure
  in `evidence/p2_arch_probe2.py`).
- Frames: `out/C-1a..d-*`, `out/C-2*`, `out/C-3-*` (worktree `kg-mejoras`).
- Batch 2026-10-04-batch-02's contract (the milestone flag this batch builds on).

### 1.6 NEW literals and constants (C-36)

Every value an acceptance names reconciles here — each greps to a constant DEFINED on disk or
is flagged `NEW — created in Phase 3`:

| Literal | Where it lives | Status |
|---|---|---|
| `"flag"`, `"push_delta"`, `"together"` | `models.py` (the mode strings, `plan_move`'s vocabulary) | NEW — created in Phase 3 (defined today only in the throwaway `cascade.py`) |
| `"push"` | `models.py` (`plan_move` accepts it under its name; no surface offers it) | NEW — created in Phase 3 |
| `"date_links"` | the `Project.extra` key holding the setting | NEW — created in Phase 3 |
| `stay` / `push` / `together` | the setting's on-screen labels (the prototype's SHORT map, `variants_cascade.py`) | NEW — created in Phase 3 |
| `flagged` / `pushed` / `moved` | the toast's verb per mode (frame C-3) | NEW — created in Phase 3 |
| `‹title› due ‹Mon D› (‹+N›d)` | the toast's lead (frame C-3: `▌Audit… due Oct 3 (+1d)`) | NEW — created in Phase 3 (`_md` and `clip` are defined) |
| `· ‹project› +‹N›d past ◆` | the toast's project clause (frame C-3); ‹project› is the MOVED task's project, full name or first word per the toast ladder (§1.3) | NEW — created in Phase 3 |
| `· u undo · m change for this move` | the toast's key suffix, narrowing `… · m change` → `· m` (the toast ladder) | NEW — created in Phase 3 (`· u undo` is the shipped form) |
| `flagged ‹names› +‹N›d` | the flag clause: the worsened overlaps' waiters by name (the ladder's name rule) with the ADDED days; a count when names do not fit (`flagged 2 +2d each`); mixed added days spelled per waiter (`flagged 2 overlaps (‹A› +1d, ‹B› +3d)`) | NEW — created in Phase 3 |
| `m re-applies the last date move — nothing to re-apply` | `m`'s refusal toast | NEW — created in Phase 3 |
| `m` | `keymap.py` — re-apply the last move under the next mode: `Key("m", "m", "cascade_mode", "Chain", group="date")` | NEW key; the letter is free and reserved (`keymap.py:87`) |
| `◆`, `↳`, `▲` | shipped glyphs (gantt due, waits-on, late) | defined — `views.py` |
| `+1d` / `in Nd` / `Nd late` | shipped date/delta formats (`_md`, chips) | defined — `views.py` |

## 2. Overall description

### 2.1 Product perspective

taskboard is a frameless Textual desktop widget over one JSON board. Links (`depends_on`, "waits
on") shipped in batch 2026-10-04-batch-01; milestones in 2026-10-04-batch-02. Today moving a
task's dates moves nothing else, and a chain drifts apart silently. This batch makes the move
carry its chain, by a rule the project sets and the user can override per move.

### 2.2 Product functions

- A date move (quick bump or editor) plans and applies the cascade for the resolved mode.
- The move is said (a toast: WHO moved — names when they fit, a count when they do not — by how
  much, and what it pushed past its project's due).
- The move undoes as one step (`u`).
- `m` re-applies the last move under the next mode.
- Each project carries the rule (`stay` / `push` / `together`; default `push` = `push_delta`).

### 2.3 User characteristics

The operator, keyboard-first, on boards with real chains (the kg board's five projects).

### 2.4 Constraints

- One JSON file; the lenient model never raises on load; `u` undoes any date move in one step.
- The operator's real board is never opened by tests — synthetic boards only (the commission).
- Windows terminal; width-1 glyph discipline; `rich.markup.escape` on untrusted text.
- Local JSON only; there is no slow state (no network, no latency class to design for).

### 2.5 Assumptions

- The two date-moving surfaces are the only ones (P-1/P-1b, executed).
- `Project.extra` round-trips verbatim through load/save (P-3, executed) — the setting needs no
  model change.
- The undo stack already replays multi-task entries (P-5, executed) — the cascade's entry is a
  third shape of a shipped pattern.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-604 | As a taskboard user, I want moving a task's dates to move what waits on it — push by default (`push_delta`: a dependent moves only by the overlap the move ADDED), a per-project setting (`date_links`), `m` per move — so that a chain stays consistent. | round 6 verdict (operator, 2026-10-01: "Empujar" default, per-project setting, `m` per-move override); BACKLOG "Batch B2b" | READY |

#### Refinement log (one block per story)

**US-604 — moving linked dates**
- **INVEST:** I ✓ (one story, one move rule) · N ✓ (modes named, default fixed) · V ✓ (a chain stays consistent) · E ✓ (the prototype's logic runs and asserts; scenarios already enumerated) · S ✗ at round 5 → split pre-authorized (D-601); this batch IS the split · T ✓ (below)
- **Functionality (V, N):** user = the operator moving dates on a linked board · outcome = moving a task's dates moves what waits on it, by the project's rule, overridable per move · why = a chain stays consistent without re-dating every dependent by hand · out of scope = the chain map (batch C), a gantt drag/edit mode (none exists — P-17), strict `push` as a user-facing mode (rejected by the verdict; stays an engine-internal name), pulling dependents EARLIER in push_delta (slack absorbs; only `together` pulls back)
- **Feasibility (E, S):** implementation path = port the prototype's proved engine (`prototypes/kg_mejoras/cascade.py` — `plan_move`/`resolve_mode`/`snapshot`/`restore`, all asserts pass in `cascade_logic.py`) into `models.py` against the shipped `Task.milestone` (A-14), wrap the two shipped date-moving surfaces (`action_due_bump` `+`/`-` and the editor's date save), add `m` and the per-project setting · dependencies/unknowns = the editor save's exact seat; the setting's home (C-2 frame) · fits one batch = yes (this is the split half)
- **Evaluability (T) — behavioral, black-box:** "When the user presses `+` on a task whose dependent starts the day after its due, the dependent's dates move by the added overlap and a toast names what moved" · "When the project's `date_links` is `flag`, the same bump moves nothing and the toast names the worsened overlap" · "When the user presses `m` after the bump, the move is re-applied under the next mode" (become AT-NNN in Phase 1)
- **Open questions:** none blocking — the setting's exact surface (chain map C-2 vs the project editor) is decided at P1 against the shipped seats (D-627: the project editor)
- **Classification:** `READY` — the verdict exists, the engine is proved, the surfaces are known

Evaluability: each HLR's acceptance block (§3).
RC-1 (b): none already shipped (`git grep push_delta/date_links/plan_move origin/main` hits only closed dev-flow records; output pasted in `p0-probes.txt`).

### 2.7 Premise evaluation (C-43)

Every premise EXECUTED; transcripts in `evidence/p0-probes.txt`, `evidence/p1-premises.txt`,
`evidence/p1-cascade-logic.txt`, `evidence/p1-thresholds.txt`.

| # | Premise | Verdict | Executed evidence |
|---|---|---|---|
| P-1 | The only task-date writers outside `models.py` are the `+`/`-` bump (`action_due_bump`, `app.py:1066-1078`) and the editor's save (`_on_task_edited`'s `setattr`, `app.py:1703`) — plus undo restores and `set_milestone` | TRUE | `p1-premises.txt` §P-1 (0 direct assignment sites — the empty output pasted), §P-1b (`setattr(task` → `app.py:1155` undo, `app.py:1703` editor) |
| P-2 | The editor's date save records no undo and sends no success toast today | TRUE | `p1-premises.txt` §P-2: `_undo_stack.append` sites at 300/333/821/881/900/955/1010/1022/1075/1535/1758/1784 — none in `_on_task_edited` (1690-1714) |
| P-3 | `Project.extra` survives a load→save round-trip verbatim | TRUE | `p1-premises.txt` §P-3: executed round-trip, `{'date_links': 'together'}` intact |
| P-4 | `m` is unbound; `M` took the milestone key with `m` reserved for this batch | TRUE | `p1-premises.txt` §P-4: only `Key("M", …)` matches; `keymap.py:87` reserves `m` |
| P-5 | The undo stack already replays multi-task entries as one step (the offer's `milestones`, the migration's `migration`) | TRUE | `p1-premises.txt` §P-5: pushed at `app.py:300/333`, replayed at `app.py:1120/1132` |
| P-6 | Team sync does NOT merge a project's `extra` for an EXISTING project (only name/color/status/dates/archived); a project first seen in a push is built whole by `Project.from_dict`, which sweeps unknown keys into `extra` | TRUE, with the second limb named | `p1-premises.txt` §P-6: the merge list at `team_sync.py:280-290`; the new-project path at `team_sync.py:291-296` + `models.py:803` (S-4) |
| P-7 | The prototype engine's scenarios all pass — the rule is proved before any port — and pass again under the shipped overlap measure | TRUE | `p1-cascade-logic.txt`: "all asserts passed"; `p2_arch_probe2.py` (the whole suite re-run with `link_overlap` semantics: green) |
| P-8 | A milestone's due is authoritative in the shipped code: `bump_due` moves it whole (D-605) | TRUE | `p1-premises.txt` §P-8: `models.py:667-669` |
| P-9 | Every AT threshold is EXECUTED on the exact AT board, not predicted — moved-sets and toast strings; the two NEW strings (the flag clause and `m`'s refusal, §1.6) have their components executed and their derivation stated | TRUE, scoped | `p1-thresholds.txt` (moved-sets, both overlap measures listed); `p2_arch_probe.py` + `p2-arch-probe.txt` (the toast ladder executed at 118 and 80); the flag clause's names and added days reconcile against `tests/kg_board.py` and `p1-thresholds.txt` |

### 2.8 Fork preconditions (C-52)

`none — the batch runs one lane: the increments land in order, each on the previous one's tree.`

## 3. High-level requirements (HLR)

### HLR-604 — Moving a task's dates moves what waits on it, by the project's rule
- **Traceability:** US-604
- **Ledger:** LED-2026-10-06-batch-01.1, LED-2026-10-06-batch-01.2, LED-2026-10-06-batch-01.3
- **Statement:** When the user moves a task's dates — by the `+`/`-` bump or by saving dates in the editor — the system shall compute the cascade for the resolved mode (the moved task's project's `date_links`, or the per-move override) before writing anything, shall apply it so that: under `push_delta` an open dependent moves later by only the overlap the move ADDED (slack absorbs the move, a pre-existing overlap is tolerated, a zero or earlier move pulls nothing); under `together` every open transitive dependent shifts by the due delta both directions (all gaps kept); under `flag` nothing else moves and the toast names each worsened overlap; done and archived tasks never move and stop the cascade; a milestone moves whole; and the moved task's project's rule decides for the whole cascade, cross-project links included — shall say what happened in a toast that names what moved, and shall record the whole move as ONE undo entry, restored by a single `u`.
- **Rationale (informative):** the round-6 verdict; strict `push` was rejected on evidence (`p1-cascade-logic.txt` §2: a +3d move slipped the project +9d; a zero-day move moved three tasks).
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_cascade.py tests/test_cascade_app.py -q`
- **Numeric pass threshold:** 0 failures; the ATs' exact boards, moved-sets and toasts as §5 states them (`p1-thresholds.txt`, `p2_arch_probe.py`).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the user bumps a task and watches its chain move with it — by the added overlap, by the whole gap, or not at all, as the project's rule says — reads WHO moved in the toast, changes his mind with `m`, takes it all back with one `u`.
  - **Shipped surface:** the kanban/gantt quick keys and the task editor; the toast; the project editor's setting; the undo stack.
  - **Acceptance test(s):** AT-607, AT-608, AT-609, AT-610, AT-611
  - **Boundary catalog (QC-3):** ☑ empty (an undated task bumps from today — the shipped `bump_due` rule, and the cascade computes on the resulting dates) ☑ boundary (a zero-delta move; a waiter starting the day after its predecessor's due — overlap 0) ☑ invalid (a `date_links` value the app never wrote) ☑ error (a `depends_on` id that names no task — the shipped lenient read)
  - **Negative control:** the same bump under `flag` moves nothing — an AT arm that goes RED if the cascade ignores the mode.

---

## 4. Low-level requirements (LLR)

### LLR-604.1 — The cascade engine in the model
- **Traceability:** HLR-604
- **Ledger:** LED-2026-10-06-batch-01.1, LED-2026-10-06-batch-01.2, LED-2026-10-06-batch-01.3, LED-2026-10-06-batch-01.5
- **Statement:** `models.py` shall provide `plan_move(board, task_id, start_delta, due_delta, mode, today) -> Plan` — pure, writing nothing — computing `moved` (the new dates per touched task, the moved task included), `shift` (days per task), `new_conflicts` (overlaps added or worsened, as `(waiter, predecessor, ADDED days)` — `ov_new − ov_old`, deliberately not the prototype's new-total) and `project_over` (days past the project's own due, before and after); `apply_plan` / `snapshot` / `restore` (one undo step, byte-identical restore); and `resolve_mode(board, task_id, override)` — the override, else the moved task's project's `date_links`, else `push_delta`. Modes: `flag`, `push_delta` (DEFAULT), `together`; `push` (strict) is accepted under its name and offered nowhere. The overlap measure is the shipped `link_overlap` applied to the planned dates — ONE measure, the same one the screen paints (D-633); the downstream is computed through open tasks only; a milestone ignores `start_delta` and moves whole; an undated moved task bases its dates on `today` (the bump's own rule, `bump_due` `models.py:666`) before the cascade is computed.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_cascade.py -q`
- **Numeric pass threshold:** TC-618..TC-630, 0 failures — the prototype's scenarios re-run against the shipped `Task.milestone` (A-14): `tm2` +3d pushes `tm3` +3d and `tm4` +3d (never the strict +9d); a zero move and an earlier move move nobody under `push_delta`; `together` pulls back keeping every gap; a done/archived dependent stops the chain; a milestone moves whole; snapshot/apply/restore round-trips byte-identically; an undated task bumped +1 reads as today+1 and cascades from there; at the slack boundary a `push_delta` move that lands a milestone waiter on its predecessor's due moves the milestone +1d (the shipped measure; TC-628 — RED against the prototype's carve-out); a move that creates a FIRST overlap pair reports the added days, never a crash (TC-629, code review C-1); a planned task vanished before the restore is skipped, never a crash (TC-630, code review C-2).
- **Negative control:** strict `push` on `tm2` +3d slipping Mobile +9d — the rejected mode's transcript (`p1-cascade-logic.txt` §2) is the RED the default was chosen against; TC-618 asserts the delta, not the strict, outcome.
- **Boundary catalog:** ☑ empty (undated waiter: the no-start arm of the measure; undated moved task: the today base) ☑ boundary (overlap 0: the waiter starts the day after the predecessor's due; the slack-boundary milestone) ☑ invalid (junk `date_links` reads as the default) ☑ error (a dangling `depends_on` id contributes nothing)

### LLR-604.2 — The `+`/`-` bump routes through the cascade
- **Traceability:** HLR-604
- **Ledger:** LED-2026-10-06-batch-01.1, LED-2026-10-06-batch-01.2, LED-2026-10-06-batch-01.3, LED-2026-10-06-batch-01.4, LED-2026-10-06-batch-01.6, LED-2026-10-06-batch-01.8
- **Statement:** `action_due_bump` shall plan the cascade for the resolved mode before writing, apply it, push ONE undo entry carrying every moved task's prior dates, and save once — atomically (`save_atomic`) whenever the write touches more than one task, on the apply and on its undo's restore alike (D-634). It shall toast the move on the toast ladder (§1.3): lead `‹title› due ‹Mon D› (‹+N›d)`; then the cascade clause naming WHO moved when the rung affords names (`pushed Add push, Offline sync +1d each`; mixed shifts `pushed 2 dependents (Offline sync +3d, Beta release +6d)`), else the count (`pushed 2 +1d each`); under `flag`, when the move adds or worsens overlaps, `flagged ‹names› +‹N›d` with the ADDED days — names when they fit, the count `flagged 2 +2d each` when they do not, mixed added days spelled per waiter (`flagged 2 overlaps (‹A› +1d, ‹B› +3d)`) — the prototype transcript's `flagged 0 dependents ()` is a degenerate artifact (its ladder has no flag clause), NOT this grammar; then `· ‹project› +‹N›d past ◆` when the moved task's project slips further past its own due (the moved task's project only — a cross-project slip of another project's due is not reported); then `· u undo · m change for this move`, narrowing per the ladder. Under `flag` nothing else moves and the shipped `↳` conflict mark is the persistent flag surface (D-632). A task with no dependent moves alone, and the toast carries no cascade clause.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_cascade_app.py -q`
- **Numeric pass threshold:** AT-607 arms, every number and string executed (`p1-thresholds.txt`, `p2_arch_probe.py`): on the shifted milestones board (§5), `+` on `tm2` moves `tm3` +1d AND `tm4` +1d (tm4's pre-existing 3d overlap would grow to 4d on tm3's new date, so tm4 is pushed +1d, restoring it) and no other task (`tm5` stays: 7d of slack absorbs the move); the toast at 118 columns holds `pushed Add push, Offline sync +1d each`, at 80 columns `pushed 2 +1d each`; one `u` restores all three tasks' dates byte-identically.
- **Negative control:** the `flag` arm of AT-610 — same bump, nothing moves.
- **Boundary catalog:** ☑ empty (undated task: the bump bases on today, the cascade computes on the new date) ☑ boundary (a +0-added overlap edge) ☑ invalid ☑ error — both inherited from LLR-604.1's engine arms.

### LLR-604.3 — The editor's date save routes through the cascade
- **Traceability:** HLR-604
- **Ledger:** LED-2026-10-06-batch-01.1, LED-2026-10-06-batch-01.2, LED-2026-10-06-batch-01.8
- **Statement:** When `_on_task_edited` changes a task's start or due, the system shall plan and apply the cascade for the resolved mode with the same rules as the bump (the delta per field: new minus old, per `parse_iso`; an unreadable old or new date is no delta on that field), push ONE undo entry, save once (atomically when the plan touches more than one task), and toast on the toast ladder only when the cascade moved other tasks (the editor's successful save stays silent otherwise — today's behaviour, D-629). A save that changes no date plans nothing, pushes nothing and toasts nothing.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_cascade_app.py -q -k editor`
- **Numeric pass threshold:** AT-609, executed in `p1-thresholds.txt`: the editor moves `tm2`'s due +3d → `tm3` +3d AND `tm4` +3d, the toast holds `pushed`, `u` restores all three; a save touching only the title writes no undo entry and no toast.
- **Negative control:** the title-only save arm — RED if the editor cascades on an unchanged date.
- **Boundary catalog:** ☑ empty (a date cleared in the editor: no delta on that field) ☑ boundary ☑ invalid ☑ error — engine arms as LLR-604.1.

### LLR-604.4 — `m` re-applies the last move under the next mode
- **Traceability:** HLR-604
- **Ledger:** LED-2026-10-06-batch-01.1, LED-2026-10-06-batch-01.2, LED-2026-10-06-batch-01.6, LED-2026-10-06-batch-01.8
- **Statement:** When the top of the undo stack is this session's last date move (bump or editor), `m` (`Key("m", "m", "cascade_mode", "Chain", group="date")`) shall undo it and re-apply the same move under the next mode in the cycle `flag → push_delta → together → flag`, replacing the undo entry and refreshing the toast with the new mode's outcome. Otherwise `m` shall refuse with the toast `m re-applies the last date move — nothing to re-apply` and write nothing. The cycle never offers `push`.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_cascade_app.py -q -k override`
- **Numeric pass threshold:** AT-608, every moved-set executed in `p1-thresholds.txt`: after `+` on `tm2` (push_delta: `tm3` and `tm4` +1d), `m` re-applies under `together` — `tm3`, `tm4` AND the milestone `tm5` +1d each, the toast holding `moved` and `Mobile +1d past ◆` (the mode discriminator: `tm5` moves only under `together`; `Mobile` is the project name's first word, the ladder's rule); `m` again re-applies under `flag` — `tm3`/`tm4`/`tm5` back to their dates, `tm2` +1d alone, the toast holding `flagged Add push +1d`; `m` on a fresh board toasts the refusal verbatim and writes nothing.
- **Negative control:** the refusal arm — RED if `m` with no move on top mutates any date.
- **Boundary catalog:** ☑ empty (nothing to re-apply) ☑ boundary (the cycle wraps `together → flag`) ☑ invalid — none: the cycle's values are the app's own ☑ error (the moved task deleted between the move and `m`: the refusal, never a crash).

### LLR-604.5 — The per-project setting in the project editor
- **Traceability:** HLR-604
- **Ledger:** LED-2026-10-06-batch-01.1, LED-2026-10-06-batch-01.2, LED-2026-10-06-batch-01.3, LED-2026-10-06-batch-01.7, LED-2026-10-06-batch-01.8
- **Statement:** The project editor (`P` → `e`, `ProjectModal`) shall carry a `Linked dates` select over `stay` / `push` / `together`, stored as `extra["date_links"]` = `flag` / `push_delta` / `together` (D-627, D-631), defaulting to `push` when the key is absent, and reading as the default — never raising — when the stored value is not one of the three (the lenient model; the value arrives from a file). The setting rides the project editor's existing save; it is local-only for an existing project (D-630).
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_cascade_app.py -q -k setting`
- **Numeric pass threshold:** AT-610, executed in `p1-thresholds.txt`: set Data Warehouse to `together`, move `td4` +2d IN THE EDITOR (start and due both — the `+` key moves the due only) → the milestone `td0` and `td5` move +2d each, the toast holding `moved` and `Data +2d past ◆` (the ladder's first-word rule); set `flag`, the same edit moves nothing else and the toast holds `flagged Revenue +2d` (the added days: 1d pre-existing → 3d); a board hand-edited to `"date_links": 5` loads, behaves as `push_delta`, and saves the bad value back untouched (no silent repair).
- **Negative control:** the junk-value arm — RED if an unknown `date_links` raises or moves under a different rule than the default.
- **Boundary catalog:** ☑ empty (no key) ☑ boundary (the three exact values) ☑ invalid (junk, non-text) ☑ error — none beyond load leniency.

---

## 4b. Information Flow Contract (IFC)

Part A always. Part B: yes — `#f-date-links` is a NEW addressable widget; its block is added by
the increment that creates it, as a ledger amendment (B1 D-514, `V14`).

```
FLOW: linked dates, from the board file and the user's keys to the screen and back
  SOURCE : the board file on disk (depends_on, start_date, due_date, milestone, project extra); the user's keys
  NODES  :
    - fn    : plan_move / apply_plan / snapshot / restore / resolve_mode (the overlap measure is link_overlap's)
      owner : LLR-604.1
    - fn    : KEYMAP +,- / action_due_bump / the bump toast
      owner : LLR-604.2
    - fn    : TaskModal date fields / _on_task_edited
      owner : LLR-604.3
    - fn    : KEYMAP m / action_cascade_mode (the re-apply) / its toasts
      owner : LLR-604.4
    - fn    : ProjectModal Linked dates select / ProjectPicker._on_edited
      owner : LLR-604.5
  SINK   : the painted screen, the saved board file, the undo stack, the pushed board.<user>.json (the moved dates ride the shipped task sync like any edit)
```

```
COMPONENT: project-date-links
  PARENT : SYSTEM
  SURFACE: the project editor (P → e)
  INPUTS : board: Board ; project: Project
  OUTPUTS:
    - id          : date-links-select
      value       : the project's linked-dates rule, as the payload key "date_links"
                    (flag / push_delta / together; absent or junk reads as the default)
      address     : "#f-date-links"
      consumers   : taskboard/modals.py::ProjectModal ; taskboard/modals.py::ProjectPicker ; taskboard/app.py::TaskboardApp ; tests/test_cascade_app.py
      owner       : LLR-604.5
```

> The editor's date fields are NOT a new component: `#f-start` / `#f-due` are shipped
> addresses this increment reroutes through the cascade, not new ones.

## 5. Validation strategy

Layer A (`TC-618` through `TC-630`) and Layer B (`AT-607` through `AT-611`, one node each — C-18)
are pytest nodes carrying their id in docstring and name, in `tests/test_cascade.py` (the engine)
and `tests/test_cascade_app.py` (the app). The ATs drive `TaskboardApp` with real keys (C-16) over
a board file in `tmp_path`.

**The boards.** `tests/kg_board.py` `shifted` + `milestones` (§5 of batch 2026-10-04-batch-02):
the chains are `tm2→tm3→tm4→tm5` (tm5 a milestone), `tw2→tw4`, `tw2+tw4→tw5` (a milestone),
`td4→td0` (a milestone) `→td5`, `ta4→ta6`. The pre-existing overlaps under the shipped measure
(`p1-thresholds.txt`, both listings): `tm3<tm2` 2d, `tm4<tm3` 3d, `ta6<ta4` 11d, `td0<td4` 1d
(the milestone's due lands on its predecessor's due; §1.3) — so AT-610's flag arm ends at 3d =
1 pre-existing + 2 added, and the toast says the ADDED 2d (AT-608's evidence line shows the
prototype's TOTAL 3d; its added days are 1d). A cross-project arm adds `td2` waits
on `ta4` in-test (the prototype's scenario 4a).

**Captures:** the bump toast at 118×30 and 80×24 (the C-3 frame's home), the project editor's
new row, the gantt's `↳` gutter under `flag` — `evidence/captures/`; base not applicable (no
surface exists at base).

| AT | Story | Drives (the HLR's threshold) |
|---|---|---|
| AT-607 | US-604 | `+` on `tm2`; the toast at 118 and 80; `u` |
| AT-608 | US-604 | `+`, then `m` twice through the cycle (the `tm5` discriminator); the refusal on a fresh board |
| AT-609 | US-604 | `e` edits `tm2`'s due; a title-only save |
| AT-610 | US-604 | `P` `e` sets the project's rule; edits under `together` and `flag`; a hand-edited junk value |
| AT-611 | US-604 | a done dependent stops the chain; a milestone moves whole (slack absorbs its waiter); an earlier move pulls nothing; the cross-project arm |

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion shown RED on the base tree or by a recorded mutation.
- each existing node the batch changes is listed in its increment's reverse census.
- full suite: 0 failures other than a declared environment flake (G-011 is the known one).

## 6. Appendices

### 6.2 Relevant design decisions

| Id | Decision | Why |
|---|---|---|
| D-626 | The move surfaces are `+`/`-` and the editor; the gantt ⇧←→ edit-preview mode (C-1 frames) is OUT → BACKLOG | no gantt move/edit mode exists (P-17 of batch 2026-10-04-batch-02); the verdict ruled the cascade rule, the setting and `m` — not a new editing mode |
| D-627 | The setting lives in the project editor (`ProjectModal`), not the chain map | the chain map is batch C and does not exist; `ProjectModal` is the shipped per-project seat. The operator approved the C-2 frame's per-chain radio; the re-siting is called out by name for the P4 visual verdict |
| D-628 | One cascade = one undo entry, the multi-task shape | the offer's `milestones` entry is the shipped pattern (P-5); the user thinks in moves, not in cells |
| D-629 | The editor gains the cascade, an undo entry and a toast ONLY when a date changed and others moved | the editor's successful save is silent today (P-2); the new information is the cascade, not the save |
| D-630 | `date_links` is local-only for an existing project | team sync merges only name/color/status/dates/archived for existing projects (`team_sync.py:280`, P-6); a project FIRST SEEN in a teammate's push is built whole by `Project.from_dict`, which sweeps unknown keys into `extra` — a teammate's setting can arrive that way, is read leniently, and is never written back by sync (S-4). Syncing the setting properly is a separate question → BACKLOG |
| D-631 | Stored values are the engine's strings (`flag`/`push_delta`/`together`); on-screen labels are `stay`/`push`/`together` | the prototype's SHORT map (`variants_cascade.py`); the engine vocabulary is the contract's, the labels are the user's |
| D-632 | `flag` adds no new marker: the shipped `↳` early-start conflict (over tone) IS the persistent flag; the toast's `flagged` clause is the per-move one | one overlap measure, one conflict surface; the mark already paints in the gantt gutter |
| D-633 | The ONE overlap measure is the shipped `link_overlap`, applied to planned dates | P2 (A-2/S-2/UX-2): the prototype's milestone carve-out disagrees with the painted screen by 1d when a milestone's due lands on its predecessor's due. The measures agree in the overlap regime and on every AT arm (re-run under both: `p2_arch_probe2.py`); at a milestone waiter's slack boundary the shipped measure moves the milestone one day sooner — the same day the painted `↳` counts (TC-628 pins it). The constant does NOT universally cancel (P2 iteration 2, A-9/S-8); the choice stands on the screen, not on the algebra |
| D-634 | A cascade that touches more than one task saves through `save_atomic()`, on the apply AND on its undo's restore; a single-task move keeps `save()` | P2 S-3: `Board.save()` is a plain `write_text` (`models.py:983-985`); the cascade is the first feature that rewrites a chain in one save, and the restore writes the same chain back (ux S-6). The undo is session-only (the shipped LIFO) — said in §6.3 |

### 6.3 Open risks

- **security_required: true** — the scan's flags (`session`, `migration`, `escape`), answered:
  - the cascade writes the board through `save_atomic()` when it touches more than one task
    (D-634); the undo is the shipped session LIFO — a crash after the save is NOT undoable past
    the session, the same boundary every shipped feature has.
  - file-derived text reaches the screen in the toasts (task titles, project names): the control
    is the shipped S1 convention — `clip()` and `markup=False` (e.g. `app.py:1014`), never a raw
    interpolation into markup.
  - the engine parses file-derived dates through `parse_iso` (lenient, never raises) and the
    setting through the lenient read (LLR-604.5's junk arm).
- `m`'s re-apply lives on the undo stack's top entry — an `m` after an intervening action
  refuses by design (LLR-604.4); the risk is a user expecting `m` to arm the NEXT move (the
  C-1 frame's in-edit cycling). The refusal literal is pinned; the key bar advertises `m Chain`.
  Carried to the operator's visual verdict.
