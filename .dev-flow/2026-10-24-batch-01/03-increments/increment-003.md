# Increment 003 — HLR-2605, HLR-2606 · `the editor Select and the # manager`

| Field | Value |
|---|---|
| Batch | `2026-10-24-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2605` / `LLR-2605.1` · `HLR-2606` / `LLR-2606.1`, `LLR-2606.2`, `LLR-2606.3` |
| Acceptance | `AT-2601` minted here · `AT-2604` minted here — white-box `TC-2605`, `TC-2606`, the `TC-2407` inventory law |
| Agent | `software-dev` (spawned coder) |
| Date | `2026-10-24` |

## 1 · What changed

The editor gained the milestone-class Select of variant A and `#` gained its manager. `TaskModal` composes a Textual `Select` (`#f-mark`) in `#task-chips-what` directly after `#f-milestone` whenever the marks directory holds classes: options `none` and every class — each a `Text.assemble` of the shape in the class colour and the name in the ink tone, never markup — the task's current class selected, no `+ new class…` option (ARCH-4's declared drop); `alt+m` (a priority binding, in `TASK_KEYS` at index 1 per the round's `EDIT_KEYS`) focuses it and opens the overlay. The saved task carries the chosen class id, or no `mark` key for `none`; the write happens only when the operator changed the Select from its composed value (Textual posts `Select.Changed` on mount, so dirty-event tracking was unsound — found when AT-2607 regressed), so an untouched edit keeps the field, an id the directory lost included, and unticking `milestone` never touches it. An empty directory composes no Select: the editor, its tab walk and its key line draw exactly as before (UX-5's "an empty directory"). `modals.MarkForm(cls_id=None)` is the manager's form: the name `Input`, the shape row over `SHAPES` alone (the round's `ShapeRow` — NO `◆` choice; LED .45 + the code-review F1 fold, LED .46: a saved class can never carry `◆`; the glyph lives in the Select's `none` option and the manager frame), the colour row over `COLOURS` (←→ stepping, the shape row wearing the chosen colour), a live open/late/reached preview of the mark, Save/Cancel, the key line `alt+n name alt+c colour alt+h shape alt+s save esc cancel`, the modal-keys law. The form writes the directory itself (a refused write says `The marks directory was not saved: <reason>` and keeps the form — LLR-2606.2's "form kept"); a blank name says `A class needs a name.`; a save dismisses with the class's id. `app.MarksManager` is a full `Screen` (the `PeopleDirectory` pattern): the pure `views.render_marks` frame with live per-class `(open, all)` counts read once at open over `registry.active()`; `up,k`/`down,j` move, `space` toggles `hidden` (persisted in `marks.json`, the board beneath refreshed — it reads `board.marks` live), `n`/`e` open the form (edit keeps the id), `esc` AND `#` close; `d` and `↵` are inert and un-named (out of scope, asserted absent). `keymap` declares `#` (`number_sign`, `Milestone classes`, global, `bar=False` like `@`); `?` and the palette list it; `check_action` lets it act from the main screen and the home, refuses it over any modal (a pushed modal holds its own keys — the editor's focused field consumes what it types), and refuses every seat action but `quit` while the manager holds the keys (architect A-9). `taskboard.tcss` carries the Select's width and its 24-cell overlay.

## 2 · Files modified

