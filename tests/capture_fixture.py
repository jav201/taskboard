"""Synthetic boards, stores and pilot helpers for Inc K, the capture view (`n`).

Three fixtures, all synthetic (owner `username_subject`, no real person):

* **F** (`f_lanes`, `f_marks`, `build_f`) — G-T's executed fixture (graph-proto-T §Fixture F, adopted
  by graph-proto-V): lane 0 `Client A` (colour sky, THE OPEN BOARD, phases Backlog/Doing/Done,
  projects `Eval harness` pe blue and `Pilot rollout` pr indigo, eight tasks) and lane 1 `Course`
  (colour violet, phases Todo/Doing/Done, project `Module 4 · Volumes` pv violet, three tasks); the
  marks M (`payment`, `release`). `f_lanes` builds the lanes in memory (layer 0 of suggest.py);
  `build_f` writes them as the app's registry under `<home>/.taskboard` (`S`) for the pilots.
* **S** (`build_s`) — G-S's layer-0 fixture (graph-proto-S head): `S/a/board.json` "Client A"
  (projects pe "Eval harness" lime, pp "Pilot rollout" green, phases Backlog/Doing/Done) and
  `S/c/board.json` "Course" (project pm "Module 4 · Volumes" sky, task tc1 "Old one", phases
  Todo/Doing/Done); new task ids patched to t0000001, t0000002, … (`seq_ids`).
* the store helpers (`write_store`, `read_store`, `entry`) — `inbox.json` as LLR-4407.2/.3 shape it.

WHY these helpers exist: every Inc K name (`taskboard.inbox`, `taskboard.suggest`, `CaptureView`,
`PadArea`, `ReviewList`) is new, so the tests reach them only through `inbox()`, `suggest()`, `need`
and `app_class`, which turn their absence on the base revision (545c18a) into an assertion failure
with a message — never an ImportError at collection.
"""
from __future__ import annotations

import hashlib
import importlib
import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from taskboard.models import Board, Project, Task

STAMP_RE = r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d$"
W118, W80 = (118, 30), (80, 24)

# --------------------------------------------------------------------------- #
# new names, reached without an import (RED on base is an assertion, not an error)
# --------------------------------------------------------------------------- #
_MISSING = object()


def module(name: str):
    """`taskboard.<name>` imported, or a test failure saying it is not built yet."""
    try:
        return importlib.import_module(f"taskboard.{name}")
    except ModuleNotFoundError as exc:
        if exc.name == f"taskboard.{name}":
            pytest.fail(f"taskboard.{name} missing (not built yet)")
        raise


def inbox():
    return module("inbox")


def suggest():
    return module("suggest")


def need(mod, name: str):
    """`mod.name` (mod a module or the short name "inbox"/"suggest"/"app"), or a failure."""
    if isinstance(mod, str):
        mod = module(mod)
    obj = getattr(mod, name, _MISSING)
    if obj is _MISSING:
        pytest.fail(f"{mod.__name__}.{name} missing (not built yet)")
    return obj


def app_class(name: str):
    from taskboard import app as app_module
    return need(app_module, name)


# --------------------------------------------------------------------------- #
# Fixture F (graph-proto-T §Fixture F) — in memory and on disk
# --------------------------------------------------------------------------- #
N1 = ("Golden set: 12 questions still have no answer key\n"
      "ask @username_subject which stores count")
N2 = "Volume lab fails on WSL\nthe oracle script expects /mnt/c\nimg: board-0938.png"
N3 = "Quote for the new client: contracts Q&A\ntwo weeks, fixed price"
N4 = "Steering deck: demo the hybrid search on pilot stores"
N5 = "Answer the region chair"
N2_TITLE = "Volume lab fails on WSL"
N1_TITLE = "Golden set: 12 questions still have no answer key"


def f_marks() -> dict:
    from taskboard.marks import Mark
    return {"payment": Mark("payment", "Payment", "▲", "amber"),
            "release": Mark("release", "Release", "★", "cyan")}


