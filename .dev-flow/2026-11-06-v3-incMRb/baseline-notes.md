# Baseline notes — Inc MR-b, the presentation's field rows, cursor stops and view 3 layout at 2ce3943

**Counts:** 14 nodes, 7 entities, 22 edges. `codewire_lint` exit 0 (0 findings, 0 lines not read). `codewire_marks` wrote 14 marks, 0 nodes without code. `codewire_extract --path taskboard/app.py --path taskboard/views.py` exit **1**: 9 findings, all "unannotated in code" (6 parameters, 3 returns). No type mismatch, no missing node, no mark drift. 21 calls; `extract-baseline.txt` marks each one REAL or LIFTED. Lines below are at 2ce3943 (unmarked).

**Which tree is imported:** each probe puts `taskboard-wt/incMRb-marks` and its `tests/` first on `sys.path` (`python -I`), and prints `taskboard.__file__` = `…\taskboard-wt\incMRb-marks\taskboard\__init__.py` first. The marks tree is a detached worktree at 2ce3943, removed with `--force` after the run. No test was run: the facts come from the probes and the code.

**Fixture:** MR-F (`tests/milestone_row_fixture.py`, `board()`), today 2026-10-20. Ids: `ppr` *Pilot rollout*, `ppe` *Eval harness*, `ppd` *Docs & handover*; `t<key>` for tasks.

## What the code does now

- **One field row per open task, milestones included, in all three views.**
  - Views 1 and 2 share `render_present` (views.py:7566). Its loop at :7616-7617 emits one `_present_task_row` (:7475) per task of `present_tasks_m(…)[0]` (:6958), in order by due. P-2 shows 8 field rows for `ppr`, and 4 of them are milestones.
  - View 3: `_all_timeline` (:7856) emits one `_present_task_row` per open task under each unfolded head (:7892-7894).
  - Reached milestones are not open, so no view draws them (P-1: `tm1` absent). The row MR-b adds keeps that rule.
- **A milestone's field row** (`_present_task_row` :7480-7490):
  - The label is ` <lead>▎ <glyph> <title>`; the lead is `⟦` on the cursor, else a blank.
  - The gutter is `gantt_dep_mark`.
  - The field is `gantt_milestone_cells` (one task, its mark and `Mon D`). The cursor recolours the mark `accent`.
  - The chip is ` ` + `_present_chip(None, due)`, for example `due Oct 19` in `over` when the due has passed.
- **`_present_field`** (:7019) knows no `rev:`, `run:` or `""` cell. P-8 feeds it MR-a's `gantt_milestone_row(lane, "tm2", …)` on the present axis: it raises `KeyError: 'rev:violet'`. LLR-4652.2 and slice row 4 name this defect; it is real.
- **The cursor (views 1/2).**
  - The renderer takes `cursor_id` when it is open, else `open_t[0]` (:7602-7606).
  - `PresentScreen._cursor` (app.py:405) applies the same rule to `_shown_ids()` (app.py:400), which is `present_tasks_m` order.
  - `↓` from `tm2` lands on `tstore`, a task between two milestones (P-1).
  - The fallback falls on a task when a task is due before every milestone: on `ppd` it is `tha` *API reference* (P-7), not `th1`. This is LLR-4653.3's negative control, and it can be reached in MR-F.
- **The briefs (view 1) and the blocks (view 2)** follow `open_t` order.
  - View 2 splits that order at `half = (n + 1) // 2` from 100 columns (:7622).
  - P-3, `ppr`: the left column holds m2, store, m3, m4, and the right one tele, train, m5, rota.
- **View 3's layout** (`_all_layout` :7806).
  - `need` counts each unfolded project as 1 + `len(ts)`, so every milestone counts as a row. Each milestone is a stop with its own line.
  - P-4 room 15 (118x18): base folds `ppe` and `ppd`.
  - P-4 room 21 (118x24, 80x24): base folds **nothing**.
  - P-4 room 11 (80x14): base folds `ppe` and `ppd`.
