# Design proposal — taskboard — Batch 2026-10-20-batch-01

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
| Id | `PDR-2026-10-20-batch-01` |
| Requirements covered | HLR-2201..HLR-2206 · LLR-2201.1..LLR-2206.1 (LED-2026-10-20-batch-01.1) |
| Modules touched (from `docs/ARCHITECTURE.md`) | `models` (`taskboard/boards.py` new, `taskboard/models.py`), `views` (`taskboard/views.py`), `app` (`taskboard/app.py`, `taskboard/__main__.py`, `taskboard/taskboard.tcss`), `modals` (`taskboard/modals.py`), `keymap` (`taskboard/keymap.py`), `tests`, `docs` |
| Triggers that fired | A1 · A2 · A3 · B1 · B2 · B3 · B4 · C1 · C5 · C6 · C8 · D1 · E1 |
| Author / reviewers | orchestrator (author) · `architect` · `qa-reviewer` · `ux-reviewer` · `security-reviewer` |

---

## 1 · Objective and scope

Ship variant C of the multi-board round with P1–P4 as accepted. Four increments, in this order:

- **001 — the registry and switching (HLR-2201, HLR-2202).** `taskboard/boards.py` (new, `models` layer): `slug`, `BoardEntry`, `Registry` (`load`, `single`, `get`, `active`, `opening`, `entry_for`, `register`, `touch`, `save`), `peek_board`, `registry_path`. `app.TaskboardApp(registry=None)`: `self.registry`, `self.board_id`; `on_mount` split into the per-board `_open_board()` (the shipped ten top-level steps, the clock interval among them only at mount, between `_apply_clock_settings` and `_warn_if_rescued`); `_start_team_daemon` keeps `self._team_timer`; `switch_board(id)`. `__main__.open_app(board)`; `main()` runs it. Nothing visible changes yet: no chip, no home, no key (the registry is loaded and `--board` registers).
- **002 — the chip, the home and `B` (HLR-2203, HLR-2204).** `models.Board.label`; `views.board_chip`, `header(..., chip=)` at the fifteen main-screen head rows and `render_setup`'s first row; `views.board_summary`, `ago`, `due_strip`, `home_card`, `home_title`, `home_keys` (the round's `summary`/`due_strip`/`HomeScreen._paint` bodies, minus option D); `app.BoardsHome` (the round's `HomeScreen`: a title `Static`, a `VerticalScroll` holding a 2-column `Grid` of card `Static`s with border/border title/subtitle styles, the key `Static`), `action_boards`, `check_action`, the launch push; `keymap.KEYMAP` `B`. The key bar of every view gains `B Boards`: the shipped key-bar assertions are updated law-driven (census); `README.md`'s Keys table gains `B` in this increment (docs — the seat's README law, architect A-21, qa QA-10).
- **003 — the board forms (HLR-2205).** `boards.Registry.create/edit/archive/free_color`; `modals.BoardForm` (the round's form); `BoardsHome` `n`/`e`/`x` (`x` through `ConfirmModal`); `taskboard.tcss`'s shared backdrop rule gains `BoardForm`.
- **004 — the move (HLR-2206).** `boards.MovePlan`, `move_plan`, `move_project` (the round's `crossing`/`do_move` plus atomic saves, the log as a list, the backup suffixes, the image references, the refusals); `modals.MoveTarget`, `MoveConfirm`, `ProjectPicker` `m`; `app.after_move()`; `taskboard.tcss` backdrop. Docs: `README.md` (a `## Boards` section; `## Data files`; `## Command line`), `.dev-flow/BACKLOG.md` (option D, OPTIONAL).

**Not done:** variants A/B; option D; un-archiving from the home; cross-board links; locking; the presentation's chip (D3).

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `models` (`boards.py`) | the registry file and its rules; reading a board without writing; the move between two board files and their folders | `Registry`, `BoardEntry`, `slug`, `registry_path`, `peek_board`, `MovePlan`, `move_plan`, `move_project` | `views`, `app`, `modals` (any markup, widget or key) |
| `models` (`models.py`) | `Board.label` (runtime only) | the attribute | — |
| `views` | the chip in the head rows; the card bodies, the home's title and key rows | `board_chip`, `header(..., chip=)`, `board_summary`, `ago`, `due_strip`, `home_card`, `home_title`, `home_keys` | the registry (it receives `Board.label`, names and colours as arguments); reading files |
| `app` | which board is open and switching it; the home screen; the launch; `B`'s guard; the team ids a move checks | `TaskboardApp.registry`, `board_id`, `switch_board`, `move_team_ids`, `after_move`, `BoardsHome`, `open_app` | rendering (calls `views`); the registry's file format (calls `boards`) |
| `modals` | the board form; the move's picker and confirmation; `m` in the projects modal | `BoardForm`, `MoveTarget`, `MoveConfirm` | the app's import (a local `self.app` call only) |
| `keymap` | `B` | `KEYMAP` | — |
| `tests` | `tests/multi_board_fixture.py` (the round's four boards), `tests/conftest.py` (the home seam), `tests/test_boards*.py`; the law-driven key-bar updates | — | importing `prototypes/` code (the round's SVGs are read as FILES) |
| `docs` | `docs/ARCHITECTURE.md` (ARQ amendment), `README.md`, `.dev-flow/BACKLOG.md` | — | — |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ (`boards` → `models.py`/`history.py` inside the layer; `views` never reads the registry; `modals` → `boards`/`models`/`views` only; `app` → all)

## 3 · Diagrams

The files (P1; the round's `evidence.json` tree, a move made):

```
~/.taskboard/
  boards.json                         the registry (written only when it changes, or at an opening with >1 board)
  board.json                          Main — today's board, in place
  board.json.pre-move-2026-10-20      a byte copy, before a move touched it
  move-2026-10-20.json                [ {date, project, from, to, tasks, links_kept, links_dropped} ]
  history.jsonl  images/  reports/    Main's, as today
  boards/
    client-retail-rag/board.json      + its own history.jsonl, images/, reports/, .pre-move copy, move log
    personal/board.json
```

The start (`open_app`) and the switch:

```
open_app(board?) ─ Registry.load(~/.taskboard/boards.json, ~/.taskboard/board.json)
   │                  (missing → [Main]; unreadable → .corrupt copy + [Main] + a notice)
   ├─ board given → register(path)  (new entry, or the existing one un-archived)
   ├─ entry = registered or opening()   (last if active · first active · first)
   ├─ touch(entry)                     (writes only if >1 entry or the file exists)
   └─ TaskboardApp(entry.path, registry)
         on_mount: label → [>1 active → push BoardsHome] → _open_board(at_mount) (its clock interval between the clocks and the notices)
switch_board(id): missing file? warn → snapshot → Board.load(path) → stop team timer → clear per-board state → label → _open_board()
                  [False → restore the snapshot, restart the timer, return] → touch
```

The home (variant C as captured; the cursor's card heavy and coloured):

```
 ◆ TASKBOARD  boards                                       4 boards · ▲5 late · Tue 20 Oct
 ┏━ ▶ Personal ━━━━━━━━━━━━━━━━━━━━━┓  ╭─ Client · Retail RAG ──────────────╮
 ┃ 6 open · ▲1 late · 3 due this week · 2 projects ┃  │ 7 open · ▲1 late · 2 due … │
 ┃ ▲1 ▃▃▅▅·· …  (28 days × 2 cells)  ┃  │ …                                 │
 ┃    20     26      2      9    16  ┃  │                                   │
 ┃  today  Book physio   (5/3/1 next dues by height) │                       │
 ┃ ■ Home & paperwork  ■ Fitness block (≥40 rows)    │                       │
 ┗━━━━━━━━━━━━━━━━━━━━━━━━━ open now ┛  ╰──────────────────── opened 20h ago ╯
 ←→↑↓ move  ↵ open  n new  e name/colour  x archive  esc back  q quit
```

The move (P3):

```
P → m → MoveTarget (other active boards) → move_plan(src, peek_board(dst), pid,
                                                    app.move_team_ids(src), app.move_team_ids(dst))
      refusal? → notice, nothing written
      → MoveConfirm (tasks, kept, crossing [scrolls], the backup/log/undo lines, keys) → enter
      → move_project, on COPIES of both boards (the live board untouched):
           stale plan? refuse · byte copies (exclusive) · references rewritten
           → dst.save_atomic → src.save_atomic
           → image folders (copy to temp, rename, remove; only from src's own images/)
           → history (append to dst, then rewrite src) → move logs (atomic)
      → app.after_move(new_src) (the open board replaced, undo cleared, repaint) → notice
      OSError → notice naming .steps and the backups (before the source save: the open board unchanged)
```

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `boards.json` (new) | — | as `docs/ARCHITECTURE.md` §4 | `open_app`, the home, the forms, the move | no — one lane |
| `boards.py` API (new) | — | as LLR-2201.1, LLR-2205.1, LLR-2206.1 | `app`, `modals`, `__main__`, tests | no |
| `TaskboardApp.__init__` | `(board_path=None, *, team_sync_interval=1800.0)` | `+ registry=None` | `__main__`, every app test (unchanged calls) | no |
| `TaskboardApp.on_mount` | nine calls + the clock interval | the label, the home push, then `_open_board(at_mount=True)` (the same ten steps, the same order, the interval at mount only) | the mount-order tests | no |
| `Board.label` (new) | — | `(name, colour)` or None, never saved | `views`, `app` | no |
| `views.header` | `(title, right, w, tone)` | `+ chip=None` (None: byte-identical) | the 15 head rows; `test_app.py`, `test_present_polish.py` | no |
| `KEYMAP` | 55 keys | + `B` (universal, primary, after `q`) | the bar, `?`, the palette, every key-bar test | no |
| `ProjectPicker` | `e x d j k esc` | + `m`; its title | the operator; `test_markup_sites.py` | no |
| `TaskboardApp.move_team_ids`, `after_move` (new) | — | as LLR-2206.1 | `modals.ProjectPicker` | no |
| `taskboard.tcss` backdrop rule | 8 modals | + `BoardForm`, `MoveTarget`, `MoveConfirm` | the new modals | no |

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-2201 | 0 | the registry's load table (missing, unreadable + `.corrupt`, the entry rules, `last`), the round trip, the atomic save, `touch`'s write rule, `register`, `slug`, `peek_board` | the unreadable file read as empty without a copy; a duplicate path kept; `archived` truthy; `touch` writing one board; `save` in place |
| AT-2201 | B | `open_app(None)` with no registry → the main screen, no chip, no `boards.json` after; with `{not json` → the default board, the `.corrupt` copy, the `Boards` notice | `touch` writing one board; the quarantine skipped |
| TC-2202 | A | `switch_board` clears each per-board field, stops a stand-in timer, runs `_open_board` once, keeps the view; the open id a no-op; setup → the view before; `open_app` with `--board` and with `last` archived; the mount order recorder; `registry=None` beside the board | the undo stack kept; the timer not stopped; `_open_board` not run; `--board` ignored |
| AT-2202 | B | the round's boards: home → `esc` → Personal's tasks; `B` `right` `enter` → Client's; `[` on `tc1` → Client's own `history.jsonl`; restart → the home's cursor on Client; `--board` → a new entry and its chip | the switch not loading the file; `touch` not recording `last` |
| TC-2203 | A | `board_chip` (style, cut, escape); every view × widths 30–160 with a label: the head row's visible width exactly `w`, the chip first where not the fallback; the S-2 payloads literal at every width (the narrow fallback included); with None equal to `base_ref`'s frames (`evidence/frames-base.json`: `evidence/frames_base.py` in a worktree at `783397e`, `render_view(mode, <the round's Main board>, False, None, today=2026-10-20, width, height=40)` at widths 40, 80, 118, 160 — plain text and row 0's spans); the presentation without chip | the chip without a label; no escape (chip or fallback); no cut; the width counted twice; a view's head row without the chip |
| AT-2203 | B | after opening Personal / Client: the first row of views 1–9, 0 starts with the chip; back on `1`, Client's equal to `C-160-switched.svg` row 0; no chip in `R`; none with one board | the chip at one board; a view's head row without `chip=` |
| TC-2204 | 0/A | `board_summary` = the captures' counts and Personal's next ids; `ago`; `due_strip`'s choice at five widths; the separators; `n_next`; cursor clamps; `check_action` for `boards`, on the home and under its modals; `enter` into a team board with no identity (the picker active, no home); `B` in every view's bar; markup payloads (border title too); seven boards scroll; a missing and an unreadable board file; no board written | `boards` not released under a modal; a main key acting behind the home; `week` past Sunday; a late task counted next; a missing board seeded; `enter` switching before closing the home |
| AT-2204 | B | at launch the home equals `C-160-open` / `C-118-open` / `C-80-open` but the key row; `B` opens it, not over `R` or `P`; `3`/`a` inert on it (the lanes view and no editor after `esc`); the key bar's `B Boards`; `?` lists `B` | `boards` released under a modal; a main key acting behind the home; the card's text order (the launch push at one board is AT-2201's) |
| TC-2205 | 0/A | `create` (folder, empty board, settings, slug collisions against registry and disk, a reserved name, the racing folder → `FileExistsError` with nothing written, `ValueError`, 60 cut), `edit`, `archive`, `free_color`; the form's colour cycle, blank name and cut file line; `x` on the open board writes nothing; the chip following a rename and leaving at one board | `exist_ok=True` (killed by the racing-folder arm); slug ignoring disk; an empty name accepted; the open board archivable; the renumbering flag missing; the archive button `Delete` |
| AT-2205 | B | `n` + name + `tab` + `enter` → the folder, the chip; `e` rename; `x` archive another (folder intact); `x` on the open board refused; a blank name inert | the new board not opened; archive touching the folder |
| TC-2206 | 0/A | `move_plan` (tasks, kept, crossing, every refusal — the traversal ids, team on either side, the same file, a missing, unreadable or changed target — with both folders hashed before/after); `move_project` (files, backups, `-2` suffix, log list and a non-list log left alone, image references three ways, archived task, rank cleared, history order); the target's save raising and the source's save raising (failure injection); the confirmation's box rows vs `move-160-3-confirm.svg` + the undo row; eight crossing links at 80×24; markup payloads | a crossing link kept on one side; an inside link dropped; a backup clobbered; the source saved first (the injection arm); the live board changed before the saves; a refusal writing; references not rewritten; a folder outside `images/` moved |
| AT-2206 | B | Main → Client move of `Retail RAG · pilot` through `P`, `m`, the picker, the confirmation: both files, backups, logs, history line, image folder and reference, the projects list, the notice | `m` unbound; links not filtered; the history line left behind |

**5b · The gauntlet controls that apply, and who pays:** C-40 (each new assertion RED on `base_ref` — a worktree at `783397e` — or by a recorded mutation; the orchestrator, a `mutate-00N.py` per increment beside its transcript); C-19 (one complete suite run per increment and at P4 — the orchestrator, in clean worktrees); C-42 (the ATs read the screen's widgets and the files as written); C-17/C8 (every new site over file-derived text escaped or a plain `Text` piece; `tests/test_markup_census.py` and `tests/test_markup_sites.py` stay green); C-26 (the reverse census per increment, the key-bar census in 002); the captures (the real app headless, `NO_COLOR` unset, compared with the round's captures — the orchestrator, at 002 and 004).

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| several boards inside one `board.json` | the history, images and reports beside the file would be shared (P-1); one corrupt file would take every board |
| move `~/.taskboard/board.json` into `boards/main/` | the commission: nothing moved or migrated automatically; `Main` stays in place |
| a module-level chip in `views` (set by the app, read by `header`) | renders stay pure functions of their arguments (`docs/ARCHITECTURE.md` §5); `Board.label` travels with the board, also through `filtered_board`'s copy |
| post-processing the head row in `render_view` | the head row's layout (title · gap · right) is `header`'s; splicing a prefix into finished markup would duplicate its width rules |
| `B` as a palette-only key (`bar=False`) | the commission asks the key bar to list `B`, and the round's capture shows it on the bar; palette-only would leave the bar unchanged but hide the way to the second board |
| the home as a `ModalScreen` | a modal dims the board behind it; the home is a full screen as captured (variant C) |
| a chip in the presentation too | its frames and exports are for an audience; the shipped presentation oracles would drift (D3, recorded for the operator) |
| an undoable move | two files change; the undo stack holds one board's snapshots (D4) |
| re-id a moving task whose id the target holds | its history lines and image folder are keyed by the id; a refusal is safer for a 1-in-4-billion case |
| reload every board on each home paint (the round) | a board file read per keypress; `Board.load` at a missing path writes (P-2) |

Risks: the key-bar law-driven updates (census in 002); the home's capture equality depends on Textual's layout (same pin); a move writes two files and folders (copies first, refusals, target before source); `--board` on a copy registers it (README).

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | §1, §2, §3 and §4 here → increments 001–004's packets §1 and §2; §2's module table → the ARQ amendment of `docs/ARCHITECTURE.md` |
| rejected alternatives and risks | the DDR | §6 → the DDR's "what changed against the PDR and why" |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | `tests/multi_board_fixture.py` (the round's four boards and registry as a test fixture); `tests/conftest.py`'s home seam; the `base_ref` worktree for the REDs; Edge for the PNGs; `evidence/capture.py` for the real-app captures |
| proposed test cases | layers 0/A/B and the DDR | §5 → the packets' §4 `Mutation verdicts`; the DDR's checklist |
| design → requirement traceability | the matrix and the DDR | §5's Id column ↔ `01-requirements.md` §3/§4; the packets' §2 `Traces to` |

- ⚠ Any row whose consumer column is empty: **remove the output, or explain why it is being produced.**

## 8 · Parallelisation plan *(only if the batch forks)*

none — one lane, four increments in order.

**After the P2/PDR review, iteration 1 (LED-2026-10-20-batch-01.2):** the conditions are carried by the requirements (the narrow head row escaped and every view's head row exactly `w`; the home blocking the main keys while it is anywhere on the stack and `enter` closing it before the switch; a failed migration at a switch keeping the open board; the interval at mount only; the move on copies with the target saved before the source and the folders after; the traversal, team (both sides), same-file, missing, unreadable and changed-target refusals; `peek_board` without the quarantine copy; the registry never rewritten after an unreadable read and `.corrupt-N`; the archive button `Archive`; the confirmation's scrolling links; the frozen clock at every module) and by §1, §3, §4 and §5 above.

**After iteration 2 (LED-2026-10-20-batch-01.3):** §1, §3, §4, §5 aligned with LLR-2202.1 (ten steps, the interval at mount, `touch` after a successful switch, `[`), `move_team_ids` in §2, the base-frame oracle's arguments named; the move hands the new source over after a failure past the source save; the counts row's drop rule is the round's.
