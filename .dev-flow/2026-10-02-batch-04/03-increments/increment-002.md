# Increment 002 — HLR-402, HLR-404 (LLR-402.1..3, LLR-404.1, LLR-404.2) · control bytes stripped at the doors; a shared config cannot act or crash

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`. Revision 4 of the
> increment (operator ruling at the P3 gate, 2026-10-03: "Corregir todo en el 002").

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-04` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-402 (LLR-402.1, LLR-402.2, LLR-402.3), HLR-404 (LLR-404.1, LLR-404.2); §6.5 A-5; D-404, D-408, D-410, D-412, D-414, D-416..D-419 |
| Acceptance | AT-404, AT-405, AT-407 · white-box TC-407, TC-408, TC-409, TC-410, TC-413, TC-414, TC-416, TC-418, TC-419 · unit TC-407 ×256 (layer 0) |
| Agent | `software-dev` (this runtime's implementing agent); `tester` authored AT-407 |
| Date | `2026-10-03` |

---

## 1 · What changed

**No control byte gets in, and a teammate's shared files can no longer act on, crash or grow
anyone's board.** Every string read from the board file, a teammate's file, the team config (also
where the Setup view reads it) and the clipboard passes ONE rule, `models.strip_controls`: C0 but
tab and newline, DEL and C1 removed (a CR-LF keeps its newline), nothing else touched — so an ESC
sequence in a title or a note never reaches the terminal, and what the app pushes reaches a teammate
clean. A synced project's name, colour, status and dates are applied only when present and only
through the loading rule (`Project.from_dict`, which now also refuses non-text names and dates,
any-type colours and non-boolean flags); refused input leaves the field as it was; the first entry of
an id wins; an empty id — literal or once cleaned — is refused (F1: it grew the board by one project
per sync tick). The roster passes `clean_roster` (one entry per id, a text name or the id, a palette
hue or `mut`), read by every roster consumer including Setup, which now also stages the board's
validated values rather than raw synced fields (F3). A file nested deeper than the cleaning can follow
is refused like any unreadable one: `team.json` with a visible toast, a teammate file skipped, the
board file quarantined — it crashed every teammate's startup in revision 1 (S4-1).

Closes S-1 (HIGH) with increment 001 — `security-reviewer` verified with transcripts.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-402.1, LLR-402.2, LLR-404.1 | NEW `strip_controls`, `clean_strings`; the clipboard cleaner uses the rule; `project_color_on_load` any type; `Project.from_dict` name/date/flag checks; `Board.load` cleans inside its error handling |
| `taskboard/team_sync.py` | source | LLR-402.3, LLR-404.1, LLR-404.2 | `_read_json` cleans inside its error handling; NEW `clean_roster`; `roster()` via it; `apply_config_to_board`: present keys only through `from_dict`, refused input unchanged, `archived` bool only, first entry per id, empty id refused |
| `taskboard/app.py` | source | LLR-402.3, LLR-404.1, LLR-404.2 | Setup reads `team.json` through `_read_json`, its roster through `clean_roster`, stages the first entry's validated values; a visible toast for an unreadable `team.json`; `import json` dropped |
| `tests/test_control_bytes.py` | test | HLR-402, LLR-402.1, LLR-402.2, LLR-402.3 | NEW: TC-407 ×257, TC-408 ×2, TC-409 ×2, TC-410 ×2, TC-414, TC-419, AT-404, AT-405 |
| `tests/test_sync_fields.py` | test | HLR-404, LLR-404.1, LLR-404.2 | NEW: TC-413 (matrix ×36, absent keys, new/duplicate ids, any colour ×6, empty ids ×3, sync ticks), TC-416, TC-418 |
| `tests/test_markup_sites.py` | test | HLR-404, LLR-404.1, LLR-404.2 | NEW node (`tester`): AT-407 (48 runs) |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 3 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_control_bytes.py tests/test_sync_fields.py tests/test_markup_sites.py -k "not AT_401 and not AT_402 and not AT_403"
python -m pytest -q -p no:cacheprovider
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (cyclomatic ≥3, or crosses a declared module boundary) | `core` · `full` | TC-407 ×256 (`strip_controls` over U+0000..U+00FF) + its shapes node; TC-413 any-colour ×6 | 263 passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-408..410, TC-413 (matrix and arms), TC-414, TC-416, TC-418, TC-419 | 52 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-404, AT-405 (the C-12 chain), AT-407 (48 runs) | 3 passed |

Gate run on the frozen r4 tree (`evidence/inc002-frozen-r4.sha256`, 6/6 OK), the next increment's
new file deselected: `python -m pytest -q -p no:cacheprovider --deselect tests/test_details_grid.py` →
**2206 passed, 1 failed, 7 deselected in 351.84 s**; the one failure is
`tests/test_app.py::test_win_clipboard_roundtrip` (its SETUP message names the environment, as on base) —
`evidence/inc002-green.txt`.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | (a) the pre-fix tree (increment 001, no increment-002 code) with this increment's nodes; (b) the frozen r1 tree with revision 2's nodes; (c) the batteries below |
| Where it ran | (a) the live tree before any increment-002 product edit (nothing else measuring it); (b), (c) scratch `git archive` exports |
| Transcript | `inc002-red-prefix.txt` (281 failed / 29 passed — the 29 are valid-value and pre-guarded `archived` pins); `inc002-at407-red-prefix.txt` (AT-407: 47 of 48 runs RED; boundary case (d) a pin); `inc002-red-r2.txt` (on r1: F1 ×4, TC-418, TC-419 RED; TC-410's keep-everything arm passes by design — RED by R7/R8) |
| Restore proven by | the battery's per-mutant sha256 check (all OK) |
| Bytecode cache | `-B`, `-p no:cacheprovider`, `PYTHONDONTWRITEBYTECODE=1` |
| Arms resolved at baseline | 318 nodes (310 mine + AT-407's node; AT-407 runs 48 cases inside it) |
| Verdict granularity | per node (`-rA`); AT-407 per case inside the node |
| Arms that stayed GREEN | named above: 29 pins on the pre-fix tree, AT-407 (d), TC-410's keep-everything arm on r1 |

| Field | Value |
|---|---|
| **RED counterfactual** | the pre-fix tree with this increment's nodes: 281 RED (`evidence/inc002-red-prefix.txt` sha256 `30d2dd22…`), AT-407 47/48 RED (`inc002-at407-red-prefix.txt` sha256 `31ddeee3…`); revision 2's nodes on the frozen r1 tree: 6 RED (`inc002-red-r2.txt` sha256 `9c8f0568…`); the live tree was measured before any product edit and the exports are discarded (restore n/a), the battery's restore digests are in its transcripts |

| Field | Value |
|---|---|
| **Mutation verdicts** | revision 1 battery `inc002-mutations.txt` (sha256 `64c64f4d…`): 22/23 KILLED, N4 SURVIVED — an equivalent mutant (the CR-LF replace was dead; deleted in revision 2). Revision 2 battery `inc002-mutations-r2.txt` (`729ac461…`; run 1 aborted on a moved anchor, kept as `inc002-mutations-r2-run1-aborted.txt`): N1–N3, N5–N23 and R1–R4 KILLED (rule, doors, from_dict checks, apply_config guards, roster, Setup reads, empty id, deep-file catches, visible toast); R5, R6 SURVIVED — the two F3 guards masked each other in TC-418's fixture; R7/R8 BAD (anchor). Fixture fixed (r4) and `inc002-mutations-r4.txt` (`26854dfa…`): R5, R6, R7, R8 KILLED (R7/R8 = F2's over-stripping mutants, each turning `test_TC_410_the_rule_strips_nothing_else` RED). Net: 30/30 KILLED on the final tree, 1 equivalent mutant removed with its dead code |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the `_dirty` fixture (TC-408/TC-410) | its first form dirtied schema keys too | TC-410 PASSED on the pre-fix tree — caught as vacuous (an empty board), fixture rewritten, then RED for the stated reason (§5) |
| `mutate.py` | the revision-2 spec with a moved N13 anchor; R7/R8 with literal tab/newline chars | `mutation site not unique / absent`, battery stopped (`inc002-mutations-r2-run1-aborted.txt`; `inc002-mutations-r2.txt` R7) |
| TC-418 | the R5/R6 mutants | SURVIVED — the fixture masked one guard with the other; rewritten so each is observable (r4: both KILLED) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown reporting a failure before its pass was believed (table above) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the saved `board.json` | AT-404 / TC-410 parse the file the app wrote and assert its strings (json writes ESC as `\u001b`, so a raw-byte search would be vacuous — Q-5) | 0 control bytes; a saved board byte-identical after load + save |
| the pushed `board.<user>.json` | AT-405 re-reads the file app A wrote and feeds it unchanged to a second `TeamState` and a second app | 0 control bytes; the teammate's title painted `Ship[5m it now` |
| the republished `team.json` | TC-409 / TC-418 parse the file Setup wrote | clean strings; the first entry's validated values |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted against the form its producer emitted (table above) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| gate run, frozen r4 | `.dev-flow/2026-10-02-batch-04/evidence/inc002-green.txt` | `2ce9a424fd6dd8d175cd5da23f08bd8e8c1448b9c8608b922d55dc5f676a6867` |
| pre-fix RED (mine) | `.dev-flow/2026-10-02-batch-04/evidence/inc002-red-prefix.txt` | `30d2dd227847b1ebeaf6f3f13b92758b4bf33a80ca7ded69c41b98696d89b203` |
| pre-fix RED (AT-407) | `.dev-flow/2026-10-02-batch-04/evidence/inc002-at407-red-prefix.txt` | `31ddeee3ad2d5eb9590a62d952b0b2868c2078cd5a0b7bab69d03a46b55644c1` |
| revision-2 RED on r1 | `.dev-flow/2026-10-02-batch-04/evidence/inc002-red-r2.txt` | `9c8f056837d4ed68ebcbf6fad4a8e20699df3b87a1666368486e28c9945e8dab` |
| battery r1 | `.dev-flow/2026-10-02-batch-04/evidence/inc002-mutations.txt` | `64c64f4d8a7a316b826667dad4a025d7bea4d24eab736b7573f09fc40620e33a` |
| battery r2 | `.dev-flow/2026-10-02-batch-04/evidence/inc002-mutations-r2.txt` | `729ac461de56ae7415445804691dcf58000cf1bc1726664df8f7179bf357989f` |
| battery r2, run 1 (aborted) | `.dev-flow/2026-10-02-batch-04/evidence/inc002-mutations-r2-run1-aborted.txt` | `207e66efa07218ba19a542b7daa691abe1c91e19a5ea33ab99ce8a68973184e5` |
| battery r4 | `.dev-flow/2026-10-02-batch-04/evidence/inc002-mutations-r4.txt` | `26854dfaccc3f3c6e72e1f10cb7579c76a7b65d5ce4d4ca41c6a18da5c67e272` |
| suite on r3 (kept) | `.dev-flow/2026-10-02-batch-04/evidence/inc002-green-r3.txt` | `0f321d08f1dbc82ede64431712f9140e53101eabe9516a8070ddd9feb04e9c7f` |
| frozen set r4 | `.dev-flow/2026-10-02-batch-04/evidence/inc002-frozen-r4.sha256` | `04f6e76ad9fcfc6e1df0e029b6a05ded3230afb5dc9a5526d892435ce6f9c248` |

| Field | Value |
|---|---|
| **Evidence files** | 10 artifacts at `artifact_homes.evidence`, each cited with the digest of its stored bytes (table above); home paths redacted before hashing |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "0 control bytes" in the loaded model, the saved and pushed files |
| If the result is an ABSENCE, what made the search wide enough | TC-408 plants a control byte in EVERY string value and free-form key of a board file (the set derived by walking the JSON, its size asserted ≥ 15) and asserts the loaded board's size so an empty load cannot pass |
| Guard labelled as protecting a CONCLUSION, not a behaviour | TC-408's `_dirty` docstring (why schema keys stay intact) |
| Conjunctive criteria: one mutation per conjunct | the rule (N1–N3, R7, R8), each door (N6, N7, N8, N23), each from_dict check (N9–N12), each apply_config guard (N13–N17, R1), the roster (N18–N22), Setup (R5, R6), the deep-file catches (R2–R4) |
| Synthetic instance of the absent case | `_dirty(...)` boards and teammate files; `_nested(1000)` |
| **Positive control for every probe that returned an ABSENCE** | the pre-fix tree: 281 RED (`inc002-red-prefix.txt`) |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln -e _clean_clipboard_text -e "roster()" -e member_names -e member_hues -e apply_config_to_board -e Project.from_dict -e _read_json tests/` | `test_app.py:1135-1147` (clipboard arms hold: no CR asserted), `test_team_sync.py` (set of roster ids; valid synced values still apply), `test_setup_help.py` — all re-validated green (code review, 603 passed) |
| B2 file moved on disk | `git diff --name-status HEAD -- taskboard tests \| grep ^R` | 0 |
| B3 byte-identical golden captures this source | `ls tests/goldens` | no such directory |
| B4 artifact produced here is consumed elsewhere | the saved board file and the pushed `board.<user>.json` (read by teammates), the republished `team.json` | AT-405 (C-12 chain) and TC-409/TC-418 assert the consumers' view |
| A3 | interface consumed by another module changed | `grep -rn "roster()\|_read_json\|clean_roster" taskboard` | `TeamState.roster` keeps its signature (now cleaned); `_read_json` keeps its contract (never raises, None when unreadable); `clean_roster` NEW, read by `team_sync` and `app` |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3, each with its command and verdict: B1 three test files hit, every hit re-validated; B2, B3 0 hits; B4 three artifacts with their consumer-side assertions; A3 two signatures kept, one new reader |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| text entering without the rule | every place a file or the clipboard is read into the app | `grep -n "json.loads\|read_text\|_clean_clipboard_text" taskboard/*.py` (P2 architect and security door census) | 5 (`models.py:872`, `team_sync.py:33`, `app.py:1007`, `history.py:60`, the clipboard) | 4 | `history.py` — legacy records, never painted (D-409, BACKLOG) |
| synced fields set raw | every `setattr`/copy of a synced project or roster field | `grep -n "setattr\|tp.get\|r.get(\"name\|r.get(\"hue" taskboard/team_sync.py taskboard/app.py` | 4 | 4 | 0 |

| Field | Value |
|---|---|
| **Correction population** | 2 corrections, each enumerated before its first site was edited (table above) |

### Signed-balance test ledger

`post = base − deleted + added` → `2207 = 1889 − 0 + 318` ✓ reconciles (the next increment's
`tests/test_details_grid.py` deselected from this gate run)

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` · OK to advance after four rounds on frozen sets (`inc002-frozen-r1..r4.sha256`): round 1 `BLOCK-UNTIL: F1` (F1 HIGH: a control-byte-only synced id cleaned to `""` and grew the board per sync tick — STOPPED and reported; operator ruled "Corregir todo en el 002"; folded with RED-first tests, verified round 2), F2, F3 MEDIUM and F4 LOW folded, F5 LOW folded r3, F6 LOW declared (D-419); round 2 OK (G1 MEDIUM, G2 LOW folded r3); round 3 OK; round 4 OK (TC-418 fixture). `security-reviewer` · PASS-WITH-NOTES twice: CLOSED S-1 (HIGH) with transcripts; S4-1 MEDIUM folded and CLOSED with boot transcripts at depths 990/2000/50000; S4-2..S4-4, S5-1 LOW → BACKLOG; S5-2 folded (= G1) |

---

## 5 · Risks

- The `_dirty` fixture first dirtied schema keys and made TC-408/TC-410 vacuous on the pre-fix tree; caught before the fix landed (§4 Instrument RED-proof). The final fixture asserts the loaded board's size.
- A hand-edited board file holding `""` / non-text names, non-text dates or non-boolean flags is normalised on load and rewritten on the next save (D-410); a control-only project id loses its tasks' links (D-419).
- `clean_roster` accepts any palette key, alert tones included (S4-2, BACKLOG); Setup saving over an unreadable `team.json` resets its version (S5-1, BACKLOG).
- The depth at which a nested file is refused depends on the stack depth at the read; refused or read, never a crash (security, executed).

## 6 · Pending items / spec deviations

- Contract amendment §6.5 A-5 (ledger LED .11); D-416..D-419.
- BACKLOG at close: S4-2, S4-3, S4-4, S5-1; `history.jsonl` (D-409); `Task.from_dict` synced dates untyped (code review note).

## 7 · Suggested next task

Increment 003 — the details grid rule (LLR-403.1; TC-411, AT-406), before/after captures for PV-1.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 3 / 4 |
| 2 | Tests written in this same increment | all | ✓ | §2: 3 test files |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | TC-407 ×256 over `strip_controls`; TC-413 any colour; `clean_strings`/`clean_roster` covered by TC-407 shapes and TC-416 |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 field |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 field |
| 6 | `code-reviewer` passed — a HIGH blocks | `core` · `full` | ✓ | §4b: F1 HIGH folded and verified; OK to advance (round 4) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | `_read_json` / `roster()` contracts kept (§4 A3) |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | 318 nodes collected and passed in `inc002-green.txt` |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 C-55 table |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 field: 30/30 on the final tree, N4 equivalent removed |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 table: 3 instruments |
| 13 | **Correction population** declared | all | ✓ | §4 table: 2 corrections |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 table: 3 artifacts |
| 15 | **Independent review** names somebody | all | ✓ | §4b: `code-reviewer`, `security-reviewer` |
| 16 | **Evidence files** declared | all | ✓ | §4 table: 10 files |
