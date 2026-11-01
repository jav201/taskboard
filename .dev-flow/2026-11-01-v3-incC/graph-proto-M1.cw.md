# Code-Wire prototype — group M1: TaskModal pens and live ink (Inc C, E2)

Differences from `graph-baseline.cw.md` only. Changed nodes carry their full contract; new nodes are marked by `req:` ids of HLR-4203 / HLR-4204 / LLR-4202.10. Shared seams (`colour_spans`, `highlight_segments`, `TaskModal._lift_pen`, `TaskModal._pen_span`, `TaskModal.check_action`, `[Data: PEN_CODES]`, `[Data: Span]`, `[Data: TaskModal.pen]`) are defined in `graph-interfaces.cw.md` and are not repeated here. Pen index i is 0..5 into PEN_CODES (r o y g b v), so `alt+5` is pen `4` (`b`, tone `blue`, `#60a5fa`).

Unchanged on purpose: `TaskModal.on_text_area_changed` (the ink is rebuilt inside `TextArea.edit`, before `Changed` is posted, so the handler needs no ink call; a forward `delete` can only extend a span, never move the cursor out of it, so it needs no leave-check either). `notes_preview` and `#task-preview` are unchanged.

Notes column widths (taskboard.tcss: `#task-box` padding `0 1`, `#task-edit` and `#task-prev` both `1fr`): notes width = (terminal width - 2) // 2, so `39` at 80x24 and `58` at 118x30.

Textual 8.2.8 internals relied on (read in `textual/widgets/_text_area.py` and `textual/_text_area_theme.py`): the private `TextArea._build_highlight_map` (called by `edit()` line 1700 after the change and before `Changed` is posted, by undo/redo lines 1765 and 1814, and by `_set_document` line 1184 during `__init__` and `load_text`); the private `TextArea._highlights` (`defaultdict[int, list[(start_byte, end_byte | None, name)]]`), which `_render_line` (lines 1494-1508) maps from UTF-8 bytes to code points with `build_byte_to_codepoint_dict`, and where an end of `0` is read as `None`, meaning "to the line end"; the private `TextArea._line_cache` (its cache key has the theme name but not the highlight map, so the override must clear it). Public API: `TextArea.register_theme` (it writes the per-instance `_themes` dict), the `theme` reactive, and `TextAreaTheme(name, syntax_styles)` (exported as `textual.widgets.text_area.TextAreaTheme`). Why the prototype leaked: `_set_theme` stores `dataclasses.replace(theme_object)`, which is a shallow copy, so `ta._theme.syntax_styles` IS the dict of the built-in theme. The built-in `css` theme is `TextAreaTheme(name="css", syntax_styles=_DARK_VS.syntax_styles)`, so writing to that dict changes every TextArea on every screen and the `vscode_dark` theme too. Probe on 8.2.8: `get_builtin_theme("css").syntax_styles is get_builtin_theme("vscode_dark").syntax_styles` → True; `dataclasses.replace(css).syntax_styles is css.syntax_styles` → True. `_app_theme_changed` runs `_set_theme(self._theme.name)` again, so a registered theme survives a change of app theme, but a direct mutation of `_theme` would be lost (after it had already leaked).

## Nodes

_unshadow_alt_digits
req: LLR-4203.16, HLR-4203
in:
out: None
func: NEW, module level in modals.py, run once at import (ARCH-1). For k in "\x1b0", "\x1b1", …, "\x1b6" (seven keys): `textual._ansi_sequences.ANSI_SEQUENCES_KEYS.pop(k, None)`. Those entries exist only to turn WezTerm-on-macOS Option+digit into glyphs (`"\x1b5": "∞"`, `"\x1b0": "º"`, `_ansi_sequences.py:384-394`); without them `ESC <digit>` takes the XTermParser's generic alt path, as `ESC s` already does for `alt+s`. Idempotent (`pop(k, None)`: a second import or call changes nothing and raises nothing). `"\x1b7"`..`"\x1b9"` and every other entry stay. Trade-off (ruling): a macOS WezTerm user's Option+digit no longer types its glyph
module: taskboard/modals.py
modify: [Outside: textual ANSI_SEQUENCES_KEYS] (delete)
examples: (TC-4249) after `import taskboard.modals`: `p = XTermParser()`, `list(p.feed("\x1b5")) + list(p.feed(""))` → one Key, key "alt+5", character "5" (executed on Textual 8.2.8 with the seven pops; base gives key "infinity", character "∞")
examples: (TC-4249) after the import: feeding "\x1b0" → key "alt+0", character "0"; feeding "\x1b1" → key "alt+1", character "1" (2/2 + the alt+5 arm; NC base table: RED)
examples: (TC-4249) after the import: feeding "\x1b7" → key "pilcrow_sign", character "¶" (left as at base); feeding "\x1bs" → key "alt+s", character "s" (unchanged)
examples: (TC-4249) `_unshadow_alt_digits()` called a second time → no exception; ANSI_SEQUENCES_KEYS byte-equal to after the first call

TaskModal.__init__
req: LLR-4203.4, HLR-4203
in: Board board; Task? task = None; Directory? people = None; object? marks = None
out: None
func: as at base (board, task, people, marks, mention picker state, image key), plus `self.pen = None` (no pen on when the editor opens) and `self._pen_at = None`
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace); [Data: TaskModal._pen_at] (replace)
examples: (TC-4233) board with one task, task that task → pen `None`, _pen_at `None`

TaskModal.compose
req: LLR-4203.9, LLR-4204.1, LLR-4204.6, HLR-4204
in:
out: ComposeResult widgets
func: as at base, with two changes inside `#task-edit`. (1) The Notes label is `Label(pen_label(self.pen), id="notes-label", classes="task-sec")` (one form, no width input: ARCH-7; `_pen_label` rewrites it after each pen write). (2) `#f-notes` is `InkArea(t.notes if t else "", id="f-notes")`, a TextArea subclass, so `query_one("#f-notes", TextArea)` and the `#task-box #f-notes` tcss rule still match. `#f-urls` and `#f-images` stay plain `TextArea`
module: taskboard/modals.py
examples: (TC-4247) task with notes "a ::b:: x :: c" → `#f-notes` is an InkArea and a TextArea; `#f-urls` and `#f-images` are of type TextArea, not InkArea
examples: (test_edit_window.py::test_the_editor_paints_its_keys_in_full) any task → the Preview label is unchanged: "ctrl+v paste · esc cancel"

