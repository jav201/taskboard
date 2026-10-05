# Validation — taskboard — Batch 2026-10-04-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1 and **names who executed each one**. The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Mode: validation.** Every case below carries a result or one of the seven evidence states, and every executed result names who executed it. Executors in this record are:
> - **the orchestrator**: the ONE complete gate-suite run (`evidence/inc004-gate-r3.txt`) and the close captures (`evidence/captures/close-*`).
> - **`software-dev`** (per its packets): the RED counterfactuals and the mutation batteries.
> - **`qa-reviewer`** (me): a targeted run of the batch's nodes, the freeze check, the node inventory, inspection of the captures, and an isolated re-run of the one failed node.

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

- **Result:** PASS-WITH-NOTES — 0 blocker gaps. Four minor gaps (G-001..G-004) and one environment failure (G-005) are explained in §Gaps detected. No route to `iterate-to-fix` or `iterate-to-refine`.
- **Layer 0:** 20 units met the criterion (cyclomatic ≥ 3 or crossing the board-file boundary) · 20 carry a named reddening mutation (KILLED in the battery transcripts cited in §Layer 0)
- **Requirements:** 17/17 pass (5 HLR + 12 LLR) · 0 blocker fails. The one failed node in the increment-004 gate run is outside every requirement (G-005, environment). On the final product (increment 007 frozen r1) the gate has 0 failures; see §Increment 006 re-validation and §Increment 007 re-validation.
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (`TaskboardApp` driven with real keys via `run_test`; saved board file, backup and log re-read from disk), with boundary and negative arms. Two notes: preconditions select the task with a direct setter (G-001), and the `═` over tone is observed only in the close capture, not by a node (G-002).
- **Surface-reachability (bidirectional):** ✓ every named input and every named output/deliverable is reached or observed at the surface (matrix below). The single partial is the `═` tone (G-002).
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative. `BlockerPicker` appears 0 times in `taskboard/` (TC-508, and my grep); `b` = `action_toggle_blocked` flips the flag only (`app.py:815-825`, TC-506, AT-501); `⛓` is painted nowhere (it survives in one docstring, `views.py:353`, and 0 times in `README.md`).
- **Test ledger:** ✓ reconciles on the final product: 2306 = 2218 − 2 + 90, matching the 2306 nodes the orchestrator's increment-006 gate run collected (2306 passed, 0 failed, `evidence/inc006-gate-r2.txt`); increment 007 keeps it at 2306 = 2306 − 1 + 1 (2306 passed, 0 failed, `evidence/inc007-gate-r1.txt`). At the first P4 it was 2295 = 2218 − 2 + 79 (2294 passed, 1 failed)
- **Evidence checklist (qa-reviewer):** qa-reviewer · 11 of 11 rows ✓ with evidence

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### What was executed, by whom, on which tree

| Run | Executor | Tree | Command | Output | State |
|---|---|---|---|---|---|
| Base suite | orchestrator (P1, P-12) | `0447070` | `python -m pytest -q` | `evidence/base-suite.txt`: 2218 passed in 339.95 s, exit 0 | `executed` |
| **The ONE complete gate run** (C-25) | **orchestrator** | frozen r3 = the product at close | `python -m pytest -q -p no:cacheprovider` | `evidence/inc004-gate-r3.txt`: **1 failed, 2294 passed in 576.52 s**. The failure is `tests/test_app.py::test_win_clipboard_roundtrip`, with SETUP message "SETUP failed — this is the environment…" (`Set-Clipboard` `ExternalException`) | `executed` |
| Freeze check: is the tree on disk the gated tree? | qa-reviewer | working tree | `sha256sum -c` over `inc001-frozen-r4`, `inc002-frozen-r2`, `inc003-frozen-r2`, `inc004-frozen-r3` | Every changed file matches its **latest** freeze: `views.py`, `modals.py`, `app.py` and `test_gantt_link.py` / `test_markup_census.py` match r3; `models.py`, `keymap.py`, `README.md` and the 003 tests match 003-r2; the 002 tests match 002-r2; `kg_board.py` and `test_app.py` match 001-r4. Mismatches against earlier freezes belong only to files a later increment re-froze | `executed` |
| Targeted run of the batch's nodes plus README/keymap/census/S1 | **qa-reviewer** | same tree | `python -B -m pytest -q -p no:cacheprovider -rA tests/test_gantt_link.py tests/test_links.py tests/test_link_picker.py tests/test_details_links.py tests/test_link_migration.py tests/test_readme.py tests/test_keymap.py tests/test_markup_census.py tests/test_markup_sites.py` | **124 passed in 153.15 s**, 0 failed | `executed` |
| Node inventory | qa-reviewer | same tree | `--collect-only` over the five new files | 79 nodes; each of AT-501..508 and TC-501..518 resolves to ≥ 1 collected node (AT-503 → 2 nodes, TC-515 → 16) | `executed` |
| Isolated re-run of the failed node | qa-reviewer | same tree | `pytest tests/test_app.py::test_win_clipboard_roundtrip` and a bare `powershell Set-Clipboard -Value 'qa probe'` | Both failed with `Requested Clipboard operation did not succeed`. The bare shell call fails outside pytest, so the environment refuses the clipboard. Both were write attempts on the machine clipboard and both failed, so nothing was written | `executed` (`failed`, environment) |
| RED counterfactuals, mutation batteries | software-dev (per packets 001–004) | each increment's frozen revision, in a scratch export | `evidence/battery.py` + `mutants_inc00N*.json` | See §Layer 0. I re-counted the verdicts in the transcripts (`grep -c KILLED/SURVIVED/BAD`) | `executed` (consumed, not re-run by me) |

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `migrate_links` (`models.py`) | cc ≥ 3 | TC-514 ×4 | pass (gate, orchestrator; targeted, qa-reviewer) |
| `run_link_migration` | boundary: writes the board file, backup and log | TC-515 ×16 | pass |
| `_create_beside` | boundary: exclusive create beside the board file | TC-515 (names taken, dangling symlink) | pass |
| `Board.save_atomic` | boundary: temp file + `os.replace` | TC-515 (failure arms, leftover temp, symlinked board) | pass |
| `links_marked` | cc ≥ 3 (dict / list / str / `{"links": 0}`) | TC-515 (5 parametrized marks) | pass |
| `TaskboardApp._migrate_links` + multi-task `action_undo` | cc ≥ 3; boundary (on_mount ordering vs the first save) | TC-516, AT-506 | pass |
| `open_predecessors` / `open_dependents` / `link_marks` | cc ≥ 3 | TC-501 ×2, TC-502 ×2 | pass |
| `link_overlap` (the one measure) | cc ≥ 3 | TC-503 ×8 | pass |
| `loop_path` | cc ≥ 3 | TC-501, TC-518 | pass |
| `waiting_ids` / `ready_messages` | cc ≥ 3 | TC-506 ×3 | pass |
| `archive_refusal` and the app guards | cc ≥ 3 | TC-517 ×5, AT-505 | pass |
| `_link_tokens` / `card_cell` / `_card_meta` | cc ≥ 3 (shed order) | TC-504 ×3 | pass |
| `gantt_dep_mark` / `_flowing` | cc ≥ 3 | TC-505 | pass |
| `link_refusal` | cc ≥ 3 | TC-507 ×2 | pass |
| `link_candidates` / `loopers_of` | cc ≥ 3 | TC-509 ×3 | pass |
| `link_hint` | cc ≥ 3 (six timing forms) | TC-509 ×3 | pass |
| `project_archive_refusal` | cc ≥ 3 | TC-517, AT-505 (project arm) | pass |
| `gantt_link_overlay` | cc ≥ 3 | TC-511 ×6 | pass |
| `gantt_link_order` / `GanttLinkMode` cycle and filter | cc ≥ 3 | TC-512 ×4 | pass |
| `gantt_link_frame` status rows (cell clipping) | cc ≥ 3 | TC-512 (80 columns, wide titles, long filter) | pass |

