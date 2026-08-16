# Increment 008 — R-06 + R-07 · Card aging token (`·Nd`) and terminal-phase collapse (`z`)

| Field | Value |
|---|---|
| Batch | `2026-08-14-batch-04` |
| Increment | `008` (Increment 4 of the batch) |
| Lane | — (batch not forked) |
| Requirement(s) | R-06 / HLR-006 / LLR-006.1 · R-07 / HLR-007 / LLR-007.1 · §3.0 key-registration contract (`z` row) · §6.5 AMD-02 (collapse targets THE LAST phase, from anywhere, no selection; nav skips the column entirely) · D-9 · 01b F-7 (ruled: selection relocates) |
| Acceptance | AT-011, AT-012 (Layer B, Pilot) · TC-009 (Layer A: aging token N=0/None/done/tone/width-shedding) · TC-010 (Layer A: collapsed column shape + nav exclusion + seat input; relocation pin folded into AT-012(b), V-5) |
| Agent | `software-dev` (supervised-incremental-development) |
| Date | 2026-08-15 |

---

## 1 · What changed

**BLUF: kanban cards now confess how long they have been sitting — a `·Nd` token computed from the `phase_changed` stamp through the existing `days_in_phase` seat, only while the task is open and the stamp is known — and `z` collapses THE LAST phase column to a single `✓ N` summary row, with the navigation model treating that column as nonexistent (absent, not empty) and the cursor relocating out of it, so nothing the board does not draw can ever hold the selection.**

- **Aging (HLR-006/LLR-006.1).** `card_cell` (`taskboard/views.py:301`) gained a defaulted `today` parameter (sole production call site `views.py:2329`, grep-verified; the legend renders through `legend_entries`, never `card_cell`) and appends the token `·{N}d` — N = `days_in_phase(task, today)` (`models.py:695`) — to its right-indicator list, only when N is not None AND the task is not done. None is UNKNOWN, never zero: an unstamped card renders no token rather than a lying `·0d` (the exact bug the models docstring warns about); done work rests. The token sits just BEFORE the archived mark in the token list, so under width pressure it sheds before the one mark that says the row is not live work (the LLR-006.1 ordering pin), and `_fit_indicators` (`views.py:280`) now measures each token at `1 + cell_len(glyph)` instead of a flat 2 cells — identical for every existing 1-cell glyph, correct for the multi-cell `·Nd` — so the card's always-exactly-`wc` contract holds at every width, the title truncating first.
- **Tone (flagged in §6):** the spec does not name a color key (02-review-architect m-6); the token wears `dim` — the house date distances already wear (`reldue_token`, `views.py:383`) — never a judging hue and never a project colour, so the `test_archive.py:581` / `test_palette_ration.py` law class cannot trip.
- **Collapse (HLR-007/LLR-007.1, §6.5 AMD-02).** The app-held session flag `kanban_collapsed` (never persisted — a working posture, §6.2 D-4) is an INPUT TO THE SEAT on both paths: `_kanban_column_rows` and the kanban `nav_model` branch both pass it into `kanban_order` (the Inc-006 seed, `collapsed=True` → no groups), positionally gated to `i == len(board.phases) - 1` — the rule is positional, never name-matched, so a custom-named terminal phase still collapses. The render side then adds exactly one `(markup, None)` row — `c(fit(f"✓ {len(tasks)}", wc), "done")`, N the phase's visible task count recomputed from the bucket, the existing non-selectable row convention, no new row kind; the `✓` wears the `done` house, which on the terminal phase never lies. The nav side SKIPS the phase: the column is ABSENT from the nav model — a genuinely EMPTY phase keeps its empty column (the ux B-1 distinction, pinned in TC-010 with an empty-Review fixture).
- **`TaskboardApp`:** `kanban_collapsed` state beside `kanban_sort`/`kanban_group`; `action_collapse_toggle` — view-guarded no-op outside kanban (the `action_toggle_presentation` precedent), needs NO selection, flips the flag and, on collapse only, relocates a selection inside the terminal phase to the nearest non-empty column's FIRST card (the exact `action_hmove` landing rule; `_nav_columns()` is consulted AFTER the flip, so the terminal phase is already absent); `collapse_toggle` joins `BOARD_ACTIONS` (the aperture drop); the flag is threaded through `refresh_view`, `_repaint_flow` and `_nav_columns`.
- **`keymap.py`:** `Key("z", "z", "collapse_toggle", "Collapse", views=("kanban",))` beside its sort/group siblings, before the arrow block (AMD-03 placement rule).
- **README keybinding table:** the `z` row after `g`, "Kanban only:" convention (enforced by `test_the_readme_keybinding_table_matches_the_seat`).

