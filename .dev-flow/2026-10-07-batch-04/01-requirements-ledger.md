# Requirements ledger — taskboard — Batch 2026-10-07-batch-04

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-07-batch-04.1 — batch E derived from the prototype's verdict (P1)
- **Requirement:** HLR-1001, LLR-1001.1, LLR-1001.2
- **Date:** 2026-10-07
- **What changed:** new requirements: the presentation mode (the operator's verdict 2026-10-07 on the prototype round: PRES-C one interactive surface; SVG + PNG export; `R` REPLACES the report). The PRES-C prototype frames (committed copies at `evidence/frames/PRES-C-118x30.txt`, `PRES-C-80x24.txt` — the live prototype dir stays on disk, uncommitted, house rule) are the oracle; the prototype's build.py is the port source (re-derive, not paste).
- **Why:** the plan's ruling (batch E is design-first: a prototype round with a verdict before implementation) is satisfied — the verdict arrived with the prototype's recommendation (PRES-C) accepted.
- **Evidence:** `evidence/veredicto-present.json` (committed copy of the prototype round's verdict; the live prototype dir stays on disk uncommitted, house rule) · the PRES frames (`evidence/frames/PRES-C-*.txt`, copies of `prototypes/present_e/out/`) · the round's record (`evidence/BRIEF.md`, `evidence/run2.log`).
