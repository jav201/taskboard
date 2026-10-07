# Batch close — taskboard — Batch 2026-10-07-batch-03

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**,
> and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/docs/close-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Conditional-gate discharge` · `New controls` · `Human perimeter` · `Human review ledger` · `Gated tree` · `Found before the batch` · `⏸ DEFER`
> **And the §6 DEPTH tokens — cell VALUES rather than field names, reserved for the same reason:**
> `light` · `rigorous` · `spot-check` · `none` · `✅` · `❌`. A CLOSED set, declared closed by the first
> revision that ships it — so the vocabulary a later promotion of `V54` to BLOCK will need already exists,
> instead of being introduced over a free-text field that six authors have by then written six ways.
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Notice convention.** `⚠` yellow = declare and continue · `✗` red = block · `✓` green = satisfied
> **with its citation**.

---

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` → **6 block · 34 notice · exit 1** · 2026-10-07 — every block is the SAME class, `V22`'s canon fold-back (the six requirement ids mirrored into `REQUIREMENTS.md`), which sits outside the close-out's writable file set (`.dev-flow/**` + one `.gitattributes` line); the loop cleared every other block it found (`V59` trace id · `V36` reviewer naming · `V41` evidence paths · `V56` figure naming) and the remaining NOTICEs are historical-batch lines or the three runtime-expected ones named in §5. Discharge: `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-init.py" --fold-canon` at the coordinator's commit step, then re-run — recorded in *What was NOT done* |
| Gated tree | `34bab3c8b110e0a18ddba281c3e75d8597e07a8f` · dirty — `taskboard/app.py` · `taskboard/models.py` · `taskboard/views.py` · `tests/test_team_sync.py` (the batch's frozen-surface edits) · `tests/test_cleanup.py` (new) · `.dev-flow/2026-10-07-batch-03/` (new) · `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` · `.dev-flow/2026-10-07-batch-02/decisions-log.json` · `.dev-flow/rollover_cleanup.py` — uncommitted **by design**: the coordinator commits and pushes once per batch under the operator's commission, after the verdict |
| Requirements canon | `repo:REQUIREMENTS.md` (`artifact_homes.requirements_canon`) — the living-canon table; this batch's HLR-901/902/903 + LLR rows land in it at the coordinator's commit (the close-out's allowed file set is `.dev-flow/**` plus one `.gitattributes` line, so the canon itself was not writable here — declared, not deferred silently) |

---

## 1 · What changed

*(BLUF. What the user can now do that they could not before, and through which surface. Then the mechanism.)*

**The six loose items are closed.** A failed link migration can no longer lose the board or
re-run on a false mark — the failure path restores the board and the mark first, cleans up
best-effort, and names the ORIGINAL failure (`run_link_migration`, `result.error`). A
hand-edited board with `"title": 5` (or a list, mapping, null, bool) now opens instead of
crashing a render — scalars keep the user's text, containers read `Untitled` (`Board.load`).
What the kanban screen says is now what it draws: the `?` legend names `◆` only for DRAWN
bands, a milestones-only project keeps its rule-only band (`N open`), a late milestone below
the fold marks the fold row, and milestones read as milestones in lanes, agenda and focus.
**Fold canon pinned (7 census nodes):** the fold row's canonical literal is `▼ N below` with
the ` · ▲N ◆` suffix appended before the final fit — `taskboard/views.py:5161` (the literal)
and `:5179-5181` (the suffix ahead of `fit`) — pinned by `tests/test_kanban_readable.py:66,
:480, :574, :607, :1221` (7 of the 9 TC-311 nodes) and AT-903 arm 3's `▼.*▲1 ◆`; the
`▾ N more` rename (the BACKLOG's pre-shipped note) was tried once, reddened the 7 censuses,
and was reverted (LED .3, `evidence/inc002-mutations.log` M1). Suite at close: **2541 passed,
0 failed** (the orchestrator's ONE run, C-25).

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-901` (S-4) | v1 | `AT-901` · `TC-901` | pass |
| `HLR-902` (S-9) | v1 | `AT-902` · `TC-902` | pass |
| `HLR-903` (K2-1 · D-623 · UX2-2 · milestones-in-views) | v1 | `AT-903` (×4 arms) · the TC-311 census | pass |

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| — (candidate, not minted) — the fold-canon lesson: a BACKLOG shape that predates a shipped law must not rename the law's literal; the contract carries the canonical literal and the census pins it | a "cleanup" renaming a pinned literal and reddening its census (measured: 7 of 9 TC-311 nodes, this batch's increment 002) | LED .3 + this close; promotion to a catalog control is the operator's ruling — the catalog lives in the flow bundle, outside this close-out's writable tree |

**The four landings — record which ones actually happened. Command-but-not-template is *half-encoded*, and the missing half is the enforceable one:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | not landed — nothing minted this batch | — |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | not landed — nothing minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | not landed — nothing minted | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | not landed — nothing minted | — |

- **New controls:** `none — this batch minted no control: the fold-canon lesson is recorded as LED .3 and the §1 pin above; minting it into the flow's catalog is the operator's ruling at the next aperture`

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/models.py` · `taskboard/app.py` · `taskboard/views.py` · `tests/test_team_sync.py` | 📋 left on purpose — the batch's frozen-surface edits, uncommitted by design; the coordinator commits + pushes under the commission after the operator's verdict | the gate's dirty list above; the diffs in `evidence/close-review.log` LENS 4 |
| `tests/test_cleanup.py` | 📋 left on purpose — the batch's 12 new test nodes, untracked for the same commit | sha256 `b604df5e8ec072782b522220d1d1a4d37187935848f8d9706b9a40cfb87ce15b` |
| `.dev-flow/2026-10-07-batch-03/` | 📋 left on purpose — the batch record (this close) | the artifacts themselves |
| `.dev-flow/state.json` · `.gitattributes` · `.dev-flow/2026-10-07-batch-02/decisions-log.json` · `.dev-flow/rollover_cleanup.py` | 📋 left on purpose — the batch's own bookkeeping (decisions, the evidence-line attribute, the archived batch-C log, the P0 rollover helper) | `git status --porcelain` |

- **Found before the batch:** `none — no tracked file was modified when the batch began` (base_ref `34bab3c8…` equals the pushed Batch C tip; the tree was clean at open)

### Conditional-gate discharge

- **Conditional-gate discharge:** `none — no gate closed conditionally`

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| — | — | — |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| S-4 — the link migration's cleanup-before-restore | ✅ done in `2026-10-07-batch-03` (restore-first + best-effort cleanup + the refusing-unlink arm; TC-901/AT-901) | `.dev-flow/BACKLOG.md` line 43 · `03-increments/increment-001.md` |
| S-9 — a non-text title crashes the app | ✅ done in `2026-10-07-batch-03` (the load-boundary coercion; TC-902's five exact strings; the folded `["Good", "123"]`) | BACKLOG line 47 · increment-001 |
| K2-1 — the kanban `?` legend reads the unfiltered board | ✅ done in `2026-10-07-batch-03` (search half: app.py's filtered-? branch; fold half: the shared `_fold_keep` drawn-band seat) | BACKLOG line 50 · increments 001+002 |
| UX2-2 — a late milestone below the fold | ✅ done in `2026-10-07-batch-03` (the fold-row marker `▼ N below · ▲1 ◆`; LED .3's canon) | BACKLOG line 52 · increment-002 |
| D-623 — a milestones-only project draws no kanban band | ✅ done in `2026-10-07-batch-03` (the rule-only band carrying `◆`, head `N open`) | BACKLOG line 55 · increment-002 |
| milestones-in-views (lanes/agenda/focus) | ✅ done in `2026-10-07-batch-03` (the `◆` marker sites; marker-only, CL-9) | BACKLOG line 57 · increment-002 |
| carries | none new — the two minor review notes (dead `isinstance` guard; PLAN template cells) stay notes in `02-review.md` F1/F2, not backlog items, per the cleanup-batch scope | `02-review.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-07-batch-03
mode: core
verdict: pass
increments: 2
source_files_max: 2          # increment 001: models.py + app.py (increment 002: views.py only)
notices_raised: 2            # the two minor review findings declared in 02-review.md (F1 · F2); the final validator run's NOTICE lines naming this batch are enumerated below
rework_returns: 1            # P2 iteration 1 (qa/ux FAIL on the contract wording) → CL-1..CL-9 folded (LED .2) → iteration 2 PASS
triggers_fired: "B1,C5,C6,C8,D1,E1"
tests_base_to_post: "2529 -> 2541"
new_control: none
open_items_next: 10         # 3 chainmap carries + 6 B2a-residue items + 1 present-a-project round — none new from this batch
```

**The final gate runs (record-then-rerun, per the closing rule):** the close record above was
written from the final validating run (**6 block · 34 notice · exit 1**); after writing it the
gate was run once more and reported the identical figures — the record is stable. The six
blocks are the single irreducible class named in §0 (the `V22` canon fold-back into
`REQUIREMENTS.md`, outside the close-out's writable set); the 34 NOTICEs are historical-batch
lines (`V9`/`V13`/`V22`/`V23`/`V42` over older batches) plus the three runtime-expected ones
the skill names (`V30`'s bundle-floor half-derivation; `V53`'s closed-record census delta;
`V57`'s dirty-tree line, expected while the coordinator's commit is pending by design —
`origin` exists here, so the `V25` no-remote notice does not apply).

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` | the contract filled · V33–V35/V45/V46 fields declared | ❌ | `none` | — |
| `02-review.md` (the lenses) | `evidence/close-review.log` executed · 0 blockers · 2 minors | ❌ | `none` | — |
| `03-increments/increment-001.md` · `increment-002.md` | the 16-row gates signed · M1–M2 kills executed per packet · digests verified | ❌ | `none` | — |
| `04-validation.md` | `Result: PASS` · the ledger reconciles 2529 − 0 + 12 = 2541 | ❌ | `none` | — |
| `05-close.md` | the `Gated tree` row binds `34bab3c8…` · C-44/C-45 answered | ❌ | `none` | — |
| The code | the close suite 2541 green · 4 mutants KILLED · the diff read (LENS 4) | ❌ | `none` — not audited line by line beyond the diff read | the untouched 6,800-line views.py outside the diff hunks |
| The commission ("HAz ambas, paraleliza" + the standing authorization) | recorded in `state.json` | ✅ | — | the operator's own words |

- **Human perimeter:** `the operator owns the visual verdict on the fold marker and the render items, the commit/push, personnel, and business judgement — the flow covers the record, the gates, and the suite; nothing else lies outside`
- **Human review ledger:** `none — no human audited these artifacts: the review pool was the coordinator's self-executed lenses (named once in 02-review.md), the suite was the orchestrator's, and the operator's visual verdict on this cleanup batch is invited at the next session`

---

## What was NOT done (declared)

- The batch `PLAN.md` still carries its template placeholder cells (its Triggers/Where-we-are
  rows) — F2 in `02-review.md`; the load-bearing facts live in the contract §2.7 and this close.
- The vault-homed artifacts (`design_pdr` · `design_ddr` · `postmortem` · `metrics` under
  `vault:taskboard/…`) were not written this close-out — no vault in this runtime; the repo
  record is complete and the sync is the operator's `/dev-flow-sync` step.
- `REQUIREMENTS.md` (the living canon) gained no batch-03 rows here — outside the close-out's
  writable file set (`.dev-flow/**` + one `.gitattributes` line). The gate therefore reports the
  six `V22` canon fold-back BLOCKs (HLR-901/902/903 · LLR-901.1/902.1/903.1); the discharge is
  one mechanical command at the coordinator's commit step:
  `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-init.py" --fold-canon` (run
  from the repo root), then the gate re-run — the same step batch 2026-10-07-batch-01/-02 left
  to their commits (their HLR-701/801 rows are not in the canon either). Declared, not deferred
  silently.
- The dead `isinstance(task.title, str)` guard at `team_sync.py:226` was left in place — the
  implementation is frozen; F1 names it.
- No commit, no push — per the standing authorization's Git clause (merge NOT granted; the
  coordinator commits and pushes once per batch after the operator's verdict).
