"""The Textual application: view switching, selection, modals, one clock."""

from __future__ import annotations

import os
import webbrowser
from datetime import date
from pathlib import Path

from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.keys import format_key
from textual.screen import ModalScreen
from textual.widgets import Static

from . import history
from .models import (AUTO_ARCHIVE_DAYS, IMAGE_EXTS, Board, Project, Task,
                     bump_due, default_board_path, next_priority)
from .modals import (BlockerPicker, ClockModal, CommandPalette, ConfirmModal,
                     ImageViewer, LegendModal, PhaseEditor, ProjectModal, ProjectPicker,
                     StandupModal, TaskDetails, TaskModal, TeamIdentityPicker, TextPrompt)
from .keymap import KeyBar, app_bindings, palette_commands
from .ribbon import Ribbon
from .team_sync import TeamState
from .views import clip, escape, filtered_board, nav_model, render_view, valid_url

# The app's ONE shared clock. Every animated surface counts in these ticks, so
# the ambient's cycle length is this times the number of phases it rotates
# through — which is why the motion laws read it instead of assuming it.
TICK_SECONDS = 1.0

# Written into board.json the first time the renumbering notice is shown, so it
# is shown exactly once per board rather than at every launch.
RENUMBER_NOTICE_KEY = "seen_view_renumber_2026_07"

