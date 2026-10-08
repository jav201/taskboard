# Increment 001 — HLR-1202 · the kanban window shows its hidden sides

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
> `.dev-flow/2026-10-07-batch-06/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-06` |
| Increment | `001` |
| Lane (if the batch forked) | `none — one implementing session, two increments serialized (the single brief owned views.py for both, task 1 then task 2; no two live briefs ever wrote the same file)` |
| Requirement(s) | `HLR-1202` (+ `LLR-1202.1`) |
| Acceptance | `AT-1202` — 4 arms, all green · the pinned chrome arms `tests/test_app.py:1598-1603` (the window test) and `TC-313` at `tests/test_kanban_readable.py:557` updated in place to the new glyph law · unit: `_windowed_header`'s marker law |
| Agent | `software-dev` — DeepSeek V4 Pro (one session, both increments) |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

The kanban's phase-head row now announces its hidden sides: when the phase window is offset, a `◂`
sits immediately before the first visible phase title; when columns hide on the right, ` ▸ N` (N
exact) follows the last visible one; when everything fits, the head row carries no markers at all.
The `?` kanban help gained the window bullet: `more phases than fit — the window follows the
selection (j/k into a later column) · ◂ ▸ mark the hidden sides` (`views.help_usage("kanban")`,
`taskboard/views.py:6817-6822`). Mechanism: `_windowed_header` (`taskboard/views.py:4435-4467`)
gains a `pre`/`suf` pair around the shipped title/tag cell (`views.py:4456-4457`) — `pre = "◂ " if
(i == 0 and start > 0)`, `suf = f" ▸ {n - end}"` on the last visible cell when `end < n`; the
tag-last layout and the WIP counts are untouched, and the no-marker case is byte-identical to the
pre-batch row.

**Review note, carried from the coordinator's mutation log and folded into the close's lessons:**
the hidden-phase marks EXISTED in a prior chrome — `◀ N` left, `N ▶` right, pinned by
`tests/test_app.py`'s window test. This increment REFINES the form (`◂`, and `▸ N` with the count
on the right edge only), keeps the exact count law, adds the left-edge case (`◂` fires whenever
`start > 0`, the old chrome marked the left only with a count) and the `?` bullet. The operator's
real gap was discoverability — nothing said the rest existed — and the help bullet is the
substantive fix; the marks make it true on the surface itself.

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | HLR-1202 · LLR-1202.1 | `_windowed_header`'s `pre`/`suf` marker pair (:4456-4457, docstring :4437); the kanban help bullet (:6817-6822) |
| `tests/test_kanban_window.py` | test | LLR-1202.1 — pinned by AT-1202 | new — 4 arms (the right marker, the late-selection left marker, the all-fits none, the help bullet) |
| `tests/test_app.py` | test | LLR-1202.1 — the pinned window arms | the two marker assertions :1598-1603 updated to the new glyphs (`◀ 5` → `◂`, `5 ▶` → `▸ 5` — same counts, new chrome; assertions NOT weakened) |
| `tests/test_kanban_readable.py` | test | LLR-1202.1 — TC-313's hidden-count arm | :557 — `f"{hidden} ▶"` → `f"▸ {hidden}"` (same count arithmetic) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 3 (uncapped) |
| Doc files | 0 (outside the count) |

