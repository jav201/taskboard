# Increment 002 — HLR-1103 · HLR-1104 · the single-task undo toast · the `?` word-clip

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
> `.dev-flow/2026-10-07-batch-05/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-05` |
| Increment | `002` |
| Lane (if the batch forked) | `none — one lane per increment (§2.8 of the contract; landed AFTER increments 001/004 had settled, so no two live briefs shared a file)` |
| Requirement(s) | `HLR-1103` · `HLR-1104` (+ `LLR-1103.1` · `LLR-1104.1`) |
| Acceptance | `AT-1103` (the positive pin + the purged-skip silent arm) · `AT-1104` (the 80×24 integration arm) · `TC-1104` (the `_clip_words` boundary pins) — 4 nodes, all green |
| Agent | `software-dev` — DeepSeek V4 Pro (second attempt: `inc002-run.log` died on the /tmp sandbox rejection with ZERO edits; `inc002b-run.log` is the successful run) |
| Date | `2026-10-07` |

---

## 1 · What changed

*(BLUF: state the outcome first, then the mechanism. Name the shipped surface the user reaches.)*

Pressing `u` after a change that touched exactly one task now says what came back: the
single-task fall-through of `app.action_undo` (`taskboard/app.py:1468-1469`) toasts one line —
`Undone — {task.title} is back as it was.`, `title="Undo"`, `severity="information"`,
`markup=False` — placed BEFORE the save, covering both the field-restore and the re-insert
sub-paths. The cascade/milestones/migration branches and the stale-skip (a task purged since the
snapshot stays silent) are untouched. The `?` help at 80 cells no longer cuts a word in half: the
investigation found the true seat — Textual's COMPOSITOR wraps a height-1 `Label` inside the
narrow help column (22 cells) with `break_long_words=True`, so a word straddling the column edge
broke mid-glyph and the rest of the line was dropped (e.g. `the project under most pressure`
painted `the project under m`). The fix lives at composition: `_clip_words` (word-boundary clip +
`…`, unbreakable token clips at the edge) and `_HelpLine(Label)` in `taskboard/modals.py`
(`:1750-1794`), through which `HelpModal.compose` now renders every legend meaning and usage
bullet (`:1862-1867`). `_HelpLine` SUBCLASSES `Label` (not `Static`) so the suite's
`query("Label")` census still reads the lines, and takes the column width (`1fr`) so `render()`
sees the true cells.

## 2 · Files modified

**The budget counts SOURCE files only. Tests are not capped. Product docs and `.dev-flow/**` are outside the count.**

One row per file. `Kind` is one of `source` · `test` · `doc` · `config` · `generated` · `fixture`; `Traces to` names the US/HLR/LLR (or `R-<AREA>-<NNN>`) ids the file serves, and `doc` rows leave it empty.

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | HLR-1103 · LLR-1103.1 | the one-line undo toast at the single-task fall-through (:1468-1469), before the save; the `_md` import row at :38 is increment 001's |
| `taskboard/modals.py` | source | HLR-1104 · LLR-1104.1 | `_clip_words` (:1750-1767) + `_HelpLine(Label)` (:1772-1794); `HelpModal.compose` renders legend meanings + usage bullets through `_HelpLine` (:1862-1867) |
| `tests/test_undo_toast.py` | test | LLR-1103.1 — pinned by AT-1103 | new — the positive pin (a real single-task mutation, `u`, the toast read off the painted `Toast` equals the pinned literal) + the purged-skip silent arm (0 toasts) |
| `tests/test_help_clip.py` | test | LLR-1104.1 — pinned by AT-1104 + TC-1104 | new — the 80×24 integration arm (every visible help line of both columns ends at a word boundary or with `…`) + the `_clip_words` unit pins (exact-edge · overlong-token · word-boundary · degenerate widths) |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 (outside the count) |

---

## 3 · How to test

