# BACKLOG — taskboard (canonical, cross-batch)

Shared by `/dev-flow` and `/fast-dev-flow`. Every open item lives here exactly once.
No `docs/engineering-rules.md` exists in this repo, so this is the default location.

**Base ref:** `0447070` (local HEAD == `origin/main`; batch 2026-10-04-batch-01 started here)
· **Last refresh:** 2026-10-04
**Status:** **2296 tests** (batch `2026-10-04-batch-01`, Batch B1: waits-on links — `◂N`/`▸N`,
the ready message, `L` through the picker and the gantt link mode, the details dependency section,
the archive/delete guard, the one-time link migration with backup, log, undo and run-once; flow
rev99 from a read-only snapshot). `test_win_clipboard_roundtrip` remains an intermittent
environmental flake (failed in the batch's gate runs on its own SETUP; G-011).

## Open — after `2026-10-04-batch-01` (Batch B1: waits-on links)

- **Present a whole project** (operator request with the visual verdict, 2026-10-04 — a new
  feature, routed to a PROTOTYPE ROUND FIRST, real renders and the operator's verdict before any
  increment): a presentation of one complete project — its gantt, its tasks and the tasks' text —
  in a format fit to present, with an export of what is shown to SVG or an image. Operator's
  words: "presentación de un proyecto completo. Donde se vea el gantt, las tareas y el texto de
  las tareas en un formato apropiado para presentar. Además de poder exportar SVG o una imagen de
  lo proyectado." Open questions for the round: full-screen view vs export-only; page size and
  pagination; which task text (notes, links); the export path and file naming.
- **Batch B2 — milestones, moving linked dates, the M-3 offer** (D-501, the pre-authorized B1/B2
  split): milestones M-1/M-2, moving a task's dates moves what waits on it (round 6), the one-time
  M-3 milestone offer. Seed: the kg_mejoras verdict frames; the waits-on model and the one overlap
  measure (`models.link_overlap`, D-503) are in place. Batch C (the chain map view) keeps key `6`.
- ✓ done in `2026-10-04-batch-01` increment 006 (operator: "Corregirlo antes del push"; A-9) — **The gantt link mode can fold the waiter's row** (ux F4, MED; D-528): `gantt_plan` unfolds
  groups greedily by fit, so at 118×20 — and at 118×30 on boards with larger projects — the
  waiter's group folds and the overlay has no row to draw on; increment 005 says it on the hint
  row (A-8). The fix is a fold rule that keeps the waiter's group open (fold every other group
  first), in the shared seat that also feeds `nav_model` — the operator's call at PV-5.
- ✓ done in `2026-10-04-batch-01` increment 006 (operator: "Corregirlo antes del push"; A-10) — **A lanes card can lose its whole title** (ux U-2, MED; D-529): `card_cell` keeps indicators the
  moment their cells fit, so beside `▸1 ◂1` (5 cells, where `⛓1` was 2) two cards at 118 and 80
  paint no title (one at base). A title floor breaks two shipped width contracts
  (`tests/test_cells.py`: the aging and deadline tokens are kept the moment they fit) — the
  operator's call at PV-1 on which wins.
- ✓ done in `2026-10-04-batch-01` increment 006 (operator: "Corregirlo antes del push"; A-11) — **A read-only board on Windows leaves a temp file per launch** (security close F1, LOW; D-530):
  `Board.save_atomic` copies the board's mode onto its temp file, so on Windows the read-only bit
  makes `os.replace` and the cleanup `unlink` both fail; each launch of an unmigrated read-only
  board leaves a `.board.json.<random>.tmp` and the error names the temp file. Fix: clear the bit
  before the unlink (or copy the mode only off Windows), with a read-only-board test.
- ✓ done in `2026-10-04-batch-01` increment 007 (operator: "Dejar ◂ solo, quitar la edad antes"; A-12) — **Lanes show no link marks below about 140 columns** (ux R6-3, D-533; flagged to the operator):
  the D-529 floor sheds `▸`/`◂` before the age `·Nd`, so at 118 and 80 the lanes paint no marks;
  the operator may prefer the age shed first, or `◂` kept alone.
- **At 80 columns an overdue waiting lanes card loses its overdue chip** (ux N-1 after increment
  007): under D-533 the due is "other meta" and goes before `◂` (`SDK re… ◂1 -5d` at 118 → `SDK r…
  ◂1` at 80). If overdue should outrank `◂`, that is a new operator ruling.
- **Lanes test and wording details** (qa G-009, G-010; ux N-2, N-3, after increment 007): TC-504
  checks waiting cards by a unique title prefix and ends with `assert waiting_seen` — assert the exact
  number of waiting cards painted instead; the 160×40 test's docstring says "no `▸` at 118" where it
  means no WAITING card shows `▸`; a cut at a word gap leaves a blank cell before `…`; no painted
  grouped-kanban baseline at 118×40, 140×30, 160×40.
- **Link-mode paging details** (ux R6-1, R6-2, LOW): the fallback note says "folded" when the waiter
  is only off the page ("is off this page" reads truer); when the two groups share the rows, the
  waiter's group gets no `▲/▼` pager line.
- **The read-only exit advice names the folder** (ux R6-4, LOW): since D-530/D-532 the cause is the
  board file's own read-only bit; the message should say so.
- **`python -m taskboard` exits 0 after a fail-closed stop** (ux R6-5, LOW, pre-existing):
  `__main__.py` ignores `app.return_code`, so a script reads success.
- **`critical_chain` is recursive and exponential on dense boards** (security S-6, MEDIUM,
  pre-existing): the gantt's critical chain walks every path; the waits-on model's own searches
  are iterative (D-522) but this seat was not this batch's requirement.
- **An unreadable board is saved over by the renumber notice** (security S-13, LOW,
  pre-existing): the migration does nothing on an unreadable file; the renumber path still saves.
- **Render cost grows quadratically on boards of thousands of tasks** (code review 002 F8):
  `link_marks` is computed once per render, but some views still pay per card on large boards.
- **`◂` carries several meanings** (ux UX-22, PV-1): a card's wait count, the conflict prefix,
  the details heading's "◂ waiting" and the gantt's off-window glyph; on cards it always carries a
  count.
- **Both `L` surfaces start on the first candidate even when it is already linked** (ux U-3,
  LOW): `L ↵` then removes a link (said, and `u` restores it); start on the first unlinked one.
- **Link-mode details** (ux U-4, U-5, LOW): `═` runs past the waiter's own due and covers its `○`;
  the waiter's row loses its selection mark while the candidate holds it.
- **80-column details** (ux U-6, U-7, N-5, N-6, LOW/NIT): the grouped kanban shows `◂` on 2 of 5
  waiting cards (a wrapped title takes the meta row, as `⛓` did); the picker shows about two
  candidates and a long hint wraps to a third line; the migration toast splits "u / undo"; the
  loop legend clips.
- **Wording seams** (ux N-1..N-4, N-7, NIT): the picker's and link mode's key rows say different
  things; "↵ link" is offered on "no match"; toast titles "Links" vs "Dependencies"; "Waits on
  ◂0 open of 0" after the last link is removed; `L` pushes "Standup" off key `8` in kanban at 118.
- **The picker lists every open task** (increment 003 risk): on a board of thousands the list is
  long; the filter narrows it.
- **A comment overstates** (code review 005 NIT): `GanttLinkMode._paint` says rows past the frame
  are not mapped; at a frame of 3 rows the candidate can be (never the waiter, so `folded` holds).

## Open — after `2026-10-02-batch-04` (Batch S: hardening)

- **The markup census's residual blind spots** (code review H1, H2, round-1 residuals and security
  S4-4 of `2026-10-02-batch-04`, LOW): `tests/test_markup_census.py` trusts a `-> Text` call by NAME,
  so six shapes still fool it — a local rebinding of the name, a parameter of that name, an import
  alias, a lying helper in an uncensused module, `self.x = str` before `self.x(...)`, an unannotated
  namesake; also a module-attribute widget (`w.Label(x)`), a widget subclass passing `content` to
  `super().__init__`, `getattr(Text, "from_markup")`, and a piece style built from data
  (`Text(t, style=p.color)`, D-413 is review-only). None is used today. Fix: refuse a trusted name
  that is a parameter, stored, or imported in the calling function/module; collect unannotated
  namesakes; plant each shape in TC-403. H2: the `_text_functions` docstring says "its definition".
- **Ctrl+V through the handler is untested** (P4 qa G-001): TC-414 calls `_clean_clipboard_text`
  directly and the Ctrl+V tests patch `modals.grab_clipboard_text`, past the cleaner. Add a test
  that drives the real paste with a dirty clipboard stub below the cleaner.
- **Roster hues may wear alert tones** (security S4-2, LOW): `clean_roster` accepts any `HEX` key,
  so a teammate's hue can be `over` / `soon` / `accent`. Restrict to a person-hue subset.
- **Hand-edited data is normalised silently** (security S4-3, LOW): `Project.from_dict` turns a
  hand-edited `archived: 1` into `False`, and `clean_strings` keeps the later of two keys equal once
  cleaned (D-410, D-408). Consider a load-report line naming normalised fields.
- **Setup saving over an unreadable `team.json` resets its version** (security S5-1, LOW): the new
  file gets `version: 1`, teammates holding a newer version ignore it. Warn on save, or carry the
  last adopted version + 1.
- **Synced phases and project extras are cleaned, not bounded** (D-414): duplicate phase names and
  the list's length are unbounded; a new project adopts unknown synced keys into `extra`.
