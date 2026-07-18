# Architecture — taskboard

How the pieces fit at runtime. The `TaskboardApp` owns selection + view state, renders the active view into `BoardView`, opens modals for writes, and delegates persistence to `Board`. The two open actions (`o`/`i`) reach out to the OS openers. ≤12 nodes.

```mermaid
flowchart TD
    App["TaskboardApp<br/>(app.py) — bindings, selection,<br/>o/i open actions"]
    Board["BoardView (Static)<br/>active-view surface"]
    Views["views.render_view<br/>swimlanes / columns / agenda / gantt<br/>+ card_cell indicators ↗ ◉ ▤"]
    Ribbon["Ribbon (ribbon.py)<br/>time · date · week · 2 city clocks"]
    Modals["Modals (modals.py)<br/>Task / Project / Clock / Confirm"]
    Model["Board (models.py)<br/>owns projects + tasks"]
    Data["Project / Task<br/>dataclasses (urls[], images[])"]
    JSON[("~/.taskboard/board.json")]
    Browser["webbrowser.open<br/>(http/https URLs + image URLs)"]
    OS["os.startfile<br/>(allowlisted local image files)"]

    App -->|refresh_view| Board
    Board -->|render| Views
    App --> Ribbon
    App -->|push_screen| Modals
    Modals -->|data dict on save| App
    App -->|load / save / mutate| Model
    Views -->|read| Model
    Model --> Data
    Model <-->|from_dict / asdict| JSON
    App -->|action_open_url| Browser
    App -->|action_open_images| Browser
    App -->|action_open_images → _open_local_image| OS
```

**Notes**
- The **modal is the only write path** for task/project fields; it returns a `data` dict whose keys match `Task`/`Project` field names, applied by `_on_task_added` / `_on_task_edited` (`app.py:210-231`).
- `Board` is the single source of truth read by both the renderers (for `↗`/`◉`/`▤` indicators) and the open actions.
- `os.startfile` is reached only through `_open_local_image`'s security allowlist (`app.py:279-296`) — see the open-image sequence diagram.
