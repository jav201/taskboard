# Quick Spec — the live board becomes unreachable from anything committable

**Batch:** `2026-08-07-fastflow-05` · **Base ref:** `82cc256` (branch `kanban-variants`, NOT on the remote)
**Backup of the pre-rewrite tip:** tag `backup-kanban-variants-20260807` = `338973c`
**Language:** English · **security_required: TRUE** (see §6)

## 1. Objective

No file this repository can commit may contain the operator's live board data —
and that property must be held by **a law that fails**, not by an act that was
performed once.

Today the leak was removed by hand: strings substituted, a generated capture
deleted, branch history rewritten, two commits pushed to a public `main`. All of
it verified, **none of it defended**. `prototypes/capture.py` — the generator
that produced the leak — was still reading `~/.taskboard/board.json`, so the next
run would have restored it. That gap, not the strings, is what this batch closes.

## 2. User stories

- As the operator, I want the scripts that write committable artifacts to be
  **incapable** of reading my live board, so the leak cannot be re-authored.
- As the operator, I want a **detector that is itself tested against a planted
  leak**, so "the sweep came back clean" means the sweep can fail.
- As the operator, I want a stray `git add -A` in `prototypes/` to be unable to
  commit 892 scratch files.
- As the operator, I want today's hand work re-checked **by that detector**
  rather than trusted because I watched it happen.

## 3. Acceptance criteria (observable)

- [ ] **AC1 — capability, not policy.** `prototypes/capture.py` and
  `prototypes/verify_variants.py` contain **no reference to
  `default_board_path`**, and each **exits non-zero with a named error** when the
  fixture is missing, instead of falling back. Observable: run both with the
  fixture temporarily renamed → non-zero exit, message names the missing fixture;
  run both with it present → exit 0.
- [ ] **AC2 — the fixture is in git.** `prototypes/out/_fixture_late.json` is
  **tracked**. Observable: `git ls-files --error-unmatch` succeeds on it. (Today
  it is untracked, so AC1's fix depends on a file a fresh clone does not have —
  and `capture_languages.py` already had this defect.)
- [ ] **AC3 — the detector can fail.** A sweeper takes a board JSON and a tree
  and reports every file containing any of its project names / task titles
  (verbatim, length ≥ 12). Observable, and **both halves are required**: planted
  a known title into a temp tree → the sweeper **names that file**; a clean temp
  tree → the sweeper reports **nothing**. A sweeper that returns empty for both
  fails this criterion.
- [ ] **AC4 — the sweep is executed and recorded.** AC3's sweeper, run against
  the operator's real board over the **tracked** trees of `main@caa4bab` and
  every one of the **6 rewritten commits** on this branch, reports **zero files**.
  Observable: the executed output is pasted into the closing artifact.
- [ ] **AC5 — the accident is blocked.** `git add -A` under `prototypes/` cannot
  stage scratch output. Observable: `git check-ignore` reports the scratch path
  ignored **and** reports `_fixture_late.json` and the 4 tracked `.svg` **not**
  ignored.
- [ ] **AC6 — no artifact carries board data.** No file written by this batch
  (spec, tests, closing artifact) contains any real board string. Observable: the
  same sweeper, run over this batch's own diff, reports zero.
- [ ] **AC7 — the implicit fallback is gone (from P6 coming back FALSE).**
  `TaskboardWidget.__init__` **requires** an explicit board path; nothing reaches
  the live board by omission. The one legitimate interactive read —
  `widget_slice/app.py:1514`'s `__main__` — passes `default_board_path()`
  **explicitly**, so reading the operator's board is a visible act at exactly one
  site instead of a default at every site. Observable: `TaskboardWidget()` with no
  argument **raises**; `verify_ink.py` and `verify_widget.py` (4 sites) name a
  fixture and still pass; `grep` finds no remaining `TaskboardWidget()` with an
  empty argument list.

## 4. Out of scope (declared)

