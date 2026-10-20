# Validation — taskboard — Batch 2026-10-19-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

**`Mode`:** `validation`

## ✅ Verdict (read first)

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Result` · `Gate run` · `Layer 0` · `Evidence checklist` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.
>
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.
> A Spanish batch writes `- **Result:** PASS`, not `- **Resultado:** aprobado`: the label, the tokens and the
> reviewer-identity tokens below are the machine's vocabulary.


- **Result:** PASS-WITH-NOTES
- **Gate run:** `python -m pytest -q -p no:cacheprovider -rs --color=no` in a clean git worktree at commit `91d1f8c` (`feat/present-all` after increment 006, the batch's last code commit; 0 changed files), `NO_COLOR` unset · exit 0 · run and collected by the orchestrator · 2819 passed in 661.81s, 0 failed, 0 skipped — `evidence/suite-p4.txt`
- **Layer 0:** 3 unit(s) met the criterion · 3 carry a named reddening mutation (`Project.from_dict`'s load rule N1–N3; `PresentScreen._hint`'s wording choice Q2, Q13; `_all_layout`'s auto-fold P3, R1, S3 — all KILLED)
- **Requirements:** 12/12 pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ⚠ every named output observed at the surface but the PNG of the export (Edge-dependent, G-5); heights below 24 and widths 36–99 reached at the renderer, not through the app (G-3); `u` not driven in view 2 (G-4)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — the packets' B1 censuses re-ran green in `suite-p4.txt`; the round's committed files unchanged (`git diff bdf6e9d -- prototypes/present_portfolio` empty, qa-reviewer)
- **Test ledger:** ✓ reconciles (`2758 − 2 + 63 = 2819`)
- **Evidence checklist (qa-reviewer):** qa-reviewer — spawned with agents/qa-reviewer.md · 9 of 11 rows ✓ with evidence, 2 ✗ (the gate pending at review time — now run, above; bidirectional reachability: G-3..G-5, accepted below)

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `models.Project.from_dict` (the two keys) | decision — a type table of 18 values | `tests/test_present_all.py::test_TC_2102_show_in_present_is_false_only_for_the_json_false[*]`, `::test_TC_2102_present_rank_is_kept_only_as_an_integer[*]` | pass (`suite-p4.txt`) |
| `app.PresentScreen._hint` (view 3 and the `u` tail) | decision — four wordings × rail / no rail × counts | `::test_TC_2104_view_3s_hint_takes_the_first_wording_that_fits`; `tests/test_present_narrow.py::test_TC_1904_the_hint_takes_the_first_wording_that_fits` | pass |
| `views._all_layout` (auto-fold, drawn rows) | complexity ≥ 3 — the fold loop and the trim | `::test_TC_2103_the_frame_sweep[*]`, `::test_TC_2103_no_stop_hides_under_the_overflow_row` | pass |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `from_dict` | N1 bool accepted · N2 None written · N3 read truthy | yes | `evidence/mutation-002.txt` |
| `_hint` | Q2 the tail without `u` · Q13 view 3's middle wording dropped | yes | `evidence/mutation-004.txt` |
| `_all_layout` | P3 the cursor's project may fold · R1 cut rows kept · S3 no trim | yes | `mutation-003.txt`, `mutation-004-views.txt`, `mutation-004-review.txt` |

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| `R`, `3` shows every shown project on one ruler beside the rail, as the approved C | the real-app captures (`export_screenshot`) at 160×45 and 118×30 against `prototypes/present_portfolio/out/C-160-initial.svg`, `C-118-initial.svg`, row by row as text | the order, the rail, the folds, the chips equal; the hint's one-count tail and the tick row's label the declared differences | pass |
| at 80×24 the timeline takes the full width | `captures/view3-80x24.svg` | no rail (D5; the approved C-80 had a 12-cell rail — UX4-7, shown to the operator at the close) | pass |
| the hint keeps its labels at 118 with something hidden (UX-1) | the captures at 118/160 | `␣ hide`, `⇧↑↓ order`, `enter fold`, `a all` at 118; `u 3 hidden` | pass |
| `a` says what came back (UX-3) | headless run by the ux-reviewer: `R 3 u space esc a a` at 80×24 | `Shown again: 2 projects + 2 tasks`; the second `a` inert, no notice | pass |
| `u` lists the hidden and one comes back | the same run; `captures/seq-160x45-4-picker.svg`, `-5-shown.svg` | the picker over the dimmed presentation (after 005/006); at 7c4140a `space` on row 0 hid a shown project (UX4-1) — fixed in 006, the cursor opens on the first hidden row | pass after 006 |
| the milestone reads as a milestone | `captures/view1-118x31-before.svg` / `-after.svg` | a bar from today → a `◆` on Oct 25 | pass |

**Mechanism used:** the real app headless (Textual `run_test`, keys and resizes through the pilot) — the batch's `evidence/capture.py` and the ux-reviewer's own runs outside the repo (`scratchpad/uxw/`); PNGs rendered with Edge from the SVGs.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — by the ux-reviewer, and by AT-2101..AT-2106 in `suite-p4.txt` |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — ux-reviewer, pass-with-notes (UX4-1 major, fixed in 006; UX4-2 fixed in 006; UX4-3..UX4-7 minor, below) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the operator's verdict on the round is the human check |

- **Method:** the shipped app headless over the synthetic portfolio board, keys and resizes through the pilot, frames read as text and as PNGs.
- **Participants or population:** none — no user evaluation.
- **Evidence of the evaluation:** `evidence/captures/` (re-taken on `91d1f8c`); `evidence/suite-p4.txt`; the ux-reviewer's report (folded here).
- **Limits:** no real projector or terminal font (`␣` renders as a low mark in the capture font, UX4-6); `shift+arrow` in other terminals not tried (UX-8); the rail's `space` and `shift+↑/↓` on the rail driven by the ATs, not by the reviewer.

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-2101 | test | AT-2101, TC-2101 | one `◆` in the project `◆`'s column, no bar glyph, `due Oct 25` | pass | RED `red-001.txt`; M1–M5 KILLED |
| HLR-2102 | test | AT-2102, TC-2102 | the ranks and flags in the file; the restart order; the board gantt unchanged | pass | RED `red-002.txt`, `red-004.txt`; N1–N6, Q6 KILLED |
| HLR-2103 | test | AT-2103, TC-2103 | header, order, rail strings, widths, no rail at 80 | pass | RED `red-003.txt`, `red-004.txt`; P1–P8, R1, R2, S3 KILLED |
| HLR-2104 | test | AT-2104, TC-2104; the hint files | three views, the hand-off, the `-all` export, the literal hints | pass (G-2) | Q1–Q4, Q13, Q14, S1, S2 KILLED |
| HLR-2105 | test | AT-2105, TC-2105 ×2 | one save per change, none for a no-op; the caret; the notice | pass | Q5–Q8, Q11, Q15 KILLED |
| HLR-2106 | test | AT-2106, TC-2106 ×4 | the rows, the toggle, `nothing hidden`, the backdrop, the first row | pass | Q9, Q10, Q12, P7, P8 KILLED; `red-005.txt`, `red-006.txt` |
| LLR-2101.1 | test (unit) | TC-2101 ×11 | the sweep at four widths | pass | M1–M5 |
| LLR-2102.1 | test (unit) | TC-2102 ×22 | the load table, the save rule, the order, the pull | pass | N1–N6 |
| LLR-2103.1 | test (unit) | TC-2103 ×15 | the sweep, the round's text, the drawn stops | pass | P1–P6, R1, S3 |
| LLR-2104.1 | test (unit) | TC-2104 ×3 | the literal first widths | pass | Q1–Q3, Q13 |
| LLR-2105.1 | test (unit) | TC-2105 ×2 | counted saves; the resize | pass | Q5–Q8, S1, S2 |
| LLR-2106.1 | test (unit) | TC-2106 ×4 | rows, toggles, markup, backdrop, first row | pass | P7, P8, Q9, Q10 |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-2101 | AT-2101 — `tests/test_present_milestone.py::test_AT_2101_the_cut_over_weekend_reads_as_a_milestone` | `R`, `2` at 118×31 | `#present-frame` rows | repr: Cut-over weekend · boundary: TC-2101 (36 columns, a start date, no due) · negative: RED on base | pass |
| US-2102 | AT-2103, AT-2104 — `tests/test_present_all.py::test_AT_2103_the_portfolio_on_one_ruler`, `::test_AT_2104_three_views_one_cursor_and_the_export` | `R`, `3`, `tab`, `→`, `↓`, `1`, `x` at 160×45, 118×30, 80×24 | `#present-frame`, `#present-hint`, `reports/present-board-2026-10-19-all.svg` | repr: the portfolio · boundary: 80 (no rail), 118 · negative: RED on base | pass |
| US-2103 | AT-2102, AT-2105 — `::test_AT_2102_the_order_and_hidden_projects_survive_a_restart`, `::test_AT_2105_the_presenter_curates_view_3` | rail and timeline keys, a restart, the main gantt | `board.json`, the frame, the notice | repr: reorder + hide · boundary: the ends, `a` twice · negative: RED on base, unchanged bytes | pass |
| US-2104 | AT-2106 — `::test_AT_2106_u_lists_the_hidden_and_brings_one_back` | `space`, `u`, `space`, `esc`, `3`, `u`, `a`, `u` | `#picker-rows`, `board.json`, the frame | repr: two hidden · boundary: `nothing hidden` · negative: RED on base | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | widths 160, 118, 90, 80, 30 (pilot); 36–200 (renderer, method) | `PresentScreen.size` | yes at the five | AT-2103, AT-2104, TC-2105 (resize) | ✓ |
| input | heights 45, 31, 30, 24 (pilot); 6–14, 10 (renderer) | `render_present_all(height)` | the overflow row through the renderer only | TC-2103 | ⚠ G-3 |
| input | views 1, 2, 3 | `_view` | yes; `u` in view 2 shares view 1's path | AT-2104, AT-2106 | ⚠ G-4 |
| input | hidden counts 0, 1, 3 | `_hidden_count` | yes at 3 and 0 (pilot); 1 at the method | AT-2104, TC-2104 | ✓ |
| input | rail focus | `_rail` | yes | AT-2104, AT-2105, TC-2105 | ✓ |
| output | `#present-frame`, `#present-hint`, `#picker-rows` | `render_present_all`, `_hint`, `PresentHiddenPicker` | yes | AT-2103..AT-2106 | ✓ |
| output | `board.json` | `Board.save` | yes | AT-2102, AT-2105, AT-2106 | ✓ |
| output | the `-all` export SVG | `action_export` | yes, read from disk | AT-2104 | ✓ |
| output | the `-all` export PNG | `save_present_png` (Edge) | no — written only where Edge exists | — | ⚠ G-5 |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2758 (`suite-base.txt`: 2757 passed + 1 skipped on `bdf6e9d`) | 2 (TC-1604's two parametrize ids renamed with the hint wording, increment 004) | 63 (001: 12 · 002: 22 · 003: 13 · 004: 13 + the 2 renamed ids · 005: 1; 006: 0) | 2819 | 2819 | 2819 passed in 661.81s, 0 failed, 0 skipped | yes |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-1 | HLR-2105 | AT-2105 accepted the cursor's `⟦` in place of the folded caret | minor | fixed in 006 (`▸` read after `↑`) |
| G-2 | HLR-2104 | AT-2104 checks the tick row after `→`, not the cursor's row; several ATs read the private `_all_cur` | minor | accept; `BACKLOG.md` |
| G-3 | HLR-2103 | the overflow row at short heights is reached through the renderer, not the app | minor | accept (TC-2103's overflow node) |
| G-4 | HLR-2106 | `u` not driven in view 2 (view 1's path); AT-2106 closes the picker with `u`, not `esc` | minor | accept |
| G-5 | HLR-2104 | the exported PNG is never observed (Edge-dependent, as shipped) | minor | accept, as 2026-10-18-batch-03's G-2 |
| G-6 | ledger | packet 004 counted the net +13, not the two renamed TC-1604 ids | minor | recorded here |
| UX4-4 | HLR-2104 | at 80×24 view 3's hint is glyphs only (the specified third wording) | minor | `BACKLOG.md` |
| UX4-5 | HLR-2104 | the `-all` export carries the presenter's cursor (the `⟦` lead, the echoed span) and empty rows below | minor | `BACKLOG.md` |
| UX4-6 | — | `␣` is a low mark in the capture font | cosmetic | none |
| UX4-7 | D5 | the operator never saw 80×24 without the rail | info | shown at the close (`captures/view3-80x24.svg`) |

### Escaped-bug regression (if a defect escaped the suite)

none — no defect escaped the suite: the milestone bar was found by the round before any test claimed it (RED on base, `red-001.txt`); the code reviews' F1 crash (004) and the walkthrough's UX4-1 were caught before the gate, each with a node RED on the tree that had it (`red-004-review.txt`, `red-006.txt`).

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- ✓ Given/When/Then — §2.6's evaluability lines and the AT thresholds.
- ✓ Expected values explicit — exact strings, bytes, columns.
- ✓ Edge cases — empty, boundary, invalid per the §4 catalogs; error declared none with reasons.
- ✓ Regression checklist — the PRES-V3/V4 frame tests, TC-1904/TC-1808/TC-2002 law-driven, the board gantt's order (AT-2102).
- ✓ Exit criteria — §5.2.
- ✓ No PII or secrets — the synthetic portfolio board.
- ✓ Mode declared — validation.
- ✗ → ✓ Every result names its executor — the gate was pending at review time; run since by the orchestrator (`suite-p4.txt`).
- ✓ Layer B through the shipped surface — every story observed with boundary and negative.
- ✗ Bidirectional reachability — G-3, G-4, G-5, accepted above.
- ✓ No unfilled template.
