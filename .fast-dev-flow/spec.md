# Quick Spec — taskboard: task notes + read-only details view

> Minimal spec for `/fast-dev-flow`. Acceptance criteria are observable.

---

## 1. Objective (1 line)

Give tasks an optional free-text **notes** field and a **read-only details view** (a keybinding) that shows every field of the selected task — including its images rendered inline — without opening the edit modal.

---

## 2. User stories

- As a user, I want to attach longer notes/description to a task, so that a card can carry detail that doesn't fit in the title.
- As a user, I want to press one key to see all of a task's data (including its images) read-only, so that I can review it without risking accidental edits.

---

## 3. Acceptance criteria (observable)

- [ ] **AC1 — model back-compat:** When a `Task` is loaded from a `board.json` that has **no** `notes` key, the system shall load it with `notes == ""` (no crash, existing boards unaffected).
- [ ] **AC2 — persist notes:** When the user types text into the notes field of the edit modal and saves, the system shall persist that text to `board.json` and reload it on the task's `notes` after a fresh `Board.load`.
- [ ] **AC3 — open details:** When a task is selected on the board and the user presses **Enter**, the system shall push a read-only details screen (`TaskDetails`) and shall **not** push the edit modal (`TaskModal`).
- [ ] **AC4 — shows all fields:** When the details screen is open, it shall display the task's title, project name (or "Inbox"), status, priority, start/due dates, URLs, and notes.
- [ ] **AC5 — renders images inline:** When the selected task has image paths/URLs, the details screen shall render each local image inline (same mechanism as `ImageViewer`) and list remote-URL images as links; a missing/bad file shall show a "missing/could not render" line, never crash the modal.
- [ ] **AC6 — read-only + safe render:** The details screen shall expose no Save/edit control; `esc` closes it. Notes and all user text shall be passed through `rich.markup.escape()` so square-bracket content cannot inject Rich markup (pitfall A1).

---

## 4. Validation strategy

Unit + Textual `pilot` tests in `tests/test_app.py`, one per AC where feasible:
- AC1: `Task.from_dict({...no notes...}).notes == ""`.
- AC2: drive the edit modal, set the notes `TextArea`, save, `Board.load` from the same path, assert `notes` persisted.
- AC3: seed a task, `pilot.press("enter")`, assert `app.screen` is a `TaskDetails` (and pressing enter did not open `TaskModal`).
- AC4/AC5: mount `TaskDetails` for a task with a real temp PNG + a remote URL + a missing path; assert it composes without error and the labels contain the field values.
- AC6: `TaskDetails` has no `#save` button; a title containing `[red]x[/red]` renders escaped (assert the modal builds and the raw string is treated as literal).
Manual smoke: run the app, press Enter on a seeded task, confirm the panel + image render, press esc.

---

## 5. Non-goals

- No change to card rendering on the board (no "has notes" glyph) — existing look stays as-is.
- No editing from the details view (no inline edit, no jump-to-edit shortcut required).
- No new persistence format/migration beyond the additive `notes` field.
- No change to the existing `i` ImageViewer or `o`/`e`/`d` bindings.

---

## 6. Detected security flags

- [ ] Auth / identity
- [ ] Secrets / config
- [ ] External integrations
- [ ] Sensitive data
- [ ] Destructive DB
- [x] Input / attack surface (free-text user input rendered in the TUI)
- [ ] Network / exposure

**`security_required`:** `true`

**Risk summary:** The only flag is **input/rendering**: `notes` is free-text user input shown in a Rich/Textual `Label`. This codebase has a documented markup-injection pitfall (A1) and already `escape()`s all user-controlled text (titles, project names). The notes field — and every user string shown in `TaskDetails` — must go through `rich.markup.escape()`. Local image opening already has an allowlist/existence gate (`_open_local_image`, C-6/F3/F4); the details view only *renders* via the existing `ImageViewer` path and adds no new file-execution surface. No secrets, network, or DB surface. Mitigation is a one-line-per-field discipline, verified by AC6's test.

---

## 7. Batch status

| Field | Value |
|-------|-------|
| Current phase | closed |
| Started | 2026-07-20 |
| Closed | 2026-07-20 |
| Promoted to /dev-flow | no |
| Notes | single 5-file increment; 51/51 tests pass |

---

## 8. Close (filled in phase C)

### What changed
Added an optional free-text `notes` field to `Task` (additive/back-compatible) with a matching notes box in the edit modal, and a read-only `TaskDetails` screen opened with **Enter** that shows every field of the selected task — project, status, priority, dates, URLs, notes — with images rendered inline (via a shared `image_block` helper extracted from `ImageViewer`). No board-card changes; no existing binding changed.

### How it was tested
- `test_task_notes_backcompat_from_dict` (AC1) · `test_task_notes_persist_through_reload` (AC2) · `test_enter_opens_readonly_details` (AC3/AC6) · `test_details_shows_all_fields_and_image` (AC4/AC5) · `test_details_escapes_notes_markup` (AC6) · `test_image_block_link_and_missing_fallbacks` (AC5).
- Full suite: **51 passed** (45 pre-existing + 6 new). Pilot tests drive real `enter` keypresses = runtime smoke.

### Open risks / pending
- None functional. Note: the project `.venv` lacks Pillow (pre-existing); tests must run under an interpreter with Pillow + textual-image + pytest-asyncio.

### Security flags — handling
Input/rendering flag: every user string in `TaskDetails` (title, status, priority, dates, project name, notes, URLs) passes through `rich.markup.escape()`; `test_details_escapes_notes_markup` proves `[bold]…[/bold]` in notes renders literally. Two bugs caught by *running*: a Rich-markup path and a `self._task` collision with Textual's internal message-pump task (renamed `self._detail_task`). No new file-exec/network/DB surface — `open_all_images_raw` reuses the existing allowlist/existence gate.

### Suggested commit message
```
feat(task): notes field + read-only details view with inline images

Add an optional free-text notes field to Task (backward-compatible) and a
TaskDetails screen (Enter) showing all task data read-only, images inline.
Extract a shared image_block helper from ImageViewer. All user text escaped.
```
