# Requirements ledger — taskboard — Batch 2026-10-02-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-02-batch-01.1 — G-A replaces the shipped gantt's fixed 2-day axis
- **Requirement:** HLR-101
- **Date:** 2026-10-02
- **What changed:** before this batch the gantt laid every board on a fixed axis of two days per cell with today at 30 % of the field, and drew every task row (done included) until the height ran out ("+N not shown"). It now fits the window to the open work at the smallest of 0.5/1/2/3/7 days per cell.
- **Why:** operator verdict rounds 1–2, 2026-09-30 ("Gantt: G-A"); measured on the oracle board: 9 rows hidden at 118×30, 15 at 80×24 (P-1).
- **Evidence:** `NOTES.md` "Verdict (operator, 2026-09-30)" and "Round 2 verdict"; prototype frames `out/G-A-118x30.txt` (k = 1, "1 cell = 1 day") and `out/G-A-80x24.txt` (k = 2) — the thresholds of HLR-101 are read off these executed renders (C-39).

### LED-2026-10-02-batch-01.2 — folding and the "nothing hidden" rule
- **Requirement:** HLR-102
- **Date:** 2026-10-02
- **What changed:** non-selected projects fold to their span row when rows run out; the selected task's project unfolds first, then the most-late; rest work folds to `✓n`.
- **Why:** NOTES.md open ruling carried to implementation: "G-A unfolds the selected project plus the most-late projects while rows remain"; commission: "no project hidden".
- **Evidence:** `out/G-A-118x30.txt` (Data Warehouse `4 open` folded), `out/G-A-80x24.txt` (Mobile App and Data Warehouse folded).

### LED-2026-10-02-batch-01.3 — compact due chip and dependency gutter
- **Requirement:** HLR-103
- **Date:** 2026-10-02
- **What changed:** the `start → due` date pair becomes one due chip; the `└─►` drawn after the title becomes `↳` in its own gutter column.
- **Why:** G-A verdict; the baseline measurement "dep arrows overwrite labels" (NOTES.md "Measured baseline").
- **Evidence:** `variants_gantt.py` `due_chip`, `gutter`; `out/G-A-118x30.txt`.

### LED-2026-10-02-batch-01.4 — nav walks the drawn open work only
- **Requirement:** HLR-104
- **Date:** 2026-10-02
- **What changed:** the gantt's nav no longer walks done tasks or tasks shed below the fold.
- **Why:** F-3 law; with folding, rest work is not drawn (D2); P-2 measured the shipped nav reaching 7–11 undrawn ids.
- **Evidence:** P0 probe `evidence/p0-probes.txt`.

### LED-2026-10-02-batch-01.5 — the ruler moves to the top (AX-2)
- **Requirement:** HLR-105
- **Date:** 2026-10-02
- **What changed:** the axis row under the field is removed; two rows under the header carry months and day numbers.
- **Why:** round 5: "the bottom axis drops labels; operator suggested month + day rows at the top"; verdict "Ruler AX-2 (es mejor)".
- **Evidence:** `out/AX-2-118x30.txt` (`Mondays · 1 cell = 1 day`), `out/AX-2-80x24.txt` (`1st/15th · 2 d/cell`); P-3.

### LED-2026-10-02-batch-01.6 — the no-drop law becomes a test
- **Requirement:** HLR-106
- **Date:** 2026-10-02
- **What changed:** the prototype's capture-time assertion (every scheduled tick present, none touching) becomes a requirement with a pytest node.
- **Why:** commission: "The no-drop law (every scheduled tick present, none touching) becomes a test."
- **Evidence:** `capture_round5.py` assertions at lines 75–83 (prototype).

### LED-2026-10-02-batch-01.7 — the selection echo
- **Requirement:** HLR-107
- **Date:** 2026-10-02
- **What changed:** new: the day row brackets the selection with exact dates; the month row marks the project's `◆`.
- **Why:** AX-2 = "AX-1 plus an echo of the selection" (round 5 verdict).
- **Evidence:** `out/AX-2-118x30.txt` row 3: `24 ⟦━━━⟧ Sep 28`.

### LED-2026-10-02-batch-01.8 — the colour budget on the kanban and the gantt
- **Requirement:** HLR-108
- **Date:** 2026-10-02
- **What changed:** before, the accent branded titles, the critical chain, a horizon group, the matrix percent, the link token and the ≤7-day due token; now, on these two views, it marks the focus role and today only.
- **Why:** round 7: "the accent (#2dd4bf) is overloaded (selection, critical path, variables, chips, keys)"; `BUDGET`: accent = focus only, critical = structure. Scope D10 (kanban + gantt); today kept D4.
- **Evidence:** P-4 accent census.

