"""THROWAWAY prototype — the capture round: a quick-capture inbox that turns notes into
tasks (with deterministic project suggestions), a list view in the order tasks were
added, and multicolour notes.

    unset NO_COLOR; PYTHONUTF8=1 python prototypes/capture_round/proto.py list
    unset NO_COLOR; PYTHONUTF8=1 python prototypes/capture_round/proto.py shot [SCENE ...]
    python prototypes/capture_round/proto.py live SCENE [SECONDS]      (a real terminal)
    python prototypes/capture_round/proto.py play SCENE                (interactive, no timer)

Sub-shape A: the REAL `TaskboardApp` (subclassed here) on a real registry in a temporary
folder (fixture.py), driven by real key presses (`App._press_keys`) — in a real Windows
Terminal for the PNGs (shoot.ps1). Each variant is a new screen, or a subclass of the
shipped editor, patched into the app's modules for that scene only. Nothing under
`taskboard/` is edited; nothing writes outside the temporary folder.
"""
from __future__ import annotations

import asyncio
import inspect
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

import fixture as fx  # noqa: E402
import suggest as sg  # noqa: E402
from rich.text import Text  # noqa: E402
from textual.binding import Binding  # noqa: E402
from textual.color import Color  # noqa: E402
from textual.containers import Horizontal, Vertical  # noqa: E402
from textual.screen import ModalScreen, Screen  # noqa: E402
from textual.widgets import Input, Static, TextArea  # noqa: E402

from taskboard import app as app_mod, history, models, modals, report_html, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry, peek_board  # noqa: E402
from taskboard.keymap import key_line  # noqa: E402
from taskboard.models import Project, Task  # noqa: E402
from taskboard.views import HEX, board_hex, fit  # noqa: E402

TODAY = fx.TODAY
NOW = datetime(2026, 11, 4, 10, 2)
OUT = HERE / "out"


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


app_mod.date = _Today
models.date = _Today
views.date = _Today

ACC, MUT, DIM, INK = HEX["accent"], HEX["mut"], HEX["dim"], HEX["ink"]


def see_through(screen, alpha: float) -> None:
    """The app's `Screen { background: #0d1117 }` (taskboard.tcss) outranks a screen's
    DEFAULT_CSS, so a modal that should show what is under it sets it inline."""
    screen.styles.background = Color(13, 17, 23, alpha)


def ph(p) -> str:
    return HEX.get(p.color, HEX["sky"]) if p else MUT


def boards_of(app) -> list:
    lanes, ids = app_mod.board_lanes(app)
    return [(bid, name, col, b) for (name, col, b, _s), bid in zip(lanes, ids) if b is not None]


def docs_of(app) -> list:
    return sg.corpus(boards_of(app))


def hit_text(h, w: int | None = None, bars: bool = True) -> Text:
    """`Eval harness · Client A ▰▰▰` — the project in its colour, the board dim."""
    t = Text(no_wrap=True)
    if h is None:
        t.append("+ new project", f"b {HEX['amber']}")
        return t
    t.append(h.doc.name, f"b {HEX.get(h.doc.colour, INK)}")
    t.append(" · " + h.doc.board, board_hex(h.doc.board_colour))
    if bars:
        t.append(" " + sg.bars(h.score), ACC if sg.level(h.score) >= 2 else HEX["amber"])
    if w:
        t.truncate(w, overflow="ellipsis")
    return t


def options(hits: list) -> list:
    """What `alt+o` cycles: the best project first — or `new project` first when the best
    is only a weak guess (below MID) — then the rest, `new project` always last or first."""
    if hits and sg.level(hits[0].score) >= 2:
        return list(hits) + [None]
    return [None] + list(hits)


# =============================================================================
# the inbox (D1: one global file beside the registry) and the dump
# =============================================================================
class Inbox:
    def __init__(self, root: Path):
        self.path = root / "inbox.json"
        self.root = root
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.notes = raw["notes"]

    def open_notes(self) -> list[dict]:
        return [n for n in self.notes if not n.get("dumped")]

    def dumped(self) -> list[dict]:
        return [n for n in self.notes if n.get("dumped")]

    def save(self) -> None:
        self.path.write_text(json.dumps({"version": 1, "notes": self.notes}, indent=2,
                                        ensure_ascii=False), encoding="utf-8")

    def image(self, name: str) -> Path | None:
        hits = sorted((self.root / "inbox" / "images").glob(f"*/{name}"))
        return hits[0] if hits else None


def board_for(app, bid: str):
    if bid == app.board_id:
        return app.board
    entry = next(e for e in app.registry.active() if e.id == bid)
    return peek_board(entry.path)


def dump(app, inbox: Inbox, text: str, hit, new_name: str | None = None,
         new_board: str | None = None) -> dict:
    """Turn a note into a task: first line the title, the rest the notes, `img:` lines the
    images (copied beside the board), `created` stamped. `hit` None = a new project."""
    title, notes, imgs = sg.as_task(text)
    bid = hit.doc.board_id if hit else (new_board or app.board_id)
    board = board_for(app, bid)
    made_project = None
    if hit is None:
        used = {p.color for p in board.projects}
        colour = next((c for c in ("amber", "orange", "rose", "teal", "cyan", "lime")
                       if c not in used and c in HEX), "amber")
        made_project = Project(name=new_name or title[:30], color=colour)
        board.add_project(made_project)
        pid = made_project.id
    else:
        pid = hit.doc.project_id
    task = Task(title=title, project_id=pid, notes=notes,
                extra={"created": NOW.isoformat(timespec="seconds")})
    for name in imgs:
        src = inbox.image(name)
        if src:
            dest = board.image_dir(task.id) / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            task.images.append(str(dest))
    board.add_task(task)
    if board is not app.board:
        board.save()
    note = {"id": f"n{len(inbox.notes) + 1}", "at": NOW.isoformat(timespec="seconds"),
            "text": text, "dumped": {"task": task.id, "board": bid, "project": pid,
                                     "new_project": bool(made_project),
                                     "at": NOW.isoformat(timespec="seconds")}}
    proj = made_project.name if made_project else hit.doc.name
    bname = next((n for b, n, _c, _b in boards_of(app) if b == bid), bid)
    app.notify(f"Dumped → {proj} · {bname}   ·   alt+u undo", title="Inbox", timeout=30,
               markup=False)
    return note


def undo_dump(app, note: dict) -> None:
    d = note["dumped"]
    board = board_for(app, d["board"])
    board.delete_task(d["task"])
    if d.get("new_project"):
        board.projects = [p for p in board.projects if p.id != d["project"]]
    board.save()


INBOX: list[Inbox | None] = [None]


def topic_rows(topics, cur: int, choices: dict, docs, w: int, compact: bool) -> list[Text]:
    rows: list[Text] = []
    for i, (_a, _b, text) in enumerate(topics):
        title, notes, imgs = sg.as_task(text)
        hits = sg.suggest(text, docs)
        opts = options(hits)
        ch = opts[choices.get(i, 0) % len(opts)]
        on = i == cur
        if compact and not on:
            continue
        head = Text(no_wrap=True)
        head.append("▌" if on else " ", ACC)
        head.append(f"{i + 1} ", f"b {ACC}" if on else DIM)
        head.append(title, f"b {INK}" if on else HEX["hd"])
        if imgs:
            head.append(f"  ▣ {len(imgs)}", HEX["amber"])
        head.truncate(w, overflow="ellipsis")
        rows.append(head)
        r = Text(no_wrap=True)
        r.append("▌" if on else " ", ACC)
        r.append("  → ", ACC)
        r.append_text(hit_text(ch))
        r.truncate(w, overflow="ellipsis")
        rows.append(r)
        why = Text(no_wrap=True)
        why.append("▌" if on else " ", ACC)
        if ch is not None:
            why.append("    why ", DIM)
            why.append(" · ".join(ch.why[:3]), MUT)
        elif hits:
            why.append("    weak: ", DIM)
            why.append(" · ".join(hits[0].why[:2]) + f" ({hits[0].doc.name})", MUT)
        else:
            why.append("    no project shares a word", MUT)
        why.truncate(w, overflow="ellipsis")
        rows.append(why)
        alts = [o for o in opts if o is not ch]
        if on and alts:
            a = Text(no_wrap=True)
            a.append("▌", ACC)
            a.append("    or ", DIM)
            for j, o in enumerate(alts[:2]):
                if j:
                    a.append("  ·  ", DIM)
                a.append_text(hit_text(o))
            a.truncate(w, overflow="ellipsis")
            rows.append(a)
        if not compact:
            rows.append(Text(""))
    return rows


