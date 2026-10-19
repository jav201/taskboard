# Validation — taskboard — Batch 2026-10-18-batch-03

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
- **Gate run:** `python -m pytest -q -p no:cacheprovider -rs --color=no` in a clean git worktree at commit `984ba8e` (`present-polish` after increment 003; 0 changed files) · exit 0 · run and collected by the orchestrator · 2759 passed in 657.42s, 0 failed, 0 skipped — `test_win_clipboard_roundtrip` passed · `evidence/suite-p4.txt`
- **Layer 0:** 1 unit(s) met the criterion · 1 carry a named reddening mutation (`PresentScreen._hint` N1–N4, all KILLED)
- **Requirements:** 6/6 pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ⚠ all named inputs and outputs reached at the surface but one: the `x` export's contents, reached by inspection only (G-2)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — the packets' B1 censuses re-ran green in `suite-p4.txt`; the PRES-V3 files and the round's committed files unchanged (`evidence/inspection-p4.txt`, with its positive control)
- **Test ledger:** ✓ reconciles (`2740 − 0 + 19 = 2759`)
- **Evidence checklist (qa-reviewer):** qa-reviewer — spawned with agents/qa-reviewer.md · 10 of 11 rows ✓ with evidence, 1 ✗ (bidirectional reachability: G-2, accepted below)

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `app.PresentScreen._hint` | decision — a loop over five wordings, the narrow branch, the zero budget, the cut | `tests/test_present_polish.py::test_TC_2002_the_middle_wording_sits_between_the_long_and_the_short` ×8, `tests/test_present_narrow.py::test_TC_1904_the_hint_takes_the_first_wording_that_fits` | pass (`suite-p4.txt`) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `_hint` | N1 no middle wording · N2 the middle tried first · N3 its gap one space · N4 its keys drop `show all` | yes — `1 failed` on each of the 8 arms | `evidence/mutation-002.txt` |

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| after `R` / `2` the view word and the cut and edge marks are readable, quieter than titles and dates | `run_test`, `R`, `→ →`, `2`, `pgdn`; per-segment colour read from the rendered strips | `gantt`/`split`, `… +N lines`, ` … +4 lines`, `↑ N lines above`, `↓ N more lines` `#7a828c` (4.87:1, not bold); titles `#e6edf7` bold (16.06:1), dates `#8b98a5` (6.43:1); lead, separators, `no notes` `#5b6675` | pass |
| at 80×25 the hint names `next` and `show all` | the same driver, `#present-hint` | gantt `1 gantt  2 split  ⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc`; split with `pgdn · ` first; 118 the long wording | pass |
| the gantt note fills the free rows and says where it is cut | `→ →` at 80×25 and 118×31 | 80: rows 14–22, ends `· … +5 lines`, then the last brief; 118: the 11 rows whole, no cut | pass |
| the split view, `pgdn` and `space` do not regress | `2`, `pgdn`, `space`, `1` | `pgdn` pages the cursor note (edge marks shown); `space` → `4 open`, `· 1 hidden` survives the view switch | pass |
| below 36 the narrow frame still shows | `resize_terminal` 50 / 36 / 35 / 30 | 36: the header whole in bold `bright` (the declared overflow clause); 35/30: `widen to 36+ columns`, hint `esc leave · 1 hidden` | pass |
| the real-app PNGs match the approved A round | the PNGs side by side | `captures/gantt-long-118x31` = `notecap-A-gantt-long-118x31`; `captures/split-long-118x31` = `contrast-A-split-long-118x31` — no visible difference | pass |

