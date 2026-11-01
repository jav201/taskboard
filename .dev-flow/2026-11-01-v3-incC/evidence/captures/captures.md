# E13 captures — Inc C (shipped app, synthetic board, owner `username_subject`)

Scripts: `scene.py` (scenes ed-pen, palette, details, present; `html` export), `shoot.ps1` (Windows Terminal PNGs,
windows titled `cpi-<scene>-<WxH>-<n>`), `html_shot.py` (Playwright, 1200x800). Log: `capture-log.txt`.
Colour count = distinct colours in the shoot's sample grid (gate: >= 8); retries = extra tries beyond the first.

| file | size px | colours | retries | end-state check |
|---|---|---|---|---|
| ed-pen_118x30.png | 1708x928 | 35 | 0 | TaskModal, pen = blue, `::b:: new blue words ::` in notes: OK |
| ed-pen_80x24.png | 1176x760 | 39 | 0 | same: OK |
| palette_118x30.png | 1708x928 | 10 | 0 | ColourPalette over TaskModal, cursor on `later`: OK |
| palette_80x24.png | 1176x760 | 11 | 0 | same: OK |
| details_118x30.png | 1708x928 | 31 | 0 | TaskDetails of "Sync notes": OK |
| details_80x24.png | 1176x760 | 22 | 0 | same: OK |
| present_118x30.png | 1708x928 | 19 | 0 | PresentScreen (key `R`, gantt layout) listing the notes: OK |
| present_80x24.png | 1176x760 | 23 | 0 | same: OK |
| html-workspace.png | 1200x800 | n/a | 0 | workspace report, Notes card coloured; 0 console errors |

Note: the shipped palette modal paints on an opaque screen background, so the editor is not visible behind it
(the prototype's see-through was not shipped). Not a capture defect.

No cpi- window left: assertion passed (shoot.ps1 printed `no cpi-* window left open`; re-checked at the end).
Temp homes (`cp-cap-*`) and the temporary report folder were deleted.