def dumped_rows(inbox: Inbox, w: int) -> list[Text]:
    done = inbox.dumped()
    if not done:
        return []
    t = Text(no_wrap=True)
    t.append(f"✓ dumped {len(done)}", f"b {HEX['done']}")
    t.append("  ·  alt+u undo  ·  folded, kept 7 days", DIM)
    t.truncate(w, overflow="ellipsis")
    rows = [t]
    for n in done[-2:]:
        r = Text(no_wrap=True)
        r.append("  ✓ ", HEX["done"])
        r.append(n["text"].split("\n")[0], DIM)
        r.truncate(w, overflow="ellipsis")
        rows.append(r)
    return rows


# =============================================================================
# 1 · A — the pad: one free text, the suggestions in a rail beside it
# =============================================================================
PAD_KEYS = [("alt+d", "dump"), ("alt+o", "other"), ("alt+n", "new project"),
            ("alt+a", "review all"), ("alt+i", "image"), ("alt+u", "undo"), ("esc", "close")]


class PadScreen(Screen[None]):
    BINDINGS = [Binding("escape", "close", "", priority=True),
                Binding("alt+d", "dump", "", priority=True),
                Binding("alt+o", "other", "", priority=True),
                Binding("alt+n", "new", "", priority=True),
                Binding("alt+b", "board", "", priority=True),
                Binding("alt+a", "review", "", priority=True),
                Binding("alt+i", "image", "", priority=True),
                Binding("alt+u", "undo", "", priority=True)]
    DEFAULT_CSS = """
    PadScreen { background: #0d1117; }
    #pad-head { height: 1; padding: 0 1; }
    #pad-main { height: 1fr; }
    #pad-left { width: 1fr; }
    #pad { height: 1fr; border: tall #2dd4bf 40%; background: #0b0f17; }
    #pad-rail { width: 50; padding: 0 1; }
    #pad-new { display: none; margin: 0 1; }
    #pad-new.on { display: block; }
    #pad-keys { dock: bottom; height: 1; padding: 0 1; background: #0b0f17; }
    PadScreen.-narrow #pad-main { layout: vertical; }
    PadScreen.-narrow #pad-rail { width: 1fr; height: 7; }
    """

    def __init__(self) -> None:
        super().__init__()
        self.inbox = INBOX[0]
        self.choices: dict[int, int] = {}
        self.new_board: str | None = None

    def compose(self):
        yield Static(id="pad-head")
        with Horizontal(id="pad-main"):
            with Vertical(id="pad-left"):
                text = "\n\n".join(n["text"] for n in self.inbox.open_notes()) + "\n\n"
                yield TextArea(text, id="pad", soft_wrap=True, show_line_numbers=False)
            with Vertical(id="pad-rail-box"):
                yield Static(id="pad-rail")
                yield Input(placeholder="new project name", id="pad-new")
        yield Static(id="pad-keys")

    def on_mount(self) -> None:
        self.docs = docs_of(self.app)
        ta = self.query_one("#pad", TextArea)
        ta.focus()
        ta.move_cursor(ta.document.end)
        self.set_class(self.app.size.width < 100, "-narrow")
        self._paint()

    def on_resize(self, _e) -> None:
        self.set_class(self.app.size.width < 100, "-narrow")
        self._paint()

    def topics(self):
        return sg.split_topics(self.query_one("#pad", TextArea).text)

    def cur(self) -> int:
        row = self.query_one("#pad", TextArea).cursor_location[0]
        tps = self.topics()
        for i, (a, b, _t) in enumerate(tps):
            if a <= row <= b + 1:
                return i
        return len(tps) - 1

    def on_text_area_changed(self, _e) -> None:
        self._paint()

    def on_text_area_selection_changed(self, _e) -> None:
        self._paint()

    def _paint(self) -> None:
        w = self.app.size.width
        narrow = w < 100
        tps = self.topics()
        head = Text(no_wrap=True)
        head.append("INBOX", f"b {ACC}")
        head.append(f"  {len(tps)} notes · a blank line starts the next note · "
                    "suggestions read every board", MUT)
        head.append("   inbox.json", DIM)
        self.query_one("#pad-head", Static).update(head)
        rw = (w - 4) if narrow else 46
        rows = topic_rows(tps, self.cur(), self.choices, self.docs, rw, narrow)
        if not narrow:
            rows += dumped_rows(self.inbox, rw)
        elif self.inbox.dumped():
            rows += dumped_rows(self.inbox, rw)[:1]
        self.query_one("#pad-rail", Static).update(Text("\n").join(rows))
        keys = PAD_KEYS
        if self.query_one("#pad-new", Input).has_class("on"):
            bname = next((n for b, n, _c, _b in boards_of(self.app)
                          if b == (self.new_board or self.app.board_id)), "")
            keys = [("↵", f"create on {bname} + dump"), ("alt+b", "board"), ("esc", "back")]
        self.query_one("#pad-keys", Static).update(key_line(keys, w - 2))

    def _topic(self):
        tps = self.topics()
        if not tps:
            return None, None, None
        i = self.cur()
        a, b, text = tps[i]
        opts = options(sg.suggest(text, self.docs))
        return i, (a, b, text), opts[self.choices.get(i, 0) % len(opts)]

    def _remove(self, a: int, b: int) -> None:
        ta = self.query_one("#pad", TextArea)
        lines = ta.text.split("\n")
        del lines[a:b + 1]
        if a < len(lines) and not lines[a].strip():
            del lines[a]
        ta.text = "\n".join(lines)
        ta.move_cursor((min(a, len(lines) - 1), 0))

    def action_dump(self, hit_override=False, name=None) -> None:
        i, tp, ch = self._topic()
        if tp is None:
            return
        if ch is None and name is None:
            self.action_new()
            return
        note = dump(self.app, self.inbox, tp[2], None if name else ch, name, self.new_board)
        self.inbox.notes = [n for n in self.inbox.notes if n["text"] != tp[2]] + [note]
        self.inbox.save()
        self._remove(tp[0], tp[1])
        self.choices.clear()
        self.docs = docs_of(self.app)
        self._paint()

    def action_other(self) -> None:
        i, tp, _ch = self._topic()
        if tp is not None:
            self.choices[i] = self.choices.get(i, 0) + 1
            self._paint()

    def action_new(self) -> None:
        inp = self.query_one("#pad-new", Input)
        i = self.cur()
        inp.border_title = f"New project for note {i + 1}"
        inp.add_class("on")
        inp.focus()
        self._paint()

    def action_board(self) -> None:
        ids = [b for b, *_ in boards_of(self.app)]
        cur = self.new_board or self.app.board_id
        self.new_board = ids[(ids.index(cur) + 1) % len(ids)]
        self._paint()

    def on_input_submitted(self, event) -> None:
        name = event.value.strip()
        event.input.remove_class("on")
        event.input.value = ""
        self.query_one("#pad", TextArea).focus()
        if name:
            self.action_dump(name=name)

    def action_close(self) -> None:
        inp = self.query_one("#pad-new", Input)
        if inp.has_class("on"):
            inp.remove_class("on")
            self.query_one("#pad", TextArea).focus()
            self._paint()
            return
        self.app.pop_screen()

    def action_review(self) -> None:
        tps = self.topics()
        self.app.push_screen(ReviewScreen([t for _a, _b, t in tps]))

    def action_image(self) -> None:
        ta = self.query_one("#pad", TextArea)
        name = f"pasted-{NOW:%H%M}.png"
        fx.tiny_png(self.inbox.root / "inbox" / "images" / "new" / name, (96, 165, 250))
        row = ta.cursor_location[0]
        ta.move_cursor((row, len(ta.document.get_line(row))))
        ta.insert(f"\nimg: {name}")

    def action_undo(self) -> None:
        done = self.inbox.dumped()
        if not done:
            return
        note = done[-1]
        undo_dump(self.app, note)
        self.inbox.notes.remove(note)
        note["dumped"] = None
        self.inbox.notes.append(note)
        self.inbox.save()
        ta = self.query_one("#pad", TextArea)
        ta.text = ta.text.rstrip("\n") + "\n\n" + note["text"] + "\n"
        self.docs = docs_of(self.app)
        self._paint()


