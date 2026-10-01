# Increment 001 — HLR-001 / HLR-002 · `Full-screen task editor with live preview`

> Template: flow `templates/increment-template.md` (core). Reserved field names kept literal.
> Lives at `.dev-flow/2026-09-30-batch-01/03-increments/increment-001.md`.

| Field | Value |
|---|---|
| Batch | `2026-09-30-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | n/a — one lane |
| Requirement(s) | HLR-001, HLR-002, LLR-001.1, LLR-001.2, LLR-001.3, LLR-001.4, LLR-002.1 |
| Acceptance | AT-001, AT-002, AT-005 · white-box TC nodes listed in §4 · Layer 0: `notes_preview_markup` exercised through AT-002 |
| Agent | `software-dev` |
| Date | `2026-09-30` |

---

## 1 · What changed

`TaskModal` is now the owner-chosen variant C: a full-screen editor (`#task-box`) with a
one-line title row (the `.modal-title` "Edit task · ctrl+e emoji" + the title `Input`), a chip
row of properties (project · phase · priority · start 📅 → due 📅 · blocked · archived ·
pinned) that folds into two rows below `TASK_CHIPS_ONE_ROW = 122` columns, a horizontal split
of the notes `TextArea` (left, 1fr) and a live preview (right) that renders each line through
the app's `_highlight_markup` (`notes_preview`, parsed by Rich into a `Text` so Textual never parses note text), refreshes on every notes change and
keeps the cursor's part of the note in view, and a 5-row footer with URLs, images, Paste
image, Save, Cancel. One-row controls lose the tall border; focus is an accent (`#2dd4bf`) left
bar on the focused control (always present in the box colour when unfocused, so nothing
shifts). The preview is not a tab stop. Every widget id, the `_save` payload, the bindings and
the calendar / paste-image handlers are unchanged. All new CSS is scoped to `#task-box`.

Measured with the round's 23-line fixture (`evidence/measure-baseline.json` →
`evidence/measure-after.json`):

| size | note rows visible | notes width | title on screen | Save on screen | all 17 ids on screen |
|---|---|---|---|---|---|
| 120×36 | 3 → **23** | 50 → 55 | no → **yes** | no → **yes** | no → **yes** |
| 80×24 | 3 → **11** | 50 → 35 | no → **yes** | no → **yes** | no → **yes** |

