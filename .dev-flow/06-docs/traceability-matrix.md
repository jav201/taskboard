# Traceability Matrix — taskboard — Batch 2026-07-18-batch-01

> **Artifact language:** English. Phase 6 artifact. Owner: `docs-writer`.
> Every requirement has a verifying node; every user story has one black-box acceptance node. Nodes reconcile to the `36 passed` suite run (Phase 4, `.dev-flow/04-validation.md`).

## At a glance (read first)

- **Coverage: 0 open gaps.** 3/3 user stories closed on BOTH chains (functional + behavioral); 7/7 HLR verified; 22/22 CI-gated LLR verified by ≥1 passing node; the single non-CI LLR (007.4, inline preview) is an intentional non-binding stretch that **degrades to the verified LLR-007.2**, so US-003's outcome is fully covered.
- **Suite:** `.venv\Scripts\python.exe -m pytest -q` → **36 passed** · `--collect-only` → **36 collected** · **0 fail · 0 pending**.
- **The 3 acceptance nodes are distinct and mutation-discriminating:** AT-001 → `test_at_001_seed_generic_and_complete`, AT-002 → `test_at_002_multiple_urls_black_box`, AT-003 → `test_at_003_images_black_box`.

---

## 1. Master table — functional chain (white-box)

> `File:line` = the shipped source that implements the LLR. `TC` = the test-case id from `01-requirements.md §5.2`. Node column = the actual collected pytest node + assertion line from `04-validation.md`.

| US | HLR | LLR | TC | File:line (implementation) | Verifying node (`tests/test_app.py::`) | Status |
|----|-----|-----|-----|-----------------------------|-----------------------------------------|--------|
| US-001 | HLR-001 | LLR-001.1 — all project statuses + archived project | TC-001a | `models.py:322-376` (`seed_data`) | `test_at_001_seed_generic_and_complete` `:539,:544` | pass |
| US-001 | HLR-001 | LLR-001.2 — all task statuses/priorities + archived task | TC-001b | `models.py:322-376` | `test_at_001_seed_generic_and_complete` `:541-542,:545` | pass |
| US-001 | HLR-001 | LLR-001.3 — all urgency buckets + standalone/project split | TC-001c | `models.py:322-376`; `views.py:206` (`urgency`) | `test_at_001_seed_generic_and_complete` `:547-553` | pass |
| US-001 | HLR-001 | LLR-001.4 — seed exercises new `urls[]` + `images[]` | TC-001d | `models.py:348-354` (seed tasks) | `test_at_001_seed_generic_and_complete` `:555-556` | pass |
| US-001 | HLR-001 | LLR-001.5 — no author-identifying token | TC-001e | `models.py:322-376` | `test_at_001_seed_generic_and_complete` `:536` (denylist over on-disk `board.json` == 0) | pass |
| US-001 | HLR-001 | LLR-001.6 — load-safe seed, invariants held | TC-001f | `models.py:234-247` (`Board.load`) | `test_boots_and_seeds`; `test_corrupt_file_starts_empty` | pass |
| US-002 | HLR-002 | LLR-002.1 — `Task.urls: list[str]` field | TC-002a | `models.py:190` | `test_task_urls_model_migration` `:406-407` | pass |
| US-002 | HLR-002 | LLR-002.2 — `from_dict` migrates legacy `url`, reads `urls` | TC-002b | `models.py:199-204` | `test_task_urls_model_migration` `:409-415` | pass |
| US-002 | HLR-002 | LLR-002.3 — save serializes `urls`, round-trips | TC-002c | `models.py:252-253` (`asdict`); `models.py:241` (load) | `test_task_urls_roundtrip`; `test_legacy_url_board_migrates_on_load` | pass |
| US-002 | HLR-003 | LLR-003.1 — modal presents all URLs for editing | TC-003a | `modals.py:67-69` (`#f-urls` TextArea) | `test_at_002_multiple_urls_black_box` `:454` (widget wired); prefill by inspection (see G-001) | pass |
| US-002 | HLR-003 | LLR-003.2 — modal save returns ordered valid-URL list | TC-003b | `modals.py:100,108` (`valid_url` filter → `data["urls"]`) | `test_at_002_multiple_urls_black_box` `:462` | pass |
| US-002 | HLR-004 | LLR-004.1 — card renders `↗` iff ≥1 valid URL | TC-004a | `views.py:163-164` (`has_url` gate); `views.py:122-127` (`title_markup`) | `test_at_002…` `:466`; `test_url_renders_link_and_arrow`; `test_columns_card_indicators_never_overlap_title` `:360-377` | pass |
| US-002 | HLR-004 | LLR-004.2 — open action opens all valid URLs | TC-004b | `app.py:259-266` (`action_open_url`), binding `app.py:54` | `test_at_002…` `:471` (real `o` keypress); `test_url_task_open_action` `:391` | pass |
| US-003 | HLR-005 | LLR-005.1 — `Task.images: list[str]` field | TC-005a | `models.py:191` | `test_task_images_model` `:478-479` | pass |
| US-003 | HLR-005 | LLR-005.2 — `from_dict` reads / `save` serializes `images` | TC-005b | `models.py:205`; `models.py:253` (`asdict`) | `test_task_images_model` `:480-488` | pass |
| US-003 | HLR-006 | LLR-006.1 — modal presents image refs for editing | TC-006a | `modals.py:71-74` (`#f-images` TextArea) | `test_at_003_images_black_box` `:578` (widget wired); prefill by inspection (see G-001) | pass |
| US-003 | HLR-006 | LLR-006.2 — modal save returns ordered image list | TC-006b | `modals.py:109` (`data["images"]`) | `test_at_003_images_black_box` `:581` | pass |
| US-003 | HLR-007 | LLR-007.1 — width-1 image indicator (`▤`) | TC-007a | `views.py:167-168` | `test_at_003…` `:586-588`; overlap invariant `:360-377` | pass (cell-width caveat, accepted) |
| US-003 | HLR-007 | LLR-007.2 — open-image action (browser / `os.startfile`) | TC-007b | `app.py:268-277` (`action_open_images`), binding `app.py:55` | `test_at_003…` `:594-595` (real `i` keypress); `test_open_images_allowlist_and_isfile` `:512` | pass |
| US-003 | HLR-007 | LLR-007.3 — image-extension allowlist gates `os.startfile` | TC-007c | `app.py:26` (`IMAGE_EXTS`); `app.py:279-296` (`_open_local_image`) | `test_open_images_allowlist_and_isfile` `:501-512`; `test_at_003…` `:596-597` | pass |
| US-003 | HLR-007 | LLR-007.4 — inline preview (OPTIONAL/stretch) | — (no CI TC) | not built — degrades to LLR-007.2 by design (`app.py:268-277`) | **degrades to** `test_at_003…` / `test_open_images_allowlist_and_isfile` (verified fallback) | accepted (non-binding `may`) |

