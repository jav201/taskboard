# Validation — taskboard — Batch 2026-10-07-batch-07

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
- **Layer 0:** `1` unit met the criterion (the store's lenient read) · `3` named reddening mutations over the unit and the insert's two conjuncts (M15 leniency · M13 one-step undo · M14 the links) — all KILLED
- **Requirements:** `1`/`1` pass (HLR-1301 via AT-1301's 9 arms; LLR-1301.1 · LLR-1301.2 below) · `0` blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — the templates key survives as `T` in NO live seat (HLR-1301 pins `I`, LLR-1301.2 binds `I`, the IFC node reads `keymap I` after the record-pass fix); the only `T` mentions are the append-only ledger entry, the brief minted under LED .1, and the stopped session's transcript — history, each standing beside LED-2026-10-07-batch-07.2
- **Test ledger:** ✓ reconciles (`base − D + A = post` → `2575 = 2566 − 0 + 9`)
- **Evidence checklist (qa-reviewer):** `human:coordinator` — self-executed by the close-out coordinator · `10` of `10` rows ✓ with evidence (increment-001's packet tables; `evidence/mutations.log`)

> The ONE complete run (`C-25`): the orchestrator's full suite on the gated tree at P4 — this
> artifact consumes that result; it does not re-own the run. The implementing session's ONE
> complete green run over the settled tree passed **2575 / 2575** (`evidence/inc001b-run.log`,
> 423.20s), and the close-out re-collected the suite at **2575 tests** on the final tree
> (`pytest tests --collect-only -q`). Every Layer-0/A/B row below was executed by the implementing
> agent or the close-out coordinator (`human:coordinator`) under the batch's standing
> authorization, named per row. (Candor: the session's FIRST full-suite attempt, same log at
> :722, held 21 failures — one the README keybinding census the increment then shipped, twenty
> git-state/environment arms the settled-tree re-run cleared; the green 2575 is the settled,
> reproducible result.)

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| the store's lenient read (`models.templates`/`_read_template`, `models.py:2284-2326`) | the isinstance/branch cascade over entries → tasks → titles/notes/waits; cyclomatic ≥3 | `test_round_trip_reads_back_equal` · `test_lenient_read_skips_junk_and_drops_bad_waits` · `test_presets_present_with_names_and_counts` · `test_no_user_templates_returns_presets_only` | pass (mutation M15 below) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| the store's lenient read | M15: `templates()` raises ValueError on a non-dict entry instead of skipping | yes — `1 failed, 3 passed` on `tests/test_templates.py`: the lenient-read arm (the six-shape junk list) reddened; the round-trip, presets, and presets-only arms stayed GREEN (named in increment-001's packet) | `evidence/mutations.log` M15 |
| the insert's one-step undo conjunct | M13: `{"templates": [t.id for t in created]}` → `{"templates": [created[0].id]}` | yes — `1 failed, 4 passed` on `tests/test_templates_app.py`: the undo arm reddened (one `u` leaves two inserted tasks behind); the four non-undo arms stayed GREEN | `evidence/mutations.log` M13 |
| the insert's linking conjunct | M14: the `wait` application (`new.depends_on = [created[one.wait].id]`) → `pass` | yes — `2 failed, 3 passed` on `tests/test_templates_app.py`: the exact-chain arm and the user-template chain arm reddened; the picker/no-project/empty arms stayed GREEN | `evidence/mutations.log` M14 |

### UX walkthrough — only if trigger family D fired

Family D did NOT fire this batch — no operator-feedback surface (the batch ships a commissioned
feature, not a report's remedy). The acceptance arms below ARE the automated walkthrough, driven
through the real mechanism; the three evaluation states are declared under the table.

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| press `I` and the picker lists presets with counts | `TaskboardApp` driven with keys through `run_test` (key `I`) | the `#template-list` OptionList paints `["Simple chain — 3 tasks", "Bugfix — 3 tasks"]` | ✓ |
| pick `Simple chain` on a board with a selected task | `enter` on the highlighted row | 3 tasks exist in that task's project, first phase, no dates, `depends_on` the exact forward chain; the toast renders `Inserted 'Simple chain' — 3 tasks into Plat` byte-exact | ✓ |
| `u` after the insert | key `u`, then `u` again | all 3 removed in one step; the second `u` toasts `Nothing to undo.` — no resurrection | ✓ |
| `I` with no resolvable project | key `I` on an empty board | no picker; the refusal toast `No project to insert into.` | ✓ |
| a user template lists before the presets and inserts with its links | a `settings["templates"]` board, `I`, `enter` | the rows `["Deploy — 2 tasks", "Simple chain — 3 tasks", "Bugfix — 3 tasks"]`; the insert lands linked; the toast names `Deploy` | ✓ |
| an empty template | `enter` on `Empty — 0 tasks` | nothing inserted; `Template 'Empty' is empty.` | ✓ |

**Mechanism used:** Textual's `run_test` pilot — the criteria driven through the REAL mechanism,
their painted results asserted off the emitted widgets/toasts/rows.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — AT-1301's 5 app arms drive the app with keys and read the painted surface + board state |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — the close-out coordinator read the picker rows, the toast bytes, and the undo sequence against the contract's arms (C-32) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — no trigger-D surface this batch; the batch-06 visual re-verdict stays PENDING in the backlog (carried, not this batch's gate) |

- **Method:** the arms' fixtures — synthetic boards in `tmp_path` (the house pilot at 100×30)
- **Participants or population:** none — no user session this batch
- **Evidence of the evaluation:** `evidence/inc001b-run.log`, `evidence/mutations.log`, `tests/test_templates.py`, `tests/test_templates_app.py`, the close suite re-collection
- **Limits:** no user performed the walkthrough; the operator's eye remains owed on the batch-06 frames/chrome (the carried re-verdict), and the template picker itself is fresh surface the operator has not yet seen

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-1301 | test | `pytest tests/test_templates.py tests/test_templates_app.py -q` | 0 failures; the 9 arms: store round-trip · lenient read · presets · presets-only · picker census · the insert with links + one undo + the toast · no-project refusal · user-template precedence · the empty template | pass | `evidence/inc001b-run.log` (9 passed; the full green at 2575); M13/M14/M15 |
| LLR-1301.1 | test (unit) | the 4 store arms | the junk list → only the valid entries; a bad `wait` drops the link, keeps the task; presets ship `Simple chain`/`Bugfix` with exact names, shapes, counts; an absent/empty settings list → presets only | pass | `models.py:2253-2326`; M15 |
| LLR-1301.2 | test (integration) | the 5 app arms | `I` opens the picker (global, palette-only, group misc); the pick lands N tasks in the right project, first phase, no dates, `depends_on` exact; ONE undo entry removes all; the toast equals the pinned literal; the `?` bullet names `I` and the board-JSON edit seat | pass | `app.py:723-763` · `:1499-1511`; `modals.py:933-977`; `keymap.py:139`; `views.py:6837`; `README.md:135`; M13/M14 |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-1301 | AT-1301 (the dash token in `tests/test_templates_app.py`'s docstring, line 3) | the app pilot — keys `I`/`enter`/`u`, the picker, the toast, the board | the painted picker rows + the rendered toast bytes + `board.tasks`/`depends_on` after each act | repr: `Inserted 'Simple chain' — 3 tasks into Plat` · boundary: an empty template (inserts nothing, says so) and a board with no user templates (presets still list) · negative: no resolvable project → the refusal toast; a second `u` → `Nothing to undo.` (no resurrection) | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | key `I` (global, palette-only) | `action_templates` ← `keymap.py:139` + `BOARD_ACTIONS` (`app.py:331`) | yes | AT-1301 (`test_I_opens_the_picker_listing_presets_with_counts`) | ✓ |
| input | the selection / the focused project | `present_project_id(board, selected, focused)` | yes | AT-1301 (the insert lands in the selected task's project) | ✓ |
| input | the pick (enter / esc) | `TemplatePicker.on_option_list_option_selected` → `dismiss(name)` | yes | AT-1301 (the insert arm; esc is the shipped modal chrome) | ✓ |
| input | a user template in `settings["templates"]` (valid · junk-shaped · empty) | `models.templates`/`_read_template` | yes | the round-trip/lenient arms · `test_user_template_lists_before_presets_and_inserts_with_links` · `test_empty_template_toasts_is_empty` | ✓ |
| input | a board with no resolvable project | `action_templates`'s refusal branch | yes | AT-1301 (`test_no_project_refuses_with_the_toast`) | ✓ |
| output | the picker rows (`name — N tasks`, user first) | the `#template-list` OptionList | yes | AT-1301 (the two census assertions) | ✓ |
| output | the created chain (tasks + `depends_on`) | `board.tasks` after the pick | yes | AT-1301 (titles, project, phase, no dates, the exact chain) | ✓ |
| output | the outcome toast (insert / refusal / empty) | the painted `Toast` | yes | AT-1301 (`_toast_check`, byte-exact) | ✓ |
| output | the one-step undo | `u` → `action_undo`'s `"templates"` branch | yes | AT-1301 (all removed; second `u` says `Nothing to undo.`) | ✓ |
| output | the `?` help bullet + the README row | `views.help_usage` · the README keybinding table | yes | the bullet at `views.py:6837`; the census test at `tests/test_keymap.py:404` | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2566 | 0 | 9 | 2575 | 2575 | 2575 / see the C-25 run | yes |

base = the batch-06 trunk (2566); A = the batch's 9 new nodes — `tests/test_templates.py` (4) ·
`tests/test_templates_app.py` (5); the README row and the `?` bullet modified no test. The
close-out re-collected the suite at **2575 tests** on the final tree (`pytest tests
--collect-only -q`), and the implementing session's complete green run passed 2575
(`evidence/inc001b-run.log`, 423.20s); the orchestrator's C-25 close run owns the final passed
count.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| — | — | none — no test gap detected; the M13-M15 battery is all-KILLED with per-node verdicts, and the one spec deviation (the README row outside the brief's file list) is forced by a shipped census test, declared in increment-001's packet and `02-review.md`, not a gap | — | — |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| — none — no defect escaped the suite this batch (the T-key conflict was caught BEFORE the first edit by the stop gate, not by a reddened suite — `evidence/inc001-run.log`) | | | | | |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

`qa-reviewer` — self-executed by the close-out coordinator (`human:coordinator`; the runtime spawned nobody, named per the dev-flow runtime rule):

- [x] Acceptance criteria observable — AT-1301 reads the painted picker rows + the rendered toast bytes + `board.tasks`/`depends_on` through the app pilot (`tests/test_templates_app.py` · `tests/test_templates.py`)
- [x] Test cases have explicit Expected — the exact picker row census; the pinned toast literals (`Inserted 'Simple chain' — 3 tasks into Plat` · `No project to insert into.` · `Template 'Empty' is empty.`); the exact `depends_on` forward chain; `Nothing to undo.` after the second `u`; the presets' names/shapes/counts
- [x] Edge cases include empty, boundary, invalid, error — the Boundary catalog fields across the contract: ☑ empty (an empty template — inserts nothing, says so; no user templates — presets still list) ☑ boundary (a bad `wait` — the link drops, the task stays; a template as the FIRST link of a project) ☑ invalid (the six-shape junk list — skipped, never raising) ☑ error (no resolvable project — the refusal toast)
- [x] Regression checklist exists — the reverse census (5 probes), the M13-M15 battery with per-node verdicts and named GREEN arms, the supersession inspection over the T→I correction (0 live `T` refs), the suite re-collection at 2575
- [x] Exit criteria stated — the contract §5.2's criteria, all met (every HLR a passing AT; every new assertion RED by a recorded mutation or by construction at base; full suite green at the last settled run; the batch-06 visual re-verdict kept pending per §5.2)
- [x] No real PII / secrets — synthetic boards in `tmp_path` throughout; no operator board data read or written
- [x] **Mode declared** — validation mode: this artifact, Result PASS; every executed result names its executor (the implementing sessions or the close-out coordinator; the orchestrator for the ONE full C-25 run)
- [x] **Layer B (black-box)** — the story's deliverable observed through the shipped surface with boundary + negative (the Layer B table)
- [x] **Bidirectional surface-reachability** — the matrix above, 10/10 rows ✓
- [x] **No unfilled template** — the verdict fields filled; the artifacts carry no placeholder cells naming nothing
