# Validation — taskboard — Batch 2026-10-25-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

**`Mode`:** `validation`

## ✅ Verdict (read first)

> **Reserved field names.** `Result` · `Gate run` · `Layer 0` · `Evidence checklist` · `⏸ DEFER` — parsed literally, never translated.
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.

- **Result:** PASS
- **Gate run:** `env -u NO_COLOR python -m pytest -q -rs -p no:cacheprovider tests/<113 files in 3 disjoint chunks>` ·
  exit 0 on all three chunks · HEAD `0ffde24a079ba0a41563a6fcfba41f728625bb31` (the captures-evidence commit;
  `git diff 409a575 0ffde24` touches `.dev-flow/.../captures/` evidence only — no source change between
  the shots and the gate) · executed by the orchestrator (C-25), three SEQUENTIAL chunks, nothing in
  parallel: chunk00 **1440 passed** (`evidence/suite-p4-chunk00-run.txt`), chunk01 **959 passed**
  (`evidence/suite-p4-chunk01-run.txt`), chunk02 **879 passed** (`evidence/suite-p4-chunk02-run.txt`,
  holds `tests/test_present_note_highlights.py`) · total **3278 passed, 0 skipped, 0 failed**.
- **Baseline reconciliation (COND-2 / Q5 deviation, named per packet §6):** HLR-2905's threshold text
  contemplated a full-suite P3 baseline; per the operator's standing rule the full suite runs ONLY at P4.
  The executed pre-change baseline is therefore the 9 affected suites at 200 passed, run at base_ref
  (`evidence/baseline-affected.txt`); the post-change affected run holds the identical 200
  (`evidence/suite-affected.txt`, sha-verified) → Δ0 in the affected suites. The full-suite reconciliation:
  commission baseline 3258 + 20 new nodes = 3278 expected = 3278 collected.
