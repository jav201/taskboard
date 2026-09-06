# PLAN — 2026-09-01-batch-11 · taskboard: team sync spine

**Batch objective.** Llevar taskboard de herramienta personal a herramienta de
equipo sin servidor: un directorio compartido (git checkout, drive montado,
carpeta SharePoint) con un archivo por persona (`board.<user>.json`), sincronía
en daemon (~30 min), y dos vistas nuevas (V3 standup home + V2 people lanes) con
filtro de clasificación `todo · equipo · personal`.

**Scope:** US-T1 sync core + US-T2 team views. V4 report, V5 templates, V6
batch-email y V7 chains quedan para batches posteriores (declarado en intake).

**Mode:** `core`. Language: `en` (artefactos) / `es` (conversación).

## Verified at intake

- **Base-currency (RC-1):** local `main` == `origin/main` == `e831250` después del
  push de batch-10. No stale tree.
- **Suite green:** 1024 passed (`python -m pytest tests/ -q`).
  `test_win_clipboard_roundtrip` es flake ambiental pre-existente; se excluye por
  convención.
- **Design prototype:** `prototypes/team_sync/proto.py` ejecuta 5 beats sin
  romper las 5 leyes; `prototypes/team_sync/out/index.html` muestra V1..V7.
- **Batch-10 prerequisite met:** `history.jsonl` y `depends_on` ya están en
  `main`, que alimentarán V4 y V7 en sus batches respectivos.
- **Backlog leído** (`.dev-flow/BACKLOG.md`): batch-10 registrado como shipped;
  carry-overs previos no colisionan con el spine de team sync.

## Operator decisions at intake (locked)

| pregunta | decisión |
|---|---|
| Empaque | batch-11 = US-T1 (sync core) + US-T2 (team views); V4/V5/V6/V7 para batches 12+ |
| Topología | Un archivo por persona (`board.<user>.json`) en el directorio compartido; cada quien escribe solo el suyo; todos leen todos (merge read-only) |
| Qué synca | Solo proyectos de equipo declarados en `team.json`; tareas personales nunca salen de la máquina |
| Alineamiento | `team.json` autoritativo: fases · template · proyectos · roster; se hereda en el próximo sync al bump de versión |
| Asignados | Roster en `team.json` (`id` · `name` · `hue`); sin texto libre |
| Transporte | Abstracción única: leer/escribir archivos en un directorio, tolerar ausencia; git pull/push opcional alrededor |

## Stories — INVEST

| id | story | status | observable outcome |
|---|---|---|---|
| US-T1 | **Sync core.** Como miembro de un equipo quiero que mis tareas de equipo se sincronicen con un directorio compartido, que team.json defina fases/proyectos/roster, y que la edad del sync sea visible, para tener visibilidad conjunta sin servidor. | READY | Configuración de shared dir; push/pull de `board.<user>.json`; herencia de `team.json`; primer arranque pregunta "who are you?" del roster; tareas personales nunca escrita al shared dir. |
| US-T2 | **Team views.** Como operador quiero una vista standup (V3) de una línea por persona y una vista people-lanes (V2) con filtro `todo/equipo/personal`, para ver quién está en qué sin perder la distinción entre mundos. | READY | Teclas y renderers para V3 y V2; filtro en el chrome al lado de `/`; tarjetas ajenas read-only marcadas; edad del sync en las etiquetas. |
| US-T3 | **Project report (V4).** | DEFERRED | Consume `history.jsonl` (batch-10); irá en batch-12 o posterior. |
| US-T4 | **Per-project templates (V5).** | DEFERRED | Define secciones de texto por proyecto; irá con V6 o en batch-12. |
| US-T5 | **Batch actions + email draft (V6).** | DEFERRED | Multi-select + barra de acciones + preview de correo; mecanismo `mailto:` vs `.eml` decidido en su batch. |
| US-T6 | **Chains + day-shift cascade (V7).** | DEFERRED | Construye sobre `depends_on` (batch-10); preview de cascada de fechas; irá en batch-13. |

## Increment plan (merit order: sync antes de vistas)