**Measured by mutation, never by line coverage.** For each unit, the named mutation (ids as in the spec files) and the transcript that shows it RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `migrate_links` | M1 released links kept · M2 D-515 broken · M3 no loop check · M18 repeated id migrated · M19 walk back stops early · M21 walk on every link | yes — KILLED | `evidence/inc001-mutations-r4.txt` (22 KILLED, 0 SURVIVED) |
| `run_link_migration` | M6 no rollback · M8 malformed mark not logged · M9 team-pull-readable backup name · M17 a failed run leaves files · M20 dict mark replaced | yes — KILLED | `inc001-mutations-r4.txt` |
| `_create_beside` | M5 overwrite a taken name · M15 symlink written through | yes — KILLED | `inc001-mutations-r4.txt` (M15 SURVIVED at r1 → arm added) |
| `Board.save_atomic` | M7 save in place · M16 fixed temp name · M22 temp left on failure | yes — KILLED | `inc001-mutations-r4.txt` |
| `links_marked` | M4 loose mark | yes — KILLED | `inc001-mutations-r4.txt` |
| `_migrate_links` / undo | M11 migration after the renumber save · M12 undo one task · M13 no stop on failure | yes — KILLED | `inc001-mutations-r4.txt` |
| `open_predecessors` / `link_marks` | N1 closed predecessors counted · N2 repeated id · N16 closed waiters counted | yes — KILLED | `evidence/inc002-mutations-r2.txt` (21 KILLED) |
| `link_overlap` | N3 strict measure (`<` for `≤`) | yes — KILLED | `inc002-mutations-r2.txt` |
| `loop_path` | N4 open-only loop search | yes — KILLED | `inc002-mutations-r2.txt` |
| `waiting_ids` / `ready_messages` | N9 no cap · N10 ready while still waiting · N19 ready never said | yes — KILLED | `inc002-mutations-r2.txt` |
| `archive_refusal` + guards | N11–N13 `x`/`d`/editor unguarded · N14 the archived set's own waiters · N20 Setup `x` reaches the task · N22 delete not judged again | yes — KILLED | `inc002-mutations-r2.txt` |
| `_link_tokens` / `card_cell` | N5 teammate task paints marks · N6 marks dropped · N15 people view on the fallback · N18 `◂` shed before `▸` | yes — KILLED | `inc002-mutations-r2.txt` |
| `gantt_dep_mark` / `_flowing` | N7 archived predecessor in the gutter · N8 packet on a waiting task | yes — KILLED | `inc002-mutations-r2.txt` |
| `link_refusal` | P1 closed predecessor · P2 loops · P3 long path · P14 app skips refusal | yes — KILLED | `evidence/inc003-mutations-r2.txt` (20 KILLED + P8 anchor `BAD`, re-anchored in `inc003-mutations-r2b.txt`: KILLED) |
| `link_candidates` / `loopers_of` | P4 order · P5 done offered · P6 loop unmarked | yes — KILLED | `inc003-mutations-r2.txt` |
| `link_hint` | P7 hint off by a day | yes — KILLED | `inc003-mutations-r2.txt` |
| `project_archive_refusal` | P8 inside waiters · P9 project unguarded | yes — KILLED | `inc003-mutations-r2b.txt`, `inc003-mutations-r2.txt` |
| `gantt_link_overlay` | Q1 overlay in the label · Q2 `═` a day too many · Q3 connector over bars · Q4 `═` with no start · Q17 connector a day late | yes — KILLED | `evidence/inc004-mutations.txt` (21 KILLED), `inc004-mutations-r2.txt` |
| `gantt_link_order` / cycle | Q5 loop selectable · Q6 filter ignored · Q7 cursor start · Q24 cycle not in gantt order | yes — KILLED | `inc004-mutations-r2.txt` |
| `gantt_link_frame` status rows | Q10 keys clipped · Q22 row guard removed · Q22b clip by `len()` · Q23 filter unclipped | yes — KILLED (Q22/Q22b/Q23 SURVIVED at r2, KILLED at r3 after the test was strengthened) | `inc004-mutations-r2.txt`, `inc004-mutations-r3.txt` (3 KILLED) |

> Note on 004's "25 of 25": the 22 r2 kills were made with the r2 tests, and the 3 r3 kills with the strengthened r3 test. r3 only ADDED assertions (test-only, `code-reviewer` confirmed), and added assertions cannot turn a killed mutant back to green, so combining the two counts is sound. The 22 were not re-run on r3; I record that rather than assume it.

### UX walkthrough — only if trigger family D fired

Trigger family D fired (new and changed surfaces: card marks, picker, gantt link mode, details section, toasts). **Owned by `ux-reviewer` (walkthrough `evidence/p4-ux-walkthrough.txt`), merged by the orchestrator.** Verdict **PASS-WITH-NOTES** — no HIGH; three MED (F4, U-2, E-1), handled as below.

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| US-501: kanban `4` → `◂N`/`▸N` muted where `⛓` stood, no accent | ✓ run_test, real keys | ✓ painted strips + segment styles | pass |
| US-501: lanes `4 tab tab` → every card identifiable | ✓ | ✓ — a card with `▸1 ◂1` loses its title (U-2, MED; base had 1 such card) | ⚠ D-529 → operator at PV-1 |
| US-501: `]` twice → one "Ready" toast naming both tasks | close capture | ✓ `close-ready-*` | pass |
| US-502: `L` in kanban → picker, filter, loop row with its path | ✓ (selection set as setup) | ✓ | pass (U-3 LOW) |
| US-502: `L` in gantt → header, `⟲`, ↑/↓, no match, `═` + connector, ↵ links (file re-read), toast | ✓ | ✓ | pass |
| US-502: same at 118×20 / larger projects → the link stays visible | ✓ | the waiter's row folds, overlay gone (F4, MED) | ⚠ fixed by saying it (increment 005, A-8); the fold rule → operator at PV-5 (D-528) |
| US-503: `enter`, `tab`, `x`, `u`, `↵` → section, removal saved, undo, jump | ✓ | ✓ | pass |
| US-504: `d` on a task others wait on → refusal naming the waiter, no confirm | ✓ | ✓ | pass |
| US-505: legacy board start → migration toast with backup name and `u undo` | close capture | ✓ `close-migration-*` | pass |

**Mechanism used:** a UI test driver — Textual `run_test` with real key presses on a synthetic `kg_board`, plus the close captures.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed (`ux-reviewer`) |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed (`ux-reviewer`, against US-501..505, A-1..A-7, PV-1..PV-7) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the operator's visual verdict on the captures is owed at close |