- **The walk order** exists only nested in `gantt_plan` (`walk_key`, :2490). Its one caller is `gantt_plan` (:2511, the extractor's "ref" site).
- **The deck** (`present_deck_boards` :7647) reads `present_tasks_m` in board order. It reads no cursor, no fold and no stop.
- **Keys:** `PRESENT_KEYS` (keymap.py) holds `move(±1)` on `↑↓`, `side(±1)` on `←→` and `hide` on `space`. `action_side` (app.py:442) calls `action_move` unless view 3 draws the rail (≥ 100 columns).

## Probes (`%TEMP%/incMRb-probe/p1.py`–`p3.py`, outside the repo; values printed)

| Probe | What | Result |
|---|---|---|
| P-1 | `present_tasks_m(b, "ppr")[0]` | `tm2 tstore tm3 tm4 ttele ttrain tm5 trota` |
| P-2 | view 1 `ppr`, 118x30 and 80x24 | header line 0; ruler lines 1–2; legend strip line 3; span line 4; field rows 5–12 (8); rule line 13; briefs 14–21; cursor `tm2` (` ⟦▎ ■ Rubric sign-off`) |
| P-3 | view 2 `ppr`, 118x30 | the same field; blocks 14–17 in two columns as above |
| P-4 | view 3 at 118x30, 118x18, 80x24, 80x14 | 19, 11, 19 and 11 stops; folded none, {ppe, ppd}, none, {ppe, ppd} |
| P-5 | `_all_plan(b)` | ppr 8 tasks, ppe `tgq tg1 tgr tg2 tgx`, ppd `tha thr th1` |
| P-6 | MR-a's `gantt_milestone_row` and `gantt_lane_label(…, label_w − 3)` on the present axis, lane `tm2 tm3 tm4 tm5` | the cells and labels in the table below |
| P-7 | `ppd`, no cursor | base cursor brief `⟦API reference⟧` |
| P-8 | `_present_field(gantt_milestone_row(…, "tm2", …))` | `KeyError 'rev:violet'` |
| P-9 | a milestone titled `\`, `x\`, `a]b[/]`, `[@click=app.quit]x` or `日本語のタイトル` added to `ppr`, the cursor, views 1/2/3 at 80x24 and 118x30 (run on the ms-row-proto tree at 2ce3943, read only) | 0 exceptions, 0 `@click` spans; but for `\` and `x\` the view-1 brief line reads `⟦\\⟧` / `⟦x\\⟧` (the backslash doubled) and is width + 1 (81, 119); views 2 and 3 keep the width |

P-6 (the plain field and label each selection gives; `field_w` is 73 at 118, 55 at 100 and 45 at 80):

| w | selection | label (`label_w − 3`) | field (plain) | `rev:` cell | chip |
|---|---|---|---|---|---|
| 118 | none | ` ◆ 4 milestones ▲1` | `        ■ ▲1d     ■2 Oct 24   ★ Oct 30` | — | `due Oct 24` |
| 118 | tm2 | ` ■ Rubric sign-off` | `        ■ Rubric… ■2 Oct 24   ★ Oct 30` | 8 `rev:violet` | `due Oct 19` |
| 118 | tm3 | ` ■ Steering go/no-go   1/2` | `        ■ ▲1d     ■2 Steerin… ★ Oct 30` | 18 `rev:violet` | `due Oct 24` |
| 118 | tm4 | ` ▲ Store list frozen   2/2` | `        ■ ▲1d     ▲2 Store l… ★ Oct 30` | 18 `rev:cyan` | `due Oct 24` |
| 118 | tm5 | ` ★ Pilot launch` | `        ■ ▲1d     ■2 Oct 24   ★ Pilot launch` | 30 `rev:pink` | `due Oct 30` |
| 80 | none | ` ◆ 4 ms ▲1` | `▲1d ■    ■2    ★ Oct 30` | — | `due Oct 24` |
| 80 | tm2 | ` ■ Rubric sign-…` | `    ■    ■2    ★ Oct 30` | 4 `rev:violet` | `due Oct 19` |
| 80 | tm4 | ` ▲ Store li… 2/2` | `▲1d ■    ▲2    ★ Oct 30` | 9 `rev:cyan` | `due Oct 24` |
| 80 | tm5 | ` ★ Pilot launch` | `▲1d ■    ■2    ★ Pilot launch` | 15 `rev:pink` | `due Oct 30` |

## Tests that pin presentation frames (grep of `tests/test_present*`, plus the two the slice names)

**Byte oracles on boards with NO milestone.** `tests/present_board.py` and `tests/present_notes_board.py` hold 0 `milestone` hits. These tests should therefore stay byte-equal under MR-b: they guard LLR-4651.5 (no row when there is no milestone) and LLR-4652.8. They are not re-baselines (finding B-1).
- `test_present.py::test_TC_1001_the_exact_presc_frame_at_118x30`, `::test_TC_1002_the_exact_presc_frame_at_80x24` and `::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle` compare against PRES-V3-gantt (`2026-10-18-batch-01/evidence/frames`).
- `test_present_views.py::test_TC_1803_the_exact_split_frames` compares against PRES-V3-split.
- `test_present_views_app.py::test_AT_1801_2_shows_every_task_text_at_once` compares against PRES-V3-split, through the app.
- `test_present_polish.py::test_TC_2003_the_long_note_equals_the_rounds_frame` compares against PRES-V4-gantt-notes (`2026-10-18-batch-03`).
- `test_present_note_highlights.py::test_AT_2905_the_regression_pin` compares against the PRES-V3-gantt-118x30 golden.

**Deck byte oracles.** These stay byte-equal and pin LLR-4654.1:
- `test_present_html_export.py::test_TC_4703_LLR_4501_3_bytes_equal_independent_url_free_H_fixture`, `::test_TC_4704_LLR_4501_4_all_bytes_equal_independent_url_free_H_fixture` and `::test_TC_4741_LLR_4504_1_one_file_oracle`. Their fixture holds milestones, among them `a3` and the hidden-class `hm1`.
- `test_present_html_at.py`: its sha256 checks are of the board file, not the deck.

**Frame assertions on boards WITH milestones.** These are the likely re-baselines; E4 confirms them one at a time:
- `test_present_milestone.py`: 5 tests, on the portfolio board (open milestones).
- `test_present_all.py`: 28 tests. Among them are `::test_TC_2103_the_frame_sweep` (the stops are the drawn rows, 1 per milestone today), `::test_TC_2103_no_stop_hides_under_the_overflow_row` and `::test_AT_2104_three_views_one_cursor`.
- `test_present_backlog_round.py`: its fixture holds milestones; it also has the `PRESENT_KEYS` and `PresentKeys` guard at :158-193, which is LLR-4653.6.
- `test_legend.py`: `render_present` and `render_present_all` at :598-699, and `R` at :755 and :812, on the milestone-marks fixture.
- `test_milestone_marks.py`: `R` at :488.

## Findings for E2 (base facts that touch the requirements)

- **B-1.** §6 of `01-requirements.md` lists PRES-V3, PRES-V4 and the `tests/test_present*.py` family as frames that "pin one row per milestone in `R`" and must be re-baselined. The PRES-V3 and PRES-V4 boards hold no milestone (see above), so those frames must stay byte-equal. They are guards, not re-baselines. Only the milestone boards' tests move.
- **B-3.** `_present_brief` (views.py:7534) escapes its cut title with `escape`, the escape R-7 rejected: a title ending in `\` prints the backslash twice and the brief line is one cell too wide (P-9). `_present_finish`'s width assert measures the markup and misses it. The unit is not in the slice; AT-4655 depends on it (E2-F1).
- **B-2.** AT-4653 says: "At 80x24 the overflow folds fewer projects than at base." At 80x24, base folds no project of MR-F (P-4: room 21, need 19), so "fewer" cannot be met. LLR-4651.7's own 118x18 example can be met: base folds 2 and the design folds 0 (the arithmetic is in `graph-proto-V.cw.md` `_all_layout`).
