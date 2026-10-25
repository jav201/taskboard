# Requirements Document — taskboard — Batch 2026-10-25-batch-02

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/req-template.md` and its part 2, `templates/guides/req-template.part2.md`, explain each field below and the rules that read them. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the validator parses them literally and they are never translated:
> `Validation` · `Acceptance test(s)` · `Boundary catalog` · `Negative control` · `Premise evaluation` · `Fork preconditions` · `Ledger` · `Requirement` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

---

## 1. Introduction

### 1.1 Purpose

The live contract of batch `2026-10-25-batch-02`: the presentation (`R`) colours the notes'
highlights. The notes' highlight syntax — `==text==` (tone `soon`), `!!text!!` (tone `over`),
`++text++` (tone `green`) — is tokenised by exactly one function, `views.highlight_segments`
(`taskboard/views.py:3450`, D-411), and every other seat of the app (the board's markup, the
details/editor preview) already drops the markers and paints each span in its tone. The
presentation's note rows — the gantt view's cursor note (view 1), the split view's note blocks
(view 2) and their `x` exports — bypass the tokeniser and paint the raw text `ink`, so the room
sees the marker characters. This contract fixes that one gap.

### 1.2 Scope

Covers: the presentation's note pipeline in `taskboard/views.py` — `present_note_lines`
(`:6640`), `_present_note_markup` (`:6707`), `_present_cut` (`:6713`), `_paint_marks`
(`:6697`) and their two call sites (the gantt cursor note, `taskboard/views.py:7052-7054`; the
split view's body, `:6830`, `:6852`, `:6855`); the `x` SVG/PNG exports in so far as they render
the same composed frame (`save_present_svg`, `:7072`).

Does NOT cover: the board's own markup (`_highlight_markup`, `:3527`) and the details/editor
preview (`notes_text`, `:3503`) — already coloured, byte-unchanged here; the presentation's
layout, keys, hints and every other surface (the regression pin, HLR-2905); view 3 (`all`) —
checked at intake, it draws no note rows (§2.7 row 5); any new design («No prototype», the
commission).

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| highlight / marker | the notes' inline syntax `==text==`, `!!text!!`, `++text++`; the marker characters themselves are never shown |
| tone | one of `soon` (yellow `#fbbf24`), `over` (`#f43f5e`), `green` (`#4ade80`) — the HEX table, `taskboard/views.py:45-75` |
| `ink` / `mut` | the presentation's base text tone (`#e6edf3`) / the board's base text tone (`#8b98a5`) — PH-1 keeps `ink` on the presentation |
| tokeniser | `views.highlight_segments` (`taskboard/views.py:3450`): notes text → `(segment, tone)` pairs, markers dropped; the ONE parser (D-411) |
| mention | `@Name` of a person the directory holds, drawn bold pink on the presentation (`mention_marks`, `taskboard/views.py:3496`) |
| presentation views | the `R` screen's three views: 1 `gantt`, 2 `split`, 3 `all` (`PRESENT_SCREEN_VIEWS`, `taskboard/views.py:7127`) |
| cut rows | a note given fewer rows than it needs ends `… +N lines` (`_present_cut`, `taskboard/views.py:6713`) |
| `x` export | the presentation's SVG/PNG export (`present_paths`, `taskboard/views.py:7058`) |

### 1.4 References

- `.dev-flow/COMMISSION-present-note-highlights.md` — the commission (PH-1..PH-4, AT-a..AT-e, evidence rules)
- `.dev-flow/BACKLOG.md` item 4 — the people-round finding (pre-existing defect), the story's source
- D-411 — the one-tokeniser decision, recorded in `highlight_segments`'s docstring (`taskboard/views.py:3451-3455`)
- Batch 2026-10-21-batch-01 — the people round: mentions on the presentation (`present_mentions`, `mention_marks`, `_paint_marks`)
- Batch 2026-10-20-batch-03 — view 3 (`all`) and its export (`present_all_export`, `taskboard/views.py:7374`)

### 1.5 Document overview

§2 the story, its premises and the fork declaration. §3 the high-level requirements (one per
acceptance limb). §4 the low-level requirements (the mechanism). The Information Flow Contract
(C-54) follows §4. §5 the validation strategy. §6 appendices.

---

## 2. Overall description

### 2.1 Product perspective

