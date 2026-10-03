# Batch close — taskboard — Batch 2026-10-02-batch-03

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**,
> and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/docs/close-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Conditional-gate discharge` · `New controls` · `Human perimeter` · `Human review ledger` · `Gated tree` · `⏸ DEFER`
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
| Gate record | `cd <scratchpad>/devflow-rev98-48154ab/dev-flow && python scripts/devflow-validate.py <project>` (the PINNED rev98 bundle, skills `48154ab`, operator ruling "Sí, fijar a rev98") · exit 0 · **0 block** · 19 notice · 61 n/a · 2026-10-02 · `evidence/validator-close.txt`. Notices: 16 are inherited and declared in `PLAN.md` (V9 ×9, V13 batch-01 `nav-order`, V22 ×3, V23, V30, V53). This batch's own are three: V13 (its IFC address `kanban-grouped-body/card-rows` is computed, so grep cannot follow it; it is listed with batch-01's two in one notice); V26 size (the live contract is 62701 characters against a budget of 54000; the P2 and P4 amendments grew it, and moving the §6.5 narration into the ledger is left to the next batch's P1 rather than rewritten at close); V57 (the dirty tree, declared in the next row). The first close run had 1 block: V26 two-way, LLR-309.2 → LED .18, where the ledger entry did not name LLR-309.2. It was fixed in the ledger and the validator re-run |
| Gated tree | `13745f6f268f7f080141f9c0226b2441541dbff5` · dirty: every change is still in the working tree, waiting for the coordinator's commit (standing authorization; this agent does not commit). Files: `taskboard/views.py`, `taskboard/app.py`, `tests/test_kanban_readable.py` (new), `tests/kg_board.py`, `tests/test_app.py`, `tests/test_kanban_priority.py`, `tests/test_prism_laws.py`, `.gitattributes`, `REQUIREMENTS.md`, `.dev-flow/state.json`, `.dev-flow/BACKLOG.md`, `.dev-flow/2026-10-02-batch-02/decisions-log.json` (new), `.dev-flow/2026-10-02-batch-03/**` (new) |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`), folded with the pinned `devflow-init.py --fold-canon`. First run: 21 folded (10 HLR + 11 LLR), 1 refused, because LLR-306.1's statement had no `shall`. The statement was reworded with no change of meaning; the second run folded LLR-306.1 (1 folded, 21 kept, 0 refused). HLR-003 and LLR-003.2 are marked `superseded by …` (D-301, D-313) |

---

## 1 · What changed

**The grouped kanban (key `4`) is now readable.** Every changed design point below has its decision id.

- **Cards and widths.** Each card takes two rows: the title runs across the column and the facts sit on a quiet second row. Stacked cards are separated by `┈`. Column widths follow the frames' proportional rule.
- **Project bands.** Each project is named once, by a band rule across all the columns. The rule shows the project's colour bar, its open count and its due fact.
- **Finished work.** It moves to a DONE rail: titled at 100 cells and wider, a `✓N` count below that.
- **Urgent work.** It rides one board-wide high band on top. The band is capped at two thirds of the body, and a `+N more ↓` row counts the cards that do not fit.
- **Bands that do not fit.** They fold into one row that names them (`▲ N above … ▼ M below: NAME (k open)`). A band taller than the room is cut around the selected card and its hidden cards are counted (`▲ k more in NAME`). The board is never taller than the panel, and the selected card is always whole.
- **Colour.** Accent marks only the focused card and today. Due dates within 7 days are amber. The selection is in reverse video.
- **Help and legend.** Both describe the new board.
- **After `]`.** The cursor moves to the card that took the moved one's place, and a notice says where the task went.
- **Coexist or replace (commission item 9).** The new board **replaces** the old grouped body (D-301). `tab` still cycles grouped → matrix → lanes.

**Readability:** oracle board, measured on the panel's body rows at scroll 0, with a title counted only when its whole first word is drawn (`evidence/captures/readability-*.txt`).

| Panel | Base (`13745f6`) avg visible title chars · full titles | Close avg · full | Threshold |
|---|---|---|---|
| 118×30 | 7.3 · 0 | **11.8 · 13** | ≥ 11.0 · ≥ 12 |
| 80×24 | 1.0 · 0 | **6.2 · 3** | ≥ 5.5 |
| 80×22 | — | 6.2 · 3 | — |

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-301 | v3 | AT-301 · TC-302, TC-303 | pass |
| HLR-302 | v2 | AT-301 · TC-304, TC-305 | pass |
| HLR-303 | v3 | AT-302 · TC-306 | pass |
| HLR-304 | v3 | AT-302 · TC-307 | pass |
| HLR-305 | v3 | AT-303 · TC-308, TC-301 | pass |
| HLR-306 | v3 | AT-304 · TC-309 | pass |
| HLR-307 | v2 | AT-305 | pass |
| HLR-308 | v2 | AT-306 · TC-310 | pass |
| HLR-309 | v4 | AT-307 · TC-311 | pass |
| HLR-310 | v3 | AT-308 · TC-312 | pass |

- **Versions.** Each version is 1 plus the item's entries in `01-requirements-ledger.md` (LED .1–.21).
- **LLRs.** The 12 LLRs pass with their parents (`04-validation.md` iteration 2, PASS-WITH-NOTES).
- **P4 amendment.** HLR-309 was amended at P4 (LED .18 and .21): the cut replaces the scroll.
- **Executed verification.** Every requirement's *Executed verification* selector collects at least one node (`evidence/p4-selectors.txt`).

| Increment | SOURCE files | Tests (suite after) | Code review | Mutants |
|---|---|---|---|---|
| 001: the readable board | `views.py` | 1821 passed | 2 rounds. Round 1 BLOCK-UNTIL F1 (HIGH: a vacuous UX-15 assertion), folded; round 2 OK | 28/28 KILLED |
| 002: the cap, the copy, the cursor | `views.py`, `app.py` | 1845 passed | 2 rounds. Round 1 BLOCK-UNTIL F1 (HIGH: a selection reset bypassed the kanban rule), folded; round 2 OK. Security PASS-WITH-NOTES | 15/15 KILLED |
| 003: the cut (P4 iterate-to-fix) | `views.py` | 1854 passed + the clipboard environment failure | 3 rounds. Round 1 BLOCK-UNTIL F1, F2 (HIGH: an exact fit was cut; counts were clipped), folded with RED proof; rounds 2 and 3 OK | 12/12 KILLED |

**Final gate run:** **1855 passed**, 0 failed (`evidence/p4-gate3.txt`; the clipboard node also passed alone).

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| none | — | — |

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a — no control minted | — |
| 2 | its **artifact** (a template section) | n/a — no control minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | n/a — no control minted | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a — no control minted | — |

- **New controls:** none — every failure in this batch was caught by an existing control:
  - **C-40 mutation per arm.** It found a survivor in each increment (C3 and C5 in increment 003), and each survivor became a new arm.
  - **The code-review freeze rule.** It caught four HIGHs: a vacuous assertion, a reset that bypassed the kanban rule, an exact-fit cut, and clipped counts.
  - **C-21 re-cut.** It ran when AT-307 and AT-308 arrived at P2.
  - **The ux-reviewer's P4 walk through the real app.** It found UXV3-1 (a tall band scrolled the head and the fold row away), which every render-level node had passed.
- **Lesson for the flow owner (not minted):** a test written against `render_view` cannot see the app's scroll. An acceptance node for a windowed view needs a `run_test` arm that reads `scroll_offset`. AT-307 now has one.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| every file in §0 *Gated tree* | 📋 ready to commit. The coordinator commits and pushes to `main` without a PR, after the operator's visual verdict (standing authorization, `merge: false`); this agent does not | `git status --short` |
| `~/.claude/skills/dev-flow/**` | 📋 not this batch's; never edited here (operator ruling, flow pinned to rev98) | `PLAN.md` header "Flow pin" |
| scratch copies, mutation trees, the pinned rev98 snapshot, the reviewers' probes | 🗑️ outside the repo (session scratchpad). The harness sources are kept in `evidence/mutate.py`, `evidence/capture.py` and `evidence/sweep.py` | `evidence/inc00*-mutations*.txt` |

- **G-005, from the P4 qa review, is discharged here:**
  - (a) iteration 1's `p4-gate.txt` has no header. Its digest is in `04-validation.md`. The final gate `p4-gate3.txt` names its command through this record.
  - (b) every `captures/base-*`, `inc001-*` and `close-*` file comes from `evidence/capture.py` (`python <file> OUT_DIR LABEL`, run in the captured tree). The base set is of the base tree `13745f6`; the close set was re-taken on the final tree (G-009).
  - (c) `.gitattributes` gets one line, `.dev-flow/2026-10-02-batch-03/evidence/** -text`, following the earlier batches' pattern, and is listed in §0.

### Conditional-gate discharge

- **Conditional-gate discharge:** 8 condition(s) · ✅ all discharged

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| qa-reviewer P2 FAIL iteration 1 (Q-1, Q-2) | ✅ | `02-review.md` §Iteration 2; LED .9–.13 |
| qa / ux P2 FAIL iteration 2 (N-1, UX-15) | ✅ | `02-review.md` §Iteration 2 discharge re-read: DISCHARGED 12/12 |
| code-reviewer BLOCK-UNTIL F1 (increment 001) | ✅ | `03-increments/increment-001.md` §4b round 2 OK |
| code-reviewer BLOCK-UNTIL F1 (increment 002) | ✅ | `03-increments/increment-002.md` §4b round 2 OK |
| code-reviewer BLOCK-UNTIL F1, F2 (increment 003) | ✅ | `03-increments/increment-003.md` §4b rounds 2–3 OK; F1/F2a/F2b KILLED in `evidence/inc003-mutations-r2.txt` |
| ux-reviewer P4 FAIL UXV3-1 (blocker) | ✅ | `evidence/p4-ux-rewalk.txt`: PASS-WITH-NOTES, 0 bad steps over 8 walks |
| qa-reviewer P4 G-006, G-009..G-012 | ✅ | `04-validation.md` §Orchestrator fold; G-002 is ⏸ DEFER to BACKLOG |
| the clipboard node failed in the gate run (G-011) | ✅ | `evidence/p4-gate3.txt`: 1855 passed |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| Batch A2: readable kanban K-A + R-1b | shipped (uncommitted) | increments 001–003; BACKLOG entry marked ✓ done |
| The operator's verdicts on PV-1..PV-10. Operator questions: the high-band cap at a cut band (UXV3-12), `up` re-flow (UXV3-3), lateral moves (UXV3-5), `at risk` (UXV3-2), the entry cursor (UXV3-9), `done today` (UXV3-8), the help at 80×24 (UXV3-4), the no-match copy and `z` (UXV3-10/11), the fold row at 80 (UXV3-13), band counts vs fold counts (UXV3-14), the toast over the fold row (UXV3-15). Also: `collapse_runs` S-2, the gantt's nav height under `/`, `_phase_window` reuse, done work past the rail, horizon `Done (0 open)`, the detail line, the AT-307 transient, and ⏸ DEFER G-002 (four threshold clauses asserted weaker than written) | added | `.dev-flow/BACKLOG.md` §Open — after `2026-10-02-batch-03` (20 items) |
| Everything else in BACKLOG | carried | `.dev-flow/BACKLOG.md` |
| Header refresh | done: 1855 tests, base `13745f6`. The base ref moves when the coordinator commits | `.dev-flow/BACKLOG.md` header |

---

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-02-batch-03
mode: core
verdict: pass
increments: 3
source_files_max: 2
notices_raised: 19
rework_returns: 2
triggers_fired: "B1,B4,C,D,E,F2"
tests_base_to_post: "1677 -> 1855"
new_control: none
open_items_next: 20
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` | P2 qa / ux PASS-WITH-NOTES at iteration 2; security PASS-WITH-NOTES (`02-review.md`) | ❌ | `none` | the operator has not reviewed it yet; this batch ends at his visual verdict and the coordinator's commit |
| Code (2 source files) | code-reviewer OK on every increment (3 increments, 7 rounds) · mutants 28, 15, 12 KILLED | ❌ | `none` | as above |
| Tests / ATs | `04-validation.md` iteration 2 PASS-WITH-NOTES; C-18 8 ATs = 8 nodes; ledger 1855 | ❌ | `none` | as above |
| Captures (`evidence/captures/close-*` beside `base-*`) | ux-reviewer P4 re-walk PASS-WITH-NOTES | ❌ | `none` | as above |

- **Human perimeter:** the operator (Javier) owns:
  - the visual verdict on the close captures at 118×30 and 80×24 against the base ones
  - the provisional visual decisions PV-1..PV-10 (`PLAN.md` §Provisional visual decisions, with capture names)
  - the operator questions now in BACKLOG
  - the commit itself
- **Human review ledger:** none — no human has reviewed this batch yet; it ran autonomously under "Autónomo, agente Opus" and ends at the coordinator's commit.
