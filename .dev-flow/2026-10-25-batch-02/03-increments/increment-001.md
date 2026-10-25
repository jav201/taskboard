# Increment 001 — LLR-2901.1 · `the presentation colours the notes' highlights`

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label.
> **Owed in.** `core` ✓ · `full` ✓
> **Field guide:** `templates/guides/increment-template.md` explains each field below and the rules that read them.
> **Reserved field names** (language-independent, parsed literally): `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`

| Field | Value |
|---|---|
| Batch | `2026-10-25-batch-02` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `US-2901` / `HLR-2901..HLR-2905` / `LLR-2901.1, LLR-2901.2, LLR-2902.1, LLR-2903.1, LLR-2904.1, LLR-2905.1` |
| Acceptance | `AT-2901` · `AT-2902` · `AT-2903` · `AT-2904` · `AT-2905` (the regression pin; white-box folded into the layer-0 arms) · unit `test_L0_*` (7 nodes) |
| Agent | `software-dev` (spawned implementer sub-agent; the orchestrator verified) |
| Date | `2026-10-25` |

---

## 1 · What changed

The presentation's note rows — the gantt cursor note (view 1), the split view's blocks (view 2) and
their `x` exports — now colour the notes' `==..==` / `!!..!!` / `++..++` highlights through the one
tokeniser, `views.highlight_segments`: the markers are dropped, each span is painted in its tone
(`soon`/`over`/`green`), the unmarked text keeps the presentation's base tone `ink`, a mention inside
any span stays bold pink, and every piece of note text is escaped before it enters markup. The wrap
measures the marker-free text (a highlighted row is not cut early) and a span split by a row boundary
keeps its tone on every row. The user reaches this by opening the presentation (`R`) and reading any
task's notes, views 1 and 2, and pressing `x`.

Mechanism (per the sealed PDR-2026-10-25-batch-02): `present_note_lines` tokenises each paragraph
before wrapping (same `textwrap`/`_wrap_cells` regime on the marker-free plain, so marker-free
geometry is byte-identical) and returns rows of `(lead, [(segment, tone)])`; the new `_tone_row`
helper re-attributes each wrapped row to its tones (two-pointer walk; only whitespace-class
divergences allowed); `_paint_marks` keeps its name with the new `(pieces, marks)` signature —
mentions bold pink, every group escaped, per-tone colouring; `_present_note_markup` clips pieces by
cells before painting; `_present_cut`'s `k == 1` seat cuts the composed row on a glyph boundary first,
then paints piece by piece. The export functions are untouched — the SVG/PNG render the same composed
frame the screen shows (PH-4).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2901.1, LLR-2901.2, LLR-2902.1, LLR-2904.1 | the note pipeline: tokenise-before-wrap, `_tone_row`, `_paint_marks(pieces, marks)`, the clip and the `k==1` cut seat |
| `tests/test_present_note_highlights.py` | test | HLR-2901, HLR-2902, HLR-2903, HLR-2904 / LLR-2901.1, LLR-2901.2, LLR-2902.1, LLR-2903.1, LLR-2904.1 | new — 20 nodes (AT-2901..AT-2905 + 10 layer-0 arms) |
| `tests/test_present_views.py` | test | HLR-2905, LLR-2905.1 | the LED-2905.2/LED-2905.3 oracle updates: row-shape equality + 13 row-shape consumers |
| `tests/test_people_look.py` | test | HLR-2905, LLR-2905.1 | the LED-2905.2/LED-2905.3 oracle updates: 3 row-shape consumers |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 3 (uncapped) |
| Doc files | 0 |

- Frozen set byte-identical (verified by `git diff` on the commit): `highlight_segments`, `_wrap_cells`, `_marks_re`, `mention_marks`, `present_mentions`, `save_present_svg`, `present_paths`, `present_all_export`, `render_present`, `render_present_all`, `_present_scrolled`, `_present_window`, `HEX`, `c`, `vis`, `clip`, `fit`.

## 3 · How to test

