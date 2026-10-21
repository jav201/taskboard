# Design proposal — taskboard — Batch 2026-10-20-batch-03

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language
> The normative rules below are language-independent. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Design proposal` · `7 · Forward-applicability table` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **Why a HEADING is reserved here and a FIELD NAME everywhere else:** `C-49`'s artifact is the §7 TABLE, and a rule that read a summary bullet instead of the rows would be reading a claim about the table rather than the table. `V52` therefore keys on this document's own H1 and on the §7 heading, which is why both are on the machine plane. **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`.

> **Owed in.** `core` by trigger · `full` ✓
> **Source:** `/dev-flow-init` step 4's seed-by-level table, which is this fact's one home. A level marked `—` **does not owe this artifact, and its absence is not an omission**; `by trigger` means the station exists only when the `triggers` block fired, and `stations_active` in `state.json` is the authority for *this* batch. Where a SECTION or a gate row is owed more narrowly than the artifact, it says so on the row.

> **Where this lives: the VAULT + Drive**, not the repo — it is deliberation, and its traceability to
> code is weak. It is **cited by id** from the repo (`PDR-<batch_id>#D<n>`), never copied.
> What binds code — a frozen interface, a design characteristic — also lands in the **repo**, in the
> requirement or in `docs/ARCHITECTURE.md`. *The vault keeps the deliberation; the repo keeps the commitment.*

> **The forward-applicability rule (ISO/IEC/IEEE 15288).** Everything below must be NAMED as the input
> of a later activity. **If a section of this proposal is nobody's input, delete it — it does not belong
> in the PDR.** That rule is what allows this document to cost half the batch without being waste.

| Field | Value |
|---|---|
| Id | `PDR-2026-10-20-batch-03` |
| Requirements covered | `HLR-2401 v1 · HLR-2402 v1 · HLR-2403 v1 · HLR-2404 v1 · HLR-2405 v1 · HLR-2406 v1 · HLR-2407 v1 · HLR-2408 v1 · HLR-2409 v1 · HLR-2410 v1 · LLR-2401.1 · LLR-2401.2 · LLR-2402.1 · LLR-2403.1 · LLR-2403.2 · LLR-2404.1 · LLR-2405.1 · LLR-2406.1 · LLR-2407.1 · LLR-2408.1 · LLR-2409.1 · LLR-2409.2 · LLR-2410.1 · LLR-2410.2` |
| Modules touched (from `docs/ARCHITECTURE.md`) | `app` (`app.py`, `__main__.py`, `taskboard.tcss`) · `views` · `modals` · `keymap` · `models` (`boards.py`) |
| Triggers that fired | `A2 · A3 · B1 · B4 · C5 · C6 · C8 · D1 · E1` |
| Author / reviewers | `architect` · `qa-reviewer` · `ux-reviewer` (D1) · `security-reviewer` (C5, C6, C8) |

---

## 1 · Objective and scope

The round's nine chosen variants, ported from `prototypes/backlog_round/proto.py` into the shipped classes, in four increments on one branch (`feat/backlog-round`, one lane):

