# Validation — taskboard — Batch 2026-10-07-batch-06

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

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

- **Result:** PASS
- **Layer 0:** `4` unit(s) met the criterion · `4` carry a named reddening mutation (M12 for `_windowed_header`'s marker law · M9 for `_chainmap_plan`'s `○` admission · M10 for the band-admission guard / the `no links` emptiness · M11 for the tile-aware fold's cap branch) — all four KILLED
- **Requirements:** `2`/`2` pass (HLR-1201 via AT-1201 + the amended TC-801/TC-802/TC-810 riding LED-2026-10-07-batch-06.1; HLR-1202 via AT-1202) · `0` blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — the sealed batch-02 frames path has 0 refs in `tests/test_chainmap.py` (the `FRAMES` path moved under the LED); the old kanban chrome (`◀`/`▶`) has 0 refs in the shipped law; the chains-only cap arithmetic has 0 refs (`tail_n` counts chains AND tiles at `views.py:5869`)
- **Test ledger:** ✓ reconciles (`base − D + A = post` → `2566 = 2556 − 0 + 10`)
- **Evidence checklist (qa-reviewer):** `human:coordinator` — self-executed by the close-out coordinator · `10` of `10` rows ✓ with evidence (`02-review.md`; the per-increment packet tables)

> The ONE complete run (`C-25`): the orchestrator's full suite on the gated tree at P4 — this
> artifact consumes that result; it does not re-own the run. The implementing session's two
> complete green runs over the settled tree both passed **2566 / 2566** (`evidence/inc001-run.log`,
> 447.08s and 422.53s), and the close-out re-collected the suite at **2566 tests** on the final
> tree (`pytest tests --collect-only -q` → `2566 tests collected`). Every Layer-0/A/B row below was
> executed by the implementing agent or the close-out coordinator (`human:coordinator`) under the
> batch's standing authorization, named per row.

> **The amended-oracle note:** the C-2b oracle AMENDS under LED-2026-10-07-batch-06.1 — the
> amended frames are this renderer's bytes on the SAME frozen fixture (kg_board shifted + Data
> Warehouse `together`, frozen calendar), stored CRLF at
> `.dev-flow/2026-10-07-batch-06/evidence/frames/` (sha256
> `cd955e18…` / `227a2ced…`, digests in increment-002's packet); the sealed batch-02 frames stay
> history. The amendment's RED counterfactual is M9: without the renderer change the amended frames
> cannot match (`6 failed, 5 passed`, `evidence/mutations.log`). The operator's visual re-verdict
> on the amended frames + the new chrome is PENDING at close (batch C's form).

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `_windowed_header`'s marker law (views.py:4435-4467) | the `pre`/`suf` conditionals over the shipped `fits`/`start`/`n_open` window arithmetic; cyclomatic ≥3 | the 4 arms of `tests/test_kanban_window.py` | pass (mutation M12 below) |
| `_chainmap_plan`'s `○` admission (views.py:5551-5585) | the 3-tuple bands, FIFO-by-due, the bare guard; crosses the plan/renderer boundary | `test_an_open_unlinked_task_is_a_selectable_open_tile` · `test_the_nav_reaches_an_open_tile_in_band_order` + the byte-exact TC-801/TC-802 | pass (mutation M9 below) |
| the band-admission guard / the `no links` emptiness (views.py:5581) | the `if ts or unlinked:` conjuncts; the inert row only for a no-open-work project | `test_the_no_links_row_only_for_a_project_with_no_open_work` | pass (mutation M10 below) |
| the tile-aware fold's cap branch (views.py:5869) | the fit / partial / zero-fit split with tiles in the draw order and the cap; cyclomatic ≥3 | `test_TC_810_the_fold_caps_a_partial_band_and_still_drops_whole` | pass (mutation M11 below) |

**Measured by mutation, never by line coverage.** For each unit, name the mutation and paste the RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `_windowed_header`'s marker law | M12: the right marker removed (`suf = f" ▸ {n - end}" …` → `suf = ""`) | yes — `1 failed, 3 passed` on the new file: the hidden-count arm reddened; the left-marker, all-fits and help arms stayed GREEN (named in increment-001's packet) | `evidence/mutations.log` M12 |
| `_chainmap_plan`'s `○` admission | M9: `unlinked = sort_by_due(...)` → `unlinked = []` (the admission dropped) | yes — `6 failed, 5 passed` on `tests/test_chainmap.py`: the amended TC-801/TC-802 frames diff (the `○` rows are gone) plus the tile arms; doubles as the oracle amendment's RED counterfactual | `evidence/mutations.log` M9 |
| the band-admission guard / the `no links` emptiness | M10: `if ts or unlinked:` → `if ts:` (bare rows despite open work) | yes — `3 failed, 8 passed` on `tests/test_chainmap.py`: the arms pinning "the `no links` row only for a project with no open work" | `evidence/mutations.log` M10 |
| the tile-aware fold's cap branch | M11: `tail_n = (nslot - limit) + (n_open - n_tiles)` → `tail_n = (nslot - limit)` (the cap's N drops the tiles) | yes — `1 failed` on TC-810: the cap count is exact over chains AND tiles | `evidence/mutations.log` M11 |

