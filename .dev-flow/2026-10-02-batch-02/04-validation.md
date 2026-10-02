# Validation — taskboard — Batch 2026-10-02-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1 and **names who executed each one**. The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Mode: validation.** Author: `qa-reviewer` (named sub-agent, `agents/qa-reviewer.md`, flow pinned to rev98), 2026-10-02. **Iteration 2:** re-issued after increment 006, the P3 `iterate-to-fix` that iteration 1's FAIL routed. Iteration 1's record is kept below (§Iteration 1 record, and the gap rows marked closed), and its verdict is superseded.
> **Iteration 2 — who executed what.**
> 1. **The gate RE-RUN** was **launched and collected by the orchestrator** (C-25) after increment 006: `python -m pytest -q -p no:cacheprovider` → **1677 passed in 182.11 s, EXIT 0** (`evidence/p4-gate2.txt`). I read the tail from that run's own output and did not run the suite. **Revision check (`executed` by qa-reviewer):** the transcript was written at 13:57:15. `find taskboard tests -newer evidence/p4-gate2.txt` returns nothing, and the newest edit is `tests/test_gantt_polish.py` at 13:43:29. `--collect-only` gives **1677 collected**. The iteration-1 run (`p4-gate.txt`) is superseded as the run of record.
> 2. **Increment 006's RED and mutation runs** were **executed by the increment author** (`software-dev`): `evidence/inc006-red.txt` (both AT-207 arms FAILED on the increment-004 tree) and `evidence/inc006-mutations.txt` (W1, 2 of 2 arms red, restore `a4688ae7…` OK). The code-reviewer's increment-006 review (PASS-WITH-NOTES) is as stated in increment-006 §4b.
> 3. **My own iteration-2 checks**, each `executed` by qa-reviewer and read-only toward the repo:
>    - `grep -n "def test_AT_2" tests/*.py` → **10 functions for 10 ATs**, one AT-207.
>    - A **fresh scratch-copy probe** (`%TEMP%\claude\qa-p4\tree2`, with `pyproject.toml`) of the merged node: both arms passed unmutated. Both arms FAILED at `test_gantt_polish.py:533` (`▾ Website` absent at `tm6`) under W1 (`previous` ignored) AND under my iteration-1 mutant (previous offered last). The restore was verified by sha256 `a4688ae7c1788b66…`.
>    - A re-read of increment-005 §4 (rows 77, 81), increment-001 §2 (row 38), `01-requirements.md` HLR-203 and §6.5, `01-requirements-ledger.md` LED .19, `PLAN.md:85`, and `grep "date_chip(" taskboard/views.py` (6 callers).
>    - A home-path grep of the batch record: 0 hits.
>
> **Iteration 1 — who executed what.**
> 1. **The gate run** was **launched and collected by the orchestrator** (C-25) on the increment-005 frozen tree: `python -m pytest -q -p no:cacheprovider` → **1677 passed in 183.75 s, EXIT 0** (`evidence/p4-gate.txt`). I read the tail from that run's own output and did not run the suite. **Revision check (`executed` by qa-reviewer):** the transcript was written at 13:30:00. `find taskboard tests -newer evidence/p4-gate.txt` returns nothing; the newest edits are `tests/test_gantt_polish.py` at 13:18:54 and `taskboard/views.py`/`app.py` at 13:16:38. The run therefore postdates every edit.
> 2. **RED counterfactuals, mutation batteries, reverse-census runs and per-increment green runs** were **executed by the increment author** (`software-dev`) and recorded in `03-increments/increment-00N.md` plus `evidence/inc00N-*.txt`. I evaluate them here, and I re-read each claim against its transcript (G-002 is one that does not hold).
> 3. **My own checks.** Each was `executed` by qa-reviewer and is read-only toward the repo:
>    - `pytest --collect-only -q`: **1677 collected** over the suite, and **66** in the three new files (`test_colour_budget_app.py` 24, `test_english.py` 9, `test_gantt_polish.py` 33).
>    - A grep of every `AT-2NN` / `def test_AT_2NN` under `tests/`.
>    - A grep of the batch record for home paths and `{{`/`<...>` placeholders: 0 hits.
>    - A spot re-run of the AT nodes: `pytest -k AT_` over the three files, 16 passed. It found 11 AT-named functions for 10 ATs.
>    - A two-mutant probe of `test_AT_207_at_full_size_…` in a scratch copy (`%TEMP%\claude\qa-p4\tree`), with the restore verified by sha256 `a4688ae7c1788b66…` matching the live `views.py`. See G-002.
> 4. **The UX walkthrough** was **executed by the `ux-reviewer`**, with verdict PASS-WITH-NOTES. The orchestrator relayed it as `evidence/p4-ux-walkthrough.txt`, which I read. I did not drive it.
> **Result states** in this file use the seven words: `planned` · `executed` · `approved` · `failed` · `blocked` · `not-run` · `n/a — <reason>`. Every node marked "pass" below was `executed` by the orchestrator in the gate run: 1677 collected = 1677 passed, 0 failed, 0 skipped.

## ✅ Verdict (read first)

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Result` · `Layer 0` · `Evidence checklist` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.
>
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.
> A Spanish batch writes `- **Result:** PASS`, not `- **Resultado:** aprobado`: the label, the tokens and the
> reviewer-identity tokens below are the machine's vocabulary.

- **Result:** `PASS-WITH-NOTES`
- **Layer 0:** `8 unit(s) met the criterion · 8 carry a named reddening mutation` (see §Layer 0. All are KILLED in `evidence/inc00{1,4,5}-mutations.txt`; increment 006 changed no unit.)
- **Requirements:** `23`/`23` pass (10 HLR + 13 LLR; every node is green in the gate re-run) · `0` blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative). US-201..205 are all observed. **C-18 ✓:** AT-201..210 each realise in exactly one on-disk function. AT-207 is one function parametrised over two terminal sizes, and both arms are RED on the increment-004 tree.
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables are reached/observed at the surface · `0` gaps (one weak output noted, G-005)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative. Increments 001–005 are as recorded in iteration 1. Increment 006: Correction population of 2 (the 11 AT functions for 10 ids → 1 site edited; the 6 `date_chip` seats named) and a 5-probe reverse census, none fired; `_walk` has 0 references left.
- **Test ledger:** ✓ reconciles (`1611 − 2 + 68 = 1677`; collected 1677 = passed 1677 in the gate re-run)
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 11 of 11 rows ✓ with evidence`

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.
> **Closed in iteration 2 (re-read, not trusted):**
> - **G-001:** the AT-207 re-cut.
> - **G-002:** increment-005 §4 corrected, plus the merged node's RED and mutation proof.
> - **G-003:** the HLR-203 §6.5 amendment and LED .19.
> - **G-004:** increment-001's breakdown corrected.
>
> **Why the verdict is PASS-WITH-NOTES and not PASS:**
> - **Declared minors G-005..G-008:** G-005 (body-row weekend shading is checked only below the surface), G-006 (the 118×30 bound is a pin), G-007 (UX-8 not named in the relay) and G-008 (the key-bar `more` layer readability, for the operator).
> - **Two new minors, record only:** G-009 (the `date_chip` BACKLOG entry the amended HLR-203 promises is not yet in `.dev-flow/BACKLOG.md`; owed at close) and G-010 (increment-006 §4b points to a PLAN.md decision-log entry for code-review round 2 that does not exist).
> - **Operator questions, not defects:** UXV2-2..UXV2-8 are routed to the close.

