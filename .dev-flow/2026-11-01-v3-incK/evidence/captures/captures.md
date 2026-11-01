# Inc K captures (E13): real Windows Terminal PNGs of the shipped capture view (`n`)

App: worktree `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` at head `f931070`, interpreter
`C:/Users/jjgh8/anaconda3/python.exe`, cwd = the worktree; every shot logged
`taskboard.__file__=C:\Users\jjgh8\Github\taskboard-wt\capture-proto\taskboard\__init__.py` (see `capture-log.txt`).
Harness: `scene.py` (synthetic two-board registry + `inbox.json` in a temp home, `Path.home` redirected; keys driven
through `App._press_keys`), `shoot.ps1` (one Windows Terminal window per shot, title `cpi-<scene>-<WxH>-<random>`,
`NO_COLOR` unset, `COLORTERM=truecolor`, WM_CLOSE to the exact title only, verified gone). Distinct colours are counted
over the full PNG; the harness also rejected any grab with < 8 sampled colours (none was rejected). Temp homes removed
(no `cp-cap-*` left in %TEMP%).

| file | size | distinct colours | retries | end-state check |
|---|---|---|---|---|
| k-empty_118x30.png | 1708x928 | 223 | 0 | OK: capture open, pad empty, ghost + hint row drawn |
| k-empty_80x24.png | 1176x760 | 223 | 0 | OK: capture open, pad empty, ghost + hint row drawn |
| k-dividers_118x30.png | 1708x928 | 354 | 0 | OK: cursor note 4, head '4 notes', 3 rules, 0 raw ____ rows; divider notice shown at open, waited out |
| k-dividers_80x24.png | 1176x760 | 289 | 0 | OK: cursor note 4, head '4 notes', 3 rules, 0 raw ____ rows; divider notice shown at open, waited out |
| k-notice_118x30.png | 1708x928 | 291 | 0 | OK: one-time divider notice toast shown, flag stored |
| k-notice_80x24.png | 1176x760 | 261 | 0 | OK: one-time divider notice toast shown, flag stored |
| k-rail_118x30.png | 1708x928 | 355 | 0 | OK: cursor note 4, rail has → / why, no or line (one hit); divider notice shown at open, waited out |
| k-rail_80x24.png | 1176x760 | 289 | 0 | OK: cursor note 4, rail has → / why, no or line (one hit); divider notice shown at open, waited out |
| k-review_118x30.png | 1708x928 | 487 | 0 | OK: review list on top; divider notice shown at open, waited out |
| k-review_80x24.png | 1176x760 | 397 | 0 | OK: review list on top; divider notice shown at open, waited out |
| k-dump_118x30.png | 1708x928 | 388 | 0 | OK: toast 'Dumped →' shown, note 1 gone, head '3 notes'; divider notice shown at open, waited out |
| k-dump_80x24.png | 1176x760 | 307 | 0 | OK: toast 'Dumped →' shown, note 1 gone, head '3 notes'; divider notice shown at open, waited out |
| k-newproject_118x30.png | 1708x928 | 380 | 0 | OK: name field open, value 'Contracts QA', ⇥ board in key row; divider notice shown at open, waited out |
| k-newproject_80x24.png | 1176x760 | 293 | 0 | OK: name field open, value 'Contracts QA', ⇥ board in key row; divider notice shown at open, waited out |
| k-colour_118x30.png | 1708x928 | 335 | 0 | OK: capture open, colour pad loaded verbatim |
| k-colour_80x24.png | 1176x760 | 334 | 0 | OK: capture open, colour pad loaded verbatim |

Notes
- The store carries no `divider_notice` (as the brief gives the data), so on the 4-note pad the one-time divider notice
  opens with the view. In run 1 (superseded; still in `capture-log.txt`) that toast covered the scene's subject (the
  `alt+n` field at 118x30, the dump toast at 80x24). Run 2 checks the notice was shown, waits out its 15 s timeout, then
  presses the scene's keys; the data is unchanged. Observation for the reviewer: on first use the notice sits over the
  new-project field for 15 s.
- `k-rail`: with the brief's data note 4 shares words with one project only (Pilot rollout), so `options()` returns a
  single strong hit and the rail draws no `or` alternatives line; the shot shows the top option, the `why` words and the
  board chips.
- `k-notice`: the head reads `2 notes` with the cursor on the empty line after the divider: `note_count` counts the note
  being started (LLR-4402.8), by design.
- scene.py does not call `super().on_mount()` (incL's did): Textual already runs `TaskboardApp.on_mount`, and the second
  call pushed the boards home twice at this head.

**no cpi-* window left open** (asserted by shoot.ps1 at the end of run 2 over every visible window whose title starts with `cpi-`; the
operator's `JJ_WORKPC: dev-flow` window was still open after the run).
