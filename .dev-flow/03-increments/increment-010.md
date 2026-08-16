# Increment 010 — R-11 · Weekly standup modal (`S`) + AT-019 full aperture sweep (FINAL)

| Field | Value |
|---|---|
| Batch | `2026-08-14-batch-04` |
| Increment | `010` (Increment 6 of the batch — FINAL) |
| Lane | — (batch not forked) |
| Requirement(s) | R-11 / HLR-011 / LLR-011.1 (`standup_query`) / LLR-011.2 (`StandupModal`) · HLR-012 / LLR-012.1 (`S` four-seat row of §3.0) |
| Acceptance | AT-018 (modal lists the week grouped, ✓/→ marks, 7d-in/8d-out, empty week, esc, mutates nothing) · AT-019 (all 13 §3.0 keys dead on the aperture, seat-derived) · TC-014 (window boundaries, grouping, done marks, empty query) · TC-015 (keymap + legend module gates green with `S` aboard) |
| Agent | `software-dev` (supervised-incremental-development) |
| Date | 2026-08-15 |

---

## 1 · What changed

**BLUF: `S` opens a read-only weekly standup modal — what moved (`→`) and what closed (`✓`) in the last 7 days, grouped per project with an Inbox section last and a recomputed `closed/total` line under each — derived ENTIRELY from the `phase_changed` stamp the board already keeps. Nothing new is stored; a quiet week says so in one honest line ("Nothing moved this week."). The modal closes on `escape`/`q`/`S` and mutates nothing (asserted byte-equal across open+close). AT-019 sweeps the FULL §3.0 key set (13 physical keys, read off the seat) across the aperture: nothing reaches the hidden board.**

- **`standup_query(board, today, show_archived)`** (`taskboard/models.py`, module-level pure function after the `Board` class — LLR-011.1's "models.py or views.py", placed beside `days_in_phase`'s sibling helpers): window `today−7 ≤ parse_iso(phase_changed) ≤ today` — the boundary day IN, 8 days OUT, None OUT (unknown is not zero, the `days_in_phase` law), corrupt OUT (`parse_iso` leniency), and a FUTURE stamp OUT (the window closes at today — a pin beyond the spec's text, flagged §6). Groups follow `visible_projects` order (never `board.tasks` order); any mover not under a visible project (project-less, or its project left the visible set) lands in Inbox LAST; empty groups produce NO section (the legend's no-ghost law applied to the week). Each task is annotated `(task, done)` with `done` read off `board.is_done` — the terminal-phase seat, not the literal string "Done", so a renamed terminal phase still reads as closed.
- **`StandupModal`** (`taskboard/modals.py`, after `LegendModal` — the pattern LLR-011.2 mandates): `ModalScreen[None]`, BINDINGS `escape`/`q`/`S` → one `action_close` (grep shows no other `def action_` — read-only by construction, the LLR-011.2 inspection condition). Content composed at OPEN time from `standup_query`: title `Standup · week ending <today>`, per project a `▐ Name` section, rows `  ✓ title  phase` / `  → title  phase`, and a dim `  n/m closed this week` fold per project. Every title/name/phase passes through the same `rich.markup.escape` the modals already use (`modals.py:23`).
- **`action_standup`** (`taskboard/app.py`, beside `action_report`): pushes the modal with the live board and the current `show_archived`; `"standup"` joins `BOARD_ACTIONS` (what drops it on the aperture — the AT-019 RED hook).
- **`keymap.py`:** ONE entry `Key("S", "S", "standup", "Standup")` before the arrow block (AMD-03 placement), GLOBAL (`views=None`) — the standup reads the board in any view, like `R`; the shifted-key precedent (X/P/R) holds.
- **README keybinding table:** one `S` row after `u` (outside the source count). The keymap enforcement trio (`test_keymap.py`) and the legend pins (`test_legend.py`) pass unchanged — the bar laws re-derive from the seat.

The prototype (`prototypes/kanban_ideas/proto.py:169-192`, K11) was the shape reference; the spec won every conflict (§6).

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count. SOURCE: 4/4.**

