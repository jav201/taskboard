# PLAN — taskboard — Batch 2026-10-07-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 in both modes; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/docs/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-07-batch-01 |
| Objective | Cleanup batch: the P4 residue of 2026-10-06-batch-01 -- DS-5 the app reuses the tested models.restore; bump_due's today-base unified with plan_move's (one rule, ARCH4-4/SEC4-6); Plan.conflicts documented as the totals intermediate (ARCH4-3); the C-5 vanished-task arm pinned (SEC4-3); the toast rungs below 80 pinned as degrade-by-design (GAP-3) |
| Standing authorization | Operator (Javier), 2026-10-07: "Haz el residuo de P4 y si puedes empezar el siguiente incremento paralelizando sería bueno. Sigue llamando a Deepseek." Read with the established chain: autonomous gates with the two exceptions; the coordinator commits and pushes after verification (residue the operator ordered done; no PR); synthetic boards only; the implementing agents do NOT commit/push/stash. Two DeepSeek instances (V4 Pro: product; Flash: tests) implement disjoint halves in parallel per the operator's request |
| First gate | exit 0 · V7 did not fire — 0 block 55 notice (all inherited from closed batches); the rollover readback clean |
| Premises / RC-1 | <the verified `origin/main` tip, or: no origin — RC-1 not possible, local tip <sha>; each premise the batch rests on> |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| <A1 / B1 / …> | <fired / not fired> | <the probe run and what it printed> |

## Where we are

<one paragraph: station, what the last gate decided, what is owed next>

## Objective

<the batch objective, restated>

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| <US-NNN / station> | <status> | <notes> |

## Roadmap + increment plan

<the increments this batch expects, in order>

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-07 | <decision> | <reason> |

## Risks / watch-items

- <risk · likelihood · mitigation>

## Conventions honored

- <convention>

## Out-of-scope carries

- <what this batch deliberately does not do, and where it is tracked>

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| <command> | <date> | <result> |
