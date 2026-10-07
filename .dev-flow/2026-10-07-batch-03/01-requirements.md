# Requirements Document — taskboard — Batch 2026-10-07-batch-03

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `debería` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

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

The requirements of the cleanup batch: the six loose items the reviews and the operator filed —
S-4, S-9, K2-1, UX2-2, D-623, milestones-in-views — restated as three user stories, three HLRs
and three LLRs, each with its acceptance test, its negative control and its boundary catalog.

### 1.2 Scope
*(What this batch covers and what it does NOT cover.)*

Covers: the link migration's failure path (S-4), the non-text title at the load boundary (S-9),
the kanban `?` legend's drawn-band rule (K2-1), the late-milestone fold-row marker (UX2-2), the
milestones-only rule-only band (D-623), and the milestone `◆` identity in lanes/agenda/focus.
Does NOT cover: batch E (the presentation-mode prototype round, running in the `present-e`
worktree in parallel), the now-dead `isinstance(task.title, str)` guard in `team_sync.py`
(harmless no-op post-S-9, noted in the close-out review), and every backlog item not named above.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| `◆` | the milestone mark — one date, no bar; drawn on band rules, the agenda dot, and beside milestone titles |
| the fold row | the kanban footer row naming bands folded off screen: the canonical `▼ N below` (LLR-309.1's shipped shape) |
| a drawn band | a band the painted frame actually draws at the asked width/height — the filter and the fold both apply |
| `result.error` | the offer's error-as-data convention: a migration/conversion RETURNS its reason (a basename and the OS's words), nothing raises past it |
| late milestone | a milestone due before today (per `milestone_tone`) |

### 1.4 References
*(Related documents, standards, external tickets.)*

- `.dev-flow/BACKLOG.md` — the six items, as filed (S-4/S-9 by the 2026-10-04 security reviews; K2-1 by the batch code review; UX2-2 by PV-605; D-623 and milestones-in-views by the batch reviews).
- `01-requirements-ledger.md` — LED .1 (the batch derived), LED .2 (the P2 folds), LED .3 (the fold-canon ruling).
- `tests/test_cleanup.py` — the batch's twelve test nodes (TC-901/902, AT-901/902/903).
- Batch C's close (`.dev-flow/2026-10-07-batch-02/05-close.md`) — the base tip and its 2529-test gate.

### 1.5 Document overview
*(How this document is structured.)*

§2 the stories, the items' law, the premise evaluation and the fork preconditions. §3 the HLRs
and LLRs with their thresholds and controls. §5 the two-layer validation strategy and the batch
acceptance criteria. §7 the ledger — authored as the separate `01-requirements-ledger.md`.

---

## 2. Overall description

### 2.1 Product perspective
*(How the change fits into the larger system.)*

The board file flows in through the load boundary (`Task.from_dict`, the S-9 seat) and out
through the renderers (views.py, the LLR-903.1 seats); the link migration's failure path flows
back to the board file on disk. This batch hardens those three seats — one never-raise boundary,
one restore-first failure path, one legend/fold/band agreement between what the screen draws and
what the screen says.

### 2.2 Product functions
*(High-level list of functional capabilities.)*

- A failed link migration restores the board and the mark before any cleanup, cleans up
  best-effort, and surfaces the ORIGINAL failure via `result.error`.
- A board file with a non-text title loads safely — scalars keep the user's text, containers
  and null read `Untitled`.
- The kanban `?` legend names `◆` only for bands the screen draws; a milestones-only project
  keeps its rule-only band; a late milestone below the fold marks the fold row
  (`▼ N below · ▲N ◆`); milestones read as milestones in lanes, agenda and focus.

### 2.3 User characteristics
*(Roles, permissions, expected experience levels.)*

The maintainer (owns the board file and the migration), the operator (loads boards hand-edited
off-site), and the taskboard user (reads the kanban, lanes, agenda and focus).

### 2.4 Constraints
*(Technological, regulatory, business.)*

