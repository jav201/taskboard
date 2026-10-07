# Validation — taskboard — Batch 2026-10-07-batch-01 (the residue batch)

**PASS — all four lenses** over the 40-line delta (qa PASS-WITH-NOTES, architect PASS,
security PASS with SEC-R-1 "none", ux PASS-WITH-NOTES). The behavior-preserving equivalence
verified branch-by-branch by three lenses independently (`date_base` provably identical at
both seats — `_cascade_dates` returns None ⟺ `parse_iso` returns None; both `restore` sites
byte-identical to the replaced loops, skip-vanished preserved). The pins' mutants executed
LIVE by the ux-lens (C-5 gate removed → TC-701 RED; width hardcoded → TC-702 RED; both
reverted, diff byte-identical).

## Signed-balance test ledger

`post = base − deleted + added` → `2514 = 2512 − 0 + 2` ✓ reconciles.

## Carried notes (no folds owed)

QAR-1/UXR-1: TC-702's narrow-width pins assert the constructed string (the ladder's output),
not the painted widget — proportionate for a cleanup batch (AT-607 already reads the painted
toast at 80; a plain-text toast's string is the near-complete visual truth). Widen if the
clause matrix grows.

## Evidence

The close suite (below) · V4 Pro's 2514-passed full run (`evidence/chunkA-run.log`) · the
lenses' targeted 28-node runs · the lens-executed mutation pass (recorded in the P2 gate).
