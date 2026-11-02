# E4 independent tests — Inc X

Base: `8506cb7b071a4a75b23f33805ace7f270374a48b` (`incX-tests`). Tests were written from the requirements, graphs, seams, rulings and E3 addenda only; no implementation tree was read.

## New tests and RED evidence

- `tests/test_present_html_export.py`: 45 test functions, 166 collected cases, covering all 42 LLRs and the binding E3 addenda.
- `tests/test_present_html_at.py`: the six black-box AT-4501..AT-4506, driven through `run_test` keys/dialogs with real files under temporary homes.
- Evidence: `evidence/red-base.txt`. Its header prints this worktree's `taskboard.__file__`; the run was `env -u NO_COLOR PYTHONIOENCODING=utf-8 python -m pytest tests/test_present_html_export.py tests/test_present_html_at.py --tb=short`.
- Result: **172 collected; 133 failed; 39 passed**. There were no collection, import, fixture, attribute or type errors.

The 133 RED cases fail on the designed base behavior: `x` writes SVG rather than the scoped HTML deck; hidden/URL/board-scope and byte-oracle assertions consequently have no deck; `o` and the shared write/offer/error route are absent; SVG/rasteriser code and process calls remain; `H` is off the bar and in global help; presentation help, bindings and README retain their base wording. AT-4504 also exposes the unhandled failing `reports/` path. These are behavioral failures, not failures to import proposed helpers.

### Base passes by design

- **TC-4764, 36/36:** literal hint-text stability guards for LLR-4506.4; the design expressly leaves the hint byte-stable.
- **TC-4713 and TC-4714, 2/2:** the unchanged narrow-terminal warning and no-file behavior.
- **AT-4505, 1/1:** the same unchanged narrow behavior through the black-box route.

TC-4703/4704 use A-R2-2's independent oracle: `H` runs on a separate fixture whose tasks already have empty `urls`, while `x` runs on an otherwise identical fixture with URLs. TC-4727 also asserts S-R2-2: source task URL lists remain exact after `x`, and a subsequent real save writes those original URLs.

## Mutant table

Each E1 negative control is mapped to the test whose assertion kills it. Parameterized rows cover every required view/width arm.

| LLR | Negative control | Killing test |
|---|---|---|
| 4501.1 | Use `H`'s `deck-…` project filename | TC-4701, TC-4701b |
| 4501.2 | Use `H`'s `deck-<date>.html` filename | TC-4702 |
| 4501.3 | Extract with the wrong board key | TC-4703 (2 views; independent byte oracle) |
| 4501.4 | Pass `people={}`; mention becomes plain text | TC-4704 (independent byte oracle) |
| 4501.5 | Export every shown project instead of the presented one | TC-4705 (shown/hidden presented flag) |
| 4501.6 | Use board order rather than presentation order | TC-4706 (overview and slides) |
| 4501.7 | Extract every registry board | TC-4707 (views 1 and 3) |
| 4501.8 | Skip folded projects/tasks | TC-4708; AT-4502 |
| 4501.9 | Export open tasks only | TC-4709 (views 1 and 3); AT-4502 |
| 4501.10 | Save the board during export | TC-4710 (6/6 board/history hashes) |
| 4501.11 | Registry lookup fails for unlisted `bid=None` | TC-4711 (label and `this board`) |
| 4501.12 | Return without writing an empty view-3 scope | TC-4712 |
| 4501.13 | Drop the narrow warning branch | TC-4713; AT-4505 |
| 4501.14 | Write before the width check | TC-4714; AT-4505 |
| 4501.15 | Keep a missing project id or insert `None` | TC-4715 |
| 4502.1 | Extract the unfiltered board | TC-4721 (title and id, 3 views); AT-4501 |
| 4502.2 | Filter tasks but not hidden projects | TC-4722; AT-4502 |
| 4502.3 | Keep archived/projectless tasks or the Inbox row | TC-4723 (views 1 and 3) |
| 4502.4 | Use `present_tasks` instead of `present_tasks_m` | TC-4724 (views 1 and 3) |
| 4502.5 | Pass every milestone class to the legend | TC-4725 |
| 4502.6 | Capture hide flags when `R` opens | TC-4726; AT-4501 |
| 4502.7 | Leave task URLs in the deck | TC-4727 (3 views) |
| 4503.1 | Keep the old `Exported …` toast | TC-4731; AT-4501, AT-4503 |
| 4503.2 | Leave `o` unbound in `R` | TC-4732; AT-4503 |
| 4503.3 | Offer never expires or is reusable | TC-4733, TC-4733b; AT-4503 |
| 4503.4 | Let write `OSError` escape | TC-4734; AT-4504 |
| 4503.5 | Preserve an earlier offer after failed write | TC-4735; AT-4504 |
| 4503.6 | Swallow opener failure or let URI `ValueError` escape | TC-4736, TC-4736b |
| 4503.7 | Render toast folder with `markup=True` | TC-4737 |
| 4504.1 | Keep SVG/PNG writer beside the deck | TC-4741 (one changed file per view); AT-4501, AT-4502 |
| 4504.2 | Keep the external rasteriser | TC-4742 (3 views; `run`/`Popen` forbidden) |
| 4504.3 | Leave removed SVG/rasteriser functions or imports | TC-4743 (package inspection) |
| 4505.1 | Keep `H` as `bar=False` | TC-4751 (20/20); AT-4506 |
| 4505.2 | Promote all global keys and change overflow | TC-4752 (20/20) |
| 4505.3 | Make `H` universal and lose multiple words | TC-4753 (20/20) |
| 4505.4 | Give `H` an empty label | TC-4754 |
| 4505.5 | List `H` in both help band and global line | TC-4755 (10/10); AT-4506 |
| 4506.1 | Keep `SVG + PNG` help wording | TC-4761; AT-4506 |
| 4506.2 | Bind `o` without its help row | TC-4762; AT-4506 |
| 4506.3 | Add `o` but drop an existing binding | TC-4763 (exact base set plus `o`) |
| 4506.4 | Add export wording to the hint | TC-4764 (36/36 literal base strings) |
| 4506.5 | Leave README's SVG/PNG presentation wording | TC-4765 |

