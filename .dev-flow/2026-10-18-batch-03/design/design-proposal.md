# Design proposal — taskboard — Batch 2026-10-18-batch-03

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language
> The normative rules below are language-independent. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Design proposal` · `7 · Forward-applicability table` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **Why a HEADING is reserved here and a FIELD NAME everywhere else:** `C-49`'s artifact is the §7 TABLE, and a rule that read a summary bullet instead of the rows would be reading a claim about the table rather than the table. `V52` therefore keys on this document's own H1 and on the §7 heading, which is why both are on the machine plane. **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`.

> **Owed in.** `core` by trigger · `full` ✓
> **Source:** `/dev-flow-init` step 4's seed-by-level table, which is this fact's one home. A level marked `—` **does not owe this artifact, and its absence is not an omission**; `by trigger` means the station exists only when the `triggers` block fired, and `stations_active` in `state.json` is the authority for *this* batch. Where a SECTION or a gate row is owed more narrowly than the artifact, it says so on the row.

> **Where this lives: the VAULT + Drive**, not the repo — it is deliberation, and its traceability to
> code is weak. It is **cited by id** from the repo (`PDR-<batch_id>#D<n>`), never copied.
> What binds code — a frozen interface, a design characteristic — also lands in the **repo**, in the
> requirement or in `docs/ARCHITECTURE.md`. *The vault keeps the deliberation; the repo keeps the commitment.*

> **The forward-applicability rule (ISO/IEC/IEEE 15288).** Everything below must be NAMED as the input
> of a later activity. **If a section of this proposal is nobody's input, delete it — it does not belong
> in the PDR.** That rule is what allows this document to cost half the batch without being waste.

| Field | Value |
|---|---|
| Id | `PDR-2026-10-18-batch-03` |
| Requirements covered | HLR-2001..HLR-2003 · LLR-2001.1, LLR-2002.1, LLR-2003.1 (LED-2026-10-18-batch-03.1 and its P2 amendment LED .2) |
| Modules touched (from `docs/ARCHITECTURE.md`) | `views` (`taskboard/views.py`), `app` (`taskboard/app.py`), `tests`, `docs` |
| Triggers that fired | A2 · B1 · B3 · B4 · D1 · E1 |
| Author / reviewers | orchestrator (author) · `architect` · `qa-reviewer` · `ux-reviewer` |

---

## 1 · Objective and scope

Port variant A of the three approved polish items from the round's code, one increment each: (001) `"dim"` → `"reached"` at the four quiet-mark sites — `render_present`'s view word, `_present_cut`'s one-row tag and `… +N lines` row, `_present_mark`; (002) the round's `HINT_A` tuple inserted in `PresentScreen._hint`'s wordings after the long one; (003) the gantt branch's `_present_cut(rows, 3, width - 6)` → `_present_cut(rows, max(3, height - len(lines) - len(open_t)), width - 6)`, `lines` taken before the brief loop, and `render_present`'s docstring. **Not done:** any other `dim` site (`no notes`, the separators, the `· ` lead, `+N more rows not shown`, `no project to present`), the hint's inactive view name (`#5b6675`), the split view's allocation, the narrow frame, the hint's other wordings, the round's files, the PRES-V3 files.

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `views` | the four tone literals; the gantt note's row count | `render_present` (unchanged signature) | the screen's state; keys |
| `app` | `PresentScreen._hint`'s wording list | — | rendering the frame (calls `render_present`) |
| `tests` | `tests/test_present_polish.py` (new); the law-driven updates of TC-1807, TC-1808, TC-1904, TC-1604's 80-column arm | — | importing `prototypes/` code (they read the round's frames as FILES) |
| `docs` | `docs/ARCHITECTURE.md` (ARQ amendment) | — | — |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ (no row moves; the `render_present` contract cell and the `prototypes`/`tests` rows amended at ARQ)

## 3 · Diagrams

The gantt view's frame, top to bottom, and where the note's rows come from (the one viewpoint that changes):

