# Design proposal — taskboard — Batch 2026-10-18-batch-02

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
| Id | `PDR-2026-10-18-batch-02` |
| Requirements covered | HLR-1901..HLR-1905 · LLR-1901.1, LLR-1902.1, LLR-1903.1, LLR-1904.1, LLR-1905.1 (as amended by LED-2026-10-18-batch-02.2) |
| Modules touched (from `docs/ARCHITECTURE.md`) | `views` (`taskboard/views.py`), `app` (`taskboard/app.py`), `tests`, `prototypes` |
| Triggers that fired | A2 · A3 · B1 · B3 · B4 · D1 · E1 |
| Author / reviewers | orchestrator (author) · `architect` · `qa-reviewer` · `ux-reviewer` |

---

## 1 · Objective and scope

Build what HLR-1901..1905 ask in three increments: (001) the suite's two standup tests and its clipboard roundtrip test fixed test-side, the six stale round files marked `HISTORICAL`; (002) the presentation's narrow mode below `PRESENT_MIN_WIDTH` — the frame's rung, the key guard, the export notice — and the hint's four wordings and cut; (003) the polish round. **Not done:** any change to `render_standup` or `grab_clipboard_text`; any change to the frame at 36 columns and above; any production change for the three polish items.

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `views` | the narrow branch of `render_present`; `PRESENT_MIN_WIDTH`, `PRESENT_NARROW` | `PRESENT_MIN_WIDTH` (to `app`) | the screen's state; keys |
| `app` | `PresentScreen._narrow`, the guards in its seven actions, `_hint` | — | rendering the frame (calls `render_present`) |
| `tests` | the repaired nodes, the new TC/AT nodes, `_clipboard_roundtrip` | — | patching product symbols in an AT |
| `prototypes` | `backlog_polish/` (capture, forks, page) | — | writing anything under `taskboard/` |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ (the `PRESENT_MIN_WIDTH` row and the round's forks were added at ARQ / LED .2)

## 3 · Diagrams

State dynamics of `PresentScreen` against its width (the one viewpoint that applies):

```
           width >= 36                         width < 36
  ┌──────────────────────────┐  resize   ┌───────────────────────────┐
  │ wide: the views' frame;  │ ────────▶ │ narrow: one mut rung;     │
  │ every key acts; x exports│ ◀──────── │ only esc acts; x notifies │
  └──────────────────────────┘  resize   └───────────────────────────┘
   state (view, cursor, page, hidden) is untouched in narrow, so widening repaints it as it was
   (a resize resets the page, as shipped — LED .5 of 2026-10-18-batch-01)
```

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `render_present(...)` | raises below 36 | every width ≥ 0: below 36 the narrow rung | `app.PresentScreen`, tests, prototypes | no — one lane |
| `PRESENT_MIN_WIDTH` | — | `36` | `app.PresentScreen`, tests | no — one lane |

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-1901 | A | the two repaired standup nodes + the 12/13-cell name-cell arm | `is_self` → muted spine (`prefix = c("▌", "bright")…` swapped); the stale tone on every row (`tone = "over"`) |
| AT-1901 | B | key `8`: `▌ username_su…`, `▎ Ana` | the same spine swap |
| TC-1902 | 0 | the helper's seven arms (pass, skip on refusal ×5, refusal then pass, contention ×5 fails, refusal ×4 then contention fails, a disturbing reader fails, mismatch fails) | a refusal raises instead of returning; contention returns a reason; a mismatch returns a reason |
| AT-1902 | B | the real test body under a refusing `_ps` → skip quoting the refusal, 5 seeds, the restore | the skip replaced by `pytest.fail(reason)`; on `base_ref` the SETUP assert |
| TC-1903 | 0/A | the width × height × view × cursor × scroll × board sweep; the rung table; `mut` | threshold 36 → 35 and → 37; a rung dropped; `"mut"` → `"dim"` |
| AT-1903 | B | the resize ladder 60 … 1, the keys at 30 change nothing, `x` notifies and writes nothing, back at 118 the kept frame | a guard removed from `action_hide` (the board written); the export guard removed (an SVG in `reports/`) |
| TC-1904 | 0 | the hint over widths 1–140 × views × 0/3/10 hidden against the literal threshold table; bold span | the compact wording removed; `hint.truncate` removed; the `room <= 0` guard removed; the narrow branch keeping the names |
| AT-1904 | B | 50/40/30/15 columns with 3 hidden, both views, the bold span | the compact wording removed (50 columns shows `esc`); the narrow branch removed |
| AT-1905 | B | the page, the manifest, the captures, the variants differ, `data-recommend`, three RED arms on copies | its own arms: a capture moved aside, a variant equal to the current look, an external `href` |

**Declared here, at authoring time, not at execution time.** A proposed case whose reddening mutation
cannot be named is not yet a test case — it is a hope. Layer 0 applies where the unit has cyclomatic
complexity ≥3 **or** transforms data crossing a declared module boundary.

**5b · The gauntlet controls that apply, and who pays:** C-40 (each new assertion RED by a recorded mutation — the orchestrator, `mutate.py` per increment); C-19 (one complete suite run per increment and at P4 — the orchestrator); C-20 (the RED of a new test file by move-aside on a `git archive` export of `base_ref` — the orchestrator); C-42 (AT-1903 reads the exported-or-not `reports/` on disk and the notification text as Textual holds it; AT-1905 reads the SVG text with `&#160;` as a space — the author); C-26 (the reverse census per packet — the author).

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| a narrow gantt layout below 36 (drop the chip, shrink the label) | a design change to the frame needing a prototype round; the commission asked only for no crash |
| `x` below 36 exports at the 118×31 reference size | changes what `x` means (the frame on screen) and writes a frame nobody saw; the notice tells the presenter what to do (UX-5) |
| contention ×5 as a skip | hides a reader that disturbs the clipboard (QA-2) |
| repairing the six round files' imports | their recorded outputs came from the deleted helpers; a repaired script would not reproduce them (PLAN §Key decisions) |
| lifting the polish literals into module constants so the round can patch them | a production change made for a prototype (ARCHITECTURE §3) |

Risk: the narrow rungs, the guard and the compact wording are UI the operator has not seen — shown in the round (HLR-1905) at 30×12 and 50×20.

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | §1, §3 and §4 here → increments 001–003's packets §1 |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | the 12-task project built in TC-1904 from `tests/present_board.py`; `tests/present_notes_board.py` for the ATs and the round; Edge for the round's PNGs |
| proposed test cases | layers 0/A/B and the DDR | §5 → the packets' §4 `Mutation verdicts`; the DDR's checklist row 4 |
| design → requirement traceability | the matrix and the DDR | §5's Id column ↔ `01-requirements.md` §3/§4; the packets' §2 `Traces to` |

- ⚠ Any row whose consumer column is empty: **remove the output, or explain why it is being produced.**
