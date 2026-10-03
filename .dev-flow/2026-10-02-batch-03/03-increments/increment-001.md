# Increment 001 — HLR-301..305, HLR-307, HLR-309 · the readable board

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-03` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-301 (LLR-301.2), HLR-302 (LLR-302.1), HLR-303 (LLR-303.1, LLR-301.3), HLR-304 (LLR-304.1), HLR-305 (LLR-305.1, LLR-301.1), HLR-307, HLR-309 (LLR-309.1) |
| Acceptance | AT-301, AT-302, AT-303, AT-305, AT-307 · white-box TC-301..TC-308, TC-311, TC-313 |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**The kanban (key `4`, grouped) is the readable board the operator chose.** Each card is two
rows: the title across the column after the shipped `!!`/`==`/`++` badge, its rest and a dim fact
strip (link, image, age, dependants, due — the due last to go) underneath; a `┈` row splits cards
stacked in a column; columns are sized by their longest title. Each group is named ONCE, by a band
rule across the board carrying its open count, `N high ↑`, `at risk` and the project due; the last
phase is a narrow rail (done titles with `done Nd ago` at ≥ 100 cells, `✓N` below or collapsed).
Every column's open high cards ride ONE band on top, each naming its project on row 2. The board
fits the panel: whole bands are windowed from the earliest one that still draws the selection and
a last row says what is folded (`▼ 2 below: Data Warehouse (4 open), Ops & Security (5 open)` —
the approved frame's own row). Renderer and navigator read one seat, `kanban_plan`, so the cursor
walks what is drawn. The re-render over the oracle board reproduces `out/R-1b-118x30.txt` /
`-80x24.txt` cell for cell apart from the spine (D-306) and the head (shipped chrome, LLR-301.3);
title readability rises from 7.3 to 11.8 characters (0 → 13 in full) at 118×30 and from 1.0 to 6.2
at 80×24. Found on the way and fixed: rich drops the backslash before ANY bracket and prints a
trailing backslash twice when spaces follow — `_literal` now writes markup that prints a cut piece
exactly (the hostile titles of TC-302; `title_markup` shares it).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-301.1, LLR-301.2, LLR-301.3, LLR-302.1, LLR-303.1, LLR-304.1, LLR-305.1, LLR-309.1, HLR-307 | NEW `_literal`, `_title_piece`, the `KANBAN_*` constants, `KanbanBand`/`KanbanPlan`, `kanban_plan`, `kanban_nav`, `kanban_card` and its helpers, `_band_rule`, `_rail_cells`, `_fold_row`; `_kanban_grouped` rewritten (returns `(rows, pinned)`); `_fit_indicators` escapes its tokens; `_windowed_header(n=)`; the grouped `nav_model` branch reads the seat; `_kanban_column_rows`, `_col_junctions` removed |
| `tests/test_kanban_readable.py` | test | HLR-301, HLR-302, HLR-303, HLR-304, HLR-305, HLR-307, HLR-309, LLR-301.1, LLR-301.2, LLR-301.3, LLR-302.1, LLR-303.1, LLR-304.1, LLR-305.1, LLR-309.1 | NEW: AT-301 ×3, AT-302, AT-303, AT-305, AT-307 ×2, TC-301 ×62, TC-302 ×43, TC-303, TC-304 ×7, TC-305, TC-306 ×4, TC-307 ×3, TC-308 ×7, TC-311 ×7, TC-313 |
| `tests/kg_board.py` | fixture | HLR-301 | the prototype's readability metric (`readability`, `body`), re-derived for the tests (P2 Q-3 form) |
| `tests/test_app.py` | test | HLR-303, HLR-304, HLR-305, LLR-301.1 | reverse census: `_painted_kanban` reads band rules; 8 nodes re-pointed (see §4) |
| `tests/test_kanban_priority.py` | test | HLR-305 | reverse census: HLR-003's per-column band → the board-wide band (2 nodes, D-313) |
| `tests/test_prism_laws.py` | test | HLR-303 | reverse census: band rules cross the divides past their text |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 5 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_kanban_readable.py tests/test_kanban_priority.py tests/test_app.py tests/test_prism_laws.py
python -m pytest -q -p no:cacheprovider
python .dev-flow/2026-10-02-batch-03/evidence/capture.py .dev-flow/2026-10-02-batch-03/evidence/captures inc001
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | `_kanban_widths` (TC-305), `_wrap_title`/`kanban_card` at every width 0..40 (TC-302), `_due_fact` (TC-306), `_literal` through TC-302's hostile titles | 44 passed (TC-302 ×43, TC-305) |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-301..TC-308, TC-311, TC-313 | 92 passed (TC-301 ×62, TC-303, TC-304 ×7, TC-306 ×4, TC-307 ×3, TC-308 ×7, TC-311 ×7, TC-313) |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-301 ×3, AT-302, AT-303, AT-305, AT-307 ×2 | 8 passed |

Gate run on the frozen round-2 tree: `python -m pytest -q -p no:cacheprovider` → **1821 passed in 306.79 s, exit 0**
(`evidence/inc001-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the base tree (`git archive HEAD`) with `tests/test_kanban_readable.py` overlaid; then the battery on the increment tree |
| Where it ran | scratch exports in the session scratchpad, never the live checkout |
| Transcript | `evidence/inc001-red-on-base.txt` (79 failed, 62 passed); `evidence/inc001-mutations.txt` |
| Restore proven by | the battery's per-mutant sha256 check (`views.py` restored to its pre-mutation digest every time) |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 141 on base (the round-1 file) |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | on base: the 60 arms of `test_TC_301_nav_is_the_draw_order` (an F-3 PIN — the shipped seat held it; KILLED by M10), `test_TC_301_the_arm_set_is_complete` (a guard of the input set), the 118×30 arm of `test_TC_311_every_selection_is_drawn_inside_the_panel` (KILLED by M12, M13) |

