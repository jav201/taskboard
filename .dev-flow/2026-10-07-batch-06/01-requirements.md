# Requirements Document — taskboard — Batch 2026-10-07-batch-06

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
| US-1201 | As the operator, I want the chain map to show every open task and let me create the first link right there with `L`, so that building the dependency web happens where I look at it. | operator report 2026-10-07 ("es imposible crear cadenas") | READY |
| US-1202 | As the operator, I want the kanban to show me when phase columns are hidden and on which side, so that I know the rest exists without guessing. | operator report 2026-10-07 ("no logro ver el resto... incluso reescalando") | READY |

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
| P-1 | The shipped `L` LinkPicker flow works off-view (kanban/gantt): on a copy of the operator's real board (84 tasks, 0 links) `L` on kanban opened the picker with all 34 open tasks as candidates | base behavior | TRUE | coordinator reproduction 2026-10-07 on a temp copy of the operator's default board (LinkPicker opened, 34 candidates; the board file is read-only input) | the fix moves creation INTO the map (LLR-1201.2) |
| P-2 | The chain map's nav/selection machinery (`_chainmap_nav`, the seats) and the `○` "open chain head" glyph already exist — the tiles are an admission change, not a new mechanism | base behavior | TRUE | `taskboard/views.py` (`_chainmap_nav`, the legend in `help_usage`) | LLR-1201.1 admits the tasks; LLR-1201.2 wires the seats |
| P-3 | The C-2b frames pin a zero-link band as an inert `no links` row and the fixture's bands carry "open not linked" counts (2 on Website) — those tasks exist in the fixture and the amended frames change | contract being amended | TRUE — and it is exactly what LED-2026-10-07-batch-06.1 amends | `.dev-flow/2026-10-07-batch-02/evidence/frames/C-2b-118x30.txt:22` | the amended oracle is this renderer's bytes on the same frozen fixture, stored at this batch's evidence home |

- **Premise evaluation:** 3 premise(s) · ✅ TRUE / ✅ TRUE / ✅ TRUE

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — the batch runs one lane on the main checkout. (One implementing brief at P3 owns the whole tree sequentially; the trunk — requirements, the LED, the oracle amendment's record — is the coordinator's alone.)

---

## 3. High-level requirements (HLR)

### HLR-1201 — The chain map draws every open task; chains are created on the map
- **Traceability:** US-1201
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** The chain map shall draw every OPEN task of a visible project: linked tasks as today (chains, the meta rows, the critical chain, the per-band `dates` switch) and UNLINKED open tasks as one-row `○` tiles at depth 0 inside their project's band — the legend's existing "open chain head" mark — each selectable and reachable by the arrows; `L` on ANY tile opens the shipped LinkPicker so a chain is created where it is seen (the picked task gains its incoming link and its tile joins that chain); `x` unlinks the selected task's first incoming link as today, leaving it an `○` tile — visible and re-linkable, never vanished; the band heads keep their counts (`‹n› linked · ‹m› open not linked` — the `○` tiles ARE those m tasks); the inert `no links` row survives only for a project with no open work at all; the C-2b oracle frames at 118×30 and 80×24 AMEND under LED-2026-10-07-batch-06.1 (the amended frames are the new renderer's bytes on the same frozen fixture, stored at this batch's evidence home; the sealed batch-02 frames stay history).
- **Rationale (informative):** the operator's report 2026-07.. no — 2026-10-07: a board with zero links shows projects with no tasks and no way to create a chain ("es imposible crear cadenas"); the picker flow existed only off-view (kanban/gantt `L`), invisible from the map.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_chainmap.py tests/test_chainmap_app.py -q`
- **Numeric pass threshold:** `0 failures`; TC-801/TC-802 byte-exact against the AMENDED frames at both sizes; the new arms: an unlinked task paints as an `○` tile, is selectable, `L` links it ON the map (the picker opens, the link lands, the tile joins the chain); `x` leaves an `○` tile; the `no links` row only for projects with no open work.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** on a board with no links, the chain map shows every open task as an `○` tile; selecting one and pressing `L` creates the first link right there; the web grows where it is looked at.
  - **Shipped surface:** the chain map (tiles, the `L`/`x` seats, the band heads), the amended oracle frames.
  - **Acceptance test(s):** AT-1201.
  - **Boundary catalog (QC-3):** ☑ empty (a project with no open work — the inert row stands) ☑ boundary (the first link of a board; a task that becomes unlinked) ☑ error — none new.
  - **Negative control:** `x` on a never-linked task refuses as today (nothing to remove).

