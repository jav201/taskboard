"""The Textual application: view switching, selection, modals, one clock."""

from __future__ import annotations

import os
import webbrowser
from datetime import date
from pathlib import Path

from rich.text import Text
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.keys import format_key
from textual.screen import ModalScreen
from textual.widgets import Static

from . import history
from .models import (AUTO_ARCHIVE_DAYS, IMAGE_EXTS, Board, Project, Task,
                     archive_refusal, default_board_path, is_open, link_refusal,
                     milestone_candidates, milestones_marked, next_priority, parse_iso,
                     ready_messages, run_link_migration, run_milestone_offer,
                     set_milestone, strip_controls, waiting_ids,
                     CASCADE_MODES, apply_plan, plan_move, resolve_mode, restore,
                     snapshot)
from .modals import (ClockModal, GanttLinkMode, LinkPicker, CommandPalette, ConfirmModal,
                     HelpModal, ImageViewer, MilestoneOffer, PhaseEditor, ProjectModal,
                     ProjectPicker,
                     StandupModal, TaskDetails, TaskModal, TeamIdentityPicker, TextPrompt)
from .keymap import KeyBar, app_bindings, palette_commands
from .ribbon import Ribbon
from .team_sync import (TEAM_FILENAME, TeamState, _read_json, clean_roster,
                        probe_setup_health)
from .views import (clip, filtered_board, focus_tasks, gantt_group_key, group_key,
                    gantt_plan, nav_model, sort_by_due, fit, vis,
                    render_view, valid_url)

def _md(d: date) -> str:
    return f"{d:%b} {d.day}"


# The app's ONE shared clock. Every animated surface counts in these ticks, so
# the ambient's cycle length is this times the number of phases it rotates
# through — which is why the motion laws read it instead of assuming it.
TICK_SECONDS = 1.0

# Written into board.json the first time the renumbering notice is shown, so it
# is shown exactly once per board rather than at every launch.
RENUMBER_NOTICE_KEY = "seen_view_renumber_2026_07"

VIEW_ORDER = ["swimlanes", "agenda", "gantt", "kanban", "focus", "chainmap",
              "flow", "standup", "people", "setup"]
