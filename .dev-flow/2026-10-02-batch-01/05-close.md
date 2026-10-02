# Batch close — taskboard — Batch 2026-10-02-batch-01

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
| Gate record | `cd <home>/.claude/skills/dev-flow && PYTHONUTF8=1 python scripts/devflow-validate.py <project>` · exit 0 · **0 block** · 17 notice · 61 n/a · 2026-10-02 · `evidence/validator-close.txt`. Notices: V9 ×8, V22 (canon US), V23, V30 inherited from the base record; V26 contract over budget (declared at P2); V13, V22 (LLR owner), V53 census counts; V57 the dirty tree, declared in the next row |
| Gated tree | `57a60756fda953bdde5d26c64bcf0eec202f44c8` · dirty — every change is in the working tree for the coordinator's commit (standing authorization: this agent does not commit): `taskboard/views.py`, `taskboard/app.py`, `taskboard/modals.py`, `tests/kg_board.py`, `tests/test_gantt_board.py`, `tests/test_colour_budget.py`, `tests/test_readme.py`, `tests/test_gantt.py`, `tests/test_app.py`, `tests/test_archive.py`, `tests/test_dependencies.py`, `tests/test_motion.py`, `tests/test_spend.py`, `tests/test_vertical_fill.py`, `tests/test_requirements.py`, `tests/test_cells.py`, `README.md`, `RUN.md`, `docs/taskboard-gantt.svg`, `.gitattributes`, `REQUIREMENTS.md`, `.dev-flow/state.json`, `.dev-flow/BACKLOG.md`, `.dev-flow/2026-09-30-batch-01/decisions-log.json`, `.dev-flow/2026-10-02-batch-01/**` |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`), folded with `devflow-init.py --fold-canon`: 30 folded, 0 kept, 0 refused |

---

## 1 · What changed

The gantt shows the whole board on a window fitted to the open work: every project is present,
and the ones that do not fit are folded to one row instead of disappearing behind "+N not shown".
A two-row date ruler stays at the top. Its month and day labels never collide, and it echoes the
selected task's start and due. The cursor walks exactly what is drawn. On the kanban and the
gantt the accent colour now means only the edit field and today: titles are bold bright, and
the critical chain is drawn as structure (bold `━`). The README and RUN.md describe the app as it
ships, with no personal path.

Mechanism: one fold plan (`gantt_plan`) feeds both the renderer and the navigation, so draw order
and nav order cannot drift apart. The axis picks a scale k ∈ {½, 1, 2, 3, 7} days per cell. The ruler
cadence (Mondays / 1st & 15th / 1st / daily) follows that scale. The help and the legend read the
same frame the panel paints.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-101 | v5 | AT-101, AT-109, AT-110, AT-111 · its LLRs' TCs (`04-validation.md` Layer A) | pass |
| HLR-102 | v3 | AT-101 · its LLRs' TCs (`04-validation.md` Layer A) | pass |
| HLR-103 | v3 | AT-103 · its LLRs' TCs (`04-validation.md` Layer A) | pass |
| HLR-104 | v6 | AT-102, AT-108, AT-113 · its LLRs' TCs (`04-validation.md` Layer A) | pass |
| HLR-105 | v4 | AT-104, AT-112 · its LLRs' TCs (`04-validation.md` Layer A) | pass |
| HLR-106 | v3 | AT-104 (the no-drop law) · its LLRs' TCs (`04-validation.md` Layer A) | pass |
| HLR-107 | v3 | AT-105 · its LLRs' TCs (`04-validation.md` Layer A) | pass |
| HLR-108 | v3 | AT-106 · its LLRs' TCs (`04-validation.md` Layer A) | pass |
| HLR-109 | v3 | AT-107 · its LLRs' TCs (`04-validation.md` Layer A) | pass |

Version = 1 + the item's entries in `01-requirements-ledger.md` (LED .1–.31). The 21 LLRs pass with their parents (`04-validation.md`: 30/30, 0 blocker fails); LLR-101.7,
LLR-101.10 and LLR-102.5 were amended at P4 (LED .29–.31).

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

