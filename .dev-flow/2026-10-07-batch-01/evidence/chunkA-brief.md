# CHUNK A (product) — DeepSeek V4 Pro — increment 001 of batch 2026-10-07-batch-01

You are the software-dev implementer for the PRODUCT half of a small cleanup batch in
`C:/Users/jjgh8/Github/taskboard` (Textual TUI; 2512 pytest tests green at base `f665425`).
A second agent works on TESTS only; you must NOT touch anything under `tests/`.

## YOUR FILES (exclusive)
- `taskboard/models.py`
- `taskboard/app.py`

## THE WORK — three residue items from the previous batch's P4 review. BEHAVIOR-PRESERVING
refactors only; the full suite must stay green with zero changes to any test.

1. **DS-5 — the app reuses the tested restore.** `models.py` ships
   `restore(board, snap: dict)` (unit-tested by TC-623/630) but `app.py` hand-rolls the same
   loop twice: in `action_cascade_mode` (~line 1213: restoring `cas["tasks"]` before the
   re-apply) and in `action_undo`'s `"cascade"` branch (~line 1291). Replace BOTH hand-rolled
   loops with calls to `restore`: build the snap dict `{task_id: (start_date, due_date)}` from
   the entry's `tasks` list and call `restore(self.board, snap)`. The skip-vanished-tasks
   semantics live inside `models.restore` already — do not re-implement it.

2. **ARCH4-4/SEC4-6 — one today-base rule.** `bump_due` (models.py ~658) bases an undated due
   on `today`; `plan_move` (models.py ~1917-1920) re-implements the same base for an undated
   MOVED task. Extract ONE module-level helper in models.py, e.g.
   `def date_base(stored: str | None, today: date) -> date` returning
   `parse_iso(stored) or today`, and use it in BOTH seats. No signature changes to
   `bump_due` or `plan_move`; no behavior change.

3. **ARCH4-3 — document the totals.** `Plan.conflicts` (the after-state TOTALS) is computed
   but consumed only by tests; `new_conflicts` (the ADDED days) is the production field. Add
   a docstring line on the `Plan` dataclass field saying exactly that: totals, kept as the
   tested intermediate (TC-629); production reads `new_conflicts`.

## DISCIPLINE
- NO git mutations. NO files beyond the two above. NO behavior changes — if you find you
  need one, STOP and report.
- Verify with the FULL suite:
  `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests -q`
  (expect 2512 passed; `test_win_clipboard_roundtrip` MAY fail — the declared G-011 flake;
  any OTHER failure is yours to fix by correcting the refactor, never the tests).
- English comments matching the surrounding voice.

## REPORT BACK
What changed per file (file:line), the final suite count, any deviation.