def f_client_a(path: Path) -> Board:
    pe = Project("Eval harness", "blue", id="pe")
    pr = Project("Pilot rollout", "indigo", id="pr")
    tasks = [
        Task("Question bank", project_id="pe", phase="Backlog",
             notes="40 questions; each needs a key from @username_subject", id="a1"),
        Task("Judge rubric", project_id="pe", phase="Backlog", id="a2"),
        Task("Eval report v1", project_id="pe", phase="Doing", due_date="2026-11-20",
             milestone=True, mark="release", id="a3"),
        Task("Pilot store list", project_id="pr", phase="Backlog",
             notes="six stores, two per region", id="a4"),
        Task("Steering committee", project_id="pr", phase="Doing",
             notes="@username_subject chairs; demo hybrid search on pilot stores", id="a5"),
        Task("Invoice October", project_id="pr", phase="Backlog", due_date="2026-11-30",
             milestone=True, mark="payment", id="a6"),
        Task("Loose idea zebra", phase="Backlog", id="a7"),
        Task("Old golden set", project_id="pe", phase="Done", archived=True, id="a8"),
    ]
    return Board([pe, pr], tasks, path, {}, ["Backlog", "Doing", "Done"])


def f_course(path: Path) -> Board:
    pv = Project("Module 4 · Volumes", "violet", id="pv")
    tasks = [
        Task("Volume oracle script", project_id="pv", phase="Todo", notes="check on Windows",
             id="c1"),
        Task("Bind vs named volumes page", project_id="pv", phase="Doing",
             notes="the oracle prints the inode", id="c2"),
        Task("Module 4 publish", project_id="pv", phase="Todo", due_date="2026-11-25",
             milestone=True, mark="release", id="c3"),
    ]
    return Board([pv], tasks, path, {}, ["Todo", "Doing", "Done"])


def f_lanes(root: Path) -> list:
    """The lanes `board_lanes` would return for fixture F (in memory, never saved)."""
    a = f_client_a(root / "boards" / "client-a" / "board.json")
    c = f_course(root / "boards" / "course" / "board.json")
    return [("Client A", "sky", a, ""), ("Course", "violet", c, "")]


def settings() -> dict:
    from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION
    return {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
            "seen_view_renumber_2026_07": True}


def f_paths(home: Path) -> dict:
    return {"S": home, "A": home / "boards" / "client-a" / "board.json",
            "C": home / "boards" / "course" / "board.json",
            "store": home / "inbox.json", "images": home / "inbox-images",
            "people": home / "people.json", "marks": home / "marks.json",
            "registry": home / "boards.json"}