### Iteration 1 record (superseded by iteration 2)

- **Result (iteration 1):** `FAIL`, routed to `iterate-to-fix` (P3, tests and record only). The blockers were G-001 (C-18: AT-207 realised by two on-disk functions) and G-002 (a false kill claim in increment-005's packet). G-003 (HLR-203's text vs the corrected D-209) was major and needed a recorded amendment.
- **Requirements (iteration 1):** 22/23 pass · 1 blocker fail (HLR-207).
- **Evidence checklist (iteration 1):** qa-reviewer · 9 of 11 rows ✓. The ✗ rows were Layer B (G-001) and executor attribution / false claim (G-002).
- **Gate run of record (iteration 1):** `evidence/p4-gate.txt`, 1677 passed in 183.75 s, EXIT 0 (orchestrator).

---

## Detail (reference)

### Layer 0 — unit

Criterion: cyclomatic complexity ≥ 3, or data crossing a declared boundary (file-derived text into markup/notify). Excluded per C-51: the re-toned style constants, the key-bar style (002 collapsed its two branches into one), and copy/lookup dicts (003). Every node is green in the orchestrator's gate run.

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `_fit_text` (`views.py`, LLR-201.3) | cut + ellipsis + style-preserving fit (≥ 3 paths) | `tests/test_colour_budget_app.py::test_TC_213_a_long_value_is_cut_to_its_column_with_its_style` | pass — `executed` (orchestrator, gate run) |
| `reldue_token` soon branch (LLR-203.1) | five tone branches; +7/+8 boundary | `::test_TC_205_the_relative_due_token_is_amber_within_a_week` | pass — `executed` (orchestrator) |
| `GanttAxis.weekends()` (LLR-209.1) | `k ≤ 1` gate + all-weekend-days test per cell | `tests/test_gantt_polish.py::test_TC_211_half_a_day_per_cell_shades_both_cells`, `::test_TC_211_no_shading_above_a_day_per_cell`, `::test_TC_211_weekend_columns_are_shaded_at_one_day_per_cell` | pass — `executed` (orchestrator) |
| `gantt_echo` clip arrows (LLR-210.1) | left/right clip × two-date / one-date-open forms | `::test_TC_212_a_start_before_the_window_draws_the_clip_arrow`, `::test_TC_212_a_due_past_the_window_draws_the_right_arrow`, `::test_TC_212_a_start_on_the_first_day_keeps_its_bracket`, `::test_TC_212_the_one_date_forms_clip_too` | pass — `executed` (orchestrator) |
| `gantt_plan` `pressure` + `previous` (LLR-207.1) | 4-key ordering, skip-and-continue fill, Inbox key | `::test_TC_209_due_today_counts_as_urgency`, `::test_TC_209_a_tie_on_weight_goes_to_the_group_due_today`, `::test_TC_209_the_previous_group_is_offered_rows_before_urgency`, `::test_TC_209_the_inbox_can_be_the_previous_group`, `::test_TC_209_the_filtered_view_keeps_the_previous_group_too` | pass — `executed` (orchestrator) |
| `_gantt_frame` paging + hint row (LLR-205.1) | room 1 / ≥ 2; first / middle / last page; zero parts omitted | `::test_TC_207_a_paged_project_says_what_is_above_and_below[…]` ×3, `::test_TC_207_one_row_left_draws_no_hint_two_rows_draw_it` | pass — `executed` (orchestrator) |
| `_track_gantt_group` (`app.py`, LLR-207.2) | new group / same group / no selection | `::test_TC_210_only_the_group_just_left_is_remembered` | pass — `executed` (orchestrator) |
| `_notify_folded` from `action_phase_move` (LLR-206.1) | gantt × reaches-last-phase × count; **boundary**: a file-derived title into `notify` (C-17) | `::test_TC_208_only_the_move_that_finishes_notifies`, `::test_TC_208_the_count_is_the_groups_own_with_v_on`, `::test_TC_208_the_count_follows_the_filter`, `::test_TC_208_a_markup_title_is_shown_literally[…]` ×3 | pass — `executed` (orchestrator) |

**Measured by mutation, never by line coverage.** Each unit's named mutation and the RED it produced are below. All of these were executed by the increment author.

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `_fit_text` | X12: the ellipsis dropped. X13: the cut is one cell too wide. | yes — both KILLED | `evidence/inc001-mutations.txt:318`, `:339` |
| `reldue_token` | M10: the ≤ 7-day token grey again. M11: the +7 boundary moved (`< 7`); arms resolved 19, red 1 (TC-205). | yes — KILLED | `evidence/inc001-mutations.txt:191`, `:212` |
| `GanttAxis.weekends()` | G6: `k <= 1` written `k < 1`, so nothing is shaded at a day per cell. | yes — KILLED | `evidence/inc004-mutations.txt:108` |
| `gantt_echo` | G10 (`< 0` → `<= 0`, the first-day boundary), G11/G12 (the left/right arrow removed), M1/M2 (the open-ended forms) | yes — all KILLED | `evidence/inc004-mutations.txt:174`, `:195`, `:216`, `:241`, `:244` |
| `gantt_plan` | G4: urgency counts late only. G5: the due-today tie-break dropped. S1: `previous` ignored. S5: the Inbox key collides with "none". M5: the filtered branch drops `previous`. | yes — all KILLED | `evidence/inc004-mutations.txt:66`, `:87`; `evidence/inc005-mutations.txt:2`, `:78`, `:365` |
| `_gantt_frame` paging | G1: pages of the whole room. G2: no hint. G3: the hint not dim. | yes — all KILLED | `evidence/inc004-mutations.txt:2`, `:24`, `:45` |
| `_track_gantt_group` | S2: the previous group never remembered. S3: the same group overwrites it. | yes — KILLED | `evidence/inc005-mutations.txt:37`, `:72` |
| `_notify_folded` | T1: every move notifies. T2: the kanban notifies. T3: markup on. T4: escaped and markup off. T5: the count off by one. M1/M2: filter / `v` ignored. | yes — all KILLED | `evidence/inc005-mutations.txt:81`, `:116`, `:151`, `:186`, `:221`, `:260`, `:295` |

