# Increment 003 — LLR-1603.1, LLR-1603.2 · `the ? help: a Keys band and the pinned global keys`

| Field | Value |
|---|---|
| Batch | `2026-10-16-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1603` / `LLR-1603.1`, `LLR-1603.2` |
| Acceptance | `AT-1603` · white-box `TC-1606`, `TC-1607` · unit: `keys_grid` and `global_lines` (layer 0: loops with branches) |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-16` |

## 1 · What changed

`keymap.global_keys(view)` returns the live `bar=False` keys in seat order. In `HelpModal`, the view's keys leave the right column for a full-width band (`Keys · this view`) under the two columns: a column-major grid (`keys_grid`) sized to the box's content width, composed at an estimated width and re-laid at the measured width (`_fit_keys`, on mount and on resize). The global keys are a line (`Global  o URL  i Images … R Present  I Templates  S Standup`, entries joined by two spaces, wrapped only between entries by `global_lines`) docked at the bottom of the box, outside the scroll, with the `m full map · ? palette · esc/q closes` hint on its own row below: one row plus the hint at 118×30, two rows plus the hint at 80×24. The usage/legend row is now `height: auto` so the body scrolls as one (it was `1fr`, and the band squashed it to one row at 80×24); the box's vertical scrollbar is 1 cell, so the columns keep the width TC-116 measures.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/keymap.py` | source | LLR-1603.2 | `global_keys` |
| `taskboard/modals.py` | source | LLR-1603.1, LLR-1603.2 | `keys_grid`, `GLOBAL_LEAD`, `global_lines`; `HelpModal`: docstring, CSS (`#help-cols`, `#help-keys-title`, `#help-foot` dock, thin scrollbar), compose (band + docked footer), `on_mount`/`on_resize`/`_fit_keys`/`_key_texts` |
| `tests/test_help_keys.py` | test | HLR-1603, LLR-1603.1, LLR-1603.2 | new: TC-1606 ×4 (+1 parametrised; the resize arm after review F1), TC-1607 ×2, AT-1603 ×2 sizes |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-003-118x31-gantt-help.svg` | generated | HLR-1603 (AT-1603) | `?` in the gantt view, unscrolled |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-003-118x31-gantt-help-end.svg` | generated | HLR-1603 (AT-1603) | after `end`: the band |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-003-80x25-gantt-help.svg` | generated | HLR-1603 (AT-1603) | `?` at 80 columns, unscrolled |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-003-80x25-gantt-help-end.svg` | generated | HLR-1603 (AT-1603) | after `end` |
| `.dev-flow/2026-10-16-batch-01/evidence/capture_app.py` | doc | HLR-1603 | the 003 plan gains the `end` frame |
| `.dev-flow/2026-10-16-batch-01/evidence/mutate.py` | doc | HLR-1603 | battery 003 (P1–P5) |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_help_keys.py tests/test_help_clip.py tests/test_gantt_board.py tests/test_markup_census.py tests/test_markup_sites.py tests/test_legend.py tests/test_setup_help.py tests/test_english.py`; captures: `python .dev-flow/2026-10-16-batch-01/evidence/capture_app.py 003`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 and A | `tests/test_help_keys.py` TC-1606 (5 nodes), TC-1607 (2 nodes) | in the full suite (`suite-003.txt`) |
| B | `tests/test_help_keys.py::test_AT_1603_the_help_shows_the_global_keys_without_scrolling` (118x30, 80x24) | in the full suite (`suite-003.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider` | 2 failed, 2625 passed (`suite-003.txt`); the 2 failures are the pre-existing `base_ref` pair (`preexisting-base-failures.txt`) |

| Field | Value |
|---|---|
| **RED counterfactual** | `modals.py` and `keymap.py` at `d30aa8e` (increment 002's commit): the test file errors at collection (no `keys_grid`/`global_keys`), and an import-free copy of AT-1603 run against the same base files FAILS at both sizes (`R Present` is never painted) · `.dev-flow/2026-10-16-batch-01/evidence/red-003.txt` · restore digest (of the two files' digests) `bc1a88072e17118c3da79c31d6b9af282b34d602f6a273ee8caf45d2866c3250` |
| **Mutation verdicts** | 6 mutants, all KILLED: P1 the grid filled row-major (TC-1606 order arm) · P2 a hand-typed global list (TC-1607 injected-key arm) · P3 the footer not docked (AT-1603: at 80×24 the line scrolls off) · P4 the global line never wraps (TC-1607 row-count arm) · P5 one column too many (TC-1606 width arm) · P6 `_fit_keys` a no-op (TC-1606 resize arm) · arms that stayed GREEN: none · `.dev-flow/2026-10-16-batch-01/evidence/mutation-003.txt` |
| **Instrument RED-proof** | none — no new instrument |
| **Emitted-form assertion** | 1 artifact: AT-1603 reads the screen as the compositor PAINTS it (`render_strips`), not the widget tree |
| **Reverse census** | 5 probes: B1 `grep -rl` over `tests/ taskboard/` — `help-modal-box` → `test_markup_sites.py` (the `Keys` heading flags: still bold `#e6edf7`, green); `help-left`/`help-right` → `test_gantt_board.py` TC-116 (RED once on the 2-cell outer scrollbar, green with the 1-cell one — no assertion changed), `test_help_clip.py` (columns only, green); `bar_keys` → `test_help_clip.py`, `test_keymap.py`, `test_legend.py`, `test_milestones.py` (accessor unchanged); `HelpModal` → `test_cleanup.py`, `test_legend.py`, `test_setup_help.py`, `test_markup_census.py` (TC-401 RED once on `Label(band)` with a non-literal `Text` — the sinks now call `Text(...)`/`Text.assemble(...)` where the census reads them; green); `test_english.py` (`Keys` still painted) · B2 no file moved · B3 no golden · B4 none — the modal emits no artifact · A3 `keymap.global_keys` is new; nothing existing changed shape |
| **Correction population** | none — no correction |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-16-batch-01/evidence/suite-003.txt | f5518e3c63fc0db9c24abf0df6d8058c00d6d40ed945b42d20851f46515e5869 |
| red-003.txt | .dev-flow/2026-10-16-batch-01/evidence/red-003.txt | 46395fc0d1342a268f91bf71571116e73c5a674d8d9f7460b910057c77f5a785 |
| mutation-003.txt | .dev-flow/2026-10-16-batch-01/evidence/mutation-003.txt | c9609226da1aea8277dab5770d0cfb57c75337fc7e295629cc846d062b8d039f |
| app-003-118x31-gantt-help.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-003-118x31-gantt-help.svg | a931dbc4f867af517e51c7ed089206333ab25a3525db1f24cbf9e43e8cfcec97 |
| app-003-118x31-gantt-help-end.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-003-118x31-gantt-help-end.svg | 14316c02636d56efbd5ba36486f3cbcd6db20217d2826503f9bdb06304ce881e |
| app-003-80x25-gantt-help.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-003-80x25-gantt-help.svg | 09d2d087e47b907b2870c4ae83defe72ae6aecf55f7ec20c4f5f751a78cf1a58 |
| app-003-80x25-gantt-help-end.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-003-80x25-gantt-help-end.svg | 48a1792ac2535087718dc2ea29c207d93f02e80b36bd4ea0a7f9d2954b9c4e57 |

