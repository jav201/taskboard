# Requirements ledger — taskboard — Inc MR-b, the presentation's milestones share one row

> Append-only. Every entry names the requirements it amends one by one (V26: no ranges).

### LED-2026-11-06-incMRb.1 — D1 and R-2 made strict, reusing MR-a's row
- **Requirement:** HLR-4651
- **Requirement:** HLR-4652
- **Requirement:** HLR-4653
- **Date:** 2026-11-06
- **What changed:** D1 ("`R` follows the board's gantt") and R-2 (`↑↓` stops at each milestone, and no key changes) were split into 22 single-`shall` LLRs. The row's field and label text are not restated: they are MR-a's (LLR-4602.1–4602.8, LLR-4603.1–4603.8, LLR-4603.11), carried into `R` by cell equality (LLR-4652.1) and by citation (LLR-4652.3–4652.6). Added for `R`:
  - The drawn set stays `R`'s at base, with no reached milestones (LLR-4651.3).
  - View 3's head row is the anchor of its row, in place of a span row (LLR-4651.2), and the view's overflow budget is covered (LLR-4651.7).
  - `_present_field` learns MR-a's reversed and covered cells (LLR-4652.2).
  - The present label column gets a `⟦` lead and a `▎` hue bar (LLR-4652.3, LLR-4652.4).
  - The cursor walks one stop order (milestones in walk order, then tasks) in every view. The briefs and blocks follow that order (LLR-4653.1, LLR-4653.2, LLR-4653.5), and so does the cursor's fallback (LLR-4653.3).
  - `space` hides one milestone (LLR-4653.4).
  - The key set is pinned (LLR-4653.6).
  - The header, the ruler, the strip and the hint row are pinned to base (LLR-4652.8).