pen_label
req: LLR-4203.9, LLR-4202.10, LLR-4203.4
in: int? pen
out: Text label
func: the editor's Notes label as Text pieces, never markup (C-17). ONE form (ARCH-7): "Notes <state> alt+123456 0 off alt+c". Pieces: `Notes` in `#8b98a5`; the state, which is `pen: none` in `mut` with no pen, or the chip " <name> " in `b #0d1117 on HEX[tone]`; the keys `1`..`6`, each bold in HEX[tone] of PEN_CODES; `0 off`; and `alt+c` in bold `bright`. Widths: none 38, red 34, orange 37, yellow 37, green 36, blue 35, violet 37, so it fits the 39-cell notes column at 80x24 (≥ 1 cell spare) and the 58-cell column at 118x30, and the chip names the pen at both sizes (LLR-4203.9)
module: taskboard/modals.py
examples: (TC-4239) pen `None` → label "Notes pen: none alt+123456 0 off alt+c", cell_len `38`
examples: (TC-4239) pen `4` → label "Notes  blue  alt+123456 0 off alt+c", cell_len `35`; " blue " styled "b #0d1117 on #60a5fa"
examples: (TC-4239) pen `5` → label "Notes  violet  alt+123456 0 off alt+c", cell_len `37`
examples: (TC-4239) pen `0` → the spans of "1".."6" carry "#f43f5e", "#fb923c", "#fbbf24", "#4ade80", "#60a5fa", "#a78bfa" (6/6 tone hexes, LLR-4202.10)
examples: (TC-4239, root compose) the editor at 80x24 and at 118x30, each of the 7 pen states → the Notes label's visible cells hold "1".."6", "0", "alt+c" and the state, 0 clipped key glyphs (14/14)
examples: (TC-4233) pen `None` → label holds "pen: none"

TaskModal._pen_label
req: LLR-4203.9, LLR-4203.4
in:
out: None
func: writes `pen_label(self.pen)` into `Label #notes-label`. It runs after every write of [Data: TaskModal.pen] (action_pen, _lift_pen, _pen_follow); compose writes the first label (no `_fit_width` hook, no resize dependency: ARCH-7)
module: taskboard/modals.py
modify: [Interface: TaskModal Notes label] (replace)
examples: (TC-4233, root action_pen) pen `None` → the Notes label's plain text "Notes pen: none alt+123456 0 off alt+c"