| Field | Value |
|---|---|
| **Evidence files** | `7 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS with notes, 0 HIGH · 0 MEDIUM · F1 LOW (the resize re-layout unproven) → fixed: `test_TC_1606_the_band_re_lays_when_the_terminal_shrinks` + mutant P6 KILLED · F2 LOW (TC-1607's expected list mirrors `_live_keys`'s filter) → kept, the injected key and P2 keep it discriminating · F3 LOW (`len` vs `cell_len`) → fixed |

## 5 · Risks

At 80×24 the Keys band starts below the fold: the 1-cell scrollbar is the only cue there is more (the ux-reviewer's PDR notice; the contract owes only the global line unscrolled). The thin scrollbar is this modal's only — a visual difference from the other modals.

## 6 · Pending items / spec deviations

- LLR-1603.2 named the global line "beside" the hint in the commission; the contract (LED .4) put the hint on its own pinned row — 2 rows at 118×30, 3 at 80×24 — and so it is.
- Two changes the contract did not spell out, both made to keep its laws: `#help-cols` `height: auto` (one scroll for the body) and `scrollbar-size-vertical: 1` (TC-116's column width).

## 7 · Suggested next task

Phase 4 — validation (`stations/p4-validation.md`), after the DDR.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 2 source files |
| 2 | Tests in this increment | ✓ | `tests/test_help_keys.py` |
| 3 | Layer 0 where it applies | ✓ | TC-1606/TC-1607 unit cases |
| 4 | RED counterfactual | ✓ | §4, `red-003.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-003.txt` |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence |
| 11 | Mutation verdicts | ✓ | §4: 6/6 KILLED |
| 12 | Instrument RED-proof | ✓ | none new, declared |
| 13 | Correction population | ✓ | none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4 |
