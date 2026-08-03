"""The Textual application: view switching, selection, modals, one clock."""

from __future__ import annotations

import os
import webbrowser
from pathlib import Path

from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.keys import format_key
from textual.screen import ModalScreen
from textual.widgets import Footer, Static

from .models import IMAGE_EXTS, Board, Project, Task, default_board_path
from .modals import (ClockModal, ConfirmModal, ImageViewer, PhaseEditor, ProjectModal,
                     ProjectPicker, TaskDetails, TaskModal)
from .ribbon import Ribbon
from .views import nav_model, render_view, valid_url

VIEW_ORDER = ["swimlanes", "columns", "agenda", "gantt", "kanban"]
VIEW_KEYS = {"1": "swimlanes", "2": "columns", "3": "agenda", "4": "gantt",
             "5": "kanban"}


class BoardView(Static):
    """The main board surface; re-renders the active view whenever it resizes."""

    def on_resize(self, event: events.Resize) -> None:
        self.app.refresh_view()


def binding_map(screen, shown: bool | None = None) -> list[tuple[str, str, Binding]]:
    """Every binding that ACTUALLY fires on `screen`, one row per action.

    Derived from `active_bindings`, never from a BINDINGS list: a hand-written
    hint drifts the moment a binding moves, and a static list cannot know what
    `check_action` dropped or which screen shadows which key. `format_key` is
    Textual's own name->glyph table (question_mark -> `?`, escape -> `esc`).

    Aliases are kept, not dropped: a binding written `d,delete` prints as
    `d/del`. A working key indicated nowhere is the defect this exists to
    prevent — and the Footer prints only the FIRST key of such a binding.
    """
    keys: dict[tuple[str, str], list[str]] = {}
    firsts: dict[tuple[str, str], Binding] = {}
    for key, ab in screen.active_bindings.items():
        b = ab.binding
        if not ab.enabled or (shown is not None and b.show is not shown):
            continue
        ident = (b.action, b.description)
        keys.setdefault(ident, []).append(key)
        firsts.setdefault(ident, b)
    out = []
    for ident, ks in keys.items():
        b = firsts[ident]
        out.append((b.key_display or "/".join(format_key(k) for k in ks),
                    b.description, b))
    return out


