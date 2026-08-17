# Requirements Document — taskboard — Batch 2026-08-16-batch-05

> **Artifact language:** English (`state.json.language = en`).
> **Base ref:** `bfc000d` (= `origin/main`, HEAD, merge-base — RC-1 PASS).
> **Normative convention:** `shall` is binding and appears ONLY inside HLR/LLR **Statement** lines. `should` never appears inside one.

---

## 1. Introduction

### 1.1 Purpose

Define, at HLR and LLR level, the change that improves key-binding
discoverability in taskboard by implementing the operator-approved **E + F**
proposal: a fuzzy command palette summoned by `?` and a layered keybar toggled
by `;`.

### 1.2 Scope

**In scope**
- `taskboard/keymap.py`: the `KEYMAP` contract, `Key` tuple, `KeyBar`,
  `app_bindings()`, `fit_bar()`, `render_key_bar()`.
- `taskboard/app.py`: `TaskboardApp`, `action_legend()`, `check_action()`,
  `BOARD_ACTIONS`.
- `taskboard/modals.py`: modal pattern reused for the new `CommandPalette`.
- `taskboard/views.py`: `HEX` palette used for bar markup (read-only).
- `README.md`: key-binding table update.

**Out of scope, explicitly**
- New board actions or mutation behaviour.
- Redesign of `LegendModal` beyond making it reachable from the palette or the
  layered bar.
- The aperture's `HelpScreen` surface (`app.py:328–337`) — it is not on the
  `?` path being changed.
- Darkside, ledger, prism, or kanban follow-ups.

### 1.3 Definitions, acronyms, abbreviations

| Term | Definition |
|------|------------|
| **palette** | The floating command-search panel opened by `?`. |
| **primary layer** | The default keybar state showing only essential keys. |
| **more layer** | The secondary keybar state showing all commands, grouped. |
| **the seat** | `KEYMAP` in `taskboard/keymap.py` — the single source of truth for all bindings. |
| **view-relevant key** | A `Key` whose `views` is `None` or contains the current view mode. |
| **primary key** | A `Key` marked for display in the primary layer. |

### 1.4 References

- `.dev-flow/2026-08-16-batch-05/PLAN.md` — the living plan (objective, stories, risks, decision log).
- `prototypes/keybar_ideas/out/keybar-ideas.html` — approved deliberation artifact.
- `~/.claude/templates/dev-flow/req-template.md` — the artifact shape enforced here.
- IEEE 830-1998 · EARS (Easy Approach to Requirements Syntax).

### 1.5 Document overview

§2 states the world this change lands in. §3 states two HLRs, each with a
black-box Acceptance block. §4 decomposes them into LLRs with declared touched
symbols (C-26). §5 is the validation skeleton for `qa-reviewer`. §6 carries
decisions and risks.

---

## 2. Overall description

### 2.1 Product perspective

taskboard is a single-process Textual TUI with no network and no persistence
beyond a local JSON board. This batch is a pure interaction change: it adds a
new modal and a new rendering mode for the existing keybar. No trust boundary is
crossed. `security_required: false` — no pattern matched.

The keybar is governed by a strict contract: `KEYMAP` is the only place a key is
declared, every shown key works, and every working key is shown. Any change that
weakens that contract breaks the app's most visible surface.

### 2.2 Product functions

1. Pressing `?` opens a command palette listing every command derived from
   `KEYMAP`.
2. Typing in the palette filters the list by substring match against labels and
   key shows.
3. Pressing `↵` on a highlighted palette item executes the bound action.
4. Pressing `esc`, `?`, or `q` closes the palette without executing anything.
5. The keybar displays a primary layer showing only essential keys.
6. Pressing `;` toggles the keybar to a more layer showing all view-relevant
   keys grouped by category.
7. Pressing `esc` or `;` again returns the keybar to the primary layer.
8. The layer state survives view switches and terminal resizes.

### 2.3 User characteristics

One role: the board's owner, an expert terminal user who wants fast access to
commands without memorising every binding.

### 2.4 Constraints

