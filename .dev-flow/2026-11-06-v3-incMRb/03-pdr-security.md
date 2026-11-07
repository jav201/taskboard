VERDICT: PASS-WITH-NOTES

# Security Review — Inc MR-b, the presentation's milestones share one row (PDR, E3, code-free)

> security-reviewer, 2026-11-06. Read-only review of the Code-Wire design at `fe8ecb8`, with RB-1..RB-6 as the
> intended design. I edited no product file.
> Counts: HIGH 0 · MEDIUM 1 · LOW 2. **Nothing blocks.** Every mitigation below is `planned`.

## Scope reviewed

- `.dev-flow/2026-11-06-v3-incMRb/`: 01-requirements.md, 00-e1-rulings.md, graph-interfaces.cw.md,
  graph-proto-V.cw.md, graph-proto-S.cw.md, e2-seams.md, baseline-notes.md (P-9, B-3).
- MR-a: `03-pdr-security.md`, `03-pdr-security-r2.md`, `05-review-security.md` (SEC-1..SEC-9).
- Current code, read-only: `views.py` `c`, `fit`, `_literal`, `clip`, `_strip`, `_pad`, `to_text`,
  `_lane_marks`, `gantt_milestone_row`, `gantt_lane_label`, `_gantt_field`, `present_tasks_m`,
  `_present_field`, `_present_heading`, `_present_brief`, `_present_finish`, `render_present`,
  `present_deck_boards`, `_all_plan`, `_all_layout`, `_all_timeline`; `app.py` `_shown_ids`, `_hide_all`,
  `action_export`.
