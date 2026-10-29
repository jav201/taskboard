# Terminal captures — batch 2026-10-29-batch-01 (`H` report modal and its toast)

Real full-colour Windows Terminal PNGs of the shipped `TaskboardApp`, unpatched, at
**118x30 only**. The harness is a COPY of batch 2026-10-25-batch-02's
(`.dev-flow/2026-10-25-batch-02/evidence/captures/shoot.ps1` + `shoot_real.py`, which are
left untouched), adapted with `hx-` titles and three scenes.

## Re-run

From the worktree root, in PowerShell:

```
powershell -NoProfile -ExecutionPolicy Bypass -File .dev-flow\2026-10-29-batch-01\evidence\captures\terminal\shoot.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .dev-flow\2026-10-29-batch-01\evidence\captures\terminal\shoot.ps1 -Scenes report-modal,report-toast
```

Needs `%USERPROFILE%\anaconda3\python.exe` with the worktree's dependencies and `wt.exe`.
PNGs are overwritten in `png/`; result lines are APPENDED to `png/capture-log.txt`.
The last line printed is the window assertion (`no hx-* window left open`, else `FAIL`
with the titles left and exit code 1).

## Rules the harness keeps

- Each window gets a unique title `hx-<scene>-118x30-<n>`, launched as
  `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --size 118,30 --title <title> cmd.exe /c <TEMP\<title>.cmd>'`;
  the app re-asserts it (`PROTO_SHOT_TITLE`). Windows are matched by title PREFIX
  (`StartsWith`), in `WindowsTerminal` windows only; zero or two matches are errors.
- The window is closed right after its shot by that title only (`WM_CLOSE`) and verified
  gone. No process is killed; no other window is touched (`JJ_WORKPC: dev-flow` among
  them). The final sweep asserts no window whose title starts with `hx-` remains.
- Full colour: a grab with fewer than 8 sampled colours (black / flat) is rejected and
  the scene retried in a new window, up to 3 tries; the written PNG is re-verified from
  disk (>= 8 colours, > 20 KB).
- The app writes a READY file once its keys are played: line 1 is the scene's temporary
  home, line 2 the end state. A non-`OK` state is rejected and retried. The home is removed
  after the window is closed.

## Data

Synthetic only. `shoot_real.py` points `Path.home()` at a fresh `TEMP\hx-cap-*` folder and
builds the home exactly as `tests/test_report_export_app.py` (`build_home` / `open_home`)
does: `tests/report_fixture.py`'s `personal` / `client_a` / `course` boards saved to
`<home>\.taskboard\boards\<id>\board.json`, a `boards.json` registry (Personal, Client A,
Course; Client A opened last), the fixture's people and marks in memory; the registry is
then opened as `taskboard.__main__.open_app(None)` does. Date pinned to the fixture's
TODAY, 2026-10-29. Every scene starts with `esc` (from the home of boards to the open
board, Client A) and selects task `tst2` (Storefront relaunch), as TC-3118 does.

## Scenes and their READY checks

| scene | keys | READY check (on the live app's composited frame at capture time) |
|---|---|---|
| `report-modal` | `esc`, select `tst2`, `H` | top screen `ReportExport`; `Export an HTML report`, `● all boards (3)`, `○ Storefront relaunch on Client A`, `Personal · Client A · Course`, `Writes to … reports`, the key words |
| `report-modal-p` | same, then `p` | top screen `ReportExport`; `○ all boards (3)`, `● Storefront relaunch on Client A`, same names / folder / keys |
| `report-toast` | `esc`, select `tst2`, `H`, `b` | main `Screen`; exactly one `Report` toast whose text is `Report written: workspace-2026-10-29.html to <home>\.taskboard\boards\client-a\reports — o opens it (10 s)`; the file exists; `Report written:` and `o opens it (10 s)` painted. The grab happens about 3 s after `b`, inside the 10 s |

## Results (2026-10-29, HEAD `e8ec477`)

All three accepted on try 1 (PrintWindow); READY `OK` each; `no hx-* window left open`
after both runs; no `hx-cap-*` home, `hx-*.ready` or `hx-*.cmd` left in TEMP.

| PNG | colours (grab / PNG) | bytes |
|---|---|---|
| `png/report-modal_118x30.png` | 14 / 18 | 29,396 |
| `png/report-modal-p_118x30.png` | 14 / 19 | 29,241 |
| `png/report-toast_118x30.png` | 36 / 40 | 54,848 |

Seen in the PNGs (eyeballed):

- Key line in both modal shots: `b workspace   c deck   a both   p Storefront relaunch   o all boards   esc close`.
- `Writes to` shows the head-clipped folder `…Users\<user>\AppData\Local\Temp\hx-cap-*\.taskboard\boards\client-a\reports\`.
- Toast: `Report` / `Report written: workspace-2026-10-29.html to C:\Users\<user>\AppData\Local\Temp\hx-cap-*\.taskboard\boards\client-a\reports — o opens it (10 s)`, wrapped over three rows. The folder breaks mid-word (`.task` / `board`).
- Every shot also shows the app's own `Archived old work` toast (Client A's done task
  finished more than 20 days ago is auto-archived on open — fixture data, see the
  `STOREFRONT` note in `tests/test_report_export_app.py`).
- In the two modal shots the board behind the modal is not visible (backdrop reads solid
  dark). This is an observation from the pixels, not a diagnosed defect.
