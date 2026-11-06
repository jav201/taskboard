# Inc MR captures (E13): real Windows Terminal PNGs of the shipped board gantt milestone row

Harness: `scene.py` (scenes `mri-rest`, `mri-sel`, `mri-hidden`, `mri-hostile`; `dump <scene> WxH` is the headless check) and
`shoot.ps1` (adapted from the Inc X harness: titles `mri-<scene>-<WxH>-<n>`, closed by exact title right after each shot and
verified gone; no other window touched; asserts at the end that no `mri-*` window remains). Log: `capture-log.txt`.
Board: the round's fixture `tests/milestone_row_fixture.py` (MR-F: 3 projects + Inbox; Pilot rollout holds 5 milestones, m3+m4 on
the same day, m2 late, m1 reached), real app keys, `Path.home` redirected to a temp folder (`mri-cap-*`, removed; none left).
Launch: `set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --size C,R --title mri-...`.

| file (118x30 / 80x24) | scene |
|---|---|
| mri-rest_* | board gantt, cursor on `Pilot store list`: one milestone row per project (`◆ 5 milestones ▲1`, `■ ▲1d`, `■2`) |
| mri-sel_* | `↑`, then `→` twice: m5 selected, title in full (`★ Pilot launch`), the others as dates |
| mri-hidden_* | class Review hidden in `#`; from m1, `→` lands on m4: m3 (Review) skipped (end state asserts `sel=tm4`, no `■` on the row) |
| mri-hostile_* | milestone titled `[@click=app.quit]x`, selected: drawn literally (cut with `…` at 80 cols) |

## Checks
- Every scene ended in the asserted state (`state OK` in the log, selected id shown).
- Width: after each scene the app's rendered lines were all <= the terminal width (`width_ok=True`, all 8 shots).
- Colour: all 8 shots 195-232 sampled colours via PrintWindow (none black, none < 8).
- Windows: each `mri-*` window closed by title and verified gone; final assert `no mri-* window left open`.
