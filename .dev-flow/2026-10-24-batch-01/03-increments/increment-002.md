# Increment 002 — HLR-2604 · `the encoding through one seat`

| Field | Value |
|---|---|
| Batch | `2026-10-24-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2604` / `LLR-2604.1` (the seat), `LLR-2604.2` (the 20-site routing + the enumeration guard) · `LLR-2606.3` (`render_marks`, the ARQ A-1 fold) · TC-2604, `AT-2603`, `AT-2607` minted here |
| Acceptance | `AT-2603` · `AT-2607` — white-box `TC-2604`, `TC-2606` (`render_marks` arms) |
| Agent | `software-dev` (spawned coder) |
| Date | `2026-10-24` |

## 1 · What changed

Every milestone mark in every view and notice now renders through one seat, `views.milestone_mark(task, board, today) -> (glyph, style, late_chip)` (LLR-2604.1, MM-D1 variant B): the class's shape in its colour from `board.marks`; unclassified (unset or unknown id) `◆` in `mut`; late → the caller's date renders `over` and the chip is `▲Nd` (one channel — the gantt cells derive the date label's tone from the chip, never their own lateness); reached → hollow via `HOLLOW` plus `✓` in `reached`. The 20 sites of LLR-2604.2 route through it: lanes/focus title markers, the bank edge (when a milestone ends the bank), the kanban/focus axis glyph, `_milestone_title`, `gantt_milestone_cells`, the one-date bars and their echo, the gantt ruler milestones, the gantt row label, the chain map label, the band rule facts, the presentation field row, the agenda row (mark before the title, the round's `agenda_row_m`), the people view's task rows, and `app.py`'s two notices (`:2133`, `:2172`). The exclusions stay byte-identical and census-enforced: the title glyphs, the project-span due marks, the slip notice at `app.py:2433`, the fold-row/band `+N ◆` count tails, the month ruler's lateness. A source-census test enumerates the sites (the seat's call per site function + a tokenize-based sweep that fails on any new literal `◆` draw outside the declared lists) so a new frame cannot skip the seat. `views.render_marks(directory, sel, w, h, counts=None)` ships the `#` manager's pure frame (the ARQ's A-1 fold): one row per class — shape in colour, name, open/all counts (dropped first under width pressure), hidden dimmed with `hidden: gantt + present` — the chosen row shaded, the `◆ (no class)` row, `No classes yet.` when empty, and the key line `↑↓ move ␣ hide/show n new e edit esc close`; every row exactly `w` cells of explicit-style `Text` pieces. Tested here, unwired until 003 (D-4's accepted cost). Two engine fixes the seat made visible: peeked boards (agenda/people lanes) now carry the live marks dict (`board_lanes` in app.py), and a milestone due on the project's due day no longer overwrites the project-due ruler mark.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2604.1, LLR-2604.2, LLR-2606.3 | the seat, HOLLOW, MARK_GLYPHS, the 16 view routings, `render_marks`, the census helpers |
| `taskboard/app.py` | source | LLR-2604.2, LLR-2601.3 | the two notices through the seat; `board_lanes` hands the live marks dict to peeked boards |
| `tests/test_milestone_marks.py` | test | HLR-2604, HLR-2602 (TC-2604, TC-2606, AT-2603, AT-2607, a TC-2602 arm) | 11 nodes |
| `tests/test_gantt_milestones.py` | test | LLR-2604.2 | the seat's signature: reached hollow, the date tone from the chip, the due-day collision |
| `tests/test_kanban_milestones.py` | test | LLR-2604.2 | `band_milestone_facts(board)`; the glyph in the seat's style |
| `tests/test_present_milestone.py` | test | LLR-2604.2 | the presentation field row through the seat; the late law amended to MM-D1 |
| `tests/test_people_view.py` | test | LLR-2604.2 | the unclassified `◆` row expectation |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |

## 3 · How to test

`env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_milestone_marks.py` (11 nodes; `-k sites` / `-k TC_2604` for the contract's selectors); with the close suites (`evidence/suite-002.txt`, 275 passed); the broad touched batch of 30 suites (`evidence/suite-002b.txt`).

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 | `test_TC_2604_the_seats_truth_table` + `test_TC_2604_a_nonempty_chip_implies_over_at_the_gantt_cells` (the seat's 3-path unit and its one-channel arm) | 2 passed (`suite-002.txt`) |
| A | TC-2604 enumeration guard, TC-2606 `render_marks` arms | 6 passed (`suite-002.txt`) |
| B | `test_AT_2603_the_state_shows_in_text`, `test_AT_2607_an_unknown_id_is_safe` (C-18: one node each, minted here) | 2 passed (`suite-002.txt`) |

| Field | Value |
|---|---|
| **RED counterfactual** | `taskboard/views.py` `_milestone_title` — a raw `◆` draw inserted beside the seat call — made `test_TC_2604_the_sites_enumeration_every_milestone_mark_routes_through_the_seat` fail (the census sweep flags any literal `◆` outside the declared lists) · `evidence/mutation-002.txt` (arm 6) · restore digest `e37416015f7ac6926ba54f5235bc0887d5226446b43ed8fe52324e40715e9992` |
| **Mutation verdicts** | 14 arms over the 11 new nodes (the truth table, the one-channel and the enumeration nodes carry two reddeners each): 14/14 KILLED · 0 SURVIVED · 0 CRASH/BAD · every restore proven by hash · `evidence/mutation-002.txt` · arms that stayed GREEN: none (two first-round arms were replaced as inert/ill-aimed before the final run — the fallback-tone drift for the one-channel arm, the milestone-gated seat read for the TC-2602 arm) |
| **Instrument RED-proof** | none — no instrument beyond the suite |
| **Emitted-form assertion** | none — this increment emits no artifact (the captures are P4's) |
| **Reverse census** | 5 probes: B1 `grep -rl "milestone_tone\|milestone_mark\|band_milestone_facts\|gantt_milestone_cells" tests/` — the touched suites re-run (suite-002 + suite-002b, `1576 passed, 1 skipped` — the environmental clipboard arm, pre-existing); B2 no file moved; B3 no golden capture; B4 `board_lanes`/`board.marks` consumed by the agenda/people lanes — covered by `test_all_agenda`/`test_people_view` in suite-002; A3 no other module — 0 foreign hits (`grep -rl "milestone_mark" tests/` → `test_milestone_marks.py` + the touched suites only) |
| **Correction population** | none — no correction |
| **Frozen interfaces** | people.py, boards.file_lock/keep_aside, models.write_atomic/clean_strings untouched; the section-3 exclusion sites byte-identical (the census enforces it); `Board._to_dict` untouched — verified in the diff the code-reviewer reads |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-24-batch-01/evidence/suite-002.txt | c8f67741ca7586b3548a65b948d83281c42b1c05baf567625733f6b2102e1ded |
| suite-002b.txt | .dev-flow/2026-10-24-batch-01/evidence/suite-002b.txt | b404a0637ab3413827c619236e160a22e3d69829d01490c0bfc1ebe71f9f67a0 |
| mutation-002.txt | .dev-flow/2026-10-24-batch-01/evidence/mutation-002.txt | c594a56d5671e5b4021ad56a4e3a3aae134bbd2c01892fb94e53dee9b2ffb11b |

| Field | Value |
|---|---|
| **Evidence files** | `3 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · OK to advance, 0 HIGH (F1 the echo glyph-only adoption — declared §6 + docstring; F2 the due-today `soon` label — declared; F3 docstrings; F4 typing deferred to 003); frozen set named untouched; packet claims verified against the bytes; folds re-passed and DISCHARGED by the same reviewer |

## 5 · Risks

(1) The bank-edge ("when a milestone ends the bank") and count-tail readings are judgment calls — both follow the commission's own words and are declared in the census. (2) `render_marks`' `counts` keyword is minted here with the manager as its only intended caller (003). (3) `milestone_tone` is now called by no view site but remains (its law tests call it directly); retirement is a cleanup outside this batch. (4) `lead_band`'s new optional `board` parameter defaults to the old behaviour. (5) The enumeration census is anchor-based: legitimate new `◆` draws (004's legend) must be declared in the census lists — by design.

## 6 · Pending items / spec deviations

AT-2603 and AT-2607 are realised here (C-18: exactly one node each). AT-2601 remains provisional (its node mints in 003). Five interpretations declared in §5 — all traceable to the commission's words or the round. No silent spec edit. The code-reviewer's folds (re-pass discharged, see §4b): **F1** `gantt_echo` adopts the seat's glyph only — its tone law (the `over` selection cue) predates marks and stays, so the class colour is not adopted in the echo (declared here and in the docstring); **F2** the due-today gantt date label renders `soon` (aligns with the band's today->`soon` convention, TC-613) — declared, kept; **F3** docstrings updated (`lead_band`, `gantt_echo`, the `_gantt_frame` collision comment); **F4** `AgendaItem.board`/`PersonItem.board` typed `object` — tightened when 003 wires the manager (deferred, named there).

## 7 · Suggested next task

Increment 003 — the editor's variant-A Select (`alt+m`, `TASK_KEYS`), `modals.MarkForm`, `app.MarksManager` (frame = `views.render_marks`), `keymap` `#`, `taskboard.tcss`; tests `tests/test_marks_manager.py` (mints `test_AT_2601_a_class_is_created_and_survives`) and the modal-law rows in `tests/test_modal_keys.py`.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 2 source files |
| 2 | Tests in this increment | ✓ | 11 new nodes + 4 touched suites |
| 3 | Layer 0 where it applies | ✓ | §4: the seat's truth table + one-channel arms |
| 4 | RED counterfactual | ✓ | §4, `mutation-002.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b: OK to advance, 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | §4 + the census |
| 9 | Coverage verified on disk | ✓ | `suite-002.txt`: 275 passed |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence |
| 11 | Mutation verdicts | ✓ | §4: 14/14 KILLED |
| 12 | Instrument RED-proof | ✓ | §4: none, declared |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4: none, declared |
| 15 | Independent review | ✓ | §4b: PASS, folds discharged |
| 16 | Evidence files | ✓ | §4: 3 digests |