| Field | Value |
|---|---|
| **RED counterfactual** | 79 nodes RED on the base tree for the specified reasons (no `kanban_plan`/`kanban_card`; one-row cards; 18 per-column headers; a full-width Done column; per-column `── high` dividers; a 30-row render that names nothing) · `evidence/inc001-red-on-base.txt` · the PINs KILLED by M10, M12, M13 · restore digests in `evidence/inc001-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 28 of 28 KILLED (`evidence/inc001-mutations.txt`, `inc001-mutations-tail.txt`; harness `evidence/mutate.py`; specs `mutants_inc001.json`, `mutants_inc001_r1.json`): M1 unescaped pieces · M2 no wrap · M3 `⛓N` after the due · M4 no `┈` · M5 equal widths · M6 crossings off by one · M7 the 100-cell boundary · M8 the rail oldest first · M9 highs drawn twice · M10 nav walks the band last · M11 the prototype's selection-first window · M12 the window ignores the selection · M13 the fold row clips its `▼` side (round 1: SURVIVED → the node rewritten, F1; round 2: KILLED on the 80×24, 80×22, 40×22 arms, the 118×30 arm green by design — nothing folds on both sides there) · M14 the near due in the accent · M15 separators off the frame tone · M16 no tag · M17 first word always · M18 the rest kept with no room · M19 markers count the rail · M20 the open count drops the lifted highs · R1 groups by name only · R2 archived counted · R3 the fold row unescaped · R4 the fold one row early · R5 the badge at 8 cells · R6 the head rule misses the rail · R7 the narrow age from the oldest · R8 tags by characters. Every restore digest OK; arms that stayed green under a kill are named per mutant in the transcripts |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `kg_board.readability` (the metric) | the shipped render | 7.3 / 0 full at 118×30 → AT-301 RED on base |
| `is_rule` (band-rule detector) | the shipped per-column `▐ name` headers | no rule found → TC-306/AT-302 RED on base |
| `FOLD` (fold-row detector) + the plan-derived fold oracle | mutant M13 (the `▼` side clipped) | `▼ 3 below` missing → KILLED (round 2) |
| the TC-302 hostile set | the first `_literal` (bracket backslash) | `\[b]z` row 6 cells at `wc` 5 — the defect it found |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the kanban's rendered `Text` | plain rows and spans of `render_view("kanban", …)` | TC nodes passed |
| the painted board in the running app | `#board` `render()` spans (`rgb(…)` form) and the compositor's strips (the selection's `reverse`) | AT-301/302/303/305/307 passed |
| the frames the operator compares | `evidence/captures/inc001-kanban-*.txt` against `out/R-1b-*.txt` | equal but for the spine glyph and the head row |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on base | `.dev-flow/2026-10-02-batch-03/evidence/inc001-red-on-base.txt` | `1a5dc67b3bbef97dfbb968f831eb922e03624e70f133217f93e7907742542f4e` |
| mutation battery M1–M16, R1–R8 (round-2 tree) | `.dev-flow/2026-10-02-batch-03/evidence/inc001-mutations.txt` | `c6e7ab444e6235e6c9b1c041b3758da3c08aa32038d74b307913ac4e058d14d7` |
| mutation battery M17–M20 (site moved by the F3 fold) | `.dev-flow/2026-10-02-batch-03/evidence/inc001-mutations-tail.txt` | `4c8c093cf7fed8f57bd90092a8bbc1d55e9af452fbf65ae993bf882eb1555cce` |
| battery harness | `.dev-flow/2026-10-02-batch-03/evidence/mutate.py` | `e712e3db18980130c3c081694090368feb9134e12afa0051a024a216710f3755` |
| mutant specs | `.dev-flow/2026-10-02-batch-03/evidence/mutants_inc001.json` | `9b8d60811f8ca52b0592d5bccdfe90535707a0a7a7ca22de2d8e05449a6d0de6` |
| mutant specs, tail | `.dev-flow/2026-10-02-batch-03/evidence/mutants_inc001_tail.json` | `6ff9492e5aa1c3b2d8f19b36e7e3aca2a204488293eb43dd12c40cd82bfecc46` |
| mutant specs, review round 1 | `.dev-flow/2026-10-02-batch-03/evidence/mutants_inc001_r1.json` | `7c08399bd31d6ad20d9cdbbb66caa166e718e5cc645e3bac2a30d328744b31e1` |
| spec generator | `.dev-flow/2026-10-02-batch-03/evidence/make_mutants_inc001.py` | `9a74bd559cb76938d75b1f504c9431c9dbd517749f3d8169cebef725c3c09490` |
| spec generator, round 1 | `.dev-flow/2026-10-02-batch-03/evidence/make_mutants_inc001_r1.py` | `71558e517ca466cf33d433422ebca6f85adaa0ec0ba463e3449b744233fe0aba` |
| reverse census (new views.py, old tests) | `.dev-flow/2026-10-02-batch-03/evidence/inc001-reverse-census.txt` | `37dbb82f86f4d8b0cb4d61311840e56115c78db605d14a65dfd1e605fc17bb48` |
| gate run | `.dev-flow/2026-10-02-batch-03/evidence/inc001-green.txt` | `b3f8421a0da821275422729c911b56bfd7983a22f8558fb8d3ce87e37f31a9ed` |
| capture recipe | `.dev-flow/2026-10-02-batch-03/evidence/capture.py` | `f425a4f3588f7abd41ccca8a9c0b9d3e03eeca3749e6e9c103e9dc1cabd18faa` |
| kanban 118×30 | `.dev-flow/2026-10-02-batch-03/evidence/captures/inc001-kanban-118x30.txt` | `80f424869159c14211d005cdc77b3f0bfe1e321adc4d47278b0c2a4709b1e6a2` |
| kanban 80×24 | `.dev-flow/2026-10-02-batch-03/evidence/captures/inc001-kanban-80x24.txt` | `c327a949a00658b6ce88f2d6026188fde40a3b9f7121358b68c636823a1c3be9` |
| kanban 80×22 | `.dev-flow/2026-10-02-batch-03/evidence/captures/inc001-kanban-80x22.txt` | `42c9dfec2ec84cf6dff50e8f031f0f378de24119a6cbc0dfb84ca0d666a94f74` |
| readability after | `.dev-flow/2026-10-02-batch-03/evidence/captures/readability-inc001.txt` | `8df66a00d9b24a15fe6a92e80414e1ef04e8ab105bc513f31858ca32c9c3d972` |
| readability before | `.dev-flow/2026-10-02-batch-03/evidence/captures/readability-base.txt` | `d6b9c90dfe11b29ed47834df67340f0dbf82498036b8343f2bc7411a8ec556a7` |
| premise probes | `.dev-flow/2026-10-02-batch-03/evidence/p0-probes.txt` | `16d294f0a1f58bfd5e59d5ecda118f68495a83ca5e5593363d6a0f27fa340874` |

