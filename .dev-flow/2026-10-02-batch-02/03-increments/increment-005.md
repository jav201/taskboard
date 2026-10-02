# Increment 005 — HLR-206, HLR-207 · the project just left stays open; a finished task says where it went

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`. Flow pinned to rev98.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-02` |
| Increment | `005` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-206 (LLR-206.1), HLR-207 (LLR-207.1 `previous`, LLR-207.2) |
| Acceptance | AT-206, AT-207 · white-box TC-208, TC-209, TC-210 |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**Walking into the next project keeps the one just left open while it fits** (answer UXV-2):
the app remembers the selection's gantt group and the group before it, and the plan offers the
previous group rows right after the selected one, before urgency. On the operator's 80×24
board, stepping from Website Redesign into Mobile App no longer folds Website, and the walk moves
the highlight up twice instead of three times (once at full size, as before) — measured, and
for the operator (D-203). **`]` that finishes a task in the gantt posts a short notice** —
`Build component library done · folded into ✓2 · u undo` (answer D14) — counting the `✓n` of the
task's own group, with archived work while `v` shows it and under a `/` filter. The title is shown
literally: markup off, not escaped (security S-1; a `[/]` title with markup on would crash the
app). Folded from review: one rule for a group's key (`group_key`); a `team.json` colour that is
not a string no longer crashes Setup (security L2).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-207.1, LLR-201.3 | `INBOX_GROUP`, `group_key`, `gantt_group_key`; `gantt_plan(previous=)`; `previous`/`gantt_previous` threaded through `render_gantt`, `_gantt_frame`, `render_view` (both branches), `legend_entries`; Setup colour guard takes non-strings |
| `taskboard/app.py` | source | LLR-206.1, LLR-207.2 | `_gantt_group` / `_gantt_previous`, `_track_gantt_group` (in `refresh_view`), `gantt_previous` to both renders and `HelpModal`; `_notify_folded` from `action_phase_move` |
| `taskboard/modals.py` | source | LLR-207.2 | `HelpModal(gantt_previous=)` passed to `legend_entries` |
| `tests/test_gantt_polish.py` | test | HLR-206, HLR-207, LLR-206.1, LLR-207.1, LLR-207.2 | appended 14 nodes (AT-206, AT-207 ×2, TC-208 ×6, TC-209 ×3, TC-210 ×2) |
| `tests/test_colour_budget_app.py` | test | LLR-201.3 | the bad-colour node parametrized over a bad string and a non-string (+1 arm) |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_gantt_polish.py tests/test_colour_budget_app.py
python -m pytest -q
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | `gantt_plan(previous=)` (TC-209 ×2), the filtered branch (TC-209) | 3 passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-208 ×6 (finishing only; kanban silent; own group with `v`; filter; 3 hostile titles), TC-210 ×2 (memory; the legend asks the same frame) | 8 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-206, AT-207 (80×24), AT-207 (118×30, a pin) | 3 passed |

