# Quick Spec — `2026-08-07-fastflow-06`: land the branch, gate the sweep

**Base ref:** `b5f30e9` (main, local; `origin/main` == `caa4bab`, 2 behind)
**Branch to merge:** `kanban-variants` @ `9e94013` (164 green)
**Language:** English · **security_required: TRUE** (personal data)

## 1. Objective

Execute the five operator decisions of 2026-08-07, in the order that keeps a
safety net until it is no longer needed.

| # | decision | verbatim | effect |
|---|---|---|---|
| 1 | main's history rewrite | *"el main, ni hablar"* | **NOT DONE.** The leak stays in `main`'s history back to `5ae4d42` on a PUBLIC remote. Recorded as an **accepted risk**, not an open task |
| 2 | merge `kanban-variants` → `main` | *"Sí quiero el merge"* | **DO IT**, full merge, 4 conflicts resolved deliberately |
| 3 | git identity for future commits | *"OK"* + earlier *"en el futuro que no aparezca"* | set a `users.noreply` author address so new commits stop carrying the address |
| 4 | pre-commit gate | *"Construye"* | a hook that runs the sweep and **refuses the commit** on a hit |
| 5 | backup refs | *"Borra si ya cumplieron su propósito"* | delete **after** the merge is verified, never before |

## 2. Acceptance criteria (observable)

- [ ] **AC1 — the merge lands with its conflicts decided, not defaulted.** All 4
  conflicted paths resolved with a stated reason; `taskboard/app.py` keeps
  **main's** `keymap.py` implementation, because the operator ruled the branch's
  inline `HelpScreen` superseded. Observable: no conflict markers anywhere, and
  `taskboard/keymap.py` still present and imported after the merge.
- [ ] **AC2 — nothing regresses.** The merged tree runs **both** suites' contents
  green. Observable: one `pytest` run over the merged `tests/`, count stated,
  0 failed.
- [ ] **AC3 — the merged tree carries no board data.** Observable:
  `tools/privacy_sweep.py` over every tracked file of the merge commit → **0**.
- [ ] **AC4 — the gate refuses a real leak.** A pre-commit hook runs the sweep on
  STAGED content and exits non-zero on a hit. Observable, both directions: stage
  a file containing a real title → commit is **refused** and the file is named;
  stage a clean file → commit proceeds. Tested by executing the hook, not by
  reading it.
- [ ] **AC5 — the gate cannot be satisfied by doing nothing.** If the sweep
  errors, or the board file is absent, the hook must **fail closed with a
  message**, never pass silently. Observable: run it with the board path pointed
  at a missing file → non-zero.
- [ ] **AC6 — future commits stop carrying the address.** Observable:
  `git config user.email` returns a `users.noreply` address, and a test commit's
  `%ae` shows it. Existing commits untouched (decision 1 by extension).
- [ ] **AC7 — the safety net is removed only after it is redundant.** The four
  refs are deleted **after** AC1–AC3 pass, and the deletion is reported with what
  each held.

## 3. Out of scope

| item | why |
|---|---|
| Rewriting `main`'s history | decision 1: *"ni hablar"* |
| Pushing anything | the operator pushes |
| A server-side / CI gate | the hook is local; a bypassed `--no-verify` is not covered and this is stated, not hidden |

## 4. Premise table (C-43)

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| P1 the merge has exactly 4 conflicts | premise | ✅ TRUE | `git merge --no-commit` → `.fast-dev-flow/spec.md`, `.gitignore`, `taskboard/app.py`, `tests/test_app.py`; 80 files / 44 132 insertions |
| P2 `main`'s `taskboard/keymap.py` supersedes the branch's inline `HelpScreen` | **hypothesis** | ❓ pending | to be executed: both must not co-exist after the merge, and `tests/test_keymap.py` must still pass |
| P3 a pre-commit hook can see staged content | premise | ❓ pending | must be executed against a real staged leak, not asserted |
| P4 the backup refs are the only thing holding the pre-rewrite objects | premise | ❓ pending | `git for-each-ref` + reflog check before deleting |

## 5. Batch status

| field | value |
|---|---|
| Current phase | **B — implementing** |
| Pushed | **nothing** |
