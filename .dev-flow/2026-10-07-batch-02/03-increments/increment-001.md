# Increment 001 — LLR-801.1/.2 · LLR-802.1 · LLR-803.1 · The chain map

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-02` |
| Increment | `001` (the batch's only increment) |
| Requirement(s) | `LLR-801.1` · `LLR-801.2` · `LLR-802.1` · `LLR-803.1` (HLR-801/802/803) |
| Acceptance | `TC-801..TC-810` · `AT-801` (+`AT-801b`) · `AT-802` · `AT-803` |
| Agent | `software-dev` — **DeepSeek V4 Pro (product) + DeepSeek V4.1 Flash (tests) in parallel**, orchestrated; review folds by the coordinator under the second exception |
| Date | `2026-10-07` |

## 1 · What changed

The chain map view behind key `6` — the C-2b oracle frames byte-faithful at 118×30 and 80×24:
per-project full-width band heads with the `dates` switch (the shipped `extra["date_links"]`
storage's labels), the chains with `──▸`/`┬▸`/`╰───╯` connectors and the heavy critical chain,
the meta row, the `no links` heads, the legend, the selection strip (the prototype's
plain-difference early measure), the keys bar; `x` view-dispatched to the shipped unlink seat
(the verbatim refusal), `m` cycling the selected task's PROJECT rule (stored strings, lenient),
`L` extended to this view, `↵` the shipped details. HLR-803 pinned the shipped cap — no renderer
change. Review folds: the deep-chain crash (columns capped at 4, the 24-col floor), the
whole-band fold (no dangling head; the app's nav filters to the drawn `line_map`), the header
counting only drawable tasks, the selection inked bright per the app-wide accent budget.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-801.1 · LLR-802.1 | the renderer + nav/help/legend branches + the review folds |
| `taskboard/app.py` | source | LLR-801.2 · LLR-802.1 | VIEW_ORDER/KEYS, `_select_first`, the x/m view-dispatch, the nav filter |
| `taskboard/keymap.py` | source | LLR-801.2 | `Key("6", …)`, L's views= |
| `tests/test_chainmap.py` | test | TC-801..810 · LLR-801.1 | new (Flash) + the review arms (coordinator) |
| `tests/test_chainmap_app.py` | test | AT-801/801b/802/803 · LLR-801.2 · LLR-802.1 | new (Flash) + the review arms (coordinator) |
| `tests/test_app.py` | test | LLR-801.2 | the view-keys pins, executed |
| `tests/test_colour_budget_app.py` | test | LLR-801.2 | KEYBAR_BASE + the census counts, executed |
| `tests/test_english.py` | test | LLR-801.2 | the help-sections pin, executed |
| `tests/test_link_picker.py` | test | LLR-801.2 | L's views tuple, executed |
| `tests/test_readme.py` | test | LLR-801.2 | the README pins, executed |
| `README.md` | doc | — | the `6` row, the ten-views lines |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** (views · app · keymap) |
| Test files | 7 (uncapped) |

## 4 · Test results

Suite at the increment's gate: in `evidence/inc001-gate.txt` (the final close run). The 13
chainmap nodes (TC-801..810, AT-801/801b/802/803) pass; TC-801/802 compare the painted frame
against the C-2b oracle bytes. The 12 census REDs the new view provoked were reconciled by
the coordinator (executed, not hand-written).

### RED counterfactual

Flash captured the 8 RED transcripts before the product landed (no `render_chainmap`, key `6`
unbound). The review folds carried their own REDs: TC-809 (textwrap crash), TC-810 (the
mid-band fold), AT-201 (accent selection) — each RED on the pre-fold code (the reviewer's
executed repros).

### Mutation verdicts

The pins' mutants were executed LIVE by the code-reviewer (CM-1's crash probe, CM-2's
24/36-undrawn probe) and by the ux lens in P2; the reviewer's rev-2 re-run of the same probes
on the fixed tree confirms the kills. The behavior surface beyond the pins is oracle-pinned
(byte-exact frames) — a drift reddens TC-801/802.

### Evidence files

`evidence/chunkA-run.log` · `evidence/chunkB-run.log` (the two agents' runs + RED transcripts) ·
`evidence/inc001-gate.txt` (the close suite) · `evidence/frames/C-2b-*.txt` (the law).

## 4b · Independent review

`code-reviewer` — r1 **BLOCK-UNTIL CM-1 + CM-2** (both HIGH, both with executed repros beyond
the oracle's reach) + CM-3/4/5 · fixed RED-first under the standing authorization's second
exception (coordinator) · r2 **PASS-WITH-NOTES**: CM-1/CM-2 VERIFIED by re-running the original
probes on the fixed tree; notes: the resize-heal mechanism (LOW, backlog), the deep-chain
whole-band fold at typical heights (backlog refinement candidate), AT-801b's docstring nit.
Plus the four P2 lenses over the contract (iteration 4: PASS/PASS-WITH-NOTES).

## 5 · Risks / 6 · Pending

- Deep chains pile into the capped columns and can fold whole at 24–30 rows (honest counts,
  no invisible selection) — a per-band cap/split is a backlog candidate.
- The resize-heal leans on a second refresh (LOW).
- Backlog takes both.

## Increment gate checklist — all ✓ (3 source files; tests in the pass; REDs executed;
## reverse census: the 12 registrations re-derived and green; code-reviewer r2 PASS-WITH-NOTES;
## evidence at the declared homes).