| item | why |
|---|---|
| Merging `kanban-variants` → `main` | operator ruled: **do not merge** (`main`'s `keymap.py` supersedes this branch's inline `HelpScreen`) |
| Anything on `main` | clean and pushed at `caa4bab`; AC4 only **reads** it |
| Git author identity for future commits | operator-level config, not a repo change — carried to the backlog |
| ~~`prototypes/widget_slice/app.py:1146` left as-is~~ | **WITHDRAWN — P6 came back FALSE.** Moved INTO scope as AC7 |
| Rewriting `main`'s history | needs force-push; operator's call, in the backlog |

## 5. Premise table (C-43)

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| P1 `capture.py` and `verify_variants.py` called `Board.load(default_board_path())` | premise | ✅ TRUE | `grep -rn "default_board_path()" prototypes/` → `capture.py:29`, `verify_variants.py:79` (pre-edit) |
| P2 `_fixture_late.json` is untracked | premise | ✅ TRUE | `git ls-files --error-unmatch` → fails; `git ls-files prototypes/out/` lists only 4 `.svg` |
| P3 `.gitignore` does not cover `prototypes/out/` | premise | ✅ TRUE | `git check-ignore -v prototypes/out/_ap43.log` → no match; 892 files show as `??` |
| P4 The 892 untracked files carry no real board data | premise | ✅ TRUE | sweep: 892 scanned as text, **0 verbatim hits**; 680 token-only hits all generic (`change`, `layout`, `padding`, `verify`); `headroom` spot-checked → `_b41.log` "settle() keeps headroom under its bound", the layout term |
| P5 `_fixture_late.json` is synthetic | premise | ✅ TRUE | 6 projects / 16 tasks; **0 overlap** with the real board; names `Website Redesign`, `Mobile App`, `API Platform` |
| P6 `verify_board.py:launch` raises when `board_path is None`, so the automated path never reaches the fallback | **hypothesis** | ❌ **FALSE** | `launch()` does raise — but **four verifiers never call it.** `verify_ink.py:82`, `verify_widget.py:22`, `:63`, `:90` construct `TaskboardWidget()` with **no path**, so they hit the `default_board_path()` fallback and run against the live board. A fifth, `widget_slice/app.py:1514` (`__main__`), does the same. **The guard is reachable-around; the "leave as-is" decision it justified is withdrawn.** This is the row the premise table exists to produce. |
| P7 The 6 rewritten commits are clean | premise | ✅ TRUE | per-commit `git grep -c` over all 4 strings + `variants.txt` presence → 0 / absent on all 6 |
| P8 `docs/sample/report-example.html` (tracked, public) is synthetic | premise | ✅ TRUE | 0 verbatim matches; its vocabulary is the fixture family (`Website Redesign`, `Fix checkout 500 error`); the `KServe` token collision is coincidence — the operator's board does hold one task naming that product, and **none of its wording appears in the HTML** (checked by string containment, not quoted here: AC6 forbids this file from carrying it) |
| P9 No test today would catch a re-leak | **hypothesis** | ✅ TRUE | `grep -rlin "privacy\|leak\|real board\|live board" tests/` → matches are unrelated prose; no assertion over tracked-file content exists |
| P10 A test that reads `~/.taskboard/board.json` auto-skips where the file is absent | premise | ✅ TRUE by construction | this is why AC3 splits **tested detector** from **executed sweep** — an auto-skipping guard is the vacuous check this repo already recorded as an anti-pattern |

**P6 blocks §4's "leave as-is" row only.** It does not block AC1–AC5.

## 6. Security flags

| pattern | matched | handling |
|---|---|---|
| `pii` / `personal data` | ✅ the operator's own task titles and project names | the whole batch is the mitigation; AC4 + AC6 are the evidence |
| `sanitize` / `escape` | ❌ | — |
| `secret` / `credential` / `.env` | ❌ | swept today: no email, no handle, no surname in any tracked file |

