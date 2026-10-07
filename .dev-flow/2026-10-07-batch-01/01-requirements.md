# Requirements Document — taskboard — Batch 2026-10-07-batch-01

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/req-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Validation` · `Acceptance test(s)` · `Boundary catalog` · `Negative control` · `Premise evaluation` · `Fork preconditions` · `Ledger` · `Requirement` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

---

## 1. Introduction

### 1.1 Purpose
*(Informative text. Describes the document's objective.)*

### 1.2 Scope
*(What this batch covers and what it does NOT cover.)*

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| | |

### 1.4 References
*(Related documents, standards, external tickets.)*

### 1.5 Document overview
*(How this document is structured.)*

---

## 2. Overall description

### 2.1 Product perspective
*(How the change fits into the larger system.)*

### 2.2 Product functions
*(High-level list of functional capabilities.)*

### 2.3 User characteristics
*(Roles, permissions, expected experience levels.)*

### 2.4 Constraints
*(Technological, regulatory, business.)*

### 2.5 Assumptions and dependencies
*(What we take for granted. If an assumption fails, the batch is invalidated.)*

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-701 | As the maintainer, I want the P4 residue closed — one restore rule, one today-base rule, the totals documented, the C-5 arm and the narrow-width toast rungs pinned — so that the shipped cascade cannot silently drift from its tested primitives. | P4 findings DS-5, ARCH4-3/4, SEC4-3/6, GAP-3 of batch 2026-10-06-batch-01 (`.dev-flow/2026-10-06-batch-01/04-validation.md`) | READY |

**US-701 — refinement:** INVEST all ✓ (the five items are named, severitized and behavior-specified by the P4 findings; the refactor is behavior-preserving by definition, its oracle the 2512-test suite at `f665425`). Classification: READY.

#### Refinement log (one block per story)

**US-001 — `<short title>`**
- **INVEST:** I · N · V · E · S · T  (mark ✓/✗ each)
- **Functionality (V, N):** user = … · outcome = … · why = … · out of scope = …
- **Feasibility (E, S):** implementation path = … · dependencies/unknowns = … · fits one batch? = yes/no (split or spike if no)
- **Evaluability (T) — behavioral, black-box:** ≥1 observable acceptance criterion at the behavior level = "When `<input>`, the user observes `<outcome through the shipped surface>`" (becomes an `AT-NNN` in Phase 1). A story phrased as a mechanism (implementation spec) is mis-captured → REFINE.
- **Open questions:** …
- **Classification:** `READY` / `REFINE` / `SPIKE` / `OUT` — `<reason / next action>`

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| `<one row per premise this batch relies on>` | | | | | |

- **Premise evaluation:** `<the table's roll-up: N premise(s) · ✅ TRUE / ❌ FALSE / ❓ UNDECIDABLE — or: none — this batch relies on no premise>`

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

| # | Condition (`C-52`) | Discharged? | The executed evidence |
|---|---|---|---|
| 1 | **Frozen contract** — no shared interface is touched inside a lane; one that must change returns to the trunk (trigger A3) | ✅ \| ❌ \| ❓ | `<the interface list and where it is frozen>` |
| 2 | **Disjoint FILE sets**, not just modules — two lanes may not edit the same file, not even different regions | ✅ \| ❌ \| ❓ | `<the per-lane file sets and the intersection test>` |
| 3 | **Crossed reverse census** — family B run per lane and **shared before starting**; the trunk's act, impossible from inside a lane | ✅ \| ❌ \| ❓ | `<the per-lane symbol sets, the cross-grep and its output>` |
| 4 | **One owner of the trunk** — requirements, traceability, backlog and spec are never written from a lane | ✅ \| ❌ \| ❓ | `<who owns the trunk>` |

- **Fork preconditions:** `<N lane(s) · the four conditions, each with its verdict — or: none — this batch runs one lane>`

---

## 3. High-level requirements (HLR)