Textual TUI on the shipped render pipeline; the shipped `Untitled` and restore-first conventions
are the house law this batch mirrors (LED .2, CL-1); the taskboard/ + tests/ surface is frozen
except by this batch's review-filed edits; artifacts in English.

### 2.5 Assumptions and dependencies
*(What we take for granted. If an assumption fails, the batch is invalidated.)*

Tests drive synthetic boards (`tests/kg_board.py`, `tmp_path`) — no user data. The milestone
offer's order (`run_milestone_offer`) is the restore law S-4 mirrors. The operator's visual
verdict on the fold marker lands at the next session (the marker's literal is census-pinned in
its absence). The full suite is the orchestrator's single close run.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-901 | As the maintainer, I want the link migration's failure path to restore the board and its mark BEFORE any cleanup (cleanup best-effort, never raising), so that a failed migration never loses the board or re-runs on a false mark. | S-4 (security review of 2026-10-04-batch-01, MEDIUM) | READY |
| US-902 | As the operator, I want a board file with a non-text title to load safely (coerced at the boundary), so that one bad field never crashes the app. | S-9 (LOW, pre-existing) | READY |
| US-903 | As a taskboard user, I want the kanban `?` legend to name only what the drawn board shows, a milestones-only project to keep its band, and milestones to render in lanes/agenda/focus — so that what the screen says is what the screen shows. | K2-1 (LOW), D-623, UX2-2, milestones-in-views (BACKLOG) | READY |

**Refinement:** INVEST all ✓ (six named items, severity-tagged, each behavior-specified by the
finding that filed it). Out of scope: everything not named.

### 2.6a The items' law

