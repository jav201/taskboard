# Requirements ledger — taskboard — Batch 2026-10-29-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._

_P1, 2026-10-29: the live contract is born at v1 (US-3101, HLR-3101..HLR-3107, 18 LLRs), every requirement declaring `**Ledger:** none`. The first amendment — a P2 fold, a PDR condition or a P3 drift — writes the first entry below._


### LED-2026-10-29-batch-01.1 — task URLs restricted to http(s) (S1 HIGH)
- **Requirement:** LLR-3101.1, HLR-3106, LLR-3106.2
- **Date:** 2026-10-29
- **What changed:** before — Task URLs reached `href` unrestricted (`a.href = u` in the prototype): a `javascript:`/`data:`/`file:` URL in a board file was stored XSS in both reports. After — `extract` keeps only `views.valid_url` results; the page re-checks `^https?://` before any `href`; links carry `rel="noopener noreferrer"`; AT-3106 gains `javascript:` and `data:` URL arms (0 non-http(s) anchors in both reports); new TC-3124 (increment 001); §2.7 row 10; §6.3 C8 bullet.
- **Why:** P2 round 1, finding(s) S1 (security-reviewer, blocker HIGH); the orchestrator's disposition D1 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `evidence/p1-probes-iter2.txt` probe 9 (`valid_url` drops `javascript:`, `data:`, `file:`, `vbscript:`)
- **Parent HLR re-read:** amended here and re-read: HLR-3106; HLR-3101 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3101.1 (`01-requirements.md:299`), HLR-3106 (`01-requirements.md:258`), LLR-3106.2 (`01-requirements.md:440`).
- **Owning increment:** 001 (extract, workspace), 003 (deck).

### LED-2026-10-29-batch-01.2 — the download's leak surface: no board text outside the data element
- **Requirement:** LLR-3102.1, LLR-3102.3, HLR-3103, LLR-3103.1, LLR-3103.2
- **Date:** 2026-10-29
- **What changed:** before — The download's byte check covered only project X's names and titles; the shell, `meta.view`, the summary and the hash `p` could carry hidden names, keys or URLs. After — HLR-3103: the shell holds no board-derived text outside `<script id="board-data">`; the byte search covers every dropped project/board/person/class name, task title, task URL and key/id by unique tokens, raw and JSON-escaped. LLR-3102.1: every board-text control is built client-side from the data. LLR-3102.3: hash `p` lists the CHECKED keys. LLR-3103.1: `meta.view` and the summary name only kept items. LLR-3103.2: the pristine shell holds no board text.
- **Why:** P2 round 1, finding(s) S2, Q5, A4; the orchestrator's disposition D2 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** the round's shell (`prototypes/html_report/variant_b/build.py`) renders project options server-side; `taskboard/boards.py:449-453` (ids are slugs of names)
- **Parent HLR re-read:** amended here and re-read: HLR-3103; HLR-3102 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3102.1 (`01-requirements.md:329`), LLR-3102.3 (`01-requirements.md:360`), HLR-3103 (`01-requirements.md:210`), LLR-3103.1 (`01-requirements.md:370`), LLR-3103.2 (`01-requirements.md:380`).
- **Owning increment:** 002 (test arms).

