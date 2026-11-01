# Inc C — RED on base `0a8dfaa` (tester, E4)

Evidence state: **executed** (RED capture). Producer: tester (Opus). Not reviewed; no verdict here.

## Run

- Transcript: `evidence/red-base.txt` (one complete run, `taskboard.__file__` header =
  `C:\Users\jjgh8\Github\taskboard-wt\incC-base\taskboard\__init__.py`, HEAD `0a8dfaa`).
- Command (cwd = base tree):
  `env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -p no:cacheprovider tests/test_colour_notes.py tests/test_colour_pens.py tests/test_colour_palette.py tests/test_modal_keys.py::test_TC_2407_every_modal_is_in_the_inventory -rA`
- **Deviation from the brief, declared:** the brief's command names the three new files; I
  added `tests/test_modal_keys.py::test_TC_2407_every_modal_is_in_the_inventory` (the
  inventory row this increment adds, TC-4278) to the SAME command, so its RED is in the same
  single run instead of a second transcript.
- Result: **212 failed, 6 passed, 0 errors** in 63 s (218 collected: notes 52, pens 74,
  palette 91, modal_keys 1).
- Every failure is an assertion: 137 `AssertionError` + 75 `Failed: <name> is missing: Inc C
  is not built here` (the `_need` helper turns an absent new name into `pytest.fail`). 0
  ImportError, 0 collection errors, 0 other exception types (`grep` of the transcript).

## The 6 tests that pass on base — each one by design

| Test | Why it passes on base |
|---|---|
| `test_colour_notes.py::test_TC_4203_inputs_without_colons_tokenise_as_at_base` | GUARD, LLR-4201.3: inputs with no `::` must tokenise exactly as at base. |
| `test_colour_notes.py::test_AT_4204_legacy_notes_render_as_at_base[at4204]` | GUARD, AT-4204: frozen base oracle (captured by me on the base tree). |
| `test_colour_notes.py::test_AT_4204_legacy_notes_render_as_at_base[mixed]` | GUARD, AT-4204 (second legacy note: `10::30`, `a :: b`, `x::y`, a mention, a blank line). |
| `test_colour_pens.py::test_P_M1_7_the_textual_internals_the_ink_rests_on_keep_their_shape` | GUARD, ruling P-M1-7: goes RED when a Textual upgrade reshapes `_build_highlight_map` / `_highlights` / `_line_cache` / `_render_line`. |
| `test_colour_notes.py::test_reference_scanner_reproduces_the_designs_examples` | ORACLE SELF-CHECK, not a product test: the reference scanner agrees with every graph-proto-V example and with the frozen base tokeniser over the 1 112 base inputs. |
| `test_colour_notes.py::test_C4_the_oracle_functions_are_right` | ORACLE SELF-CHECK: the WCAG contrast and HLS saturation functions on known values (21:1; the LLR NCs `#5b6675`, `#8b98a5`). |

Tests that would otherwise pass on base were given a positive control so they fail for a
behavioural reason: TC-4205 (literal `::` must stay literal BESIDE a working span), TC-4213
(the timing test also asserts the scanner finds the spans), TC-4220..4223 (the tones are read
from the painted surface; base paints all six codes `mut`), TC-4246 surrogate (after deleting
the surrogate the field must ink again, LLR-4204.1).

## Oracle feasibility (scratch, not evidence of the product)

With the base tokeniser monkeypatched to the test's reference scanner (scratch plugin outside
the repo), the layer-0 reader tests TC-4210, 4211, 4212, 4214, 4216, 4220, 4221, 4222, 4223,
4225 pass — their expected values are reachable without any change to the readers, as the
design claims. CSS / legend / pens / palette tests need the product and were not exercised
GREEN.

## TC → LLR map (every LLR id appears at least once)

File legend: N = `tests/test_colour_notes.py`, P = `tests/test_colour_pens.py`,
L = `tests/test_colour_palette.py`, K = `tests/test_modal_keys.py`.

