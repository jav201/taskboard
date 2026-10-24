# Requirements Document — taskboard — Batch 2026-10-24-batch-01

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/req-template.md` and its part 2, `templates/guides/req-template.part2.md`, explain each field below and the rules that read it. It ships with the flow and is not copied into this batch.

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
| US-2601 | As the operator, I want one directory of milestone classes — a name, a shape, a colour, a hidden flag — shared by every board and safe from a second window, and a task field carrying the class, so that a class is written once and classifies anywhere. | MM-D2, MM-D3, MM-D4; AT-a, AT-c (store side), AT-g | READY |
| US-2602 | As the operator, I want every milestone mark drawn by one rule — the shape and colour say the class, lateness and reached state move to text beside the mark — in every view and notice, so that I classify milestones at a glance and no frame drifts. | MM-D1; section 3; AT-b | READY |
| US-2603 | As the operator editing a milestone, I want `alt+m` to open the class Select and `#` to open the manager where `n` adds a class and `space` hides one, so that classifying is two keys and the modal law holds. | MM-D5, MM-D6 (storage), MM-D8; AT-a, AT-f | READY |
| US-2604 | As the operator, I want the legend strip under the gantt ruler and in the presentation naming the drawn classes and the hidden count, hidden classes gone from the gantt and every presentation view and export, and `/#cls` to filter, so that the classification reads in the frame and filters like anything else. | MM-D6, MM-D7; AT-d, AT-e | READY |

