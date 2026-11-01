# Code-Wire baseline — notes highlight slice at 0a8dfaa

Baseline of the notes highlight syntax (`==x==` soon, `!!x!!` over, `++x++` green) as the code is at commit 0a8dfaa (marks tree `taskboard-wt/incC-marks`). Every node has `req: to trace`: the requirements of this increment are written in parallel. Example sources are test ids (file::test) of the current suite, or a probe `P-n` run on 0a8dfaa (values printed by the probe, listed in baseline-notes.md). The three `_highlight_markup` call sites inside the Focus renderers (`_focus_detail_lines`, `_focus_tiles`, `_focus_review`) are caller sites, not nodes: they pass a note line to `_highlight_markup` and do not tokenise themselves.

## Nodes

highlight_segments
req: to trace
in: str text
out: list[tuple[str, str]] segments
func: the one tokeniser of the notes' highlight syntax; splits one line into (segment, tone) pairs with `_HIGHLIGHT_RE` (non-greedy, alternation == then !! then ++): ==x== `soon`, !!x!! `over`, ++x++ `green`, every other run `mut`; markers dropped, an empty highlight gives an empty segment in its tone
module: taskboard/views.py
examples: (test_highlight_segments.py::test_TC_417_segments_drop_markers_and_keep_text) text "a ==y== b" → segments "a " `mut`, "y" `soon`, " b" `mut`
examples: (test_highlight_segments.py::test_TC_417_segments_drop_markers_and_keep_text) text "x\ ==[b]== :smile:" → segments "[b]" `soon`, " :smile:" `mut` (payload kept as text)
examples: (test_highlight_segments.py::test_TC_417_segments_drop_markers_and_keep_text) text "a !!!! b" → segments "a " `mut`, an empty segment `over`, " b" `mut` (D-415)

notes_text
req: to trace
in: str text; dict? people = None
out: Text note
func: a note as Rich Text pieces, never parsed: each line through `highlight_segments`, each segment appended in HEX[tone]; with `people`, a known mention drawn `@Name` bold pink inside the highlight, an unknown handle dimmed; blank lines kept as bare newlines
module: taskboard/views.py
examples: (test_present_note_highlights.py::test_AT_2905_the_regression_pin) text "==a==", people `None` → note "a" with one span `#fbbf24`
examples: (test_people_look.py::test_TC_2506_the_preview_draws_a_known_mention_as_its_name_in_pink, root harness) text "Review with @ana.ruiz\n- ==send to @diego.paz== now" → note "Review with @Ana Ruiz\n- send to @Diego Paz now"; "send to " `#fbbf24`

_highlight_markup
req: to trace
in: str text
out: str markup
func: the board's markup seat: each segment of `highlight_segments` escaped and wrapped by `c(…, tone)`; an input with no segment gives `c("", "mut")`
module: taskboard/views.py
examples: (test_present_note_highlights.py::test_AT_2905_the_regression_pin) text "==a==" → markup "[#fbbf24]a[/]" (contains `#fbbf24`)
examples: (test_highlight_segments.py::test_TC_417_the_board_markup_is_unchanged) over 1000+ derived inputs (pieces "ab", "==y==", "!!r!!", "++g++", "[b]", "x\\") → markup byte-equal to the frozen 56a1b10 function
examples: (P-1) text "" → markup "[#8b98a5][/]"

_focus_note_snippet
req: to trace
in: str notes; int width
out: str snippet
func: the Focus cards' one-line note: first non-blank line, stripped, `" …"` added when more lines follow, clipped to `width`, then `_highlight_markup`; empty or blank notes give ""
module: taskboard/views.py
examples: (P-1) notes "==a== b\nsecond", width `40` → snippet "[#fbbf24]a[/][#8b98a5] b …[/]"
examples: (test_focus.py::test_render_focus_presentations_smoke) notes "- [ ] todo\n- [x] done" in the `cards` presentation → the card draws a snippet line and the frame holds "task with note" (no assertion on the snippet itself)

