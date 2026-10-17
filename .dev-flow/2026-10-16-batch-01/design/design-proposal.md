# Design proposal — taskboard — Batch 2026-10-16-batch-01

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
> code is weak. It is **cited by id** from the repo (`PDR-2026-10-16-batch-01#D1`), never copied.
> What binds code — a frozen interface, a design characteristic — also lands in the **repo**, in the
> requirement or in `docs/ARCHITECTURE.md`. *The vault keeps the deliberation; the repo keeps the commitment.*

> **The forward-applicability rule (ISO/IEC/IEEE 15288).** Everything below must be NAMED as the input
> of a later activity. **If a section of this proposal is nobody's input, delete it — it does not belong
> in the PDR.** That rule is what allows this document to cost half the batch without being waste.

| Field | Value |
|---|---|
| Id | `PDR-2026-10-16-batch-01` |
| Requirements covered | HLR-1601 (LLR-1601.1, LLR-1601.2) · HLR-1602 (LLR-1602.1, LLR-1602.2, LLR-1602.3) · HLR-1603 (LLR-1603.1, LLR-1603.2) |
| Modules touched (from `docs/ARCHITECTURE.md`) | `taskboard/**` — layers `views`, `models`, `app`, `modals`, `keymap` |
| Triggers that fired | A2 · A3 · B1 · B4 · C8 · D1 · E1 |
| Author / reviewers | `architect` · `qa-reviewer` · `ux-reviewer` |

---

## 1 · Objective and scope

Realise HLR-1601/1602/1603 as the prototype round proved them, inside the shipped seams: the ruler is the gantt view's own builders re-seated in the present columns; the chip is one label function; the hide flag is one `Task` field omitted at its default; the help fix is a grid band plus a docked footer derived from `KEYMAP`. NOT in scope: the header's ` — hybrid` suffix and the in-frame keys row (kept as shipped; the prototype's app capture dropped both — named for the operator's verdict, not changed), weekend shading on the present field, undo for the flag, any change to the gantt view's output.

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `views` | the ruler rows, the chip label, the shown/hidden filter (`present_tasks`, `present_hidden`), the `shade_weekends` keyword | `render_present`, `present_span_label`, `present_tasks`, `present_hidden`, `gantt_day_row(..., shade_weekends=True)` | the board file (it never saves), keys |
| `models` | `Task.show_in_present` (and its entry in `_TASK_KEYS`), its read and its omission on write | the field; `Board.save` byte-identity for shown tasks | markup |
| `app` | `PresentScreen`'s `space`/`a` bindings, the save after a flag change, the hint row | `PresentScreen` | rendering the frame (delegates to `views`) |
| `modals` | the `Show in presentation` checkbox; the help modal's Keys band and pinned global line | `TaskModal`, `HelpModal` | the key seat's contents (reads `keymap`) |
| `keymap` | `global_keys(view)` | the accessor | — |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ (no new edge: `views` stays pure, `app` saves, `modals` reads `keymap`).

## 3 · Diagrams

