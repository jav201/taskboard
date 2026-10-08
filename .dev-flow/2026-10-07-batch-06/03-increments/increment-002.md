# Increment 002 — HLR-1201 · the chain map admits every open task (the `○` tiles + the oracle amendment)

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
> `.dev-flow/2026-10-07-batch-06/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-06` |
| Increment | `002` |
| Lane (if the batch forked) | `none — one implementing session, two increments serialized (the single brief owned views.py for both, task 1 then task 2; no two live briefs ever wrote the same file)` |
| Requirement(s) | `HLR-1201` (+ `LLR-1201.1` · `LLR-1201.2`) — riding **LED-2026-10-07-batch-06.1** (the C-2b oracle amendment) |
| Acceptance | `AT-1201` — the app arms (L links a tile on the map · x returns a tile to `○` · the nav reaches a tile) · `TC-801`/`TC-802` byte-exact against the AMENDED frames at both sizes · the amended `TC-810` (the cap counts chains AND tiles) · unit: `_chainmap_plan`'s admission + the fold's cap branch with tiles |
| Agent | `software-dev` — DeepSeek V4 Pro (one session, both increments) |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

**The chain map is now the place where chains are born.** Every open task of a visible project
paints: linked tasks as today (chains, meta rows, the critical chain, the per-band `dates` switch),
and every open UNLINKED task as a one-row `○` tile at depth 0 in its project's band — the legend's
existing "open chain head" mark — each tile selectable and reachable by the arrows/`j`/`k`.
`L` on any tile (or chain row) opens the shipped LinkPicker and applies the pick as the task's
incoming link — the tile joins that chain on re-render; `x` unlinks the first incoming link and the
task REMAINS an `○` tile, visible and re-linkable, never vanished. The selection strip names an
`○` selection's truth: `◂ waits on  nothing yet` / `▸ unblocks  nothing waits on it`
(`views.py:5954` and its `ft2` sibling — the shipped fallback forms an `○` selection now reaches).
The inert `no links` row survives ONLY for a project with no open work at all, and `?` on the map
gained the bullet `○ an open task with no links yet — L starts its chain here`
(`views.py:6927-6928`).

**The oracle amendment (LED-2026-10-07-batch-06.1).** The `○` tiles move every band's bytes, so the
C-2b oracle frames AMEND: the amended frames are THIS renderer's bytes on the SAME frozen fixture
(`kg_board.shifted` + Data Warehouse `together`, the frozen calendar — exactly as `tests/test_chainmap.py`
renders), stored at `.dev-flow/2026-10-07-batch-06/evidence/frames/C-2b-118x30.txt` and
`C-2b-80x24.txt` (UTF-8, CRLF). `tests/test_chainmap.py`'s `FRAMES` path moved there citing the
LED; the sealed batch-02 frames stay history. Frame deltas at both sizes: every band gains its
`○` tile rows after its chains; Ops' inert `─▌Ops & Security  5 open · no links ───…` row is GONE
(Ops is a `○`-tile band now — its five open tasks would paint as tiles, and under the fold law the
Ops band folds out at both pinned sizes); at 80×24 Data Warehouse folds out too (its two tiles grew
the band past the 24-row body).

Mechanism, one source file (`taskboard/views.py`): `_chainmap_plan` (`views.py:5551`) bands are now
`(project, linked, unlinked)` — `unlinked` = the project's open unlinked tasks, FIFO by due via the
shipped `sort_by_due` (`views.py:559`), soonest first, undated last; the admission guard
`if ts or unlinked:` (`views.py:5581`) sends only a no-open-work project to the inert row;
`_chainmap_open_tile` (`views.py:5751`) paints the one-row tile with the chain-head chrome
(`○`, title, due chip, late mark — no connectors, no meta row), clipped and escaped through the
shipped `_ChainmapCanvas` seams (its `line()` escapes every run, `views.py:5659-5668`); the fold is
tile-aware — tiles join the band's draw order after its chains, take part in the fold, and the cap
counts them: `tail_n = (nslot - limit) + (n_open - n_tiles)` (`views.py:5869`), with only painted
rows reaching the `line_map`; `_chainmap_nav` (`views.py:6006-6014`) admits the tiles at the
depth-0 column after the band's chained heads, so the cursor can rest where the view paints (the
F-3 law). The app seats ride SHIPPED paths — `L` → `action_link` → LinkPicker → `link_tasks`
(verified against a FIRST incoming link: `depends_on` goes `[] → [pred]`), `x` → `_chainmap_unlink`
→ `unlink_tasks`; **app.py is untouched**.