| File | Kind | Change |
|---|---|---|
| `taskboard/models.py` | source | `standup_query(board, today, show_archived)` — the pure window/grouping seat (LLR-011.1) |
| `taskboard/modals.py` | source | `StandupModal` — derived content, three close bindings, no mutation path (LLR-011.2) |
| `taskboard/app.py` | source | `action_standup` + `StandupModal` import + `"standup"` in `BOARD_ACTIONS` |
| `taskboard/keymap.py` | source | ONE `S` entry before the arrow block |
| `README.md` | docs (outside count) | 1 keybinding row (`S`) |
| `tests/test_app.py` | test | 4 new nodes: `test_standup_action_is_registered_and_guarded`, `test_standup_modal_lists_the_week_grouped_and_marked` (AT-018), `test_standup_modal_empty_week_says_so_in_one_line` (AT-018 empty limb), `test_all_batch_keys_are_dead_on_the_aperture` (AT-019) + 2 shared helpers |
| `tests/test_momentum.py` | test | 4 new nodes (TC-014): window boundaries, grouping/order/no-ghosts, done-mark terminal-phase + count fold, empty query |

---

## 3 · How to test

```bash
python -m pytest tests -q --deselect tests/test_app.py::test_win_clipboard_roundtrip   # full gate: MUST be 0 failed
python -m pytest tests/test_app.py -k "standup" -q                                      # AT-018 + registration (HLR-011 selector)
python -m pytest tests/test_momentum.py -k "standup" -q                                 # TC-014 (LLR-011.1 selector)
python -m pytest tests/test_app.py -k "aperture" -q                                     # AT-019 (HLR-012 selector)
python -m pytest tests/test_keymap.py tests/test_legend.py -q                           # TC-015 module gates
PYTHONIOENCODING=utf-8 python prototypes/verify_aperture.py                             # aperture law (ALL PASSED)
```

---

## 4 · Test results

**One complete run, post-restore, after all three RED cycles. Tail read from THAT run's own output:**

```
.......................................                                  [100%]
831 passed, 1 deselected in 67.32s (0:01:07)
```

**Aperture harness:**

```
  [PASS] the hero leg is not vacuous: some languages really do compose the detail line into the panel at 118x34 (the rest are a regression guard, and this check is what would notice the last one going away)  3/10: ['swiss', 'industrial', 'darkside']

ALL PASSED
```

**TC-015 module gates (with `S` aboard — no re-measure needed, the laws re-derive):**

```
...................................                                      [100%]
35 passed in 3.38s
```

### RED counterfactuals — executed, not predicted

Mutations applied to `taskboard/models.py` one at a time, restored from a byte-copy (`cp`, no `sed -i`), `__pycache__` cleared after EVERY mutation/restore cycle (C-46), restore hash-confirmed against the pre-mutation `sha256 = 49ff0b6fad0877b8f61115951f928f49d2d9cedfe9018afc44ef449a643cfcf4` after each cycle.

**(a1) window off-by-one, `week_ago <= d` → `week_ago < d` (the `> 7` form) → the 7d-IN limbs red:**

```
>       assert shown == {"w-today", "w-seven"}
E       AssertionError: assert {'w-today'} == {'w-seven', 'w-today'}
tests\test_momentum.py:338: AssertionError
>               assert title in text, f"{title} is missing from the standup"
E               AssertionError: BOUNDARY7 is missing from the standup
tests\test_app.py:3889: AssertionError
2 failed in 0.97s
```

**(a2) window widened, `timedelta(days=7)` → `timedelta(days=8)` → the 8d-OUT limbs red (the leak shows in the derived set AND moves the recomputed count line):**

```
E       AssertionError: assert {'w-eight', '...n', 'w-today'} == {'w-seven', 'w-today'}
E         Extra items in the left set:
E         'w-eight'
E               AssertionError: Alpha's count line is wrong or missing
E               assert '1/3 closed this week' in '...→ OUTEIGHT Backlog\n  1/4 closed this week...'
2 failed in 0.97s
```

**(b) derivation reads a stored field that does not exist, `parse_iso(t.phase_changed)` → `parse_iso(t.extra.get("moved_this_week"))` → the derivation limbs red (the modal reports an empty week while the fixture moved):**

```
E               AssertionError: MOVEDTODAY is missing from the standup
E               assert 'MOVEDTODAY' in 'Standup · week ending 2026-08-15\nNothing moved this week.\nS or esc closes'
E       AssertionError: assert set() == {'w-seven', 'w-today'}
E       ValueError: not enough values to unpack (expected 1, got 0)
3 failed in 0.87s
```

### Signed-balance test ledger

| | nodes |
|---|---|
| Inc 5 close (declared) | 824 |
| + `tests/test_app.py` Inc-6 (registration, AT-018, AT-018-empty, AT-019) | +4 |
| + `tests/test_momentum.py` Inc-6 (TC-014 ×4) | +4 |
| **Inc 6 close (measured: 831 passed + 1 deselected)** | **832** |