### LED-2026-10-02-batch-01.9 — README and RUN.md rewrite
- **Requirement:** HLR-109
- **Date:** 2026-10-02
- **What changed:** new requirement: the two docs are checked against the code.
- **Why:** operator's standing request 2026-09-30; `README-AUDIT.md` (33 findings, P0 privacy ×3).
- **Evidence:** P-5, P-6.

### LED-2026-10-02-batch-01.10 — P2 fold into HLR-101 (Q-6, Q-8, Q-12, Q-20)
- **Requirement:** HLR-101
- **Date:** 2026-10-02
- **What changed:** every visible project keeps a span row (clipped or empty, not only those crossing the window); an unparsable date counts as absent; the AT drives the app (painted panel) and AT-109 drives `v`, `F`, `/`.
- **Why:** qa-reviewer Q-6 (a past or undated project would vanish), Q-8 (C-10a non-default inputs), Q-12 (ATs through the shipped surface), Q-20.
- **Evidence:** `02-review.md` Q-6, Q-8, Q-12, Q-20.

### LED-2026-10-02-batch-01.11 — P2 fold into HLR-102 (Q-4, Q-5, UX-2)
- **Requirement:** HLR-102
- **Date:** 2026-10-02
- **What changed:** narrow label form (`N`, no `✓n` below 26 cells) and the frames' literal strings; skip-and-continue fold order stated, with a synthetic board.
- **Why:** the 80×24 verdict frame shows `▸ Mobile App      5`; the prototype's `if n and n <= left` skips and continues.
- **Evidence:** `02-review.md` Q-4, Q-5, UX-2.

### LED-2026-10-02-batch-01.12 — P2 fold into HLR-103 (Q-13, Q-22)
- **Requirement:** HLR-103
- **Date:** 2026-10-02
- **What changed:** the chip's date stated as output (`Oct 6`) not as a `strftime` pattern; "late" defined; a task without a start is never `over`.
- **Why:** `%-d` raises `ValueError` on Windows (Q-13, probed); `ta2`/`tw4` have no start (Q-22).
- **Evidence:** `02-review.md` Q-13, Q-22.

### LED-2026-10-02-batch-01.13 — P2 fold into HLR-104 (Q-2, Q-3, Q-7, UX-1, UX-8, UX-9, UX-10)
- **Requirement:** HLR-104
- **Date:** 2026-10-02
- **What changed:** the selection repair on entry and after a change makes it rest work (LLR-101.9, `app.py`); painted-screen + scroll assertions; span-overflow run of groups; page-aligned window for a tall group; end-of-list no-op instead of "wrap".
- **Why:** both reviewers' blocker — a done selection strands the cursor once nav holds open work only (P-9).
- **Evidence:** `02-review.md` Q-2, UX-1 (blockers), Q-3, Q-7, UX-8, UX-9, UX-10.

### LED-2026-10-02-batch-01.14 — P2 fold into HLR-105 (UX-4, Q-17, Q-18)
- **Requirement:** HLR-105
- **Date:** 2026-10-02
- **What changed:** the day row's label column (cadence · scale) is part of the ruler; `daily` moved to the LLR; the vertical split stated (LLR-101.10).
- **Why:** with the axis gone the label is the only place the scale is named (UX-4).
- **Evidence:** `02-review.md` UX-4, Q-17, Q-18.

### LED-2026-10-02-batch-01.15 — P2 fold into HLR-106 (Q-1, UX-3, Q-14)
- **Requirement:** HLR-106
- **Date:** 2026-10-02
- **What changed:** a tick overlapping the echo zone (± 1 cell) may yield; with no selection every tick is drawn; the sweep asserts every scale is reached and each arm checks ticks.
- **Why:** both reviewers' blocker — the verdict frames themselves drop Sep 21 / Oct 5 under the echo; the prototype's own check exempts the echo zone (`capture_round5.py:66-77`).
- **Evidence:** `02-review.md` Q-1 (blocker), UX-3, Q-14.

### LED-2026-10-02-batch-01.16 — P2 fold into HLR-107 (Q-16, Q-23, UX-4, UX-13)
- **Requirement:** HLR-107
- **Date:** 2026-10-02
- **What changed:** the label-column fallback and the no-selection `today …` label stated; the AT drives `tw3` then `tm4` explicitly and asserts the old bracket is gone; the same-month shortening applies to the joined form only.
- **Why:** Q-23 (the drive was undetermined), Q-16, UX-4, UX-13.
- **Evidence:** `02-review.md` Q-16, Q-23, UX-4, UX-13.

