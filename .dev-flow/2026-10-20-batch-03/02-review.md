# Review — taskboard — Batch 2026-10-20-batch-03

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` — iteration 1 `iterate-to-refine` (architect A-1..A-3 requirement defects; qa-reviewer QA-1..QA-6 requirement-defect majors; ux-reviewer UX-1, UX-2, UX-4 majors; security-reviewer approve with conditions S-1..S-3) → LED-2026-10-20-batch-03.2; iteration 2: architect ARQ/P2 approve, PDR approve with condition A-18; qa-reviewer P2 approve, PDR approved with conditions QA-18/QA-20/QA-24; ux-reviewer P2 approve, PDR approved with conditions C2/C4; security-reviewer P2 and PDR approve (S-1..S-3 re-read at increment 003) → LED .3 folds the minors → Phase 3 through the PDR
- **Out-of-scope findings:** 5 named and routed below — a read-only `--open` (architect A-2) → `BACKLOG.md`, the operator's; `--report --board <missing>` seeds a board (security S-3, pre-existing) → `BACKLOG.md`; checkboxes and selects stay `tab`-reached fields (qa QA-15) → recorded in D-6; the objection's standard for the other TUI repositories (D-6) → `BACKLOG.md`; the unverdicted visual of the key lines (ux UX-3) → the close's operator items
- **Findings:** iteration 1: 0 blocker · 15 major (A-1..A-3, QA-1..QA-6, UX-1..UX-4, S-1..S-3 as medium) · 37 minor/low; iteration 2: 0 blocker · 0 major · 18 minor/low (A-16..A-19, QA-18..QA-24, UX-21..UX-24 with the UX-3/UX-16 residuals, S-11, S-12)
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are black-box (they drive `open_app`/`main`/`TaskboardApp` and keys and read the screen, the notices, the files and the exported SVG's text, row by row after QA-2)
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ⚠ 10 findings (S-1..S-3 medium, folded as contract text and kept as conditions on increment 003's code; S-4..S-9 low, folded; S-10 information)
- **Evidence checklists (architect / qa / security):** ✓ all complete (in the reviewers' returns; ux-reviewer too)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

Reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (D1 fired), `security-reviewer` (C5, C6, C8 fired) — each spawned as a sub-agent with its `agents/<role>.md` role, read-only, in parallel, 2026-10-20, two iterations; each reviewed the ARQ amendment, the requirements (P2) and the design proposal (PDR) together.

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A-1 | architect | major | HLR-2404, LLR-2404.1 | the cursor-less export anchors the overflow folds on the first project, not the screen's | lay out around the screen's cursor project, draw no cursor | fixed (LED .2) |
| A-2 | architect | major | HLR-2410 | `--open`'s start writes the opened file (migrations, marks, sweep), unstated | state it; route a read-only `--open` to the operator | fixed (LED .2); routed → `BACKLOG.md` |
| A-3 | architect | major | ARQ `Board.label`, HLR-2408 vs HLR-2410 | the label row and the chip condition contradict the unlisted chip | key on the label; amend the row | fixed (LED .2, ARQ) |
| A-4 | architect | minor | ARQ §5; LLR-2401.1 | two §5 rows' revisit triggers fired silently; registry entries into `views` | record the revisit; plain lanes | fixed |
| A-5 | architect | minor | ARQ §1, D-9 | "never in a board folder" — `~/.taskboard/` is Main's | reword | fixed |
| A-6 | architect | minor | LLR-2401.1, LLR-2409.2 | `%-d` raises on Windows | `f"{d:%a} {d.day}"` | fixed (LED .2) |
| A-7 | architect | minor | LLR-2407.1 | the named actions do not exist; keys could drift from buttons | one `press_button(<id>)` | fixed (LED .2) |
| A-8 | architect | minor | ARQ, HLR-2409/2410 | the naming rule is private | expose `name_for` | fixed |
| A-9 | architect | minor | HLR-2410, HLR-2401 | unstated: unreachable after a switch, missing from the agenda, `1 boards` | state; singular | fixed (LED .2; the agenda adds it as a lane, UX-11) |
| A-10 | architect | minor | HLR-2401 | "nothing written" vs the switch's writes | reword | fixed |
| A-11 | architect | minor | LLR-2410.1 | the check after `--report` would let the loader seed | check first; a TC | fixed (with S-3) |
| A-12 | architect | minor | census | two apps on one board now see a notice | grep the multi-app suites | fixed (increment 003's census) |
| A-13 | architect | minor | LLR-2409.1 | "regular file" unspecified | `lstat` + `S_ISREG` | fixed (with S-4) |
| A-14 | architect | minor | TC-2405 | the label changes which wording fits | pin with and without | fixed |
| A-15 | architect | minor | §6.3 | `esc`+letter read as `alt+letter` | record | fixed (§6.3) |
| QA-1 | qa-reviewer | major | AT-2401 | no arm jumps to another board | `enter` on Personal's task first | fixed (LED .2) |
| QA-2 | qa-reviewer | major | AT-2402, AT-2404 | SVG text checks vacuous (`&#160;`, split `<text>`) | read row by row, unescaped | fixed |
| QA-3 | qa-reviewer | major | AT-2404 | the clip-path count is rows − 1 | highest `line-N` + 1; the rasteriser's size for the RED | fixed |
| QA-4 | qa-reviewer | major | LLR-2401.1, LLR-2409.2 | `%-d` on Windows | as A-6 | fixed |
| QA-5 | qa-reviewer | major | AT-2407 vs LLR-2406.1 | two vs three spaces | three | fixed |
| QA-6 | qa-reviewer | major | TC-2407 | the law could be vacuous; no result check; visibility unheld | walk the modules; compose; compare results; read the screen | fixed |
| QA-7 | qa-reviewer | minor | AT-2410 | the both-options arm passes on base; no `--report --open` arm | assert argparse's text; add the arm | fixed |
| QA-8 | qa-reviewer | minor | HLR-2409 | the key undefined; two spellings | `boards._key`; an arm | fixed |
| QA-9 | qa-reviewer | minor | HLR-2402/2408 | chip condition | as A-3 | fixed |
| QA-10 | qa-reviewer | minor | HLR-2401, HLR-2410 | `<n>` undefined; plurals | the lanes; singular | fixed |
| QA-11 | qa-reviewer | minor | AT-2406 | the wrapped path breaks a substring check | read the box's region, whitespace aside | fixed |
| QA-12 | qa-reviewer | minor | AT-2407 | `c`, `I`, TextPrompt named, not driven | arms | fixed (`c`, `I`; TextPrompt by TC-2407) |
| QA-13 | qa-reviewer | minor | design §5 | the "no priority" mutation survives | record as not observable | fixed (LLR-2407.1) |
| QA-14 | qa-reviewer | minor | AT-2408 | `<board>` placeholder, team fixture unnamed | name them | fixed |
| QA-15 | qa-reviewer | minor | D-6 | toggles and selects stay `tab`; the picker shows no keys | record; a key line | fixed (D-6; HLR-2408) |
| QA-16 | qa-reviewer | minor | AT-2401, AT-2404 | internals read as seams | prefer the screen | fixed in AT-2401 (the highlighted row, the chip); the rasteriser's size kept as a declared seam |
| QA-17 | qa-reviewer | minor | HLR-2403 | `? keys` at 80; "narrow" ambiguous | name it; the arm | fixed |
| UX-1 | ux-reviewer | major | HLR-2401 | the round opened the agenda from the home | `A` on the home | fixed (LED .2) |
| UX-2 | ux-reviewer | major | D-6 | `MoveConfirm` still confirms on `enter` | `y`/`n`, no `enter` | fixed (LED .2) |
| UX-3 | ux-reviewer | major | HLR-2407 | the key lines were never rendered for the operator | real captures; the operator's verdict | PDR condition PC-1 |
| UX-4 | ux-reviewer | major | TC-2407 | visibility unchecked for four modals | the law reads the screen | fixed (with QA-6) |
| UX-5 | ux-reviewer | minor | AT-2407 | spacing | as QA-5 | fixed |
| UX-6 | ux-reviewer | minor | HLR-2401 | the agenda's key row cut with `…` at 80 | `key_line(width)` | fixed |
| UX-7 | ux-reviewer | minor | dates | `%-d` | as A-6 | fixed |
| UX-8 | ux-reviewer | minor | HLR-2401 | `<n> boards`, plurals | as QA-10 | fixed |
| UX-9 | ux-reviewer | minor | HLR-2401 | a missing board's lane looks empty | dim and say it | fixed |
| UX-10 | ux-reviewer | minor | HLR-2401 | uncapped lanes | declare | fixed (§6.3) |
| UX-11 | ux-reviewer | minor | HLR-2401 × 2410 | the unlisted open board missing from the agenda | a last lane | fixed |
| UX-12 | ux-reviewer | minor | HLR-2406 | `n / esc` styled as one key | the `/` dim | fixed |
| UX-13 | ux-reviewer | minor | HLR-2407 | `enter` saves `TextPrompt`, unsaid | `↵ / alt+s save` | fixed |
| UX-14 | ux-reviewer | minor | HLR-2407 | three key idioms in the editor | decide with the captures | recorded (kept; PC-1) |
| UX-15 | ux-reviewer | minor | LLR-2403.1 | `(all)` on an unscoped row | reword | fixed |
| UX-16 | ux-reviewer | minor | HLR-2408 | the picker's title cut; no keys | wrap; a key line | fixed |
| UX-17 | ux-reviewer | minor | HLR-2409/2410 | no timeouts | 30 s / 15 s | fixed |
| UX-18 | ux-reviewer | minor | HLR-2402/2408 | chip condition | as A-3 | fixed |
| UX-19 | ux-reviewer | minor | §6.3 | Caps Lock | record | fixed (§6.3) |
| UX-20 | ux-reviewer | minor | HLR-2402 | a mirrored hint row | narrow the rationale | fixed |
| S-1 | security-reviewer | medium | HLR-2409/2410 | `notify` parses markup: a bracketed name or path crashes a start | `markup=False`; arms | fixed (contract); condition at increment 003 |
| S-2 | security-reviewer | medium | LLR-2409.1 | the wrong JSON shape raises | a total, bounded reader; arms | fixed (contract); condition at increment 003 |
| S-3 | security-reviewer | medium | LLR-2410.1 | `--report --open <missing>` would seed | the check before `--report` | fixed (contract); condition at increment 003; the pre-existing `--board` case → `BACKLOG.md` |
| S-4 | security-reviewer | low | LLR-2409.1 | symlinks followed | `lstat`, full-name match | fixed |
| S-5 | security-reviewer | low | LLR-2409.1 | the takeover race | a second `lstat` | fixed |
| S-6 | security-reviewer | low | HLR-2409 | a clock step | the mtime only | fixed (accepted, stated) |
| S-7 | security-reviewer | low | LLR-2409.1 | an empty marker after a failed write | remove it | fixed |
| S-8 | security-reviewer | low | HLR-2410 | `~`, a folder, a non-board file, control characters | expand; regular file parsing to an object; strip | fixed |
| S-9 | security-reviewer | low | HLR-2401 | the agenda's reads | none | recorded |
| S-10 | security-reviewer | info | §6.3 | the scan answers hold | — | recorded |
| A-16 | architect | minor | ARQ §1 | the board-file row omits `--open` | add the clause | open — increment 004's ARCH pass |
| A-17 | architect | minor | ARQ §5, LLR-2401.2 | `A` on the home vs "only `quit`" | the top screen only | fixed (LED .3, ARQ) |
| A-18 | architect | minor | B1 census | `MoveConfirm`'s `enter` → `y` moves two suites | census row; name the updates | PDR condition PC-2 (B1 row added) |
| A-19 | architect | minor | LLR-2410.1 | `__main__` reads a private `_expand_home` | `expand_home` public | fixed (LED .3) |
| QA-18 | qa-reviewer | minor | LLR-2407.1 | the weak law text | copy the strong one | fixed (LED .3) |
| QA-19 | qa-reviewer | minor | B1 | as A-18 | — | with A-18 |
| QA-20 | qa-reviewer | minor | AT-2401 | byte-identity across two switches unverified | keep; declare a RED | PDR condition PC-3 (watch) |
| QA-21 | qa-reviewer | minor | AT-2407 | the 118 row and the `I` arm | exact; key by key | fixed (LED .3) |
| QA-22 | qa-reviewer | minor | AT-2406 | the move arm's start state | a fresh app | fixed (LED .3) |
| QA-23 | qa-reviewer | minor | HLR-2401 | the key row at 80×24 | an arm | fixed (LED .3) |
| QA-24 | qa-reviewer | minor | PDR §5 | stale and missing mutations | update | fixed (proposal §5) |
| UX-21 | ux-reviewer | minor | LLR-2407.1 | as QA-18 | — | fixed |
| UX-22 | ux-reviewer | minor | AT-2407 | as QA-21 | — | fixed |
| UX-23 | ux-reviewer | minor | LLR-2408.1 | the space after the chip | `board_chip_text` carries it | fixed |
| UX-24 | ux-reviewer | minor | AT-2401 | the home's row at 80 | an arm | fixed |
| UX-3 (residual) | ux-reviewer | minor | AT-2407 | the editor's notes at 80×24 | at most one row shorter | fixed (LED .3); the captures stay PC-1 |
| UX-16 (residual) | ux-reviewer | minor | HLR-2408 | the offer's title fit | wrap | fixed (LED .3) |
| S-11 | security-reviewer | low | LLR-2410.2 | `name_for` unstripped | strip | fixed |
| S-12 | security-reviewer | low | HLR-2410 | a file swapped after the check | accept | recorded |