**The chains, one line each:** US-2601 → HLR-2601, HLR-2602, HLR-2603 → AT-2601, AT-2602, AT-2607 · US-2602 → HLR-2604 → AT-2603 · US-2603 → HLR-2605, HLR-2606 → AT-2604, AT-2606 · US-2604 → HLR-2607, HLR-2608 → AT-2605 (the HLR/AT numbering is set at P1; the commission's AT-a..AT-g map onto AT-2601..AT-2607).

#### Refinement log (one block per story)

**US-2601 — the store and the field**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `~/.taskboard/marks.json` read at start beside `people.json`, written under its lock; a task's `mark` field · why = MM-D2, MM-D3 · out of scope = seeded classes (MM-D4); class deletion (not offered)
- **Feasibility (E, S):** a new `taskboard/marks.py` in the `models` layer reusing `boards.file_lock`, `keep_aside` and the atomic-write pattern of `people.py`; `Task.mark` in `models.py` written only when set · fits one batch? = yes, increment 001
- **Evaluability (T) — behavioral, black-box:** `open_app` on the round's boards: a class added in `#` survives a restart in `marks.json`; two windows each add a class and both survive; an unreadable `marks.json` is set aside never overwritten; a board with no marks keeps its bytes; a task whose `mark` is unknown renders unclassified and keeps the id on save.
- **Open questions:** none. · **Classification:** `READY`.

**US-2602 — the encoding through one seat**
- **INVEST:** I ✓ (after 001) · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = every milestone mark in every view drawn by `views.milestone_mark(task, board, today)` — class glyph+colour, late date in `over` plus `▲Nd`, reached hollow plus `✓`, unclassified `◆` in `mut` · why = MM-D1 · out of scope = the title glyphs and the project-span due marks (section 3's exclusions); the gantt ruler's lateness (accepted cost)
- **Feasibility (E, S):** one seat in `views.py`; every site listed in section 3 routed through it; `app.py`'s notices at 2133/2172/2433 · fits one batch? = yes, increment 002
- **Evaluability (T) — behavioral, black-box:** on the round's boards: a late classed milestone shows its date in `over` with `▲3d`; a reached one the hollow glyph with `✓`; an unclassified one `◆` in `mut`; a test enumerates the sites so a new frame cannot skip the seat.
- **Open questions:** none. · **Classification:** `READY`.

**US-2603 — the editor Select and the `#` manager**
- **INVEST:** I ✓ (after 001) · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = the editor's variant A: an `alt+m` Select in `#task-chips-what` after `#f-milestone`; the `#` manager window listing the classes, `n` opening its form (name, shape, colour), `space` toggling `hidden`; `#` free in `keymap.py` and `alt+m` in `TASK_KEYS` · why = MM-D5, MM-D6 (storage), MM-D8 · out of scope = class deletion; the ▲ ambiguity fix (MM-D5's log ruling)
- **Feasibility (E, S):** `modals.py` (the Select and `MarksManager` + the form), `keymap.py` (`#`), `app.py` (the screen), `taskboard.tcss` · fits one batch? = yes, increment 003, 4 source files
- **Evaluability (T) — behavioral, black-box:** `#`, `n`, a name, a shape, a colour, `alt+s`: the class is in `marks.json`; `e` on a milestone, `alt+m`, `down`, `↵`: the task carries the class and the gantt draws the class glyph; `tests/test_modal_keys.py` covers the manager and its form; unticking `milestone` keeps the field.
- **Open questions:** none. · **Classification:** `READY`.

**US-2604 — the legend, hide, search and help**
- **INVEST:** I ✓ (after 002) · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = the legend strip under the gantt ruler and in the presentation with its exports, naming only the drawn classes and the hidden count; hidden classes leave the gantt and all three presentation views and exports; `/#pay` filters by class; `?` names the classes · why = MM-D6, MM-D7 · out of scope = the legend in the agenda and people views (the strip's placement is the gantt and the presentation)
- **Feasibility (E, S):** `views.legend_strip` of the round; `matches_m`/`filter_bar_m`; `app.py` the help · fits one batch? = yes, increment 004, 3 source files
- **Evaluability (T) — behavioral, black-box:** on the round's boards: the gantt's strip names the drawn classes and `1 hidden`; after `space` in `#`, that class's milestones are gone from the gantt and all three presentation views and their exports; `/`, `#pay`, `↵` filters to that class.
- **Open questions:** none. · **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
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

### HLR-001 — `<Short title>`
- **Traceability:** US-001
- **Ledger:** none
- **Statement:** When `<trigger>`, the system shall `<response>`. *(Current state only. If you are about to write "because measured …", stop: the obligation belongs here, the measurement belongs in a ledger entry.)*
- **Rationale (informative):** *(why this requirement exists — `should` may technically be used here informally, but avoid it to prevent confusion.)*
- **Validation:** `test` | `demo` | `inspection` | `analysis`
- **Executed verification:** *(required if `test`/`analysis`. e.g. `npm run typecheck`, `vitest run TC-001`, `worst-case gain-staging sum analysis`.)*
- **Numeric pass threshold:** *(required if `test`/`analysis`. e.g. `0 errors`, `peak post-limiter ≤ −6 dBFS`.)*
- **Priority:** high | medium | low
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** *(what the user observes)*
  - **Shipped surface:** *(the handler / screen / CLI that produces it)*
  - **Acceptance test(s):** AT-001
  - **Boundary catalog (QC-3):** `<☐ empty ☐ boundary ☐ invalid ☐ error — tick each class that gets an AT/TC, or: none — and the reason no input class applies>`
  - **Negative control:** `<the executed input on which this verification GOES RED, or: none — and why it has no executed RED side>`

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-001.1 — `<Short title>`
- **Traceability:** HLR-001
- **Ledger:** none
- **Statement:** The `<component>` shall `<verifiable technical response>`.
- **Validation:** `test (unit)` | `test (integration)` | `test (e2e)` | `inspection` | `analysis`
- **Executed verification:** *(required if `test`/`analysis`. e.g. `vitest run src/lib/audio/masterBus.test.ts -t TC-001`; `gain-sum analysis vs the compressor threshold`.)*
- **Numeric pass threshold:** *(required if `test`/`analysis`. e.g. `assert exit code 0`; `peak ≤ −6 dBFS`; `RMS error < 0.01`.)*
- **Negative control:** `<the executed input on which this verification goes RED, or: none — and why it has no executed RED side>`
- **Boundary catalog:** `<☐ empty ☐ boundary ☐ invalid ☐ error — tick each class that gets an AT/TC, or: none — and the reason no input class applies>`

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
# Requirements ledger — taskboard — Batch 2026-10-24-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
