# Increment 003 — LLR-1905.1 · `the backlog polish prototype round`

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`. The normative RULES below are
> language-independent.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/increment-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-18-batch-02/03-increments/increment-003.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-18-batch-02` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1905` / `LLR-1905.1` |
| Acceptance | `AT-1905` · white-box none — LLR-1905.1 is verified by inspection (`red-003.txt`) · unit none — the checker's branches are exercised by AT-1905's own corrupted-copy arms |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-18` |

---

## 1 · What changed

`prototypes/backlog_polish/` is the prototype round for the three polish items the operator's standing rule keeps out of production until a verdict. `capture.py` runs the real `TaskboardApp` headless on the synthetic notes board (calendar frozen), presses the presenter's keys and writes each frame with the app's own `export_screenshot()` (SVG) and `views.save_present_png` (Edge PNG), with every pair's SHA-256 in `out/manifest.json` — 45 captures: **contrast** (the view word and cut marks: current `dim` 3.2:1 · A `reached` 4.9:1 · B `mut` 6.4:1, gantt and split with the long note), **hint80** (current short wording · A a middle wording keeping `next`/`show all` · B double spaces instead of `·`, gantt and split with nothing hidden and gantt with one task hidden, where every look falls back — the 8 variant captures equal to the current look, all at 118 columns or with the hidden task, are labelled `= actual` on the page), **notecap** (the gantt view's 3-row note: current · A fills the free rows · B 6 rows, the long and a 3-paragraph note) — each at 118×31 and 80×25 — and **narrow** (increment 002's shipped narrow frame at 30×12, 20×12 and the compact hint at 50×20, for review). Variants are forks held by the script and bound in its own process only (`taskboard.app.render_present`, `PresentScreen._hint`, `views._present_cut`), restored after every look. `build_html.py` writes one self-contained page (`lang="es"`, PNGs embedded, click-to-zoom) comparing the looks side by side, printing the contrast ratios from the app's own tones, and recommending one capture per item (`data-recommend`): contrast A, hint80 A, notecap A. `tests/test_backlog_polish_round.py` (AT-1905) checks the round and rejects eight corrupted copies of it.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `tests/test_backlog_polish_round.py` | test | HLR-1905, LLR-1905.1 | new: `check_round` and AT-1905 with its eight corrupted-copy arms |
| `prototypes/backlog_polish/backlog-polish-prototype.html` | doc | HLR-1905 | the verdict page (Spanish prose, PNGs embedded) |
| `prototypes/backlog_polish/build_html.py` | doc | HLR-1905 | the page builder |
| `prototypes/backlog_polish/capture.py` | doc | HLR-1905 | the round's capture: the real app headless, the in-process forks |
| `prototypes/backlog_polish/out/contrast-A-gantt-long-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-A-gantt-long-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-A-gantt-long-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-A-gantt-long-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-A-split-long-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-A-split-long-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-A-split-long-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-A-split-long-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-B-gantt-long-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-B-gantt-long-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-B-gantt-long-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-B-gantt-long-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-B-split-long-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-B-split-long-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-B-split-long-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-B-split-long-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-current-gantt-long-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-current-gantt-long-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-current-gantt-long-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-current-gantt-long-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-current-split-long-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-current-split-long-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/contrast-current-split-long-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/contrast-current-split-long-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-A-gantt-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-A-gantt-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-A-gantt-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-A-gantt-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-A-gantt-hidden-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-A-gantt-hidden-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-A-gantt-hidden-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-A-gantt-hidden-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-A-split-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-A-split-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-A-split-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-A-split-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-B-gantt-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-B-gantt-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-B-gantt-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-B-gantt-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-B-gantt-hidden-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-B-gantt-hidden-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-B-gantt-hidden-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-B-gantt-hidden-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-B-split-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-B-split-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-B-split-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-B-split-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-current-gantt-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-current-gantt-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-current-gantt-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-current-gantt-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-current-gantt-hidden-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-current-gantt-hidden-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-current-gantt-hidden-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-current-gantt-hidden-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-current-split-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-current-split-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/hint80-current-split-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/hint80-current-split-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/manifest.json` | generated | HLR-1905 | each capture's SVG/PNG pair and SHA-256 (`capture.py`) |
| `prototypes/backlog_polish/out/narrow-current-narrow-20x12.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/narrow-current-narrow-20x12.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/narrow-current-narrow-30x12.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/narrow-current-narrow-30x12.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/narrow-current-narrow-30x12-x.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG — added at the DDR (DDR-C1) |
| `prototypes/backlog_polish/out/narrow-current-narrow-30x12-x.svg` | generated | HLR-1905 | the app's own `export_screenshot()`, toasts enabled — added at the DDR (DDR-C1) |
| `prototypes/backlog_polish/out/narrow-current-narrow-50x20-hidden.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/narrow-current-narrow-50x20-hidden.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-A-gantt-long-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-A-gantt-long-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-A-gantt-long-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-A-gantt-long-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-A-gantt-short-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-A-gantt-short-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-A-gantt-short-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-A-gantt-short-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-B-gantt-long-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-B-gantt-long-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-B-gantt-long-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-B-gantt-long-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-B-gantt-short-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-B-gantt-short-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-B-gantt-short-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-B-gantt-short-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-current-gantt-long-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-current-gantt-long-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-current-gantt-long-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-current-gantt-long-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-current-gantt-short-118x31.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-current-gantt-short-118x31.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |
| `prototypes/backlog_polish/out/notecap-current-gantt-short-80x25.png` | generated | HLR-1905 | Edge raster (`views.save_present_png`) of the SVG |
| `prototypes/backlog_polish/out/notecap-current-gantt-short-80x25.svg` | generated | HLR-1905 | the app's own `export_screenshot()` |