def build_f(home: Path, extra_boards: list | None = None, last: str = "client-a",
            course: bool = True) -> dict:
    """Write fixture F as the app's registry under `home` (= `<Path.home()>/.taskboard`).
    `extra_boards`: (id, name, colour, Board | None) appended in that order (None: a registry
    entry whose file does not exist). Returns `f_paths(home)`."""
    p = f_paths(home)
    home.mkdir(parents=True, exist_ok=True)
    a = f_client_a(p["A"])
    a.settings = settings()
    a.save()
    entries = [{"id": "client-a", "name": "Client A", "color": "sky",
                "path": str(p["A"].resolve()), "last_opened": "2026-11-01T07:00",
                "archived": False}]
    (p["A"].parent / "history.jsonl").write_text(
        json.dumps({"task": "a1", "from": None, "to": "Backlog",
                    "at": "2026-10-28T10:30:00"}) + "\n", encoding="utf-8")
    if course:
        c = f_course(p["C"])
        c.settings = settings()
        c.save()
        (p["C"].parent / "history.jsonl").write_text(
            json.dumps({"task": "c1", "from": None, "to": "Todo",
                        "at": "2026-10-29T12:00:00"}) + "\n", encoding="utf-8")
        entries.append({"id": "course", "name": "Course", "color": "violet",
                        "path": str(p["C"].resolve()), "last_opened": "2026-10-31T20:00",
                        "archived": False})
    for bid, name, colour, board in extra_boards or []:
        path = home / "boards" / bid / "board.json"
        if board is not None:
            board.path = path
            board.settings = settings()
            board.save()
        entries.append({"id": bid, "name": name, "color": colour,
                        "path": str(path.resolve()), "last_opened": "2026-10-30T20:00",
                        "archived": False})
    p["registry"].write_text(json.dumps({"version": 1, "last": last, "boards": entries},
                                        indent=2), encoding="utf-8")
    p["marks"].write_text(json.dumps(
        {"version": 1, "marks": [{"id": "payment", "name": "Payment", "shape": "▲",
                                  "colour": "amber"},
                                 {"id": "release", "name": "Release", "shape": "★",
                                  "colour": "cyan"}]}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    p["people"].write_text(json.dumps(
        {"version": 1, "people": [{"id": "username_subject", "name": "Username Subject"}]},
        indent=2), encoding="utf-8")
    return p


def sha(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def board_files(p: dict) -> list[Path]:
    """The six files LLR-4407.27 keeps byte-identical."""
    return [p["A"], p["C"], p["A"].parent / "history.jsonl", p["C"].parent / "history.jsonl",
            p["people"], p["marks"]]


def shas(p: dict) -> list:
    return [sha(f) for f in board_files(p)]


def tasks_of(path: Path) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))["tasks"]


def task_ids(path: Path) -> list[str]:
    return [t["id"] for t in tasks_of(path)]


def history_lines(path: Path) -> list[dict]:
    h = Path(path).parent / "history.jsonl"
    if not h.exists():
        return []
    return [json.loads(x) for x in h.read_text(encoding="utf-8").splitlines() if x.strip()]


# --------------------------------------------------------------------------- #
# Fixture S (graph-proto-S head) — layer 0 of inbox.py
# --------------------------------------------------------------------------- #
def build_s(root: Path) -> dict:
    a_path, c_path = root / "a" / "board.json", root / "c" / "board.json"
    a = Board([Project("Eval harness", "lime", id="pe"),
               Project("Pilot rollout", "green", id="pp")], [], a_path, settings(),
              ["Backlog", "Doing", "Done"])
    a.save()
    c = Board([Project("Module 4 · Volumes", "sky", id="pm")],
              [Task("Old one", project_id="pm", phase="Todo", id="tc1")], c_path, settings(),
              ["Todo", "Doing", "Done"])
    c.save()
    return {"S": root, "A": a_path, "C": c_path, "store": root / "inbox.json",
            "F": root / "inbox-images"}


def seq_ids(monkeypatch, start: int = 1):
    """`models._new_id` yields t0000001, t0000002, … (dump_note calls it through the module,
    graph-proto-S head). Returns the list of ids handed out."""
    from taskboard import models
    handed: list[str] = []
    state = {"n": start - 1}

    def nxt():
        state["n"] += 1
        tid = f"t{state['n']:07d}"
        handed.append(tid)
        return tid
    monkeypatch.setattr(models, "_new_id", nxt)
    return handed


# --------------------------------------------------------------------------- #
# the store (LLR-4407.2 / LLR-4407.3)
# --------------------------------------------------------------------------- #
def stamp(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def entry(text: str, task: str, title: str, board, project: str, at: str | None = None,
          new_project: bool = False, images=()) -> dict:
    return {"at": at or stamp(datetime.now()), "text": text, "task": task, "title": title,
            "board": str(board), "project": project, "new_project": new_project,
            "images": list(images)}


def write_store(folder: Path, pad: str = "", dumped: list | None = None,
                divider_notice: bool | None = None, raw: str | None = None) -> Path:
    path = Path(folder) / "inbox.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if raw is not None:
        path.write_text(raw, encoding="utf-8")
        return path
    data = {"version": 1, "pad": pad, "dumped": dumped or []}
    if divider_notice is not None:
        data["divider_notice"] = divider_notice
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def read_store(folder: Path) -> dict:
    return json.loads((Path(folder) / "inbox.json").read_text(encoding="utf-8"))


def ago(days: float = 0, seconds: float = 0) -> str:
    return stamp(datetime.now() - timedelta(days=days, seconds=seconds))


# --------------------------------------------------------------------------- #
# pilot helpers
# --------------------------------------------------------------------------- #
@pytest.fixture
def home(tmp_path, monkeypatch):
    """`Path.home()` = this test's folder (never the operator's `~/.taskboard`); the real
    clock (the store's 7-day keep and the app's stamps read one clock). Returns
    `<home>/.taskboard` (`S`)."""
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    return tmp_path / ".taskboard"


def open_f_app():
    """The app as `taskboard` starts it, on the registry under `Path.home()`."""
    from taskboard.__main__ import open_app
    return open_app(None)


async def press(pilot, *keys, wait: float | None = None):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()
    if wait:
        await pilot.pause(wait)


async def type_text(pilot, text: str):
    """Type `text` key by key (`\n` → enter); Textual's pilot maps a single printable
    character to its key name itself (`_character_to_key`)."""
    for ch in text:
        await pilot.press("enter" if ch == "\n" else ch)
    await pilot.pause()


async def post_key(pilot, key: str, char: str | None):
    """Post `events.Key(key, char)` through the driver, as a real terminal delivers it
    (P-V-2/P-V-3: `ESC o` arrives as Key("alt+o", "o"), a PRINTABLE key; the pilot's own
    `press("alt+o")` sends char None, which cannot show a non-priority binding)."""
    from textual import events
    app = pilot.app
    ev = events.Key(key, char)
    ev.set_sender(app)
    app._driver.send_message(ev)
    await pilot.pause()
    await pilot.pause()


def screen_names(app) -> list[str]:
    return [type(s).__name__ for s in app.screen_stack]


def on_capture(app) -> bool:
    return type(app.screen).__name__ == "CaptureView"


def captures_on_stack(app) -> int:
    return sum(type(s).__name__ == "CaptureView" for s in app.screen_stack)


async def leave_home(pilot):
    """`escape`: the boards home closes and the open board starts (ARCH-3)."""
    await pilot.pause()
    await press(pilot, "escape")
    await pilot.pause()


async def open_capture(pilot, app, *before):
    """`before` keys, then `n`; fails here, with a message, when no capture view opens."""
    await press(pilot, *before, "n")
    await pilot.pause(0.2)
    assert on_capture(app), f"`n` opened no capture view: screen stack {screen_names(app)}"
    return app.screen


def capture_view(app):
    for s in reversed(app.screen_stack):
        if type(s).__name__ == "CaptureView":
            return s
    pytest.fail(f"no CaptureView on the stack: {screen_names(app)}")


def pad_of(app):
    view = capture_view(app)
    found = list(view.query("PadArea"))
    assert found, "the capture view holds no PadArea"
    return found[0]


async def set_pad(pilot, app, text: str, cursor=None):
    """Put `text` in the pad (as a paste would: one TextArea edit) and the cursor at
    `cursor` (row, col), default the end."""
    pad = pad_of(app)
    pad.text = text
    await pilot.pause()
    pad.move_cursor(cursor if cursor is not None else pad.document.end)
    await pilot.pause()
    return pad


async def cursor_to(pilot, app, row: int, col: int = 0):
    pad = pad_of(app)
    pad.move_cursor((row, col))
    await pilot.pause()


def plain(widget) -> str:
    content = getattr(widget, "content", None)
    p = getattr(content, "plain", None)
    if isinstance(p, str):
        return p.replace("\xa0", " ")
    rendered = getattr(widget, "renderable", None)
    p = getattr(rendered, "plain", None)
    if isinstance(p, str):
        return p.replace("\xa0", " ")
    return str(content if content is not None else "").replace("\xa0", " ")


def by_id(app, wid: str, screen=None):
    scr = screen or capture_view(app)
    found = list(scr.query(f"#{wid}"))
    assert found, f"the screen draws no #{wid}"
    return found[0]


def head(app) -> str:
    return plain(by_id(app, "cap-head")).split("\n")[0]


def hint(app) -> str:
    return plain(by_id(app, "cap-hint")).strip()


def keys_row(app) -> str:
    return plain(by_id(app, "cap-keys")).strip()


def rail_lines(app) -> list[str]:
    return [x.rstrip() for x in plain(by_id(app, "cap-rail")).split("\n")]


def rail_text(app) -> str:
    return "\n".join(rail_lines(app))


def notes_of(app) -> list:
    """Every notification raised so far (Textual's own list, not reaped)."""
    return list(app._notifications)


def messages(app) -> list[str]:
    return [str(n.message) for n in notes_of(app)]


def notified(app, text: str):
    """The notifications whose message equals `text`."""
    return [n for n in notes_of(app) if str(n.message) == text]


def painted(app) -> list[list[tuple[str, str | None]]]:
    """The screen as painted now: per row, (char, foreground hex) per cell."""
    from rich.cells import cell_len
    rows = []
    for strip in app.screen._compositor.render_strips(app.screen.size):
        out = []
        for seg in strip:
            st = seg.style
            fg = (st.color.triplet.hex.lower()
                  if st and st.color and st.color.triplet else None)
            for ch in seg.text:
                out.append((ch, fg))
                out += [("", fg)] * (cell_len(ch) - 1)
        rows.append(out)
    return rows


def screen_rows(app) -> list[str]:
    return ["".join(c for c, _ in r) for r in painted(app)]


def region_rows(app, widget) -> list[str]:
    """The widget's content region as painted, one string per screen row."""
    r = widget.content_region
    rows = painted(app)
    return ["".join(c for c, _ in rows[y][r.x:r.x + r.width]) for y in range(r.y, r.y + r.height)]
