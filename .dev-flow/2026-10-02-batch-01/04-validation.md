# Validation — taskboard — Batch 2026-10-02-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1 and **names who executed each one**. The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Mode: validation.** Author: `qa-reviewer` (named sub-agent, `agents/qa-reviewer.md`), 2026-10-02. **Iteration 3:** re-issued on the frozen tree, after increment 004 round 3. Iteration 2's FAIL rested on stale gate evidence (G-010) and is superseded.
> **Who executed what.**
> 1. **The gate run.** It was **re-executed by the orchestrator** on the frozen tree (base `57a6075` + increments 001–004 round 3): `python -m pytest -q -p no:cacheprovider` → **1611 passed in 162.76 s, exit 0**. The transcript (redacted) is `evidence/full-suite-close.txt`, overwritten, and its header names the round-3 frozen tree. I read the tail from that run's own output and did not run the suite. **Revision check (`executed` by qa-reviewer):** the transcript was written at 09:28:18. The newest file under `taskboard/` and the three new test files is `taskboard/views.py` at 09:21:32, so the run postdates every edit. The 1606 and 1610 runs of iterations 1–2 are superseded.
> 2. **RED-on-base transcripts and mutation batteries.** These were **executed by the increment author** and recorded in `03-increments/increment-00N.md` + `evidence/`, including `inc004-red.txt` and `inc004-mutations.txt` (4 of 4 KILLED). I evaluate them here.
> 3. **My own checks.** I ran only read-only checks, each `executed` by `qa-reviewer`:
>    - `pytest --collect-only -q -p no:cacheprovider` to prove each node id below exists on disk: **1611 collected** = the gate run's 1611 passed; 77 in the three new files.
>    - `grep -rn "{{sha:"` over the batch record.
>    - in the P3 README fact-check, the README laws run in memory against HEAD's docs and four mutated READMEs.
> 4. **The UX walkthrough** was **executed by the `ux-reviewer`**, and so was its **re-check** of UXV-1/5/6. Both are summarised below from its reports as relayed by the orchestrator; I did not read the report files.
> **Result states** in this file use the seven words: `executed` · `approved` · `failed` · `blocked` · `not-run` · `n/a — <reason>` · `planned`. A node that is "pass" was `executed` by the orchestrator in the gate run. Every collected node passed: 1611 collected = 1611 passed, 0 failed, 0 skipped.

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
- **Layer 0:** `4 unit(s) met the criterion · 4 carry a named reddening mutation` (TC-101 ← G1, TC-104 ← G5, TC-105 ← G6, TC-112 ← G11; all KILLED, `evidence/inc001-mutations.txt`)
- **Requirements:** `30`/`30` pass (9 HLR + 21 LLR) · `0` blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative): US-101..104, through `TaskboardApp` under `App.run_test()` or the shipped files. C-18 ✓ after the re-cut: AT-101..AT-113 each realise in exactly one on-disk test function (AT-101/102 parametrised over two sizes).
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface · `0` gaps (one weak output noted, G-005: the README's gantt SVG is checked on disk, not in the commit)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative. Increment-001 §Reverse census: `cadena crítica`, `└─►`, `gantt_geometry`/`gantt_gauge`/`_task_reach` → 0 refs in `taskboard/`; 31 census nodes dispositioned. Increments 002–004 each declare 5 probes (increment-004 §4: B1 fired, 2 files green; B4 fired, measured by TC-116; B2/B3/A3 did not fire).
- **Test ledger:** ✓ reconciles (`1535 − 4 + 80 = 1611`; collected 1611 = passed 1611)
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 11 of 11 rows ✓ with evidence`

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.
> **Closed across iterations 2–3:** G-001 (AT re-cut), G-002 (TC-107 node), G-004 (packet fields), G-006 (UX walkthrough filled), G-008 (increment-004 packet), G-009 (UX re-check: UXV-1/5/6 pass; UXV-12 found and fixed) and G-010 (gate re-run on the frozen tree).
> **The verdict is PASS-WITH-NOTES, not PASS, because of:**
> - **G-005:** `docs/taskboard-gantt.svg` must be in the commit; the coordinator holds it.
> - **G-003 and G-007:** minor and declared.
> - **operator questions:** UXV-2/3 are routed to the operator; they are not defects.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `gantt_axis` (LLR-101.1) | one case per scale (5) + spare/context + Monday alignment; a week window keeps its latest due | `tests/test_gantt_board.py::test_TC_101_the_axis_takes_the_smallest_scale_that_fits`, `::test_TC_101_a_week_window_keeps_its_latest_due_inside` | pass — `executed` (orchestrator, gate run) |
| `gantt_due_chip` (LLR-101.4) | the four forms; width exact for 6 and 7; unparsable → `no due` | `tests/test_gantt_board.py::test_TC_104_the_due_chip` | pass — `executed` (orchestrator, gate run) |
| `gantt_dep_mark` (LLR-101.5) | the four outcomes + the no-start case | `tests/test_gantt_board.py::test_TC_105_the_dependency_mark` | pass — `executed` (orchestrator, gate run) |
| `gantt_cadence` (LLR-102.1) | k = 0.5, 1 → Mondays; 2, 3 → 1st/15th; 7 → 1st; synthetic 1/3 → daily | `tests/test_gantt_board.py::test_TC_112_the_cadence_rule` | pass — `executed` (orchestrator, gate run) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `gantt_axis` | G1 — the axis takes the LARGEST fitting scale | yes — KILLED, `-k TC_101`, arms 2 (red 1, green 1); restore sha256 `a4bfc0f0336737e4` ok | `evidence/inc001-mutations.txt:2` (executed by the increment author) |
| `gantt_due_chip` | G5 — the chip calls a future date late | yes — KILLED, `-k 'TC_104 or AT_103'`, arms 2 (red 2) | `evidence/inc001-mutations.txt:20` |
| `gantt_dep_mark` | G6 — the gutter counts finished dependencies | yes — KILLED, `-k TC_105`, arms 1 (red 1) | `evidence/inc001-mutations.txt:24` |
| `gantt_cadence` | G11 — Mondays needs MORE than one cell per day (`>=` → `>`) | yes — KILLED, `-k 'TC_112 or AT_104'`, arms 2 (red 2) | `evidence/inc001-mutations.txt:47` |

On the base tree these four nodes are also RED, but as a *shape* RED: the function is absent (`TypeError: 'NoneType'…`, `evidence/inc001-red-on-base.txt:823,824,831`). The mutations above are the *value* REDs that make the criterion count.

### UX walkthrough — only if trigger family D fired

> Trigger family D fired (user-visible gantt and kanban). **Summarised from the `ux-reviewer` walkthrough report**, which was `executed` by the ux-reviewer with verdict PASS-WITH-NOTES, as relayed to qa-reviewer by the orchestrator. qa-reviewer did not drive it and has not read the report file itself. The ux-reviewer's re-check of the increment-004 fixes was also `executed` by the ux-reviewer: UXV-1/5/6 pass, and it raised UXV-12 (fixed in round 3).

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| Pressing `3` shows the whole board: ruler, folds, chips and gutter as in the approved AX-2 / G-A frames | `App.run_test` at 118×34 and 80×24, key `3`, `export_screenshot` | identical to the frames. The differences are recorded decisions: D3 packets, budget `━`, no weekend shading (D5), title caption | `executed` — pass |
| `down` ×25 walks the drawn open work; `]` to done moves the cursor to drawn work | keys `down` ×25, `]` | selection always painted and in view | `executed` — pass |
| `?` in the gantt shows help that reads in its column (UXV-1) | key `?` | lines overflowed the column | `failed` → fixed in increment 004 (TC-116 help-fits nodes, H1/H4 KILLED) → **re-check `executed` by ux-reviewer: pass** |
| `/` and `F` narrow the gantt; `4` + `Tab` cycles the kanban layouts | keys `/` + text, `F`, `4`, `Tab` | the panel follows the filter/focus | `executed` — pass; UXV-2/3 (reflow surprises) routed to the operator as questions |
| Colour: the accent marks only today and the filter field inside the panels | keys `3`, `4`, `/` | accent only on today and the filter field | `executed` — pass |
| Low/info findings UXV-4..10 | as above | UXV-5 (packet over `◂`) and UXV-6 (scale label at k = 0.5) fixed in increment 004 (TC-107, TC-110 scale-label node; H3/H2 KILLED). UXV-7 and UXV-9 → BACKLOG. UXV-8 (a packet claim) corrected. UXV-4, UXV-10 informational | `executed`. Re-check of UXV-5/6 `executed` by ux-reviewer: **pass** |
| A project focus that a `/` filter empties still says the view is focused (UXV-12, raised by the re-check) | keys `F`, then `/` + text that excludes the focused project | the header lost its ` (focused)` label | `failed` (re-check) → fixed in increment 004 round 3: `test_TC_108_a_focus_the_filter_empties_still_says_focused`, RED round 3 in `inc004-red.txt`, H5 KILLED; pass in the gate run |

**Mechanism used:** `the UI framework the UI test driver` (Textual `App.run_test()` + `export_screenshot`, at 118×34 and 80×24)

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | `performed` (ux-reviewer; and AT-101..113 in the gate run) |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | `performed` (ux-reviewer, fidelity against the approved AX-2 / G-A frames) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | `not performed — one-person product; the operator's own reading of the captures is planned outside this batch (requirements §6.1)` |