---

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | HLR-1201 · LLR-1201.1 · LLR-1201.2 | `_chainmap_plan`'s 3-tuple bands + FIFO-by-due admission + the `bare` guard (:5551, :5581); `_chainmap_open_tile` (:5751); the tile-aware fold + `tail_n` counting chains AND tiles (:5869); the selection fallback admitting tiles; `_chainmap_nav` admitting tiles at depth 0 (:6006-6014); the chainmap help bullet (:6927-6928) |
| `tests/test_chainmap.py` | test | LLR-1201.1/.2 — pinned by AT-1201 + TC-801/TC-802/TC-810 | `FRAMES` moved to the amended home citing LED-2026-10-07-batch-06.1 (docstring + :30); TC-810 amended in place (the fixture, below); 3 new unit arms (the tile paints + is selectable · the `no links` row only for no-open-work · the nav reaches a tile in band order) |
| `tests/test_chainmap_app.py` | test | LLR-1201.2 — AT-1201 | 3 new app arms (`test_L_links_an_open_tile_on_the_map` · `test_x_unlinks_a_linked_tile_back_to_an_open_tile` · `test_nav_reaches_an_open_tile`); AT-802's two pilots resized (118,30) → (118,32); AT-801c reselects API's `ta4` (the old fixture growth removed) — both named below |
| `.dev-flow/2026-10-07-batch-06/evidence/frames/C-2b-118x30.txt` | generated | LLR-1201.1 | the AMENDED oracle — this renderer's bytes on the frozen fixture, CRLF (sha256 below) |
| `.dev-flow/2026-10-07-batch-06/evidence/frames/C-2b-80x24.txt` | generated | LLR-1201.1 | the AMENDED oracle at 80×24, CRLF |
| `.dev-flow/2026-10-07-batch-06/evidence/gen_frames.py` | generated | LLR-1201.1 | the frames' generator — renders exactly as the test renders, freezes the calendar, writes CRLF |
| `.dev-flow/2026-10-07-batch-06/evidence/c2b.json/board.json` | fixture | LLR-1201.1 | the generator's saved fixture board (kg shifted + DWH `together`) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 (outside the count) |

- One source file: the admission, the tile, the fold arithmetic, the nav, and the help bullet all
  live in the chainmap region of views.py; the app seats needed no new code (the shipped picker
  path already handled a first incoming link — premise P-1).

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_chainmap.py tests/test_chainmap_app.py -q     # 19 passed
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python .dev-flow/2026-10-07-batch-06/evidence/gen_frames.py               # regenerates the amended frames
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (`_chainmap_plan`'s admission — the 3-tuple bands, FIFO-by-due, the bare guard; the tile-aware fold's cap branch — cyclomatic ≥3) | `core` · `full` | `test_an_open_unlinked_task_is_a_selectable_open_tile` · `test_the_no_links_row_only_for_a_project_with_no_open_work` · `test_the_nav_reaches_an_open_tile_in_band_order` + the byte-exact `TC-801`/`TC-802` + the amended `TC-810` | 6 nodes passed (mutation-proven — M9/M10/M11 below) |
| **A · white-box** `TC-801`/`TC-802` ↔ LLR-1201.1 (the amended oracle) · `TC-810` ↔ the fold law | `core` · `full` | the frame arms + `test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole` | byte-exact vs the amended frames at 118×30 and 80×24; the cap `+3 more ↓` exact (1 chain + 2 tiles); the zero-fit band still drops whole |
| **B · black-box** `AT-1201` ↔ US-1201, through the shipped surface | `core` · `full` | `test_L_links_an_open_tile_on_the_map` · `test_x_unlinks_a_linked_tile_back_to_an_open_tile` · `test_nav_reaches_an_open_tile` | 3 nodes passed (picker opens on the map → pick lands → the tile joins the chain; `x` leaves an `○` tile; `down` rests on a tile) |

