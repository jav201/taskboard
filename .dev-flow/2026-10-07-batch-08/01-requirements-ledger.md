# Requirements ledger — taskboard — Batch 2026-10-07-batch-08

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-07-batch-08.1 — template authoring v2: save a chain as a template (P1)
- **Requirement:** HLR-1401, LLR-1401.1
- **Date:** 2026-10-07
- **What changed:** new requirements closing the batch-07 carry: a chain-map key saves the selected task's connected component (open tasks, both directions through depends_on, within the project) as a user template under a typed name; fan-in collapses to the first predecessor (the template shape cannot hold a diamond — declared); saving writes settings only, not an undo step (declared); the degenerate single-task component is allowed.
- **Why:** the operator's 'continua junto con deepseek lo que sigue' 2026-10-07 — the queued carry.
- **Evidence:** the batch-07 store/picker/insert seats (bafa1e3) · the fan-in/shape analysis in LLR-1401.1.