⚠ **SOURCE count: 4 / 4 — AT THE CAP.** It could not be cut smaller: `render_marks` already moved to increment 002 (D-4, the ARQ's A-1 fold), and the Select, the form, the manager and the key each own a file — the minimum wiring of HLR-2605/2606 is exactly `modals.py` + `app.py` + `keymap.py` + `taskboard.tcss` (the last only the Select's two rules). The PDR carried this ⚠ (architect ARCH-1 / ux F-3).

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | LLR-2605.1, LLR-2606.2, LLR-2602.1 | `TASK_KEYS` + `("alt+m","mark")`; the variant-A Select (`#f-mark`, conditional compose, Text-piece options, value-change-only save); `MarkForm` + `_ChoiceRow`; `mark_option_text` |
| `taskboard/app.py` | source | LLR-2606.1, LLR-2606.3 | `MarksManager`, `mark_counts`, `action_marks_manager`, `check_action` gating, `marks=` at both editor call sites |
| `taskboard/keymap.py` | source | LLR-2606.1 | the `#` seat entry (`number_sign`, `bar=False`) |
| `taskboard/taskboard.tcss` | source | LLR-2605.1 | `#f-mark` width + `SelectOverlay` width |
| `tests/test_marks_manager.py` | test | HLR-2605, HLR-2606 (TC-2605, TC-2606, AT-2601) | 18 nodes (new file) |
| `tests/test_modal_keys.py` | test | HLR-2606, AT-2604 (D8) | the INVENTORY `MarkForm` row + `test_AT_2604_...` (2 params) |
| `tests/test_keymap.py`, `tests/test_readme.py` | test | HLR-2606 (the README↔seat law) | `#`↔`number_sign` spelling maps |
| `README.md` | doc | the README↔seat law | one `#` key-table row (004 owns further prose) |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** ⚠ at the cap, the reason above |

## 3 · How to test