- **Why:** under R-2 the cursor still names one milestone, but the field now draws the milestones on one row ahead of the tasks. With base order kept (milestones among the tasks, by due), `↓` would bounce between the milestone row and the task rows, and the view-1 briefs would no longer read top to bottom with the field. One stop order fixes both. The order lives in a new helper, so `present_tasks_m` keeps its order and nothing the deck reads changes.
- **Evidence:**
  - `taskboard/views.py:6949-6968` (`present_tasks`, `present_tasks_m`)
  - `views.py:7019-7031` (`_present_field`: no `rev:` tone)
  - `views.py:7475-7495` (`_present_task_row` for a milestone)
  - `views.py:7566-7645` (`render_present`: field loop, briefs, blocks)
  - `views.py:7714` (`_all_plan`)
  - `views.py:7806-7836` (`_all_layout`)
  - `views.py:2896-3020` (MR-a's `gantt_milestone_row`, `gantt_lane_label`)
  - `views.py:2490` (`walk_key`, nested)
  - `taskboard/app.py:399-403` (`_shown_ids`), `app.py:423-456` (`move`, `side`)
  - `taskboard/keymap.py:240-262` (`PRESENT_KEYS`)

### LED-2026-11-06-incMRb.2 — the `x` deck is stated unaffected
- **Requirement:** HLR-4654
- **Requirement:** LLR-4654.1
- **Date:** 2026-11-06
- **What changed:** the scope's option "the deck follows what `R` draws, or state that it is unaffected" is resolved as **unaffected**. A byte-equality oracle against base pins it.
- **Why:** MR-b changes layout and cursor order only, never which tasks are shown. The deck draws its own HTML layout from `present_deck_boards`, which reads `present_tasks_m(...)[1]` in board order (`views.py:7671`), and that order is left unchanged. A row layout has no meaning in the HTML deck.
- **Evidence:** `views.py:7647-7680` (`present_deck_boards`); Inc X LLR-4501.3/LLR-4501.4 (the deck is `H` → `c`'s bytes).

### LED-2026-11-06-incMRb.3 — E3 round 1, RB-2 with SEC-B1 and SEC-B2: the view-1 brief prints a title literally
- **Requirement:** LLR-4652.9
- **Requirement:** HLR-4652
- **Date:** 2026-11-06
- **What changed:** LLR-4652.9 is added (Unwanted). `_present_brief` joins the slice as unit 10. Of RB-2's two fixes, only `_literal` is taken; the measure-only fix is rejected, and the LLR's second NC pins that choice. The threshold is measured on the rendered frame, after `to_text`.
- **Why:** SEC-B1 shows that `collapse_runs` merges the title run with the same-style `⟧`, so `escape`'s trailing `\` prints twice. Measuring the line would only pad it: the audience would still read `x\`. SEC-B2 shows that a test measuring with `_strip` passes on base, so its RED would be vacuous.
- **Evidence:** `views.py:7534-7545` (`_present_brief`); `views.py:290-312` (`_literal`); `03-pdr-security.md` SEC-B1, SEC-B2 (P-a: 119 / 81 cells).

### LED-2026-11-06-incMRb.4 — E3 round 1, SEC-B3: the view-2 block heading keeps a backslash before `[`
- **Requirement:** LLR-4652.10
- **Requirement:** AT-4655
- **Date:** 2026-11-06
- **What changed:** LLR-4652.10 is added (Unwanted), with an NC that is RED on base. `_present_heading` joins the slice as unit 11, with the same `_literal` swap. AT-4655 adds the titles `x\` and `a\[b]` and view 2, and it measures the rendered frame.
- **Why:** `escape(clip(task.title, tw))` drops the `\` before a non-tag `[`, so the room reads a title that differs from the board. The architect's A-6 says to leave `views.py:7402` alone, because it is width-true. The orchestrator's ruling takes SEC-B3 into the slice instead: the defect is in the text, not the width.
- **Evidence:** `views.py:7388-7403` (`_present_heading`); `03-pdr-security.md` SEC-B3; `03-pdr-architect.md` A-6.

### LED-2026-11-06-incMRb.5 — E3 round 1, RB-3: the R-7 cut at every width
- **Requirement:** LLR-4652.4
- **Requirement:** AT-4651
- **Date:** 2026-11-06
- **What changed:** the 80-column label literals take the cut form: ` ⟦▎ ▲ Store li… 2/2` and ` ⟦▎ ■ Rubric sign-…`. The 118-column forms stay. LLR-4652.4's threshold now has 4 cases (4/4).
- **Why:** E2-F2. `gantt_lane_label` at `label_w - 3` (17 cells at 80) cuts by cell width with `…`, so the uncut literals could not pass on a correct row.
- **Evidence:** `baseline-notes.md` P-6; `graph-proto-V.cw.md` `_present_lane_row` (TC-4914).

### LED-2026-11-06-incMRb.6 — E3 round 1, RB-4: AT-4653's fold clause
- **Requirement:** AT-4653
- **Date:** 2026-11-06
- **What changed:** "At 80x24 the overflow folds fewer projects than at base" becomes "At 118x18 (room 15, need 15) the overflow folds no project, where base folds 2".
- **Why:** E2-F3. At 80x24, base folds no project of MR-F, so "fewer" had no passing outcome. At 118x18 the fitted frame shows the fold that exists, which is also LLR-4651.7's case.
- **Evidence:** `baseline-notes.md` P-4; `graph-proto-V.cw.md` `_all_layout` (TC-4907); `03-pdr-architect.md` A-7.

### LED-2026-11-06-incMRb.7 — E3 round 1, RB-5: the milestone row's gutter is blank
- **Requirement:** LLR-4651.8
- **Requirement:** AT-4651
- **Date:** 2026-11-06
- **What changed:** LLR-4651.8 is added (Ubiquitous) and carries MR-a's LLR-4601.8 into `R`. AT-4651 checks the blank gutter.
- **Why:** E2-F4. The design drew MR-a's blank, but no MR-b requirement or test pinned it. RB-5 allows either a citation or an LLR. The LLR is chosen because a citation alone gives `R` no test (A-7 preferred the citation).
- **Evidence:** `views.py:7490-7491` (base: `gantt_dep_mark` on each milestone's own row); `../2026-11-06-v3-incMR/01-requirements.md` LLR-4601.8.

### LED-2026-11-06-incMRb.8 — E3 round 1, RB-6 with A-1: the deck's negative control can fail
- **Requirement:** HLR-4654
- **Requirement:** LLR-4654.1
- **Date:** 2026-11-06
- **What changed:** the NC is now a mutant of WHICH tasks the deck holds. `present_deck_boards` takes `present_stop_order(present_tasks_m(board, p.id)[0])` in place of `present_tasks_m(board, p.id)[1]`, so `tm1` drops and the sha256 differs from the `8ca174c` oracle. E2-F7's extra-fixture remedy is dropped.
- **Why:** A-1. `present_deck_boards` re-sorts the tasks it holds by board position (`views.py:7675`), so a mutant of the order alone is undone and could never turn RED.
- **Evidence:** `views.py:7647-7680`; `03-pdr-architect.md` A-1.

### LED-2026-11-06-incMRb.9 — E3 round 1, A-2: `_present_task_row` loses its milestone branch
- **Requirement:** LLR-4651.1
- **Requirement:** LLR-4651.4
- **Date:** 2026-11-06
- **What changed:** `_present_task_row` joins the slice as unit 12. Its `if task.milestone:` branch is removed. The slice now holds 12 units in 2 files. No statement changes: the LLRs that map the unit already require one milestone row and one row per non-milestone.
- **Why:** after MR-b, both callers pass only non-milestones, so the branch is dead code. A test that called it directly would test an entry point that no product route calls (E4's partial rule), and `R` would hold two ways to draw a milestone, which could drift apart.
- **Evidence:** `views.py:7475-7490`; callers `views.py:7617`, `views.py:7894`; `tests/test_milestone_marks.py:153`.

### LED-2026-11-06-incMRb.10 — E4 integration, ruling J-2: LLR-4652.10's negative control is `\[x`
- **Requirement:** LLR-4652.10
- **Date:** 2026-11-06
- **What changed:** the negative-control example is `\[x` (base draws `▌ [x`). The "RED on base" claim for `a\[b]` is withdrawn: base already draws `a\[b]`. `a\[b]` stays in the threshold as a positive case. The 6/6 count does not change.
- **Why:** E4 tester finding F-1. On `8ca174c`, rich's `escape` already escapes the tag-shaped `[b]`, so `a\[b]` could not be the RED regression. The base defect is a backslash before a `[` that does not open a tag.
- **Evidence:** `e4-tests.md` §7 F-1; `TC-4920[a\[b]]` passes on base and `TC-4920[\[x]` is RED on base (`evidence/red-base.txt`); GREEN on MR-b (`evidence/green-2.txt`).

### LED-2026-11-06-incMRb.11 — E5 code review F1: LLR-4652.9's negative control is `\[x`, and the threshold is 8/8
- **Requirement:** LLR-4652.9
- **Date:** 2026-11-06
- **What changed:** `\[x` joins the threshold as a RED-on-base title (base draws `⟦[x`). The "RED on base" claim for `a\[b]` is withdrawn: base already draws `⟦a\[b]⟧`. `a\[b]` stays as a positive case. The threshold becomes 4 titles × 2 sizes, 8/8. NC 1 names the titles it turns RED: `\`, `x\` and `\[x`. The claim for `\` and `x\` (119 / 81 cells, reading `\\`) holds and is unchanged.
- **Why:** E5 code review F1 (MEDIUM, `design-gap`). The probe on `8ca174c` confirmed the trailing-backslash defect and refuted the `a\[b]` half, which is the same mistake LED-2026-11-06-incMRb.10 corrected in LLR-4652.10. TC-4919 already ran the 4 titles, but the requirement still said 3 titles, 6/6. The requirement now matches its test. No code and no test changed.
- **Evidence:** `05-review-code.md` F1; `tests/test_present_milestone_row.py` (`BRIEF_TITLES`, TC-4919); `evidence/red-base.txt` (TC-4919 RED on base for `\`, `x\`, `\[x`); `evidence/green-3.txt` (GREEN).
