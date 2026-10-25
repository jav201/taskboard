# PLAN — taskboard — Batch 2026-10-25-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 at both levels; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/guides/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.
> **Two header labels are read literally and are never translated:** `Standing authorization` and `Last updated`; the field guide names their readers.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-25-batch-02 |
| Objective | the presentation's note rows (gantt cursor note view 1, split view 2 and their x exports; view 3 checked) colour the notes' ==..==, !!..!! and ++..++ highlights through views.highlight_segments, dropping the markers and keeping the presentation's own base tone, so the room never sees raw markers (PH-1..PH-4) |
| Last updated | P1 · 2026-10-25 |
| Standing authorization | The operator, 2026-10-25, on the ordered backlog: «Sigue con 4 con Kimi.» — item 4 of `.dev-flow/BACKLOG.md` (the people-round finding), commissioned in `.dev-flow/COMMISSION-present-note-highlights.md`. Read from the commission and the task: autonomy over the gates the commission names (P0..P5 plus the commissioned PDR/DDR reviews); merge/push NOT granted («Do NOT push or merge»); a HIGH finding blocks regardless and returns to the operator. |
| First gate | exit 0 · 0 block / 165 notice / 62 n/a · `V7`: bundle identical to the manifest it ships, both directions (57 declared files unmoved, 0 undeclared) at `2026-10-12-rev102` |
| Premises / RC-1 | `origin/main` verified at `6e72e2a` (2026-10-25 15:53 -0600); RC-1(a): merge-base of HEAD equals the origin/main tip — HEAD is strictly ahead (rebase a no-op); RC-1(b): the story is NOT already shipped — `origin/main:taskboard/views.py` still draws the presentation note rows without `highlight_segments`; RC-2: `git ls-remote --exit-code --heads origin` answered (refs listed; newest `origin/main` commit dated today). Premises: `views.highlight_segments` is the one tokeniser; the presentation keeps its own base tone (`ink`); tests drive the app by keys. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — the planned change creates no module and moves no boundary; commission caps the source set at `taskboard/views.py` |
| A2 | not fired | judged — the planned touch set is ONE source module (`taskboard/views.py`; tests are not product modules per the module map), below ≥2 |
| A3 | not fired | judged — no interface another module consumes changes; the fix consumes the existing `highlight_segments` |
| A4 | not fired | judged — one story, one increment (commission §Increments) |
| B1 | fired | `grep -rl highlight_segments tests/` → `tests/test_edit_window.py`, `tests/test_highlight_segments.py` — owned by other requirements; reverse census (C-26) due at P2/P3 |
| B2 | not fired | judged — no file moves location on disk |
| B3 | not fired | probe — `tests/goldens/` does not exist in this tree; no byte-identical golden captures the touched source |
| B4 | not fired | judged — the `x` SVG/PNG export is consumed by no component (a user artifact, not an input) |
| C1–C7 | not fired | judged — no auth/secrets/external-integration/sensitive-data/destructive-DB/input-surface/network content in colouring note text; the Phase-1 scan is the mechanized probe |
| C8 | fired | judged — the fix turns on markup/ANSI rendering over file-derived note text (C-17); scan mechanizes at P1 |
| D1 | fired | judged — the room sees the notes' colours change (the presentation is a user-visible surface) |
| D2 | not fired | judged — no prototype; the commission declares «No prototype» |
| E1 | not fired | judged — 1 story, 1 increment |
| E2 | not fired | judged — no high risk declared at intake |
| E3 | not fired | judged — the operator's own presentation tool, not a client deliverable or regulated context |
| F1 | not fired | bundle runtime — `V7` line stands as the probe: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | `.dev-flow/BACKLOG.md` carries «Last refresh: 2026-10-25 (2026-10-25-batch-01 close)» |
| PDR/DDR take-up | operator directive | the commission's SWARM paragraph names the PDR (architect) and DDR (qa + ux) reviews explicitly; taken up at intake by the operator's directive (no A-family trigger fired), recorded here and in the P0 decision |

