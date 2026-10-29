# Batch close — taskboard — Batch 2026-10-29-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**, and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/guides/close-template.md` explains each field below and the rules that read it.

> **Reserved field names** (parsed literally, never translated): `Conditional-gate discharge` · `New controls` · `Human perimeter` · `Human review ledger` · `Gated tree` · `Found before the batch` · `⏸ DEFER` · and the §6 DEPTH tokens `light` · `rigorous` · `spot-check` · `none` · `✅` · `❌`.

> **Notice convention.** `⚠` yellow = declare and continue · `✗` red = block · `✓` green = satisfied **with its citation**.

---

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 179 notice · 2026-10-29 |
| Gated tree | `d853d2d26436703f007ee54cb4e8694b82b3b3d9` · dirty — .dev-flow/BACKLOG.md (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` — 26 ids folded by `--fold-canon` at close (`canon: REQUIREMENTS.md -- 26 folded, 0 kept, 0 refused`: HLR-3101..HLR-3107, LLR-3101.1..3, LLR-3102.1..3, LLR-3103.1..3, LLR-3104.1, LLR-3105.1..2, LLR-3106.1..2, LLR-3107.1..5); every id this batch's `01-requirements.md` declares as a heading is a token in it |

---

## 1 · What changed

The owner can now export, from the app, two HTML reports of every loaded board, built from one
extraction: press `H` (global, off the bar), choose `b` workspace, `c` deck or `a` both, and the scope
`o` all loaded boards (default) or `p` the current project; the files land in
`<board dir>/reports/` and a toast names them and the folder and offers `o` to open the file for
10 s. **B, the workspace**, has one control bar (projects, status, people, classes, dates, search,
sections, zoom, Reset, the active-filter count) whose view lives in a whitelisted URL hash; it prints
only the configured view (no controls, only the shown boards and projects named, the whole table
and gantt) and downloads "this view" as a new self-contained file holding only the kept tasks
(plus CSV/JSON of the visible rows, formula-guarded). **C, the deck**, is a cover, an overview and
one vector slide per project in scope, paged by keys, one slide per printed page. Both are offline
single files, light and dark, phone width, with every board string escaped and task URLs limited to
http(s). The mechanism: `taskboard/report_html.py` (`extract` → one JSON-able dict, `write_reports`),
`taskboard/report_workspace.py` and `taskboard/report_deck.py` render that dict alone; `keymap.py`,
`modals.py` (`ReportExport`) and `app.py` wire `H`, the files, the toast and the offer. The CLI
`taskboard --report` and the presentation's `x` export are unchanged (`git diff 9da7438` of
`report.py`, `__main__.py`, `views.py` = 0 lines).

**HR-1 — the CLI `--report` stays as it is.** Why: it is a single-board, script-free,
server-rendered document with its own laws in `tests/test_report.py` (read-only board, unaged, no
forecast) serving the CLI and scripts, where an interactive page adds nothing; re-pointing it to the
workspace would change a shipped CLI output and its 18 tests outside the commission's increments.
The new extraction reuses `report._e` and `report._due_word`, so the two cannot disagree on a due
word. Retiring or re-pointing it is the operator's decision, carried in `.dev-flow/BACKLOG.md`.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-3101` | v1 (LED .12) | `AT-3105` (`a` arm) · `TC-3101`..`TC-3104`, `TC-3125`; `tests/test_report.py` 18 | pass |
| `HLR-3102` | v1 (LED .15, .17) | `AT-3102` · `TC-3105`..`TC-3108` | pass |
| `HLR-3103` | v1 (LED .2, .7, .15) | `AT-3103` · `TC-3109`..`TC-3111`, `TC-3122` | pass |
| `HLR-3104` | v1 (LED .14, .15) | `AT-3104` · `TC-3112` (+ increment 005's arms) | pass |
| `HLR-3105` | v1 (LED .12, .15, .17, .21) | `AT-3105` · `TC-3113`, `TC-3114` | pass |
| `HLR-3106` | v1 (LED .1, .15, .17) | `AT-3106` · `TC-3115`, `TC-3116`, `TC-3124` | pass |
| `HLR-3107` | v1 (LED .8, .10, .15) | `AT-3101`, `AT-3107` · `TC-3117`..`TC-3120` | pass |
| `LLR-3101.1`..`LLR-3101.3` | v1 as amended (LED .1, .6, .18, .19, .21, .22, .25) | `TC-3101`..`TC-3104`, `TC-3124`, `TC-3125`; the 0-line diff | pass |
| `LLR-3102.1`..`LLR-3102.3` | v1 as amended (LED .2, .8, .11, .17, .18, .19, .21, .22, .23) | `TC-3105`..`TC-3108` | pass |
| `LLR-3103.1`..`LLR-3103.3` | v1 as amended (LED .2, .3, .5, .6, .7, .13, .18, .21, .22, .24, .27) | `TC-3109`..`TC-3111`, `TC-3122` | pass |
| `LLR-3104.1` | v1 as amended (LED .14, .22, .27) | `TC-3112` | pass |
| `LLR-3105.1`, `LLR-3105.2` | v1 as amended (LED .8, .12, .17, .18, .19, .21, .25) | `TC-3113`, `TC-3114` | pass |
| `LLR-3106.1`, `LLR-3106.2` | v1 as amended (LED .1, .4, .17) | `TC-3115`, `TC-3116`, `AT-3106` | pass |
| `LLR-3107.1`..`LLR-3107.4` | v1 as amended (LED .6, .8, .9, .10, .16, .20, .22, .26, .27) | `TC-3117`..`TC-3120`, `TC-3123`, `AT-3107` | pass |
| `LLR-3107.5` | v1 | `TC-3121` — an inspection pin (DQ6, `DDR-2026-10-29-batch-01#D3`): the 0-line diff + the green suites | pass |

Evidence: `04-validation.md` — `PASS-WITH-NOTES`, the P4 suite 3332 passed / 0 failed / 0 skipped in 3 sequential chunks at `18e6057` (3281 + 51).

### Decisions summary — every autonomous decision of the batch

All taken under the batch's standing authorization (`PLAN.md` header); each is recorded where named.

- **HR-1..HR-6** (the commission's decisions, `PLAN.md` §Key decisions): HR-1 one extraction, the CLI report kept (above); HR-2 the `H` key, the `ReportExport` modal, `reports/` files, the toast and `o`; HR-3 the control bar and the URL hash; HR-4 print and "Download this view"; HR-5 the deck; HR-6 offline, themes, 390 px, escaping.
- **Scribe decisions (1)–(13)** at P1 where the brief was silent (`PLAN.md` §Key decisions): keys = board id + id, the deck's slides, the action name, the `a` toast wording, the hash `v`, the current-project rule, the import seats (superseded at PDR), the client-side escape, the browser-AT route, the app-AT thread, no IFC Part B, the archived-project fixture, the empty ledger.
- **D1–D20** (P2 round 1 dispositions, one ledger entry each, `LED-2026-10-29-batch-01.1` … `.20`; `02-review.md` §Findings): D1 task URLs http(s) only (S1 HIGH) · D2 no board text outside the data element (the download's leak surface) · D3 no `String.replace` patterns · D4 one `innerHTML` exception, `notes_html` · D5 `meta.view` through the hash whitelists · D6 task keys not text; the dict's full fact list · D7 CSV/JSON downloads kept, visible rows, formula guard (new LLR-3103.3) · D8 scope default stays `o` — accepted risk, two controls · D9 the opener's safety on its real ground · D10 AT-3107 black-box; the INVENTORY row a TC · D11 TC-3105's hand-enumerated Tab oracle · D12 the deck's per-slide count and the agreement threshold · D13 multiset duplicate check · D14 the print arm reachable (explicit `beforeprint`, computed styles) · D15 no browser skip on this machine · D16 the `o` offer's clock seam · D17 the missing boundary arms · D18 the Inbox defined · D19 one status rule, server-side · D20 board slug in project file names; the slug pinned.
- **R1–R7** (P2 round 2 residue, `LED-2026-10-29-batch-01.21`): R1 one slide rule (all-archived projects and the Inbox) · R2 the CSV `'` prefix on due words asserted on purpose · R3 the download reduces `meta`'s board names and the header · R4 the §6.3 "not fired" bullet restated · R5 the JS chip mapping `late` → `open` as the negative control · R6 `views.valid_url` in the ARCHITECTURE row · R7 the AST import walk's allow/ban lists.
- **C1–C14** (PDR dispositions, `LED-2026-10-29-batch-01.22`; `design/PDR-2026-10-29-batch-01.md` §C): C1 the nine dict facts, `closed`/`inbox` dropped · C2 `notes_text` stripped with `notes_html` · C3 `views.HEX` frozen · C4 function-local `from . import`, no `importlib` · C5 `project` is the key · C6 captions beside every export control · C7 `@page { margin: 0 }`, printed counts over kept tasks · C8 the `o` offer single-use, main screen only · C9 the modal names the folder and the boards · C10 the count counts filter kinds · C11 count and Reset in the first viewport at 390 px · C12 a pressed chip differs by more than hue · C13 the CSV guard excepts plain numbers · C14 print width measured at 794 px.
- **LED .1–.27** (`01-requirements-ledger.md`): .1–.20 = D1–D20; .21 = R1–R7; .22 = C1–C14; .23 the active count's English (CR1, increment 001); .24 the download keeps no derived project facts and no mentions of withheld notes (SD1, CR2-1, increment 002); .25 finished work is never late, `1 task` / `N tasks` (increment 003); .26 the toast's failure wording and the singular skipped count (increment 004); .27 the printed view names only what it shows, the table prints whole, the toast on three lines (increment 005, the DDR corrections).
- **Increment-level decisions** (`PLAN.md` §Key decisions): PQ6 app-level browser checks in a worker thread; CR1 the count's wording; SD1/CR2-1 the reduced download.

### Reviewer roster, by gate

Every reviewer was an independent generic sub-agent carrying the bundle's `agents/<role>.md`; none authored what it reviewed.

| Gate | Reviewers | Verdict |
|---|---|---|
| P2 round 1 | architect · qa-reviewer · security-reviewer | `iterate-to-refine` (S1 HIGH + majors) → D1–D20 |
| P2 round 2 | architect · qa-reviewer · security-reviewer | `approve` → R1–R7 |
| PDR | architect · qa-reviewer · ux-reviewer | `approved with conditions` → C1–C14 |
| P3 increment 001 | code-reviewer · security-reviewer | OK to advance (with notes) · PASS |
| P3 increment 002 | code-reviewer (+ re-read on `613702e`) · security-reviewer | PASS · PASS |
| P3 increment 003 | code-reviewer · security-reviewer | OK to advance (with notes; CR3-2/CR3-3 fixes not re-read, declared) · PASS |
| P3 increment 004 | code-reviewer · security-reviewer | OK to advance (with notes; fixes not re-read, declared) · PASS |
| DDR | qa-reviewer · ux-reviewer | `approved with conditions` (C-DDR-1) → increment 005 → re-sealed `approved` |
| P3 increment 005 | code-reviewer | OK to advance (with notes; the print-wrap fix not re-read, declared) |
| P4 | qa-reviewer | accept with notes (V1–V4) |

**Runtime absences:** declared once in `PLAN.md` §*Gate notices and runtime absences* (no named reviewer roles, no hooks, no prompt guard, no slash commands; `V15`/`V16`/`V17` not-run from a bundle; `V30` half). **`dev-flow-sync`: `not-run`** — no export destination is declared (a bundle install ships no deployment record), and push/merge are not granted.

### Residual risks (accepted, named)

- **D8 — scope `o`, the default, writes every loaded board's facts beside the OPEN board** (`<board dir>/reports/`, which may be a client's folder). Accepted with two controls: the modal prints the destination folder and the board names before any key writes (LLR-3107.2, the `report-modal_118x30.png` capture), and both reports' header states the scope (LLR-3102.1, LLR-3105.1). The operator may revisit the default on `review.html`.
- **SD2 — the owner's search text travels in a downloaded view's `meta.view`** (summary and `q`) and is printed in its header. Accepted: it is the owner's own input, visible in the header before the file is sent; no hidden item's text travels.
- **The toast's long folder path wraps mid-word** (DU4 residue, low): the file name never splits (three lines since increment 005), but a long folder path breaks inside a word (`evidence/captures/terminal/png/report-toast_118x30.png`). Carried in BACKLOG.
- **CI cannot see the browser nodes** (Playwright is not a declared dependency; CI skips them): their evidence is this machine's transcripts (`01-requirements.md` §6.3).

### Open reviewer findings at close

None blocking; no HIGH open. Carried to `.dev-flow/BACKLOG.md`: CR5 (the Inbox key collision, LOW), CR3-4 (the deck legend from the first project, LOW), CR3-5 (a tall slide spans pages, LOW), CR4-4 (tests read Textual's private `_notifications`, watch item), DDR N1 (opaque modal backdrop) and N2 (faint dashed export buttons). Accepted, not carried: CR5-2 (the TC-3112 summary literal depends on the fixed fixture order). Declared, not re-read: the post-review fixes of increments 003, 004 and 005.

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| none — no new control minted. The batch's candidate lesson is recorded in `design/DDR-2026-10-29-batch-01.md` §*Lesson*: for every design criterion that names printed or exported text, the node asserts that text (and the absence of the forbidden text) in the artefact the recipient receives, with a fixture that hides something — a bound on an enclosing box does not bound a clipped child (the O1/O2 escape that increment 005 fixed). Encoding it as a flow control is the operator's sitting, not this close's. | — | — |

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a — no control minted | |
| 2 | its **artifact** (a template section) | n/a — no control minted | |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | n/a — no control minted | |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a — no control minted | |

- **New controls:** none — no control minted; the DDR's candidate lesson (assert the recipient's printed/exported text against a hiding fixture) is left for the operator's control-encode sitting.

---

## 3 · Working-file reconciliation (C-44)

Sweep: `git status --short` and `git log feat/html-report --not --remotes` in the one repository the batch touched (the worktree `C:/Users/jjgh8/Github/taskboard-wt/report-proto` of `taskboard`). `origin` answers (`origin/main` = `9cc7d4e`) but the branch `feat/html-report` is on no remote: push and merge are NOT granted (the commission: «Do NOT push or merge»), so every ✅ row lands on the local branch and the operator owns the landing.

| File | State | Evidence |
|---|---|---|
| `taskboard/report_html.py`, `taskboard/report_workspace.py`, `taskboard/report_deck.py` (new) | ✅ committed — local branch `feat/html-report`, not pushed (not granted) | `31eddb2`, `613702e`, `f7eb6d7`, `7b47714` |
| `taskboard/app.py`, `taskboard/modals.py`, `taskboard/keymap.py`, `README.md` | ✅ committed — same branch | `e8ec477`, `7b47714` |
| `tests/report_fixture.py`, `tests/report_browser.py`, `tests/test_report_html.py`, `tests/test_report_workspace.py`, `tests/test_report_deck.py`, `tests/test_report_export_app.py`, `tests/test_modal_keys.py` | ✅ committed — same branch | `31eddb2`, `613702e`, `f7eb6d7`, `e8ec477`, `7b47714` |
| `docs/ARCHITECTURE.md` (the module map) | ✅ committed — same branch | `cb76bee`, `263cd58`, `c36a392`, `d117ea0` |
| `.gitattributes`, `.dev-flow/2026-10-26-batch-01/decisions-log.json` (the rollover) | ✅ committed — same branch | `cb76bee` |
| `REQUIREMENTS.md` (the canon fold, 26 rows) | ✅ committed — same branch, the deliverable commit (§0 `Gated tree`) | the deliverable commit |
| `.dev-flow/2026-10-29-batch-01/` (the record, the evidence, the P4 transcripts, `review.html`) and `.dev-flow/state.json` | ✅ committed — same branch, the batch commits and the deliverable commit | `cb76bee` … `18e6057`; the deliverable commit |
| `.dev-flow/BACKLOG.md`, `.dev-flow/2026-10-29-batch-01/05-close.md` | ✅ committed — same branch, the close commit | the close commit |
| `.scratch/` (the orchestrator's briefs, review notes, harness scripts) | 📋 left on purpose — git-excluded (`.git/info/exclude`), never committed; the orchestrator deletes it after the close (its plan, step 6) | `git status --short` shows no `.scratch/` entry |
| the 7 commits before the batch on the branch (`47e4a88` … `9da7438`: the prototype round, the commission, the handoff) | found on the branch at open (`base_ref` `9da7438`), unpushed — not this batch's; they land with the branch when the operator pushes | `git log feat/html-report --not --remotes` (24 commits before the close: 7 prototype + 17 batch) |

- **Found before the batch:** `none — no tracked file was modified when the batch began`

### Conditional-gate discharge

- **Conditional-gate discharge:** 3 condition(s) · ✅ all discharged

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PDR C1–C14 (the contract-level conditions) | ✅ | `01-requirements-ledger.md` `LED-2026-10-29-batch-01.22`; `design/PDR-2026-10-29-batch-01.md` §C table (each C row names its contract line) |
| PDR increment-owned conditions (PA2–PA5, PA7, PQ1–PQ11, PU1–PU7) | ✅ | `design/DDR-2026-10-29-batch-01.md` §B row 8 (all re-read; Q9 partial and PU2 open there) + §Discharge (DQ5 → the literal dates arm, DQ2 → the print scope; increment 005) |
| DDR C-DDR-1 (DQ1, DQ2 high; DQ3–DQ5, DU3–DU5) | ✅ | `design/DDR-2026-10-29-batch-01.md` §Discharge: increment 005 (`7b47714`), `suite-005.txt` 68 passed, `mutation-005.txt` 15/15; re-sealed `approved` |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| (no prior BACKLOG item named this story — the commission came from the operator's prototype verdict) | nothing to mark shipped | `.dev-flow/COMMISSION-html-report.md` |
| CR5 — the Inbox key collision | carried (already in the batch's section) | `.dev-flow/BACKLOG.md` §Open — after `2026-10-29-batch-01` |
| CR3-4, CR3-5 — the deck's legend; a tall slide spans pages | carried (already there) | same section |
| CR4-4 — tests read Textual's private `_notifications` | carried — moved into the batch's section from the cross-platform CI section, where it had been appended | same section |
| DDR N1, N2 — the opaque modal backdrop; the faint dashed export buttons | carried — moved into the batch's section from the CI section | same section |
| the CLI report: retire, re-point or keep (HR-1) | NEW — the operator's call | same section |
| the toast's long folder path wraps mid-word (DU4 residue) | NEW | same section |
| the cross-platform CI fixes (Linux, macOS) | untouched — the operator's item from 2026-10-29 | `.dev-flow/BACKLOG.md` §Open — cross-platform CI |
| qa note V2 (confirm the BACKLOG holds CR3-4, CR3-5, CR4-4, CR5, N1/N2) | discharged by the moves above | `04-validation.md` §QA-P4 notes |
| the header | refreshed — `Last refresh: 2026-10-29 (2026-10-29-batch-01 close …)`, `origin/main` = `9cc7d4e`, the local branch `feat/html-report` not pushed | `.dev-flow/BACKLOG.md` line 7 |

---

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-29-batch-01
mode: core
verdict: pass
increments: 5                 # 001–004 planned + 005, the DDR correction
source_files_max: 3           # increment 004: keymap.py, modals.py, app.py (README.md is docs)
notices_raised: 25            # V9 V13 V22 V23 V26 V27 V30 V31 V32 V36 V37 V38 V41 V42 V43 V44 V47 V48 V49 V50 V51 V52 V53 V54 V57 — declared in PLAN.md §Gate notices and runtime absences
rework_returns: 2             # P2 round 1 iterate-to-refine (D1–D20); DDR approved with conditions → back to P3 for increment 005
triggers_fired: "A1,A2,B1,B4,C4,C6,C8,D1,E1"
tests_base_to_post: "3281 -> 3332"   # +51 new nodes; TC-1902 ran and passed (0 skips)
new_control: none
open_items_next: 7            # the batch's BACKLOG section: CR5, CR3-4, CR3-5, CR4-4, N1/N2, the CLI report decision, the toast path wrap
```

**Not done, declared:** no evaluation with real users (one-person team); the real browser print dialog was not driven (print emulation only); the qa-reviewer at P4 did not open the PNGs; `dev-flow-sync` not run; nothing pushed or merged.

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` + ledger | gate `V26` (declared budget NOTICE), no block at any gate · scan flags answered in §6.3 | ❌ | `none — reviewed by three lenses at P2 (two rounds) and three at the PDR` | |
| Test cases / ATs | `04-validation.md`: 3332 passed; mutation 154/154 KILLED across `mutation-001.txt` … `mutation-005.txt` | ❌ | `none — the code-reviewers and the DDR/P4 qa lenses audited the oracles` | |
| Code | gates + `code-reviewer` OK to advance at every increment, 0 HIGH; `security-reviewer` PASS at 001–004 | ❌ | `none — the post-review fixes of 003–005 were not re-read by the code-reviewer (declared)` | |
| The reports, the captures and `review.html` | `evidence/captures/capture-log.json` 0 errors / 0 external; the WT READY checks; the DDR ux lens's seven criteria | ❌ | `none — the review page waits for the operator's judgement of the HR-3 controls before the push` | |

- **Human perimeter:** the operator owns what this flow does not cover: the push/merge decision (NOT granted — nothing is pushed), the judgement of the HR-3 controls on `review.html`, the D8 default (`o` writes all boards beside the open board), the CLI report's fate (HR-1, BACKLOG), the disposition of the backlog queue, and any evaluation with users (none exist outside the one-person team).
- **Human review ledger:** `none — every review in this batch was an independent sub-agent lens carrying the flow's role files (21 reviewer passes: 3 + 3 at P2, 3 at the PDR, 2 per increment 001–004 and 1 at 005, 2 at the DDR, 1 at P4); no human read the artifacts at a gate. The operator's first reading is review.html; the reconstruction path is the decisions_log + this record.`