| Count | Value |
|---|---|
| **SOURCE files** | **0 / 4** |

## 3 · How to test

`python prototypes/backlog_polish/capture.py` then `python prototypes/backlog_polish/build_html.py` (Edge needed for the PNGs; ~70 s); `python -m pytest -q -p no:cacheprovider tests/test_backlog_polish_round.py`; open `prototypes/backlog_polish/backlog-polish-prototype.html`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| B | `tests/test_backlog_polish_round.py::test_AT_1905_the_round_is_fit_for_a_verdict` (AT-1905, with its eight corrupted-copy arms) | in the full suite (`suite-003.txt`) |
| inspection | LLR-1905.1: `git diff --stat 1ba8c3f -- taskboard/` empty after both scripts ran; every write path under the round's folder (`red-003.txt`) | ✓ |
| full suite | `python -m pytest -q -p no:cacheprovider -rs` on the working tree with increments 001–003 | 0 failed, 2740 passed (`suite-003.txt`; 2739 + AT-1905) — `test_win_clipboard_roundtrip` passed |

| Field | Value |
|---|---|
| **RED counterfactual** | AT-1905 on `base_ref` `9e82b10` (a `git archive` export, the test copied in): FAILED — `no page backlog-polish-prototype.html` · `.dev-flow/2026-10-18-batch-02/evidence/red-003.txt` · no file of the tree was mutated |
| **Mutation verdicts** | none — no mutation battery in this increment: the round is a prototype, not product logic; AT-1905's falsifiability is shown inside the node, which builds eight corrupted copies of the round (a capture moved aside, a variant equal to the current look, an external `href`, a hand-written SVG without the `terminal-` classes, an SVG whose digest disagrees with the manifest, a recommendation naming another item's capture, an equal capture left unlabelled, two PNGs swapped) and asserts the checker names each one |
| **Instrument RED-proof** | 2 instruments: `capture.py` — its first run produced hint scenes where every variant fell back to the short wording (one hidden task leaves no room) and a 30-column PNG cropped by Edge's minimum window, both seen on the PNGs before the round was believed; the scenes were redrawn (nothing hidden, plus one hidden scene to show the fallback) and the PNG window widened to ≥ 60 cells with the SVG's aspect; the checker in AT-1905 — RED on base and on each corrupted copy |
| **Emitted-form assertion** | 2 artifacts: the SVGs as `export_screenshot` wrote them (read with `&#160;` as a space, `terminal-<n>` ids normalised before the variant comparison); the page as `build_html.py` wrote it (`data-capture`, `data-recommend`, `data:image/png;base64,` counted) |
| **Reverse census** | 5 probes: B1 `grep -rl "backlog_polish" tests/` → `test_backlog_polish_round.py` only · B2 no file moved · B3 no golden; no oracle frame touched · B4 the round writes only under its folder (`red-003.txt`), read by AT-1905 and the operator · A3 no interface: the forks rebind names in the capture process only — 0 foreign hits |
| **Correction population** | none — no correction |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-18-batch-02/evidence/suite-003.txt | 78039d1bc2195e958027a549120f425d10dce0abf2a87e4042c2f3bb26f19766 |
| red-003.txt | .dev-flow/2026-10-18-batch-02/evidence/red-003.txt | 4adc8d17ff24e4649246d535bf50555363324b2273540ae1d1a467cfeb7e8943 |

