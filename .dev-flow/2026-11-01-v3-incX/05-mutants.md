# E5 mutants — Inc X

Base under test: `git diff 8506cb7 f55bb4b -- taskboard/` (app.py, keymap.py, views.py).
Each E1 negative control (NC) from `01-requirements.md` was applied to the source of the
throwaway worktree `incX-mut` (detached at `f55bb4b`), the mapped test(s) from the E4
mutant table (`e4-tests.md`) were run with
`env -u NO_COLOR python -m pytest -q -p no:cacheprovider <node>`, the result recorded,
and the mutant reverted with `git checkout -- <file>`.

Baseline before the battery: `tests/test_present_html_export.py` +
`tests/test_present_html_at.py` → **172 passed, 0 failed** (GREEN).

Result: **40 KILLED, 2 SURVIVED** (42 NCs). After the E5 corrective pass: **43 KILLED, 0 SURVIVED** (43 NCs; M10 and M15 killed by strengthened tests, M43 added from the security review). See *Corrective pass*.

| id | LLR | mutation | test | result |
|---|---|---|---|---|
| M01 | 4501.1 | `present_name` project arm uses H's `deck-<board>-<project>-<date>.html` | TC-4701, TC-4701b | KILLED |
| M02 | 4501.2 | `present_name` None arm uses H's `deck-<date>.html` | TC-4702 | KILLED |
| M03 | 4501.3 | `_deck_lane` keys the deck `#0` instead of the registry id | TC-4703 | KILLED |
| M04 | 4501.4 | `action_export` extracts with `people={}` | TC-4704 | KILLED |
| M05 | 4501.5 | views 1/2 proxy holds every shown project, not the presented one | TC-4705 | KILLED |
| M06 | 4501.6 | view-3 proxy holds shown projects in board order | TC-4706 | KILLED |
| M07 | 4501.7 | deck scope built from the presented board twice (every-board scope) | TC-4707 | KILLED |
| M08 | 4501.8 | proxy skips folded projects (folds read at export) | TC-4708; AT-4502 | KILLED |
| M09 | 4501.9 | proxy holds open tasks only (`present_tasks_m[0]`) | TC-4709; AT-4502 | KILLED |
| M10 | 4501.10 | `action_export` calls `self._board.save()` during export | TC-4710 | **SURVIVED** → KILLED (E5 corrective, 3/3) |
| M11 | 4501.11 | `_deck_lane` indexes the registry unguarded (raises on `bid None`) | TC-4711 | KILLED |
| M12 | 4501.12 | `action_export` returns without writing an empty view-3 scope | TC-4712 | KILLED |
| M13 | 4501.13 | narrow-width warning branch dropped | TC-4713; AT-4505 | KILLED |
| M14 | 4501.14 | narrow branch warns but no longer returns (writes anyway) | TC-4714; AT-4505 | KILLED |
| M15 | 4501.15 | missing presented id kept in the proxy (`proxy.projects = [p]`) | TC-4715 | **SURVIVED** → KILLED (E5 corrective, arm `[True]`) |
| M16 | 4502.1 | proxy skipped: the unfiltered board is extracted | TC-4721; AT-4501 | KILLED |
| M17 | 4502.2 | view-3 proxy keeps hidden projects (tasks filtered only) | TC-4722; AT-4502 | KILLED |
| M18 | 4502.3 | `proxy.tasks = list(board.tasks)` (archived/projectless kept, Inbox row) | TC-4723 | KILLED |
| M19 | 4502.4 | held tasks use `present_tasks` (hidden-class milestones kept) | TC-4724 | KILLED |
| M20 | 4502.5 | `extract` passes every milestone class to the deck | TC-4725 | KILLED |
| M21 | 4502.6 | export scope captured when `R` opens (cached on the screen) | TC-4726; AT-4501 | KILLED |
| M22 | 4502.7 | task URLs left on the copies (`t2.urls = list(t.urls)`) | TC-4727 | KILLED |
| M23 | 4503.1 | `_write_report` keeps the old `Exported …` toast text | TC-4731; AT-4501, AT-4503 | KILLED |
| M24 | 4503.2 | `o` row removed from `PRESENT_KEYS` (unbound in `R`) | TC-4732; AT-4503 | KILLED |
| M25 | 4503.3 | offer never expires and is reusable (slot not cleared, no clock check) | TC-4733, TC-4733b; AT-4503 | KILLED |
| M26 | 4503.4 | write `OSError` left unguarded (escapes the screen) | TC-4734; AT-4504 | KILLED |
| M27 | 4503.5 | a failed write preserves the earlier live offer | TC-4735; AT-4504 | KILLED |
| M28 | 4503.6 | opener failure swallowed silently (no error toast) | TC-4736, TC-4736b | KILLED |
| M29 | 4503.7 | success toast renders the folder with `markup=True` | TC-4737 | KILLED |
| M30 | 4504.1 | an `.svg` sibling written beside the deck | TC-4741; AT-4501, AT-4502 | KILLED |
| M31 | 4504.2 | external rasteriser kept (`subprocess.run` in `action_export`) | TC-4742 | KILLED |
| M32 | 4504.3 | removed `present_paths` left defined in views.py | TC-4743 | KILLED |
| M33 | 4505.1 | `H` kept `bar=False` (base seat) | TC-4751; AT-4506 | KILLED |
| M34 | 4505.2 | every global key (`R A N n @ # I S`) promoted `primary=True` onto the bar | TC-4752 | KILLED |
| M35 | 4505.3 | `H` declared universal (sorts first, keeping its word) | TC-4753 | KILLED |
| M36 | 4505.4 | `H` given an empty label | TC-4754 | KILLED |
| M37 | 4505.5 | `H` listed in the help's global line as well as the band | TC-4755; AT-4506 | KILLED |
| M38 | 4506.1 | `x` help row keeps the base `SVG + PNG` wording | TC-4761; AT-4506 | KILLED |
| M39 | 4506.2 | `o` bound but its row skipped in `PresentKeys.lines()` | TC-4762; AT-4506 | KILLED |
| M40 | 4506.3 | `K`/`J` aliases dropped from the reorder binding | TC-4763 | KILLED |
| M41 | 4506.4 | hint row gains `o open` wording | TC-4764 | KILLED |
| M42 | 4506.5 | README key table names `SVG + PNG` as the presentation export | TC-4765 | KILLED |
| M43 | 4502.7 (S-R2-2) | `t2.urls = []` → `t2.urls.clear()` (empties the SOURCE task's URLs) | TC-4727 (3 views) | KILLED 3/3 (security reviewer's replay in a `git archive` copy, `05-review-security.md` §Runs and E5-S2) |

