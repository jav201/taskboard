"""Synthetic boards for Inc L, the added-order list view (`N`) and `Task.created`.

Two fixtures, both synthetic (owner `username_subject`, no real person):

* **F-V** (`fv_lanes`) — the in-memory lanes of graph-proto-V.cw.md ("Fixture F-V"): lane 0
  `Work` (4 phases, project "Eval harness"), lane 1 `Home` (3 phases, project "House"), the
  Work board's `history.jsonl` holding two birth records for `w3`. Layer-0 tests feed it to
  `views.added_rows` / `added_order` / `render_added_list`.
* **S** (`build`) — the registry of graph-proto-S.cw.md ("Test fixture of this group"): two
  boards `alpha` / `beta`, each in its own folder with its own `history.jsonl`, written in
  the bytes the app writes (a set `created` placed just before `id`, as group D's
  `Board._to_dict` writes it), so a load + save rewrites nothing.

The clock of both: today 2026-11-01 (a Sunday), now 2026-11-01T08:10:00.

New names of the increment (`views.added_rows`, `models.stamp`, ...) are reached only through
`need()`, which turns their absence on the base revision into an assertion failure with a
message, never an ImportError at collection.
"""
from __future__ import annotations

import json
from dataclasses import fields
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task

TODAY = date(2026, 11, 1)
NOW = datetime(2026, 11, 1, 8, 10, 0)
STAMP_RE = r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d$"

# palette hexes the design names (views.HEX at eb411e1)
INK, DIM, MUT, HD, ACCENT, FRAME = "#e6edf3", "#5b6675", "#8b98a5", "#c9d4e0", "#2dd4bf", "#334154"
BLUE, GREEN, SKY, ROSE, PINK, CYAN, SOON = ("#60a5fa", "#4ade80", "#38bdf8", "#fb7185",
                                            "#f472b6", "#22d3ee", "#fbbf24")


# --------------------------------------------------------------------------- #
# new names, reached without an import (RED on base is an assertion, not an error)
# --------------------------------------------------------------------------- #
def need(module, name: str):
    """`module.name`, or a test failure that says the increment's name is missing."""
    obj = getattr(module, name, None)
    if obj is None:
        pytest.fail(f"{module.__name__}.{name} missing (not built yet)")
    return obj


def need_created_field() -> None:
    if "created" not in {f.name for f in fields(Task)}:
        pytest.fail("Task.created missing: the dataclass has no `created` field (not built yet)")


def created_of(task):
    """The task's `created` FIELD (never an attribute a test set by hand)."""
    need_created_field()
    return task.created


def make_task(title: str, created=None, **kw) -> Task:
    """A Task with `created` set as an attribute after construction: valid on the base
    revision too (the dataclass has no slots), and the field once it exists."""
    t = Task(title, **kw)
    if created is not None:
        t.created = created
    return t


# --------------------------------------------------------------------------- #
# F-V: the lanes of graph-proto-V.cw.md (layer 0)
# --------------------------------------------------------------------------- #
FV_PEOPLE_ID, FV_PEOPLE_NAME = "ana", "Ana Ruiz"


def fv_people() -> dict:
    from taskboard.people import Person
    return {FV_PEOPLE_ID: Person(FV_PEOPLE_ID, FV_PEOPLE_NAME)}


def write_history(folder: Path, records: list[dict]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "history.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")


def birth(tid: str, at: str, to: str = "Backlog") -> dict:
    return {"task": tid, "from": None, "to": to, "at": at}


