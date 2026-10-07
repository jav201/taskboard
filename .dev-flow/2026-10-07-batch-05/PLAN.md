# PLAN — taskboard — Batch 2026-10-07-batch-05

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
| Batch | 2026-10-07-batch-05 |
| Objective | Carries batch: close the BACKLOG's standing items -- S5-3 a failed backup write leaves no partial file (_create_beside unlinks its exclusively created file on a failed write, a RED arm with a refusing remove); F-6 the Mon D formatter in three copies becomes one; UXV-3 `u` on a single-task change says what came back (one-line undo toast); UXV-6 the ? help at 80 cells clips with `...` never mid-word; the chain-map carries (deep chains fold with a per-band +N more cap, the resize-heal re-verifies the selection against the fresh line_map, AT-801b's docstring); the P4 F-3..F-5 test-strength arms; BACKLOG bookkeeping (present-a-project closes with batch E) |
| Standing authorization | Operator (Javier), 2026-10-07: "Ok, continuemos" — continue until the plan's proposed changes are done (the remaining work is the BACKLOG's standing carries). Read with the established chain: Gates — autonomous with the two exceptions; Git — the COORDINATOR commits and pushes at each close (no PR); data safeguard — synthetic boards only; implementing agents (DeepSeek instances under coordinator briefs, the standing 'Sigue usando Deepseek') do NOT commit/push/stash. This batch runs in the MAIN checkout; the increment briefs take disjoint file sets (001 owns models.py; 002 owns app.py/modals.py/views.py-help; 004 owns the milestones tests; 003 lands after 002) |
| First gate | the batch opened by rollover from 2026-10-07-batch-04 (`a820880`); the seed readback was clean (state.json `batch_id` rolled, the ledger seeded with LED-2026-10-07-batch-05.1); the P1 contract passed the validator at 0 block before the increments started |
| Premises / RC-1 | RC-1: local HEAD `a820880` == `origin/main` as of the batch's open (pushed at batch-04's close); premises P-1..P-3 in `01-requirements.md` §2.7, all TRUE with executed evidence |

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
