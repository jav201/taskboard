# CHUNK — DeepSeek V4 Pro — increment 002 of batch 2026-10-07-batch-05 (the carries batch)

You implement increment 002 of batch-05 in the MAIN checkout at
`C:/Users/jjgh8/Github/taskboard`. Two UX carries from the BACKLOG.

## READ FIRST
- The contract: `.dev-flow/2026-10-07-batch-05/01-requirements.md` — HLR-1103/LLR-1103.1
  (the single-task undo toast) and HLR-1104/LLR-1104.1 (the `?` help never cuts a word).

## THE WORK — `taskboard/app.py`, `taskboard/modals.py`, and — ONLY if the clip's seat
## lives there — `taskboard/views.py`. Plus TWO NEW test files. No other source. No git.

A PARALLEL agent owns `taskboard/models.py` and nothing else; do NOT touch it.

1. **LLR-1103.1 — `u` on a single-task change says what came back.** `app.action_undo`
   (~app.py:1408) has branches for milestones/migration/cascade and then a SINGLE-TASK
   fall-through (~1463-1473: restores the task's fields, or re-inserts a deleted task, then
   saves and refreshes — SILENT). Add ONE `self.notify(...)` there: a single line naming the
   task (`title="Undo"`, `severity="information"`, `markup=False`), placed BEFORE the save,
   covering both the field-restore and the re-insert sub-paths. The other branches and the
   stale-skip (purged task → `continue`, silent) stay exactly as shipped. Pin the literal in
   your test; it must include the task's title.
2. **LLR-1104.1 — the `?` help clips at word boundaries.** FIRST investigate where the
   mid-word cut actually happens at 80 cells: `HelpModal` (modals.py:1750) renders
   `legend_entries` (views.py:6882) and `help_usage` as `Label`s. Reproduce at 80×24 on a
   board with a long legend meaning / usage bullet; find the true seat (Label wrap config?
   a manual width in the compose? the example lines?). THEN fix at that seat so no line ends
   mid-word: break at word boundaries, and when a word must be cut, clip at the last fitting
   word and append `…`; an unbreakable token longer than the width clips at the edge with `…`.
   Every legend/help line, not only the new ones.

## THE TESTS (new files, yours)

3. `tests/test_undo_toast.py` — app-level (the house pilot pattern: `TaskboardApp`,
   `run_test`, read toasts off the painted `Toast`): drive a real SINGLE-TASK mutation with
   keys (explore which shipped mutation pushes a one-task undo entry — e.g. an edit via the
   task editor), press `u`, assert the toast equals your pinned literal with the task's title
   (read it back like `tests/test_markup_sites.py`'s `_toast_check` does); and the negative
   arm: an undo whose entry went stale (task purged) stays silent. RED on base: no toast.
4. `tests/test_help_clip.py` — open the `?` modal at 80×24 on a fixture board carrying a
   deliberately long legend meaning and a long usage bullet; assert every visible help line
   ends at a word boundary or with `…` (check each painted line's tail), including the
   exact-edge and overlong-token fixtures.

## SANDBOX (the first attempt died on this)
- NEVER write or run anything outside the project tree: no /tmp scripts. Put every
  repro/scratch script under `.dev-flow/2026-10-07-batch-05/evidence/` (inside the
  project, writable) and run it with `env -u NO_COLOR PYTHONIOENCODING=utf-8 python
  .dev-flow/2026-10-07-batch-05/evidence/<name>.py` from the repo root. Do not read
  or write site-packages either — everything you need is in the repo.

## DISCIPLINE
- Run: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_undo_toast.py tests/test_help_clip.py -q` — green. Then the FULL suite once — report the count; if anything outside your files reddens, STOP and name it.
- Minimal change, shipped voice, English comments.

## REPORT BACK
Per item: what changed (file:line), where the mid-word cut lived, the two tests' results, the full-suite count, anything you punted.
