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

import calendar
import os
from datetime import date, timedelta
from pathlib import Path

from rich.markup import escape

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.suggester import SuggestFromList
from textual.widgets import (Button, Checkbox, Input, Label, OptionList, Select, Static,
                             TextArea)
from textual.widgets.option_list import Option

from .models import (IMAGE_EXTS, PROJECT_COLORS, PROJECT_STATUSES, TASK_PRIORITIES,
                     Board, Project, Task, _new_id, city_names,
                     grab_clipboard_image, grab_clipboard_text, parse_iso,
                     resolve_city, save_pil_image)
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

_WEEK_HEADER = "[dim]Mo Tu We Th Fr Sa Su[/dim]"


class CalendarModal(ModalScreen[str | None]):
    """Arrow-key month calendar. Dismisses with 'YYYY-MM-DD' on Enter, None on
    Esc. Navigation: left/right ±1 day, up/down ±1 week, [ / ] (or PageUp/Down)
    ±1 month, t = today. Monday-first; stdlib calendar + datetime only.

    Nav bindings are priority so the focusable scroll container can't eat the
    arrows (pitfall A6)."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        Binding("left", "move(-1)", "-1d", show=False, priority=True),
        Binding("right", "move(1)", "+1d", show=False, priority=True),
        Binding("up", "move(-7)", "-1w", show=False, priority=True),
        Binding("down", "move(7)", "+1w", show=False, priority=True),
        Binding("left_square_bracket,pageup", "month(-1)", "-1m", show=False, priority=True),
        Binding("right_square_bracket,pagedown", "month(1)", "+1m", show=False, priority=True),
        Binding("t", "today", "Today", show=False, priority=True),
        Binding("enter", "pick", "Pick", show=False, priority=True),
    ]

    def __init__(self, initial: str | None = None):
        super().__init__()
        self._sel = parse_iso(initial) or date.today()

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="cal-box", classes="modal"):
            yield Label(self._title_text(), id="cal-title", classes="modal-title")
            yield Static(self._grid_text(), id="cal-grid")

    def _title_text(self) -> str:
        # escape the literal [ ] (the month-nav keys) so Rich renders them
        # verbatim instead of treating them as a markup tag
        return (f"[b]{self._sel:%B %Y}[/b]  —  "
                "←→ day · ↑↓ week · \\[ \\] month · t today · enter pick")

    def _grid_text(self) -> str:
        d = self._sel
        lines = [_WEEK_HEADER]
        for week in calendar.Calendar(firstweekday=0).monthdatescalendar(d.year, d.month):
            cells = []
            for day in week:
                label = f"{day.day:2d}"
                if day == d:
                    cells.append(f"[b reverse]{label}[/]")
                elif day.month != d.month:
                    cells.append(f"[dim]{label}[/dim]")
                else:
                    cells.append(label)
            lines.append(" ".join(cells))
        return "\n".join(lines)

    def _redraw(self) -> None:
        # NOT _render: that name is Textual's internal Widget._render(), which
        # must return a Visual. Overriding it to return None makes the screen's
        # own visual None and crashes Visual.to_strips (render_strips).
        self.query_one("#cal-title", Label).update(self._title_text())
        self.query_one("#cal-grid", Static).update(self._grid_text())

    def action_move(self, days: int) -> None:
        self._sel += timedelta(days=days)
        self._redraw()

    def action_month(self, delta: int) -> None:
        month_index = self._sel.month - 1 + delta
        year = self._sel.year + month_index // 12
        month = month_index % 12 + 1
        last = calendar.monthrange(year, month)[1]
        self._sel = self._sel.replace(year=year, month=month, day=min(self._sel.day, last))
        self._redraw()

    def action_today(self) -> None:
        self._sel = date.today()
        self._redraw()

    def action_pick(self) -> None:
        self.dismiss(self._sel.isoformat())

    def action_cancel(self) -> None:
        self.dismiss(None)


class ClipboardPasteMixin:
    """Reliable Ctrl+V text paste for a modal: reads OS clipboard TEXT and
    inserts it into the focused Input/TextArea. Textual's native paste is
    unreliable on Windows, so we read the clipboard ourselves. Each modal wires
    the Ctrl+V binding in its own BINDINGS (Textual doesn't collect BINDINGS from
    a plain mixin); this class supplies the action."""

    def action_paste_text(self) -> None:
        target = self.app.focused
        if not isinstance(target, (Input, TextArea)):
            self.notify("Focus a text field to paste into.", severity="warning")
            return
        text = grab_clipboard_text()
        if not text:
            self.notify("Clipboard has no text.", severity="warning")
            return
        if isinstance(target, Input):
            target.insert_text_at_cursor(text)
        else:
            target.insert(text)


class DatePickerMixin:
    """Calendar-button handler: opens CalendarModal for a date field and writes
    the picked 'YYYY-MM-DD' back into that field's Input. Button ids are
    'cal-<field-id>' (e.g. 'cal-f-start')."""

    def _open_calendar(self, field_id: str) -> None:
        current = self.query_one(f"#{field_id}", Input).value.strip()
        self.app.push_screen(CalendarModal(current or None),
                             lambda res, fid=field_id: self._on_date_picked(fid, res))

    def _on_date_picked(self, field_id: str, result: str | None) -> None:
        if result:
            self.query_one(f"#{field_id}", Input).value = result


class TaskModal(ClipboardPasteMixin, DatePickerMixin, ModalScreen[dict | None]):
    """Returns a dict of task fields on save, or None on cancel."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("ctrl+v", "paste_text", "Paste", priority=True)]

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
                yield Label("Phase")
                phases = self.board.phases
                yield Select([(escape(p), p) for p in phases],
                             value=(t.phase if (t and t.phase in phases) else phases[0]),
                             allow_blank=False, id="f-phase")
                yield Label("Blocked")
                yield Checkbox("blocked", value=bool(t.blocked) if t else False,
                               id="f-blocked")
                yield Label("Priority")
                yield Select([(p, p) for p in TASK_PRIORITIES],
                             value=(t.priority if t else "normal"),
                             allow_blank=False, id="f-priority")
                yield Label("Start (YYYY-MM-DD)")
                with Horizontal(classes="date-row"):
                    yield Input(value=(t.start_date or "" if t else ""), placeholder="optional",
                                id="f-start", classes="date-input")
                    yield Button("📅", id="cal-f-start", classes="cal-btn")
                yield Label("Due (YYYY-MM-DD)")
                with Horizontal(classes="date-row"):
                    yield Input(value=(t.due_date or "" if t else ""), placeholder="optional",
                                id="f-due", classes="date-input")
                    yield Button("📅", id="cal-f-due", classes="cal-btn")
            yield Label("Notes")
            notes_area = TextArea(t.notes if t else "", id="f-notes")
            notes_area.styles.height = 5   # 1fr TextArea would collapse in the auto modal
            yield notes_area
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
        bid = event.button.id or ""
        if bid == "save":
            self._save()
        elif bid == "paste-img":
            self._paste_image()
        elif bid.startswith("cal-"):
            self._open_calendar(bid[4:])
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
            "phase": self._val("f-phase"),
            "blocked": bool(self.query_one("#f-blocked", Checkbox).value),
            "priority": self._val("f-priority"),
            "start_date": self._val("f-start") or None,
            "due_date": self._val("f-due") or None,
            "notes": self.query_one("#f-notes", TextArea).text.strip(),
            "urls": urls,
            "images": self._lines("f-images"),   # local paths valid at entry (no filter)
        }
        self.dismiss(data)