Additional addenda controls: traversal/reserved/empty slugs → TC-4701b; shared offer after `escape` → TC-4733b; source URL rebinding and next save → TC-4727; folded/done titles and notes → TC-4708/4709; renderer-only single-file write → TC-4741/4743.

## Legacy tests changed and why

The changes below remove only the export superseded by HLR-4504 or update the `H` seat required by HLR-4505. Frame, hint, help, hide and persistence assertions remain where they are independent of SVG/PNG.

- `tests/test_present.py` — AT-1001: removed the `x` SVG/PNG and Edge-toast arm; retained the frame oracle, cursor expansion and no-save/no-HTML exit controls.
- `tests/test_present_all.py` — AT-2104 and TC-2104: removed the view-3 SVG content and `present_paths` naming arms; retained three-view navigation, cursor hand-off and exact hints.
- `tests/test_present_backlog_round.py` — deleted export-only TC-2404 and AT-2404; removed the PNG fixture and SVG helpers; AT-2402 retains board-chip/frame separation, AT-2403 retains help/modal/hint behavior without export byte checks.
- `tests/test_present_room.py` — TC-1608: removed SVG serialization assertions; retained the no-presenter-text frame law at both sizes.
- `tests/test_present_views_app.py` — AT-1803: removed SVG export/file-content arms while retaining view/cursor/scroll/hide/exit behavior; deleted export-name-only TC-1809.
- `tests/test_tick_label.py` — TC-1701 positive control and presentation sweep: removed SVG writer arms; retained the literal scale regex control and all frame sweeps.
- `tests/test_legend.py` — TC-2607, TC-2608 and AT-2605: removed SVG/export arms; retained strips, hidden-class filtering, all three frames and key-driven hide/unhide checks.
- `tests/test_present_hide.py` — AT-1602: removed the SVG arm; retained flag-only save, restart persistence and show-all restoration.
- `tests/test_present_note_highlights.py` — deleted AT-2903 because every assertion concerned the removed split SVG and its serialization; the remaining note-highlight and hostile-markup tests are unchanged.
- `tests/test_markup_census.py` — updated the reason: `_frame_text` is no longer shared with the `x` export.
- `tests/test_present_narrow.py`, `tests/test_present_polish.py` — inspected and intentionally unchanged: their controls are narrow/no-file and stable hint wording, not SVG/PNG behavior.
- `tests/test_report_export_app.py` — TC-3117 rewritten under ruling 7: `H` is one seat, `bar=True`, `primary=True`, present in both bar layers and absent from global keys; palette, help and lowercase `h` controls remain.
- `tests/test_added_list.py` — TC-4321 drops `H` from the literal `global_keys("gantt")` expectation under ruling 15 because `H` is now on the bar.
- `tests/test_colour_budget_app.py` — `KEYBAR_BASE` re-baselined only at gantt 80 primary and gantt 118 more, using the exact E3-P1 strings in `e3-addenda.md` and this file's comment-plus-evidence convention (ruling 15).
