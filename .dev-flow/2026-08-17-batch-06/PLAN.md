# PLAN — 2026-08-17-batch-06 (living compendium)

**Batch objective.** Implement the operator-approved **C** gantt direction from the
`prototypes/next_ideas/` concept page: give the gantt task rows semantic meaning
through priority colour, milestone glyphs, and dependency indicators, plus a
project-focus filter to cut density on busy boards.

**Mode:** `core` (4 stories, interaction change, model contract touched). Language: `en`.
**Where we are:** Phase 0 — intake & refinement, operator approved variant **C** 2026-08-17.

## Verified at intake (executed, not asserted)

- **RC-1 base currency:** `git fetch origin` 2026-08-17 → `HEAD == origin/main ==
  merge-base == 8b73920`. Branch current. Untracked deliberation directory
  `prototypes/next_ideas/` present.
- **Flow currency (C-45 PULL):** `~/.claude/skills/dev-flow` == backup repo
  `~/kimi/agent-skills/dev-flow` at **rev25** (verified at batch-05; no reason to
  expect drift within the same session).
- **Prototypes approved:** operator verdict 2026-08-17: implement variant **C**
  from `prototypes/next_ideas/out/next-ideas.html`.

## Stories (4) — INVEST

| id | story | status | observable outcome (the AT surface) |
|---|---|---|---|
| R-01 | **Priority colour.** As a gantt user, I want task bars to wear a priority hue so I can see urgency at a glance. | READY | High-priority tasks render rose, normal sky, low muted; project rows keep project colour. |
| R-02 | **Milestones.** As a gantt user, I want zero-duration tasks to appear as a diamond so I can distinguish deadlines from spans. | READY | A task whose `start_date == due_date` renders `◆` at that cell. |
| R-03 | **Dependencies.** As a gantt user, I want to see which tasks have downstream blockers so I can read the critical chain. | READY | A task with non-empty `depends_on` shows a `└─►` indicator; the field persists round-trip. |
| R-04 | **Project focus.** As a gantt user, I want to filter the gantt to one project and clear it with `esc`, like kanban focus. | READY | `F` cycles projects in gantt; header shows `(focused: X)`; `esc` clears. |

## Trigger evaluation (id · verdict · probe)

- **B1** (touched symbol asserted by other requirements' tests) — **FIRED**:
  `render_gantt`, `_task_reach`, `Task`, `Board`, `focus_cycle` appear in tests.
  → reverse census at Phase 2.
- **B2** (file location move) — did not fire: no file moves planned.
- **B3** (byte-identical goldens) — did not fire: no `goldens/` dir.
- **B4** (artifact consumed downstream) — did not fire: prototypes are read-only.
- **C** (security patterns) — did not fire: no new string reaches markup unescaped;
  `depends_on` is a list of task ids persisted as JSON.
- **D** (interaction change) — **FIRED**: `F`/`esc` now active in gantt, new modal
  field → `ux-reviewer` joins the PDR.
- **E** (≥3 stories) — **FIRED**: 4 stories → lane raised to `core`.
- **F** (flow currency) — verified current at batch-05; backlog refresh due at close.

## Increment plan (≤4 source files each, tests uncapped)

| inc | content | source files (planned) |
|---|---|---|
| 1 | R-03 data contract: add `depends_on` to `Task`, load/save/migration, default `[]` | `models.py` |
| 2 | R-01 + R-02 + R-03 render: priority hue in `_task_reach`, milestone diamond, dependency indicator | `views.py` |
| 3 | R-04 focus filter + key wiring: gantt focus cycle/exit, `F`/`esc` in keymap, pass focus through `render_view` | `app.py`, `keymap.py`, `views.py` |
| 4 | README key table + contract tests + integration ATs | `README.md`, `tests/test_gantt.py`, `tests/test_models.py`, `tests/test_keymap.py` |

## Risks / watch-items

- **Existing gantt law change.** `test_a_bar_never_wears_an_urgency_hue` asserted
  that bars only wear identity/project hues. Variant C intentionally breaks that
  law: priority is now a bar hue. The test will be updated, not weakened.
- **`depends_on` migration.** Legacy tasks have no `depends_on`; `from_dict` must
  default to `[]` without writing `null` back to disk (round-trip discipline).
- **Focus state shared with kanban.** `focused_project_id` already exists; gantt
  reuse means switching views keeps the filter. This is consistent with kanban
  but must be documented in the key legend.
- **Task meters removed.** To match the approved prototype, task due meters are
  removed in favour of the bar semantics. If the operator wants meters back,
  this is a one-row revert in `render_gantt`.

## Conventions honored

≤4 source files/increment · tests uncapped · README key table documents
every bound key (`test_keymap.py` enforces) · no commits/push without operator
decision at the merge gate · artifacts in English, conversation in Spanish ·
RED counterfactual mandatory per AT · every acceptance falsifiable (C-40) ·
`shall` reserved for HLR/LLR statements.

## Decision log

| date | decision | by |
|---|---|---|
| 2026-08-17 | Batch opened under /dev-flow, lane `core` (E/D fired) | orchestrator, pending operator gate |
| 2026-08-17 | Variant **C** approved for implementation: priority colours, milestones, dependency indicators, gantt focus | operator |
| 2026-08-17 | `depends_on` stored as a list of task ids on `Task`; no UI editor in this batch | orchestrator default, pending gate |
| 2026-08-17 | Task due meters removed to match prototype density; project rows keep due figure | orchestrator default, pending gate |

## Test ledger

| node | suite | last run | result |
|---|---|---|---|
| tests/ | pytest | 2026-08-17 | **841 passed** |
| tests/test_gantt.py | pytest | 2026-08-17 | 27 passed — priority hue, milestone, dependency, focus |
| tests/test_app.py | pytest | 2026-08-17 | passed — focus scope updated to kanban+gantt |
| tests/test_keymap.py | pytest | 2026-08-17 | passed — README/seat contract |
| tests/test_archive.py | pytest | 2026-08-17 | passed — date mock added to purge AC1 |
