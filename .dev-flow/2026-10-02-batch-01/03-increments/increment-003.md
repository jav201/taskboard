# Increment 003 — HLR-109 · README.md and RUN.md describe the shipped app

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-109; LLR-104.1, LLR-104.2 |
| Acceptance | AT-107 · white-box TC-120, TC-121 · unit: none (documents, no unit) |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**The README and RUN.md now describe the app as it ships and carry no personal path** — the
operator's standing request ("está muy desactualizado y tiene errores y problemas estéticos"),
done from `README-AUDIT.md`'s 33 findings and its outline, every fact re-read from the code at
writing time and fact-checked by qa-reviewer (two rounds). The README now installs from a
`git clone` of the public repository, names the nine views and their keys in one table,
documents `?` as the per-view help (`m` there for the full map), has one key table that every
bound key appears in and in which every key is bound, and adds Team mode, Dependencies, the
new gantt, Data files and a CLI table; the 100-line key list and the colour essays are gone.
RUN.md, which documented a retired prototype worktree flow under a personal path, now gives
the run / test / privacy-hook commands relative to a clone. `docs/taskboard-gantt.svg` is a
new render of the gantt on the seeded demo board (the old PNG showed the retired gantt).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `README.md` | doc | | rewritten (audit outline) |
| `RUN.md` | doc | | rewritten |
| `docs/taskboard-gantt.svg` | generated | HLR-109 | the README's gantt image, from `evidence/make_readme_gantt.py` (seeded demo board) |
| `tests/test_readme.py` | test | HLR-109, LLR-104.1, LLR-104.2 | AT-107, TC-120, TC-121 (9 nodes) |

| Count | Value |
|---|---|
| **SOURCE files** | **0 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 2 (outside the count) + 1 generated image |

## 3 · How to test

```bash
python -m pytest -q tests/test_readme.py tests/test_keymap.py
python .dev-flow/2026-10-02-batch-01/evidence/make_readme_gantt.py   # regenerates the image
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | n/a — no code unit; the one instrument (HOME_PATH) has its own RED-proof node | — |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-120 ×6, TC-121, the HOME_PATH RED-proof node | 8 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-107 (the file a reader opens) | 1 passed |

Plus the three README laws already in `tests/test_keymap.py` (images exist, every bound key
documented, the retired view explained and every view named) — green on the new README.
Full suite: in the increment-002 run, `evidence/inc002-green.txt` (1606 passed), which already
held these docs and tests; the batch's close run is `evidence/full-suite-close.txt`.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the base README.md / RUN.md / docs (HEAD) |
| Where it ran | a scratch `git archive HEAD` copy |
| Transcript | `evidence/inc003-red-on-base.txt` (7 failed / 5 passed) |
| Restore proven by | n/a — the base copy was never mutated |
| Bytecode cache | fresh copy, `-p no:cacheprovider` |
| Arms resolved at baseline | 12 |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | the HOME_PATH RED-proof (a self-test), the views-table preservation pin (the base table already had the nine rows), and the three `test_keymap.py` README laws (pre-existing, still satisfied) |

| Field | Value |
|---|---|
| **RED counterfactual** | the base README / RUN.md (scratch `git archive HEAD` copy): 7 of 12 nodes RED — AT-107 (6 home paths), TC-121 (2 paths, the retired flow), `?` documented as the palette, install not from a clone / a test count, "Four switchable views", no `## Keys` section, the derived facts · `evidence/inc003-red-on-base.txt` · the copy was not mutated, so no restore digest applies |

| Field | Value |
|---|---|
| **Mutation verdicts** | none — no mutation battery on documents; qa-reviewer mutated the README in memory four times (a phantom key row, 340 → 341 cities, a renamed CLI flag, a swapped colour) and each turned its node RED (round-2 report) |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `HOME_PATH` (the privacy pattern) | nine leak forms (drive, forward slash, doubled backslashes, Git-Bash, WSL, `/home`, `/Users`, drive-less, UNC) | each matched; the placeholders `<you>`, `%USERPROFILE%`, `~` did not (`test_the_home_path_pattern_sees_every_form_and_spares_placeholders`); first version missed UNC — the node went RED, the pattern was fixed |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 1 instrument, shown failing on its own fixture before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| `README.md`, `RUN.md` | the laws read the files as committed (UTF-8 text) | 10 + 3 passed |
| `docs/taskboard-gantt.svg` | `test_every_image_the_readme_shows_exists` (on disk); the security pass decoded its entities and swept it against the live board (0 hits) | passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts (the documents and the image), each asserted in its emitted form |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on base | `.dev-flow/2026-10-02-batch-01/evidence/inc003-red-on-base.txt` | `0157d57006362f02e4b8188a4292c377c931617934b82f1e69b5e6add81e2ffb` |
| image generator | `.dev-flow/2026-10-02-batch-01/evidence/make_readme_gantt.py` | `38070760f09f358bf27e1d0a6906bfacb590317a1e0163b2c29144c1c938478f` |
| suite run holding these docs and tests | `.dev-flow/2026-10-02-batch-01/evidence/inc002-green.txt` | `cd93df9841952c81cc143f980ae4e6e6f7751367427610ef8795af5b69bada62` |
| P4 gate run | `.dev-flow/2026-10-02-batch-01/evidence/full-suite-close.txt` | `719e918d5a3474e00637052fc192e7f0d60df7249d41985d23787874ed949a64` |

