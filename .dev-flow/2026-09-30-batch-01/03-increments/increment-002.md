# Increment 002 — HLR-003 / HLR-004 · `Kanban high band (K4) + priority badges`

> Template: flow `templates/increment-template.md` (core). Reserved field names kept literal.
> Lives at `.dev-flow/2026-09-30-batch-01/03-increments/increment-002.md`.

| Field | Value |
|---|---|
| Batch | `2026-09-30-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | n/a — one lane |
| Requirement(s) | HLR-003, HLR-004, LLR-003.1, LLR-003.2, LLR-004.1, LLR-004.2 |
| Acceptance | AT-003, AT-004, AT-006 · white-box TC nodes in §4 · Layer 0: `kanban_order` band arms, `card_cell` badge/width arms |
| Agent | `software-dev` |
| Date | `2026-09-30` |

---

## 1 · What changed

- **K4 band, through the one ordering seat.** `kanban_order(..., band=False)` gained a `band`
  keyword: when true and the group mode is not `priority`, the column's OPEN high cards (not
  done, not archived; blocked included) are lifted — after the project-focus filter — into a
  first group named by the NUL-led constant `KANBAN_BAND`, sorted by the active sort like any
  group. `_kanban_column_rows` (grouped renderer) asks for it and draws a non-selectable
  `── high ──` divider, the cards and a closing rule; the grouped branch of `nav_model` asks
  for it exactly when the presentation is `grouped`, so nav order = draw order (F-3). Lanes
  and matrix never ask (decision D1, `01-requirements.md` §6.2), so the prototype's `\x00high`
  pseudo-lane cannot occur — tested.
- **Badges.** `PRIORITY_BADGE = {high: !! over, normal: == soon, low: ++ green}` — the
  `_highlight_markup` tokens and tones. `card_cell(..., badge=False)`: with `badge=True` an open
  card gets a bold reverse-video badge + space between the prefix and the title (3 cells, shed
  when the cell is narrower) and no `!` ink token; done/archived cards get neither. The grouped
  and lanes kanban pass `badge=True`; the Focus rail and People keep `!` (D4).
- **THE GLYPH HOUSE** comment rewritten: the history kept, the 2026-09-30 owner choice stated,
  and the conflicts recorded — `==`/`soon` = due-today amber family, `!!`/`over` = overdue
  chip hue, `++`/`green` = also a project hue — all three accepted by the owner on 2026-09-30
  (the green one explicitly, after this packet's first version: LED .5).
- **Legend / help.** The kanban legend's `!` entry is replaced by the three badges, each listed
  only while a visible open card of that priority exists (`open_priorities` fact). The kanban
  help example shows `▊ !! …`; help usage gains a "la prioridad" section saying the band is
  grouped-only (help copy is Spanish like its siblings).

Measured (`evidence/measure-baseline.json` → `evidence/measure-after.json`, the round's
fixture, selection on t11):

| | 120×36 | 80×24 |
|---|---|---|
| board rows (non-empty lines) | 16 → 17 (+1) | 16 → 17 (+1) |
| cards in `line_map` | 21 → 21 | 21 → 21 |
| title chars, high cards | 12–17 → 11–16 (−1 each) | 2–7 → 1–6 (−1 each) |
| title chars, normal cards | 16–18 → 14–16 (−3, or 0 when the title already fit) | 7–13 → 4–10 (−3 each) |
| title chars, low cards | 11–18 → 11–18 (0 here: titles short enough) | 7–12 → 4–9 (−3 each) |

Badge cost = 3 cells per open card; high cards net −1 because the 2-cell ` !` token is freed.
Band cost = 2 rows (divider + rule) per column holding open highs (3 of 4 columns here), less
the group headers the band empties; the tallest column grew by 1 row.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | HLR-003, HLR-004, LLR-003.1, LLR-003.2, LLR-004.1, LLR-004.2 | `PRIORITY_BADGE`, `card_cell(badge)`, GLYPH HOUSE comment, `KANBAN_BAND`, `kanban_order(band)`, `_kanban_column_rows` band rows + badge, lanes badge, `nav_model` grouped `band=`, legend fact + entries, help example/usage. (The `bar_h` hunk in `render_view` is NOT this batch's — the operator's own gantt-filter fix, left intact.) |
| `prototypes/kanban_priority/proto.py` | fixture | HLR-003, HLR-004 (the prototype round; `fixture.py` also feeds `measure_real.py` / `capture_after.py`) |
| `prototypes/kanban_priority/fixture.py` | fixture | HLR-003, HLR-004 (the prototype round; `fixture.py` also feeds `measure_real.py` / `capture_after.py`) |
| `prototypes/kanban_priority/NOTES.md` | doc | HLR-003 | round notes |
| `prototypes/kanban_priority/out/facts_kanban.json` | generated | HLR-003, HLR-004 (the round's measurements) |
| `prototypes/edit_modal/out/after/kanban_120x36.svg` | generated | HLR-003, HLR-004 (after-captures of the real app) |
| `prototypes/edit_modal/out/after/kanban_80x24.svg` | generated | HLR-003, HLR-004 (after-captures of the real app) |
| `prototypes/edit_modal/out/after/wt_kanban_120x36.png` | generated | HLR-003, HLR-004 (after-captures of the real app) |
| `prototypes/edit_modal/out/after/wt_kanban_80x24.png` | generated | HLR-003, HLR-004 (after-captures of the real app) |
| `tests/test_kanban_priority.py` | test | AT-003, AT-004, AT-006, LLR-003.1, LLR-003.2, LLR-004.1, LLR-004.2 | NEW — 133 nodes |
| `tests/test_palette_ration.py` | test | HLR-004 (LED .1) | 2 tests' expectations changed (see §6) |
| `tests/test_app.py` | test | HLR-003 | 2 tests' oracles made band-aware (see §6) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 3 (uncapped) |
| Doc files | batch record only |

## 3 · How to test

```
cd C:\Users\jjgh8\Github\taskboard
set PYTHONUTF8=1
python -m pytest -q tests/test_kanban_priority.py tests/test_palette_ration.py tests/test_legend.py tests/test_cells.py tests/test_app.py
python -m pytest -q                                   # full suite
python prototypes/edit_modal/capture_after.py svg     # out/after/kanban_*.svg
```
Manual: `python -m taskboard`, `4` (kanban), raise a card with `!`: it jumps into the band
and the cursor stays on it; `g` to group=priority: the band disappears (the High group is it);
`tab` to lanes: badges, no band.

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | `test_seat_band_holds_the_open_highs_in_the_sorts_order[5]`, `test_seat_band_skips_done_archived_and_the_priority_grouping`, `test_seat_band_respects_the_project_focus`, `test_seat_without_band_is_unchanged[15]`, `test_badged_cards_are_exactly_their_width[41]`, `test_card_badge_per_priority_and_none_when_finished`, `test_unknown_priority_wears_the_normal_badge` | 65 passed |
| **A · white-box** | `core` · `full` | `test_lanes_and_matrix_draw_no_band[2]`, `test_legend_lists_the_badges_that_are_on_the_board`, `test_help_example_shows_a_badge_and_says_the_band_is_grouped_only` | 4 passed |
| **B · black-box** | `core` · `full` | AT-003 `test_band_is_drawn_and_nav_walks_the_draw_order[60]`, `test_the_cursor_walks_the_band_first_in_the_app`; AT-004 `test_the_app_paints_a_badge_on_every_open_card[grouped,lanes]`; AT-006 `test_a_card_raised_to_high_joins_the_band_and_keeps_the_cursor` | 64 passed |

Executed: `tests/test_kanban_priority.py` 133 passed; with `test_palette_ration.py`,
`test_legend.py`, `test_cells.py`, `test_app.py`: **545 passed** in 60.79 s; full suite **1506 passed** in 192.40 s
(`evidence/inc002-green.txt`, before the L2/L3 test-only fold; the folded nodes re-run
89 passed). **Full suite (both increments): see `evidence/full-suite-after.txt` and §4 of the
validation record.**

### RED counterfactual — executed, not predicted

RED on base: `evidence/inc002-red-on-base.txt` — **111 failed, 22 passed**. The 22 GREEN on
base are preservation arms by design: the 20 `group=priority` arms of the AT-003 matrix (no
band there, before or after) and the 2 lanes/matrix "no band" arms; each is shown RED under a
mutation (K3 for group=priority via the seat test, K10 for lanes/matrix).

| Field | Value |
|---|---|
| **RED counterfactual** | 111 of 133 new nodes RED on the base tree (`evidence/inc002-red-on-base.txt`); the 22 preservation arms RED under K3/K10 (`evidence/inc002-mutations.txt`); restore proven per mutation by SHA-256 `0e137914826a11de…` ok=True |

| Field | Value |
|---|---|
| **Mutation verdicts** | 10 mutations on `taskboard/views.py`, `evidence/inc002-mutations.txt` (script `evidence/mutate_inc002.py`): K1 band takes done highs KILLED · K2 nav forgets the band KILLED (29 arms RED; the 20 group=priority + lanes-free arms stay GREEN, correctly) · K3 band under group=priority KILLED · K4 badge on finished work KILLED · K5 badge never shed KILLED (3 narrow-width arms) · K6 legend ignores the board KILLED · K7 divider unlabelled KILLED · K8 lanes cards unbadged KILLED · K9 band before the focus filter KILLED · K10 seat defaults band on KILLED · every restore ok=True (re-run after the review fold) |

### Instrument RED-proof

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `measure_real.py` kanban title counter | base tree | 2–13 chars at 80 (baseline), the numbers the table starts from |
| `_painted_badges` (app strips) | base tree | `counts == {"!!": 0, "==": 0, "++": 0}` → AT-004 RED (inc002-red-on-base.txt) |
| divider-in-column slice | review finding L2: a whole-row search let Backlog's divider answer for Doing | rewritten to slice the Doing column; K7 still KILLED |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown reporting a failure before its first PASS was believed |

### Emitted-form assertion

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts: the rendered kanban text (`render_kanban(...).plain` + `line_map`, what the app paints) and the app's painted strips (AT-004 reads colour + reverse off the compositor) |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc002-red-on-base.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc002-red-on-base.txt` | `e3d3b309f008227b463f5ea3c0719a96792310e4e2f9dc7932df375f3d842c39` |
| inc002-mutations.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc002-mutations.txt` | `070b99be8cbfb81ac2e28ac98d421cb2e0f612611b7f0a26bfa522d2c7073626` |
| inc002-green.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc002-green.txt` | `514e3238c9788b3d86e3aeb8989d2d2f2942754fea8837a0f156cef66ab0f3ef` |
| full-suite-after.txt | `.dev-flow/2026-09-30-batch-01/evidence/full-suite-after.txt` | `a64ea72a3221a02a0467518571349064ab54f545db08e5c11c9276924fe5fc15` |
| measure-baseline.json | `.dev-flow/2026-09-30-batch-01/evidence/measure-baseline.json` | `1fe8ea53f36acd6351325cea1b9a957bde466637ffe1218af01bd72e746aa3b1` |
| measure-after.json | `.dev-flow/2026-09-30-batch-01/evidence/measure-after.json` | `69ac2f6c578b602b368441576e5ee41436854d436d59cfe2d15e4df6951432b7` |