The session's targeted run held `tests/test_chainmap.py tests/test_chainmap_app.py` at **19 passed,
0 failed** (`evidence/inc001-run.log`), and the two complete green runs over the settled tree
passed **2566 / 2566** (447.08s and 422.53s, same log) — "see 04-validation" for the close number;
the orchestrator's C-25 owns the ONE final clean-tree run.

### The layout-driven test updates — named honestly

Three pinned tests reddened when the tiles landed, **by LAYOUT, not by mechanism**: the tiles add
rows to every band that has open unlinked tasks, and the shipped fold law (batch C / TC-810) then
folds bands at terminal sizes that used to fit. Each update changed a SIZE or a SELECTION or a
FIXTURE — never a law's threshold:

- **TC-810** (`tests/test_chainmap.py:187-233`): part (1)'s fixture is now **pdwh-only with 6 added
  chains** (the base chain + 6 + the 2 open tiles no longer fit at 80×24), asserting the exact
  `+3 more ↓` tail (1 folded chain + 2 folded tiles) and that the folded chains AND tiles never
  reach the `line_map`. On the pre-amendment whole-board fixture, Data Warehouse's band — two tiles
  taller — now drops WHOLE at 80×24, so the old fixture could no longer exercise a PARTIAL band
  deterministically. The mechanism under test (the cap + the drop-whole law) is intact and pinned
  harder: the cap's N now discriminates chains from tiles.
- **AT-802** (`tests/test_chainmap_app.py:162,227`): the two `run_test` pilots resized
  `(118, 30)` → `(118, 32)` — Data Warehouse's band grew two tile rows and folded at the old
  height. Every rule-cycle and bump assertion is unchanged.
- **AT-801c** (`tests/test_chainmap_app.py:318-341`): reselects **API's `ta4`** (drawn at 80×24,
  folded at 80×18). The old arm grew its fixture by 4 added Data Warehouse chains to force `td4`'s
  fold at 80×18; with the tiles, Data Warehouse no longer fits even at 80×24, so the growth is
  removed and the one-refresh heal is exercised on API's chain instead. The end-state assertion
  (healed selection, one refresh) is unchanged.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M9 (the `○` admission dropped):** `_chainmap_plan`'s `unlinked = sort_by_due(...)` → `unlinked = []` — the pre-law renderer: bands carry only their chains |
