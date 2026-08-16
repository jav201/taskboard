# Increment 009 — R-08 + R-09 + R-10 · Project focus (`F`/escape), due-date bump (`+` `-` `=`), session undo (`u`)

| Field | Value |
|---|---|
| Batch | `2026-08-14-batch-04` |
| Increment | `009` (Increment 5 of the batch) |
| Lane | — (batch not forked) |
| Requirement(s) | R-08 / HLR-008 / LLR-008.1 · R-09 / HLR-009 / LLR-009.1 · R-10 / HLR-010 / LLR-010.1 · §3.0 key-registration contract (`F`, `+,=`, `-`, `u`, `escape` rows) · §6.5 AMD-03 (escape companion fires ONLY on active focus in kanban) · AMD-05 (undo domain: quick keys + `x` + `d`, modal add excluded) · AMD-06 (`=` aliases `+` in ONE `"+,="` entry) · D-5 (Inbox is not a focus target) |
| Acceptance | AT-013 (focus cycle + header + escape exit + passthrough) · AT-014 / AT-015 (due bump dated/undated both directions + `=` alias + today boundary) · AT-016 / AT-016b / AT-017 (undo field-verbatim / archive+delete+modal-add domain / LIFO + empty) · TC-011 (focus cycle order, seat filter, archived drop) · TC-012 (`bump_due` unit) · TC-013 (undo stack: verbatim snapshot, stale skip, no-write on empty) |
| Agent | `software-dev` (supervised-incremental-development) |
| Date | 2026-08-15 |

---

## 1 · What changed

**BLUF: `F` cycles a project focus through the visible projects and off — the kanban renders and navigates only the focused project's tasks (the focus is an INPUT to the shared `kanban_order` seat on BOTH the render and nav paths, like collapse before it) and the header names it; `escape` leaves an active focus and is a guarded no-op otherwise, so it never eats another screen's escape. `+`/`-` bump the selected task's due date one day (undated bases on today, symmetric), with `=` aliasing `+` in ONE `"+,="` seat entry. `u` undoes the last single-task mutation from a session LIFO of pre-mutation snapshots — quick keys, archive `x`, delete `d` (same-id resurrection) — and says so when there is nothing to undo.**

- **Focus (HLR-008/LLR-008.1).** `TaskboardApp.focused_project_id` (session-level, never persisted) beside the other kanban view-state. `action_focus_cycle` walks `board.visible_projects(show_archived)` order ending in `None` (Inbox is not a target — D-5: focusing hides project-less tasks); `action_focus_exit` fires ONLY on an active focus in kanban (AMD-03). `_validate_focus` (called from `refresh_view`) drops a focus whose project left the visible set; `_select_first` is focus-aware in kanban so the selection can never rest on a task the filter hides. Both actions are view-guarded no-ops outside kanban (the `action_toggle_presentation` precedent). In `views.py` the focus threads `render_view → render_kanban → _kanban_grouped → _kanban_column_rows → kanban_order` (the Inc-006 seed at `views.py:2263` consumed verbatim) and `nav_model → kanban_order` — hidden-but-navigable is impossible by construction. `_kanban_grouped` also scopes its INPUT (WIP header counts and the `N tasks` tally describe what is drawn — decision flagged in §6) and names the focus in the existing mode-annotation seat (`· focus: Name`, user text escaped).
- **Due bump (HLR-009/LLR-009.1).** New pure helper `bump_due(task, delta, today)` in `taskboard/models.py` beside `parse_iso`: base = `parse_iso(due_date) or today` (corrupt dates read as undated, per the leniency), writes ISO text, caller saves (the `set_task_phase` convention). `action_due_bump(delta)` snapshots for undo, bumps, saves, refreshes. Selection-scoped like the other quick keys — NOT view-scoped (§3.0 marks no `views=` for `+`/`-`/`u`).
- **Undo (HLR-010/LLR-010.1).** App-held `self._undo_stack` (session LIFO — never a file format). `_snapshot(task, deleted=False)` captures the six mutable fields VERBATIM (`phase`, `phase_changed`, `priority`, `blocked`, `due_date`, `archived`) — the stamp included, or a restore would fabricate a fresh-looking card; for delete it also keeps the FULL task object and its board index. Push sites: `action_phase_move` (only when `set_task_phase` reports a real move — a clamped end records nothing), `action_prio_cycle`, `action_toggle_blocked`, `action_due_bump`, `action_archive`, `_on_delete` (post-confirm, pre-delete). Modal add records NOTHING (AMD-05); collapse/sort/group/focus are view state — outside the domain by the spec's own list. `action_undo` pops the newest entry whose task still exists — a deleted task counts as restorable (full snapshot re-inserted at its old index, SAME object, SAME id); restores fields verbatim; saves; refreshes. A purged-since-snapshot entry is skipped; an empty or fully-stale stack fires the nothing-to-undo notification and writes nothing. Undo pushes nothing itself, so `u` after `u` walks down, never oscillates.
- **`keymap.py`:** `F` (`views=("kanban",)`), ONE `"+,="` entry → `due_bump(1)` (the `"d,delete"` precedent, AMD-06), `-` → `due_bump(-1)`, `u` → `undo`, `escape` → `focus_exit` (`views=("kanban",)`, non-priority so modal/aperture escapes answer first) — all placed BEFORE the arrow block (AMD-03).
- **Latent defect found and fixed in the seat (keymap.py `render_key_bar`):** the `[` key's show rendered through Textual's `Content` markup parser as the literal `[[/]` — three phantom cells the fit math never counted — so with the bar's +8 computed cells the painted row overflowed its 118-cell widget and the last key (`→`) silently clipped, reddening `test_the_app_paints_its_keys_instead_of_a_blank_row`. Neither `rich.markup.escape` nor `textual.markup.escape` touches a bare `[` (both only neutralize tag-LOOKING sequences; measured); the fix is a local `_mshow` (`text.replace("[", "\\["]`), identity for every plain glyph. This bug predates the increment — it was simply never over the edge before.
- **README keybinding table:** rows for `F`, `esc`, `+`/`=` (one row), `-`, `u` after `z`; the enforcement test's `spelled` map gained `"+,=": "+"` and `"escape": "esc"` (the `"d,delete": "d"` mechanism, tests uncapped).

