"""Add/edit modals for tasks and projects.

Notes on the pitfalls these avoid:
- Select option labels are markup sinks too -> project names are escaped (A1).
- ``Select.BLANK`` is a plain bool in textual 8.2.8, not a unique sentinel
  (A7). We never rely on it: ``allow_blank=False`` + an explicit "(none)"
  option whose value we map to ``None`` ourselves.
- Options are fixed at compose time, so ``set_options`` (which fires
  ``Changed``) is never called and needs no guard here.
"""

from __future__ import annotations

import os
from pathlib import Path

from rich.markup import escape

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.suggester import SuggestFromList
from textual.widgets import Button, Input, Label, OptionList, Select, TextArea
from textual.widgets.option_list import Option

from .models import (IMAGE_EXTS, PROJECT_COLORS, PROJECT_STATUSES, TASK_PRIORITIES,
                     TASK_STATUSES, Board, Project, Task, _new_id, city_names,
                     grab_clipboard_image, resolve_city, save_pil_image)
from .views import valid_url

# Imported at MODULE load (before the app starts) on purpose: textual-image
# detects the terminal's graphics support by QUERYING the terminal, which only
# works before Textual seizes it. A lazy import inside the viewer would run
# after app start -> detection fails -> silent low-res half-cell fallback.
try:
    from textual_image.widget import Image as AutoImage
except Exception:          # pragma: no cover - dependency present in prod
    AutoImage = None

NONE_VALUE = "__none__"


class TaskModal(ModalScreen[dict | None]):
    """Returns a dict of task fields on save, or None on cancel."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, board: Board, task: Task | None = None):
        super().__init__()
        self.board = board
        self._edit_task = task
        # stable folder key for pasted images; a NEW task adopts it as its id on
        # save, so images live at images/<task-id>/.
        self._img_key = task.id if task else _new_id()

    def compose(self) -> ComposeResult:
        t = self._edit_task
        proj_options = [("(none · Inbox)", NONE_VALUE)] + [
            (escape(p.name), p.id) for p in self.board.projects
        ]
        proj_value = t.project_id if (t and t.project_id) else NONE_VALUE
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label("[b]Edit task[/b]" if t else "[b]New task[/b]", classes="modal-title")
            yield Label("Title")
            yield Input(value=(t.title if t else ""), placeholder="what needs doing",
                        id="f-title")
            with Grid(classes="modal-grid"):
                yield Label("Project")
                yield Select(proj_options, value=proj_value, allow_blank=False, id="f-project")
                yield Label("Status")
                yield Select([(s, s) for s in TASK_STATUSES],
                             value=(t.status if t else "backlog"),
                             allow_blank=False, id="f-status")
                yield Label("Priority")
                yield Select([(p, p) for p in TASK_PRIORITIES],
                             value=(t.priority if t else "normal"),
                             allow_blank=False, id="f-priority")
                yield Label("Start (YYYY-MM-DD)")
                yield Input(value=(t.start_date or "" if t else ""), placeholder="optional",
                            id="f-start")
                yield Label("Due (YYYY-MM-DD)")
                yield Input(value=(t.due_date or "" if t else ""), placeholder="optional",
                            id="f-due")
            yield Label("URLs (one per line)")
            urls_area = TextArea("\n".join(t.urls) if t else "", id="f-urls")
            urls_area.styles.height = 4   # 1fr TextArea would collapse in the auto modal
            yield urls_area
            yield Label("Images (path or URL, one per line)")
            images_area = TextArea("\n".join(t.images) if t else "", id="f-images")
            images_area.styles.height = 4
            yield images_area
            yield Button("Paste image from clipboard", variant="primary",
                         id="paste-img")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self._save()
        elif event.button.id == "paste-img":
            self._paste_image()
        else:
            self.dismiss(None)

    def _paste_image(self) -> None:
        """Grab an image (or image files) from the clipboard, persist a pasted
        bitmap under the task's image folder, and append the path(s) to the
        images field. Friendly notice when the clipboard has no usable image."""
        grabbed = grab_clipboard_image()
        if grabbed is None:
            self.notify("No image found in the clipboard.", severity="warning")
            return
        added: list[str] = []
        if isinstance(grabbed, list):                    # files copied in Explorer
            for p in grabbed:
                if Path(p).suffix.lower() in IMAGE_EXTS and os.path.isfile(p):
                    added.append(p)
            if not added:
                self.notify("Clipboard holds no image files.", severity="warning")
                return
        else:                                            # a raw bitmap
            dest = save_pil_image(self.board.image_dir(self._img_key), grabbed)
            added.append(str(dest))
        area = self.query_one("#f-images", TextArea)
        existing = area.text.rstrip("\n")
        area.text = (existing + "\n" if existing else "") + "\n".join(added)
        self.notify(f"Added {len(added)} image{'' if len(added) == 1 else 's'}.")

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _val(self, wid: str) -> str:
        node = self.query_one(f"#{wid}")
        return str(node.value).strip()

    def _lines(self, wid: str) -> list[str]:
        """Non-blank, stripped lines from a multi-line TextArea, in order."""
        text = self.query_one(f"#{wid}", TextArea).text
        return [ln.strip() for ln in text.splitlines() if ln.strip()]

    def _save(self) -> None:
        title = self._val("f-title") or "Untitled"
        proj = self._val("f-project")
        urls = [v for v in (valid_url(ln) for ln in self._lines("f-urls")) if v]
        data = {
            "id": self._img_key,
            "title": title,
            "project_id": None if proj == NONE_VALUE else proj,
            "status": self._val("f-status"),
            "priority": self._val("f-priority"),
            "start_date": self._val("f-start") or None,
            "due_date": self._val("f-due") or None,
            "urls": urls,
            "images": self._lines("f-images"),   # local paths valid at entry (no filter)
        }
        self.dismiss(data)


class ProjectModal(ModalScreen[dict | None]):
    """Returns a dict of project fields on save, or None on cancel."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, project: Project | None = None):
        super().__init__()
        self.project = project

    def compose(self) -> ComposeResult:
        p = self.project
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label("[b]Edit project[/b]" if p else "[b]New project[/b]",
                        classes="modal-title")
            yield Label("Name")
            yield Input(value=(p.name if p else ""), placeholder="project name", id="f-name")
            with Grid(classes="modal-grid"):
                yield Label("Color")
                yield Select([(col, col) for col in PROJECT_COLORS],
                             value=(p.color if p else "violet"),
                             allow_blank=False, id="f-color")
                yield Label("Status")
                yield Select([(s, s) for s in PROJECT_STATUSES],
                             value=(p.status if p else "on_track"),
                             allow_blank=False, id="f-status")
                yield Label("Start (YYYY-MM-DD)")
                yield Input(value=(p.start_date or "" if p else ""), placeholder="optional",
                            id="f-start")
                yield Label("Due (YYYY-MM-DD)")
                yield Input(value=(p.due_date or "" if p else ""), placeholder="optional",
                            id="f-due")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self._save()
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _val(self, wid: str) -> str:
        return str(self.query_one(f"#{wid}").value).strip()

    def _save(self) -> None:
        data = {
            "name": self._val("f-name") or "Untitled",
            "color": self._val("f-color"),
            "status": self._val("f-status"),
            "start_date": self._val("f-start") or None,
            "due_date": self._val("f-due") or None,
        }
        self.dismiss(data)


