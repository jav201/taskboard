# Increment 002 — LLR-604.2 · LLR-604.4 · The bump moves the chain; `m` changes the mode

| Field | Value |
|---|---|
| Batch | `2026-10-06-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | `single lane` |
| Requirement(s) | `LLR-604.2` · `LLR-604.4` |
| Acceptance | black-box `AT-607` · `AT-608` · regression `TC-631` |
| Agent | `software-dev` |
| Date | `2026-10-06` |

---

## 1 · What changed

The `+`/`-` bump no longer nudges one date in silence: it plans the cascade for the
resolved mode (the moved task's project's `date_links`, default `push_delta`), applies it,
pushes ONE multi-task undo entry, saves atomically when the write touches more than one
task (D-634, on the apply and on the undo's restore), and says what happened on the C-3
toast ladder — names when they fit (`pushed Add push, Offline sync +1d each` at 118), a
count when they do not (`pushed 2 +1d each` at 80), the project's further slip
(`Mobile +1d past ◆`), the narrowing `· u undo · m change for this move` suffix, and the
flag clause with the ADDED days (`flagged Add push +1d`). `m` re-applies the last move
under the next mode (flag → push_delta → together → flag), refusing — verbatim, writing
nothing — when no date move tops the undo stack or the moved task is gone (C-5). The toast
is PLAIN TEXT (`markup=False`): the shipped TC-401 law forbids a markup-parsed toast, so
the prototype frame's colours stay out — the contract pins the text, not the paint.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | LLR-604.2 · LLR-604.4 | `action_due_bump` → `_apply_cascade` (the one move seat) + `_cascade_toast` (the ladder) + `action_cascade_mode` (`m`) + the `"cascade"` undo branch |
| `taskboard/keymap.py` | source | LLR-604.4 | `Key("m", "m", "cascade_mode", "Chain", group="date")`; the `M` comment now points at its lowercase |
| `taskboard/views.py` | source | LLR-604.4 | two help bullets in the kanban help_usage section |
| `README.md` | doc | — | the keybinding table carries `m` (the shipped test reads the table) |
| `tests/test_cascade_app.py` | test | AT-607 · AT-608 · TC-631 · LLR-604.2 · LLR-604.4 | 3 new nodes |
| `tests/test_colour_budget_app.py` | test | LLR-604.4 | KEYBAR_BASE's more layer re-derived (executed) with `m` added |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** (app · keymap · views) |
| Test files | 2 (uncapped) |
| Doc files | 1 (outside the count) |

## 3 · How to test

```powershell
$env:PYTHONIOENCODING = "utf-8"
python -m pytest tests/test_cascade_app.py -q     # 3 passed
python -m pytest tests -q                         # the increment's gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` | — | increment 001's engine, unchanged |
| **A · white-box** `TC-NNN` ↔ LLR | `core` | — | this increment's layer is black-box |
| **B · black-box** `AT-NNN` ↔ story | `core` | AT-607 · AT-608 · TC-631 | 3 passed |

Gate: `2501 passed, 1 failed` — the failed is `test_win_clipboard_roundtrip`, the DECLARED
environment flake G-011 (`inc002-gate.txt`). AT-607's negative control: `Offline sync`
must NOT appear at 80 columns.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the increment's whole wiring — AT-607/608 RED on the increment-001 tree (`inc002-red-on-inc001.txt`: bump moved only the due, no toast, no `m`); plus the review folds' REDs (1-1's TypeError reproduced by the reviewer) |
| Instrument | project code: the suite · restore checked by hash |
| Where it ran | **my own tree** |
| Transcript | `evidence/inc002-red-on-inc001.txt` · the reviewer's executed repros (in its report) |
| Restore proven by | `evidence/inc002-frozen.sha256` (app.py/keymap.py hashes return after every battery pass) |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` |
| Arms resolved at baseline | 3 — asserted by the battery's baseline control |
| Verdict granularity | per resolved node id (3 node ids) |
| Arms that stayed GREEN | none |

| Field | Value |
|---|---|
| **RED counterfactual** | the absent wiring: both ATs fail on the increment-001 tree · restore digest in `inc002-frozen.sha256` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 8 mutants, 8 KILLED, 0 SURVIVED (N1 bump bypasses the cascade · N2 per-task undo entries · N3 m cycles backwards · N4 m never restores first · N5 the toast never names · N6 the flag clause reports totals · N7 the refusal literal is wrong · N8 m unbound) · 1 BAD by design (N9 — the harness's non-application proof) · `inc002-mutations-r4.txt` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the full suite | the first revision's markup=True toast + the README gap + the reviewer's HIGH | TC-401 (markup census), the README-table test, and the reviewer's BLOCK-UNTIL — all red before any PASS was believed |
| the mutation harness's baseline control | a non-green suite (the r2 run's mis-anchored mutants) | the battery refused to run / reported BAD anchors instead of verdicts (`inc002-mutations.txt`, r2) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments, each shown RED before its first PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the toast's rendered text | AT-607 asserts `pushed Add push, Offline sync +1d each` at 118 and `pushed 2 +1d each` at 80 against `str(t.render())` of the painted Toast | both substrings present, `Offline sync` absent at 80 (3 passed) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 1 artifact (the toast), asserted against its rendered form at both widths |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on the increment-001 tree | `evidence/inc002-red-on-inc001.txt` | `7a25528073e7de6a48fe2d6fff3f46d6257f69f69f380e393591e45b42cb21d8` |
| mutation battery r4 | `evidence/inc002-mutations-r4.txt` | `1f1dd2e6c1dfdbe5035136b1ffef27c26b663504ba1badadf2eeefd9d2c4aa75` |
| increment gate (full suite) | `evidence/inc002-gate.txt` | `fedeceac256b2b12684f376f5c53b064ee0e69f62555d27d66878472772f879f` |
| AT oracle (executed thresholds) | `evidence/p1-thresholds.txt` | `5f24f9885fce37d8c77767067d0d7b3bf484da33a252fa336168c44fb301b0ce` |
| toast ladder oracle | `evidence/p2-arch-probe.txt` | `321e378c6903d0192470e0e4c143d4b63967b421e1d5a7a47a6b657b02105` |
| frozen tree | `evidence/inc002-frozen.sha256` | the file's own lines |

| Field | Value |
|---|---|
| **Evidence files** | 6 artifacts at the declared home, digests cited |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | no |
| **Positive control for every probe that returned an ABSENCE** | — |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl "action_due_bump\|_undo_stack\|due_bump" tests/` | test_app, test_momentum, test_milestones, test_edit_window — the bump's OLD body was their oracle; all pass unchanged (the undo-entry shape they never read; the bump's observable dates moved only for chained tasks, which their boards lack) |
| B2 file moved on disk | `git status` | none |
| B3 byte-identical golden captures this source | no `tests/goldens` directory | — |
| B4 artifact produced here is consumed elsewhere | the toast text is read by no consumer; the undo stack is session-only | — |
| A3 | `grep -rn "due_bump(" taskboard/` | `bump_due` keeps its model seat (the editor path, increment 003, still uses it); the app's `action_due_bump` changed body, same action name — no interface change |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes; the B1 hits re-validated by the full suite |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population | Enumeration method | Count | Sites edited | Sites left |
|---|---|---|---|---|---|
| every Textual sink's markup posture | every `notify(` call | `grep -n "notify(" taskboard/app.py` | 40+ | 1 (the new toast, `markup=False`) | the rest stay `markup=False` (TC-401 green) |
| every surface naming the key set | README table · key bar · help · `?` map | grep + the suite | 4 | 4 (README row · KEYBAR_BASE · kanban help · keymap) | — |

