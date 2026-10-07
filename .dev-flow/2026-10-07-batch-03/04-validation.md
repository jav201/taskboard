# Validation — taskboard — Batch 2026-10-07-batch-03

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Result` · `Layer 0` · `Evidence checklist` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.
>
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.
> A Spanish batch writes `- **Result:** PASS`, not `- **Resultado:** aprobado`: the label, the tokens and the
> reviewer-identity tokens below are the machine's vocabulary.

- **Result:** PASS
- **Layer 0:** 4 unit(s) met the criterion · 3 carry a named reddening mutation
- **Requirements:** 3 HLR + 3 LLR pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative
- **Test ledger:** ✓ reconciles (`base − D + A = post`)
- **Evidence checklist (qa-reviewer):** qa-reviewer — self-executed by the close-out coordinator · 10 of 10 rows ✓ with evidence (`02-review.md`)

> The ONE complete run (`C-25`): the orchestrator's full suite on this tree — **2541 passed, 0 failed**
> (run 2026-10-07 on the gated tree; G-011 did not fire). This artifact consumes that result; it does
> not re-own the run. Every Layer-0/A/B row below was executed by the close-out coordinator (named per
> row) under the batch's standing authorization.

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `_coerce_title` (models.py:782-791) | cyclomatic ≥ 3 — None / list·dict / try·except | TC-902 ×5 params | pass (mutation M1 below) |
| `run_link_migration`'s error path (models.py:1618-1633) | crosses the save/restore seam | TC-901 (+ its happy-path arm) | pass (mutation M2 below) |
| `_fold_row` (views.py:5151-5181) | cyclomatic ≥ 3 — the fit/clipping branches | TC-311 census ×7 + AT-903[3_fold] | pass (mutations M1/M2 below) |
| `_fold_keep` (views.py:5130-5148) | cyclomatic ≥ 3 — the two while-loops | the 9-node TC-311 census | pass (transitively: its keep-lists feed every fold assertion; no direct mutation — its seat is the CL-7 share both renderer and legend read) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `_coerce_title` | container branch returns `str(value)` (the repr) instead of `Untitled` | yes — TC-902[list] `assert "['x']" == 'Untitled'`, TC-902[dict] `assert "{'a': 1}" == 'Untitled'`; the int/null/bool arms stayed GREEN | `evidence/inc001-mutations.log` M1 |
| `run_link_migration`'s error path | the unguarded backup/log `unlink` moved BEFORE the restore | yes — TC-901 `1 failed`: the refusing unlink escapes the handler | `evidence/inc001-mutations.log` M2 |
| `_fold_row` | M1: the down seat renamed `▼ N below` → `▾ N more` · M2: `if late_ms:` made unreachable | yes — M1: the census `7 failed, 2 passed` + AT-903[3_fold] `1 failed` · M2: AT-903[3_fold] `1 failed` with the census GREEN | `evidence/inc002-mutations.log` M1/M2 |

### UX walkthrough — only if trigger family D fired

Family D fired (state.json triggers: D1 — a ux-filed item, UX2-2's fold-row marker).

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| a late milestone below the kanban fold marks the fold row `▼ N below · ▲1 ◆` | `TaskboardApp`/`render_kanban` at 118×24 on the kg milestones board (the AT-903 arm-3 fixture) | the emitted fold row reads `▼ 2 below: Data Warehouse (4 open), Ops & Security (5 open) · ▲1 ◆` | ✓ |
| the `?` legend names `◆` only for drawn bands | the app driven with the `?` key + a search query hiding every milestone band (arm 1, through HelpModal) | the legend lines lose `a milestone on its project's band rule` | ✓ |

