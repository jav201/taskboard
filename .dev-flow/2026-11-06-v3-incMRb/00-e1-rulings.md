# MR-b: orchestrator rulings (2026-11-06)

MR-a's rulings R-1..R-8, I-1, I-2 and C-1..C-5 (`.dev-flow/2026-11-06-v3-incMR/`) apply wherever the presentation draws the same row.

- **RB-1: the stop order is accepted.** In all three views, the cursor, the view-1 briefs and the view-2 blocks follow one order: milestones by date, then tasks. The operator sees this at review.
- **RB-2 (E2-F1, MAJOR, pre-existing): `_present_brief` joins the slice, making 10 units.**
  - The defect: it doubles a trailing `\` while escaping, so the line comes out one cell too wide. The fix: measure the width on the rendered (escaped) text, or escape with the same `_literal` helper R-7 uses.
  - AT-4655 then holds as written.
  - Regression test: a title ending in `\` renders at exactly the frame width. It is RED on base.
- **RB-3 (F2): the R-7 cut applies at every width.** Labels are cut by cell width with `…` at 80 columns too. Amend the 80-column literals in the examples to the cut form.
- **RB-4 (F3): rewrite AT-4653's 80x24 fold clause** to the behaviour the fitted frame can actually show. Use the fold that exists, and record it in one ledger entry naming AT-4653.
- **RB-5 (F4): the dependency gutter is blank on the milestone row,** the same as MR-a's LLR-4601.8. Add one LLR, or cite LLR-4601.8 as the governing rule.
- **RB-6 (F7): the deck's negative control must be able to fail.** The mutant draws the shared row into the `x` deck, and the byte check against the `8ca174c` copy turns RED.
- **Corrections.** The design corrections for RB-2..RB-6 are made in ONE pass AFTER E3 round 1, together with the reviewers' findings. E3 reviews the graph and these rulings as the intended design.
