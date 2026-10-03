# Phase checklists — taskboard — Batch 2026-10-02-batch-03

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
| 1 | Context of use per story: user · **task** · **environment** |  ✓ | `01-requirements.md` §2.3: one operator; the daily read of the kanban (key `4`), moving cards with `[`/`]`; Windows Terminal truecolor, 80×24 to full screen |
| 2 | Observable outcome stated per story |  ✓ | US-301..303 each state their outcome ("so that …"); AT table §5 |
| 3 | Risk estimate: importance and criticality, used to prioritise |  ✓ | `Priority:` per HLR in §3; risks in `PLAN.md` §Risks / watch-items |
| 4 | RC-1: `origin/main` tip fetched and recorded in `PLAN.md` **before** deriving |  ✓ | `PLAN.md` §RC-1: `git fetch origin` → `origin/main` = `13745f6f268f` = HEAD = merge-base |
| 5 | RC-2: `origin` reachable and the age of its newest commit recorded in `PLAN.md` **before** deriving (`git ls-remote --exit-code --heads origin`; V25) |  ⚠ | origin is reachable (the P0 fetch succeeded), but the newest commit's age was not written into `PLAN.md`. Declared here, as in batch-02 |
| 6 | "already shipped?" check per candidate story |  ✓ | `evidence/p0-probes.txt` P-1..P-6 and `evidence/p1-geometry.txt`: each feature measured absent on the base tree (one-row cards, a per-column band, no rail, no fold row) |
| 7 | `flow_hash` verified against the manifest (C-45 PULL) |  ✓ | the pinned rev98 bundle (skills `48154ab`, operator: "Sí, fijar a rev98"); V7 clean at kickoff and at close |
| 8 | **Triggers evaluated AND recorded — the ones that fired and the ones that did not, each with its probe (C-48)** |  ✓ | `PLAN.md` §Triggers: B1, B4, C, D, E, F2 fired; B2, B3, A (judged, D-310), F1 not fired, each with its probe |
| 9 | Mode declared; any change recorded in `mode_history` with its reason |  ✓ | `state.json` `mode: core`; `mode_history` appended at the rollover |

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
| 1 | Each `R-NN` with its `AT` and the surface that produces it |  ✓ | 10 HLRs, each with `Acceptance test(s)`, AT-301..308; the AT table in §5 names the surface (`TaskboardApp` keys or `render_view`) |
| 2 | **Version per item** (`R-NN v3` · `AT-NNa v2`) |  ✓ | versions = 1 + ledger entries (`01-requirements-ledger.md` LED .1–.21); P2 folds .9–.16, P3 .17, P4 .18–.21 |
| 3 | Symbols cited with `file:line`, or flagged `NEW` |  ✓ | the LLRs name `views.py`/`app.py` symbols; new ones are flagged NEW (`kanban_plan`, `KanbanPlan`, `_literal`, …) |
| 4 | Premises executed (§2.7), each with its probe |  ✓ | §2.7, each premise with its executed probe (`evidence/p0-probes.txt`, `evidence/p1-geometry.txt`) |
| 5 | `shall`/`deberá` only inside statements |  ✓ | `shall` appears only in HLR/LLR statements; LLR-306.1's statement gained its `shall` at close (the canon fold refused it without one) |
| 6 | Each UX scenario with its observable criterion |  ✓ | every HLR/LLR carries a numeric pass threshold and a negative control |
| 7 | Cites by id the design record that originated it |  ✓ | §1.4 References: `prototypes/kg_mejoras/variants_kanban.k_a`, `variants_reconcile` R-1b, the approved frames `R-1b-118x30` / `R-1b-80x24`, `2026-10-02-batch-01` US-105 |
| 8 | Any premise resting on an **absence** flagged as load-bearing, with its synthetic instance (C-55) |  ✓ | load-bearing absences are flagged in the packets' C-55 tables, each with its synthetic instance |

⚠ a requirement rising in version without its `AT`/`TC` rising or being re-confirmed

