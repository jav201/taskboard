# Requirements Document — taskboard — Batch 2026-10-07-batch-08

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
| US-1401 | As the operator, I want to save an existing chain as a template with one key and a name, so that my real processes become reusable without hand-writing JSON. | the batch-07 carry + the operator's 'continua con lo que sigue' 2026-10-07 | READY |

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
| P-1 | The v1 store + picker + insert all ship (batch-07, 2575 green) — authoring only writes `settings.templates` and reuses the read/insert seats | base behavior | TRUE | `git show bafa1e3 --stat` (the batch-07 files) + the green suite | HLR-1401 composes them |

- **Premise evaluation:** 1 premise(s) · ✅ TRUE

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — one lane on the main checkout.

---

## 3. High-level requirements (HLR)

### HLR-1401 — Save a chain as a template from the app
- **Traceability:** US-1401
- **Ledger:** LED-2026-10-07-batch-08.1
- **Statement:** The app shall save a dependency chain as a user template from the chain map: a key on a selected tile stores the task's CONNECTED CHAIN — every open task of the same project reachable through `depends_on` in both directions (the component) — into `settings["templates"]` as `{"name", "tasks": [{"title", "notes"?, "wait"?}]}` (order: by the component's due/insertion order, each `wait` pointing at its predecessor's index; a task with several predecessors keeps the FIRST and the rest are dropped, declared); the operator types the name in a one-line prompt (the shipped TextPrompt pattern; empty/esc cancels, nothing written); on save the app saves the board and toasts `Template '<name>' saved — <N> tasks` (`markup=False`); the new template lists in the `I` picker from then on (user templates first); saving is NOT an undo step (it writes settings, not tasks — declared); a tile whose component is a single unlinked task saves a one-task template (the degenerate case is allowed and useful).
- **Rationale (informative):** the batch-07 carry — building templates by hand in JSON is the v1 stopgap; the operator asked to keep going with what follows.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_template_save.py tests/test_template_save_app.py -q` (the increment's files)
- **Numeric pass threshold:** `0 failures`; the component arms (both directions, the multi-predecessor drop declared, the single-task degenerate case) and the app arms (key → prompt → saved → picker lists it → insert reproduces the chain) all green.
- **Priority:** medium
- **Acceptance (black-box):**
  - **Observable outcome:** on the chain map, select a tile of a chain, press the key, type a name — the chain is a reusable template from then on.
  - **Shipped surface:** the chain map key, the name prompt, `settings.templates`, the `I` picker.
  - **Acceptance test(s):** AT-1401.
  - **Boundary catalog (QC-3):** ☑ empty (esc/empty name — nothing written) ☑ boundary (the single-task component; the multi-predecessor task keeps its first link) ☑ error — none new.
  - **Negative control:** esc leaves `settings.templates` byte-identical.

### LLR-1401.1 — the component walk and the template shape
- **Traceability:** HLR-1401
- **Ledger:** LED-2026-10-07-batch-08.1
- **Statement:** `models` shall provide `chain_template(board, task_id) -> Template | None`: the task's connected component through `depends_on` within its project (BFS both directions, OPEN tasks only, each task once); None when the task is missing or done/archived; the emitted template orders tasks so every `wait` index points backward (a topological order by the component's links; a task with multiple predecessors keeps the first encountered, the rest dropped — the shape cannot represent a fan-in); titles/notes carried verbatim.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_template_save.py -q`
- **Numeric pass threshold:** `0 failures`; the arms: both-direction BFS, the fan-in drop, the degenerate single task, None for a done/archived/missing task.
- **Negative control:** a fan-in task's saved template keeps ONE predecessor — inserting it reproduces a chain, not a diamond (asserted by the round-trip arm).
- **Boundary catalog:** ☑ boundary (fan-in) ☑ empty (single task).

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
- full suite: 0 failures.
- the batch-06 visual re-verdict stays pending (the verdict sheet ships with this batch's record).## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
### 6.3 Open risks
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-07-batch-08

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
