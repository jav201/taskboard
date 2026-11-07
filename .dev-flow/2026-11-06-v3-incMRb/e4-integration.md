# E4 — integration — Inc MR-b (the presentation's milestones share one row)

**Role:** E4 integration step (software-dev). Brings the build (`4543a45`) and the independent tests (`52c4808`, `688dc9b`) to GREEN and applies the orchestrator's rulings at the seams.
**Worktree:** `C:\Users\jjgh8\Github\taskboard-wt\ms-row-proto`, branch `feat/milestone-row-present`. `taskboard.__file__` = `…\ms-row-proto\taskboard\__init__.py` (printed in each evidence header).
**Command:** `env -u NO_COLOR python -m pytest -p no:cacheprovider -q -rfE <set>`. The set has the 2 new files, the 4 changed old files, MR-a's `test_milestone_row.py`, `test_milestone_row_at.py` and `test_gantt_milestones.py`, and the law guards `test_colour_budget.py`, `test_colour_budget_app.py`, `test_english.py`, `test_prism_laws.py`, `test_markup_census.py` and `test_modal_keys.py`.
**MR-a tests:** byte-identical to `8ca174c` (the `git diff --stat` in each evidence header is empty).

## 1. GREEN-1 — `executed`, 6 failed, 429 passed (`evidence/green-1.txt`)

| # | Failing node | Class | Cause | Fix |
|---|---|---|---|---|
| F-1 | `test_present_milestone_row.py::test_TC_4922_…down_from_the_head_walks_the_row` | `test` | (a) The test found the cursor row only by the lead ` ⟦▎`. That lead belongs to the milestone row (LLR-4652.4). A cursor TASK row is drawn as at base: `  ▎ <title>` with the `⟦━⟧` echo on its bar (graph-proto-V `_present_task_row`, LLR-4651.4). So the 5th `↓` (`Pilot store list`) found no row. (b) The test compared 10-character title prefixes. View 3's label column is 17 cells, so `gantt_lane_label` cuts with `…` and keeps the tag (`Steering… 1/2`), as R-7 and LLR-4652.4 require. | (a) New fixture reader `milestone_row_present_fixture.cursor_rows(r)`: the ` ⟦▎` milestone row, or a `  ▎` task row that carries `⟦`. (b) The label must be the whole title, or a head of at least 8 cells cut with `…` that is a true prefix of the full title, with the `k/n` tag removed first. This check is stricter than before: the old one only compared a prefix. The row positions `[4, 4, 4, 4, 5]` are unchanged. |
| F-2 | `test_present_milestone_row_at.py::test_AT_4653_…` | `test` | Same as F-1(a): the walk's task stops were looked for by ` ⟦▎`. | `cursor_rows(r)`. Every other assertion is unchanged. |
| F-3, F-4 | `test_present_milestone_row_at.py::test_AT_4654_hiding_milestones_from_the_row[size0, size1]` | `test` | `space` on m3 moves the cursor to the next stop, m4. This is base `action_hide`, and LLR-4653.4 does not change it. After `a`, m3 is back and shares m4's cell, so the cursor member leads that cell: `▲2`. The test expected `■2`, which is the unselected lead. AT-4654 itself only says "m3 back on the row". | Assert that the cursor is `tm4`, that `at["tm3"] == at["tm4"]`, and that the cell reads `▲2`. If m3 were not back, the cell would read `▲` with no count, so this still kills the "m3 not restored" mutant. |
| F-5 | `test_present_note_highlights.py::test_AT_2902_…[size0]` (118x30) | `test` | The blocks now follow the stop order (LLR-4653.5), so the marker-free twin's block (`Judge rubric`) sits in the right column, on a row ABOVE the marked note's `alpha` row. The test read the first frame row that contains `alpha`, and that row is now the twin's, which is ink. The E4 rewrite moved `_block` to column-aware reading but left this read row-wise. | New readers `_col_bounds`, `_col`, `_block_rows` and `_col_spans`. `_block` keeps its old output. The `alpha` and `lima` rows are read in the marked block's own column only. **NC run:** pointing the read at the twin's column (`Judge rubric`) → RED at both sizes (2 failed), so the check can fail. |
| F-6 | `test_milestone_marks.py::test_TC_2604_the_sites_enumeration…` | `test` (census entry), **J-1** | `_present_lane_row` draws no mark of its own. It takes the field from `gantt_milestone_row` and the label from `gantt_lane_label`, which are MR-a's units, and both call `milestone_mark(` (`views.py:2993`, `:3024`, `:3031`, plus `_lane_marks` `:2864`). The row already goes through the seat, so the census entry is wrong, not the code. | J-1 applied (§2). |