present_note_lines
req: to trace
in: str notes; int w; dict? people = None
out: list[tuple[str, list[tuple[str, str]]]] rows
func: the presentation's notes as (lead, pieces) rows that fit `w` cells: mentions written `@Name` first, list leads `• ` / `1. `, highlights tokenised per paragraph BEFORE the wrap, `mut` mapped to `ink`, tones walked onto the wrapped rows
module: taskboard/views.py
examples: (test_people_look.py::test_TC_2506_present_lines_write_the_name_and_never_split_it) notes "with @ana.ruiz", w `40` → rows lead "" with one piece "with @ana.ruiz" `ink`
examples: (P-1) notes "- ==alpha== bravo", w `40` → rows lead "• ", pieces "alpha" `soon`, " bravo" `ink`
examples: (test_present_note_highlights.py::test_L0_marker_free_twin_wraps_identically) notes "==alpha== bravo ++charlie delta echo foxtrot++ golf" at w `24` → the same row shapes as its marker-free twin "alpha bravo charlie delta echo foxtrot golf"

legend_entries
req: to trace
in: str mode; Board board; date? today = None; int width = 96; int height = 30; bool show_archived = False; TeamState? team_state = None; str team_filter = "equipo"; str? selected_id = None; str? gantt_focus = None; str? gantt_previous = None; str kanban_presentation = "grouped"; str kanban_group = "project"; str? kanban_focus = None
out: list[tuple[str, str]] entries
func: (swatch, meaning) pairs for the marks the current view draws; in mode `focus` with any pinned task it lists the project spine and the three highlight swatches (views.py:8734-8736), whether or not a pinned note holds a highlight
module: taskboard/views.py
examples: (P-2) mode "focus", one pinned task with notes "==a==" → entries "highlight: yellow / warning" with swatch "[#fbbf24]==text==[/]", "highlight: red / attention", "highlight: green / resolved"
examples: (P-2) mode "focus", no pinned task → entries empty, no highlight line
examples: (test_legend.py::test_no_entry_describes_a_mark_the_view_is_not_drawing) mode "focus" on the `full` and `bare` boards → every swatch's glyphs occur in the painted view (a weak check for "==text==": any of its characters passes)

notes_html
req: to trace
in: str text; dict people
out: str html
func: notes as inert HTML for the report: per line, each segment of `highlight_segments` split by mentions, each piece escaped inside `<span class="hl-<tone>">` (tone soon/over/green/mut), a known mention `<span class="hl-<tone> mention">@Name</span>`; lines joined by `<br>`; "" for empty text
module: taskboard/report_html.py
examples: (test_report_html.py::test_TC_3115_embed_json_and_notes_are_inert) text "==a== <b>x</b> @ana.ruiz" → html `<span class="hl-soon">a</span>`, `&lt;b&gt;x&lt;/b&gt;`, `<span class="hl-mut mention">@Ana Ruiz</span>`
examples: (test_report_html.py::test_TC_3115_embed_json_and_notes_are_inert) text "" → html "" (no span)

_notes_text
req: to trace
in: str text
out: str plain
func: the report's plain notes (for search and the CSV): each line's segments joined with the markers dropped; None-safe through `(text or "")`
module: taskboard/report_html.py
examples: (P-1) text "==a== !!b!!\n++c++" → plain "a b" on the first line, "c" on the second
examples: (test_report_workspace.py::test_TC_3110_notes_off_strips_the_notes) the notes section off → every `notes_text` is empty (the dict key, not this function, is cleared)

notes_preview
req: to trace
in: str text; dict? people = None
out: Text preview
func: the editor preview and the details card: `Text.assemble(notes_text(text, people))`; no parser reads the notes (S1, S-4)
module: taskboard/modals.py
examples: (test_people_look.py::test_TC_2506_the_preview_draws_a_known_mention_as_its_name_in_pink) text "Review with @ana.ruiz\n- ==send to @diego.paz== now" → preview "@Ana Ruiz" `b #f472b6`, "send to " `#fbbf24`
examples: (test_people_look.py::test_TC_2506_without_a_directory_the_preview_is_unchanged) text "Ask @ana.ruiz", people `None` → preview "Ask @ana.ruiz" in `#8b98a5`
examples: (test_edit_window.py::test_the_preview_paints_markup_typed_in_a_note_as_text) text "[reverse]boom[/reverse] [link=https://evil.example]x[/link] ==[b]y[/b]==" → preview holds "[reverse]boom[/reverse]" and "[b]y[/b]" as text

