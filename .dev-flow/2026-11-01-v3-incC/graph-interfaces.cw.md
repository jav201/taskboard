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
func: if a pen is on: s = _pen_span(); if s is None only set pen to None; else if s's inner text is empty remove text[s.start:s.end] and put the cursor at s.start, else put the cursor at s.end; then set pen to None and refresh the Notes label. No pen: does nothing. Owned by M1; called by M1 (action_pen, _save) and M2 (action_colour). (P-M1-10)
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace); [Data: TextArea #f-notes] (replace)
examples: (TC-4258) notes "::b:: abc ::", cursor (0, 9), pen `4` → notes "::b:: abc ::", cursor (0, 12), pen `None`
examples: (TC-4259) notes "x::y::  ::", cursor (0, 7), pen `2` → notes "x", cursor (0, 1), pen `None`

TaskModal._pen_span
req: LLR-4203.7, LLR-4203.8
in:
out: Span? span
func: the pen's span holding the cursor: None when no pen is on, when the selection of #f-notes is not empty, or when no Span of colour_spans(cursor row) has code PEN_CODES[pen][0] with inner_start <= col <= inner_end; else the first such span. Owned by M1, used by _lift_pen and M2.
module: taskboard/modals.py
examples: (TC-4258) notes "::b:: abc ::", cursor (0, 9), pen `4` → span start `0`, inner_start `6`, inner_end `9`, end `12`
examples: (TC-4245) notes "::b:: abc ::", cursor (0, 12), pen `4` → span `None`

TaskModal.check_action
req: LLR-4203.10, LLR-4203.7, LLR-4205.16, HLR-4203, HLR-4205
in: str action; tuple[object, ...] parameters
out: bool? allowed
func: base arms unchanged (`mark`, `drop_move`, `drop_pick`). ONE notes-focus gate (P-M2-6): `pen`, `pen_enter` and `colour` are allowed only while #f-notes has the focus; `pen_enter` additionally only while a pen is on and the `drop_pick` arm is False (P-M1-2). In BINDINGS `drop_pick` precedes `pen_enter` on `enter`, so the picker wins, then the pen, then the TextArea's newline. Every other action → True.
module: taskboard/modals.py
examples: (TC-4240) action "pen", parameters (4,), App.focused `#f-title` → allowed `False`
examples: (TC-4230) action "pen", parameters (4,), App.focused `#f-notes` → allowed `True`
examples: (TC-4237) action "pen_enter", pen `None` → allowed `False`; the notes get a plain new line as in test_TC_2503_with_no_one_listed_enter_is_a_new_line
examples: (TC-4284) action "colour", App.focused `#f-title` → allowed `False`

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

## Edges

[Data: PEN_CODES] ──▶ colour_spans
[Data: PEN_CODES] ──▶ TaskModal._lift_pen
[Data: TaskModal.pen] ──▶ TaskModal._lift_pen
[Data: TaskModal.pen] ──▶ TaskModal._pen_span
[Data: TaskModal.pen] ──▶ TaskModal.check_action
TaskModal._pen_span ──▶ TaskModal._lift_pen
TaskModal._lift_pen ──▶ [Data: TaskModal.pen]
