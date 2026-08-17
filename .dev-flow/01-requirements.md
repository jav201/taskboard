# Requirements Document — taskboard — Batch 2026-08-17-batch-06

> **Artifact language:** English (`state.json.language = en`).
> **Base ref:** `8b73920` (= `origin/main`, HEAD, merge-base — RC-1 PASS).
> **Normative convention:** `shall` is binding and appears ONLY inside HLR/LLR **Statement** lines. `should` never appears inside one.

---

## 1. Introduction

### 1.1 Purpose

Define the change that gives the gantt view task-level semantics: priority as
bar colour, milestones as diamond glyphs, dependencies as a visible indicator,
and a project-focus filter to control density.

### 1.2 Scope

**In scope**
- `taskboard/models.py`: add `depends_on: list[str]` to `Task` with safe
  load/save/migration.
- `taskboard/views.py`: `_task_reach`, `render_gantt`, `render_view`.
- `taskboard/app.py`: extend `focus_cycle` / `focus_exit` to gantt.
- `taskboard/keymap.py`: bind `F` and `esc` focus actions for the gantt view.
- `README.md`: key-binding table update.

**Out of scope, explicitly**
- A UI editor for dependencies in `TaskModal`.
- New board actions unrelated to gantt semantics.
- Darkside, ledger, prism, keybar, or palette follow-ups.

### 1.3 Definitions

| Term | Definition |
|------|------------|
| Milestone | A task whose `start_date` equals its `due_date` (and both are present). |
| Dependency indicator | A small rendered hint that a task has one or more downstream dependents. |
| Focus filter | The existing `focused_project_id` mechanism, extended from kanban to gantt. |

---

## 2. High-level requirements

### HLR-001 — Priority-coloured task bars

- **Statement:** When the gantt renders a task row, the bar **shall** wear a hue
  derived from the task's `priority`.
- **Acceptance (black-box):**
  - `high` priority renders in rose.
  - `normal` priority renders in sky.
  - `low` priority renders in muted grey.
  - Project rows remain in the project's own colour.

### HLR-002 — Milestone rendering

- **Statement:** When a task is a milestone, the gantt **shall** render a single
  diamond glyph at its date cell instead of a span.
- **Acceptance (black-box):** A milestone task with `start_date == due_date`
  shows `◆` at that cell and no span.

### HLR-003 — Dependency indicator

- **Statement:** When a task has a non-empty `depends_on` list, the gantt
  **shall** display a dependency indicator beside the task row.
- **Acceptance (black-box):** A task with `depends_on` shows `└─►` after its
  bar; a task without it does not.

### HLR-004 — Gantt project-focus filter

- **Statement:** The gantt **shall** support the same project-focus filter as
  kanban, bound to `F` to cycle and `esc` to clear.
- **Acceptance (black-box):** Pressing `F` in gantt cycles visible projects and
  hides other projects' rows; the header names the focused project; `esc`
  restores all rows.

---

## 3. Low-level requirements

### LLR-001.1 — `Task.depends_on` field

- **Statement:** `Task` **shall** expose a `depends_on: list[str]` attribute
  defaulting to an empty list.

### LLR-001.2 — `depends_on` persistence

- **Statement:** `Board.save` **shall** persist `depends_on`; `Board.load`
  **shall** default missing values to `[]` without raising.

### LLR-002.1 — Priority-to-hue mapping

- **Statement:** `_task_reach` **shall** map `priority` to a hue before
  identity/project colour: `high` → rose, `normal` → sky, `low` → mut.

### LLR-002.2 — Milestone short-circuit

- **Statement:** `_task_reach` **shall** detect `start_date == due_date` and
  return a single-cell diamond instead of a span.

### LLR-003.1 — Dependency indicator placement

- **Statement:** `render_gantt` **shall** append the dependency indicator to a
  task row when `task.depends_on` is non-empty.

### LLR-004.1 — Focus wiring

- **Statement:** `action_focus_cycle` and `action_focus_exit` **shall** act on
  gantt in addition to kanban.

### LLR-004.2 — Focus render parameter

- **Statement:** `render_gantt` **shall** accept a `focus` parameter and omit
  non-focused projects' rows when it is set.

### LLR-004.3 — Keymap visibility

- **Statement:** `README.md` **shall** document `F` and `esc` as active in the
  gantt view.

---

## 4. User stories / acceptance tests

| US | Observable outcome | Shipped surface | AT |
|---|---|---|---|
| US-1 | High-priority task bar is rose | `render_gantt` output | `test_gantt_priority_colours` |
| US-2 | Milestone draws a diamond | `render_gantt` output | `test_gantt_milestone_diamond` |
| US-3 | Dependency indicator appears | `render_gantt` output | `test_gantt_dependency_indicator` |
| US-4 | Focus filter hides other projects | `App.run_test()` | `test_gantt_focus_filter` |

---

## 5. Validation strategy

- **Layer B (black-box AT):** drive `App.run_test()` for the focus filter.
- **Layer A (white-box):** assert rendered markup colours and glyphs in
  `tests/test_gantt.py`; assert model persistence in `tests/test_models.py`.
- **Ratified stack:** `pytest` + `pytest-asyncio`.
- **Gate:** `pytest tests/ -q` 0 failures, 0 skips.

---

## 6. Open risks

- The existing `test_a_bar_never_wears_an_urgency_hue` will be updated to allow
  priority hues.
- Removing task due meters changes the right-edge law; tests will be updated to
  assert the new marker set.