### UX walkthrough — only if trigger family D fired

Family D fired: the batch IS the operator-feedback batch — two reports from real use (the chain
map's empty projects / "es imposible crear cadenas"; the kanban's hidden phase columns).

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| on a board with no links, the chain map shows every open task as an `○` tile; selecting one and pressing `L` creates the first link right there | `TaskboardApp` driven with keys through `run_test` (key `6`, select `tw3`, `L`, `enter` — the real LinkPicker) | the painted row carries `○ Fix checkout 500 error`; after the pick, `depends_on == ["tw2"]` and the task is still drawn (inside the chain) | ✓ |
| `x` on a linked tile leaves it an `○` tile (visible, re-linkable) | the app driven with keys (`x` on `tw3` linked to `tw2`) | `depends_on == []` and the painted row still carries `○ Fix checkout 500 error` | ✓ |
| the arrows reach the `○` tiles | the app's own nav columns + a real `down` move onto the tile | `tw3` in the nav flat order and reachable by one `down` from the previous task | ✓ |
| the kanban head row marks the hidden sides and the `?` help names the window | `views.render_kanban` at 40/80 cells + `help_usage("kanban")` | the emitted rows `'BACKLOG 1│NEXT 1 ▸ 2│✓1'` / `'◂ DOING 1/3│REVIEW 1│✓1'`; the joined help text ends `… · ◂ ▸ mark the hidden sides` | ✓ |

**Mechanism used:** Textual's `run_test` pilot + the renderer directly — the criteria driven through the REAL mechanism, their painted results asserted off the emitted widgets/rows.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — AT-1201's app arms drive the app with keys; AT-1202's arms render the shipped surface |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — the close-out coordinator read the amended frames band-by-band against the old chrome (the `○` rows, the gone Ops inert row, the fold behavior at both sizes) and the marker rows against the contract's arms (C-32) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — the operator's visual re-verdict on the amended frames + the new chrome is requested at close (batch C's precedent; the batch pushes under the commission; the operator's verdict folds on arrival) |

- **Method:** the arms' fixtures — synthetic boards in `tmp_path` / the batch's evidence home (the kg board, frozen calendar), the house pilot at 118×32 and 80×24
- **Participants or population:** none — no user session this batch
- **Evidence of the evaluation:** `evidence/inc001-run.log`, `evidence/mutations.log`, the amended frames, `tests/test_chainmap.py`, `tests/test_chainmap_app.py`, `tests/test_kanban_window.py`, the close suite re-collection
- **Limits:** no user performed the walkthrough; the operator's eye is owed on the amended C-2b frames and the new chrome (markers + tiles) at the next session

