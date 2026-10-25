# Design proposal — taskboard — Batch 2026-10-25-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language
> The normative rules below are language-independent. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the validator parses them literally and they are never translated:
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
| Id | `PDR-2026-10-25-batch-02` |
| Requirements covered | `LLR-2901.1 v1 · LLR-2901.2 v1 · LLR-2902.1 v1 · LLR-2903.1 v1 · LLR-2904.1 v1 · LLR-2905.1 v1` (under `HLR-2901..HLR-2905`, `US-2901`) |
| Modules touched (from `docs/ARCHITECTURE.md`) | `taskboard/views.py` (the presentation's renderer) + `tests/` |
| Triggers that fired | `B1 · C8 · D1` (PDR/DDR taken up by the operator's directive, PLAN.md#triggers) |
| Author / reviewers | `architect` (author: the orchestrator) · reviewer: `architect` (independent, spawned) |

---

## 1 · Objective and scope

Colour the presentation's note rows through the one tokeniser (`highlight_segments`), so views 1 and
2 and their `x` exports drop the `==`/`!!`/`++` markers and paint each span in its tone, with the
presentation's base tone `ink` on unmarked text, wrapping measured on the marker-free text, mentions
bold pink inside any span, and zero change to layout, keys, hints, cut wording or any other surface
(`01-requirements.md`, LLR-2901.1..LLR-2905.1).

This design will NOT: touch the board's markup or the details/editor preview; add an export-side
painter; change `present_note_lines`'s geometry for marker-free text; re-open view 3 (checked: it
draws no notes).

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `taskboard/views.py` — the note pipeline (`present_note_lines`, `_present_note_markup`, `_paint_marks`, `_present_cut`) | tokenise-before-wrap, tone-carrying rows, tone-aware paint | the same three public entry points, new row shape (`lead`, `[(segment, tone)]`) | `taskboard/people.py` (mentions machinery is consumed as-is); the export writer (untouched) |
| `taskboard/views.py` — the composers (`render_present`, `_present_stack`, `_present_scrolled`/`_present_window`) | consume the rows; no change except the row type flowing through | markup strings, byte-shaped as today | the tokeniser (consumed, not modified) |
| `tests/` | the new AT nodes + justified oracle updates | — | — |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ — one module, no boundary moves; `highlight_segments`, `_wrap_cells`, `mention_marks`, `_marks_re`, `save_present_svg` are consumed, not edited.

## 3 · Diagrams

Information viewpoint (the only one that applies — the full IEEE 1016 set is not owed at `core`):

```
task.notes (file-derived text)
   │ present_mentions (people → @Name, NBSP-joined)     — unchanged
   ▼
highlight_segments  ── the ONE tokeniser (D-411) ──►  [(segment, tone)]   tone "mut"→"ink"
   ▼                                                     │
wrap (textwrap narrow path │ _wrap_cells wide path,      │ _tone_row: re-attribute each
   on the marker-free plain text — the SAME functions     │ wrapped row to its segments;
   and the same geometry regime as today)                 │ wrap-drop whitespace skipped
   ▼                                                     ▼
rows: (lead, [(segment, tone)])  ──►  _present_note_markup / _present_cut
                                        lead → mut; each segment → c(escape(seg), tone);
                                        mention marks (regex over the row's plain text)
                                        → c(escape(mark), "pink", bold=True); clip by cells
   ▼
markup strings (byte-shaped as today)  ──►  render_present / _present_stack  ──►  screen
                                          └──►  save_present_svg (UNCHANGED) ──►  the x SVG/PNG
```

State/algorithm viewpoint: the wrap stays greedy-per-word; the ONLY new state is the per-row tone
attribution, computed by a two-pointer walk (row text × segment stream) that asserts the skipped
stream chars are whitespace (a violated assertion is a bug alarm, not a silent recolour).

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `present_note_lines(notes, w, people) -> list[tuple[str, str]]` (rows of `(lead, plain_text)`) | `(lead, str)` rows | `(lead, [(segment, tone)])` rows — tones carried | `_present_cut`, `_present_note_markup`, `_present_stack.blocks`, the gantt cursor note (`views.py:7052`), tests | n/a — one lane, no fork |
| `_present_note_markup(row, w, marks)` / `_paint_marks(txt, marks)` | paints all `ink` | paints pieces by tone, mentions bold pink | `_present_cut`, `_present_stack`, the gantt cursor note | n/a |
| `highlight_segments`, `_wrap_cells`, `mention_marks`, `_marks_re`, `save_present_svg`, `present_paths`, `present_all_export` | — | **byte-unchanged** | everyone | **frozen** — a lane needing to change one returns to the trunk (A3) |

## 5 · Proposed test cases

All in `tests/test_present_note_highlights.py` (new), driving the app by keys through the `R`
screen where a user would; synthetic directory + the notes fixture (`tests/present_notes_board.py`).
One node per AT, per the commission.

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-2901 `test_AT_2901_gantt_cursor_note_colours_highlights` | B (AT-a) | view 1 cursor note: `a`/`b`/`c` painted in `#fbbf24`/`#f43f5e`/`#4ade80`, 0 marker chars, unmarked words `#e6edf3` | bypass `highlight_segments` in the note pipeline (paint raw) → markers + no tones |
| TC-2902 `test_AT_2902_split_view_colours_highlights_two_sizes` | B (AT-b) | view 2 at 118x30 AND 80x24: tones present, 0 markers; the wrap fixture's span keeps its tone on BOTH rows; width-equivalence: a note and its marker-free twin wrap to identical row shapes | restore the marker-counting wrap (tokenise after wrap) → twin shapes diverge |
| TC-2903 `test_AT_2903_split_export_svg_carries_tones` | B (AT-c) | the exported SVG bytes hold the three tone HEX values, no `==`/`!!`/`++` run, the words inside the toned spans | add an export-side painter (or strip tones at export) → SVG tones missing |
| TC-2904 `test_AT_2904_mentions_bullets_unpaired_markers` | B (AT-d) | mention inside a span stays `bold #f472b6`; unclosed `!!attention` literal in `#e6edf3`; `• ` lead in `mut` with the span toned; hostile payloads (`[bold red]`, `\x1b[31m`, a link tag) render literal in `ink` with 0 other styles | drop the mention pass inside toned pieces → mention recoloured; remove `escape` on one segment → hostile arm fails (style leak / `MissingStyle`) |
| TC-2905 (AT-e) | — | not a node: the P4 suite in 3 sequential chunks + the packet's oracle-update census | — |
| layer-0 arms (unit) | 0 | `_tone_row` over fixtures: tones re-attributed per row; whitespace-drop and tab-replacement walks; 0 mis-attributed chars | permute a tone in `_tone_row` → unit arms fail |

**Declared here, at authoring time, not at execution time.** Every AT names its reddening
mutation; the battery runs them per arm at P3 with per-arm verdicts (C-40's rider), restore
digests recorded.

## 6 · Risks and rejected alternatives

> Rejected alternatives are owed WHERE A REAL DECISION EXISTS.

| Alternative considered | Why it was rejected |
|---|---|
| Reimplement the wrap over segments directly (one new greedy wrapper, replacing both `textwrap` and `_wrap_cells`) | must reproduce `textwrap`'s hyphen-break and whitespace-collapse regime exactly or unmarked geometry drifts (AT-e blast radius: every present oracle); the re-attribution design keeps today's wrap functions byte-unchanged and pins geometry with the twin-equivalence arm instead |
| Keep `(lead, plain_text)` rows and re-tokenise at paint time | a row that dropped its markers no longer tokenises to the same spans — the paint cannot recover which characters were marked; tones must be carried from the tokeniser, not re-derived |
| Tokenise after the wrap (paint-time colouring of markers in wrapped rows) | PH-2 violated: the wrap counts the markers (measured at base_ref, `evidence/red-p1.txt` probe 4); a span cut by a row boundary could not keep its tone on the continuation row |
| An export-side painter that colours the SVG separately | a second parser/painter D-411 forbids in spirit; PH-4 is satisfied because the export renders the screen's composed frame — the PDR freezes the export functions byte-unchanged and AT-2903 asserts the emitted bytes |
| Mapping unmarked text to the board's `mut` | PH-1 pins `ink`: the audience surface keeps its contrast; `mut` is the board's seat's base |

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics — tokenise-before-wrap; rows carry `[(segment, tone)]`; `mut`→`ink` base mapping; `_paint_pieces` with mention override and escape on every segment; `_tone_row` two-pointer attribution | the Phase-3 increments | increment 001's packet §1/§2 and the code diff of `taskboard/views.py` |
| enablers — the notes fixture (`tests/present_notes_board.py`), a synthetic people directory, the 118x30 and 80x24 pilot sizes | Phase 3 and validation | the new test module's fixtures; the P4 captures |
| proposed test cases — TC-2901..TC-2904 + layer-0 arms, each with its named reddening mutation | layers 0/A/B at P3, and the DDR | `tests/test_present_note_highlights.py`; the increment packet's mutation battery; the DDR's conformance read |
| design → requirement traceability — the LLR ↔ design-element map (§2/§4 tables) | the matrix and the DDR | this proposal's tables, cited as `PDR-2026-10-25-batch-02#D<n>`; the DDR record |

- ⚠ Any row whose consumer column is empty: none — all four rows name a consumer.

## 8 · Parallelisation plan *(only if the batch forks)*

One lane — §8 not owed (`01-requirements.md` §2.8 declares the empty).