There were no `impl` or `seam` failures. No production file changed in this step.

## 2. Rulings

- **J-1 (B-5, `test_milestone_marks`):** `_present_lane_row` already goes through the seat, through MR-a's `gantt_milestone_row` (field) and `gantt_lane_label` (label). Per the ruling, I **corrected the census entry**, not the code. The one entry is replaced by two that name the seat's callers: `presentation milestone row field → gantt_milestone_row` and `presentation milestone row label → gantt_lane_label`. A new assertion keeps the chain closed: the body of `_present_lane_row` calls `gantt_milestone_row(` and `gantt_lane_label(` and has no literal `◆`, and `_present_task_row` no longer calls `milestone_mark(` or `gantt_milestone_cells(` (A-2). The marks law (D1, one seat) is not weakened. A milestone mark in the presentation drawn outside the seat would still fail the census through `_diamond_code_lines`, and so would a `_present_lane_row` that stopped using MR-a's units.
- **J-2 (tester F-1):** I amended LLR-4652.10 in `01-requirements.md`. The negative control is now `\[x` (base draws `▌ [x`). `a\[b]` is withdrawn as a RED-on-base claim and kept as a positive case. The 6/6 count does not change. Ledger entry: `LED-2026-11-06-incMRb.10`.
  - **Pending, not ruled:** LLR-4652.9's threshold makes the same wrong claim (`a\[b]` reads `a[b]` on base). TC-4919 already carries `\[x` as its RED regression. I did not amend LLR-4652.9 because the ruling names only LLR-4652.10. Routed to the orchestrator.

## 3. GREEN-2 — see `evidence/green-2.txt`

Same command, same set, same worktree, HEAD `688dc9b` plus the working-tree fixes above. `taskboard.__file__` = `…\ms-row-proto\taskboard\__init__.py`. MR-a's tests are byte-identical to `8ca174c`.

## 4. Result

**GREEN-2 `executed`: 435 passed, 0 failed, pytest exit 0 (212.6 s).** Each of the 6 GREEN-1 failures was fixed as a `test` defect within the graph. No law and no assertion was weakened: the F-1 label check and the J-1 chain assertion are stricter than before, and the F-5 column read was proven RED-capable by an NC run.

## 5. Files changed in this step (tests and docs only, 0 source files)

- `tests/milestone_row_present_fixture.py` — `cursor_rows`
- `tests/test_present_milestone_row.py` — TC-4922
- `tests/test_present_milestone_row_at.py` — AT-4653, AT-4654
- `tests/test_present_note_highlights.py` — AT-2902 column readers
- `tests/test_milestone_marks.py` — J-1 census entry and chain assertion
- `.dev-flow/2026-11-06-v3-incMRb/01-requirements.md`, `01-requirements-ledger.md` — J-2
- `.dev-flow/2026-11-06-v3-incMRb/e4-integration.md`, `evidence/green-1.txt`, `evidence/green-2.txt`

## 6. Limits

- This step ran the scoped set, not the full suite. The full suite belongs to the batch close (E-close).
- The mutant runner's `planned` NCs (`e4-tests.md` §6) stay `planned`. The only mutant run here is F-5's column NC.
- B-6 (a real capture of view 2 on MR-F at 118x30) is still `blocked` on the operator's RB-1 review. It is not this step's work.
