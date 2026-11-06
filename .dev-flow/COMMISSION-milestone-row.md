# Commission — a project's milestones share one gantt row

The orchestrator wrote this on 2026-11-06. Branch: `feat/milestone-row`, on the round `prototypes/milestone_row/` (`57517bf`) and `main` `222403e`.

**Process.** dev-flow-v3-beta, as ONE increment in `.dev-flow/2026-11-06-v3-incMR/`. The orchestrator runs every stage.

**Models, at the operator's order** («usa deepseek para la implementación, tú planeas y orquestas»):
- DeepSeek v4 Pro implements E4 and runs the mutants, through `pi`.
- Opus designs (E1–E3), writes the tests as the independent tester, and reviews.

## The operator's verdict (verbatim)

```
Variante: A    (one dedicated milestone row per project, under its span row)
D1: si         (the presentation `R` follows the board's gantt: its milestones share one row too)
D2: fila       (Inbox milestones go on the Inbox group's own milestone row)
D3: si         (`/` search and hidden-class filtering still reach individual milestones on the row)
notes: (none)
```

The round's design facts are the spec. Read `prototypes/milestone_row/` (`BRIEF.md`, the variant A scenes, the captures):
- Marks sit at their dates with their class glyph and colour. A same-day clash is drawn as `◆N`.
- The selected milestone shows its full title. The others show their date when it fits.
- Late milestones carry `▲Nd`. Reached milestones are hollow plus `✓`.
- `↑↓` stop on the row once, at the next open milestone. `←→` walk its milestones by date, same-day ones included. `enter` opens the details. Today `←→` (`hmove`) does nothing in the gantt, because it has a single column.
- Normal tasks stay one per row, done rows at the tail as since `f4b53cc`.

## Decisions

- **MR-1.** Variant A on the board's gantt AND in the presentation's gantt-based views (D1). Check views 1 and 3, and say which views draw milestones.
- **MR-2.** The link mode (`L`) and the paged fold were not captured in the round. E1 must state their behaviour with the shared row: a milestone that is a link endpoint, and a fold of the row.
- **MR-3. Size cap:** about 40 LLRs and about 25 prototype nodes. If the increment needs more, split it into "board gantt" and "presentation".
- **Standing rules:**
  - the law guards run in E5;
  - real Windows Terminal captures at 118x30 and 80x24, in windows titled `mri-…`, each closed by title; never close another window;
  - no line wider than the terminal;
  - `env -u NO_COLOR`;
  - the full suite runs once at the batch end;
  - push only on approval, and check CI after it.