The matrix presentation is deliberately untouched for focus too — the standing Inc-006 precedent (§5).

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count. SOURCE: 4/4.**

| File | Kind | Change |
|---|---|---|
| `taskboard/app.py` | source | `focused_project_id` + `_undo_stack` state; `action_focus_cycle` / `action_focus_exit` / `_validate_focus`; `action_due_bump`; `_snapshot` / `action_undo` + `_UNDO_FIELDS`; undo push sites in `action_phase_move`, `action_prio_cycle`, `action_toggle_blocked`, `action_archive`, `_on_delete`; focus-aware `_select_first`; 4 `BOARD_ACTIONS` members; 3 call-site pass-throughs (`refresh_view`, `_repaint_flow`, `_nav_columns`); stale `action_archive` docstring updated (it claimed `x` was its own only undo) |
| `taskboard/views.py` | source | `focus` threaded through `_kanban_column_rows`, `_kanban_grouped` (+ input scoping and the `· focus:` header annotation), `render_kanban`, `render_view` (`kanban_focus`), `nav_model` (`kanban_focus` into the seat) |
| `taskboard/models.py` | source | `bump_due(task, delta, today)` beside `parse_iso` |
| `taskboard/keymap.py` | source | 5 new entries (`F`, `+,=`, `-`, `u`, `escape`) before the arrow block; `_mshow` fix in `render_key_bar` (the phantom-cell defect above) |
| `README.md` | docs (outside count) | 5 keybinding rows |
| `tests/test_app.py` | test | 10 new nodes + 1 shared fixture (`_focus_board`) |
| `tests/test_momentum.py` | test | 1 new node (TC-012) |
| `tests/test_keymap.py` | test | `spelled` map: 2 entries added (alias spelling mechanism, no law changed) |

---

## 3 · How to test

```bash
python -m pytest tests -q --deselect tests/test_app.py::test_win_clipboard_roundtrip   # full gate: MUST be 0 failed
python -m pytest tests/test_app.py -k "focus" -q                                       # AT-013 + TC-011 + registration (HLR-008 selector)
python -m pytest tests/test_app.py -k "due_bump" -q                                    # AT-014, AT-015 (HLR-009 selector)
python -m pytest tests/test_momentum.py -k "bump_due" -q                               # TC-012 (LLR-009.1 selector)
python -m pytest tests/test_app.py -k "undo" -q                                        # AT-016, AT-016b, AT-017 (HLR-010 selector)
python -m pytest tests/test_app.py -k "undo_stack" -q                                  # TC-013 (LLR-010.1 selector)
python -m pytest tests/test_keymap.py -q                                               # four-seat enforcement + README table
grep -n "kanban_order(" taskboard/views.py                                             # convergence probe: exactly 2 consumers
PYTHONIOENCODING=utf-8 python prototypes/verify_aperture.py                            # aperture law (4 new BOARD_ACTIONS members)
```

