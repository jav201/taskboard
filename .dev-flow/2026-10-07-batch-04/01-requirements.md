# Requirements Document — taskboard — Batch 2026-10-07-batch-04

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
| US-1001 | As the operator, I want one key (`R`) to turn the current project into a presentation — the gantt on top, the tasks and their full text below, a cursor that expands each task's notes — exporting to SVG and PNG, so that I can present the project without leaving the app. | batch E of the kg_mejoras plan; the operator's verdict 2026-10-07 on the prototype round (PRES-C; SVG+PNG; R replaces the report); the D-530 request | READY |

**Refinement:** INVEST all ✓ (the prototype round + the verdict de-risked every axis). The PRES-C
frames are the oracle; the prototype's build.py is the port source.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | Key `R` is bound to the report on the base tree, and `report` is a global palette-only key — the verdict's ruling (`R` REPLACES the report) has a real seat to take over | base behavior | TRUE | `git show HEAD:taskboard/keymap.py` prints `Key("R", "R", "report", "Report", group="misc", bar=False)`; `tests/test_keymap.py:67` carries `report` in `GLOBAL_ACTIONS` | the binding becomes `present` in LLR-1001.2; the CLI `--report` keeps its seat |
| P-2 | The HTML report's destination convention is the board's own `reports/` folder — the presentation's export can inherit it without a new convention | base behavior | TRUE | `views.py` (`present_paths`, beside the report's path builder): the base is `Path(board.path).parent / "reports"` on both | LLR-1001.2 exports there |
| P-3 | The headless-browser PNG recipe runs on the operator's machine (Microsoft Edge) — and where it does not, the export must degrade to SVG + a named warning, never a crash | environment | TRUE | `evidence/run2.log` (the prototype round's probe rendered the PNGs; committed copy); the degrade path is pinned by AT-1001's `PNG needs Microsoft Edge` arm | `save_present_png` returns `None` on a missing renderer; `action_export` toasts the warning (markup=False) |

- **Premise evaluation:** 3 premise(s) · ✅ TRUE / ✅ TRUE / ✅ TRUE

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — the batch runs one lane: the increments land in order on the previous one's tree. (The trunk was forked into the `present-e` worktree for isolation from the parallel cleanup batch; one owner — the orchestrator — holds the trunk; the two tracks touch disjoint file sets: batch-04 owns the presentation section of `taskboard/views.py` + `app.py` + `keymap.py`, the cleanup batch owns `models.py` + the fold row in `views.py` — the merge resolves the one shared file by union.)

---

## 3. High-level requirements (HLR)

### HLR-1001 — The presentation mode
- **Traceability:** US-1001
- **Ledger:** LED-2026-10-07-batch-04.1
- **Statement:** Key `R` shall open the presentation of the selected task's project (the focused project when set): the gantt field on top and the brief blocks below — each task's title, dates, phase, the notes paragraph wrapped to the width, the links line — a `⟦━⟧` cursor across the brief blocks (`←`/`→` move, the cursor'd task's notes expand), `esc` leaving, the frame byte-faithful to the PRES-C oracle at 118×30 and 80×24 (the C-2b budget; S1 throughout); and the presentation shall export what it shows to SVG and PNG at the shipped report's destination convention.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests -q` + the oracle frame diff
- **Numeric pass threshold:** the exact PRES-C oracle rows at both sizes; the suite green.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** `R` presents the project; the cursor expands each task's notes; the export lands SVG + PNG.
  - **Shipped surface:** key `R`, the surface, the export.
  - **Acceptance test(s):** AT-1001.
  - **Boundary catalog:** ☑ empty (a project with no tasks) ☑ boundary (the last brief block; the 24-row fold) ☑ error — none new.
  - **Negative control:** `esc` leaves without a trace.

