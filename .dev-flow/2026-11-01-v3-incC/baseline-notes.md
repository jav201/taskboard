# Baseline notes — notes highlight slice at 0a8dfaa

**Counts:** 12 nodes, 28 entities, 27 edges. `codewire_lint` exit 0 (0 lines not read); `codewire_marks` 12 marks, 0 nodes without code; `codewire_extract --path views.py,report_html.py,modals.py` exit 0, 0 findings, 8 calls between marked nodes. Lines below are at 0a8dfaa (unmarked). The lines in extract-baseline.txt are in the marked tree, so they run a few lines later.

**Callers of `highlight_segments`:** views.py:3569 `notes_text`, :3586 `_highlight_markup`, :6719 `present_note_lines`; report_html.py:50 `notes_html`, :61 `_notes_text`. Outside the slice (prototypes/, not product code): html_report/variant_a/build.py:171, variant_b/build.py:44, variant_c/build.py:96, people_round/proto.py:160. capture_round/proto.py:1191 keeps `views.highlight_segments` as a value (`_ORIG_SEG`) and defines `highlight_segments_6` (:1194, six pens adding `::` blue, `^^` violet, `%%` orange). The extractor does not see that as a call.
**Indirect callers:** `_highlight_markup` ← `_focus_note_snippet` views.py:3600, `_focus_detail_lines` :3643, `_focus_tiles` :3800, `_focus_review` :3971. `_focus_note_snippet` ← `_focus_cards` :3690. `notes_text` ← `notes_preview` modals.py:368, `_task_rows` views.py:9049. `notes_preview` ← `TaskModal.compose` modals.py:577, `TaskModal.on_text_area_changed` :618, `TaskDetails.compose` :2545. `present_note_lines` ← `_present_column` views.py:7024, `render_present` :7246. `notes_html` / `_notes_text` ← `report_html.extract` :151 / :152. `legend_entries` ← `HelpModal` modals.py:2830.

**Where the syntax is listed to the user:**
- modals.py:568: TaskModal `.task-sec` label `Notes  [dim]==…== yellow · !!…!! red · ++…++ green[/dim]`. No test pins this text.
- modals.py:2543: `TaskDetails` label `[b]Notes[/b]  [dim]highlight: ==…== yellow, !!…!! red, ++…++ green[/dim]`.
- views.py:8734-8736: `legend_entries` in mode `focus` gives `==text==` "highlight: yellow / warning", `!!text!!` "red / attention", `++text++` "green / resolved". It lists them whenever any task is pinned, even when no note holds a highlight (probe P-2).
- README.md:247 and REQUIREMENTS.md:8 (HLR-002) describe the syntax in the docs. Docstrings views.py:3506 and :3583 are not user-facing.
- A related vocabulary: views.py:353-356 `PRIORITY_BADGE` reuses `!!` (over) and `==` (soon) as priority badges.

**Textual private API on TextArea:** none. `_highlights`, `_build_highlight_map` and `.theme` / `_theme` have zero hits in taskboard/ and tests/. `#f-notes` is a plain `TextArea(text, id="f-notes")` with no language and no theme. The raw markers stay visible while typing; only `#task-preview` shows colour.

**alt keys:**
- alt+0 … alt+9 are FREE everywhere: not in TaskModal.BINDINGS, not in keymap.KEYMAP / app_bindings, not in any modal.
- Plain 0-9 are app view keys (keymap.py:65-74, not priority). In `#f-notes` they type digits.
- alt+c is FREE in TaskModal and globally. It is bound only in `MarkForm` (modals.py:2101, `focus_row('mf-colour')`).
- TaskModal holds:
  - esc;
  - ctrl+v, ctrl+e (priority);
  - alt+s, alt+t, alt+d, alt+m, alt+i (priority);
  - up, down, enter, tab (priority, show=False).