```
  header (1) · ruler (2) · span row (1) · task rows (n) · rule (1)   = len(lines) before the briefs
  brief rows (n), the cursor's note under its brief                   = len(open_t) more
  note rows k = max(3, height - len(lines) - len(open_t))            -> fills to the last row
  k >= rows of the note: shown whole;  k < rows: k - 1 rows + "… +N lines" (N = rows - k + 1)
  height - len(lines) - len(open_t) < 3: k = 3 and the frame overflows as shipped ("+N more rows not shown")
```

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `render_present(...)` | quiet marks `dim`; gantt note 3 rows | quiet marks `reached`; gantt note the free rows, 3 at least; signature and frame shape unchanged | `app.PresentScreen`, tests, prototypes (frozen) | no — one lane |

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-2001 | A | the sweep: every view word (where the header keeps its tones), cut and edge mark `reached`, never `dim`; the lead, `no notes`, the overflow row `dim`; every kind met; the one-row cut at 60×20; `no project to present` `dim`; the contrast ordering dim < 4.5 ≤ reached < mut | each of the four sites kept `"dim"` (four mutants); the `· ` lead repainted `"reached"` |
| AT-2001 | B | 80×25, `R`, `→ →`: `gantt` and `… +N lines` `#7a828c`, the lead `#5b6675`; `2`: the split view's marks `#7a828c` | the view word kept `dim`; `_present_cut`'s row kept `dim`; `_present_mark` kept `dim` |
| TC-2002 | 0 | for both views × 0/1/3/10 hidden: the middle wording at its first width and one below the long one's, the short one a column narrower, the long one at its first width | the middle wording removed; tried before the long one; its gap one space |
| TC-1904 (updated) | 0 | the threshold sweep with the middle tier | the middle wording removed |
| AT-2002 | B | 80×25: the middle wording in both views (78 cells in split), bold current view, the short one with one hidden; 118: the long one | the middle wording removed; its keys changed |
| TC-2003 | A | the long note's frames equal `PRES-V4-gantt-notes-*` (the round's output); the sweep: where the frame holds the note, `min(n, max(3, height - L))` note rows, a cut note leaves no blank row and ends on `· … +N lines`; where it does not, the floor of 3 and the shipped overflow row; the room-equals-note and one-row-more boundaries met; no note for a task without notes | the cap kept at 3; the floor dropped (`max(0, …)`); the brief rows not subtracted |
| AT-2003 | B | 80×25 and 118×31, `→ →`: the frame equals the round's frame; at 80 no blank row and `… +5 lines` above the last brief; at 118 no cut | the cap kept at 3; the brief rows not subtracted |

**Declared here, at authoring time, not at execution time.** A proposed case whose reddening mutation
cannot be named is not yet a test case — it is a hope. Layer 0 applies where the unit has cyclomatic
complexity ≥3 **or** transforms data crossing a declared module boundary.

**5b · The gauntlet controls that apply, and who pays:** C-40 (each new assertion RED on `base_ref` and by a recorded mutation — the orchestrator, `evidence/mutate.py` per increment); C-19 (one complete suite run per increment and at P4 — the orchestrator); C-20 (the RED of the new nodes on a `base_ref` worktree — the orchestrator); C-42 (the ATs read the frame and the hint as Textual holds them, with their `Text` spans); the round comparison (`evidence/port_captures.py`, the round's code on `base_ref` as oracle — the orchestrator, after each increment).

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| repaint every `dim` mark of the presentation | not what A showed: the round kept the lattice, `no notes` and the lead `dim` (`capture.py` `_QUIET`) |
| lift the four tones into one module constant | a refactor beyond the verdict; four literals at four sites is what the code does elsewhere |
| fill computed by rendering twice (the round's `cap_fork`) | a fork's technique; the arithmetic is the same on every frame (P-4) and costs one render |
| rewrite the PRES-V3 gantt-notes frames | their hashes are recorded; new frames go in new files (the commission) |
| retire the round folder in this batch (AT-1905's rule) | no deletion is commissioned and the round is the port's oracle; handed to the operator |

Risks: the law-driven updates of shipped tests (TC-1807, TC-1808, TC-1904, TC-1604) — each named old → new in its packet's census, the new values from P-3 or the round's frames. With the fill, the gantt view shows more of the cursor's note than the split view gives it when every note shares the room (ux-reviewer UX-1) — variant A as approved, recorded for the operator in `BACKLOG.md`.

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | §1, §3 and §4 here → increments 001–003's packets §1 |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | `tests/present_board.py`, `tests/present_notes_board.py` (the boards); the 12-task project of `tests/test_present_narrow.py::_screen` (TC-2002); `evidence/frames/PRES-V4-gantt-notes-*.txt` and `evidence/expected/` (the round's oracle); the `base_ref` worktree for the REDs; Edge for the PNGs |
| proposed test cases | layers 0/A/B and the DDR | §5 → the packets' §4 `Mutation verdicts`; the DDR's checklist |
| design → requirement traceability | the matrix and the DDR | §5's Id column ↔ `01-requirements.md` §3/§4; the packets' §2 `Traces to` |

- ⚠ Any row whose consumer column is empty: **remove the output, or explain why it is being produced.**

## 8 · Parallelisation plan *(only if the batch forks)*

none — one lane, three increments in order.