| Instrument | project code: the coordinator's byte-level mutation runner (`evidence/mutations.log` — byte-anchored, restores hash-verified) |
| Where it ran | **my own tree** — the MAIN checkout (the batch's single lane; the battery is the coordinator-run close-out set, executed on this tree) |
| Transcript | `evidence/mutations.log` M9 — on `tests/test_chainmap.py` (the whole file, 11 nodes): `6 failed, 5 passed` — "the amended TC-801/TC-802 frames diff (the `○` rows are gone) plus the tile arms" |
| Restore proven by | **file hash returned to its pre-mutation value** — `evidence/mutations.log`: "All four restores returned OK (file hash identical before/after)"; views.py's hash at this close `12b5059f…2e8e` |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **11** — `pytest tests/test_chainmap.py --collect-only -q` (8 pre-batch arms + 3 new) |
| Verdict granularity | the battery's recorded granularity for M9 is the file-level count with the failing FAMILY named (frames diff + tile arms); M11/M12 carry node-level granularity in the same transcript |
| Arms that stayed GREEN | the 5 GREEN arms are the untouched-law arms whose assertions do not touch the admission — the greyscale census (TC-803), the header counts (TC-804 — the `‹m› open not linked` count is computed from the project's tasks, not the drawn tiles), the hostile title (TC-807), the deep-chain no-crash (TC-809) and the cycle law (TC-808) |

M9 doubles as this increment's RED counterfactual for the ORACLE AMENDMENT: without the renderer
change, the amended frames cannot match — the increment's own new assertions (TC-801/TC-802
byte-exact, the tile arms) fail by construction, which is exactly the `6 failed` the transcript
records.

| Field | Value |
|---|---|
| **RED counterfactual** | M9 — `_chainmap_plan`'s admission emptied (no `○` tiles) · the amended frames cannot match without the renderer change · transcript `evidence/mutations.log` M9 (`6 failed, 5 passed`) · restore digest: all four restores `OK`, views.py at `12b5059f…2e8e` |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node, from the transcript: **M9** · KILLED — the frames-diff arms + the tile arms (6 failed; the 5 GREEN arms named above) · **M10** · KILLED — `if ts or unlinked:` → `if ts:` (bare rows despite open work): `3 failed, 8 passed` on `tests/test_chainmap.py`, "the arms pinning 'the `no links` row only for a project with no open work'" — with the guard dropped, a tiles-only band vanishes and the no-open-work law's arms redden; the 8 GREEN arms are the file's remaining nodes, every one whose fixture bands all carry linked chains (the no-links arm is the one that reddens by name; the frame arms' bytes carry the same law) · **M11** · KILLED — `tail_n = (nslot - limit) + (n_open - n_tiles)` → `tail_n = (nslot - limit)` (the cap's N drops the tiles): `1 failed` on `test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole` — "the cap count is exact over chains AND tiles" · inert arms: none — every mutant reddened at least one named arm; M12 (increment 001) per-node with its GREEN arms named there · registry: no `docs/tools/devflow-mutants.json` battery in this repo — M9-M12 are the batch's own counterfactuals from the coordinator-run battery · transcript `evidence/mutations.log` · restore digest: `OK` (hash-identical) for all four |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M9's mutant (no tiles) | `6 failed, 5 passed` — the amended-frame arms diff against frames that still carry the `○` rows (`evidence/mutations.log` M9) |
| `pytest` (the suite) | M10's mutant (bare rows despite open work) | `3 failed, 8 passed` — the no-open-work law's arms (`evidence/mutations.log` M10) |
| `pytest` (the suite) | M11's mutant (the cap N drops tiles) | `1 failed` on TC-810 — `+3 more ↓` painted as `+1` (`evidence/mutations.log` M11) |
| the hostile-title probe | a tile whose title is a doubled `[bold]…[/bold]` string, 80 cells | the painted row is `' ○ A [bold]very[/bold] long hostile title that runs well past any tile wi… Oct 5'` — width exactly 80, the bracket escaped (S1 through the shipped canvas seams); TC-807 stayed green (`evidence/inc001-run.log`) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown RED (or discriminating) before its first PASS was believed (transcripts in `evidence/mutations.log` · `evidence/inc001-run.log`) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

**The amended C-2b frames ARE the emitted bytes** — not hand-authored. The assertion, run against
the emitted form:

1. `python .dev-flow/2026-10-07-batch-06/evidence/gen_frames.py` renders
   `views.render_chainmap(b, False, "tm3", TODAY, width=w, height=h).plain.split("\n")` on the
   frozen fixture (exactly the test's own render path) and writes CRLF.
2. What it returned — verified at rest (`evidence/inc001-run.log`):

   | Frame | Rows | Line endings | SHA-256 |
   |---|---|---|---|
   | `.dev-flow/2026-10-07-batch-06/evidence/frames/C-2b-118x30.txt` | 30 | CRLF ×30, no lone LF | `cd955e185f60282aa9fe6297915370931ff0043079775462a3817e956aac56f3` |
   | `.dev-flow/2026-10-07-batch-06/evidence/frames/C-2b-80x24.txt` | 24 | CRLF ×24, no lone LF | `227a2ced15770d006e359474b7c0dbdc07acc71f957b4af253fb50d1f790be58` |

3. `tests/test_chainmap.py`'s `_frame()` reads them back and TC-801/TC-802 assert the painted rows
   byte-exact at both sizes → `19 passed` across the two chainmap files.

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the amended C-2b oracle frames (118×30 · 80×24) | regenerated by `gen_frames.py`; byte-compared by TC-801/TC-802 via `_frame()` | the digests above; `19 passed` |
| the painted `○` tile row | the tile arm renders the kg fixture at 118×30 and reads `rows[line_map["tw3"]]` | `○ Fix checkout 500 error ▲2d` — the late mark rides the tile; the row is in the `line_map` (selectable) |
| the strip for an `○` selection | rendered with the selection on `tw3` (visible in the session's painted canvases, `evidence/inc001-run.log`) | ` ◂ waits on  nothing yet` / ` ▸ unblocks  Build component… (starts 5d early)` — the shipped fallback forms, now reachable from a tile |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted against the form its producer emitted (the frames byte-exact, the painted tile row, the strip) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the AMENDED oracle frame 118×30 (CRLF) | `.dev-flow/2026-10-07-batch-06/evidence/frames/C-2b-118x30.txt` | `cd955e185f60282aa9fe6297915370931ff0043079775462a3817e956aac56f3` |
| the AMENDED oracle frame 80×24 (CRLF) | `.dev-flow/2026-10-07-batch-06/evidence/frames/C-2b-80x24.txt` | `227a2ced15770d006e359474b7c0dbdc07acc71f957b4af253fb50d1f790be58` |
| the frames' generator | `.dev-flow/2026-10-07-batch-06/evidence/gen_frames.py` | `e165eabdf213d69f6eca731e84c709b1a11dc63d4bb02f0e68e543ba3223bce3` |
| the generator's fixture board | `.dev-flow/2026-10-07-batch-06/evidence/c2b.json/board.json` | `878599d97e95932a23463c6857ea8050f60ab6af9fb7a1d7719764cb4f77d2d0` |
| the close-out mutation battery M9-M12 | `.dev-flow/2026-10-07-batch-06/evidence/mutations.log` | `f74656736101c6a3fe6cf4a6305142d4cc35127b82511ca841e11b35aef7b3ab` |
| the session's run log (targeted verifies · the emitted canvases · two full-suite greens at 2566 · the report) | `.dev-flow/2026-10-07-batch-06/evidence/inc001-run.log` | `3a5f95c61a9811e7790f448b8da0965a86168578020ddd7cd0ef0bb543f114e3` |

The amended test files' stored bytes (their home is the `tests/` home `artifact_homes.tests`
declares — cited for the record, not as evidence-home artifacts): `tests/test_chainmap.py`
sha256 `0ea347be5d943de176440256eccfbec2b8c1efb3f309020ce8d07169e632ea9f` ·
`tests/test_chainmap_app.py` sha256
`607df379bf55fcf57587df50cc200e89562c57ab698e6fdbeb0b72a337f2d3f7`.

| Field | Value |
|---|---|
| **Evidence files** | `6` artifacts at the evidence home, each cited with the digest of its stored bytes; the two amended test files' digests are cited beside the table (their home is `artifact_homes.tests`) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — "the inert `no links` row renders ONLY for a project with no open work" is now an ABSENCE claim about every band that has open work: across the kg fixture and the app fixtures, NO band with open unlinked tasks may draw the row |
| If the result is an ABSENCE, what made the search wide enough | the guard is a single seat — `if ts or unlinked:` (`views.py:5581`) — and the arms probe the whole painted canvas for the row's text (`"no links" in "\n".join(rows)`) rather than one band's neighborhood; M10 mutates the guard itself (the mechanism-level probe), and the amended frames carry the law at both sizes (every band's bytes were re-emitted and byte-compared) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_the_no_links_row_only_for_a_project_with_no_open_work` — its docstring states the conclusion it guards (the row only for a no-open-work project) so the next reader does not "simplify" it into a presence-only pin |
| Conjunctive criteria: one mutation per conjunct | the admission has three conjuncts — `ts` (chains present), `unlinked` (open tiles present), neither → `bare` — M10 kills the `unlinked` conjunct (`3 failed`), the positive tile arms pin the first two, and the synthetic instance below pins the third |
| Synthetic instance of the absent case | the arm's in-memory board — "Lonely" (a done task only: the no-open-work project the tree's fixtures do not otherwise hold) beside "Busy" (one open unlinked task) — synthesizes the absent case at the mechanism level |
| **Positive control for every probe that returned an ABSENCE** | the same unmodified render returns the row for Lonely (`no links` present — the known-present case) while `b1` paints as an `○` tile: one probe, both outputs, so the absence on Busy is discriminated, not uniform |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln "render_chainmap\|_chainmap_nav" tests/` → `tests/test_chainmap.py` · `tests/test_chainmap_app.py` (+ stale caches) | the chainmap surfaces' named test seats are this batch's two pins (the view-survival suites exercise the map transitively) — all re-validated by the green suite |
| B2 file moved on disk | `git status --porcelain -- taskboard/views.py` → ` M` (modified in place) | no rename, no delete; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → `No such file or directory` | the repo holds no golden-capture directory; the C-2b frames ARE the oracle and live under the batch's evidence home; did NOT fire |
| B4 artifact produced here is consumed elsewhere | `grep -rln "C-2b" tests/ taskboard/` → `tests/test_chainmap.py` (the `FRAMES` path) · `tests/test_chainmap_app.py` (docstring) · `taskboard/views.py` (the render's docstring names the oracle) | the frames' only executable consumer is `test_chainmap.py::_frame()`; the sealed batch-02 path has **0** surviving refs in the test file (the docstring names it as history) |
| A3 interface consumed by another module changed | `_chainmap_plan`'s return shape changed (bands 2-tuple → 3-tuple): `grep -n "in bands" taskboard/views.py` → :5794 · :5977 · :6012 — all three unpack sites updated in the same edit; the session's probe for a leftover 2-tuple unpack found none (`evidence/inc001-run.log`); `_chainmap_nav`'s public shape (a list of columns) is unchanged; `app.py` untouched | every consumer is inside the owning module and was updated atomically; no cross-module reader exists |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B4 names the frames' single executable consumer and the sealed path's zero surviving refs, A3 names the 3-tuple's three unpack sites, B2/B3 did NOT fire · transcripts in `evidence/inc001-run.log` |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| — none — no correction wave in this increment (the three layout-driven test updates are law-driven layout updates, named above — not corrections of shipped claims) | — | — | — | — | — |

| Field | Value |
|---|---|
| **Correction population** | none — no correction |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the sealed batch-02 frames path in the test | 0 hits — `grep -n "2026-10-07-batch-02" tests/test_chainmap.py` → 0 (the docstring says "the sealed batch-02 frames stay history") | yes | `tests/test_chainmap.py:8-10` · `FRAMES` at :30 |
| the inert `no links` row as the zero-link band's rendering | the row survives ONLY in the `bare` branch — `grep -n "no links" taskboard/views.py` → the band-head rule string; the amended frames carry no instance of it (Ops' row is gone; the operator's board copy that motivated the report draws tiles now) | yes | `views.py:5581-5585` · the frames' digests above |
| the chains-only cap arithmetic | 0 hits — `grep -n "tail_n = (nslot - limit)$\|n_chains -" taskboard/views.py` → 0; the cap counts chains AND tiles at :5869 | yes | `views.py:5869` |

### Signed-balance test ledger

`post = base − D + A` → this increment's checkpoint `2566 = 2560 + 6` (the 3 unit arms of
`tests/test_chainmap.py` + the 3 app arms of `tests/test_chainmap_app.py`; the TC-810/AT-802/
AT-801c amendments and the `FRAMES` move modified, not added). Batch post `2566 = 2556 − 0 + 10`
✓ reconciles against the close-out's re-collection (`pytest tests --collect-only -q` →
**2566 tests**). The batch-level ledger is summed in `04-validation.md` — "see 04-validation"
for the close number.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` — the close-out coordinator self-executed the P2 lens pool over the two packets and the diffs · verdict PASS-WITH-NOTES, 0 HIGH — the notes: (a) the contract's marker-glyphs writing defect (increment 001's note, folded there); (b) the three layout-driven test updates (TC-810 · AT-802 · AT-801c) are law-driven, each named in §4 above — assertions on sizes/fixtures/selections, never on the laws' thresholds · the P2 review verdict stands in `02-review.md` (0 blocker · 0 major · 0 minor; reviewer `human:coordinator`, the runtime spawned nobody) |

---

## 5 · Risks

- The tiles make every band with open unlinked tasks taller: real boards near the fold at typical
  terminal heights will see bands fold that used to fit (the amended frames RECORD this for the kg
  fixture — Ops folds at both sizes, Data Warehouse at 80×24). The operator's denser boards may
  fold more; the visual re-verdict covers it.
- `L` on the only task of a one-task board opens the picker with no candidates — the shipped
  picker's empty-candidate law stands (not re-pinned here; no occurrence in the fixtures).
- The strip's `nothing yet`/`nothing waits on it` fallbacks are the shipped forms, now reachable
  from a tile; if a future change gives tiles a synthetic predecessor list, the strip arms in the
  app suite redden first.

## 6 · Pending items / spec deviations

- **The operator's visual re-verdict is PENDING** — on the amended C-2b frames (the oracle amended
  under LED-2026-10-07-batch-06.1) and the new chrome (the `○` tiles + the window markers). The
  batch pushes under the commission; the operator's verdict folds on arrival (batch C's form, at
  the close).
