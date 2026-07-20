# Quick Spec — taskboard: reliable paste + calendar date picker

> Minimal spec for `/fast-dev-flow`. Acceptance criteria are observable.

---

## 1. Objective (1 line)
Make text **paste** work reliably (Ctrl+V from any Windows app) and replace flow-stopping typed dates with an **arrow-key calendar picker**, while keeping typed dates working.

---

## 2. User stories
- As a user, I want to paste text I copied from another app into a task's title/notes/URLs, so I don't have to retype it.
- As a user, I want to pick dates from a calendar instead of typing `YYYY-MM-DD`, so setting a due date isn't a chore.

---

## 3. Acceptance criteria (observable)
- [ ] **AC1 — clipboard text read:** `grab_clipboard_text()` returns the OS clipboard's text as a `str`, or `None` when it holds no text / on any error (never raises). Windows uses `ctypes` `CF_UNICODETEXT`; macOS `pbpaste`; Linux `xclip`/`xsel`.
- [ ] **AC2 — paste into Input:** When a text `Input` is focused in a modal and the user presses **Ctrl+V**, the system shall insert the clipboard text at the cursor (verified by monkeypatching `grab_clipboard_text` and asserting the Input's value contains it).
- [ ] **AC3 — paste into TextArea:** Same as AC2 but for a focused `TextArea` (e.g. the notes field) — clipboard text is inserted into the TextArea.
- [ ] **AC4 — paste guard:** When the clipboard has no text (or no text field is focused), Ctrl+V shall show a friendly `notify` and change no field (no crash).
- [ ] **AC5 — calendar opens & returns a date:** A `CalendarModal` seeded with a date string shall, on **Enter**, dismiss returning the highlighted day as `YYYY-MM-DD`; **esc** dismisses returning `None`.
- [ ] **AC6 — calendar navigation:** In `CalendarModal`, left/right move ±1 day, up/down ±1 week, `[`/`]` (and pageup/pagedown) ±1 month, `t` jumps to today — each changing the highlighted date.
- [ ] **AC7 — wired into the modals:** Pressing the calendar button next to a date field in `TaskModal`/`ProjectModal` opens `CalendarModal`; picking a day writes `YYYY-MM-DD` into that field's `Input`. Typing a date directly still works and still saves.
- [ ] **AC8 — back-compat:** All existing tests still pass; no change to persistence, the board file format, or existing bindings other than adding Ctrl+V (paste) and the calendar buttons.

---

## 4. Validation strategy
Pytest + Textual `pilot` (asyncio auto), in `tests/test_app.py`:
- AC1: monkeypatch the platform read; assert `str`/`None` and no raise on failure.
- AC2/AC3: open TaskModal, focus title `Input` / notes `TextArea`, monkeypatch `grab_clipboard_text` → `"PASTED"`, press `ctrl+v`, assert the widget contains it.
- AC4: monkeypatch to `None`, press `ctrl+v`, assert no crash and field unchanged.
- AC5/AC6: mount `CalendarModal("2026-07-20")`, drive keys via pilot, assert the dismissed result / highlighted date (`right`→21, `down`→27, `]`→Aug, `t`→today).
- AC7: open TaskModal, press the start-date calendar button, pick a day, assert `#f-start` value is a valid `YYYY-MM-DD`.
- AC8: full suite green.

---

## 5. Non-goals
- No recurring dates, ranges, times, or locale/first-day-of-week config (Mon-first, fixed).
- No new dependency (stdlib `calendar` + `datetime` only).
- No change to how dates are stored or validated on save (still ISO strings via `parse_iso`).
- Not touching the board/agenda/gantt views or the image-paste button.

---

## 6. Detected security flags
- [ ] Auth / identity
- [ ] Secrets / config
- [ ] External integrations
- [ ] Sensitive data
- [ ] Destructive DB
- [x] Input / attack surface (pasted clipboard text is user input; Linux read shells out to `xclip`/`xsel`)
- [ ] Network / exposure

**`security_required`:** `true`

**Risk summary:** Two mild input-surface points. (1) **Pasted text** is user-controlled — but it's inserted as literal data into an `Input`/`TextArea`, never rendered as markup here; places that later render task text already `rich.markup.escape()` it (card titles, the details view). No new render path. (2) The **Linux clipboard read** invokes `xclip`/`xsel` — must use a fixed `subprocess` argv list (no `shell=True`, no interpolation) so nothing can inject a command; macOS `pbpaste` likewise. Windows uses `ctypes` (no process). All reads wrapped to never raise. No secrets, network, or DB surface.

---

## 7. Batch status
| Field | Value |
|-------|-------|
| Current phase | closed |
| Started | 2026-07-20 |
| Closed | 2026-07-20 |
| Promoted to /dev-flow | no |
| Notes | builds on merged notes/details feature; prior spec archived; independent code-review audit passed |

---

## 8. Close (filled in phase C)

### What changed
Added reliable **Ctrl+V text paste** (`grab_clipboard_text()` — Windows `ctypes`, macOS `pbpaste`, Linux `xclip`/`xsel`, never raises — inserted into the focused `Input`/`TextArea` via a priority `ctrl+v` binding on the text-field modals) and a **`CalendarModal` date picker** (stdlib `calendar`+`datetime`; arrow-key nav, `t`=today, Enter→`YYYY-MM-DD`, Esc cancels) opened from a 📅 button beside each date field in `TaskModal`/`ProjectModal`. Typing dates still works; persistence/format unchanged.

### How it was tested
- 7 new tests (AC1–AC7) in `tests/test_app.py`; AC6 expanded to both directions + a short-month day-clamp (Jan 31 → Feb 28).
- Full suite: **58 passed**, 0 failed.

### Open risks / pending
- None blocking. Windows clipboard path is the one exercised on this machine; the Linux `xclip`/`xsel` argv branch isn't run under CI-on-Windows (guarded, never raises).

### Security flags — handling
Input/surface flag: pasted text is inserted as **literal data** (`insert_text_at_cursor`/`insert`), no new render path; existing render paths already `escape()`. Linux/macOS clipboard read uses a **fixed `subprocess` argv (no shell, 2s timeout)**; Windows uses `ctypes` with `finally` cleanup (no leaked clipboard lock). `grab_clipboard_text` is double-guarded and never raises. Independent code-review confirmed PASS.

### Notable bug caught in-flight
`CalendarModal` first named its redraw helper `_render` — which **shadows Textual's internal `Widget._render()`** (must return a `Visual`), making the screen's visual `None` and crashing `render_strips`. Renamed `_redraw`. Same name-collision class as the documented `self._task` pitfall.

### Suggested commit message
```
feat(modals): Ctrl+V clipboard paste + calendar date picker

Add grab_clipboard_text() (Windows ctypes / macOS pbpaste / Linux xclip|xsel,
never raises) and a Ctrl+V paste action into the focused Input/TextArea on the
text-field modals. Add CalendarModal (stdlib calendar/datetime) opened from a
button beside each date field; arrow-key nav, t=today, Enter picks. Typing
dates still works. Redraw helper is named _redraw (not _render) to avoid
shadowing Textual's Widget._render.
```