# =============================================================================
# 1 · B — the drawer: capture over the board, an autocomplete line under the draft
# =============================================================================
DRAWER_KEYS = [("⇥", "other"), ("alt+d", "dump now"), ("↵↵", "keep in inbox"),
               ("alt+n", "new project"), ("alt+i", "image"), ("esc", "close")]


class DrawerScreen(ModalScreen[None]):
    BINDINGS = [Binding("escape", "close", "", priority=True),
                Binding("tab", "other", "", priority=True),
                Binding("alt+d", "dump", "", priority=True),
                Binding("alt+n", "new", "", priority=True),
                Binding("alt+i", "image", "", priority=True)]
    DEFAULT_CSS = """
    DrawerScreen { align: center bottom; background: #0d1117 25%; }
    #dr-box { width: 100%; height: 55%; background: #0b0f17; border-top: thick #2dd4bf;
              padding: 0 1; }
    #dr-list { height: 1fr; }
    #dr-draft { height: 4; border: none; background: #111a26; }
    #dr-sugg { height: 2; }
    #dr-keys { height: 1; }
    """

    def __init__(self) -> None:
        super().__init__()
        self.inbox = INBOX[0]
        self.choice = 0

    def compose(self):
        with Vertical(id="dr-box"):
            yield Static(id="dr-list")
            yield TextArea("", id="dr-draft", soft_wrap=True)
            yield Static(id="dr-sugg")
            yield Static(id="dr-keys")

    def on_mount(self) -> None:
        see_through(self, 0.25)
        self.docs = docs_of(self.app)
        self.query_one("#dr-draft", TextArea).focus()
        self._paint()

    def on_text_area_changed(self, e) -> None:
        ta = e.text_area
        if ta.text.endswith("\n\n") and ta.text.strip():
            self.inbox.notes.append({"id": f"n{len(self.inbox.notes) + 1}",
                                     "at": NOW.isoformat(timespec="seconds"),
                                     "text": ta.text.strip(), "dumped": None})
            self.inbox.save()
            ta.text = ""
        self.choice = 0
        self._paint()

    def _paint(self) -> None:
        w = self.app.size.width - 4
        rows = []
        t = Text(no_wrap=True)
        t.append("CAPTURE", f"b {ACC}")
        t.append(f"  inbox {len(self.inbox.open_notes())} · ↵↵ files the draft · the board "
                 "stays above", MUT)
        rows.append(t)
        for n in self.inbox.open_notes()[-4:]:
            hits = sg.suggest(n["text"], self.docs)
            ch = options(hits)[0]
            r = Text(no_wrap=True)
            r.append(" • ", DIM)
            r.append(fit(n["text"].split("\n")[0], max(20, w - 40)), HEX["hd"])
            r.append("  → ", DIM)
            r.append_text(hit_text(ch))
            r.truncate(w, overflow="ellipsis")
            rows.append(r)
        self.query_one("#dr-list", Static).update(Text("\n").join(rows))
        draft = self.query_one("#dr-draft", TextArea).text
        s = Text(no_wrap=True)
        why = Text(no_wrap=True)
        if draft.strip():
            opts = options(sg.suggest(draft, self.docs))
            ch = opts[self.choice % len(opts)]
            s.append("→ ", f"b {ACC}")
            s.append_text(hit_text(ch))
            s.append(f"   ⇥ {self.choice % len(opts) + 1}/{len(opts)}", DIM)
            if ch is not None:
                why.append("  why ", DIM)
                why.append(" · ".join(ch.why[:4]), MUT)
            else:
                why.append("  alt+n names it; ⇥ for the weak guesses", MUT)
        else:
            s.append("→ type a note; the project appears here as you write", DIM)
        s.truncate(w, overflow="ellipsis")
        self.query_one("#dr-sugg", Static).update(Text("\n").join([s, why]))
        self.query_one("#dr-keys", Static).update(key_line(DRAWER_KEYS, w))

    def action_other(self) -> None:
        self.choice += 1
        self._paint()

    def action_dump(self) -> None:
        ta = self.query_one("#dr-draft", TextArea)
        if not ta.text.strip():
            return
        opts = options(sg.suggest(ta.text, self.docs))
        ch = opts[self.choice % len(opts)]
        if ch is None:
            return
        self.inbox.notes.append(dump(self.app, self.inbox, ta.text.strip(), ch))
        self.inbox.save()
        ta.text = ""
        self.docs = docs_of(self.app)
        self.app.refresh_view()
        self._paint()

    def action_new(self) -> None:
        self.app.notify("new project: same inline field as the pad (not drawn here)",
                        markup=False)

    def action_image(self) -> None:
        self.query_one("#dr-draft", TextArea).insert(f"\nimg: pasted-{NOW:%H%M}.png")

    def action_close(self) -> None:
        self.dismiss(None)


# =============================================================================
# 1 · C — one line, one note: a capture line and the inbox as a list
# =============================================================================
LINES_KEYS = [("↵", "add"), ("- …", "sub-line"), ("↑↓", "pick"), ("alt+d", "dump"),
              ("alt+o", "other"), ("alt+r", "review all"), ("alt+i", "image"), ("esc", "close")]


