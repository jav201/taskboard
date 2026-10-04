# Increment 001 — HLR-401 (LLR-401.1, LLR-401.2, LLR-401.3) · user and synced text as Text pieces; the census

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-04` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-401 (LLR-401.1, LLR-401.2, LLR-401.3; §6.5 A-1..A-4); the picker half of S-1 (HLR-404's visible seat, LLR-401.3) |
| Acceptance | AT-401, AT-402, AT-403 · white-box TC-401, TC-402, TC-403, TC-404, TC-405, TC-406, TC-412, TC-415 · unit TC-417 (layer 0) |
| Agent | `software-dev` (this runtime's implementing agent); `tester` authored AT-401..403, TC-412, TC-415 and the details payload extension |
| Date | `2026-10-03` |

---

## 1 · What changed

**No dialog, picker, select, button or toast hands user, synced or OS text to a markup parser any
more: the text is a Rich `Text` piece, painted exactly as written, styled as before.** A title, a
project or phase name, a synced roster name or project status, a typed id, a path or an exception
holding `[LINK=http://e]x`, `x\\\` or `:smile: [b]y[/b]` no longer kills the screen, vanishes or
changes (19 reachable sites, §5.1 of the contract; on base 29 + 5 + 11 + 2 arms were RED). The
project picker's line is built from pieces, so a teammate's `team.json` status can no longer carry a
clickable action into it (the picker half of S-1; the validation half is increment 002). Every
toast carrying user or OS text has markup off and no `escape`. The notes' highlights in the details
view and the editor preview are pieces from ONE tokeniser, `views.highlight_segments`, which the
board's `_highlight_markup` now reads too — its output byte-identical, except that an empty highlight
(`====`) no longer raises (`TypeError` on base, D-415). A census test derives every Textual sink and
markup parser in the package from the code (150 sink sites) and fails on any new site fed a str,
any parser over a non-literal, or a `-> Text` helper that does not return a Text; seven sites are
declared (five app-constant, the two board repaints, D-402/D-405).

Mechanism: `modals.py` — `_rich` retired; every user-text sink is `Text(...)` / `Text.assemble(...)`
with constant styles; calendar title and grid built as `Text`; Select prompts as `Text`; the
picker, phase, palette lines as `Text`; ConfirmModal/TextPrompt/confirm Button as `Text`; the phase
editor's duplicate toasts `markup=False`. `app.py` — eleven notifies `markup=False`, `escape` dropped
(and its import). `views.py` — `highlight_segments` (NEW), `_highlight_markup` reads it.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | HLR-401, LLR-401.1, LLR-401.2, LLR-401.3 | every user-text sink a Text piece; `_rich` retired; `notes_preview` from `highlight_segments`; calendar, pickers, selects, confirm, prompt, standup, help, palette as Text; duplicate-phase toasts markup off |
| `taskboard/app.py` | source | HLR-401, LLR-401.2 | eleven notifies with user/OS text `markup=False`, `escape` dropped |
| `taskboard/views.py` | source | LLR-401.3 | `highlight_segments` (NEW); `_highlight_markup` reads it (D-411, D-415) |
| `tests/test_markup_census.py` | test | LLR-401.1, LLR-401.2, LLR-401.3 | NEW: TC-401..TC-406 — the derived census, planted module, exemptions keyed with bindings |
| `tests/test_markup_sites.py` | test | HLR-401, LLR-401.2, LLR-401.3 | NEW (`tester`): AT-401, AT-402, AT-403, TC-412, TC-415 |
| `tests/test_highlight_segments.py` | test | LLR-401.3 | NEW: TC-417 (layer 0, base oracle frozen in the test) |
| `tests/test_details_markup.py` | test | HLR-401 | HOSTILE + the batch's two payloads (`tester`, review F3) |
| `tests/test_app.py` | test | LLR-401.3 | two nodes rewritten in place: the picker and phase-editor lines are Text, no backslash (A-7) |
| `tests/test_archive.py` | test | LLR-401.2 | one node rewritten in place: the archive toast is raw with markup off (A-7) |
| `tests/test_prism_laws.py` | test | LLR-401.3 | the weekday-header exemption re-pointed at the unmarked literal |
| `tests/test_edit_window.py` | test | LLR-401.3 | one docstring: the preview is built from pieces (review F4) |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 8 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_markup_census.py tests/test_markup_sites.py tests/test_highlight_segments.py tests/test_details_markup.py
python -m pytest -q -p no:cacheprovider
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** (cyclomatic ≥3, or crosses a declared module boundary) | `core` · `full` | TC-417 ×9 (`highlight_segments`: five paths) | 9 passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-401..TC-406 (census), TC-412, TC-415 | 8 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-401, AT-402, AT-403 (67 + 12 + 17 arms, one `run_test` per arm) | 3 passed |

Gate run on the frozen round-3 tree (`evidence/inc001-frozen-r3.sha256`, 11/11 OK):
`python -m pytest -q -p no:cacheprovider` → **1888 passed, 1 failed in 274.84 s**; the one failure is
`tests/test_app.py::test_win_clipboard_roundtrip`, whose own SETUP message names the environment
(`Set-Clipboard` failed), as on base (`evidence/base-suite.txt`) — `evidence/inc001-green.txt`.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | (a) the base tree `56a1b10` with this increment's new tests overlaid (`git archive` export); (b) the battery below on the increment tree |
| Instrument | `evidence/mutate.py` (batch-local; byte-exact restore after run 1) and `tester`'s `evidence/inc001_style_mutations.py` |
| Where it ran | scratch exports in the session scratchpad, never the live checkout |
| Transcript | `evidence/inc001-red-on-base.txt` (AT-401 29/67, AT-402 5/12, AT-403 11/17, TC-412 2/3 arms RED; TC-415 1/40 — the base calendar title's stray backslash); `evidence/inc001-red-census-base.txt` (TC-401, TC-402, TC-406 RED; TC-417 trigger-absent: `highlight_segments` missing); `evidence/inc001-details-red-on-base.txt` (8 failed) |
| Restore proven by | the battery's per-mutant sha256 check (all OK); `tester`'s 51/51 restores OK |
| Bytecode cache | `-B`, `-p no:cacheprovider`, `PYTHONDONTWRITEBYTECODE=1` |
| Arms resolved at baseline | AT-401 67, AT-402 12, AT-403 17, TC-412 3, TC-415 51 (`tester`'s counts) |
| Verdict granularity | per node (`-rA`), per arm inside each AT node (failures collected) |
| Arms that stayed GREEN | named in `inc001-red-on-base.txt`: 38 AT-401, 7 AT-402, 6 AT-403, 1 TC-412 arms are not RED on base by construction (a payload the base parser happens to leave intact — e.g. `:smile:` at Textual-parsed sites); kept as preservation arms |

| Field | Value |
|---|---|
| **RED counterfactual** | the base tree (no Text pieces, no tokeniser) with this increment's tests: AT-401/402/403 and TC-412 RED per site, TC-401/402/406 RED listing the sites, TC-417 RED (import absent) — `evidence/inc001-red-on-base.txt` sha256 `f2b40b62…`, `evidence/inc001-red-census-base.txt` sha256 `ecb93bcb…`; ran on `git archive` exports, live tree untouched (restore n/a); the battery's restore digests in `evidence/inc001-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 18/18 KILLED over two runs of `evidence/mutants_inc001.json` / `mutants_inc001_r3.json` (byte-exact sha256 restores): M1 confirm message as str · M2 picker line re-parsed · M3 archive toast markup on · M4 notes pieces untoned · M5 tokeniser tone swapped · M6 calendar base style dims days · M7 transition-log markup on · M8 identity picker str · M9 prompt title unbolded · M10 board markup re-escaped · M11 phase toast markup on · M12 sync-failure markup on · C1 census drops `tooltip` · C3 census drops `from_markup` · C4 census trusts any `+` · C5 census trusts the annotation · C6 census judges the last namesake only — all KILLED; C2 (census trusts a tuple rebinding) SURVIVED run 2 (an inert planted arm), the arm was rewritten and C2 KILLED in run 3 — `evidence/inc001-mutations.txt` sha256 `0ecbc0d4…`, `evidence/inc001-mutations-r3.txt` sha256 `9e05770a…`. TC-415 per arm (`tester`): 42/51 KILLED; 9 painted bold arms survive by design (the `.modal-title` CSS carries the bold), each with a KILLED "(CSS bold off)" sibling — `evidence/inc001-style-mutations.txt` sha256 `3ac57fa9…` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the census (TC-401..406) | the base package; the planted module (`PLANTED`, 30 unsafe forms) | base: 45 + 15 sites listed (`inc001-red-census-base.txt`); planted: each form flagged (TC-403 asserts the exact list) |
| `mutate.py` | its first run on an LF file (a text round trip rewrote it as CRLF) | `restore sha256 … MISMATCH` + `AssertionError`, battery stopped (`inc001-mutations-run1-aborted.txt`) — fixed to byte-exact, re-run |
| the AT harness (one `run_test` per arm) | the base tree | per-arm RED list, every failing site named (`inc001-red-on-base.txt`) |
| TC-415's style reader | the planted calendar defect during the conversion (`Text(header, style="dim")`) | `calendar selected day … now … '#89919b'` — RED before the fix (§5) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 4 instruments, each shown RED before its first PASS was believed: the census, the mutation harness, the AT harness, TC-415's reader (table above) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the painted screen (dialogs, pickers, toasts) | AT-401..403 read `app.screen._compositor.render_strips(...)` cropped to the widget's region, and `str(toast.render())` of each painted `Toast` | 96 arms GREEN on the increment tree (`inc001-sites-green.txt`) |
| `_highlight_markup`'s markup string | TC-417 compares the emitted string with the base function's, byte for byte, over ≥ 1000 derived inputs | equal on every input the base rendered (`inc001-green.txt`) |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts, each asserted against the form its producer emitted (table above) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| gate run, frozen r3 | `.dev-flow/2026-10-02-batch-04/evidence/inc001-green.txt` | `a03b63076b2af5460ea27ecd68693468e6abe61675539d16778c4a28f9fd6d27` |
| AT/TC RED on base | `.dev-flow/2026-10-02-batch-04/evidence/inc001-red-on-base.txt` | `f2b40b62db8406233ed9e5cf72f4e09c4c56703556903c745553c7614d67d75e` |
| census/tokeniser RED on base | `.dev-flow/2026-10-02-batch-04/evidence/inc001-red-census-base.txt` | `ecb93bcb85d6830d53338147814af14d4e18df0a25c2bf58f8e6faa083f1cc0b` |
| details payloads RED on base | `.dev-flow/2026-10-02-batch-04/evidence/inc001-details-red-on-base.txt` | `a4e71c1358bd36a471f6330e264b6c5c00544242e0c15560711094dfc501c4c8` |
| battery run 2 | `.dev-flow/2026-10-02-batch-04/evidence/inc001-mutations.txt` | `0ecbc0d4a33bfacc0a482fb0f4e4ef854e1d0da45a68727f6009c07b7cd003e0` |
| battery run 3 (C2, C5, C6) | `.dev-flow/2026-10-02-batch-04/evidence/inc001-mutations-r3.txt` | `9e05770a0646a616c90d251b01a53640ed1223b8fdfcf2eb46ce5a7621d36151` |
| battery run 1 (aborted, kept) | `.dev-flow/2026-10-02-batch-04/evidence/inc001-mutations-run1-aborted.txt` | `016d37f55be30b51c9d5af3277e06ad55b9d6e07ada9566404c099519d5fbd5a` |
| TC-415 per-arm battery | `.dev-flow/2026-10-02-batch-04/evidence/inc001-style-mutations.txt` | `3ac57fa99524c79cfdce8562b010bc81d5abc5d3a0c3079a424d06845bb49f4c` |
| TC-415 base flags | `.dev-flow/2026-10-02-batch-04/evidence/inc001-style-base-r2.txt` | `189a2d84cd09646b4e026bb1075f204e35ce0f44f95979a321f2f017c58862f5` |
| site tests green | `.dev-flow/2026-10-02-batch-04/evidence/inc001-sites-green.txt` | `11dd25102b09367857ac787bc8e17e41b82fb8937a5d98d710c74c76d150dc72` |
| reverse census | `.dev-flow/2026-10-02-batch-04/evidence/inc001-reverse-census.txt` | `72b4bdfcdd1b674ffc5c50dd34875ad5c01d355f38e3163ee6f86952399da37d` |
| frozen set, round 3 | `.dev-flow/2026-10-02-batch-04/evidence/inc001-frozen-r3.sha256` | `f4d6649e99fb4f3ec909e1e59d49c7d12992891e2e76b4b693e66d30d7bf038a` |

| Field | Value |
|---|---|
| **Evidence files** | 12 artifacts at `artifact_homes.evidence`, each cited with the digest of its stored bytes (table above); home paths redacted to `<home>` / `<user>` before hashing |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "0 non-exempt unsafe sites" and "0 parser calls over a non-literal" (TC-401, TC-406) |
| If the result is an ABSENCE, what made the search wide enough | the census derives its sinks from Textual's constructor signatures and every method/attribute sink form the P2 reviews named; TC-404 guards the population (≥ 140 sites, 11 kinds, every imported widget censused or declared plain) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | TC-403 / TC-404 docstrings say they protect the census's reach |
| Conjunctive criteria: one mutation per conjunct | sink rule and parser rule mutated separately (C1, C3, C4, C5, C6, C2) |
| Synthetic instance of the absent case | `PLANTED` in `tests/test_markup_census.py` (30 unsafe forms, 12 safe) |
| **Positive control for every probe that returned an ABSENCE** | the base package: 45 unsafe sinks + 15 unsafe parser calls (`inc001-red-census-base.txt`) |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -l -F <symbol> tests/*.py` per touched symbol (`evidence/inc001-reverse-census.txt`) | 16 files hit (`ConfirmModal`, `TextPrompt`, `TeamIdentityPicker`, `BlockerPicker`, `StandupModal`, `CommandPalette`, `HelpModal`, `Report written`, `pinned`, `Mo Tu We`, `highlight_segments`); four nodes rewritten in place (A-7 ×3, the weekday exemption); every other hit re-validated by the full run (1888 passed) |
| B2 file moved on disk | `git diff --name-status HEAD -- taskboard tests \| grep ^R` | 0 |
| B3 byte-identical golden captures this source | `ls tests/goldens` | no such directory |
| B4 artifact produced here is consumed elsewhere | who reads what this increment writes | none — paint only, no file format |
| A3 | interface consumed by another module changed | `grep -rln _rich taskboard tests` | `modals._rich` removed — no importer (docstring mentions only); `views.highlight_segments` NEW, read by `modals.notes_preview`; `_highlight_markup` unchanged signature |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 with their commands and verdicts: B1 16 files hit, 4 nodes rewritten in place, the rest re-validated by the full run; B2, B3, B4 0 hits; A3 one removed helper with no importer and one new reader (`evidence/inc001-reverse-census.txt`) |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| user text reaching a markup sink or parser | every Textual sink site and parser call in `taskboard/` | the census (`evidence/p1-census-iter2.txt`, before any edit) | 58 sinks + 15 parsers | 58 + 15 | 0 — the two board repaints declared (D-405) |
| assertions pinning the old escaping | tests asserting `\[` output or `_rich` | the P2 architect census (A-7) + `inc001-reverse-census.txt` | 3 + 1 | 4 | 0 |

| Field | Value |
|---|---|
| **Correction population** | 2 corrections, each enumerated before its first site was edited (table above) |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| `_rich(` in product code | 0 hits in `taskboard/` | yes | `grep -n "_rich(" taskboard/*.py` → none |
| `escape(` in `modals.py` / `app.py` | 0 | yes | `grep -n "escape(" taskboard/modals.py taskboard/app.py` → none |

### Signed-balance test ledger

`post = base − deleted + added` → `1889 = 1855 − 0 + 34` ✓ reconciles (6 census, 5 sites, 9 tokeniser, 14 details payload arms; 1888 passed + the clipboard environment failure)

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` · PASS-WITH-NOTES, 0 HIGH over three rounds on frozen sets (`inc001-frozen-r1/r2/r3.sha256`): round 1 OK-with-fixes (F1 MEDIUM census fooled by a `-> Text` annotation → folded, A-1; F2 MEDIUM six TC-415 bold arms could not go RED → folded by `tester`, declared pins + CSS-off arms; F3 MEDIUM details payloads → folded; F4 LOW docstring → folded; F5 LOW test names → accepted), round 2 OK-with-fixes (G1 MEDIUM namesake bypass → folded, C6 KILLED; G2, G3 LOW → folded), round 3 OK to advance (H1 MEDIUM six name-shadowing census bypasses, unused by the package, and H2 LOW → BACKLOG, the set left unmoved) |

---

## 5 · Risks

- The census is syntactic: six name-shadowing shapes still fool its `-> Text` trust (review H1 — a local rebinding, a parameter, an import alias, an uncensused module's helper, `self.x = str`, an unannotated namesake); the package uses none today. Also a module-attribute widget (`w.Label(x)`), a widget subclass passing `content` to `super().__init__`, `getattr(Text, "from_markup")` (review round 1). BACKLOG.
- Nine TC-415 bold arms are preservation pins the CSS carries; a stylesheet change removing `.modal-title`'s bold would not be seen by a code mutation — their CSS-off siblings would.
- The project picker shows a synced status as text but does not validate it until increment 002 (S-1 stays `BLOCK-UNTIL` until then).
- Working-copy line endings: `app.py` and three test files are LF in the working tree (others CRLF); git (`core.autocrlf=true`) normalises both on commit, the diff is content-only.

## 6 · Pending items / spec deviations

- Contract amendments §6.5 A-1..A-4 (ledger LED .10): seven exemptions; the title tail bold as base paints it; TC-417/D-415; `_init_team_mode`.
- BACKLOG at close: census residual gaps (H1, H2, round-1 residuals); the two test names (F5).
- The details grid fields still read via `w.render()` in `test_details_markup.py` — increment 003.

## 7 · Suggested next task

Increment 002 — S2 + S-1/S-3 validation (LLR-402.1..3, LLR-404.1, LLR-404.2; AT-404, AT-405, AT-407 by `tester`).

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 3 / 4 |
| 2 | Tests written in this same increment | all | ✓ | §2: 3 new test files, 5 changed |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | TC-417 ×9 over `highlight_segments` (five paths); the converted builders are branchless or delegate (out of layer 0) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 field; `inc001-red-on-base.txt`, `inc001-red-census-base.txt` |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 field; `inc001-reverse-census.txt` |
| 6 | `code-reviewer` passed — a HIGH blocks | `core` · `full` | ✓ | §4b: three rounds, 0 HIGH, OK to advance |
| 7 | No file from another lane touched | all | ✓ | one lane (§2.8) |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | no fork; `_highlight_markup`'s signature and output kept (TC-417) |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | the nodes in §4 ran in `inc001-green.txt` (1888 passed) |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 C-55 table; `PLANTED` |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 field: 18/18 product + census mutants; TC-415 42/51 with 9 declared pins |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 table: 4 instruments |
| 13 | **Correction population** declared | all | ✓ | §4 table: 2 corrections |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 table: 2 artifacts |
| 15 | **Independent review** names somebody | all | ✓ | §4b: `code-reviewer` |
| 16 | **Evidence files** declared | all | ✓ | §4 table: 12 files with digests |
