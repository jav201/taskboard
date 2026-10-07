# Validation — taskboard — Batch 2026-10-07-batch-05

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
- **Layer 0:** `3` unit(s) met the criterion · `3` carry a named reddening mutation (M1/M2 for `_create_beside`'s failure path · M4 for `_clip_words` · M6/M7 for the fold's cap branch) · `1` further unit-level surface (the resize heal) carries M8 — SURVIVED-with-cause, declared in `03-increments/increment-003.md` §4 with its GREEN arm named
- **Requirements:** `6`/`6` pass (HLR-1101..1106 via AT-1101..1106/the amended TC-810/AT-801c; LLR-1101.1..1106.1 via the named arms) · `0` blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — TC-810 renamed/amended riding **LED-2026-10-07-batch-05.1** (the old node name `test_TC_810_the_fold_drops_whole_bands_never_a_dangling_head` has 0 surviving refs; the zero-fit whole-drop law survives INSIDE the amended node); the second/third `def _md` have 0 surviving refs (views.py/app.py hold only the import rows); the amended arms' direct `selected_task_id` assignments have 0 surviving refs
- **Test ledger:** ✓ reconciles (`base − D + A = post` → `2556 = 2546 − 0 + 10`)
- **Evidence checklist (qa-reviewer):** `human:coordinator` — self-executed by the close-out coordinator · `10` of `10` rows ✓ with evidence (`02-review.md`; the per-increment packet tables)

