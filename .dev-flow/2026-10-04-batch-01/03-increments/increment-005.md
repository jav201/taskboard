# Increment 005 — HLR-502 (LLR-502.3) · P4 fold: the link mode says a folded waiter row

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal). Mode
> `core`, language `en`. A P4 fold: ux-reviewer raised code review 004's F4 to MED (the overlay
> vanished in silence when the gantt folded the waiter's group); qa-reviewer's G-002 (the tones of
> the overlay unasserted). Revision 3 (frozen r3): round 1 OK to advance with N1, N2 (LOW) folded
> in r2; r3 removes a dead clause the r2 battery exposed.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-01` |
| Increment | `005` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-502, LLR-502.3; amendment A-8; D-528 |
| Acceptance | TC-512 (the folded-row arm), TC-511 (the tones) |
| Agent | `software-dev` |
| Date | `2026-10-04` |

---

## 1 · What changed

**When the gantt cannot unfold the waiting task's group beside the candidate's, the link mode now
says so instead of losing the link in silence.** The hint row ends with "‹waiter› is folded — a
taller terminal draws the link" (the title clips, the reason stays; "waiter row folded" where the row
is short); a closed waiter, never drawn, gets no note. The gantt's shared fold rule (`gantt_plan`,
which also feeds `nav_model`) is unchanged — keeping the waiter's group open is the operator's call at
PV-5 (D-528). TC-511 now also asserts the overlay's tones: `═` in the over tone, the connector in the
bright tone (qa G-002).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | LLR-502.3 | `GanttLinkMode._paint` computes `folded` from the frame's line map; `_status` appends the note |
| `tests/test_gantt_link.py` | test | LLR-502.3 | NEW `test_TC_512_a_folded_waiter_row_is_said` (118×20 note, 118×30 none, long title at 118 and 80, closed waiter); TC-511 tone assertions |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 0 (records: A-8, D-528..D-530, LED .19) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_gantt_link.py
python -m pytest -q -p no:cacheprovider          # the gate
```

Manual: a terminal 20 rows tall, `3`, select `Launch new homepage`, `L`, type `push`.

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-511 (tones via rendered segments) | passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-512 folded arm, TC-511 | 2 passed (14 in the file) |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-503 unchanged | passed |

Gate run on frozen r3: `python -m pytest -q -p no:cacheprovider` → **2295 passed, 1 failed in 444.93 s** (`.dev-flow/2026-10-04-batch-01/evidence/inc005-gate-r3.txt`); the one failure is `test_win_clipboard_roundtrip`, whose SETUP message names the environment — the known flake (G-011).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | the folded-row arm on increment 004's frozen r3 product (`modals.py` `7fa70f59…`): FAILED — the note absent at 118×20 (`evidence/inc005-f4-red.txt`); the tone assertions are pinned by mutants R4, R5 |