---

## 4 · Test results

**One complete run, post-restore, after all three RED cycles. Tail read from THAT run's own output:**

```
........................................................................ [ 96%]
...............................                                          [100%]
823 passed, 1 deselected in 66.51s (0:01:06)
```

The deselected node is `tests/test_app.py::test_win_clipboard_roundtrip` — the known-environmental OS-clipboard lock documented in increment-007 §4 (unchanged handling).

`verify_aperture.py` — final lines of the same verification pass (all four new actions in `BOARD_ACTIONS`):

```
  [PASS] the hero under test is the DEADLINE's reading, and its detail is the user's TITLE — the reason `hero.py` escapes at all  deadline: '[URGENT] rotate keys'
  [PASS] the hero leg is not vacuous: some languages really do compose the detail line into the panel at 118x34 (the rest are a regression guard, and this check is what would notice the last one going away)  3/10: ['swiss', 'industrial', 'darkside']

ALL PASSED
```

Convergence probe (pass condition: the ordering seat has exactly TWO consumers):

```
2245:def kanban_order(board, tasks, show_archived, *, group="project",
2324:    for name, color, items in kanban_order(board, tasks, show_archived,   ← render path (receives focus=)
2604:            groups = kanban_order(board, bucket, show_archived,           ← nav path (receives focus=)
```

| Layer | Nodes | Result |
|---|---|---|
| **A · white-box** | `test_focus_cycle_order_seat_filter_and_archived_drop` (TC-011: full cycle = `visible_projects` order + None and closes; seat filter `kanban_order(focus=)` exact + non-vacuous; archived-project focus drops on refresh; both actions guarded outside kanban) · `test_bump_due_dated_undated_and_corrupt_base` (TC-012: dated ±, undated ± symmetric, corrupt base today — 5 pins) · `test_undo_stack_snapshot_stale_skip_and_no_write_on_empty` (TC-013: double empty pop → 2 notifications + byte-unchanged file; snapshot verbatim incl. None stamp; purged-task entry skipped without raise) · `test_focus_due_undo_actions_are_registered_and_guarded` (§3.0 four seats + before-arrow placement + ONE `"+,="` alias entry) | 4 passed |
| **B · black-box** | `test_focus_cycle_filters_the_board_and_escape_restores` (AT-013: filter + header naming + different-project cycle + Inbox hidden + cycle-closes-to-off + escape restore + byte-identical passthrough + modal-escape shadow limb + nav companion) · `test_due_bump_moves_dated_and_undated_tasks_forward` (AT-014: JSON `today+6` / `today+1` via C-12 disk re-read + agenda token `+6d` / `+1d`) · `test_due_bump_minus_and_the_equals_alias` (AT-015: `-` dated, `=` exactly-`+` dated + undated, today→`-1d` boundary token flip) · `test_undo_restores_the_phase_and_its_stamp_verbatim` (AT-016: column back + reloaded `phase_changed is None`) · `test_undo_covers_archive_and_delete_but_not_modal_add` (AT-016b: `x`+`u` archived False; `d`+confirm+`u` SAME id + same object; modal add + `u` → notification + task stays) · `test_undo_is_lifo_and_the_empty_stack_says_so` (AT-017: blocked-before-priority LIFO, third pop byte-unchanged + notification) · `test_focus_due_undo_keys_are_dead_on_the_aperture` (aperture probe for all four keys) | 7 passed |

### RED counterfactuals — executed, not predicted

Three mutations, each applied in my own tree, restored byte-exact and PROVEN by hash (restore via `cp` of hash-verified goldens — NO `sed -i` — with `__pycache__` cleared after every mutation/restore cycle, C-46). Goldens: `taskboard/app.py` sha256 `083c23feb1b31065912e0b843ca807420e15693a8f3338247261dac46d9e0ab7`, `taskboard/keymap.py` sha256 `34acf3942ecaefcb8c01aea7d5988879a14c6a495848b5631f45a85fc57545f3` — both re-proven after the final restore (`HASHES-MATCH`), and the 823-passed run above is post-restore.

