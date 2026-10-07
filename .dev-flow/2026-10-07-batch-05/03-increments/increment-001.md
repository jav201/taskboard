# Increment 001 — HLR-1101 · HLR-1102 · the failed-backup partial file · one `Mon D` formatter

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`. The normative RULES below are
> language-independent.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/increment-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-07-batch-05/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-05` |
| Increment | `001` |
| Lane (if the batch forked) | `none — one lane per increment (§2.8 of the contract; the parallel briefs took disjoint file sets, this one owning models.py + the two `_md` import rows)` |
| Requirement(s) | `HLR-1101` · `HLR-1102` (+ `LLR-1101.1` · `LLR-1102.1`) |
| Acceptance | `AT-1101` (arm 1: ENOSPC write + working removal · arm 2: ENOSPC write + refusing removal) · `AT-1102` (the identity pin + the 14-date sweep) — 4 nodes, all green |
| Agent | `software-dev` — DeepSeek V4 Pro |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

A failed backup or log write beside the board no longer leaves a partial file pretending to be a
backup: `models._create_beside` (`taskboard/models.py:1562-1583`) now wraps the exclusive-create
write so that ANY exception from `fh.write` (a full disk) closes the handle best-effort (nested
guard — Windows needs the handle released before the unlink), removes the just-created path
best-effort (a second nested guard that swallows its own errors), and re-raises the ORIGINAL
exception unchanged. BOTH writers — the link migration (`models.py:1620,1626`) and the milestone
offer (`models.py:1734,1743`) — inherit the law through the shared helper, untouched themselves.
The `Mon D` date formatter now exists exactly once: `def _md` stays at `taskboard/models.py:2147`
(body unchanged, `f"{d:%b} {d.day}"`); the `views.py` and `app.py` copies were deleted in favor of
the shared import (`taskboard/views.py:38`, `taskboard/app.py:38` — each joins the existing
`from .models import (...)` list). Dates render byte-identically in every view; a format change
now has one seat.

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | HLR-1101 · LLR-1101.1 · HLR-1102 · LLR-1102.1 | `_create_beside`'s failed-write guard (:1562-1583 — close-then-unlink nested guards, original re-raised); the kept single `def _md` (:2147) |
| `taskboard/views.py` | source | LLR-1102.1 | the local `def _md` deleted; `_md` joins the models import list (:38) |
| `taskboard/app.py` | source | LLR-1102.1 | the local `def _md` deleted; `_md` joins the models import list (:38) |
| `tests/test_backup_write.py` | test | LLR-1101.1 — pinned by AT-1101 | new — 2 arms (ENOSPC write + working removal → no partial file + the original error; ENOSPC write + refusing `Path.unlink` → the original error unmasked) |
| `tests/test_mon_d.py` | test | LLR-1102.1 — pinned by AT-1102 | new — the identity pin (`views._md is models._md`, `app._md is models._md`) + the 14-date sweep (12 month starts + Dec 31 + Feb 29 leap) through every access path |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 (outside the count) |

