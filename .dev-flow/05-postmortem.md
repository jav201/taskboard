# Post-mortem — 2026-08-03-batch-03

**Closed at Phase 2 without implementing.** Operator decision, after the orchestrator stopped the
batch and separated verified fact from agent claim.

**Nothing was implemented. `taskboard/` and `tests/` are byte-identical to `f237cb3` throughout.**

---

## 1. What the batch was for, and what it produced

The lanes project row was to state its demand in text (open · late · next Nd) and the cumulative
load curve was to move to a disclosure row appearing only on selection. The design was never in
doubt and is not why the batch closed.

What it produced: 5 HLR, 20 LLR, 15 AT, 26 TC, 26 premises, three cross-reviews, and roughly 180 KB
of executed measurement — none of which reached code.

## 2. Why it closed: one unresolved question wearing six disguises

Every substantive disagreement across two iterations reduced to **the row cost model** — `room`,
`prof`, and a ±2 for the lead band. Five of six refutations are that arithmetic seen from different
angles.

| # | claim | claimed by | verdict |
|---|---|---|---|
| 1 | The cost model undercharges `prof`; a defect would ship | architect iter-2 | **FALSE** — `views.py:2127` already passes `h - 2 - (2 if active else 0)` |
| 2 | Amendment A-6 corrects it | architect iter-2 | **INVERTED** — A-6 pads 28 blank rows over 18 renders where the original padded 0 |
| 3 | No fixture permits the mutation (`open == total`) | qa iter-1 | **FALSE** — 15 of 16 on-disk lanes have `open != total` |
| 4 | `test_prism_laws.py:147` goes vacuous | architect iter-1 | refuted; its replacement figure `35 → 20` also failed to reproduce (`35 → 17` or `35 → 30`) |
| 5 | The bench occupies 87 % of the panel | architect iter-2 | **90 % at h=60**, 95 % at h=120 — the band is `(prof+2)/h`. **The operator ruled O-3 on the understated number.** |
| 6 | `titles == 1` is the calm case | qa iter-1 | fixture-only; the operator's real board gives 8/6/17 |

**The root cause is not agent error. No single verified cost model was ever fixed, so each agent
measured against its own** — and the disagreements were only visible when a later agent re-derived
an earlier one's number. Every refutation above came from re-derivation, never from review-by-reading.

## 3. The orchestrator's own defects

1. **Half-verified a load-bearing finding and reported it as confirmed.** I measured that
   `lead_band` draws `prof + 2` (constant across 5 values) and stopped. I never opened the call
   site, where the subtraction already lives. This is **C-15.1** of the flow itself — *a data-flow
   claim is verified at the state's writers, not at the caller* — applied to me.
2. **Dispatched two Phase-1 agents in parallel with no shared identifier registry**, so both minted
   `AT-001..004` with different subjects and the behavioural traceability chain pointed at ids
   meaning different things. Fixed structurally in iteration 2: the orchestrator fixes the register
   before dispatch, and the iteration ran as a single agent.
3. **Asserted `views.py:986` was `load_curve`'s only caller** in `PLAN.md`. `report.py:137` is a
   second one; my grep swept only `views.py`. Caught by the architect.

## 4. What the batch got right, and should be reused

- **The premise table (C-43) paid for itself twice**, both times against me: it disproved my own
  occupancy risk (72.3/80.9/83.8 % vs a 45 % floor) and my own reflow risk (−0.17 ms, because
  `refresh_view` already repaints the whole view).
- **C-39/C-40 caught an acceptance predicate that would have rejected a correct implementation** —
  `distinct braille glyphs` is monotone the wrong way, and its `>= 4` threshold false-fails correct
  code on 3 of 13 occupancy lanes in regime.
- **P6 explains the operator's original question.** The legend has never described the wave. The
  ghost-mark law could not catch it because it verifies that every legend entry is drawn, **not that
  every drawn mark is explained.** That asymmetry is a candidate control (see the backlog).
- The interruption protocol worked: a sub-agent died at the probe→write boundary and was resumed
  from its transcript rather than restarted, with an explicit instruction to mark unrecoverable
  probes `NOT RECOVERED` rather than reconstruct them.

## 5. Decisions taken without asking (kickoff contract)

| decision | rationale |
|---|---|
| `security-reviewer` not dispatched at Phase 2 | `security_required: false`; the batch renders counts and a curve from already-loaded data — no auth, secrets, integration or new input surface |
| **O-4 proceeded on its measured default** | The operator ruled O-3 and did not address O-4 (how the legend learns the disclosure row was drawn). Flagged in-conversation; never reached code |
| Phase-1 iteration run as one agent, not two | Structural fix for the id collision |

## 6. Working-file reconciliation (C-44)

| file | state |
|---|---|
| `.dev-flow/01-requirements.md`, `01b-qa-validation-plan.md`, `02-review-architect.md`, `02-review-qa.md`, `02-review-qa-iter2.md`, `2026-08-03-batch-03/PLAN.md`, `05-postmortem.md`, `state.json` | ✅ **committed as the record** — the measurement is the batch's only durable output |
| `.fast-dev-flow/spec.md` (deleted), `archive/2026-08-03-fastflow-01-spec.md`, `archive/2026-08-03-fastflow-02-PROMOTED-spec.md` | ✅ **committed** — the promotion trail |
| `_prototypes/` | ✅ **committed** — the Ledger/Darkside/Naught/hybrid renders and the A/C/D comparison that produced the operator's mechanism decision |
| `taskboard/**`, `tests/**` | 🗑️ **untouched** — no code was written |

**Nothing is in limbo.** No commit from this batch exists that has not landed.

## 7. Carried forward

See `.dev-flow/BACKLOG.md` → *From 2026-08-03-batch-03 (closed at Phase 2)*.
