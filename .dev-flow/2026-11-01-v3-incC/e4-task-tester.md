# E4 test design — independent tester (Opus)

You write the tests for Inc C from the approved design, NOT from the code (the code is being written in
parallel by another model and is not yours to read until your tests are RED on base). You never edit
product code (`taskboard/`).

Role file: `C:\Users\jjgh8\.claude\skills\dev-flow\agents\tester.md` (read it first).

## Inputs (folder `.dev-flow/2026-11-01-v3-incC/` in the worktree `C:/Users/jjgh8/Github/taskboard-wt/capture-proto`)
- `01-requirements.md` — 67 LLRs, 6 HLRs, 4 ATs; each LLR has a numeric threshold and a negative control.
- `graph-interfaces.cw.md`, `graph-proto-V.cw.md`, `graph-proto-M1.cw.md`, `graph-proto-M2.cw.md` — every
  `examples:` line is an exact expected value with its TC id; `[Interface: …] offers:` lines are key contracts.
- `03-pdr-rulings.md` — rulings override older text (e.g. pens/colour keys are allowed by check_action and
  return early without notes focus; tests post `events.Key("alt+5", "5")` / `Key("alt+c", "c")` with the character).
- Existing test conventions: `tests/test_highlight_segments.py`, `tests/test_edit_window.py`,
  `tests/test_people_picker.py`, `tests/test_modal_keys.py` (fixtures, how the editor is opened in a pilot,
  synthetic boards). Synthetic data only; never a real person's name (use `username_subject` for an owner).

## What to write
- `tests/test_colour_notes.py` — layer 0: tokeniser (LLR-4201.1–.10, incl. the derived-set oracle with an
  independent reference scanner written in the test from the requirements, the base-equivalence set of
  test_highlight_segments.py, linearity), surfaces (LLR-4202.1–.8: `_highlight_markup`, `notes_text`,
  mentions, `present_note_lines`, `notes_html`, deck/workspace CSS), C-4 palette (LLR-4206.1–.5 computed
  with rich `Color` and a WCAG function in the test), AT-4203 (HTML export through `report_html.extract` +
  `write_reports`), AT-4204 (legacy notes render byte-identically to a frozen base oracle).
- `tests/test_colour_pens.py` — Textual pilot: pens (LLR-4203.1–.17 incl. the parser test LLR-4203.16 via
  `textual._xterm_parser.XTermParser` after importing `taskboard.modals`), label at 118x30 and 80x24
  (LLR-4203.9 / 4202.10), live ink on rendered cells (LLR-4204.1–.9, incl. theme isolation, fail-safe with a
  monkeypatched `colour_spans` that raises, lone surrogate), AT-4201.
- `tests/test_colour_palette.py` — pilot: palette (LLR-4205.1–.16), details label (LLR-4202.9), AT-4202.
- `tests/test_modal_keys.py` — add `ColourPalette` to the modal inventory exactly as the design says (M2).
- Test names carry the ids: `test_TC_42nn_<why>` / `test_AT_42nn_<why>`; each module docstring states the
  WHY (field report: the operator writes multicolour notes like pens in a notebook) and the RED conditions.

## RED for behavioural reasons
- Import ONLY names that exist at base at module level. Reach new names (`colour_spans`, `PEN_CODES`,
  `Span`, `recolour`, `colour_target`, `ColourPalette`, …) through a helper that turns their absence into an
  assertion failure with a message (e.g. `pytest.fail("colour_spans missing")`), so on base each test fails on
  an assertion, not a collection ImportError.

## Prove RED on base
Base tree: `C:/Users/jjgh8/Github/taskboard-wt/incC-base` (clean worktree of `0a8dfaa`). Copy ONLY your
test files there (the base tree is scratch: do not commit there), and run with cwd = base:
`cd C:/Users/jjgh8/Github/taskboard-wt/incC-base && env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard;print(taskboard.__file__)" && env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -p no:cacheprovider tests/test_colour_notes.py tests/test_colour_pens.py tests/test_colour_palette.py -rA`
Save the full transcript (with the `taskboard.__file__` header) to
`.dev-flow/2026-11-01-v3-incC/evidence/red-base.txt` in the WORKTREE. Every new test must fail; tests that
pass on base must be legacy guards by design (AT-4204, LLR-4201.3) — list them explicitly. Write
`.dev-flow/2026-11-01-v3-incC/evidence/red-summary.md`: counts (failed/passed/errors), each passing test with
why it is a guard, and the TC → LLR map (every LLR id appears at least once).

Return ≤10 lines: files and test counts, RED counts on base, guards passing on base, LLRs without a test.
