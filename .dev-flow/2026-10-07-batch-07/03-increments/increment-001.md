# Increment 001 — HLR-1301 · process/chain templates insertable into a project

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
> `.dev-flow/2026-10-07-batch-07/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-07` |
| Increment | `001` (the whole batch — one increment, one brief) |
| Lane (if the batch forked) | `none` — one implementing brief owned the tree; TWO sessions under it: the first STOPPED before writing any code (it named the `T`-key conflict instead — the batch's hero lesson, §1 below), the second shipped green after the contract was corrected to `I` under LED-2026-10-07-batch-07.2 |
| Requirement(s) | `HLR-1301` (+ `LLR-1301.1` the store · `LLR-1301.2` the insert) |
| Acceptance | `AT-1301` — 9 arms, all green (4 store arms in `tests/test_templates.py` + 5 app arms in `tests/test_templates_app.py`, the docstring home of the `AT-1301` dash token) |
| Agent | `software-dev` — DeepSeek V4 Pro (two sessions: the stopped reconnaissance, then the shipping session; `evidence/inc001-run.log` · `evidence/inc001b-run.log`) |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

Press `I`, pick a template, and the project's chain of tasks exists — linked, named, undoable in one
step. The picker (`TemplatePicker`, `taskboard/modals.py:933-977`, LinkPicker chrome) lists the
board's user templates first — `settings["templates"]`, portable with the board, edited by hand in
the board JSON at v1 — then the two factory presets, each row `name — N tasks`. A pick resolves
through `app.action_templates` (`taskboard/app.py:723-736`): the target project is the selected
task's, exactly the presentation's `present_project_id` resolution (the focused project when set;
none resolvable → the `No project to insert into.` toast, `markup=False`, no picker). The insert
(`_on_template_picked`, `app.py:738-763`) creates every task in the board's FIRST phase with NO
dates, house-generated ids, titles/notes from the template, linked exactly as the template declares
(`wait` = the predecessor's index inside the template — forward-only, cycles impossible by
construction; a `wait` that does not resolve drops only that link, the task is kept unlinked); it
selects the first created task, pushes ONE `{"templates": [ids…]}` undo entry, saves, refreshes, and
toasts the pinned literal `Inserted '<name>' — <N> tasks into <project>` (`markup=False`). An empty
template inserts nothing and toasts `Template '<name>' is empty.` The undo branch
(`app.py:1499-1511`, the shipped milestones-undo pattern applied to removal) removes every inserted
id in one step and toasts `Template insert undone — N tasks removed`; a second `u` says
`Nothing to undo.` — no resurrection. The `?` kanban help gained one bullet
(`views.help_usage`, `taskboard/views.py:6837`): `I inserts a template · edit it in board JSON`, and
the README keybinding table gained the `I` row (`README.md:135`).

Mechanism, by seat: the store (`models.templates(board)`, `taskboard/models.py:2284-2326`) —
`TemplateTask`/`Template` frozen dataclasses, `PRESET_TEMPLATES` (`Simple chain`: Plan → Build →
Ship; `Bugfix`: Triage → Fix → Verify), a lenient `_read_template` that skips a malformed entry
whole (non-dict, non-text name, non-list tasks, a task that is not a dict or has a non-text/empty
title — dropping a mid-chain task would silently rewire the `wait` targets, so the entry goes, not
the task) and reads a bad `wait` as None (link dropped, task kept). The key
(`keymap.py:139`, `Key("I", "I", "templates", "Templates", group="misc", bar=False)` — global,
palette-only, listed in `BOARD_ACTIONS` at `app.py:331` beside `"present"`).

**The `T`-key conflict — carried prominently, it is this batch's hero lesson.** The contract as first
written (LED-2026-10-07-batch-07.1, and the brief minted from it) pinned `T` as the picker key. The
first implementing session read the seat before editing, found `T` already shipped —
`keymap.py:86`, `Key("T", "T", "project_pin_toggle", "Pin proj", group="task")` — pinned by
`tests/test_focus.py:46` and `:151` and `tests/test_markup_sites.py:267` (each presses `T` and
expects the "Pin project" toast) — and STOPPED before writing any code, naming the conflict and the
two ways it could only redden the suite (`evidence/inc001-run.log`, the session's stopped-run
report). The contract was corrected to `I` under LED-2026-10-07-batch-07.2 **before the first edit**;
the second session then shipped green with every existing seat untouched. The stop-and-name gate —
"if anything outside your files reddens, STOP and name it" — working exactly as designed. (A
residual of the same class was caught at this record pass: the IFC block still read `keymap T` after
the LED .2 sweep — fixed, finding F1 in `02-review.md`.)

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | HLR-1301 · LLR-1301.1 | the store — `TemplateTask` · `Template` · `PRESET_TEMPLATES` · `templates(board)` · `_read_template` (`:2253-2326`) |
| `taskboard/app.py` | source | HLR-1301 · LLR-1301.2 | `action_templates` (`:723-736`) + `_on_template_picked` (`:738-763`); `"templates"` in `BOARD_ACTIONS` (`:331`); the `templates`/`TemplatePicker` imports (`:24`, `:30`); the `"templates"` undo branch (`:1499-1511`) |
| `taskboard/modals.py` | source | HLR-1301 · LLR-1301.2 | `TemplatePicker` (`:933-977`) — LinkPicker chrome, an `OptionList` of `name — N tasks`, esc closes; the `templates` import (`:40`) |
| `taskboard/keymap.py` | source | HLR-1301 · LLR-1301.2 | `Key("I", "I", "templates", "Templates", group="misc", bar=False)` (`:139`) + its two-line comment — +3 lines |
| `taskboard/views.py` | doc | | the `?` kanban bullet (`:6837`): `I inserts a template · edit it in board JSON` — LLR-1301.2's help deliverable; a one-string documentation addition shipped in code (see the notice below) |
| `README.md` | doc | | the `I` keybinding-table row (`:135`) — forced by the shipped README-census test (§4, Instrument RED-proof) |
| `tests/test_templates.py` | test | LLR-1301.1 — pinned by AT-1301 | new — 4 store arms |
| `tests/test_templates_app.py` | test | HLR-1301 · LLR-1301.2 — AT-1301's docstring home | new — 5 app arms |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 2 (outside the count) |

- ⚠ **At exactly 4 source files:** the four seats of ONE user gesture — the key (`keymap.py`), the
  store (`models.py`), the action + one-step undo (`app.py`), the picker surface (`modals.py`) —
  the same shape batch-2026-10-04-batch-01's 4/4 recorded ("one gesture over four seats"). Cut any
  one and the shipped feature is a key with nothing to insert, a picker listing nothing, a store
  nobody reads, or an insert with no surface.
- ⚠ **`views.py` counted as `doc`, not source:** its entire change is one `?`-help sentence — a
  documentation string shipped in code, the README row's sibling. Declared here (the notice form);
  if a third consecutive batch reads a help-only `.py` change this way it becomes a rule or is
  retired.

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_templates.py tests/test_templates_app.py -q   # 9 passed
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests --collect-only -q                                   # 2575 collected
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (the store's lenient read — `templates`/`_read_template`'s isinstance/branch cascade over entries, tasks, titles, notes, waits; cyclomatic ≥3) | `core` · `full` | the 4 arms of `tests/test_templates.py` | 4 passed (mutation-proven — M15 below) |
| **A · white-box** ↔ LLR-1301.2 (the insert's mechanism: project resolution, creation in the first phase, the exact `depends_on` chain, the ONE undo entry, the refusal) | `core` · `full` | `test_I_opens_the_picker_listing_presets_with_counts` · `test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo` · `test_no_project_refuses_with_the_toast` · `test_user_template_lists_before_presets_and_inserts_with_links` · `test_empty_template_toasts_is_empty` | 5 passed (mutation-proven — M13/M14) |
| **B · black-box** `AT-1301` ↔ US-1301, through the shipped surface | `core` · `full` | the same 5 app arms — keys through `run_test` (`I`, `enter`, `u`), the painted picker rows, the toast's rendered bytes, the board state — AT-1301 named in the file docstring | 5 nodes passed |

The shipping session's targeted run held the two files at **9 passed, 0 failed** (2.17s,
`evidence/inc001b-run.log`) and its ONE complete green run over the settled tree passed **2575 /
2575** (423.20s, `evidence/inc001b-run.log`); the close-out re-collected the suite at **2575
tests** on the final tree (`pytest tests --collect-only -q`). "See 04-validation" for the close
number; the orchestrator's C-25 owns the ONE final clean-tree run.

**The 21 failures in the cited transcripts, named (V56):** they sit in
`evidence/inc001b-run.log:722` — the shipping session's FIRST full-suite attempt (21 failed, 2554
passed). One is the README keybinding census, the known forced row the session then shipped
(`README.md:135`); the other 20 are git-state/environment arms (the precommit-gate family, the
scratch-cannot-be-committed family, the report CLI pair, the live-board fixture) disturbed by the
in-flight tree during that attempt — the settled-tree re-run passed 2575 / 2575 with zero. The
mutation battery's `failed` counts (`evidence/mutations.log`) are the deliberate per-mutant REDs
tabled above. No failure count anywhere in the evidence contradicts the packet's `0 failed` at
settle.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M13 (the one-step undo holds only the first id):** `{"templates": [t.id for t in created]}` → `{"templates": [created[0].id]}` — the batch's signature behavior (ONE `u` removes the whole insert) collapsed to a single task |
| Instrument | project code: the coordinator's byte-level mutation runner (`evidence/mutations.log` — byte-anchored, restores sha256-verified) |
| Where it ran | **my own tree** — the MAIN checkout (the batch's single lane; the battery is the coordinator-run close-out set M13-M15, executed on this tree) |
| Transcript | `evidence/mutations.log` M13 — `1 failed, 4 passed` on `tests/test_templates_app.py` |
| Restore proven by | **file hash returned to its pre-mutation value** — `evidence/mutations.log`'s header: "byte-level, restores sha256-verified; all OK" |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **5** — `pytest tests/test_templates_app.py --collect-only -q` resolves exactly the 5 arms named in the Layer table |
| Verdict granularity | **per resolved node id** — M13 reddened exactly the undo arm (`test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo`); the other four stayed GREEN on the same mutant |
| Arms that stayed GREEN | **named:** `test_I_opens_the_picker_listing_presets_with_counts` (the picker lists regardless of the undo entry), `test_no_project_refuses_with_the_toast` (no insert happens), `test_user_template_lists_before_presets_and_inserts_with_links` (asserts the insert + its links + the toast, none of which the mutated undo entry touches), `test_empty_template_toasts_is_empty` (no insert happens) |

The base-tree RED is by construction, and is itself executed evidence: both new files import
symbols that do not exist at base (`from taskboard.models import … Template, TemplateTask,
templates`; `from taskboard.modals import TemplatePicker`) — on the pre-batch tree the collection
itself fails, the signature of a wholly new surface. M13 is the executed counterfactual on THIS
tree, where the feature exists.

| Field | Value |
|---|---|
| **RED counterfactual** | M13 — the undo entry reduced to the first created id · transcript `evidence/mutations.log` M13 (`1 failed, 4 passed`, the GREEN arms named above) · restore digest: sha256-verified `all OK` · the base-tree RED: the new files' imports fail at collection on the pre-batch tree |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node: **M13** · `test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo` KILLED (one `u` leaves two inserted tasks behind) · the four GREEN arms named above · **M14** (the `wait` application `new.depends_on = [created[one.wait].id]` → `pass`) · `test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo` KILLED + `test_user_template_lists_before_presets_and_inserts_with_links` KILLED (`2 failed, 3 passed` — the exact-chain and the user-template chain arms) · GREEN: the picker arm, the no-project arm, the empty arm · **M15** (`templates()` raising ValueError on a non-dict entry instead of skipping) · `test_lenient_read_skips_junk_and_drops_bad_waits` KILLED (`1 failed, 3 passed`) · GREEN: the round-trip, presets, and presets-only arms · inert arms: none · registry: no `docs/tools/devflow-mutants.json` battery in this repo — M13-M15 are the coordinator-run close-out battery · transcript `evidence/mutations.log` · restore digest: sha256 `all OK` for all three |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M13/M14/M15's mutant code | per-arm `failed` exactly as tabled above (`evidence/mutations.log`) |
| the README keybinding census (`tests/test_keymap.py:404`, `test_the_readme_keybinding_table_matches_the_seat`) | the `I` key landed WITHOUT the README row | reddened on the shipping session's own keymap change — "without it the suite reddened on my own keymap change" (`evidence/inc001b-run.log` §5); the row was added and the census went green |
| the stop-gate seat census (the first session's probes) | the proposed `T` binding against the shipped keymap | `grep -rn "Pin proj\|project_pin_toggle" tests/test_keymap.py tests/test_markup_sites.py` → `tests/test_markup_sites.py:267` … and the pressing-`T` arms at `tests/test_focus.py:46` / `:151` named — the collision reported BEFORE the first edit, with the predicted RED named (either binding order silently unseats `project_pin_toggle`, or a duplicate-key construction error — `evidence/inc001-run.log`) |
| the arm-resolution probe (`--collect-only`) | a whitespace-delimited `-k` pattern would silently drop parametrized arms | resolves exactly 4 + 5 = 9 nodes on the two files (run at this close, `04-validation.md`) — the count every verdict above is granular over |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown RED (or discriminating) before its first PASS was believed (transcripts in `evidence/mutations.log` · `evidence/inc001-run.log` · `evidence/inc001b-run.log`) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the picker's OptionList rows (no user templates) | `_plains(app.screen.query_one("#template-list"))` — the painted `Option` prompts | `["Simple chain — 3 tasks", "Bugfix — 3 tasks"]` (verbatim, `tests/test_templates_app.py:69-70`) |
| the picker's OptionList rows (a user template first) | same probe on the user-template board | `["Deploy — 2 tasks", "Simple chain — 3 tasks", "Bugfix — 3 tasks"]` (`:140-141`) |
| the insert toast | `_toast_check(app, "Templates", "Inserted 'Simple chain' — 3 tasks into Plat")` — `str(t.render())` of the painted `Toast`, partitioned on its newline | `None` (a byte-exact title/body match; `:100-101`) · and on the user template: `Inserted 'Deploy' — 2 tasks into Plat` (`:149-150`) |
| the refusal + empty toasts | same probe | `No project to insert into.` (`:120`) · `Template 'Empty' is empty.` (`:168`) |
| the `?` kanban help | the bullet line itself, `views.py:6837` | `I inserts a template · edit it in board JSON` |
| the README keybinding row | the census test's table read | ``| `I` | Templates | Insert a process template (a named chain of tasks) into the selected task's project |`` (`README.md:135`) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 6 artifacts, each asserted against the form its producer emitted (the painted picker rows · the rendered toast bytes · the refusal/empty toasts · the help bullet · the README row) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the increment brief (the coordinator's chunk brief, minted under LED .1, key line corrected by LED .2) | `.dev-flow/2026-10-07-batch-07/evidence/inc001-brief.md` | `ef07f59ad8be6f61669d52e54f23ecba3c96d4d3c5cb57129da4e88cdd5271c7` |
| the stopped session's run log (the reconnaissance + the T-conflict stop-and-name report — the batch's hero evidence) | `.dev-flow/2026-10-07-batch-07/evidence/inc001-run.log` | `890ecc08d17a26dc4f1d184bd058c8c2883fef2f33324afd65dc77273209efd4` |
| the shipping session's run log (the targeted 9-passed run, the full green at 2575/423s, the review packet) | `.dev-flow/2026-10-07-batch-07/evidence/inc001b-run.log` | `293565d0c0f15ec231ad1f22fa34c698391e453cbc35bb5f6a4cf486c8131863` |
| the close-out mutation battery M13-M15 (all KILLED, restores sha256-verified) | `.dev-flow/2026-10-07-batch-07/evidence/mutations.log` | `ce1ef2c2004a5dcce2be13b579a314ac99f303a59daae69e91225c16ea022739` |
| the P1 contract fill script (writes `01-requirements.md` + the ledger seeds at Phase 1) | `.dev-flow/2026-10-07-batch-07/evidence/p1_fill.py` | `bb70a2ace4fa91033f70ac51e3ac734c1f31d821adb7d169d68a920ad35775d3` |

The new test files' stored bytes: `tests/test_templates.py` sha256
`cb1a38b3df7dae59dfd582bef5370c58bf59d2cbdb6745a2d514f2b88357e720` · `tests/test_templates_app.py`
sha256 `80e650d2e39122ceb89213fd3fae06e7b7ba2b07969fa66b4d771d78fd259cfb` (their home is the
`tests/` home `artifact_homes.tests` declares — cited here for the record, not as evidence-home
artifacts).

| Field | Value |
|---|---|
| **Evidence files** | `5` artifacts at the evidence home, each cited with the digest of its stored bytes; the two new test files' digests cited beside the table (their home is `artifact_homes.tests`) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — three: (1) "no shipped seat moved — the tree holds NO second binding of `T` (or `I`)", the stop-gate claim; (2) "the insert invents NO dates" — an absence over every created task's `start_date`/`due_date`; (3) "a second `u` does NOT resurrect the inserted tasks" — an absence after the second undo |
| If the result is an ABSENCE, what made the search wide enough | (1) the whole `keymap.py` seat census by the shipped keymap tests (`test_keymap.py` — every bound key documented and exactly seated), plus the stop-gate grep over `tests/` for `T`'s pins — not a peek at one binding; (2) the arm asserts the full `(project_id, phase, start_date, due_date)` tuple on EVERY created task (`for c in created:`), not a spot check; (3) the arm counts `len(app.board.tasks)` after each of the two undos |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_no_user_templates_returns_presets_only` — its docstring names it "The boundary" (an absent/empty settings list → presets only); the undo arm's docstring names "a second `u` says Nothing to undo." — both say what the absence CONCLUSION is, so the next reader does not "simplify" the arm into a presence check |
| Conjunctive criteria: one mutation per conjunct | the insert law conjoins creation + linking + one-step undo: M14 kills the linking conjunct (`2 failed`), M13 kills the undo conjunct (`1 failed`), M15 kills the leniency conjunct — one probe per conjunct, each discriminating |
| Synthetic instance of the absent case | the junk-list fixture inside `test_lenient_read_skips_junk_and_drops_bad_waits` (six malformed entries of six different shapes) is the tree-level instance of "a settings list the user fat-fingered" — the tree ships no such board, the fixture carries it in-memory |
| **Positive control for every probe that returned an ABSENCE** | (1) the same suite run keeps the pressing-`T` arms GREEN (`tests/test_focus.py:46`/`:151` assert "Pin project", `tests/test_markup_sites.py:267` expects the pin toast — a non-absence on the known-present seat); (2) the same tuple probe reads the pre-existing task and the phase name `"Backlog"` (non-None fields on the known-present case) and the count probe returns `n0 + 3` before any undo; (3) the first undo's count assertion (`== n0`) is the non-absence half of the same probe — uniformity over the sequence, not one probe repeated |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln "\btemplates(" tests/` → `tests/test_templates.py` · `tests/test_templates_app.py`; `grep -rln "TemplatePicker" tests/` → `tests/test_templates_app.py`; `grep -rn "\btemplates(" taskboard/*.py` → `app.py:741` · `modals.py:963` · `models.py:2284` | every reader of the new symbols is THIS batch's own — no pre-existing test asserted a symbol this increment moved; the `help_usage` surface is censused by the shipped help families (`test_help_clip.py` et al.) — every outside reader re-validated by the green suite (2575) |
| B2 file moved on disk | `git status --porcelain -- taskboard/ tests/test_templates.py tests/test_templates_app.py README.md` → ` M` models/app/modals/views/keymap/README · `??` the two test files | modified in place, no rename, no delete — the old paths are the current paths; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → `No such file or directory` | the repo holds no golden-capture directory (as batch-05/06 recorded); did NOT fire |
| B4 artifact produced here is consumed elsewhere | `grep -rn "templates(" taskboard/*.py` → `app.py:741` (the insert's pick lookup) · `modals.py:963` (the picker's list); `grep -rn "TemplatePicker" taskboard/*.py` → `app.py:30` (import) · `app.py:735` (pushed); `grep -rn '"templates"' taskboard/app.py` → `:331` (`BOARD_ACTIONS` — the palette listing) · `:758` (the undo entry) · `:1499` (the undo branch) | the consumers are exactly this increment's seats — the store is read by the picker and the insert, the picker is pushed by the action, the undo key is read by the shipped `action_undo`; the palette's generic consumer of `BOARD_ACTIONS` is unchanged machinery; all re-validated by the green suite |
| A3 interface consumed by another module changed | new symbols only — no pre-existing interface moved: `present_project_id`'s resolution, the milestones undo-entry pattern, `help_usage`'s (mode) → sections signature, the LinkPicker chrome, and `BOARD_ACTIONS`'s listing shape are pre-batch bytes; `T`'s seat (`keymap.py:86`) untouched, proven by the pin arms staying green | no cross-module consumer exists outside the seats named in B4; the change is additive |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1's hits are this batch's own files + the help census family (re-validated by the suite), B4 names the four in-module consumers under unchanged machinery, B2/B3 did NOT fire with their probes recorded · transcripts in `evidence/inc001-run.log` · `evidence/inc001b-run.log` |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the templates key is `I`, not `T` (LED-2026-10-07-batch-07.2) | every contract/brief seat claiming the templates key + every shipped seat pressing `T` | the stopped session's probes BEFORE the first edit: `keymap.py:86` read · `grep -rn "Pin proj\|project_pin_toggle\|\"T\"" tests/test_keymap.py tests/test_markup_sites.py` · `tests/test_focus.py:46`/`:151` read · the contract's HLR-1301/LLR-1301.2 statements + the IFC node + the brief's tasks 2-3 read (`evidence/inc001-run.log`) | 7 claim sites (HLR-1301 statement · LLR-1301.2 statement · the IFC node · the brief's keymap line · the brief's help line · the brief's test line · the AT surface line) + 3 shipped `T` pins | all 7 claim sites corrected to `I` under LED .2 before the first code edit; the residual IFC line (`01-requirements.md:145`, missed by the first sweep) fixed at this record pass — `02-review.md` F1 | the 3 shipped `T` pins (`keymap.py:86`, `tests/test_focus.py:46`/`:151`, `tests/test_markup_sites.py:267`) — the correction's whole point; verified as the negative set by the same grep, green throughout |

| Field | Value |
|---|---|
| **Correction population** | 1 correction — the T→I key — enumerated with its method before the first site was edited, its positive set (7 claim sites) and negative set (3 shipped pins) both named |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the templates key as `T` in the LIVE contract | `grep -rn "keymap T\|key \`T\`" .dev-flow/2026-10-07-batch-07/01-requirements.md` → 0 hits (HLR-1301 pins `I` · LLR-1301.2 binds `I` · the IFC node now reads `keymap I` — fixed at this record pass, finding F1) | yes | `01-requirements.md:93` · `:119` · `:145` |
| the templates key as `T` in the batch record | the only surviving `T` mentions are historical: LED .1's append-only entry, the brief minted under .1, the stopped session's transcript, the p1 fill script — each names `T` as what WAS written, and LED .2 stands beside them as the correction | yes — history, not live refs | `01-requirements-ledger.md:12-17` · `evidence/inc001-brief.md:59` · `evidence/inc001-run.log` |

### Signed-balance test ledger

`post = base − D + A` → batch post `2575 = 2566 − 0 + 9` ✓ reconciles (base = the batch-06
trunk at 2566; A = 9 new nodes — the 4 store arms + the 5 app arms; the README row and the `?`
bullet modified no test). The close-out re-collected the suite at **2575 tests** on the final tree
(`pytest tests --collect-only -q`). "See 04-validation" for the close number; the orchestrator's
C-25 owns the ONE final clean-tree run.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` — the close-out coordinator self-executed the P2 lens pool over the packet, the diffs, and the evidence · verdict PASS-WITH-NOTES, 0 HIGH — the notes: (a) the contract pinned `T` without checking the seat — a writing defect of the same class as batch-06's marker glyphs, caught by the AGENT's stop gate before any code and folded via LED .2 (§1); (b) the IFC residual (`keymap T`, missed by the first sweep) fixed at this record pass — finding F1 in `02-review.md`; (c) the README row landed outside the brief's file list, forced by the shipped census test — declared and accepted · the P2 review verdict stands in `02-review.md` (0 blocker · 0 major · 1 minor; reviewer `human:coordinator`, the runtime spawned nobody) |

---

## 5 · Risks

- The picker's pick resolves **by name** (`next(t for t in templates(self.board) if t.name == name,
None)`, `app.py:741`): a user template named exactly `Simple chain` or `Bugfix` shadows the preset
(user templates list first, so the user's own wins). Reasonable, but the shadowing is silent —
declared so the next reader does not "fix" it into an error.
- v1 authoring is hand-edited board JSON; a fat-fingered settings list degrades silently (the
  lenient read skips — by design, pinned by M15). The `?` bullet is the documentation seat; a v2
  in-app authoring surface is the declared carry.
- The undo branch removes the created ids wholesale, like the shipped milestones pattern it copies:
  if a task created minutes ago has since gained dependents, undo removes it and leaves their
  `depends_on` dangling — the SAME exposure the milestones undo already ships; inherited, declared,
  not new.
- ⚠ The picker arm asserts the exact row census (`["Simple chain — 3 tasks", "Bugfix — 3 tasks"]`)
  — a third factory preset added later reddens it by design (the arm's job), not by regression.

## 6 · Pending items / spec deviations

- None open in this increment. The declared carry — template authoring from the app ("save this
  chain as a template"), v2 — is the batch-level pending; the close lands it in the canonical
  backlog.

## 7 · Suggested next task

- Template authoring v2 — "save this chain as a template" from the app (the declared carry in
  HLR-1301): a name prompt + a `settings["templates"]` write behind the shipped modal/seam pattern,
  one undo step, contractible as its own batch.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 4 source files — models/app/modals/keymap, the four seats of one gesture; the `views.py` help bullet counted as `doc` (notice declared in §2) |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_templates.py` (4 arms) + `tests/test_templates_app.py` (5 arms) landed with the product in the same session; 9 passed, 2.17s (`evidence/inc001b-run.log`) |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | the store's lenient read — the 4 store arms, mutation-proven (M15) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M13 executed (`1 failed, 4 passed`); transcript `evidence/mutations.log`; restore sha256 `all OK`; the base-tree RED (collection fails on the new files' imports) declared |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above); B2/B3 did NOT fire |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b — `human:coordinator` · PASS-WITH-NOTES 0 HIGH (F1 minor in `02-review.md`) |
| 7 | No file from another lane touched | all | ✓ | one lane, one brief; the two sessions never overlapped a file (the first wrote nothing) |
| 8 | Frozen interfaces untouched | all | ✓ | `present_project_id`, the milestones undo pattern, `help_usage`'s signature, the LinkPicker chrome, `BOARD_ACTIONS`'s shape, and `T`'s seat are pre-batch bytes (A3 probe) |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | three absences — the unmoved-seat census, the no-dates tuple, the no-resurrection count — each with its positive control and its synthetic fixture |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | M13/M14/M15 per-node (6 node-kills total, 0 SURVIVED, the GREEN arms named each time); transcript + restore digest cited |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) — pytest, the README census, the stop-gate seat census, the arm-resolution probe |
| 13 | **Correction population** declared | all | ✓ | 1 correction — T→I — enumerated before the first site was edited, positive + negative sets named |
| 14 | **Emitted-form assertion** declared | all | ✓ | 6 artifacts — the painted picker rows, the rendered toast bytes (insert/refusal/empty), the help bullet, the README row |
| 15 | **Independent review** names somebody | all | ✓ | §4b — `human:coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 5 artifacts at the evidence home + the two new test files' digests cited beside the table |