- **Method:** the ux-reviewer drove the real app with the real keys at two terminal sizes and compared exported screenshots with the approved verdict frames.
- **Participants or population:** none (no user evaluation). The expert inspection is one reviewer agent.
- **Evidence of the evaluation:** the ux-reviewer report (held by the orchestrator; summarised here), `evidence/captures/`, and for the fixes `evidence/inc004-red.txt` + `evidence/inc004-mutations.txt`.
- **Limits:** a reviewer agent is not a user; the board is the seeded/oracle board; the UXV-12 fix is proven by its node and H5 but was not re-walked after round 3; UXV-2/3 are open operator questions, not defects.

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

All node ids were checked on disk by `pytest --collect-only`, `executed` by qa-reviewer. Every "pass" is the orchestrator's gate run (`evidence/full-suite-close.txt`: 1611 passed, exit 0, frozen tree).

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-101 | test | `tests/test_gantt_board.py` → AT-101[size0,size1], AT-109 (`v`), AT-110 (`F`), AT-111 (`/`), TC-102, TC-101 (×2) | k=1 @118×30, k=2 @80×24; 5 project rows; 0 rest rows; past/undated projects keep a row; `v`/`F`/`/` driven off default | pass | gate run; RED on base `inc001-red-on-base.txt:804-805,815-819` |
| HLR-102 | test | `-k fold` → TC-103 ×3, TC-111 | frame strings at both sizes; skip-and-continue board | pass | gate run; G3/G4/G16 KILLED |
| HLR-103 | test | `-k "AT_103 or chip or gutter"` → AT-103, TC-104, TC-105 | gutter column 30, 7 marks; chips `▲2d`/`today`/`no due`/`Oct 6` | pass | gate run; G5/G6 KILLED |
| HLR-104 | test | AT-102[size0,size1], AT-108, AT-113, TC-106 ×5 | 25 presses, selection in viewport each time; tw1→tw2 on entry; `]` to done moves one row | pass | gate run; G7/G8/G15/G17 KILLED |
| HLR-105 | test | AT-104, AT-112, TC-114, TC-110 scale-label node | Mondays / 1st/15th; `30` within 2 cells; no bottom axis; scale label fits at k = 0.5 (`.5 d/cell`, UXV-6) | pass | gate run; G11/G12, H2 KILLED |
| HLR-106 | test | `-k no_drop` → TC-113 ×2 | widths 60..160 step 4 × every scale; set of scales == `GANTT_SCALES`; echo-zone exemption | pass | gate run; G10 KILLED |
| HLR-107 | test | `-k "AT_105 or echo"` → AT-105, TC-115 ×2 | `⟦` Sep 24 / `⟧` Sep 28; tm4 → Oct 10–28, `◆` Nov 4 | pass | gate run; G12/G13 KILLED |
| HLR-108 | test | `tests/test_colour_budget.py` (14 nodes) | 0 non-today/non-filter accent cells; detector non-vacuous | pass | gate run; K1–K6 KILLED (`inc002-mutations.txt`) |
| HLR-109 | test + inspection | `tests/test_readme.py` (9 nodes) + qa fact-check rounds 1–2 + security privacy pass | 0 home paths; 9 views with keys; key table ⊆ bound keys; derived facts | pass | gate run; RED on base `inc003-red-on-base.txt` (7 failed / 5 passed); qa round 2 PASS-WITH-NOTES; security PASS-WITH-NOTES, 0 HIGH (increment-003 §4b) |
| LLR-101.1 | test (unit) | TC-101: `::test_TC_101_the_axis_takes_the_smallest_scale_that_fits`, `::test_TC_101_a_week_window_keeps_its_latest_due_inside` | 5 scales + spare/context + Monday | pass | G1 KILLED |
| LLR-101.2 | test (unit) | TC-102: `::test_TC_102_the_window_is_fitted_to_the_open_work` | lo Sep 23, hi Dec 1, start Sep 14 | pass | G2 KILLED (after strengthening; first run survived, named in increment-001) |
| LLR-101.3 | test (unit) | TC-103: `::test_TC_103_the_fold_rule_matches_the_verdict_frames`, `::test_TC_103_a_group_that_does_not_fit_is_skipped_not_the_end`, `::test_TC_103_a_late_tie_unfolds_the_earlier_due_first_and_height_0_unfolds_all` | two oracle sizes; skip board; tie; height 0 | pass | G3, G4 KILLED |
| LLR-101.4 | test (unit) | TC-104: `::test_TC_104_the_due_chip` | four forms; widths 6/7 | pass | G5 KILLED |
| LLR-101.5 | test (unit) | TC-105: `::test_TC_105_the_dependency_mark` | four outcomes + no start; 7 marks at column 30 | pass | G6 KILLED |
| LLR-101.6 | test (integration) | TC-106: `::test_TC_106_nav_is_the_plans_open_work_and_every_selection_is_drawn`, `::test_TC_106_a_tall_group_pages_and_keeps_its_count`, `::test_TC_106_span_overflow_draws_the_page_holding_the_selection`, `::test_TC_106_every_selection_is_drawn_at_every_height`, `::test_TC_106_groups_exactly_filling_the_body_keep_every_span_and_the_selection` | nav == plan; every selection in `line_map`; 30-task and 30-project boards | pass | G7, G17 KILLED |
| LLR-101.7 | test (integration) | TC-107: `tests/test_gantt_board.py::test_TC_107_the_motions_ride_the_fitted_axis_and_clear_the_clip_marker` (new in increment 004); preservation: `tests/test_flow.py::test_flow_preserves_gantt_row_width`, `::test_render_view_threads_tick_to_gantt`, `::test_packet_moves_as_the_tick_advances`; `tests/test_motion.py::test_the_gantt_flow_rides_the_ONE_shared_clock`, `::test_the_pulse_runs_only_where_the_work_is_behind`, `::test_the_pulse_rides_the_ONE_shared_clock_and_clears_the_floor`, `::test_the_pulse_changes_no_colour` | packet one cell per tick (8 distinct cells over 8 ticks); packet `▬` on a `━` chain reach; never on the `◂` clip marker (UXV-5); pulse laws green | pass | gate run; RED `evidence/inc004-red.txt`; H3 KILLED (`inc004-mutations.txt:9`) |
| LLR-101.8 | test (integration) | TC-108: `::test_TC_108_board_text_is_never_parsed_as_markup`, `::test_TC_108_the_focused_header_paints_a_trailing_backslash_as_typed`; `::test_TC_108_a_focus_the_filter_empties_still_says_focused` (UXV-12, increment 004 round 3; RED `inc004-red.txt` round 3) | 6 payloads × seats; render succeeds; literal text | pass | RED on base: `MarkupError: closing tag '[/]'…` (`inc001-red-on-base.txt:678`); G9, H5 KILLED |
| LLR-101.9 | test (integration) | TC-109 = the AT-108 and AT-113 nodes, as the LLR's executed verification states (G-003) | entry and `]` arms | pass | G8, G15 KILLED |
| LLR-101.10 | test (unit) | TC-110: `::test_TC_110_every_row_is_exactly_the_width[24,39,40,59,60,80,99,100,118,160]`, `::test_TC_110_the_vertical_split`, `::test_TC_110_a_narrow_label_sheds_its_counts_before_it_overflows`, `::test_TC_110_the_scale_label_fits_at_half_a_day_per_cell` (increment 004, UXV-6) | every row == width for 24..160; 26 rows + legend @118×30, 21 rows @80×24 | pass | G14 KILLED (9 of 12 arms red); H2 KILLED. The 10 width arms are green on base (preservation, declared in increment-001) |
| LLR-101.11 | test (unit) | TC-111: `::test_TC_111_the_group_label_forms` | the frame strings; label 25 vs 26 | pass | G4 KILLED (TC-111 arm) |
| LLR-102.1 | test (unit) | TC-112: `::test_TC_112_the_cadence_rule` | per scale + synthetic daily | pass | G11 KILLED |
| LLR-102.2 | test (integration) | TC-113: `::test_TC_113_no_drop_law_over_every_scale_and_width`, `::test_TC_113_a_tick_never_touches_the_echo_label` | per HLR-105/106 | pass | G10 KILLED |
| LLR-102.3 | test (integration) | TC-114: `::test_TC_114_the_month_row` | per HLR-105; every band ≥ 4 cells named | pass | G12 KILLED |
| LLR-102.4 | test (unit) | TC-115: `::test_TC_115_the_echo_carries_exact_dates`, `::test_TC_115_the_echo_falls_back_to_the_label_column_untruncated` | four task shapes; fallback untruncated | pass | G13 KILLED (via AT-105) |
| LLR-102.5 | test (unit) | TC-116: `::test_TC_116_the_legend_names_what_the_gantt_draws`, `::test_TC_116_the_gantt_legend_reads_the_frame_on_screen`, `::test_TC_116_the_gantt_help_fits_its_column[size0,size1]` (increment 004, UXV-1); preservation `tests/test_legend.py` (no-ghost), `tests/test_vertical_fill.py::test_the_gantt_legend_sits_on_the_last_row` (3 arms) | no-ghost law green; `┃`/`⟦` entries with a selection | pass | G18, H1, H4 KILLED |
| LLR-103.1 | test (unit) | TC-117: `tests/test_colour_budget.py::test_TC_117_the_title_is_bold_bright[kanban-grouped,kanban-lanes,kanban-matrix,gantt-grouped]` | 4 title spans bright + bold | pass | K5, K6 KILLED |
| LLR-103.2 | test (unit) | TC-118: `::test_TC_118_the_critical_chain_is_structure_not_hue` | `tm2..tm5` reach `━` bright bold; `chain 4` | pass | RED on base (`inc002-red.txt`) |
| LLR-103.3 | test (unit) | TC-119: `::test_TC_119_the_kanban_paints_no_accent`, `::test_TC_119_the_census_can_see_the_accent`, `::test_TC_119_the_shared_card_tokens_left_the_accent_everywhere`, `::test_TC_119_the_gantt_paints_only_today_and_the_filter[118-30,80-24,60-20,40-14,24-10]` | census over every presentation × group (reach asserted); non-vacuity; shared tokens in the other views | pass | K1–K4 KILLED |
| LLR-104.1 | test + inspection | TC-120: `tests/test_readme.py::test_TC_120_the_readme_names_every_view_with_its_key` (preservation pin), `::test_TC_120_question_mark_is_documented_as_help`, `::test_TC_120_the_readme_installs_from_a_clone_and_counts_no_tests`, `::test_TC_120_the_readme_states_the_view_count_from_the_app`, `::test_TC_120_every_key_the_readme_documents_is_bound`, `::test_TC_120_the_facts_the_readme_states_match_the_code`; instrument `::test_the_home_path_pattern_sees_every_form_and_spares_placeholders` | per HLR-109 | pass | RED on base: 5 of the 6 TC-120 nodes (`inc003-red-on-base.txt`); in-memory mutations (phantom key, 341 cities, renamed flag, swapped colour) each RED (qa round 2, `executed` by qa-reviewer) |
| LLR-104.2 | test + inspection | TC-121: `::test_TC_121_run_md_carries_no_home_path_and_no_retired_flow` | 0 paths; no `6` key; no worktree flow | pass | RED on base (2 home paths); each of the 3 arms individually true on base RUN.md (qa round 1, `executed` by qa-reviewer) |

