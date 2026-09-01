# HANDOFF — taskboard batch-12: Setup in-app + ayuda por vista (próximo agente)

**For:** the agent implementing the in-app Setup view and the per-view help
family. **Status:** team mode SHIPPED (batch-11: `team_sync.py`, daemon,
standup `8`, people `9`, classification filter). The designs below are
rendered and browser-verified prototypes; this document is the operational
spec. Resume with `/dev-flow` from this root (batch id suggestion:
`2026-09-01-batch-12`). Commits per increment authorized if the operator
confirms the standing authorization; **push only on explicit order.**

**Read first:**
- `prototypes/team_sync/out/team-setup-y-ayuda.html` — the report: REAL app
  captures + the designs, in full color.
- `prototypes/team_sync/NOTES.md` §V8 v2 / §V9 family — the design record.
- `prototypes/team_sync/generate.py` — reference renders of V8 and all 8
  help screens (the COPY of record for the help texts).

## Part 0 — the one-line fix that rides along (do it first)

**On mount with a configured identity, team mode runs NO initial sync** —
`app.py` `_enter_team_mode` (~:308): when `team_user_id` is already set it
goes straight to `_start_team_daemon()`, so team views show empty until the
first 30-min tick. The identity-picker path DOES sync on entry
(`_on_identity_picked`). Fix: call `_run_team_sync()` before
`_start_team_daemon()` in the configured branch too. Test: mount with
configured settings + a peer file present → the standup view shows the peer
WITHOUT waiting for a tick (pilot test; the repo's fixture style).

## Part A — V8 · Setup view (new screen, key `0` — verified free)

One screen, three sections, everything editable **inside the app** — the
operator's law: "el setup no se hace fuera de la aplicación". The app writes
`team.json` and `board.settings`; nobody edits files by hand.

**Layout (strict grid — the v1 free-form rows read as disorder):**
label col 24 · control col 30 · **check col 4** · note col. Sections:
`equipo` · `proyectos del equipo` · `roster`.

**Fields:**
- `modo equipo` — switch on/off. Off = the daemon stops, team views hide,
  personal board untouched.
- `carpeta compartida` — text field (`▌` cursor). Accepts a local path or
  anything that IS a directory (git checkout / drive / SharePoint-synced —
  the same shape). Writes `board.settings["team_shared_dir"]`.
- `sync cada` — stepper `− N +` minutes (5..120, default 30). Writes
  `team_sync_interval` (app.py:180) and `team.json["sync_tolerance_minutes"]`.
- `mi identidad` — chip from the roster (`TeamIdentityPicker` precedent,
  app.py:~314). Writes `board.settings["team_user_id"]`.
- Per team project row: name · `compartido` toggle (adds/removes the project
  dict in `team.json["projects"]` — the dict shape `team_sync.team_project_ids`
  expects) · hue swatch (cycles the project color) · template name.
- Per roster row: `██ id` · name · hue swatch. `a` adds a member (id prompt,
  unique), `x` removes (only with no assignee references — otherwise warn).

**Health checks — every row carries one, recomputed on open and on save:**
- `✓` green when verified working; `⚠` amber when attention is needed;
  the row's note says WHAT (never a bare icon). Glyph note: `✓` is already
  in the app's verified set (HEAT done glyph); `⚠` is new — pin a fallback
  (`!` amber) behind the repo's glyph-coverage discipline.
- Probes (each a function returning `(ok: bool, note: str)`):
  folder exists · folder writable (probe-write a temp file, delete it) ·
  folder reachability/lag (time the stat; warn over ~5s — the SharePoint
  case) · `team.json` parses + has roster · identity set and in roster ·
  last sync inside tolerance (`team_sync.sync_tone` already computes the
  tone) · roster non-empty.
- Checks are ADVISORY: they never block editing, and they re-run after
  `ctrl+s`.

**Editing semantics:** the screen edits a STAGED copy; `ctrl+s` commits
(writes team.json with a version bump — so teammates inherit on their next
sync — plus `board.settings`, saves, re-runs checks); `esc` discards.
Keybar (this screen only): `tab` sección · `↵` edita · `espacio` alterna ·
`a` agrega · `x` quita · `ctrl+s` guarda · `esc` cancela.

**AT sketch:** folder checks with tmp dirs (exists/writable/missing);
stepper clamps; shared toggle adds a well-formed project dict; version
bumps on save; esc leaves files byte-identical; `⚠` appears with its note
when the probe fails (mutation: unwritable dir → the row must show it).

## Part B — V9 · the help family (`?` opens the ACTIVE view's help)

Today `?` opens `HelpScreen` (app.py:79) — the FULL global keymap. New
law: **`?` opens the help of the view you're in**; the full-keymap screen
stays reachable as a second tier from inside it (`m` "mapa completo").

**Layout (all views, from the prototype):** header `AYUDA · <vista>` —
left column "para qué es / lo primero que haces / las marcas(o números)" —
right column "leyenda" (swatches) + "ejemplo anotado". Keybar: ONLY this
view's bindings + `esc cierra`.

**Content seats — never hand-maintained lists:**
- Legend: the existing `legend_entries(mode, ...)` (views.py:4669), which is
  already state-aware (a view that doesn't draw it doesn't advertise it).
- Keys: from the ONE keymap seat (`keymap.py`), filtered to the view —
  `fit_bar(width, view)` (keymap.py:181) already filters by view; reuse it,
  do not invent a second list.
- Usage text: authored per view — THE COPY IS IN
  `prototypes/team_sync/generate.py` (`v9` + `v9_family`), verbatim.

**The 8 views** (each with its authored text in the prototype): kanban,
lanes, agenda, gantt, focus, flow, standup, people. Setup (`0`) gets one
too — same layout (sections mirroring its three groups).

**Keybar law (the second amendment):** the footer bar shows ONLY the active
view's bindings. `fit_bar` already view-filters — audit what it emits per
view and tighten so the bar answers "what works HERE"; global commands live
in `?`/palette, never in the bar.

**AT sketch:** `?` from each view opens THAT view's help (pilot, per view);
the legend contains no swatch the view isn't painting (the ghost-mark law,
`tests/test_legend.py` precedent — the flow-view legend stays state-aware);
the help's key list ⊆ the view's `fit_bar` output; `m` reaches the old full
keymap.

## Suggested stories (Phase 0 confirms)

- **US-S1** initial sync on mount (the one-liner + its pilot test).
- **US-S2** Setup screen with staged editing, health checks, version-bump
  writes.
- **US-S3** per-view help family from the two seats (legend_entries +
  keymap), with the full-keymap second tier.
- **US-S4** keybar per-view audit + tighten.

## Verification (this repo's law, binds every increment)

- `python -m pytest tests/ -q` green; the clipboard test is an intermittent
  environmental flake (re-run alone once, report — not a batch signal).
- Mutation evidence executed per AT, transcripts in the increment reports.
- Deterministic tests: tmp_path boards + tmp shared dirs, injected clock,
  pilot for key behavior. Fixture privacy law: synthetic data only, never
  the operator's live board.
- Register decisions in `state.json.decisions_log` + the batch PLAN.md.
