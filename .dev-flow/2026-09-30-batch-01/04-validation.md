# Validation — taskboard — Batch 2026-09-30-batch-01

> Template: flow `templates/validation-template.md` (core). Reserved field names kept literal.
> P4 executed by the orchestrator (`software-dev`) with the evidence below; the qa lens ran at P2
> (`qa-reviewer`, independent sub-agent) and code review at each increment (`code-reviewer`).

## ✅ Verdict (read first)

- **Result:** PASS-WITH-NOTES
  Notes: full suite `1535 passed in 213.66s`, 0 failed (`evidence/full-suite-after.txt`); known gaps G-001, G-002, G-004 are declared, not failures.
- **Layer 0:** 2 unit(s) met the criterion (`kanban_order` band arms — cyclomatic ≥ 3; `card_cell` badge/width) · 2 carry a named reddening mutation (K1/K3/K9/K10; K4/K5)
- **Requirements:** 19/19 pass (7 HLR + 12 LLR) · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (app `run_test`: keys `e`, `tab`, `enter`, `escape`, `down`, `!`; painted strips) with boundary and negative evidence
- **Surface-reachability (bidirectional):** ✓ (matrix below)
- **Supersession inspection (read off the P3 packets, rev60):** ✓ increment-002 §Correction population — the `!` kanban mark: every surviving `"!", "ink"` site is the non-badge path (Focus rail / People), negative for kanban
- **Test ledger:** ✓ reconciles (below)
- **Evidence checklist (qa-reviewer):** WAIVED-BY-OPERATOR — not available: no operator on this runtime to waive; stated plainly instead — the P4 checklist below was self-executed by `software-dev`, a self-review; the independent lenses were qa-reviewer at P2 and code-reviewer per increment

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `views.kanban_order` (band branch) | cyclomatic ≥ 3 | `test_seat_band_*` (22 nodes), `test_seat_without_band_is_unchanged[15]` | passed |
| `views.card_cell` (badge) | cyclomatic ≥ 3 | `test_card_badge_*`, `test_badged_cards_are_exactly_their_width[41]`, `test_unknown_priority_*` | passed |

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `kanban_order` | K1 done highs in band · K3 band under priority · K9 band before focus · K10 default on | yes ×4 | `evidence/inc002-mutations.txt` |
| `card_cell` | K4 badge on finished work · K5 badge never shed | yes ×2 | `evidence/inc002-mutations.txt` |

### UX walkthrough — trigger family D fired

| Criterion | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| typing in notes keeps ≥20/≥10 rows, title and Save on screen | `run_test` + `e`, cursor at end | compositor clip regions | pass |
| tab walks 17 stops, never the preview; enter on Save saves | `pilot.press("tab")`, `enter` | `app.focused` + board model | pass |
| typed `!!…!!` appears red in the preview, in view | `pilot.press` per character | painted segments in the preview region | pass |
| `down` walks the band first | `pilot.press("down")` in kanban | `selected_task_id` sequence | pass |
| `!` raises a card into the band, cursor stays | `pilot.press("!")` | `line_map` rows + selection | pass |
| badges painted per priority, reverse, right tone | app at 160×40, grouped + lanes | painted strips | pass |

