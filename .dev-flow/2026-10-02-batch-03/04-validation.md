# Validation — taskboard — Batch 2026-10-02-batch-03

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1 and **names who executed each one**. The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Mode: validation.** Author: `qa-reviewer` (a named sub-agent following `agents/qa-reviewer.md`, flow pinned to rev98), 2026-10-02. **Iteration 2** — this section is the live record. The iteration-1 record is kept verbatim at the end of this file under *Superseded — iteration 1*; its verdict lines are history, not the gate.
>
> **Who executed what (iteration 2).**
> 1. **The gate re-run** was **launched and collected by the orchestrator** (C-25) on the frozen tree after increment 003: `python -m pytest -q -p no:cacheprovider` → **`1 failed, 1854 passed in 318.08s`** (`evidence/p4-gate2.txt`, sha256 `925bfd3a…70867`; the transcript now carries its command line and names its executor). I read the summary line and the one failure's trace from that run's own output. **I did not run the suite.**
>    **Revision check (`executed` by qa-reviewer):** the transcript was written at 19:42:58. `find taskboard tests -newer evidence/p4-gate2.txt` returns nothing. The newest edits are `tests/test_kanban_readable.py` at 19:30:12 and `taskboard/views.py` at 19:29:04; a 318 s run ending at 19:42:58 began at about 19:37:40, after both. In a scratch copy of the tree, `pytest --collect-only -q` gives **1855 collected** (178 in `tests/test_kanban_readable.py`). The copy's `views.py` hashes to `e46de44c…`, the restore digest in increment 003's final battery; `app.py` is unchanged since iteration 1 (`7c1410e8…`).
>    **The one failure — attributed and classified.** `tests/test_app.py::test_win_clipboard_roundtrip`: state **`failed`**, executor the orchestrator, **cause: environment, not product.** Evidence: (a) the assertion that fired is the test's own SETUP guard: `Set-Clipboard` returned 1 with `Requested Clipboard operation did not succeed` (`ExternalException`), raised before any product code ran; (b) `git diff 13745f6 -- taskboard tests` has **0** lines that mention the clipboard, so the batch did not touch the code or the test; (c) the same node passed in the base run (1677 passed), in both increment green runs and in the iteration-1 gate (1845 passed); (d) `PENDING.md` #22 tracks it as an environment-dependent WATCH item. The orchestrator also reports that it fails in isolation. That is the orchestrator's statement; I did not run it, because the test writes to the operator's machine-wide clipboard. §5.2's "full suite: 0 failures" is therefore **not literally met** (G-011).
> 2. **Increment 003's RED counterfactuals, mutation batteries and green run** were **executed by the increment author** (`software-dev`): `03-increments/increment-003.md`, `evidence/inc003-*.txt`.
> 3. **The code-reviewer's three rounds** on increment 003 (F1–F12, a 2,295-frame sweep) are the reviewer's statement in packet §4b. Its probes are not on disk, so I cite them as stated and do not count them as traced evidence.
> 4. **The ux-reviewer's iteration-1 walkthrough** is now on record, relayed verbatim by the orchestrator (`evidence/p4-ux-walkthrough.txt`, sha256 `82a5f8e3…a1aca`). Its verdict was **FAIL — UXV3-1 (blocker)**. **The ux re-walk of UXV3-1 had not landed in `evidence/` when I finished (checked at 19:50). It is `not-run` here and is not counted** (G-006).
> 5. **My own checks.** Each was `executed` by qa-reviewer and is read-only toward the repo. Probes ran in `%TEMP%\claude\<session>\scratchpad\qa-p4b\` against a fresh copy of the frozen tree (`tree\`) and a `git archive 13745f6` copy of the base (`base\`):
>    - **Evidence digests:** the 14 digests increment 003 cites, checked against the bytes on disk: **14 / 14 OK**.
>    - **Mutation re-run:** I re-ran all 12 recorded increment-003 mutants (C1–C6, F1, F2a, F2b, F3, F5, F10) on my copy with the final tests: **12 of 12 KILLED**, every restore digest `e46de44c…` OK. My transcript (`qa-mutations-inc003.txt`) is **byte-identical** to `evidence/inc003-mutations-r2.txt` (both sha256 `28d7b751…2fc`). C4 and C6 run from `mutants_inc003_c4c6.json`, which the packet does not digest. Its two entries are identical to C4 and C6 in the digested `mutants_inc003.json`.
>    - **The title seat on base and on the frozen tree:** on `13745f6`, `render_view` printed a title of `a` + backslash + `[b` as `a[b` in **5 of 5** seats (agenda, matrix, lanes, Focus inspector, Focus review). On the frozen tree it printed the literal in 5 of 5.
>    - **The widths comparison:** `evidence/widths_compare.py` re-run on the frozen tree gives the same four lines as `evidence/inc001-widths.txt`: floor-first 5.32 at 80×24, proportional 6.21.
>    - **An app walk, down and then back up** (`probe-walk-out.txt`, sha256 `ffc43cbf…811e`). Real `down` then `up` keys over column 0, at 6 cases: oracle under `g g` at 80×24, 118×30 and 80×22, and the 14-high board at 118×30, 80×24 and 80×20. Each step checked: the viewport's `scroll_offset.y == 0`, the painted rows ≤ the viewport, the head row on row 0, and both rows of the selected card inside. **0 violations in 168 steps.** Fold rows that name a cut were painted through the app, e.g. `▲ 2 above   ▲ 3 more in Later   ▼ 1 more in Later   ▼ …`.
>    - **The captures regenerated** with `evidence/capture.py` on the frozen tree: **14 of 16** `close-*.txt` and `readability-close.txt` are byte-identical. **`close-kanban-ops-80x24.txt` and `close-kanban-ops-80x22.txt` differ** (G-009).
>    - **A `-k` audit** of every requirement's *Executed verification* command (G-010).
>    - **Collection counts, the C-18 grep, and the diffs** of the G-004 nodes, D-313, HLR-307 and LLR-301.2.
>
> **Result states** in this file use the seven words: `planned` · `executed` · `approved` · `failed` · `blocked` · `not-run` · `n/a — <reason>`. Every node marked "pass" below was `executed` by the orchestrator in the gate re-run: 1855 collected = 1854 passed + 1 failed (the clipboard node above), 0 skipped.

## ✅ Verdict (read first)

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Result` · `Layer 0` · `Evidence checklist` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.
>
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.

- **Result:** `PASS-WITH-NOTES`
- **Layer 0:** `9 unit(s) met the criterion · 9 carry a named reddening mutation` (the 8 of iteration 1 plus the cut in `_kanban_grouped`. `_fold_row` gained the cut's counts; all KILLED on the frozen tree, re-run by qa)
- **Requirements:** `22`/`22` pass (10 HLR + 12 LLR, with LLR-309.2 new; every requirement node green in the orchestrator's gate re-run) · `0` blocker fails. The one failed node is outside every requirement (environment, G-011)
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface. **C-18 ✓:** AT-301..AT-308 still realise in exactly ONE on-disk function each. `grep "def test_AT_30" tests/*.py` finds 8 functions, all in `tests/test_kanban_readable.py`, none elsewhere. Collected arms: AT-301 ×3, AT-307 ×5 (was ×2), AT-308 ×3, the rest ×1, for 16 in all.
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs are reached or observed at the surface · `0` gaps. AT-307 does not assert the cut fold row's text; it is asserted at the render seat (TC-311) and was seen painted in qa's app walk.
- **Supersession inspection (read off the P3 packets):** ✓ no live dependency on a superseded law. HLR-309's "the panel shall scroll" is deleted (LED .18) and no node asserts it. The G-004 nodes now read the band rules and the phase row's separators. One residue: §6.3 still lists the deleted scroll as an open risk (G-012).
- **Test ledger:** ✓ reconciles (`1677 − 0 + 178 = 1855`; collected 1855 = 1854 passed + 1 failed in the gate re-run)
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 11 of 11 rows ✓ with evidence`

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

> **Why PASS-WITH-NOTES, and not PASS or FAIL.**
> - **Not FAIL:** no blocker in qa's lens. Every HLR and LLR has a green node, and every story has a single-function black-box AT. UXV3-1 is fixed in the code and guarded: AT-307's horizon and 14-high arms and TC-311's two cut nodes were RED on the increment-002 tree, are green now, and are killed by 12 of 12 mutants (qa re-run). qa's own app walk down and back up shows no scroll in 168 steps. Iteration 1's G-001, G-003 and G-004 are discharged on re-read (§Iteration-1 gaps).
> - **Not PASS — four notes and one pending act:**
>   - **G-006:** the ux re-walk of UXV3-1 is not on record. The ux FAIL of iteration 1 stands until it lands. **The P4 gate needs both verdicts.**
>   - **G-011:** the gate run has 1 failed node. It is environmental and classified above, but it does not meet §5.2's "0 failures" literally. The orchestrator re-runs that one node when the clipboard is free, or the operator accepts it at close.
>   - **G-009:** two close captures show a transient increment-003 state the frozen tree no longer paints. Regenerate them before the operator reads the captures (§6.1).
>   - **G-010:** three *Executed verification* commands select 0 nodes, and two select only part of their nodes. This is a record fix.
>   - **G-002:** carried from iteration 1; it was not in increment 003's scope. ⏸ DEFER or tests-only.
>   - **Recommended route:** no further increment for qa's lens. Fold G-009, G-010, G-011 and G-012 into the close record, and fold the ux re-walk verdict. **The user decides** (station: "otherwise, user decides").

---

## Detail (reference) — iteration 2

### Iteration-1 gaps — each discharged by RE-READING the artifact

| Gap | What iteration 1 asked | What is on disk now (re-read) | State |
|---|---|---|---|
| G-001 | put `evidence/inc001-widths.txt` on disk or re-point LED .17 / §6.5 | the file exists, sha256 `d209dfb0…197b` = the packet's digest. Its 4 lines (floor-first 80×24 **5.32** / 2 full; proportional 6.21 / 3) reproduce byte-for-byte when qa re-runs `evidence/widths_compare.py` on the frozen tree. §6.5's citation is now true | **closed** |
| G-002 | tighten 4 threshold clauses or ⏸ DEFER | untouched; not in increment 003's scope (packet §1 names G-001, G-003a, G-003b, G-004). The behaviour still holds by iteration 1's probe1 | **open — minor**, route unchanged |
| G-003a | a shipped-surface regression per shared title seat, RED on base | `test_TC_302_the_shared_title_seat_prints_a_backslash_before_a_bracket` ×5 seats (`test_kanban_readable.py:1130`). RED on `13745f6` in `inc003-red-on-base.txt` (5 FAILED); qa reproduced the pre-fix value directly (`a[b` in 5 of 5 seats on base, the literal on frozen). Mutant C6 (the seat back on `escape`) is KILLED, 5 of 5 arms, in qa's re-run. §6.5 and LED .20 name the scope extension. Note: the node's input is backslash + bracket, not the trailing-backslash `x\ y\` of iteration 1's probe7. The cause is the same (`escape` vs `_literal` at the shared seat) and C6 shows the node guards it | **closed** |
| G-003b | HLR-307 `tw3` → `to3`; LLR-301.2's literal lengths | HLR-307 threshold now reads "with the selection on `to3` (so the Ops & Security band and its `project due +5d` are drawn)". LLR-301.2 reads "a 58-char title, a 24-char single word". §6.5's P4 bullet records both | **closed** |
| G-004 | (a)(b) re-point the stale-geometry nodes; (c) reword D-313 and qualify the docstring | (a) `test_kanban_groups_by_project` (`test_app.py:1496`) now finds `▐ Alpha  ` / `▐ Inbox  ` rules, asserts the tasks sit below their rule, and asserts no other rule falls between them. (b) `test_kanban_marks_blocked_without_moving_it` (`:1516`) reads column bounds off the phase row's `│`. Both carry a dated "Changed … G-004" docstring. (c) D-313 now reads "still holds as written because it renders unwindowed at 160 cells (h 0)". The node's own docstring ("show them ALL", `:1487`) is still unqualified, which is a cosmetic residue. Both nodes are green in the gate re-run. They are PINs of laws that hold, not new assertions, so no RED is owed (packet §4, "Arms that stayed GREEN") | **closed** (residue: notice) |
| G-005 | (a) the gate transcript's header; (b) captures' producer; (c) `.gitattributes` | (a) `p4-gate2.txt` now carries the command, the tree and the executor; iteration 1's `p4-gate.txt` does not, and its digest is recorded here. (b) the producer of `captures/close-*` is still unnamed, and two of them are now stale (G-009). (c) `.gitattributes` is still in no packet | **open — minor**, close record |
| G-006 | fold the ux P4 walkthrough | iteration 1's walkthrough is on record (FAIL, UXV3-1). The re-walk is **not on record** at this write | **open — pending** |
| G-007 | the `up` re-flow, as an operator question | the ux walkthrough raised it as UXV3-3 (major, operator question). Increment 003 §6 routes it to close | **routed** — operator |

### Layer 0 — unit

The criterion and the C-51 exclusions are unchanged from iteration 1. New this iteration: **the cut** in `_kanban_grouped` (`views.py:4700`, CC ≥ 3: room < 3, the selection inside or outside the band, rail-title rounding, kept-all vs folded). `_fold_row` (`:4828`) gained the `cut` argument and the in-band counts.

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| the 8 units of iteration 1 (`_kanban_widths`, `_wrap_title`, `kanban_card`/`_card_meta`, `_literal`, `_due_fact`, the cap arithmetic, `_project_tags`, `_fold_row`) | as iteration 1 | as iteration 1 | pass (gate re-run) |
| the cut in `_kanban_grouped` | CC ≥ 3 (the window arithmetic `3j + 2`, the card boundary, rail rows every 2) | `test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection`, `test_TC_311_the_cut_keeps_every_count_and_whole_cards` | pass (gate re-run) |
| `_fold_row` + cut | CC ≥ 3 (which side, clip order ▲ names → cut name → ▼ list); user text | the two above + `test_TC_311_the_board_folds_whole_bands_and_names_them` | pass (gate re-run) |

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| the cut | C1 no cut · C2 the cut ignores the selection · C3 not on a card boundary · F1 an exact fit cut · F3 a lone first row | yes, all 5 (C1 5 of 7 arms; C2 4 of 6; C3, F1, F3 on the cut nodes) | `evidence/inc003-mutations-r2.txt` (software-dev); `qa-p4b/qa-mutations-inc003.txt` (qa, byte-identical) |
| `_fold_row` + cut | C4 the cards above not counted · C5 no fold row for a cut alone · F2a, F2b counts clipped · F5 rail titles counted · F10 one-sided `▲` loses its names | yes, all 6 | same |
| `_literal` at the shared seat | C6 `title_markup` back on `escape` | yes, 5 of 5 arms | same |

### Layer A — functional (white-box): per-requirement results

Every "pass" is `executed` by the orchestrator (`evidence/p4-gate2.txt`). Probe rows are `executed` by qa-reviewer. **Rows whose evidence changed since iteration 1 are spelled out. The other rows hold as iteration 1 recorded them, with their nodes green again in the re-run.**

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-301 | test | AT-301 ×3; TC-302 ×48, TC-303 | as iteration 1 | pass | gate re-run. Readability unchanged: `readability-close.txt` regenerated byte-identical by qa (11.8 / 13; 6.2 / 3) |
| HLR-302 | test | TC-304 ×7, TC-305, TC-301 window | as iteration 1 | pass | gate re-run |
| HLR-303 | test | AT-302; TC-306 ×4; `test_kanban_groups_by_project` (rewritten) | as iteration 1, now naming the `at risk` limit | pass | gate re-run. `at risk` is asserted on an in-memory status the shipped model cannot hold (D-315, LED .19): unreachable through the app, routed as an operator question (G-008) |
| HLR-304 | test | AT-302; TC-307 ×3 | as iteration 1 | pass | gate re-run |
| HLR-305 | test | AT-303; TC-308 ×7; TC-301 ×62 | as iteration 1 | pass | gate re-run; the 80×24 tag clause is still without a node (G-002) |
| HLR-306 | test | AT-304; TC-309 ×15 | as iteration 1 | pass | gate re-run |
| HLR-307 | test | AT-305 | selection on `to3` (amended, G-003b) | pass | gate re-run. The threshold text and the AT now agree. `-k budget` selects 0 nodes (G-010) |
| HLR-308 | test | AT-306; TC-310 | as iteration 1 | pass | gate re-run |
| HLR-309 (amended, LED .18) | test | AT-307 ×5; TC-311 ×9 | the approved frames; the walk at 118×30/80×24; **`g g` at 80×24 and the 14-high board at 118×30 / 80×24: the panel never scrolls, the selected card is whole**; h 0 no fold | pass | gate re-run. RED on the increment-002 tree: AT-307 horizon + both 14-high arms and the cut node (`inc003-red.txt`, `4 failed, 9 passed`; the `td3` arm reports `('td3', 28)` rows at h 22). qa app walk: 0 violations in 168 down/up steps over 6 cases, 2 of them beyond the AT (80×22, 80×20). Captures 118×30 / 80×24 unchanged (qa regeneration) |
| HLR-310 | test | AT-308 ×3; TC-312 ×3 | as iteration 1 | pass | gate re-run. `-k unseen` selects 0 nodes (G-010) |
| LLR-301.1 | test (unit) | TC-301 ×62 | as iteration 1 | pass | gate re-run |
| LLR-301.2 | test (unit) | TC-302 ×48 (43 + the 5 title seats), TC-303 | 58 / 24-char literals (amended); the shared seat (LED .20) | pass | gate re-run; the seat nodes are RED on base, and C6 is KILLED (qa re-run) |
| LLR-301.3 | test (unit) | TC-313; shipped WIP nodes | as iteration 1 | pass | gate re-run |
| LLR-302.1 | test (unit) | TC-304, TC-305 | as iteration 1 (LED .17) | pass | gate re-run; LED .17's measurement on disk and reproduced (G-001 closed) |
| LLR-303.1 | test (unit) | TC-306 ×4 | as iteration 1 | pass | gate re-run |
| LLR-304.1 | test (unit) | TC-307 ×3 | as iteration 1 | pass | gate re-run |
| LLR-305.1 | test (unit) | TC-308 ×7 | as iteration 1 | pass | gate re-run |
| LLR-306.1 | test (unit) | TC-309 ×15 | as iteration 1 | pass | gate re-run |
| LLR-308.1 | test (unit) | TC-310 | as iteration 1 | pass | gate re-run |
| LLR-309.1 | test (unit) | TC-311 ×7 (iteration-1 nodes) | as iteration 1 | pass | gate re-run |
| **LLR-309.2 (NEW, LED .18/.21)** | test (unit) | `test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection`, `test_TC_311_the_cut_keeps_every_count_and_whole_cards`; AT-307's horizon and 14-high arms | 80×22 horizon `td3` → 22 rows, `▲ 3 more in Later` / `▼ 1 more in Later`; `td5` → `▲ 5 more in Later`; h 0 25 cards; exact fit not cut, one row less is; counts print with the cut band last and with a 34-char name; no lone first row at 80×24 / 80×23 / 118×22; rail-title rounding; counts + drawn = open cards | pass | gate re-run. Every clause is a literal in the two nodes (`test_kanban_readable.py:1145–1232`, read by qa). RED: `inc003-red.txt` (cut node) and `inc003-red-r1.txt` (`the_cut_keeps…` RED on the round-1 code, `1 failed, 6 passed`). 11 mutants KILLED (qa re-run). The boundary room < 3 (drawn alone, scrolls) is declared, not tested. `-k taller_than` selects 1 of its 2 nodes (G-010) |
| LLR-310.1 | test (unit) | TC-312 ×3 | as iteration 1 | pass | gate re-run. `-k unseen` selects 0 nodes (G-010) |

### Layer B — behavioral (black-box) acceptance

C-18: one on-disk function per AT (`grep "def test_AT_30" tests/*.py` finds 8 functions, all in `tests/test_kanban_readable.py`). AT-307 is re-parametrised in place (5 arms), not split into a second function.

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-301 | AT-301 | as iteration 1 | as iteration 1 | ✓ · ✓ · ✓ | pass |
| US-301..303 | AT-305 | key `4`; selection `to3` | spans + compositor strips | ✓ · ✓ · ✓ | pass |
| US-302 | AT-302 | as iteration 1 | as iteration 1 | ✓ · ✓ · ✓ | pass |
| US-302, US-303 | AT-307 `test_AT_307_the_selected_card_is_always_whole_on_screen` ×5 | `TaskboardApp` keys `4`, `g g`, `down` at terminals 118×30, 80×24; oracle and 14-high boards. The start selection `tw5` is set as a fixture | `#viewport.scroll_offset.y == 0`, painted rows = viewport height, both rows of the selection inside, its own band rule above it, the band set unchanged on a `down` into a drawn band | ✓ · ✓ (80×24 under horizon; 14 highs) · ✓ (horizon + 14-high arms RED on the 002 tree; all 5 RED on base; C1/C2 KILLED) | pass |
| US-302 | AT-308 | as iteration 1 | as iteration 1 | ✓ · ✓ · ✓ | pass |
| US-303 | AT-303 | as iteration 1 | as iteration 1 | ✓ · ✓ · ✓ | pass |
| US-303 | AT-304 | as iteration 1 | as iteration 1 | ✓ · ✓ · ✓ | pass |
| US-301..303 | AT-306 | as iteration 1 | as iteration 1 | ✓ · n/a — copy · ✓ | pass |

### Bidirectional surface-reachability matrix (extends A-5) — changes since iteration 1

All iteration-1 rows hold. The rows that changed:

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | group mode `horizon` with a band taller than the room | `kanban_group`, `height` | yes (`g g` at 80×24) | AT-307 arm 3 | ✓ |
| input | a board of 14 highs walked by `down` | board, `selected_id` | yes (118×30, 80×24) | AT-307 arms 4–5 | ✓ |
| input | `up` across a cut band | `selected_id` | not in an AT; qa app walk: 84 `up` steps over 6 cases, 0 scroll or half-card violations | qa probe | ✓ (the re-flow on `up` is UXV3-3, an operator question) |
| output | the cut fold row `▲ k more in NAME` / `▼ m more in NAME` | `_fold_row(…, cut)` | painted through the app (qa walk) but not asserted by AT-307; the text is asserted at the render seat | TC-311 ×2 | ✓ |
| output | the shared title seat (agenda, matrix, lanes, Focus) | `title_markup` → `_literal` | at the render seat (`render_view`), not via key | TC-302 seat ×5 | ✓ below the app; the seats are shipped renders |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| `1677` | `0` | `178` | `1855` | `1855` | `n/a — no slow marker` / `1854 passed + 1 failed` | yes |

- Increment 003: `1845 − 0 + 10 = 1855`. The 10: AT-307 +3 arms, TC-311 +2 (the cut nodes), TC-302 +5 (the title seats). The two G-004 nodes are rewritten in place, net 0. qa's collect-only in `tests/test_kanban_readable.py` gives 178 = 168 + 10, with TC-311 9 and TC-302 48. No node was deleted.
- Gate re-run: 1854 passed + 1 failed = 1855 = collected. The failed node is the clipboard node (G-011), which is pre-existing and outside the batch's diff.

### Packet claims re-read — increment 003 (each against its transcript)

| Claim (packet) | Transcript | Holds? |
|---|---|---|
| RED on the 002 tree: 4 failed (AT-307 horizon + both 14-high arms, the cut node), 13 arms resolved | `inc003-red.txt`: `4 failed, 9 passed, 326 deselected`; the FAILED lines name exactly those 4; the 9 PASSED are the 2 oracle AT-307 arms, the 5 seats and the 2 G-004 nodes | ✓ |
| RED on base: 11 failed (incl. the 5 title seats) | `inc003-red-on-base.txt`: `11 failed`, 5 AT-307 + 5 seats + the cut node | ✓ (qa reproduced the seats' `a[b`) |
| instrument RED-proof: "FAILED on `td3`" | `inc003-red.txt`: `AssertionError: ('td3', 28)` | ✓ |
| round-1 node RED on the round-1 code | `inc003-red-r1.txt`: `1 failed, 6 passed` (`the_cut_keeps_every_count_and_whole_cards`) | ✓ |
| 12 distinct mutants, 12 KILLED on the final tree; C3, C5 survived round 1 | `inc003-mutations.txt` "4 of 6 KILLED" (C3, C5 SURVIVED); `-r1.txt` 2 of 2; `-r2.txt` 10 of 10 + 2 of 2, restore `e46de44c…` OK | ✓ (qa's re-run byte-identical) |
| emitted form: 22 rows at 80×22, `▲ 3 more in Later` / `▼ 1 more in Later` | TC-311 node literals (`:1154–1159`) | ✓ (inspection + gate) |
| 14 evidence files with digests | sha256 re-check | ✓ (14 / 14) |
| signed ledger `1855 = 1845 − 0 + 10` | collect-only 1855 | ✓ |
| gate: "1854 passed, 1 failed in 325.57 s — the clipboard flake" | `inc003-green.txt` tail | ✓ |
| B1 reverse census: "the gate run: every node green" | `inc003-green.txt` has 1 failed (clipboard) | ⚠ wording only. The failure is not a product node and is disclosed in §4 of the same packet |
| correction population: 2 sites, `test_kanban_shows_every_task_in_its_phase` left | diff of `test_app.py:1486–1533` | ✓ |
| SOURCE 1/4 (`views.py`) | `git diff` timestamps: `app.py` unchanged since 17:47:58 (`7c1410e8…`); `views.py` edited | ✓ |
| §6.5 / LED .18, .19, .20, .21; D-314b (PV-9), D-315 (PV-10) | `01-requirements.md` §6.2, §6.5; ledger headings `.18`–`.21`; `PLAN.md` PV-9, PV-10 | ✓ |
| the requirement count | `01-requirements.md` §3–§4: 10 HLR, 12 LLR (LLR-309.2 new) | ✓ |

### Gaps detected (iteration 2)

| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-002 | HLR-303, HLR-305, HLR-306, LLR-302.1, LLR-303.1 | carried unchanged from iteration 1 (the threshold clauses with no node or a weaker node) | minor | ⏸ DEFER to BACKLOG with iteration 1's row as the reason, or a tests-only pass |
| G-005 | record | (b) the producer of `captures/close-*` is unnamed; (c) `.gitattributes` (+1 line) is in no packet. (a) is fixed for `p4-gate2.txt` | minor | orchestrator records it in the close artifact |
| G-006 | HLR-309 (trigger D) | the ux re-walk of UXV3-1 is **not on record** at this write; the iteration-1 ux FAIL stands until it lands | major (pending, not a defect) | fold the ux verdict before the P4 gate decision |
| G-008 | HLR-303 (D-315, LED .19) | `at risk` cannot reach the screen through the app (`PROJECT_STATUSES` has no `at_risk`). The clause passes only on an in-memory status. Declared and routed (UXV3-2) | notice | operator question at close (already routed) |
| G-009 | HLR-309 / §6.1 | **Stale captures.** `captures/close-kanban-ops-80x24.txt` (sha256 `9ab88717…62bb`) and `-ops-80x22.txt` (`4d180178…f8b1`) were written at 19:00. Their last row reads `▲ 4 above` with no names. That is the round-1 state that code review F10 flagged, before the fix at 19:29. The frozen tree paints `▲ 4 above: Website Redesign (5 open), Mobile App (5 open), API Platform (6 open…`, as the increment-001 capture did. qa regenerated all 16 with `evidence/capture.py`, and the other 14 are byte-identical. The matching `.svg` files are presumably stale too (not compared). §6.1 has the operator read these captures | minor | regenerate `captures/close-*` on the frozen tree before close, name the producer, and digest them in the close record |
| G-010 | HLR-307, HLR-309, HLR-310, LLR-309.1, LLR-309.2, LLR-310.1 | **The *Executed verification* commands do not select their nodes.** On the frozen tree: `-k budget` (HLR-307) selects **0** (pytest exit 5); `-k unseen` (HLR-310, LLR-310.1) selects **0**; `-k fold` (HLR-309, LLR-309.1) selects 2 TC-311 nodes and neither AT-307 nor the cut nodes; `-k taller_than` (LLR-309.2) selects 1 of its 2 nodes; `-k band_rule` misses AT-302. Results stay traceable through the node ids in this record and the full gate run. **Iteration 1 missed this**; the HLR-307 and HLR-310 commands were already wrong then | minor | record fix at close: replace each command with its node ids, or with a `-k` that collects them (e.g. `-k "AT_307 or TC_311"`) |
| G-011 | §5.2 ("full suite: 0 failures") | the gate re-run has 1 failed node, `test_app.py::test_win_clipboard_roundtrip`, which failed at its SETUP (`Set-Clipboard` failed). The cause is the environment: 0 batch lines touch it, it passed on base and in 3 earlier batch runs, and `PENDING.md` #22 tracks it. The exit criterion is not literally met | minor (environmental) | the orchestrator re-runs that ONE node when the clipboard is free and records it, or the operator accepts it at close with this row as the reason. PENDING #22's fix (a `skipif` or a mock) stays in BACKLOG |
| G-012 | HLR-309 (amended) | §6.3 *Open risks* still says "A band taller than the panel … is drawn alone and scrolls; its row 2 can then fall below the fold", and `PLAN.md` *Risks* says "A card's row 2 can fall below the fold". Both describe the deleted behaviour. The live residual is only room < 3 (LLR-309.2's boundary). G-004(c) left a residue too: `test_kanban_shows_every_task_in_its_phase`'s docstring is still unqualified | notice | reword both at close |

**The ux findings routed by increment 003 §6** (UXV3-2..UXV3-11) are the ux-reviewer's. qa does not re-grade them; G-007 and G-008 point at the two that touch qa's rows.

### Escaped-bug regression

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| TC-302 shared title seat ×5 (the shipped `title_markup` defect, G-003a) | `inc003-red-on-base.txt`: 5 FAILED on `13745f6`; qa reproduced `a[b` in 5 of 5 seats on base | value (`a[b` printed for the literal) | yes: asserts the literal title in the plain text; C6 (`escape`) reddens 5 of 5 | pass (gate re-run) | `test_TC_302_the_shared_title_seat_prints_a_backslash_before_a_bracket[*]` |
| AT-307 horizon / 14-high arms + TC-311 cut (UXV3-1, escaped P3 into P4) | `inc003-red.txt` on the increment-002 tree: 4 FAILED (`('td3', 28)` rows at h 22) | shape (render taller than the panel, viewport scrolled) | yes: exact row count, `scroll_offset.y == 0`, the fold row's counts literal | pass (gate re-run) | AT-307 arms 3–5; TC-311 cut ×2 |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

1. ✓ **Acceptance criteria use Given/When/Then** — n/a by design: EARS statements plus numeric thresholds per HLR, accepted at P2 (`02-review.md`). LLR-309.2 follows the same form (`01-requirements.md:385–394`).
2. ✓ **Test cases have explicit Expected** — every Layer-A row carries its threshold. The new nodes assert literals (`test_kanban_readable.py:1157–1174`, `:1201–1232`, `:1142`).
3. ✓ **Edge cases include empty, boundary, invalid, error** — new boundaries: exact fit vs one row less, room 6 at 80×23, rail-title rounding, the cut band last, a 34-char cut name, one band alone. Invalid: the backslash-bracket title in 5 seats. Error: n/a — no error surface (§6.4). Room < 3 is declared, not tested.
4. ✓ **Regression checklist exists** — the B1 census per increment, the gate re-run (every product node green), and qa's capture regeneration (14 of 16 identical; G-009 names the 2 that differ).
5. ✓ **Exit criteria stated** — `01-requirements.md` §5.2. This record applies them; the "0 failures" item is not met for an environmental node (G-011).
6. ✓ **No real PII / secrets** — the oracle board and synthetic boards only. A home-path grep over `.dev-flow/2026-10-02-batch-03/` gives 0 hits. This record cites the scratch as `%TEMP%\claude\<session>\…`.
7. ✓ **Mode declared** — `validation`, iteration 2, at the top of this file.
8. ✓ **Validation mode: every case carries a result or a state, and each executed result names its executor** — the gate re-run: orchestrator. Increment runs: software-dev. Code review: the reviewer's statement. ux iteration 1: ux-reviewer, relayed. ux re-walk: `not-run` (pending). qa probes: qa-reviewer. The clipboard node: `failed`, orchestrator, environment. G-001's untraceable citation is now traced.
9. ✓ **Layer B (black-box)** — 3 of 3 stories observed through `App.run_test`. AT-307 has 5 arms covering UXV3-1's three reproductions, with boundary and negative evidence. C-18: 8 functions for 8 ATs.
10. ✓ **Bidirectional surface-reachability** — the iteration-1 matrix plus the changed rows above. `up` across a cut and the cut fold row's text were observed through the app by qa's walk.
11. ✓ **No unfilled template** — no `<...>` placeholder, no unassigned id, and no empty Steps or Expected in the iteration-2 section. The literal `<session>` and `<reason>` are a redaction and the state vocabulary, not placeholders.

---

# Superseded — iteration 1

> **Superseded by iteration 2 above (2026-10-02).** Kept verbatim as history. Its verdict, Layer 0 and checklist lines are not the gate. Its gap table is re-read row by row in iteration 2 §*Iteration-1 gaps*.

# Validation — taskboard — Batch 2026-10-02-batch-03

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1 and **names who executed each one**. The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Mode: validation.** Author: `qa-reviewer` (a named sub-agent following `agents/qa-reviewer.md`, flow pinned to rev98), 2026-10-02. Iteration 1.
>
> **Who executed what.**
> 1. **The gate run** was **launched and collected by the orchestrator** (C-25) on the frozen tree after increment 002: `python -m pytest -q -p no:cacheprovider` → **1845 passed in 306.00 s** (`evidence/p4-gate.txt`, sha256 `6d1533f8…cbda04b9`). I read the summary line from that run's own output. I did not run the suite. The command is the CI's command (`.github/workflows/ci.yml`: `python -m pytest -q`) with the cache plugin off. The project has no `slow` marker, so the lean and full counts are the same run.
>    **Revision check (`executed` by qa-reviewer):** the transcript was written at 18:11:39. `find taskboard tests -newer evidence/p4-gate.txt` returns nothing. The newest edits are `tests/test_kanban_readable.py` at 17:48:28 and `taskboard/app.py` at 17:47:58. The run therefore postdates every edit. In a scratch copy of the tree, `pytest --collect-only -q` gives **1845 collected** (168 of them in `tests/test_kanban_readable.py`). The copy's `views.py` and `app.py` hash to `39a81dbc…` and `7c1410e8…`, the restore digests in increment 002's batteries.
> 2. **The base run** (`evidence/base-suite.txt`, **1677 passed in 237.82 s**, P-8 at `13745f6`) was recorded at P1. Its executor is not named in the record.
> 3. **The RED counterfactuals, mutation batteries, reverse-census runs and per-increment green runs** were **executed by the increment author** (`software-dev`): `03-increments/increment-00{1,2}.md` and `evidence/inc00{1,2}-*.txt`. The code-reviewer's own batteries (20 + 11 mutants in increment 001, 12 + 3 in increment 002, plus a 46-case probe) are as stated in each packet's §4b. They are not on disk, so I cannot trace them, and I cite them only as the reviewer's statement.
> 4. **The close captures** (`evidence/captures/close-*`, `readability-close.txt`) are on disk. Only the two 14-high frames carry a packet digest (increment 002). The producer of the others is not named in the record (G-005).
> 5. **My own checks.** Each was `executed` by qa-reviewer and is read-only toward the repo. Probes ran in `%TEMP%\claude\<session>\scratchpad\qa-p4\` against a copy of the frozen tree (`tree\`) and a `git archive 13745f6` copy of the base (`base\`):
>    - I verified the 34 evidence digests the two packets cite against the bytes on disk: **34 / 34 OK**.
>    - I re-read every count claim in the packets against its transcript (see §Packet claims re-read).
>    - I **re-ran all 43 recorded mutants (M1–M20, R1–R8, Q1–Q15) on the FROZEN tree with the FINAL tests**: **43 of 43 KILLED**, every restore digest OK (`qa-mutations-final.txt`, sha256 `1881a114…`). The increment-001 battery ran on a pre-002 `views.py` (`9b59f9ad…`) and the pre-rewrite AT-307. This run shows that the kills still hold after 002, including M11 against the rewritten AT-307 (both arms RED).
>    - I wrote and ran 3 Layer-0 mutants of my own: QA-L1 and QA-L2 on `_literal`, QA-D1 on `_due_fact`. All 3 were KILLED (`qa-mutations-layer0.txt`, sha256 `b5293afc…`).
>    - Probes (`probe1..7.py` and their `-out.txt`):
>      - the width law at every width 24..160 × h {0, 24, 30} × 3 group modes;
>      - tags at 118×30 / 80×24 / 80×22;
>      - the oracle at 80×19;
>      - the WIP tone;
>      - a stale-node geometry check;
>      - band re-flow on `up` / `down`;
>      - a re-derivation of LED .17's 5.3;
>      - base readability on the base tree;
>      - the approved frames `out/R-1b-*.txt` against `captures/close-*`;
>      - `title_markup` on the base tree against the frozen tree.
>    - **These probe transcripts live in the session scratchpad, outside the declared evidence home.** The orchestrator may copy them into `evidence/` if the gate wants them on record.
> 6. **The UX walkthrough** (trigger family D fired) is owed to the `ux-reviewer` at P4 (§6.1, plus the carried UX-9, UX-10, UX-11 and the P2 discharge's `up` observation). **It is not on record at the time of this write. It is `not-run` here and is not counted as evidence** (G-006).
>
> **Result states** in this file use the seven words: `planned` · `executed` · `approved` · `failed` · `blocked` · `not-run` · `n/a — <reason>`. Every node marked "pass" below was `executed` by the orchestrator in the gate run: 1845 collected = 1845 passed, 0 failed, 0 skipped.

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

- **Result:** `PASS-WITH-NOTES`
- **Layer 0:** `8 unit(s) met the criterion · 8 carry a named reddening mutation` (all KILLED on the frozen tree. `_literal` had no named mutant in either packet; QA-L1 and QA-L2 supply one, see §Layer 0)
- **Requirements:** `21`/`21` pass (10 HLR + 11 LLR; every node green in the orchestrator's gate run) · `0` blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (`App.run_test`, real keys, painted `#board` / compositor strips / `Label`s / `Toast`), with boundary and negative arms. US-301..303 are all observed. **C-18 ✓:** AT-301..AT-308 each realise in exactly ONE on-disk function (`tests/test_kanban_readable.py`, 8 `def test_AT_30N` functions, none elsewhere under `tests/`). Each AT is RED on base, except AT-308's 118×30 no-move arm, which is a declared policy arm.
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables are reached/observed at the surface · `0` gaps (2 threshold clauses are observed only below the surface or in a capture, G-002)
- **Supersession inspection (read off the P3 packets):** ⚠ live dependency found. No product code depends on a superseded law. Two shipped nodes, however, still assert a superseded law or geometry and pass by coincidence, and D-313 names a node as "rewritten" that was left untouched (G-004). The shared `title_markup` also changed behaviour outside scope (G-003).
- **Test ledger:** ✓ reconciles (`1677 − 0 + 168 = 1845`; collected 1845 = passed 1845 in the gate run)
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 10 of 11 rows ✓ with evidence` (✗: row 8, because one executed claim in the record cites a transcript that does not exist, G-001)

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

> **Why PASS-WITH-NOTES and not PASS or FAIL.**
> - **Not FAIL:** no blocker. Every HLR/LLR has a green node and every story has a single-node black-box AT. The readability thresholds are met and independently re-measured. All 43 recorded mutants plus 3 of mine are KILLED on the frozen tree.
> - **Not PASS — three majors and one pending act:**
>   - **G-001:** LED .17 / §6.5 cite an "executed" transcript, `evidence/inc001-widths.txt`, that is not on disk. The number reproduces, but the citation is false.
>   - **G-003:** the shared `title_markup` now prints trailing-backslash titles correctly on 10 shipped call sites outside the declared scope. This is an escaped-defect fix with no shipped-surface regression that fails before the fix.
>   - **G-004:** supersession leftovers.
>   - **G-006:** the ux-reviewer's P4 walkthrough is not on record.
>   - **Recommended route:** one short P3 pass, tests and record only, for G-001, G-003 and G-004. Then fold the ux verdict. **The user decides** (station: "otherwise, user decides").

---

## Detail (reference)

### Layer 0 — unit

Criterion: cyclomatic complexity ≥ 3, or user (file-derived) text crossing into markup. Excluded per C-51:
- the `KANBAN_*` constants and the `KanbanBand` / `KanbanPlan` records (constructors that only assign);
- `kanban_nav`, a pure delegation to the plan;
- the help and legend copy (lookup text, covered at Layer A by TC-310).

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `_kanban_widths` | CC ≥ 3 (fallback, remainder loop) | `test_TC_305_the_columns_are_sized_by_their_titles` | pass (gate) |
| `_wrap_title` | CC ≥ 3 (word cut, over-wide first word) | `test_TC_302_a_card_is_two_rows_of_exactly_its_width[0..40]`, `test_TC_302_the_title_wraps_on_a_word_and_the_rest_sits_under_it` | pass (gate) |
| `kanban_card` (+ `_card_meta`) | CC ≥ 3 (badge ≥ 9 cells, rest / no rest, shed order) | `test_TC_302_*`, `test_TC_303_the_due_token_is_the_last_fact_to_go`, `test_TC_307_the_secondary_limbs_hold` | pass (gate) |
| `_literal` | user text → markup (C-17); CC ≥ 3 | `test_TC_302_a_card_is_two_rows_of_exactly_its_width[*]` (hostile set), `test_TC_307_a_full_rail_counts_what_it_cannot_draw` | pass (gate) |
| `_due_fact` | CC ≥ 3 (late / today / ≤7 / >7) | `test_TC_306_each_project_is_named_once_by_a_band_rule` | pass (gate) |
| the cap arithmetic in `kanban_plan` (`R`, `K`, `3m − 1 ≤ R`) | CC ≥ 3 | `test_TC_309_the_cap_is_two_thirds_of_the_body[h ∈ {0,11,12,13,14,19,20,22,24,30}]` | pass (gate) |
| `_project_tags` | CC ≥ 3; user text | `test_TC_308_tags_tell_projects_apart_and_print_literally` | pass (gate) |
| `_fold_row` | CC ≥ 3 (both sides, clip keeping counts); user text | `test_TC_311_every_selection_is_drawn_inside_the_panel[*]`, `test_TC_311_a_hostile_name_folds_literally_and_an_exact_fit_folds_nothing` | pass (gate) |

**Measured by mutation, never by line coverage.** Every row was re-run by qa-reviewer on the FROZEN tree with the FINAL tests. Restore digests were OK every time (`views.py` `39a81dbc…`, `app.py` `7c1410e8…`).

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `_kanban_widths` | M5 equal widths (`distribute`) | yes: TC-305, TC-304 arms, AT-301 ×3 | `evidence/inc001-mutations.txt` (software-dev); `qa-p4/qa-mutations-final.txt` (qa) |
| `_wrap_title` | M2 no word wrap (one-row title cut with `…`) | yes | same |
| `kanban_card` / `_card_meta` | M3 `⛓N` after the due · M18 the rest kept with no room · R5 badge from 8 cells | yes (TC-303 at `wc` 14, TC-302, TC-307 limbs) | `inc001-mutations.txt`, `inc001-mutations-tail.txt`; `qa-mutations-final.txt` |
| `_literal` | **QA-L1** tag-shaped `[` treated like any `[` (`k + 1`) · **QA-L2** trailing backslash run not doubled | yes: QA-L1 33 of 64 arms red; QA-L2 2 of 64 red (TC-302 hostile arms) | `qa-p4/qa-mutations-layer0.txt` (qa-reviewer). Neither packet names a `_literal` mutant; M1 bypasses the call in `_title_piece` instead |
| `_due_fact` | M14 the near due in the accent · **QA-D1** `n < 7` (the +7 boundary) | yes: M14 → AT-305, TC-306; QA-D1 → TC-306 | `inc001-mutations.txt`; `qa-mutations-layer0.txt` |
| the cap arithmetic | Q1 no cap · Q2 `K = R // 3 + 1` · Q3 the half-body cap | yes: TC-309 h-table arms, AT-304 | `evidence/inc002-mutations.txt`; `qa-mutations-final.txt` |
| `_project_tags` | M17 first word always · R8 tags by characters | yes: TC-308 tags | `inc001-mutations-tail.txt`, `inc001-mutations.txt`; `qa-mutations-final.txt` |
| `_fold_row` | M13 the `▼` side clipped · R3 unescaped · R4 one row early | yes: M13 on 80×24 / 80×22 / 40×22 (118×30 green by design); R3, R4 | `inc001-mutations.txt`; `qa-mutations-final.txt` |

### UX walkthrough — only if trigger family D fired

Trigger family D fired (`state.json` `triggers.fired`). The criteria below come from the HLRs' observable outcomes. They are driven by the ATs in the gate run.

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| Key `4` at 118×32 / 80×26 / 80×24 → two-row cards with `┈` between them, unequal columns, readable titles | `App.run_test`, `pilot.press("4")`. The start selection is set directly, as a fixture, not as the interaction under test | `#board.render()` rows; readability on the painted body | pass (AT-301 ×3) |
| `4`, `right` ×4, `z`, `g` ×2, `v`, and 80×26 → band rules name projects once; DONE is a rail; collapse gives `✓3`; horizon bands appear; archived cards show | real keys | painted rows | pass (AT-302) |
| `down`, `!`, `g`, `s` → the high band is first, the cursor walks it, `!` lifts a card into the band | real keys | painted rows, `_line_map`, `_nav_columns()` | pass (AT-303) |
| `down` on a 14-high board → `+8 more ↓`, a project still on screen, every overflow high reachable | real keys | painted rows, `_line_map` | pass (AT-304) |
| Key `4` → no accent, soon amber, late red, `┈` in the frame tone, selection reverse | real key | `#board` spans plus compositor strips (`seg.style.reverse`) | pass (AT-305) |
| `?` → the help describes the band rule, `┈`, the rail, `more ↓` and the project band | real keys | painted `Label`s of the `HelpScreen` | pass (AT-306) |
| `down` the whole Backlog at 118×30 / 80×24 → the selected card is whole on screen under its band rule, and a `down` into a drawn band moves no band | real keys | viewport `scroll_offset`, painted rows | pass (AT-307 ×2) |
| `]` at 80×24 → the cursor lands on the neighbour, the toast names the title, `u` undoes; at 118×30 → no move, nothing posted | real keys | `_notifications`, `_line_map`, toast render (TC-312) | pass (AT-308 ×3) |
| **`up` into a band already drawn** (P2 discharge observation) | — | — | **`not-run` through the app.** A qa probe on the render seat finds the board re-flows: 16 transitions over 4 sizes, e.g. 118×30 col 0 `to4 → td5` gives `[API, DW, Ops] → [Mobile, API, DW]`. This is spec-conformant (HLR-309's window rule). It goes to the ux-reviewer and the operator (G-007) |

**Mechanism used:** `the UI framework the UI test driver` (Textual `App.run_test`), plus artifact-on-disk captures (`evidence/captures/close-*.txt|svg`) for the operator's read.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — by the ATs in the orchestrator's gate run (1845 passed) |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | not performed — at the time of this write, the ux-reviewer's P4 walkthrough (§6.1; carried UX-9, UX-10, UX-11 and the `up` re-flow) is not on record. It is owed before the P4 gate (G-006) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — §6.1 plans for the operator to read the captures before the push, which happens outside the batch. A driver run and an expert read are not users |

- **Method:** automated, with `pilot.press` key sequences per AT and assertions on the painted widget output. No human operated the app inside the batch.
- **Participants or population:** none (no evaluation with users happened).
- **Evidence of the evaluation:** `evidence/p4-gate.txt` (the AT nodes' green run); the AT bodies in `tests/test_kanban_readable.py` lines 659–1014; the captures in `evidence/captures/close-*`.
- **Limits:** the ATs assert what their authors chose. The `up` direction, `left`/`right` re-windowing (UX-11), `]` into a capped column (UX-9) and filter edge cases (UX-10) are not walked through the app. Some ATs set the start selection directly, which is a fixture and not the interaction under test. Colour is asserted on spans, not on a viewed terminal.

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

Every "pass" below is `executed` by the orchestrator (`evidence/p4-gate.txt`, 1845 passed). Probe rows are `executed` by qa-reviewer.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-301 | test | AT-301 ×3; TC-302 ×43, TC-303 | panel 118×30 avg ≥ 11.0, ≥ 12 full; 80×24 ≥ 5.5; every card two consecutive rows | pass | measured **11.8 / 13** (118×30) and **6.2 / 3** (80×24), against base 7.3 / 0 and 1.0 / 0 (`captures/readability-close.txt`, `readability-base.txt`). qa re-measured both on the frozen and base trees (probe4, probe5): identical |
| HLR-302 | test | TC-304 ×7, TC-305, TC-301 window | rows = w at 7 widths; one `┈` between cards; adaptive; ≥ MIN_COL; 8 phases at 80 | pass | gate; qa probe1: rows = w at **every** width 24..160 × h {0, 24, 30} × 3 group modes, 0 violations |
| HLR-303 | test | AT-302; TC-306 ×4 | 5 rules; Website `5 open · 2 high ↑ · project due +10d`; API `at risk`; `┼` past text | pass | gate. Weak clause: "one rule per non-empty group" under priority/horizon is asserted only as a subset (G-002) |
| HLR-304 | test | AT-302; TC-307 ×3 | `✓ DONE 3`, `✓ Design homepa…` / `done 18d ago`; `✓3` / `✓1` / `18d ago`; nav last column; `+2 more`; 99/100 | pass | gate |
| HLR-305 | test | AT-303; TC-308 ×7; TC-301 ×62 | 9 highs first; `9 open · 4 projects`; tags = frame (8 of 9) at 118; at 80×24 a tag exactly when the shed order leaves room; 60-arm nav = draw order | pass | gate. **The 80×24 tag clause has no node** (G-002). qa probe1 + the `close-kanban-80x24.txt` capture: 2 of 9 tagged; every untagged card has a title rest that takes the room, consistent with HLR-305 "after the title's rest and the due token" (inspection). Hue asserted for `Ops` only |
| HLR-306 | test | AT-304; TC-309 ×15 | R table; 14-high: 6 + `+8 more ↓` at 118×30, 4 + `+10` at 80×24; 80×19 oracle 3 + `+1`, `to5` in Ops | pass | gate. The 80×19 specifics are asserted only as "capped or not" (G-002). qa probe1: shown `tw5 tm4 ta2`, `+1 more ↓`, `to5` in the Ops band ✓ |
| HLR-307 | test | AT-305 | 0 accent; soon amber; late red; Ops `project due +5d` amber; `┈` frame; reverse | pass | gate. The AT selects `to3`, not the `tw3` the threshold names; with `tw3` the Ops band is folded and its due cannot be observed (G-003b) |
| HLR-308 | test | AT-306; TC-310 | `band rule`, `┈`, `rail`, `more ↓`; not `top of each column`; ≤ 44 cells; legend label | pass | gate |
| HLR-309 | test | AT-307 ×2; TC-311 ×7 | 30 rows + the approved fold row; `to3` names above; every `down` whole and in view; both counts at 80×24; h 0 no fold | pass | gate. qa probe6: `close-kanban-118x30.txt` / `-80x24.txt` equal `out/R-1b-*.txt` on every row except the head (rows 1..29 / 1..23; spine glyphs folded to `▊`). This confirms the packet's frame claim |
| HLR-310 | test | AT-308 ×3; TC-312 ×3 | `to3 → ta6`, notification literal, `[b]x[/b]` literal, 118×30 no move, `u` restores | pass | gate |
| LLR-301.1 | test (unit) | TC-301 ×62 (60 arms + guard + window) | 60 arms, guarded board; h 0 equality; ⊆ at 80×24, 140×14, 8 phases | pass | gate; M10 KILLED (41 arms red) |
| LLR-301.2 | test (unit) | TC-302 ×43, TC-303 | both rows `wc` cells at 0..40, hostile set; frame card literal; due survives | pass | gate. Literal drift: the "60-char title" / "20-char word" are 58 / 24 characters (G-003b, trivial) |
| LLR-301.3 | test (unit) | TC-313; shipped `test_kanban_wip_header_*`, `test_kanban_windows_phases_when_they_dont_fit` | head modes; `6/4` in `over`; markers count open phases only; empty line | pass | gate. TC-313 does not assert the tone, but the shipped WIP nodes do (`test_app.py:3071/3078`); qa probe1 shows ` 6/4` painted `#f43f5e` |
| LLR-302.1 | test (unit) | TC-304, TC-305 | widths sum to room at every width 24..160 (amended LED .17) | pass | gate (room sampled every 7). qa probe1: the sum and MIN_COL hold at every width 24..160 |
| LLR-303.1 | test (unit) | TC-306 ×4 | `[b]Odd[/b]` literal; rule = w at 24..160; ±0 / 7 / 8 days | pass | gate (widths sampled); probe1: all widths ✓ |
| LLR-304.1 | test (unit) | TC-307 ×3 | 16 / 7 cells; cap `(cap − 1) // 2`; hostile done title literal at 16 cells | pass | gate |
| LLR-305.1 | test (unit) | TC-308 ×7 | band order = seat under every sort; word-wise tags; `[b]Odd[/b]` | pass | gate |
| LLR-306.1 | test (unit) | TC-309 ×15 | the executed h-table; `3m − 1 = R` shows all, `R + 1` caps | pass | gate |
| LLR-308.1 | test (unit) | TC-310 | as HLR-308 | pass | gate |
| LLR-309.1 | test (unit) | TC-311 ×7 | every task as the selection at 118×30 / 80×24 drawn, exactly h rows; hostile hidden name literal | pass | gate |
| LLR-310.1 | test (unit) | TC-312 ×3 | as HLR-310, plus the reset path (filter, lost id) | pass | gate |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a verification nobody ran. Write your own rows in the table above.

```text
| *(example)* HLR-001 | test | `pytest … -k TC-001` | exit 0 | | |
| *(example)* LLR-001.1 | test (unit) | `…` | `…` | | |
```

### Layer B — behavioral (black-box) acceptance

C-18: one on-disk function per AT (`grep "def test_AT_30" tests/*.py` → 8 functions, all in `tests/test_kanban_readable.py`; collected arms AT-301 ×3, AT-307 ×2, AT-308 ×3, the rest ×1).

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-301 | AT-301 `test_AT_301_cards_read_across_the_column` | `TaskboardApp` key `4` at 118×32, 80×26, 80×24 | painted `#board` rows: two-row cards, `┈`, unequal columns, readability ≥ floor | ✓ · ✓ (80×24, the smallest; no floor there, two-row law only) · ✓ (RED on base, 3 arms) | pass |
| US-301..303 | AT-305 `test_AT_305_the_kanban_spends_no_accent` | key `4` at 118×32, 80×26 | `#board` spans plus compositor strips | ✓ · ✓ (+7 vs +8 via `_due_fact`; `today`) · ✓ (RED on base; M14, M15) | pass |
| US-302 | AT-302 `test_AT_302_projects_are_named_once_and_done_is_a_rail` | keys `4`, `right`, `z`, `g`, `v`, at 118×32 and 80×26 | band rules; rail head `✓ DONE 3` / `✓3`; horizon bands; an archived card | ✓ · ✓ (80 count rail, collapsed) · ✓ (RED on base) | pass |
| US-302, US-303 | AT-307 `test_AT_307_the_selected_card_is_always_whole_on_screen` | keys `4`, `down` at 118×30, 80×24 | viewport offset, the band rule above the selection, the band list unchanged on a `down` into a drawn band | ✓ · ✓ (80×24) · ✓ (RED on base; M11 KILLED on the final node, qa re-run) | pass |
| US-302 | AT-308 `test_AT_308_finishing_a_card_keeps_the_cursor_on_the_board` | keys `4`, `]`, `u` at 80×24, 118×30 | selection in `_line_map`, notification text, phase restored | ✓ · ✓ (column-last `to3`, column-first `tw2`; 118×30) · ✓ (RED on base for the 80×24 arms; Q6, Q7, Q15) | pass |
| US-303 | AT-303 `test_AT_303_the_high_band_is_first_and_the_cursor_walks_it` | keys `4`, `down`, `!`, `g`, `s` | first band `── high  9 open · 4 projects`; walk order; `!` lifts into the band; no band under priority; band order under sort | ✓ · ✓ (group priority) · ✓ (RED on base; M10) | pass |
| US-303 | AT-304 `test_AT_304_a_board_full_of_highs_keeps_its_projects` | keys `4`, `down` on a 14-high board at 118×32 | `+8 more ↓`, a project rule on screen, all 8 overflow highs reached and drawn | ✓ · ✓ (cap) · ✓ (RED on base; Q1–Q4) | pass |
| US-301..303 | AT-306 `test_AT_306_the_help_explains_what_is_drawn` | keys `4`, `?` | painted `Label`s | ✓ · n/a — copy, no width boundary at the AT (the 44-cell bound is TC-310) · ✓ (RED on base and on the 001 tree) | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | terminal size (118×30/32, 80×24/26) | `width`, `height` | yes | AT-301, AT-307, AT-308 | ✓ |
| input | group mode (`g`: project → priority → horizon) | `kanban_group` | yes | AT-302 (horizon), AT-303 (priority) | ✓ |
| input | sort mode (`s`) | `kanban_sort` | yes | AT-303 | ✓ |
| input | show archived (`v`) | `show_archived` | yes | AT-302 | ✓ |
| input | collapse (`z`) | `kanban_collapsed` | yes | AT-302 | ✓ |
| input | project focus | `kanban_focus` | no — not driven by a key in any AT | TC-301 (30 arms with focus on), TC-313 | ✓ below the surface only. Out of the stories' named keys; noted, not a gap |
| input | selection movement (`down`, `up`, `right`) | `selected_id` | `down`, `right` yes; `up` not driven in any AT | AT-303, AT-307, AT-302 | ✓ (`up` → G-007, ux) |
| input | priority cycle (`!`) | task priority | yes | AT-303 | ✓ |
| input | phase move / undo (`]`, `u`) | `action_phase_move` | yes | AT-308 | ✓ |
| input | `/` filter | `search_query` (render h − 2) | set programmatically, not typed | TC-309 filtered ×4, TC-312 filter | ✓ below the surface (D-312) |
| input | help (`?`) | `help_usage` | yes | AT-306 | ✓ |
| output | two-row cards, `┈`, adaptive widths, readability | `kanban_card`, `_kanban_cell`, `_kanban_widths` | yes (painted) | AT-301 | ✓ |
| output | band rules (one per group) | `_band_rule` | yes | AT-302 | ✓ |
| output | DONE rail (titles ≥ 100, count < 100, collapsed) | `_rail_cells` | yes | AT-302, AT-308 | ✓ |
| output | high band, tags | `kanban_plan` (high), `_project_tags` | yes (rule, order); tags 118 ✓; **80×24 tag rule observed only in a capture / probe** | AT-303; TC-308 | ✓ (G-002) |
| output | `+N more ↓` cap row | `kanban_plan` cap | yes | AT-304 | ✓ |
| output | fold row `▲ N above / ▼ M below` | `_fold_row` | observed in the app indirectly (band set, the selection in view); the fold-row text is asserted at the render seat | AT-307; TC-311 | ✓ |
| output | colour budget | spans | yes | AT-305 | ✓ |
| output | help and legend copy | `help_usage`, `legend_entries` | help yes; legend label at the seat (the AT sees "project band" in the help) | AT-306; TC-310 | ✓ |
| output | done notification | `notify(markup=False)` | yes (toast render) | AT-308; TC-312 | ✓ |
| output | cursor relocation off a counted card | `_select_first` | yes | AT-308; TC-312 | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| `1677` | `0` | `168` | `1845` | `1845` | `n/a — no slow marker` / `1845` | yes |

- Increment 001: `1677 − 0 + 144 = 1821` (`inc001-green.txt`: 1821 passed). Increment 002: `1821 − 0 + 24 = 1845` (`inc002-green.txt`: 1845 passed, 357.16 s). Gate: 1845 passed, 306.00 s (orchestrator).
- 168 = the collected nodes of `tests/test_kanban_readable.py`: AT ×13, TC ×155 (TC-301 62, TC-302 43, TC-303 1, TC-304 7, TC-305 1, TC-306 4, TC-307 3, TC-308 7, TC-309 15, TC-310 1, TC-311 7, TC-312 3, TC-313 1). The 11 census rewrites in `test_app.py`, `test_kanban_priority.py` and `test_prism_laws.py` are in place, net 0. No node was deleted.

### Packet claims re-read (each against its transcript)

| Claim (packet) | Transcript | Holds? |
|---|---|---|
| 001: RED on base 79 failed / 62 passed; the 62 green = the 60 TC-301 arms + the guard + the 118×30 TC-311 arm | `inc001-red-on-base.txt`: `79 failed, 62 passed` | ✓ |
| 001: 28 of 28 KILLED (M1–M20, R1–R8) | `inc001-mutations.txt` (M1–M16 + R1–R8, M13 round 2) + `-tail.txt` (M17–M20) | ✓ (the "SURVIVED" token in the transcript is M13's round-1 label; the M17 assertion trace is the documented site move) |
| 001: reverse census 57 failed / 1620 passed | `inc001-reverse-census.txt` | ✓ |
| 001: gate 1821 passed in 306.79 s | `inc001-green.txt` | ✓ |
| 001: the re-render equals `out/R-1b-*` but for the spine and the head | qa probe6 | ✓ |
| 001: title readability 7.3 → 11.8 (0 → 13), 1.0 → 6.2 | `readability-base.txt`, `readability-inc001.txt`; qa probes 4 and 5 | ✓ |
| 001: 18 evidence files with digests | sha256 re-check | ✓ (18 / 18) |
| 002: RED on the 001 tree 8 failed; on base 16 failed | `inc002-red.txt` `8 failed, 13 passed`; `inc002-red-on-base.txt` `16 failed, 5 passed` | ✓ |
| 002: 15 of 15 KILLED | `inc002-mutations.txt` (Q1–Q6, Q13–Q15), `-q7q8.txt`, `-tail.txt` (Q9–Q12) | ✓ |
| 002: reverse census 7 failed / 1814 passed, all environment-only | `inc002-reverse-census.txt` | ✓ (count); environment-only accepted on the packet's word plus the green gate run |
| 002: gate 1845 passed in 357.16 s | `inc002-green.txt` | ✓ |
| 002: 16 evidence files with digests | sha256 re-check | ✓ (16 / 16) |
| §6.5 / LED .17: "the floor-first split measured 5.3 chars at 80×24 … executed, `evidence/inc001-widths.txt`" | **file absent** from `evidence/` | ✗ **citation false** (G-001). The number reproduces: qa probe4, floor-first 5.3 / 2 full at 80×24 and 11.3 / 12 at 118×30 |
| D-313: "the nodes are rewritten with reasons in the increments' censuses", naming `test_kanban_shows_every_task_in_its_phase` | `git diff tests/test_app.py`; census lists | ✗ that node is untouched; it stays green at 160×0 (G-004) |
| 001 §1: "`title_markup` shares it" (the `_literal` fix) | `git diff taskboard/views.py` | ✓ disclosed, but it is not in Files-modified, not in the correction population and not tested (G-003) |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | LLR-302.1 (LED .17, §6.5) | The amendment cites an executed transcript, `evidence/inc001-widths.txt`, that does not exist (C-59). The claimed number (5.3 at 80×24 under the floor-first rule) **reproduces** in qa probe4, so the rationale stands. The citation, however, is false. | major | Record fix before close (`iterate-to-fix`, P3, record only): put the measurement on disk under that name (qa probe4 can be re-run or copied in) or re-point the ledger / §6.5 citation. No code change. |
| G-002 | HLR-303, HLR-305, HLR-306, LLR-302.1, LLR-303.1 | Threshold clauses with no node, or a weaker node than the text: (a) HLR-305 "at 80×24 a tag is drawn exactly when the shed order leaves room" has **no node**, and the tag hue is asserted for `Ops` only; (b) HLR-306 80×19 "3 highs, `+1 more ↓`, `to5` in Ops" is asserted only as capped-or-not; (c) HLR-303 "one rule per non-empty group" is asserted as a subset; (d) "every width 24..160" is sampled (7 widths; rooms every 7). The behaviour holds on every clause by qa probe1 and inspection of the 80×24 capture. | minor | Tighten the arms in a tests-only pass (with G-003/G-004), or ⏸ DEFER to BACKLOG with this row as the reason. |
| G-003 | out of scope (§1.2: "matrix and lanes … unchanged") | (a) **Escaped-defect fix without its regression.** The shared, shipped `title_markup` now routes through `_literal`. That changes 10 call sites outside the kanban grouped body: `card_cell` (lanes), `row_markup` ×2, `task_row`, `_focus_cards`, `tile_lines`, `_focus_inspector`, `_focus_image_card`, `_focus_compact_card`, `_kanban_matrix`. qa probe7: on base, `title_markup("x\ y\", 5)` printed 6 cells (a row that leans); now it prints 5. The fix is correct, but no requirement covers it, it is not listed in either packet's Files-modified or correction population, and no shipped-surface regression demonstrates the pre-fix RED (station §Escaped-bug regression). (b) Literal drift: AT-305 selects `to3` where HLR-307 names `tw3`. Under `tw3` the Ops band is folded at 118×30, so the threshold as written cannot be observed. TC-302's "60-char / 20-char" titles are 58 / 24. Neither drift is in §6.5. | major (a) · minor (b) | (a) `iterate-to-fix` (P3, tests only): one shipped-surface node, e.g. lanes or the list row with a title `x\ y\` at a cutting width, captured RED on `13745f6` and green now, plus a §6.5 / packet note naming the scope extension. (b) A §6.5 Before/After line at close (`tw3` → `to3`; the literal lengths). |
| G-004 | D-313 (supersession) | (a) `test_app.py::test_kanban_groups_by_project` still asserts the superseded per-column per-project header ("Each phase column groups its tasks under a per-project header line"). It **passes by coincidence**: it slices columns with the old `_phase_window` geometry (`[52, 52, 52]` at 160, while the drawn columns differ and the rail is 16 cells), and "Alpha" / "Inbox" fall inside its column-0 slice only because the band rule crosses column 0 (qa probe2: rows 3 and 15 are `▐ Alpha  4 open ──…`, `▐ Inbox  1 open ──…`). (b) `::test_kanban_marks_blocked_without_moving_it` uses the same stale geometry. (c) D-313 says `test_kanban_shows_every_task_in_its_phase` is rewritten. It is untouched and green, because nothing folds or is counted at 160×0, and its "show them ALL" docstring is unqualified. The B1 census catches only failing nodes, so these stale passers were outside its reach. | major | Tests-only pass (with G-003a): re-point (a)/(b) to the band rule and `kanban_plan` widths, or retire them with a reason. Correct D-313's wording so (c) reads "kept — the law holds unwindowed at ≥ 100 cells", and qualify the docstring. Mark the canon accordingly at close. |
| G-005 | record | (a) `evidence/p4-gate.txt` carries no command line, tree identity or executor header. Its attribution rests on the orchestrator's hand-off plus my revision check, with digest `6d1533f8…` recorded here. (b) `captures/close-kanban-{118x30,80x24,80x22,…}` and `readability-close.txt` (`545f6558…`) have no packet digest and no named producer. (c) `.gitattributes` (+1 line, `evidence/** -text`, the prior batches' pattern) is changed but appears in no packet. | minor | Orchestrator records (a)–(c) in the close artifact. |
| G-006 | HLR-301..310 (trigger D) | The ux-reviewer's P4 expert walkthrough (§6.1; carried UX-9 `]` into a capped column, UX-10 filter edge cases, UX-11 `left`/`right` re-window, the `up` re-flow) is **not on record** at the time of this write. | major (pending, not a defect) | Fold the ux-reviewer verdict into this record before the P4 gate decision. |
| G-007 | HLR-309 (D-314) | `up` into a band already drawn re-flows the board (qa probe3: 16 transitions at 118×28/30 and 80×22/24). This is per spec: HLR-309 starts the window at the earliest band that keeps the selection's band drawn, and UX-14 asked only about `down`. | notice | Operator question via the ux walkthrough. Keep, or `iterate-to-refine` (P1) toward a symmetric rule. |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| none on disk for the shipped `title_markup` defect (trailing backslash prints twice, the row leans) | not-run — no regression node exists. qa probe7 shows the pre-fix value on base: `x\ y\` at width 5 → 6 cells | value | n/a — no node | not-run | none (G-003a) |
| TC-302 hostile arms (kanban card, NEW code — not an escaped defect: `_literal`'s first draft was caught in-increment) | `instrument RED-proof`, increment 001: `\[b]z` row 6 cells at `wc` 5 on the first `_literal` (narrated, no transcript) | value | yes — QA-L1 and QA-L2 KILLED on the final tree (`qa-mutations-layer0.txt`) | pass (gate) | `test_TC_302_a_card_is_two_rows_of_exactly_its_width[*]` |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

1. ✓ **Acceptance criteria use Given/When/Then** — n/a by design. The batch writes EARS statements plus numeric thresholds per HLR, as accepted at P2 (`02-review.md` qa checklist). Each AT docstring states its key sequence and expected painted result.
2. ✓ **Test cases have explicit Expected** — every Layer-A row above carries its numeric threshold, and every TC asserts literals (`test_kanban_readable.py`, e.g. `:178–179`, `:273`, `:570`).
3. ✓ **Edge cases include empty, boundary, invalid, error** — boundary catalogs per HLR/LLR. Empty: the empty board (TC-313), no done task, no high. Invalid: hostile titles and names (TC-302, TC-306, TC-307, TC-308, TC-311, TC-312). Error: n/a — no error surface (§6.4).
4. ✓ **Regression checklist exists** — the reverse census B1 per increment (`inc00{1,2}-reverse-census.txt`) and the P2 per-node census. Matrix and lanes nodes are green in the gate. The stale passers are reported as G-004.
5. ✓ **Exit criteria stated** — `01-requirements.md` §5.2; this record's verdict applies them.
6. ✓ **No real PII / secrets** — the oracle board `tests/kg_board.py` only. A home-path grep over `.dev-flow/2026-10-02-batch-03/` gives 0 hits. Transcripts are redacted (`redact.py`, security S-1).
7. ✓ **Mode declared** — `validation`, at the top of this file.
8. ✗ **Validation mode: every case carries a result or a state, and each executed result names its executor** — every case does carry a result and an executor (orchestrator / software-dev / qa-reviewer / code-reviewer statement / unnamed, as declared above). However, one executed claim in the record (LED .17, "executed, `evidence/inc001-widths.txt`") cannot be traced to its transcript (G-001). The ux walkthrough is `not-run` (G-006).
9. ✓ **Layer B (black-box)** — 3 of 3 stories observed through `App.run_test` with boundary and negative arms. C-18 holds with 8 functions for 8 ATs.
10. ✓ **Bidirectional surface-reachability** — the matrix above. The inputs and outputs not driven by a key (focus, the typed `/`, `up`, the 80×24 tags) are named, with their below-surface node.
11. ✓ **No unfilled template** — no `<...>` placeholder, no unassigned id, no empty Steps or Expected in this file. A grep of this file for the template's angle-bracket placeholders returns 0 hits.

## Orchestrator fold — P4 iteration 2 gate (2026-10-02)

Appended by the implementing agent; qa's text above is unchanged.

| Gap | Discharge | Evidence | State |
|---|---|---|---|
| G-006 | ux re-walk of UXV3-1: **PASS-WITH-NOTES**, UXV3-1 fixed (8 walks, 0 bad steps; scroll 0, head and fold row on screen, selected card whole). New notices UXV3-12..15, none blocking; routed to close | `evidence/p4-ux-rewalk.txt` sha256 `7f0cade30bb76d794da81566130caa7d8cb32b2fb7013b225a76e630a730e8ac` | executed · approved |
| G-009 | close captures re-taken on the frozen tree (the 80×24 fold row keeps its names) | `evidence/close-*` | executed |
| G-010 | the 22 *Executed verification* commands in `01-requirements.md` now select by AT/TC id (`-k AT_305`, `-k "AT_308 or TC_312"`, `-k "taller_than or keeps_every_count"`, …); each re-collected ≥ 1 node | `evidence/p4-selectors.txt` | executed |
| G-011 | the clipboard node passes alone and in a full re-run: **1855 passed**, 0 failed | `evidence/p4-gate3.txt` sha256 `067c9837898525022aed3b52ce764a5dd4d0941cb6054ce3fddcec735ec87fce` | executed |
| G-012 | §6.3 and the PLAN risks now say the cut replaces the scroll (room < 3 declared) | `01-requirements.md` §6.3, `PLAN.md` | executed |
| cosmetic | `test_kanban_shows_every_task_in_its_phase` docstring scoped to the unwindowed render; increment-003 census wording names the clipboard node | `tests/test_app.py`, `03-increments/increment-003.md` | executed |
| G-002 | carried, DEFER to BACKLOG | — | deferred |

**Gate decision (standing authorization, autonomous):** P4 **approved** at iteration 2 — qa PASS-WITH-NOTES, ux PASS-WITH-NOTES, no HIGH open, suite 1855/1855. Operator questions routed to close: PV-9 (accept the cut), the PV-2 cap at a cut band (UXV3-12), UXV3-3 (`up` re-flow across bands), UXV3-2/G-008 (`at risk` unreachable).
