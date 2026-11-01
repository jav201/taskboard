# Inc L captures (real Windows Terminal PNGs of the shipped app)

Harness: `scene.py`, `shoot.ps1`; log: `capture-log.txt`. Distinct colours counted over the full PNG; the harness also sampled >= 8 per shot.

| file | size | distinct colours | retries | end-state check |
|---|---|---|---|---|
| ls-archived_118x30.png | 1708x928 | 290 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-archived_80x24.png | 1176x760 | 290 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-inferred_118x30.png | 1708x928 | 275 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-inferred_80x24.png | 1176x760 | 275 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-newest_118x30.png | 1708x928 | 291 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-newest_80x24.png | 1176x760 | 291 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-oldest_118x30.png | 1708x928 | 274 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-oldest_80x24.png | 1176x760 | 274 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-pane_118x30.png | 1708x928 | 354 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-pane_80x24.png | 1176x760 | 354 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-unknown_118x30.png | 1708x928 | 274 | 0 | OK (list open, cursor on the scene's task, head text checked) |
| ls-unknown_80x24.png | 1176x760 | 275 | 0 | OK (list open, cursor on the scene's task, head text checked) |

no cpi-* window left open (asserted by shoot.ps1 at the end of the run).
