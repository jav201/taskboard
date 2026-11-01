# E5 mutants — Inc K new arms (results)

Copy: `C:/Users/jjgh8/Github/taskboard-wt/incK-mut` @ `f931070`. Interpreter: `C:/Users/jjgh8/anaconda3/python.exe`.

## BASELINE-RED

None — baseline `325 passed, 0 failed`.

| M | Where | Edit applied | Req | Result | First failing test / Notes |
|---|---|---|---|---|---|
| M01 | keymap.py:KEYMAP | delete `Key("n","n","capture",…)` | LLR-4401.1 | KILLED | test_TC_4401_n_is_one_global_key_declared_after_N_off_the_bar |
| M02 | app.py:check_action | `if action == "capture" and …:` → `if False:` | LLR-4401.19 (ARCH-3) | KILLED | test_TC_4419_capture_is_refused_under_the_boards_home |
| M03 | app.py:check_action | `"capture"):` → `"capture_off"):` | LLR-4401.14 | KILLED | test_TC_4411_capture_is_refused_while_a_modal_is_open |
| M04 | app.py:check_action | `AddedList, CaptureView))` → `AddedList))` | LLR-4401.12 | KILLED | test_TC_4412_the_view_holds_the_seat |
| M05 | app.py:CaptureView.BINDINGS | `priority=True` dropped | LLR-4401.18 | KILLED | test_TC_4418_the_terminal_form_of_an_alt_key_types_nothing |
| M06 | app.py:CaptureView.on_mount | `move_cursor(pad.document.end)` → `move_cursor((0, 0))` | LLR-4401.5 | KILLED | test_TC_4405_the_pad_has_focus_with_the_cursor_at_the_end |
| M07 | inbox.py:DIVIDER_RE | `_{4,}` → `_{3,}` | LLR-4402.1 | KILLED | test_TC_4431_a_divider_is_four_or_more_underscores_and_nothing_else |
| M08 | inbox.py:note_count | `if len(parts) > 1 …:` → `if False:` | LLR-4402.8 | KILLED | test_TC_4438_…[a\n____\n-2] |
| M09 | app.py:PadArea.get_line | drop `line_index != …` | LLR-4402.7 | KILLED | test_TC_4437_the_cursors_divider_shows_its_raw_text |
| M10 | app.py:action_divider | `if line.strip() == "":` → `if False:` | LLR-4402.10 | KILLED | test_TC_4440_alt_l_on_a_blank_line_writes_the_divider_there |
| M11 | app.py:_notice_divider | drop `or self.app._divider_said` → keep `_divider_said` | LLR-4402.15 | KILLED | test_TC_4445_a_stored_flag_keeps_the_notice_away |
| M12 | suggest.py:stem | `w[:6]` → `w[:5]` | LLR-4403.2 | KILLED | test_TC_4462_stems_ies_to_y_drop_final_s_cut_to_six_handles_unstemmed |
| M13 | suggest.py:words | drop `and not w.isdigit()` | LLR-4403.1 | KILLED | test_TC_4461_words_fold_accents_drop_short_words_numbers_and_stop_words |
| M14 | suggest.py:W_NAME.. | `3,2,2,1,1` → `2,2,2,1,1` | LLR-4403.4 | KILLED | test_TC_4464_weights_name_x3_titles_x2_handles_x2_mark_name_x1_notes_x1 |
| M15 | suggest.py:_idf | `log((n+1)/(c+1))+1.0` → `log(n/c)` | LLR-4403.6 | KILLED | test_TC_4466_idf_is_ln_n_plus_1_over_df_plus_1_plus_1 |
| M16 | suggest.py:suggest | `score *= 0.5` → `score *= 1.0` | LLR-4403.8 | KILLED | test_TC_4468_one_shared_stem_halves_the_score_two_do_not |
| M17 | suggest.py:options | `>= MID` → `>= HIGH` | LLR-4403.11 | KILLED | test_TC_4471_a_best_hit_at_or_above_MID_is_the_top_choice |
| M18 | suggest.py:suggest sort | drop `.casefold()` | LLR-4403.9 | KILLED | test_TC_4469_equal_scores_order_by_board_then_casefolded_name_then_name_then_position |
| M19 | app.py:options_for | `suggest(nt.title + "\n" + nt.notes, …)` → `suggest(text, …)` | LLR-4403.28 | KILLED | test_TC_4488b_the_view_scores_a_note_without_its_image_lines |
| M20 | inbox.py:_dump_other | `with file_lock(path, name):` → `with open(os.devnull):` | LLR-4404.9/.13 | KILLED | test_TC_4509_another_board_is_written_fresh_under_its_lock |
| M21 | inbox.py:_dump_other | `fresh.save_atomic()` → `fresh.save()` | LLR-4404.9 | KILLED | test_TC_4509_another_board_is_written_fresh_under_its_lock |
| M22 | inbox.py:_dump_other | drop `created=models.stamp(now),` | LLR-4404.4 | KILLED | test_TC_4504_a_dumped_task_is_stamped_on_both_paths |
| M23 | inbox.py:_dump_other | drop `phase=fresh.phases[0],` | LLR-4404.5 | KILLED | test_TC_4505_a_dumped_task_takes_the_boards_first_phase |
| M24 | inbox.py:_dump_other | delete `history.append(…birth…)` | LLR-4404.32 | KILLED | test_TC_4532_a_dump_writes_one_birth_record |
| M25 | inbox.py:dump_note | delete `note.encode("utf-8")` | LLR-4404.34 (SEC-2) | KILLED | test_TC_4534_a_note_that_will_not_encode_dumps_nothing |
| M26 | inbox.py:_dump_open | `live.projects.remove(project_obj)` → `pass` | LLR-4404.15 | KILLED | test_TC_4515_a_failed_open_board_save_rolls_the_live_board_back |
| M27 | app.py:_dump | `if Path(path).resolve() == …` → `if False` | LLR-4404.8 | KILLED | test_TC_4508_an_open_board_dump_goes_through_the_live_board |
| M28 | app.py:_key | drop `, opt.doc.project_id` from tuple | LLR-4404.17 (ARCH-2) | KILLED | test_TC_4516_alt_o_cycles_the_options_and_wraps |
| M29 | inbox.py:_unchanged | `asdict(task) == asdict(expected)` → `(title, notes) == …` | LLR-4405.10 (SEC-3) | KILLED | test_TC_4550_a_task_changed_in_any_field_is_left_by_the_undo[phase] |
| M30 | inbox.py:last_dump | `result[-1]` → `result[0]` | LLR-4405.1 | KILLED | test_TC_4541b_the_newest_entry_is_undone_first |
| M31 | inbox.py:last_dump | `state["dumped"] if … else self.dumped` → `self.dumped` | LLR-4405.17 | KILLED | test_TC_4557_alt_u_reads_the_files_dumped_list_fresh |
| M32 | inbox.py:last_dump | `result.append(dict(e))` → `pass` | LLR-4405.18 (ARCH-4) | KILLED | test_TC_4558_a_pending_record_is_the_newest_undo |
| M33 | inbox.py:_needed | `return any(…)` → `return False` | LLR-4405.19 (SEC-3) | KILLED | test_TC_4559_a_task_another_task_depends_on_is_left |
| M34 | app.py:action_undo | `… == norm), None)` → `…, (entry["board"], "", None, ""))` | LLR-4405.16 (SEC-8) | KILLED | test_TC_4556_an_entry_naming_an_unknown_board_undoes_nothing[False] |
| M35 | app.py:ReviewList.on_mount | `[chosen(t) is not None …]` → `[True …]` | LLR-4406.3 | KILLED | test_TC_4563_rows_open_checked_for_a_project_and_unchecked_for_new_project |
| M36 | app.py:ReviewList.action_move | drop `min(len(self.texts) - 1, …)` | LLR-4406.4 | KILLED | test_TC_4564_up_and_down_move_the_cursor_clamped_to_the_rows |
| M37 | app.py:ReviewList.action_toggle | `not self.on[self.sel]` → `True` | LLR-4406.5 | KILLED | test_TC_4565_space_toggles_a_project_rows_check |
| M38 | app.py:ReviewList.action_toggle | `if self.view.chosen(t) is None:` → `if False:` | LLR-4406.6 | KILLED | test_TC_4566_space_on_a_new_project_row_is_refused_with_a_notice |
| M39 | app.py:ReviewList.action_dump | drop `target=targets[t], rebuild=False` | LLR-4406.17 (ARCH-2) | KILLED | test_TC_4577_every_checked_rows_target_is_fixed_before_the_first_dump |
| M40 | inbox.py:union_pads | delete `budget.update(unseen)` | LLR-4407.19 (SEC-1) | KILLED | test_TC_4599_a_changed_file_is_merged_note_by_note |
| M41 | inbox.py:union_pads | `budget[p.text] -= 1` → `pass` | LLR-4407.19 (SEC-1) | KILLED | test_TC_4599_a_changed_file_is_merged_note_by_note |
| M42 | inbox.py:write_pad (inner) | delete `p = _remove_first_note(p, e["text"])` | LLR-4407.48 (ARCH-1) | KILLED | test_TC_4688_a_dumps_record_removes_its_note_from_the_fresh_pad |
| M43 | inbox.py:_commit | `dict(fresh) if fresh is not None else {` → `if False else {` | LLR-4407.4 (ARCH-1) | KILLED | test_TC_4584_each_write_applies_its_change_to_the_file_as_it_is_now |
| M44 | inbox.py:_parse | delete `json.dumps(…).encode("utf-8")` | LLR-4407.43 (SEC-2) | KILLED | test_TC_4683_a_lone_surrogate_in_the_store_makes_it_unreadable |
| M45 | inbox.py:_commit | `except UnicodeError` → `except LookupError` | LLR-4407.44 (SEC-2) | KILLED | test_TC_4684_text_that_will_not_encode_is_refused_as_an_oserror |
| M46 | inbox.py:refresh | `self._stamp = stamp` moved before read | LLR-4407.45 (SEC-4) | KILLED | test_TC_4685_a_failed_read_keeps_the_old_stamp |
| M47 | app.py:action_quit | `if view._flush():` → `if view._flush() or True:` | LLR-4407.46 (SEC-5) | KILLED | test_TC_4686_quit_with_an_unsaved_pad_that_cannot_be_written_warns |
| M48 | inbox.py:load | `fh.read(STORE_MAX_BYTES + 1)` → `fh.read()` | LLR-4407.35 | SURVIVED | full-file rerun (143 passed) |
| M49 | inbox.py:_commit | `len(data) + text.count("\n") * (len(os.linesep)-1)` → `len(data)` | LLR-4407.37 | KILLED | test_TC_4677_a_write_over_the_cap_changes_nothing |
| M50 | inbox.py:write_pad (except) | `self.pending.append(("record", record))` → `pass` | LLR-4407.39 (ARCH-4) | KILLED | test_TC_4558_a_pending_record_is_the_newest_undo |
| M51 | inbox.py:write_pad | `ops = list(self.pending)` → `ops = []` | LLR-4407.41 (ARCH-4) | KILLED | test_TC_4598b_a_pending_record_makes_an_unchanged_pad_write |
| M52 | inbox.py:_links_ok | `if os.path.islink(…) …:` → `if False:` | LLR-4408.20 (SEC-6) | KILLED | test_TC_4650_no_source_is_removed_through_a_junction |
| M53 | inbox.py:_image_ok | drop `.rstrip(" ")` | LLR-4408.18 (SEC-7) | KILLED | test_TC_4628_an_image_line_names_only_a_bare_safe_image_file[img: con .png] |
| M54 | inbox.py:_copy_images | `copy2` → `move` | LLR-4408.11 | KILLED | test_TC_4621_a_failed_board_save_keeps_every_pad_image |
| M55 | inbox.py:_copy_images | `mkdir()` → `mkdir(exist_ok=True)` | LLR-4408.13 | KILLED | test_TC_4623_an_image_that_cannot_be_moved_stops_the_dump |
| M56 | inbox.py:attach_images | `copy2` → `move` | LLR-4408.3 | KILLED | test_TC_4613_a_clipboard_file_is_copied_never_moved |
| M57 | inbox.py:_images_back | `_free_name(folder, name)` → `name` | LLR-4408.16 | KILLED | test_TC_4626_an_undone_dump_moves_its_images_back_renamed_when_taken |
| M58 | inbox.py:_task_fields | `strip_controls(notes)` → `notes` | LLR-4409.3 | KILLED | test_TC_4633_control_characters_leave_a_dumped_title_and_notes |
| M59 | app.py:rail_rows.emit | `r.append(…)` → `r.append_text(Text.from_markup(…))` | LLR-4409.4 | KILLED | test_TC_4634_markup_in_notes_projects_and_boards_draws_literally |
| M60 | inbox.py:write_pad | delete `pad = strip_controls(pad)` | LLR-4409.5 | KILLED | test_TC_4635_the_pad_is_stored_without_control_characters |

killed 59 / 60 (NOT JUDGED: none)
