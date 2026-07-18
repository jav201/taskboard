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
from textual.widgets import Button, Input, Label, Select

from .models import (PROJECT_COLORS, PROJECT_STATUSES, TASK_PRIORITIES,
                     TASK_STATUSES, Board, Project, Task)

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
                yield Label("URL")
                yield Input(value=(t.url or "" if t else ""), placeholder="https://…",
                            id="f-url")
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

    def _save(self) -> None:
        title = self._val("f-title") or "Untitled"
        proj = self._val("f-project")
        data = {
            "title": title,
            "project_id": None if proj == NONE_VALUE else proj,
            "status": self._val("f-status"),
            "priority": self._val("f-priority"),
            "start_date": self._val("f-start") or None,
            "due_date": self._val("f-due") or None,
            "url": self._val("f-url") or None,
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
