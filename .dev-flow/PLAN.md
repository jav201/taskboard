# PLAN — taskboard · batch 2026-07-18-batch-01 (living compendium)

## BLUF
Full `/dev-flow` V-model audit of the taskboard tool + 3 code changes, run **end-to-end autonomously**, **committed straight to main** (operator authorization 2026-07-18: "End to end autonomously… Commit straight to main").

## Objective / scope (3 stories)
- **US-1** Replace personal seed data (GRNDIA/Textual/job-hunt/real URL) with generic capability-showcase demo data.
- **US-2** Multiple URLs per task (model list + migration, modal input, ↗ render, open action).
- **US-3** Images per task (store image refs, indicator, open-in-viewer; inline preview = optional/terminal-dependent stretch).
Plus the full artifact set (requirements→review→increments→validation→postmortem→docs).

## Standing authorization
Autonomy: self-approve every gate vs objective exit criteria, document each decision. Merge: commit to main (no PR).

## Roadmap / phase status
- [x] P1 Requirements — architect agent running → 01-requirements.md
- [x] P2 Cross-review → 02-review.md
- [x] P3 Implementation (3 increments) → code + tests + 03-increments/
- [x] P4 Validation → 04-validation.md
- [x] P5 Post-mortem → 05-postmortem.md
- [x] P6 Docs (traceability/functionality/diagrams/exec-summary) → 06-docs/ ; commit to main

## Decisions log
- 2026-07-18 · Kickoff · autonomy=end-to-end, merge=commit-to-main, +US-3 (images) added mid-kickoff. Route: full /dev-flow (operator-requested "whole SW engineering artifacts").

## Risks / watch-items
- Images inline preview is terminal-protocol-dependent (Kitty/iTerm) & unverifiable headlessly → core = store+open-in-viewer, preview flagged stretch.
- Repo edit-guard blocks orchestrator's direct Edit tool; artifacts written by agents / via Bash.
- ≤5 files/increment; keep the 28 existing tests green + add new.

## Out-of-scope carries
- project-status edit binding (parked earlier), wezterm repo paste-binding sync (minor).