### LED-2026-10-29-batch-01.3 — the download composes the file without `String.replace` patterns
- **Requirement:** LLR-3103.1, LLR-3103.2
- **Date:** 2026-10-29
- **What changed:** before — `String.replace(shell, marker, json)` interprets `$&`/`$'` in board text and re-inserts the full block. After — LLR-3103.2: a function replacer or a DOM build; LLR-3103.1: a fixture title with `$&` and `$'` keeps the kept set exact; LLR-3103.2's negative control names the replace mutation.
- **Why:** P2 round 1, finding(s) S3; the orchestrator's disposition D3 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** JavaScript `String.prototype.replace` pattern semantics (`$&`, `$'`)
- **Parent HLR re-read:** HLR-3103 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3103.1 (`01-requirements.md:370`), LLR-3103.2 (`01-requirements.md:380`).
- **Owning increment:** 002.

### LED-2026-10-29-batch-01.4 — exactly one `innerHTML` exception: `notes_html`
- **Requirement:** LLR-3106.1
- **Date:** 2026-10-29
- **What changed:** before — "Never `innerHTML`" contradicted the server-built `notes_html` the page inserts. After — LLR-3106.1: the one exception is a kept task's `notes_html`, into the task card's notes and the notes section only.
- **Why:** P2 round 1, finding(s) S4; the orchestrator's disposition D4 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `prototypes/html_report/variant_b/build.py:479` (`#m-notes` innerHTML)
- **Parent HLR re-read:** HLR-3106 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3106.1 (`01-requirements.md:430`).
- **Owning increment:** 001.

### LED-2026-10-29-batch-01.5 — `meta.view` restored through the hash whitelists
- **Requirement:** LLR-3103.2
- **Date:** 2026-10-29
- **What changed:** before — Restoring a downloaded file's `meta.view` bypassed `parseHash`'s whitelists. After — LLR-3103.2: restore through the same `parseHash` whitelists; threshold arm: an edited `meta.view` with an unknown key is dropped.
- **Why:** P2 round 1, finding(s) S5; the orchestrator's disposition D5 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** LLR-3102.3 (the whitelist grammar)
- **Parent HLR re-read:** HLR-3103 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3103.2 (`01-requirements.md:380`).
- **Owning increment:** 002.

### LED-2026-10-29-batch-01.6 — keys, not text, between tasks; the dict's full fact list; the IFC's `write_reports` input
- **Requirement:** LLR-3101.1, LLR-3103.1, LLR-3107.3
- **Date:** 2026-10-29
- **What changed:** before — A task carried other tasks' titles in `deps` and `chain` was undefined; the deck's facts, the `boards` shape and the unlisted board's id were missing; the IFC gave `write_reports` rendered pages as input. After — LLR-3101.1: `deps`/`chain` are task KEYS, titles resolved client-side; the dict lists every fact both renderers need; `boards` = `[{key, name, colour}]`, an unlisted board keyed `#<position>`. LLR-3103.1: dropped keys removed. LLR-3107.3 and the IFC: `write_reports` takes the dict and calls the renderers.
- **Why:** P2 round 1, finding(s) S6, A6; the orchestrator's disposition D6 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `prototypes/html_report/variant_b/build.py:100-125`; `taskboard/app.py:841-871` (`board_lanes`: unlisted board id None)
- **Parent HLR re-read:** HLR-3101, HLR-3103, HLR-3107 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3101.1 (`01-requirements.md:299`), LLR-3103.1 (`01-requirements.md:370`), LLR-3107.3 (`01-requirements.md:470`).
- **Owning increment:** 001.

### LED-2026-10-29-batch-01.7 — the round's CSV/JSON downloads kept, visible rows only, formula guard (new LLR-3103.3)
- **Requirement:** HLR-3103, LLR-3103.3
- **Date:** 2026-10-29
- **What changed:** before — HR-1 names B's CSV/JSON downloads; the contract did not trace them, and the round's version leaks dependency titles and notes and carries CSV formula injection under a false label. After — New LLR-3103.3 (TC-3122, increment 002); HLR-3103's statement names it; the IFC gains its node.
- **Why:** P2 round 1, finding(s) S7, A1; the orchestrator's disposition D7 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `.dev-flow/COMMISSION-html-report.md:36`; `prototypes/html_report/variant_b/build.py:562-600`
- **Parent HLR re-read:** amended here and re-read: HLR-3103.
- **Body edit landed:** HLR-3103 (`01-requirements.md:210`), LLR-3103.3 (`01-requirements.md:390`).
- **Owning increment:** 002.

