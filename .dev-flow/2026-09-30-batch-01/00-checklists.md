# Phase checklists — taskboard — Batch 2026-09-30-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.

> **Owed in.** `core` ✓ · `full` ✓
> **Source:** `/dev-flow-init` step 4's seed-by-mode table, which is this fact's one home (flow rev72, `T05`). A mode marked `—` **does not owe this artifact, and its absence is not an omission**; `by trigger` means the station exists only when the `triggers` block fired, and `stations_active` in `state.json` is the authority for *this* batch. Where a SECTION or a gate row is owed more narrowly than the artifact, it says so on the row.

> **Who signs these.** `qa-reviewer` signs one checklist **per station listed here** — INTAKE · ARQ · REQUIREMENTS · PDR · INCREMENT · DDR · VALIDATION · CLOSE. P2 (cross-agent review) and P6 (docs) are gated on their own artifacts' checks and carry no separate checklist in this file — that is
> what makes review and re-work *visible* instead of assumed. Each item carries **executed evidence**:
> a node id, command output, or a `file:line`. **An item without a citation is asserted, not satisfied.**
> ↳ **INCREMENT is signed in the packet, not here** — §5 is a pointer from flow rev72; see it.

> **MODE APPLICABILITY — which stations exist at all (flow rev72, `T05`).** `stations_active` in
> `state.json` is the authority: `core` → `["P0", "P1", "P2", "P3", "P4", "P5"]` (one home:
> `/dev-flow-init` step 3's bullet — this literal is held equal to it by `CMD CORE-STATIONS-agree`),
> `full` → all seven; `ARQ` · `PDR` · `DDR` are **by trigger** in `core` and in
> `full` alike (`/dev-flow` §Modes is that rule's one home), and the `triggers` block records which fired. **A station this batch
> does not have is written `n/a — station not active in this batch`, with the reason, and is never
> left blank**: *absent by design* and *omitted without a reason* must not look alike, which is the
> same distinction `stations_active` already draws and the one this file lacked the vocabulary for.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to declare the reason ·
> `✗` red = block · `✓` green = satisfied with its citation.
> **A notice that repeats for three consecutive batches becomes a rule or is retired** — decided at close.

> **Home follows the station** (see §Artifact homes in `/dev-flow`): intake · requirements · increment ·
> validation → **repo**. PDR · DDR → **vault + Drive** (`artifact_homes.design_pdr` / `design_ddr`),
> **staged locally and published by `/dev-flow-sync` alone**. Close → **repo**, canonical — the vault
> `<batch_id>-README.md` (`artifact_homes.metrics`) is a **generated view** of it, written only by
> `/dev-flow-sync`. Until flow rev72 this row read `Close → both` — two homes for one artifact, and
> no word on which of them was canonical (`Q22`). The retired phrase is recorded inside a span, because
> a history note spelled as live prose reads to a scanner exactly like the assignment it replaced.

> **Re-work counter.** Every station records how many items came **back**, from which station, and why.
> That number is the only cheap signal that a gate is theatre: if the PDR approves and the DDR keeps
> rejecting, the number says so without anyone having to argue it. It feeds the batch metrics.

---

## 1 · INTAKE — repo

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Context of use per story: user · **task** · **environment** | | |
| 2 | Observable outcome stated per story | | |
| 3 | Risk estimate: importance and criticality, used to prioritise | | |
| 4 | RC-1: `origin/main` tip fetched and recorded in `PLAN.md` **before** deriving | | |
| 5 | RC-2: `origin` reachable and the age of its newest commit recorded in `PLAN.md` **before** deriving (`git ls-remote --exit-code --heads origin`; V25) | | |
| 6 | "already shipped?" check per candidate story | | |
| 7 | `flow_hash` verified against the manifest (C-45 PULL) | | |
| 8 | **Triggers evaluated AND recorded — the ones that fired and the ones that did not, each with its probe (C-48)** | | |
| 9 | Mode declared; any change recorded in `mode_history` with its reason | | |

⚠ backlog not refreshed at the previous close · ⚠ a story with a role but no task or environment

## 2 · ARQ — repo *(only if A1/A2/A3/A4 fired)*

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Module map updated — or "no architecture change" **with its empty diff** | | |
| 2 | Every planned file falls under a declared module | | |
| 3 | Interfaces that change, listed | | |
| 4 | Lanes proposed with **disjoint FILE sets**, not just modules | | |
| 5 | `rationale` per structural decision | | |

⚠ a planned file under no declared module (the map is stale) · ✗ two lanes sharing even one file

## 3 · REQUIREMENTS — repo

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Each `R-NN` with its `AT` and the surface that produces it | | |
| 2 | **Version per item** (`R-NN v3` · `AT-NNa v2`) | | |
| 3 | Symbols cited with `file:line`, or flagged `NEW` | | |
| 4 | Premises executed (§2.7), each with its probe | | |
| 5 | `shall`/`deberá` only inside statements | | |
| 6 | Each UX scenario with its observable criterion | | |
| 7 | Cites by id the design record that originated it | | |
| 8 | Any premise resting on an **absence** flagged as load-bearing, with its synthetic instance (C-55) | | |

⚠ a requirement rising in version without its `AT`/`TC` rising or being re-confirmed

## 4 · PDR — vault + Drive

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Proposal complete (objective · modules · diagrams · interfaces · **proposed test cases** · risks · rejected alternatives **where a real decision exists**, otherwise `n/a — <the decision already made, and by what>`) | | |
| 2 | Respects the ARQ boundaries | | |
| 3 | **Forward applicability: every output has a NAMED consumer** | | |
| 4 | Proposed test cases observable and non-vacuous — **the reddening mutation named for each** | | |
| 5 | Interfaces **frozen** for the fork | | |
| 6 | UX lens applied (family D) · security lens applied (family C) | | |
| 7 | Verdict + record **sealed** (date · verdict · participants · approved ids) | | |

⚠ any PDR output with no consumer · ✗ no increment starts without an approved PDR **when this
station is active** — `ARQ` · `PDR` · `DDR` are **by trigger** in `core` and in
`full` alike (`/dev-flow` §Modes), and `stations_active` in `state.json` is the authority on which stations
exist in *this* batch. **A station absent by design is written `n/a — station not active in this
batch` and never left blank** (flow rev72, `T05`): a blank is an omission, and a gate nobody owed must
not read like a gate nobody ran.

## 5 · INCREMENT — repo · ×N, one per lane

> **THIS STATION'S CHECKLIST HAS ONE HOME AND IT IS NOT HERE** — `C-50`, flow rev72, `T05`, on the
> enumeration `increment-template.md` wrote at rev68. **The increment gate is
> `templates/increment-template.md` §*Increment gate checklist*, copied into every
> packet at `.dev-flow/<batch_id>/03-increments/increment-<NNN>.md`. Sign it there**, with its
> `Owed in` column, its evidence column and its 16 rows.
>
> **Why a POINTER and not a regenerated copy — measured, not preferred.** Until rev72 this section
> carried its own 10-row version, and it had already diverged: measured 2026-09-10 it carried **no row
> at all** for five of the sixteen the packet's table carries — flow revs 60, 63, 64 and 66 each
> extended the gate and skipped this copy — and it cited **0 of the 12** field-keyed rules that table
> cites. The five are enumerated once, in `increment-template.md`'s own note, and are deliberately not
> re-listed here: a pointer that restates the rows is the second inventory it exists to end. **No rule reads
> either table**: `00-checklists.md` is in no rule's artifact family (`V39`'s family map names
> `01-`, `02-`, `04-`, `05-` and `06-docs/` and nothing else), so a regenerated copy would need a
> generator AND a guard to protect a document that has no reader, while a pointer needs neither and
> cannot diverge. `TPL CHECKLIST-one-home` reddens if a gate table is planted back here.
>
> **What is still signed at this station, here:** the re-work counter above, and this station's entry
> in the sign-off list. The per-increment rows are signed in the packet, once.

## 6 · DDR — vault + Drive · *the join point*

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | What changed against the PDR, and **why** | | |
| 2 | Frozen interfaces intact — or returned to the trunk, declared | | |
| 3 | **Reverse census crossed between lanes** | | |
| 4 | Every `AT` = exactly one on-disk node (C-18) | | |
| 5 | Ledger **summed** across lanes | | |
| 6 | Open PDR conditions discharged **by re-reading the artifact** | | |

⚠ a lane that reached or exceeded the source budget · ✗ a lane that touched another lane's file

## 7 · VALIDATION — repo

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | **ONE complete run**, launched by the orchestrator — never stitched | | |
| 2 | Layer 0 unit · layer A white-box · layer B black-box | | |
| 3 | UX walkthrough with the **real mechanism** and the **painted** result | | |
| 4 | Representative + **boundary** + **negative** | | |
| 5 | The deliverable actually **observed** | | |
| 6 | Bidirectional surface-reachability matrix | | |
| 7 | **A NEGATIVE result names the over-breadth that makes it sound, and that over-breadth is guarded** (C-55 limb 1) | | |
| 8 | **Every probe that returned an absence carries its POSITIVE CONTROL** — the same probe, unmodified, returning a non-absence on a known-present case | | |
| 9 | Verdict `PASS` / `PASS-WITH-NOTES` / `FAIL` declared as the keyed `**Result:**` field, ONE token — the whole batch-verdict vocabulary, and not the increment gate's `BLOCK` | | |
| 10 | **Evaluation with users (ISO 9241-210): the STATE, keyed to what happened** — `performed` / `not performed — <reason>` / `not applicable — no trigger-D surface`, for each of automated walkthrough, expert inspection and evaluation with users, kept apart | | |
| 11 | `**Layer 0:**` and `**Evidence checklist (qa-reviewer):**` declared as keyed fields, the checklist naming WHO completed it | | |

✗ **Never pre-write the answer to item 10.** An instruction to state that evaluation with users was
NOT performed tells a batch that ran one to deny its own evidence. Declare what happened; if it did
not happen, say so with the reason. (`close-template.md` §*Declare what was NOT done* is the form.)

## 8 · CLOSE — repo + vault

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | `(item, version)` baseline sealed | | |
| 2 | Backlog reconciled — the three moves | | |
| 3 | C-44 reconciliation across **every** repo touched, auxiliary ones included | | |
| 4 | Every artifact in its declared home, **no copies** | | |
| 5 | repo↔vault ids resolved in both directions | | |
| 6 | New controls pushed upstream (C-45): command · artifact · catalog · pushed | | |
| 7 | Re-work counted per station | | |
| 8 | **What was NOT done, declared** | | |

⚠ any commit that exists and never landed · ⚠ a notice now in its third consecutive batch — make it a rule or retire it