| # | Mutation applied | Reddened node(s) | Restore proven by |
|---|---|---|---|
| A | **Undo resurrects with a NEW id** — `task.id = task.id + "x"` after the re-insert in `action_undo` | `test_undo_covers_archive_and_delete_but_not_modal_add` RED — `AssertionError: the delete was not undone` / `assert None is not None`: with a mutated id no task with the ORIGINAL id exists on disk, so the id-equality family trips at its first limb | hash → `083c23fe…` ✓, node green on re-run |
| B | **Modal add becomes undoable** — `_on_task_added` pushes an `{"added": True}` entry and `action_undo` removes the task for it | same node RED — first at the notification limb (`AssertionError: no nothing-to-undo notification fired`), and a direct probe of the mutant (`_on_task_added` → `action_undo`) printed `MODALTASK still present: False`, i.e. the stays-put limb is red by the same mechanism | same hash ✓, node green on re-run |
| C | **Escape swallows without an active focus** — the seat entry gains `priority=True`, so the app-level binding answers before any screen's own escape | `test_focus_cycle_filters_the_board_and_escape_restores` RED — `AssertionError: escape was swallowed before the modal could see it`, `assert 2 == 1` (ConfirmModal still on the stack) | hash → `34acf394…` ✓, node green on re-run |

### Reverse census — trigger family B (C-26, reconciled BEFORE touching the seats)

| Probe | Command | Result |
|---|---|---|
| B1 census over touched symbols | `grep -rln "kanban_order\|_kanban_column_rows\|_kanban_grouped\|render_kanban\|render_view\|nav_model\|render_key_bar\|_select_first\|refresh_view" tests/` | every consumer calls with defaulted kws or positional prefixes — additive-only change (A3). `key_bar_plain`/`fit_bar` (unescaped, plain-text path) untouched by the `_mshow` fix — only the markup half changed; `test_the_rendered_markup_carries_every_key_the_fit_chose` asserts `show in markup` and `\[` contains `[` |
| B1 assertion-level reconciliation | read `test_keymap.py` width laws, occupancy/palette/span suites | the kanban bar grows to 35 entries (≈+13 no-word cells); all width expectations are DERIVED from the seat at assert time (Inc-1 amended law), so they re-derive green — measured: full module green |
| B2/B3 | file moves / byte-identical goldens | did not fire |
| A3 interface consumed by another module changed | `kanban_order` seed param `focus` consumed; `_kanban_column_rows`/`_kanban_grouped`/`render_kanban`/`render_view`/`nav_model` (+1 defaulted kw each); `_select_first`/`refresh_view` (behavior: focus-aware only when a focus is active — inert otherwise, full suite green) | additive only |
| occupancy/palette/span-economy/legend sweep | full `pytest tests` | all green — the header focus annotation wears `mut` like its sort/group siblings; the seeded demo board trips no ration/occupancy law |

### Signed-balance test ledger

`post = base − deleted + added` → `824 = 813 − 0 + 11` ✓ reconciles (11 new nodes: 10 in `tests/test_app.py`, 1 in `tests/test_momentum.py`; no test deleted; the only existing-test edit is the `spelled` spelling map — mechanism, not law). Gate line: 823 passed + 1 environmental deselect = 824.

---

## 5 · Risks

- **Matrix presentation ignores the focus** (flagged): the standing Inc-006 precedent, now inherited by a third flag — in matrix presentation with a focus active, `_kanban_matrix` draws everything while the nav model (which has no presentation concept) honors the filter, so non-focused tasks are drawn (as dots) but not nav-reachable. The one-site fix, if a PDR rules otherwise, is the `render_kanban` call in `app.py`.
- **The kanban bar grew by five entries** (~+13 no-word cells, 35 total): all width laws re-derive from the seat at assert time (Inc-1 amendment) — measured green. At the app's shipped 118-cell keybar the kanban bar now drops keys and counts them (`+N`) — the amended law working as designed, and `?` carries the full set.
- **`escape` is now an app-level binding**: every modal and the aperture bind their own escape and screen bindings answer first (the AT-013 modal limb and the RED-C probe prove the ordering); any FUTURE screen that forgets its own escape over a focused kanban would inherit focus-exit — the guarded no-op keeps that harmless.
- **Undo granularity is single-task by design** (AMD-05 reading recorded in the spec): multi-step modal edits remain outside the domain; the stack dies with the session (the story's session-level law, TC-013's restart shape).

