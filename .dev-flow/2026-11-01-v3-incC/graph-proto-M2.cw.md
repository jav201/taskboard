# Code-Wire prototype — group M2 — the colour palette and the details label (Inc C)

Differences from `graph-baseline.cw.md` only (base 0a8dfaa). Group M2 owns, in `taskboard/modals.py`: `alt+c` in the task editor, the pure target finder `colour_target`, the pure rewrite `recolour`, the pure placement `palette_offset`, the `ColourPalette` modal, the editor's write-back `_apply_colour` (where the cursor ends), and the details screen's Notes label. Requirements: HLR-4205, LLR-4205.1 to LLR-4205.16, LLR-4202.9. Test ids TC-4260 to TC-4289 are this group's (TC-4284 is used by graph-interfaces `TaskModal.check_action`; `check_action` itself now lives there, P-M2-6). Offsets are `str` indices of one line; a location is (row, col). Every value in the examples below was run through a reference scanner written from LLR-4201.1 to LLR-4201.8 (a scratch script, not product code), so the example lines agree with the tokeniser that group V builds.

Notice texts (one per refusal, `notify(..., severity="warning", markup=False)`):
- N1 (LLR-4205.10): "Colour one line at a time."
- N2 (LLR-4205.11, P-M2-1): "The selection crosses a colour edge: select inside one colour, or plain text."
- N3 (LLR-4205.12, P-M2-3): "Nothing to colour: select text or put the cursor on a word."
- N4 (LLR-4205.15, P-M2-2): "That colour would change the text you see: nothing changed." (the one visible-text check in `_apply_colour`; it is not limited to `::`; M1's action_pen reuses it, LLR-4203.17)
- N5 (SEC-5): "The notes changed while the palette was open: nothing changed." (the callback's re-validation in `_apply_colour`)

## Nodes

TaskModal.action_colour
req: HLR-4205, LLR-4205.1, LLR-4205.2, LLR-4205.10, LLR-4205.11, LLR-4205.12, LLR-4205.14, LLR-4205.16
in:
out: None
func: NEW. alt+c (priority binding `Binding("alt+c", "colour", "Colour", priority=True)`; check_action always allows it, ARCH-2). Steps, in order: (0) If `#f-notes` does not have the focus: return at once; the key is consumed, no palette opens and no field changes (LLR-4205.16; a denied binding would let the terminal's `Key("alt+c", "c")` type "c" into the focused Input). (1) s = `_pen_span()` BEFORE the lift (ARCH-3). (2) `_lift_pen()` (M1). (3) If s is not None and s.inner_start < s.inner_end: the target is (row, s.inner_start, s.inner_end), the pen's span (LLR-4205.14); the lift moved only the cursor, or (no closer, ARCH-10) inserted " ::" after inner_end, so these offsets still hold. If s is not None and its inner text is empty: the lift removed it; notify N3 and stop (no palette). If s is None: `colour_target(notes.document.lines, notes.selection.start, notes.selection.end)` on the lines AFTER the lift; a notice → `notify` it and stop (no palette). (4) A target (row, a, b) → line_at_open = `notes.document.get_line(row)`; `push_screen(ColourPalette(notes.cursor_screen_offset), partial(self._apply_colour, row, a, b, line_at_open))`. The notes at that moment (after the lift, when the palette opens) are the reference of LLR-4205.7 and LLR-4205.8: `0` on an uncoloured target and `esc` leave the notes byte-equal to them, not to the notes before alt+c (P-M2-4)
module: taskboard/modals.py
modify: [Data: App.screen_stack] (append); [I/O: notifications] (append)
examples: (TC-4284, root action_colour) focus on `#f-title`, title "T", notes "n"; post `events.Key("alt+c", "c")` (the terminal's event, not pilot.press) → no palette, title "T" and notes "n" byte-equal, `0` notify (ARCH-2, LLR-4205.16; NC a denied check_action: the title becomes "Tc", RED)
examples: (TC-4260, root action_colour) notes "the plan works", selection (0, 8)→(0, 4) → the screen is ColourPalette; target row `0`, a `4`, b `8`
examples: (TC-4261, root action_colour) notes "the plan works", cursor (0, 6), no selection → ColourPalette for a `4`, b `8` ("plan")
examples: (TC-4270, root action_colour) notes "ab\ncd", selection (0, 1)→(1, 1) → no palette; 1 notify "Colour one line at a time."
examples: (TC-4271, root action_colour) notes "::b:: ab :: cd", selection (0, 7)→(0, 13) (`b :: c`) → no palette; 1 notify "The selection crosses a colour edge: select inside one colour, or plain text."
examples: (TC-4272, root action_colour) notes "", cursor (0, 0) → no palette; 1 notify "Nothing to colour: select text or put the cursor on a word."
examples: (TC-4274, root action_colour) keys alt+5, "ab" → notes "::b:: ab ::", cursor (0, 8), pen `4`; alt+c → s = the pen's span (inner 6..8) read before the lift; `_lift_pen` puts the cursor at (0, 11), pen `None`; ColourPalette for a `6`, b `8` (the pen's inner text, ARCH-3); then "3" → "::y:: ab ::" (LLR-4205.14)
examples: (TC-4274, root action_colour) notes "now", cursor (0, 0), keys alt+5, "go" → "::b:: go ::now", cursor (0, 8), pen `4`; alt+c → ColourPalette for a `6`, b `8`, no notice (ARCH-3; NC the word ending at the lifted cursor is "::now" 9..14, which overlaps the span 0..11 → N2: RED)
examples: (TC-4274, root action_colour) notes "x ", cursor (0, 2), keys alt+5 → "x ::b::  ::"; alt+c → the lift removes the empty span: notes "x ", cursor (0, 2); no palette; 1 notify "Nothing to colour: select text or put the cursor on a word."
examples: (TC-4274, root action_colour) notes "plan", cursor (0, 4), keys alt+5 → "plan::b::  ::"; alt+c → the lift removes the empty pen span: notes "plan", cursor (0, 4); no palette; 1 notify N3 (ARCH-3 ruling: an empty pen span ends the call with the "nothing to colour" notice, it does not fall back to the word before it)

colour_target
req: LLR-4205.1, LLR-4205.2, LLR-4205.10, LLR-4205.11, LLR-4205.12
in: list[str] lines; tuple[int, int] start; tuple[int, int] end
out: tuple(tuple[int, int, int]? target, str? notice)
func: NEW, pure. The palette's target as (row, a, b) with a < b, or a notice (exactly one of the two is None). start and end are the TextArea selection's two ends in any order. Rules in this order: (1) the ends on two rows → N1; (2) a selection → its columns sorted; no selection → a word (ARCH-4): cut the line into regions by `colour_spans(line)`: for each span its opener [start, inner_start), its inner [inner_start, inner_end) and its closer [inner_end, end), and the gaps between spans; a word is a maximal run of non-whitespace inside ONE region. The target is the word w with w.start <= col < w.end (holding col), else the word with w.end == col (ending at col), else none. So a word never takes span markers with it, and a cursor on a span's markers targets a marker word, which lies inside that span (recolour then rewrites the whole span); (3) no target (no selection and no word at the cursor), or a selection of whitespace only → N3 (LLR-4205.12 as amended, P-M2-3); (4) the target overlaps a span of `colour_spans(line)` (a < s.end and b > s.start) without lying inside it (s.start <= a and b <= s.end) → N2 (LLR-4205.11 as amended, P-M2-1); this includes a selection that holds a whole span plus other text. A target that touches a span's edge does not overlap it
module: taskboard/modals.py
examples: (TC-4261) lines ["the plan works"], start (0, 6), end (0, 6) → target (0, 4, 8)
examples: (TC-4261) lines ["the plan works"], start (0, 8), end (0, 8) (just after the word) → target (0, 4, 8)
examples: (TC-4261) lines ["the plan works"], start (0, 4), end (0, 4) (on the word's first letter) → target (0, 4, 8)
examples: (TC-4260) lines ["the plan works"], start (0, 8), end (0, 4) → target (0, 4, 8)
examples: (TC-4261) lines ["::r:: a b ::"], start (0, 6), end (0, 6) → target (0, 6, 7); it lies inside the span 0..12
examples: (TC-4261) lines ["::b:: ab ::"], start (0, 11), end (0, 11) → target (0, 9, 11) (the closer word, ending at col, inside the span 0..11)
examples: (TC-4261) lines ["::b:: abc ::d"], start (0, 12), end (0, 12) → target (0, 12, 13) ("d", in the gap after the span; ARCH-4; NC the old rule took "::d" 10..13, which overlaps the span 0..12 → N2: RED); recolour with "g" then gives "::b:: abc ::::g:: d ::", visible "abcd" unchanged
examples: (TC-4261) lines ["==late=="], start (0, 3), end (0, 3) → target (0, 2, 6) ("late", the legacy span's inner region; it lies inside the span 0..8, so recolour rewrites the whole span)
examples: (TC-4261) lines ["x ::b:: y :: z"], start (0, 1), end (0, 1) → target (0, 0, 1): "x" touches no span (the span starts at `2`)
examples: (TC-4270) lines ["ab", "cd"], start (0, 1), end (1, 1) → notice "Colour one line at a time."
examples: (TC-4270) lines ["ab", "cd"], start (0, 0), end (1, 0) (a whole line taken with shift+down) → notice "Colour one line at a time."
examples: (TC-4271) lines ["::b:: ab :: cd"], start (0, 7), end (0, 13) → notice "The selection crosses a colour edge: select inside one colour, or plain text."
examples: (TC-4280) lines ["x ::b:: y :: z"], start (0, 0), end (0, 14) (a whole span and plain text) → notice "The selection crosses a colour edge: select inside one colour, or plain text."
examples: (TC-4280) lines ["x::b::y::"], start (0, 0), end (0, 0) → target (0, 0, 1) ("x": the word stops at the span's start 1; ARCH-4 — under the old rule the word was the whole line and gave N2)
examples: (TC-4280) lines ["x::b::y::"], start (0, 0), end (0, 9) (a selection of the whole line) → notice "The selection crosses a colour edge: select inside one colour, or plain text." (N2 now comes from selections only)
examples: (TC-4272) lines [""], start (0, 0), end (0, 0) → notice "Nothing to colour: select text or put the cursor on a word."
examples: (TC-4272) lines ["the  plan"], start (0, 4), end (0, 4) (two spaces around the cursor) → notice "Nothing to colour: select text or put the cursor on a word."
examples: (TC-4281) lines ["a   b"], start (0, 1), end (0, 4) (three spaces selected) → notice "Nothing to colour: select text or put the cursor on a word."

recolour
req: LLR-4205.4, LLR-4205.5, LLR-4205.6, LLR-4205.7, LLR-4205.9
in: str line; int a; int b; str code
out: tuple(str new_line, int? col)
func: NEW, pure. code is one of the PEN_CODES codes or "0". s = the span of `colour_spans(line)` with s.start <= a and b <= s.end. Inside s: code "0" → line[:s.start] + inner + line[s.end:], col = s.start + len(inner); a code → line[:s.start] + "::<code>:: " + inner + " ::" + line[s.end:], col = the new span's end. No such span: code "0" → (line, None) unchanged; a code → line[:a] + "::<code>:: " + line[a:b] + " ::" + line[b:], col = the new span's end. inner = line[s.inner_start:s.inner_end], so the optional marker spaces go with the markers (any of the 9 forms: 6 codes, 3 legacy). col is the column just after the written closer (or after the uncoloured text for `0`). recolour checks nothing about the visible text: that single invariant check is `_apply_colour`'s (LLR-4205.15, P-M2-2). It raises ValueError only on a target that partly overlaps a span (colour_target never hands one)
module: taskboard/modals.py
examples: (TC-4263) line "the plan works", a `4`, b `8`, code "r" → new_line "the ::r:: plan :: works", col `17`
examples: (TC-4263) line "the plan works", a `4`, b `8`, code "o" → new_line "the ::o:: plan :: works", col `17`
examples: (TC-4263) line "the plan works", a `4`, b `8`, code "y" → new_line "the ::y:: plan :: works", col `17`
examples: (TC-4263) line "the plan works", a `4`, b `8`, code "g" → new_line "the ::g:: plan :: works", col `17`
examples: (TC-4263) line "the plan works", a `4`, b `8`, code "b" → new_line "the ::b:: plan :: works", col `17`
examples: (TC-4263) line "the plan works", a `4`, b `8`, code "v" → new_line "the ::v:: plan :: works", col `17`
examples: (TC-4264) line "go ::o::now:: ok", a `8`, b `11`, code "r" → new_line "go ::r:: now :: ok", col `15`
examples: (TC-4264) line "go ::o::now:: ok", a `8`, b `11`, code "o" → new_line "go ::o:: now :: ok", col `15` (the same code: only the spaced form)
examples: (TC-4264) line "go ::o::now:: ok", a `8`, b `11`, code "y" → new_line "go ::y:: now :: ok", col `15`
examples: (TC-4264) line "go ::o::now:: ok", a `8`, b `11`, code "g" → new_line "go ::g:: now :: ok", col `15`
examples: (TC-4264) line "go ::o::now:: ok", a `8`, b `11`, code "b" → new_line "go ::b:: now :: ok", col `15`
examples: (TC-4264) line "go ::o::now:: ok", a `8`, b `11`, code "v" → new_line "go ::v:: now :: ok", col `15`
examples: (TC-4264) line "::r:: a b ::", a `6`, b `7`, code "y" → new_line "::y:: a b ::", col `12` (the whole span, not only "a")
examples: (TC-4264) line "::b::  x  ::", a `7`, b `8`, code "y" → new_line "::y::  x  ::", col `12` (inner " x " kept)
examples: (TC-4265) line "==late==", a `0`, b `8`, code "b" → new_line "::b:: late ::", col `13`
examples: (TC-4265) line "!!x!! y", a `2`, b `3`, code "r" → new_line "::r:: x :: y", col `10`
examples: (TC-4265) line "++done++", a `2`, b `6`, code "g" → new_line "::g:: done ::", col `13`
examples: (TC-4266) line "x ::b:: y :: z", a `8`, b `9`, code "0" → new_line "x y z", col `3`
examples: (TC-4266) line "==y==", a `0`, b `5`, code "0" → new_line "y", col `1`
examples: (TC-4266) line "::r:: open", a `6`, b `10`, code "0" → new_line "open", col `4` (a span open to the line end)
examples: (TC-4266) line "::b:: x ::r:: y ::", a `6`, b `7`, code "0" → new_line "x ::r:: y ::", col `2` (a span ended by the next opener keeps its space)
examples: (TC-4267) line "the plan works", a `4`, b `8`, code "0" → new_line "the plan works", col `None`
examples: (TC-4282) line "::r:: open", a `6`, b `10`, code "y" → new_line "::y:: open ::", col `13` (the rewrite closes the open span)
examples: (TC-4282) line "::b:: x ::r:: y ::", a `6`, b `7`, code "y" → new_line "::y:: x  ::::r:: y ::", col `11` (inner "x " kept; the next span untouched)
examples: (TC-4282) line "a:plan", a `2`, b `6`, code "b" → new_line "a:::b:: plan ::", col `15` (the opener after a lone colon; P-M2-7)
examples: (TC-4282) line "é café ☕", a `2`, b `6`, code "o" → new_line "é ::o:: café :: ☕", col `15` (str offsets, not bytes)
examples: (TC-4285) line "std::vector", a `0`, b `11`, code "b" → new_line "::b:: std::vector ::", col `20`; its visible text "stdvector ::" differs from "std::vector", so `_apply_colour` refuses it
examples: (TC-4285) line "planb::", a `0`, b `4`, code "b" → new_line "::b:: plan ::b::", col `13`; `::b::` at 11 is an opener that ends the span (visible "plan "), so `_apply_colour` refuses it
examples: (TC-4286) line "==a::b==", a `0`, b `8`, code "b" → new_line "::b:: a::b ::", col `13`; visible "ab ::" differs from "a::b", so `_apply_colour` refuses it; code "0" → new_line "a::b", col `4`, visible "a::b" unchanged, allowed
examples: (TC-4269) over the 12 cases of TC-4263 and TC-4264: new_line[:x] == line[:x] and the tail after the rewritten range is byte-equal, where x..y is the target (plain) or s.start..s.end (inside a span); 12/12
examples: (TC-4287) over every case above except TC-4285 and the coloured TC-4286 case: the joined `highlight_segments` text of new_line equals that of line, and for a code the span at x has that code and the old text as inner; 100 %
oracle: 01-requirements.md LLR-4205.4 to LLR-4205.9 thresholds ("the ::b:: plan :: works", "::b:: late ::", "::y:: a b ::", "x y z", "y")

### Recolour table (TC-4263 to TC-4267, TC-4282; target a..b; col = the cursor column after the rewrite)
| # | line | a..b | key | new line | col |
|---|---|---|---|---|---|
| 1 | `the plan works` | 4..8 | 1 r | `the ::r:: plan :: works` | 17 |
| 2 | `the plan works` | 4..8 | 2 o | `the ::o:: plan :: works` | 17 |
| 3 | `the plan works` | 4..8 | 3 y | `the ::y:: plan :: works` | 17 |
| 4 | `the plan works` | 4..8 | 4 g | `the ::g:: plan :: works` | 17 |
| 5 | `the plan works` | 4..8 | 5 b | `the ::b:: plan :: works` | 17 |
| 6 | `the plan works` | 4..8 | 6 v | `the ::v:: plan :: works` | 17 |
| 7 | `go ::o::now:: ok` | 8..11 | 1 r | `go ::r:: now :: ok` | 15 |
| 8 | `go ::o::now:: ok` | 8..11 | 2 o | `go ::o:: now :: ok` | 15 |
| 9 | `go ::o::now:: ok` | 8..11 | 3 y | `go ::y:: now :: ok` | 15 |
| 10 | `go ::o::now:: ok` | 8..11 | 4 g | `go ::g:: now :: ok` | 15 |
| 11 | `go ::o::now:: ok` | 8..11 | 5 b | `go ::b:: now :: ok` | 15 |
| 12 | `go ::o::now:: ok` | 8..11 | 6 v | `go ::v:: now :: ok` | 15 |
| 13 | `==late==` | 0..8 | 5 b | `::b:: late ::` | 13 |
| 14 | `!!x!! y` | 2..3 | 1 r | `::r:: x :: y` | 10 |
| 15 | `++done++` | 2..6 | 4 g | `::g:: done ::` | 13 |
| 16 | `::r:: a b ::` | 6..7 | 3 y | `::y:: a b ::` | 12 |
| 17 | `x ::b:: y :: z` | 8..9 | 0 | `x y z` | 3 |
| 18 | `==y==` | 0..5 | 0 | `y` | 1 |
| 19 | `::r:: open` | 6..10 | 0 | `open` | 4 |
| 20 | `::b:: x ::r:: y ::` | 6..7 | 0 | `x ::r:: y ::` | 2 |
| 21 | `the plan works` | 4..8 | 0 | unchanged | none |
| 22 | `::r:: open` | 6..10 | 3 y | `::y:: open ::` | 13 |
| 23 | `::b:: x ::r:: y ::` | 6..7 | 3 y | `::y:: x  ::::r:: y ::` | 11 |
| 24 | `std::vector` | 0..11 | 5 b | `::b:: std::vector ::`, refused by `_apply_colour` (N4) | 20 |

palette_offset
req: LLR-4205.13
in: int x; int y; int screen_w; int screen_h
out: tuple(int box_x, int box_y)
func: NEW, pure. The palette box's top-left from the anchor (x, y) = the notes cursor's screen cell, for a box of PALETTE_W `15` by PALETTE_H `10` cells: box_x = max(0, min(x - 1, screen_w - 15)); box_y = y + 1 when y + 1 + 10 <= screen_h (the rows just below the target), else max(0, y - 10) (the rows just above it). So the box's top row = anchor row + 1, or, when it would not fit below, its bottom row = anchor row − 1 (the measure of LLR-4205.13 as amended, P-M2-9). On any screen of 21 rows or more the box is wholly on screen and one of the two holds
module: taskboard/modals.py
examples: (TC-4273) x `4`, y `5`, screen_w `80`, screen_h `24` → box_x `3`, box_y `6` (below; rows 6..15)
examples: (TC-4273) x `70`, y `20`, screen_w `80`, screen_h `24` → box_x `65`, box_y `10` (above; rows 10..19, the target on row 20)
examples: (TC-4273) x `0`, y `3`, screen_w `118`, screen_h `30` → box_x `0`, box_y `4`
examples: (TC-4273) x `110`, y `26`, screen_w `118`, screen_h `30` → box_x `103`, box_y `16` (above; rows 16..25)

ColourPalette.compose
req: LLR-4205.3
in:
out: ComposeResult widgets
func: NEW. `class ColourPalette(ModalScreen[str | None])`: one `Vertical #cp-box` (border round HEX accent, border title "colour", padding 0 1, width 15, height auto) holding one `Static #cp-rows`: a Text of 8 rows built from PEN_CODES, never markup: `<n> ██ <name>` for n 1..6 (the digit in KEY_STYLE bold bright, "██" and the name in HEX[tone]), then `0 none` ("none" in HEX mut) and `esc cancel` ("cancel" in HEX mut). No Button (the modal-key law: keys only). The screen's background lets the editor show under it
module: taskboard/modals.py
examples: (TC-4262) → rows "1 ██ red", "2 ██ orange", "3 ██ yellow", "4 ██ green", "5 ██ blue", "6 ██ violet", "0 none", "esc cancel" in that order (8 rows)
examples: (TC-4262) → the styles of "red" `#f43f5e`, "orange" `#fb923c`, "yellow" `#fbbf24`, "green" `#4ade80`, "blue" `#60a5fa`, "violet" `#a78bfa` (6/6); every key ("1".."6", "0", "esc") in "b #e6edf7"
examples: (TC-4278) the source of ColourPalette holds no "Button(" and INVENTORY gains "ColourPalette": {} → test_TC_2407_every_modal_is_in_the_inventory passes

ColourPalette.on_mount
req: LLR-4205.13
in:
out: None
func: NEW. Places `#cp-box`: `styles.offset = palette_offset(at.x, at.y, app.size.width, app.size.height)`, at = the anchor given to `__init__` (the editor's `notes.cursor_screen_offset` when alt+c ran)
module: taskboard/modals.py
modify: [Data: ColourPalette._at] (replace)
examples: (TC-4273, root action_colour) 80x24, notes "plan" on the notes field's first row, cursor (0, 4), alt+c → the box region lies inside (0, 0, 80, 24) and its top row is the anchor row + 1
examples: (TC-4273, root action_colour) 80x24, notes of 30 lines "line N", cursor on the last visible row of `#f-notes`, alt+c → the box region lies inside (0, 0, 80, 24) and its bottom row is the anchor row - 1
examples: (TC-4273, root action_colour) 118x30, the same two notes → both boxes inside (0, 0, 118, 30); 4/4

ColourPalette.action_pick
req: LLR-4205.4, LLR-4205.5, LLR-4205.6, LLR-4205.7
in: str code
out: None
func: NEW. Keys 1..6 and 0 (priority bindings `Binding(str(n), "pick('<code>')", "", priority=True)` from PEN_CODES, and `Binding("0", "pick('0')", ...)`): `dismiss(code)`. Any other key does nothing; the palette stays (P-M2-8)
module: taskboard/modals.py
modify: [Data: App.screen_stack] (replace)
examples: (TC-4263, root action_pick) key "5" → dismiss "b"; the screen is TaskModal again
examples: (TC-4266, root action_pick) key "0" → dismiss "0"
examples: (TC-4283) keys "a", "enter", "7" in the palette → the screen is still ColourPalette and the notes are byte-equal

ColourPalette.action_cancel
req: LLR-4205.8
in:
out: None
func: NEW. esc (priority binding): `dismiss(None)`
module: taskboard/modals.py
modify: [Data: App.screen_stack] (replace)
examples: (TC-4268, root action_cancel) notes "the plan works", selection (0, 8)→(0, 4), alt+c, esc → the palette gone, notes "the plan works" byte-equal, the selection still (0, 8)→(0, 4), focus `#f-notes`
examples: (TC-4268, root action_cancel) notes "::b:: ab", cursor (0, 8), pen `4` (a pen span with no closer); alt+c → the target is (0, 6, 8), the lift writes "::b:: ab ::" and the palette opens; esc → notes "::b:: ab ::", byte-equal to the notes at palette open, not to "::b:: ab" (P-M2-4, ARCH-10; the old "plan" + empty pen case now opens no palette, ARCH-3)

TaskModal._apply_colour
req: LLR-4205.4, LLR-4205.5, LLR-4205.6, LLR-4205.7, LLR-4205.8, LLR-4205.15
in: int row; int a; int b; str line_at_open; str? code
out: None
func: NEW, the palette's callback. code None (esc) → nothing. Re-validation first (SEC-5): if row >= `notes.document.line_count` or `notes.document.get_line(row) != line_at_open` (the line the target was computed on), notify N5 once and change nothing (no recolour call, so `recolour`'s ValueError on a partly overlapping target can never be raised inside the callback). Else `recolour(line, a, b, code)` on line = line_at_open: col None → nothing changed (cursor and selection as they were). Then the one visible-text check (LLR-4205.15, P-M2-2): if `"".join(seg for seg, _ in highlight_segments(new_line)) != "".join(seg for seg, _ in highlight_segments(line))` → notify N4 once and change nothing (text, cursor and selection as they were at palette open); else `notes.replace(new_line, (row, 0), (row, len(line)))` (one undo step) and `notes.move_cursor((row, col))`: the cursor ends just after the new span's closer, or for `0` just after the uncoloured text, with no selection. The pen stays None; the TextArea posts Changed, so the preview and the live ink follow (baseline on_text_area_changed, M1)
module: taskboard/modals.py
modify: [I/O: TextArea #f-notes] (replace); [I/O: notifications] (append)
examples: (TC-4275, root action_pick) notes "the plan works", target (0, 4, 8), code "y" → notes "the ::y:: plan :: works", cursor (0, 17), selection empty; typing "!" then gives "the ::y:: plan ::! works" (the "!" is not yellow)
examples: (TC-4275, root action_pick) notes "x ::b:: y :: z", target (0, 8, 9), code "0" → notes "x y z", cursor (0, 3)
examples: (TC-4275, root action_pick) notes "line one\n==late== two", target (1, 0, 8), code "b" → notes "line one\n::b:: late :: two", cursor (1, 13); row 0 byte-equal
examples: (TC-4267, root action_pick) notes "the plan works", selection (0, 8)→(0, 4), code "0" → notes byte-equal, the selection still (0, 8)→(0, 4)
examples: (TC-4285, root action_pick) notes "std::vector", cursor (0, 2), alt+c, "5" → target (0, 0, 11); notes "std::vector" byte-equal; 1 notify "That colour would change the text you see: nothing changed."
examples: (TC-4286, root action_pick) notes "==a::b==", cursor (0, 3), alt+c, "5" → target (0, 2, 6) (inside the legacy span 0..8, ARCH-4); notes "==a::b==" byte-equal; 1 notify N4
examples: (TC-4288, root action_pick) notes "the plan works", cursor (0, 6), alt+c → palette for (0, 4, 8), line_at_open "the plan works"; while the palette is on top the test replaces row 0 with "the plan" (`notes.replace`); "5" → notes "the plan" byte-equal, 1 notify "The notes changed while the palette was open: nothing changed." (SEC-5)
examples: (TC-4288, root action_pick) notes "a\nthe plan works", target (1, 4, 8); row 1 deleted while the palette is on top (notes "a"); "5" → notes "a" byte-equal, 1 notify N5, no exception
examples: (TC-4286, root action_pick) notes "==a::b==", cursor (0, 3), alt+c, "0" → notes "a::b", cursor (0, `4`) (visible text unchanged, allowed)

TaskDetails.compose
req: LLR-4202.9
in:
out: ComposeResult widgets
func: CHANGED, one line: the Notes label above the notes becomes `Label(DETAILS_NOTES_LABEL)`, a markup constant built once from PEN_CODES and HEX: "[b]Notes[/b]  " + the syntax hint "[<HEX mut>]::c:: … ::[/]" + "  " + the six codes in pen order, each "[<HEX[tone]>]<code>[/]", one space apart (ruling C-2, ARCH-5). No legacy listing (`==…==`, `!!…!!`, `++…++`, P-M2-5); legacy notes still render as at base. The rest of compose is unchanged
module: taskboard/modals.py
examples: (TC-4276) the label's plain text "Notes  ::c:: … ::  r o y g b v" (`30` cells, inside the 56-cell box); it holds no "==", "!!" or "++"
examples: (TC-4276) the label's markup holds `#f43f5e`, `#fb923c`, `#fbbf24`, `#4ade80`, `#60a5fa`, `#a78bfa` (6/6), each wrapping its own code letter; the hint "::c:: … ::" in `#8b98a5`
examples: (TC-4276) a task with notes "::b:: ask ::" opened in TaskDetails at 80x24 → the label row shows "::c:: … ::  r o y g b v" whole, and "ask" in `#60a5fa` below it

## Entities

[Outside: key alt+c]
desc: CHANGED. Now bound in TaskModal too: `Binding("alt+c", "colour", "Colour", priority=True)`. `TaskModal.check_action` always allows it (ARCH-2); action_colour returns at once, consuming the key, when the notes lack the focus (LLR-4205.16). In the legacy encoding the terminal's `ESC c` arrives as `Key("alt+c", "c")` (printable), so a denied binding would type "c" into the focused Input. Still bound in MarkForm (a different modal; test_AT_2604 untouched). Shown to the user on the editor's Notes label (M1, LLR-4203.9), not on `#task-keys` (that line names buttons)

[Outside: palette key 1..6]
desc: priority bindings of ColourPalette, one per PEN_CODES row in pen order: 1 r, 2 o, 3 y, 4 g, 5 b, 6 v; the app's plain digit view keys (keymap.py:65-74, not priority) never see them while the palette is on top

[Outside: palette key 0]
desc: priority binding of ColourPalette: `pick('0')`, uncolour

[Outside: palette key esc]
desc: priority binding of ColourPalette: `cancel`; the editor's own esc (action_cancel) does not run, the editor stays open

[Interface: colour palette]
desc: ColourPalette `#cp-box`, 15 by 10 cells, next to the target and on screen; its 8 rows are its key line (the keys bold bright, the names in their tones)
offers: (TC-4263) "1 ██ red" → ColourPalette.action_pick
offers: (TC-4263) "2 ██ orange" → ColourPalette.action_pick
offers: (TC-4263) "3 ██ yellow" → ColourPalette.action_pick
offers: (TC-4263) "4 ██ green" → ColourPalette.action_pick
offers: (TC-4263) "5 ██ blue" → ColourPalette.action_pick
offers: (TC-4263) "6 ██ violet" → ColourPalette.action_pick
offers: (TC-4266) "0 none" → ColourPalette.action_pick
offers: (TC-4268) "esc cancel" → ColourPalette.action_cancel

[Interface: TaskDetails Notes label]
desc: CHANGED. "Notes  ::c:: … ::  r o y g b v", the hint in mut and each code letter in its tone (DETAILS_NOTES_LABEL; ruling C-2, ARCH-5); the legacy listing is gone (P-M2-5)

[Data: DETAILS_NOTES_LABEL]
in: str
desc: modals.py constant, the details label's markup, built at import from PEN_CODES and views.HEX

[Data: ColourPalette._at]
in: Offset
desc: the anchor handed to ColourPalette at push: the editor's `#f-notes` cursor_screen_offset after the lift

[Data: App.screen_stack]
desc: the palette is pushed on top of TaskModal and popped by a pick or esc; the target (row, a, b) rides in the callback (`functools.partial`), so TaskModal keeps no palette state
sequence:
  altC: TaskModal.check_action (always True) → TaskModal.action_colour (returns unless #f-notes has the focus) → TaskModal._pen_span (read before the lift) → TaskModal._lift_pen (pen None; an empty span removed; a missing closer written) → colour_target (only when no non-empty pen span; reads the lines after the lift) → ColourPalette.compose → ColourPalette.on_mount → palette_offset
  pick: ColourPalette.action_pick → TaskModal._apply_colour (re-validates line_at_open) → recolour → TaskModal.on_text_area_changed wins (the preview and the ink follow)
  cancel: ColourPalette.action_cancel → TaskModal._apply_colour (code None: nothing)

[I/O: notifications]
desc: `App._notifications`; the four notices N1 to N4, one per refusal, severity warning, markup False

[Data: modal-key INVENTORY]
desc: tests/test_modal_keys.py `INVENTORY` (TC-2407) gains the row "ColourPalette": {} under "no buttons: keys only"; the law's checks then hold: no "Button(" in its source, its keys bound on it

## Edges

[Outside: key alt+c] ──▶ TaskModal.check_action
when: TaskModal is the screen; action "colour" is always allowed (ARCH-2)
[Outside: key alt+c] ──▶ TaskModal.action_colour
when: TaskModal is the screen; without the notes' focus the action returns at once: no palette, no field changes (LLR-4205.16, TC-4284)
[Data: TaskModal.pen] ──▶ TaskModal._lift_pen
TaskModal._pen_span ──▶ TaskModal.action_colour
TaskModal.action_colour ──▶ [Data: App.screen_stack]
TaskModal.action_colour ──▶ [I/O: notifications]
[I/O: TextArea #f-notes].selection ──▶ colour_target
[I/O: TextArea #f-notes].cursor_location ──▶ ColourPalette.on_mount
[Data: PEN_CODES] ──▶ ColourPalette.compose
[Data: PEN_CODES] ──▶ [Data: DETAILS_NOTES_LABEL]
[Data: views.HEX] ──▶ ColourPalette.compose
[Data: views.HEX] ──▶ [Data: DETAILS_NOTES_LABEL]
[Data: DETAILS_NOTES_LABEL] ──▶ TaskDetails.compose
TaskDetails.compose ──▶ [Interface: TaskDetails Notes label]
ColourPalette.compose ──▶ [Interface: colour palette]
[Data: ColourPalette._at] ──▶ ColourPalette.on_mount
[Outside: palette key 1..6] ──▶ ColourPalette.action_pick
when: ColourPalette is the screen
[Outside: palette key 0] ──▶ ColourPalette.action_pick
when: ColourPalette is the screen
[Outside: palette key esc] ──▶ ColourPalette.action_cancel
when: ColourPalette is the screen
ColourPalette.action_pick ──▶ [Data: App.screen_stack]
ColourPalette.action_cancel ──▶ [Data: App.screen_stack]
[I/O: TextArea #f-notes].text ──▶ TaskModal._apply_colour
TaskModal._apply_colour ──▶ [I/O: TextArea #f-notes]
TaskModal._apply_colour ──▶ [I/O: notifications]

### Seams
> Consumed from group V (views.py): `colour_spans(line)` → list[Span] (start, inner_start, inner_end, end, tone, code) — read by colour_target (overlap test) and recolour (the span to rewrite); `highlight_segments` (`_apply_colour`'s visible-text check, LLR-4205.15); `PEN_CODES` (pen order, code, tone, name) — read by ColourPalette.compose, the palette bindings and DETAILS_NOTES_LABEL; `Span` (the `.start/.inner_start/.inner_end/.end` fields only). recolour needs colour_spans to find an opener at the first position where one matches, also after a lone ":" ("a:::b:: plan ::" → one span start 2; P-M2-7).
> Consumed from group M1 (modals.py): `TaskModal._pen_span()` (read first in action_colour, before the lift: a non-empty pen span is the target, ARCH-3) and `TaskModal._lift_pen()` (called next; after it the pen is None and the cursor past the old span's closer — a missing closer is written first, ARCH-10 — or at its start when the empty span was removed); the editor's Notes label shows `alt+c` (LLR-4203.9) — the palette's only on-screen key; `TaskModal.check_action` now lives in graph-interfaces with one notes-focus gate for `pen`, `pen_enter` and `colour` (P-M2-6); the live ink repaints from the TextArea's Changed after `_apply_colour`.
> Offered to the others: nothing; colour_target, recolour and palette_offset are module-level and private to the palette.

## Findings

finding P-M2-1 a selection that holds a whole span and more has no requirement
anchor: colour_target
seen: (TC-4280) "x ::b:: y :: z" all selected is not uncoloured (LLR-4205.4), not inside one span (LLR-4205.5), and does not "partly" overlap a span (LLR-4205.11): it covers it fully; wrapping it nests one span in another
effect: untestable; a mutant that wraps it passes every threshold
decision: ruling (03-pdr-rulings round 0): "Accept: LLR-4205.11 → "overlaps a span without lying inside it" (refuse)." Applied: colour_target rule (4); TC-4271, TC-4280

finding P-M2-2 text holding :: cannot be coloured and keep its text
anchor: recolour
seen: (TC-4279) wrapping "std::vector" gives "::b:: std::vector ::", which shows "stdvector ::"; recolouring "==a::b==" gives "::g:: a::b ::", which shows "ab ::"; a selection glued to `b::` ("planb::", select "plan") turns the `b::` into an opener; LLR-4205.4 and LLR-4205.5 then break their own intent (the text is no longer the target's text)
effect: the palette would corrupt technical notes; no escape syntax exists in LLR-4201
decision: ruling (03-pdr-rulings round 0): "Accept as a single invariant check: if the visible text (joined segments) of the line after the rewrite differs from before, change nothing and notify. New LLR-4205.15." Applied: the check moved from recolour into `_apply_colour`; N4 reworded to the general case; TC-4285 (std::vector, planb::), TC-4286 (==a::b==); the old TC-4279 is gone

finding P-M2-3 a selection of only spaces is not "nothing to colour"
anchor: colour_target
seen: (TC-4281) LLR-4205.12 covers "no selection and no word"; a selection of three spaces would wrap to "a::b::     ::b", a colour nobody can see
decision: ruling (03-pdr-rulings round 0): "Accept (LLR-4205.12 amended)." Applied: colour_target rule (3); TC-4272, TC-4281

finding P-M2-4 "unchanged" in LLR-4205.7 and LLR-4205.8 has no reference point
anchor: TaskModal.action_colour
seen: (TC-4274) LLR-4205.14 lifts the pen before the target; when the pen's span is empty the lift removes it (LLR-4203.6), so after alt+c then esc the notes differ from the notes before alt+c
effect: a test comparing with the text before alt+c fails on a correct build
decision: ruling (03-pdr-rulings round 0): "Accept: compared with the notes at the moment the palette opened (after the lift). LLR-4205.7/.8 amended." Applied: action_colour func; TC-4267, TC-4268

finding P-M2-5 the details label drops the legacy listing
anchor: TaskDetails.compose
seen: LLR-4202.9 asks for the six codes and is silent on the base text "highlight: ==…== yellow, !!…!! red, ++…++ green"; both together are about 70 cells and the details box has 56
decision: ruling (03-pdr-rulings round 0): "Accept. The label lists the six codes only; legacy notes still render." Applied: TaskDetails.compose label "Notes  r o y g b v" (the syntax hint "colour ::c:: text ::" is dropped too, read as part of "six codes only"); TC-4276

finding P-M2-6 TaskModal.check_action is edited by M1 and M2
anchor: TaskModal.check_action
seen: the pen keys (LLR-4203.10, M1) and alt+c (M2) both gate on the notes' focus in the one method; alt+c outside the notes is in no requirement (LLR-4203.10 names alt+n and alt+0 only)
decision: ruling (03-pdr-rulings round 0): "Accept: `TaskModal.check_action` moves into graph-interfaces with ONE notes-focus gate for `pen`, `pen_enter`, `colour`. New LLR-4205.16 (alt+c without notes focus changes nothing)." Applied: M2's check_action node deleted; the alt+c edge's `when:` cites LLR-4205.16; TC-4277 is replaced by graph-interfaces TC-4284

finding P-M2-7 proposal for colour_spans: an opener after a lone colon
anchor: recolour
seen: (TC-4282) "a:plan" with "plan" coloured gives "a:::b:: plan ::"; a scanner that consumes "::" at col 1 as literal text before it tries an opener at col 2 shows "a:::b:: plan ::" raw
decision: ruling (03-pdr-rulings round 0): "Accept." Applied in graph-proto-V `colour_spans` example TC-4229 ("a:::b:: plan ::" → one span start 2)

finding P-M2-8 keys the palette does not list, and a part of a span
anchor: ColourPalette.action_pick
seen: (TC-4283) no requirement says what a key outside 1..6, 0, esc does; (TC-4264) a target inside a span recolours the whole span ("::r:: a b ::" with "a" → "::y:: a b ::"), so a span is never split
decision: ruling (03-pdr-rulings round 0): "Accept as decisions." Other keys do nothing and the palette stays open (TC-4283); no span splitting (LLR-4205.5 as written)

finding P-M2-9 "next to the target" in LLR-4205.13 has no measure
anchor: palette_offset
seen: the threshold checks only box ⊂ screen; a box clamped to (0, 0) passes it
decision: ruling (03-pdr-rulings round 0): "Accept: box top row = anchor row + 1, or box bottom row = anchor row − 1 when it would not fit below. LLR-4205.13 amended." Applied: palette_offset func; TC-4273 (4/4)

finding ARCH-3 alt+c under a pen targeted "the word ending at the cursor", not the pen's span
anchor: TaskModal.action_colour
seen: (TC-4274) after the lift the cursor stands just after the closer; on "::b:: go ::now" the word is "::now" (9..14), which overlaps the span 0..11 → N2, no palette
decision: ruling (03-pdr-rulings round 1): "Accept. `action_colour` reads `_pen_span()` BEFORE `_lift_pen()`; a non-empty pen span is the target (its inner range); an empty one is removed by the lift and the call ends with the "nothing to colour" notice. Example `::b:: go ::now` added." Applied: action_colour steps (1)-(3); TC-4274 (the "plan" + empty pen case now ends with N3), TC-4268 rewritten on a closer-less pen span

finding ARCH-4 the word target swallowed span markers
anchor: colour_target
seen: on "::b:: abc ::d" at (0, 12) the old word "::d" (10..13) overlapped the span 0..12 → N2 about "the selection" with nothing selected
decision: ruling (03-pdr-rulings round 1): "Accept the architect's fix (word = non-whitespace run inside the gap or span-inner region holding the cursor; a cursor on markers targets that span)." Applied: colour_target rule (2) (regions: opener, inner, closer, gaps); TC-4261 (new "::b:: abc ::d" example, "==late==" → (0, 2, 6)), TC-4280 ("x::b::y::" at (0, 0) → (0, 0, 1)), TC-4286 target (0, 2, 6)

finding ARCH-5 the details label contradicted ruling C-2
anchor: TaskDetails.compose
seen: the node and TC-4276 pinned "Notes  r o y g b v" with "no `::`"; C-2 keeps the syntax hint
decision: ruling (03-pdr-rulings round 1): "Accept (= C-2)." C-2: "keep the syntax hint — `Notes  ::c:: … ::  r o y g b v`, each code letter in its tone (≈ 30 cells, fits the 56-cell box). Legacy listing stays dropped." Applied: TaskDetails.compose, TC-4276, [Interface: TaskDetails Notes label]

finding SEC-5 the palette callback re-read the line and could raise inside a callback
anchor: TaskModal._apply_colour
seen: the target (row, a, b) is computed at open, the line re-read at pick; a changed line could make `recolour` raise ValueError inside the `push_screen` callback and crash the editor
decision: ruling (03-pdr-rulings round 1): "Accept (E4 addendum): the palette callback re-validates the target; if the line changed it does nothing and notifies." Applied: `line_at_open` rides in the partial; _apply_colour re-validation and notice N5; TC-4288
