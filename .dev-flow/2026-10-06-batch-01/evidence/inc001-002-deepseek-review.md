# Adversarial read-only review — increments 001 + 002 (deepseek-flash)

**Reviewer:** deepseek-flash (second, independent pass). **Mode:** read-only — no repo file was
modified except this report. **Commands run:** the two cascade test files (18 passed), the full
suite once (`2504 passed in 378s`, G-011 did not fire), and ~10 standalone `python -` probes
(no scratch files written into the repo).

**Tree note / premise correction.** The brief says the editor "is NOT yet cascaded — known, by
design", but the working tree **does** contain increment 003 (`_on_task_edited` routes dates
through `_apply_cascade`, `ProjectModal` has `#f-date-links`, `modals.py` +21). I reviewed the
cumulative diff as it exists. This matters for DS-2 (the only reachable trigger is the editor
path) and for the "editor between a bump and `m`" question. I verified both editor behaviours
below rather than trusting the note.

---

## Findings

### DS-1 — MEDIUM — `_short_title` crashes on an empty/blank title
- **Where:** `taskboard/app.py:1083-1091` (`out = words[0]`, line 1086).
- **Defect:** `_short_title` indexes `words[0]` without checking `words`. A task whose title is
  `""` or whitespace-only (`split()` → `[]`) raises `IndexError`. Titles are **not** guaranteed
  non-empty by the lenient load: `Task.from_dict` does `d.get("title", "Untitled")`
  (`models.py:857`), so a board file (or a teammate push) carrying `"title": ""` loads with an
  empty title — the "never raises on load" contract holds, but the first cascade toast that
  names that task as a dependent/waiter raises. Impact: the C-3 toast never appears (the move
  itself is already applied and saved), so the user gets a silent, unexplained move.
- **Fix:** `words = t.split(); if not words: return ""` (or `return t.strip()[:n]`).
- **Repro:** **EXECUTED.** Direct `_short_title("",12)` / `_short_title("   ",12)` →
  `IndexError`. Full app path on a `kg_board` board with `tm3.title=""` + `action_due_bump(1)`
  → traceback `action_due_bump → _apply_cascade → _cascade_toast → _short_title IndexError`,
  and via `pilot.press("+")` the exception is swallowed (Textual) and `app.screen.query("Toast")`
  is empty. The dates *did* move.

### DS-2 — MEDIUM — the toast formats `None` when the moved task has no due (`_md(None)`)
- **Where:** `taskboard/app.py:1101` (`nd = plan.moved[task.id][1]`) and `app.py:1145`
  (`f"▌{title} due {_md(nd)} ({plan.shift[task.id]:+d}d)"`).
- **Defect:** `_md` is `f"{d:%b} {d.day}"` (`app.py:38`). When a move has `due_delta == 0` on a
  task whose due is `None`, `plan_move` keeps `moved[task] = (start±k, None)` and the lead
  formats `None` → `TypeError: unsupported format string passed to NoneType.__format__`. The
  bump can't hit it (always `dd=±1`), but the editor can: a task with a start and **no due**,
  whose **start alone** is edited (`sd≠0, dd=0`) calls `_apply_cascade(task, sd, 0)`
  (`app.py:1878`, inc-003). The engine itself is fine (`apply_plan` skips the `None`); only the
  toast dies. Same class as DS-1: move succeeds, feedback is lost.
- **Fix:** guard the lead when `nd is None` (e.g. omit `due … (+Nd)` or print `due —`).
- **Repro:** **EXECUTED.** Shim call `_cascade_toast` on a board with one task
  `start=today, due=None` and `plan_move(b,"s1",1,0,…)` → `TypeError`. The undated-task bump
  control (`due_delta=1`) toasts correctly.

### DS-3 — LOW — `together` counts an undated dependent in the toast as "moved"
- **Where:** `taskboard/models.py:1936-1938` (`for wid in down: put(...)`, `due_delta`) with
  `put` at `models.py:1930-1934`; consumed by `_cascade_toast`
  (`app.py:1099-1100`, `1126-1141`).
- **Defect:** under `together`, every open transitive dependent is put with `shift=due_delta`
  even when it has no dates, so `plan.moved[id] = (None, None)` and `plan.shift[id] = due_delta`.
  The toast then counts/names it as moved. The contract's clause is "WHO moved … by how much";
  an undated task cannot move. TC-631 exercises exactly this case but only asserts `"moved" in
  said` and board integrity, so it does not catch the inflated count.
- **Fix:** only `put` a task whose planned dates actually differ (or filter `plan.moved` ids
  with `(None, None)` in `_cascade_toast`). Alternative: treat it as by-design and pin it.
- **Repro:** **EXECUTED.** `tm2` +1 `together` with an undated follower `u9` → toast
  `moved 5 +1d each`, while `plan.moved["u9"] == (None, None)`. (Only 4 tasks actually moved.)