### Layer B — behavioral (black-box) acceptance

Every AT drives `TaskboardApp` through `App.run_test()` and reads the painted panel (`app.query_one("#board").render()` and its span styles). The exception is AT-107, whose deliverable is the shipped file. Every node passed in the orchestrator's gate run on the frozen tree (1611 passed). Each one is also RED on the base tree on its own assertion (`inc001-red-on-base.txt:804-817`, `inc002-red.txt`, `inc003-red-on-base.txt`).

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-101 | AT-101 — `tests/test_gantt_board.py::test_AT_101_the_whole_board_is_on_screen[size0]`, `[size1]` (one function, 2 size arms) | keys `3` at terminal 118×30 and 80×24 | painted panel: every project's span row, folds per HLR-102, no `not shown` | repr: oracle board · boundary: 80×24 folds · negative: base paints `+9 not shown` (RED) | pass |
| US-101 | AT-102 — `::test_AT_102_down_walks_the_drawn_open_work[size0]`, `[size1]` (one function, 2 size arms) | `3`, `up`, `down` ×25 | selection painted in reverse inside the viewport (`scroll_offset.y ≤ row < scroll_offset.y + height`) after each key; ruler rows 1–2; end key a no-op | repr: walk · boundary: last task + `down` · negative: base `KeyError: 'td4'` (cursor on an undrawn row) | pass |
| US-101 | AT-103 — `::test_AT_103_chips_and_the_dependency_gutter` | `3` | painted chips and the `↳` gutter column | repr: 7 marks · boundary: no due / today / late · negative: base `└─►` in the label (RED) | pass |
| US-101 | AT-108 — `::test_AT_108_entering_on_a_done_task_lands_on_drawn_work` | `3` on a done selection, then `down` | painted selection on drawn open work | repr: tw1 → tw2 · boundary: entry on rest work · negative: base `'tw1' == 'tw2'` failed; G15 KILLED | pass |
| US-101 | AT-113 — `::test_AT_113_finishing_a_task_moves_one_row_and_an_extra_key_is_local` | `]` to done; one more `]`; `down` | the cursor moves one row to drawn work; the extra key stays local | repr: finish a task · boundary: the group's last open task done · negative: base RED (`inc001-red-on-base.txt:814`, under its former name); G8 KILLED | pass |
| US-101 | AT-109 — `::test_AT_109_show_archived_grows_the_rest_count` | `v` | `✓n` grows on the span row | non-default drive (C-10a) · negative: base RED (`inc001-red-on-base.txt:815`) | pass |
| US-101 | AT-110 — `::test_AT_110_focus_narrows_to_one_group_and_its_window` | `F` | one group and its own window | non-default drive · negative: base RED (`:816`, former name) | pass |
| US-101 | AT-111 — `::test_AT_111_a_filter_narrows_nav_and_keeps_the_ruler` | `/` + text + `enter`, `up`/`down` | nav follows the filtered board; the ruler under the filter bar | non-default drive · negative: base RED (`:817`, former name) | pass |
| US-102 | AT-112 — `::test_AT_112_the_legend_under_a_filter_describes_the_filtered_frame` | `/` + text, then `?` | the help legend describes the filtered frame | boundary: filter + help together · negative: RED on the pre-fold snapshot under its former name (`evidence/inc001-review-red.txt:140-170`) | pass |
| US-102 | AT-104 — `::test_AT_104_the_ruler_is_at_the_top` | `3` | panel rows 1–2 = month row + day row; cadence label; no bottom axis | repr: Mondays @118 · boundary: sweep in TC-113 · negative: base rows 1–2 are task rows (RED); G11 KILLED | pass |
| US-102 | AT-105 — `::test_AT_105_the_echo_follows_the_selection` | keys to `tw3`, then to `tm4` | day-row bracket + dates; month-row `◆`; label `◆ dates · Mobile App` | repr: tw3 · boundary: tm4 cross-month · negative: old `⟦` gone; G13 echo pinned KILLED | pass |
| US-103 | AT-106 — `tests/test_colour_budget.py::test_AT_106_the_panels_paint_the_accent_only_for_today_and_the_filter` | `4`, `tab`, `tab`, `3`, `/` + text + `enter` | painted spans in Textual's `rgb()` spelling: 0 non-today, non-filter accent cells | repr: kanban + gantt · boundary: filter bar keeps accent · negative: increment-001 accent sites RED (`inc002-red.txt`); K2/K4 KILLED | pass |
| US-104 | AT-107 — `tests/test_readme.py::test_AT_107_the_readme_carries_no_home_path` | the shipped file `README.md` | the file a reader opens | repr: README · boundary: placeholders spared (instrument node) · negative: base README 6 home paths (RED) | pass |

