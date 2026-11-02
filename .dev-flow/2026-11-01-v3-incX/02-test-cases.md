# Test cases — Inc X: presentation HTML deck export

Base `8506cb7`; design head `a732c34`. One case covers each active HLR and LLR. Parameterized tests cover all their collected arms. Every node below was checked with `env -u NO_COLOR python -m pytest --collect-only -q` (173 cases in the two new files, plus the three named legacy nodes).

Node prefixes:
- `E` = `tests/test_present_html_export.py`
- `A` = `tests/test_present_html_at.py`
- `R` = `tests/test_report_export_app.py`
- `D` = `tests/test_readme.py`
- `K` = `tests/test_keymap.py`

## HLR-4501 — write the deck of what the presentation shows

### HLR-4501/1
- **Objective:** Verify that `x` in the presentation writes the deck of the presentation's scope into the presented board's `reports/` folder.
- **Class:** normal.
- **Preconditions:** None stated (`When` event).
- **Inputs:** Press `x` in the presentation, including the project, all-projects and narrow-terminal alternatives.
- **Expected result:** The scoped deck is written in the presented board's `reports/` folder; all LLR-4501.n thresholds pass.
- **Tests:** `A::test_AT_4501_views_1_and_2_write_only_the_presented_scope` (partial); `A::test_AT_4502_view_3_exports_order_scope_and_folded_tasks` (partial); `A::test_AT_4505_narrow_export_warns_and_creates_no_folder` (partial).

### LLR-4501.1/1 — TC-4701
- **Objective:** Verify that project views write the exact project-scoped HTML filename.
- **Class:** normal.
- **Preconditions:** None stated (`When` event).
- **Inputs:** In view 1 and view 2 at width at least 36 columns, press `x`; also use project names `..\..\evil`, `CON` and `!!!` for the naming controls.
- **Expected result:** `<board dir>/reports/present-<project slug>-<date>.html` exists with the exact name in both views (2/2); the slug is `report_html.slug` of the presented project's name, or `project` when empty.
- **Tests:** `E::test_TC_4701_LLR_4501_1_project_views_write_exact_html_name` (full); `E::test_TC_4701b_LLR_4501_1_names_cannot_escape_reports` (full).

### LLR-4501.2/1 — TC-4702
- **Objective:** Verify that view 3 writes the exact date-scoped HTML filename.
- **Class:** normal.
- **Preconditions:** None stated (`When` event).
- **Inputs:** In view 3 at width at least 36 columns, press `x`.
- **Expected result:** `<board dir>/reports/present-<date>.html` exists with the exact name (1/1).
- **Tests:** `E::test_TC_4702_LLR_4501_2_all_view_writes_exact_html_name` (full).

### LLR-4501.3/1 — TC-4703
- **Objective:** Verify that an unfiltered project-view export is byte-identical to the independent `H c p` deck.
- **Class:** normal.
- **Preconditions:** The presented board is registered; no task of the presented project is hidden, archived or a milestone of a hidden class; the independent `H` fixture already has every held task's `urls` cleared.
- **Inputs:** On the two-project fixture with a done task, classified milestone, dependency, mention and task URL, press `x` in views 1 and 2; independently press `H`, `p`, `c` for the same project and day.
- **Expected result:** For each view, `x` bytes == `H c p` bytes over the equivalent URL-cleared proxy board (2/2).
- **Tests:** `E::test_TC_4703_LLR_4501_3_bytes_equal_independent_url_free_H_fixture` (full).

### LLR-4501.4/1 — TC-4704
- **Objective:** Verify that an unfiltered view-3 export is byte-identical to the independent `H c o` deck.
- **Class:** normal.
- **Preconditions:** The registry lists only the presented board; none of its projects or tasks is hidden, archived, ranked out of board order, without a project or a milestone of a hidden class; the independent `H` fixture already has every held task's `urls` cleared.
- **Inputs:** Press `x` in view 3; independently press `H`, `c` with scope `o` on the same day.
- **Expected result:** `x` bytes == `H c o` bytes over the equivalent URL-cleared proxy board (1/1).
- **Tests:** `E::test_TC_4704_LLR_4501_4_all_bytes_equal_independent_url_free_H_fixture` (full).

