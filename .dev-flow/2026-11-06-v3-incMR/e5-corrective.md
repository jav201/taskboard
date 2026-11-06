# E5 corrective pass — Inc MR-a

Author: `software-dev` (Opus 5.5), one pass. Input head `478b32c`; corrective commit `5d2c880`; records in the
commit after it. Source touched: `taskboard/views.py` only (1 of 4). Tests: `tests/test_milestone_row.py`.
RED-first evidence: `evidence/e5-red.txt` (new tests against the HEAD source); mutant replay:
`evidence/e5-mutant-replay.txt`; GREEN-3: `evidence/green-3.txt`.

## Orchestrator rulings, as applied

| Ruling | Finding | Tag | Fix | Test, RED first | State |
|---|---|---|---|---|---|
| C-1 | mutant 4605.3 | impl | **No source change was needed, and the premise is corrected here.** At `478b32c`, `action_hmove` (`app.py:3444`) already walks `gantt_lane(self._view_board(), …)`, and `gantt_lane` reads `gantt_plan(done_rows=True)`, whose `_hide` filters the classes. The strengthened test is GREEN on the unchanged source (`evidence/e5-red.txt`). The defect described in `05-mutants.md` was the MUTANT's behaviour. The real gap was the test: its two `→` steps from m1 land where the snap-back also lands. | `test_TC_4843…` now asserts each step: `→` m4, m5, m5, then `←` m4, m1, m1. The `←` from m4 is the discriminating step. RED on mutant 39. | executed |
| C-2 | mutant 4605.2 | impl | `_gantt_frame` hands `gantt_plan` the board it received when `done_rows` (`views.py:3586`, `raw if done_rows else board`), so the plan's `_hide` (`views.py:2458`) is the one class-filter seat of the board gantt's rows, lanes and nav column. The frame's own `_hide` stays for its other reads (legend strip, chain, title markers) and for the `done_rows=False` frames (link mode, presentation). Neither seat could be removed outright: dropping the plan's leaves `nav_model` and `gantt_lane` unfiltered (R-4), and dropping the frame's unfilters the legend and the link frame. | TC-4842 unchanged. RED on mutant 38 (it had survived). | executed |
| C-3 / C-5 | F1, SEC-9 | impl / design-gap | `put_label` writes the run's tone as `run:<tone>` (`views.py:2956`). `_gantt_field` tells a run by that tone, never by `len(glyph)`, and paints it with no weekend ground (`views.py:3156`). The docstring now states the invariant: only `put_label` writes `run:`. The change was small, so SEC-9 is fixed rather than sent to the backlog. | New `test_TC_4820c_N9…` (titles `x`, `中`, `Go`; it controls that a ground cell on the same row is shaded). RED at `478b32c`: 2 failed (`x`, `中`). RED on mutant 46. | executed |
| C-3 | F2 | impl (test) | **Correction to F2:** `DANGER`'s `étape` was already decomposed (U+0065 U+0301, read with `ascii()`). It is now spelled as `DECOMPOSED = "e\u0301tape"` so a reader can see it. Added `ZW_INSIDE = "a\u0301\u200bb gate"` (a combining mark and a zero-width space inside), with its `LONG` cut. | TC-4820 gains 4 arms, GREEN (the code already handled them). | executed |
| C-3 | F3 | design-gap | `graph-proto-V.cw.md`: `gantt_lane_label` `in:` gains `GanttAxis ax`, the `task_row` call names `ax`, there is a new `_lane_marks` node, and there are 2 edges. Ledger entry LED-2026-11-06-incMR.8. | n/a, graph text | executed |
| C-4 | F4 | design-gap | `graph-interfaces.cw.md` LABEL PATH step 4 now counts the PLAIN cut label's cells, names `run:<tone>`, and says a 0-cell label is not laid. | n/a, graph text | executed |
| C-4 | F5 | impl | `_LaneMark(NamedTuple)` replaces the dict records (`views.py:2823`). The optional `place` helper was not done: it is BACKLOG MR-BL-1. | covered by the existing TC-48xx (GREEN-3) | executed |
| C-4 | F6 | design-gap | `graph-interfaces.cw.md` pass 3 names the tones `reached`, `soon` and `mut`, and `▲Nd` in `over`. | n/a, graph text | executed |
| C-4 | SEC-8 | impl | none (the guard is correct) | New `test_TC_4820b_SEC6…` (`\u0301`, `\u200b`, `\u0301\u200b`): the row is exactly 118 cells, the field is `ax.w`, and there is no label cell. GREEN at HEAD, as expected. RED on mutant 47 (the guard dropped): 3 failed. | executed |

## Left open
- BACKLOG MR-BL-1 (F5's `place` helper, LOW). MR-BL-2 (an unverified observation: link mode may offer
  hidden-class milestones in its candidate cycle; it is pre-existing and outside MR-a).
- The independent re-check of the `full`/`partial` marks in `02-test-cases.md` (E5) has not been done. It is owed
  by someone who did not write them.
