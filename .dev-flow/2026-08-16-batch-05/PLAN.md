# PLAN — 2026-08-16-batch-05 (living compendium)

**Batch objective.** Improve discoverability of taskboard key bindings by
implementing the operator-approved **E + F** proposal:

- **E · Command palette:** pressing `?` opens a floating fuzzy-search panel of
  all commands; type to filter, press `↵` to run.
- **F · Layered keybar:** the footer shows only essentials; pressing `;` toggles
  a second layer with every command grouped by category; `esc` or `;` returns to
  the primary layer.

The deliberation artifacts are in `prototypes/keybar_ideas/`.

**Mode:** `core` (2 stories, interaction change, touched contract). Language: `en`.
**Where we are:** Phase 6 — **closed**. Validation passed; merge gate approved.

## Verified at intake (executed, not asserted)

- **RC-1 base currency:** `git fetch origin` 2026-08-16 → `HEAD == origin/main ==
  merge-base == bfc000d`. Branch current. Working tree has one untracked
  deliberation directory: `prototypes/keybar_ideas/`.
- **Flow currency (C-45 PULL):** `~/.claude/skills/dev-flow` == backup repo
  `~/kimi/agent-skills/dev-flow` at **rev25** (0 real diffs, 0 missing both
  directions). Verified by full-tree walk.
- **Backlog read:** `.dev-flow/BACKLOG.md` (refreshed 2026-08-07). No open item
  blocks this batch.
- **Prototypes approved:** operator verdict 2026-08-16: implement proposal **E + F**
  for key-binding discoverability (`prototypes/keybar_ideas/out/keybar-ideas.html`).

## Stories (2) — INVEST

| id | story | status | observable outcome (the AT surface) |
|---|---|---|---|
| R-01 | **US-E:** As a taskboard user, I want to press `?` and search commands by name, so I can run a command without memorising its key. | **DONE** | `?` opens a palette; typing filters; `↵` executes; `esc`/`?`/`q` closes. |
| R-02 | **US-F:** As a taskboard user, I want the footer to show only essential keys and reveal the rest on `;`, so the bar stays readable. | **DONE** | Primary layer shows essentials; `;` toggles grouped more-layer; `esc`/`;` returns. |

## Trigger evaluation (id · verdict · probe)

- **B1** (touched symbol asserted by other requirements' tests) — **FIRED**:
  `grep -rl "KEYMAP\|KeyBar\|app_bindings\|TaskboardApp" tests/` →
  `test_keymap.py`, `test_app.py`, `test_legend.py`, `test_archive.py`, etc.
  → reverse census (C-26) at Phase 2.
- **B2** (file location move) — did not fire: no file moves planned.
- **B3** (byte-identical goldens) — did not fire: no `goldens/` dir.
- **B4** (artifact consumed downstream) — did not fire: deliberation SVGs are
  read-only artifacts.
- **C** (security patterns) — did not fire: no auth/secrets/network/destructive
  DB. The palette executes existing app actions only; no new interpolation of
  user text.
- **D** (interaction change) — **FIRED**: `?` repurposed, `;` added, new modal
  → `ux-reviewer` joins the PDR.
- **E** (≥3 stories) — did not fire: 2 stories; lane stays `core` because D
  fired and the keybar contract is a load-bearing surface.
- **F** (flow currency) — verified current (rev25); backlog refresh due at
  Phase 6 (last: 2026-08-07).

## Increment plan (≤4 source files each, tests uncapped)

| inc | content | source files (planned) | status |
|---|---|---|---|
| 1 | R-02 (F): layered keybar — `;` binding, layer state, primary/more rendering, `action_layer_toggle` | `keymap.py`, `app.py` | **DONE** |
| 2 | R-01 (E): command palette — repurpose `?`, `CommandPalette` modal, fuzzy filter, execute action | `modals.py`, `app.py`, `keymap.py` | **DONE** |
| 3 | Integration + contract tests + README key table update | `README.md`, `tests/test_keymap.py`, `tests/test_legend.py` (tests only) | **DONE** |

## Risks / watch-items

- **`?` is a contract change.** `?` currently opened `LegendModal` via
  `action_legend`. Repurposing it for the palette means the legend must remain
  reachable — it is reachable from the more-layer label and the palette is the
  new discovery surface. The old `HelpScreen` on the aperture (`action_legend`'s
  aperture branch) stays untouched.
- **The keybar contract is the seat.** `KEYMAP` is the only place a key is
  declared (`keymap.py:6`). Every key shown must work and every working key
  must be shown. The more-layer obeys the fit/drop contract; the palette is a
  separate surface that does not weaken it.
- **`test_keymap.py` needed surgical updates.** Adding `;` and changing `?`'s
  action changed oracle constants; tests were updated, not weakened.
- **Group separators in the more-layer are cosmetic markup.** They are not
  counted as keys and did not break width math or the `+N` overflow note.
- **Palette action dispatch for parameterized actions** (`view('kanban')`,
  `phase_move(-1)`) is delegated to `App.run_action` so parsing matches normal
  bindings exactly.

## Conventions honored

≤4 source files/increment · tests uncapped · README key table documents
every bound key (`test_keymap.py` enforces) · no commits/push without operator
decision at the merge gate · artifacts in English, conversation in Spanish ·
RED counterfactual mandatory per AT · every acceptance falsifiable (C-40) ·
`shall` reserved for HLR/LLR statements · every key declared only in `KEYMAP`.

## Out-of-scope carries

- Retiring or redesigning the existing `LegendModal` beyond making it reachable
  from the palette or the layered bar.
- Adding new board actions or changing existing action behaviour.
- Darkside / ledger / prism follow-ups.
- Any change outside `taskboard/keymap.py`, `taskboard/app.py`,
  `taskboard/modals.py`, `README.md`, the test suite, and deliberation artifacts.

## Decision log

| date | decision | by |
|---|---|---|
| 2026-08-16 | Batch opened under /dev-flow, lane `core` (D fired, contract surface) | orchestrator, pending operator gate |
| 2026-08-16 | Proposal **E + F** approved for implementation; `?` repurposed for palette, `;` added for layer toggle | operator |
| 2026-08-16 | `LegendModal` retained and made reachable from the palette / layered bar rather than keeping a dedicated key | orchestrator default, approved at gate |
| 2026-08-16 | Batch artifacts live in `.dev-flow/2026-08-16-batch-05/`; root `01-requirements.md` overwritten for current batch per repo convention | orchestrator |
| 2026-08-16 | `_on_palette_run` implemented as `async def` calling `await self.run_action(action)` to match Textual's binding dispatch | orchestrator (discovered during Inc 2) |
| 2026-08-16 | `date` group hue changed from `amber` to `orange` to avoid collision with `system` in the more layer | orchestrator (discovered during Inc 1) |
| 2026-08-16 | Validation passed; merge to `main` and push approved | operator |

## Test ledger

| node | suite | last run | result |
|---|---|---|---|
| tests/ | pytest | 2026-08-16 | **836 passed in 82.63s** (0 failures, 0 skips) |
| tests/test_keymap.py | pytest | 2026-08-16 | pass (layer oracles updated) |
| tests/test_legend.py | pytest | 2026-08-16 | pass (3 new palette tests) |