The measured one-row threshold is 122 columns (121 clips `f-pinned`, mutation M5), so the
120×36 reference folds the chip row into two rows; at 80 columns the folded row fits.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | HLR-001, HLR-002, LLR-001.1–001.3, LLR-002.1 | `TaskModal.compose` rebuilt; `TASK_CHIPS_ONE_ROW`, `notes_preview` (returns a Rich `Text`, security S1); `on_mount`/`on_resize`/`_fold_chips`, preview change + cursor-follow handlers; `Vertical` and `events` imports |
| `taskboard/taskboard.tcss` | source | HLR-001, LLR-001.1, LLR-001.2, LLR-001.4 | new `#task-box` block (layout, one-row controls, focus bar, fold) |
| `tests/test_edit_window.py` | test | AT-001, AT-002, AT-005, LLR-001.1–001.4, LLR-002.1 | NEW — 37 nodes |
| `prototypes/edit_modal/measure_real.py` | fixture | HLR-001, HLR-003 (P-1, P-5 measurements) | NEW — throwaway measurement harness (real app, not shipped) |
| `prototypes/edit_modal/capture_after.py` | fixture | HLR-001, HLR-003, HLR-004 (captures) |
| `prototypes/edit_modal/shoot_after.ps1` | fixture | HLR-001, HLR-003, HLR-004 (captures) |
| `prototypes/edit_modal/proto.py` | fixture | HLR-001, HLR-002 (the prototype round the owner judged; throwaway, committed as the decision's record) |
| `prototypes/edit_modal/shoot.ps1` | fixture | HLR-001, HLR-002 (the prototype round the owner judged; throwaway, committed as the decision's record) |
| `prototypes/edit_modal/look.py` | fixture | HLR-001, HLR-002 (the prototype round the owner judged; throwaway, committed as the decision's record) |
| `prototypes/edit_modal/build_html.py` | fixture | HLR-001, HLR-002 (the prototype round the owner judged; throwaway, committed as the decision's record) |
| `prototypes/edit_modal/NOTES.md` | doc | HLR-001 | round notes |
| `prototypes/edit_modal/out/facts_edit.json` | generated | HLR-001 (the round's measurements) |
| `prototypes/edit_modal/out/after/edit_120x36.svg` | generated | HLR-001, HLR-002 (after-captures of the real app) | NEW — throwaway capture harness for the after-captures |
| `prototypes/edit_modal/out/after/edit_80x24.svg` | generated | HLR-001, HLR-002 (after-captures of the real app) | NEW — throwaway capture harness for the after-captures |
| `prototypes/edit_modal/out/after/wt_edit_120x36.png` | generated | HLR-001, HLR-002 (after-captures of the real app) | NEW — throwaway capture harness for the after-captures |
| `prototypes/edit_modal/out/after/wt_edit_80x24.png` | generated | HLR-001, HLR-002 (after-captures of the real app) | NEW — throwaway capture harness for the after-captures |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 1 (uncapped) |
| Doc files | batch record only (outside the count) |

## 3 · How to test

```
cd C:\Users\jjgh8\Github\taskboard
set PYTHONUTF8=1
python -m pytest -q tests/test_edit_window.py tests/test_app.py tests/test_emoji_picker.py
python prototypes/edit_modal/measure_real.py          # the table in §1
python prototypes/edit_modal/capture_after.py svg     # out/after/edit_*.svg
```
Manual: `python -m taskboard`, select a task, `e`; type in the notes and watch the preview;
tab through; resize the terminal across ~122 columns and watch the chip row fold.

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | `notes_preview` is a 2-line pure function, exercised through AT-002's painted checks and the 5 markup-safety nodes | executed via AT-002 |
| **A · white-box** | `core` · `full` | `test_every_chip_stays_reachable_at_every_width[*]` (18), `test_focus_mark_shows_on_every_one_row_control`, `test_save_payload_round_trips_every_field`, `test_project_modal_keeps_its_box`, `test_an_empty_note_previews_as_nothing`, `test_escape_discards_an_edited_task`, `test_the_preview_paints_markup_typed_in_a_note_as_text`, `test_a_bracket_textual_would_parse_neither_crashes_nor_vanishes[4]` | 28 passed |
| **B · black-box** | `core` · `full` | AT-001 `test_the_notes_own_the_screen_while_writing[120x36,80x24]`, `test_a_new_task_gets_the_same_room`; AT-002 `test_the_preview_paints_the_note_on_open`, `test_the_preview_follows_the_typing_to_the_last_line`; AT-005 `test_tab_walks_the_editor_and_save_works_from_the_keys[120x36,80x24]`, `test_the_editor_paints_its_keys_in_full[120x36,80x24]` | 9 passed |

Executed: `tests/test_edit_window.py` 37 passed (after the S1 fix); with `tests/test_app.py` and
`tests/test_emoji_picker.py`: **217 passed** in 99.26 s (`evidence/inc001-green.txt`). Full
suite at the batch gate: see increment 002 §4 (`evidence/full-suite-after.txt`).

### RED counterfactual — executed, not predicted

RED on base (`a9bbd1c`, `modals.py`/`taskboard.tcss` untouched in the tree at the time):
`evidence/inc001-red-on-base.txt` — **29 failed, 3 passed**. The 3 GREEN-on-base nodes are the
preservation tests by design (payload round trip, ProjectModal box, escape discards); each is
shown RED under its own mutation below.

| Field | Value |
|---|---|
| **RED counterfactual** | 29 of 32 new nodes RED on the base tree (`evidence/inc001-red-on-base.txt`); the 3 preservation nodes RED under mutations M6 (payload drops `pinned`), M7 (rules leak to `#modal-box`) and — for escape — `not-run` as a mutation (escape is unchanged code; GREEN on base by design). Restore proven per mutation by SHA-256 in `evidence/inc001-mutations.txt`. |

| Field | Value |
|---|---|
| **Mutation verdicts** | 12 mutations, `evidence/inc001-mutations.txt` (script `evidence/mutate_inc001.py`, `PYTHONDONTWRITEBYTECODE=1`): M1 no change handler KILLED · M2 no initial render KILLED · M3 preview focusable KILLED · M4 no focus bar KILLED · M5 threshold 121 KILLED (`[threshold]` arm only; the other 17 width arms stay GREEN, as they should) · M6 payload drops pinned KILLED · M7 rules leak to `#modal-box` KILLED · M8 preview does not follow cursor KILLED · M9 ctrl+v hint gone KILLED · M10 notes back to 5 rows KILLED · M11 preview renders raw notes KILLED · M12 Static parses the markup string (S1) KILLED · every restore ok=True (run after the code-review fold, §6). |

### Instrument RED-proof

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `_fully_visible` / `_note_rows` (compositor reads) | the base editor | `only 3 note rows visible`; `off-screen or clipped while writing` (inc001-red-on-base.txt) |
| painted-segment reader `_preview_segments` | first version measured codepoints, not cells | `f-due: no accent mark painted at its left edge` — the 📅 is 2 cells; fixed to `cell_len` |
| `measure_real.py` | base tree | 3 rows / title false / save false (measure-baseline.json) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown reporting a failure before its first PASS was believed (table above) |

### Emitted-form assertion

| Field | Value |
|---|---|
| **Emitted-form assertion** | 1 artifact: the painted screen — every AT reads the compositor's painted strips / clipped regions (what the terminal is sent), not markup strings |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc001-red-on-base.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc001-red-on-base.txt` | `805f085a2b0764806c64c8e13b9dd77fd232f885f0b5058fc8dfc81f4e118063` |
| inc001-mutations.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc001-mutations.txt` | `e5544b869d5d13385120d752a51c805514275a3d96be44b81c1a1becce83a86b` |
| inc001-green.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc001-green.txt` | `a1572332f1807e5e6b36b993759c73cfc27e1ed0a85636c5c26cd585760fe612` |
| s1-red.txt | `.dev-flow/2026-09-30-batch-01/evidence/s1-red.txt` | `708fc305efb1e476a62e875ecd572f6b433b2aa1999f10318fb69a44bd0d8491` |
| full-suite-after.txt | `.dev-flow/2026-09-30-batch-01/evidence/full-suite-after.txt` | `a64ea72a3221a02a0467518571349064ab54f545db08e5c11c9276924fe5fc15` |
| measure-baseline.json | `.dev-flow/2026-09-30-batch-01/evidence/measure-baseline.json` | `1fe8ea53f36acd6351325cea1b9a957bde466637ffe1218af01bd72e746aa3b1` |
| measure-after.json | `.dev-flow/2026-09-30-batch-01/evidence/measure-after.json` | `69ac2f6c578b602b368441576e5ee41436854d436d59cfe2d15e4df6951432b7` |

| Field | Value |
|---|---|
| **Evidence files** | 7 artifacts at `artifact_homes.evidence`, each cited above with the SHA-256 of its stored bytes; the full-suite transcript `full-suite-after.txt` holds `1506 passed` |

### Load-bearing emptiness

No claim rests on an absence except "the preview is never a tab stop" — the tab-order AT walks
all 17 stops and asserts the exact list (M3 makes the preview focusable → RED).

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by other tests | `grep -rln "TaskModal\|f-notes\|modal-title" tests/` | `test_app.py`, `test_emoji_picker.py` — both re-run: 185 passed |
| B2 file moved | none moved | did not fire |
| B3 byte-identical goldens | `grep -rl "modals.py\|taskboard.tcss" tests/` | no golden captures the editor; did not fire |
| B4 artifact consumed elsewhere | `_save` payload → `app._on_task_added/_on_task_edited` | payload unchanged; covered by `test_save_payload_round_trips_every_field` |
| A3 interface consumed by another module | `grep -n "TaskModal(" taskboard/` | `app.py:1280`, `app.py:1305` — constructor unchanged |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes (B1 · B2 · B3 · B4 · A3): B1 2 files re-validated green; B2/B3 did not fire; B4 payload consumers covered by the round-trip test; A3 two constructor call sites, signature unchanged |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | none — no correction |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS-WITH-NOTES, 0 HIGH / 1 MEDIUM / 4 LOW · and `security-reviewer` (family C, C-17) · BLOCK — BLOCK-UNTIL: S1 · S1 (MEDIUM: Textual parses `[LINK=…`/`[B]` in a note → MarkupError crash / vanished text) fixed — `notes_preview` returns a Rich `Text`; RED captured in `evidence/s1-red.txt` (3 failed), GREEN after, M12 KILLED; S2 (LOW, control bytes, pre-existing path) → BACKLOG · F1 (private `_compositor`) folded as a one-place helper comment naming textual 8.2.8; F2 `on_resize(event: events.Resize)`; F3 `#f-project/#f-phase/#f-priority/#f-notes` scoped under `#task-box`; F4 "below 80 columns the flags clip" recorded at `TASK_CHIPS_ONE_ROW`; F5 new-task test pauses ×3 |

## 5 · Risks

- Textual private API in tests (`screen._compositor`): a Textual upgrade can break the helpers (they fail loudly, not silently).
- Below 80 columns the folded chip row still clips `f-pinned` (80×24 is the supported floor).
- Preview scroll-follow is proportional, not row-exact: the cursor's line is in view at the ends of the note and approximately in the middle.
- 📅 in a one-row Button: Textual pads the label to 4 cells, so the calendar buttons are 5 wide; a narrower width paints past the region (measured, fixed by width).
- The one-row fields are visually lighter than the old tall-bordered ones; the accent bar is the only focus mark besides Textual's own (checkbox label highlight, button bold).

## 6 · Pending items / spec deviations

- The mutation battery was re-run AFTER the code-review fold (F2–F5) and the S1 fix: 12/12 KILLED, restore digests `26fa8c286c7674b3…` (modals.py) and `3915cad51cddf53a…` (taskboard.tcss) — `inc001-mutations.txt` holds that run. `inc001-green.txt` predates the fold; the full suite at the batch gate covers the folded tree.
- ProjectModal keeps the old crowded layout (out of scope by commission).
- S1 also exists, pre-existing, in `TaskDetails` (not touched here) → BACKLOG; S2 control bytes → BACKLOG.
- The after-captures were taken before the S1 fix; the fix changes how the preview text is parsed, not what a normal note looks like.

## 7 · Suggested next task

Increment 002 — kanban K4 band + priority badges.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | §2: 2/4 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_edit_window.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` ‹one complete run owned by the orchestrator ~ Layer 0› | ⚠ | `notes_preview_markup` is cyclomatic 2; exercised through AT-002, no own node |
| 4 | **RED counterfactual** declared | `core` · `full` ‹RED counterfactual mandatory ~ RED counterfactual› | ✓ | inc001-red-on-base.txt, inc001-mutations.txt |
| 5 | **Reverse census** declared | `core` · `full` ‹reverse census of the touched symbol ~ Reverse census› | ✓ | §Reverse census |
| 6 | `code-reviewer` passed | `core` · `full` ‹RED counterfactual mandatory ~ code-reviewer› | ✓ | §4b, 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane; foreign uncommitted edits in `app.py`, `tests/test_focus.py`, `views.py` (bar_h), `tests/test_gantt.py` untouched |
| 8 | Frozen interfaces untouched | all | ✓ | `TaskModal(board, task)` signature and payload unchanged |
| 9 | Coverage claims verified on disk | all | ✓ | 32 nodes collected and passed |
| 10 | Load-bearing emptiness declared | all | ✓ | §Load-bearing emptiness |
| 11 | **Mutation verdicts** declared | all | ✓ | 12/12 KILLED |
| 12 | **Instrument RED-proof** declared | all | ✓ | 3 instruments |
| 13 | **Correction population** declared | all | ✓ | none |
| 14 | **Emitted-form assertion** declared | all | ✓ | painted strips |
| 15 | **Independent review** names somebody | all | ✓ | `code-reviewer` |
| 16 | **Evidence files** declared | all | ✓ | evidence/SHA256SUMS.txt |