class ProjectPicker(ModalScreen[None]):
    """Manage existing projects: edit / archive / delete, in place.

    Mutations persist immediately (Board.save) and re-render the board behind
    the modal, so the picker stays open for the next action. Option labels are
    markup sinks -> project names are escaped (A1). Deleting a project reassigns
    its tasks to no-project (Inbox), the least-destructive choice — no task is
    ever lost to a project delete.
    """

    BINDINGS = [
        ("escape", "close", "Close"),
        ("e", "edit", "Edit"),
        ("x", "archive", "Archive"),
        ("d", "delete", "Delete"),
        Binding("j", "move(1)", show=False),
        Binding("k", "move(-1)", show=False),
    ]

    def __init__(self, board: Board):
        super().__init__()
        self.board = board

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="picker-box", classes="modal"):
            yield Label("[b]Projects[/b]  —  e edit · x archive · d delete · esc close",
                        classes="modal-title")
            yield OptionList(id="proj-list")

    def on_mount(self) -> None:
        self._reload()
        self.query_one("#proj-list", OptionList).focus()

    # ---- list rendering ----------------------------------------------------
    def _project_line(self, p: Project) -> str:
        n = sum(1 for t in self.board.tasks if t.project_id == p.id)
        parts = [f"[b]{escape(p.name)}[/b]", p.status]
        if p.archived:
            parts.append("[dim]archived[/dim]")
        parts.append(f"{n} task{'s' if n != 1 else ''}")
        return "  ·  ".join(parts)

    def _reload(self, keep: str | None = None) -> None:
        """Rebuild the list from the board (clear-before-add avoids DuplicateIds)."""
        ol = self.query_one("#proj-list", OptionList)
        ol.clear_options()
        projects = self.board.projects
        if not projects:
            ol.add_option(Option("No projects yet — press esc, then p to add one.",
                                 disabled=True))
            return
        for p in projects:
            ol.add_option(Option(self._project_line(p), id=p.id))
        if keep is not None:
            for i, p in enumerate(projects):
                if p.id == keep:
                    ol.highlighted = i
                    break

    def _current(self) -> Project | None:
        ol = self.query_one("#proj-list", OptionList)
        idx = ol.highlighted
        if idx is None:
            return None
        return self.board.project_by_id(ol.get_option_at_index(idx).id)

    # ---- navigation / actions ---------------------------------------------
    def action_move(self, delta: int) -> None:
        projects = self.board.projects
        if not projects:
            return
        ol = self.query_one("#proj-list", OptionList)
        cur = ol.highlighted if ol.highlighted is not None else 0
        ol.highlighted = max(0, min(len(projects) - 1, cur + delta))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.action_edit()   # Enter / click on a row opens the editor

    def action_edit(self) -> None:
        proj = self._current()
        if proj is None:
            return
        self.app.push_screen(ProjectModal(proj),
                             lambda data, p=proj: self._on_edited(p, data))

    def _on_edited(self, proj: Project, data: dict | None) -> None:
        if not data:
            return
        for k, v in data.items():
            setattr(proj, k, v)
        self.board.save()
        self.app.refresh_view()
        self._reload(keep=proj.id)

    def action_archive(self) -> None:
        proj = self._current()
        if proj is None:
            return
        proj.archived = not proj.archived
        self.board.save()
        self.app.refresh_view()
        self._reload(keep=proj.id)

    def action_delete(self) -> None:
        proj = self._current()
        if proj is None:
            return
        n = sum(1 for t in self.board.tasks if t.project_id == proj.id)
        msg = f"Delete '{proj.name}'? Its {n} task{'s' if n != 1 else ''} move to Inbox."
        self.app.push_screen(ConfirmModal(msg),
                             lambda ok, p=proj: self._on_delete(p, ok))

    def _on_delete(self, proj: Project, ok: bool) -> None:
        if not ok:
            return
        self.board.delete_project(proj.id)   # tasks -> Inbox (project_id=None)
        self.app.refresh_view()
        self._reload()

    def action_close(self) -> None:
        self.dismiss(None)