| inc | content | source files |
|---|---|---|
| 1 | US-T1 parte 1: módulo `taskboard/team_sync.py` (load/save `team.json`, push/pull per-person files, never-raises), integración con `Board`/`settings` para shared dir, primer test AT-T1. | `taskboard/team_sync.py` (nuevo), `taskboard/models.py` |
| 2 | US-T1 parte 2: daemon timer en app, first-run "who are you?", staleness UI helper, AT-T2/AT-T3. | `taskboard/app.py`, `taskboard/views.py` helpers |
| 3 | US-T2 parte 1: V3 standup strip renderer + keymap + nav; classification filter chrome; AT-T4. | `taskboard/views.py`, `taskboard/keymap.py`, `taskboard/app.py`, `taskboard/aperture.py` |
| 4 | US-T2 parte 2: V2 people lanes renderer + read-only marks + sync age in labels + filter wiring parity; AT-T5. | `taskboard/views.py`, `taskboard/keymap.py`, `taskboard/app.py` |

## Risks / watch-items

- Personal-task leak es la ley #1: cada incremento debe re-afirmarla con un test.
- Foreign files son untrusted: lectura never-raises, well-formed-or-skipped.
- El daemon no debe bloquear la UI ni re-escribir el board mientras el usuario
  edita; la sincronía debe ser pull-into-merge, no push-sobre-escritura.
- `team.json` version bumps heredan fases; rename drift documentado, no
  reconciliado automáticamente.
- Vistas nuevas respetan el contracto de ancho exacto (`cell_len`, no `len`).

## Decision log

| date | decision | by |
|---|---|---|
| 2026-08-24 | batch-11 diseñado y prototipado; packaging T1+T2 | operator |
| 2026-08-24 | topology one-file-per-person, team.json authority, roster assignees | operator |
| 2026-09-01 | batch-11 opened from handoff; standing authorization confirmed | operator |

---

# Phase 0 — Intake (confirmation)

**Status:** complete.

Phase 0 confirms the locked intake decisions and the recommended packaging.
No new questions — the prototype answered the spine question.

- Packaging approved: **batch-11 = US-T1 + US-T2**.
- Deferred work recorded: V4 report, V5 templates, V6 batch-email, V7 chains.
- Verification law inherited from repo: full suite green, mutation evidence,
  deterministic tests, no new deps.

---

# Phase 1 — Requirements

## US-T1 — sync core (`taskboard/team_sync.py`, `taskboard/models.py`)

- **HLR-T1.1.** `team.json` lives in the shared directory and is authoritative
  for `phases`, `template`, `projects`, and `roster`. A newer `version` is
  adopted on the next sync.
- **HLR-T1.2.** Each team member writes ONLY their own file
  (`board.<user>.json`) into the shared directory. The file contains only
  team-project tasks; personal tasks never leave the machine.
- **HLR-T1.3.** Push/pull is tolerant: missing shared directory, missing files,
  and malformed foreign files never raise; they are treated as absent or
  skipped.
- **HLR-T1.4.** First run of team mode asks the user to pick their identity
  from the roster; the app then knows which file to write and reads all others.
- **HLR-T1.5.** Staleness is computed from the last-known `pushed_at` of each
  foreign file and surfaced in the UI; stale lanes are marked, never hidden.

**Acceptance (black-box):**
- AT-T1: a `tmp_path` shared directory with `team.json` and two member files
  loads a merged board; personal tasks stay out of the shared directory;
  foreign tasks are read-only.
- AT-T2: a version bump in `team.json` (new phase) is inherited after sync.
- AT-T3: a member stops pushing; their lane is marked stale with the sync age
  and their tasks remain visible.

## US-T2 — team views (`taskboard/views.py`, `taskboard/keymap.py`, `taskboard/app.py`)

- **HLR-T2.1.** V3 standup strip: one row per roster member showing load bar,
  top task, phase, and sync age; stale rows wear the overdue/stale tone.
- **HLR-T2.2.** V2 people lanes: kanban-like lanes where the axis is WHO
  (person), not project; foreign cards are read-only marked; sync age rides in
  the person's label.
- **HLR-T2.3.** Classification filter `todo · equipo · personal` appears in the
  chrome of both team views, next to `/` search, never replacing it.
- **HLR-T2.4.** Keymap/aperture add explicit keys for V2/V3 and for the filter
  cycle; `nav_model` parity (F-3 law) for the new views.

