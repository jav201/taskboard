# Inc C — shared interfaces (owned by the orchestrator; agents PROPOSE changes in their group file, never edit here)

> The seams between the three prototype groups. Group V owns views.py + report_deck.py +
> report_workspace.py; group M1 owns the pens and the live ink in modals.py; group M2 owns the
> palette in modals.py. Offsets are `str` indices of one line unless a node says bytes.

## Nodes

colour_spans
req: LLR-4201.1, LLR-4201.2, LLR-4201.4, LLR-4201.5, LLR-4201.6, LLR-4201.7, LLR-4201.8, LLR-4204.4
in: str text
out: list[Span] spans
func: the one scanner: every colour span and legacy span of text, in order, never crossing a line break; each Span gives str offsets start <= inner_start <= inner_end <= end, its tone, and its code (None for a legacy span). The markers are text[start:inner_start] and text[inner_end:end]; the optional spaces belong to the markers.
module: taskboard/views.py
examples: (TC-4202) text "a ::b:: x :: c" → spans start `2`, inner_start `8`, inner_end `9`, end `12`, tone "blue", code "b"
examples: (TC-4204) text "::r:: open" → one span start `0`, inner_start `6`, inner_end `10`, end `10`, tone "over"
examples: (TC-4206) text "::b:: x ::r:: y ::" → span 1 inner "x " (inner_start `6`, inner_end `8`, end `8`, tone "blue"); span 2 start `8`, inner "y", tone "over"
examples: (TC-4205) text "std::vector" → spans `[]`
examples: (TC-4203) text "==late==" → one span start `0`, inner_start `2`, inner_end `6`, end `8`, tone "soon", code `None`

highlight_segments
req: LLR-4201.1, LLR-4201.3, LLR-4201.9, HLR-4201
in: str text
out: list[tuple[str, str]] segments
func: derived from colour_spans: text between spans as "mut", each span's inner text in its tone; joined segment texts = text without markers. Signature unchanged from base.
module: taskboard/views.py
examples: (TC-4202) text "a ::b:: x :: c" → segments ("a ", "mut"), ("x", "blue"), (" c", "mut")
examples: (TC-4203) text "==y== !!r!!" → segments ("y", "soon"), (" ", "mut"), ("r", "over") as at base

