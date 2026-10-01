"""THROWAWAY PROTOTYPE — task edit window, five structures (sub-shape A).

The real TaskboardApp (kanban view, real theme, real tcss) with TaskModal
subclasses that re-compose the SHIPPED field widgets at their REAL ids, so
`_save`, the calendar buttons, paste-image and ctrl+v / ctrl+e keep working.

    python prototypes/edit_modal/proto.py            live: 0-4 open a variant,
                                                     ←/→ cycle, esc closes it
    python prototypes/edit_modal/proto.py live C 12  open C directly, exit after 12 s
    python prototypes/edit_modal/proto.py shot       SVGs + measurements -> out/

0 baseline · A split editor · B tabs · C full screen + preview · D compact
Nothing here ships. Saves go to a temp copy of the fixture board.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes" / "kanban_priority"))

from rich.markup import escape  # noqa: E402
from textual.binding import Binding  # noqa: E402
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll  # noqa: E402
from textual.widgets import (Button, Checkbox, Input, Label, Select, Static,  # noqa: E402
                             TabbedContent, TabPane, TextArea)

import fixture  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.modals import NONE_VALUE, TASK_PRIORITIES, TaskModal  # noqa: E402
from taskboard.views import HEX, _highlight_markup  # noqa: E402

fixture.pin_today()

VARIANTS = ["0", "A", "B", "C", "D"]
NAMES = {"0": "baseline", "A": "split editor", "B": "tabs",
         "C": "full screen + preview", "D": "compact"}
HINT = "[dim]highlight: ==…== yellow, !!…!! red, ++…++ green[/dim]"


# ---------------------------------------------------------------------------
# the shipped fields, built exactly as TaskModal.compose builds them
# ---------------------------------------------------------------------------
class Fields:
    """Factory for the SHIPPED widgets at their real ids / initial values."""

    def __init__(self, modal: TaskModal):
        self.m = modal
        self.t = modal._edit_task

    def title(self, **kw):
        t = self.t
        return Input(value=(t.title if t else ""), placeholder="what needs doing",
                     id="f-title", **kw)

    def project(self, **kw):
        t = self.t
        opts = [("(none · Inbox)", NONE_VALUE)] + [
            (escape(p.name), p.id) for p in self.m.board.projects]
        val = t.project_id if (t and t.project_id) else NONE_VALUE
        return Select(opts, value=val, allow_blank=False, id="f-project", **kw)

    def phase(self, **kw):
        t = self.t
        phases = self.m.board.phases
        return Select([(escape(p), p) for p in phases],
                      value=(t.phase if (t and t.phase in phases) else phases[0]),
                      allow_blank=False, id="f-phase", **kw)

    def priority(self, **kw):
        t = self.t
        return Select([(p, p) for p in TASK_PRIORITIES],
                      value=(t.priority if t else "normal"),
                      allow_blank=False, id="f-priority", **kw)

    def check(self, name: str, label: str | None = None, **kw):
        t = self.t
        return Checkbox(label or name, value=bool(getattr(t, name)) if t else False,
                        id=f"f-{name}", **kw)

    def date(self, which: str, **kw):
        t = self.t
        attr = "start_date" if which == "start" else "due_date"
        return Input(value=(getattr(t, attr) or "" if t else ""), placeholder="optional",
                     id=f"f-{which}", classes="date-input", **kw)

    def cal(self, which: str, slim: bool = False):
        return Button("📅", id=f"cal-f-{which}",
                      classes="cal-btn slim-btn" if slim else "cal-btn")

    def notes(self):
        return TextArea(self.t.notes if self.t else "", id="f-notes")

    def urls(self):
        return TextArea("\n".join(self.t.urls) if self.t else "", id="f-urls")

    def images(self):
        return TextArea("\n".join(self.t.images) if self.t else "", id="f-images")

    def paste(self, slim: bool = False):
        return Button("Paste image" if slim else "Paste image from clipboard",
                      variant="primary", id="paste-img",
                      classes="slim-btn" if slim else "")

    def buttons(self, slim: bool = False):
        cls = "slim-btn" if slim else ""
        return (Button("Save", variant="success", id="save", classes=cls),
                Button("Cancel", variant="default", id="cancel", classes=cls))

    def heading(self):
        return Label(("[b]Edit task[/b]" if self.t else "[b]New task[/b]")
                     + "  [dim]· ctrl+e emoji[/dim]", classes="modal-title")


# ---------------------------------------------------------------------------
# 0 · baseline is TaskModal itself
# ---------------------------------------------------------------------------
class VariantA(TaskModal):
    """A · split editor: narrow metadata column left, notes fill the right."""

    def compose(self):
        f = Fields(self)
        with Vertical(id="va-box", classes="modal pbox"):
            yield f.heading()
            yield f.title()
            with Horizontal(id="va-split"):
                with VerticalScroll(id="va-meta", classes="slim"):
                    for key, w in (("Project", f.project()), ("Phase", f.phase()),
                                   ("Priority", f.priority())):
                        with Horizontal(classes="row1"):
                            yield Label(key, classes="k")
                            yield w
                    for which in ("start", "due"):
                        with Horizontal(classes="row1"):
                            yield Label(which.capitalize(), classes="k")
                            yield f.date(which)
                            yield f.cal(which, slim=True)
                    yield f.check("blocked")
                    yield f.check("archived")
                    yield f.check("pinned")
                    yield Label("URLs", classes="sec")
                    u = f.urls()
                    u.styles.height = 4
                    yield u
                    yield Label("Images", classes="sec")
                    im = f.images()
                    im.styles.height = 3
                    yield im
                    yield f.paste(slim=True)
                with Vertical(id="va-notes"):
                    yield Label("Notes  " + HINT, classes="sec")
                    yield f.notes()
            with Horizontal(classes="modal-buttons"):
                yield from f.buttons()


class VariantB(TaskModal):
    """B · tabs: title pinned, Notes / Details / Links tabs, buttons always on."""

    def compose(self):
        f = Fields(self)
        with Vertical(id="vb-box", classes="modal pbox"):
            yield f.heading()
            yield f.title()
            with TabbedContent(id="vb-tabs", initial="vb-notes"):
                with TabPane("Notes", id="vb-notes"):
                    yield Label(HINT, classes="sec")
                    yield f.notes()
                with TabPane("Details", id="vb-details"):
                    with Grid(id="vb-grid"):
                        yield Label("Project")
                        yield f.project()
                        yield Label("Phase")
                        yield f.phase()
                        yield Label("Priority")
                        yield f.priority()
                        yield Label("Blocked")
                        yield f.check("blocked")
                        yield Label("Start")
                        with Horizontal(classes="date-row"):
                            yield f.date("start")
                            yield f.cal("start")
                        yield Label("Due")
                        with Horizontal(classes="date-row"):
                            yield f.date("due")
                            yield f.cal("due")
                        yield Label("Archived")
                        yield f.check("archived")
                        yield Label("Pinned")
                        yield f.check("pinned")
                with TabPane("Links", id="vb-links"):
                    yield Label("URLs (one per line)", classes="sec")
                    yield f.urls()
                    yield Label("Images (path or URL, one per line)", classes="sec")
                    yield f.images()
                    yield f.paste()
            with Horizontal(classes="modal-buttons"):
                yield from f.buttons()


def preview_markup(text: str) -> str:
    """The notes as the app's own highlight renderer draws them, line by line
    (the app's regex is per line too), bullets turned into •."""
    out = []
    for ln in text.splitlines():
        s = ln.rstrip()
        if s.startswith("- "):
            out.append(f"[{HEX['dim']}]  •[/] " + _highlight_markup(s[2:]))
        elif s and s[0].isdigit() and s[1:3] == ". ":
            out.append(f"[{HEX['dim']}]  {s[0]}.[/] " + _highlight_markup(s[3:]))
        elif s and not s.endswith((".", ":", ";")) and len(s) < 40 and " " in s \
                and not any(m in s for m in ("==", "!!", "++", "http")):
            out.append(f"[b {HEX['hd']}]{escape(s)}[/]")       # a section heading
        else:
            out.append(_highlight_markup(s) if s else "")
    return "\n".join(out)


class VariantC(TaskModal):
    """C · full screen: title line, one row of property chips, notes | preview."""

    def compose(self):
        f = Fields(self)
        with Vertical(id="vc-box", classes="pbox"):
            with Horizontal(id="vc-head", classes="slim"):
                yield Label("[b]✎ EDIT[/b]", classes="k")
                yield f.title()
                yield Label("[dim]ctrl+e emoji · esc cancel[/dim]", classes="tail")
            with Horizontal(id="vc-chips", classes="slim"):
                yield f.project()
                yield f.phase()
                yield f.priority()
                yield f.date("start")
                yield f.cal("start", slim=True)
                yield Label("→", classes="arrow")
                yield f.date("due")
                yield f.cal("due", slim=True)
                yield f.check("blocked")
                yield f.check("archived")
                yield f.check("pinned")
            with Horizontal(id="vc-split"):
                with Vertical(id="vc-edit"):
                    yield Label("NOTES · editing  " + HINT, classes="sec")
                    yield f.notes()
                with Vertical(id="vc-prev"):
                    yield Label("PREVIEW · as the board renders it", classes="sec")
                    with VerticalScroll(id="vc-prev-scroll"):
                        yield Static(preview_markup(self._edit_task.notes
                                                    if self._edit_task else ""),
                                     id="vc-preview")
            with Horizontal(id="vc-foot", classes="slim"):
                with Vertical(classes="foot-col"):
                    yield Label("URLs", classes="sec")
                    yield f.urls()
                with Vertical(classes="foot-col"):
                    yield Label("Images", classes="sec")
                    yield f.images()
                with Vertical(id="vc-actions"):
                    yield f.paste(slim=True)
                    yield from f.buttons(slim=True)

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area.id == "f-notes":
            self.query_one("#vc-preview", Static).update(
                preview_markup(event.text_area.text))


class VariantD(TaskModal):
    """D · compact: same vertical modal, wider, 4-col grid of one-row fields."""

    def compose(self):
        f = Fields(self)
        with VerticalScroll(id="vd-box", classes="modal pbox"):
            yield f.heading()
            yield f.title()
            with Grid(id="vd-grid", classes="slim"):
                yield Label("Project", classes="k")
                yield f.project()
                yield Label("Phase", classes="k")
                yield f.phase()
                yield Label("Priority", classes="k")
                yield f.priority()
                yield Label("Start", classes="k")
                with Horizontal(classes="row1"):
                    yield f.date("start")
                    yield f.cal("start", slim=True)
                yield Label("Due", classes="k")
                with Horizontal(classes="row1"):
                    yield f.date("due")
                    yield f.cal("due", slim=True)
                yield Label("", classes="k")
                yield Label("")
            with Horizontal(id="vd-flags", classes="slim"):
                yield f.check("blocked")
                yield f.check("archived")
                yield f.check("pinned")
            yield Label("Notes  " + HINT, classes="sec")
            yield f.notes()
            with Horizontal(id="vd-links"):
                with Vertical(classes="foot-col"):
                    yield Label("URLs (one per line)", classes="sec")
                    yield f.urls()
                with Vertical(classes="foot-col"):
                    yield Label("Images (path or URL)", classes="sec")
                    yield f.images()
            with Horizontal(classes="modal-buttons"):
                yield f.paste()
                yield Static("", classes="spacer")
                yield from f.buttons()


CLASSES = {"0": TaskModal, "A": VariantA, "B": VariantB, "C": VariantC,
           "D": VariantD}

# App-level CSS (same tier as taskboard.tcss, so specificity — not load order
# tier — decides; DEFAULT_CSS on the screens would LOSE to `.modal Label`).
PROTO_CSS = """
.pbox { padding: 0 1; }
#va-box, #vb-box { width: 92%; height: 92%; max-height: 92%; max-width: 92%; }
#vd-box { width: 100; max-width: 96%; height: 92%; max-height: 92%; }
#vc-box { width: 100%; height: 100%; background: #0d1219;
          border-top: solid #334154; }
TaskModal .modal-title { margin-bottom: 0; }

/* slim: one-row fields — no tall borders, a tinted well instead */
.pbox .slim Label { margin-top: 0; }
.pbox .slim Input { border: none; height: 1; padding: 0 1; background: #111a26; }
.pbox .slim Input:focus { border: none; background: #10343a; }
.pbox .slim Select { height: 1; }
.pbox .slim SelectCurrent { border: none; height: 1; padding: 0 1; background: #111a26; }
.pbox .slim Select:focus SelectCurrent { background: #10343a; }
.pbox .slim Checkbox { border: none; height: 1; padding: 0; background: transparent;
                       width: auto; margin-right: 2; }
.pbox .slim-btn { height: 1; min-width: 4; border: none; margin: 0 0 0 1; }
.pbox .slim .cal-btn { width: 4; min-width: 4; height: 1; margin-left: 1; }
.pbox .sec { margin-top: 1; color: #8b98a5; }
.pbox .slim .k { width: 9; color: #8b98a5; }

/* A */
#va-split { height: 1fr; margin-top: 1; }
#va-meta { width: 34; height: 1fr; padding-right: 1;
           border-right: vkey #1f2733; scrollbar-size: 1 1; }
#va-meta .row1 { height: 1; margin-bottom: 1; }
#va-meta Select { width: 1fr; }
#va-meta .date-input { width: 1fr; }
#va-meta Checkbox { margin-bottom: 0; }
#va-meta .sec { margin-top: 0; }
#va-meta #f-blocked { margin-top: 0; }
#va-meta #f-pinned { margin-bottom: 1; }
#va-meta #paste-img { margin: 1 0 0 0; width: 100%; }
#va-notes { width: 1fr; height: 1fr; padding-left: 1; }
#va-notes .sec { margin-top: 0; }
#va-notes #f-notes { height: 1fr; }
#va-box .modal-buttons { margin-top: 0; }

/* B */
#vb-tabs { height: 1fr; margin-top: 1; }
#vb-tabs ContentSwitcher { height: 1fr; }
#vb-tabs TabPane { height: 1fr; padding: 0; }
#vb-notes .sec { margin-top: 0; }
#vb-notes #f-notes { height: 1fr; }
#vb-grid { grid-size: 4; grid-columns: 10 1fr 10 1fr; grid-gutter: 0 1;
           grid-rows: 3; height: auto; margin-top: 1; }
#vb-grid Label { margin-top: 0; height: 3; content-align: left middle; }
#vb-links #f-urls, #vb-links #f-images { height: 1fr; }
#vb-box .modal-buttons { margin-top: 0; }

/* C */
#vc-head { height: 1; margin-top: 0; }
#vc-head .k { width: 9; color: #2dd4bf; }
#vc-head #f-title { width: 1fr; text-style: bold; }
#vc-head .tail { width: auto; margin-left: 2; }
#vc-chips { height: 1; margin-top: 1; overflow: hidden hidden; }
#vc-chips #f-project { width: 24; }
#vc-chips #f-phase { width: 12; margin-left: 1; }
#vc-chips #f-priority { width: 11; margin-left: 1; }
#vc-chips .date-input { width: 11; margin-left: 1; padding: 0 0 0 1; }
#vc-chips .arrow { width: 2; content-align: center middle; color: #5b6675; }
#vc-chips Checkbox { margin-left: 0; margin-right: 0; }
#vc-chips .cal-btn { margin-left: 0; }
#vc-split { height: 1fr; margin-top: 1; }
#vc-edit { width: 1fr; height: 1fr; }
#vc-edit .sec, #vc-prev .sec { margin-top: 0; }
#vc-edit #f-notes { height: 1fr; }
#vc-prev { width: 1fr; height: 1fr; padding-left: 1; }
#vc-prev-scroll { height: 1fr; border: tall #1b2431; padding: 0 1; background: #0b111a; }
#vc-foot { height: 5; margin-top: 0; }
#vc-foot .foot-col { width: 1fr; height: 5; }
#vc-foot TextArea { height: 1fr; }
#vc-actions { width: 18; height: 5; padding-top: 1; }
#vc-actions Button { width: 100%; margin: 0 0 0 1; }

/* D */
#vd-grid { grid-size: 4; grid-columns: 9 1fr 9 1fr; grid-gutter: 0 2;
           grid-rows: 1; height: auto; margin-top: 1; }
#vd-grid Select, #vd-grid .row1 { width: 1fr; height: 1; }
#vd-grid .date-input { width: 1fr; }
#vd-flags { height: 1; margin-top: 1; }
#vd-box #f-notes { height: 1fr; min-height: 8; }
#vd-links { height: 5; }
#vd-links .foot-col { width: 1fr; height: 5; }
#vd-links .foot-col:first-child { margin-right: 1; }
#vd-links TextArea { height: 1fr; }
#vd-box .spacer { width: 1fr; }
#vd-box .modal-buttons { margin-top: 0; }
"""


class EditProto(TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")   # the REAL stylesheet
    CSS = PROTO_CSS
    BINDINGS = [Binding(k, f"variant('{k}')", f"{k}", priority=True) for k in "01234"] + [
        Binding("left", "cycle(-1)", "prev", priority=True),
        Binding("right", "cycle(1)", "next", priority=True),
    ]

    def __init__(self, variant: str | None = None, seconds: float | None = None):
        super().__init__(board_path=fixture.write_board(), team_sync_interval=1e9)
        self._variant = variant
        self._seconds = seconds
        self._idx = 0

    def on_mount(self) -> None:
        super().on_mount()
        if os.environ.get("PROTO_SHOT_TITLE"):
            # the window names itself — the WT harness selects it by this title
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.view_mode = "kanban"
        self.selected_task_id = fixture.LONG_TASK_ID
        self.refresh_view()
        if self._variant:
            self.call_after_refresh(self.open_variant, self._variant)
        if self._seconds:
            self.set_timer(self._seconds, self.exit)

    def check_action(self, action, parameters):
        if action in ("variant", "cycle") and len(self.screen_stack) > 1:
            return False          # inside the modal the keys type, they don't switch
        return super().check_action(action, parameters)

    def action_variant(self, key: str) -> None:
        self.open_variant(VARIANTS[int(key)])

    def action_cycle(self, d: int) -> None:
        self.open_variant(VARIANTS[(self._idx + d) % len(VARIANTS)])

    def open_variant(self, v: str) -> None:
        self._idx = VARIANTS.index(v)
        task = self.board.task_by_id(fixture.LONG_TASK_ID)
        modal = CLASSES[v](self.board, task)
        self.push_screen(modal, lambda data, t=task: self._on_task_edited(t, data))
        self.call_after_refresh(self._start_writing)

    def _start_writing(self) -> None:
        """Focus the notes with the cursor at the end — the 'writing' state."""
        try:
            ta = self.screen.query_one("#f-notes", TextArea)
        except Exception:
            return
        ta.focus()
        ta.move_cursor(ta.document.end)
        if os.environ.get("PROTO_SHOT_TITLE"):
            ta.cursor_blink = False      # a blink-off frame would hide the cursor


# ---------------------------------------------------------------------------
# measurement + shot
# ---------------------------------------------------------------------------
def measure(app: EditProto) -> dict:
    scr = app.screen
    ta = scr.query_one("#f-notes", TextArea)
    vis = scr._compositor.visible_widgets
    rows = cols = 0
    if ta in vis:
        region, clip = vis[ta]
        content = region.shrink(ta.styles.gutter).intersection(clip)
        rows, cols = content.height, content.width
    total = ta.wrapped_document.height
    title_on = scr.query_one("#f-title") in vis
    save_on = scr.query_one("#save") in vis
    return {"notes_rows_visible": rows, "notes_cols": cols,
            "notes_wrapped_rows_total": total,
            "notes_logical_lines": ta.document.line_count,
            "title_visible": title_on, "save_visible": save_on}


def _shot() -> None:
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    facts: dict = {}

    async def run(v: str, size: tuple[int, int], tab: str | None = None) -> None:
        app = EditProto()
        async with app.run_test(size=size) as pilot:
            await pilot.pause()
            app.open_variant(v)
            for _ in range(4):
                await pilot.pause()
            ta = app.screen.query_one("#f-notes", TextArea)
            ta.cursor_blink = False          # a blink-off frame would hide the cursor
            if tab:
                app.screen.query_one("#vb-tabs", TabbedContent).active = tab
                for _ in range(3):
                    await pilot.pause()
            await pilot.pause(0.2)
            key = f"{v}-{size[0]}" + (f"-{tab}" if tab else "")
            facts[key] = measure(app)
            name = f"edit_{v}_{size[0]}x{size[1]}" + ("_details" if tab else "") + ".svg"
            app.save_screenshot(filename=name, path=str(out))
            print(name, facts[key])

    for v in VARIANTS:
        for size in ((120, 36), (80, 24)):
            asyncio.run(run(v, size))
    for size in ((120, 36), (80, 24)):
        asyncio.run(run("B", size, tab="vb-details"))
    (out / "facts_edit.json").write_text(json.dumps(facts, indent=2), encoding="utf-8")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "shot":
        _shot()
    elif args and args[0] == "live":
        v = args[1] if len(args) > 1 else "0"
        secs = float(args[2]) if len(args) > 2 else None
        EditProto(variant=v, seconds=secs).run()
    else:
        EditProto().run()