VIEW_ORDER = ["swimlanes", "agenda", "gantt", "kanban", "focus", "flow", "standup", "people"]
VIEW_KEYS = {"1": "swimlanes", "2": "agenda", "3": "gantt", "4": "kanban",
             "5": "focus", "7": "flow", "8": "standup", "9": "people"}


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
    prevent — and a collapsed hint prints only the FIRST key of such a binding.
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

    The key bar can only afford the primaries; everything it drops is
    indicated here, `show=False` bindings included — the motion keys, the
    aliases, `ctrl+q`. The bar is allowed to carry less only because this
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

    # GENERATED, never hand-written: the same KEYMAP that draws the key bar.
    # A binding that is not in the seat does not exist, and a binding in the seat
    # is always on screen. (`priority=True` on tab and the arrows comes from the
    # seat too: tab must reach us instead of the screen's focus_next, and the
    # arrows must beat the focused VerticalScroll's own scrolling — pitfall A6.
    # `check_action` hands them all back to modals; see below.)
    BINDINGS = app_bindings()

    def __init__(self, board_path: str | Path | None = None, *,
                 team_sync_interval: float = 1800.0):
        super().__init__()
        self.board = Board.load(board_path or default_board_path())
        self.view_mode = "swimlanes"
        self.kanban_presentation = "grouped"
        self.kanban_sort = "project"       # session-level view state (LLR-003.2):
        self.kanban_group = "project"      # never persisted, survives view hops
        self.kanban_collapsed = False      # session-level too (LLR-007.1): THE
                                           # LAST phase only — a working posture,
                                           # not board data (§6.2 D-4)
        self.focus_presentation = "tiles"  # session-level (batch-07): tiles /
                                           # inspector / images
        self.lanes_presentation = "grid"   # session-level (batch-09): grid /
                                           # waves
        self.focused_project_id: str | None = None   # session-level (LLR-008.1):
                                           # the kanban project focus — None off
        self._undo_stack: list[dict] = []  # session LIFO of pre-mutation
                                           # snapshots (LLR-010.1) — never a
                                           # file format, gone on restart
        self.show_archived = False
        self.search_query: str | None = None   # session-level filter (LLR-003.2)
        self.selected_task_id: str | None = None
        self._tick_n = 0                 # drives the gantt flow packet
        self._last_history_error: str | None = None  # suppress duplicate warnings
        self.team_sync_interval = team_sync_interval
        self.team_state: TeamState | None = None
        self.team_filter: str = "equipo"   # session-level classification filter

    # keys that act on the BOARD. They stay live on pushed screens (e.g. a
    # modal) and were indicated by nothing. FALSE, not None: Textual drops a
    # binding from `active_bindings` only on `is False`; None leaves it listed
    # and merely disabled, i.e. a legend entry that does nothing.
    BOARD_ACTIONS = frozenset({
        "add_task", "add_project", "manage_projects", "manage_phases",
        "details", "edit", "delete", "archive", "purge_done", "report",
        "toggle_archived", "open_url", "open_images", "clocks",
        "phase_move", "prio_cycle", "toggle_blocked",
        "kanban_sort", "kanban_group", "collapse_toggle",
        "focus_cycle", "focus_exit", "due_bump", "undo", "standup",
        "toggle_presentation", "cursor", "hmove",
        "pin_toggle", "project_pin_toggle"})

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """While a modal is open, release the board's priority arrow/vim bindings
        so the modal's own widgets (e.g. the ProjectPicker list, Select dropdowns)
        receive them instead of moving the hidden board selection."""
        if (action in ("cursor", "hmove", "toggle_presentation")
                and len(self.screen_stack) > 1):
            return False
        return True

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="viewport"):
            yield BoardView(id="board")
        with Vertical(id="statusbar"):     # ribbon (top row) + key bar (bottom row)
            yield Ribbon(id="ribbon")
            yield KeyBar(id="keybar")

    def on_mount(self) -> None:
        self._announce_renumbering()
        self._sweep_old_done()
        self._select_first()
        self.refresh_view()
        self._apply_clock_settings()
        # ONE shared clock interval for the whole app (never per-widget).
        self.set_interval(TICK_SECONDS, self._tick)
        self._warn_if_rescued()
        self._init_team_mode()

    def _announce_renumbering(self) -> None:
        """Say ONCE that the keys moved. Muscle memory is a real thing a user
        built, and moving `2` from columns to agenda without a word is the same
        sin as hiding a key: the screen would stop matching what they know."""
        if self.board.settings.get(RENUMBER_NOTICE_KEY):
            return
        self.board.settings[RENUMBER_NOTICE_KEY] = True
        self.board.save()
        self.notify(
            "The columns view was retired — kanban does the same job better. "
            "The views are now 1 lanes · 2 agenda · 3 gantt · 4 kanban.",
            title="View keys renumbered", severity="information", timeout=10)

    def _sweep_old_done(self) -> None:
        """Archive long-finished work at startup — and SAY SO. Tasks leaving the
        board without a word is the thing that would make a user distrust it;
        they are archived, not deleted, and `v` shows them again."""
        moved = self.board.auto_archive_done()
        if not moved:
            return
        self.board.save()
        self.notify(
            f"{len(moved)} task(s) finished more than {AUTO_ARCHIVE_DAYS} days ago "
            "were archived. Press 'v' to see archived items, 'x' to bring one back.",
            title="Archived old work", severity="information", timeout=8)

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
                "Started empty — the original file was not overwritten.",
                title="Board recovered", severity="error", timeout=10)
        elif r.get("tasks_rescued") or r.get("projects_rescued"):
            n = r.get("tasks_rescued", 0) + r.get("projects_rescued", 0)
            self.notify(
                f"{n} item(s) had an unreadable format and were recovered "
                "(see their notes). Nothing was lost.",
                title="Tasks recovered", severity="warning", timeout=10)

    # ---- team sync ---------------------------------------------------------
    def _init_team_mode(self) -> None:
        """Enter team mode if ``board.settings["team_shared_dir"]`` is set.

        If the user has no ``team_user_id`` yet, ask them to pick from the
        roster before any sync runs.  A missing or unparseable ``team.json``
        cannot identify them, so team mode stays off until the directory is
        healthy.
        """
        shared_dir = self.board.settings.get("team_shared_dir")
        user_id = self.board.settings.get("team_user_id")
        self.team_state = TeamState.from_settings(shared_dir, user_id)
        if self.team_state is None:
            return
        self.team_state.load_config()
        if self.team_state.user_id:
            self._run_team_sync()
            self._start_team_daemon()
            return
        roster = self.team_state.roster()
        if roster:
            self.push_screen(TeamIdentityPicker(roster), self._on_identity_picked)
        else:
            # roster-less shared dir cannot identify the owner
            self.team_state = None

    def _on_identity_picked(self, user_id: str | None) -> None:
        """Persist the chosen identity, run an initial sync, and start daemon."""
        if user_id is None or self.team_state is None:
            self.team_state = None
            return
        self.board.settings["team_user_id"] = user_id
        self.team_state.user_id = user_id
        self._run_team_sync()
        self.board.save()
        self.refresh_view()
        self._start_team_daemon()

    def _start_team_daemon(self) -> None:
        """Schedule the periodic pull/push cycle when team mode is active."""
        if self.team_state is None or not self.team_state.user_id:
            return
        self.set_interval(self.team_sync_interval, self._team_sync_tick)

    def _run_team_sync(self) -> None:
        """One sync pass: push/pull then inherit authoritative config."""
        if self.team_state is None:
            return
        self.team_state.sync(self.board)
        self.team_state.apply_config_to_board(self.board)

    def _team_sync_tick(self) -> None:
        """Daemon callback.  Never crashes the app; a failure surfaces as a
        warning notification and the next tick tries again."""
        if self.team_state is None:
            return
        try:
            self._run_team_sync()
            self.refresh_view()
        except Exception as exc:
            self.notify(f"Team sync failed: {exc}", title="Team sync",
                        severity="warning")

    # ---- clock -------------------------------------------------------------
    def _tick(self) -> None:
        ribbons = self.query("#ribbon")
        if ribbons:
            ribbons.first(Ribbon).update_clock()
        self._tick_n += 1
        if self.view_mode in ("gantt", "swimlanes"):
            # gantt: advance the flow packet. lanes: breathe the today rule.
            # Both keep scroll and selection exactly where they were.
            self._repaint_flow()

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
                              presentation=self.kanban_presentation, tick=self._tick_n,
                              kanban_sort=self.kanban_sort,
                              kanban_group=self.kanban_group,
                              kanban_collapsed=self.kanban_collapsed,
                              kanban_focus=self.focused_project_id,
                              gantt_focus=self.focused_project_id,
                              lanes_presentation=self.lanes_presentation,
                              focus_presentation=self.focus_presentation,
                              search_query=self.search_query,
                              team_state=self.team_state,
                              team_filter=self.team_filter))

    def _apply_clock_settings(self) -> None:
        ribbons = self.query("#ribbon")
        if not ribbons:
            return
        ribbon = ribbons.first(Ribbon)
        ribbon.clock1_key, ribbon.clock2_key = self.board.get_clocks()
        ribbon.update_clock()

    def action_legend(self) -> None:
        """`?` — the command palette: search every binding by name or key and
        run it."""
        self.push_screen(CommandPalette(palette_commands(self.view_mode)),
                         callback=self._on_palette_run)

    async def _on_palette_run(self, action: str | None) -> None:
        """Execute the action selected from the palette, if any."""
        if not action:
            return
        await self.run_action(action)

    def action_layer_toggle(self) -> None:
        """`;` -- toggle the keybar between its compact primary layer and the
        grouped more-layer. The state lives on the KeyBar so it survives view
        switches and resizes."""
        keybar = self.query_one("#keybar", KeyBar)
        keybar.set_layer("more" if keybar.layer == "primary" else "primary")

    def action_report(self) -> None:
        """`R` — write an HTML report of the board beside the board file.

        It says where the file went and does NOT open it: opening a browser is
        an action the reader did not ask for, so it stays their move."""
        from .report import write_report
        out = write_report(self.board)
        self.notify(f"Report written to {out}", title="Report",
                    severity="information", timeout=10)

    def action_standup(self) -> None:
        """`S` — the week in one modal: what moved and what closed, per
        project, derived from `phase_changed` alone. Nothing is stored for
        this, and the modal mutates nothing — it is a reading, not an edit."""
        self.push_screen(StandupModal(self.board,
                                      show_archived=self.show_archived))

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
        # The lanes view's allocator spends the HEIGHT it is given, so how many
        # tasks it names — and therefore what the cursor can reach — depends on
        # the viewport. Navigation asks the same question the renderer answered.
        vps = self.query("#viewport")
        h = vps.first().size.height if vps else 0
        boards = self.query("#board")
        bw = boards.first(BoardView).size.width if boards else 0
        board = self._view_board()
        if self.view_mode == "kanban":
            presentation = self.kanban_presentation
        elif self.view_mode == "swimlanes":
            presentation = self.lanes_presentation
        else:
            presentation = "grouped"
        return nav_model(self.view_mode, board, self.show_archived,
                         width=bw or 68, height=h,
                         selected_id=self.selected_task_id,
                         kanban_sort=self.kanban_sort,
                         kanban_group=self.kanban_group,
                         kanban_collapsed=self.kanban_collapsed,
                         kanban_focus=self.focused_project_id,
                         gantt_focus=self.focused_project_id,
                         presentation=presentation,
                         focus_presentation=self.focus_presentation,
                         team_state=self.team_state,
                         team_filter=self.team_filter)

    def _nav_flat(self) -> list[str]:
        return [tid for col in self._nav_columns() for tid in col]

    def _select_first(self) -> None:
        """Selection must be a currently-visible task (data validity). It may
        not be individually navigable in a compact view (e.g. a non-first
        swimlane task) — navigation snaps to nav order on the next key."""
        board = self._view_board()
        tasks = board.visible_tasks(self.show_archived)
        if self.focused_project_id is not None and self.view_mode in ("kanban", "gantt"):
            # A focused board draws ONE project's cards; the selection may not
            # rest on a task the filter hides (hidden-but-navigable is the
            # F-3 trap in a new costume, HLR-008). The same holds in gantt.
            tasks = [t for t in tasks if t.project_id == self.focused_project_id]
        ids = [t.id for t in tasks]
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

    def _warn_history_error(self) -> None:
        """Surface a history-append failure once per distinct message.

        The global is left in place so the failure is discoverable; the app
        only nags the operator when the message changes."""
        err = history.HISTORY_ERROR
        if err and err != self._last_history_error:
            self.notify(err, title="Transition log", severity="warning")
            self._last_history_error = err

    def action_phase_move(self, delta: int) -> None:
        """`[` / `]` — move the selected task one phase back/forward, dated.

        The move routes through `set_task_phase`, the ONLY seat allowed to
        write the `phase_changed` stamp (assigning `task.phase` here would
        leave the stamp behind and momentum unknowable). Both ends clamp to a
        silent no-op: no wrap, no re-stamp, no save, no re-render — a key that
        did nothing by design says nothing."""
        task = self.selected_task
        if task is None:
            return
        idx = self.board.phase_index(task) + delta
        idx = max(0, min(idx, len(self.board.phases) - 1))
        snap = self._snapshot(task)      # BEFORE the mutation (LLR-010.1); a
        if self.board.set_task_phase(task, self.board.phases[idx]):
            self._undo_stack.append(snap)  # clamped end is a no-op — nothing
            self.board.save()              # executed, nothing recorded
            self._warn_history_error()
            self.refresh_view()

    def action_prio_cycle(self) -> None:
        """`!` — cycle the selected task's priority low→normal→high→low."""
        task = self.selected_task
        if task is None:
            return
        self._undo_stack.append(self._snapshot(task))
        task.priority = next_priority(task.priority)
        self.board.save()
        self.refresh_view()

    def action_toggle_blocked(self) -> None:
        """`b` — block the selected task (with a blocker task) or unblock it.

        Blocking asks "What blocks it?" when there are candidate tasks.  The
        operator can create a new blocker or pick an existing open task; the
        blocked task gets ``blocked=True`` and the blocker id appended to
        ``depends_on``.  Cancelling the prompt leaves no snapshot on the undo
        stack.  With no candidates (single-task board) the flag flips directly.
        Unblocking flips the flag back without asking, preserving ``depends_on``
        so undo can restore it."""
        task = self.selected_task
        if task is None:
            return
        if task.blocked:
            self._undo_stack.append(self._snapshot(task))
            task.blocked = False
            self.board.save()
            self.refresh_view()
            return
        candidates = [t for t in self.board.tasks
                      if t is not task
                      and not self.board.is_done(t)
                      and not t.archived]
        if not candidates:
            # no candidate blocker -> plain flip, no prompt
            self._undo_stack.append(self._snapshot(task))
            task.blocked = True
            self.board.save()
            self.refresh_view()
            return
        self.push_screen(BlockerPicker(self.board, task.id),
                         lambda result: self._on_blocker_picked(task, result))

    def _on_blocker_picked(self, task: Task, result: str | None) -> None:
        """Commit the blocker choice: cancelled prompts leave no snapshot."""
        if result is None:
            return
        if result == "__new__":
            self.push_screen(TextPrompt("New blocker title", placeholder="title"),
                             lambda title: self._on_new_blocker(task, title))
            return
        blocker = self.board.task_by_id(result)
        if blocker is None:
            return
        self._undo_stack.append(self._snapshot(task))
        task.blocked = True
        task.depends_on = [*task.depends_on, blocker.id]
        self.board.save()
        self.refresh_view()

    def _on_new_blocker(self, task: Task, title: str | None) -> None:
        """Create a new blocker task, persist it, and link it."""
        if not title:
            return
        self._undo_stack.append(self._snapshot(task))
        phase = self.board.phases[0] if self.board.phases else "Backlog"
        blocker = Task(title, project_id=task.project_id, phase=phase)
        self.board.add_task(blocker)
        task.blocked = True
        task.depends_on = [*task.depends_on, blocker.id]
        self.board.save()
        self.refresh_view()

    def action_due_bump(self, delta: int) -> None:
        """`+` / `=` (delta +1 — ONE aliased seat entry, §6.5 AMD-06) and `-`
        (delta −1): move the selected task's due date one day — from its own
        date, or from today when undated (LLR-009.1, the base lives in the
        `bump_due` seat). Not view-scoped: it acts on the selection, like the
        other quick keys."""
        task = self.selected_task
        if task is None:
            return
        self._undo_stack.append(self._snapshot(task))
        bump_due(task, delta, date.today())
        self.board.save()
        self.refresh_view()

    # ---- undo (LLR-010.1: a session LIFO of single-task snapshots) ---------
    # The covered domain is EXACTLY the quick keys of §3.0 plus archive `x`
    # and delete `d` (§6.5 AMD-05). Collapse/sort/group/focus are VIEW state —
    # they mutate nothing, so there is nothing to undo. A modal add records
    # NOTHING: creation is deliberate, deletion covers the destructive path.
    _UNDO_FIELDS = ("phase", "phase_changed", "priority", "blocked",
                    "due_date", "archived", "pinned", "depends_on")

    def _snapshot(self, task: Task, *, deleted: bool = False) -> dict:
        """The pre-mutation state of ONE task: the six mutable fields VERBATIM
        — the stamp included, because restoring `phase` without `phase_changed`
        would fabricate a fresh-looking card (the models.py:1016 honesty rule).
        A delete keeps the FULL task object and its position, so the
        resurrection brings back the SAME id — a copy with a new id would
        break line_map, nav and every later undo."""
        fields: dict[str, object] = {}
        for f in self._UNDO_FIELDS:
            v = getattr(task, f)
            if f == "depends_on":
                v = list(v)          # snapshot as a COPY; the blocked flow mutates the list
            fields[f] = v
        entry = {"task_id": task.id, "fields": fields}
        if deleted:
            entry["task"] = task
            entry["index"] = self.board.tasks.index(task)
        return entry

    def action_undo(self) -> None:
        """`u` — restore the most recent not-yet-undone single-task mutation.

        LIFO, and an undo is NOT a new mutation (it pushes nothing, so `u`
        after `u` walks the stack down, never oscillates). A deleted task
        counts as restorable — its full snapshot re-inserts it with its
        original id; an entry whose task was PURGED since the snapshot (the
        one destructive route undo does not cover) is skipped; an empty or
        fully-stale stack says so through the notification channel and
        writes nothing."""
        while self._undo_stack:
            entry = self._undo_stack.pop()
            task = self.board.task_by_id(entry["task_id"])
            if task is None:
                gone = entry.get("task")
                if gone is None:
                    continue            # purged since the snapshot: stale, skip
                idx = min(entry["index"], len(self.board.tasks))
                self.board.tasks.insert(idx, gone)   # SAME object, SAME id
                task = gone
            else:
                for f, v in entry["fields"].items():
                    setattr(task, f, v)
            self.board.save()
            self.selected_task_id = task.id
            self.refresh_view()
            return
        self.notify("Nothing to undo.", title="Undo", severity="information")

    # ---- rendering ---------------------------------------------------------
    def _view_board(self) -> Board:
        """The board the CURRENT view renders from: the real board, or a shallow
        filtered copy when a search query is active in kanban/gantt."""
        if not self.search_query or self.view_mode not in ("kanban", "gantt"):
            return self.board
        return filtered_board(self.board, self.search_query, self.show_archived)

    def _validate_focus(self) -> None:
        """A focus naming a project that is no longer visible — archived or
        deleted mid-session — drops to off on the next refresh (LLR-008.1),
        never strands the board behind a filter nothing can leave."""
        if self.focused_project_id is None:
            return
        visible = {p.id for p in self.board.visible_projects(self.show_archived)}
        if self.focused_project_id not in visible:
            self.focused_project_id = None

    def refresh_view(self) -> None:
        self._validate_focus()
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
                              presentation=self.kanban_presentation, tick=self._tick_n,
                              kanban_sort=self.kanban_sort,
                              kanban_group=self.kanban_group,
                              kanban_collapsed=self.kanban_collapsed,
                              kanban_focus=self.focused_project_id,
                              gantt_focus=self.focused_project_id,
                              lanes_presentation=self.lanes_presentation,
                              focus_presentation=self.focus_presentation,
                              search_query=self.search_query,
                              team_state=self.team_state,
                              team_filter=self.team_filter)
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
            self._refresh_keybar()      # the bar states the CURRENT view's keys
            self.refresh_view()

    def action_team_filter_cycle(self) -> None:
        """Cycle the team-view classification filter: todo → equipo → personal.

        The filter is session-level and survives view hops. It affects both
        team views (V3 standup and V2 people lanes)."""
        modes = ("todo", "equipo", "personal")
        self.team_filter = modes[(modes.index(self.team_filter) + 1) % len(modes)]
        self.refresh_view()

    def _refresh_keybar(self) -> None:
        bars = self.query("#keybar")
        if bars:
            bars.first(KeyBar).refresh_bar(self.view_mode)

    def action_toggle_presentation(self) -> None:
        """Tab flips the kanban layout, cycles the Focus Board presentations,
        or switches swimlanes grid/waves; a no-op elsewhere."""
        if self.view_mode == "kanban":
            modes = ("grouped", "matrix", "lanes")
            self.kanban_presentation = modes[(modes.index(self.kanban_presentation) + 1)
                                             % len(modes)]
            self.refresh_view()
        elif self.view_mode == "focus":
            modes = ("tiles", "inspector", "images", "review", "stale")
            self.focus_presentation = modes[(modes.index(self.focus_presentation) + 1)
                                            % len(modes)]
            self.refresh_view()
        elif self.view_mode == "swimlanes":
            modes = ("grid", "waves")
            self.lanes_presentation = modes[(modes.index(self.lanes_presentation) + 1)
                                            % len(modes)]
            self.refresh_view()

    def action_pin_toggle(self) -> None:
        """`t` — pin/unpin the selected task so it appears in the Focus Board."""
        task = self.selected_task
        if task is None:
            return
        self._undo_stack.append(self._snapshot(task))
        task.pinned = not task.pinned
        self.board.save()
        self.refresh_view()

    def action_project_pin_toggle(self) -> None:
        """`T` — pin/unpin the whole project of the selected task."""
        task = self.selected_task
        if task is None:
            return
        proj = self.board.project_by_id(task.project_id)
        if proj is None:
            self.notify("Inbox tasks have no project to pin.", title="Pin project",
                        severity="information")
            return
        proj.pinned = not proj.pinned
        self.board.save()
        shown = escape(clip(proj.name, 40))
        self.notify(f'"{shown}" {"pinned" if proj.pinned else "unpinned"}',
                    title="Pin project", severity="information")
        self.refresh_view()

    def action_kanban_sort(self) -> None:
        """`s` — cycle the kanban column sort project→priority→due→recent→unblock;
        a no-op in every other view (the bar never advertises it there)."""
        if self.view_mode != "kanban":
            return
        modes = ("project", "priority", "due", "recent", "unblock")
        self.kanban_sort = modes[(modes.index(self.kanban_sort) + 1) % len(modes)]
        self.refresh_view()

    def action_kanban_group(self) -> None:
        """`g` — cycle the kanban column grouping project→priority→horizon;
        a no-op in every other view (same guard as the sort cycle)."""
        if self.view_mode != "kanban":
            return
        modes = ("project", "priority", "horizon")
        self.kanban_group = modes[(modes.index(self.kanban_group) + 1) % len(modes)]
        self.refresh_view()

    def action_collapse_toggle(self) -> None:
        """`z` — collapse THE LAST phase column to one `✓ N` summary row, or
        restore it. Session-level, needs NO selection, fires from anywhere in
        the kanban view (§6.5 AMD-02: the target is positional — the last
        phase in `board.phases` — never the selected task's phase); a no-op
        in every other view (same guard as the sort/group cycles)."""
        if self.view_mode != "kanban":
            return
        self.kanban_collapsed = not self.kanban_collapsed
        if self.kanban_collapsed:
            self._relocate_out_of_collapsed()
        self.refresh_view()

    def _relocate_out_of_collapsed(self) -> None:
        """A selection inside the just-collapsed terminal phase moves to the
        nearest visible task — the nearest non-empty column's FIRST card, the
        exact `action_hmove` landing rule — so the cursor never rests on a
        task the board no longer draws (HLR-007/LLR-007.1)."""
        task = self.selected_task
        if task is None or self.board.phase_index(task) != len(self.board.phases) - 1:
            return
        for col in reversed(self._nav_columns()):   # terminal phase already absent
            if col:
                self.selected_task_id = col[0]
                return
        self.selected_task_id = None

    def action_focus_cycle(self) -> None:
        """`F` — cycle the project focus through the visible projects in
        `board.visible_projects` order and then OFF (None); live in kanban and
        gantt, a view-guarded no-op elsewhere. Inbox is not a focus target
        (§6.2 D-5): focusing hides project-less tasks along with every other
        project. The filter itself lives in the shared ordering seat — this
        only holds the input."""
        if self.view_mode not in ("kanban", "gantt"):
            return
        ids = [p.id for p in self.board.visible_projects(self.show_archived)]
        cycle = ids + [None]
        try:
            nxt = cycle[(cycle.index(self.focused_project_id) + 1) % len(cycle)]
        except ValueError:
            nxt = cycle[0]              # a stale focus restarts the walk
        self.focused_project_id = nxt
        self.refresh_view()

    def action_focus_exit(self) -> None:
        """escape — clear an ACTIVE search query first, then an ACTIVE project
        focus in kanban or gantt, and do NOTHING otherwise (§6.5 AMD-03)."""
        if self.view_mode not in ("kanban", "gantt"):
            return
        if self.search_query:
            self.search_query = None
            self.refresh_view()
            return
        if self.focused_project_id is None:
            return
        self.focused_project_id = None
        self.refresh_view()

    def action_search(self) -> None:
        """`/` — prompt for a live filter query; applies to kanban and gantt.

        An empty query clears the filter. The filtered board is a shallow copy,
        so the underlying data is never touched."""
        if self.view_mode not in ("kanban", "gantt"):
            return
        self.push_screen(TextPrompt("Filter tasks", initial=self.search_query or "",
                                    placeholder="type to filter…"),
                         self._on_search_set)

    def _on_search_set(self, query: str | None) -> None:
        """Apply the filter query, treating an empty string as 'clear'."""
        if query is None:
            return
        self.search_query = query.strip() or None
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
            if k == "phase":
                # routed through the board so the move is DATED; assigning it
                # here would leave the stamp behind and momentum unknowable
                self.board.set_task_phase(task, v)
                continue
            setattr(task, k, v)
        self.board.save()
        self._warn_history_error()
        self.refresh_view()

    def action_purge_done(self) -> None:
        """`X` — the ONE-TIME archive of finished work the board has no date for.

        Deliberate, never automatic: it says how many it is about to move and
        waits for a yes. The standing 20-day sweep cannot reach these tasks —
        an undated task is not old — so this is the only way they leave the
        board, and it is the user's decision rather than a timer's."""
        pending = self.board.unstamped_done()
        if not pending:
            self.notify("No finished tasks are missing a completion date.",
                        title="Nothing to archive", severity="information")
            return
        self.push_screen(
            ConfirmModal(f"{len(pending)} finished task(s) have no completion "
                         "date, so the automatic sweep can never archive them. "
                         "Archive them now? They go to the normal archive — "
                         "'v' shows them, 'x' brings one back.",
                         confirm="Archive", variant="warning"),
            self._on_purge_confirmed)

    def _on_purge_confirmed(self, ok: bool | None) -> None:
        if not ok:
            return
        moved = self.board.archive_unstamped_done()
        self.board.save()
        self.refresh_view()
        self.notify(f"{len(moved)} finished task(s) archived. Press 'v' to see "
                    "them, 'x' to bring one back.",
                    title="Archived", severity="information", timeout=8)

    def action_delete(self) -> None:
        task = self.selected_task
        if task is None:
            return
        self.push_screen(ConfirmModal(f"Delete '{task.title}'?"),
                        lambda ok, t=task: self._on_delete(t, ok))

    def _on_delete(self, task: Task, ok: bool) -> None:
        if not ok:
            return
        self._undo_stack.append(self._snapshot(task, deleted=True))
        self.board.delete_task(task.id)
        self.selected_task_id = None
        self.refresh_view()

    def action_archive(self) -> None:
        """`x` — put a task away, or bring it back. It SAYS SO EITHER WAY.

        The complaint this answers: with `v` off, archiving makes the row vanish,
        and a row vanishing is indistinguishable from a key that did nothing. The
        row disappearing IS the effect, but the screen never said which effect it
        was. So the app states the fact and names the way back — and since the
        batch-04 undo shipped, `u` also reverses it (LLR-010.1: archive is in
        the undo domain), so the pre-flip state is snapshotted first."""
        task = self.selected_task
        if task is None:
            return
        self._undo_stack.append(self._snapshot(task))
        task.archived = not task.archived
        self.board.save()
        # the title is the user's text and goes through the SAME escape the views
        # use: a title holding markup must never be able to render as markup here
        shown = escape(clip(task.title, 40))
        if task.archived:
            # WITH `v` OFF THE ROW LEAVES THE SCREEN, and the selection leaves
            # with it — so `x` on its own no longer targets this task. Saying
            # "x brings it back" there would be a promise the app does not keep.
            body = (f'"{shown}" archived · '
                    + ("x brings it back" if self.show_archived
                       else "v shows it, then x brings it back"))
        else:
            body = f'"{shown}" restored'
        self.notify(body, title="Archive", severity="information")
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
