# Design proposal — taskboard — Batch 2026-10-18-batch-01

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
> code is weak. It is **cited by id** from the repo (`PDR-2026-10-18-batch-01#D1`), never copied.
> What binds code — a frozen interface, a design characteristic — also lands in the **repo**, in the
> requirement or in `docs/ARCHITECTURE.md`. *The vault keeps the deliberation; the repo keeps the commitment.*

> **The forward-applicability rule (ISO/IEC/IEEE 15288).** Everything below must be NAMED as the input
> of a later activity. **If a section of this proposal is nobody's input, delete it — it does not belong
> in the PDR.** That rule is what allows this document to cost half the batch without being waste.

| Field | Value |
|---|---|
| Id | `PDR-2026-10-18-batch-01` |
| Requirements covered | HLR-1801 (LLR-1801.1, LLR-1801.2) · HLR-1802 (LLR-1802.1) · HLR-1803 (LLR-1801.3, LLR-1803.1, LLR-1803.2, LLR-1803.3) |
| Modules touched (from `docs/ARCHITECTURE.md`) | `taskboard/**` — layers `views`, `app`; `tests`, `docs`, `dev-flow record`, `prototypes` (committed unmodified) |
| Triggers that fired | A2 · A3 · B1 · B3 · B4 · C8 · D1 · E1 |
| Author / reviewers | `architect` · `qa-reviewer` · `ux-reviewer` · `security-reviewer` (C8, at P2) |

---

## 1 · Objective and scope

