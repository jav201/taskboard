# Executive summary — taskboard — Batch 2026-07-18-batch-01

> Phase 6 artifact. Audience: non-technical stakeholder. 1-2 pages. BLUF.

## 🔑 Bottom line (read first)

- **What we delivered:** we made the taskboard desktop widget **safe to publish** and gave a task two everyday attachments — **several links** and **images** — with an open-in-viewer action, all verified by an automated test suite.
- **Business outcome:** the public demo now reveals **zero** information about the author (privacy scrub), the tool self-demonstrates every feature to anyone who clones it, and the two new capabilities ship behind a **security guard** — **36 tests pass, 0 fail**.
- **Next step:** commit to `main` and add the new `i` (open-image) key to the public README (a 5-minute doc touch); optionally, sync the batch record to the knowledge vault.

---

## Context

`taskboard` is a small, frameless kanban board that floats always-on-top on the desktop — a personal, single-user productivity widget. Ahead of sharing the code publicly, two things needed attention: the built-in demo data leaked the author's real projects and links, and users wanted to attach more than one link — and images — to a task.

## Problem

- **Privacy leak.** The demo data that ships on first run named the author's real projects, an internal course, and a live personal URL. Anyone cloning the repo could infer who built it. It also happened to be *incomplete* — it never showed the "cancelled" project state or any archived items, so it under-sold the tool.
- **Single-link limit.** A task could hold only one URL and no images, so real work (an incident with two dashboards, a design task with two mockups) didn't fit.
- **A hidden safety risk in "just open the file."** Opening a local file by its type can *run* it, not just view it — so the image feature had to be built carefully, not naively.

## Solution

Three focused changes, delivered as three small increments and independently reviewed for security:

1. **Privacy scrub of the public demo.** The starter data was rewritten to a neutral, invented software company. It now reveals nothing about the author **and** showcases every feature — all project and task states, priorities, deadlines, archived items, links, and images — so the demo sells the tool on its merits.
2. **Multiple links per task.** A task now holds an ordered list of links; the card shows a small ↗ marker and one key opens them all. Boards created with the old single-link format are migrated automatically, with no data loss.
3. **Images per task, opened safely.** A task can hold image references (local files or image links); a distinct marker appears on the card, and one key opens each — links in the browser, local images in the default viewer. **Only recognized image files are ever opened**, and risky paths (network shares, executable types) are refused by design, so the feature cannot be tricked into running a program.

## Outcomes / results

| Result | Evidence |
|--------|----------|
| **0** author-identifying tokens in the public demo | Scanned over the actual saved data file — 0 of 16 tracked tokens (down from 16) |
| Demo exercises **100%** of feature dimensions | All project/task states, priorities, urgency buckets, archived items, links, images present |
| **36** automated tests pass, **0** fail, **0** pending | Full suite run 2026-07-18 (`36 passed`) |
| Security-guarded image opening | Independent security review folded in; only allowlisted image files reach the OS viewer; a re-check confirmed a disallowed type is refused |
| **0** open coverage gaps | Every requirement and every user story maps to a passing verifying test |
| No regression in existing behavior | The prior test suite stayed green through the change |

**Scope honesty:** inline image *preview inside the terminal* was intentionally **not** built — it depends on terminal features we cannot guarantee — so images open in the normal viewer instead. This was a deliberate decision, not a shortfall, and the delivered path is fully tested.

## Next steps

1. **Now:** commit the batch to `main` (authorized) — code + engineering artifacts.
2. **This week (≈5 min):** add the new `i` "open image" shortcut to the public README keybindings table.
3. **Optional:** sync the batch documentation to the Obsidian knowledge vault; add one convenience test for editing a task's links/images (a minor read-path nicety, not a gap).