| Field | Value |
|---|---|
| **Evidence files** | 6 artifacts at `artifact_homes.evidence`, each cited above with the SHA-256 of its stored bytes |

### Load-bearing emptiness

"The band never reaches lanes/matrix" is an absence: guarded by
`test_lanes_and_matrix_draw_no_band` (no divider, no NUL drawn) and positively controlled by
K10 (defaulting the band on makes lanes draw it → RED).

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by other tests | `grep -rln "card_cell\|kanban_order\|nav_model\|legend_entries\|help_example" tests/` | `test_palette_ration.py` (2 RED → expectations changed, LED .1), `test_app.py` (2 RED → band-aware oracles), `test_legend.py`, `test_cells.py`, `test_emoji_picker.py`, `test_lanes_grid.py`, others — full suite green after the change |
| B2 file moved | none | did not fire |
| B3 goldens | `grep -rl "views.py" tests/` | no byte-identity golden of the kanban; did not fire |
| B4 artifact consumed elsewhere | `HelpModal` reads `legend_entries`/`help_example`/`help_usage` | strings changed, same shape; covered by the legend/help tests |
| A3 interface consumed outside the module | `grep -n "card_cell\|kanban_order" taskboard/*.py` | only `views.py`; new keywords default to the old behaviour |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes (B1 · B2 · B3 · B4 · A3): B1 fired — 4 existing tests went RED and were re-validated with changed expectations (§6); B2/B3 did not fire; B4 HelpModal consumers covered; A3 no outside consumer |

