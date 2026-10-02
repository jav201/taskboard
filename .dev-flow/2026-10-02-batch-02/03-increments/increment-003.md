# Increment 003 — HLR-204 · the app speaks English

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`. Flow pinned to rev98.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-02` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-204 (LLR-204.1; amended by LED .17, decision D-219) |
| Acceptance | AT-204 · white-box TC-206 ×8 |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**Every string the app paints is English.** The help modal (headings `Usage · Legend · Example ·
Keys`, footer, each view's usage and example), the flow view (`no history yet — it builds from
today`, `open n=N`), Setup (header, sections, labels, the `shared` chip, the hint row, every check
note) and the team filter's labels (`all · team · personal`) are translated; the stored values —
the filter's `todo`/`equipo`/`personal`, the check keys, Setup's section keys — are data and
unchanged (D-212). Every help bullet of every view now fits its 44-cell column (27 base bullets did
not). The help copy names only shipped keys (D-219: `t` pins, not `p`; the people filter has no
key). The first draft spoke to the reader ("what YOU pinned"); the app's existing law against the
second person caught it and the copy was rewritten.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-204.1 | `help_usage` rewritten, `help_example`, flow messages/labels and legend, `render_setup` copy, `TEAM_FILTER_LABELS` + `render_team_filter_chrome` |
| `taskboard/team_sync.py` | source | LLR-204.1 | `probe_setup_health` notes (and two section comments) |
| `taskboard/modals.py` | source | LLR-204.1 | `HelpModal` headings and footer |
| `tests/test_english.py` | test | HLR-204, LLR-204.1 | NEW: AT-204, TC-206 ×8 (9 nodes); derived + frozen vocabulary |
| `tests/test_flow_view.py` | test | HLR-204 | reverse census: the two flow strings (in place) |
| `tests/test_setup_help.py` | test | HLR-204 | reverse census: section names, modal headings, usage heading (in place) |
| `tests/test_team_views.py` | test | HLR-204 | reverse census: the filter's painted labels (in place) |
| `tests/test_colour_budget_app.py` | test | HLR-204, LLR-201.3 | reverse census: `SETUP_ROWS_BASE` in English, same columns |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 5 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_english.py tests/test_prism_laws.py tests/test_setup_help.py
python -m pytest -q
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | n/a — copy and one lookup dict; no 2+-path unit added | — |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-206: lexicon guard, source-literal scan, help copy + fit, shipped keys, views ×4 | 8 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-204 (every view's panel and `?` modal, team mode on; the filter through its three values) | 1 passed |

Gate run on the frozen round-1 tree: `python -m pytest -q -p no:cacheprovider` → **1643 passed in
183.38s, exit 0** (`evidence/inc003-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the increment-002 tree with the final `tests/test_english.py`; then 14 mutants on the increment tree |
| Where it ran | scratch exports |
| Transcript | `evidence/inc003-red.txt` (8 failed, 1 passed — the lexicon guard, green by design); `evidence/inc003-mutations.txt` |
| Restore proven by | per-mutant sha256, byte-exact harness `evidence/mutate_bytes.py` (`views.py` `84f73583edfd8a11…`) |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 9 |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | `test_TC_206_the_lexicon_sees_every_base_surface` (a guard of the input set) |

| Field | Value |
|---|---|
| **RED counterfactual** | 8 behaviour nodes RED on the increment-002 tree (Spanish in the help, flow, Setup, filter; 27 over-wide bullets; `p pinea`; base literals in the source scan) · `evidence/inc003-red.txt` · restore digests in `evidence/inc003-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 14 of 14 KILLED (`evidence/inc003-mutations.txt`, specs `mutants_inc003.json` 10/10 + `mutants_inc003_r1.json` 4/4): E1 heading, E2 bullet over 44 cells, E3 flow message, E4 Setup label, E5 check note, E6 modal heading (AT-204 alone), E7 stored values painted, E8 the frozen vocabulary loses a word (C-31: the input SET mutated), E9 second person, E10 an unbound key named; X1 `ninguna ruta`, X2 `escribe solo`, X3 `ceniza = reposo` (code review), X4 a stored value painted again |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `SPANISH` (painted-text lexicon) | the base surfaces (`BASE_SPANISH`, every word) | each flagged (the guard node); the increment-002 renders (8 RED nodes) |
| `WORD_ONLY` (source scan) | the base package literals | RED (`inc003-red.txt`) |
| the 44-cell fit check | the base help copy | 27 bullets over |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the help modal, every view | the `Label` widgets' rendered plain text in `run_test` | AT-204 passed |
| the painted panels (flow, Setup, standup, people) | `#board` rendered plain, under three filter values | AT-204, TC-206 views passed |
| the package's string literals | parsed by `ast` (docstrings excluded) | TC-206 source scan passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on the increment-002 tree | `.dev-flow/2026-10-02-batch-02/evidence/inc003-red.txt` | `47a72aa4e5729f432bfd28701b2a050c6ce4b8cc6fb21ad2becd7b65bc4314e7` |
| mutation battery | `.dev-flow/2026-10-02-batch-02/evidence/inc003-mutations.txt` | `217b9d0af4f8253284206f4bad41ea22c24c64dd32e0d52fffe5d5a313e3dce1` |
| mutant specs | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc003.json` | `a7e0f25c923abea6752cd61f69568708efe5482496572687c230a83e45f6e9e4` |
| mutant specs, review round | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc003_r1.json` | `d7e981a75b8aa99a0bfa26a3364a21f2d50ac5db3d7ff8d6e48f8789f38e85bd` |
| byte-exact harness | `.dev-flow/2026-10-02-batch-02/evidence/mutate_bytes.py` | `76c8f629ae99ede850420f893365a65fc5ba0d24204a5d9f3004cb1b9afb331e` |
| vocabulary derivation | `.dev-flow/2026-10-02-batch-02/evidence/spanish_vocab.py` | `c7bf6df83b3679d26d39c66bf0d61ae666c3607f85b5d880cc6716a4e77426c2` |
| vocabulary transcript | `.dev-flow/2026-10-02-batch-02/evidence/inc003-vocab.txt` | `25c7e83b508554362e4b87cd2972007da9d071886ae396df3b183323bd55f506` |
| reverse census run | `.dev-flow/2026-10-02-batch-02/evidence/inc003-reverse-census.txt` | `3c875440d9676a01c273648fa93145587896b1b6b0ce94c8411fe2d09583ee66` |
| gate run | `.dev-flow/2026-10-02-batch-02/evidence/inc003-green.txt` | `187e1a6b7c76322cdeff663934b8bef03a33b0cb54abb1dc21f028d4a49a1fa0` |
| Setup, 118×30 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc003-setup-118x30.txt` | `9bed8add3074e20a1b5e919037b6f20f8c645d645260f69657691a1f01815046` |
| flow, 80×24 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc003-flow-80x24.txt` | `a9f4cf7bc7f574f9c0f92e5c43e07e37caba62b23bdcd7c25a54468d42a82b68` |
| help modal, 118×30 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc003-app-help-118x30.svg` | `736d6d1fbb38177200e61cf48a973c99f32f34dcdc181e76af956ab9dfa0cd62` |

| Field | Value |
|---|---|
| **Evidence files** | 12 artifacts, each cited with its digest (`captures/inc003-*`: flow, standup, people, Setup at both sizes, the app and help at both terminal sizes — taken before the review-round copy fixes F2/F3; the close captures carry the final copy) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no Spanish painted" |
| If the result is an ABSENCE, what made the search wide enough | the base copy's whole removed vocabulary (derived, 218 words) + stored values + frequent words + accents, over every view's panel and help modal and every package literal |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_TC_206_the_lexicon_sees_every_base_surface` |
| Conjunctive criteria: one mutation per conjunct | E1–E7, X1–X4 one per surface |
| Synthetic instance of the absent case | each mutant |
| **Positive control for every probe that returned an ABSENCE** | `BASE_SPANISH`, every word flagged; E8 (the set mutated → the guard RED) |

**Declared limit:** Spanish built only of words in neither the derived vocabulary nor the frequent
list would pass (stated in the test, as the privacy sweep states its floor).

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | full suite after the edit (`evidence/inc003-reverse-census.txt`: 8 failed / 1634 passed) | 7 superseded Spanish pins rewritten in place (`test_flow_view.py` ×2, `test_setup_help.py` ×2, `test_team_views.py` ×1, `test_colour_budget_app.py` TC-213 ×2); 1 REAL law broken by the draft — `test_prism_laws.py::test_no_literal_in_the_source_can_emit_the_second_person` — fixed in the copy, the test untouched |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | none | did not fire |
| B4 artifact produced here is consumed elsewhere | `help_usage` → `HelpModal`; `probe_setup_health` → `render_setup` | AT-204 reads the painted modal and panel |
| A3 | interface consumed by another module changed | `TEAM_FILTER_MODES` and the check keys | unchanged (D-212) |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (7 rewritten, 1 law kept), B4 fired, B2/B3/A3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| Spanish painted | non-docstring string literals of the package carrying Spanish | `evidence/p0-probes.txt` §P-3 (AST census, 176 literals) + `spanish_vocab.py` | 176 | the painted ones in `views.py`, `team_sync.py`, `modals.py` | stored values and keys (`app.py`, `TEAM_FILTER_MODES`, the check keys) and city names (`models.py`) — data, D-212 |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1643 = 1634 − 0 + 9` ✓ (the rewrites are in place, net 0).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` (rev98 snapshot) · round 1: `BLOCK-UNTIL: F1` — F1 HIGH (the 55-word hand-picked lexicon missed ~190 base words; its mutants X1–X3 put three Spanish strings on painted surfaces and all 8 nodes stayed green), F2–F5 LOW (Setup bullet dropped `esc cancel`, flow help no longer quoted the message, `todo`/place names flagged, two weak asserts); independent scan: no Spanish left painted, every stored key intact · all folded (derived vocabulary, every-word guard, source scan, a declared frequent layer) · round 2: OK to advance — F1 closed by re-reading and re-running X1–X3 (each RED), F2–F5 verified; two LOW notes (the source scan misses the frequent/accent layers — stated; the lattice bullet drops "not data") |

## 5 · Risks

- The lexicon is wide but not exhaustive (declared limit above).
- Internal keys stay Spanish in the code; a future screen that paints a key raw would show Spanish — PAINT_TOO catches the five known ones.

## 6 · Pending items / spec deviations

- `team_filter_cycle` still has no key (BACKLOG, README audit #10) — the help now names none.

## 7 · Suggested next task

Increment 004 — the gantt field: paged hint, urgency order, weekends, clip arrows.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 3 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 9 new nodes |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | n/a — no 2+-path unit added |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b (round 2) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | stored values unchanged |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | ids in docstrings |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
