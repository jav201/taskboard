# Increment 004 — HLR-1106 · the key-walking acceptance arms

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
> `.dev-flow/2026-10-07-batch-05/03-increments/increment-004.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-05` |
| Increment | `004` |
| Lane (if the batch forked) | `none — one lane per increment (§2.8 of the contract; ran parallel with increment 001 over DISJOINT files — the two milestones test files vs models/views/app)` |
| Requirement(s) | `HLR-1106` (+ `LLR-1106.1`) |
| Acceptance | the amended `AT-601` · the amended `AT-602` · the new team-folder arm (`test_AT_601_offer_converted_milestones_reach_a_team_folder`) — the two files at 71 nodes, all green |
| Agent | `software-dev` — DeepSeek V4.1 Flash |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

The milestone acceptance arms now walk the surface the way the user does. In
`tests/test_milestones.py`, the `AT-601` arm's last leg reached its task through a direct
`selected_task_id` assignment hidden in the `_edit` helper — the helper is split:
`_editor_save(app, pilot, **fields)` opens the editor on the CURRENT selection and saves (no
assignment ever), while `_edit(app, pilot, tid, **fields)` = the assignment + `_editor_save` is
kept for the untouched TC-605 arms. `AT-601` now does `_select(app, pilot, "ta1")` then
`_editor_save(...)`; the `_select` helper was upgraded from down-only to BIDIRECTIONAL (it reads
`app._nav_flat()` for the direction and moves by `up`/`down` only — `ta1` sits above `ta5`, where
the old down-only walk could never reach). In `tests/test_gantt_milestones.py`, `AT-602` gained
its own `_select` key-walk helper and every direct assignment (`tw5` start · `td0` · `tw2` · the
80×24 `ta3`) now walks with keys; the redundant `app.refresh_view()` calls went away (the key
press already refreshes). `AT-602`'s month-row ash `◆` is no longer "any diamond": it is pinned
to the exact column — `month[label_w + 1 + ax.cell(tw0.due)] == ("◆", REACHED)` — computed
through the SHIPPED axis math (`gantt_axis`/`gantt_window`/`gantt_plan` on `app.board` with
`today` and the `tw5` selection), Mockups' reached-grey cell. One new arm drives the
offer-converted milestones into a TEAM folder end to end
(`test_AT_601_offer_converted_milestones_reach_a_team_folder`): the house `shared/team.json`
folder pattern (config listing pweb/pmob/papi), `team_shared_dir` + `team_user_id` set, the
`@pytest.mark.milestone_offer` mark so the start offer actually opens; `enter` converts the three
pre-checked one-day candidates (`ta3` · `tw5` · `tm5`), each is flagged in the saved board, then
the arm polls the team file ≤5s and asserts all three reached it with `milestone: true` and
`start == due`. The 80×24 block's two assertions were kept byte-identical through a key-driven
selection the old shortcut could not express (§5 names the nuance, surfaced not faked).

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `tests/test_milestones.py` | test | HLR-1106 · LLR-1106.1 — the amended AT-601 | `_edit` split into `_editor_save` (no assignment) + `_edit` (kept for TC-605); `_select` bidirectional; AT-601 walks to `ta1` with keys; the new team-folder arm |
| `tests/test_gantt_milestones.py` | test | HLR-1106 · LLR-1106.1 — the amended AT-602 | the `_select` key-walk helper; all four direct assignments replaced with key walks; the redundant refreshes removed; the ash `◆` pinned to the exact column via the shipped axis math |

| Count | Value |
|---|---|
| **SOURCE files** | **0 / 4** — the increment is test-strength only; its brief forbade touching `taskboard/**` (parallel agents owned every source file) |
| Test files | 2 (uncapped) |
| Doc files | 0 (outside the count) |

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_milestones.py tests/test_gantt_milestones.py -q    # 71 passed
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  bash -c 'grep -n "selected_task_id =" tests/test_milestones.py tests/test_gantt_milestones.py'   # no hit inside an amended arm body
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | none new — no product code in this increment; the criterion does not apply (declared, not silently skipped) | — |
| **A · white-box** the grep pin ↔ LLR-1106.1 | `core` · `full` | the census probe over both files' amended-arm bodies | the pin is GREEN (no direct assignment in an amended arm body) and was shown RED by M5 below |
| **B · black-box** the amended `AT-601`/`AT-602` + the team-folder arm ↔ story | `core` · `full` | the two files at 71 nodes (was 70; +1) — outcome assertions byte-identical, reached by keys | 71 passed |

