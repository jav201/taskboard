# E1 rulings — Inc MR, a project's milestones share one gantt row (dev-flow-v3-beta)

> E1 (Opus, architect) stopped at the size gate (MR-3). Nothing in this file is a requirement yet: it is the
> split proposal and the design facts read so far, so the next E1 pass does not re-derive them.
> Base: `59775bb` (branch `feat/milestone-row`). Commission: `.dev-flow/COMMISSION-milestone-row.md`.

## 1. Size gate: the scope is about 58 LLRs, over the cap of about 40

Inventory, one singular EARS row each, failure paths separate (estimates, not drafted):

| Area | LLRs | Content |
|---|---|---|
| Board plan | 6 | one shared row per group with a drawn milestone, under its span row; the same members as base (open, plus reached while the group has open work, D-606); tasks one per row, done tail unchanged (`f4b53cc`); Inbox row (D2); folded group draws none; the fold budget counts the row as 1 |
| Board drawing | 11 | mark at date with class glyph and colour; same-day `<glyph>N` (`+` from 10); reached alone = hollow + `✓`; selected title beside its mark, cut with `…`; others' date when it fits whole; late `▲Nd`; label column (`◆ N milestones` / `N ms` below 24 cells, `▲L`; selected: glyph, title, ` i/N`); chip column (selected, else next open, else blank); no line wider than the terminal; rows saved on the round's board (23 → 18) |
| Board navigation | 8 | `↑↓` one stop; the landing rule (selected, else next open with due ≥ today, else first open, else first); `←→` walk by (due, title), same-day included; ends are no-ops; `←→` off the row unchanged; `enter` details; task keys act on the walked milestone |
| D3 | 4 | `/` keeps only matching milestones on the row; no match = no row; `/`+`enter` lands on the match; a hidden class leaves the row |
| MR-2 | 4 | link mode (ruling 2); the paged fold (ruling 3) |
| Failure paths | 7 | no due date; date off the window; 10+ same day; one milestone; no room for any label; the selected milestone filtered out; a group whose only open work is milestones |
| **Board gantt subtotal** | **~40** | |
| Presentation (D1) | ~18 | views 1, 2, 3 field rows (ruling 4); cursor stops; `←→` (open question Q-1); `space`/`a`/`u` on a milestone of the row; briefs (view 1) and blocks (view 2); hint row and PRES-V3/V4 oracle re-baseline; width |
| **Total** | **~58** | |

## 2. Proposed split (MR-3)

- **Inc MR-a — board gantt** (this folder): US-4601, HLR-4601.., AT-4601.., TCs `TC-48nn`. About 40 LLRs. Slice
  estimate: `views.gantt_plan`, `views._gantt_frame` (row emission, paged branch), new `views.gantt_milestone_row`
  (cells + labels), new label/chip helpers or `_gantt_group_label` extension, `views.nav_model` (gantt branch),
  `app.action_hmove` (gantt branch), and the link candidate path if ruling 2 changes — about 7 units in 2 files
  (`views.py`, `app.py`).
- **Inc MR-b — presentation** (`2026-11-xx-v3-incMRb`): US-4651, HLR-4651.., about 18 LLRs, after Q-1 is ruled.
  Shares with MR-a the row drawing unit (cells + labels) as its one interface.

Range check (2026-11-06, `grep -rhoE "(HLR|LLR|AT|US)-<r>[0-9]{2}" REQUIREMENTS.md .dev-flow/ tests/` for r = 46..50):
0 hits each. `TC-46nn`/`TC-47nn` are taken (Inc K, Inc X); `TC-48nn` is free.

## 3. Design facts read (base `59775bb`)

1. **Which views draw milestones (MR-1).** Board gantt: one row each (`gantt_plan`, `views.py:2432`). Presentation
   view 1 `gantt` and view 2 `split` share `render_present`'s field loop (`views.py:7325-7326`): one field row per
   shown open task, milestones included (`_present_task_row`, `:7172`); view 1 also draws one brief per open task
   (`:7337`), view 2 one block. View 3 `all` draws one row per shown open task under each project head
   (`_all_timeline`, `:7589-7592`). All three draw milestones; views 1 and 2 change together unless split on purpose.
2. **`←→` today.** Board gantt: `hmove` (`keymap.py:191`, `app.py:3439`) jumps to the next non-empty nav column;
   the gantt has one column (`nav_model`, `views.py:8425-8430`), so it is a no-op there. Presentation: `side(±1)`
   (`keymap.py:247`) is a cursor move in views 1/2 and in view 3 below 100 columns, and rail ↔ timeline in view 3
   from `PRESENT_RAIL_MIN` = 100 (`app.py:445-456`).
3. **Link mode** is a modal frame (`gantt_link_frame`, `views.py:8893`) over `_gantt_frame` with `done_rows=False`;
   its candidate cycle is every open row (`gantt_link_order`, `:8885`); the overlay draws `═` on the waiter's row
   and a connector from the candidate's row (`gantt_link_overlay`, `:8926`); loops wear `⟲` in the row's gutter.
   Every one of these keys on one task per row (`line_map[task.id]`). It already differs from the board gantt
   (no done tail).
4. **Paged fold**: `_gantt_frame` pages a group taller than the body (`views.py:3448-3476`) by row index, and below 3
   body rows draws only the span and the selected row (`:3421-3425`).
