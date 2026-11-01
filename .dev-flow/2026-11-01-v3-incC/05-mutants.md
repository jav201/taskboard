# Mutants — Inc C new arms

| M | Where | Edit applied | Req | Result | First failing test / Notes |
|---|---|---|---|---|---|
| M01 | views.PEN_CODES | swapped the tones of `b` and `v` (`b`→violet, `v`→blue) | LLR-4201.1 | KILLED | test_TC_4201_each_code_colours_its_inner_text_in_its_tone[b] |
| M02 | views.colour_spans | `inner_start = om.start(2)` so the opener's optional space stays in the text | LLR-4201.2 | KILLED | test_TC_4201_each_code_colours_its_inner_text_in_its_tone[r] |
| M03 | views.colour_spans | `inner_end = j` (no space dropped before the closer) | LLR-4201.2 | KILLED | test_TC_4201_each_code_colours_its_inner_text_in_its_tone[r] |
| M04 | views.colour_spans | unclosed opener (nl≥0 or j<0) → `pos = om.end(); continue`, no span emitted | LLR-4201.4 | KILLED | test_TC_4204_an_open_span_ends_at_the_line_end |
| M05 | views.colour_spans | `_OPENER_RE` code class changed to `[a-z]` | LLR-4201.5 | KILLED | test_TC_4205_a_colon_pair_that_opens_nothing_stays_literal[::x:: t ::] (KeyError on `x`) |
| M06 | views.colour_spans | removed the `_OPENER_RE.match(text, j)` branch (only a closer ends a span) | LLR-4201.6 | KILLED | test_TC_4206_the_next_opener_ends_the_open_span_keeping_its_space |
| M07 | views.colour_spans | `:::<c>::` branch: dropped the `and _OPENER_RE.match(text, j+1)` check (kept `text[j:j+3]==":::"`) | LLR-4201.6 / ARCH-11 | KILLED | test_TC_4206_the_next_opener_ends_the_open_span_keeping_its_space |
| M08 | views.highlight_segments | gap text emitted with the previous span's tone (tracked `prev`, incl. trailing tail) | LLR-4201.9 | KILLED | test_TC_4202_one_space_beside_each_marker_belongs_to_the_marker[a ::b:: x :: c-segments0] |
| M09 | views.highlight_segments | deleted the `if sp.start > last` gap append (text between spans dropped) | LLR-4201.9 | KILLED | test_TC_4202_one_space_beside_each_marker_belongs_to_the_marker[a ::b:: x :: c-segments0] |
| M10 | views.legend_entries | removed the focus legend colour row (`:: … ::` swatch) | LLR-4202.8 | KILLED | test_TC_4219_the_focus_legend_lists_the_six_codes_in_their_tones |
| M11 | report_deck CSS | deleted `.hl-blue{color:var(--blue)} ` from the tone-class line | LLR-4202.6 | KILLED | test_TC_4217_the_deck_defines_the_three_new_tone_classes_in_both_themes |
| M12 | report_deck CSS | LIGHT `--blue:#0969da` → `--blue:#60a5fa` | LLR-4206.5 | KILLED | test_TC_4224_the_decks_tone_variables_read_on_their_themes_background |
| M13 | report_workspace CSS | deleted the `.hl-violet{…}` rule | LLR-4202.7 | KILLED | test_TC_4218_the_workspace_defines_the_new_tones_like_hl_soon |
| M14 | modals._unshadow_alt_digits | `return` as the first statement (no-op) | LLR-4203.16 | KILLED | test_TC_4249_esc_digit_parses_as_alt_digit_after_the_import |
| M15 | modals TaskModal.action_pen | `pair = f"::{code}::::"` (no two spaces) | LLR-4203.1 | KILLED | test_TC_4230_alt_n_opens_a_spaced_pair_with_the_cursor_inside[pilot] |
| M16 | modals TaskModal.action_pen | removed the `if not notes.has_focus: return` guard | LLR-4203.10 | KILLED | test_TC_4240_a_pen_key_outside_the_notes_changes_no_field[alt+5-5] |
| M17 | modals TaskModal.action_pen | removed the `for s in colour_spans(…): if s.start < col < s.end: notify; return` refusal | LLR-4203.12 | KILLED | test_TC_4252_a_pen_refuses_where_it_would_change_written_text[::r:: ab ::-cursor0-alt+5-Pens write new text — use alt+c to recolour.] |
| M18 | modals TaskModal.action_pen | removed the visible-text check (the `highlight_segments` equality guard) | LLR-4203.17 | KILLED | test_TC_4252_a_pen_refuses_where_it_would_change_written_text[b:: x-cursor3-alt+1-That colour would change the text you see: nothing changed.] |
| M19 | modals TaskModal.action_pen | removed the `if i == self.pen: return` guard | LLR-4203.15 | KILLED | test_TC_4255_the_same_pen_key_again_changes_nothing |
| M20 | modals TaskModal._lift_pen | empty-span branch replaced with `pass` (no removal) | LLR-4203.6 | KILLED | test_TC_4235_lifting_an_empty_pen_removes_its_span[x-keys0-x] |
| M21 | modals TaskModal._lift_pen | no-closer branch replaced with `pass` (no ` ::` inserted) | ARCH-10 | KILLED | test_TC_4258_lifting_a_span_with_no_closer_writes_the_closer |
| M22 | modals TaskModal.action_pen_enter | insert plain `"\n"` instead of `" ::\n::{code}:: "` | LLR-4203.7 | KILLED | test_TC_4236_enter_under_a_pen_continues_the_pen_on_the_next_line |
| M23 | modals TaskModal._pen_follow | removed `self.pen = None` (pen never turned off) | LLR-4203.8 | KILLED | test_TC_4236_leaving_the_fresh_span_after_enter_removes_it |
| M24 | modals TaskModal._pen_follow | removed the `notes.replace("", (row0, target.start), (row0, target.end))` removal | LLR-4203.14 | KILLED | test_TC_4236_leaving_the_fresh_span_after_enter_removes_it |
| M25 | modals TaskModal._save | removed the `self._lift_pen()` call before reading the notes | LLR-4203.11 | KILLED | test_TC_4241_saving_with_an_empty_pen_saves_no_empty_span |
| M26 | modals ink_highlights | marker segments painted `f"pen.{tone}"` instead of `"pen.mark"` | LLR-4204.2 | KILLED | test_TC_4243_the_markers_are_painted_dim |
| M27 | modals ink_highlights | `ba, bb = a, b` (str offsets) instead of `off[a], off[b]` | LLR-4204.5 | KILLED | test_TC_4245_the_ink_colours_exactly_the_tokenisers_ranges |
| M28 | modals InkArea | mutate `TextAreaTheme.get_builtin_theme("css").syntax_styles` and set `self.theme = "css"` instead of a private theme | LLR-4204.6 | KILLED | test_TC_4247_the_ink_never_touches_another_text_area |
| M29 | modals InkArea._build_highlight_map | removed the outer `try/except Exception` fallback | LLR-4204.8 | KILLED | test_TC_4251_an_ink_that_raises_leaves_the_editor_working |
| M30 | modals ink_highlights | strict `ch.encode("utf-8")` in `_byte_offsets` (the `surrogatepass` lives there, not in `ink_highlights` itself) | LLR-4204.9 | KILLED | test_TC_4246_ink_offsets_are_utf8_bytes_even_for_a_lone_surrogate |
| M31 | modals colour_target | word branch → `a, b = 0, len(line)` (whole line) | LLR-4205.2 | KILLED | test_TC_4261_the_target_is_the_selection_or_the_word_and_never_crosses_an_edge[lines0-start0-end0-target0-None] |
| M32 | modals recolour | plain wrap without spaces (`::c::text::`) | LLR-4205.4 | KILLED | test_TC_4263_recolour_rewrites_the_target_or_its_span[the plan works\|r] |
| M33 | modals recolour | inside a span: wrap the target (a,b) again, keeping the old markers | LLR-4205.5 | KILLED | test_TC_4263_recolour_rewrites_the_target_or_its_span[go ::o::now:: ok\|r] |
| M34 | modals recolour | code 0: `line[:s.start] + inner + line[s.inner_end:]` (opener removed, closer kept) | LLR-4205.6 | KILLED | test_TC_4263_recolour_rewrites_the_target_or_its_span[x ::b:: y :: z\|0] |
| M35 | modals colour_target | removed the `if start[0] != end[0]: return None, n1` guard | LLR-4205.10 | KILLED | test_TC_4261_the_target_is_the_selection_or_the_word_and_never_crosses_an_edge[lines10-start10-end10-None-Colour one line at a time.] |
| M36 | modals colour_target | removed the partial-overlap check (span loop → `pass`) | LLR-4205.11 | KILLED | test_TC_4261_the_target_is_the_selection_or_the_word_and_never_crosses_an_edge[lines12-start12-end12-None-The selection crosses a colour edge: select inside one colour, or plain text.] |
| M37 | modals TaskModal._apply_colour | removed the visible-text check (the `highlight_segments` equality guard) | LLR-4205.15 | KILLED | test_TC_4285_a_rewrite_that_changes_the_visible_text_is_refused[std::vector-kw0] |
| M38 | modals TaskModal.action_colour | `self._lift_pen()` moved before `s = self._pen_span()` | LLR-4205.14 / ARCH-3 | KILLED | test_TC_4274_alt_c_under_a_pen_targets_the_pens_span[now-setup1-3-::y:: go ::now] |
| M39 | modals palette_offset | `box_x = x - 1`, `box_y = y + 1` (no clamping) | LLR-4205.13 | KILLED | test_TC_4273_the_box_sits_next_to_the_target_and_on_screen[70-20-80-24-box1] |
| M40 | modals ColourPalette | `escape` binding → `pick('0')` instead of `cancel` | LLR-4205.8 | KILLED | test_TC_4268_esc_compares_with_the_notes_at_palette_open |

killed 40 / total 40