**Mechanism used:** a UI test driver (Textual `run_test`, headless; the rendered strips read by the ux-reviewer's own script outside the repo, deleted after), plus the real-app SVG/PNG captures of `evidence/captures/` against the round's

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — by the ux-reviewer, and by AT-2001..2003 in `suite-p4.txt` |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — ux-reviewer, against the projector-presenter context (`01-requirements.md` §2.3): pass-with-notes (UX4-1 `esc` without `leave` in the middle wording, the approved design; UX4-2 the quiet tier left `dim` at 3.25:1, intended; UX4-3 `␣` drawn like `_` in the PNGs, pre-existing; UX4-4 the view word bold at 36, the declared clause) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the operator's verdict on the round is the human check |

- **Method:** headless app, keys and resizes through the pilot, painted cells and their colours read; the 118 PNGs viewed against the round's (the visual claim of AT-2001 rests on that comparison, ux-reviewer UX-3 of P2).
- **Participants or population:** none — no user evaluation.
- **Evidence of the evaluation:** `evidence/suite-p4.txt`; `evidence/captures/`; `evidence/compare-003.txt`; the ux-reviewer's report (folded here).
- **Limits:** no PNG at 80 columns (the SVGs and the driver's strips stand for it); no real projector — contrast computed, not observed; the start-up milestone offer bypassed as the suite does.

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-2001 | test | AT-2001, TC-2001 | the marks `#7a828c`, not `#5b6675`; the lead `#5b6675`; ≥ 4.5:1 and below `mut` | pass | `suite-p4.txt`; RED `red-001.txt`; M1, M3–M5 KILLED |
| HLR-2002 | test | AT-2002; the narrow, views_app and hide files | the literal hints at 80 and 118 | pass | RED `red-002.txt`; N1, N3, N4 KILLED |
| HLR-2003 | test | AT-2003; `tests/test_present_views.py` | the PRES-V4 frames; `… +5 lines`; no blank row | pass | RED `red-003.txt`; K1, K3 KILLED |
| LLR-2001.1 | test (unit) | TC-2001 ×4 | the sweep, every mark kind seen; `no project to present` `dim` | pass | M1–M6 KILLED; G-1 |
| LLR-2002.1 | test (unit) | TC-2002 ×8, TC-1904 | P-3's widths; ≤ `w − 2` | pass | N1–N4 KILLED |
| LLR-2003.1 | test (unit) | TC-2003 ×4, TC-1807, AT-1802 | `min(n, max(3, height − L))`; overflow, cut, exact, one-short seen | pass | K1–K4 KILLED (11/11) |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-2001 | AT-2001 — `tests/test_present_polish.py::test_AT_2001_the_quiet_marks_read_in_the_running_app` | `R`, `→ →`, `2`, `pgdn` at 80×25 | `#present-frame` spans | repr: the cut note · boundary: the edge marks after `pgdn` · negative: RED on base | pass |
| US-2002 | AT-2002 — `::test_AT_2002_the_80_column_hint_names_next_and_show_all` | `R`, `2`, `space` at 80×25; `R` at 118×31 | `#present-hint` text and spans | repr: both views · boundary: 78 cells exactly; one hidden → short · negative: RED on base | pass |
| US-2003 | AT-2003 — `::test_AT_2003_the_gantt_note_runs_to_the_bottom_of_the_frame` | `R`, `→ →` at 80×25 and 118×31 | `#present-frame` rows against PRES-V4 | repr: the long note · boundary: whole at 118, cut at 80 · negative: RED on base | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | widths 80, 118 (pilot); 36–140 (renderer, method) | `PresentScreen.size` → `render_present`, `_hint` | yes at 80 and 118; the rest at unit level | AT-2001..2003, TC-2001..2003, TC-1904 | ✓ |
| input | heights 25, 31 (pilot); 5–60 and the boundary heights (renderer) | `render_present(height)` | yes at 25 and 31 | AT-2003, TC-2003 | ✓ |
| input | views gantt / split; `pgdn` | `view`, `scroll` | yes | AT-2001, AT-2002 | ✓ |
| input | hidden 0 / 1 (pilot); 3 / 10 (method) | `present_hidden` | yes at 0 and 1 | AT-2002, TC-2002, TC-1904 | ✓ |
| output | `#present-frame` (tones, the filled note) | `render_present` | yes | AT-2001, AT-2003 | ✓ |
| output | `#present-hint` | `_hint` | yes | AT-2002 | ✓ |
| output | the `x` export (SVG, PNG) | `action_export` → `_frame_text()` | by inspection: `app.py:404-407` writes the same `Text` the frame shows; the captures are the app's `export_screenshot` | — | ⚠ G-2 |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2740 (`suite-base.txt`, 2740 passed on `620f58c`) | 0 (rewrites in place: TC-1807, TC-1808, TC-1904, TC-1604, AT-1802, AT-1603 — parametrize values and assertions, no row added or removed) | 19 (5 in increment 001, 9 in 002, 5 in 003) | 2759 | 2759 | 2759 / 2759 | yes |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-1 | LLR-2001.1 | the header's ` · ` separators are said to stay `dim`, but TC-2001's stay-dim pattern matches only the note lead; no arm repaints a separator (lines this batch did not change) | minor | `BACKLOG.md`: a separator assertion and arm |
| G-2 | HLR-2001, HLR-2003 | no node asserts the new tones or the fill inside the exported SVG/PNG; inspection: `action_export` writes `_frame_text()`, the frame on screen | minor | accept with the inspection; `BACKLOG.md` |
| G-3 | HLR-2001 | the gantt cut row's `· ` lead stays `dim` where the round's capture painted it `reached` (a fork span-merge artefact) — declared deviation | minor | the operator's call (`BACKLOG.md`) |
| G-4 | evidence | packet 003's correction population was enumerated after `suite-003-run1.txt` failed on AT-1802 (declared ⚠ in the packet) | minor | none — corrected before the gate run |

### Escaped-bug regression (if a defect escaped the suite)

none — no defect escaped the suite in this batch: the three changes are new behaviour with RED-on-base evidence (`red-001.txt`..`red-003.txt`); the help-modal flake was pre-existing (`flake-001.txt`: 2 of 8 on base) and was hardened.

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- ✓ Given/When/Then — each story's evaluability line in `01-requirements.md` §2.6.
- ✓ Expected values explicit — literal strings, hex colours, the PRES-V4 frame files.
- ✓ Edge cases — the one-row cut, room equal to the note and one short, overflow, no cursor / no notes; invalid and error declared none with reasons.
- ✓ Regression checklist — TC-1807, TC-1808, TC-1904, TC-1604, AT-1802 and the PRES-V3 nodes in the 2759.
- ✓ Exit criteria — §5.2 of the requirements, met.
- ✓ No PII or secrets — synthetic fixtures; `username_subject`.
- ✓ Mode declared — validation.
- ✓ Every result names its executor — the orchestrator (gate run, RED, batteries, comparisons, inspections); the qa-reviewer (read-only, `--collect-only`); the ux-reviewer (walkthrough).
- ✓ Layer B through the shipped surface — AT-2001..2003 drive the real app and read `#present-frame` / `#present-hint`, boundary and RED on base each.
- ✗ Bidirectional reachability — the `x` export's contents reached by inspection only (G-2, accepted).
- ✓ No unfilled template.
