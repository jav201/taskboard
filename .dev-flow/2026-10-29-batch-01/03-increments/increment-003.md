# Increment 003 — HLR-3105 · HLR-3106 · `the deck, and the escape of board text in both reports`

> **Owed in.** `core` ✓ · `full` ✓
> **Reserved field names** (language-independent, parsed literally): `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`

| Field | Value |
|---|---|
| Batch | `2026-10-29-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `US-3101` / `HLR-3105` · `HLR-3106` / `LLR-3105.1, LLR-3105.2, LLR-3106.1, LLR-3106.2` · `LLR-3101.2` and `LLR-3101.3` (the deck arm of TC-3104) |
| Acceptance | `AT-3106` · white-box `TC-3113`, `TC-3114`, `TC-3116`, `TC-3104` (re-run over the deck) |
| Agent | `software-dev` (spawned implementer; the orchestrator ran the suites, the code-review and the security gate; this packet was written by a scribe from the records) |
| Date | `2026-10-29` |

---

## 1 · What changed

The batch's second report exists: a presentation deck, written from the same extraction dict as the workspace page. `taskboard/report_deck.py` (new) renders a cover (the scope line, totals per board, the class legend), an overview (every project on one timeline) and one slide for every non-archived project that holds at least one task, the Inbox included. Each slide is a vector gantt with real `<text>` labels, today's rule, phase-coloured bars with direct labels, milestone shapes by class, dependency arrows by task key, treatments for blocked, done, undated and archived tasks, and the project's notes with their highlights and resolved mentions. The footer prints `1 task` / `N tasks` for the non-archived tasks and `k archived` when k > 0. Paging works on the arrow keys, PageUp/PageDown, Home and End, only when focus is not in an input, textarea or select and no Ctrl/Alt/Meta key is held; there are on-screen previous/next buttons and an `n / N` counter. A second layout serves 390 px; `@media print` prints one slide per page in the light palette. Nothing in the app reaches the deck yet (the `H` key is increment 004); the surface is the file `write_reports(...)` writes, through the function-local import increment 001 already wired.

The deck reads the dict alone. The dict's frozen shape is unchanged, so the PDR is not re-opened: the only change in `report_html.py` is the VALUE of `due_word` for finished work (see below), not a field added, removed or retyped. The deck re-derives neither status nor due word.

One value change in `taskboard/report_html.py`: a done or archived task now passes `closed=True` to `report._due_word`, so finished work reads the plain distance (`-30d`), never `30d overdue`; open and late tasks pass `closed=False`. This supersedes decision D19 ("tasks never pass `closed`") and amends two requirements as `LED-2026-10-29-batch-01.25`: LLR-3101.2 (the `closed` rule) and LLR-3105.1 (the count reads `1 task` / `N tasks`, not "1 tasks").

AT-3106 is the escape acceptance test for both reports: it builds the workspace and the deck from the hostile fixture (`<script>`, `<img onerror>`, a `window.__x` sentinel, hostile project/board/person/class/phase names, `javascript:` and `data:` URLs, and a URL and a project name carrying a `"` with an `onmouseover` breakout) and asserts 0 dialogs, the sentinel untouched (also after hovering), 0 injected elements, 0 non-http(s) anchors and the hostile text visible as text. The review rounds added: the deck ignores keys held with Ctrl/Alt/Meta (CR3-2), esc-removed mutants for the gantt meta tspan, the legend and the milestone label (CR3-3), and the attribute-breakout pair (security finding SC1).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/report_deck.py` | source | HLR-3105, HLR-3106 / LLR-3105.1, LLR-3105.2, LLR-3106.1, LLR-3106.2 | NEW, 514 lines: `render(d)`; cover, overview, project slides, gantt SVG, notes, legend, `safe_href`, the paging script, the 390 px layout and the print rules |
| `taskboard/report_html.py` | source | LLR-3101.2 | `_due_word(days, closed=True)` for done and archived tasks (the value change; shape unchanged) |
| `tests/test_report_deck.py` | test | HLR-3105, HLR-3106 / TC-3113, TC-3114, TC-3116, TC-3104, AT-3106 | NEW, 6 nodes |
| `tests/test_report_html.py` | test | LLR-3101.2 / TC-3102 | literals edited for the never-late rule (see Reverse census) |
| `tests/report_fixture.py` | fixture | HLR-3106 / AT-3106 | the side board's last phase and the `secret` class name made hostile (CR3-3's M34, M35) |
| `tests/report_browser.py` | fixture | HLR-3105 | `open_page(..., ready="#tbody")`: a `ready` selector argument, so the deck page can wait on its own element (2 lines) |
| `.dev-flow/2026-10-29-batch-01/01-requirements.md`, `01-requirements-ledger.md` | doc | LLR-3101.2, LLR-3105.1 | the amendment `LED-2026-10-29-batch-01.25` |
| `.dev-flow/2026-10-29-batch-01/PLAN.md`, `.dev-flow/BACKLOG.md` | doc | — | the plan's state and Test ledger rows; CR3-4 and CR3-5 as known limits |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** (`report_deck.py` new, `report_html.py` value change) |
| Test files | 4 (uncapped; `report_fixture.py` and `report_browser.py` are support modules) |
| Doc files | 5 (outside the count) |