TaskModal.on_text_area_changed
req: to trace
in: TextArea.Changed event
out: None
func: on a change of `#f-notes` only: re-renders `#task-preview` with `notes_preview(text, board.people)`, follows the cursor after refresh, and with a directory closes the add form (typing in the notes) or re-scans for an `@`
module: taskboard/modals.py
modify: [I/O: Static #task-preview] (replace); [Data: TaskModal._mention] (clear)
examples: (test_edit_window.py::test_the_preview_follows_the_typing_to_the_last_line, root on_text_area_changed) typing "!!ship it now!!" on the note's last line at 80x24 → the preview's visible rows hold "ship it now" in `#f43f5e`
examples: (test_edit_window.py::test_the_preview_paints_markup_typed_in_a_note_as_text, root on_text_area_changed) `#f-notes` text set to "[reverse]boom[/reverse] … ==[b]y[/b]==" → the preview shows "[b]y[/b]" literally

TaskModal.on_text_area_selection_changed
req: to trace
in: TextArea.SelectionChanged event
out: None
func: on a cursor move in `#f-notes` only: keeps the preview scrolled to the cursor's line (by proportion) and re-scans the `@` picker while it lists
module: taskboard/modals.py
modify: [I/O: VerticalScroll #task-preview-scroll] (replace)
examples: (test_people_picker.py::test_TC_2503_closed_the_arrows_move_the_cursor, root on_text_area_selection_changed) `up` with the picker closed → the notes' cursor row goes up by `1` and the drop stays hidden (display `False`)

TaskModal.check_action
req: to trace
in: str action; tuple[object, ...] parameters
out: bool? allowed
func: gates the editor's own priority keys: `mark` (alt+m) only when `#f-mark` was composed; `drop_move` (up/down) and `drop_pick` (enter) only while the picker lists something, or while the add form holds the focus; everything else (alt+s, alt+i, alt+t, alt+d, ctrl+v, ctrl+e, tab, esc) `True`
module: taskboard/modals.py
examples: (test_people_picker.py::test_TC_2503_closed_the_arrows_move_the_cursor) action "drop_move", _mention `None` → allowed `False` (the key falls to `#f-notes`)
examples: (test_people_picker.py::test_TC_2503_with_no_one_listed_enter_is_a_new_line) action "drop_pick", _mention "list" with no option → allowed `False`; the notes read "@\n"
examples: (test_marks_manager.py::test_TC_2605_an_empty_directory_composes_no_select) action "mark" with no `#f-mark` → allowed `False`; "alt+m" not painted

## Entities

[Data: views._HIGHLIGHT_RE]
in: re.Pattern
desc: views.py:3502 `==(.*?)==|!!(.*?)!!|\+\+(.*?)\+\+` — three fixed delimiters, three tones; non-greedy, so `==a==b==` closes at the first `==`; also imported by tests/test_highlight_segments.py as the frozen-oracle input

[Data: views.HEX]
in: dict[str, str]
desc: the tone → hex table; soon #fbbf24, over #f43f5e, green #4ade80, mut #8b98a5, ink #e6edf3, pink #f472b6, dim; read by `c()`, `notes_text`, the editor and the report (`report_html._hex`)

[Data: TaskModal._mention]
in: str?
desc: the `@` picker's state: None (closed), "list" or "add"; read by check_action, the two TextArea handlers, on_descendant_focus, action_cancel

[Data: TaskModal._opts]
in: list
desc: the picker's current choices; `drop_move` / `drop_pick` are allowed only when it is not empty (with `_mention` "list")

[I/O: TextArea #f-notes]
in: str
desc: modals.py:570 `TextArea(t.notes if t else "", id="f-notes")` inside `#task-edit`; tcss `#task-box #f-notes { height: 1fr; }` (taskboard.tcss:264); no language, no theme, no highlight query; the repo uses NO TextArea private API (`_highlights`, `_build_highlight_map`, `_theme`: zero hits in taskboard/ and tests/); the raw markers stay visible while typing, the colours show only in the preview

[I/O: Static #task-preview]
in: Text
desc: modals.py:577 the preview beside the notes, inside `VerticalScroll #task-preview-scroll` (can_focus False); composed with `notes_preview(t.notes, board.people)`, re-rendered by on_text_area_changed

[I/O: VerticalScroll #task-preview-scroll]
in: float
desc: the preview's scroll offset; `_follow_cursor` sets `scroll_y` by the cursor line's proportion

[Interface: TaskModal Notes label]
desc: modals.py:568 `Label("Notes  [dim]==…== yellow · !!…!! red · ++…++ green[/dim]", classes="task-sec")` above `#f-notes`; tcss `#task-box .task-sec { color: #8b98a5; }` (taskboard.tcss:261); the only in-editor listing of the syntax; no test pins this text

[Interface: TaskModal Preview label]
desc: modals.py:572 `Label("Preview  [dim]ctrl+v paste · esc cancel[/dim]", classes="task-sec")`; pinned by test_edit_window.py::test_the_editor_paints_its_keys_in_full
offers: "ctrl+v paste" → ClipboardPasteMixin.action_paste_text
offers: "esc cancel" → TaskModal.action_cancel

[Interface: TaskModal title]
desc: modals.py:514 `.modal-title` "Edit task" / "New task" + "  [dim]· ctrl+e emoji[/dim]"
offers: "ctrl+e emoji" → EmojiPickerMixin.action_pick_emoji

[Interface: editor key line]
desc: `Static #task-keys`, `key_line(TASK_KEYS, width - 2)` in TaskModal._fit_width (modals.py:601-607); TASK_KEYS (modals.py:379) = alt+s save, alt+m mark, alt+i image, alt+t start, alt+d due, esc cancel; alt+m dropped when no `#f-mark`; holds no notes-highlight key
offers: "alt+s save" → ButtonKeysMixin.action_press_button
offers: "alt+m mark" → TaskModal.action_mark
offers: "alt+i image" → ButtonKeysMixin.action_press_button
offers: "alt+t start" → ButtonKeysMixin.action_press_button
offers: "alt+d due" → ButtonKeysMixin.action_press_button
offers: "esc cancel" → TaskModal.action_cancel

[Interface: TaskDetails Notes label]
desc: modals.py:2543 in `TaskDetails.compose`: `Label("[b]Notes[/b]  [dim]highlight: ==…== yellow, !!…!! red, ++…++ green[/dim]")`, then `Static(notes_preview(t.notes, board.people))` (2545) or a dim dash

[Interface: focus legend]
desc: `legend_entries("focus", …)` lines views.py:8734-8736: "==text==" soon "highlight: yellow / warning", "!!text!!" over "highlight: red / attention", "++text++" green "highlight: green / resolved"; shown by HelpModal (modals.py:2830) when any task is pinned

[I/O: report task dict]
desc: report_html.extract (report_html.py:98) builds each task's dict: `notes_html` (151) and `notes_text` (152); embedded as JSON in the workspace page and read by report_deck

[I/O: deck CSS]
desc: report_deck.py CSS (384): `.hl-soon{color:var(--soon)} .hl-over{color:var(--over)} .hl-green{color:var(--green)}` (439), `.mention{color:var(--accent);font-weight:600}` (438); vars dark `:root` (385-389: --soon #fbbf24, --over #f43f5e, --green #4ade80), LIGHT (379-382: --soon #8a5a00, --over #c81e4f, --green #1a7f37); no `.hl-mut` rule (inherits ink); consumer `report_deck._notes` (338-344) puts `t["notes_html"]` in `<p class="nl">`

[I/O: workspace CSS]
desc: report_workspace.py CSS (14): `.hl-soon/.hl-over/.hl-green{background:color-mix(in srgb,var(--x) 22%,transparent);border-radius:3px;padding:0 .15em}` (84-86), `.mention` (87); vars dark `:root` (17: --over #f43f5e, --soon #fbbf24, --green #4ade80); the light block (18-21) does NOT redefine --soon/--over/--green; no `.hl-mut` rule; consumers in JS (155): `notes.innerHTML = t.notes_html` (608), the notes section (685-692), the export filter (748)

[Outside: key enter]
desc: TaskModal priority binding `drop_pick` (modals.py:474); gated by check_action

[Outside: key up]
desc: TaskModal priority binding `drop_move(-1)` (modals.py:472); the app's priority `up,k` (cursor) is released while a modal is open (app.py:1309)

[Outside: key down]
desc: TaskModal priority binding `drop_move(1)` (modals.py:473)

[Outside: key tab]
desc: TaskModal priority binding `drop_field` (modals.py:475); not gated (check_action `True`); outside the add form it is `focus_next`; the app's priority `tab` (toggle_presentation) is released while a modal is open

[Outside: key alt+m]
desc: TaskModal priority binding `mark` (modals.py:468); gated by check_action on `#f-mark`

[Outside: key alt+s]
desc: FORM_KEYS `press_button('save')` (modals.py:372), priority

[Outside: key alt+i]
desc: `press_button('paste-img')` (modals.py:469), priority

[Outside: key alt+t]
desc: DATE_KEYS `press_button('cal-f-start')` (modals.py:373), priority

[Outside: key alt+d]
desc: DATE_KEYS `press_button('cal-f-due')` (modals.py:374), priority

[Outside: key printable]
desc: a letter, digit or symbol typed while `#f-notes` has the focus; the TextArea inserts it and posts TextArea.Changed; plain 0-9 are app view keys (keymap.py:65-74, not priority), so in `#f-notes` they type digits

[Outside: key alt+0..alt+9]
desc: FREE: bound nowhere — not in TaskModal.BINDINGS, not in keymap.KEYMAP / app_bindings, not in any other modal; no test names them

[Outside: key alt+c]
desc: FREE in TaskModal and globally; bound only in MarkForm (modals.py:2101 `focus_row('mf-colour')`, a different modal), pinned there by test_marks_manager.py and test_modal_keys.py::test_AT_2604_the_marks_manager_and_its_form_obey_the_modal_key_law

## Edges

[Data: views._HIGHLIGHT_RE] ──▶ highlight_segments
[Data: views.HEX] ──▶ notes_text
[Data: views.HEX] ──▶ _highlight_markup
[I/O: TextArea #f-notes].text ──▶ TaskModal.on_text_area_changed
TaskModal.on_text_area_changed ──▶ [I/O: Static #task-preview]
[I/O: TextArea #f-notes].cursor_location ──▶ TaskModal.on_text_area_selection_changed
TaskModal.on_text_area_selection_changed ──▶ [I/O: VerticalScroll #task-preview-scroll]
[Data: TaskModal._mention] ──▶ TaskModal.check_action
[Data: TaskModal._opts] ──▶ TaskModal.check_action
[Data: TaskModal._mention] ──▶ TaskModal.on_text_area_changed
[Data: TaskModal._mention] ──▶ TaskModal.on_text_area_selection_changed
legend_entries ──▶ [Interface: focus legend]
notes_html ──▶ [I/O: report task dict].notes_html
_notes_text ──▶ [I/O: report task dict].notes_text
[I/O: report task dict].notes_html ──▶ [I/O: deck CSS]
[I/O: report task dict].notes_html ──▶ [I/O: workspace CSS]
[Outside: key printable] ──▶ TaskModal.on_text_area_changed
when: App.focused is `#f-notes` (the TextArea inserts the key and posts TextArea.Changed)
[Outside: key enter] ──▶ TaskModal.check_action
when: TaskModal is the screen; allowed only while `_mention` is "list" with options, or "add" with the focus in `#mdrop`; otherwise the key reaches `#f-notes` as a new line
[Outside: key up] ──▶ TaskModal.check_action
when: TaskModal is the screen; same gate as enter (drop_move)
[Outside: key down] ──▶ TaskModal.check_action
when: TaskModal is the screen; same gate as enter (drop_move)
[Outside: key up] ──▶ TaskModal.on_text_area_selection_changed
when: App.focused is `#f-notes` and check_action("drop_move") is False (the picker closed): the TextArea moves its cursor and posts SelectionChanged
[Outside: key tab] ──▶ TaskModal.check_action
when: TaskModal is the screen; always allowed (drop_field)
[Outside: key alt+m] ──▶ TaskModal.check_action
when: TaskModal is the screen; allowed only when `#f-mark` was composed
[Outside: key alt+s] ──▶ TaskModal.check_action
when: TaskModal is the screen; always allowed
[Outside: key alt+i] ──▶ TaskModal.check_action
when: TaskModal is the screen; always allowed
[Outside: key alt+t] ──▶ TaskModal.check_action
when: TaskModal is the screen; always allowed
[Outside: key alt+d] ──▶ TaskModal.check_action
when: TaskModal is the screen; always allowed