TaskModal.action_pen
req: LLR-4203.1, LLR-4203.3, LLR-4203.4, LLR-4203.5, LLR-4203.6, LLR-4203.10, LLR-4203.12, LLR-4203.13, LLR-4203.15, LLR-4203.17, HLR-4203
in: int i
out: None
func: `alt+<n>` gives i = n - 1; `alt+0` gives i = -1. Steps, in order: (0) If `#f-notes` does not have the focus: return at once; the key is consumed (check_action allows `pen` always, ARCH-2) and no field, pen or label changes (LLR-4203.10). (1) If i equals the pen that is on: change nothing, no text, cursor or pen (LLR-4203.15). (2) If no pen is on and i >= 0, and either the selection of `#f-notes` is not empty (LLR-4203.13) or the cursor is inside a Span of `colour_spans(row)` with start < col < end (LLR-4203.12, colour and legacy spans alike): insert nothing, keep pen `None`, keep the selection, and call `notify("Pens write new text — use alt+c to recolour.")` once; stop. A cursor at col == start or col == end is outside the span. (3) If a pen is on: `_lift_pen()`, which moves the cursor past the closer, or removes the span when it is empty. (4) If i >= 0: let line be the cursor row and new_line = line[:col] + "::<code>::  ::" + line[col:]. The visible-text check (SEC-2, LLR-4203.17, the same invariant as M2's `_apply_colour`): if `"".join(seg for seg, _ in highlight_segments(new_line)) != "".join(seg for seg, _ in highlight_segments(line))` (the pair adds no visible character when it parses as one empty span, so the two must be equal), insert nothing, keep pen `None`, and call `notify("That colour would change the text you see: nothing changed.", severity="warning", markup=False)` (N4) once; stop. Else insert the pair at the cursor, move the cursor to (row, col + 6), set pen = i and `_pen_at = (row, col)` (ARCH-8: set by the action itself, so a next key that overtakes the queued SelectionChanged still finds the span). Then `_pen_label()`. alt+0 with no pen on changes nothing
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace); [Data: TaskModal._pen_at] (replace); [I/O: TextArea #f-notes] (replace); [I/O: notifications] (append)
examples: (TC-4240, root action_pen) focus on `#f-title`, title "T", notes "n"; post `events.Key("alt+5", "5")` (the terminal's event, not pilot.press) → title "T" and notes "n" byte-equal, pen `None`, `0` notify (ARCH-2, LLR-4203.10)
examples: (TC-4240, root action_pen) focus on `#f-title`, title "T", notes "n"; post `events.Key("alt+0", "0")` → title "T" and notes "n" byte-equal (NC: a denied check_action lets the Input type "0" → "T0": RED)
examples: (TC-4230, root action_pen) notes "", cursor (0, 0), pen `None`, i `4` → notes "::b::  ::", cursor (0, `6`), pen `4`, _pen_at (0, `0`)
examples: (TC-4252, root action_pen) notes "b:: x", cursor (0, 0), pen `None`, i `0` → notes "b:: x" byte-equal, pen `None`, `1` notify "That colour would change the text you see: nothing changed." ("::r::  ::b:: x" would show " x": the user's `b::` would become an opener; SEC-2, LLR-4203.17)
examples: (TC-4252, root action_pen) notes "C::b", cursor (0, 4), pen `None`, i `0` → notes "C::b" byte-equal, pen `None`, `1` notify N4 ("C::b::r::  ::" would show "Cr  ::")
examples: (TC-4252, root action_pen) notes "note y::", cursor (0, 5), pen `None`, i `0` → notes byte-equal, `1` notify N4 (the pair's `::` + "y::" would form an opener)
examples: (TC-4232, root action_pen) notes "::b:: abc ::", cursor (0, 9), pen `4`, i `-1` → notes "::b:: abc ::", cursor (0, `12`), pen `None`; the next `d` gives "::b:: abc ::d"
examples: (TC-4233, root action_pen) notes "::b:: abc ::", cursor (0, 9), pen `4`, i `-1` → pen `None`; label "pen: none"
examples: (TC-4234, root action_pen) notes "::r:: ab ::", cursor (0, 8), pen `0`, i `4` → notes "::r:: ab ::::b::  ::", cursor (0, `17`), pen `4`; the next `x` gives "::r:: ab ::::b:: x ::", segments ("ab", "over"), ("x", "blue")
examples: (TC-4235, root action_pen) notes "x::o::  ::", cursor (0, 7), pen `1`, i `-1` → notes "x", cursor (0, `1`), pen `None`
examples: (TC-4235, root action_pen) notes "::o::  ::", cursor (0, 6), pen `1`, i `4` → notes "::b::  ::", cursor (0, `6`), pen `4`; the next `y` gives "::b:: y ::"
examples: (TC-4248, root action_pen) notes "::b:: ab ::", cursor (0, 8), pen `4`, i `4` → notes "::b:: ab ::", cursor (0, `8`), pen `4`
examples: (TC-4255, root action_pen) `alt+5`, type `ab`, `alt+5` → notes "::b:: ab ::", cursor (0, `8`), pen `4`, `0` notify (LLR-4203.15)
examples: (TC-4252, root action_pen) notes "::r:: ab ::", cursor (0, 7), pen `None`, i `4` → notes "::r:: ab ::" byte-equal, cursor (0, `7`), pen `None`, `1` notify "Pens write new text — use alt+c to recolour." (LLR-4203.12)
examples: (TC-4252, root action_pen) notes "::b:: abc ::", cursor (0, 7), pen `None`, i `4` → notes byte-equal, pen `None`, `1` notify: the same code does not turn the pen on (no "continue in span", P-M1-3)
examples: (TC-4252, root action_pen) notes "==late==", cursor (0, 1), pen `None`, i `4` → notes byte-equal, pen `None`, `1` notify (a legacy span; col 1 lies inside its opener, start `0` < 1 < end `8`)
examples: (TC-4252, root action_pen) notes "::r:: ab ::", cursor (0, 11) = end, pen `None`, i `4` → notes "::r:: ab ::::b::  ::", cursor (0, `17`), pen `4`, `0` notify (col == end is outside)
examples: (TC-4254, root action_pen) notes "the plan works", selection (0, 4)-(0, 8) ("plan"), pen `None`, i `4` → notes byte-equal, selection (0, 4)-(0, `8`), pen `None`, `1` notify "Pens write new text — use alt+c to recolour." (LLR-4203.13)
examples: (TC-4254, root action_pen) notes "the plan works", selection (0, 4)-(0, 8), pen `None`, i `-1` → notes byte-equal, `0` notify (alt+0 with no pen on)

TaskModal.action_pen_enter
req: LLR-4203.7, HLR-4203
in:
out: None
func: `enter` while a pen is on (gated by check_action, which also requires `_pen_span()` is not None: ARCH-8). Let (row, col) be the cursor, inside the pen's span. Insert " ::\n::<code>:: " at the cursor and move the cursor to (row + 1, 6), and set `_pen_at = (row + 1, 0)` (ARCH-8: the new span's start, written by the action itself). The pen's span ends before the line break and the same pen's span opens after it, carrying the text after the cursor. One path for every col, col == inner_start included (no special case: P-M1-9 rejected). The pen does not change
module: taskboard/modals.py
modify: [I/O: TextArea #f-notes] (replace); [Data: TaskModal._pen_at] (replace)
examples: (TC-4236, root action_pen_enter) notes "::b:: ab ::", cursor (0, 8), pen `4` → notes "::b:: ab ::\n::b::  ::", cursor (1, `6`), pen `4`, _pen_at (1, `0`); typing `cd` then gives "::b:: ab ::\n::b:: cd ::" and both lines tokenise "blue"
examples: (TC-4236, root action_pen_enter) notes "::b:: ab ::", cursor (0, 8), pen `4`; `enter` then `home` handled before any queued SelectionChanged → `_pen_follow` finds _pen_at (1, 0) holding the empty span "::b::  ::" → notes "::b:: ab ::\n", cursor (1, `0`), pen `None` (LLR-4203.14 holds under the race, ARCH-8)
examples: (TC-4236, root action_pen_enter) notes "::b:: abcd ::", cursor (0, 8), pen `4` → notes "::b:: ab ::\n::b:: cd ::", cursor (1, `6`)

TaskModal._pen_follow
req: LLR-4203.8, LLR-4203.2, LLR-4203.14
in:
out: None
func: the cursor-leave check, with a pen on (no pen: nothing). Let s = `_pen_span()`. If s is not None, the cursor is in the pen's span: store `_pen_at = (row, s.start)` and stop. If s is None, the cursor has left: (a) LLR-4203.14: only if `_pen_at` is not None and row `_pen_at[0]` still holds a Span of `colour_spans` with start `_pen_at[1]`, the pen's code and inner_start == inner_end (SEC-4: `_pen_at` was written for THIS pen by action_pen, action_pen_enter or this handler, and is None after any lift, so it cannot point at an older pen's span), delete line[start:end] of that row and move the cursor explicitly (no reliance on TextArea's own shift): on another row it stays; on the same row, col < start stays, start <= col <= end (the cursor stands on the span's own markers, for example after one `right` from the inner start, or `end` right after the closer) goes to start, and col > end moves left by end - start; a selection collapses to that cursor. Because leaving puts the cursor outside the inner text, it never ends inside the removed text. (b) set pen = None, set `_pen_at = None` (SEC-4) and call `_pen_label()`. The delete posts one more SelectionChanged, which finds the pen None and does nothing. A span that is not empty stays as typed. It reads the LIVE cursor, selection and text, never `event.selection`. The editor's own edits (action_pen, action_pen_enter, _lift_pen) post several SelectionChanged before their last `move_cursor`. Each action body runs whole before Textual handles the action's own queued messages, so those are judged on the settled state, and the editor's own insert never turns the pen off. The NEXT key can overtake them (the insert's SelectionChanged bubbles through `#task-edit`, `#task-split`, `#task-box`, while a `home` is handled by the TextArea in one hop: ARCH-8); that is safe because action_pen and action_pen_enter write `_pen_at` themselves, so the first `_pen_follow` that runs finds the empty span either way
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace); [Data: TaskModal._pen_at] (replace); [I/O: TextArea #f-notes] (replace)
examples: (TC-4230, root on_text_area_selection_changed) after `alt+5` on empty notes, the two queued SelectionChanged (posted at (0, 9) by the insert and at (0, 6) by move_cursor) both read the live cursor (0, `6`) → pen `4`
examples: (TC-4231, root on_text_area_selection_changed) `alt+5`, then typing `abc` → notes "::b:: abc ::", cursor (0, `9`) = inner_end → pen `4`; highlight_segments gives ("abc", "blue")
examples: (TC-4238, root on_text_area_selection_changed) notes "::b:: ab ::", cursor (0, 8), `right` → cursor (0, `9`), pen `None`; the label shows "pen: none"; after `right right right` → pen `None`
examples: (TC-4238, root on_text_area_selection_changed) notes "::b:: ab ::", cursor (0, 8), `left` → cursor (0, `7`), pen `4`
examples: (TC-4238, root on_text_area_selection_changed) `home` → cursor (0, `0`), pen `None`
examples: (TC-4250, root on_text_area_selection_changed) pen `4` on "::b::  ::", typing `std::` → notes "::b:: std:: ::", cursor (0, `11`), span inner_end `9` → pen `None` (P-M1-5)
examples: (TC-4250, root on_text_area_selection_changed) pen `4` on "::b::  ::", cursor (0, 6), typing `:` `:` → the typed `::` is the closer of an empty span 0..8, the cursor (0, 8) is past it, the span is removed → notes " ::", cursor (0, `0`), pen `None` (ARCH-13: the two typed colons are eaten; pinned, README sentence in graph V)
examples: (TC-4256, root on_text_area_selection_changed) notes "x", `end`, `alt+3` → notes "x::y::  ::", cursor (0, 7), pen `2`, _pen_at (0, `1`) written by action_pen; `home` → cursor (0, 0) before the span → notes "x", cursor (0, `0`), pen `None`, _pen_at `None` (LLR-4203.14)
examples: (TC-4256, root on_text_area_selection_changed) notes "x", `end`, then `alt+3` and `home` in one `press()` so that `home` is handled before the insert's queued SelectionChanged → notes "x", cursor (0, `0`), pen `None` (ARCH-8: _pen_at came from action_pen, not from a prior _pen_follow)
examples: (TC-4257, root on_text_area_selection_changed) notes "::y::  ::", pen `None`, _pen_at `None` (a pen lifted earlier); `alt+3` at (0, 9) → notes "::y::  ::::y::  ::", _pen_at (0, `9`); `home` → only the span at 9 is removed: notes "::y::  ::", cursor (0, `0`), pen `None` (SEC-4: the older empty span at 0 is not touched)
examples: (TC-4256, root on_text_area_selection_changed) notes "::y::  ::", cursor (0, 6), pen `2`, `right` → cursor (0, 7) on the closer's space → notes "", cursor (0, `0`), pen `None`
examples: (TC-4257, root on_text_area_selection_changed) notes "x::y::  ::z", cursor (0, 7), pen `2`, `end` → cursor (0, 11), after the span on the same row → notes "xz", cursor (0, `2`) (11 - 9), pen `None`
examples: (TC-4257, root on_text_area_selection_changed) notes "a\n::y::  ::", cursor (1, 6), pen `2`, `up` → cursor (0, 1) on another row → notes "a\n", cursor (0, `1`), pen `None`
examples: (TC-4257, root on_text_area_selection_changed) notes "::y:: ab ::", cursor (0, 8), pen `2`, `home` → notes "::y:: ab ::" byte-equal (not empty), cursor (0, `0`), pen `None`

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
req: LLR-4204.1, LLR-4204.2, LLR-4204.4, LLR-4204.5, LLR-4204.7, LLR-4204.9, HLR-4204
in: list[str] lines
out: dict[int, list[tuple[int, int, str]]] highlights
func: the live ink as Textual's highlight map. For each row and each Span of `colour_spans(line)` (legacy spans included, P-M1-1) it adds (b(start), b(inner_start), "pen.mark"), (b(inner_start), b(inner_end), "pen.<tone>") and (b(inner_end), b(end), "pen.mark"), where b(i) is the UTF-8 BYTE offset of str index i: TextArea highlights are byte offsets, not str offsets. b is built in ONE pass per line (SEC-1, LLR-4204.7): b(i) = i when `line.isascii()`; otherwise a prefix table cum[0] = 0, cum[k+1] = cum[k] + len(line[k].encode("utf-8", "surrogatepass")), computed once and indexed per offset (never `line[:i].encode()` per offset, which is quadratic). `surrogatepass` (SEC-6, LLR-4204.9): a lone surrogate counts its 3 bytes and never raises here. Empty ranges are skipped, because an end of 0 reads as "to the line end" in `_render_line`. A row with no span has no key. Linear in the total text length (colour_spans is linear, LLR-4201.10)
module: taskboard/modals.py
examples: (TC-4242) lines ["a ::b:: x :: c"] → highlights row `0`: (2, 8, "pen.mark"), (8, 9, "pen.blue"), (9, 12, "pen.mark")
examples: (TC-4246) lines ["é ::b:: café ☕ ::"] → row `0`: (3, 9, "pen.mark"), (9, 18, "pen.blue"), (18, 21, "pen.mark"); the str offsets are 2, 8, 14, 17 (é and ☕ take 2 and 3 bytes)
examples: (TC-4246) lines ["\ud800 ::b:: x ::"] → row `0`: (4, 10, "pen.mark"), (10, 11, "pen.blue"), (11, 14, "pen.mark"); no exception (the lone surrogate counts 3 bytes; str offsets 2, 8, 9, 12; executed in a scratch reference) (SEC-6, LLR-4204.9; NC strict `encode("utf-8")`: UnicodeEncodeError, RED)
examples: (TC-4246) lines ["::b:: x ::" × 10 000] (100 000 chars, 10 000 spans) and lines ["::b:: é ::" × 10 000] → each builds in ≤ `250` ms and t(100k) / t(10k) ≤ `20` (LLR-4204.7; scratch reference, executed: 19.6 ms ratio 11.1, and 28.0 ms ratio 10.8; NC per-offset `line[:i].encode()`: 1 103 ms on 100k chars, RED)
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
req: LLR-4204.1, LLR-4204.2, LLR-4204.3, LLR-4204.8, LLR-4204.9, HLR-4204
in:
out: None
func: overrides Textual 8.2.8's private `TextArea._build_highlight_map`. With no language, the base method only clears `_line_cache` and `_highlights`. The override, fail-safe (SEC-3, LLR-4204.8): inside `try`: new = `ink_highlights(document.lines)`; if the text holds a lone surrogate (`not text.isascii()` and `text.encode("utf-8")` raises UnicodeEncodeError), new = {} (SEC-6: Textual's own `_render_line` encodes EVERY visible line strictly as soon as `_highlights` is non-empty, so any ink on such a document makes every paint raise; probe executed on 8.2.8: a highlight on row 1 makes `render_line(0)` of "\ud800 ::b:: x ::" raise UnicodeEncodeError); then `super()._build_highlight_map()` (clears the cache and the map) and `_highlights.update(new)`. `except Exception`: `super()._build_highlight_map()` only, so the field shows plain text with no ink and keeps working (the base method uses its own private names, so a renamed `_highlights` / `_line_cache` falls back too). Textual calls it inside `TextArea.edit` after the change and before it posts `Changed`, and also on undo, redo, load_text and `__init__`, so the next paint already shows the new colours. A changed `_render_line` tuple shape is NOT covered by this guard (it raises at paint time): the P-M1-7 guard test and the backlog pin cover it
module: taskboard/modals.py
modify: [Data: InkArea._highlights] (replace); [Data: InkArea._line_cache] (clear)
examples: (TC-4251, root harness) `taskboard.modals.colour_spans` (the name modals imports from views; the preview's `notes_text` uses views' own name and stays live) monkeypatched to raise RuntimeError; open the editor on notes "::b:: x ::" → it opens, `_highlights` empty, the cell of "x" not "#60a5fa"; type "y" at the end, `alt+s` → data notes "::b:: x ::y"; `0` uncaught exceptions (SEC-3, LLR-4204.8; NC no try/except: the app crashes in `TextArea.__init__`, RED)
examples: (TC-4251, root harness) `InkArea._line_cache` deleted before an edit (a renamed private) → the edit lands, the field shows plain text, `0` uncaught exceptions
examples: (TC-4246, root on_mount) notes "\ud800 ::b:: x ::" (a board file holding the JSON escape "\ud800") → the editor opens, `_highlights` empty (no ink on a document with a lone surrogate), `render_line(0)` raises nothing, typing and `alt+s` work (SEC-6; see finding SEC-6: LLR-4204.9's "cell of x blue" cannot hold on Textual 8.2.8)
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
  leave: TaskModal.on_text_area_selection_changed → TaskModal._pen_follow wins (empty span at _pen_at removed, cursor moved, pen None) → TaskModal._pen_label
  save: TaskModal._save → TaskModal._lift_pen wins (empty span removed) → TaskModal._save (reads and strips the text)

[Data: TaskModal._pen_at]
in: tuple[int, int]?
desc: NEW (P-M1-4, LLR-4203.14): (row, start) of the pen's current span. Written by `action_pen` ((row, col) when it opens the span) and `action_pen_enter` ((row + 1, 0)) themselves (ARCH-8), refreshed by `_pen_follow` while the span holds the cursor, and set to `None` wherever the pen is set to `None` (`__init__`, `_lift_pen`, `_pen_follow` (b); SEC-4). Read only by `_pen_follow`: when the cursor leaves, `_pen_span()` (live cursor) can no longer find the span, so this is where the empty span is looked up, and it is deleted only while it is still an empty span of the pen's code there. `_lift_pen` (graph-interfaces) does not read it: it runs while the cursor is still inside

[Outside: textual ANSI_SEQUENCES_KEYS]
in: dict[str, tuple[Keys, ...] | str]
desc: Textual 8.2.8's private `textual._ansi_sequences.ANSI_SEQUENCES_KEYS`, read by `XTermParser` (also behind the Windows driver's VT input). `_unshadow_alt_digits` removes its seven entries "\x1b0".."\x1b6" at import (ARCH-1). Windows Terminal 1.24 answers no kitty-protocol query (orchestrator probe, `evidence/wt-kitty-query.log`), so the pens arrive as `ESC <digit>` and this table decides their key name

[I/O: notifications]
desc: `App._notifications`, as in graph-proto-M2. M1 adds the P-M1-3 notice ("Pens write new text — use alt+c to recolour.") and N4 from action_pen (SEC-2)

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
desc: CHANGED: `Label #notes-label` (classes `task-sec`) above `#f-notes`, filled by compose and then by `TaskModal._pen_label` with `pen_label(pen)`. One form (ARCH-7) "Notes <state> alt+123456 0 off alt+c", 34 to 38 cells, inside the 39-cell column at 80x24 and the 58-cell column at 118x30. It replaces the base text `==…== yellow · !!…!! red · ++…++ green`, which no test pins
offers: "1" → TaskModal.action_pen
offers: "2" → TaskModal.action_pen
offers: "3" → TaskModal.action_pen
offers: "4" → TaskModal.action_pen
offers: "5" → TaskModal.action_pen
offers: "6" → TaskModal.action_pen
offers: "0 off" → TaskModal.action_pen
offers: "alt+c" → TaskModal.action_colour

[Outside: key alt+1..alt+6]
desc: NEW TaskModal priority bindings `Binding("alt+<n>", "pen(<n-1>)", "", priority=True, show=False)`. They were free everywhere at base. A terminal in the legacy encoding (Windows Terminal: no kitty protocol) sends `ESC <n>`; with `_unshadow_alt_digits` the parser gives `Key("alt+<n>", "<n>")` (ARCH-1). That event carries a printable character, so if its binding were denied it would fall through and type "<n>" into the focused widget: check_action therefore always allows `pen`, and action_pen consumes the key when the notes lack the focus (ARCH-2). Pilot tests that use `pilot.press` build `Key("alt+5", None)` and cannot see either path: TC-4249 feeds the parser, TC-4240 posts the terminal's event

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
TaskModal._pen_follow ──▶ [Data: TaskModal._pen_at]
[Data: TaskModal._pen_at] ──▶ TaskModal._pen_follow
TaskModal._pen_follow ──▶ [I/O: TextArea #f-notes]
TaskModal._pen_span ──▶ TaskModal._pen_follow
[Data: PEN_CODES] ──▶ pen_label
[Data: PEN_CODES] ──▶ TaskModal.action_pen
[Data: PEN_CODES] ──▶ TaskModal.action_pen_enter
[Data: PEN_CODES] ──▶ TaskModal._pen_span
[Data: PEN_CODES] ──▶ InkArea.__init__
[Data: views.HEX] ──▶ pen_label
[Data: views.HEX] ──▶ InkArea.__init__
TaskModal.__init__ ──▶ [Data: TaskModal._pen_at]
TaskModal.action_pen ──▶ [Data: TaskModal._pen_at]
TaskModal.action_pen_enter ──▶ [Data: TaskModal._pen_at]
TaskModal.action_pen ──▶ [I/O: notifications]
_unshadow_alt_digits ──▶ [Outside: textual ANSI_SEQUENCES_KEYS]
[Outside: textual ANSI_SEQUENCES_KEYS] ──▶ [Outside: key alt+1..alt+6]
when: the terminal sends `ESC <n>` (legacy encoding); the parser gives `Key("alt+<n>", "<n>")`
[Outside: textual ANSI_SEQUENCES_KEYS] ──▶ [Outside: key alt+0]
when: the terminal sends `ESC 0`; the parser gives `Key("alt+0", "0")`
TaskModal.compose ──▶ [Interface: TaskModal Notes label]
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
when: TaskModal is the screen; action "pen" is always allowed (ARCH-2)
[Outside: key alt+1..alt+6] ──▶ TaskModal.action_pen
when: TaskModal is the screen; i = n - 1; the action returns at once unless App.focused is `#f-notes`
[Outside: key alt+0] ──▶ TaskModal.check_action
when: TaskModal is the screen; same as alt+1..alt+6
[Outside: key alt+0] ──▶ TaskModal.action_pen
when: TaskModal is the screen; i = -1 (no pen on: nothing changes); the action returns at once unless App.focused is `#f-notes`
[Outside: key enter] ──▶ TaskModal.check_action
when: TaskModal is the screen; drop_pick first, then pen_enter
[Outside: key enter] ──▶ TaskModal.action_pen_enter
when: check_action("drop_pick") is False, a pen is on, `_pen_span()` is not None, and App.focused is `#f-notes`
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
decision: ruling (03-pdr-rulings round 0): "Accept. LLR-4204.1/.2 say "span" (colour or legacy)." Applied: ink_highlights paints every Span; TC-4245 pins "==late=="

finding P-M1-2 the gate for pen-enter: "mention picker closed" is the wrong condition
anchor: TaskModal.check_action
seen: LLR-4203.7 says "while a pen is on and the mention picker is closed". With an empty directory and `@` typed (the state of test_TC_2503_with_no_one_listed_enter_is_a_new_line) the picker is open (`_mention` "list", "type a name") but drop_pick is denied
cause: the requirement names the picker's display state; the real question is whether drop_pick takes the key
effect: under the literal text, enter under a pen with an empty list is a plain new line: "::b:: @\n ::", and line 2 shows " ::" as literal text, which is the flaw LLR-4203.7 exists to fix
decision: ruling (03-pdr-rulings round 0): "Accept. LLR-4203.7 reworded." Applied in graph-interfaces `TaskModal.check_action` (pen_enter only while drop_pick is False)

finding P-M1-3 alt+n with no pen while the cursor is inside a span, or with a selection
anchor: TaskModal.action_pen
seen: LLR-4203.1 inserts "::<code>::  ::" at the cursor whatever is there. Inside "::r:: abc ::" at (0, 7) that gives "::r:: a::b::  ::bc ::": red ends at the opener (LLR-4201.6), and "bc ::" shows as literal text. With a selection, the insert leaves the selection standing
cause: the requirement assumes the cursor is in plain text
effect: one key press corrupts a span the user typed earlier
decision: ruling (03-pdr-rulings round 0): "Remove the case: if the pen is off and the cursor is inside a span (start < col < end) or the selection is non-empty, `alt+n` inserts nothing and notifies `Pens write new text — use alt+c to recolour.` New LLR-4203.12 (inside a span), LLR-4203.13 (selection). No "continue in span" feature." Applied: action_pen step (2); TC-4252, TC-4254; the old TC-4249 (same code turns the pen on) is dropped

finding P-M1-4 leaving an empty pen span by the cursor leaves it in the notes, and save keeps it
anchor: TaskModal._pen_follow
seen: `alt+3`, then `right` (or a click) at once: LLR-4203.8 turns the pen off, and "::y::  ::" stays in the text. LLR-4203.6 covers only a lift (alt+0, alt+n, alt+c), and LLR-4203.11 only a pen that is on at save
cause: the definition of "lift" does not include the cursor leaving
effect: an empty span that renders nothing is saved: "x::y::  ::"
decision: ruling (03-pdr-rulings round 0): "Accept. New LLR-4203.14." Applied as proposal A in `_pen_follow` with the new [Data: TaskModal._pen_at]; TC-4256, TC-4257. LLR-4203.6 keeps its lift-only wording; proposal B (strip at save) not taken

finding P-M1-5 typing `::` under a pen ends the span
anchor: TaskModal._pen_follow
seen: pen `b` on "::b::  ::", typing `std::` gives "::b:: std:: ::". The first `::` after the inner start is the closer, so the inner text is "std" and the cursor (0, 11) is past inner_end 9, and the pen turns off. The old closer " ::" stays as literal `mut` text
cause: `::` is both the closer and ordinary text (C++ scopes, times), and notes are plain text with no escape
effect: LLR-4203.2 ("each typed character inside that pen's span") cannot hold for `::`
decision: ruling (03-pdr-rulings round 0): "Accept as designed; LLR-4203.2 states the exception; README sentence." TC-4250 pins the result; the README sentence is in graph-proto-V (README node)

finding P-M1-6 the notes column is 39 cells at 80x24, not 37
anchor: pen_label
seen: taskboard.tcss: `#task-box` padding `0 1`, then `#task-edit` and `#task-prev` both `1fr`, so (80 - 2) // 2 = 39. The prototype's label clipped `off` at cell 39 (out/png/col-B-ed_80x24.png)
cause: the brief estimated "about 37"
effect: the widest narrow form ("Notes pen: none alt+123456 0 off alt+c") is 38 cells: it fits 39 with 1 spare cell, but not 37. Below 78 terminal columns the narrow form clips "alt+c" first
decision: ruling (03-pdr-rulings round 0): "Accept (measured from tcss). Narrow form ≤ 38." pen_label as above; TC-4239

finding P-M1-7 the live ink depends on three private Textual internals
anchor: InkArea._build_highlight_map
seen: the override uses `_build_highlight_map`, `_highlights` (byte offsets; an end of 0 reads as "to the line end") and `_line_cache`. pyproject.toml declares `textual` without a version; only requirements.txt pins 8.2.8
cause: Textual has no public API for a custom highlighter without tree-sitter
effect: a Textual upgrade can rename these, and the ink then fails without an error (no colours) or raises
decision: ruling (03-pdr-rulings round 0): "Accept guard tests (one test that fails if `TextArea._build_highlight_map`/`_highlights`/`_line_cache` change shape). Pinning Textual in pyproject → backlog (out of scope)."

finding P-M1-8 the same pen key while that pen is on
anchor: TaskModal.action_pen
seen: LLR-4203.5 covers alt+m with pen n ≠ m; nothing covers m = n
cause: gap in the requirement
effect: the literal lift-then-open rule would close the span and open an empty one after it, which LLR-4203.6 would then remove on the next lift
decision: ruling (03-pdr-rulings round 0): "Accept: changes nothing. New LLR-4203.15." action_pen step (1); TC-4248, TC-4255

finding P-M1-9 enter at the start of the pen's inner text
anchor: TaskModal.action_pen_enter
seen: the literal LLR-4203.7 on "::b::  ::" at (0, 6) gives "::b::  ::\n::b::  ::": an empty span stays on line 1, and LLR-4203.11 cannot remove it (it is not the pen's span any more)
cause: the requirement splits at the cursor without the empty case
effect: an empty span is saved
decision: ruling (03-pdr-rulings round 0): "Reject (special case for a cosmetic empty span; the general LLR-4203.7 path is enough). Remove the `col == s.inner_start` branch from `action_pen_enter`." Done; TC-4251 dropped

finding P-M1-10 proposal for the `_lift_pen` contract: no span holds the cursor
anchor: TaskModal._lift_pen
seen: graph-interfaces says `_lift_pen` "finds the span holding the cursor whose code is the pen's", but not what happens when there is none (for example M2's action_colour after a click that `_pen_follow` has not handled yet, or a closer deleted by hand)
cause: the contract is silent
effect: an implementation can raise or move the cursor by mistake
decision: ruling (03-pdr-rulings round 0): "Accept." Applied in graph-interfaces `TaskModal._lift_pen` (no span → only pen = None) and `TaskModal._pen_span`

finding ARCH-1 the pen keys never reached their bindings on a terminal in the legacy key encoding
anchor: _unshadow_alt_digits
seen: Textual 8.2.8 maps `"\x1b5"` to `Key("infinity", "∞")` and `"\x1b0"` to `º` (`_ansi_sequences.py:384-394`); the orchestrator's probe shows Windows Terminal 1.24 answers no kitty query; the pilot's `Key("alt+5", None)` never takes that path
decision: ruling (03-pdr-rulings round 1): "Accept; keep the operator's keys. At import, modals.py removes the seven entries `"\x1b0"`..`"\x1b6"` from `textual._ansi_sequences.ANSI_SEQUENCES_KEYS` … so `ESC <digit>` takes the parser's generic alt path → `Key("alt+5", "5")` … New LLR-4203.16 (parser level)." Applied: new node `_unshadow_alt_digits`, [Outside: textual ANSI_SEQUENCES_KEYS], TC-4249 (parser output executed on 8.2.8)

finding ARCH-7 nothing required the wide Notes-label form
anchor: pen_label
seen: the narrow form (≤ 38 cells) fits 39 and 58 cells and names the pen; the wide form added `_notes_w`, a resize hook and 7 width examples
decision: ruling (03-pdr-rulings round 1): "Accept: remove the wide label form (one form ≤ 38 cells; no `_notes_w`, no resize hook)." Applied: `_fit_width` node, [Data: TaskModal._notes_w], PEN_LABEL_WIDE and the wide examples deleted; pen_label takes no width; compose writes the first label

finding SEC-1 the ink re-encoded each prefix per offset
anchor: ink_highlights
seen: `b(i) = len(line[:i].encode())` four times per span: 1 103 ms on a 100 000-char line (security, executed)
decision: ruling (03-pdr-rulings round 1): "Accept: linear scanner (cache each kind's next match) and one-pass byte offsets. New LLR-4201.10, LLR-4204.7." Applied: ink_highlights (identity offsets for ASCII, one prefix table otherwise); TC-4246 timing example

finding SEC-2 a pen insert could fuse with neighbouring text
anchor: TaskModal.action_pen
seen: "b:: x" at (0, 0) + alt+1 → "::r::  ::b:: x" shows " x"; "C::b" at (0, 4) → "C::b::r::  ::" shows "Cr  ::"
decision: ruling (03-pdr-rulings round 1): "Accept: the pen insert gets the visible-text check and notice N4. New LLR-4203.17." Applied: action_pen step (4); TC-4252 (three examples)

finding SEC-3 the private-API override was not fail-safe
anchor: InkArea._build_highlight_map
seen: a renamed `_line_cache` / `_highlights` raises inside `TextArea.__init__` or `edit()`, crashing the editor and losing the unsaved edit
decision: ruling (03-pdr-rulings round 1): "Keep HLR-4204 … Make it fail-safe: the override catches any exception and falls back to the base map (no ink, no crash). New LLR-4204.8. Pinning Textual in pyproject → BACKLOG." Applied: try/except around the override body, fallback `super()._build_highlight_map()`; TC-4251

finding SEC-6 a lone surrogate crashed the editor once any line had ink
anchor: InkArea._build_highlight_map
seen: `ink_highlights`' strict encode raised; and (probe executed on Textual 8.2.8, scratch) `_render_line` runs `_utf8_encode(line.plain)` (strict) on EVERY visible line whenever `_highlights` is non-empty: a highlight on row 1 makes `render_line(0)` of "\ud800 ::b:: x ::" raise UnicodeEncodeError
cause: the ruled fix (surrogatepass offsets) makes `ink_highlights` total, but cannot reach Textual's own strict encode at paint time
effect: LLR-4204.9's threshold "cell of `x` blue" cannot hold on Textual 8.2.8 without overriding the private `_render_line` too; the design keeps the editor alive by leaving the map empty for a document that holds a lone surrogate (no ink, field works)
decision: ruling (03-pdr-rulings round 1): "Accept: byte offsets via `encode("utf-8", "surrogatepass")`. New LLR-4204.9." Applied: ink_highlights (surrogatepass, TC-4246) and the empty-map guard in `_build_highlight_map` (TC-4246, root on_mount). OPEN for the orchestrator: amend LLR-4204.9's threshold to "the editor opens and works; no ink while the notes hold a lone surrogate", or rule an `_render_line` override (one more private name)

finding ARCH-13 typing `::` into a fresh pen gives ` ::`
anchor: TaskModal._pen_follow
seen: on "::b::  ::" at (0, 6), `:` `:` → the empty span is removed with the two typed colons in it; the line reads " ::"
decision: ruling (03-pdr-rulings round 1): "Accept: pin the ` ::` result in TC-4250 and the README sentence; no code." Applied: TC-4250 example; README sentence in graph-proto-V

### Seams
> Consumed from group V (views.py): `colour_spans(text) -> list[Span]` (str offsets, one line) in `_pen_span`, `action_pen` (the inside-a-span test) and `ink_highlights`; `[Data: PEN_CODES]` (code, tone, name in pen order) in `pen_label`, `action_pen`, `action_pen_enter`, `_pen_span` and `InkArea.__init__`; `[Data: Span]` (start, inner_start, inner_end, end, tone, code; code None for a legacy span) in `_pen_span`, `action_pen_enter` and `ink_highlights`; `highlight_segments` only as the oracle of TC-4231 and TC-4245; `views.HEX` must hold "orange", "blue" and "violet" (it already does) and "dim" `#5b6675`.
> Offered to group M2 (palette): `TaskModal._lift_pen()` (the contract in graph-interfaces, plus P-M1-10), which M2's `action_colour` calls before it computes the target (LLR-4205.14); `[Data: TaskModal.pen]` (read only); the Notes label, which already shows "alt+c" (one form, ARCH-7), offered to `TaskModal.action_colour`, so M2 must not add another listing of alt+c in the editor. `TaskModal.check_action` now lives in graph-interfaces with one notes-focus gate for `pen`, `pen_enter` and `colour` (P-M2-6); M2 adds its own `alt+c` binding. M2's palette rewrites go through `TextArea.replace`, so the ink is rebuilt for them by `InkArea._build_highlight_map` with no call from M2.
> Shared file: modals.py. M1 changes TaskModal.__init__, compose, on_text_area_selection_changed and _save, and adds _unshadow_alt_digits, pen_label, ink_highlights, InkArea, action_pen, action_pen_enter, _pen_follow, _pen_label and [Data: TaskModal._pen_at]; it implements the interface nodes check_action, _pen_span and _lift_pen. `_fit_width` stays as at base (ARCH-7).
> Seam note for the orchestrator (LLR-4203.14): graph-interfaces lists LLR-4203.14 on `_lift_pen` and names the leave handler as a caller, but when the cursor has left, `_pen_span()` (live cursor) returns None, so `_lift_pen` would only set pen = None. The removal on leave is therefore done in `_pen_follow` from `_pen_at`; `_pen_follow` does not call `_lift_pen`.