| # | Constraint | Source |
|---|---|---|
| C1 | **Every key declared in `KEYMAP` is a real app action.** | `tests/test_keymap.py:67` |
| C2 | **Every app binding comes from `KEYMAP`.** | `tests/test_keymap.py:39` |
| C3 | **Words drop before keys; dropped keys are counted.** | `tests/test_keymap.py:110` |
| C4 | **Universal keys drop last.** | `tests/test_keymap.py:124` |
| C5 | **README key table documents every bound key.** | `tests/test_keymap.py:348` |
| C6 | **≤4 source files per increment.** | `PLAN.md` §Increment plan |
| C7 | **`shall` appears only inside HLR/LLR statements.** | This document |

### 2.5 Assumptions and dependencies

- `KEYMAP` already drives both `TaskboardApp.BINDINGS` and the keybar; this
  batch extends it rather than replacing the mechanism.
- `check_action` already blocks `BOARD_ACTIONS` when a modal is on the stack,
  so the palette inherits the same guard.
- `LegendModal` is reusable; its only change is how it is reached.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|---|---|---|---|
| **US-E** | As the board's owner, I want to press `?` and search commands by name so I can run one without memorising its key. | Phase 0 intake, approved prototype E | **READY** |
| **US-F** | As the board's owner, I want the footer to show only essential keys and reveal the rest on `;`, so the bar stays readable. | Phase 0 intake, approved prototype F | **READY** |

---

## 3. High-level requirements (HLR)

### 3.0 THE CANONICAL `AT` REGISTER

Every acceptance below is black-box, falsifiable, and tied to one user story.

| id | story | subject | observation surface | reddening mutation (C-40) |
|---|---|---|---|---|
| **AT-E001** | US-E | Pressing `?` opens the command palette and lists every `KEYMAP` command. | `App.run_test()` | remove one `KEYMAP` entry from the palette source → list shrinks → red |
| **AT-E002** | US-E | Typing filters the palette by substring; a non-matching query yields an empty list. | `App.run_test()` | disable filtering → all options remain → red |
| **AT-E003** | US-E | Pressing `↵` on a highlighted command executes its action (e.g. opens the add-task modal). | `App.run_test()` | make `↵` close without action → no modal → red |
| **AT-E004** | US-E | `esc`, `?`, or `q` closes the palette without executing anything. | `App.run_test()` | make the close binding run the current command → modal appears → red |
| **AT-F001** | US-F | The primary layer shows only primary keys; a non-primary key is absent. | `render_key_bar()` / `App.run_test()` | show all keys in primary layer → non-primary key appears → red |
| **AT-F002** | US-F | Pressing `;` toggles the bar to the more layer; pressing `;` again returns to primary. | `App.run_test()` | make `;` a no-op → layer unchanged → red |
| **AT-F003** | US-F | Pressing `esc` while the more layer is active returns to the primary layer. | `App.run_test()` | make `esc` leave more layer active → red |
| **AT-F004** | US-F | The more layer shows every view-relevant key from `KEYMAP`. | `render_key_bar()` / `App.run_test()` | omit one group → missing key → red |
| **AT-F005** | US-F | The more layer survives view switches and resizes. | `App.run_test()` | reset to primary on view switch → red |

### HLR-001 — Command palette (`?`)

- **Traceability:** US-E
- **Statement:** When the user presses `?`, the system **shall** open a floating
  command palette that lists every command bound in `KEYMAP`; typing **shall**
  filter the list by substring match against each command's label and shown key;
  pressing `↵` on a highlighted command **shall** execute its bound action; and
  pressing `esc`, `?`, or `q` **shall** close the palette without executing any
  action.
- **Rationale (informative):** The current bar can only afford primary keys. A
  palette lets a user find and run any command by name, removing the memorisation
  barrier.
- **Validation:** `test`
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** The user presses `?`, types "add", sees "Add task",
    presses `↵`, and the add-task modal opens.
  - **Shipped surface:** `App.run_test()` — the live app with a simulated
    terminal.
  - **Deliverable + observation:** screen state before and after each keypress.
  - **Acceptance test(s):** `AT-E001`, `AT-E002`, `AT-E003`, `AT-E004`.
  - **Boundary catalog (QC-3):**
    - ☑ **empty query** — shows all commands.
    - ☑ **no matches** — shows an empty/no-match state, does not crash.
    - ☑ **action with parameters** — `phase_move(-1)` executes with its declared
      parameter.
    - ☑ **modal already open** — palette is the top screen; its close bindings
      dismiss it.

