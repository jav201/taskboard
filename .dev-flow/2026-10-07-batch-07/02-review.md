# Review — taskboard — Batch 2026-10-07-batch-07

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3
- **Out-of-scope findings:** `none`

- **Findings:** `0` blocker · `0` major · `1` minor (F1 — the IFC residual of the T-correction, fixed at the record pass)
- **shall/should check:** ✓ clean — every HLR/LLR statement is `shall`-normative; rationales are informative and modal-free
- **Two-layer (blockers):** ✓ every story has an `AT` (US-1301 → AT-1301) · output reqs name deliverable+observation (the painted picker rows + the rendered toast bytes + the board's tasks/links, observed through the app pilot) · both trace chains complete (US → HLR-1301 → LLR-1301.1/.2 → `test_templates{,_app}.py`; US → AT-1301 → the outcomes through the shipped surface) · ATs are genuinely black-box (keys through `run_test`; the `board.tasks`/`depends_on` reads are the observed surface state; no internal symbol is asserted beyond the shipped modal class)
- **Census (change-first):** done — best-effort + gate-confirmed (the increment gate carries the five reverse-census probes)
- **Security:** ✓ no findings — the only new user-text surfaces are the picker's rows (each a `Text` piece, S1 — `modals.py:936`'s docstring names it) and the template-carried titles/notes flowing into `Task.title`/`Task.notes` (user text into the shipped markup seams; every toast ships `markup=False`); the hostile-title families of the suite stayed green
- **Evidence checklists (architect / qa / security):** `core` mode — the coordinator's lens covered the contract; the increment packet carries the evidence tables

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| F1 | coordinator | minor | the live contract's IFC block | LED-2026-10-07-batch-07.2's correction swept the HLR/LLR statements but MISSED the IFC node — `01-requirements.md:145` still read `+ keymap T` after the correction, a surviving positive ref of the superseded key (same writing defect as the original: text frozen before the seat was checked) | fold into the same correction; re-run the supersession grep over the whole batch dir | **fixed** — `:145` now reads `keymap I`; the packet's V-3 table records the before/after |

**TWO declared observations** (not findings — writing/process notes the gate records, both folded):

| # | Observation | Folded where |
|---|-------------|--------------|
| (a) | **The T-key writing defect — the batch's hero lesson.** The contract pinned `T` as the picker key without checking the seat: `T` ships `project_pin_toggle` (`keymap.py:86`), pinned by `tests/test_focus.py:46`/`:151` and `tests/test_markup_sites.py:267`. The defect is the SAME CLASS as batch-06's marker glyphs (contract text written against an imagined blank slate) — but this time it was caught by the implementing AGENT's stop gate BEFORE any code was written: the session named the conflict, named the two ways it could only redden the suite, and stopped. The contract was corrected to `I` under LED-2026-10-07-batch-07.2 before the first edit; every shipped seat stayed untouched. The stop-and-name gate working as designed is the batch's central lesson — carried into the close's lessons and the backlog's control candidate. | `01-requirements-ledger.md` LED .2 · increment-001's packet §1 + Correction population · the close's lessons |
| (b) | **The README row landed outside the brief's file list.** The brief closed its file list with "Nothing else", but the shipped census test `test_keymap.py:404` (`test_the_readme_keybinding_table_matches_the_seat`) enforces every bound key documented — the keymap line reddened the census until the README row landed. Forced by a shipped test, declared in the session's report, accepted: the README row (`README.md:135`) is part of the increment's record as a `doc` change. | increment-001's packet §2 + Instrument RED-proof · `evidence/inc001b-run.log` §5 |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a finding nobody raised. Write your own rows in the table above.

```text
| *(example)* F1 | architect | blocker / major / minor | | | | open / fixed |
```

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

✓ clean — HLR-1301 and LLR-1301.1/.2 are `shall`-normative throughout; the rationales and the
boundary-catalog notes are informative and modal-free. (The `?`-help clause of LLR-1301.2 —
"the `?` help names the key and documents that v1 edits templates in the board JSON" — is a
deliverable obligation on shipped text, verified at `views.py:6837`, not a modal inside the
normative statement.)

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-1301 / HLR-1301 / LLR-1301.1/.2 | yes (AT-1301 — the dash token in `tests/test_templates_app.py`'s docstring) | yes (the painted picker rows + the rendered toast bytes + the board's tasks/links, observed through the app pilot and the byte-exact `_toast_check`) | yes (US-1301 → HLR-1301 → LLR-1301.1/.2 → `test_templates.py` · `test_templates_app.py`) | yes (keys through `run_test`; the `board.tasks`/`depends_on`/toast reads are the observed surface state) | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

`taskboard/models.py` · `taskboard/app.py` · `taskboard/modals.py` · `taskboard/keymap.py` (edited)
× `taskboard/views.py` · `README.md` (edited, doc) × `tests/test_templates.py` ·
`tests/test_templates_app.py` (new): families run — the frozen-module family is clean (no frozen
interface's signature moved: `present_project_id`, the milestones undo pattern, `help_usage`'s
(mode) → sections signature, the LinkPicker chrome, `BOARD_ACTIONS`'s listing shape, and `T`'s
seat at `keymap.py:86` are pre-batch bytes — the pin arms stay green); the AST-composition family
is clean (all new symbols, no existing composition rewritten); the behavioral-placeholder family
is clean (no placeholder shipped — the picker is the shipped LinkPicker chrome composed for real);
the structural/placement family is clean (the correction population was enumerated before the
first site was edited; the residual IFC ref is F1, fixed). Reservations: none. The increment gate
carries the five reverse-census probes.

### Security review summary
✓ no findings — `human:coordinator` self-executed the security lens (trigger family C; the runtime
spawned nobody). The new user-text surfaces: the picker rows (each built as a `Text` piece, S1 —
`modals.py:936` names the law in the docstring) and the template-carried titles/notes flowing into
`Task.title`/`Task.notes` — the shipped user-text seams with S1 escaping; every toast ships
`markup=False`; the suite's hostile-title families stayed green across the full run (2575). The
picker/unlink/present paths this feature composes are the shipped, previously-reviewed seats.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.

`core` mode — self-executed by the close-out coordinator (`human:coordinator`): the contract lens
(shall/should · two-layer · supersession · security above) is complete; the per-increment evidence
tables (instruments · mutations · emitted forms · evidence files with sha256 · load-bearing
emptiness · reverse census · correction population) live in increment-001's packet; the validation
evidence checklist is in `04-validation.md`. Reviewer: `human:coordinator`.