### The modal inventory (D-6) — every `ModalScreen` of the package, by qa-reviewer's AST scan at `base_ref`

| Modal (file:line) | Buttons (id) | Keyboard path at `base_ref` | After this batch |
|---|---|---|---|
| TaskModal modals:362 | cal-f-start, cal-f-due, paste-img, save, cancel | esc = cancel; the other four **only tab+enter** | `alt+t`, `alt+d`, `alt+i`, `alt+s`, `esc`; the key line `#task-keys` |
| ProjectModal :560 | save, cancel, cal-f-start, cal-f-due | esc; the rest **only tab+enter** | `alt+s`, `alt+t`, `alt+d`, `esc`; key line |
| TemplateEditor :1064 | save, cancel | esc; save **only tab+enter** | `alt+s`, `esc`; key line |
| ClockModal :1508 | save, cancel | esc; save **only tab+enter** | `alt+s`, `esc`; key line |
| ConfirmModal :1548 | yes, no | esc = no; yes **only tab+enter** | `y`, `n`/`esc`; key line; the message wraps |
| TextPrompt :1574 | save, cancel | enter in the field saves; esc | + `alt+s`; key line `↵ / alt+s save` |
| MoveConfirm :2495 | — | `enter` = yes, `esc` = no (shown) | `y` yes, `n`/`esc` no, `enter` nothing; key line (UX-2) |
| TeamIdentityPicker :1465 | — | list `enter`, `esc`; **no keys shown** | + the chip, a key line `↵ pick   esc cancel` (UX-16) |
| CalendarModal :127 · EmojiPicker :204 · ProjectPicker :643 · LinkPicker :878 · TemplatePicker :1010 · MilestoneOffer :1111 · PresentHiddenPicker :1234 · GanttLinkMode :1312 · PhaseEditor :1613 · ImageViewer :1783 · TaskDetails :1815 · HelpModal :2086 · StandupModal :2230 · CommandPalette :2271 · BoardForm :2369 · MoveTarget :2440 · HelpScreen app:104 · PresentScreen app:190 | — | keys only, each shown on its hint or key line (or, for `ImageViewer`/`TaskDetails`/`StandupModal`, its own keys) | unchanged, but: `ProjectPicker`'s `m` refused on an unlisted board; `MilestoneOffer` gains the chip; `PresentScreen` binds from `PRESENT_KEYS`; new `PresentKeys` (`esc`/`?`/`q`) |