5. A milestone with no due draws nothing on its row today (`gantt_milestone_cells`, `views.py:2723`).
6. `nav_model`'s gantt branch walks `g.rows` of every group, folded ones included (`views.py:8430`).

## 4. Proposed rulings for MR-2 (for the orchestrator to confirm)

- **Ruling 2 — link mode keeps one row per milestone.** While `L` is open, the frame draws each milestone on its
  own row, as at base; the shared row comes back when the mode closes, with the waiter (or the linked task) still
  selected. *Why:* the `═` overlap, the connector and the `⟲` loop mark each name one task by its row; on a shared
  row a connector end or a `⟲` cannot say which of N marks it means, and the candidate cycle already walks tasks,
  not rows. The mode already draws a different layout (no done tail), and the prototype assumed it (`proto.py:143`).
  *Cost:* the layout jumps when `L` opens. *Alternative:* the shared row in link mode, the candidate shown as the
  row's selected mark, `⟲` moved to the mark's cell — about 6 more LLRs and a change to `gantt_link_overlay`.
- **Ruling 3 — the paged fold treats the shared row as one row.** It is the group's first drawn row, so it sits on
  page 1; a selected milestone selects the page holding the shared row; with 2 body rows or fewer the selected
  milestone draws the shared row, not a lone milestone row. `▲ N above` / `▼ N below` count rows, the shared row
  as 1.

## 5. Open questions

- **Q-1 (blocks MR-b).** In the presentation `←→` already means a move (views 1/2) and rail ↔ timeline (view 3 at
  100+ columns). Walking the shared row's milestones needs either (a) `←→` repurposed on the row in views 1/2 and a
  different walk in view 3, or (b) `↑↓` stopping at each milestone in turn while the row draws them shared (no key
  change). Recommendation: (b), since the presentation freezes its keys (X-4 precedent) and a presenter walks with
  `↑↓`.
- **Q-2.** Confirm ruling 2 (link mode as at base) over the alternative.
- **Q-3.** Confirm the split, and that view 2 follows view 1 (shared code, `views.py:7325`).

## Orchestrator rulings (2026-11-06) on the E1 size gate

- **R-1 (Q-3): the split is confirmed.**
  - **MR-a, board gantt.** Runs now, in this folder (`2026-11-06-v3-incMR`).
  - **MR-b, presentation.** A separate increment, run after MR-a closes, in folder `2026-11-06-v3-incMRb`.
  - View 2 changes with view 1, because the two share code.
- **R-2 (Q-1), presentation: `↑↓` stops at each milestone, and no key changes.** In `R`, `←→` already moves the cursor, or toggles rail and timeline in view 3. This rule applies to MR-b only. On the board gantt (MR-a), `←→` walks the milestone row as the round showed, because `hmove` is a no-op there today.
- **R-3 (Q-2): the link mode keeps one row per milestone.** While `L` is active, each overlay and each `⟲` names exactly one task. The simple form is kept.
- **R-4 (baseline finding, `974289f`).** The gantt cursor's row list (`nav_model`) ignores hidden milestone classes, so the cursor can stop on rows that are not drawn. This is a pre-existing defect, and MR-a fixes it: navigation reads the same filtered board the renderer draws, which is what LLR-4605.3 depends on. E2 designs the fix, and E4 carries a regression test that is RED on base.
- **R-5.** HLR-4606 has two responses: link mode and the paged fold. E2 may split it into two HLRs with a ledger entry. The orchestrator approves this in advance.

## E3 round-1 rulings (2026-11-06). Architect: FAIL (`5d08321`). Security: FAIL (`79ad23f`).

- **R-6 (F-1, F-2, F-3, F-4, F-5).** The architect's resolutions are adopted as written.
  - **F-1:** a shared cell shows its lead's date, or `▲Nd` when the lead is late. `i/N` counts "in its cell".
  - **F-2:** the threshold is `mut`, from the seat. `milestone_tone` stays as it is.
  - **F-3:** AT-4607 and LLR-4602.6 are rewritten with a milestone reached early: `<hollow>✓▸`.
  - **F-4:** the slice is 9 units, including `nav_model`.
  - **F-5:** the dependency gutter stays blank on the milestone row. This is the new LLR-4601.8.
- **R-7 (SEC-1, HIGH, and N-1, MAJOR: the same defect).**
  - **Defect:** the selected milestone's title (and any label) is never placed into field cells as raw markup characters. Probes showed a `MarkupError` on `a]b[/]`, and that `[@click…]` became a live tag.
  - **Fix:** each label is escaped as one whole string BEFORE it is cut into cells. Cell runs are joined only from escaped segments. Better still, the label is emitted as a styled `Text` segment rather than per-cell markup; pick the smaller change that the markup census law accepts.
  - **Width:** the label is measured with cell width (`cell_len`, wide glyphs) and cut with a visible `…`. No row may exceed the field.
  - **Requirements and tests:** one new Unwanted-form LLR carries a negative control: titles `a]b[/]`, `[@click=app.quit]x`, `\` and a wide-glyph title must each render literally, with no exception, and stay within the width.
- **R-8.** The security reviewer's other MEDIUM and LOW findings, and the architect's other MINOR findings, are adopted as proposed. They go into the requirements or graph where they are design, and into `e3-addenda.md` where they are E4 instructions.

The design correction is ONE agent making targeted edits (Opus). E3 round 2 follows: the same two roles re-check only what was blocking, plus anything new.