`taskboard/views.py` is the presentation's one renderer: `render_present` composes the frame
for views 1 and 2, `render_present_all` for view 3, and `save_present_svg` prints the very
same composed `Text` to the `x` SVG. The note rows are built in three steps — `present_note_lines`
turns a task's notes into wrapped `(lead, text)` rows, `_present_cut`/`_present_note_markup`
turn the rows into padded markup strings, and `_paint_marks` paints everything `ink` with
mentions bold pink. Because the painting step never calls `highlight_segments`, the markers
survive to the screen and the export. The fix belongs entirely inside this pipeline; every
consumer of it (both views, both exports, the scrolled/paged note paths) is downstream of the
same three functions.

### 2.2 Product functions

- Tokenise each note paragraph's text with `highlight_segments` before it is wrapped or painted.
- Wrap by visible cells on the marker-free text, attributing each output cell to its span's tone.
- Paint each row: the lead in `mut`, each span in its tone (`soon`/`over`/`green`), unmarked
  text in `ink`, a mention inside any span bold pink.
- The `x` exports show exactly what the screen shows, unchanged in layout, keys or hints.

### 2.3 User characteristics

The operator presenting a board to a room, reading the projected notes at a glance. No other
role is affected.

### 2.4 Constraints

- One increment; SOURCE set expected to be `taskboard/views.py` alone (at most 4; commission §Increments). Tests uncapped.
- The presentation's base tone stays `ink`, not the board's `mut` (PH-1); the audience surface keeps its contrast.
- Cut rows (`… +N lines`), edge marks, bullet and number leads keep their current wording and shape (PH-2, PH-3).
- Synthetic data only; the operator's real name never appears (`username_subject`).

### 2.5 Assumptions and dependencies

- `highlight_segments`'s semantics are stable and shared: markers dropped, tones assigned, unpaired markers literal (verified by execution, §2.7 rows 1-2).
- The tone values live in the HEX table (`taskboard/views.py:45-75`); the presentation's markup painter is `c(text, tone)` with `escape` for user text (`taskboard/views.py:78`, `:87`).
- The export prints the screen's composed frame (`save_present_svg`, `taskboard/views.py:7072-7082`), so the SVG needs no painter of its own.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-2901 | As the operator presenting the board to a room, I want the presentation's note rows to colour the notes' `==..==`, `!!..!!` and `++..++` highlights (dropping the markers) exactly as the board does, so that the room sees highlighted notes, not raw marker characters. | `.dev-flow/BACKLOG.md` item 4 (the people-round finding, pre-existing); commissioned by `.dev-flow/COMMISSION-present-note-highlights.md` | READY |

#### Refinement log (one block per story)

**US-2901 — the presentation colours the notes' highlights**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator presenting to a room · outcome = note highlights appear in their tones on views 1 and 2 and their `x` exports, with no marker characters · why = the room currently sees raw `!!`/`++` text the rest of the app colours · out of scope = the board's own markup (already coloured), the presentation's layout/keys/hints, any new design («No prototype», commission)
- **Feasibility (E, S):** implementation path = route `present_note_lines` / `_present_note_markup` / `_present_cut` and the split-view body through the existing `views.highlight_segments` tokeniser · dependencies/unknowns = none — the tokeniser, `mention_marks`, `_wrap_cells` all exist · fits one batch? = yes (one increment, `taskboard/views.py` only)
- **Evaluability (T) — behavioral, black-box:** "When a note holds `==a== !!b!! ++c++`, the operator observes each word painted in its tone with no marker characters on the presentation's gantt view (1) and split view (2), at 118x30 and 80x24, including a highlighted span wrapped across two rows, and the `x` SVG export of view 2 shows the same tones with no markers." → AT-2901..AT-2905.
- **Open questions:** none — the commission pins PH-1..PH-4 (one tokeniser, visible-width wrapping, coexistence, exports).
- **Classification:** `READY` — INVEST closed on all six axes; the behavior is observable through the shipped presentation surface; ≥1 black-box AT stated.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| 1 | `highlight_segments("==a== !!b!! ++c++")` returns the markers dropped and each word in its tone | premise | ✅ TRUE | executed probe: `[('a', 'soon'), (' ', 'mut'), ('b', 'over'), (' ', 'mut'), ('c', 'green')]` (`evidence/red-p1.txt` probe 1) | folded into LLR-2901.1's acceptance |
| 2 | An unclosed marker stays literal text: `highlight_segments("pay !!attention now")` returns one `mut` segment with the `!!` intact | premise | ✅ TRUE | executed probe: `[('pay !!attention now', 'mut')]` (`evidence/red-p1.txt` probe 2) | AT-2904's literal arm |
| 3 | Today the presentation paints the note rows `ink` with the markers raw: `_present_cut(present_note_lines("==a== !!b!! ++c++", 30), …)` yields markup holding 12 marker characters and none of the three tone colours | premise | ✅ TRUE | executed probe at `base_ref`: 12 marker chars, `any tone colour present: False`, the row painted `ink` (`evidence/red-p1.txt` probe 3) | the defect; AT-2901/AT-2902's RED side |
| 4 | The tone values are `soon #fbbf24`, `over #f43f5e`, `green #4ade80`, `mut #8b98a5`, `ink #e6edf3`, `pink #f472b6` | premise | ✅ TRUE | executed probe read the HEX table (`evidence/red-p1.txt` probe header) | AT assertions key on these literals |
| 5 | View 3 (`all`) draws no note rows, so it cannot show raw markers | premise | ✅ TRUE | `grep -n note` over `taskboard/views.py:7127-7349` (the `_all_timeline` block) prints nothing; view 3's only note-adjacent surface is `present_hidden_rows`'s `u` list, plain text | view 3 checked and discharged (commission: «Check view 3 as well») |
| 6 | The `x` exports render the same composed frame the screen shows — `save_present_svg` prints the `Text` the view returned; no export-side painter exists | premise | ✅ TRUE | `taskboard/views.py:7072-7082` (`save_present_svg`), `:7374-7386` (`present_all_export` → `to_text`); the app calls them with the render output (`taskboard/app.py:616-630`) | PH-4 needs no export code; AT-2903 asserts on the SVG bytes |