```bash
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_undo_toast.py tests/test_help_clip.py -q    # 4 passed
env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_undo_toast.py --collect-only -q             # 2 node ids resolved
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (`_clip_words` — cyclomatic ≥3: degenerate width / fits / word-loop / unbreakable token) | `core` · `full` | `test_TC_1104_clip_words_exact_edge_and_overlong_token` | 1 node passed (mutation M4-proven below) |
| **A · white-box** `AT-1104` ↔ LLR-1104.1 | `core` · `full` | `test_AT_1104_help_lines_end_at_word_boundary` (the `#help-left`/`#help-right` lines read off the composed modal) | 1 node passed |
| **B · black-box** `AT-1103` ↔ story, through the shipped surface | `core` · `full` | `test_AT_1103_undo_names_the_single_task` · `test_AT_1103_purged_entry_stays_silent` (the house pilot drives keys, reads the painted `Toast`) | 2 nodes passed |

Suite at the increment's close: **2555 passed, 0 failed** (`evidence/inc002b-run.log`, ~7:08).
The agent's first DRAFT of the help fix reddened 5 regression classes (the gantt help fit, the
gantt legend frame, the kanban help copy, the markup-census exemption) — the transcript's
intermediate failures — settled by making `_HelpLine` a `Label` SUBCLASS and leaving the example
`Label` untouched; every failure line in the cited bytes is either that settled draft or the
dead first attempt's /tmp sandbox rejection, and each is named in this paragraph. The dead first
attempt (`evidence/inc002-run.log`) produced ZERO edits — the close-out lesson: scratch lives
inside the project (`evidence/`), never `/tmp`. The ONE complete clean-tree run at close is the
orchestrator's (C-25) — "see 04-validation" for the final number.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | **M3 (no undo toast):** the two-line `self.notify(...)` at the single-task fall-through replaced by a comment — the pre-law silence. **M4 (never clip):** `_clip_words`'s fit-check replaced by `if True: return s` — the pre-law mid-word cut |
| Instrument | project code: the coordinator's scripted exact-string replacement (`evidence/run-mutations-abc.py` for the stored battery; the close-out's binary-mode re-runs `evidence/m3_anchor_fix.py` / `evidence/m4_arms.py` — byte-exact restores) |
| Where it ran | **my own tree** — the MAIN checkout (the batch's single lane) |
| Transcript | M3: stored battery logged `BAD: anchor not unique/found (0)` — the script's ONE-LINE anchor never matched because the shipped notify is a TWO-LINE call (`mutations-abc.log` §M3); the clean re-run with the true two-line anchor: `evidence/m3-anchor-fix.log` — `test_AT_1103_undo_names_the_single_task` reddens (`toasts []`), `1 failed, 1 passed`, exit 1 → KILLED. M4: `mutations-abc.log` §M4 `1 failed, 1 passed`; the per-node re-run `evidence/m4-arms.log` — exactly `test_TC_1104_clip_words_exact_edge_and_overlong_token` reddens (`assert 'the project ...most pressure' == 'the project under…'`), exit 1 → KILLED |
| Restore proven by | **file hash returned to its pre-mutation value**: M3's re-run restored app.py byte-exact to `9d9ac6e0c33fb46176bb50f2193df1b2a23528da258cda77d30a8a7991239921` (`OK`); M4's re-run restored modals.py byte-exact to `88d45a33b7b495da87f75d4d393beb464cb38531f5fa132421a79d4d3c11b85b` (`OK` — the stored battery's M4 restore had reported `MISMATCH` on the same text-mode line-ending note as increment 001's M1; the normalized hash IS modals.py's hash at this close-out, verified again by the green suite) |
| Bytecode cache | run with `PYTHONDONTWRITEBYTECODE=1` (C-46) |
| Arms resolved at baseline | **2 + 2** — `pytest tests/test_undo_toast.py --collect-only -q` resolves exactly the 2 toast nodes; `pytest tests/test_help_clip.py --collect-only -q` resolves exactly the 2 help-clip nodes |
| Verdict granularity | **per resolved node id** — M3 reddened exactly the positive pin; M4 reddened exactly the unit pin |
| Arms that stayed GREEN | M3: `test_AT_1103_purged_entry_stays_silent` stayed GREEN — a removed toast cannot fire on the skip branch (the skip stays silent either way; its load-bearing case is the notify NOT moving above the skip, which the shipped placement holds). M4: `test_AT_1104_help_lines_end_at_word_boundary` stayed GREEN **vacuously and honestly named**: the arm reads each line's `render()` output and accepts "ends with `…` OR equals a full source line" — an unclipped line IS its full source, so the integration arm alone cannot see M4; the load-bearing RED arm is the unit pin, which is why TC-1104 exists |

| Field | Value |
|---|---|
| **RED counterfactual** | M3 — the two-line undo toast removed · M4 — `_clip_words`'s clip neutered (`if True: return s`) · stored transcripts at `evidence/mutations-abc.log`; the clean per-node transcripts at `evidence/m3-anchor-fix.log` (digest `9d9ac6e0…9921`) and `evidence/m4-arms.log` (digest `88d45a33…b85b`) |

| Field | Value |
|---|---|
| **Mutation verdicts** | per resolved node: M3 · `test_AT_1103_undo_names_the_single_task` KILLED (`toasts []` — no toast at all), the purged-skip arm GREEN (named above) · M4 · `test_TC_1104_clip_words_exact_edge_and_overlong_token` KILLED (the exact-edge assert), the integration arm GREEN vacuously (named above — its assertion accepts a full source line, so the unit pin carries the RED) · inert arms: none (both "green" arms are named with their mechanism) · registry: no `docs/tools/devflow-mutants.json` battery in this repo — the named mutants are the increment's own counterfactuals · transcripts `evidence/mutations-abc.log` · `evidence/m3-anchor-fix.log` · `evidence/m4-arms.log` · restore digests `9d9ac6e0…9921` · `88d45a33…b85b` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `pytest` (the suite) | M3's mutant code | `1 failed` — the positive pin: `"no 'Undo' toast equal to 'Undone — Write the migration guide is back as it was.'; toasts []"` (`evidence/m3-anchor-fix.log`) |
| `pytest` (the suite) | M4's mutant code | `1 failed` — the unit pin: `assert 'the project ...most pressure' == 'the project under…'` (`evidence/m4-arms.log`) |
| the toast-reading harness (`_toast_check`, the house pattern off `tests/test_markup_sites.py`, read at `tests/test_undo_toast.py:72`) | a real single-task mutation + `u` on the BASE tree (no toast shipped) | the instrument's RED on base: "no 'Undo' toast … toasts []" — the same harness reads the painted `Toast` at the green baseline and sees the pinned literal |
| the `query("Label")` census (the markup suites across `tests/`) | the first draft's `Static`-based help line | 5 regression classes reddened (gantt help fit · gantt legend frame · kanban help copy · markup-census exemption — `evidence/inc002b-run.log`); the shipped `Label` subclass returned them green — the census distinguishes a Label from a look-alike |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown RED before its first PASS was believed (transcripts cited per row) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the painted `Toast` | `_toast_check(app, "Undo", UNDONE) is None` where `UNDONE = "Undone — Write the migration guide is back as it was."` — read off the painted `Toast` widget, not a mock | the literal matched exactly (the emitted notification text, `markup=False`) |
| the painted help lines at 80×24 | every line of `#help-left`/`#help-right`, trimmed, `endswith("…") or line in sources` (the full source set rebuilt from `help_usage`/`legend_entries`/`help_example`/`bar_keys`) | every visible line holds — the emitted render() text, per line, not the fixture's intent |
| the `_clip_words` outputs | the unit pins: `"the project under most pressure" @20 → "the project under…"`, `"supercalifragilistic" @10 → "supercali…"`, exact-edge + degenerate widths | exact strings — the emitted clipped text |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted against the form its producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the increment brief | `.dev-flow/2026-10-07-batch-05/evidence/inc002-brief.md` | `43d5bc95ceb3e600c3e4028f269e261541ed5a7208b505c4d11dc21ffa3ded93` |
| the dead first attempt's log (the /tmp sandbox rejection — ZERO edits; the close-out lesson) | `.dev-flow/2026-10-07-batch-05/evidence/inc002-run.log` | `42ad5ecd8c660303bb1417c26886692f5fe92bf04dbb0e9cb18ecbcb5bef7c0c` |
| the successful run + report (2555 passed; the 5 settled draft regressions named) | `.dev-flow/2026-10-07-batch-05/evidence/inc002b-run.log` | `ce0e3bedddbe76b5a3c954e6b380290ac4d309d338ead95ed6281f317aae7cdd` |
| the stored mutation battery M1-M5 (M3/M4 this increment) | `.dev-flow/2026-10-07-batch-05/evidence/mutations-abc.log` | `4273b8ae4f58805cc2f70413422b2cc2d8b2e1ca3e47429f3eeed5cda856e082` |
| M3's clean re-run (two-line anchor; per-node; byte-exact restore) | `.dev-flow/2026-10-07-batch-05/evidence/m3-anchor-fix.log` | `1dcd32a4520b54984e099ab92a18170c53bb5506745cc9429f9caf12009275c8` |
| M4's per-node re-run (both arms resolved; byte-exact restore) | `.dev-flow/2026-10-07-batch-05/evidence/m4-arms.log` | `bdd71bd6fd22211b450b5632f5cc05a232a3b6570178c96e5da39fa68c7149b8` |

| Field | Value |
|---|---|
| **Evidence files** | 6 artifacts, each at the declared home and cited with the digest of its stored bytes |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | **yes** — "no painted help line ends mid-word" and "the skip branch emits no toast" are absence claims over the composed modal |
| If the result is an ABSENCE, what made the search wide enough | the integration arm walks EVERY child line of BOTH help columns (`#help-left` + `#help-right`), skipping only empty chrome — not a sampled subset; the toast arm enumerates the painted toasts (`toasts []` on the skip) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_AT_1104_help_lines_end_at_word_boundary` — its docstring states the law (no mid-word tail) so the vacuous-pass shape (§4, M4 row) is never "improved" into a weaker assertion |
| Conjunctive criteria: one mutation per conjunct | M3 kills the toast's presence; the purged-skip arm is the second conjunct (the toast must not move above the skip) — its GREEN under M3 is named, and its load-bearing case is the shipped placement, probed by the contract's negative control |
| Synthetic instance of the absent case | the fixture board's long legend meaning + long usage bullet (`tests/test_help_clip.py:30-38`) synthesize the mid-word cut the shipped help copy doesn't guarantee on its own; the purged entry synthesizes the stale-skip silence |
| **Positive control for every probe that returned an ABSENCE** | the toast probe's known-present control: the positive arm's same `_toast_check` returns the pinned literal on the same painted surface (a non-absence); the line probe's control: lines that FIT whole are accepted only by matching the rebuilt source set — a known-present full source |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln "_HelpLine\|_clip_words" tests/` → `tests/test_help_clip.py`; `grep -rln "Undone — " tests/` → `tests/test_undo_toast.py` | 1 file each — this increment's pins; the `query("Label")`-style censuses of `tests/test_app.py` · `test_details_links.py` · `test_english.py` · `test_gantt_board.py` (and siblings) read the help family through the Label contract — all re-validated green by the 2555 close |
| B2 file moved on disk | `git status --porcelain -- taskboard/app.py taskboard/modals.py` → ` M` both | no rename, no delete; probe executed, did NOT fire |
| B3 byte-identical golden captures this source | `ls tests/goldens` → no such directory in this repo | did NOT fire |
| B4 artifact produced here is consumed elsewhere | the help copy readers: `HelpModal` through `help_usage`/`legend_entries`/`help_example`/`bar_keys`; the gantt/kanban help copies and the markup censuses re-validated (the 5 settled draft regressions in `inc002b-run.log`) | consumers green at the increment's 2555 close |
| A3 interface consumed by another module changed | `grep -c "self.notify(" taskboard/app.py` → 44 notify sites, one added at the single-task fall-through; `_HelpLine(Label)` is a NEW Label subclass under the existing `query("Label")` census | the notify's `title`/`severity`/`markup=False` contract matches the house discipline; the census contract is preserved BY the subclass (that was the draft's 5-regression lesson) |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 — B1's hits are this increment's own pins (the transitive census readers re-validated), A3 names one new notify site + one new Label subclass under a preserved contract, B2/B3 did NOT fire with their probes recorded |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| UXV-3 + UXV-6 (this increment) | the BACKLOG's standing carries | `.dev-flow/BACKLOG.md` "Open — after …" sections (the ten-item tranche) | 10 items | UXV-3 (app.py) + UXV-6 (modals.py) — this increment | S5-3 + F-6 → increment 001; the 3 chain-map carries → increment 003; F-3..F-5 → increment 004; none left |

| Field | Value |
|---|---|
| **Correction population** | 1 correction wave (the ten-item backlog tranche), enumerated before the first site was edited; every site accounted for across the four increments |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the pre-law silent fall-through (no notify between the field restore and the save) | 0 hits for any notify between the restore and `self.board.save()` in the single-task branch | yes — exactly one notify at :1468-1469, before the save | `taskboard/app.py:1460-1473` |
| the first draft's `Static`-based help line | 0 hits — shipped is `class _HelpLine(Label)` | yes | `taskboard/modals.py:1772` |

### Signed-balance test ledger

`post = base − D + A` → `2554 = 2550 − 0 + 4` ✓ at this increment's own checkpoint (base =
increment 001's 2550 collected). The observed close run reported **2555** passed
(`evidence/inc002b-run.log`) — the +1 is the parallel increment 004's team-folder arm, whose two
test files are disjoint from this increment's; the count reconciles at the batch level in
`04-validation.md` — "see 04-validation".

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `human:coordinator` — the close-out coordinator self-executed the P2 lens pool over the four packets and the diffs · verdict PASS-WITH-NOTES, 0 HIGH — the notes: the M4 integration arm's vacuous GREEN under the mutation (named in §4 — the unit pin carries the RED, and the arm's docstring says why it must not be "strengthened" into a paint-level read), the example-line punt (§6), the dead attempt's sandbox lesson (§4 narrative) · the P2 review verdict stands in `02-review.md` |

