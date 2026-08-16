# Increment 005 — R-01 + R-02 · Quick keys: `[`/`]` phase move, `!` priority, `b` blocked (+ HLR-012 seats)

| Field | Value |
|---|---|
| Batch | `2026-08-14-batch-04` |
| Increment | `005` (Increment 1 of the batch) |
| Lane | — (batch not forked) |
| Requirement(s) | R-01 / HLR-001 / LLR-001.1 · R-02 / HLR-002 / LLR-002.1, LLR-002.2 · HLR-012 / LLR-012.1, LLR-012.2 (this increment's seats) · §3.0 key-registration contract · §6.5 AMD-03 width law |
| Acceptance | AT-001, AT-002, AT-003, AT-004 (Layer B, Pilot) · TC-001, TC-002 (Layer A) · unit `next_priority` · legend KEYS pins |
| Agent | `software-dev` (supervised-incremental-development) |
| Date | 2026-08-15 |

---

## 1 · What changed

**BLUF: the four dead keys are alive, the suite is green, and the key bar's 96-cell law is now measured instead of predicted.** The pre-batch session had bound `[` `]` `!` `b` in `KEYMAP` and listed their actions in `BOARD_ACTIONS` but never wrote the handlers or the README rows — 3 tests red. This increment:

- `action_phase_move(delta)` (app.py, beside `action_hmove`): computes the clamped target phase and routes the move through `Board.set_task_phase` — the ONLY stamping seat (models.py:1011). On a True return it saves and refreshes; on a clamped/no-op target it does nothing at all (no wrap, no re-stamp, no save, no re-render).
- `action_prio_cycle` / `action_toggle_blocked`: cycle priority via the new pure helper `next_priority` (models.py, beside `TASK_PRIORITIES` at :49; unknown → `normal`) and flip `blocked`; both save + refresh. Render markers (`!` token, `▲`/`▊` prefix) were already shipped in views.py.
- README keybinding table: rows for `[` `]`, `!`, `b` (the exact `Key.show` spellings the enforcement test parses).
- `LegendModal` KEYS section (LLR-012.2): the current view's live keys derived from `keymap.bar_keys(view)` — never hand-written, so a key the narrow bar drops stays one `?` away.
- The two width-law tests re-specified per AMD-03/P-14: all expected widths are DERIVED from the raw `KEYMAP` tuple at assert time (`len(SEP.join(...))`), so the constants can never silently go stale again. Executed values recorded in the docstrings: no-word 85/85/85/88 cells, full-word 273/273/273/283 (29/29/29/30 keys).

Undo (LLR-010.1, R-10/Inc 5): the LLR declares the undo stack itself as "NEW — created in Phase 3" at its own increment and declares no Inc-1 integration point — so no seam was added (per the batch brief: nothing more). The three new actions each perform exactly one mutation then save + refresh, which is the shape the Inc-5 snapshot hook needs.

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

| File | Kind | Change |
|---|---|---|
| `taskboard/app.py` | source | `action_phase_move` / `action_prio_cycle` / `action_toggle_blocked`; `next_priority` import |
| `taskboard/models.py` | source | `next_priority` pure helper beside `TASK_PRIORITIES` |
| `taskboard/modals.py` | source | `LegendModal` KEYS section from `bar_keys(self._mode)` |
| `tests/test_app.py` | test | AT-001, AT-002, TC-001, AT-003, AT-004 + helpers (`_key_for`, `_ops_board`, `_painted_column`, `_card_row`) |
| `tests/test_keymap.py` | test | `test_at_a_normal_width_nothing_is_dropped_at_all` and `test_the_widest_bars_keep_their_words` re-specified (derived widths, measurement method in docstrings) |
| `tests/test_momentum.py` | test | `next_priority` unit (LLR-002.1); TC-002 pins re-confirmed |
| `tests/test_legend.py` | test | 2 KEYS-section pins (exact per-view rows; scope limbs) |
| `README.md` | doc | 3 keybinding rows (`[` `]`, `!`, `b`) |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 4 (uncapped) |
| Doc files | 1 (README) + this packet (outside the count) |

`keymap.py` was NOT touched: the four `Key(...)` entries already sat BEFORE the arrow block (`keymap.py:54-57` vs arrows at :72-75), satisfying the AMD-03 placement rule as found — verified by mutation F below.

---

## 3 · How to test

```bash
python -m pytest tests -q                                              # full gate: MUST be 0 failed
python -m pytest tests/test_app.py -k "phase_move or prio_cycle or toggle_blocked" -q   # AT-001..004 + TC-001
python -m pytest tests/test_momentum.py -q                             # TC-002 pins + next_priority
python -m pytest tests/test_keymap.py tests/test_legend.py -q          # width laws + KEYS section
PYTHONIOENCODING=utf-8 python prototypes/verify_aperture.py            # aperture law (UTF-8 forced: cp1252 console)
```

---

## 4 · Test results

**One complete run. Tail read from THAT run's own output:**

```
........................................................................ [ 91%]
..................................................................       [100%]
786 passed in 51.12s
```

`verify_aperture.py` — final lines of the same run:

```
  [PASS] the hero under test is the DEADLINE's reading, and its detail is the user's TITLE — the reason `hero.py` escapes at all  deadline: '[URGENT] rotate keys'
  [PASS] the hero leg is not vacuous: some languages really do compose the detail line into the panel at 118x34 (the rest are a regression guard, and this check is what would notice the last one going away)  3/10: ['swiss', 'industrial', 'darkside']

ALL PASSED
```

The 3 known batch-scope reds (`test_every_shown_key_has_a_real_action_on_the_app`, `test_the_readme_keybinding_table_matches_the_seat`, `test_the_widest_bars_keep_their_words`) are CLOSED — the failure set is empty, per the PLAN ledger's Phase-4 green definition.

Aperture law for the NEW keys specifically (the harness's fixed list predates them; AT-019's 13-key sweep is Phase-4 scope). Executed probe: board opened, `6` pressed, then `[` `]` `!` `b` on the aperture —

```
aperture still top after [ ] ! b: True
board file byte-unchanged: True
```

| Layer | Nodes | Result |
|---|---|---|
| **0 · unit** | `tests/test_momentum.py::test_next_priority_walks_the_declared_order_with_wraparound` (pure seat, LLR-002.1: 4 order assertions incl. unknown→normal) | 1 passed |
| **A · white-box** | `tests/test_app.py::test_phase_move_clamps_unknown_phase_into_bucket_zero` (TC-001) · TC-002 = existing `tests/test_momentum.py:44-59` stamping pins — re-confirmed green (13/13 module) inside the full run | passed |
| **B · black-box** | `test_phase_move_forward_dates_the_move` (AT-001) · `test_phase_move_round_trip_restamps_and_the_ends_are_silent_no_ops` (AT-002) · `test_prio_cycle_walks_the_declared_order_and_paints_the_marker` (AT-003) · `test_toggle_blocked_flips_the_flag_and_the_card_prefix` (AT-004) · 2 legend KEYS pins (LLR-012.2) | 6 passed |

### RED counterfactual — executed, not predicted

Six mutations, each applied in my own tree, each reddening exactly the named limb, each restored and PROVEN by hash (`sha256sum` back to the pre-mutation value; mutations run with `PYTHONDONTWRITEBYTECODE=1`):

| # | Mutation applied | Reddened node(s) | Restore proven by |
|---|---|---|---|
| A | `action_phase_move` assigns `task.phase` directly, bypassing `set_task_phase` (the F-2 trap) | AT-001, AT-002, TC-001 red — and AT-002's failing assertion was the STAMP limb (`assert None == '2026-08-14'`) while the phase limb (`t.phase == "Review"`) stayed green, the exact discrimination the AT was built for | `taskboard/app.py` hash → `28536c5fb779…` ✓ |
| B | clamp replaced by wrap (`idx % len(phases)`) | AT-002 no-op limb + TC-001 red (2 failed) | same hash ✓ |
| C | `next_priority` direction inverted (`+1` → `-1`) | AT-003 + `next_priority` unit red (2 failed) | `taskboard/models.py` hash → `473dba960f03…` ✓ |
| D | `toggle_blocked` writes but never clears (`= True`) | AT-004 red (1 failed) | `taskboard/app.py` hash ✓ |
| E | legend KEYS section hard-coded to `bar_keys("kanban")` | both LLR-012.2 pins red (2 failed) | `taskboard/modals.py` hash → `d3a2638d75b4…` ✓ |
| F | the four quick-key `Key(...)` entries moved AFTER the arrow block (AMD-03 placement violated) | `test_at_a_normal_width_nothing_is_dropped_at_all` red (law limb 4: arrows must drop before the new keys) | `taskboard/keymap.py` hash → `4f4a905ab81a…` ✓ |

Transcript sample (mutation A, AT-002):

```
            assert t.phase == "Review"
>           assert t.phase_changed == today
E           AssertionError: assert None == '2026-08-14'
```

Incident during B (recorded, resolved): the first restore used `sed -i`, which silently stripped the repo's CRLF line endings from `app.py` — caught BECAUSE the hash did not return to its pre-mutation value (`4ab1ec…` ≠ `28536c…`), diagnosed to CRLF→LF (the CRLF re-encode of the content matches the pre-mutation hash exactly), and repaired by re-encoding CRLF: hash back to `28536c5fb779…` ✓, tests re-run green. The remaining mutations used byte-level Python edits. The hash-restore rule did its job.

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by other tests | `grep -rln "next_priority" taskboard/ tests/ prototypes/` | `app.py` (consumer, this increment), `test_momentum.py` (this increment) — no pre-existing consumers |
| B1 | `grep -rln "LegendModal\|bar_keys" taskboard/ tests/ prototypes/` | `app.py` (imports/pushes — unchanged call sites), `tests/test_legend.py`, `prototypes/verify_aperture.py` — ALL PASSED post-change |
| B2 file moved on disk | — | did not fire: no file moves |
| B3 byte-identical goldens | `ls tests/goldens` | did not fire: no such directory |
| B4 artifact consumed elsewhere | packet path convention | consumed by `.dev-flow/04-validation.md`, `BACKLOG.md`, `PLAN.md` (repo convention, root `03-increments/` as increments 001–004) |
| A3 interface consumed by another module changed | `bar_keys`, `LegendModal`, `set_task_phase` signatures | did not fire: all changes additive (new optional compose section, new helper, new actions); no signature touched |

### Signed-balance test ledger

`post = base − deleted + added` → `786 = 778 − 0 + 8` ✓ reconciles (5 in test_app.py + 1 in test_momentum.py + 2 in test_legend.py; the 2 re-specified keymap nodes were edited in place; the 3 former reds are inside the 786 green)

---

## 5 · Risks

- **Undo seam absent by design** (LLR-010.1 is Inc 5): if Inc 5's design changes, these three actions are where the snapshot hook lands. The actions' single-mutation-then-save shape is the intended hook point.
- **AT-019 (13-key aperture sweep) is Phase-4 scope**: this increment probed only its own four keys on the aperture (pasted above). Keys landing in Inc 2–6 must each join `BOARD_ACTIONS` or the aperture leak reopens.
- The amended 96-cell law holds today partly because nothing drops at 96 yet (bare widths 85/88 < 96); when Inc 2's `s g z F` entries push the kanban bar past 96, the law's drop-order limbs (arrows before new keys, universals last, exact `+N`) become load-bearing — they are asserted at swept widths, not only at 96, so they already bite.

## 6 · Pending items / spec deviations

- **Node id kept while its law changed** (flagged, not silently chosen): `test_at_a_normal_width_nothing_is_dropped_at_all` was re-specified to the AMD-03 amended law but retains its name because HLR-012 and LLR-012.1 reference that node id. The name now understates the body (it asserts the degradation law across a sweep, and zero-drops-at-96 only via the derived bare width). Rename candidate at Phase 4 id reconciliation (V-5).
- **AT-002 "RE-DATES" observability** (flagged): a same-day re-stamp is value-identical to a kept stamp, so the test backdates the stamp to `2000-01-01` mid-test (fixture doctoring, in-memory + save) before pressing `[` — this is what makes "the clock restarts" discriminating. Interpretation of the AT's intent, recorded.
- **AT-003 fixture start value** (flagged): requirements AT-003 starts at default `normal`; 01b AT-K02 starts at non-default `low`. Requirements is law → implemented as written (normal start); the non-default value `low` is still driven AND observed by the wrap limb (high→low→normal), so the cycle's full order is covered either way.
- **TC-001 fixture route** (flagged): `Board.load` snaps unknown phases at load (models.py:868-869), so the unknown-phase task cannot arrive through a file. The test swaps an in-memory board into the running app (docstring records why); the load-time snap and the live-path `phase_index` fallback are different seats, and this test pins the latter.
- **P-14 draft number vs. executed number**: the draft recorded "280 cells (30 keys)"; executed at Inc 1 the full-word widths are 273 (29-key views) / 283 (kanban, 30 keys). The re-specified tests DERIVE the widths at assert time, so the discrepancy is documentary only; the docstrings record the executed values and method.
- **LLR-012.2's `s g z F`/`escape` pin** (flagged): those keys land in Inc 2/5 and cannot be pinned today. The KEYS test asserts EXACT equality against the raw seat per view, so it extends to them automatically the moment they are declared — plus an explicit `tab`-scope limb as the discriminating precedent.
- **Line endings**: `tests/test_legend.py` append was normalized to the file's CRLF convention after detection (the `test_app.py`/`test_momentum.py` appends matched their files' LF). No other file's endings were altered (the `app.py` CRLF incident above was repaired).

