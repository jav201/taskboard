# Functionality — taskboard — Batch 2026-07-18-batch-01

> **Artifact language:** English. Phase 6 artifact. Owner: `docs-writer`. Audience: technical stakeholder.
> Accurate to the code at commit state 2026-07-18 (`36 passed`). Symbols cited `file:line`.

## 🔑 At a glance (read first)

- **What this batch added:** three user-facing changes to an existing frameless Textual kanban desktop-widget — (1) a **privacy-scrubbed, capability-complete demo seed**, (2) **multiple URLs per task**, (3) **image references per task** with a security-gated open-in-viewer action.
- **Capabilities:** a task now holds an ordered `urls[]` **and** `images[]` list · `o` opens every valid URL, `i` opens each image (browser for `http(s)`, `os.startfile` for allowlisted local image files) · the built-in demo data reveals nothing about the author yet exercises every board dimension.
- **How to use it:** run `taskboard` (or `python -m taskboard`); press `a`/`e` to add/edit a task, enter URLs and image refs one-per-line in the modal, then press `o` / `i` on the selected card.

> Enough to know what shipped and how to reach it. Detail below.

---

## What taskboard is

`taskboard` is a **single-process Textual TUI kanban board designed to run as a frameless, always-on-top desktop widget**. It persists to one JSON file at `~/.taskboard/board.json` (`models.py:136-142`); a missing file is seeded from `seed_data()` and saved, and a corrupt file starts empty and is left untouched so the user can recover it by hand (`models.py:234-247`). It is built and pinned against **Textual 8.2.8 / rich 15.0.0** on Python ≥3.10 (`requirements.txt`, `pyproject.toml`).

### The four views (same data, four lenses)

| Key | View | Renderer | What it shows |
|-----|------|----------|---------------|
| `1` | **Swimlanes** | `render_swimlanes` `views.py:311` | Projects as rows × TODO/DOING/DONE columns, with a per-project progress bar. |
| `2` | **Columns** | `render_columns` `views.py:388` | Classic kanban BACKLOG / ACTIVE / BLOCKED / DONE, project-colored cards, WIP counts + throughput sparklines. |
| `3` | **Agenda** | `render_agenda` `views.py:508` | Tasks grouped by urgency bucket: OVERDUE / TODAY / THIS WEEK / LATER / NO DATE. |
| `4` | **Gantt** | `render_gantt` `views.py:567` | An 8-week time axis with a bar per project (start→due) and its task bars; undated items under UNSCHEDULED. |

`render_view` (`views.py:673`) dispatches to the active renderer; every line is padded to the exact viewport width so the box-art stays aligned and the four views reflow when the window resizes (`BoardView.on_resize` → `refresh_view`, `app.py:32-33,168`).

### The data model

- **`Project`** (`models.py:159-179`): `name`, `color`, `status` (`on_track` / `paused` / `cancelled` / `completed`), `archived`, `start_date`, `due_date`, `id`.
- **`Task`** (`models.py:182-217`): `title`, `project_id` (`None` → shown in the "Inbox" group), `status` (`backlog` / `active` / `blocked` / `done`), `priority` (`low` / `normal` / `high`), `start_date`, `due_date`, **`urls: list[str]`**, **`images: list[str]`**, `archived`, `id`.
- **`Board`** (`models.py:220-319`): owns `projects` + `tasks`, round-trips them through `asdict` / `from_dict`, and also stores two ribbon-clock cities in `settings`.

All model parsing is **lenient and never raises on load** (`from_dict`, `parse_iso` — Constraint C-4): unknown enum values fall back to the default, malformed list fields degrade to `[]`.

---

## The three NEW capabilities this batch

### 1. Author-neutral, dimension-complete demo seed (US-001 · HLR-001)

`seed_data()` (`models.py:322-376`) was fully rewritten to a generic software-product org — *Website Redesign, Mobile App, API Platform, Legacy Sunset, Data Warehouse, Internal Wiki*. It **reveals nothing about the author** (0 matches against a 16-token author denylist, scanned over the actual on-disk `board.json`) while still exercising **every** board dimension: all 4 project statuses (including the previously-missing `cancelled`), all 4 task statuses, all 3 priorities, every urgency bucket, ≥1 archived project + ≥1 archived task, standalone + project tasks, a ≥2-URL task, and image tasks — so the demo self-demonstrates the whole tool, including this batch's own two new fields.

> Design note (`increment-003.md`): image-bearing seed tasks are deliberately kept `normal`/`low` priority with no URL, so a card carries **only** the `▤` glyph — never `▤` alongside `◉`/`↗`. This preserves the existing indicator-overlap invariant without weakening it.