**Every functional row has a verifying node.** LLR-007.4 is the only requirement without a dedicated CI node; it is a spec-sanctioned non-binding `may` (inline preview needs a terminal graphics protocol, unverifiable headlessly — Constraint C-5) whose mandatory fallback (open-in-viewer, LLR-007.2) is fully verified. Therefore no requirement is left unverified.

## 1b. Behavioral chain (black-box) — one acceptance node per story

> Each story observed through the SHIPPED surface (real Pilot keypress / on-disk `board.json`) with representative + boundary + negative evidence. Each AT reconciles to exactly one distinct collected node.

| US | Acceptance test (`AT-NNN` → node) | Shipped surface | Observed outcome / deliverable | Status |
|----|-----------------------------------|-----------------|--------------------------------|--------|
| US-001 | AT-001 → `test_at_001_seed_generic_and_complete` | `Board.load(fresh)`→`seed_data()`; on-disk `~/.taskboard/board.json` (`:535`) | Freshly seeded board: **0** author-denylist tokens over the persisted JSON (`:536`) + ≥1 item in every feature dimension (4/4 project statuses incl. `cancelled`, 4/4 task statuses, 3/3 priorities, all urgency buckets, ≥1 archived project + task, ≥2-URL task, ≥1-image task) | pass |
| US-002 | AT-002 → `test_at_002_multiple_urls_black_box` | `TaskModal #f-urls` → save handler → `card_cell`/`title_markup` → `action_open_url` bound to `o` (`app.py:54`) | 2 valid URLs kept in order; `↗` present in `board_text`; real `o` opens exactly the 2 valid URLs; markup/`not a url` lines dropped by `valid_url`, no MarkupError | pass |
| US-003 | AT-003 → `test_at_003_images_black_box` | `TaskModal #f-images` → save handler → `card_cell` `▤` → `action_open_images` bound to `i` (`app.py:55`) | `▤` present + all lines width-exact; real `i` opens the http image via browser + the existing image-ext file via `startfile`; `.svg`/`.exe`/missing file/UNC/`file://` NONE `startfile`'d | pass |

