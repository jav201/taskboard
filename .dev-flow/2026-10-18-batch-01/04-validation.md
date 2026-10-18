# Validation — taskboard — Batch 2026-10-18-batch-01

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
- **Gate run:** `python -m pytest -q -p no:cacheprovider --color=no` in a clean git worktree at commit `038b5f2` (`present-v3` after increment 002; 0 changed files) · exit 1 · run and collected by the orchestrator · 2 failed, 2721 passed in 513.07s — the 2 failures are the known standup pair (`tests/test_team_views.py`, failing on `origin/main` since the 2026-10-11 rewrite; `test_win_clipboard_roundtrip` passed in this run) · `evidence/suite-p4.txt`
- **Layer 0:** 3 unit(s) met the criterion · 3 carry a named reddening mutation (`present_note_lines` M1–M3, M20; `present_alloc` M5, M15; `present_paths` N6, N7 — all KILLED)
- **Requirements:** 10/10 pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs reached/observed at the surface, with one declared seam (G-1)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — `git grep -n "_present_note_lines\|_present_note_row\|PRESENT_SCROLL_STEP" -- taskboard tests` → none; the two prototypes that import the deleted helpers are frozen evidence (`docs/ARCHITECTURE.md` §3)
- **Test ledger:** ✓ reconciles (`2663 − 0 + 60 = 2723`)
- **Evidence checklist (qa-reviewer):** qa-reviewer — spawned as a generic agent with agents/qa-reviewer.md · 11 of 11 rows ✓ with evidence

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `views.present_note_lines` | decision — 5 branches (blank collapse, bullet, number, wide glyphs, continuation) | `tests/test_present_views.py::test_TC_1801_line_breaks_bullets_and_numbers_are_kept` | pass (`suite-p4.txt`) |
| `views.present_alloc` | decision — cyclomatic 9 | `tests/test_present_views.py::test_TC_1802_present_alloc_truth_table` ×9 | pass (`suite-p4.txt`) |
| `views.present_paths` | boundary — the export file name crosses into the file system | `tests/test_present_views_app.py::test_TC_1809_each_view_exports_to_its_own_file` | pass (`suite-p4.txt`) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `present_note_lines` | M1 line breaks dropped · M2 dash kept · M3 one digit · M20 wide glyphs by code points | yes — `1 failed` on each arm | `evidence/mutation-001.txt` |
| `present_alloc` | M5 the cursor's half dropped · M15 the below-floor row removed | yes | `evidence/mutation-001.txt` |
| `present_paths` | N6 one file for both views · N7 the suffix on gantt | yes | `evidence/mutation-002.txt` |

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| `R`, `2` → every shown open task's note text at once, the gantt rows above, `no notes` for the empty one | `run_test`, keys | `#present-frame` = PRES-V3 split frame, every note's first words after each `→` | pass |
| `→ →` in the gantt view → the plan's `1. Feature-flag` on its own row | keys | `#present-frame` = PRES-V3 gantt-notes frame | pass |
| `1`/`2`/`tab`/`shift+tab` → the view word follows; the board behind does not react | keys | the header; `view_mode` (a declared seam, G-1) | pass |
| `pgdn`/`pgup` → more of a cut note, every row reachable, no dead page | keys | `lines above`; the last page's last line; `pgup` after the end moves | pass |
| `space` in split → the task out of both views; `x` → the view on screen to its own file, no key in it | keys | frame; both SVGs by literal path | pass |
| the hint names the keys of the view on screen and fits its row | keys | `#present-hint` at 80, 96, 99, 100, 118 | pass |

**Mechanism used:** a UI test driver (Textual `run_test`, headless), plus real-app SVG captures (`evidence/captures/app-002-*`, PNGs at 118×31 through Edge)

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — AT-1801 ×2, AT-1802 ×2, AT-1803, TC-1808 ×5, TC-1810 in `suite-p4.txt`; 14 SVG captures + 7 PNG |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — `ux-reviewer` over the captures, compared with the prototype's `r2-118-D2-stacked*.png`, `r2-80-D2-stacked*.png`, `r2-118-A-gantt.png`: pass-with-notes (UX4-1 hint fit ✓; UX4-2 the dim view word and cut marks ~3:1 contrast, accepted — quiet by design, backed by the bold hint name and the `▌`/`▎` shapes; UX4-3, UX4-4 → `BACKLOG.md`; UX4-5 fidelity to D2 ✓) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the operator's review of the captures is the human check |