### LED-2026-10-02-batch-01.17 — P2 fold into HLR-108 (UX-6, UX-7, UX-11, UX-12, Q-9, Q-19)
- **Requirement:** HLR-108
- **Date:** 2026-10-02
- **What changed:** "the accent means focus" restated as what ships — the filter field and today's marks; the selection stays reverse; the keybar is outside; the header count is `chain N` (the frame), not `━ chain N`; "This week" takes `hd`; the census covers a URL card, every presentation × group (asserted reached), a non-vacuity arm and the shared tokens' other views.
- **Why:** UX-7 (the selection is reverse, not accent), UX-6 (the keybar), UX-11a and Q-19 (invented `━` in the header), UX-12 (D11), Q-9 (C-31 input set).
- **Evidence:** `02-review.md` UX-6, UX-7, UX-11, UX-12, Q-9, Q-19.

### LED-2026-10-02-batch-01.18 — P2 fold into HLR-109 (S-4, Q-21)
- **Requirement:** HLR-109
- **Date:** 2026-10-02
- **What changed:** the three literal strings become one home-path pattern with explicit placeholders allowed.
- **Why:** the literal list missed forward-slash, WSL, JSON-escaped and other-drive forms and over-matched the `<you>` placeholder.
- **Evidence:** `02-review.md` S-4, Q-21.

### LED-2026-10-02-batch-01.19 — P2 iteration 2 fold into HLR-104 (UX-15)
- **Requirement:** HLR-104
- **Date:** 2026-10-02
- **What changed:** the selection repair moves to the done task's neighbour in its group's draw order (after, else before), not to the group's first task; AT-108 gains the overshoot arm (one more `]`).
- **Why:** ux-reviewer UX-15 — repairing to the group's top made an extra `]` (or key repeat) advance a task up to four rows away with no visible cue.
- **Evidence:** `02-review.md` §Iteration 2, UX-15.

### LED-2026-10-02-batch-01.20 — P2 iteration 2 fold into HLR-101 (qa N-1, N-2, N-3)
- **Requirement:** HLR-101
- **Date:** 2026-10-02
- **What changed:** AT-109's fixture and expected values pinned (archived `tw7` → `✓1`→`✓2`; focus window Sep 25–Oct 16; filter nav and ruler rows 3–4); height 0 = unbounded only, heights 1–3 defined; the filtered row offset stated in the IFC.
- **Why:** the `v` arm could not fail on a board with no archived task; the F and / arms had no expected values; `height 0` vs `height − 3` conflicted.
- **Evidence:** `02-review.md` §Iteration 2, qa N-1, N-2, N-3.

### LED-2026-10-02-batch-01.21 — P2 iteration 2 fold into HLR-104 (qa N-4)
- **Requirement:** HLR-104
- **Date:** 2026-10-02
- **What changed:** the overflow run of groups is page-aligned (`index // (body − 2)`), like the task page; in overflow only the selected task's row is drawn under its span.
- **Why:** many runs hold the selected group; the expected rows were not determined.
- **Evidence:** `02-review.md` §Iteration 2, qa N-4.

### LED-2026-10-02-batch-01.22 — P3 code-review fold into LLR-101.1 (F6)
- **Requirement:** LLR-101.1
- **Date:** 2026-10-02
- **What changed:** Before: "at `k = 7` the start moves back to its Monday". After: "…and, when that shift would put `hi` past the field's last cell, to `lo`'s Monday instead".
- **Why:** code-reviewer F6: the Monday shift could hide the latest due behind `▸` although `need ≤ field_w × 7` (110 (w, need) pairs measured).
- **Evidence:** `evidence/inc001-review-red.txt` (`test_TC_101_a_week_window_keeps_its_latest_due_inside` RED on the frozen snapshot).

### LED-2026-10-02-batch-01.23 — P3 code-review fold into LLR-101.6 (F1, F2)
- **Requirement:** LLR-101.6
- **Date:** 2026-10-02
- **What changed:** Before: the page of groups applied "when the span rows alone exceed the body". After: when they fill it — more groups than rows, or exactly as many while an open task is selected; bodies of one and two rows defined; a selected rest-work task in a group with no room draws no task row.
- **Why:** code-reviewer F1 (HIGH): with groups == body rows the selected task was cut (F-3) or the last span vanished uncounted; F2: bodies under three rows dropped every selection.
- **Evidence:** `evidence/inc001-review-red.txt` (`test_TC_106_every_selection_is_drawn_at_every_height`, `test_TC_106_groups_exactly_filling_the_body_keep_every_span_and_the_selection` RED on the frozen snapshot).