### 2. Multiple URLs per task (US-002 · HLR-002/003/004)

- **Model:** `Task.url: str` was replaced by the canonical `Task.urls: list[str]` (`models.py:190`). `from_dict` (`models.py:199-204`) **migrates** a legacy single `url` string into a one-element list (one-way, DD-2), reads a modern `urls` list, and degrades malformed input to `[]`.
- **Modal:** a `TextArea` (`#f-urls`, `modals.py:67-69`) accepts **one URL per line**, pre-filled from the task. On save each line is stripped and filtered through `valid_url` (`views.py:106-114`), keeping only valid `http(s)` URLs in order (`modals.py:100,108`). `valid_url` also rejects `[`, `]`, whitespace and newlines — the OSC-8 link-injection guard (C-3).
- **Card + action:** a card shows `↗` when `any(valid_url(u))` (`views.py:163-164`); the title renders as an OSC-8 hyperlink to the first valid URL (`views.py:122-127`). Pressing **`o`** opens **every** valid URL via `webbrowser.open` (`action_open_url`, `app.py:259-266`).

### 3. Image references per task, with safe open-in-viewer (US-003 · HLR-005/006/007)

- **Model:** new `Task.images: list[str]` (`models.py:191`); read leniently (`models.py:205`), persisted via `asdict`.
- **Modal:** a second `TextArea` (`#f-images`, `modals.py:71-74`) accepts image refs one-per-line — local paths **or** `http(s)` image URLs. Every non-blank line is kept in order; **no `http` filter at entry** (local paths are valid — the extension allowlist is applied only at open time).
- **Card:** a width-1 `▤` glyph (sky) when the task has ≥1 image (`views.py:167-168`), visually distinct from `↗` and `◉` (Constraint C-2: single-cell glyphs only).
- **Open action (`i` → `action_open_images`, `app.py:268-277`):** for each ref, a valid `http(s)` URL opens in the browser; otherwise it is treated as a local file and passed to `_open_local_image` (`app.py:279-296`), which is **security-gated** (see below).

#### Why the image-open path is guarded (security)

`os.startfile(path)` launches a path with its **OS-associated handler** — a non-image file (e.g. `.exe`) would *execute* (Constraint C-6). `_open_local_image` therefore opens a local ref **only** when all of these hold (`app.py:285-296`):

| Guard | Rule |
|-------|------|
| No UNC path | refuse `\\host\share\…` and `//…` prefixes |
| No `file://` URL | refuse `file://` refs |
| Extension allowlist | `Path(ref).suffix.lower()` ∈ `{.png,.jpg,.jpeg,.gif,.webp,.bmp}` — **`.svg` excluded** (scriptable) |
| Existing regular file | `os.path.isfile(ref)` is true |
| Crash-safe | wrapped in `try/except OSError` so a keypress never crashes the app |

`os.startfile` is Windows-only (DD-4); `http(s)` image refs work cross-platform via `webbrowser`. **Inline in-terminal image preview is intentionally NOT built** — it needs a terminal graphics protocol (Kitty/iTerm/Sixel) that cannot be verified headlessly (C-5), so the batch degrades to open-in-viewer (the non-binding stretch LLR-007.4).

---

## Keybindings (full)

| Key | Action | Handler |
|-----|--------|---------|
| `1` `2` `3` `4` | Switch view (Swimlanes / Columns / Agenda / Gantt) | `action_view` `app.py:201` |
| `↑`/`k` `↓`/`j` | Move selection within the current column/lane | `action_cursor` `app.py:136` |
| `←`/`h` `→`/`l` | Jump to the nearest non-empty column's first task | `action_hmove` `app.py:150` |
| `a` | Add task | `action_add_task` `app.py:207` |
| `p` | Add project | `action_add_project` `app.py:299` |
| `e` | Edit selected task | `action_edit` `app.py:218` |
| `d` / `Delete` | Delete selected task (confirm modal) | `action_delete` `app.py:233` |
| `x` | Archive / unarchive selected task | `action_archive` `app.py:247` |
| `v` | Toggle showing archived items | `action_toggle_archived` `app.py:255` |
| **`o`** | **Open every valid URL of the selected task** | `action_open_url` `app.py:259` |
| **`i`** | **Open every image ref of the selected task (browser / viewer)** | `action_open_images` `app.py:268` |
| `c` | Choose the two ribbon city clocks (type to find a city) | `action_clocks` `app.py:101` |
| `q` | Quit | built-in |

