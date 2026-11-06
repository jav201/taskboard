# Prototype brief: a project's milestones share one gantt row

Written by the orchestrator on 2026-11-06. Branch `proto/milestone-row`, from `main` `222403e`.

## The operator's words (verbatim)

> «Necesito un cambio más, los milestones ocupan cada uno una línea en el gantt... esto gasta mucho espacio. Necesito que queden en una sola línea en el gantt.»

They then picked "prototype first", after this proposal:
- all of a project's milestones on one row, each at its date with its class mark;
- a same-day clash drawn as `◆2`;
- the selected milestone shows its full title, the others their date when it fits;
- `↑↓` reaches the row, `←→` jumps between its milestones, `enter` opens one;
- normal tasks unchanged, and the presentation unchanged.

## Today (read the code)

`views.gantt_plan` (`taskboard/views.py`, around line 2433) gives each milestone its own drawn row. A reached milestone is placed among its group's rows by date (D-606), and done rows sit at the tail since `f4b53cc`. `task_row` draws a milestone as a mark on its date, using the class glyph and colour from `milestone_mark` (marks batch `2026-10-24-batch-01`), plus a chip (`▲Nd` late, `✓` reached).

`nav_model` (around line 8314) walks `g.rows`. `←`/`→` are `hmove(±1)` in `keymap.py:191`. Find what `hmove` does in the gantt view: whether it moves the time window or the cursor. The new milestone row must not break it.

## Variants (real-app renders, 118x30 and 80x24, current state + 3 variants)

Use a synthetic board: 3 projects, one with 5 milestones spread over two weeks (two of them on the same day, one late, one reached), and the others with 1–2 milestones and normal tasks.

- **A. A dedicated milestone row per project**, right under the project's span row, holding every milestone of that project. This is the proposal.
- **B. The milestones drawn ON the project's span row itself**, which needs zero extra rows. Show how the marks coexist with the span bar and the project's own due `◆`.
- **C. One milestone row for the whole gantt**, under the ruler, with every project's milestones in their class or project colours. A board-wide "milestone lane".

For each variant, show:
- the label strategy at both widths: the selected milestone's full title, the others' date or nothing, and the clash `◆2`;
- how the cursor selects one milestone (`←→` on the row, or another way if `hmove` already means something), and the details or `enter` on it;
- the late and reached states (`▲Nd`, hollow plus `✓`, from the marks design);
- the space saved: count the rows before and after on the synthetic board.

Decisions to put on the page, each with its consequences:
- **D1.** Does the presentation (`R`) follow the board's gantt?
- **D2.** Where does a milestone with no project (Inbox) go?
- **D3.** Does `/` search, or the filtering of a hidden class, still reach individual milestones on the shared row?

## Rules

- **Skills.** Follow the tui-design skill (`C:\Users\jjgh8\.claude\skills\tui-design\SKILL.md` + `PROTOTYPE.md`) for the round, and html-visualizer, genre A, for the page.
- **Model rounds.** Use `prototypes/milestone_marks/` and `prototypes/critical_chain/` as the model: their scenes, the real Windows Terminal capture harness, and the verdict page.
- **Captures.** Every variant gets a real full-colour Windows Terminal PNG at 118x30 and 80x24, embedded in the page.
  - Launch with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <unique mr-…> ...'`.
  - Close each window by title right after its shot, and verify it is gone.
  - At the end, assert that no `mr-*` window remains. NEVER close any other window (`JJ_WORKPC: dev-flow`).
  - Reject black shots, shots with fewer than 8 colours, and shots in the wrong end state.
- **Layout.** Check every capture for a wrapped or overflowing line. The operator saw date text wrap in the last round. No rendered line may exceed the terminal width.
- **Page.** `prototypes/milestone_row/milestone-row.html`.
  - Spanish prose, English UI strings, BLUF at the top.
  - Per variant: the captures, the consequence in plain Spanish, the rows saved, and a recommendation.
  - D1–D3, each with an objection field.
  - «Elijo esta» plus an objection field per item.
  - A GENERAL NOTES field.
  - «Exportar respuestas», which copies text and JSON.
  - 0 console errors. Then open the page with `Start-Process`.
- **Data and code.** Synthetic data only, and never the operator's real name. Nothing under `taskboard/` changes: the prototype wraps or forks the app inside `prototypes/milestone_row/`.
- **Tests.** Run them with `env -u NO_COLOR`. No full suite.