## Survivors

**M10 / LLR-4501.10 — `board.save()` during export (TC-4710 SURVIVED, 3/3 passed).**
`Board.save()` re-serializes the already-saved board to byte-identical content, so the
sha256 of `board.json` and `history.jsonl` before/after `x` is unchanged. Missing
assertion: TC-4710 only compares file *contents*; nothing spies on the write path — no
monkeypatched `Board.save`/`Path.write_text` asserting zero save calls, and no
mtime/write-count oracle. A redundant byte-identical save is invisible to this test.

**M15 / LLR-4501.15 — missing presented id kept in the proxy (TC-4715 SURVIVED, 1/1 passed).**
`present_deck_boards` resolves a missing id through `render_present`'s first-visible
fallback *before* the mutated line, so with visible projects Alpha/Beta both the mutant
(`proxy.projects = [p]`) and the code (`[] if p is None else [p]`) hold `[Alpha]` — the
mutant diverges only when no visible project exists at all (p is None → `[None]` →
downstream `AttributeError`). Missing assertion: no arm where the presented id is
missing **and** the board has zero visible projects (or a direct unit assertion on
`present_deck_boards`'s projects list for the missing-id case).

## Notes

- M34 and M40 needed corrected mutant implementations: M34's control only turns RED when
  the globals enter the **primary** layer (`primary=True`, bar defaulting True) that
  TC-4752 measures; M40's first edit was syntactically unbalanced and its first "kill"
  was a collection error — the corrected mutant fails TC-4763's exact binding-set
  assertion. M39's control requires decoupling the seat: the binding row stays in
  `PRESENT_KEYS` while `PresentKeys.lines()` skips it (adding a raw `Binding` cannot
  remove the generated window row).
- Every mutation was reverted with `git checkout -- <file>` after its run; the worktree
  is clean at `f55bb4b` and no background processes remain.

## Corrective pass (E5)

Replayed in the throwaway copy `incX-mut2` (`git worktree add --detach … HEAD` at `4c49dd8`,
removed with `git worktree remove --force` afterwards), with the corrective-pass tests copied
in and `taskboard.__file__` checked to resolve to the copy. Evidence:
`evidence/mutants-replay-e5.txt`.

| id | mutation | previous test | strengthened test | result |
|---|---|---|---|---|
| M10 | `self._board.save()` added in `action_export` before the deck path | TC-4710: 3 passed (survived again, as recorded) | TC-4710 now spies on `Board.save` / `Board.save_atomic` around the `x` press and asserts no call | KILLED 3/3: `assert ['save'] == []` |
| M15 | `proxy.projects = [p]` | TC-4715: 1 passed (survived again) | TC-4715 gains the arm `none_visible=True`: missing id and every project archived, so the deck must hold no project and name the empty scope | KILLED: `[True]` FAILED (`AttributeError: 'NoneType' object has no attribute 'id'`, views.py:7361); `[False]` passes |
| M43 | `t2.urls.clear()` | — | TC-4727 (unchanged) | KILLED 3/3 by the security reviewer (not re-run here) |

With the mutants reverted, the copy's TC-4710 and TC-4715 pass (5 passed).
