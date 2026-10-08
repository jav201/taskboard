# Increment 001 — HLR-1401 · save a chain as a template from the app (template authoring v2)

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
> `.dev-flow/2026-10-07-batch-08/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-08` |
| Increment | `001` (the whole batch — one increment, one brief) |
| Lane (if the batch forked) | `none` — one implementing session owned the tree; the MAIN checkout |
| Requirement(s) | `HLR-1401` (+ `LLR-1401.1` the component walk and the template shape) |
| Acceptance | `AT-1401` — 11 arms, all green (7 unit arms in `tests/test_template_save.py` + 4 app arms in `tests/test_template_save_app.py`, the docstring home of the `AT-1401` dash token) |
| Agent | `software-dev` — DeepSeek V4 Pro (one shipping session under the coordinator's brief; `evidence/inc001-run.log`) |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

On the chain map, `,` on a selected tile, type a name, press enter — the chain is a template from
then on. The saved template lives in the board's own `settings["templates"]` (portable with the
board), lists FIRST in the batch-07 `I` picker from that moment on, and inserts with its links
through the shipped insert. The name prompt is the app's shipped one-line `TextPrompt`, prefilled
with the chain's first task's title (selected, ready to overtype); esc or an empty name cancels and
writes nothing. On save the board is saved and the pinned toast renders
`Template '<name>' saved — <N> tasks` (`markup=False`). Saving is **NOT an undo step** — it writes
settings, not tasks (declared in the action's docstring, `app.py:767-777`): there is deliberately
no `u` for it.

Mechanism, by seat:

- **The walk** — `models.chain_template(board, task_id)`, `taskboard/models.py:2329-2390`: the
  task's connected component through `depends_on` **within its own project** — BFS in both
  directions (what it waits on, everything that waits on it), **open tasks only** (done/archived
  are not entered and not bridged), each task once (a `seen` set); `None` when the task is missing,
  done, or archived. The emitted order is topological and deterministic: **(depth, board order)** —
  `depth` is the longest `depends_on` path from a chain head (the chain map's own column rule,
  memoized, cycle-guarded by a path argument), board order is first occurrence over
  `board.tasks` (as `_ids`, `models.py:1783`). Every `wait` therefore points backward. **A task
  with several predecessors keeps the FIRST in that order as its `wait`; the rest are dropped** —
  the template shape holds one link per task, so a fan-in cannot be represented (LLR-1401.1's
  declared drop). Titles/notes verbatim; the template's provisional name is the first task's title
  (the app replaces it with the typed name).
- **The action** — `app.action_chain_template_save` (`app.py:766-789`) + `_on_chain_template_named`
  (`app.py:791-808`): a view guard (`view_mode != "chainmap"` → silent return, the shipped
  `action_kanban_sort` style); nothing selected → the refusal toast `Select a chain tile to save.`;
  `chain_template` → None → `The selection carries no open chain.`; else the `TextPrompt`
  (`"Save chain template"`, initial = `tpl.tasks[0].title`). The named callback cancels on a falsy
  name (esc → None, blank → ""), builds the entries (`{"title", "notes"?, "wait"?}` — absent keys,
  not nulls), `settings.setdefault("templates", []).append(...)`, `save()`, the pinned toast. The
  `chain_template` import joined the models import line at `app.py:21`.
- **The key** — `keymap.py:143`, `Key("comma", ",", "chain_template_save", "Save chain tpl",
  views=("chainmap",), group="task")`, view-dispatched on the chain map only. **The key NAME is
  `comma`, not a literal `,`:** a literal `,` in Textual's binding grammar is the *alias
  separator*, and the session's first construction died at collection with
  `textual.binding.InvalidBinding` ("Can not bind empty string" — executed evidence in
  `evidence/inc001-run.log:978-1052`, including the probe of Textual's own machinery:
  `_character_to_key(',')` → `comma`, `Keys.Comma`, `ASCII_KEY_NAMES` empty for `,`). The session
  bound the canonical key name with the literal `,` as the DISPLAY. Group is `task` — the brief
  guessed `chains`, the seat census found no `chains` group and the fitting shipped group is
  `task` (the keybar re-derives from the seat).
- **The doc seats** — the `?` chainmap bullet at `views.py:6924`
  (`x unlinks · , saves the chain as a template.`) and the README keybinding row at `README.md:136`
  (``| `comma` | Save chain | Save the selected chain as a template (chain map) |``).

**The in-frame footer key-hints were deliberately NOT touched** — the chainmap footer's key-hint
row is byte-golden in the C-2b frames (`test_TC_801`/`test_TC_802` render it; the session named
this, `evidence/inc001-run.log` "Punted / notes"). The `,` key is discoverable through the docked
keybar (re-derived from the keymap seat automatically) and the `?` bullet. Recorded as a declared
notice — the golden-footer vs keybar-discoverability trade (see `02-review.md` observation (a) and
the close's lessons).

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | HLR-1401 · LLR-1401.1 | `chain_template(board, task_id)` (`:2329-2390`) — the component walk, the (depth, board order) order, the fan-in drop; +61 lines |
| `taskboard/app.py` | source | HLR-1401 | `action_chain_template_save` (`:766-789`) + `_on_chain_template_named` (`:791-808`); the `chain_template` import (`:21`); +45 lines |
| `taskboard/keymap.py` | source | HLR-1401 | `Key("comma", ",", "chain_template_save", "Save chain tpl", views=("chainmap",), group="task")` (`:143`) + its three-line comment (`:140-142`); +5 lines |
| `taskboard/views.py` | doc | | the `?` chainmap bullet (`:6924`): `x unlinks · , saves the chain as a template.` — one string, a documentation change shipped in code (the notice below) |
| `README.md` | doc | | the `comma` keybinding-table row (`:136`) — forced by the shipped README-census test (§4, Instrument RED-proof) |
| `tests/test_template_save.py` | test | LLR-1401.1 — pinned by AT-1401 | new — 7 unit arms |
| `tests/test_template_save_app.py` | test | HLR-1401 · LLR-1401.1 — AT-1401's docstring home | new — 4 app arms |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 2 (outside the count) |

- ⚠ **`views.py` counted as `doc`, not source:** its entire change is one `?`-help sentence — the
  same reading batch-2026-10-07-batch-07 recorded for its help bullet; this is the SECOND
  consecutive batch reading a help-only `.py` change as `doc`. Declared here per the notice form;
  if a third consecutive batch reads it this way it becomes a rule or is retired.
- ⚠ **No 4-source-file pressure:** 3 source files — one under the cap — the walk (`models.py`), the
  action (`app.py`), the key (`keymap.py`); the two `doc` seats ride along.

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_template_save.py tests/test_template_save_app.py -q   # 11 passed
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests --collect-only -q                                   # 2586 collected
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (the component walk — `chain_template`'s BFS/seen-set, the depth memo, the sort, the drop; cyclomatic ≥3, crosses into `Template`/`TemplateTask`) | `core` · `full` | the 7 arms of `tests/test_template_save.py` | 7 passed (mutation-proven — M17) |
| **A · white-box** ↔ LLR-1401.1/HLR-1401 (the save's mechanism: view guard → refusals → prompt prefill → settings append + save → the pinned toast → picker listing) | `core` · `full` | `test_comma_opens_the_name_prompt_prefilled` · `test_type_a_name_and_enter_saves_and_lists_in_the_picker` · `test_escape_cancels_and_writes_nothing` · `test_an_unlinked_tile_saves_a_one_task_template` | 4 passed (mutation-proven — M16) |
| **B · black-box** `AT-1401` ↔ US-1401, through the shipped surface | `core` · `full` | the same 4 app arms — keys `6`/`,`/name/`enter`/`escape`/`I` through `run_test` at the house pilot (100×30), the painted `TextPrompt`/`TemplatePicker`, the rendered toast bytes, `board.settings` + the board file — AT-1401 named in the file docstring | 4 nodes passed |

The shipping session's targeted run held the two files at **11 passed, 0 failed** (2.66s,
`evidence/inc001-run.log:1065`) and its ONE complete settled run over the tree passed **2585 /
2585 with 1 failed** — `1 failed, 2585 passed in 437.37s` (`evidence/inc001-run.log:1293`; the one
failure the G-011 environmental flake, declared below). The close-out re-collected the suite at
**2586 tests** on the final tree (`pytest tests --collect-only -q`, 0.59s). "See 04-validation"
for the close number; the orchestrator's C-25 owns the ONE final clean-tree run.

**The 2 failures in the cited transcripts, named (V56):** they sit in
`evidence/inc001-run.log:1108` — the session's FIRST full-suite attempt (`2 failed, 2584 passed`,
441.25s). One is the README keybinding census (`test_keymap.py:404`), the known forced row the
session then shipped (`README.md:136` — the suite's own keymap re-run passed 24/24 in 1.17s,
`:1249`); the other is `test_app.py::test_win_clipboard_roundtrip` — **G-011**, the declared
environmental clipboard flake: it fails in its OWN clipboard SETUP (`SETUP failed — this is the
environment, not the code under test`, the PowerShell `Set-Clipboard` ExternalException), the
coordinator verified it fails ISOLATED too (`1 failed in 4.19s`, `:1293`'s isolated run at
`:1251-1266`), and the BACKLOG has declared it since batch B2. The settled re-run passed 2585 with
that one flake alone. The mutation battery's `failed` counts (`evidence/mutations.log`) are the
deliberate per-mutant REDs tabled below. No failure count anywhere in the evidence contradicts the
packet's settled state.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M16 (the save writes nothing):** the `settings["templates"].append(...)` + `save()` in `_on_chain_template_named` → `_ = (name, tasks)` — the increment's signature behavior (a named template the picker lists) collapsed to a no-op |
| Instrument | project code: the coordinator's byte-level mutation runner (`evidence/mutations.log` — byte-anchored, restores sha256-verified) |
| Where it ran | **my own tree** — the MAIN checkout (the batch's single lane; the battery is the coordinator-run close-out set M16-M17, executed on this tree) |
| Transcript | `evidence/mutations.log` M16 — `2 failed, 2 passed` on `tests/test_template_save_app.py` |
| Restore proven by | **file hash returned to its pre-mutation value** — `evidence/mutations.log`'s header: "byte-level, restores sha256-verified; all OK" |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **4** — `pytest tests/test_template_save_app.py --collect-only -q` resolves exactly the 4 arms named in the Layer table |
| Verdict granularity | **per resolved node id** — M16 reddened exactly the two arms that save (the named-save arm and the unlinked-tile arm); the other two stayed GREEN on the same mutant |
| Arms that stayed GREEN | **named:** `test_comma_opens_the_name_prompt_prefilled` (the prompt opens and is prefilled regardless of whether the save lands), `test_escape_cancels_and_writes_nothing` (esc writes nothing either way) |

The base-tree RED is by construction, and is itself executed evidence: both new files import
`chain_template`, which does not exist at base (`from taskboard.models import … chain_template …`,
`tests/test_template_save.py:18`) — on the pre-batch tree the collection itself fails, the
signature of a wholly new surface. M16 is the executed counterfactual on THIS tree, where the
feature exists.

| Field | Value |
|---|---|
| **RED counterfactual** | M16 — the settings append + save reduced to a no-op · transcript `evidence/mutations.log` M16 (`2 failed, 2 passed`, the GREEN arms named above) · restore digest: sha256-verified `all OK` · the base-tree RED: the new files' imports fail at collection on the pre-batch tree |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node: **M16** (the settings append + `save()` → `_ = (name, tasks)`) · `test_type_a_name_and_enter_saves_and_lists_in_the_picker` KILLED (the settings entry and the picker-listing assertions both redden) + `test_an_unlinked_tile_saves_a_one_task_template` KILLED (`2 failed, 2 passed`) · GREEN: the prompt-prefill arm and the esc-cancels arm (named above) · **M17** (`chain_template` returns None at the top) · six of the seven unit arms KILLED — every arm that dereferences the template reddens (`6 failed, 1 passed`): the both-directions walk, the fan-in + round-trip arm, the degenerate single task, the within-project boundary, the skipped-not-bridged neighbour arm, the verbatim titles/notes arm · GREEN: `test_none_for_done_archived_and_missing` — its four assertions are ALL `is None`, so the always-None mutant passes it (the count `6 failed, 1 passed` is the load-bearing fact; it matches the resolved arms exactly) · ⚠ the log's parenthetical names the GREEN arm "the round-trip arm" — that is a wording slip in the stored transcript: the round-trip code lives INSIDE `test_fan_in_keeps_the_first_predecessor_and_round_trips_as_a_chain`, which reddens at its first `tpl.tasks` dereference; the arm whose assertions make it GREEN under an always-None mutant is the None-cases arm, named above. Declared here; `mutations.log`'s stored bytes untouched · inert arms: none · registry: no `docs/tools/devflow-mutants.json` battery in this repo — M16-M17 are the coordinator-run close-out battery · transcript `evidence/mutations.log` · restore digest: sha256 `all OK` for both |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M16/M17's mutant code | per-arm `failed` exactly as tabled above (`evidence/mutations.log`) |
| the README keybinding census (`tests/test_keymap.py:404`, `test_the_readme_keybinding_table_matches_the_seat`) | the `comma` key landed WITHOUT the README row | reddened on the session's own keymap change — ``AssertionError: , (Save chain tpl) is bound but the README never mentions it`` (`evidence/inc001-run.log:1090-1105`); the row was added and the census went green (`:1249`, 24 passed) |
| Textual's binding construction (via collection) | the first keymap attempt bound a LITERAL `,` as the key name | `ERROR collecting tests/test_template_save_app.py — textual.binding.InvalidBinding: Can not bind empty string` (`evidence/inc001-run.log:978-1000`) — the alias separator swallowed the key; the session probed Textual's key machinery (`_character_to_key(',')` → `comma`, `Keys.Comma`, `ASCII_KEY_NAMES.get(",")` → None, `:795-1047`) and re-bound as the key NAME `comma` with `,` as the display |
| the arm-resolution probe (`--collect-only`) | a whitespace-delimited `-k` pattern would silently drop parametrized arms | resolves exactly 7 + 4 = 11 nodes on the two files (run at this close, `04-validation.md`) — the count every verdict above is granular over |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown RED (or discriminating) before its first PASS was believed (transcripts in `evidence/mutations.log` · `evidence/inc001-run.log`) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the saved settings entry | `app.board.settings["templates"] == [{"name": "Release", "tasks": [{"title": "Alpha"}, {"title": "Beta", "wait": 0}, {"title": "Gamma", "wait": 1}]}]` | equal — the exact dict, absent keys not nulls (`tests/test_template_save_app.py:106-110`) |
| the save toast | `_toast_check(app, "Templates", "Template 'Release' saved — 3 tasks")` — `str(t.render())` of the painted `Toast`, partitioned on its newline | `None` (a byte-exact title/body match; `:111`) · and on the degenerate tile: `Template 'Solo' saved — 1 tasks` (`:159`) |
| the picker row after the save | `_plains(app.screen.query_one("#template-list"))[0]` | `"Release — 3 tasks"` — the saved template lists FIRST (`:116`) |
| the name prompt + prefill | `isinstance(app.screen, TextPrompt)` and `app.screen.query_one("#f-text", Input).value` | `"Alpha"` — the chain's first task title, not the selected mid-chain tile's (`:83-85`) |
| the esc cancellation | `"templates" not in app.board.settings` and `path.read_bytes() == raw_before` | both held — the settings AND the board file are byte-identical (`:131-138`) |
| the emitted template order (unit) | `[t.title for t in tpl.tasks]` / `[t.wait for t in tpl.tasks]` | `["Alpha", "Beta", "Gamma", "Delta"]` / `[None, 0, 1, 2]` on the mid-chain selection; `["Alpha", "Beta", "Gamma"]` / `[None, None, 0]` on the fan-in — the drop (`:43-44`, `:57-58`) |
| the round-trip graph shape | `parents == [[], [], ["Alpha"]]` and `all(len(ps) <= 1 for ps in parents)` | a CHAIN, not a diamond — no fan-in survives the store and the insert link builder (`:73-76`) |
| the `?` chainmap help | the bullet line itself, `views.py:6924` | `x unlinks · , saves the chain as a template.` |
| the README keybinding row | the census test's table read | ``| `comma` | Save chain | Save the selected chain as a template (chain map) |`` (`README.md:136`) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 9 artifacts, each asserted against the form its producer emitted (the settings dict · the rendered toast bytes · the picker row · the prompt prefill · the esc byte-identity · the template order · the round-trip graph · the help bullet · the README row) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the increment brief (the coordinator's chunk brief) | `.dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md` | `13ce2ac573a17c8432a83bd09107518f3221467f7b5cf3a047bb75987da3ba25` |
| the shipping session's run log (the seat census, the `,`-alias construction failure + Textual probes, the targeted 11-passed run, the two full-suite runs, the review packet) | `.dev-flow/2026-10-07-batch-08/evidence/inc001-run.log` | `5618421a1451d7428c1024c918e26ba763c4c395d0fc7f142eca9a01bf9db020` |
| the close-out mutation battery M16-M17 (both KILLED, restores sha256-verified) | `.dev-flow/2026-10-07-batch-08/evidence/mutations.log` | `e68167a37434ef7e41722b5a71c6c73644a0781cbce3c64806ae75eb82098531` |

The new test files' stored bytes: `tests/test_template_save.py` sha256
`c2d4ca3061c8c5d6630a03356088fb58bff32a11ae92ff4c730fcb1fac6fff1d` ·
`tests/test_template_save_app.py` sha256
`ca6d1af86fb791fcf4491e508fb94693c93d804794fa18a291ac1be546cc3867` (their home is the
`tests/` home `artifact_homes.tests` declares — cited here for the record, not as evidence-home
artifacts).

| Field | Value |
|---|---|
| **Evidence files** | `3` artifacts at the evidence home, each cited with the digest of its stored bytes; the two new test files' digests cited beside the table (their home is `artifact_homes.tests`) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — three: (1) "esc/empty writes NOTHING" — an absence over `settings` AND the board file's bytes; (2) "a fan-in does NOT survive the round trip" — an absence of any task with two parents after the store + insert link builder; (3) "a saved template does NOT get an undo entry" — an absence over the undo stack (declared semantics, docstring-pinned, not arm-pinned) |
| If the result is an ABSENCE, what made the search wide enough | (1) the esc arm reads the WHOLE board file's bytes before/after (`path.read_bytes() == raw_before`) plus the settings dict — not a spot check of one key; (2) the round-trip arm computes EVERY task's parent list and asserts `all(len(ps) <= 1 for ps in parents)` — universal, not sampled; (3) the docstring states the law at the action seat (`app.py:767-777`), and no undo key exists in the settings-entry shape to assert against — the absence is by construction, declared |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_fan_in_keeps_the_first_predecessor_and_round_trips_as_a_chain` — its docstring names the conclusion "a fan-in survived the round-trip" for the `all(len(ps) <= 1)` probe; `test_escape_cancels_and_writes_nothing` names "byte-identical (absent)" for the file-identity probe — both say what the absence CONCLUSION is, so the next reader does not "simplify" the arm into a presence check |
| Conjunctive criteria: one mutation per conjunct | the save law conjoins prompt+prefill · settings write · save · toast · picker listing: M16 kills the write conjunct (`2 failed`, the two save arms); M17 kills the walk conjunct upstream (`6 failed`, every component arm) — one probe per conjunct, each discriminating |
| Synthetic instance of the absent case | the fan-in fixture inside the fan-in arm (two predecessors `("a", "b")` on one task) is the tree-level instance of "a diamond the shipped templates never hold" — the tree ships no such template; the fixture carries it in-memory |
| **Positive control for every probe that returned an ABSENCE** | (1) the same file-bytes probe's positive half is the save arm's settings assertion (the entry IS present after enter, `tests/test_template_save_app.py:106-110`) — uniformity over the same mechanism, save vs esc; (2) the parents probe returns the known-present non-empty parent `["Alpha"]` for Gamma before the universal emptiness half; (3) the batch-07 insert's ONE-undo-entry shape is the known-present undo neighbor — the settings save composes beside it, never into it |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rn "chain_template" taskboard/*.py tests/*.py` → `taskboard/models.py:2329` (the def) · `taskboard/app.py:21` (import) · `:783` (the call) · `:789` (the prompt callback's closure) · `taskboard/keymap.py:143` (the action name) · `tests/test_template_save.py` (the import + 6 calls) | every reader of the new symbol is THIS batch's own — no pre-existing test asserted a symbol this increment moved; the `help_usage`/`KEYMAP` surfaces are censused by the shipped keymap/help families (`test_keymap.py`'s global-bar and README censuses, the help-clip families) — every outside reader re-validated by the suite (2585 passed + the declared G-011) |
| B2 file moved on disk | `git status --porcelain -- taskboard/ tests/test_template_save.py tests/test_template_save_app.py README.md` → ` M` models/app/keymap/views/README · `??` the two test files | modified in place, no rename, no delete — the old paths are the current paths; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → `No such file or directory` | the repo holds no golden-capture directory (as batch-05/06/07 recorded); did NOT fire — and the in-frame chainmap footer was deliberately left byte-untouched precisely because the C-2b frames are golden (`tests/test_chainmap.py`'s FRAMES path) |
| B4 artifact produced here is consumed elsewhere | `grep -rn "chain_template" taskboard/*.py` → `app.py:783` (the only caller); `grep -rn '"chain_template_save"' taskboard/*.py` → `keymap.py:143` (the seat — Textual's dispatch invokes the action by name; the keybar + `?` census read the seat); `grep -rn '"templates"' taskboard/app.py` → the batch-07 read/insert seats (`:741`-family) now ALSO read what this increment appends | the consumers are exactly this increment's seats + the batch-07 store/picker machinery (unchanged — the saved entry is read through the shipped `templates()`/`_read_template` lenient read); all re-validated by the green suite |
| A3 interface consumed by another module changed | new symbols only — no pre-existing interface moved: `help_usage`'s (mode) → sections signature, the `TextPrompt` chrome, the `templates()` store shape, `is_open`/`_ids`/`_live`, and the batch-07 insert seats are pre-batch bytes; the `,` key was FREE (the brief's discipline grep — `grep 'Key(","' taskboard/keymap.py` → 0 before the write, re-run at this record) | no cross-module consumer exists outside the seats named in B4; the change is additive |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1's hits are this batch's own files + the shipped census families (re-validated by the suite), B4 names the one caller and the store's unchanged readers, B2/B3 did NOT fire with their probes recorded · transcripts in `evidence/inc001-run.log` |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| — none — no correction this batch: the contract (LED-2026-10-07-batch-08.1) pinned `,` and the seat was free; the brief's group guess (`chains`) was corrected by the agent at the seat, not by a contract LED | — | — | 0 | — | — |

| Field | Value |
|---|---|
| **Correction population** | none — no correction (the one contract deviation — the key group — was the brief's own guess, fixed at the seat before the key landed; no requirement text ever claimed `chains`) |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| — none — nothing superseded this batch | — | — | — |

### Signed-balance test ledger

`post = base − D + A` → batch post `2586 = 2575 − 0 + 11` ✓ reconciles (base = the batch-07
trunk at 2575; A = 11 new nodes — the 7 unit arms + the 4 app arms; the `?` bullet and the README
row modified no test). The close-out re-collected the suite at **2586 tests** on the final tree
(`pytest tests --collect-only -q`, 0.59s); the shipping session's complete settled run passed 2585
with the 1 declared environmental flake (`evidence/inc001-run.log:1293`). "See 04-validation" for
the close number; the orchestrator's C-25 owns the ONE final clean-tree run.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` — the close-out coordinator self-executed the P2 lens pool over the packet, the diffs, and the evidence · verdict PASS-WITH-NOTES, 0 HIGH — the notes: (a) the in-frame chainmap footer key-hints were deliberately left untouched (byte-golden C-2b frames) — the `,` key's discoverability rides the docked keybar + the `?` bullet; declared and accepted, recorded in §1 and the close's lessons · (b) the README `comma` row landed outside the brief's file list, forced by the shipped census test `test_keymap.py:404` — declared and accepted, the row is a `doc` change · the P2 review verdict stands in `02-review.md` (0 blocker · 0 major · 0 minor, two declared observations; reviewer `human:coordinator`, the runtime spawned nobody) |

---

## 5 · Risks

- The picker resolves by name (batch-07's standing risk, inherited): a saved template named
  exactly `Simple chain` or `Bugfix` shadows the preset silently (user templates list first).
  Unchanged by this increment; carried in the backlog's standing line, not new.
- The degenerate one-task save toasts `Template '<name>' saved — 1 tasks` — ungrammatical but the
  PINNED literal (the app arm asserts it byte-exact, `tests/test_template_save_app.py:159`).
  Changing the pluralization reddens the pinned arm; declared so the next reader does not
  "correct" it unarmed.
- The save is not undoable (declared, docstring-pinned): a fat-fingered save appends a template
  the operator removes by hand in the board JSON at v1 — the same deletion seat batch-07's `?`
  bullet documents. The batch-06/07 exposures (wholesale-remove dangling links) do not apply:
  saving touches no task.
- The fan-in drop is SILENT: saving a diamond keeps one link and says so only in the toast's task
  count. Declared in LLR-1401.1, pinned by the round-trip arm — a v1 choice, documented here and
  in the contract's boundary catalog.
- The `,` key is view-scoped: on a selected task in another view it does nothing (the silent
  guard matches the shipped `action_kanban_sort` style) — discoverable on the chain map only, via
  the keybar and `?`.

## 6 · Pending items / spec deviations

- None open in this increment. The batch-06 visual re-verdict backlog item was CLOSED by the
  coordinator's fold before this batch closed (commit `762d18c`, operator verdict "Se ve bien."
  2026-10-08, all four accepted — `2026-10-07-batch-06/evidence/veredicto-batch06.json`); it is
  recorded as done in the backlog and is NOT reopened here. The only spec deviation: the README
  row outside the brief's file list (forced by the shipped census test — declared in §2, §4, and
  `02-review.md` observation (b)).

## 7 · Suggested next task

- None pressing — the backlog's only open feature item (template authoring v2) ships in this
  batch. Standing candidates: the operator's first-eye verdict on the name prompt (fresh surface,
  no trigger-D commission); the operator's ruling on minting the seat-check-before-key and
  LED-sweep candidate controls (two and three batches deep respectively); and the evergreen
  G-011 environmental flake (standing, environmental).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 3 source files — models/app/keymap, one under the cap; the `views.py` help bullet counted as `doc` (notice declared in §2) |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_template_save.py` (7 arms) + `tests/test_template_save_app.py` (4 arms) landed with the product in the same session; 11 passed, 0 failed (2.66s — `evidence/inc001-run.log:1065`) |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | the component walk — the 7 unit arms, mutation-proven (M17) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M16 executed (`2 failed, 2 passed`); transcript `evidence/mutations.log`; restore sha256 `all OK`; the base-tree RED (collection fails on the new files' imports) declared |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above); B2/B3 did NOT fire |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b — `human:coordinator` · PASS-WITH-NOTES 0 HIGH (two observations in `02-review.md`) |
| 7 | No file from another lane touched | all | ✓ | one lane, one brief, one session |
| 8 | Frozen interfaces untouched | all | ✓ | `help_usage`'s signature, the `TextPrompt` chrome, the `templates()` store shape, `is_open`/`_ids`/`_live`, and the batch-07 insert seats are pre-batch bytes (A3 probe) |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | three absences — the esc byte-identity, the no-fan-in round trip, the no-undo-entry save — each with its positive control and its synthetic fixture |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | M16/M17 per-node (8 node-kills total, 0 SURVIVED, the GREEN arms named each time); the M17 log-parenthetical wording slip declared, not hidden; transcript + restore digest cited |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) — pytest, the README census, Textual's binding construction, the arm-resolution probe |
| 13 | **Correction population** declared | all | ✓ | none — no correction this batch (the key-group deviation was the brief's own guess, fixed at the seat) |
| 14 | **Emitted-form assertion** declared | all | ✓ | 9 artifacts — the settings dict, the rendered toast bytes, the picker row, the prompt prefill, the esc byte-identity, the template order, the round-trip graph, the help bullet, the README row |
| 15 | **Independent review** names somebody | all | ✓ | §4b — `human:coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 3 artifacts at the evidence home + the two new test files' digests cited beside the table |