### Layer A — functional (white-box): per-requirement results
> `TC-NNN` ↔ LLR/HLR. `Result` = pass / fail. `Evidence` = command output, observed behavior, inspection note, or analysis result.

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-1201 | test | `pytest tests/test_chainmap.py tests/test_chainmap_app.py -q` | 0 failures; TC-801/TC-802 byte-exact against the AMENDED frames at both sizes; the tile arms; L/x/nav on the map | pass | `evidence/inc001-run.log` (19 passed; two full greens at 2566); the frames' digests; M9/M10/M11 |
| HLR-1202 | test | `pytest tests/test_kanban_window.py tests/test_kanban_readable.py tests/test_cells.py -q` | 0 failures; `◂`/`▸ 2` at the 2-of-4 fit; none at the full width; the help bullet verbatim | pass | `evidence/inc001-run.log` (399 passed; 30 passed, 132 deselected on `-k kanban`); M12 |
| LLR-1201.1 | test (unit) | the 3 unit arms + TC-801/TC-802/TC-810 | the tile paints + is selectable; the `no links` row only for no-open-work; nav order; the cap N exact over chains AND tiles | pass | `views.py:5551-5585` · `:5751` · `:5869`; M9/M10/M11 |
| LLR-1201.2 | test (integration) | the 3 app arms | the picker opens on the map and the pick lands as the FIRST incoming link; `x` leaves an `○` tile; `down` rests on a tile; the strip's `◂ waits on  nothing yet` for an `○` selection | pass | `tests/test_chainmap_app.py:345-410`; `views.py:5954` |
| LLR-1202.1 | test (unit) | the 4 arms of `tests/test_kanban_window.py` + the two pinned updates | `◂` at `start > 0`; `▸ N` exact; none when all fits; the bullet verbatim | pass | `views.py:4456-4457` · `:6817-6822`; M12 |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-1201 | AT-1201 | the chain map through the app pilot (key `6`, arrows, `L`, `x`) | the painted `○` tile rows + the amended frames' bytes + `depends_on` after the pick | repr: `○ Fix checkout 500 error ▲2d` · boundary: the first link of a board (`[] → [pred]`) and a task becoming unlinked back to a tile · negative: the `no links` row survives ONLY for a no-open-work project (the Lonely/Busy arm) | pass |
| US-1202 | AT-1202 | the kanban render + the `?` help | the phase-head row at 40/80 cells + the joined help text | repr: `▸ 2` exact at the 2-of-4 fit · boundary: the late selection (`◂`, count drops) and the exactly-fits width · negative: the all-fits width renders zero markers | pass |

### Bidirectional surface-reachability matrix (extends A-5)
> Every named INPUT dimension AND every named OUTPUT/deliverable is exercised/observed through the handler — not only the service API.

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | `L` on an `○` tile | `action_link` → LinkPicker → `link_tasks` (a FIRST incoming link) | yes | AT-1201 (`test_L_links_an_open_tile_on_the_map`) | ✓ |
| input | `x` on a linked tile | `_chainmap_unlink` → `unlink_tasks` | yes | AT-1201 (`test_x_unlinks_a_linked_tile_back_to_an_open_tile`) | ✓ |
| input | the arrows / `j`/`k` on the map | `_chainmap_nav` (tiles at depth 0, band order) | yes | AT-1201 (`test_nav_reaches_an_open_tile`) · the unit nav arm | ✓ |
| input | the terminal size (fold pressure) | `render_chainmap` at 118×30 / 80×24 / 80×18 / 118×32 | yes | TC-801/TC-802 · TC-810 · AT-801c · AT-802 | ✓ |
| input | the kanban width + the selection's phase | `_phase_window` / `_windowed_header` at 40/80 cells | yes | AT-1202's 4 arms | ✓ |
| output | the painted `○` tile rows (every open task) | the canvas + the `line_map` (selectability) | yes | AT-1201 (the tile arm) | ✓ |
| output | the created link (the chain born on the map) | `depends_on == ["tw2"]` + the task still drawn | yes | AT-1201 (`test_L_links_an_open_tile_on_the_map`) | ✓ |
| output | the strip truth for an `○` selection | `◂ waits on  nothing yet` / `▸ unblocks  …` | yes | AT-1201 (the painted canvases in `evidence/inc001-run.log`) | ✓ |
| output | the amended oracle's bytes | the frames at the batch's evidence home (CRLF, sha256-verified) | yes | TC-801 · TC-802 | ✓ |
| output | the window markers + the help bullet | the phase-head row + `help_usage("kanban")` | yes | AT-1202 | ✓ |

### Signed-balance test ledger
> `post = base − D + A`. State counts in collected / passed-lean / passed-full form.

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2556 | 0 | 10 | 2566 | 2566 | 2566 / see the C-25 run | yes |