**No modal is left with tab-then-enter as its only keyboard path after this batch**: the 17 buttons of the six modals that hold any each get a direct key it shows; the law `tests/test_modal_keys.py` (TC-2407) walks both modules and fails on a new modal without its row. `BoardsHome` and `AllBoardsAgenda` are `Screen`s without buttons. Checkboxes and selects are fields reached by `tab` (qa QA-15).

### shall / should check

✓ clean — every HLR states its `shall`s (EARS event-driven, state-driven or ubiquitous); no `should` in a normative slot.

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-2401 / HLR-2401 | AT-2401 | yes (the agenda's text, the chip after the jump) | yes | yes (after QA-1, QA-16) | ✓ |
| US-2402 / HLR-2402, HLR-2403, HLR-2405 | AT-2402, AT-2403, AT-2405 | yes (the hint row, the keys window, the rail and the file's ranks) | yes | yes | ✓ |
| US-2403 / HLR-2404 | AT-2404 | yes (the exported SVG's text, row by row) | yes | yes (the rasteriser's size a declared seam) | ✓ |
| US-2404 / HLR-2406, HLR-2407 | AT-2406, AT-2407 | yes (the modal's text, the board) | yes | yes | ✓ |
| US-2405 / HLR-2408 | AT-2408 | yes (the titles) | yes | yes | ✓ |
| US-2406 / HLR-2409 | AT-2409 | yes (the notices, the presence folder) | yes | yes (a second app in-process: the same code a second process runs) | ✓ |
| US-2407 / HLR-2410 | AT-2410 | yes (`boards.json`, the chip, the notice, stderr) | yes | yes | ✓ |

### Supersession census (change-first)

The files `PLAN.md` §Triggers B1 lists; in particular `tests/test_boards_move.py` and `tests/test_boards_concurrency.py` confirm a move with `enter` (now `y`, law-driven, increment 001); the presentation suites pin the hint's exact wordings (`? keys`, `K J`, the chip — law-driven, increment 002); the multi-app suites are grepped for notices (increment 003, A-12). The I-gate confirms each still passes, or names the law-driven update.

### Security review summary
iteration 1 approve with conditions (S-1..S-3 medium; S-4..S-9 low; S-10 information) — all folded into the contract (LED .2); S-1..S-3 stay conditions on increment 003's code, re-read there by the security-reviewer; iteration 2: approve; S-11 (strip `name_for`) folded, S-12 (a file swapped between the check and the load) accepted.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
In the reviewers' returns (iterations 1 and 2), each with its role file's checklist complete; ux-reviewer: expert inspection, no user evaluation (one-person team), stated.