### LED-2026-10-02-batch-01.24 — P3 code-review fold into LLR-101.11 (F4)
- **Requirement:** LLR-101.11
- **Date:** 2026-10-02
- **What changed:** New clause: a label too narrow for its counts sheds `✓n`, then `▲n`, then `N`.
- **Why:** code-reviewer F4: two-digit counts in an 8-cell label made the row one cell too wide (LLR-101.10).
- **Evidence:** `evidence/inc001-review-red.txt` (`test_TC_110_a_narrow_label_sheds_its_counts_before_it_overflows`).

### LED-2026-10-02-batch-01.25 — P3 code-review fold into LLR-102.5 (F3)
- **Requirement:** LLR-102.5
- **Date:** 2026-10-02
- **What changed:** Before: the legend named the gantt's marks "each only while drawn", planned with no selection, no focus and the terminal size. After: it is asked of the frame the screen shows (selection, archive toggle, focus, panel size threaded from the app through `HelpModal`), and names `⟦━⟧` and `◂▸` when that frame draws them.
- **Why:** code-reviewer F3 (HIGH): the legend described a different frame and could not name the echo the requirement listed; TC-116 never asserted it.
- **Evidence:** `evidence/inc001-review-red.txt` (`test_TC_116_the_gantt_legend_reads_the_frame_on_screen`).

### LED-2026-10-02-batch-01.26 — P4 → P3 iterate-to-fix (increment 004) into HLR-101
- **Requirement:** HLR-101
- **Date:** 2026-10-02
- **What changed:** the AT registry: AT-109 (show archived) kept; the focus and filter nodes become AT-110 and AT-111.
- **Why:** qa-reviewer P4 G-001: C-18 wants one AT per on-disk node; AT-109 was realised by four functions (C-21 re-cut).
- **Evidence:** `04-validation.md` (G-001, UX walkthrough); `evidence/inc004-red.txt`.

### LED-2026-10-02-batch-01.27 — P4 → P3 iterate-to-fix (increment 004) into HLR-104
- **Requirement:** HLR-104
- **Date:** 2026-10-02
- **What changed:** the AT registry: AT-108 (entry repair) kept; the finish-and-overshoot node becomes AT-113.
- **Why:** qa-reviewer P4 G-001 (C-18, C-21).
- **Evidence:** `04-validation.md` (G-001, UX walkthrough); `evidence/inc004-red.txt`.

### LED-2026-10-02-batch-01.28 — P4 → P3 iterate-to-fix (increment 004) into HLR-105
- **Requirement:** HLR-105
- **Date:** 2026-10-02
- **What changed:** the AT registry gains AT-112 (the legend under a `/` filter describes the filtered frame), the node added for code review F12.
- **Why:** qa-reviewer P4 G-001: that node had no AT id of its own.
- **Evidence:** `04-validation.md` (G-001, UX walkthrough); `evidence/inc004-red.txt`.

### LED-2026-10-02-batch-01.29 — P4 → P3 iterate-to-fix (increment 004) into LLR-102.5
- **Requirement:** LLR-102.5
- **Date:** 2026-10-02
- **What changed:** Before: the help usage "shall describe the fitted, folded board and the ruler". After: "…each line whole in the help column (44 cells after its bullet)".
- **Why:** ux-reviewer P4 UXV-1 (criterion failed): 7 of 11 help lines were cut mid-word in the 48-cell column; at 80x24 three lines and the example were lost.
- **Evidence:** `04-validation.md` (G-001, UX walkthrough); `evidence/inc004-red.txt`.

### LED-2026-10-02-batch-01.30 — P4 → P3 iterate-to-fix (increment 004) into LLR-101.7
- **Requirement:** LLR-101.7
- **Date:** 2026-10-02
- **What changed:** New clause: the flow packet never covers the `◂` of a reach that began before the window.
- **Why:** ux-reviewer P4 UXV-5: on some ticks the packet hid the clip marker.
- **Evidence:** `04-validation.md` (G-001, UX walkthrough); `evidence/inc004-red.txt`.

### LED-2026-10-02-batch-01.31 — P4 → P3 iterate-to-fix (increment 004) into LLR-101.10
- **Requirement:** LLR-101.10
- **Date:** 2026-10-02
- **What changed:** New clause: the day row's scale label fits its column whole (`.5 d/cell`).
- **Why:** ux-reviewer P4 UXV-6: `Mondays · 0.5 d/ce…` at 80 columns under a focus.
- **Evidence:** `04-validation.md` (G-001, UX walkthrough); `evidence/inc004-red.txt`.