- **New controls:** none — every finding this batch was caught by an existing control: C-18 (AT one node), C-40 (mutation RED proofs), C-55 (positive controls), V56 (cited counts), and the P4 walkthrough. None of these failures needed a new rule.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| every file in §0 *Gated tree* | 📋 ready to commit — the coordinator commits and pushes to `main` without a PR (standing authorization, `merge: false`); this agent does not | `git status --short` |
| `docs/taskboard-gantt.svg` | 📋 untracked and new; the README's hero image. It MUST be in the commit (qa G-005; verify with `git ls-files docs/taskboard-gantt.svg`) | `04-validation.md` G-005 |
| `docs/taskboard-gantt.png` | 📋 left on purpose — orphaned: the README no longer links it; delete or keep is the operator's call | `.dev-flow/BACKLOG.md` (screenshots item) |
| scratch copies and mutation harness runs | 🗑️ outside the repo (session scratchpad); harness sources kept in `evidence/mutate_inc00{1,2,4}.py` | `evidence/inc00*-mutations.txt` |

### Conditional-gate discharge

- **Conditional-gate discharge:** 3 condition(s) · ✅ all discharged

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| code-reviewer BLOCK-UNTIL F1/F3 (increment 001) | ✅ | `03-increments/increment-001.md` §4b rounds 2–3 OK; RED in `evidence/inc001-review-red.txt` |
| code-reviewer BLOCK-UNTIL F1 (increment 002) | ✅ | `03-increments/increment-002.md` §4b round 2 OK; RED in `evidence/inc002-review-red.txt` |
| qa-reviewer P4 FAIL (G-008, G-009, G-010) | ✅ | `04-validation.md` iteration 3 `**Result:** PASS-WITH-NOTES`, G-008/009/010 closed |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| gantt G-A, AX-2 ruler, month band dropped, rows shed at short heights | shipped (uncommitted) | increments 001, 004; BACKLOG items marked ✓ done in `2026-10-02-batch-01` |
| colour budget on kanban and gantt | shipped (uncommitted) | increments 001, 002 |
| README / RUN.md rewrite (standing request 2026-09-30) | shipped (uncommitted) | increment 003 |
| Batch A2 (K-A + R-1b) | carried — pre-authorized split | `.dev-flow/BACKLOG.md` §Open — after `2026-10-02-batch-01` |
| app-wide colour budget, operator questions D4, D9, D10, D12, D13, D14, UXV-2, UXV-3, weekend shading | carried | same section |
| UXV-7, UXV-9, `_strip` F5, panels < 3 rows, help right column, Setup sync interval, README audit #4/#10, outdated screenshots, S-8, S-5 | carried | same section |
| UXV-12 not re-walked; inherited personal strings in state/BACKLOG | added at close | same section |
| header refresh | done — 1611 tests, base `57a6075`; the base ref moves when the coordinator commits | `.dev-flow/BACKLOG.md` header |

---

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-02-batch-01
mode: core
verdict: pass
increments: 4
source_files_max: 3
notices_raised: 17
rework_returns: 2
triggers_fired: "B1,B4,C,D,E,F2"
tests_base_to_post: "1535 -> 1611"
new_control: none
open_items_next: 17
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` | P2 qa / ux / security PASS-WITH-NOTES (`02-review.md`) | ❌ | `none` | the operator has not reviewed yet; this batch ends at his commit gate |
| Code (`views.py`, `app.py`, `modals.py`) | code-reviewer OK per increment · mutants 18/18, 6/6, 5/5 KILLED | ❌ | `none` | as above |
| Tests / ATs | `04-validation.md` 30/30, C-18 ✓, ledger 1611 | ❌ | `none` | as above |
| README.md, RUN.md | qa PASS-WITH-NOTES, security PASS-WITH-NOTES | ❌ | `none` | as above |
| Captures (`evidence/captures/close-*`) | ux re-check pass (UXV-1/5/6), UXV-12 fixed | ❌ | `none` | as above |

- **Human perimeter:** the operator (Javier) owns: the visual verdict on the close captures at 118×30 and 80×24; the operator questions in BACKLOG (D4, D9, D10, D12, D13, D14, UXV-2, UXV-3, weekend shading); whether to scrub the inherited personal strings; the commit itself.
- **Human review ledger:** none — no human has reviewed this batch yet; it ran autonomously under "Autónomo, agente Opus" and ends at the coordinator's commit.