- **`history.jsonl` is not cleaned** (D-409; security note): legacy records may hold control bytes
  (never painted: phases are matched against the board's), and `history.read`'s `json.loads` does
  not catch `RecursionError` (a local file). Clean at `history.read` and catch it.
- **A teammate's task dates are untyped** (code review note, increment 002): `Task.from_dict` lets an
  int or list `due_date` / `start_date` through; no crash was found (8 views rendered).
- **Unicode format characters pass** (P2 security S-9): bidi overrides and zero-width characters
  are not control bytes; a roster name or title can be visually spoofed.
- **The details view paints values in the label tone** (P2 UX-8, pre-existing): `.modal Label`
  colours both `#8b98a5`; the values are the information.
- **Two test names say "escapes"** (code review F5 of increment 001): `test_app.py`
  `test_manage_projects_escapes_markup_name`, `test_phase_name_with_markup_is_escaped` now assert the
  text is NOT escaped. Rename when the file is next touched.
- **The `team.json` toast wraps mid-sentence on a long path** (P4 UXV-3, minor); **the 80×24 details
  scrollbar thumb sits inside the border with no track** (P4 UXV-2, pre-existing).
- **`run_test` hides toasts unless `notifications=True`** (P4 ux note): a toast assertion without the
  flag finds nothing. Record it in `docs/engineering-rules.md` when that file exists.
- **`.modal-title { margin-bottom: 1 }` never applies to a Label title inside `.modal`** (code review
  observation, increment 004 of `2026-10-02-batch-04`): `.modal Label { margin-top: 1 }` outranks it,
  and Textual's `margin-top` replaces the whole margin, so every modal title has a row above and none
  below. The details view now overrides it by id (UX-3); decide whether the edit modals should match,
  then drop or fix the dead declaration.
- **`state.json` `owner` holds the full local path** (security S7-1 of `2026-10-02-batch-04`, LOW,
  pre-existing): the Windows account name reaches the remote. Decide whether `owner` must be a machine
  path; if not, make it repo-relative at batch init.

## Open — after `2026-10-02-batch-03` (Batch A2: the readable kanban)

- ~~**Operator verdicts owed on the provisional visual decisions** (PV-1..PV-10)~~ **DONE 2026-10-02**
  — the operator accepted all ten on the before/after captures, before the push (PV-2: the cap at
  two thirds): `2026-10-02-batch-03/evidence/operator-verdict-provisional.json`.
- **`collapse_runs` can join two adjacent same-style escaped pieces into a tag** (kept open by
  `2026-10-02-batch-04`, D-405: its seat is `views.py`'s Rich markup, not the Textual sinks that batch
  converted to Text pieces; the class cannot occur there any more) (security S-2 of
  `2026-10-02-batch-03` increment 002, LOW, latent): an unclosed `[` in one piece meets a `]` in the
  next once `[/][same]` is collapsed. No path this batch draws reaches it (each user piece is
  bounded by fixed text or another style); the same weakness exists for `escape` everywhere. Fix:
  `collapse_runs` refuses a merge when the text before holds an unmatched `[`; regression test from the repro.
- **The gantt's nav asks the full height under a `/` filter** while `render_view` draws it two rows
  shorter (the D-312 gap, fixed for the kanban only in `2026-10-02-batch-03`): check whether
  `gantt_plan`'s paging makes nav and draw disagree; if so, extend `_nav_columns`'s `h − 2` to the gantt.
- **`kanban_plan` repeats `_phase_window`'s window arithmetic** over the open phases (code review
  F10 of increment 001, accepted): a shared helper taking a phase count.
- **The cut band at a small room** (P4 UXV3-12): at room 4 (14 highs, 80×24) a cut band shows one
  card then two blank rows before the fold row, which read as the band's end; below room 3 the band
  is drawn alone and the panel scrolls (declared). Operator: shrink the high-band cap (PV-2) when a
  band has to be cut?
- **The fold row at 80 columns** (P4 UXV3-13): the in-band cut counts push the `▼ below` names into
  the ellipsis sooner (`Done (0 open)` drops off under horizon); every count still prints.
- **A band rule's open count includes its highs drawn in the high band** (P4 UXV3-14: `Later 10 open
  · 3 high ↑` beside fold counts summing to 7): say `7 here · 3 high ↑`?
- **A toast paints over the fold row's right end** (P4 UXV3-15; the shipped toast) until it expires.
- **Four threshold clauses asserted weaker than written** (P4 qa G-002, `2026-10-02-batch-03`
  `04-validation.md`): HLR-305's 80×24 tag-room clause has no node; HLR-306's 80×19 case is asserted
  as capped-or-not; HLR-303's one-rule-per-group as a subset; widths 24..160 sampled. The behaviour
  holds by qa probe1; a tests-only pass tightens them.
- **Done work past the rail's `+N more`, and every done task below 100 cells, cannot be reopened
  with `[` from the kanban** (D-305): widen to ≥ 100 cells or use the agenda. A selectable count?
- **The horizon group mode's `Done` band reads `Done (0 open)` in the fold row** (its open cells are
  empty by definition): word it `Done (N done)`?
- **The prototype's selected-card detail line** (shown in the approved frame when nothing is folded,
  not in the commission): ship it?
- **AT-307 saw the band rules shift one cell once** (a transient width change during a `down` walk
  at terminal 80×24 — likely a scrollbar or a resize race): the test now compares the band SET;
  look for the transient at the next UX pass.
- **`at risk` cannot reach the screen** (P4 UXV3-2, D-315): the band rule prints `at risk` for a
  project whose status is `at_risk`, but `models.PROJECT_STATUSES` has no such status and
  `Project.from_dict` maps it to `on_track`. Operator: add the status, derive "at risk" (e.g. late
  work), or drop the fact?
- **`up` into a band already drawn re-flows the board** (P4 UXV3-3, D-314 covers `down` only):
  operator — keep the window on `up` as well?
- **`left`/`right` land on the next column's first card and re-window to the top** (P4 UXV3-5,
  UX-11; the shipped `hmove`): operator — should a lateral move stay in the same band?
- **The entry cursor rests on a done rail title at ≥ 100 cells** (P4 UXV3-9; `_select_first` picks
  the first visible task in board order): start on the first high card instead?
- **`done 0d ago` for a task finished today** (P4 UXV3-8): say `done today`.
- **`?` at 80×24 clips the kanban help's "the board" section** (P4 UXV3-4) — joins the existing help
  right-column layout item; at 118 two bullets touch the Keys column.
- **A no-match filter still says `press 'a' to add one`** (P4 UXV3-10); **`z` below 100 cells changes
  nothing visible** (P4 UXV3-11).

## Open — after `2026-10-02-batch-02` (Batch P: polish)

- ~~**Operator verdicts owed on the provisional visual decisions**~~ **DONE 2026-10-02** — the
  operator accepted all eight (D-203, D-204, D-205, D-208, D-211, D-213, D-214, D-217) on the
  before/after captures, before the push: `2026-10-02-batch-02/evidence/operator-verdict-provisional.json`.
  The residuals they named (UXV2-3/4/5/6/7) stay as known behaviour, not defects.
- **The key bar's `more` layer has no group boundaries** since the group hues left (UXV2-2, D-211):
  a dim ` · ` group separator costs ~7 cells (~3 keys dropped at 80). `;` reaches it again since
  D-218 (the toggle had read Textual's CSS `layer` since 8b73920).
- **Soon-due amber outside `reldue_token`** (UXV2-1, HLR-203 amended, LED .19): the Focus view's
  `date_chip` seats — tiles, cards, image and compact cards, the detail pane, the review layout's
  selected-task line — still paint +1..+7d in `later` slate (`_URG_COLOR["week"]`). Operator: extend
  the amber to them?
- **The word `today` has three tones** (D-209, UXV2-8): accent on the lanes meter and the agenda
  ruler, amber in `reldue_token` and the gantt chip — and kanban `today` is the same amber as
  `+1d..+7d`. Unify?
- **The remembered previous gantt group can be stale** (increment-005 code review F4): after a
  detour through another view it is the gantt's last group, and finishing a group's last task makes
  that empty group the previous one. Option: clear it when leaving the gantt.
- **An echo clipped on the opposite side still draws an edge bracket** (increment-004 code review
  F3): a due before the window draws `⟧`, a start past it `⟦`; for rest work `drawn` lacks
  "beyond". Unreachable through the app (the selection moves onto open work).
- ✓ done in `2026-10-02-batch-04` (HLR-402, `strip_controls` at the board, team and clipboard doors) — **Titles carry terminal escape sequences** (security L1, pre-existing): ESC in a board-file title
  reaches the terminal (only BEL/BS/VT/FF/CR are stripped); in team mode a teammate's file could
  inject sequences. Apply `_clean_clipboard_text`'s character rule when a board loads.
- ✓ done in `2026-10-02-batch-04` (LLR-401.2: every user/OS-text toast `markup=False`, no escape) — **`app.py` notifies prompt-typed ids and exceptions with markup on** (security S-5 of P2,
  pre-existing): `app.py` the setup id prompts and the team-sync failure — `[/]` raises
  `MarkupError`. Pass `markup=False`.
- **Cleanup:** `app._select_first`'s `group_of` is a fourth spelling of the gantt group key, `None`
  for the Inbox (increment-005 code review F3) → use `views.group_key`; the dead `HEAT` table
  (`views.py`, its `week ▒ accent`); the Setup colour guard's expression readability (increment-005
  F6); the AT-207 param ids `[size0-2]` (increment-006 F5); the lattice help bullet drops "not data"
  (increment-003 note).
- **Setup at 80×24 wraps its check notes onto the next line** (pre-existing, P4 walkthrough).
- **`team_filter_cycle` still has no key** (README audit #10) — the help names none now (D-219).

## Open — after `2026-10-02-batch-01` (gantt G-A + AX-2, colour budget on kanban/gantt, README)

- ✓ done in `2026-10-02-batch-03` (HLR-301..310, D-301) — **Batch A2 — readable kanban K-A + R-1b.** Two-row cards, one project band rule across
  columns, `┈` separators, DONE rail, adaptive widths; one board-wide `high` band on top capped
  with "+N more" (cap rule to be set at its P1). Split out of Batch A at P0 under the
  pre-authorized A1/A2 split (`2026-10-02-batch-01` US-105). Seed:
  `prototypes/kg_mejoras/variants_kanban.k_a(sep_mode="rule")`, `variants_reconcile` R-1b.
- ✓ done in `2026-10-02-batch-02` (HLR-201/202, D-201/202) — **Colour budget, app-wide.** Kanban and gantt panels are done; still accent: the other seven
  views' titles, the keybar key hints (`keymap.py` group hues), the ribbon clock, the setup
  hints. Operator questions carried with it (`2026-10-02-batch-01` §6.2): D4 today in accent
  vs the selection in accent (UX-7) · D10 a title colour that differs per view until this pass
  (UX-6) · D12 the gantt header's English beside Spanish help prose · D13 `━` shared by the
  critical chain and the selection echo.
- ✓ done in `2026-10-02-batch-02` (HLR-205/206) — **Operator questions, gantt.** D9 an above/below hint for a paged project (none drawn) · D14
  a cue (toast) when `]` finishes a task and it leaves the gantt.
- ✓ done in `2026-10-02-batch-02` (HLR-209) — **Weekend shading on the gantt ruler** (round-5 frames) — not shipped: off-palette background
  `#161d27`, not in the AX-2 commission (D5).
