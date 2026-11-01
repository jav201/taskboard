# Inc L — RED on base (E4, independent tester)

**State: `executed`** (RED on base only; GREEN is `not-run` — the product code is being written in parallel and these tests were never run in the worktree).

- Base: `C:/Users/jjgh8/Github/taskboard-wt/incL-base`, HEAD `eb411e1c38f39763c64c1cff925d330dc3754df5`, `taskboard.__file__` = `C:\Users\jjgh8\Github\taskboard-wt\incL-base\taskboard\__init__.py` (first line of the transcript).
- Command (one complete run, cwd = base, the three test files copied in, deleted afterwards):
  `env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -p no:cacheprovider tests/test_task_created.py tests/test_added_list.py -rA`
- Transcript: `evidence/red-base.txt` (exit 1, `90 failed, 4 passed in 23.66s`).

## Files (worktree `tests/`, not committed)

| File | Functions | Nodes | RED on base | Passed on base | Errors |
|---|---|---|---|---|---|
| `tests/test_task_created.py` | 20 | 22 (TC-4315 ×3) | 18 | 4 | 0 |
| `tests/test_added_list.py` | 71 | 72 (TC-4339 ×2) | 72 | 0 | 0 |
| `tests/added_list_fixture.py` | fixture module (F-V, S registry, clocks, `need()`, pilot readers) | — | — | — | — |
| **Total** | 91 | **94** | **90** | **4** | **0** |

0 collection errors: every new name (`models.stamp`, `Task.created`, `Board._to_dict(…, with_created=)`, `views.added_rows / added_moment / added_order / first_created / state_boxes / render_added_list / AddedRow`, the `AddedList` screen) is reached through `added_list_fixture.need` / `created_of` / `_record` / `open_list`, which fail with a message.

## Why each RED fails on base (tally from one `--tb=no -rf` run of the same files, scratch)

| Reason | Tests |
|---|---|
| `taskboard.views.added_rows missing` | 34 (layer 0) |
| `` `N` opened no list view `` (`open_list`, right after `N`) | 27 (26 from the main screen, 1 from the home: TC-4324b) |
| `Task.created missing: the dataclass has no created field` | 10 (TC-4301, 4307..4314, 4318) |
| behavioural: the file / record holds no `created` (`None`, `0 == 16`) | 7 (TC-4302, 4303, 4304, 4305, 4306, AT-4302, AT-4303) |
| `views.added_moment` / `AddedRow` / `state_boxes` / `render_added_list` / `models.stamp` missing | 3 / 2 / 2 / 1 / 1 |
| behavioural: no KEYMAP `N` (TC-4321); README row after `A` is `@` (TC-4343); `check_action("added_list")` True under a modal (TC-4341) | 3 |

## Guards that PASS on base (4) — by design