### LLR-4501.5/1 — TC-4705
- **Objective:** Verify that project views export only the presented project regardless of its own rail flag.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export view 1 or 2 from a three-project board, with the presented project's `show_in_present` first true and then false.
- **Expected result:** Exactly one project slide, named for the presented project; each of the other two project names has 0 occurrences, for both flag values (2/2).
- **Tests:** `E::test_TC_4705_LLR_4501_5_project_scope_ignores_own_rail_flag` (full).

### LLR-4501.6/1 — TC-4706
- **Objective:** Verify that view 3 exports shown projects in presentation order.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export view 3 with projects A, B, C ranked C=0, A=1, B=2.
- **Expected result:** Overview rows read C, A, B and project slides read C, A, B (2/2).
- **Tests:** `E::test_TC_4706_LLR_4501_6_all_scope_uses_presentation_order` (full).

### LLR-4501.7/1 — TC-4707
- **Objective:** Verify that the deck contains only the presented board.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** With two boards in the registry, press `x` in views 1 and 3.
- **Expected result:** The cover's board table has one row; the other board's name and its projects' names each have 0 occurrences in both views (2/2).
- **Tests:** `E::test_TC_4707_LLR_4501_7_only_presented_board_reaches_deck` (full).

### LLR-4501.8/1 — TC-4708
- **Objective:** Verify that folding a view-3 project does not remove its shown tasks from the deck.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** In view 3, fold project B with `enter`, then press `x`.
- **Expected result:** B's slide lists both shown tasks (1/1).
- **Tests:** `E::test_TC_4708_LLR_4501_8_folded_project_keeps_tasks_and_notes` (full); `A::test_AT_4502_view_3_exports_order_scope_and_folded_tasks` (partial).

### LLR-4501.9/1 — TC-4709
- **Objective:** Verify that every shown task, open and done, reaches each exported project.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export views 1 and 3 with a project holding two open and one done shown task.
- **Expected result:** The project slide reads `3 tasks` and contains the done title in both views (2/2).
- **Tests:** `E::test_TC_4709_LLR_4501_9_done_task_title_and_notes_reach_file` (full); `A::test_AT_4502_view_3_exports_order_scope_and_folded_tasks` (partial).

### LLR-4501.10/1 — TC-4710
- **Objective:** Verify that export does not modify the board file or its history.
- **Class:** normal.
- **Preconditions:** None stated (`When` event).
- **Inputs:** Hash the board file and `history.jsonl`, press `x` in views 1, 2 and 3, then hash both again; spy on board save routes.
- **Expected result:** Before/after sha256 values are equal for both files in all three views (6/6).
- **Tests:** `E::test_TC_4710_LLR_4501_10_export_changes_neither_board_nor_history` (full); `A::test_AT_4501_views_1_and_2_write_only_the_presented_scope` (partial).

### LLR-4501.11/1 — TC-4711
- **Objective:** Verify that an unlisted presented board uses its label or the exact fallback name.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** Open an unregistered board with `--open`; export view 1 first with label `("Client A", "pink")`, then with no label.
- **Expected result:** The cover's board cell is respectively `Client A` and `this board`; both filenames are `present-<project slug>-<date>.html` (2/2).
- **Tests:** `E::test_TC_4711_LLR_4501_11_unlisted_board_uses_label_or_fallback` (full).

### LLR-4501.12/1 — TC-4712
- **Objective:** Verify that an empty view-3 scope still writes the required empty deck.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** Hide every project on the view-3 rail, then press `x`.
- **Expected result:** The file exists and its overview slide reads exactly `No project in this scope holds a task.`; 0 exceptions (2/2).
- **Tests:** `E::test_TC_4712_LLR_4501_12_empty_all_scope_still_writes_deck` (full).

### LLR-4501.13/1 — TC-4713
- **Objective:** Verify that narrow export shows the exact warning.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** At 30 columns, press `x` in the presentation.
- **Expected result:** A warning toast titled `Present` reads exactly `Widen the terminal to 36+ columns to export` (1/1).
- **Tests:** `E::test_TC_4713_LLR_4501_13_narrow_warning_is_unchanged` (full); `A::test_AT_4505_narrow_export_warns_and_creates_no_folder` (partial).

