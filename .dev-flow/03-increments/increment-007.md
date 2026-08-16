# Increment 007 — R-05 · WIP limits in the kanban phase header (`n/limit`, burning strictly over)

| Field | Value |
|---|---|
| Batch | `2026-08-14-batch-04` |
| Increment | `007` (Increment 3 of the batch) |
| Lane | — (batch not forked) |
| Requirement(s) | R-05 / HLR-005 / LLR-005.1, LLR-005.2 · §6.5 AMD-08 (pure getter + sole setter; `rename_phase` migrates the entry) · D-12 · 01b F-11 (closed by construction) |
| Acceptance | AT-009, AT-010 (Layer B, Pilot) · TC-008 (Layer A: getter precedence/purity, setter write path, rename migration, header tag tone boundary table) |
| Agent | `software-dev` (supervised-incremental-development) |
| Date | 2026-08-15 |

---

## 1 · What changed

**BLUF: every kanban phase header now carries its WIP tag — ` n/limit` when the phase has a limit, bare ` n` when it does not — burning in the `over` tone ONLY when strictly over the limit, with the operator-approved default `Doing ≤ 3` reading from a constant map instead of being written into the board file, so a READ can never dirty a hand-edited board (the M-4 defect class, excluded by construction).**

- `Board.wip_limit(phase)` — NEW PURE getter (`taskboard/models.py:926`, beside the clock settings per LLR-005.1's placement). Precedence chain exactly per Statement: an operator-set value in `settings["wip_limits"]` that coerces to a positive int wins; anything else (absent, non-numeric, non-positive, or keyed to a phase the board does not have) is ignored and falls through to `DEFAULT_WIP_LIMITS = {"Doing": 3}` (`models.py:73`), then to `None`. **No write side-effects, no read-time materialization** — the default lives in the constant, never in `board.settings`, which is how the default materializes WITHOUT a write-on-read (AMD-08's exact demand).
- `Board.set_wip_limit(phase, limit)` — NEW and the ONLY write path (`models.py:949`): validation and coercion live here, never in the getter. A positive-coercing value sets the limit; anything else CLEARS it, so a value the getter would misread can never be persisted. The caller saves (the `add_phase`/`rename_phase` precedent — LLR-005.1's round-trip acceptance lists `save` as a separate step).
- `Board.rename_phase` (`models.py:1114`) now migrates `settings["wip_limits"][old]` → `[new]` alongside the task-phase rewrite it already performed, so a rename can never orphan an operator-set limit (closes 01b F-11 by construction; the sole pre-existing caller, `modals.py:874` PhaseEditor, is signature-untouched).
- `_windowed_header` (`taskboard/views.py:2165`) appends the tag to each visible phase cell, computing `n` from `phase_buckets` over the view's visible tasks (LLR-005.2). Layout is tag-LAST: the phase name truncates before the tag, so the count survives width pressure; `over` tone iff `n > limit`, the quiet `mut` tone otherwise (at-limit is CALM — the cheapest mutation is the off-by-one, and both sides are pinned). Both call sites updated (`views.py:2348` grouped, `views.py:2380` matrix — the tag lands on both presentations through the one shared seat).
- **No keymap changes.** K5 has no key; LLR-005.1 declares no interactive management surface (limits are settings-driven), so none was invented. `app.py`, `keymap.py`, README key table: untouched.

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count. SOURCE: 2/4.**

| File | Kind | Change |
|---|---|---|
| `taskboard/models.py` | source | `DEFAULT_WIP_LIMITS` constant (:73); `wip_limit` pure getter (:926) + `set_wip_limit` sole write path (:949) beside the clock settings; `rename_phase` migrates the settings entry (:1114, docstring updated to say so) |
| `taskboard/views.py` | source | `_windowed_header` (:2165) gains the `tasks` parameter and the tag/tone/tag-last layout; both call sites pass `tasks` (:2348, :2380) |
| `tests/test_app.py` | test | 3 new nodes + 1 helper (`_hex_span_covers`, `:2920`): AT-009 `:2938`, AT-010 `:2976`, TC-008 header `:3006` |
| `tests/test_momentum.py` | test | 4 new nodes (LLR-005.1 model half): precedence `:197`, purity `:217`, rename migration `:235`, setter round-trip `:249` |

`taskboard/app.py`, `taskboard/keymap.py`, `taskboard/modals.py` — **NOT touched** (no new action, no new key, the PhaseEditor's `rename_phase` call needs no change).

---

## 3 · How to test

```bash
python -m pytest tests -q                                                          # full gate: 0 failed (see §4 for the environmental caveat)
python -m pytest tests/test_app.py -k "wip" -q                                     # AT-009, AT-010
python -m pytest tests/test_app.py -k "wip or windowed_header" -q                  # + TC-008 header boundary table
python -m pytest tests/test_momentum.py -k "wip_limit or rename_phase" -q          # LLR-005.1 model half
python -m pytest tests/test_archive.py tests/test_momentum.py -q                   # settings-bearing model seats stay green
grep -n "wip_limits" taskboard/models.py                                           # write-path census: exactly the setter + rename migration
```

---

## 4 · Test results

**One complete run. Tail read from THAT run's own output (post-restore, after both RED cycles):**

```
............                                                             [100%]
804 passed, 1 deselected in 53.12s
```

The deselected node is `tests/test_app.py::test_win_clipboard_roundtrip` — an **environmental** failure, not an increment regression (evidence and handling at the end of this section). The same complete run without the deselect: `1 failed, 804 passed`, the failure being exactly that node.

| Layer | Nodes | Result |
|---|---|---|
| **A · white-box** | `test_wip_limit_reads_settings_then_default_then_none` (TC-008/LLR-005.1 precedence: absent → `Doing` 3; explicit `{"Doing": 2}` → 2; unlimited → None; `0`/`-1`/`"many"`/unknown-phase entries ignored — 9 pins, ≥ 6 required) · `test_wip_limit_getter_is_pure` (AMD-08: getter called TWICE, `board.settings` deep-unchanged AND on-disk bytes unchanged — the write-on-read limb) · `test_rename_phase_migrates_the_wip_limit` (limit follows `Doing→In Progress`, no orphan left, task rewrite intact, entry-less rename clean) · `test_set_wip_limit_is_the_only_write_path_and_round_trips` (coercion at the write, verbatim save/load round-trip, non-positive CLEARS, hand-edited file honored without rewrite) · `test_windowed_header_wip_tag_tones_and_boundaries` (TC-008 boundary table n ∈ {0, limit−1, limit, limit+1} off a NON-default settings limit: fraction present, `over` tone ⇔ strictly over, cells width-exact; no-limit phase → bare count, no fraction, asserted on STRIPPED text; tag survives at `MIN_COL`) | 5 passed |
| **B · black-box** | `test_kanban_wip_header_shows_count_over_default_limit` (AT-009: default limit, never materialized into settings; `3/3` calm on the emitted spans, one task over → `4/3` burns — span tone compared as parsed `textual.color.Color`, because a hex-substring check on the style would be vacuous) · `test_kanban_wip_header_honors_a_non_default_limit` (AT-010, C-10 settings-driven: `4/2` painted, `4/3` NOT; sibling Backlog shows bare count, no fraction) | 2 passed |

### RED counterfactuals — executed, not predicted

Two mutations, each applied in my own tree, restored byte-exact and PROVEN by hash (restore via `cp` of hash-verified goldens — NO `sed -i` — with `__pycache__` cleared after every mutation/restore cycle, C-46).

| # | Mutation applied | Reddened node(s) | Restore proven by |
|---|---|---|---|
| A | **Burn at `>=`** — `_windowed_header` tone condition flipped from `count > limit` to `count >= limit` | `test_windowed_header_wip_tag_tones_and_boundaries` (TC-008 at-limit limb) + `test_kanban_wip_header_shows_count_over_default_limit` (AT-009 calm limb) RED — **2 failed, 5 passed**; AT-010 stayed green (its fixture is always over — correct: it never exercises the boundary) | `views.py` → `c56c7607b36faf192b460f9bbb4d217277970ce78a9596c4ceea2a77569f3995` ✓, suite re-run |
| B | **Write-on-read getter** — `wip_limit` prepended with `self.settings.setdefault("wip_limits", dict(DEFAULT_WIP_LIMITS))` (the exact M-4 defect) | `test_wip_limit_getter_is_pure` (purity limb) + `test_kanban_wip_header_shows_count_over_default_limit` (AT-009's not-materialized companion) RED — **2 failed, 6 passed** | `models.py` → `d96e31587d5f66371a1c67edf2fb4153da4db3272384a869a008751123e8c29a` ✓, suite re-run |

Transcript samples:

```
# A — TC-008, at-limit burns under the mutation:
>           assert (HEX["over"] in cells[doing_i]) == (count > limit)
E           AssertionError: assert ('#f43f5e' in '[#8b98a5][/][b #c9d4e0]DOING ... [/][#f43f5e] 2/2[/][#8b98a5][/]') == (2 > 2)

# B — purity, the read materialized the default map:
>       assert b.settings == before_settings            # nothing materialized
E       AssertionError: assert {'wip_limits': {'Doing': 3}} == {}
```

### Reverse census — trigger family B (C-26, reconciled BEFORE touching the seats)

| Probe | Command | Result |
|---|---|---|
| B1 pre-increment census re-run | `grep -rln "_windowed_header\|wip_limit\|rename_phase" tests/` | pre-change: `_windowed_header` and `wip_limit` — **zero** files (exact match with `02-review-architect.md` §1's census); `rename_phase` — zero test asserters, one production caller (`modals.py:874`, signature unchanged) |
| B1 header-content asserters read | `test_app.py:1300-1316`, `:1338-1355`, `:1439+` | survive by substring (`"DOING"` ⊂ `"DOING 4/3"`); width-exactness (`all(len(l) == 140)`) and divider-count laws hold — the tag is laid out INSIDE the existing width-exact cell math (verified green in the full run) |
| B2/B3 | file moves / byte-identical goldens | did not fire |
| A3 interface consumed elsewhere | `_windowed_header` (+1 required param), `rename_phase` (unchanged), `Board` (+2 methods) | `_windowed_header` is private with exactly TWO call sites, both updated (`views.py:2348`, `:2380`); additive-only otherwise |
| occupancy/palette/span-economy sweep | full `pytest tests` | all green — the added header spans/text trip no ration law |

### Signed-balance test ledger

`post = base − deleted + added` → `805 = 798 − 0 + 7` ✓ reconciles (7 new nodes: 3 in `tests/test_app.py`, 4 in `tests/test_momentum.py`; no test edited or deleted). Gate line: 804 passed + 1 environmental (below) = 805.

### The environmental red — `test_win_clipboard_roundtrip`

After the final restore, the full gate ran `1 failed, 804 passed`, the failure being `tests/test_app.py::test_win_clipboard_roundtrip`. **Evidence it is the environment, not this increment:** (1) the failing assertion is the test's own SETUP guard — `powershell Set-Clipboard` fails before any app code runs, with the test's own message "SETUP failed — this is the environment, not the code under test"; (2) `powershell -NoProfile -Command "Set-Clipboard -Value 'probe'"` fails DIRECTLY, no Python or repo involvement (`Requested Clipboard operation did not succeed`), and stayed locked across 6 retries over 60 s; (3) the baseline run at this increment's start (798 passed) included this node GREEN on a tree differing only by this increment's diff, which touches no clipboard path; (4) git log records this node's known flakiness class (`30473d4`). The increment gate therefore reads **804/804 relevant green**; the orchestrator should re-run the full set once the OS clipboard frees (a long-lived 747 MB `python.exe`, PID 21260, is the suspected lock holder — deliberately NOT killed: killing an unidentified user-session process is out of bounds for an increment).

---

## 5 · Risks

- **The default `Doing ≤ 3` is name-keyed**: renaming `Doing` WITHOUT a settings entry drops the default for that phase (the renamed phase reads unlimited). This is the spec's literal design (default map keyed by phase name, HLR-005), and the migration law covers every OPERATOR-SET limit; flagged so a future "renamed Doing keeps its default" surprise is a ruled change, not a bug report.
- **The header count `n` counts visible tasks in the phase regardless of group/sort mode** (it comes from `phase_buckets`, not from `kanban_order` output) — correct per LLR-005.2, but under a future focus-filter increment (R-08) the question "does `DOING 4/3` count focused-only tasks?" (arch m-6) lands here; the seat is the one `phase_buckets` call in `_windowed_header`.
- **`set_wip_limit` does not save** (caller-saves precedent). If a future management surface (a limits modal) is added, it must call `board.save()` — as the round-trip test documents.
- **Matrix presentation carries the tag too** (shared `_windowed_header`). Consistent and tested width-exact, but HLR-005's acceptance prose was written against the grouped kanban; noted for Phase-4 id reconciliation.

## 6 · Pending items / spec deviations

- **No management surface implemented** (flagged, per brief point 3): LLR-005.1 declares none — limits change by editing settings (via `set_wip_limit` or a hand-edited file, both tested). If the operator wants a key/modal, that is a new requirement, not a gap in this increment.
- **V-5 id reconciliation**: LLR-005.1's verification named `tests/test_momentum.py -k "wip_limit or rename_phase"` and HLR-005's named `tests/test_app.py -k "wip"` / `-k "wip or windowed_header"` — both selectors work as written against the implemented node names. TC-008's ≥ 6 pins are split across the four `test_momentum.py` nodes (model) and `test_windowed_header_wip_tag_tones_and_boundaries` (header), all matched by those selectors.
- **The environmental clipboard red** (§4) is carried as a known-environmental, not batch-scope; the Phase-4 "empty-red" criterion needs one re-run with a free clipboard.
- **`verify_aperture.py` not run this increment**: no new actions/keys/`BOARD_ACTIONS` members — the aperture surface is untouched. Phase-4's complete gate run covers it.

## 7 · Suggested next task

**Inc 4 — R-06 + R-07 (K6 aging token, K7 collapse)**: `card_cell` gains the `·Nd` token from `days_in_phase` with a defaulted `today` (None → no token, never `·0d`; the `test_archive.py:581`/`test_palette_ration.py` unstamped fixtures are already safe), and the collapse flag feeds the `collapsed` parameter `kanban_order` ALREADY carries (Inc-006 seed: `collapsed=True` returns no groups — LLR-007.1's nav exclusion is half-built). The `✓ N` summary row and selection relocation (`_select_first`, `app.py:371-377`) are the new work; the F-7 ruling (selection relocates to nearest non-collapsed column) is pinned in HLR-007.

---

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | ≤4 source files, or reason declared | ✓ | 2/4 (models.py, views.py) — §2 |
| 2 | Tests written in this same increment | ✓ | 7 new nodes — §2/§4 |
| 3 | Layer 0 written where the criterion applies | ✓ | 4 model units on the getter/setter/rename seats + header boundary table — §4 Layer A |
| 4 | RED counterfactual captured and restored by hash | ✓ | A (`>=` burn) + B (write-on-read), hashes `c56c7607…`/`d96e3158…` re-proven, `__pycache__` cleared per cycle — §4 |
| 5 | Reverse census run on every touched symbol | ✓ | B1 re-run and reconciled against 02-review-architect §1 (zero `_windowed_header`/`wip_limit` asserters confirmed); B2/B3 non-fires; A3 additive — §4 |
| 6 | `code-reviewer` passed — a HIGH blocks | ⚠ | Not invoked by this agent; left for the orchestrator's review gate (declared per notice convention) |
| 7 | No file from another lane touched | ✓ | Batch not forked |
| 8 | Frozen interfaces untouched | ✓ | `rename_phase` signature unchanged (sole caller `modals.py:874` compiles/runs green); `_windowed_header` private, both call sites updated — §4 |
| 9 | Coverage claims verified on disk, not from intent | ⚠ | pytest tail pasted from complete runs; ONE environmental red (`test_win_clipboard_roundtrip`, OS clipboard locked — evidence pasted §4), 804/804 relevant green |