- `check_action` gates three of them. `mark` acts only when `#f-mark` is composed. `drop_move` / `drop_pick` act only while `_mention` is "list" with options, or "add" with the focus in `#mdrop`. Every other action returns True. App.check_action releases the app's priority cursor/hmove/tab while a modal is open (app.py:1309).

**Design facts for the prototype:**
- A new tone needs a `HEX[tone]` entry: `notes_text` indexes `HEX[tone]` and raises KeyError without one.
- A new tone also needs `.hl-<tone>` CSS in BOTH report_deck.py:439 and report_workspace.py:84-86. `notes_html` writes `class="hl-<tone>"` straight from the tone name.
- Neither CSS has a `.hl-mut` rule.
- report_workspace's light block (:18-21) does not redefine `--soon`, `--over` or `--green`. report_deck's `LIGHT` (:379-382) does.
- `present_note_lines` maps `mut` to `ink`.

**Guards (tests that pin highlight behaviour):**
- tests/test_highlight_segments.py::test_TC_417_the_board_markup_is_unchanged (frozen oracle; imports `_HIGHLIGHT_RE`), ::test_TC_417_segments_drop_markers_and_keep_text
- tests/test_present_note_highlights.py::test_AT_2901_gantt_cursor_note_colours_highlights, ::test_AT_2902_split_view_colours_highlights_two_sizes, ::test_AT_2903_split_export_svg_carries_tones, ::test_AT_2904_mentions_bullets_unpaired_markers, ::test_AT_2905_the_regression_pin, ::test_L0_marker_free_twin_wraps_identically, ::test_L0_cut_seat_k1_paints_lead_span_and_tag, ::test_L0_unicode_whitespace_at_wrap_boundaries
- tests/test_focus.py::test_note_highlights_are_rendered
- tests/test_edit_window.py::test_the_preview_paints_the_note_on_open, ::test_the_preview_follows_the_typing_to_the_last_line, ::test_the_preview_paints_markup_typed_in_a_note_as_text, ::test_the_editor_paints_its_keys_in_full
- tests/test_people_look.py::test_TC_2506_the_preview_draws_a_known_mention_as_its_name_in_pink, ::test_TC_2506_an_unknown_handle_stays_as_typed_and_dimmed, ::test_TC_2506_without_a_directory_the_preview_is_unchanged, ::test_TC_2506_present_lines_write_the_name_and_never_split_it
- tests/test_report_html.py::test_TC_3115_embed_json_and_notes_are_inert (`hl-soon`, `hl-mut mention`)
- tests/test_legend.py::test_no_entry_describes_a_mark_the_view_is_not_drawing (weak for `==text==`)
- Key guards: tests/test_people_picker.py::test_TC_2503_closed_the_arrows_move_the_cursor, ::test_TC_2503_with_no_one_listed_enter_is_a_new_line; tests/test_marks_manager.py::test_TC_2605_an_empty_directory_composes_no_select; tests/test_modal_keys.py::test_TC_2407_every_modal_is_in_the_inventory, ::test_AT_2407_alt_s_saves_and_letters_type, ::test_AT_2604_the_marks_manager_and_its_form_obey_the_modal_key_law (pins `alt+c` in MarkForm)

**Probes (run on incC-marks, `taskboard.__file__` = incC-marks):**
- P-1:
  - `_highlight_markup("")` → `[#8b98a5][/]`
  - `_focus_note_snippet("==a== b\nsecond", 40)` → `[#fbbf24]a[/][#8b98a5] b …[/]`
  - `present_note_lines("- ==alpha== bravo", 40)` → `[("• ", [("alpha","soon"),(" bravo","ink")])]`
  - `_notes_text("==a== !!b!!\n++c++")` → `"a b\nc"`
- P-2: `legend_entries("focus", board)` with one pinned task → the spine and the three highlight lines. With no pinned task → `[]`.

The `# node:` marks remain uncommitted in incC-marks (12 lines in views.py, report_html.py, modals.py).
