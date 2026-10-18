# Increment 002 — LLR-1803.1, LLR-1803.2, LLR-1803.3 · `the presentation's view keys, page, hint and export (screen)`

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
> `.dev-flow/2026-10-18-batch-01/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-18-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1801` (its acceptance) · `HLR-1802` (its acceptance) · `HLR-1803` / `LLR-1803.1`, `LLR-1803.2`, `LLR-1803.3` · the repointed `LLR-1602.2` (j) hint arm and the `PresentScreen._paint` census key |
| Acceptance | `AT-1801`, `AT-1802`, `AT-1803` · white-box `TC-1808`, `TC-1809`, `TC-1810`, `TC-1604` (hint arm, repointed), `TC-401`/`TC-402` (the census key) · unit `TC-1809` |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-18` |

---

## 1 · What changed

`PresentScreen` gains the two views: six priority bindings (`1`, `2`, `tab`, `shift+tab`, `pagedown`, `pageup`), a view index and a page held on the screen and never persisted (`R` always opens on `gantt`; the page resets on a view change, a cursor move, `space` and `a`), one `_frame_text` that both the paint and the `x` export render, a `pgdn` that is not taken when the next page would paint the same frame, and a hint row that names both views (the current one bright and bold), `pgdn` in the split view only, the moves and the hidden count — its long wording when the whole hint fits the row, else the short one. `x` exports the view on screen to its own file (`-split` for the split view). The README's Presentation section describes the two views and their keys. Two earlier pinned tests change law-driven: TC-1604's hint arm (the hint now opens with the view switch) and TC-402's `PresentScreen._paint` exemption key (the render call moved into `_frame_text`). Real-app captures of both views at 118×31 and 80×25 (PNG at 118) are in the evidence.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | LLR-1803.1, LLR-1803.2, LLR-1803.3 | `PresentScreen`: the six bindings, `_view`, `_scroll`, `_frame_text`, `_hint`, `action_view`, `action_cycle`, `action_scroll`; the page reset in `action_move`, `action_hide`, `action_show_all`; `action_export` renders `_frame_text()` to `present_paths(..., PRESENT_VIEWS[self._view])`; docstring |
| `tests/test_present_views_app.py` | test | HLR-1801, HLR-1802, HLR-1803, LLR-1803.1, LLR-1803.2, LLR-1803.3 | new: AT-1801 ×2, AT-1802 ×2, AT-1803, TC-1808 ×5, TC-1809, TC-1810 (resize arm per LED .5) |
| `tests/test_present_hide.py` | test | LLR-1803.2 (repointing LLR-1602.2 (j)) | TC-1604's two hint strings and docstring; assertions otherwise unchanged |
| `tests/test_markup_census.py` | test | LLR-1803.1 | TC-402's `PresentScreen._paint` exemption key → `self._frame_text()`; its reason text |
| `README.md` | doc | HLR-1801, HLR-1802, HLR-1803 | the Presentation section: the two views, their keys, the shared cursor and hidden tasks, the `-split` export |
| `.dev-flow/2026-10-18-batch-01/evidence/capture_app.py` | doc | HLR-1801, HLR-1802, HLR-1803 | the running-app capture; batch record |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-1-gantt-open.png` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | Edge raster (`views.save_present_png`) of the SVG |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-1-gantt-open.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-2-gantt-long.png` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | Edge raster (`views.save_present_png`) of the SVG |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-2-gantt-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-3-split-open.png` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | Edge raster (`views.save_present_png`) of the SVG |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-3-split-open.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-4-split-moved.png` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | Edge raster (`views.save_present_png`) of the SVG |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-4-split-moved.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-5-split-long.png` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | Edge raster (`views.save_present_png`) of the SVG |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-5-split-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-6-split-pgdn.png` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | Edge raster (`views.save_present_png`) of the SVG |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-6-split-pgdn.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-7-split-hidden.png` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | Edge raster (`views.save_present_png`) of the SVG |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-7-split-hidden.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-1-gantt-open.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-2-gantt-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-3-split-open.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-4-split-moved.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-5-split-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-6-split-pgdn.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |
| `.dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-7-split-hidden.svg` | generated | HLR-1801, HLR-1802, HLR-1803 (AT-1801..AT-1803) | the app’s own `export_screenshot()` |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_views_app.py tests/test_present_hide.py tests/test_markup_census.py tests/test_readme.py tests/test_keymap.py` (with `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8`); the captures: `python .dev-flow/2026-10-18-batch-01/evidence/capture_app.py`; the battery: `python .dev-flow/2026-10-18-batch-01/evidence/mutate.py <a scratch copy of the tree> 002`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| A | `tests/test_present_views_app.py` TC-1808 ×5, TC-1809, TC-1810; `tests/test_present_hide.py` TC-1604 (hint ×2); `tests/test_markup_census.py` TC-401, TC-402 | in the full suite (`suite-002.txt`) |
| B | `tests/test_present_views_app.py` AT-1801 ×2, AT-1802 ×2, AT-1803 | in the full suite (`suite-002.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider` in a git worktree holding increments 001 and 002 | 2 failed, 2721 passed (`suite-002.txt`); the 2 failures are the pre-existing standup tests (`suite-base.txt`) |

| Field | Value |
|---|---|
| **RED counterfactual** | this increment's new and repointed nodes run against `base_ref` `6ddea9f` (a `git archive` export with the test files and frames copied in): 16 failed, 15 passed — every new AT/TC node and the two repointed hint arms and TC-401/TC-402 fail; the 15 passing are TC-1604/AT-1602's untouched arms and the census's other nodes · `.dev-flow/2026-10-18-batch-01/evidence/red-002.txt` · restore digest `9878f3e3e6da3fe0eccc2d4d801b6e219aa15e4a248b73f16af74c2b793ce701` (the batch tree's `app.py`, untouched: the RED ran on the base export) |
| **Mutation verdicts** | 12 mutants, 16 arms, all KILLED: N1 `2` loses priority (TC-1810) · N2 the same-frame guard removed (TC-1810, AT-1803) · N3 a move keeps the page (TC-1810) · N4 `pgdn` in the gantt hint (TC-1808[118]) · N5 bold on the other view (TC-1808[80]) · N6 one export file for both views (TC-1809, AT-1803) · N7 the suffix on gantt (TC-1809) · N8 `R` opens on split (AT-1803, TC-1810, AT-1802[118]) · N9 `x` exports to the gantt file whatever the view (AT-1803) · N10 `tab` clamps (AT-1803) · N11 `w >= 100` instead of fit (TC-1808[100]) · N12 a resize keeps the page (TC-1810) · arms that stayed GREEN: none · `.dev-flow/2026-10-18-batch-01/evidence/mutation-002.txt` · restore digest `9878f3e3e6da3fe0eccc2d4d801b6e219aa15e4a248b73f16af74c2b793ce701` |
| **Instrument RED-proof** | 2 instruments: `mutate.py` (as increment 001); `capture_app.py` (writes the app's own `export_screenshot()`; its frames were read against the prototype's PNGs — §6) |
| **Emitted-form assertion** | 2 artifacts: the frames as `#present-frame` holds them (`content.plain`); the exported SVG read with `&#160;` unescaped (AT-1803), the key words searched in its text |
| **Reverse census** | 5 probes: B1 `grep -rl` for `PresentScreen`, `present-hint`, `present-frame`, `_paint`, `present_paths` over `tests/` → `test_present_hide.py` (TC-1604 hint, repointed), `test_markup_census.py` (TC-402 key, repointed), `test_present.py`, `test_present_rulers.py`, `test_tick_label.py`, `test_markup_sites.py`, `test_report.py` (read the frame or open `R`; green in `suite-002.txt`) · B2 no file moved · B3 no goldens; the PRES-V3 frames unchanged by this increment · B4 the export: the gantt name unchanged (AT-1001's `x` arm), the split view to `-split` (AT-1803) · A3 `KEYMAP` untouched: the app's `1`/`2` stay non-priority, its `tab` released while a modal is open (TC-1810; `tests/test_keymap.py` green) — 0 foreign hits left un-revalidated |
| **Correction population** | none — no correction |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-18-batch-01/evidence/suite-002.txt | 0694a41e8968bbc9bd2a81b4b2eed51b1c4fe253c9318448b240b92d2edd6ae4 |
| red-002.txt | .dev-flow/2026-10-18-batch-01/evidence/red-002.txt | 30b16c951434b2cda7c85b414c07151eda342434292ca6d2083461f35aecad1a |
| mutation-002.txt | .dev-flow/2026-10-18-batch-01/evidence/mutation-002.txt | 4a9da74305060bd4e114cb22318771433ba8c19102a8e2239b97da291b26c067 |
| app-002-118x31-1-gantt-open.png | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-1-gantt-open.png | ee27d18e0bfcd56a9b6a78af66b66b517343c2f10f152d3ccc20666ca130031a |
| app-002-118x31-1-gantt-open.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-1-gantt-open.svg | c931fdcb06eb1f29bfb84285ef34a481c28309fb124b79cc2559798bb08a4690 |
| app-002-118x31-2-gantt-long.png | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-2-gantt-long.png | 07b4e9a5ba69c9b116fdea19e93eaf9f2fff610b7e3179bb7ffe2917c961f5c8 |
| app-002-118x31-2-gantt-long.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-2-gantt-long.svg | be53b35a9023b0887a4d715968fdeba4a67a4cc48788b81005c903fe7423df60 |
| app-002-118x31-3-split-open.png | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-3-split-open.png | b62ddf3b12bbf9818a78b702958e0b9328c90aeb9286b4f8c28103475a90cebd |
| app-002-118x31-3-split-open.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-3-split-open.svg | b98b1c5c4604d89822f8cac79b87afc27218c3878016d5070ebb492880f827e6 |
| app-002-118x31-4-split-moved.png | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-4-split-moved.png | 4539d4b21aeed28c1d813fef9d3c89d1e5dd835ae82bb36487edf883d94ea374 |
| app-002-118x31-4-split-moved.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-4-split-moved.svg | e5567d1cafe08339f576fe63fb86c09d846f260fab03700268fab7b9b3dfb7d4 |
| app-002-118x31-5-split-long.png | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-5-split-long.png | cf8564d1ba5a56196d1dda0242511a707f8151690bcc60144c1fb2d34d165a3a |
| app-002-118x31-5-split-long.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-5-split-long.svg | f28bbcc7985c3724422cf4bb8962494c00235da97000e50c3096c2eb6762a4e4 |
| app-002-118x31-6-split-pgdn.png | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-6-split-pgdn.png | 320e29f7f208e21212127d93b45c4df5dca33ed9561ec20a22faf5932e0c611a |
| app-002-118x31-6-split-pgdn.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-6-split-pgdn.svg | 2d39a74343ef0cc1731ba648fac2ae0c84c58d1017c4a4c7636894dcee9ae476 |
| app-002-118x31-7-split-hidden.png | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-7-split-hidden.png | ce43642f489c82594bac41f138d10e078ad855c9994aac1f43724b2a3e8e9175 |
| app-002-118x31-7-split-hidden.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-118x31-7-split-hidden.svg | 679ca2426cc5fbd3d4df4d028aae7e77317bddd22f7ac7d64a6104b7f9915d2b |
| app-002-80x25-1-gantt-open.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-1-gantt-open.svg | 7ccf13dfe2cf3e544b11f7af49f1ab2bc1c86cdfa44564ba2b3c44dd5579ed76 |
| app-002-80x25-2-gantt-long.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-2-gantt-long.svg | d5bd36a3204c2caba70608c174aeace25f71c7811b487203a6bc2ebdf706b23f |
| app-002-80x25-3-split-open.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-3-split-open.svg | 00e228dfbe8547611aa731765271012bbb840acf861126781dbeaed202f3e60b |
| app-002-80x25-4-split-moved.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-4-split-moved.svg | 3fb2ca55d3f57d4cb4c566aef2f1a06c93e152237bafd18f1d45cb93f06e8c34 |
| app-002-80x25-5-split-long.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-5-split-long.svg | 3974544f6c5d12089f27f357a29887ea320732429000e20dd085492fff02a2b0 |
| app-002-80x25-6-split-pgdn.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-6-split-pgdn.svg | 4b7067a258d0b34e29846d6a950013abe71ed9c32e8ba9f8f96ef85e0caac5d4 |
| app-002-80x25-7-split-hidden.svg | .dev-flow/2026-10-18-batch-01/evidence/captures/app-002-80x25-7-split-hidden.svg | 3d7d6aac4145cad2b514776094d020509ea47b03bf0ecd433ff25851b8e659e4 |

| Field | Value |
|---|---|
| **Evidence files** | `24 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · OK to advance, 0 HIGH · F1 MEDIUM (a page kept across a taller resize leaves dead pages) → fixed: `on_resize` resets `_scroll`, LED .5, TC-1810 resize arm, N12 KILLED · F3 LOW (README line past the wrap), F4 LOW (README said "every open task") → fixed · F2 LOW (below ~60 columns the short hint is clipped) → accepted, carried to `BACKLOG.md` · re-read on the re-frozen set (app.py 9878f3e3…): OK to advance |

## 5 · Risks

The hint's long/short choice is measured on the cell width of the whole hint; a width where the long split hint fits only without a count switches wording when a task is hidden (TC-1808 pins it at 100 and 99). The captures are SVGs from the app's own `export_screenshot()`; the PNGs are Edge's raster through the shipped `save_present_png`.

## 6 · Pending items / spec deviations

- Captures read against the prototype (`prototypes/present_views/out/r2-118-D2-stacked*.png`, `r2-80-D2-stacked*.png`, `r2-118-A-gantt.png`): the split frames equal the prototype's D2 at page 0 (gantt rows on top, two columns at 118, one at 80, the cursor's block accented, `no notes` on the SEO heading); the deltas are the declared ones — the hint names two views (`1 gantt  2 split`), a one-row cut reads `… +N lines`, `pgdn` pages (the prototype stepped 5 rows).
- PDR PC-U2 (the hint at 80/99/100/118 with 0 and 12 hidden on the real `#present-hint`) is TC-1808's arms here and the ux walkthrough at P4.

## 7 · Suggested next task

The DDR, then P4.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_present_views_app.py` (new); two repointed |
| 3 | Layer 0 where it applies | ✓ | `present_paths`' branch: TC-1809; `_hint` (2 branches) through TC-1808 |
| 4 | RED counterfactual | ✓ | §4, `red-002.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b: 0 HIGH; F1, F3, F4 fixed and re-read; F2 accepted |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-002.txt` |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence |
| 11 | Mutation verdicts | ✓ | §4: 16/16 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: digests |
