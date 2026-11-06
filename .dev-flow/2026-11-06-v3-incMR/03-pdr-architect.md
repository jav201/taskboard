# E3 PDR — architect — Inc MR-a (board gantt milestone row)

> Reviewer: architect (Opus), read-only. Tree: `ms-row-proto` at `02b4a87`. Read: `01-requirements.md`, its
> ledger, `00-e1-rulings.md` (R-1..R-5), `graph-baseline`, `graph-interfaces`, `graph-proto-V`, `graph-proto-S`,
> `e2-seams.md`, `e2-trace.txt`, `baseline-notes.md`, the commission, and the source by range
> (`views.py` 2309-2550, 2551-2770, 2877-2895, 3141-3160, 3259-3490, 8420-8432; `app.py` 3279-3290,
> 3417-3455, 3523-3540; `prototypes/milestone_row/proto.py` 207-270). Nothing was run: every check below is
> `executed` as a read, and every test claim is `not-run`.

**Verdict: FAIL.** 5 MAJOR, 7 MINOR. Every fix is a targeted edit to a requirement, a threshold or a graph
node; no fix adds a source file or changes a seam's shape. A re-review needs only the amended rows.

## 1. Rulings proposed on the E2 findings F-1..F-5

### F-1 — MAJOR — a shared cell's label, and "day" against "cell"
- **Seen:** LLR-4603.3 excludes "part of a shared cell" from dating, but its threshold and AT-4601 read
  `■2 Oct 24`, and so does the oracle: `proto.py:249-255` labels every bucket by its `lead`.
- **Wider than E2 said:** `GanttAxis` has `k` days per cell, and `k` is a float fitted to the window
  (`views.py:2310-2321`). On a long board (`k > 1`), two milestones on different days share a cell. The oracle
  buckets by cell (`proto.py:214-217`), and so does LLR-4602.2. But LLR-4603.7's ` i/N` counts "milestones on
  its day", and the commission and the walk talk about "same-day". At `k > 1`, `■2` can sit beside a label
  column that reads `1/1`.
- **Fix (statement edits, ledger entry LED .4):**
  - LLR-4603.3 becomes: *"The milestone row shall draw, beside each mark that holds no selected milestone and
    whose lead is not late, the lead's date `Mon D`, past one blank cell, only where the whole date fits
    without touching another mark or label."*
  - LLR-4603.4 becomes "a mark whose lead is late".
  - Define **lead** in §1: the selected member of the cell, else the first in walk order. Walk order sorts by
    due first, so the lead's date is the cell's earliest.
  - LLR-4603.7: change "of N milestones on its day" to "of N milestones in its cell".
  - Keep the rest of the threshold. Removing the shared-cell date is not an option, because it would contradict
    the capture the operator approved.

### F-2 — MAJOR — the colour of h1
- **Seen:** `milestone_mark` gives an unclassed milestone `◆` in `mut` (`views.py:2600-2602`). That is the seat
  for every mark (LLR-2604.1). The "project hue" is `milestone_tone` (`views.py:2567`), which has no caller in
  `views.py`: it is dead.
- **Fix:** in the LLR-4602.1 threshold, replace "h1 `◆` in its project hue" with "h1 `◆` in `mut` (the seat)".
  Do not revive `milestone_tone`: a second colour channel outside the seat is a feature to remove, not to guard.

### F-3 — MAJOR — `▸` for an open milestone cannot be reached
- **Seen:** `gantt_window` puts `hi` at `max(open dues, project dues, today) + margin` (`views.py:2518-2533`).
  So no open due ever falls to the right. A REACHED milestone that was done early, with a due past `hi`, does
  fall to the right, and it is drawn while its group has open work (D-606).
- **Fix:** rewrite the LLR-4602.6 threshold and AT-4607 with *"a reached milestone due 90 days ahead, in a group
  with open work"*. Drop the open-milestone case: TC-4816 through a hand-built `GanttAxis` would test a route
  that no product code calls, which makes it **partial** under the E4 rule.
