"""The Textual application: view switching, selection, modals, one clock."""

from __future__ import annotations

import webbrowser
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Static

from .models import Board, Project, Task, default_board_path
from .modals import ClockModal, ConfirmModal, ProjectModal, TaskModal
from .ribbon import Ribbon
from .views import render_view, valid_url

VIEW_ORDER = ["swimlanes", "columns", "agenda", "gantt"]
VIEW_KEYS = {"1": "swimlanes", "2": "columns", "3": "agenda", "4": "gantt"}


class TaskboardApp(App):
    """Frameless kanban desktop widget."""

    CSS_PATH = "taskboard.tcss"
    TITLE = "taskboard"

    BINDINGS = [
        ("1", "view('swimlanes')", "Lanes"),
        ("2", "view('columns')", "Cols"),
        ("3", "view('agenda')", "Agenda"),
        ("4", "view('gantt')", "Gantt"),
        ("a", "add_task", "Add"),
        ("p", "add_project", "Project"),
        ("e", "edit", "Edit"),
        ("d", "delete", "Del"),
        ("delete", "delete", "Del"),
        ("x", "archive", "Archive"),
        ("h", "toggle_archived", "Show arch"),
        ("o", "open_url", "Open URL"),
        ("c", "clocks", "Clocks"),
        ("down,j", "cursor(1)", "Down"),
        ("up,k", "cursor(-1)", "Up"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, board_path: str | Path | None = None):
        super().__init__()
        self.board = Board.load(board_path or default_board_path())
        self.view_mode = "swimlanes"
        self.show_archived = False
        self.selected_task_id: str | None = None

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="viewport"):
            yield Static(id="board")
        yield Ribbon(id="ribbon")
        yield Footer()

    def on_mount(self) -> None:
        self._select_first()
        self.refresh_view()
        self._apply_clock_settings()
        # ONE shared clock interval for the whole app (never per-widget).
        self.set_interval(1.0, self._tick)

    # ---- clock -------------------------------------------------------------
    def _tick(self) -> None:
        ribbons = self.query("#ribbon")
        if ribbons:
            ribbons.first(Ribbon).update_clock()

    def _apply_clock_settings(self) -> None:
        ribbons = self.query("#ribbon")
        if not ribbons:
            return
        ribbon = ribbons.first(Ribbon)
        ribbon.clock1_key, ribbon.clock2_key = self.board.get_clocks()
        ribbon.update_clock()

    def action_clocks(self) -> None:
        k1, k2 = self.board.get_clocks()
        self.push_screen(ClockModal(k1, k2), self._on_clocks_saved)

    def _on_clocks_saved(self, data: dict | None) -> None:
        if not data:
            return
        self.board.set_clocks(data["clock1"], data["clock2"])
        self._apply_clock_settings()

    # ---- selection ---------------------------------------------------------
    def _visible_task_ids(self) -> list[str]:
        return [t.id for t in self.board.visible_tasks(self.show_archived)]

    def _select_first(self) -> None:
        ids = self._visible_task_ids()
        if self.selected_task_id not in ids:
            self.selected_task_id = ids[0] if ids else None

    @property
    def selected_task(self) -> Task | None:
        return self.board.task_by_id(self.selected_task_id)

    def action_cursor(self, delta: int) -> None:
        ids = self._visible_task_ids()
        if not ids:
            return
        if self.selected_task_id in ids:
            idx = ids.index(self.selected_task_id)
            idx = max(0, min(len(ids) - 1, idx + delta))
        else:
            idx = 0
        self.selected_task_id = ids[idx]
        self.refresh_view()

    # ---- rendering ---------------------------------------------------------
    def refresh_view(self) -> None:
        self._select_first()
        boards = self.query("#board")
        if not boards:
            return
        content = render_view(self.view_mode, self.board, self.show_archived,
                              self.selected_task_id)
        boards.first(Static).update(content)

    def action_view(self, mode: str) -> None:
        if mode in VIEW_ORDER:
            self.view_mode = mode
            self.refresh_view()

    # ---- task CRUD ---------------------------------------------------------
    def action_add_task(self) -> None:
        self.push_screen(TaskModal(self.board), self._on_task_added)

    def _on_task_added(self, data: dict | None) -> None:
        if not data:
            return
        task = Task(**data)
        self.board.add_task(task)
        self.selected_task_id = task.id
        self.refresh_view()

    def action_edit(self) -> None:
        task = self.selected_task
        if task is None:
            return
        self.push_screen(TaskModal(self.board, task),
                        lambda data, t=task: self._on_task_edited(t, data))

    def _on_task_edited(self, task: Task, data: dict | None) -> None:
        if not data:
            return
        for k, v in data.items():
            setattr(task, k, v)
        self.board.save()
        self.refresh_view()

    def action_delete(self) -> None:
        task = self.selected_task
        if task is None:
            return
        self.push_screen(ConfirmModal(f"Delete '{task.title}'?"),
                        lambda ok, t=task: self._on_delete(t, ok))

    def _on_delete(self, task: Task, ok: bool) -> None:
        if not ok:
            return
        self.board.delete_task(task.id)
        self.selected_task_id = None
        self.refresh_view()

    def action_archive(self) -> None:
        task = self.selected_task
        if task is None:
            return
        task.archived = not task.archived
        self.board.save()
        self.refresh_view()

    def action_toggle_archived(self) -> None:
        self.show_archived = not self.show_archived
        self.refresh_view()

    def action_open_url(self) -> None:
        task = self.selected_task
        if task and valid_url(task.url):
            webbrowser.open(task.url)

    # ---- project -----------------------------------------------------------
    def action_add_project(self) -> None:
        self.push_screen(ProjectModal(), self._on_project_added)

    def _on_project_added(self, data: dict | None) -> None:
        if not data:
            return
        self.board.add_project(Project(**data))
        self.refresh_view()