def fv_boards(root: Path) -> tuple[Board, Board]:
    p1 = Project("Eval harness", "blue", id="p1")
    work = Board([p1], [
        make_task("Volume oracle script", project_id="p1", phase="Backlog", id="w1"),
        make_task("Sync notes", created="2026-10-31T18:20:00", project_id="p1", phase="Doing",
                  priority="high", start_date="2026-10-30", due_date="2026-11-03",
                  milestone=True,
                  notes="::b:: ask the vendor ::\nping @ana before Friday",
                  urls=["https://example.com/spec"], images=["img/w2/board.png"],
                  depends_on=["w3"], id="w2"),
        make_task("Pilot store list", project_id="p1", phase="Review", id="w3"),
        make_task("Pay the rent", created="2026-11-01T08:10:00", project_id="p1",
                  phase="Backlog", id="w4"),
        make_task("Old archived", project_id="p1", phase="Done", archived=True, id="w5"),
    ], root / "work" / "board.json", {}, ["Backlog", "Doing", "Review", "Done"])
    write_history(root / "work", [birth("w3", "2026-10-28T10:30:00", "Review"),
                                  birth("w3", "2026-10-29T11:00:00", "Review")])
    p2 = Project("House", "green", id="p2")
    home = Board([p2], [
        make_task("Hybrid search index", phase="Todo", id="h1"),
        make_task("Compose file anatomy", created="2026-10-31T21:47:00", project_id="p2",
                  phase="Done", id="h2"),
    ], root / "home" / "board.json", {}, ["Todo", "Doing", "Done"])
    (root / "home").mkdir(parents=True, exist_ok=True)
    return work, home


def fv_lanes(root: Path) -> list:
    work, home = fv_boards(root)
    return [("Work", "sky", work, ""), ("Home", "lime", home, "")]


def solo_lanes(root: Path, tasks: list[Task], name: str = "Solo",
               phases=("Todo", "Doing", "Done"), history: list[dict] | None = None,
               colour: str = "sky", projects: list | None = None) -> list:
    folder = root / name.lower()
    folder.mkdir(parents=True, exist_ok=True)
    if history is not None:
        write_history(folder, history)
    b = Board(projects or [], tasks, folder / "board.json", {}, list(phases))
    return [(name, colour, b, "")]


# --------------------------------------------------------------------------- #
# S: the two-board registry of graph-proto-S.cw.md (pilot)
# --------------------------------------------------------------------------- #
SETTINGS = {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
            "seen_view_renumber_2026_07": True}

ALPHA_HISTORY = [birth("ta2", "2026-10-28T10:30:00")]
BETA_HISTORY = [{"task": "tb2", "from": "Doing", "to": "Done", "at": "2026-10-29T12:00:00"}]


def _board_text(board: Board, created: dict[str, object]) -> str:
    """The file text the increment's code writes for `board`: the base record of every
    task, with `created` (when the task has one) placed just before `id`."""
    data = json.loads(board._serialized())
    for rec in data["tasks"]:
        rec.pop("created", None)                 # whatever this revision did with it
        if rec["id"] in created:
            tid = rec.pop("id")
            rec["created"] = created[tid]
            rec["id"] = tid
    return json.dumps(data, indent=2)


def write_board(path: Path, board: Board, created: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_board_text(board, created), encoding="utf-8")


def alpha_board(path: Path, archived_on_alpha: bool = False, all_archived: bool = False,
                notes: dict | None = None) -> tuple[Board, dict]:
    notes = notes or {}
    pa = Project("Ops", "blue", id="pa")
    rows = [("ta1", "Sync notes", "Doing", "2026-10-31T18:20:00", False),
            ("ta2", "Pilot store list", "Backlog", None, False),
            ("ta3", "Old invoice", "Review", None, False)]
    if archived_on_alpha:
        rows.append(("ta4", "Old memo", "Review", "2026-10-30T09:00:00", True))
    tasks, created = [], {}
    for tid, title, phase, c, arch in rows:
        tasks.append(Task(title, project_id="pa", phase=phase, archived=arch or all_archived,
                          notes=notes.get(tid, ""), id=tid))
        if c:
            created[tid] = c
    return Board([pa], tasks, path, dict(SETTINGS), ["Backlog", "Doing", "Review", "Done"]), created


def beta_board(path: Path, with_archived: bool = False) -> tuple[Board, dict]:
    pb = Project("Home", "green", id="pb")
    rows = [("tb1", "Pay the rent", "Todo", "2026-11-01T07:55:00", False),
            ("tb2", "Archive scans", "Done", None, False)]
    if with_archived:
        rows.append(("tb3", "Old receipts", "Done", "2026-10-30T09:00:00", True))
    tasks, created = [], {}
    for tid, title, phase, c, arch in rows:
        tasks.append(Task(title, project_id="pb", phase=phase, archived=arch, id=tid))
        if c:
            created[tid] = c
    return Board([pb], tasks, path, dict(SETTINGS), ["Todo", "Doing", "Done"]), created


