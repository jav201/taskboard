# E4 test design — independent tester (Opus)

You write the tests for Inc L from the approved design, NOT from the code (the code is being written in
parallel by another model and is not yours to read until your tests are RED on base). You never edit
product code (`taskboard/`, `README.md`).

Role file: `C:\Users\jjgh8\.claude\skills\dev-flow\agents\tester.md` (read it first).

## Inputs (folder `.dev-flow/2026-11-01-v3-incL/` in the worktree `C:/Users/jjgh8/Github/taskboard-wt/capture-proto`)
- `01-requirements.md` — 69 active LLRs (LLR-4304.16 withdrawn), 6 HLRs, 5 ATs; each LLR has a numeric
  threshold and a negative control; the TC numbering rule is in its header.
- `graph-interfaces.cw.md`, `graph-proto-D.cw.md`, `graph-proto-V.cw.md`, `graph-proto-S.cw.md` — every
  `examples:` line is an exact expected value with its TC id; `[Interface: …] offers:` lines are key contracts.
  None of group S's examples was executed at design time (ARCH-4): you are the first to run them; if one is
  wrong against the requirements, write the test from the requirement and list the disagreement.
- `03-pdr-rulings.md` (rounds 0 and 1) and `e4-addenda.md` — override older text. Notably: P-S-1 (TC-4341
  calls `app.check_action("added_list", ())` directly), P-D-10/P-S-2 (a clock that advances 1 s per call for
  TC-4303/TC-4306, monkeypatched where the code reads it), ARCH-1 (shuffled input for TC-4364/TC-4365), ARCH-2
  (TC-4316's board holds a birth record), SEC-1 (TC-4318: no `created` in the push record), SEC-2/SEC-3
  (TC-4372c, TC-4377), P-D-1 (TC-4315's legacy arm compares to the base bytes, a literal oracle you capture
  by running `eb411e1`'s `Board.load`+`save` in the base tree and freeze in the test).
- Existing conventions: `tests/test_all_agenda.py` (2-board registry, `Path.home` redirect, pilot sizes),
  `tests/test_templates_app.py`, `tests/test_link_picker.py`, `tests/test_history.py`,
  `tests/test_marks_directory.py` (byte tests), `tests/test_keymap.py`. Synthetic data only; owner
  `username_subject`; never a real person's name.

## What to write
- `tests/test_task_created.py` — HLR-4301, HLR-4302: the field, every creation path (editor add, template
  insert, link-picker create, `Board.add_task`, seed), keep-paths (edit, move_project, undo restore, rescue),
  serialisation (only when set, str read, non-str round-trip), byte stability (3 old boards vs oracle), old
  entries unchanged on add, the push record (LLR-4302.7), AT-4302, AT-4303.
- `tests/test_added_list.py` — HLR-4303..4306: layer 0 (`added_rows`, `added_moment`, `added_order`,
  `first_created`, `state_boxes`, `render_added_list` at 116x29 and 78x23 — exact strings, cell positions,
  styles) and Textual pilots at 118x30 and 80x24 (keys `N`, `esc`, `↑↓`, `o`, `v`, `enter`, the key row, the
  check_action gate and seat hold, no writes while open by sha256), AT-4301, AT-4304, AT-4305.
- Test names carry the ids: `test_TC_43nn_<why>` / `test_AT_43nn_<why>`; each module docstring states the
  WHY (field report: the owner captures tasks in a hurry and must find them by when they were added; old
  boards must never be rewritten) and the RED conditions.
- If `tests/test_keymap.py` or another existing test must learn about `N`, do NOT edit it unless the design
  says so; list it.

## RED for behavioural reasons
- Import ONLY names that exist at base at module level. Reach new names (`stamp`, `added_rows`,
  `added_moment`, `added_order`, `first_created`, `state_boxes`, `render_added_list`, `AddedList`,
  `ADDED_KEYS`, …) through a helper that turns their absence into an assertion failure with a message
  (`pytest.fail("added_rows missing")`), so on base each test fails on an assertion, never a collection error.

## Prove RED on base
Base tree: `C:/Users/jjgh8/Github/taskboard-wt/incL-base` (clean worktree of `eb411e1`). Copy ONLY your test
files there (scratch: do not commit there), run with cwd = base:
`cd C:/Users/jjgh8/Github/taskboard-wt/incL-base && env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard;print(taskboard.__file__)" && env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -p no:cacheprovider tests/test_task_created.py tests/test_added_list.py -rA`
Save the full transcript (with the `taskboard.__file__` header first) to
`.dev-flow/2026-11-01-v3-incL/evidence/red-base.txt` in the WORKTREE. Every new test must fail; a test that
passes on base must be a guard by design (e.g. keep-paths whose value is None at base, byte stability of old
boards) — list each explicitly. Write `.dev-flow/2026-11-01-v3-incL/evidence/red-summary.md`: counts
(failed/passed/errors), each passing test with why it is a guard, and the TC → LLR map (every active LLR
appears at least once; AT ids too). Delete the copies from the base tree afterwards.

Return ≤ 10 lines: files and test counts, RED counts on base, guards passing on base, LLRs without a test,
disagreements with the graph.
