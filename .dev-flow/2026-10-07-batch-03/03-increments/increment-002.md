# Increment 002 — HLR-903 · The render items (K2-1 fold half · D-623 · UX2-2 · milestones-in-views)

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
> `.dev-flow/2026-10-07-batch-03/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-03` |
| Increment | `002` |
| Lane (if the batch forked) | `none — one lane per increment (§2.8 of the contract)` |
| Requirement(s) | `HLR-903` (+ `LLR-903.1`) — K2-1's fold half, D-623, UX2-2, milestones-in-views |
| Acceptance | `AT-903[1_legend fold half]` · `AT-903[2_rule_only]` · `AT-903[3_fold]` · `AT-903[4_views]` — the 4 arms RED-by-design at increment 001, green here |
| Agent | `software-dev` — DeepSeek V4 Pro (views.py only), after DeepSeek V4.1 Flash's RED arms; the coordinator reverted the fold-row rename and re-fitted the suffix |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

What the kanban screen says is now what it draws. The `?` legend names `◆` "a milestone on its
project's band rule" only for bands the screen DRAWS — ONE shared drawn-band computation
(`_fold_keep`, `taskboard/views.py:5130-5148`) serves the renderer and the legend (CL-7), the
renderer calling it at `:5092` and the legend branch at `:6746-6751`. A milestones-only project
keeps its rule-only band carrying `◆`, its head reading `N open` (`kanban_plan`'s admission
`:4695-4726`; `_kanban_grouped`'s empty-plan check `:5047`). A late milestone folded off below
marks the fold row — the canonical `▼ N below` literal (`:5161`) with the ` · ▲N ◆` suffix
appended BEFORE the final fit (`:5179-5181`), the late count computed at `:5122-5127`. Lanes,
agenda and focus render milestones with their `◆` identity (the grid row `:1037`, the waves row
`:1611`, the agenda dot `:1982`, the focus title sites via `_milestone_title` `:2480`), marker
only — no layout change to non-milestone rows (CL-9); the swimlanes `?` legend names the
milestone `◆` (CL-5, `:6623-6632`). The deviating rename `▼ N below` → `▾ N more` was tried,
redditened the 7-fold TC-311 census, and was reverted by the coordinator (LED .3); the suffix
was then appended to the canonical literal before its final fit.

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | HLR-903 · LLR-903.1 | `_fold_keep` (:5130) · `_kanban_band_geometry` (:5184) · `_kanban_high_rows` (:5198) — the shared drawn-band seat; `kanban_plan`'s milestones-only admission (:4695-4726); `_kanban_grouped`'s late-ms count (:5122-5127) + empty-plan check (:5047); `_fold_row`'s canonical literal kept + the ` · ▲N ◆` suffix before the fit (:5151-5181); `legend_entries`'s drawn-band kanban branch (:6741-6751) + swimlanes CL-5 branch (:6623-6632); the `◆` marker sites (:1037, :1611, :1982, :2480 + the focus titles) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 0 — the arms already existed, RED by design (`tests/test_cleanup.py`, landed with increment 001) |
| Doc files | 0 (outside the count) |

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_cleanup.py -q                       # 12 passed (the 4 arms green)
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_kanban_readable.py -q -k TC_311    # 9 passed (the 7-fold literal census)
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (`_fold_keep` — the fold's while-loop bands ≥3; `_fold_row` — the fit/clipping branches ≥3) | `core` · `full` | `_fold_keep` · `_fold_row` | 2 units — mutation-proven below |
| **A · white-box** ↔ LLR | `core` · `full` | the 7-fold TC-311 census (test_kanban_readable.py:66,480,574,607,1221) | 9 nodes passed |
| **B · black-box** `AT-903` ↔ story, through the shipped surface | `core` · `full` | AT-903 ×4 arms (1_legend fold half · 2_rule_only · 3_fold · 4_views) | 4 nodes passed |

Suite at the increment's close baseline: `tests/test_cleanup.py` → **12 passed, 0 failed** and
the fold census → **9 passed, 0 failed** (`evidence/inc002-mutations.log`, BASELINE section).
The implementing agent's own log records the mid-flight state honestly: the rename sat in place
for one run — its full-suite run records 27 failed (2514 passed), of which 7 are the census
reddening the rename caused and 20 are the declared environmental subprocess crashes under
full-suite load (`test_no_live_board` etc., green in isolation —
`evidence/inc002-run.log`); after the coordinator's revert + suffix re-fit the close suite is
**2541 passed, 0 failed** (`04-validation.md`, orchestrator-owned). The 27-failed and
20-failed lines below are those deliberate/mid-flight transcripts, named here so no failure
count is read silently: chunkB-run.log holds the 4 RED-by-design arm failures (`4 failed`);
inc002-run.log holds the mid-flight 27 failed; inc002-mutations.log holds M1's `7 failed` and
M2's `1 failed`.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M1 (the fold canon):** `_fold_row`'s down seat renamed `▼ {len(below)} below` → `▾ {len(below)} more` — the historical rename this batch reverted. **M2 (the UX2-2 suffix):** `_fold_row`'s `if late_ms:` made unreachable (`if late_ms > 99:`) — the canonical literal survives but ` · ▲N ◆` never paints |
| Instrument | project code: the coordinator's own hand via a scripted exact-string replacement; the restore checked by sha256 |
| Where it ran | **my own tree** — the MAIN checkout (the present-e worktree untouched) |
| Transcript | `evidence/inc002-mutations.log` — M1: fold census `7 failed, 2 passed` + AT-903[3_fold] `1 failed`; M2: AT-903[3_fold] `1 failed` with the census `9 passed` |
| Restore proven by | **file hash returned to its pre-mutation value**: `sha256(taskboard/views.py)` → `e2dec7845059ea0066bfb7f43aa09a19cdf6e0a43f60908f8d32272b4075a66f` before, after M1, and after M2 (transcript); re-run green after each restore |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **13** — the 12 cleanup nodes + the 9-node TC_311 census, per resolved node id (M1's `7 failed, 2 passed` is the granularity proof: exactly the literal-reading census nodes reddened, the two shape-only nodes stayed GREEN) |
| Verdict granularity | **per resolved node id** — never the process exit code |
| Arms that stayed GREEN | M1: `test_TC_311_a_down_into_a_drawn_band_moves_nothing` + `test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection` (shape, not literal) + every non-census node · M2: the whole TC-311 census (the literal is untouched) |

| Field | Value |
|---|---|
| **RED counterfactual** | M1 — `_fold_row` (:5161), the down-seat literal renamed `▼ N below` → `▾ N more` · M2 — `_fold_row` (:5179), the `late_ms` suffix guard made unreachable · transcripts at `evidence/inc002-mutations.log` · restore digest `sha256 e2dec7845059ea0066bfb7f43aa09a19cdf6e0a43f60908f8d32272b4075a66f` |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node: M1 · the 7 literal-reading TC-311 nodes KILLED + AT-903[3_fold] KILLED, the 2 shape-only census nodes GREEN (named above) · M2 · AT-903[3_fold] KILLED (`assert any(re.search(r"▼.*▲1 ◆", r) ...)`) with the census GREEN — the two conjuncts of arm 3 (the canonical literal · the suffix) each carry their own kill · inert arms: none · registry: no `docs/tools/devflow-mutants.json` battery in this repo — the two named mutants are the increment's own counterfactuals · transcript `evidence/inc002-mutations.log` · restore digest `e2dec784…a66f` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M1's renamed fold seat | fold census `7 failed, 2 passed`; AT-903[3_fold] `1 failed` |
| `pytest` (the suite) | M2's unreachable suffix | AT-903[3_fold] `1 failed` while the census stayed `9 passed` |
| the painted-frame reader (`tests/test_cleanup.py:53-66`) | reads the compositor's own cells, not the renderer's strings | arm 4's `◆`-in-row assertions — the frame the user sees is what is asserted (a markup-rendering fault would show here, not in a string compare) |
| `grep` census probes | a nonsense control pattern `_fold_keep_nonsense` | `0` files — against the real probes' N — presence vs absence distinguished |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown RED before its first PASS was believed (transcripts in `evidence/inc002-mutations.log`) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the kanban frame's fold row on the AT-903 arm-3 board at 118×24 (the kg milestones board, saved) | `render_kanban(b, False, None, date.today(), 118, 24).plain.split("\n")` — the row holding `▼` | `'▼ 2 below: Data Warehouse (4 open), Ops & Security (5 open) · ▲1 ◆'` — the canonical literal + the suffix, emitted before the final fit; the arm-3 regex `▼.*▲1 ◆` matches this row |
| the kanban frame at 118×15 on the arm-1 fold fixture (the 5-project synthetic, only the last band milestone-bearing) | `legend_entries("kanban", folded, today, 118, 15)` — the emitted legend lines | no `a milestone on its project's band rule` entry — the folded-off band is not named (AT-903[1_legend] asserts exactly this) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts, each asserted against the form its producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc002 run — the 4 arms green, the census reddening named, the environmental 20 declared | `.dev-flow/2026-10-07-batch-03/evidence/inc002-run.log` | `640ac63b83ce61d3b65311fdb9624e862956bef6cbc667a53b23c94b644fd77d` |
| chunkB run — the 4 arms' RED-by-design transcripts (this increment's counterfactual, captured before the product landed) | `.dev-flow/2026-10-07-batch-03/evidence/chunkB-run.log` | `84fdb36879183be878481e55ad94bf0077522a96f784f398eaf8664cab323313` |
| the close-out mutations, reverse census + instrument RED-proof | `.dev-flow/2026-10-07-batch-03/evidence/inc002-mutations.log` | `d81bb13ab426fdf70c5ccf0a169725465f2047d65f8d22baef95695117a2685b` |

| Field | Value |
|---|---|
| **Evidence files** | 3 artifacts, each at the declared home and cited with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — "the legend names only DRAWN bands" rests on no renderer drawing a band the fold drops; and "no layout change to non-milestone rows" (CL-9) rests on the marker sites being the only touched rows |
| If the result is an ABSENCE, what made the search wide enough | the guard: AT-903[1_legend]'s fold fixture renders the frame AND reads the legend at 118×15 (the milestone band provably folded first — `:313-315` asserts no `▐…◆` row paints); CL-9's guard: the paint census (`test_markup_sites` / `test_colour_budget`) stayed green through the increment — every non-milestone row's bytes unchanged |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_AT_903_the_render_items[1_legend]` / `[4_views]` — the docstrings name the drawn-band conclusion and the marker-only scope |
| Conjunctive criteria: one mutation per conjunct | arm 3's two conjuncts killed separately — M1 (the literal) and M2 (the suffix); the legend's two halves (search · fold) each carry their own arm (`[1_legend]` drives both) |
| Synthetic instance of the absent case | `_folded_milestone_board` (`tests/test_cleanup.py:253-267`) — five projects, only the last milestone-bearing, so the only milestone band provably folds away at 118×15 |
| **Positive control for every probe that returned an ABSENCE** | the known-present cases: the same legend call at 118×30 names `a milestone on its project's band rule` (band drawn — the emitted-form table above); the same fold row without a late milestone paints no suffix (TC-311's arms) — non-absences on known-present cases, same unmodified probes |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln _fold_keep tests/` → **0 files**; `grep -rln legend_entries tests/` → 8+ suites (test_archive, test_cleanup, test_colour_budget_app, test_gantt_*, test_kanban_*, …) | `_fold_keep` is exercised through `render_kanban`/`legend_entries` frames, not by name — the symbol-level probe did not fire; every `legend_entries` reader re-validated green |
| B2 file moved on disk | `git status --porcelain -- taskboard/views.py` → ` M` | no rename, no delete; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → no such directory | the byte-exact kanban seats live in `tests/test_kanban_readable.py` itself (FOLD regex :66 + four literal sites) and the paint census (`test_markup_sites`/`test_colour_budget`) — green at baseline and at close; did NOT fire |
| B4 artifact produced here is consumed elsewhere | `grep -rn _fold_row( taskboard/views.py` → the producer at :5151 and the single renderer call at :5127 | the fold row is produced and consumed inside the kanban renderer; its byte readers are the census tests of B1; the agenda-axis and focus-title sites feed the app compositor (paint census green) |
| A3 interface consumed by another module changed | `grep -rn legend_entries taskboard/` → `modals.py:1799-1800` (HelpModal) | the signature is unchanged; the kanban branch's internal drawn-band computation is the CL-7 seat both renderer and legend now read; app.py's HelpModal call gained its filtered-kanban branch in increment 001, not here. Did NOT fire beyond the declared sites |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1's `legend_entries` hits and B4/A3's internal hits re-validated, `_fold_keep` 0 named references (frame-exercised), B2/B3 did NOT fire with their probes recorded · transcripts in `evidence/inc002-mutations.log` §REVERSE CENSUS |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the render items (K2-1 fold half · D-623 · UX2-2 · milestones-in-views) | the same six-item backlog tranche increment 001 drew from | `.dev-flow/BACKLOG.md` "Open — after 2026-10-04-batch-02" lines 43-58 | 6 (the 4 render items here) | views.py — the drawn-band seat, the band admission, the fold row, the marker sites | none — the tranche is closed by increments 001+002 together |

| Field | Value |
|---|---|
| **Correction population** | 1 correction wave (the six-item backlog tranche), enumerated from the canonical backlog before the first site was edited; this increment accounts for its four items |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the renamed fold seat `▾ N more` | 0 hits in `taskboard/views.py` — the only surviving `▾` seats are the gantt/group unfold heads (:2847, :2863, :6463, :6548), a different seat | yes | `taskboard/views.py:5161` |
| the legend's old all-bands `◆` check | 0 hits — the kanban branch reads only `_fold_keep`'s drawn indices | yes | `taskboard/views.py:6746-6751` |

### Signed-balance test ledger

`post = base − deleted + added` → `2541 = 2529 − 0 + 12` ✓ reconciles at the batch level (this
increment added no test file — its arms pre-landed RED-by-design with increment 001 and turned
green here). The batch-level ledger is summed in `04-validation.md`.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `qa-reviewer` ∥ `ux-reviewer` ∥ `security-reviewer` ∥ `architect` — the close-out lens pool, self-executed by the `coordinator` with the role files (named in `02-review.md` per the runtime rule); the P2 iteration over the contract folded CL-1..CL-9 (LED .2); over the SHIPPED tree: **PASS-WITH-NOTES, 0 HIGH / 2 minor** — the fold-rename trap is the batch's own lesson (LED .3), the census reconciliation executed by the coordinator (7 REDs re-derived, not hand-written); every minor named in `02-review.md` · the close-out lens transcript: `evidence/close-review.log` |

---

## 5 · Risks

- The ` · ▲N ◆` suffix appends before the final `fit()` — at pathological widths the fit could
  clip the suffix. The shipped fit keeps the `▼` side last (the LLR-309.1 clip order), and
  arm 3's 118×24 frame shows the suffix intact; a width-sweep pin is a backlog candidate if a
  real board ever clips it.

## 6 · Pending items / spec deviations

- None open — the four RED-by-design arms are green; the mid-flight census reddening was
  reverted and re-derived (LED .3). The 20 environmental subprocess crashes the agent's log
  records under full-suite load are the house's known Windows load behaviour, unrelated to
  views.py (green in isolation — `evidence/inc002-run.log`).

## 7 · Suggested next task

- Batch close (P4 validation read + P5 close), then batch E's prototype verdict in the
  present-e worktree.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 1 source file (views.py) |
| 2 | Tests written in this same increment | all | ✓ | the arms pre-landed with increment 001 (RED by design — chunkB's brief commissioned exactly that); they turn green here — the counterfactual preserved in chunkB-run.log |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `_fold_keep` · `_fold_row` — mutation-proven (M1/M2) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M1/M2 executed; transcript `evidence/inc002-mutations.log`; restore digest `e2dec784…a66f` |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above); transcript in the log |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b: the close-out lens pool under the coordinator · PASS-WITH-NOTES 0 HIGH / 2 minor |
| 7 | No file from another lane touched | all | ✓ | `git diff --name-only HEAD` for this increment → views.py only |
| 8 | Frozen interfaces untouched | all | ✓ | `legend_entries`'s signature unchanged (A3 probe); modals.py untouched |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | the fold fixture + the CL-9 paint census guards, each with its known-present positive control |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | per-node table above; inert arms: none |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) |
| 13 | **Correction population** declared | all | ✓ | the six-item backlog tranche; this increment's four items |
| 14 | **Emitted-form assertion** declared | all | ✓ | the emitted fold-row bytes + the emitted legend lines |
| 15 | **Independent review** names somebody | all | ✓ | §4b — the coordinator + the lens pool |
| 16 | **Evidence files** declared | all | ✓ | 3 artifacts with stored-byte digests |