- ✓ answered and done in `2026-10-02-batch-02` (D5, UXV-2, UXV-3, PKT, SOON, HELP) — **Operator questions from the P4 walkthrough** (`2026-10-02-batch-01` `04-validation.md`): the
  approved AX-2 frame DOES shade weekends — ship it? (D5) · folding is accordion-style: moving
  the cursor or finishing a task can open/close projects above the cursor, so the highlight can
  move up on `down` (UXV-2) — keep, or keep a visited project open? · at a real 80×24 terminal
  Ops & Security folds although it holds the only task due today (UXV-3) — should "due today"
  weigh in fold order? · the flow packet `▬` shares the chain's bright tone · the kanban's
  ≤7-day `+Nd` now differs from later dues by a grey step only · help headings in accent.
- **The UXV-12 fix was not re-walked by the ux-reviewer** after `2026-10-02-batch-01`
  increment 004 round 3 (proven by its node and mutant H5 only) — glance at a focused gantt under a
  `/` filter that empties it at the next UX pass.
- **Inherited personal strings in committed state** (P5 privacy sweep, not introduced by
  `2026-10-02-batch-01`; byte-identical in `57a6075`): `.dev-flow/state.json` `owner` holds the
  absolute project path with the home folder (the flow writes it), and this file's git-identity note below carries personal
  e-mail addresses and the username on three lines. Operator decides whether to scrub.
- ✓ done in `2026-10-02-batch-02` (HLR-210) — **The ruler's echo for a task starting before the window** draws `⟦` at the window edge with
  no `◂` (UXV-7); the printed dates are right.
- ✓ done in `2026-10-02-batch-02` (HLR-202; the input border kept as the edited-field focus role, D-207) — **Accent outside the panels, undeclared until now** (UXV-9): the help modal's headings and the
  filter modal's input border — join the app-wide colour-budget pass.
- **`_strip` treats an escaped `\[` as a tag** (code review F5, pre-existing): a task or project
  name with brackets makes a gantt / lanes row — and a header row with a bracketed focus name —
  wider than the panel. Fix: measure plain text before markup, or skip escaped brackets in
  `_strip`; add a bracket payload to the width laws.
- **The help modal's right column (legend, example) cuts lines below ~118 columns, every
  view** (code review R1 of increment 004): `HelpModal` fixes `#help-left` at 48 cells and gives
  `#help-right` the rest of a 110-wide box — 56 cells at 118, 41 at 100, 22 at 80. Needs a modal
  layout decision (stack the columns when narrow, or wrap the entries); the gantt's own legend
  wording fits at 118 (TC-116).
- **Gantt panels under 3 rows** (code review F11, accepted limit): header + ruler take 3 rows, so
  a 1–2-row panel scrolls.
- **Setup's sync interval does not drive the sync timer** (qa D-4): Setup saves it to
  `team.json` `sync_tolerance_minutes` (staleness tone) while the timer stays at the
  constructor's 1800 s (`app.py:183`, `:341`). The README says what happens today.
- **README audit leftovers** (code / owner): #4 the in-app renumber notice text is stale
  (`app.py` "1 lanes · 2 agenda · 3 gantt · 4 kanban"); #10 `team_filter_cycle` is bound to no
  key — bind it or delete it.
- **Screenshots predate this release's colours**: `docs/taskboard-kanban.png`, `-lanes.png`,
  `-agenda.png`, `-ambient.gif` (README caption says so); `docs/taskboard-gantt.png` is no longer
  referenced (the README shows `docs/taskboard-gantt.svg`) — delete or regenerate.
- **Privacy tools do not decode HTML entities** (security S-8): `tools/privacy_sweep.py` and
  `tools/precommit_privacy.py` should read `html.unescape(text).replace("\u00a0", " ")` before
  matching; rich's SVG writes spaces as `&#160;`, so a multi-word board title in an SVG capture
  could pass unseen. RED test: an `.svg` holding `Alpha&#160;Beta…`. Until it lands, every
  batch close runs the entity-decoded sweep over `evidence/` and `docs/*.svg` by hand.
- **The operator's username is in older tracked files** (security S-5, accepted risk — a local
  account name, not a credential): `.dev-flow/state.json` `owner` and older batch evidence.
  Options: a repo-relative `owner` if the flow allows it; a one-time redaction pass over
  `.dev-flow/**`. History rewriting not recommended.

## Open — after `2026-09-30-batch-01` (edit window C + kanban K4/badges)

- **Legend ghosts under matrix and project focus.** `legend_entries` takes no
  presentation/focus, so in matrix (no cards drawn) and under a project focus it
  can list a `!!`/`==`/`++` badge no card draws. Inherited from the old `!`
  entry. Fix needs `presentation`/`focus` threaded from `app.py` through
  `HelpModal` into `legend_entries`.
- **Owner question: badges outside the kanban.** The Focus review rail and the
  People view still mark high priority with `!` in ink (`card_cell` without
  `badge`).
- **ProjectModal is still the old crowded modal** (out of scope by commission).
- ✓ done in `2026-10-02-batch-04` (HLR-401: 58 sink sites and 15 parser calls converted to Text pieces, a derived census TC-401..406) — **Security S1, the remaining sites (MEDIUM).** Fixed in the editor preview,
  `TaskDetails`, `image_block` and the `ImageViewer` title (batch
  2026-09-30-batch-01, increments 001/003). About 13 other sites in
  `modals.py` still hand `escape()`d user text to Textual as a str (Select /
  Option labels, confirm/prompt titles, `notify`, standup title/phase) — wrap
  them with `_rich` and extend `tests/test_details_markup.py`.
- ✓ done in `2026-10-02-batch-04` (HLR-403: a scoped rule; PV-1 provisional, UX-3 / UX-4 open to the operator) — **`TaskDetails` info grid paints blank (pre-existing).** Project / phase /
  priority / start / due labels in the `.modal-grid` render no cells (seen on
  the base tree too, textual 8.2.8).
- ✓ done in `2026-10-02-batch-04` (HLR-402) — **Security S2 (LOW).** ESC / C1 bytes in notes survive `_highlight_markup`;
  strip C0/C1 (keep `\n`, `\t`) once at load/sync.
- **80-column kanban titles are 1–10 characters** after the badge (−3 per
  normal/low card, −1 per high). Watch for a request to shed the badge first.

## Open — after `2026-08-07-fastflow-07`

- **`chrome` is 3.1 %, not 0.0, and 3.1 % of it is a LIE.** `_census`'s frame
  set contains `─`, and the gantt now draws a project's span with it, so data
  ink is counted as furniture. The law (`chrome < 10.0`) passes comfortably and
  was NOT amended — splitting the two rules moved most of those cells to `╌`
  and made the amendment unnecessary. Left as-is deliberately; re-open if a
  future design pushes chrome near its ceiling, because the number will run out
  before the furniture does.
- **The pulse's ration has no UI.** A reader who never sees a circle breathe
  cannot tell "nothing is behind" from "the feature is broken". The legend names
  the resting `●` only.
- **`PULSE_PHASES` is a palindrome and that hides arithmetic.** Any future law
  written against the shipped glyphs will be blind to a tick multiplier the same
  way this batch's first version was. The lesson is local to this constant and
  is recorded in `test_the_pulse_rides_the_ONE_shared_clock_and_clears_the_floor`.

## Shipped — batch-10 (`0cf0e72`, 2026-08-29)

- **US-A transitions log:** append-only `history.jsonl` sidecar, hooked into
  `set_task_phase` and `add_task`, never raises.
- **US-B flow view:** key `7`, cycle time per phase, phase×week heatmap,
  weekly throughput, honest empty state.
- **US-D dependency intelligence:** blocking a task creates/links a blocker
  task (`depends_on`), `⛓N` token, `unblock` sort, gantt critical chain
  highlight.
- **Deferred:** US-C desk loop remains cross-repo and out of scope for this
  batch.
- **No new carry-overs.** All batch-10 acceptance tests pass (1024 total);
  mutation evidence recorded in `.dev-flow/2026-08-24-batch-10/PLAN.md`.

## Shipped — batch-11 (`2eda873`, 2026-09-01)

- **US-T1 sync core:** `taskboard/team_sync.py` with `TeamState`
  (load/push/pull/sync), one file per person (`board.<user>.json`),
  `team.json` authority, first-run identity picker, daemon cadence, staleness
  helper; personal tasks never leave the machine.
- **US-T2 team views:** V3 standup strip (key `8`) and V2 people lanes
  (key `9`) with `todo · equipo · personal` classification filter; foreign
  cards carry read-only marks.
- **Deferred:** V4 project report, V5 per-project templates, V6 batch-email,
  V7 task chains + day-shift cascade.
- **No new carry-overs.** All batch-11 acceptance tests pass (1290 total);
  mutation evidence recorded in `.dev-flow/2026-09-01-batch-11/PLAN.md`.

## Shipped — batch-12 (`3a11eb0`, 2026-09-01)

- **US-S1 initial sync on mount:** configured identities sync immediately on
  mount, before the daemon's first tick.
- **US-S2 in-app Setup:** full-screen Setup view on key `0`, editable shared
  directory / sync interval / identity / shared projects / roster, advisory
  health checks, `ctrl+s` commit, `esc` discard.
- **US-S3 per-view help family:** `?` opens `HelpModal` for the active view
  (usage + live legend + example + keys); `m` opens the full keymap;
  `?` inside help opens the command palette.
- **US-S4 keybar per-view law:** new `bar` flag on `Key`; global commands
  (`o`, `i`, `p`, `P`, `f`, `c`, `R`, `S`) are bound but palette-only; the
  footer shows only view-local + universal keys.
