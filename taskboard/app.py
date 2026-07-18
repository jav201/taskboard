"""The Textual application: view switching, selection, modals, one clock."""

from __future__ import annotations

import webbrowser
from pathlib import Path

from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Footer, Static

from .models import Board, Project, Task, default_board_path
from .modals import ClockModal, ConfirmModal, ProjectModal, TaskModal
from .ribbon import Ribbon
from .views import nav_model, render_view, valid_url

VIEW_ORDER = ["swimlanes", "columns", "agenda", "gantt"]
VIEW_KEYS = {"1": "swimlanes", "2": "columns", "3": "agenda", "4": "gantt"}


class BoardView(Static):
    """The main board surface; re-renders the active view whenever it resizes."""

    def on_resize(self, event: events.Resize) -> None:
        self.app.refresh_view()


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
        ("v", "toggle_archived", "Show arch"),
        ("o", "open_url", "Open URL"),
        ("c", "clocks", "Clocks"),
        # priority=True so these beat the focused VerticalScroll's own arrow-key
        # scrolling when the board overflows (pitfall A6).
        Binding("down,j", "cursor(1)", "Down", priority=True),
        Binding("up,k", "cursor(-1)", "Up", priority=True),
        Binding("left,h", "hmove(-1)", "Left", priority=True),
        Binding("right,l", "hmove(1)", "Right", priority=True),
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
            yield BoardView(id="board")
        with Vertical(id="statusbar"):     # ribbon (top row) + footer (bottom row)
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

    # ---- selection (follows the CURRENT VIEW's on-screen order) -------------
    def _nav_columns(self) -> list[list[str]]:
        return nav_model(self.view_mode, self.board, self.show_archived)

    def _nav_flat(self) -> list[str]:
        return [tid for col in self._nav_columns() for tid in col]

    def _select_first(self) -> None:
        """Selection must be a currently-visible task (data validity). It may
        not be individually navigable in a compact view (e.g. a non-first
        swimlane task) — navigation snaps to nav order on the next key."""
        ids = [t.id for t in self.board.visible_tasks(self.show_archived)]
        if self.selected_task_id not in ids:
            self.selected_task_id = ids[0] if ids else None

    def _locate(self, cols: list[list[str]]) -> tuple[int, int] | None:
        for ci, col in enumerate(cols):
            if self.selected_task_id in col:
                return ci, col.index(self.selected_task_id)
        return None

    @property
    def selected_task(self) -> Task | None:
        return self.board.task_by_id(self.selected_task_id)

    def action_cursor(self, delta: int) -> None:
        """Up/Down: move WITHIN the current column (no jump off the ends)."""
        cols = self._nav_columns()
        loc = self._locate(cols)
        if loc is None:
            self._select_first()
            self.refresh_view()
            return
        ci, ri = loc
        ri2 = ri + delta
        if 0 <= ri2 < len(cols[ci]):     # in-bounds only -> top/bottom is a no-op
            self.selected_task_id = cols[ci][ri2]
            self.refresh_view()

    def action_hmove(self, delta: int) -> None:
        """Left/Right: jump to the nearest non-empty column's first task."""
        cols = self._nav_columns()
        loc = self._locate(cols)
        if loc is None:
            self._select_first()
            self.refresh_view()
            return
        ci = loc[0] + delta
        while 0 <= ci < len(cols):
            if cols[ci]:
                self.selected_task_id = cols[ci][0]
                self.refresh_view()
                return
            ci += delta
        # no non-empty column that direction -> no-op

    # ---- rendering ---------------------------------------------------------
    def refresh_view(self) -> None:
        self._select_first()
        boards = self.query("#board")
        if not boards:
            return
        board_widget = boards.first(BoardView)
        w = board_widget.size.width or 0
        vps = self.query("#viewport")
        h = vps.first().size.height if vps else (board_widget.size.height or 0)
        self._line_map: dict[str, int] = {}
        content = render_view(self.view_mode, self.board, self.show_archived,
                              self.selected_task_id, width=w, height=h,
                              line_map=self._line_map)
        board_widget.update(content)
        self._scroll_selected_into_view()

    def _scroll_selected_into_view(self) -> None:
        idx = getattr(self, "_line_map", {}).get(self.selected_task_id)
        if idx is None:
            return
        vps = self.query("#viewport")
        if not vps:
            return
        vp = vps.first()
        h = vp.size.height or 0
        if h <= 0:
            return
        top = vp.scroll_offset.y
        if idx < top:
            vp.scroll_to(y=idx, animate=False)
        elif idx >= top + h:
            vp.scroll_to(y=idx - h + 1, animate=False)

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
