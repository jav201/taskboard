# CHUNK — DeepSeek V4 Pro — increment 001 of batch 2026-10-07-batch-05 (the carries batch)

You implement increment 001 of batch-05 in the MAIN checkout at
`C:/Users/jjgh8/Github/taskboard`. Two carried items from the BACKLOG, both owned
in `taskboard/models.py`.

## READ FIRST
- The contract: `.dev-flow/2026-10-07-batch-05/01-requirements.md` — HLR-1101/LLR-1101.1
  (S5-3 the failed-backup partial file) and HLR-1102/LLR-1102.1 (one `Mon D` formatter).

## THE WORK — `taskboard/models.py` ONLY, plus TWO NEW test files. No other source. No git.

1. **LLR-1101.1 — `_create_beside` unlinks its file on a failed write.** The helper at
   `taskboard/models.py:1562` writes backup/log files beside the board by exclusive create:
   `with open(p, "xb") as fh: fh.write(data)`. If `fh.write` raises (a full disk), the
   partially-written file STAYS on disk. Wrap the write so that ANY exception from the write
   closes the handle and removes the just-created path best-effort — the removal in a NESTED
   guard that swallows its own errors — and then re-raises the ORIGINAL exception unchanged.
   Style model: the restore-first/best-effort pattern already shipped in this file (see
   `run_link_migration`'s failure path, ~models.py:1692-1754). Both callers (the link
   migration ~1606/1612, the milestone offer ~1720/1729) inherit the law through the helper —
   do NOT touch them.
2. **LLR-1102.1 — one `_md`, owned at models.** `def _md(d: date) -> str: return f"{d:%b} {d.day}"`
   exists THREE times: `taskboard/models.py:2133`, `taskboard/views.py:2680`, `taskboard/app.py:40`.
   Keep the models.py definition; DELETE the views.py and app.py copies and import the models one
   instead (`from .models import _md` — check each file's existing import block for the right
   shape and any name collisions; views.py already imports many names from models). The output
   must be byte-identical — no behavior change anywhere.

## THE TESTS (new files, yours)

3. `tests/test_backup_write.py` — two arms, no real disk-full (mechanism-level patch):
   - arm 1: the write fails AFTER the exclusive create, the removal works → after the call the
     partial file does NOT exist and the ORIGINAL exception propagates.
   - arm 2: the write fails AND `Path.unlink` refuses (raises) → the ORIGINAL exception still
     propagates; the guard adds no new error.
   Drive the helper directly (`from taskboard.models import _create_beside`) in tmp_path; a
   practical mechanism: monkeypatch `builtins.open` (or the file object's `write`) so the
   write raises; assert with `Path.exists`. RED on the base tree: arm 1 finds the partial file.
4. `tests/test_mon_d.py` — the characterization pin:
   - exactly one `def _md` in the package (assert `views._md is models._md` and
     `app._md is models._md`);
   - a 14-date sweep (every month start, Dec 31, Jan 1, Feb 29 on a leap year, a mid-month)
     renders identical strings through all three access paths.

## DISCIPLINE
- Run: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_backup_write.py tests/test_mon_d.py tests/test_team_sync.py tests/test_cleanup.py -q` — all green. Then the FULL suite once: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests -q` — report the count; if anything outside your files reddens, STOP and name it.
- Minimal change, shipped voice, English comments.

## REPORT BACK
Per item: what changed (file:line), the two arms' results, the full-suite count, anything you punted.
