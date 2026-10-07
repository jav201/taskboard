# CHUNK — DeepSeek V4 Pro — increment 002 of batch 2026-10-07-batch-03 (the render items, MAIN checkout)

You implement increment 002 of the cleanup batch in `C:/Users/jjgh8/Github/taskboard`: the four
render items of HLR-903/LLR-903.1. The TESTS already exist — `tests/test_cleanup.py` — with
4 RED arms (the counterfactual): arm 1's fold half (the `?` legend must name `◆` only for
DRAWN bands), arm 2 (D-623: a milestones-only project draws its rule-only band with `◆`, the
head reading `N open`), arm 3 (UX2-2: a late milestone below the fold marks the fold row
`▾ N more · ▲1 ◆`), arm 4 (lanes/agenda/focus render milestone rows carrying `◆`, marker only —
no layout change to non-milestone rows; the swimlanes `?` legend names the milestone `◆`).

## YOUR FILE: `taskboard/views.py` ONLY. No tests. No git.

## THE WORK (read the contract first: .dev-flow/2026-10-07-batch-03/01-requirements.md
## HLR-903 + LLR-903.1 with LED .2's arm definitions)

1. **K2-1 fold half**: `legend_entries("kanban")` (:6490) checks all `plan.bands`; the fold is
   computed in `_kanban_grouped` (:5050-5067). Expose ONE shared drawn-band computation (a small
   helper both the renderer and the legend call — CL-7) so the `◆` legend entry appears only
   when a DRAWN band carries a milestone.
2. **D-623**: the band-rule facts (`_band_facts` / `band_rule_facts`, :4833-4933) and the
   band-exists test (`kanban_plan`'s drop test, :4675): admit a project whose only open items
   are milestones — its band draws the rule-only head (`N open` counting the milestones) and
   carries them. A project with no cards, no done, no visible milestones still draws none.
3. **UX2-2**: the fold row (`▾ N more` seat): when a late milestone (due before today, per
   `milestone_tone`) sits below the fold, mark `▾ N more · ▲1 ◆` (the BACKLOG's shape).
4. **Milestones in lanes/agenda/focus**: the three renderers' milestone rows carry `◆` —
   a marker beside the title (lanes/focus) and on the day's dot (agenda), marker only.

## DISCIPLINE
- Run: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_cleanup.py -q` → all green; then the FULL suite → 0 failures other than the declared G-011 flake (the census may redden if a legend/band line moves — name any such test in your report, do not fix tests).
- English comments, shipped voice. Match the C-2b budget (accent = focus only).

## REPORT BACK
Per item: what changed (file:line), the suite counts, any census test your change reddens.
