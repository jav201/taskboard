# Validation — taskboard — Batch 2026-10-07-batch-09

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
- **Layer 0:** `0` unit(s) met the criterion — no new module-level function this batch; the new logic is the app callback `_on_template_authored`, covered white-box (Layer A) · `1` named reddening mutation over the chain conjunct (`entry["wait"] = i - 1` → `pass`, M18) — KILLED
- **Requirements:** `1`/`1` pass (HLR-1501 via AT-1501's 6 arms; LLR-1501.1 below) · `0` blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — nothing superseded this batch (the V-3 inspection reads `none`)
- **Test ledger:** ✓ reconciles (`base − D + A = post` → `2592 = 2586 − 0 + 6`, measured by collect-only)
- **Evidence checklist (qa-reviewer):** `human:coordinator` — self-executed by the close-out coordinator · `10` of `10` rows ✓ with evidence (increment-001's packet tables; `evidence/mutations.log`; `evidence/inc001-run.log`)

> The ONE complete run (`C-25`): the orchestrator's full suite on the gated tree at P4 — this
> artifact consumes that result; it does not re-own the run. The implementing session's ONE complete
> run over the tree reported **`5 failed, 2587 passed in 455.47s`** (`evidence/inc001-run.log:483`)
> — the 5 failures ALL pre-existing batch-07/08 arms pinning the old picker shape, named in the
> session's STOP report (`:529-537`) and closed by the coordinator's five law-driven fixture updates
> (`evidence/mutations.log`), after which the 15 template arms across the three files stand green.
> The close-out re-collected the suite at **2592 tests** on the final tree (`pytest tests
> --collect-only -q`, 0.62s — the arithmetic cross-check: the session's run collected 2587 + 5 =
> 2592). Every Layer-A/B row below was executed by the implementing agent or the close-out
> coordinator (`human:coordinator`) under the batch's standing authorization, named per row.
>
> **The G-011 declaration** (exactly as the backlog states it): `test_win_clipboard_roundtrip`
> remains an intermittent environmental flake (G-011) — it failed on its own clipboard SETUP in
> every B2 gate run (the test's own message: `SETUP failed — this is the environment, not the code
> under test`, the PowerShell `Set-Clipboard` ExternalException), and the BACKLOG has declared it
> since batch B2. It did NOT fire in this batch's recorded full-suite run (`5 failed, 2587 passed`
> names five picker-shape arms, no clipboard arm); it is expected in any full run and is unrelated
> to this batch's surface (the increment touched no clipboard seat).

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| — none this batch — the increment's new logic is the app callback `_on_template_authored` (`app.py:814-843`), not a module-level function; `models` gained nothing | the cyclomatic/unit criterion applies to no new function | — | n/a (declared in increment-001 §4; the callback is covered white-box below and by M18) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| the chain conjunct of `_on_template_authored` | M18: `entry["wait"] = i - 1` → `pass` (`app.py:835`) | yes — `1 failed, 5 passed` on `tests/test_template_new.py`: the round-trip chain arm reddened (the `wait` indices after an `I` insert); the picker-first, all-empty, name-without-tasks, esc, and single-task arms stayed GREEN (named) | `evidence/mutations.log` M18 |

### UX walkthrough — only if trigger family D fired

Family D did NOT fire this batch — no operator-feedback surface (the batch ships a commissioned
feature, not a report's remedy). The acceptance arms below ARE the automated walkthrough, driven
through the real mechanism; the three evaluation states are declared under the table.

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| `I` opens the picker with `New template...` first | `TaskboardApp` driven with keys through `run_test` (key `I`) | the `#template-list` OptionList's rows are exactly `New template...`, `Deploy — 2 tasks`, `Simple chain — 3 tasks`, `Bugfix — 3 tasks` | ✓ |
| `enter` on the authoring row opens the editor | keys `I`, `enter` | a `TemplateEditor` screen: the `#f-name` Input and the `#f-tasks` TextArea | ✓ |
| a name + multi-line tasks (blanks between) saves the linear chain | the editor widgets set, Save pressed | `settings["templates"]` holds the exact entry (Design/Build/Ship, waits 0/1); the toast renders `Template 'Launch' saved — 3 tasks` byte-exact | ✓ |
| `I` after the save lists the template and reproduces the chain | keys `I`, `down`, `enter` | the second row is `Launch — 3 tasks`; the three created tasks' `depends_on` are `[]`, `[Design]`, `[Build]` | ✓ |
| an all-empty edit saves nothing | the editor widgets set blank, Save pressed | `settings` holds no `templates` key AND the board file's bytes are unchanged; the refusal toast names the why | ✓ |
| a name with zero task lines saves nothing | name set, tasks blank, Save pressed | `settings` holds no `templates` key | ✓ |
| `esc` cancels | name typed, key `escape` | `settings` holds no `templates` key AND the board file's bytes are unchanged | ✓ |
| a single task line is a valid template | one line, Save pressed | `settings["templates"] == [{"name": "Solo", "tasks": [{"title": "One task"}]}]` — no `wait` key; the toast `Template 'Solo' saved — 1 tasks` | ✓ |

**Mechanism used:** Textual's `run_test` pilot — the criteria driven through the REAL mechanism,
their painted results asserted off the emitted widgets/toasts/rows/file bytes.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — AT-1501's 6 arms drive the app with keys and read the painted surface + board state |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — the close-out coordinator read the picker rows, the editor composition, the toast bytes, and the all-empty/esc byte-identity against the contract's arms (C-32) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — no trigger-D surface this batch; the editor is fresh surface the operator has not yet seen (a first-eye candidate, not a gate) |

- **Method:** the arms' fixtures — synthetic boards in `tmp_path` (the house pilot at 100×30)
- **Participants or population:** none — no user session this batch
- **Evidence of the evaluation:** `evidence/inc001-run.log`, `evidence/mutations.log`, `tests/test_template_new.py`, `tests/test_templates_app.py`, `tests/test_template_save_app.py`, the suite re-collection at 2592
- **Limits:** no user performed the walkthrough; the operator's eye on the new editor surface remains a standing candidate, not this batch's gate

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-1501 | test | `pytest tests/test_template_new.py -q` | 0 failures; the 6 arms: the picker lists `New template...` first · the editor saves a linear chain with blank lines skipped (the exact `wait` indices after an `I` round-trip) · the toast equals the pinned literal · all-empty saves nothing (settings AND file bytes) · a name with no tasks saves nothing · esc writes nothing · a single-task line works | pass | `evidence/inc001-run.log:440` (6 passed; the full run at `:483`); M18 |
| LLR-1501.1 | test (integration) | the 6 arms through the app pilot | the editor is the lightest house-consistent composition (VerticalScroll modal-box + Input + TextArea + buttons, one `DEFAULT_CSS` rule, no `.tcss`); the emitted `wait` chain is linear 0←1←2… through the same validation seam the JSON read uses; the save rides the batch-08 settings/toast contract verbatim | pass | `modals.py:987-1031` · `app.py:814-843`; M18 |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-1501 | AT-1501 (the dash token in `tests/test_template_new.py`'s docstring, line 4) | the app pilot — keys `I`/`enter`/`down`/`escape`, the editor, the toast, the `I` picker, the board | the saved `settings["templates"]` entry + the rendered toast bytes + the picker's rows + the round-trip `depends_on` + the board file's byte-identity on the empty/esc paths | repr: `Template 'Launch' saved — 3 tasks` · boundary: a single task line saves a one-task template (`1 tasks` pinned literal); blank lines between tasks are skipped, lines trimmed · negative: an all-empty edit and a name-without-tasks save nothing (settings AND file bytes) with the one-line refusal toast; esc writes nothing | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | key `I` on the board | `action_templates` → the `TemplatePicker` | yes | AT-1501 (`test_picker_lists_new_template_first`) | ✓ |
| input | `enter` on the authoring row | the `__new__` option → `("new", "")` → the `TemplateEditor` | yes | AT-1501 (`_open_editor` + the round-trip arm) | ✓ |
| input | the typed name + the multi-line tasks (blanks between) | the `#f-name` Input + `#f-tasks` TextArea → `_on_template_authored` | yes | AT-1501 (the save arm) | ✓ |
| input | an all-empty edit / a name with zero tasks | the same widgets, blank | yes | AT-1501 (the two refusal arms) | ✓ |
| input | `esc` at the editor | `action_cancel` → None | yes | AT-1501 (`test_escape_writes_nothing`) | ✓ |
| output | the saved settings entry (`{"name", "tasks"}`) | `board.settings["templates"]` after Save | yes | AT-1501 (`:102-106` the exact dict) | ✓ |
| output | the outcome toast | the painted `Toast` | yes | AT-1501 (`_toast_check`, byte-exact; the `1 tasks` degenerate literal) | ✓ |
| output | the picker lists the new template after the authoring row | the `#template-list` OptionList | yes | AT-1501 (`:114` the second row) | ✓ |
| output | the round-trip chain | the created tasks' `depends_on` | yes | AT-1501 (`:117-121`) | ✓ |
| output | the empty/esc byte-identity | the board file's bytes + the settings dict | yes | AT-1501 (`:136-137`, `:168-169`) | ✓ |
| output | the `?` help bullets | `views.help_usage` | yes | the bullets at `views.py:6837-6838`; the shipped `test_english.py`/`test_help_clip.py` censuses green | ✓ |
| output | NOT an undo step | the absence of any undo entry (declared semantics) | yes | the callback's docstring (`app.py:814-822`); no undo key exists in the entry shape | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2586 | 0 | 6 | 2592 | 2592 | 2587+5 in the session's one run (the 5 closed by the coordinator's updates) / see the C-25 run | yes |

base = the batch-08 trunk (2586); A = the batch's 6 new nodes — `tests/test_template_new.py`;
the coordinator's five law-driven fixture updates deleted/added NO nodes (the `?` bullet modified
no test). The close-out re-collected the suite at **2592 tests** on the final tree (`pytest tests
--collect-only -q`, 0.62s); the implementing session's complete run collected the same 2592
(`5 failed + 2587 passed`, `evidence/inc001-run.log:483`); the orchestrator's C-25 close run owns
the final passed count.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| — | — | none — no test gap detected; the M18 battery is KILLED with per-node verdicts and named GREEN arms, and the five pre-existing reds were the contract's own ripple, closed law-driven (not weakened) and named in increment-001's packet and `02-review.md` | — | — |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| — none — no defect escaped the suite this batch | | | | | |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

`qa-reviewer` — self-executed by the close-out coordinator (`human:coordinator`; the runtime spawned nobody, named per the dev-flow runtime rule):

- [x] Acceptance criteria observable — AT-1501 reads the saved `settings["templates"]` entry + the rendered toast bytes + the picker rows + the round-trip `depends_on` + the board file's byte-identity through the app pilot (`tests/test_template_new.py`)
- [x] Test cases have explicit Expected — the exact settings dict (the linear waits 0/1); the pinned toast literals (`Template 'Launch' saved — 3 tasks` · `Template 'Solo' saved — 1 tasks`); the refusal toast byte-exact; the round-trip `depends_on` (`[]`, `[Design]`, `[Build]`); the picker row lists (the authoring row FIRST); the empty/esc byte-identity
- [x] Edge cases include empty, boundary, invalid, error — the Boundary catalog fields across the contract: ☑ empty (all-empty edit / name with zero tasks — nothing written, file byte-identical) ☑ boundary (a single task line; blank lines between tasks; lines trimmed) ☑ invalid — none new ☑ error — none new (the one-line refusal is information, not an error path)
- [x] Regression checklist exists — the reverse census (5 probes), the M18 battery with per-node verdicts and named GREEN arms, the five law-driven fixture updates (enumerated before edit, 0 left), the suite re-collection at 2592
- [x] Exit criteria stated — the contract §5.2's criteria, all met (every HLR/LLR a passing AT; every new assertion RED by a recorded mutation or by construction at base; the suite at 2592 collected with the 15 template arms green after the coordinator's updates)
- [x] No real PII / secrets — synthetic boards in `tmp_path` throughout; no operator board data read or written
- [x] **Mode declared** — validation mode: this artifact, Result PASS; every executed result names its executor (the implementing session or the close-out coordinator; the orchestrator for the ONE full C-25 run)
- [x] **Layer B (black-box)** — the story's deliverable observed through the shipped surface with boundary + negative (the Layer B table)
- [x] **Bidirectional surface-reachability** — the matrix above, 12/12 rows ✓
- [x] **No unfilled template** — the verdict fields filled; the artifacts carry no placeholder cells naming nothing