- Probes (`.scratch/`, `python -I`, deleted afterwards), both through the real seat `to_text`
  (`collapse_runs` → `Text.from_markup(…, emoji=False)`):
  - **P-a, current frames:** 10 hostile milestone titles as the cursor, views 1/2/3 at 118x30 and 80x24, 60 renders.
  - **P-b, the designed row:** `_present_lane_row` and the 3-branch `_present_field` composed exactly as
    graph-proto-V says, over MR-a's shipped `gantt_milestone_row` / `gantt_lane_label`. 13 hostile titles
    (incl. `[@click=app.quit]x`, `[link=file:///…]`, `x\`, `a\[b]`, a 300-char title, a 0-cell title) ×
    5 dues × 3 classes × widths 118/100/93 (view 3 beside the rail)/80 × 3 cursors = **2340 rows**.

## Checked, no finding

| Check | Result | Evidence (`executed` on the probe; `planned` for E4) |
|---|---|---|
| 1. Labels reach Textual escaped (row) | ✓ | P-b: 2340/2340 rows at exact width, 0 exceptions, 0 spans with meta or link, titles literal (e.g. ` ⟦▎ ■ [@click=app.…` at 80). The row adds no escape of its own: field labels come only from `gantt_milestone_row.put_label` (`fit` → `_literal` once → `run:<tone>` + `""`), and the label column only from `gantt_lane_label` (`title_markup`). The graph's `run:` branch matches the tone MR-a ships (SEC-9 closed). `◆N`, `▲L`, `i/N`, `Mon D`, `▲Nd` and the chip are app text; glyphs and `rev:<style>` come from allowlisted classes (`marks.py` `SHAPES`). |
| 2. Hidden items not drawn or reachable | ✓ | `present_stop_order` only reorders `present_tasks_m(…)[0]` (shown, open, hidden classes out). MR-a's units read only `lane` for membership and counts; `board` is read only for the class lookup (`milestone_mark`). P-b: Review hidden + tm4 `show_in_present` false → lane `[tm5]`, label `◆ 1 milestone`. S steps over `_shown_ids` (same source) and view 3 over `_all_layout` stops (same plan). `space` hides by the stop's id (`_hide_all`), so one milestone alone. |
| 3. The `x` deck gets no new data | ✓ | `present_deck_boards` is unchanged and reads `present_tasks_m(…)[1]` in board order. `action_export` calls nothing the slice changes, and S changes only `_shown_ids`. RB-6 gives the NC a way to fail. |
| 4. No line wider than the terminal | ✓ (row) | Design arithmetic: label `label_w` (` `+lead+`▎`+`gantt_lane_label` at `label_w − 3`) + gutter 1 + field `field_w` + chip `chip_w + 1` = width. P-b holds it at 118/100/93/80. The one over-wide line at base is the view-1 brief, which is SEC-B1. |

## Findings

### SEC-B1 — RB-2 must fix `_present_brief` with `_literal`; measuring alone would not fix it  [Severity: MEDIUM]
- **What:** P-a reproduces P-9: a title `\` or `x\` as the cursor makes the view-1 brief line 119 / 81 cells
  (4/60 renders; all other lines exact). Cause: the brief puts `c(escape(txt), accent, bold)` next to the
  same-style `⟧`. `collapse_runs` merges the two runs, so the tag that `escape`'s trailing `\\` relied on is
  gone and both backslashes print. `_pad` and `_present_finish` measure the markup before the merge (`_strip`),
  so they see the right width.
- **Where:** `views.py` `_present_brief` (`c(escape(txt), …)`); the seat `to_text` → `collapse_runs`.
- **Why it matters:** RB-2 offers "measure the width on the rendered text" as an alternative fix. That would
  only detect or pad the line. The audience would still read `x\\`, and the line would still wrap.
  `_literal` closes a trailing backslash run with its own tag, which survives the merge. The P-a piece probe
  showed that, and so did MR-a's 154 renders.
- **Recommendation:** take RB-2's `_literal` option: `escape(txt)` → `_literal(txt)`, cut first with `clip`,
  as now. Reject the measure-only option.
- **State:** `planned`.

### SEC-B2 — The RB-2 regression test must measure the rendered frame, not the markup  [Severity: LOW]
- **What:** `_present_finish`'s assert and `_pad` measure with `_strip`. The merge happens downstream in
  `to_text`. A regression test that measures with `_strip` (or the assert alone) passes on base. Its RED is
  then vacuous.
- **Where:** RB-2's regression test; LLR-4652.6 / LLR-4652.7 / AT-4655 measurements.
- **Recommendation:** measure `cell_len` per line of `render_present(…).plain` (after `to_text`). Use the
  titles `\` and `x\`, the cursor on them, view 1 at 80 and 118. Prove it RED on base (119 / 81, P-a).
- **State:** `planned`.

### SEC-B3 — `escape` on cut titles still drops a backslash before a non-tag `[` in briefs and view-2 headings  [Severity: LOW]
- **What:** P-a piece probe: `escape("review ab\[…")` prints `review ab[…`. `escape("\[…")` prints `[…`.
  `_strip` agrees with the wrong text, so the width is kept and nothing is injected. The audience reads a
  title that differs from the board. SEC-B1's `_literal` fixes this in view 1. `_present_heading` (the view-2
  blocks, `escape(clip(task.title, tw))`) keeps it. That unit is outside the 10-unit slice.
- **Where:** `views.py` `_present_heading`.
- **Recommendation:** make the same one-line `_literal` swap there (an 11th unit, same file). If the
  orchestrator prefers to keep the slice, record it in the backlog. Add `a\[b]`-style titles to AT-4655.
- **State:** `planned`.

## Verdict

- [x] **PASS-WITH-NOTES.** No HIGH finding. The new row's escape and width hold on the real seat, by design
  and on the probe. Hidden items stay unreachable, and the deck gets no new data. SEC-B1 should be settled in
  the E3 correction pass (RB-2's wording). SEC-B2 and SEC-B3 are notes for E4.
- This is a design clearance only. The row's evidence stays `planned` until E4 runs TC-4916 / AT-4655
  through `to_text`. It authorises no merge or deploy, and it is not the operator's approval.

## Evidence checklist

- [x] Each finding has what · where · why · recommendation (SEC-B1..SEC-B3).
- [x] Each finding has a severity: 1 MEDIUM, 2 LOW.
- [x] No secret values appear in this report. The increment touches no secret.
- [x] The verdict is explicit: PASS-WITH-NOTES, with no HIGH open.
- [x] New tool or integration: none. No new I/O, network or dependency (01-requirements §1). The deck path is unchanged.