## 7 · Suggested next task

**Inc 2 — R-03 + R-04 (K2 sort `s`, K3 group `g`)**: the batch's named top risk (nav/render parallel model). Land the shared `kanban_order(...)` seat in views.py with the parity oracle (01b §4), the two kanban-scoped KEYMAP entries (before the arrow block, `views=("kanban",)`, view-guarded actions), README rows, and the BOARD_ACTIONS memberships. Note: the kanban bar crossing 96 cells is EXPECTED and now lawful — the re-specified width test is built for it.

---

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | ≤4 source files, or reason declared | ✓ | 3/4 — §2 |
| 2 | Tests written in this same increment | ✓ | 8 new nodes + 2 re-specified — §2/§4 |
| 3 | Layer 0 written where the criterion applies | ✓ | `next_priority` pure seat unit, 4 assertions — §4 Layer 0 |
| 4 | RED counterfactual captured and restored by hash | ✓ | 6 mutations A–F, hashes pasted — §4 (incl. the CRLF incident the hash rule caught) |
| 5 | Reverse census run on every touched symbol | ✓ | B1–B4 + A3 probes incl. non-fires — §4 |
| 6 | `code-reviewer` passed — a HIGH blocks | ⚠ | Not invoked by this agent; left for the orchestrator's review gate (declared per notice convention) |
| 7 | No file from another lane touched | ✓ | Batch not forked |
| 8 | Frozen interfaces untouched | ✓ | A3 probe: additive only — §4 |
| 9 | Coverage claims verified on disk, not from intent | ✓ | pytest tail pasted from one complete run (786 passed); verify_aperture `ALL PASSED` pasted; aperture probe executed — §4 |
