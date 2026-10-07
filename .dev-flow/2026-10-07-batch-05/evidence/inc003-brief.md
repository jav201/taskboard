# CHUNK — DeepSeek V4 Pro — increment 003 of batch 2026-10-07-batch-05 (the carries batch)

You implement increment 003 of batch-05 in the MAIN checkout at
`C:/Users/jjgh8/Github/taskboard`. The chain-map carries (batch C's open items).

## READ FIRST
- The contract: `.dev-flow/2026-10-07-batch-05/01-requirements.md` — HLR-1105/LLR-1105.1
  (the deep-chain cap amends TC-810's fold; the one-pass resize heal; AT-801b's docstring).
- The amendment rides **LED-2026-10-07-batch-05.1** — the amended TC-810 cites it.

## THE WORK — `taskboard/views.py` (the chainmap region), `taskboard/app.py`
## (`refresh_view` ONLY), `tests/test_chainmap.py`, `tests/test_chainmap_app.py`.
## No other source. No git.

1. **The deep-chain cap.** Today the chain map's fold drops WHOLE bands that do not fit
   (`test_TC_810` pins it). The carried refinement: a band that PARTIALLY fits draws its
   fitting chains and ONE tail row naming the rest `+N more ↓` — the kanban law (HLR-803's
   pin, kanban-style). A band whose FIRST chain does not fit still drops whole — the
   dangling-head law stands (no head without its canvas). N is exact (the band's chains
   minus the drawn ones). Read the fold in `views.render_chainmap`'s pipeline and the
   existing `test_TC_810` fixture before shaping the fix; the line_map must only ever name
   rows that actually painted.
2. **Amend TC-810** in `tests/test_chainmap.py`: a partially-fitting band draws its chains
   + the `+N more ↓` tail (N exact); the zero-fit band still drops whole (head AND canvas
   gone); the tail row reaches the line_map like any painted row. Keep the test's frozen
   fixture and calendar seam.
3. **The resize heal.** `app.refresh_view` (~app.py:1495): at its END, re-verify
   `selected_task_id` against the FRESH `line_map` — a selection the new frame does not
   name drops to the nearest painted row (or clears when nothing paints), so resizing heals
   in ONE refresh. The chain map's current heal leans on a second refresh — this lands the
   re-verify in the one place every repaint closes through. Guard: only touch the selection
   when the current view actually produced a line_map naming tasks (the kanban/lanes/gantt
   line_maps too — read how `refresh_view` consumes `self._line_map` first; when in doubt,
   scope the re-verify to entries the map does not name, keep other views' behavior
   byte-identical, and say what you scoped in your report).
4. **AT-801b's docstring** (`tests/test_chainmap_app.py:296`): correct it to what the arm
   actually does (it says "linking re-renders" but presses escape — read the body, write
   the truth).

## DISCIPLINE
- Run: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_chainmap.py tests/test_chainmap_app.py -q` — green. Then the FULL suite once — report the count; if anything outside your files reddens, STOP and name it.
- The C-2b oracle frames (`tests/test_chainmap.py`'s TC-801/TC-802 byte-exact arms) must stay
  byte-green — the cap only touches bands that previously vanished, so the oracle frames
  (no folded bands) must not move. If they move, your change over-reached: stop and report.
- Minimal change, shipped voice, English comments.

## REPORT BACK
Per item: what changed (file:line), the amended TC-810's arms, the resize re-verify's exact
scoping, the suite counts, anything you punted.
