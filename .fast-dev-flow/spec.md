# Quick Spec — taskboard: 12 colours · custom phases · kanban view · gantt v2

## 1. Objective (1 line)
Expand the project palette 5 -> 12, introduce ordered custom phases (whose order drives progress and estimation), add a full kanban view (grouped, with a matrix swap) where every task sits in its phase, and rebuild the gantt bar with dual-density braille.

## 2. User stories
- As a user with many projects, I want more than 5 project colours, so that projects stay tellable apart at a glance.
- As a user, I want to define my own ordered phases (not just 3 fixed columns), so that the board matches how the work actually flows — and since phases are linear, their order should drive progress and the estimate.
- As a user, I want a kanban view showing ALL tasks in their phase, colour-coded by project (today's swimlanes shows only the first + "N more"), so that I see the real board.

## 3. Acceptance criteria (observable)
- [ ] AC1 PALETTE: 12 project colours are selectable; the original 5 keep their exact hex; a project set to any of the 12 renders in that colour.
- [ ] AC2 PHASES: a board holds an ORDERED phases list (default equal to today's columns); a task references a phase; `blocked` becomes a separate boolean, not a phase.
- [ ] AC3 MIGRATION: loading a legacy board.json maps backlog->Backlog, doing->Doing, done->Done, blocked->Doing + blocked=true, losing no task and no field.
- [ ] AC4 PROGRESS: progress(task) = phase_index / (n_phases - 1); progress(project) = mean of its tasks; both surface as a %.
- [ ] AC5 KANBAN VIEW: a new view renders one column per phase with EVERY task, grouped under its project with the project colour; a blocked task shows a mark without leaving its phase; a key swaps between the grouped and matrix presentations.
- [ ] AC6 WIDTHS: phase columns split the available width (fewer phases -> wider); at >= 6 phases the view scrolls horizontally rather than truncating below a legible floor.
- [ ] AC7 GANTT: the project bar is one continuous braille bar in the project colour, dense (8/8) for the completed share and half-density (4/8) for the remainder, with divider lines between projects, and the % comes from phase weight.

## 4. Validation strategy
Unit tests on pure logic: palette membership/hex, phase ordering + progress maths (incl. 1-phase and empty-project edge cases), the legacy migration mapping (round-trip a legacy board.json fixture and assert no task/field lost), width distribution, and the gantt bar composition (counts of dense vs half glyphs for a given %). Render tests assert the new view places every task in its phase column and marks blocked. Pilot tests drive the view key + the grouped/matrix swap. All existing tests must stay green. Manual smoke: open the real board and confirm it looks unchanged after migration.

## 5. Non-goals
- No per-project phases (phases are per board).
- No drag-and-drop reordering UI in this batch (phases are edited via the project/board modal).
- No change to capture/records/other apps; taskboard only.

## 6. Detected security flags
- [ ] Auth / identity
- [ ] Secrets / config
- [ ] External integrations
- [ ] Sensitive data
- [x] Destructive DB (schema change + migration)
- [ ] Input / attack surface
- [ ] Network / exposure

**security_required:** true

**Risk summary:** This batch changes the on-disk schema of board.json and migrates the user's REAL board (projects, tasks, statuses). The risk is data loss or silent field drop, not attack surface. Mitigations required in phase B: (1) migration happens on LOAD and is non-destructive — unknown/extra fields are preserved, nothing is deleted; (2) a legacy fixture round-trip test asserts task count and fields survive; (3) defaults make a migrated board look identical to today; (4) recommend the user back up ~/.taskboard/board.json before the first run with the new version.

## 7. Batch status
| Field | Value |
|-------|-------|
| Current phase | closed |
| Started | 2026-07-20 |
| Closed | 2026-07-23 |
| Promoted to /dev-flow | no |
| Notes | Design approved via prototype artifact f5405921. 4 increments planned: (1) palette; (2) phases + migration + progress; (3) kanban view + swap; (4) gantt v2. At the upper bound of fast-flow scope. |


## 8. Close (2026-07-23)

### What changed
Four increments, all on `main`: (1) `8589440` palette 5 -> 12 colours, originals keeping their exact hex; (2) `7984c5b` ordered custom phases replace the fixed status — a board owns `phases`, a task has `phase` + a separate `blocked` flag, every view derives its columns from the phase list, progress is positional (`phase_index/(n-1)`), and legacy boards migrate non-destructively; (3) `222ada2` fix: phase resolution is case-insensitive so a stored `"done"` is no longer silently demoted to the first phase; (4) `2fc1d28` new kanban view (key `5`) showing EVERY task in its phase grouped by project, with `tab` swapping to a matrix presentation; (5) `1eab279` gantt project bar rebuilt as one continuous dual-density braille bar (⣿ 8/8 done, ⢕ 4/8 remaining, same colour) split by phase weight, with ┈ dividers between projects.

### How it was tested
86 tests green (from a 60 baseline). 16 named test functions verified present on disk, mapped to the acceptance criteria. Beyond the suite, verified against a COPY of the real board (28 tasks, 3 projects, never touching the original): migration preserved every task, project and field including `notes`; the kanban shows 28/28 task titles where swimlanes hid 23 behind "N more"; the gantt renders the dual-density bar, dividers and percentages; all views width-exact at 40/68/100/140.

### Open risks / pending
- (CLOSED) Phase editor shipped in `01b51ad` (key `f`: add / rename / reorder / delete) with its UI paths covered in `ee5dd68`.
- The gantt timeline gives up ~2 week-columns at width 68 to make room for the `prog/due` column (at 110 it still shows 13 weeks).
- The trailing gantt figure is the project's own due-date distance, NOT a forecast: phase-transition timestamps are not stored, so a velocity estimate would have been invented.
- Two views still print the header word "KANBAN" (the older columns view and the new one).

### Security flags — handling
`Destructive DB` (schema change + migration) fired and was handled: migration runs on load and is non-destructive (unknown keys preserved via `extra` on both Task and Project, proved by a load->save->reload round-trip test); a backup was taken before any work (`~/.taskboard/backups/board-2026-07-23-185817.json`); the real board was never read or written by any test or agent; and verification ran against a copy. One real defect was caught by that verification (the case-insensitive demotion) and fixed in increment 3.


### Addendum — increments 5 & 6 (2026-07-23)
`01b51ad` **phase editor** (key `f`): add / rename / reorder / delete phases from the app. Renaming also moves every task that referenced the phase (otherwise they would be orphaned and demoted on the next load); deleting reassigns tasks to the neighbouring phase and is refused for the last remaining phase; reordering changes only the order, which is what progress and the gantt read.
`ee5dd68` **UI coverage** for those flows, driven through Pilot and asserting persistence by reloading from disk. The riskiest test was mutation-checked: removing the task-moving loop from `rename_phase` makes it fail, so the assertion is real.

Final: **100 tests** (from a 60 baseline). Integrated check against a COPY of the real board (28 tasks, 3 projects): all five views render width-exact; add + move + rename left 28 tasks with zero orphans and nothing demoted after a reload. The real `~/.taskboard/board.json` was never read or written by any test or agent.