base = the batch-05 trunk (2556); A = the batch's 10 new nodes — `tests/test_kanban_window.py`
(4) · `tests/test_chainmap.py` (3: the tile, the no-links emptiness, the nav) ·
`tests/test_chainmap_app.py` (3: L-links-on-the-map, x-returns-a-tile, nav-reaches-a-tile); the
TC-810/AT-802/AT-801c amendments, the `FRAMES` move, and the two pinned kanban updates modified,
not added. The close-out re-collected the suite at **2566 tests** on the final tree
(`pytest tests --collect-only -q`), and the two complete green runs over the settled tree passed
2566 (`evidence/inc001-run.log`); the orchestrator's C-25 close run owns the final passed count.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| — | — | none — no test gap detected; the M9-M12 battery is all-KILLED, and the three layout-driven pinned-test updates (TC-810 · AT-802 · AT-801c) are law-driven and named in increment-002's packet, not gaps | — | — |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| AT-1201 (the operator's 2026-10-07 report: "es imposible crear cadenas") | the filing — a zero-link board's chain map drew inert `no links` rows with nothing selectable and creation lived only off-view (P-1's reproduction: the picker worked on kanban/gantt, invisible from the map) | shape (a dead-end surface) | yes — the tile arms discriminate a painted, selectable tile; L/x arms discriminate a link created/removed ON the map; M9/M10/M11 discriminate the admission, the emptiness and the cap | 6 new nodes + the amended frame arms green | `test_an_open_unlinked_task_is_a_selectable_open_tile` · `test_the_no_links_row_only_for_a_project_with_no_open_work` · `test_the_nav_reaches_an_open_tile_in_band_order` · `test_L_links_an_open_tile_on_the_map` · `test_x_unlinks_a_linked_tile_back_to_an_open_tile` · `test_nav_reaches_an_open_tile` |
| AT-1202 (the operator's 2026-10-07 report: hidden later phase columns, "incluso reescalando") | the filing — the window followed the selection with no on-screen sign the rest existed | value (silence) | yes — the marker arms discriminate side + exact count; the all-fits arm discriminates the no-marker case; M12 discriminates the right marker | 4 new nodes + the 2 pinned updates green | `test_the_narrow_window_marks_the_hidden_right` · `test_a_late_selection_marks_the_hidden_left_and_drops_the_count` · `test_the_full_window_carries_no_markers` · `test_the_help_names_the_window_bullet` |

### Evidence checklist — qa-reviewer (full)
> Attach `qa-reviewer`'s completed evidence checklist (items in `agents/qa-reviewer.md`), each marked ✓/✗ with one-line evidence. An unchecked or evidence-less item blocks the gate.

`qa-reviewer` — self-executed by the close-out coordinator (`human:coordinator`; the runtime spawned nobody, named per the dev-flow runtime rule):

- [x] Acceptance criteria observable — AT-1201 reads the painted tile rows + `depends_on` through the app pilot; AT-1202 reads the emitted head row + the joined help text; TC-801/TC-802 read the painted canvas byte-exact against the amended frames (`tests/test_chainmap_app.py` · `test_kanban_window.py` · `test_chainmap.py`)
- [x] Test cases have explicit Expected — the amended frames' bytes (sha256-verified); the exact `▸ 2` / `◂` law; the verbatim help bullets; `+3 more ↓` exact over chains AND tiles; `depends_on == ["tw2"]`; the strip's `◂ waits on  nothing yet`
- [x] Edge cases include empty, boundary, invalid, error — the Boundary catalog fields across the contract: ☑ empty (the no-open-work project — the inert row stands; the all-fits window) ☑ boundary (the first link of a board; exactly-fits vs one-hidden; the late selection; the zero-fit band drops whole) ☑ invalid — none new ☑ error — none new (the shipped `x`-on-a-never-linked refusal stands, unchanged)
- [x] Regression checklist exists — the reverse census (5 probes × 2 packets), the M9-M12 battery with per-node/family verdicts, the amended-oracle byte check, the old-chrome supersession greps, the suite re-collection at 2566
- [x] Exit criteria stated — the contract §5.2's criteria, all met (every HLR a passing AT; every new assertion RED by a recorded mutation; the amended oracle at the batch's evidence home with the LED; full suite green at the last settled runs; the visual re-verdict requested at close per batch C's precedent)
- [x] No real PII / secrets — synthetic boards in `tmp_path` + the batch's evidence home (the kg fixture); the operator's board copy was read-only input to P-1's reproduction, never written
- [x] **Mode declared** — validation mode: this artifact, Result PASS; every executed result names its executor (the implementing session, the close-out coordinator, or the orchestrator for the ONE full C-25 run)
- [x] **Layer B (black-box)** — every story's deliverable observed through the shipped surface with boundary + negative (the Layer B table)
- [x] **Bidirectional surface-reachability** — the matrix above, 10/10 rows ✓
- [x] **No unfilled template** — the verdict fields filled; the artifacts carry no placeholder cells naming nothing