State (the presentation's cursor over shown tasks):

```
open R      ──▶ cursor = selected task if shown & open, else the first shown open task, else none
space       ──▶ cursor none: no-op, writes nothing
                else: flag off on the cursor task, save, cursor = next shown by due
                      (previous at the end; none when it was the last shown)
a           ──▶ nothing hidden: no-op, writes nothing
                else: every hidden task's flag on, save; cursor stays on its task,
                      or (cursor none) = the first shown open task
←→↑↓        ──▶ cursor walks the shown open tasks; hidden ones are not stops
```

Layout (present columns, both widths): `label(30|20) · gutter(1) · field(w-label-15) · space(1) · chip(13)`; ruler rows put the label text right-aligned in the label column and blanks under the chip.

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `gantt_day_row(ax, today, echo)` | shades weekends always | `+ *, shade_weekends: bool = True` | gantt view (default, unchanged), presentation (`False`) | n/a — one lane |
| `present_tasks(board, pid)` | every visible task | shown tasks only; `present_hidden` beside it | `PresentScreen`, tests | n/a |
| `present_span_label(start, due) -> str` | — (`_present_chip(due_iso, today, width, wide)` drew the due + distance) | new `views` export, the chip text; `_present_chip` removed (its only callers are the two field rows) | `render_present`, tests | n/a |
| `board.json` task record | no such key | `"show_in_present": false` on hidden tasks only | `team_sync` push, older app versions (an unknown key round-trips through `extra`) | n/a |
| `TaskModal` result | 14 keys | `+ show_in_present` | `app._on_task_added` (`Task(**data)`), `_on_task_edited` (`setattr`) | n/a |
| `keymap` | — | `global_keys(view)` | `HelpModal` | n/a |

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-1001 / TC-1002 | A | the frame equals `evidence/frames/PRES-R-118x30.txt` / `PRES-R-80x24.txt` (this batch) | chip_w 13 → 12; the ruler rows not appended |
| AT-1001 (frame arm, repointed) | B | `R` through the app paints `PRES-R-118x30.txt`; its zero-saves arm unchanged | the ruler rows not appended |
| TC-1601 | 0 | today's cells `accent`; the echo `bright` on a future cursor task and `over` on the past-due oracle cursor; no weekend background in the frame (the window spans Sep–Oct weekends); a project with no open task still paints both ruler rows; the gantt default still shades weekends | `shade_weekends=False` → `True` in `render_present`; the echo tone forced `bright`; today `accent` → `bright` |
| TC-1602 | 0 | the six labels, cross-year `Dec 28–Jan 3`, an unparseable date read as absent, the three tones; the oracle board's chips as literals (`Aug 21–Oct 10`, `Sep 5–27`, `Sep 24–28`, `due Oct 6`, `Oct 4–10`, `due Oct 14`); `Aug 21–Oct 10` whole at chip 13 | same-month branch returns `<Mon D>–<Mon D>`; chip_w 12 |
| AT-1601 | B | `R` on the oracle board: the month row names `September`, the tick row carries the cursor's dates, each field row ends in its literal chip; `→` moves the dates on the tick row | the ruler rows not appended |
| TC-1603 | 0 | round-trip byte identity with no hidden task; `false` written only for the hidden one; `"no"` and `0` load as shown and are dropped on save; hide-then-show leaves no key and nothing in `extra` | drop the omission in `_to_dict`; `is not False` → `bool(...)` (RED on the `0` arm: `bool(0)` hides); drop the key from `_TASK_KEYS` (RED on the `extra` arm) |
| TC-1604 | A | (a) `present_tasks` excludes hidden, `present_hidden` lists them; (b) hiding `tw6` (latest due) narrows the axis; (c) `space` moves the cursor to the next task by due; (d) hiding the last shown moves it up; (e) all hidden: the frame paints header, ruler (scale label), span, separator, keys row, no brief row; (f) `space` with all hidden writes nothing; (g) `a` with nothing hidden writes nothing; (h) all hidden → `a` → a cursor task is painted; (i) `a` in the presentation opens no editor; (j) the hint texts at 118 and 80 plus `· n hidden`, n = `len(present_hidden)`; (k) the frame never holds `hidden` | (a) filter removed; (b) axis over all open tasks; (c) cursor reset to the first task; (e) brief rows painted for hidden; (f)(g) always save; (h) cursor left none; (i) `priority=False`; (j)(k) count rendered in the frame |
| TC-1605 | A | at 80×24 `f-present` is fully painted and `space` on it toggles it; unchecking + Save writes the flag; a new task starts checked; `#f-title` keeps ≥ 20 painted cells at 80; `TASK_CHIPS_ONE_ROW` stays 137 | the result dict drops `show_in_present`; `#f-title` `1fr` → `auto` |
| AT-1602 | B | `R`, `space` → the cursor task's title gone, hint `· 1 hidden`, `board.json` differs only by the flag; `x` → the SVG holds no `hidden`, not the hidden title, the open count one lower; restart + `R` → still hidden; `a` → back, file bytes equal the original | `space` without save; the export rendered from the unfiltered list |
| TC-1606 | 0 | the grid: every key once; column-major on 7 keys at a width for 3 columns; no line wider than the inner width; inner width < one cell → one column | row-major fill |
| TC-1607 | 0 | `global_keys` = exactly the live `bar=False` entries in seat order, including one monkeypatched into `KEYMAP` for the test; the packed line's row count at 104 and 70 computed from those entries; no entry split across rows | a hand-typed list (RED on the injected key); wrap mid-entry |
| AT-1603 | B | `?` in the gantt view at 118×30 and 80×24: the compositor's rows hold `R Present` and `S Standup` unscrolled; the Keys band, scrolled into view, paints hard-coded gantt pairs whole | the footer inside the scroll area (80×24 pushes it off-screen) |

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| store the flag in `task.extra["present"]` (the prototype's seam) | `extra` is the preserved-unknown-keys bag; a modelled flag belongs on the dataclass where the editor and `setattr` reach it |
| always write `show_in_present` (plain `asdict`) | every existing board would change bytes on its next save (P-2) |
| paint today `bright` on the ruler (the prototype's C-2b budget) | the operator chose accent («Se ve mejor en acento») |
| the global keys in the left column (the first legend prototype) | the 118×40 capture clipped that block exactly at `R` and `S` |
| a hand-typed global list in the help | drifts the moment a key is added (P-4) |

Editor placement: the checkbox goes in the title row (`#task-head`, after the `1fr` title input) — the chip row's folded form already needs exactly 80 columns (`modals.py` `TASK_CHIPS_ONE_ROW` comment) and the actions column is 16 wide; the title row is the only row with spare width at 80. Spike evidence for the help footer: a `dock: bottom` label inside `#help-modal-box` stays inside the box at 80×24 (box inner width 70) and 118×30 (104).

Footer layout: two docked rows — the global line (entries joined by two spaces, ~101 cells: one row at 118×30's inner 104, two rows at 80×24's inner 70, wrapped at entry boundaries) and the hint on its own row. The Keys band stays inside the scrolled body (P2 A-1: it cannot fit unscrolled at 80×24).

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | increments 001 (§2 views), 002 (models/app/modals/views), 003 (modals/keymap) — their packets' §1 |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | `tests/present_board.py` (oracle board, reused); `evidence/gen_frames.py` (the oracle generator + `render_b2` cross-check) — written by increment 001 BEFORE TC-1001/1002 are repointed; `evidence/capture_app.py` (the app captures) — written by increment 001, extended by 002 and 003 |
| proposed test cases | layers 0/A/B and the DDR | §5 above → `tests/test_present_rulers.py`, `tests/test_present_hide.py`, `tests/test_help_keys.py`; the DDR re-reads each mutation verdict |
| design → requirement traceability | the matrix and the DDR | §5's Id column ↔ `01-requirements.md` LLR `Executed verification` |

## 8 · Parallelisation plan *(only if the batch forks)*

n/a — one lane.