### HLR-002 — Layered keybar (`;`)

- **Traceability:** US-F
- **Statement:** The keybar **shall** render a primary layer showing only the
  designated primary keys; pressing `;` **shall** toggle a more layer that shows
  every view-relevant key grouped by category; pressing `esc` or `;` again
  **shall** return the bar to the primary layer; and the layer state **shall**
  survive view switches and terminal resizes.
- **Rationale (informative):** A single-row bar carrying ~30 bindings becomes
  unreadable. A primary layer keeps the essentials visible; the more layer
  exposes the rest on demand while preserving the contract that every working
  key is discoverable.
- **Validation:** `test`
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** The bar shows `? map · ; more · 1 Lanes · 2 Agenda ·
    a Add · e Edit · ↓↑←→ Nav · ↵ Open`. After `;` it shows grouped categories
    such as Phase/Priority, Kanban, Date, Misc, System.
  - **Shipped surface:** `render_key_bar()` and the live app footer.
  - **Deliverable + observation:** rendered bar text at each state transition.
  - **Acceptance test(s):** `AT-F001`, `AT-F002`, `AT-F003`, `AT-F004`, `AT-F005`.
  - **Boundary catalog (QC-3):**
    - ☑ **narrow width** — more layer degrades by dropping whole keys with a
      `+N` count, never by truncating a group label.
    - ☑ **view-scoped keys** — the more layer shows only keys relevant to the
      current view.
    - ☑ **universal keys** — `?`, `q`, `;` appear in both layers.

---

## 4. Low-level requirements (LLR)

### LLR-E.1 — `?` maps to the palette action

- **Traceability:** HLR-001
- **Statement:** `KEYMAP` **shall** contain exactly one entry mapping `?` to
  the action `palette`, with label "Cmd" and `universal=True`.
- **Touched symbols (C-26):** `KEYMAP` (`keymap.py:43`), `Key`
  (`keymap.py:32`), `app_bindings()` (`keymap.py:106`).
- **Validation:** `inspection`
- **Executed verification:** `rg -n "question_mark|action_legend" taskboard/keymap.py`
  → the old `legend` action entry is replaced; `pytest tests/test_keymap.py`.
- **Acceptance criteria (informative):** The old `action_legend` binding is
  removed from `KEYMAP`; the legend remains reachable from the palette or the
  layered bar.

### LLR-E.2 — App exposes `action_palette`

- **Traceability:** HLR-001
- **Statement:** `TaskboardApp` **shall** define `action_palette()` that pushes
  the `CommandPalette` modal.
- **Touched symbols (C-26):** `TaskboardApp` (`app.py:161`), new method
  `action_palette`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_keymap.py::test_every_shown_key_has_a_real_action_on_the_app`
  and `pytest tests/test_app.py -k palette`.
- **C-40 mutation that reddens this:** rename the method → `hasattr` fails for
  `?` → `AT-E001` red.

### LLR-E.3 — `CommandPalette` modal

- **Traceability:** HLR-001
- **Statement:** `taskboard/modals.py` **shall** contain a `CommandPalette`
  modal with an `Input` for search, an `OptionList` for results, and bindings
  for `escape`, `question_mark`, and `q` to dismiss, plus `enter`, `up`, and
  `down` to select and run.
- **Touched symbols (C-26):** `modals.py` (new class), `Binding`, `Input`,
  `OptionList`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k palette`.
- **Acceptance criteria (informative):** Follows the `EmojiPicker` / `ProjectPicker`
  modal pattern in the same file.

### LLR-E.4 — Palette options derived from `KEYMAP`

- **Traceability:** HLR-001
- **Statement:** `CommandPalette` **shall** build its option list from `KEYMAP`
  so that every bound action is reachable and no action appears that is not in
  `KEYMAP`.