### LED-2026-10-29-batch-01.8 — scope default stays `o`: an accepted risk with two controls
- **Requirement:** LLR-3102.1, LLR-3105.1, HLR-3107, LLR-3107.2
- **Date:** 2026-10-29
- **What changed:** before — Scope `o` writes every loaded board's data beside the open board, possibly a client's folder. After — The default stays `o` (HR-2) and the destination stays `<board dir>/reports/`, declared in §6.3 as an accepted risk; controls: (a) the modal prints the destination folder and the board count before any key writes (HLR-3107, LLR-3107.2); (b) both reports' header states the scope (LLR-3102.1, LLR-3105.1). The operator may revisit it on the review page.
- **Why:** P2 round 1, finding(s) S8, A5; the orchestrator's disposition D8 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `taskboard/boards.py:399-410` (board folders)
- **Parent HLR re-read:** amended here and re-read: HLR-3107; HLR-3102, HLR-3105 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3102.1 (`01-requirements.md:329`), LLR-3105.1 (`01-requirements.md:410`), HLR-3107 (`01-requirements.md:274`), LLR-3107.2 (`01-requirements.md:460`).
- **Owning increment:** 001, 003, 004.

### LED-2026-10-29-batch-01.9 — the `o` opener's safety stated on its real ground
- **Requirement:** LLR-3107.4
- **Date:** 2026-10-29
- **What changed:** before — §6.3 leaned on the image opener's gates, which do not apply to the report path. After — LLR-3107.4: only a path this export wrote inside `<board dir>/reports/`; §6.3 reworded; TC-3120 asserts the opened path is inside `reports/`.
- **Why:** P2 round 1, finding(s) S9; the orchestrator's disposition D9 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `taskboard/app.py:3554-3565`; `evidence/p1-probes-iter2.txt` probe 11 (the slug alphabet)
- **Parent HLR re-read:** HLR-3107 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3107.4 (`01-requirements.md:480`).
- **Owning increment:** 004.

### LED-2026-10-29-batch-01.10 — AT-3107 made black-box; the INVENTORY row is a TC
- **Requirement:** HLR-3107, LLR-3107.2
- **Date:** 2026-10-29
- **What changed:** before — "Contains `b c a p o esc`" was vacuous; the modal-key law checks painted keys only for Button modals, so AT-3107 asserted no effect. After — HLR-3107's threshold: press `H`, read the painted key line by pattern (`b workspace`, `c deck`, `a both`, `p <project>`, `o all boards`, `esc close`), press each key and assert its effect. LLR-3107.2: the key-line words; TC-3118 carries the `INVENTORY` row `{}`.
- **Why:** P2 round 1, finding(s) Q1, Q2; the orchestrator's disposition D10 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `tests/test_modal_keys.py:324-335`
- **Parent HLR re-read:** amended here and re-read: HLR-3107.
- **Body edit landed:** HLR-3107 (`01-requirements.md:274`), LLR-3107.2 (`01-requirements.md:460`).
- **Owning increment:** 004 (test side).

### LED-2026-10-29-batch-01.11 — TC-3105's Tab oracle is hand-enumerated
- **Requirement:** LLR-3102.1
- **Date:** 2026-10-29
- **What changed:** before — The Tab-reach oracle used the page's own selector, the set it was checking. After — LLR-3102.1's threshold: a control list derived from the fixture's literal counts.
- **Why:** P2 round 1, finding(s) Q3; the orchestrator's disposition D11 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** —
- **Parent HLR re-read:** HLR-3102 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3102.1 (`01-requirements.md:329`).
- **Owning increment:** 001.