class LinesScreen(Screen[None]):
    BINDINGS = [Binding("escape", "close", "", priority=True),
                Binding("up", "move(-1)", "", priority=True),
                Binding("down", "move(1)", "", priority=True),
                Binding("alt+d", "dump", "", priority=True),
                Binding("alt+o", "other", "", priority=True),
                Binding("alt+r", "review", "", priority=True),
                Binding("alt+i", "image", "", priority=True)]
    DEFAULT_CSS = """
    LinesScreen { background: #0d1117; }
    #ln-head { height: 1; padding: 0 1; }
    #ln-body { height: 1fr; padding: 0 1; }
    #ln-in { margin: 0 1; border: tall #2dd4bf 50%; }
    #ln-keys { dock: bottom; height: 1; padding: 0 1; background: #0b0f17; }
    """

    def __init__(self) -> None:
        super().__init__()
        self.inbox = INBOX[0]
        self.sel = len(self.inbox.open_notes()) - 1
        self.choices: dict[str, int] = {}

    def compose(self):
        yield Static(id="ln-head")
        yield Static(id="ln-body")
        yield Input(placeholder="a note per line · start with - to add to the note above",
                    id="ln-in")
        yield Static(id="ln-keys")

    def on_mount(self) -> None:
        self.docs = docs_of(self.app)
        self.query_one("#ln-in", Input).focus()
        self._paint()

    def on_resize(self, _e) -> None:
        self._paint()

    def on_input_submitted(self, e) -> None:
        v = e.value.rstrip()
        e.input.value = ""
        notes = self.inbox.open_notes()
        if not v:
            return
        if v.lstrip().startswith("-") and notes:
            notes[self.sel]["text"] += "\n" + v.strip()
        else:
            self.inbox.notes.append({"id": f"n{len(self.inbox.notes) + 1}",
                                     "at": NOW.isoformat(timespec="seconds"),
                                     "text": v, "dumped": None})
            self.sel = len(self.inbox.open_notes()) - 1
        self.inbox.save()
        self._paint()

    def _paint(self) -> None:
        w = self.app.size.width - 2
        notes = self.inbox.open_notes()
        head = Text(no_wrap=True)
        head.append("INBOX", f"b {ACC}")
        head.append(f"  {len(notes)} notes · one line, one note · the project is "
                    "suggested on the right", MUT)
        self.query_one("#ln-head", Static).update(head)
        wide = w >= 100
        lw = w - 44 if wide else w
        rows = []
        for i, n in enumerate(notes):
            on = i == self.sel
            lines = n["text"].split("\n")
            imgs = [x for x in lines if x.strip().startswith("img:")]
            body = [x for x in lines[1:] if not x.strip().startswith("img:")]
            hits = sg.suggest(n["text"], self.docs)
            opts = options(hits)
            ch = opts[self.choices.get(n["id"], 0) % len(opts)]
            r = Text(no_wrap=True)
            r.append("▶ " if on else "  ", ACC)
            r.append(n["at"][11:16] + "  ", DIM)
            r.append(fit(lines[0], max(10, lw - 14 - (5 if imgs else 0))),
                     f"b {INK}" if on else HEX["hd"])
            if imgs:
                r.append(f" ▣ {len(imgs)}", HEX["amber"])
            if wide:
                r.append("  → ", DIM)
                r.append_text(hit_text(ch, 40))
            rows.append(r)
            subs = body[:2]
            for j in range(max(len(subs), 1 if wide else 0)):
                s = Text(no_wrap=True)
                s.append("         ")
                s.append(fit(subs[j] if j < len(subs) else "", max(10, lw - 9)), MUT)
                if wide and j == 0:
                    if ch is not None:
                        s.append("     why ", DIM)
                        s.append(", ".join(ch.why[:3]), MUT)
                    else:
                        s.append("     no project shares a word", MUT)
                rows.append(s)
            if not wide and on:
                s = Text(no_wrap=True)
                s.append("         → ", ACC)
                s.append_text(hit_text(ch, w - 12))
                rows.append(s)
        self.query_one("#ln-body", Static).update(Text("\n").join(rows))
        self.query_one("#ln-keys", Static).update(key_line(LINES_KEYS, w))

    def action_move(self, d: int) -> None:
        n = len(self.inbox.open_notes())
        if n:
            self.sel = max(0, min(n - 1, self.sel + d))
            self._paint()

    def action_other(self) -> None:
        notes = self.inbox.open_notes()
        if notes:
            k = notes[self.sel]["id"]
            self.choices[k] = self.choices.get(k, 0) + 1
            self._paint()

    def action_dump(self) -> None:
        notes = self.inbox.open_notes()
        if not notes:
            return
        n = notes[self.sel]
        opts = options(sg.suggest(n["text"], self.docs))
        ch = opts[self.choices.get(n["id"], 0) % len(opts)]
        if ch is None:
            return
        self.inbox.notes.remove(n)
        self.inbox.notes.append(dump(self.app, self.inbox, n["text"], ch))
        self.inbox.save()
        self.sel = max(0, self.sel - 1)
        self.docs = docs_of(self.app)
        self._paint()

    def action_review(self) -> None:
        self.app.push_screen(ReviewScreen([n["text"] for n in self.inbox.open_notes()]))

    def action_image(self) -> None:
        notes = self.inbox.open_notes()
        if notes:
            notes[self.sel]["text"] += f"\nimg: pasted-{NOW:%H%M}.png"
            self._paint()

    def action_close(self) -> None:
        self.app.pop_screen()


# =============================================================================
# 1 · the review pass before a batch dump (shared by A and C)
# =============================================================================
REVIEW_KEYS = [("↑↓", "move"), ("␣", "include"), ("o", "other"), ("d", "dump checked"),
               ("esc", "back")]


class ReviewScreen(ModalScreen[None]):
    BINDINGS = [Binding("escape", "close", "", priority=True),
                Binding("up", "move(-1)", "", priority=True),
                Binding("down", "move(1)", "", priority=True),
                Binding("space", "toggle", "", priority=True),
                Binding("o", "other", "", priority=True),
                Binding("d", "dump", "", priority=True)]
    DEFAULT_CSS = """
    ReviewScreen { align: center middle; background: #0d1117 60%; }
    #rv-box { width: 96%; max-width: 112; height: auto; max-height: 90%; background: #0b0f17;
              border: round #2dd4bf; border-title-color: #2dd4bf; padding: 0 1; }
    """

    def __init__(self, texts: list[str]) -> None:
        super().__init__()
        self.texts = texts
        self.row = 0
        self.choice = [0] * len(texts)
        self.on: list[bool] = []

    def compose(self):
        box = Vertical(id="rv-box")
        box.border_title = "Review · dump all"
        with box:
            yield Static(id="rv-body")

    def on_mount(self) -> None:
        see_through(self, 0.6)
        self.docs = docs_of(self.app)
        self.on = [options(sg.suggest(t, self.docs))[0] is not None for t in self.texts]
        self._paint()

    def _paint(self) -> None:
        w = min(110, self.app.size.width - 8)
        tw = max(18, w - 60) if w >= 90 else w - 6
        rows = []
        for i, t in enumerate(self.texts):
            opts = options(sg.suggest(t, self.docs))
            ch = opts[self.choice[i] % len(opts)]
            sel = i == self.row
            r = Text(no_wrap=True)
            r.append("▶ " if sel else "  ", ACC)
            r.append("[x] " if self.on[i] else "[ ] ", f"b {ACC}" if self.on[i] else DIM)
            r.append(fit(t.split("\n")[0], tw), f"b {INK}" if sel else HEX["hd"])
            if w >= 90:
                r.append("  ")
                r.append_text(hit_text(ch, 34))
            rows.append(r)
            s = Text(no_wrap=True)
            s.append("      ")
            if w < 90:
                s.append_text(hit_text(ch, 34))
                s.append("  ")
            if ch is not None:
                s.append("why " + ", ".join(ch.why[:3]), DIM)
            else:
                s.append("needs a name: alt+n in the pad", HEX["amber"])
            s.truncate(w, overflow="ellipsis")
            rows.append(s)
        n = sum(self.on)
        rows.append(Text(""))
        rows.append(key_line([(k, f"dump {n} checked" if k == "d" else v) for k, v in REVIEW_KEYS], w))
        self.query_one("#rv-body", Static).update(Text("\n").join(rows))

    def action_move(self, d: int) -> None:
        self.row = max(0, min(len(self.texts) - 1, self.row + d))
        self._paint()

    def action_toggle(self) -> None:
        self.on[self.row] = not self.on[self.row]
        self._paint()

    def action_other(self) -> None:
        self.choice[self.row] += 1
        self._paint()

    def action_dump(self) -> None:
        self.app.notify(f"Dumped {sum(self.on)} notes (prototype: not written)", markup=False)
        self.dismiss(None)

    def action_close(self) -> None:
        self.dismiss(None)


# =============================================================================
# 2 · the list view: every task of every board in the order it was added
# =============================================================================
class Row(NamedTuple):
    task: Task
    board: object
    bname: str
    bcol: str
    how: str             # "c" the `created` field, "h" history.jsonl, "?" unknown
    at: datetime | None
    pos: int             # place in its board file (append order)
    bi: int


def all_rows(app) -> list[Row]:
    rows = []
    for bi, (bid, name, col, board) in enumerate(boards_of(app)):
        recs, _skip = history.read(board.path)
        born = {}
        for r in recs:
            if r.get("from") is None:
                born.setdefault(r["task"], r["at"])
        for pos, t in enumerate(board.tasks):
            if t.archived:
                continue
            c = t.extra.get("created") if isinstance(t.extra.get("created"), str) else None
            if c:
                rows.append(Row(t, board, name, col, "c", datetime.fromisoformat(c), pos, bi))
            elif t.id in born:
                rows.append(Row(t, board, name, col, "h", datetime.fromisoformat(born[t.id]), pos, bi))
            else:
                rows.append(Row(t, board, name, col, "?", None, pos, bi))
    return rows


