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

from rich.markup import escape

from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.suggester import SuggestFromList
from textual.widgets import Button, Input, Label, Select, TextArea

from .models import (PROJECT_COLORS, PROJECT_STATUSES, TASK_PRIORITIES,
                     TASK_STATUSES, Board, Project, Task, city_names, resolve_city)
from .views import valid_url

NONE_VALUE = "__none__"


class TaskModal(ModalScreen[dict | None]):
    """Returns a dict of task fields on save, or None on cancel."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, board: Board, task: Task | None = None):
        super().__init__()
        self.board = board
        self._edit_task = task

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