- The three source files are the minimal dedup set: the law's owner (models.py) plus the two
  one-line import rows that retire the duplicate definitions. The undo-toast seat in app.py is
  increment 002's.

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_backup_write.py tests/test_mon_d.py -q    # 4 passed
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_backup_write.py --collect-only -q         # 2 node ids resolved
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (`_create_beside`'s failure path — nested guards, cyclomatic ≥3; `_md` — the one-definition census) | `core` · `full` | the 2 backup arms + the identity pin + the sweep | 4 nodes passed |
| **A · white-box** `AT-1101` ↔ LLR-1101.1 | `core` · `full` | `test_failed_write_leaves_no_partial_file` · `test_refusing_unlink_never_masks_the_write_error` | 2 nodes passed |
| **B · black-box** `AT-1102` ↔ story, through the shipped surface | `core` · `full` | `test_one_md_definition_shared_by_all` · `test_md_renders_identically_through_every_access_path` | 2 nodes passed |

The agent's targeted run held `tests/test_backup_write.py tests/test_mon_d.py
tests/test_team_sync.py tests/test_cleanup.py` at **32 passed, 0 failed** (the 4 new nodes + 16
team_sync + 12 cleanup; `evidence/inc001-run.log`). Its one full-suite pass at that checkpoint
reported **2530 passed, 20 failed — 2550 collected**: every failure OUTSIDE its files
(`test_no_live_board` 1 · `test_precommit_gate` 7 · `test_report` 2 ·
`test_scratch_cannot_be_committed` 10 — the git-subprocess-under-load flake family reacting to
the uncommitted batch state while the parallel increment 004 was editing test files). The
coordinator re-ran exactly those four files on the settled tree: **45 passed, 0 failed**
(`evidence/env-flake-note.md`) — recorded so the close does not chase them. The ONE complete
clean-tree run at close is the orchestrator's (C-25), recorded in `04-validation.md` /
`05-close.md` — "see 04-validation" for the final number.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M1 (the unlink removed):** the guarded `p.unlink(missing_ok=True)` block inside the failure handler replaced by a comment — the pre-law behavior, the partial file stays. **M2 (the masking guard removed):** the same block collapsed to an UNGUARDED `p.unlink(missing_ok=True)` — a refusing removal now escapes and masks the original ENOSPC |
| Instrument | project code: the coordinator's scripted exact-string replacement (`evidence/run-mutations-abc.py` — byte-anchor, sha256-checked restore) |
| Where it ran | **my own tree** — the MAIN checkout (the batch's single lane; the parallel briefs owned disjoint file sets) |
| Transcript | `evidence/mutations-abc.log` — M1: `1 failed in 0.31s` on `test_failed_write_leaves_no_partial_file` (the partial file survived); M2: `1 failed in 0.28s` on `test_refusing_unlink_never_masks_the_write_error` (the refusing unlink escaped) |
| Restore proven by | **file hash returned to its pre-mutation value**: M2's restore hashed `OK` at `96574d9f36204836baaf6d540f861eb57ad3ce349f0fb9cb2b600879cbbdc10c`. M1's restore line reported `MISMATCH` — the runner restores through a text-mode write that normalized line endings in the touched region (content exact, cosmetic; git normalizes on commit); the normalized hash `96574d9f…` IS models.py's hash at this close-out, verified again by the green suite |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **2** — `pytest tests/test_backup_write.py --collect-only -q` resolves exactly `test_failed_write_leaves_no_partial_file` and `test_refusing_unlink_never_masks_the_write_error` |
| Verdict granularity | **per resolved node id** — M1 reddened exactly arm 1; M2 reddened exactly arm 2 |
| Arms that stayed GREEN | M1: arm 2 stayed GREEN — with the unlink removed entirely the refusal is never attempted, so the original ENOSPC still propagates (that arm's load-bearing case is the guard, not the unlink). M2: arm 1 stayed GREEN — the unguarded unlink SUCCEEDS against a willing disk, so the file is still removed |

| Field | Value |
|---|---|
| **RED counterfactual** | M1 — `_create_beside`'s failure handler, the guarded unlink block removed (no unlink) · M2 — the same block unguarded (the masking guard removed) · transcripts at `evidence/mutations-abc.log` · restore digest `96574d9f…c10c` (M2 `OK`; M1's restore line-ending note above) |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node: M1 · arm 1 KILLED (the partial file survives the failed write), arm 2 GREEN (the removal is never attempted — named above) · M2 · arm 2 KILLED (the refusing unlink escapes — `EACCES` masks `ENOSPC`), arm 1 GREEN (the unguarded unlink succeeds — named above) · inert arms: none · registry: no `docs/tools/devflow-mutants.json` battery in this repo — the two named mutants are the increment's own counterfactuals · transcript `evidence/mutations-abc.log` · restore digest `96574d9f…c10c` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M1's mutant code | `1 failed` on arm 1 — the partial file survived the failed write (`evidence/mutations-abc.log` M1) |
| `pytest` (the suite) | M2's mutant code | `1 failed` on arm 2 — `assert exc.value.errno == errno.ENOSPC` failed: the escaped refusal (`EACCES`) masked the original |
| the `_FlakyFile` monkeypatch (`tests/test_backup_write.py:25-56`) | an exclusive-created file whose `write` raises `ENOSPC` (a synthesized full disk — the mechanism-level fault, not a verdict tweak) | on the base tree: arm 1's RED — the partial file stayed on disk after the failed write (cited in the file docstring); at this increment's baseline: the file is gone and the original errno propagates |
| `grep` census probe | `grep -rn "def _md" taskboard/` over the whole package | pre-dedup **3** hits (models.py · views.py · app.py — P-1's evidence), post-dedup **1** (models.py:2147) — the probe distinguishes presence from absence |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown RED before its first PASS was believed (transcripts in `evidence/mutations-abc.log`; the census counts in `evidence/inc001-run.log`) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the backup file beside the board after a failed write | `{p.name for p in tmp_path.iterdir()} == {"board.json"}` and `not partial.exists()` (arm 1, `tests/test_backup_write.py:70-71`) | both hold — the EMITTED directory listing carries no partial file; the whole listing is enumerated, not a single-path guess |
| the error the caller receives | `exc.value.errno == errno.ENOSPC` in both arms | `ENOSPC` — the original failure's errno, never the guard's |
| the rendered `Mon D` strings | the sweep through all three access paths: `views._md is models._md` · `app._md is models._md`; the 14 emitted strings (anchors `Feb 29` · `Dec 31`) | identity holds; every rendered string byte-identical across the three access paths — the emitted text, not the function object alone |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted against the form its producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the increment brief (the coordinator's chunk brief) | `.dev-flow/2026-10-07-batch-05/evidence/inc001-brief.md` | `3797f21ada0714658da689f17e2ddd3397795d024dd63992aa18621f8513de22` |
| the agent's run + its report (targeted 32 passed; the full-suite count with the 20 out-of-scope failures NAMED, not chased) | `.dev-flow/2026-10-07-batch-05/evidence/inc001-run.log` | `bb21dcb15a1da1c7ddb35a943a221195edc9253b1f8b1476084573d4224b0f28` |
| the close-out mutations M1-M5 (M1/M2 this increment; M3/M4 increment 002; M5 increment 004) | `.dev-flow/2026-10-07-batch-05/evidence/mutations-abc.log` | `4273b8ae4f58805cc2f70413422b2cc2d8b2e1ca3e47429f3eeed5cda856e082` |
| the environmental flake note (the 20 failures triaged: the four files re-run clean, 45 passed) | `.dev-flow/2026-10-07-batch-05/evidence/env-flake-note.md` | `281bc0fca9715db674b59539c8be6a97c64aff23bebce798f57594e6bb616c76` |

| Field | Value |
|---|---|
| **Evidence files** | 4 artifacts, each at the declared home and cited with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — "the package holds exactly ONE `def _md`" and "a failed write leaves NO partial file" are both absence claims |
| If the result is an ABSENCE, what made the search wide enough | the census runs over the WHOLE package (`grep -rn "def _md" taskboard/`), not the three known sites — pre-dedup it found exactly the three P-1 sites, post-dedup exactly one; the partial-file absence is asserted on the full `tmp_path` directory listing (every entry enumerated), not a single-path check |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_one_md_definition_shared_by_all` — its docstring says the census is the one-definition conclusion's guard (the next reader "simplifies" an identity assert away without it) |
| Conjunctive criteria: one mutation per conjunct | LLR-1101.1 has two conjuncts — the unlink happens (M1 kills its removal) and the guard never masks (M2 kills its nesting); one mutation per conjunct, both KILLED |
| Synthetic instance of the absent case | the `_FlakyFile` full-disk fault (`tests/test_backup_write.py:25-44`) — the tree has no real full disk; the fake file synthesizes the ENOSPC fault at the mechanism level, and the refusal monkeypatch synthesizes the EACCES disk |
| **Positive control for every probe that returned an ABSENCE** | the census's known-present control: the same probe returned **3** on the pre-dedup tree (a non-absence on a known multiplicity); arm 1's listing returns `{"board.json"}` — the known-present board file enumerated by the same probe that establishes the partial's absence |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln "_create_beside" tests/` → `tests/test_backup_write.py`; `grep -rln "def _md\|_md(" tests/` → `tests/test_mon_d.py` | 1 file each — this batch's pins; both shipped callers exercise `_create_beside` through the migration/offer suites (`models.py:1620,1626,1734,1743`) and every `_md` render seat through the view suites — all re-validated by the green suite |
| B2 file moved on disk | `git status --porcelain -- taskboard/models.py taskboard/views.py taskboard/app.py` → ` M` all three | no rename, no delete — the old paths are the current paths; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → no such directory in this repo | the repo holds no golden-capture directory at all; did NOT fire |
| B4 artifact produced here is consumed elsewhere | `grep -rn "MIGRATION_BACKUP\|MILESTONE_BACKUP\|MIGRATION_LOG\|MILESTONE_LOG" taskboard/ tests/` | the constants and the backup/log naming contract are unchanged — models.py (producer), app.py's undo path, the test pins; every reader re-validated by the green suite |
| A3 interface consumed by another module changed | `grep -rn "_md" taskboard/views.py taskboard/app.py` → the import rows at `views.py:38` / `app.py:38` | two NEW consumers of `models._md` — the contract's P-1 verified the three bodies byte-identical BEFORE the dedup; the identity pin proves both files now share the one object; the function's signature and output contract unchanged |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1's hits are this batch's own pins (the transitive callers re-validated by the suite), A3 names two new import rows under a byte-identical-body premise, B2/B3 did NOT fire with their probes recorded · transcripts in `evidence/inc001-run.log` |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| S5-3 — a failed backup write leaves no partial file | every open carry in the canonical backlog | `.dev-flow/BACKLOG.md` "Open — after …" sections (the batch-03 note enumerates 3 from Batch C · 6 from the B2a residue · 1 present-a-project round) | 10 items | S5-3 + F-6 — this increment | UXV-3 + UXV-6 → increment 002; the 3 chain-map carries → increment 003; F-3..F-5 → increment 004; none left — all ten closed this batch (present-a-project by batch E's landing) |

| Field | Value |
|---|---|
| **Correction population** | 1 correction wave (the ten-item backlog tranche), enumerated from the canonical backlog before the first site was edited; every site accounted for across the four increments |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the second `def _md` (views.py) | 0 hits — `grep -c "def _md" taskboard/views.py` → 0; its only `_md` is the import | yes | `taskboard/views.py:38` |
| the third `def _md` (app.py) | 0 hits — `grep -c "def _md" taskboard/app.py` → 0; its only `_md` is the import | yes | `taskboard/app.py:38` |
| the unguarded write body (`with open(p, "xb") as fh: fh.write(data)`) | 0 hits — the write now sits inside the nested close-then-unlink guard | yes | `taskboard/models.py:1573-1586` |

### Signed-balance test ledger

`post = base − D + A` → `2550 = 2546 − 0 + 4` ✓ reconciles at this increment's checkpoint
(base = the trunk batch-03+batch-04 merge, 2546 collected; this increment added the 4 nodes of
`tests/test_backup_write.py` + `tests/test_mon_d.py`). The increment's own full-suite pass
collected exactly 2550 (2530 passed + 20 environmental failures OUTSIDE its files, triaged in
`evidence/env-flake-note.md` — counts reconcile; the pass/fail triage is the coordinator's). The
batch-level ledger is summed in `04-validation.md` — "see 04-validation" for the close number.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` — the close-out coordinator self-executed the P2 lens pool (qa ∥ ux ∥ architect ∥ security; the runtime spawned nobody, named in `02-review.md` per the runtime rule) over the four packets and the diffs · verdict PASS-WITH-NOTES, 0 HIGH — the notes: the M8 SURVIVED-with-cause declaration (increment 003 names its GREEN arm and why), the inc-002 example-line punt, the inc-004 team-folder limit — each carried in its packet §5/§6 · the P2 review verdict stands in `02-review.md` (0 blocker · 0 major · 0 minor) |

---

## 5 · Risks

- The `.1/.2/…` rotation still accumulates backup files when the WRITE SUCCEEDS but a later step
  of the migration/offer fails — S5-3 names the failed write only; a wider cleanup is a new item,
  not opened here (no occurrence observed this batch).
- The 14-date sweep characterizes `_md`'s output but cannot see a render seat that formats dates
  WITHOUT `_md` — the full suite's render arms (kanban/gantt/lanes/agenda pins) stand behind the
  census as the widened guard.

## 6 · Pending items / spec deviations

- None open here — the two arms of the contract are closed; the environmental 20 of the agent's
  own full-suite pass are triaged in `evidence/env-flake-note.md` (not this increment's files).

## 7 · Suggested next task

- Increment 002 — the UX carries (the `u` toast at `app.action_undo`; the `?` word-clip at
  `modals.py`), serialized after this increment's landing.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 3 source files (models.py · views.py import row · app.py import row) |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_backup_write.py` (2) + `tests/test_mon_d.py` (2) landed with the product in the same run |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `_create_beside`'s failure path — the two mechanism-level arms, mutation-proven (M1/M2); the `_md` census + sweep |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M1/M2 executed; transcript `evidence/mutations-abc.log`; restore digest `96574d9f…c10c` |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above); transcripts in `evidence/inc001-run.log` |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b — `human:coordinator` self-executed lenses · PASS-WITH-NOTES 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane; the file-set plan put the `_md` import rows here and the undo-toast seat in 002 — and 002's first attempt died with zero edits before this increment landed, so no two live briefs ever wrote the same file (`git diff --name-only HEAD` per increment) |
| 8 | Frozen interfaces untouched | all | ✓ | `_create_beside`'s signature/suffix-rotation contract unchanged; `_md`'s body byte-identical (P-1); both callers untouched |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | the one-`def _md` census + the full-disk `_FlakyFile` synthesis |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | per-node table above; inert arms: none |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) |
| 13 | **Correction population** declared | all | ✓ | the ten-item backlog tranche, enumerated before the first edit |
| 14 | **Emitted-form assertion** declared | all | ✓ | the directory listing + errno + the sweep's rendered strings |
| 15 | **Independent review** names somebody | all | ✓ | §4b — `human:coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 4 artifacts with stored-byte digests |