---

## 5 · Risks

- The example line (a markup DIAGRAM, not prose — `HelpModal`'s `Example` block) stays unclipped:
  out of LLR-1104.1's stated legend+usage scope, and in the chainmap help it can still cut the
  `━━▸┃Add` token mid-glyph. A diagram-aware clip is a new item if the operator wants it — no
  occurrence was promoted this batch.
- The 80×24 integration arm reads `render()` output (the emitted per-line text), not the
  compositor's wrapped grid — that is the level the law is written at (the compositor can no
  longer cut a word because the line it receives already ends at a word boundary or `…`).

## 6 · Pending items / spec deviations

- The example diagram line's unclipped state (§5) — declared punt, out of the LLR's scope; not
  opened as a backlog item (the operator's call whether a diagram token deserves the clip).

## 7 · Suggested next task

- Increment 003 — the chain-map carries (the deep-chain cap at `views.py`'s fold; the one-pass
  resize heal at `app.refresh_view`), serialized after this increment by design (§2.8).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 2 source files (app.py · modals.py) |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_undo_toast.py` (2) + `tests/test_help_clip.py` (2) landed with the product in the same run |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `_clip_words` — the unit pin, mutation-proven (M4) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | M3 (clean re-run) / M4 executed; transcripts `evidence/m3-anchor-fix.log` · `evidence/m4-arms.log` · `evidence/mutations-abc.log`; restore digests `9d9ac6e0…9921` · `88d45a33…b85b` |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | 5 probes run (table above) |
| 6 | `code-reviewer` passed — HIGH blocks; verdict + reviewer in §4b | `core` · `full` | ✓ | §4b — `human:coordinator` self-executed lenses · PASS-WITH-NOTES 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane; this increment landed after 001/004 had settled (its brief's disjoint set: app.py + modals.py); `git diff --name-only HEAD` per increment |
| 8 | Frozen interfaces untouched | all | ✓ | the `query("Label")` census contract preserved BY `_HelpLine(Label)`; the notify contract matches the house discipline; the other branches/stale-skip untouched |
| 9 | Coverage claims verified **on disk** | all | ✓ | every claim cites a stored transcript + sha256 (Evidence files table) |
| 10 | Load-bearing emptiness declared, with synthetic instance | all | ✓ | the no-mid-word-line sweep over both columns + the long-line fixtures |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | per-node table above; the vacuous GREEN arm named with its mechanism |
| 12 | **Instrument RED-proof** declared | all | ✓ | 4 instruments (table above) |
| 13 | **Correction population** declared | all | ✓ | the ten-item backlog tranche, enumerated before the first edit |
| 14 | **Emitted-form assertion** declared | all | ✓ | the painted Toast + the painted per-line help text + the clip outputs |
| 15 | **Independent review** names somebody | all | ✓ | §4b — `human:coordinator` |
| 16 | **Evidence files** declared | all | ✓ | 6 artifacts with stored-byte digests |
