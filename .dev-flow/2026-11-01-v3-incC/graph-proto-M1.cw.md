# Code-Wire prototype — group M1: TaskModal pens and live ink (Inc C, E2)

Differences from `graph-baseline.cw.md` only. Changed nodes carry their full contract; new nodes are marked by `req:` ids of HLR-4203 / HLR-4204 / LLR-4202.10. Shared seams (`colour_spans`, `highlight_segments`, `TaskModal._lift_pen`, `[Data: PEN_CODES]`, `[Data: Span]`, `[Data: TaskModal.pen]`) are defined in `graph-interfaces.cw.md` and are not repeated here. Pen index i is 0..5 into PEN_CODES (r o y g b v), so `alt+5` is pen `4` (`b`, tone `blue`, `#60a5fa`).

Unchanged on purpose: `TaskModal.on_text_area_changed` (the ink is rebuilt inside `TextArea.edit`, before `Changed` is posted, so the handler needs no ink call; a forward `delete` can only extend a span, never move the cursor out of it, so it needs no leave-check either). `notes_preview` and `#task-preview` are unchanged.

Notes column widths (taskboard.tcss: `#task-box` padding `0 1`, `#task-edit` and `#task-prev` both `1fr`): notes width = (terminal width - 2) // 2, so `39` at 80x24 and `58` at 118x30.

Textual 8.2.8 internals relied on (read in `textual/widgets/_text_area.py` and `textual/_text_area_theme.py`): the private `TextArea._build_highlight_map` (called by `edit()` line 1700 after the change and before `Changed` is posted, by undo/redo lines 1765 and 1814, and by `_set_document` line 1184 during `__init__` and `load_text`); the private `TextArea._highlights` (`defaultdict[int, list[(start_byte, end_byte | None, name)]]`), which `_render_line` (lines 1494-1508) maps from UTF-8 bytes to code points with `build_byte_to_codepoint_dict`, and where an end of `0` is read as `None`, meaning "to the line end"; the private `TextArea._line_cache` (its cache key has the theme name but not the highlight map, so the override must clear it). Public API: `TextArea.register_theme` (it writes the per-instance `_themes` dict), the `theme` reactive, and `TextAreaTheme(name, syntax_styles)` (exported as `textual.widgets.text_area.TextAreaTheme`). Why the prototype leaked: `_set_theme` stores `dataclasses.replace(theme_object)`, which is a shallow copy, so `ta._theme.syntax_styles` IS the dict of the built-in theme. The built-in `css` theme is `TextAreaTheme(name="css", syntax_styles=_DARK_VS.syntax_styles)`, so writing to that dict changes every TextArea on every screen and the `vscode_dark` theme too. Probe on 8.2.8: `get_builtin_theme("css").syntax_styles is get_builtin_theme("vscode_dark").syntax_styles` → True; `dataclasses.replace(css).syntax_styles is css.syntax_styles` → True. `_app_theme_changed` runs `_set_theme(self._theme.name)` again, so a registered theme survives a change of app theme, but a direct mutation of `_theme` would be lost (after it had already leaked).

## Nodes

TaskModal.__init__
req: LLR-4203.4, HLR-4203
in: Board board; Task? task = None; Directory? people = None; object? marks = None
out: None
func: as at base (board, task, people, marks, mention picker state, image key), plus `self.pen = None` (no pen on when the editor opens) and `self._notes_w = 39` (the 80x24 notes width until `_fit_width` runs)
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace); [Data: TaskModal._notes_w] (replace)
examples: (TC-4233) board with one task, task that task → pen `None`, _notes_w `39`

TaskModal.compose
req: LLR-4203.9, LLR-4204.1, LLR-4204.6, HLR-4204
in:
out: ComposeResult widgets
func: as at base, with two changes inside `#task-edit`. (1) The Notes label is `Label("", id="notes-label", classes="task-sec")`; `_fit_width` → `_pen_label` fills it on mount, because the label's form depends on the width. (2) `#f-notes` is `InkArea(t.notes if t else "", id="f-notes")`, a TextArea subclass, so `query_one("#f-notes", TextArea)` and the `#task-box #f-notes` tcss rule still match. `#f-urls` and `#f-images` stay plain `TextArea`
module: taskboard/modals.py
examples: (TC-4247) task with notes "a ::b:: x :: c" → `#f-notes` is an InkArea and a TextArea; `#f-urls` and `#f-images` are of type TextArea, not InkArea
examples: (test_edit_window.py::test_the_editor_paints_its_keys_in_full) any task → the Preview label is unchanged: "ctrl+v paste · esc cancel"

