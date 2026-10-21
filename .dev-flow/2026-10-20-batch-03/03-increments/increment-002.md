# Increment 002 — LLR-2402.1, LLR-2403.1, LLR-2403.2, LLR-2404.1, LLR-2405.1 · `the presentation: the hint's chip, ? and its seat, the clean export, K/J`

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
> `.dev-flow/2026-10-20-batch-03/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.


| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-03` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2402`, `HLR-2403`, `HLR-2404`, `HLR-2405` / `LLR-2402.1`, `LLR-2403.1`, `LLR-2403.2`, `LLR-2404.1`, `LLR-2405.1` |
| Acceptance | `AT-2402`, `AT-2403`, `AT-2404`, `AT-2405` · white-box `TC-2402`..`TC-2405` · unit: `present_all_export`'s cut and anchor, the seat ↔ bindings equality (Layer 0) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in the scratch worktree, ported here) |
| Date | `2026-10-20` |

---

## 1 · What changed

The presentation (`R`) takes the round's items 2, 3, 4 and 5. Its key bindings are now generated from one seat, `keymap.PRESENT_KEYS` — the same pairs as before plus `K`/`J` and `?` — and `?` opens a window listing every row of that seat by group, the current view's keys bright and another view's dim with its view named (`modals.PresentKeys`). The hint row opens with the board's chip when the board has one (never the frame or an export), names `K J` beside `⇧↑↓` in view 3, and ends with `? keys`, which takes its 8 cells off the room the wordings are chosen in (D-14: at 80 columns the gantt view now takes the short wording; `?` lists `next` and `show all` in words). `x` in view 3 exports the timeline laid out as the screen lays it out — its folds anchored on the cursor's project — but drawn without the cursor, and cut after its last row of content (`views.present_all_export`).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/keymap.py` | source | LLR-2403.1 | `PresentKey`, `PRESENT_KEYS`, `present_bindings` (new) |
| `taskboard/views.py` | source | LLR-2402.1, LLR-2404.1 | `board_chip_text`, `present_all_export` (new); `_all_timeline(…, anchor=None)` |
| `taskboard/modals.py` | source | LLR-2403.2 | `PresentKeys` (new) |
| `taskboard/app.py` | source | LLR-2402.1, LLR-2403.1, LLR-2403.2, LLR-2404.1, LLR-2405.1 | `PresentScreen.BINDINGS = present_bindings()`; `_hint` (the chip) over `_keys_hint` (`? keys`, view 3's `K J` wordings); `action_keys`; `action_export`'s view 3 |
| `tests/test_present_backlog_round.py` | test | HLR-2402, HLR-2403, HLR-2404, HLR-2405, LLR-2402.1, LLR-2403.1, LLR-2403.2, LLR-2404.1, LLR-2405.1 | new: TC-2402..TC-2405, AT-2402..AT-2405 |
| `tests/test_modal_keys.py` | test | HLR-2407 | the inventory gains `PresentKeys` (no buttons) |
| `tests/test_present_narrow.py` | test | HLR-2403, HLR-2405 | law-driven (LED .5, D-14): every expected hint ends `  ? keys`, its wording chosen in the room left (first widths + 8, the long view-3 one + 12), view 3's wordings with `K J`; AT-2002 now checks that `?` lists `next` and `show all`; `ALL_FIRST` re-pinned as literal measured numbers (+8, the long one +12; code review CR-3); TC-1904's overflow arm renamed and given a 48-column count (CR-5) |
| `tests/test_present_polish.py` | test | HLR-2403, HLR-2405 | as the row above |
| `tests/test_present_views_app.py` | test | HLR-2403, HLR-2405 | as the row above |
| `tests/test_present_hide.py` | test | HLR-2403, HLR-2405 | as the row above |
| `tests/test_present_all.py` | test | HLR-2403, HLR-2405 | as the row above |
| `.dev-flow/2026-10-20-batch-03/evidence/mutate-002.py` | doc | HLR-2402, HLR-2403, HLR-2404, HLR-2405 | the increment's mutation battery |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** — at the cap: the four items are one surface (`PresentScreen`) whose seat lives in `keymap`, window in `modals` and pure renders in `views` by the layering of `docs/ARCHITECTURE.md`; one source file per layer, none splittable without a layer ban |
| Test files | 7 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_backlog_round.py` (with `NO_COLOR` unset); the targeted set of `suite-002.txt`; `python .dev-flow/2026-10-20-batch-03/evidence/mutate-002.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_present_backlog_round.py` — 14 nodes: `test_TC_2402_the_hint_opens_with_the_chip`, `test_TC_2402_the_chip_never_costs_the_keys[2]`, `test_AT_2402_the_presenter_reads_the_board_the_slide_never_does`, `test_TC_2403_the_bindings_are_the_seat`, `test_TC_2403_the_window_is_the_seat_live_by_view[2]`, `test_AT_2403_question_mark_shows_every_key`, `test_TC_2404_the_export_has_no_cursor_and_ends_at_its_content`, `test_AT_2404_the_export_reads_as_a_slide[118x30, 80x24]`, `test_TC_2405_the_hint_names_K_J[2]`, `test_AT_2405_K_and_J_reorder` | executed: 370 passed in the targeted run of the new file and every presentation, home, markup, keymap and readme suite, after the code review's fixes (`suite-002.txt`) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on increment 001's commit `fab1206` (a clean detached worktree, the new test file as first written copied in): 12 failed, 0 passed (the two `TC_2402_the_chip_never_costs_the_keys` nodes, added after the code review, are proven by their mutation arm M2b) · `.dev-flow/2026-10-20-batch-03/evidence/red-002.txt` |
| **Mutation verdicts** | 16 arms over 14 mutants, one run, each restore proven by digest: the chip dropped · KILLED ×2; the chip painted in the frame · KILLED; narrow and the rail read off the chip's room (CR-1) · KILLED; a binding outside the seat · KILLED; `?` unbound · KILLED; the live/dim rule inverted · KILLED ×2 (TC, AT — the AT's style check added after a first run where the AT arm SURVIVED: it read the window's text only); `? keys` dropped · KILLED; the export keeping the cursor · KILLED; the cut dropping a content row · KILLED; no cut · KILLED; the export anchored on no project · KILLED; the export back on the screen's timeline · KILLED; `K`/`J` unbound · KILLED; a wording without `K J` · KILLED · arms that stayed GREEN: none in the recorded run · `.dev-flow/2026-10-20-batch-03/evidence/mutation-002.txt` |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate-002.py` — increment 001's harness; its first run here printed `CRASH/BAD (exit 4)` for a node id holding non-ASCII parameters and `GREEN (SURVIVED)` for the AT's live-rule arm, both repaired before the recorded run; `arms: 16` |
| **Emitted-form assertion** | 1 artifact: the view-3 SVG (`reports/present-board-2026-10-20-all.svg`), read row by row as Rich emits it (`&#160;` unescaped, the `<text>` pieces of each `line-N` joined, rows = the highest `line-N` + 1) — AT-2402, AT-2403, AT-2404 |
| **Reverse census** | 4 probes: B1 `grep -rln "PresentScreen\|present-hint\|_hint\|render_present_all\|action_export\|KEYMAP" tests/` → the presentation suites (5 law-driven updates, §2), `test_boards_home.py`, `test_gantt_polish.py`, `test_link_picker.py`, `test_report.py`, `test_markup_census.py`, `test_markup_sites.py`, `test_keymap.py`, `test_help_keys.py`, `test_readme.py` — green in `suite-002.txt` · B2 no file moves · B3 the round frames read by `test_present_polish.py`/`test_present_views.py` are frames, never the hint — green · B4 the view-3 SVG/PNG (above) · 0 foreign hits |
| **Evidence files** | the table under §4 *Evidence files*: each artifact's path and SHA-256 |
| **Correction population** | 1 correction: the hint pins, enumerated by `grep -rln "esc leave\|x export · esc\|⇧↑↓ order\|⇧↑↓ reorder" tests/` before the first edit — 5 files, each pin moved by the one rule (`  ? keys` appended, the wording chosen 8 cells narrower; view 3 `K J`) |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-20-batch-03/evidence/suite-002.txt | 81639c4233e1a184bfa1c25f793f62dfea3d01f42e69898a664706d89088eb63 |
| red-002.txt | .dev-flow/2026-10-20-batch-03/evidence/red-002.txt | f892394e45c615c6e1260a90ac67c0e51b67892615de2f10a12bf0802a87c1b3 |
| mutation-002.txt | .dev-flow/2026-10-20-batch-03/evidence/mutation-002.txt | b78ee33422766a2c8e3a39fcea7a25ffb0e8d47f66a19133d0836f339ea29f24 |
| mutate-002.py | .dev-flow/2026-10-20-batch-03/evidence/mutate-002.py | 0a749f6138d7c87622220083c831ed91092e06d9c471654ec4523718a86747a5 |
| inc002.diff | .dev-flow/2026-10-20-batch-03/evidence/inc002.diff | 165392544265b3db77b0e8dfd33b6abb3f5ced5d685aed92faf485e9300defb1 |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · **OK to advance** after one FIX FIRST: HIGH CR-1 (with a chip, `? keys` was lost from 36 to 36 + the chip's columns) fixed in `_hint`/`_keys_hint(w, hidden, room)` and verified on the re-read diff (the TC-2402 chip law over 36..139 columns, M2b KILLED, 143 passed in the affected files); MEDIUM CR-2 (the rail wording with a chip), CR-3 (an oracle restating the code) and LOW CR-4..CR-6 fixed; LOW R-1 (a double ellipsis with a 27-cell chip at 36 columns) and R-2 (the chip law in view 3 only) recorded |

## 5 · Risks

The generated bindings carry no descriptions (the old `Leave`/`Export` were read by nothing: `binding_map` reads other screens; code review CR-6). 
At 80 columns the gantt hint no longer names `next` and `show all` (D-14; `?` does) — an OPERATOR item at the close. Caps Lock turns `k`/`j` into `K`/`J` in view 3 (§6.3).

## 6 · Pending items / spec deviations

The full suite is owed at P4. `SOURCE files` at the cap (4/4), declared in §2. D-14 recorded (LED .5).

## 7 · Suggested next task

Increment 003 — the boards (HLR-2408, HLR-2409, HLR-2410).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 4 source files, at the cap, the reason declared |
| 2 | Tests in this increment | ✓ | `tests/test_present_backlog_round.py` |
| 3 | Layer 0 where it applies | ✓ | the export's cut and anchor; the seat ↔ bindings law |
| 4 | RED counterfactual | ✓ | §4, `red-002.txt` |
| 5 | Reverse census | ✓ | §4: 4 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-002.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 16/16 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: 1, enumerated |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |
