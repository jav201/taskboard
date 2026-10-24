# Requirements ledger — taskboard — Batch 2026-10-24-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-24-batch-01.1 — the marks directory (P1)
- **Requirement:** HLR-2601
- **Date:** 2026-10-24
- **What changed:** new requirement: one directory of milestone classes (`id`, `name`, `shape`, `colour`, `hidden:false`) for every board at `~/.taskboard/marks.json` beside `people.json`; the id a slug of the name, stable on rename; read at start never raising (missing/blank → empty; unreadable → empty after `keep_aside` at `marks.json.corrupt` + one notice); written only on add/edit/hide, atomically under `marks.json.lock`, read-modify-write; starts empty (MM-D4). Declares AT-2601 (the commission's AT-a) with it.
- **Why:** the operator's commission and the round's verdict (`01-requirements.md` §1.4), MM-D2 and MM-D4.
- **Evidence:** P-3 (`evidence/premises.txt` — the `people.py` pattern at people.py:27-30,119-134,187,198,248); `evidence/scan-p1.txt`; `prototypes/milestone_marks/proto.py`.

### LED-2026-10-24-batch-01.2 — the task field (P1)
- **Requirement:** HLR-2602
- **Date:** 2026-10-24
- **What changed:** new requirement: `Task.mark: str | None`, the class id, meaningful only on a milestone; written only when set (the `show_in_present` pattern, models.py:1045-1053); unknown ids render unclassified and are never dropped; unticking `milestone` keeps the field; team sync travels it unchanged, the directory never. Declares AT-2607 (AT-g) with it.
- **Why:** MM-D3 and its teammate consequence.
- **Evidence:** models.py:1045-1053 read at draft; team_sync.py:143-157; P-2.

### LED-2026-10-24-batch-01.3 — the store's safety (P1)
- **Requirement:** HLR-2603
- **Date:** 2026-10-24
- **What changed:** new requirement: every write a read-modify-write under `boards.file_lock`, atomic via `models.write_atomic`; an unparseable file kept aside, never written over when it cannot be copied aside; two windows each add a class and both survive; a failed write changes nothing in memory. Declares AT-2602 (AT-c) with it.
- **Why:** MM-D2's «written exactly like people.py's Directory»; the commission's AT-c.
- **Evidence:** people.py:181-215 (the `_commit`/`_set_aside` pattern); `evidence/red-p1.txt`.

### LED-2026-10-24-batch-01.4 — the one seat (P1)
- **Requirement:** HLR-2604
- **Date:** 2026-10-24
- **What changed:** new requirement: `views.milestone_mark(task, board, today) -> (glyph, style, late_chip)` — shape+colour say the class, unclassified `◆` in `mut`, late date in `over` + `▲Nd`, reached hollow (`HOLLOW`) + `✓`; every section-3 site routed through it (the 21-site list), a test enumerates the sites; the title glyphs and project-span due marks stay. Declares AT-2603 (AT-b) with it.
- **Why:** MM-D1 (verdict D1 B); the commission's §3 «Route them all through ONE seat».
- **Evidence:** P-1 and P-2 (`evidence/premises.txt` — every site and exclusion verified at cited lines); proto.py:83,112-128.

### LED-2026-10-24-batch-01.5 — the editor Select, variant A (P1)
- **Requirement:** HLR-2605
- **Date:** 2026-10-24
- **What changed:** new requirement: the `alt+m` Select in `#task-chips-what` after `#f-milestone`; `alt+m` focuses it and joins `TASK_KEYS`; choosing `none` saves no `mark`. Carries AT-2601's editor arm.
- **Why:** the verdict's item 2 A (recommended, unmarked); MM-D8.
- **Evidence:** modals.py:501,513,378; proto.py:560-577; P-5.

### LED-2026-10-24-batch-01.6 — the `#` manager (P1)
- **Requirement:** HLR-2606
- **Date:** 2026-10-24
- **What changed:** new requirement: `#` opens `MarksManager` (frame the pure `views.render_marks`, D-4's fold); `n` opens `MarkForm` (name, shape from `SHAPES` plus `◆`, colour); `space` toggles `hidden`, persisted; the modal-keys law covers both; no class deletion. Declares AT-2604 (AT-f) and carries AT-2601's manager arm.
- **Why:** MM-D5, MM-D6 (storage), MM-D8; the ARQ's A-1 folded as D-4.
- **Evidence:** P-4 (`#` free); proto.py:774-935; `docs/ARCHITECTURE.md`:133,175.

### LED-2026-10-24-batch-01.7 — the legend strip (P1)
- **Requirement:** HLR-2607
- **Date:** 2026-10-24
- **What changed:** new requirement: the strip under the gantt ruler and in the presentation with its exports; only the classes drawn in the frame; none when none in view; the hidden count; `?` names the classes; `?`, the details line and the README updated. Declares AT-2605's legend arm.
- **Why:** MM-D7 (verdict 3 B).
- **Evidence:** proto.py:246-261,353-361; P-1.

### LED-2026-10-24-batch-01.8 — hide and search (P1)
- **Requirement:** HLR-2608
- **Date:** 2026-10-24
- **What changed:** new requirement: hidden classes leave the gantt and all three presentation views and their exports (`_hide`/`present_tasks_m`); the legend counts them; `/#cls` filters exactly, the bar names the class. Declares AT-2606 (AT-e) and carries AT-2605's hide arm.
- **Why:** MM-D6 (verdict 4 B); the round's cheap extra.
- **Evidence:** proto.py:294-299,367-371,505-520; P-1.

### LED-2026-10-24-batch-01.9 — `marks.Directory.load` (P1)
- **Requirement:** LLR-2601.1
- **Date:** 2026-10-24
- **What changed:** new LLR: `Mark`, `MARKS_NAME`, `SHAPES`, `COLOURS`, `Directory` with a live dict; `load` never raising (missing/blank/unreadable + `keep_aside`), entries cleaned and validated (slug id, unique, named, known shape); `find`/`named`.
- **Why:** HLR-2601's decomposition, mirroring people.py:119-160.
- **Evidence:** people.py:119-160; `evidence/premises.txt` P-3.

### LED-2026-10-24-batch-01.10 — `Directory.add`/`edit`/`set_hidden`/`_commit` (P1)
- **Requirement:** LLR-2601.2
- **Date:** 2026-10-24
- **What changed:** new LLR: the read-modify-write under `file_lock`, `write_atomic` `{"version": 1, "marks": [...]}`; `handle_for` ids; `edit` keeps the id; `set_hidden` flips only `hidden`; an `OSError` leaves memory unchanged; the unparseable file kept aside first.
- **Why:** HLR-2601/HLR-2603's write path, mirroring people.py:181-246.
- **Evidence:** people.py:181-246.

### LED-2026-10-24-batch-01.11 — the app holds the directory; `Board.marks` (P1)
- **Requirement:** LLR-2601.3
- **Date:** 2026-10-24
- **What changed:** new LLR: `Board.marks` (`{}`, app-set, never saved); the app loads `Directory.load(registry.path.parent / MARKS_NAME)`, sets `board.marks` in `_label_board` beside `board.people`, carries it in `after_move`, warns once on the unreadable report.
- **Why:** HLR-2601's app-side, mirroring app.py:1102,1208,1312-1315.
- **Evidence:** app.py:1102,1208,1312-1315; P-7.

### LED-2026-10-24-batch-01.12 — `Task.mark` on the model and through the editor (P1)
- **Requirement:** LLR-2602.1
- **Date:** 2026-10-24
- **What changed:** new LLR: the field on `Task`, read by `from_dict`, dropped when `None` by `_to_dict` (models.py:1049-1051 pattern); unknown ids round-trip; the editor carries the Select's value and keeps the field on untick.
- **Why:** HLR-2602's mechanism.
- **Evidence:** models.py:894-943,1045-1053; modals.py:789.

### LED-2026-10-24-batch-01.13 — team sync carries the field, never the directory (P1)
- **Requirement:** LLR-2602.2
- **Date:** 2026-10-24
- **What changed:** new LLR: `push` serialises `_to_dict(t)` unchanged (team_sync.py:157); a pulled unknown id draws unclassified; only `marks.py` reads or writes `marks.json`; nothing of the directory reaches the team folder.
- **Why:** HLR-2602's sync side; MM-D3.
- **Evidence:** team_sync.py:143-172.

### LED-2026-10-24-batch-01.14 — two windows, both survive (P1)
- **Requirement:** LLR-2603.1
- **Date:** 2026-10-24
- **What changed:** new LLR: two `Directory` objects on one file each keep the other's classes; 10 interleaved adds lose none.
- **Why:** HLR-2603's concurrency arm (AT-c's «two windows»).
- **Evidence:** the commission's AT-c; the `_commit` re-read (LED-2026-10-24-batch-01.10).

### LED-2026-10-24-batch-01.15 — the unreadable file kept; the bytes hold (P1)
- **Requirement:** LLR-2603.2
- **Date:** 2026-10-24
- **What changed:** new LLR: `keep_aside` before replace, never overwritten (the earlier `.corrupt` kept); a no-mark board's bytes equal before and after a load/save; no file until the first add.
- **Why:** HLR-2603's keep-aside and bytes arms (AT-c).
- **Evidence:** boards.keep_aside (docs/ARCHITECTURE.md:38); models.py:1045-1053.

### LED-2026-10-24-batch-01.16 — `views.milestone_mark`, the seat (P1)
- **Requirement:** LLR-2604.1
- **Date:** 2026-10-24
- **What changed:** new LLR: the seat's signature and truth table (classed/late/reached/unclassified × glyph, style, chip), `HOLLOW` per proto.py:83, reading `board.marks`; replaces `milestone_tone` (views.py:2523) at every site.
- **Why:** HLR-2604's mechanism; MM-D1's encoding.
- **Evidence:** proto.py:83,112-128; P-1.

### LED-2026-10-24-batch-01.17 — every site routed through the seat (P1)
- **Requirement:** LLR-2604.2
- **Date:** 2026-10-24
- **What changed:** new LLR: the 21-site enumeration (views.py:1107/1113,1677/1689,1800,2037,2541,2554,2643,2732,3035,3078,3615,5069-5099,5310,6538-6547,7146,8433; app.py:2133/2172/2433) with a test that fails on a site drawn outside the seat; the exclusion list (title glyphs; project-span due marks views.py:2613/3030/3044/6579/6856; the ruler's lateness).
- **Why:** the commission's §3 and its «a test enumerates the sites».
- **Evidence:** P-2 (`evidence/premises.txt` — all sites and exclusions verified).

### LED-2026-10-24-batch-01.18 — `TaskModal`'s class Select, variant A (P1)
- **Requirement:** LLR-2605.1
- **Date:** 2026-10-24
- **What changed:** new LLR: the Select mounted in `#task-chips-what` after `#f-milestone`, options as `Text.assemble` pieces (C-17), `alt+m` priority binding focusing it, `TASK_KEYS` gaining `("alt+m", "mark")`, `none` saving no `mark`, no-directory unchanged.
- **Why:** HLR-2605; the round's `EditorSelect`.
- **Evidence:** proto.py:560-577; modals.py:378,501,513; P-5.

### LED-2026-10-24-batch-01.19 — keymap `#` and `app.MarksManager` (P1)
- **Requirement:** LLR-2606.1
- **Date:** 2026-10-24
- **What changed:** new LLR: `Key("number_sign", "#", "marks_manager", "Milestone classes", group="misc", bar=False)`; `MarksManager` with its priority bindings (`escape,number_sign`, `up,k`/`down,j`, `space`, `n`, `e`); `check_action` gating; `?`/palette listing.
- **Why:** HLR-2606; MM-D8.
- **Evidence:** P-4 (`#` free); the `PeopleDirectory` pattern (app.py:985-1055); proto.py:852-867.

### LED-2026-10-24-batch-01.20 — `modals.MarkForm` and the modal law (P1)
- **Requirement:** LLR-2606.2
- **Date:** 2026-10-24
- **What changed:** new LLR: `MarkForm` (name, shape row over `SHAPES`+`◆`, colour row, the live preview, the key line); `alt+n`/`alt+c`/`alt+h`/`alt+s`/`esc`; the save through `Directory.add`/`edit`; the write error said; both modals in `tests/test_modal_keys.py`'s inventory.
- **Why:** HLR-2606; MM-D5 and MM-D8.
- **Evidence:** proto.py:774-849; modals.py:322.

### LED-2026-10-24-batch-01.21 — `space` persists; `views.render_marks` the pure frame (P1)
- **Requirement:** LLR-2606.3
- **Date:** 2026-10-24
- **What changed:** new LLR: the toggle through `Directory.set_hidden` + redraw + refresh; `render_marks(directory, sel, w, h)` — one row per class (shape, name, counts, hidden dimmed), `▶` on the chosen, `◆ (no class)`, exactly `w` cells of Text pieces — shipped in increment 002 (D-4's fold).
- **Why:** HLR-2606's storage and the ARQ's A-1 (folded as D-4).
- **Evidence:** proto.py:882-905; `docs/ARCHITECTURE.md`:133,175; PLAN.md D-4.

### LED-2026-10-24-batch-01.22 — `legend_strip` / `legend_strip_project` (P1)
- **Requirement:** LLR-2607.1
- **Date:** 2026-10-24
- **What changed:** new LLR: the two strips (only the classes drawn in the frame, then `N hidden`), drawn under the gantt's ruler (`_gantt_frame`) and by `render_present` with its export, per project in the all-boards presentation; nothing when none in view.
- **Why:** HLR-2607; MM-D7.
- **Evidence:** proto.py:246-261,353-361,267-291; views.py:2973,6622.

### LED-2026-10-24-batch-01.23 — the `?` help, the details line, the README (P1)
- **Requirement:** LLR-2607.2
- **Date:** 2026-10-24
- **What changed:** new LLR: `help_usage`/`legend_entries` name the classes; the gantt's details line says what a class mark is (its exact seat `assumed — verify in Phase 3`); `README.md` documents the feature.
- **Why:** HLR-2607's help side; MM-D7.
- **Evidence:** views.py:7866,8027,2929; README.md (exists).

### LED-2026-10-24-batch-01.24 — `_hide` / `present_tasks_m` (P1)
- **Requirement:** LLR-2608.1
- **Date:** 2026-10-24
- **What changed:** new LLR: `_hide` the shallow proxy dropping hidden-classed milestones, applied to the gantt frame; `present_tasks_m` wrapping `views.present_tasks` for the presentation screen and the export writer; the board object itself untouched.
- **Why:** HLR-2608's hide arm; MM-D6.
- **Evidence:** proto.py:294-299,367-371; views.py:6179; app.py:47,390; P-7.

### LED-2026-10-24-batch-01.25 — `matches_m` / `filter_bar_m` (P1)
- **Requirement:** LLR-2608.2
- **Date:** 2026-10-24
- **What changed:** new LLR: the `#cls` query (the directory's `find`, lower case, prefix), the `"class"` kind, the bar `/ <shape> <Name>  milestones of this class only` with the tally; a `#cls` naming no class keeps nothing; text queries unchanged.
- **Why:** HLR-2608's search arm; the round's item 4.
- **Evidence:** proto.py:500-520; views.py:3720,3751,7385.

### LED-2026-10-24-batch-01.26 — the seat's site list: app.py:2433 is a project-span due mark (P2 fold)
- **Requirement:** HLR-2604
- **Date:** 2026-10-24
- **What changed:** Before → After. The statement's notice list read «`app.py`'s notices (`:2133`, `:2172`, `:2433`)»; it now reads «`app.py`'s notices when they show a milestone mark (`:2133`, `:2172` — `:2433` qualifies only while it shows one, which today it does not: it is a project-span due mark, `{pn} +{over}d past ◆`, and stays as it is)», and the exclusion clause gains `:2433` among the project-span due marks. The boundary catalog's empty class reworded (UX-1) is recorded in this entry's requirement too: «no directory: every frame draws exactly as before» → «no classes: every milestone draws unclassified — `◆` in `mut`, its state in text; an unclassified milestone loses its red mark, MM-D1's accepted cost».
- **Why:** the P2 architect review, ARCH-1 (major: the seat is keyed by task; 2433 is a project slip mark) and the P2 ux review, UX-1 (major: the old empty-boundary claim was unsatisfiable — MM-D1's accepted cost is exactly that unclassified loses the red mark).
- **Evidence:** `app.py:2433` read at draft (`{pn} +{over}d past ◆`, the slip clause); `evidence/premises.txt` re-run (P-2: the slip notice now in the exclusion list, all TRUE).

### LED-2026-10-24-batch-01.27 — LLR-2604.2's site list and exclusion list (P2 fold)
- **Requirement:** LLR-2604.2
- **Date:** 2026-10-24
- **What changed:** Before → After. «…and `app.py`'s notices (`:2133`, `:2172`, `:2433`)» → «…and `app.py`'s notices when they show a milestone mark (`:2133`, `:2172`)»; the exclusion list gains «the slip notice at `app.py:2433` (`{pn} +{over}d past ◆` — a project-span due mark, not a milestone seat site; the seat is keyed by task)».
- **Why:** ARCH-1 (same finding as LED-2026-10-24-batch-01.26, at the LLR the site enumeration belongs to).
- **Evidence:** `evidence/premises.txt` (P-2, re-run 2026-10-24).

### LED-2026-10-24-batch-01.28 — the late chip implies `over`, one channel (P2 fold)
- **Requirement:** LLR-2604.1
- **Date:** 2026-10-24
- **What changed:** Before → After. The statement gains: «a non-empty `late_chip` shall imply the milestone's date renders in `over` at every site — one channel out of the seat, no site re-deriving lateness».
- **Why:** the P2 architect review, ARCH-3 (minor: the implication was implicit; a site re-deriving lateness could drift from the seat).
- **Evidence:** the seat's truth table in the threshold (`unclassified+late → date style `over``) already pinned the channel; the statement now says it.

### LED-2026-10-24-batch-01.29 — the Directory's load validation and find (P2 fold)
- **Requirement:** LLR-2601.1
- **Date:** 2026-10-24
- **What changed:** Before → After. (1) The skip clause gains: the `colour` must be one of the defined `COLOURS` set (named `COLOURS`, NEW — created in Phase 3, mirroring `SHAPES`); every field must be of its expected type (a non-string name, shape or colour an entry skipped); `hidden` coerced to `bool`. (2) `find(q)` — «name starts, then inside the name, lower case» → «prefix only, lower case, mirroring the round's `find_class` (`proto.py:500`-`:503`)»; `named(name)` dropped from the interface (no consumer anywhere in the contract). (3) The cleaning clause now cites the flattening: «cleaned with `models.clean_strings` and flattened to one line as `people._clean` does it (`people.py:60`-`:64`: every whitespace run — newlines and tabs included — becomes a single space)» — `clean_strings` keeps tab and newline by design (`models.py:534`-`:535`), so the one-line flattening is the directory's own step. (4) The TC-2601 threshold arms: the mixed file gains a bad-colour and a non-string-name entry; new arms — an unknown colour / a non-string name skipped with the good entries kept, an embedded-newline name loads flattened to one line, and a name carrying control bytes/ANSI (`\x1b[31m`) loads and renders literally — no error, no style leak.
- **Why:** the P2 architect review, ARCH-2 (major: `/#cls` resolves by prefix; find must mirror the round), ARCH-5 (minor: `named` had no consumer); the P2 security review, SEC-1 (major: load-time type/colour/bool validation), SEC-2 (minor: the control-byte claim overreached — the flattening is the directory's own step), SEC-3 (minor: the hostile-payload arm named explicitly).
- **Evidence:** `proto.py:500`-`:503` (`find_class` startswith, lower case); `people.py:60`-`:64` (`_clean` flattens whitespace runs to single spaces); `models.py:534`-`:535` (`strip_controls` keeps `\t` and `\n`).

### LED-2026-10-24-batch-01.30 — AT-2601 asserts the file on disk (P2 fold)
- **Requirement:** HLR-2601
- **Date:** 2026-10-24
- **What changed:** Before → After. AT-2601's black-box threshold arm «`app.marks.path` is `<home>/.taskboard/marks.json`; `#`, `n`, … → the class in `marks.json` …» → «`#`, `n`, … → the file `<home>/.taskboard/marks.json` exists on disk and holds the class with `hidden: false` (read back from disk, not through the app)». The internal `app.marks.path` assertion stays in LLR-2601.3's white-box threshold only.
- **Why:** the P2 qa review, QA-1 (minor: an acceptance arm must assert the observable surface, not an internal attribute).
- **Evidence:** LLR-2601.3's threshold (unchanged, white-box).

### LED-2026-10-24-batch-01.31 — HLR-2607's verification covers the README clause (P2 fold)
- **Requirement:** HLR-2607
- **Date:** 2026-10-24
- **What changed:** Before → After. «`python -m pytest -q -p no:cacheprovider tests/test_legend.py`» → «`env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_legend.py tests/test_readme.py -k "AT_2605 or TC_2607 or readme"`».
- **Why:** the P2 qa review, QA-2 (minor: the statement's README clause had no covering command).
- **Evidence:** the commission's env rule (`env -u NO_COLOR` for every pytest).

### LED-2026-10-24-batch-01.32 — LLR-2607.2's firmness and the `/#cls` help entry (P2 fold)
- **Requirement:** LLR-2607.2
- **Date:** 2026-10-24
- **What changed:** Before → After. The statement's hedge gains its discharge: «`assumed — verify in Phase 3` — increment 004 names it, and its gate shall confirm `_gantt_legend` (`views.py:2929`) is that operator-visible line; if it is not, the gate names the true seat and a ledger entry records the amendment». The threshold pins the same seat with the same condition («the details-line seat named in the statement, confirmed at the increment-004 gate») and gains «`?` names the `/#cls` filter».
- **Why:** the P2 qa review, QA-3 (minor: the statement hedged while the threshold pinned — now they agree in firmness, and the gate owns the confirmation); the P2 ux review, UX-4 (minor: `?` must name the filter, not only the README).
- **Evidence:** `views.py:2929` (`_gantt_legend`) read at draft.

### LED-2026-10-24-batch-01.33 — the Select's `+ new class…` drop and the empty-directory wording (P2 fold)
- **Requirement:** LLR-2605.1
- **Date:** 2026-10-24
- **What changed:** Before → After. The statement gains «and no `+ new class…` option (that is the manager's job, `n`; the Select only picks)» — the round's Select has that option (proto.py:567-568) and the contract drops it, recorded in §1.2's Out of scope with the same reason. «with the directory `None` the modal composes exactly as before» → «with an empty directory (the app always loads one) the modal composes no Select»; the TC-2605 threshold's «no directory → no Select» → «an empty directory → no Select».
- **Why:** the P2 architect review, ARCH-4 (minor: the dropped option must be recorded, not silent); the P2 ux review, UX-5 (minor: the app always loads a directory, possibly empty — «no directory» was unfalsifiable prose).
- **Evidence:** proto.py:567-568 (the round's `+ new class…` option); §1.2 Out of scope (the drop and its reason).

### LED-2026-10-24-batch-01.34 — HLR-2605's empty-directory wording (P2 fold)
- **Requirement:** HLR-2605
- **Date:** 2026-10-24
- **What changed:** Before → After. «with no directory the editor shall draw exactly as before» → «with an empty directory (the app always loads one, possibly empty) the editor shall draw no Select — a change from before»; the boundary catalog's «empty (no directory: no Select)» → «empty (an empty directory: no Select — the app always loads one, possibly empty; a change from before)».
- **Why:** UX-5 (same finding as LED-2026-10-24-batch-01.33, at the HLR).
- **Evidence:** app.py:1102 (the app always loads a directory).

### LED-2026-10-24-batch-01.35 — the manager's key row toggles both ways (P2 fold)
- **Requirement:** HLR-2606
- **Date:** 2026-10-24
- **What changed:** Before → After. The threshold's key row «`↑↓ move   ␣ hide   n new   e edit   esc close`» → «`↑↓ move   ␣ hide/show   n new   e edit   esc close``.
- **Why:** the P2 ux review, UX-2 (minor: `space` toggles both ways, and the round's frame paints `␣ hide/show`, proto.py:915).
- **Evidence:** proto.py:903-905 (the round's key line).

### LED-2026-10-24-batch-01.36 — AT-2602's file-as-surface exception (P2 fold)
- **Requirement:** HLR-2603
- **Date:** 2026-10-24
- **What changed:** Before → After. AT-2602's acceptance cell records the exception: «the two-window arm is the rule-(d) file-as-surface exception, recorded: two `Directory` objects are the code a second process runs, and the observable surface the test asserts is `marks.json` on disk — both classes in the file after each window's add».
- **Why:** the P2 security review, SEC-5 (minor: a black-box test driving two in-process objects needed its surface exception stated, reasoned — the file is the shared surface a second process would hold).
- **Evidence:** `evidence/premises.txt` P-3 (the two-window code path is the directory itself); §5.1 («another window» is a second `Directory` on the same file).

### LED-2026-10-24-batch-01.37 — the notice count downstream of ARCH-1 (P2 second pass)
- **Requirement:** HLR-2604
- **Date:** 2026-10-24
- **What changed:** Before → After. AT-2603's threshold: «…the people view's rows and the three notices; … the site-enumeration test lists every section-3 site…» → «…the people view's rows and the two notices (`:2133`, `:2172` — the slip notice at `:2433` stays as it is); … the site-enumeration test lists every site of the statement above…»; the Shipped surface: «the milestone/done/slip notices» → «the milestone/done notices»; and the statement's site names were aligned to LLR-2604.2's granularity (per-function seats: `_milestone_title`, `gantt_milestone_cells` :2545-:2576, the chain map's label :3613-:3617, `band_milestone_facts` :5053-:5099, `_present_task_row` :6537-:6547, `_task_rows` :8433-:8467) so both enumerations name the same seats the same way. Parent-HLR re-read: not required beyond this entry — the changes ARE the HLR's own statement/threshold/surface cells.
- **Why:** the second P2 pass found the ARCH-1 fold had half-landed — the site lists were fixed but the notice count and the slip surface rode along; the granularity alignment closes the last drift between the HLR and its LLR.
- **Evidence:** `app.py:2433` read at draft (the slip clause); the seat list diffed line by line against LLR-2604.2 (20 seats, same names both sides).

### LED-2026-10-24-batch-01.38 — the enumeration count (P2 second pass)
- **Requirement:** LLR-2604.2
- **Date:** 2026-10-24
- **What changed:** Before → After. «lists every site above (21 sites)» → «lists every site above (20 sites — one line-ref = one site; the gantt echo folds into the one-date bars at `:2732`)».
- **Why:** the second P2 pass: the ARCH-1 removal of `:2433` made the count 20, and the echo at `:2732` is the same seat as the one-date bars — one line-ref, one site.
- **Evidence:** the site list counted at draft (20 refs: two per lanes/focus pair, sixteen single seats, two notices).

### LED-2026-10-24-batch-01.39 — the load-time skip enumeration (P2 second pass)
- **Requirement:** HLR-2601
- **Date:** 2026-10-24
- **What changed:** Before → After. «an entry with a malformed or repeated id, no name, or an unknown shape skipped» → «an entry with a malformed or repeated id, no name, an unknown shape or colour, or a field of the wrong type, is skipped» — the HLR's skip clause now covers what LLR-2601.1 already validated (LED-2026-10-24-batch-01.29, SEC-1).
- **Why:** the second P2 pass: the HLR lagged its own LLR after the SEC-1 fold; a reader of the HLR alone would miss the colour/type skips.
- **Evidence:** LLR-2601.1's statement (LED-2026-10-24-batch-01.29).

### LED-2026-10-24-batch-01.40 — SHAPES membership and the ANSI arm (P2 second pass)
- **Requirement:** LLR-2601.1
- **Date:** 2026-10-24
- **What changed:** Before → After. «`SHAPES` (the nine glyphs plus `◆`, the oracle proto.py:85)» → «`SHAPES` (the eight glyphs of `proto.py:85` plus `◆` — `◆` is not a member of `SHAPES`; it is the unclassified mark's glyph)»; the TC-2601 ANSI arm: «loads and renders literally — no error, no style leak» → «loads without error and renders with no style leak (control bytes stripped at load)» — matching `strip_controls`'s actual contract (C0 bytes other than tab/newline removed, `models.py:534`-`:535`).
- **Why:** the second P2 pass: `SHAPES` holds eight glyphs (proto.py:85) and `◆` stands apart as the unclassified mark's glyph — saying «the nine glyphs plus `◆`» miscounted and blurred the membership; «renders literally» overclaimed for a byte that is stripped, not rendered.
- **Evidence:** proto.py:85 (eight entries); models.py:534-535 (`strip_controls` keeps `\t`/`\n`, removes the rest of C0).

### LED-2026-10-24-batch-01.41 — the Select's empty-directory boundary (P2 second pass)
- **Requirement:** LLR-2605.1
- **Date:** 2026-10-24
- **What changed:** Before → After. The boundary catalog's «empty (no directory; `none` chosen)» → «empty (an empty directory; `none` chosen)» — the UX-5 fold (LED-2026-10-24-batch-01.33) had updated the statement and the threshold but missed the boundary cell.
- **Why:** the second P2 pass: the app always loads a directory, possibly empty — «no directory» was unfalsifiable prose in the last place it survived.
- **Evidence:** app.py:1102 (the app always loads a directory).

### LED-2026-10-24-batch-01.42 — the env prefix on every verification command (P2 second pass)
- **Requirement:** HLR-2604
- **Date:** 2026-10-24
- **What changed:** Before → After. Every `Executed verification` command in the contract (24 of 25; the 25th, HLR-2607's, already carried it) now reads `env -u NO_COLOR python -m pytest …`, and §5.1 states the rule once: «Every `Executed verification` command in this contract carries the `env -u NO_COLOR ` prefix — the commission's rule … without it the colour tests fail» (this §5.1 amendment is the UX-3 follow-up, HLR-2604 named as nearest owner — §5 is not a requirement and names no heading of its own).
- **Why:** the second P2 pass, fold 9: the commission's rule («Run env -u NO_COLOR for every pytest, otherwise the colour tests fail») applied to the contract's own commands; the style-asserting tests of AT-2603 and the tone arms run under the prefix at the gates.
- **Evidence:** the commission's evidence rules (`IMPLEMENTATION.md` §6); the 24-line replace audited (25 `Executed verification` fields, all prefixed).

### LED-2026-10-24-batch-01.43 — the §6.3 amendments (P2 second pass)
- **Requirement:** LLR-2602.2
- **Date:** 2026-10-24
- **What changed:** Before → After. §6.3's C6 answer: «hostile-payload AT arms … are owed in Phase 3» → «hostile-payload TC arms …» — the payload arms live in TC-2601's threshold (LLR-2601.1) and TC-2605/TC-2606, not in an AT (this §6.3 amendment is the SEC-2 follow-up; LLR-2602.2 named as nearest owner for the payload-render claim — §6 is not a requirement and names no heading of its own).
- **Why:** the second P2 pass, fold 7: an «AT arm» that does not exist in any AT node would be a phantom obligation; the TCs carry them.
- **Evidence:** LLR-2601.1's threshold (the ANSI arm); LLR-2605.1/LLR-2606.2's thresholds (the `[b]x[/b]` arms).

### LED-2026-10-24-batch-01.44 — the §6.3 SEC-4 line's owner (P2 second pass)
- **Requirement:** HLR-2601
- **Date:** 2026-10-24
- **What changed:** Before → After. No text change — this entry records the second pass's ruling that the §6.3 SEC-4 amendment (the id-slug sensitivity line added at LED-2026-10-24-batch-01.29's pass) names HLR-2601 as its nearest owner (the line speaks for the directory's ids, HLR-2601's subject), keeping §6.3's amendments paired with a requirement for `V26`.
- **Why:** the second P2 pass, fold 10: §6 is not a requirement; every §6.3 amendment names its nearest owner so the ledger pair stays complete.
- **Evidence:** §6.3 (the SEC-4 line); HLR-2601 (the directory and its ids).

### LED-2026-10-24-batch-01.45 — `◆` is not a member of `SHAPES`, in every consumer (P2 third pass)
- **Requirement:** HLR-2606
- **Date:** 2026-10-24
- **What changed:** Before → After. The §1.3 glossary row and this HLR's statement defined the form's shape set as «`SHAPES` … plus `◆`», contradicting LLR-2601.1 (LED .40: «`◆` is not a member of `SHAPES`») — a class saved with `◆` would be skipped by the load validation on the next start. Now: the glossary row reads «the manager's one-cell shape set `▲ ■ ⬢ ★ ⬟ ▼ ✦ ⚑` (proto.py:85); the form offers `◆` beside it as the unclassified mark's glyph — `◆` is NOT a member of `SHAPES`, so the load validation (LLR-2601.1) never drops a saved class», and the statement reads «the shape row (`SHAPES` = `▲ ■ ⬢ ★ ⬟ ▼ ✦ ⚑`, proto.py:85, plus a separate `◆` choice — the unclassified mark's glyph, not a member of `SHAPES`)».
- **Why:** the third P2 pass, QA-4: the LED .40 fold landed in LLR-2601.1 only; its two downstream consumers still defined the set as including `◆` — the same half-landed-fold class the gate caught at pass 2, this time closed at both consumers.
- **Evidence:** §1.3 (the `SHAPES` row); HLR-2606's statement (the shape row clause); LLR-2601.1's skip clause (`shape ∈ SHAPES`, LED .40).
