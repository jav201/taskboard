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
