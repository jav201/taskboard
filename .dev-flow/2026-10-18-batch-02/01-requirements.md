# Requirements Document — taskboard — Batch 2026-10-18-batch-02

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
| US-1901 | As the maintainer running the full suite, I want a red test to mean a product defect — the two standup tests encoding their intent with the scrubbed placeholder name, and the clipboard roundtrip test skipping, with its reason, when Windows refuses to seed the clipboard — so that a clean run is 0 failures and a failure is worth reading. | operator 2026-10-18 (translated): «Continue with the backlog: fix the Standup tests and the other missing items»; backlog lane of 2026-10-16-batch-01 (the standup failures, the clipboard G-001) | READY |
| US-1902 | As a presenter whose terminal is resized narrow (a split screen, a small window), I want the presentation to keep running and to say what it cannot show — at any width — and its key hint to stay readable or visibly cut, so that `R` never crashes the app and never silently hides keys. | backlog lane of 2026-10-18-batch-01 (the pre-existing narrow-width assert; code-review F2) | READY |
| US-1903 | As the operator, the design authority for the TUI, I want the three open polish items (the dim view word and cut marks, the terse 80-column hint, the gantt view's 3-row note cap) shown as real-app variants next to today's look, at 118×31 and 80×25, on one page that compares them and recommends one, so that I can give a verdict before anything ships. | backlog lane of 2026-10-18-batch-01 (UX4-2, UX4-3, UX4-4); the operator's standing rule: TUI design changes need a prototype round with real-app renders and a verdict BEFORE implementation | READY |

#### Refinement log (one block per story)

**US-1901 — the suite tells the truth**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the maintainer (and every batch's gate run) · outcome = the full suite reports 0 failures; `test_win_clipboard_roundtrip` either passes, fails on a real roundtrip mismatch, or skips with a reason naming the environment's refusal · why = two known failures and an intermittent environment failure have been carried through five batch gates, so a red run no longer means anything · out of scope = the standup view's rendering (its name column stays 12 cells), the clipboard reader `models.grab_clipboard_text`
- **Feasibility (E, S):** implementation path = test-side only: the standup tests locate the operator's row by the name as the standup paints it (the 16-cell placeholder cut to the 12-cell name column with `…`); the clipboard test's loop moves into a helper that returns a skip reason when the machine never lets the sample be seeded and confirmed and still raises on a mismatch · dependencies/unknowns = none · fits one batch? = yes, one increment with no source file
- **Evaluability (T) — behavioral, black-box:** When the maintainer runs the full suite, it reports 0 failures; when `Set-Clipboard` is refused during the clipboard test's setup, the test is reported SKIPPED with the refusal in its reason; when the clipboard holds the sample and the reader returns something else, the test FAILS (AT-1901, AT-1902).
- **Open questions:** none.
- **Classification:** `READY`.

**US-1902 — the presentation at any width**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = a presenter in the real app (`R`) · outcome = below 36 columns the frame shows one fixed line saying the presentation needs 36+ columns (cut with `…` when even that does not fit), and every key still works; the hint row under the frame shows the long wording, the short one, or the view switch and `esc` alone — the first that fits — and cuts with a visible `…` below that; the `x` export writes the frame on screen · why = the app dies on an `AssertionError` when the terminal is narrowed below 36 columns with `R` open, and the hint is clipped silently below ~58 · out of scope = a narrow layout of the gantt field itself (a design change), the frame at 36 and above (byte oracles PRES-V3 unchanged)
- **Feasibility (E, S):** implementation path = `views.render_present` returns the narrow frame before the column split when `width < 36`; `PresentScreen._hint` tries its wordings longest first and truncates the last · dependencies/unknowns = none (probed on a scratch worktree, §2.7) · fits one batch? = yes, one increment, 2 source files
- **Evaluability (T) — behavioral, black-box:** When the presenter opens `R` at 118×31 and the terminal is resized to 60, 40, 35, 30, 20, 5 and 1 columns, the app keeps the presentation open, the frame below 36 reads `present needs 36+ columns` (cut to the width), the hint row never exceeds its row and ends in `…` whenever it is cut, and `x` at 30 columns writes an SVG holding the narrow frame (AT-1903, AT-1904).
- **Open questions:** none — the wording is fixed text; the operator sees it in the evidence captures.
- **Classification:** `READY`.

**US-1903 — the polish prototype round**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `prototypes/backlog_polish/` holds, for each of the three items, the current look and one or two variants captured from the running app headless (`export_screenshot` → SVG → PNG through `views.save_present_png`) at 118×31 and 80×25, and one self-contained HTML page (prose in Spanish, UI in English) that compares them and recommends one per item · why = the standing rule: no TUI design change ships without a prototype round and a verdict · out of scope = any change under `taskboard/` for these items (the variants live in the prototype's own patches); implementing the verdict
- **Feasibility (E, S):** implementation path = a capture script that patches the presentation's tones, hint wordings and note cap inside the prototype process, the app untouched; a page builder embedding the PNGs (the `prototypes/present_views/` pattern) · dependencies/unknowns = Microsoft Edge for the PNGs (present on this host; the earlier rounds used it) · fits one batch? = yes, one increment with no source file
- **Evaluability (T) — behavioral, black-box:** When the operator opens `prototypes/backlog_polish/backlog-polish-prototype.html`, each item shows the current look and its variants at both sizes as images from the real app, and a recommendation (AT-1905).
- **Open questions:** none for the round; the verdict is the operator's.
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
# Requirements ledger — taskboard — Batch 2026-10-18-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