| Field | Value |
|---|---|
| **Mutation verdicts** | **7 of 7 KILLED** on r3 (`evidence/inc005-mutations-r3.txt`, spec `mutants_inc005_r3.json`): R1 note never said · R2 said with the row drawn · R4 `═` tone · R5 connector tone · R6 no short form at 80 · R7 a closed waiter noted · R8 the reason clipped instead of the title. r1 5/5 (`inc005-mutations.txt`); r2 6/8 (`inc005-mutations-r2.txt`): R3 SURVIVED — the `>= rows` clause was dead (the renderer pages; rows past the frame are never mapped, probed at heights 5–9) and was removed in r3; R8 SURVIVED — the long-title arm at 118 added in r3 |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 1 instrument: the r2 battery reported R3 and R8 SURVIVED — it can say no |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts asserted in their emitted form: the painted screen (compositor strips, 118×20, 118×30, 80×18), the rendered segments' colours (TC-511) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| `inc005-f4-red.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc005-f4-red.txt` | `06dcc8c8524ac520be762800aa3b7d1a5ec6f98c42b6bac2e8533cd2833e1493` |
| `mutants_inc005.json` | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc005.json` | `f4bdf2126bc705678a534d1ee930f134cf924a0ac1dd761b602db3e8c1facf10` |
| `inc005-mutations.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc005-mutations.txt` | `c1a3fffbb7df178a37d11f5f9cad18eb12bbb6f6059d103f0962c5ba4669002b` |
| `mutants_inc005_r2.json` | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc005_r2.json` | `77b7d44e0f0bc2a9d3b25770ef48fe6fafcc278d225efd2cd18d0ef2d71adc4d` |
| `inc005-mutations-r2.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc005-mutations-r2.txt` | `a5cccf307fe7232e819fa31d0329fe5c8d088889c30bce7ea48727c86516dcbe` |
| `mutants_inc005_r3.json` | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc005_r3.json` | `b1cd2a8bbe356c40b339f3902d08805efc74a1c3a35075e72e0c68ec77545409` |
| `inc005-mutations-r3.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc005-mutations-r3.txt` | `1ab5b1c70004871416498478d58a5221f8e50305c674b78ca6d7806297461959` |
| `inc005-frozen-r1.sha256` | `.dev-flow/2026-10-04-batch-01/evidence/inc005-frozen-r1.sha256` | `2fe8bd026b5d82b5e431835861a1786f8a604c34db22deb21401fee742447619` |
| `inc005-frozen-r2.sha256` | `.dev-flow/2026-10-04-batch-01/evidence/inc005-frozen-r2.sha256` | `7559a791c188879b1db11b86d26e103f069d576403d56750ee91677f0170e1df` |
| `inc005-frozen-r3.sha256` | `.dev-flow/2026-10-04-batch-01/evidence/inc005-frozen-r3.sha256` | `1b31c26347c70b00124e243d01d4d936269aa00ed1a7e292471872698bb5666d` |
| `inc005-gate-r3.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc005-gate-r3.txt` | `71ef6936a9e6e63c71255ea1435907548ab4bab61b18a10fe91a521065dd1845` |
| `battery.py` | `.dev-flow/2026-10-04-batch-01/evidence/battery.py` | `a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb` |

| Field | Value |
|---|---|
| **Evidence files** | 12 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "a row past the frame is never in the line map" |
| If the result is an ABSENCE, what made the search wide enough | heights 5–9 with the candidate in the waiter's own group (`tw2`, `tw3`, `tw4`): `line_map` never held `tw5` |
| Synthetic instance of the absent case | R2 (the note with the row drawn) KILLED; the dead clause's mutant R3 SURVIVED on r2, the reason it was removed |
| **Positive control for every probe that returned an ABSENCE** | R2 |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 2 probes: B1 `grep -rln "GanttLinkMode\|_status" tests/` → `test_gantt_link.py` only (green); B4 none (no file written) |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | 0 corrections — a new note, no wording replaced |

### Signed-balance test ledger

`post = base − deleted + added` → `2296 = 2295 − 0 + 1` ✓ (1 in `test_gantt_link.py`; 2296 = 2295 passed + the clipboard flake).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — round 1 (r1) OK to advance: the `folded` rule, S1, the keys row at 80 checked; N1 LOW (at 80 the clip ate the reason, not the title) and N2 LOW (a closed waiter would be noted) → folded in r2 with arms; r3 removes the dead clause · r3 OK to advance: N1, N2 discharged on the diff; NIT — the comment "rows past the frame are not mapped" overstates: at a frame of 3 rows (terminal ≤ 6) the CANDIDATE can be mapped past the frame, never the waiter (0 of 243 such frames), so `folded` is unaffected; comment left as frozen, recorded here · no HIGH open |

---

## 5 · Risks

- The waiter's group still folds where the frame is short or the projects are large; the note says it (D-528 — the fold rule is the operator's call at PV-5).

## 6 · Pending items / spec deviations

- A-8 (the note).

## 7 · Suggested next task

P4 close-out: close captures (lanes re-shot), then P5.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 1 new node + TC-511 assertions |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | TC-511 |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | OK to advance |
| 7 | No file from another lane | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none frozen |
| 9 | Coverage on disk | all | ✓ | `pytest --collect-only tests/test_gantt_link.py` → 14 |
| 10 | Load-bearing emptiness | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 7/7 |
| 12 | **Instrument RED-proof** | all | ✓ | 1 |
| 13 | **Correction population** | all | ✓ | 0 |
| 14 | **Emitted-form assertion** | all | ✓ | 2 |
| 15 | **Independent review** | all | ✓ | `code-reviewer` |
| 16 | **Evidence files** | all | ✓ | 12 |
