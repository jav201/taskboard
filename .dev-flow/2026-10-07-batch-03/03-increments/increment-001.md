# Increment 001 — HLR-901 · HLR-902 · K2-1's filter half · The safe fixes

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
> `.dev-flow/2026-10-07-batch-03/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-03` |
| Increment | `001` |
| Lane (if the batch forked) | `none — one lane per increment (§2.8 of the contract)` |
| Requirement(s) | `HLR-901` · `HLR-902` (+ `LLR-901.1` · `LLR-902.1`) · K2-1's search-filter half of `LLR-903.1` |
| Acceptance | `TC-901` · `TC-902` (×5 params) · `AT-901` · `AT-902` · `AT-903[1_legend]` (search half) — 12 nodes, all green |
| Agent | `software-dev` — DeepSeek V4 Pro (product, chunkA) ∥ DeepSeek V4.1 Flash (tests, chunkB), orchestrated; review folds by the coordinator |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

A failed link migration can no longer lose the board or re-run on a false mark: the failure path
restores the board bytes and the migration mark FIRST, removes its own backup/log best-effort in
a nested guard that never raises, and surfaces the ORIGINAL failure via `result.error`
(`taskboard/models.py:1618-1633`, the offer's order). A hand-edited board with `"title": 5`
(or a list) now opens instead of crashing a string-only render path: `Task.from_dict` coerces at
the load boundary — `str(value)` for scalars, the shipped `Untitled` for containers and null
(`taskboard/models.py:782-791` `_coerce_title`, `:875-877` the from_dict call). The kanban `?`
legend now reads the FILTERED board the screen draws when a search query is active
(`taskboard/app.py:579-584`). The tests agent landed the pins and folded the one obsolete
expectation (`tests/test_cleanup.py`, 12 nodes; `tests/test_team_sync.py:184-185` now expects
`["Good", "123"]` — a coerced foreign task is kept, not skipped).

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | HLR-901 · LLR-901.1 · HLR-902 · LLR-902.1 | `_coerce_title` (:782-791); `Task.from_dict` coercion (:875-877); the restore-first error handler (:1618-1633) + docstring (:1589-1594) |
| `taskboard/app.py` | source | LLR-903.1 (K2-1 search half) | the kanban+search `?`-legend branch passing `self._view_board()` (:579-584) |
| `tests/test_cleanup.py` | test | LLR-901.1 · LLR-902.1 · LLR-903.1 (K2-1's search half) — pinned by TC-901 · TC-902 · AT-901 · AT-902 · AT-903 | new — 12 nodes (TC-901 + happy arm, TC-902 ×5, AT-901, AT-902, AT-903 ×4 arms; the 4 render arms RED here by design — increment 002's counterfactual, captured in chunkB-run.log) |
| `tests/test_team_sync.py` | test | HLR-902 | the folded expectation :184-185 — `["Good", "123"]` |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 (outside the count) |

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_cleanup.py -q           # 12 passed
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_team_sync.py -q         # 16 passed (the folded expectation)
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (`_coerce_title` — None/list/dict/try-except ≥3; `run_link_migration`'s error path crosses the save/restore seam) | `core` · `full` | `_coerce_title` · the error handler | 2 units — mutation-proven below |
| **A · white-box** `TC-901` · `TC-902` ↔ LLR | `core` · `full` | TC-901 (+ its happy-path arm) · TC-902 ×5 params | 6 nodes passed |
| **B · black-box** `AT-901` · `AT-902` ↔ story, through the shipped surface | `core` · `full` | AT-901 (app exit names the original failure) · AT-902 (the `5` board opens) · AT-903[1_legend] (search half, through the running app) | 3 nodes passed (arm 1's fold half + arms 2-4 RED by design here — increment 002 owns them) |

Suite at the increment's close baseline: `tests/test_cleanup.py` → **12 passed, 0 failed** and
`tests/test_team_sync.py` → **16 passed, 0 failed** (`evidence/inc001-mutations.log`, BASELINE
section). The workers' runs: chunkA held the suite at 2528 passed with exactly 1 failed — the
stale team_sync expectation S-9 invalidated, since folded to `["Good", "123"]`
(`evidence/chunkA-run.log`); chunkB ran 8 nodes green + the 4 RED-by-design render arms, its
intermediate runs recording up to 5 failed while the arms were being settled — every failure
line in the cited bytes is a deliberate counterfactual capture or a since-folded stale
expectation, and each is named in this paragraph (`evidence/chunkB-run.log`). The orchestrator's
full close suite — 2541 passed, 0 failed — is recorded in `04-validation.md` and `05-close.md`
(orchestrator-owned, C-25).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M1 (S-9):** `_coerce_title`'s container branch returned `str(value)` (the repr) instead of `Untitled` — the pre-P2 behaviour. **M2 (S-4):** the error handler's unguarded backup/log `unlink` moved BEFORE `_set_links`/mark restore — the pre-S-4 order |
| Instrument | project code: the coordinator's own hand via a scripted exact-string replacement; the restore checked by sha256 |
| Where it ran | **my own tree** — the MAIN checkout (no other session reads it; the present-e worktree is this batch's parallel track and was not touched) |
| Transcript | `evidence/inc001-mutations.log` — M1: `2 failed, 3 passed` (TC-902's list/dict arms RED — `assert "['x']" == 'Untitled'`); M2: `1 failed` (TC-901 — the refusing unlink escapes the handler) |
| Restore proven by | **file hash returned to its pre-mutation value**: `sha256(taskboard/models.py)` → `0ee9326a2bdbdcf333d90fb7e30322483aaa8a0a5793a3dc6600793dfc80fece` before, after M1, and after M2 (transcript); re-run green after each restore |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **12** — `pytest tests/test_cleanup.py --collect-only -q` resolves 12 node ids (TC-901 ×1 [+ happy arm inside], TC-902 ×5 [int/list/dict/null/bool], AT-901, AT-902, AT-903 ×4 [1_legend, 2_rule_only, 3_fold, 4_views]) |
| Verdict granularity | **per resolved node id** — M1 reddened exactly `test_TC_902_a_non_text_title_coerces_at_the_boundary[list]` and `[dict]` (the int/null/bool arms stayed GREEN); M2 reddened `test_TC_901_...` alone |
| Arms that stayed GREEN | M1: TC-902[int/null/bool], TC-901, AT-901/902 — the scalar coercion is untouched by a container mutation. M2: every node but TC-901 — the order mutation touches only the failure path |

| Field | Value |
|---|---|
| **RED counterfactual** | M1 — `_coerce_title`, the `isinstance(value, (list, dict))` branch, returns `str(value)` instead of `"Untitled"` · M2 — `run_link_migration`'s `except OSError` block, the unguarded `unlink` loop moved ahead of the restore · transcripts at `evidence/inc001-mutations.log` · restore digest `sha256 0ee9326a2bdbdcf333d90fb7e30322483aaa8a0a5793a3dc6600793dfc80fece` |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node: M1 · TC-902[list] KILLED (`assert "['x']" == 'Untitled'`), TC-902[dict] KILLED (`assert "{'a': 1}" == 'Untitled'`), all other arms GREEN (named above) · M2 · TC-901 KILLED (the cleanup `PermissionError` escapes — `1 failed`), all other arms GREEN · inert arms: none · registry: no `docs/tools/devflow-mutants.json` battery in this repo — the two named mutants are the increment's own counterfactuals · transcript `evidence/inc001-mutations.log` · restore digest `0ee9326a…fece` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M1's mutant code | `2 failed, 3 passed` on TC-902 — per-node, the list/dict arms only |
| `pytest` (the suite) | M2's mutant code | `1 failed` on TC-901 — the escaping cleanup exception |
| the refusing-unlink monkeypatch (`tests/test_cleanup.py:92-110`) | refuses ONLY the migration's own backup/log names | M2: the refusal escaped the handler (the harness saw the exception); at baseline the same refusal is swallowed best-effort and `result.error` names the original failure |
| `grep` census probes | a nonsense control pattern `_coerce_title_nonsense_control` | `0` files — against `3` for the real probe (`_coerce_title`: test_cleanup/test_link_migration/test_team_sync) — the probe distinguishes presence from absence |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown RED before its first PASS was believed (transcripts in `evidence/inc001-mutations.log`) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the saved board file after a load+save of the `"title": 5` board | `Board.load(p); b.save(); '"title": "5"' in p.read_text(encoding="utf-8")` | `True` — the file's bytes carry `'["title": "5",']`; the coerced string is what lands on disk, not just what the loader holds |
| `result.error` on the failing migration | TC-901's assertions on the returned string: `"the original save refused" in result.error`, `"cleanup refused" not in result.error` | both hold — the error names the original save's basename and the OS's words (the emitted form, not a repr of an exception) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts, each asserted against the form its producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| chunkA run + RED transcript (the product agent's full log) | `.dev-flow/2026-10-07-batch-03/evidence/chunkA-run.log` | `d9a06c0d204cfdfa90f45be299f041de836c1de3fb2ec324a4276635689faba4` |
| chunkB run + the 4 RED-arm transcripts (the tests agent's log) | `.dev-flow/2026-10-07-batch-03/evidence/chunkB-run.log` | `84fdb36879183be878481e55ad94bf0077522a96f784f398eaf8664cab323313` |
| the close-out mutations, reverse census + instrument RED-proof | `.dev-flow/2026-10-07-batch-03/evidence/inc001-mutations.log` | `247d4d658e9fbab547c38ade2fb2f4d5d15d1df0cade18b6efcb6de2ff94488d` |

| Field | Value |
|---|---|
| **Evidence files** | 3 artifacts, each at the declared home and cited with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — "a non-text title never crashes a render" rests on every render path consuming `Board.load` output (no path parsing raw JSON itself) |
| If the result is an ABSENCE, what made the search wide enough | the over-broad property: a render path bypassing `from_dict` would crash on an int title; the guard: TC-902's `render_view` sweep over **every** view (`for mode in VIEWS`, `tests/test_cleanup.py:185-186`) + AT-902 driving the real app through views 1-5 at 118×30 |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_TC_902_...` — its docstring says the sweep is the never-crash conclusion's guard |
| Conjunctive criteria: one mutation per conjunct | M1 (containers read `Untitled`) and the folded team_sync expectation (the foreign task is kept) are the two conjuncts of S-9 — M1 kills the first; the `["Good", "123"]` expectation kills a "skip non-text titles" revert |
| Synthetic instance of the absent case | the hand-built boards in TC-902 (`tests/test_cleanup.py:160-184`) — `"title": 5 / ["x"] / {"a": 1} / null / true` in one bad field at a time |
| **Positive control for every probe that returned an ABSENCE** | the known-present case: the `5` board — the same unmodified sweep renders it and AT-902 sees the task show `5` (a non-absence on a known-present coercion); the census probes' nonsense-pattern controls returned 0 against the real probes' N |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln _coerce_title tests/` → `tests/test_cleanup.py` `tests/test_link_migration.py` `tests/test_team_sync.py` | 3 files — test_cleanup (this batch), test_link_migration (the shipped migration arms — the error path's data surface is unchanged), test_team_sync (the folded expectation — re-ran 16 passed) |
| B2 file moved on disk | `git status --porcelain -- taskboard/models.py taskboard/app.py` → ` M` both | no rename, no delete — the old paths are the current paths; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → no such directory in this repo | the repo holds no golden-capture directory at all; the byte-exact seats this batch touched live in `tests/test_kanban_readable.py` (increment 002's seat, probed there); did NOT fire |
| B4 artifact produced here is consumed elsewhere | `grep -rn MIGRATION_BACKUP\|MIGRATION_LOG taskboard/ tests/` | the constant names did not change — models.py (producer), app.py's undo, the test pins; every reader re-validated by the green suite |
| A3 interface consumed by another module changed | `grep -rn run_link_migration taskboard/` → `app.py:324` the `_migrate_links` call site | signature and `result.error` contract unchanged; the app.py kanban-? branch is a NEW caller input, not a changed interface |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1 3 hits (each re-validated), B4/A3 hits internal to the declared sites, B2/B3 did NOT fire with their probes recorded · transcripts in `evidence/inc001-mutations.log` §REVERSE CENSUS |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| S-4 restore-first | every backlog loose item filed by the reviews | `.dev-flow/BACKLOG.md` "Open — after 2026-10-04-batch-02" lines 43-58 | 6 | S-4 (models.py handler), S-9 (models.py boundary), K2-1 search half (app.py) — this increment; K2-1 fold half, UX2-2, D-623, milestones-in-views — increment 002 | none — all six closed by the two increments |

| Field | Value |
|---|---|
| **Correction population** | 1 correction wave (the six-item backlog tranche), enumerated from the canonical backlog before the first site was edited; every site accounted for across the two increments |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the pre-S-9 raw title seat `title=d.get("title", "Untitled")` | 0 hits for the old one-liner | yes — the only from_dict title seat is the coercing one | `taskboard/models.py:875-877` |
| the pre-S-4 handler order (unguarded unlink before the mark restore) | 0 hits — the `try/except OSError: pass` guard wraps the only unlink loop in the handler | yes | `taskboard/models.py:1626-1632` |
| the superseded team_sync skip (`titles == ["Good"]`) | 0 hits | yes — `tests/test_team_sync.py:184` expects `["Good", "123"]` | `tests/test_team_sync.py:184-185` |

### Signed-balance test ledger

`post = base − deleted + added` → `2541 = 2529 − 0 + 12` ✓ reconciles at the batch level (base = Batch C's 2529 close gate; this increment added the 12 cleanup nodes; the team_sync change modified, not added). The batch-level ledger is summed in `04-validation.md`.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `qa-reviewer` ∥ `ux-reviewer` ∥ `architect` ∥ `security-reviewer` — the P2 lens pool, self-executed by the close-out `coordinator` with the role files (the runtime spawned nobody; that self-execution is named in `02-review.md` per the runtime rule) · iteration 1: qa FAIL, ux FAIL, architect/security PASS-WITH-NOTES — the convergent blockers CL-1..CL-9 folded into the contract (LED .2) and verified there; close-out re-read of the shipped tree: **PASS-WITH-NOTES, 0 HIGH / 2 minor** — every minor named in `02-review.md` with its disposition · the close-out lens transcript: `evidence/close-review.log` |

---

## 5 · Risks

- The dead `isinstance(task.title, str)` guard at `taskboard/team_sync.py:226` (title is always
  text post-load): harmless no-op, left in place — the implementation is frozen; noted as a
  minor in `02-review.md`.

## 6 · Pending items / spec deviations

- None open here — AT-903's four render arms were RED by design in this increment and are closed
  by increment 002 (their RED transcripts are this increment's counterfactual evidence).

## 7 · Suggested next task

- Increment 002 — the render items (K2-1's fold half, D-623, UX2-2, milestones in
  lanes/agenda/focus), `taskboard/views.py`.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 2 source files (models.py · app.py) |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_cleanup.py` 12 nodes landed with the product (chunkB against chunkA's report) |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `_coerce_title` + the error path — mutation-proven (M1/M2) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M1/M2 executed; transcript `evidence/inc001-mutations.log`; restore digest `0ee9326a…fece` |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above); transcript in the log |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b: the P2 lens pool under the coordinator · PASS-WITH-NOTES 0 HIGH / 2 minor |
| 7 | No file from another lane touched | all | ✓ | the disjoint-sets probe (`git diff --name-only HEAD`) — §2.8 of the contract |
| 8 | Frozen interfaces untouched | all | ✓ | `run_link_migration`'s signature/`result.error` contract unchanged (A3 probe) |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | the never-crash sweep's guard + the TC-902 synthetic boards |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | per-node table above; inert arms: none |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) |
| 13 | **Correction population** declared | all | ✓ | the six-item backlog tranche, enumerated before the first edit |
| 14 | **Emitted-form assertion** declared | all | ✓ | the saved board bytes + `result.error`'s emitted string |
| 15 | **Independent review** names somebody | all | ✓ | §4b — the coordinator + the P2 lens pool |
| 16 | **Evidence files** declared | all | ✓ | 3 artifacts with stored-byte digests |