### Correction population

| Correction | Population | Enumeration method | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| "kanban marks high priority with `!` in ink" | every surface stating the kanban priority mark | `grep -n '"!", "ink"\|high-priority\|! alta' taskboard/views.py` + `grep -rn '"!"' tests/` | 5 | card_cell (badge path), kanban legend, kanban help example, 2 palette tests | card_cell's non-badge path (Focus rail, People keep `!` — D4); swimlanes `!N` (a different mark, unchanged) |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated by grep before the first edit; 5 sites edited, 2 left with reasons |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS-WITH-NOTES, 0 HIGH / 0 MEDIUM / 3 LOW · L2 (divider check read the whole row) folded — sliced to the Doing column; L3 (band derived from phase) folded — `board.is_done`; L1 (matrix legend lists badges) recorded as a known, inherited gap → §6 and BACKLOG |

## 5 · Risks

- Titles at 80 columns lose 3 more characters per normal/low card (1 per high card); at 80 a high card's title can be 1 character.
- The legend is presentation- and focus-blind: in matrix (and under a project focus) it can list a badge no card draws (inherited from the `!` entry; L1).
- Colour conflicts, all owner-accepted 2026-09-30: `==` vs due-today amber, `!!` vs overdue `-Nd` and blocked `▲`; `++` vs a green project stripe (LED .5).
- `KANBAN_BAND` is a sentinel group name; only the grouped renderer reads it. A future caller that passes `band=True` and draws group names itself would draw a NUL-led name.