def ordered(rows: list[Row], newest: bool) -> list[Row]:
    known = sorted([r for r in rows if r.at], key=lambda r: (r.at, r.bi, r.pos))
    unknown = sorted([r for r in rows if not r.at], key=lambda r: (r.bi, r.pos))
    return (known[::-1] + unknown[::-1]) if newest else (unknown + known)


SINCE = fx.CREATED_SINCE.strftime("%b %d").replace(" 0", " ")


def when(r: Row, short: bool = False) -> tuple[str, str]:
    if r.how == "c":
        return (f"{r.at:%b %d %H:%M}", INK) if not short else (f"{r.at:%H:%M}", INK)
    if r.how == "h":
        return (f"≈{r.at:%b %d %H:%M}", MUT) if not short else (f"≈{r.at:%H:%M}", MUT)
    return (f"? before {SINCE}", DIM) if not short else ("?", DIM)


def day_head(r: Row) -> str:
    if r.at is None:
        return f"ADDED BEFORE {SINCE.upper()} · ORDER UNKNOWN · board file order"
    d = r.at.date()
    tag = "TODAY · " if d == TODAY else "YESTERDAY · " if d == TODAY - timedelta(days=1) else ""
    src = "" if r.how == "c" else "  ≈ from history.jsonl"
    return f"{tag}{d:%a %b %d}".upper() + src


def proj_of(r: Row):
    return next((p for p in r.board.projects if p.id == r.task.project_id), None)


def meta(r: Row, app) -> Text:
    t, out = r.task, Text(no_wrap=True)
    sep = ("  ", DIM)
    out.append(t.phase, HEX["sky"] if t.phase == "Doing" else HEX["done"] if t.phase == "Done" else MUT)
    out.append(*sep)
    out.append({"high": "▲ high", "low": "▽ low"}.get(t.priority, "· normal"),
               HEX["rose"] if t.priority == "high" else DIM)
    if t.start_date or t.due_date:
        out.append(*sep)
        s = (t.start_date or "")[5:].replace("-", "/")
        d = (t.due_date or "")[5:].replace("-", "/")
        out.append(f"{s}→{d}" if s else f"due {d}", HEX["amber"] if t.due_date and
                   t.due_date <= TODAY.isoformat() else MUT)
    if t.milestone:
        m = app.marks.marks.get(t.mark) if t.mark else None
        out.append(*sep)
        out.append(f"{m.shape} {m.name}" if m else "◆ milestone",
                   HEX.get(m.colour, MUT) if m else MUT)
    names = views.mention_names(t, app.people.people)
    if names:
        out.append(*sep)
        out.append(" ".join("@" + n.split()[0] for n in names), f"b {HEX['pink']}")
    if t.urls:
        out.append(*sep)
        out.append(f"🔗{len(t.urls)}", HEX["cyan"])
    if t.images:
        out.append(*sep)
        out.append(f"▣ {len(t.images)}", HEX["amber"])
    return out


def proj_chip(r: Row, w: int, pad: bool = True) -> Text:
    p = proj_of(r)
    t = Text(no_wrap=True)
    name = p.name if p else "Inbox"
    t.append(fit(name, max(6, w - 11)) if pad else name, ph(p))
    t.append(" · " + fit(r.bname, 8), board_hex(r.bcol))
    return t


def source_line(r: Row) -> str:
    """Where the row's place in the list comes from, said honestly."""
    if r.how == "c":
        return f"added {r.at:%a %b %d · %H:%M} · the created field"
    if r.how == "h":
        return f"added ≈ {r.at:%a %b %d · %H:%M} · from history.jsonl (its first phase record)"
    return f"added: unknown, before {SINCE} · #{r.pos + 1} in {r.bname}'s board file"


def first_note(t: Task) -> str:
    for ln in (t.notes or "").split("\n"):
        if ln.strip():
            return ln.strip()
    return ""


class ListBase(Screen[None]):
    BINDINGS = [Binding("escape,N", "back", "", priority=True),
                Binding("up,k", "move(-1)", "", priority=True),
                Binding("down,j", "move(1)", "", priority=True),
                Binding("o", "order", "", priority=True),
                Binding("space", "expand", "", priority=True),
                Binding("enter", "open", "", priority=True)]
    DEFAULT_CSS = """
    ListBase { background: #0d1117; overflow-y: hidden; }
    #ls-body { height: 1fr; padding: 0 1; }
    #ls-keys { dock: bottom; height: 1; padding: 0 1; background: #0b0f17; }
    """
    KEYS: list = []

    def __init__(self) -> None:
        super().__init__()
        self.newest, self.sel, self.open_ids = True, 0, set()

    def compose(self):
        yield Static(id="ls-body")
        yield Static(id="ls-keys")

    def on_mount(self) -> None:
        self.rows = all_rows(self.app)
        self._paint()

    def on_resize(self, _e) -> None:
        self._paint()

    def items(self) -> list[Row]:
        return ordered(self.rows, self.newest)

    def head(self, w: int) -> Text:
        t = Text(no_wrap=True)
        t.append("ADDED", f"b {ACC}")
        t.append(f"  {len(self.rows)} tasks · every board · ", MUT)
        t.append("newest first" if self.newest else "oldest first", f"b {INK}")
        t.append("  ·  time = created  ≈ = history  ? = unknown", DIM)
        t.truncate(w, overflow="ellipsis")
        return t

    def _paint(self) -> None:
        w = self.app.size.width - 2
        h = self.app.size.height - 1
        self.query_one("#ls-body", Static).update(self.body(w, h))
        self.query_one("#ls-keys", Static).update(key_line(self.KEYS, w))

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_move(self, d: int) -> None:
        self.sel = max(0, min(len(self.rows) - 1, self.sel + d))
        self._paint()

    def action_order(self) -> None:
        self.newest = not self.newest
        self.sel = 0
        self._paint()

    def action_expand(self) -> None:
        tid = self.items()[self.sel].task.id
        self.open_ids ^= {tid}
        self._paint()

    def action_open(self) -> None:
        r = self.items()[self.sel]
        self.app.pop_screen()
        self.app.selected_task_id = r.task.id
        self.app.refresh_view()


def window(lines: list[tuple[Text, int]], sel: int, h: int) -> list[Text]:
    """Scroll so the selected row's lines are on screen; `lines` = (text, row index)."""
    first = next((i for i, (_t, r) in enumerate(lines) if r == sel), 0)
    last = max((i for i, (_t, r) in enumerate(lines) if r == sel), default=0)
    top = 0
    if last >= h:
        top = min(first - 1, last - h + 2)
    return [t for t, _r in lines[max(0, top):max(0, top) + h]]


class ListA(ListBase):
    """A · a ledger: two lines a task, `space` unfolds the whole note inline."""
    KEYS = [("↑↓", "move"), ("␣", "unfold"), ("↵", "open on board"), ("o", "newest/oldest"),
            ("esc / N", "back")]

    def body(self, w: int, h: int) -> Text:
        out: list[tuple[Text, int]] = [(self.head(w), -1), (Text(""), -1)]
        last_head = None
        cw = 30 if w >= 100 else 22
        for i, r in enumerate(self.items()):
            dh = day_head(r)
            if dh != last_head:
                hd = Text(no_wrap=True)
                hd.append("── " + dh + " ", f"b {HEX['hd']}" if r.at else f"b {DIM}")
                hd.append("─" * max(0, w - hd.cell_len), HEX["frame"])
                out.append((hd, i))
                last_head = dh
            on = i == self.sel
            wt, tone = when(r, short=w < 100)
            ln = Text(no_wrap=True)
            ln.append("▶ " if on else "  ", ACC)
            wcol = 16 if w >= 100 else 10
            ln.append(fit(wt, wcol), tone)
            tw = w - wcol - cw - 4
            ln.append(fit(r.task.title, tw), f"b {INK}" if on else HEX["hd"])
            ln.append("  ")
            ln.append_text(proj_chip(r, cw))
            out.append((ln, i))
            m = Text(no_wrap=True)
            m.append(" " * (wcol + 2))
            m.append_text(meta(r, self.app))
            fn = first_note(r.task)
            if fn and r.task.id not in self.open_ids:
                m.append("   " + fn, DIM)
            m.truncate(w, overflow="ellipsis")
            out.append((m, i))
            if r.task.id in self.open_ids:
                pad = " " * (wcol + 2)
                nt = views.notes_text(r.task.notes, self.app.people.people)
                for nl in nt.split("\n"):
                    x = Text(pad + "│ ", HEX["frame"], no_wrap=True)
                    x.append_text(nl)
                    x.truncate(w, overflow="ellipsis")
                    out.append((x, i))
                for u in r.task.urls:
                    out.append((Text(pad + "│ 🔗 " + u, HEX["cyan"], no_wrap=True), i))
                for im in r.task.images:
                    out.append((Text(pad + "│ ▣ " + Path(im).name, HEX["amber"], no_wrap=True), i))
                src = source_line(r)
                out.append((Text(pad + "└ " + src, DIM, no_wrap=True), i))
        return Text("\n").join(window(out, self.sel, h))


