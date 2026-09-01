# HANDOFF — taskboard batch-11: team sync (próximo agente, /dev-flow)

**For:** the agent who takes taskboard from personal tool to team tool.
**Status:** design COMPLETE and prototyped; nothing implemented. Resume by
running `/dev-flow` from this root — `state.json` points at batch-10
(`awaiting-handoff`, spec fully written in `handoff-batch-10.md`). **Batch-10
lands first**: the report (US-T3) consumes its `history.jsonl` and chains
(US-T6) consume its `depends_on` wiring. This batch's intake decisions are
ALREADY made (below) — Phase 0 is a confirmation, not a conversation.

**Read first (the spec is rendered, not described):**
- `prototypes/team_sync/NOTES.md` — the design record: decisions, verified
  laws, verdicts, open questions.
- `prototypes/team_sync/out/index.html` — 7 verified renders (V1..V7).
- `prototypes/team_sync/proto.py` — the sync state machine, 5 beats, laws
  asserted in code. Run it: `python prototypes/team_sync/proto.py`.

## 1. What this is (the operator's intent)

taskboard stays personal-first. Team mode adds: my team-project tasks sync
through a shared location on a daemon cadence (~30 min), so the team gets
joint visibility without a server — Teams/email already cover real-time.
Everyone shares the same task template, kanban stages, projects; assignees
appear from a roster.

## 2. Intake decisions (operator, 2026-08-24 — locked)

| question | decision |
|---|---|
| Topology | **One file per person** (`board.<user>.json`) in the shared location; each person writes ONLY their own; everyone reads everyone's (merged read-only). Conflicts disappear by construction. |
| What syncs | **Only team projects** (declared in `team.json`). Personal tasks never leave the machine (law asserted in proto.py BEAT 1). |
| Alignment | **`team.json` is authoritative**: phases · task template · projects · roster. A version bump is inherited on the next sync. |
| Assignees | **Roster in `team.json`** (id · name · hue). No free text. |

**The transport insight (binds the design):** a git checkout, a shared drive
and a SharePoint-synced folder are THE SAME SHAPE — a directory that appears,
disappears, and lags. The sync layer needs exactly one abstraction:
read/write files in a directory, tolerate absence, optional git pull/push
around it. No server, no API, no auth inside taskboard.

## 3. Verified laws (proto.py — re-verify them in Phase 1 tests)

1. Personal never leaks (asserted).
2. Owner-only writes; others merge read-only.
3. Offline is first-class: sync AGE visible on every foreign lane; a lane
   past tolerance marks STALE — never hidden, never deleted.
4. team.json version bumps inherit on next sync; tasks keep phase names
   (rename drift accepted and documented).
5. Staleness is stated, never silent.

## 4. Views (operator verdict: V2 + V3 chosen; V1 set aside)

- **V3 · standup strip = the team HOME** (glanced posture): one row per
  person — load `▰▱`, top task, phase, sync age; stale judged in red.
- **V2 · people lanes = the detail view** (operated): lane axis is WHO, not
  project; sync age in the person's label; others' cards read-only marked.
- **Classification filter** in the chrome of both: `todo · equipo ·
  personal` segmented control, NEXT TO the existing `/` search (never
  replacing it). Personal and project tasks coexist on every board; the
  filter keeps one screen honest about which world it shows.
- **V4 · project report**: hero = braille overlay of cumulative created
  (INK) vs completed (ACCENT) — never crossing by construction, so the
  sediment gap IS the open backlog. Below: **small multiples** per
  collaborator (same scale, total as dim reference line, roster hue).
  Ruling: N series of the same kind = small multiples, NEVER overlay;
  overlay is reserved for the one ordered pair. Then per-collaborator
  completion microbars, creation/completion rates, ratio. No history →
  "se construye desde hoy", invents nothing.
- **V5 · per-project task templates**: the project's rules declare text
  sections (e.g. *definición de problema*, *descripción de resolución*);
  the ficha renders them as labeled areas with dim provenance notes.
- **V6 · batch actions + email**: `espacio` multi-selects (solid ✓), an
  action bar (`e enviar por correo · m mover · a archivar · esc`), and the
  email DRAFT preview (tasks grouped by phase, format and content
  preserved, To/Subject prefilled).
- **V7 · task chains + day-shift insert**: chains wire via `depends_on`
  (batch-10 US-D); inserting inside a chain previews the downstream
  day-shift (`ago 28 → sep 1`, …) with the honest fork as actions:
  `↵` confirm shift · `s` insert WITHOUT shifting · `esc` cancel. Shift =
  inserted task's duration in days, applied to downstream due dates only;
  done tasks never move; the preview names every task before moving it.

## 5. Suggested stories and packaging (Phase 0 confirms)

| id | story | needs | note |
|---|---|---|---|
| US-T1 | Sync core: shared-dir config, push/pull cycle (in-app timer), per-person files, team.json inherit + first-run identity ("who are you?" from roster), staleness | — | the spine; writer/reader never-raise (Board.load precedent), foreign files untrusted |
| US-T2 | Team views: V3 standup home + V2 people lanes + classification filter | T1 | read-only merge surface; sync age everywhere |
| US-T3 | Project report (V4) | T1 + **batch-10** (history.jsonl) | consumes transitions log |
| US-T4 | Per-project templates (V5) | — | cheap, local; team.json carries them in team mode |
| US-T5 | Batch actions + email draft (V6) | — | Phase 1 decides `mailto:` vs `.eml` (Outlook association; format fidelity; ~2000-char mailto limits) |
| US-T6 | Chains + day-shift cascade (V7) | **batch-10 US-D** (depends_on wiring) | cascade preview = the acceptance surface |

Recommended packaging: **batch-11 = T1 + T2** (the spine) · batch-12 =
T4 + T6 · batch-13 = T3 + T5. E-trigger (≥3 stories) fires whatever the
packaging — declare rigor at intake.

## 6. Open questions the prototype did NOT answer (Phase 1 must)

- **Deletes:** owner deletes a task → absence propagates on next sync (the
  merged view re-derives from current files). Verify no tombstones are
  needed under per-person files — prove with a test.
- **team.json authorship:** any member edits the file in place; version
  bumps serialize changes. A team-admin convention is social, not code.
- **Read-retry:** SharePoint/OneDrive can surface a partially-synced file —
  every foreign file read is never-raises + well-formed-or-skipped.
- **Identity on first run:** team mode asks "who are you?" from the roster
  and writes only that file; a roster-less board cannot enter team mode.
- **Email mechanism:** `mailto:` vs `.eml` (see US-T5).

## 7. Verification law (this repo, binds every increment)

- `python -m pytest tests/ -q` green (880 + batch-10's additions at open).
  `test_win_clipboard_roundtrip` is an intermittent environmental flake —
  re-run it alone once and report; not a batch signal.
- Mutation evidence executed (RED arms), transcripts pasted in the increment
  reports — see PLAN.md of batch-10 for the standard.
- Deterministic tests: tmp_path boards, injected clocks, simulated shared
  directory as a tmp_path tree (proto.py's dict becomes real files).
- Commits per increment authorized IF the operator confirms the same
  standing authorization; **push only on explicit operator order.**

## 8. Register the decision

Record intake confirmations in `state.json.decisions_log` + the batch
PLAN.md; refresh `.dev-flow/BACKLOG.md` at close (C-44).
