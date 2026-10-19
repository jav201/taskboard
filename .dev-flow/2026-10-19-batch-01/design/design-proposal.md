# Design proposal — taskboard — Batch 2026-10-19-batch-01

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
| Id | `PDR-2026-10-19-batch-01` |
| Requirements covered | HLR-2101..HLR-2106 · LLR-2101.1..LLR-2106.1 (LED-2026-10-19-batch-01.1) |
| Modules touched (from `docs/ARCHITECTURE.md`) | `models` (`taskboard/models.py`), `team_sync` (`taskboard/team_sync.py`, increment 002: → `models` only, an allowed direction), `views` (`taskboard/views.py`), `app` (`taskboard/app.py`), `modals` (`taskboard/modals.py`), `tests`, `docs` |
| Triggers that fired | A2 · A3 · B1 · B3 · B4 · C1 · C4 · C5 · C8 · D1 · E1 |
| Author / reviewers | orchestrator (author) · `architect` · `qa-reviewer` · `ux-reviewer` · `security-reviewer` |

---

## 1 · Objective and scope

Ship variant C of the present-portfolio round as Present view 3 `all`, and fix the milestone row it found. Four increments, in this order:

- **001 — the milestone row (HLR-2101).** `views._present_task_row` gains the round's milestone branch (`portfolio_proto.task_row`): `gantt_milestone_cells` on the frame's axis, `◆` in the label, chip `_present_chip(None, due)`, the cursor's `◆` accent. Views 1/2 change only on milestone rows; view 3 (003) inherits it.
- **002 — the model (HLR-2102).** `Project.show_in_present` / `Project.present_rank` (the round's `Project.extra` stand-ins made fields); `present_order`, `set_present_order` in `models`; `_to_dict` drops a `None` rank; `team_sync`'s pull strips the two keys from a new team project (security S-4). 2 source files.
- **003 — the view-3 renderer (HLR-2103; the rows of HLR-2106).** `views.render_present_all` — the round's A/C path (`geo`, `layout`, `timeline_lines`, `head_row`, `_label`, `_echo_span`, `ruler`, `head`, `rail_lines`, `render`) moved in, B's code (`_ticks`, `_legend`, `unfolded`) left out, the rail fixed at 24 cells and not drawn below 100 columns; `PRESENT_SCREEN_VIEWS`; `present_hidden_rows`. 1 source file; nothing reachable from the app yet.
- **004 — the screen and the picker (HLR-2104, HLR-2105, HLR-2106).** `PresentScreen`: `3`, the cycle over three views, the view-3 cursor and its hand-off, `↑↓`/`←→`, `space`/`a` in view 3, `shift+↑/↓`, `enter`, `u`, `x` in view 3, the hint (three names, view 3's wordings, the `u` tail); `modals.PresentHiddenPicker`. 2 source files. Docs: `README.md` §Presentation, `.dev-flow/BACKLOG.md`. One increment for the screen, so no commit ships view 3 with the views-1/2 `space`/`a` acting in it or advertises `u` before it is bound (architect A-11, A-12).

**Not done:** variants A/B and B's ticks; persisting folds or the view; reordering `board.projects`; the `?` help (§6).

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `models` | the two project fields, their load/save rule, the presentation order | `Project.show_in_present`, `Project.present_rank`, `present_order`, `set_present_order` | any render, any key |
| `views` | the milestone row; view 3's frame (timeline + rail); the hidden rows `u` lists | `render_present_all`, `PresentAll`, `PRESENT_SCREEN_VIEWS`, `PRESENT_RAIL_MIN`, `PRESENT_RAIL_W`, `present_hidden_rows` | the screen's state beyond its arguments; saving the board |
| `app` | `PresentScreen`: the view index over three views, the view-3 cursor, folds and rail focus (session only), the keys, the hint, the export | — | rendering a frame (calls `render_present` / `render_present_all`) |
| `modals` | `PresentHiddenPicker` | the picker | the presentation's state (it gets the board and its rows) |
| `tests` | `tests/present_portfolio_board.py` (the round's board), `tests/test_present_milestone.py`, `tests/test_present_all.py`; the law-driven hint updates | — | importing `prototypes/` code |
| `docs` | `docs/ARCHITECTURE.md` (ARQ amendment), `README.md` | — | — |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ (`modals` → `views`/`models` only; `app` → all; `views` never → `app`/`modals`)

## 3 · Diagrams

View 3, at 100 columns or more (the round's C):

```
 rail (24) │ timeline (width - 25)
 PROJECTS  │ ◆ PRESENT · 5 projects  all                     29 open · ▲4 past due
           │      today Mon Oct 19  October 2026 … (month row; the cursor project's ◆ due)
           │      project span ▸   … (tick row: the cursor's exact dates)
▶ 1 ● Cust…│ ▾ ■ Customer Portal  4 open in 18d  ⟦━━━◆━⟧ …           Sep 14–Nov 6
  2 ● Bill…│   ▎ Account settings page   ━━━━━◑ …                       Oct 7–23
  …        │   …
  5 ○ Secu…│ (blank row between projects while every row fits)
           │ ▸ ■ Data Platform … (folded: by enter, or auto — furthest from the cursor first)
 5 shown · │ +N more rows not shown (only if folding every other project still overflows)
 1 hidden  │
```

The cursor: `("proj" | "task", id)`. Stops: on the rail every visible project (`present_order`); on the timeline the drawn header and task rows. Below 100 columns: no rail, `←/→` move like `↑/↓`. Leaving view 3: the shown project ← the cursor's project, the views-1/2 cursor ← the cursor's task (if any). Entering view 3: rail focus at ≥100 with the cursor on the shown project; else the views-1/2 cursor task when drawn, else the project's header.

The writes (all `Board.save()` at once): `space` → one flag; `a` → every hidden flag; `shift+↑/↓` → `set_present_order` over every visible project (dense 0..n-1); the picker's toggle → one flag. `enter`, `←/→`, `↑/↓`, `tab`, `x` write no board byte.

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `board.json` project record | no presentation keys | `show_in_present` (only `false`), `present_rank` (only an integer) | `team_sync` (pull: new projects through `from_dict`), other app versions (`extra`) | no — one lane |
| `Project` fields | 9 fields | + `show_in_present`, `present_rank` | `models`, `views`, `app`, `team_sync` | no |
| `_present_task_row` (private) | every task a bar | a milestone is `◆` on its date | `render_present`, `render_present_all` | no |
| `render_present_all` (new), `PRESENT_SCREEN_VIEWS` (new), `present_hidden_rows` (new) | — | as LLR-2103.1, LLR-2104.1, LLR-2106.1 | `app.PresentScreen`, `modals`, tests | no |
| `PresentScreen` keys and hint | 2 views; ` · N hidden` | 3 views; `3`, `shift+↑↓`, `enter`, `u`; ` · u N hidden` (one count in every view) | the presenter; the hint tests (law-driven) | no |

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-2101 | A | every milestone row of the round's board in views 1/2 at four widths: the field is `gantt_milestone_cells`, the chip `due <Mon D>`, `◆` in the label, the cursor's `◆` accent; a milestone with a start date the same | the branch removed (the bar returns); the chip given the start; the cursor's `◆` not accented |
| AT-2101 | B | `R` on Billing Migration at 118×31: `Cut-over weekend` holds one `◆` at Oct 25, no bar glyph, chip `due Oct 25`; the same in view 2 | the branch removed |
| TC-2102 | 0 | the load table of both keys; the save rule; byte-identity of boards without keys; `present_order` / `set_present_order` | rank accepting a bool; `None` written; `show_in_present` read truthy; unranked first |
| AT-2102 | B | reorder + hide on the rail → the file's ranks and flags; restart → same order; the board gantt in board order | `_to_dict` dropping the rank; the order read from `board.projects` |
| TC-2103 | A | the frame sweep over three boards incl. a reverse-ranked one with a hidden project (dims, rail iff ≥100, order, hidden absent, cursor never auto-folded, no overflow row when everything fits); the round's C text at 160×45 / 118×30 row for row; the S-2 markup payloads | the rail at <100; hidden projects drawn; auto-fold of the cursor's project; the order ignoring `present_rank` |
| AT-2103 | B | `R`, `3` at 160×45 / 118×30 / 80×24: header, projects in order, rail contents, no rail at 80 | `3` unbound; the rail threshold moved |
| TC-2104 | 0 | the cycle table; the cursor hand-off; the hint against LITERAL first-width tables (measured with `cell_len` outside the code); `present_paths(..., "all")`; the law-driven hint tables | `tab` modulo 2; `u` dropped from the tail; the hand-off keeping the old project |
| AT-2104 | B | the views' cycle with one cursor; `x` → `-all` SVG without `PROJECTS`; the hint's tail and labels in view 3 | the export written with the rail; the cycle |
| TC-2105 | A | `space` / `a` / `shift+↑↓` / `enter` / `←→` on a mounted screen with counted saves | a no-op key that saves; reorder over shown only on the rail; ranks not dense; `enter` saving |
| AT-2105 | B | the curation sequence through keys, read in the frame and the file | `space` on a header hiding nothing; the rail's toggle one-way |
| TC-2106 | A | `present_hidden_rows` both modes (003); the picker's toggle and save, markup in a title, `nothing hidden`, the census unchanged (004) | shown tasks listed; a hidden project's hidden tasks dropped; the toggle not saving; the title through a parser |
| AT-2106 | B | `u` in view 1 and view 3: the rows, a toggle, `esc`, the frame | `u` unbound; the picker's rows from the wrong project |

**5b · The gauntlet controls that apply, and who pays:** C-40 (each new assertion RED on `base_ref` — a worktree at `bdf6e9d` — or by a recorded mutation; the orchestrator, `evidence/mutate.py` per increment); C-19 (one complete suite run per increment and at P4 — the orchestrator); C-42 (the ATs read the frame, the hint and the picker as Textual holds them); C-17/C8 (every new site over board-file text escaped or a plain `Text` piece; `tests/test_markup_census.py` stays green and gains no exemption); the captures (the real app headless, `NO_COLOR` unset, compared by eye with the round's C captures — the orchestrator, at increments 003 and 004).

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| `"all"` as a third value of `render_present`'s `view` | view 3's cursor spans two kinds of row and it needs the folds and the rail focus; `docs/ARCHITECTURE.md` §5's re-open condition ("a third view needs state the renderer cannot take as an argument") is met |
| reorder `board.projects` itself | the board gantt and every other view would follow; the round's before/after showed the board gantt untouched and the operator did not object (D2) — flagged for the operator |
| the rail at every width (the round's 18 cells below 100) | at 80 columns the rail leaves names 10 cells and the field 26 (P-4); D5 |
| `u` in the hint as a separate key (`u picker`) | +9 cells in every wording; the count is where `u` matters, so the tail reads `u N hidden` (key + label, the hint's own grammar) and appears only when something is hidden |
| the picker without a row for a shown project holding hidden tasks | the tasks would stand without their project in view 3; the project row is listed `●` so the grouping reads |
| add view 3 and `u` to the `?` help (D8) | the help lists the main screen's keys only, by design (§5 of the module map); a declared deviation — the hint row and the README carry them |
| persist the folds | not asked; folds follow the room in the moment |

Risks: the law-driven updates of the shipped hint tests (TC-1904, TC-1808, TC-2002, AT-2002, TC-1604, AT-1602) — each named old → new in packet 003's census, the new values derived from the wording strings in the test, not from the code; the split view's hint at 80 columns falls to the short wording (7 more cells for `3 all  `); a team pull of a NEW project carries its presentation keys from `team.json` (through `from_dict`), an existing project's are never touched by a pull; the round's capture script subclasses `PresentScreen` and will not reproduce its frames after 003 (frozen evidence, `docs/ARCHITECTURE.md` §3 `prototypes`).

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | §1, §3 and §4 here → increments 001–004's packets §1 |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | `tests/present_portfolio_board.py` (the round's board as a test fixture); `tests/present_board.py` (PRES-V3); the `base_ref` worktree for the REDs; Edge for the PNGs; `evidence/capture.py` for the real-app captures |
| proposed test cases | layers 0/A/B and the DDR | §5 → the packets' §4 `Mutation verdicts`; the DDR's checklist |
| design → requirement traceability | the matrix and the DDR | §5's Id column ↔ `01-requirements.md` §3/§4; the packets' §2 `Traces to` |

- ⚠ Any row whose consumer column is empty: **remove the output, or explain why it is being produced.**

## 8 · Parallelisation plan *(only if the batch forks)*

none — one lane, four increments in order.

**After the P2/PDR review (LED-2026-10-19-batch-01.2):** the conditions are carried by the requirements (the view-3 tail one count, the rail toggle in place, `a`'s notice, `u` closing, the escape order, the census key, the literal hint tables, the team pull stripping the keys) and the re-cut above.
