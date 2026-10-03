# Increment 003 — HLR-309 (amended), LLR-309.2, LLR-301.2 · a band taller than the room is cut; the P4 record gaps

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`.
> A P4 `iterate-to-fix` (iteration 1: ux FAIL UXV3-1; qa PASS-WITH-NOTES G-001, G-003a, G-003b, G-004).

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-03` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-309 v3 (LLR-309.2 NEW), LLR-301.2 (the shared title seat), HLR-303 (the `at risk` note), HLR-307 (threshold) |
| Acceptance | AT-307 (re-parametrised) · white-box TC-311 (the cut), TC-302 (the title seats) |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**The board is never taller than the panel while a whole card fits.** A band taller than the room
left (the oracle board's `Later` band under `g g` at 80×24; a project band on a board of 14 highs)
used to be drawn whole and scroll — taking the head, the selected card's second row and the fold
row out of the panel (P4 UXV3-1). It is now cut on card boundaries around the selection, and the
fold row counts what the cut hides: `▲ 3 more in Later   ▼ 1 more in Later`. Walking `down` moves
the cut card by card; the approved frames are unchanged (nothing is cut there). The record gaps
the P4 qa pass found are closed: the widths transcript LED .17 cites now exists (G-001); the shared
title seat increment 001 moved onto `_literal` has a regression node per seat, RED on base
(G-003a); two old `test_app` nodes read the band-rule geometry instead of passing by accident
(G-004); two threshold texts are corrected (G-003b).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-309.2, LLR-309.1 | `_kanban_grouped` cuts a band taller than the room around the selection; `_fold_row` takes the cut and counts the cards above and below it |
| `tests/test_kanban_readable.py` | test | HLR-309, LLR-309.2, LLR-301.2 | AT-307 re-parametrised (oracle ×2, `g g` at 80×24, 14 highs at 118×30 and 80×24; the panel never scrolls); TC-311 the cut; TC-302 the shared title seat ×5 |
| `tests/test_app.py` | test | HLR-303, HLR-302 | `test_kanban_groups_by_project`, `test_kanban_marks_blocked_without_moving_it` read the band rules and the phase row's separators (G-004) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_kanban_readable.py -k "AT_307 or taller_than or shared_title_seat"
python -m pytest -q -p no:cacheprovider
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | the cut's window arithmetic through TC-311 | 1 passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-311 (the cut), TC-302 ×5 (the title seats), the two G-004 nodes | 7 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-307 ×5 | 5 passed |

Gate run on the frozen tree: `python -m pytest -q -p no:cacheprovider` → **1854 passed, 1 failed in 325.57 s — the failure is `test_app.py::test_win_clipboard_roundtrip`, whose own SETUP reports the Windows clipboard unavailable (the known environmental flake, BACKLOG); the P4 gate re-run is the run of record**
(`evidence/inc003-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the increment-002 tree with this increment's tests overlaid; the base tree likewise; the battery on the increment tree |
| Where it ran | scratch exports in the session scratchpad, never the live checkout |
| Transcript | `evidence/inc003-red.txt` (on the increment-002 tree: 4 failed — AT-307's horizon and 14-high arms, TC-311's cut); `evidence/inc003-red-on-base.txt` (11 failed — the title seats too); `evidence/inc003-mutations.txt` |
| Restore proven by | the battery's per-mutant sha256 check |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 13 on the increment-002 tree |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | on the increment-002 tree: AT-307's two oracle project arms (increment 001's laws, kept), the 5 title-seat arms (the fix shipped in 001 — RED on base), the 2 G-004 nodes (PINs of laws that hold) |

| Field | Value |
|---|---|
| **RED counterfactual** | AT-307's horizon arm and both 14-high arms and TC-311 RED on the increment-002 tree for the specified reason (the render taller than the panel, the viewport scrolled, the fold row past its bottom) · `evidence/inc003-red.txt` · the title-seat nodes RED on base `13745f6` (`a[b` printed for a-backslash-[b) · `evidence/inc003-red-on-base.txt` · restore digests in `evidence/inc003-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 12 distinct mutants, 12 KILLED on the final tree (`evidence/inc003-mutations-r2.txt`; specs `mutants_inc003.json`, `mutants_inc003_r2.json`): C1 no cut · C2 the cut ignores the selection · C3 not on a card boundary (round 1: SURVIVED — the 80×23 and rail-title arms added; KILLED) · C4 the cards above not counted · C5 no fold row for a cut alone (round 1: SURVIVED — the one-band arm added; KILLED) · C6 the title seat back on `escape` · F1 an exact fit cut · F2a counts clipped with nothing below · F2b a long cut name pushes `▼` off · F3 a lone first row at the bottom · F5 rail titles counted · F10 a one-sided `▲` row loses its names. Every restore digest OK |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| AT-307's "the panel never scrolls" check (`scroll_offset.y == 0`, rows == viewport) | the increment-002 tree under `g g` at 80×24 | FAILED on `td3` (`evidence/inc003-red.txt`) |
| the title-seat node | the base tree | `a[b` printed, the literal title absent — 5 of 5 FAILED |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments, each shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the cut board | the rendered rows (22 at panel 80×22) and the fold row's text | `▲ 3 more in Later` / `▼ 1 more in Later` |
| the painted app under `g g` and 14 highs | the viewport's scroll offset and the painted rows | never scrolled, both card rows inside |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts, each asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on the increment-002 tree | `.dev-flow/2026-10-02-batch-03/evidence/inc003-red.txt` | `df826dffbf36ca16f47b4fcbe397d3b63a29ef797dbbe617f1d8458bb1f0e83f` |
| RED on base | `.dev-flow/2026-10-02-batch-03/evidence/inc003-red-on-base.txt` | `d2c1d2a6b7cbb4058e926fb5f4469eb05ebeb503c23f8bd5744cd033786bd266` |
| RED of the round-1 node on the round-1 code | `.dev-flow/2026-10-02-batch-03/evidence/inc003-red-r1.txt` | `b21c6dbb263f23105406a76aa56c67695c5ff825da51a4a7dcd2a5f8d21d833c` |
| battery round 1 (C1–C6) | `.dev-flow/2026-10-02-batch-03/evidence/inc003-mutations.txt` | `46a3bb0c1241e8edb6b6520cfd98a85b51c42bb7adafab09e5b42a8ac88423de` |
| battery round 1, C3/C5 re-run | `.dev-flow/2026-10-02-batch-03/evidence/inc003-mutations-r1.txt` | `4bc3c3f54a914bc6bf9dc1b2f176cf83aa073faf41de5160f84eb7ad4b79513b` |
| battery on the final tree (C1–C6, F1–F10) | `.dev-flow/2026-10-02-batch-03/evidence/inc003-mutations-r2.txt` | `28d7b75164f25162e0b8bd6f79075c001147e40228f6524a3c9b4465958f52fc` |
| mutant specs | `.dev-flow/2026-10-02-batch-03/evidence/mutants_inc003.json` | `cb466887d520fe34c89e206b3a28622417c2e70955a0bd9b12205dd095e260bd` |
| mutant specs, round 2 | `.dev-flow/2026-10-02-batch-03/evidence/mutants_inc003_r2.json` | `acfd894927e1d34d1ccabe312ff9d01e66beb97abdb82a9b3ed9bb5bdef0179b` |
| spec generators | `.dev-flow/2026-10-02-batch-03/evidence/make_mutants_inc003.py` | `ee57063b3a72d5715b202e6efcec34fc83e42a111d36a658c97661c7668ce2d3` |
| spec generator, round 2 | `.dev-flow/2026-10-02-batch-03/evidence/make_mutants_inc003_r2.py` | `d4626a540f147ec6d171d394874995331adcf046811b6d1333fb40c268ebe289` |
| widths transcript (G-001) | `.dev-flow/2026-10-02-batch-03/evidence/inc001-widths.txt` | `d209dfb063e8b369b7f4243bb4eeaa96f70ef3c58672701714f6521290b9197b` |
| widths script | `.dev-flow/2026-10-02-batch-03/evidence/widths_compare.py` | `276eb0f740bfce7be33b7bea965d2e53f6cb47f833f7838f0ecb577ac262b15a` |
| P4 ux walkthrough relay | `.dev-flow/2026-10-02-batch-03/evidence/p4-ux-walkthrough.txt` | `82a5f8e31e84f3301c06ce69a593071f2d691779c2f520fb471373a0e09a1aca` |
| gate run | `.dev-flow/2026-10-02-batch-03/evidence/inc003-green.txt` | `43c16bdcabb0c6d6953b941ec276c12eb0e787df2295e1df208f0eabb04fe120` |

| Field | Value |
|---|---|
| **Evidence files** | 14 artifacts under the declared home, each cited with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "the panel never scrolls" — true while a whole card fits the room (room ≥ 3); below that the band is drawn alone and scrolls (declared, LLR-309.2's boundary) |
| If the result is an ABSENCE, what made the search wide enough | AT-307 walks every card of a column on three boards/modes at two sizes |
| Guard labelled as protecting a CONCLUSION, not a behaviour | AT-307's horizon and 14-high arms |
| Conjunctive criteria: one mutation per conjunct | C1 (no cut), C2 (cut ignores the selection), C3 (not on a card boundary), C4 (counts) |
| Synthetic instance of the absent case | the 14-high board; the oracle under `g g` |
| **Positive control for every probe that returned an ABSENCE** | the same walk on the increment-002 tree scrolls (`inc003-red.txt`) |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | the full suite on this tree (the gate run) | the gate run: every product node green (the one failure is the environmental clipboard node, G-011) — the census over increment 003's own surface found no other node asserting the scroll or the fold row's old form; the two G-004 nodes rewritten in place |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` | did not fire |
| B4 artifact produced here is consumed elsewhere | `line_map` → `app._scroll_selected_into_view` | AT-307 reads the viewport |
| A3 | interface consumed by another module changed | `_fold_row` (views-internal) gained an optional argument | no external caller |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 run (0 product nodes broken), B4 fired (AT-307), B2/B3/A3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| nodes asserting the superseded per-column geometry (G-004) | `test_app.py` nodes indexing kanban columns by computed widths or per-column headers | `grep -n "_phase_window(b, w - 2\|col0 = \|1 + sum(widths" tests/test_app.py` | 2 | 2 | `test_kanban_shows_every_task_in_its_phase` holds as written (unwindowed, 160 cells) — D-313 reworded |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1855 = 1845 − 0 + 10` ✓ (AT-307 +3 arms, TC-311 the cut ×2, TC-302 the title seat ×5; the two G-004 nodes in place, net 0).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` · round 1: `BLOCK-UNTIL: F1, F2` (HIGH F1: a single band that exactly fits was cut; HIGH F2: the fold row clipped counts — the cut band last, a long band name) with F3 (MEDIUM, a lone first row at the cut's bottom), F4 (MEDIUM, C3/C5 survived), F5 (MEDIUM, rail titles counted), F6–F9 (LOW) — reproduced on scratch copies (probes 4–7) · folded with RED proof (`inc003-red-r1.txt`: the new node FAILS on the round-1 code) · round 2: `OK to advance`, F1 and F2 discharged by re-reading and re-running its probes (a sweep of 2,295 cut frames, 0 violations), the approved 80×24 one-sided frame unchanged; notes F10 (MEDIUM, a one-sided `▲` row lost its names), F11 (MEDIUM, rooms 3–5), F12 (LOW, two no-effect lines) · folded (F10 coded with an 80×24 arm, F11 declared in LLR-309.2, F12 lines removed) · round 3 over the frozen tree: `OK to advance`, nothing open |

## 5 · Risks

- Below a room of 3 rows (a tiny panel, or a high band filling it) a tall band is still drawn alone and the panel scrolls — declared at LLR-309.2's boundary.
- The cut moves card by card as the selection walks a tall band; a step that crosses the cut shifts the band's rows (not its set).

## 6 · Pending items / spec deviations

- Operator questions from the P4 walkthrough, routed at close: UXV3-2 (`at risk`), UXV3-3 (`up` re-flow), UXV3-5 (`left`/`right`), UXV3-6 (horizon's `Done (0 open)`), UXV3-7 (head row, PV-10), UXV3-9 (entry cursor on a rail done task); minor UXV3-4 (help at 80×24, pre-existing), UXV3-8 (`done 0d ago`), UXV3-10, UXV3-11 → BACKLOG.

## 7 · Suggested next task

P4 iteration 2: the orchestrator's gate re-run; qa re-validation; the ux re-walk of UXV3-1.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | §2 |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | the cut's arithmetic (TC-311, C2/C3) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | no public signature changed |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | ids in docstrings |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
