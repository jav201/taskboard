# Batch-end corrective pass — feat/capture-list-colour

The batch-end full suite on `3c7e18c` (`suite-chunk00..02.txt`) failed 4 project-wide
law tests. The per-increment change-only validation never ran them. This pass fixes all
four with targeted edits, in one commit (`ac1f3f3`).

- **RED:** `corrective-red.txt` (the 4 laws on `3c7e18c`: 4 failed).
- **GREEN, scoped:** `corrective-green.txt` (the law modules plus the batch's 11 new or
  changed test files: 758 passed).
- **GREEN, full:** `suite2-chunk00..02.txt` (same split as `chunk00..02`, run on `ac1f3f3`):
  - chunk00: 1897 passed, 1 skipped (TC-1902, `test_win_clipboard_roundtrip`: Set-Clipboard refused by the machine).
  - chunk01: 1192 passed.
  - chunk02: 934 passed.
  - **Total:** 4023 passed, 1 skipped, 0 failed. The per-chunk counts match the first run's 1898, 1192 and 934.
  - The background job's exit code 1 came from the closing `tail -4` over three files, not from pytest.

| # | Law (test) | Cause | Fix | Ruling |
|---|---|---|---|---|
| 1 | TC-204 `test_colour_budget_app.py::test_TC_204_modal_titles_and_the_key_map_are_bright` (HLR-202, LLR-202.2) | Inc K put two accent rules in `app.py` between `HelpScreen` and `TaskboardApp`, the span the law scans as help source: `PadArea { border: tall #2dd4bf 40% }` (always on) and `#rv-box { border: round #2dd4bf; border-title-color: #2dd4bf }`. | `app.py:1510`: the pad's resting border is the neutral `tall #1b2431` (the `.modal Input` convention). `taskboard.tcss:122-126`: `PadArea:focus { border: tall #2dd4bf 40%; }`. `app.py:2120-2121`: the review list's frame is `round #334154` and its title is `#e6edf7` bold (the `.modal` and `.modal-title` convention). The law now also requires the accent in `PadArea:focus`. | The budget gives the accent to the field being edited, so the pad keeps it only while focused (it loses it when `alt+n` moves focus to the new-project field). A modal title is bold bright (LLR-202.2), so the review list's accent title broke the law's intent as well as its scan. Its accent frame went too: no other modal uses one. The law is not weakened, it gains one arm. |
| 2 | TC-206 `test_english.py::test_TC_206_no_literal_in_the_source_carries_the_old_copy` (HLR-204) | `inbox.py:48` `'con'` is the Windows device name in `RESERVED_STEMS` (SEC-7), not Spanish copy. `suggest.py:22` is the stop-word list `STOP` (LLR-4403.1), which holds `las los para por que una`. | `tests/test_english.py:126-134, 145`: the law's own data-exemption mechanism (`STORED` and `CITY_TO_ZONE`, "place names are data") gains `RESERVED_STEMS` (exact membership) and `stop_words()`. That function exempts a literal only when every word of it is in `STOP`. An in-test guard asserts that a Spanish sentence which shares `para` and `que` with the list is still seen. | Both values are data that code matches against and never paints (`inbox.py:140`, `suggest.py:88`). Moving them to a data file would break `suggest.py`'s stated purity ("never reads a file"). Hiding the words, by splitting or encoding them, would weaken the law without saying so. A named exemption is the honest route, as the law already states for place names. |
| 3 | TC-401 `test_markup_census.py::test_TC_401_no_textual_sink_takes_a_markup_str` (HLR-401) | Three sinks: `app.py:1030` `AddedList._paint` (Inc L), `modals.py:582` `InkArea._build_highlight_map` (Inc C), `modals.py:3046` `Label(DETAILS_NOTES_LABEL)` (Inc C). | (a) `modals.py:706-713`: real safety, no exemption. The markup constant `DETAILS_NOTES_LABEL` is now `details_notes_label() -> Text` (`Text.assemble` and `append`), which the census trusts. Its plain text and spans are identical to the old markup (checked with a probe), and TC-4276 stays green. (b) An EXEMPT row for `render_added_list`: it already builds Text pieces with no parser (notes go through `notes_text`), but it lives in `views.py`, which the census does not reach. The row cites TC-4340, which proves that board text shaped like markup is drawn literally (the same precedent as `render_marks`). (c) An EXEMPT row for `InkArea`: `self._highlights.update(new)` is `dict.update` on TextArea's highlight map, with `(start, end, style-name)` tuples. It is not a widget sink and carries no text. | User text can reach (b), so it got real safety first: the Text pieces exist and TC-4340 covers them, and only the census's module boundary needs the row. (a) holds only app constants, but converting it was cheap, so it takes no exemption. (c) is a false positive of the census's name-based `update` match. A row that states this is honest, and editing the code only to dodge the match would not be. |
| 4 | `test_prism_laws.py::test_no_literal_in_the_source_can_emit_the_second_person` | `modals.py:591` N4: "That colour would change the text you see: nothing changed." | `modals.py:591`: "That colour would change the visible text: nothing changed." `tests/test_colour_palette.py:47` and `tests/test_colour_pens.py:55` pin the new text. | The new text keeps the meaning and is the wording LLR-4203.17 and LLR-4205.15 already use ("the line's visible text"). |

## Pending, outside this pass

- `modals.py:725-726` `ColourPalette #cp-box` (Inc C) also has an accent frame and an accent
  title. No law scans it, and it is a palette anchored at the cursor rather than a centred
  modal. It is left as built, as a candidate for the colour-budget backlog.

## Ledger lines

`LED-2026-11-01-incC.8`, `LED-2026-11-01-incL.6`, `LED-2026-11-01-incK.7`.
