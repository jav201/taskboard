# Increment 002 — US-3 Images per task (HLR-005/006/007)

## 1. What changed
- `Task.images: list[str]` added (`field(default_factory=list)`), read leniently in `from_dict` (non-list → `[]`), persisted via `asdict`.
- TaskModal now edits image refs in a second `TextArea` (`#f-images`); on save every non-blank line is kept in order under `data["images"]` (NO http filter — local paths are valid at entry).
- Card renders a width-1 `▤` (sky) image glyph when `task.images` is non-empty, distinct from `↗`/`◉`.
- New `i` binding → `action_open_images`: each ref that is a valid http(s) URL opens in the browser; each local path opens via `os.startfile` ONLY if it passes ALL guards.
- `import os` added.

## 2. Security guards on the os.startfile branch (F3/F4 folded from Phase 2 review)
`_open_local_image(ref)` opens a local path only when:
- not a UNC path (`\\` or `//` prefix) — refused;
- not a `file://` URL — refused;
- `Path(ref).suffix.lower()` in allowlist `{.png,.jpg,.jpeg,.gif,.webp,.bmp}` — **.svg excluded** (scriptable, F4);
- `os.path.isfile(ref)` is true (existing regular file, F3);
- wrapped in `try/except OSError` so a keypress never crashes.
Anything failing any check is silently skipped.

## 3. Files modified (5 — at cap)
- `taskboard/models.py` — `images` field + lenient read.
- `taskboard/views.py` — `▤` image glyph in `card_cell`.
- `taskboard/modals.py` — `#f-images` TextArea + `data["images"]`.
- `taskboard/app.py` — `IMAGE_EXTS`, `i` binding, `action_open_images`, `_open_local_image`.
- `tests/test_app.py` — added 3 (TC-005a/b, TC-007c, AT-003).

## 4. How to test
`.venv\Scripts\python.exe -m pytest -q`
New ids: `test_task_images_model`, `test_open_images_allowlist_and_isfile`, `test_at_003_images_black_box`.

## 5. Test results
`35 passed in 12.28s` (32 → 35, +3). Ledger: base 28 → 35.
Mutation-sanity: re-adding `.svg` to `IMAGE_EXTS` turned AT-003 RED (svg reached startfile); restored → green.
AT-003 presses the real `i` key (F2), asserts glyph + width-invariance + startfile/browser routing + negatives (.svg/.exe/missing/UNC/file:// never executed).

## 6. Risks
- `os.startfile` is Windows-only (DD-4); non-Windows local-image open is a documented limitation. http(s) image refs work cross-platform.
- `▤` cell width is verified single-cell via Python-len line-width invariance headlessly; true terminal cell width in WezTerm is a Phase-3/manual render check (C-2/C-5), not asserted in CI.
- Inline preview (LLR-007.4) intentionally NOT implemented — degrades to open-in-viewer (stretch, out of core scope).

## 7. Suggested next task
Increment 3 — US-1 generic author-neutral demo seed (0 denylist tokens, all 4 project statuses incl. cancelled, ≥1 archived project + task, multi-url + image tasks) + AT-001.

## Evidence checklist
- [✓] Tests pass — `35 passed`. No type/lint config in repo.
- [✓] No secrets in code or output.
- [✓] No destructive commands run without approval.
- [✓] File count within cap — 5 files.
- [✓] Review packet attached — this file.
- [✓] Security surface (os.startfile) implemented to Phase-2 spec (F3/F4 guards); allowlist excludes .svg.