Port the approved prototype faithfully: D2 · stacked (`prototypes/present_views/views_d.py` `alloc`, `_clipped`, `_heading`, `_stack_column`, `render_stacked`, with `views_proto.py` `wrap_notes`, `_note_markup`, `_scrolled`) and the fixed gantt branch (`views_d.render_gantt`) into `taskboard/views.py`, as one renderer with a `view` argument; give `PresentScreen` the prototype's keys (`1`/`2`, `tab`/`shift+tab`, `pgdn`/`pgup`) with the view and the page held on the screen, never persisted. Deltas from the prototype, each from the brief or a P2 finding: two views instead of four (the hint names `1 gantt  2 split`); paging by tiled pages instead of a 5-row step (UX-1) and the area scroll when no cursor note can scroll (the brief); ` … +N lines` on a one-row cut (the brief, UX-4); the cursor keeps one row below the per-note floor and a column's overflow ends on `↓ N more lines` (QA-1); nothing under the rule with every task hidden (UX-5); `N. ` items up to three digits; the export of the split view to `-split` files. NOT in scope: views C (slide) and B (cards); images; remembering the view.

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `views` | the note wrapper, the share, the blocks, the columns, the paging, the gantt note rows, the header's view word, the export names | `render_present(..., view, scroll)`, `PRESENT_VIEWS`, `present_note_lines`, `present_alloc`, `present_paths(..., view)` | keys, the screen's state, the board file (it never saves) |
| `app` | `PresentScreen`: the six bindings, `_view`, `_scroll`, `_frame_text`, `_hint`, the same-frame guard on `pgdn`, the export of the current view | `PresentScreen` | rendering (delegates to `views`), the `KEYMAP` seat (the presentation's keys are its own, ARCHITECTURE §5) |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ (no new edge: `views` stays pure; `app` already imported `views`; `prototypes` → `taskboard` private names declared in §3 of the map).

## 3 · Diagrams

State (the presentation's view and page; the cursor and the hidden set as shipped):

```
R            ──▶ view = gantt, page = 0
1 / 2        ──▶ view = gantt / split, page = 0
tab / ⇧tab   ──▶ view = next / previous (wrapping), page = 0
pgdn         ──▶ gantt: nothing
                 split: if the frame at page+1 == the frame now: nothing  (the last page)
                        else page += 1
pgup         ──▶ page = max(0, page - 1)
←→↑↓ space a ──▶ as shipped (cursor, hide, show all) and page = 0
x            ──▶ write the current view's frame to present-<slug>-<date>[-split].svg/.png
```

Paging (PDR UX PC-1): when page 0 windowed a column onto the cursor's block, the whole-text paging starts at the first block page 0 showed, so the first `pgdn` never moves the text back to the top.

Split layout: `header · 2 ruler rows · span row · n field rows · rule` then `room` rows; at `width ≥ 100` two columns of `(width − 5) // 2` (`" " + left + " │ " + right`), else one of `width − 2`; per column the blocks `heading + note rows (present_alloc)`; page `p` per column: the cursor's note paged (`note_scrolls`: cut and ≥ 3 rows) or, when no cursor note in the frame can scroll, page `p − 1` of the column's whole text.

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `render_present(board, project_id, cursor_id, today, width, height)` | the gantt frame | `+ view="gantt", scroll=0`; `view` one of `PRESENT_VIEWS`; the header names the view | `PresentScreen` (paint, export, the same-frame guard), tests, prototypes | n/a — one lane |
| `PRESENT_VIEWS` | — | `("gantt", "split")` | `PresentScreen`, tests | n/a |
| `present_note_lines(notes, w)`, `present_alloc(ns, cur, room, floor_n=2)` | — (`_present_note_lines`, `_present_note_row`, deleted) | new `views` exports | `render_present`, tests | n/a |
| `present_paths(board, project_name, today=None)` | one name | `+ view="gantt"`: `-<view>` for any other view | `PresentScreen.action_export`, tests | n/a |
| `PresentScreen` hint text | `←→ ↑↓ move · …` | `1 gantt  2 split  [pgdn notes · ]⇥ next · …`, long or short by fit | `tests/test_present_hide.py` (TC-1604), `tests/test_present_views_app.py` | n/a |

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-1801 | 0 | the wrapper's ten exact rows: breaks, three bullet forms, `1.`/`12.` with a hanging wrap, a collapsed blank run; empty / `None` → `[]` | the line split removed (M1); `- ` kept (M2); one digit only (M3) |
| TC-1802 | 0 | `present_alloc`'s nine rows exact (among them `([5,6,3,13,0], 0, 6) → [3,1,1,1,0]`, where the half-room promise binds); ≥ 1 row per note when the room holds it; a cursor with notes always ≥ 1 | the cursor's half dropped (M5, the room-6 row); the below-floor row removed (M15) |
| TC-1803 | A | the four PRES-V3 split frames (118×30, 80×24; cursors `tw3`, `tw5`); the split top equals the gantt top | the cut mark removed (M6); the no-notes word removed (M7); the one-row unit dropped (M16) |
| TC-1804 | A | every noted task's text at nine sizes × every cursor; `no notes`; a per-block cut mark; `│` iff ≥ 100; below the floor the cursor's block in view with its note and an edge mark; all hidden → blank under the rule; hidden/done in neither part; the cursor's note longer as the cursor's (a regression pin: the surplus alone also lengthens it) | two columns only above 100 (M4); the cursor's block windowed out (M18); all-hidden columns painted (M17) |
| TC-1805 | A | markup in notes and titles literal in both views, at the one-row cut, a paged note, a markup cursor title, `\` and `\[` | a note row's escape dropped (M8) |
| TC-1806 | A | page 1 of the cut cursor note `↑ 3 lines above`; page 999 its last line; paging shows every row (4 sizes); the area scroll at 60×20; after a page 0 windowed onto the cursor, page 1 never moves back to the top (80×18); gantt ignores scroll; every frame exact | note paging ignored (M9); the area branch removed (M10); page 1 skips the top (M11); a page jumps rows (M14); the first page down jumps back (M19) |
| TC-1807 | A | the gantt-notes frames; 3 rows, `1. Feature-flag` on its own row, `… +N lines`; the header word, no key word | 4 rows (M12); the view word dropped (M13) |
| TC-1001 / TC-1002 / AT-1001 | A / B | repointed to `PRES-V3-gantt-118x30.txt` / `-80x24.txt` | the view word dropped (M13) |
| TC-1808 | A | the hint at five widths × three states, exact; bold on the current view; within `w − 2` | pgdn in the gantt hint (N4); bold on the other view (N5); `w >= 100` instead of fit (N11) |
| TC-1809 | 0 | `present_paths` names per view | the suffix dropped (N6); the suffix on gantt (N7) |
| TC-1810 | A | the six priority bindings; the app's `1`/`2` non-priority and `tab` released; view 0 / page 0 at open; page stepping and its stop; a move resets the page | `2` loses priority (N1); the same-frame guard removed (N2); a move keeps the page (N3) |
| AT-1801 | B | `R`, `2` → the split frame; every noted task's first words after each of five cursor positions; the cursor's block accented | (base: no `2`) |
| AT-1802 | B | `R` opens on `gantt`; `→ →` → the gantt-notes frame, `1. Feature-flag` on its own row | `R` opens on split (N8) |
| AT-1803 | B | the view keys, the shared cursor and hidden set, `pgdn`/`pgup`, the two exports by literal path, no key word in frame or SVG, reopen on gantt, 2 saves | the guard removed (N2); split export to the gantt file (N6, N9); `tab` clamps instead of wrapping (N10) |

### 5b · The gauntlet controls that apply, and who pays for them (PDR PC-A1)

| Control | Applies because | Paid by |
|---|---|---|
| RED on the base tree for every new and repointed node (C-40) | every TC/AT here is new or repointed | each increment: `evidence/red-001.txt`, `evidence/red-002.txt`, run on a `git archive 6ddea9f` export |
| the mutation battery, one verdict per arm, restore by digest (C-46, C-57) | the new logic of both increments | `evidence/mutate.py` (M1..M19 on `views.py` at increment 001; N1..N11 on `app.py` and `present_paths` at increment 002), run in a scratch copy of the tree |
| the byte oracles in new files (B3, C-24) | the gantt frame changes (the view word, the 80-column note wrap) | increment 001: `evidence/gen_frames.py` writes the eight PRES-V3 frames and cross-checks them row for row against `views_d.py`; PRES-R / PRES-R2 untouched |
| the B1 repoints, named, law-driven (C-26) | earlier batches' tests assert the frame, the hint, the census key | increment 001: TC-1001, TC-1002, AT-1001 (`tests/test_present.py`); increment 002: TC-1604's hint arm (`tests/test_present_hide.py`), TC-402's `PresentScreen._paint` key (`tests/test_markup_census.py`) |
| the full suite with a saved transcript (C-19) | every increment and P4 | each increment's `evidence/suite-NNN.txt`; P4's `evidence/suite-p4.txt` (the orchestrator's run) |
| the real-app captures (D1) | the change is what the room sees | increment 002: `evidence/capture_app.py` (SVG at 118×31 and 80×25, PNG at 118 through Edge) |

### 5c · Security lens (C8; PDR PC-A2)

`security-reviewer` approved at P2 (0 HIGH · 0 MEDIUM · 3 LOW). The S1 escape holds at every new markup site — `_present_note_markup`, the one-row cut in `_present_cut`, `_present_heading`, the gantt note rows — proved by TC-1805 (both nodes) and mutant M8. S-1 (`present_paths` takes `view` unvalidated) is accepted: every caller passes a `PRESENT_VIEWS` constant. S-3 (`textwrap` counts code points) is accepted: a wide row is cut by `clip` with a visible `…`, the frame stays exact; a cell-width wrap is a backlog option. No new write: the board is still written only by `space`/`a`; the export writes the shipped `reports/` folder under one new name (`-split`).

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| a renderer function per view (`render_present_split`) | the two views share the top of the frame, the cursor rule and `present_tasks`; one function with a `view` argument keeps one cursor rule |
| keep the prototype's fixed 5-row scroll step | at 80×24 the cursor note's window is 4 rows, so a 5-row step skips rows no page shows (UX-1) |
| a renderer-side scroll clamp returned to the screen | it would need the layout twice or a second return value; the screen's same-frame guard (`pgdn` not taken when the next page paints the same frame) clamps with one comparison |
| keep `_present_note_lines` / `_present_note_row` for the old prototypes | dead product code; the prototypes are frozen evidence (ARCHITECTURE §3) and `gen_frames.py` binds the names itself |
| remember the last view in `settings` | refused by the brief: the presentation writes only `show_in_present` |
| one export file for both views | exporting both on one day would keep only the second |
| a cell-width wrap (S-3) | `textwrap` is the prototype's; a wide-glyph row is cut by `clip` with a visible `…`, the frame stays exact; carried as a backlog option |

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | increment 001 (`views.py`: §1, §3 split layout, §4 rows 1–3), increment 002 (`app.py` + `present_paths`: §3 state diagram, §4 rows 4–5) — their packets' §1 |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | `tests/present_notes_board.py` (the notes overlay, new, increment 001); `tests/present_board.py` (reused); `evidence/gen_frames.py` (the PRES-V3 writer and the prototype cross-check, increment 001); `evidence/mutate.py` (the battery, both increments); `evidence/capture_app.py` (the app captures, increment 002) |
| proposed test cases | layers 0/A/B and the DDR | §5 → `tests/test_present_views.py` (increment 001), `tests/test_present_views_app.py` (increment 002), the repointed `tests/test_present.py`, `tests/test_present_hide.py`; the DDR re-reads each mutation verdict |
| design → requirement traceability | the matrix and the DDR | §5's Id column ↔ `01-requirements.md` LLR `Executed verification` |

## 8 · Parallelisation plan *(only if the batch forks)*

n/a — one lane.