- **Touched symbols (C-26):** `KEYMAP`, `CommandPalette.compose` / `on_mount`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k palette_lists_all_keymap_commands`.
- **C-40 mutation that reddens this:** hard-code one extra option → count
  exceeds `len(KEYMAP)` → `AT-E001` red.

### LLR-E.5 — Execute selected command

- **Traceability:** HLR-001
- **Statement:** When the user confirms a palette option, `CommandPalette`
  **shall** dispatch the corresponding action on the app, parsing any
  parenthesised parameters exactly as Textual does.
- **Touched symbols (C-26):** `CommandPalette.action_run`, `App.call_action` or
  equivalent dispatch.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_app.py -k palette_runs_command`.
- **C-40 mutation that reddens this:** make the run action close without
  dispatch → `AT-E003` red.

### LLR-E.6 — Fuzzy/substring filter

- **Traceability:** HLR-001
- **Statement:** As the user types in the palette input, the option list
  **shall** be filtered to items whose label or shown key contains the typed
  substring, case-insensitively.
- **Touched symbols (C-26):** `Input`, `OptionList`, `CommandPalette._filter`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_app.py -k palette_filters`.
- **C-40 mutation that reddens this:** return the full list regardless of input
  → `AT-E002` red.

### LLR-E.7 — Board actions blocked while palette is open

- **Traceability:** HLR-001
- **Statement:** While `CommandPalette` is the top screen, no board-editing
  action **shall** fire.
- **Touched symbols (C-26):** `check_action()` (`app.py:210`), `BOARD_ACTIONS`
  (`app.py:199`).
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_app.py -k palette_blocks_board_actions`.
- **Acceptance criteria (informative):** Inherited from the existing modal
  guard: `len(self.screen_stack) > 1` blocks `BOARD_ACTIONS`.

### LLR-F.1 — `;` maps to the layer toggle action

- **Traceability:** HLR-002
- **Statement:** `KEYMAP` **shall** contain exactly one entry mapping `;` to
  the action `layer_toggle`, with label "more" and `universal=True`.
- **Touched symbols (C-26):** `KEYMAP` (`keymap.py:43`), `Key`
  (`keymap.py:32`), `app_bindings()` (`keymap.py:106`).
- **Validation:** `inspection`
- **Executed verification:** `pytest tests/test_keymap.py`.
- **C-40 mutation that reddens this:** remove the `;` entry → bar never enters
  more layer → `AT-F002` red.

### LLR-F.2 — `KeyBar` holds layer state

- **Traceability:** HLR-002
- **Statement:** `KeyBar` **shall** store a `layer_mode` state with values
  `"primary"` (default) or `"more"`.
- **Touched symbols (C-26):** `KeyBar` (`keymap.py:184`).
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_keymap.py -k layer_mode`.

### LLR-F.3 — Primary layer rendering

- **Traceability:** HLR-002
- **Statement:** When `layer_mode` is `"primary"`, `render_key_bar()` **shall**
  show only the designated primary keys plus all universal keys, using the
  existing fit/drop logic.
- **Touched symbols (C-26):** `render_key_bar()` (`keymap.py:174`), `fit_bar()`
  (`keymap.py:128`), `KeyBar.refresh_bar()` (`keymap.py:196`).
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_keymap.py -k primary_layer`.
- **C-40 mutation that reddens this:** show all keys in primary layer →
  `AT-F001` red.

### LLR-F.4 — More layer rendering

- **Traceability:** HLR-002
- **Statement:** When `layer_mode` is `"more"`, `render_key_bar()` **shall**
  show every view-relevant key grouped by category, with category separators
  that are not counted as keys.
- **Touched symbols (C-26):** `render_key_bar()`, `fit_bar()`, `Key`
  (`keymap.py:32`) — may gain a `group` field.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_keymap.py -k more_layer`.
- **C-40 mutation that reddens this:** omit one category → `AT-F004` red.

### LLR-F.5 — App layer toggle action

- **Traceability:** HLR-002
- **Statement:** `TaskboardApp` **shall** define `action_layer_toggle()` that
  flips `KeyBar.layer_mode` between `"primary"` and `"more"` and refreshes the
  bar.
- **Touched symbols (C-26):** `TaskboardApp` (`app.py:161`), new method
  `action_layer_toggle`, `KeyBar.refresh_bar`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_keymap.py::test_every_shown_key_has_a_real_action_on_the_app`
  and `pytest tests/test_app.py -k layer_toggle`.