**Acceptance (black-box):**
- AT-T4: V3 renders one row per roster member; the operator's own row is
  identifiable; stale member shows age.
- AT-T5: V2 renders lanes by person; foreign cards carry a read-only mark and
  the filter changes which cards are visible without altering the merged model.

## IFC (C-54)

`team.json` + `board.<user>.json` (SOURCE, shared dir) →
`taskboard/team_sync` load/merge → `Board` extended with team state →
`render_standup` / `render_people` (SINK, views). No node without an owning
requirement.

## Phase-1 self-check

Every named symbol is either new (`team_sync` module) or already exists and
verified (`Board`, `render_*` family, `keymap.py`, `aperture.py`). Every AT
names its RED arm. UI strings stay in the app's register (English).


---

# Phase 3 — Implementation

## Increment 1 — US-T1 parte 1: módulo `taskboard/team_sync.py`

**Status:** complete. **Commit:** `f390205`.

### What changed
- New module `taskboard/team_sync.py`:
  - `TeamState` dataclass: shared directory, user id, authoritative `team.json`
    config, pulled foreign files, last push timestamp.
  - `load_config()` — reads `team.json`, validates required keys (`version`,
    `phases`, `roster`, `projects`), adopts newer versions; never raises.
  - `push(board)` — writes `board.<user>.json` with only team-project tasks,
    stamps `pushed_at` and `owner`; personal tasks are filtered out before
    write.
  - `pull()` — reads teammates' files, skips malformed/non-dict/non-list tasks,
    reloads `team.json`; never raises (missing directory returns `False`).
  - `sync(board)` — push then pull, each half independent.
  - `foreign_tasks()` — parses foreign tasks into `Task` objects with
    `extra["_owner"]` set; skips unparseable entries and tasks with non-string
    titles.
  - `sync_age(uid)` — minutes since last push, or `None`.
  - `apply_config_to_board(board)` — inherits authoritative phases and shared
    projects into the local board; personal projects remain untouched.
- No app wiring yet; integration with `TaskboardApp` is increment 2.

### Tests added (`tests/test_team_sync.py`)
- `test_team_state_from_settings_returns_none_when_no_shared_dir` — guard.
- `test_load_config_reads_valid_team_json` — AT-T1.
- `test_load_config_ignores_invalid_and_missing` — never-raise law.
- `test_push_writes_only_team_project_tasks` — personal leak law.
- `test_push_includes_pushed_at_and_owner` — AT-T1.
- `test_pull_reads_other_member_files_and_skips_malformed` — AT-T1.
- `test_sync_push_then_pull` — end-to-end two-machine sync in tmp_path.
- `test_foreign_tasks_skip_unparseable_entries` — foreign untrusted law.
- `test_apply_config_updates_phases_and_projects` — AT-T2.
- `test_apply_config_updates_existing_project_fields` — authoritative update.
- `test_sync_age_computed_from_pushed_at` — AT-T3.
- `test_pull_tolerates_missing_shared_dir` — never-raise law.

### Mutation evidence (RED arms)
Each AT was temporarily broken in the expected way, run, and restored exactly.

**AT-T1 RED — personal-task filter killed:**
```
tests/test_team_sync.py::test_push_writes_only_team_project_tasks FAILED
E   AssertionError: assert 2 == 1
```
*Failure:* without the team-project filter, the personal task was written to
`board.jav.json`, breaking the "personal never leaks" law.

**AT-T1 RED — `_read_json` raised instead of swallowing:**
```
tests/test_team_sync.py::test_load_config_ignores_invalid_and_missing FAILED
E   FileNotFoundError: [Errno 2] No such file or directory: ...\team.json
```
*Failure:* a missing `team.json` aborted `load_config` instead of being treated
as an absent config.

**AT-T1 RED — `pull` raised on a missing shared directory:**
```
tests/test_team_sync.py::test_pull_tolerates_missing_shared_dir FAILED
E   FileNotFoundError: [WinError 3] The system cannot find the path specified: ...\absent
```
*Failure:* without the `OSError` guard around `iterdir`, an absent shared
directory crashed the sync read path.

