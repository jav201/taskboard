# Requirements ledger — taskboard — Batch 2026-10-18-batch-03

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-18-batch-03.1 — the operator's verdict on the polish round (P1)
- **Requirement:** HLR-2001, HLR-2002, HLR-2003, LLR-2001.1, LLR-2002.1, LLR-2003.1
- **Date:** 2026-10-18
- **What changed:** new requirements: the quiet marks' tone (HLR-2001), the hint's middle wording (HLR-2002), the gantt note's fill (HLR-2003). They supersede, in the canon: LLR-1802.1's "the cursor task's note expanded to 3 rows" (superseded by LLR-2003.1: the note takes the free rows, 3 at least); LLR-1803.2's and LLR-1904.1's wording lists (superseded in part by LLR-2002.1: a middle wording between the long and the short one); the `dim` tone of the view word (LLR-1802.1) and of the cut marks (LLR-1801.2, LLR-1802.1), superseded by LLR-2001.1.
- **Why:** the operator's verdict of 2026-10-18 on `prototypes/backlog_polish/backlog-polish-prototype.html`: «Si, apruebo.» — variant A of all three items.
- **Evidence:** P-1..P-6 (`01-requirements.md` §2.7); `evidence/suite-base.txt` on `base_ref`.

### LED-2026-10-18-batch-03.2 — P2 iteration 1 amendments (P1, iterate-to-refine)
- **Requirement:** HLR-2001, LLR-2001.1, LLR-2003.1
- **Date:** 2026-10-18
- **What changed:** Before → After. HLR-2001 / LLR-2001.1: the view word `reached` at every width → wherever the header keeps its tones (`header()` paints a title too wide for its row, `vis(title) + 2 > width`, whole in bold `bright`, as shipped and as the round's fork left it) (QA-1); TC-2001: `no project to present` asserted `dim` on a board with no project, the view word among the kinds the sweep must meet (QA-4). LLR-2003.1 / TC-2003: the note's `min(n, max(3, height - L))` rows only where the frame holds the floor (`height ≥ L + min(n, 3)`), else the shipped `+N more rows not shown` (QA-2); the room-equals-note and one-row-longer boundaries and the overflow asserted by a seen-set (QA-3). §2.7 P-2: `capture.py:63` → `:70` (QA-8). §1.2: the hint's inactive view name out of scope (UX-2); §6.3: the gantt note against the split view recorded (UX-1).
- **Why:** the P2 review of 2026-10-18, iteration 1 (qa-reviewer `iterate-to-refine`: QA-1, QA-2 majors; ux-reviewer `approve` with UX-1, UX-2; architect — see `02-review.md`).
- **Evidence:** the reviewers' returns (`02-review.md` §Findings); the qa-reviewer's probe: the header at 36 → `bold #e6edf7`, at 37 → `#5b6675`; the notes board at 80, `L = 15`, heights 5 and 12 → 0 note rows.

### LED-2026-10-18-batch-03.3 — P2 iteration 1 amendments, the architect lens (P1, iterate-to-refine)
- **Requirement:** HLR-2001, HLR-2002, HLR-2003, LLR-2001.1, LLR-2002.1, LLR-2003.1
- **Date:** 2026-10-18
- **What changed:** Supersessions in the canon, added to LED .1's list (A-1): HLR-1802 ("at most three rows" of the cursor's note, superseded by HLR-2003; "one dim word" for the view, superseded by HLR-2001); HLR-1904 ("the first of its four wordings", superseded in part by HLR-2002: five, the middle one second); LLR-1001.1 ("the cursor'd task's notes expand, capped at 3 lines", superseded by LLR-2003.1, and its PRES-V3 gantt-notes oracle replaced for the notes frames by `PRES-V4-gantt-notes-*`). Correction of LED .1 (A-2): the cut marks' `dim` was LLR-1801.2's alone; LLR-1802.1 set the view word's and the note dot's. HLR-2002: "every other rule of HLR-1904 stands" → "five wordings where HLR-1904 counts four; every other rule of HLR-1904 stands" (A-1). Executed verification of HLR-2002, HLR-2003 and LLR-2002.1: one pytest command per `-k` expression, the regression files in their own command (A-3: pytest kept the last `-k` and filtered every file by it — 0 collected). LLR-2001.1: "the frames' plain text equals `base_ref`'s" → "unchanged by this LLR" (A-4: increment 003 changes the gantt frames' text). A-5 (the note count where the header and briefs alone overflow the frame) is folded by LED .2's `height ≥ L + min(n, 3)` clause.
- **Why:** the P2 review of 2026-10-18, iteration 1, architect lens `iterate-to-refine` (A-1, A-3, A-4, A-5 majors; A-2 minor).
- **Evidence:** the architect's probe: 13,440 frames, an exec'd port equal to `cap_fork("fill")` in plain text and to `contrast_fork(reached)` span for span (0 differ); `pytest --collect-only` → 0 of 48 and 0 of 18 for the old commands.

### LED-2026-10-18-batch-03.4 — the PDR's conditions on the contract (PDR seal)
- **Requirement:** HLR-2001
- **Date:** 2026-10-18
- **What changed:** AT-2001: in the split view at 80×25 "every span over a cut or edge mark … at least one such mark" → `pgdn` pages the cursor's note first and at least one `↑`/`↓` edge mark is required, so the `_present_mark` tone is observed through the app (PDR PC-1: the first page shows no edge mark, so a `dim` `_present_mark` survived AT-2001); the `gantt` and `split` view words also asserted not `#5b6675`.
- **Why:** the PDR of 2026-10-18 (qa lens, executed: M4 survived AT-2001 on a throwaway copy of the design).
- **Evidence:** the PDR record `design/PDR-2026-10-18-batch-03.md` (PC-1).
