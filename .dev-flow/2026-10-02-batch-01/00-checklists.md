# Phase checklists — taskboard — Batch 2026-10-02-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/phase-checklists.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to declare the reason ·
> `✗` red = block · `✓` green = satisfied with its citation.
> **A notice that repeats for three consecutive batches becomes a rule or is retired** — decided at close.

> **Re-work counter.** Every station records how many items came **back**, from which station, and why.
> That number is the only cheap signal that a gate is theatre: if the PDR approves and the DDR keeps
> rejecting, the number says so without anyone having to argue it. It feeds the batch metrics.

---

## 1 · INTAKE — repo

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Context of use per story: user · **task** · **environment** |  ✓ | `01-requirements.md` §2.3 (user, task UX-14, environment 80×24 to full screen, Windows Terminal) |
| 2 | Observable outcome stated per story |  ✓ | each US in §2.6 states its outcome ("so that …"); AT table §5 |
| 3 | Risk estimate: importance and criticality, used to prioritise |  ✓ | `Priority:` per HLR in §3; risks in `PLAN.md` §Risks / watch-items |
| 4 | RC-1: `origin/main` tip fetched and recorded in `PLAN.md` **before** deriving |  ✓ | `PLAN.md` §RC-1: `git fetch origin` → `origin/main` = `57a60756fda9` = HEAD |
| 5 | RC-2: `origin` reachable and the age of its newest commit recorded in `PLAN.md` **before** deriving (`git ls-remote --exit-code --heads origin`; V25) |  ⚠ | origin reachable (the P0 fetch succeeded); the newest commit's age was not written into `PLAN.md` — declared here |
| 6 | "already shipped?" check per candidate story |  ✓ | §2.6 DoR column and `evidence/p0-probes.txt`; US-105 classified OUT (A2) |
| 7 | `flow_hash` verified against the manifest (C-45 PULL) |  ✓ | `PLAN.md` §RC-1: validator at P0, `V7` silent (bundle hashes match) |
| 8 | **Triggers evaluated AND recorded — the ones that fired and the ones that did not, each with its probe (C-48)** |  ✓ | `PLAN.md` §Triggers: B1, B4, C, D, E, F2 fired; B2, B3, A, F1 not, each with its probe |
| 9 | Mode declared; any change recorded in `mode_history` with its reason |  ✓ | `state.json` `mode: core`, `mode_history` one entry (kickoff) |

⚠ backlog not refreshed at the previous close · ⚠ a story with a role but no task or environment

## 2 · ARQ — repo *(only if A1/A2/A3/A4 fired)*

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Module map updated — or "no architecture change" **with its empty diff** |  n/a — station not active in this batch | trigger family A did not fire (`PLAN.md` §Triggers); `stations_active` holds no ARQ |
| 2 | Every planned file falls under a declared module |  n/a — station not active in this batch | trigger family A did not fire (`PLAN.md` §Triggers); `stations_active` holds no ARQ |
| 3 | Interfaces that change, listed |  n/a — station not active in this batch | trigger family A did not fire (`PLAN.md` §Triggers); `stations_active` holds no ARQ |
| 4 | Lanes proposed with **disjoint FILE sets**, not just modules |  n/a — station not active in this batch | trigger family A did not fire (`PLAN.md` §Triggers); `stations_active` holds no ARQ |
| 5 | `rationale` per structural decision |  n/a — station not active in this batch | trigger family A did not fire (`PLAN.md` §Triggers); `stations_active` holds no ARQ |

⚠ a planned file under no declared module (the map is stale) · ✗ two lanes sharing even one file

## 3 · REQUIREMENTS — repo

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Each `R-NN` with its `AT` and the surface that produces it |  ✓ | 9 HLR each with `Acceptance test(s)`; AT table §5 names the surface (`TaskboardApp` / shipped files) |
| 2 | **Version per item** (`R-NN v3` · `AT-NNa v2`) |  ✓ | contract v2 at P2; P4 amendments versioned in `01-requirements-ledger.md` LED .26–.31 |
| 3 | Symbols cited with `file:line`, or flagged `NEW` |  ✓ | LLR statements cite `views.py` / `app.py` symbols; new ones flagged NEW in IFC Part A |
| 4 | Premises executed (§2.7), each with its probe |  ✓ | §2.7 P-1..P-10, each with its executed probe (`evidence/p0-probes.txt`) |
| 5 | `shall`/`deberá` only inside statements |  ✓ | `shall` appears only in HLR/LLR statements |
| 6 | Each UX scenario with its observable criterion |  ✓ | UX scenarios carry a numeric pass threshold and negative control per LLR |
| 7 | Cites by id the design record that originated it |  ✓ | §1.4 References: `IMPLEMENTATION-PLAN.md`, `NOTES.md` rounds, `README-AUDIT.md` |
| 8 | Any premise resting on an **absence** flagged as load-bearing, with its synthetic instance (C-55) |  ✓ | load-bearing absences flagged in the packets' C-55 tables, each with its synthetic instance |

