# Requirements Document — taskboard — Batch 2026-10-18-batch-02

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
The live contract for batch 2026-10-18-batch-02: the open backlog items classed FIX — the two standup tests, the clipboard test's environment refusal, the presentation below 36 columns and its hint row below ~58 — and the prototype round for the three items classed PROTOTYPE.

### 1.2 Scope
In: `tests/test_team_views.py` (the standup tests), `tests/test_app.py` (the clipboard roundtrip test), `views.render_present` below 36 columns, `PresentScreen._hint`, `HISTORICAL` header notes on the six round files that no longer import (doc), the stale presentation comments (doc), and the round `prototypes/backlog_polish/`. Out: the standup's rendering (its 12-cell name column stays), the clipboard reader `models.grab_clipboard_text`, the presentation at 36 columns and above (the PRES-V3 oracle frames stay byte-equal), any production change for the three PROTOTYPE items (their verdict is the operator's), the OPERATOR and DECLINE rows of `PLAN.md` §*Backlog inventory*, pushing to any remote.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| name column | the standup row's member-name cells: `min(12, …)` wide (`views.py:4303`); `fit` cuts a longer name to 11 cells and `…` |
| placeholder | `username_subject`, the scrubbed stand-in for the operator's name (16 cells) |
| refusal | `Set-Clipboard` exiting non-zero during the clipboard test's setup (`Requested Clipboard operation did not succeed`) |
| contention | the sample was set, but the independent oracle (`Get-Clipboard`) no longer holds it after our reader ran |
| narrow frame | what `render_present` returns below `PRESENT_MIN_WIDTH`: one `dim` line `present needs 36+ columns`, cut with `…` to the width, then blank rows |
| wording | one of the hint row's three key lists: long, short, and the view switch with `esc` |
| round | a prototype round: captures of the real app with variants, and one page for the operator's verdict |