def board_path(home: Path, bid: str) -> Path:
    return home / "boards" / bid / "board.json"


def history_file(home: Path, bid: str) -> Path:
    return home / "boards" / bid / "history.jsonl"


def build(home: Path, with_archived: bool = False, archived_on_alpha: bool = False,
          only_alpha: bool = False, all_archived: bool = False,
          notes: dict | None = None, people: dict | None = None) -> Path:
    """Write the S registry under `home` (= `<Path.home()>/.taskboard`); return it.
    `only_alpha`: a one-board registry (the app starts on the board, no home screen).
    `all_archived`: every Alpha task archived. `people`: handle → name, a people file."""
    home.mkdir(parents=True, exist_ok=True)
    a_path = board_path(home, "alpha")
    a, a_created = alpha_board(a_path, archived_on_alpha, all_archived, notes)
    write_board(a_path, a, a_created)
    write_history(a_path.parent, ALPHA_HISTORY)
    entries = [{"id": "alpha", "name": "Alpha", "color": "sky", "path": str(a_path.resolve()),
                "last_opened": "2026-11-01T07:00", "archived": False}]
    if not only_alpha:
        b_path = board_path(home, "beta")
        b, b_created = beta_board(b_path, with_archived)
        write_board(b_path, b, b_created)
        write_history(b_path.parent, BETA_HISTORY)
        entries.append({"id": "beta", "name": "Beta", "color": "lime",
                        "path": str(b_path.resolve()), "last_opened": "2026-10-31T20:00",
                        "archived": False})
    if people:
        (home / "people.json").write_text(json.dumps(
            {"people": [{"id": h, "name": n} for h, n in people.items()]}, indent=2),
            encoding="utf-8")
    reg = home / "boards.json"
    reg.write_text(json.dumps({"version": 1, "last": "alpha", "boards": entries}, indent=2),
                   encoding="utf-8")
    return reg


# --------------------------------------------------------------------------- #
# clocks
# --------------------------------------------------------------------------- #
class Today(date):
    @classmethod
    def today(cls):
        return TODAY


