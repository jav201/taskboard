# PLAN — taskboard — Batch 2026-10-07-batch-04

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
| Batch | 2026-10-07-batch-04 |
| Objective | Batch E of the kg_mejoras plan: the presentation mode behind R (replacing the report) -- the PRES-C interactive hybrid per the operator's verdict 2026-10-07 (gantt on top, brief blocks below, a ⟦━⟧ cursor expanding the notes), exporting SVG and PNG |
| Standing authorization | Operator (Javier), 2026-10-07: "Arranca y continua hasta terminar los cambios propuestos para el proyecto" + "HAz ambas, paraleliza" (the cleanup batch and this presentation batch in parallel, this one in the `present-e` worktree) + "Sigue usando Deepseek". Read with the established chain: autonomous gates with the two exceptions; the coordinator commits and pushes at each batch's close; synthetic boards only; implementing agents do NOT commit/push/stash |
| First gate | the batch opened by rollover from 2026-10-07-batch-02 (`34bab3c`); the scaffold readback was clean (state.json `batch_id` rolled, the ledger seeded with LED-2026-10-07-batch-04.1); the tree then forked into `.claude/worktrees/present-e` so the parallel cleanup batch could land on main |
| Premises / RC-1 | RC-1: no origin — local tip `34bab3c` (= `origin/main` as of batch C's push, unverified here); premises P-1..P-3 in `01-requirements.md` §2.7, all TRUE with executed evidence |

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
