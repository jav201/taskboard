# Validation — taskboard — Batch 2026-10-24-batch-01

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

- **Result:** PASS-WITH-NOTES
- **Gate run:** `env -u NO_COLOR python -m pytest <chunk files>` — the collected suite split into three sequential chunks (118 files: 40/39/39, lists at `evidence/suite-p4-chunkNN-files.txt`), each chunk's transcript at `evidence/suite-p4-chunkNN.txt` — exit 0 on all three chunks · ran on commit `512813d` (no code or test diff vs `1cae9c6`, the implemented HEAD) · run and collected by the orchestrator (`C-25`)
- **Layer 0:** 81 mutation arms met the criterion (31 + 14 + 17 + 19 across `evidence/mutation-001..004`) · 81 carry a named reddening mutation, 81 KILLED, 0 BAD arms (each restored by hash, `after:` lines in the transcripts)
- **Requirements:** 8/8 HLRs pass (HLR-2601..HLR-2608) · 17/17 LLRs pass (LLR-2601.1-.3, 2602.1-.2, 2603.1-.2, 2604.1-.2, 2605.1, 2606.1-.3, 2607.1-.2, 2608.1-.2) · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (painted frame via the styled-segment export at 118×30 and 80×24 + on-disk read-backs) with boundary and negative arms
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface (matrix below, no gaps)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative (each increment packet's census; the DDR re-ran the cross-increment census)
- **Test ledger:** ✓ reconciles — 3152 + 84 = 3236 collected, exactly the collected count; see the signed-balance table
- **Evidence checklist (qa-reviewer):** qa-reviewer · 10 of 10 rows ✓ with evidence (its P4 evaluation pass over this artifact and the transcripts, 2026-10-24)

**The one NOTE (the only deviation from the commission's "0 failed and 0 skipped"):** chunk 00's run shows **1 skipped** — `tests/test_app.py:1270 test_win_clipboard_roundtrip` (TC-1902, a pre-existing clipboard test from an earlier batch, untouched by this batch's diff). Its designed skip fired: "Set-Clipboard refused the sample on all 5 attempts (the machine, not the code under test)". Verified environmental at gate time, from two contexts (the orchestrator's shell AND the interactive console session via a scheduled task run as the logged-on user): `Set-Clipboard`, `Get-Clipboard`, WinForms `Clipboard.SetText` and `clip.exe` all fail machine-wide; `cbdhsvc` cannot be opened for start without elevation; `cbdhsvc_1d3b90` runs yet `OpenClipboard` still refuses. The skip is the test's own declared machine-refusal arm, not a code regression; every other collected test passed (3235 passed + 1 environmental skip = 3236). The batch's own 84 tests: all passed, 0 skipped. Recorded as a gap (G-001, minor, environmental) for the operator's decision per the station file ("Otherwise, user decides").

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| the store and the field (001) | every new assertion is RED on the base or by a declared mutation | `tests/test_marks_directory.py` (31) | pass (`suite-001.txt`, `suite-001b.txt`) |
| the seat (002) | every new assertion is RED on the base or by a declared mutation | `tests/test_milestone_marks.py` (15) | pass (`suite-002.txt`, `suite-002b.txt`) |
| the editor Select and the `#` manager (003) | every new assertion is RED on the base or by a declared mutation | `tests/test_marks_manager.py` (16), `test_modal_keys.py` rows | pass (`suite-003.txt`, `suite-003b.txt`) |
| the legend, hide, search, help, README (004) | every new assertion is RED on the base or by a declared mutation | `test_legend.py`, `test_readme.py`, `test_modal_keys.py` rows | pass (`suite-004.txt`, `suite-004b.txt`) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| 001 | 31 arms (memory-only `_commit`, wrong filename, the empty-directory arms, the keep-aside arms…) | 31/31 KILLED | `evidence/mutation-001.txt` |
| 002 | 14 arms (the seat swapped for plain diamonds, `_hide` bypassed…) | 14/14 KILLED | `evidence/mutation-002.txt` |
| 003 | 17 arms (the Select never composed, the form's write stubbed…) | 17/17 KILLED | `evidence/mutation-003.txt` |
| 004 | 19 arms (the strip dropped, the filter dropped…) | 19/19 KILLED | `evidence/mutation-004.txt` |

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| the gantt/present strips, the manager, the form, the editor Select, the hidden redraw, the `/#cls` bar read as designed at 118×30 and 80×24 | the app's own key path (`App._press_keys`) on synthetic boards in a temporary home, `PrintWindow` full-colour grabs | yes — 14 PNGs, every grab re-verified from disk (not black, 8–52 colours); the no-`m01-`-window assertion passed | ✓ (`evidence/captures/README.md`, `png/`) |

**Mechanism used:** a UI test driver (the real app subclass `evidence/captures/shoot_real.py`, windows titled `m01-<scene>-<size>-<n>`, each closed by title)

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — 14 shots, all 7 scenes × 2 sizes |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — the ux-reviewer's DDR pass read all 14 PNGs against the shipped contract |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — one-person team, no user of this surface exists outside it (declared at the DDR) |

- **Method:** scripted scene playback through the app's own input path; synthetic fixture boards (`tests/milestone_marks_fixture.py`, TODAY pinned to 2026-10-20)
- **Participants or population:** n/a — no human participants (expert inspection by the spawned ux-reviewer role only; no PII anywhere, synthetic data)
- **Evidence of the evaluation:** `evidence/captures/README.md` (claims table + verification results), `evidence/captures/png/capture-log.txt`, `assert-no-m01.ps1` output "no m01-* window left open"
- **Limits:** expert inspection is not user evaluation; the MM-D5 ▲ echo surface is documented but unpainted (no late Delivery milestone in the fixture scenes)

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-2601 / LLR-2601.1-.3 | test | `pytest tests/test_marks_directory.py` (31) | exit 0 | pass | `suite-p4-chunk01.txt` (1071 passed) |
| HLR-2602 / LLR-2602.1-.2 | test | `pytest tests/test_milestone_marks.py` (15) | exit 0 | pass | `suite-p4-chunk01.txt` |
| HLR-2603 / LLR-2603.1-.2 | test | the two-window and keep-aside arms of `test_marks_directory.py` | exit 0 | pass | `suite-p4-chunk01.txt`; mutation-001 arms |
| HLR-2604 / LLR-2604.1-.2 | test | `test_milestone_marks.py` + the site-enumeration guard (test_milestone_marks.py:263-297) | exit 0 | pass | `suite-p4-chunk01.txt`; mutation-002 |
| HLR-2605 / LLR-2605.1 | test | `test_modal_keys.py` rows + the editor suites | exit 0 | pass | `suite-p4-chunk01.txt` |
| HLR-2606 / LLR-2606.1-.3 | test | `tests/test_marks_manager.py` (16) | exit 0 | pass | `suite-p4-chunk01.txt`; mutation-003 |
| HLR-2607 / LLR-2607.1-.2 | test | `test_legend.py` painted-frame arms at both sizes + `test_readme.py` | exit 0 | pass | `suite-p4-chunk01.txt` (test_legend) + `suite-p4-chunk02.txt` (test_readme); mutation-004 |
| HLR-2608 / LLR-2608.1-.2 | test | `test_legend.py` hide arms, `test_milestone_marks.py` `/#cls` arms | exit 0 | pass | `suite-p4-chunk01.txt` |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| the directory lives beside people.json and survives the app | AT-2601 | the app end-to-end (manager → form → editor → disk read-back → restart → gantt glyph) | `marks.json` on disk in a temporary home | repr: the full journey · boundary: both sizes painted · negative: the refused-write keeps the form | pass (`test_marks_manager.py:462`, orchestrator-run) |
| two windows adding at once both survive | AT-2602 | two `Directory` seats on one file | the file's bytes after interleaved writes | repr + negative: a failed write changes nothing in memory | pass (`test_marks_directory.py:350`) |
| every milestone mark renders through the one seat | AT-2603 | the painted gantt/present frames | styled-segment export at 118×30/80×24 | repr + boundary: unclassified `◆` arm | pass (`test_milestone_marks.py:421`) |
| the `#` manager and its form obey the modal law | AT-2604 | `MarksManager` + `MarkForm` key-by-key | the modal-keys law's assertions | repr + negative: refused-over-modal `#` | pass (`test_modal_keys.py:417`) |
| the legend strip names the drawn classes | AT-2605 | the painted strips (gantt, hidden, present) | the strip in the styled frame at both sizes | repr + boundary: none-drawn arm | pass (`test_legend.py:702`) |
| hidden classes leave the gantt/present; `/#cls` filters | AT-2606 | the painted frames + the search bar | hidden milestones absent; the named bar + tally | repr + negative: unknown id arm | pass (`test_milestone_marks.py:626`) |
| an unknown class id is safe | AT-2607 | the editor + the seat | the id kept, rendered unclassified | repr + negative | pass (`test_milestone_marks.py:568`) |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | the class name/shape/colour at the form | `MarkForm` `_save` | yes — the form's keys and the saved file | TC-2606 / AT-2601 | ✓ |
| input | the class pick in the editor | `TaskModal`'s Select, `alt+m` | yes — the painted overlay at both sizes | TC-2605 / AT-2601 | ✓ |
| input | the hide toggle | `space` in the manager | yes — persisted `hidden: true` observed | TC-2606 / AT-2604 | ✓ |
| input | the `/#cls` search | the `/` bar | yes — the painted bar and the filtered frame | TC-2608 / AT-2606 | ✓ |
| output | the gantt mark (glyph/style/chip) | `views.milestone_mark` | yes — the painted frames | TC-2604 / AT-2603 | ✓ |
| output | the legend strip + hidden count | `legend_strip` / `legend_strip_project` | yes — painted at both sizes in three scenes | TC-2607 / AT-2605 | ✓ |
| output | `marks.json` on disk | `Directory._commit` | yes — on-disk read-back after every arm | TC-2601/2603 / AT-2602 | ✓ |
| output | the refused-write notice | the form + the app notice seat | yes — the exact string asserted | TC-2606 / AT-2604 | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 3152 | 0 | 84 (+67 collected from the three new files, +17 from the law-driven files — measured by the qa-reviewer at the DDR) | 3236 | 3236 | 3235 / 3235 (+1 environmental skip) | yes |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | TC-1902 (pre-existing, not this batch) | `test_win_clipboard_roundtrip` skipped: the machine's clipboard is broken OS-wide (verified from two contexts at gate time; the test's own designed machine-refusal arm). 3235/3236 passed; every batch test passed. | minor — environmental, not a code defect | operator decision: accept as environmental, or re-run chunk 00 (`suite-p4-chunk00-files.txt`) once the machine's clipboard recovers |

### Escaped-bug regression (if a defect escaped the suite)

None — no defect escaped the suite in this batch.

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

The qa-reviewer's P4 evaluation pass (2026-10-24, over this artifact, the three chunk transcripts and the mutation transcripts; it did not launch the run — the orchestrator did, `C-25`):

| # | Item | ✓/✗ | Evidence |
|---|---|---|---|
| 1 | the gate run is one complete suite, collected by the orchestrator | ✓ | three sequential chunks, transcripts `evidence/suite-p4-chunk00/01/02.txt`, exit 0 each, run on `512813d` |
| 2 | 0 failed | ✓ | every chunk summary line: "passed", no F |
| 3 | the single skip is environmental and named | ✓ (reworded per the qa-reviewer) | the chunk00 transcript prints summary-only (no `-rs`), so the identity rests on `test_app.py:1270` being chunk00's only clipboard test plus the gate-time probe, now persisted at `evidence/suite-p4-clipboard-probe.txt` (two contexts: the orchestrator's shell and the interactive console session — both fail); the test's skip clause is its designed machine-refusal arm |
| 4 | the ledger reconciles against the collection | ✓ | 3152 + 84 = 3236 = the collected count |
| 5 | every AT realises in exactly one node and passed | ✓ | the seven nodes of the DDR's B4 row, all in passing chunks |
| 6 | the mutation batteries are intact evidence | ✓ | 81/81 KILLED, 0 BAD arms, restored by hash |
| 7 | Layer B observes the deliverable at the surface | ✓ | painted-frame arms at both sizes + on-disk read-backs + the 14 captures |
| 8 | no vacuous assertions in the batch's new tests | ✓ | DDR spot-check (exact strings, hex checks, read-backs, byte-equality arms) |
| 9 | no test touches the real home; synthetic data only | ✓ | the conftest seam + per-file `home` fixtures; synthetic fixtures |
| 10 | G-001 is honestly recorded for the operator | ✓ | the Gaps table and the verdict NOTE |
