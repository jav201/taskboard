# PLAN — taskboard — Batch 2026-10-25-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 at both levels; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/guides/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.
> **Two header labels are read literally and are never translated:** `Standing authorization` and `Last updated`; the field guide names their readers.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-25-batch-01 |
| Objective | D-12: the start-up modals (MilestoneOffer, TeamIdentityPicker) open only after the board has painted at its real size, so the user sees the board dimmed by the shared #0007 backdrop behind them; the order is unchanged (identity picker first, offer last) and nothing else changes (SB-1..SB-3) |
| Last updated | P2 · 2026-10-25 |
| Standing authorization | «Sigue, tú planeas, la implementación dásela a kimi 2.8» — the operator's commission for this batch (.dev-flow/COMMISSION-startup-backdrop.md, the operator's words recorded there). This runtime cannot prompt; the commission is the answer: autonomy over the gates it commissions, recorded per-gate in `state.json.decisions_log`; merge NOT granted (do not push or merge); a HIGH finding blocks regardless. |
| First gate | exit 0 — `0 block · 153 notice · 63 not applicable` over the closed 2026-10-24-batch-02 record; `V7` reported no bundle-hash disagreement (the run proves the tool and bundle, not the batch). |
| Premises / RC-1 | `origin/main` tip verified at intake: `3053c1e` (2026-10-25); merge-base of `fix/startup-backdrop` == tip, no rebase needed. RC-1 (b): `git grep D-12 origin/main -- REQUIREMENTS.md` → no hit, D-12 not shipped externally. RC-2: `git ls-remote --exit-code --heads origin` exit 0, remote answered. Flow revision: bundle mirror at `C:/Users/jjgh8/.claude/skills/dev-flow` (F1 not-run from a bundle — `V7`'s bundle-identity line is its probe). |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — docs/ARCHITECTURE.md §2 layer list read; no module created, no boundary moved |
| A2 | fired | judged — docs/ARCHITECTURE.md §2: "touches ≥2 modules" counts layers. The commission expects `taskboard/app.py` only, but SB-1's fix location is cause-dependent (the hypothesis points at the BoardView paint lifecycle, `views`), so the touch set is not decidable at intake; the operator's commission directs architect-level design review (PDR) and a DDR. Fired; the question is carried to the PDR. |
| A3 | not fired | judged — no interface in docs/ARCHITECTURE.md §4 changes shape; the deferral is app-internal timing |
| A4 | not fired | judged — one increment commissioned |
| B1 | fired | `grep -rl _offer_milestones tests/` and `grep -rl _init_team_mode tests/` → hits in tests not owned by this story (e.g. tests/test_milestone_offer.py, tests/test_app.py) · reverse census owed at P2/P3 |
| B2 | not fired | probe — no file moves location on disk |
| B3 | not fired | probe — `grep -r "app.py" tests/goldens/` no byte-identical golden cites the touched source |
| B4 | not fired | probe — the change produces no artifact another component consumes |
| C1–C8 | not fired | the C scan runs mechanically at P1 (`devflow-scan-spec.py`); no auth/secrets/external-integration/sensitive-data/destructive-DB/input-surface/network/markup-rendering pattern in the commissioned scope |
| D1 | fired | judged — the change alters what the user sees at start (the backdrop behind the start-up modals) |
| D2 | not fired | judged — no prototype; the commission declares none needed |
| E1 | not fired | judged — one story, one increment |
| E2 | not fired | judged — defect fix of a rendered-backdrop gap; no high risk declared at intake |
| E3 | not fired | judged — internal defect batch, no client deliverable |
| F1 | not fired | from a bundle, which cannot recompute `flow_hash`; `V7`'s bundle-identity line is the probe output |
| F2 | not fired | probe — `.dev-flow/BACKLOG.md` reconciled by 2026-10-24-batch-02's close (2026-10-25); the queue is fresh |

## Where we are

P1 done, gate green (0 block). The requirements contract is written and the SB-1
diagnosis is complete: the commission's unpainted-board hypothesis is REFUTED by
measurement (`evidence/red-p1.txt` — the board beneath holds 23-29 painted rows
with the modal up); the cause is `taskboard/taskboard.tcss:309-312` (the shared
`#0007` backdrop rule does not name `MilestoneOffer`/`TeamIdentityPicker`, so the
`Screen { background: #0d1117 }` rule paints them opaque). One US, 4 HLR, 6 LLR,
AT-2801..AT-2804, IFC Part A; the family-C scan is clean (`flags: none`,
`security_required: false`). P2 review is next.

## Objective

<the batch objective, restated>

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-001 (D-12) | READY → derived | 4 HLR, 6 LLR, AT-2801..AT-2804; cause measured at P1, hypothesis refuted |
| P0 / ARQ | closed | 96684bd; module map fresh, no amendment |
| P1 | in review | contract + ledger seeded; scan clean; red-p1.txt at base_ref |

## Roadmap + increment plan

<the increments this batch expects, in order>

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-25 | <decision> | <reason> |

## Risks / watch-items

- <risk · likelihood · mitigation>

## Conventions honored

- <convention>

## Out-of-scope carries

- <what this batch deliberately does not do, and where it is tracked>

## Gate notices and runtime absences

<per gate: each NOTICE it printed and why it stands (`stations/core-runbook.md` §*Expected NOTICEs*); once: each mechanism `SKILL.md`'s gate step 5 found unavailable on this runtime, and each rule recorded `not-run`, with the reason>

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| <command> | <date> | <result> |
