# Review — taskboard — Batch 2026-10-07-batch-09

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3
- **Out-of-scope findings:** `none`

- **Findings:** `0` blocker · `0` major · `0` minor — no findings raised; ONE declared observation below (folded into the record)
- **shall/should check:** ✓ clean — HLR-1501 and LLR-1501.1 are `shall`-normative throughout; the rationale/boundary notes are informative and modal-free
- **Two-layer (blockers):** ✓ every story has an `AT` (US-1501 → AT-1501) · output reqs name deliverable+observation (the saved `settings["templates"]` entry + the rendered toast bytes + the picker rows + the board file's byte-identity, observed through the app pilot) · both trace chains complete (US-1501 → HLR-1501 → LLR-1501.1 → `test_template_new.py`; US-1501 → AT-1501 → the outcomes through the shipped surface) · ATs are genuinely black-box (keys through `run_test`; the `board.settings`/toast/picker/file reads are the observed surface state; no internal symbol is asserted beyond the shipped `TemplatePicker`/`TemplateEditor` classes)
- **Census (change-first):** done — best-effort + gate-confirmed (the increment gate carries the five reverse-census probes)
- **Security:** ✓ no findings — the only new user-text surfaces are the typed name and task lines flowing into `settings["templates"]` and the toasts (every toast ships `markup=False`; the editor never paints the name as markup — its docstring says so); the hostile-title families of the suite stayed green
- **Evidence checklists (architect / qa / security):** `core` mode — the coordinator's lens covered the contract; the increment packet carries the evidence tables

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| — none — no finding this batch | | | | | | |

**ONE declared observation** (not a finding — a process note the gate records, folded):

| # | Observation | Folded where |
|---|-------------|--------------|
| (a) | **The FIRST-row law rippled into five pre-existing tests — the named cost of the contract change.** The contract's "`New template...` is the FIRST option" moved the SHARED `I` picker's listing shape and first-highlight; the pre-batch-09 tests pinned the old shape, and the implementing session's full-suite run reddened exactly 5 arms. The session STOPPED and named them (honoring the brief's "Nothing else" cap) instead of quietly editing them; the coordinator then updated the 5 fixtures — law-driven, enumerated before the first edit, assertions NOT weakened (same outcomes, new shape): `tests/test_templates_app.py` ×4 (the listing arms gain the leading row; the `enter` arms gain a `down` past it) and `tests/test_template_save_app.py` ×1 (the saved template now lists at index 1). This ripple is recorded as the cost of the contract change, named — the next contract that reshapes a shared pinned surface should carry its correction population in the brief. | increment-001's packet §1/§2/§4 Correction population · `evidence/mutations.log` |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a finding nobody raised. Write your own rows in the table above.

```text
| *(example)* F1 | architect | blocker / major / minor | | | | open / fixed |
```

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

✓ clean — HLR-1501 and LLR-1501.1 are `shall`-normative throughout; the rationales and the
boundary-catalog notes are informative and modal-free.

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-1501 / HLR-1501 / LLR-1501.1 | yes (AT-1501 — the dash token in `tests/test_template_new.py`'s docstring, line 4) | yes (the saved `settings["templates"]` entry + the rendered toast bytes + the picker rows + the round-trip `depends_on` + the board file's byte-identity, observed through the app pilot and the byte-exact `_toast_check`) | yes (US-1501 → HLR-1501 → LLR-1501.1 → `tests/test_template_new.py`) | yes (keys `I`/`enter`/`down`/`escape` through `run_test`; the `board.settings`/toast/picker/file reads are the observed surface state) | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

`taskboard/modals.py` · `taskboard/app.py` (edited) × `taskboard/views.py` (edited, doc) ×
`tests/test_template_new.py` (new) × `tests/test_templates_app.py` ·
`tests/test_template_save_app.py` (edited, the law-driven fixture updates): families run — the
frozen-module family is clean (the `templates()` store read, `_read_template`'s lenient shape, the
batch-08 settings/save seam, the `TextPrompt`/`ProjectModal` chrome, and `help_usage`'s signature
are pre-batch bytes; the one interface move — `TemplatePicker`'s return type — has a single caller,
the route this increment owns); the AST-composition family is clean (the editor is a new modal
composing the shipped `VerticalScroll`/`Input`/`TextArea`/`Button` seats; the picker row composes
the house `__new__` reserved-id pattern the `L` link picker already ships); the
behavioral-placeholder family is clean (no placeholder shipped — the row, the editor, the route,
and the save are the real seats); the structural/placement family is clean (the picker row and the
editor landed in their owning module; the `?` bullet at its documented seat). Reservations: none.
The increment gate carries the five reverse-census probes.

### Security review summary
✓ no findings — `human:coordinator` self-executed the security lens (trigger family C; the runtime
spawned nobody). The new user-text surfaces: the typed template name and the task lines flowing
into `settings["templates"]` and the save/refusal toasts (every toast ships `markup=False`; the
editor never paints the name as markup — its docstring states so, S1) and the round-trip titles —
the batch-07/08-reviewed seams with S1 escaping. The editor composes the shipped, previously-reviewed
widget seats; the hostile-title families of the suite stayed green across the recorded run.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.

`core` mode — self-executed by the close-out coordinator (`human:coordinator`): the contract lens
(shall/should · two-layer · supersession · security above) is complete; the per-increment evidence
tables (instruments · mutations · emitted forms · evidence files with sha256 · load-bearing
emptiness · reverse census · correction population) live in increment-001's packet; the validation
evidence checklist is in `04-validation.md`. Reviewer: `human:coordinator`.
