# Increment 002 — LLR-1602.1, LLR-1602.2, LLR-1602.3 · `the persisted "show in presentation" flag`

| Field | Value |
|---|---|
| Batch | `2026-10-16-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1602` / `LLR-1602.1`, `LLR-1602.2`, `LLR-1602.3` (and LLR-1001.2's read-only clause, narrowed — LED-2026-10-16-batch-01.2) |
| Acceptance | `AT-1602` · white-box `TC-1603`, `TC-1604`, `TC-1605` · unit: `TC-1603` (the model read/write crosses the `board.json` boundary) |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-16` |

## 1 · What changed

`Task.show_in_present: bool = True`, in `_TASK_KEYS`, read as `False` only from the JSON `false`, omitted from `board.json` when `True` — a board with nothing hidden keeps its bytes, and so does every team push. `views.present_tasks` returns the shown tasks only (field, brief, counts and axis follow); `views.present_hidden` lists the rest (one shared pool, `_present_pool`). `PresentScreen` binds `space` (hide the cursor task, save, cursor to the next by due / the previous at the end / none) and `a` (show every hidden task, save; nothing hidden → nothing written), both `priority=True`; its id list is read live; the hint row reads the commission's texts plus ` · <n> hidden`, as a plain `Text` (the markup census); the frame — and so `x` — never carries the count. The task editor's title row gains `Show in presentation` (`#f-present`), checked by default, applied by the existing `setattr`/`Task(**data)` paths. The read-only wording of `PresentScreen`, `tests/present_board.py`, AT-1001 and the report test is narrowed honestly: open/move/`x`/`esc` write nothing; only `space`/`a` write, and only the flag.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-1602.1 | `Task.show_in_present`; `_TASK_KEYS`; `from_dict`; `_to_dict` omission |
| `taskboard/views.py` | source | LLR-1602.2 | `present_tasks` filter; `present_hidden`; `_present_pool` |
| `taskboard/app.py` | source | LLR-1602.2 | `PresentScreen`: docstring, `space`/`a` bindings, `_shown_ids`, `_cursor`, `action_hide`, `action_show_all`, the hint row |
| `taskboard/modals.py` | source | LLR-1602.3 | `TaskModal`: the `#f-present` checkbox in `#task-head`; `show_in_present` in the result |
| `tests/test_present_hide.py` | test | HLR-1602, LLR-1602.1, LLR-1602.2, LLR-1602.3 | new: TC-1603 ×3 (+4 parametrised), TC-1604 ×3 (+2), TC-1605 ×2, AT-1602 |
| `tests/test_edit_window.py` | test | LLR-1602.3 | `CONTRACT_IDS`, `FOCUS_MARKED`, `TAB_ORDER` gain `f-present` (law-driven: the editor must paint, focus-mark and tab to the new box; the tab stop after the title is accepted in LED .5) |
| `tests/test_present.py` | test | LLR-1602.2 | AT-1001's docstring: the narrower no-write law; assertions unchanged |
| `tests/test_report.py` | test | LLR-1602.2 | the read-only comment narrowed; assertions unchanged |
| `tests/present_board.py` | fixture | LLR-1602.2 | the docstring's "never saved" narrowed |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-002-118x31-present-open.svg` | generated | HLR-1602 (AT-1602) | the app's own `export_screenshot()` |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-002-118x31-hidden.svg` | generated | HLR-1602 (AT-1602) | after `space`: the hint shows `· 1 hidden` |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-002-118x31-show-all.svg` | generated | HLR-1602 (AT-1602) | after `a` |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-002-118x31-editor.svg` | generated | LLR-1602.3 | the editor's title row with the box |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-002-80x25-present-open.svg` | generated | HLR-1602 (AT-1602) | the app's own `export_screenshot()` |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-002-80x25-hidden.svg` | generated | HLR-1602 (AT-1602) | after `space` |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-002-80x25-show-all.svg` | generated | HLR-1602 (AT-1602) | after `a` |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-002-80x25-editor.svg` | generated | LLR-1602.3 | the editor at 80 columns |
| `.dev-flow/2026-10-16-batch-01/evidence/capture_app.py` | doc | HLR-1602 | the 002 plan gains the editor frame |
| `.dev-flow/2026-10-16-batch-01/evidence/mutate.py` | doc | HLR-1602 | battery 002 (N1–N11) |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** — at the cap, as commissioned (the brief's increment 002 names these four: the model, the screen, the editor, the filter); no fifth file was needed (`team_sync.py` untouched — P-6) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_hide.py tests/test_edit_window.py tests/test_present.py tests/test_report.py tests/test_markup_census.py`; captures: `python .dev-flow/2026-10-16-batch-01/evidence/capture_app.py 002`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 and A | `tests/test_present_hide.py` TC-1603 (7 nodes), TC-1604 (4 nodes), TC-1605 (2 nodes) | in the full suite (`suite-002.txt`) |
| B | `tests/test_present_hide.py::test_AT_1602_space_hides_and_it_is_remembered_a_shows_all` | in the full suite (`suite-002.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider` | 2 failed, 2616 passed (`suite-002.txt`); the 2 failures are the pre-existing `base_ref` pair (`preexisting-base-failures.txt`) |

| Field | Value |
|---|---|
| **RED counterfactual** | increment 002's tests against the four source files at `ea002aa` (increment 001's commit): 18 failed, 32 passed — 12 of the 13 new nodes RED; the 13th, `test_TC_1603_a_board_with_nothing_hidden_keeps_its_bytes`, is a preservation law by design (GREEN on base, RED under N1); the 6 `test_edit_window.py` arms that now name `f-present` RED · `.dev-flow/2026-10-16-batch-01/evidence/red-002.txt` · restore digest (of the four files' digests) `280885dc0815f5941943b3fa77fb3262f239ed43a23f7ef1d7be50a5ebcda011` |
| **Mutation verdicts** | 11 mutants: N1 omission removed (TC-1603 bytes) KILLED · N2 `is not False` → `bool(...)` (TC-1603 `0`/`null` arms) KILLED · N3 key out of `_TASK_KEYS` (the `extra` arm) KILLED · N4 filter removed (TC-1604, AT-1602) KILLED · N5 `space` without save (AT-1602) KILLED · N6 `a` saves with nothing hidden (TC-1604) KILLED · N7 `a` `priority=False` · SURVIVED — an equivalent mutant today, verified by the code-reviewer: the app's `a` is non-priority (`keymap.py:74`) and `PresentScreen` has no focusable child, so the screen's binding already wins; the behaviour ("`a` opens no editor", TC-1604 arm i) is asserted and holds; equivalence holds only while both conditions do (comment at the binding) · N8 cursor reset to the first (TC-1604) KILLED · N9 hint count dropped (TC-1604 hint) KILLED · N10 editor result drops the key (TC-1605) KILLED · N11 `present_hidden` empty (TC-1604) KILLED · arms that stayed GREEN: N7 only, as above · `.dev-flow/2026-10-16-batch-01/evidence/mutation-002.txt` |
| **Instrument RED-proof** | none — no new instrument (the harness and the capture script were shown failing first at increment 001) |
| **Emitted-form assertion** | 2 artifacts: `board.json` is asserted as `Board.save` EMITS it (bytes and parsed records, TC-1603/AT-1602); the exported SVG as `x` emits it (AT-1602) |
| **Reverse census** | 5 probes: B1 `grep -rl` over `tests/ taskboard/` — `present_tasks` → `test_present.py`, `test_present_rulers.py` (shown-only: the oracle board hides nothing, unchanged); `PresentScreen` → `test_markup_census.py` (the hint became a plain `Text` — the census's TC-401 was RED on a markup `str` and is green), `test_markup_sites.py`, `test_present.py`, `test_report.py` (zero-save arms still hold); `_open_ids` → none left; `_TASK_KEYS` → `models.py` only; `_to_dict` → `test_cascade.py`, `team_sync.py` (push follows the omission, P-6); `TAB_ORDER`/`f-title` → `test_edit_window.py` (updated, law-driven), `test_app.py`, `test_cascade_app.py`, `test_emoji_picker.py`, `test_links.py`, `test_milestones.py` (query `#f-title` by id, unaffected) · B2 no file moved · B3 no golden · B4 `board.json` gains an optional key consumed by `team_sync` (push) and older versions (`extra` round-trip) — byte law TC-1603 · A3 `Task` field + `TaskModal` result key — both consumers (`setattr`, `Task(**data)`) apply it unchanged (TC-1605) |
| **Correction population** | none — no correction |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-16-batch-01/evidence/suite-002.txt | d90417b1b8b75f1865947c7928f405570b78072aa3658e50a914168b7f3a1724 |
| red-002.txt | .dev-flow/2026-10-16-batch-01/evidence/red-002.txt | b4508983c6952ff78118d606483803aebdd0ee2f53a0b480103d90c7656bdd60 |
| mutation-002.txt | .dev-flow/2026-10-16-batch-01/evidence/mutation-002.txt | 4e8cfc6322439e09bed17041824a54a9c46d248bdb6074a7be50f8ba3564b9db |
| app-002-118x31-present-open.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-002-118x31-present-open.svg | 29d1dab7d00b8385b801a157520757fcd8c66416633f246e71e9ac17f789a992 |
| app-002-118x31-hidden.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-002-118x31-hidden.svg | 3f05048f8b89f368f443c3b7649d2e86de4cd7be3d621e801334587b855d4ef6 |
| app-002-118x31-show-all.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-002-118x31-show-all.svg | 8ebf3211b84caeac31c8d5d7df0cddcb0b2fdc5521722bf655cc2ab159d39f82 |
| app-002-118x31-editor.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-002-118x31-editor.svg | 09735a8fc7485f7bfdedbf61b8cfbe460553bcb17149755473dbfeff304a0ddd |
| app-002-80x25-present-open.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-002-80x25-present-open.svg | 0cd7cc4bf7ae4d11652664658996e447f769b572975c23b7e39aac8c5b9bbcb0 |
| app-002-80x25-hidden.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-002-80x25-hidden.svg | b0988c5b48035c302d5f3721011283d9dbe097f81a4b884dd3241c8bb6b369ba |
| app-002-80x25-show-all.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-002-80x25-show-all.svg | 4958563afedde54e54f900a9f1ed2d809afbcf2cd9f5cc498a38ff5540992795 |
| app-002-80x25-editor.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-002-80x25-editor.svg | 46dc525de15532bd9d65baf93aaed88190231fbba5a82ae3cccd039a769317d7 |

| Field | Value |
|---|---|
| **Evidence files** | `11 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS with notes, 0 HIGH · 0 MEDIUM · F1 LOW (N7's equivalence is conditional) → recorded in §4 and as a comment at the binding · F2 LOW (the filter's pool built twice) → fixed: `_present_pool` · F3 LOW (long lines in `test_edit_window.py`) → fixed; the test-edit judged stricter, not weaker |

## 5 · Risks

A stray `space` mid-meeting is recovered only by `a`, which also reveals tasks hidden on purpose (no undo — declared limit). The flag is presentation-only, not confidentiality: a hidden task stays in `board.json` and in team pushes (security P2 note).

## 6 · Pending items / spec deviations

- the brief's increment 002 named "the render filter in views.py" — done in `present_tasks` (the renderer's own source), so `render_present` itself needed no change.
- the title input keeps ≥ 20 painted cells at 80 (TC-1605); UX2-N2 observed here.

## 7 · Suggested next task

Increment 003 — the `?` help modal's Keys band and pinned global line (`modals.py`, `keymap.py`).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 4 / 4, the reason declared |
| 2 | Tests in this increment | ✓ | `tests/test_present_hide.py` (new) + 4 law-driven updates |
| 3 | Layer 0 where it applies | ✓ | TC-1603 (crosses the `board.json` boundary) |
| 4 | RED counterfactual | ✓ | §4, `red-002.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-002.txt` |
| 10 | Load-bearing emptiness | ✓ | `_open_ids` → no hit: positive control, the same grep finds `_shown_ids` in `app.py` |
| 11 | Mutation verdicts | ⚠ | §4: 10/11 KILLED, N7 an equivalent mutant (declared, reviewer-verified) |
| 12 | Instrument RED-proof | ✓ | none new, declared |
| 13 | Correction population | ✓ | none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4 |