**Mechanism used:** the UI framework the UI test driver (Textual `App.run_test` / `Pilot`), plus real Windows Terminal PNGs (`prototypes/edit_modal/out/after/wt_*.png`).

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above | performed |
| Expert inspection | ux-reviewer lens over the requirements | performed (P2, requirements only — not over the built screens) |
| Evaluation with users | the owner using the build | not performed — the owner reviews the captures and the working tree after this batch |

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-001 | test | `tests/test_edit_window.py` AT-001/AT-005 | ≥20 / ≥10 rows; 17 ids on screen; 17-stop tab order | 23 / 11 rows; all ids; order exact | measure-after.json, full suite |
| HLR-002 | test | `-k preview` | soon on open; over after typing, in view | pass | full suite |
| HLR-003 | test | `-k band` | nav == draw over 60 mode arms; band == open highs | pass | full suite |
| HLR-004 | test | `-k badge` | token/tone/reverse; 0 on done/archived; width exact | pass | full suite |
| LLR-001.1 | test (integration) | `-k chip` | 80..140 + 121/122 | pass (threshold measured 122) | inc001-mutations M5 |
| LLR-001.2 | test (integration) | `-k focus_mark` | accent bar on focused only, painted | pass | M4 |
| LLR-001.3 | test (integration) | `-k save_payload` + test_app/test_emoji_picker | payload equal | pass | M6 |
| LLR-001.4 | test (integration) | `-k project_modal` | 62 cols | pass | M7 |
| LLR-002.1 | test (integration) | `-k preview`, `-k markup` | spans + literal brackets | pass | M1/M2/M8/M11 |
| LLR-003.1 | test (unit) | `-k seat` | band order == High-group oracle | pass | K1/K3/K9/K10 |
| LLR-003.2 | test (integration) | `-k band` | no divider/NUL in lanes/matrix | pass | K2/K7/K10 |
| LLR-004.1 | test (unit) | `-k badge` | widths 0..40 | pass | K4/K5/K8 |
| LLR-004.2 | test (unit) | `-k legend`, `-k help` | entries per board | pass | K6 |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test | Surface driven | Deliverable observed | repr · boundary · negative | Result |
|----|----------------|----------------|----------------------|----------------------------|--------|
| US-001 | AT-001, AT-002, AT-005 | `TaskboardApp` → `e` / `a` → `TaskModal` | clip regions, painted preview segments, focus walk, saved task | ✓ · ✓ (80×24, new task, empty notes) · ✓ (RED on base; escape discards) | pass |
| US-002 | AT-003, AT-006 | `render_kanban`+`nav_model` as the app calls them; app keys `down`, `!` | divider row, `line_map`, selection | ✓ · ✓ (priority group, lanes, matrix, focus, archived, done high) · ✓ (RED on base) | pass |
| US-004 | AT-007 | `TaskboardApp` → `enter`, `i` | modal region painted, label renders | ✓ · ✓ (7 fields, unclosed `a[b`) · ✓ (RED on base, 21) | pass |
| US-005 | AT-008 | `render_view` with `search_query` | row count, scale row, filter bar, matching card | ✓ · ✓ · ✓ (RED re-captured) | pass |
| US-006 | AT-009 | `TaskboardApp` keys `5`, `t` | selection + board state | ✓ · ✓ (last card) · ✓ (RED re-captured) | pass |
| US-003 | AT-004 | `TaskboardApp` kanban grouped + lanes | painted badge segments (colour, reverse) | ✓ · ✓ (done, archived, narrow) · ✓ (RED on base) | pass |

### Bidirectional surface-reachability matrix

| Direction | US dimension / deliverable | Producer | Reached at surface? | TC / AT | Status |
|---|---|---|---|---|---|
| input | terminal size 80×24 / 120×36 / 80..140 | layout + `_fold_chips` | yes | AT-001, chip sweep | ✓ |
| input | sort × group × focus × show_archived | `kanban_order(band)` | yes (60 arms) | AT-003 | ✓ |
| input | priority change via `!` | `prio_cycle` | yes | AT-006 | ✓ |
| output | editor layout / preview | `TaskModal` | painted | AT-001/002/005 | ✓ |
| output | band + badges | `_kanban_column_rows`, lanes, `card_cell` | painted | AT-003/004 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed / full | reconciles? |
|------|-----|-----|--------|------------------|---------------|-------------|
| 1336 (operator figure) | 0 | 199 (37 + 133 + 29) | 1535 | 1535 | 1535 passed / 1535 | yes — `evidence/full-suite-after.txt`: `1535 passed in 213.66s` |

Note: the operator's 1336 baseline was taken with the adopted Focus and gantt tests (3 nodes) already in the working tree; this batch's own new nodes are 37 (`test_edit_window.py`) + 133 (`test_kanban_priority.py`) + 29 (`test_details_markup.py`) = 199; 1336 + 199 = 1535.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | LLR-004.2 | legend lists badges in matrix / under focus (presentation-blind legend, inherited) | minor | BACKLOG |
| G-002 | HLR-003 | tall column beyond the viewport not separately tested (UX-9) | minor | declared |
| G-003 | HLR-005 | security S1 in `TaskDetails` / `ImageViewer` / `image_block` | major | CLOSED by increment 003 (owner verdict 2026-09-30) |
| G-004 | (pre-existing) | the `TaskDetails` info grid paints its cells blank (base tree too); ≈13 other `escape()`-into-Textual sites; S2 control bytes | minor/major | BACKLOG |

### Evidence checklist — qa-reviewer (full)

Self-executed by `software-dev` (see Verdict):
- ✓ every AT RED on base — inc001-red-on-base.txt (29/32), inc002-red-on-base.txt (111/133); preservation arms RED under named mutations
- ✓ every mutation KILLED — inc001-mutations.txt (11), inc002-mutations.txt (10)
- ✓ full suite run once by the orchestrator — evidence/full-suite-after.txt
- ✓ four changed existing tests listed with reasons — increment-002 §6
- ✓ no secrets; no destructive command; no commit (commission)