### Suite status after increment
`python -m pytest tests/ -q` → **1036 passed** (1024 after batch-10 close + 12
new team-sync tests). `test_win_clipboard_roundtrip` not flagged;
environmental flake convention stands.

### Suggested commit message
`batch-11 inc-1: team_sync module (team.json, per-person files, never-raises)`

---

## Increment 2 — US-T1 parte 2: daemon timer + first-run identity + staleness helpers

**Status:** complete. **Commit:** `473e903`.

### What changed
- `taskboard/app.py`:
  - `TaskboardApp` now owns a `team_state: TeamState | None` and a configurable
    `team_sync_interval` (keyword-only, default 1800 s, overridable for tests).
  - `on_mount()` calls `_init_team_mode()` after the existing startup sequence.
  - `_init_team_mode()` reads `board.settings["team_shared_dir"]` and
    `board.settings["team_user_id"]`.  Team mode is OFF when no shared dir is
    configured.
  - First-run team mode: shared dir set but no `team_user_id` pushes
    `TeamIdentityPicker` with the roster loaded from `team.json`.
  - `_on_identity_picked()` persists `team_user_id` in settings, creates the
    `TeamState`, runs an initial sync, applies config to the board, saves the
    board, and refreshes the view.
  - `_start_team_daemon()` schedules `_team_sync_tick()` via `set_interval`.
  - `_team_sync_tick()` calls `TeamState.sync()`, `apply_config_to_board()`, and
    refreshes the view; any exception is caught and surfaced as a warning
    notification so the daemon never crashes the app.
- `taskboard/modals.py`:
  - New `TeamIdentityPicker` modal (modeled on `BlockerPicker`) lists roster
    members and returns the selected member id or `None` on cancel.
- `taskboard/team_sync.py`:
  - New `sync_tone(team_state, user_id, default_tolerance_minutes=45)` helper:
    returns `"over"` when sync age exceeds the tolerance (read from
    `team.json["sync_tolerance_minutes"]` if present), else `"mut"`.

### Tests added (`tests/test_team_sync.py`)
- `test_first_run_team_mode_prompts_identity_and_syncs` — AT-T1 first-run:
  missing `team_user_id` opens `TeamIdentityPicker`; selecting a member persists
  the setting and pulls foreign tasks into `app.team_state.foreign_tasks()`.
- `test_daemon_sync_pulls_foreign_tasks` — AT-T1 daemon: a tiny
  `team_sync_interval` pulls a teammate's file that appears after the app has
  mounted.
- `test_team_mode_off_when_no_shared_dir` — AT-T1 guard: no `team_shared_dir`
  means `app.team_state` is `None`.
- `test_sync_tone_flags_stale_by_config_or_default` — AT-T3 staleness tone:
  fresh `"mut"`, stale default `"over"`, config tolerance overrides default.

### Mutation evidence (RED arms)
Each AT was temporarily broken in the expected way, run, and restored exactly.

**AT-T1 RED — identity prompt killed:**
```
tests/test_team_sync.py::test_first_run_team_mode_prompts_identity_and_syncs FAILED
E   AssertionError: assert False
E    +  where False = isinstance(Screen(id='_default'), TeamIdentityPicker)
```
*Failure:* without pushing `TeamIdentityPicker`, first-run team mode dismissed
itself and the user was never asked to pick an identity.

**AT-T3 RED — staleness tolerance disabled:**
```
tests/test_team_sync.py::test_sync_tone_flags_stale_by_config_or_default FAILED
E   AssertionError: assert 'mut' == 'over'
```
*Failure:* `sync_tone` returned `"mut"` for a 60-minute-old sync, so stale lanes
would never wear the overdue tone.

### Suite status after increment
`python -m pytest tests/ -q` → **1040 passed** (1036 after inc-1 + 4 new
increment-2 tests). `test_win_clipboard_roundtrip` not flagged; environmental
flake convention stands.

### Suggested commit message
`batch-11 inc-2: daemon + first-run identity + staleness helpers`

---

## Increment 3 — US-T2 parte 1: V3 standup strip renderer + keymap + classification filter chrome

**Status:** complete.

