# Capture page — batch 2026-10-25-batch-02 (the presentation colours the notes' highlights)

Real full-colour Windows Terminal PNGs of the shipped `TaskboardApp`, unpatched, at
**118x30** and **80x24**. Method: batch 2026-10-25-batch-01's harness (`shoot.ps1` +
`shoot_real.py`), adapted with `n01-` titles and two scenes (`gantt` = view 1, `split`
= view 2). Each window is launched as
`cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title n01-<scene>-<size>-<n> ...'`,
the app re-asserts the title (`PROTO_SHOT_TITLE`, again at capture time before the READY
write), plays the scene's keys through its own key path (`App._press_keys` — the cursor
task is selected exactly as the app's own ATs do, then `R`, then `2` for the split view)
and writes a READY file with its end state **and the scripted content check** (the
batch's C2, batch-01's discipline): the composited full-screen-stack render of the LIVE
app at capture time — the same source the pixels hold — must carry the three highlight
tone hexes `#fbbf24` (soon), `#f43f5e` (over), `#4ade80` (green) **in its styles**
(HTML export with inline styles) AND hold no run of `==`, `!!`, `++` anywhere (the note
rows included), with the note's marker-free words present. A shot that is merely
non-black can therefore never pass; a wrong end screen (`PresentScreen`) or wrong view
(`PRESENT_SCREEN_VIEWS[_view]`) fails too. The window is closed by its unique title
right after its shot (WM_CLOSE, Windows Terminal windows only, verified gone); no
terminal process is killed and no other window is touched (`JJ_WORKPC: dev-flow` among
them). A grab that is black, has fewer than 8 sampled colours, ends in the wrong state,
or fails the content check is rejected and retried (up to 3 tries); every written PNG is
re-verified from disk (>= 8 colours, > 20 KB). Data: a synthetic board only — one
project (`Launch readiness`), two open tasks, the FIRST task's (`Launch plan review`)
notes holding the commission's highlighted note
`Review ==the launch plan== with !!care!! and ++the sponsor++ before Friday` — in a
temporary home (`TEMP\n01-cap-*`, removed after each shot; the two empty folders the
first two shots' closed windows left were removed by hand, verified none left).
Calendar/clock pinned to Tuesday 2026-10-20 09:30. Nothing touches the real home; no
real names anywhere.

Run: `powershell -NoProfile -File .dev-flow\2026-10-25-batch-02\evidence\captures\shoot.ps1`
Final assertion, as its own command: `powershell -NoProfile -File ...\captures\assert-no-n01.ps1`

## The shots

| scene | file | what it proves | confirms |
|---|---|---|---|
| gantt | `png/gantt_<size>.png` | view 1: the cursor sits on the first task (the highlighted note is its notes) and the gantt cursor note expands under the briefs: `the launch plan` in #fbbf24, `care` in #f43f5e, `the sponsor` in #4ade80, no marker characters. READY: `PresentScreen` on top, view `gantt`, the three tone hexes in the composited frame's styles, 0 marker runs, the note words present | AT-2901 · HLR-2901 |
| split | `png/split_<size>.png` | view 2 (the `2` key): every shown open task's note block below the field carries the same tones, no markers; at 118x30 the two-column split shows the `++…++` span wrapped across two rows, both in #4ade80. READY: `PresentScreen` on top, view `split`, same tone / no-marker assertions | AT-2902 · HLR-2902 |

## Results (2026-10-25, HEAD `409a575`)

All 4 shots accepted on try 1; every READY end state was `OK` (screen `PresentScreen`,
view as scene, the three tones present, 0 marker runs, the note words present).

| shot | colours (grab / PNG) | bytes |
|---|---|---|
| gantt 118x30 | 18 / 11 | 30,831 |
| gantt 80x24 | 13 / 10 | 26,113 |
| split 118x30 | 16 / 14 | 34,534 |
| split 80x24 | 13 / 11 | 28,770 |

`assert-no-n01.ps1` (its own command): `no n01-* window left open`. No `n01-cap-*` temp
home and no `n01-*.ready`/`n01-*.cmd` file remains in TEMP (verified after the manual
cleanup of the two empty folders).

## The content check, named (the batch's C2)

The mechanism is scripted, not a glance: `shoot_real.py`'s `_check_scene` asks the live
app for its composited full-screen-stack frame at capture time (the same source the
pixels hold), exported twice — as text (0 runs of `==`/`!!`/`++`, the marker-free note
words `the launch plan` / `care` / `the sponsor` present) and as HTML with inline
styles (all of `#fbbf24`, `#f43f5e`, `#4ade80` present) — and the end screen is
`PresentScreen` on the scene's view (`PRESENT_SCREEN_VIEWS[_view]`). A human eyeball of
all four PNGs agrees with the script: the gantt cursor note and both split blocks read
marker-free with the three coloured words, at both sizes; the split view at 118x30
shows the green span wrapped across two rows, both green.