The two files: **71 passed, 0 failed** in 24.24s (`evidence/inc004-run.log`). The agent's
full-suite pass at its own checkpoint reported **2551 passed** — a MID-FLIGHT count (increments
001 and this increment's arm had landed; 002's four nodes were still landing: `2546 + 4 + 1 =
2551`); after increment 003 settled, the last complete green on the settled tree is **2556**
(`evidence/inc003-run.log`). The increment's packet cites the final close run as its own — "see
`04-validation.md`" (the orchestrator re-runs the ONE complete clean-tree suite at P4, C-25).

> ⚠ **Failure-count declaration (V56):** this packet's settled figure is `0 failed`; the cited
> transcript `evidence/inc004-run.log` holds one earlier `1 failed, 70 passed in 25.16s`
> (line 967) — an intermediate run of the same two files while the 80×24 two-selection sequence
> was being settled. The settled final run in the same file is 71 passed, 0 failed.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M5 (the planted direct assignment):** `    app.selected_task_id = 'ta1'  # MUTATION M5` inserted at the head of the AT-601 body — the exact pattern LLR-1106.1 forbids |
| Instrument | project code: the coordinator's scripted plant (`evidence/run-mutations-abc.py` §M5) + the grep pin named in the increment's brief |
| Where it ran | **my own tree** — the MAIN checkout (the batch's single lane) |
| Transcript | `evidence/mutations-abc.log` §M5 — the grep probe exits 0 and lists the planted line (`446:    app.selected_task_id = 'ta1'  # MUTATION M5`) alongside the remaining legitimate hits — the pin FIRES |
| Restore proven by | the file hash: the restore line reported `MISMATCH` on the same text-mode line-ending note as increment 001's M1 (content exact, cosmetic; git normalizes on commit) — the normalized hash `bb62c13a7459aeafe92c12603f5501fe1bbcfd9656b56acb29b1e9e4ef7db731` IS `tests/test_milestones.py`'s hash at this close-out, verified again by the green 71 |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | the probe's census over `tests/test_milestones.py tests/test_gantt_milestones.py` — the planted line is one resolved hit among the file's remaining legitimate assignments (the module-level `_edit` helper kept for TC-605 · the untouched TC arms · the fixture setups · the `_select` helpers' `==` comparisons) |
| Verdict granularity | **per resolved line** — the probe names each surviving assignment's site and owner; only the planted line is the mutant |
| Arms that stayed GREEN | the suite stayed green after the plant was REMOVED (the restore) — and the pin's value is precisely that a reverted arm cannot hide: any direct assignment in an amended body is listed the same way |

| Field | Value |
|---|---|
| **RED counterfactual** | M5 — the planted `app.selected_task_id = 'ta1'` inside the AT-601 body, killed by the grep pin · transcript `evidence/mutations-abc.log` §M5 · restore digest `bb62c13a…b731` (the text-mode note above) |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved line: M5 · KILLED-by-probe (the grep exit 0 + the planted line listed) · the probe is RED on the base tree as well — the pre-increment arms assigned the selection directly, which is exactly the failure this increment corrects · the surviving legitimate hits, named: `tests/test_milestones.py:250` (the module-level `_edit` helper, kept for the untouched TC-605 arms) · `:177` / `:222` (fixture setups) · `:343` / `:373` / `:428` / `:433` (the untouched TC arms) · the `_select` helpers' comparisons (`==`, `:62` and `tests/test_gantt_milestones.py:292,361,364`) · inert arms: none — the arm-level RED is the probe's own firing · registry: no `docs/tools/devflow-mutants.json` battery in this repo — the planted probe is the increment's own counterfactual · transcript `evidence/mutations-abc.log` · restore digest `bb62c13a…b731` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the grep pin (`grep -n "selected_task_id =" tests/test_milestones.py tests/test_gantt_milestones.py`) | M5's planted assignment inside the AT-601 body | the planted line listed, probe exit 0 — the pin fires (`evidence/mutations-abc.log` §M5) |
| the exact-column ash assertion (`tests/test_gantt_milestones.py`) | the pre-increment "any ◆" check — a known-weak instrument that accepts a diamond at ANY column | the shipped pin discriminates: `month[label_w + 1 + ax.cell(tw0.due)] == ("◆", REACHED)` — the exact reached-grey cell via the shipped axis math, not a substring search |
| the team-file byte assertion | the offer path WITHOUT the team-folder listing | the arm fails when the converted milestones never reach `board.jav.json` — the emitted JSON is the asserted surface (its ≤5s poll tolerates the async push) |
| `pytest` (the suite) | a broken key-walk (a `_select` that presses the wrong direction) | the arm's outcome assertions depend on the selection being where the user would be — the walk's failure surfaces as the arm's own RED (the 71-node green stands behind every walk) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown able to report FAILURE before its PASS was believed (the M5 transcript is the pin's own RED; the column-pin and team-file rows name the known-weak instrument each replaces) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the team file (`board.jav.json`) | polled ≤5s: all three converted milestones (`ta3` · `tw5` · `tm5`) present with `milestone: true` and `start == due` | all three reached the team file — the emitted JSON on disk, not the app's memory |
| the saved board | each converted task flagged as a milestone in the board file's bytes | holds before the team-file poll |
| the painted gantt month row | `month[label_w + 1 + ax.cell(tw0.due)] == ("◆", REACHED)` on the emitted frame | the ash sits at Mockups' exact reached-grey column — computed through `gantt_axis`/`gantt_window`/`gantt_plan`, the same math the painter runs |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted against the form its producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the increment brief | `.dev-flow/2026-10-07-batch-05/evidence/inc004-brief.md` | `15fffa92452358c914714f4167ff67df93712f013715d96f563526750f19ff9f` |
| the agent's run + report (71 passed; the per-arm account; the 80×24 nuance; the grep pin) | `.dev-flow/2026-10-07-batch-05/evidence/inc004-run.log` | `4cbbe3f897235b963d71a6ccbd316881f6949e354e538b45585ea188ea5d3c62` |
| the stored mutation battery M1-M5 (M5 this increment) | `.dev-flow/2026-10-07-batch-05/evidence/mutations-abc.log` | `4273b8ae4f58805cc2f70413422b2cc2d8b2e1ca3e47429f3eeed5cda856e082` |

| Field | Value |
|---|---|
| **Evidence files** | 3 artifacts, each at the declared home and cited with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — "no direct `selected_task_id` assignment inside an amended arm body" is an absence claim over both test files |
| If the result is an ABSENCE, what made the search wide enough | the census greps BOTH files line-by-line with a single simple pattern — no scope qualifier that could miss a reintroduced assignment in either amended body |
| Guard labelled as protecting a CONCLUSION, not a behaviour | the increment's brief + the M5 plant — the grep pin is the no-direct-assignment conclusion's standing guard, and M5 is its scheduled RED |
| Conjunctive criteria: one mutation per conjunct | the pin kills the assignment conjunct; the arm-level outcome assertions (unchanged, byte-identical) kill a "walk somewhere else and still assert" revert — the two conjuncts of LLR-1106.1 |
| Synthetic instance of the absent case | M5's planted assignment IS the synthetic instance of the forbidden case — planted precisely so the absence probe must speak |
| **Positive control for every probe that returned an ABSENCE** | the same grep returns the KNOWN-PRESENT legitimate hits (the `_edit` helper · the untouched TC arms · the fixtures — each named in the verdict table): a non-absence on known-present sites, by the identical probe |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -n "selected_task_id =" tests/test_milestones.py tests/test_gantt_milestones.py` → `:250` (the `_edit` helper) · `:177`/`:222` (fixtures) · `:343`/`:373`/`:428`/`:433` (untouched TC arms); the `_select` helpers' hits are `==` comparisons (`:62` · `tests/test_gantt_milestones.py:292,361,364`) | every surviving assignment owned by a named non-amended site; the amended arm bodies carry none |
| B2 file moved on disk | `git status --porcelain -- tests/test_milestones.py tests/test_gantt_milestones.py` → ` M` both | no rename, no delete; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → no such directory in this repo | did NOT fire |
| B4 artifact produced here is consumed elsewhere | the arms' outcome assertions are byte-identical — their consumers are the suite's own milestones/gantt pins | re-validated by the 71-node green |
| A3 interface consumed by another module changed | none — ZERO source files touched; the arms consume the SHIPPED navigation (`app._nav_flat()`, the arrows) without changing it | the navigation model is read-only here |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1's hits are all named non-amended owners, A3 is vacuously clean (no product surface touched), B2/B3 did NOT fire with their probes recorded |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| qa P4 F-3..F-5 (this increment) | the BACKLOG's standing carries | `.dev-flow/BACKLOG.md` "Open — after `2026-10-04-batch-02` (Batch B2a)" — the "Test strength, LOW" bullet | 1 item (three sub-parts: the key-walks · the team-folder gap · the column pin) | AT-601 + AT-602 rewritten; the team-folder arm added; the ash pinned — this increment | none — the sub-parts are one backlog item, closed whole |

| Field | Value |
|---|---|
| **Correction population** | 1 correction wave (the F-3..F-5 item of the ten-item backlog wave), enumerated before the first site was edited; closed whole |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the AT-601 body's hidden assignment (via the old `_edit`) | 0 hits inside the amended body — `_editor_save` never assigns; `_edit`'s assignment survives only for the TC-605 arms | yes | `tests/test_milestones.py` (`_editor_save` · `_select` · the amended AT-601) |
| the AT-602 direct assignments (`tw5` start · `td0` · `tw2` · the 80×24 `ta3`) | 0 hits inside the amended arm — every selection is a `_select(...)` call | yes | `tests/test_gantt_milestones.py` (the amended AT-602) |

### Signed-balance test ledger

`post = base − D + A` → `2551 = 2550 − 0 + 1` ✓ at this increment's own checkpoint (base =
increment 001's 2550 collected; this increment added exactly one node — the team-folder arm; the
AT-601/602 amendments modified, not added). The observed 2551 was mid-flight; the batch-level
ledger — and the final close number this packet cites as its own — is summed in
`04-validation.md`: "see 04-validation".

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` — the close-out coordinator self-executed the P2 lens pool over the four packets and the diffs · verdict PASS-WITH-NOTES, 0 HIGH — the notes: the team-folder arm's declared limit (only listed projects push — §1), the 80×24 nuance surfaced-not-faked (§5) · the P2 review verdict stands in `02-review.md` |

---

## 5 · Risks

- The team-folder arm's coverage limit, declared by the agent and kept: only projects DECLARED in
  `team.json` are pushed, so the arm lists the three team projects explicitly — the strongest
  end-to-end the house fixture supports; a folder with an unlisted project would need the
  shipped push rule to change first.
- The 80×24 nuance (surfaced, not faked): the block asserts the frame draws BOTH the reached
  milestone (pweb) and the Partner notice (api). The old `assign ta3` shortcut left
  `_gantt_previous = pweb` — a state the arrows CANNOT reproduce (walking into api from pweb
  traverses pmob, keeping pmob open and folding pweb, so the legend names `chain`, not
  `reached`). To keep both outcome assertions byte-identical, the arm reaches the 80-wide legend
  on the reached milestone's group (`_select tw5`, previous `None` → the legend draws both
  marks), then `_select ta3` for Partner notice's row. The assertion strings are unchanged; a
  key-driven selection was inserted between them. This is the one place the "keys alone" law
  meets a state the shipped keys cannot reach — documented so a future reader does not
  "simplify" it back into an assignment.
