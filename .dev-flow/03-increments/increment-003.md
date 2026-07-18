# Increment 003 — US-1 Generic author-neutral demo seed (HLR-001)

## 1. What changed
- `seed_data()` fully rewritten to a neutral software-product org (Website Redesign / Mobile App / API Platform / Legacy Sunset / Data Warehouse / Internal Wiki). Reveals nothing about the author (0 denylist tokens) while exercising every board dimension.
- Design constraint honored: image-bearing seed tasks are normal/low priority with no URLs, so their card carries ONLY the `▤` glyph — never combined with `◉`/`↗` — keeping the existing overlap invariant test green without modifying it.

## 2. Seed coverage (independently verified, live seed)
- Project statuses: `cancelled, completed, on_track, paused` == full `PROJECT_STATUSES` (the previously-missing `cancelled` is now present).
- Task statuses: `active, backlog, blocked, done` (4/4). Priorities: `high, low, normal` (3/3).
- Archived: 1 project (Internal Wiki) + 1 task (Archive old logs).
- Urgency buckets: `done, later, none, overdue, today, week` (all).
- Standalone tasks: 3 · project-bound: 13.
- Multi-URL tasks: 1 (Fix checkout, 2 URLs) · image tasks: 2 (Design mockups ×2, Optimize image assets ×1).
- Denylist hits over serialized seed: `[]` (0).

## 3. Files modified (2)
- `taskboard/models.py` — `seed_data()` rewrite.
- `tests/test_app.py` — added AT-001 (`test_at_001_seed_generic_and_complete`) + `import re`.

## 4. How to test
`.venv\Scripts\python.exe -m pytest -q`  ·  new id: `test_at_001_seed_generic_and_complete`.

## 5. Test results
`36 passed in 12.59s` (35 → 36, +1). Ledger: base 28 → 36 (+8 total across the batch).
Mutation-sanity: renaming a project to "Textual Redesign" turned AT-001 RED (`assert ['Textual'] == []`); restored → green.
AT-001 reads the ACTUAL on-disk `board.json` for the denylist scan (observes the shipped deliverable) and derives every dimension check from the seed (input-set-as-oracle).

## 6. Risks
- The seed is heavier (16 tasks / 6 projects). Existing nav/scroll tests remain green; the agenda is intentionally tall enough for the overflow-scroll test.
- `▤`/`◉`/`↗` co-occurrence is deliberately avoided in the seed to preserve the overlap invariant; a future seed edit adding an image to a high-priority/URL task would break `test_columns_card_indicators_never_overlap_title` (guard is doing its job).

## 7. Suggested next task
Phase 4 validation (dev-flow): run the full two-layer matrix, confirm AT-001/002/003 + all TCs, then Phase 5/6 (post-mortem + docs/README update for the new URL/image capabilities and the `i` binding).

## Evidence checklist
- [✓] Tests pass — `36 passed`. No type/lint config in repo.
- [✓] No secrets in code or output. Seed scrubbed of author identity (0 denylist tokens, independently verified).
- [✓] No destructive commands run without approval.
- [✓] File count within cap — 2 files.
- [✓] Review packet attached — this file.
