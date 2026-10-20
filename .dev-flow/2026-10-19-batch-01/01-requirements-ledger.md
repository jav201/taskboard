# Requirements ledger — taskboard — Batch 2026-10-19-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-19-batch-01.1 — the operator's verdict on the present-portfolio round (P1)
- **Requirement:** HLR-2101, HLR-2102, HLR-2103, HLR-2104, HLR-2105, HLR-2106, LLR-2101.1, LLR-2102.1, LLR-2103.1, LLR-2104.1, LLR-2105.1, LLR-2106.1
- **Date:** 2026-10-19
- **What changed:** new requirements: the milestone row of the presentation (HLR-2101), the project's presentation state on the board (HLR-2102), view 3 (HLR-2103, HLR-2104), its curation keys (HLR-2105), the `u` picker (HLR-2106). They supersede, in the canon: HLR-1803's "the gantt view on 1, the split view on 2, the next view on tab … wrapping" (two views → three, HLR-2104) and "writing nothing but the show_in_present flag" (the presentation also writes the projects' flag and place, HLR-2105); LLR-1803.1's `_view` "an index into PRESENT_VIEWS" (→ `PRESENT_SCREEN_VIEWS`, LLR-2104.1); LLR-1803.2's, LLR-1904.1's and LLR-2002.1's view names and ` · <n> hidden` tail at 36 columns or more (three names; ` · u <n> hidden`, LLR-2104.1) — their wording lists and choice rule otherwise stand.
- **Why:** the operator's verdict of 2026-10-19 on `prototypes/present_portfolio/present-portfolio-prototype.html`: «C: Me parece la mejor opción para mis objetivos.» · «Sí, que persista el orden.» · «Siempre la traigo con (a), pero sería útil tener el seleccionador propuesto con (u)»; the round's finding of the milestone bar; the orchestrator's D1–D8.
- **Evidence:** P-1..P-7 (`01-requirements.md` §2.7, `evidence/premises.txt`); `evidence/suite-base.txt` on `base_ref`.

### LED-2026-10-19-batch-01.2 — the P2/PDR review amendments (P1, iterate-to-refine)
- **Requirement:** HLR-2101, HLR-2102, HLR-2103, HLR-2104, HLR-2105, HLR-2106, LLR-2101.1, LLR-2102.1, LLR-2103.1, LLR-2104.1, LLR-2105.1, LLR-2106.1
- **Date:** 2026-10-19
- **What changed:** Before → After. HLR-2101/LLR-2101.1: the unreachable `◆✓` and off-window arms → a start date, a 1-cell field at 36 columns (no `◆`), no due (`no dates`); AT-2101 names the bar glyphs and finds the column from the project row's `◆` (QA-7). HLR-2102/LLR-2102.1: the flag governs view 3 only; the rank never painted; duplicate, `1.0` and 300-digit ranks in the table; a team pull adds a new project shown and unranked (`team_sync` strips the two keys — security S-3, S-4); AT-2102's keys spelled and its RED file `red-004.txt` (QA-5, QA-10). HLR-2103/LLR-2103.1: the rail's strings exact, its task count over every visible project; the S-2 markup payloads; `escape(fit(...))`; TC-2103's milestone carve-out dropped (the round already drew milestones as the fix does), a reverse-ranked board with a hidden project added, the cursor sweep bounded (QA-1, QA-6, QA-12, QA-13, security S-2). HLR-2104/LLR-2104.1: the view-3 tail one count ` · u N hidden` (was ` · u P project(s) + T task(s) hidden`), the view-3 middle wording `⇥ · ↑↓ · ←→ rail · ␣ hide · ⇧↑↓ order · enter fold · a all · x · esc` and `⇧` throughout, the no-rail wordings spelled (UX-1, QA-3, QA-11); entering view 3 on a hidden project → the first drawn row, leaving it → views 1/2 show the cursor's project (UX-6, A-9); `pgdn`/`pgup` inert in view 3, `enter`/`shift+↑↓` inert in views 1/2 (UX-5, A-11); `_paint` keeps `update(self._frame_text())` (A-7); every `PRESENT_VIEWS[self._view]` site indexes `PRESENT_SCREEN_VIEWS` (A-11); literal first-width tables, not a re-derived formula, and the law-driven set adds AT-1803, AT-1904 and TC-1904's overflow arm (QA-4, A-6); the export-with-the-rail mutation moved to AT-2104 (QA-14). HLR-2105/LLR-2105.1: `space` on the rail toggles in place (UX-2); `a` notifies `Shown again: …` (UX-3); `enter` on a task inert. HLR-2106/LLR-2106.1: the title `Hidden from the presentation`, `u` also closes (UX-7), the rows read from `#picker-rows`, no new census exemption (A-7, security S-5). The increment cut: 003 is `views` only (`render_present_all`, `PRESENT_SCREEN_VIEWS`, `present_hidden_rows`); 004 is `app` + `modals` (every key, the hint, the export, the picker) — so no commit ships view 3 with the views-1/2 `space`/`a` acting in it (A-11) or advertises `u` before it is bound (A-12). Executed verification: `-k "TC_210N or AT_210N"` (A-8). Supersessions in the canon, added to LED .1's list (A-5, QA-2): HLR-1803's "export with x the frame of the view on screen" (view 3 exports its timeline without the rail) and "space, a, ←/→ … acting in either" (two views; in view 3 `space` also hides a project and `←/→` move the focus); LLR-1803.1's "paint and export `render_present(..., PRESENT_VIEWS[self._view])` through `_frame_text`" (view 3 through `render_present_all`); LLR-1803.3's "`_frame_text()` to `present_paths(..., PRESENT_VIEWS[self._view])`" (view 3: the timeline to `present_paths(board, None, today, "all")`); HLR-1602 item 1 "space shall hide the cursor task" (in view 3 also a project); LLR-1903.1's keys inert below 36 columns (now also `3`, `shift+↑↓`, `enter`, `u`); HLR-2002's "the 80-column hint names next and show all" for the split view (three view names: short, or compact with something hidden).
- **Why:** the P2 review and the PDR of 2026-10-19 (architect: P2 iterate-to-refine, A-5..A-7 and A-11 majors; qa-reviewer: P2 iterate-to-refine, QA-1..QA-4 and QA-13 majors; ux-reviewer: approve with conditions, UX-1..UX-3 majors; security-reviewer: approve with conditions, S-2, S-3 medium).
- **Evidence:** the reviewers' returns (`02-review.md` §Findings); the qa probe (the round's renderer over its own board: `23 open · ▲2 past due`, `◆ Cut-over weekend … due Oct 25`); `rich.cells.cell_len` over the view-3 wordings (long 134 / middle 95 / compact 51 cells + 2 with the rail; + 13 with ` · u 3 hidden`).

### LED-2026-10-19-batch-01.3 — P2 iteration 2 (P1)
- **Requirement:** HLR-2103
- **Date:** 2026-10-19
- **What changed:** Before → After. AT-2103's rail rows ` 1 ● Customer Portal` … → `  1 ● Customer Portal` … (the lead cell and a right-aligned two-cell number: two leading blanks on a row that is not the cursor's); the header's right end read right-stripped. §2.5: the fixture hides Security Audit through `Project.extra` at increment 001 and through the field from increment 002 (QA-9).
- **Why:** the P2 review of 2026-10-19, iteration 2 (qa-reviewer QA-6 nit, QA-9).
- **Evidence:** the qa-reviewer's probe of the round's renderer at 160×45 (`  1 ● Customer Portal`; the header ends `past due `).

### LED-2026-10-19-batch-01.4 — the sweep as it runs; the drawn stops (P3, increments 003 and 004)
- **Requirement:** LLR-2103.1
- **Date:** 2026-10-19
- **What changed:** Before → After. TC-2103's sweep "heights 10, 24, 30, 45" → "heights 10 and 45" (a cut, overflowing frame and a roomy one; the folds × rail-focus product bounded to the unfocused timeline — qa-reviewer QA-12: the four heights took 89 s of the suite); the threshold gains "every stop a row the frame draws (none under the overflow row) and the drawn cursor one of them" (code review F1 of increment 003: the stops included rows the overflow row covers; fixed in increment 004 with `TC-2103`'s overflow-row node).
- **Why:** increment 003's code review, F1 and F2 (MEDIUM).
- **Evidence:** packet 003 §4b; `tests/test_present_all.py::test_TC_2103_no_stop_hides_under_the_overflow_row` (RED without the increment-004 trim, GREEN with it — packet 004).

### LED-2026-10-19-batch-01.5 — the picker's backdrop and first row (P3, increments 005 and 006)
- **Requirement:** LLR-2106.1
- **Date:** 2026-10-20
- **What changed:** Before → After. "a cursor row, and the keys line `↑↓ move · ␣ toggle · esc close`" → "a cursor row that opens on the first hidden row, and the keys line `↑↓ move · ␣ show/hide · ○ hidden · esc close`, over the app's shared modal backdrop (`taskboard.tcss`, the presentation dimmed behind it)".
- **Why:** the coordinator's follow-up of 2026-10-20 (the capture `seq-160x45-4-picker` showed the picker over a blank screen); the P4 ux walkthrough UX4-1 (major: in view 3 `u` then `space` hid a shown project listed as a heading) and UX4-2; the code review of increment 005 (F1: the shared rule, not an inline colour).
- **Evidence:** `evidence/red-005.txt`, `evidence/red-006.txt`; packets 005 and 006; `evidence/captures/seq-160x45-4-picker.svg`.