Increment 004's base tree cannot import `WEEKEND_BG`, so its RED-on-base is a *collection error* (shape). The packet declares this (`inc004-red.txt`) and does not count it. The value REDs of record for those units are the base-behaviour mutants G1, G2, G4, G6–G8, G11 and G12 above.

### UX walkthrough — only if trigger family D fired

> Trigger family D fired (every view, the key bar, the ribbon and the modals are user-visible). **Summarised from `evidence/p4-ux-walkthrough.txt`.** That walkthrough was `executed` by the `ux-reviewer` (a spawned sub-agent with `agents/ux-reviewer.md`, rev98) with verdict **PASS-WITH-NOTES**, and the orchestrator relayed its final message. qa-reviewer did not drive it. The reviewer's scripts and screenshots are in its own scratch directory and are not under the batch's evidence home.

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| 1 · Walking `down` keeps the group just left open | `3`, `up`×60, `down`×40 at 80×24 and 118×30 | previous group `▾` at every group change; up-moves 2 at 80×24 (`ta1`, `td2`), 1 at 118×30 | `executed` — pass; the residual is UXV2-7 (operator, D-203) |
| 2 · Ops & Security open on entry at 80×24 | `3` | `▾ Ops & Security ▲1`; API Platform folds (D-204) | `executed` — pass |
| 3 · A 30-task project shows what is off its page | `3`, `down`×31 | one dim hint row every step, never selected; a page flip jumps the highlight 16 rows | `executed` — pass; the flip is UXV2-7 (operator, D-213) |
| 4 · `]` on `tw2` posts the toast; `u` | `3`, `]`, `u`, wait 6 s | exact text; the toast does not cover the selection; it stays "done" up to 5 s after `u`, and at 80×24 it covers columns 39–79 of the bottom 4 rows | `executed` — pass; UXV2-3/4 (operator, D-214) |
| 5 · Weekend bands, including today on a Saturday | `3`, select `ta3`; Wed and Sat runs | `#1a1d22` columns from the day row through every body row, the selected row included; on a Saturday the today rule is accent over the shading; 256-colour index 234 vs 16 | `executed` — pass |
| 6 · Setup cursor and chips | `0`, `tab`, `down`, `space` | `>` walks the three sections; `on` bold bright vs `off` muted; `shared` is the same word on and off | `executed` — pass; UXV2-5 (operator, D-208) |
| 7 · Accent census | `1`–`5`, `7`–`9`, `0`, `tab`, `?`, `m`, `/` | every accent cell is a focus role | `executed` — pass |
| 8 · Key-bar `more` layer reads at 80 cells | `;` | every key bold bright, but no group boundary is visible | `failed` — readability, not a requirement breach (HLR-202 is met). UXV2-2, major for readability, is routed to the operator (D-211). |
| 9 · Ribbon local clock stands apart | — | local time bold `#e6edf7`; cities muted; the date differs from the clock only by bold | `executed` — pass |
| 10 · The word `today` and soon tones | `1`–`5`, `8`, `9` | review rail `+4d` amber; **Focus tiles/stale cards `Oct 4 +4d` slate** (`date_chip`); kanban `today` = `+3d` amber | `executed` — UXV2-1 (see G-003); UXV2-8 (operator, D-209) |
| 11 · 80×24 at `tm6` / `ta1` | walk | `tm6`: Ops folded, Data open; `ta1`: three folds, two blank rows | `executed` — UXV2-6 (operator, D-217) |
| 12 · Setup chips and the `>` cursor in accent | `0`, `tab`, `space` | `>` accent in all three sections | `executed` — pass |
| 13 · Ribbon at 80 and 118 | — | the same 75-character content fits both | `executed` — pass |