⚠ a requirement rising in version without its `AT`/`TC` rising or being re-confirmed

## 4 · PDR — vault + Drive

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Proposal complete (objective · modules · diagrams · interfaces · **proposed test cases** · risks · rejected alternatives **where a real decision exists**, otherwise `n/a — <the decision already made, and by what>`) |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 two-lens review stands in (`02-review.md`) |
| 2 | Respects the ARQ boundaries |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 two-lens review stands in (`02-review.md`) |
| 3 | **Forward applicability: every output has a NAMED consumer** |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 two-lens review stands in (`02-review.md`) |
| 4 | Proposed test cases observable and non-vacuous — **the reddening mutation named for each** |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 two-lens review stands in (`02-review.md`) |
| 5 | Interfaces **frozen** for the fork |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 two-lens review stands in (`02-review.md`) |
| 6 | UX lens applied (family D) · security lens applied (family C) |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 two-lens review stands in (`02-review.md`) |
| 7 | Verdict + record **sealed** (date · verdict · participants · approved ids) |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 two-lens review stands in (`02-review.md`) |

⚠ any PDR output with no consumer · ✗ no increment starts without an approved PDR **when this
station is active** — `ARQ` · `PDR` · `DDR` are **by trigger** in `core` and in
`full` alike (`/dev-flow` §Modes), and `stations_active` in `state.json` is the authority on which stations
exist in *this* batch. **A station absent by design is written `n/a — station not active in this
batch` and never left blank**: a blank is an omission, and a gate nobody owed must
not read like a gate nobody ran.

## 5 · INCREMENT — repo · ×N, one per lane

> **THIS STATION'S CHECKLIST HAS ONE HOME AND IT IS NOT HERE** — `C-50`
. **The increment gate is
> `templates/increment-template.md` §*Increment gate checklist*, copied into every
> packet at `.dev-flow/<batch_id>/03-increments/increment-<NNN>.md`. Sign it there**, with its
> `Owed in` column, its evidence column and its 16 rows.
>
> **What is still signed at this station, here:** the re-work counter above, and this station's entry
> in the sign-off list. The per-increment rows are signed in the packet, once.

## 6 · DDR — vault + Drive · *the join point*

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | What changed against the PDR, and **why** |  n/a — station not active in this batch | one lane, no fork; DDR not in `stations_active` |
| 2 | Frozen interfaces intact — or returned to the trunk, declared |  n/a — station not active in this batch | one lane, no fork; DDR not in `stations_active` |
| 3 | **Reverse census crossed between lanes** |  n/a — station not active in this batch | one lane, no fork; DDR not in `stations_active` |
| 4 | Every `AT` = exactly one on-disk node (C-18) |  n/a — station not active in this batch | one lane, no fork; DDR not in `stations_active` |
| 5 | Ledger **summed** across lanes |  n/a — station not active in this batch | one lane, no fork; DDR not in `stations_active` |
| 6 | Open PDR conditions discharged **by re-reading the artifact** |  n/a — station not active in this batch | one lane, no fork; DDR not in `stations_active` |

⚠ a lane that reached or exceeded the source budget · ✗ a lane that touched another lane's file