- **Method:** headless app, keys pressed through the pilot, painted rows read; captures of the same states at 118×31 and 80×25; the orchestrator compared the 118 PNGs with the prototype's (same layout, two columns, the cursor block in accent, `no notes` on the SEO heading; deltas only the declared ones).
- **Participants or population:** none — no user evaluation.
- **Evidence of the evaluation:** `evidence/suite-p4.txt`, `evidence/captures/app-002-*.svg`, `app-002-118x31-*.png`.
- **Limits:** establishes the painted text and the layout at two sizes; not contrast on a compressed screen share (UX4-2) nor whether a room reads the split view comfortably — the operator's verdict on the captures.

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-1801 | test | TC-1801..TC-1806, AT-1801 (within the gate run) | AT-1801 frames at 118×31 / 80×25; every note's words after each press; 0 saves | pass | `suite-p4.txt`; RED 51 / 16 on base (`red-001.txt`, `red-002.txt`); M4 M6 M7 M16 M17 M18 KILLED |
| HLR-1802 | test | TC-1807, TC-1001, TC-1002, AT-1802 | the PRES-V3 gantt and gantt-notes frames; `1. Feature-flag` on its own row | pass | `suite-p4.txt`; M12 M13 KILLED |
| HLR-1803 | test | TC-1808..TC-1810, TC-1604 hint arm, AT-1803 | AT-1803's arms | pass | `suite-p4.txt`; N1..N12 KILLED |
| LLR-1801.1 | test (unit) | TC-1801 | the 10 exact rows; the wide-glyph arm | pass | M1 M2 M3 M20 KILLED |
| LLR-1801.2 | test (unit) | TC-1802..TC-1805 | 9 alloc rows; 9 sizes × every cursor; below-floor 80×18 / 118×15 / 80×11; all hidden; S1 sites | pass | M4..M8 M15..M18 KILLED |
| LLR-1801.3 | test (unit) | TC-1806 | paging covers every row; no backward jump; every frame exact | pass | M9 M10 M11 M14 M19 KILLED |
| LLR-1802.1 | test (unit) | TC-1807, TC-1001, TC-1002 | the frames; 3 rows; the view word | pass | M12 M13 KILLED |
| LLR-1803.1 | test (integration) | TC-1810 | the bindings; page stepping and stop; resets incl. resize | pass | N1 N2 N3 N8 N12 KILLED |
| LLR-1803.2 | test (integration) | TC-1808, TC-1604 hint arm | the hints at 5 widths × 3 states, each within `w − 2` | pass | N4 N5 N11 KILLED |
| LLR-1803.3 | test (unit) | TC-1809, AT-1803 export arm | the `-split` name; the shipped gantt name | pass | N6 N7 N9 KILLED |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-1801 | AT-1801 — `tests/test_present_views_app.py::test_AT_1801_2_shows_every_task_text_at_once` ×2 | keys `R`, `2`, `→` ×4 | `#present-frame` | repr: the split frame at 118×31 · boundary: 80×25 (one column, cut notes), the task without notes · negative: RED on base (`red-002.txt`) | pass |
| US-1802 | AT-1802 — `::test_AT_1802_the_gantt_note_keeps_its_line_breaks` ×2 | keys `R`, `→ →` | `#present-frame` | repr: the numbered plan at 118 · boundary: 80 · negative: RED on base, the flattened `Sep 22. 1.` | pass |
| US-1803 | AT-1803 — `::test_AT_1803_the_view_keys_and_what_the_views_share` | keys `R` `1` `2` `tab` `shift+tab` `pgdn` `pgup` `→` `space` `a` `x` `esc` | `#present-frame`, the board file (2 saves), `reports/present-website-redesign-2026-09-30.svg` and `…-split.svg` | repr: each key · boundary: `tab` wrapping, `pgdn` past the end, 80×25 · negative: RED on base | pass |
| (repointed) | AT-1001 — `tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle` | key `R`, `l`, `x`, `esc` | `#present-frame` = PRES-V3-gantt-118x30 | as shipped | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | view keys `1` `2` `tab` `shift+tab` | `PresentScreen.action_view` / `action_cycle` | yes | AT-1803, TC-1810 | ✓ |
| input | `pgdn` `pgup` | `action_scroll` → `render_present(scroll=)` | yes | AT-1803, TC-1810 | ✓ |
| input | `←` `→` `↑` `↓` `space` `a` `x` `esc` `R` | the shipped actions | yes (`↑`/`↓` through TC-1604) | AT-1801, AT-1803, TC-1604 | ✓ |
| input | sizes 118 / 80 (pilot) · 9 more (renderer) | `width`, `height` | 118/80 yes · others at renderer level | AT-1801..1803 · TC-1804, TC-1806 | ✓ |
| input | the board's notes | `Task.notes` from the saved file | yes | AT-1801, AT-1802 | ✓ |
| output | `#present-frame`, gantt view | `render_present(view="gantt")` | yes | AT-1802, AT-1001 | ✓ |
| output | `#present-frame`, split view | `render_present(view="split")` | yes | AT-1801, AT-1803 | ✓ |
| output | `#present-hint` | `PresentScreen._hint` | yes | TC-1808, TC-1604 | ✓ |
| output | the two export files | `present_paths(view)`, `save_present_svg` | yes, by literal path | AT-1803 | ✓ |
| output | "the board behind does not react" | `TaskboardApp.view_mode` | read as a seam, not painted | AT-1803 | ✓ (G-1) |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2663 (`suite-base.txt`: 2649 passed + 14 failed in the git-less export) | 0 (rewrites in place: `test_present.py` 5→5, `test_present_hide.py` 9→9, `test_markup_census.py` 6→6) | 60 (48 in `tests/test_present_views.py`, 12 in `tests/test_present_views_app.py`) | 2723 | 2723 | 2721 / 2721 (+ the 2 known standup failures) | yes |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-1 | HLR-1803 | "the board behind does not react" reads `app.view_mode`, a declared seam, not the painted board | minor | accept (declared at P2, QA-8) |
| G-2 | LLR-1803.2 | the 80-column hint with a two-digit count is analysis over a literal; the fixture cannot hide 12 tasks | minor | accept — real fit rendered at 80, 96, 99, 100, 118 |
| G-3 | §5.2 | PNGs at 118 only; 80×25 is SVG-only | minor | accept — §5.2 asks no more |
| G-4 | HLR-1801, HLR-1802 | UX4-3 the 80-column short hint drops key words; UX4-4 the gantt note keeps 3 rows while free rows stay empty | minor | carried to `BACKLOG.md` at the close; UX4-2 accepted |
| G-5 | evidence | the header of `evidence/suite-base.txt` says the 12 git-dependent base failures are all in `tests/test_scratch_cannot_be_committed.py`; 10 are, the other two are `tests/test_no_live_board.py::test_the_fixture_is_in_git_not_just_on_this_disk` and `tests/test_precommit_gate.py::test_the_hook_wired_in_this_repo_points_at_the_script` | minor | corrected here; the file is not rewritten (its digest is in packet 001) |

### Escaped-bug regression (if a defect escaped the suite)

none — no defect escaped the suite in this batch.

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- ✓ Given/When/Then — the stories §2.6 and each AT's key → painted outcome.
- ✓ Expected values explicit — the exact PRES-V3 frames, the hint strings, the literal export paths.
- ✓ Edge cases — empty (no notes, all hidden), boundary (99/100, below the floor, the last page, wide glyphs), invalid (S1 markup); error N/A with reason.
- ✓ Regression checklist — TC-1001/1002/AT-1001, TC-1604's hint arm, TC-402's key repointed law-driven.
- ✓ Exit criteria — §5.2 of the requirements.
- ✓ No PII or secrets — synthetic boards; `username_subject` the placeholder.
- ✓ Mode declared — validation.
- ✓ Every result names its executor — the orchestrator (gate run, RED, batteries, captures); the ux-reviewer (walkthrough).
- ✓ Layer B through the shipped TUI by keys, with boundary (two sizes) and negative (RED on base) evidence.
- ✓ Bidirectional reachability — the matrix above, G-1 named.
- ✓ No unfilled template.