```bash
env -u NO_COLOR python -m pytest -q tests/test_present_note_highlights.py
env -u NO_COLOR python -m pytest -q tests/test_present.py tests/test_present_polish.py tests/test_present_views.py tests/test_present_all.py tests/test_people_look.py tests/test_highlight_segments.py tests/test_markup_census.py tests/test_markup_sites.py tests/test_edit_window.py
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` | `test_L0_tone_row_*` (5), `test_L0_marker_free_twin_wraps_identically` (1), `test_L0_cut_seat_k1_paints_lead_span_and_tag` (1) | 7 passed (`suite-001.txt`) |
| **A · white-box** | `core` | folded into the layer-0 arms (the LLR mechanisms are unit-pinned; the ATs observe through the shipped surface) | 7 passed |
| **B · black-box** | `core` | `test_AT_2901_*`, `test_AT_2902_*[118x30, 80x24]`, `test_AT_2903_*`, `test_AT_2904_*`, `test_AT_2905_the_regression_pin` | 10 passed |
| layer-0 (post code-review) | `core` | `test_L0_unicode_whitespace_at_wrap_boundaries`, `test_L0_unicode_whitespace_fuzz_pin`, `test_L0_note_markup_clip_never_exceeds_its_width` | 3 passed |
| regression (affected suites) | `core` | the 9 presentation/markup suites | 200 passed (`suite-affected.txt`) = the base_ref baseline (`baseline-affected.txt`) |
| AT-2905's full certification | P4 | the complete suite in 3 sequential chunks | owed at P4 (`04-validation.md`) — the pin node is the disk anchor |

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the note pipeline bypasses `highlight_segments` (rows painted from the raw text) — the commission's mandated mutation for AT-a |
| Instrument | project code, mutated by hand via the battery script `.scratch/mutation_battery.py` (kept beside the transcripts), run by the spawned implementer in this tree; the orchestrator re-verified the restore hashes |
| Where it ran | this worktree, the increment tree; no other session reading |
| Transcript | `evidence/mutation-001.txt` — arm (a): AT-2901 RED, `12 marker chars, 0 tone colours` reproduced |
| Restore proven by | file hash: final `taskboard/views.py` md5 `52bdb41e…` equals the pre-battery value, recorded per arm in the transcript |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` on every run |
| Arms resolved at baseline | 22 in the battery's node set (16 new + the pinned regression nodes the arms touch); expected-arm counts asserted per arm in the script |
| Verdict granularity | per resolved node id, recorded per arm |
| Arms that stayed GREEN | none |

| Field | Value |
|---|---|
| **RED counterfactual** | `taskboard/views.py`, the tokenise step of `present_note_lines` bypassed (raw text painted) · `evidence/mutation-001.txt` (both the pre-F1 run and the POST-F1 re-run against the shipped bytes) · restore digests hash-returned per arm; the post-F1 final md5 `778eb68a…` equals the tree's value |

| Field | Value |
|---|---|
| **Mutation verdicts** | AT-2901 node: tokenise bypassed · KILLED · none green · `evidence/mutation-001.txt` · restore md5 `52bdb41e…` · AT-2902 nodes (2): the wrap restored to marker-counting (`plain := body`) · KILLED · none green · same transcript/digest · AT-2903 node: tone hexes stripped at `save_present_svg` · KILLED · none green · same transcript/digest · AT-2904 mention arm: mention pass dropped inside the toned paint · KILLED · none green · same transcript/digest · AT-2904 hostile arm: one `escape` removed · KILLED · none green · same transcript/digest · layer-0 arms (2 failed of 3 resolved): `soon`→`over` permuted in the matcher · KILLED · the surviving arm is the alarm-path node, which asserts the AssertionError and stays green by design (named here per the C-40 rider) · same transcript/digest |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the mutation battery script | a mid-run Windows cp1252 decode crash left mutation (b) APPLIED | the first run died mid-arm with the mutation live; the script now exits non-zero per arm, appends per-arm, and finally-restores — the harness's own failure mode was observed and hardened before the clean run (`mutation-001.txt` header) |
| the new AT nodes | each of the six battery mutations (mechanism-level corruptions, not verdict edits) | per-arm RED verdicts as tabulated above |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments, each shown RED before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the `x` SVG of view 2 (`reports/present-…-split-….svg`) | `test_AT_2903_*` reads the file's BYTES: the three tone hexes present, no `==`/`!!`/`++` run, the words inside the spans; a hostile note's `<`, `&`, `<script>` reach the file only as `&lt;`/`&amp;` — 0 raw `<script` bytes | passed (`suite-001.txt`); the predicate is written against the file, not the screen's memory |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 1 artifact (the exported SVG), asserted against its emitted bytes |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| new-module suite | `.dev-flow/2026-10-25-batch-02/evidence/suite-001.txt` | `b490c87fceaa76daa741ee27da5da3aa1579b82a79f56507bb77fe142609e6c1` |
| affected-suites run | `.dev-flow/2026-10-25-batch-02/evidence/suite-affected.txt` | `7540251b890e58245f6299eef3b39c78132cf86390d92efa7ccd4384f3526ef0` |
| mutation battery | `.dev-flow/2026-10-25-batch-02/evidence/mutation-001.txt` | `1fe7406e8fef3825a17f0980d7a980339f6bfee1563eb64a6c9b3c3b1eff61a2` |
| base_ref baseline | `.dev-flow/2026-10-25-batch-02/evidence/baseline-affected.txt` | `55713568416391d983226288c43828fe7322bf84de37f442f308f5878703b9f0` |
| P1 RED probes | `.dev-flow/2026-10-25-batch-02/evidence/red-p1.txt` | `bf626f784e5c7a77dbeef439bf53e6e95277a6465f5dcfa0a775fd0b296347e0` |

| Field | Value |
|---|---|
| **Evidence files** | 5 artifacts, each at the declared home with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes — "no byte oracle keys on marker text" (HLR-2905) and "no test imports `_paint_marks` with the old signature" |
| If the result is an ABSENCE, what made the search wide enough | repo-wide greps over `tests/` for the three marker runs and for `_paint_marks` (recorded in `02-review.md` round 2 and in the P3 census below) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_AT_2901_*`'s marker-run assertion + the style-pin arm (a marker-free row still paints `#e6edf3`) — labelled in the node docstring as the HLR-2905 pin |
| Conjunctive criteria: one mutation per conjunct | the AT-2904 hostile arm's conjuncts (0 `\x1b` bytes · no exception · the red style never applies) each have their own battery mutation (escape removal reddens the exception/leak conjunct) |
| Synthetic instance of the absent case | the new module's fixtures hold the markers (`==a== !!b!! ++c++`, unclosed `!!`) — the absent-in-the-oracles case is present in the new tests |
| **Positive control for every probe that returned an ABSENCE** | the marker-run grep DOES find the markers in `tests/people_round_fixture.py` (N_EVAL/N_GOLDEN) — the same probe returns hits on the known-present case, so its emptiness over the asserting tests is a measurement, not a blind spot |

