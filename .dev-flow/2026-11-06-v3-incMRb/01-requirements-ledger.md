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