### LLR-1001.1 — The presentation renderer (the PRES-C oracle)
- **Traceability:** HLR-1001
- **Ledger:** LED-2026-10-07-batch-04.1
- **Statement:** `views.py` shall provide `render_present(board, project_id, cursor_id, today, width, height)` drawing the PRES-C oracle frames byte-faithfully at 118×30 and 80×24 — the header (`◆ PRESENT · ‹project› — hybrid` against `‹n› open · ▲‹n› past due | ‹n› done`); the project's span row (ash-behind/hue-ahead bar, `◆` on the committed due, `●` where the work got to, `◂`/`▸` off-window); per open task a gantt row (`▎` label, the `↳` mark when the task waits on open work, the lattice field with the flowing `▬` pulse inside an active bar, the `⟦━⟧` heavy cursor echo over the cursor'd task's span, the `‹Mon D› ▲‹n›d` chip) and, below the separator, a brief block per task — title, dates, phase, the notes paragraph wrapped to the width (the cursor'd task's notes expand, capped at 3 lines) and the links line; every untrusted string escaped and clipped to its cell (S1), every row exactly `width` cells, and the row width measured through rich's own parse (`_strip`), never a regex — an escaped bracket a user typed is a visible cell, not a tag-shaped hole (the TC-1003 defect: the regex measure undercounted those, `_pad` over-padded, the frame grew past its width while the finish assert agreed with the wrong number); a project with no open tasks still presents its header/span/keys; a board with no visible project paints `no project to present`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_present.py -q -k "TC_1001 or TC_1002 or TC_1003 or TC_1004"`
- **Numeric pass threshold:** TC-1001 (the rendered rows at 118×30 equal `PRES-C-118x30.txt` line for line), TC-1002 (the same at 80×24), TC-1003 (a hostile `[bold]x[/bold]` title and `[/] boom` notes paint literally and every row measures exactly 118 cells), TC-1004 (both empty boundaries paint, widths held).
- **Negative control:** TC-1003's hostile payload — RED on the regex `_strip` (the task row measured 129 ≠ 118) and GREEN on the rich-parse seam.
- **Boundary catalog:** ☑ empty (no open tasks; no visible project) ☑ boundary (the 24-row fold; the last brief block) ☑ invalid — none new ☑ error — none new.

### LLR-1001.2 — The R key, the presentation screen, and the SVG + PNG export
- **Traceability:** HLR-1001
- **Ledger:** LED-2026-10-07-batch-04.1
- **Statement:** Key `R` shall open the presentation — `Key("R", "R", "present", "Present", group="misc", bar=False)`, a global palette-only key REPLACING the report key (the `--report` shell CLI is unchanged) — of the selected task's project (the focused project when set; no resolvable project → the `No project to present.` toast, `markup=False`); `PresentScreen` paints `render_present` into `#present-frame` over a one-line hint, repaints on resize, moves the `⟦━⟧` cursor across the brief blocks with `←`/`→`/`↑`/`↓`/`h`/`j`/`k`/`l`, exports with `x` what it shows — `present-‹slug›-‹today›.svg` always, the `.png` through the headless-browser recipe where a renderer exists, else the `Exported ‹svg› — PNG needs Microsoft Edge` warning toast, never a crash — both at the board's own `reports/` folder (the shipped report destination convention), and leaves on `esc`/`q`; the screen is read-only — it draws the board, it never saves it. The markup census names the presentation seat exempt like the board seat: `render_present` builds Rich markup with `escape` (D-405 family).
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle tests/test_report.py tests/test_keymap.py -q`
- **Numeric pass threshold:** AT-1001 (`R` paints the exact PRES-C-118x30 frame through the shipped surface; moving the cursor expands the next task's notes; `x` lands the SVG and the PNG or the Edge warning; `esc` leaves; the board is untouched — no save, same mtime, no `.html` written), `test_the_present_key_is_in_the_seat` (`R` is a palette-only global), `test_pressing_R_opens_the_presentation_read_only`.
- **Negative control:** the no-project toast; AT-1001's no-write net (the negative control for "read-only": any save during the presentation fails the run).
- **Boundary catalog:** none beyond LLR-1001.1's.

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the presentation, from the board file to the screen and the reports/ folder
  SOURCE : the board file on disk (projects, tasks, notes, urls, start/due dates, phases); the key seat (`R`) and the selection
  NODES  :
    - fn    : views.render_present + the _present_* helpers (the PRES-C frame rows; the escape/clip width law)
      owner : LLR-1001.1
    - fn    : KEYMAP `R` / TaskboardApp.action_present / PresentScreen (paint, cursor move, close; the read-only law)
      owner : LLR-1001.2
    - fn    : views.present_paths / save_present_svg / save_present_png (the exports at the report destination convention)
      owner : LLR-1001.2
  SINK   : the terminal surface (the painted #present-frame and the hint) and the board's reports/ folder (present-*.svg, present-*.png)
```

- **Part B — boundary decomposition:** `no — no new addressable component.` (the presentation is one modal surface of the shipped app; the exports land in the board's own reports/ folder, not an independently addressable component.)

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion RED on the base tree or by a recorded mutation.
- the exact PRES-C oracle rows at 118×30 and 80×24 byte-for-byte (`tests/test_present.py` against `.dev-flow/2026-10-07-batch-04/evidence/frames/PRES-C-*.txt`).
- full suite: 0 failures.

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
# Requirements ledger — taskboard — Batch 2026-10-07-batch-03

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