### LED-2026-10-29-batch-01.12 — the deck's per-slide count, and the agreement threshold, defined
- **Requirement:** HLR-3101, HLR-3105, LLR-3105.1
- **Date:** 2026-10-29
- **What changed:** before — The deck's task-count observable was undeclared and whether archived tasks count was ambiguous. After — LLR-3105.1: each slide prints `<n> tasks` (non-archived, open and done) and `<k> archived` when k > 0. HLR-3101: per project, the slide's n == the workspace's non-archived count (archived chip off), fixture literals. HLR-3105: literal counts.
- **Why:** P2 round 1, finding(s) Q4, A7; the orchestrator's disposition D12 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `prototypes/html_report/variant_c/build.py:496-500`, `:780`
- **Parent HLR re-read:** amended here and re-read: HLR-3101, HLR-3105.
- **Body edit landed:** HLR-3101 (`01-requirements.md:178`), HLR-3105 (`01-requirements.md:242`), LLR-3105.1 (`01-requirements.md:410`).
- **Owning increment:** 004 (literals).

### LED-2026-10-29-batch-01.13 — the duplicate check compares multisets
- **Requirement:** LLR-3103.2
- **Date:** 2026-10-29
- **What changed:** before — The re-opened file's negative control compared sets, which collapse duplicates. After — LLR-3103.2's threshold and negative control: row multisets (counts per id).
- **Why:** P2 round 1, finding(s) Q6; the orchestrator's disposition D13 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** —
- **Parent HLR re-read:** HLR-3103 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3103.2 (`01-requirements.md:380`).
- **Owning increment:** 002.

### LED-2026-10-29-batch-01.14 — the print arm made reachable: explicit `beforeprint`, computed styles
- **Requirement:** HLR-3104, LLR-3104.1
- **Date:** 2026-10-29
- **What changed:** before — `beforeprint` never fires under `emulate_media`; `break-inside` was not read under print; the card and the tooltip were never opened before the arm. After — HLR-3104 and LLR-3104.1: one print function called by `beforeprint` and the control; the arm dispatches `beforeprint`, opens the card and the tooltip, and reads `getComputedStyle` under print media.
- **Why:** P2 round 1, finding(s) Q7; the orchestrator's disposition D14 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** Playwright `emulate_media` emulates the media type only (no print event)
- **Parent HLR re-read:** amended here and re-read: HLR-3104.
- **Body edit landed:** HLR-3104 (`01-requirements.md:226`), LLR-3104.1 (`01-requirements.md:400`).
- **Owning increment:** 002.

### LED-2026-10-29-batch-01.15 — no browser skip on this machine
- **Requirement:** HLR-3102, HLR-3103, HLR-3104, HLR-3105, HLR-3106, HLR-3107
- **Date:** 2026-10-29
- **What changed:** before — `importorskip` contradicted §5.2's single accepted skip TC-1902. After — §5.1: `TASKBOARD_REQUIRE_BROWSER=1` turns a missing Playwright into a failure; P4 sets it; §5.2 counts the new nodes by `--collect-only`; each browser-bearing HLR's Executed verification says so.
- **Why:** P2 round 1, finding(s) Q8; the orchestrator's disposition D15 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `evidence/p1-probes.txt` probe 7 (Playwright 1.62.0 here, absent from requirements)
- **Parent HLR re-read:** amended here and re-read: HLR-3102, HLR-3103, HLR-3104, HLR-3105, HLR-3106, HLR-3107.
- **Body edit landed:** HLR-3102 (`01-requirements.md:194`), HLR-3103 (`01-requirements.md:210`), HLR-3104 (`01-requirements.md:226`), HLR-3105 (`01-requirements.md:242`), HLR-3106 (`01-requirements.md:258`), HLR-3107 (`01-requirements.md:274`).
- **Owning increment:** 001–004.

### LED-2026-10-29-batch-01.16 — the `o` offer's clock seam named
- **Requirement:** LLR-3107.4
- **Date:** 2026-10-29
- **What changed:** before — The 10 s offer had no named clock to replace, and the toast was read off the screen. After — LLR-3107.4: `TaskboardApp._report_clock` (`time.monotonic`); TC-3120 reads the notification record and patches `os.startfile` with `raising=False`.
- **Why:** P2 round 1, finding(s) Q14; the orchestrator's disposition D16 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** —
- **Parent HLR re-read:** HLR-3107 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3107.4 (`01-requirements.md:480`).
- **Owning increment:** 004 (test side).

