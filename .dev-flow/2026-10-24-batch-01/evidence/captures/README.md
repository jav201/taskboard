# Capture page — batch 2026-10-24-batch-01 (milestone marks)

Real full-colour Windows Terminal PNGs of every shipped milestone-marks item, at
**118x30** and **80x24**. Method: the people round's capture harness (unique
`m01-` window titles re-asserted by the app, `PrintWindow`, full colour
`COLORTERM=truecolor`, each window closed by title right after its shot, no
terminal process ever killed, no other window touched). The app subclass
(`shoot_real.py`) plays each scene through the app's own key path
(`App._press_keys`) on the round's synthetic boards and classes
(`tests/milestone_marks_fixture.py`, TODAY pinned to Tuesday 2026-10-20) in a
temporary home (`TEMP\m01-cap-*`, removed after each shot). Every grab was
rejected and retried in a new window when black or under 8 sampled colours;
every written PNG was verified again (not black, >= 8 colours, > 20 KB).

Run: `powershell -NoProfile -File .dev-flow\2026-10-24-batch-01\evidence\captures\shoot.ps1`

## The shots

| scene | size | file | what it proves | confirms |
|---|---|---|---|---|
| gantt | 118x30, 80x24 | `png/gantt_<size>.png` | Client A's gantt: late classed milestones draw their class glyph in its class colour with the date in `over` and the `▲Nd` chip (`Rubric sign-off` ■ violet `▲2d`); reached ones the hollow twin + `✓` in `reached` (`Catalog parsed` △ ✓); unclassified `◆` in `mut` (`Handover call`); the legend strip under the ruler names the drawn classes | AT-2603, TC-2604 (gantt arms), TC-2607 (the strip, LLR-2607.1) |
| manager | 118x30, 80x24 | `png/manager_<size>.png` | `#` opens the MarksManager: the four classes, each its shape in its colour, live open/all counts read across boards, the `◆ (no class)` row, `▶` on the chosen row, the key row `↑↓ move ␣ hide/show n new e edit esc close` | TC-2606 (LLR-2606.1/.3), AT-2601 step 1 |
| form | 118x30, 80x24 | `png/form_<size>.png` | `n` opens MarkForm: the name field focused, the shape row (SHAPES only — no `◆`, LED .46), the colour row, the live preview, the key line `alt+n name alt+c colour alt+h shape alt+s save esc cancel` | TC-2606 (LLR-2606.2), AT-2601 step 2 |
| editor | 118x30, 80x24 | `png/editor_<size>.png` | `e` on a classed milestone opens the editor with the class Select directly after `#f-milestone`; `alt+m` focuses it and opens the overlay (`◆ none` + the four classes, each its shape in its colour) | TC-2605 (LLR-2605.1), AT-2601 step 3 |
| hidden | 118x30, 80x24 | `png/hidden_<size>.png` | `␣` on Payment in the manager hides it (persisted `hidden: true`); the gantt redraws with Payment's milestones gone and the strip names the remaining drawn classes + `1 hidden` | TC-2606 (LLR-2606.2 `space` toggle), TC-2607, LLR-2608.1 (`_hide`) |
| search | 118x30, 80x24 | `png/search_<size>.png` | `/` `#pay` `enter` in the kanban: the bar `/ ⬢ Payment  milestones of this class only` with the tally, and only Payment's milestones in the frame | AT-2606, TC-2608 (LLR-2608.2) |
| present | 118x30, 80x24 | `png/present_<size>.png` | the presentation's view 1 of Pilot rollout (payment + review + launch milestones): the strip under its ruler names those three classes | TC-2607 (`legend_strip_project`, LLR-2607.1), MM-D5 |

## Accepted-cost surfaces the operator should eyeball

- **View 3 draws no strip** (ux-reviewer standing note): the presentation's
  view 3 (`all`, the timeline) has no ruler in the single-project sense and
  therefore no strip — the strip is view 1/2's surface. These captures show
  view 1 only; do not read view 3's bareness as a regression.
- **The `▲` glyph beside the `▲Nd` chip** (MM-D5's logged ambiguity): the late
  chip reads `▲2d` etc. in `over`; where a late Delivery milestone sits, its
  class glyph is also `▲` (cyan) — shape and chip can echo. That is the seat
  working as specified (shape says the class, the chip says late), not a
  doubled warning.
- The manager's dimmed row (`[ ]`, `hidden: gantt + present` in amber) is
  visible mid-scene in `hidden` before `#` closes the manager; the shot itself
  ends on the gantt, per the scene's contract.
- **The editor at 80x24 is wider than the screen** (real, observed): the chip
  row clips at the right edge (`milestone X blocked X ar…`) and the open class
  Select overlay covers the Preview column. The `alt+m mark` key line, the
  collapsed Select (`▲ Delivery`) and every shipped element are visible; the
  clipping is the modal's fixed layout at 80 cells, not a marks defect. The
  form (MarkForm) at 80x24, by contrast, fits whole.
- **The gantt project-span progress dot is not the same glyph in every shot**
  (real, observed — not a defect): `gantt` caught it at rest (`●`),
  `hidden` caught a pulse phase (`◎`). It is the shipped breathing animation
  for behind work (`views._progress_glyph`, `PULSE_PHASES`), a live terminal
  caught mid-frame.

## Verification results (2026-10-24, HEAD 1cae9c6)

All 14 shots accepted on **try 1** — no retries anywhere. Every grab:
PrintWindow, full colour (NO_COLOR cleared, COLORTERM=truecolor), unique
`m01-<scene>-<size>-<n>` title re-asserted by the app, exactly one window
match, WM_CLOSE by title verified after the shot. Every written PNG
re-verified from disk: not black, 8–52 sampled colours, 30,589–148,527 bytes.
READY files reported `OK` end states for all scenes (manager → MarksManager,
form → MarkForm, editor → TaskModal with the Select expanded, present →
PresentScreen; gantt/hidden/search → the main screen).

| shot | colours (grab / PNG) | bytes |
|---|---|---|
| gantt 118x30 | 39 / 52 | 148,527 |
| gantt 80x24 | 25 / 50 | 114,413 |
| manager 118x30 | 17 / 8 | 34,790 |
| manager 80x24 | 17 / 9 | 30,589 |
| form 118x30 | 29 / 32 | 44,545 |
| form 80x24 | 10 / 30 | 39,821 |
| editor 118x30 | 22 / 27 | 52,368 |
| editor 80x24 | 22 / 32 | 47,696 |
| hidden 118x30 | 35 / 36 | 130,260 |
| hidden 80x24 | 25 / 49 | 105,200 |
| search 118x30 | 18 / 14 | 56,126 |
| search 80x24 | 13 / 22 | 45,598 |
| present 118x30 | 22 / 14 | 63,586 |
| present 80x24 | 25 / 16 | 53,507 |

Final no-`m01-`-window assertion, run as its own command
(`powershell -NoProfile -File ...\captures\assert-no-m01.ps1`):

```
no m01-* window left open
```

No `m01-cap-*` temp home or `m01-*` ready/cmd file remains in TEMP.

See `png/capture-log.txt` for the raw per-shot machine log.