### HLR-1202 — The kanban window shows its hidden sides
- **Traceability:** US-1202
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** When the kanban's phase window hides open-phase columns (the shipped `fits`/`start` law), the phase-head row shall mark the hidden sides — `◂` at the left edge when any phase is hidden left, `▸ N` (N exact) at the right edge when any are hidden right; when nothing is hidden the head row carries no markers; the `?` kanban help gains the window bullet: more phases than fit — the window follows the selection (`j`/`k` into a later column), `◂`/`▸` mark the hidden sides.
- **Rationale (informative):** the operator's report 2026-10-07: "prioriza las primeras columnas... incluso reescalando" — the window follows the selection and nothing on screen says the rest exists.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_kanban_window.py tests/test_kanban_readable.py -q` (the increment's file + the readable census)
- **Numeric pass threshold:** `0 failures`; at a width fitting 2 of 4 phases the head row carries `◂` and `▸ 2` exact; at a width fitting all, none; the help bullet present.
- **Priority:** medium
- **Acceptance (black-box):**
  - **Observable outcome:** the user always sees that more phases exist and which side they are on, before moving the selection.
  - **Shipped surface:** the kanban's phase-head row, the `?` help.
  - **Acceptance test(s):** AT-1202.
  - **Boundary catalog (QC-3):** ☑ boundary (exactly-fits vs one-hidden; the left-edge marker when the selection sits late).
  - **Negative control:** an all-fits width renders zero markers.

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-1201.1 — the renderer draws the `○` tiles and the amended oracle
- **Traceability:** HLR-1201
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** `views.render_chainmap`'s plan shall admit every open unlinked task as a depth-0 one-row `○` tile in its project's band (fold-aware: the tiles take part in the fold and the `+N more ↓` cap like any row, and only painted tiles reach the `line_map`); the band heads' counts stay as shipped; the `no links` row renders only when the project has no open work; the amended C-2b frames are this renderer's bytes on the frozen kg fixture (Data Warehouse `together`, the TC-801 board) at 118×30 and 80×24, stored at `.dev-flow/2026-10-07-batch-06/evidence/frames/`, and `tests/test_chainmap.py`'s frame path moves there citing the LED.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_chainmap.py -q`
- **Numeric pass threshold:** `0 failures`; TC-801/TC-802 byte-exact vs the AMENDED frames; the fold arms (TC-810, the cap) stay green with the tiles present.
- **Negative control:** a width where a band's `○` tiles do not fit still drops/caps the band whole (the dangling-head law).
- **Boundary catalog:** ☑ empty (no-open-work project) ☑ boundary (exactly-fits vs one-over rows).

### LLR-1201.2 — the app seats: L creates a link on the map, x leaves an `○` tile
- **Traceability:** HLR-1201
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** on the chain map, `L` with a tile selected (linked or `○`) shall open the shipped LinkPicker and apply the pick as the task's incoming link (the tile joins that chain on re-render); `x` removes the first incoming link as shipped and the task REMAINS as an `○` tile; the arrows/`j`/`k` reach the `○` tiles in nav order (band order, then the chain columns — the `○` tiles at their depth-0 column); the selection strip names an `○` selection's waits-on/unblocks truthfully (waits on nothing yet · unblocks nothing).
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_chainmap_app.py -q`
- **Numeric pass threshold:** `0 failures`; the create-on-map arm (pick a predecessor → `depends_on` lands → the tile renders inside the chain); the unlink-leaves-tile arm; the nav arm reaches an `○` tile.
- **Negative control:** `x` on a never-linked task — the shipped refusal toast, unchanged.
- **Boundary catalog:** none beyond LLR-1201.1's.

### LLR-1202.1 — the window markers and the help bullet
- **Traceability:** HLR-1202
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** `views`' kanban head row shall render `◂` before the first visible phase title when `start > 0`, and `▸ N` (N = `n_open − (start + fits)`, exact) after the last visible one when positive; no markers when the window shows everything; `views.help_usage("kanban")` carries the window bullet verbatim: "more phases than fit — the window follows the selection (j/k into a later column) · ◂ ▸ mark the hidden sides".
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_kanban_window.py -q`
- **Numeric pass threshold:** `0 failures`; the 4-phase/2-fit fixture shows `◂` and `▸ 2` at 80 cells and no markers at a full width; the help bullet string present.
- **Negative control:** the all-fits width renders zero markers.
- **Boundary catalog:** ☑ boundary (exactly-fits; selection late so `start > 0`).

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the dependency web and the kanban window, from the board to the eye
  SOURCE : the board file (tasks, phases, depends_on); the keys (L, x, the arrows); the terminal size
  NODES  :
    - fn    : views.render_chainmap + the _chainmap_* plan (the `○` tiles, the amended C-2b oracle)
      owner : LLR-1201.1
    - fn    : the chain map seats (L links on the map, x leaves the tile, nav reaches the tiles)
      owner : LLR-1201.2
    - fn    : the kanban plan's window markers + help_usage("kanban")
      owner : LLR-1202.1
  SINK   : the chain map canvas (every open task a tile), the kanban's phase-head row, the ? help
```

- **Part B — boundary decomposition:** `no — no new addressable component.`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion RED on the base tree or by a recorded mutation.
- full suite: 0 failures.
- the amended C-2b oracle ships at this batch's evidence home with the LED; the operator's visual re-verdict is requested at close (batch C's precedent: the verdict folds on arrival).

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
# Requirements ledger — taskboard — Batch 2026-10-07-batch-06

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
