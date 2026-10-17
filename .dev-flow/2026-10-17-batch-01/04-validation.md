# Validation — taskboard — Batch 2026-10-17-batch-01

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
- **Gate run:** `python -m pytest -q -p no:cacheprovider --color=no -rf` from the project root · exit 1 · on commit `63c9669023516c05d1711de2185533897d179f78` (`taskboard/` and `tests/` clean against it) · run and collected by the orchestrator · 2 failed, 2661 passed in 513.70s — the 2 failures are the known standup pair (`tests/test_team_views.py`, failing on `origin/main` since the 2026-10-11 rewrite, in the backlog) · `evidence/suite-p4.txt`
- **Layer 0:** 1 unit met the criterion (`_gantt_tick_label`, cyclomatic 4) · 1 carries named reddening mutations (M1, M2, M3, M5 — all KILLED, `mutation-001.txt`)
- **Requirements:** 2/2 pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs reached/observed at the surface, with two minor notes (G-001: the `x` export observed at its producer; G-002: 60/48 columns and the hide-all route at renderer level and in captures)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — `git grep _gantt_scale_label` → only the absence assert `tests/test_tick_label.py:206`; the other hits are docstrings, the false-match guard and the agenda view's own unrelated scale (`views.py:1931`)
- **Test ledger:** ✓ reconciles (`2634 − 1 + 30 = 2663`; 2661 passed + 2 known failures)
- **Evidence checklist (qa-reviewer):** qa-reviewer — spawned as a generic agent with agents/qa-reviewer.md · 10 of 11 rows ✓ with evidence (✗ bidirectional reachability for the `x` key itself — G-001, minor, inspected)

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `views._gantt_tick_label` | decision — cyclomatic 4 (two `if`s and an `or`) | `tests/test_tick_label.py::test_TC_1701_the_label_function_branches` | pass (`suite-p4.txt`) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `_gantt_tick_label` | M1 no-selection returns `Mondays · 1 cell = 1 day` · M2 echo branch `dim` · M3 dateless branch `over` · M5 `if selected is not None` → `if False` | yes — `1 failed` on each arm, 19/19 arms KILLED in the battery | `evidence/mutation-001.txt` |

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| `3` with a task selected → the tick row's label reads `selected task ▸` | `run_test`, key `3` | `#board` row 2 | pass |
| `L` → the candidate is named the same way | key `L` | `#glink-frame` row 2 | pass |
| `/` `Daily` `enter` → the app re-selects the one drawn task, the label names it | keys `/`, text, `enter` | `#board` tick row below the search bar | pass |
| `/` `zzqx` `enter` → nothing drawn, the label blank, `today` still on the month row | keys | `#board` | pass |
| a board file with no task, `3` → blank label, ruler painted | the board file, key `3` | `#board` rows 1–2 | pass |
| `R` → the presentation's tick row reads `selected task ▸` | key `R` | `#present-frame` row 2 | pass |
| no painted row of any arm holds the scale text | all of the above | every row | pass |

**Mechanism used:** a UI test driver (Textual `run_test`, headless), plus real-app SVG captures (`evidence/captures/app-001-*`)

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — AT-1701 (4 nodes) in `suite-p4.txt`; 8 SVG captures + 1 PNG |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | not performed — at P4; the ux-reviewer reviewed the contract at P2 (two iterations), not the build |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the operator's review of the captures is the human check, pending |

