# Quick Spec — implement the Fable-5 visual redesigns (gantt · columns · agenda)

## 1. Objective
Bring the three approved Fable-5 redesigns into the real app: make schedule risk visual in the gantt, collapse columns cards to one heat-sorted line, and turn the agenda into a shared-axis due dot-plot. Reference mockup: artifact c86895c7 / generator tmp/gen_mockup.py.

## 2. User stories
- As a user, I want to see at a glance which projects/tasks have crossed "today" and which are overdue, without reading small "-5d" text.
- As a user, I want the columns board denser and ordered so the most urgent card is on top of each column.
- As a user, I want the agenda to show due dates on a time axis so distance = urgency and clusters = crunch weeks.

## 3. Acceptance criteria (observable)
- [ ] AC1 GANTT today-rule: a full-height vertical rule (teal `┃`) is drawn at today's column across every project/task row; rows stay width-exact.
- [ ] AC2 GANTT due diamond: each project shows a `◆` at its due-date position on the timeline — red when the due date is before today, bright otherwise; a project with no due date shows none.
- [ ] AC3 GANTT task colour: a task bar is red when overdue, amber when due today, else the project colour (no more uniform grey); the header shows a `▲ N past due` count.
- [ ] AC4 COLUMNS one-line cards: each card is a single line (heat glyph + project colour chip + name + relative due), cards within a phase are sorted by due date (soonest first, undated last), and each column header shows a `N late` count.
- [ ] AC5 AGENDA dot-plot: every due task is a `●` on one shared day-axis with a today rule; urgency reads from distance to the rule; the OVERDUE/TODAY/THIS-WEEK sub-headers and the braille progress dots are removed; width-exact.
- [ ] AC6: all existing tests stay green; each new behaviour has a test; the real board is never read/written by tests.

## 4. Validation strategy
Three increments, one view each (gantt / columns / agenda), each = views.py + tests/test_app.py. Per view: unit/render tests asserting the new glyphs/positions (today-rule column, diamond side of rule for a past-vs-future due, task colour by urgency, one-line card count + sort order, dot positions), plus the existing width-sweep. Manual smoke each increment: render the REAL board (via a copy) and eyeball. Escape hatch: if any single view can't be done inside 2 files or the batch drifts, stop and offer /dev-flow.

## 5. Non-goals
- No change to swimlanes or kanban views.
- No new interaction/keys (these are render changes to existing views on their existing keys 4/2/3).
- Not guaranteeing 256-colour terminals distinguish every project chip (flagged risk, see below).

## 6. Detected security flags
- [ ] all clear
**security_required:** false (pure rendering; no data-model or persistence change; no I/O).

## 7. Open design decision (needs Javier)
The gantt PROGRESS bar: today's bar is the dual-density braille `⣿`(done)/`⢕`(remaining) you tuned over several iterations. Fable-5's proposal replaces it with a solid `█`(done, project colour) + quiet `░`(remaining, dim) track, arguing the new today-rule and due-diamond read better against a calm background (2-colours-per-cell). DECIDED (Javier): OPTION B — keep the ⣿/⢕ dual-density progress bar; add the today-rule + due-diamond + urgency-coloured task bars on top of it.

## 8. Batch status
| Field | Value |
|-------|-------|
| Current phase | closed |
| Started | 2026-07-24 |
| Notes | 3 view redesigns — at the upper bound of fast-dev-flow (same as the prior batch). Promote to /dev-flow if it drifts. |


## 9. Close (2026-07-24)
Three Fable-5 view redesigns landed, all on main, 121 tests (from a 104 baseline):
- `169d454` GANTT — full-height teal today-rule across every row, per-project due `◆` diamond (red past / bright future, `◂`/`▸` clamp off-window), task bars coloured by urgency; kept the ⣿/⢕ dual-density bar underneath (Javier's decision) + `▲ N past due` header.
- `4fd4a1d` COLUMNS — one-line heat cards (`█▓▒░·✓` by urgency + project chip + name + relative due), sorted by due (urgency gradient top-down), `N late` header. 2x density.
- `cf9a07d` AGENDA — shared-axis due dot-plot with today-rule; distance = urgency, vertical clusters = crunch; dropped the OVERDUE/TODAY/THIS-WEEK headers; undated tasks kept under a `no date` group.
Verified against a COPY of the real board (28 tasks): all five views width-exact, board never touched. Origin of the design: a Fable-5 agent prototype (artifact c86895c7), approved by Javier.
Minor follow-ups (not blocking): dead `_URG_BRAILLE`/`AGENDA_GROUPS` in views.py now unused; agenda axis span is fixed (far dates clamp to the edge) — could be made adaptive; two views still titled with their own names is fine now (columns = COLUMNS, kanban = KANBAN).
