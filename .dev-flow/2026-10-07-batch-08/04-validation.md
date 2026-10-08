# Validation — taskboard — Batch 2026-10-07-batch-08

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
- **Layer 0:** `1` unit met the criterion (the component walk `models.chain_template`) · `2` named reddening mutations over the unit and the save's write conjunct (M17 the walk neutered · M16 the save writes nothing) — all KILLED
- **Requirements:** `1`/`1` pass (HLR-1401 via AT-1401's 11 arms; LLR-1401.1 below) · `0` blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — nothing superseded this batch (all-new symbols; the V-3 inspection reads `none`)
- **Test ledger:** ✓ reconciles (`base − D + A = post` → `2586 = 2575 − 0 + 11`)
- **Evidence checklist (qa-reviewer):** `human:coordinator` — self-executed by the close-out coordinator · `10` of `10` rows ✓ with evidence (increment-001's packet tables; `evidence/mutations.log`)

> The ONE complete run (`C-25`): the orchestrator's full suite on the gated tree at P4 — this
> artifact consumes that result; it does not re-own the run. The implementing session's ONE
> complete settled run over the tree passed **2585 / 2585 with 1 failed** — `1 failed, 2585
> passed in 437.37s` (`evidence/inc001-run.log:1293`) — and the close-out re-collected the suite at
> **2586 tests** on the final tree (`pytest tests --collect-only -q`, 0.59s). Every Layer-0/A/B row
> below was executed by the implementing agent or the close-out coordinator (`human:coordinator`)
> under the batch's standing authorization, named per row.
>
> **The one failure, declared exactly as the backlog states it:** `test_win_clipboard_roundtrip`
> remains an intermittent environmental flake (G-011): it failed on its own clipboard SETUP in
> every B2 gate run — and it fired there again at this batch's full-suite run (the test's own
> message: `SETUP failed — this is the environment, not the code under test`, the PowerShell
> `Set-Clipboard` ExternalException), and the coordinator verified it fails isolated too
> (`1 failed in 4.19s`, `evidence/inc001-run.log:1251-1266`). The BACKLOG has carried it since
> batch B2; it is unrelated to this batch's surface (the increment touched no clipboard seat).

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| the component walk (`models.chain_template`, `models.py:2329-2390`) | the BFS both-directions + seen-set over `depends_on` within the project, open-only, the memoized depth + (depth, board order) sort, the fan-in drop — the isinstance/None/branch cascade; cyclomatic ≥3 | `test_both_directions_a_mid_chain_task_saves_the_whole_component` · `test_fan_in_keeps_the_first_predecessor_and_round_trips_as_a_chain` · `test_a_single_unlinked_task_is_the_degenerate_one_task_template` · `test_none_for_done_archived_and_missing` · `test_component_stays_within_the_task_project` · `test_done_and_archived_neighbours_are_skipped_not_bridged` · `test_titles_and_notes_are_carried_verbatim` | pass (mutation M17 below) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| the component walk | M17: `chain_template` returns None at the top | yes — `6 failed, 1 passed` on `tests/test_template_save.py`: every arm that dereferences the template reddened (both-directions, fan-in + round-trip, the degenerate single task, the within-project boundary, the skipped-not-bridged neighbours, the verbatim titles/notes); the None-cases arm stayed GREEN (its assertions are all `is None`) | `evidence/mutations.log` M17 |
| the save's write conjunct | M16: the `settings["templates"].append(...)` + `save()` in `_on_chain_template_named` → `_ = (name, tasks)` | yes — `2 failed, 2 passed` on `tests/test_template_save_app.py`: the named-save arm and the unlinked-tile arm reddened (the settings entry and the picker listing never happen); the prompt-prefill and esc-cancels arms stayed GREEN | `evidence/mutations.log` M16 |

### UX walkthrough — only if trigger family D fired

Family D did NOT fire this batch — no operator-feedback surface (the batch ships a commissioned
feature, not a report's remedy). The acceptance arms below ARE the automated walkthrough, driven
through the real mechanism; the three evaluation states are declared under the table.

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| `,` on a selected mid-chain tile opens the name prompt, prefilled with the chain's first title | `TaskboardApp` driven with keys through `run_test` (keys `6`, `,`) | a `TextPrompt` screen; the `#f-text` Input holds `Alpha` (not the selected tile's `Beta`) | ✓ |
| type a name + `enter` saves the chain as a template | keys `"Release"`, `enter` | `settings["templates"]` holds the exact entry (Alpha/Beta/Gamma, waits 0/1); the toast renders `Template 'Release' saved — 3 tasks` byte-exact | ✓ |
| `I` after the save lists the new template first | key `I` | the `#template-list` OptionList's first row is `Release — 3 tasks` | ✓ |
| `esc` at the prompt cancels | keys `,`, `escape` | `settings` holds no `templates` key AND the board file's bytes are unchanged | ✓ |
| `,` on an unlinked `○` tile saves a one-task template | keys `,`, `"Solo"`, `enter` on the lone-tile board | `settings["templates"] == [{"name": "Solo", "tasks": [{"title": "Lone task"}]}]`; the toast `Template 'Solo' saved — 1 tasks` | ✓ |

**Mechanism used:** Textual's `run_test` pilot — the criteria driven through the REAL mechanism,
their painted results asserted off the emitted widgets/toasts/rows/file bytes.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — AT-1401's 4 app arms drive the app with keys and read the painted surface + board state |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — the close-out coordinator read the prompt prefill, the toast bytes, the picker row, and the esc byte-identity against the contract's arms (C-32) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — no trigger-D surface this batch; the name prompt is fresh surface the operator has not yet seen (a first-eye candidate, not a gate) |

- **Method:** the arms' fixtures — synthetic boards in `tmp_path` (the house pilot at 100×30)
- **Participants or population:** none — no user session this batch
- **Evidence of the evaluation:** `evidence/inc001-run.log`, `evidence/mutations.log`, `tests/test_template_save.py`, `tests/test_template_save_app.py`, the suite re-collection at 2586
- **Limits:** no user performed the walkthrough; the operator's eye on the new prompt surface remains a standing candidate, not this batch's gate

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-1401 | test | `pytest tests/test_template_save.py tests/test_template_save_app.py -q` | 0 failures; the 11 arms: the both-directions walk · the fan-in drop + round-trip-as-a-chain · the degenerate single task · None for done/archived/missing · the within-project boundary · the skipped-not-bridged neighbours · the verbatim titles/notes · the prompt + prefill · the save + toast + picker listing · the esc byte-identity · the unlinked-tile save | pass | `evidence/inc001-run.log:1065` (11 passed; the full settled run at `:1293`); M16/M17 |
| LLR-1401.1 | test (unit) | the 7 unit arms | the component is the task's own project's open reachable set, each once; the order is topological and deterministic by (depth, board order); the fan-in keeps the FIRST predecessor, the rest dropped; None for missing/done/archived; titles/notes verbatim | pass | `models.py:2329-2390`; M17 |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-1401 | AT-1401 (the dash token in `tests/test_template_save_app.py`'s docstring, line 3) | the app pilot — keys `6`/`,`/name/`enter`/`escape`/`I`, the name prompt, the toast, the `I` picker, the board | the saved `settings["templates"]` entry + the rendered toast bytes + the picker's first row + the board file's byte-identity on esc | repr: `Template 'Release' saved — 3 tasks` · boundary: the unlinked `○` tile saves a one-task template; a mid-chain tile saves the whole component both ways · negative: esc/empty writes nothing (settings AND file bytes); a selection with no open chain toasts `The selection carries no open chain.`; nothing selected toasts `Select a chain tile to save.` | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | key `,` on the chain map (view-scoped) | `action_chain_template_save` ← `keymap.py:143` | yes | AT-1401 (`test_comma_opens_the_name_prompt_prefilled`) | ✓ |
| input | the selection (a mid-chain tile, an unlinked `○` tile, none) | `app.selected_task_id` → `chain_template` | yes | AT-1401 (the prefill arm; the unlinked-tile arm; the refusals in the docstring/packet) | ✓ |
| input | the typed name / esc / empty | `TextPrompt` → `_on_chain_template_named(name, tpl)` | yes | AT-1401 (the save arm; the esc arm) | ✓ |
| input | a selection carrying no open chain | `chain_template` → None branch | yes | the action's toast (declared in the docstring + packet; driven in the session's probes) | ✓ |
| output | the saved settings entry (`{"name", "tasks"}`) | `board.settings["templates"]` after enter | yes | AT-1401 (`:106-110` the exact dict) | ✓ |
| output | the outcome toast | the painted `Toast` | yes | AT-1401 (`_toast_check`, byte-exact; the `1 tasks` degenerate literal) | ✓ |
| output | the picker lists the new template first | the `#template-list` OptionList | yes | AT-1401 (`:116` the first row) | ✓ |
| output | the prompt prefill | the `#f-text` Input's value | yes | AT-1401 (`:85` `Alpha`) | ✓ |
| output | the esc byte-identity | the board file's bytes + the settings dict | yes | AT-1401 (`:131-138`) | ✓ |
| output | the `?` help bullet + the README row | `views.help_usage` · the README keybinding table | yes | the bullet at `views.py:6924`; the census test at `tests/test_keymap.py:404` | ✓ |
| output | NOT an undo step | the absence of any undo entry (declared semantics) | yes | the action's docstring (`app.py:767-777`); no undo key exists in the entry shape | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2575 | 0 | 11 | 2586 | 2586 | 2585 / see the C-25 run | yes |

base = the batch-07 trunk (2575); A = the batch's 11 new nodes — `tests/test_template_save.py` (7) ·
`tests/test_template_save_app.py` (4); the `?` bullet and the README row modified no test. The
close-out re-collected the suite at **2586 tests** on the final tree (`pytest tests --collect-only
-q`, 0.59s); the implementing session's complete settled run passed 2585 with the 1 declared
environmental flake (`evidence/inc001-run.log:1293`, 437.37s); the orchestrator's C-25 close run
owns the final passed count.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| — | — | none — no test gap detected; the M16-M17 battery is all-KILLED with per-node verdicts and named GREEN arms, and the one spec deviation (the README row outside the brief's file list) is forced by a shipped census test, declared in increment-001's packet and `02-review.md`, not a gap | — | — |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| — none — no defect escaped the suite this batch | | | | | |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

`qa-reviewer` — self-executed by the close-out coordinator (`human:coordinator`; the runtime spawned nobody, named per the dev-flow runtime rule):

- [x] Acceptance criteria observable — AT-1401 reads the saved `settings["templates"]` entry + the rendered toast bytes + the picker's first row + the board file's byte-identity through the app pilot (`tests/test_template_save_app.py` · `tests/test_template_save.py`)
- [x] Test cases have explicit Expected — the exact settings dict (absent keys, not nulls); the pinned toast literals (`Template 'Release' saved — 3 tasks` · `Template 'Solo' saved — 1 tasks`); the exact order/wait tuples (`["Alpha", "Beta", "Gamma", "Delta"]` / `[None, 0, 1, 2]`); the round-trip parents `[[], [], ["Alpha"]]`; the prefill `Alpha`; the esc byte-identity
- [x] Edge cases include empty, boundary, invalid, error — the Boundary catalog fields across the contract: ☑ empty (esc/empty name — nothing written, file byte-identical) ☑ boundary (the single-task component; the fan-in keeps its FIRST link; a cross-project link is not traversed; a done/archived neighbour is skipped, not bridged) ☑ invalid — none new ☑ error (nothing selected → the refusal toast; a selection with no open chain → its own toast)
- [x] Regression checklist exists — the reverse census (5 probes), the M16-M17 battery with per-node verdicts and named GREEN arms, the suite re-collection at 2586
- [x] Exit criteria stated — the contract §5.2's criteria, all met (every HLR/LLR a passing AT; every new assertion RED by a recorded mutation or by construction at base; the settled full suite green at 2585 with the one declared environmental flake)
- [x] No real PII / secrets — synthetic boards in `tmp_path` throughout; no operator board data read or written
- [x] **Mode declared** — validation mode: this artifact, Result PASS; every executed result names its executor (the implementing session or the close-out coordinator; the orchestrator for the ONE full C-25 run)
- [x] **Layer B (black-box)** — the story's deliverable observed through the shipped surface with boundary + negative (the Layer B table)
- [x] **Bidirectional surface-reachability** — the matrix above, 11/11 rows ✓
- [x] **No unfilled template** — the verdict fields filled; the artifacts carry no placeholder cells naming nothing
