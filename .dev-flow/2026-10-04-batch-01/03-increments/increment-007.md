# Increment 007 — HLR-501 (LLR-501.2) · the operator's D-533: in lanes `◂` stays, the age goes first

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal). Mode
> `core`, language `en`. The second re-open (D-535, the D-422 path): asked at the gate, the operator
> ruled D-533 "Dejar ◂ solo, quitar la edad antes" and D-532 "Sí, en todas las plataformas" (recorded,
> no code). Revision 1 (frozen r1): code review OK to advance, no findings above NIT.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-01` |
| Increment | `007` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | LLR-501.2 (A-12); D-533, D-535 |
| Acceptance | AT-501 (lanes arm) · TC-504 |
| Agent | `software-dev` |
| Date | `2026-10-04` |

---

## 1 · What changed

**In lanes a waiting card keeps its `◂N`.** Under the lanes' 6-cell title floor the shed order is
now: the age `·Nd` first, then `▸`, then the other meta from the left, and `◂` (waits on N open)
last — so at 118 columns every waiting card shows `◂N` again (`Launch… ◂2 +6d`), and at 80 columns
`◂N` outlives the due (`Launch… ◂2`). Every other view, the grouped and matrix kanban, and every
other `card_cell` caller are byte-identical to increment 006 (`evidence/inc007-identity.txt`; the
code reviewer's own sweep of 10,124 renders/cells agrees).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-501.2 | `card_cell`: `age_token` kept; under `title_floor` the shed order age → `▸` → other meta → `◂` |
| `tests/test_links.py` | test | LLR-501.2 | TC-504 ×3 assert every painted waiting card keeps `◂N`; the unit test rewritten to the D-533 order; AT-501's lanes arm back to the exact `◂` count at 118×40; the 160×40 arm cites the ruling |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 0 (records: A-12, LED .23, D-532/D-533 rulings, D-535) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_links.py tests/test_cells.py tests/test_kanban_readable.py
python -m pytest -q -p no:cacheprovider          # the gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | the shed-order unit test | passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-504 ×5 | passed |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-501 (lanes arm) | passed |

Gate run on frozen r1: `python -m pytest -q -p no:cacheprovider` → **2306 passed in 432.92 s**, exit 0 (`.dev-flow/2026-10-04-batch-01/evidence/inc007-gate-r1.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | the changed tests on increment 006 frozen r2 (`views.py` `f21f3683…`): 5 FAILED — AT-501 (`Counter()` ≠ 7×`◂1` + 1×`◂2`), TC-504 ×3 (`▊ !! Launch n… +10d` — a waiting card with no `◂2`), the order unit test (`Add p… +12d`: the due kept, `◂` shed); the 160×40 arm passed on both (`evidence/inc007-red.txt`) |

| Field | Value |
|---|---|
| **Mutation verdicts** | **6 of 6 KILLED** (`evidence/inc007-mutations.txt`, spec `mutants_inc007.json`): U1 the age not shed first · U2 `◂` shed before other meta · U3 `▸` never shed · U4 `◂` treated as other meta · U5 no shed order (the shipped left-drop) · U6 floor 3 |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 1 instrument: the identity script's positive control — the same sweep over the lanes presentation hashes DIFFERENT before and after (`evidence/inc007-identity.txt`) |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts in their emitted form: the painted lanes (compositor strips at 118×30, 80×24, 118×40, 160×40), the rendered card cells (`Text.from_markup(...).plain`) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| `inc007-red.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc007-red.txt` | `3ba59273a8b93b04cd2ce0d1ba0005eba9f70b7e430496038893842effa10b5c` |
| `inc007-identity.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc007-identity.txt` | `bfe466dc0057dfd7a85d24738eb843ca00053fe42afb815ec3753fc8b6b4db9f` |
| `identity007.py` | `.dev-flow/2026-10-04-batch-01/evidence/identity007.py` | `5876a94147ff0d26cbbd826b722036c013b9735709e7ced11a59f30b31d3e057` |
| `mutants_inc007.json` | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc007.json` | `b90f09e3495d431302f1dadc431b1f4074b61f08ca72e335f2be684c5d71c7c2` |
| `inc007-mutations.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc007-mutations.txt` | `09380bacbeb2bcd6a81426450f6b57a13b4c2d06026ca4a3c0171599756a5c7f` |
| `inc007-frozen-r1.sha256` | `.dev-flow/2026-10-04-batch-01/evidence/inc007-frozen-r1.sha256` | `b519c65f6bfa63547db4e229935d0e2429b9e6b377dc1c65caae5ae42d08f9a1` |
| `inc007-gate-r1.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc007-gate-r1.txt` | `6ed4077945551279af27a2a5b41c8060a15f713d00593b29e3a6b144ec39e250` |
| `battery.py` | `.dev-flow/2026-10-04-batch-01/evidence/battery.py` | `a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb` |

| Field | Value |
|---|---|
| **Evidence files** | 8 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no view but the lanes changed", "no painted waiting card lacks its `◂N`" |
| If the result is an ABSENCE, what made the search wide enough | 4,404 renders/cells (mine) and 10,124 (the reviewer's) over every other view, presentation, selection and size; every painted lanes card at 118×30, 80×24, 118×40 |
| Synthetic instance of the absent case | the identity positive control (lanes differ); U1–U6 KILLED |
| **Positive control for every probe that returned an ABSENCE** | the lanes sweep; U2, U4 |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 2 probes: B1 `grep -rln "lanes\|card_cell" tests/` → `test_links.py` (AT-501's lanes arm and TC-504, rewritten to the ruling), `test_cells.py` and `test_kanban_readable.py` (green, unchanged — no floor there); B3 the `close3-kanban-lanes-*` captures |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | 1 correction: "under the floor the marks shed first" (D-529, increment 006) → "the age first, `◂` last" (D-533) — population `grep -rn "shed" tests/test_links.py .dev-flow/2026-10-04-batch-01/01-requirements.md`: the unit test, AT-501's comment, the 160×40 docstring, LLR-501.2 and D-533 — all edited |

### Signed-balance test ledger

`post = base − deleted + added` → `2306 = 2306 − 1 + 1` ✓ (the D-529 order unit test replaced by the D-533 one; no other node added or removed).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — round 1 (r1) OK to advance, no findings above NIT: the diff is `card_cell` only; non-lanes output byte-identical to increment 006 over 10,124 renders/cells (kanban grouped/matrix/lanes × group × archive × 29 selections × 6 sizes; the 7 other modes; floor-less cells), lanes the positive control; the D-533 order verified on 1,148 floored cells (an archived card included), 0 violations; no-age and done tasks correct; NIT — a user tag identical to the age or a link token in text and tone could collide (tags wear other tones) |

---

## 5 · Risks

- At 80 columns a waiting lanes card shows `◂N` and no due (`◂` outlives the due by the ruling).

## 6 · Pending items / spec deviations

- A-12.

## 7 · Suggested next task

Light P4 (qa, ux), re-close P5.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 1 rewritten, 5 strengthened |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | the order unit test |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | OK to advance |
| 7 | No file from another lane | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none frozen |
| 9 | Coverage on disk | all | ✓ | `pytest --collect-only tests/test_links.py` |
| 10 | Load-bearing emptiness | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 6/6 |
| 12 | **Instrument RED-proof** | all | ✓ | 1 |
| 13 | **Correction population** | all | ✓ | 1 |
| 14 | **Emitted-form assertion** | all | ✓ | 2 |
| 15 | **Independent review** | all | ✓ | `code-reviewer` |
| 16 | **Evidence files** | all | ✓ | 8 |