### LLR-4501.14/1 — TC-4714
- **Objective:** Verify that narrow export writes no file.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** At 30 columns, press `x` in the presentation.
- **Expected result:** `reports/` is absent after the key press (1/1).
- **Tests:** `E::test_TC_4714_LLR_4501_14_narrow_export_writes_nothing` (full); `A::test_AT_4505_narrow_export_warns_and_creates_no_folder` (partial).

### LLR-4501.15/1 — TC-4715
- **Objective:** Verify that a missing presented project falls back to the first visible frame project without an exception.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** Set presented project id to `missing` with visible projects Alpha then Beta, then press `x`; include the no-visible-project control.
- **Expected result:** The deck holds Alpha, not Beta, and raises 0 exceptions (1/1).
- **Tests:** `E::test_TC_4715_LLR_4501_15_missing_project_falls_back_to_first_visible` (full).

## HLR-4502 — hidden presentation data stays out of the bytes

### HLR-4502/1
- **Objective:** Verify that every project and task the presentation does not draw is absent from the deck's bytes.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export decks containing the hidden-task, hidden-project and other hidden-scope alternatives.
- **Expected result:** 0 occurrences of every sentinel over LLR-4502.1..4502.7.
- **Tests:** `A::test_AT_4501_views_1_and_2_write_only_the_presented_scope` (partial); `A::test_AT_4502_view_3_exports_order_scope_and_folded_tasks` (partial).

### LLR-4502.1/1 — TC-4721
- **Objective:** Verify that tasks hidden from the presentation leave neither title nor id in the deck.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export views 1, 2 and 3 with hidden task title `HIDDEN-T-7Q` and id `hidt7q`.
- **Expected result:** Each string has 0 occurrences in the file's bytes in every view (3/3).
- **Tests:** `E::test_TC_4721_LLR_4502_1_hidden_task_and_id_have_zero_occurrences` (full); `A::test_AT_4501_views_1_and_2_write_only_the_presented_scope` (partial).

### LLR-4502.2/1 — TC-4722
- **Objective:** Verify that view 3 excludes a hidden project and all its tasks.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export view 3 with hidden project `HIDDEN-P-4K` containing shown task `UNDER-HIDDEN-P`.
- **Expected result:** Both strings have 0 occurrences (2/2).
- **Tests:** `E::test_TC_4722_LLR_4502_2_hidden_project_and_its_tasks_have_zero_occurrences` (full); `A::test_AT_4502_view_3_exports_order_scope_and_folded_tasks` (partial).

### LLR-4502.3/1 — TC-4723
- **Objective:** Verify that archived and projectless work is absent from the deck.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export views 1 and 3 with sentinels `ARCH-T`, `ARCH-P-TASK` and `NO-PROJ-T` on an archived task, a task of an archived project and a task without a project.
- **Expected result:** Each sentinel has 0 occurrences and there is no `Inbox` slide in each view (2/2).
- **Tests:** `E::test_TC_4723_LLR_4502_3_archived_and_projectless_tasks_are_excluded` (full).

### LLR-4502.4/1 — TC-4724
- **Objective:** Verify that milestones of hidden classes are absent from the deck.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export views 1 and 3 with milestone `HID-CLASS-MS` whose class is hidden in `#`.
- **Expected result:** `HID-CLASS-MS` has 0 occurrences in each view (2/2).
- **Tests:** `E::test_TC_4724_LLR_4502_4_hidden_milestone_class_is_excluded` (full).

### LLR-4502.5/1 — TC-4725
- **Objective:** Verify that the legend contains only milestone classes used by exported tasks.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export a deck where class `CLASS-ONLY-HIDDEN` is used only by a hidden task.
- **Expected result:** `CLASS-ONLY-HIDDEN` has 0 occurrences (1/1).
- **Tests:** `E::test_TC_4725_LLR_4502_5_legend_omits_class_used_only_by_hidden_task` (full).

### LLR-4502.6/1 — TC-4726
- **Objective:** Verify that each export reads the current presentation hide flags.
- **Class:** normal.
- **Preconditions:** None stated (`When` event).
- **Inputs:** In view 1 press `space` on a task then `x`; subsequently press `a` then `x`.
- **Expected result:** The task title has 0 occurrences after the first export and is present after the second (2/2).
- **Tests:** `E::test_TC_4726_LLR_4502_6_export_reads_hide_flags_at_each_press` (full); `A::test_AT_4501_views_1_and_2_write_only_the_presented_scope` (partial).