class HelpScreen(ModalScreen[None]):
    """The `?` tier: the FULL keymap of the surface behind this one.

    The footer can only afford the primaries (29 shown bindings printed 12 at
    118 columns, with `q Quit` off the right edge). Everything it drops is
    indicated here, `show=False` bindings included — the motion keys, the
    aliases, `ctrl+q`. The footer is allowed to carry less only because this
    carries everything.
    """

    BINDINGS = [Binding("escape,question_mark,q", "dismiss", "Close",
                        key_display="esc/?/q")]

    DEFAULT_CSS = """
    HelpScreen { align: center middle; }
    #help-box {
        max-width: 98%; height: auto; max-height: 90%;
        padding: 1 2; background: #0d1219; border: round #334154;
    }
    """

    def __init__(self, shown: list[tuple[str, str]],
                 hidden: list[tuple[str, str]]) -> None:
        super().__init__()
        self.sections = [("ON THIS SCREEN", shown), ("MORE KEYS", hidden)]

    def compose(self) -> ComposeResult:
        pairs = [p for _, sec in self.sections for p in sec]
        kw = max((len(k) for k, _ in pairs), default=1)
        dw = max((len(d) for _, d in pairs), default=1)   # never truncated:
        w = kw + dw + 1                                   # a clipped word lies
        cells: list[tuple[str, str, str]] = []            # (plain, markup, sect)
        for title, sec in self.sections:
            if not sec:
                continue
            cells.append((title, f"[#8b98a5]{title}[/]", ""))
            cells += [(f"{k:<{kw}} {d}",
                       f"[#2dd4bf]{k:<{kw}}[/] [#c8d3de]{d}[/]", title)
                      for k, d in sec]
            cells.append(("", "", ""))
        # TWO COLUMNS, balanced by LINES: one column of the full map is ~36
        # rows on a 30-row screen, and the rows that scrolled off the bottom
        # were exactly the hidden keys — the defect again, one layer down. The
        # split may land inside a section, so the heading is repeated: a
        # keymap running on under someone else's title is a new lie.
        if 2 * w + 9 <= self.app.size.width:
            half = (len(cells) + 1) // 2
            for j in range(max(0, half - 2), min(len(cells), half + 3)):
                if not cells[j][0] and not cells[j][2]:   # a section boundary
                    half = j + 1                          # near the balance
                    break                                 # point: snap to it
            left, right = cells[:half], cells[half:]
            if right and right[0][2]:
                head = f"{right[0][2]} (cont.)"
                right.insert(0, (head, f"[#8b98a5]{head}[/]", ""))
        else:
            left, right = cells, []
        left += [("", "", "")] * (len(right) - len(left))
        right += [("", "", "")] * (len(left) - len(right))
        # this screen's own hint, derived like every other legend here. It rides
        # ON the title: as its own bottom row it was the line the map's height
        # pushed off the screen, i.e. the way out was the thing that got clipped
        hint = " · ".join(f"{d} {t.lower()}"
                          for d, t, _ in binding_map(self, shown=True))
        plain = [f"KEYS   {hint}", ""]
        rows = [f"[#2dd4bf]KEYS[/]   [#8b98a5]{hint}[/]", ""]
        for (lp, lm, _), (rp, rm, _) in zip(left, right):
            plain.append(f"{lp:<{w}}   {rp}".rstrip())
            rows.append(f"{lm}{' ' * (w - len(lp))}   {rm}".rstrip())
        while rows and not rows[-1]:      # trailing section gaps cost rows the
            rows.pop()                    # box does not have on a 30-row screen
            plain.pop()
        # a scrollable container does not size to its content: measure the map
        # (the widest PLAIN row) and give the box that width, or the border
        # closes on an empty 4-column box. +8 = padding, border, and the
        # scrollbar gutter — without it the last column wraps.
        box = VerticalScroll(Static("\n".join(rows)), id="help-box")
        box.styles.width = max(len(p) for p in plain) + 8
        yield box

    def on_mount(self) -> None:
        # focus the box so that when the map IS taller than the screen (narrow
        # widths fall back to one column) the arrows and pgdn can reach its
        # tail — an unreachable row is an unindicated key
        self.query_one("#help-box").focus()


