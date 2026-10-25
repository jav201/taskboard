# Capture page — batch 2026-10-24-batch-02 (the home defers the board's start)

Real full-colour Windows Terminal PNGs of the shipped `TaskboardApp`, unpatched, at
**118x30** and **80x24**. Method: batch 2026-10-24-batch-01's harness (`shoot.ps1` +
`shoot_real.py`), adapted with `h01-` titles. Each window is launched as
`cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title h01-<scene>-<size>-<n> ...'`,
the app re-asserts the title (`PROTO_SHOT_TITLE`), plays the scene's keys through its own key path
(`App._press_keys`), writes a READY file with its end state, and is grabbed with `PrintWindow`.
The window is closed by its unique title right after its shot (WM_CLOSE, Windows Terminal windows
only, verified gone); no terminal process is killed and no other window is touched. A grab that is
black, has fewer than 8 sampled colours, or ends in the wrong state is rejected and retried in a new
window (up to 3 tries); every written PNG is re-verified from disk (>= 8 colours, > 20 KB). Data:
`tests/multi_board_fixture.py` trimmed to two boards (`personal` = default, `client-retail-rag`) in a
temporary home (`TEMP\h01-cap-*`, removed after each shot), calendar/clock pinned to the fixture's
Tuesday 2026-10-20 09:30. Nothing touches the real home.

Run: `powershell -NoProfile -File .dev-flow\2026-10-24-batch-02\evidence\captures\shoot.ps1`
Final assertion, as its own command: `powershell -NoProfile -File ...\captures\assert-no-h01.ps1`

## The shots

| scene | file | what it proves | confirms |
|---|---|---|---|
| home | `png/home_<size>.png` | the quiet home at start: two boards, no modal, no toast. A foreign presence marker and a sweepable 40-day-old done task are planted on the default board BEFORE the start, and the READY check asserts: zero toasts, the default board's bytes unchanged, no marker of this window | ux-2 (quiet-home frame), AT-2701, HLR-2701 |
| offer | `png/offer_<size>.png` | `enter` on the default card: the milestone offer (`Personal  Milestones - convert one-day tasks?`) is the top screen over the chosen board; READY check: no `BoardsHome` anywhere on the stack | ux-1 (offer over the board), AT-2705, HLR-2704 |
| start | `png/start_<size>.png` | `enter` with the foreign marker and the sweepable task planted: the `Boards - open twice` warning AND the `Archived old work` notice are both up over the board (the worst-case toast stack); READY check: exactly one of each, the sweep really saved the archive | ux-2 (worst-case stack), ux-M1, AT-2702 |

## Results (2026-10-25, HEAD 8baf9ad + this commit)

All 6 shots accepted on **try 1**; every READY end state was `OK`.

| shot | colours (grab / PNG) | bytes |
|---|---|---|
| home 118x30 | 27 / 9 | 49,047 |
| home 80x24 | 18 / 14 | 36,070 |
| offer 118x30 | 14 / 34 | 56,580 |
| offer 80x24 | 25 / 24 | 47,461 |
| start 118x30 | 40 / 44 | 77,967 |
| start 80x24 | 34 / 42 | 67,363 |

Final `assert-no-h01.ps1`: `no h01-* window left open`. No `h01-cap-*` temp home and no `h01-*`
ready/cmd file remains in TEMP (one empty `h01-cap-*` folder re-created by the last window's
shutdown was removed by hand).

## Things to eyeball

- The clock in the board footer of `start_*` is the machine's real clock (the pin covers the
  calendar and `datetime.now()` in the app modules, not the footer clock widget); the toasts'
  `since 09:30` is the pinned time.
- At both sizes the `start` toasts are overlays on the lower right: at 80x24 they cover the
  Fitness lane's third task and the footer clock/city segment (visible: `Me` clipped); at 118x30
  they cover the lane's lower rows and the clock tail. Toasts overlay by design (seen in the shots).
- `start_*` shows the real stack of two toasts (marker + sweep), not the up-to-five of ux-M1's worst
  case: the rescue, renumbering and team-start notices need their own preconditions, and the
  milestone offer is a separate scene (`offer_*`, a board with an unmarked candidate). This is the
  stack the DDR condition ux-2 names for this scene.
- The `offer_*` shots show the offer as a modal over a dimmed, empty-looking board: the board
  beneath is not legible in the shot; the READY check, not the pixels, proves it is the board
  screen under the offer and that `BoardsHome` is off the stack.