> The ONE complete run (`C-25`): the orchestrator's full suite on the gated tree at P4 — this
> artifact consumes that result; it does not re-own the run. The increments' own full passes were
> mid-flight checkpoints (2550 collected at inc-001 — 2530 passed + 20 environmental failures
> OUTSIDE its files, triaged in `evidence/env-flake-note.md` with the four files re-run clean, 45
> passed; 2555 at inc-002; **2556 passed, 0 failed at inc-003 — the last complete green over the
> settled tree**, `evidence/inc003-run.log`). The close-out's own sweep re-collected the suite at
> **2556 tests** on the final tree. Every Layer-0/A/B row below was executed by the close-out
> coordinator (`human:coordinator`) or the implementing agent under the batch's standing
> authorization, named per row.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `_create_beside`'s failure path (models.py:1562-1583) | crosses the OS seam (exclusive create → failed write → close → unlink → re-raise); nested guards, cyclomatic ≥3 | `test_failed_write_leaves_no_partial_file` · `test_refusing_unlink_never_masks_the_write_error` | pass (mutations M1/M2 below) |
| `_clip_words` (modals.py:1750-1767) | cyclomatic ≥3 — degenerate width / fits / word loop / unbreakable token | `test_TC_1104_clip_words_exact_edge_and_overlong_token` | pass (mutation M4 below) |
| the chainmap fold's cap branch (views.py:5798-5871) | the fit / partial / zero-fit split, cyclomatic ≥3 | `test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole` | pass (mutations M6/M7 below) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `_create_beside`'s failure path | M1: the guarded unlink removed (no unlink) | yes — arm 1: `1 failed`, the partial file survived | `evidence/mutations-abc.log` M1 |
| `_create_beside`'s failure path | M2: the guard removed (unguarded unlink — the masking revert) | yes — arm 2: `1 failed`, the refusing unlink escaped (`EACCES` over `ENOSPC`) | `evidence/mutations-abc.log` M2 |
| `_clip_words` | M4: the fit-check → `if True: return s` (never clip) | yes — the unit pin: `assert 'the project ...most pressure' == 'the project under…'` (the integration arm stayed GREEN vacuously — named in increment-002's packet) | `evidence/m4-arms.log` (per-node re-run) + `evidence/mutations-abc.log` M4 |
| the fold's cap branch | M6: `+{tail_n} more ↓` → `+{tail_n + 1} more ↓` (N off by one) | yes — `assert "+4 more ↓" in text` against the painted `+5` | `evidence/mutations-d.log` M6 |
| the fold's cap branch | M7: the zero-fit guard `break` → `limit = 1` (the dangling head) | yes — the zero-fit band's tiles leaked into the line_map | `evidence/mutations-d.log` M7 |
| the resize heal (`_heal_selection_after_repaint`, app.py:1526-1544) | M8: the heal neutered — the guard → `if True: return`, AND the call removed entirely | **no — SURVIVED-with-cause, declared**: the shipped `_select_first` chainmap branch + the fold-aware `_nav_flat()` heal the END-STATE on the next refresh, and `pilot.pause()` drains every pending refresh, so AT-801c observes the healed end-state no matter which mechanism got there first; the heal's value is the transient-free first paint + the nearest-row landing — a transient-level difference an end-state arm cannot isolate without pinning Textual's own refresh churn (3 per measured resize) · follow-up named in the transcript: a NEW paint-level arm, not a block | `evidence/mutations-d.log` M8 |

### UX walkthrough — only if trigger family D fired

Family D fired (two ux-filed carries ship this batch: UXV-3 the silent undo · UXV-6 the mid-word help cut).

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| `u` after a single-task change names what came back | `TaskboardApp` driven with keys through `run_test` (a real single-task mutation, then `u`) | the painted `Toast` equals `Undone — Write the migration guide is back as it was.` (`title="Undo"`, `markup=False`) | ✓ |
| the `?` help at 80 cells never cuts a word in half | the `?` modal opened at 80×24 through the pilot on the fixture board | every visible line of both help columns ends at a word boundary or with `…` | ✓ |

**Mechanism used:** Textual's `run_test` pilot — the criteria driven through the REAL mechanism, their painted results asserted off the emitted widgets.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — AT-1103/AT-1104 drive the app and assert the painted results |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — the close-out coordinator read the pinned literals and the per-line tails against the contract's arms (C-32) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a carries batch ships no new user task; the operator's standing visual verdict covers the app at the next session |

- **Method:** the arms' fixtures — synthetic boards in `tmp_path`, the house pilot at 80×24
- **Participants or population:** none — no user session this batch
- **Evidence of the evaluation:** `evidence/inc002b-run.log`, `tests/test_undo_toast.py`, `tests/test_help_clip.py`, the close suite
- **Limits:** no user performed the walkthrough; the operator's eye is owed on the toast and the help at the next visual verdict

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-1101 | test | `pytest tests/test_backup_write.py -q` | 0 failures; both arms green (no partial file + original error; refusing unlink → original error unmasked) | pass | `evidence/mutations-abc.log` M1/M2; models.py:1562-1583 |
| HLR-1102 | test | `grep -c "def _md" taskboard/*.py` then 1 · `pytest tests/test_mon_d.py -q` | exactly one `def _md`; the 14-date sweep identical through every access path | pass | models.py:2147; views.py:38; app.py:38 |
| HLR-1103 | test | `pytest tests/test_undo_toast.py -q` | the toast equals the pinned literal exactly; the purged skip stays silent (0 toasts) | pass | app.py:1468-1469; `evidence/m3-anchor-fix.log` |
| HLR-1104 | test | `pytest tests/test_help_clip.py -q` | at 80×24 every visible help line ends at a word boundary or with `…`; the exact-edge/overlong arms | pass | modals.py:1750-1794,1862-1867; `evidence/m4-arms.log` |
| HLR-1105 | test | `pytest tests/test_chainmap.py tests/test_chainmap_app.py -q` | the amended TC-810 (the exact `+4 more ↓` tail; the zero-fit whole-drop); AT-801c (selection valid after ONE refresh); AT-801b's docstring | pass | views.py:5798-5871; app.py:1524-1544; `evidence/mutations-d.log` M6/M7 |
| HLR-1106 | test | `pytest tests/test_milestones.py tests/test_gantt_milestones.py -q` + the grep pin | the amended arms walk with keys (no direct assignment in an amended body); the ash at the exact column; the team-folder arm | pass | the two files; `evidence/mutations-abc.log` M5 |
| LLR-1101.1 | test (unit) | the two mechanism arms | arm 1: the file does not exist after the call, the original `OSError` propagates; arm 2: the original still propagates — the guard adds nothing | pass | models.py:1573-1586; M1/M2 |
| LLR-1102.1 | test (unit) | the identity pin + the sweep | exactly 1 definition; identical strings across the three access paths (now one object) | pass | `tests/test_mon_d.py`; the census counts |
| LLR-1103.1 | test (integration) | the positive pin + the purged-skip arm | the pinned 1-line literal with the task's title; 0 toasts on the skip | pass | app.py:1468-1469; M3 |
| LLR-1104.1 | test (integration) | the integration arm + TC-1104 | no mid-word tail at 80×24; the exact-edge and overlong-token pins | pass | modals.py; M4 |
| LLR-1105.1 | test (integration) | the amended TC-810 + AT-801c + the docstring arm | the cap row present with N exact; the zero-fit band drops whole; the selection valid after one refresh; the docstring matches the body | pass | M6/M7; M8 declared |
| LLR-1106.1 | test (integration) | the amended arms + the grep pin | no `selected_task_id` assignment in an amended arm body; the outcomes byte-identical | pass | M5; `evidence/inc004-run.log` |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-1101 (S5-3) | AT-1101 | the helper with a synthesized full disk (the `_FlakyFile` fault) + a refusing removal | the `tmp_path` listing + the propagated errno | repr: ENOSPC named · boundary: removal works vs refuses · negative: the refusing-removal arm — the guard adds no new error | pass |
| US-1102 (F-6) | AT-1102 | the import rows + the sweep through every render consumer | the rendered `Mon D` strings across the views (byte-identical) | repr: `Feb 29`/`Dec 31` · boundary: month/year edges in the sweep · negative: the pre-dedup 3-definition census is the RED control | pass |
| US-1103 (UXV-3) | AT-1103 | the app driven with keys (a real single-task mutation, then `u`) | the painted `Toast` | repr: the pinned literal naming the task · boundary: a long title clipped by the toast width · negative: the purged skip stays silent | pass |
| US-1104 (UXV-6) | AT-1104 | the `?` modal at 80×24 through the pilot | every visible help line of both columns | repr: clipped lines end with `…` · boundary: the exact-edge word + the overlong unbreakable token · negative: a fixture line whose only break was mid-word (GREEN only via the clip) | pass |
| US-1105 | AT-801c + the amended TC-810 | the chain map at the pinned sizes through the pilot/renderer | the painted canvas + the emitted `line_map` + the healed selection | repr: `+4 more ↓` exact · boundary: exactly-fits vs one-chain-over · negative: the zero-fit band drops whole (head AND canvas) | pass |
| US-1106 | AT-601/602 (amended) + the team-folder arm | the editor/gantt/offer driven with keys | the same outcomes reached by the arrows; the team file's bytes | repr: outcomes byte-identical · boundary: the bidirectional walk to `ta1` above the start · negative: the grep pin on a planted direct assignment | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | a full disk at the backup write | the ENOSPC-raising `write` (the `_FlakyFile` fault) | yes | AT-1101 arm 1 | ✓ |
| input | a removal that refuses | the EACCES `Path.unlink` | yes | AT-1101 arm 2 | ✓ |
| input | the `u` key after a single-task change | `action_undo`'s single-task fall-through | yes | AT-1103 | ✓ |
| input | the `?` key at 80 cells | `HelpModal` through the pilot | yes | AT-1104 | ✓ |
| input | a terminal resize | `refresh_view` at the new size | yes | AT-801c | ✓ |
| input | the arrows (the selection walks) | the shipped navigation (`_nav_flat()`) | yes | the amended AT-601/602 | ✓ |
| output | NO partial file + the original error | the board folder's listing + the propagated errno | yes | AT-1101 | ✓ |
| output | the one-line undo toast | the painted `Toast` | yes | AT-1103 | ✓ |
| output | the word-boundary-clipped help lines | the painted `#help-left`/`#help-right` lines | yes | AT-1104 | ✓ |
| output | the capped fold `+N more ↓` + the healed selection | the painted canvas + the emitted `line_map` + `selected_task_id` | yes | TC-810 · AT-801c | ✓ |
| output | the team file's bytes | `board.jav.json` (polled ≤5s) | yes | the team-folder arm | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2546 | 0 | 10 | 2556 | 2556 | 2556 / see the C-25 run | yes |

base = the trunk batch-03+batch-04 merge (batch-03's 2541 + batch-04's 5); A = the batch's 10 new
nodes — `tests/test_backup_write.py` (2) · `tests/test_mon_d.py` (2) · `tests/test_undo_toast.py`
(2) · `tests/test_help_clip.py` (2) · `AT-801c` (1) · the team-folder arm (1); the TC-810 rename,
the AT-801b docstring, and the AT-601/602 amendments modified, not added. The close-out
re-collected the suite at 2556 on the final tree, and the last complete green run over the
settled tree passed 2556 (`evidence/inc003-run.log`); the orchestrator's C-25 close run owns the
final passed count.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| — | — | none — no test gap detected; M8 is a declared SURVIVED-with-cause (the shipped behavior is correct; the end-state arm cannot isolate the heal's transient-level value) with its follow-up named in `evidence/mutations-d.log`, not a gap | — | — |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| AT-1101 (S5-3, carried from batch B2a) | the filing — a partial `board.json.backup` survived a failed write (the next run takes `.1`, the junk accumulates) | shape (junk on disk pretending to be a backup) | yes — the directory listing + the errno discriminate a survivor, a masked error, and a missing cleanup | 2 arms green | `test_failed_write_leaves_no_partial_file` · `test_refusing_unlink_never_masks_the_write_error` |
| AT-1102 (F-6, carried) | the review's read — three byte-identical `def _md` copies invite a fix in one view that starves another | shape (a divergence risk) | yes — the identity pin + the 14-date sweep discriminate a shadowed/divergent body | 2 nodes green | `test_one_md_definition_shared_by_all` · `test_md_renders_identically_through_every_access_path` |
| AT-1103 (UXV-3, carried) | the kanban `M` left/rejoined a card with no message — the user scanned the board for what changed | value (silence) | yes — the exact pinned literal with the task's title; the purged skip stays silent | 2 nodes green | `test_AT_1103_undo_names_the_single_task` · `test_AT_1103_purged_entry_stays_silent` |
| AT-1104 (UXV-6, carried) | the 80-cell help cut lines mid-word with no `…` | value (a screen that stops matching the user's words) | yes — the per-line tail assertion + the exact-edge/overlong pins | 2 nodes green | `test_AT_1104_help_lines_end_at_word_boundary` · `test_TC_1104_clip_words_exact_edge_and_overlong_token` |
| the amended TC-810 + AT-801c (rev-2 + batch C, carried) | deep chains folded WHOLE at typical heights; the resize heal leaned on a second refresh; AT-801b's docstring overclaimed | shape (vanished bands · a two-refresh heal) | yes — the exact `+4 more ↓` tail + the zero-fit line_map absence + the one-refresh end-state | 13 nodes green across the two chainmap files | `test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole` · `test_AT_801c_a_resize_heals_the_selection_in_one_refresh` |
| the amended AT-601/602 + the team-folder arm (qa P4 F-3..F-5, carried) | the arms assigned `selected_task_id` directly (the render, not the path); the ash was checked "at any column"; nothing pushed offer-converted milestones to a team folder | shape (a shortcut that proves less than the user's path) | yes — the grep pin discriminates a planted assignment; the axis-math pin discriminates "any ◆"; the team-file bytes discriminate a broken push | 71 nodes green across the two files | `test_AT_601_…` · `test_AT_602_…` · `test_AT_601_offer_converted_milestones_reach_a_team_folder` |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

`qa-reviewer` — self-executed by the close-out coordinator (`human:coordinator`; the runtime spawned nobody, named per the dev-flow runtime rule):

- [x] Acceptance criteria observable — AT-1101 asserts the directory listing + errno; AT-1103 reads the painted `Toast`; AT-1104 reads the painted per-line help text; TC-810 asserts the painted tail + the emitted `line_map`; the team arm polls the team file (`tests/test_backup_write.py` · `test_undo_toast.py` · `test_help_clip.py` · `test_chainmap.py` · `test_milestones.py`)
- [x] Test cases have explicit Expected — the pinned toast literal; the exact `+4 more ↓`; the exact ash column `("◆", REACHED)`; the 14 sweep strings; the one-definition census
- [x] Edge cases include empty, boundary, invalid, error — the Boundary catalog fields across the contract: ☑ error (ENOSPC/EACCES) · ☑ boundary (month/year edges; exact-edge word; overlong token; exactly-fits vs one-over) · ☑ empty (the purged skip; the zero-fit band; the degenerate widths) · ☑ invalid (the planted-assignment probe)
- [x] Regression checklist exists — the reverse census (5 probes × 4 packets), the M1-M8 battery with per-node verdicts, the C-2b oracle byte-green check, the env-flake note (the 20 triaged), the full close suite
- [x] Exit criteria stated — the contract §5.2's criteria, all met (every HLR a passing AT; every new assertion RED on the base tree or by a recorded mutation; full suite green at the last settled run; the BACKLOG carries marked done)
- [x] No real PII / secrets — synthetic boards in `tmp_path`; the team fixture is the house pattern
- [x] **Mode declared** — validation mode: this artifact, Result PASS; every executed result names its executor (the close-out coordinator, the implementing agent, or the orchestrator for the ONE full run)
- [x] **Layer B (black-box)** — every story's deliverable observed through the shipped surface with boundary + negative (the Layer B table)
- [x] **Bidirectional surface-reachability** — the matrix above, 11/11 rows ✓
- [x] **No unfilled template** — the verdict fields filled; the artifacts carry no placeholder cells naming nothing