## Where we are

P0 intake. The batch opened by rollover from `2026-10-25-batch-01`; RC-1/RC-2 verified; triggers evaluated (B1, C8, D1 fired; PDR/DDR taken up by operator directive); the story passed INVEST and the Definition of Ready (READY). Owed next: the P0 gate run, the batch-open commit, then P1 requirements.

## Objective

The presentation's note rows (gantt cursor note view 1, split view 2 and their `x` exports; view 3 checked) colour the notes' `==..==`, `!!..!!` and `++..++` highlights through `views.highlight_segments`, dropping the markers and keeping the presentation's own base tone, so the room never sees raw markers (PH-1..PH-4).

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-2901 (BACKLOG item 4, the people-round finding) | READY | INVEST evaluated at intake; DoR passed; sole story of the batch |
| P0 | in-progress | intake done; gate run + commit owed |
| P1..P5, PDR, DDR | pending | PDR/DDR taken up by operator directive (commission SWARM paragraph) |

## Roadmap + increment plan

One increment, 001: `taskboard/views.py` only (at most 4 SOURCE files), tests uncapped. AT-a..AT-e per the commission §Acceptance; the PDR precedes P3, the DDR follows it, qa-reviewer reviews again at P4.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-25 | PH-1 one tokeniser; PH-2 visible-width wrapping; PH-3 mentions/bullets/unpaired markers; PH-4 exports match the screen | the commission's decisions, recorded at intake; each is carried into the P1 contract |

## Risks / watch-items

- width accounting must drop the markers before `_wrap_cells`, or highlighted rows cut early · medium · the PDR pins the width rule and AT-b covers the wrap
- oracle fixtures that legitimately hold raw markers change at AT-e · low · packet justifies each change

## Conventions honored

- artefacts and commits in English · synthetic data only · `username_subject` placeholder, never the operator's real name
- every pytest run with `env -u NO_COLOR`; import probe before any test
- no push/merge; commits end with the Kimi co-author trailer

## Out-of-scope carries

- the `x` export of view 1 and view 3 use the same note pipeline — covered by PH-4 where they share it; any path found NOT sharing it is named in the PDR
- BACKLOG items 1–3 and 5+ of the people round stay open in `.dev-flow/BACKLOG.md`

## Gate notices and runtime absences

- Start gate (run over the freshly opened batch): the step-3 expected NOTICEs (V9/V27/V31–V51/V54 family — seeded fields); V25/V30 at every gate from a bundle; V40 resolved by this worktree's rollover (owner re-stamped to `present-hl`).
- P0 gate: step-3 NOTICEs on the fresh batch record only; 0 block.
- P1 gate (evidence/gate-p1.txt): 0 block, 179 notice, 50 n/a. V53 notices are expected (the contract names AT-2901..AT-2905 test nodes minted at P3); V27 left with the first dated decision; the scan (evidence/scan-p1.txt) flags `role`/`form`/`escape`, answered in §6.3 — `escape` is the C-17 control itself (LLR-2901.2), the other two are prose matches.
- Runtime absences (named once, per `SKILL.md` §*What refuses an invocation here* step 5): no named reviewer roles, no hooks, no prompt guard, no slash commands — reviewer roles run as spawned generic sub-agents carrying the bundle's `agents/<role>.md`; gates close under the standing authorization above. Rules `not-run` from a bundle: V15 (no canon tree), V16 (no checkout table), V17 (no settings.json hooks). V30 runs half (witnesses this interpreter; the three derived floors not derivable from a bundle). dev-flow-sync: `not-run` — no export destination declared, and push/merge not granted.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `env -u NO_COLOR python -m pytest .scratch/test_import_probe.py -s -q` | 2026-10-25 | 1 passed — `taskboard.__file__` resolves to the worktree (`evidence/import-probe.txt`) |
