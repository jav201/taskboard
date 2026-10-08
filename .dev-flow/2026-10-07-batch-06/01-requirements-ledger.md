# Requirements ledger — taskboard — Batch 2026-10-07-batch-06

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-07-batch-06.1 — the chain map admits every open task; the kanban window shows its sides (P1)
- **Requirement:** HLR-1201, HLR-1202, LLR-1201.1, LLR-1201.2, LLR-1202.1
- **Date:** 2026-10-07
- **What changed:** (a) HLR-1201 AMENDS the C-2b oracle (the batch-02 frames this operator's verdict accepted): the chain map now draws every open task — unlinked open tasks as one-row `○` tiles at depth 0 in their band — so chains are created on the map with the shipped `L` picker; the inert `no links` row survives only for a project with no open work; the `x` unlink leaves the task as a visible `○` tile. The amended frames are the new renderer's bytes on the SAME frozen fixture at 118×30 and 80×24, stored at `.dev-flow/2026-10-07-batch-06/evidence/frames/`; the sealed batch-02 frames stay history; `tests/test_chainmap.py`'s frame path moves to the amended home citing this LED. (b) HLR-1202: the kanban's phase-head row marks the hidden window sides (`◂` left, `▸ N` right, exact N) plus the `?` bullet.
- **Why:** the operator's reports from real use 2026-10-07: the chain map shows projects with no tasks and no way to create a chain; the kanban hides later phase columns with no on-screen sign.
- **Evidence:** the coordinator's reproduction on a copy of the operator's board (84 tasks, 0 links — `L` worked only off-view) · `C-2b-118x30.txt:22` (the inert row being amended) · the amended frames (this batch's evidence home, hashes in increment-001).
