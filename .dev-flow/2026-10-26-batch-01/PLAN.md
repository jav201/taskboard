# PLAN — taskboard — Batch 2026-10-26-batch-01 (AUDIT of a shipped change)

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓

The living compendium of this batch: where-we-are · objective · station status · triggers ·
decisions · risks · gate notices. **This is a retroactive audit**: the implementation it
records preceded the flow, at the operator's explicit order (see Standing authorization).

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-26-batch-01 |
| Objective | Retroactive dev-flow audit of the shipped change `f4b53cc` «fix(gantt): done work keeps its row — only archiving hides it» on `fix/gantt-done-visible` (= `main`): done, non-archived tasks keep their quiet rows on the board's gantt; only archiving hides work; presentation byte-identical (G4); 4 independent reviewer lenses (architect · code-reviewer · qa-reviewer · ux-reviewer); requirements written retroactively from the operator's request and decisions G1–G5; **no `taskboard/` source change in this batch** |
| Last updated | P5 · 2026-10-26 |
| Standing authorization | The operator, 2026-10-26, verbatim: «Haz el cambio rápido, esta vez sólo implementa. Haz push y merge verificando que funciona y después auditas el cambio con dev flow.» — autonomy over every gate the audit names (P0..P5, the four commissioned review lenses, targeted re-runs only); push/merge NOT granted in this batch («No destructive git, no push or merge»); a HIGH finding is recorded with a proposed fix but NOT applied — the orchestrator decides. |
| First gate | pre-batch run (over the closed 2026-10-25-batch-02 record): exit 1 · 10 block (all `V59`, the stale `base_ref` from the post-init rebase) · `V7` bundle intact. After re-stamping `state.json` (batch id, owner, `base_ref=f4b53cc7d89bd645a99e0615dbafb7c102de2abd`): exit 1 · **2 block, both `V26` station-expected** (the batch record not yet seeded) · 159 notice · 61 n/a |
| Premises / RC-1 | `origin/main` verified at `f4b53cc7d89bd645a99e0615dbafb7c102de2abd` = HEAD of `fix/gantt-done-visible`; RC-1(a): merge-base of HEAD equals the origin/main tip — the audited change IS the tip; RC-1(b): the story IS already shipped — this batch audits it, it does not re-implement it. RC-2: origin answered. Audit premise (honest record): **implementation preceded the flow** — commit `f4b53cc` shipped 2026-10-26 10:27 -0600 before this batch opened; every requirement in `01-requirements.md` is written retroactively from the operator's request and decisions G1–G5 (`.kimi-prompt.md`), and the change's own evidence (3 suite chunks, 3280 passed, transcripts in `.scratch-evidence/`) stands as the increment evidence. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1–A4 | not fired | judged — the audit creates no module, moves no boundary, changes no interface, plans no increment of its own (the increment under audit is `f4b53cc` itself) |
| B1 | not fired | judged — the audit changes no source ownership; the reverse census of done_rows consumers is the architect lens's question, answered in 02-review.md |
| B2 | not fired | judged — no file moves except `git mv .scratch-evidence/ → evidence/` (evidence hygiene, commissioned) |
| **B3** | **fired** | probe — a byte-level golden captures the touched surface: `.dev-flow/2026-10-20-batch-01/evidence/frames-base.json` (TC-2203 golden of a SEALED batch) was regenerated inside `f4b53cc`; the qa lens owes the golden-file verdict |
| B4 | not fired | judged — the gantt frames are consumed by no component (user/evidence artifacts) |
| C1–C8 | not fired | judged — no auth/secrets/network/input-surface content; the change is pure presentation-of-board-data |
| **D1** | **fired** | judged — the change altered a user-visible surface (the board's gantt); the ux lens owes real-terminal captures at 118x30 and 80x24 |
| D2 | not fired | judged — no prototype in this batch |
| E1–E3 | not fired | judged — one audited story, no high-risk context beyond the sealed-oracle question (B3) |
| F1 | not fired | bundle runtime — `V7` line stands as the probe |
| F2 | not fired | `.dev-flow/BACKLOG.md` carries a 2026-10-25 refresh; this batch appends its open findings at close |
| Review take-up | operator directive | the commission names four lenses explicitly (architect · code-reviewer · qa-reviewer · ux-reviewer), all spawned as independent generic sub-agents with their `agents/` role files |

## Where we are

P0 intake → P1 retroactive requirements → P2 four-lens review → P4 validation (targeted re-runs +
the shipped chunk transcripts) → P5 close. No P3 increment of new code: the audited increment is
`f4b53cc` itself; its packet is written retroactively at `03-increments/increment-001.md`.

## Risks / watch-items

- **R1 (HIGH-candidate).** A sealed batch's oracle (`frames-base.json` of 2026-10-20-batch-01) was
  regenerated by the change. If anything beyond the four gantt frames moved, a sealed record was
  falsified. The qa lens holds this question; the verdict lands in 02-review.md and 04-validation.md.
- **R2.** Done rows consume fold room (G3): at 80x24 a busy board shows fewer projects; the ux
  lens captures this on a real terminal.
- **R3.** `state.json` `owner` previously named another checkout (`V40`); re-stamped to this
  worktree at P0. One checkout, one active batch.

## Gate notices and runtime absences

- **Runtime mechanisms unavailable (named once, per SKILL.md step 5):** no Claude Code `Agent`
  tool by name / hooks / prompt guard — the reviewer roles are executed by **generic sub-agents
  spawned per role**, each carrying its `agents/<role>.md` file; no operator prompt channel — every
  gate that would ask runs under the **standing authorization** quoted in the header.
- **`V15`, `V16`, `V17`:** not-run from a bundle (no canon tree / checkout table / settings.json
  hooks), per SKILL.md step 4.
- **`V25`:** not raised — this tree has an `origin` remote and it answered.
- **`V30`:** NOTICE expected at every gate — floors derived from a declared subset; recorded, not a pass.
- **`V40`:** NOTICE at the pre-batch run (state.json owner named `present-hl`); cleared by the P0 re-stamp.
- **`V26` (2 block):** station-expected — the batch record was not yet seeded when the gate ran;
  clears when `01-requirements.md` + ledger exist (walked past per `commands/dev-flow.md`
  §Two-layer validation model, the freshly-seeded-batch case).
- **`V57`:** NOTICE expected at close for the sealed batches whose record predates this tree.
- **`V59`:** the 10 pre-batch BLOCKs were the stale `base_ref`; re-stamped at P0 per the rule's own
  prescription, re-run, cleared.
- **`V42`:** any `⏸ DEFER` marker this batch writes must carry its backlog lane; none planned.

## Decision log (human-readable mirror of `state.json`)

| Station | Date | Decision |
|---|---|---|
| P0 | 2026-10-26 | P0 intake approved under the batch's standing authorization — «Haz el cambio rápido… después auditas el cambio con dev flow.»; state.json re-stamped (batch 2026-10-26-batch-01, owner this worktree, base_ref f4b53cc, phase in-progress); triggers B3/D1 fired; the implementation-preceded-flow premise recorded honestly in the header; gate re-run: 2 station-expected V26 block pending the seeded record. P1 is next. |
| P1 | 2026-10-26 | P1 approved under the standing authorization — retroactive requirements written from the operator's request + G1–G5 (US-3001, HLR-3001..3005 with Statements, 11 LLRs, AT-3001..AT-3006 mapped to the shipped test nodes); the retroactive authorship is declared in the artifact, not disguised; gate 0 block (evidence/gate-p1.txt; one V53 path correction fixed in place). P2 is next. |
| P2 | 2026-10-26 | P2 closed under the standing authorization — four independent lenses as spawned generic sub-agents (architect, code-reviewer, qa-reviewer, ux-reviewer): architect iterate-to-refine on the records layer (AX-1 canon stale HIGH, AX-2 toast stale HIGH, AX-3 legend MEDIUM), code-reviewer OK-TO-ADVANCE 0 HIGH, qa PASS with the golden-file verdict CLEAN, ux PASS with 4 real-terminal captures and window-cleanup PASS; consolidated in 02-review.md; gate 0 block (evidence/gate-p2.txt). P4 is next (no P3 increment of new code — the audited increment is f4b53cc, packet written retroactively at 03-increments/increment-001.md). |
| P4 | 2026-10-26 | P4 closed under the standing authorization — PASS-WITH-NOTES: consumed the change's 3280-passed 3-chunk evidence (moved to evidence/scratch-evidence/), executed targeted re-runs 123+62 passed after the import probe, qa golden verdict CLEAN (4/40 frames, .plain only), ux captures PASS; the two HIGHs are records-layer, none invalidates behaviour; gate 0 block (evidence/gate-p4.txt). P5 close is next. |
| P5 | 2026-10-26 | P5 close under the standing authorization — the canon gained the dated audit annex (20 ids; the stale-row amendment stays open as AUD-01, not applied), the BACKLOG carries AUD-01..AUD-08, the scratch evidence was git-mv'd into the batch, the close record filled, the final gate runs next; no push/merge (not granted). |