- **No new carry-overs.** All batch-12 acceptance tests pass (1298 total);
  mutation evidence recorded in `.dev-flow/2026-09-01-batch-12/PLAN.md`.

## Open — after `2026-08-07-fastflow-06`

- **`main`'s HISTORY WAS REWRITTEN on 2026-08-07 — and that did NOT fully close
  it.** Operator reversed the earlier "ni hablar" ruling as a deliberate
  exception, on the grounds that this repository is where the rule was learned.
  All **119 commits** were rewritten with the same synthetic names the tip
  already carried, prefix-aware to 10 characters; verified commit-by-commit with
  `tools/privacy_sweep.py`: **119/119 clean, 0 leaking files**. The tip's tree is
  byte-identical to the pre-rewrite tag — the code did not change, only the
  history. Force-pushed with `--force-with-lease`.

  **WHAT REMAINS, MEASURED AFTER THE PUSH, NOT ASSUMED.** The old commits are
  still reachable on GitHub by SHA: `eec3c8c`, `694f38a` and `ec8c940` all
  answer the API, and the leaked file downloads (2 545 bytes) at `694f38a`.
  They are not linked from anything and cannot be found by browsing, but "hard
  to find" is not "gone". Two things actually close it:
    1. **A GitHub Support request** to purge cached views and unreachable
       objects — the documented remedy, and the operator's to file.
    2. Making the repository private, which cuts anonymous API access
       immediately.
  Until one of those, treat the old SHAs as public.

  **The local tag `pre-rewrite-20260807` still holds the pre-rewrite history**,
  including the leaked strings. Kept on purpose as the safety net for a
  same-day rewrite; delete it once the operator is satisfied.

- **The global git identity still carries the address.** Repo-local is set
  (`46639531+jav201@users.noreply.github.com`, verified on `5057c6a`); the
  global remains `jjgh89@msn.com`, deliberately untouched — changing it retags
  every repository on the machine, including ones whose remotes may require a
  verified address. One line when wanted:
  `git config --global user.email "46639531+jav201@users.noreply.github.com"`
- **The gate is local only.** `--no-verify` bypasses it, as it bypasses every
  hook, and a fresh clone must run `git config core.hooksPath .githooks` (a test
  says so rather than leaving it silent). A server-side or CI equivalent was NOT
  built.
- **`prototypes/` and `_prototypes/` now co-exist** on `main` after the merge.
  Not a defect, but two directories with the same purpose and different
  vintages is a decision waiting to be made.
- **8 more app symbols are still imported by `prototypes/kanban_variants.py`**
  (`HEX`, `blank_line`, `bottom`, `fill_height`, `fit`, `header`, `line`,
  `phase_buckets`, …). Two of them broke on this merge and became local copies;
  the rest are the same exposure, unbroken so far.
- **A stale worktree registration `clipboard-fix`** could not be pruned by
  `git gc` (permission denied on `.git/worktrees/clipboard-fix`). Harmless,
  cosmetic, and it will keep printing an error on every gc.
- **`docs/sample/report-example.html` is clear but ungoverned** — synthetic
  today, with no law tying it to a fixture. `taskboard/report.py` is the writer
  to watch.

## Superseded — the privacy work as it stood before the merge

- **`main`'s HISTORY still carries the operator's board data.** `caa4bab` and
  `ff733ec` are clean and `6083c01` is clean, but `694f38a` and every commit
  back to `5ae4d42` (2026-07-24) still contain **two project names and one task
  title** from the operator's board in
  `.fast-dev-flow/archive/20260724-025459-spec.md` — not quoted here, because
  AC6 forbids this file from carrying them and writing this entry tripped that
  law on its first draft. Run the sweep to see them. **This remote is PUBLIC.**
  `git log -S` finds them in 6 commits. Excising them needs a history rewrite
  and a force-push — the operator's call, and GitHub retains unreachable
  objects for a while afterwards, so forks and caches are not covered by it
  either. **Verified by `tools/privacy_sweep.py` over every commit in
  `7de3ad6..caa4bab`.**
- **`kanban-variants` is NOT merged, deliberately.** Attempted and aborted:
  **80 files / 44 132 insertions**, 4 conflicts, and it would create
  `prototypes/` alongside the existing `_prototypes/` while resurrecting the
  inline `HelpScreen` that `taskboard/keymap.py` replaced. The operator ruled
  against merging on 2026-08-07 and the measured scope confirms it. **The
  portable part — the detector — was cherry-picked instead** (`6083c01`). If
  anything else from that branch is wanted, it is a cherry-pick, not a merge.
- **The operator's name and address remain in every commit's AUTHOR metadata.**
  Accepted by the operator for existing commits; he asked that it not appear
  going forward. That is a git identity change (a GitHub `users.noreply`
  address), **operator-level config, not a repo change — NOT DONE HERE.**
- **`docs/sample/report-example.html` was cleared, not fixed.** It is synthetic
  (fixture vocabulary, 0 verbatim matches) but there is no law tying it to a
  fixture, so a regenerated sample could quietly come from the live board.
  `taskboard/report.py` is the writer to watch.
- **The sweep is a command, not a gate.** Nothing runs `tools/privacy_sweep.py`
  against the real board automatically, by design — but that means a leak is
  caught only when someone runs it. A pre-commit hook is the obvious next step
  and was NOT built.

> **The header sat at `eec625b` / 2026-07-31 for a whole day of shipping.** The
> close step that owns this line did not run when batch-02 closed, which is the
> failure the carry-over contract exists to prevent, and it is now the second
> recorded instance (the first: 2026-07-20 operator audit, ~10 batches stale).
> Nine commits are reconciled below at once; a backlog read between those dates
> would have reported an empty queue that looked like "nothing pending".

## Shipped

- **DONE** · `2026-08-07-fastflow-07` — **the gantt gets a line and a rationed
  circle.** Progress stops being a second shaded row and becomes one cell on the
  span; the freed row goes back to the tasks (at 104x28 with 5 projects / 21
  tasks the old shape **hid 4**, this one hides none). Span `─` solid, task `╌`
  dashed, phase tips `○◔◑◕`. The circle **breathes only where the work is behind
  its calendar** — same clock, same >= 2 s floor, no colour moves, and a board
  with nothing behind it is completely still. **776 green.**
  (`9601e84`, `b7e47b8` — local, **not pushed**)
  · *Six defects the harness found and review would not have — including a law
  that could not see a private tick multiplier because the breath's glyph
  sequence is a palindrome, and a pre-existing aliasing bug in
  `test_backlog_bar_is_static_across_ticks` (tick 0 vs 7 on a seven-cell reach)
  that had been passing for the wrong reason. Full list in
  `.fast-dev-flow/spec.md` §10.*
  · *The planned census amendment (O-1) was never made: splitting the two rules
  moved chrome 5.0 -> 3.1 and `marked` 67.8 -> 69.8 on its own.*

- **DONE** · `2026-08-07-fastflow-06` — **the branch lands and the gate goes
  up.** `kanban-variants` merged (80 files / 44 132 insertions, 4 conflicts each
  resolved toward `main` with a stated reason); a **pre-commit hook** that reads
  the INDEX, refuses a commit carrying board data, and **fails closed** when it
  cannot read the board; the repo-local author address moved to GitHub
  `users.noreply`; and the four backup refs deleted after the merge was green,
  verified by object id — the 19 077-byte blob holding 25 real task titles no
  longer exists locally. **767 green.** (`ecde0da`…`5057c6a`, local — **not
  pushed**)
  · *The merge's real cost was NOT in the conflicts: git auto-merged into 31
  failures. The worst was invisible in any diff —
  `prototypes/kanban_variants.py` monkeypatched `views.render_kanban` AT IMPORT
  TIME, so importing a prototype rewrote a shipping function for the whole
  process (22 unrelated failures, green in isolation). The auto-merge had also
  taken the branch's `m` binding into five of main's modal tests while the app
  binds `P`.*

- **DONE** · `2026-08-07-fastflow-05` — **the live board becomes unreachable
  from anything committable.** `tools/privacy_sweep.py` + 8 tests, matching
  truncated forms down to a stated 10-char floor because the failure that
  happened was a name reaching a file ONE LETTER short through an ellipsising
  label column — a first hand scrub replaced the whole token and called six
  rewritten commits clean while all six still carried it. Tested against a
  planted leak in both directions, 7 mutations all killing. Executed: main's
  tracked tree 99 files / 0 leaking. `tests/test_requirements.py` widened
  (hand-written first-party tuple → discovery; `tools/` had been outside its
  sweep entirely). **739 green.** (`6083c01`, local — **not pushed**)
  · *Three defects the flow caught that the hand work had not: the truncated
  residue in 6 commits; the batch's own spec quoting a real task title; and
  the detector's own test file using three real project names as fixture
  constants — invisible to its first sweep because the file was still
  untracked. Two of the batch's own tests were vacuous on their first mutation
  run (`board_strings` sort order, and `git check-ignore` answering from the
  INDEX so every `.gitignore` negation went untested).*
  · *Branch-side work — capture scripts, the widget constructor, the scratch
  `.gitignore` — landed on `kanban-variants` (`f5f0e81`, 164 green), which is
  NOT merged; see above.*

- **DONE** · `2026-08-06-fastflow-04` — **the gantt gets its gauge.** The three
  parts of the approved prototype that never shipped when its texture did
  (`81dcb66`): a 2-cell `GUTTER` so a truncated title stops touching its own bar
  (measured 0 cells of separation on 5 of 5 long-title rows at 104x30 / 102x16 /
  96x30 / 120x40, now >= 2 at all four); a **week guide** `┆` at every monday
  column and **month names** on the bottom axis beside the day figures; and
  `FIELD_REACH` `█` -> `━`, so a project span is a rule instead of a slab.
  Occupancy improved (`dead` 23.1 -> 21.5 %, `marked` 76.9 -> 78.5 %, chrome
  still 0.0); span economy 135 -> 155 runs against a 594.7 ceiling. 5 new tests,
  **730 green**, 9 mutations each verified to redden their predicate.
  (local commit — **not pushed**; see `.fast-dev-flow/spec.md`)

