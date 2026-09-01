# PLAN — 2026-09-01-batch-12 · taskboard: in-app Setup + per-view help

**Batch objective.** Implementar la configuración de equipo dentro de la aplicación (Setup, tecla `0`) con health checks, la familia de ayuda por vista (`?` muestra la ayuda de la vista activa), y ajustar la barra para que solo muestre las teclas de la vista actual.

**Scope:** US-S1 (initial sync on mount) + US-S2 (Setup in-app) + US-S3 (per-view help) + US-S4 (keybar per-view law). V4/V5/V6/V7 siguen diferidos.

**Mode:** `core`. Language: `en` (artefactos técnicos) / `es` (conversación y PLAN).

## Verified at intake

- **Base-currency (RC-1):** local `main` == `origin/main` == `ff4bb7e` después del push de cleanup-aperture. El handoff de batch-12 ya está commiteado como `9dda458`.
- **Suite green:** 1284 passed (`python -m pytest tests/ -q`). `test_win_clipboard_roundtrip` es flake ambiental pre-existente; se excluye por convención.
- **Design prototype:** `prototypes/team_sync/generate.py` contiene el copy autorizado para V8 setup y V9 help family.
- **Keybinding `0` verified free** tras la limpieza del aperture/widget.

## Operator decisions at intake (locked)

| pregunta | decisión |
|---|---|
| Setup como vista o modal | **Vista** (`view_mode == "setup"`, tecla `0`) para que el KeyBar propio sea visible. |
| Per-view help | `?` abre ayuda de la vista activa; `m` dentro de ella abre el mapa completo (`HelpScreen`); `?` dentro de la ayuda abre la paleta de comandos (`CommandPalette`). |
| Keybar law | Solo teclas de la vista actual + universales (`?`, `q`, `;`); comandos globales (`o`, `i`, `p`, `P`, `f`, `c`, `R`, `S`) viven en `?`/palette, no en la barra. |
| Health checks | Asesorias: nunca bloquean edición; se re-computan al abrir y tras `ctrl+s`. `⚠` usa fallback `!` si no está cubierto. |
| Staged editing | Setup muta estado *staged* en memoria; `ctrl+s` escribe `team.json` (version bump) + `board.settings`; `esc` descarta y vuelve a la vista previa. |

## Stories

| id | story | observable outcome |
|---|---|---|
| US-S1 | Initial sync on mount. | `_init_team_mode` llama `_run_team_sync()` antes de `_start_team_daemon()` cuando `team_user_id` ya está seteado. |
| US-S2 | Setup in-app. | Vista `setup` (tecla `0`) con grid editable; `ctrl+s` persiste; `esc` cancela; checks ✓/⚠. |
| US-S3 | Per-view help family. | `LegendModal` → `HelpModal`; copy de `generate.py` para 8 vistas + setup; `m` abre `HelpScreen`. |
| US-S4 | Keybar per-view law. | Nuevo flag `bar` en `Key`; comandos globales ocultos de la barra pero presentes en palette. |

## Increment plan

| inc | content | source files |
|---|---|---|
| 1 | US-S1: one-liner initial sync + pilot test. | `taskboard/app.py` |
| 2 | US-S2 parte 1: Setup como vista (`"setup"` en `VIEW_ORDER`/`VIEW_KEYS`, `render_setup`, keymap `0`, staging). | `taskboard/app.py`, `taskboard/views.py`, `taskboard/keymap.py` |
| 3 | US-S2 parte 2: health checks, staged edits, save/discard, mutaciones. | `taskboard/app.py`, `taskboard/views.py`, `taskboard/team_sync.py` |
| 4 | US-S3: per-view help (`HelpModal`), full-keymap second tier, copy de `generate.py`. | `taskboard/modals.py`, `taskboard/app.py`, `taskboard/views.py` |
| 5 | US-S4: keybar audit — `bar` flag, global commands palette-only, tests/README. | `taskboard/keymap.py`, `tests/test_keymap.py`, `README.md` |

## Decision log

| date | decision | by |
|---|---|---|
| 2026-09-01 | batch-12 opened from handoff; packaging S1+S2+S3+S4 | operator |
| 2026-09-01 | Setup implemented as a view to keep KeyBar contract | plan |
| 2026-09-01 | Global commands moved to palette-only via `bar=False` flag | plan |

---

# Phase 0 — Intake