---

## 5 · Risks

- **The standup is only as honest as the stamp.** Boards written before `phase_changed` existed show an empty week — that is the intended behavior (unknown is not zero), and the empty line says so rather than inventing motion. The seeded demo board has no in-window stamps either, so a first-run `S` reads "Nothing moved this week." — correct, and worth knowing before a demo.
- **Focus mode does not scope the standup** (HLR-011 says "every visible task"; the focus is a kanban view posture). `show_archived` DOES scope it (the modal receives the app's live flag, the LegendModal convention). Flagged in §6.
- **A task stamped in the future is excluded** (`≤ today`). A clock-skewed stamp is not motion; if that ever hides real work the pin is one limb in `test_standup_window_seven_days_in_eight_out_none_out`.

---

## 6 · Pending items / spec deviations

1. **Count-line language (flagged, resolved toward the spec).** The increment brief quoted the prototype's Spanish `n/m cerradas esta semana`; the batch's artifact language is English and every shipped modal string is English (the `LegendModal` "Nothing is drawn on this board yet." precedent). HLR-011 mandates the marks and the empty message but not the count line's wording; the prototype is reference-only ("the SPEC wins"). Shipped: `n/m closed this week`, empty line `Nothing moved this week.`, title `Standup · week ending <today>`. If the operator wants the Spanish copy it is a three-string change in `StandupModal.compose`.
2. **Count arithmetic is pinned in AT-018 (pilot), not in a `test_momentum` unit.** The fold (`sum(done)/len(group)`) is composed in the modal; `StandupModal.compose` cannot run outside an app (Textual compose context), so the recomputed-fraction limb lives in the pilot test. TC-014 pins the query's `(task, done)` annotations the fold consumes — the mutation space between the two is one line.
3. **Future-stamp exclusion is a pin beyond the spec's text** (HLR-011 writes the window as "within the last 7 days"; LLR-011.1 writes `today−7 ≤ stamp ≤ today` — the `≤ today` half is implemented and asserted, so it is spec-faithful, but the AT set never names a future stamp; TC-014 does).
4. **AT-019's action list is the §3.0 declaration; the physical keys are seat-derived.** The 12 actions are spelled in the test (they ARE the requirement); each entry's `.keys.split(",")` supplies the 13 physical presses (`=` alias included), with a `len(keys) == 13` guard so a split/merged alias reddens. A 14th batch key would still need a human to extend the tuple — no seat marks "batch-04 keys" as a set.
5. **Movers whose project is not visible fall to Inbox** (project-less, or an archived project with `v` off). LLR-011.1 groups by `visible_projects` and puts Inbox last; the fallback for "visible task, invisible project" was unspecified. It is implemented and behavior-verified (mover under an archived project lands in Inbox, last); the test pins only the project-less case — the archived-project limb is a pin gap, accepted and declared at Phase 4 (per the Inc-010 code-review nit).
6. **Owed to Phase 4 (out of this increment's scope):** the supersession-completeness sweep (template rule V-3), `verify_language.py` set-isolation run (01b §9), and the one complete Phase-4 gate (C-25, orchestrator-owned).

---

## 7 · Suggested next task

**Phase-4 close-out (orchestrator-owned, C-25):** one complete gate run of all four suites — `pytest tests/` (empty-red, achieved here: 831 passed / 0 failed / 1 deselected), `verify_aperture.py` (ALL PASSED, achieved), `verify_widget.py` + `verify_board.py` (failure SET equals the Phase-0 set), `verify_language.py` (L1 ⊆ L0 by failure NAME, never by count). Then the supersession sweep and the R-11 row of the coverage matrix. No batch scope remains: all thirteen §3.0 keys are live, documented, and dead on the aperture.

---

## Increment gate checklist

- [x] Requirements traced: HLR-011 / LLR-011.1 / LLR-011.2 / HLR-012 (`S` row) — each landed in the same increment (LLR-012.1)
- [x] AT-018 (2 nodes), AT-019, TC-014 (4 nodes) written; TC-015 module gates green (35 passed)
- [x] Full suite: **0 failed** (831 passed, 1 deselected) — post-restore run
- [x] `verify_aperture.py`: **ALL PASSED**
- [x] RED counterfactuals EXECUTED (a1, a2, b), restored byte-exact (sha256 confirmed ×3), `__pycache__` cleared each cycle
- [x] Source budget: **4/4** declared
- [x] LLR-011.2 inspection: three close bindings present; `def action_` inside `StandupModal` shows only `action_close`
