# E4 test design — independent tester (Opus)

You write the tests for Inc K (the capture view) from the approved design, NOT from the code (the code is
being written in parallel by another model and is not yours to read until your tests are RED on base). You
never edit product code (`taskboard/`, `README.md`).

Role file: `C:\Users\jjgh8\.claude\skills\dev-flow\agents\tester.md` (read it first).

## Inputs (folder `.dev-flow/2026-11-01-v3-incK/` in the worktree `C:/Users/jjgh8/Github/taskboard-wt/capture-proto`)
- `01-requirements.md` — 9 HLRs, 203 active LLRs (9 withdrawn: no test), 8 ATs; each LLR has a numeric threshold, a negative control
  and its TC id (numbering rule in the header, incl. its overflow rules).
- `graph-interfaces.cw.md`, `graph-proto-S.cw.md`, `graph-proto-T.cw.md`, `graph-proto-V.cw.md` — every
  `examples:` line is an exact expected value with its TC id; `[Interface: …] offers:` lines are key contracts.
  `e2-trace.txt` maps every LLR/AT to its examples. If an example is wrong against the requirements, write the
  test from the requirement and list the disagreement.
- `00-orchestrator-rulings.md`, `03-pdr-rulings.md` (all rounds) and `e4-addenda.md` — override older text.
  Notably: P-V-2 (a terminal-form `events.Key("alt+d", "d")` posted through the driver must not type into the
  pad), P-V-4 (TC-4413 asserts the README row), P-V-5 (you add `"ReviewList": {}` to the INVENTORY in
  `tests/test_modal_keys.py` — the one existing test you may edit, and say so), R1-1 (`alt+l` divider; assert
  `alt+enter` is NOT bound), P-V-1 (`tab` board cycle).
- Existing conventions: `tests/test_added_list.py` and `tests/test_task_created.py` (Inc L: 2-board registry,
  `Path.home` redirect, pilot sizes 118x30 and 80x24, byte tests), `tests/test_marks_directory.py` and the
  people directory tests (store pattern: lock, atomic, keep_aside, refresh), `tests/test_keymap.py`,
  `tests/test_modal_keys.py`. Synthetic data only; owner `username_subject`; never a real person's name.
  Never touch the real `~/.taskboard`: every test redirects `Path.home` to `tmp_path`.

## What to write (split by HLR so files stay readable)
- `tests/test_inbox_store.py` — note parsing (HLR-4402 layer 0), the store HLR-4407 (schema, load/refresh,
  write_pad incl. the typing union, fresh-state dump/undo (ARCH-1), the pending record (ARCH-4), caps, keep_aside, lock, notice flag, byte stability of `people.json`/`marks.json`
  and old boards), undo/7-day keep HLR-4405 layer 0, images HLR-4408 layer 0, untrusted text HLR-4409 layer 0.
- `tests/test_suggest.py` — HLR-4403 (fixture F, exact scores/why words/order/ties/halving/new-project cut,
  determinism across PYTHONHASHSEED via subprocess if the graph says so, the caps).
- `tests/test_capture_view.py` — HLR-4401, HLR-4402 (render: rule, ghost, hint row, notice), HLR-4404
  (dump through `Board.add_task` → `created` set; other-board path), HLR-4406 (review), pilots at 118x30 and
  80x24, and AT-4401..AT-4408 (black box, through keys and dialogs).
- Test names carry the ids: `test_TC_44nn_<why>` / `test_AT_44nn_<why>`; each module docstring states the WHY
  (the owner captures notes in a hurry and must never lose one; the store must never corrupt boards or the other
  stores) and the RED conditions.

## RED for behavioural reasons
- Import ONLY names that exist at base at module level. Reach new names (`taskboard.inbox`, `taskboard.suggest`,
  `CaptureView`, `PadArea`, `ReviewList`, …) through a helper that turns their absence into an assertion failure
  with a message (`pytest.fail("taskboard.inbox missing")`), so on base each test fails on an assertion, never a
  collection error.

## Prove RED on base
Base tree: `C:/Users/jjgh8/Github/taskboard-wt/incK-base` (clean worktree of `545c18a`). Copy ONLY your test
files there (scratch: do not commit there), run with cwd = base:
`cd C:/Users/jjgh8/Github/taskboard-wt/incK-base && env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard;print(taskboard.__file__)" && env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -p no:cacheprovider tests/test_inbox_store.py tests/test_suggest.py tests/test_capture_view.py -rA`
Save the full transcript (with the `taskboard.__file__` header first) to
`.dev-flow/2026-11-01-v3-incK/evidence/red-base.txt` in the WORKTREE. Every new test must fail; a test that
passes on base must be a guard by design (e.g. byte stability of `people.json`) — list each explicitly. Write
`.dev-flow/2026-11-01-v3-incK/evidence/red-summary.md`: counts (failed/passed/errors), each passing test with
why it is a guard, and the TC → LLR map (every active LLR appears at least once; AT ids too). Restore the base
tree afterwards (`git -C <base> status --short` must be empty: delete your copies, and if you copied the
edited `tests/test_modal_keys.py`, restore it with `git -C <base> checkout -- tests/test_modal_keys.py`).

Return ≤ 10 lines: files and test counts, RED counts on base, guards passing on base, LLRs without a test,
disagreements with the graph.
