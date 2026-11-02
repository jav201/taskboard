# E4 integration — Inc X (HTML deck export)

GREEN-1 (`evidence/green-1.txt`): 2 failed, 531 passed. Both failures were test defects. No source file changed in this step, and no requirement changed.

| # | Test | Class | Cause | Fix |
|---|------|-------|-------|-----|
| 1 | `test_present_html_export.py::test_TC_4737_LLR_4503_7_markup_in_folder_is_literal_toast_text` | `test` | The fixture folder `[red]rx[/red]` holds a `/`, so `pathlib` nests it into two directories. On Windows the toast path reads `[red]rx[\red]`. The code already shows markup literally (`app.py:3068`, `markup=False`). The old oracle read `Notification.message`, which is the raw string whatever `markup` is, so it could not kill the `markup=True` mutant either. | The folder is now `[red]rx[red]`: the same markup in one path segment. The oracle now reads the toast's plain text by the rule Textual's `Toast.render` applies (`Content.from_markup` if `markup`, else `Content`). |
| 2 | `test_report_export_app.py::test_TC_3117_H_is_seated_once_on_the_bar` | `test` | The test paints at 118x30. That is below the ruling-16 threshold, so it is the **test-wrong** case. The assertion read `H Report` from the painted `?` HelpModal. There, `H` is no longer on the global line (`bar=True`). The Keys band lists it as `H   Report` (padded to 3), and at 30 rows the band sits below the fold. | The 118 arm now asserts a bare `H` on the painted bar and no `H Report`. The `?` arm counts `H\s+Report` over the `#help-keys` and `#help-global` text and expects exactly 1 (LLR-4505.5). A new wide arm at 201x30 expects `H Report` on the painted bar. |

## Fit-rule measurement (case 2)

- `keymap.fit_bar`, primary layer: `H Report` first fits at 193 for swimlanes, kanban and focus, and at 183 for agenda and gantt. This matches e3-addenda.
- In the live app the `KeyBar` is 2 cells narrower than the terminal. At terminal width 194 (bar 192) it shows a bare `H`. At terminal width 195 (bar 193) it shows `H Report`. So the app agrees with the fit rules at every width tried, and nothing in the code needed fixing.
- The wide arm uses 201 columns, the wide frame from ruling 1, which is at least 193.

## Deviation recorded (requirement unchanged)

The LLR-4503.7 threshold names the fixture `[red]rx[/red]`. That literal cannot exist as a single folder on any OS. The test uses `[red]rx[red]` and still tests the same requirement statement. This is flagged for the batch-end canon fold, so the threshold literal can be corrected there.

## Negative controls (mutants applied one at a time, then reverted; source tree clean afterwards)

| Mutant | Target test | Result |
|--------|-------------|--------|
| M1 `app.py:3068` Report toast `markup=True` | TC-4737 | KILLED (`'[red]rx[red]' in '…markup0[red]rx\\reports…'` fails, the markup parser consumed the second `[red]`) |
| M2 help band drops `H` (`modals.py` `_key_texts`) | TC-3117 | KILLED (`0 == 1`) |
| M3 `fit_bar` never keeps a word | TC-3117 wide arm | KILLED (`'H Report' in '… ⇥  H  ↓  ↑'` fails) |
| M4 `fit_bar` keeps `H`'s word at any width | TC-3117 118 arm | KILLED (`'  H  ' in '… ⇥  H Report  ↓  ↑'` fails) |

## GREEN-2

`evidence/green-2.txt`: **527 passed, 0 failed**, over 19 files. These are HEAD's 15 test files plus `test_colour_budget.py`, `test_english.py`, `test_prism_laws.py` and `test_modal_keys.py`. `test_markup_census.py` is already among HEAD's 15. A supplementary run of `test_keymap.py` gave 24 passed.

**Count discrepancy, not resolved.** GREEN-1 reports 533 tests (2 + 531). The 15-file set collects 458, and the 19-file set collects 527. GREEN-1's file does not record its command or its file list, so the 6-test gap cannot be attributed from the evidence.