- **Clipboard delta (named, not smoothed — batch-01's convention):** the commission's clause allows no
  skip other than TC-1902 (`tests/test_app.py`, chunk00). Today the machine allowed Set-Clipboard: TC-1902
  RAN and PASSED — 0 skips across all three chunks. The suite is stronger than the contract's allowance;
  no other skip, no fail.
- **Layer 0:** 10 unit arms met the criterion (5 `test_L0_tone_row_*` + marker-free twin + the `k==1` cut
  seat + 3 post-review arms) · the mutation battery names a reddening mutation per LLR seat; arm e
  resolves 3 layer-0 nodes (2 RED, 1 designed survivor — the alarm-path node, named per the C-40 rider).
- **Requirements:** 11/11 pass (5 HLR + 6 LLR) · 0 blocker fails.
- **Black-box acceptance (Layer B):** ✓ every story's AT observes its outcome through the shipped surface
  (boundary + negative): AT-2901..AT-2905 each realise in exactly one on-disk node in
  `tests/test_present_note_highlights.py` (C-18), re-executed inside the green gate chunk02; PLUS the
  family-D painted-result evidence: 4 real-terminal PNG captures whose READY gate asserted the three tone
  hexes and 0 marker runs on the live composited frame (DDR UX-1, discharged here).
- **Surface-reachability (bidirectional):** ✓ all named inputs (highlight markers, mentions, bullets,
  unclosed marker, hostile Rich/ANSI/link payload) AND outputs (the painted rows of views 1/2 on screen,
  the emitted `reports/present-…-split-….svg` bytes) reached/observed at the surface.
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — old two-arg
  `_paint_marks(txt, marks)`: zero test hits; old `(lead, text)` row asserts: surviving hits all unwrap
  pieces (`tests/test_present_views.py:92-100, 189-190, 362-364`).
- **Test ledger:** ✓ reconciles — base 3258 − D 0 + A 20 = post 3278; actual collected 3278
  (1440+959+879); passed/full 3278/3278. Secondary pin: affected suites base 200 (base_ref) = post 200, Δ0.
- **Evidence checklist (qa-reviewer):** qa-reviewer (evaluation; execution attributed per row) · 10 of 10 rows ✓ with evidence.

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part. — every line is ✓.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `_tone_row` re-attribution | whitespace drops at row breaks; substitutions; empty row stays put; zero misattributed chars; alarm outside whitespace | `test_L0_tone_row_whitespace_drops_at_row_breaks` · `…_substitutions` · `…_empty_row_stays_put` · `…_zero_misattributed_chars` · `…_alarm_outside_whitespace` | pass — in `suite-001.txt` (20 passed) and gate chunk02; executed by the software-dev implementer at P3, re-executed by the orchestrator's gate |
| marker-free width equivalence | a note and its marker-free twin wrap identically (Δ0 rows, Δ0 cells) at w ∈ {7,12,24,30,50} | `test_L0_marker_free_twin_wraps_identically[5 params]` | pass — same evidence |
| the `k==1` cut seat | the cut row is glyph-split first, then painted lead/span/tag piece by piece | `test_L0_cut_seat_k1_paints_lead_span_and_tag` | pass — same |
| Unicode whitespace at wrap boundaries (code-review F1) | NBSP/em-space at a textwrap break cannot crash the render | `test_L0_unicode_whitespace_at_wrap_boundaries` · `test_L0_unicode_whitespace_fuzz_pin` | pass — landed RED-first in `abe324c`; re-run against the shipped bytes |
| clip budget guard (code-review F3) | the composed note row never exceeds its width | `test_L0_note_markup_clip_never_exceeds_its_width` | pass — same |

**Measured by mutation, never by line coverage.** Executed by the spawned implementer; restore hashes
re-verified by the orchestrator; transcript `evidence/mutation-001.txt` (sha-verified):

| Unit / seat | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| AT-2901 / LLR-2901.1 tokenise-before-wrap | bypass `highlight_segments`: paint raw text | ✓ RED `12 marker chars, 0 tone colours` — both runs (pre-F1 md5 `52bdb41e…`, post-F1 shipped bytes md5 `778eb68a…`) | mutation-001.txt arm a |
| AT-2902 / LLR-2902.1 visible-width wrap | tokenise AFTER the wrap (`plain := body`) | ✓ RED, 2 nodes | arm b |
| AT-2903 / LLR-2903.1 export renders composed frame | strip the three tone hexes at `save_present_svg` | ✓ RED | arm c |
| AT-2904 mention / LLR-2904.1 | drop the mention pass in the toned paint | ✓ RED | arm d1 |
| AT-2904 hostile / LLR-2901.2 escape | remove `escape` on toned segments | ✓ RED | arm d2 |
| layer-0 `_tone_row` | permute every `soon` char to `over` | ✓ RED on 2 of 3 resolved nodes; the survivor is the alarm-path node (asserts the AssertionError — green by design, named per the C-40 rider) | arm e, `2 failed, 1 passed` |

All six arms: none stayed green; every restore hash-equals the pre-mutation md5, per arm, in both runs.

### UX walkthrough — trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| Open `R`, cursor on the task whose note holds `==…== !!…!! ++…++` (view 1, gantt): each span reads in its tone, no marker chars, rest in ink | real `TaskboardApp` in Windows Terminal (`wt.exe`), keys via the app's own `App._press_keys` path (`R`), 118x30 and 80x24 | each shot's READY gate exported the LIVE composited frame at capture time and asserted `#fbbf24`+`#f43f5e`+`#4ade80` in its styles, 0 runs of `==`/`!!`/`++`, the marker-free words present, `PresentScreen`/view `gantt`; the PNG itself ≥8 colours, re-verified from disk (18/13 colours sampled; 30,831 / 26,113 bytes) | pass — `captures/png/gantt_118x30.png`, `gantt_80x24.png`; AT-2901 node + captures; executor: orchestrator (batch-01 harness adapted) |
| Press `2` (view 2, split): every shown note block carries the tones at both sizes; the `++…++` span wrapped across two rows keeps `#4ade80` on both | same mechanism (`R`, `2`), 118x30 and 80x24 | same READY assertions on the live frame (view `split`); 16/13 colours sampled; 34,534 / 28,770 bytes | pass — `captures/png/split_118x30.png`, `split_80x24.png`; AT-2902 node + captures |
| Leave no trace | n/a | `assert-no-n01.ps1` as its own command: `no n01-* window left open`; no `n01-cap-*` temp home, no `n01-*.ready/.cmd` left in TEMP | pass — captures/README.md §Results |

**Mechanism used:** a UI test driver — real terminal windows of the shipped app, scripted keys, a scripted content check on the live composited frame (not a glance), PrintWindow grabs.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — the capture harness (shoot.ps1/shoot_real.py), 4/4 shots accepted on try 1, by the orchestrator |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — a human eyeball of all four PNGs against the README's per-shot criteria (agrees: marker-free, three coloured words, the green span wrapped across two rows at 118x30), by the orchestrator/operator |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — one-person team; no user population exists to recruit. Named, not smoothed. |

- **Method:** scripted walkthrough, synthetic board only (`Launch plan review`, pinned clock 2026-10-20 09:30), no real names, nothing in the real home.
- **Participants or population:** n/a — no user evaluation performed (one-person team).
- **Evidence of the evaluation:** `evidence/captures/` — README.md, 4 PNGs, capture-log.txt, the assert-no-n01 output quoted in the README.
- **Limits:** expert inspection is a single reviewer checking his own criteria; it does not establish usability with a real audience, and the absence of a user evaluation is a scope limit of the team, not evidence of acceptability.

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|---|---|---|---|---|---|
| HLR-2901 | test | `pytest … tests/test_present_note_highlights.py -k AT_2901` (node minted P3; RED probe at base_ref) | 0 marker runs; all three tone hexes ≥1; unmarked words in `#e6edf3` | pass | node in gate chunk02 (879 passed); P1 RED `red-p1.txt` probe 3: 12 marker chars, 0 tones |
| HLR-2902 | test | `-k AT_2902` at 118x30 and 80x24 | 0 markers; three tones; the wrap span's tone on every touched row; the marker-free twin fills the identical cell count | pass | gate chunk02; P1 wrap-counting probe (`red-p1.txt` probe 4) |
| HLR-2903 | test (emitted form, C-42) | `-k AT_2903` reads the exported SVG's bytes | three hexes present; no marker run; the words in the spans; 0 raw `<script` bytes (`&lt;`/`&amp;` only) | pass | gate chunk02; the emitted `reports/present-…-split-….svg` bytes |
| HLR-2904 | test | `-k AT_2904` (mention arm via view 2, literal arm via view 1, hostile payload inside) | the mention in bold `#f472b6` exactly once; unclosed `!!attention` verbatim in `#e6edf3`; the `• ` lead in `mut`, the span keeps its tone; the hostile row: 0 non-ink styles, 0 exceptions, 0 `\x1b` bytes | pass | gate chunk02; mutation arms d1/d2 RED |
| HLR-2905 | test | the P4 gate suite in 3 chunks + the affected suites re-run | 3278 = 3258+20 passed; only justified oracle updates; a marker-free row still paints `#e6edf3` (the style-only pin) | pass | chunk00/01/02 transcripts; `suite-affected.txt` 200 = `baseline-affected.txt` 200; the oracle files: `tests/test_present_views.py` (chunk02), `tests/test_people_look.py` (**chunk01**); executed by the orchestrator |
| LLR-2901.1 | test (unit) | the layer-0 arms + the P3 reverse-census grep (`_HIGHLIGHT_RE`/`==` in views.py lists the tokeniser as the only marker-syntax reader) | AT-2901's numbers; one tokeniser, no second parser | pass | layer-0 nodes in gate chunk02; mutation arm a RED; the census in increment-001 §4 |
| LLR-2901.2 | test (unit) | the hostile-input arm inside AT-2904's node | 0 style leaks, 0 raised exceptions, the hostile bytes all present escaped/verbatim, 0 `\x1b` | pass | gate chunk02; mutation arm d2 RED |
| LLR-2902.1 | test (unit) | AT-2902's wrap fixture + the width-equivalence arm (5 widths) | the span tone on both touched rows; Δ0 rows / Δ0 cells vs the marker-free twin | pass | gate chunk02; mutation arm b RED |
| LLR-2903.1 | inspection + test | `git diff` of the increment: no change under `save_present_svg`/`present_paths`/`present_all_export`; AT-2903 asserts the emitted bytes | an empty diff at the export functions; three hexes, no markers, 0 raw `<script` | pass | increment-001 §2 frozen set (byte-identical, git-diff verified); gate chunk02; mutation arm c RED |
| LLR-2904.1 | test (unit) | AT-2904's mention arm through the split view with a synthetic directory | the mention exactly once in bold `#f472b6`; the surrounding span keeps its tone on the same row | pass | gate chunk02; mutation arm d1 RED |
| LLR-2905.1 | inspection | the packet §2 diff census + the P4 suite | 0 modified files outside `taskboard/views.py` + tests; 0 hunks outside the note pipeline; 16 row-shape consumers updated in the two LED-2905-authorised files | pass | increment-001 §2 (SOURCE 1/4); the P4 gate green with the two named oracle files in chunk02/chunk01 |

### Layer B — behavioral (black-box)

| US | Acceptance test | Surface driven | Deliverable observed | repr · boundary · negative | Result |
|---|---|---|---|---|---|
| US-2901 / HLR-2901 | AT-2901 → `test_AT_2901_gantt_cursor_note_colours_highlights` | the `R` screen's gantt view by keys, the cursor on the highlighted task | the painted cursor-note rows on screen (+ `gantt_<size>.png`) | repr: three spans in tone · boundary: an exactly-one-marker-pair note fills a row, markers dropped · negative: the P1 RED at base_ref (12 markers, 0 tones); mutation arm a RED | pass — node in gate **chunk02** (879 passed); P3 `suite-001.txt`; the capture evidence |
| US-2901 / HLR-2902 | AT-2902 → `test_AT_2902_split_view_colours_highlights_two_sizes[118x30, 80x24]` | view 2 by keys at both room regimes | the painted note blocks under each heading (+ `split_<size>.png`) | repr: tones at both sizes · boundary: a span split by the row edge keeps its tone on both rows; the marker-free width equivalence · negative: the marker-counting wrap RED (`red-p1.txt` probe 4); mutation arm b RED | pass — gate chunk02; the captures |
| US-2901 / HLR-2903 | AT-2903 → `test_AT_2903_split_export_svg_carries_tones` | the `x` key in view 2 | the emitted file `reports/present-…-split-….svg` — bytes read from disk (C-42) | repr: hexes + words in the spans · boundary: a cursor-less export pinned by the existing export arms · negative: hostile `<`/`&`/`<script>` reach the file only escaped; mutation arm c RED | pass — gate chunk02 |
| US-2901 / HLR-2904 | AT-2904 → `test_AT_2904_mentions_bullets_unpaired_markers` | view 2 (mention arm) and view 1 (literal arm) by keys | the painted rows: the mention bold pink inside the tone; unclosed `!!attention` literal in ink; the `• ` lead unchanged | repr: coexistence · boundary: a mention the directory does not hold stays as typed · negative: the hostile Rich/ANSI/link payload renders literally; mutation arms d1/d2 RED | pass — gate chunk02 |
| US-2901 / HLR-2905 | AT-2905 → `test_AT_2905_the_regression_pin` | the whole app — the P4 gate suite | the full suite's pass state + the marker-free row's `#e6edf3` style pin | pin (invariant by construction; C-40 corollary) | pass — the 3-chunk gate, 3278 passed; the oracle files named: `tests/test_present_views.py` (**chunk02**), `tests/test_people_look.py` (**chunk01**) |

All Layer B rows: executed at P3 by the software-dev implementer (`suite-001.txt`) and re-executed in the
orchestrator's P4 gate chunk02. The P4 run is the execution of record; the qa-reviewer consumed, did not run.

### Bidirectional surface-reachability matrix

| Direction | US dimension / deliverable | Service param / producer | Reached at surface? | TC / AT | Status |
|---|---|---|---|---|---|
| input | note text with `==`/`!!`/`++` highlights | `task.notes` → `present_note_lines` | yes — typed into a real board, driven by keys | AT-2901/2902 | ✓ |
| input | a mention inside a span | directory marks → `_paint_marks` | yes — synthetic directory, split view by keys | AT-2904 | ✓ |
| input | an unclosed marker | the tokeniser | yes — view 1 by keys | AT-2904 | ✓ |
| input | a hostile Rich/ANSI/link payload | the escape seat | yes — inside AT-2904's node | AT-2904 | ✓ |
| output | the painted note rows, views 1/2 | the composed frame | yes — the live-frame export at capture time + 4 PNGs | AT-2901/2902 + captures | ✓ |
| output | the `x` SVG file | `save_present_svg` | yes — the file bytes read from disk | AT-2903 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed/full | reconciles? |
|---|---|---|---|---|---|---|
| 3258 (commission baseline; batch-01's collected post) | 0 | 20 | 3278 | 3278 (1440+959+879, 3 chunks) | 3278 / 3278 | yes |
| 200 (affected suites at base_ref, `baseline-affected.txt`) | 0 | 0 | 200 | 200 (`suite-affected.txt`, sha-verified) | 200 / 200 | yes — Δ0 in the affected suites (COND-2's executed-baseline row) |

### QA-P4 findings (folded — none forces iterate)

| # | Severity | Finding | Fold |
|---|---|---|---|
| QA-P4-01 | minor (citation — the batch-01 class) | the layer map must cite `tests/test_people_look.py` to **chunk01**, not chunk00 | folded — the Layer A HLR-2905 row and the Layer B AT-2905 row cite chunk01 |
| QA-P4-02 | minor (naming) | the shots ran at HEAD `409a575`, the gate at `0ffde24` (delta: 9 capture-evidence files, no code) | folded — the Gate run line names it, mirroring batch-01 |
| QA-P4-03 | minor (reconciliation) | HLR-2905's threshold literally asked for a full-suite P3 baseline; the executed baseline is the 9 affected suites at 200 (packet §6 deviation, COND-2) | folded — the Baseline reconciliation paragraph + the second ledger row discharge it |
| QA-P4-04 | info | TC-1902 (clipboard, chunk00) ran and passed — 0 skips; the commission's «no skip other than TC-1902» clause is satisfied a fortiori | named in the Clipboard delta line |
| QA-P4-05 | info | arm e's 1 green node is the designed alarm-path survivor (C-40 rider) | recorded as such in the mutation table |

### Evidence checklist — qa-reviewer (10 of 10)

- [✓] Acceptance criteria use Given/When/Then — §3 of `01-requirements.md`, each HLR carries Statement / observable outcome / threshold
- [✓] Explicit Expected per case — the numeric pass thresholds, per requirement
- [✓] Edge cases: empty (no-notes rows) · boundary (the wrap-split span, the exactly-full row) · invalid (unclosed marker, hostile payload) · error (none new — named per the QC-3 catalogs)
- [✓] Regression checklist exists — the HLR-2905 pin + the affected-suite Δ0 + the full 3-chunk gate
- [✓] Exit criteria stated — contract §5.2 (100% LLR coverage, ATs at the surface, 3258+20, the mutation kills)
- [✓] No real PII/secrets — synthetic boards, no real names (captures README §Method)
- [✓] Mode declared: `validation`
- [✓] Every case carries a result + executor: orchestrator (gate C-25, captures), software-dev implementer (P3 runs, battery), code-reviewer (packet §4b), qa-reviewer (this evaluation)
- [✓] Layer B: every AT observes the deliverable through the shipped surface with boundary + negative evidence (incl. the painted-result captures, DDR UX-1)
- [✓] Bidirectional surface-reachability: the matrix above, no gaps; no unfilled template placeholders in the returned rows