## 3 · How to test

```bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
cd C:/Users/jjgh8/Github/taskboard-wt/report-proto
env -u NO_COLOR python -m pytest .scratch/test_import_probe.py -s -q -p no:cacheprovider   # must print a path inside report-proto
TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q tests/test_report_deck.py tests/test_report_workspace.py tests/test_report_html.py tests/test_report.py
# the mutation battery
env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-003.py
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | none separate — the deck's pure functions (`safe_href`, the scale, the row order) are asserted through the white-box nodes below | n/a |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | `test_TC_3113_one_slide_per_project` (LLR-3105.1: slide count and titles from the fixture's literals, `1 task`/`N tasks`, `k archived`, the all-archived Inbox, the task-less project, scope-`p` dicts) · `test_TC_3104_the_deck_reads_the_dict_only` (AST walk over `report_deck.py`, determinism) · `test_TC_3114_keys_page_and_print_splits` (LLR-3105.2: real `keyboard.press`; End/Home/PageDown/ArrowRight at the last slide; keys ignored in INPUT/TEXTAREA/SELECT; Ctrl/Alt/Meta ignored; under print media every slide `break-after: page` and a real PDF of 13 pages for 13 slides) · `test_TC_3116_offline_themes_and_phone_width` (LLR-3106.2: offline, 0 console errors, 0 external requests, light and dark, 390 px with no page overflow on every slide, long and unicode titles; the edited-dict arm for `safe_href` incl. `JAVASCRIPT:` and `" javascript:"`) · `test_finished_work_is_never_late_in_either_report` (LLR-3101.2 as amended) (5, `tests/test_report_deck.py`) | 5 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | `test_AT_3106_board_text_is_escaped_in_both_reports` — writes BOTH reports with `write_reports` from the hostile fixture, opens each as `file://`, and asserts 0 dialogs, the `window.__x` sentinel untouched (before and after hovering), 0 injected elements, 0 non-http(s) anchors, the hostile text present as text, and a raw-bytes arm over the deck file | 1 passed |
| regression | `core` | `tests/test_report.py` (18) and the 52 nodes of increments 001–002 (`tests/test_report_html.py` 12, `tests/test_report_workspace.py` 22, with the TC-3102 literals edited) | green in the run below |
| increment total | — | `TASKBOARD_REQUIRE_BROWSER=1` over the four files, 0 skipped | **58 passed** in 17.40 s (`suite-003.txt`) |