class ProjectModal(ClipboardPasteMixin, DatePickerMixin, ModalScreen[dict | None]):
    """Returns a dict of project fields on save, or None on cancel."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("ctrl+v", "paste_text", "Paste", priority=True)]

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
                with Horizontal(classes="date-row"):
                    yield Input(value=(p.start_date or "" if p else ""), placeholder="optional",
                                id="f-start", classes="date-input")
                    yield Button("📅", id="cal-f-start", classes="cal-btn")
                yield Label("Due (YYYY-MM-DD)")
                with Horizontal(classes="date-row"):
                    yield Input(value=(p.due_date or "" if p else ""), placeholder="optional",
                                id="f-due", classes="date-input")
                    yield Button("📅", id="cal-f-due", classes="cal-btn")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id or ""
        if bid == "save":
            self._save()
        elif bid.startswith("cal-"):
            self._open_calendar(bid[4:])
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


class ClockModal(ClipboardPasteMixin, ModalScreen[dict | None]):
    """Pick the two ribbon clocks by CITY (type to find one). Returns city names."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("ctrl+v", "paste_text", "Paste", priority=True)]

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


class TextPrompt(ModalScreen[str | None]):
    """One-line text prompt. Dismisses with the STRIPPED text on Save/Enter and
    None on Cancel/Esc, so the caller can tell "left it blank" from "cancelled"."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, title: str, initial: str = "", placeholder: str = ""):
        super().__init__()
        self._title = title
        self._initial = initial
        self._placeholder = placeholder

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label(f"[b]{escape(self._title)}[/b]", classes="modal-title")
            yield Input(value=self._initial, placeholder=self._placeholder, id="f-text")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#f-text", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self._save()
        else:
            self.dismiss(None)

    def _save(self) -> None:
        self.dismiss(str(self.query_one("#f-text", Input).value).strip())

    def action_cancel(self) -> None:
        self.dismiss(None)


class PhaseEditor(ModalScreen[None]):
    """Manage the board's ORDERED phases: add / rename / reorder / delete.

    Mutations persist immediately (Board.save) and re-render the board behind
    the modal, so the editor stays open for the next action. Phase names are
    user text -> escaped everywhere they are rendered (A1). Renaming moves the
    tasks that referenced the old name and deleting reassigns them to a
    neighbour, so no edit here can orphan a task; the last phase can't be
    deleted because every view indexes into the list.
    """

    BINDINGS = [
        ("escape", "close", "Close"),
        ("a", "add", "Add"),
        ("e", "rename", "Rename"),
        ("d", "delete", "Delete"),
        Binding("left_square_bracket", "reorder(-1)", "Earlier"),
        Binding("right_square_bracket", "reorder(1)", "Later"),
        Binding("j", "move(1)", show=False),
        Binding("k", "move(-1)", show=False),
    ]

    def __init__(self, board: Board):
        super().__init__()
        self.board = board

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="picker-box", classes="modal"):
            # the literal [ is escaped so Rich prints the key instead of
            # reading it as the start of a markup tag
            yield Label("[b]Phases[/b]  —  a add · e rename · d delete · "
                        "\\[ / ] reorder · esc close", classes="modal-title")
            yield OptionList(id="phase-list")

    def on_mount(self) -> None:
        self._reload()
        self.query_one("#phase-list", OptionList).focus()

    # ---- list rendering ----------------------------------------------------
    def _phase_line(self, index: int, name: str) -> str:
        n = sum(1 for t in self.board.tasks if t.phase == name)
        return (f"[dim]{index + 1}.[/dim]  [b]{escape(name)}[/b]"
                f"  ·  {n} task{'s' if n != 1 else ''}")

    def _reload(self, keep: int | None = None) -> None:
        """Rebuild the list from the board (clear-before-add avoids DuplicateIds)."""
        ol = self.query_one("#phase-list", OptionList)
        ol.clear_options()
        phases = self.board.phases
        for i, name in enumerate(phases):
            ol.add_option(Option(self._phase_line(i, name)))
        if phases:
            ol.highlighted = max(0, min(len(phases) - 1, keep or 0))

    def _committed(self, keep: int) -> None:
        self.board.save()
        self.app.refresh_view()
        self._reload(keep=keep)

    def _current_index(self) -> int | None:
        """Position of the highlighted phase, or None when nothing is selected.
        Rows carry no id — a phase is identified by its position, which is the
        thing reordering changes."""
        idx = self.query_one("#phase-list", OptionList).highlighted
        if idx is None or not (0 <= idx < len(self.board.phases)):
            return None
        return idx

    # ---- navigation / actions ---------------------------------------------
    def action_move(self, delta: int) -> None:
        phases = self.board.phases
        if not phases:
            return
        ol = self.query_one("#phase-list", OptionList)
        cur = ol.highlighted if ol.highlighted is not None else 0
        ol.highlighted = max(0, min(len(phases) - 1, cur + delta))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.action_rename()   # Enter / click on a row renames it

    def action_add(self) -> None:
        self.app.push_screen(TextPrompt("New phase", placeholder="phase name"),
                             self._on_added)

    def _on_added(self, name: str | None) -> None:
        if name is None:
            return
        if not name:
            self.notify("A phase needs a name.", severity="warning")
            return
        if not self.board.add_phase(name):
            self.notify(f"'{escape(name)}' already exists.", severity="warning")
            return
        self._committed(len(self.board.phases) - 1)

    def action_rename(self) -> None:
        i = self._current_index()
        if i is None:
            return
        old = self.board.phases[i]
        self.app.push_screen(TextPrompt("Rename phase", initial=old),
                             lambda new, o=old: self._on_renamed(o, new))

    def _on_renamed(self, old: str, new: str | None) -> None:
        if new is None or new == old:
            return
        if not new:
            self.notify("A phase needs a name.", severity="warning")
            return
        if not self.board.rename_phase(old, new):
            self.notify(f"'{escape(new)}' already exists.", severity="warning")
            return
        self._committed(self.board.phases.index(new))

    def action_delete(self) -> None:
        i = self._current_index()
        if i is None:
            return
        if len(self.board.phases) <= 1:
            self.notify("A board needs at least one phase.", severity="warning")
            return
        name = self.board.phases[i]
        target = self.board.phases[i - 1] if i > 0 else self.board.phases[1]
        n = sum(1 for t in self.board.tasks if t.phase == name)
        self.app.push_screen(
            ConfirmModal(f"Delete '{name}'? Its {n} task{'s' if n != 1 else ''} "
                         f"move to '{target}'."),
            lambda ok, nm=name, k=i: self._on_delete(nm, k, ok))

    def _on_delete(self, name: str, index: int, ok: bool) -> None:
        if not ok or not self.board.delete_phase(name):
            return
        self._committed(max(0, index - 1))

    def action_reorder(self, delta: int) -> None:
        i = self._current_index()
        if i is None:
            return
        if not self.board.move_phase(self.board.phases[i], delta):
            return
        self._committed(i + delta)      # follow the phase to its new position

    def action_close(self) -> None:
        self.dismiss(None)


def image_block(ref: str):
    """Render one image reference inline (crisp via terminal graphics where
    supported, else a fallback line). Remote URLs are listed as links; a
    missing / unrenderable local file yields a dim notice. A generator of
    widgets, shared by ImageViewer and TaskDetails. Never raises."""
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
        img = AutoImage(str(path))           # size comes from the Image TCSS rule
    except Exception:                        # never blank the modal on one bad file
        yield Label(f"[dim]could not render:[/dim] {escape(ref)}")
        return
    yield img
    yield Label(f"[dim]{escape(path.name)}[/dim]")


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
                yield from image_block(ref)

    def action_open_raw(self) -> None:
        self.app.open_all_images_raw(self._view_task)

    def action_close(self) -> None:
        self.dismiss(None)


class TaskDetails(ModalScreen[None]):
    """Read-only view of every field on a task, with images rendered inline.
    No save/edit control (can't mutate the task) — ``o`` opens images/URLs raw
    in the OS handler, ``esc`` closes. Every user-controlled string is escaped
    (markup-injection pitfall A1)."""

    BINDINGS = [("escape", "close", "Close"), ("o", "open_raw", "Open raw")]

    def __init__(self, task: Task, board: Board):
        super().__init__()
        self._detail_task = task     # NOT self._task: collides with Textual's pump task
        self._board = board

    def compose(self) -> ComposeResult:
        t = self._detail_task
        proj = self._board.project_by_id(t.project_id)
        proj_name = escape(proj.name) if proj else "Inbox"
        with VerticalScroll(id="details-box", classes="modal"):
            yield Label(f"[b]{escape(t.title)}[/b]  —  o open raw · esc close",
                        classes="modal-title")
            with Grid(classes="modal-grid"):
                yield Label("Project")
                yield Label(proj_name)
                yield Label("Phase")
                yield Label(escape(t.phase) + (" · blocked" if t.blocked else ""))
                yield Label("Priority")
                yield Label(escape(t.priority))
                yield Label("Start")
                yield Label(escape(t.start_date or "—"))
                yield Label("Due")
                yield Label(escape(t.due_date or "—"))
            yield Label("[b]Notes[/b]")
            yield Static(escape(t.notes) if t.notes else "[dim]—[/dim]")
            yield Label("[b]URLs[/b]")
            if t.urls:
                for u in t.urls:
                    yield Label(f"link · {escape(u)}")
            else:
                yield Label("[dim]—[/dim]")
            yield Label("[b]Images[/b]")
            if t.images:
                for ref in t.images:
                    yield from image_block(ref)
            else:
                yield Label("[dim]—[/dim]")

    def action_open_raw(self) -> None:
        self.app.open_all_images_raw(self._detail_task)

    def action_close(self) -> None:
        self.dismiss(None)