## 6 · Pending items / spec deviations

Existing tests changed (each because the owner's decision legitimately changes its expectation):
1. `tests/test_palette_ration.py::test_a_judging_hue_is_never_worn_by_a_name_or_a_priority_mark` — kanban badge (`!!`/`==` + reverse) exempted by exact shape; every other priority mark in a judging hue still fails (LED .1).
2. `tests/test_palette_ration.py::test_every_view_that_marks_priority_marks_it_with_the_glyph` — `marks["kanban"]` is now `[("bold reverse #f43f5e", "!!")]` (LED .1).
3. `tests/test_app.py::test_kanban_sort_cycles_and_names_the_mode` — oracle puts the band first; one local Doing card `k10` added so the five sort orders stay pairwise distinct (with the band, only 4 orders were possible over the old fixture — measured by exhaustive search, `/tmp/search.py`, not kept).
4. `tests/test_app.py::test_kanban_group_cycles_headers_and_membership` — band cards sit above every header; header set computed over non-band cards.
- L1 matrix/focus legend ghost → BACKLOG.
- Focus rail / People still show `!` — owner may want the badge there too → BACKLOG question.
- `taskboard/views.py`'s `bar_h` hunk is NOT this increment's: it is increment 004 (adopted).

## 7 · Suggested next task

Owner review of the after-captures (`prototypes/edit_modal/out/after/`), then a ruling on
`++`/green vs project hue and on badges outside the kanban.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | 1/4 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_kanban_priority.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` ‹one complete run owned by the orchestrator ~ Layer 0› | ✓ | 65 unit nodes (§4) |
| 4 | **RED counterfactual** declared | `core` · `full` ‹RED counterfactual mandatory ~ RED counterfactual› | ✓ | inc002-red-on-base.txt, inc002-mutations.txt |
| 5 | **Reverse census** declared | `core` · `full` ‹reverse census of the touched symbol ~ Reverse census› | ✓ | §Reverse census |
| 6 | `code-reviewer` passed | `core` · `full` ‹RED counterfactual mandatory ~ code-reviewer› | ✓ | 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | `views.py` `bar_h` hunk untouched |
| 8 | Frozen interfaces untouched | all | ✓ | new keywords default to old behaviour |
| 9 | Coverage claims verified on disk | all | ✓ | 133 collected |
| 10 | Load-bearing emptiness declared | all | ✓ | §Load-bearing emptiness |
| 11 | **Mutation verdicts** declared | all | ✓ | 10/10 KILLED |
| 12 | **Instrument RED-proof** declared | all | ✓ | 3 |
| 13 | **Correction population** declared | all | ✓ | 1 correction |
| 14 | **Emitted-form assertion** declared | all | ✓ | 2 |
| 15 | **Independent review** names somebody | all | ✓ | `code-reviewer` |
| 16 | **Evidence files** declared | all | ✓ | SHA256SUMS.txt |
