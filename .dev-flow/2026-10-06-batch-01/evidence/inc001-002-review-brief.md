# Adversarial review of increments 001+002 — read-only

You are an adversarial code reviewer. You are the SECOND, independent review of two already-approved
increments in the repo at `C:/Users/jjgh8/Github/taskboard` (Textual TUI task board, ~2500 tests).
A primary reviewer already passed these increments — your value is in what a different model notices.
You may READ anything and RUN tests, but you must NOT modify any file (review-only).

## What changed (all uncommitted, one cumulative diff)

- **Increment 001** — the cascade engine in `taskboard/models.py`, a new block after
  `link_conflicts` (~line 1830): `CASCADE_MODES`, `Plan`, `_cascade_dates`, `_cascade_open`,
  `_cascade_dependents`, `_cascade_downstream`, `_cascade_overlap`, `resolve_mode`, `plan_move`,
  `apply_plan`, `snapshot`, `restore`; and `link_overlap` now delegates to `_cascade_overlap`
  on the stored dates. Tests: `tests/test_cascade.py` (TC-618..TC-630).
- **Increment 002** — the app wiring in `taskboard/app.py`: `action_due_bump` → `_apply_cascade`
  (one seat: plan → snapshot → apply → ONE `{"cascade": …}` undo entry → `save_atomic` when >1
  task → plain-text toast on a width ladder), `_cascade_toast`, `action_cascade_mode` (`m`:
  re-apply the last move under the next mode, refusal literal, C-5 gate), a `"cascade"` branch
  in `action_undo`; `Key("m", …)` in `taskboard/keymap.py`; two help bullets in
  `taskboard/views.py` help_usage; README keybinding row; KEYBAR_BASE updated. Tests:
  `tests/test_cascade_app.py` (AT-607, AT-608, TC-631).

## The contract

`.dev-flow/2026-10-06-batch-01/01-requirements.md` — read §1.3 (the overlap measure + the toast
ladder), LLR-604.1, LLR-604.2, LLR-604.4, and §6.2 (D-626..D-634). The requirements are the law;
the code must match them, not the other way around.

## Hunt for (be specific, cite file:line, execute repros where you can)

1. Engine edge cases the tests miss: cycles in `depends_on` under `together` with mixed dated/
   undated tasks; `plan_move` on a board where the moved task's project was deleted;
   `project_over` when a moved task has no project; `restore` when `snap` holds a task whose
   project vanished.
2. The undo interplay: `m` re-applies after a `u` took the move back (stack state?); an editor
   save between a bump and `m` (the editor is NOT yet cascaded — known, by design); the undo
   stack growing unboundedly with cascade entries.
3. The toast ladder at exotic widths (24, 40, 60): any rung where the count/names logic produces
   a gram­matically wrong or misleading string; the `▌` glyph on a width-1 screen.
4. `save_atomic` failure modes: what does the app do if `save_atomic` raises mid-cascade (the
   undo entry is already pushed — is the in-memory board consistent?)?
5. Anything that smells: dead code, silent rescues, off-by-ones in `_short_title`, the
   `date.min` sort fallback hiding a dated task behind all undated ones (is the toast order still
   sensible?), imports left unused.

Run tests with: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8
python -m pytest <target> -q` (Git Bash). Full suite takes ~6 minutes — you may run it once.

## Report (write it to BOTH your final message AND the file
## `.dev-flow/2026-10-06-batch-01/evidence/inc001-002-deepseek-review.md` — that file is the ONLY
file you may write)

Findings with id DS-N, severity (HIGH/MEDIUM/LOW), file:line, the defect, the fix, and whether
you EXECUTED a repro. End with a verdict: how many findings per severity, and one paragraph on
overall confidence. If you find nothing material, say so plainly — a clean second review is a
useful result.
