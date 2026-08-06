# PLAN — 2026-08-03-batch-03 (living compendium)

**Where we are:** Phase 0, awaiting gate. Promoted from `/fast-dev-flow` by operator decision.

**Base ref:** `f237cb3` — **RC-1 PASS**, executed: `HEAD == origin/main == f237cb3`, merge-base
identical. Derivation runs against a current tree.

**Flow revision:** `2026.07.28-rev1`. **PULL executed**: 11 of 12 flow files hash-match the
manifest byte-for-byte. The twelfth, `dev-flow-lessons/SKILL.md`, is 641 lines against the 620
recorded — because **C-46 landed in `f3d4fba` and is already pushed, and nobody bumped
`FLOW-VERSION.md`**. I am not behind; the manifest is. Carried as a process item.

---

## Objective

In the **lanes** view:

1. the project row states, in text, **what the project asks of you now** — open count, overdue
   count, next due distance (mechanism **D**);
2. the **cumulative load curve** (`wave.load_curve`, mechanism **A**) moves out of the project row
   and into a **disclosure row that appears only while a task is selected**;
3. that row is paid for by the **focused project shedding one title** (option **(a)**, operator-
   decided at the fast-flow Phase-A gate).

## Why this was promoted

Not a visual swap. `allocate()` searches over `(titles, lead rows, wave rows)`, `swimlane_plan()`
returns that triple, and `stack_block()` spends it — **39 coupled call sites** across app and tests.
Lanes **never pads** (measured: 0 blank rows at h=30/45/60), so the height is spent exactly and the
row budget moves with the change. The escape hatch fired on "layout engine", not on ambiguity.

## Stories (Phase 0 intake)

| id | story | INVEST notes | status |
|---|---|---|---|
| **US-A** | As the board's owner **operating** the board, I want each project row to tell me open count, overdue count and next deadline, so I can triage without decoding a mark. | Independent ✓ · Negotiable ✓ · Valuable ✓ · Estimable ✓ · Small ✓ · Testable ✓ (observable in the rendered row) | **READY** |
| **US-B** | As the board's owner **stopping on a project**, I want its load curve where I am already looking, so the shape answers a question I just asked instead of decorating a row I scroll past. | Independent ✗ — **depends on US-A** for its row budget · rest ✓ · Testable ✓ (curve present iff selected) | **READY** (ordered after US-A) |

**Out of scope, explicitly:** the gantt (its prototype work is a separate batch); any new visual
language (Ledger/Darkside/Naught stay uncommitted prototypes); deleting `wave.py` or `load_curve`
— **the curve moves, it does not die**; the lanes geometry off-by-one (`today_cell` 44 vs rule at
column 43), which stays in the backlog.

## Premises carried from the promoted fast-flow spec (C-43)

| # | premise | tier | verdict | executed evidence |
|---|---|---|---|---|
| P1 | Removing the wave breaks the occupancy floor | Hypothesis | ❌ **FALSE** | `test_occupancy.census`: marked **72.3 / 80.9 / 83.8 %** vs floor **45 %**; wave = **114 cells, 4.0 %** of 96×30 |
| P2 | The disclosure row costs a reflow per keypress | Hypothesis | ❌ **FALSE** | marginal cost of one row **−0.17 ms** (4.51→4.34 ms). `refresh_view()` already repaints the whole view every keypress |
| P4 | The allocator's doctrine supports the change | Premise | ✅ TRUE | `allocate()` docstring: *"a named task outranks a taller curve on a mission-control surface"* |
| P5 | `load_curve` is callable outside the lane machinery | Premise | ✅ TRUE | `wave.load_curve(bm, steps, total, edge)`; `views.py:986` is its only caller |
| P6 | The legend describes the wave today | Premise | ❌ **FALSE** | Swept every `out.append` in `legend_entries`: the swimlanes branch names spine, lattice, today rule, due diamond, status marks, phase glyphs, `!N` — **never the wave**. So AC "legend" **ADDS** an entry; it does not move one. |

**P6 is the finding that explains the request.** The operator said *"I am not certain what they
do"* about a mark the app draws and its own legend has never described. The ghost-mark law did not
catch it because that law checks that every legend entry is drawn — **not that every drawn mark is
explained**. That asymmetry is itself a candidate control.

## Risks / watch-items

1. **The row budget is the whole batch.** `allocate()`'s search dimension `wrows` loses its
   consumer in the project row and gains one in the disclosure row. Getting this wrong does not
   look like a bug — it looks like a view that pads or overflows.
2. **Reverse census (C-26) owed** on every touched symbol: `wrows`, `project_wave`, `field_rows`,
   `stack_block`, `_figures`. 39 sites is the forward count; the reverse grep across `tests/` is
   not yet run.
3. **`_figures`' docstring is a live claim that this batch falsifies** — *"the project's own wave
   already draws its progress"* was the stated reason `n/N` was removed. Removing the wave makes
   that reason false; the docstring must be amended, not left lying.
4. **Occupancy re-measure is owed** even though P1 came back false — 27-38 points of headroom is a
   margin, not a proof for the post-change tree.

## Conventions honored

`language: en` · normative `shall` only inside HLR/LLR · dual traceability (`AT-NNN` black-box +
`TC-NNN` white-box) · ≤5 files per increment · review packet per increment · `security_required:
false` (no pattern matched).

## Decision log

| date | decision | notes |
|---|---|---|
| 2026-08-03 | Mechanism **D** in the row, **A** on disclosure | Operator, after seeing A/C/D rendered on real data. C was rejected as answering the least actionable question. |
| 2026-08-03 | Row budget paid by **(a)** the focused project shedding a title | Operator. (b) reserves a row even unselected — the waste this batch removes; (c) hides a real row. |
| 2026-08-03 | **Promote** to `/dev-flow` | Operator, after the layout-engine scope was measured. |
| 2026-08-03 | **O-1: silent refusal** | When `titles==1` the only title IS the selection; shedding unnames the cursor's own row. Operator ruled refuse silently — US-B does not fire there. Not reachable on the operator's real board (titles 8/6/17). |
| 2026-08-03 | **O-2: supersede `test_spend.py:277`** | Retiring `wrows` sends the surplus to the lead's bench (`prof` 8→19 @96×30, 10→33 @96×44, executed). Operator ruled supersede: the law's premise — a 1-row stack lane is *starved* — stops holding once that is the lane's designed form. |
| 2026-08-03 | Phase 1 approved with a named Evidence gap | LLR-003.5's mutation is not runnable on current fixtures (`open == total` everywhere). Phase 3 owes the fixture. |
| 2026-08-03 | **Orchestrator error** | PLAN claimed `views.py:986` was `load_curve`'s only caller. FALSE — `report.py:137` is a second one. My grep swept only `views.py`. |
| 2026-08-03 | `state.json` reconciled | It still described `2026-07-31-batch-02` at phase 0; that batch closed via fast-flow. |

## Batch-kickoff authorization (answered 2026-08-03)

Asked at Phase 0, per-batch, never carried from a prior batch.

- **Autonomy / merge:** *"Yo apruebo cada gate; yo hago el merge."* The operator approves **every**
  gate. **No merge authority granted** — this batch stops at *"PR opened, CI green"* and the
  operator merges. No self-approval of any gate.
- **Decision recording:** *"En los cuatro sitios."* Every decision taken without asking is recorded
  in this PLAN's decision log, `state.json.decisions_log`, `05-postmortem.md`, and carried to the
  vault at `/dev-flow-sync`.
