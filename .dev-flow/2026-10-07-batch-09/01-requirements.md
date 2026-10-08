# Requirements Document — taskboard — Batch 2026-10-07-batch-09

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
| US-1501 | As the operator, I want to author a template from scratch in the app (name + tasks, one per line), so that I can define a process before any task of it exists. | operator follow-up 2026-10-08 | READY |

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
| P-1 | The v1 store + the `I` picker + the batch-08 save all ship and green — scratch authoring reuses the store/picker seats and the same save/toast contract | base behavior | TRUE | `git show 979cf59 --stat` + the green suite | HLR-1501 composes them |

- **Premise evaluation:** 1 premise(s) · ✅ TRUE

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — one lane on the main checkout.

---

## 3. High-level requirements (HLR)

### HLR-1501 — Author a template from scratch in the app
- **Traceability:** US-1501
- **Ledger:** LED-2026-10-07-batch-09.1
- **Statement:** The `I` picker shall carry a first entry `New template...` that opens a small editor: ONE field for the name and ONE multi-line field for the tasks — one task per line, order = the chain (each task waits on the previous, a linear chain; empty lines skipped; leading/trailing whitespace trimmed; the shape holds one link per task, same as the batch-08 save); Save appends `{"name", "tasks": [{"title", "wait"}]}` to `settings["templates"]`, saves the board, toasts `Template '<name>' saved — <N> tasks` (`markup=False`, the batch-08 literal); an all-empty edit (no name or no tasks) saves NOTHING and says why in one line; esc cancels with nothing written; the new template lists in the `I` picker immediately and inserts with `I` like any other; authoring is NOT an undo step (settings, not tasks — declared, the batch-08 rule); notes are not editable here (v1 of scratch authoring — the JSON remains the full editor, the `?` says so).
- **Rationale (informative):** the operator's follow-up 2026-10-08: "No puedo hacer una plantilla desde cero tambien?" — saving an existing chain covers reuse of real work; scratch authoring covers the blank page.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_template_new.py -q` (the increment's file)
- **Numeric pass threshold:** `0 failures`; the arms: the picker lists `New template...` first; the editor saves a linear chain (each `wait` = previous index, empty lines skipped); the toast equals the pinned literal; all-empty saves nothing; esc writes nothing; the saved template inserts with `I` and reproduces the chain.
- **Priority:** medium
- **Acceptance (black-box):**
  - **Observable outcome:** open `I`, choose `New template...`, type a name and the tasks one per line — the template exists and inserts from then on.
  - **Shipped surface:** the `I` picker, the editor, `settings.templates`.
  - **Acceptance test(s):** AT-1501.
  - **Boundary catalog (QC-3):** ☑ empty (all-empty edit — nothing saved, one-line reason) ☑ boundary (blank lines between tasks; a single task) ☑ error — none new.
  - **Negative control:** esc leaves `settings.templates` byte-identical.

### LLR-1501.1 — the editor modal and the linear-chain shape
- **Traceability:** HLR-1501
- **Ledger:** LED-2026-10-07-batch-09.1
- **Statement:** `modals` shall provide the editor modal (name field + the multi-line tasks field, the app's shipped editor patterns — read how the setup/project editors collect text; a TextArea is acceptable if the app already ships one, else the lightest house-consistent composition); on save it emits the template through the same validation seam the JSON read uses (`models`'s lenient shape — a line becomes a title; the emitted `wait` chain is linear 0<-1<-2...); `app` wires the picker's `New template...` row to it and the save to `settings` + the pinned toast.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_template_new.py -q`
- **Numeric pass threshold:** `0 failures`; the arms above all green.
- **Negative control:** the all-empty edit — settings byte-identical.
- **Boundary catalog:** none beyond HLR-1501's.

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:** `<one fenced FLOW block per information flow: SOURCE, NODES (each node with exactly one owner, an LLR above — split a node two LLRs own), SINK>`
- **Part B — boundary decomposition:** `<yes — one fenced COMPONENT block per component | no — and why no component of the boundary is addressable on its own>`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

### 5.2 Batch acceptance criteria
- every HLR/LLR has a passing TC/AT; every new assertion RED on the base tree or by a recorded mutation.
- full suite: 0 failures besides the declared G-011 flake.

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
# Requirements ledger — taskboard — Batch 2026-10-07-batch-09

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
