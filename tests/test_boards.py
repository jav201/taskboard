"""Several boards: the registry and switching boards in place.

Batch 2026-10-20-batch-01 (variant C of the multi-board round, P1/P4):
HLR-2201, HLR-2202 / LLR-2201.1, LLR-2202.1 · TC-2201, TC-2202 · AT-2201
(US-2201). Synthetic data only: the round's boards (`tests/multi_board_fixture.py`)
and boards built here, every one under `tmp_path` — `Path.home()` is a temporary
folder for the whole suite (`tests/conftest.py`), and patched again per test.
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from pathlib import Path

import pytest

import multi_board_fixture as mb
from taskboard import boards
from taskboard.boards import BoardEntry, Registry, peek_board, slug
from taskboard.models import Board, Project, Task

NOW = datetime(2026, 10, 20, 9, 30)


def _main(tmp_path) -> Path:
    p = tmp_path / ".taskboard" / "board.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    Board([Project("Main work", id="pm")], [Task("Main task", project_id="pm", id="tm")],
          p).save()
    return p


def _write(reg_path: Path, data) -> None:
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    reg_path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")


# --------------------------------------------------------------------------- #
# TC-2201 — the registry read without failing (LLR-2201.1)
# --------------------------------------------------------------------------- #
def test_TC_2201_a_missing_registry_is_main_alone(tmp_path):
    """TC-2201: no file → the default board alone, `main`/`Main`, last `main`;
    nothing is written by reading."""
    main = tmp_path / "board.json"
    reg = Registry.load(tmp_path / "boards.json", main)
    assert [(e.id, e.name, e.path) for e in reg.entries] == [("main", "Main", str(main))]
    assert reg.last == "main" and reg.load_report == {}
    assert not (tmp_path / "boards.json").exists()


@pytest.mark.parametrize("raw", ["{not json", "[]", '{"boards": 3}', '"x"', ""])
def test_TC_2201_an_unreadable_registry_is_kept_aside(tmp_path, raw):
    """TC-2201: a file that is not a registry is copied to `.corrupt` (its bytes
    kept for the operator) and read as the default board alone — never raising.
    An empty file has nothing to keep."""
    reg_path = tmp_path / "boards.json"
    _write(reg_path, raw)
    reg = Registry.load(reg_path, tmp_path / "board.json")
    assert [e.id for e in reg.entries] == ["main"]
    assert reg.load_report["unreadable"] is True
    corrupt = tmp_path / "boards.json.corrupt"
    if raw:
        assert corrupt.read_text(encoding="utf-8") == raw
        assert reg.load_report["backup"] == str(corrupt)
    else:
        assert not corrupt.exists() and reg.load_report["backup"] is None


def test_TC_2201_an_existing_corrupt_copy_is_never_overwritten(tmp_path):
    """TC-2201: the first copy is the operator's oldest bytes; a second unreadable
    read keeps it and copies the new bytes to `.corrupt-2` (code review F5)."""
    reg_path = tmp_path / "boards.json"
    (tmp_path / "boards.json.corrupt").write_text("first", encoding="utf-8")
    _write(reg_path, "second")
    reg = Registry.load(reg_path, tmp_path / "board.json")
    assert (tmp_path / "boards.json.corrupt").read_text(encoding="utf-8") == "first"
    assert (tmp_path / "boards.json.corrupt-2").read_text(encoding="utf-8") == "second"
    assert reg.load_report["backup"] == str(tmp_path / "boards.json.corrupt-2")
    reg.touch("main", NOW)                       # nothing written after an unreadable read
    assert reg_path.read_text(encoding="utf-8") == "second"


def test_TC_2201_the_entry_rules(tmp_path):
    """TC-2201 (HLR-2201's boundary catalog): entries that are not objects or have
    no text path are skipped, a path seen before is skipped (in another spelling
    too), a bad or repeated id becomes a unique slug of the name, a bad name the
    file's name, a bad colour `violet` (or its ration remap), a bad time none,
    `archived` true only for `true`, `last` kept only when it names an entry."""
    a = tmp_path / "a" / "board.json"
    b = tmp_path / "b.json"
    data = {"version": 1, "last": "ghost", "boards": [
        7, "x", {"name": "No path"}, {"path": ""}, {"path": 3},
        {"id": "a b", "name": "Alpha", "color": "plaid", "path": str(a),
         "last_opened": "yesterday", "archived": "yes"},
        {"id": "alpha", "name": "", "color": [], "path": str(b),
         "last_opened": "2026-10-19T08:00", "archived": True},
        {"id": "dup", "name": "Again", "path": str(tmp_path / "a" / ".." / "a" / "board.json")},
        {"id": "", "name": "Gamma", "color": "amber", "path": str(tmp_path / "c.json")},
        {"id": "rel", "name": "Relative", "path": "rel/board.json"},
        {"id": "alpha", "name": "Delta", "color": "sky", "path": str(tmp_path / "d.json"),
         "archived": False},
    ]}
    _write(tmp_path / "boards.json", data)
    reg = Registry.load(tmp_path / "boards.json", tmp_path / "board.json")
    got = [(e.id, e.name, e.color, Path(e.path).name, e.last_opened, e.archived)
           for e in reg.entries]
    assert got == [
        ("alpha", "Alpha", "violet", "board.json", None, False),
        ("b", "b", "violet", "b.json", "2026-10-19T08:00", True),
        ("gamma", "Gamma", "lime", "c.json", None, False),
        ("delta", "Delta", "sky", "d.json", None, False),
    ], got
    assert reg.last is None and reg.load_report == {}
    a.parent.mkdir(parents=True)
    a.write_text("{}", encoding="utf-8")
    assert reg.opening().id == "alpha"


def test_TC_2201_no_valid_entry_is_main_alone(tmp_path):
    _write(tmp_path / "boards.json", {"boards": [{"path": ""}, 4]})
    reg = Registry.load(tmp_path / "boards.json", tmp_path / "board.json")
    assert [e.id for e in reg.entries] == ["main"]


def test_TC_2201_the_round_trip_and_the_atomic_save(tmp_path, monkeypatch):
    """TC-2201: the round's registry reads back what `save` wrote; `save` swaps a
    temporary file in, so a failed swap leaves the old bytes and no temporary file."""
    reg_path = mb.build(tmp_path, "client-retail-rag")
    reg = Registry.load(reg_path, tmp_path / "board.json")
    assert [e.id for e in reg.entries] == ["personal", "client-retail-rag", "course-docker",
                                           "main"]
    assert reg.last == "client-retail-rag"
    before = [(e.id, e.name, e.color, e.path, e.last_opened, e.archived) for e in reg.entries]
    reg.save()
    again = Registry.load(reg_path, tmp_path / "board.json")
    assert [(e.id, e.name, e.color, e.path, e.last_opened, e.archived)
            for e in again.entries] == before
    assert again.last == "client-retail-rag"
    old = reg_path.read_bytes()

    def boom(*a, **k):
        raise OSError("disk full")
    from taskboard import models as models_module
    monkeypatch.setattr(models_module.os, "replace", boom)
    reg.entries[0].name = "Changed"
    with pytest.raises(OSError):
        reg.save()
    assert reg_path.read_bytes() == old
    assert [p.name for p in tmp_path.iterdir() if p.name.endswith(".tmp")] == []


def test_TC_2201_touch_writes_only_with_more_than_one_board_or_a_file(tmp_path):
    """TC-2201 (HLR-2201): a one-board user without a registry file never gets one;
    with a second board, or once the file exists, an opening is recorded."""
    reg = Registry.load(tmp_path / "boards.json", tmp_path / "board.json")
    reg.touch("main", NOW)
    assert not (tmp_path / "boards.json").exists()
    assert reg.last == "main" and reg.get("main").last_opened == "2026-10-20T09:30"
    _write(tmp_path / "boards.json", {"boards": [{"id": "main", "name": "Main",
                                                  "path": str(tmp_path / "board.json")}]})
    reg = Registry.load(tmp_path / "boards.json", tmp_path / "board.json")
    reg.touch("main", NOW)
    assert json.loads((tmp_path / "boards.json").read_text(encoding="utf-8"))["last"] == "main"
    (tmp_path / "boards.json").unlink()
    reg = Registry.load(tmp_path / "boards.json", tmp_path / "board.json")
    reg.register(tmp_path / "side" / "notes.json")
    (tmp_path / "boards.json").unlink()
    reg.touch("main", NOW)
    assert (tmp_path / "boards.json").exists()


def test_TC_2201_register(tmp_path):
    """TC-2201: a new path → an entry named after the file (`notes` for
    `notes.json`, the folder for a `board.json`), the first colour no active board
    wears, a unique id; the default board in another spelling → no new entry; an
    archived entry's path → un-archived."""
    main = tmp_path / "board.json"
    reg = Registry.load(tmp_path / "boards.json", main)
    a = reg.register(tmp_path / "side" / "notes.json")
    assert (a.id, a.name, a.color) == ("notes", "notes", "lime")
    assert Path(a.path).is_absolute()
    b = reg.register(tmp_path / "client" / "board.json")
    assert (b.id, b.name, b.color) == ("client", "client", "green")
    c = reg.register(tmp_path / "other" / "notes.json")
    assert c.id == "notes-2"
    spelled = tmp_path / "x" / ".." / "board.json"
    if os.name == "nt":
        spelled = Path(str(spelled).upper())
    assert reg.register(spelled).id == "main"
    assert len(reg.entries) == 4
    b.archived = True
    reg.save()
    assert reg.register(tmp_path / "client" / "board.json").archived is False
    on_disk = json.loads((tmp_path / "boards.json").read_text(encoding="utf-8"))
    assert [e["id"] for e in on_disk["boards"]] == ["main", "notes", "client", "notes-2"]


@pytest.mark.parametrize("name, want", [("Course · Kubernetes", "course-kubernetes"),
                                        ("Diseño", "diseno"), ("***", "board"),
                                        ("../../etc", "etc"), ("  A  b  ", "a-b"),
                                        ("Con", "con-board"), ("nul", "nul-board"),
                                        ("COM1", "com1-board"), ("日本", "board")])
def test_TC_2201_slug(name, want):
    """TC-2201: the folder name holds only a-z, 0-9 and `-` — never a separator."""
    assert slug(name) == want


def test_TC_2201_opening(tmp_path):
    """TC-2201: the last board when active, else the first active, else the first —
    a board whose file is missing skipped and named (ux-reviewer UX-10), the
    default board never skipped."""
    main = tmp_path / "board.json"
    for n in ("a", "b"):
        (tmp_path / f"{n}.json").write_text("{}", encoding="utf-8")
    reg = Registry(tmp_path / "boards.json", [
        BoardEntry("a", "A", "lime", str(tmp_path / "a.json"), archived=True),
        BoardEntry("b", "B", "sky", str(tmp_path / "b.json")),
        BoardEntry("main", "Main", "violet", str(main))], last="a", main_path=str(main))
    assert reg.opening().id == "b"
    reg.last = "main"
    assert reg.opening().id == "main"
    for e in reg.entries:
        e.archived = True
    assert reg.opening().id == "a"
    for e in reg.entries:
        e.archived = False
    reg.last = "b"
    (tmp_path / "b.json").unlink()
    assert reg.opening().id == "a"
    assert reg.load_report["missing"] == str(tmp_path / "b.json")
    (tmp_path / "a.json").unlink()
    assert reg.opening().id == "main"
    # the default board is known by its path, not by an id a file can carry (F3)
    impostor = Registry(tmp_path / "boards.json", [
        BoardEntry("main", "Main", "violet", str(tmp_path / "gone.json"))], last="main",
        main_path=str(main))
    e = impostor.opening()
    assert Path(e.path) == main and impostor.load_report["missing"].endswith("gone.json")


def test_TC_2201_peek_board_never_writes(tmp_path):
    """TC-2201 (P-2): `Board.load` seeds and saves at a missing path; the peek does not."""
    missing = tmp_path / "nowhere" / "board.json"
    b = peek_board(missing)
    assert b.projects == [] and b.tasks == [] and not missing.exists()
    real = _main(tmp_path)
    before = real.read_bytes()
    assert [p.name for p in peek_board(real).projects] == ["Main work"]
    assert real.read_bytes() == before
    for bad in ("{oops", "[]"):
        unreadable = tmp_path / "bad" / "board.json"
        unreadable.parent.mkdir(exist_ok=True)
        unreadable.write_text(bad, encoding="utf-8")
        b = peek_board(unreadable)
        assert b.load_report["file_unreadable"] is True and b.projects == []
        assert sorted(p.name for p in unreadable.parent.iterdir()) == ["board.json"]


# --------------------------------------------------------------------------- #
# TC-2202 — open_app, the app's registry, switching in place (LLR-2202.1)
# --------------------------------------------------------------------------- #
class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


@pytest.fixture
def home(tmp_path, monkeypatch):
    """`Path.home()` → this test's own folder; the clock frozen at 09:30."""
    from taskboard import app as app_module
    import taskboard.__main__ as entry
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(app_module, "datetime", _Now)
    monkeypatch.setattr(entry, "datetime", _Now)
    return tmp_path / ".taskboard"


def _open(board=None):
    from taskboard.__main__ import open_app
    return open_app(board)


async def test_TC_2202_switch_board_starts_the_other_board_over(home):
    """TC-2202: the other file is loaded; the selection, focus, search, undo stack,
    gantt memory, setup staging and team state cleared; the team timer stopped;
    the per-board start run once; the view and layouts kept; the registry's last
    set — and the open board's id reloads nothing."""
    mb.build(home, "main")
    app = _open()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        assert app.board_id == "main" and app.board.path == home / "board.json"
        await pilot.press("escape")          # leave the home: the deferred start runs (HD-1)
        await pilot.pause()
        assert app._started_board == "main"
        app.view_mode = "gantt"
        app.kanban_presentation = "matrix"
        app.selected_task_id = "tr3"
        app.focused_project_id = "pmr"
        app.search_query = "demo"
        app._undo_stack.append({"task_id": "tr3", "fields": {}})
        app._gantt_group, app._gantt_previous = "g1", "g0"
        app._last_history_error = "x"

        class _Timer:
            stopped = False

            def stop(self):
                self.stopped = True
        timer = _Timer()
        app._team_timer = timer
        calls = []
        real_open = app._open_board
        app._open_board = lambda **k: (calls.append(k), real_open(**k))[1]
        same = app.board
        app.switch_board("main")
        assert app.board is same and calls == []
        app.switch_board("client-retail-rag")
        await pilot.pause()
        assert app.board.path == home / "boards" / "client-retail-rag" / "board.json"
        assert {p.name for p in app.board.projects} == {"Ingest & index", "Eval harness"}
        assert app.board_id == "client-retail-rag"
        assert app.selected_task_id in {t.id for t in app.board.tasks}
        assert app._last_history_error is None
        assert app.focused_project_id is None and app.search_query is None
        assert app._undo_stack == []
        assert app._gantt_previous is None and app._gantt_group != "g1"
        assert app.team_state is None and app._team_timer is None and timer.stopped
        assert calls == [{}]
        assert app.view_mode == "gantt" and app.kanban_presentation == "matrix"
        assert app.registry.last == "client-retail-rag"
        reg = json.loads((home / "boards.json").read_text(encoding="utf-8"))
        assert reg["last"] == "client-retail-rag"
        assert next(e for e in reg["boards"]
                    if e["id"] == "client-retail-rag")["last_opened"] == "2026-10-20T09:30"


async def test_TC_2202_from_the_setup_view_back_to_the_view_before(home):
    mb.build(home, "main")
    app = _open()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        app.action_view("kanban")
        app.action_view("setup")
        assert app._setup_state is not None
        app.switch_board("personal")
        await pilot.pause()
        assert app.view_mode == "kanban" and app._setup_state is None


async def test_TC_2202_a_switched_board_gets_the_start_a_board_gets(home):
    """TC-2202: the per-board start runs on the new board — its renumbering notice,
    shown once, sets its flag in ITS file."""
    mb.build(home, "main")
    side = home / "boards" / "personal" / "board.json"
    data = json.loads(side.read_text(encoding="utf-8"))
    data["settings"].pop("seen_view_renumber_2026_07")
    side.write_text(json.dumps(data), encoding="utf-8")
    app = _open()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        before = len(app._notifications)
        app.switch_board("personal")
        await pilot.pause()
        titles = [n.title for n in list(app._notifications)[before:]]
        assert titles.count("View keys renumbered") == 1
    saved = json.loads(side.read_text(encoding="utf-8"))
    assert saved["settings"]["seen_view_renumber_2026_07"] is True


def test_TC_2202_open_app_picks_the_board(home, tmp_path):
    """TC-2202: `--board` opens (and registers) its file over the registry's last;
    `last` archived → the first active board; `--board` on a registered path adds
    no entry."""
    mb.build(home, "personal")
    app = _open(str(home / "boards" / "course-docker" / "board.json"))
    assert app.board_id == "course-docker"
    assert len(app.registry.entries) == 4
    reg = json.loads((home / "boards.json").read_text(encoding="utf-8"))
    assert reg["last"] == "course-docker"
    reg["boards"][2]["archived"] = True
    (home / "boards.json").write_text(json.dumps(reg), encoding="utf-8")
    assert _open().board_id == "personal"
    app = _open(str(tmp_path / "side" / "notes.json"))
    assert app.board_id == "notes" and app.board.path == tmp_path / "side" / "notes.json"
    assert [e["id"] for e in json.loads((home / "boards.json").read_text(
        encoding="utf-8"))["boards"]][-1] == "notes"


async def test_TC_2202_an_app_without_a_registry_keeps_it_beside_its_board(tmp_path):
    """TC-2202 (D12): the suite's `TaskboardApp(board_path=...)` knows only its own
    board, its registry file beside it — and mounting writes no registry at all."""
    from taskboard.app import TaskboardApp
    p = _main(tmp_path)
    app = TaskboardApp(board_path=str(p))
    assert app.registry.path == p.parent / "boards.json"
    assert app.board_id == "main" and len(app.registry.entries) == 1
    async with app.run_test(size=(100, 30)) as pilot:
        await pilot.pause()
    assert not (p.parent / "boards.json").exists()


async def test_TC_2202_the_mount_order_is_the_shipped_one(home, monkeypatch):
    """TC-2202 (LLR-2202.1): the per-board start keeps the shipped order, the clock
    interval set once, between the clocks and the recovery notices. With the home
    at start only the read-only half mounts (HD-1, LLR-2701.1); leaving the home
    runs the deferred start in the shipped order."""
    from taskboard.app import TaskboardApp
    mb.build(home, "main")
    order = []
    depth = [0]
    names = ["_migrate_links", "_announce_renumbering", "_sweep_old_done", "_select_first",
             "refresh_view", "_apply_clock_settings", "set_interval", "_warn_if_rescued",
             "_init_team_mode", "_offer_milestones"]
    for n in names:
        real = getattr(TaskboardApp, n)

        def spy(self, *a, _n=n, _real=real, **k):
            if depth[0] == 0:                     # the start's own calls, not nested ones
                order.append(_n)
            depth[0] += 1
            try:
                return _real(self, *a, **k)
            finally:
                depth[0] -= 1
        monkeypatch.setattr(TaskboardApp, n, spy)
    app = _open()
    async with app.run_test(size=(100, 30)) as pilot:
        # the home shows at start: only the read-only half mounts (HD-1, LLR-2701.1);
        # BoardView's resize re-render may append refresh_view after it
        assert order[:5] == ["_select_first", "refresh_view", "_apply_clock_settings",
                             "set_interval", "_warn_if_rescued"], order
        await pilot.pause()
        order.clear()
        await pilot.press("escape")               # the deferred start runs here (HD-1)
        await pilot.pause()
        assert order[:9] == [n for n in names if n != "set_interval"], order
        order.clear()
        app.switch_board("personal")
        app.switch_board("course-docker")
        app.switch_board("main")
        assert "set_interval" not in order, order       # three switches, no new interval (F5)
        assert order[:9] == [n for n in names if n != "set_interval"], order


def test_TC_2202_the_guard_the_suite_runs_under():
    """D12: `Path.home()` is never the operator's real home inside the suite."""
    real = Path(os.path.expanduser("~"))
    assert Path.home() != real


# --------------------------------------------------------------------------- #
# AT-2201 — today's board, untouched (HLR-2201)
# --------------------------------------------------------------------------- #
async def test_AT_2201_no_registry_and_an_unreadable_one(home):
    """AT-2201 (US-2201): with no `boards.json` the app opens the default board as
    today — no chip, no home — and leaves no `boards.json` behind; with an
    unreadable one it opens the default board, keeps the bytes in `.corrupt` and
    says so — and leaves the unreadable file as it found it."""
    _main(home.parent)
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        assert type(app.screen).__name__ == "Screen"
        first = app.query_one("#board").content.plain.split("\n")[0]
        assert first.startswith("◆ TASKBOARD"), first
        assert app.board.path == home / "board.json"
    assert not (home / "boards.json").exists()
    (home / "boards.json").write_text("{not json", encoding="utf-8")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        assert app.board.path == home / "board.json"
        first = app.query_one("#board").content.plain.split("\n")[0]
        assert first.startswith("◆ TASKBOARD"), first
        notes = [n for n in app._notifications if n.title == "Boards"]
        assert len(notes) == 1 and str(home / "boards.json.corrupt") in notes[0].message
    assert (home / "boards.json.corrupt").read_text(encoding="utf-8") == "{not json"
    assert (home / "boards.json").read_text(encoding="utf-8") == "{not json"   # kept as found


async def test_TC_2202_a_failed_migration_at_a_switch_keeps_the_open_board(home, monkeypatch):
    """TC-2202 (architect A-6, ux UX-12): the other board's link migration fails —
    an error notice, the open board back as it was (its undo stack and search
    too), no second start notice, `last` unchanged, the app still running."""
    from taskboard import app as app_module
    from taskboard.models import LinkMigration
    mb.build(home, "main")
    app = _open()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        app._undo_stack.append({"task_id": "tr3", "fields": {}})
        app.search_query = "demo"
        before_notes = len(app._notifications)
        real = app_module.run_link_migration

        def failing(board):
            if board.path != home / "board.json":
                return LinkMigration([], error="disk full")
            return real(board)
        monkeypatch.setattr(app_module, "run_link_migration", failing)
        app.switch_board("personal")
        await pilot.pause()
        assert app.is_running
        assert app.board_id == "main" and app.board.path == home / "board.json"
        assert app._undo_stack == [{"task_id": "tr3", "fields": {}}]
        assert app.search_query == "demo"
        new = list(app._notifications)[before_notes:]
        assert [n.title for n in new] == ["Boards"] and "disk full" in new[0].message
        assert app.registry.last == "main"


async def test_TC_2202_a_switch_into_a_team_board_starts_its_timer(home):
    """TC-2202: the start a board gets includes team mode: a board with a team
    folder and an identity starts its own sync timer at the switch."""
    mb.build(home, "main")
    shared = home.parent / "team"
    shared.mkdir()
    (shared / "team.json").write_text(json.dumps({
        "version": 1, "phases": ["Backlog", "Next", "Doing", "Review", "Done"],
        "roster": [{"id": "u1", "name": "Member One", "hue": "sky"}], "projects": []}),
        encoding="utf-8")
    p = home / "boards" / "personal" / "board.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["settings"].update(team_shared_dir=str(shared), team_user_id="u1")
    p.write_text(json.dumps(data), encoding="utf-8")
    app = _open()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        assert app._team_timer is None
        app.switch_board("personal")
        await pilot.pause()
        assert app._team_timer is not None and app.team_state is not None


async def test_TC_2202_a_missing_board_file_opens_nothing(home):
    mb.build(home, "main")
    (home / "boards" / "personal" / "board.json").unlink()
    app = _open()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        app.switch_board("personal")
        await pilot.pause()
        assert app.board_id == "main"
        assert any("its file is missing" in n.message for n in app._notifications)
    assert not (home / "boards" / "personal" / "board.json").exists()


async def test_TC_2202_the_last_board_missing_at_start(home):
    mb.build(home, "personal")
    (home / "boards" / "personal" / "board.json").unlink()
    app = _open()
    assert app.board_id == "client-retail-rag"
    assert app.registry.load_report["missing"].endswith("board.json")
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        notes = [n.message for n in app._notifications if n.title == "Boards"]
        assert any(str(home / "boards" / "personal" / "board.json") in m for m in notes), notes
    assert not (home / "boards" / "personal" / "board.json").exists()


def test_TC_2202_a_registry_that_cannot_be_written_never_stops_a_start(home, monkeypatch):
    """TC-2202 (code review F1): recording the board opened is bookkeeping — a
    `boards.json` that cannot be written still opens the board, and says so."""
    mb.build(home, "personal")
    from taskboard import models as models_module

    def boom(*a, **k):
        raise PermissionError("locked")
    monkeypatch.setattr(models_module.os, "replace", boom)
    app = _open()
    assert app.board_id == "personal"
    assert "locked" in app.registry.load_report["save_error"]
