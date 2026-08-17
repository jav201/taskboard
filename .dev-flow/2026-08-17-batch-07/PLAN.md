# PLAN — 2026-08-17-batch-07 (living compendium)

**Batch objective.** Add a **Focus Board** view for tracking and detail work: only tasks
marked `pinned` (and projects marked `pinned`) appear. Three presentations:

- **A — Card stream:** vertical cards with title, dates, notes, images, URLs, emoji annotations and colour highlights.
- **C — Inspector split:** left list of pinned items, right detail pane with notes, checklist and image preview.
- **D — Image-first board:** pinned tasks with images lead; tasks without images listed below.

**Mode:** `core` (new view, model contract, interaction change). Language: `en`.
**Where we are:** Phase 0 approved; operator verdict implements all three variants.

## Verified at intake

- **RC-1 base currency:** batch-06 just merged to `origin/main` @ `449aebe`; local `main` is current.
- **Flow currency:** local dev-flow mirror verified current against `~/.claude/commands/` (no diff).
- **Prototype approved:** `prototypes/focus-board-prototype.html`, variants A/C/D.

## Stories (5) — INVEST

| id | story | status | observable outcome |
|---|---|---|---|
| R-01 | **Pin a task.** As a user, I want to pin/unpin a task with a key so it appears in the Focus Board. | READY | `t` toggles `task.pinned`; the flag persists and appears in the task editor. |
| R-02 | **Pin a project.** As a user, I want to pin/unpin a whole project so all its tasks appear in the Focus Board. | READY | `T` toggles `project.pinned`; all tasks of a pinned project are included. |
| R-03 | **Card stream.** As a user, I want to read pinned tasks as cards with dates, notes, images and quick emoji markers. | READY | View `5`/`A` renders cards with spine, emoji row, note snippet, image count and due meter. |
| R-04 | **Inspector split.** As a user, I want a two-pane layout to read full notes and see image previews for the selected pinned task. | READY | View `5`/`C` shows list left, detail right with notes, checklist and image preview. |
| R-05 | **Image-first board.** As a user, I want pinned tasks with images to surface first so visual material is scannable. | READY | View `5`/`D` groups pinned tasks by "with images" / "without images" and shows thumbnails. |

## Trigger evaluation

- **B1** touched symbols: `Task`, `Project`, `render_view`, `views.py`, `app.py`, `keymap.py` — reverse census required.
- **D** interaction change: new view, new bindings — UX review at Phase 2.
- **E** ≥3 stories fired — lane `core`.

## Increment plan

| inc | content | source files |
|---|---|---|
| 1 | Model: `pinned` flag on `Task` and `Project`, load/save, editor checkbox, tests | `models.py`, `modals.py`, `tests/test_app.py` |
| 2 | Core renderer: `render_focus` with card stream + focus ordering; navigation model | `views.py` |
| 3 | Alternate presentations: inspector split + image-first; image preview helpers | `views.py` |
| 4 | App wiring + keymap: view key `5`, `t`/`T` toggle, presentation cycle, README, tests | `app.py`, `keymap.py`, `README.md`, tests |

## Risks / watch-items

- **Image handling.** Terminal graphics protocols (Sixel/iTerm) are unverifiable across terminals. Inline preview will be a placeholder/thumbnail strip; `i` opens the existing ImageViewer for real pixels.
- **Colour highlights.** Stored as simple markup tags or as a separate `highlights` list on the task? Decision: start with rendered highlights in the view only (no persistence) to avoid scope creep; can be promoted later.
- **Pin vs focus.** "Project focus" (`F`) filters the current view to one project; "project pinned" (`T`) marks all its tasks for the Focus Board. These are separate concepts and must stay separate in the UI.

## Conventions honored

≤4 source files/increment · every bound key documented in README · tests enforce keymap contract · no push without green suite.

## Test ledger

| node | suite | last run | result |
|---|---|---|---|
| tests/ | pytest | 2026-08-17 | 850 passed |

## Decision log

| date | decision | by |
|---|---|---|
| 2026-08-17 | Batch opened; operator approved all three variants | operator |
| 2026-08-17 | Flag name `pinned` on Task and Project | orchestrator default |
| 2026-08-17 | View key `5`; presentations cycled with `Tab` inside the view | orchestrator default |
| 2026-08-17 | Colour highlights rendered only (not persisted) to limit scope | orchestrator default |
| 2026-08-17 | `Tab` handled by a single `toggle_presentation` action that dispatches to kanban or focus; avoids duplicate key in seat | implementation |
| 2026-08-17 | Focus card title kept left; emoji ribbon moved to right edge so title reads cleanly | operator feedback |
| 2026-08-17 | Inline note highlights: `==yellow==`, `!!red!!`, `++green++` rendered in Focus Board only | operator feedback |
| 2026-08-17 | Automatic emoji ribbon removed; emojis are user-controlled inside notes | operator feedback |