class ListB(ListBase):
    """B · a narrow list and a detail pane with everything about the cursor's task."""
    KEYS = [("↑↓", "move"), ("↵", "open on board"), ("o", "newest/oldest"), ("esc / N", "back")]

    def body(self, w: int, h: int) -> Text:
        lw = 46 if w >= 100 else 34
        rw = w - lw - 3
        left: list[tuple[Text, int]] = []
        last_head = None
        for i, r in enumerate(self.items()):
            dh = day_head(r).split(" · ")[0] if r.at else f"BEFORE {SINCE.upper()} · ?"
            if r.at and r.how == "h":
                dh = f"{r.at:%a %b %d}".upper() + " ≈"
            if dh != last_head:
                left.append((Text(fit(dh, lw), f"b {HEX['hd']}" if r.at else f"b {DIM}"), i))
                last_head = dh
            on = i == self.sel
            wt, tone = when(r, short=True)
            ln = Text(no_wrap=True)
            ln.append("▶" if on else " ", ACC)
            ln.append(fit(wt, 7), tone)
            p = proj_of(r)
            ln.append("▍", ph(p))
            ln.append(fit(r.task.title, lw - 9), f"b {INK}" if on else HEX["hd"])
            left.append((ln, i))
        lrows = window(left, self.sel, h - 2)
        r = self.items()[self.sel]
        t = r.task
        right: list[Text] = []
        tt = Text(no_wrap=True)
        tt.append(t.title, f"b {INK}")
        right.append(tt)
        right.append(proj_chip(r, rw))
        right.append(meta(r, self.app))
        src = source_line(r)
        right.append(Text(src, MUT if r.how != "?" else DIM))
        right.append(Text("─" * rw, HEX["frame"]))
        nt = views.notes_text(t.notes, self.app.people.people) if t.notes else Text("no notes", DIM)
        for nl in nt.wrap(self.app.console, rw):
            right.append(nl)
        for u in t.urls:
            right.append(Text("🔗 " + u, HEX["cyan"]))
        for im in t.images:
            right.append(Text("▣ " + Path(im).name, HEX["amber"]))
        if t.depends_on:
            right.append(Text("after: " + ", ".join(next((x.title for x in r.board.tasks if x.id == d), d)
                                                    for d in t.depends_on), MUT))
        head = self.head(w)
        out = [head, Text("")]
        for k in range(h - 2):
            ln = Text(no_wrap=True)
            ln.append_text(lrows[k] if k < len(lrows) else Text(""))
            ln.pad_right(lw - ln.cell_len) if ln.cell_len < lw else ln.truncate(lw)
            ln.append(" │ ", HEX["frame"])
            if k < len(right):
                rr = right[k].copy()
                rr.truncate(rw, overflow="ellipsis")
                ln.append_text(rr)
            out.append(ln)
        return Text("\n").join(out)


class ListC(ListBase):
    """C · a logbook: a time spine, every entry with all its lines, nothing to unfold."""
    KEYS = [("↑↓", "move"), ("↵", "open on board"), ("o", "newest/oldest"), ("esc / N", "back")]

    def body(self, w: int, h: int) -> Text:
        out: list[tuple[Text, int]] = [(self.head(w), -1)]
        last_head = None
        for i, r in enumerate(self.items()):
            dh = day_head(r)
            if dh != last_head:
                out.append((Text(""), i))
                hd = Text(no_wrap=True)
                hd.append("      ╭ ", HEX["frame"])
                hd.append(dh, f"b {HEX['hd']}" if r.at else f"b {DIM}")
                out.append((hd, i))
                last_head = dh
            on = i == self.sel
            wt, tone = when(r, short=True)
            p = proj_of(r)
            ln = Text(no_wrap=True)
            ln.append(fit(wt, 6, "right"), tone)
            ln.append(" ● " if on else " ○ ", ACC if on else ph(p))
            ln.append(r.task.title, f"b {INK}" if on else f"b {HEX['hd']}")
            ln.append("   ")
            ln.append_text(proj_chip(r, 30, pad=False))
            ln.truncate(w, overflow="ellipsis")
            out.append((ln, i))
            m = Text("       │ ", HEX["frame"], no_wrap=True)
            m.append_text(meta(r, self.app))
            m.truncate(w, overflow="ellipsis")
            out.append((m, i))
            nt = views.notes_text(r.task.notes, self.app.people.people) if r.task.notes else None
            if nt is not None:
                for nl in nt.split("\n")[:3]:
                    x = Text("       │   ", HEX["frame"], no_wrap=True)
                    x.append_text(nl)
                    x.truncate(w, overflow="ellipsis")
                    out.append((x, i))
        return Text("\n").join(window(out, self.sel, h))


# =============================================================================
# 3 · multicolour notes: one tokeniser with six pens, and three ways to switch pen
# =============================================================================
PENS = [("==", "soon", "yellow"), ("!!", "over", "red"), ("++", "green", "green"),
        ("::", "blue", "blue"), ("^^", "violet", "violet"), ("%%", "orange", "orange")]
_PEN_RE = re.compile("|".join(f"{re.escape(m)}(.*?){re.escape(m)}" for m, _t, _n in PENS))
_ORIG_SEG = views.highlight_segments


def highlight_segments_6(text: str) -> list[tuple[str, str]]:
    """The one tokeniser, six pens: today's three pairs plus `::blue::`, `^^violet^^`,
    `%%orange%%` (D4) — (segment, tone) pairs, markers dropped, never across a line."""
    out, last = [], 0
    for m in _PEN_RE.finditer(text):
        if m.start() > last:
            out.append((text[last:m.start()], "mut"))
        k = next(i for i in range(len(PENS)) if m.group(i + 1) is not None)
        out.append((m.group(k + 1), PENS[k][1]))
        last = m.end()
    if last < len(text):
        out.append((text[last:], "mut"))
    return out


def pen_legend(cur: int | None = None, keys: bool = False) -> str:
    """The editor's Notes label (markup, constant text only)."""
    parts = []
    for i, (m, tone, name) in enumerate(PENS):
        k = f"{i + 1} " if keys else ""
        style = f"b {HEX[tone]} reverse" if cur == i else HEX[tone]
        parts.append(f"[{style}]{k}{name}[/]")
    return " ".join(parts)


def pen_dots(cur: int | None = None, keys: bool = False) -> str:
    """The pens as coloured dots (with their alt+number), the current one reversed."""
    parts = []
    for i, (_m, tone, _n) in enumerate(PENS):
        style = f"b #0d1117 on {HEX[tone]}" if cur == i else f"b {HEX[tone]}"
        parts.append(f"[{style}]{f'{i + 1}' if keys else ''}●[/]")
    return ("" if keys else " ").join(parts) if not keys else " ".join(parts)