Gate run on the frozen round-1 tree: `python -m pytest -q -p no:cacheprovider` → **1677 passed in
190.36s, exit 0** (`evidence/inc005-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the increment-004 tree (views, app, modals) with the new tests; then 16 mutants on the increment tree |
| Where it ran | scratch exports (CRLF) |
| Transcript | `evidence/inc005-red.txt` (9 failed, 21 passed); `evidence/inc005-mutations.txt` |
| Restore proven by | per-mutant sha256, `evidence/mutate_bytes.py` (`views.py` `a4688ae7c1788b66…`, `app.py` `bd923308acb6a44b…`, `modals.py` `06cf53b189e3ff8b…`) |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 30 (the 19 increment-004 nodes green, as they must be) |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | regression pins by design: `test_AT_207_at_full_size_the_walk_moves_up_at_most_once` (base also ≤ 1) and `test_TC_210_the_legend_asks_the_same_frame` (base has no previous group). CORRECTED at P4 (qa G-002): only `test_TC_210_the_legend_asks_the_same_frame` is killed by mutants — S2, S4, S6 (`inc005-mutations.txt:70`, `:77`, `:258`); the 118×30 walk is killed by NONE of this battery — it is a regression pin green on base by design, and in increment 006 it became the 118×30 arm of the one AT-207 node |

| Field | Value |
|---|---|
| **RED counterfactual** | 9 nodes RED on the increment-004 tree (no `previous` keyword; no memory; Website folds at `tm6`; no notice) · `evidence/inc005-red.txt` · the TC-210 legend pin RED under S2, S4 and S6 (`inc005-mutations.txt:70`, `:77`, `:258`); the 118×30 walk pin RED under no mutant (corrected at P4, qa G-002) · restore digests in `evidence/inc005-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 16 of 16 KILLED (`mutants_inc005.json` 11/11 + `mutants_inc005_r1.json` 5/5): S1 `previous` ignored, S2 never remembered, S3 the same group overwrites, S4 the modal's legend drops it, S5 the Inbox key collides with "none", S6 `legend_entries` drops it, T1 every move notifies, T2 the kanban notifies, T3 markup on (C-17), T4 escaped and markup off, T5 the count off by one; M1 the count ignores the filter, M2 `v` ignored, M4 always the first group, M5 the filtered branch drops `previous` (code review), L2 the colour type guard removed (security) |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the walk's upward-move counter (AT-207) | the increment-004 fold order | Website folds at `tm6`, the highlight moves up |
| the legend spies (TC-210) | S4, S6 | `asked == [None]` / `seen == [None]` |
| the painted toast (TC-208, `notifications=True`) | T3 (markup on) | `MarkupError` / a parsed title |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the notice | `App._notifications[-1].message` exactly, and the painted `Toast` text | AT-206, TC-208 passed |
| the gantt panel | painted `#board` span rows and `line_map` rows through a 24-step walk | AT-207 passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts, each asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on the increment-004 tree | `.dev-flow/2026-10-02-batch-02/evidence/inc005-red.txt` | `7ace14647259eb331952f8d1094240d699b8bd365fd7b519e9208f44a5942756` |
| mutation battery | `.dev-flow/2026-10-02-batch-02/evidence/inc005-mutations.txt` | `f8e950b9d8e41ed27f276cb3e6de7e76cc654fadef08ee3e082b3420ecb29be9` |
| mutant specs | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc005.json` | `b175a1d8dec2339df388e08f4e487994766dd46e96645148b5d98d8a6104bd95` |
| mutant specs, review round | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc005_r1.json` | `292fd29044afa3956a2d6225011869370e82b45ad198665dda377e7022c30c36` |
| reverse census run | `.dev-flow/2026-10-02-batch-02/evidence/inc005-reverse-census.txt` | `ba77c235e3ad9feef62e81fd2079e631c592d80dbaa15382c422303f78d27201` |
| gate run | `.dev-flow/2026-10-02-batch-02/evidence/inc005-green.txt` | `f95aec3ad181b3b9dcc77d64d038d1d44e6d5f33af70955b8a3afe13ec6ba104` |
| gantt, 118×30 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc005-gantt-118x30.txt` | `388959930d05d501157e8b0337c565e1396c64792bdce42a672b271312c434d3` |
| app, 80×24 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc005-app-gantt-80x24.svg` | `4b4fbc0f96123f05efe36e9ea825b7b7fd357d753483d840bfb0a22a90fc89d1` |

| Field | Value |
|---|---|
| **Evidence files** | 8 artifacts, each cited with its digest (the gantt render at entry is byte-identical to increment 004's — no previous group yet) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no notice for a move that does not finish a task"; "at most N upward moves" |
| If the result is an ABSENCE, what made the search wide enough | Doing→Review, the kanban, a clamped `]`; the full 24-step walk at both sizes |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `assert "tm6" in ids and "ta1" in ids and len(set(ids)) == 25` (the walk reached every task); `assert folded_on_screen` |
| Conjunctive criteria: one mutation per conjunct | T1 (finishing), T2 (the gantt) separately |
| Synthetic instance of the absent case | T1, T2 |
| **Positive control for every probe that returned an ABSENCE** | the same nodes see the notice when the move finishes the task |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | full suite after the edit (`evidence/inc005-reverse-census.txt`: 1673 passed, 0 failed) | none fired: the new keywords default to the shipped behaviour |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | none | did not fire |
| B4 artifact produced here is consumed elsewhere | `render_view(gantt_previous=)` ← `app.py` (refresh, tick); `legend_entries(gantt_previous=)` ← `HelpModal` | both threaded; spies prove both (TC-210) |
| A3 | interface consumed by another module changed | `render_view`, `render_gantt`, `legend_entries`, `HelpModal` gain an optional keyword | defaults keep every existing caller's result (0 reverse-census failures) |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B4 fired (spied), A3 fired (optional keywords, 0 failures), B1/B2/B3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| callers that draw the gantt frame | `render_view(` / `legend_entries(` callers passing `gantt_focus=` | `grep -n "gantt_focus=" taskboard/app.py taskboard/modals.py taskboard/views.py` | 5 | 4 (`app.py` ×3 renders/help, `modals.py` ×1) | `nav_model` — its order does not depend on folding (confirmed by code review) |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1677 = 1662 − 0 + 15` ✓ (14 new nodes + 1 new parametrized arm).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` (rev98 snapshot) · round 1: OK to advance, no HIGH; F1/F2 MEDIUM (the toast's group/`v`/filter and the filtered branch untested — its M1, M2, M4, M5 survived), F3 LOW (the group-key rule written four times), F4 LOW informational (after a view detour or finishing a group's last task, the remembered previous group can be stale — matches LLR-207.2 as written; for the operator), F5 LOW (a TC-210 assertion that could pass both-False) · folded · round 2: OK to advance, M1, M2, M4, M5 and L2 each killed by its intended node; F6 LOW optional (the colour-guard expression's readability) left as is to keep the reviewed set frozen. `security-reviewer` — spawned with `agents/security-reviewer.md` · PASS-WITH-NOTES, 0 HIGH: S-1 verified (markup off, raw title; mutants markup-on and escape+off each fail all 3 payloads); every other new markup path clean; evidence directory clean of the home path; L1 (ESC sequences in titles reach the terminal) and L3 (`state.json` `owner`) pre-existing → BACKLOG; L2 folded here |

## 5 · Risks

- The remembered previous group can be stale after a detour through another view (code review F4) — recorded for the operator.
- The notice reflows at 80×24 and stays for its timeout after `u` (ux UX-6) — P4 walkthrough item.

## 6 · Pending items / spec deviations

- `app._select_first`'s own `group_of` (pre-existing, `None` for the Inbox) is the fourth spelling of the group key — cleanup → BACKLOG.

## 7 · Suggested next task

P4 validation (qa-reviewer + ux-reviewer walkthrough).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 3 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 15 new nodes |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `gantt_plan(previous=)` |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b (round 2) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | optional keywords only, defaults = shipped |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | ids in docstrings |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
