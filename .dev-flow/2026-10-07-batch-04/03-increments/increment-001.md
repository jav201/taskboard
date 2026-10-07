# Increment 001 — HLR-1001 · `The presentation mode (PRES-C behind R)`

> **Where this lives:** the repo, next to the diff it describes —
> `.dev-flow/2026-10-07-batch-04/03-increments/increment-001.md`.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-04` |
| Increment | `001` |
| Lane (if the batch forked) | `none — one lane` |
| Requirement(s) | `HLR-1001 v1 / LLR-1001.1, LLR-1001.2` |
| Acceptance | `AT-1001` · white-box `TC-1001, TC-1002, TC-1003, TC-1004` · unit the `_present_*` renderer helpers (pinned through `render_present`) |
| Agent | `software-dev` (two worker runs, `evidence/inc001-run.log`, `inc001b-run.log`) + coordinator corrections (this package's oracle pin and the `_strip` S1 fix) |
| Date | `2026-10-07` |

---

## 1 · What changed

`R` no longer writes the HTML report — it opens the presentation of the selected
task's project (the focused project when set): the project's gantt field on top,
the brief blocks below (title, dates, phase, the notes paragraph wrapped to the
width, the links line), a `⟦━⟧` cursor across the brief blocks whose task's notes
expand (`←→↑↓`/`hjkl` move it), `x` exporting what it shows to
`reports/present-<slug>-<today>.svg` + `.png` beside the board (the shipped
report destination convention; the PNG through the headless-browser recipe,
degrading to an SVG-only export with a named warning where no renderer exists),
`esc`/`q` leaving. The frame is byte-faithful to the PRES-C oracle at 118×30 and
80×24. The screen is read-only: it draws the board, it never saves it. The shell
CLI `--report` is unchanged.

Two things beyond the worker's code, both by the coordinator:

1. **The byte contract had no shipped test.** The worker validated byte-identity
   ad hoc in the prototype round; the suite pinned nothing. Folded here:
   `tests/present_board.py` (the frozen PRES-C oracle board — the kg_mejoras
   fixture + the NOTES/URLS overlay, marked migrated so the app's startup link
   migration leaves its `depends_on` alone), the two oracle frames under
   `evidence/frames/`, and `tests/test_present.py` (TC-1001/TC-1002 the exact
   rows at both sizes, TC-1003 the S1 hostile payload, TC-1004 the empty
   boundaries, AT-1001 through the shipped surface).
2. **The S1 width law was broken at `_strip`.** TC-1003 caught it: the regex
   "strip tags" measure ate the brackets `_literal` prints literally, `_pad`
   over-padded, the task row grew to 129 cells in a 118 frame — and
   `_present_finish`'s own assert agreed with the wrong number. Fix: `_strip`
   measures through rich's parse (`Text.from_markup(markup, emoji=False).plain`),
   the same `emoji=False` law `to_text` pins (a regex cannot tell a tag from a
   printed bracket; and `emoji=True` would rewrite `:bug:` inside the measure
   while the painters priced it as literal text — the 12 test_cells arms caught
   that first cut). One seam, every `_pad`/`header`/width caller inherits it.

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | HLR-1001, LLR-1001.1 | `render_present` + the `_present_*` geometry/brief/note helpers; `present_paths`, `save_present_svg`, `save_present_png`; `_strip` now measures through rich's parse (`emoji=False`) — the TC-1003 S1 fix |
| `taskboard/app.py` | source | LLR-1001.2 | `PresentScreen` (paint, cursor move, export, close; the read-only law) and `action_present`; the old `action_report` and its `report` action entry are gone (the CLI `--report` keeps `write_report`) |
| `taskboard/keymap.py` | source | LLR-1001.2 | `Key("R", "R", "present", "Present", group="misc", bar=False)` — the report key's seat |
| `README.md` | doc | | the `R` row of the key table + the new Presentation section (Reports now names the shell CLI only) |
| `tests/test_present.py` | test | HLR-1001, LLR-1001.1, LLR-1001.2 | new: TC-1001, TC-1002, TC-1003, TC-1004, AT-1001 |
| `tests/present_board.py` | fixture | LLR-1001.1 | new: the frozen PRES-C oracle board (migrated marks, the renumber notice seen) |
| `tests/test_report.py` | test | LLR-1001.2 | the two R census tests rewritten to the present contract (`test_the_present_key_is_in_the_seat`, `test_pressing_R_opens_the_presentation_read_only`); the CLI `--report` arms untouched |
| `tests/test_keymap.py` | test | LLR-1001.2 | `GLOBAL_ACTIONS`: `report` → `present` |
| `tests/test_markup_sites.py` | test | LLR-1001.2 | AT-403's `R` arm: the presentation opens, `esc` leaves, no report is written |
| `tests/test_markup_census.py` | test | LLR-1001.2 | the EXEMPT tuple naming the presentation seat (same D-405 family as the board seat) |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | `5 modified + 2 added` (uncapped) |
| Doc files | `1` (outside the count) |

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 \
    python -m pytest tests/test_present.py -q
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 \
    python -m pytest tests/test_report.py tests/test_keymap.py \
    tests/test_markup_census.py tests/test_markup_sites.py -q
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 \
    python -m pytest tests/ -q          # the one complete run is the orchestrator's
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (the `_present_*` helpers, pinned through the public `render_present`) | `core` | `TC-1001` · `TC-1002` · `TC-1003` · `TC-1004` (all in `tests/test_present.py`) | 4 passed (`evidence/inc001d-test-present.log`: `5 passed in 3.39s`) |
| **A · white-box** `TC-1001`..`TC-1004` ↔ LLR-1001.1 | `core` | the 4 nodes above | 4 passed (same transcript) |
| **B · black-box** `AT-1001` ↔ US-1001, through the shipped surface | `core` | `test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle` | 1 passed (plus the rewritten census seats: `test_report.py` 10, `test_keymap.py` 16, `test_markup_census.py` 4, AT-403's present arms) |

Full suite: see `04-validation.md` (the orchestrator's one complete run).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M6** — `_strip`'s body restored to the old regex deletion (`re.sub(r"\[/?[^\]]*\]", "", markup)`) |
| Instrument | project code, the coordinator's own hand, driven by `evidence/run-mutations.py`; restore checked by sha256 |
| Where it ran | **my own worktree** — `.claude/worktrees/present-e`, no other session reads it |
| Transcript | `.dev-flow/2026-10-07-batch-04/evidence/inc001c-run.log` (`===== M6 =====` block) |
| Restore proven by | **file hash returned to its pre-mutation value** — `views.py` `e4e300fcbb72…18b197e` before and after |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` on every battery run (C-46) |
| Arms resolved at baseline | `tests/test_present.py` — **5** arms (the `-q` header prints `5 passed` before each mutation) |
| Verdict granularity | per resolved node id — each mutation ran its targeted node(s) with `-x`, never the process exit code |
| Arms that stayed GREEN | **none** — 6 mutations, 6 KILLED (the two SURVIVED first cuts were mutation-design bugs — a no-op `pass` prepend and an arm that read the brief's copy of the title — both fixed and re-run, transcript shows the clean pass) |

Plus the base-tree RED the template's first column asks about: on `HEAD`
(`34bab3c`, before this batch) `views.render_present` does not exist —
`git show HEAD:taskboard/views.py | grep -c render_present` prints `0`, so
`tests/test_present.py` fails at import on the base tree. The worker's own
first-run logs carry the same shape (`inc001-run.log`).

| Field | Value |
|---|---|
| **RED counterfactual** | **M6** — the regex measure back in `_strip` makes THIS increment's own TC-1003 fail (`129 != 118` on the hostile row) · transcript `evidence/inc001c-run.log` · restore digest `e4e300fcbb72…18b197e` |

| Field | Value |
|---|---|
| **Mutation verdicts** | **M1** `_present_title` returns the raw title (no escape/clip) → TC-1003 **KILLED** (the row-label arm: the literal title count drops 2→1) · **M2** the cursor-echo loop emptied → TC-1001 **KILLED** (the frame loses `⟦━⟧`) · **M3** `action_present`'s guard inverted (the screen never opens) → AT-1001 and `test_pressing_R_opens_the_presentation_read_only` **KILLED** · **M4** the cursor move reversed → AT-1001 **KILLED** (the moved-to task's notes do not expand) · **M5** the SVG write skipped → AT-1001 **KILLED** (`svg.is_file()` fails) · **M6** the regex `_strip` back → TC-1003 **KILLED** · arms that stayed GREEN: **none** · registry ids: none (project-code battery, not the flow's mutate tool) · transcript `evidence/inc001c-run.log`, every restore line `OK` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` + the oracle diff (TC-1001/TC-1002) | the M2-corrupted renderer (no cursor echo) | the exact row diff at the first changed line, `exit 1` — `inc001c-run.log` M2 block |
| the width law (`vis == width` per row, TC-1003) | a hostile `[bold]x[/bold]` title via M1/M6 | `AssertionError: (129, '  ▎ [bold]x[/bold] ↗ …')` — `129 == 118` failed, in the M6 block |
| the markup census (TC-401) | the new `PresentScreen._paint` sink before its EXEMPT entry existed | `Textual sinks fed a markup str: app.py PresentScreen._paint update(text <- render_present(…))` — fixed by naming the seat, then GREEN |

| Field | Value |
|---|---|
| **Instrument RED-proof** | `3` instruments, each shown RED on a planted corruption of its mechanism before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the painted frame (the screen's bytes) | AT-1001 reads `#present-frame`'s content and compares it to the stored oracle file | equality with `PRES-C-118x30.txt`, line for line (`5 passed`) |
| `reports/present-website-redesign-<today>.svg` | `'Website&#160;Redesign' in svg_path.read_text(encoding="utf-8")` after an `x`-shaped export (rich's save_svg joins words with `&#160;`) | `True` — and `'missing&#160;tax-rate' in s` (the cursor'd task's notes) → `True`: the SVG carries the frame's text verbatim |
| the PNG (where Edge renders it) | `png_path.read_bytes()[:4] == b"\x89PNG"` | `True` on the operator machine; where no renderer exists the emitted form is the SVG + the named warning toast (AT-1001's `else` arm) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | `3` artifacts, each asserted against the form its producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the 118×30 oracle frame | `.dev-flow/2026-10-07-batch-04/evidence/frames/PRES-C-118x30.txt` | `e55c7c610e4370ffcfeae3a0d0803d767a5a45df74b04c4543d2cc9806c57892` |
| the 80×24 oracle frame | `.dev-flow/2026-10-07-batch-04/evidence/frames/PRES-C-80x24.txt` | `059378904ad2b5467e12af460b064d20dfc678ce2c91907a286c033cfffe95aa` |
| the mutation battery transcript | `.dev-flow/2026-10-07-batch-04/evidence/inc001c-run.log` | `b049a3fffff50589f7c1cee4941014358ed7b77020ea29da491c395128124893` |
| the battery harness | `.dev-flow/2026-10-07-batch-04/evidence/run-mutations.py` | `98de71ef8703edd304b407345fbb4a84298507ba20bc2b9b7592eb9d164be42d` |
| the worker's two runs | `.dev-flow/2026-10-07-batch-04/evidence/inc001-run.log`, `inc001b-run.log` | (from the worker, cited as history) |

| Field | Value |
|---|---|
| **Evidence files** | `5` artifacts at the declared home, the three above cited with the digest of their stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes — (a) the census EXEMPT rests on the absence of an unescaped sink in the render family; (b) AT-1001's "no HTML report written" is an absence |
| If the result is an ABSENCE, what made the search wide enough | (a) the census walks every Textual-importing module's AST, every `update`/`Static`/`notify` sink — the over-broad property is "no unescaped user text reaches a markup sink", and the guard is the D-405 seat family + S1; (b) `glob("*.html")` over the whole `reports/` folder the presentation touched |
| Guard labelled as protecting a CONCLUSION, not a behaviour | TC-1003's hostile fixture is labelled S1 in its docstring; the no-report glob is labelled "the HTML report must not appear" in AT-1001 |
| Conjunctive criteria: one mutation per conjunct | TC-1003 is conjunctive (literal text AND exact width): M1 kills the escape conjunct, M6 kills the measure conjunct — separate mutations, per-conjunct verdicts |
| Synthetic instance of the absent case | the hostile title/notes fixture IS the synthetic unescaped case; for the report absence the synthetic known-present case is the CLI `--report` arm (writes an `.html` on the same tree — the positive control below) |
| **Positive control for every probe that returned an ABSENCE** | (a) M1 (escape removed) → the literal-title probe's count drops 2→1 — the NON-absent output the same probe returns on the known-present case; (b) the CLI `--report` test writes `board-<date>.html` — the same glob probe finds it there, so the empty glob in AT-1001 is the presentation's doing, not a broken probe |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl "render_present\|PresentScreen" tests/` | `test_present.py` (this increment), `test_markup_census.py`, `test_markup_sites.py`, `test_report.py` — all this batch's, no orphan owners |
| B2 file moved on disk | `git status --short taskboard/` | `M` on `views.py`/`app.py`/`keymap.py` — no rename, no reader left behind |
| B3 byte-identical golden captures this source | `grep -rl "PRES-C" tests/` | `test_present.py` only; the frames' home is `evidence/frames/` (cited in the test docstring) |
| B4 artifact produced here is consumed elsewhere | `grep -rn "present_paths\|present-" taskboard/ tests/` | the writer seats (`app.py`, `views.py`) and the AT-1001 assertion — the `.svg`/`.png` are operator-facing files, no in-tree consumer |
| A3 | interface consumed by another module changed | `grep -rn '"present"' taskboard/ tests/` | the keymap action name is consumed by `app.py`'s `action_present` (this increment) and the rewritten census tests; `grep -rn "build_report" tests/` shows the CLI seats untouched |

| Field | Value |
|---|---|
| **Reverse census** | `5` probes run (B1 · B2 · B3 · B4 · A3), each with its command and verdict; 4 hits, every hit re-validated as this batch's own |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| "`R` writes the report" is dead — every seat claiming it must say the presentation contract | every test/doc seat referencing the report key or its toast | `grep -rn "Report written to\|report_key_is_in_the_seat\|pressing_R" tests/ README.md` (run before the first edit) | 6 sites in 5 files | `test_keymap.py`, `test_markup_census.py`, `test_markup_sites.py`, `test_report.py`, `README.md` | 0 — the CLI `--report` seats correctly still say "report" and were verified as the negative set by the same grep |
| the width measure must not eat printed brackets | every width call site (`_pad`, `header`, the per-row gutters) | `grep -c "_strip(" taskboard/views.py` | 20 call sites | 1 — the single `_strip` definition all 20 share | 0 — one seam was the whole population |

| Field | Value |
|---|---|
| **Correction population** | `2` corrections, each enumerated with its method before its first site was edited |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| `action_report` (the R key's old seat) | `grep -rn "action_report" taskboard/ tests/` → 0 hits | yes — the only surviving "report" refs are the CLI's (`write_report`, `--report`), the report's own test file, and the census's historical EXEMPT entries for the modal seats | `taskboard/app.py` (`action_present` at 704); `tests/test_report.py:257` (the CLI arm) |
| `"report"` as a keymap action | `grep -rn '"report"' taskboard/keymap.py` → 0 hits | yes — `Key("R", "R", "present", …)` is the only R seat | `taskboard/keymap.py:136` |

### Signed-balance test ledger

`post = base − deleted + added` → `2534 = 2529 − 0 + 5` ✓ reconciles
(base `2529` = the worktree suite at `34bab3c` + the worker's code, the old R
tests still passing; `+5` = `tests/test_present.py`; the two rewritten R tests
replace two deleted ones 1:1, names swapped, count neutral; the final number is
the orchestrator's complete run cited in `04-validation.md`).

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` (the orchestrator, reviewing the worker's diff) · PASS-WITH-NOTES, 0 HIGH / 2 MEDIUM · both folded into this increment — **N1** the byte contract had no shipped test (folded: `tests/present_board.py` + `evidence/frames/` + TC-1001/TC-1002, and AT-1001 asserting the painted frame equals the oracle through the shipped surface) · **N2** the regex `_strip` broke the S1 width law on hostile linked titles, 129 cells in a 118 frame, with the finish assert agreeing with the wrong number (folded: the rich-parse measure with `emoji=False`, TC-1003, mutation M6 as its standing RED) |

---

## 5 · Risks

- The PNG half of the export depends on a headless browser existing on the
  machine (Microsoft Edge today). Where none exists the user gets SVG + a named
  warning — pinned by AT-1001's conditional arm, but no CI arm exercises the
  missing-renderer path on a renderer-less host (declared, not deferred).
- `PresentScreen._paint` re-renders on every resize; on a pathological board
  (hundreds of open tasks) the per-resize render is the same cost as a view
  repaint — the fold caps it, and the suite's 118×30 render stays in
  milliseconds, but a 4K-resize storm is untested.
- The presentation opens over whatever modal is up (the milestone offer at a
  fresh start); keys stay correct because the screen stack handles priority,
  but the interplay is pinned only for the offer-under-presentation case
  (AT-1001's comment documents the seam).

---

## 6 · Pending items / spec deviations

- None. The `_strip` fix inherits to every view through the one seam; the
  suite's hostile-title arms (test_cells' emoji/shortcode rows among them)
  verify the benign rows stayed byte-true under the new measure.

---

## 7 · Suggested next task

None from this increment — the kg_mejoras plan's next batch is the operator's
call.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 3 / 4 (`taskboard/views.py`, `app.py`, `keymap.py`) |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_present.py` (5 arms) + `tests/present_board.py` — written and green in this increment |
| 3 | Layer 0 written where the criterion applies | `core` | ✓ | the 4 TC nodes + the full-suite run is the orchestrator's (`04-validation.md`) |
| 4 | **RED counterfactual** declared | `core` | ✓ | M6 · `inc001c-run.log` · restore `e4e300fc…` · plus the base-tree import RED (`git show HEAD:taskboard/views.py \| grep -c render_present` → 0) |
| 5 | **Reverse census** declared | `core` | ✓ | 5 probes with commands and verdicts (table above) |
| 6 | `code-reviewer` passed | `core` | ✓ | §4b — `coordinator` · PASS-WITH-NOTES, 0 HIGH / 2 MEDIUM, both folded |
| 7 | No file from another lane touched | all | ✓ | one lane; the parallel cleanup batch's files (`models.py`, the fold row) untouched by this diff |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | `render_view`'s signature unchanged; `to_text` unchanged; the key seat keeps the same shape (only the action name moved, with every consumer in this diff) |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | the frames are read from `evidence/frames/` at test time; the byte claims diff against bytes on disk |
| 10 | Load-bearing emptiness declared, with its synthetic instance | all | ✓ | table above — the hostile fixture is the synthetic instance; M1 its positive control |
| 11 | **Mutation verdicts** declared — **per arm**, inert arms named | all | ✓ | 6 mutations, all KILLED, per-node verdicts, transcript + restore hashes |
| 12 | **Instrument RED-proof** declared | all | ✓ | 3 instruments each shown RED first |
| 13 | **Correction population** declared | all | ✓ | 2 corrections, enumerated before the first edit |
| 14 | **Emitted-form assertion** declared | all | ✓ | 3 artifacts asserted as emitted (frame rows, SVG bytes, PNG magic) |
| 15 | **Independent review** names somebody | all | ✓ | §4b names `coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 3 digests cited above + the worker's two logs |
