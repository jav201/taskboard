# Validation — taskboard — Batch 2026-10-02-batch-04

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1 and **names who executed each one**. The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Mode: validation.** Every case below carries a result or one of the seven evidence states, and every executed result names its executor. Executors used on this page: **the orchestrator (this runtime's implementing agent)** — the ONE P4 gate run; **the implementing agent** (`software-dev` role, the same runtime) — per-increment RED-on-base runs and mutation batteries; **`tester`** — author of AT-401..403, AT-407, TC-412, TC-415 and the TC-415 per-arm battery; **`qa-reviewer`** (this evaluation) — read-only checks listed in §Checks run by `qa-reviewer`, none of them a gate run.

## ✅ Verdict (read first)

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Result` · `Layer 0` · `Evidence checklist` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.
>
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.
> A Spanish batch writes `- **Result:** PASS`, not `- **Resultado:** aprobado`: the label, the tokens and the
> reviewer-identity tokens below are the machine's vocabulary.

- **Result:** PASS-WITH-NOTES
- **Layer 0:** 3 units met the criterion · 3 carry a named reddening mutation (`strip_controls` — TC-407 ×256 + shapes; `highlight_segments` — TC-417 ×9; `project_color_on_load` — TC-413 any-colour ×6)
- **Requirements:** 13/13 pass (4 HLR + 9 LLR) · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative) — 4 stories, 7 ATs, each exactly one on-disk node (C-18 checked by collection); notes on where a boundary lives white-box (§Layer B)
- **Surface-reachability (bidirectional):** ⚠ 1 gap (minor, G-001) — the clipboard input has no suite node at the handler; it was reached and observed at the shipped Ctrl+V handler by `qa-reviewer`'s P4 probe (final tree clean, base RED), so the dimension is observed but not pinned
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative (re-run by `qa-reviewer` on the final tree: `_rich(` 0, `escape(` in `modals.py`/`app.py` 0, `json.loads` in `app.py` 0, the one surviving `setattr` in `apply_config_to_board` reads `Project.from_dict`'s validated value)
- **Test ledger:** ✓ reconciles (`1855 − 0 + 359 = 2214`; node-id diff base→final: 0 removed, 359 added; after increment 004, by node id, `2214 − 1 + 5 = 2218`, §Increment 004 re-validation)
- **Evidence checklist (qa-reviewer):** qa-reviewer · 11 of 11 rows ✓ with evidence

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

**Gate run (C-25), executed by the orchestrator (this runtime's implementing agent), consumed here:** `python -m pytest -q -p no:cacheprovider` over the final tree (HEAD `56a1b10` + the batch's working-tree changes) → `2214 passed in 306.98s (0:05:06)`, `exit=0` — `evidence/p4-gate.txt` (sha256 `cb68cdef…0680`, re-hashed by `qa-reviewer`: matches `increment-003.md`). The tail was read from that run's own output file. The tree it ran over is pinned by the frozen sets `inc003-frozen-r2.sha256` (3/3 OK), `inc002-frozen-r4.sha256` (6/6 OK) and, for the increment-001 files no later set covers, `inc001-frozen-r3.sha256` (`modals.py`, `views.py` and the six untouched-since test files OK; its three FAILED lines — `app.py`, `test_markup_sites.py`, `test_details_markup.py` — are files later increments changed and r4/r2 re-pin) — all re-verified by `qa-reviewer` with `sha256sum -c` after the run. The declared clipboard environment flake (`test_win_clipboard_roundtrip`) passed in this run: 0 failures of any kind.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `models.strip_controls` (new, branches per code-point class) | cyclomatic ≥ 3; the one rule four doors read | `tests/test_control_bytes.py::test_TC_407_strip_controls_keeps_exactly_the_printable[0..255]` (256 derived arms) + `::test_TC_407_strip_controls_shapes` | executed — 257 passed in the gate run (orchestrator) |
| `views.highlight_segments` (new tokeniser, five paths) | cyclomatic ≥ 3; crosses the board/modal seat (D-411) | `tests/test_highlight_segments.py::test_TC_417_segments_drop_markers_and_keep_text[×8]` + `::test_TC_417_the_board_markup_is_unchanged` (≥ 1000 derived inputs vs the frozen base function) | executed — 9 passed in the gate run (orchestrator) |
| `models.project_color_on_load` (any-type input) | crosses the sync→model boundary (S2-2) | `tests/test_sync_fields.py::test_TC_413_any_colour_value_loads[×6]` | executed — 6 passed in the gate run (orchestrator) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `strip_controls` | N1 — the keep-set of the rule also keeps CR (position: the C0 exclusion list) | yes — `…keeps_exactly_the_printable[13]`, `…_shapes`, `test_TC_410_a_saved_board_round_trips` FAILED; restore sha256 `93059509…` OK (= the final `models.py`) | `evidence/inc002-mutations-r2.txt` (implementing agent) |
| `strip_controls` | N2 — the rule keeps DEL (position: the DEL clause) | yes — `[127]` and TC-410 round-trip FAILED | `evidence/inc002-mutations-r2.txt` (implementing agent) |
| `strip_controls` | N3 — the rule drops NBSP (position: the ≥ U+00A0 keep clause) | yes — `[160]`, `…_shapes`, `test_TC_410_the_rule_strips_nothing_else` FAILED | `evidence/inc002-mutations-r2.txt` (implementing agent) |
| `strip_controls` | R7 — the rule also drops newline (position: the kept-whitespace exception) | yes — `[10]`, `…_shapes`, TC-410 strips-nothing-else FAILED | `evidence/inc002-mutations-r4.txt` (implementing agent) |
| `strip_controls` | R8 — the rule drops every character from U+00A0 up (position: the upper keep bound) | yes — arms `[160]..[255]` (96), `…_shapes`, TC-410 FAILED | `evidence/inc002-mutations-r4.txt` (implementing agent) |
| `highlight_segments` | M5 — the tokeniser gives the `==…==` group the wrong tone (position: the group→tone table) | yes — `the_board_markup_is_unchanged` and 3 segment arms (`a ==y== b`, the payload arm, `====`) FAILED; restore sha256 `59595a9f…` OK (= the final `views.py`, r3 pin) | `evidence/inc001-mutations.txt` (implementing agent) |
| `highlight_segments` | M10 — the board markup is re-escaped (position: `_highlight_markup`'s piece join) | yes — `the_board_markup_is_unchanged` FAILED | `evidence/inc001-mutations.txt` (implementing agent) |
| `project_color_on_load` | N9 — an unhashable colour reaches the dict lookup (position: the type guard before the lookup) | yes — `any_colour_value_loads[color0]`, `[color1]`, two matrix arms, `new_projects_and_duplicate_ids`, AT-407 FAILED | `evidence/inc002-mutations-r2.txt` (implementing agent) |

Note on TC-407's reach: the recorded mutants redden the CR, LF, DEL and ≥ U+00A0 arms; no recorded mutant targets the ESC or C1 (U+0080–U+009F) arms specifically. Those arms assert an exact derived output per code point, and the ESC/C1 behaviour is shown RED at the surface by AT-404/AT-405's pre-fix run; recorded as an observation, not a gap.

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| The details view (`enter`) at 140×40 and 80×24 shows the five fields one per row, values at the value column | `enter` in `run_test` | `Project  Website` / `Phase  Doing` / `Priority  high` / `Start …` / `Due …` painted, values at column 23 (C1.1–1.2) | PASS |
| An 89-character project name wraps under its column, nothing cut | `enter` | 2 rows at 140×40, 3 at 80×24, continuations under the value column (C1.3) | PASS |
| A blocked task with no dates; an Inbox task | `enter` | `Doing · blocked`, `—`, `Inbox` painted (C1.4–1.5) | PASS |
| Scrolling the box reaches notes, URLs, images; `esc` closes | `down`, `pagedown`, `esc` | scroll 0 → max, `Images` reached; main screen back (C1.6–1.7) | PASS |
| Matches the after captures; base painted the grid blank | captures `base-details-*` / `after-details-*` | base blank, after as painted (C1.8) | PASS |
| Bracket / backslash / emoji text in delete confirm, archive toast, project picker, phase editor, standup paints exactly, styles as base | `d`, `x`, `P`, `f`, `S` | exact text on every surface at 140×40 and 80×24; bold names and dim meta identical to base (C2.1–2.6) | PASS |
| A hostile synced status in team mode: `P` shows `on_track`; a click opens only the project editor | `P`, mouse click on the painted line | `Shared  ·  on_track …`; the view stays on lanes (C3.1–3.2) | PASS |
| A deeply nested `team.json`: the app starts with a visible toast | app start in team mode | toast `team.json in <tmp> could not be read; team sync waits for a readable file.` (C3.3) | PASS |

**Mechanism used:** a UI test driver — the shipped app headless in `App.run_test(..., notifications=True)`, real keys and a real mouse click, read from the final painted frame (and the base tree driven the same way for contrast)

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — a cognitive walkthrough of the six tasks by `ux-reviewer` |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; no user of this surface exists outside it |

- **Method:** `ux-reviewer` drove 17 criteria (C1.1–C3.3) through the shipped app on fresh temporary boards, at 140×40 and 80×24, and the same driver on the base tree for contrast; executed by `ux-reviewer`
- **Participants or population:** none — no user evaluation (above)
- **Evidence of the evaluation:** `evidence/p4-ux-walkthrough.txt` (sha256 `e9193892…`); captures `evidence/captures/base-details-*` / `after-details-*`
- **Limits:** the headless driver only — no real terminal font, colour profile or wide-glyph rendering; `:smile:` checked as literal text; two sizes walked. Verdict PASS-WITH-NOTES: UXV-1 (UX-3, the title's blank rows above, none below — closed by increment 004), UXV-2 (the 80×24 scrollbar thumb, pre-existing), UXV-3 (a long path in the `team.json` toast wraps mid-sentence) — minor, BACKLOG; recommendations to the operator: PV-1 accept, UX-3 accept by moving one blank row from above the title to below it, UX-4 accept (a 10-cell label column)

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

Every row's "executed" result comes from the ONE gate run, executed by the orchestrator (this runtime's implementing agent), `evidence/p4-gate.txt` (2214 passed, exit 0). The RED-first evidence was executed by the implementing agent (and `tester` where named), on `git archive` exports of the base or the pre-fix tree.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-401 | test | AT-401, AT-402, AT-403 + TC-412 + `tests/test_details_markup.py` (43 nodes) | every reachable §5.1 site × payload set, own `run_test` each; 0 exceptions, painted exactly | pass — executed (orchestrator) | arms 67 / 12 / 17 (`tester`); base RED 29/67, 5/12, 11/17 (`evidence/inc001-red-on-base.txt`, implementing agent); details payloads RED on base 8 (`inc001-details-red-on-base.txt`) |
| LLR-401.1 | test (unit) | TC-401, TC-402, TC-403, TC-404 | 0 non-exempt unsafe sinks; 7 exemptions each one live site; planted forms flagged; population ≥ 140, 11 kinds | pass — executed (orchestrator) | base RED: 45 sinks + 15 parsers listed (`inc001-red-census-base.txt`); census mutants C1–C6 KILLED (`inc001-mutations.txt`, `inc001-mutations-r3.txt`, implementing agent) |
| LLR-401.2 | test (unit) | TC-405, TC-412 | 0 `markup=False` messages holding `escape`; sync-failure toast paints `Team sync failed: <payload>` | pass — executed (orchestrator) | TC-412 base RED 2/3 arms (`inc001-red-on-base.txt`); M3, M7, M11, M12 KILLED. TC-412 is declared fault injection (D-407) |
| LLR-401.3 | test (unit) | TC-406, TC-415, TC-417, `test_details_markup.py` | 0 parser calls over a non-literal; painted styles = base flags; board markup byte-identical; `====` no longer raises | pass — executed (orchestrator) | TC-406 base RED (`inc001-red-census-base.txt`); TC-415 42/51 arms KILLED + 9 declared CSS pins each with a KILLED CSS-off sibling (`inc001-style-mutations.txt`, `tester`); base flags `inc001-style-base-r2.txt` |
| HLR-402 | test | AT-404, AT-405 + `tests/test_control_bytes.py` | 0 control bytes in model, saved file, paint (ESC/C1), pushed file, second TeamState and app; clean file byte-identical | pass — executed (orchestrator) | pre-fix RED: 281 failed / 29 pins passed (`inc002-red-prefix.txt`, implementing agent; the pre-fix tree is the increment-001 tree — the doors were untouched there, P-3/P-4 show the same keep on `56a1b10`) |
| LLR-402.1 | test (unit) | TC-407 ×257, TC-414 | 256 code points kept exactly per class; CR-LF→LF, lone CR removed; clipboard `"a\r\nb\rc"` → `"a\nbc"` | pass — executed (orchestrator) | N1–N3, N5, N6, R7, R8 KILLED (`inc002-mutations-r2.txt`, `-r4.txt`); N4 equivalent, its dead code deleted (A-5) |
| LLR-402.2 | test (unit) | TC-408 ×2, TC-410 ×2 | every planted string clean on load (set size asserted); clean saved file byte-identical; control-only phase → defaults; `""` / int → `Untitled` / `None` | pass — executed (orchestrator) | N7, N10, N12, R3 KILLED; fixture vacuity caught and fixed before the fix landed (`increment-002.md` §Instrument RED-proof) |
| LLR-402.3 | test (unit) | TC-409 ×2, TC-419 | 0 control bytes in `foreign_tasks()`, `member_names()`, applied board, Setup's republished `team.json`; deep file refused visibly | pass — executed (orchestrator) | N8, N23, R2, R4 KILLED; TC-409/TC-419 RED on r1 (`inc002-red-r2.txt`) |
| HLR-403 | test | AT-406 + TC-411 + TC-420 + TC-421 + `test_details_markup.py` | five labels painted in order at 140×40 and 80×24; 89-char name wraps at the value column (2 rows at both sizes, amendment A-7); five visible at 80×24 | pass — executed (orchestrator) | base RED 17 owed to the rule (`inc003-red-on-base.txt`); visibility clause RED at 80×12 (`inc003-f1-red.txt`); increment 004: 5 RED on increment 003's stylesheet (`inc004-red-on-inc003.txt`) |
| LLR-403.1 | test (unit) | TC-411 ×6, TC-420 ×2, TC-421 ×2 | every details grid cell ≥ 1 row on its label's row; long cell 2 rows at both sizes (amendment A-7); 1 blank row above the title and 1 below, the `ProjectModal` title 2 under its border; values 11 cells right of labels, `ProjectModal` 21; `ProjectModal` / `ClockModal` 2/3 pins | pass — executed (orchestrator) | G1, G2, G3 KILLED (`inc003-mutations.txt`); increment 004 U1, U2, U4–U7 KILLED, U3 equivalent (`inc004-mutations-r2.txt`); the two edit-modal pins GREEN on base by design (pins) |
| HLR-404 | test | AT-407 + `tests/test_sync_fields.py` | hostile `team.json`: no action, `on_track` painted, name/due kept, one line per id, all views + pickers render | pass — executed (orchestrator) | pre-fix RED 47/48 (`inc002-at407-red-prefix.txt`, `tester`); base `56a1b10` RED 21/22 incl. the `app.view('gantt')` click arm (run by `qa-reviewer`, see G-002) |
| LLR-404.1 | test (unit) | TC-413 (36 matrix + absent + new/dup + 6 colours + 3 empty ids + ticks), TC-418 | applied = `from_dict` value / previous on refusal / previous when absent; first entry per id; empty id refused | pass — executed (orchestrator) | N9, N11, N13–N17, R1, R5, R6 KILLED (R5/R6 after the r4 fixture fix, `inc002-mutations-r4.txt`) |
| LLR-404.2 | test (unit) | TC-416 | ids `a`, `b` (first `a`); names `a`, `Bo`; hues `mut` for `[]`/`evil`; Setup staged = `clean_roster`; people/standup/setup/identity picker render | pass — executed (orchestrator) | N18–N22 KILLED (`inc002-mutations-r2.txt`) |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a verification nobody ran. Write your own rows in the table above.

```text
| *(example)* HLR-001 | test | `pytest … -k TC-001` | exit 0 | | |
| *(example)* LLR-001.1 | test (unit) | `…` | `…` | | |
```

### Layer B — behavioral (black-box) acceptance

C-18 check (`qa-reviewer`, `pytest --collect-only` on the final tree, no execution): each of AT-401..AT-407 collects as **exactly one** node — `tests/test_markup_sites.py::test_AT_401_board_text_is_painted_exactly`, `::test_AT_402_synced_text_is_painted_exactly`, `::test_AT_403_typed_and_os_text_is_painted_exactly`, `::test_AT_407_a_shared_config_cannot_act_or_crash`; `tests/test_control_bytes.py::test_AT_404_a_dirty_board_opens_clean_and_saves_clean`, `::test_AT_405_what_the_app_pushes_reaches_a_teammate_clean`; `tests/test_details_grid.py::test_AT_406_the_details_view_shows_its_five_fields`. None is parametrised; each runs its arms inside the one node (one `run_test` per arm, failures collected).

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-401 | AT-401 | `TaskboardApp` via `run_test(notifications=True)`, shipped keys `d x T P b e f S enter i` and typed notes | painted dialogs, picker lines, selects, standup, details/image viewer, image-block branches, editor preview (compositor strips cropped to the widget) and toasts (`str(toast.render())`) | repr: the three-payload set at 23 board-text sites (67 arms) · boundary: `a[B]x.png` / `bad[B].png` image branches, highlight around a payload · negative: base RED 29/67 | executed — pass (orchestrator gate run) |
| US-401 | AT-402 | team mode over a shared dir on disk; identity picker at mount, `e`, `P` | identity picker line, editor project/phase selects, project-picker line | repr: synced roster name, project and phase × payloads (12 arms) · boundary: the picker line built from pieces · negative: base RED 5/12 | executed — pass (orchestrator gate run) |
| US-401 | AT-403 | Setup `0` + `tab` + `a` + typed id twice; phase editor `a`/`e`; `R`; unreadable board at mount; `]` with `history.jsonl` a directory | duplicate-id / duplicate-name toasts, report and recovery toasts compared whole with `str(path)`, transition-log toast vs the OS error text | repr: typed ids and names × payloads · boundary: dirs `a[B]x` and `[B]x`, lowercased Setup id · negative: base RED 11/17 | executed — pass (orchestrator gate run) |
| US-402 | AT-404 | a dirty `board.json` on disk opened by the app; `enter`, `escape`, `]` | painted `#details-box` (no ESC / C1, printable remnant `Wri[31mte thespec` kept); the saved `board.json` parsed (0 control bytes, phase moved to `Review`) | repr: ESC, C1, BEL, OSC in title, notes, project, phase · boundary: BEL dropped by Rich so asserted at the file (Q-5); tab/newline/NBSP kept is white-box (TC-407, TC-410) · negative: pre-fix RED | executed — pass (orchestrator gate run) |
| US-402 | AT-405 | app A in team mode over a dirty board (startup sync pushes); second `TeamState`; app B as `ana`, key `9` | pushed `board.me.json` parsed (0 control bytes); `foreign_tasks()` title `Ship[5m it now`; app B's painted people view (no ESC/C1/BEL, title shown) | repr: the C-12 output-then-consume chain · boundary: printable remnant `[5m` kept · negative: pre-fix RED (and RED under a reverted load door alone, Q2-4) | executed — pass (orchestrator gate run) |
| US-403 | AT-406 | `enter` on a high-priority task at 140×40 and 80×24 | `#details-box` painted rows: five labels and values on one row, in order; 89-char name rebuilt from wrapped rows, continuations at the value column; five visible at 80×24 | repr: 140×40 · boundary: 80×24 long name, no dates `—`, `Doing · blocked`, Inbox · negative: base RED (no label painted); visibility clause RED at 80×12 | executed — pass (orchestrator gate run) |
| US-404 | AT-407 | team mode over a hostile `team.json`; startup sync as `a` and with no identity; `P`, a mouse click per painted status cell, keys `1..5 7 8 9 0` | picker lines (`Alpha  ·  on_track`, one `Untitled  ·  on_track` for `n1`, no `Second`), the view after each click (`swimlanes`), board p1 name/due kept, identity picker ids once, eight views + Setup alive | repr: action tag, `[]` colour, int name/due, duplicate ids, hostile roster · boundary (d): valid `paused`/`sky` applied, `null` due clears · negative: pre-fix RED 47/48 (`tester`); base RED 21/22 (`qa-reviewer`) | executed — pass (orchestrator gate run) |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | board file on disk (titles, notes, URLs, images, project/phase names, settings) | `Board.load` → `clean_strings` | yes — the app opens the file | AT-401, AT-404, AT-406 (TC-408, TC-410 white-box) | ✓ |
| input | shared dir `team.json` (projects, roster, phases) | `team_sync._read_json`; `apply_config_to_board`; `clean_roster`; Setup's read | yes — startup sync and Setup | AT-402, AT-407 (TC-409, TC-413, TC-416, TC-418, TC-419) | ✓ |
| input | shared dir teammate file `board.<user>.json` | `_read_json` → `foreign_tasks()` | yes — app B reads what app A pushed | AT-405, AT-402 (TC-409) | ✓ |
| input | typed input (Setup ids, phase names, notes keystrokes) | Setup handlers, `PhaseEditor`, `TaskModal` / `notes_preview` | yes — keys typed through the pilot | AT-403, AT-401 (editor preview arm) | ✓ |
| input | clipboard text (Ctrl+V) | `grab_clipboard_text` → `_clean_clipboard_text` | yes, by `qa-reviewer`'s P4 probe only (dirty OS clipboard through the shipped Ctrl+V of `TaskModal`): final tree 0 control bytes in `#f-title` and `#f-notes`, tab/LF/NBSP kept; base export keeps CR in the Input. No suite node: the existing Ctrl+V nodes patch `modals.grab_clipboard_text`, bypassing the cleaner | TC-414 (white-box only) | gap — G-001 (minor) |
| input | OS paths and OS error text | `action_report`, `_warn_if_rescued`, `_warn_history_error` | yes — real dirs `a[B]x`, `[B]x`, a real failing write | AT-403 | ✓ |
| input | exception text from team sync | `_team_sync_tick` | no black-box input reaches it (the sync path swallows its errors, Q-3) — declared fault injection | TC-412 | ✓ declared (D-407) |
| output | painted dialogs, confirms, prompts | `ConfirmModal`, `TextPrompt`, `PhaseEditor`, `StandupModal`, `ImageViewer` | yes — compositor strips | AT-401, AT-403 | ✓ |
| output | painted pickers (project, blocker, identity) and selects | `ProjectPicker._project_line`, `BlockerPicker`, `TeamIdentityPicker`, `TaskModal` selects | yes | AT-401, AT-402, AT-407 | ✓ |
| output | painted toasts | `notify(..., markup=False)` sites | yes — painted `Toast` | AT-401, AT-403 (TC-412) | ✓ |
| output | painted details info grid | `TaskDetails` + `#details-box .modal-grid Label` rule | yes | AT-406 (TC-411) | ✓ |
| output | saved board file | `Board.save` | yes — parsed after `]` | AT-404 (TC-410) | ✓ |
| output | pushed teammate file | `TeamState.push` at startup sync | yes — re-read and fed to a second app | AT-405 | ✓ |
| output | republished `team.json` | Setup save | yes at the file; the save is invoked as `app.action_setup_save()` after entering Setup by key `0`, not by its key binding | TC-409, TC-418 | ✓ (white-box drive of the save action; noted) |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 1855 | 0 (1 renamed in increment 004) | 359 + 4 | 2218 | 2218 | n/a — the project marks no `slow` tests; one full run / 2214 passed at P4, 2218 at the increment-004 gate (`inc004-gate-r3.txt`) | yes |

- Base: `56a1b10`, 1854 passed + 1 failed (clipboard environment, G-011) = 1855 (`evidence/base-suite.txt`).
- Additions by increment: 001 +34 (census 6, sites 5, tokeniser 9, details payload arms 14); 002 +318 (`test_control_bytes.py` 267, `test_sync_fields.py` 50, AT-407 1); 003 +7 (TC-411 ×6, AT-406). 34 + 318 + 7 = 359. Increment 004 (after the re-open): +4 (TC-420 ×2, TC-421 ×2), and TC-411's long arm renamed `[size1-3]` → `[size1-2]` → 2218.
- Checked by `qa-reviewer` from node ids, not from counts: `--collect-only` on a `git archive 56a1b10` export (1855 ids) vs the final tree (2214 ids): **0 removed**, 359 added (by file: control_bytes 267, sync_fields 50, highlight_segments 9, markup_census 6, markup_sites 6, details_markup 14, details_grid 7). The in-place rewrites (`test_app.py` ×2, `test_archive.py` ×1, `test_prism_laws.py` exemption, `test_edit_window.py` docstring, `test_details_markup.py` project/phase arms) kept their node ids.

### Supersession inspection (read off the P3 packets, re-run on the final tree)

| Superseded marker (packet) | grep on the final tree (`qa-reviewer`) | All surviving refs negative? |
|---|---|---|
| `_rich(` in product code (inc 001) | `grep -n "_rich(" taskboard/*.py` → 0 | yes — test mentions are docstrings only (`test_markup_sites.py:9, 229, 244`) |
| `escape(` in `modals.py` / `app.py` (inc 001) | 0 | yes |
| bare `json.loads` / `import json` in `app.py` (inc 002, Setup's `team.json` read) | 0 | yes |
| raw `setattr` of synced fields (inc 002) | 1 hit, `team_sync.py:288` | yes — it sets `getattr(fresh, key)` where `fresh = Project.from_dict(pd)`, after the input-refusal guards |
| tests pinning the old escaping (A-7: `test_archive.py:557-577`, `test_app.py:300-313`, `test_app.py:2052-2059`) | rewritten in place (inc 001 §Reverse census) | yes — green in the gate run |
| `test_details_markup.py` project/phase arms via `w.render()` (inc 003) | rewritten to read the painted screen | yes — green in the gate run |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | HLR-402 / LLR-402.1 | The clipboard input has no suite node through the handler: TC-414 calls `_clean_clipboard_text` directly, and the existing Ctrl+V nodes (`test_app.py:1028-1070`) patch `modals.grab_clipboard_text`, which bypasses the cleaner. Observed at P4 only by `qa-reviewer`'s probe (final tree clean; base keeps CR in the Input). | minor | BACKLOG: add a Ctrl+V node that patches `models._win_clipboard_text` with dirty text and asserts the Input and TextArea values (the probe's shape). |
| G-002 | HLR-404 (threshold clause, UX3-2) | "The base RED of the `app.view('gantt')` click is recorded at P3": no P3 packet or evidence file records it — AT-407's pre-fix run used the increment-001 tree, where the picker line was already built from pieces. `qa-reviewer` ran AT-407 on a `56a1b10` export at P4: 21 of 22 arms RED; the status alone painted `X` (markup consumed) and the click on its cell raised `InvalidSelectValueError` — a crash, not a fired action (the fired action on base is recorded with `app.pwn`, P-12). Transcript at the qa scratchpad (`at407-base.txt`, sha256 `720dc816…3dea3`), not at the evidence home. | minor (evidence) | Orchestrator copies the transcript under `evidence/` (or re-runs) before close; the clause is then met as "RED by crash", not "RED by action". |
| G-003 | HLR-403 (D-406) | PV-1 (one row per field, values wrap), UX-3 (gap under the title) and UX-4 (narrower label column) are provisional visual decisions; the operator's verdict on the captures is owed before the coordinator pushes (`PLAN.md` standing authorization). | minor (operator) — **closed 2026-10-04**: PV-1 accepted, UX-3 and UX-4 applied in increment 004 (`evidence/operator-verdict-provisional.json`) | Operator verdict on `evidence/captures/` at close. |
| G-004 | LLR-401.1 | Census residuals: H1 (six name-shadowing shapes fool the `-> Text` trust), H2, the round-1 residuals (module-attribute widget, `super().__init__` content, `getattr(Text, "from_markup")`), F5 test names. The package uses none today. Not yet in `.dev-flow/BACKLOG.md` (grep: 0 hits). | minor | Route to BACKLOG at P5 close, as the packets state. |
| G-005 | HLR-402 / HLR-404 | Security S4-2, S4-3, S4-4, S5-1 (LOW); D-409 legacy `history.jsonl`; D-414 phase-list bounds; `Task.from_dict` synced dates untyped; UX-8 dim value tone. Not yet in BACKLOG (grep: 0 hits). | minor | Route to BACKLOG at P5 close. |
| G-006 | LLR-401.3 (D-415) | The escaped empty-highlight crash (`====`): the pre-fix RED on file is a shape RED (`highlight_segments` import absent, `inc001-red-census-base.txt`); the base `TypeError` is shown by the frozen base copy inside TC-417 (`_base_renders` excludes it), not by a run of a shipped renderer on `56a1b10`. The post-fix arm is value-discriminating. | minor | Accept; optionally capture a base run of a board view over a `====` note at close. |
| G-007 | trigger D | UX walkthrough rows owed by `ux-reviewer` (running in parallel). | pending | Orchestrator fills §UX walkthrough from the `ux-reviewer` result. |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| AT-401, AT-402, AT-403 (S1, S-5) | `evidence/inc001-red-on-base.txt` (implementing agent, base export) | value (`MarkupError`, altered or vanished payload) | yes — painted text compared exactly | executed — pass (orchestrator) | the three `test_markup_sites.py` AT nodes |
| AT-404, AT-405 (S2, L1) | `evidence/inc002-red-prefix.txt` (implementing agent, increment-001 tree) | value (control bytes painted, saved, pushed) | yes — control-byte set and printable remnant | executed — pass (orchestrator) | the two `test_control_bytes.py` AT nodes |
| AT-406 (details grid blank) | `evidence/inc003-red-on-base.txt` (implementing agent, base export) | value (labels not painted, 0-row cells) | yes — label/value text per row | executed — pass (orchestrator) | `test_details_grid.py::test_AT_406_…` |
| AT-407 (S-1 HIGH, S-3) | `evidence/inc002-at407-red-prefix.txt` (`tester`, increment-001 tree, 47/48); base `56a1b10` 21/22 (`qa-reviewer`, G-002) | value and crash | yes — painted line, view after click, board fields | executed — pass (orchestrator) | `test_markup_sites.py::test_AT_407_…` |
| TC-417 `====` arm (D-415) | `evidence/inc001-red-census-base.txt` (implementing agent) | shape (import absent) — see G-006 | yes | executed — pass (orchestrator) | `test_highlight_segments.py::test_TC_417_segments_drop_markers_and_keep_text[====-segments6]` |
| TC-413 empty-id arms (F1 HIGH, P3) | `evidence/inc002-red-r2.txt` (implementing agent, r1 tree) | value (board grew per tick) | yes — board size asserted | executed — pass (orchestrator) | `test_sync_fields.py::test_TC_413_an_empty_synced_id_never_grows_the_board[×3]`, `…sync_ticks_and_the_startup_save_keep_the_board_size` |

### Checks run by `qa-reviewer` (read-only toward the repo; none is a gate run)

| Check | Command / instrument | Result |
|---|---|---|
| gate-run file identity | `sha256sum evidence/p4-gate.txt` | `cb68cdef…0680`, equal to `increment-003.md` |
| tree identity | `sha256sum -c` of `inc003-frozen-r2`, `inc002-frozen-r4`, `inc001-frozen-r3` | 3/3 OK, 6/6 OK, 8/11 OK (the 3 mismatches are files later re-pinned by r4/r2) |
| C-18 | `python -m pytest --collect-only -q -p no:cacheprovider` | each AT-401..407 exactly one node; 2214 collected (2218 after increment 004, the ATs unchanged) |
| ledger by node id | collect-only on a `git archive 56a1b10` export vs the final tree | 1855 → 2214, 0 removed, 359 added; increment 004: 2214 → 2218, 1 renamed, 4 added |
| supersession | the greps of §Supersession | all surviving refs negative |
| G-001 clipboard probe | scratch `probe_clip.py` (sha256 `005b107d…7340`): `models._win_clipboard_text` returns `"Ti\x1b[31mtle\x07\x9b x\r\ny\tz\x7f e"`; `a`, focus, Ctrl+V into `#f-title` and `#f-notes` | final tree: both `'Ti[31mtle x\ny\tz\xa0e'`, 0 control bytes; base export: Input keeps `\r` (`0xd`) |
| G-002 base RED | `pytest -B -q -p no:cacheprovider -rA tests/test_markup_sites.py -k AT_407` on a `56a1b10` export with the final test file overlaid | `1 failed` — 21 of 22 arms RED (scratch `at407-base.txt`, sha256 `720dc816…3dea3`) |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- [✓] Acceptance criteria use Given/When/Then — in substance: each AT's docstring and §5 row state the given state (a board file / shared dir holding X), the action (keys) and the observable outcome (`test_control_bytes.py:241-249`, `test_markup_sites.py:988-1027`); the contract's §3 uses outcome/surface/threshold rather than literal G/W/T keywords.
- [✓] Test cases have explicit Expected, not vague "works" — every HLR/LLR carries a numeric pass threshold (`01-requirements.md` §3–§4); every Layer A row above repeats it.
- [✓] Edge cases include empty, boundary, invalid, error — boundary catalogs per HLR/LLR (QC-3), each unticked kind marked N/A; error: TC-412, AT-403 transition-log toast, TC-419.
- [✓] Regression checklist exists — the full suite (2214, 0 removed by node id; 2218 after increment 004) plus each packet's reverse census (B1 hits rewritten in place or re-validated).
- [✓] Exit criteria stated — `01-requirements.md` §5.2 (every HLR an AT, every LLR a TC, RED or mutation per assertion, census clean, 0 failures but the declared flake): met — `p4-gate.txt` 0 failures.
- [✓] No real PII / secrets — fixtures only (users `a`, `b`, `me`, `ana`; projects `Alpha`, `Ops`); evidence paths redacted to `<home>` / `<user>`.
- [✓] Mode declared at the top of the artifact — `validation` (§Mode line).
- [✓] Validation mode: every case carries a result or one of the seven states, and each executed result names its executor — Layer 0/A/B rows name the orchestrator, implementing agent, `tester` or `qa-reviewer`; the UX rows read `pending — ux-reviewer` for the orchestrator to fill.
- [✓] Layer B (black-box): every output-producing story observed through the shipped surface with boundary + negative evidence — §Layer B, 7 ATs over 4 stories, C-18 checked by collection.
- [✓] Bidirectional surface-reachability — every named input and output reached/observed at the handler (§matrix); the clipboard was observed only by the P4 probe and is G-001; the sync-failure toast is declared fault injection (D-407).
- [✓] No unfilled template — no `<...>` placeholder left; the UX subsection, first left `pending — ux-reviewer` by instruction, not a placeholder.

### Orchestrator fold (2026-10-03)

- The UX walkthrough rows above are filled from `ux-reviewer`'s record (`evidence/p4-ux-walkthrough.txt`, PASS-WITH-NOTES, 17/17 PASS), executed by `ux-reviewer` (G-007 discharged).
- G-002 discharged: `qa-reviewer`'s base run of AT-407 is now stored at `evidence/p4-at407-base.txt` (sha256 `e643b3ad…`): the gantt click on base crashed (`InvalidSelectValueError`) rather than firing — the action itself was shown firing on base by P-12 (`evidence/p1-sync-fields-probe.txt`, `app.pwn`).
- G-001, G-004, G-005 land in `BACKLOG.md` at P5; G-003 (PV-1, UX-3, UX-4) went to the operator, who accepted PV-1 and applied UX-3 and UX-4 on 2026-10-04 (increment 004); G-006 is declared (TC-417 embeds the base function as its oracle).

### Increment 004 re-validation (light P4, 2026-10-04 — amendment A-7, D-422)

The operator's verdict (`evidence/operator-verdict-provisional.json`): PV-1 accepted, UX-3 and UX-4 applied. The batch
re-opened to P3; increment 004 (`03-increments/increment-004.md`) added one scoped stylesheet block.

| Req | Validation | Verification | Threshold (amendment A-7) | Result | RED / mutation |
|---|---|---|---|---|---|
| HLR-403 | test | AT-406 + TC-411 + TC-420 + TC-421 + `test_details_markup.py` | five labels painted in order at 140×40 and 80×24, values 11 cells right of labels (x 34 / 16, measured in `inc004-probe.txt`); 89-char name over 2 rows at both sizes; five visible at 80×24 | pass — executed (orchestrator, `inc004-gate-r3.txt`: 2218 passed, exit 0); details files 54 passed — executed (qa-reviewer, frozen r3) | `inc004-red-on-inc003.txt` 5 RED |
| LLR-403.1 | test (unit) | TC-411 ×6, TC-420 ×2, TC-421 ×2 | cells ≥ 1 row; long cell 2 / 2 rows; 1 blank row above the title, 1 below; the `ProjectModal` title 2 rows under its border; label→value offset 11 ×5; `ProjectModal` 21; `ProjectModal` / `ClockModal` 2/3 pins | pass — executed (qa-reviewer, the `-k` command, 10 passed on frozen r3; orchestrator, gate r3; frozen r4 details files 91 passed, `inc004-details-r4.txt`) | r2 battery 6 of 7 KILLED, U3 equivalent (`inc004-mutations-r2.txt`) |

| AT | Story | Result |
|---|---|---|
| AT-406 (re-run, unchanged) | US-403 | executed — pass at the amendment-A-7 geometry (gate r3) |

- **qa-reviewer (light P4): PASS-WITH-NOTES**, conditional on the r3 gate, which then landed at 2218 passed, exit 0.
  - **N1:** declare the ledger by node id. Done: 2214 − 1 + 5 = 2218, the packet's ledger.
  - **N2:** x 34 / 16 is measured only by the probe. HLR-403 cites `inc004-probe.txt`; TC-421 asserts the offset.
  - **N3:** the packet lagged revision 2. Updated.
  - **N4:** amendment A-7 lacked its Before/After. Added in §6.5.
  - **N5:** "A-7" had two meanings. Written as "amendment A-7".
  - **N6:** P-14 is a P1 premise, kept as history; the current threshold is amendment A-7.
- **ux-reviewer walkthrough: PASS**, through `App.run_test` with `enter` at 140×40 and 80×24, short and long name.
  - One blank row above the title and one below; box heights unchanged (23 / 24 at 140×40, 21 at 80×24); values at x 34 / 16.
  - The long name over 2 rows, painted whole; the five fields inside the box; `Priority` fits (8 of 10).
  - `ProjectModal` paints as before the batch.
  - Notices, all pre-existing or intended: the 80×24 details still scrolls, the `ProjectModal` `Due` sits below the fold at 80×24, and the details title's gap now differs from the edit modals' by the operator's choice.
- **Captures:** `evidence/captures/after2-details-{140x40,80x24}[-long].{svg,txt}`.
- **Test ledger (increment 004):** by node id 2214 − 1 + 5 = 2218 (TC-411's long arm `[size1-3]` → `[size1-2]`, TC-420 ×2, TC-421 ×2). Gate run: 2218 passed in 398.62 s, exit 0, run by the orchestrator (`inc004-gate-r3.txt`).
