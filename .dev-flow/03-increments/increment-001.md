# Increment 001 — US-2 Multiple URLs per task (HLR-002/003/004)

## 1. What changed
- `Task.url: str | None` replaced by canonical `Task.urls: list[str]` (`field(default_factory=list)`).
- `Task.from_dict` migrates a legacy single `url` string into a one-element `urls` list (one-way, DD-2), reads a modern `urls` list, and degrades malformed input to `[]` without raising. `Board.save` writes only `urls` (legacy key dropped on next save).
- TaskModal now edits multiple URLs via a `TextArea` (`#f-urls`, one per line); on save each line is stripped and filtered through `valid_url`, keeping only valid http(s) URLs in order under `data["urls"]`.
- Card `↗` indicator now fires when `any(valid_url(u) for u in task.urls)`; the OSC-8 `[link=]` target is the FIRST valid URL (F6).
- Open action (`o`) opens EVERY valid URL (http/https only, via `valid_url`), not just one (DD-3).
- Seed's 3 legacy `url=` kwargs migrated to `urls=[...]` so the app still boots (full author-neutral rewrite is Increment 3).

## 2. Files modified (5 — at cap, no tcss needed)
- `taskboard/models.py` — `urls` field + migration in `from_dict`; seed kwargs.
- `taskboard/views.py` — `first_valid_url()` helper; `has_url()`; `title_markup` OSC-8 target; `card_cell` indicator gate.
- `taskboard/app.py` — `action_open_url` opens all valid URLs.
- `taskboard/modals.py` — `TextArea` URL entry + `valid_url` filtering on save; `_lines` helper.
- `tests/test_app.py` — updated 2 breaking tests + added 4 (TC-002a/b/c, migration-on-load, AT-002).

## 3. How to test
`.venv\Scripts\python.exe -m pytest -q`
Key new ids: `test_task_urls_model_migration`, `test_task_urls_roundtrip`, `test_legacy_url_board_migrates_on_load`, `test_at_002_multiple_urls_black_box`.

## 4. Test results
`32 passed in 11.74s` (base 28 + 4 new). Ledger: 28 → 32.
Mutation-sanity: reverting open-all to first-URL-only turned AT-002 RED (`assert ['one'] == ['one','two']`); restored → green.

## 5. Risks
- DD-2 one-way migration: old readers of a new file lose links (accepted, single-user local app).
- `TextArea` height set programmatically to 4 (1fr collapses in the auto-height modal); visual only, verified functionally by AT-002, not by eye in a real terminal.

## 6. Pending items
- Increment 2 (images) and Increment 3 (generic seed) still contain author tokens in the seed — expected, removed in Increment 3.

## 7. Suggested next task
Increment 2 — US-3 images per task (model list, modal TextArea, image glyph, `i` open-image action with os.startfile allowlist + isfile/UNC guards, F2/F3/F4).

## Evidence checklist
- [✓] Tests/type/lint pass — `32 passed` (pytest output above). No type/lint config in repo.
- [✓] No secrets in code or output.
- [✓] No destructive commands run without approval.
- [✓] File count within cap — 5 files.
- [✓] Review packet attached — this file.