`security_required: true` → a security pass runs at Phase C against AC4/AC6, and
the closing artifact states residual risk explicitly.

## 7. Increments (≤5 files each)

1. **The detector, tested against a planted leak** — sweeper + its test (AC3).
2. **Capability + fixture** — `capture.py`, `verify_variants.py`, track the
   fixture, test that both refuse the fallback (AC1, AC2).
3. **The fallback dies** — `widget_slice/app.py` constructor requires a path,
   `__main__` opts in explicitly, 4 verifier sites named a fixture (AC7).
4. **The accident** — `.gitignore` with negations, test (AC5); execute AC4/AC6
   and record.

**4 increments is the fast-flow ceiling** (the escape hatch triggers above 3
in Phase B). Increment 3 exists only because P6 came back FALSE at the gate. If
increment 3 turns out to touch more than 5 files, I stop and propose promotion
to `/dev-flow` rather than widening silently.

## 8. Batch status

| field | value |
|---|---|
| Current phase | **CLOSED 2026-08-07** |
| Branch tip | `f5f0e81` — 164 green · **not pushed** |
| Landed on `main` | `6083c01` + `b5f30e9` — 739 green · **not pushed** |
| Merged | **NO — deliberately.** See §10 |

## 9. Acceptance criteria — executed

| AC | verdict | evidence |
|---|---|---|
| AC1 capability | ✅ | `capture.py` exits **0** with the fixture, **1** without; `verify_variants.py` prints ALL CHECKS PASSED, exit 0. Symbol absent from both. 4 mutations kill |
| AC2 fixture in git | ✅ | `git ls-files --error-unmatch` succeeds; it was untracked before this batch |
| AC3 detector can fail | ✅ | 8 tests, planted leak in both directions; **7 mutations, all killing** |
| AC4 sweep executed | ✅ | every commit in `b3cc60d..kanban-variants` (11) → **0 leaking**; `main@caa4bab` and `@6083c01` → **0**. `694f38a` and earlier still leak — carried, needs force-push |
| AC5 accident blocked | ✅ | `git status -uall` 892 → **0**; 4 mutations kill |
| AC6 no artifact leaks | ✅ **after 3 failures** | the spec, the detector's own test file, and the backlog entry each carried real strings and each was caught by AC3's sweeper |
| AC7 no implicit fallback | ✅ | `TaskboardWidget()` raises; 4 bypass sites named a fixture; 3 mutations kill. `verify_widget` 105 PASS; `verify_ink` glance column unchanged vs the live board (9/11 below floor **both ways** — pre-existing) |

## 10. Why the merge did not happen

`continua hasta el merge` was attempted and **aborted with measurements**:
**80 files, 44 132 insertions, 4 conflicts** (`taskboard/app.py`,
`tests/test_app.py`, `.gitignore`, `.fast-dev-flow/spec.md`). It would place
`prototypes/` beside the existing `_prototypes/` and resurrect the inline
`HelpScreen` that `taskboard/keymap.py` replaced — the outcome the operator
ruled against earlier the same day, now with numbers behind it. The **portable
part was cherry-picked instead**: the detector is on `main`. Anything else from
this branch is a cherry-pick, not a merge.

## 11. Self-defects this batch produced

Recorded because they are the batch's own evidence that hand verification is
not defence:

1. The **first history rewrite was incomplete** — whole-token substitution left
   a truncated form in all 6 commits. Found by the test suite, not the scrub.
2. **Two of this batch's own tests were vacuous on their first mutation run**:
   `board_strings`'s sort order (no nesting pair in the fixture) and every
   `.gitignore` negation (`git check-ignore` answers from the INDEX, so a
   tracked file never reports ignored).
3. **Three artifacts of this batch leaked** — the spec, the detector's test
   file, the backlog entry. The second was invisible to the first sweep only
   because the file was still untracked when it ran.
4. Renaming the detector's fixture **made a passing test vacuous** (it planted
   words from the old fixture, which then matched nothing).
