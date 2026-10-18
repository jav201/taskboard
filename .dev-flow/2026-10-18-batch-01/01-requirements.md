# Requirements Document — taskboard — Batch 2026-10-18-batch-01

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
| US-1801 | As a presenter, I want a second view in the presentation that shows, under the gantt rows, the notes of every shown open task at the same time, so that the room reads what each task says while the timeline stays in sight. | operator, 2026-10-17: «si las demás tareas tienen texto, me gustaría que todas se vieran al mismo tiempo»; the prototype round `prototypes/present_views/` (round 2, D2 · stacked, chosen 2026-10-17/18); `BACKLOG.md` "Present v3" | READY |
| US-1802 | As a presenter, I want the gantt view's expanded cursor note to keep its line breaks, bullets and numbered steps, so that a plan reads as the steps it is and not as one run-on line. | the coordinator's brief (the prototype's accepted fix: «la nota de la vista gantt conserva sus saltos de línea»), `prototypes/present_views/out/r2-118-A-gantt.png` | READY |
| US-1803 | As a presenter, I want one key to switch between the two views (`1`, `2`, `tab`, `shift+tab`), `pgdn`/`pgup` to scroll the notes, and the cursor, the hidden tasks and the `x` export to follow the view I am on, with `R` always opening on the gantt view, so that switching in front of the room never loses my place or writes anything. | the coordinator's brief (keys, shared state, R opens on gantt, the view not remembered) and the prototype's key set | READY |

#### Refinement log (one block per story)

**US-1801 — the split view: every task's notes at once**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter and the room · outcome = `2` in `R` shows the shipped gantt rows on top and, below them, one block per shown open task (heading: title, dates, days late or left; then its wrapped note with line breaks, bullets and numbered lists kept), the cursor's block in accent, two columns at ≥ 100 columns and one below; everything when it fits, else the cursor's note up to half the area and every other note at least 1–2 rows, each cut declared; a task with no notes is one row with `no notes` · why = the operator wants every task's text visible at once · out of scope = done tasks, images (not shown in this view), the round-1 "Slide" (C, kept as a backlog option) and "Cards" (B, dropped) views
- **Feasibility (E, S):** implementation path = port `prototypes/present_views/views_d.py` (`alloc`, `_clipped`, `_heading`, `_stack_column`, `render_stacked`) and the helpers of `views_proto.py` it calls (`wrap_notes`, `_note_markup`, `_scrolled`) into `taskboard/views.py` beside `render_present`, which gains a `view` argument · dependencies/unknowns = none · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the presenter presses `R` then `2`, the painted frame shows text from every shown open task that has notes, the gantt rows above, and `no notes` for a task without one (AT-1801).
- **Open questions:** none — the brief and the verdicts settle the layout, the share and the cut marks.
- **Classification:** `READY` — prototyped with real-app captures and chosen by the operator.

**US-1802 — the gantt view's note keeps its structure**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter · outcome = the cursor note (at most 3 rows) keeps its line breaks, bullets and numbered items, a cut said `… +N lines` · why = on `base_ref` `_present_note_lines` runs `textwrap.wrap` over the whole note, which flattens it («Sep 22. 1. Feature-flag…») · out of scope = the brief rows, the ruler, the field
- **Feasibility (E, S):** implementation path = the gantt branch of `render_present` uses the split view's note wrapper (`render_gantt` in `views_d.py`) · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the presenter moves the cursor onto a task whose note is a numbered plan, the painted frame shows `1. Feature-flag …` starting its own row (AT-1802).
- **Open questions:** none.
- **Classification:** `READY`.

**US-1803 — switching, scrolling, and what the views share**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter · outcome = `1` gantt, `2` split, `tab`/`shift+tab` cycle; `pgdn`/`pgup` scroll the split view's notes; the keys appear in the hint row only, never in the frame or the `x` export; the header carries a quiet grey view word; the cursor and the space-hidden tasks are shared; `a` and `x` work in both views, `x` exporting the current view's frame; `R` always opens on the gantt view and the view is not remembered, so the presentation still writes only `show_in_present` · why = the presenter switches in front of the room · out of scope = remembering the last view (refused by the brief)
- **Feasibility (E, S):** implementation path = `taskboard/app.py` `PresentScreen` gains six priority bindings, a view index and a scroll offset · dependencies/unknowns = the app's own `1`/`2` and `tab` must not fire behind the modal (checked at P1) · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the presenter presses `2`, `tab`, `shift+tab`, `1`, the header's view word follows and the board behind does not change view; `pgdn` scrolls the cut note; `space` in the split view hides the task from both views; `x` writes the current view's frame (AT-1803).
- **Open questions:** none.
- **Classification:** `READY`.

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
# Requirements ledger — taskboard — Batch 2026-10-18-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