`env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_manager.py` (18 nodes; `-k "AT_2601 or TC_2605"` / `-k "TC_2606"` for the contract's selectors); `tests/test_modal_keys.py` (34 nodes, `-k AT_2604`); the close suites (`evidence/suite-003.txt`, 89 passed); the touched batch (`evidence/suite-003b.txt`).

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0/A | TC-2605 (5), TC-2606 (10), the TC-2407 inventory law + AT-2604 (2 params) | 16 + 34 passed (`suite-003.txt`) |
| B | `test_AT_2601_a_class_is_created_and_survives` (2 sizes — `# n name shape colour alt+s`, `alt+m` in the editor, restart, the gantt draws the class glyph in its colour) | 2 passed (`suite-003.txt`) |

| Field | Value |
|---|---|
| **RED counterfactual** | `taskboard/modals.py` `TaskModal.on_mount` — the initial focus moved off the title field — made `test_TC_2606_hash_over_a_modal_does_nothing` fail (the pressed keys bubble past the editor into the seat: the modal no longer holds its own keys) · `evidence/mutation-003.txt` (arm 14) · restore digest `947d90f5ca73a088b55d8d8ce0de7f9ef2b8f251fe3d973667372d480040d7bb` |
| **Mutation verdicts** | 17 arms over the 16 new nodes (the manager-lists and AT-2601 nodes have 2 params; AT-2604 runs from `tests/test_modal_keys.py`): **17/17 KILLED · 0 SURVIVED · 0 CRASH/BAD** · every restore proven by hash · `evidence/mutation-003.txt` · arms that stayed GREEN: none. Note the hash-over-modal arm needed three honest attempts: the gate-opening mutation is structurally inert while the editor's focused `Input` consumes `#` (probed: `action_marks_manager` never fires) — the landed arm moves the initial focus so the keys bubble, which is the reachable path that falsifies "a pushed modal holds its own keys". |
| **Instrument RED-proof** | none — no instrument beyond the suite |
| **Emitted-form assertion** | none — this increment emits no artifact |
| **Reverse census** | 5 probes: B1 `grep -rl "TaskModal\|TASK_KEYS\|check_action" tests/` — the touched suites re-run (`suite-003.txt` 89 passed, `suite-003b.txt` `8b6f6f506e769c6449101768ae3a406b99e3cd20aa0cc4b4174c1ed7f9dbd52e`); B2 no file moved; B3 no golden capture; B4 `marks.json`/`board.marks` consumed by every later start — TC-2606's persistence arms; A3 no other module — 0 foreign hits (`grep -rl "MarkForm\|MarksManager" tests/` → the new/touched suites only) |
| **Correction population** | none — no correction |
| **Frozen interfaces** | people.py, boards.file_lock/keep_aside, models.write_atomic/clean_strings untouched; `views.py` untouched by 003 (F4's `object` typing stays, declared); the section-3 exclusion sites byte-identical — verified in the diff the code-reviewer reads |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-24-batch-01/evidence/suite-003.txt | 4b6b9c351ec267920cb007eb10ad28083c8cf093f6058baa6775694050f01c48 |
| suite-003b.txt | .dev-flow/2026-10-24-batch-01/evidence/suite-003b.txt | 8b6f6f506e769c6449101768ae3a406b99e3cd20aa0cc4b4174c1ed7f9dbd52e |
| mutation-003.txt | .dev-flow/2026-10-24-batch-01/evidence/mutation-003.txt | a6f959148c3f5b7d146c491c8ef067fd6ef6821e75878bd25038e4b8fcfc8f62 |

| Field | Value |
|---|---|
| **Evidence files** | `3 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · APPROVE-WITH-CONDITIONS → approved, 0 HIGH (F1 the form has no `◆` choice — the record claimed one; folded as LED .46, option (a): the form matches the round's `ShapeRow`, `◆` lives in the Select's `none` option and the manager frame; discharged by the same reviewer); the frozen set named untouched; the packet claims verified against the bytes; the modals.py regeneration proven faithful by the battery restore hash |

## 5 · Risks

(1) `Select.Changed` fires on mount — the save compares against the composed value instead of tracking events; a future Textual change to init semantics is covered by AT-2607. (2) The one-row chip threshold rises by `MARK_SELECT_W = 17` when the Select is composed — measured reasoning, not re-swept (the sweep suite uses an empty directory and stays green; the folded layout at 80×24 is asserted in the painted overlay arm). (3) `MarkForm` writes via `self.app.marks` — the form is app-coupled at runtime (the LLR's `cls_id`-only signature is kept). (4) The counts read every active board at open — the people view's precedent, no latency criterion. (5) `#`/`@`/`A` are now all refused over modals (was: only the new gate — the others previously fired; the new gate is the architect A-9 reading and is asserted for `#` and the seat keys).

## 6 · Pending items / spec deviations

AT-2601 and AT-2604 are minted here (C-18: exactly one node each); AT-2605/AT-2606 remain for 004. Seven declared interpretations from the implementer's report: the refused write lives in the form (LLR-2606.2's "form kept"); `TASK_KEYS` position per the proto oracle (EDIT_KEYS[:1] + alt+m); the untouched-edit composed-value comparison (AT-2607 preserved); `registry.active()` counts; `has_focus_within` for `alt+m`; the README row (law-driven, docs file — 004 owns further prose); F4 stays deferred (`AgendaItem.board`/`PersonItem.board` remain `object` in views.py — out of 003's scope, named again here for 004). **Recovery note:** `taskboard/modals.py` was once reverted by an orchestrator mishap (`git checkout --`) and regenerated byte-equivalent by the implementer (same 239-line diff footprint; 89 passed re-verified) — the battery above ran against the regenerated tree. No silent spec edit.

## 7 · Suggested next task

Increment 004 — `views.legend_strip`/`legend_strip_project` (only the drawn classes, then `N hidden`), `views._hide` + `present_tasks_m`, `views.matches_m`/`filter_bar_m` wired into `matches`/`filter_bar`; the `?` help, the gantt details line and the README prose; tests `tests/test_legend.py` (additions, mints `test_AT_2605_hide_and_the_legend`) and `tests/test_readme.py`; 3 source files (`views.py`, `app.py`, `README.md`).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ⚠ | §2: 4/4 at the cap, the reason declared |
| 2 | Tests in this increment | ✓ | 18 new nodes + the modal-law rows |
| 3 | Layer 0 where it applies | ✓ | §4 (the form/save arms; the mount wiring) |
| 4 | RED counterfactual | ✓ | §4, `mutation-003.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b: approved, F1 discharged |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | §4 + the diff |
| 9 | Coverage verified on disk | ✓ | `suite-003.txt`: 89 passed |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence |
| 11 | Mutation verdicts | ✓ | §4: 17/17 KILLED |
| 12 | Instrument RED-proof | ✓ | §4: none, declared |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4: none, declared |
| 15 | Independent review | ✓ | §4b: PASS, fold discharged |
| 16 | Evidence files | ✓ | §4: 3 digests |
