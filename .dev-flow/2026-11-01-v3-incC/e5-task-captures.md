# E13 captures — Inc C (mechanical task)

Real Windows Terminal PNGs of the SHIPPED app (not the prototype) for: the editor with a pen on, the colour
palette, coloured notes in the details screen, coloured notes in the presentation — each at 118x30 and 80x24 —
plus the HTML workspace report with coloured notes (one browser PNG). Worktree:
`C:/Users/jjgh8/Github/taskboard-wt/capture-proto`. Interpreter `C:/Users/jjgh8/anaconda3/python.exe`.
Never edit `taskboard/` or `tests/`. Write everything under `.dev-flow/2026-11-01-v3-incC/evidence/captures/`.

## Model to copy
`prototypes/capture_round/shoot.ps1` (window per scene, unique title, READY file, WM_CLOSE by title, verify
gone, reject black / < 8 colours, retry ≤ 3) and the scene runner pattern in `prototypes/capture_round/proto.py`
(class `Proto(TaskboardApp)`: builds a synthetic board in a temp home, `_play()` presses keys with
`self._press_keys([...])`, writes READY, sets the title from an env var). Copy and cut them down; do not import
from `prototypes/`.

## Scenes (`scene.py <name>`), synthetic board only, owner `username_subject`
Notes of the task used everywhere (exact):
```
Sync notes
::b:: ask the vendor for the store list ::
::r:: blocker: 12 questions lack a key ::
::g:: done: rubric draft :: and ::o:: later: cost per query ::
::v:: idea: judge with two models :: — ==legacy yellow== still works
```
- `ed-pen`: open the task editor on that task, focus the notes, move to the end, press `alt+5`, type `new blue words` (pen still on, chip shows `blue`).
- `palette`: editor, notes cursor on the word `later`, press `alt+c` (palette open over it).
- `details`: the TaskDetails screen for the task (find the key the app binds; see `taskboard/keymap.py`).
- `present`: the presentation view showing that task's notes (find the key / route the app uses; `tests/test_present_note_highlights.py` shows how notes reach the presentation).
Drive keys through the app (`_press_keys` / the same path the pilot uses). Pens must be pressed as `alt+5`.

## Window rules (load-bearing)
- Launch: `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <title> ...'` with a UNIQUE
  title `cpi-<scene>-<WxH>-<random>`; the app re-asserts it.
- Close each window by its exact title (WM_CLOSE to that window only) right after its shot; verify it is gone.
  NEVER kill WindowsTerminal.exe, NEVER close any window whose title does not start with `cpi-` (the operator's
  `JJ_WORKPC: dev-flow` window must survive).
- At the end assert no window titled `cpi-*` remains, and print that assertion's result.
- Reject a shot that is black or has < 8 distinct colours, or whose end state is wrong (e.g. no palette); retry ≤ 3.

## HTML report
Export the workspace report for the same synthetic board through `report_html.extract` + `write_reports`
(see `tests/test_report_html.py`), open it headless (see `tests/report_browser.py` for the repo's helper, else
playwright if installed), screenshot the task's notes at 1200x800 → `html-workspace.png`. Report 0 console errors.

## Output
PNGs `<scene>_<WxH>.png` (8 TUI + 1 HTML) in `evidence/captures/`, the scripts (`scene.py`, `shoot.ps1`), and
`captures.md`: one row per PNG (file, size, distinct-colour count, retries, end-state check) plus the final
"no cpi- window left" line. Delete any temp homes you created. Return ≤8 lines.
