# Commission — the presentation colours the notes' highlights

Written by the orchestrator on 2026-10-25 for batch `2026-10-25-batch-02`. Branch `fix/present-note-highlights`, from `main` `6e72e2a`.

## The operator's words

The operator, 2026-10-25, on the ordered backlog: «Sigue con 4 con Kimi.» Item 4 is `.dev-flow/BACKLOG.md`'s entry from the people round:

> the presentation's split view draws the notes' `!!…!!` and `++…++` markers raw (`views._present_note_markup` paints the text `ink` with no `highlight_segments`; the rest of the app colours them).

## The defect

The notes' highlight syntax is `==text==` (`soon`), `!!text!!` (`over`) and `++text++` (`green`). `views.highlight_segments` (`taskboard/views.py`, around line 3450) is its one tokeniser. The board's markup and the details/editor preview both use it: they drop the markers and colour the span.

The presentation's note rows bypass it. Three paths are affected:

- `present_note_lines`, around line 6640;
- `_present_note_markup`, around line 6707;
- `_present_cut` and the split view's body, around line 6852.

So the room sees the raw markers. This affects the gantt view's cursor note (view 1), the split view's notes (view 2), and their `x` exports. Check view 3 as well.

## Decisions (record each in the plan)

- **PH-1, one tokeniser.** Presentation note text is coloured through `highlight_segments`, never a second parser, so the presentation cannot disagree with the board on what a note highlights (D-411).
  - The markers are dropped.
  - Each span takes its tone: `soon`, `over` or `green`.
  - The unmarked text keeps the presentation's own base tone (today `ink`, not the board's `mut`). The audience surface keeps its contrast.
- **PH-2, the width.**
  - **Wrapping.** It counts the visible text only, never the markers, so a highlighted row is not cut early.
  - **Spans across rows.** A span that wraps across rows keeps its tone on every row.
  - **Cuts.** The cut rows (`… +N lines`) and the edge marks keep their current wording.
  - **Glyphs.** Wide glyphs still wrap by cells (`_wrap_cells`).
- **PH-3, coexistence.**
  - **Mentions.** `@Name` (bold pink, `mention_marks`) and highlights can overlap. A mention inside a highlighted span stays bold pink.
  - **Bullets.** The bullet and number leads (`• `, `1. `) are unchanged.
  - **Unpaired markers.** An unclosed marker (`!!text` with no closer) stays literal text, exactly as `highlight_segments` treats it.
- **PH-4, exports.** The `x` exports (SVG/PNG) show the same colours as the screen. No other change to the presentation's layout, keys or hints.
- **No prototype.** This applies the app's existing, approved highlight colours to one more surface; it is not a new design.

## Increments

One increment, 001: at most 4 SOURCE files, expected `taskboard/views.py` only. Tests are uncapped.

## Acceptance

One node per AT; drive the app by keys where a user would.

- **AT-a, view 1.** A note with `==a==`, `!!b!!` and `++c++` shows no marker characters on the presentation's gantt view (1). Each word is painted in its tone (read the painted styles, not the text).
- **AT-b, view 2.** The same note in the split view (2), at 118x30 and at 80x24, including a highlighted span wrapped across two rows.
- **AT-c, the export.** The `x` export of view 2 carries the tones and no markers. Assert on the exported SVG.
- **AT-d, edge cases.** A mention inside a highlight stays bold pink. An unclosed `!!` stays literal.
- **AT-e, regressions.** Every presentation byte oracle and capture-based test stays green. Where an oracle fixture contains markers, the oracle legitimately changes: update it and justify it in the packet.

## Evidence

- **Import probe.** Before any test, run a probe test from the worktree root that prints `taskboard.__file__`. It must resolve to the worktree's `taskboard/`. Use `python -m pytest`.
- **Tests.** Use `env -u NO_COLOR` for every pytest run. `NO_COLOR=` does NOT unset it.
- **Full suite.** At P4, run it in 3 SEQUENTIAL chunks. The baseline is 3258 passed. Any skip other than the clipboard arm TC-1902, or any fail, blocks the close. Keep the transcripts.
- **Validator.** Run `--brief` at start and at close. It must report 0 BLOCK.
- **Mutation.** Mutation-check every new test. Bypassing `highlight_segments` must turn AT-a red.
- **Captures.** Take real Windows Terminal captures at 118x30 and 80x24 of view 1 and view 2 showing a highlighted note.
  - Reuse `.dev-flow/2026-10-25-batch-01/evidence/captures/` with `n01-` titles.
  - Close each window by title right after its shot and verify it is gone. Never close any other window.
  - Launch with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <t> ...'`.
  - Reject black shots and shots with fewer than 8 colours.