**Status:** complete.

Packaging approved: **batch-12 = US-S1 + US-S2 + US-S3 + US-S4**. Deferred: V4/V5/V6/V7.

---

# Phase 1 — Requirements

## US-S1 — initial sync on mount

- **HLR-S1.1.** When `board.settings["team_user_id"]` is already set on mount, `_init_team_mode` runs one sync immediately before starting the daemon.

**AT:** mount `TaskboardApp` with configured identity + peer file → standup shows peer immediately.

## US-S2 — Setup in-app

- **HLR-S2.1.** Setup is a full-screen view bound to key `0`; entering it stages current team config in memory.
- **HLR-S2.2.** Layout: label col 24 · control col 30 · check col 4 · note col; sections `equipo`, `proyectos del equipo`, `roster`.
- **HLR-S2.3.** Editable fields: modo equipo, carpeta compartida, sync cada (stepper 5..120 min), mi identidad, project rows (shared/hue/template), roster rows (id/name/hue; `a` add, `x` remove).
- **HLR-S2.4.** Advisory health checks per row; re-run on open and `ctrl+s`.
- **HLR-S2.5.** `ctrl+s` commits (team.json version bump + board.settings + sync + save); `esc` discards and returns to previous view.

**ATs:** save writes files; unwritable dir shows warning; esc leaves files unchanged; stepper clamps; `Enter` edits shared dir / interval / names; `Space` toggles modo equipo and project shared flag; `a`/`x` add/remove roster/project rows.

## US-S3 — per-view help family

- **HLR-S3.1.** `?` opens `HelpModal` for the active view.
- **HLR-S3.2.** Legend from `legend_entries`; keys from `fit_bar`; no hand-maintained lists.
- **HLR-S3.3.** Usage copy from `generate.py` for 9 modes.
- **HLR-S3.4.** `m` opens `HelpScreen`; `?` opens `CommandPalette`; `esc` closes.

**ATs:** `?` from each view names it; legend has no ghosts; help keys ⊆ `fit_bar`; `m` reaches full keymap.

## US-S4 — keybar per-view law

- **HLR-S4.1.** Footer bar shows only view-local + universal keys.
- **HLR-S4.2.** Global commands remain bound and reachable via `?`/palette, but not drawn in bar.
- **HLR-S4.3.** `Key` gets `bar: bool`; `bar_keys`/`fit_bar` respect it; `palette_commands` includes all live keys.

**ATs:** global commands absent from bar but in palette; README still documents every bound key.

---

# Phase 3 — Implementation

## Increment 1 — US-S1: initial sync on mount

**Status:** complete. **Commit:** `TBD`.

### Changes
- `taskboard/app.py` `_init_team_mode`: when `team_state.user_id` is set, call `self._run_team_sync()` before `self._start_team_daemon()`.

### Tests
- `tests/test_setup_help.py::test_configured_identity_syncs_on_mount`: pilot test; peer appears in standup immediately.

### Mutation evidence
RED arm verified by temporarily removing the new `_run_team_sync()` call: test failed because Ana's task did not appear until a daemon tick. Restored.

## Increment 2 — US-S2 parte 1: Setup como vista

**Status:** complete. **Commit:** `TBD`.

### Changes
- `taskboard/app.py`: add `"setup"` to `VIEW_ORDER`/`VIEW_KEYS`; `_stage_setup_state`; `_pre_setup_view`/`_setup_state`; `action_view` stages on entry; `action_setup_exit`; `action_focus_exit` dispatches to setup exit; existing `tab`/`enter`/`a`/`x` actions dispatch to setup stubs.
- `taskboard/keymap.py`: add `0` view key; setup-only `space`/`ctrl+s`; `escape` scoped to kanban/gantt/setup.
- `taskboard/views.py`: `render_setup` with sections/equipo/proyectos/roster; dispatch in `render_view`; `nav_model("setup") -> []`.
- `README.md`: document `0` Setup and setup controls.
- `tests/test_app.py`: update `VIEW_ORDER`/`VIEW_KEYS` assertions and escape scoping.

### Tests
- `tests/test_setup_help.py::test_setup_key_0_switches_view`
- `tests/test_setup_help.py::test_setup_renders_grid_with_sections`
- `tests/test_setup_help.py::test_setup_esc_returns_to_previous_view`

### Mutation evidence
RED arm verified by temporarily removing `"0"` from `VIEW_KEYS`: the view-switch test failed.

