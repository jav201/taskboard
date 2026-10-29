# Review — taskboard — Batch 2026-10-29-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3, through PDR (round 2: architect, qa-reviewer and security-reviewer approve the amended contract; round 1 was `iterate-to-refine` — S1 HIGH and requirement-defect majors — folded by D1–D20, `LED-2026-10-29-batch-01.1` … `.20`; the round-2 residue minors folded by R1–R7, `LED-2026-10-29-batch-01.21`)
- **Out-of-scope findings:** `none` — every finding is folded into the contract or carried, named, into its owning increment below

- **Findings:** `1` blocker · `15` major · `26` minor (rounds 1+2 cumulative: round 1 1/15/18; round 2 0/0/8)
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box (round 1's ✗ on AT-3107, Q2, folded by D10 and closed at round 2)
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ⚠ `11` findings, all closed or folded — S1 (HIGH) discharged at contract level at round 2, its mitigation `planned` and re-verified at the increment 001 and 003 gates; S2–S9 closed (S8 as an accepted risk); round-2 minors SN1, SN2 folded
- **Evidence checklists (architect / qa / security):** ✓ all complete (summaries below; the raw lens reports are the orchestrator's working notes)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

### Review setup

- **Batch:** `2026-10-29-batch-01` · **Input:** `01-requirements.md` as approved at P1 (commit `2b9343d`), with `docs/ARCHITECTURE.md` (ARQ) and `PLAN.md`.
- **Lenses:** `architect` + `qa-reviewer` + `security-reviewer` (trigger family C fired — C4, C6, C8), each spawned as an independent generic sub-agent carrying the bundle's `agents/<role>.md`; none of them authored the contract (the scribe did, from the orchestrator's brief).
- **Round 1 verdicts:** architect `iterate-to-refine`; qa-reviewer `iterate-to-refine` (no blocker); security-reviewer `iterate-to-refine` (S1 HIGH).
- **Dispositions:** the orchestrator ruled D1–D20 (contract folds) and the named implementation carries. Each D is one ledger entry, `LED-2026-10-29-batch-01.<n>` with `<n>` = the D number. The `file:line` column cites the round-1 contract (`2b9343d`) as the lens raised it.

### Findings (round 1)

| ID | Lens | Severity | Requirement | file:line | Finding (one line) | Disposition |
|----|------|----------|-------------|-----------|--------------------|-------------|
| S1 | security-reviewer | blocker (HIGH) | LLR-3106.2, §6.3 | `taskboard/models.py:915`, `prototypes/html_report/variant_b/build.py:475`, `taskboard/views.py:273` | Task URLs are unrestricted on load and the prototype sets `a.href = u`: a `javascript:`, `data:` or `file:` URL in a board file is stored XSS in both reports. | folded-in-LED-2026-10-29-batch-01.1 (D1) — OPEN until the security lens re-reads |
| S2 | security-reviewer | major | HLR-3103, LLR-3103.1, LLR-3103.2 | `01-requirements.md:213`, `:372` | The byte check covers only project X's names and titles; every dropped project/board/person/class name needs a raw and JSON-escaped byte search, and the shell must hold no board text outside the data element. | folded-in-LED-2026-10-29-batch-01.2 (D2); test arms carried — increment 002 |
| S3 | security-reviewer | major | LLR-3103.2 | `01-requirements.md:378` | JS `String.replace` with a `$&` or `$'` in board text re-inserts the full block into the downloaded file. | folded-in-LED-2026-10-29-batch-01.3 (D3); carried — increment 002 |
| S4 | security-reviewer | minor | LLR-3106.1 | `prototypes/html_report/variant_b/build.py:479` | "never `innerHTML`" contradicts the server-built `notes_html` the page inserts. | folded-in-LED-2026-10-29-batch-01.4 (D4) |
| S5 | security-reviewer | minor | LLR-3103.2 vs LLR-3102.3 | `01-requirements.md:378`, `:358` | Restoring `meta.view` bypasses the hash whitelists. | folded-in-LED-2026-10-29-batch-01.5 (D5); carried — increment 002 |
| S6 | security-reviewer | minor | LLR-3101.1, LLR-3103.1 | `prototypes/html_report/variant_b/build.py:100-125` | A task carries other tasks' titles in `deps`; `chain` is undefined — a kept task can leak a dropped task's title. | folded-in-LED-2026-10-29-batch-01.6 (D6) |
| S7 | security-reviewer | minor | scope (HR-1) | `prototypes/html_report/variant_b/build.py:562-600` | The round's CSV/JSON downloads are untraced in the contract; CSV formula injection. | folded-in-LED-2026-10-29-batch-01.7 (D7) |
| S8 | security-reviewer | minor | HLR-3107 | `01-requirements.md:272` | The default scope `o` writes every board's data beside the open board; at least a header note, or default `p`. | folded-in-LED-2026-10-29-batch-01.8 (D8 — default kept, accepted risk with two controls) |
| S9 | security-reviewer | minor | §6.3 | `taskboard/app.py:3554-3565` | The wording leans on the image opener's gates, which do not apply; the safety rests on the path being app-written — pin it. | folded-in-LED-2026-10-29-batch-01.9 (D9); assertion carried — increment 004 |
| Q1 | qa-reviewer | major | LLR-3107.2, HLR-3107 | `01-requirements.md:452`, `:277` | "Contains `b c a p o esc`" is vacuous over a painted screen; assert key-line tokens by pattern. | folded-in-LED-2026-10-29-batch-01.10 (D10); test side carried — increment 004 |
| Q2 | qa-reviewer | major | AT-3107 | `01-requirements.md:276`, `:619`; `tests/test_modal_keys.py:324-335` | AT-3107 is not black-box: the law checks painted keys only for Button modals; press `H`, read the key line, press each key, assert its effect; the INVENTORY row is a TC. | folded-in-LED-2026-10-29-batch-01.10 (D10); test side carried — increment 004 |
| Q3 | qa-reviewer | major | LLR-3102.1 | `01-requirements.md:331-332` | The Tab-reach oracle uses the same selector as the control set it checks; it needs an independent, hand-enumerated list. | folded-in-LED-2026-10-29-batch-01.11 (D11) |
| Q4 | qa-reviewer | major | HLR-3101 | `01-requirements.md:181` | The deck's task-count observable is undeclared (what is printed, what it counts); expected counts must be fixture literals. | folded-in-LED-2026-10-29-batch-01.12 (D12); literals carried — increment 004 |
| Q5 | qa-reviewer | major | HLR-3103, LLR-3103.2 | `01-requirements.md:213`, `:379` | The shell and `meta.view` may carry hidden keys, ids, names or URLs; search each, raw and escaped, by a unique token. | folded-in-LED-2026-10-29-batch-01.2 (D2); arms carried — increment 002 |
| Q6 | qa-reviewer | major | LLR-3103.2 | `01-requirements.md:382-383` | The duplicate negative control compares sets, which collapse duplicates. | folded-in-LED-2026-10-29-batch-01.13 (D13); arm carried — increment 002 |
| Q7 | qa-reviewer | major | HLR-3104, LLR-3104.1 | `01-requirements.md:229`, `:392` | `beforeprint` never fires under `emulate_media`; `break-inside` unread under print; modal and tooltip not opened before the print arm. | folded-in-LED-2026-10-29-batch-01.14 (D14) |
| Q8 | qa-reviewer | major | §5.1, §5.2 | `01-requirements.md:621`, `:631` | `importorskip` contradicts "the only accepted skip is TC-1902"; 0 browser skips on this machine, and node counts by `--collect-only`. | folded-in-LED-2026-10-29-batch-01.15 (D15) |
| Q9 | qa-reviewer | minor | LLR-3102.2 (TC-3106) | `01-requirements.md:351` | Boundary arms need literal id sets; define the case folding. | carried — increment 001 |
| Q10 | qa-reviewer | minor | LLR-3102.3 | `01-requirements.md:363` | The named mutation is unreachable behind the whitelist; mutate "drop the whitelist and echo into the summary via `innerHTML`". | carried — increment 001 |
| Q11 | qa-reviewer | minor | AT-3106 | `01-requirements.md:261` | Scripts inserted by `innerHTML` do not run, so a `<script>` payload cannot fail the arm; add `<img onerror>` with a `window.__x` sentinel, and hostile project and board names. | carried — increment 003 |
| Q12 | qa-reviewer | minor | LLR-3101.3 | `01-requirements.md:320` | The import probe is a regex; use an AST walk. | carried — increment 001 |
| Q13 | qa-reviewer | minor | LLR-3107.3 | `01-requirements.md:462` | The fixture's project "Client A" shares a board's name. | folded-in-LED-2026-10-29-batch-01.20 (D20) |
| Q14 | qa-reviewer | minor | LLR-3107.4 | `01-requirements.md:469`, `:277` | Name the clock seam; read the notification record, not the screen; patch `os.startfile` with `raising=False`. | folded-in-LED-2026-10-29-batch-01.16 (D16); test side carried — increment 004 |
| Q15 | qa-reviewer | minor | boundary catalogs | `01-requirements.md:203`, `:251` | Missing arms: unicode and long titles at 390 px, all status chips off, `from == due`, scope `p` on an all-archived project. | folded-in-LED-2026-10-29-batch-01.17 (D17) |
| Q16 | qa-reviewer | minor | LLR-3101.2 | `01-requirements.md:311` | Pin the due-word literals. | carried — increment 001 |
| A1 | architect | major | HR-1 / C4 | `.dev-flow/COMMISSION-html-report.md:36`; `prototypes/html_report/variant_b/build.py:574-600` | The CSV/JSON download is untraced, leaks dependency titles and notes, and its label is false. | folded-in-LED-2026-10-29-batch-01.7 (D7) |
| A2 | architect | major | LLR-3101.1, LLR-3102.2, LLR-3103.1, LLR-3105.1, §5.1 | `taskboard/models.py:871`, `taskboard/views.py:979-989`, `prototypes/html_report/variant_b/build.py:86-91` | Project-less (Inbox) tasks are undefined: key, filter, deck slide, download, fixture. | folded-in-LED-2026-10-29-batch-01.18 (D18) |
| A3 | architect | major | LLR-3101.2 vs LLR-3102.2 | `taskboard/report.py:204`, `:217`; `taskboard/views.py:950` | The "late" rule contradicts itself and the JS re-derives it while the deck derives it server-side — two engines. | folded-in-LED-2026-10-29-batch-01.19 (D19) |
| A4 | architect | major | C4 — LLR-3103.1, LLR-3103.2, AT-3103 | `taskboard/boards.py:449-453` | The shell text, the hash `p` semantics, `meta.view`, key slugs and the summary may leak hidden data; widen the byte search. | folded-in-LED-2026-10-29-batch-01.2 (D2) |
| A5 | architect | major | LLR-3107.3, §6.3 | `taskboard/boards.py:399-410` | Scope `o` writes every board's data beside the open board, which may be a client's folder; declare it and decide the destination. | folded-in-LED-2026-10-29-batch-01.8 (D8 — accepted risk, two controls) |
| A6 | architect | minor | LLR-3101.1, IFC | `taskboard/app.py:841-871` | The deck's facts are missing from the dict; the `boards` shape; the unlisted board's id None; the IFC's `write_reports` input is wrong. | folded-in-LED-2026-10-29-batch-01.6 (D6) |
| A7 | architect | minor | HLR-3101 | `prototypes/html_report/variant_c/build.py:496-500`, `:780` | Whether archived tasks count in the agreement threshold is ambiguous. | folded-in-LED-2026-10-29-batch-01.12 (D12) |
| A8 | architect | minor | LLR-3101.3 (TC-3104) | `docs/ARCHITECTURE.md:100` | The import ban is a regex; use an AST probe. | carried — increment 001 (the deck file joins the probe at increment 003) |
| A9 | architect | minor | ARQ §4, LLR-3107.3 | `docs/ARCHITECTURE.md:147`; `taskboard/report.py:265-271` | `board_lanes`' new consumer and the consumed private helpers lack interface rows; the copied slug rule is unpinned; same-named projects on two boards collide in the file name. | folded-in-LED-2026-10-29-batch-01.20 (D20) |

Round-1 dispositions summary: the blocker S1 and every requirement-defect major are folded by the P1 amendment (D1–D20, one ledger entry each). Q9, Q10, Q11, Q12, Q16 and A8 are implementation carries, each named here with its owning increment; the increment gates close them. The test sides of D2, D3, D5, D9, D10, D12, D13 and D16 are carried into increments 002 and 004 the same way.

### Findings (round 2 — the three lenses re-read the amended contract)

Round-2 verdicts: architect `approve` (ledger pairs 53/53 both directions; A1–A7, A9 closed; A8 carried); qa-reviewer `approve` (Q1–Q8, Q14, Q15 closed; Q11–Q13, Q16 no objection); security-reviewer `approve` (S1–S9 closed; S1 HIGH discharged at contract level; S8 closed as an accepted risk). Each lens spawned again as an independent generic sub-agent carrying its `agents/<role>.md`. The residue minors below are ruled by the orchestrator's R1–R7 and folded as ONE ledger entry, `LED-2026-10-29-batch-01.21`; the PDR lenses review that fold with the design proposal.

| ID | Lens | Severity | Requirement | file:line | Finding (one line) | Disposition |
|----|------|----------|-------------|-----------|--------------------|-------------|
| qN1 | qa-reviewer | minor | LLR-3105.1 | `01-requirements.md:413` | Contradiction: a slide for "a project that has a task" versus an all-archived project's `0 tasks · k archived` slide — settle one rule. | folded-in-LED-2026-10-29-batch-01.21 (R1) |
| qN2 | qa-reviewer | minor | LLR-3103.3 (TC-3122) | `01-requirements.md:393` | The CSV's `'` prefix also hits `-3d` due words — assert it intentionally. | folded-in-LED-2026-10-29-batch-01.21 (R2) |
| SN1 | security-reviewer | minor | LLR-3103.1 | `01-requirements.md:373` | The download must also reduce `meta`'s scope board names and the header's N/names to the kept boards (a wording gap; AT-3103's byte search would catch it). | folded-in-LED-2026-10-29-batch-01.21 (R3); arm carried — increment 002 |
| SN2 | security-reviewer | minor | §6.3 | `01-requirements.md:680` | The "Not fired" bullet still says task URLs are inert links — they are filtered to http/https (the C8 bullet). | folded-in-LED-2026-10-29-batch-01.21 (R4) |
| AN1 | architect | minor | HLR-3105, LLR-3105.1 | `01-requirements.md:245`, `:413` | "One slide per non-archived project" (HLR) versus "that has a task" plus the Inbox rule (LLR). | folded-in-LED-2026-10-29-batch-01.21 (R1) |
| AN2 | architect | minor | LLR-3102.2 | `01-requirements.md:357` | The negative control "(status ignores the due date)" is stale now that status is emitted server-side — restate it as the JS chip mapping `late` → `open`. | folded-in-LED-2026-10-29-batch-01.21 (R5) |
| AN3 | architect | minor | ARCHITECTURE §3 | `docs/ARCHITECTURE.md:99` | The `report_html` dependency row lacks `views.valid_url`. | folded-in-LED-2026-10-29-batch-01.21 (R6) |
| AN4 | architect | minor | LLR-3105.1 | `01-requirements.md:413` | An all-archived project gets a slide and an all-archived Inbox does not — rationale unstated. | folded-in-LED-2026-10-29-batch-01.21 (R1) |

**Round-1 items still carried after round 2 (implementation, no contract change):**

| ID | Lens | Disposition |
|----|------|-------------|
| Q9 | qa-reviewer | carried — increment 001 (literal id sets for boundary arms; no case folding beyond JS `toLowerCase`, ASCII-only search fixtures) |
| Q10 | qa-reviewer | carried — increment 001 (the mutation: drop the whitelist and echo into the summary via `innerHTML`) |
| print width | qa-reviewer | carried — increment 002 (the page width is the viewport width under `emulate_media`) |
| A8, Q12 | architect, qa-reviewer | folded-in-LED-2026-10-29-batch-01.21 (R7: the AST import walk and its precise allow/ban lists); its execution carried — increment 001, re-run at increment 003 |
| Q11, Q16 | qa-reviewer | carried — increments 003 and 001, unchanged |


### shall / should check

✓ clean — every HLR/LLR statement reads `shall`; no modal `should` inside a statement (probe: `grep -n "Statement:.*\bshould\b" 01-requirements.md` → 0 hits).

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-3101 → AT-3101..AT-3107 → HLR-3101..HLR-3107 → LLR-3101.1..LLR-3107.5 → TC-3101..TC-3121 | yes | yes (files at `reports/`, the downloaded file, the painted modal and toast) | yes | no at round 1 — AT-3107 (Q2) | blocker → folded by D10 |

(a) ✓ US-3101 names AT-3101..AT-3107, one planned node each. (b) ✓ the output-producing requirements name the file (`reports/workspace-<date>.html`, `deck-<date>.html`, `workspace-view-<date>.html`) and how it is observed (headless Chromium, the bytes). (c) ✓ both chains complete. (d) ✗ at round 1: AT-3107 asserted the inventory and the law's arms, not the painted modal and the keys' effects — D10 rewrites it to press `H`, read the key line by pattern and press every key.

### Supersession census (change-first)

B1 fired. The census commands owed at P3, per increment, keyed on the planned edits:
- `grep -rl KEYMAP tests/` (15 files, `evidence/p1-probes.txt` probe 8), `grep -rl INVENTORY tests/`, `grep -rl open_url tests/`, `grep -rl build_report tests/`, `grep -rl report_path tests/` — increment 004 (and 001 for the slug pin, D20).
- Structural and placement guards over the three new files (`report_html.py`, `report_workspace.py`, `report_deck.py`): `rg -n "glob\(|listdir|iterdir|_root_modules" tests/` — increment 001.
- Frozen / no-diff guards over `report.py`, `views.py`, `__main__.py`: LLR-3107.5's `git diff 9da7438 --` — every increment.

Best-effort + gate-confirmed; the increment gate running the real suite is the completeness guarantee.

### Security review summary

Family C fired (C4 the filtered download, C6 the URL hash, C8 HTML rendering of file-derived board text), so the security lens ran. Verdict `iterate-to-refine`. **S1 (HIGH, blocker):** task URLs reach `href` unrestricted, so a hostile board file carries stored XSS into both reports. Fold D1: `extract` keeps only `views.valid_url` results (http/https, `taskboard/views.py:273`), the page re-checks `^https?://` before any `href`, links carry `rel="noopener noreferrer"`, and AT-3106 gains `javascript:` and `data:` URL arms asserting 0 non-http(s) anchors in both reports. **Round 2: the security lens re-read the fold and approves — S1 HIGH is discharged at contract level; its mitigation is `planned` (no code exists yet) and is re-verified at the increment 001 gate (`extract`'s filter, the workspace's `^https?://` check, TC-3124) and the increment 003 gate (the deck's links, AT-3106's `javascript:`/`data:` arms).** S2–S3 (major) and S4–S9 (minor) closed by D2–D9; S8 closed as an accepted risk with two controls (D8, `01-requirements.md` §6.3). Round-2 minors SN1 (the download reduces `meta`'s scope names) and SN2 (§6.3 wording) are folded by R3/R4 (`{L}`). The scan's flags are answered in §6.3 (`evidence/scan-p1-iter2.txt`).

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer

- **Architect** — ✓ the module map read against the tree and the contract (A9: missing interface rows); ✓ the dict's facts read against both prototypes (A6, A7); ✓ the status rule read across `report.py`, `views.py` and the JS (A3); ✓ the Inbox lane read in `views.lanes_of` (A2); ✓ the scope's write destination read in `boards.py` (A5); ✓ the commission's HR-1 read for the CSV/JSON downloads (A1).
- **QA-reviewer** — ✓ every AT read for black-box purity (Q2); ✓ every threshold read for vacuity (Q1, Q3, Q4, Q6); ✓ the print and download arms read for reachability under headless emulation (Q5, Q7); ✓ the skip policy read against §5.2 (Q8); ✓ boundary catalogs read for missing classes (Q15).
- **Security-reviewer** — ✓ the scan flags traced; ✓ every board-text sink enumerated (server templates, client JS, the download, the URLs — S1, S3, S4); ✓ the hash and `meta.view` read as input surfaces (S5); ✓ the download read as a data-exposure control (S2, S6, S7); ✓ the scope default and the opener read (S8, S9).

### Verdict

`approve` (round 2) — the gate tokens' home is `templates/review-template.md`. Round 1 was `iterate-to-refine`, folded by the P1 amendment D1–D20 (`LED-2026-10-29-batch-01.1` … `.20`); round 2's three lenses approve, and their residue minors are folded by R1–R7 (`LED-2026-10-29-batch-01.21`). PDR is next: the design proposal, reviewed by architect, qa-reviewer and ux-reviewer.
