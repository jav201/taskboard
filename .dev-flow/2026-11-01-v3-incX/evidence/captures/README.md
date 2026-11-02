# Inc X captures (E13): real Windows Terminal PNGs of the shipped app

Harness: `scene.py` (scenes `xh-bar`, `xh-bar-wide`, `xh-toast`, `xh-keys`; `deck <dir>` writes the deck), `shoot.ps1`
(window titles `xh-<scene>-<WxH>-<n>`, closed by exact title right after each shot and verified gone; no other window touched).
Log: `capture-log.txt`. Adapted from the Inc L harness; the colour sampling was made denser (5 x 7 px) because a dark modal
(`?`) read as < 8 colours on a sparse grid and PrintWindow/CopyFromScreen then gave a black shot (rejected and retaken).
Synthetic boards in a temp HOME (`Path.home` redirected), owner `username_subject`; temp homes deleted.

| file | scene | size |
|---|---|---|
| xh-bar_118x30.png / xh-bar_80x24.png | main board key bar, `H` on the bar (label dropped at these widths) | 118x30, 80x24 |
| xh-bar-wide_201x30.png | same bar at 201 columns: `H Report` | 201x30 |
| xh-toast_118x30.png / xh-toast_80x24.png | `R`, then `x`: toast `present-eval-harness-2026-11-01.html`, `o opens it (10 s)` | 118x30, 80x24 |
| xh-keys_118x30.png / xh-keys_80x24.png | presentation `?`: `o open the last export (10 s)`, `x export this view · HTML deck` | 118x30, 80x24 |
| xh-deck-desktop.png / xh-deck-narrow.png | playwright (headless chromium) of the view-3 deck, project "Quasar Hidden" hidden | 1280x800, 480x800 |

## Deck byte checks (`deck/present-2026-11-01.html`, written by `R` `3` `x`, 16706 bytes)
- Hidden project `Quasar Hidden` (and its task `Quasar secret task`, URL `https://hidden.example.org/quasar`): 0 matches (case-insensitive) -> absent.
- Visible project `Eval harness`: present (control: the check can fail).
- `http` anywhere in the file: 0 matches; `example.com` (the visible task's fixture URL): 0. No `http` URL at all.
- Playwright: 0 non-file requests, 0 page errors, both viewports.

## End state
Every shot: end-state check OK in `capture-log.txt`; every PNG has > 8 colours (full-image counts 134-2667 on the checked set;
the black `xh-keys_118x30` first take was replaced). `shoot.ps1` asserts at the end that no `xh-*` window is left open.
