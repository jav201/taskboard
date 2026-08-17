# Postmortem — 2026-08-17-batch-06

## Verdict
**Shipped.** Full suite green (841 passed). Operator approved merge.

## What worked
- Reusing `focused_project_id` for both kanban and gantt kept the model simple and the behavior consistent.
- Adding `depends_on` as a plain `list[str]` was a minimal, round-trip-safe model change.
- Reserving 3 cells for the dependency indicator on every row avoided the field misalignment that appeared when the indicator was conditional.

## What fought back
- **Gantt width pins shifted.** Reducing the title width for the dependency indicator changed the measured title lengths in `test_a_task_whose_reach_starts_later_gets_a_wider_title`. The fix was to reserve the 3 cells always and update the pin.
- **Date-dependent archive test failed.** `test_the_purge_says_the_count_before_it_moves_anything` uses `TODAY = 2026-07-30` but the app uses real `date.today()`; on 2026-08-17 a task "moved 2 days ago" relative to TODAY was exactly 20 days old and got auto-swept. Patched `taskboard.app.date` and `taskboard.models.date` with a fake `today()` returning TODAY.
- **Stale view-key test.** `test_url_renders_link_and_arrow` still pressed `3` expecting agenda; `3` is gantt after the renumbering. Changed to `2`.

## Lessons
- Any layout change that makes a prefix width conditional must be measured against the row's right-edge alignment; a net-neutral width change is not enough if the conditional branch changes the pad distribution.
- Tests that compare against `date.today()` are ticking time bombs; pin the date or measure against a fixed anchor.

## Debt / next batch hook
- Batch-07 will add the Focus Board view (card stream, inspector split, image-first). It needs a new `pinned` flag on `Task` and possibly `Project`, plus new view mode and bindings.