- **Geometry correction:** a reached mark is 2 cells. `gantt_milestone_cells` puts it at
  `x = w - 1 - len(marks)` (`views.py:2731-2733`), so the threshold reads `<hollow>✓▸` in the last three cells,
  not `<glyph>▸` in two.
- **Gap the rule leaves:** the graph does not say where an off-window member is bucketed. Bucket by the cell it
  is DRAWN in, which is clamped next to the edge. Two off-window members on one side then read `<glyph>2▸`, and
  never draw two marks on one cell.
- **Fixture caveat:** the left case (`◂`, 40 days back) must fall before `ctx`, the earliest open start that the
  spare cells may show (`views.py:2533`). The tester checks MR-F's start dates.

### F-4 — MINOR — the slice is 9 units, not 6 or 8
- **Accepted:** `gantt_lane` (new) and `_gantt_field` (one `rev:` branch). The alternative, a static
  `sel-<colour>` table in `HEX`, registers N keys for one use, which is speculative.
- **Missed by both counts:** `nav_model`'s gantt branch changes behaviour (R-4: `_hide` before the plan,
  graph-proto-V `nav_model`), so it is a changed unit, not a call-site edit.
- **Fix:** amend §6 by ledger entry to **9 units in 2 source files** (3 new, 6 changed). This is within the
  file budget.

### F-5 — MAJOR — the dependency gutter goes blank, and no requirement says so
- **Seen:** base draws `gantt_dep_mark` in each milestone row's gutter, and that call adds `waits` or `early` to
  `drawn` (`views.py:3384-3386`). On a shared row, one cell cannot name which of N marks waits. Critical-chain
  membership shows for a milestone only through that bold `↳` (`views.py:2561-2563`).
