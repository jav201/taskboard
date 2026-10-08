# Increment 001 — HLR-1501 · `Author a template from scratch (templates v3)`

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`. The normative RULES below are
> language-independent.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/increment-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-07-batch-09/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-09` |
| Increment | `001` (the whole batch — one increment, one brief) |
| Lane (if the batch forked) | `none` — one implementing session owned the tree; the MAIN checkout |
| Requirement(s) | `HLR-1501` (+ `LLR-1501.1` the editor modal and the linear-chain shape) |
| Acceptance | `AT-1501` — 6 arms, all green (`tests/test_template_new.py`, the docstring home of the `AT-1501` dash token, line 4: `HLR-1501 / LLR-1501.1 · AT-1501.`) |
| Agent | `software-dev` — DeepSeek V4 Pro (one shipping session under the coordinator's brief; `evidence/inc001-brief.md`) |
| Date | `2026-10-07/08` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

`I` → the picker now opens with a leading **`New template...`** row → `enter` opens a small editor: ONE
name field and ONE multi-line tasks field. Type a name, type the tasks one per line, `Save` (or the
Save button) — the template exists from then on: it appends to the board's own
`settings["templates"]` as a **linear chain** (task i waits on i−1, task 0 on nothing; lines trimmed,
blank lines skipped), the board is saved, and the pinned toast renders
`Template '<name>' saved — <N> tasks` (`markup=False`, the batch-08 literal verbatim). The new
template lists in the `I` picker immediately (after the authoring row) and inserts with `I` like any
other, reproducing the chain. An all-empty edit (blank name or zero task lines) saves NOTHING and
toasts one line saying why; `esc` cancels with nothing written. Authoring is **NOT an undo step** —
it writes settings, not tasks (the batch-08 rule, docstring-pinned at `app.py:815-822`). Notes stay
JSON-only at this version — the `?` bullet says so (`views.py:6837-6838`).

Mechanism, by seat:

- **The picker row** — `taskboard/modals.py:933-985` (`TemplatePicker`): the list gains a leading
  `New template...` option carrying the **reserved id `__new__`** (`modals.py:967`) — the house's
  existing reserved-id convention, the same id the `L` link picker's "+ create a new task" row
  already ships (`modals.py:872`, `:922`). The row is NOT a template: the selection handler
  recognises the id instead of indexing into `_templates` (`modals.py:978-981`). The picker's return
  type changed `ModalScreen[str | None]` → `ModalScreen[tuple[str, str] | None]` (the house
  "kind tag" convention): a template row returns `("insert", name)`, the authoring row returns
  `("new", "")`, `esc` returns None; template rows now carry their index as the option id
  (`modals.py:968-971`).
- **The editor modal** — `taskboard/modals.py:987-1031` (`TemplateEditor`, new): a thin collector —
  `VerticalScroll(id="modal-box", classes="modal")` + `Input(#f-name)` + `TextArea(#f-tasks)` +
  `Horizontal(classes="modal-buttons")` Save/Cancel, one `DEFAULT_CSS` rule giving the TextArea
  `height: 8` and border/background (`modals.py:998-1000`). This is the lightest house-consistent
  composition: `TextArea` already ships in the app (`TaskModal` uses it for notes), the
  `.modal`/`modal-box` shell is exactly `ProjectModal`/`TextPrompt`'s, and no `.tcss` was touched
  (the session's tcss census: `taskboard.tcss` greps at `evidence/inc001-run.log:20-47`). `_save`
  dismisses `{"name", "tasks"}` — the name stripped, the tasks as stripped non-blank lines in order;
  the modal writes nothing and toasts nothing (the caller owns the chain shape and the save).
- **The wiring** — `taskboard/app.py`: `action_templates`'s docstring names the route
  (`app.py:724-733`); `_on_template_picked` routes `("new", "")` to the editor
  (`app.py:741-746`); `_on_template_authored` (`app.py:814-843`) validates (blank name OR zero task
  lines → the one-line refusal toast, nothing written), builds the linear chain
  (`entry["wait"] = i - 1` at **`app.py:835`**), appends through the SAME
  `settings.setdefault("templates", []).append(...)` seam the batch-08 save uses, `save()`, and
  toasts the pinned literal. The `TemplateEditor` import joined the modals import line at
  `app.py:31`.
- **The doc seat** — the `?` kanban bullet at `views.py:6837-6838`
  (`I inserts · New template... authors` / `notes stay JSON-only at this version`), split out of the
  old single line; both stay ≤44 cells and English (the shipped `test_english.py` census stayed
  green — `evidence/inc001-run.log:513-544`).

**The five law-driven fixture updates (coordinator, after the implementing session's STOP-and-name).**
The contract's "`New template...` is the FIRST option" changed the SHARED `I` picker's shape; the
pre-batch-09 tests pin the old shape. The shipping session's full-suite run reddened exactly 5
pre-existing arms, it STOPPED and named them (did NOT touch them — the brief's "Nothing else" cap;
`evidence/inc001-run.log:529-537`), and the coordinator then updated the 5 fixtures as the
law-driven record: `tests/test_templates_app.py` ×4 (the two listing arms gain the leading row, the
two `enter`-navigation arms gain a `down` past the authoring row) and
`tests/test_template_save_app.py` ×1 (the saved template now lists at index 1). Assertions NOT
weakened — same outcomes, new shape. Enumerated in §4 Correction population.

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | HLR-1501 · LLR-1501.1 | the leading `New template...` row + reserved id `__new__` in `TemplatePicker` (`:933-985`, row at `:967`, handler at `:978`); the new `TemplateEditor` collector (`:987-1031`); +64/−10 lines |
| `taskboard/app.py` | source | HLR-1501 · LLR-1501.1 | `_on_template_picked` routes `("new", "")` to the editor (`:741-746`); `_on_template_authored` — the validation, the linear wait chain (`:814-843`, the `entry["wait"] = i - 1` at `:835`); the `TemplateEditor` import (`:31`); +44/−9 lines |
| `taskboard/views.py` | doc | | the `?` kanban bullet (`:6837-6838`): `I inserts · New template... authors` + `notes stay JSON-only at this version` — one help change shipped in code (the notice below) |
| `tests/test_template_new.py` | test | HLR-1501 · LLR-1501.1 — AT-1501's docstring home | new — 6 arms |
| `tests/test_templates_app.py` | test | HLR-1501 (the FIRST-row law) | the coordinator's law-driven fixture update ×4 arms — the listing arms gain the leading row, the `enter` arms gain `down` past it; assertions not weakened |
| `tests/test_template_save_app.py` | test | HLR-1501 (the FIRST-row law) | the coordinator's law-driven fixture update ×1 arm — the saved template now lists at index 1 |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 3 (uncapped — 1 new + 2 updated) |
| Doc files | 1 (outside the count) |

- ⚠ **`views.py` counted as `doc`, not source:** its entire change is the `?`-help bullet pair — the
  same reading batch-2026-10-07-batch-07 and batch-2026-10-07-batch-08 recorded for their help
  bullets. This is the THIRD consecutive batch reading a help-only `.py` change as `doc` — per the
  notice convention the recurrence is now named: either it becomes the standing rule ("a help-only
  `.py` change is `doc`, outside the source budget") or the operator retires it at the next aperture.
- ⚠ **No 4-source-file pressure:** 2 source files — two under the cap — the picker/editor
  (`modals.py`), the route/save (`app.py`); the help bullet rides as `doc`.

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_template_new.py -q   # 6 passed
env -u NO_COLOR PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests --collect-only -q         # 2592 collected
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (cyclomatic ≥3, or crosses a declared module boundary) | `core` · `full` | none — no new module-level function met the unit criterion this batch: the new logic is the app callback `_on_template_authored` (covered white-box below, mutation-proven by M18); `models` gained nothing | 0 (declared) |
| **A · white-box** ↔ LLR-1501.1/HLR-1501 (the editor + the linear-chain save: validation → the `wait = i−1` chain → the settings append + save → the pinned toast → the picker listing) | `core` · `full` | `test_editor_saves_a_linear_chain_and_round_trips` · `test_all_empty_saves_nothing` · `test_name_without_tasks_saves_nothing` · `test_single_task_line_works` | 4 passed (mutation-proven — M18) |
| **B · black-box** `AT-1501` ↔ US-1501, through the shipped surface | `core` · `full` | the 6 arms of `tests/test_template_new.py` — keys `I`/`enter`/`down`/`escape` + the painted editor widgets through `run_test` at the house pilot (100×30), the rendered toast bytes, `board.settings` + the board file — AT-1501 named in the file docstring | 6 nodes passed |

The shipping session's targeted run held the file at **6 passed, 0 failed** (3.50s,
`evidence/inc001-run.log:440`) and its ONE complete run over the tree reported **`5 failed, 2587
passed in 455.47s`** (`evidence/inc001-run.log:483`) — the 5 failures ALL pre-existing batch-07/08
arms pinning the old picker shape (the contract's FIRST-row law), which the session STOPPED and
named rather than touched (`:529-537`). The coordinator's five law-driven fixture updates followed
(named in `evidence/mutations.log`), after which the 15 template arms across the three files stand
green (the coordinator's verification, `evidence/mutations.log`). "See 04-validation" for the close
number; the orchestrator's C-25 owns the ONE final clean-tree run.

**The 5 failures in the cited transcript, named (V56):** they sit in
`evidence/inc001-run.log:477-483` — the session's single full-suite run, and every one is the
picker-shape ripple, not a defect in the increment and NOT the G-011 flake (G-011 did not fire in
this run):
`tests/test_templates_app.py::test_I_opens_the_picker_listing_presets_with_counts` ·
`::test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo` ·
`::test_user_template_lists_before_presets_and_inserts_with_links` ·
`::test_empty_template_toasts_is_empty`, and
`tests/test_template_save_app.py::test_type_a_name_and_enter_saves_and_lists_in_the_picker`.
The exact diffs are tabled in §2 and §4 Correction population; the suite's settled state after the
coordinator's updates is 2592 collected, 15/15 template arms green. No failure count anywhere in
the evidence contradicts the packet's settled state.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M18 (the linear wait chain not written):** `entry["wait"] = i - 1` → `pass` (`app.py:835`) — the increment's signature shape (the chain) collapses to a bag of independent tasks |
| Instrument | project code: the coordinator's byte-level mutation runner (`evidence/mutations.log` — byte-anchored, restores sha256-verified) |
| Where it ran | **my own tree** — the MAIN checkout (the batch's single lane; the battery is the coordinator-run close-out set M18, executed on this tree) |
| Transcript | `evidence/mutations.log` M18 — `1 failed, 5 passed` on `tests/test_template_new.py` |
| Restore proven by | **file hash returned to its pre-mutation value** — `evidence/mutations.log`'s header: "byte-level, restore sha256 OK" |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **6** — `pytest tests/test_template_new.py --collect-only -q` resolves exactly the 6 arms named in the Layer table (run at this close) |
| Verdict granularity | **per resolved node id** — M18 reddened exactly the arm that asserts the round-trip chain; the other five stayed GREEN on the same mutant |
| Arms that stayed GREEN | **named:** `test_picker_lists_new_template_first` (the row lists regardless of the chain), `test_all_empty_saves_nothing` (nothing saved either way), `test_name_without_tasks_saves_nothing`, `test_escape_writes_nothing`, `test_single_task_line_works` (a one-task template carries no `wait` to drop) |

The base-tree RED is by construction, and is itself executed evidence: the new file imports
`TemplateEditor`, which does not exist at base (`from taskboard.modals import TemplateEditor`,
`tests/test_template_new.py:23`) — on the pre-batch tree the collection itself fails, the signature
of a wholly new surface. M18 is the executed counterfactual on THIS tree, where the feature exists.

| Field | Value |
|---|---|
| **RED counterfactual** | M18 — the `wait = i−1` chain reduced to `pass` · transcript `evidence/mutations.log` M18 (`1 failed, 5 passed`, the GREEN arms named above) · restore digest: sha256 `restore sha256 OK` · the base-tree RED: the new file's import fails at collection on the pre-batch tree |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node: **M18** (`entry["wait"] = i - 1` → `pass`, `app.py:835`) · `test_editor_saves_a_linear_chain_and_round_trips` KILLED (the round-trip chain arm reddens — the `wait` indices after an `I` insert) · GREEN: `test_picker_lists_new_template_first` · `test_all_empty_saves_nothing` · `test_name_without_tasks_saves_nothing` · `test_escape_writes_nothing` · `test_single_task_line_works` (all five named above) · inert arms: none · registry: no `docs/tools/devflow-mutants.json` battery in this repo — M18 is the coordinator-run close-out battery · transcript `evidence/mutations.log` · restore digest: sha256 `restore sha256 OK` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M18's mutant code | per-arm `failed` exactly as tabled above (`evidence/mutations.log` — `1 failed, 5 passed`) |
| `pytest` (the suite) | the contract's FIRST-row law landed on a tree whose pre-existing tests pin the old picker shape | `5 failed, 2587 passed` on the session's full run — every failure a pre-existing arm, each named in the session's STOP report (`evidence/inc001-run.log:477-537`); after the coordinator's five fixture updates the same arms pass unchanged in outcome (`evidence/mutations.log`) |
| the arm-resolution probe (`--collect-only`) | a whitespace-delimited `-k` pattern would silently drop parametrized arms | resolves exactly 6 nodes on `tests/test_template_new.py` (run at this close) — the count every verdict above is granular over |
| the shipped help/English censuses (`test_english.py`, `test_help_clip.py` — they read `help_usage` for every mode) | the `?` bullet split into two lines | stayed green through the session's full run (`evidence/inc001-run.log:513-544`) — both new lines ≤44 cells, English, no markup flags |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown RED (or discriminating) before its first PASS was believed (transcripts in `evidence/mutations.log` · `evidence/inc001-run.log`) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the saved settings entry | `app.board.settings["templates"] == [{"name": "Launch", "tasks": [{"title": "Design"}, {"title": "Build", "wait": 0}, {"title": "Ship", "wait": 1}]}]` | equal — the exact dict, the `wait` chain 0←1 (`tests/test_template_new.py:102-106`) |
| the save toast | `_toast_check(app, "Templates", "Template 'Launch' saved — 3 tasks")` — `str(t.render())` of the painted `Toast`, partitioned on its newline | `None` (a byte-exact title/body match; `:107-108`) · and on the single task: `Template 'Solo' saved — 1 tasks` (`:184-185`) |
| the picker rows after the save | `_plains(app.screen.query_one("#template-list"))[1]` | `"Launch — 3 tasks"` — the saved template lists right after the authoring row (`:114`) |
| the round-trip graph shape | `created[0].depends_on == []` · `created[1].depends_on == [created[0].id]` · `created[2].depends_on == [created[1].id]` | the exact linear chain after an `I` insert — titles `["Design", "Build", "Ship"]` (`:117-121`) |
| the picker rows at open | `_plains(...) == ["New template...", "Deploy — 2 tasks", "Simple chain — 3 tasks", "Bugfix — 3 tasks"]` | the authoring row FIRST, ahead of the user template and both presets (`:84-86`) |
| the all-empty refusal | `_toast_check(app, "Templates", "Template not saved — give it a name and at least one task.")` | `None` — one line saying why, nothing saved (`:138-140`) |
| the all-empty / esc byte-identity | `"templates" not in app.board.settings` and `path.read_bytes() == raw_before` | both held — the settings AND the board file are byte-identical (`:136-137`, `:168-169`) |
| the single-task shape | `settings["templates"] == [{"name": "Solo", "tasks": [{"title": "One task"}]}]` | one entry, NO `wait` key — absent, not null (`:182-183`) |
| the `?` kanban help | the bullet lines themselves, `views.py:6837-6838` | `I inserts · New template... authors` · `notes stay JSON-only at this version` |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 9 artifacts, each asserted against the form its producer emitted (the settings dict · the rendered toast bytes ×2 · the picker rows ×2 · the round-trip depends_on · the refusal toast · the byte-identity ×2 halves counted with their arms · the single-task shape · the help bullets) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the increment brief (the coordinator's chunk brief) | `.dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md` | `422a4e0bfabbd32c7fc01d8897c0625edeb05d844e30f18e7a77bbb6eca79643` |
| the shipping session's run log (the seat/tcss census, the picker+editor+app+views diffs, the targeted 6-passed run, the one full-suite run + the STOP-and-name of the 5 pre-existing reds, the review packet) | `.dev-flow/2026-10-07-batch-09/evidence/inc001-run.log` | `5f1f12c413c7f1a9a180039d3152114a5bd2d361c79c1dbb1c1a7d7c0da476c1` |
| the close-out mutation battery M18 + the five law-driven fixture updates (coordinator-run, byte-level, restore sha256 OK) | `.dev-flow/2026-10-07-batch-09/evidence/mutations.log` | `5240152b483e9fd3e561a35a860654849a27f0d8753cc50e22ccbc45e1e4a2da` |

The new test file's stored bytes: `tests/test_template_new.py` sha256
`54c4469a133f839670ba5a2a82645b0cb252ef26f7b03972608130a7e3338f31` (its home is the `tests/`
home `artifact_homes.tests` declares — cited here for the record, not as an evidence-home artifact).

| Field | Value |
|---|---|
| **Evidence files** | `3` artifacts at the evidence home, each cited with the digest of its stored bytes; the new test file's digest cited beside the table (its home is `artifact_homes.tests`) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — three: (1) "an all-empty edit / esc writes NOTHING" — an absence over `settings` AND the board file's bytes; (2) "authoring is NOT an undo step" — an absence over the undo stack (declared semantics, docstring-pinned, the batch-08 rule); (3) "a one-task template carries NO `wait` key" — an absence of the key in the emitted entry (absent keys, not nulls — the batch-08 store contract) |
| If the result is an ABSENCE, what made the search wide enough | (1) the all-empty and esc arms read the WHOLE board file's bytes before/after (`path.read_bytes() == raw_before`) plus the settings dict — not a spot check of one key; (2) the docstring states the law at the callback seat (`app.py:814-822`), and no undo entry exists in the settings-entry shape to assert against — the absence is by construction, declared; (3) the single-task arm asserts the emitted dict EXACTLY (`[{"title": "One task"}]` — `:182-183`), so any extra key (`wait`, `notes`) reddens it |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_all_empty_saves_nothing` — its docstring names the conclusion "settings byte-identical (absent)" for the file-identity probe; `test_escape_writes_nothing` names "nothing written, the board file untouched" — both say what the absence CONCLUSION is, so the next reader does not "simplify" the arm into a presence check |
| Conjunctive criteria: one mutation per conjunct | the save law conjoins the listing row · the validation · the linear chain · the settings append + save · the toast: M18 kills the chain conjunct (`1 failed`, the round-trip arm); the session's full-suite RED killed the listing-shape conjunct in the pre-existing arms (5 failed, named) — one probe per conjunct, each discriminating |
| Synthetic instance of the absent case | the all-empty fixture (`"   "` + `"\n\n  \n"`) and the esc fixture (`"Doomed"` then `escape`) are the tree-level instances of "an edit that must write nothing" — the tree ships no such path that writes; the fixtures carry it in-memory |
| **Positive control for every probe that returned an ABSENCE** | (1) the same file-bytes probe's positive half is the save arm's settings assertion (the entry IS present after Save, `:102-106`) — uniformity over the same mechanism, save vs esc/empty; (2) the batch-08 chain-save's ONE-undo-entry insert is the known-present undo neighbour — the settings save composes beside it, never into it; (3) the multi-task save arm emits `wait: 0` / `wait: 1` — the known-present key the single-task arm asserts absent |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rn "__new__\|TemplateEditor" taskboard/*.py tests/*.py` → `taskboard/app.py:31` (import) · `:746` (the `push_screen`) · `taskboard/modals.py:872`/`:922` (the PRE-EXISTING `L` link-picker create row — the same reserved-id convention this increment composes) · `:967`/`:978` (this increment's seats) · `:987` (the editor def) · `tests/test_template_new.py:23`/`:63` (the import + the arm's isinstance) | every reader of the NEW symbols is THIS batch's own; the `:872`/`:922` hits are the house pattern the row was modelled on, not moved by it; the `help_usage`/`TemplatePicker` surfaces are censused by the shipped help/keymap families — every outside reader re-validated by the suite |
| B2 file moved on disk | `git status --porcelain -- taskboard/ tests/` → ` M` app/modals/views · `tests/test_template_save_app.py` · `tests/test_templates_app.py` · `??` `tests/test_template_new.py` | modified in place, no rename, no delete — the old paths are the current paths; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → `No such file or directory` | the repo holds no golden-capture directory (as batch-05..08 recorded); did NOT fire — the `?` bullet is instead censused by the shipped help/English families (`test_help_clip.py` · `test_english.py`), which stayed green through the full run |
| B4 artifact produced here is consumed elsewhere | `grep -rn "TemplatePicker\|_on_template_picked\|_on_template_authored" taskboard/*.py` → `app.py:738-739` (the only push/callback pair) · `modals.py:933` (the def); `grep -rn '"templates"' taskboard/app.py` → the batch-07/08 read/insert seats now ALSO read what this increment appends | the consumers are exactly this increment's seats + the batch-07 store/picker machinery and the batch-08 save seam (both unchanged — the authored entry is read through the shipped `templates()`/`_read_template` lenient read and appended through the shipped batch-08 settings seam); all re-validated by the green suite |
| A3 interface consumed by another module changed | `TemplatePicker`'s return type moved `str | None` → `tuple[str, str] | None` — the ONLY caller is `action_templates` (`app.py:738-746`); `grep -rn "_on_template_picked" taskboard/*.py tests/*.py` → the definition and its one call site, no test calls it directly (the session's risk note, re-run at this record) | no cross-module consumer exists outside the seats named in B4; the change is additive at every other seam — the picker still lists, the store still reads, the insert still inserts |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1's hits are this batch's own files + the house `__new__` pattern it composes (not moved), B4 names the one caller and the store's unchanged readers, A3 names the return-type change and its single caller, B2/B3 did NOT fire with their probes recorded · transcripts in `evidence/inc001-run.log` |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the contract's "`New template...` is the FIRST option" — the shared `I` picker's listing shape and first-highlight moved; every pre-batch-09 assertion pinning the old shape must be updated, not weakened | every test arm asserting the picker's exact rows, first-highlight navigation, or a saved template's picker index | the shipping session's ONE full-suite run over the tree with the increment landed (`python -m pytest -q`, `evidence/inc001-run.log:443-483`) + the seat grep `grep -rn "TemplatePicker\|#template-list" tests/` (`:100-113`); the session named all 5 in its STOP report BEFORE any fixture was edited (`:529-537`) | 5 | `tests/test_templates_app.py` ×4 — `:70` (the presets listing gains the leading row) · `:88` (`enter` → `down, enter`, past the authoring row to Simple chain) · `:141-142` (the user-template listing gains the row + `down, enter`) · `:166` (`down, enter` past the row to Empty); `tests/test_template_save_app.py` ×1 — `:116` (the saved template now lists at index 1) | 0 — the enumeration closed on the run's failure list; every red arm was a picker-shape pin, none was weakened (same outcomes, new shape — the diffs tabled in §2) |

| Field | Value |
|---|---|
| **Correction population** | `1` correction — the FIRST-row law's ripple into the pre-existing picker tests — enumerated with its method (the full-suite run + the seat grep) BEFORE the first fixture was edited; 5 sites, 0 left, assertions not weakened |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| — none — nothing superseded this batch | — | — | — |

### Signed-balance test ledger

`post = base − deleted + added` → `2592 = 2586 − 0 + 6` ✓ reconciles (base = the batch-08 trunk
at 2586; A = 6 new nodes — the arms of `tests/test_template_new.py`; the coordinator's five
law-driven fixture updates deleted/added NO nodes; the `?` bullet modified no test). The close-out
re-collected the suite at **2592 tests** on the final tree (`pytest tests --collect-only -q`,
0.62s) — matching the session's full run arithmetic exactly (`5 failed + 2587 passed = 2592`
collected). "See 04-validation" for the close number; the orchestrator's C-25 owns the ONE final
clean-tree run.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` — the close-out coordinator self-executed the P2 lens pool over the packet, the diffs, and the evidence · verdict PASS-WITH-NOTES, 0 HIGH — the notes: (a) the five law-driven fixture updates are the named cost of the contract's FIRST-row law rippling into the shared picker's pinned tests — recorded in §1/§4 and `02-review.md`'s observation, the assertions verified not weakened · (b) the `views.py` help-bullet read as `doc` is the third consecutive batch to record it — named for the operator's rule-or-retire ruling · the P2 review verdict stands in `02-review.md` (0 blocker · 0 major · 0 minor, one declared observation; reviewer `human:coordinator`, the runtime spawned nobody) |

---

## 5 · Risks

- The picker resolves by name (batch-07's standing risk, inherited): a scratch template named
  exactly `Simple chain` or `Bugfix` shadows the preset silently (user templates list after the
  authoring row but before the presets). Unchanged by this increment; carried in the backlog's
  standing line, not new.
- The degenerate one-task save toasts `Template '<name>' saved — 1 tasks` — ungrammatical but the
  PINNED batch-08 literal (the arm asserts it byte-exact, `tests/test_template_new.py:185`).
  Changing the pluralization reddens the pinned arm; declared so the next reader does not
  "correct" it unarmed.
- The save is not undoable (declared, docstring-pinned): a fat-fingered save appends a template the
  operator removes by hand in the board JSON at v1 — the same deletion seat batch-07's `?` bullet
  documents.
- The FIRST row changes every future picker fixture: any new test pinning the picker's listing or
  first-highlight must account for `New template...` at index 0 — the cost the five law-driven
  updates paid; named so the next author does not "discover" it in a red suite.
- The authoring row requires a resolvable project BEFORE the picker opens (the batch-07
  `No project to insert into.` guard runs first): on an empty board, `I` refuses and the authoring
  route is unreachable — the shipped seat's semantics, composed unchanged, not a defect.

## 6 · Pending items / spec deviations

- None open in this increment. The five pre-existing picker-shape reds the session surfaced were
  CLOSED by the coordinator's law-driven fixture updates before this close (named in
  `evidence/mutations.log`; the diffs in §2 and §4 Correction population). The only spec note: the
  `?` bullet gained one line (the notes-stay-JSON clause), split out of the old single line —
  inside the brief's `views.py` remit, declared in §1.

## 7 · Suggested next task

- None pressing — the operator's follow-up (scratch authoring) ships in this batch. Standing
  candidates: the operator's first-eye verdict on the editor surface (fresh surface, no trigger-D
  commission); the operator's ruling on minting the stop-and-name candidate control (now THREE
  consecutive batches deep — batch-07, batch-08, this batch); and the evergreen G-011 environmental
  flake (standing, environmental).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 2 source files — modals/app, two under the cap; the `views.py` help bullet counted as `doc` (the third-consecutive notice declared in §2) |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_template_new.py` (6 arms) landed with the product in the same session; 6 passed, 0 failed (3.50s — `evidence/inc001-run.log:440`); the 2 updated files' 5 arms re-green after the coordinator's law-driven updates (`evidence/mutations.log`) |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | none applied — no new module-level unit this batch (declared in the Layer table); the callback's logic is covered white-box + M18 |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M18 executed (`1 failed, 5 passed`); transcript `evidence/mutations.log`; restore sha256 OK; the base-tree RED (collection fails on the new file's import) declared |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above); B2/B3 did NOT fire; A3 names the return-type change's single caller |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b — `human:coordinator` · PASS-WITH-NOTES 0 HIGH (the observation in `02-review.md`) |
| 7 | No file from another lane touched | all | ✓ | one lane, one brief, one session |
| 8 | Frozen interfaces untouched | all | ✓ | the `templates()` store read, `_read_template`'s lenient shape, the batch-08 settings/save seam, the `TextPrompt`/`ProjectModal` chrome, and `help_usage`'s signature are pre-batch bytes; the `TemplatePicker` return type is the one interface move — its only caller is the route this increment owns (A3 probe) |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | three absences — the all-empty/esc byte-identity, the no-undo-entry authoring, the no-`wait` single task — each with its positive control and its synthetic fixture |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | M18 per-node (1 KILLED, 0 SURVIVED, the 5 GREEN arms named); transcript + restore digest cited |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) — pytest ×2 (M18 + the 5-arm picker-shape RED), the arm-resolution probe, the shipped help/English censuses |
| 13 | **Correction population** declared | all | ✓ | 1 correction — the FIRST-row law's 5-site ripple — enumerated by the full-suite run + seat grep BEFORE the first fixture was edited; 0 left; assertions not weakened |
| 14 | **Emitted-form assertion** declared | all | ✓ | 9 artifacts — the settings dict, the toast bytes ×2, the picker rows ×2, the round-trip depends_on, the refusal toast, the byte-identities, the single-task shape, the help bullets |
| 15 | **Independent review** names somebody | all | ✓ | §4b — `human:coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 3 artifacts at the evidence home + the new test file's digest cited beside the table |