- **Method:** cognitive walkthrough per story with real keys; the selection set as setup (no arrow navigation); before/after against the base captures.
- **Participants or population:** none — reviewer inspection only.
- **Evidence of the evaluation:** `.dev-flow/2026-10-04-batch-01/evidence/p4-ux-walkthrough.txt`; the captures under `evidence/captures/`.
- **Limits:** toast timing and severity colour, the migration's `u` and second start not driven (AT-505..508 cover them); colour read from painted segments, not SVG; the captures set the selection by property (E-2). E-1 (the lanes captures showed matrix) re-shot with `4 tab tab` at close.

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result. Every result below is `executed` in the orchestrator's gate run (`inc004-gate-r3.txt`, 2294 passed, with no requirement node among the failures) **and** in qa-reviewer's targeted run (124 passed).

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-501 | test (B) | `pytest tests/test_links.py -k AT_501` | `◂` 7/8 grouped, 8/8 lanes; `▸` 8/8; muted tone; 0 `⛓`; `b` 0 screens and `depends_on` byte-equal; one ready toast; 0 on a further `]` | pass | AT-501; tone read from compositor segments (`_mark_tones == {HEX["mut"]}`); close capture `close-ready-118x30.txt` shows the toast "Add push notifications is ready — Audit dependencies done" |
| HLR-502 | test (B) | `pytest tests/test_link_picker.py tests/test_gantt_link.py` | picker order/filter/loop/↵/unlink/`u`/create; gantt header "24 candidates · ⟲1 would loop", cycle skips the loop, `═` on overlap days, 0 label cells, ↵ links, esc no-op | pass (the `═` tone clause by inspection only, G-002) | AT-502, AT-503 ×2, TC-510 ×2, TC-512 ×4 (app-driven); `close-gantt-link-*.svg`: `═` fill `#f43f5e` = `HEX["over"]` (`views.py:57`) |
| HLR-503 | test (B) | `pytest tests/test_details_links.py` | section rows, "▸1 direct · 2 in chain", conflict "overlaps … by 2d", `x` both directions (board + file), `↵` jump, `L` repaint, S1 | pass | AT-504; TC-513 (app-driven, `enter`) asserts the conflict line `◂ starts Oct 1, overlaps Audit dependencies by 2d (due Oct 2)` |
| HLR-504 | test (B) | `pytest tests/test_links.py -k AT_505` | `x`/`d`/editor box refused, file bytes unchanged, 0 confirms, toast names the waiter; project archive refused; done predecessor archives; `X` unchanged | pass | AT-505; `close-guard-80x24.txt` shows "can't archive Partner notice emails — 1 open task waits on it (Deprecate v1 endpoints)…" |
| HLR-505 | test (B) | `pytest tests/test_link_migration.py` | backup bytes == pre-start bytes; rule result per shape; log = changed set; 1 toast; `u` reverts with mark kept; 2nd start byte-identical; no-change board marked only; backup failure leaves file byte-identical, unmarked, exit with no dir path | pass | AT-506, AT-507, AT-508; `close-migration-80x24.txt` shows "Links migrated: 6 tasks · backup board.json.pre-links-migration · u undo" |
| LLR-501.1 | test (unit) | `-k "TC_501 or TC_502 or TC_503 or TC_518"` | invariants over kg board + 11 session states; loop path; TC-503 table; hostile boards < 1 s (< 2 s dense rotating) | pass | 13 nodes; N1–N4, N16 KILLED |
| LLR-501.2 | test (unit) | `-k TC_504` | widths 9/12/24/40, shed order, ≥ 4 callers by AST, help names `◂N`/`▸N`/`L` | pass | TC-504 ×3; N5, N6, N15, N18 KILLED |
| LLR-501.3 | test (unit) | `-k TC_505` | archived pred → blank; due-day start → over; next day → not; `_flowing` | pass | TC-505; N7, N8 KILLED |
| LLR-501.4 | test (unit) | `-k TC_506` | `b` flag only; ready toast count; cap 3 + "+2 more ready"; `u` silent | pass | TC-506 ×3; M14, N9, N10, N19 KILLED |
| LLR-502.1 | test (unit) | `-k "TC_507 or TC_508"` | `L` bound once; painted at 80×24 kanban + gantt; link/unlink + `u`; loop refused; `grep BlockerPicker taskboard/` → 0 | pass | TC-507 ×2, TC-508; P1–P3, P14, P15 KILLED; the `L` key is visible in the 80×24 close captures' key bar |
| LLR-502.2 | test (unit) | `-k "TC_509 or TC_510"` | TC-509 oracle (72 rows, 7 forms reached); `ma` → 4 of 24; S1 | pass | TC-509 ×3, TC-510 ×2; P4–P7, P10, P11, P16 KILLED |
| LLR-502.3 | test (unit) | `-k "TC_511 or TC_512"` | `═` exactly the overlap columns; connectors right of the gutter; loop skipped; keys at 80×24 | pass (the tone clause by inspection, G-002) | TC-511 ×6, TC-512 ×4; Q1–Q24 KILLED |
| LLR-502.4 | test (unit) | `pytest tests/test_readme.py tests/test_keymap.py` | README key table = keymap; 0 `⛓` in README | pass | qa-reviewer run green; `grep ⛓ README.md` → 0 |
| LLR-503.1 | test (unit) | `-k TC_513` | rows for tm3/tw5/ta2/to4 = TC-513 table; due form; repaint after `x` | pass | TC-513 ×4; P12, P13, P17–P21 KILLED |
| LLR-504.1 | test (unit) | `-k TC_517` | refusal text 1/2/5 waiters; `None` for done / archived waiter / inside set / unarchive; 0 undo snapshots | pass | TC-517 ×5; N11–N14, N20, N22, P8, P9 KILLED |
| LLR-505.1 | test (unit) | `-k TC_514` | eight shapes land as §5; board unchanged by the call | pass | TC-514 ×4; M1–M3, M18, M19, M21 KILLED |
| LLR-505.2 | test (unit) | `-k TC_515` | backup bytes; `.1` on a taken name; symlink taken; log = changes; mark; second call no-op; malformed marks; failures leave file byte-identical + unmarked; team pull sees no extra user | pass | TC-515 ×16; M4–M9, M15–M17, M20, M22 KILLED |
| LLR-505.3 | test (unit) | `-k TC_516` | one toast; `u` one step restores all, mark stays; purged task skipped; exit message basename only | pass | TC-516, AT-508; M11–M13 KILLED |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a verification nobody ran. Write your own rows in the table above.

```text
| *(example)* HLR-001 | test | `pytest … -k TC-001` | exit 0 | | |
| *(example)* LLR-001.1 | test (unit) | `…` | `…` | | |
```

### Layer B — behavioral (black-box) acceptance

All ATs run `TaskboardApp.run_test(...)` over a board file in `tmp_path`, built from the synthetic `tests/kg_board.py` (no real board opened, A2). Executor: the orchestrator (gate run) and qa-reviewer (targeted run). Both runs were green for every AT.

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-501 | AT-501 `test_AT_501_the_board_says_who_waits_and_b_is_an_outside_block` | keys `4`, `tab`, `b`, `]` at 118×40 | painted kanban strips (grouped + lanes): `◂`/`▸` counts, muted tone from segments; `screen_stack`; toast text | ✓ marks equal `link_marks` · ✓ `◂2`, high-band card keeps its tag (A-3), lanes 8/8 · ✓ 0 `⛓`, `b` opens nothing and keeps `depends_on`, a further `]` gives 0 ready toasts | pass |
| US-502 | AT-502 `test_AT_502_L_links_from_the_picker` | keys `L`, typed filter, `enter`, `up`, `u`, `escape` | `.modal-title`; `#link-list` prompts; **saved board file re-read** (`tw5.depends_on == [tw2, tw4, tm6]`); `◂3` painted on the card; toast | ✓ link / unlink / `u` · ✓ create with typed title and with empty filter (TextPrompt) · ✓ loop row disabled with "⟲ would loop", esc leaves `depends_on == []`, S1 title literal | pass |
| US-502 | AT-503 `test_AT_503_link_in_the_gantt` + `test_AT_503_board_text_is_painted_as_text` | keys `3`, `L`, `down`, `enter`, `escape` at 118×30 | painted gantt strips (header, "24 candidates · ⟲1 would loop", `⟲` on SEO row, loop legend, status row); **saved board file** after ↵ link and ↵ unlink; bytes unchanged after esc; toast | ✓ link · ✓ linked candidate → "↵ unlink" · ✓ esc changes no byte; S1 payloads painted literally. Filter echo and no-match are app-driven in TC-512; `═` and connector glyphs are asserted in TC-511 on the frame function, and their tone only in the capture (G-002, G-003) | pass |
| US-503 | AT-504 `test_AT_504_the_details_show_and_edit_the_links` | keys `enter`, `tab`, `x`, `escape`, `u`, `L`, typed filter at 118×40 | `#deps-list` rows; focus; **saved board file** after `x`; `selected_task_id` + `_line_map` after jump; repainted section after `L` | ✓ rows · ✓ `tab` round trip with layout unchanged, chain row, `u` restores · ✓ removed row absent, S1 title literal. The conflict line is asserted by TC-513 through the app | pass |
| US-504 | AT-505 `test_AT_505_work_others_wait_on_is_not_put_away` | keys `x`, `d`, `e` + `#save` click, `X` + `#yes`, `P`, `j`, `x`, `escape` | **board file bytes unchanged** after `x`/`d`; toast naming `Deprecate v1 endpoints`; screen stack (no confirm); project not archived | ✓ refused on 3 task paths + project · ✓ done predecessor archives, `X` archives done work · ✓ 0 confirm dialogs, editor's other field saved ("other changes saved") | pass |
| US-505 | AT-506 `test_AT_506_an_old_board_opens_migrated_once_with_its_backup` | app start on an unmarked legacy file, key `u`, **second app start on the file the first wrote** (C-12) | **backup file** `board.json.pre-links-migration.1` bytes == pre-start bytes (first name taken); **saved board** per shape; **log file** JSON change set; one toast; bytes of board, backup and log identical after the 2nd start | ✓ eight shapes · ✓ taken backup name → `.1` · ✓ 2nd start: 0 `Links migrated` toasts, no byte changed | pass |
| US-505 | AT-507 `test_AT_507_a_board_needing_no_change_is_only_marked` | app start on a legacy file whose links already read right | no backup, no log beside the file; mark set on disk; L4 kept | ✓ empty branch · ✓ released link to done kept · ✓ 0 toasts | pass |
| US-505 | AT-508 `test_AT_508_a_backup_that_cannot_be_made_stops_the_app` | app start with stdlib `open` refusing `.pre-links-migration` names | `app.return_code == 1`; **stderr** holds "Link migration stopped", "Permission denied", `--board`, no `tmp_path`; board bytes == pre-start; unmarked on disk | ✓ fail closed · ✓ message has no folder path · ✓ app does not open unmigrated. Log and save failures are covered at `run_link_migration` (TC-515), not through app start (G-004) | pass |