**Mechanism used:** `the UI framework the UI test driver` (Textual `App.run_test()` at 80×24 and 118×30; painted cells read from the compositor `render_strips`; dates frozen to `kg_board.TODAY` plus a Saturday run; board `kg_board.census`, team mode on). A browser driver is `n/a — a terminal app; no web surface`.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | `performed` (ux-reviewer, 13 items; also AT-201..210 in the orchestrator's gate run) |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | `performed` (ux-reviewer, against the P2 walkthrough list items 1–13 and D-201..D-219) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | `not performed — one-person product; the operator's verdict on the captures is planned outside the batch (requirements §6.1, D-216)` |

- **Method:** the ux-reviewer drove the real app with the real keys at two terminal sizes, read the compositor's painted cells (char, fg, bg, bold, reverse), and judged each item against its declared criterion.
- **Participants or population:** none (no user evaluation). The expert inspection was done by one reviewer agent.
- **Evidence of the evaluation:** `evidence/p4-ux-walkthrough.txt` (the relay), `evidence/captures/close-*` (SVG + text, 118×30 and 80×24) and `evidence/captures/base-*` for comparison.
- **Limits:** a reviewer agent is not the user. There was no physical terminal: truecolor and 256-colour were judged by computed hex and index, not by eye. A Textual screenshot is not a Windows Terminal frame. Only the default city clocks were used, and upward walking (`k`) was not exercised. P2 item UX-8 (amber's third meaning on the `==` badge) is not named in the relay (G-007).

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

Every node id below was confirmed on disk by `--collect-only` (qa-reviewer). Every "pass" comes from the orchestrator's gate run: iteration 1 is `evidence/p4-gate.txt` (1677 passed, EXIT 0, increment-005 frozen tree), and **iteration 2, the run of record, is `evidence/p4-gate2.txt`** (1677 passed, EXIT 0, after increment 006). The RED and mutation results were executed by the increment author.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-201 | test | `tests/test_colour_budget_app.py`: AT-201, TC-201 ×2, TC-202 ×4, TC-213 ×9 | 16 view × presentation pairs (guard `== 16`) × 3 sizes: 0 off-role accent runs; titles bold bright; Setup chips | pass | RED on base: 12 of 13 (`inc001-red-on-base.txt`); M1–M15 KILLED |
| HLR-202 | test | `-k "203 or 204 or AT_202"`: TC-203, TC-204 ×2, AT-202 | widths 24..160 × 9 views × 2 layers; ribbon 0 accent; `.modal-title` `#e6edf7`; `/` border `#2dd4bf` | pass | RED on the inc-001 tree (`inc002-red.txt`, 4 failed); 16 of 16 KILLED |
| HLR-203 | test | `-k "205 or AT_203"`: TC-205 ×2, AT-203 | +1/+4/+7 → `soon`, +8 → `dim`; ≥ 12 `▬` all `mut`; kanban `+Nd` amber (≥ 1) | pass (as verified). The text exceeds the verification (G-003). | RED on base (`+1d` `mut`, packet `#e6edf7`); M10–M12 KILLED |
| HLR-204 | test | `tests/test_english.py`: AT-204, TC-206 ×8 | 0 lexicon hits in every help modal, flow, Setup, standup, people × 3 filter modes; guard on the base surfaces; 44-cell fit | pass | RED on the inc-002 tree (8 failed); 14 of 14 KILLED (E8 mutates the input SET, C-31) |
| HLR-205 | test | `-k "207 or AT_205"`: TC-207 ×4, AT-205 | `tb0..tb18` + `▼ 11 below`; `tb19..29` + `▲ 19 above`; 50-task middle page; 80 cells; room 1 → no hint | pass | G1–G3 KILLED |
| HLR-206 | test | `-k "208 or AT_206"`: AT-206, TC-208 ×6 | exact toast text; Review step silent; kanban silent; 3 hostile titles literal | pass | RED on the inc-004 tree (`inc005-red.txt`); T1–T5, M1, M2 KILLED; security S-1 verified (increment-005 §4b) |
| HLR-207 | test | AT-207 (one node, `[size0-2]` 80×24 and `[size1-1]` 118×30), TC-209 ×3 (`previous`), TC-210 ×2 | 80×24: Website `▾` at `tm6`, Mobile `▾` at `ta1`, ≤ 2 up-moves; 118×30: the same fold checks, ≤ 1 | pass (iteration 2). Iteration 1: fail (blocker), G-001/G-002, now closed. | both arms RED on the inc-004 tree (`inc006-red.txt`); W1 KILLED (`inc006-mutations.txt`); qa scratch probe RED at `:533` under W1 and under previous-last; S1, S2 KILLED |
| HLR-208 | test | `-k "urgen or AT_208"`: TC-209 ×2, AT-208 | synthetic 80×14: B `▾` A `▸`; oracle 80×24: Ops `▾`, API `▸` | pass | G4, G5 KILLED |
| HLR-209 | test | `-k "211 or AT_209"`: TC-211 ×5, AT-209 | 22 columns on the day row and every body row at k = 1; 0 at k = 2; k = 0.5 both cells; Saturday rule; 256-index 234 ≠ 16 | pass | G6–G9, G13 KILLED |
| HLR-210 | test | `-k "212 or AT_210"`: TC-212 ×4, AT-210 | `◂` on cell 0 with `Sep 5` printed; `▸` at +230 on k = 7; first-day `⟦`; open forms | pass | G10–G12, M1, M2 KILLED |
| LLR-201.1 | test (unit) | TC-201: `::test_TC_201_every_view_title_is_bold_bright[118-30]`, `[24-10]` | title span bold `#e6edf7`, every view × presentation | pass | M1 KILLED |
| LLR-201.2 | test (unit) | TC-202: `::test_TC_202_the_census_set_is_complete` (guard), `::test_TC_202_every_accent_run_is_a_focus_role`, `::test_TC_202_the_census_can_see_the_accent` (non-vacuity), `::test_TC_202_the_legend_swatches_follow_their_marks` | per HLR-201; guard `== 16` | pass | M2–M6, M13–M15 KILLED; the guard is green on base by design (declared) |
| LLR-201.3 | test (unit) | TC-213: `::test_TC_213_setup_rows_keep_their_styles[True]`, `[False]`, `::test_TC_213_the_cursor_is_painted_on_every_section[…]` ×4, `::test_TC_213_a_long_value_is_cut_to_its_column_with_its_style`, `::test_TC_213_a_passing_check_is_done_not_accent`, `::test_TC_213_a_bad_project_colour_does_not_crash_setup[not a colour]`, `[bad1]` | ≥ 1 span per row; plain text = frozen base; `>` accent | pass | M7, M8, M9, M9b, F2, F9, X12, X13, L2 KILLED |
| LLR-202.1 | test (unit) | TC-203: `::test_TC_203_the_key_bar_wears_bright_keys_and_muted_words`; `;` covered by AT-202 (`bar_layer`) | hexes ⊆ {bright, mut, dim}; `key_bar_plain` = frozen | pass | K1–K3, MG, F3 KILLED |
| LLR-202.2 | test (unit) | TC-204: `::test_TC_204_the_ribbon_has_no_accent`, `::test_TC_204_modal_titles_and_the_key_map_are_bright` | ribbon 0 accent; `.modal-title` `#e6edf7`; `HelpScreen` 0 `#2dd4bf` | pass | R1, R2, A1, A2, C1, C3, MA–MC, P1 KILLED |
| LLR-203.1 | test (unit) | TC-205: `::test_TC_205_the_relative_due_token_is_amber_within_a_week`, `::test_TC_205_the_packet_is_quiet` | +7/+8 boundary; ≥ 12 `▬` `mut` | pass | M10–M12 KILLED |
| LLR-204.1 | test (unit) | TC-206: `tests/test_english.py::test_TC_206_the_lexicon_sees_every_base_surface` (guard), `::test_TC_206_no_literal_in_the_source_carries_the_old_copy`, `::test_TC_206_help_copy_is_english_and_fits`, `::test_TC_206_the_help_names_only_shipped_keys`, `::test_TC_206_the_views_paint_english[flow|setup|standup|people]` | per HLR-204; same section count; 44 cells | pass | E1–E10, X1–X4 KILLED; declared limit: Spanish outside the derived and frequent vocabulary would pass |
| LLR-205.1 | test (unit) | TC-207: `tests/test_gantt_polish.py::test_TC_207_a_paged_project_says_what_is_above_and_below[…]` ×3, `::test_TC_207_one_row_left_draws_no_hint_two_rows_draw_it` | per HLR-205 | pass | G1–G3 KILLED |
| LLR-206.1 | test (integration) | TC-208: `::test_TC_208_only_the_move_that_finishes_notifies`, `::test_TC_208_the_count_is_the_groups_own_with_v_on`, `::test_TC_208_the_count_follows_the_filter`, `::test_TC_208_a_markup_title_is_shown_literally[…]` ×3 | per HLR-206; `markup=False`, raw title | pass | T1–T5, M1, M2 KILLED |
| LLR-207.1 | test (unit) | TC-209: `::test_TC_209_due_today_counts_as_urgency`, `::test_TC_209_a_tie_on_weight_goes_to_the_group_due_today`, `::test_TC_209_the_previous_group_is_offered_rows_before_urgency`, `::test_TC_209_the_inbox_can_be_the_previous_group`, `::test_TC_209_the_filtered_view_keeps_the_previous_group_too` | per HLR-207/208; `INBOX_GROUP` ≠ `None` | pass | G4, G5, S1, S5, M5 KILLED |
| LLR-207.2 | test (integration) | TC-210: `::test_TC_210_only_the_group_just_left_is_remembered`, `::test_TC_210_the_legend_asks_the_same_frame` | previous = `pu` after a/u/s; the legend asks `pweb`; no-ghost | pass | S2, S3, S4, S6 KILLED (the legend node is green on the inc-004 tree by design and killed by S2/S4/S6: `inc005-mutations.txt:70`, `:77`, `:258`) |
| LLR-209.1 | test (unit) | TC-211: `::test_TC_211_weekend_columns_are_shaded_at_one_day_per_cell`, `::test_TC_211_no_shading_above_a_day_per_cell`, `::test_TC_211_half_a_day_per_cell_shades_both_cells`, `::test_TC_211_today_on_a_saturday_keeps_the_accent_rule_on_the_background`, `::test_TC_211_the_weekend_background_survives_256_colours` | per HLR-209 | pass | G6–G9, G13 KILLED |
| LLR-210.1 | test (unit) | TC-212: `::test_TC_212_a_start_before_the_window_draws_the_clip_arrow`, `::test_TC_212_a_due_past_the_window_draws_the_right_arrow`, `::test_TC_212_a_start_on_the_first_day_keeps_its_bracket`, `::test_TC_212_the_one_date_forms_clip_too` | per HLR-210 | pass | G10–G12, M1, M2 KILLED |

### Layer B — behavioral (black-box) acceptance

Every AT drives `TaskboardApp` through `App.run_test()` and reads what the app painted: `#board` `render()` spans in Textual's `rgb()` form, the `#keybar`/`#ribbon` widgets, modal `Label`/`Static` widgets and computed styles, and `App._notifications`. Every node passed in the orchestrator's gate run, and qa-reviewer's spot re-run of the AT nodes also passed (16 passed).

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-201 | AT-201 — `tests/test_colour_budget_app.py::test_AT_201_every_view_paints_the_accent_only_for_focus` | keys for every view in `VIEW_ORDER` + `tab` through every presentation, team mode on, 118×30; `0` | painted `#board` accent runs ⊆ focus roles across 16 pairs (asserted `== 16`); Setup `on` chip bold bright | repr: census board · boundary: team on, a task due today, URL cards · negative: base `◆ TASKBOARD`, `◐`, spine, Setup hints in accent (RED, `inc001-red-on-base.txt`) | pass |
| US-201 | AT-202 — `::test_AT_202_the_chrome_spends_no_accent` | key bar both layers (`;`), ribbon, `?`, `m`, `/` | 0 accent spans in `#keybar`/`#ribbon` (layer asserted); `.modal-title` color `#e6edf7` bold; key map styles ⊆ {b bright, mut, …}; focused `Input` border `#2dd4bf` | repr: gantt view · boundary: the `more` layer; the edited field keeps its accent (positive control C2/P1) · negative: base 18 accent keys (RED `inc002-red.txt`) | pass |
| US-201 | AT-203 — `::test_AT_203_soon_is_amber_and_the_packet_quiet` | `4`, then `3` | every painted `+1d..+7d` `#fbbf24` (≥ 1); every `▬` not bright | repr: oracle kanban · boundary: +7 (M11 is killed by TC-205, not by this AT) · negative: base `mut` tokens, bright packet | pass |
| US-202 | AT-204 — `tests/test_english.py::test_AT_204_no_spanish_is_painted` | every view + `?` in each, team mode on; `team_filter_cycle` ×3 in standup and people | painted `#board` text and help `Label`s: 0 lexicon hits; `all · team · personal` | repr: every view · boundary: three filter values; the action has no key (D-219) · negative: base `Uso`, `para qué es`, `todo · equipo` (RED) | pass |
| US-203 | AT-205 — `tests/test_gantt_polish.py::test_AT_205_a_long_project_says_how_much_is_off_the_page` | `3`, `down` ×30 on a 30-task project at 80×24 | exactly one hint row each step; the selection inside the `#viewport` scroll window; the hint is never the selected row; both `above` and `below` seen | repr: walk · boundary: first and last pages · negative: base paints no hint (G2 KILLED) | pass |
| US-203 | AT-206 — `::test_AT_206_a_finished_task_says_where_it_folded` | `3`, `]` at 118×30 | `App._notifications[-1].message` == `Build component library done · folded into ✓2 · u undo`, exactly one | repr: `tw2` · boundary and invalid in TC-208 (Review step, kanban, markup titles) · negative: base posts 0 (RED `inc005-red.txt`) | pass |
| US-204 | AT-207 — `::test_AT_207_the_project_just_left_stays_open[size0-2]`, `[size1-1]` (one function, 2 size arms; increment 006) | `3`, `down` ×24 at 80×24 and at 118×30 | painted `▾ Website` at `tm6`, `▾ Mobile` at `ta1` (both sizes); `_line_map` up-moves ≤ 2 / ≤ 1 | repr: oracle walk · boundary: rows run out at 80×24 · negative: both arms RED on the inc-004 tree (`inc006-red.txt`), W1 KILLED; the ≤ 1 bound alone is a declared pin (G-006) | pass (gate re-run). C-18 ✓ (iteration 1: ✗, G-001 closed) |
| US-204 | AT-208 — `::test_AT_208_urgent_projects_stay_open` | `3` on the synthetic board at 80×14, then the oracle board at 80×24 (one function) | painted `▾ Bee` / `▸ Aye`; `▾ Ops & Sec` / `▸ API Plat` | repr: oracle · boundary: weight tie → due-today · negative: G4 (late-only) KILLED | pass |
| US-205 | AT-209 — `::test_AT_209_weekends_are_painted_in_the_app` | `3` at 118×30 | painted day-row weekend columns == the axis's weekend cells, recomputed independently (≥ 20) | repr: k = 1 · boundary: k = 2 / 0.5 / Saturday in TC-211 · negative: G6/G8 KILLED. Body rows are not asserted at the surface (G-005). | pass |
| US-205 | AT-210 — `::test_AT_210_the_echo_shows_where_the_task_starts_earlier` | `3` at 118×30 (entry selection `tw2`) | painted day row: `◂` at the field's first cell, no `⟦` | repr: `tw2` · boundary: the first-day `⟦` and the right branch in TC-212 · negative: G11 KILLED | pass |

**C-18 reconciliation (one AT = one node) — iteration 2: ✓ for all ten.** `grep -n "def test_AT_2" tests/*.py` (`executed` by qa-reviewer) gives 10 functions for 10 ATs. AT-207 is one function parametrised over `((80, 24), 2)` and `((118, 30), 1)`, the form batch-01 accepted for AT-101/102, and both arms carry the whole chain (the fold checks at `tm6` and `ta1`, all 25 tasks reached, the up-move bound). G-001 is closed.

**Iteration 1 (kept): ✗ for AT-207, ✓ for the other nine.**
- **On disk:** `grep -rn "def test_AT_2" tests/` gives 11 functions for 10 ATs. AT-201..206 and AT-208..210 each realise in exactly one function, and each drives the whole chain §5 names. AT-208 joins its two boards inside one function.
- **AT-207 is two functions.** `test_AT_207_the_project_just_left_stays_open` (80×24) carries the §5 chain on its own. `test_AT_207_at_full_size_the_walk_moves_up_at_most_once` (118×30) carries HLR-207's "at 118×30 on at most 1" clause. Batch-01 accepted a *parametrised* function over two sizes (AT-101/102) as one node, but two separate functions are not one node. → **G-001, blocker.**

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | view keys `1`–`5`, `7`–`9`, `0` | `action_view` → `render_view(mode)` | yes | AT-201, AT-204 | ✓ |
| input | `tab` (presentations of lanes, kanban, focus) | `action_toggle_presentation` | yes | AT-201 (16 pairs asserted) | ✓ |
| input | team mode on / off | `team_state`, Setup toggle | on: yes (AT-201, AT-204); off: render level | AT-201; TC-213 `[False]` | ✓ |
| input | filter mode `todo`/`equipo`/`personal` | `team_filter_cycle` action (no key, D-219) | yes, through the app's own action | AT-204 | ✓ |
| input | `;` (key-bar layer) | `action_layer_toggle` → `bar_layer` (D-218) | yes, with the layer asserted | AT-202 | ✓ |
| input | `?`, `m`, `/` | `HelpModal`, `HelpScreen`, filter `Input` | yes | AT-202, AT-204 | ✓ |
| input | `3` (gantt), `4` (kanban) | `render_gantt`, kanban | yes | AT-203, AT-205..210 | ✓ |
| input | `down` walk | `action_cursor` → `nav_model` + `_track_gantt_group` | yes | AT-205, AT-207 | ✓ |
| input | `]` (phase move) | `action_phase_move` → `_notify_folded` | yes | AT-206; TC-208 (kanban, Review step) | ✓ |
| input | `v`, `/` filter on the toast count | `show_archived`, `search_query` | yes (app, keys) | TC-208 `_with_v_on`, `_follows_the_filter` | ✓ |
| input | terminal size 118×30 / 80×24 / 80×14 | panel w × h | yes | AT-201..210 at the named sizes | ✓ |
| input | board date (today on a weekend) | `today` | render level + ux walkthrough (Saturday run) | TC-211 Saturday | ✓ |
| output | painted accent runs on every view | `HEX["accent"]` sites | yes | AT-201 | ✓ |
| output | key bar, ribbon, modal titles, key map, focus border | `render_key_bar`, `Ribbon.update_clock`, `.modal-title`, `HelpScreen` | yes | AT-202 | ✓ |
| output | soon tokens, packet tone | `reldue_token`, `_gantt_bar` | yes (kanban, gantt) | AT-203 | ✓ (Focus tiles' `date_chip` is outside the verified seat: G-003) |
| output | English painted text | `help_usage`, flow, Setup, filter chrome | yes | AT-204 | ✓ |
| output | page hint row + `line_map` → `_scroll_selected_into_view` | `_gantt_frame` | yes (the viewport scroll asserted) | AT-205 | ✓ |
| output | toast | `notify(markup=False)` | yes (`App._notifications`) | AT-206 | ✓ |
| output | fold marks `▾`/`▸` | `gantt_plan(previous=)` | yes | AT-207, AT-208 | ✓ |
| output | legend under the sticky frame | `legend_entries(gantt_previous=)` → `HelpModal` | yes (`?` with a spy) | TC-210 legend | ✓ |
| output | weekend background | `_on_weekend` in `_gantt_field`, `gantt_day_row` | day row: yes (AT-209); body rows: render (TC-211) + ux item 5 | AT-209 | ✓ with note — G-005 |
| output | echo clip arrows | `gantt_echo` | yes | AT-210 | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| `1611` | `2` | `68` | `1677` | `1677` | `n/a — the project's CI command is the full suite (no slow marker)` / `1677` (gate re-run, `p4-gate2.txt`) | yes |

- **Iteration 2:** increment 006 adds `1677 = 1677 − 2 + 2`. The two AT-207 functions (each 1 node, counted in increment 005's +15) were deleted, and one node of 2 arms was added (`inc006-suite.txt` 1677; `p4-gate2.txt` 1677). Summed over the batch: `1611 − 2 + 68 = 1677`. The new-file count is still 66 (`test_gantt_polish.py` 33). Iteration 1's row read `1611 − 0 + 66 = 1677`, which is the same post-count before the re-cut.

- **Sources** (each packet's ledger is checked against its green transcript):
  - **base:** `evidence/base-suite.txt`, 1611 passed at `a0e7d9a`.
  - **001:** `1630 = 1611 − 0 + 19` (`inc001-green.txt` 1630). 19 nodes in `test_colour_budget_app.py`. 3 rewrites in place (`test_cells`, `test_colour_budget`, `test_team_views`).
  - **002:** `1634 = 1630 − 0 + 4` (`inc002-green.txt` 1634). TC-203, TC-204 ×2, AT-202. `test_keymap` rewritten in place.
  - **003:** `1643 = 1634 − 0 + 9` (`inc003-green.txt` 1643). `test_english.py` 9. 7 pins rewritten in place.
  - **004:** `1662 = 1643 − 0 + 19` (`inc004-green.txt` 1662). 19 in `test_gantt_polish.py`. TC-106 rewritten in place; one relaxation reverted (the file equals HEAD).
  - **005:** `1677 = 1662 − 0 + 15` (`inc005-green.txt` 1677). 14 in `test_gantt_polish.py` plus 1 parametrised arm of TC-213's bad-colour node (L2).
- **Cross-check** (`executed` by qa-reviewer):
  - `--collect-only` gives `test_colour_budget_app.py` 24 (= 19 + 4 + 1), `test_english.py` 9, and `test_gantt_polish.py` 33 (= 19 + 14), i.e. 66 new-file nodes. The suite collects 1677, the same as the gate run's 1677 passed.
  - The reverse-census transcripts agree with each packet: 001 3 failed / 1621; 002 1 / 1633; 003 8 / 1634; 004 2 / 1659; 005 0 / 1673.
- **Breakdown note (G-004):** increment-001's file table lists "AT-201, AT-203, TC-201, TC-202 ×3, TC-205 ×2, TC-213 ×6", which sums to 14, not 19. On disk the 19 are TC-201 ×2, TC-202 ×4 (guard included), TC-213 ×9, TC-205 ×2, AT ×2. The total is right and the breakdown is not.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | HLR-207 / US-204 | **C-18: AT-207 is realised by two on-disk functions:** `test_AT_207_the_project_just_left_stays_open` (80×24) and `test_AT_207_at_full_size_the_walk_moves_up_at_most_once` (118×30). | closed (iteration 2; was blocker) | `iterate-to-fix` (P3, test only). Merge them into one function parametrised over `(80, 24, ≤ 2, with tm6/ta1 asserts)` / `(118, 30, ≤ 1)`, net 0 on the ledger. Or re-home the full-size pin as a TC-209/210 preservation arm and say so in §3/§5. Re-collect to show one AT-207 node. **Closed:** increment 006 merged the two into one function parametrised over `((80,24),2)` and `((118,30),1)`; `grep "def test_AT_2"` → 10 for 10. Both arms RED on the inc-004 tree (`inc006-red.txt`); qa scratch probe: RED at `:533` under W1 and under previous-last. |
| G-002 | HLR-207 (increment-005 packet) | **False claim.** Increment-005 §4 says the two regression pins went "RED under S1, S2, S4, S6" ("each killed by a mutant instead"). That holds for `test_TC_210_the_legend_asks_the_same_frame` (`inc005-mutations.txt:70`, `:77`, `:258`). It is false for `test_AT_207_at_full_size_…`: it is green on the inc-004 tree (`inc005-red.txt`), it PASSED under S1, S2, T1–T5, M1, M2, M4 and M5 (`inc005-mutations.txt:25`, `:60`, …, `:356`), and S3–S6 never selected it (`mutants_inc005.json`). **qa probe (scratch copy, `executed` by qa-reviewer):** the node CAN fail. With the selected group no longer unfolded first, it went RED (2 failed). With the previous group offered last, it stayed green while the 80×24 node went RED. It is therefore a preservation bound that is not discriminating for this change, which is legitimate but not what the packet says. | closed (iteration 2; was blocker) | Correct increment-005 §4 ("RED counterfactual", "Arms that stayed GREEN"). Either add a named mutant that kills the pin to the battery, or declare it a preservation bound that is green on base by design. Fold it into G-001's re-cut. **Closed:** increment-005 §4 rows 77 and 81 re-read. They now say the legend pin was killed by S2, S4, S6 (`:70`, `:77`, `:258`) and the 118×30 walk by no mutant (a pin). That walk is now the 118×30 arm of the one AT-207 node, whose fold checks W1 kills (`inc006-mutations.txt`). |
| G-003 | HLR-203 / US-201 (UXV2-1, D-209) | HLR-203's statement reads "**A** relative due token one to seven days ahead shall be drawn in `soon`". The Focus tiles, cards and stale layouts paint `Oct 4 +4d` through `date_chip` (`views.py:528`, `_URG_COLOR["week"] = "later"`) in slate, which the ux walkthrough observed through the shipped surface. LLR-203.1 and the verification name only `reldue_token`, so the TC and AT pass. D-209 was corrected after P4 to put `date_chip` out of scope, but no §6.5 Before/After and no ledger entry records it, and `PLAN.md:85` still says "D-209 SOON shared everywhere". | closed (iteration 2; was major) | **I agree with the orchestrator's substance:** `date_chip` is a different helper, the operator's SOON answer was about the kanban, and the threshold never named the Focus tiles. **I do not agree that D-209 alone closes it:** the live contract still states a broader rule than the shipped app keeps. That is the black-box-fails / white-box-passes edge, so the requirement text must change. Close it either by (a) a recorded §6.5 amendment plus a LED entry narrowing HLR-203 to `reldue_token`'s seats, with `date_chip` → BACKLOG for the operator, or (b) the operator extending `date_chip`'s week tone (code, one more increment). Fix `PLAN.md:85` either way. **Closed by option (a):** §6.5 carries the full Before/After/Deleted/New and the re-derivation (AT-203 and TC-205 unchanged; US-201 re-read); LED .19 is recorded; HLR-203 now lists the `reldue_token` seats and names all 6 `date_chip` seats as outside (`grep "date_chip(" views.py` → 6 callers); `PLAN.md:85` is corrected. The BACKLOG entry is still owed (G-009). |
| G-004 | ledger (increment-001) | The file-table breakdown sums to 14 against the stated and actual 19. | closed (iteration 2) | Correct the breakdown in increment-001 §2. **Closed:** increment-001 §2 row 38 now reads TC-201 ×2, TC-202 ×4, TC-205 ×2, TC-213 ×9 + 2 AT = 19. |
| G-005 | HLR-209 | AT-209 observes the weekend background on the painted day row only. Body-row shading is asserted at render level (TC-211, every span and task row) and observed by the ux walkthrough (item 5), not by an AT. | minor | Accept as declared, or add the body-row assertion to AT-209 in the G-001 re-cut (same file). |
| G-006 | AT-207 (the 118×30 clause) | HLR-207's 118×30 bound equals base (1 up-move). It guards against regression and does not show the feature. | minor | Covered by G-002's declaration. |
| G-007 | P2 UX-8 | P2 routed "amber's third meaning on cards (`==` badge)" to the P4 walkthrough. The relayed walkthrough does not name the `==` badge; UXV2-8 covers `today` vs `+Nd` only. | minor | The orchestrator confirms with the ux-reviewer whether UX-8 was looked at. Otherwise carry it to the operator's capture review with UXV2-8. |
| G-008 | HLR-202 (UXV2-2) | ux item 8 `failed` on readability: the `more` layer shows no group boundary once the hues are gone. The requirement is met as written. | minor (operator decision; ux rates it major for readability) | The operator decides at close (D-211; option: a dim ` · ` separator). Not a defect against HLR-202. |
| G-009 | HLR-203 (amended) | HLR-203's After text sends the 6 `date_chip` seats to "(BACKLOG)", but `.dev-flow/BACKLOG.md` has no `date_chip` entry yet. | minor (iteration 2) | Add the entry at close, with UXV2-1 and the operator's choice (extend the week tone or keep slate). |
| G-010 | increment 006 §4b | §4b says "round 2: see `02-review.md`-style note in `PLAN.md` decision log", but PLAN.md's decision log has no increment-006 entry. Round 1 was PASS-WITH-NOTES with record-only folds (F1–F4), so nothing is blocked; the round-2 result is simply unrecorded. | minor (iteration 2) | Record code-review round 2 (or state that none ran) in increment-006 §4b before close. |

**Operator questions, not defects** (routed to the close): UXV2-3, UXV2-4 (D-214), UXV2-5 (D-208), UXV2-6 (D-217), UXV2-7 (D-203/D-213), UXV2-8 (D-209). Code review F4 (a stale previous group after a view detour, increment 005) is also routed. Pre-existing and not blocking: Setup at 80×24 wraps its status notes (the same in the base capture).

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| AT-202 + `test_keymap` layer node (D-218: `;` never reached the `more` layer since 8b73920, because `action_layer_toggle` read Textual's CSS `layer`; found by code review of increment 002, F3) | mutant F3 re-applies the pre-fix toggle: `evidence/inc002-mutations.txt:187-222`, AT-202 and `test_keymap.py::test_the_app_paints_its_keys_instead_of_a_blank_row` FAILED, `'primary' == 'more'` (executed by the increment author) | value (the node exists and the layer reads the wrong value) | yes. AT-202 asserts `bar_layer == layer` for each layer AND that the two painted bars differ (`seen[0] != seen[1]`); MG (accent on the `more` layer only) is killed by AT-202 alone. | pass — gate run (orchestrator) | `tests/test_colour_budget_app.py::test_AT_202_the_chrome_spends_no_accent`; `tests/test_keymap.py::test_the_app_paints_its_keys_instead_of_a_blank_row` |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- [✓] **Acceptance criteria use Given/When/Then.** Each AT states drive → observe in requirements §3 (Observable outcome / Shipped surface / threshold) and in the §5 AT table, which is the template's form.
- [✓] **Test cases have explicit Expected, not vague "works".** Every Layer A row cites a numeric threshold: 16 pairs, 22 columns, `▼ 11 below`, the exact toast text, ≤ 2 up-moves, index 234 ≠ 16.
- [✓] **Edge cases include empty, boundary, invalid, error.**
  - Empty: no history, no paged group, no previous group (`None`).
  - Boundary: +7/+8, room 1/2, k 0.5/1/2, the window's first day, a Saturday today, 24-cell bars.
  - Invalid: 3 markup titles, bad and non-string colours.
  - Error: the colour that crashed Textual (F9, L2) is now a node.
- [✓] **Regression checklist exists.** Five 5-probe reverse censuses with their transcripts. 12 pins rewritten in place with their laws kept, and 3 real laws kept by fixing the code. The full suite of 1677 ran in the orchestrator's gate run.
- [✓] **Exit criteria stated.** Requirements §5.2 are met in iteration 2: every HLR has a passing AT realised by one node, every LLR a passing TC, new assertions are RED on base or by mutation (the AT-207 ≤ 1 bound alone is a declared pin, G-006), and the gate re-run has 0 failures (1677 passed).
- [✓] **No real PII / secrets.** Fixtures come from `tests/kg_board.py` and `census()`. A grep of the batch record for home paths gives 0 hits. Security PASS-WITH-NOTES with 0 HIGH (increment-005 §4b). This file names no person or board content.
- [✓] **Mode declared** at the top of the artifact: `validation` (header note).
- [✓] **Validation mode: every case carries a result or one of the seven states, and each executed result names its executor.** Gate runs: orchestrator (`p4-gate.txt`, `p4-gate2.txt`). RED/mutations: the increment author (incl. `inc006-*`). Collect, greps, AT spot-run and both scratch probes: qa-reviewer. Walkthrough: ux-reviewer. Iteration 1's ✗ (G-002, the false kill claim) is closed: increment-005 §4 is corrected and re-read.
- [✓] **Layer B (black-box): every output-producing story's deliverable is observed through the SHIPPED surface.** US-201..205 are observed in the painted app with boundary and negative evidence, and C-18 holds for all ten ATs (AT-207 is one parametrised node). Iteration 1's ✗ (G-001) is closed.
- [✓] **Bidirectional surface-reachability.** 12 inputs and 10 outputs, all reached through the handler (matrix above). The note is G-005.
- [✓] **No unfilled template.** No `<...>` placeholder remains in this file. A grep of the packets for `{{` and `<...>` gives 0 hits.