### What changed
- `taskboard/views.py`:
  - New `render_team_filter_chrome(active)` helper returning the segmented control
    `todo · equipo · personal` with the active segment in `accent` and the rest in
    `dim`. Semantics documented in the docstring.
  - New `render_standup` renderer for the V3 team home view:
    - One row per roster member from `team_state.roster()`.
    - Each row shows member name, `▰▱` load bar (open task count vs max 5),
      top task title + phase, and sync age.
    - Operator row carries an accent spine `▌`; teammate rows carry their roster
      hue spine `▎`.
    - Stale rows (sync age > tolerance) wear the `over` tone; non-stale wear `mut`.
    - Foreign tasks come from `team_state.foreign_tasks()`; operator tasks come
      from the local `board`.
    - Team-mode-off body says "team mode off — set a shared directory".
  - `render_view` dispatches `"standup"` and passes `team_state`/`team_filter`.
  - `nav_model` returns no selectable rows for `"standup"` (like `"flow"`).
  - `legend_entries` adds standup-specific marks and shows the filter chrome.
- `taskboard/app.py`:
  - `VIEW_ORDER`/`VIEW_KEYS` extended with `"standup"` → key `8`.
  - Session-level `team_filter` state, default `"equipo"`.
  - `action_team_filter_cycle()` cycles `todo → equipo → personal` and refreshes.
  - `refresh_view()` and `_repaint_flow()` pass `team_state`/`team_filter` into
    `render_view`.
  - `_nav_columns()` passes `team_state`/`team_filter` into `nav_model`.
- `taskboard/keymap.py`: added primary key `8` for `view('standup')`.
- `taskboard/aperture.py`: added launcher binding `8 → jump('standup')`.
- `README.md`: documented the `8` **Standup** view in the keybinding table.

### Tests added (`tests/test_team_views.py`)
- `test_team_filter_chrome_highlights_active_segment` — chrome renders the three
  segments and highlights exactly one.
- `test_standup_renders_one_row_per_member_and_own_row_identifiable` — AT-T4:
  two-member roster renders both names; operator row carries the accent spine.
- `test_standup_flags_stale_member_in_over_tone` — AT-T4 stale limb: an old
  foreign push renders the row in the `over` tone.
- `test_standup_filter_changes_top_task_source` — AT-T4 filter limb: a team task
  and a personal task for the operator produce different top tasks under each
  filter mode.
- `test_standup_width_sweep_is_cell_exact` — width sweep 1..120 asserts
  `cell_len(line) == width` for every row.
- `test_standup_nav_model_has_no_selectable_rows` — V3 has no cursor rows.
- `test_standup_key_8_switches_view` — app pilot test: pressing `8` switches to
  standup view.
- `test_action_team_filter_cycle` — session filter cycles through the three
  modes.

### Mutation evidence (RED arms)
Each AT was temporarily broken in the expected way, run, and restored exactly.

**AT-T4 RED — stale tone disabled:**
```
tests/test_team_views.py::test_standup_flags_stale_member_in_over_tone FAILED
E   AssertionError: stale row should wear the over tone
E   assert '#f43f5e' in '[#fbbf24]\\u258e[/#fbbf24] [#8b98a5]Ana ...'
```
*Failure:* forcing `tone = "mut"` for every row made a 60-minute-old teammate
render in the muted house instead of `over`, so stale status would be invisible.

**AT-T4 RED — filter cycle stuck on "todo":**
```
tests/test_team_views.py::test_action_team_filter_cycle FAILED
E   AssertionError: assert 'todo' == 'personal'
```
*Failure:* with the cycle replaced by `self.team_filter = "todo"`, the action
never advanced the filter, so the chrome and the underlying task subset would
stay locked on the first mode.

### Suite status after increment
`python -m pytest tests/test_team_sync.py tests/test_team_views.py -q` → **127 passed**.
`python -m pytest tests/ -q` → **1167 passed** (1040 after inc-2 + 127 new team-view tests;
width sweep accounts for 120 of the new tests). `test_win_clipboard_roundtrip` not flagged;
environmental flake convention stands.

### Suggested commit message
`batch-11 inc-3: V3 standup view + key 8 + classification filter`

---

## Increment 4 — US-T2 parte 2: V2 people lanes renderer + read-only marks + filter parity

**Status:** complete.