### LLR-4502.7/1 — TC-4727
- **Objective:** Verify that task URLs in scope never reach the deck's bytes.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** Export views 1, 2 and 3 with shown task a1 holding `https://example.test/capability-a1`.
- **Expected result:** That URL has 0 occurrences in each view (3/3).
- **Tests:** `E::test_TC_4727_LLR_4502_7_urls_strip_without_mutating_source_or_next_save` (full).

## HLR-4503 — toast and ten-second open offer

### HLR-4503/1
- **Objective:** Verify that a deck written from the presentation is named in a toast and can be opened with `o` for 10 seconds.
- **Class:** normal.
- **Preconditions:** None stated (`When` event).
- **Inputs:** Write a deck, exercise the live, consumed, expired and failed-write offer alternatives.
- **Expected result:** The toast names the file; the offer opens it only while live for 10 s; all LLR-4503.n thresholds pass.
- **Tests:** `A::test_AT_4503_the_open_offer_is_single_use_and_expires` (partial); `A::test_AT_4504_an_oserror_toasts_offers_nothing_and_leaves_r_usable` (partial).

### LLR-4503.1/1 — TC-4731
- **Objective:** Verify that successful export shows the exact information toast for exactly 10 seconds.
- **Class:** normal.
- **Preconditions:** None stated (`When` event).
- **Inputs:** Press `x` and successfully write the deck.
- **Expected result:** Title `Report`, severity information, timeout 10 s, and exact text `Report written: <file name>\n<folder>\no opens it (10 s)` (1/1).
- **Tests:** `E::test_TC_4731_LLR_4503_1_success_toast_is_exact` (full); `A::test_AT_4503_the_open_offer_is_single_use_and_expires` (partial).

### LLR-4503.2/1 — TC-4732
- **Objective:** Verify that `o` opens a live offered file through the operating system's default handler.
- **Class:** normal.
- **Preconditions:** None stated (`When` event).
- **Inputs:** After `x` creates a live offer, press `o` with `os.startfile` (or `webbrowser.open` off Windows) monkeypatched.
- **Expected result:** The handler is called once with the deck's path (1/1).
- **Tests:** `E::test_TC_4732_LLR_4503_2_o_opens_offered_deck_once` (full); `A::test_AT_4503_the_open_offer_is_single_use_and_expires` (partial).

### LLR-4503.3/1 — TC-4733
- **Objective:** Verify that absent, expired and consumed offers open nothing.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** Press `o` without `x`; press `x`, advance the clock 10 s and press `o`; press `x`, `o`, `o`; also consume the shared offer after `escape`.
- **Expected result:** Respectively 0 calls, 0 calls and exactly 1 call in total; 0 exceptions (3/3).
- **Tests:** `E::test_TC_4733_LLR_4503_3_absent_expired_and_consumed_offers_open_nothing` (full); `E::test_TC_4733b_LLR_4503_3_shared_offer_survives_esc_for_one_main_o` (full); `A::test_AT_4503_the_open_offer_is_single_use_and_expires` (partial).

### LLR-4503.4/1 — TC-4734
- **Objective:** Verify that a write `OSError` produces the exact error toast without crashing.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** Make `reports` an existing plain file so `mkdir` raises `OSError`, then press `x`.
- **Expected result:** An error toast titled `Report` reads exactly `Report not (fully) written: <error>`; 0 exceptions (1/1).
- **Tests:** `E::test_TC_4734_LLR_4503_4_write_oserror_toasts_without_crashing` (full); `A::test_AT_4504_an_oserror_toasts_offers_nothing_and_leaves_r_usable` (partial).

### LLR-4503.5/1 — TC-4735
- **Objective:** Verify that a failed write withdraws any earlier live offer.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** Create a live offer with `x`, make the next `x` fail with `OSError`, then press `o`.
- **Expected result:** The OS handler receives 0 calls (1/1).
- **Tests:** `E::test_TC_4735_LLR_4503_5_failed_export_withdraws_earlier_offer` (full); `A::test_AT_4504_an_oserror_toasts_offers_nothing_and_leaves_r_usable` (partial).

