# CHUNK — DeepSeek V4.1 Flash — increment 004 of batch 2026-10-07-batch-05 (the carries batch)

You implement increment 004 of batch-05 in the MAIN checkout at
`C:/Users/jjgh8/Github/taskboard`. The test-strength carries (qa P4 F-3..F-5).

## READ FIRST
- The contract: `.dev-flow/2026-10-07-batch-05/01-requirements.md` — HLR-1106/LLR-1106.1.
- The arms: `tests/test_milestones.py::test_AT_601_a_task_becomes_a_milestone_saved_undoable_said_and_pushed`
  and `tests/test_gantt_milestones.py::test_AT_602_milestones_read_as_dates_reached_ones_quiet_the_ruler_marks_them`.

## THE WORK — `tests/test_milestones.py` and `tests/test_gantt_milestones.py` ONLY. NO source
## files. No git. (Parallel agents own `taskboard/models.py` and `taskboard/app.py` — do NOT
## touch anything under `taskboard/`.)

1. **The key-walking arms.** Wherever the AT-601/AT-602 arms ASSIGN `app.selected_task_id`
   directly, rewrite them to reach the selection with KEY PRESSES alone (the shipped
   navigation: the arrows/`j`/`k` move the selection — look at how
   `tests/test_chainmap_app.py` walks the selection with `pilot.press` for the house pattern).
   The outcome assertions stay byte-identical — only the path to the selection changes.
2. **One team-folder arm.** Add ONE arm that drives the offer-converted milestones into a
   TEAM folder end to end (the `M` path): the house team fixture is the `shared/team.json`
   folder pattern — see how `tests/test_team_sync.py` or the chainmap/milestone tests build a
   team folder, and the offer's conversion path (`run_milestone_offer` / the `M` key on a
   converted milestone). If a true end-to-end arm exceeds what the fixture allows, write the
   strongest arm the fixture supports and SAY SO in your report — do not fake it.
3. **AT-602's ash `◆` at the exact column.** The arm that checks the month-row ash `◆`
   currently accepts "any" `◆`; pin it to the exact column (Mockups' month, per the test's
   own fixture — read the fixture's dates and compute the expected column the way the shipped
   axis math does, or pin the observed correct column after verifying it by hand against the
   fixture).

## DISCIPLINE
- Run: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_milestones.py tests/test_gantt_milestones.py -q` — green. Then the FULL suite once — report the count; if anything outside your files reddens, STOP and name it.
- A grep pin: `grep -n "selected_task_id =" tests/test_milestones.py tests/test_gantt_milestones.py`
  must show no direct assignment inside the AMENDED arms' bodies (module-level fixtures may keep theirs).

## REPORT BACK
Per arm: what changed, what now walks with keys, the team-folder arm's coverage (or its declared limit), the column pin, the full-suite count.