### LED-2026-10-29-batch-01.17 — the missing boundary arms
- **Requirement:** HLR-3102, LLR-3102.2, HLR-3105, LLR-3105.1, HLR-3106, LLR-3106.2
- **Date:** 2026-10-29
- **What changed:** before — Unicode and long titles at 390 px, all status chips off, `from == due`/`to == start`, and scope `p` on an all-archived project were not in the catalogs. After — HLR-3102, LLR-3102.2 (status off, edge dates), HLR-3105, LLR-3105.1 (`0 tasks · k archived`), HLR-3106, LLR-3106.2 (120-character and Unicode titles at 390 px).
- **Why:** P2 round 1, finding(s) Q15; the orchestrator's disposition D17 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** —
- **Parent HLR re-read:** amended here and re-read: HLR-3102, HLR-3105, HLR-3106.
- **Body edit landed:** HLR-3102 (`01-requirements.md:194`), LLR-3102.2 (`01-requirements.md:339`), HLR-3105 (`01-requirements.md:242`), LLR-3105.1 (`01-requirements.md:410`), HLR-3106 (`01-requirements.md:258`), LLR-3106.2 (`01-requirements.md:440`).
- **Owning increment:** 001–003.

### LED-2026-10-29-batch-01.18 — the Inbox defined
- **Requirement:** LLR-3101.1, LLR-3102.1, LLR-3103.1, LLR-3105.1
- **Date:** 2026-10-29
- **What changed:** before — Project-less tasks had no key, filter entry, slide rule, download rule or fixture row. After — §1.3 and LLR-3101.1: key `<board key>:inbox`, name `Inbox`, hue `dim`; LLR-3102.1: listed per board; LLR-3105.1: a slide only with a non-archived task; LLR-3103.1: reduced like any project; §5.1: the fixture holds one project-less task; §2.7 row 11.
- **Why:** P2 round 1, finding(s) A2; the orchestrator's disposition D18 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `taskboard/views.py:987-990` (the Inbox lane); `taskboard/models.py:871`
- **Parent HLR re-read:** HLR-3101, HLR-3102, HLR-3103, HLR-3105 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3101.1 (`01-requirements.md:299`), LLR-3102.1 (`01-requirements.md:329`), LLR-3103.1 (`01-requirements.md:370`), LLR-3105.1 (`01-requirements.md:410`).
- **Owning increment:** 001, 003.

### LED-2026-10-29-batch-01.19 — ONE status rule, server-side
- **Requirement:** LLR-3101.1, LLR-3101.2, LLR-3102.2, LLR-3105.1
- **Date:** 2026-10-29
- **What changed:** before — The `late` rule disagreed between `report.py`, `views.py` and the page; the JS re-derived it while the deck derived it server-side. After — §1.3 and LLR-3101.1: `extract` emits `status` (archived > done > late > open); LLR-3101.2: `due_word` = `report._due_word(days)`, never `closed`; LLR-3102.2 and LLR-3105.1 read the fields, never re-derive; new TC-3125 (increment 001).
- **Why:** P2 round 1, finding(s) A3; the orchestrator's disposition D19 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `taskboard/report.py:204`, `:217`; `taskboard/views.py:950`
- **Parent HLR re-read:** HLR-3101, HLR-3102, HLR-3105 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3101.1 (`01-requirements.md:299`), LLR-3101.2 (`01-requirements.md:309`), LLR-3102.2 (`01-requirements.md:339`), LLR-3105.1 (`01-requirements.md:410`).
- **Owning increment:** 001.