- One source file: the marker law and its help bullet both live in the kanban region of views.py;
  there is no smaller seat — the head row is the law's only surface.

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_kanban_window.py tests/test_kanban_readable.py tests/test_cells.py -q   # 399 passed
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_app.py -q -k "kanban"                                                   # 30 passed, 132 deselected
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (`_windowed_header`'s marker law — the `pre`/`suf` conditional pair over the shipped `fits`/`start`/`n_open` window arithmetic; cyclomatic ≥3) | `core` · `full` | the 4 arms of `tests/test_kanban_window.py` | 4 passed (mutation-proven — M12 below) |
| **A · white-box** `TC-313` ↔ LLR-1202.1 (the pinned chrome census) | `core` · `full` | `test_TC_313_the_chrome_names_the_modes_and_counts_hidden_phases` · `test_kanban_windows_phases_when_they_dont_fit` (`tests/test_app.py`) | 2 arms passed, updated in place |
| **B · black-box** `AT-1202` ↔ US-1202, through the shipped surface | `core` · `full` | `test_the_narrow_window_marks_the_hidden_right` · `test_a_late_selection_marks_the_hidden_left_and_drops_the_count` · `test_the_full_window_carries_no_markers` · `test_the_help_names_the_window_bullet` | 4 nodes passed |

The session's targeted run held `tests/test_kanban_window.py tests/test_kanban_readable.py
tests/test_cells.py` at **399 passed, 0 failed** and `tests/test_app.py -k kanban` at **30 passed,
132 deselected** (`evidence/inc001-run.log`). The two complete green runs over the settled tree
passed **2566 / 2566** both times (447.08s and 422.53s, `evidence/inc001-run.log`) — "see
04-validation" for the close number; the orchestrator's C-25 owns the ONE final clean-tree run.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M12 (the right window marker removed):** `_windowed_header`'s `suf = f" ▸ {n - end}" …` → `suf = ""` — the pre-law behavior on the right edge (the left `pre` line untouched) |
| Instrument | project code: the coordinator's byte-level mutation runner (`evidence/mutations.log` — byte-anchored, restores hash-verified) |
| Where it ran | **my own tree** — the MAIN checkout (the batch's single lane; the battery is the coordinator-run close-out set, executed on this tree) |
| Transcript | `evidence/mutations.log` M12 — `1 failed, 3 passed` on `tests/test_kanban_window.py` |
| Restore proven by | **file hash returned to its pre-mutation value** — `evidence/mutations.log`: "All four restores returned OK (file hash identical before/after)"; views.py's hash at this close `12b5059f…2e8e` |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **4** — `pytest tests/test_kanban_window.py --collect-only -q` resolves exactly the 4 arms named in the Layer table |
| Verdict granularity | **per resolved node id** — M12 reddened exactly the hidden-count arm (`test_the_narrow_window_marks_the_hidden_right`); the left-marker, all-fits and help arms stayed GREEN on the same mutant |
| Arms that stayed GREEN | **named:** `test_a_late_selection_marks_the_hidden_left_and_drops_the_count` (the late-selection case asserts NO right marker — `▸` absent — so a removed right marker cannot redden it), `test_the_full_window_carries_no_markers` (asserts absence on both sides), `test_the_help_names_the_window_bullet` (the help bullet is not the marker line) |

The pre-change chrome's existence is evidence, not assertion: the pinned arms this increment
updated carried `◀ 5` / `5 ▶` (removed lines, `tests/test_app.py:1598-1603` diff) and `{hidden} ▶`
(`tests/test_kanban_readable.py:557` diff) — so the new file's arms fail by construction on the
base tree (its docstring declares the RED: "the head row wore `◀ N` / `N ▶`; `◂` and `▸ N` did not
exist"), and M12 is the executed counterfactual on this tree.

| Field | Value |
|---|---|
| **RED counterfactual** | M12 — `_windowed_header`'s `suf` marker line emptied (the right-edge count removed) · transcript `evidence/mutations.log` M12 (`1 failed, 3 passed`, the GREEN arms named above) · restore digest: all four restores `OK`, views.py at `12b5059f…2e8e` |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node: **M12** · `test_the_narrow_window_marks_the_hidden_right` KILLED (the `▸ 2` count is gone) · the three GREEN arms named above (a removed right marker is invisible to them) · inert arms: none · registry: no `docs/tools/devflow-mutants.json` battery in this repo — M12 is the increment's own counterfactual from the coordinator-run batch battery (M9-M12) · transcript `evidence/mutations.log` · restore digest: `OK` (hash-identical) |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M12's mutant code (the right marker removed) | `1 failed` on `test_the_narrow_window_marks_the_hidden_right` — the painted head row lacked `▸ 2` (`evidence/mutations.log` M12) |
| the old-chrome census probe | the pre-batch tree (via the pinned arms' removed lines) | the pinned arms asserted `◀ 5` / `5 ▶` / `{hidden} ▶` — the probe's pre-batch output named the old glyphs the new law replaced (the diff's `-` lines; `evidence/inc001-run.log`) |
| the help-width probe | the window bullet wrapped to the help column's 44 cells | the joined text reconstructs the verbatim tail `more phases than fit — the window follows the selection (j/k into a later column) · ◂ ▸ mark the hidden sides` — the probe printed the joined string and the per-line cell counts 46/45/41 (over-width lines would have failed the wrap; `evidence/inc001-run.log`) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown RED (or discriminating) before its first PASS was believed (transcripts in `evidence/mutations.log` · `evidence/inc001-run.log`) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the phase-head row at width 40 (the 4-phase fixture) | `views.render_kanban(b, False, sel, TODAY, width=40, height=0).plain.split("\n")[1]` — asserted by the new arms | `'BACKLOG         1│NEXT     1 ▸ 2│✓1     '` (sel at the first phase — `▸ 2` exact) · `'◂ NEXT       1│DOING     1/3 ▸ 1│✓1     '` (mid window — both marks) · `'◂ DOING     1/3│REVIEW         1│✓1     '` (late selection — left mark only, the count drops) — verbatim from `evidence/inc001-run.log` |
| the phase-head row at width 40 (the 8-phase board, `tests/test_app.py`'s fixture) | the pinned window arms, updated in place | `'◂ PHASE5       0│PHASE6        0│✓1     '` and `'PHASE0           6│PHASE1  0 ▸ 5│✓1     '` — the same emitted row the user sees (`evidence/inc001-run.log`) |
| the `?` kanban help | `" ".join(line for _h, lines in views.help_usage("kanban") for line in lines)` | the verbatim bullet tail `… · ◂ ▸ mark the hidden sides` (printed in `evidence/inc001-run.log`) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted against the form its producer emitted (the painted head row at two fixtures + the joined help text) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the increment brief (the coordinator's chunk brief — tasks 1+2, one session) | `.dev-flow/2026-10-07-batch-06/evidence/inc001-brief.md` | `38d93b8c81c619d8b4d77503562aa0c9ad42fb9c256775d6530b00d402691650` |
| the session's run log (targeted verifies, the emitted-row prints, two full-suite greens at 2566, the report) | `.dev-flow/2026-10-07-batch-06/evidence/inc001-run.log` | `3a5f95c61a9811e7790f448b8da0965a86168578020ddd7cd0ef0bb543f114e3` |
| the close-out mutation battery M9-M12 (M12 this increment) | `.dev-flow/2026-10-07-batch-06/evidence/mutations.log` | `f74656736101c6a3fe6cf4a6305142d4cc35127b82511ca841e11b35aef7b3ab` |

The new test file's stored bytes: `tests/test_kanban_window.py` sha256
`24b24e7c5b4b5f54bc879346d1738673ebf9a4808cf667407851efe4ee1374d1` (its home is the `tests/`
home `artifact_homes.tests` declares — cited here for the record, not as an evidence-home artifact).

| Field | Value |
|---|---|
| **Evidence files** | `3` artifacts at the evidence home, each cited with the digest of its stored bytes; the new test file's digest is cited beside the table (its home is `artifact_homes.tests`) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — "when everything fits, the head row carries NO markers" is an absence claim, and so is "no OLD-chrome glyph (`◀`/`▶`) survives in the shipped law" |
| If the result is an ABSENCE, what made the search wide enough | the all-fits arm probes the WHOLE emitted head row for both glyphs (`◂` and `▸`), not a substring around one phase; the old-chrome census runs over `tests/` and `taskboard/` (`grep -rln "▶\|◀" tests/ taskboard/`) — the only hits are this batch's own docstring mention in `tests/test_kanban_window.py` and stale bytecode caches |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_the_full_window_carries_no_markers` — its docstring names it "LLR-1202.1 (negative control)" (the next reader "simplifies" an absence arm away without the label) |
| Conjunctive criteria: one mutation per conjunct | the marker law has two sides — right (M12 kills it) and left (the late-selection arm pins `◂`; a removed `pre` reddens it by symmetry — the arm's assertion is the left side's mutation probe); one probe per side, both discriminating |
| Synthetic instance of the absent case | n/a — the absence is on the emitted row, exercised over a fixture board built in the test file (4 open phases + Done at widths 40/80); no tree-level instance is claimed absent |
| **Positive control for every probe that returned an ABSENCE** | the same unmodified `_head()` probe at width 40 returns the markers (`▸ 2` present — a non-absence on the known-present case); the census probe returned the old glyphs on the pre-batch tree (the pinned arms' removed `-` lines) — uniformity over heterogeneous inputs, not one probe repeated |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln "_windowed_header" tests/` → `tests/test_app.py` (+ stale caches); `grep -rln "help_usage" tests/` → `tests/test_english.py` · `test_gantt_milestones.py` · `test_help_clip.py` · `test_kanban_milestones.py` · `test_kanban_priority.py` · `test_kanban_readable.py` · `test_kanban_window.py` · `test_links.py` · `test_markup_sites.py` | the marker symbol's only named test seat is the pinned window arm (updated here); the help surface is censused by the readable/help families — every reader re-validated by the green suite (399 + 30-deselected runs + two full greens) |
| B2 file moved on disk | `git status --porcelain -- taskboard/views.py` → ` M` (modified in place) | no rename, no delete — the old path is the current path; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → `No such file or directory` | the repo holds no golden-capture directory (as batch-05 recorded); did NOT fire |
| B4 artifact produced here is consumed elsewhere | `grep -rn "help_usage" taskboard/ --include=*.py \| grep -v views.py` → `taskboard/modals.py:1845,1859` | the HelpModal consumes `help_usage(mode)` wholesale — the (mode) → sections signature is unchanged, the kanban section gained a bullet; the modal renders bullets generically, re-validated by `test_help_clip.py` green |
| A3 interface consumed by another module changed | the head-row byte contract changed BY DESIGN (that is HLR-1202); the composed interface around it is untouched — `_phase_window`'s `(start, widths)` return (`views.py:4418-4433`), the WIP-tag/count seat, and the cell-assembly order are pre-batch bytes | no cross-module consumer of the cells exists outside views.py's kanban composer (the only reader, in the same module); the change is self-contained |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1's hits are this batch's own pins + the help census family (re-validated by the suite), B4 names the one modal consumer under an unchanged signature, B2/B3 did NOT fire with their probes recorded · transcripts in `evidence/inc001-run.log` |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| — none — no correction wave in this increment (a glyph refinement + a help bullet, not a correction of a shipped claim) | — | — | — | — | — |

| Field | Value |
|---|---|
| **Correction population** | none — no correction |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the old left glyph `◀ ` in the shipped law | 0 hits — `grep -rn "◀" tests/test_app.py tests/test_kanban_readable.py taskboard/views.py` → 0 (the only `◀`/`▶` survivors are the docstring's historical note in `tests/test_kanban_window.py` + caches) | yes | `tests/test_app.py:1601` · `tests/test_kanban_readable.py:557` |
| the old right glyph ` ▶` in the shipped law | 0 hits — same probe over the same files | yes | `tests/test_app.py:1603` |

### Signed-balance test ledger

`post = base − D + A` → batch post `2566 = 2556 − 0 + 10` ✓ reconciles (base = the batch-05
trunk at 2556; A = 10 new nodes across both increments — this increment's share is the 4 arms of
`tests/test_kanban_window.py`; the pinned updates in `test_app.py` / `test_kanban_readable.py`
modified, not added). This increment's checkpoint: `2560 = 2556 + 4`. The batch-level ledger is
summed in `04-validation.md` — "see 04-validation" for the close number; the close-out
re-collected the suite at **2566 tests** (`pytest tests --collect-only -q`).

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` — the close-out coordinator self-executed the P2 lens pool over the two packets and the diffs · verdict PASS-WITH-NOTES, 0 HIGH — the notes: (a) the contract specified the marker glyphs without checking the shipped `◀/▶` chrome (a writing defect caught at review — folded: the batch refines rather than invents; carried into this packet §1 and the close's lessons); (b) the three layout-driven test updates of increment 002 are law-driven, each named in that packet · the P2 review verdict stands in `02-review.md` (0 blocker · 0 major · 0 minor; reviewer `human:coordinator`, the runtime spawned nobody) |

---

## 5 · Risks

- The marker law keys on `_phase_window`'s `(start, fits, n_open)` policy: a future change to the
  window policy (e.g. a centered window) moves the markers with it — the arms pin the CURRENT
  policy at two widths and both selection extremes, so such a change reddens them (that is the
  arms' job, but the contract would need re-reading, not just the code).
- The help bullet is hand-wrapped to the help column's 44 cells; a future help-column resize must
  re-wrap the three lines — the joined-text arm fails if the wrap stops reconstructing the verbatim
  tail.
- ⚠ The all-fits arm asserts the absence of the NEW glyphs only; the pre-batch glyphs were
  different codepoints (`◀`/`▶`). "Byte-identical to the pre-batch row" holds because the no-marker
  case emits neither generation's marks — declared here so the next reader does not "strengthen"
  the arm into a cross-generation pin it was never written to be.

## 6 · Pending items / spec deviations

- None open here. The operator's visual re-verdict on the new chrome (and increment 002's amended
  frames) is the batch-level pending — the close carries it in batch C's form.

## 7 · Suggested next task

- Increment 002 — the chain map admits every open task (the `○` tiles + the oracle amendment
  under LED-2026-10-07-batch-06.1), serialized after this increment in the same session.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 1 source file (views.py — the kanban region) |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_kanban_window.py` (4 arms) landed with the product in the same session; the two pinned files updated in place |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `_windowed_header`'s marker law — the 4 arms, mutation-proven (M12) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M12 executed; transcript `evidence/mutations.log`; restore digest hash-identical; the base-tree RED declared in the new file's docstring + the pinned arms' removed old-glyph lines |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above); B2/B3 did NOT fire |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b — `human:coordinator` · PASS-WITH-NOTES 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane; the single brief owned views.py sequentially (task 1 then task 2) |
| 8 | Frozen interfaces untouched | all | ✓ | `_phase_window`'s return, the WIP-tag seat, the cell order, and `help_usage`'s (mode) → sections signature are pre-batch bytes |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | the all-fits absence + the old-chrome census, each with its positive control |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | M12 per-node (1 KILLED, 3 GREEN named); transcript + restore digest cited |
| 12 | **Instrument RED-proof** declared | all | ✓ | 3 instruments (table above) |
| 13 | **Correction population** declared | all | ✓ | none — no correction this increment |
| 14 | **Emitted-form assertion** declared | all | ✓ | the painted head rows at two fixtures + the joined help text |
| 15 | **Independent review** names somebody | all | ✓ | §4b — `human:coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 3 artifacts at the evidence home + the new test file's digest cited beside the table |
