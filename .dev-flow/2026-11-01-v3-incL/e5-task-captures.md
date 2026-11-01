# E13 captures — Inc L (mechanical task)

Real Windows Terminal PNGs of the SHIPPED app (not the prototype) for the added-order list (`N`). Worktree:
`C:/Users/jjgh8/Github/taskboard-wt/capture-proto`. Interpreter `C:/Users/jjgh8/anaconda3/python.exe`.
Never edit `taskboard/` or `tests/`. Write everything under `.dev-flow/2026-11-01-v3-incL/evidence/captures/`.

## Model to copy
The previous increment's harness: `.dev-flow/2026-11-01-v3-incC/evidence/captures/` (`scene.py`,
`shoot.ps1`, `captures.md`) — window per scene, unique title, READY file, WM_CLOSE by exact title, verify gone,
reject black / < 8 colours, retry ≤ 3. Copy and adapt; do not import from `prototypes/` or from incC.

## The synthetic data (temp home; `Path.home` redirected as the incC scene does)
A registry of TWO boards, owner `username_subject`, no real names:
- Board **Work** (4 phases Backlog · Doing · Review · Done): project "Eval harness"; tasks
  1. "Volume oracle script" — no `created`, no history record (unknown, `?`);
  2. "Pilot store list" — no `created`, a `history.jsonl` birth record `{"task": id, "from": null, "to": "Backlog", "at": "2026-10-28T10:30:00"}` (inferred `≈`);
  3. "Sync notes" — `created` "2026-10-31T18:20:00", phase Review, priority high, due 2026-11-03, one URL, notes
     `Sync notes, 3 pens\n::y:: decided: 400-token chunks ::\n::r:: blocker: 12 questions lack a key ::\n::g:: done: rubric draft ::\n::b:: ask the vendor for the store list ::`;
  4. "Archived memo" — `created` "2026-10-30T09:00:00", `archived: true`.
- Board **Home** (3 phases Backlog · Doing · Done): project "House"; tasks
  5. "Pay the rent" — `created` = today 08:10, phase Done;
  6. "Week 3 plan" — `created` = yesterday 21:47, phase Doing.
Write the boards and history files as JSON directly (the app's format, `tests/added_list_fixture.py` shows the
shapes); launch the app on the registry so `N` reads both boards. If the app opens on the boards home, press
`escape` first (as the tests do).

## Scenes (`scene.py <name>`)
- `ls-newest`: `N` (newest first, archived hidden — the head says `1 archived hidden`; the state column visible).
- `ls-oldest`: `N`, `o`.
- `ls-archived`: `N`, `v` (archived shown, dimmed; head `archived shown`), cursor moved onto "Archived memo".
- `ls-pane`: `N`, cursor on "Sync notes" (the detail pane with coloured notes, meta, source line).
- `ls-inferred`: `N`, cursor on "Pilot store list" (`≈` time and the history source line).
- `ls-unknown`: `N`, cursor on "Volume oracle script" (`?` and `added: unknown, before Oct 31 · #1 in Work's board file`).
Drive keys through the app (`_press_keys` / the pilot path). Each at 118x30 and 80x24 → 12 PNGs.

## Window rules (load-bearing)
- Launch: `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <title> ...'` with a UNIQUE
  title `cpi-<scene>-<WxH>-<random>`; the app re-asserts it.
- Close each window by its exact title (WM_CLOSE to that window only) right after its shot; verify it is gone.
  NEVER kill WindowsTerminal.exe, NEVER close any window whose title does not start with `cpi-` (the operator's
  `JJ_WORKPC: dev-flow` window must survive).
- At the end assert no window titled `cpi-*` remains, and print that assertion's result.
- Reject a shot that is black or has < 8 distinct colours, or whose end state is wrong (e.g. the list not
  open, the cursor not on the scene's task); retry ≤ 3.

## Output
PNGs `<scene>_<WxH>.png` in `evidence/captures/`, the scripts (`scene.py`, `shoot.ps1`), and `captures.md`: one
row per PNG (file, size, distinct-colour count, retries, end-state check) plus the final "no cpi- window left"
line, and `capture-log.txt`. Delete any temp homes you created. Return ≤ 8 lines.