### DS-4 — MEDIUM — AT-611 has no test node anywhere
- **Where:** `.dev-flow/2026-10-06-batch-01/01-requirements.md:291` (§5 table), HLR-604
  acceptance (`:183`), and `03-increments/increment-001.md:9` ("AT-607..AT-611 arrive with
  increments 002/003").
- **Defect:** increments 002/003 delivered AT-607/608/609/610; **no pytest node carries the id
  AT-611** (`grep -rn "AT-611\|AT_611" tests/` → nothing). §5 says Layer B is "AT-607 through
  AT-611, one node each", and §5.2 requires "every HLR has a passing AT". The *behaviours*
  AT-611 names are covered at unit level (TC-619/620/621/622) and thresholds were executed in
  `p1-thresholds.txt`, but the black-box AT itself is absent, so the batch cannot show its own
  acceptance criterion met.
- **Fix:** add the AT-611 node (done dependent stops the chain; milestone whole with slack
  absorbing; an earlier move pulls nothing; the cross-project arm) driving `TaskboardApp`, or
  formally fold it and amend the contract/ledger.
- **Repro:** grep only (no node).

### DS-5 — LOW — the tested `restore` is not the code path the app runs
- **Where:** `taskboard/models.py:2018-2023` (`restore`); app never imports it — `action_undo`
  hand-rolls the loop at `app.py:1280-1284` and `action_cascade_mode` at `app.py:1202-1206`.
- **Defect:** TC-623/TC-630 test `restore`, but production undo/mode-switch restores dates with
  duplicate inline loops. A change to `restore` would not change undo behaviour, so those tests
  give false confidence; the duplicated loops can drift.
- **Fix:** call `restore(self.board, snap)` in both places (and import it).
- **Repro:** grep (used only in `tests/test_cascade.py`).

### DS-6 — LOW — unused import `bump_due`
- **Where:** `taskboard/app.py:21` (`bump_due` in the import list).
- **Defect:** after inc-003 rewired the editor, nothing in `app.py` calls `bump_due` (the only
  remaining reference is the docstring at `app.py:1071`). Inc-002's reverse census A3 claimed
  "the editor path, increment 003, still uses it" — that is no longer true on this tree.
- **Fix:** drop `bump_due` from the import.
- **Repro:** `grep -n "bump_due" taskboard/app.py` → import + docstring only.

### DS-7 — LOW — `CASCADE_VERB` has no `"push"` entry
- **Where:** `taskboard/app.py:1081`.
- **Defect:** `plan_move` accepts the engine-internal `"push"`, but `_apply_cascade(mode="push")`
  would reach `CASCADE_VERB["push"]` and `KeyError` in the toast. Unreachable today (the cycle
  only offers `CASCADE_MODES`; the editor/undo pass stored modes), but it is a landmine for the
  next caller.
- **Fix:** add `"push": "pushed"`, or assert the surface never passes it.
- **Repro:** code reading (not executed).

### Observations (not defects)

- **`m` after `u`:** EXECUTED — after `+` then `u`, the cascade entry is gone from the stack,
  so `m` refuses verbatim and writes nothing. Consistent with LLR-604.4/§6.3 ("an `m` after an
  intervening action refuses by design"), but note the entry is *not* re-pushable once undone.
- **Editor between bump and `m`:** EXECUTED — a title-only editor save pushes no undo entry
  (`app.py:1882`), so the cascade entry stays on top and `m` re-applies correctly; a date-
  changing editor save pushes its own cascade entry, so `m` then re-applies the editor move.
- **`save_atomic` failure mid-cascade (`app.py:1172-1183`):** apply_plan mutates memory, the
  undo entry is pushed, then the save runs. If the save raises, memory is ahead of disk with an
  entry already pushed — the same posture every shipped single-task action has (they also mutate
  then save), so inherited, but the cascade is the first multi-task writer.
- **`m` clobbers intervening non-undoable changes:** `action_cascade_mode` restores the stored
  snapshot dates unconditionally; a team-sync tick between the move and `m` would be lost. Same
  hazard as the shipped undo; rare.

---

## Verified-clean (hunted, no defect)

- **Engine, deleted moved-task project** — `plan_move` on a board with `pmob` removed:
  no `AttributeError`; `project_over`/`resolve_mode` degrade to 0/`push_delta`.
- **Engine, moved task with no project** (`project_id=None`): no crash.
- **Engine, cycles** — a 2-cycle under `together` with a mixed dated/undated pair: no hang,
  no crash; `push_delta` on 2-cycles and a self-loop terminates (strictly-increasing shift
  guard at `models.py:1952`). Done/archived stop the chain.
- **`restore` with a vanished task / vanished project:** skips, never raises (TC-630).
- **Toast ladder at widths 24/40/60** (and 0/1/2/3): every rung is grammatical; truncation is
  `fit`'s ellipsis; the `▌` glyph survives at width ≥2 and is dropped at 0/1 (no crash). No rung
  produced a malformed count/name string beyond DS-3.
- **`project_over` populations:** the apparent asymmetry (`project_over` over moved tasks,
  `project_over_before` over all tasks) reconciles for the "slips further" comparison — verified
  by construction on several boards; not a defect.

---

## Verdict

**HIGH: 0 · MEDIUM: 3 (DS-1, DS-2, DS-4) · LOW: 4 (DS-3, DS-5, DS-6, DS-7) · Observations: 4.**

Overall confidence is moderate-to-high that increments 001+002 are structurally sound: the
engine handles the pathological inputs the brief named (deleted project, absent project, cycles,
vanished tasks), the undo/mode interlock behaves as the contract describes, and the full suite is
green (2504 passed). The material issues are all in the **reporting layer**, not the data path:
two unguarded `None`/empty-string inputs can kill the toast while leaving the move applied
(DS-1, DS-2 — both fixed with one-line guards), the `together` toast over-counts undated
dependents (DS-3), and one contract-required acceptance node (AT-611) is simply missing (DS-4).
None of these corrupts the board or breaks the one-undo-entry promise. I would not block on the
LOWs, but DS-1/DS-2 should be folded before the operator's visual verdict because both turn a
successful move into a silent one, and DS-4 must be resolved (or the contract amended) before
the batch can claim §5.2.