- **Fix (remove, do not guard):** keep the gutter blank and state it as a new LLR, **LLR-4601.8** (Ubiquitous; TC-4808 — not LLR-4603.11, whose TC-4831 would collide with LLR-4604.1's):
  *"The milestone row's dependency gutter shall be blank."* NC: draw the stop's `↳` → RED.
  - The legend follows on its own, because it asks the frame what it drew (LLR-102.5).
  - The wait stays visible in details, in the link mode (R-3) and in the chain map.
  - The LLR count becomes 41, which is still "about 40".
  - Re-baseline any test that expects `↳` on a board-gantt milestone row (`tests/test_gantt_board.py:180-198`,
    `tests/test_gantt.py:610-617`, to be checked case by case).
  - List this loss in the batch's review packet as an accepted change in behaviour.
- **Rejected:** "show the stop's `↳`" adds a mark whose referent changes as you walk the row.

## 2. Further findings

### N-1 — MAJOR — a title drawn into field cells breaks the markup and the width law
- **Seen:** `_gantt_field` paints each cell as `c(glyph, tone)`, and `c` does not escape (`views.py:75-78`,
  `:2888`). Dates are safe ASCII. The selected title in the field (LLR-4603.1, LLR-4603.2) is board text, laid
  out one character per cell, as in the oracle's `put` (`proto.py:242-245`).
  - **Backslash:** a title ending in `\` (a TC-610 case, `tests/test_gantt_milestones.py:186`) escapes its own
    cell's `[/]`. The frame then prints a literal `[/]` and leaves the style open, which is a regression of
    S-1.
  - **Wide characters:** a CJK or emoji character takes 2 columns but only 1 cell, so the line grows wider than
    the terminal (against LLR-4603.9).
- **Fix (no new unit):**
  - `gantt_milestone_row` cuts the title with `fit()`, which is aware of cell widths.
  - It puts the label into ONE cell as `_literal(piece)`, then fills the next `cell_len(piece) - 1` cells with
    the glyph `""`. `c("", tone)` paints nothing.
  - The room checks measure with `cell_len`, not `len`.
  - Add to TC-4821 and TC-4822 the three titles of TC-610 plus one CJK title, asserting `txt.plain` and the
    width of every line.
- **Alternative for the orchestrator:** drop the title from the field. The label column already shows the
  selected title (LLR-4603.7), so LLR-4603.1 and LLR-4603.2 would go. But the commission's design fact says
  "the selected milestone shows its full title", and the label column cuts the title, so removing it needs the
  operator's word.

### N-2 — MINOR — AT-4606 disagrees with LLR-4606.1
AT-4606 says "one row per open milestone". LLR-4606.1 and TC-4851 say m1..m5 on 5 rows, with the reached m1
kept, as base does. **Fix:** AT-4606 reads "one row per drawn milestone (m1..m5), byte-equal to base".

### N-3 — MINOR — a hidden or filtered selection is a failure path with no LLR
The E1 inventory listed it (`00-e1-rulings.md` §1, "the selected milestone filtered out"), but the 40 LLRs do
not cover it.
- **Seen:** after R-4, a selected milestone whose class is then hidden is in no nav column, so the next `↑↓`
  runs `_select_first` (`app.py:3428-3432`). `action_hmove` does the same, because `gantt_lane` returns `()`.
  This is base's behaviour for a selection that cannot be located, and it is correct.
- **Fix:** an E4 addendum, a TC: hide the class of the selected m3, press `↑` → base `_select_first`, with 0
  exceptions. No new behaviour.

### N-4 — MINOR — §6 under-lists the tests that pin rows
- **Seen:** §6 names 6 files. `baseline-notes.md` §C tags `g`/`g2` tests in other files too: `test_cascade_app`,
  `test_legend`, `test_marks_manager`, `test_milestones`, `test_milestone_offer`, `test_boards`,
  `test_boards_home` and `test_people_search`. A group with ONE milestone changes as well: its title leaves the
  label column unless the milestone is selected, and the column reads `◆ 1 milestone`.
- **Fix:** E4 takes the re-baseline list from the instrumented run's `g` tags (§A, §B with `M`, §C `g`/`g2`),
  not from §6. Each changed assertion cites the LLR that moves it.
- **Presentation guard:** every test tagged ONLY `p` must stay byte-identical in MR-a. A `p`-only test that
  turns RED is a regression of the "presentation unchanged" scope, not a re-baseline.

### N-5 — MINOR — the class filter is applied in three places
- **Seen:** R-4 adds `_hide` to `nav_model`. `gantt_lane` applies it again, and `_gantt_frame` already does.
  P-10 was exactly one of three call sites forgetting it.
- **Fix:** apply the class filter inside `gantt_plan` when `done_rows`, which its docstring calls "THE ONE SEAT
  for what the gantt draws".
  - `_hide` keeps the same `Task` objects, so `_notify_folded`'s `is` test (`app.py:3534`) still holds, and
    hiding twice changes nothing.
  - `nav_model` and `gantt_lane` then need no filter of their own.
  - This is not a new unit. SEAM-4 and SEAM-3 keep their contracts.

### N-6 — MINOR — SEAM-7 promises too much to MR-b
`gantt_lane_label` is frozen as an interface that MR-b "reuses unchanged". The presentation's label column has
its own form (`▎ ◆ title`, briefs), and R-2 gives it a different cursor model. **Fix:**
- Freeze only `gantt_milestone_row`, whose cells take a generic axis and a lane passed in by the caller, as
  MR-b's interface.
- Leave `gantt_lane_label` as a V-internal unit that MR-b may adopt.
- Add one invariant for MR-b: the board gantt's frames stay byte-equal.

### N-7 — MINOR — tones left unspecified
- The count digit and `+` beside a selected glyph: the oracle uses `bright` when selected, else the class style
  (`proto.py:225`).
- The selected title in the field: the oracle uses `bright`.
- The selected title in the label column: say `title_markup(t, w, selected=True)`, so it wears the selection cue
  that every other row wears (`views.py:281-287`).

**Fix:** write these three into the `gantt_milestone_row` and `gantt_lane_label` funcs as E4 addenda.

## 3. Checks that passed (with the evidence read)

- **Cursor model.**
  - `action_cursor` is unchanged (`app.py:3417-3437`). It locates the selection in a column built with that
    selection, so a walked member is the stop and can be located.
  - `↑↓` from a task lands on the stop chosen with the task selected, which is the anchor.
  - The fold budget counts `len(rows)` (`views.py:2489-2511`). Walking `←→` swaps the stop but not the row
    count, so the folds never move while the user walks the row.
  - Re-entering the row re-anchors and does not resume, which matches "stop once, at the next open milestone".
  - The D8 branch's `sel in groups[sel_g].rows` (`views.py:3415`) and the pager's `ids.index(selected_id)`
    (`:3460`) both hold, because the selected member IS the stop.
  - Status: `executed`, by reading.
- **R-4 filtered nav.**
  - The defect is real: `nav_model`'s gantt branch takes the board as it comes (`views.py:8425-8430`), while
    `_gantt_frame` hides classes first.
  - The fix as designed is correct, and N-5 makes it structural.
  - `_notify_folded` and `gantt_link_order` keep the flag off (`app.py:3531`, `views.py:8889`), as SEAM-6
    states.
- **Presentation unchanged.**
  - `gantt_milestone_cells` and the presentation path are untouched.
  - The `rev:` branch in `_gantt_field` is inert for any tone without `rev:`.
  - MR-b's dependency is limited by N-6.
- **Link mode (R-3).** Flag off means base rows. `line_map` maps every lane id to the shared line (SEAM-9) only
  under the flag. `GanttLinkMode` reads `selected_task_id`, so the walked member becomes the waiter
  (LLR-4606.2).
- **Pages.** TC-4854's `▼ 13 below` = 21 rows − page 8, consistent with `views.py:3456-3477`. The exact body of
  10 rows at 118x14 is `not-run`; the tester confirms it.

## 4. PDR §A checklist (`templates/design-review-template.md`)

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Proposal complete | ⚠ | graph + seams + trace complete; F-1, F-2, F-3, F-5 and N-1 open; alternatives: `n/a — R-1/R-3 rule the real decisions` |
| 2 | Respects `docs/ARCHITECTURE.md` | ✓ | 2 files, no new dependency, no new key; `gantt_plan` stays the one seat (N-5 strengthens it) |
| 3 | Every output has a named consumer | ✓ | `e2-seams.md` SEAM-1..9 |
| 4 | Every requirement has foreseen coverage | ✓ | `e2-trace.txt` 47/47; the new LLR-4601.8 (F-5) maps to the free TC-4808 |
| 5 | Test cases observable and non-vacuous | ⚠ | NCs named per LLR; F-3's open `▸` case would be partial; N-1 adds the hostile and wide titles |
| 6 | Gauntlet controls declared | ✓ | commission: law guards at E5, WT captures, `env -u NO_COLOR` |
| 7 | Frozen interfaces listed | ⚠ | `graph-interfaces.cw.md`; N-6 narrows what MR-b inherits |
| 8 | Lane plan disjoint | ✓ | V = `views.py`, S = `app.py`; cross-group ATs have one tester |
| 9 | UX lens | n/a — ux-reviewer's lens, not this file |
| 10 | Security lens | ⚠ | N-1 is S-1 territory; the security reviewer rules on it |

**Verdict: FAIL**, which is the template's `rejected` for this round. To reach PASS-WITH-NOTES, close F-1, F-2,
F-3, F-5 and N-1 by targeted edits (statements, thresholds, AT-4607, LLR-4601.8, ledger LED .4). F-4 and
N-2..N-7 can then ride to E4 as addenda.