- **DONE** · Prism increment 1 — the colour ration: four colliding project hues
  retired (amber 0.0 / cyan 48.3 / orange 51.0 / rose 63.8 from a reserved hue),
  deterministic injective remap on load, high-priority marker moved from the amber
  `◉` to the neutral glyph `!`. 15 new tests, 152 green, 4 mutants killed.
  (`a06a635` — see `.fast-dev-flow/spec.md`)
- **DONE** · Prism increment 2 — `taskboard/wave.py`: the REV2 dot engine ported
  as a pure, view-independent module (2x4 dots per cell, braille packed last,
  carve/notch, 4x7 font). Behaviour verified identical to the proposal's module
  over 400 randomized differential trials. 16 new tests, 168 green, 4 mutants
  killed. **No view imports it yet — that is increment 3/4.** (this batch)
- **DONE** · R5 (render cost of the field) — **measured**, no optimisation done:
  at 96x30 with the proposal's L-step geometry (68-day window, leader bench 10
  rows), the engine costs **1.37 ms (calm) / 1.84 ms (typical) / 2.24 ms
  (extreme)** per frame for 748 / 952 / 1156 braille cells. Against increment 6's
  700 ms ambient tick that is 0.3 %. Engine only — markup, styling and Textual
  compositing are NOT in these numbers, so the view's real cost is still unmeasured.

- **DONE** · Prism increment 3 (roadmap row 2) — the shared day axis + field
  lattice as pure helpers (`field_geometry`, `day_col`, `off_window_glyph`,
  `field_rows`); the clip/flag vocabulary finally gets a MARK. 14 tests,
  182 green, 4 mutants killed. (`d3061e4`)
- **DONE** · Prism increment 4 (roadmap row 3) — the new lanes row replaces the
  two per project; scale row; nav follows what is drawn. 18 tests, 202 green,
  5 mutants killed. (`f433e19`)
- **DONE** · Prism increment 5 (roadmap row 4) — pressure ranking, leader's
  bench with its carved count and `◆`, resting row, height allocator, "+N not
  shown". 25 tests, 207 green, 5 mutants killed — **three of which were vacuous
  on the first run and were fixed**. (`f3509ea`)
- **DONE** · Prism increment 6 (roadmap row 5) — momentum: `Task.phase_changed`,
  `Board.set_task_phase`, `days_in_phase` (None = unknown, never zero), the
  lead's `Nd in phase · N unaged` figure. 13 tests, 219 green, 4 mutants killed.
  (`e9f36be`)
- **DONE** · Prism increment 7 (roadmap row 6) — the ambient: the today rule
  rotates through 4 glyphs on the app's one shared clock; nothing else moves and
  no colour changes. 7 tests, 226 green, 4 mutants killed. (`0b635e3`)

## Open — Prism roadmap

**Nothing.** Rows 1-6 of `_tui_prism_proposal/PROPOSAL.md` §9 are all shipped.

## Open — findings raised while shipping increment 1

- **`ribbon.py:49` paints the ISO week number in `amber` (#fbbf24)** — the reserved
  *due today* hue worn by a mark that is neither identity nor severity. Same class
  of collision the ration just fixed, one file away. Small, self-contained.
- **`views.py:177` paints the image indicator `▤` in `sky`** — `sky` is an
  *identity* hue (a project colour), so a task attribute is wearing the house that
  names projects. Decide: move it to a neutral tone, or accept and document.
- **The `!` marker is per-card only.** The proposal's `!N` aggregate (count of
  high-priority open tasks per project) belongs to the new lanes row — increment 3.
- **Columns / agenda / gantt render no priority at all.** Not a regression (they
  never did), but if priority matters at a glance, three of five views omit it.
- **`sky` survives the ration by 7.4 units** (62.4 vs the 55 accent band). If
  `accent` #2dd4bf is ever retuned, re-run the oracle in `tests/test_palette_ration.py`.
- **`modals.py:322-324` would raise `InvalidSelectValueError`** if an in-memory
  `Project` ever carried a retired hue (only reachable by constructing `Project`
  directly in code — the loader always returns a lawful hue). Left unguarded on
  purpose; revisit if any code path starts building projects from raw data.
- **`.venv` cannot run the suite** — `ModuleNotFoundError: No module named 'PIL'`
  makes 5 image tests error there; the suite is green under system python. Either
  install Pillow into `.venv` or mark those tests as requiring it.

## Open — findings raised while porting the wave engine (increment 2)

- ~~`taskboard/wave.py` is imported by nothing but its tests.~~ **RETIRED** —
  `views.field_rows` draws with it as of increment 3.
- **`field_geometry` does not fit below 32 columns** (increment 3, measured and
  pinned by `test_the_ported_geometry_does_not_fit_below_32_columns`): `field_w`
  has a floor of 8, so at 24-31 columns label + field + figures exceed the width
  by 32-w cells. Inherited from the proposal's `Geo`; harmless while no view
  calls it, and it must be resolved by whoever wires the lanes row at MIN_WIDTH.
- **The proposal's §4.1 budget table says the L step shows a "68-day window";
  the code shows 134 days** (67 field cells x 2 days per cell). The table counts
  cells, the code counts days. Code governs; the table is wrong.
- **`carve_text` carries prototype-grade edges, kept for port fidelity:** its
  returned width includes the trailing inter-glyph gap (`"40"` -> 10, not 9), the
  loop index `i` is unused, and the returned height is the constant 7 rather than
  the glyph's real extent. Behavioural changes, so they were NOT "cleaned" —
  decide deliberately when a caller exists.
- **The engine has no clip/flag vocabulary of its own.** `verify_prism.py` law 12
  ("a date beyond the window is FLAGGED, not clamped") lives in the prototype's
  `Geo`, not in `wave.py`; increment 2's helpers must carry that, not the engine.

- **DONE** · The occupancy harness — `tests/test_occupancy.py` measures the
  rebuilt lanes view by AUDIT.md's own method at its own reference size and
  compares against its numbers. 11 laws, 235 green, 3 mutants killed.

- **DONE** · The world-city catalog — `CITY_ZONES` 75 -> 340 cities / 243 zones,
  all 40 UTC offsets in use covered, every zone resolved through `zoneinfo` by
  the test suite; `resolve_city` is accent-blind on a fallback. 14 laws + 1 app
  test, 250 green, 5 mutants killed. (`9ed055b`)
- **DONE** · Gantt ordering + auto-archive — open work first, done work at the
  tail; `AUTO_ARCHIVE_DAYS = 20` sweeps long-finished work into the existing
  `archived` flag at startup, but only when the completion date is KNOWN.
  16 laws, 266 green, 5 mutants killed. (`db31a5c`)

- **DONE** · The key-bar contract — `taskboard/keymap.py` is the one seat;
  `BINDINGS` and the bar are both generated from it. Replaced Textual's `Footer`,
  which mounted zero children and painted a BLANK row while 24 bindings were
  live. 17 laws, 283 green, 6 mutants killed. (`68e85b4`)

- **DONE** · REV5 #17 columns retirement (`17c705b`) · #18 lanes due meter
  (`c3ff23d`) · #19 gantt meter + field titles (`52349ff`) · #20 agenda laws
  (`889e812`) · #21 the `?` legend (`0259948`). 320 green.
- ~~Until a legend key exists, `+N` is the fallback below ~50 columns.~~
  **CLOSED** — `?` ships declared `universal=True`.

- **DONE** · REV5 #22 — the 17 prototype laws reconciled into the suite under a
  disk-checked MANIFEST; attribution and register ported; the register law found
  a real second-person string in the app's voice. (`90a7f4f`)
- **DONE** · The gantt FIELD redesign (REV3) — two bands, the slip as a length,
  an axis with a past. **Carrying 71.4 % at typical (target 71.1 %) and ink now
  MONOTONE: 25.0 % -> 25.9 % typical to extreme, where the old view inverted
  23.3 % -> 21.0 %.** Chrome 21.2 % -> 7.8 %. (`c17dded`)
- ~~The gantt's field redesign is not done.~~ **CLOSED** by `c17dded`.

- **DONE** · The frame removed — the closure law is GREEN and chrome is 0.0 % in
  lanes and gantt. Marked +2.5 points at typical and extreme (the extreme margin
  over the 45 % floor went 2.4 -> 4.9). (this batch)
- ~~The closure law stays red.~~ **CLOSED.**

- **DONE** · The deliberate one-time archive (`X`) + archive from the task
  editor. Closes the "auto-archive does nothing on the operator's board" carry-over:
  the timer owns dated work, `X` owns everything older, and neither invents a
  date. 12 laws, 343 green, 6 mutants killed. (this batch)
- ~~Auto-archive does nothing on the operator's existing board, by design... he must
  archive them by hand — or we add an explicit, opt-in one-time action.~~
  **CLOSED**: that action is `X`.

- **DONE** · The board report (batch `2026-07-31-batch-02`) — self-contained HTML,
  whole board or one project, `R` in the app and `taskboard --report [PROJECT]`.
  Read-only by law. 18 laws, 363 green, 8 mutants killed. (this batch)

## Open — raised by the report batch

