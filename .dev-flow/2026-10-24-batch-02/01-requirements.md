# Requirements Document — taskboard — Batch 2026-10-24-batch-02

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
| US-2701 | As an operator with several boards, I want the start screen to touch nothing until I pick a board, so that a second window with another board open no longer alarms me that the board is "already open" while I am still on the home. | The operator, 2026-10-23: «Me es útil incluso tener dos terminales abiertas, cada una con un board distinto… vi el mensaje de que ya tenía el board abierto y tenía que cerrarlo, a pesar de que estaba en la ventana de selección de Boards.» · approval 2026-10-24: «Ok, arréglalo.» · `.dev-flow/COMMISSION-home-deferred-start.md` (HD-1..HD-4) | READY |
| US-2702 | As an operator working in two windows, I want people and mark classes added in the other window to appear without a restart, so that the `@` picker, the `alt+m` Select and `#` reflect the directories as they are on disk. | The commission's second defect (HD-5) · BACKLOG item (architect A-7, accepted): «a person another window adds shows here after a restart or this window's next write» | READY |

#### Refinement log (one block per story)

**US-2701 — the home defers the board's start**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator running several boards in two terminals · outcome = the home at start writes nothing, announces nothing and opens no board modals until a board is picked; picking a board (its card's `enter`, or `esc`/`back`) starts exactly that board once; the start-up modals then open over the board · why = the false "already open" notice and the blank screen behind the start-up modals (BACKLOG D-12) · out of scope = any other home behaviour, any change to the single-board start, `--open`, or `B` pressed later.
- **Feasibility (E, S):** implementation path = read in `TaskboardApp.on_mount` / `_open_board` / `switch_board` and the `BoardsHome` actions: defer the write/announce/modal half of the start behind a per-board "started" flag · dependencies/unknowns = none — the commission records the defect read in the code · fits one batch? = yes.
- **Evaluability (T) — behavioral, black-box:** "When the app starts with two boards and another window's presence marker on the default board, the user observes on the home: no open-twice notice, no marker written, the board file's bytes unchanged; after `enter` on the card: the notice once, the marker written, the sweep run." (AT-a; AT-b..AT-d in Phase 1.)
- **Open questions:** none — the operator approved the fix as described («Ok, arréglalo.»), no prototype needed.
- **Classification:** READY — observable through the home, the notices and the board file.

**US-2702 — the directories stay fresh**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator in either window · outcome = the `@` picker, the `alt+m` class Select, `#` and the `/` `@…`/`#…` search re-read `people.json` / `marks.json` when the file changed (mtime or size) and show what the other window wrote; a failed re-read keeps the in-memory directory and notifies once · why = a person or class added in another window does not appear until restart (BACKLOG A-7) · out of scope = any other refresh path, the team roster, cross-window deletion semantics.
- **Feasibility (E, S):** implementation path = a cheap mtime/size-gated re-read helper on `Directory` (people.py / marks.py), called at the four open sites in app.py · dependencies/unknowns = none · fits one batch? = yes.
- **Evaluability (T) — behavioral, black-box:** "When a second `Directory` instance (the other window) appends a person to `people.json`, the user observes the new person in the `@` picker the next time the editor opens; the same holds for a class in the `alt+m` Select and in `#`." (AT-e; AT-f for the unreadable re-read.)
- **Open questions:** none.
- **Classification:** READY — observable through the pickers and the marks manager.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| 1 | At start with more than one board, `TaskboardApp.on_mount` pushes `BoardsHome` and then calls `_open_board(at_mount=True)`, which migrates links, sweeps old done, enters presence and opens the start-up modals — before the user picks a board. | premise | ✅ TRUE | `grep -n "at_mount" taskboard/app.py` → `app.py:1307` `self.push_screen(BoardsHome())` · `app.py:1308` `if self._open_board(at_mount=True):` · `app.py:1410` `self._migrate_links(at_switch=not at_mount)` · `app.py:1417` `if at_mount:` | the defect's pre-image; HD-1 removes the write/announce/modal half of that start |
| 2 | `switch_board` returns early when `bid == self.board_id`, so a deferred default board needs the early-return path to still run the start. | premise | ✅ TRUE | `grep -n "def switch_board" taskboard/app.py` → `app.py:1453` (the early return read at P1 increment 001) | HD-1's «esc / back runs the deferred start» leans on it |
| 3 | `self.people` and `self.marks` are loaded once at mount; a file the other window changes is not re-read until restart. | premise | ✅ TRUE | `grep -n "def load" taskboard/people.py taskboard/marks.py` → `people.py:119` · `marks.py:67`; the only loads are the mount's (read at P1) | HD-5's pre-image |
| 4 | The directories' cross-window writes are safe today (read-modify-write under a lock), so re-reading at open time inherits that safety. | premise | ✅ TRUE | asserted by the commission (§The defect, defect 2); the lock is read at P1 increment 002 | relied on, not re-proven |
| 5 | The suite's baseline at this batch's base is 3235 passed + 1 environmental skip (the clipboard arm TC-1902 / G-001, batch 2026-10-24-batch-01's P4), so P4 expects the same plus this batch's new nodes. | premise | ✅ TRUE | `.dev-flow/2026-10-24-batch-01/04-validation.md` (its P4 transcripts) · BACKLOG G-001 | P4's expected totals derive from it |

- **Premise evaluation:** 5 premise(s) · ✅ TRUE ×5 — the batch's derivation stands on all five; 4 is the commission's assertion, re-read at the increment it binds.

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

| # | Condition (`C-52`) | Discharged? | The executed evidence |
|---|---|---|---|
| 1 | **Frozen contract** — no shared interface is touched inside a lane; one that must change returns to the trunk (trigger A3) | ✅ | not applicable — one lane, no frozen interface is re-signed (A3 judged not fired at intake) |
| 2 | **Disjoint FILE sets**, not just modules — two lanes may not edit the same file, not even different regions | ✅ | not applicable — one lane; the commission's increments 001 and 002 run sequentially and both touch `taskboard/app.py` in sequence, never concurrently |
| 3 | **Crossed reverse census** — family B run per lane and **shared before starting**; the trunk's act, impossible from inside a lane | ✅ | not applicable — one lane; the B1 probe at intake (`grep -rln` over `tests/`) is the batch-wide census, re-run per increment cut per family B's rule |
| 4 | **One owner of the trunk** — requirements, traceability, backlog and spec are never written from a lane | ✅ | the orchestrator owns the trunk; no lane exists |

- **Fork preconditions:** none — this batch runs one lane (declared empty per C-52).

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
# Requirements ledger — taskboard — Batch 2026-10-24-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
