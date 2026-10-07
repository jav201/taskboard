# Increment 001 — LLR-604.1 · The cascade engine in the model

| Field | Value |
|---|---|
| Batch | `2026-10-06-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | `single lane` |
| Requirement(s) | `LLR-604.1` |
| Acceptance | white-box `TC-618..TC-630` · black-box `AT-607..AT-611` arrive with increments 002/003 (the V2 station-expected reds) |
| Agent | `software-dev` |
| Date | `2026-10-06` |

---

## 1 · What changed

The cascade engine the whole batch stands on: `plan_move` / `apply_plan` / `snapshot` /
`restore` / `resolve_mode` + the `Plan` record, added to `taskboard/models.py` beside the links
it consumes (`link_overlap` now delegates to the engine's `_cascade_overlap` on the STORED
dates — one rule, the screen untouched). The prototype's engine (`kg_mejoras/cascade.py`),
ported with its four declared adaptations: the shipped `Task.milestone` (not `extra`), the
milestone carve-out dropped from the measure (D-633 — one measure, the painted one),
`new_conflicts` carrying the ADDED days (`ov_new − ov_old`), and the undated-task today base.
No surface changes — the user cannot reach this code yet; increments 002/003 wire it to the
`+`/`-` bump, the editor, `m`, and the toast.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-604.1 | the engine (new block after `link_conflicts`) + `link_overlap` delegates to `_cascade_overlap` (C-3) |
| `tests/test_cascade.py` | test | TC-618..TC-630 · LLR-604.1 | 13 new nodes, the prototype's scenarios re-run against the shipped board |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 0 (outside the count) |

## 3 · How to test

```powershell
$env:PYTHONIOENCODING = "utf-8"   # or the verify scripts die with UnicodeEncodeError
python -m pytest tests/test_cascade.py -q     # 13 passed
python -m pytest tests -q                     # 2499 passed (the increment's gate)
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` | TC-618..TC-630 | 13 passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` | TC-618..TC-630 | 13 passed |
| **B · black-box** `AT-NNN` ↔ story | `core` | — | not this increment (V2 station-expected red) |

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the increment's whole engine — `plan_move` does not exist on the base tree; both review-fold fixes also carried a RED (C-1: `KeyError ('w1','p1')`) |
| Instrument | project code: a script in the project's stack (the suite) · restore checked by hash |
| Where it ran | **my own tree** — no other session reading it |
| Transcript | `evidence/inc001-red-on-base.txt` (collection error, plan_move absent) · `evidence/inc001-c1-red.txt` (TC-629/630 RED against the C-1/C-2 bugs before the fixes) |
| Restore proven by | `evidence/inc001-frozen.sha256` (`models.py` hash returns to the frozen value after every battery pass) |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` throughout |
| Arms resolved at baseline | 13 — asserted by the battery's baseline control (a non-green baseline aborts the battery) |
| Verdict granularity | per resolved node id — 13 node ids in `tests/test_cascade.py` |
| Arms that stayed GREEN | none — every mutant reddens at least one arm |

| Field | Value |
|---|---|
| **RED counterfactual** | the absent engine: every TC-618..630 node fails to import on the base tree (`inc001-red-on-base.txt`); plus the two review-fold REDs (C-1 KeyError, C-2 AttributeError — `inc001-c1-red.txt`) · restore digest in `inc001-frozen.sha256` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 10 mutants, 10 KILLED, 0 SURVIVED (M1 strict-in-disguise · M2 done join · M3 milestone keeps start delta · M4 override ignored · M5 totals-not-added · M6 no today base · M7 start arm drops +1 · M8 restore writes nothing · M9 together never pulls back · M10 non-transitive downstream) · 1 BAD by design (M11 — the harness's own non-application proof) · `inc001-mutations-r3.txt` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the mutation harness's baseline control | a suite that is not green (the run before the env fix: every pytest invocation died with `OSError: [WinError 10106]`) | `AssertionError: BASELINE NOT GREEN` — aborted before any mutant verdict, in `inc001-mutations.txt` (the false-KILLED run that preceded the fix) |
| the mutation harness's anchor check | M11, whose anchor text does not exist in models.py | `BAD` — reported as non-application, never as a verdict, in `inc001-mutations-r3.txt` |
| the engine's own RED arms | the C-1/C-2 bugs before the fixes | `KeyError: ('w1', 'p1')` / `AttributeError`, in `inc001-c1-red.txt` |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown RED before its first PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the plan's JSON dump | `json.dumps([Board._to_dict(t) ...], sort_keys=True)` before/after apply+restore (TC-623) | byte-identical — the undo's promise on the emitted serialization |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 1 artifact (the plan's applied serialization), asserted on the emitted form |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| base-tree RED (engine absent) | `evidence/inc001-red-on-base.txt` | `fac1ba0e860469d1640f07abe9f2e52f1c3fc9b0749573276a6c1682208f577f` |
| review-fold RED (C-1/C-2) | `evidence/inc001-c1-red.txt` | `832d9d59a0a98f5fd224bf744db88cf508b673abd03e72e52fba35bc7fa97612` |
| mutation battery r3 | `evidence/inc001-mutations-r3.txt` | `c68b2f295ee585c6ec4a1363d51720f14b52578293eebd21734cf262cd805879` |
| increment gate (full suite) | `evidence/inc001-gate.txt` | `e3ea6330726ab3a6f2af5b7242f271b62344e0cf9dffe1d02bcf02f2e8e20f07` |
| AT oracle (the executed thresholds) | `evidence/p1-thresholds.txt` | `5f24f9885fce37d8c77767067d0d7b3bf484da33a252fa336168c44fb301b0ce` |
| frozen tree | `evidence/inc001-frozen.sha256` | the file's own lines |

| Field | Value |
|---|---|
| **Evidence files** | 6 artifacts at the declared home, digests of the stored bytes cited |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | no |
| If the result is an ABSENCE, what made the search wide enough | — |
| Guard labelled as protecting a CONCLUSION, not a behaviour | — |
| Conjunctive criteria: one mutation per conjunct | no conjunctive criterion |
| Synthetic instance of the absent case | — |
| **Positive control for every probe that returned an ABSENCE** | — |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl "plan_move\|resolve_mode\|apply_plan\|snapshot\|restore\|Plan" tests/` | `tests/test_cascade.py` (this increment's own) |
| B2 file moved on disk | `git status` | no file moved |
| B3 byte-identical golden captures this source | `grep -r models.py tests/goldens 2>$null` | no `tests/goldens` directory |
| B4 artifact produced here is consumed elsewhere | `grep -rl "plan_move" taskboard/` | `taskboard/models.py` only — the consumers (app.py) arrive in increment 002 |
| A3 | `grep -rn "link_overlap" taskboard/ tests/` | the delegation changed `link_overlap`'s BODY, not its interface; its consumers (`views.py`, `modals.py`, the links tests) keep their behavior — verified by `test_links.py` green and the reviewer's 12-input equivalence battery |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run; the one hit (A3, internal delegation) re-validated by the full links suite and the equivalence battery |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the overlap rule implemented twice (C-3) | every overlap computation in the product | `grep -rn "link_overlap\|_cascade_overlap\|cascade.overlap" taskboard/` | 3 (the two rules + the engine's planned-dates seat) | 1 (`link_overlap` delegates) | `_cascade_overlap` remains the single rule; the planned-dates call is the engine's design |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated before its site was edited |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the duplicated overlap rule | `link_overlap`'s old body (the `if pdue is None` chain) | yes — the delegation references `_cascade_overlap` | `taskboard/models.py:1812-1819` |

### Signed-balance test ledger

`post = base − deleted + added` → `2499 = 2486 − 0 + 13` ✓ reconciles (the increment's own gate)

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with `agents/code-reviewer.md` · r1 BLOCK-UNTIL: C-1 HIGH (KeyError on a first overlap pair) + C-2 MEDIUM (vanished task) + C-3 MEDIUM (rule twice) · fixed RED-first under the standing authorization's second exception (the increment was under construction), C-4/C-5 noted · r2 **PASS-WITH-NOTES**: C-1/C-2/C-3 VERIFIED on the diff, the 12-input equivalence battery clean, no new defect · C-5 carried: `plan_move` stays strict on a missing moved-task id — the app gates before `m` re-applies |

---

## 5 · Risks

- The engine is unreachable from the shipped surface until increment 002 — a latent risk the
  V2 station-expected reds state honestly.
- C-4's note accepted: the engine collapses a milestone's start==due on plan while the screen
  reads the stored start; a hand-edited file with `milestone: true, start ≠ due` can make the
  engine and the painted `↳` disagree by the delta. Junk-only; `set_milestone` enforces the
  invariant on every edit.
- `plan_move` raises on a moved-task id that vanished between the move and `m` — the app
  increment gates this (LLR-604.4's error arm).

## 6 · Pending items / spec deviations

- C-5 (LOW) carried to increment 002: the `m` handler gates `task_by_id` before re-applying.
- The ATs (V2 reds) — increments 002/003.

## 7 · Suggested next task

Increment 002 (LLR-604.2/LLR-604.4): the `+`/`-` bump routes through the cascade with the C-3
toast and one undo entry, and `m` re-applies the last move under the next mode — AT-607,
AT-608.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|
| 1 | ≤4 source files, or reason declared | ✓ | 1/4 (§2) |
| 2 | Tests written in this same increment | ✓ | `tests/test_cascade.py` in the same pass |
| 3 | Layer 0 written where the criterion applies | ✓ | TC-618..TC-630, 13 nodes, cyclomatic ≥3 |
| 4 | **RED counterfactual** declared | ✓ | `inc001-red-on-base.txt` + `inc001-c1-red.txt` + frozen hashes |
| 5 | **Reverse census** declared | ✓ | §4's five probes |
| 6 | `code-reviewer` passed | ✓ | r2 PASS-WITH-NOTES (§4b) |
| 7 | No file from another lane touched | ✓ | single lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | ✓ | `link_overlap`'s body delegating is not a frozen-interface change — its behavior is byte-identical (the reviewer's 12-input battery) |
| 9 | Coverage claims verified **on disk** | ✓ | 13 nodes run, counts in `inc001-gate.txt` |
| 10 | Load-bearing emptiness declared | ✓ | none (§4) |
| 11 | **Mutation verdicts** declared | ✓ | 10 KILLED · 1 BAD · 0 SURVIVED, per mutant in `inc001-mutations-r3.txt` |
| 12 | **Instrument RED-proof** declared | ✓ | 3 instruments shown RED first |
| 13 | **Correction population** declared | ✓ | the C-3 correction, enumerated before the edit |
| 14 | **Emitted-form assertion** declared | ✓ | the plan's applied serialization (TC-623) |
| 15 | **Independent review** names somebody | ✓ | `code-reviewer`, spawned generic agent (§4b) |
| 16 | **Evidence files** declared | ✓ | 6 artifacts with digests (§4) |
