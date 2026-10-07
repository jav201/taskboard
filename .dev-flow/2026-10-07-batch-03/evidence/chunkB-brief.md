# CHUNK B (tests) — DeepSeek V4.1 Flash — batch 2026-10-07-batch-03

You are the test author for the cleanup batch in `C:/Users/jjgh8/Github/taskboard` (2529 tests
green; the PRODUCT for S-4/S-9/K2-1's filter half is already implemented — your tests pin it;
the render items of AT-903 arm 1's fold half / arms 2-4 land in increment 002 and your arms for
them will RED until then — that is expected: report the REDs).

## YOUR FILE (new): `tests/test_cleanup.py`

## THE CONTRACT
`.dev-flow/2026-10-07-batch-03/01-requirements.md` — HLR-901/902/903 + LLR-901.1/902.1/903.1
with the exact thresholds (LED .2 folds). House idioms: `tests/test_link_migration.py` (the
migration arms + the refusing-`unlink` monkeypatch pattern), `tests/test_cascade_app.py`
(app driving), `kg_board.milestones(kg_board.shifted(...), date.today())`.

## THE TESTS (ids in docstring + name)

- `test_TC_901_the_failed_migration_restores_first_and_surfaces_the_original_error`:
  drive `run_link_migration` on a legacy board; monkeypatch `Path.unlink` to refuse ONLY the
  cleanup phase (after conversion); assert: the board file's bytes and the migration mark are
  restored (the board loads with the ORIGINAL links and no mark), `result.error` names the
  ORIGINAL failure, and no exception escapes. Plus the happy-path arm (converts, cleans up,
  `result.error is None`).
- `test_TC_902_a_non_text_title_coerces_at_the_boundary`: parametrize over
  `"title": 5 / ["x"] / {"a": 1} / null / true` in a hand-built board dict; assert the loaded
  titles are exactly `5 / Untitled / Untitled / Untitled / True`; a MISSING key stays the
  shipped Untitled; the board saves back with the coerced strings; every view renders without
  raising (drive the app at 118×30 on the `5` board).
- `test_AT_901_902` (one node each in the same file): AT-901 — through the app: a migration
  failure at startup (monkeypatched) shows the toast naming the original failure and the board
  opens unconverted. AT-902 — the `5`-title board opens; the task shows `5`.
- `test_AT_903_the_render_items` — FOUR nodes (arm 1 fold half RED until increment 002, arms
  2-4 RED): arm 1 the kanban `?` legend with a search query hiding every milestone band names
  no `◆` (and names it when one band is drawn); arm 2 a milestones-only project draws its
  rule-only band carrying `◆` with the head's `N open`; arm 3 a late milestone below the fold
  marks the fold row `▾ N more · ▲1 ◆`; arm 4 lanes, agenda and focus each render a milestone
  row carrying `◆` (painted-frame reads).

## DISCIPLINE
- NO git mutations. `tests/test_cleanup.py` ONLY (plus the one folded expectation in
  test_team_sync.py — ALREADY DONE, do not touch).
- Env: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_cleanup.py -q`.
- Capture the RED transcripts for the increment-002 arms (they are the counterfactual).
- English, house style.

## REPORT BACK
The node list, green/RED counts, the RED transcripts for the increment-002 arms.