### LLR-4503.6/1 — TC-4736
- **Objective:** Verify that an OS-handler failure produces the exact open-error toast.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** Make `os.startfile` raise `OSError`, then press `o` on a live offer; include the relative-URI `ValueError` control.
- **Expected result:** The toast reads exactly `Could not open the report <file name>.` (1/1).
- **Tests:** `E::test_TC_4736_LLR_4503_6_opener_oserror_has_exact_error_toast` (full); `E::test_TC_4736b_LLR_4503_6_relative_uri_valueerror_is_caught` (full).

### LLR-4503.7/1 — TC-4737
- **Objective:** Verify that Rich markup in a filename or folder is shown literally in the toast.
- **Class:** robustness.
- **Preconditions:** None stated (`If` unwanted condition).
- **Inputs:** Export from a board folder containing Rich markup; use the single-path-segment fixture `[red]rx[red]` recorded in E4 integration because the E1 literal `[red]rx[/red]` contains a path separator.
- **Expected result:** The toast's plain text contains the folder markup literally, including `[red]rx[red]` for the executable fixture (1/1).
- **Tests:** `E::test_TC_4737_LLR_4503_7_markup_in_folder_is_literal_toast_text` (full).

## HLR-4504 — no SVG/PNG presentation export

### HLR-4504/1
- **Objective:** Verify that the presentation exports in no format but the HTML deck.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Export the presentation in all supported views and inspect the resulting files.
- **Expected result:** Only the HTML deck is exported; all LLR-4504.n thresholds pass.
- **Tests:** `A::test_AT_4501_views_1_and_2_write_only_the_presented_scope` (partial); `A::test_AT_4502_view_3_exports_order_scope_and_folded_tasks` (partial); `E::test_TC_4742_LLR_4504_2_export_starts_no_subprocess` (partial); `E::test_TC_4743_LLR_4504_3_package_has_no_svg_or_rasteriser_route` (partial).

### LLR-4504.1/1 — TC-4741
- **Objective:** Verify that every presentation export writes exactly one new or changed file, an HTML deck.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Hash the board directory before and after `x` in views 1, 2 and 3.
- **Expected result:** `reports/` holds that scope's `present-*.html`, 0 `.svg`, 0 `.png`, and no other file is new or changed in each view (3/3).
- **Tests:** `E::test_TC_4741_LLR_4504_1_one_file_oracle` (full); `A::test_AT_4501_views_1_and_2_write_only_the_presented_scope` (partial); `A::test_AT_4502_view_3_exports_order_scope_and_folded_tasks` (partial).

### LLR-4504.2/1 — TC-4742
- **Objective:** Verify that presentation export starts no external process.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Monkeypatch `subprocess.run` and `subprocess.Popen` to raise, then press `x` in views 1, 2 and 3.
- **Expected result:** The deck is written and the process spies record 0 calls in every view (3/3).
- **Tests:** `E::test_TC_4742_LLR_4504_2_export_starts_no_subprocess` (full).

### LLR-4504.3/1 — TC-4743
- **Objective:** Verify that the package contains no presentation SVG writer or rasteriser route.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Inspect `taskboard/*.py` with `save_svg|msedge|--screenshot|present_paths|present_all_export`.
- **Expected result:** 0 hits (1/1).
- **Tests:** `E::test_TC_4743_LLR_4504_3_package_has_no_svg_or_rasteriser_route` (full).

## HLR-4505 — discoverable `H`

### HLR-4505/1
- **Objective:** Verify that `H` appears in the main primary key bar and is listed in `?` help.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Inspect the main primary bar and open `?` help at 80 and 118 columns across the main views.
- **Expected result:** `H` is on the primary bar and listed in help; all LLR-4505.n thresholds pass at 80 and 118 columns.
- **Tests:** `A::test_AT_4506_h_is_discoverable_and_presentation_help_says_html` (partial); `E::test_TC_4751_LLR_4505_1_H_is_in_all_20_primary_bars` (partial); `E::test_TC_4755_LLR_4505_5_help_lists_H_Report_exactly_once` (partial).

### LLR-4505.1/1 — TC-4751
- **Objective:** Verify that the primary bar draws `H` in every main view at both required widths.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Fit the primary bar for `swimlanes agenda gantt kanban focus chainmap flow standup people setup` at 80 and 118 columns.
- **Expected result:** `H` is among the drawn keys in all 10 views × 2 widths (20/20).
- **Tests:** `E::test_TC_4751_LLR_4505_1_H_is_in_all_20_primary_bars` (full); `R::test_TC_3117_H_is_seated_once_on_the_bar` (partial); `A::test_AT_4506_h_is_discoverable_and_presentation_help_says_html` (partial).