| Field | Value |
|---|---|
| **Evidence files** | 4 artifacts under the declared home, each cited with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "the docs carry no personal path" |
| If the result is an ABSENCE, what made the search wide enough | HOME_PATH's nine forms plus the security-reviewer's runtime-username grep over the docs, the SVG, the tests and the whole batch folder |
| Guard labelled as protecting a CONCLUSION, not a behaviour | the HOME_PATH comment and its RED-proof node |
| Conjunctive criteria: one mutation per conjunct | AT-107 (README) and TC-121 (RUN.md) are separate nodes |
| Synthetic instance of the absent case | the nine synthetic `someone` paths in the RED-proof node |
| **Positive control for every probe that returned an ABSENCE** | the same pattern finds 6 paths in the base README and 2 in the base RUN.md (`evidence/inc003-red-on-base.txt`) |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -l "README\|_readme" tests/*.py` | `tests/test_keymap.py` (3 README laws) — kept and satisfied: bold view names, the Columns sentence (now under History), Setup's `space`/`ctrl+s` in the key table, the image exists |
| B2 file moved on disk | none moved | did not fire |
| B3 byte-identical golden captures this source | none in the repo | did not fire |
| B4 artifact produced here is consumed elsewhere | the README is read by GitHub's renderer | the SVG must be in the commit (D-3, coordinator list) |
| A3 | interface consumed by another module changed | no code | did not fire |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (3 laws kept green), B4 fired (the untracked SVG goes in the commit), B2/B3/A3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the audit's punch list | README / RUN.md claims | `README-AUDIT.md` (33 findings, each with code evidence) | 33 | all but the code-side ones | #4 (the in-app renumber notice text) and #10 (the unbound team filter) are code / owner items → BACKLOG; #24 rewritten (the PATH snippet the audit could not test was wrong, qa D-2) |
| personal paths | home-path forms in tracked docs | `grep -n OneDrive README.md RUN.md` (P-5) | 4 sites | 4 | none |

| Field | Value |
|---|---|
| **Correction population** | 2 corrections, each enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → counted in increment 002's ledger (the 6 first nodes of
`tests/test_readme.py` entered with increment 001's run, the other 3 with increment 002's;
the RED-proof and the 2 later folds are among them). File total: 9 nodes (corrected at P4, qa G-004).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `qa-reviewer` — spawned as a named sub-agent with `agents/qa-reviewer.md` · fact-check round 1 FAIL (D-1 the `6` key's history, D-2 a wrong PATH snippet, D-3 the untracked SVG, D-4 the Setup interval does not drive sync; D-5..D-7 test gaps) · all folded; round 2 PASS-WITH-NOTES (16 of 17; D-3 is the coordinator's commit-list item; N-1, N-3 folded) · `security-reviewer` — spawned as a named sub-agent with `agents/security-reviewer.md` · privacy pass PASS-WITH-NOTES, 0 HIGH: S-7 (the username in pytest temp paths inside three evidence transcripts) fixed and verified; S-8 (the privacy tools do not decode SVG entities) routed to BACKLOG with a close-gate manual sweep; S-9 accepted |

## 5 · Risks

- The kanban, lanes and agenda PNGs and the ambient GIF predate this release's colour changes
  (the caption says so); regenerating them needs a real terminal capture.
- `docs/taskboard-gantt.png` is no longer referenced (left in place for the operator).

## 6 · Pending items / spec deviations

- D-3: `docs/taskboard-gantt.svg` must be in the coordinator's commit.
- D-4 code bug: Setup's sync interval sets only the staleness tolerance; the timer is fixed at 30 minutes — BACKLOG.
- Audit #4 (the in-app renumber notice text), #10 (team filter bound to no key) — BACKLOG.
- S-8 privacy-tool entity decoding — BACKLOG.

## 7 · Suggested next task

P4 validation.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 0 / 4 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_readme.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | n/a — no code unit |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | no source changed; the documents' reviewers are qa-reviewer and security-reviewer (§4b) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | no code |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | AT/TC ids in `tests/test_readme.py` docstrings |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |
