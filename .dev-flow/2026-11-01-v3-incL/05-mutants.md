| M | Where | Edit applied | Req | Result | First failing test / Notes |
|---|---|---|---|---|---|
| M01 | models.Task | created: field(default_factory=stamp) | LLR-4301.1 | KILLED | tests/test_task_created.py::test_TC_4301_created_is_an_optional_field_that_defaults_to_none |
| M02 | models.Board.add_task | remove the stamp block (closest eq: drop the whole `if task.created is None` stamp) | LLR-4301.2 | KILLED | tests/test_task_created.py::test_TC_4302_a_task_added_in_the_editor_is_stamped |
| M03 | models.Board.add_task | stamp unconditionally (drop `is None` check) | LLR-4301.7 | KILLED | tests/test_task_created.py::test_TC_4307_add_task_keeps_a_created_that_is_already_set |
| M04 | models.Board.add_task | stamp moved after self.save() | LLR-4301.5 | KILLED | tests/test_task_created.py::test_TC_4302_a_task_added_in_the_editor_is_stamped |
| M05 | models.Board.add_task | history.append without at=now | LLR-4301.5 | KILLED | tests/test_task_created.py::test_TC_4305_add_task_stamps_before_the_save_and_the_birth_record_agrees |
| M06 | models.Board.load (seed) | remove the seed stamping | LLR-4301.6 | KILLED | tests/test_task_created.py::test_TC_4306_a_seeded_board_stamps_every_task_with_one_moment |
| M07 | models.Board.load (seed) | stamp() once per task inside the loop | LLR-4301.6 | KILLED | tests/test_task_created.py::test_TC_4306_a_seeded_board_stamps_every_task_with_one_moment |
| M08 | models.Board._to_dict | always write created (delete only on the push path) | LLR-4302.1 | KILLED | tests/test_task_created.py::test_TC_4308_an_edit_keeps_created_as_it_was |
| M09 | models.Board._to_dict | ignore with_created (keep created on the push path) | LLR-4302.7 | KILLED | tests/test_task_created.py::test_TC_4318_the_team_push_carries_no_created |
| M10 | models.Board._to_dict | do not pop extra['created'] on the push path | LLR-4302.7 | KILLED | tests/test_task_created.py::test_TC_4318_the_team_push_carries_no_created |
| M11 | models.Board._serialized | tasks serialized without with_created=True | LLR-4302.1 | KILLED | tests/test_task_created.py::test_TC_4302_a_task_added_in_the_editor_is_stamped |
| M12 | models.Task.from_dict | drop a non-str created instead of keeping it in extra | LLR-4302.3 | KILLED | tests/test_task_created.py::test_TC_4314_a_non_string_created_is_written_back_unchanged |
| M13 | models._rescue_task / from_dict | set created=stamp() on the rescued task | LLR-4301.11 | KILLED | tests/test_task_created.py::test_TC_4311_a_rescued_entry_is_not_stamped |
| M14 | app._on_template_picked | remove created=when (no stamp on template insert) | LLR-4301.3 | KILLED | tests/test_task_created.py::test_TC_4303_a_template_insert_stamps_every_task_with_one_moment |
| M15 | app._on_template_picked | created=stamp() per task inside the loop | LLR-4301.3 | KILLED | tests/test_task_created.py::test_TC_4303_a_template_insert_stamps_every_task_with_one_moment |
| M16 | app.check_action | remove "added_list" from the modal-gated tuple | LLR-4303.21 | KILLED | tests/test_added_list.py::test_TC_4323_N_brings_the_open_list_back_without_a_second_one |
| M17 | app.check_action | remove AddedList from the screens that hold the seat | LLR-4303.22 | KILLED | tests/test_added_list.py::test_TC_4342_the_list_holds_the_seat |
| M18 | app.AddedList.__init__ | show_archived = True (self.app not reachable in __init__) | LLR-4306.2 | KILLED | tests/test_added_list.py::test_TC_4338_an_empty_list_ignores_enter_and_the_arrows |
| M19 | app.AddedList.action_order | keep sel (no reset to 0) | LLR-4304.7 | KILLED | tests/test_added_list.py::test_TC_4367_o_reverses_the_order_and_puts_the_cursor_on_top |
| M20 | app.AddedList.action_archived | always reset the cursor to 0 | LLR-4306.4 | KILLED | tests/test_added_list.py::test_TC_4394_the_toggle_keeps_the_cursor_on_its_task |
| M21 | app.AddedList BINDINGS | remove N from the back binding (escape only) | LLR-4303.4 | KILLED | tests/test_added_list.py::test_TC_4324_escape_or_N_closes_the_list |
| M22 | app.AddedList.action_jump | remove the `if not rows: return` guard | LLR-4303.18 | KILLED | tests/test_added_list.py::test_TC_4338_an_empty_list_ignores_enter_and_the_arrows |
| M23 | app.AddedList.on_screen_resume | delete the method | LLR-4303.11 | KILLED | tests/test_added_list.py::test_TC_4331b_a_name_renamed_under_the_list_shows_when_it_returns |
| M24 | views.added_moment | accept offset-aware (return with tzinfo stripped) | LLR-4304.13 | KILLED | tests/test_added_list.py::test_TC_4373_an_offset_aware_moment_is_not_valid |
| M25 | views.added_moment | except ValueError removed (unparseable raises) | LLR-4304.8 | KILLED | tests/test_added_list.py::test_TC_4368_a_created_that_is_not_a_date_is_no_created |
| M26 | views.added_rows | use the LAST birth record per id instead of the first | LLR-4304.2 | KILLED | tests/test_added_list.py::test_TC_4362_no_created_takes_the_first_birth_record |
| M27 | views.added_rows | narrow the history guard to `except OSError` | LLR-4304.12 | KILLED | tests/test_added_list.py::test_TC_4372b_a_history_file_that_is_not_utf8_gives_no_births |
| M28 | views.added_rows | drop the isinstance(task.id, str) check before the births lookup | LLR-4304.17 | KILLED | tests/test_added_list.py::test_TC_4377_a_task_id_that_is_not_a_string_is_listed_unknown |
| M29 | views.added_rows | prefer the birth record over a valid created | LLR-4304.1 | KILLED | tests/test_task_created.py::test_AT_4302_a_task_added_on_an_old_board_is_first_in_the_list |
| M30 | views.added_order | sort dated rows by `at` only (no lane/pos tie-break) | LLR-4304.4 | KILLED | tests/test_added_list.py::test_TC_4364_ties_break_by_board_order_then_file_position |
| M31 | views.added_order | put unknown rows after dated rows in oldest-first order | LLR-4304.5 | KILLED | tests/test_task_created.py::test_AT_4302_a_task_added_on_an_old_board_is_first_in_the_list |
| M32 | views.added_order | do not filter archived rows when show_archived is False | LLR-4306.1 | KILLED | tests/test_added_list.py::test_TC_4365_unknown_rows_come_first_in_board_then_file_order |
| M33 | views.first_created | include source "h" rows in the minimum | LLR-4304.10 | KILLED | tests/test_added_list.py::test_TC_4370_first_created_is_the_earliest_valid_created |
| M34 | views.state_boxes | exclusive fill (`i` boxes instead of `i + 1`) | LLR-4305.1 | KILLED | tests/test_added_list.py::test_TC_4327_the_body_at_118x30_is_the_designed_capture |
| M35 | views.state_boxes | no 8-box cap (draw n boxes when n > 8) | LLR-4305.2 | KILLED | tests/test_added_list.py::test_TC_4382_more_than_eight_phases_draw_eight_boxes |
| M36 | views._added_row | no padding of the state column to the widest count | LLR-4305.3 | KILLED | tests/test_added_list.py::test_TC_4327_the_body_at_118x30_is_the_designed_capture |
| M37 | views._added_row | state-column filled boxes in HEX["sky"] instead of HEX["ink"] | LLR-4305.4 | KILLED | tests/test_added_list.py::test_TC_4328_a_row_reads_cursor_time_boxes_hue_title |
| M38 | views._added_row | archived title not dimmed (use the normal title style) | LLR-4306.5 | KILLED | tests/test_added_list.py::test_TC_4395_archived_rows_are_dimmed_while_shown |
| M39 | views.added_time_label | drop the `≈` prefix for source h | LLR-4304.9 | KILLED | tests/test_added_list.py::test_TC_4327_the_body_at_118x30_is_the_designed_capture |
| M40 | views.added_source_line | omit ` · #<n> in <board>'s board file` for source ? | LLR-4304.10 | KILLED | tests/test_added_list.py::test_TC_4370_the_source_line_names_how_the_moment_is_known |
| M41 | views._added_plan | no ` ≈` suffix on a history-only day | LLR-4303.9 | KILLED | tests/test_added_list.py::test_TC_4327_the_body_at_118x30_is_the_designed_capture |
| M42 | views._added_head | omit the `archived hidden` / `archived shown` tail | LLR-4306.6 | KILLED | tests/test_added_list.py::test_TC_4327_the_body_at_118x30_is_the_designed_capture |
| M43 | views._added_pane | render notes with Text(task.notes) instead of notes_text | LLR-4303.12 | KILLED | tests/test_added_list.py::test_TC_4327_the_body_at_118x30_is_the_designed_capture |
| M44 | views._added_pane | omit the `after:` line | LLR-4303.13 | KILLED | tests/test_added_list.py::test_TC_4377_a_task_id_that_is_not_a_string_is_listed_unknown |
| M45 | views._added_pane | build the `after:` lookup over all ids (no str filter) | LLR-4304.17 | KILLED | tests/test_added_list.py::test_TC_4377_a_task_id_that_is_not_a_string_is_listed_unknown |
| M46 | views._added_pane | no note cut before the wrap | LLR-4303.12 | KILLED | tests/test_added_list.py::test_TC_4332b_a_huge_note_is_cut_before_it_is_wrapped |
| M47 | views.render_added_list | lw = 46 at every width | LLR-4303.7 | KILLED | tests/test_added_list.py::test_TC_4370_the_source_line_names_how_the_moment_is_known |
| M48 | views._added_top | always top = 0 (no scroll window) | LLR-4303.15 | KILLED | tests/test_added_list.py::test_TC_4335_the_list_scrolls_to_keep_the_cursor_on_screen |
| M49 | views._one_line | return the text unchanged (no flattening) | LLR-4303.8 | KILLED | tests/test_added_list.py::test_TC_4328_a_row_reads_cursor_time_boxes_hue_title |
| M50 | keymap.KEYMAP | remove the `N` entry | LLR-4303.1 | KILLED | tests/test_task_created.py::test_AT_4302_a_task_added_on_an_old_board_is_first_in_the_list |

killed 50 / 50