**Migration safeguard (US-505) — the operator's "Respaldo automático + deshacer", checked clause by clause:**

| Clause | Where observed | State |
|---|---|---|
| backup before any change, byte-identical | AT-506 (`backup.read_bytes() == raw`, read before the app starts); TC-515; M11 (migration after the renumber save) KILLED | `executed` ✓ |
| never overwrite a file | AT-506 (first name taken → `.1`); TC-515 (backup and log names taken; dangling symlink counts as taken); M5, M15 KILLED | `executed` ✓ |
| every change logged | AT-506 (log `task_id` set == `LEGACY_CHANGED`); TC-515 (records == change list); M8 KILLED | `executed` ✓ |
| undo as one step, mark kept | AT-506 (`u` → L2 back to `(True, [to1, to2])`); TC-516 (every changed task restored, purged one skipped, mark on disk); M12 KILLED | `executed` ✓ |
| never twice | AT-506 (fresh app on the written file: 0 toasts, 3 files byte-identical); TC-515 (second call returns `None`); M4, M20 KILLED | `executed` ✓ |
| fail closed (backup / log / save) | AT-508 (backup, through the app: exit 1, file byte-identical, unmarked); TC-515 ×3 failure arms (backup, log, save at `run_link_migration`: file byte-identical, unmarked, no temp, no files left); M6, M13, M17, M22 KILLED | `executed` ✓ (log/save through the app: G-004) |
| backup/log invisible to team pull | TC-515 team-pull arm; M9 KILLED (it SURVIVED at r3 when an edit deleted the arm, and was restored at r4) | `executed` ✓ |
| synthetic boards only | every migration node builds `kg_board.legacy(tmp_path / …)`; no real board path appears in the tests | inspection ✓ |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | `b` on a linked task | `action_toggle_blocked` | yes (key) | AT-501, TC-506 | ✓ |
| input | `]` to the last phase / editor phase | `action_phase_move`, `_on_task_edited` → `ready_messages` | yes (key; editor) | AT-501, TC-506 | ✓ |
| input | `L` in kanban (picker) | `action_link` → `LinkPicker` | yes (key) | AT-502, TC-510 | ✓ |
| input | `L` in gantt (link mode) | `action_link` → `GanttLinkMode` | yes (key `3`, `L`) | AT-503, TC-512 | ✓ |
| input | `L` from details | `TaskDetails` → `open_link_picker` | yes (key) | AT-504 | ✓ |
| input | typed filter, `backspace`, no-match | `LinkPicker` / `GanttLinkMode.filter` | yes (keys) | TC-510, TC-512 | ✓ |
| input | `↑`/`↓` over candidates (loop skipped) | `GanttLinkMode` cycle; `#link-list` | yes (keys) | TC-512, AT-503 | ✓ |
| input | create row (typed title / empty filter) | `_create_and_link`; `TextPrompt` | yes (keys) | AT-502 | ✓ |
| input | `tab` / `x` / `↵` in details | `TaskDetails` → `unlink_tasks`, `jump_to` | yes (keys) | AT-504, TC-513 | ✓ |
| input | `x`, `d`, editor archived box, `P` project archive | `archive_refusal`, `project_archive_refusal` | yes (keys, click) | AT-505 | ✓ |
| input | `u` after link / unlink / migration | `action_undo` | yes (key) | AT-502, AT-504, AT-506, TC-516 | ✓ |
| input | board file on disk: unmarked / marked / no-change / malformed mark / unwritable backup | `run_link_migration` on `on_mount` | yes (app start) for unmarked, marked (2nd start), no-change, backup failure; malformed marks at the service | AT-506, AT-507, AT-508; TC-515 | ✓ |
| output | `◂N` / `▸N` card marks, muted | `link_marks` → `card_cell` | yes (painted strips + segment tone) | AT-501 | ✓ |
| output | gantt `↳` gutter, over tone on conflict | `gantt_dep_mark` | yes in captures (`close-gantt-*.txt`); asserted at function level | TC-505 | ✓ |
| output | ready toast | `ready_messages` | yes (painted toast) | AT-501; `close-ready-118x30.txt` | ✓ |
| output | refusal toasts (task, project) | `archive_refusal`, `project_archive_refusal` | yes (toast) | AT-505; `close-guard-*.txt` | ✓ |
| output | picker title, rows, hints, loop row | `LinkPicker`, `link_hint`, `link_candidates` | yes (`#link-list` prompts) | AT-502, TC-510; `close-picker-*.txt` | ✓ |
| output | link-mode header, `⟲`, status rows, legend | `gantt_link_frame` | yes (painted strips) | AT-503, TC-512 | ✓ |
| output | `═` overlap cells + connector, over / bright tone | `gantt_link_overlay` | glyphs: function level (TC-511) + painted capture; tone: capture SVG only | TC-511; `close-gantt-link-*.svg` | partial — G-002 |
| output | details dependency section + conflict line | `TaskDetails` | yes (`#deps-list`, render) | AT-504, TC-513; `close-details-*.txt` | ✓ |
| output | saved board file (links, flags, mark) | `Board.save` / `save_atomic` | yes (re-read from disk) | AT-502, AT-503, AT-504, AT-505, AT-506, AT-507 | ✓ |
| output | backup file, log file | `run_link_migration` | yes (on disk, bytes compared) | AT-506, AT-507 | ✓ |
| output | migration toast; undo toast | `_migrate_links`, `action_undo` | yes (toast) | AT-506, TC-516; `close-migration-*.txt` | ✓ |
| output | exit message on failure | `_migrate_links` exit path | yes (stderr, return code) | AT-508 | ✓ |
| output | README links section, key table | `README.md` | yes (file) | `test_readme.py`, `test_keymap.py` | ✓ |
| output | `L` in the primary key bar at 80×24 | keymap → key bar | yes (painted; captures) | TC-508; `close-*-80x24.txt` | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2218 | 2 | 79 | 2295 | 2295 (gate run: 2294 passed, 1 failed) | n/a — one suite, no lean tier / 2294 of 2295 | yes |

