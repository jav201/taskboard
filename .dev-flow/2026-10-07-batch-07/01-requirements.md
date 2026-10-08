# Requirements Document — taskboard — Batch 2026-10-07-batch-07

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
| US-1301 | As the operator, I want process/chain templates I can insert into a project as linked tasks in one action, so that recurring processes become chains without typing each task. | operator request 2026-10-07 | READY |

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
| P-1 | The shipped patterns cover every mechanism this needs: the LinkPicker-style modal (AT-801b), the milestones one-step undo (`u` removes a whole conversion), the presentation's project resolution, and the `○` tiles that make a fresh chain visible at once | base behavior | TRUE | `taskboard/modals.py` (the picker family) · `app.action_undo` milestones branch · `action_present` resolution · batch-06's LLR-1201 | LLR-1301.2 composes them; nothing new is invented |
| P-2 | A template's `wait` chain is forward-only by construction (an index may only point backwards), so cycles are impossible and a malformed index degrades to one unlinked task | design invariant | TRUE | the store's read (LLR-1301.1) — enforced where the link list is built | the lenient-read arm pins the degradation |

- **Premise evaluation:** 2 premise(s) · ✅ TRUE / ✅ TRUE

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — one lane on the main checkout (one implementing brief owns the tree; the trunk is the coordinator's).

---

## 3. High-level requirements (HLR)

### HLR-1301 — Process/chain templates insertable into a project
- **Traceability:** US-1301
- **Ledger:** LED-2026-10-07-batch-07.1 · LED-2026-10-07-batch-07.2
- **Statement:** The app shall carry insertable process templates — named task chains — and insert one into a project in one action: user templates live in the board's own `settings["templates"]` (portable with the board; edited in the board JSON at v1, documented in the `?` help); TWO factory presets ship as examples; key `I` opens the template picker (user templates first, then presets); the insert targets the selected task's project (the focused project when set; no resolvable project → the `No project to insert into.` toast, `markup=False`); the tasks are created in the board's FIRST phase with NO dates, ids generated, linked exactly as the template declares (`wait` = the predecessor's index inside the template — forward-only, cycles impossible by construction; a malformed `wait` is skipped, the task still created unlinked); the whole insert is ONE undo step (`u` removes every inserted task, the shipped milestones-undo pattern); a toast names the outcome (`Inserted '<name>' — <N> tasks into <project>`, `markup=False`); the inserted chain is immediately visible — chained tasks on the chain map, unlinked ones as `○` tiles (HLR-1201); v1 does NOT include template authoring from the app ("save this chain as a template" is a declared carry).
- **Rationale (informative):** the operator's request 2026-10-07: "crear templates de procesos o templates de cadenas que se reflejan en tareas que se pueden insertar a proyecto".
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_templates.py tests/test_templates_app.py -q` (the increment's files)
- **Numeric pass threshold:** `0 failures`; the store arms (round-trip, lenient read, presets) and the app arms (picker → insert with links into the right project → one-step undo → the exact toast) all green.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** press `I`, pick a template, and the project's chain of tasks exists — linked, named, undoable in one step.
  - **Shipped surface:** key `I`, the picker, the board's tasks/links, the undo, the toast.
  - **Acceptance test(s):** AT-1301.
  - **Boundary catalog (QC-3):** ☑ empty (no user templates — presets still list; an empty template inserts nothing and says so) ☑ boundary (a template whose `wait` points forward/malformed — that link skipped) ☑ error (no project to insert into — the toast).
  - **Negative control:** `u` after the insert removes EVERY inserted task in one step; a second `u` does not resurrect them.

### LLR-1301.1 — the template store (user settings + factory presets, lenient read)
- **Traceability:** HLR-1301
- **Ledger:** LED-2026-10-07-batch-07.1
- **Statement:** `models` shall provide the template store: `settings["templates"]` holds a list of `{"name": str, "tasks": [{"title": str, "notes"?: str, "wait": int|null}]}`; the read is lenient — a malformed entry (non-text name, empty title, bad `wait`) is skipped, never raising; the store ships TWO factory presets (`Simple chain`: Plan → Build → Ship; `Bugfix`: Triage → Fix → Verify); the picker lists user templates first, presets after, each with its task count.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_templates.py -q`
- **Numeric pass threshold:** `0 failures`; the round-trip arm, the lenient-read arm (junk list → only valid entries), the presets arm.
- **Negative control:** a template with a forward/malformed `wait` reads with that link dropped.
- **Boundary catalog:** ☑ invalid (junk entries) ☑ empty (no user templates).

### LLR-1301.2 — the insert (picker, creation, links, one undo, the toast)
- **Traceability:** HLR-1301
- **Ledger:** LED-2026-10-07-batch-07.1 · LED-2026-10-07-batch-07.2
- **Statement:** `app` shall bind `I` (global, palette-only, group "misc") to the template picker; on a pick, the app resolves the target project (selected task's, the focused when set — the presentation's resolution), creates the tasks in the board's first phase with no dates, links them per the template (`wait` indices, forward-only; malformed waits skipped), pushes ONE undo entry holding every created id, saves, refreshes, and toasts `Inserted '<name>' — <N> tasks into <project>` (`markup=False`); `u` removes them all in one step; the `?` help names the key and documents that v1 edits templates in the board JSON.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_templates_app.py -q`
- **Numeric pass threshold:** `0 failures`; AT-1301 arms: picker lists presets with counts; the insert lands N tasks with the exact `depends_on` chain in the right project; the toast equals the pinned literal; one `u` removes all; the no-project toast arm.
- **Negative control:** `u` twice — the second says "Nothing to undo." (no resurrection).
- **Boundary catalog:** none beyond LLR-1301.1's.

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: a template, from the board's settings to the project's chain
  SOURCE : settings["templates"] (user) + the factory presets; the key `I`; the selection/focus
  NODES  :
    - fn    : models template store (lenient read, presets)
      owner : LLR-1301.1
    - fn    : app action_templates (picker, creation, links, one undo, toast) + keymap I
      owner : LLR-1301.2
  SINK   : the board's tasks/depends_on (the kanban band, the chain map chains), the undo stack, the toast
```

- **Part B — boundary decomposition:** `no — no new addressable component.`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

### 5.2 Batch acceptance criteria
- every HLR/LLR has a passing TC/AT; every new assertion RED on the base tree or by a recorded mutation.
- full suite: 0 failures.
- the batch-06 visual re-verdict stays pending in the backlog (not this batch's gate).

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
# Requirements ledger — taskboard — Batch 2026-10-07-batch-07

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