- **Method:** headless app, keys pressed through the pilot, painted rows read; captures of the same states at 118×31 and 80×25.
- **Participants or population:** none — no user evaluation.
- **Evidence of the evaluation:** `evidence/suite-p4.txt`, `evidence/captures/app-001-*.svg`, `app-001-118x31-gantt-selected.png`.
- **Limits:** establishes the painted text and tone at two sizes; not whether a reader finds `selected task ▸` / `selected: no dates` clear (the operator's open approval of the latter).

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-1701 | test | `python -m pytest -q -p no:cacheprovider tests/test_tick_label.py tests/test_present_room.py tests/test_present_rulers.py tests/test_gantt_board.py tests/test_present.py` (within the gate run) | every arm passes; AT-1701 at 118×31 and 80×25; 0 scale-text matches; PRES-R2 frames equal | pass | `suite-p4.txt` (0 failures in these files); RED on base 27 failed (`red-001.txt`) |
| LLR-1701.1 | test (unit) | `python -m pytest -q -p no:cacheprovider tests/test_tick_label.py -k TC_1701` (within the gate run) | (a) cases, (b) sweep, (c) the function gone | pass — 26 nodes | `suite-p4.txt`; `mutation-001.txt` M1–M7 KILLED |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-1701 | AT-1701 — `tests/test_tick_label.py::test_AT_1701_the_tick_row_names_the_selection` ×2, `::test_AT_1701_a_board_with_no_task_has_a_blank_label` ×2 | keys `3`, `L`, `/`, `R`; a board file | `#board` tick row, `#glink-frame`, `#present-frame` | repr: `selected task ▸` in gantt, link mode, search-kept task, presentation · boundary: search drawing nothing, board with no task, 118×31 and 80×25 · negative: 0 scale-text matches in every painted row; RED on base | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | selection: selected / none / candidate | `selected_id`, `cand`, `cursor` | yes | AT-1701 | ✓ |
| input | selection: dateless / too-long echo / before the window | `gantt_echo`, `meta["echo_label"]` | renderer level; dateless also in a real-app capture | TC-1701 | ✓ (G-002) |
| input | search | `search_query` → `filtered_board` | yes (`/`) | AT-1701, TC-1701 | ✓ |
| input | link mode | `GanttLinkMode` → `gantt_link_frame` | yes (`L`) | AT-1701, TC-1701 | ✓ |
| input | board file | `Board` load | yes (a saved file with no task) | AT-1701 | ✓ |
| input | size 118 / 80 · 60 / 48 | `gantt_columns`, `_present_cols` | 118/80 yes · 60/48 renderer level | AT-1701 · TC-1701 | ✓ (G-002) |
| output | gantt tick row | `_gantt_frame` → `#board` | yes | AT-1701 | ✓ |
| output | link-mode tick row | `gantt_link_frame` → `#glink-frame` | yes | AT-1701 | ✓ |
| output | presentation tick row | `_present_ruler` → `#present-frame` | yes | AT-1701 | ✓ |
| output | the `x` SVG | `save_present_svg` | at the producer (the handler passes `render_present` straight to it, `app.py:302-308`, inspected) | TC-1701 (b) | ✓ (G-001) |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2634 | 1 (TC-110) | 30 (`tests/test_tick_label.py`) | 2663 | 2663 | 2661 / 2661 (+ the 2 known standup failures) | yes |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | HLR-1701 | no AT presses `x`; the export is read at its producer, which the handler calls unchanged (inspected) | minor | accept, noted |
| G-002 | LLR-1701.1 | 60/48 columns, the bold tone, and the hide-all route are asserted at renderer level and in real-app captures, not in an AT | minor | accept |
| G-003 | HLR-1701 (scope) | the README hero image `docs/taskboard-gantt.svg` still shows `Mondays · 1 d/cell` | minor | Out of scope (LED .2); carried to `BACKLOG.md` at the close |

### Escaped-bug regression (if a defect escaped the suite)

none — no defect escaped the suite in this batch.

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- ✓ Given/When/Then — HLR-1701's outcome and AT-1701's arms as key → painted row.
- ✓ Expected values explicit — `selected task ▸`, `Jul 1 → Dec 31 ▸`, `selected: no d…`, blank.
- ✓ Edge cases — empty (no task, no candidate, all hidden), boundary (48/80, off-window, too-long); invalid/error N/A with reasons.
- ✓ Regression checklist — B1 census; 5 pinned tests updated law-driven; PRES-R2 frames unchanged.
- ✓ Exit criteria — §5.2 of the requirements.
- ✓ No PII or secrets — `kg_board` and `present_board` fixtures only.
- ✓ Mode declared — validation.
- ✓ Every result names its executor — the orchestrator for the gate run, RED, mutation and captures; the qa-reviewer's own spot-check: `tests/test_tick_label.py` on `63c9669`, 30 passed.
- ✓ Layer B through the shipped TUI by keys, with boundary and negative evidence.
- ✗ Bidirectional reachability for the `x` key itself — G-001 (minor), the handler pass-through inspected.
- ✓ No unfilled template.
