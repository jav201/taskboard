# Review — taskboard — Batch 2026-10-07-batch-04

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3
- **Out-of-scope findings:** `none`

- **Findings:** `0` blocker · `0` major · `2` minor (both found at the increment, folded — N1 the byte contract had no shipped test, N2 the `_strip` regex measure broke the S1 width law; see `03-increments/increment-001.md` §4b)
- **shall/should check:** ✓ clean — HLR-1001/LLR-1001.1/.2 use `shall` throughout; no modal `should`
- **Two-layer (blockers):** ✓ every story has an `AT` (US-1001 → AT-1001) · output reqs name deliverable+observation (the painted frame at both operator sizes; the SVG+PNG at the reports/ convention) · both trace chains complete (US-1001 → HLR-1001 → LLR-1001.1/.2 → TC-1001..TC-1004) · ATs are genuinely black-box (AT-1001 drives keys, reads the painted surface and the folder, names no internal symbol)
- **Census (change-first):** done — best-effort + gate-confirmed (the increment's reverse census carries the five probes)
- **Security:** ⚠ `1` finding — the S1 hostile-text width defect at `_strip`, folded in-increment (the rich-parse measure + TC-1003 + mutation M6 as its standing RED); no finding survives the close
- **Evidence checklists (architect / qa / security):** `core` mode — the full-mode reviewer pool is not owed; the coordinator's lens covered the contract, the increment gate carries the evidence tables

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| `<one row per finding>` | | | | | | |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a finding nobody raised. Write your own rows in the table above.

```text
| *(example)* F1 | architect | blocker / major / minor | | | | open / fixed |
```

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

`<result>`

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-001 | yes/no | yes/no/n/a | yes/no | yes/no | ✓ / blocker |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

`<files × families run · reservations · what the I-gate must confirm>`

### Security review summary
`<security-reviewer findings + verdict, or "not run — trigger family C did not fire" in core>`

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.
