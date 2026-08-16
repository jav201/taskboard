# Increment 006 — R-03 + R-04 · Kanban column sort (`s`) and grouping (`g`) on ONE shared ordering seat

| Field | Value |
|---|---|
| Batch | `2026-08-14-batch-04` |
| Increment | `006` (Increment 2 of the batch) |
| Lane | — (batch not forked) |
| Requirement(s) | R-03 / HLR-003 / LLR-003.1, LLR-003.2 · R-04 / HLR-004 / LLR-004.1 · §3.0 key-registration contract (`s`, `g` rows) · §6.5 AMD-04 (trailing Done group), AMD-07 (painted-text oracle anchor), AMD-09 (stability pin) |
| Acceptance | AT-005, AT-006, AT-007, AT-008 (Layer B, Pilot) · TC-005 (Layer A, sort modes + stability + default-order pin + purity) · TC-006 (the nav/render parity oracle, 01b §4) · TC-007 horizon boundary pins (folded into the horizon unit, V-5) |
| Agent | `software-dev` (supervised-incremental-development) |
| Date | 2026-08-15 |

---

## 1 · What changed

**BLUF: the kanban view's render order and nav order now come out of ONE pure function, so the batch's named top bug class — the cursor walking a different order than the screen paints — is structurally impossible, and the painted-text parity oracle proves it across the full 4×3 mode cross-product.** `s` cycles the column sort `project → priority → due → recent`; `g` cycles the grouping `project → priority → horizon` (with the spec's fifth trailing `Done` group); the header names any non-default mode (`· sort: due`, `· group: horizon`); both keys are kanban-scoped in the seat and guarded no-ops elsewhere.

- `kanban_order(board, tasks, show_archived, *, group, sort, collapsed, focus, today)` — NEW pure seat in `taskboard/views.py` beside `_kanban_groups` (LLR-003.1). It answers "in what order do this column's tasks appear" for BOTH consumers: `_kanban_column_rows` (render) and the kanban branch of `nav_model` (nav). Sort modes are intra-group and ALL STABLE (AMD-09): `project` = board order; `priority` = blocked first, high→normal→low, ties by due (undated sink); `due` = `sort_by_due` semantics with blocked first; `recent` = `phase_changed` desc, None sunk, ties board order. Group modes (LLR-004.1): `project` delegates to `_kanban_groups` verbatim (Inbox last — the default-mode regression pin is byte-equal tuple equality); `priority` = High/Normal/Low; `horizon` = Overdue/This week/Later/No date via `urgency()`, plus the trailing `Done` group in dim tone with its own pinned `phase_changed`-desc order (AMD-04). Empty groups emit no header (the no-ghost law).
- Convergence (the parallel-model trap closed): `_kanban_groups` now has exactly ONE call site — inside `kanban_order` itself. The old second ordering site (nav branch re-deriving via `_kanban_groups` + `phase_buckets`) is deleted; nav buckets first, then asks the seat per column. Probe output in §4.
- `TaskboardApp`: `kanban_sort` / `kanban_group` state fields (session-level, never persisted — LLR-003.2's explicit ruling, so `models.py` is UNTOUCHED), `action_kanban_sort` / `action_kanban_group` cycle actions view-guarded per the `action_toggle_presentation` precedent, both added to `BOARD_ACTIONS` (the aperture drop), and the mode state threaded through `refresh_view`, `_repaint_flow` and `_nav_columns`.
- `keymap.py`: `Key("s", …, "kanban_sort", "Sort", views=("kanban",))` and `Key("g", …, "kanban_group", "Group", views=("kanban",))`, placed before the arrow block (AMD-03 placement rule), beside the Tab precedent they follow.
- Kanban header (`_kanban_grouped`): appends `· sort: {mode}` and `· group: {mode}` when non-default — LLR-003.2's naming requirement plus ux-review m-3's symmetric group token (the brief's indicator requirement); the default mode stays bare, so the token disappearing IS the exit indicator.
- README keybinding table: `s` and `g` rows with the "Kanban only:" convention and the full cycles named (ux m-4; enforced by `test_the_readme_keybinding_table_matches_the_seat`).

The matrix presentation is deliberately untouched ("matrix presentation sorting" is out of scope, R-03 functionality line).

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count. SOURCE: 3/4.**

| File | Kind | Change |
|---|---|---|
| `taskboard/views.py` | source | `kanban_order` seat + `_recent_first` + `_KANBAN_SORT_MODES`/`_KANBAN_GROUP_MODES`/`_PRIO_RANK`; `_kanban_column_rows`, `_kanban_grouped`, `render_kanban`, `render_view`, `nav_model` re-wired to consume it (all new params defaulted — the census's 3-arg `nav_model` calls compile unchanged) |
| `taskboard/app.py` | source | `kanban_sort`/`kanban_group` state, two view-guarded cycle actions, 2 `BOARD_ACTIONS` members, 3 call-site pass-throughs |
| `taskboard/keymap.py` | source | `s`/`g` entries before the arrow block, `views=("kanban",)` |
| `README.md` | docs (outside count) | `s`/`g` keybinding rows |
| `tests/test_app.py` | test | 12 new nodes + 3 shared helpers (`_mode_board`, `_painted_kanban`, `_painted_card_ids`, `_assert_kanban_parity`) |

`taskboard/models.py` — **NOT touched.** LLR-003.2 rules the mode state session-level ("not persisted; it lives on the app, like `kanban_presentation`"), so the spec requires no settings persistence and none was invented (the brief's point 4 resolves to NO).

---

## 3 · How to test

```bash
python -m pytest tests -q                                                          # full gate: MUST be 0 failed
python -m pytest tests/test_app.py -k "kanban_sort" -q                             # AT-005, AT-006
python -m pytest tests/test_app.py -k "kanban_group" -q                            # AT-007, AT-008
python -m pytest tests/test_app.py -k "kanban_order or parity" -q                  # TC-005 + TC-006 (+ parity ATs)
python -m pytest tests/test_app.py -k "horizon" -q                                 # TC-007 boundary pins
python -m pytest tests/test_keymap.py -q                                           # four-seat enforcement, 0 failed
grep -n "_kanban_groups\|phase_buckets" taskboard/views.py                         # LLR-003.1 convergence probe
PYTHONIOENCODING=utf-8 python prototypes/verify_aperture.py                        # aperture law (UTF-8 forced: cp1252 console)
```

---

## 4 · Test results

**One complete run. Tail read from THAT run's own output:**

```
........................................................................ [ 99%]
......                                                                   [100%]
798 passed in 53.71s
```

`verify_aperture.py` — final lines of the same run:

```
  [PASS] the hero under test is the DEADLINE's reading, and its detail is the user's TITLE — the reason `hero.py` escapes at all  deadline: '[URGENT] rotate keys'
  [PASS] the hero leg is not vacuous: some languages really do compose the detail line into the panel at 118x34 (the rest are a regression guard, and this check is what would notice the last one going away)  3/10: ['swiss', 'industrial', 'darkside']

ALL PASSED
```

LLR-003.1 convergence probe (pass condition: both routes converge on the new seat):

```
2182:def _kanban_groups(board, tasks, show_archived) -> list[tuple[str, str, list[Task]]]:
2256:        groups = _kanban_groups(board, tasks, show_archived)      ← sole call site: INSIDE kanban_order
2284:    for name, color, items in kanban_order(board, tasks, show_archived,   ← render path
2528:                 kanban_order(board, bucket, show_archived,                ← nav path
```

(views.py:2321/2377 are `phase_buckets` in `_kanban_grouped`/`_kanban_matrix` — the bucketing step both paths share, not an ordering site.)

| Layer | Nodes | Result |
|---|---|---|
| **A · white-box** | `test_kanban_order_sort_modes_are_stable_and_distinct` (TC-005: 4 modes, pairwise-distinct fixture guard, every tie pinned) · `test_kanban_order_default_reproduces_kanban_groups` (default-order regression PIN: byte-equal tuples vs `_kanban_groups`) · `test_kanban_order_is_pure_and_unknown_phase_falls_to_bucket_zero` (purity + bucket-0 fallback) · `test_kanban_order_horizon_boundaries_and_done_group` (TC-007 pins: −1d/today/+7/+8/None, future-due last-phase → trailing dim `Done`, `phase_changed`-desc, empty-group no-ghost) · `test_kanban_mode_actions_are_registered_and_guarded` (§3.0 four seats + before-arrow placement) | 5 passed |
| **B · black-box** | `test_kanban_sort_cycles_and_names_the_mode` (AT-005) · `test_kanban_sort_parity_arrow_walk` (AT-006) · `test_kanban_group_cycles_headers_and_membership` (AT-007) · `test_kanban_group_parity_arrow_walk` (AT-008) · `test_kanban_parity_painted_text_oracle` (TC-006: painted-text anchor + non-emptiness + union-coverage + arrow walk, swept over 4 `s` presses, 3 `g` presses and the full 4×3 cross-product; `line_map` limb labelled PIN) · `test_kanban_mode_keys_are_noops_outside_kanban` (view guard) · `test_kanban_mode_keys_are_dead_on_the_aperture` (aperture probe for `s`/`g`) | 7 passed |

### RED counterfactuals — executed, not predicted

Two mutations, each applied in my own tree, restored byte-exact and PROVEN by hash (`sha256sum` back to the pre-mutation value `e45e3ede46775c7978876ee3c98d852007888dd973f5157da7d44c11aad221d5`; restore via `cp` of a hash-verified backup — NO `sed -i` — with `__pycache__` cleared after every mutation/restore cycle, C-46). The on-disk files are LF (verified: zero `\r` in all five touched files; the CRLF warnings come from git's checkout convention, not the working tree), so no ending hazard existed this time — the hash rule was enforced anyway.

| # | Mutation applied | Reddened node(s) | Restore proven by |
|---|---|---|---|
| A | **The oracle's trap** — `nav_model`'s kanban branch reverted to the raw `_kanban_groups` + `phase_buckets` ordering, i.e. nav and render fed DIFFERENT orderings (the exact F-3/01b-§4 mutation, executable by construction) | `test_kanban_parity_painted_text_oracle` (TC-006), `test_kanban_sort_parity_arrow_walk` (AT-006), `test_kanban_group_parity_arrow_walk` (AT-008) RED — **3 failed, 4 passed**; AT-005/AT-007 stayed green (they never consult nav), which is exactly the asymmetry the oracle exists for | `views.py` hash → `e45e3ede4677…` ✓, suite re-run green |
| B | **Sort direction** — `_recent_first` flipped to ascending (`reverse=True` dropped): `recent` becomes oldest-first with None FIRST | `test_kanban_order_sort_modes_are_stable_and_distinct` (TC-005 recent limb), `test_kanban_sort_cycles_and_names_the_mode` (AT-005 recent press), `test_kanban_order_horizon_boundaries_and_done_group` (Done-group pinned-order limb) RED — **3 failed, 5 passed**; the parity oracle stayed green (both ends share the seat — it catches DIVERGENCE, not wrongness; wrongness is TC-005/AT-005's job). Demonstrates the two test families are not redundant | same hash ✓, suite re-run green |

Transcript sample (mutation A, TC-006 — painted ≠ nav under `priority` sort):

```
>           assert p_col == n_col, \
                f"column {ci} ({names[ci]}): painted {p_col} != nav {n_col}"
E           AssertionError: column 1 (Doing): painted ['55590417', '73a02709', 'd0b74494', '6f483eee', 'a10fd993'] != nav ['55590417', '73a02709', 'd0b74494', 'a10fd993', '6f483eee']
```

### Reverse census — trigger family B (C-26 reconciled BEFORE touching views.py)

| Probe | Command | Result |
|---|---|---|
| B1 pre-increment census re-run | `grep -rl "_kanban_groups\|_kanban_column_rows\|phase_buckets\|nav_model\|render_kanban" tests/` | `test_app.py`, `test_archive.py`, `test_swimlanes.py` — EXACT match with `02-review-architect.md` §1 (nav_model hits in archive/swimlanes are the non-kanban branches) |
| B1 assertion-level reconciliation | read `test_app.py:430-457` (3-arg `nav_model("kanban", …)`), `:1300-1356`, `:1432-1526` | protected by design: all new params defaulted (3-arg calls compile and behave identically — the default-mode byte-equal PIN proves it); the whole module green post-change |
| B2 file moved on disk | — | did not fire: no file moves |
| B3 byte-identical goldens | `ls tests/goldens` | did not fire: no such directory (re-checked) |
| B4 artifact consumed elsewhere | packet path convention | consumed by `.dev-flow/04-validation.md`, `BACKLOG.md`, `PLAN.md` |
| A3 interface consumed by another module changed | `nav_model`, `render_kanban`, `render_view`, `_kanban_column_rows` signatures | additive only — every new parameter keyword-defaulted; `render_view`'s 12 consumer test files green; no positional signature broken |

### Signed-balance test ledger

`post = base − deleted + added` → `798 = 786 − 0 + 12` ✓ reconciles (12 new nodes in `tests/test_app.py`: 4 pilot ATs, 1 parity oracle, 4 `kanban_order` units, 1 registration unit, 2 guard/aperture pilots; no test edited or deleted)

---

## 5 · Risks

- **Inc 4/5 will consume the `collapsed`/`focus` parameters** already in the seat's signature (LLR-003.1 pins them). Their seed semantics are honest and tested-by-nobody-yet: `focus` filters the column's tasks to one project; `collapsed=True` returns NO groups (the column contributes nothing — LLR-007.1's nav exclusion). If Inc 4's design wants the `✓ N` count from the seat instead of the caller, that is a one-site change.
- **The parity oracle's walk limb assumes nothing is windowed** (asserts drawn phases == `board.phases` at 120 cells). A future phase-count growth past the window will fail LOUDLY there, not silently — the assert is the guard, but the fixture's width/phase budget is a real coupling.
- **The kanban bar crossed 96 cells** with `s`/`g` aboard (kanban bare width now 94 cells; 38 entries) — EXPECTED and lawful under the Inc-1 amended width law; `test_keymap.py` is green across the sweep.

## 6 · Pending items / spec deviations

- **`today` parameter added to `kanban_order`** (flagged): LLR-003.1 pins the signature `(board, tasks, show_archived, *, group, sort, collapsed, focus)` — no clock — but `horizon` grouping cannot bucket without one. Added as a defaulted keyword (`today=None` → `date.today()`), the LLR-006.1 defaulted-parameter precedent; it keeps the seat testable (TC-007 pins inject it) and all pinned parameters present. Candidate for formal amendment.
- **Done-group order is pinned `phase_changed`-desc REGARDLESS of the active sort** (flagged): LLR-004.1's Statement gives the trailing `Done` group its own order unconditionally, so under `sort=priority/due` + `group=horizon` the Done group does NOT follow the sort mode. Strictest reading implemented; if the intent was "sorted like everything else once a sort is active", this is a one-line change with an existing test limb to flip (`test_kanban_order_horizon_boundaries_and_done_group`).
- **HLR-004 prose vs D-3 on label case** (flagged): HLR-004's acceptance prose says "e.g. `NO DATE`" (uppercase); LLR-004.1 + §6.2 D-3 pin the PDR-confirmed strings "Overdue / This week / Later / No date" (sentence case). D-3 is the ruling → sentence case shipped; HLR prose is the stale one.
- **ux m-3 adopted without an AMD** (flagged): the `· group: {mode}` header token was a ux-review minor ("cheap fix"), never formalized in §6.5; the increment brief explicitly required the header to annotate sort AND group, so both tokens ship. Recorded here for the Phase-2/4 paper trail.
- **`group=priority` collapses `sort=priority` and `sort=due` to the same order** (noted, not a defect): inside a priority group the rank key is constant, so both modes reduce to blocked-first + due. The pairwise-distinctness guards live at `group=project` where the modes genuinely diverge.
- **TC-007 has no standalone node** (V-5 provisional ids): its ≥7 boundary pins are folded into `test_kanban_order_horizon_boundaries_and_done_group` (matched by both `-k "horizon"` and `-k "kanban_order"` selectors from LLR-004.1). Reconcile at Phase 4 id mapping.
- **CRLF claim in the brief is stale** (noted): the touched files are LF on disk (Inc-005's CRLF incident belonged to an earlier tree state); the hash-verified restore was enforced regardless and is ending-agnostic.
- **ux m-5 (new keys firing behind open modals)** was a minor with no AMD and is NOT addressed here: `s`/`g` behave exactly like the existing non-priority board keys behind modals. If a ruling lands, it applies batch-wide, not to this increment alone.

## 7 · Suggested next task

**Inc 3 — R-05 (K5 WIP limits)**: `Board.wip_limit` pure getter + `set_wip_limit` only-write-path in `models.py` with the `rename_phase` migration (AMD-08), the ` n/limit` tag in `_windowed_header` burning `over` only when strictly over (the at-limit calm boundary is the cheapest mutation — pin both sides), settings-driven Fixture A AND default-map Fixture B. The census already cleared `_windowed_header` (zero direct asserters) and the header-content tests (`test_app.py:1300-1356`) survive ` n/limit` suffixes by substring.

---

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | ≤4 source files, or reason declared | ✓ | 3/4 (views.py, app.py, keymap.py); models.py deliberately untouched — §2 |
| 2 | Tests written in this same increment | ✓ | 12 new nodes — §2/§4 |
| 3 | Layer 0 written where the criterion applies | ✓ | 4 pure-seat units on `kanban_order` (modes, stability, purity, horizon boundaries) — §4 Layer A |
| 4 | RED counterfactual captured and restored by hash | ✓ | mutations A (the oracle trap) + B (sort direction), hash `e45e3ede…` re-proven twice, `__pycache__` cleared per cycle — §4 |
| 5 | Reverse census run on every touched symbol | ✓ | B1 re-run and reconciled against 02-review-architect §1 pre-change; B2/B3 non-fires; A3 additive-only — §4 |
| 6 | `code-reviewer` passed — a HIGH blocks | ⚠ | Not invoked by this agent; left for the orchestrator's review gate (declared per notice convention) |
| 7 | No file from another lane touched | ✓ | Batch not forked |
| 8 | Frozen interfaces untouched | ✓ | A3 probe: every signature change is a defaulted keyword — §4 |
| 9 | Coverage claims verified on disk, not from intent | ✓ | pytest tail pasted from one complete run (798 passed / 0 failed); verify_aperture `ALL PASSED` pasted; convergence probe pasted — §4 |