| Field | Value |
|---|---|
| **Evidence files** | `2 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned with agents/code-reviewer.md · OK to advance, 0 HIGH · F1 MEDIUM (8 hint variant captures equal the current look; the threshold said each differs) → fixed: the threshold amended (LED .8), equal captures labelled `data-same="current"` and checked both ways · F2 MEDIUM (`mkdtemp` boards left behind, outside the round) → fixed: `TemporaryDirectory`, LLR-1905.1 amended · F3 LOW (the external-resource regex) → widened · F4 LOW (PNG digests unchecked) → checked against the manifest and the embedded figure; two new RED arms · re-read on the folded set: OK to advance; its one LOW (LLR-1905.1's threshold line) → fixed |

## 5 · Risks

The variants are forks of increment 002's code frozen into the round; once the verdict is implemented they go stale, as every round does (ARCHITECTURE §3). The `x` notice is captured painted at 30×12 (DDR-C1; `run_test` needs `notifications=True` for toasts).

## 6 · Pending items / spec deviations

- PDR PC-5 (and the DDR's condition DDR-C1): first declared `not exercised` because no toast reached `export_screenshot`; the DDR's architect lens refused that as a discharge, and the cause was found — `run_test` disables toasts unless `notifications=True`. After the gate, the round gained the scene `narrow-30x12-x` (toasts enabled, the start-up toasts cleared): the notice `Widen the terminal to 36+ columns to export` is painted (`out/narrow-current-narrow-30x12-x.png`); 46 captures. Added after this packet's review as `doc`/`generated` rows (the prototype script and its outputs, no product code), declared in PLAN §Gate notices.
- 12 stale files of the first capture run (`out/hint80-*-split-hidden-*`) stay on disk, excluded in `.git/info/exclude` (a removal was refused by the runtime's safety check; it is the operator's to make).
- The verdict on the three items is the operator's; `BACKLOG.md` lists them as awaiting it.

## 7 · Suggested next task

The DDR, then P4.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 0 source files |
| 2 | Tests in this increment | ✓ | `tests/test_backlog_polish_round.py` (new) |
| 3 | Layer 0 where it applies | ✓ | not due: no product unit; the checker's branches are AT-1905's arms |
| 4 | RED counterfactual | ✓ | §4, `red-003.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-003.txt` |
| 10 | Load-bearing emptiness | ✓ | "no file under `taskboard/` changed" rests on an empty diff: its positive control is the same command over increment 002's range (`git diff --stat 2c6ac76 1ba8c3f -- taskboard/` → 2 files), in `red-003.txt` |
| 11 | Mutation verdicts | ✓ | §4: none, declared — the node's own corrupted-copy arms |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: digests |
