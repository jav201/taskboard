# Review — taskboard — Batch 2026-10-07-batch-08

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3
- **Out-of-scope findings:** `none`

- **Findings:** `0` blocker · `0` major · `0` minor — no findings raised; TWO declared observations below (both folded into the record)
- **shall/should check:** ✓ clean — HLR-1401 and LLR-1401.1 are `shall`-normative throughout; the rationale/boundary notes are informative and modal-free
- **Two-layer (blockers):** ✓ every story has an `AT` (US-1401 → AT-1401) · output reqs name deliverable+observation (the saved `settings["templates"]` entry + the rendered toast bytes + the picker's first row, observed through the app pilot) · both trace chains complete (US-1401 → HLR-1401 → LLR-1401.1 → `test_template_save{,_app}.py`; US-1401 → AT-1401 → the outcomes through the shipped surface) · ATs are genuinely black-box (keys through `run_test`; the `board.settings`/toast/picker reads are the observed surface state; no internal symbol is asserted beyond the shipped `TextPrompt`/`TemplatePicker` classes)
- **Census (change-first):** done — best-effort + gate-confirmed (the increment gate carries the five reverse-census probes)
- **Security:** ✓ no findings — the only new user-text surface is the typed name flowing into `settings["templates"]` and the toast (both `markup=False`; the toast is a notify body, not markup); the template-carried titles/notes are the batch-07-reviewed seams; the hostile-title families of the suite stayed green
- **Evidence checklists (architect / qa / security):** `core` mode — the coordinator's lens covered the contract; the increment packet carries the evidence tables

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| — none — no finding this batch | | | | | | |

**TWO declared observations** (not findings — writing/process notes the gate records, both folded):

| # | Observation | Folded where |
|---|-------------|--------------|
| (a) | **The golden-footer vs keybar-discoverability trade.** The `,` key ships view-scoped on the chain map, but the chainmap frame's own footer key-hint row was deliberately NOT edited: it is byte-golden in the C-2b frames (`test_TC_801`/`test_TC_802`), and touching it would have reopened the byte-exact oracle the operator re-verified at `762d18c`. The key's discoverability rides the docked keybar (re-derived from the keymap seat) and the `?` bullet (`views.py:6924`). A declared notice in the increment packet §1/§5 and the close's lessons — the first batch where golden frames actively vetoed an in-frame hint; if it recurs it becomes the standing rule "new chainmap keys document at the keybar/`?` seats only". | increment-001's packet §1 · §5 · the close's lessons |
| (b) | **The README row landed outside the brief's file list.** The brief closed its file set with "Nothing else", but the shipped census test `test_keymap.py:404` (`test_the_readme_keybinding_table_matches_the_seat`) enforces every bound key documented — the session's first full-suite attempt reddened on its own keymap change (``, (Save chain tpl) is bound but the README never mentions it``), and the `comma` row (`README.md:136`) followed. Forced by a shipped test, declared in the session's report, accepted: the row is a `doc` change outside the source budget — the same shape batch-07 recorded for its `I` row. | increment-001's packet §2 + Instrument RED-proof · `evidence/inc001-run.log` |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a finding nobody raised. Write your own rows in the table above.

```text
| *(example)* F1 | architect | blocker / major / minor | | | | open / fixed |
```

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

✓ clean — HLR-1401 and LLR-1401.1 are `shall`-normative throughout; the rationales and the
boundary-catalog notes are informative and modal-free. (The fan-in clause of HLR-1401 — "a task
with several predecessors keeps the FIRST and the rest are dropped, declared" — is a normative
shaping rule with its declaration built in, not a modal.)

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-1401 / HLR-1401 / LLR-1401.1 | yes (AT-1401 — the dash token in `tests/test_template_save_app.py`'s docstring, line 3) | yes (the saved `settings["templates"]` entry + the rendered toast bytes + the picker's first row + the board file's byte-identity on esc, observed through the app pilot and the byte-exact `_toast_check`) | yes (US-1401 → HLR-1401 → LLR-1401.1 → `tests/test_template_save.py` · `tests/test_template_save_app.py`) | yes (keys `6`/`,`/name/`enter`/`escape`/`I` through `run_test`; the `board.settings`/toast/picker/file reads are the observed surface state) | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

`taskboard/models.py` · `taskboard/app.py` · `taskboard/keymap.py` (edited) ×
`taskboard/views.py` · `README.md` (edited, doc) × `tests/test_template_save.py` ·
`tests/test_template_save_app.py` (new): families run — the frozen-module family is clean (no frozen
interface's signature moved: `help_usage`'s (mode) → sections signature, the `TextPrompt` chrome,
the `templates()` store shape, `is_open`/`_ids`/`_live`, and the batch-07 insert seats are pre-batch
bytes); the AST-composition family is clean (all new symbols, no existing composition rewritten —
`chain_template` composes the shipped `Template`/`TemplateTask` dataclasses and `_ids`/`_live`
helpers); the behavioral-placeholder family is clean (no placeholder shipped — the walk, the
action, and the key are the real seats); the structural/placement family is clean (the `,` seat
was verified FREE before the write — the brief's discipline grep, re-run at this record). The
in-frame chainmap footer was deliberately left byte-untouched (observation (a)). Reservations:
none. The increment gate carries the five reverse-census probes.

### Security review summary
✓ no findings — `human:coordinator` self-executed the security lens (trigger family C; the runtime
spawned nobody). The new user-text surfaces: the typed template name flowing into
`settings["templates"]` and the save/refusal toasts (every toast ships `markup=False`; the name is
board data, displayed through the shipped notify seam) and the template-carried titles/notes — the
batch-07-reviewed seams with S1 escaping. The prompt/picker/notify paths this feature composes are
the shipped, previously-reviewed seats; the hostile-title families of the suite stayed green across
the full run (2585 passed + the declared G-011 flake).

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.

`core` mode — self-executed by the close-out coordinator (`human:coordinator`): the contract lens
(shall/should · two-layer · supersession · security above) is complete; the per-increment evidence
tables (instruments · mutations · emitted forms · evidence files with sha256 · load-bearing
emptiness · reverse census · correction population) live in increment-001's packet; the validation
evidence checklist is in `04-validation.md`. Reviewer: `human:coordinator`.