| Field | Value |
|---|---|
| **Evidence files** | 18 artifacts under the declared home, each cited with the digest of its stored bytes; the kanban captured as SVG + text at panels 118×30, 80×24, 80×22 (`captures/inc001-*`, base in `captures/base-*`) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no accent run on the kanban" (AT-305) and "no `▐` in a card cell" (AT-302, TC-306) |
| If the result is an ABSENCE, what made the search wide enough | every span of the painted board at two terminal sizes; every row of the render |
| Guard labelled as protecting a CONCLUSION, not a behaviour | AT-305's `no tone readable: vacuous` guard; `test_TC_301_the_arm_set_is_complete` |
| Conjunctive criteria: one mutation per conjunct | M14 (accent due), M15 (separator tone) |
| Synthetic instance of the absent case | mutants M14, M15 |
| **Positive control for every probe that returned an ABSENCE** | AT-305 asserts the frame tone IS readable in the same spans, and the soon tokens amber |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | the full suite with the NEW `views.py` and the OLD tests (`evidence/inc001-reverse-census.txt`) | 57 failed / 1620 passed: 50 product nodes (11 distinct) rewritten in place, each keeping its law or carrying a stated supersession — `test_kanban_priority.py::test_band_is_drawn_and_nav_walks_the_draw_order` ×40 and `::test_a_card_raised_to_high_joins_the_band_and_keeps_the_cursor` (HLR-003's per-column band → the board-wide band, D-313); `test_app.py::test_kanban_parity_painted_text_oracle`, `::test_kanban_group_cycles_headers_and_membership`, `::test_kanban_collapse_toggles_the_terminal_phase_and_restores`, `::test_kanban_collapsed_column_shape_and_nav_exclusion` (HLR-007's `✓ N` row → the rail's `✓N`, `_kanban_column_rows` retired), `::test_kanban_windows_phases_when_they_dont_fit`, `::test_kanban_aging_token_renders_only_for_dated_open_cards` (the age rides row 2), `::test_matrix_presentation_nav_ignores_the_modes_like_the_render`, `::test_right_moves_to_next_column_first_task` (the app's width draws the rail); `test_prism_laws.py::test_the_rule_crosses_exactly_where_the_columns_divide` (band rules cross past their text); 7 environment-only (the scratch export has no git history or hook: `test_no_live_board` ×1, `test_precommit_gate` ×1, `test_scratch_cannot_be_committed` ×5) — green in the live checkout |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` | did not fire |
| B4 artifact produced here is consumed elsewhere | `line_map` → `app._scroll_selected_into_view`; `nav_model` → `app._nav_columns` | AT-303/AT-307 drive the keys; F2 (the `/` filter) routed to increment 002 |
| A3 | interface consumed by another module changed | `render_kanban`, `nav_model` signatures | unchanged; `_kanban_column_rows` (tests only) removed |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (11 product nodes rewritten in place), B4 fired (AT-303, AT-307), B2/B3/A3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| user text printed through the new kanban code | every `escape(`/`_literal(` site in the new functions | `grep -n "escape(\|_literal(" taskboard/views.py` over `kanban_plan` … `_fold_row` | 5 | 5 (`_title_piece`, `_fit_indicators`, `_band_rule`, `_fold_row`, rail titles via `_title_piece`) | the header's focus name keeps `escape` (shipped, whole string, a tag follows) |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1821 = 1677 − 0 + 144` ✓ (the 144 nodes of `tests/test_kanban_readable.py`; the 11 census rewrites are in place, net 0).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` · round 1: `BLOCK-UNTIL: F1` (HIGH: the UX-15 both-counts assertion could not go RED; M13/N20 survived) with F2–F12 (MEDIUM: F2 the `/` filter nav/draw gap, F3 character-wise tags, F4 the 1-phase board, F5 missing fold arms, F6 evidence off the final tree; LOW F7–F12) — its own 20-mutant battery (10 survived) · folded: F1 the node derives what folded from the plan (+ a 40×22 arm), F3, F4, F5, F7, F8, F9, F12 in code and tests, F6 re-run on the final tree, F2/F11 routed to increment 002, F10 accepted · round 2 over the frozen tree: `OK to advance`, F1 discharged by re-reading and by M13/N20/N20c KILLED, 11/11 of its mutants KILLED; F13 (LOW, the prism band-rule anchor) → increment 002 |

## 5 · Risks

- **Open F-3 gap under a `/` filter (code review F2):** the cap makes the grouped nav depend on the panel height; `render_view` draws a filtered kanban two rows shorter while `app._nav_columns` asks with the full height, so at panels 12, 13, 20, 21 nav and draw can disagree (`down` skips a card). Fixed in increment 002 (D-312) with filtered arms.
- A band taller than the panel is drawn alone and scrolls; its row 2 can fall below the fold (declared, §6.3).
- The provisional visual decisions PV-1..PV-7 ship before the operator's verdict on the captures.

## 6 · Pending items / spec deviations

- LLR-302.1 amended (LED .17): the frames' proportional width rule, the floor-first split as its fallback (§6.5).
- `kanban_plan` repeats `_phase_window`'s window arithmetic over the open phases (code review F10, accepted) → BACKLOG cleanup at close.
- `_assert_kanban_parity`'s `+N more` regex will also see 002's `+N more ↓` → re-scoped in 002 (F11).

## 7 · Suggested next task

Increment 002 — the cap's tests, the copy, the cursor off undrawn done work, the filtered nav height (HLR-306, HLR-308, HLR-310, D-312).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_kanban_readable.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `_kanban_widths`, `_wrap_title`, `_literal`, `_due_fact` (§4) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | `render_kanban`, `nav_model` signatures unchanged |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | ids in docstrings; nodes collected |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