### LED-2026-10-29-batch-01.20 — project-scope file names carry the board slug; the slug pinned
- **Requirement:** LLR-3107.3
- **Date:** 2026-10-29
- **What changed:** before — Same-named projects on two boards collided in the file name; the copied slug rule was unpinned; the interface map lacked `board_lanes`' new consumer and the consumed helpers; the fixture's project shared a board's name. After — LLR-3107.3: `workspace-<board slug>-<project slug>-<date>.html`, `report_html.slug` pinned against `report.report_path` (new TC-3123, increment 001); the fixture's project is `Storefront relaunch` on board `Client A`; `docs/ARCHITECTURE.md` §4 gains the rows; §2.7 row 12.
- **Why:** P2 round 1, finding(s) A9, Q13; the orchestrator's disposition D20 (`02-review.md` §Findings round 1). Folded by iterate-to-refine, P1 iteration 1.
- **Evidence:** `taskboard/report.py:265-271`; `evidence/p1-probes-iter2.txt` probe 11
- **Parent HLR re-read:** HLR-3107 re-read — no change required (the HLR states the outcome; the LLR binds the mechanism).
- **Body edit landed:** LLR-3107.3 (`01-requirements.md:470`).
- **Owning increment:** 001, 004.

### LED-2026-10-29-batch-01.21 — wording folds, the P2 round-2 residue (R1–R7)
- **Requirement:** LLR-3101.3, LLR-3102.2, LLR-3103.1, LLR-3103.3, HLR-3105, LLR-3105.1
- **Date:** 2026-10-29
- **What changed:** R1 (qa N1, architect AN1, AN4) — before: HLR-3105 said "one slide per non-archived project" while LLR-3105.1 said "that has a task (the Inbox only when it has a non-archived task)", so an all-archived project got a slide and an all-archived Inbox did not, with no rationale. After: ONE rule — a slide for every non-archived project in scope, the Inbox included, holding at least one task of any status; an all-archived one reads `0 tasks · k archived` (HLR-3105, LLR-3105.1, TC-3113). R2 (qa N2) — the CSV's `'` prefix applies to a `-3d` due-word cell on purpose, asserted by TC-3122 (LLR-3103.3). R3 (security SN1) — the download also reduces `meta`'s scope board names and the header's board count and names to the kept boards (LLR-3103.1). R4 (security SN2) — §6.3's "Not fired" bullet no longer calls task URLs inert links; they are filtered to http/https (§6.3, `01-requirements.md:669`). R5 (architect AN2) — LLR-3102.2's negative control is restated as the page's status-chip mapping `late` → `open`, since status is now emitted server-side (LED .19). R6 (architect AN3) — `docs/ARCHITECTURE.md` §3's `report_html` row lists `views.valid_url` (`taskboard/views.py:273`). R7 (architect A8, qa Q12) — LLR-3101.3's import probe is an AST walk with precise allow/ban lists (renderers: only `report_html`; `report_html`: no `app`, `modals`, `keymap`, `boards`, `team_sync`, from `report` only `_e`/`_due_word`), TC-3104 moves to `tests/test_report_html.py` at increment 001 and is re-run at 003 with the deck.
- **Why:** P2 round 2 — all three lenses approve; their residue minors are ruled by the orchestrator's dispositions R1–R7 as wording folds, reviewed by the PDR lenses with the design proposal.
- **Evidence:** `02-review.md` §Findings (round 2); `taskboard/views.py:273` (`valid_url`); `taskboard/report.py:78`, `:85` (`_e`, `_due_word`).
- **Parent HLR re-read:** amended here and re-read: HLR-3105; HLR-3101, HLR-3102, HLR-3103 re-read — no change required (each states the outcome; the LLRs bind the mechanism).
- **Body edit landed:** LLR-3101.3 (`01-requirements.md:319`), LLR-3102.2 (`01-requirements.md:339`), LLR-3103.1 (`01-requirements.md:370`), LLR-3103.3 (`01-requirements.md:390`), HLR-3105 (`01-requirements.md:242`), LLR-3105.1 (`01-requirements.md:410`); §6.3 (`01-requirements.md:669`); `docs/ARCHITECTURE.md` §3.
- **Owning increment:** 001 (R5, R7), 002 (R2, R3), 003 (R1, R7's re-run).

### LED-2026-10-29-batch-01.22 — PDR conditions (C1–C14)
- **Requirement:** LLR-3101.1, LLR-3101.3, LLR-3102.1, LLR-3103.1, LLR-3103.2, LLR-3103.3, LLR-3104.1, LLR-3107.2, LLR-3107.4
- **Date:** 2026-10-29
- **What changed:** before — LLR-3101.1 left nine facts both renderers read unnamed (the open item P-1) and the design listed `closed`/`inbox`; `notes_text` survived a notes-off download; `write_reports` was drawn with `importlib.import_module`; `project=` was unspecified; the export captions did not name their object; print carried the browser's header/footer; the `o` offer was re-armable and unlabelled; the modal named no boards; the filter count had no unit; the CSV guard prefixed plain negative numbers. After — C1 (PA1): LLR-3101.1 admits `v`, `tasks[].board`/`priority`/`due_in`/`age`/`notes_text`, `projects[].id`/`high`, `people[].role` and drops `closed`/`inbox` (also `docs/ARCHITECTURE.md` §4, design proposal §3.1). C2 (PA2): LLR-3103.1 strips `notes_text` with `notes_html`. C3 (PA6): design proposal §4 freezes `views.HEX`. C4 (PA3): plain function-local `from . import` per renderer, no `importlib` (LLR-3101.3, design proposal §3.2, `docs/ARCHITECTURE.md` §3). C5 (PA4): `project` is the key `<board key>:<project id>` (LLR-3101.3, §3.2). C6 (PU1): the captions of LLR-3103.2 (Print, Download) and LLR-3103.3 (CSV/JSON, "visible rows only"), visible next to the control at 1366 and 390 px. C7 (PU2): LLR-3104.1 `@page { margin: 0 }` and kept-tasks-only printed counts. C8 (PU4): LLR-3107.4 single-use offer, main screen only, toast `… — o opens it (10 s)`. C9 (PU3): LLR-3107.2 names the folder and the board names. C10 (PU5): LLR-3102.1 the count's unit (filter kinds; sections and zoom excluded) and label "N filters active". C11 (PU6): LLR-3102.1 count and Reset in the first viewport at 390 px. C12 (PU7): LLR-3102.1 a pressed chip differs by more than hue. C13 (PQ1): LLR-3103.3 the guard excepts a plain number (`due_in` = `-1`), one mutation per prefix class. C14 (PQ3): LLR-3104.1 / TC-3112 print width at a 794 px viewport, RED with the `min-width:0!important` rule dropped.
- **Why:** PDR 2026-10-29 — architect (PA1–PA7), qa-reviewer (PQ1–PQ12) and ux-reviewer (PU1–PU7) all `approved with conditions`; the orchestrator's dispositions C1–C14 (`design/PDR-2026-10-29-batch-01.md`). The increment-owned conditions change no contract text and are listed in the PDR record.
- **Evidence:** `design/PDR-2026-10-29-batch-01.md`; `taskboard/views.py:273` (`valid_url`); `prototypes/html_report/variant_c/build.py:186`, `:198`, `:524` (the deck reads priority, age, high).
- **Parent HLR re-read:** HLR-3101, HLR-3102, HLR-3103, HLR-3104, HLR-3107 re-read — no change required (each states the outcome; the LLRs bind the mechanism).
- **Body edit landed:** LLR-3101.1 (`01-requirements.md:299`), LLR-3101.3 (`01-requirements.md:319`), LLR-3102.1 (`01-requirements.md:329`), LLR-3103.1 (`01-requirements.md:370`), LLR-3103.2 (`01-requirements.md:380`), LLR-3103.3 (`01-requirements.md:390`), LLR-3104.1 (`01-requirements.md:400`), LLR-3107.2 (`01-requirements.md:460`), LLR-3107.4 (`01-requirements.md:480`); `docs/ARCHITECTURE.md` §3 and §4; `design/design-proposal.md` §3.1, §3.2, §4.
- **Owning increment:** 001 (C1, C4, C5, C10–C12 and the LLR-3101.3 arms), 002 (C2 verification, C6, C7, C13, C14), 003 (the deck reads the admitted facts), 004 (C8, C9).

### LED-2026-10-29-batch-01.23 — the active count's wording is correct English (CR1)
- **Requirement:** LLR-3102.1
- **Date:** 2026-10-29
- **What changed:** before — LLR-3102.1 (via LED .22, C10) pinned the label as "N filters active" ("0 filters active" at default), which reads "1 filters active" for one active filter kind. After — the count reads `0 filters active`, `1 filter active`, `N filters active` (N ≥ 2): the singular for exactly one. Deleted: the single pinned form "N filters active". New: the three-form label. The count's unit (filter kinds) and the exclusion of sections and zoom stand unchanged. Increment 001 implemented the singular and its tests assert all three forms.
- **Why:** increment 001's code-review finding CR1 (MEDIUM, `taskboard/report_workspace.py:382`): the implementation wrote correct English and the contract's one-form wording did not; the orchestrator's disposition is to keep the singular and amend the wording rather than ship "1 filters active".
- **Evidence:** `.scratch/p3/cr-001.md` CR1; `tests/test_report_workspace.py` (the count asserted at lines 127, 244, 320, 331, 336, 363); `evidence/suite-001.txt`.
- **Parent HLR re-read:** HLR-3102 re-read — no change required (it states the outcome, controls with a counted, visible state; the LLR binds the label). TC-3105, TC-3108 and AT-3102 re-derived: each asserts the three-form label through the shipped page; no new node.
- **Body edit landed:** LLR-3102.1 `Statement` and `Numeric pass threshold` (`01-requirements.md:332`, `:335`) and its `Ledger:` field (`01-requirements.md:331`).
- **Owning increment:** 001.

### LED-2026-10-29-batch-01.24 — the download keeps no derived project facts and no mentions of withheld notes (SD1, CR2-1)
- **Requirement:** LLR-3103.1
- **Date:** 2026-10-29
- **What changed:** before — LLR-3103.1 stripped `notes_html` and `notes_text` when the notes section is off but said nothing of the mentions, so the People chips and directory and the CSV/JSON mentions column still named who was mentioned in the withheld notes; and a kept project's `open`/`late`/`done`/`high`/`worst`/`momentum` were silent, so the first implementation re-derived them client-side over the kept tasks (a second engine of `views.sitting`/`lane_facts` that nothing reads). After — with the notes section off the download drops the mentions unless a person filter is active, and then only the pressed people's; `people` reduce to those still referenced; the CSV and JSON follow. A kept project's `momentum` and `worst` are null; its open, late, done and high counts are plain counts over the kept tasks. New: the mention rule and the null facts. Deleted: nothing.
- **Why:** increment 002's security-reviewer finding SD1 (minor: a withheld note's mentions revealed who is named in it) and the code-reviewer's CR2-1 (MEDIUM: `keptFacts` was a second client-side engine with no consumer); the orchestrator's dispositions, under the batch's standing authorization, fixed both in code and amend the contract so it names what the code does.
- **Evidence:** `.scratch/p3/sec-002.md` SD1; `.scratch/p3/cr-002.md` CR2-1; `evidence/suite-002.txt` (52 passed); `evidence/mutation-002.txt` M30..M37 (40/40 killed); `tests/test_report_workspace.py::test_TC_3110_notes_off_strips_the_notes` and `::test_TC_3109_the_download_keeps_only_used_entries`.
- **Parent HLR re-read:** HLR-3103 re-read — no change required (it states the outcome: only the kept tasks and what they use leave the file; the LLR binds the mechanism).
- **Body edit landed:** LLR-3103.1 `Ledger:`, `Statement` and `Numeric pass threshold` (`01-requirements.md:372`, `:373`, `:376`).
- **Owning increment:** 002.