| Field | Value |
|---|---|
| **Correction population** | 2 corrections, each enumerated before its first site was edited |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the prototype-coloured toast (markup=True) | `grep -n "markup=True" taskboard/app.py` | yes — zero hits | the notify call at `app.py:1183` |
| the un-keyed `m` | `grep -n '"m"' taskboard/keymap.py` | yes | `keymap.py:101` |

### Signed-balance test ledger

`post = base − deleted + added` → `2502 = 2499 − 0 + 3` ✓ reconciles (the increment's own gate)

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with `agents/code-reviewer.md` · r1 BLOCK-UNTIL: 1-1 HIGH (toast crashed on a `None` planned due under `together`) + 1-2 MEDIUM (project clause fired on "past due", not "slips further") + 1-3 LOW (flag count form) · fixed RED-first under the standing authorization's second exception · r2 **PASS-WITH-NOTES** ("OK to advance"): 1-1/1-2/1-3 VERIFIED on the diff, TC-631 proved RED-by-construction on the old code, the plain-text rewrite changed no pinned literal · 1-4 nits noted (restore-loop reuse; unpinned mixed-shift count forms) |

---

## 5 · Risks

- `m`'s availability lives on the undo stack's top — an action between the move and `m`
  (pin, phase, link) makes `m` refuse by design; the key bar advertises `m Chain`
  regardless. The C-1 frame's in-edit cycling remains out (D-626) — the operator's visual
  verdict owns this.
- The toast counts/names forms at very narrow widths (<60) fall to the count rungs; the
  mixed-shift pushed form `pushed 2 (+3d/+6d)` is unpinned by the contract (noted, LOW).
- G-011 (clipboard flake) remains the suite's declared environmental noise.

## 6 · Pending items / spec deviations

- Increment 003 (LLR-604.3/LLR-604.5): the editor's date save routes through the cascade
  and the per-project `date_links` setting lands in the project editor — AT-609, AT-610,
  and the IFC Part B `#f-date-links` block.
- 1-4 nits ride to the backlog at close if still open.

## 7 · Suggested next task

Increment 003 (LLR-604.3 · LLR-604.5): the editor's date save and the project editor's
`Linked dates` select — AT-609, AT-610.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | ≤4 source files | ✓ | 3/4 (§2) |
| 2 | Tests written in this same increment | ✓ | test_cascade_app.py in the same pass |
| 3 | Layer 0 written where the criterion applies | ✓ | engine layer is increment 001's, untouched |
| 4 | **RED counterfactual** declared | ✓ | `inc002-red-on-inc001.txt` + frozen hashes |
| 5 | **Reverse census** declared | ✓ | §4's five probes |
| 6 | `code-reviewer` passed | ✓ | r2 PASS-WITH-NOTES (§4b) |
| 7 | No file from another lane touched | ✓ | single lane |
| 8 | Frozen interfaces untouched | ✓ | action_due_bump's body changed, its name/seat did not; `bump_due` keeps its model seat |
| 9 | Coverage claims verified **on disk** | ✓ | counts in `inc002-gate.txt` |
| 10 | Load-bearing emptiness declared | ✓ | none (§4) |
| 11 | **Mutation verdicts** declared | ✓ | 8 KILLED · 1 BAD · 0 SURVIVED, `inc002-mutations-r4.txt` |
| 12 | **Instrument RED-proof** declared | ✓ | 2 instruments shown RED first (the suite itself + the harness) |
| 13 | **Correction population** declared | ✓ | 2 corrections enumerated before their edits |
| 14 | **Emitted-form assertion** declared | ✓ | the toast at both widths |
| 15 | **Independent review** names somebody | ✓ | `code-reviewer`, spawned generic agent (§4b) |
| 16 | **Evidence files** declared | ✓ | 6 artifacts with digests (§4) |