> The `i` binding is **new this batch**. The public README keybindings table (`README.md:129-142`) does not yet list it — a suggested doc follow-up. <!-- TBD: add `i` (Open image) to README keybindings table -->

Inside a modal: `Esc` cancels, `Tab` moves between fields, `Enter` on a button activates it.

---

## Install

`taskboard` is a packaged console app (`pyproject.toml` `[project.scripts] taskboard = "taskboard.__main__:main"`). Both `python -m taskboard` and the installed `taskboard` command launch the same app; `--board PATH` overrides the JSON store location.

```powershell
# Recommended: pipx — isolated env, global `taskboard` command
python -m pip install --user pipx
python -m pipx ensurepath          # then reopen the terminal so PATH updates
pipx install "C:\Users\<you>\...\taskboard"
taskboard

# Editable / development install (pip)
cd "C:\Users\<you>\...\taskboard"
pip install -e .
taskboard

# Run from source (venv)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m taskboard
```

Data lives at `C:\Users\<you>\.taskboard\board.json` — outside the (read-only) installed package. Created + seeded on first run.

### Frameless WezTerm setup

Textual **cannot remove the OS window chrome** — that is the terminal's job, and Windows Terminal / PowerShell cannot go borderless. The repo ships a ready-made **WezTerm** config (`wezterm.lua`) that sets `window_decorations = "NONE"`, hides the tab bar, uses `window_background_opacity = 0.9`, and sizes the window to 96×30.

1. Install WezTerm (<https://wezterm.org>).
2. Copy `wezterm.lua` to `C:\Users\<you>\.wezterm.lua`, **or** launch with `wezterm --config-file "…\taskboard\wezterm.lua"`.
3. Pin the window **always-on-top** with PowerToys → *Always On Top* (`Win+Ctrl+T`).

Runtime frame toggles (WezTerm bindings, not app buttons): `Ctrl+Shift+B` flips the frame on/off, `F11` toggles borderless fullscreen (`wezterm.lua:47-64`).

---

## Detail (reference)

### How it works (flow)

The modal is the only write path for task fields. `TaskModal._save` (`modals.py:97-111`) builds a `data` dict whose keys **must** match `Task` field names (contract), which `_on_task_added` / `_on_task_edited` (`app.py:210-231`) apply via `Task(**data)` / `setattr` and then `Board.save()`. Reads flow the other way: `Board` → `render_view` → the `card_cell`/`title_markup` indicators (`↗`, `◉`, `▤`). The open actions (`o`, `i`) read the selected task's `urls`/`images` and route to `webbrowser.open` / `os.startfile`.

### Components / modules touched this batch

| Module | Role in this batch |
|--------|--------------------|
| `taskboard/models.py` | `Task.urls`/`Task.images` fields + lenient/legacy `from_dict`; full `seed_data()` rewrite |
| `taskboard/modals.py` | `#f-urls` and `#f-images` `TextArea` inputs + `valid_url` filtering on save |
| `taskboard/views.py` | `has_url`/`first_valid_url` helpers; `↗` gate over `urls`; `▤` image glyph in `card_cell` |
| `taskboard/app.py` | `action_open_url` opens all URLs; new `i` binding + `action_open_images` + `_open_local_image` allowlist; `IMAGE_EXTS` |

### Diagrams

- Architecture: [`diagrams/architecture.md`](diagrams/architecture.md)
- Data model: [`diagrams/data-model.md`](diagrams/data-model.md)
- Open-image sequence: [`diagrams/sequence-open-image.md`](diagrams/sequence-open-image.md)

### Evidence checklist — docs-writer

- [✓] Audience + purpose declared at top (technical stakeholder; functional description of the batch).
- [✓] Structure follows the scaffold (at-a-glance → detail) with the required sections (views, model, 3 new capabilities, keybindings, install, frameless setup).
- [✓] Code/CLI snippets run — install commands mirror the verified `README.md`; `36 passed` suite backs the behavior described.
- [✓] Assumptions listed — lenient model (C-4), single-user trust boundary (A-1), Windows-only `os.startfile` (DD-4).
- [✓] Risks / limitations called out — `os.startfile` execution risk + allowlist (C-6); inline preview not built (C-5); README `i` binding gap flagged `<!-- TBD -->`.
- [✓] Next steps stated — README keybindings `i` row (TBD); optional edit-path prefill TC (G-001).
- [✓] Diagrams included — architecture, data model, open-image sequence (links above).
- [✓] No invented APIs / versions / metrics — every symbol cited `file:line`; versions from `requirements.txt`; `36 passed` from `04-validation.md`.