def live_ink(ta: TextArea) -> None:
    """Variant B's editor shows the ink as typed: the TextArea's own highlight map is
    filled from the tokeniser (markers dimmed, the text in its pen)."""
    theme = ta._theme
    if theme is not None:
        for _m, tone, _n in PENS:
            from rich.style import Style
            theme.syntax_styles[f"pen.{tone}"] = Style(color=HEX[tone], bold=True)
        theme.syntax_styles["pen.mark"] = Style(color=HEX["dim"])

    def build() -> None:
        ta._line_cache.clear()
        hl = ta._highlights
        hl.clear()
        for row, line in enumerate(ta.text.split("\n")):
            b = line.encode("utf-8")
            for m in _PEN_RE.finditer(line):
                k = next(i for i in range(len(PENS)) if m.group(i + 1) is not None)
                s, e = len(line[:m.start()].encode()), len(line[:m.end()].encode())
                hl[row].append((s, s + 2, "pen.mark"))
                hl[row].append((s + 2, e - 2, f"pen.{PENS[k][1]}"))
                hl[row].append((e - 2, e, "pen.mark"))
            del b
    ta._build_highlight_map = build
    build()
    ta.refresh()


class EditorA(modals.TaskModal):
    """A · six marker pairs; `alt+c` wraps the word at the cursor (or the selection) and
    each further press moves it to the next pen, then back to plain."""
    BINDINGS = [Binding("alt+c", "pen_cycle", "", priority=True)]

    def on_mount(self) -> None:
        super().on_mount()
        self.query(".task-sec").first().update(
            "Notes  [dim]alt+c colours the word:[/dim] " + pen_dots() + " [dim]▸ none[/dim]")

    def action_pen_cycle(self) -> None:
        ta = self.query_one("#f-notes", TextArea)
        row, col = ta.cursor_location
        line = ta.document.get_line(row)
        for m in _PEN_RE.finditer(line):
            if m.start() <= col <= m.end():
                k = next(i for i in range(len(PENS)) if m.group(i + 1) is not None)
                inner = m.group(k + 1)
                new = inner if k == len(PENS) - 1 else PENS[k + 1][0] + inner + PENS[k + 1][0]
                ta.replace(new, (row, m.start()), (row, m.end()))
                ta.move_cursor((row, m.start() + len(new)))
                return
        a = col
        while a > 0 and not line[a - 1].isspace():
            a -= 1
        b = col
        while b < len(line) and not line[b].isspace():
            b += 1
        if a == b:
            return
        mk = PENS[0][0]
        ta.replace(mk + line[a:b] + mk, (row, a), (row, b))
        ta.move_cursor((row, b + 4))


class EditorB(modals.TaskModal):
    """B · pens: `alt+1..6` picks the pen and what you type next is in it; `alt+0` lifts
    it. The pen opens a pair at the cursor and types inside it; the notes field shows
    the ink as typed."""
    BINDINGS = ([Binding(f"alt+{i + 1}", f"pen({i})", "", priority=True) for i in range(6)]
                + [Binding("alt+0", "pen(-1)", "", priority=True)])

    def on_mount(self) -> None:
        super().on_mount()
        self.pen = None
        live_ink(self.query_one("#f-notes", TextArea))
        self._label()

    def _label(self) -> None:
        cur = Text()
        if self.pen is None:
            chip = "[dim]pen: none[/dim]"
        else:
            _m, tone, name = PENS[self.pen]
            chip = f"[b #0d1117 on {HEX[tone]}] ✎ {name} [/]"
        self.query(".task-sec").first().update(
            f"Notes  {chip} [dim]alt+[/dim]" + pen_dots(self.pen, keys=True) + " [dim]0 off[/dim]")
        del cur

    def on_text_area_changed(self, event) -> None:
        super().on_text_area_changed(event)
        if event.text_area.id == "f-notes":
            event.text_area._build_highlight_map()

    def action_pen(self, i: int) -> None:
        ta = self.query_one("#f-notes", TextArea)
        row, col = ta.cursor_location
        line = ta.document.get_line(row)
        if self.pen is not None:                 # step out of the open pair
            mk = PENS[self.pen][0]
            if line[col:col + 2] == mk:
                ta.move_cursor((row, col + 2))
                col += 2
        self.pen = None if i < 0 else i
        if self.pen is not None:
            mk = PENS[self.pen][0]
            ta.insert(mk + mk)
            ta.move_cursor((row, col + 2))
        self._label()


class Swatch(ModalScreen[str | None]):
    BINDINGS = ([Binding(k, f"pick({i})", "", priority=True) for i, k in enumerate("yrgbvo")]
                + [Binding("x", "pick(-1)", "", priority=True),
                   Binding("escape", "cancel", "", priority=True)])
    DEFAULT_CSS = """
    Swatch { background: #0d1117 20%; }
    #sw-box { width: 22; height: auto; background: #0b0f17; border: round #2dd4bf;
              border-title-color: #2dd4bf; padding: 0 1; }
    """

    def __init__(self, at) -> None:
        super().__init__()
        self.at = at

    def compose(self):
        box = Vertical(id="sw-box")
        box.border_title = "colour"
        with box:
            t = Text()
            for i, (_m, tone, name) in enumerate(PENS):
                t.append(f" {'yrgbvo'[i]} ", f"b {HEX['bright']}")
                t.append("██ ", HEX[tone])
                t.append(name + "\n", HEX[tone])
            t.append(" x ", f"b {HEX['bright']}")
            t.append("   none\n", MUT)
            t.append(" esc", f"b {HEX['bright']}")
            t.append(" cancel", MUT)
            yield Static(t)

    def on_mount(self) -> None:
        see_through(self, 0.2)
        box = self.query_one("#sw-box")
        x, y = self.at
        box.styles.offset = (max(0, min(x, self.app.size.width - 24)),
                             max(0, min(y + 1, self.app.size.height - 11)))

    def action_pick(self, i: int) -> None:
        self.dismiss(str(i))

    def action_cancel(self) -> None:
        self.dismiss(None)


class EditorC(modals.TaskModal):
    """C · select, then colour: `alt+c` on a selection opens a swatch with a key per pen."""
    BINDINGS = [Binding("alt+c", "swatch", "", priority=True)]

    def on_mount(self) -> None:
        super().on_mount()
        self.query(".task-sec").first().update(
            "Notes  [dim]select (shift+←→) then alt+c: a key per colour[/dim]")

    def action_swatch(self) -> None:
        ta = self.query_one("#f-notes", TextArea)
        if ta.selection.is_empty:
            self.notify("Select some text first (shift+arrows).", markup=False)
            return
        off = ta.cursor_screen_offset
        self.app.push_screen(Swatch((off.x - 10, off.y)), self._picked)

    def _picked(self, res) -> None:
        if res is None:
            return
        ta = self.query_one("#f-notes", TextArea)
        sel = ta.selection
        start, end = sorted([sel.start, sel.end])
        text = ta.get_text_range(start, end)
        for m, _t, _n in PENS:                   # an already-coloured selection is re-inked
            if text.startswith(m) and text.endswith(m) and len(text) >= 4:
                text = text[2:-2]
        i = int(res)
        new = text if i < 0 else PENS[i][0] + text + PENS[i][0]
        ta.replace(new, start, end)


def report_html_snippet(text: str, people: dict) -> str:
    """The HTML report's notes for `text`, through the shipped `notes_html` with the
    six-pen tokeniser — what the page embeds as the report's rendering."""
    old = report_html.highlight_segments
    report_html.highlight_segments = highlight_segments_6
    try:
        return report_html.notes_html(text, people)
    finally:
        report_html.highlight_segments = old


# =============================================================================
# the app and the scenes
# =============================================================================
def sel(tid: str):
    def step(app):
        app.selected_task_id = tid
        app.refresh_view()
    return step


def notes_end(app) -> None:
    ta = app.screen.query_one("#f-notes", TextArea)
    ta.focus()
    ta.move_cursor(ta.document.end)