TaskModal._fit_width
req: LLR-4203.9, LLR-4202.10
in: int width
out: None
func: as at base (the chip row folds below TASK_CHIPS_ONE_ROW plus the class Select's cost; `#task-keys` gets `key_line(keys, width - 2)`), plus `self._notes_w = (width - 2) // 2` (the notes column: `#task-box` pads one cell on each side, then two `1fr` columns), then `_pen_label()`. Runs on mount and on every resize, so the label's form follows the terminal width
module: taskboard/modals.py
modify: [Data: TaskModal._notes_w] (replace)
examples: (TC-4239, root on_mount) width `80` → _notes_w `39`, Notes label in the narrow form
examples: (TC-4239, root on_resize) width `118` → _notes_w `58`, Notes label in the wide form

pen_label
req: LLR-4203.9, LLR-4202.10, LLR-4203.4
in: int? pen; int width
out: Text label
func: the editor's Notes label as Text pieces, never markup (C-17). Pieces: `Notes` in `#8b98a5`; the state, which is `pen: none` in `mut` with no pen, or the chip " <name> " in `b #0d1117 on HEX[tone]`; the keys `1`..`6`, each bold in HEX[tone] of PEN_CODES; `0 off`; and `alt+c` in bold `bright`. Wide form (width >= `54`, PEN_LABEL_WIDE): "Notes  <state>  alt+1 2 3 4 5 6  0 off  alt+c colour". Narrow form (otherwise): "Notes <state> alt+123456 0 off alt+c". Wide widths: none 54, red 50, orange 53, yellow 53, green 52, blue 51, violet 53. Narrow widths: none 38, red 34, orange 37, yellow 37, green 36, blue 35, violet 37. The narrow form fits the 39-cell column at 80x24 with at least 1 cell spare. The wide form fits the 58-cell column at 118x30 with at least 4 spare. Both forms name the pen in the chip
module: taskboard/modals.py
examples: (TC-4239) pen `None`, width `58` → label "Notes  pen: none  alt+1 2 3 4 5 6  0 off  alt+c colour", cell_len `54`
examples: (TC-4239) pen `4`, width `58` → label "Notes   blue   alt+1 2 3 4 5 6  0 off  alt+c colour", cell_len `51`; " blue " styled "b #0d1117 on #60a5fa"
examples: (TC-4239) pen `None`, width `39` → label "Notes pen: none alt+123456 0 off alt+c", cell_len `38`
examples: (TC-4239) pen `5`, width `39` → label "Notes  violet  alt+123456 0 off alt+c", cell_len `37`
examples: (TC-4239) pen `0`, width `39` → the spans of "1".."6" carry "#f43f5e", "#fb923c", "#fbbf24", "#4ade80", "#60a5fa", "#a78bfa" (6/6 tone hexes, LLR-4202.10)
examples: (TC-4233) pen `None`, width `39` → label holds "pen: none"

TaskModal._pen_label
req: LLR-4203.9, LLR-4203.4
in:
out: None
func: writes `pen_label(self.pen, self._notes_w)` into `Label #notes-label`. It runs after every write of [Data: TaskModal.pen] (action_pen, _lift_pen, _pen_follow) and from `_fit_width`
module: taskboard/modals.py
modify: [Interface: TaskModal Notes label] (replace)
examples: (TC-4233, root action_pen) pen `None`, _notes_w `39` → the Notes label's plain text "Notes pen: none alt+123456 0 off alt+c"

TaskModal.check_action
req: LLR-4203.10, LLR-4203.7, HLR-4203
in: str action; tuple[object, ...] parameters
out: bool? allowed
func: as at base for `mark`, `drop_move` and `drop_pick`. New arms: `pen` (alt+1..alt+6 and alt+0) is allowed only while `#f-notes` has the focus (LLR-4203.10). `pen_enter` (enter) is allowed only while a pen is on, `#f-notes` has the focus and `check_action("drop_pick")` is False (P-M1-2). In BINDINGS, `drop_pick` comes before `pen_enter` on `enter`, and Textual's `App._check_bindings` tries the bindings of one key in order until one runs. So the picker's pick wins, then the pen, and with neither allowed the key reaches `#f-notes` as a plain new line. Every other action returns `True` (M2 adds its own `colour` arm)
module: taskboard/modals.py
examples: (TC-4240) action "pen", parameters (4,), App.focused `#f-title` → allowed `False`; the key falls to the Input, which inserts nothing for alt+5
examples: (TC-4230) action "pen", parameters (4,), App.focused `#f-notes` → allowed `True`
examples: (TC-4237) action "pen_enter", pen `None`, _mention "list" with no option → allowed `False`; the notes read "@\n" as in test_TC_2503_with_no_one_listed_enter_is_a_new_line
examples: (TC-4237) action "pen_enter", pen `4`, _mention "list" with no option → allowed `True`
examples: (TC-4236) action "drop_pick", pen `4`, _mention `None` → allowed `False`; then action "pen_enter" → allowed `True`
examples: (test_people_picker.py::test_TC_2503_closed_the_arrows_move_the_cursor) action "drop_move", _mention `None` → allowed `False`
examples: (test_marks_manager.py::test_TC_2605_an_empty_directory_composes_no_select) action "mark" with no `#f-mark` → allowed `False`

TaskModal.action_pen
req: LLR-4203.1, LLR-4203.3, LLR-4203.4, LLR-4203.5, LLR-4203.6, HLR-4203
in: int i
out: None
func: `alt+<n>` gives i = n - 1; `alt+0` gives i = -1. Steps: (1) a non-empty selection collapses to its end. (2) If i equals the pen that is on: nothing (P-M1-8). (3) If a pen is on: `_lift_pen()`, which moves the cursor past the closer, or removes the span when it is empty. (4) If i >= 0 and the cursor is inside a Span of `colour_spans(row)` (inner_start <= col <= inner_end): a span of the same code sets pen = i and changes no text; a span of another code, or a legacy span, changes nothing and shows one notify (P-M1-3). (5) Otherwise, if i >= 0: insert "::<code>::  ::" at the cursor, move the cursor to (row, col + 6), and set pen = i. Then `_pen_label()`
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace); [I/O: TextArea #f-notes] (replace)
examples: (TC-4230, root action_pen) notes "", cursor (0, 0), pen `None`, i `4` → notes "::b::  ::", cursor (0, `6`), pen `4`
examples: (TC-4232, root action_pen) notes "::b:: abc ::", cursor (0, 9), pen `4`, i `-1` → notes "::b:: abc ::", cursor (0, `12`), pen `None`; the next `d` gives "::b:: abc ::d"
examples: (TC-4233, root action_pen) notes "::b:: abc ::", cursor (0, 9), pen `4`, i `-1` → pen `None`; label "pen: none"
examples: (TC-4234, root action_pen) notes "::r:: ab ::", cursor (0, 8), pen `0`, i `4` → notes "::r:: ab ::::b::  ::", cursor (0, `17`), pen `4`; the next `x` gives "::r:: ab ::::b:: x ::", segments ("ab", "over"), ("x", "blue")
examples: (TC-4235, root action_pen) notes "x::o::  ::", cursor (0, 7), pen `1`, i `-1` → notes "x", cursor (0, `1`), pen `None`
examples: (TC-4235, root action_pen) notes "::o::  ::", cursor (0, 6), pen `1`, i `4` → notes "::b::  ::", cursor (0, `6`), pen `4`; the next `y` gives "::b:: y ::"
examples: (TC-4248, root action_pen) notes "::b:: ab ::", cursor (0, 8), pen `4`, i `4` → notes "::b:: ab ::", cursor (0, `8`), pen `4`
examples: (TC-4249, root action_pen) notes "::b:: abc ::", cursor (0, 7), pen `None`, i `4` → notes "::b:: abc ::" unchanged, pen `4`
examples: (TC-4249, root action_pen) notes "::r:: abc ::", cursor (0, 7), pen `None`, i `4` → notes unchanged, pen `None`, `1` notify

TaskModal.action_pen_enter
req: LLR-4203.7, HLR-4203
in:
out: None
func: `enter` while a pen is on (gated by check_action). Let s = `_pen_span()` and (row, col) the cursor. If col > s.inner_start: insert " ::\n::<code>:: " at the cursor and move the cursor to (row + 1, 6). The pen's span ends before the line break and the same pen's span opens after it, carrying the text after the cursor. If col == s.inner_start (empty first half, P-M1-9): insert "\n" at (row, s.start) and move the cursor to (row + 1, col - s.start). The whole span moves down, so no empty span stays behind. The pen does not change
module: taskboard/modals.py
modify: [I/O: TextArea #f-notes] (replace)
examples: (TC-4236, root action_pen_enter) notes "::b:: ab ::", cursor (0, 8), pen `4` → notes "::b:: ab ::\n::b::  ::", cursor (1, `6`), pen `4`; typing `cd` then gives "::b:: ab ::\n::b:: cd ::" and both lines tokenise "blue"
examples: (TC-4236, root action_pen_enter) notes "::b:: abcd ::", cursor (0, 8), pen `4` → notes "::b:: ab ::\n::b:: cd ::", cursor (1, `6`)
examples: (TC-4251, root action_pen_enter) notes "x ::b::  ::", cursor (0, 8), pen `4` → notes "x \n::b::  ::", cursor (1, `6`)

TaskModal._pen_span
req: LLR-4203.8, LLR-4203.7
in:
out: Span? span
func: the pen's span that holds the cursor. It returns None when no pen is on, when the selection of `#f-notes` is not empty, or when no Span of `colour_spans(line of the cursor row)` has code PEN_CODES[pen][0] with inner_start <= col <= inner_end. Otherwise it returns the first such span. Proposed as the lookup that `_lift_pen` uses too (P-M1-10)
module: taskboard/modals.py
examples: (TC-4238) notes "::b:: ab ::", cursor (0, 7), pen `4` → span start `0`, inner_start `6`, inner_end `8`, end `11`, code "b"
examples: (TC-4238) notes "::b:: ab ::", cursor (0, 9), pen `4` → span `None`
examples: (TC-4234) notes "::r:: ab ::::b::  ::", cursor (0, 17), pen `4` → span start `11`, inner_start `17`, inner_end `17`, end `20`
examples: (TC-4238) notes "::b:: ab ::", selection (0, 6)-(0, 8), pen `4` → span `None`

TaskModal._pen_follow
req: LLR-4203.8, LLR-4203.2
in:
out: None
func: the cursor-leave check. With a pen on and `_pen_span()` None, it sets pen = None and calls `_pen_label()`. It reads the LIVE cursor, selection and text, never `event.selection`. The editor's own edits (action_pen, action_pen_enter, _lift_pen) post several SelectionChanged before their last `move_cursor`. Each action body runs whole before Textual handles any queued message, so every queued SelectionChanged is judged on the settled state, and the editor's own insert never turns the pen off
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace)
examples: (TC-4230, root on_text_area_selection_changed) after `alt+5` on empty notes, the two queued SelectionChanged (posted at (0, 9) by the insert and at (0, 6) by move_cursor) both read the live cursor (0, `6`) → pen `4`
examples: (TC-4231, root on_text_area_selection_changed) `alt+5`, then typing `abc` → notes "::b:: abc ::", cursor (0, `9`) = inner_end → pen `4`; highlight_segments gives ("abc", "blue")
examples: (TC-4238, root on_text_area_selection_changed) notes "::b:: ab ::", cursor (0, 8), `right` → cursor (0, `9`), pen `None`; the label shows "pen: none"; after `right right right` → pen `None`
examples: (TC-4238, root on_text_area_selection_changed) notes "::b:: ab ::", cursor (0, 8), `left` → cursor (0, `7`), pen `4`
examples: (TC-4238, root on_text_area_selection_changed) `home` → cursor (0, `0`), pen `None`
examples: (TC-4250, root on_text_area_selection_changed) pen `4` on "::b::  ::", typing `std::` → notes "::b:: std:: ::", cursor (0, `11`), span inner_end `9` → pen `None` (P-M1-5)

TaskModal.on_text_area_selection_changed
req: LLR-4203.8
in: TextArea.SelectionChanged event
out: None
func: on a cursor move in `#f-notes` only: as at base (it keeps the preview scrolled to the cursor's line, and re-scans the `@` picker while it lists), plus `_pen_follow()`
module: taskboard/modals.py
modify: [I/O: VerticalScroll #task-preview-scroll] (replace)
examples: (test_people_picker.py::test_TC_2503_closed_the_arrows_move_the_cursor, root on_text_area_selection_changed) `up` with the picker closed → the notes' cursor row goes up by `1`; the drop stays hidden (display `False`)
examples: (TC-4238, root on_text_area_selection_changed) notes "::b:: ab ::", pen `4`, `end` → cursor (0, `11`), pen `None`

TaskModal._save
req: LLR-4203.11, HLR-4203
in:
out: None
func: as at base (title, project, phase, flags, priority, dates, URLs, images, and the class only when the operator changed it; then `dismiss(data)`), with one new first step: `_lift_pen()` when a pen is on. A pen span that holds no inner text is removed before `#f-notes` text is read and stripped. Reached through `alt+s` (`press_button('save')`) and the Save button (on_button_pressed). A click on Save moves the focus but not the cursor, so the pen is still on here
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace); [I/O: TextArea #f-notes] (replace)
examples: (TC-4241, root on_button_pressed) notes "x", `end` → cursor (0, 1), `alt+3` → notes "x::y::  ::", cursor (0, 7), pen `2`; `alt+s` → data notes "x"
examples: (AT-4201, root on_button_pressed) notes "::b:: ask :: now", pen `None` → data notes "::b:: ask :: now"

ink_highlights
req: LLR-4204.1, LLR-4204.2, LLR-4204.4, LLR-4204.5, HLR-4204
in: list[str] lines
out: dict[int, list[tuple[int, int, str]]] highlights
func: the live ink as Textual's highlight map. For each row and each Span of `colour_spans(line)` (legacy spans included, P-M1-1) it adds (b(start), b(inner_start), "pen.mark"), (b(inner_start), b(inner_end), "pen.<tone>") and (b(inner_end), b(end), "pen.mark"), where b(i) = len(line[:i].encode("utf-8")): TextArea highlights are UTF-8 BYTE offsets, not str offsets. Empty ranges are skipped, because an end of 0 reads as "to the line end" in `_render_line`. A row with no span has no key
module: taskboard/modals.py
examples: (TC-4242) lines ["a ::b:: x :: c"] → highlights row `0`: (2, 8, "pen.mark"), (8, 9, "pen.blue"), (9, 12, "pen.mark")
examples: (TC-4246) lines ["é ::b:: café ☕ ::"] → row `0`: (3, 9, "pen.mark"), (9, 18, "pen.blue"), (18, 21, "pen.mark"); the str offsets are 2, 8, 14, 17 (é and ☕ take 2 and 3 bytes)
examples: (TC-4245) lines ["::r:: open"] → row `0`: (0, 6, "pen.mark"), (6, 10, "pen.over"); the open span's empty closer is skipped
examples: (TC-4245) lines ["std::vector", "==late=="] → row `1` only: (0, 2, "pen.mark"), (2, 6, "pen.soon"), (6, 8, "pen.mark")
examples: (TC-4245) over the single-line derived set of LLR-4201.9 → the "pen.<tone>" ranges, decoded back to text, equal in order the non-empty, non-"mut" segments of highlight_segments for 100 % of inputs

InkArea.__init__
req: LLR-4204.6, LLR-4204.1, LLR-4204.2
in: str text; str id
out: None
func: `TextArea.__init__(text, id=id)`, then `register_theme(TextAreaTheme(name="taskboard-ink", syntax_styles=NEW_DICT))` and `theme = "taskboard-ink"`. NEW_DICT is a dict made for this instance: "pen.<tone>" → Style(color=HEX[tone]) for each tone of PEN_CODES (over, orange, soon, green, blue, violet, so the legacy tones are included), and "pen.mark" → Style(color=HEX["dim"]). The theme has no base_style, so the field keeps its CSS colours, cursor and selection as under the `css` theme (`apply_css` fills them). It never writes to `TextAreaTheme.get_builtin_theme("css")` or to any other TextArea
module: taskboard/modals.py
modify: [Data: InkArea theme] (replace)
examples: (TC-4247) text "a ::b:: x :: c", id "f-notes" → `_theme.name` "taskboard-ink"; `_theme.syntax_styles` holds "pen.mark" and "pen.blue"; it is not `TextAreaTheme.get_builtin_theme("css").syntax_styles`
examples: (TC-4247) after the editor mounts → `#f-urls` `_theme.name` "css", with `0` "pen." keys in its syntax_styles; the built-in css theme has `45` keys and `0` "pen." keys, the same as before the mount

InkArea._build_highlight_map
req: LLR-4204.1, LLR-4204.2, LLR-4204.3, HLR-4204
in:
out: None
func: overrides Textual 8.2.8's private `TextArea._build_highlight_map`. With no language, the base method only clears the map. The override clears `_line_cache`, clears `_highlights`, and fills `_highlights` from `ink_highlights(document.lines)`. Textual calls it inside `TextArea.edit` after the change and before it posts `Changed`, and also on undo, redo, load_text and `__init__`, so the next paint already shows the new colours
module: taskboard/modals.py
modify: [Data: InkArea._highlights] (replace); [Data: InkArea._line_cache] (clear)
examples: (TC-4242, root on_mount) notes "a ::b:: x :: c", cursor (0, 0) → the cell at col `8` of `render_line(0)` ("x") has fg "#60a5fa"
examples: (TC-4243, root on_mount) notes "a ::b:: x :: c" → the cells at cols 2, 3, 4, 5, 6, 10 and 11 have fg "#5b6675" (7/7 marker cells)
examples: (TC-4244, root harness) notes "::b:: x ::", cursor (0, 7), key `y` → `_highlights` row `0` holds (6, 8, "pen.blue"); after one pilot.pause() the cell of "y" (col `7`) has fg "#60a5fa"
examples: (TC-4246, root on_mount) notes "é ::b:: café ☕ ::", cursor (0, 17) → cells at cols 8 to 14 ("café ☕", where ☕ fills 13 and 14) have fg "#60a5fa"; the cell at col `0` ("é") is not "#60a5fa"

## Entities

[I/O: TextArea #f-notes]
in: str
desc: CHANGED: `InkArea(t.notes if t else "", id="f-notes")`, a TextArea subclass with its own registered theme "taskboard-ink" and its own highlight map (live ink, LLR-4204). The tcss `#task-box #f-notes { height: 1fr; }` is unchanged. Still no language and no tree-sitter query
sequence:
  alt5Open: TaskModal.check_action → TaskModal.action_pen wins → InkArea._build_highlight_map (inside TextArea.edit, before Changed) → TaskModal.on_text_area_selection_changed (queued at (0, 9), read live as (0, 6)) → TaskModal._pen_follow (pen stays) → TaskModal.on_text_area_changed (preview)
  typeInPen: InkArea._build_highlight_map → TaskModal.on_text_area_selection_changed → TaskModal._pen_follow (cursor = inner_end, pen stays) → TaskModal.on_text_area_changed
  penSwitch: TaskModal.check_action → TaskModal._lift_pen (cursor past the closer of n) → TaskModal.action_pen wins (opens the span of m) → TaskModal._pen_follow (every queued SelectionChanged reads the settled cursor)
  penEnter: TaskModal.check_action (drop_pick False) → TaskModal.check_action (pen_enter True) → TaskModal.action_pen_enter wins → InkArea._build_highlight_map → TaskModal._pen_follow (cursor (row + 1, 6), pen stays)
  leave: TaskModal.on_text_area_selection_changed → TaskModal._pen_follow wins (pen None) → TaskModal._pen_label
  save: TaskModal._save → TaskModal._lift_pen wins (empty span removed) → TaskModal._save (reads and strips the text)

[Data: TaskModal._notes_w]
in: int
desc: the notes column's width in cells, (terminal width - 2) // 2; written by `__init__` (39) and `_fit_width`, read by `_pen_label` to choose the label's form

[Data: InkArea theme]
in: TextAreaTheme
desc: the theme "taskboard-ink" in the InkArea's own `_themes` dict, with a syntax_styles dict made for this instance ("pen.over", "pen.orange", "pen.soon", "pen.green", "pen.blue", "pen.violet", "pen.mark"). `_set_theme` shallow-copies it into `_theme`; the copy shares only this private dict

[Data: TextAreaTheme css]
in: TextAreaTheme
desc: Textual's built-in `css` theme. Its syntax_styles dict IS the `vscode_dark` dict, and every plain TextArea's `_theme` shares that dict through `dataclasses.replace`. Nothing in this group writes it (LLR-4204.6); the prototype's `live_ink` wrote "pen.*" keys into it

[Data: InkArea._highlights]
in: defaultdict[int, list[tuple[int, int | None, str]]]
desc: Textual's private highlight map (byte offsets, name). Written only by `InkArea._build_highlight_map`; read by `TextArea._render_line`, which looks up each name in `_theme.syntax_styles`

[Data: InkArea._line_cache]
in: LRUCache[tuple, Strip]
desc: Textual's private cache of rendered lines. Its key does not hold the highlight map, so every rebuild of the map must clear it

[Interface: TaskModal Notes label]
desc: CHANGED: `Label #notes-label` (classes `task-sec`) above `#f-notes`, filled by `TaskModal._pen_label` with `pen_label(pen, _notes_w)`. Wide form (notes width >= 54, so 118x30) "Notes  <state>  alt+1 2 3 4 5 6  0 off  alt+c colour", 50 to 54 cells. Narrow form "Notes <state> alt+123456 0 off alt+c", 34 to 38 cells, inside the 39-cell column at 80x24. It replaces the base text `==…== yellow · !!…!! red · ++…++ green`, which no test pins
offers: "1" → TaskModal.action_pen
offers: "2" → TaskModal.action_pen
offers: "3" → TaskModal.action_pen
offers: "4" → TaskModal.action_pen
offers: "5" → TaskModal.action_pen
offers: "6" → TaskModal.action_pen
offers: "0 off" → TaskModal.action_pen
offers: "alt+c" → TaskModal.action_colour

[Outside: key alt+1..alt+6]
desc: NEW TaskModal priority bindings `Binding("alt+<n>", "pen(<n-1>)", "", priority=True, show=False)`. They were free everywhere at base. `key_to_character` gives None for them, so the TextArea's `check_consume_key` does not filter them out of the binding chain

[Outside: key alt+0]
desc: NEW TaskModal priority binding `Binding("alt+0", "pen(-1)", "", priority=True, show=False)`. alt+7..alt+9 stay free

[Outside: key enter]
desc: CHANGED: two TaskModal priority bindings, in this order: `drop_pick` (base, modals.py:473) and the NEW `Binding("enter", "pen_enter", "", priority=True, show=False)`. Both are gated by check_action; with neither allowed, the key reaches the focused widget

[Outside: key cursor-move]
desc: `left`, `right`, `home`, `end`, the shift+arrows that make a selection, and a mouse click in `#f-notes`. The TextArea moves its cursor or selection and posts TextArea.SelectionChanged (only when the selection changed). `up` and `down` reach it only while the picker lists nothing (check_action of drop_move)

## Edges

[Data: TaskModal.pen] ──▶ TaskModal.check_action
[Data: TaskModal.pen] ──▶ TaskModal._pen_label
[Data: TaskModal.pen] ──▶ TaskModal._pen_span
[Data: TaskModal.pen] ──▶ TaskModal.action_pen
[Data: TaskModal.pen] ──▶ TaskModal._pen_follow
[Data: TaskModal.pen] ──▶ TaskModal._save
TaskModal.__init__ ──▶ [Data: TaskModal.pen]
TaskModal.action_pen ──▶ [Data: TaskModal.pen]
TaskModal._pen_follow ──▶ [Data: TaskModal.pen]
[Data: PEN_CODES] ──▶ pen_label
[Data: PEN_CODES] ──▶ TaskModal.action_pen
[Data: PEN_CODES] ──▶ TaskModal.action_pen_enter
[Data: PEN_CODES] ──▶ TaskModal._pen_span
[Data: PEN_CODES] ──▶ InkArea.__init__
[Data: views.HEX] ──▶ pen_label
[Data: views.HEX] ──▶ InkArea.__init__
TaskModal.__init__ ──▶ [Data: TaskModal._notes_w]
TaskModal._fit_width ──▶ [Data: TaskModal._notes_w]
[Data: TaskModal._notes_w] ──▶ TaskModal._pen_label
TaskModal._pen_label ──▶ [Interface: TaskModal Notes label]
TaskModal.action_pen ──▶ [I/O: TextArea #f-notes]
TaskModal.action_pen_enter ──▶ [I/O: TextArea #f-notes]
TaskModal._save ──▶ [I/O: TextArea #f-notes]
[I/O: TextArea #f-notes].cursor_location ──▶ TaskModal._pen_span
[I/O: TextArea #f-notes].selection ──▶ TaskModal._pen_span
[I/O: TextArea #f-notes].cursor_location ──▶ TaskModal.action_pen
[I/O: TextArea #f-notes].cursor_location ──▶ TaskModal.action_pen_enter
[I/O: TextArea #f-notes].text ──▶ TaskModal._save
[I/O: TextArea #f-notes].document ──▶ InkArea._build_highlight_map
InkArea.__init__ ──▶ [Data: InkArea theme]
[Data: InkArea theme] ──▶ InkArea._build_highlight_map
InkArea._build_highlight_map ──▶ [Data: InkArea._highlights]
InkArea._build_highlight_map ──▶ [Data: InkArea._line_cache]
[Outside: key alt+1..alt+6] ──▶ TaskModal.check_action
when: TaskModal is the screen; action "pen" is allowed only while App.focused is `#f-notes`
[Outside: key alt+1..alt+6] ──▶ TaskModal.action_pen
when: check_action("pen") is True; i = n - 1
[Outside: key alt+0] ──▶ TaskModal.check_action
when: TaskModal is the screen; same gate as alt+1..alt+6
[Outside: key alt+0] ──▶ TaskModal.action_pen
when: check_action("pen") is True; i = -1 (no pen on: nothing changes)
[Outside: key enter] ──▶ TaskModal.check_action
when: TaskModal is the screen; drop_pick first, then pen_enter
[Outside: key enter] ──▶ TaskModal.action_pen_enter
when: check_action("drop_pick") is False, a pen is on, and App.focused is `#f-notes`
[Outside: key printable] ──▶ InkArea._build_highlight_map
when: App.focused is `#f-notes`; TextArea.edit rebuilds the map before it posts Changed
[Outside: key printable] ──▶ TaskModal.on_text_area_selection_changed
when: App.focused is `#f-notes`; the insert moves the cursor by one
[Outside: key cursor-move] ──▶ TaskModal.on_text_area_selection_changed
when: App.focused is `#f-notes` and the selection changed
[Outside: key alt+s] ──▶ TaskModal._save
when: TaskModal is the screen; press_button('save') → on_button_pressed

## Findings

finding P-M1-1 the live ink's scope: colour spans only, or every span
anchor: ink_highlights
seen: LLR-4204.1 and LLR-4204.2 say "colour span" (`::c::` only, by the definitions), while LLR-4204.4 says "exactly the character ranges `highlight_segments` gives", which include the legacy spans `==…==`, `!!…!!`, `++…++`
cause: the requirements were written from the `::` syntax, but the tokeniser they reference reads both kinds
effect: with colour spans only, TC-4245 fails on "==late==" (the tokeniser gives "late" in soon, the ink gives nothing); with every span, LLR-4204.1 and .2 are silent on legacy markers
decision: proposal: the ink paints every Span of colour_spans, legacy ones included (inner text in its tone, markers dim), the same as the preview. Amend LLR-4204.1 and LLR-4204.2 from "colour span" to "span". The graph does this now

finding P-M1-2 the gate for pen-enter: "mention picker closed" is the wrong condition
anchor: TaskModal.check_action
seen: LLR-4203.7 says "while a pen is on and the mention picker is closed". With an empty directory and `@` typed (the state of test_TC_2503_with_no_one_listed_enter_is_a_new_line) the picker is open (`_mention` "list", "type a name") but drop_pick is denied
cause: the requirement names the picker's display state; the real question is whether drop_pick takes the key
effect: under the literal text, enter under a pen with an empty list is a plain new line: "::b:: @\n ::", and line 2 shows " ::" as literal text, which is the flaw LLR-4203.7 exists to fix
decision: proposal: amend LLR-4203.7 to "while a pen is on and the mention picker offers no pick" (check_action("drop_pick") is False). The graph gates pen_enter this way. TC-2503 stays green (no pen there, so pen_enter is denied)

finding P-M1-3 alt+n with no pen while the cursor is inside a span, or with a selection
anchor: TaskModal.action_pen
seen: LLR-4203.1 inserts "::<code>::  ::" at the cursor whatever is there. Inside "::r:: abc ::" at (0, 7) that gives "::r:: a::b::  ::bc ::": red ends at the opener (LLR-4201.6), and "bc ::" shows as literal text. With a selection, the insert leaves the selection standing
cause: the requirement assumes the cursor is in plain text
effect: one key press corrupts a span the user typed earlier
decision: proposal: inside a span of the same code, set the pen on with no edit (the user re-enters the pen); inside a span of another code or a legacy span, change nothing and show one notify ("alt+c recolours a span"); a non-empty selection collapses to its end first. TC-4249 pins this. Needs an LLR (4203.12) if accepted

finding P-M1-4 leaving an empty pen span by the cursor leaves it in the notes, and save keeps it
anchor: TaskModal._pen_follow
seen: `alt+3`, then `right` (or a click) at once: LLR-4203.8 turns the pen off, and "::y::  ::" stays in the text. LLR-4203.6 covers only a lift (alt+0, alt+n, alt+c), and LLR-4203.11 only a pen that is on at save
cause: the definition of "lift" does not include the cursor leaving
effect: an empty span that renders nothing is saved: "x::y::  ::"
decision: proposal A (recommended): `_pen_follow` removes an empty pen span when the pen turns off, and moves the cursor left by the span's length when the cursor is after it on the same row; amend LLR-4203.6 to "lifted or left". Proposal B: the save path strips every empty colour span (it can touch text typed by hand). The graph follows the requirements as written until a decision is made

finding P-M1-5 typing `::` under a pen ends the span
anchor: TaskModal._pen_follow
seen: pen `b` on "::b::  ::", typing `std::` gives "::b:: std:: ::". The first `::` after the inner start is the closer, so the inner text is "std" and the cursor (0, 11) is past inner_end 9, and the pen turns off. The old closer " ::" stays as literal `mut` text
cause: `::` is both the closer and ordinary text (C++ scopes, times), and notes are plain text with no escape
effect: LLR-4203.2 ("each typed character inside that pen's span") cannot hold for `::`
decision: proposal: accept the limitation, with no escape syntax in this increment; amend LLR-4203.2 to "each typed character, except a `:` that completes `::`"; TC-4250 pins the result

finding P-M1-6 the notes column is 39 cells at 80x24, not 37
anchor: pen_label
seen: taskboard.tcss: `#task-box` padding `0 1`, then `#task-edit` and `#task-prev` both `1fr`, so (80 - 2) // 2 = 39. The prototype's label clipped `off` at cell 39 (out/png/col-B-ed_80x24.png)
cause: the brief estimated "about 37"
effect: the widest narrow form ("Notes pen: none alt+123456 0 off alt+c") is 38 cells: it fits 39 with 1 spare cell, but not 37. Below 78 terminal columns the narrow form clips "alt+c" first
decision: proposal: keep the forms; the cut is notes width >= 54 for the wide form; TC-4239 asserts 0 clipped glyphs at 80x24 and 118x30 (7 states × 2 sizes); record 78 columns as the floor of LLR-4203.9

finding P-M1-7 the live ink depends on three private Textual internals
anchor: InkArea._build_highlight_map
seen: the override uses `_build_highlight_map`, `_highlights` (byte offsets; an end of 0 reads as "to the line end") and `_line_cache`. pyproject.toml declares `textual` without a version; only requirements.txt pins 8.2.8
cause: Textual has no public API for a custom highlighter without tree-sitter
effect: a Textual upgrade can rename these, and the ink then fails without an error (no colours) or raises
decision: proposal: accept, with guards: TC-4242 and TC-4244 fail when the override is no longer called, and a layer-0 test checks that `TextArea.edit` calls `_build_highlight_map` and that `_highlights` is a dict. Pin `textual==8.2.8` in pyproject (a separate decision; not in this slice)

finding P-M1-8 the same pen key while that pen is on
anchor: TaskModal.action_pen
seen: LLR-4203.5 covers alt+m with pen n ≠ m; nothing covers m = n
cause: gap in the requirement
effect: the literal lift-then-open rule would close the span and open an empty one after it, which LLR-4203.6 would then remove on the next lift
decision: proposal: alt+n while pen n is on does nothing (TC-4248)

finding P-M1-9 enter at the start of the pen's inner text
anchor: TaskModal.action_pen_enter
seen: the literal LLR-4203.7 on "::b::  ::" at (0, 6) gives "::b::  ::\n::b::  ::": an empty span stays on line 1, and LLR-4203.11 cannot remove it (it is not the pen's span any more)
cause: the requirement splits at the cursor without the empty case
effect: an empty span is saved
decision: proposal: when the first half is empty, insert the line break before the span's opener, so the whole span moves down (TC-4251); the example of LLR-4203.7 is unchanged

finding P-M1-10 proposal for the `_lift_pen` contract: no span holds the cursor
anchor: TaskModal._lift_pen
seen: graph-interfaces says `_lift_pen` "finds the span holding the cursor whose code is the pen's", but not what happens when there is none (for example M2's action_colour after a click that `_pen_follow` has not handled yet, or a closer deleted by hand)
cause: the contract is silent
effect: an implementation can raise or move the cursor by mistake
decision: proposal: add to the func of `_lift_pen`: "no such span: set the pen to None and refresh the label, leaving text and cursor unchanged"; and use `TaskModal._pen_span` for the lookup, with the selection test dropped (M2 calls it with a selection standing). Example: (TC-4253) notes "abc", cursor (0, 1), pen `4` → notes "abc", cursor (0, 1), pen `None`

### Seams
> Consumed from group V (views.py): `colour_spans(text) -> list[Span]` (str offsets, one line) in `_pen_span`, `action_pen` (the inside-a-span test) and `ink_highlights`; `[Data: PEN_CODES]` (code, tone, name in pen order) in `pen_label`, `action_pen`, `action_pen_enter`, `_pen_span` and `InkArea.__init__`; `[Data: Span]` (start, inner_start, inner_end, end, tone, code; code None for a legacy span) in `_pen_span`, `action_pen_enter` and `ink_highlights`; `highlight_segments` only as the oracle of TC-4231 and TC-4245; `views.HEX` must hold "orange", "blue" and "violet" (it already does) and "dim" `#5b6675`.
> Offered to group M2 (palette): `TaskModal._lift_pen()` (the contract in graph-interfaces, plus P-M1-10), which M2's `action_colour` calls before it computes the target (LLR-4205.14); `[Data: TaskModal.pen]` (read only); the Notes label, which already shows "alt+c" (narrow form) and "alt+c colour" (wide form), offered to `TaskModal.action_colour`, so M2 must not add another listing of alt+c in the editor. M2 adds its own `colour` arm to `TaskModal.check_action` and its own `alt+c` binding; the M1 arms (`pen`, `pen_enter`) do not read `colour`. M2's palette rewrites go through `TextArea.replace`, so the ink is rebuilt for them by `InkArea._build_highlight_map` with no call from M2.
> Shared file: modals.py. M1 changes TaskModal.__init__, compose, _fit_width, check_action, on_text_area_selection_changed and _save, and adds pen_label, ink_highlights, InkArea, action_pen, action_pen_enter, _pen_span, _pen_follow and _pen_label.
