# CHUNK B (tests) — DeepSeek V4.1 Flash — increment 001 of batch 2026-10-07-batch-01

You are the test author for the TESTS half of a small cleanup batch in
`C:/Users/jjgh8/Github/taskboard`. A second agent refactors PRODUCT code
(`taskboard/models.py`, `taskboard/app.py`) in parallel — you must NOT touch anything
outside `tests/`. Your tests pin CURRENT behavior; they must pass on the tree as it is AND
after the refactor (the refactor is behavior-preserving by contract).

## YOUR FILE (append-only)
- `tests/test_cascade_app.py` — add the two test functions at the END. Do not modify
  existing tests.

## READ FIRST
The file's header and AT-608 (the refusal idiom), `test_TC_631` (in-test task append), and
the top imports. The app idiom: `run_test(size=(118, 30), notifications=True)`,
`app.selected_task_id = ...; app.refresh_view()`, toasts via
`[str(t.render()) for t in app.screen.query("Toast")]`, board fixture
`kg_board.milestones(kg_board.shifted(path), date.today())` with the renumber key
`seen_view_renumber_2026_07`, and `TaskboardApp(board_path=..., team_sync_interval=1e9)`.

## THE TESTS

1. `async def test_TC_701_the_c5_gate_refuses_when_the_moved_task_vanished(tmp_path)`
   (docstring id `TC-701`): LLR-604.4's error arm — the moved task deleted between the move
   and `m`. The UI cannot reach this (a delete pushes its own undo entry), so synthesize it:
   drive a real `+` on `tm2`, then REPLACE the undo stack's top entry with a cascade entry
   whose `task_id` names a task that does not exist (e.g. set `entry["cascade"]["task_id"] =
   "gone"` on the real entry — keep its `tasks` list), press `m`, and assert: the refusal
   toast `m re-applies the last date move — nothing to re-apply` and NO date on the board
   changed. (Read `app._undo_stack[-1]` and mutate the dict in place — the entry shape is
   `{"cascade": {"task_id", "sd", "dd", "mode", "tasks": [...]}}`.)

2. `async def test_TC_702_the_toast_fits_and_degrades_below_80(tmp_path)`
   (docstring id `TC-702`): pin GAP-3's degrade-by-design. On the shifted+milestones board
   at 118x30, select `tm2`, press `+`, then for the rendered toast text assert the ladder's
   contract at narrow widths: re-render the toast through the app for widths 80, 60, 40, 24
   (call `app._cascade_toast(app.board.task_by_id("tm2"), plan, 0)` for a fresh
   `plan = plan_move(app.board, "tm2", 0, 1, resolve_mode(app.board, "tm2"), date.today())`
   and measure with `taskboard.views.vis`) — assert `vis(text) <= width` for each width and
   that at 24 the text is non-empty. Import `plan_move`, `resolve_mode` from
   `taskboard.models` and `vis` from `taskboard.views`.

## DISCIPLINE
- NO git mutations. Append-only in the one file. Run ONLY your two tests plus the file:
  `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m
  pytest tests/test_cascade_app.py -q` (12+2 nodes must pass).
- English, matching the file's existing style.

## REPORT BACK
The two test names, the run counts, any deviation.
