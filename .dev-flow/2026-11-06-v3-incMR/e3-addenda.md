# E3 addenda — Inc MR-a — instructions to E4 (ruling R-8)

These are E4 instructions from the E3 round-1 findings that R-8 adopts as proposed. Design changes are in the
requirements (LED-2026-11-06-incMR.4, .5, .6) and the graphs; this file holds only what E4 must do or check.
Sources: `03-pdr-architect.md` (F-3, F-5, N-3, N-4, N-5, N-7) and `03-pdr-security.md` (SEC-1, SEC-2, SEC-3, SEC-5).

| # | From | Owner | Instruction |
|---|---|---|---|
| A-1 | F-3 | V tester | TC-4816 and AT-4607 go through `render_gantt` with no hand-built `GanttAxis`; a case through an axis no product route builds is **partial**. The `◂` case (40 days back) must fall before `ctx`, the earliest open start the spare cells may show (`views.py:2533`): check MR-F's start dates before you fix the fixture. |
| A-2 | SEC-3 | V tester | TC-4818 (LLR-4602.8) also goes through `render_gantt`: a reached milestone whose due is the window's last day (`hi`). If no product route puts a two-cell mark at `w-1`, record that as a deviation and do not hand-build the axis. |
| A-3 | F-5 | integrator | Re-baseline, one case at a time, every test that expects `↳` on a board-gantt milestone row (start with `tests/test_gantt_board.py:180-198` and `tests/test_gantt.py:610-617`). Each changed assertion cites LLR-4601.8. List the lost gutter in the batch review packet as an accepted change in behaviour. The wait stays visible in details, in the link mode (R-3) and in the chain map. |
| A-4 | N-4 | integrator | Take the re-baseline list from the instrumented run's `g` tags (`baseline-notes.md` §A, §B with `M`, §C `g`/`g2`), not from `01-requirements.md` §6. This includes `test_cascade_app`, `test_legend`, `test_marks_manager`, `test_milestones`, `test_milestone_offer`, `test_boards`, `test_boards_home` and `test_people_search`, and the one-milestone group whose title leaves the label column. Each changed assertion cites the LLR that moves it. **Presentation guard:** every test tagged ONLY `p` stays byte-identical in MR-a. A `p`-only test that turns RED is a regression, not a re-baseline. |
| A-5 | N-3, SEC-5 | S tester | TC-4843d (graph-proto-S `action_cursor`): select m3, hide class Review in `#`, then assert: the selection leaves m3; `↑` falls back to base `_select_first` with 0 exceptions, and `action_hmove` does the same because `gantt_lane` gives `()`; `enter` and `]` do not act on m3; neither the label column nor the ruler echo shows m3. TC-4843b and TC-4843c start with the class already hidden, so they do not cover this path. |
| A-6 | N-5 | V implementer | The class filter has one seat: `gantt_plan` under `done_rows`. `nav_model` and `gantt_lane` add no filter of their own. `_gantt_frame` keeps its base `_hide`, which changes nothing the second time. TC-4843b (R-4) must be RED on base. |
| A-7 | N-7 | V tester | Assert the three tones written into the graph: the count digit and `+` are `bright` beside the selected glyph, else in the class style; the selected title in the field is `bright`; the selected title in the label column is `title_markup(t, w, selected=True)`. |
| A-8 | SEC-1 (R-7) | V tester | TC-4820 goes through the real seat (`collapse_runs` then `Text.from_markup(…, emoji=False)`), never a bare `c()` string. Check `Text.spans` for `@click` or any meta. Include a case where the title run sits next to a cell of the same tone (the `bright` count digit), so `collapse_runs` joins them. Test the escaped run joined with its neighbours, not only on its own. |
| A-9 | SEC-1 (R-7) | V implementer | Follow the LABEL PATH in `graph-interfaces.cw.md` `gantt_milestone_row` in order: cells, `fit`, `_literal`, then lay the run. Amend `_gantt_field`'s docstring invariant ("every cell here is a constant glyph") to name the escaped label run. Register no HEX key at run time. |
| A-10 | SEC-2 | V tester | The wide-glyph and combining-mark titles that SEC-2 asked of TC-4829 are covered by TC-4820 (LLR-4603.11, 15 cases). TC-4829 keeps its MR-F frames. |
| A-11 | SEC-1 | orchestrator | The SEC-1 block lifts only after the security reviewer re-verifies the amended graph (LABEL PATH, `[Data: field label run]`, SEAM-8) and TC-4820's design in E3 round 2. |

## E3 round-2 addenda (orchestrator, 2026-11-06). Binding on E4.

E3 closed PASS-WITH-NOTES from both reviewers: the architect (`d603b53`) and security (`cbc14a8`). Each minor finding below is an E4 instruction.

- **N-8.** A two-cell mark never overwrites a neighbouring mark's cell. A clash resolves to the `◆N` rule.
- **N-9.** A label run does not inherit its first cell's weekend shading. The label carries its own style.
- **N-10.** Apply the architect's two threshold-wording and fixture fixes, as `03-pdr-architect-r2.md` states them.
- **SEC-6.** A 0-cell label (no room) leaves the row at exactly the field width. Pad, and never fall short.
- **SEC-7.** TC-4820 includes titles long enough to hit the `…` cut at 80 and 118 columns.