- **Premise evaluation:** 6 premise(s) · ✅ 6 TRUE / ❌ 0 FALSE / ❓ 0 UNDECIDABLE — the commission's hypothesis (the defect) is premise 3, confirmed TRUE at `base_ref`.

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

| # | Condition (`C-52`) | Discharged? | The executed evidence |
|---|---|---|---|
| 1 | **Frozen contract** — no shared interface is touched inside a lane; one that must change returns to the trunk (trigger A3) | ✅ | one lane; no interface consumed by another module changes — the fix consumes `highlight_segments` unchanged |
| 2 | **Disjoint FILE sets**, not just modules — two lanes may not edit the same file, not even different regions | ✅ | one lane; the file set is `{taskboard/views.py, tests/}` |
| 3 | **Crossed reverse census** — family B run per lane and **shared before starting**; the trunk's act, impossible from inside a lane | ✅ | one lane; B1's census (B1 fired: `tests/test_edit_window.py`, `tests/test_highlight_segments.py` own the tokeniser) is run at P2/P3 over this lane's whole set |
| 4 | **One owner of the trunk** — requirements, traceability, backlog and spec are never written from a lane | ✅ | the orchestrator owns the trunk; no lane exists |

- **Fork preconditions:** none — this batch runs one lane.

---

## 3. High-level requirements (HLR)