class ClockModal(ModalScreen[dict | None]):
    """Pick the two ribbon clocks by CITY (type to find one). Returns city names."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, clock1: str, clock2: str):
        super().__init__()
        self._clock1 = clock1
        self._clock2 = clock2

    def compose(self) -> ComposeResult:
        # inline autocomplete: type "mad" -> suggests "Madrid" (accept with →/Enter)
        suggester = SuggestFromList(city_names(), case_sensitive=False)
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label("[b]Ribbon clocks[/b] — type a city", classes="modal-title")
            with Grid(classes="modal-grid"):
                yield Label("Clock 1")
                yield Input(value=self._clock1, suggester=suggester,
                            placeholder="find a city…", id="f-clock1")
                yield Label("Clock 2")
                yield Input(value=self._clock2, suggester=suggester,
                            placeholder="find a city…", id="f-clock2")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            # unknown / blank entry -> keep the current value (guarded)
            c1 = resolve_city(str(self.query_one("#f-clock1").value)) or self._clock1
            c2 = resolve_city(str(self.query_one("#f-clock2").value)) or self._clock2
            self.dismiss({"clock1": c1, "clock2": c2})
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)


class ConfirmModal(ModalScreen[bool]):
    """Small yes/no confirm."""

    BINDINGS = [("escape", "no", "No")]

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="confirm-box", classes="modal"):
            yield Label(escape(self.message), classes="modal-title")
            with Horizontal(classes="modal-buttons"):
                yield Button("Delete", variant="error", id="yes")
                yield Button("Cancel", variant="default", id="no")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")

    def action_no(self) -> None:
        self.dismiss(False)


class ImageViewer(ModalScreen[None]):
    """Show a task's images rescaled inline — crisp via the terminal graphics
    protocol where the terminal supports it (e.g. WezTerm), half-block/Unicode
    fallback otherwise. ``o`` opens every image raw in its OS-default app /
    browser; ``esc`` closes. Remote URLs are listed as links (``o`` opens them).
    """

    BINDINGS = [("escape", "close", "Close"), ("o", "open_raw", "Open raw")]

    def __init__(self, task: Task, board: Board):
        super().__init__()
        self._view_task = task
        self._board = board

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="viewer-box", classes="modal"):
            yield Label(
                f"[b]{escape(self._view_task.title)}[/b]  —  o open raw · esc close",
                classes="modal-title")
            if not self._view_task.images:
                yield Label("[dim]No images on this task.[/dim]")
                return
            for ref in self._view_task.images:
                yield from self._image_block(ref)

    def _image_block(self, ref: str):
        if valid_url(ref):                       # remote: can't inline; link it
            yield Label(f"link · {escape(ref)}")
            return
        path = Path(ref)
        if path.suffix.lower() not in IMAGE_EXTS or not path.is_file():
            yield Label(f"[dim]missing:[/dim] {escape(ref)}")
            return
        if AutoImage is None:
            yield Label(f"[dim](install textual-image to preview)[/dim] {escape(ref)}")
            return
        try:
            img = AutoImage(str(path))           # size comes from #viewer-box Image (TCSS)
        except Exception:                        # never blank the modal on one bad file
            yield Label(f"[dim]could not render:[/dim] {escape(ref)}")
            return
        yield img
        yield Label(f"[dim]{escape(path.name)}[/dim]")

    def action_open_raw(self) -> None:
        self.app.open_all_images_raw(self._view_task)

    def action_close(self) -> None:
        self.dismiss(None)