The matrix presentation is deliberately untouched — the Inc-006 precedent for sort/group, inherited unchanged (see §6).

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count. SOURCE: 3/4.**

| File | Kind | Change |
|---|---|---|
| `taskboard/views.py` | source | `_fit_indicators` (:280) measures real token widths; `card_cell` (:301) gains `today` + the `·Nd` token; `_kanban_column_rows` (:2315) gains `collapsed` (one `✓ N` row through the seat); `_kanban_grouped` (:2356), `render_kanban` (:2449), `render_view` (:2474), `nav_model` (:2560) gain defaulted collapse pass-throughs; the nav kanban branch skips the terminal column entirely |
| `taskboard/app.py` | source | `kanban_collapsed` state, `action_collapse_toggle` + `_relocate_out_of_collapsed`, 1 `BOARD_ACTIONS` member, 3 call-site pass-throughs |
| `taskboard/keymap.py` | source | `z` entry, `views=("kanban",)`, before the arrow block |
| `README.md` | docs (outside count) | `z` keybinding row |
| `tests/test_cells.py` | test | 2 new nodes (TC-009 + width/shedding limb) |
| `tests/test_app.py` | test | 6 new nodes + 1 shared fixture (`_aging_board`) |

`taskboard/models.py` — **NOT touched.** `days_in_phase` is reused as-is (HLR-006 pins the reuse); collapse state is session-level by spec (§6.2 D-4), so no settings persistence was invented.

---

## 3 · How to test

```bash
python -m pytest tests -q --deselect tests/test_app.py::test_win_clipboard_roundtrip   # full gate: MUST be 0 failed
python -m pytest tests/test_app.py -k "aging" -q                                       # AT-011
python -m pytest tests/test_cells.py -k "aging" -q                                     # TC-009 (LLR-006.1's own selector)
python -m pytest tests/test_app.py -k "collapse" -q                                    # AT-012 + TC-010 + registration/guard/aperture
python -m pytest tests/test_app.py -k "collapse or parity" -q                          # LLR-007.1's selector (adds the TC-006 oracle)
python -m pytest tests/test_momentum.py -q                                             # days_in_phase seats stay green
python -m pytest tests/test_keymap.py -q                                               # four-seat enforcement + README table
grep -n "kanban_order(" taskboard/views.py                                             # convergence probe: exactly 2 consumers
PYTHONIOENCODING=utf-8 python prototypes/verify_aperture.py                            # aperture law (new key + BOARD_ACTIONS member)
```

---

## 4 · Test results

**One complete run, post-restore, after both RED cycles. Tail read from THAT run's own output:**

```
........................................................................ [ 97%]
....................                                                     [100%]
812 passed, 1 deselected in 65.05s (0:01:05)
```

The deselected node is `tests/test_app.py::test_win_clipboard_roundtrip` — the known-environmental OS-clipboard lock documented in increment-007 §4 (unchanged handling: deselected per the batch gate convention; the clipboard path is untouched by this increment).

`verify_aperture.py` — final lines of the same verification pass (new `z` key + `collapse_toggle` in `BOARD_ACTIONS`):

```
  [PASS] the hero under test is the DEADLINE's reading, and its detail is the user's TITLE — the reason `hero.py` escapes at all  deadline: '[URGENT] rotate keys'
  [PASS] the hero leg is not vacuous: some languages really do compose the detail line into the panel at 118x34 (the rest are a regression guard, and this check is what would notice the last one going away)  3/10: ['swiss', 'industrial', 'darkside']

ALL PASSED
```

