# Batch close — taskboard — Batch 2026-10-26-batch-01 (audit of shipped f4b53cc)

> **Artifact language.** English. **Mode:** `core`. Audit batch — nothing in `taskboard/` was
> changed; the close records the audit and queues its findings.

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` from the project root · P1 exit 0 (0 block / 177 notice / 57 n/a) · P2 exit 0 (0 block / 187 notice / 49 n/a) · P4 exit 0 (0 block / 187 notice / 49 n/a) · 2026-10-26 |
| Gated tree | `f4b53cc7d89bd645a99e0615dbafb7c102de2abd` (the audited change = HEAD = origin/main) + the audit's own record commits; final gate transcript: `evidence/gate-final.txt` |
| Requirements canon | `REQUIREMENTS.md` — 20 ids folded by the close as the dated **Audit annex — 2026-10-26-batch-01** (US-3001, HLR-3001..3005, LLR-3001.1-.3, LLR-3002.1-.3, LLR-3004.1/.2, LLR-3005.1/.2); the pre-existing stale rows (HLR-102/104, LLR-101.3/602.1) are deliberately NOT amended — that is finding AUD-01, the orchestrator's decision |

## 1 · What changed

Nothing in the product. The audit retroactively contracted, reviewed, validated and recorded the
shipped change `f4b53cc` «done work keeps its row — only archiving hides it»: done, non-archived
tasks keep quiet rows (reached tone, `✓` chip, never late) at each group's tail on the board's
gantt; only archiving hides work; folding/pressure/window unchanged (G3); the presentation is
byte-identical (G4). The audit's own tree changes: the batch record under
`.dev-flow/2026-10-26-batch-01/`, the `git mv` of `.scratch-evidence/` into the batch's
`evidence/`, the BACKLOG findings section, and the REQUIREMENTS.md audit annex.

| Requirement | Verified by | Verdict |
|---|---|---|
| HLR-3001 (rows, G1) | AT-3001/3002/3005 + 3280-suite + captures | pass |
| HLR-3002 (quiet look, G2) | AT-3001/3006 + capture 1 (118x30) | pass |
| HLR-3003 (unchanged, G3) | fold arms + captures 3-4 (flag on/off) | pass |
| HLR-3004 (presentation, G4) | AT-3004 + golden verdict CLEAN | pass |
| HLR-3005 (else/cursor, G5) | AT-3003/AT-3006 + 13-file diff census | pass |

## 2 · The review at a glance

Four independent lenses, each a spawned generic sub-agent with its `agents/` role file:
architect (iterate-to-refine: seam APPROVE, records layer AX-1..AX-5), code-reviewer
(OK-TO-ADVANCE, 0 HIGH), qa-reviewer (PASS; **golden-file verdict CLEAN** — exactly 4 of 40
frames moved, `.plain` only; HEAD regen reproduces the committed golden byte-exactly), ux-reviewer
(PASS; 4 real Windows Terminal captures, window-cleanup assertion PASS, ≥8 colours per shot).
Consolidated: the shipped code is faithful to G1–G5; the defects are in the records layer.

## 3 · Findings carried out (all open, nothing applied — orchestrator decides)

- **AUD-01 (HIGH)** — canon still encodes the retired G-A law (HLR-102/104, LLR-101.3/602.1); amendment proposed.
- **AUD-02 (HIGH)** — finish toast still says «folded into ✓N» (`taskboard/app.py:2313`); reword proposed.
- **AUD-03 (MEDIUM)** — legend gloss + swatch tone mismatch (`taskboard/views.py:8702`).
- **AUD-04 (MEDIUM)** — declared colour-budget rebaseline (25.5→29.5; ink-direction arm dropped).
- **AUD-05..AUD-08 (LOW)** — nav/frame body-height parity edge; doc/test-picture drift (G-A citations, TC-118 at 118x40, AT-207 pins, emptiness bound); G3 busy-board fold trade-off awaiting the operator's eyes; first-run toast in captures.
Full text: `02-review.md` and `.dev-flow/BACKLOG.md` §Open — raised by the 2026-10-26 audit.

## 4 · Evidence index (all under `.dev-flow/2026-10-26-batch-01/evidence/`)

`gate-p1/p2/p4/final.txt` · `import-probe.txt` · `suite-targeted.txt` (123 passed) ·
`suite-targeted2.txt` (62 passed) · `scratch-evidence/suite-chunk0{0,1,2}.txt` (3280 passed,
consumed) · `qa-regen-baseref.json`, `qa-regen-head.json`, `qa-tmp-base.json`, `qa-tmp-head.json`
(golden regen) · `captures/png/{gantt_118x30,gantt_80x24,busy_80x24,busyoff_80x24}.png` +
`captures/README.md` + `captures/capture-log.txt`.

## 5 · Honest record — what this batch did NOT do

- No `taskboard/` source change (commissioned); HIGH fixes are proposed, not applied.
- No push, no merge (not granted).
- Full suite NOT re-run by the audit (operator's rule: the change's 3 chunks are its evidence);
targeted re-runs only, 185 passed.
- `dev-flow-sync` (vault export): not-run — no `vault_root` deployment row in this bundle.

## 6 · Postmortem (light)

- **What the fast path cost:** the records layer (canon, toast, legend) now contradicts the
  shipped behaviour — exactly the defects P1–P2 of a normal batch would have caught before ship.
  The audit caught them a few hours later; nothing user-visible is broken, but AUD-02 is a
  user-facing string telling the old story.
- **What went right:** the change's own evidence was hash-verifiable and TRUE — the golden
  regeneration claim in the commit message survived independent regen (CLEAN); the `done_rows`
  default-off seam kept G4 structurally.
- **Candidate control** for `dev-flow-lessons`: *a shipped commit that regenerates a sealed
  batch's oracle must name the regeneration script and the expected frame delta in the message* —
  it did, and the audit could verify it in minutes.