### LLR-4505.2/1 — TC-4752
- **Objective:** Verify that adding `H` loses no base key and changes no overflow count.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Compare new and base primary bars in every main view at 80 and 118 columns.
- **Expected result:** Base key set ⊆ new key set and `dropped` values are equal in all 20 cases (20/20).
- **Tests:** `E::test_TC_4752_LLR_4505_2_base_keys_and_overflow_are_preserved` (full).

### LLR-4505.3/1 — TC-4753
- **Objective:** Verify that adding `H` costs at most one drawn base word per bar.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Compare base and new primary-bar words in every main view at 80 and 118 columns.
- **Expected result:** At most one base word is lost in each of the 20 cases (20/20).
- **Tests:** `E::test_TC_4753_LLR_4505_3_at_most_one_base_word_is_lost` (full).

### LLR-4505.4/1 — TC-4754
- **Objective:** Verify that a sufficiently wide primary bar names the key and its word.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Render the primary bar at width 250 in view `swimlanes`.
- **Expected result:** The plain bar contains `H Report` (1/1).
- **Tests:** `E::test_TC_4754_LLR_4505_4_wide_primary_bar_names_H_Report` (full); `R::test_TC_3117_H_is_seated_once_on_the_bar` (partial).

### LLR-4505.5/1 — TC-4755
- **Objective:** Verify that `?` help lists `H Report` exactly once in every main view.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Read the Keys band and global line for each of the 10 main views.
- **Expected result:** Exactly one `H Report` entry across the two locations in each view (10/10).
- **Tests:** `E::test_TC_4755_LLR_4505_5_help_lists_H_Report_exactly_once` (full); `R::test_TC_3117_H_is_seated_once_on_the_bar` (partial); `A::test_AT_4506_h_is_discoverable_and_presentation_help_says_html` (partial).

## HLR-4506 — HTML wording and unchanged remainder of `R`

### HLR-4506/1
- **Objective:** Verify that every presentation-export description names the HTML deck.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Inspect the presentation's `?` wording and the README export description.
- **Expected result:** The export is described as the HTML deck wherever named; all LLR-4506.n thresholds pass.
- **Tests:** `A::test_AT_4506_h_is_discoverable_and_presentation_help_says_html` (partial); `E::test_TC_4765_LLR_4506_5_readme_names_html_deck_not_svg_or_png` (partial).

### LLR-4506.1/1 — TC-4761
- **Objective:** Verify that presentation help names `x` with the exact HTML-deck wording and no legacy formats.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Open the presentation's `?` window and read its text.
- **Expected result:** The window contains row `x export this view · HTML deck`; `SVG` and `PNG` each have 0 occurrences (2/2).
- **Tests:** `E::test_TC_4761_LLR_4506_1_present_help_names_only_HTML_deck` (full); `A::test_AT_4506_h_is_discoverable_and_presentation_help_says_html` (partial).

### LLR-4506.2/1 — TC-4762
- **Objective:** Verify that presentation help names `o` with the exact offer wording.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Open the presentation's `?` window and read its text.
- **Expected result:** The window contains row `o open the last export (10 s)` (1/1).
- **Tests:** `E::test_TC_4762_LLR_4506_2_present_help_names_o_offer` (full); `A::test_AT_4506_h_is_discoverable_and_presentation_help_says_html` (partial).

### LLR-4506.3/1 — TC-4763
- **Objective:** Verify that the presentation adds exactly `o` to its base bindings.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Read the `PresentScreen` binding-key set.
- **Expected result:** The set is exactly `1 2 3 tab shift+tab up,k down,j left,h right,l pageup pagedown space a u shift+up,K shift+down,J enter x escape,q question_mark` ∪ `{o}` (1/1).
- **Tests:** `E::test_TC_4763_LLR_4506_3_present_bindings_are_base_plus_only_o` (full).

### LLR-4506.4/1 — TC-4764
- **Objective:** Verify that every presentation hint row remains exactly equal to base.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Render views 1, 2, 3 at widths 130, 118, 100, 80, 60 and 36, with hidden count 0 and 2.
- **Expected result:** Plain hint text equals base in all 3 × 6 × 2 cases (36/36).
- **Tests:** `E::test_TC_4764_LLR_4506_4_hint_text_is_byte_stable_with_base` (full).