### 1.4 References
- The commission and the backlog inventory (`PLAN.md`); the module map (`docs/ARCHITECTURE.md`, amended at this batch's ARQ).
- The standup: batch-11 increment 3 (AT-T4), `taskboard/views.py:4232-4325`; the scrub `6bff525`.
- The clipboard test: `tests/test_app.py:1151-1230`; 2026-10-16-batch-01 G-001 (`evidence/p4-clipboard-env.txt`).
- The presentation: LLR-1001.1, HLR-1801..1803 (canon); `taskboard/views.py:6084-6540`, `taskboard/app.py:190-410`.
- The polish items: 2026-10-18-batch-01 `04-validation.md` (UX4-2, UX4-3, UX4-4).

### 1.5 Document overview
§2 the stories, premises and fork preconditions; §3 five HLRs; §4 five LLRs and the information-flow contract; §5 the validation strategy.

---

## 2. Overall description

### 2.1 Product perspective
Two of the five requirements change product code (`views`, `app`); two change only tests; one is a prototype round outside the package.

### 2.2 Product functions
1. The suite's standup and clipboard tests encode their intent and fail only on a product defect.
2. The presentation runs at any width and says what it cannot show; its hint row never overflows silently.
3. The operator gets a round of real-app variants for three polish items.

### 2.3 User characteristics
The maintainer runs the suite on Windows (the clipboard test is Windows-only) where other processes may hold the machine-global clipboard. The presenter uses the real app (`R`) in a terminal that can be resized at any time, keyboard-only. The operator judges design from captures on a page.

### 2.4 Constraints
Textual + Rich as shipped; no new dependency; every frame row exactly `width` cells (S1); the PRES-V3 oracle frames unchanged; no production change for the PROTOTYPE items; synthetic data; the operator's name nowhere.

### 2.5 Assumptions and dependencies
The fixtures `tests/present_board.py` and `tests/present_notes_board.py` stay as they are. Microsoft Edge is present for the round's PNGs (`views._find_msedge()` on this host → `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-1901 | As the maintainer running the full suite, I want a red test to mean a product defect — the two standup tests encoding their intent with the scrubbed placeholder name, and the clipboard roundtrip test skipping, with its reason, when Windows refuses to seed the clipboard — so that a clean run is 0 failures and a failure is worth reading. | operator 2026-10-18 (translated): «Continue with the backlog: fix the Standup tests and the other missing items»; backlog lane of 2026-10-16-batch-01 (the standup failures, the clipboard G-001) | READY |
| US-1902 | As a presenter whose terminal is resized narrow (a split screen, a small window), I want the presentation to keep running and to say what it cannot show — at any width — and its key hint to stay readable or visibly cut, so that `R` never crashes the app and never silently hides keys. | backlog lane of 2026-10-18-batch-01 (the pre-existing narrow-width assert; code-review F2) | READY |
| US-1903 | As the operator, the design authority for the TUI, I want the three open polish items (the dim view word and cut marks, the terse 80-column hint, the gantt view's 3-row note cap) shown as real-app variants next to today's look, at 118×31 and 80×25, on one page that compares them and recommends one, so that I can give a verdict before anything ships. | backlog lane of 2026-10-18-batch-01 (UX4-2, UX4-3, UX4-4); the operator's standing rule: TUI design changes need a prototype round with real-app renders and a verdict BEFORE implementation | READY |

#### Refinement log (one block per story)

**US-1901 — the suite tells the truth**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the maintainer (and every batch's gate run) · outcome = the full suite reports 0 failures; `test_win_clipboard_roundtrip` either passes, fails on a real roundtrip mismatch, or skips with a reason naming the environment's refusal · why = two known failures and an intermittent environment failure have been carried through five batch gates, so a red run no longer means anything · out of scope = the standup view's rendering (its name column stays 12 cells), the clipboard reader `models.grab_clipboard_text`
- **Feasibility (E, S):** implementation path = test-side only: the standup tests locate the operator's row by the name as the standup paints it (the 16-cell placeholder cut to the 12-cell name column with `…`); the clipboard test's loop moves into a helper that returns a skip reason when the machine never lets the sample be seeded and confirmed and still raises on a mismatch · dependencies/unknowns = none · fits one batch? = yes, one increment with no source file
- **Evaluability (T) — behavioral, black-box:** When the maintainer runs the full suite, it reports 0 failures; when `Set-Clipboard` is refused during the clipboard test's setup, the test is reported SKIPPED with the refusal in its reason; when the clipboard holds the sample and the reader returns something else, the test FAILS (AT-1901, AT-1902).
- **Open questions:** none.
- **Classification:** `READY`.

**US-1902 — the presentation at any width**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = a presenter in the real app (`R`) · outcome = below 36 columns the frame shows, in `mut`, the longest of five rungs that fits (`widen to 36+ columns · esc leave` … `36+`), no key but `esc` acts there and `x` notifies `Widen the terminal to 36+ columns to export` instead of writing a file; widened again, the frame is back as it was; the hint row under the frame shows the first of four wordings that fits (long, short, compact `⇥ ←→ ␣ x esc`, then the view switch and `esc`), below 36 `esc leave` and the hidden count, cut with a visible `…` when needed · why = the app dies on an `AssertionError` when the terminal is narrowed below 36 columns with `R` open, and the hint is clipped silently below 58 · out of scope = a narrow layout of the gantt field itself (a design change), the frame at 36 and above (byte oracles PRES-V3 unchanged)
- **Feasibility (E, S):** implementation path = `views.render_present` returns the narrow rung before the column split when `width < 36`; `PresentScreen` guards its actions below 36 and `_hint` tries its wordings longest first and truncates the last · dependencies/unknowns = none (probed on a scratch worktree, §2.7 P-7) · fits one batch? = yes, one increment, 2 source files
- **Evaluability (T) — behavioral, black-box:** When the presenter opens `R` at 118×31 and the terminal is resized down to 1 column, the app keeps the presentation open, the frame below 36 reads the rung for that width, keys there change nothing and `x` writes nothing; back at 118 the frame is the one before the narrowing; the hint row never exceeds its row and ends in `…` whenever it is cut (AT-1903, AT-1904).
- **Open questions:** none — the wording is fixed text; the operator sees it in the evidence captures.
- **Classification:** `READY`.

**US-1903 — the polish prototype round**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the operator · outcome = `prototypes/backlog_polish/` holds, for each of the three items, the current look and one or two variants captured from the running app headless (`export_screenshot` → SVG → PNG through `views.save_present_png`) at 118×31 and 80×25, and one self-contained HTML page (prose in Spanish, UI in English) that compares them and recommends one per item · why = the standing rule: no TUI design change ships without a prototype round and a verdict · out of scope = any change under `taskboard/` for these items (the variants live in the prototype's own patches); implementing the verdict
- **Feasibility (E, S):** implementation path = a capture script that patches the presentation's tones, hint wordings and note cap inside the prototype process, the app untouched; a page builder embedding the PNGs (the `prototypes/present_views/` pattern) · dependencies/unknowns = Microsoft Edge for the PNGs (present on this host; the earlier rounds used it) · fits one batch? = yes, one increment with no source file
- **Evaluability (T) — behavioral, black-box:** When the operator opens `prototypes/backlog_polish/backlog-polish-prototype.html`, each item shows the current look and its variants at both sizes as images from the real app, and a recommendation (AT-1905).
- **Open questions:** none for the round; the verdict is the operator's.
- **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | The two standup tests fail because the scrub `6bff525` replaced a roster name that fit the standup's 12-cell name column with the 16-cell placeholder, which the standup paints cut to `username_su…`, so the tests' substring search for the whole placeholder finds no row | premise | TRUE | `git show 6bff525 -- tests/test_team_views.py` → 5 lines changed, the old roster name 6 characters long (measured, not printed); `views.py:4303` `name_w = min(12, …)`, `:4304` `fit(name, name_w)`; probe: `render_standup(…, width=80)` paints `▌ username_su… ▱▱▱▱▱ —` and `▎ Ana          ▱▱▱▱▱ —`; `pytest tests/test_team_views.py` → `2 failed, 251 passed`, both on `"username_subject" in …` (`:78`, `:103`) | the defect is in the tests, not the source: the tests locate the row by the name as painted |
| P-2 | `Set-Clipboard` refused during the setup exits non-zero and the current test turns that into a FAILED assertion | premise | TRUE | `tests/test_app.py:1214-1217` (`assert setup.returncode == 0, "SETUP failed — this is the environment…"`); `.dev-flow/2026-10-16-batch-01/evidence/p4-clipboard-env.txt`: `AssertionError: SETUP failed … "Set-Clipboard : Requested Clipboard operation did not succeed.` ×2 | HLR-1902 skips that case with its reason |
| P-3 | `render_present` raises `AssertionError` at every width 1–35 and at none of 36–120, in both views, with and without a cursor, on both presentation boards | premise | TRUE | sweep on `base_ref` (widths 1–120 × heights 1, 2, 5, 24 × `gantt`/`split` × cursor `tw3`/`None` × `present_board`/`present_notes_board`) → `AssertionError @_present_finish:6464 widths 1 - 35` for each of the four (board, view) groups, nothing else | the narrow frame starts below 36 |
| P-4 | 36 is the narrowest width whose gantt field keeps a cell: below 100 the label is 20 and the chip 13 | premise | TRUE | `views.py:6084-6090` (`field_w = width - label_w - 1 - 1 - chip_w`, `label_w = 30 if wide else 20`, `chip_w = 13`) → `field_w = width - 35`: 1 at 36, 0 at 35 | `PRESENT_MIN_WIDTH = 36` |
| P-5 | The running app dies when `R` is open and the terminal is narrowed below 36 columns | premise | TRUE | probe on `base_ref`: the app at 118×31, `R`, `resize_terminal(60, 12)` … `(35, 12)` → the run ends on `AssertionError: (36, 35, '   today Wed Sep 30                 ')` from `_present_finish` | AT-1903 drives the same resizes |
| P-6 | The hint row's short wording is wider than its row below 58 columns in the gantt view (65 in the split view), and nothing shorter exists | premise | TRUE | `app.py:275-293`: two wordings, the short one taken whenever the long one does not fit; `cell_len("1 gantt 2 split ⇥ · ←→ · ␣ hide · a all · x export · esc")` = 56 (+ 7 for `pgdn · ` in split) against `w - 2` | HLR-1904 adds the compact and `esc` wordings, the narrow wording and the cut |
| P-7 | With the narrow frame (the five rungs, `mut`), the narrow key guard and the four wordings in place (probed on a scratch worktree of `base_ref`), every width 0–120 renders a frame of exactly `height` rows of `width` cells, the hint never exceeds `w - 2` cells, and the presentation tests at 118/80 stay green | premise | TRUE | scratch worktree with the edits: the sweep of P-3 over widths 1–120 → no exception, every row `width` cells; widths 0–36 at height 3 → row 0: 0 `''` (3 empty rows), 1 `…`, 2 `3…`, 3–7 `36+`, 8–13 `36+ cols`, 14–19 `needs 36+ cols`, 20–31 `widen to 36+ columns`, 32–35 `widen to 36+ columns · esc leave`, 36 `◆ PRESENT · Website Redesign  gantt`; the hint probe over widths 1–140 × both views × 0/3/10 hidden on a 12-task project → `cell_len ≤ max(0, w - 2)` everywhere, first widths per wording: gantt 0 hidden compact 36 · short 58 · long 84; 3 hidden esc 36 · compact 41 · short 69 · long 95; 10 hidden esc 36 · compact 42 · short 70 · long 96; split 0 hidden compact 36 · short 65 · long 97; 3 hidden esc 36 · compact 46 · short 76 · long 108; 10 hidden esc 36 · compact 47 · short 77 · long 109; below 36: empty at 1–2, cut from 3, `esc leave` whole from 11 (0 hidden), `esc leave · 3 hidden` from 22, `esc leave · 10 hidden` from 23; `pytest tests/test_present.py tests/test_present_views.py tests/test_present_views_app.py tests/test_present_hide.py` → `78 passed` | these are the literal tables TC-1903 and TC-1904 pin |
| P-8 | The round files that no longer import are exactly six, all in `prototypes/present_rulers/` and `prototypes/present_views/` | premise | TRUE | on `base_ref`, `python -c "import <m>"` in each round directory for every `.py`: `ImportError: cannot import name '_present_note_lines'` for `present_rulers/{proto,app_capture}.py`, `present_views/{views_proto,views_d,app_capture,app_capture2}.py`; `build_html.py` ×2, `legend_proto.py`, `fixture.py` import | six `HISTORICAL` notes (doc) |
| P-9 | The presentation's three polish points are literals inside functions (no name to patch): the view word's tone, the cut marks' tone, the gantt note cap, and the hint's wordings | premise | TRUE | `views.py:6502` (`c(f"  {escape(view)}", "dim")`), `:6240`, `:6241`, `:6273` (the cut and edge marks, `"dim"`), `:6532` (`_present_cut(rows, 3, width - 6)`); `app.py:280-286` (the wordings); `app.py:36` binds `render_present` at import | the round forks whole functions in its own process (ARCHITECTURE §3) |

- **Premise evaluation:** 9 premise(s) · ✅ TRUE ×9

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane: three increments in order on one branch, one owner (the orchestrator) holds the trunk.

---

## 3. High-level requirements (HLR)

### HLR-1901 — The standup marks the operator's own row, whatever the name's length
- **Traceability:** US-1901
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2, LED-2026-10-18-batch-02.3
- **Statement:** When the standup view paints the roster, the system shall mark the operator's own row with the bright spine `▌ ` and every teammate's row with the muted spine `▎ `, paint each member's name in the 12-cell name column — whole when it fits, else its first 11 cells and `…` — and paint a member whose last push is past the stale window in the `over` tone and the operator's fresh row never in it.
- **Rationale (informative):** the standup's behaviour is unchanged; its two tests lost their intent when the scrub made the fixture's name longer than the column.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_team_views.py`
- **Numeric pass threshold:** every node passes; AT-1901: the app on a board joined to a synthetic team folder (`username_subject` as the operator, `Ana` as a teammate), key `8`, at 120×40: the painted row whose name cell is `username_su…` starts with `▌ `, the row whose name cell is `Ana` padded to 12 starts with `▎ `.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `8` → the STANDUP frame; the operator's row reads `▌ username_su…`, the teammate's `▎ Ana`.
  - **Shipped surface:** key `8` → the board panel `#board` in standup mode.
  - **Acceptance test(s):** AT-1901
  - **Boundary catalog (QC-3):** ☑ boundary (a 12-cell name → whole; a 13-cell name → 11 cells and `…`; the 16-cell placeholder → cut; a 3-cell name → whole) ☐ empty — none: the roster-empty and team-off frames are pinned by existing tests ☐ invalid — none: no input text ☐ error — none
  - **Negative control:** the repaired tests and AT-1901 go RED when `render_standup` gives the operator's row the muted spine (mutation at increment 001, `evidence/mutation-001.txt` — planned); on `base_ref` the two standup tests are RED (`2 failed`, P-1, executed).

### HLR-1902 — The clipboard test fails on the product, never on the machine
- **Traceability:** US-1901
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2
- **Statement:** When the clipboard roundtrip test runs on Windows, the suite shall report it SKIPPED, with a reason quoting the refusal, when `Set-Clipboard` refused the sample on every attempt; and shall report it FAILED when an attempt found the sample still held by the independent oracle after the reader ran and `grab_clipboard_text` had returned anything else, or when the sample was set on some attempt but no attempt found it still held after the read.
- **Rationale (informative):** five batch gates carried a red that was the machine refusing `Set-Clipboard`; a skip quoting the refusal keeps the run honest, while a mismatch — and a clipboard that never holds what was just set, which a reader that disturbs the clipboard would also cause — still accuse the code.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider -rs tests/test_app.py -k "clipboard_roundtrip or TC_1902 or AT_1902"`
- **Numeric pass threshold:** AT-1902 passes: the real `test_win_clipboard_roundtrip` body, run with the module's PowerShell runner `_ps` replaced by a fake that answers `Get-Clipboard -Raw` (the prior content) with `prior text`, every `Set-Clipboard` with exit 1 and `Set-Clipboard : Requested Clipboard operation did not succeed.`, and records every command → `pytest.skip` is raised, its message holding `Requested Clipboard operation did not succeed` and `5 attempts`; the fake saw 5 seeding commands and the restore `Set-Clipboard -Value 'prior text'`; no command reached a real PowerShell. On this host the real node passes or skips — a skip is recorded `not-run` for the roundtrip at P4, never `executed`.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a refused setup is a SKIP whose reason quotes the refusal.
  - **Shipped surface:** the pytest outcome of `tests/test_app.py::test_win_clipboard_roundtrip`, its machine faked at the one seam it already has (`_ps`, the PowerShell runner); no product symbol is patched (the mismatch arm, which needs the reader replaced, is TC-1902's).
  - **Acceptance test(s):** AT-1902
  - **Boundary catalog (QC-3):** ☑ error (refused on every attempt → skip; refused then contended → fail; contended on every attempt → fail) ☑ negative (held, a wrong value read → fail; TC-1902) ☐ empty — none: the sample is fixed ☐ invalid — none
  - **Negative control:** on `base_ref` AT-1902 is RED: the shipped test raises `AssertionError: SETUP failed` where a skip is required (`evidence/red-001.txt` — planned; base `tests/test_app.py:1214-1217`).

### HLR-1903 — The presentation runs at every width
- **Traceability:** US-1902
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2, LED-2026-10-18-batch-02.3, LED-2026-10-18-batch-02.4, LED-2026-10-18-batch-02.6
- **Statement:** When the presentation is painted at a width below 36 columns, the system shall paint, in `mut`, the longest of `widen to 36+ columns · esc leave`, `widen to 36+ columns`, `needs 36+ cols`, `36+ cols`, `36+` that fits the width (the last cut with `…` when even it does not), above blank rows; there, every presentation key but `esc`/`q` (leave) shall change nothing, and `x` shall write no file and say `Widen the terminal to 36+ columns to export`; when the terminal is widened to 36 columns or more, the system shall paint the views' frames as shipped, in the state they had before the narrowing.
- **Rationale (informative):** narrowing the terminal with `R` open kills the app today (P-5); below 36 nothing on screen would show what a key did, so no key acts but the way out (ux-reviewer UX-1/UX-5/UX-7, architect A-6, A-11).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_narrow.py tests/test_present.py tests/test_present_views.py`
- **Numeric pass threshold:** AT-1903: the app on the notes board at 118×31, `R`, `→` (the cursor on the next task), `space` (that task hidden; one hidden), `2` (the split view); the frame painted then is kept; `resize_terminal` to 60, 40, 36, 35, 32, 30, 20, 14, 8, 5, 3, 1 columns, 12 rows each: `PresentScreen` stays the screen; frame row 0 at 36 and above starts `◆ PRESENT`, below 36 it is, stripped, the ladder's rung for that width (`widen to 36+ columns · esc leave` at 35 and 32, `widen to 36+ columns` at 30 and 20, `needs 36+ cols` at 14, `36+ cols` at 8, `36+` at 5 and 3, `…` at 1) and every other row is blank; at 30 columns `tab`, `→`, `pagedown`, `pageup`, `space`, `a` and `x` leave the frame unchanged (`1`, `shift+tab` and `h` reach the same guarded actions as `tab` and `→`), write the board file 0 times, create no `reports/` file and show the notification `Widen the terminal to 36+ columns to export`; resized back to 118×31 the frame equals the one kept before the narrowing — so `tab` (the view), `→` (the cursor), `space` and `a` (the hidden set) are each observed; `pagedown`'s guard is a regression pin only, since a resize resets the page (LED .5 of 2026-10-18-batch-01). The PRES-V3 frames still equal the painted frames (TC-1001, TC-1002 and `test_present_views.py`).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** narrowed below 36 the presentation says how wide it must be and stays open; keys there change nothing; widened again it is back as it was.
  - **Shipped surface:** key `R` → `PresentScreen` `#present-frame`; `resize_terminal`; key `x` → the notification, and `reports/` on disk.
  - **Acceptance test(s):** AT-1903
  - **Boundary catalog (QC-3):** ☑ boundary (35 / 36; each rung's first width — 32, 20, 14, 8, 3 — and widths 1–2, where even `36+` is cut; width 0, which the screen can pass) ☑ empty (no project, no open task, every task hidden — at a narrow width; TC-1903) ☐ invalid — none: no input text ☐ error — none: no failure path left
  - **Negative control:** on `base_ref` AT-1903 is RED: the resize to 35 raises `AssertionError` in `_present_finish` (P-5, executed; `evidence/red-002.txt` — planned).

### HLR-1904 — The hint row fits its row, or says it was cut
- **Traceability:** US-1902
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2
- **Statement:** When the presentation paints its hint row at 36 columns or more, the system shall paint the first of its four wordings that fits the row — the long one, the short one, the compact one (`⇥ ←→ ␣ x esc`, with `pgdn ` before it in the split view), then the view switch with `esc` alone — each after the view switch and before the hidden count; below 36 columns it shall paint `esc leave` and the hidden count; whatever does not fit shall be cut with a visible `…`, and the hint shall never paint more cells than its row holds.
- **Rationale (informative):** below ~58 columns the short hint was clipped silently by the widget (code-review F2 of 2026-10-18-batch-01); a compact wording keeps the keys longest, and below 36, where only `esc` acts, the way out and the hidden count are what survive (ux-reviewer UX-3, UX-6).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_narrow.py tests/test_present_views_app.py tests/test_present_hide.py`
- **Numeric pass threshold:** AT-1904: the app on the notes board at 118×31, `R`, `space` ×3 (three tasks hidden), resized to 50×20 → `#present-hint` reads `1 gantt 2 split ⇥ ←→ ␣ x esc · 3 hidden`, `2` → `1 gantt 2 split pgdn ⇥ ←→ ␣ x esc · 3 hidden`; resized to 40×20 (split) → `1 gantt 2 split esc · 3 hidden`; to 30×12 → `esc leave · 3 hidden`; to 15×10 → `esc leave · …`; each at most `w - 2` cells, the current view's name painted bold `#e6edf7` and the other `#5b6675` wherever the names show (the `Text` spans of `#present-hint`); at 80×25 and 118×31 the existing wordings are unchanged (TC-1808, TC-1604 green).
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a narrow presentation still names its keys in fewer words, then only the way out and the hidden count; a cut hint ends in `…`.
  - **Shipped surface:** `PresentScreen` `#present-hint`.
  - **Acceptance test(s):** AT-1904
  - **Boundary catalog (QC-3):** ☑ boundary (each wording's first width and the width below it, both views, 0 / 3 / 10 hidden; the 35/36 switch; a hint budget of 0 at widths 1–2) ☐ empty — none: the hint always has a wording ☐ invalid — none ☐ error — none
  - **Negative control:** on `base_ref` AT-1904 is RED: at 50 columns the short wording (56 cells and the count) is painted into a 48-cell row (P-6, executed; `evidence/red-002.txt` — planned).

### HLR-1905 — The polish round reaches the operator
- **Traceability:** US-1903
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2
- **Statement:** The batch shall deliver `prototypes/backlog_polish/` holding, for each of the three polish items (the dim view word and cut marks, the 80-column hint, the gantt view's note cap), the current look and one or two variants captured from the running app headless as SVG and PNG at 118×31 and 80×25, the shipped narrow frame and hint (HLR-1903, HLR-1904) at 30×12 and 50×20 for the operator's review, a manifest pairing each SVG with its PNG, and one self-contained HTML page — prose in Spanish, UI in English — that shows them side by side and recommends one look per polish item; no file under `taskboard/` shall change for them.
- **Rationale (informative):** the operator's standing rule: a TUI design change needs a prototype round with real-app renders and a verdict before implementation; the narrow frame and hint ship under the commission's FIX class and are shown for review (ux-reviewer UX-4).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_backlog_polish_round.py`
- **Numeric pass threshold:** AT-1905: the page exists, is `lang="es"`, carries no `src=`/`href=` to `http`, and embeds one PNG per manifest entry; every manifest entry's SVG is on disk with the SHA-256 the manifest records, its PNG beside it, and is a Textual `export_screenshot` (the `terminal-` classes) holding `PRESENT` or the narrow rung; every polish item has its current look and ≥ 1 variant at both sizes, each variant's SVG differing from the current look's at the same size and scene; each polish item carries `data-recommend="<capture id>"` naming a capture of that item; its checker goes RED on a copy with a capture moved aside, a variant equal to its current look, or an external `href` (the node's own arms). Retirement: the round folder and this test leave together, in the batch that implements the verdict.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** one page: three polish sections, each with the current look, its variants at both sizes and a recommendation, and the narrow frame for review.
  - **Shipped surface:** `prototypes/backlog_polish/backlog-polish-prototype.html` (a file the operator opens).
  - **Acceptance test(s):** AT-1905
  - **Boundary catalog (QC-3):** ☑ empty (a capture missing; a variant equal to the current look; an external resource — each RED in the node) ☐ boundary — none: fixed sizes ☐ invalid — none ☐ error — none
  - **Negative control:** AT-1905 is RED before the round exists (the folder is absent on `base_ref`) and on each of its three corrupted copies (`evidence/red-003.txt` — planned).

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-1901.1 — The standup tests find the row by the name as painted
- **Traceability:** HLR-1901
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2, LED-2026-10-18-batch-02.3, LED-2026-10-18-batch-02.5
- **Statement:** `tests/test_team_views.py` shall locate a member's standup row as the row whose name cell — on the row stripped of its padding, the 12 cells after the 2-cell spine — equals `views.fit(name, 12)`, and shall keep both repaired tests' assertions: the operator's row starts with `▌ `, the teammate's with `▎ `, the stale teammate's row holds `HEX["over"]` and the operator's fresh row does not; `render_standup` itself is unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_team_views.py -k "standup"`
- **Numeric pass threshold:** TC-1901 passes: the two repaired nodes, and the name-column arm — a roster of a 12-cell name (`twelve_cells`), a 13-cell name (`thirteen_cell`) and the placeholder paints `twelve_cells`, `thirteen_ce…` and `username_su…` in their rows' name cells, each found by the locator and by no other row.
- **Negative control:** the repaired nodes go RED when `is_self` picks the muted spine, and when the stale tone is painted on every row (mutations at increment 001 — planned).
- **Boundary catalog:** ☑ boundary (12 / 13 cells; the 16-cell placeholder) ☐ empty — none ☐ invalid — none ☐ error — none

### LLR-1902.1 — One roundtrip helper decides pass, skip or fail
- **Traceability:** HLR-1902
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2, LED-2026-10-18-batch-02.4
- **Statement:** `tests/test_app.py` shall provide `_clipboard_roundtrip(seed, ours, oracle, sample, attempts=5)` that, per attempt, calls `seed(sample)` (returning `None` when the clipboard took it, else the refusal text) and, when it took it, `ours()` then `oracle()`; it shall return `None` on the first attempt whose oracle still holds the sample and whose `ours()` equals it; raise `AssertionError` naming the handle bug on the first attempt whose oracle holds the sample and whose `ours()` does not; after the last attempt raise `AssertionError` naming contention when some attempt seeded the sample; and return a skip reason quoting the last refusal and the attempt count when every attempt was refused. `test_win_clipboard_roundtrip` shall seed, read the oracle and restore through `_ps` only, skip with that reason, and restore the prior clipboard in every case.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_app.py -k TC_1902`
- **Numeric pass threshold:** TC-1902 passes on every platform with fakes: held and equal → `None`, `ours` called once; refused ×5 → a reason holding the refusal text and `5 attempts`, `ours` never called; refused once then held and equal → `None`; contended ×5 → `AssertionError` holding `contended`; refused ×4 then contended → `AssertionError` holding `contended`; contended then refused ×4 → `AssertionError` holding `contended`; a reader that empties the clipboard ×5 → `AssertionError` (never a skip); held and different → `AssertionError` holding `this IS the handle bug`.
- **Negative control:** TC-1902's refusal arm goes RED when a refusal raises instead of returning a reason; its contention arms go RED when contention returns a skip reason; its mismatch arm goes RED when a mismatch returns a reason (mutations at increment 001 — planned).
- **Boundary catalog:** ☑ error (refusal, contention, a disturbing reader) ☑ boundary (a refusal then success on attempt 2; four refusals then contention) ☐ empty — none ☐ invalid — none

### LLR-1903.1 — The narrow frame
- **Traceability:** HLR-1903
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2, LED-2026-10-18-batch-02.3, LED-2026-10-18-batch-02.7
- **Statement:** `taskboard/views.py` shall define `PRESENT_MIN_WIDTH = 36` and `PRESENT_NARROW`, the five rungs of HLR-1903 longest first, and `render_present`, when `width < PRESENT_MIN_WIDTH`, shall return `to_text` of one row `_pad(c(escape(fit(rung, width)), "mut"), width)`, `rung` the first of `PRESENT_NARROW` whose cell width is at most `width` (else the last), and blank rows to `height`, before reading the project, the view, the cursor or the scroll; at width 0 every one of the `height` rows is empty. `PresentScreen` shall take no action for `1`, `2`, `tab`, `shift+tab`, every key bound to `move` (the arrows and `h j k l`), `pagedown`, `pageup`, `space` and `a` while its width is below `PRESENT_MIN_WIDTH`, and `x` there shall only notify `Widen the terminal to 36+ columns to export` (warning).
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_narrow.py -k TC_1903`
- **Numeric pass threshold:** TC-1903 passes: over widths 0–35 and 36, 37, 50, 79, 80, 99, 100, 118, 120 × heights 1, 5, 31 × `gantt`/`split` × cursor `tw3`/`None` × scroll 0/3 × the two presentation boards plus a board with no project and a project with every task hidden: no exception; exactly `height` rows; each row exactly `width` cells; below 36 row 0 is the rung for that width (the literal table: 0 → empty, 1 → `…`, 2 → `3…`, 3–7 → `36+`, 8–13 → `36+ cols`, 14–19 → `needs 36+ cols`, 20–31 → `widen to 36+ columns`, 32–35 → `widen to 36+ columns · esc leave`), its markup in `mut` (`HEX["mut"]`), the rest blank, the same for every view, cursor and scroll; at 36 row 0 starts `◆ PRESENT`.
- **Negative control:** TC-1903 goes RED when the threshold is 35 (the assert at 35) or 37 (the narrow frame at 36), when a rung is dropped, or when the message is painted `dim` (mutations at increment 002 — planned); on `base_ref` its widths 1–35 raise (P-3, executed).
- **Boundary catalog:** ☑ boundary (0, 1, 2, 3, 7/8, 13/14, 19/20, 31/32, 35/36) ☑ empty (no project; every task hidden) ☐ invalid — none ☐ error — none

### LLR-1904.1 — The hint's wordings and the cut
- **Traceability:** HLR-1904
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2, LED-2026-10-18-batch-02.4
- **Statement:** `PresentScreen._hint(w)` shall return an empty `Text` when `w - 2 ≤ 0`; below `PRESENT_MIN_WIDTH` it shall return `esc leave` plus ` · N hidden` when N tasks are hidden, in `#8b98a5`, truncated to `w - 2` cells ending in `…`; otherwise it shall take, in order, the long wording (two-space gaps after the view names), the short wording, the compact wording `⇥ ←→ ␣ x esc` (`pgdn ⇥ ←→ ␣ x esc` in the split view) and the wording `esc` (one-space gaps), each followed by ` · N hidden`, and paint the first whose cell width is at most `w - 2`, truncating to `w - 2` cells with `…` if none does; the current view's name bold `#e6edf7`, the others `#5b6675`, the keys `#8b98a5`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_narrow.py -k TC_1904`
- **Numeric pass threshold:** TC-1904 passes over widths 1–140 × both views × 0, 3 and 10 hidden (a 12-task project): the hint is at most `max(0, w - 2)` cells; the wording at each width is the one of the literal threshold table of P-7 (gantt: 0 hidden compact 36 · short 58 · long 84; 3 hidden `esc` 36 · compact 41 · short 69 · long 95; 10 hidden `esc` 36 · compact 42 · short 70 · long 96; split: 0 hidden compact 36 · short 65 · long 97; 3 hidden `esc` 36 · compact 46 · short 76 · long 108; 10 hidden `esc` 36 · compact 47 · short 77 · long 109; below 36 `esc leave` and the count, whole from 11 / 22 / 23 columns, cut with `…` from 3, empty at 1–2), each threshold and the width one below it asserted with the literal strings; the current view's span bold `#e6edf7`; with `present_hidden` patched to 123456 tasks, at 36 columns the `esc` wording overflows and is cut to 34 cells ending in `…`.
- **Negative control:** TC-1904 goes RED when the compact wording is removed, when the truncation is removed, when the zero-budget guard is removed, or when the narrow branch keeps the view names (mutations at increment 002 — planned); on `base_ref` it is RED below 58 columns (P-6, executed).
- **Boundary catalog:** ☑ boundary (each threshold and one below; 35/36; widths 1–2; a two-digit hidden count) ☐ empty — none ☐ invalid — none ☐ error — none

### LLR-1905.1 — The round's captures come from the running app, its forks stay in its process
- **Traceability:** HLR-1905
- **Ledger:** LED-2026-10-18-batch-02.1, LED-2026-10-18-batch-02.2, LED-2026-10-18-batch-02.3
- **Statement:** `prototypes/backlog_polish/capture.py` shall run `TaskboardApp` headless on the synthetic notes board with the calendar frozen, press the keys a presenter presses, and write each frame with the app's own `export_screenshot()` as SVG, with `views.save_present_png` as PNG, and each pair's SHA-256 into `out/manifest.json`; each variant shall be applied by rebinding, inside the capture process only, `taskboard.app.render_present`, `PresentScreen._hint` or `views._present_cut` to a fork the script holds, and restored before the next look; the script shall write only under `prototypes/backlog_polish/`.
- **Validation:** `inspection` (the write-path and diff property; the captures themselves are AT-1905's `test`)
- **Executed verification:** `git diff --stat <increment 002's commit> -- taskboard/` after running the script → empty; `grep -n "write_text\|write_bytes\|open(" prototypes/backlog_polish/*.py` → only paths under the round's folder; AT-1905's `terminal-` class and manifest checks.
- **Numeric pass threshold:** the diff is empty; every write path is under `prototypes/backlog_polish/`; every SVG passes AT-1905.
- **Negative control:** AT-1905 goes RED on a capture that is not an app export (a hand-written SVG without the `terminal-` classes) and on an SVG whose digest disagrees with the manifest — the node's own arms at increment 003 (planned).
- **Boundary catalog:** none — a fixed set of scenes and sizes, no input class

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the presentation frame at a narrow width, from the terminal size to the screen and the export
  SOURCE : the terminal size (PresentScreen.size); the board file on disk
  NODES  :
    - fn    : views.render_present's narrow branch (width < PRESENT_MIN_WIDTH)
      owner : LLR-1903.1
    - fn    : app.PresentScreen._hint, the wording choice and the cut
      owner : LLR-1904.1
  SINK   : the terminal surface (#present-frame, #present-hint) and the x export (reports/present-*.svg, .png)
```

```
FLOW: the suite's verdict on the standup and the clipboard roundtrip
  SOURCE : a synthetic team folder and board (tmp_path); the machine-global Windows clipboard
  NODES  :
    - fn    : the standup row locator in tests/test_team_views.py
      owner : LLR-1901.1
    - fn    : tests/test_app.py::_clipboard_roundtrip
      owner : LLR-1902.1
  SINK   : the pytest outcome (passed / skipped with its reason / failed)
```

```
FLOW: the polish round, from the running app to the operator's page
  SOURCE : tests/present_notes_board.py (synthetic), the frozen calendar
  NODES  :
    - fn    : prototypes/backlog_polish/capture.py (the forks, export_screenshot, save_present_png)
      owner : LLR-1905.1
  SINK   : prototypes/backlog_polish/out/*.svg, *.png and backlog-polish-prototype.html
```

- **Part B — boundary decomposition:** `no — no component a consumer addresses on its own changes: the narrow frame and the hint are the existing #present-frame and #present-hint widgets, addressed as before.`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer 0: `_clipboard_roundtrip` (cyclomatic ≥ 3) through TC-1902; `_hint` (a loop and four branches) through TC-1904; the narrow branch of `render_present` through TC-1903. Layer A: TC-1901..TC-1904 (renderer, helper and method level), LLR-1905.1 by inspection. Layer B: AT-1901, AT-1903, AT-1904 drive the real app headless (`run_test`, keys and `resize_terminal`); AT-1902 drives the shipped test body with its PowerShell runner `_ps` faked (the machine, not the product); AT-1905 reads the round's files on disk and corrupts copies of them.

### 5.2 Batch acceptance criteria
- every LLR has a passing TC (LLR-1905.1 its inspection); every story a passing AT through its surface;
- every new assertion RED on `base_ref` or by a recorded mutation; mutants KILLED on the new logic;
- the full suite: 0 failures; `test_win_clipboard_roundtrip` passes or skips with its reason; transcript under the batch's evidence;
- real-app captures (SVG and PNG) of the narrow frame and hint at 30×12 and 50×20 in the round (HLR-1905);
- inspection: `grep -n HISTORICAL` finds the note, with the last commit each file ran on, in each of the six round files of P-8; `grep -n "PRES-C\|PRES-R\|hybrid"` finds none left in the presentation section header of `taskboard/views.py` or the TC-1001 banner of `tests/test_present.py`;
- the RED and mutation transcripts the HLR/LLR negative controls mark `planned` exist before their increment's gate (`evidence/red-00N.txt`, `mutation-00N.txt`);
- the PRES-V3 frames unchanged; no file under `taskboard/` changed by increment 003.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
See `PLAN.md` §Key decisions and `docs/ARCHITECTURE.md` (amended by this batch).
### 6.3 Open risks
- **Security questions (the P1 scan):** `devflow-scan-spec.py` over this document, 2026-10-18: 65 patterns, 5 control rows ok, `flags: truncate, escape`, `security_required: true`, exit 1. Answered: `truncate` is Rich's `Text.truncate` of the hint row's own fixed wording (LLR-1904.1) — no table, no file, no data is truncated (C5 not fired); `escape` is Rich's markup `escape` over the narrow frame's fixed message (LLR-1903.1) — no board-file text enters a new markup row, the hint is a `Text` built with `append` and never parsed as markup (C8 not fired). No auth, secret, external integration, sensitive data, network or new input surface (C1–C4, C6, C7 not fired); the clipboard test reads and restores the machine clipboard exactly as it already did. No open security risk.
- The narrow frame's and the third wording's text are new UI strings the operator has not seen; the evidence captures carry them to the close.
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-18-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```