Convergence probe (pass condition: the seat has exactly TWO consumers; `card_cell` exactly ONE production caller):

```
2245:def kanban_order(board, tasks, show_archived, *, group="project",
2323:    for name, color, items in kanban_order(board, tasks, show_archived,   ← render path (receives collapsed=)
2586:            groups = kanban_order(board, bucket, show_archived,           ← nav path (receives collapsed=)

301:def card_cell(task: Task, board: Board, wc: int, selected: bool, *,
2329:            rows.append((card_cell(t, board, wc, t.id == selected_id,    ← sole production call site
```

| Layer | Nodes | Result |
|---|---|---|
| **A · white-box** | `test_card_cell_aging_token_follows_the_stamp_and_never_lies` (TC-009: N=0 → `·0d`, N recomputed via `days_in_phase`, None → no token, done → no token, dim tone / no judging hue) · `test_card_cell_aging_token_sheds_before_the_archived_mark` (TC-009 width limb: exact-`wc` sweep over wc ∈ [1,40) for an aged+archived card, token shed before the archived mark at wc=5, both present at wc=30) · `test_kanban_collapsed_column_shape_and_nav_exclusion` (TC-010: exactly one `(markup, None)` row, `✓ N` recomputed and width-exact, `kanban_order(collapsed=True)` == [] — the flag THROUGH the seat —, nav == full-minus-terminal with the genuinely-empty Review KEEPING its empty column) · `test_collapse_action_is_registered_and_guarded` (§3.0 four seats + before-arrow placement) | 4 passed |
| **B · black-box** | `test_kanban_aging_token_renders_only_for_dated_open_cards` (AT-011: `·5d` on the dated card's own painted cell, no `·\d+d` on the unstamped or the done card — assertions confined to the card's column segment so a neighbour's token cannot leak in) · `test_kanban_collapse_toggles_the_terminal_phase_and_restores` (AT-012 both directions: one `✓ N` row with N recomputed, terminal titles gone, other columns' painted rows identical via the 01b §4 anchor, nav absent-not-empty + collapsed-state painted/nav parity, byte-exact restore, arrow walk never lands on a terminal task; then selection walked INTO Done → relocates to Review's first card) · `test_collapse_key_is_a_noop_outside_kanban` (view guard) · `test_collapse_key_is_dead_on_the_aperture` (aperture probe for `z`) | 4 passed |

### RED counterfactuals — executed, not predicted

Two mutations, each applied in my own tree, restored byte-exact and PROVEN by hash (restore via `cp` of a hash-verified golden — NO `sed -i` — with `__pycache__` cleared after every mutation/restore cycle, C-46). Golden: `taskboard/views.py` sha256 `28584ae2a3de208934fa672614088868e9b5811f15dab43da3969c25a88033a7`, re-proven after EACH cycle.

| # | Mutation applied | Reddened node(s) | Restore proven by |
|---|---|---|---|
| A | **Aging rendered for done tasks** — the `not board.is_done(task)` guard in `card_cell` replaced by `if True:` | `test_card_cell_aging_token_follows_the_stamp_and_never_lies` (TC-009 done limb) + `test_kanban_aging_token_renders_only_for_dated_open_cards` (AT-011 done limb) RED — 1 failed in each focused run; the shedding sweep stayed green (it never exercises done) | hash → `28584ae2…` ✓, full suite re-run green (the 812-passed run above is post-restore) |
| B | **Collapse EMPTYING the nav column instead of dropping it** — `continue` became `cols.append([]); continue` in `nav_model` (an empty nav column vs a missing one — the ux B-1 distinction) | `test_kanban_collapsed_column_shape_and_nav_exclusion` (TC-010 `collapsed == full[:-1]` limb) + `test_kanban_collapse_toggles_the_terminal_phase_and_restores` (AT-012 nav-length limb) RED — **2 failed, 3 passed**; the guard/aperture/registration nodes stayed green (they never consult nav shape) | same hash ✓, full suite re-run green |

Transcript samples:

```
# A — AT-011, the done card painted its age under the mutation:
>           assert not re.search(r"·\d+d", card_of("echo")), \
                "a done card painted an age — done work rests"
E           AssertionError: a done card painted an age — done work rests
E           assert not <re.Match object; span=(26, 29), match='·9d'>

# B — TC-010, the empty column is one column too many:
>       assert collapsed == full[:-1], \
            "the nav model with collapse is not exactly full-minus-terminal"
E       AssertionError: assert [['04c3ad0f',...7d8'], [], []] == [['04c3ad0f',...9b447d8'], []]
E          Left contains one more item: []
```

### Reverse census — trigger family B (C-26, reconciled BEFORE touching the seats)

| Probe | Command | Result |
|---|---|---|
| B1 census over touched symbols | `grep -rln "card_cell\|kanban_order\|_kanban_column_rows\|nav_model\|collapse" tests/` | `card_cell` asserters: `test_archive.py:581` (archived-cell hue law — forbids project/over/soon hexes only; `dim` is lawful) and `test_palette_ration.py:180/193/194/318` (unstamped fixtures → no token; `!`/hue assertions unaffected — verified green in the full run). `collapse` hits are `collapse_runs` (span economy) and prose — unrelated. `_kanban_column_rows`/`kanban_order` kanban asserters: only Inc-006's own (all params defaulted → compile and behave identically) |
| B1 assertion-level reconciliation | read `test_archive.py:572-583`, `test_palette_ration.py:175-194,308-322` | protected by construction: the aging token cannot appear without a stamp (all those fixtures are unstamped) and never wears a forbidden hue when it does |
| B2/B3 | file moves / byte-identical goldens | did not fire |
| A3 interface consumed by another module changed | `card_cell` (+1 defaulted kw), `_fit_indicators` (private, sole caller `card_cell`), `_kanban_column_rows`/`_kanban_grouped`/`render_kanban`/`render_view`/`nav_model` (all +1 defaulted kw) | additive only — the census's 3-arg `nav_model` calls compile unchanged (full suite green); `card_cell`'s two direct test callers compile unchanged |
| occupancy/palette/span-economy/legend sweep | full `pytest tests` | all green — the token lives inside the existing width-exact cell math and the dim house; the seeded demo board's stamped cards now show `·Nd` and trip no ration/occupancy law |

### Signed-balance test ledger

`post = base − deleted + added` → `813 = 805 − 0 + 8` ✓ reconciles (8 new nodes: 2 in `tests/test_cells.py`, 6 in `tests/test_app.py`; no test edited or deleted). Gate line: 812 passed + 1 environmental deselect = 813.

---

## 5 · Risks

- **Matrix presentation + collapse diverge by inherited precedent** (flagged): exactly like sort/group in Inc-006, the nav model honors the flag always while `_kanban_matrix` ignores it — in matrix presentation with the flag on, terminal tasks are drawn (as dots) but not nav-reachable. This is the batch's standing answer to "matrix is out of scope for column-shaping"; if a PDR rules otherwise, the one-site fix is the `render_kanban`/`nav_model` call in `app.py`.
- **The `_select_first` corner** (documented, not fixed): collapsed AND zero visible tasks outside the terminal phase → relocation yields `None`, but `refresh_view`'s `_select_first` then re-selects the first visible task — a terminal, undrawn one. Reachable only on a board whose every visible task is done; **only `z` (or a data change) resolves it — arrow keys re-select the same undrawn task via `_locate → None → _select_first`** (wording corrected at Phase 4 per the Inc-008 code-review). Making shared selection machinery collapse-aware was judged out of minimal scope.
- **The kanban bar gained `z Collapse`** (~+11 cells): `test_keymap.py` is green across the sweep under the Inc-1 amended width law — EXPECTED and lawful, same trajectory as Inc-006's `s`/`g`.
- **The seeded demo board's stamped cards now show `·Nd`** — the feature working as specified; occupancy, span economy, palette ration and legend suites all measured green after the change.

## 6 · Pending items / spec deviations

- **Aging tone unspecified in the spec** (flagged — 02-review-architect m-6 named the gap): chose `dim`, the house date distances already wear (`reldue_token`, `views.py:383`); the review's one constraint (no judging-house tone, or `test_archive.py:581`'s law class trips) is honored and pinned by TC-009's tone limbs. Candidate for a one-line §6.5 amendment.
- **AT-K07's "other columns byte-equal" limb implemented as per-column painted-content equality** (flagged): a literal line-by-line byte compare is unsatisfiable BY DESIGN — the collapsed column is shorter, so the frame's rows below it shift up (reclaiming the height is the point of the feature). The executable form uses the 01b §4 painted-anchor machinery (`_painted_kanban` tuples, headers included); the BYTE-EXACT pin lives on the direction AT-012 actually pins — the restore (`board_text` equality asserted).
- **Token shed order relative to ↗/!/▤ is unpinned** (noted): the spec pins only "sheds before the archived mark"; the token sits just before it in the list, so it outlives ↗/!/▤ under pressure. A different priority among those three is a one-line reorder with an existing test limb to extend.
- **TC-010's selection-relocation pin is folded into AT-012(b)** (V-5): the relocation is an app behaviour, asserted behaviourally (walk into Done → `z` → lands on Review's first card). No standalone node; reconcile at Phase-4 id mapping.
- **No `· collapsed` header token** (considered, rejected): LLR-003.2's naming law covers sort/group MODES; the collapse is self-announcing (the column's cards are gone, the `✓ N` row is there, and the bar advertises `z`). Adding a header token would spend the kanban header's width budget on what the screen already says.
- **V-5 selector reconciliation**: HLR-006's `-k "aging"` (test_app + test_cells) and HLR-007's `-k "collapse"` / `-k "collapse or parity"` selectors all work as written against the implemented node names.