def typed(s: str) -> list[str]:
    return [["enter" if ch == "\n" else "space" if ch == " " else ch for ch in s]]


class Proto(TaskboardApp):
    BINDINGS = [Binding("n", "capture", "", show=False),       # prototype: not in KEYMAP
                Binding("N", "added", "", show=False)]
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, scene: str, root: Path, seconds: float | None = None):
        sc = SCENES[scene]
        self.scene, self._steps, self._seconds = scene, sc["steps"], seconds
        self.played = False
        self._root = root
        fx.build(root, last=sc.get("last", "client-a"))
        INBOX[0] = Inbox(root)
        reg = Registry.load(root / "boards.json", root / "board.json")
        entry = reg.opening()
        reg.touch(entry.id, datetime.now())
        self._capture = sc.get("capture")
        self._added = sc.get("added")
        self._undo_patch = []
        patch = dict(sc.get("patch", {}))
        if sc.get("pens"):
            patch[(views, "highlight_segments")] = highlight_segments_6
            patch[(report_html, "highlight_segments")] = highlight_segments_6
        for (mod, name), val in patch.items():
            self._undo_patch.append((mod, name, getattr(mod, name)))
            setattr(mod, name, val)
        super().__init__(board_path=entry.path, registry=reg, team_sync_interval=1e9)

    def unpatch(self) -> None:
        for mod, name, val in reversed(self._undo_patch):
            setattr(mod, name, val)

    def check_action(self, action, parameters):
        if action == "capture":
            return self._capture is not None and len(self.screen_stack) == 1
        if action == "added":
            return self._added is not None and len(self.screen_stack) == 1
        return super().check_action(action, parameters)

    def action_capture(self) -> None:
        self.push_screen(self._capture())

    def action_added(self) -> None:
        self.push_screen(self._added())

    def on_mount(self) -> None:          # runs BEFORE TaskboardApp.on_mount (MRO dispatch)
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.set_timer(1.0, lambda: self.run_worker(self._play()))

    async def _play(self) -> None:
        for step in self._steps:
            if isinstance(step, str):
                await self._press_keys([step])
            elif isinstance(step, list):
                await self._press_keys(step)
            else:
                r = step(self)
                if inspect.isawaitable(r):
                    await r
            await asyncio.sleep(0.25)
        await asyncio.sleep(0.6)
        self.played = True
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            ok = self.check_state()
            Path(ready).write_text(f"{self._root}\n{'OK' if ok else 'BAD'} {self.screen_stack!r} "
                                   f"view={self.view_mode} sel={self.selected_task_id}",
                                   encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)

    def check_state(self) -> bool:
        want = SCENES[self.scene]["end"]
        return type(self.screen).__name__ == want


TM = (app_mod, "TaskModal")
EDIT = ["escape", sel("tca"), "e", notes_end]
NEW_NOTE = "\n\n" + fx.INBOX_LIVE
SCENES: dict[str, dict] = {
    # 1 · quick capture
    "cap-now": dict(steps=["escape", "4", "a"], end="TaskModal"),
    "cap-A": dict(steps=["escape", "n"] + typed(fx.INBOX_LIVE), capture=PadScreen, end="PadScreen"),
    "cap-A-dump": dict(steps=["escape", "n"] + typed(fx.INBOX_LIVE) + ["alt+d"],
                       capture=PadScreen, end="PadScreen"),
    "cap-A-new": dict(steps=["escape", "n", "up", "up", "alt+n"] + typed("Contracts Q&A pilot"),
                      capture=PadScreen, end="PadScreen"),
    "cap-B": dict(steps=["escape", "4", "n"] + typed(fx.INBOX_LIVE), capture=DrawerScreen,
                  end="DrawerScreen"),
    "cap-B-tab": dict(steps=["escape", "4", "n"] + typed(fx.INBOX_LIVE) + ["tab"],
                      capture=DrawerScreen, end="DrawerScreen"),
    "cap-C": dict(steps=["escape", "n"] + typed(fx.INBOX_LIVE) + ["enter"]
                  + typed("- ask @elena.vidal for the date") + ["enter"],
                  capture=LinesScreen, end="LinesScreen"),
    "cap-C-rev": dict(steps=["escape", "n"] + typed(fx.INBOX_LIVE) + ["enter", "alt+r", "down"],
                      capture=LinesScreen, end="ReviewScreen"),
    # 2 · the list view in the order tasks were added
    "ls-now": dict(steps=["escape", "2"], end="Screen"),
    "ls-A": dict(steps=["escape", "N", "down", "down"], added=ListA, end="ListA"),
    "ls-A-open": dict(steps=["escape", "N", "down", "down", "down", "space"], added=ListA,
                      end="ListA"),
    "ls-A-old": dict(steps=["escape", "N", "o", "down", "space"], added=ListA, end="ListA"),
    "ls-B": dict(steps=["escape", "N", "down", "down", "down"], added=ListB, end="ListB"),
    "ls-C": dict(steps=["escape", "N", "down"], added=ListC, end="ListC"),
    # 3 · multicolour notes
    "col-now-ed": dict(steps=EDIT, end="TaskModal"),
    "col-now-det": dict(steps=["escape", sel("tca"), "enter"], end="TaskDetails"),
    "col-A-ed": dict(steps=EDIT + typed("\n- confirm the venue") + ["alt+c", "alt+c", "alt+c", "alt+c"],
                     patch={TM: EditorA}, pens=True, end="EditorA"),
    "col-B-ed": dict(steps=EDIT + typed("\n- ") + ["alt+4"] + typed("call the venue") + ["alt+0"]
                     + typed(", then ") + ["alt+2"] + typed("pay the deposit"),
                     patch={TM: EditorB}, pens=True, end="EditorB"),
    "col-C-ed": dict(steps=EDIT + typed("\n- send the invoice by friday") + ["shift+left"] * 9
                     + ["alt+c"], patch={TM: EditorC}, pens=True, end="Swatch"),
    "col-C-done": dict(steps=EDIT + typed("\n- send the invoice by friday") + ["shift+left"] * 9
                       + ["alt+c", "r"], patch={TM: EditorC}, pens=True, end="EditorC"),
    "col-all-det": dict(steps=["escape", sel("tca"), "enter"], pens=True, end="TaskDetails"),
    "col-all-pr": dict(steps=["escape", sel("tca"), "R", "2"], pens=True, end="PresentScreen"),
}
SIZES = [(118, 30), (80, 24)]


def _strip_font(svg: str) -> str:
    return re.sub(r"@font-face\s*\{[^}]*\}", "", svg)


async def _shot_one(scene: str, size) -> None:
    root = Path(tempfile.mkdtemp(prefix="cp-svg-"))
    app = Proto(scene, root)
    try:
        async with app.run_test(size=size) as pilot:
            for _ in range(300):
                if app.played:
                    break
                await pilot.pause(0.1)
            await pilot.pause(0.3)
            ok = app.check_state()
            svg = app.export_screenshot(title=f"taskboard · {scene} · {size[0]}x{size[1]}")
            (OUT / "svg" / f"{scene}_{size[0]}x{size[1]}.svg").write_text(
                _strip_font(svg), encoding="utf-8")
            print("svg", scene, size, "OK" if ok else f"BAD {type(app.screen).__name__}")
    finally:
        app.unpatch()
        shutil.rmtree(root, ignore_errors=True)


def shot(names: list[str]) -> None:
    (OUT / "svg").mkdir(parents=True, exist_ok=True)
    for name in names or list(SCENES):
        for size in SIZES:
            asyncio.run(_shot_one(name, size))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
    elif args and args[0] == "shot":
        shot(args[1:])
    elif args and args[0] in ("live", "play"):
        root = Path(tempfile.mkdtemp(prefix="cp-cap-"))
        try:
            secs = float(args[2]) if args[0] == "live" and len(args) > 2 else None
            Proto(args[1], root, secs).run()
        finally:
            shutil.rmtree(root, ignore_errors=True)
    else:
        print(__doc__)