Per increment, read off the packets and checked against each gate transcript:
- 001: 2242 = 2218 − 2 + 26 (AT-D1's two block-flow nodes deleted; 25 in `test_link_migration.py`, 1 in `test_links.py`). Gate: 2242 passed.
- 002: 2265 = 2242 − 0 + 23 (`test_links.py`; pins rewritten in place). Gate: 2265 passed.
- 003: 2282 = 2265 − 0 + 17 (9 picker, 5 details, 3 links). Gate: 2281 passed, 1 failed (the clipboard node).
- 004: 2295 = 2282 − 0 + 13 (`test_gantt_link.py`). Gate: 2294 passed, 1 failed (the clipboard node).
- The additions total 79 (26, 23, 17, 13), which equals the 79 nodes I collected from the five new files (25 migration, 27 links, 9 picker, 5 details, 13 gantt).

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | HLR-501, HLR-502, HLR-503, HLR-504 | AT-501/502/504/505 select the task under test with `app.selected_task_id = …`, and AT-505 fills the editor with `.value =` before a real `#save` click. The keys under test (`b`, `]`, `L`, `x`, `d`, `enter`) are real; reaching the task is a setter proxy (C-16). Navigation is pre-existing, unchanged surface. | minor | Accept for this batch. The ux-reviewer walkthrough reaches tasks by navigation. No test change required to close. |
| G-002 | HLR-502, LLR-502.3 | The threshold says the waiter's row paints `═` "in the over tone", and §5 says colour claims are asserted from painted segments. No node asserts the tone. TC-511 asserts the `═` glyphs and columns on `gantt_link_frame`'s output, not on the app's painted screen. Observed by qa-reviewer **inspection** of `close-gantt-link-118x30.svg`: the `═` cells are filled `#f43f5e` (= `HEX["over"]`), and the connector is in the bright tone `#e6edf7`. The inspection cannot catch a future regression. | minor | Tests-only follow-up: add a segment-tone arm for `═` to AT-503 (the orchestrator decides: fold now under the test-only rule, or BACKLOG). |
| G-003 | HLR-502 (record) | §5 says "one node each (C-18)", but AT-503 has 2 nodes. §5's AT-503 row also lists filter echo / no-match and `═` / connector, which live in TC-512 / TC-511 rather than in the AT. Traceability record only; every clause is covered by some green node. | minor | Note at close; no product or test change. |
| G-004 | HLR-505, LLR-505.3 | Fail-closed on a **log** or **save** failure is observed at `run_link_migration` (TC-515), not through app start and exit; only the backup failure goes through the app (AT-508, as the contract specifies). The app's exit path reads the same `result.error`, so the risk is low. | minor | None required. Optionally parametrize AT-508 over backup / log / save. |
| G-005 | §5.2 "0 failures other than a declared environment flake" | Gate run: `tests/test_app.py::test_win_clipboard_roundtrip` failed. **Classified environment, not product:** (a) the failing assertion is the test's own SETUP guard (`Set-Clipboard` exit 1, `ExternalException`), raised before product code runs; (b) a bare `powershell Set-Clipboard` outside pytest fails identically (qa-reviewer, this session); (c) the batch diff changes no clipboard line (the only hit is an unchanged import context line); (d) the node passed in the base run (2218 passed) and in the 001 and 002 gate runs. It is the known G-011 item. §5.2 allows a declared environment flake, so the criterion is met. | minor (environment) | The orchestrator re-runs that node when the OS clipboard is free, or the operator accepts it at close, as in batch 2026-10-02-batch-03. |

**Record hygiene for the orchestrator (outside this artifact; not gaps in the product):**
- `increment-004.md` cites its evidence as `evidence/…` rather than repo-relative `.dev-flow/2026-10-04-batch-01/evidence/…`. The validator raises a V41 notice on each of its 13 rows and V56 ("none of its 13 cited artifacts could be read"). The files exist and their bytes are in the evidence home.
- `increment-004.md` §Signed-balance has stray backticks (``` ``2295 = 2282 − 0 + 13` ✓ (…)` ```).
- `increment-002.md` gets a V56 notice ("6 failed" vs "7 failed" in a cited transcript): the 7 come from `inc002-red-on-inc001.txt` (a RED by construction) and the 6 from `inc002-green.txt`. Saying which transcript is which would clear it.

### Escaped-bug regression (if a defect escaped the suite)

No defect escaped to a shipped build. Three product defects escaped an increment's own tests and were caught by `code-reviewer`. Each got a RED-first regression:

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| TC-517 Setup arm (inc 002 F2: Setup `x` archived the hidden selection) | `evidence/inc002-f2-red.txt` — `ta3` archived from Setup | value | yes — N20 (Setup `x` reaches the task) KILLED | pass | `tests/test_links.py::test_TC_517_*` (Setup arm) |
| TC-513 closed-task arm (inc 003 F1: a closed task's open predecessors painted `done`) | `evidence/inc003-f1-red.txt` — `tw4` painted `done` | value | yes — P19/P20 KILLED | pass | `tests/test_details_links.py::test_TC_513_a_closed_tasks_rows_show_their_own_state` |
| TC-512 wide-title / long-filter arms (inc 004 F1: keys pushed off at 80 columns) | `evidence/inc004-f1-red.txt` | value (painted keys missing) | yes — Q22, Q22b, Q23 KILLED at r3 | pass | `tests/test_gantt_link.py::test_TC_512_keys_survive_wide_titles_and_a_long_filter[*]` |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

- ✓ **Acceptance criteria in Given / When / Then.** The contract writes them in the flow's EARS form, which maps onto Given/When/Then: "When …, the system shall …" plus a numeric threshold over a named fixture. Given = the shifted kg board / the legacy file (§5); When = the keys of each HLR's *Shipped surface*; Then = the *Numeric pass threshold*. 5/5 HLR carry all three (`01-requirements.md` §3).
- ✓ **Explicit Expected, not "works".** Every HLR/LLR has a numeric threshold, e.g. "`◂` 7 of 8 grouped", "backup bytes == pre-call file bytes", "24 candidates · ⟲1 would loop".
- ✓ **Edge cases: empty, boundary, invalid, error.** Every HLR/LLR has a QC-3 boundary catalog; each N/A is declared. Error arms are AT-508 and the TC-515 ×3 failure arms; empty arms are AT-507, TC-514 (empty board) and TC-513 ("no links — L adds one").
- ✓ **Regression checklist exists.** A reverse census per increment (B1–B4, A3) with two misses named and fixed (002 `test_gantt_polish.py`, 003 `test_colour_budget_app.py`), plus the full gate run: 2294 passed.
- ✓ **Exit criteria stated.** `01-requirements.md` §5.2. All three are met: every HLR has a passing AT and every LLR a passing TC; every existing node changed is in a census; 0 failures other than the declared environment flake (G-005).
- ✓ **No real PII / secrets.** All boards come from `tests/kg_board.py` in `tmp_path` (A2). The only host paths in evidence are redacted to `<home>`.
- ✓ **Mode declared.** `validation`, at the top of this artifact.
- ✓ **Validation mode: every case carries a result or a state, with its executor.** §What was executed names the orchestrator, `software-dev` and `qa-reviewer` per run. The UX walkthrough is pending `ux-reviewer` and is declared as such rather than left blank.
- ✓ **Layer B (black-box).** 5/5 stories are observed through `TaskboardApp` with real keys, and the deliverables (board file, backup, log, stderr, painted strips, toasts) are read back. Notes are G-001 and G-002.
- ✓ **Bidirectional surface-reachability.** 12 input and 14 output rows in the matrix above. 1 partial (G-002, tone by inspection).
- ✓ **No unfilled template.** No `<…>` placeholders, unassigned ids or empty Steps/Expected remain. The UX rows say `pending — ux-reviewer` by design (parallel walkthrough, merged by the orchestrator).

---

### Orchestrator fold after the P4 evaluations (2026-10-04)

The qa evaluation above ran on increment 004's frozen r3. The ux walkthrough (merged above) and the
security close pass came back in parallel; their product findings were handled as follows, and the
result re-gated.

| Finding | Source | Handling | Evidence |
|---|---|---|---|
| F4 (MED) — the overlay vanishes when the waiter's group folds | ux, from code review 004 | increment 005: the hint row says it (A-8); the shared fold rule is the operator's call at PV-5 (D-528) | `03-increments/increment-005.md`; `evidence/inc005-f4-red.txt` |
| G-002 — the `═` tone unasserted | qa | increment 005: TC-511 asserts the over and bright tones (mutants R4, R5 KILLED) | `evidence/inc005-mutations-r3.txt` |
| U-2 (MED) — a lanes card's title shed beside `▸1 ◂1` | ux | not changed: a title floor broke two shipped width contracts (`test_cells.py`), reverted byte-exact; the operator's call at PV-1, BACKLOG (D-529) | `01-requirements.md` D-529 |
| E-1 (MED, evidence) — the lanes captures showed the matrix | ux | `capture_b1.py` presses `4 tab tab`; base and close lanes re-shot | `evidence/captures/{base,close}-kanban-lanes-*` |
| E-2 (LOW, evidence) — PLAN PV-5 said "two status rows" | ux | PLAN updated (A-7) | `PLAN.md` |
| security F1 (LOW) — a read-only board on Windows leaves a temp file per launch | security close | approved migration save path: routed to the operator and BACKLOG (D-530) | `05-close.md` §1 |
| U-3..U-7, N-1..N-7 (LOW/NIT) | ux | BACKLOG | `05-close.md` §4 |

- **Re-gate on the final product (increment 005 frozen r3):** 2295 passed, 1 failed — the same
  environment flake (G-005/G-011) — in 444.93 s (`evidence/inc005-gate-r3.txt`). Test ledger: 2296 =
  2218 − 2 + 80 (one node added by increment 005).
- **Verdict unchanged:** `PASS-WITH-NOTES`; the PV verdicts are the operator's (05-close.md).

### Increment 006 re-validation (re-open, D-531)

**Light P4 by `qa-reviewer`. The re-opened batch still holds `PASS-WITH-NOTES`, with 0 blocker gaps.** The operator ruled on three items (D-528, D-529, D-530). Each ruling is observed through the shipped surface by a node that went RED on the product as first closed. The migration safeguard is still evidenced. The gate on the final product has 0 failures. Three new minor notes (G-006..G-008) are below. The evaluation above is unchanged; only the **Requirements** and **Test ledger** lines of §✅ Verdict were updated, because their facts changed.

**Mode: validation.** This section evaluates increment 006 frozen r2, which is the final product.

#### What was executed, by whom, on which tree

| Run | Executor | Tree | Command | Output | State |
|---|---|---|---|---|---|
| **The ONE complete gate run** (C-25) | **orchestrator** | 006 frozen r2 | `python -m pytest -q -p no:cacheprovider` | `evidence/inc006-gate-r2.txt`: **2306 passed in 414.80 s**, 0 failed, 0 skipped. The clipboard node passed (r1: 2304 passed, `inc006-gate-r1.txt`) | `executed` |
| RED counterfactual on 005 frozen r3; M1 RED on r1 | software-dev (packet 006) | 005 frozen r3 / 006 r1 | `evidence/battery.py` | `evidence/inc006-red.txt`: 6 FAILED. `evidence/inc006-m1-red.txt`: (11, tw3, tw4) paged apart | `executed` (consumed) |
| Mutation battery r2 | software-dev (packet 006) | 006 frozen r2 | `evidence/battery.py` + `mutants_inc006_r2.json` | 12 KILLED, 0 SURVIVED, 0 BAD (recounted by qa-reviewer: S1–S12 each on a `KILLED` header line in `inc006-mutations-r2.txt`) | `executed` (consumed) |
| Security delta and safeguard re-run | security-reviewer (packet 006 §4b) | 006 r1/r2, synthetic boards | per packet | PASS-WITH-NOTES. Backup before the write, `.1`, the log exact, `u` one step, run-once byte-identical, fail-closed, read-only ×3 launches leave nothing | `executed` (consumed) |
| Freeze check | **qa-reviewer** | working tree | `sha256sum -c inc006-frozen-r2.sha256` (`<home>` expanded) | 5/5 OK: `models.py`, `views.py`, `test_link_migration.py`, `test_gantt_link.py`, `test_links.py` | `executed` |
| Targeted run | **qa-reviewer** | same tree | `python -B -m pytest -q -p no:cacheprovider -rs tests/test_gantt_link.py tests/test_links.py tests/test_link_migration.py tests/test_cells.py tests/test_kanban_readable.py` | **471 passed in 57.22 s**, 0 failed, 0 skipped. The Windows-only failed-swap arm ran and was not skipped | `executed` |
| Node inventory | **qa-reviewer** | same tree | `--collect-only` over the five new files | 90 nodes = 79 (001–004) + 1 (005) + 10 (006) | `executed` |
| Capture comparison `close-*` vs `close2-*` vs `base-*` | **qa-reviewer** (inspection) | captures by the orchestrator | `cmp`, `diff`, and a count of `◂N`/`▸N`/`⛓` per capture | See G-006 and the capture inspection below | `executed` (inspection) |

#### Each ruling, observed at the surface

| Ruling | Black-box (`TaskboardApp`, real keys) | White-box / unit | RED on the product as first closed | Mutants | State |
|---|---|---|---|---|---|
| **D-528**: link mode pins the waiter's group (A-9) | `test_TC_512_link_mode_keeps_the_waiters_group_open`. At 118×20 the waiter row is painted once with `═` and no fold note. At 118×14 both rows are painted (shared rows). The plain `gantt_plan` still folds Website Redesign, so the shipped rule is untouched | TC-512 fallback moved to 118×12 and 80×12 | pin test FAILED (folded at 118×20) | S4, S5, S6, S7 KILLED | `executed` (gate: orchestrator; targeted: qa-reviewer) |
| **D-534**: one page holds both (M1) | n/a — a frame-allocation property that needs an exhaustive oracle across groups × pairs × heights, so it is asserted on `gantt_link_frame` (the frame link mode paints). The surface arm is the D-528 node | `test_TC_512_one_page_holds_both_when_it_can`: more than 100 pairs at heights 11–13, with the full gantt's row order as oracle | M1 RED (`inc006-m1-red.txt`) | S12 KILLED | `executed` |
| **D-529 / D-533**: lanes title floor of 6 cells, marks shed first (A-10) | `test_TC_504_a_lanes_card_keeps_a_readable_title[118×30, 80×24, 118×40]`: every painted lanes cell shows ≥ 5 title characters or a whole title or word. `test_TC_504_wide_lanes_still_paint_every_mark`: at 160×40 the counts are exact, `◂` {1:7, 2:1} and `▸` {1:7, 2:1} | `test_TC_504_the_lanes_floor_sheds_the_marks_before_other_meta`: for widths 8–39, a mark is never kept after the age is shed. Without the floor the shipped law keeps `◂1` (`test_cells.py` is unchanged and green) | TC-504 ×3 FAILED (`▊ ++  ▸1 ◂1 +6d`) | S8, S9, S10, S11 KILLED | `executed` |
| **D-530 / D-532**: read-only refusal and temp cleanup (A-11) | `test_AT_508_a_read_only_board_stops_the_app_and_leaves_nothing`: exit 1, stderr names `board.json` and no folder path, nothing beside the board, bytes unchanged | TC-515 read-only (two runs, error starts `board.json:`). TC-515 failed swap with `os.access` patched (Windows): the temp file is removed and the save's error is not masked | TC-515 and AT-508 read-only FAILED (`.board.json.<random>.tmp: Access is denied`) | S1, S2, S3 KILLED | `executed` |

**Capture inspection (qa-reviewer).** In lanes, `close-kanban-lanes-118x30` painted 16 marks and cards with no title (`▊ ==  ·7d ▸1 ◂1 +8d`). `close2-kanban-lanes-118x30` and `close2-kanban-lanes-80x24` paint 0 marks, 0 `⛓`, and every title with ≥ 5 characters, as D-533 states. Waiting stays visible in the grouped kanban (AT-501's grouped arm is unchanged), the gantt gutter and the details section.

#### Migration safeguard, still evidenced

AT-506 (old board migrated once, with its backup), AT-507 (no change → only marked), AT-508 backup refused (fail closed, bytes unchanged, unmarked), the new AT-508 read-only arm, and TC-515 (16 earlier arms + read-only + failed swap) all passed in the orchestrator's gate and in my targeted run. The security delta re-ran the safeguard by hand on synthetic boards (packet 006 §4b). D-532 changes the POSIX behaviour by design: a read-only board is now refused instead of replaced. This is recorded for the operator in the packet's §5 Risks.

#### Reverse census claim, checked

The claim is that AT-501's lanes arm was rewritten to the new law and a 160×40 exact arm was added. **It holds, with a strength note (G-007).** The lanes arm at 118×40 now asserts `◂` counts ≤ the board's values and no `⛓`. The exact values moved to a separate node, `test_TC_504_wide_lanes_still_paint_every_mark` (160×40), which is a TC-504 node and not part of AT-501. `test_cells.py` has no diff, so the shipped width law stands for every other caller.

#### Vacuity check

- Every new node has a named RED (6 on the product as first closed, plus M1) or a KILLED mutant. No new node passes on both sides.
- G-007: the AT-501 lanes arm alone is weak. It passes on 0 marks, and it does not check `▸`. The law is still held at the surface by TC-504 ×3 and the 160×40 arm.
- G-008: D-533 claims more pinning than the tests do.

#### Gaps detected (re-open)

| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-006 | HLR-502, LLR-502.3 (D-528) | The `close2-gantt-link-*` captures are **byte-identical** to `close-gantt-link-*` at 118×30 and 80×24. At those sizes both groups were already drawn before 006, so the captures do not show the pinned case. The pin is observed only by nodes (TC-512 at 118×20/14/12, app-driven), not in a capture the operator can look at. | minor | Optional: the orchestrator adds a `close2-gantt-link-118x20` capture if the operator wants to see D-528 before the push. No test change. |
| G-007 | HLR-501 (AT-501 lanes arm) | The lanes arm is an upper bound on `◂` (`lanes[k] <= …`), so it passes on 0 marks and never checks `▸`. On its own it cannot fail for lost marks. The surface law is held by TC-504 ×3 and the 160×40 exact arm (S8–S11 KILLED). | minor | Accept. Optionally assert in AT-501 that at 118×40 lanes paint 0 `◂`/`▸` (D-533's consequence) instead of the bound. |
| G-008 | LLR-501.2 (record, D-533) | D-533 says "TC-504 pins both: 0 marks at 118 with every title readable". No node asserts 0 marks at 118: TC-504 at 118 asserts titles only. The 0 is observed by my capture inspection (`close2-kanban-lanes-118x30`: 0 marks). The claim is stronger than its nodes. | minor | Reword D-533 ("observed in the close2 capture"), or add the 0-marks assertion with G-007's change. Record only; no product change. |

G-005 (clipboard, environment) did not reproduce on the final product: the node passed in both 006 gate runs. It stays above as history.

#### Test ledger (re-open)

| base | − D | + A | = post | actual collected | passed | reconciles? |
|------|-----|-----|--------|------------------|--------|-------------|
| 2218 | 2 | 90 (79 + 1 + 10) | 2306 | 2306 (orchestrator's gate, `inc006-gate-r2.txt`) | 2306 of 2306 | yes |

Increment 006 adds +10: 3 in `test_link_migration.py`, 2 in `test_gantt_link.py`, 5 in `test_links.py`. 2296 + 10 = 2306. The five new files collect 90 nodes (qa-reviewer).

#### Evidence checklist — qa-reviewer (re-open delta)

- ✓ **Explicit Expected.** Every new node states a value oracle: exact mark counts at 160×40; ≥ 5 title characters; `board.json:` named; an empty listing beside the board; bytes unchanged.
- ✓ **Edge cases.** Boundary: 118×12 / 80×12 (fallback), 118×14 (shared rows), widths 8–39 (floor). Error: read-only board, failed swap, a cleanup error that must not mask the save's error.
- ✓ **Regression checklist.** Reverse census B1/B4 checked above. `test_cells.py` and `test_kanban_readable.py` are green in my run. The plain gantt is byte-identical over 1,218 frames (code-reviewer, consumed).
- ✓ **No real PII / secrets.** Only `kg_board` in `tmp_path` was used. The real board was not touched by me. Home paths in the evidence are `<home>`.
- ✓ **Validation mode: every result names its executor.** See the run table above.
- ✓ **Layer B.** D-528, D-529 and D-530 are each observed through `TaskboardApp`. D-534 is the one frame-level property; its surface arm is D-528's node.
- ✓ **No unfilled template.**

Re-open verdict: PASS-WITH-NOTES. 0 blockers. G-006, G-007 and G-008 are minor, and none needs a product change before the push.

### UX light walkthrough after the re-open (increment 006) — merged by the orchestrator

`ux-reviewer` **PASS-WITH-NOTES** (`.dev-flow/2026-10-04-batch-01/evidence/p4-ux-walkthrough-006.txt`):
D-528, D-529, D-530 met as worded, driven with real keys on synthetic boards (link mode at 118×30,
118×20, 118×14, 118×13, 118×12, 80×24, 80×14, 80×12 and an 11-task-project board; lanes at 118×30,
118×40, 80×24, 140×30, 160×40; a read-only board through `run_test` and `python -m taskboard`);
the plain gantt and the other surfaces identical to the accepted captures but the clock. Five LOW:
R6-1 (the fallback note says "folded" for a paged-out waiter; the packet's threshold corrected),
R6-2 (no pager line on the waiter's group when rows are shared), R6-3 (lanes show no marks at 118 and
80 while the age stays — flagged to the operator with D-533), R6-4 (the read-only exit advice names
the folder), R6-5 (pre-existing: `python -m taskboard` exits 0 after a fail-closed stop) → BACKLOG.
qa's G-006 answered with `evidence/captures/close2-gantt-link-118x20.*` (the waiter pinned where it
used to fold); G-008 answered by rewording D-533.

### Increment 007 re-validation (second re-open, D-535)

**Light P4 by `qa-reviewer`. The batch still holds `PASS-WITH-NOTES`, with 0 blocker gaps.** The operator ruled D-533 "Dejar ◂ solo, quitar la edad antes" (A-12) and D-532 "Sí, en todas las plataformas" (recorded, no code). The surface shows the D-533 ruling: at 118×30 and 80×24, every painted waiting card in lanes shows its `◂N` and keeps a title of at least 6 cells. Every other view is byte-identical to increment 006. The gate on the final product has 0 failures. G-007 is closed for `◂`. G-008 is superseded. Two new minor notes are below (G-009, G-010). Only the **Requirements** and **Test ledger** lines of §✅ Verdict changed, and only to point at 007.

**Mode: validation.** This section evaluates increment 007 frozen r1, which is the final product.

#### What was executed, by whom, on which tree

| Run | Executor | Tree | Command | Output | State |
|---|---|---|---|---|---|
| **The ONE complete gate run** (C-25) | **orchestrator** | 007 frozen r1 | `python -m pytest -q -p no:cacheprovider` | `evidence/inc007-gate-r1.txt`: **2306 passed in 432.92 s**, 0 failed | `executed` |
| RED counterfactual on 006 frozen r2 (`views.py` `f21f3683…`) | software-dev (packet 007) | 006 frozen r2 | `evidence/battery.py` | `evidence/inc007-red.txt`: 5 FAILED (AT-501 `Counter()` ≠ 7×`◂1` + 1×`◂2`; TC-504 ×3 `▊ !! Launch n… +10d` with no `◂2`; the order unit test). The 160×40 arm PASSED on both sides, as the packet declares | `executed` (consumed) |
| Mutation battery | software-dev (packet 007) | 007 frozen r1 | `evidence/battery.py` + `mutants_inc007.json` | 6 KILLED, 0 SURVIVED (qa-reviewer recounted U1–U6, each on a `KILLED` line in `inc007-mutations.txt`) | `executed` (consumed) |
| Identity proof | software-dev (packet 007); code-reviewer sweep (§4b) | 006 r2 vs 007 r1 | `evidence/identity007.py` | `inc007-identity.txt`: 4,404 non-lanes renders/cells IDENTICAL. Positive control: lanes DIFFERENT. The reviewer's 10,124-render sweep agrees | `executed` (consumed) |
| Freeze check | **qa-reviewer** | working tree | `sha256sum` vs `inc007-frozen-r1.sha256`; `sha256sum -c inc006-frozen-r2.sha256` | `views.py` `3f773ada…` and `test_links.py` `f39c3ddb…` match 007 r1. Against 006 r2, only those two files differ; `models.py`, `test_link_migration.py` and `test_gantt_link.py` are OK | `executed` |
| Targeted run | **qa-reviewer** | same tree | `python -B -m pytest -q -p no:cacheprovider -rs tests/test_links.py tests/test_cells.py tests/test_kanban_readable.py` | **427 passed in 31.29 s**, 0 failed, 0 skipped | `executed` |
| Node inventory | **qa-reviewer** | same tree | `--collect-only` over the five new files | 90 nodes, unchanged from 006 (one unit test replaced) | `executed` |
| Capture comparison `close3-kanban-lanes-*` vs `close2-*` | **qa-reviewer** (inspection) | captures by the orchestrator | `grep -o` counts of `◂N`/`▸N`/`⛓`/`·Nd`; per-cell read | See below | `executed` (inspection) |

#### D-533, observed at the surface

| Size | `close2` (006) | `close3` (007) | Ruling met? |
|---|---|---|---|
| 118×30 | `◂` 0 · `▸` 0 · age 7 · `⛓` 0 | `◂` {1:7, 2:1} = all 8 waiting cards (`Launch… ◂2 +6d`, `Optimi… ◂1`, `Offli… ◂1`, `Beta … ◂1`, `Add pu… ◂1`, `Deprec… ◂1`, `SDK re… ◂1`, `BI da… ◂1`). Every waiting title is ≥ 6 cells (smallest: `Offli…`, `Beta …`, `BI da…`). `▸` 4, on non-waiting cards only. Age 5. `⛓` 0 | yes. `Add pu… ◂1 +8d` (tm3: `▸1 ◂1`, aged) sheds the age and `▸` and keeps `◂` and the due |
| 80×24 | `◂` 0 · `▸` 0 · age 0 | `◂` {1:7, 2:1} = all 8 waiting cards (the DONE column is off-screen and holds no waiter). Every title is ≥ 6 cells (smallest: `SDK r…`). The due is shed on waiting cards (`Launch… ◂2`), and `Partn… -1d` sheds `▸1` and keeps its due | yes, in the ruled order: age → `▸` → other meta → `◂` |

The nodes hold the ruling: AT-501's lanes arm at 118×40 now asserts the exact `Counter({1: 7, 2: 1})` for `◂` and cites D-529 + D-533. The 160×40 arm's docstring cites D-533 and still asserts the exact `◂` and `▸` values. TC-504 ×3 (118×30, 80×24, 118×40) checks each painted waiting card for its `◂N`. The order unit test sweeps widths 8–39 on tm3. Every changed node went RED on 006 except the 160×40 arm, which the packet declares as passing on both sides (it is a regression guard, not a ruling witness).

**Vacuity check.** TC-504's surface loop only checks cards whose title stub matches exactly one board title. I resolved the stubs painted at 118×30 and 80×24 (`Launch`, `Optimi`, `Offli`/`Offlin`, `Beta`/`Beta r`, `Add pu`, `Deprec`, `SDK re`/`SDK r`, `BI da`/`BI das`) against `kg_board`: each matches 1 title. So today every waiting card is checked, not skipped (see G-009 for the weak final assertion). U2 and U4 (`◂` shed early) are KILLED. No node passes on both sides except the declared 160×40 guard.

**Grouped kanban and other views unchanged.** AT-501's grouped arm is unchanged (`◂` {1:6, 2:1}, `▸` {1:7, 2:1}), and the identity proof is IDENTICAL with a positive control. `test_cells.py` and `test_kanban_readable.py` are green in my run.

**D-532.** No code. It is recorded in `increment-007.md` and `01-requirements.md`; there is nothing to observe.

#### Earlier notes, status

| ID | Status after 007 |
|---|---|
| G-006 | answered at 006 (`close2-gantt-link-118x20`). Unchanged |
| G-007 | **closed for `◂`**: AT-501's lanes arm asserts the exact `◂` count at 118×40 and went RED on 006 r2 (`Counter()`). `▸` is still unchecked in that arm, but the ruling makes `▸` the second token to shed and so fixes no `▸` count at 118. The 160×40 arm holds the exact `▸` values |
| G-008 | **superseded**: D-533's "0 marks at 118" consequence is replaced by A-12, and the new claim is pinned by nodes (AT-501 exact, TC-504 ×3), not by a capture alone |
| ux R6-3 (lanes show no marks while the age stays) | resolved by the ruling: the age now sheds first (`close3` 118×30 age 7 → 5) |

#### Gaps detected (second re-open)

| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-009 | LLR-501.2 (TC-504 surface arm) | `test_TC_504_a_lanes_card_keeps_a_readable_title` ends with `assert waiting_seen`, which is ≥ 1, and skips any card whose stub matches more than one title. Today the check is exact: 8 of 8 stubs are unique (qa-reviewer). A future fixture title that shares a prefix could skip a waiting card silently. AT-501's exact count at 118×40 backs it up at one size | minor | Optional test-only: assert `waiting_seen == ` the number of waiting cards painted (8 at these sizes). BACKLOG |
| G-010 | LLR-501.2 (record) | The 160×40 arm's docstring says "at 118 every waiting card keeps `◂`, no `▸`". The `close3-kanban-lanes-118x30` capture paints 4 `▸` (`Build … ▸2`, `Audit … ▸1`, `Partne… ▸1`, `Daily… ▸1`), all on non-waiting cards. The ruling allows this, because `▸` sheds only when it is short of room. The docstring overstates. A visible consequence for ux: a non-waiting aged card now trades its age for `▸` (`Build… ·8d -7d` → `Build … ▸2 -7d`) | minor (record) | Reword the docstring to "no waiting card shows `▸`" at the next test touch. No product change |

#### Test ledger (second re-open)

| base | − D | + A | = post | actual collected | passed | reconciles? |
|------|-----|-----|--------|------------------|--------|-------------|
| 2306 | 1 | 1 | 2306 | 2306 (orchestrator's gate, `inc007-gate-r1.txt`) | 2306 of 2306 | yes |

The D-529 order unit test was replaced by the D-533 one (`test_TC_504_the_lanes_floor_sheds_age_then_unblocks_and_keeps_waits`). The five new files still collect 90 nodes (qa-reviewer).

#### Evidence checklist — qa-reviewer (second re-open delta)

- ✓ **Explicit Expected.** The oracles are exact: `◂` `Counter({1: 7, 2: 1})` at 118×40 and 160×40; `◂N` in every painted waiting cell; per width, no age without `▸`+`◂`, no `▸` without `◂`, no other meta without `◂`.
- ✓ **Edge cases.** Boundary: widths 8–39 (floor), 80×24 (the due sheds before `◂`). Negative: a non-waiting card shows no `◂`. A no-floor caller keeps the shipped law (the unit test's last arm; `test_cells.py` green).
- ✓ **Regression checklist.** Reverse census B1/B3 checked. Non-lanes identity holds over 4,404 + 10,124 renders, with a positive control.
- ✓ **No real PII / secrets.** Only `kg_board` was used, in `tmp_path`. Nothing touched a real board.
- ✓ **Validation mode: every result names its executor.** See the run table above.
- ✓ **Layer B.** D-533 is observed through `TaskboardApp` with real keys (`4`, `tab`, `tab`) at 118×30, 80×24, 118×40 and 160×40, and in the `close3` captures.
- ✓ **No unfilled template.**

Second re-open verdict: PASS-WITH-NOTES. 0 blockers. G-009 and G-010 are minor, and neither needs a product change before the push.

### UX light walkthrough after the second re-open (increment 007) — merged by the orchestrator

`ux-reviewer` **PASS-WITH-NOTES** (`.dev-flow/2026-10-04-batch-01/evidence/p4-ux-walkthrough-007.txt`):
D-533 met as worded at 118×30, 118×40, 80×24, 140×30, 160×40 — 8 of 8 waiting cards show the right
`◂N`, no title under 6 cells, the age goes first and `▸` next; the grouped kanban's painted strips
identical to `close-kanban-*` but the clock. N-1 (minor, the ruling's trade-off: at 80 an overdue
waiting card loses its overdue chip — a new ruling if overdue should outrank `◂`), N-2 (existing: a
cut at a word gap leaves a blank cell), N-3 (no painted grouped baseline at the three larger sizes;
the identity sweep covers them) → BACKLOG, with qa's G-009 and G-010.
