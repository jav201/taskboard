# E13 captures — Inc K (mechanical task)

Real Windows Terminal PNGs of the SHIPPED app (not the prototype) for the capture view (`n`). Worktree:
`C:/Users/jjgh8/Github/taskboard-wt/capture-proto`. Interpreter `C:/Users/jjgh8/anaconda3/python.exe`.
Never edit `taskboard/` or `tests/`. Write everything under `.dev-flow/2026-11-01-v3-incK/evidence/captures/`.

## Model to copy
The previous increment's harness: `.dev-flow/2026-11-01-v3-incL/evidence/captures/` (`scene.py`,
`shoot.ps1`, `captures.md`) — window per scene, unique title, READY file, WM_CLOSE by exact title, verify gone,
reject black / < 8 colours, retry ≤ 3. Copy and adapt; do not import from `prototypes/` or from incL.

## The synthetic data (temp home; `Path.home` redirected as the incL scene does)
A registry of TWO boards, owner `username_subject`, no real names:
- Board **Client A** (phases Backlog · Todo · Doing · Done), the open board: projects "Eval harness" (tasks
  "Golden set questions", "Answer key rubric") and "Pilot rollout" (tasks "Pilot stores list", "Steering deck").
- Board **Course** (phases Backlog · Todo · Done): project "Module 4 · Volumes" (tasks "Volume lab", "Oracle script").
- `~/.taskboard/inbox.json` written directly in the store's schema (read `01-requirements.md` HLR-4407 and
  `graph-proto-S.cw.md` for the exact keys; `divider_notice` absent unless the scene says so). Pad text for the
  scenes that need notes (4 notes, dividers `____`):
  1. `Golden set: 12 questions still have no answer key` / `ask @username_subject which stores count`
  2. `Volume lab fails on WSL` / `the oracle script expects /mnt/c`
  3. `Quote for the new client: contracts Q&A` / `two weeks, fixed price`
  4. `Steering deck: demo the hybrid search on pilot stores`
Launch the app on the registry; if it opens on the boards home, press `escape` first (as the tests do), then `n`.

## Scenes (`scene.py <name>`), each at 118x30 and 80x24
- `k-empty`: empty pad (`pad` ""): the ghost example with its drawn rule and the hint row `____ ↵ new note · alt+l divider`.
- `k-dividers`: the 4-note pad, cursor in note 4 (every divider line drawn as a full-width rule; the note count in the head).
- `k-notice`: empty pad and no `divider_notice`; type `First note`, `enter`, `____`, `enter` → the one-time notice visible.
- `k-rail`: the 4-note pad, cursor in note 4 (the rail: top option + alternatives, the `why` words, board chips).
- `k-review`: the 4-note pad, `alt+a` (the batch review list).
- `k-dump`: the 4-note pad, cursor in note 1, `alt+d` → the toast visible and the note gone from the pad.
- `k-newproject`: the 4-note pad, cursor in note 3, `alt+n` (the inline new-project field with its board cycle `⇥ board`); type `Contracts QA`.
- `k-colour`: pad `Vendor call\n::b:: ask the vendor :: @username_subject\n::r:: blocker: 12 questions lack a key ::\n==decided: 400-token chunks==` (colour spans live in the pad).
Drive keys through the app (`_press_keys` / the pilot path, as incL's scene does). 16 PNGs.

## Window rules (load-bearing)
- Launch: `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <title> ...'` with a UNIQUE
  title `cpi-<scene>-<WxH>-<random>`; the app re-asserts it.
- Close each window by its exact title (WM_CLOSE to that window only) right after its shot; verify it is gone.
  NEVER kill WindowsTerminal.exe, NEVER close any window whose title does not start with `cpi-` (the operator's
  `JJ_WORKPC: dev-flow` window must survive).
- At the end assert no window titled `cpi-*` remains, and print that assertion's result.
- Reject a shot that is black or has < 8 distinct colours, or whose end state is wrong (e.g. the capture view not
  open, the review not open, the toast missing); retry ≤ 3.

## Output
PNGs `<scene>_<WxH>.png` in `evidence/captures/`, the scripts (`scene.py`, `shoot.ps1`), and `captures.md`: one
row per PNG (file, size, distinct-colour count, retries, end-state check) plus the final "no cpi- window left"
line, and `capture-log.txt`. Delete any temp homes you created. Never touch the real `~/.taskboard`. Return ≤ 8 lines.