## 7 · VALIDATION — repo

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | **ONE complete run**, launched by the orchestrator — never stitched |  ✓ | `evidence/full-suite-close.txt`: one run by the orchestrator, 1611 passed, exit 0, on the frozen tree |
| 2 | Layer 0 unit · layer A white-box · layer B black-box |  ✓ | `04-validation.md` Layer 0 (4 units), Layer A, Layer B (AT-101..113) |
| 3 | UX walkthrough with the **real mechanism** and the **painted** result |  ✓ | ux-reviewer walkthrough in the running app (`04-validation.md` §UX walkthrough); re-check after increment 004 |
| 4 | Representative + **boundary** + **negative** |  ✓ | `04-validation.md` Layer B rows name boundary and negative per AT |
| 5 | The deliverable actually **observed** |  ✓ | captures `evidence/captures/close-*-{118x30,80x24}.{txt,svg}`; README/RUN.md read as shipped files (AT-107) |
| 6 | Bidirectional surface-reachability matrix |  ✓ | `04-validation.md` §Surface-reachability: 0 gaps |
| 7 | **A NEGATIVE result names the over-breadth that makes it sound, and that over-breadth is guarded** (C-55 limb 1) |  ✓ | packets' C-55 tables name the search width (e.g. increment-004: every `Label` in both columns, two sizes) |
| 8 | **Every probe that returned an absence carries its POSITIVE CONTROL** — the same probe, unmodified, returning a non-absence on a known-present case |  ✓ | positive controls cited per absence probe (increment-004: 52 > 48 and 61 > 56 on earlier trees) |
| 9 | Verdict `PASS` / `PASS-WITH-NOTES` / `FAIL` declared as the keyed `**Result:**` field, ONE token — the whole batch-verdict vocabulary, and not the increment gate's `BLOCK` |  ✓ | `04-validation.md` `**Result:** PASS-WITH-NOTES` |
| 10 | **Evaluation with users (ISO 9241-210): the STATE, keyed to what happened** — `performed` / `not performed — <reason>` / `not applicable — no trigger-D surface`, for each of automated walkthrough, expert inspection and evaluation with users, kept apart |  ✓ | automated walkthrough performed (ux-reviewer, two rounds); expert inspection performed (qa, code, security reviewers); evaluation with users not performed — autonomous batch, the operator reviews at his commit gate |
| 11 | `**Layer 0:**` and `**Evidence checklist (qa-reviewer):**` declared as keyed fields, the checklist naming WHO completed it |  ✓ | `04-validation.md` `**Layer 0:**` and `**Evidence checklist (qa-reviewer):**` 11 of 11, named |

## 8 · CLOSE — repo + vault

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | `(item, version)` baseline sealed |  ✓ | `REQUIREMENTS.md` canon fold: 30 rows (9 HLR + 21 LLR), versions per `01-requirements-ledger.md` |
| 2 | Backlog reconciled — the three moves |  ✓ | `05-close.md` §4: carried (A2, app-wide budget, operator questions), closed (gantt items ✓ done), added (UXV-12 re-walk, inherited privacy strings) |
| 3 | C-44 reconciliation across **every** repo touched, auxiliary ones included |  ⚠ | one repo; nothing committed by this agent — every change is a working-tree change for the coordinator's commit (`05-close.md` §3) |
| 4 | Every artifact in its declared home, **no copies** |  ✓ | batch record under `.dev-flow/2026-10-02-batch-01/`, evidence under its `evidence/`; no copies |
| 5 | repo↔vault ids resolved in both directions |  n/a — no vault artifact this batch | `obsidian_synced: false`; nothing written to the vault |
| 6 | New controls pushed upstream (C-45): command · artifact · catalog · pushed |  ✓ | none minted (`05-close.md` §2) |
| 7 | Re-work counted per station |  ✓ | P2 1 return (iterate-to-refine), P4 1 return (iterate-to-fix → increment 004); code review HIGHs: 001 ×2, 002 ×1 |
| 8 | **What was NOT done, declared** |  ✓ | `05-close.md` §3 and §4: A2 not done, UXV-12 not re-walked, user evaluation not performed, commit left to the coordinator |

⚠ any commit that exists and never landed · ⚠ a notice now in its third consecutive batch — make it a rule or retire it

## Re-work counter

| Station | Items that came back | From | Why |
|---|---|---|---|
| P2 | 1 loop (Q-1, Q-2, UX-1) | P2 iteration 1 | qa FAIL and ux FAIL on the contract v1 |
| P3 | 3 HIGH folded (001 F1, F3; 002 F1) | code-reviewer | selection cut at full body; legend read another frame; clipped titles in accent |
| P4 | 1 loop → increment 004 | ux UXV-1, qa G-001 | help cut mid-word; ATs on several nodes (C-18) |

## Sign-off

- P0 · P1 · P2 · P3 · P4 · P5: self-approved by the agent under the standing authorization ("Autónomo, agente Opus"), each recorded in `state.json` `decisions_log`; 0 HIGH open.
- Close privacy sweep (S-4, S-8): `evidence/privacy-sweep-close.txt` — entity-decoded, file names only; 0 real-board strings in any changed file; 2 inherited hits (state `owner`, BACKLOG e-mail) unchanged from `57a6075`, carried to BACKLOG.
- Close security verification (a)–(c): security-reviewer PASS-WITH-NOTES, 0 HIGH — BACKLOG S-5/S-8/close entries present, sweep independently re-run (84 files, 0 new personal strings), review rows recorded; N1–N3 (LOW, wording of the sweep classification and the BACKLOG entry) folded.