- **001 — the modal keys (HLR-2406, HLR-2407; item 6 and its objection).** `key_line` (new); `ConfirmModal` gains `y`/`n` and `#confirm-keys` (the round's `ConfirmKeys.on_mount`, moved into `compose`) and `#confirm-box .modal-title { width: 100% }`; `TaskModal`, `ProjectModal`, `TemplateEditor`, `ClockModal`, `TextPrompt` gain their `alt` keys and key lines; `#task-keys` in the editor. 2 source files (`modals.py`, `taskboard.tcss`); tests in a new `tests/test_modal_keys.py`, the inventory law among them.
- **002 — the presentation (HLR-2402..HLR-2405; items 2, 3, 4, 5).** `keymap.PRESENT_KEYS`/`present_bindings` (the round's `PRESENT_KEYS` table, now also the bindings); `PresentScreen.BINDINGS = present_bindings()`, `_hint` with the chip (`PresentChipHint`), `? keys` (`_HelpHint`) and `K J` (`PresentReorderKJ`) in its wordings, `action_keys` (`PresentHelpModal`), `action_export` on `views.present_all_export` (the round's `_export` variant); `modals.PresentKeys` (the round's, generated from the seat); `views.board_chip_text`. 4 source files (`app.py`, `views.py`, `modals.py`, `keymap.py`); tests in `tests/test_present_backlog_round.py` (new) on `tests/backlog_round_fixture.py` (the round's fixture, copied).
- **003 — the boards (HLR-2408..HLR-2410; items 7, 8, 9).** `MilestoneOffer`/`TeamIdentityPicker` titles with the chip (`OfferNamedA`, `IdentityNamedA`); `boards.announce`/`renew`/`withdraw`/`open_elsewhere` (new) and the app's lifecycle and notice (`warn_twice`); `--open` and the unlisted board (`opened_unlisted`). 4 source files (`boards.py`, `app.py`, `__main__.py`, `modals.py`); tests in `tests/test_boards_backlog_round.py` (new).
- **004 — the agenda (HLR-2401; item 1, variant C).** `views.agenda_buckets`/`all_agenda`/`render_all_agenda` (the round's `AgendaRuler.body` and `gather`, made pure); `app.AllBoardsAgenda` (its screen), `A` in `KEYMAP`, `check_action`; the docs (`README.md`, `docs/ARCHITECTURE.md`'s final pass, `.dev-flow/BACKLOG.md`). 3 source files (`app.py`, `views.py`, `keymap.py`); tests in `tests/test_all_agenda.py` (new).

Out: the black window on `Personal`/`Course` and the blank screen behind the start-up modals (logged); editing from the agenda; the chip in the presentation's frame.

## 2 · Modules and boundaries

| Module | Change | Boundary moved? |
|---|---|---|
| `keymap` | a second seat (`PRESENT_KEYS`) joins `KEYMAP`; `A` joins `KEYMAP` | no — §2/§4 rows amended (the ARQ amendment) |
| `views` | pure renders: `board_chip_text`, `present_all_export`, the agenda | no |
| `modals` | `key_line`, every form's keys, `ConfirmModal`, `PresentKeys`, the start-up titles, the unlisted move refusal | no |
| `app` | `AllBoardsAgenda`, `PresentScreen` (generated bindings, hint, `?`, export), the presence lifecycle, the unlisted start; `__main__` `--open` | no |
| `models` (`boards.py`) | the presence functions | no |

No new import edge: `modals` already imports `keymap` and `views`; `boards.py` adds `hashlib` (stdlib).

## 3 · Diagrams

```
start / switch (_open_board, success)        a window's life on one board
  others = open_elsewhere(path)                announce ──► open/<hash>-<token>.json {since, pid}
  withdraw(previous marker)                    every 30 ticks: renew (utime) │ gone → announce again
  marker = announce(path, now)                 left (switch) or exit (on_unmount): withdraw
  others → notify "… open in another window"   another window's marker > 120 s old → removed by the reader

R (PresentScreen)                            keymap.PRESENT_KEYS ──► present_bindings() ──► BINDINGS
  hint: [chip ][1 gantt 2 split 3 all][keys…][  ? keys]          └──► modals.PresentKeys (the `?` window)
  x in view 3 ──► views.present_all_export (cur=None, cut after the last content row) ──► svg/png

A (AllBoardsAgenda)  lanes = registry.active() × (app.board | peek_board | None)
  views.all_agenda ──► items ──► views.render_all_agenda(day, row) ──► Static
  enter ──► pop, switch_board(entry) when another, jump_to(task)
```

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `keymap.PRESENT_KEYS`, `PresentKey`, `present_bindings` (new) | — | LLR-2403.1 | `app.PresentScreen`, `modals.PresentKeys`, tests | no — one lane |
| `PresentScreen.BINDINGS` | a hand-written list | `present_bindings()` (the same pairs plus `K`, `J`, `?`) | Textual; the presentation suites | no |
| `views.board_chip_text`, `present_all_export`, `agenda_buckets`, `all_agenda`, `render_all_agenda`, `AgendaItem` (new) | — | LLR-2402.1, LLR-2404.1, LLR-2401.1 | `app`, `modals`, tests | no |
| `modals.key_line`, `PresentKeys` (new) | — | LLR-2406.1, LLR-2403.2 | the modals, `app.PresentScreen` | no |
| `TeamIdentityPicker(roster)` | one parameter | `(roster, label=None)` | `app._init_team_mode`, tests | no |
| `boards.announce`, `renew`, `withdraw`, `open_elsewhere`, `presence_dir`, `PRESENCE_STALE` (new) | — | LLR-2409.1 | `app.TaskboardApp`, tests | no |
| `__main__.open_app(board)` | one parameter | `(board, unlisted=None)` | `main`, tests | no |
| `KEYMAP` | 56 keys | + `A` (`agenda_all`, `bar=False`) | `app_bindings`, `?`'s map, the palette, `tests/test_keymap.py`'s README law | no |

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-2401 | 0/A | buckets to Sunday; the dues' filter and order; rows exactly `width`; no project column at 80; Text pieces; `A` refused over a modal/home/presentation; seat keys dead behind the agenda; the jump's switch | the lane order dropped from the sort; `is_open` dropped; the 100-cell rule inverted; `agenda_all` not refused in `check_action`; the switch skipped |
| AT-2401 | B | `A` on the round's boards: three lanes, today's two dues in order, `down`, `enter` → `Golden question set` on Client A; files unchanged | `A` unbound; the sort by board name (the round's); the switch skipped |
| TC-2402 | A | `_hint` opens with the chip, bold on the board's colour, cut at 24 | the chip dropped; the chip in `_frame_text` |
| AT-2402 | B | the hint row starts ` Client A `; frame and SVG never hold it | the chip dropped; the chip added to the frame |
| TC-2403 | 0/A | `PresentScreen.BINDINGS` pairs == the seat's; every seat row in the window; live/dim by view | a binding added outside the seat; a row skipped; the dim rule inverted |
| AT-2403 | B | `?` in view 3 opens the window, the reorder row bright; `?` closes; view 1 dims it | `question_mark` unbound; the live rule inverted |
| TC-2404 | 0 | `present_all_export`: 93×21 on Client A, no `⟦`; a full frame keeps every row | the cut drops a content row; the cursor kept; the frame height passed |
| AT-2404 | B | `x` in view 3 writes 21 rows, no `⟦`/`project span`; the screen keeps `⟦` | `action_export` back on `_render_all().timeline` |
| TC-2405 | A | the three view-3 wordings name `K J` | a wording without `K J` |
| AT-2405 | B | `down`, `K` puts `Eval harness` first on the rail and in the file; `J` back | `K` unbound |
| TC-2406 | 0/A | `key_line`'s text, spans and fit; `y`/`n`/`escape`/`enter`; the wrap | `y` unbound; the wrap rule dropped; a key dropped before the words |
| AT-2406 | B | the home's archive: the whole message, the key line, `enter` nothing, `n` cancels, `y` archives; `d`, `y` deletes | `y` unbound; the `width: 100%` rule dropped |
| TC-2407 | 0/A | each form's `alt` keys do what the button does; the inventory law over every `ModalScreen` subclass | a key unbound; a modal missing from the law's table; a button with no key |
| AT-2407 | B | `a`, `Draft s`, `alt+s` saves `Draft s`; `alt+d` opens the calendar; `p`, `alt+s`; the editor's key line at 118 and 80 | `alt+s` unbound; `alt+s` bound without priority (the field eats it — to be measured); the key line dropped |
| TC-2408 | A | the offer's and the picker's titles open with the chip; none with one board; markup-looking names literal | the chip dropped; the app passing no label |
| AT-2408 | B | a start with Client A's offer pending: ` Client A  ◆ Milestones …`; the team picker opened from the home names its board | the chip dropped |
| TC-2409 | 0/A | `announce`/`open_elsewhere`/`renew`/`withdraw` with fresh, stale (119/121 s, future), invalid and foreign files; unwritable folder; the lifecycle at a failed switch and at the 30th tick | the stale test inverted; `mine` counted; the hash prefix ignored; the withdraw at a switch removed |
| AT-2409 | B | a second app on Client A shows the notice with `since 09:30`; after the first exits, a third shows none; a switch moves the marker | `open_elsewhere` not called; `withdraw` at exit removed |
| TC-2410 | 0/A | `open_app(None, path)` writes nothing; a missing path exits 2; both options exit 2; the unlisted label; the move refused | `open_app` registering; the existence check removed; the label None |
| AT-2410 | B | `main()` with `--open`: `boards.json` unchanged, the chip, the notice, no home, `B` lists the three boards, `m` refused | `--open` through `register` |

**5b · The gauntlet controls that apply, and who pays:** C-40 (each new assertion RED on `base_ref` — a clean worktree at `1fd667b` — or by a recorded mutation; the orchestrator, `mutate-00N.py` beside its transcript); C-19 (one complete run per gate; the whole suite in three sequential chunks at P4 — the host's memory, the commission); C-42 (the ATs read the screen's text, the notices and the files); B1's reverse census in each packet (the files §B1 of `PLAN.md` lists); the law-driven pin updates (the hint's `? keys` and `K J`) named in increment 002's packet.

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| the agenda as variant A (three bands) | the operator chose C; the round's A is the recommendation the verdict overrode |
| the agenda as a view of the main screen (`1`–`0`) | the views render one board (`render_view(board, …)`); the agenda reads every board |
| the chip in the presentation's frame (round's C) | the operator chose B; C leaks an internal board name to every export |
| a hand-written `PresentKeys` window beside hand-written bindings | two lists drift; the key bar's law (`keymap.py`'s docstring) is one seat |
| the presentation's keys inside `KEYMAP` | `a`, `u`, `x`, `1`–`3` mean other things on the main screen |
| a sheet under the frame for `?` (round's B) | the operator chose A; B costs the frame its rows |
| focus on the confirm button (round's 6 A) | a stray `enter` would delete a project; the operator chose B |
| `ctrl+<letter>` for the forms' buttons | `ctrl+v`/`ctrl+e` are the editors' own already; `ctrl+s` saves nowhere yet; `alt+<letter>` keeps one family for "a button" |
| keys inside the buttons' labels (`Save alt+s`) | the editor's action column is 16 cells; one key line in the key bar's style is the house's form (`MoveConfirm`, `BoardForm`, `MoveTarget`) |
| one shared presence file per board | two windows would overwrite and erase each other's; one file per window never collides |
| a liveness probe by pid | `os.kill(pid, 0)` is not a probe on Windows; the age rule is batch-02's lock rule |
| the markers beside each board file | a new file in every board folder (the suite lists board folders; the operator copies them); the home's `open/` folder is one place |
| `--open` of a missing path creating a board | the loader would seed and save sample data at a path the operator only wanted to look at |
| `--open` registering then hiding | it would write `boards.json`, which is what the item is about |

Risks: a marker outlives a crash ≤ 120 s (a false notice); a suspended window stops renewing (no notice); the generated bindings could drop a key the suite drives (TC-2403's equality and the existing suites); `alt` in a terminal that eats it (Windows Terminal passes it; `tab` stays); the black window on `Personal`/`Course` in real Windows Terminal (logged; the agenda's `enter` may land there).

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | §1–§4 here → increments 001–004's packets §1 and §2; §2/§4 → the ARQ amendment of `docs/ARCHITECTURE.md` |
| rejected alternatives and risks | the DDR | §6 → the DDR's "what changed against the PDR and why" |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | `tests/backlog_round_fixture.py` (the round's boards), the conftest home seam, a frozen clock (09:30) and calendar (2026-10-20); the PNG rasteriser stubbed in the export ATs; a clean `base_ref` worktree for the REDs; the round's `shoot.ps1` method for the real-app captures |
| proposed test cases | layers 0/A/B and the DDR | §5 → the packets' §4 `Mutation verdicts`; the DDR's checklist |
| design → requirement traceability | the matrix and the DDR | §5's Id column ↔ `01-requirements.md` §3/§4; the packets' §2 `Traces to` |

- ⚠ Any row whose consumer column is empty: **remove the output, or explain why it is being produced.**

## 8 · Parallelisation plan *(only if the batch forks)*

none — one lane, four increments in order.
