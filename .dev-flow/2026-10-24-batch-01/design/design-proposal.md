# Design proposal — taskboard — Batch 2026-10-24-batch-01

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
| Id | `PDR-2026-10-24-batch-01` |
| Requirements covered | `HLR-2601 v1 · HLR-2602 v1 · HLR-2603 v1 · HLR-2604 v1 · HLR-2605 v1 · HLR-2606 v1 · HLR-2607 v1 · HLR-2608 v1 · LLR-2601.1 · LLR-2601.2 · LLR-2601.3 · LLR-2602.1 · LLR-2602.2 · LLR-2603.1 · LLR-2603.2 · LLR-2604.1 · LLR-2604.2 · LLR-2605.1 · LLR-2606.1 · LLR-2606.2 · LLR-2606.3 · LLR-2607.1 · LLR-2607.2 · LLR-2608.1 · LLR-2608.2` |
| Modules touched (from `docs/ARCHITECTURE.md`) | `models` (`marks.py` new, `models.py`) · `app` (`app.py`) · `views` · `modals` · `keymap` · `taskboard.tcss` · docs (`README.md`) |
| Triggers that fired | `A1 · A2 · A3 · B1 · B4 · C6 · C8 · D1 · E1` |
| Author / reviewers | `architect` · `qa-reviewer` · `ux-reviewer` (D1) · `security-reviewer` (C6, C8; `marks.py` at 001's gate) |

---

## 1 · Objective and scope

The milestone-marks round's chosen variants, ported from `prototypes/milestone_marks/proto.py` into the shipped classes, in four increments on one branch (`feat/milestone-marks`, one lane — D-3). Written against the twice-review-folded contract (LED .1–.44).

- **001 — the store and the field (MM-D2, D3, D4; HLR-2601..2603).** `taskboard/marks.py` (new), a byte-level sibling of `people.py`: `Mark(id, name, shape, colour, hidden=False)`, `MARKS_NAME`, `SHAPES` (the eight glyphs of proto.py:85 — `◆` stands apart as the unclassified mark's glyph), `COLOURS` (the round's `SWATCH`, proto.py:86, ported as named tones), `Directory` (`load` never raising with the LED .29/.40 validation: slug id, unique, named, shape ∈ SHAPES, colour ∈ COLOURS, typed fields, `hidden` coerced to `bool`, one-line flattening per `people._clean`), `add`/`edit`/`set_hidden`/`_commit` on `boards.file_lock` + `models.write_atomic`, `find` prefix-only (the round's `find_class`), `people.handle_for` reused. `Task.mark: str | None` in `models.py`, written only when set (`Board._to_dict`'s `show_in_present` pattern, models.py:1049-1051). `Board.marks` (memory only); the app loads the directory beside `people.json` (app.py:1102's pattern) and hands it to every board (app.py:1208's). 3 source files; tests `tests/test_marks_directory.py` (new), `tests/milestone_marks_fixture.py` (the round's boards + four example classes, copied, synthetic).
- **002 — the encoding through one seat (MM-D1; HLR-2604).** `views.milestone_mark(task, board, today) -> (glyph, style, late_chip)` — shape+colour say the class, unclassified `◆` in `mut`, late date `over` + `▲Nd` (a non-empty chip implies `over` at every site, one channel), reached hollow (`HOLLOW`) + `✓`; the 20 sites of LLR-2604.2 routed (lanes/focus, bank edge, kanban/focus glyph, gantt's seven seats, chain map label, band facts + fold row, presentation field row, agenda row, people-view rows, the two notices); the exclusions byte-identical (title glyphs, project-span due marks, the slip notice, the ruler's lateness); plus `views.render_marks(directory, sel, w, h)` — the `#` manager's pure frame, shipped here per the ARQ's A-1 fold (D-4), the people view's pattern. 2 source files (`views.py`, `app.py`); tests `tests/test_milestone_marks.py` (new) with the site-enumeration guard.
- **003 — the editor Select and the `#` manager (verdict 2 A; MM-D5, D6 storage, D8; HLR-2605, HLR-2606).** `TaskModal`'s variant-A Select in `#task-chips-what` after `#f-milestone` (options `none` + classes as `Text.assemble` pieces; no `+ new class…` — the manager adds), `alt+m` priority binding, `TASK_KEYS` gains `("alt+m", "mark")`; `modals.MarkForm` (name, shape row, colour row, the live preview, the modal law); `app.MarksManager` (frame = `views.render_marks`; `escape,number_sign`/`up,k`/`down,j`/`space`/`n`/`e`; `check_action` gating); `keymap` `#` (`number_sign`, off the bar); `taskboard.tcss`. ⚠ exactly 4 SOURCE files — at the cap; it could not be cut smaller because `render_marks` already moved to 002 (D-4), and the Select, the form, the manager and the key each own a file; the packet §2 will carry the same ⚠. Tests: `tests/test_marks_manager.py` (new), the modal law's rows (`tests/test_modal_keys.py`).
- **004 — the legend, hide, search, help (MM-D6, D7; HLR-2607, HLR-2608).** `views.legend_strip`/`legend_strip_project` (only the drawn classes, then `N hidden`; nothing when none in view) under the gantt's ruler and in `render_present` with its exports; `views._hide` (shallow proxy) + `present_tasks_m` wrapping `views.present_tasks` (views.py:6179, consumed at app.py:390 and the export writer); `views.matches_m`/`filter_bar_m` wired into `matches`/`filter_bar` (views.py:3720/3751) with the round's prefix `find_class` rule; the `?` help, the gantt details line and `README.md`. Delta from the round: the strips' `◆ unclassed`/`◆ milestone` part (proto.py:257, proto.py:359-360) moves to the `_gantt_legend` details line — `legend_strip` must NOT port that part verbatim (no double-drawn `◆`). 3 source files (`views.py`, `app.py`, `README.md`); tests `tests/test_legend.py` (additions), `tests/test_readme.py`.

Out: class deletion; the `+ new class…` editor option; the `↵ only this` solo mode; `d` and `↵` inert in the shipped manager (bound in the round's `MarksWindow`, proto.py:859-862 — out of scope; the modal-keys law asserts their absence); variant A/C encodings and the class band; the legend in the agenda/people views. Carried costs, stated for the increment author: MM-D1's accepted costs — the unclassified milestone loses its red mark, the gantt month ruler shows no lateness, a class colour can resemble a project colour — and the `▲`-glyph ambiguity beside the `▲Nd` chip and the fold row (→ `BACKLOG.md` at the close, not fixed).

AT realisation per increment: AT-2602 → 001; AT-2607 → 002 (node `test_milestone_marks.py:568` minted in 002, not 001 as first mapped — the deviation is declared at `03-increments/increment-001.md:9`); AT-2603 → 002; AT-2604 → 003; AT-2601 → realised across 001 (store) + 002 (seat) + 003 (manager/editor), its node in `tests/test_marks_manager.py` — 001/002's gates treat AT-2601 as provisional (V53) without ambiguity; AT-2605, AT-2606 → 004.

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `models` (`marks.py`, new file in the layer) | the marks directory file, the class record, `SHAPES`/`COLOURS`, the slug | `Mark`, `Directory` (`load`, `find`, `add`, `edit`, `set_hidden`), `MARKS_NAME`, `SHAPES`, `COLOURS` | any widget, markup, key; any team folder; `marks.json` read/written only here |
| `models` (`models.py`) | `Task.mark` (round-trip, written only when set), `Board.marks` (memory only) | the field, the attribute | the directory's file |
| `views` | pure renders: the seat, the manager's frame, the strips, the hide wrappers, the filter | `milestone_mark`, `render_marks`, `legend_strip`, `legend_strip_project`, `_hide`, `present_tasks_m`, `matches_m`, `filter_bar_m` | reading keys; writing the directory; mutating the board (the proxy is read-only) |
| `modals` | the class Select in `TaskModal`, `MarkForm` | `MarkForm`; `TaskModal(…, marks=)`'s Select | `app` (the manager is pushed by `app`) |
| `keymap` | `#` in the seat (addition only) | `KEYMAP` | — |
| `app` | the directory's load and hand-off, `MarksManager`, the notices through the seat | `MarksManager`, `TaskboardApp.marks`, `action_marks_manager` | rendering (views) |

New import edges inside the layering: `views` → `models` (`marks.py`), `modals` → `models` (`marks.py`), `app` → `models` (`marks.py`) — all allowed by the map's §3; `marks.py` → `boards.py`, `models.py`, `people.py` (inside the layer, the `people.py` pattern reused not changed). `modals` never imports `app`.

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ (the ARQ already amended the map — marks rows at docs/ARCHITECTURE.md:41,66-70,128-134,175; A-1 folded as D-4, `render_marks` in 002).
- **Amendment D-5 (DDR, 2026-10-24):** the `modals` row's frozen cell above ("must NOT reach into: `app`") is amended to allow exactly one runtime reach — `MarkForm._save` calls `self.app.marks.add/edit` (modals.py:2189-2196) so the refused-write notice lands on the form that stays open (LLR-2606.2; PC-2's reddener). It is a screen-attribute reach, not an import edge (`modals` still never imports `app`; the increment-003 packet disclosed it as risk (3)). The rejected alternative — the `PersonForm` pattern, dismissing with data and letting `MarksManager` perform the write — splits the form's save/cancel contract across two screens and moves the validation-error surface off the form; recorded here as a real decision, not drift (trigger A3 read through the DDR per its station file).

## 3 · Diagrams

```
marks.json (~/.taskboard)  ◄── Directory._commit: file_lock ─► re-read ─► change ─► write_atomic
      │ load (never raises; unreadable → .corrupt + notice; LED .29/.40 validation)
      ▼
app.marks (Directory) ── .marks (one live dict handle → Mark) ──► board.marks (every board opened)
      │                                                             │
      │ TaskModal(marks=): Select (none + classes, Text pieces)      ▼
      │   alt+m focuses; saved task carries the class id             views.milestone_mark(task, board,
      │ MarksManager: render_marks frame; n → MarkForm ─► add/edit;  today) → (glyph, style, late_chip)
      │   space ─► set_hidden ─► marks.json; refresh                 │     the 20 sites of LLR-2604.2
      │                                                              ├─ classed: shape + colour
      ▼                                                              ├─ late: date over + ▲Nd (one channel)
team push (unchanged): the mark id travels, never the directory      ├─ reached: HOLLOW + ✓
      │ legend_strip / legend_strip_project: drawn classes + N hidden└─ unclassified: ◆ mut
      ▼                                                              ▼
_hide (proxy) ─► gantt frame; present_tasks_m ─► presentation ×3 +   matches_m/filter_bar_m: /#cls
   exports (hidden classes absent)                                   → "class" kind + the named bar
```

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `marks.*` (new module) | — | LLR-2601.1/.2 | `app`, `views`, `modals`, tests | no — one lane |
| `Task.mark`, `Board.marks` | — | `str | None` (written only when set); `{}`, the live dict | `views`, `modals`, `team_sync` (unchanged), the app | no |
| `views.milestone_mark` (new) | — | LLR-2604.1 | every milestone site, the notices, tests | no |
| `views.render_marks` (new, increment 002) | — | LLR-2606.3 | `app.MarksManager`, tests | no |
| `views.legend_strip(_project)`, `_hide`, `present_tasks_m`, `matches_m`, `filter_bar_m` (new) | — | LLR-2607.1, LLR-2608.1/.2 | `render_view`, `render_present` + exports, tests | no |
| `modals.TaskModal` | no Select | the variant-A Select, `alt+m`; options as Text pieces | the editor suites, `test_modal_keys.py` | no |
| `modals.MarkForm` (new) | — | LLR-2606.2 | `app.MarksManager`, the law | no |
| `app.MarksManager` (new) | — | LLR-2606.1 | `keymap`/`check_action`, tests | no |
| `KEYMAP` | `#` free | + `#` (`marks_manager`, `bar=False`) — addition only | `app_bindings`, `?`, the palette, README laws | **frozen: additions only** |
| `people.py` `Directory`/`handle_for` | the reuse pattern | **unchanged** — reused, not edited | `marks.py` | **FROZEN** |
| `boards.file_lock`/`keep_aside`, `models.write_atomic`/`clean_strings` | the lock/atomic/clean core | **unchanged** | `marks.py` | **FROZEN** |
| the section-3 exclusion sites (title glyphs, project-span due marks, slip notice, ruler lateness) | as they are | **byte-identical behaviour** | every view suite | **FROZEN** |
| `Board._to_dict`'s byte-preservation contract | defaults dropped | `mark` joins the dropped-when-`None` set | every board-file test | **FROZEN** |

**A frozen interface is not touched inside a lane.** If a lane needs to change one, the work returns to
the trunk — that is trigger **A3**. (One lane here; the freeze list is what the increment diffs are reviewed against.) Enforcement instrument: the project has no frozen-file guard tests and no `docs/engineering-rules.md`, so C-27's automated guard has no home — the instrument is the code-reviewer pass (the commission's swarm): each increment's diff is read against `base_ref` and names the frozen functions/sites — `people.py`'s `Directory`/`handle_for`, `boards.file_lock`/`keep_aside`, `models.write_atomic`/`clean_strings`, the section-3 exclusion sites, `Board._to_dict`'s byte-preservation — as untouched, and the packet §4b records it.

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-2601 | 0/A | the load table (missing, mixed with bad id/name/shape/colour/type, 61-char and newline names, the ANSI payload); `add`/`edit`/`set_hidden`; the slug; `find` prefix-only; `hidden` coerced to `bool` | the colour/type validation skipped; the one-line flattening dropped; `find` matching inside the name; `hidden` kept as a raw string |
| AT-2601 | B | `# n name shape colour alt+s` → `<home>/.taskboard/marks.json` on disk holds the class; restart keeps it; the gantt draws the class glyph in its colour; `alt+m` in the editor carries the class | `_commit` updating memory only, or writing to a wrong filename (restart loses the class / the file is absent); the seat returning `◆` always. (The write skipping the on-disk re-read reddens the two-window arm — AT-2602/TC-2603 — not this one.) |
| TC-2602 / AT-2607 | 0 / B | the `mark` round-trip (written only when set, bytes kept); unknown ids kept byte-for-byte; untick keeps the field; a push carries the id, never a class name (the push arm's node names reconcile at P4 with LLR-2602.2's `-k 2607` selector in `tests/test_marks_directory.py` — a TC-2607 node name, not an AT-only name) | `_to_dict` writing `mark: null`; an unknown id dropped on save; a push writing a class name |
| TC-2601 (LLR-2601.3 hand-off) | A | `board.marks is app.marks.marks` before and after a board switch; `after_move` carries it; the unreadable-file mount notice shows once | `_label_board` not setting `marks` (a switched board draws unclassified); `Board._to_dict` writing `marks` |
| TC-2603 / AT-2602 | 0 / B | two directories on one file both survive; 10 interleaved adds; the corrupt copy never overwritten; a no-mark board's bytes equal; the lock and failed-write arms | the re-read under the lock dropped; `keep_aside` overwriting an earlier copy; a no-mark board gaining bytes |
| TC-2604 / AT-2603 | 0 / B | the seat's truth table (classed/late/reached/unclassified × glyph/style/chip); `▲Nd` and the `over` channel; the 20-site enumeration; the exclusions untouched | the seat returning `◆` always; the chip empty on a late classed milestone; a site hard-coding `c("◆", …)` |
| TC-2605 | 0/A | the Select's mount point and options (Text pieces, no `+ new`); `alt+m` focuses and opens; `TASK_KEYS` carries it; `none` saves no `mark`; an empty directory composes no Select and the tab walk of `tests/test_edit_window.py` stays green | the Select mounted elsewhere; `alt+m` unbound; options built as markup strings; the Select composed for an empty directory |
| TC-2606 / AT-2604 | A / B | `MarkForm`'s rows and law; `MarksManager`'s bindings and `check_action` gating; `#` from the main screen and the home; the law's inventory rows; a failed `Directory.add/edit` shows `The marks directory was not saved: <reason>` with the form kept | a form button without a direct key; the seat keys acting behind the manager; `#` acting over a modal; the form dismissed (or nothing said) on a failed write |
| TC-2606 (render_marks) | 0 | the frame's rows at 76/60/40 cells; the chosen row shaded; a hidden class dimmed; the empty directory's line | the row pad/cut to `w` dropped; the dim style for hidden dropped |
| TC-2607 / AT-2605 | 0 / B | the strips list only the drawn classes + `N hidden`; none when none in view; the presentation's views and exports carry them; `?` names the classes and the `/#cls` filter; the class entries actually render in the painted frame (styled-segment export) at 118×30 and 80×24 — else the conditional visibility of `_gantt_legend` (spare-row only, views.py:2965) is ledgered as an accepted cost per LLR-2607.2's hedge (the painted-frame assertion is recommended) | the legend counting all classes, not the drawn ones; the strip drawn with no classed milestone in view; the strip computed but never painted into the frame |
| TC-2608 / AT-2606 | 0 / B | `/#pay` keeps exactly that class's milestones in kanban and gantt; the bar names the class; `/#zzz` keeps nothing; hidden classes gone from the gantt, presentation ×3 and the export's bytes | `present_tasks_m` not filtering hidden classes; the class rule falling through to text; one export still drawing a hidden class |
| TC-2407 (extended) | A | `MarksManager` and `MarkForm` in the modal law, buttons read along the bases | `alt+s` unbound on `MarkForm` |

**5b · The gauntlet controls that apply, and who pays:** C-40 (each new assertion RED on `base_ref` (`7e66e0e`, clean worktree — no other session reading) or by the declared mutation above; the orchestrator, `mutate-00N.py` beside its transcript, restored by hash); C-19 (one complete run per gate; the suite in three sequential chunks at P4, `env -u NO_COLOR` on every command); C-42 (ATs read the screen's text via the styled-segment export, the notices and the files); C-17 (markup safety paid in 001/003: the hostile TC arms of TC-2601/TC-2605/TC-2606 — the `[b]x[/b]` and ANSI payloads rendered literally); B1's reverse census in each packet; C-18 (each AT exactly one node); C-20 (`marks.py` and `milestone_marks_fixture.py` are net-new files — the base_ref RED, `evidence/red-p1.txt`, covers module absence); the law-driven updates (`test_modal_keys.py`, `test_legend.py`, `test_readme.py`) named in their packets; the frozen-interface enforcement of §4 paid by the code-reviewer pass, recorded in each packet §4b. The `security-reviewer` reviews `marks.py` at 001's gate (the commission).

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| a class list per board (in each `board.json`) | MM-D2: one directory for every board; a class written once classifies anywhere |
| state in the glyph (variant A: colour = state) / state as the cell's ground (variant C) | the operator chose D1 B: shape+colour say the class, state moves to text |
| the editor's `+ new class…` option (proto.py:567-568) | adding a class is the manager's job (`n`); the Select only picks — one home for the write path |
| a `mark: {id, name, …}` blob on the task | MM-D3: the id only; the directory is the one source of names/shapes/colours |
| a mutable module-level directory (the round's `CLS`/`HIDDEN` globals) | hundreds of apps per suite; the attributes `Board.marks` / the app's `Directory`, like `Board.people` and `Board.label`, are per app |
| `_hide` filtering inside `present_tasks` itself | `present_tasks` is consumed by the presentation screen and the export writer (app.py:390); one wrapper keeps both, and the board object stays untouched (LLR-2608.1) |
| the manager's frame composed in `app` (the round's `_draw` inline) | the ARQ's A-1, folded as D-4: `views.render_marks` pure in 002, the people view's pattern; 003 keeps 4 source files |

Risks: `_hide`'s shallow proxy must not leak into a save (it never reaches `Board.save`; TC-2608 asserts the board object untouched); the agenda/people rows gain a mark where today there is none — new seats, covered by the enumeration test; `render_marks` ships in 002 with its only consumer in 003 — one increment of tested-but-unwired code, accepted per D-4; the manager's counts read every board of the registry at open (the people view's `peek_board` precedent; no latency criterion); `▲` beside `▲Nd` and the fold row (MM-D5, logged, not fixed).

**Questions carried to the PDR** (the contract left these open; recommended answers):
1. `COLOURS`' exact membership — the contract declares it NEW without enumerating it. **Recommend:** `COLOURS = ["cyan", "amber", "violet", "pink", "green", "orange", "sky", "lime"]`, the round's `SWATCH` (proto.py:86), named tones the app's `HEX` map already defines.
2. The gantt details-line seat — hedged «assumed — verify in Phase 3» (QA-3). **Recommend:** proceed treating `_gantt_legend` (views.py:2929) as that line; the increment-004 gate confirms or amends by ledger, as LLR-2607.2 states.
3. `_hide` as `copy.copy` proxy vs a filtered task-list parameter threaded through the gantt frame. **Recommend:** the round's shallow proxy, applied at frame entry (proto.py:294-299) — zero signature churn in `_gantt_frame`, read-only by construction.

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | §1 (the four increments and their files), §4; the ARQ-amended map rows |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | `tests/milestone_marks_fixture.py` (the round's boards + four example classes, synthetic); the conftest home seam (tests/conftest.py:26-35); the styled-segment export helper for tone assertions (§5.1 of the contract); the captures harness (`prototypes/milestone_marks/shoot.ps1` pattern, unique `m01-` windows) |
| proposed test cases | layers 0/A/B and the DDR | §5 → `01-requirements.md`'s thresholds and the increments' mutation batteries |
| design → requirement traceability | the matrix and the DDR | the Requirements covered row; §4's table; each increment packet §2's `Traces to` column |

- ⚠ Any row whose consumer column is empty: **remove the output, or explain why it is being produced.**

## 8 · Parallelisation plan *(only if the batch forks)*

Not applicable — one lane (A4 not fired; D-3: four sequential increments).