| Node | Why it is a guard | What turns it RED |
|---|---|---|
| `test_task_created.py::test_TC_4315_an_old_board_keeps_the_bytes_eb411e1_writes[plain]` | LLR-4302.4: an old board's bytes after load+save equal the base oracle — base writes them too | `_to_dict` writing `"created": null` (or any back-fill) |
| `…[legacy]` | same; oracle = the 761-byte LF literal captured in the base tree (sha256 `fa38dbd0…`, = group D's), frozen in the test (P-D-1) | same |
| `…[unknown]` | same; oracle = the input (741 bytes LF), `zz` first | same |
| `test_task_created.py::test_TC_4316_an_add_leaves_every_old_entry_as_it_was` | LLR-4302.5: base never touches other entries on an add | a save-time back-fill from the `ta` birth record (ARCH-2, HLR-4302's NC) |

No test of `test_added_list.py` passes on base.

## TC → LLR / AT map (every node by its real name)

`test_task_created.py`

| Test | TC | Covers |
|---|---|---|
| test_TC_4301_created_is_an_optional_field_that_defaults_to_none | TC-4301 | LLR-4301.1 |
| test_TC_4302b_the_stamp_is_local_time_to_the_second | TC-4302b | stamp node; LLR-4301.2..6 (format) |
| test_TC_4302_a_task_added_in_the_editor_is_stamped | TC-4302 | LLR-4301.2 |
| test_TC_4303_a_template_insert_stamps_every_task_with_one_moment | TC-4303 | LLR-4301.3 |
| test_TC_4304_the_link_pickers_create_row_stamps_the_new_task | TC-4304 | LLR-4301.4 |
| test_TC_4305_add_task_stamps_before_the_save_and_the_birth_record_agrees | TC-4305 | LLR-4301.5 (+P-D-4) |
| test_TC_4306_a_seeded_board_stamps_every_task_with_one_moment | TC-4306 | LLR-4301.6 |
| test_TC_4307_add_task_keeps_a_created_that_is_already_set | TC-4307 | LLR-4301.7 |
| test_TC_4308_an_edit_keeps_created_as_it_was | TC-4308 | LLR-4301.8 |
| test_TC_4309_a_project_move_keeps_each_moved_tasks_created | TC-4309 | LLR-4301.9 |
| test_TC_4310_undo_restores_a_deleted_task_with_its_created | TC-4310 | LLR-4301.10 |
| test_TC_4311_a_rescued_entry_is_not_stamped | TC-4311 | LLR-4301.11 |
| test_TC_4312_created_is_written_only_when_set | TC-4312 | LLR-4302.1 |
| test_TC_4313_a_string_created_is_read_as_it_is | TC-4313 | LLR-4302.2 |
| test_TC_4314_a_non_string_created_is_written_back_unchanged | TC-4314 | LLR-4302.3 |
| test_TC_4315_an_old_board_keeps_the_bytes_eb411e1_writes[plain/legacy/unknown] | TC-4315 | LLR-4302.4, HLR-4302 (guard) |
| test_TC_4316_an_add_leaves_every_old_entry_as_it_was | TC-4316 | LLR-4302.5, HLR-4302 NC (guard) |
| test_TC_4318_the_team_push_carries_no_created | TC-4318 | LLR-4302.7 (SEC-1; `_to_dict` default, `_serialized`, a real `TeamState.push`) |
| test_AT_4302_a_task_added_on_an_old_board_is_first_in_the_list | AT-4302 | HLR-4301, LLR-4302.5, LLR-4304.6/.9/.10 |
| test_AT_4303_a_template_insert_lists_its_tasks_with_one_time | AT-4303 | HLR-4301, LLR-4301.3, LLR-4304.4 |

`test_added_list.py`

| Test | TC | Covers |
|---|---|---|
| test_TC_4317_the_open_list_writes_no_board_and_no_history | TC-4317 | LLR-4302.6 |
| test_TC_4321_N_is_one_global_key_of_the_seat | TC-4321 | LLR-4303.1 |
| test_TC_4322_N_opens_the_list_view | TC-4322 | LLR-4303.2 |
| test_TC_4323_N_brings_the_open_list_back_without_a_second_one | TC-4323 | LLR-4303.3, LLR-4303.5 (same instance) |
| test_TC_4324_escape_or_N_closes_the_list | TC-4324 | LLR-4303.4 |
| test_TC_4324_N_on_the_home_opens_over_it_and_N_closes_it | TC-4324 | LLR-4303.2, LLR-4303.4 |
| test_TC_4325_the_list_reads_every_board_of_the_registry | TC-4325 | LLR-4303.5 |
| test_TC_4326_the_head_counts_boards_not_read | TC-4326 | LLR-4303.6 (layer 0, styles) |
| test_TC_4326_a_board_whose_file_is_missing_is_counted_not_read | TC-4326 | LLR-4303.6 (pilot) |
| test_TC_4327_the_body_at_118x30_is_the_designed_capture | TC-4327 (+4328/4329/4330) | LLR-4303.7, .8, .9, .10, HLR-4303 |
| test_TC_4327_the_body_at_80x24_is_the_designed_capture | TC-4327 | LLR-4303.7, .11 (wrap), LLR-4304.14 (degrade) |
| test_TC_4327_the_separator_follows_the_terminal_width | TC-4327 | LLR-4303.7 (pilot, resize) |
| test_TC_4328_a_row_reads_cursor_time_boxes_hue_title | TC-4328 | LLR-4303.8 (+P-V-9) |
| test_TC_4329_day_headers_newest_first | TC-4329 | LLR-4303.9 |
| test_TC_4330_the_pane_heads_with_title_chip_meta_source_and_rule | TC-4330 | LLR-4303.10 |
| test_TC_4331_the_meta_line_holds_every_fact_the_task_has | TC-4331 | LLR-4303.11 |
| test_TC_4331b_a_name_renamed_under_the_list_shows_when_it_returns | TC-4331b | LLR-4303.11 (A-1) |
| test_TC_4332_notes_are_drawn_through_notes_text_never_as_markers | TC-4332 | LLR-4303.12 |
| test_TC_4332b_a_huge_note_is_cut_before_it_is_wrapped | TC-4332b | SEC-4 / A-3 (LLR-4303.12) |
| test_TC_4333_the_pane_lists_urls_images_and_what_the_task_waits_on | TC-4333 | LLR-4303.13 |
| test_TC_4334_up_and_down_move_the_cursor_clamped | TC-4334 | LLR-4303.14 |
| test_TC_4335_the_list_scrolls_to_keep_the_cursor_on_screen | TC-4335 | LLR-4303.15 |
| test_TC_4335_a_note_longer_than_the_pane_ends_with_a_count | TC-4335/4335b | P-V-7, A-3 |
| test_TC_4336_enter_opens_the_task_on_its_board | TC-4336 | LLR-4303.16 |
| test_TC_4336b_enter_on_another_boards_task_switches_to_it | TC-4336b | LLR-4303.16 |
| test_TC_4336d_enter_on_a_board_whose_file_went_missing_says_so | TC-4336d | LLR-4303.16 |
| test_TC_4337_an_empty_list_says_so | TC-4337 | LLR-4303.17 |
| test_TC_4338_an_empty_list_ignores_enter_and_the_arrows | TC-4338 | LLR-4303.17, LLR-4303.18 |
| test_TC_4339_the_key_row_shows_every_key_the_view_binds[size0/size1] | TC-4339 | LLR-4303.19 (A-2) |
| test_TC_4340_board_text_that_looks_like_markup_is_drawn_literally | TC-4340 | LLR-4303.20 |
| test_TC_4341_added_list_is_refused_under_a_modal | TC-4341 | LLR-4303.21 (P-S-1) |
| test_TC_4342_the_list_holds_the_seat | TC-4342 | LLR-4303.22 |
| test_TC_4343_the_readme_key_table_has_a_row_for_N | TC-4343 | LLR-4303.23 |
| test_TC_4344_enter_on_an_archived_task_says_so_and_selects_nothing | TC-4344 | LLR-4303.24 |
| test_TC_4344b_enter_on_another_boards_archived_task_switches_then_says_so | TC-4344b | LLR-4303.24 |
| test_TC_4361_a_valid_created_is_the_moment_even_with_a_birth_record | TC-4361 | LLR-4304.1 |
| test_TC_4362_no_created_takes_the_first_birth_record | TC-4362 | LLR-4304.2 |
| test_TC_4363_neither_created_nor_birth_is_unknown | TC-4363 | LLR-4304.3, LLR-4303.5 (rows) |
| test_TC_4364_ties_break_by_board_order_then_file_position | TC-4364 | LLR-4304.4 (ARCH-1 shuffled) |
| test_TC_4365_unknown_rows_come_first_in_board_then_file_order | TC-4365 | LLR-4304.5 |
| test_TC_4365b_with_archived_shown_unknowns_stay_in_board_then_file_order | TC-4365b | LLR-4304.5 |
| test_TC_4366_the_list_opens_newest_first | TC-4366 | LLR-4304.6 (pilot) |
| test_TC_4366b_newest_first_is_the_exact_reverse | TC-4366b | LLR-4304.6 |
| test_TC_4367_o_reverses_the_order_and_puts_the_cursor_on_top | TC-4367 | LLR-4304.7 |
| test_TC_4368_a_created_that_is_not_a_date_is_no_created | TC-4368 | LLR-4304.8 |
| test_TC_4369_time_labels_say_how_the_moment_is_known | TC-4369 | LLR-4304.9 |
| test_TC_4370_first_created_is_the_earliest_valid_created | TC-4370 | LLR-4304.10 (first date) |
| test_TC_4370_the_source_line_names_how_the_moment_is_known | TC-4370 | LLR-4304.10 |
| test_TC_4371_with_no_valid_created_anywhere_unknowns_sit_before_any_record | TC-4371 | LLR-4304.11 (+ARCH-8) |
| test_TC_4372_a_history_read_that_raises_oserror_gives_no_births | TC-4372 | LLR-4304.12 |
| test_TC_4372b_a_history_file_that_is_not_utf8_gives_no_births | TC-4372b | LLR-4304.12 |
| test_TC_4372c_a_deeply_nested_history_line_gives_no_births | TC-4372c | LLR-4304.12 (SEC-2) |
| test_TC_4373_an_offset_aware_moment_is_not_valid | TC-4373 | LLR-4304.13 |
| test_TC_4373b_a_zulu_or_pre_1970_offset_moment_is_none_without_raising | TC-4373b | LLR-4304.13 |
| test_TC_4374_the_head_names_the_order_and_the_legend | TC-4374 | LLR-4304.14 |
| test_TC_4375_with_no_valid_created_the_unknown_source_line_names_no_date | TC-4375 | LLR-4304.15 |
| test_TC_4377_a_task_id_that_is_not_a_string_is_listed_unknown | TC-4377 | LLR-4304.17 (SEC-3) |
| test_TC_4381_boxes_fill_up_to_and_including_the_phase | TC-4381 | LLR-4305.1 |
| test_TC_4382_more_than_eight_phases_draw_eight_boxes | TC-4382 | LLR-4305.2 |
| test_TC_4383_the_state_column_is_as_wide_as_the_widest_board | TC-4383 | LLR-4305.3 |
| test_TC_4384_the_state_column_is_ink_and_dim_only | TC-4384 | LLR-4305.4 |
| test_TC_4391_archived_tasks_are_left_out_while_hidden | TC-4391 | LLR-4306.1 |
| test_TC_4392_the_list_opens_with_archived_hidden_whatever_v_says | TC-4392 | LLR-4306.2 |
| test_TC_4393_v_toggles_archived_tasks_both_ways | TC-4393 | LLR-4306.3 |
| test_TC_4394_the_toggle_keeps_the_cursor_on_its_task | TC-4394 | LLR-4306.4 (P-S-8) |
| test_TC_4395_archived_rows_are_dimmed_while_shown | TC-4395 | LLR-4306.5 |
| test_TC_4396_the_head_ends_with_the_archived_state | TC-4396 | LLR-4306.6 |
| test_TC_4397_the_meta_line_says_archived | TC-4397 | LLR-4306.7 |
| test_AT_4301_one_list_of_every_board_newest_first | AT-4301 | HLR-4303..4305, LLR-4302.6 |
| test_AT_4304_the_archived_toggle | AT-4304 | HLR-4306 |
| test_AT_4305_old_tasks_are_inferred_honestly_and_never_rewritten | AT-4305 | HLR-4302, HLR-4304 |

**Coverage check.** Active LLRs with at least one test: 4301.1–.11 (11/11), 4302.1–.7 (7/7), 4303.1–.24 (24/24), 4304.1–.15 + .17 (16/16; .16 withdrawn, no test by design), 4305.1–.4 (4/4), 4306.1–.7 (7/7) = **69/69**. ATs: AT-4301..AT-4305 = **5/5**, each in exactly one node. **Uncovered: none.**

## Disagreements with the graph / notes for the reviewers

1. **None of S's post-`N` examples could run on base** (ARCH-4): every pilot stops at `open_list` because `N` opens nothing, and every layer-0 test stops at a missing name. So the RED proves that each test CAN fail; it does NOT check the D/V/S expected strings themselves. They stay `planned` until the orchestrator's GREEN run. I found no example that contradicts the requirements while transcribing them (every F-V line was checked for its width: 116/78 cells, `│` once per line; the heads are 108/78 cells, the key rows 71/112, as the graph says).
2. **TC-4323** — the graph says "compose ran 1 time"; the test checks the observable equivalent instead: after `N A N` the screen on top is the SAME object as after the first `N` (no counter on the implementation).
3. **TC-4372** — besides the monkeypatched `history.read` the threshold names, an arm makes `history.jsonl` a folder (a real `PermissionError` through the real read), so a `from .history import read` in views cannot make the monkeypatch arm miss. The patch also replaces any `views` attribute that IS `history.read`.
4. **TC-4332b** keeps the design's 50 ms bound (best of 3 paints). It is a timing test; on a loaded machine it could flake. If it does, the bound is the reviewers' call, not mine.
5. **AT-4302 / TC-4312 rely on group D's field position**: a set `created` is written just before `id` (graph-proto-D `[Data: Task dataclass fields]`). The S fixture files are written that way, so a load+save leaves them unchanged. An implementation that writes the key somewhere else fails TC-4312 (key order) and AT-4302 (the `ta1` slice).
6. **TC-4327 pilot** checks both body cell 47 / 35 and screen column 48 at 118x30 (the 1-cell gutter of `padding: 0 1`).
7. **AT-4304's dim check** reads the rendered cells (`Static.render_line`), and the pilots read the body/key row from the Static whose text starts `ADDED` / holds `esc / N`. They do not use the widget ids `#al-body` / `#al-keys`.

## Existing tests that must learn about `N` (NOT edited; per the design they need product/README changes, not test edits)

- `tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat` — RED until the README `N` row exists (LLR-4303.23, group D's README edit).
- `tests/test_keymap.py::test_every_shown_key_has_a_real_action_on_the_app` — RED until `TaskboardApp.action_added_list` exists (group S).
- `tests/test_help_keys.py` — the `?` help's global line grows 3 → 4 rows at 80x24 (P-D-8), stated GREEN by group D with the seat patched.

## Limits (environment, scope)

- GREEN `not-run` (product code in flight; I never ran anything in the worktree).
- One platform: Windows, Python 3.12 (anaconda), Textual 8.2.8. The byte oracle is LF-frozen and compared as `os.linesep` bytes (what `write_text` writes), so it holds on POSIX too, but that was not run.
- The 3 test files and the probe were deleted from the base tree after the run (`git status` clean). Byte-code caches of BASE files (`tests/__pycache__/conftest…`, `test_modal_keys…`, `backlog_round_fixture…`) were left in place: they are git-ignored.