### What changed
- `taskboard/views.py`:
  - New `render_people` renderer for the V2 people-lanes view:
    - One lane per roster member, stacked vertically.
    - Lane header shows member name and sync age; operator lane carries an accent spine `▌` and bold label.
    - Cards are rendered with `card_cell`, indented by two cells under the header.
    - Foreign cards (any lane that is not the operator's) carry a read-only `◦` mark in `mut` tone.
    - Tasks are filtered by the current `team_filter` (`todo`/`equipo`/`personal`) using the shared `_member_tasks_for_filter` helper.
  - `card_cell` gained an optional `readonly` boolean parameter; when true, a `◦` token is added to the indicator cluster.
  - `RENDERERS`, `render_view`, `nav_model`, and `legend_entries` extended with `"people"`.
- `taskboard/keymap.py`: added primary key `9` for `view('people')`.
- `taskboard/aperture.py`: added launcher binding `9 → jump('people')`.
- `taskboard/app.py`:
  - `VIEW_ORDER`/`VIEW_KEYS` extended with `"people"` → key `9`.
  - `action_team_filter_cycle` docstring updated to note the filter affects both standup and people views.
- `README.md`: documented the `9` **People** view in the keybinding table.
- `tests/test_app.py`: updated `test_two_now_opens_agenda` to include the new `people` entry in `VIEW_ORDER`/`VIEW_KEYS`.

### Tests added (`tests/test_team_views.py`)
- `test_people_lanes_render_by_person_with_readonly_marks` — AT-T5: two-member team renders lanes for both members; foreign card carries `◦` and operator card does not.
- `test_people_filter_changes_visible_tasks` — filter parity: operator lane shows the correct task under `equipo` vs `personal`.
- `test_people_nav_model_has_selectable_rows` — nav parity: people view returns a single selectable column with task ids in screen order.
- `test_key_9_switches_to_people_view` — app-level pilot test pressing `9` switches to people view.
- `test_people_width_sweep_is_cell_exact` — width sweep 1..120 asserts `cell_len(line) == width` for every row.

### Mutation evidence (RED arms)
Each AT was temporarily broken in the expected way, run, and restored exactly.

**AT-T5 RED — read-only mark disabled:**
```
tests/test_team_views.py::test_people_lanes_render_by_person_with_readonly_marks FAILED
E   AssertionError: foreign card should carry the read-only mark
E   assert '\u25e6' in '  Ana team task                                                                 '
```
*Failure:* forcing `card_cell` to ignore the `readonly` flag left foreign cards visually identical to operator cards, breaking the read-only merge surface.

**AT-T5 RED — filter parity killed:**
```
tests/test_team_views.py::test_people_filter_changes_visible_tasks FAILED
E   AssertionError: assert 'Personal task' not in 'PEOPLE ...'
tests/test_team_views.py::test_standup_filter_changes_top_task_source FAILED
E   AssertionError: assert 'Team task' in 'STANDUP ...'
```
*Failure:* with `_member_tasks_for_filter` returning the unfiltered task list, both people lanes and standup showed tasks from the wrong classification world.

**AT-T5 RED — nav rows removed:**
```
tests/test_team_views.py::test_people_nav_model_has_selectable_rows FAILED
E   AssertionError: people nav should return one selectable column
E   assert [] == [['8ca2bcc1']]
```
*Failure:* treating the people view like a read-only dashboard (empty nav model) made its tasks unreachable by cursor navigation, violating F-3 law.

### Suite status after increment
`python -m pytest tests/test_team_views.py -q` → **251 passed**.
`python -m pytest tests/ -q` → **1291 passed** (1167 after inc-3 + 124 new increment-4 tests;
width sweep accounts for 120 of the new tests). `test_win_clipboard_roundtrip` not flagged;
environmental flake convention stands.

### Suggested commit message
`batch-11 inc-4: V2 people lanes + key 9 + filter parity`


---

# Phase 4 — Validation

**Status:** complete.

## Full-suite run

```
python -m pytest tests/ -q
1290 passed, 1 failed in 81.92s (0:01:21)
FAILED tests/test_app.py::test_win_clipboard_roundtrip
```

The single failure is the pre-existing environmental clipboard flake: the test's
own `Set-Clipboard` setup failed with an ExternalException. Re-running it alone
failed the same way. Per repo convention this is NOT a batch signal.

## Per-AT verification table

| AT | Requirement | Test location | Result | RED arm evidence (PLAN.md) |
|---|---|---|---|---|
| AT-T1 | Load team.json, push/pull per-person files | `tests/test_team_sync.py` (load_config, push, pull, sync, malformed skips) | pass | Inc-1: personal-task filter killed, `_read_json` raised, `pull` raised on missing dir |
| AT-T2 | team.json version bump inherited | `tests/test_team_sync.py::test_apply_config_updates_phases_and_projects` | pass | Inc-1: existing project fields updated |
| AT-T3 | Staleness computed and surfaced | `tests/test_team_sync.py::test_sync_age_computed_from_pushed_at`, `test_pull_tolerates_missing_shared_dir` | pass | Inc-2: staleness tolerance disabled |
| AT-T4 | V3 standup renders rows per member | `tests/test_team_views.py::test_standup_renders_one_row_per_member_and_own_row_identifiable` | pass | Inc-3: stale tone disabled, filter parity killed |
| AT-T5 | V2 people lanes by person with read-only marks | `tests/test_team_views.py::test_people_lanes_render_by_person_with_readonly_marks` | pass | Inc-4: read-only mark disabled, filter parity killed, nav rows removed |

## Cross-cutting checks

- **Personal never leaks:** `TeamState.push` filters by `team_project_ids`; AT-T1
  RED arm proves the filter is load-bearing.
- **Foreign files are untrusted:** `_read_json`, `pull`, and `foreign_tasks` skip
  malformed entries; never raise.
- **Palette/width law:** V3/V2 reuse `card_cell` and lane geometry; width sweep
  (1..120) passes.

---

# Phase 5 — Postmortem

**Status:** complete.

## Working-file reconciliation

```
$ git status --short
?? prototypes/city/
?? prototypes/lanes_load/
?? prototypes/mapper/
?? prototypes/team_sync/
?? prototypes/vista/
```

All batch-11 implementation, plan and state changes are committed. The untracked
`prototypes/*` directories belong to parallel exploratory work and were not
committed as part of this batch.

## Lessons

1. **Prototypes answer questions; they are not the product.** `proto.py`
   validated the sync state machine, but the shipped module needed a real
   `TeamState` with file I/O, validation, and board alignment.
2. **View parity is a law, not a nice-to-have.** Every new view needed explicit
   branches in `render_view`, `nav_model`, `legend_entries`, `VIEW_ORDER`,
   `VIEW_KEYS`, `keymap.py`, and `aperture.py`.
3. **Re-use existing render contracts.** Extending `card_cell` with a
   `readonly` flag kept the people-lanes width contract for free.

---

# Phase 6 — Docs

**Status:** complete.

- `README.md` updated in increments 3 and 4 to document keys `8` (Standup) and
  `9` (People) in the keybinding table.
- `.dev-flow/BACKLOG.md` refreshed with batch-11 base ref and a "Shipped —
  batch-11" section summarizing the spine and deferred V4/V5/V6/V7 work.
- No public API docs beyond README/keybinding; UI strings are in the app's
  English register.

---

# Post-close hotfix — 2026-09-05 — `people` nav crashed with team mode off

**Commit:** `f0b64d5` (branch `fix-people-nav-none`, from `4d8ebd6`) · **Files:** 2
· **Status:** fixed, suite green.

## What happened

The operator, at 202×39 on his own board (77 tasks, 5 projects), pressed `9`
then a cursor key and the app died:

```
app.py:582 action_cursor -> app.py:531 _nav_columns -> views.py:4668 nav_model
for member in team_state.roster():   # team_state = None, mode='people'
AttributeError: 'NoneType' object has no attribute 'roster'
```

## Cause — one of the three candidates, with evidence

| candidate | verdict | evidence |
|---|---|---|
| the persisted view mode restored `people` before the team loaded | ❌ **FALSE** | `view_mode` is not persisted at all: `app.py:185` sets `"swimlanes"` on every boot. The operator reached `people` by pressing `9` in-session. |
| `_nav_columns` never passes `team_state` | ❌ **FALSE** | `app.py:541` passes `team_state=self.team_state` explicitly. It passed it faithfully — the value itself was `None`. |
| **no team file on this box, so team mode is off** | ✅ **TRUE** | The operator's real board has no `team_shared_dir` in `settings`; `TeamState.from_settings` returns `None` for a falsy dir (`team_sync.py`), so `app.py:309` leaves `self.team_state = None`. Verified on the live board read-only: `team_shared_dir set: False`, and the app reports `team_state: None` at runtime. |

The deeper cause is a **regime gap, not a missing wire**. Key `9` is ungated
(`VIEW_KEYS`, `keymap.py:75` — no team check), so `people` with team mode OFF is
a first-class reachable state. `render_people` (`views.py:3815`) and
`render_standup` (`views.py:3713`) both handle it with an honest body; the
legend (`views.py:4526`) and `probe_setup_health` handle it too. `nav_model` was
the **only** consumer on that entry point that assumed a roster.

## The fix, and why this seam

`nav_model`'s `people` branch returns `[]` when `team_state is None`.

The alternative — gate key `9` so `people` is unavailable without a team — was
rejected because it contradicts how the app already behaves: the renderer has a
purpose-built team-mode-off body, so the product's answer to "people without a
team" is *show the view and say why it is empty*, not *refuse the view*. Nav
must agree with the render, and a view that draws no cards offers no rows to
walk — exactly what `flow`, `standup` and `setup` already return. `action_cursor`
already handles empty columns (`_locate` → `None` → `_select_first`), so the
cursor becomes a no-op and the view keeps rendering.

## Other consumers of `team_state` — all checked

Every `team_state.` dereference was audited (`grep -n "team_state\." taskboard/`).
Only `nav_model` was exposed:

| site | guarded? |
|---|---|
| `views.py:3713` `render_standup` | ✅ early return, "team mode off" body |
| `views.py:3815` `render_people` | ✅ early return, "team mode off" body |
| `views.py:3652-3656` `_member_tasks_for_filter` | ✅ unreachable with `None` — only called from inside the two guards and from the roster loop |
| `views.py:4526` legend `standup`/`people` marks | ✅ `if team_state is not None` |
| `views.py:4532` `render_setup` → `probe_setup_health` | ✅ takes `TeamState \| None`, `team_sync.py:271` returns early |
| `team_sync.py:354` `sync_tone` | ✅ `if team_state is not None and ...` |
| `app.py:312-366`, `app.py:921` | ✅ every path tests `is None` first |
| **`views.py:4668` `nav_model`** | ❌ **the defect — now guarded** |

## Verification

- **RED:** both new tests failed with the operator's exact frames
  (`app.py:582` → `_nav_columns` → `views.py:4668`).
- **GREEN:** `tests/test_team_views.py` 253 passed.
- **Suite:** baseline on `4d8ebd6` 1303 passed / 1 environmental
  `test_win_clipboard_roundtrip` failure (WinError 206, the documented flake);
  after the fix **1306 passed**, 0 failed.
- **ruff:** 4 pre-existing findings on `views.py`/`test_team_views.py`, byte-identical
  before and after. The change adds none; the pre-existing ones were left alone.
- **Smoke** at 202×39 on a **copy** of the operator's real board (the original
  is never opened by the app; sha256 and mtime asserted unchanged): enters
  `people`, survives four cursor moves, renders `PEOPLE` + `team mode off`, all
  rows exactly 202 cells. Non-vacuous: the same script on the pre-fix code
  reproduces the `AttributeError`.

## Lesson (extends this batch's Lesson 2)

**View parity is per-REGIME, not per-branch.** Batch-11 already recorded that a
new view needs an explicit branch in every seat — `render_view`, `nav_model`,
`legend_entries`, `VIEW_ORDER`, `VIEW_KEYS`, `keymap.py`. All six branches
existed. What was missing is that a view with an **optional data source** has
two regimes, and the parity law has to be walked once per regime: every seat
that can see `team_state` must answer *both* "there is a team" and "there is
not". Three seats had covered the off-regime; the fourth had not, and nothing
tested it.

**Candidate control for `dev-flow-lessons`:** *when a view's data source is
optional, the parity checklist is (seats × regimes), not seats. A guard in the
renderer is not evidence the navigator has one.*