### HLR-701 — The P4 residue is closed without drift
- **Traceability:** US-701
- **Ledger:** LED-2026-10-07-batch-01.1
- **Statement:** The system shall carry ONE restore rule (the tested `models.restore`, used by every restore site), ONE undated-date base rule (shared by `bump_due` and `plan_move`), the `Plan.conflicts` totals documented as the tested intermediate, the C-5 vanished-task refusal pinned by a synthetic test, and the toast ladder's narrow-width degradation (≤ the width at 80/60/40/24, non-empty at 24) pinned by test — with the full 2512-node suite green and byte-identical behavior throughout.
- **Rationale (informative):** P4 found no defect; it found five places where the shipped code and its tested primitives could silently drift apart.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests -q` (env: NO_COLOR unset, TERM=xterm-256color, COLORTERM=truecolor, PYTHONIOENCODING=utf-8)
- **Numeric pass threshold:** 2512 + 2 nodes, 0 failures other than the declared G-011 flake.
- **Priority:** medium
- **Acceptance (black-box):**
  - **Observable outcome:** the maintainer reads one restore loop, one base rule, and sees the two pins go red if anyone re-introduces the drift.
  - **Shipped surface:** `taskboard/models.py`, `taskboard/app.py`, the suite.
  - **Acceptance test(s):** TC-701, TC-702 (TC-703: the refactor's oracle is the whole suite — a behavior change reddens it)
  - **Boundary catalog:** ⑆ none — no input class changes
  - **Negative control:** TC-701 goes RED if the C-5 gate is removed (the refusal never fires and `m` re-applies a move whose task is gone)

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-701.1 — One restore rule, one base rule, the totals documented
- **Traceability:** HLR-701
- **Ledger:** LED-2026-10-07-batch-01.1
- **Statement:** `models.py` shall provide one module-level date-base rule used by both `bump_due` and `plan_move`'s undated branch; every date-restore site in `app.py` shall call the tested `models.restore` (the skip-vanished semantics stay in the model); `Plan.conflicts` shall document itself as the after-state totals, the tested intermediate (TC-629), with production reading `new_conflicts`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests -q`
- **Numeric pass threshold:** 2512 nodes green, byte-identical behavior (the refactor touches no test).
- **Negative control:** the suite itself — any behavior change reddens it.
- **Boundary catalog:** none.

### LLR-701.2 — The C-5 arm pinned
- **Traceability:** HLR-701
- **Ledger:** LED-2026-10-07-batch-01.1
- **Statement:** `m` shall refuse — the verbatim toast, writing nothing — when the undo stack's top cascade entry names a moved task that no longer exists (LLR-604.4's error arm), pinned by a synthetic test (the UI cannot reach the state: a delete evicts the entry).
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_cascade_app.py -q -k TC_701`
- **Numeric pass threshold:** 1 node green; RED if the gate is removed.
- **Negative control:** TC-701 itself.
- **Boundary catalog:** ⑆ error (the vanished moved task).

### LLR-701.3 — The narrow-width toast rungs pinned
- **Traceability:** HLR-701
- **Ledger:** LED-2026-10-07-batch-01.1
- **Statement:** the C-3 toast shall fit its width at 80, 60, 40 and 24 columns and stay non-empty at 24 — the degrade-by-design the ladder's contract implies below the pinned 118/80 arms.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_cascade_app.py -q -k TC_702`
- **Numeric pass threshold:** `vis(text) <= width` at each width; non-empty at 24.
- **Negative control:** the assertion itself — a rung that overflows reddens it.
- **Boundary catalog:** ⑆ boundary (the four widths).

### Information Flow Contract (IFC)

Part A (no new information flow exists in a behavior-preserving cleanup; the one touched flow,
named so its nodes stay owned):

```
FLOW: the undo entry's dates, restored through the one tested rule
  SOURCE : the undo stack's cascade entries (the user's keys and the editor, batches prior)
  NODES  :
    - fn    : models.restore (the one restore rule) / its two app.py call sites
      owner : LLR-701.1
    - fn    : models.date_base (the one undated-date base) / bump_due / plan_move
      owner : LLR-701.1
  SINK   : the restored task dates, the saved board file
```

Part B: `no — no new addressable component.`

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

### 5.2 Batch acceptance criteria
- *(e.g.: 100% of LLRs covered by at least one TC with pass result.)*
- *(e.g.: 0 blocker fails in validation.)*
- *(e.g.: test coverage >= X% where applicable.)*
- *(e.g.: no requirement without an assigned validation method.)*
- *(e.g.: every user story has ≥1 passing `AT-NNN` black-box acceptance test observing its outcome through the shipped surface — with boundary + negative evidence.)*

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
### 6.3 Open risks
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-07-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
