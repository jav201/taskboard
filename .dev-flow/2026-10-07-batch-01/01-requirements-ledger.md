# Requirements ledger — taskboard — Batch 2026-10-07-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-07-batch-01.1 — the P4 residue derived (P1)
- **Requirement:** HLR-701, LLR-701.1, LLR-701.2, LLR-701.3
- **Date:** 2026-10-07
- **What changed:** new requirements: US-701 (the residue), HLR-701, LLR-701.1 (one restore rule via `models.restore` at every site; one date-base rule shared by `bump_due` and `plan_move`; `Plan.conflicts` documented as the tested totals intermediate), LLR-701.2 (the C-5 vanished-task refusal pinned by a synthetic test — TC-701), LLR-701.3 (the toast fits ≤ width at 80/60/40/24 and stays non-empty at 24 — TC-702). The refactor's oracle is the whole suite (behavior-preserving by definition).
- **Why:** P4 of batch 2026-10-06-batch-01 found no defect — it found five drift risks (DS-5, ARCH4-3, ARCH4-4, SEC4-3, GAP-3), all LOW, all behavior-verified. The operator commissioned the closure 2026-10-07.
- **Evidence:** `.dev-flow/2026-10-06-batch-01/04-validation.md` §Carried · the P4 lenses' findings.