| LLR / AT | Test function(s) |
|---|---|
| LLR-4201.1 | N `test_TC_4201_each_code_colours_its_inner_text_in_its_tone` (6), `test_TC_4201_each_code_is_one_span_with_its_code` |
| LLR-4201.2 | N `test_TC_4202_one_space_beside_each_marker_belongs_to_the_marker` (3), `test_TC_4202_the_scanner_gives_str_offsets_of_markers_and_inner` |
| LLR-4201.3 | N `test_TC_4203_inputs_without_colons_tokenise_as_at_base` (guard), `test_TC_4203_a_legacy_span_is_a_span_with_no_code` |
| LLR-4201.4 | N `test_TC_4204_an_open_span_ends_at_the_line_end` |
| LLR-4201.5 | N `test_TC_4205_a_colon_pair_that_opens_nothing_stays_literal` (5) |
| LLR-4201.6 | N `test_TC_4206_the_next_opener_ends_the_open_span_keeping_its_space` |
| LLR-4201.7 | N `test_TC_4207_markers_of_the_other_kind_are_literal_inside_a_span` |
| LLR-4201.8 | N `test_TC_4208_an_empty_span_shows_nothing` |
| LLR-4201.9 | N `test_TC_4209_joined_segments_are_the_text_without_its_markers` (11 110 inputs; + A-5 closed tone set), `test_TC_4228_spans_are_ordered_disjoint_and_match_the_reference`, `test_TC_4228_offsets_are_str_indices_not_bytes` |
| LLR-4201.10 | N `test_TC_4213_the_scanner_is_linear_in_the_line` (3) |
| LLR-4202.1 | N `test_TC_4210_the_board_markup_paints_the_span_in_its_hex` (3) |
| LLR-4202.2 | N `test_TC_4211_details_and_preview_paint_the_span_in_its_hex` |
| LLR-4202.3 | N `test_TC_4212_a_mention_inside_a_span_stays_bold_pink` |
| LLR-4202.4 | N `test_TC_4214_the_presentation_carries_the_tone_on_every_wrapped_row` |
| LLR-4202.5 | N `test_TC_4216_the_html_notes_write_a_tone_class_and_escape_the_text`, `test_TC_4212_…` (html arm), `test_TC_4225_the_reports_plain_notes_drop_the_markers` |
| LLR-4202.6 | N `test_TC_4217_the_deck_defines_the_three_new_tone_classes_in_both_themes` |
| LLR-4202.7 | N `test_TC_4218_the_workspace_defines_the_new_tones_like_hl_soon` |
| LLR-4202.8 | N `test_TC_4219_the_focus_legend_lists_the_six_codes_in_their_tones` |
| LLR-4202.9 | L `test_TC_4276_the_details_label_lists_the_six_codes_in_their_tones` (80x24, 118x30; A-2 form) |
| LLR-4202.10 | P `test_TC_4239_the_label_shows_the_pen_and_every_key_unclipped` (key tones) |
| LLR-4203.1 | P `test_TC_4230_alt_n_opens_a_spaced_pair_with_the_cursor_inside` (pilot + terminal) |
| LLR-4203.2 | P `test_TC_4231_typing_under_a_pen_stays_inside_its_span`, `test_TC_4250_typing_a_double_colon_under_a_pen_closes_its_span`, `test_TC_4250_two_colons_first_thing_in_a_fresh_pen_leave_only_the_old_closer` |
| LLR-4203.3 | P `test_TC_4232_alt_0_moves_past_the_closer`, `test_TC_4258_lifting_a_span_with_no_closer_writes_the_closer` |
| LLR-4203.4 | P `test_TC_4233_alt_0_turns_the_pen_off_and_the_chip_says_so` |
| LLR-4203.5 | P `test_TC_4234_another_pen_closes_the_first_and_opens_after_it` |
| LLR-4203.6 | P `test_TC_4235_lifting_an_empty_pen_removes_its_span` (2) |
| LLR-4203.7 | P `test_TC_4236_enter_under_a_pen_continues_the_pen_on_the_next_line`, `test_TC_4236_enter_mid_span_splits_it_in_two_spans_of_the_same_pen`, `test_TC_4237_enter_with_the_pen_off_is_a_plain_new_line` |
| LLR-4203.8 | P `test_TC_4238_leaving_the_span_turns_the_pen_off` (6: arrows, home, end, selection), `test_TC_4238_a_click_before_the_span_turns_the_pen_off` |
| LLR-4203.9 | P `test_TC_4239_the_label_shows_the_pen_and_every_key_unclipped` (7 states × 2 sizes), `test_TC_4239_every_label_form_fits_the_narrow_column` |
| LLR-4203.10 | P `test_TC_4240_a_pen_key_outside_the_notes_changes_no_field` (terminal events `Key("alt+5","5")`, `Key("alt+0","0")`) |
| LLR-4203.11 | P `test_TC_4241_saving_with_an_empty_pen_saves_no_empty_span` |
| LLR-4203.12 | P `test_TC_4252_a_pen_refuses_where_it_would_change_written_text` (3 arms), `test_TC_4252_at_a_spans_end_the_cursor_is_outside_it` |
| LLR-4203.13 | P `test_TC_4254_a_pen_key_over_a_selection_inserts_nothing` (2) |
| LLR-4203.14 | P `test_TC_4256_leaving_an_empty_pen_span_removes_it` (4), `test_TC_4257_only_the_pens_own_empty_span_is_removed` (SEC-4), `test_TC_4257_leaving_a_span_with_text_keeps_it`, `test_TC_4236_leaving_the_fresh_span_after_enter_removes_it` |
| LLR-4203.15 | P `test_TC_4255_the_same_pen_key_again_changes_nothing` (TC-4248/4255) |
| LLR-4203.16 | P `test_TC_4249_esc_digit_parses_as_alt_digit_after_the_import`, `test_TC_4249_the_unshadowing_is_idempotent_and_spares_foreign_values` (A-1), `test_TC_4249_a_read_only_table_never_stops_the_app_starting` (A-1 immutable arm) |
| LLR-4203.17 | P `test_TC_4252_a_pen_refuses_where_it_would_change_written_text` (3 N4 arms) |
| LLR-4204.1 | P `test_TC_4242_the_field_paints_the_inner_text_in_its_tone` (colour + legacy), `test_TC_4246_a_lone_surrogate_opens_and_types_without_ink` (recovery arm), `test_AT_4201_…` |
| LLR-4204.2 | P `test_TC_4243_the_markers_are_painted_dim` |
| LLR-4204.3 | P `test_TC_4244_a_typed_character_is_inked_before_the_next_paint` |
| LLR-4204.4 | P `test_TC_4245_the_ink_colours_exactly_the_tokenisers_ranges` (7 380 inputs vs the reference scanner), `test_TC_4245_rows_without_a_span_have_no_ink_and_an_open_span_no_closer_range` |
| LLR-4204.5 | P `test_TC_4246_ink_offsets_are_utf8_bytes_even_for_a_lone_surrogate`, `test_TC_4246_non_ascii_text_is_inked_on_exactly_its_cells` |
| LLR-4204.6 | P `test_TC_4247_the_ink_never_touches_another_text_area` |
| LLR-4204.7 | P `test_TC_4246_the_ink_is_built_in_linear_time` (2) |
| LLR-4204.8 | P `test_TC_4251_an_ink_that_raises_leaves_the_editor_working` |
| LLR-4204.9 | P `test_TC_4246_a_lone_surrogate_opens_and_types_without_ink`, `test_TC_4246_ink_offsets_are_utf8_bytes_even_for_a_lone_surrogate` |
| LLR-4205.1 | L `test_TC_4260_alt_c_over_a_selection_opens_the_palette`, `test_TC_4261_the_target_is_…` (pure) |
| LLR-4205.2 | L `test_TC_4261_alt_c_on_a_word_colours_that_word` (2), `test_TC_4261_the_target_is_…` (pure) |
| LLR-4205.3 | L `test_TC_4262_the_palette_lists_six_pens_none_and_cancel` |
| LLR-4205.4 | L `test_TC_4263_recolour_rewrites_the_target_or_its_span` (rows 1–6), `test_TC_4260_…`, `test_TC_4261_alt_c_on_a_word_…`, `test_AT_4202_…` |
| LLR-4205.5 | L `test_TC_4263_…` (rows 7–17), `test_TC_4264_a_digit_inside_a_span_swaps_its_markers` (2) |
| LLR-4205.6 | L `test_TC_4263_…` (rows 18–21), `test_TC_4266_zero_inside_a_span_uncolours_it` (2), `test_TC_4286_uncolouring_a_span_with_colons_inside_is_allowed` |
| LLR-4205.7 | L `test_TC_4263_…` (row 22), `test_TC_4267_zero_on_plain_text_changes_nothing` |
| LLR-4205.8 | L `test_TC_4268_esc_closes_the_palette_and_changes_nothing`, `test_TC_4268_esc_compares_with_the_notes_at_palette_open` (P-M2-4) |
| LLR-4205.9 | L `test_TC_4269_recolour_changes_nothing_outside_the_rewritten_range` (12 cases) |
| LLR-4205.10 | L `test_TC_4270_alt_c_refuses_with_one_notice_and_no_palette` (N1), `test_TC_4261_the_target_is_…` (pure) |
| LLR-4205.11 | L `test_TC_4270_…` (N2 ×2), `test_TC_4261_the_target_is_…` (pure) |
| LLR-4205.12 | L `test_TC_4270_…` (N3 ×3), `test_TC_4261_the_target_is_…` (pure) |
| LLR-4205.13 | L `test_TC_4273_the_box_sits_next_to_the_target_and_on_screen` (pure, 4), `test_TC_4273_the_palette_box_is_on_screen_next_to_the_target` (4/4 pilot) |
| LLR-4205.14 | L `test_TC_4274_alt_c_under_a_pen_targets_the_pens_span` (2), `test_TC_4274_alt_c_on_an_empty_pen_removes_it_and_says_nothing_to_colour` (2) |
| LLR-4205.15 | L `test_TC_4285_a_rewrite_that_changes_the_visible_text_is_refused` (3), `test_TC_4287_every_allowed_rewrite_keeps_the_visible_text` |
| LLR-4205.16 | L `test_TC_4284_alt_c_outside_the_notes_changes_no_field` (terminal `ESC c`) |
| LLR-4206.1 | N `test_TC_4220_every_tone_is_saturated` |
| LLR-4206.2 | N `test_TC_4221_every_tone_reads_on_both_terminal_backgrounds` |
| LLR-4206.3 | N `test_TC_4222_the_256_colour_downgrade_keeps_six_distinct_non_greys` |
| LLR-4206.4 | N `test_TC_4223_no_tone_is_the_accent` |
| LLR-4206.5 | N `test_TC_4224_the_decks_tone_variables_read_on_their_themes_background` |
| AT-4201 | P `test_AT_4201_a_pen_written_note_is_saved_and_shown_blue` (terminal bytes → parser → editor → file → details) |
| AT-4202 | L `test_AT_4202_select_a_word_colour_it_yellow_and_save` (terminal bytes → palette → file) |
| AT-4203 | N `test_AT_4203_the_exported_workspace_and_deck_hold_the_colours` (`extract` + `write_reports`) |
| AT-4204 | N `test_AT_4204_legacy_notes_render_as_at_base` (2, guard) |
| Addenda | A-1 → TC-4249 ×2; A-2 → TC-4276; A-4 (SEC-5) → L `test_TC_4288_a_line_changed_under_the_palette_is_left_alone` (2); A-5 → TC-4209; TC-4226 PEN_CODES; TC-4227 / TC-4229 rulings P-V-4, ARCH-11; TC-4275, TC-4283 (P-M2-8) |
| TC-4278 | K `INVENTORY` gains `"ColourPalette": {}` (RED on base: the row names a modal the package lacks) |

LLRs without a test: **none** (67/67 named above). TC ids with no test of their own:
TC-4215 (free), TC-4253 (`_pen_span` at the closer end — covered by behaviour in TC-4237),
TC-4259 (inside TC-4235), TC-4277 / TC-4279 (removed by rulings P-M2-6 / P-M2-2), TC-4289
(unused).

## Gaps and limits (written, not implied)

- Not covered: the TC-4237 race example (`_pen_span()` None before any SelectionChanged is
  handled) — the pilot waits for idle between keys, so the race is not reproducible
  deterministically; the TC-4258 "span ended by the next opener" lift and the TC-4251
  "deleted `_line_cache`" arm (as written it cannot hold: Textual's own
  `_build_highlight_map` and `render_line` also read `_line_cache`); P-M1-2 (enter under a pen
  while an empty-directory `@` picker is open).
- Not run here: the full suite and the HLR-4206 guards (`test_colour_budget*.py`,
  `test_palette_ration.py` with 0 edits) — the orchestrator's single gate run (C-25); GREEN
  against the build; the real Windows Terminal check (ARCH-14, E5).
- The tests bind to the design's names (graph-interfaces / M1 / M2): `views.colour_spans`,
  `views.PEN_CODES`, Span fields `start/inner_start/inner_end/end/tone/code`;
  `modals.colour_spans` (the name the ink reads), `ink_highlights`, `pen_label`,
  `_unshadow_alt_digits`, `recolour`, `colour_target`, `palette_offset`; `TaskModal.pen`; the
  palette class name `ColourPalette` and its `#cp-box`; the Notes label = the first `.task-sec`
  in `#task-edit`. A build that renames one fails with `… is missing`, not silently.
- Timing tests (TC-4213, TC-4246 linear) use wall-clock medians of 3 with the design's
  thresholds (250 ms, ratio 20); a heavily loaded machine can make them flaky.
- Tests read Textual privates already read by the suite (`_compositor`, `_driver`,
  `_notifications`, `_theme`, `_highlights`), each in one helper.
- The base tree `incC-base` now holds copies of the three new files and the edited
  `tests/test_modal_keys.py` (uncommitted scratch, as the brief allows).
- Fixtures: synthetic only (`Ana Ruiz` is the suite's existing synthetic person; no real
  names, credentials or client data).
