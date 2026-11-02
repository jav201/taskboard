# Inc X — validation (E5: the change only)

**Verdict: done for E5, with two record gaps open (below).** No MAJOR/HIGH is open. Head before the corrective pass: `4c49dd8`. The corrective pass is the commit that adds this file.

## Scope proven
- Requirements: US-4501, 6 HLR (4501..4506), 48 active LLR, 6 AT (`01-requirements.md`, ledger `01-requirements-ledger.md`). TC numbering: LLR-450k.n → TC-(4700 + 20(k−1) + n).
- Design: Code-Wire baseline + interfaces + proto-A (`app.py`) + proto-B (`views.py`) (`graph-*.cw.md`; trace `e2-trace.txt`). PDR: round 1 architect FAIL + security PASS-WITH-NOTES, round 2 both PASS-WITH-NOTES (`03-pdr-*.md`, rulings 1–22 in `00-e1-rulings.md`, addenda in `e3-addenda.md`).
- The change: `x` in `R` writes the scoped HTML deck through `report_deck.render`; the SVG/PNG export and the Edge rasteriser are removed; `H` is on the key bar; the `o` offer is shared with `H`.

## Tests (all `env -u NO_COLOR python -m pytest`, `taskboard.__file__` in each header)
| Run | cwd | Result | Evidence |
|---|---|---|---|
| RED, new tests on base `8506cb7` | incX-tests | 133 failed / 39 passed | `evidence/red-base.txt` |
| GREEN after the E4 build | worktree | 531 passed / 2 failed (both test defects, fixed at integration) | `evidence/green-1.txt`, `e4-integration.md` |
| GREEN after integration, 19 files | worktree | 527 passed | `evidence/green-2.txt` |
| GREEN after the E5 corrective pass, same 19 files | worktree | **528 passed, 0 failed** (+1: TC-4715's new arm) | `evidence/green-3.txt` |
| Supplementary: `test_keymap.py` + `test_readme.py` | worktree | 1 failed (CP-1) → fixed → 35 passed | `evidence/green-3.txt` |

No full suite in this increment: it runs once at the batch end.

## Mutants (in copies of the tree, never the worktree)
- E5 battery (Kimi K2.8, copy `incX-mut`): 40 killed, 2 survived of 42 (`05-mutants.md`).
- Corrective pass (copy `incX-mut2`, removed afterwards): **M10 killed 3/3** by TC-4710's new `Board.save`/`save_atomic` spy (`assert ['save'] == []`); **M15 killed** by TC-4715's new `none_visible=True` arm (`AttributeError` on the `None` slot). Both still survive the previous tests, so the kill is the new assertion's. `evidence/mutants-replay-e5.txt`.
- M43 (E5-S2, `t2.urls.clear()`): killed 3/3 by TC-4727, the security reviewer's replay (`05-review-security.md`).
- **Score: 43/43 killed.**

## Reviews of the code
- Code review: PASS-WITH-NOTES, 3 LOW + 3 MINOR (`05-review-code.md`). Fixed: F1 (dead `w` removed from `action_export`, `app.py:635`), F2 (stale export text: `app.py:293`, `views.py:6651`, `:6665`, `:7220`, `:7548`; `docs/ARCHITECTURE.md` rows for `render_present`, `render_present_all`, `legend_strip`, the `views` module row, and the removed `present_all_export` row), F5 (the no-op `_find_msedge`/`save_present_png` patches dropped, TC-4742's kept as a commented guard), F6 (TC-4734's oracle bound through `pytest.raises`). To BACKLOG, open: F3 (design-gap), F4 (design-gap).
- Security review: PASS-WITH-NOTES, 3 LOW (`05-review-security.md`). Fixed: E5-S1 (README `x` paragraph and the BACKLOG S-1 known-limit line say done and folded tasks' titles and notes reach the deck by design, ruling 13), E5-S2 (row M43). To BACKLOG, open: E5-S3 (lone surrogate escapes the `OSError` catch; pre-existing).
- Corrective finding CP-1 (found by this pass): `tests/test_readme.py::test_TC_2607…` pinned the README words E4 removed ("and their SVG/PNG exports"); it was outside the 19-file set. The oracle now pins the new wording; the claim is unchanged. `evidence/green-3.txt`.
- Re-review: nothing was blocking, so none is owed. The orchestrator checks M10/M15 through the replay evidence.

## Acceptance tests (black-box, keys and dialogs)
AT-4501..AT-4506 in `tests/test_present_html_at.py`, all GREEN in `evidence/green-3.txt`.

## Not done / not run
- **CASE gap:** `trace_check.py --req …/01-requirements.md --base 8506cb7 --src taskboard` reports `no 02-test-cases.md` (the test design lives in `e4-tests.md`). Not written in this pass.
- **Captures:** the UI changed (the `H` key bar entry, the `x`/`o` help rows), and no real Windows Terminal captures were taken in this increment.
- Full suite: at the batch end, by rule.