### Reverse census — trigger family B, and A3

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl highlight_segments tests/` → `tests/test_edit_window.py`, `tests/test_highlight_segments.py` (both own OTHER requirements; the tokeniser is frozen and untouched — re-validated green in the affected run) · `grep -rln "present_note_lines\|_present_cut\|_present_note_markup\|_paint_marks" tests/` → `tests/test_people_look.py`, `tests/test_present_polish.py`, `tests/test_present_views.py` | every hit re-validated: the 16 row-shape consumers updated under LED-2905.2/LED-2905.3; `test_present_polish.py` needed no change (asserts frames, not rows) — green |
| B2 file moved on disk | n/a — no file moved (probe not fired, declared) |
| B3 byte-identical golden captures this source | `tests/goldens/` does not exist; the byte oracles are `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-*.txt` compared via `.plain` — all marker-free boards, re-validated green (TC-1001/1002, TC-1803, TC-1807) |
| B4 artifact produced here is consumed elsewhere | the `x` SVG/PNG is a user artifact; no component consumes it (probe run over `taskboard/`: only `app.py`'s export action writes it) |
| A3 interface consumed by another module changed | `grep -rn "present_note_lines\|_paint_marks" taskboard/ --include=*.py` outside views.py → no hits; the row type is internal to views.py + tests |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run (B1, B3, B4, A3 with hits re-validated; B2 declared not fired) — the census the P2 round named and the increment completed, incl. the 16 consumers LED-2905.3 records |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the row-type change's consumers | tests asserting or hand-building the old `(lead, text)` row shape | `grep -rln "present_note_lines\|_present_cut" tests/` + the suite run's failure list | 16 nodes in 2 files (the two LED-2905.2-authorised files) | 16 | 0 — all consumers updated; no marker-content oracles existed to leave |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated at P2 (census) and completed by the P3 suite run (16 nodes) before the last site was edited |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|---|---|---|---|
| the old `_paint_marks(txt, marks)` two-arg plain-text form | `grep -rn "_paint_marks" taskboard/ tests/` → only the new `(pieces, marks)` definition + its call sites; no test imports it | yes | `taskboard/views.py` (definition + 2 call sites); zero test hits |
| the old `(lead, text)` row asserts | `grep -rn 'lead + txt\|x for _, x in' tests/` | yes — surviving hits all unwrap pieces | `tests/test_present_views.py:92-100,189-190,362-364` |

### Signed-balance test ledger

`post = base − deleted + added` → `post = 200 − 0 + 16` → the affected suites hold 200 (baseline) and the new module adds 16: `200 + 20 = 220` green across the census — 200 in the affected suites (base line held) and 20 in the new module (`suite-001.txt`: 16, then 17, then 20 passed across the increment's three states; the final 20 is the figure of record).

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · BLOCK on F1 (HIGH: the tone matcher's ASCII whitespace test let textwrap-dropped NBSP/em-space crash the render — reachable by legal note text), F2 docstring drift, F3 a latent one-cell ellipsis overflow, F4 the lost annotation · the fixes landed RED-first in commit abe324c (isspace() both sides, three-draw docstrings, the budget guard, the annotation; three new RED-discriminating arms) · the battery re-ran against the shipped bytes, 6/6 RED, final md5 `778eb68a…` · the reviewer's re-read of the fixed diff DISCHARGED F1-F4 (executed probes incl. 80k fresh fuzz trials, zero crashes; the alarm still fires on non-whitespace mutations) and returned OK-TO-ADVANCE with one LOW note (N1: the three new arms' pre-fix RED is asserted in the commit message, not transcribed — noted here so the DDR does not trip on it; the battery re-run and the boundary arm's replay-evidenced RED carry the weight) |

---

## 5 · Risks

- The `_tone_row` matcher allows whitespace-class divergences only; a future `textwrap` behaviour change (new break class) would trip the AssertionError in the render path — loud, not silent, and pinned by the layer-0 alarm arm.
- Notes with tabs: `textwrap.expand_tabs` draws one tab as several spaces; the matcher absorbs it (documented third class, whitespace-internal). Wide-glyph rows keep `_wrap_cells` semantics (unchanged).
- The 80x24 regime's split columns are narrow; a highlight hugging the column edge is clipped by cells with `…` in its tone — the clip mirrors `clip()`'s existing ellipsis contract.

## 6 · Pending items / spec deviations

- LED-2905's Q5 pin (baseline executed at P3, pinned in `04-validation.md`): the full suite is run ONLY at P4 per the operator's standing rule; the pre-increment baseline is therefore the 9 affected suites (200 passed, `baseline-affected.txt`) and the P4 chunks pin the exact totals. Deviation named here; the P4 record reconciles baseline + new nodes.
- The battery script lives at `.scratch/mutation_battery.py` (git-excluded scratch, deleted at close) — its transcript is the evidence of record.

## 7 · Suggested next task

The DDR (design/DDR-2026-10-25-batch-02.md), then P4 validation.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | ≤4 source files | ✓ | §2: 1 source file |
| 2 | Tests written in this same increment | ✓ | `tests/test_present_note_highlights.py` (20 nodes) |
| 3 | Layer 0 where it applies | ✓ | 7 layer-0 arms (`suite-001.txt`) — the units are cyclomatic ≥3 (matcher/cut/clip) and cross the declared pipeline boundary |
| 4 | RED counterfactual | ✓ | §4: tokenise bypass · `mutation-001.txt` · restore md5 `52bdb41e…` |
| 5 | Reverse census | ✓ | §4: 5 probes, B2 declared, hits re-validated |
| 6 | `code-reviewer` passed | ✓ | §4b: BLOCK → fixes → re-read OK-TO-ADVANCE, 0 HIGH open |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | frozen set byte-identical (`git diff` verified) |
| 9 | Coverage verified on disk | ✓ | transcripts hold 200 + 20 passed |
| 10 | Load-bearing emptiness | ✓ | §4 table + positive controls |
| 11 | Mutation verdicts | ✓ | §4: 6 arms, per-node verdicts, one designed survivor named |
| 12 | Instrument RED-proof | ✓ | §4: 2 instruments |
| 13 | Correction population | ✓ | §4: 1 correction, enumerated P2, completed P3 |
| 14 | Emitted-form assertion | ✓ | §4: the SVG bytes |
| 15 | Independent review | ✓ | §4b: `code-reviewer` · OK-TO-ADVANCE |
| 16 | Evidence files | ✓ | §4: 5 digests |
