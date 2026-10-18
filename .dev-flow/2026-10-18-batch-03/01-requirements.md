# Requirements Document — taskboard — Batch 2026-10-18-batch-03

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
The live contract for batch 2026-10-18-batch-03: the three presentation polish items the operator approved on 2026-10-18 («Si, apruebo.»), variant A of each, ported from the prototype round `prototypes/backlog_polish/` (batch 2026-10-18-batch-02, increment 003).

### 1.2 Scope
In: the tone of the presentation's view word and its cut and edge marks (`views.render_present`, `_present_cut`, `_present_mark`); a middle wording of the hint row (`app.PresentScreen._hint`); the gantt view's cursor note filling the frame's free rows (`views.render_present`); the tests that pin the shipped behaviour these change (law-driven updates, named in each packet's census); `docs/ARCHITECTURE.md` (doc). Out: every other `dim` mark of the presentation (the lattice, the separators, `no notes`, the gantt note's `· ` lead, `+N more rows not shown`, `no project to present`); the hint row's inactive view name, `#5b6675` (3.25:1, `app.py:309`) — variant A did not touch it (ux-reviewer UX-2); the split view's note allocation; the narrow frame below 36 columns; the OPERATOR items (`selected: no dates`, the Slide view, page snapping); the round folder itself (kept, see §6.3); pushing to any remote.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| quiet mark | a presentation mark that says what the frame does not show or which view it is: the header's view word (`gantt` / `split`), a note's cut mark `… +N lines` (and ` … +N lines` beside a one-row note), a paged window's edge marks `↑ N lines above` and `↓ N more lines` |
| `reached` tone | `HEX["reached"]` = `#7a828c`, the reached-milestone tone, 4.87:1 on the presentation background `#0d1117` (WCAG 2 contrast ratio) |
| `dim` tone | `HEX["dim"]` = `#5b6675`, 3.25:1 on `#0d1117` |
| middle wording | the hint wording `⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc` (`pgdn · ` before it in the split view), tried right after the long one, with two-space gaps after the view names |
| free rows | the rows of the presentation frame left blank under the gantt view's last brief row |
| round | the prototype round `prototypes/backlog_polish/`: its capture script's forks, its captures and its page |

### 1.4 References
- The operator's verdict, 2026-10-18 (the commission): «Si, apruebo.» — variant A of the three items of `prototypes/backlog_polish/backlog-polish-prototype.html`.
- The round: `prototypes/backlog_polish/capture.py` (`contrast_fork`, `hint_fork` + `HINT_A`, `cap_fork("fill")`), `out/manifest.json`; HLR-1905, LLR-1905.1 (canon).
- The presentation: LLR-1001.1, HLR-1801..1803, LLR-1802.1, LLR-1803.2, HLR-1903, HLR-1904, LLR-1904.1 (canon); `taskboard/views.py:6230-6278`, `:6472-6542`; `taskboard/app.py:280-312`.
- The P4 walkthrough of 2026-10-18-batch-01 (`04-validation.md`: UX4-2, UX4-3, UX4-4).

### 1.5 Document overview
§2 the stories, premises and fork preconditions; §3 three HLRs; §4 three LLRs and the information-flow contract; §5 the validation strategy.

---

## 2. Overall description

### 2.1 Product perspective
Three changes inside the shipped presentation (`R`): two in the renderer (`views`), one in the screen's hint row (`app`). No new key, view, file or setting.

### 2.2 Product functions
1. The marks that say "there is more" or "which view this is" read on a projector (≥ 4.5:1), still quieter than the text.
2. At 80 columns the hint names `next` and `show all`.
3. The gantt view shows as much of the cursor's note as the frame has room for.

### 2.3 User characteristics
A presenter in the real app (`R`), keyboard-only, often on a shared screen or a projector, at the operator sizes 118×31 and 80×25 and at any other width ≥ 36.

### 2.4 Constraints
Textual + Rich as shipped; no new dependency; every frame row exactly `width` cells (S1) and exactly `height` rows; every untrusted string escaped before it enters markup (S1/C8, unchanged sites); the PRES-V3 oracle files are not rewritten (new frames go in new files); the round's committed files are not rewritten; synthetic data only; the operator's name nowhere.

### 2.5 Assumptions and dependencies
The fixtures `tests/present_board.py` and `tests/present_notes_board.py` stay as they are. Microsoft Edge is present for the PNG captures (`views._find_msedge()`; the round used it on this host).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-2001 | As a presenter on a shared screen or a projector, I want the view word and the marks that say a note or a column was cut to be readable, yet quieter than the titles and dates, so that the room sees there is more without the marks competing with the content. | operator verdict 2026-10-18 «Si, apruebo.» — round item 1, variant A (`reached`); UX4-2 of 2026-10-18-batch-01 | READY |
| US-2002 | As a presenter at 80 columns, I want the hint row to name `next` and `show all` when there is room for them, so that I find the keys a first-time presenter cannot guess. | operator verdict 2026-10-18 — round item 2, variant A (the middle wording); UX4-3 | READY |
| US-2003 | As a presenter in the gantt view, I want the cursor task's note to use the rows left empty under the list, still saying when it is cut, so that I can talk from the note without switching to the split view. | operator verdict 2026-10-18 — round item 3, variant A (fill the free rows); UX4-4 | READY |

#### Refinement log (one block per story)

**US-2001 — the quiet marks read on a projector**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = a presenter (and the room) · outcome = the view word, `… +N lines` and the `↑ N lines above` / `↓ N more lines` marks painted in `reached` (4.87:1) where they are `dim` (3.25:1) today; every other `dim` mark unchanged · why = at ~3:1 the marks can vanish on a projector (UX4-2), and `mut` (6.43:1) would put them level with the secondary text (the round's reason for A over B) · out of scope = the lattice, the separators, `no notes`, the `· ` note lead, `+N more rows not shown`
- **Feasibility (E, S):** implementation path = four `"dim"` literals → `"reached"` in `views.py` (the header's view word, the two cut marks of `_present_cut`, `_present_mark`) · dependencies/unknowns = none (P-1, P-2) · fits one batch? = yes, one increment, 1 source file
- **Evaluability (T) — behavioral, black-box:** When the presenter opens `R` on a long note at 80×25, the frame's view word and its `… +N lines` are painted `#7a828c`; in the split view so are its cut and edge marks; the `· ` lead and `no notes` stay `#5b6675` (AT-2001).
- **Open questions:** none.
- **Classification:** `READY`.

**US-2002 — the 80-column hint names next and show all**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = a presenter · outcome = the hint row takes the middle wording whenever the long one does not fit and the middle one does: at 80×25 with nothing hidden, gantt `1 gantt  2 split  ⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc`, split `1 gantt  2 split  pgdn · ⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc`; with one task hidden at 80 the short wording as today · why = at 80 columns the hint fell to the short wording with ~20 cells to spare (UX4-3) · out of scope = the long, short, compact and `esc` wordings and the narrow hint (unchanged)
- **Feasibility (E, S):** implementation path = one tuple added to `_hint`'s wordings, after the long one · dependencies/unknowns = none (P-3) · fits one batch? = yes, one increment, 1 source file
- **Evaluability (T) — behavioral, black-box:** When the presenter opens `R` at 80×25, the hint row reads the middle wording in both views and fits its row (AT-2002).
- **Open questions:** none.
- **Classification:** `READY`.

**US-2003 — the gantt note fills the free rows**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = a presenter · outcome = the gantt view's cursor note takes every row left under the brief list (never fewer than 3); a note that still does not fit ends on `… +N lines`; a note that fits shows whole · why = the gantt view kept the note to 3 rows with 6 (80×25) to 12 (118×31) rows empty under it (UX4-4) · out of scope = the split view (it already shows notes whole or shared); the briefs' order and the frame above them
- **Feasibility (E, S):** implementation path = the 3-row cap in `render_present`'s gantt branch becomes `max(3, height - <rows above the note> - <brief rows>)` (P-4: equal to the round's `cap_fork("fill")` on every frame of the probe) · dependencies/unknowns = none · fits one batch? = yes, one increment, 1 source file
- **Evaluability (T) — behavioral, black-box:** When the presenter opens `R` on the long note at 80×25, the note runs to the frame's last row and ends on `… +N lines`; at 118×31 the same note shows whole (AT-2003).
- **Open questions:** none.
- **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | On the presentation background `#0d1117`, `dim` `#5b6675` reads 3.25:1, `reached` `#7a828c` 4.87:1 and `mut` `#8b98a5` 6.43:1 (WCAG 2 relative-luminance ratio), so `reached` clears 4.5:1 and stays below `mut` | premise | TRUE | probe over `views.HEX` on `base_ref` → `dim #5b6675 3.25`, `reached #7a828c 4.87`, `mut #8b98a5 6.43`; `views.py:64` `"reached": "#7a828c",  # … 4.9:1 on #0d1117`; `app.py` `PresentScreen { background: #0d1117; }` | `reached` is the tone (US-2001) |
| P-2 | The quiet marks are painted `dim` at exactly four sites of the presentation section, and the round's `contrast_fork` repaints exactly the spans those sites produce | premise | TRUE | `grep -n '"dim")' taskboard/views.py` in 6160–6545 → `:6243` (the one-row cut tag), `:6244` (`… +N lines`), `:6277` (`_present_mark`, both edge marks), `:6511` (the view word); the other hits are `:6324` (`no notes`, separator), `:6463` (`+N more rows not shown`), `:6494` (`no project to present`), `:6510`/`:6512` (` · `), `:6540` (`· ` lead) — none of them matched by the fork's `_QUIET` pattern (`capture.py:70`) | the four sites change, the others stay (HLR-2001) |
| P-3 | With the middle wording inserted after the long one, its first width is gantt 73 / 84 / 84 / 85 and split 80 / 91 / 91 / 92 for 0 / 1 / 3 / 10 hidden, below each long first width (84 / 95 / 95 / 96 and 97 / 108 / 108 / 109) and above each short first width (58 / 69 / 69 / 70 and 65 / 76 / 76 / 77) | premise | TRUE | probe: `cell_len("1 gantt  2 split  " + middle + tail) + 2` for both views × 0/1/3/10 hidden on `base_ref` → `gantt 0 73`, `gantt 1 84`, `gantt 3 84`, `gantt 10 85`, `split 0 80`, `split 1 91`, `split 3 91`, `split 10 92`; the long and short first widths: `01-requirements.md` of 2026-10-18-batch-02 P-7, pinned by TC-1904 (`tests/test_present_narrow.py:84-120`) | the literal threshold table of TC-2002 |
| P-4 | The round's `cap_fork("fill")` (`k = 3 + <blank rows under a 3-row render>`) equals `k = max(3, height - <rows above the briefs> - <brief rows>)` on every frame, and differs from the shipped 3-row cap only where a cut note had free rows | premise | TRUE | probe on `base_ref`: the fork over both presentation boards × every open task as cursor × widths 36, 50, 80, 100, 118, 140 × heights 5, 12, 20, 24, 30, 40, 60 → `420 frames; 120 differ from the 3-row cap`; at 118×30 the long note (`tw5`, 11 rows at width 112) leaves 12 free rows under 3 note rows, at 80×24 (13 rows at width 74) 6 | the port's formula; the oracle frames are the fork's own output (P-6) |
| P-5 | The shipped tests pin the behaviour these changes alter: TC-1807 (3 note rows; the PRES-V3 gantt-notes frames), TC-1808 (the short wording at 80, 96, 99, 100 columns), TC-1904's literal table and AT-1604's 80-column hint | premise | TRUE | `tests/test_present_views.py:403-421` (`assert len(notes) == 3`), `tests/test_present_views_app.py:259-276`, `tests/test_present_narrow.py:84-120`, `tests/test_present_hide.py:230-231`; `grep -l "… +" .dev-flow/2026-10-18-batch-01/evidence/frames/*` → the gantt-notes and split frames (the split frames' text does not change) | law-driven updates, named in each packet's census; the PRES-V3 files stay |
| P-6 | Re-run on `base_ref`, the round's own capture code reproduces its committed variant-A captures byte for byte (SVG, after the run-specific `terminal-<N>` class ids are normalised) | premise | TRUE | `evidence/port_captures.py --mode round` on a scratch worktree at `620f58c`, then `--compare` with `prototypes/backlog_polish/out` → `EQUAL` ×14 (every A capture of the three items, both sizes), `0 differ or missing` (`evidence/expected/compare-round.txt`) | the round's code re-run on `base_ref` is the port's oracle: `evidence/expected/upto-{1,2,3}.txt`, the final SVGs in `evidence/expected/upto-3/`; the frames `evidence/frames/PRES-V4-gantt-notes-*.txt` by `evidence/frames/gen_frames.py` |

- **Premise evaluation:** 6 premise(s) · ✅ TRUE ×6

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane: three increments in order on one branch, one owner (the orchestrator) holds the trunk.

---

## 3. High-level requirements (HLR)

### HLR-2001 — The quiet marks read at 4.5:1 and stay below the text
- **Traceability:** US-2001
- **Ledger:** LED-2026-10-18-batch-03.1, LED-2026-10-18-batch-03.2, LED-2026-10-18-batch-03.3
- **Statement:** When the presentation paints its header's view word — wherever the header keeps its tones (a title too wide for its row, `vis(title) + 2 > width`, is painted whole in bold `bright` by `header()`, as shipped) —, a note's cut mark (`… +N lines`, and ` … +N lines` beside a one-row note) or a paged window's edge mark (`↑ N lines above`, `↓ N more lines`), the system shall paint it in the `reached` tone, and shall keep the presentation's other `dim` marks — the separators, `no notes`, the gantt note's `· ` lead, `+N more rows not shown`, `no project to present` — in `dim`.
- **Rationale (informative):** variant A of the round's item 1, approved by the operator: 4.87:1 clears the 4.5:1 reading floor and stays quieter than `mut`, so the marks neither vanish on a projector nor compete with titles and dates.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_polish.py -k "2001"`
- **Numeric pass threshold:** AT-2001: the app on the notes board at 80×25, `R`, `→ →` (the cursor on `tw5`, whose note is cut): in `#present-frame`'s `Text`, the span over the header's `gantt` and the span over `… +N lines` carry `#7a828c` and no `#5b6675`; the span over the `· ` lead carries `#5b6675`; `2` (the split view): every span over a `… +N lines`, `↑ N lines above` or `↓ N more lines` carries `#7a828c`, the span over `split` too, and at least one such cut or edge mark is present; the WCAG ratio of the marks' colour on `#0d1117` is ≥ 4.5 and below that of `HEX["mut"]`.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the view word and the cut and edge marks painted `#7a828c` in both views; the lead and the separators still `#5b6675`.
  - **Shipped surface:** key `R` → `PresentScreen` `#present-frame` (and, through it, the `x` export, which writes the same frame).
  - **Acceptance test(s):** AT-2001
  - **Boundary catalog (QC-3):** ☑ boundary (a one-row cut, ` … +N lines` beside the first line — TC-2001 at 60×20 in the split view; the edge marks at page 0 and page 1) ☐ empty — none: a task with no notes paints no cut mark, its `no notes` is out of scope and stays `dim` (asserted) ☐ invalid — none: no input text ☐ error — none
  - **Negative control:** on `base_ref` AT-2001 is RED: the marks carry `#5b6675` (`evidence/red-001.txt` — planned).

### HLR-2002 — The hint row takes a middle wording before the short one
- **Traceability:** US-2002
- **Ledger:** LED-2026-10-18-batch-03.1, LED-2026-10-18-batch-03.3
- **Statement:** When the presentation paints its hint row at 36 columns or more, the system shall try, in order, the long wording, the middle wording (`⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc`, with `pgdn · ` before it in the split view, two-space gaps after the view names), the short wording, the compact wording and the `esc` wording, each followed by the hidden count, and paint the first that fits the row — five wordings where HLR-1904 counts four; every other rule of HLR-1904 stands.
- **Rationale (informative):** variant A of the round's item 2, approved by the operator: it keeps `next` and `show all` — the keys a first-time presenter does not guess — with the long wording's vocabulary and order, and keeps the `·` groups that variant B dropped.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_polish.py -k 2002`; `python -m pytest -q -p no:cacheprovider tests/test_present_narrow.py tests/test_present_views_app.py tests/test_present_hide.py`
- **Numeric pass threshold:** AT-2002: the app on the notes board at 80×25, `R` → `#present-hint` reads `1 gantt  2 split  ⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc` (71 cells, within its 78), the `1 gantt` span bold `#e6edf7`; `2` → `1 gantt  2 split  pgdn · ⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc` (78 cells); `space` (one hidden) → `1 gantt 2 split pgdn · ⇥ · ←→ · ␣ hide · a all · x export · esc · 1 hidden`; at 118×31 the long wording as shipped.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** at 80 columns the hint names `next` and `show all` in both views.
  - **Shipped surface:** `PresentScreen` `#present-hint`.
  - **Acceptance test(s):** AT-2002
  - **Boundary catalog (QC-3):** ☑ boundary (each middle first width and the width below it, both views, 0 / 1 / 3 / 10 hidden — TC-2002; 80 exactly is the split view's first middle width) ☐ empty — none: the hint always has a wording ☐ invalid — none ☐ error — none
  - **Negative control:** on `base_ref` AT-2002 is RED: at 80×25 the hint is the short wording (`evidence/red-002.txt` — planned).

### HLR-2003 — The gantt view's cursor note fills the free rows
- **Traceability:** US-2003
- **Ledger:** LED-2026-10-18-batch-03.1, LED-2026-10-18-batch-03.3
- **Statement:** When the presentation paints the gantt view with a cursor task, the system shall give the cursor's note every row of the frame left under the brief list, and never fewer than 3; a note with more rows than that shall end on `… +N lines` (N the rows not shown, the mark's own row counted), and a note that fits shall be shown whole.
- **Rationale (informative):** variant A of the round's item 3, approved by the operator: the rows under the list were empty (6 at 80×25, 12 at 118×31), and filling them adapts to the terminal by itself; the cut is still declared.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_polish.py -k 2003`; `python -m pytest -q -p no:cacheprovider tests/test_present_views.py`
- **Numeric pass threshold:** AT-2003: the app on the notes board at 80×25, `R`, `→ →` (the cursor on `tw5`): the frame's rows equal `evidence/frames/PRES-V4-gantt-notes-80x24.txt` (the round's `cap_fork("fill")` output on `base_ref`), the note's last row is `· … +5 lines`, the next brief (`SEO redirects map`) is the frame's last row and no row of the frame is blank; at 118×31 they equal `PRES-V4-gantt-notes-118x30.txt`, the note's 11 rows whole and no `… +` in the frame.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the note runs to the bottom of the frame and declares its cut; a note that fits shows whole.
  - **Shipped surface:** key `R` → `PresentScreen` `#present-frame` (and the `x` export).
  - **Acceptance test(s):** AT-2003
  - **Boundary catalog (QC-3):** ☑ boundary (free rows 0, so the floor of 3 holds and the frame overflows as shipped; a note exactly as long as the room; one row more) ☑ empty (no cursor: no note; a cursor task with no notes: no note rows) ☐ invalid — none ☐ error — none
  - **Negative control:** on `base_ref` AT-2003 is RED: the note stops at 3 rows (`evidence/red-003.txt` — planned).

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-2001.1 — Four tone literals
- **Traceability:** HLR-2001
- **Ledger:** LED-2026-10-18-batch-03.1, LED-2026-10-18-batch-03.2, LED-2026-10-18-batch-03.3
- **Statement:** `taskboard/views.py` shall paint, with `c(…, "reached")`, the header's view word in `render_present` (which `header()` keeps wherever the title fits with two cells to spare), the one-row cut tag and the `… +N lines` row of `_present_cut`, and every row `_present_mark` returns; the presentation's other `c(…, "dim")` sites shall be unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_polish.py -k TC_2001`
- **Numeric pass threshold:** TC-2001 passes: over both presentation boards × both views × widths 36, 60, 80, 100, 118 × heights 20, 24, 30 × every open task as cursor × scroll 0 / 1 / 3: every span whose text matches a cut or edge mark, and the view word wherever the header keeps its tones, carries `HEX["reached"]` and not `HEX["dim"]`; every span over the `· ` lead, a ` · ` separator, `no notes` or `+N more rows not shown` carries `HEX["dim"]`; on a board with no project, `no project to present` carries `HEX["dim"]`; at least one view word, one cut mark, one `↓ N more lines` and one `↑ N lines above` occur in the sweep; the frames' plain text is unchanged by this LLR (after increment 001 the PRES-V3 nodes TC-1001/1002 and `tests/test_present_views.py` stay green; increment 003's frames are held by TC-2003).
- **Negative control:** TC-2001 goes RED when any one of the four sites keeps `"dim"`, and when a lead or separator site is repainted `reached` (mutations at increment 001 — planned).
- **Boundary catalog:** ☑ boundary (the one-row cut at 60×20; page 0 vs page 1 edge marks) ☐ empty — none ☐ invalid — none ☐ error — none

### LLR-2002.1 — The middle wording in `_hint`
- **Traceability:** HLR-2002
- **Ledger:** LED-2026-10-18-batch-03.1, LED-2026-10-18-batch-03.3
- **Statement:** `PresentScreen._hint(w)` shall hold, between the long and the short wording, the wording `("  ", ("pgdn · " if split else "") + "⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc")` — the round's `HINT_A`, verbatim — and keep LLR-1904.1's choice, cut and styles.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_narrow.py -k TC_1904`; `python -m pytest -q -p no:cacheprovider tests/test_present_polish.py -k TC_2002`
- **Numeric pass threshold:** TC-2002 passes over widths 1–140 × both views × 0, 1, 3 and 10 hidden: the wording at each width is the one of P-3's literal table and of TC-1904's table (each first width and one below asserted with the literal strings); the hint is at most `max(0, w - 2)` cells.
- **Negative control:** TC-2002 goes RED when the middle wording is removed, when it is tried before the long one, and when its gap is one space (mutations at increment 002 — planned).
- **Boundary catalog:** ☑ boundary (each middle first width and one below; 80 exactly in the split view) ☐ empty — none ☐ invalid — none ☐ error — none

### LLR-2003.1 — The fill formula
- **Traceability:** HLR-2003
- **Ledger:** LED-2026-10-18-batch-03.1, LED-2026-10-18-batch-03.2, LED-2026-10-18-batch-03.3
- **Statement:** In `render_present`'s gantt branch, the cursor's note shall be cut with `_present_cut(rows, max(3, height - len(lines) - len(open_t)), width - 6)`, `lines` the rows painted before the brief list; `_present_cut` itself is unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_polish.py -k TC_2003`
- **Numeric pass threshold:** TC-2003 passes: the frames at 118×30 and 80×24 with the cursor on `tw5` equal `PRES-V4-gantt-notes-*.txt`; over both boards × every open task as cursor × widths 36, 50, 80, 100, 118, 140 × heights 5, 12, 20, 24, 30, 40, 60: exactly `height` rows; where `height ≥ L + min(n, 3)` (`n` the note's rows, `L` the header, ruler, span, task, rule and brief rows) the note shows `min(n, max(3, height - L))` rows and the frame has no `+N more rows not shown`, and a cut note leaves no blank row and ends on `· … +N lines` with `N` = `n - shown + 1`; where `height < L + min(n, 3)` the frame's last row is the shipped `+N more rows not shown` (the 3-row floor overflowing, as on `base_ref`); the sweep meets a note exactly as long as its room (`height - L = n`: whole, no cut, no blank row), one row longer (`height - L = n - 1`: `… +2 lines`), and the overflow case — asserted by a seen-set.
- **Negative control:** TC-2003 goes RED when the cap stays 3, when the floor of 3 is dropped (a frame with no free rows loses its note), and when the brief rows are not subtracted (the frame overflows) (mutations at increment 003 — planned).
- **Boundary catalog:** ☑ boundary (free rows 0; the note exactly the room; one row more) ☑ empty (no cursor; a cursor task with no notes) ☐ invalid — none ☐ error — none

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the presentation frame, from the board to the screen and the export
  SOURCE : the board file on disk (the presented project's tasks and notes); the terminal size
  NODES  :
    - fn    : views.render_present, its quiet marks' tone (_present_cut, _present_mark, the header)
      owner : LLR-2001.1
    - fn    : views.render_present's gantt branch, the cursor note's row count
      owner : LLR-2003.1
  SINK   : the terminal surface (#present-frame) and the x export (reports/present-*.svg, .png)
```

```
FLOW: the hint row, from the terminal width to the screen
  SOURCE : the terminal size (PresentScreen.size); the hidden count (present_hidden)
  NODES  :
    - fn    : app.PresentScreen._hint, the wording choice
      owner : LLR-2002.1
  SINK   : the terminal surface (#present-hint)
```

- **Part B — boundary decomposition:** `no — no component a consumer addresses on its own changes: the frame and the hint are the existing #present-frame and #present-hint widgets, addressed as before.`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer 0: `_hint` (a loop over five wordings) through TC-2002; the gantt note's row count through TC-2003; the four tone sites through TC-2001. Layer A: TC-2001..TC-2003 at the renderer and method level. Layer B: AT-2001..AT-2003 drive the real app headless (`run_test`, keys), reading `#present-frame` and `#present-hint`. Beside the suite, the port is compared with the round: the round's own capture code re-run on `base_ref` (P-6), its forks composed cumulatively, against the real app's captures after each increment (`evidence/expected/`, `evidence/captures/`).

### 5.2 Batch acceptance criteria
- every LLR has a passing TC; every story a passing AT through its surface;
- every new assertion RED on `base_ref` or by a recorded mutation; mutants KILLED on the new logic;
- the full suite: 0 failures; `test_win_clipboard_roundtrip` passes or skips with its quoted reason; transcript under the batch's evidence;
- real-app captures (SVG) of the gantt and the split view at 118×31 and 80×25, and PNGs at 118, in `evidence/captures/`; after each increment the port's captures equal the round's code re-run with the forks of the increments so far (normalised SVG), and the final ones are compared by eye with the round's A PNGs;
- the PRES-V3 files and the round's committed files unchanged (`git diff --stat 620f58c -- .dev-flow/2026-10-18-batch-01 prototypes/backlog_polish` empty);
- the RED and mutation transcripts the HLR/LLR negative controls mark `planned` exist before their increment's gate.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
See `PLAN.md` §Key decisions and `docs/ARCHITECTURE.md` (amended by this batch).
### 6.3 Open risks
- **Security questions (the P1 scan):** `devflow-scan-spec.py` over this document, 2026-10-18: 65 patterns, 5 control rows ok, `flags: none`, `security_required: false`, exit 0. No auth, secret, external integration, sensitive data, destructive DB, network or new input surface (C1–C7 not fired); no new markup site over board-file text — the gantt note's extra rows go through the shipped escaped site `_present_note_markup`, the tones are fixed tone names (C8 not fired). No open security risk.
- **The gantt note against the split view (ux-reviewer UX-1).** With the fill, the gantt view can show more of the cursor's note than the split view, which shares its room among every note (at 80×25: 9 rows ending `… +5 lines` against 3 rows and `… +10 lines`). Variant A as approved; the split allocation is out of scope (§1.2); recorded for the operator in `BACKLOG.md`.
- **The round's retirement.** AT-1905 (2026-10-18-batch-02) says the round folder and `tests/test_backlog_polish_round.py` leave together in the batch that implements the verdict. This batch keeps both: the commission names no deletion, and the round is the oracle this batch's comparison reads (P-6). The retirement is handed to the operator in `BACKLOG.md` (a deviation, declared in `PLAN.md` and the close).
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-18-batch-03

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