**C-18 reconciliation (one AT = one node) — iteration 2: ✓.**
- **The re-cut:** the AT registry was re-cut in increment 004 (requirements §3/§5; ledger LED .26–.28). AT-108 split into AT-108 (entry) and AT-113 (finish + overshoot). AT-109 split into AT-109 (show archived), AT-110 (focus), AT-111 (filter) and AT-112 (legend under a filter); AT-112 gives the formerly orphan 4th node its own spec scenario.
- **On disk:** `pytest --collect-only` (`executed` by qa-reviewer) shows each of AT-101..AT-113 realised by exactly one test function, each driving the whole chain. AT-101 and AT-102 are one function parametrised over the two named terminal sizes, which is accepted (the same node, a second size).
- **Outcome:** G-001 is closed.

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | key `3` (gantt) | `action_view('gantt')` → `render_view("gantt")` | yes | AT-101..105, AT-108..113 | ✓ |
| input | key `4` + `tab` (kanban, 3 presentations) | `action_view('kanban')`, `toggle_presentation` | yes | AT-106 (+ TC-119 census over every presentation × group) | ✓ |
| input | `down` / `up` | `action_cursor` → `nav_model("gantt")` | yes | AT-102, AT-111 | ✓ |
| input | `]` (phase move to done) | `action_phase_move` → `_select_first` repair | yes | AT-113 (and AT-108 for entry) | ✓ |
| input | `v` (show archived) | `show_archived` | yes | AT-109 (`✓n` grows) | ✓ |
| input | `F` (project focus) | `gantt_focus` | yes | AT-110 | ✓ |
| input | `/` + query (filter) | `search_query` → `filtered_board` + overlay | yes | AT-111, AT-106 | ✓ |
| input | `?` (help / legend) | `action_legend` → `legend_entries` of the frame on screen | yes | AT-112 (legend under filter); TC-116 incl. `test_TC_116_the_gantt_help_fits_its_column[size0/1]` | ✓ |
| input | selection (non-default) | `selected_id` | yes | AT-105 (tw3 → tm4), AT-102 | ✓ |
| input | terminal size 118×30 / 80×24 | panel width × height | yes | AT-101, AT-102 (both sizes); TC-110 widths 24..160; TC-113 widths 60..160 | ✓ |
| input | README / RUN.md text | the files | yes | AT-107, TC-120, TC-121 | ✓ |
| output | painted gantt panel rows (spans, folds, chips, gutter) | `render_gantt` | yes | AT-101, AT-103 | ✓ |
| output | ruler (month row + day row, echo) | `render_gantt` ruler rows | yes | AT-104, AT-105 | ✓ |
| output | in-view legend row / help legend | `legend_entries`, LLR-101.10 legend row | yes | AT-112 (legend under filter), TC-116, `test_vertical_fill::test_the_gantt_legend_sits_on_the_last_row` | ✓ |
| output | `line_map` → viewport scroll (consumer `_scroll_selected_into_view`) | `render_gantt(line_map=…)` → `app._scroll_selected_into_view` | yes — the consumer's outcome is asserted (`scroll_offset`) | AT-102 | ✓ |
| output | nav order (consumer `_nav_columns`, `_select_first`) | `nav_model("gantt")` | yes — through real keys | AT-102, AT-108, AT-113 | ✓ |
| output | accent cells on kanban + gantt panels | `HEX["accent"]` sites | yes — painted spans | AT-106 | ✓ |
| output | `README.md`, `RUN.md` | the files at the repository root | yes | AT-107, TC-120, TC-121 | ✓ |
| output | `docs/taskboard-gantt.svg` (README hero image) | `evidence/make_readme_gantt.py` | on disk yes; **in the commit: not yet** (`git status`: `??`) | `test_keymap.py::test_every_image_the_readme_shows_exists` (filesystem only) | ✓ with note — G-005 |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| `1535` | `4` | `80` | `1611` | `1611` | `n/a — the project's CI command is the full suite (no slow marker)` / `1611` | yes |