- **Increment 22b (REV6's spend ladder) is APPROVED AND QUEUED** — the allocator
  prohibition, the lattice behind title rows, the absence line. The prototype's
  `law_spend` is already in `verify_prism.py` and is recorded QUEUED in the
  prism-laws manifest. REV6 also carries its own open defect to check for in the
  app: extreme sat 0.5pt below typical in marked cells (an ink-monotone violation).
- **The report has no `--format svg`.** Struck deliberately in the spec (an SVG
  container cannot reflow); if a single pasteable figure is ever wanted, it is a
  small follow-on, not a redesign.
- **The report is not linked from the app's legend.** `?` explains marks in the
  views; it says nothing about `R`. Minor, and arguably correct — the legend is
  about marks, not actions.

## Open — process / operator actions

- **DONE** · **`/dev-flow-sync` for batch `2026-07-18-batch-01`** — run 2026-07-31 on
  the operator's authorization, 13 days after the batch closed. The four phase artifacts
  plus `06-docs/` (9 files) are now in the vault at
  `G:\My Drive\ConsultIA\Obsidian_Vaults\AI-Consulting-Brain\01 - Proyectos\taskboard\dev-flow-batches\2026-07-18-batch-01\`,
  with a frontmatter-carrying `2026-07-18-batch-01-README.md` index and a project
  `Dashboard.md`. This created the vault's `taskboard` project folder — it had none.
  `03-increments/` deliberately not synced (vault convention since batch-04), so the
  increment records remain repo-only. Folder named from the artifacts' own
  self-identification, NOT `state.json`'s `batch_id` — see the state.json note below.

## Open — raised by the report batch's Phase 0 (measured)

- **The 8 project hues fail as a CATEGORICAL palette — identity-vs-identity was
  never measured.** The colour ration checked every identity hue against the hues
  that JUDGE (>=70 from over/soon, >=55 from accent) and never checked the identity
  hues against EACH OTHER. Run through `dataviz/scripts/validate_palette.js` on
  both the dark surface (`#0d1117`) and light:
  - `fuchsia #e879f9` vs `violet #a78bfa` — **dE 0.4 for protanopia**: identical to
    a red-blind reader.
  - `violet #a78bfa` vs `indigo #818cf8` — **dE 5.4 normal vision**, against a floor
    of 15: hard to tell apart *with full colour vision*.
  In the TUI this is survivable (a project is also its row, its spine and its name),
  which is why it never surfaced. It would NOT be survivable in a chart that encodes
  a project by hue alone — hence the report's design rule (direct labels + a table
  view, never hue-alone). **Fixing the palette itself is a separate decision**: it
  means re-stepping two of the eight hues and remapping existing boards, exactly the
  cost the original ration paid.

## Open — raised by the one-time archive

- **`x` cannot undo itself from the board.** Archiving hides the task, so the
  selection moves on; bringing it back is `v` then `x`. Correct but two-step,
  and now the confirm text says so explicitly. If it trips people up, an undo
  toast on the archive notification is the small fix.
- **The purge is board-wide.** There is no per-project variant; `P` archives a
  whole project but not "this project's finished work". Nobody has asked.

## Open — raised by removing the frame

- **Most of the reclaimed 7.6 % became DEAD, not marked.** The frame was on the
  perimeter: the content gained two columns (~0.5 points) and the spent bottom
  row gave +2.5, but the rest is blank space nothing has been designed to use.
  It is available headroom, measured and unspent.
- **Box-drawing survives in two places, deliberately**: kanban's phase-column
  dividers (chrome 4.4 %) and the agenda's "no date" section rule (7.3 %). They
  are internal structure — they say WHICH column and WHICH group — not an
  enclosure. Whether the closure law should eventually reach them is a design
  question, not an oversight.
- **`calm` is now 65.5 % dead in lanes and 74.8 % in gantt.** Removing the frame
  raised both, since a quiet board has nothing to put in the reclaimed cells.
  Same honest weakness the proposal records for calm.

## Open — raised by the gantt field redesign

- **The closure law stays red** (`test_the_closure_law_is_knowingly_unmet`): all
  four views still draw a box. The gantt's chrome fell from 21.2 % to 7.8 % by
  removing the divider rows, so what remains IS the frame. Removing it is now
  the single largest occupancy win left in the app.
- **`calm` gantt is 67.8 % dead.** The two-band field needs data to fill; a
  near-empty board has little to draw. Same honest weakness the proposal records
  for calm lanes.
- ✓ done in `2026-10-02-batch-01` (projects fold; nothing hidden while folding holds it): **The gantt sheds rows at short heights** and counts them (`+N not shown`),
  which the old view did not do — it simply drew fewer. Consistent with lanes
  now, but it is a behaviour change worth knowing.

## Open — raised by the REV5 roadmap

- **REV5 #22 (the 90 laws ported to `tests/`) was NOT attempted** — it was not
  in the approved list.
- **The gantt's field redesign is not done.** #19 ported the RULING (meter at the
  edge, titles over the field, one severity seat) onto the existing week-grid
  gantt. The frames show a lanes-style dot field with compact marks near each due
  date; that is a separate redesign and is not claimed.
- **The proposal's title targets did not transfer**, in three views: its numbers
  (lanes 77→83, gantt 11→33, agenda 12→19) describe a prototype whose titles were
  boxed inside a label column. Measured here BEFORE the pass: lanes 83-85,
  agenda 30, gantt 27. The freed width in lanes went to the FIELD (+6 L / +4 S)
  instead, and gantt titles now grow +6 per empty week in front of their bar.
- **Task rows in lanes lost 2 cells** to the meter (6 cells vs the `+12d` token's
  4) — the trade the proposal names explicitly.
- **At narrow gantt widths the percent drops and the meter stays** — a drop-order
  the proposal legislates only for the wide case.
- **The agenda's ink ceiling is nowhere near breached** (38.3 % vs 85 %), so the
  designed half-density reach lattice is deliberately NOT applied. Pinned by law
  so a future widening cannot cross it silently.

## Open — raised by the key-bar contract

- **REV5's remaining items are NOT started, by instruction**, pending the operator's
  review of the prototype: the `?` legend popup, the columns retirement, the
  meters, the title widths.
- **Until a legend key exists, `+N` is the fallback below ~50 columns.** Once `?`
  ships it must be declared `universal=True` so it sorts beside `q` and can never
  be the key that drops — the seat already supports it.
- **`o` (URL) and `i` (Images) are shown always but do nothing unless the
  selected task has one.** That is "live but a no-op", not a dead key, and
  hiding them would violate the standing instruction not to hide keys — but if
  the contract is ever tightened to per-selection state, they are the two
  entries that need a rule.

## Open — raised by the archive increment

- **Auto-archive does nothing on the operator's existing board, by design.** Every
  finished task there predates `phase_changed`, so its age is unknown and it is
  left alone (measured: a 30-done legacy board sweeps 0). If he wants the old
  ones gone he must archive them by hand (`x`) — or we add an explicit,
  opt-in "treat everything done before <date> as archived" action, which would
  be a deliberate one-time decision rather than a guess.
- **Reordering phases can make a task "done" while carrying an older stamp**, so
  the next start may sweep it. It cannot touch a legacy board (no stamp), but if
  phase reordering becomes common, consider re-stamping on `move_phase`.
- **The sweep runs only at startup.** A long-running widget will not archive work
  that ages past 20 days while it is open, until the next launch.

## Open — raised by the occupancy measurement

- **PROPOSAL §4.3's ">= 45 % marked at typical/extreme" is met at typical
  (45.4 %) and MISSED at extreme (44.7 %)** — by 0.3 points. Pinned by
  `test_the_proposals_own_45_percent_floor_is_met_at_typical_and_missed_at_extreme`
  so it cannot quietly widen. The frame alone costs ~7.6 %; removing it would
  clear the floor at both loads.
- **"Wider is worse" is reduced, not cured.** Stepping 72x24 -> 96x30 still adds
  dead space at typical (+1.3 points) and extreme (+11.1), against the old
  view's +10.9 and +15.9. Cause: named-task rows are short strings that gain only
  blanks as the widget widens, while the field is what spends width. A calm board
  now INVERTS (it gets better as it widens). Fix candidate: let a title row carry
  something on its right at wide sizes, or give the lead more bench rows instead
  of more titles.

## Open — raised while finishing the roadmap (increments 4-7)

- **The box frame and the `◆ TASKBOARD` header survive**, so PRISM's measured
  "0 % chrome" is NOT reached. The roadmap allocates no increment to the frame,
  so it was not mine to remove. Decide deliberately: the frame is ~2 columns and
  2 rows of every render.
- **The proposal's open items, untouched by design** (they are not roadmap rows):
  the Inbox is drawn as an ordinary lane rather than designed (R6 — it works, it
  just was never designed); only two size steps exist (S/L); and `calm` boards
  still leave a lot of empty field. Recorded, not solved.
- **The 21 laws of `verify_prism.py` were adapted, not ported wholesale.** Laws
  that measure the PROTOTYPE's composed frame (occupancy floors, tone histogram,
  ink percentages) have no meaning against the real app's framed render, so the
  laws about mechanism (resolution, carving, attribution, ordered coverage,
  clip-and-flag, motion) were reproduced in `tests/` and the frame-occupancy
  ones were not. A real occupancy harness for the app is still missing.
- ~~**`progress_bar`, `sparkline` and `_lane_junctions` are now unused**~~
  DONE: `_lane_junctions` had already died with the lanes rewrite; `progress_bar`,
  `sparkline` and `_SPARK` deleted (zero callers, zero test references, verified
  by grep). The README's view-2 line promised "throughput sparklines" that no
  code drew — corrected in the same commit.
- **The gantt's own `_flowing` animation and the lanes ambient now share one
  clock**, so a future change to `TICK_SECONDS` moves both. The motion laws read
  the constant, so the illegal-band failure will be caught, but the gantt's
  speed is not pinned by any test.
- **`sitting()` reports the lead only.** Every other lane's momentum is computed
  (`days_in_phase`) but not shown; a drawn stagnation channel remains open, and
  it now has data to draw from.

## Open — raised by the gantt gauge batch (`2026-08-06-fastflow-04`)

- **The week guide is dense, and its rhythm is irregular.** One cell is two days,
  so a week is 3.5 cells and the guides alternate 3 and 4 cells apart:
  `·┆···┆··┆···┆··┆`. It reads closer to texture than to a ruled gauge. It is the
  approved prototype's own density and it SHIPPED as approved — but if the operator
  reads it as noise, the cheap levers are a guide every fortnight, or guides only
  at month boundaries. **Decide with the render in front of you, not from this
  line.**
- ✓ done in `2026-10-02-batch-01` (the AX-2 ruler names every month band): **`AUG` is dropped from the axis whenever the month starts within ~3 cells of
  today.** The day figures are the anchors and a month that cannot stand clear is
  dropped whole (a half-printed month is a wrong date). At `TODAY = 2026-07-30`
  the axis reads `-48d  JUL  today  SEP  OCT  NOV +111d` — the month immediately
  ahead is the one you cannot see. Options if it matters: let the month win over
  `today` (it has the today RULE in the field already), or shorten the day
  figures.
- **`NOV +111d` sits with a single space between them** at 104 wide. The
  one-blank-either-side rule held, but it is tight; consider two.
