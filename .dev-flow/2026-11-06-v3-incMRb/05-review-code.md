# E5 — Code review — Inc MR-b (the presentation's milestones share one row)

**Reviewer:** code-reviewer (it also covers the security lens; security findings are tagged `SEC-`).
**Scope:** `git diff 8ca174c 5a6a906 -- taskboard/` (`views.py` +103/−42, `app.py` +4/−3), read in full. Also read: the test diffs `tests/test_milestone_marks.py` and `tests/test_present_all.py`, TC-4918..4920 in `tests/test_present_milestone_row.py`, and the design (`01-requirements.md` §4.2, `00-e1-rulings.md`, `e3-addenda.md`, `e4-deviations.md`, `e4-integration.md`, `graph-proto-V.cw.md`).
**Method:** read-only. The probes ran in `.scratch/` against head and against a `git archive 8ca174c` copy (`taskboard.__file__` printed for each). The scratch was deleted afterwards.

## Verdict

**PASS-WITH-NOTES.** 0 HIGH, 1 MEDIUM, 2 LOW (1 of them `SEC-`). Nothing blocks. The MEDIUM is a record defect in LLR-4652.9's threshold; the code and the test are right.

## Checks

| # | Check | State | Evidence |
|---|---|---|---|
| C1 | The code implements the graph, with no silent divergence | `executed` ✓ | Each of the 12 units matches `graph-proto-V.cw.md`. `_present_lane_row` (`views.py:7499-7520`): label ` `+lead+`▎`+`gantt_lane_label(…, label_w - 3)`, blank gutter (LLR-4651.8), field `_present_field(gantt_milestone_row(…))`, chip = the `sel` member's, else the first due ≥ today, else blanks. `render_present` (`:7637-7676`): `stops`/`lane`, cursor fallback `stops[0]`, task rows over `stops[len(lane):]`, briefs and blocks over `stops` (B-7). The note room keeps `len(open_t)`, as the graph says. `_all_layout`/`_all_timeline` (`:7847-7955`): the milestone stops share one row and the cost is 1. `_present_task_row`'s milestone branch is removed (B-5). D-1 and J-1 are recorded, not silent. |
| C2 | MR-a's units are reused, not duplicated; MR-a's board gantt is unchanged | `executed` ✓ | `gantt_milestone_row`, `gantt_lane_label` and `_lane_marks` are called unchanged. `milestone_walk_key` (`:2435`) is a verbatim lift of the nested `walk_key`, and `gantt_plan` has its one use (`:2515`). Probe: `repr(gantt_plan(MR-F, …))` sha256 is equal on head and base for 4 selections × 2 heights. `_present_field`'s three tone branches repeat `_gantt_field`'s (`:3158-3166`) on purpose (SEAM-8). The functions already differed at base (the today rule), so this is not a finding. |
| C3 | The milestone marks go through the `milestone_mark` seat | `executed` ✓ | `_present_lane_row` draws no glyph of its own. Its marks come from `gantt_milestone_row` and `gantt_lane_label`, and both call `milestone_mark(` (`:2993`, `:3024`, `:3031`). `_present_task_row` no longer calls the seat or `gantt_milestone_cells`. J-1's census assertion pins both. |
| C4 | The stop order (RB-1) is the same in views 1, 2 and 3 | `executed` ✓ | There is one source, `present_stop_order` (`:6975`). It feeds `render_present` (field, briefs, blocks, cursor fallback), `PresentScreen._shown_ids` (`app.py:404`, cursor movement) and `_all_plan` (`:7754`), and `_all_layout` emits the stops in that order. `_cursor` (`app.py:407`) uses `ids[0]`, which is the renderer's `stops[0]`. |
| C5 | R-7 escaping on every presentation title label, probed on the real render | `executed` ✓ | Titles `a]b[/]`, `[@click=app.quit]x`, `x\`, `\`, `\[x`, `a\[b]`, `日本語のタイトル`, `ab\[`+60 `x`. Each is the cursor task, as a milestone and as a plain task, in views 1, 2, 3, at 118x30 and 80x24 (96 frames). The result: 0 exceptions, every line `cell_len` == width (view 3: `timeline_w`), the text literal in `.plain` after `to_text`, each backslash once, and the click tag printed as text. Base on the same probe: the brief for `\` and `x\` is 119/81 cells and reads `\\`; the brief and block for `\[x` read `[x`; and `ab\[x…` reads `ab[x…`. |
| C6 | The `x` deck is unchanged | `executed` ✓ | `present_deck_boards`, `present_tasks_m` and `report_deck` are untouched. Probe: the deck's sha256 for views 1/2/3 on MR-F is equal on head and base (`16fc6e72…`, `16fc6e72…`, `a825967d…`). |
| C7 | The tests encode WHY | `executed` ✓ | TC-4919 and TC-4920 name the defect, the RED-on-base reading and both NCs. The TC-2103, AT-2103, AT-2104 and overflow re-baselines each cite the LLR that moves them, and they keep pinning the rail, the header and ruler, the order of the non-milestone rows, and the per-project milestone count. J-1's chain assertion is stricter than the old entry. See F2 for one nit. |
| C8 | The open question: is LLR-4652.9's "RED on base" claim wrong? | `executed` | See F1. |

## Findings

### F1 — LLR-4652.9's threshold misstates base for `a\[b]`, and its count is stale  [MEDIUM · `design-gap` · `executed`]
- **What:** The threshold says *"RED on base: `\` and `x\` give a 119 / 81-cell line reading `\\`, and `a\[b]` reads `a[b]`"*, over 3 titles, 6/6.
- **Probe on `8ca174c` (the answer to the open question):** a title ending in `\` **was really defective on base**. The view-1 brief is 119 cells at 118 and 81 at 80, and it reads `⟦\\`. This holds for `\` and `x\`, as a task and as a milestone. That half of the claim is TRUE, and RB-2's regression is genuine. The other half is FALSE: `a\[b]` reads `a\[b]` on base, because rich's `escape` escapes the tag-shaped `[b]`. This is the same mistake LED-.10 corrected in LLR-4652.10. The real non-tag RED case is `\[x` (base: `⟦[x`). TC-4919 already carries `\[x` and runs 4 titles × 2 sizes = 8 cases. Its docstring records the discrepancy, but the requirement still says 3 titles, 6/6.
- **Where:** `01-requirements.md:135-136`; `tests/test_present_milestone_row.py:460`.
- **Why it matters:** The canon states a false RED-on-base fact and a count that differs from its test. This is the trace defect J-2 already fixed once.
- **Suggested fix:** Amend LLR-4652.9 the way LED-.10 amended LLR-4652.10. Titles `\`, `x\`, `\[x` are RED on base; `a\[b]` is kept as a positive case; the threshold becomes 8/8. Add one ledger entry. The requirement and test change; no code changes.

### F2 — J-1's census assertion has a collapsed line continuation and stale line labels  [LOW · `impl` · `executed`]
- **What:** `assert lane_row is not None and "gantt_milestone_row(" in lane_row         and "gantt_lane_label(" …` is one 140-character line with an embedded space run, apparently a lost `\`+newline. The two new `SEAT_SITES` entries reuse the old `":6537-6547"` label, which no longer points at these units.
- **Where:** `tests/test_milestone_marks.py` (the J-1 assertion after `:283`; entries `:157-158`).
- **Why it matters:** Readability and the line-length convention only. The logic is right.
- **Suggested fix:** Split the line with parentheses. Relabel the entries `":7499 presentation milestone row field/label"` or drop the line reference.

### SEC-F3 — a project name holding `\[` drops its backslash in the presentation's header, span label and view-3 head (pre-existing)  [LOW · `design-gap` · `executed`]
- **What:** The `escape(fit(proj.name…))` / `escape(proj.name)` sites (`views.py:7494`, `:7646`, `:7790`, `:7969`) are outside this slice. Probe: a project named `\[x`, in views 1/2/3 at 118 and 80, prints `[x`. The same happens on base. A name ending in `\` keeps exact width and reads literally, and no live tag forms.
- **Why it matters:** It is the class of defect LLR-4652.10 fixed for task titles, on a label this increment does not own. Text is misrendered, but the frame cannot be injected or overflowed. B-1 says to report such a site and not fix it.
- **Suggested fix:** Backlog it: route the project-name labels through `_literal` in a later increment, with a regression on `\[x`. No action in MR-b.

## Evidence checklist

- ✓ Diff read in full: `views.py` hunks at `:2435`, `:2495-2515`, `:6972-6983`, `:7034-7056`, `:7423`, `:7496-7527`, `:7576`, `:7634-7676`, `:7749-7755`, `:7846-7887`, `:7947-7955`; `app.py:57-61`, `:399-404`.
- ✓ Correctness pass: empty `open_t` (`lane` is empty, so no lane row is drawn and the cursor is None), a cursor that is not in the lane (`sel` None), an all-past lane (blank chip), folded projects (`cost` = 1), and the view-3 cursor on a project head (`sel` None).
- ✓ Simplicity pass: no new abstraction beyond the two seams the graph names.
- ✓ Reuse checked: MR-a's units are called, not copied (C2).
- ✓ Tests reviewed for intent (C7, F2).
- ✓ Verdict explicit: PASS-WITH-NOTES. There is no HIGH, so none needs applied-and-verified evidence.

## Independent review cell (§4b)

`code-reviewer` · PASS-WITH-NOTES · no HIGH. F1 (MEDIUM, design-gap) routes to the corrective pass as an LLR-4652.9 amendment and a ledger entry. F2 is LOW; it goes to the corrective pass or the backlog. SEC-F3 is LOW and goes to the backlog (pre-existing, outside the slice).
