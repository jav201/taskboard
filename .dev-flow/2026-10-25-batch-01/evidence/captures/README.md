# Capture page — batch 2026-10-25-batch-01 (the board shows behind the start-up modals)

Real full-colour Windows Terminal PNGs of the shipped `TaskboardApp`, unpatched, at
**118x30** and **80x24**. Method: batch 2026-10-24-batch-02's harness (`shoot.ps1` +
`shoot_real.py`), adapted with `b01-` titles and three scenes. Each window is launched
as `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title b01-<scene>-<size>-<n> ...'`,
the app re-asserts the title (`PROTO_SHOT_TITLE`), plays the scene's keys through its own
key path (`App._press_keys`), and writes a READY file with its end state **and the scripted
content check** (ux condition C2): the composited full-screen-stack render of the LIVE app
at capture time — the same source `App.export_screenshot` consumes, i.e. the same frame the
pixels hold — must show > 0 board rows outside the modal's box. A shot that is merely
non-black can therefore never pass. The window is closed by its unique title right after its
shot (WM_CLOSE, Windows Terminal windows only, verified gone); no terminal process is killed
and no other window is touched. A grab that is black, has fewer than 8 sampled colours, ends
in the wrong state, or fails the content check is rejected and retried (up to 3 tries); every
written PNG is re-verified from disk (>= 8 colours, > 20 KB). Data:
`tests/multi_board_fixture.py` trimmed (one board for `single`/`picker`, two for `offer`) in
a temporary home (`TEMP\b01-cap-*`, removed after each shot; the 12 folders the failed picker
tries left were removed by hand, verified none left). Calendar/clock pinned to the fixture's
Tuesday 2026-10-20 09:30. Nothing touches the real home. Synthetic roster only
(`username_subject`, Ana).

Run: `powershell -NoProfile -File .dev-flow\2026-10-25-batch-01\evidence\captures\shoot.ps1`
Final assertion, as its own command: `powershell -NoProfile -File ...\captures\assert-no-b01.ps1`

## The shots

| scene | file | what it proves | confirms |
|---|---|---|---|
| single | `png/single_<size>.png` | a single-board start whose board has a candidate: the offer opens at mount over its own board, dimmed, rows readable around the box. READY: `MilestoneOffer` on top, no home, > 0 rows outside the box | the commission's first capture · AT-2801 · HLR-2801 |
| offer | `png/offer_<size>.png` | two boards, `enter` on the default card: the offer opens over the chosen board, the home gone (the `Personal` chip shows). READY: no `BoardsHome` on the stack, > 0 rows outside the box | the commission's second capture · AT-2802 · HLR-2802 |
| picker | `png/picker_<size>.png` | a team-shared board with no identity (the offer mark pre-set): the picker ALONE over the dimmed board, at its blessed top-left placement (row 0, cols 0-61, bottom row 11 at 118x30 — `PDR-2026-10-25-batch-01#D1`). READY: `TeamIdentityPicker` on top, > 0 rows outside the box, the 118x30 geometry exact | ux C3's picker capture · AT-2803's picker half · HLR-2803 |

## Results (2026-10-25, HEAD `9aaada7` + the captures commit)

All 6 shots accepted; `single`/`offer` on try 1; `picker` needed two fixture fixes in
`shoot_real.py` (the roster is `kg_board.TEAM`; the picker's board is the registry's default,
not `board.json`; and a single-board registry, else the home defers the picker) and then
passed on try 1. Every READY end state was `OK`.

| shot | colours (grab / PNG) | bytes |
|---|---|---|
| single 118x30 | 31 / 37 | 55,103 |
| single 80x24 | 20 / 33 | 39,929 |
| offer 118x30 | 31 / 37 | 56,196 |
| offer 80x24 | 20 / 33 | 40,891 |
| picker 118x30 | 23 / 22 | 30,950 |
| picker 80x24 | 9 / 19 | 22,036 |

Final `assert-no-b01.ps1` (its own command): `no b01-* window left open`. No `b01-cap-*`
temp home and no `b01-*` ready/cmd file remains in TEMP (verified after the manual cleanup).

## The content check, named (ux condition C2)

The mechanism is scripted, not a glance: `shoot_real.py`'s `_check_board_visible` computes
the composited full-screen-stack render of the live app at capture time and counts non-blank
rows outside the modal's box borders (corners by glyph); a shot whose frame shows no board
rows is rejected and retried. A human eyeball of all six PNGs agrees with the script (the
board's rows are readable around every box; the picker's placement is its pre-batch
top-left). At 80x24 the offer box is full-width (pre-existing layout), so "rows around it"
reads as rows above and below — the fixture guarantees them.