### LLR-4506.5/1 — TC-4765
- **Objective:** Verify that the README describes only HTML-deck presentation export and retains the key-table contract.
- **Class:** normal.
- **Preconditions:** None stated (ubiquitous).
- **Inputs:** Inspect `README.md` excluding `<img` lines and run the README keybinding-table seat comparison.
- **Expected result:** 0 matches of `SVG|PNG`; the `R` key-table row contains `HTML deck`; `tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat` is GREEN (3/3).
- **Tests:** `E::test_TC_4765_LLR_4506_5_readme_names_html_deck_not_svg_or_png` (partial); `K::test_the_readme_keybinding_table_matches_the_seat` (partial); `D::test_TC_2607_readme_documents_the_classes_end_to_end` (partial).

## Acceptance tests — black-box keys and dialogs

### AT-4501
- **Objective:** Verify the project-view export scenario end to end through the shipped application.
- **Class:** normal.
- **Preconditions:** A registry has two boards; the open board has two projects and a presented-project task titled `HIDDEN-T-7Q`.
- **Inputs:** Press `R`, `space` on that task, `x`; then `2`, `x`.
- **Expected result:** Toast names `present-<project slug>-<date>.html`; that file exists and is rewritten; `HIDDEN-T-7Q`, the other project name and other board name each occur 0 times; no `.svg`/`.png`; board-file sha256 is unchanged.
- **Tests:** `A::test_AT_4501_views_1_and_2_write_only_the_presented_scope` (full).

### AT-4502
- **Objective:** Verify view-3 ordering, hiding and folded-task export end to end.
- **Class:** normal.
- **Preconditions:** Projects A, B, C are available in the presentation.
- **Inputs:** Press `R`, `3`; rank C first with `K`; hide B with `space`; fold A with `enter`; press `x`.
- **Expected result:** `present-<date>.html` is written; overview and slides read C, A; B's name occurs 0 times; A's slide lists all its shown tasks.
- **Tests:** `A::test_AT_4502_view_3_exports_order_scope_and_folded_tasks` (full).

### AT-4503
- **Objective:** Verify the open offer end to end, including single use and expiry.
- **Class:** normal.
- **Preconditions:** The OS handler is monkeypatched and the report clock is controllable.
- **Inputs:** Press `R`, `x`, `o`, `o`; then `x`, advance the clock 10 s and press `o`.
- **Expected result:** The handler receives the deck path exactly once; the immediate second `o` and expired `o` add no call.
- **Tests:** `A::test_AT_4503_the_open_offer_is_single_use_and_expires` (full).

### AT-4504
- **Objective:** Verify write-failure handling end to end without losing use of the presentation.
- **Class:** robustness.
- **Preconditions:** `reports` exists as a plain file and the OS handler is monkeypatched.
- **Inputs:** Press `R`, `x`, `o`, then `esc`.
- **Expected result:** Toast begins `Report not (fully) written: ` with a nonempty error; `o` makes 0 calls; `esc` still leaves the presentation.
- **Tests:** `A::test_AT_4504_an_oserror_toasts_offers_nothing_and_leaves_r_usable` (full).

### AT-4505
- **Objective:** Verify narrow-terminal export behavior end to end.
- **Class:** robustness.
- **Preconditions:** Terminal width is 30 columns.
- **Inputs:** Press `R`, `x`.
- **Expected result:** Toast reads exactly `Widen the terminal to 36+ columns to export`; no `reports/` folder exists.
- **Tests:** `A::test_AT_4505_narrow_export_warns_and_creates_no_folder` (full).

### AT-4506
- **Objective:** Verify `H` discoverability, its unchanged modal route and the presentation's HTML wording end to end.
- **Class:** normal.
- **Preconditions:** Main screen available at 118x30 and 80x24.
- **Inputs:** At both sizes inspect the bar, press `?`, then `esc`, `H`; close the modal, press `R`, `?`.
- **Expected result:** Main bar shows `H`; help lists `H Report` exactly once; `H` opens the report modal; presentation help lists `x export this view · HTML deck` and `o open the last export (10 s)`.
- **Tests:** `A::test_AT_4506_h_is_discoverable_and_presentation_help_says_html` (full).