### LLR-F.6 — `esc` returns to primary layer

- **Traceability:** HLR-002
- **Statement:** When the more layer is active and the user presses `escape`,
  the system **shall** return the keybar to the primary layer.
- **Touched symbols (C-26):** `TaskboardApp.action_layer_toggle`,
  `KeyBar.layer_mode`.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_app.py -k esc_returns_to_primary`.
- **C-40 mutation that reddens this:** make `escape` a no-op in more layer →
  `AT-F003` red.

### LLR-F.7 — Layer state survives view switch and resize

- **Traceability:** HLR-002
- **Statement:** `KeyBar.refresh_bar()` **shall** preserve `layer_mode` across
  view changes and `on_resize` events, recomputing only the keys shown.
- **Touched symbols (C-26):** `KeyBar.on_resize` (`keymap.py:193`),
  `KeyBar.refresh_bar`, `App.action_view` (`app.py:609`).
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_app.py -k layer_survives`.
- **C-40 mutation that reddens this:** reset layer to primary inside
  `refresh_bar` → `AT-F005` red.

### LLR-F.8 — README key table updated

- **Traceability:** HLR-001, HLR-002
- **Statement:** `README.md` **shall** document `?` as the command palette and
  `;` as the layer toggle.
- **Touched symbols (C-26):** `README.md`.
- **Validation:** `inspection`
- **Executed verification:** `pytest tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat`.
- **C-40 mutation that reddens this:** omit `;` from the table → README test red.

---

## 5. Validation strategy

### 5.1 Methods

**Layer B — black-box `AT-NNN` (`acceptance`).** All nine ATs live in
`tests/test_app.py` or a new `tests/test_keybar.py`, one `def test_…` per AT
(C-18). They drive `App.run_test()` and reference only shipped surfaces.

**Layer A — white-box `TC-NNN`** (`test` / `inspection`), living in the files
named per row below.

**Ratified stack:** `pytest` + `pytest-asyncio` (`pyproject.toml`).

### 5.2 Dual-traceability table

**Behavioral chain (black-box) — per user story.**

| US | Observable outcome | Shipped surface | Acceptance test (`AT-NNN`) | Observed? |
|---|---|---|---|---|
| US-E | `?` opens a palette listing every `KEYMAP` command | `App.run_test()` | `AT-E001` | Phase 3 |
| US-E | Typing filters the palette | `App.run_test()` | `AT-E002` | Phase 3 |
| US-E | `↵` runs the highlighted command | `App.run_test()` | `AT-E003` | Phase 3 |
| US-E | `esc`/`?`/`q` closes without action | `App.run_test()` | `AT-E004` | Phase 3 |
| US-F | Primary layer shows only primary keys | `render_key_bar()` / `App.run_test()` | `AT-F001` | Phase 3 |
| US-F | `;` toggles the more layer | `App.run_test()` | `AT-F002` | Phase 3 |
| US-F | `esc` returns to primary layer | `App.run_test()` | `AT-F003` | Phase 3 |
| US-F | More layer shows every view-relevant key | `render_key_bar()` / `App.run_test()` | `AT-F004` | Phase 3 |
| US-F | Layer survives view switch and resize | `App.run_test()` | `AT-F005` | Phase 3 |

**Functional chain (white-box) — per requirement.**