- **Sources:**
  - base: `evidence/base-suite.txt` (1535 passed at `57a6075`).
  - increment 001: `1588 = 1535 − 4 + 57`. The 4 deleted are the gantt arm of `test_every_view_marks_an_archived_row` and the 3 gantt arms of the bottom-axis law. The 57 added are 48 in `test_gantt_board.py`, 3 legend-row arms and 6 nodes of `test_readme.py`.
  - increment 002: `1606 = 1588 − 0 + 18`: 14 in `test_colour_budget.py`, 1 trailing-backslash node and 3 more `test_readme.py` nodes.
  - increment 003 adds nothing of its own; its nodes are counted inside 001/002.
  - increment 004: `1611 = 1606 − 0 + 5`: `test_TC_116_the_gantt_help_fits_its_column[size0]`, `[size1]`, `test_TC_110_the_scale_label_fits_at_half_a_day_per_cell`, `test_TC_107_the_motions_ride_the_fitted_axis_and_clear_the_clip_marker`, `test_TC_108_a_focus_the_filter_empties_still_says_focused`. The AT re-cut renamed 4 functions in place (net 0). This matches increment-004 §Signed-balance.
- **Cross-check:**
  - collected per file (`executed` by qa-reviewer): `test_gantt_board.py` 54, `test_colour_budget.py` 14, `test_readme.py` 9 → 77 new-file nodes, plus 3 legend-row arms = 80 ✓.
  - the gate run: 1611 passed (orchestrator, frozen tree).