## 7 · Suggested next task

**Inc 5 — R-08 (K8 focus mode)**: `action_focus_cycle`/`action_focus_exit` on the `board.visible_projects` cycle ending in `None`, view-guarded with the AMD-03 escape-companion ruling; the `focus` parameter `kanban_order` ALREADY carries (Inc-006 seed: filters the column's tasks to one project — the same seed pattern this increment consumed for `collapsed`). The header names the focused project; the nav companion (hidden-but-navigable tasks are the F-3 trap in a new costume) comes free if the flag goes through the seat on both paths, as `collapsed` now does. Watch the Inc-007-carried question (arch m-6): whether `DOING 4/3` counts focused-only tasks — the one `phase_buckets` call in `_windowed_header` is the site.

---

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | ≤4 source files, or reason declared | ✓ | 3/4 (views.py, app.py, keymap.py); models.py deliberately untouched — §2 |
| 2 | Tests written in this same increment | ✓ | 8 new nodes — §2/§4 |
| 3 | Layer 0 written where the criterion applies | ✓ | TC-009 pure-cell units + TC-010 pure nav/column units on the seats — §4 Layer A |
| 4 | RED counterfactual captured and restored by hash | ✓ | A (done-suppression dropped) + B (empty-vs-absent nav column), golden `28584ae2…` re-proven after each cycle, `__pycache__` cleared per cycle — §4 |
| 5 | Reverse census run on every touched symbol | ✓ | B1 re-run and reconciled (archive/palette asserters safe by construction); B2/B3 non-fires; A3 additive-only — §4 |
| 6 | `code-reviewer` passed — a HIGH blocks | ⚠ | Not invoked by this agent; left for the orchestrator's review gate (declared per notice convention) |
| 7 | No file from another lane touched | ✓ | Batch not forked |
| 8 | Frozen interfaces untouched | ✓ | Every signature change is a defaulted keyword; the 3-arg `nav_model` census calls and direct `card_cell` test callers compile unchanged — §4 A3 |
| 9 | Coverage claims verified on disk, not from intent | ✓ | pytest tail pasted from one complete post-restore run (812 passed / 0 failed / 1 environmental deselect); verify_aperture `ALL PASSED` pasted; convergence probe pasted — §4 |