AT-3101, AT-3105 and AT-3107 have no node yet (increment 004, the `H` key and the modal): their `V2` rows in the gate are station-expected, as the plan declares. AT-3106 is now on disk. The package-scanning law suites were not re-run in this increment; they re-run in increment 004 and at P4.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | 37 single-fault mutants M01–M37, each a one-line change aimed at one of this increment's OWN assertions (the list under *Mutation verdicts*); M01–M31 were written with the code, M32–M37 for the review fixes |
| Instrument | project code, mutated by the script `evidence/mutation-003.py` (anchor-checked string replacement, `finally`-restore, per-node verdicts) |
| Where it ran | this worktree, the increment tree; the harness restores the file before the next mutant |
| Transcript | `evidence/mutation-003.txt` (the last run, M01–M37 on the final bytes, is the verdict of record) |
| Restore proven by | sha256 recorded before and after every mutant (`restored, identical`); final `report_deck.py` `5f8d062cd25c1c1be01a744e53a9e603311740cb6996eb6b2155cd5de7ccd34d`, `report_html.py` `07d1d7f68a650ae123c2ff0acb023723c38f42e83f594b92d52dbde510c7b549`, `report_workspace.py` `99a97735c581126ce1cc481fc2adc1c4e81129f0672cf5baa58df27f58870f83`, the tree's bytes at commit `f7eb6d7` |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` on every run |
| Arms resolved at baseline | 37 mutants, each with its `-k` selection resolved to the named node(s) |
| Verdict granularity | per resolved node id (the transcript prints `RED nodes: [...]` for each mutant) |
| Arms that stayed GREEN | none |

| Field | Value |
|---|---|
| **RED counterfactual** | the AT's own mutations: M01–M06 (`esc` removed from the deck's SVG and HTML sinks) and M08 (`valid_url` dropped) turn `test_AT_3106_board_text_is_escaped_in_both_reports` RED; M07 (the workspace title set through `innerHTML`, PQ9) turns the same node RED; M09 (`safe_href` identity in the deck) and M10 (`safeHref` identity in the workspace, SI1) turn `test_TC_3116_offline_themes_and_phone_width` RED · transcript `evidence/mutation-003.txt` · restore digests as in the table above |

### Mutation verdicts