## Increment 3 — US-S2 parte 2: health checks y edición staged

**Status:** complete. **Commit:** `TBD`.

### Changes
- `taskboard/team_sync.py`: added `probe_setup_health` with advisory checks for folder exists/writable/lag, team.json parse, identity, sync age, roster.
- `taskboard/app.py`: `import json`; setup mutations (tab section, enter edit via TextPrompt, space toggle, a/x add/remove roster/project, ctrl+s save); `action_cursor` moves setup cursor; `action_setup_save` writes team.json with version bump + board.settings + re-initializes team state.
- `taskboard/views.py`: `render_setup` draws cursor highlight, health check ✓/! per row.

### Tests
- `tests/test_setup_help.py::test_setup_save_writes_team_json_and_settings`
- `tests/test_setup_help.py::test_setup_esc_leaves_files_unchanged`
- `tests/test_setup_help.py::test_probe_setup_health_flags_unwritable_shared_path`
- `tests/test_setup_help.py::test_setup_stepper_clamps_interval`
- `tests/test_setup_help.py::test_setup_enter_edits_shared_directory`
- `tests/test_setup_help.py::test_setup_enter_edits_sync_interval`
- `tests/test_setup_help.py::test_setup_space_toggles_team_mode_enabled`
- `tests/test_setup_help.py::test_setup_a_adds_project_row`
- `tests/test_setup_help.py::test_setup_x_removes_roster_row`

### Mutation evidence
RED arm verified by temporarily returning `(True, "ok")` for all checks: the unwritable-path test failed.

## Increment 4 — US-S3: per-view help family

**Status:** complete. **Commit:** `3a11eb0` (merged with inc-5).

### Changes
- `taskboard/modals.py`: refactor `LegendModal` → `HelpModal`.
- `taskboard/app.py`: `action_legend` pushes `HelpModal`; callbacks for `m` and `?`.
- `taskboard/views.py`: `help_usage` / `help_example` for 9 modes.

### Tests
- `tests/test_setup_help.py::test_question_mark_opens_per_view_help_modal`
- `tests/test_setup_help.py::test_help_modal_shows_usage_legend_example_and_keys`
- `tests/test_setup_help.py::test_help_modal_m_opens_full_keymap`
- `tests/test_setup_help.py::test_help_modal_question_mark_opens_command_palette`
- `tests/test_legend.py` updated for the new `?` → HelpModal → `?` palette flow.

## Increment 5 — US-S4: keybar per-view law

**Status:** complete. **Commit:** `3a11eb0` (merged with inc-4).

### Changes
- `taskboard/keymap.py`: `bar` flag; global commands `bar=False`; `palette_commands` includes all live keys.
- `tests/test_keymap.py`: update oracles; add global-not-in-bar and palette-includes-globals tests.
- `tests/test_prism_laws.py`: update `law_keybar` oracle to renamed bar test.
- `tests/test_report.py`: report key is palette-only.
- `README.md`: document the per-view footer and palette-only globals.

### Tests
- `tests/test_keymap.py::test_global_commands_are_palette_only_not_in_the_bar`
- `tests/test_keymap.py::test_the_palette_includes_palette_only_globals`

---

# Phase 4 — Validation

**Status:** complete.

- `python -m pytest tests/ -q` green: **1298 passed**.
- Clipboard flake not observed; none of the failures were environmental.
- Mutation evidence recorded per increment in this PLAN.

- Push only on explicit order.

# Phase 5 — Close

**Status:** complete.

- Working files reconciled; `prototypes/*` remains untracked exploratory work.
- `state.json` and `.dev-flow/BACKLOG.md` updated.
- **Post-close finding (fixed in `33eb4bf`):** the ATs for US-S2 did not exercise every editable row operation (`Enter`, `Space`, `a`, `x`) during the increment; the HLR-S2.3 list of editable fields was correct, but the derived test cases stopped at save/esc/health/stepper. This allowed a constructor mismatch (`TextPrompt(..., value=...)` vs `initial=...`) to ship. Corrective action: added 5 executable-setup command tests and updated the US-S2 ATs above.

# Phase 6 — Push

**Status:** complete.

- Pushed to `origin/main`: `ff4bb7e..33eb4bf` (includes the post-close `33eb4bf` hotfix for the Setup `TextPrompt` bug and missing ATs).
