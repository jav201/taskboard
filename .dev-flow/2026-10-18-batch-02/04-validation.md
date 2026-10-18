# Validation — taskboard — Batch 2026-10-18-batch-02

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
- **Gate run:** `python -m pytest -q -p no:cacheprovider -rs --color=no` in a clean git worktree at commit `7e849dc` (`backlog-fixes` after increment 003 and the DDR follow-up; 0 changed files) · exit 0 · run and collected by the orchestrator · 2740 passed in 562.34s, 0 failed, 0 skipped — `test_win_clipboard_roundtrip` passed · `evidence/suite-p4.txt`
- **Layer 0:** 3 unit(s) met the criterion · 3 carry a named reddening mutation (`_clipboard_roundtrip` M4–M7; `PresentScreen._hint` N5–N9; `render_present`'s narrow branch N1–N4 — all KILLED)
- **Requirements:** 10/10 pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs reached/observed at the surface, two declared limits (G-1 the skip arm by fake only, G-2 the `pgdn` guard unobservable)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — the packets' B1 censuses re-ran green in `suite-p4.txt`; the PRES-V3 frames unchanged (`git diff --stat 9e82b10 7e849dc -- .dev-flow/2026-10-18-batch-01/evidence/frames` empty, `evidence/inspection-p4.txt`)
- **Test ledger:** ✓ reconciles (`2723 − 0 + 17 = 2740`)
- **Evidence checklist (qa-reviewer):** qa-reviewer — spawned with agents/qa-reviewer.md · 11 of 11 rows ✓ with evidence

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `tests/test_app.py::_clipboard_roundtrip` (the test-side verdict helper) | decision — refused / seeded / held / matched (cyclomatic 5) | `tests/test_app.py::test_TC_1902_the_roundtrip_verdict` ×6, `::test_TC_1902_a_held_sample_read_wrong_is_the_handle_bug` | pass (`suite-p4.txt`) |
| `app.PresentScreen._hint` | decision — a loop over four wordings, the narrow branch, the zero budget, the cut | `tests/test_present_narrow.py::test_TC_1904_the_hint_takes_the_first_wording_that_fits`, `::test_TC_1904_the_current_view_is_bold_and_bright`, `::test_TC_1904_an_overflowing_count_is_cut_visibly` | pass |
| `views.render_present`'s narrow branch | boundary — 35/36, the rungs' first widths, width 0 | `tests/test_present_narrow.py::test_TC_1903_every_width_renders_a_whole_frame` | pass |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `_clipboard_roundtrip` | M4 the skip keyed on the last attempt (PC-1) · M5 a refusal raises · M6 contention returns a reason · M7 a mismatch passes | yes — `1 failed` on each arm | `evidence/mutation-001.txt` |
| `_hint` | N5 no compact wording · N6 the narrow hint uncut · N7 the wide hint uncut (PC-2) · N8 no zero-budget guard · N9 the narrow hint keeps the names | yes | `evidence/mutation-002.txt` |
| narrow branch | N1 the floor at 35 · N2 at 37 · N3 a rung dropped · N4 the rung in `dim` | yes | `evidence/mutation-002.txt` |

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| narrowing `R` below 36 keeps the app and says how wide | `run_test`, `R`, `→`, `space`, `resize_terminal` 80…3 | row 0 = the rung at each width (35/32 `widen to 36+ columns · esc leave` … 3 `36+`), other rows blank; read from the compositor | pass |
| keys do nothing below 36 | `tab`, `→`, `space`, `a` at 30 | row 0 unchanged; the frame back at 118 equals the one kept | pass |
| `x` below 36 says why it writes nothing | `x` at 30 | the toast `Present / Widen the terminal to 36+ columns to export` painted (`prototypes/backlog_polish/out/narrow-current-narrow-30x12-x.{svg,png}`, toasts enabled); AT-1903 asserts the text and that nothing was written | pass |
| widening restores the presentation | resize back to 118×31 | the painted lines equal the kept frame | pass |
| the hint fits its row or ends in `…`, the current view bold | resize 80/60/50/40/36/35/30/20/14/8/3 | 80 short · 60/50 compact · 40/36 `esc` · 35–30 `esc leave · 1 hidden` · 20 `esc leave · 1 hid…` · 3 `…`; never wider than its row; `1 gantt` bold at ≥ 36 | pass |
| the narrow line in `mut` | the captures | grey in the 30×12 / 20×12 PNGs; the exact colour asserted on `Text` spans by TC-1903 | inspected, not exercised (exact colour) |

**Mechanism used:** a UI test driver (Textual `run_test`, headless; the compositor's painted strips read by the ux-reviewer's own script), plus the round's real-app SVG/PNG captures

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — by the ux-reviewer (its script outside the repo) and by AT-1903/AT-1904 in `suite-p4.txt` |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — ux-reviewer: "a split screen narrows my terminal mid-talk: do I know why the screen emptied and how to recover?" — the width and the way out are visible at every width ≥ 8; pass-with-notes (UX5-1 `esc leave` twice at 32–35; UX5-2 at 36–40 columns the gantt field holds only fragments — legal, a low floor) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the operator's look at the round is the human check |

- **Method:** headless app, keys and resizes through the pilot, painted cells read; the round's captures viewed; the walkthrough ran at `627b19d`, whose app code equals `7e849dc`'s (the follow-up commit touched only the round and records).
- **Participants or population:** none — no user evaluation.
- **Evidence of the evaluation:** `evidence/suite-p4.txt`; `prototypes/backlog_polish/out/narrow-current-*.png`; the ux-reviewer's report (folded here).
- **Limits:** no real terminal emulator resize (SIGWINCH, reflow); `q` below 36 not driven; projector legibility inferred from contrast, not observed.

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-1901 | test | the two standup nodes (rewritten in place), TC-1901, AT-1901 | `▌ username_su…` / `▎ Ana` | pass | `suite-p4.txt`; RED 2 failed on base (`red-001.txt`); M1–M3 KILLED |
| HLR-1902 | test | TC-1902 ×7, AT-1902, the real `test_win_clipboard_roundtrip` | the verdict arms; the skip quoting the refusal and `5 attempts` | pass — the real node `executed` (passed) | M4–M8 KILLED; G-1 |
| HLR-1903 | test | TC-1903, AT-1903 | the rung table; the kept frame; 0 saves; no `reports/` | pass | N1–N4, N10–N14 KILLED; G-2 |
| HLR-1904 | test | TC-1904 ×3, AT-1904, TC-1808, TC-1604 | the P-7 threshold table; ≤ `w − 2`; the 34-cell cut | pass | N5–N9 KILLED; G-3 |
| HLR-1905 | test | AT-1905 | page, manifest, captures, 8 corrupted-copy arms (LED .8) | pass | RED on base (`red-003.txt`); G-5 |
| LLR-1901.1 | test (unit) | TC-1901 | the name cell; 12/13 cells (LED .5) | pass | M1–M3 KILLED |
| LLR-1902.1 | test (unit) | TC-1902 | the eight arms | pass | M4–M7 KILLED |
| LLR-1903.1 | test (unit) | TC-1903 | widths 0–35 + 9 samples × 3 heights × views × cursor × scroll × 4 boards | pass | N1–N4 KILLED |
| LLR-1904.1 | test (unit) | TC-1904 | the threshold table, 0/3/10 hidden, 123456 | pass | N5–N9 KILLED |
| LLR-1905.1 | inspection | `git diff --stat 1ba8c3f -- taskboard/` empty (positive control: 2 files over increment 002's range); the write-path grep | empty; writes under the round, the scratch board removed | pass — by the orchestrator (`red-003.txt`), re-confirmed by the qa-reviewer | — |
| §5.2 HISTORICAL | inspection | `grep` over the two round folders | 6 files, each with its last commit | pass — orchestrator (`inspection-p4.txt`), qa-reviewer | — |
| §5.2 stale comments | inspection | `PRES-C\|PRES-R\b\|hybrid` in the `views.py` section header (positive control: 2 on base) and the TC-1001 banner | none | pass — orchestrator (`inspection-p4.txt`), qa-reviewer | G-4 |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-1901 | AT-1901 — `tests/test_team_views.py::test_AT_1901_the_standup_marks_the_operators_own_row` | key `8`, 120×40 | `#board` standup rows | repr: the own row · boundary: the 16-cell name cut · negative: RED on base | pass |
| US-1901 | AT-1902 — `tests/test_app.py::test_AT_1902_a_refused_setup_skips_with_its_reason` | the shipped test body, `_ps` faked | the pytest outcome: SKIP and its reason; the restore command | repr: refused ×5 · boundary: the restore · negative: RED on base (`SETUP failed`) | pass |
| US-1902 | AT-1903 — `tests/test_present_narrow.py::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits` | `R` `→` `space` `2`, resize 60…1, keys at 30 | `#present-frame`, the board file, `reports/`, the notice | repr: each rung · boundary: 35/36, 1 column · negative: RED on base | pass |
| US-1902 | AT-1904 — `::test_AT_1904_the_hint_shortens_and_cuts_visibly` | resize 50/40/30/15, `2` | `#present-hint` text and spans | repr: 3 hidden · boundary: 15 columns with `…` · negative: RED on base | pass |
| US-1903 | AT-1905 — `tests/test_backlog_polish_round.py::test_AT_1905_the_round_is_fit_for_a_verdict` | files on disk | the page, the manifest, 46 SVG/PNG pairs | repr: every item · boundary: 30×12, 50×20 · negative: RED on base and 8 corrupted copies | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | widths 118…1 (pilot); 0–35 + samples (renderer) | `PresentScreen.size` → `render_present(width)` | yes; width 0 at renderer level only | AT-1903, AT-1904, TC-1903 | ✓ |
| input | the narrow keys `tab` `→` `pgdn` `pgup` `space` `a` `x` | the guarded actions | yes (`1`, `shift+tab`, `h` reach the same guards) | AT-1903 | ✓ (G-2: `pgdn` unobservable) |
| input | hidden count 0/3/10, 123456 | `present_hidden` | 3 at the surface; the rest at unit level | AT-1904, TC-1904 | ✓ |
| input | a refused / contended `Set-Clipboard` | `_ps` → `_clipboard_roundtrip` | by the fake machine | AT-1902, TC-1902 | ✓ (G-1) |
| input | the roster names (16, 12, 13, 3 cells) | `render_standup` | the placeholder at the surface; 12/13 at unit level | AT-1901, TC-1901 | ✓ |
| output | standup rows | `render_standup` | yes | AT-1901 | ✓ |
| output | `#present-frame`, `#present-hint`, the notice, no file written | `render_present`, `_hint`, `action_export` | yes | AT-1903, AT-1904 | ✓ |
| output | the round page and captures | `capture.py`, `build_html.py` | yes, on disk | AT-1905 | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2723 (`suite-base.txt`: 2721 passed + the 2 standup failures, a git worktree of `9e82b10`) | 0 (rewrites in place: the two standup nodes, `test_win_clipboard_roundtrip`, the TC-1001 banner) | 17 (10 in increment 001, 6 in 002, 1 in 003) | 2740 | 2740 | 2740 / 2740 | yes |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-1 | HLR-1902 | the real roundtrip passed on this host, so its skip arm is proven only through AT-1902's fake machine | minor | accept — the contract's design |
| G-2 | LLR-1903.1 | N15 (the `pgdn` guard below 36) is an equivalent mutant: a narrow frame is the same at every page and a resize resets the page | minor | accept — a defensive guard nothing can observe, declared at the DDR |
| G-3 | HLR-1904 | the bold/bright span assertion of TC-1904 / AT-1904 is green on base and no mutant reddens it — a pin with no recorded RED | minor | accept; add a bold→dim mutant when the round's verdict is implemented |
| G-4 | §5.2 | the module docstring of `tests/test_present.py` keeps PRES-C/PRES-R/"hybrid" as history and the `*_presc_frame_*` names stay | minor | accept — provenance, outside §5.2's scope; the renames declined (`BACKLOG.md`) |
| G-5 | HLR-1905 | AT-1905's external-resource arm exercises only `href=https://`; the `url(` / `@import` branches have no copy of their own | minor | carry to the round's retirement (`BACKLOG.md`) |
| G-6 | evidence | `test_AT_1603…[118x30]` (help modal) failed once in `suite-002-run1.txt`; 5/5 alone, green in suite-002 run 2, suite-003 and the gate run — a timing flake by inference | minor | `BACKLOG.md` |
| G-7 | HLR-1905 | 12 stale captures of the round's first run stay on disk, git-excluded; the gate's clean worktree did not hold them | minor | the operator's removal (`BACKLOG.md`) |
| G-8 | HLR-1903 | ux-reviewer: `esc leave` shows twice at 32–35 columns (UX5-1); at 36–40 columns the gantt field holds only fragments (UX5-2) | minor | for the operator's review in the round (`BACKLOG.md`) |

### Escaped-bug regression (if a defect escaped the suite)

none — no defect escaped the suite in this batch: the standup and clipboard failures were known and are fixed with RED-on-base evidence (`red-001.txt`); the narrow-width assert was known (pre-existing) and is fixed with RED-on-base evidence (`red-002.txt`).

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- ✓ Given/When/Then — §2.6's evaluability lines and each AT's key → outcome.
- ✓ Expected values explicit — the literal rungs, hint strings, `username_su…`, the P-7 table.
- ✓ Edge cases — empty (no project, all hidden), boundary (35/36, widths 1–2, width 0), error (refused / contended), invalid N/A with reason.
- ✓ Regression checklist — TC-1001/1002, TC-1808, TC-1604, the PRES-V3 frames green in `suite-p4.txt`.
- ✓ Exit criteria — §5.2 of the requirements, reconciled above.
- ✓ No PII or secrets — synthetic boards; `username_subject`, `Ana`.
- ✓ Mode declared — validation.
- ✓ Every result names its executor — the orchestrator (gate run, RED, batteries, flake reruns, inspections); the qa-reviewer (the §5.2 greps, re-confirmed); the ux-reviewer (walkthrough).
- ✓ Layer B through the shipped surface — the TUI by keys and resizes, the pytest outcome, the files on disk; boundary and negative evidence each.
- ✓ Bidirectional reachability — the matrix above, G-1 and G-2 named.
- ✓ No unfilled template.