| Requirement | Method | Test Case (`TC-NNN`) | Node / notes |
|---|---|---|---|
| HLR-001 | test | `TC-E001` | rolls up `TC-E002`…`TC-E007` |
| LLR-E.1 | inspection | `TC-E002` | `KEYMAP` entry for `?` is `palette` |
| LLR-E.2 | test (unit) | `TC-E003` | `TaskboardApp.action_palette` exists |
| LLR-E.3 | test (unit) | `TC-E004` | `CommandPalette` modal bindings |
| LLR-E.4 | test (unit) | `TC-E005` | options derive from `KEYMAP` |
| LLR-E.5 | test (integration) | `TC-E006` | `↵` dispatches action |
| LLR-E.6 | test (unit) | `TC-E007` | substring filter |
| LLR-E.7 | test (integration) | `TC-E008` | board actions blocked while palette open |
| HLR-002 | test | `TC-F001` | rolls up `TC-F002`…`TC-F008` |
| LLR-F.1 | inspection | `TC-F002` | `KEYMAP` entry for `;` is `layer_toggle` |
| LLR-F.2 | test (unit) | `TC-F003` | `KeyBar.layer_mode` state |
| LLR-F.3 | test (integration) | `TC-F004` | primary layer rendering |
| LLR-F.4 | test (integration) | `TC-F005` | more layer rendering |
| LLR-F.5 | test (unit) | `TC-F006` | `TaskboardApp.action_layer_toggle` |
| LLR-F.6 | test (integration) | `TC-F007` | `esc` returns to primary |
| LLR-F.7 | test (integration) | `TC-F008` | layer survives view/resizing |
| LLR-F.8 | inspection | `TC-F009` | README table matches seat |

### 5.3 Batch acceptance criteria

- 100 % of LLRs covered by ≥1 `TC` with a pass result — **17 `TC`s over 16
  requirements, 0 gaps**.
- Every user story has ≥1 passing `AT-NNN` — **US-E: 4 ATs · US-F: 5 ATs**.
- 0 blocker fails.
- `pytest tests/ -q`: **0 failures, 0 skips**. A skip is a fail.
- Every named C-40 mutation has been run and observed to redden its AT.
- The keybar contract holds: every shown key works, every working key is shown.

---

## 6. Appendices

### 6.1 Relevant design decisions

| # | Decision | Rationale | Alternatives considered and rejected |
|---|---|---|---|
| **D-1** | **`?` is repurposed for the palette.** | The operator approved E + F; `?` is the natural discovery key. | Keep `?` for legend and bind palette to `ctrl+p` — rejected by operator choice. |
| **D-2** | **`;` is the layer toggle.** | `;` is unused, physically near the home row, and matches the prototype. | Use `space` or a chord — rejected; `space` is used for scrolling, chords are not in the seat. |
| **D-3** | **The legend remains reachable from the palette / layered bar rather than keeping a dedicated key.** | The palette is the new discovery surface; duplicating it on a second key wastes scarce key real estate. | Drop `LegendModal` entirely — rejected; it still explains marks the bar cannot show. |
| **D-4** | **The more layer groups keys by category using a new optional `group` field on `Key`.** | Keeps the seat as the single source of truth and lets the more layer render groups without a second list. | Maintain a separate group table — rejected; it would drift from `KEYMAP`. |

### 6.2 Open risks

| # | Risk | Class | Mitigation / owner |
|---|---|---|---|
| **R-1** | Repurposing `?` changes a deeply worn muscle-memory key. | ux | `ux-reviewer` evaluates at PDR; old legend is reachable from palette. |
| **R-2** | The more-layer grouping may overflow narrow widths and interact badly with the `+N` count. | rendering | Width sweep in `AT-F004`; group separators are not counted as keys. |
| **R-3** | `test_keymap.py` oracles treat `?` and the action list as constants; adding `;` changes expected counts. | test hygiene | Update oracles, do not weaken assertions. |
| **R-4** | Palette action dispatch for parameterized actions (`phase_move(-1)`) must parse parameters exactly like Textual. | correctness | Unit test `TC-E006` covers a parameterized command. |

### 6.3 Premise evaluation (C-43)

All probes executed 2026-08-16 against the tree at `bfc000d`.

| # | Premise | Verdict | Evidence |
|---|---|---|---|
| **P-1** | `KEYMAP` is the single seat for bindings. | ✅ TRUE | `keymap.py:6`, `app.py:173`. |
| **P-2** | `check_action` blocks `BOARD_ACTIONS` on any modal stack > 1. | ✅ TRUE | `app.py:222–226`. |
| **P-3** | `LegendModal` is reusable without signature change. | ✅ TRUE | `modals.py:1020–1059`; no selection parameter, so it can be called from the palette. |