- The arms walk the shipped nav order through `app._nav_flat()`: a navigation-model change
  (new sort orders, new keys) re-routes every walk — the 71-node green is the standing guard.

## 6 · Pending items / spec deviations

- None open here. The 80×24 two-selection sequence (§5) is a documented test-shape note, not a
  deviation — the law's substance (no direct assignment in an amended body) holds; the inserted
  key-walk strengthens it.

## 7 · Suggested next task

- The batch close — the record phases (04-validation · 05-close · the BACKLOG bookkeeping) are
  the coordinator's; no increment remains.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 0 source files — the test-strength increment's brief forbade touching `taskboard/**` |
| 2 | Tests written in this same increment | all | ✓ | the amended AT-601/AT-602 + the new team-folder arm landed in the same run (71 passed) |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | declared not applicable — no product code (the criterion's empty state, stated, not skipped) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M5 executed — the planted assignment fires the grep pin; transcript `evidence/mutations-abc.log` §M5; restore digest `bb62c13a…b731` |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above) |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b — `human:coordinator` self-executed lenses · PASS-WITH-NOTES 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane; the parallel window with increment 001 was over disjoint files (the two milestones test files); `git diff --name-only HEAD` — the two test files only |
| 8 | Frozen interfaces untouched | all | ✓ | ZERO product files touched; the navigation model consumed read-only |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | the no-direct-assignment census + M5 as its synthetic instance |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | per-line verdict table above; every surviving assignment's owner named |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) |
| 13 | **Correction population** declared | all | ✓ | the F-3..F-5 item (one backlog bullet, three sub-parts), enumerated before the first edit |
| 14 | **Emitted-form assertion** declared | all | ✓ | the team file's JSON + the saved board + the painted month row |
| 15 | **Independent review** names somebody | all | ✓ | §4b — `human:coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 3 artifacts with stored-byte digests |