- **G-004 closed:** increment-003 now says 9 nodes; `grep -rn "{{sha:"` over the packets and evidence finds no placeholder (the only hit is this file's own G-004 row, which quotes it).

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | HLR-104 / HLR-101 | C-18: AT-108 had 2 functions and AT-109 had 4. | closed | Re-cut in increment 004 (AT-108..AT-113, one function each; LED .26–.28), verified on disk by collect-only. |
| G-002 | LLR-101.7 | No node carried TC-107; the chain-packet clause was unasserted. | closed | `test_TC_107_the_motions_ride_the_fitted_axis_and_clear_the_clip_marker` asserts one cell per tick, `▬` on a `━` chain reach, and never on `◂`; RED in `inc004-red.txt`, H3 KILLED. One residue: its `"▬" != CRITICAL_REACH` line compares two constants, but the packet-found-on-a-`━`-reach assertions around it carry the clause. |
| G-003 | LLR-101.9 | TC-109 has no white-box node; it is realised by AT-108 and AT-113, by the LLR's own design; G8/G15 kill it. | minor | Accept as declared. |
| G-004 | ledger (increment-003) | Packet count "10" and an unfilled `{{sha:` placeholder. | closed | increment-003 now says 9 nodes; the grep finds no placeholder in packets or evidence. |
| G-005 | HLR-109 (README hero image) | `docs/taskboard-gantt.svg` is untracked; the image law checks the filesystem, not the commit. | minor (major if the commit omits it) | The coordinator includes it in the commit and verifies with `git ls-files docs/taskboard-gantt.svg`; the orphaned `docs/taskboard-gantt.png` is the operator's call. |
| G-006 | trigger family D | The UX walkthrough was `not-run` at iteration 1. | closed | Filled from the ux-reviewer report (§UX walkthrough). |
| G-007 | LLR-104.1 | The views pin passes on base (declared preservation); the key-bound node ERRORS rather than failing on base (no `## Keys` heading). | minor | Optional: assert the heading exists before splitting. |
| G-008 | increment 004 | No packet existed. | closed | `03-increments/increment-004.md`: 1 SOURCE file (`views.py`), reverse census (5 probes), mutation verdicts 5/5 KILLED (battery re-run on the round-3 tree, restore sha256 `38373f7da6c96c01…`), code-reviewer rounds 1–3 OK to advance with 0 HIGH, signed balance `1611 = 1606 − 0 + 5`, round-3 edit declared. |
| G-009 | UXV-1, UXV-5, UXV-6 | The re-check was pending. | closed | ux-reviewer re-check: UXV-1/5/6 pass. It raised UXV-12, fixed in round 3 with its own node (H5 KILLED). |
| G-010 | gate evidence | The gate transcript predated the last edits (1610 vs 1611). | closed | Re-run on the frozen tree: 1611 passed, exit 0, transcript at 09:28:18 after the last edit at 09:21:32; collected 1611. |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| TC-108 (S-1: a project named `[/]` in the focused gantt header raised `MarkupError` on the shipped base tree; found by the security-reviewer at P2) | `evidence/inc001-red-on-base.txt:573-680` — `rich.errors.MarkupError: closing tag '[/]' at position 45 has nothing to close` (executed by the increment author) | value (the shipped header seat crashes on that payload; the node exists on base) | yes — it asserts the plain text holds each payload literally (or its fitted prefix + `…`), not merely that the render returns; G9 (header unescaped) KILLED | pass — gate run (orchestrator) | `tests/test_gantt_board.py::test_TC_108_board_text_is_never_parsed_as_markup` (+ `::test_TC_108_the_focused_header_paints_a_trailing_backslash_as_typed` for the trailing `\` form) |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- [✓] **Acceptance criteria use Given/When/Then.** The ATs are stated as drive → observe in requirements §3 (Observable outcome / Shipped surface / threshold) and §5 AT table. That is the template's form, and every AT names the input, the surface and the observed outcome.
- [✓] **Test cases have explicit Expected, not vague "works".** Every Layer A row cites a numeric threshold (k values, frame strings, column 30, 25 presses, 0 accent cells, 0 home paths).
- [✓] **Edge cases include empty, boundary, invalid, error.** Empty: empty board / no open task / no selection. Boundary: widths 24..160, both terminal sizes, last task + `down`, 30-task and 30-project boards. Invalid: unparsable date, 6 markup payloads, trailing `\`. Error: `n/a — the renderer raises nothing` (HLR boundary catalogs), except the S-1 `MarkupError`, now covered by TC-108.
- [✓] **Regression checklist exists.** The reverse census in each packet (increment-001: 31 nodes; increments 002–004: 5 probes each), the preservation laws named in Layer A, and the full suite of 1611 in the orchestrator's gate run on the frozen tree.
- [✓] **Exit criteria stated.** Requirements §5.2 are met: every HLR has a passing AT, every LLR a passing TC, the new nodes were RED on base or under mutation, and the full suite has 0 failures (1611 passed).
- [✓] **No real PII / secrets.** Fixtures are `tests/kg_board.py` and the seeded demo board. The security pass (increment-003 §4b) verified 0 HIGH, and S-7 (a username in temp paths in evidence transcripts) was fixed. This file names no person, path or board content.
- [✓] **Mode declared** at the top of the artifact: `validation` (header note).
- [✓] **Validation mode: every case carries a result or one of the seven states, and each executed result names its executor.** Gate run: orchestrator. RED/mutation runs: the increment author. Collect-only, the placeholder grep and the in-memory README mutations: qa-reviewer. UX walkthrough and its re-check: ux-reviewer (`executed`).
- [✓] **Layer B (black-box): every output-producing story's deliverable is observed through the SHIPPED surface.** US-101..103 through `TaskboardApp` + `App.run_test()` on the painted panel; US-104 through the shipped file. Each has boundary + negative evidence (Layer B table).
- [✓] **Bidirectional surface-reachability.** 11 inputs and 8 outputs, all reached through the handler (matrix above). The one note is G-005 (commit inclusion).
- [✓] **No unfilled template.** No `<...>` placeholder remains in this file. The P3-packet placeholder of iteration 1 is gone (G-004 closed).
