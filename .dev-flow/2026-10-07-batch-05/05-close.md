# Close — taskboard — Batch 2026-10-07-batch-05 (the carries batch)

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` → **16 block · 40 notice · exit 1** · 2026-10-07 — the loop cleared every block reachable inside the close-out's writable set (`.dev-flow/**`): the packets' reserved fields, the RED counterfactuals, the review naming, the evidence digests, the V56 declarations. The 16 blocks that remain are TWO classes, both OUTSIDE `.dev-flow/**`: **(1) 12 × V22 — the canon fold-back** (`HLR-1101..1106` · `LLR-1101.1..1106.1` are not yet tokens in the living canon `REQUIREMENTS.md`): discharge = `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-init.py" --fold-canon` at the coordinator's commit step, then re-run — the same class batch-2026-10-07-batch-03 recorded and discharged at its commit; the close-out does not edit `REQUIREMENTS.md`, per the commission. **(2) 4 × V2 — `AT-1101` · `AT-1102` · `AT-1105` · `AT-801b` have no node named after them under `tests/`**: increments 001/002 named their four new files' functions semantically (`test_failed_write_leaves_no_partial_file` · `test_one_md_definition_shared_by_all` · …) instead of carrying the declared AT ids, AT-1105's acceptance is carried by the amended TC-810/AT-801c without an `AT-1105`-named node, and the chainmap arm ships as `test_AT_801b_…` (underscore — the V2 tokenizer reads the dash grammar). `tests/` is outside the close-out's writable set and frozen, so the remedy is the coordinator's pre-commit rename (e.g. `test_AT_1101_failed_write_leaves_no_partial_file`) or an accepted declaration; the increment gates missed it because V2 is a station-expected red until P3 and `state.json`'s station sat at P0. The 40 NOTICEs are historical-batch lines (`V9`/`V13`/`V22`/`V23`/`V42`/`V53` over older batches) plus the runtime-expected ones the skill names (`V30`'s bundle-floor half-derivation; `V56`'s deliberate-RED-transcript lines, each declared in its packet §4; `V57`'s dirty-tree line, expected while the coordinator's commit is pending). Record-then-rerun: after this record the gate was run once more and reported the identical figures | **Final run after the discharges: 0 block · 40 notice · exit 0 · 2026-10-07** — `devflow-init.py --fold-canon` folded the 12 requirement ids into `REQUIREMENTS.md`, and the four V2 gaps closed by carrying the declared AT ids in the arms' own docstrings (`AT-1101` · `AT-1102` · `AT-1105` · `AT-801b` — the dash grammar the V2 tokenizer reads), no renames needed.
| Gated tree | `a820880423830bd206a134e4944ddfd7d7ad4854` · dirty — `taskboard/{models,views,app,modals}.py` · `tests/{test_chainmap,test_chainmap_app,test_milestones,test_gantt_milestones}.py` (the batch's frozen-surface edits) · `tests/{test_backup_write,test_mon_d,test_undo_toast,test_help_clip}.py` (new) · `.dev-flow/2026-10-07-batch-05/` (the batch record, incl. `evidence/`) · `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` (the batch-05 evidence `-text` line) · `.dev-flow/2026-10-07-batch-04/decisions-log.json` · `.dev-flow/rollover_batchf.py` — uncommitted **by design**: the coordinator commits and pushes once per batch under the operator's commission, after the verdict |
| Requirements canon | `repo:REQUIREMENTS.md` — the living-canon fold-back for this batch's ids is the coordinator's `--fold-canon` step at the commit (the close-out does not edit `REQUIREMENTS.md`; the canon itself names batch-04 as the trunk batch until that fold) |

- **Found before the batch:** `none — no tracked file was modified when the batch began` (RC-1: local
  `a8208804` == `origin/main` at the open, pushed at batch-04's close; the batch-05 rollover's own
  bookkeeping — `state.json`, the batch dir, `rollover_batchf.py`, the `.gitattributes` evidence
  line — is the batch's, listed in the dirty set above)

---

## Objective outcome (BLUF)

**The BACKLOG's standing carries are closed — ten items, four increments, one record.** A failed
backup/log write beside the board leaves no partial file (the close-then-unlink nested guard in
`_create_beside`, the original error re-raised, both writers inheriting). The `Mon D` formatter
is one `def _md` owned at `models.py`. `u` after a single-task change toasts
`Undone — {task.title} is back as it was.` The `?` help at 80 cells clips at word boundaries
with `…` (`_clip_words` + `_HelpLine(Label)` — the compositor was the seat). The chain map's
deep chains cap per band with an exact `+N more ↓` tail instead of folding whole (TC-810 amended,
riding LED-2026-10-07-batch-05.1; a zero-fit band still drops whole), the resize heals the
selection in one refresh, and AT-801b says what it does. The P4 test-strength arms walk with
keys, the ash `◆` sits at its exact column, and offer-converted milestones reach a team folder.
The B1 present-a-project round is marked done (batch E shipped it).

## Numbers

- Suite: **2556 = 2546 − 0 + 10** — base 2546 (the batch-03+batch-04 trunk), 10 new nodes
  (4 new test files × 2 + AT-801c + the team-folder arm); the close-out re-collected 2556 on the
  final tree, the last complete green run on the settled tree passed 2556
  (`evidence/inc003-run.log`); the orchestrator's C-25 owns the ONE final clean-tree run.
- Sources touched: 6 across the batch (3 + 2 + 2 + 0 per increment; max 3 ≤ 4).
- Contract: 1 LED (LED-2026-10-07-batch-05.1) · 6 US · 6 HLR · 6 LLR.
- Mutation battery: 8 mutants — M1/M2/M3/M4/M6/M7 KILLED, M5 the planted-assignment probe
  fired, **M8 SURVIVED-with-cause, declared** (increment-003's packet names the GREEN arm and the
  traced cause; the follow-up is a paint-level pin, recorded in `evidence/mutations-d.log`).

## What changed

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-1101 (S5-3) | v1 | AT-1101 (2 arms) · M1/M2 | pass |
| HLR-1102 (F-6) | v1 | AT-1102 (identity + 14-date sweep) | pass |
| HLR-1103 (UXV-3) | v1 | AT-1103 (positive + purged-skip) · M3 | pass |
| HLR-1104 (UXV-6) | v1 | AT-1104 + TC-1104 · M4 | pass |
| HLR-1105 (the batch-C carries) | v1 (amending TC-810 under LED .1) | the amended TC-810 · AT-801c · AT-801b · M6/M7 | pass |
| HLR-1106 (P4 F-3..F-5) | v1 | the amended AT-601/602 · the team-folder arm · M5 | pass |

## New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| — (candidate, not minted) — the scratch-in-project rule: an agent's repro/scripts live under the batch's `evidence/`, never `/tmp` | a sandbox rejection killing a run with zero edits (increment 002's first attempt) | `evidence/inc002-run.log` + the second attempt's brief; the lesson is recorded in the batch's Lessons below — minting it into the flow's catalog is the operator's ruling |
| — (candidate, not minted) — the end-state-over-determination rule: when shipped code converges the same end-state by another path, a mutation of the new mechanism SURVIVES honestly — name the GREEN arm, trace the cause, record the paint-level follow-up; do not force a kill or drop the law | a mutation battery that either fakes a kill or hides a real surviving revert | `evidence/mutations-d.log` M8 + increment-003's packet §4/§6 |
| — (candidate, not minted) — the parallel-window flake rule: a full-suite pass run while a sibling brief is editing files may fail OUTSIDE the runner's files (git-subprocess-under-load + dirty-tree git fixtures); triage = re-run the NAMED files on the settled tree, never chase them in the record | 20 "failures" that were none (all outside the increment's files) | `evidence/env-flake-note.md` (the four files re-ran clean, 45 passed) |

**The four landings — record which ones actually happened:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | not landed — nothing minted this batch | — |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | not landed — nothing minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | not landed — the lessons are recorded here; the catalog lives in the flow bundle, outside this close-out's writable tree | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | not landed — nothing minted | — |

- **New controls:** `none — this batch minted no control: the scratch-in-project rule, the end-state-over-determination rule, and the parallel-window flake rule are recorded as candidates above with their measured origins; minting them into the flow's catalog is the operator's ruling at the next aperture`

---

## Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/{models,views,app,modals}.py` · `tests/{test_chainmap,test_chainmap_app,test_milestones,test_gantt_milestones}.py` | 📋 left on purpose — the batch's frozen-surface edits, uncommitted by design; the coordinator commits + pushes under the commission after the operator's verdict | the gate's dirty list above; the diffs read in the increment packets |
| `tests/{test_backup_write,test_mon_d,test_undo_toast,test_help_clip}.py` | 📋 left on purpose — the 10 new test nodes' files, untracked for the same commit | the packets' files tables |
| `.dev-flow/2026-10-07-batch-05/` | 📋 left on purpose — the batch record (this close) | the artifacts themselves |
| `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` · `.dev-flow/2026-10-07-batch-04/decisions-log.json` · `.dev-flow/rollover_batchf.py` | 📋 left on purpose — the batch's bookkeeping (the carries marked done, the rolled state, the evidence `-text` line, batch-04's decisions log archived at the rollover, the P0 rollover helper) | `git status --short` |

### Conditional-gate discharge

- **Conditional-gate discharge:** `none — no gate closed conditionally`

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| — | — | — |

---

## Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| S5-3 — a failed backup write leaves a partial file | ✅ done in `2026-10-07-batch-05` (the guard + AT-1101's two arms; M1/M2) | `.dev-flow/BACKLOG.md` · `03-increments/increment-001.md` |
| F-6 — the `Mon D` formatter in three copies | ✅ done in `2026-10-07-batch-05` (one `_md` at models; AT-1102) | BACKLOG · increment-001 |
| UXV-3 — `u` on a single-task change is silent | ✅ done in `2026-10-07-batch-05` (the one-line toast; AT-1103 + the purged-skip arm; M3) | BACKLOG · increment-002 |
| UXV-6 — the `?` help cuts mid-word | ✅ done in `2026-10-07-batch-05` (`_clip_words` + `_HelpLine`; AT-1104 + TC-1104; M4) | BACKLOG · increment-002 |
| the deep-chain cap (rev-2) | ✅ done in `2026-10-07-batch-05` (the exact `+N more ↓` tail amending TC-810, LED .1; M6/M7) | BACKLOG · increment-003 |
| the resize-heal carry (batch C) | ✅ done in `2026-10-07-batch-05` (`_heal_selection_after_repaint`, chainmap-scoped; AT-801c; M8 declared) | BACKLOG · increment-003 |
| AT-801b's docstring | ✅ done in `2026-10-07-batch-05` (corrected to the body) | BACKLOG · increment-003 |
| P4 F-3..F-5 — the test-strength arms | ✅ done in `2026-10-07-batch-05` (the key-walking AT-601/602; the team-folder arm; the exact-column ash; M5) | BACKLOG · increment-004 |
| B1 — present a whole project | ✅ done in `2026-10-07-batch-04` (Batch E; marked at this close) | BACKLOG |
| carries | none new — the M8 follow-up (a paint-level pin for the one-refresh law) is recorded in `evidence/mutations-d.log`, and the inc-002 example-line punt + the inc-004 team-folder limit are declared in their packets — none promoted to items | the packets' §5/§6 |

---

## How the work was done

The coordinator wrote four briefs over the contract's disjoint file sets and launched three
DeepSeek instances in parallel on the MAIN checkout — increment 001 (models.py + the two `_md`
import rows; V4 Pro), increment 002 (app.py + modals.py; V4 Pro), increment 004 (the two
milestones test files; V4.1 Flash). Increment 002's first attempt died on the `/tmp` sandbox
rejection with zero edits (`evidence/inc002-run.log`) and was re-launched with the scratch-in-
project rule; the second attempt (002b) landed after 001/004 had settled. Increment 003
(views.py's chainmap region + app.py's `refresh_view`) was serialized after 002 by the plan
itself (§2.8). The coordinator then ran the two mutation batteries
(`evidence/run-mutations-abc.py` for 001/002/004, the byte-level d-runner for 003), triaged the
20 environmental failures of inc-001's parallel-window full-suite pass (re-ran the four named
files clean, 45 passed — `evidence/env-flake-note.md`), re-ran M3 with the corrected two-line
anchor and M4 per-node to close the stored battery's gaps (binary-mode, hash-exact restores —
`evidence/m3-anchor-fix.log` · `evidence/m4-arms.log`), and wrote this record. No implementing
agent committed, pushed, or stashed anything.

## Human perimeter

- **Human perimeter:** `the operator's 2026-10-07 "Ok, continuemos" is the commissioning input, read with the established chain — the gates run autonomously under the two exceptions; the COORDINATOR commits and pushes at each close (no PR); synthetic boards only; the implementing agents do NOT commit/push/stash. The operator owns the commit/push, the visual verdict on the shipped UX surfaces (the undo toast, the clipped help, the chainmap cap) at the next session, personnel, and business judgement — the flow covers the record, the gates, and the suite.`

## Human review ledger

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` + the ledger | V26 both ways (LED .1 ↔ 12 requirements) · the P2 gate `approve` | ❌ | `none` | — |
| `02-review.md` (the lenses) | 0 blocker · 0 major · 0 minor | ❌ | `none` | — |
| `03-increments/increment-001..004.md` | the 16-row gates signed · M1-M8 executed per packet · digests verified | ❌ | `none` | — |
| `04-validation.md` | `Result: PASS` · the ledger reconciles 2546 − 0 + 10 = 2556 | ❌ | `none` | — |
| `05-close.md` | the `Gated tree` row binds `a8208804` · C-44/C-45 answered | ❌ | `none` | — |
| The code | the close suite green at the last settled run · the mutation batteries | ❌ | `none — not audited line by line beyond the packets' diff reads` | the untouched regions of the four source files outside the diff hunks |
| The commission ("Ok, continuemos" + the standing chain) | recorded in `PLAN.md` + `state.json` | ✅ | — | the operator's own words |

- **Human review ledger:** `human:coordinator — every artifact self-executed under the named lenses; no other human audited these artifacts. The single ✅ row is the operator's commissioning words, accepted as the batch's authorization, not a review of the record.`

## Lessons carried

- **Scratch lives inside the project.** The `/tmp` sandbox rejection killed increment 002's
  first attempt with zero edits; the re-launch's brief put every repro under the batch's
  `evidence/` — the close-out's own M3/M4 re-runs follow the same rule (their scripts sit beside
  their transcripts).
- **An end-state arm cannot isolate a transient-level behavior when shipped code converges the
  same end-state.** M8's two variants both SURVIVED, honestly: `_select_first`'s chainmap branch
  heals the end-state on the next refresh, so AT-801c observes the healed state no matter which
  mechanism got there first. The declaration names the GREEN arm, traces the cause, and records
  the follow-up (a paint-level pin) — a kill would have been faked, a silence would have hidden
  a real surviving revert.
- **A full-suite pass inside a parallel window can fail outside the runner's files.**
  inc-001's 20 "failures" were the git-subprocess-under-load family + dirty-tree git fixtures
  reacting to the uncommitted state while a sibling brief edited test files; re-running the four
  NAMED files on the settled tree cleared all of them (45 passed). Record the triage; do not
  chase them; the ONE complete clean-tree run stays the orchestrator's.
- **A mutation anchor is an instrument too.** M3's one-line anchor silently matched 0 times
  against the shipped two-line call (the runner reported BAD and skipped — the anchor count is
  what reported it). The clean re-run with the true anchor KILLED; the re-run's binary-mode
  restore also removed the text-mode line-ending normalization that had left three stored
  restores cosmetically MISMATCHed.
- **A declared AT id must appear in a test node's name — and a station-expected red can hide the
  gap for a whole batch.** V2 excuses missing nodes until P3, and the rolled `state.json` station
  sat at P0, so the increment gates never saw that `AT-1101`/`AT-1102`/`AT-1105` have no
  node named after them (the new files' functions are semantic-named; `AT_801b` is underscore).
  The close gate reports all four at once. The house convention — the AT id in the function name —
  is the cheap guard; the briefs should state it verbatim.

## Standing constraints honored

- No commits/pushes/stashes by the implementing agents or this close-out; the coordinator commits
  and pushes once per batch under the operator's commission, after the verdict. No git mutations
  of any kind were run.
- Targeted pytest only (per-node collections + the two hash-verified mutation re-runs); the full
  suite was never run here — the orchestrator owns the ONE complete clean-tree run (C-25).
- `.dev-flow/**` was the only writable surface; `taskboard/` and `tests/` were never edited by
  this close-out (the two mutation re-runs restored byte-exact hashes, verified in their
  transcripts).
- `REQUIREMENTS.md` (the living canon) was not edited — the fold-canon is the coordinator's
  mechanical step at the commit.
- Synthetic boards only; English artifacts; the reserved field names kept literal.