---

## 2. Coverage summary

| Metric | Value |
|--------|-------|
| Total user stories | 3 |
| Covered user stories (both chains) | 3 (100%) |
| Total HLR | 7 |
| Implemented + verified HLR | 7 (100%) |
| Total LLR | 23 |
| LLR verified by ≥1 CI node | 22 (95.7%) |
| LLR non-CI, accepted stretch (degrades to a verified LLR) | 1 — LLR-007.4 |
| Test cases + acceptance tests (collected) | 36 |
| Pass | 36 |
| Fail | 0 |
| Pending | 0 |
| Acceptance nodes (AT) | 3 (AT-001/002/003) — each a distinct node |

---

## 3. Detected gaps

> **No open coverage gap.** Every requirement maps to a verifying node; every AT maps to its single collected node. The two items below are documented as **accepted / non-blocking** (per `04-validation.md`), not open gaps.

| ID | Type | Description | Disposition |
|----|------|-------------|-------------|
| G-001 | minor — read-path convenience | No dedicated test asserts the modal, opened via `e` on a task with existing `urls`/`images`, pre-fills those refs one-per-line. The widgets' **presence and write path** ARE proven (AT-002/003 set `#f-urls`/`#f-images` `.text` and save successfully); the read-back prefill leg is covered by code inspection (`modals.py:68,72`). | **Accepted — not a deliverable gap.** Optional follow-up: an edit-path TC. Does not block the batch. |
| N/A | accepted stretch | LLR-007.4 inline image preview intentionally not built; the `may` clause degrades to open-in-viewer (LLR-007.2, verified). Inline rendering needs a terminal graphics protocol (Kitty/iTerm/Sixel), unverifiable headlessly (C-5). | **Accepted per spec — no overpromise.** US-003 outcome fully verified via the fallback. |

---

## 4. Changes from previous state (this batch)

| Type | Item | Detail |
|------|------|--------|
| new | HLR-005/006/007 + LLR-005.x/006.x/007.x | Images-per-task capability (model, modal, `▤` glyph, `i` open-image action with allowlist) |
| new | HLR-002/003/004 (list form) | Multiple-URLs-per-task (list model + legacy migration, modal TextArea, open-all `o`) |
| new | HLR-001 | Author-neutral, dimension-complete demo seed |
| modified | `Task.url: str` → `Task.urls: list[str]` | One-way forward migration (DD-2); superseded singular `url` has **0 live source references** (`04-validation.md` supersession inspection) |
| modified | `test_url_task_open_action`, `test_url_renders_link_and_arrow`, `test_columns_card_indicators_never_overlap_title` | Edited in place to the list API (migration touch, not deletion); ledger `28 − 0 + 8 = 36` |

---

## 5. Quick bidirectional mapping

### 5.1 By user story
- **US-001** → HLR-001 → LLR-001.1…001.6 → `test_at_001_seed_generic_and_complete` (+ `test_boots_and_seeds`, `test_corrupt_file_starts_empty`)
- **US-002** → HLR-002/003/004 → LLR-002.1…004.2 → `test_task_urls_model_migration`, `test_task_urls_roundtrip`, `test_legacy_url_board_migrates_on_load`, `test_url_renders_link_and_arrow`, `test_url_task_open_action`, `test_at_002_multiple_urls_black_box`
- **US-003** → HLR-005/006/007 → LLR-005.1…007.3 → `test_task_images_model`, `test_open_images_allowlist_and_isfile`, `test_at_003_images_black_box`

### 5.2 By code file
- `taskboard/models.py` → LLR-001.1…001.6 (`seed_data`), 002.1/002.2/002.3, 005.1/005.2 → seed + model/migration nodes
- `taskboard/modals.py` → LLR-003.1/003.2, 006.1/006.2 → modal nodes (via AT-002/003)
- `taskboard/views.py` → LLR-004.1, 007.1 → render/indicator nodes
- `taskboard/app.py` → LLR-004.2 (`action_open_url`), 007.2/007.3 (`action_open_images`, `_open_local_image`, `IMAGE_EXTS`)

---

## 6. Batch sign-off

| Field | Value |
|-------|-------|
| Batch ID | `2026-07-18-batch-01` |
| Closing date | 2026-07-18 |
| Total iterations (all phases) | 0 (each gate approved first pass) |
| Validation passed | yes (`04-validation.md` — PASS) |
| Open coverage gaps | 0 |
| Synced to Obsidian | no (pending `dev-flow-sync` after commit) |