- **`tests/test_gantt.py:121` is dead code** — `set(seg) <= {"⣿","⣤","⡄","⣀"," "}`
  tests the braille alphabet the field stopped using two batches ago, so the loop
  body never executes. Found while mapping the laws; NOT fixed here (out of
  scope). Same class: `tests/test_app.py:1542` (`assert "⣤" not in …`, trivially
  true).
- **`tests/test_app.py::test_win_clipboard_roundtrip` is flaky, not broken.** It
  failed on the first baseline run of this session (`Set-Clipboard` with no
  clipboard in a non-interactive shell) and passed on every run after. Worth a
  skip-marker when there is no clipboard, so a baseline count stops depending on
  which shell ran it.

## Housekeeping

- Untracked in the working tree, pre-existing and NOT part of this batch:
  `_tui_prism_proposal/` (a concurrent design agent owns it), `.claude/`, `.s19tool/`.
  Decide what to commit / ignore.

## From increment 22b — the REV6 spend ladder

- **A mutation battery can poison `__pycache__`.** M6 mutated `range(0, 4)` to
  `range(0, 1)` — the SAME number of bytes — and the restore landed inside the
  same second. Python keys a `.pyc` on (source mtime, source size), so both
  matched and the cache survived: the next full-suite run executed the MUTANT
  from a byte-identical working tree, 13 tests failing with no diff to explain
  them. The hash-verified restore is not sufficient on its own; the batteries
  must run with `PYTHONDONTWRITEBYTECODE=1`. Batteries live in `%TEMP%` and are
  rewritten per increment, so this is a habit to keep, not a file to fix.
- **A clause is not a signature.** `test_the_absence_line_yields_when_rows_were_shed`
  asserted `"nothing late" not in out`, but the shed fixture HAS late work, so
  the line reads "12 late" and the assertion held whether or not the line was
  drawn. Fixed to match the line's own shape. When asserting a thing is ABSENT,
  assert on text the thing always emits — not on the branch the fixture avoids.
- **`calm` misses REV6's dead-space number: 55.1 % here vs 50.9 % reported.**
  Typical (19.2 % vs 25 % ceiling) and extreme (ink-monotone) both hold, so the
  increment is accepted, but a nearly-empty board still spends more of the
  screen on blank than the design says it should. The third rung buys one row;
  the calm case has more than one row to spend.

## From the closure batch (increments 1-4)

- **`sitting()` beyond the lead: STOPPED, not implemented.** The data exists for
  every lane (`days_in_phase`), but there is nowhere lawful to put the figure. A
  stack row's free gap is **exactly 1 cell at every width measured** (60, 80, 96,
  120, 160) — the geometry expands the field to fill whatever the label and the
  meter leave, so `12d in phase` cannot be drawn without taking ~13 cells from
  the field of every project, permanently. Printing it INSIDE the field is worse
  than clutter: the field is a shared day axis, so a figure sitting at column X
  reads as belonging to that DATE.
  And the app's own order of loss already answers the question. `lead_band` sheds
  its right-hand block from the left and momentum goes FIRST, because "it is
  context" — on a row with strictly less room than the lead's, momentum is
  precisely the figure that does not survive. Drawing it anyway would need either
  a permanent field-width tax on every project or a new mark, and both are design
  decisions for the owner rather than defects to fix.
  **Open question if it is ever wanted:** is stagnation worth ~13 cells of every
  stack lane's curve? If yes, the honest form is the lead's existing figure in the
  lead's existing tone, and the field shrinks for everyone.

- **The identity-vs-identity collision is NOT curable at 8 hues.** Measured with
  the dataviz validator, `--pairs all`, both modes: the shipped palette fails
  three checks (violet↔blue ΔE 0.3 deutan; normal-vision floor 5.4 against a
  floor of 15). No subset of the current family passes at ANY size down to 5,
  because `Lightness band` fails listing all eight — the Tailwind-400 family is a
  tonal step too light for the surface, and it is crowded into the cool half of
  the wheel exactly because the ration reserved the warm half for severity.
  Searching a lawful pool (reference-theme slots outside the reserved bands), the
  ceiling for `--pairs all` in both modes is **four** hues. Even the dataviz
  reference theme fails all-pairs at 8 — its own docs claim only the *adjacent*
  pairlist — and 3 of its 8 slots sit inside the app's reserved bands.
  Mitigating fact: colour is NOT the sole identity channel here. Every project is
  named in text beside its bar, which is the secondary encoding the palette rules
  ask for. The failure is real but it is "two projects can share a colour", not
  "the board is unreadable".
  **DECIDED 2026-07-31 — Option A accepted by the operator ("Acepto la opción A"): the 8
  shipped hues stay.** The standing conditions of the acceptance: text remains a
  mandatory identity channel beside every hue-bearing mark (already law in the
  report: no figure encodes a project by hue alone), and this item is CLOSED — do
  not reopen the palette unless the hue family itself changes, at which point the
  all-pairs measurement above is the gate to re-run.

- **Two process findings, both from mutants that stayed green.** A test asserting
  a thing is ABSENT must assert on text the thing ALWAYS emits — `"nothing late"`
  passed whether or not the absence line was drawn, because the fixture had late
  work. And a motion test must use a fixture long enough to observe speed: over a
  two-cell reach, a packet stepping 3 and one stepping 1 are the same animation
  (3t mod 2 == t mod 2), so the first version of the gantt-speed law could not
  have failed.

- **`.gitignore` near-miss.** Rewriting it instead of appending dropped
  `board.json` — the rule that keeps a local copy of the real board out of the
  repo. Caught by diffing before the commit. Rewriting a tracked file without
  reading it first is the whole error; there is no second control that would have
  caught it.

## From the 2026-08-03 session

Nine commits, `a16608b`..`bd935ff`, all on `main` and pushed. Reconciled in one
pass because the header had gone a day stale (see the note at the top).

### Shipped

- **DONE** · **Run economy.** The board coloured cell by cell, so a 60-cell band
  left 60 `[#hex]…[/]` pairs. `Text.from_markup` was **88 % of render time**.
  `collapse_runs` + `to_text` as the one seam: gantt **139 ms → 0.3 ms** net per
  keypress, 2,880 → 302 segments, idle tick 4.9 % → 1.1 % of a core. Verified on
  the real board across 256 configurations, 0 mismatches. (`a16608b`)
- **DONE** · **Width is measured in cells.** `fit`/`clip`/`header`/`_pad` and ten
  callers used `len()` — codepoints, not cells. A title holding `:bug:` made its
  row 93 cells in a 96-cell view. `vis()` is now the only ruler; `set_cell_size`
  cuts on glyph boundaries. `emoji=False` is load-bearing (see the law below).
  New `tests/test_cells.py`, 213 cases, failed 136× against the old arithmetic.
  (`6ddc574`)
- **DONE** · **Ctrl+E emoji picker** in both text editors, inserting the glyph.
  (`efe6060`)
- **DONE** · **Tests stop reading the developer's live board.** `TaskboardApp()`
  with no path loads `~/.taskboard` and `on_mount` SAVES it. (`38ce312`)
- **DONE** · **The kanban rule crosses where the columns divide.** Headers split
  at 30/60/90, the rule crossed at 31/61/91 — a framed-era builder reserving
  column 0 for `├`. Also closed a hole in the closure law, which checked only
  `│` and so let `├`/`┤` survive the frameless pass. (`530a7a5`)
- **DONE** · **The emoji picker offers only unambiguous widths** — 1,483 of
  3,608. Every other class disagrees between rich and the terminal (ZWJ: 2 vs 4;
  variation selector: 2 vs 1; EAW=N/A: 1 vs 2). (`ccd4018`)
- **DONE** · **The gantt field draws in shade, not scatter** — braille bought
  sub-cell resolution a *span* does not need. Reach `█`, progress `▓`, task `▒`,
  half `▌`, phase tip as a rising fill. Lanes untouched. (`81dcb66`)
- **DONE** · **The right edge says the number** — `···▲3d` / `····4d` / `··done`
  / `·····—`. The bar stood for a BAND, so 4 days and 5 days drew the same two
  cells. Two laws reversed in place rather than deleted. (`e8dabba`)
- **DONE** · **Short content stays at the top** — `fill_height` pinned the last
  row assuming every view closes with an axis; the kanban and the agenda close
  with a TASK, so 84 kanban and 44 agenda sizes stranded a row at the bottom of
  the viewport. An axis is now declared. `tests/test_vertical_fill.py`,
  mutation-checked against both ways of breaking it. (`bd935ff`,
  `.fast-dev-flow/spec.md`)

### Open — carried from this session

- **Lanes geometry off-by-one.** `lane_geometry(120, …)` reports
  `today_cell = 44` while the today rule is drawn at column **43**, and
  `label_w + field_w + figs_w = 119` against a width of 120 — one cell
  unassigned. Not yet decided whether it is a defect or deliberate
  compensation; **no view misrenders because of it today**, which is why it was
  reported rather than "fixed" blind.
- **`test_win_clipboard_roundtrip` is flaky.** Its restore step
  (`Set-Clipboard -Value $prior`) raises `PositionalParameterNotFound` and leaves
  the clipboard in a state that fails the *next* run. Bug in the test, not the
  code; pre-existing.
- **The gantt meter vs the field speak two alphabets.** The right-edge reading is
  now text, but `due_meter` is shared with the lanes, so any further change to it
  moves both views. Deliberate boundary, recorded so the next reader knows it was
  a choice.
- **`emoji=False` is load-bearing and easy to "fix" wrongly.** Re-enabling
  substitution to support `:shortcodes:` turns
  `test_a_shortcode_is_drawn_as_itself_not_as_a_glyph` red *and* the row-width
  invariant with it. Whoever wants shortcodes must substitute BEFORE the width
  math (13 sites where user text enters the views), not after.

### Open — process (not this repo)

- **`~/.claude/docs/FLOW-VERSION.md` is stale by one control.** `f3d4fba` added
  **C-46** to `dev-flow-lessons/SKILL.md` (641 lines vs the 620 recorded) and is
  already pushed, but the manifest still declares `controls: C-1 … C-45` and the
  pre-C-46 hash. 11/12 files verify byte-for-byte; the twelfth is the manifest's
  own bookkeeping. Per its own rule — "if you edit a flow file, you own the bump"
  — this needs a rev2. **Different repo (`claude-config` + `claude-skills`), so
  it is not fixable from this batch's commit.**