**Mechanism used:** a UI test driver (Textual's `run_test` pilot) + the renderers' emitted frames

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — AT-903's four arms drive the app / the renderer at 118×15/24/30/40 and assert the painted result |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — the close-out coordinator read the painted frames against the contract's arms (C-32) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a cleanup batch ships no new user task; the marker's acceptance is review-filed and census-pinned. The operator's standing visual verdict covers the app at the next session |

- **Method:** the arms' fixtures — synthetic boards in `tmp_path`, the kg milestones board for the fold
- **Participants or population:** none — no user session this batch
- **Evidence of the evaluation:** `evidence/inc002-mutations.log` (the emitted fold-row bytes), `tests/test_cleanup.py:334-339`, the close suite
- **Limits:** no user performed the walkthrough; the operator's eye is owed on the marker at the next visual verdict

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-901 | test | `pytest tests/test_cleanup.py -q -k TC_901` | TC-901's refusing-unlink arm: board bytes + mark restored, `result.error` names the original, no escape | pass | `evidence/inc001-mutations.log` — 12 passed at baseline; M2's kill reddens exactly this node |
| HLR-902 | test | `pytest tests/test_cleanup.py -q -k TC_902` | the five exact strings `5`/`Untitled`/`Untitled`/`Untitled`/`True` + the round-trip | pass | same log — TC-902 ×5 green; M1's kill reddens exactly the container arms |
| HLR-903 | test | `pytest tests/test_cleanup.py -q -k AT_903` + `pytest tests/test_kanban_readable.py -q -k TC_311` | AT-903's four arms on painted frames + the 7-fold literal census | pass | `evidence/inc002-mutations.log` — 12 passed + census 9 passed |
| LLR-901.1 | test (unit) | the TC-901 arm (the mechanism level) | the restore-first order, the nested best-effort guard | pass | models.py:1618-1633; M2 |
| LLR-902.1 | test (unit) | the TC-902 arms | the coercion rule per shape | pass | models.py:782-791, :875-877; M1 |
| LLR-903.1 | test (integration) | the AT-903 arms + the census | the drawn-band legend, the D-623 band, the fold marker, the marker-only `◆` sites | pass | views.py seats named in `03-increments/increment-002.md` §1; M1/M2 |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a verification nobody ran. Write your own rows in the table above.

```text
| *(example)* HLR-001 | test | `pytest … -k TC-001` | exit 0 | | |
| *(example)* LLR-001.1 | test (unit) | `…` | `…` | | |
```

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-901 | AT-901 | the app at startup on a failing legacy board (monkeypatched OS seams) | the exit message (`capsys`) + the board file's bytes | repr: the original failure named · boundary: the save fails AND the cleanup refuses · negative: the happy path converts and cleans up | pass |
| US-902 | AT-902 | the app on the `5`-title board + the kanban frame | the task's row on the painted frame; `app.board.task_by_id("t1").title == "5"` | repr: the coerced string shown · boundary: all five shapes at the load boundary · negative: a missing key stays `Untitled` | pass |
| US-903 | AT-903 (×4 arms) | the kanban/`?`/lanes/agenda/focus surfaces at 118×15/24/30/40 | the painted frames + the legend lines | repr: the exact legend lines and the `▼ N below · ▲1 ◆` row · boundary: the exactly-full fold · negative: the filter-empty legend | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | a board file with non-text titles | `Board.load` → `Task.from_dict` | yes — the five shapes + the missing key | TC-902 | ✓ |
| input | a legacy board whose migration fails | `run_link_migration` (the save refuses, the cleanup refuses) | yes | TC-901 / AT-901 | ✓ |
| input | a search query hiding the milestone bands | the kanban `?` legend seat (HelpModal) | yes — arm 1 drives the `?` key with the query set | AT-903[1_legend] | ✓ |
| input | the terminal's width/height | `render_kanban(width, height)` | yes — 118×15/24/30/40 and the census's ×4 sizes | TC-311 / AT-903 | ✓ |
| output | the restored board + mark on failure | the board file's bytes + `links_marked` | yes — byte-compare + reload | TC-901 | ✓ |
| output | `result.error` / the exit message | the migration's returned reason / the app's exit | yes — exact-string assertions | TC-901 / AT-901 | ✓ |
| output | the coerced board on disk | the saved file's bytes | yes — `"title": "5"` in the file bytes | TC-902 | ✓ |
| output | the painted frames (kanban fold row, the three views, the legend lines) | the renderers' emitted text | yes — the emitted-form table in increment 002 | AT-903 | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2529 | 0 | 12 | 2541 | 2541 | 2541 / 2541 | yes |

base = Batch C's close gate (`evidence` of 2026-10-07-batch-02/close-gate.txt: 2529 passed, exit 0); A = `tests/test_cleanup.py`'s 12 nodes; the `tests/test_team_sync.py` change modified, not added. The orchestrator's close suite collected 2541 and passed 2541 — the ledger reconciles.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| — | — | none — no gap detected; the two minor review findings (dead `isinstance` guard; PLAN template cells) are notes, not test gaps | — | — |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| TC-902 (S-9, pre-existing) | the filing itself — a board with `"title": 5` (or a list) reached string-only render paths and crashed; no arm existed | shape (a crash at render) | yes — the five exact strings discriminate a repr, a skip, and a crash | 12 passed in `tests/test_cleanup.py` | `test_TC_902_a_non_text_title_coerces_at_the_boundary[…]` |
| TC-901 (S-4, filed 2026-10-04) | the review's read — a refusing `unlink` could raise before the board/mark were restored | shape (an escaped/replaced error) | yes — `result.error` names the original, the bytes and the mark are restored, no exception escapes | TC-901 + its happy-path arm green | `test_TC_901_the_failed_migration_restores_first_and_surfaces_the_original_error` |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

`qa-reviewer` — self-executed by the close-out coordinator (the runtime spawned nobody; named per the dev-flow runtime rule):

- [x] Acceptance criteria observable — AT-901/902/903 assert file bytes, exit text, painted frames — no vague "works" (`tests/test_cleanup.py`)
- [x] Test cases have explicit Expected — TC-902's five exact strings; AT-903's exact legend lines + the `▼.*▲1 ◆` regex
- [x] Edge cases include empty, boundary, invalid, error — the Boundary catalog fields: ☑ invalid · ☑ error · ☑ empty · ☑ boundary
- [x] Regression checklist exists — the reverse census (5 probes × 2 increments), the folded team_sync expectation (16 passed), the 7-fold census, and the full close suite
- [x] Exit criteria stated — the contract §5.2's five criteria, all met
- [x] No real PII / secrets — synthetic boards in `tmp_path` (test file docstring)
- [x] **Mode declared** — validation mode: this artifact, Result PASS; every executed result names its executor (the close-out coordinator, or the orchestrator for the ONE full run)
- [x] **Layer B (black-box)** — every story's deliverable observed through the shipped surface with boundary + negative (the Layer B table)
- [x] **Bidirectional surface-reachability** — the matrix above, 8/8 rows ✓
- [x] **No unfilled template** — the contract's 12 placeholder cells filled; the artifacts carry no `<…>` placeholders naming nothing