VIEW_KEYS = {"1": "swimlanes", "2": "agenda", "3": "gantt", "4": "kanban",
             "5": "focus", "6": "chainmap", "7": "flow", "8": "standup",
             "9": "people", "0": "setup"}


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
                       f"[b #e6edf7]{k:<{kw}}[/] [#c8d3de]{d}[/]", title)
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
        rows = [f"[b #e6edf7]KEYS[/]   [#8b98a5]{hint}[/]", ""]
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
        # the gantt group the selection is in, and the one before it: the
        # previous group stays open while it fits (answer UXV-2, HLR-207)
        self._gantt_group: str | None = None
        self._gantt_previous: str | None = None
        self._tick_n = 0                 # drives the gantt flow packet
        self._last_history_error: str | None = None  # suppress duplicate warnings
        self.team_sync_interval = team_sync_interval
        self.team_state: TeamState | None = None
        self.team_filter: str = "equipo"   # session-level classification filter
        self._setup_state: dict | None = None   # staged team config while in setup view
        self._pre_setup_view: str = "swimlanes"

    # keys that act on the BOARD. They stay live on pushed screens (e.g. a
    # modal) and were indicated by nothing. FALSE, not None: Textual drops a
    # binding from `active_bindings` only on `is False`; None leaves it listed
    # and merely disabled, i.e. a legend entry that does nothing.
    BOARD_ACTIONS = frozenset({
        "add_task", "add_project", "manage_projects", "manage_phases",
        "details", "edit", "delete", "archive", "purge_done", "report",
        "toggle_archived", "open_url", "open_images", "clocks",
        "phase_move", "prio_cycle", "toggle_blocked", "link",
        "kanban_sort", "kanban_group", "collapse_toggle",
        "focus_cycle", "focus_exit", "due_bump", "undo", "standup",
        "toggle_presentation", "cursor", "hmove",
        "pin_toggle", "project_pin_toggle", "milestone_toggle"})

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
        # FIRST, before any other write: the backup must hold the file as the
        # user left it (LLR-505.3) — the renumber notice and the sweep both save.
        if not self._migrate_links():
            return
        self._announce_renumbering()
        self._sweep_old_done()
        self._select_first()
        self.refresh_view()
        self._apply_clock_settings()
        # ONE shared clock interval for the whole app (never per-widget).
        self.set_interval(TICK_SECONDS, self._tick)
        self._warn_if_rescued()
        self._init_team_mode()
        # LAST: the one-time milestone offer covers whatever start opened (the
        # identity picker included) until it is answered (D-615)
        self._offer_milestones()

    def _offer_milestones(self) -> None:
        """The one-time milestone offer (HLR-605): nothing on an unreadable load or
        a marked board; a board with no candidate is marked silently (a failed write
        here says nothing — no offer was shown, D-616); otherwise the offer opens
        and its answer is applied. Quitting unanswered leaves the board unmarked."""
        if self.board.load_report.get("file_unreadable") or milestones_marked(self.board.settings):
            return
        cands = milestone_candidates(self.board)
        if not cands:
            run_milestone_offer(self.board, [])
            return
        self.push_screen(MilestoneOffer(self.board, cands, date.today()),
                         self._on_offer_answered)

    def _on_offer_answered(self, chosen: list | None) -> None:
        result = run_milestone_offer(self.board, list(chosen or []), date.today())
        if result is None:
            return
        if result.error is not None:
            self.notify(f"Milestone offer stopped: {result.error}. The board file was not "
                        "changed; the offer returns at the next start.",
                        title="Milestones", severity="error", timeout=30, markup=False)
            return
        late = (f" · {result.ineligible} no longer eligible" if result.ineligible else "")
        if result.changes:
            self._undo_stack.append({"milestones": [
                {"task_id": ch["task_id"],
                 "fields": {"milestone": False, "start_date": ch["start_before"],
                            "due_date": ch["due_before"]}}
                for ch in result.changes]})
            n = len(result.changes)
            self.notify(f"Milestones: {n} converted{late} · backup {result.backup} · u undo",
                        title="Milestones", timeout=30, markup=False)
        elif late:
            self.notify(f"Milestones: 0 converted{late}", title="Milestones", timeout=30,
                        markup=False)
        else:
            self.notify("Not now — this offer won't show again; M makes any task a "
                        "milestone.", title="Milestones", timeout=30, markup=False)
        self.refresh_view()

    def _migrate_links(self) -> bool:
        """The one-time link migration (HLR-505). Returns False when it failed:
        the board file was not touched, and the app stops rather than work on
        links that would be read with the wrong meaning (D-518). On success
        every changed task is one undo step, and the toast names the backup."""
        result = run_link_migration(self.board)
        if result is None:
            return True
        if result.error is not None:
            # a Text piece: the reason holds a file name, and Rich would parse a
            # str printed at exit as markup (S1)
            self.exit(return_code=1, message=Text(
                f"Link migration stopped: {result.error}. The board file was not changed. "
                "Free space or write access in the board's folder, or run "
                "taskboard --board on a copy."))
            return False
        if result.changes:
            self._undo_stack.append({"migration": [
                {"task_id": ch.task_id,
                 "fields": {"blocked": ch.before[0], "depends_on": list(ch.before[1])}}
                for ch in result.changes]})
            n = len(result.changes)
            self.notify(f"Links migrated: {n} task{'s' if n != 1 else ''} · "
                        f"backup {result.backup} · u undo",
                        title="Dependencies", severity="information", timeout=30,
                        markup=False)
        return True

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
            title="Archived old work", severity="information", timeout=8, markup=False)

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
                title="Board recovered", severity="error", timeout=10, markup=False)
        elif r.get("tasks_rescued") or r.get("projects_rescued"):
            n = r.get("tasks_rescued", 0) + r.get("projects_rescued", 0)
            self.notify(
                f"{n} item(s) had an unreadable format and were recovered "
                "(see their notes). Nothing was lost.",
                title="Tasks recovered", severity="warning", timeout=10, markup=False)

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
        team_file = self.team_state.shared_dir / TEAM_FILENAME
        if (not self.team_state.load_config() and team_file.exists()
                and _read_json(team_file) is None):          # unreadable, not incomplete
            self.notify(f"team.json in {shared_dir} could not be read; team sync waits "
                        "for a readable file.", title="Team sync", severity="warning",
                        markup=False)
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
                        severity="warning", markup=False)

    def _setup_config(self) -> dict:
        """The authoritative team config if team mode is active, else an empty
        dict."""
        if self.team_state is None:
            return {}
        return self.team_state.config or {}

    def _stage_setup_state(self) -> dict:
        """Snapshot the current team configuration into a staged dict used by
        the setup view.  Mutations edit the staged copy; nothing is written to
        disk until `ctrl+s` commits."""
        cfg = self._setup_config()
        shared_dir = self.board.settings.get("team_shared_dir", "")
        user_id = self.board.settings.get("team_user_id")
        interval = self.board.settings.get("team_sync_interval")
        if not isinstance(interval, int) or interval < 5:
            interval = max(5, int(self.team_sync_interval // 60))
        team_projects: dict = {}
        for p in cfg.get("projects", []):
            if isinstance(p, dict) and isinstance(p.get("id"), str):
                team_projects.setdefault(p["id"], p)     # the first entry of an id wins
        projects = []
        for proj in self.board.projects:
            if proj.id in team_projects:
                # the board's values, which passed the loading rule when the
                # config was applied — never the raw synced ones (code review F3)
                template = team_projects[proj.id].get("template")
                projects.append({
                    "id": proj.id,
                    "name": proj.name,
                    "color": proj.color,
                    "status": proj.status,
                    "template": template if isinstance(template, str) else "",
                    "shared": True,
                })
            else:
                projects.append({
                    "id": proj.id,
                    "name": proj.name,
                    "color": proj.color,
                    "status": proj.status,
                    "template": "",
                    "shared": False,
                })
        roster = [{"id": r["id"], "name": r["name"], "hue": r["hue"]}
                  for r in clean_roster(cfg.get("roster", []))]
        return {
            "enabled": self.team_state is not None,
            "shared_dir": str(shared_dir) if shared_dir else "",
            "interval_minutes": min(120, max(5, interval)),
            "user_id": user_id,
            "projects": projects,
            "roster": roster,
            "cursor_section": 0,
            "cursor_row": 0,
        }

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
                              gantt_previous=self._gantt_previous,
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
        """`?` — the per-view help modal: usage, legend, example and keys.

        From the help modal: `m` opens the full keymap, `?` opens the command
        palette.
        """
        size, board = self.size, self.board
        if self.view_mode == "gantt":
            # the gantt's legend is asked of the frame on screen: the panel's
            # size, the selection and the focus (code review F3)
            boards, vps = self.query("#board"), self.query("#viewport")
            if boards and vps:
                size = (boards.first().size.width or size[0],
                        vps.first().size.height or size[1])
            if self.search_query:     # render_view draws a filtered view 2 rows
                size = (size[0], max(1, size[1] - 2))   # shorter (its bar)
            board = self._view_board()
        self.push_screen(HelpModal(self.view_mode, board,
                                   today=date.today(), size=size,
                                   show_archived=self.show_archived,
                                   team_state=self.team_state,
                                   team_filter=self.team_filter,
                                   selected_id=self.selected_task_id,
                                   gantt_focus=self.focused_project_id,
                                   gantt_previous=self._gantt_previous,
                                   kanban_presentation=self.kanban_presentation,
                                   kanban_group=self.kanban_group,
                                   kanban_focus=self.focused_project_id))

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
        # `bar_layer`, not `layer`: Textual's own `layer` is the CSS layer
        # ("default"), so reading it kept the bar on primary for good
        # (code review F3, batch 2026-10-02-batch-02)
        keybar.set_layer("more" if keybar.bar_layer == "primary" else "primary")

    def action_report(self) -> None:
        """`R` — write an HTML report of the board beside the board file.

        It says where the file went and does NOT open it: opening a browser is
        an action the reader did not ask for, so it stays their move."""
        from .report import write_report
        out = write_report(self.board)
        self.notify(f"Report written to {out}", title="Report",
                    severity="information", timeout=10, markup=False)

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
        if self.view_mode == "kanban" and h and (self.search_query or "").strip():
            # `render_view` draws a filtered kanban two rows shorter (the `/`
            # bar); the grouped board's cap and window read the height, so the
            # nav asks the same question the renderer answered (D-312)
            h = max(1, h - 2)
        if self.view_mode == "kanban":
            presentation = self.kanban_presentation
        elif self.view_mode == "swimlanes":
            presentation = self.lanes_presentation
        else:
            presentation = "grouped"
        cols = nav_model(self.view_mode, board, self.show_archived,
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
        if self.view_mode == "chainmap":
            # CM-2/F-3: the map folds whole bands that do not fit -- the cursor
            # may rest only on the drawn (line_map) tiles.
            drawn = set(getattr(self, "_line_map", {}))
            cols = [[tid for tid in col if tid in drawn] for col in cols]
        return cols

    def _nav_flat(self) -> list[str]:
        return [tid for col in self._nav_columns() for tid in col]

    def _select_first(self) -> None:
        """Selection must be a currently-visible task (data validity). It may
        not be individually navigable in a compact view (e.g. a non-first
        swimlane task) — navigation snaps to nav order on the next key."""
        board = self._view_board()
        tasks = board.visible_tasks(self.show_archived)
        if self.view_mode == "focus":
            # The Focus Board draws ONLY pinned tasks and the tasks of pinned
            # projects; the selection may not rest on a card the view does
            # not draw — the F-3 law, same as the project-focus filter below.
            # Without this, `t` on the selected card removed it from the view
            # but left the cursor on it, and the next `t` toggled THAT hidden
            # card back instead of the one the user was looking at.
            tasks = focus_tasks(board, self.show_archived)
        elif (self.focused_project_id is not None
                and self.view_mode == "kanban"):
            # A focused board draws ONE project's cards; the selection may not
            # rest on a task the filter hides (hidden-but-navigable is the
            # F-3 trap in a new costume, HLR-008). The gantt's own seat
            # (`gantt_plan`, below) applies the focus itself.
            tasks = [t for t in tasks if t.project_id == self.focused_project_id]
        if self.view_mode == "gantt":
            # The gantt draws OPEN work only (rest work is its group's `✓n`),
            # so a done or archived selection would park the cursor on a row
            # the view does not draw (F-3). Move to the neighbour it had in
            # its group's draw order — one row away, so an extra `]` cannot
            # land on a distant task — else to the first task drawn.
            order = self._nav_flat()
            if self.selected_task_id in order:
                return
            sel = board.task_by_id(self.selected_task_id)

            def group_of(t):            # the plan's groups: a project, or the Inbox
                return t.project_id if board.project_by_id(t.project_id) else None
            group = [board.task_by_id(tid) for tid in order
                     if sel is not None and group_of(board.task_by_id(tid)) == group_of(sel)]
            if group:
                ranked = sort_by_due(group + [sel])
                i = ranked.index(sel)
                pick = ranked[i + 1] if i + 1 < len(ranked) else ranked[i - 1]
                self.selected_task_id = pick.id
            else:
                self.selected_task_id = order[0] if order else None
            return
        if self.view_mode == "chainmap":
            # The chain map draws only the LINKED tasks (an unlinked task is not
            # a tile): a selection on one would park the cursor on a tile the
            # view does not draw (F-3). Move to the first linked task in draw
            # order, else off.
            order = self._nav_flat()
            if self.selected_task_id not in order:
                self.selected_task_id = order[0] if order else None
            return
        if self.view_mode == "kanban":
            # a milestone is never a kanban card (LLR-603.1, D-614): the selection
            # moves to the first card of the nearest drawn column at or left of
            # its phase, in the presentation's own column order (the `z` rule)
            tasks = [t for t in tasks if not t.milestone]
            sel = board.task_by_id(self.selected_task_id)
            if sel is not None and sel.milestone:
                cols = [col for col in self._nav_columns() if col]     # built once (K-3)
                ph, best = board.phase_index(sel), None
                for col in cols:
                    if (cp := board.phase_index(board.task_by_id(col[0]))) <= ph:
                        if best is None or cp > best[0]:
                            best = (cp, col[0])
                first = cols[0][0] if cols else None
                self.selected_task_id = best[1] if best else first
        ids = [t.id for t in tasks]
        if self.selected_task_id not in ids:
            self.selected_task_id = ids[0] if ids else None
        if (self.selected_task_id is not None and self.view_mode == "kanban"
                and self.kanban_presentation == "grouped"):
            # The readable board COUNTS done work it cannot draw (the narrow or
            # collapsed rail, past `+N more`); a selection there would rest on
            # a card the screen does not show (F-3). It moves by the `z` rule:
            # the first card of the nearest column at or left of its phase
            # (HLR-310).
            cols = self._nav_columns()
            if not any(self.selected_task_id in col for col in cols):
                sel = board.task_by_id(self.selected_task_id)
                at = min(board.phase_index(sel), len(cols) - 1)
                self.selected_task_id = next(
                    (cols[i][0] for i in range(at, -1, -1) if cols[i]), None)

    def _locate(self, cols: list[list[str]]) -> tuple[int, int] | None:
        for ci, col in enumerate(cols):
            if self.selected_task_id in col:
                return ci, col.index(self.selected_task_id)
        return None

    @property
    def selected_task(self) -> Task | None:
        return self.board.task_by_id(self.selected_task_id)

    def action_cursor(self, delta: int) -> None:
        """Up/Down: move WITHIN the current column (no jump off the ends), or
        move the setup cursor up/down within the active section."""
        if self.view_mode == "setup" and self._setup_state is not None:
            section, row, max_rows = self._setup_cursor_item()
            new_row = max(0, min(max_rows - 1, row + delta))
            if new_row != row:
                self._setup_state["cursor_row"] = new_row
                self.refresh_view()
            return
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
            self.notify(err, title="Transition log", severity="warning", markup=False)
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
        kanban = self.view_mode == "kanban" and self.kanban_presentation == "grouped"
        was = self._locate(self._nav_columns()) if kanban else None
        waiting = waiting_ids(self.board)
        if self.board.set_task_phase(task, self.board.phases[idx]):
            self._undo_stack.append(snap)  # clamped end is a no-op — nothing
            self.board.save()              # executed, nothing recorded
            self._warn_history_error()
            if was is not None:
                cols = self._nav_columns()
                if not any(task.id in col for col in cols):
                    # the board counts the task now (a narrow rail): the card
                    # that took its place takes the cursor, else the one above
                    # (HLR-310 — the gantt's neighbour rule, not the top)
                    col = cols[was[0]] if was[0] < len(cols) else []
                    if col:
                        self.selected_task_id = col[min(was[1], len(col) - 1)]
            self.refresh_view()
            if self.view_mode == "gantt" and self.board.is_done(task):
                self._notify_folded(task)
            elif was is not None and self.selected_task_id != task.id:
                # only done work leaves the nav: the task was counted
                # board text: shown raw with markup OFF, never escaped (C-17)
                self.notify(f"{task.title} done · counted in the ✓ rail · u undo",
                            markup=False)
            self._say_ready(waiting, task)

    def _say_ready(self, waiting_before: set[str], task: Task) -> None:
        """When `task` has just reached the last phase, say once which waiting
        tasks it let go (LLR-501.4). Titles are board text: raw, markup OFF."""
        if not self.board.is_done(task):
            return
        for line in ready_messages(self.board, waiting_before, {task.id}):
            self.notify(line, title="Ready", severity="information", markup=False)

    def _refuse(self, task: Task, verb: str, extra: str = "") -> bool:
        """The guard (HLR-504): an open task that open tasks wait on is not
        archived or deleted. True when refused — said with the waiters named."""
        why = archive_refusal(self.board, task, verb)
        if why is None:
            return False
        self.notify(why + extra, title="Links", severity="warning", markup=False)
        return True

    def _notify_folded(self, task: Task) -> None:
        """A task `]` finished has left the gantt — it folded into its group's
        `✓n`. Say so, once, with the way back (answer D14, HLR-206). The title is
        board text: shown raw with markup OFF, never escaped (security S-1)."""
        group = gantt_group_key(self.board, task)
        board = self._view_board()
        g = next((g for g in gantt_plan(board, self.show_archived, None, date.today(),
                                        10 ** 6, self.focused_project_id)
                  if group_key(g.project) == group), None)
        if task.milestone and g is not None and any(t is task for t in g.rows):
            # a reached milestone stays drawn among its group's rows (D-606, D-614)
            self.notify(f"{clip(task.title, 40)} reached · ◆✓ · u undo", markup=False)
            return
        rest = len(g.rest) if g is not None else 0
        self.notify(f"{task.title} done · folded into ✓{rest} · u undo", markup=False)

    def action_prio_cycle(self) -> None:
        """`!` — cycle the selected task's priority low→normal→high→low."""
        task = self.selected_task
        if task is None:
            return
        self._undo_stack.append(self._snapshot(task))
        task.priority = next_priority(task.priority)
        self.board.save()
        self.refresh_view()

    def action_milestone_toggle(self) -> None:
        """`M` — the selected task becomes a milestone (one date, its due) or a
        task again (LLR-601.2). A task with no date is refused and nothing is
        written; otherwise ONE undo step, taken before the change, and a toast
        saying where the milestone now shows."""
        task = self.selected_task
        if task is None:
            return
        snap = self._snapshot(task)
        old_start = parse_iso(task.start_date)
        err = set_milestone(task, not task.milestone)
        if err:
            self.notify(err, title="Milestone", severity="warning", markup=False)
            return
        self._undo_stack.append(snap)
        self.board.save()
        self.refresh_view()
        name = clip(task.title, 40)
        if not task.milestone:
            self.notify(f"{name} is a task again · u undo", title="Milestone", markup=False)
            return
        day = parse_iso(task.due_date)
        moved = (f" · start was {_md(old_start)}"
                 if old_start is not None and old_start != day else "")
        self.notify(f"{name} is a milestone · ◆ {_md(day)}{moved} · "
                    f"{self._milestone_where(task)} · u undo",
                    title="Milestone", markup=False)

    def _milestone_where(self, task: Task) -> str:
        """Where a milestone shows: on its project's kanban band only when that
        band is drawn here — the grouped project grouping and a project that
        still has an open card that is not a milestone (D-607, D-623)."""
        p = self.board.project_by_id(task.project_id)
        if (self.view_mode == "kanban" and self.kanban_presentation == "grouped"
                and self.kanban_group == "project" and p is not None
                and any(t.project_id == p.id and not t.milestone
                        and is_open(self.board, t) for t in self.board.tasks)):
            return f"on the {p.name} band"
        return "shown on the gantt"

    def _apply_editor_milestone(self, task: Task, want: bool,
                                prior_start: str | None = None,
                                was_milestone: bool = False) -> None:
        """The editor's milestone box, applied AFTER every other field (LLR-601.3):
        the due is the date, so a start that differs from it is replaced — and said
        when the task BECOMES a milestone or the user changed the start field (an
        existing milestone's untouched start field, still showing its old date, is
        not news: code review F-4, F2-1); a box ticked on a task with no date leaves
        it a task, and says so."""
        if not want:
            set_milestone(task, False)
            return
        start, due = parse_iso(task.start_date), parse_iso(task.due_date)
        if set_milestone(task, True):
            task.milestone = False
            self.notify("not a milestone — a milestone needs a date (other changes saved)",
                        title="Milestone", severity="warning", markup=False)
        elif (start is not None and due is not None and start != due
                and (not was_milestone or start != parse_iso(prior_start))):
            self.notify(f"milestone: the start follows the due ({_md(due)})",
                        title="Milestone", markup=False)

    def action_toggle_blocked(self) -> None:
        """`b` — the EXTERNAL block (`▲`): a block with no task to point at.
        It flips the flag and nothing else; waiting on another task is a link
        (`L`), never this flag (HLR-501, D-504)."""
        task = self.selected_task
        if task is None:
            return
        self._undo_stack.append(self._snapshot(task))
        task.blocked = not task.blocked
        self.board.save()
        self.refresh_view()

    # ---- links: `L` (HLR-502, LLR-502.1) -------------------------------------
    def action_link(self) -> None:
        """`L` — "this task waits on…": the picker (D-B2), or in the gantt the
        link mode drawn on the chart (D-A). Nothing without a selected task."""
        task = self.selected_task
        if task is None:
            return
        if self.view_mode == "gantt":
            self.push_screen(GanttLinkMode(self.board, task, self.show_archived, date.today()),
                             lambda result: self._on_link_picked(task, result))
        else:
            self.open_link_picker(task)

    def open_link_picker(self, waiter: Task, after=None) -> None:
        self.push_screen(LinkPicker(self.board, waiter),
                         lambda result: self._on_link_picked(waiter, result, after))

    def _on_link_picked(self, waiter: Task, result, after=None) -> None:
        if result:
            kind, value = result
            pred = self.board.task_by_id(value)
            if kind == "link" and pred is not None:
                self.link_tasks(waiter, pred)
            elif kind == "unlink" and pred is not None:
                self.unlink_tasks(waiter, pred)
            elif kind == "new":
                self._create_and_link(waiter, value)
            elif kind == "ask":
                self.push_screen(TextPrompt("New task it waits on", placeholder="title"),
                                 lambda title: self._ask_done(waiter, title, after))
                return
        if after is not None:
            after()

    def _ask_done(self, waiter: Task, title: str | None, after=None) -> None:
        if title:
            self._create_and_link(waiter, title)
        if after is not None:
            after()

    def link_tasks(self, waiter: Task, pred: Task) -> bool:
        """Add the link `waiter` waits on `pred` — refused with the reason when it
        is the task itself, a closed task or a loop (named by its path). One
        undo step. Titles are board text: raw, markup OFF (S1)."""
        why = link_refusal(self.board, waiter, pred)
        if why is not None:
            self.notify(why, title="Links", severity="warning", markup=False)
            return False
        if pred.id in waiter.depends_on:
            return False
        self._undo_stack.append(self._snapshot(waiter))
        waiter.depends_on = [*waiter.depends_on, pred.id]
        self.board.save()
        self.refresh_view()
        self.notify(f"{clip(waiter.title, 40)} waits on {clip(pred.title, 40)} · u undo",
                    title="Links", markup=False)
        return True

    def unlink_tasks(self, waiter: Task, pred: Task) -> None:
        """Remove the link `waiter` waits on `pred`. One undo step."""
        if pred.id not in waiter.depends_on:
            return
        self._undo_stack.append(self._snapshot(waiter))
        waiter.depends_on = [x for x in waiter.depends_on if x != pred.id]
        self.board.save()
        self.refresh_view()
        self.notify(f"{clip(waiter.title, 40)} no longer waits on {clip(pred.title, 40)} "
                    "· u undo", title="Links", markup=False)

    def _chainmap_unlink(self) -> None:
        """`x` on the chain map (LLR-801.2): remove the selected task's FIRST
        incoming link through the shipped `unlink_tasks` seat; when it waits on
        nothing, refuse with the verbatim toast and write nothing."""
        task = self.selected_task
        if task is None:
            return
        pred = self.board.task_by_id(task.depends_on[0]) if task.depends_on else None
        if pred is None:
            self.notify("nothing to remove — the selection waits on no task",
                        title="Links", severity="warning", markup=False)
            return
        self.unlink_tasks(task, pred)

    def _create_and_link(self, waiter: Task, title: str) -> None:
        """The picker's create row: a new task in the waiter's project, first
        phase, no dates, and the link to it. `u` takes the link back; the task
        stays (a modal add records nothing, LLR-010.1)."""
        title = strip_controls(title).strip()
        if not title:
            return
        if len(self.board.phases) < 2:
            # a one-phase board: its first phase is the last, so the new task
            # would be closed and the link refused (code review F4)
            self.notify("a one-phase board has no open phase to create it in",
                        title="Links", severity="warning", markup=False)
            return
        new = Task(title, project_id=waiter.project_id, phase=self.board.phases[0])
        self.board.add_task(new)
        self.link_tasks(waiter, new)

    def jump_to(self, task_id: str) -> None:
        """Select a linked task from the details view: focus and search are left
        so it can be drawn; archived work hidden by `v` is said, not jumped to."""
        task = self.board.task_by_id(task_id)
        if task is None:
            return
        if task.archived and not self.show_archived:
            self.notify(f"{clip(task.title, 40)} is archived — v shows it",
                        title="Links", markup=False)
            return
        self.focused_project_id = None
        self.search_query = None
        self.selected_task_id = task.id
        self.refresh_view()
        if self.selected_task_id != task.id:
            # this view does not draw it (finished work folded away, a view of
            # pinned work only): say so rather than select something else
            self.notify(f"{clip(task.title, 40)} is not drawn in this view",
                        title="Links", markup=False)

    def action_due_bump(self, delta: int) -> None:
        """`+` / `=` (delta +1 — ONE aliased seat entry, §6.5 AMD-06) and `-`
        (delta −1): move the selected task's due date one day — from its own
        date, or from today when undated (LLR-009.1, the base lives in the
        engine's today rule, `plan_move`). Not view-scoped: it acts on the selection, like the
        other quick keys. The move ROUTES THROUGH THE CASCADE (LLR-604.2,
        batch 2026-10-06-batch-01): the chain follows by the project's rule,
        the toast names what moved, and one `u` takes the whole move back."""
        task = self.selected_task
        if task is None:
            return
        self._apply_cascade(task, 0, delta)

    # ---- moving linked dates (batch 2026-10-06-batch-01) --------------------
    CASCADE_VERB = {"flag": "flagged", "push_delta": "pushed", "together": "moved",
                    "push": "pushed"}   # strict push: accepted, never offered

    @staticmethod
    def _short_title(t: str, n: int) -> str:
        words = t.split()
        if not words:
            return ""
        out = words[0]
        for w in words[1:]:
            if len(out) + 1 + len(w) > n:
                break
            out += " " + w
        return out

    def _cascade_toast(self, task: Task, plan, sd: int = 0) -> str:
        """The C-3 toast on the contract's ladder (§1.3), PLAIN TEXT: the shipped
        law is that no toast parses markup (TC-401), so the prototype frame's
        colours stay out — the text the contract pins is the whole toast. The
        dependents sort tolerates a planned `None` due (code review 1-1)."""
        width = self.screen.size.width
        deps = sorted((t for t in plan.moved if t != task.id
                       and plan.moved[t] != (None, None)),   # an undated dependent
                      key=lambda t: (plan.moved[t][1] is None, plan.moved[t][1] or date.min))
        nd = plan.moved[task.id][1]
        pr = self.board.project_by_id(task.project_id)
        over = plan.project_over.get(pr.id, 0) if pr else 0
        over_before = plan.project_over_before.get(pr.id, 0) if pr else 0

        def clause(names_w: int) -> str:
            if plan.mode == "flag":
                if not plan.new_conflicts:
                    return ""
                verb = self.CASCADE_VERB[plan.mode]
                if names_w:
                    names = ", ".join(self._short_title(
                        self.board.task_by_id(w).title, names_w)
                        for w, _, _ in plan.new_conflicts)
                    days = {n for _, _, n in plan.new_conflicts}
                    if len(days) == 1:
                        return f"{verb} {names} +{days.pop()}d"
                    return (f"{verb} {len(plan.new_conflicts)} overlaps (" + ", ".join(
                        f"{self._short_title(self.board.task_by_id(w).title, names_w)} +{n}d"
                        for w, _, n in plan.new_conflicts) + ")")
                days = sorted({n for _, _, n in plan.new_conflicts})
                if len(days) == 1:
                    return f"{verb} {len(plan.new_conflicts)} +{days[0]}d each"
                return f"{verb} {len(plan.new_conflicts)} overlaps (" + "/".join(
                    f"+{n}d" for n in days) + ")"
            if not deps:
                return ""
            shifts = {plan.shift[t] for t in deps}
            verb = self.CASCADE_VERB[plan.mode]
            if names_w and len(shifts) == 1:
                names = ", ".join(self._short_title(
                    self.board.task_by_id(t).title, names_w) for t in deps)
                return f"{verb} {names} {next(iter(shifts)):+d}d each"
            if names_w:
                names = ", ".join(f"{self._short_title(self.board.task_by_id(t).title, names_w)} "
                                  f"{plan.shift[t]:+d}d" for t in deps)
                return f"{verb} {len(deps)} dependents ({names})"
            if len(shifts) == 1:
                return f"{verb} {len(deps)} {next(iter(shifts)):+d}d each"
            return f"{verb} {len(deps)} (" + "/".join(f"{plan.shift[t]:+d}d"
                                                      for t in deps) + ")"

        def toast(title_w, names_w, proj_full, keys):
            title = task.title if title_w is None else fit(task.title, title_w).rstrip()
            moved_due = nd is not None and plan.shift[task.id] != 0
            lead = (f"▌{title} due {_md(nd)} ({plan.shift[task.id]:+d}d)" if moved_due
                    else f"▌{title} starts {_md(plan.moved[task.id][0])} ({sd:+d}d)")
            segs = [lead]
            mid = clause(names_w)
            if mid:
                segs.append(mid)
            if over > over_before:            # the project SLIPS FURTHER past its due
                pn = pr.name if proj_full else next(iter(pr.name.split()), "")
                segs.append(f"{pn} +{over}d past ◆")
            label = ("change for this move", "change", "")[keys]
            segs.append(" · ".join(f"{k} {v}" if v else k for k, v in
                                   [("u", "undo"), ("m", label)]))
            return " · ".join(segs)

        ladder = [(None, 12, True, 0), (None, 12, False, 0), (None, 12, False, 1),
                  (None, 8, False, 1), (None, 0, True, 0), (None, 0, True, 1),
                  (None, 0, False, 1), (12, 0, False, 1), (6, 0, False, 2)]
        row = next((r for a in ladder if vis(r := toast(*a)) <= width), toast(*ladder[-1]))
        if vis(row) > width:
            row = fit(row, width)
        return row

    def _apply_cascade(self, task: Task, sd: int, dd: int, *,
                       mode: str | None = None, say_solo: bool = True) -> None:
        """The ONE seat for a date move (LLR-604.2): plan against the resolved
        mode, snapshot, apply, push ONE multi-task undo entry, save (atomically
        when the write touches more than one task — D-634) and say it. The bump
        and `m` say every move (say_solo, the default); the EDITOR passes
        say_solo=False — LLR-604.3/D-629: its save stays silent unless the
        cascade moved others or `flag` added overlaps."""
        plan = plan_move(self.board, task.id, sd, dd,
                         mode or resolve_mode(self.board, task.id), date.today())
        snap = snapshot(self.board, plan)
        apply_plan(self.board, plan)
        self._undo_stack.append({"cascade": {
            "task_id": task.id, "sd": sd, "dd": dd, "mode": plan.mode,
            "tasks": [{"task_id": i, "fields": {"start_date": s, "due_date": d}}
                      for i, (s, d) in snap.items()]}})
        if len(plan.moved) > 1:
            self.board.save_atomic()
        else:
            self.board.save()
        self.refresh_view()
        if say_solo or len(plan.moved) > 1 or plan.new_conflicts:
            self.notify(self._cascade_toast(task, plan, sd), title="Move", markup=False)

    def action_cascade_mode(self) -> None:
        """`m` — re-apply the last date move under the next mode (LLR-604.4):
        flag → push_delta → together → flag. Works only while that move is the
        top of the undo stack; otherwise the refusal, verbatim, and nothing
        moves. The cycle never offers strict `push`. On the chain map the same
        key is view-dispatched: it cycles the selected task's PROJECT rule."""
        if self.view_mode == "chainmap":
            self._chainmap_cycle_rule()
            return
        entry = self._undo_stack[-1] if self._undo_stack else None
        if entry is None or "cascade" not in entry:
            self.notify("m re-applies the last date move — nothing to re-apply",
                        title="Move", severity="information", markup=False)
            return
        cas = entry["cascade"]
        task = self.board.task_by_id(cas["task_id"])
        if task is None:                       # C-5: the moved task is gone
            self.notify("m re-applies the last date move — nothing to re-apply",
                        title="Move", severity="information", markup=False)
            return
        self._undo_stack.pop()                 # undo the entry's writes first
        restore(self.board, {one["task_id"]: (one["fields"]["start_date"],
                                              one["fields"]["due_date"])
                             for one in cas["tasks"]})
        nxt = CASCADE_MODES[(CASCADE_MODES.index(cas["mode"]) + 1) % len(CASCADE_MODES)]
        self._apply_cascade(task, cas["sd"], cas["dd"], mode=nxt)

    def _chainmap_cycle_rule(self) -> None:
        """`m` on the chain map (LLR-802.1): cycle the selected task's PROJECT
        rule stay → push → together → stay via the shipped lenient read, write
        the STORED string to `extra["date_links"]`, save and refresh the footer.
        A setting, not a move — no undo entry, nothing tops the cascade stack."""
        task = self.selected_task
        if task is None:
            return
        pr = self.board.project_by_id(task.project_id)
        if pr is None:
            return
        mode = resolve_mode(self.board, task.id)
        nxt = CASCADE_MODES[(CASCADE_MODES.index(mode) + 1) % len(CASCADE_MODES)]
        pr.extra["date_links"] = nxt
        self.board.save()
        self.refresh_view()

    # ---- undo (LLR-010.1: a session LIFO of pre-mutation snapshots) --------
    # The covered domain is EXACTLY the quick keys of §3.0 plus archive `x`
    # and delete `d` (§6.5 AMD-05). Collapse/sort/group/focus are VIEW state —
    # they mutate nothing, so there is nothing to undo. A modal add records
    # NOTHING: creation is deliberate, deletion covers the destructive path.
    _UNDO_FIELDS = ("phase", "phase_changed", "priority", "blocked",
                    "due_date", "archived", "pinned", "depends_on",
                    "start_date", "milestone")

    def _snapshot(self, task: Task, *, deleted: bool = False) -> dict:
        """The pre-mutation state of ONE task: the `_UNDO_FIELDS` VERBATIM
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
        """`u` — restore the most recent not-yet-undone mutation (one task or
        a whole cascade move; the entry's shape says which).

        LIFO, and an undo is NOT a new mutation (it pushes nothing, so `u`
        after `u` walks the stack down, never oscillates). A deleted task
        counts as restorable — its full snapshot re-inserts it with its
        original id; an entry whose task was PURGED since the snapshot (the
        one destructive route undo does not cover) is skipped; an empty or
        fully-stale stack says so through the notification channel and
        writes nothing."""
        while self._undo_stack:
            entry = self._undo_stack.pop()
            if "milestones" in entry:
                # the whole conversion is ONE step; the mark stays (D-610)
                for one in entry["milestones"]:
                    t = self.board.task_by_id(one["task_id"])
                    if t is not None:
                        for f, v in one["fields"].items():
                            setattr(t, f, v)
                self.board.save()
                self.refresh_view()
                self.notify("Milestone conversion undone — the tasks are back as they were",
                            title="Undo", severity="information", markup=False)
                return
            if "migration" in entry:
                # the whole link migration is ONE step; the mark stays, so it
                # never runs again on its own (D-517)
                for one in entry["migration"]:
                    t = self.board.task_by_id(one["task_id"])
                    if t is not None:
                        for f, v in one["fields"].items():
                            setattr(t, f, list(v) if f == "depends_on" else v)
                self.board.save()
                self.refresh_view()
                self.notify("Links migration undone — the old links now read as waits.",
                            title="Undo", severity="information", markup=False)
                return
            if "cascade" in entry:
                # one date move is ONE step — every moved task's dates come back
                # together (LLR-604.2; a task purged since is skipped, the
                # shipped stale-entry rule)
                cas = entry["cascade"]
                restore(self.board, {one["task_id"]: (one["fields"]["start_date"],
                                                      one["fields"]["due_date"])
                                     for one in cas["tasks"]})
                if len(cas["tasks"]) > 1:
                    self.board.save_atomic()
                else:
                    self.board.save()
                self.refresh_view()
                return
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
        self._track_gantt_group()
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
                              gantt_previous=self._gantt_previous,
                              lanes_presentation=self.lanes_presentation,
                              focus_presentation=self.focus_presentation,
                              search_query=self.search_query,
                              team_state=self.team_state,
                              team_filter=self.team_filter,
                              setup_state=self._setup_state)
        board_widget.update(content)
        self._scroll_selected_into_view()

    def _track_gantt_group(self) -> None:
        """In the gantt, remember the selection's group and the one it was in
        before, so the plan can keep the group just left open (LLR-207.2)."""
        task = self.selected_task
        if self.view_mode != "gantt" or task is None:
            return
        group = gantt_group_key(self.board, task)
        if group != self._gantt_group:
            if self._gantt_group is not None:
                self._gantt_previous = self._gantt_group
            self._gantt_group = group

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
        if mode not in VIEW_ORDER:
            return
        if mode == "setup":
            self._pre_setup_view = self.view_mode
            self._setup_state = self._stage_setup_state()
        self.view_mode = mode
        self._refresh_keybar()      # the bar states the CURRENT view's keys
        self.refresh_view()

    def action_setup_exit(self) -> None:
        """`esc` in setup view: discard staged changes and return."""
        self._setup_state = None
        self.view_mode = self._pre_setup_view
        self._refresh_keybar()
        self.refresh_view()

    def action_setup_save(self) -> None:
        """`ctrl+s` in setup view: commit staged changes to team.json and
        board.settings, then sync and return to the previous view."""
        if self._setup_state is None:
            return
        state = self._setup_state
        enabled = state.get("enabled", False)
        shared_dir = state.get("shared_dir", "").strip()
        interval_minutes = state.get("interval_minutes", 30)
        user_id = state.get("user_id")

        self.board.settings["team_shared_dir"] = shared_dir if enabled else ""
        self.board.settings["team_user_id"] = user_id if enabled else None
        self.board.settings["team_sync_interval"] = interval_minutes

        if enabled and shared_dir:
            from .team_sync import _write_json
            path = Path(shared_dir)
            path.mkdir(parents=True, exist_ok=True)
            team_json_path = path / "team.json"
            # through the sync door: the phases and template republished below
            # come from a teammate's file (P2 A-3)
            existing = _read_json(team_json_path)
            version = 1
            if isinstance(existing, dict) and isinstance(existing.get("version"), int):
                version = existing["version"] + 1

            team_projects = []
            for p in state.get("projects", []):
                if not p.get("shared"):
                    continue
                team_projects.append({
                    "id": p.get("id"),
                    "name": p.get("name"),
                    "color": p.get("color"),
                    "status": p.get("status", "on_track"),
                    "template": p.get("template", ""),
                })
            team_data = {
                "version": version,
                "phases": (existing.get("phases") if isinstance(existing, dict) else None)
                           or ["Backlog", "Doing", "Review", "Done"],
                "template": (existing.get("template") if isinstance(existing, dict) else None)
                            or {"fields": ["title", "assignee", "due", "priority"]},
                "projects": team_projects,
                "roster": [{"id": r.get("id"), "name": r.get("name"), "hue": r.get("hue", "mut")}
                           for r in state.get("roster", [])],
                "sync_tolerance_minutes": interval_minutes,
            }
            _write_json(team_json_path, team_data)

            # Re-initialize team state with new settings and sync once.
            self.team_state = TeamState.from_settings(shared_dir, user_id)
            if self.team_state is not None:
                self.team_state.load_config()
                self.team_state.user_id = user_id
                self._run_team_sync()

        self.board.save()
        self._setup_state = None
        self.view_mode = self._pre_setup_view
        self._refresh_keybar()
        self.refresh_view()

    def _setup_cursor_item(self) -> tuple[str, int, int]:
        """Return (section_name, row_index, max_rows) for the current setup cursor."""
        if self._setup_state is None:
            return ("", 0, 0)
        sec = self._setup_state.get("cursor_section", 0)
        row = self._setup_state.get("cursor_row", 0)
        equipo_max = 5
        proj_max = max(1, len(self._setup_state.get("projects", [])))
        roster_max = max(1, len(self._setup_state.get("roster", [])))
        if sec == 0:
            return ("equipo", row, equipo_max)
        if sec == 1:
            return ("proyectos", row, proj_max)
        return ("roster", row, roster_max)

    def action_setup_section(self) -> None:
        """`tab` cycles the active section in setup."""
        if self._setup_state is None:
            return
        self._setup_state["cursor_section"] = (self._setup_state.get("cursor_section", 0) + 1) % 3
        self._setup_state["cursor_row"] = 0
        self.refresh_view()

    def action_setup_edit(self) -> None:
        """`enter` edits the selected setup row."""
        if self._setup_state is None:
            return
        section, row, _ = self._setup_cursor_item()
        if section == "equipo" and row == 1:
            self.push_screen(TextPrompt("Shared directory", placeholder="path",
                                        initial=self._setup_state.get("shared_dir", "")),
                             self._on_setup_folder_edited)
        elif section == "equipo" and row == 3:
            self.push_screen(TextPrompt("Sync interval (minutes)", placeholder="5..120",
                                        initial=str(self._setup_state.get("interval_minutes", 30))),
                             self._on_setup_interval_edited)
        elif section == "proyectos":
            projects = self._setup_state.get("projects", [])
            if 0 <= row < len(projects):
                self.push_screen(TextPrompt("Project name", placeholder="name",
                                            initial=projects[row].get("name", "")),
                                 lambda name: self._on_setup_project_name_edited(row, name))
        elif section == "roster":
            roster = self._setup_state.get("roster", [])
            if 0 <= row < len(roster):
                self.push_screen(TextPrompt("Member name", placeholder="name",
                                            initial=roster[row].get("name", "")),
                                 lambda name: self._on_setup_member_name_edited(row, name))

    def _on_setup_folder_edited(self, value: str | None) -> None:
        if value is None or self._setup_state is None:
            return
        self._setup_state["shared_dir"] = value.strip()
        self.refresh_view()

    def _clamp_interval(self, value: str | None) -> int | None:
        """Parse and clamp a setup interval string to 5..120 minutes."""
        if value is None:
            return None
        try:
            minutes = int(value.strip())
        except ValueError:
            return None
        return min(120, max(5, minutes))

    def _on_setup_interval_edited(self, value: str | None) -> None:
        if self._setup_state is None:
            return
        minutes = self._clamp_interval(value)
        if minutes is None:
            return
        self._setup_state["interval_minutes"] = minutes
        self.refresh_view()

    def _on_setup_project_name_edited(self, idx: int, value: str | None) -> None:
        if value is None or self._setup_state is None:
            return
        projects = self._setup_state.get("projects", [])
        if 0 <= idx < len(projects):
            projects[idx]["name"] = value.strip() or projects[idx].get("id", "")
            self.refresh_view()

    def _on_setup_member_name_edited(self, idx: int, value: str | None) -> None:
        if value is None or self._setup_state is None:
            return
        roster = self._setup_state.get("roster", [])
        if 0 <= idx < len(roster):
            roster[idx]["name"] = value.strip() or roster[idx].get("id", "")
            self.refresh_view()

    def action_setup_toggle(self) -> None:
        """`space` toggles the selected setup control."""
        if self._setup_state is None:
            return
        section, row, _ = self._setup_cursor_item()
        if section == "equipo" and row == 0:
            self._setup_state["enabled"] = not self._setup_state.get("enabled", False)
        elif section == "equipo" and row == 4:
            # cycle identity through roster + None
            roster = self._setup_state.get("roster", [])
            ids = [None] + [r.get("id") for r in roster if r.get("id")]
            current = self._setup_state.get("user_id")
            try:
                nxt = ids[(ids.index(current) + 1) % len(ids)]
            except ValueError:
                nxt = ids[0] if ids else None
            self._setup_state["user_id"] = nxt
        elif section == "proyectos":
            projects = self._setup_state.get("projects", [])
            if 0 <= row < len(projects):
                projects[row]["shared"] = not projects[row].get("shared", False)
        self.refresh_view()

    def action_setup_add(self) -> None:
        """`a` adds a roster member or project in setup."""
        if self._setup_state is None:
            return
        section, row, _ = self._setup_cursor_item()
        if section == "roster":
            self.push_screen(TextPrompt("New member id", placeholder="id"),
                             self._on_setup_member_added)
        elif section == "proyectos":
            self.push_screen(TextPrompt("New project id", placeholder="id"),
                             self._on_setup_project_added)

    def _on_setup_member_added(self, value: str | None) -> None:
        if not value or self._setup_state is None:
            return
        uid = value.strip().lower()
        roster = self._setup_state.setdefault("roster", [])
        if any(r.get("id") == uid for r in roster):
            self.notify(f"Member '{uid}' already exists.", title="Setup",
                        severity="warning", markup=False)
            return
        roster.append({"id": uid, "name": uid, "hue": "mut"})
        self.refresh_view()

    def _on_setup_project_added(self, value: str | None) -> None:
        if not value or self._setup_state is None:
            return
        pid = value.strip().lower()
        projects = self._setup_state.setdefault("projects", [])
        if any(p.get("id") == pid for p in projects):
            self.notify(f"Project '{pid}' already exists.", title="Setup",
                        severity="warning", markup=False)
            return
        from .models import PROJECT_COLORS
        projects.append({"id": pid, "name": pid, "color": PROJECT_COLORS[0],
                         "status": "on_track", "template": "", "shared": False})
        self.refresh_view()

    def action_setup_remove(self) -> None:
        """`x` removes a roster member or project in setup."""
        if self._setup_state is None:
            return
        section, row, _ = self._setup_cursor_item()
        if section == "roster":
            roster = self._setup_state.get("roster", [])
            if 0 <= row < len(roster):
                removed = roster.pop(row)
                # clear user_id if it was the removed member
                if self._setup_state.get("user_id") == removed.get("id"):
                    self._setup_state["user_id"] = None
                self._setup_state["cursor_row"] = max(0, row - 1)
                self.refresh_view()
        elif section == "proyectos":
            projects = self._setup_state.get("projects", [])
            if 0 <= row < len(projects):
                projects.pop(row)
                self._setup_state["cursor_row"] = max(0, row - 1)
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
        switches swimlanes grid/waves, or cycles setup sections; a no-op
        elsewhere."""
        if self.view_mode == "setup":
            self.action_setup_section()
            return
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
        shown = clip(proj.name, 40)
        self.notify(f'"{shown}" {"pinned" if proj.pinned else "unpinned"}',
                    title="Pin project", severity="information", markup=False)
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
        """escape — clear search/focus in kanban/gantt, cancel setup, and do
        NOTHING otherwise (§6.5 AMD-03)."""
        if self.view_mode == "setup":
            self.action_setup_exit()
            return
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
        if self.view_mode == "setup":
            self.action_setup_add()
            return
        self.push_screen(TaskModal(self.board), self._on_task_added)

    def _on_task_added(self, data: dict | None) -> None:
        if not data:
            return
        want = data.pop("milestone", False)
        task = Task(**data)
        self._apply_editor_milestone(task, want)
        self.board.add_task(task)
        self.selected_task_id = task.id
        self.refresh_view()

    def action_details(self) -> None:
        """Read-only details view of the selected task (Enter), or edit the
        selected setup row when in setup view."""
        if self.view_mode == "setup":
            self.action_setup_edit()
            return
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
        waiting = waiting_ids(self.board)
        archive = data.pop("archived", None)
        want = data.pop("milestone", None)
        prior_start, was_milestone = task.start_date, task.milestone
        old_start, old_due = task.start_date, task.due_date
        new_start = data.pop("start_date", old_start)
        new_due = data.pop("due_date", old_due)
        n_s, o_s = parse_iso(new_start), parse_iso(old_start)
        sd = (n_s - o_s).days if n_s is not None and o_s is not None else 0
        n_d, o_d = parse_iso(new_due), parse_iso(old_due)
        dd = (n_d - o_d).days if n_d is not None and o_d is not None else 0
        for k, v in data.items():
            if k == "phase":
                # routed through the board so the move is DATED; assigning it
                # here would leave the stamp behind and momentum unknowable
                self.board.set_task_phase(task, v)
                continue
            setattr(task, k, v)
        # the DATE fields ride the cascade when they actually move (LLR-604.3):
        # the new value is written here (the milestone box reads it) and a field
        # whose change is a clean delta is put back to its OLD value so the
        # cascade applies it exactly once; a cleared/junk/undated field keeps
        # what the user typed (delta 0) and the cascade leaves it.
        task.start_date = new_start
        task.due_date = new_due
        if want is not None:
            self._apply_editor_milestone(task, want, prior_start, was_milestone)
        # the archive box is judged AFTER the edited phase (architect A-12): an
        # edit that finishes the task and archives it is allowed
        if archive is not None and not (archive and not task.archived and self._refuse(
                task, "archive", " — other changes saved")):
            task.archived = archive
        cascaded = False
        if sd or dd:
            if task.milestone:
                # the box has canonicalized (start == due, set_milestone): the
                # move that matters is the DUE's post-canonicalization delta; a
                # zero there means no date moved — the normal save persists the
                # box and the editor stays silent (code review K, TC-634)
                a, b = parse_iso(task.due_date), parse_iso(old_due)
                dd_eff = (a - b).days if a is not None and b is not None else 0
                if dd_eff:
                    task.start_date = old_start
                    task.due_date = old_due
                    self._apply_cascade(task, 0, dd_eff, say_solo=False)
                    cascaded = True
            else:
                task.start_date = old_start if sd else new_start
                task.due_date = old_due if dd else new_due
                self._apply_cascade(task, sd, dd, say_solo=False)
                cascaded = True
                # the undo entry must hold the TRUE pre-edit dates: a delta-0
                # field (a first date typed, say) kept its new value through the
                # restore dance, so put its old value back (TC-633)
                for one in self._undo_stack[-1]["cascade"]["tasks"]:
                    if one["task_id"] == task.id:
                        if not sd:
                            one["fields"]["start_date"] = old_start
                        if not dd:
                            one["fields"]["due_date"] = old_due
        if cascaded:
            self._warn_history_error()
            self._say_ready(waiting, task)
            return
        self.board.save()
        self._warn_history_error()
        self.refresh_view()
        self._say_ready(waiting, task)

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
                    title="Archived", severity="information", timeout=8, markup=False)

    def action_delete(self) -> None:
        task = self.selected_task
        if task is None or self._refuse(task, "delete"):
            return
        self.push_screen(ConfirmModal(f"Delete '{task.title}'?"),
                        lambda ok, t=task: self._on_delete(t, ok))

    def _on_delete(self, task: Task, ok: bool) -> None:
        # judged again: a sync tick could have changed the board while the
        # confirm was open (security S-7)
        if not ok or self._refuse(task, "delete"):
            return
        self._undo_stack.append(self._snapshot(task, deleted=True))
        self.board.delete_task(task.id)
        self.selected_task_id = None
        self.refresh_view()

    def action_archive(self) -> None:
        """`x` — put a task away, bring it back, or remove a setup row. It SAYS
        SO EITHER WAY.

        The complaint this answers: with `v` off, archiving makes the row vanish,
        and a row vanishing is indistinguishable from a key that did nothing. The
        row disappearing IS the effect, but the screen never said which effect it
        was. So the app states the fact and names the way back — and since the
        batch-04 undo shipped, `u` also reverses it (LLR-010.1: archive is in
        the undo domain), so the pre-flip state is snapshotted first."""
        if self.view_mode == "setup":
            # FIRST: in Setup `x` removes a setup row and never touches the
            # task still selected on the board behind it (code review F2,
            # security S-7; operator: "Corregir en el 002")
            self.action_setup_remove()
            return
        if self.view_mode == "chainmap":
            # On the chain map `x` is view-dispatched (LLR-801.2): it removes
            # the selected task's first incoming link, refusing verbatim when
            # there is none. The shipped archive meaning is inert here.
            self._chainmap_unlink()
            return
        task = self.selected_task
        if task is None:
            return
        if not task.archived and self._refuse(task, "archive"):
            return
        self._undo_stack.append(self._snapshot(task))
        task.archived = not task.archived
        self.board.save()
        # the title is the user's text: shown raw with markup OFF, never escaped
        # (S1) — a title holding markup must never render as markup here
        shown = clip(task.title, 40)
        if task.archived:
            # WITH `v` OFF THE ROW LEAVES THE SCREEN, and the selection leaves
            # with it — so `x` on its own no longer targets this task. Saying
            # "x brings it back" there would be a promise the app does not keep.
            body = (f'"{shown}" archived · '
                    + ("x brings it back" if self.show_archived
                       else "v shows it, then x brings it back"))
        else:
            body = f'"{shown}" restored'
        self.notify(body, title="Archive", severity="information", markup=False)
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
        date_links = data.pop("date_links", None)
        proj = Project(**data)
        if date_links:
            proj.extra["date_links"] = date_links
        self.board.add_project(proj)
        self.refresh_view()

    def action_manage_projects(self) -> None:
        self.push_screen(ProjectPicker(self.board))

    # ---- phases ------------------------------------------------------------
    def action_manage_phases(self) -> None:
        self.push_screen(PhaseEditor(self.board))