## 6 · Pending items / spec deviations

- **Prompt-vs-spec mismatch (flagged, spec followed):** the increment brief said the focus cycle includes "Inbox" as a target; HLR-008/LLR-008.1 + D-5 rule the cycle is `visible_projects` ending in `None` and Inbox is NOT a focus target. Implemented per spec.
- **Kanban cards have no due readout (spec gap, flagged):** HLR-009 names `date_chip` as the card's due readout, but the kanban `card_cell` renders no date token (only ↗/!/▤/·Nd/▣) and `date_chip` has no consumer in `views.py`; the relative due token (`reldue_token`) renders only in the AGENDA view. AT-014/AT-015 therefore press the key on the kanban (the shipped surface) and read the token in agenda. If the intent was a kanban-card date token, that is a one-line card_cell addition plus a width-shedding decision — candidate for a §6.5 amendment.
- **WIP counts under focus (decision, flagged — the Inc-007-carried arch m-6 question):** `_kanban_grouped` scopes its input, so header counts and the `N tasks` tally describe the FOCUSED set (a `DOING 4/3` burn for tasks the board is not drawing would be a lie of the same family the focus exists to remove). If a ruling wants phase-wide counts under focus, the one site is the input filter in `_kanban_grouped`.
- **Undo restore position for resurrected tasks** (noted): re-inserted at the pre-delete board index (clamped), so board order round-trips exactly; the spec pins only same-id, this is strictly stronger.
- **V-5 selector reconciliation**: HLR-008's `-k "focus"`, HLR-009's `-k "due_bump"` (test_app) / `-k "bump_due"` (test_momentum), HLR-010's `-k "undo"` / `-k "undo_stack"` selectors all work as written against the implemented node names. TC-013 ships as the `undo_stack` node (the spec's own id for the LLR-010.1 unit).

## 7 · Suggested next task

**Inc 6 — R-11 (K11 standup modal, `S`):** `standup_query(board, today, show_archived)` pure function (window today−7 ≤ stamp ≤ today, grouped by `visible_projects` order with Inbox last, done marked via `board.is_done`) + `StandupModal` on the `LegendModal` pattern with three close bindings (`escape`/`q`/`S`), per LLR-011.1/LLR-011.2 and AT-018/TC-014. Then AT-019 (the aperture swallow over all 13 keys) and the Phase-4 supersession sweep. Watch: `S` is the last new KEYMAP entry of the batch — the bar laws re-derive, but the legend KEYS section (LLR-012.2, AMD-03) is still unassigned and pairs naturally with it.

---

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | ≤4 source files, or reason declared | ✓ | 4/4 (app.py, views.py, models.py, keymap.py) — §2 |
| 2 | Tests written in this same increment | ✓ | 11 new nodes — §2/§4 |
| 3 | Layer 0 written where the criterion applies | ✓ | TC-011 seat filter, TC-012 pure-helper unit, TC-013 stack unit — §4 Layer A |
| 4 | RED counterfactual captured and restored by hash | ✓ | A (new-id resurrection) + B (undoable modal add) + C (priority escape), goldens `083c23fe…`/`34acf394…` re-proven after each cycle, `__pycache__` cleared per cycle — §4 |
| 5 | Reverse census run on every touched symbol | ✓ | B1 re-run and reconciled; B2/B3 non-fires; A3 additive-only — §4 |
| 6 | `code-reviewer` passed — a HIGH blocks | ⚠ | Not invoked by this agent; left for the orchestrator's review gate (declared per notice convention) |
| 7 | No file from another lane touched | ✓ | Batch not forked |
| 8 | Frozen interfaces untouched | ✓ | Every signature change is a defaulted keyword; census-callers compile unchanged (full suite green) — §4 A3 |
| 9 | Coverage claims verified on disk, not from intent | ✓ | pytest tail pasted from one complete post-restore run (823 passed / 0 failed / 1 environmental deselect); verify_aperture `ALL PASSED` pasted; convergence probe pasted — §4 |