class FixedNow(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


def advancing_clock(start: datetime = NOW):
    """A `datetime` whose `now()` moves one second per call (P-D-10 / P-S-2): a stamp
    taken once per task instead of once per insert gives as many values as tasks."""
    state = {"t": start - timedelta(seconds=1)}

    class Advancing(datetime):
        @classmethod
        def now(cls, tz=None):
            state["t"] += timedelta(seconds=1)
            return state["t"]

    return Advancing


# --------------------------------------------------------------------------- #
# pilot helpers: the app as `taskboard` starts it, and the list view as drawn
# --------------------------------------------------------------------------- #
@pytest.fixture
def home(tmp_path, monkeypatch):
    """`Path.home()` = this test's folder; the calendar on 2026-11-01 in app, models, views
    and modals; the app's and the entry point's clock at 08:10:00; `models.datetime` (the
    clock `stamp()` reads, P-D-4) at 08:10:00 — `raising=False`, since the base revision's
    models imports no `datetime`. Returns `<home>/.taskboard`."""
    import taskboard.__main__ as entry
    from taskboard import app as app_module, modals, models, views
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", Today)
    monkeypatch.setattr(app_module, "datetime", FixedNow)
    monkeypatch.setattr(entry, "datetime", FixedNow)
    monkeypatch.setattr(models, "datetime", FixedNow, raising=False)
    return tmp_path / ".taskboard"


def open_s_app():
    from taskboard.__main__ import open_app
    return open_app(None)


async def press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def names(app) -> list[str]:
    return [type(s).__name__ for s in app.screen_stack]


def on_list(app) -> bool:
    """The list view (working name `AddedList`, 01-requirements §1) is on top."""
    return type(app.screen).__name__ == "AddedList"


def lists_on_stack(app) -> int:
    return sum(type(s).__name__ == "AddedList" for s in app.screen_stack)


async def open_list(pilot, app, *before):
    """`escape` (leave the home: the board starts, P-S-4), any `before` keys, then `N`;
    fails here, with a message, when `N` opens no list view (the base revision)."""
    await press(pilot, *before, "N")
    await pilot.pause(0.3)
    assert on_list(app), f"`N` opened no list view: screen stack {names(app)}"


def _plain(widget) -> str:
    content = getattr(widget, "content", None)
    plain = getattr(content, "plain", None)
    return (plain if isinstance(plain, str) else str(content or "")).replace("\xa0", " ")


def body_widget(app):
    """The widget that draws the list view's body (its first line is the head row)."""
    from textual.widgets import Static
    for w in app.screen.query(Static):
        if _plain(w).startswith("ADDED"):
            return w
    return None


def body_lines(app) -> list[str]:
    w = body_widget(app)
    assert w is not None, "the list view draws no body whose head row starts `ADDED`"
    return _plain(w).split("\n")


def key_row(app) -> str:
    from textual.widgets import Static
    rows = [_plain(w) for w in app.screen.query(Static) if "esc / N" in _plain(w)
            and not _plain(w).startswith("ADDED")]
    assert rows, "the list view draws no key row holding `esc / N`"
    return rows[0]


def lw_for(width: int) -> int:
    """The list column of a terminal `width` cells wide (body = width − 2, LLR-4303.7)."""
    return 46 if width - 2 >= 100 else 34


def parse_list(lines: list[str], lw: int) -> tuple[list[dict], list[str]]:
    """The list area of a body (lines 2..): its rows (cursor, label, boxes, title) in
    order, and the day headers in order."""
    rows, headers = [], []
    for y, line in enumerate(lines[2:], start=2):
        left = line[:lw]
        if not left.strip():
            continue
        if left[0] in "▶ " and "▍" in left:
            head, title = left.split("▍", 1)
            rows.append({"cursor": left[0] == "▶", "label": left[1:8].strip(),
                         "boxes": head[8:].strip(), "title": title.rstrip(),
                         "title_at": len(head) + 1, "day": headers[-1] if headers else None,
                         "y": y})
        else:
            headers.append(left.strip())
    return rows, headers


def pane(lines: list[str], lw: int) -> list[str]:
    """The detail pane's lines, top first (body lines 2.., after ` │ `)."""
    return [line[lw + 3:].rstrip() for line in lines[2:]]


def cursor(rows: list[dict]) -> int:
    marks = [i for i, r in enumerate(rows) if r["cursor"]]
    assert len(marks) == 1, f"expected one cursor row, got {marks}"
    return marks[0]


def titles(rows: list[dict]) -> list[str]:
    return [r["title"] for r in rows]


def seen(app, width: int):
    """(rows, headers, pane lines, head row) of the list view as drawn now."""
    lines = body_lines(app)
    lw = lw_for(width)
    rows, headers = parse_list(lines, lw)
    return rows, headers, pane(lines, lw), lines[0]


def notices(app) -> list[str]:
    return [str(n.message) for n in app._notifications]


def cell_colours(widget, y: int) -> tuple[str, list]:
    """The text of the widget's rendered line `y` and each cell's rich Style."""
    strip = widget.render_line(y)
    text, styles = "", []
    for seg in strip:
        text += seg.text
        styles.extend([seg.style] * len(seg.text))
    return text, styles


def hex_of(style) -> str | None:
    if style is None or style.color is None:
        return None
    return style.color.get_truecolor().hex


def text_lines(body) -> list:
    """A rendered body (rich Text) as one Text per line, spans kept."""
    return list(body.split("\n", allow_blank=True))


def styles_of(line) -> list:
    """Each character's combined rich Style in a Text line (base style, then spans)."""
    from rich.style import Style

    def as_style(s):
        if isinstance(s, Style):
            return s
        return Style.parse(s) if s else Style.null()

    out = [as_style(line.style)] * len(line.plain)
    for span in line.spans:
        st = as_style(span.style)
        for k in range(span.start, min(span.end, len(out))):
            out[k] = out[k] + st
    return out


def colour_at(line, i: int) -> str | None:
    return hex_of(styles_of(line)[i])


def bold_at(line, i: int) -> bool:
    return bool(styles_of(line)[i].bold)