## 4 · PDR — vault + Drive

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | Proposal complete (objective · modules · diagrams · interfaces · **proposed test cases** · risks · rejected alternatives **where a real decision exists**, otherwise `n/a — <the decision already made, and by what>`) |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 review stands in for it (`02-review.md`) |
| 2 | Respects the ARQ boundaries |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 review stands in for it (`02-review.md`) |
| 3 | **Forward applicability: every output has a NAMED consumer** |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 review stands in for it (`02-review.md`) |
| 4 | Proposed test cases observable and non-vacuous — **the reddening mutation named for each** |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 review stands in for it (`02-review.md`) |
| 5 | Interfaces **frozen** for the fork |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 review stands in for it (`02-review.md`) |
| 6 | UX lens applied (family D) · security lens applied (family C) |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 review stands in for it (`02-review.md`) |
| 7 | Verdict + record **sealed** (date · verdict · participants · approved ids) |  n/a — station not active in this batch | `core`: PDR is by trigger and `stations_active` holds none; the P2 review stands in for it (`02-review.md`) |

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
| 1 | **ONE complete run**, launched by the orchestrator — never stitched |  ✓ | `evidence/p4-gate3.txt`: one run by the orchestrator after increment 003, 1855 passed. Iteration 1: `evidence/p4-gate.txt` (1845). `p4-gate2.txt` failed 1 node on the environment's clipboard (G-011) |
| 2 | Layer 0 unit · layer A white-box · layer B black-box |  ✓ | `04-validation.md`: Layer 0 (9 units), Layer A (TC-301..313), Layer B (AT-301..308) |
| 3 | UX walkthrough with the **real mechanism** and the **painted** result |  ✓ | the ux-reviewer drove `App.run_test` with real keys and read the compositor strips and the scroll offset (`evidence/p4-ux-walkthrough.txt`, `evidence/p4-ux-rewalk.txt`) |
| 4 | Representative + **boundary** + **negative** |  ✓ | the Layer B rows in `04-validation.md` name the boundary and negative cases per AT |
| 5 | The deliverable actually **observed** |  ✓ | captures `evidence/captures/close-*` (6 frames × 3 panels, plus the app at 118×30, 120×32 and 80×24) beside `base-*` |
| 6 | Bidirectional surface-reachability matrix |  ✓ | `04-validation.md` §Surface-reachability: 0 gaps |
| 7 | **A NEGATIVE result names the over-breadth that makes it sound, and that over-breadth is guarded** (C-55 limb 1) |  ✓ | the packets' C-55 tables name the width: every span of the painted board at two terminal sizes, every row of the render; the 60 mode arms guarded by `test_TC_301_the_arm_set_is_complete` |
| 8 | **Every probe that returned an absence carries its POSITIVE CONTROL** — the same probe, unmodified, returning a non-absence on a known-present case |  ✓ | per packet: AT-305 reads the frame tone in the same spans (001); the reset lands on a counted card, Q13 RED (002); the same walk scrolls on the increment-002 tree, `inc003-red.txt` (003) |
| 9 | Verdict `PASS` / `PASS-WITH-NOTES` / `FAIL` declared as the keyed `**Result:**` field, ONE token — the whole batch-verdict vocabulary, and not the increment gate's `BLOCK` |  ✓ | `04-validation.md` `**Result:** PASS-WITH-NOTES` |
| 10 | **Evaluation with users (ISO 9241-210): the STATE, keyed to what happened** — `performed` / `not performed — <reason>` / `not applicable — no trigger-D surface`, for each of automated walkthrough, expert inspection and evaluation with users, kept apart |  ✓ | automated walkthrough: performed (ux-reviewer, P4 ×2). Expert inspection: performed (ux at P2 ×2; qa, code and security). Evaluation with users: not performed — one-person team, and no user of this surface exists outside it |
| 11 | `**Layer 0:**` and `**Evidence checklist (qa-reviewer):**` declared as keyed fields, the checklist naming WHO completed it |  ✓ | `04-validation.md` `**Layer 0:**` and `**Evidence checklist (qa-reviewer):**`: 11 of 11, named |

## 8 · CLOSE — repo + vault

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | `(item, version)` baseline sealed |  ✓ | `REQUIREMENTS.md` canon fold: 22 rows (10 HLR + 12 LLR), versions per `01-requirements-ledger.md`; HLR-003 and LLR-003.2 superseded |
| 2 | Backlog reconciled — the three moves |  ✓ | `05-close.md` §4. Closed: A2, ✓ done. Carried: the rest. Added: 20 items, including PV-1..PV-10, the UXV3 questions and G-002 ⏸ DEFER |
| 3 | C-44 reconciliation across **every** repo touched, auxiliary ones included |  ⚠ | one repo. This agent committed nothing; every change is in the working tree for the coordinator's commit (`05-close.md` §3) |
| 4 | Every artifact in its declared home, **no copies** |  ✓ | the batch record is under `.dev-flow/2026-10-02-batch-03/`, evidence under its `evidence/`; no copies |
| 5 | repo↔vault ids resolved in both directions |  n/a — no vault artifact this batch | `obsidian_synced: false`; nothing written to the vault |
| 6 | New controls pushed upstream (C-45): command · artifact · catalog · pushed |  ✓ | none minted (`05-close.md` §2) |
| 7 | Re-work counted per station |  ✓ | P2: 1 return (iterate-to-refine). P4: 1 return (iterate-to-refine + iterate-to-fix → increment 003). Code-review HIGHs: 001 ×1, 002 ×1, 003 ×2 |
| 8 | **What was NOT done, declared** |  ✓ | `05-close.md` §3–§4: the operator's verdicts on PV-1..PV-10, G-002's tighter nodes (deferred), room < 3 still scrolls (declared), evaluation with users, the commit (the coordinator's) |

⚠ any commit that exists and never landed · ⚠ a notice now in its third consecutive batch — make it a rule or retire it

## Re-work counter

| Station | Items that came back | From | Why |
|---|---|---|---|
| P2 | 1 loop (Q-1, Q-2 blockers; then N-1, UX-15 at iteration 2) | P2 iteration 1 | qa: an unreachable nav claim and the readability metric; ux: a fold row losing a count |
| P3 | 4 HIGH folded (001 F1; 002 F1; 003 F1, F2) | code-reviewer | a vacuous assertion; a selection reset bypassing the kanban rule; an exact fit cut; counts clipped |
| P4 | 1 loop → increment 003 | ux UXV3-1; qa G-001, G-003a, G-004 | a band taller than the room scrolled the head and the fold row away |

## Sign-off

- P0 · P1 · P2 · P3 · P4 · P5: self-approved by the agent under the standing authorization ("Autónomo, agente Opus"), each recorded in `state.json` `decisions_log`; 0 HIGH open. Flow pinned to rev98 by operator ruling ("Sí, fijar a rev98").
- Close privacy sweep: `evidence/privacy-sweep-close.txt`: entity-decoded, file names only (`evidence/sweep.py`), 179 files; 0 real-board strings. The two home-path hits are both inherited and present in HEAD: `state.json` `owner`, and a cloud-drive folder path in an older BACKLOG entry (BACKLOG S-5/L3).
