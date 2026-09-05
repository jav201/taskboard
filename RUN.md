# taskboard — widget prototype

```powershell
cd "C:\Users\jjgh8\OneDrive\Documents\Github\taskboard\.claude\worktrees\kanban-variants"
$env:PYTHONIOENCODING = "utf-8"
python prototypes\widget_slice\app.py
```

`$env:PYTHONIOENCODING` goes on its own line and is set **once per terminal** — PowerShell has no
inline `VAR=x cmd` prefix. Without it the verify scripts below die with `UnicodeEncodeError` under
cp1252 while printing drawn glyphs, which looks like an app crash but is the script's `print`.

## Keys

    1 2 3 4     board · swimlanes · agenda · gantt
    ← ↑ ↓ → /hjkl   move the cursor (board; lateral moves land on the
                VISUAL neighbour, by region)
    t           cycle visual language — TEN, in this order: naught, corgi,
                instrument, swiss, industrial, nord, darkside, ledger,
                solari, blueprint (phosphor and bbs were RETIRED 2026-07-26
                by user curation). Six draw the board as full-width
                SECTIONS (corgi, swiss, darkside, ledger, solari,
                blueprint), nord as a master/detail SPLIT, and naught,
                instrument and industrial as COLUMNS.
    g           COMPONENT GALLERY — every component of the active language
                on one screen; press t inside it to compare languages
    v           force size class (glance / widget / board)
    c           configure the signal engine
                inside it: space toggle · ↑↓/jk move · ←→ pick the worker
                group (clamps at the ends) · [ ] threshold · r press Refresh
                (recomputes every enabled signal; dead when none are)
                the worker group is ONE choice with TWO mechanisms, chosen by
                width: wide, a radio set with every option named; narrow, a
                STEPPER showing one option with the two ways off it. Same set,
                same key, and at an end the step is not drawn — because ←→
                clamp there, and the render says so.
    ?           keymap        ctrl+p  command palette
    r           refresh now   q       quit

`?` prints the FULL map in two columns — every binding the app owns, including the ones the footer
hides (`show=False` motion keys) plus the two keys Textual itself binds (`ctrl+q`, `ctrl+p`). An
unprinted working key is the defect. The real app (`python -m taskboard`) has its own `?` map on the
same rule: five primaries on the footer, everything else printed there.

Resize the window and the surface changes on its own — that is the point.
Animations: the gantt flow packet travels; the agenda urgency bar has a
travelling highlight. `TEXTUAL_ANIMATIONS=none` degrades both to their final
frame with no loss of information.

`t` switches the STRUCTURE, not just the palette (PENDING.md item 0, fixed 2026-07-26): cards,
column heads, meter, agenda/gantt/lanes bars, calendar cells, queue markers and focus chrome all
render through the active language's kit (`taskboard/language.py`) — **and so do the components**
(tui-design/COMPONENTS.md): the `c` config screen draws each language's own switches, sliders and
cursor; the view switcher row is per-language tabs (corgi shows only the active mode, on purpose);
pending tiles spin with each language's spinner.

The `g` gallery is where the COMPONENT CONTRACT is judged: slider · bar · switch · checkbox · radio ·
button · **text field** (a caret, a placeholder and a window, per language) · **scroll bar** (a
window on a track — where the view is AND how big it is) · **stepper** (one option of a set, with the
two ways off it — the family's last component), each drawn in every state the registry derives for
it. The field and the scroll bar are **gallery-only on purpose**, for different reasons: nothing in
the engine is typed, and the surfaces that really scroll are Textual containers that draw their own
scrollbar chrome — ours documents that chrome rather than fighting the framework for it. The stepper
is not: it has a live seat on the narrow config screen, and the gallery is where its floor, its
ceiling and its two END BEHAVIOURS (clamp and wrap) are drawn side by side. **A clamped stepper at
its floor draws no step off it** — the end is a shape, never a colour.

## Checks

All paths are relative to the worktree root, so `cd` there first.

```powershell
python -m pytest tests -q              # project suite            -> 137 passed
                                       # (test_win_clipboard_roundtrip is env-
                                       # dependent: fails if the clipboard is busy)
python prototypes\verify_language.py   # THE LANGUAGE AXIS: 10857 checks — greyscale
                                       # pairs, token mutation, data-viz laws,
                                       # drive-checks, legibility, board geometry
                                       # (one measure: row_width) -> ALL PASSED
python prototypes\verify_aperture.py   # the REAL app's aperture: 151 checks —
                                       # launcher, legend, load band, queue row
                                       # closes inside its panel  -> ALL PASSED
python prototypes\verify_widget.py     # size classes, focus, budget: 24 -> ALL PASSED
python prototypes\verify_board.py      # frame integrity, motion:     22 -> ALL PASSED
python prototypes\verify_variants.py   # variant drive/render/budget: 12 -> ALL PASSED
python prototypes\verify_ink.py 12     # ink fraction per language x size class
```

`verify_language` is the slow one (~75-80 s); the rest are seconds. **It is safe to run from a clean
tree**: until `harness-hygiene` inc24 it rewrote the tracked capture fixture (F-17), and it now writes
nothing tracked. **Two flakes are open, not zero** (`PENDING.md`): F-15 in `test_surface.py`, bounded at
0/50 isolation runs and detected at every seat but never reproduced, and F-18, an observation-point race
in `test_board_seat.py`. The darkside capture race was a third and separate harness bug (settle signing
off on a frame composed at the wrong width) and is cured by settle's condition C.

## The REAL app's aperture (the prototype grown into the product)

The shipped app (`python -m taskboard`) now has the widget posture behind the
**`6` key**: hero + meter + signal tiles + due-calendar/up-next queue, drawn
through the active language (`t` cycles all ten; the choice persists). The
number keys **1-5 exit INTO that view** — the aperture is a launcher. `esc`
returns. Acceptance: `prototypes\verify_aperture.py`.

`verify_ink.py` takes an optional screen height (default 26) and reports against the ~35% glance
floor from `tui-design/DENSITY.md`. It is a measurement, not a pass/fail gate — the floor's geometry
is still undefined (`PENDING.md` items 1 and 8, both deferred).