TaskModal._lift_pen
req: LLR-4203.3, LLR-4203.4, LLR-4203.6, LLR-4203.11, LLR-4205.14
in: TaskModal self
out: None
func: if a pen is on: s = _pen_span(); if s is None only set pen to None; else if s's inner text is empty remove text[s.start:s.end] and put the cursor at s.start; else if s has no closer (s.end == s.inner_end: the span ends at the line end, at `\n` or at the next opener) insert " ::" at s.inner_end and put the cursor at s.inner_end + 3 (ARCH-10: the next typed character is outside the span; before a next opener the result "…  ::::r::" tokenises with the same visible text); else put the cursor at s.end; then set pen to None, set `_pen_at` to None (SEC-4) and refresh the Notes label. No pen: does nothing. Owned by M1; called by M1 (action_pen, _save) and M2 (action_colour). (P-M1-10)
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace); [Data: TaskModal._pen_at] (replace); [Data: TextArea #f-notes] (replace)
examples: (TC-4258) notes "::b:: abc ::", cursor (0, 9), pen `4` → notes "::b:: abc ::", cursor (0, 12), pen `None`, _pen_at `None`
examples: (TC-4258) notes "::b:: ab", cursor (0, 8), pen `4` (a span with no closer, for example after `delete` ×3 on "::b:: ab ::") → notes "::b:: ab ::", cursor (0, `11`), pen `None`; the next `d` gives "::b:: ab ::d", "d" in `mut` (ARCH-10)
examples: (TC-4258) notes "::b:: x ::r:: y ::", cursor (0, 8), pen `4` (span 1 ended by the next opener) → notes "::b:: x  ::::r:: y ::", cursor (0, `11`), pen `None`; highlight_segments ("x ", "blue"), ("y", "over"), the same visible text as before
examples: (TC-4259) notes "x::y::  ::", cursor (0, 7), pen `2` → notes "x", cursor (0, 1), pen `None`, _pen_at `None`

TaskModal._pen_span
req: LLR-4203.7, LLR-4203.8
in:
out: Span? span
func: the pen's span holding the cursor: None when no pen is on, when the selection of #f-notes is not empty, or when no Span of colour_spans(cursor row) has code PEN_CODES[pen][0] with inner_start <= col <= inner_end; else the first such span. Owned by M1, used by _lift_pen, check_action (the pen_enter arm, ARCH-8) and M2 (action_colour reads it before the lift, ARCH-3).
module: taskboard/modals.py
examples: (TC-4258) notes "::b:: abc ::", cursor (0, 9), pen `4` → span start `0`, inner_start `6`, inner_end `9`, end `12`
examples: (TC-4253) notes "::b:: abc ::", cursor (0, 12), pen `4` → span `None`

TaskModal.check_action
req: LLR-4203.10, LLR-4203.7, LLR-4205.16, HLR-4203, HLR-4205
in: str action; tuple[object, ...] parameters
out: bool? allowed
func: base arms unchanged (`mark`, `drop_move`, `drop_pick`). `pen` and `colour` → always True (ARCH-2): a denied priority binding lets the terminal's `Key("alt+c", "c")` / `Key("alt+5", "5")` fall through to the focused Input, which types the character, so the focus gate lives in the actions instead: `action_pen` (M1) and `action_colour` (M2) return at once, consuming the key, while #f-notes lacks the focus. ONE gated arm: `pen_enter` is allowed only while #f-notes has the focus, a pen is on, `_pen_span()` is not None (ARCH-8) and the `drop_pick` arm is False (P-M1-2); there the fall-through to the TextArea's newline is wanted. In BINDINGS `drop_pick` precedes `pen_enter` on `enter`, so the picker wins, then the pen, then the TextArea's newline. Every other action → True.
module: taskboard/modals.py
examples: (TC-4240) action "pen", parameters (4,), App.focused `#f-title` → allowed `True` (action_pen then returns at once; title and notes byte-equal)
examples: (TC-4230) action "pen", parameters (4,), App.focused `#f-notes` → allowed `True`
examples: (TC-4237) action "pen_enter", pen `None` → allowed `False`; the notes get a plain new line as in test_TC_2503_with_no_one_listed_enter_is_a_new_line
examples: (TC-4237) action "pen_enter", pen `4`, notes "::b:: ab ::x", cursor (0, 12) (the cursor has left the span and no SelectionChanged has been handled yet) → `_pen_span()` `None` → allowed `False`; `enter` gives a plain new line: "::b:: ab ::x\n" (ARCH-8)
examples: (TC-4284) action "colour", App.focused `#f-title` → allowed `True` (action_colour then returns at once; no palette, fields byte-equal)

## Entities

[Data: PEN_CODES]
in: tuple[tuple[str, str, str], ...]
desc: views.py constant, pen order 1..6 as (code, tone, name): ("r","over","red"), ("o","orange","orange"), ("y","soon","yellow"), ("g","green","green"), ("b","blue","blue"), ("v","violet","violet"). Every tone is a key of views.HEX. Read by colour_spans, the legends, the pen label, the palette, the live ink.

[Data: Span]
in: NamedTuple(int start, int inner_start, int inner_end, int end, str tone, str? code)
desc: views.py; one span of one line, str offsets.

[Data: TaskModal.pen]
in: int?
desc: the index 0..5 into PEN_CODES of the pen that is on, or None. Written by action_pen, _lift_pen, the cursor-leave handler; read by the label, enter handling, check_action.

[Data: TaskModal._pen_at]
in: tuple[int, int]?
desc: (row, start) of the pen's span, owned by M1 (graph-proto-M1 has the full contract). Set by action_pen and action_pen_enter when they open a span, refreshed by _pen_follow, and set to None wherever the pen is set to None (here by _lift_pen; SEC-4, ARCH-8).

## Edges

[Data: PEN_CODES] ──▶ colour_spans
[Data: PEN_CODES] ──▶ TaskModal._lift_pen
[Data: TaskModal.pen] ──▶ TaskModal._lift_pen
[Data: TaskModal.pen] ──▶ TaskModal._pen_span
[Data: TaskModal.pen] ──▶ TaskModal.check_action
TaskModal._pen_span ──▶ TaskModal._lift_pen
TaskModal._lift_pen ──▶ [Data: TaskModal.pen]
TaskModal._lift_pen ──▶ [Data: TaskModal._pen_at]
TaskModal._pen_span ──▶ TaskModal.check_action

## Findings

finding ARCH-2 a denied gate let alt+c and alt+<n> fall through as printable characters
anchor: TaskModal.check_action
seen: in legacy encoding "\x1bc" is `Key("alt+c", "c")`, is_printable True; with check_action("colour") False and the focus in `#f-title`, Input._on_key inserts "c"; the pilot builds `Key("alt+c", None)`, so TC-4284 stayed green
decision: ruling (03-pdr-rulings round 1): "Accept. `check_action` allows `pen` and `colour` always; the actions return early (consuming the key) when `#f-notes` lacks the focus. Only `pen_enter` stays gated. Tests post `events.Key("alt+c", "c")` / `Key("alt+5", "5")`." Applied: check_action func and TC-4240, TC-4284; the early returns are in M1 action_pen and M2 action_colour

finding ARCH-8 pen decisions could read stale state when the next key overtook the editor's own SelectionChanged
anchor: TaskModal.check_action
seen: the pen_enter arm checked only that a pen is on, and `_pen_at` was written only by `_pen_follow`
decision: ruling (03-pdr-rulings round 1): "Accept the 3-line fix (`_pen_at` set by `action_pen` and `action_pen_enter`; `pen_enter` arm requires `_pen_span()`)." Applied: the pen_enter arm (TC-4237) and [Data: TaskModal._pen_at] here; the writes are in M1

finding ARCH-9 TC-4245 named two different tests
anchor: TaskModal._pen_span
seen: `_pen_span`'s example here and M1's ink_highlights both cited TC-4245
decision: ruling (03-pdr-rulings round 1): "Accept: interface example TC-4245 → TC-4253." Applied

finding ARCH-10 alt+0 on a pen span with no closer left the cursor inside
anchor: TaskModal._lift_pen
seen: pen on "::b:: ab ::" at (0, 8), `delete` ×3 → "::b:: ab" (end == inner_end == 8); alt+0, `d` → "::b:: abd" with "d" blue
decision: ruling (03-pdr-rulings round 1): "Accept: `_lift_pen` on a span with no closer (`end == inner_end`) inserts ` ::` before moving past it." Applied: _lift_pen func, TC-4258 (two examples)

finding SEC-4 `_pen_at` could go stale
anchor: TaskModal._lift_pen
seen: `_pen_at` was never reset when a pen was set or lifted, so a later leave could delete an unrelated empty span of the same code at the same start
decision: ruling (03-pdr-rulings round 1): "Accept with ARCH-8: `_pen_at` is reset whenever a pen is set or lifted; `_pen_follow` deletes only if the text at `_pen_at` is still an empty span of the pen's code." Applied: _lift_pen sets it to None (TC-4258, TC-4259); the other writes and the guarded delete are in M1