S-4: the error handler of `run_link_migration` (models.py) restores the board bytes and the
migration mark FIRST; the backup/log removal runs in a nested best-effort guard; the ORIGINAL
error reaches `result.error` — the offer's (`run_milestone_offer`) restore-first order. S-9: `Task.from_dict`
coerces a present-but-non-text title (`str(value)` when it is the user's text, else the shipped
`Untitled`) — never raises, never at render. K2-1/D-623/UX2-2/milestones-in-views: render items
(increment 002, views.py); the fold marker is the canonical `▼ N below` + ` · ▲N ◆` suffix
(LED .3), not the BACKLOG's pre-shipped `▾ N more` note.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| 1 | The batch base is the operator-pushed Batch C tip: local HEAD equals `origin/main`, and the suite was green at 2529 there | repo | ✅ TRUE | `git ls-remote --heads origin` → `34bab3c8b110e0a18ddba281c3e75d8597e07a8f	refs/heads/main`; `git rev-parse HEAD` → `34bab3c8b110e0a18ddba281c3e75d8597e07a8f`; `.dev-flow/2026-10-07-batch-02/evidence/close-gate.txt` → `2529 passed in 404.16s · exit 0 — 0 failed` | recorded in PLAN/close |
| 2 | The milestone offer's failure path restores the board FIRST and removes its own files best-effort — the order S-4 mirrors | code | ✅ TRUE | `taskboard/models.py:1692-1699` (the docstring's law) and `:1744-1754` (the `except OSError`: restore flags and mark, then `try: (target.parent / name).unlink(missing_ok=True) … except OSError: pass` around this run's files) | the HLR-901 pattern source |
| 3 | The shipped title convention: a MISSING title reads `Untitled`, and pre-S-9 code assumed title-is-text at render | code | ✅ TRUE | `taskboard/models.py:875` — `raw_title = d.get("title", "Untitled")`; the assumption S-9 retires still on disk: `taskboard/team_sync.py:226` — `if not isinstance(task.title, str):` (dead post-coercion, supersession-census noted) | recorded |
| 4 | The kanban fold row's canonical literal is `▼ N below`, pinned by the 7-fold census; a rename to `▾ N more` reddens it | tests | ✅ TRUE | `grep -n "below" tests/test_kanban_readable.py` → the FOLD regex `:66` and the literal sites `:480`, `:574`, `:607` (×4 params), `:1221` — 7 of the 9 TC_311 nodes read it; executed RED: `evidence/inc002-mutations.log` M1 → `7 failed, 2 passed` | the fold-canon law (LED .3) |
| 5 | The kg milestones board (AT-903's fixture source) folds Ops & Security's late milestone off screen at 118×24 | fixture | ✅ TRUE | `tests/kg_board.py` — `milestones(shifted(path), date.today())`, the `_ms_board` fixture in `tests/test_cleanup.py:69-77`; the fold asserted at runtime by AT-903 arm 3 (`tests/test_cleanup.py:336-339`, `re.search(r"▼.*▲1 ◆", r)`) | recorded |

- **Premise evaluation:** 5 premises · ✅ TRUE

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

| # | Condition (`C-52`) | Discharged? | The executed evidence |
|---|---|---|---|
| 1 | **Frozen contract** — no shared interface is touched inside a lane; one that must change returns to the trunk (trigger A3) | ✅ | One lane per increment; the parallel agents' interfaces stayed inside their own files — `_coerce_title` is models-private; the app.py branch adds a caller input without changing a signature. The one cross-file item (K2-1's fold half) was returned to the trunk, not fixed from the lane: chunkA's report names the stop (`evidence/chunkA-run.log` REPORT BACK §3). |
| 2 | **Disjoint FILE sets**, not just modules — two lanes may not edit the same file, not even different regions | ✅ | The file sets: {`taskboard/models.py`, `taskboard/app.py`} (chunkA product) ∥ {`tests/test_cleanup.py`, `tests/test_team_sync.py`} (chunkB tests) ∥ {`taskboard/views.py`} (increment 002 render). Intersection probe: `git diff --name-only HEAD` → `taskboard/app.py`, `taskboard/models.py`, `taskboard/views.py`, `tests/test_team_sync.py` (+ untracked `tests/test_cleanup.py`) — each in exactly one set. |
| 3 | **Crossed reverse census** — family B run per lane and **shared before starting**; the trunk's act, impossible from inside a lane | ✅ | Run per increment and shared in the packets: `evidence/inc001-mutations.log` / `evidence/inc002-mutations.log` §REVERSE CENSUS (probes B1/B2/B3/B4/A3, commands + outputs). The trunk-side crossing act: the coordinator reconciled the 7-census reddening the fold rename provoked and reverted it (LED .3). |
| 4 | **One owner of the trunk** — requirements, traceability, backlog and spec are never written from a lane | ✅ | The coordinator (orchestrator) owns the contract, the ledger and the backlog; the workers' briefs forbid it — chunkA: "Do NOT touch `tests/`"; chunkB: "`tests/test_cleanup.py` ONLY"; inc002: "`taskboard/views.py` ONLY. No tests. No git." (`evidence/*-brief.md`). |

- **Fork preconditions:** 0 lane(s) — one lane per increment; the four C-52 conditions read over the parallel external agents above, each ✅ (the flow's lane fork was not used; the parallelism was disjoint-file agents meeting at the green suite)

---

## 3. High-level requirements (HLR)

### HLR-901 — The migration fails safe
- **Traceability:** US-901
- **Ledger:** LED-2026-10-07-batch-03.1, LED-2026-10-07-batch-03.2
- **Statement:** When `run_link_migration` fails at any point, the system shall restore the board file and the migration mark FIRST, shall attempt the removal of its own backup and log only inside a nested best-effort guard that never raises, and shall then surface the ORIGINAL failure unchanged via `result.error` (the offer's error-as-data convention — the function RETURNS its result like `run_milestone_offer`; nothing raises past it) — the board and the mark exactly as they were, the cleanup never inventing a new failure.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests -q -k migration`
- **Numeric pass threshold:** TC-901: a migration whose post-write cleanup hits a refusing `unlink` leaves the board bytes and the mark restored, `result.error` naming the ORIGINAL failure, and no exception escaping the cleanup.
- **Priority:** high
- **Acceptance (black-box):** **Observable outcome:** a failed migration leaves the board untouched and unmarked, `result.error` naming the original failure (the backup/log removed best-effort per the offer's pattern), the app starting clean. **Shipped surface:** `run_link_migration`.
- **Acceptance test(s):** AT-901
- **Boundary catalog:** ☑ error (the refusing unlink)
- **Negative control:** the happy path converts and cleans up unchanged.

### HLR-902 — A non-text title never crashes
- **Traceability:** US-902
- **Ledger:** LED-2026-10-07-batch-03.1, LED-2026-10-07-batch-03.2
- **Statement:** When a board file carries a task whose title is not a string (a number, a list, a mapping), the system shall load it safely — coerced to the user's text when it is scalar (`5` -> `5`, `true` -> `True`), else the shipped `Untitled` convention (containers and null) — and never raise at load or render.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests -q -k junk_title`
- **Numeric pass threshold:** TC-902: boards with `"title": 5`, `"title": ["x"]`, `"title": {"a": 1}`, `"title": null`, `"title": true` load with the titles `5`, `Untitled`, `Untitled`, `Untitled`, `True` (exact strings); the data round-trips through save.
- **Priority:** medium
- **Acceptance (black-box):** **Observable outcome:** the bad board opens; the task shows a sane title. **Shipped surface:** `Board.load` to every view.
- **Acceptance test(s):** AT-902
- **Boundary catalog:** ☑ invalid (the three non-text shapes: list, dict, null)
- **Negative control:** a missing title keeps the shipped Untitled behavior.

### HLR-903 — The legend, the rule-only band, and milestones everywhere
- **Traceability:** US-903
- **Ledger:** LED-2026-10-07-batch-03.1, LED-2026-10-07-batch-03.2, LED-2026-10-07-batch-03.3
- **Statement:** The kanban `?` legend shall name `◆` on the band rule only when a band the screen DRAWS carries a milestone (filtered-out or folded bands do not count); a project whose only open items are milestones shall draw its band rule carrying them (D-623); a late milestone below the fold shall mark the fold row; and milestones shall render with their `◆` identity in lanes, agenda and focus, not as plain tasks.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests -q -k legend_band_milestone_views`
- **Numeric pass threshold:** AT-903's arms, each reading the PAINTED frame of the named view (C-32) on the shifted milestones board — arm 1 (K2-1): with a search query hiding every milestone-bearing band, the kanban `?` legend names no `◆` (and with one drawn, it does; ONE shared drawn-band computation serves the renderer and the legend — CL-7); arm 2 (D-623): a project whose only open items are milestones draws its rule-only band carrying `◆`, its head reading `N open` with N = the milestones (a project with no cards, no done, no visible milestones draws none); arm 3 (UX2-2): a late milestone (due before today, per `milestone_tone`) below the fold marks the fold row `▼ N below · ▲1 ◆` — the canonical `▼ N below` literal plus the late-milestone suffix, NOT the BACKLOG's pre-shipped `▾ N more` note (LED .3); arm 4 (the three views): lanes, agenda and focus each render a milestone row carrying `◆` — a marker only, no layout change to non-milestone rows (CL-9); and the swimlanes `?` legend names the milestone `◆` when a lane draws one (CL-5).
- **Priority:** medium
- **Acceptance (black-box):** **Observable outcome:** what the legend says is on screen is on screen; a milestones-only project keeps its band; milestones read as milestones in every view. **Shipped surface:** the kanban legend/fold, the band rule, lanes/agenda/focus.
- **Acceptance test(s):** AT-903
- **Boundary catalog:** ☑ empty (a project with no cards draws no band — unchanged) ☑ boundary (the fold marker at exactly-full)
- **Negative control:** a filter that empties the bands removes the legend entry.

### LLR-901.1 — Restore-first, cleanup best-effort
- **Traceability:** HLR-901
- **Ledger:** LED-2026-10-07-batch-03.1, LED-2026-10-07-batch-03.2
- **Statement:** `run_link_migration`'s failure path shall restore the board and the mark before any cleanup; the backup/log removal shall run in a nested guard that swallows its own errors; the original failure reaches `result.error` unchanged and no exception escapes.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests -q -k migration`
- **Numeric pass threshold:** TC-901 (the refusing-unlink arm; a RED mutation — cleanup before restore — must redden it).
- **Negative control:** TC-901's happy-path arm.
- **Boundary catalog:** ☑ error (the refusing unlink, post-write)

### LLR-902.1 — Coercion at the load boundary
- **Traceability:** HLR-902
- **Ledger:** LED-2026-10-07-batch-03.1, LED-2026-10-07-batch-03.2
- **Statement:** `Task.from_dict` shall coerce a non-text title: `str(value)` for scalars (the user's digits survive), `Untitled` for containers (list/dict) and null; no other field changes; the coercion is visible in the loaded task and the saved file.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests -q -k junk_title`
- **Numeric pass threshold:** TC-902's three shapes.
- **Negative control:** a missing title is unchanged.
- **Boundary catalog:** ☑ invalid (list, dict, null — the three non-text shapes)

### LLR-903.1 — Legend, band, fold, and the three views
- **Traceability:** HLR-903
- **Ledger:** LED-2026-10-07-batch-03.1, LED-2026-10-07-batch-03.2, LED-2026-10-07-batch-03.3
- **Statement:** `legend_entries("kanban")` shall admit the `◆` band-rule entry only for drawn bands (the filter/fold context — ONE shared drawn-band computation, `_fold_keep`, serves the renderer and the legend, CL-7); a milestones-only project draws its rule-only band (D-623); the fold row marks a late milestone below the fold with the canonical `▼ N below` literal + the ` · ▲N ◆` suffix (LED .3); lanes/agenda/focus render a milestone with its `◆` identity.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests -q -k legend_band_milestone_views`
- **Numeric pass threshold:** AT-903's arms.
- **Negative control:** the filter-empty arm.
- **Boundary catalog:** ☑ empty ☑ boundary (the exactly-full fold).

### Information Flow Contract (IFC)

Part A (no new flow; the one touched flow, named so its nodes stay owned):

```
FLOW: the board file through the hardened boundaries, back to the board file
  SOURCE : the board file on disk (tasks, titles, links, the migration mark); teammates' pushes
  NODES  :
    - fn    : Task.from_dict / _coerce_title (the S-9 boundary)
      owner : LLR-902.1
    - fn    : run_link_migration (the restore-first failure path)
      owner : LLR-901.1
    - fn    : legend_entries("kanban") / the band-rule facts / the fold row / the lanes-agenda-focus renderers
      owner : LLR-903.1
  SINK   : the loaded board, the restored board on failure, the painted views, the saved board
```

Part B: `no — no new addressable component.`

## 5. Validation strategy

Layer A (`TC-901`, `TC-902` — unit) and Layer B (`AT-901`, `AT-902`, `AT-903` — the app layer,
real surfaces) per the thresholds above; the fold-canon literal is additionally pinned by the
7-fold TC-311 census (tests/test_kanban_readable.py). The §5.2 criteria: every HLR has a passing
AT, every LLR a passing TC; 0 suite failures other than the declared G-011 flake.

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

### 5.2 Batch acceptance criteria
- 100% of LLRs (3/3) covered by at least one passing TC with pass result — TC-901, TC-902, and AT-903's arms + the TC-311 census for LLR-903.1's fold literal.
- 0 blocker fails in validation — the close suite reports 2541 passed, 0 failed (the orchestrator's single run; G-011 did not fire).
- Every user story has ≥1 passing `AT-NNN` through the shipped surface with boundary + negative evidence — AT-901 (happy-path + refusing-unlink arms), AT-902 (missing-key arm), AT-903 (the filter-empty negative, the exactly-full boundary, the four arms).
- Every HLR declares its `Acceptance test(s)` and every acceptance-bearing requirement its `Negative control` + `Boundary catalog` (the V33–V35 scope); no requirement carries a modal `should`.
- No requirement without an assigned validation method — all six blocks declare `Validation`.

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