- No spec deviations: the contract's LLR-1201.1/.2 and LLR-1202.1 are met as written.

## 7 · Suggested next task

- Batch-07 (queued, the operator's request — to be contracted at its P1): process/chain templates,
  scoped by the coordinator to user templates in settings + factory presets, a `T` picker, and one
  undo step.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 1 source file (views.py — the chainmap region) |
| 2 | Tests written in this same increment | all | ✓ | 3 unit arms + 3 app arms landed with the product in the same session |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `_chainmap_plan`'s admission + the tile-aware fold — the unit arms, mutation-proven (M9/M10/M11) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M9 executed (the amended frames cannot match without the renderer change); transcript `evidence/mutations.log`; restore digest hash-identical |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above); B2/B3 did NOT fire |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b — `human:coordinator` · PASS-WITH-NOTES 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane; the single brief owned views.py sequentially |
| 8 | Frozen interfaces untouched | all | ✓ | `app.py` untouched (the shipped picker/unlink seats); `_chainmap_nav`'s public shape unchanged; the sealed batch-02 frames read-only as history |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | the `no links` ABSENCE claim — the guard seat, M10 as the mechanism probe, the Lonely/Busy synthetic instance with its positive control |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | M9/M10/M11 KILLED at the transcript's granularity (M11 node-level; M9/M10 file-level with the failing families named, the granularity declared); M12 per-node in increment 001; inert arms: none |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) |
| 13 | **Correction population** declared | all | ✓ | none — no correction (the layout updates are named in §4, not corrections) |
| 14 | **Emitted-form assertion** declared | all | ✓ | the amended frames ARE the emitted bytes (digests cited); the painted tile row; the strip |
| 15 | **Independent review** names somebody | all | ✓ | §4b — `human:coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 6 artifacts at the evidence home + the two amended test files' digests cited beside the table |
