# E5 — Code review — Inc MR-a (board gantt milestone row)

Reviewer: `code-reviewer` (independent; wrote no code or tests here).
Scope: `git diff 154e260 8e3272e -- taskboard/` (`views.py` +294, `app.py` +17); the test diff was sampled
(`tests/test_milestone_row.py` TC-4820, TC-4833..4838; `tests/test_milestone_marks.py` allow-list).
Design read: `01-requirements.md` §4, `00-e1-rulings.md` R-1..R-8, `graph-interfaces.cw.md`,
`graph-proto-V.cw.md`, `e3-addenda.md` (A-1..A-11, r2 N-8..SEC-7), `e4-deviations.md`, `e4-integration.md`.

**Verdict: PASS-WITH-NOTES.** 0 HIGH, 3 MEDIUM, 3 LOW. Nothing blocks.

## Checks

| Check | Result | State |
|---|---|---|
| The code follows the approved graph | Yes. All 9 units match the frozen contracts. The one stale node is F3. D-1, D-2 and D-3/I-1 are recorded, so no divergence is silent. | executed |
| R-7 LABEL PATH | `put_label` measures the PLAIN text with `cell_len`. `fit` cuts it before placement. `_literal` escapes it once, whole. The run goes in the first cell and `""` in the cells it covers. No cell holds an unescaped label character. A probe at 118 rendered these titles literally at a width of exactly 118: decomposed `étapé`, lone `́`, `x`, `\`, `[` and `中`, each placed after, before and cut. | executed |
| N-8 | `_lane_marks` merges a mark that overlaps an earlier footprint into the earlier bucket. It then recomputes the geometry and re-checks backwards. | executed |
| N-9 | Holds for runs of 2 or more codepoints. It fails for a 1-codepoint label (F1). | executed |
| N-10 | TC-4820 asserts that the milestone row is exactly `W` and every other line is at most `W`. | executed |
| SEC-6 | A 0-cell label is not drawn, and the row stays exactly `W` (lone `́` probe). | executed |
| SEC-7 | TC-4820 has 5 long cuts at 80, plus the cut set at 118. | executed |
| R-4 filtered nav | `_hide` sits once, in `gantt_plan` under `done_rows`. `nav_model` and `gantt_lane` add no filter of their own (A-6). `gantt_lane` reads `_view_board()`, the same board `render_view` and `_nav_columns` use. | executed |
| I-1 `i/N` per cell | `gantt_lane_label` counts from the bucket in `_lane_marks` that holds the selection, which is the rule the mark's count uses. TC-4827b covers it, and its mutant was killed (`e4-integration.md` §2). | executed |
| `hmove` only changed in the gantt | Yes. The branch is guarded by `view_mode == "gantt"` and by the selection being in the lane. Otherwise the base code runs byte-for-byte. Link mode is a modal, and `check_action` already disables `hmove` under any pushed screen, so R-3 holds. The ends of the lane are no-ops. | executed |
| Tests encode intent | Every TC names its negative control. The tests that pass on base by design are TC-4835, TC-4836 and TC-4843d, plus the link golden. They are guards, and the discriminating cases are TC-4833 and TC-4834. TC-4820 overclaims its coverage (F2). | executed |
| Mutant table | Most kills are still `planned`. They are E5's mutant run, not this review. | not-run |

## Findings

### F1 — A one-codepoint label is shaded as a weekend cell (N-9)  [MEDIUM · impl]
- **What:** `_gantt_field` decides that a cell is a label run with `len(glyph) > 1`. A label of one codepoint fails that test and takes the mark branch, where `_on_weekend` shades it on a weekend cell. Examples are a 1-character title (`x`), a single wide glyph (`中`, 2 cells), or any title `_literal` leaves unchanged. The rendered text and the width are still correct (probe).
- **Where:** `taskboard/views.py`, `_gantt_field`, the `if len(glyph) > 1` branch. The run is written by `gantt_milestone_row.put_label`.
- **Why it matters:** this breaks the binding E3-r2 addendum N-9 for one case. N-9 also has no test at all: the tester routed it to qa/ux (`e4-tests.md` F-T4).
- **Suggested fix:** mark the run explicitly instead of inferring it from the codepoint count. This mirrors the `rev:` channel.
  ```python
  # put_label
  cells[start] = (piece, f"run:{tone}")
  # _gantt_field, before the mark branches
  if tone.startswith("run:"):
      out.append(c(glyph, tone[4:])); continue
  ```
  Add one case with the title `x` on a weekend cell that asserts no weekend background.

### F2 — TC-4820 claims combining and zero-width coverage it does not have  [MEDIUM · impl (test)]
- **What:** the docstring says "wide and zero-width glyphs", and A-10 hands SEC-2's combining-mark titles to TC-4820. But `"étape"` in `DANGER` is precomposed (U+00E9), so no case has a combining mark or a 0-cell title. The code handles both (probe: `étapé` and `́` render at exactly 118). The gap is in the evidence, not in the behaviour.
- **Where:** `tests/test_milestone_row.py:509` (`DANGER`).
- **Suggested fix:** add `"étape"` (decomposed) and `"́"` to `DANGER`, with matching `LONG` entries. The second also gives SEC-6 a direct case.

### F3 — The graph does not match the I-1 signature  [MEDIUM · design-gap]
- **What:** `graph-proto-V.cw.md:77` still gives `gantt_lane_label` the inputs `(lane, selected_id, board, today, label_w)`. The shipped function also takes `GanttAxis ax`, and the new helper `_lane_marks` has no node. `e4-integration.md` §2 recorded the change but left the graph as "orchestrator's file".
- **Why it matters:** E5 requires a design-gap fix to update the graph. Until then, the trace and the graph of record do not describe the code.
- **Suggested fix (orchestrator):** add `GanttAxis ax` to the node's `in:`. Add a V-internal `_lane_marks` node with the edges `_lane_marks → gantt_milestone_row` and `_lane_marks → gantt_lane_label`.

### F4 — The wording of LABEL PATH step 4 counts the escaped run  [LOW · design-gap]
- **What:** `graph-interfaces.cw.md:24` says the next `cell_len(piece) - 1` cells hold `""`, where `piece` is the escaped run. Read literally, that overcounts: `\[` is 2 cells for a 1-cell `[`. The code is correct, because it uses the plain text's `cell_len`.
- **Suggested fix:** change the wording to "`cell_len` of the plain cut label, minus 1".

### F5 — Records as dicts; placement code duplicated  [LOW · impl]
- **What:** `_lane_marks` returns `dict`s with string keys, where the module's convention is `NamedTuple` (`GanttGroup`, `FieldGeo`). Passes 2 and 3 repeat the same `ra`/`rb` placement block (`views.py`, `gantt_milestone_row`).
- **Suggested fix:** use a small `NamedTuple` (`_LaneMark`). Optionally add a `place(rec, text, tone, cut_ok)` helper. Neither change is needed to pass.

### F6 — Date-label tones come from the oracle, not the contract  [LOW · design-gap]
- **What:** pass 3 paints a date in `reached` when the lead is reached, in `soon` when its due is today, and else in `mut`. This matches the variant-A oracle (`prototypes/milestone_row/proto.py:258`) and F-T5's M-1 law, but the frozen `func:` names only `over` for `▲Nd`.
- **Suggested fix:** write the three tones into the `gantt_milestone_row` `func:` together with F3.

## Evidence checklist

- ✓ Diff read in full: `views.py` hunks 2408–3780 and `app.py` 56 and 3437–3456 at `8e3272e`.
- ✓ Correctness pass: edge cells, merge, undated members (in the walk, no mark, no tag, as LLR-4602.7 and the walk-order glossary require), a 1-member lane, a folded group, a paged group, an empty selection, and link mode.
- ✓ Simplicity pass: no speculative abstraction. F5 is a nit.
- ✓ Reuse: `fit`, `_literal`, `milestone_mark`, `title_markup`, `_pad` and `gantt_milestone_chip` are reused, and nothing is re-implemented.
- ✓ Tests reviewed for intent: TC-4820, the nav TCs and the re-baselined AT-2603. F2 is noted.
- ✓ Verdict explicit: PASS-WITH-NOTES. No HIGH. F1–F3 are MEDIUM and go to the corrective pass or the backlog, at the orchestrator's choice.

**§4b Independent review cell:** `code-reviewer` · PASS-WITH-NOTES · no HIGH (F1–F3 MEDIUM, F4–F6 LOW, none blocking).
