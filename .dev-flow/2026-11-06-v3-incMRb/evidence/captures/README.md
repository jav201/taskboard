# Inc MR-b captures (E13): real Windows Terminal PNGs of the shipped presentation `R` with milestones on one row

Harness: `scene.py` (scenes below; `dump <scene> WxH` is the headless check) and `shoot.ps1` (MR-a's harness, renamed:
titles `mrb-<scene>-<WxH>-<n>`, each window closed by exact title right after its shot and verified gone; no other window
touched; final assert that no `mrb-*` window remains). Log: `capture-log.txt`.
Board: MR-F (`tests/milestone_row_fixture.py`: 3 projects + Inbox; Pilot rollout holds 5 milestones, m3+m4 on the same day,
m2 late, m1 reached), real app keys (`escape`, `R`, view key, `down`), `Path.home` redirected to a temp folder (`mrb-cap-*`,
removed). Launch: `set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --size C,R --title mrb-...`.

| file (118x30 / 80x24) | scene |
|---|---|
| mrb-v1_* | `R`, view 1: Pilot rollout's milestones on ONE row, `down` once, cursor on `Steering go/no-go`, brief below |
| mrb-v2_* | `R`, `2` (split), `down`: the milestone row, blocks in stop order (milestones first, then tasks) |
| mrb-v3_* | `R`, `3` (all): each project's milestone row (`◆ N ms`) on the shared ruler |
| mrb-hostile_* | view 1, milestone titled `[@click=app.quit]x\`, cursor on it: brief `⟦[@click=app.quit]x\⟧` drawn literally, line width kept |

## Checks
- Each scene ended in its asserted state (`state OK` in the log).
- Width: every rendered line <= the terminal width after each scene (`width_ok=True`, all 8 shots).
- Colour: 124-150 sampled colours per shot via PrintWindow (none black, none < 8).
- Windows: each `mrb-*` window closed by title and verified gone; final assert `no mrb-* window left open`.
- Temp homes `mrb-cap-*` removed (none left).
