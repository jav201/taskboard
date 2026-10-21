# Real-app captures — batch 2026-10-21-batch-01 (PDR condition PC-1)

The SHIPPED `TaskboardApp` at `d1033b0` (increment 005's commit), unpatched, in real Windows
Terminal windows (truecolor, `NO_COLOR` cleared), at 118x30 and 80x24, by `shoot_real.ps1` /
`shoot_real.py` over the round's synthetic boards and people (`tests/people_round_fixture.py`,
calendar Tuesday 2026-10-20). Every window had a unique `p01-*` title, was closed right after its
shot and verified gone; the run ended with `no p01-* window left open` (`png/capture-log.txt`).
Every shot passed the colour check (>= 8 sampled colours, none black) on its first try. `mt-flip` was added at the DDR (UX-DDR-2) and shot in a second run.

| Item | Scene | What it shows | PNGs |
|---|---|---|---|
| 1 people view (A + C's quote + B's box — the composed frame the operator reviews) | `pv` | `@`: the two panes, Ana Ruiz selected, the `1 late · 1 today · 5 open` box, each task with its mentioning note line | `png/pv_118x30.png`, `png/pv_80x24.png` |
| 1 — **named for your verdict (UX-9, D-3)** | `pv` | the box reads `N late · N today · N open` — B's rendered order, most urgent first — while the objection said «late · open · today»; say so if the spoken order is wanted | `png/pv_118x30.png` |
| 1 | `pv-tasks` | the tasks pane focused, cursor on the second task | `png/pv-tasks_118x30.png`, `png/pv-tasks_80x24.png` |
| 1 | `pv-marta` | `↵` on the people pane: Marta Gil's tasks | `png/pv-marta_118x30.png`, `png/pv-marta_80x24.png` |
| 1 | `pv-open` | `↵` on a task: opened on its board | `png/pv-open_118x30.png`, `png/pv-open_80x24.png` |
| 1 | `pv-edit` | `e`: `PersonForm` editing a person | `png/pv-edit_118x30.png`, `png/pv-edit_80x24.png` |
| D4 | `d4-view9` | view `9` keeps the team `People`, apart from `PEOPLE · directory` | `png/d4-view9_118x30.png`, `png/d4-view9_80x24.png` |
| 2 picker | `mt-list` | `@an` in the editor's notes: the dropdown under the cursor | `png/mt-list_*.png` |
| 2 | `mt-add` | `@Sofia` + `↵`: add a person, the role asked inline | `png/mt-add_*.png` |
| 2 | `mt-flip` | the notes reached by `⇥`, the cursor six lines down: the list opens ABOVE the cursor, inside the screen (ux UX-3, UX-DDR-2) | `png/mt-flip_*.png` |
| 2 | `mt-done` | the mention inserted, typing continues | `png/mt-done_*.png` |
| 3 search | `sr-list` | kanban `/` then `@an`: `PEOPLE · names only` | `png/sr-list_*.png` |
| 3 | `sr-res` | `↵`: the kanban filtered to that person, the bar naming them | `png/sr-res_*.png` |
| 4 look | `m-det` | a mention drawn `@Name` in pink in the details | `png/m-det_*.png` |
| 4 | `m-kb` | the same in the kanban card | `png/m-kb_*.png` |
| 4 | `m-pr` | the same in the presentation (split view) | `png/m-pr_*.png` |