| Field | Value |
|---|---|
| **Mutation verdicts** | 37/37 KILLED, none survived, none BAD in the final run, per resolved node: M01–M06 `esc` removed from the deck sinks (gantt task title `:182`, note card title `:349`, slide project name `:362`, and the other title sinks) → AT-3106 (raw-bytes arm) · M07 PQ9, the workspace title via `innerHTML` → AT-3106 · M08 `valid_url` dropped → AT-3106 · M09 deck `safe_href` identity, M10 workspace `safeHref` identity (SI1) → TC-3116 · M11 `rel` dropped, M12 Google Fonts link, M13 a fixed 600 px width, M14 no light palette, M15 no narrow swap → TC-3116 · M16 archived project gets a slide, M17 task-less project gets a slide, M18 all-archived project dropped, M19 count includes archived, M20 status re-derived → TC-3113 · M21 `Home` handler dropped, M22–M23 input and textarea guards, M24 wrap at the ends, M25 print `break-after`, M26 print `display`, M27 print palette, M28 print nav hidden → TC-3114 · M29 the deck imports `views.HEX` → TC-3104 · M30 a done task passes `closed=False` → TC-3102 · M31 the same fault → the finished-work node · M32 CR3-2, modifier keys not ignored → TC-3114 · M33 `:184` esc removed from the gantt meta tspan, M34 `:279` from the legend phase, M35 `:282` from the legend class name, M36 `:195,198` from the milestone label → AT-3106 · M37 SC1, `:347` the deck writes a task URL into `href` unescaped (a quote breaks out to `onmouseover`) → AT-3106 · arms that stayed GREEN: none · transcript `evidence/mutation-003.txt` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the raw-bytes search of the deck file for the hostile payloads | M01–M06 (a sink without `esc`) | AT-3106 RED — the payload appears as markup in the saved bytes (`mutation-003.txt`) |
| the dialog / sentinel / injected-element counters on the rendered pages | M07 (title via `innerHTML`) and M37 (href breakout) | AT-3106 RED — the sentinel or an `[onmouseover]` element was found (`mutation-003.txt`) |
| the non-http(s) anchor count, incl. the edited-dict arm | M09 and M10 (`safe_href`/`safeHref` as identity) | TC-3116 RED — `javascript:`, `JAVASCRIPT:` and `" javascript:"` reached an anchor (`mutation-003.txt`) |
| the paging-key reads (`keyboard.press` and the `n / N` counter) | M21–M24, M32 | TC-3114 RED per mutant |
| the PDF page count (a real `page.pdf()` under print media) | M25 (`break-after` dropped) | TC-3114 RED — the PDF held fewer pages than slides |
| the slide-count and literal-count reads | M16–M20 | TC-3113 RED per mutant |
| the AST import walk over the deck | M29 (`views.HEX`) | TC-3104 RED |
| the due-word reads | M30, M31 (`closed=False` for done tasks) | TC-3102 and the finished-work node RED |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 8 instruments, each shown RED before its first PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the deck file written by `write_reports` — the saved bytes | `test_AT_3106_board_text_is_escaped_in_both_reports`, raw-bytes arm: the file read as text is searched for every hostile payload (`<script>`, `<img onerror>`, the quote breakout) in its unescaped form, and for the escaped form of the visible hostile names | passed (`suite-003.txt`); M01–M06, M08, M33–M37 turn it RED |
| the same file — the rendered page | `test_TC_3113_...`, `test_TC_3114_...`, `test_TC_3116_...`, AT-3106: opened as `file://` headless; slide count and titles from literals, key paging, 0 dialogs, 0 injected elements, 0 non-http(s) anchors, 0 console errors, 0 external requests, light/dark, no overflow at 390 px | passed; M07, M09–M24, M32 turn them RED |
| the printed deck — a real PDF | `test_TC_3114_keys_page_and_print_splits`: `page.pdf()` under print media; the PDF's page count equals the slide count (13 pages for 13 slides) | passed; M25–M28 turn it RED |
| the workspace file, for AT-3106 | the same dialog, sentinel and anchor counters over the workspace page built from the same hostile dict (PQ9, SI1) | passed; M07, M10 turn it RED |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifact classes (the deck file's bytes, the rendered deck page, the printed PDF) asserted in 4 forms, plus the workspace file's rendered page for AT-3106 |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-29-batch-01/evidence/suite-003.txt | 7e6ec1b0e32407d0ec3e0d60a64e04e3a7df42969c9f9404aa64af672d1b4d35 |
| mutation-003.txt | .dev-flow/2026-10-29-batch-01/evidence/mutation-003.txt | 11459f2bc7c54f3bb5b08cdc3b7423f26751d45ce6323a0855703781ac7fc98d |
| mutation-003.py | .dev-flow/2026-10-29-batch-01/evidence/mutation-003.py | 3c8eacca225edd8c6400fc760c0f7ccdbe8352203ea352703d530f1b8595562e |

| Field | Value |
|---|---|
| **Evidence files** | `3 artifact(s), each at the declared home, with the digest of its bytes on disk` |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes — "no board string reaches the deck unescaped", "no anchor carries a non-http(s) scheme" and "the deck imports nothing but `report_html`" |
| If the result is an ABSENCE, what made the search wide enough | AT-3106 searches the deck's saved bytes for the unescaped payload of every hostile field the fixture carries (project, board, person, class, phase, title, note, URL) and counts injected elements and non-http(s) anchors on the rendered page; TC-3116 feeds `javascript:`, `JAVASCRIPT:` and `" javascript:"` URLs into a copy of the dict; the import claim is the AST walk over the whole file |
| Guard labelled as protecting a CONCLUSION, not a behaviour | AT-3106 protects the conclusion "board text cannot execute or break out in either report", not one function's behaviour; M01–M06 and M33–M37 each break one sink |
| Conjunctive criteria: one mutation per conjunct | AT-3106: text sinks (M01–M06, M33–M36), URL scheme (M08, M09, M10), attribute quote (M37), workspace title (M07); TC-3114: Home (M21), input guard (M22), textarea guard (M23), wrap (M24), modifier keys (M32), print break/display/palette/nav (M25–M28) |
| Synthetic instance of the absent case | `tests/report_fixture.py` holds the hostile names (a class `Secret qzM1 <img onerror…>`, a phase `Done <img onerror…>`, hostile project/board/person names) and the `javascript:`/`data:`/quote-breakout URLs |
| **Positive control for every probe that returned an ABSENCE** | M01–M06 and M37 make the raw-bytes search find the payload, and M09/M10 make the anchor counter find a `javascript:` anchor, so each probe fires on the present case |

### Reverse census — trigger family B, and A3

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl KEYMAP tests/` · `grep -rl INVENTORY tests/` · `grep -rl open_url tests/` · `grep -rl build_report tests/` | the same hits as increments 001–002. This increment edits no `keymap.py`, `app.py`, `modals.py` and no `report.py`, so no KEYMAP/INVENTORY/`open_url` assertion can move; `tests/test_report.py` (18) is green in the 58-pass run. `git diff 613702e f7eb6d7 --stat -- taskboard tests` lists `taskboard/report_deck.py` (new), `taskboard/report_html.py`, `tests/report_browser.py`, `tests/report_fixture.py`, `tests/test_report_deck.py` (new) and `tests/test_report_html.py` — nothing else |
| B2 file moved on disk | n/a — no file moved (probe not fired, declared) | — |
| B3 byte-identical golden captures this source | `tests/goldens/` does not exist (P0 probe) | not fired |
| B4 artifact produced here is consumed elsewhere | `grep -rln "report_html\|report_workspace\|report_deck" taskboard/ tests/` | the deck is consumed by `write_reports`' function-local import (increment 001) and by the new tests; `report_html.py`'s value change is consumed by the workspace (which reads `due_word` and never re-derives it) and by `tests/test_report_html.py` and `tests/test_report_workspace.py` |
| A3 interface consumed by another module changed | the fixture and browser-helper edits, and the 001/002 tests that use them | `tests/report_fixture.py`: the side board's last phase and the `secret` class name became hostile strings; every 001 and 002 test that reads the fixture stays green, because they read counts and keys, not those two names (the 58-pass run). `tests/report_browser.py`: `open_page` gained the keyword `ready="#tbody"`, a default that equals the old hard-coded selector, so every existing caller is unchanged and green. `tests/test_report_html.py`: the TC-3102 literals moved with the never-late rule (tst1 `-30d`, tmv1 `-18d`, ttx0 `-380d` archived; tst4 stays `3d overdue`) — an edit by supersession, named in the Correction population; the node still fails if a late open task loses its `overdue` wording |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run (B1 with its hits re-validated, B3, B4, A3 with the fixture and browser-helper effect on 001/002 stated; B2 declared not fired); no `keymap.py`, `app.py`, `modals.py` or `report.py` edit |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| the due-word fix (finished work is never late; `LED .25`) | every place that computes a task's `due_word` or asserts a finished task's wording | `grep -n "_due_word" taskboard/report_html.py` · `grep -n "overdue\|due_word" tests/test_report_html.py tests/test_report_deck.py tests/test_report_workspace.py` | 1 production call site in `extract`; 4 literal sites in TC-3102 | the call site (`closed` follows the status); the TC-3102 literals; the finished-work node added; M30, M31 pin it | 0 |
| CR3-2: the deck's key handler swallowed Ctrl/Alt/Meta + arrow | every keydown handler in the deck page | `grep -n "keydown\|ctrlKey\|altKey\|metaKey" taskboard/report_deck.py` | 1 handler | 1 — returns early on a modifier key; a TC-3114 arm and M32 pin it | 0 |
| CR3-3: board strings in the deck without an esc mutant (gantt meta tspan, overview heading, legend, milestone label) | every `esc(` / `_e(` sink and every board-derived string in the deck's SVG and HTML | `grep -n "esc(\|_e(" taskboard/report_deck.py` against the mutant anchors | 4 sinks without a mutant (`:184`, `:195,198`, `:279`, `:282`) | 4 mutants added (M33–M36); M34 (legend phase) needed a hostile phase, so the fixture's phase and class name were made hostile; all 4 killed | 0 |
| SC1 (security, minor): attribute sinks `href` and `data-project` escaped with `quote=True` but no hostile value carried a `"` | every attribute sink in the deck that holds board text | `grep -n 'href=\|data-project=' taskboard/report_deck.py` | 2 (`:347`, `:375`) | AT-3106's set gained a URL and a project name with a `"` and an `onmouseover` breakout (0 `[onmouseover]` in both reports, sentinel untouched after hover); M37 pins `:347` | 0 |
| CR3-1: `mutation-001.py` M03's anchor `"due_word": _due_word(due_in),` is gone | the 001 battery's mutants anchored on the `extract` call | `grep -n "M03" .dev-flow/2026-10-29-batch-01/evidence/mutation-001.py` | 1 | none edited — committed evidence is not rewritten; 001's verdict stands on the bytes it ran against, and re-running the 001 battery now SETUP-ERRORs at M03 | M03 is superseded by M30/M31 (the fault it modelled stays caught by TC-3102); CR3-1 is recorded here, not fixed |

| Field | Value |
|---|---|
| **Correction population** | 5 corrections (the due-word fix, CR3-2, CR3-3, SC1, CR3-1), each enumerated with its method and its count; the first four edited, CR3-1 recorded as superseded |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| "tasks never pass `closed`" (D19) in LLR-3101.2 | `grep -n "never pass" .dev-flow/2026-10-29-batch-01/01-requirements.md` | yes — the live statement now gives the `closed` rule per status; the ledger keeps the before text | `01-requirements.md:311-312`; `01-requirements-ledger.md` LED .25 |
| the printed count `<n> tasks` in LLR-3105.1 | `grep -n "<n> tasks" .dev-flow/2026-10-29-batch-01/01-requirements.md` | yes for the LLR; two acceptance-test lines keep the generic `<n> tasks` as a pattern for the literal, which the LLR's `1 task` / `N tasks` governs | `01-requirements.md:185`, `:249` |
| `mutation-001.py` M03 | see CR3-1 above | yes — recorded as superseded by M30/M31 | `evidence/mutation-003.txt` M30, M31 |

### Signed-balance test ledger

`post = base − deleted + added` → `58 = 52 − 0 + 6`  ✓ reconciles: the base is increment 002's 52 (`suite-002.txt`); this increment adds 6 nodes in `tests/test_report_deck.py` (TC-3113, TC-3104, TC-3114, TC-3116, AT-3106, the finished-work node); no node deleted; the TC-3102 node was edited, not counted as added.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | code-reviewer — spawned as a generic agent with agents/code-reviewer.md · OK to advance (with notes) · no HIGH finding; the LOW fixes CR3-2 and CR3-3 were applied after the review and were NOT re-read by the code-reviewer (declared) |

Reading: 0 HIGH; the reviewer re-ran 18/18 (deck + html). Checked: R1 and D12 (slides and counts come from `status`), the paging keys ignored in INPUT/TEXTAREA/SELECT, one slide per printed page (the PDF page count equals N), the 390 px narrow chart, `esc` on every sink read, fill colour only through `_hue`, links through `safe_href` plus `rel`, the deck importing only `report_html`, and the due-word fix. Findings: CR3-1 (LOW, `mutation-001.py:36`, the stale M03 anchor) is recorded above as superseded by M30/M31; CR3-2 (LOW, the key handler swallowing Alt/Ctrl/Meta + arrow, `report_deck.py:487`) and CR3-3 (LOW, no esc mutant on the gantt meta tspans, the legend and the milestone label) were fixed in this increment; CR3-4 (LOW, the legend takes its phases from `projects[0]`, `:312`) and CR3-5 (LOW, a slide taller than a page spans pages in print, `:463`) are known limits, entered in `.dev-flow/BACKLOG.md`. Deviations the reviewer accepted: `1 task`, `render(d)` for `build_deck(data)`, the TC-3104 node importing the AST helpers from `test_report_html.py`, and the TC-3113 boards built in the test.

Security: security-reviewer at the gate — PASS (6 passed in its run; `mutation-003` 31 killed, 0 survivors at that reading; 37/37 on the final bytes). S1 is fully verified on both sides: M09 (the deck's `safe_href` as identity) and M10 (the workspace's `safeHref` as identity) are killed by TC-3116's edited-dict arm, including `JAVASCRIPT:` and `" javascript:"`; SI1 is discharged. `esc` was traced on every sink (SVG text and tspans, the legend, the cover, slide head and sub, the notes title, the link text and `href`); `_hue` emits `#rrggbb` only; class names are constants or `ph0`..`ph4`; `notes_html` is the sanctioned segment builder; no `data` element and no script is built from board text; the title and aria strings are constant; there is no `url()` but the local `#ah` arrow marker; `safe_href` requires `https?://` and adds `rel` and `target`. SC1 (minor: the attribute sinks `href` and `data-project` are escaped with `quote=True` but no hostile value carried a `"`) was discharged in this increment (the breakout pair in AT-3106, M37). The SC1 fix and the LOW fixes were applied after the security-reviewer read; M37 and the AT-3106 arm are their pin.

---

## 5 · Risks

- **CR3-4 (known limit):** the deck's class legend takes its phases from the first project; a later project with other phase names has bars the legend does not name (each bar is also labelled directly). In `BACKLOG.md`.
- **CR3-5 (known limit):** a slide taller than a page spans pages in print; the PDF page count equals N only for slides that fit. In `BACKLOG.md`.
- **Browser tests do not run in CI:** Playwright is not a declared dependency; this machine's transcripts (`suite-003.txt`, `mutation-003.txt`) are the evidence of record.
- **The 001 battery no longer re-runs clean:** `mutation-001.py` M03 SETUP-ERRORs on the current `report_html.py` (CR3-1); 001's verdict stands on the bytes it ran against and M30/M31 carry the fault now.
- **The LOW fixes and the SC1 fix were not re-read by a reviewer** (declared in §4b); their pin is mutants M32–M37 and the AT-3106 arm.
- **The mutation harness anchors on source text:** a later edit to those lines makes a mutant `SETUP-ERROR`; the harness reports it rather than passing.
- **The deck's print check is a real PDF page count, not a visual comparison** of the slides against the screen.

## 6 · Pending items / spec deviations

- **Deviation, singular count:** `1 task` for one, `N tasks` otherwise (as CR1 did for the workspace); amended in `LED .25`.
- **Deviation, the entry point is `render(d)`**, not `build_deck(data)` as the brief said; it matches `report_workspace.render` and the contract's own name (LLR-3105.1).
- **Deviation, TC-3104** imports its AST helpers from `tests/test_report_html.py` instead of copying them.
- **Deviation, TC-3113** builds the all-archived Inbox and the empty-board cases in the test rather than in the shared fixture.
- **Deviation, `open_page(..., ready=...)`** in `tests/report_browser.py` (2 lines).
- **Requirement amendment:** the `closed` rule and the count wording → LLR-3101.2 and LLR-3105.1, `LED-2026-10-29-batch-01.25`. The frozen dict shape is unchanged, so the PDR is not re-opened.
- **Increment-003-owned conditions, all discharged:** PQ9 (M07), Q11 (the `window.__x` sentinel, hostile names as text), SI1 (M10, edited-dict arm), R1 (the slide rule), R7 (TC-3104 over the deck), D12 (`k archived`), D17 deck arms (390 px light and dark on every slide, long and unicode titles, the all-archived project, the Inbox), D1 (links only http(s), re-checked).
- **Carried:** CR3-4 and CR3-5 in `BACKLOG.md`; CR5 (the Inbox key collision) from increment 001.

## 7 · Suggested next task

Increment 004: the `H` key, the modal and the `app`/`keymap` wiring that reach `write_reports` (AT-3101, AT-3105, AT-3107; conditions C8, C9 and the PU3 operator question); the package-scanning law suites re-run there.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 2 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 6 new nodes in `tests/test_report_deck.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | §4: no unit is separate from its TC node |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4: M01–M08 for AT-3106, M09/M10 for TC-3116 · `evidence/mutation-003.txt` · restore digests |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4: 5 probes; the fixture and browser-helper edits named, 001/002 green |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b: OK to advance with notes, 0 HIGH; the LOW fixes not re-read (declared) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | the dict's SHAPE is unchanged (`report_html.py` changes one value); `report.py`, `views.py`, `people.py`, `models.py`, `report_workspace.py` unchanged by this increment |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | `suite-003.txt` (58 passed), `mutation-003.txt` (37 KILLED); digests in the evidence rows |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 table with positive controls |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | §4: 37 mutants, per-node verdicts, none green |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4: 8 instruments |
| 13 | **Correction population** declared | all | ✓ | §4: 5 corrections with methods |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4: the deck bytes, the rendered page, the printed PDF |
| 15 | **Independent review** names somebody | all | ✓ | §4b: code-reviewer and security-reviewer |
| 16 | **Evidence files** declared | all | ✓ | §4: rows written by `devflow-evidence.py` |
