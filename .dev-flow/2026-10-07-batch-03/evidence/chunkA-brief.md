# CHUNK A — DeepSeek V4 Pro — increment 001 of batch 2026-10-07-batch-03 (the cleanup batch, MAIN checkout)

You are the software-dev implementer for the SAFE-FIXES half of the cleanup batch in
`C:/Users/jjgh8/Github/taskboard` (Textual TUI; 2529 pytest tests green at base 34bab3c).
A second agent works in ANOTHER worktree (disjoint tree) — you own ONLY this checkout.
Do NOT touch `tests/` (the tests agent is separate).

## YOUR FILES: `taskboard/models.py`, `taskboard/app.py` ONLY.

## THE THREE ITEMS (from BACKLOG; each is a shipped-law fix, minimal change)

1. **S-4 (MEDIUM, security review of batch 2026-10-04-batch-01)**: `run_link_migration`
   (models.py) — in its error handler, a failing `unlink` of its own backup/log can raise
   BEFORE the board and the mark are restored (cleanup-before-restore). Give it the
   MILESTONE OFFER's order (app.py's `run_milestone_offer` does restore-first,
   cleanup-best-effort — read it): on ANY failure, restore the board + the migration mark
   FIRST, then attempt the backup/log cleanup inside its own try/except (never raising),
   and re-raise the original error. No behavior change on the happy path.
2. **S-9 (LOW)**: a board file with `"title": 5` (or a list) crashes string-only render
   paths. Fix at the LOAD boundary: `Task.from_dict` (models.py) coerces a non-text title
   to a sensible fallback (the shipped `"Untitled"` convention is for MISSING titles — for
   a present-but-wrong-typed title use `str(value)` if it stringifies cleanly, else
   `"Untitled"`; NEVER raise, never lose data silently: a coerced title is still the
   user's text when it has one). Mirror the check for `Project.from_dict` name if it has
   the same exposure (check first; only fix what is reachable).
3. **K2-1 (LOW)**: the kanban `?` legend (`legend_entries("kanban", …)` in views.py — you
   may READ it but the fix lives in app.py if the legend call lacks the filter context)
   reads the UNFILTERED board: its `◆` band-rule line shows when ANY band has a milestone,
   including bands folded off screen or filtered out. The shipped `legend_entries` kanban
   branch already takes the presentation/grouping/focus (batch B2a folded K-1/K-2 there) —
   verify whether it now also needs the search filter + the fold state; the minimal fix is
   at the CALLER (app.py) or the legend function's inputs so the entry appears only when a
   DRAWN band carries a milestone. READ views.py's `legend_entries` first; if the fix must
   touch views.py, STOP and report instead (views.py is the render agent's file in the
   NEXT increment — coordinate through the report).

## DISCIPLINE
- NO git mutations. NO tests (the tests agent lands them against your report).
- Verify: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests -q` must stay 2529 passed (K2-1's fix may redden a stale legend test — if so, NAME the test and the new expected behavior in your report, do not fix it).
- English comments, shipped voice.

## REPORT BACK
Per item: what changed (file:line), the design decision where the item allowed one, the
final suite count, anything you left for the tests agent.