## From 2026-08-03-batch-03 (CLOSED AT PHASE 2, nothing implemented)

The batch derived a full requirement set for "lanes row states its demand; the curve moves to a
disclosure row" and closed without code. `taskboard/` and `tests/` are byte-identical to `f237cb3`.
Full account in `.dev-flow/05-postmortem.md`.

### The next batch, and it is deliberately small

- **DONE** (2026-08-06, `/fast-dev-flow`) · **FIX AND VERIFY THE ROW COST MODEL, ALONE, WITH NO VISUAL CHANGE.** Every substantive
  disagreement across two iterations reduced to `room` / `prof` / the lead band's ±2. There is no
  single verified cost model, so each agent measured against its own and the conflicts only
  surfaced when a later agent re-derived an earlier one's number. Establish one — executed, pinned
  by a test, with `views.py:2127`'s `h - 2 - (2 if active else 0)` and `lead_band`'s `prof + 2`
  reconciled explicitly — and the rest of the design becomes row substitution.

### The design, decided and still standing (do not re-litigate)

- **Mechanism D in the project row** (`N open · ▲N late · next Nd`), **mechanism A on the
  disclosure row** (the cumulative curve). Operator-decided after seeing A/C/D rendered on the real
  board; C was rejected as answering the least actionable question.
- **Option (a)** pays for the disclosure row: the focused project sheds one title.
- **O-1: silent refusal** when the shed cannot be paid.
- **O-2 refined to option 2:** supersede `tests/test_spend.py:81` and `:277`; **REPLACE** `:238`
  with an explicit ceiling on `prof` — its subject (an upper bound on `prof`) survives the change.
- **O-3: no share cap.** ⚠ **Ruled on an understated number** — the operator was told 87 % of the
  panel; the band is `(prof+2)/h`, so it is **90 % at h=60 and 95 % at h=120**. The ruling's logic
  (the panel has only two sinks for surplus) is unaffected, but the next batch must re-present it.
- **O-3 RULED 2026-08-06: no share cap, confirmed after the correction.** The operator was
  re-presented the corrected figures — the band is `(prof+2)/h`, so **90 % at h=60 and 95 % at
  h=80**, not the 87 % he first ruled on — *and* the finding that this share is **already shipped
  behaviour on HEAD** (a calm board's bench is 93.3 % at h=60 today, driven by how many active
  lanes exist, not by `wrows`). He kept the ruling. Rationale on the record: the panel has only two
  sinks for surplus, the bench stops informing past ~4 rows (distinct column heights saturate at
  `prof = 3–4` and are unchanged through 52 while lit dots grow 16×), and the measured alternative
  `(2·room)//3` buys a 58–64 % bench for **51 blank rows over 24 renders** — retiring the shipped
  "never pads" law to install another.
- **O-4 RULED 2026-08-06: the view reports what it drew.** `render_swimlanes` returns what it
  actually drew through an out-parameter of the same kind as `line_map`, and `legend_entries` reads
  that answer. Costs four signature changes; the 8 existing call sites keep compiling on a `None`
  default. Both alternatives rejected on the record: recomputing payability inside `legend_entries`
  gives **two answers to one question** — the failure `swimlane_plan`'s own docstring names — and
  weakening the entry to *reachability* shows it when nothing is drawn. Note the gate that does NOT
  work: `selected_id is not None` is near-always true, because `App._select_first` runs at the top
  of every `refresh_view`.

### Findings that outlived the batch

- **The legend has never described the wave** (verified by sweeping every `out.append` in
  `legend_entries`). This is the direct cause of the operator's *"I am not certain what they do"*.
  **Candidate control:** the ghost-mark law verifies that every legend entry is drawn but **not that
  every drawn mark is explained**. That asymmetry is a hole in a shipped law.
- **`_figures`' docstring is one of 26 claim-bearing prose lines** that would go false; `grep "own
  wave"` catches only 3. `views.py:720` and `:2112` are the return contracts of the two functions
  the change re-signs.
- **`report.py:122` carries a false claim on disk today** — post-change the report would draw a
  curve for every project unconditionally while the app draws at most one.
- **`test_vertical_fill.py` and `test_occupancy.py:93` both render only `selected_id=None`** — so
  the never-pads law and the occupancy floor are measured in the one state the disclosure row would
  create. Two files, not one.
- **`lead_band`, `stack_block`, `project_wave` have zero direct test guards.**
- `tests/test_span_economy.py` is unmeasured against a ~114→~20 cell swap.

### Process items

- **`~/.claude/docs/FLOW-VERSION.md` is stale by one control.** C-46 landed in `f3d4fba` (pushed)
  and the manifest still declares `C-1 … C-45` with the pre-C-46 hash. 11 of 12 files verify
  byte-for-byte. Its own rule: whoever edits a flow file owns the bump. **Different repos**
  (`claude-config` + `claude-skills`), so not fixable from this one.
- **Orchestration lesson, encoded:** fix the `AT`/`TC` identifier register BEFORE dispatching
  parallel agents. Two Phase-1 agents in parallel minted colliding ids and broke the behavioural
  traceability chain.

## From 2026-08-06-fastflow-03 — the row cost model (SHIPPED, no visual change)

`/fast-dev-flow`, one increment, three files. **No behaviour change**: the `taskboard/views.py`
diff is two docstrings, proven prose-only by comparing the AST with every docstring stripped.
707 → 725 tests. Spec + probes: `.fast-dev-flow/spec.md`, `.fast-dev-flow/probes/`.

### What it settled

- **THE COST MODEL HAD NO DEFECT.** `swimlane_plan`'s `h - 2 - (2 if active else 0)` and
  `lead_band`'s `prof + 2` are the two halves of ONE correct identity, verified **124/124**
  in regime over 160 renders (5 boards × 4 widths × 8 heights, frozen clock, synthetic boards):

      room = h - 2 - 2*[active]      need = prof + Σ(wrows + min(titles,o)) + n_rest
      BODY == need + 2*[active]      2 + BODY + ABSENCE == h

  **The two `2`s are different**: `h - 2` is the panel's own chrome (header + axis, the close
  being frameless); `- 2*[active]` is the lead band's head and tail. Batch-03's headline claim
  ("the cost model undercharges `prof`") is **FALSE by execution**, and so is its inverse.
- **Pinned** by `tests/test_row_cost.py` (18 tests, laws L1–L9), and the model is now written
  down in the docstrings of `allocate` and `swimlane_plan` **with its regime**.
- **Every law is answerable to a mutation that reddens it** — 5 source mutations applied to
  `taskboard/views.py` for real (not monkeypatched), each killed, `views.py` restored
  byte-identical: `room = h-2` (6 failed) · `room = h-6` (2) · `lead_band ±1 row` (7 / 5) ·
  rung four dropping its `- 1` (1). Runner kept at `.fast-dev-flow/probes/_mutate_check.py`.

### Findings

- **A claim this repo shipped was FALSE, and is corrected.** `tests/test_vertical_fill.py:91`
  said *"the lanes never pad at all — their allocator spends the whole height it is given"*.
  It holds **only while a project is active**. On an all-resting board nothing draws the bench,
  `prof` is billed for it anyway, and the view pads **exactly `h - 3 - n_rest`** rows (verified
  across 5 lane counts × 4 widths × 8 heights). The operator reproduced this independently and
  ruled: **document the regime, do not change the behaviour.** Done.
- **`prof` is billed and never drawn when no lane is active.** Dead budget, harmless in effect
  (nothing else could spend it) but it makes the model's A=0 branch vacuous. **Deliberately left
  alone** — fixing it is a behaviour change, out of a "no visual change" batch. Carried below.
- **A vacuity trap that hid 2 of 5 mutations, and it was live in the first draft of this batch's
  own test.** Selecting the sample on `feasible = charge <= room` — a quantity computed from the
  code under test — makes M1 (call site never pays for the lead band) and M4 (no absence row
  reserved) pass **vacuously**; M1 leaves the sample EMPTY. The off-regime exclusion must be
  **static** (named fixture + height), and feasibility must be **asserted**, never selected on.
  Measured both ways. **Candidate control** for `dev-flow-lessons`: *an exclusion predicate
  computed from the code under test is a vacuous check wearing a filter's clothes.*
- **The bench share was already shipped behaviour, not change-induced.** On HEAD today, a calm
  board's bench is 86.7 % at h=30, **93.3 % at h=60, 95.0 % at h=80**; by board shape the max is
  `calm` 95.0 % · `typical` 73.8 % · `huge` 44.4 % · `busy` 41.2 %. The driver is **how many
  active lanes exist**, not `wrows`. Fed into the O-3 re-presentation above; the operator kept
  the ruling. The **post-change** share remains `NOT MEASURED` — it belongs to the redesign batch.
- **`fa821ae` was unpushed** when this batch opened, though the handoff asserted
  `HEAD == origin/main == fa821ae`. Resolved by the operator mid-batch: amended and pushed as
  `6b7c4c3` (which also made `_prototypes/` render a **synthetic** board on a frozen clock
  instead of carrying real project names and task titles into committed files), then `3b0f011`.
  **Standing practice, now explicit: no artifact may carry the operator's board data.** This
  batch's probes and fixtures are synthetic and in-memory throughout.

### Carried forward from this batch

- **`prof` is billed for a bench nothing draws when no lane is active.** A behaviour change, so
  out of scope here. Whoever opens it must keep `tests/test_row_cost.py::test_L8...` honest —
  it currently pins the pad as `h - 3 - n_rest`, which is what would change.
- **`lead_band`, `stack_block`, `project_wave` still have no direct test guards** beyond the
  arity/accounting ones this batch added. `project_wave` remains entirely unguarded.
- **The redesign batch is unblocked**: with the model fixed and pinned, "the project row states
  its demand; the curve moves to a disclosure row" becomes row substitution against a known
  budget. O-1, O-2, O-3, O-4 are all ruled; nothing in this batch reopened them.