class TaskboardApp(App):
    """Frameless kanban desktop widget."""

    CSS_PATH = "taskboard.tcss"
    TITLE = "taskboard"

    # THE FOOTER IS A BUDGET, not an inventory: at 118 columns Textual's Footer
    # prints ~12 entries, and it clips the REST off the right edge silently —
    # `q Quit` was among the casualties (29 shown bindings, 12 printed). So the
    # primaries are shown and everything else is `show=False` WITH ITS WORDS in
    # the `?` map. Nothing is hidden that is not printed there.
    BINDINGS = [
        ("1", "view('swimlanes')", "Lanes"),
        ("2", "view('columns')", "Cols"),
        ("3", "view('agenda')", "Agenda"),
        ("4", "view('gantt')", "Gantt"),
        ("5", "view('kanban')", "Kanban"),
        # the APERTURE: the widget posture as a pushed screen (aperture.py) —
        # ADD beside the five views, views.py untouched (HANDOFF §4 Inc 2)
        ("6", "aperture", "Widget"),
        # `? Keys` and `q Quit` are printed BEFORE the letter actions: the
        # Footer clips from the right at narrow widths, and the two keys that
        # must never be clipped are the way out and the way to the full map.
        Binding("question_mark", "help", "Keys"),
        ("q", "quit", "Quit"),
        ("a", "add_task", "Add"),
        ("e", "edit", "Edit"),
        Binding("d,delete", "delete", "Del"),
        # ---- the `?` tier: real keys, kept off the footer so it fits --------
        Binding("enter", "details", "Details", show=False),
        Binding("x", "archive", "Archive", show=False),
        Binding("v", "toggle_archived", "Show archived", show=False),
        Binding("o", "open_url", "Open URL", show=False),
        Binding("i", "open_images", "Images", show=False),
        Binding("c", "clocks", "Clocks", show=False),
        Binding("p", "add_project", "New project", show=False),
        # `P` (Projects) was the user's reported shift key: SHOWN on the footer
        # and unreachable without shift. The door is `m` and only `m` — no key
        # in this app needs shift.
        Binding("m", "manage_projects", "Projects", show=False),
        Binding("f", "manage_phases", "Phases", show=False),
        # priority=True so tab reaches us instead of the screen's focus_next;
        # check_action hands it back to modals (see below). Kanban-only, so it
        # spends no footer width.
        Binding("tab", "toggle_presentation", "Layout", show=False,
                priority=True),
        # priority=True so these beat the focused VerticalScroll's own arrow-key
        # scrolling when the board overflows (pitfall A6).
        Binding("down,j", "cursor(1)", "Down", show=False, priority=True),
        Binding("up,k", "cursor(-1)", "Up", show=False, priority=True),
        Binding("left,h", "hmove(-1)", "Left", show=False, priority=True),
        Binding("right,l", "hmove(1)", "Right", show=False, priority=True),
    ]

    # keys that act on the BOARD — a surface the aperture replaces. They stayed
    # live there (`d` opened a delete-confirm for a task nobody could see) and
    # they were indicated by nothing. FALSE, not None: Textual drops a binding
    # from `active_bindings` only on `is False`; None leaves it listed and
    # merely disabled, i.e. a legend entry that does nothing.
    BOARD_ACTIONS = frozenset({
        "add_task", "add_project", "manage_projects", "manage_phases",
        "details", "edit", "delete", "archive", "toggle_archived",
        "open_url", "open_images", "clocks", "toggle_presentation",
        "cursor", "hmove"})
    # `quit` is deliberately NOT in that set: the aperture shadows `q` with its
    # own Back binding, and ctrl+q must stay the one door out from anywhere.

    def __init__(self, board_path: str | Path | None = None):
        super().__init__()
        self.board = Board.load(board_path or default_board_path())
        self.view_mode = "swimlanes"
        self.kanban_presentation = "grouped"
        self.show_archived = False
        self.selected_task_id: str | None = None
        self._tick_n = 0                 # drives the gantt flow packet

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """While a modal is open, release the board's priority arrow/vim bindings
        so the modal's own widgets (e.g. the ProjectPicker list, Select dropdowns)
        receive them instead of moving the hidden board selection.

        On the APERTURE the same reasoning goes further: it is not the board, it
        is the ambient face of it, so every key that edits or navigates the board
        is dropped there (the aperture is a launcher — press 1-5 to reach the
        surface those keys belong to)."""
        if (action in ("cursor", "hmove", "toggle_presentation")
                and len(self.screen_stack) > 1):
            return False
        if action in self.BOARD_ACTIONS and len(self.screen_stack) > 1:
            from .aperture import ApertureScreen      # lazy: aperture imports us
            if isinstance(self.screen, ApertureScreen):
                return False
        return True

    def action_help(self) -> None:
        """The `?` tier: the full keymap of the surface in front of the user."""
        rows = [[(d, t) for d, t, _ in binding_map(self.screen, shown=s)]
                for s in (True, False)]
        self.push_screen(HelpScreen(rows[0], rows[1]))

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
        self._warn_if_rescued()

    def _warn_if_rescued(self) -> None:
        """Surface a load that had to repair drifted/corrupt data, so the user
        knows some items were recovered (and can open them to fix them)."""
        r = self.board.load_report
        if not r:
            return
        if r.get("file_unreadable"):
            where = r.get("backup") or "a .corrupt sidecar"
            self.notify(
                f"board.json was unreadable; a copy was kept at {where}. "
                "Started empty — your file was not overwritten.",
                title="Board recovered", severity="error", timeout=10)
        elif r.get("tasks_rescued") or r.get("projects_rescued"):
            n = r.get("tasks_rescued", 0) + r.get("projects_rescued", 0)
            self.notify(
                f"{n} item(s) had an unreadable format and were recovered "
                "(see their notes). Nothing was lost.",
                title="Tasks recovered", severity="warning", timeout=10)

    # ---- clock -------------------------------------------------------------
    def _tick(self) -> None:
        ribbons = self.query("#ribbon")
        if ribbons:
            ribbons.first(Ribbon).update_clock()
        self._tick_n += 1
        if self.view_mode == "gantt":
            self._repaint_flow()         # advance the flow packet, keep scroll/selection

    def _repaint_flow(self) -> None:
        """Re-render the board content at the new tick WITHOUT re-selecting or
        scrolling, so the gantt flow animates without yanking the viewport."""
        boards = self.query("#board")
        if not boards:
            return
        bw = boards.first(BoardView)
        vps = self.query("#viewport")
        h = vps.first().size.height if vps else (bw.size.height or 0)
        self._line_map = {}
        bw.update(render_view(self.view_mode, self.board, self.show_archived,
                              self.selected_task_id, width=bw.size.width or 0, height=h,
                              line_map=self._line_map,
                              presentation=self.kanban_presentation, tick=self._tick_n))

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
                              line_map=self._line_map,
                              presentation=self.kanban_presentation, tick=self._tick_n)
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

    def action_aperture(self) -> None:
        """The widget posture: hero + meter + signal tiles + calendar/queue,
        rendered through the active design language (t cycles the nine)."""
        from .aperture import ApertureScreen
        self.push_screen(ApertureScreen(self.board))

    def action_toggle_presentation(self) -> None:
        """Tab flips the kanban view's presentation; a no-op elsewhere."""
        if self.view_mode != "kanban":
            return
        self.kanban_presentation = ("matrix" if self.kanban_presentation == "grouped"
                                    else "grouped")
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

    def action_details(self) -> None:
        """Read-only details view of the selected task (Enter). Never opens the
        editor — a safe way to review all fields + images."""
        task = self.selected_task
        if task is None:
            return
        self.push_screen(TaskDetails(task, self.board))

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
        if not task:
            return
        for u in task.urls:                 # open EVERY valid http(s) URL
            v = valid_url(u)
            if v:
                webbrowser.open(v)

    def action_open_images(self) -> None:
        task = self.selected_task
        if not task:
            return
        self.push_screen(ImageViewer(task, self.board))

    def open_all_images_raw(self, task: Task) -> None:
        """Open every image on the task in its OS-default app / browser (raw)."""
        for ref in task.images:
            v = valid_url(ref)
            if v:                           # http(s) image URL -> browser
                webbrowser.open(v)
            else:                           # otherwise treat as a local file path
                self._open_local_image(ref)

    def _open_local_image(self, ref: str) -> None:
        """Open a local image path in the OS viewer, gated for safety (C-6).

        Only an EXISTING regular file whose extension is in the image allowlist
        is passed to os.startfile; UNC and file:// paths are refused; any
        os-level failure is swallowed so a keypress never crashes the app."""
        if ref.startswith(("\\\\", "//")):          # UNC path -> refuse (F3)
            return
        if ref.lower().startswith("file://"):       # file URL -> refuse (F3)
            return
        if Path(ref).suffix.lower() not in IMAGE_EXTS:   # extension allowlist (F4)
            return
        if not os.path.isfile(ref):                 # must be an existing file (F3)
            return
        try:
            os.startfile(ref)                       # Windows-only (DD-4)
        except OSError:
            pass

    # ---- project -----------------------------------------------------------
    def action_add_project(self) -> None:
        self.push_screen(ProjectModal(), self._on_project_added)

    def _on_project_added(self, data: dict | None) -> None:
        if not data:
            return
        self.board.add_project(Project(**data))
        self.refresh_view()

    def action_manage_projects(self) -> None:
        self.push_screen(ProjectPicker(self.board))

    # ---- phases ------------------------------------------------------------
    def action_manage_phases(self) -> None:
        self.push_screen(PhaseEditor(self.board))
