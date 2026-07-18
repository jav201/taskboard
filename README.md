# taskboard

A **frameless kanban desktop-widget task board** built in [Textual](https://textual.textualize.io/).
Run it in a borderless terminal, pin it always-on-top, and it floats on your desktop as a live
widget. Four switchable views over the same data; single dark theme tuned for a terminal.

Built and verified against **Textual 8.2.8 / rich 15.0.0** (Python 3.12).

```
╭─ ◆ TASKBOARD ──────────────────────────────── 12 open · 4 due ─╮
│          │TODO             │DOING            │DONE             │
├──────────┼─────────────────┼─────────────────┼─────────────────┤
│▐ Textual │dev-flow doc     │M22 pitfalls m… ◉│systems 5/5      │
│▐ ▇▇▇░░░░░│                 │1 more           │1 more           │
╰──────────┴─────────────────┴─────────────────┴─────────────────╯
```

## Views

| Key | View | What it's for |
|-----|------|---------------|
| `1` | **Swimlanes** | Projects as rows × TODO/DOING/DONE columns, with a half-block progress bar per project. |
| `2` | **Columns** | Classic kanban: BACKLOG / ACTIVE / BLOCKED / DONE, project-colored cards, WIP counts + throughput sparklines, due chips. |
| `3` | **Agenda** | Tasks grouped by urgency: OVERDUE / TODAY / THIS WEEK / LATER / NO DATE, with braille due-bars. |
| `4` | **Gantt** | An 8-week time axis; a bar per project (start→due) with its task bars underneath; undated items listed under UNSCHEDULED. |

## Install as a command

You have never packaged a CLI before, so here is the simplest correct path first.

### Recommended: pipx (isolated, gives you a global `taskboard` command)

`pipx` installs the app into its own isolated environment and puts the `taskboard` command on your PATH — it won't collide with anything else.

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
# >>> close and REOPEN your terminal here so PATH updates <<<
pipx install "C:\Users\jjgh8\OneDrive\Documents\Github\taskboard"
```

Now, from any terminal:

```powershell
taskboard
```

To **update** after you edit the code:

```powershell
pipx reinstall taskboard
```

### Alternative: pip (user install)

```powershell
cd "C:\Users\jjgh8\OneDrive\Documents\Github\taskboard"
pip install --user .
taskboard
```

If `taskboard` is "not recognized", your Python **user scripts** dir isn't on PATH. Find it and add it:

```powershell
python -c "import site,os; print(os.path.join(site.getuserbase(), 'Scripts'))"
# add that folder to your PATH (System Settings → Environment Variables), reopen terminal
```

To update after edits: `pip install --user . --force-reinstall`.

### Run from source (development)

```powershell
cd "C:\Users\jjgh8\OneDrive\Documents\Github\taskboard"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m taskboard
```

Both `python -m taskboard` and the installed `taskboard` command launch the same app.

## Where your data lives

Tasks are stored as JSON at:

```
C:\Users\<you>\.taskboard\board.json
```

It is **not** inside the installed package (the package dir is read-only once pip/pipx-installed).
The file is created and seeded with demo data on first run. If it ever gets corrupted, the app
starts empty and leaves the file untouched so you can recover it by hand.

## Make it frameless

**Textual cannot remove the window chrome itself** — that's the terminal's job, and
**Windows Terminal / PowerShell cannot go borderless** (they always draw a title bar). Use
**WezTerm** (or Alacritty), which can.

A ready-made config ships in this repo: [`wezterm.lua`](wezterm.lua). It sets
`window_decorations = "NONE"`, turns the tab bar off, uses `window_background_opacity = 0.9`, sizes
the window, and launches `taskboard` via `default_prog`.

1. Install WezTerm: <https://wezterm.org>
2. Use the config — either copy it to your home dir as `C:\Users\<you>\.wezterm.lua`, or point
   WezTerm at it: `wezterm --config-file "…\taskboard\wezterm.lua"`.
3. Pin the window **always-on-top** with [PowerToys](https://learn.microsoft.com/windows/powertoys/)
   → *Always On Top* (default shortcut `Win+Ctrl+T`).

The frame is gone and the board **fills the window** — resize it and the four views reflow to the
new size. Textual paints the rest.

### Toggle the window border at runtime

The bundled `wezterm.lua` binds two keys (a WezTerm feature — an in-app button *cannot* remove the
OS frame):

| Key | Action |
|-----|--------|
| `Ctrl+Shift+B` | Flip the window frame on/off (`NONE` ↔ `TITLE \| RESIZE`) |
| `F11` | Toggle borderless fullscreen |

So you can start frameless, tap `Ctrl+Shift+B` to get the title bar back when you need to drag the
window, then tap it again to go frameless.

## Keybindings

| Key | Action |
|-----|--------|
| `1` `2` `3` `4` | Switch view (Swimlanes / Columns / Agenda / Gantt) |
| `↑` `↓` (or `k` `j`) | Move selection **in the current view's on-screen order**. In Columns/Swimlanes this moves *within* the column/lane. |
| `←` `→` (or `h` `l`) | Move between columns (Columns/Swimlanes) — jumps to the next column's first task. No-op in Agenda/Gantt (single column). |
| `a` | Add task |
| `p` | Add project |
| `e` | Edit selected task |
| `d` / `Delete` | Delete selected task (asks to confirm) |
| `x` | Archive / unarchive selected task |
| `v` | Toggle showing archived items (hidden by default) |
| `o` | Open the selected task's URL in your browser |
| `c` | Choose the two ribbon clocks |
| `q` | Quit |

Navigation follows what you **see**: Down in Columns walks down the current status
column (not some unrelated task in data order); Right jumps to the next column. The
selected task stays highlighted and is scrolled into view.

Inside a modal: `Esc` cancels, `Tab` moves between fields, `Enter` on a button activates it.

Tasks with a URL show a small `↗` and render their title as an OSC-8 hyperlink (clickable in
terminals that support it, e.g. WezTerm). The `o` key always works regardless of terminal.

## The two custom clocks

The bottom ribbon shows local time, date, ISO week (e.g. `W29`), and **two custom clocks**.
Choose them **in-app**: press `c` to open the clock menu, pick a zone for Clock 1 and Clock 2,
and Save. The selection is saved to `board.json` and survives restarts. Defaults are
**CST (UTC-6)** and **EST (UTC-5)**.

The clocks use **fixed UTC offsets** (no daylight-saving shifts) — that's the "UTC convention".
Available zones:

```
UTC (UTC+0)
HST (UTC-10)  AKST (UTC-9)  PST (UTC-8)  MST (UTC-7)  CST (UTC-6)  EST (UTC-5)  AST (UTC-4)  BRT (UTC-3)
GMT (UTC+0)   CET (UTC+1)   EET (UTC+2)  MSK (UTC+3)  GST (UTC+4)  IST (UTC+5:30)  ICT (UTC+7)
HKT (UTC+8)   JST (UTC+9)   AEST (UTC+10)  NZST (UTC+12)
```

Because the offsets are fixed, no `zoneinfo`/`tzdata` timezone database is needed. Local time
(the first field) still follows your system clock.

## Development

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest            # 25 Pilot + render tests
```

## Project layout

```
taskboard/
  taskboard/
    __init__.py        package + version
    __main__.py        entry point: main() -> TaskboardApp().run()
    app.py             the App: view switching, selection, modals, one clock interval
    models.py          Project / Task dataclasses + Board (JSON persistence, seed)
    views.py           the four view renderers (rich markup, escaped user text)
    modals.py          add/edit task, add/edit project, confirm-delete modals
    ribbon.py          bottom status bar (time/date/week + two custom clocks)
    taskboard.tcss     palette + layout (single dark theme)
  tests/
    test_app.py        Pilot tests + pure-render tests
  pyproject.toml       packaging + console entry point (`taskboard`)
  requirements.txt     pinned deps
  README.md
```