**The chains, one line each:** US-2901 → HLR-2901 (view 1, the commission's AT-a), HLR-2902
(view 2 + the wrap, AT-b), HLR-2903 (the export, AT-c), HLR-2904 (coexistence, AT-d) and the
regression pin HLR-2905 (AT-e).

### HLR-2901 — the gantt view's cursor note colours the highlights
- **Traceability:** US-2901
- **Ledger:** LED-2901.3
- **Statement:** When the presentation's gantt view (view 1) shows the cursor task's note and the note holds `==a==`, `!!b!!` and `++c++`, the system shall paint each of `a`, `b` and `c` in its tone (`soon`, `over`, `green`) and shall show no marker character in the note's rows; text outside the markers keeps the presentation's base tone `ink`.
- **Rationale (informative):** the people-round finding (BACKLOG item 4): the presentation is the one seat left drawing the markers raw. The board and the details/editor preview already colour them through the same tokeniser (D-411); this HLR closes the gap on the gantt cursor note (`taskboard/views.py:7052-7054`).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_present_note_highlights.py -k AT_2901` (node minted at P3; P1 RED probe executed at `base_ref`, `evidence/red-p1.txt` probe 3)
- **Numeric pass threshold:** over the painted cursor-note rows, no run of `==`, `!!` or `++` appears in the painted rows (the fixtures are authored free of literal `=`, `!`, `+` so the scan is mechanical) AND each tone colour `#fbbf24`, `#f43f5e`, `#4ade80` appears at least once AND the unmarked words appear in `#e6edf3` (the probe at `base_ref` measured 12 marker chars and zero tone colours).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the cursor task's note on the projected gantt reads `a b c` in yellow, rose and green — no `==`, `!!`, `++` anywhere in it.
  - **Shipped surface:** the `R` screen's gantt view (view 1) with the cursor on a task whose notes hold the three highlights.
  - **Acceptance test(s):** AT-2901
  - **Boundary catalog (QC-3):** ☐ empty (a task with no notes shows no note rows — existing behaviour, pinned by the present suite) ☐ boundary (a note that is exactly one marker pair fills a row, markers dropped) ☐ invalid (an unclosed `!!` stays literal — asserted in AT-2904) ☐ error (none new — the paint cannot fail on note text)
  - **Negative control:** executed at P1 against `base_ref` — 12 marker characters in the painted row and none of the tone colours (`evidence/red-p1.txt`, probe AT-2901). The node-minted RED lands in increment 001's mutation battery (C-40): bypassing `highlight_segments` turns AT-2901 red.

### HLR-2902 — the split view colours the highlights, at 118x30 and at 80x24, across wraps
- **Traceability:** US-2901
- **Ledger:** LED-2901.3
- **Statement:** When the presentation's split view (view 2) shows a task's note holding `==a==`, `!!b!!` and `++c++`, at 118x30 and at 80x24, the system shall paint each highlighted word in its tone with no marker character in any note row; a highlighted span that wraps across two rows shall keep its tone on both rows; the wrapping shall count the visible text only, never the markers, so a highlighted row is not cut early; the cut rows (`… +N lines`) and edge marks keep their current wording.
- **Rationale (informative):** PH-2's width rule. Today `present_note_lines` wraps the marker-raw text (`taskboard/views.py:6659`), so a highlighted note wraps as if the markers were visible and a span loses its tone wherever a row boundary splits it. The 118x30 and 80x24 sizes are the commission's two room regimes.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_present_note_highlights.py -k AT_2902` (node minted at P3; P1 probe of the wrap defect, `evidence/red-p1.txt` probe 4)
- **Numeric pass threshold:** at both sizes: marker characters in the note rows == 0; each of the three tone colours present; for the wrap fixture, the wrapped span's tone appears on every row the span touches AND the row that carries the marker-free text fills to the same cell count as the equivalent unmarked note (the markers contribute 0 to the width).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the split view's note blocks read in colour at both sizes; a long highlighted phrase keeps its colour on the row it continues onto; nothing clips early and the `+N lines` cuts read as before.
  - **Shipped surface:** the `R` screen's split view (view 2), one column per half, the note blocks under each task heading.
  - **Acceptance test(s):** AT-2902
  - **Boundary catalog (QC-3):** ☐ empty (a task with no notes says `no notes` in the heading — existing, pinned) ☐ boundary (a span cut by the row edge keeps its tone on both rows; a note of exactly the row width is not cut early) ☐ invalid (unclosed marker — AT-2904) ☐ error (none new)
  - **Negative control:** executed at P1 against `base_ref` — the wrap counts the markers: `present_note_lines("word " * 8 + "==tail==", 30)` puts `word word ==tail==` on the second row, i.e. the markers consume width (`evidence/red-p1.txt`, probe 4).

### HLR-2903 — the `x` exports carry the same colours, no markers
- **Traceability:** US-2901
- **Ledger:** LED-2903
- **Statement:** When the user presses `x` in the presentation's split view (view 2), the exported SVG shall carry the same highlight tones as the screen for the same note and no marker character; the PNG, rendered from the same SVG pipeline (and only where the headless Edge renderer is installed — where it is not, the PNG limb is `n/a — no Edge`, the app's existing toast behaviour), shall match.
- **Rationale (informative):** PH-4. The export prints the screen's composed `Text` (`save_present_svg`, `taskboard/views.py:7072-7082`), so once the screen carries the tones the export does too — this HLR pins the claim with an assertion on the exported SVG bytes (C-42's emitted form: the predicate reads the SVG file, not the screen's memory).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_present_note_highlights.py -k AT_2903` (node minted at P3)
- **Numeric pass threshold:** the exported SVG's bytes contain each of `#fbbf24`, `#f43f5e`, `#4ade80` at least once AND contain no marker run (`==`, `!!`, `++`) from the note AND the SVG's visible text carries `a`, `b`, `c` in those spans; the exported SVG escapes hostile note text — a note holding `<`, `&` and `<script>` reaches the SVG only as `&lt;`/`&amp;` (Rich's `save_svg` escapes text content; `title=` is a constant) — 0 raw `<script` bytes in the file.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the file the room is handed (`reports/present-*-split-*.svg`) shows the highlighted note in colour, identical to the screen.
  - **Shipped surface:** the `x` export in view 2 (`present_paths` + `save_present_svg`).
  - **Acceptance test(s):** AT-2903
  - **Boundary catalog (QC-3):** ☐ empty (exporting with no cursor note — the existing export suite covers it) ☑ boundary (a cursor-less export — covered by the existing export suite's arms, unchanged) ☐ invalid (an unclosed-marker note in the export — pinned by screen parity and AT-2904, the export renders the screen's frame) ☐ error (an unwritable reports path is the existing export suite's arm, unchanged)
  - **Negative control:** executed at P1 against `base_ref` — the SVG path holds no tone painter: today's export of a highlighted note carries the markers in plain text and none of the tone colours (same probe 3 pipeline; the export renders the identical markup string).

### HLR-2904 — mentions, bullets and unpaired markers keep their rules inside highlights
- **Traceability:** US-2901
- **Ledger:** LED-2901.3
- **Statement:** When a note holds a mention of a person the directory holds inside a highlighted span, the mention shall stay bold pink (the highlight does not recolour it); the bullet and number leads (`• `, `1. `) shall be unchanged; an unclosed marker shall stay literal text, exactly as `highlight_segments` treats it.
- **Rationale (informative):** PH-3. The board's seat already defines the coexistence — `notes_text` paints a mention inside a highlight bold pink (`taskboard/views.py:3518-3523`); the presentation shall not diverge. The unpaired-marker rule is the tokeniser's, inherited verbatim (§2.7 row 2).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_present_note_highlights.py -k AT_2904` (node minted at P3; premise 2's probe is this arm's literal side)
- **Numeric pass threshold:** over the painted rows: the mention's text appears in `bold #f472b6` exactly once; the unclosed `!!attention` appears verbatim in `#e6edf3` with the `!!` intact; a `• `-led highlighted item keeps the lead in `mut` and the span in its tone; the span surrounding the mention keeps its tone colour on the same row.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `@Name` glows pink inside a coloured span; a stray `!!` nobody closed reads as typed; bullets look exactly as before.
  - **Shipped surface:** both presentation views' note rows (the mention arm is driven through view 2, the literal arm through view 1, by keys where a user would).
  - **Acceptance test(s):** AT-2904
  - **Boundary catalog (QC-3):** ☐ empty (a mention of a handle the directory does not hold stays as typed and uncoloured — the tokeniser-independent path) ☐ boundary (a mention spanning a wrap keeps bold pink on both rows) ☐ invalid (the unclosed marker) ☐ error (none new)
  - **Negative control:** executed at P1 against `base_ref` — today the whole row is `ink`, so the mention's bold pink is the only colour and the unclosed `!!` still prints raw; the mutation arm that drops the mention pass inside the tone painter turns AT-2904 red. Per arm: the mention-pink arm and the unclosed-marker-literal arm hold at `base_ref` by design (mentions already paint pink; raw text is already ink) — their RED sides are the increment's named mutations (mention pass dropped; escape removed); the bullet/span-tone arm is the one with an executed P1 red (the whole row is `ink` today, so the span has no tone — probe 3).

### HLR-2905 — nothing else changes (the regression pin)
- **Traceability:** US-2901
- **Ledger:** LED-2905
- **Statement:** When any surface not named in HLR-2901..HLR-2904 runs — the board's markup, the details/editor preview, view 3 (`all`), the presentation's headings, layout, keys, hints, cuts' wording, every other view of the app — the system shall behave exactly as before this batch; every existing presentation byte-oracle and capture-based test stays green, and where an oracle fixture legitimately holds the markers the update is named and justified in the increment packet (AT-e) — the split-frame byte oracle `tests/test_people_look.py` (its fixture `tests/people_round_fixture.py` holds `++sign-off by the sponsor++` in task c5's notes) is a named, expected update, re-scanned for further casualties at P3.
- **Rationale (informative):** the commission's AT-e. The change is confined to the note pipeline's paint step; everything else is pinned by the existing suite, whose baseline at P4 is 3258 passed (commission §Evidence).
- **Validation:** `test`
- **Executed verification:** the P4 full suite in 3 sequential chunks (the commission's §Evidence); the present suites (`tests/test_present*.py`) and the markup suites (`tests/test_markup_census.py`, `tests/test_markup_sites.py`, `tests/test_highlight_segments.py`, `tests/test_edit_window.py`) re-run.
- **Numeric pass threshold:** the P4 chunks hold 3258 + this batch's new-node count passed, with no skip other than the clipboard arm TC-1902 and no fail; the suites above green, with only justified oracle updates; a pre-increment baseline run of the full suite in 3 chunks is executed at P3 and its exact per-chunk counts are pinned in `04-validation.md` (the 3258 figure is the commission's; the P4 gate compares against the executed baseline); one new node asserts a pre-existing MARKER-FREE cursor-note row still paints `#e6edf3` (the existing byte oracles compare `text.plain` only and cannot see a style-only regression such as `ink`→`mut`).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** no difference anywhere except coloured highlights in the presentation's note rows and their exports.
  - **Shipped surface:** the whole app.
  - **Acceptance test(s):** AT-2905 (the P4 suite; every existing arm is a pin)
  - **Boundary catalog (QC-3):** none — a regression pin; it adds no input surface.
  - **Negative control:** not due — a regression pin, not a gate (C-40's corollary): its predicate is invariant under the change it certifies by construction, labelled a pin.

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.

### LLR-2901.1 — one tokeniser: the note rows are coloured only through `highlight_segments`
- **Traceability:** HLR-2901, HLR-2902
- **Ledger:** LED-2901
- **Statement:** The presentation's note pipeline shall tokenise each note paragraph's text with `views.highlight_segments` before any wrapping or painting; the markers shall be dropped on every path (whole rows, cut rows, scrolled/paged rows); each span shall be painted in its tone via the existing markup painter (`c(escape(segment), tone)`); text outside the spans shall keep the presentation's base tone `ink` — never the board's `mut`. No second parser of the marker syntax shall be introduced anywhere in the presentation. The changed symbols this LLR owns for the reverse census (C-26): `present_note_lines` (its row type becomes `(lead, [(segment, tone)])`), `_present_note_markup` and `_paint_marks` (the tone-aware paint); `_present_cut` is re-shaped by LLR-2902.1.
- **Rationale (informative):** PH-1, D-411. One tokeniser is what guarantees the presentation cannot disagree with the board on what a note highlights. The tokenise-before-wrap order is also PH-2's precondition: the wrap must see marker-free text.
- **Validation:** `test (unit)`
- **Executed verification:** AT-2901/AT-2902's nodes (P3) plus the reverse census probe: `grep -rn "_HIGHLIGHT_RE\|==" taskboard/views.py` at P3 lists the tokeniser as the only marker syntax reader in the presentation's note path (the regex itself stays untouched).
- **Numeric pass threshold:** AT-2901's numbers (0 markers, all three tones present, unmarked words in `#e6edf3`).
- **Negative control:** bypassing `highlight_segments` (painting the raw text) turns AT-2901 red — the commission's mandated mutation, executed in the increment's mutation battery.
- **Boundary catalog:** ☐ invalid (unclosed marker → literal, through the tokeniser, asserted in AT-2904)

### LLR-2901.2 — markup safety: every segment is escaped before it enters markup (C-17)
- **Traceability:** HLR-2901, HLR-2902, HLR-2904
- **Ledger:** LED-2901.2, LED-2901.3
- **Statement:** Every piece of note text — span or plain, mention or not — shall pass through `escape` before it is composed into a markup string, exactly as `_paint_marks` does today (`taskboard/views.py:6697-6704`); note text shall never be interpolated raw into a markup-parsed string. A hostile note (Rich brackets, ANSI control bytes, a link tag) shall render literally, with no parse error, no style leak and no crash. The `k == 1` cut path of `_present_cut` (`taskboard/views.py:6722-6727`) is an escape seat: its composed first row is painted piece by piece, never as one interpolated string.
- **Rationale (informative):** trigger C8 fired — this increment widens what is parsed into markup over file-derived note text. The presentation already escaped; the fix preserves that invariant span by span rather than row by row.
- **Validation:** `test (unit)`
- **Executed verification:** a hostile-input arm inside AT-2904's node (P3): a note holding `[bold red]`, `\x1b[31m` and a `https://` tag renders verbatim in `ink`; a note holding `a [/] b` must render literally with no exception (`MarkupError` is the failure).
- **Numeric pass threshold:** 0 styles other than `ink`'s appear in the hostile row; 0 raised exceptions; the hostile note's printable bytes all appear (escaped or verbatim) in the painted row; the painted row contains 0 `\x1b` bytes (Textual strips the control byte before render — verified by the P3 executed probe; if the probe shows a replacement glyph instead, the threshold is restated to that observed form in the increment packet, and either way the red style must never apply).
- **Negative control:** removing the escape on any segment turns the hostile-input arm red (style leak or `MissingStyle` error) — executed in the mutation battery.
- **Boundary catalog:** ☐ invalid (the hostile payload is the invalid class, covered above)

### LLR-2902.1 — the width counts visible text only; a wrapped span keeps its tone
- **Traceability:** HLR-2902
- **Ledger:** LED-2901
- **Statement:** The wrap shall measure the marker-free text in cells (the existing `_wrap_cells` semantics for wide and zero-width glyphs are unchanged, as is the `textwrap` fast path's regime); each output row shall carry its spans' tones, so a span split by a row boundary keeps its tone on every row it touches; the bullet and number leads and their hanging indent are unchanged; the cut rows (`… +N lines`) and edge marks keep their current wording and their `reached` tone. The changed symbol this LLR owns for the reverse census (C-26): `_present_cut` (its `rows` parameter carries the toned row shape, including the `k == 1` cut path).
- **Rationale (informative):** PH-2. The row representation must therefore carry tones, not a single tone per row — the PDR proposes the segment-list row form; this LLR binds the behaviour, not the type.
- **Validation:** `test (unit)`
- **Executed verification:** AT-2902's wrap fixture (P3) at 118x30 and 80x24; the width-equivalence arm: a note and its marker-free twin wrap to identical row counts and cell fills at the same width.
- **Numeric pass threshold:** the wrap fixture's span tone appears on both rows it touches (tone-bearing rows == 2 for the two-row fixture); the marker-free twin of any fixture wraps to the identical row count (delta == 0 rows) with the identical per-row cell counts (delta == 0 cells) at the same width.
- **Negative control:** restoring the marker-counting wrap (tokenising after the wrap) makes the width-equivalence arm fail — executed in the mutation battery.
- **Boundary catalog:** ☐ boundary (the row-edge split span; the exactly-full row)

### LLR-2903.1 — the exports render the composed frame; no export-side painter
- **Traceability:** HLR-2903
- **Ledger:** LED-2903
- **Statement:** `save_present_svg`, `present_paths` and `present_all_export` shall stay byte-unchanged; the `x` exports shall show whatever tones the composed frame carries. No SVG-specific colouring code shall be added.
- **Rationale (informative):** PH-4 with the least surface. The export is a renderer of the screen's `Text`; colouring it twice would be a second painter D-411 forbids in spirit.
- **Validation:** `inspection` + `test`
- **Executed verification:** `git diff` of the increment shows no change under the export functions (packet §2); AT-2903 asserts the emitted SVG's bytes.
- **Numeric pass threshold:** AT-2903's numbers (three tone HEX values present, no marker run, the words in the spans).
- **Negative control:** none beyond AT-2903 — an inspection-guarded LLR; the emitted-form assertion (C-42) is the gate.
- **Boundary catalog:** none — no new input surface.

### LLR-2904.1 — a mention inside a highlighted span stays bold pink
- **Traceability:** HLR-2904
- **Ledger:** none
- **Statement:** Mention detection shall run inside each tone span (the existing `mention_marks`/`_marks_re` machinery, `taskboard/views.py:3496`, `:6690-6694`): a mention of a person the directory holds is painted `bold pink` wherever it appears — inside or outside a highlight; the rest of the span keeps its tone. A mention across a row boundary keeps bold pink on every row it touches.
- **Rationale (informative):** PH-3, mirroring the board's `notes_text` (`taskboard/views.py:3518-3523`) so the two seats agree.
- **Validation:** `test (unit)`
- **Executed verification:** AT-2904's mention arm (P3), driven through the split view with a synthetic directory.
- **Numeric pass threshold:** the mention's text appears exactly once in `bold #f472b6`; the surrounding span keeps its tone colour on the same row.
- **Negative control:** painting the span tone over the mention (mention pass dropped) turns AT-2904 red — executed in the mutation battery.
- **Boundary catalog:** ☐ empty (a handle the directory does not hold stays as typed, uncoloured) ☐ boundary (a mention split by a wrap)

### LLR-2905.1 — the rest of the app is byte-unchanged
- **Traceability:** HLR-2905
- **Ledger:** none
- **Statement:** No file outside `taskboard/views.py` (and the new tests) shall change; inside `views.py`, the board's markup (`_highlight_markup`, `notes_text`, `_focus_note_snippet`), the details/editor preview callers, the gantt/kanban/swimlanes note snippets and every presentation surface other than the note rows' paint shall stay byte-identical.
- **Validation:** `inspection`
- **Executed verification:** the packet's §2 diff census (P3) and the P4 full suite (AT-2905).
- **Numeric pass threshold:** 0 modified files outside `taskboard/views.py` + tests; the diff hunks outside the note pipeline == 0.
- **Negative control:** not due — an inspection pin.
- **Boundary catalog:** none.

## Information Flow Contract (IFC) — C-54

- **Part A — flows:**

```flow
SOURCE: task.notes — the task's notes, file-derived text (taskboard/views.py Task.notes)
NODES:
  - present_note_lines (taskboard/views.py:6640): tokenise via highlight_segments, wrap by visible cells
    owner: LLR-2901.1, LLR-2902.1
  - _present_note_markup / _present_cut (taskboard/views.py:6707, :6713): paint each row — lead mut, spans in tone, mentions bold pink, escape every segment
    owner: LLR-2901.1, LLR-2901.2, LLR-2904.1
  - _paint_marks (taskboard/views.py:6697): the tone-aware paint — each segment escaped and coloured, mentions bold pink
    owner: LLR-2901.1, LLR-2901.2
  - render_present / render_present_all (taskboard/views.py:6977, :7349): compose the frame for views 1/2/3
    owner: LLR-2903.1
  - save_present_svg / present_all_export (taskboard/views.py:7072, :7374): emit the frame to the x SVG/PNG
    owner: LLR-2903.1
SINK: the PresentScreen terminal surface (views 1 and 2), and the SVG file at reports/present-<slug>-<date>[-<view>].svg (the x export)
```

- **Part B — boundary decomposition:** no — the presentation boundary exposes one screen surface and one file per view; no component of it is addressable by a consumer independently of the frame that carries it (the SVG file is a whole-frame artifact, not a component API).

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer A: unit arms over the pipeline functions (row shape, width equivalence, escape invariants) plus inspection pins (diff census, export functions untouched). Layer B: AT-2901..AT-2905 driving the real app by keys through the `R` screen at 118x30 and 80x24, asserting the painted styles and the emitted SVG bytes — one node per AT, per the commission.

### 5.2 Batch acceptance criteria
- 100% of LLRs covered by at least one executed verification with a pass result.
- Every user story has ≥1 passing `AT-NNN` black-box acceptance test observing its outcome through the shipped surface — with boundary + negative evidence (the P1 RED probes; the P3 mutation battery kills every new arm).
- The P4 full suite holds 3258 + new-node count passed, no skip other than TC-1902, no fail, in 3 sequential chunks.
- The mutation battery: bypassing `highlight_segments` turns AT-a (AT-2901) red, with per-arm verdicts recorded.
- No requirement without an assigned validation method.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
- *tone*: see §1.3. *cut rows*: see §1.3.

### 6.2 Relevant design decisions
- PH-1..PH-4, the commission's decisions, recorded at intake and restated per requirement above: one tokeniser (LLR-2901.1); visible-width wrapping with tone-carrying rows (LLR-2902.1); mentions/bullets/unpaired markers keep their rules (LLR-2904.1); exports render the composed frame (LLR-2903.1).

### 6.3 Open risks
- The Phase-1 security scan (`evidence/scan-p1.txt`) reports `security_required: true` with flags `role`, `form`, `escape` — each traced to its match and answered here:
  - `role` → §2.3 «No other role is affected» (user-characteristics prose; no auth surface exists or changes).
  - `form` → §1.5 «the Information Flow Contract» and §2.7 (the word "information" is not flagged; the matches are "formed"/"Information Flow Contract" — prose, no HTML form is involved; the presentation is a Textual screen, not a web form).
  - `escape` → LLR-2901.2's own subject: the fix must keep escaping note text before markup composition. This is the batch's one genuine security-adjacent control (trigger C8 → C-17), and it is answered BY a requirement, not an open risk: LLR-2901.2's hostile-input arm (Rich brackets, ANSI bytes, a link tag render literally, no parse error, no style leak) is minted at P3 inside AT-2904's node.
- No auth, secrets, external integration, sensitive data, destructive-DB, input-surface or network family (C1–C7) has a subject in this change; the scan's flags are the C6-adjacent vocabulary of the escaping control itself. Residual risk: the C-17 control is contractual but its hostile arms are P3-minted, not yet executed — the increment gate owes their execution and their mutation-battery kills before any ship verdict.

### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-25-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
