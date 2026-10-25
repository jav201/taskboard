# Increment 001 — HLR-2801..2804 · `the board shows behind the start-up modals`

| Field | Value |
|---|---|
| Batch | `2026-10-25-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2801 v2 · HLR-2802 v2 · HLR-2803 v2 · HLR-2804` / `LLR-2801.1 v2 · LLR-2801.2 · LLR-2801.3 v2 · LLR-2802.1 · LLR-2803.1` |
| Acceptance | `AT-2801` · `AT-2802` · `AT-2803` (white-box `TC-2801`, a labelled pin) · regression pin `AT-2804` (the P4 suite) |
| Agent | `software-dev` (the orchestrator, under this budget) |
| Date | `2026-10-25` |

---

## 1 · What changed

The start-up modals — the one-time milestone offer and the team identity
picker — now open over the visible board, dimmed by the same `#0007` translucent
backdrop the working modals use, on the single-board start, the home's `enter`
path and in team mode, at 118x30 and 80x24. The user reaches this surface at
every app start that owes a start-up modal.

Mechanism: one background-only declaration in `taskboard/taskboard.tcss`
(`MilestoneOffer, TeamIdentityPicker { background: #0007; }`), per
`PDR-2026-10-25-batch-01#D2`. No timing change (the commission's unpainted-board
hypothesis was refuted by measurement at P1; the board beneath already paints in
the same first composite as the modal), no `app.py`/`modals.py` change, push
order untouched (picker first, offer last, D-615). The picker's top-left
placement is preserved exactly — the PDR's D1 — because joining the shared
backdrop rule would have dragged its `align: center middle` onto the picker
(P2 blocker A1).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/taskboard.tcss` | source | LLR-2801.1, LLR-2801.2, HLR-2801..2803 | adds the background-only declaration (7 lines with comment); no other rule touched |
| `tests/test_startup_backdrop.py` | test | US-001, HLR-2801..2803, LLR-2801.1..2803.1 | new — the four nodes (AT-2801/2802/2803 + TC-2801) |
| `tests/test_milestone_offer.py` | test | HLR-2804 (pin) | one node scoped to the offer box (see §6) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 (outside the count) |

- The commission's increment clause expected `taskboard/app.py` only; the
  diagnosis (SB-1) placed the cause in the stylesheet, and the PDR's condition 2
  has this statement supersede the expectation — the touch set is
  `taskboard/taskboard.tcss` + one new test file, nothing else (`git diff` below).

## 3 · How to test

```bash
# the increment's own nodes
env -u NO_COLOR python -m pytest -q tests/test_startup_backdrop.py
# the affected suites (offer, home, team, B1 observers)
env -u NO_COLOR python -m pytest -q tests/test_startup_backdrop.py tests/test_milestone_offer.py tests/test_home_deferred_start.py tests/test_boards_home.py tests/test_boards.py tests/test_markup_sites.py tests/test_team_sync.py
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` | none due — the change is one CSS declaration; cyclomatic 1, no module boundary crossed | n/a |
| **A · white-box** | `core` | `test_TC_2801_quitting_with_the_picker_open_writes_nothing` (pin) — the contract §5.1 resolved-style probe (`styles.background` carries alpha) is superseded by the emitted-form render assertion + the mutation battery (C-42), both strictly stronger; it is not run as a separate arm (code review F1) | 1 passed |
| **B · black-box** | `core` | `test_AT_2801_the_offer_opens_over_the_painted_board[size0|size1]` · `test_AT_2802_enter_on_the_home_opens_the_offer_over_the_chosen_board[size0|size1]` · `test_AT_2803_team_mode_shows_the_board_behind_both_modals_in_todays_order[size0|size1]` · `test_AT_2803_the_picker_keeps_its_pre_batch_geometry` | 7 passed |

Affected suites: 144 passed, 0 failed (`evidence/suite-001.txt`); the B1
observer suites: see the **Reverse census** field (`evidence/suite-002.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the background-only declaration deleted from `taskboard/taskboard.tcss` (7 lines, anchor verified present before the run) |
| Instrument | project code: `evidence/mutation-001.py` (a runner in the project's stack, kept beside its transcript) |
| Where it ran | this worktree, `C:\Users\jjgh8\Github\taskboard-wt\backdrop`, run by the orchestrator; no other session reads this tree |
| Transcript | `evidence/mutation-001.txt` — `mutated: 0f9308b4…` confirms the mutation applied; every AT arm then resolved |
| Restore proven by | file hash returned to its pre-mutation value: `before: 4ed77a16c2dd067bcc8c6152e0f39e9708b3638274378940f8eb575717389fe4` == `restored: …`, `restore-ok: True` |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` |
| Arms resolved at baseline | **8** — six parametrized AT arms + the geometry arm + TC-2801, one pytest invocation each, exit code read per arm |
| Verdict granularity | per resolved node id (each arm is its own pytest run) |
| Arms that stayed GREEN | `AT-2803 geometry` (the mutation removes the backdrop, which never moves the box — that arm guards the A1 recentering shape, named inert for THIS mutant) · `TC-2801` (a labelled pin: a stylesheet cannot change writes) |

| Field | Value |
|---|---|
| **RED counterfactual** | `taskboard/taskboard.tcss` — the `MilestoneOffer, TeamIdentityPicker { background: #0007; }` declaration deleted → `test_AT_2801_the_offer_opens_over_the_painted_board[size0|size1]` both RED (opaque screen returns, 0 rows outside the box) · `.dev-flow/2026-10-25-batch-01/evidence/mutation-001.txt` · restore digest `4ed77a16c2dd067bcc8c6152e0f39e9708b3638274378940f8eb575717389fe4` |

| Field | Value |
|---|---|
| **Mutation verdicts** | AT-2801 118x30 · declaration delete · **KILLED** · `evidence/mutation-001.txt` · restore `4ed77a16…` · AT-2801 80x24 · **KILLED** · AT-2802 118x30 · **KILLED** · AT-2802 80x24 · **KILLED** · AT-2803 118x30 · **KILLED** · AT-2803 80x24 · **KILLED** · AT-2803 geometry · **SURVIVED** (inert for this mutant, named above) · TC-2801 · **SURVIVED** (pin by design) · arms that stayed GREEN: named per node above — none unexplained |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the mutation runner `evidence/mutation-001.py` | its own anchor check: the script asserts the mutation anchor is present before running (`assert ANCHOR in src`) | would end `BAD` — demonstrated live: the runner's KILLED verdicts under the applied mutation are the same instrument reporting failure per arm |
| the AT oracle itself | the base regime (declaration absent, measured at P1 and again at base in `evidence/red-p1.txt`): 0 rows outside the box at both sizes | `assert above + below > 0` fails — the instrument's RED side is the P1 measurement itself |
| the suite | `test_TC_617_rows_order_marks_and_keys` failed on the first fixed-tree run (its oracle encoded the opaque backdrop) | `AssertionError: at == sorted(at)` — later scoped (§6) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown RED before its PASS was believed (the mutation runner's per-arm KILLED verdicts, the oracle's P1-measured 0-count regime, the suite's own first-run failure) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the terminal frame (the emitted surface) | the AT oracle reads the composited full-screen-stack render — the same source `App.export_screenshot` consumes — and counts non-blank rows outside the box's corner glyphs; the P2 round-2 probe ran both states back-to-back | base: `[0, 0]` outside rows · fixed: `[7, 6]` at 118x30, `[4, 3]` at 80x24 — measured against the render, not against a description of it (`evidence/red-p1.txt`, the round-2 probe) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 1 artifact (the terminal frame), asserted against the emitted composited render; what it returned is pasted above |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-000.txt | .dev-flow/2026-10-25-batch-01/evidence/suite-000.txt | dd0603729a7b6f064afd25b2015515bb57ab2683221d5b5f446be0b0348eea1e |
| suite-001.txt | .dev-flow/2026-10-25-batch-01/evidence/suite-001.txt | 2583c02e4e309ba89aab09dd1cc241e4338c68d4e6e0ecfc281766fcd369e17e |
| suite-002.txt | .dev-flow/2026-10-25-batch-01/evidence/suite-002.txt | e6d6f66f091836e872a30be2e87c494925d5688ad154d2be913a3ecd94aef400 |
| mutation-001.txt | .dev-flow/2026-10-25-batch-01/evidence/mutation-001.txt | 4a4898ed240b9c13215a1c8134cff21d331d4742529de8f9340a65b2f62484f3 |
| mutation-001.py | .dev-flow/2026-10-25-batch-01/evidence/mutation-001.py | c8b55cb067d672acb129234e0d36244fde2b022b3b1f598ef3253bca7a527e88 |
| flake-2801.txt | .dev-flow/2026-10-25-batch-01/evidence/flake-2801.txt | 7422d475be549241a1241b023e13de6ad78550e4a60355fc315bf30ce8d79548 |
| flake-2801.py | .dev-flow/2026-10-25-batch-01/evidence/flake-2801.py | 7af7a764197f37aa39927c492cf548cd6fdd3b12407a200b9f4590da43bf292a |
| reverse-census-001.txt | .dev-flow/2026-10-25-batch-01/evidence/reverse-census-001.txt | d6644efdd5a29c4942628a7fdfd2a775a91df48015aecf472525ae13c6d2b19d |

| Field | Value |
|---|---|
| **Evidence files** | `8 artifact(s), each at the declared home, with the digest of its bytes on disk` |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | no — every claim is a presence claim (rows outside the box, the declaration's effect), measured, not absence-derived |
| If the result is an ABSENCE, what made the search wide enough | the B3 probe (no `tests/goldens` at all) and the B2 probe (no file moves) are absences — each has its positive control below |
| Guard labelled as protecting a CONCLUSION, not a behaviour | n/a |
| Conjunctive criteria: one mutation per conjunct | no conjunctive criterion — one declaration, one mutant |
| Synthetic instance of the absent case | the mutation battery IS the synthetic instance for the backdrop-absent case (it recreates the defect and the oracles go RED) |
| **Positive control for every probe that returned an ABSENCE** | B3: `grep -rl MilestoneOffer tests/` returns 12 files (the probe is not blind) while the golden grep returns none, because the tree has no `tests/goldens/` — uniformity not claimed · B2: `git status` shows the two real edits while the move-probe returns nothing |

### Reverse census — trigger family B, and A3

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl MilestoneOffer tests/` · `grep -rl TeamIdentityPicker tests/` · `grep -rl 0007 tests/` | 12 + 8 + 1 files (`evidence/reverse-census-001.txt`); only `tests/test_startup_backdrop.py` mentions `0007`; every other file drives the modals by keys/constructors and none asserts the screen background. The one changed existing node, `test_TC_617_rows_order_marks_and_keys`, re-validated and scoped (§6). The remaining observer files ran green in `evidence/suite-002.txt` (see the **Reverse census** field below) |
| B2 file moved on disk | `git status` rename probe | no moves |
| B3 byte-identical golden captures this source | `grep <source> tests/goldens/**` | no `tests/goldens/` directory exists; nothing to drift |
| B4 artifact produced here is consumed elsewhere | who reads the path/format written | none — the change emits no file |
| A3 interface consumed by another module changed | `git diff --stat` | the diff touches `taskboard.tcss` and two test files only; no interface another module consumes changed shape |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes of B1 · B2 · B3 · B4 · A3 run, each with its command and verdict in `evidence/reverse-census-001.txt` · B1: 21 file hits, 20 re-validated green by `evidence/suite-001.txt` (the offer/home/team/B1-adjacent suites) + `evidence/suite-002.txt` (the remaining observer files: test_boards_backlog_round, test_help_keys, test_milestones, test_milestone_offer_seam, test_modal_keys, test_present, test_present_hide, test_present_rulers, test_present_views_app), 1 re-validated by its scoped edit (§6) · B2/B4: no hits · B3: no goldens exist · A3: 0 foreign hits |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the offer oracle of `test_TC_617_rows_order_marks_and_keys` asserted row order over a render that the defect made opaque-only | tests that paint the start-up modals and index into the composited render | `grep -rl MilestoneOffer tests/` then read each hit's assertions | 1 | 1 (the node scoped to the box) | 0 — no other test indexes the composited render around the offer box |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated with its grep before the edit; the enumeration found exactly one site |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| none — no marker superseded | n/a | n/a | n/a |

### Signed-balance test ledger

`post = base − deleted + added` → `3256 = 3248 − 0 + 8` ✓ reconciles
(8 new nodes: 7 Layer-B arms/nodes + 1 Layer-A pin; the base of 3248 is the
commission's batch-02 close figure — re-counted exactly at P4's chunks.)

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` · PASS-WITH-NOTES, 0 HIGH / 2 LOW · both folded — F1: the §5.1 resolved-style probe's supersession is written into §4 (this table's Layer-A row) · F2: the geometry arm's docstring now says «bottom border row 11 (12 rendered rows)», matching the pinned tuple |

---

## 5 · Risks

- The 80x24 offer box is full-width with zero horizontal margin (pre-existing
  `#offer-box` layout, out of SB-3 scope); a very large candidate list can grow
  it to the full screen height, in which case no rows show around it — the fix's
  target (opaque → dimmed) holds regardless (contract LED-2801.2, ux C2).
- Under `TEXTUAL_ANSI` the fix is a framework-side no-op (the captures and the
  defect regime assume truecolor).
- The ~16 unlisted `ModalScreen` subclasses still render opaque screens — the
  backlog carry names them (P5 files the item).

## 6 · Pending items / spec deviations

- `test_TC_617_rows_order_marks_and_keys` (tests/test_milestone_offer.py:437)
  changed: its oracle indexed task titles over the whole composited render,
  which the defect had made opaque-only; with the translucent backdrop the
  board's own rows (carrying the same task titles) legitimately join the
  render, and at 118x30 they also flank the box's border row. The node now
  scopes `painted` to the offer box (corners found by glyph) — the assertion's
  intent, offer-row order inside the box, is unchanged. This is the packet's
  justification for the single existing-test edit (commission AT-d allows a
  change where an assumption must move; here a rendering-scope assumption,
  documented in the node's comment).
- PDR condition 2 (this touch-set statement) is discharged by §2 above;
  conditions 1 and 3 discharge at P5/P3 — the flake arm already ran (see
  below), the backlog item files at close.

## 7 · Suggested next task

Phase 4 (`stations/p4-validation.md`): the DDR, then the full suite in three
sequential chunks and the `b01-` captures.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_startup_backdrop.py` (8 nodes) |
| 3 | Layer 0 where it applies | ✓ | not due — cyclomatic 1 declaration, no boundary crossed |
| 4 | RED counterfactual | ✓ | §4 — mutation-001.txt, restore digest verified |
| 5 | Reverse census | ✓ | §4 — reverse-census-001.txt + suite-002.txt |
| 6 | `code-reviewer` passed | ✓ | §4b — PASS-WITH-NOTES, 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen; no interface changed |
| 9 | Coverage verified on disk | ✓ | suite-001.txt: 144 passed |
| 10 | Load-bearing emptiness | ✓ | §4 — no conclusion rests on an absence; positive controls named |
| 11 | Mutation verdicts | ✓ | §4 — per-arm KILLED/SURVIVED, inert arms named |
| 12 | Instrument RED-proof | ✓ | §4 — three instruments shown RED |
| 13 | Correction population | ✓ | §4 — one correction, enumerated before the edit |
| 14 | Emitted-form assertion | ✓ | §4 — asserted against the composited render |
| 15 | Independent review | ✓ | §4b — code-reviewer, 0 HIGH |
| 16 | Evidence files | ✓ | §4 — digests written by devflow-evidence.py |

## PDR condition discharge (this increment)

| # | Condition | Discharged? | The artifact line that proves it |
|---|---|---|---|
| 2 | the packet states the corrected touch set | ✓ | §2 — `taskboard/taskboard.tcss` + `tests/test_startup_backdrop.py`, superseding the commission's «expected `taskboard/app.py` only», with the SB-1 reason |
| 3 | the QA-P4-B01-flake arm runs with its transcript beside the mutation battery | ✓ | `evidence/flake-2801.txt` — 50/50 runs pass, min outside-box rows 4 above / 3 below at 80x24 (≥ 3) |
