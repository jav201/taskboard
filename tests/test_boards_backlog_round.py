"""The boards' items of the backlog round.

Batch 2026-10-20-batch-03: HLR-2408 / LLR-2408.1 · TC-2408 · AT-2408 — the start-up
modals name their board (US-2405); HLR-2409 / LLR-2409.1, LLR-2409.2 · TC-2409 · AT-2409
— one notice when a board is open in another window (US-2406); HLR-2410 / LLR-2410.1,
LLR-2410.2 · TC-2410 · AT-2410 — `--open PATH` (US-2407). "Another window" is a second
`TaskboardApp` in this process on the same files: the code a second process runs. The
round's boards (`backlog_round_fixture`), synthetic, under this test's own home.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import date, datetime
from pathlib import Path

import pytest

import backlog_round_fixture as fx
import kg_board
from test_modal_keys import _svg_rows
from taskboard import app as app_module, boards, models, modals, views
from taskboard.app import BoardsHome, TaskboardApp
from taskboard.boards import Registry
from taskboard.models import Board

NOW = datetime(2026, 10, 20, 9, 30)


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


@pytest.fixture
def home(tmp_path, monkeypatch):
    import taskboard.__main__ as entry
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    monkeypatch.setattr(app_module, "datetime", _Now)
    monkeypatch.setattr(entry, "datetime", _Now)
    return tmp_path / ".taskboard"


def _open(board=None, unlisted=None):
    from taskboard.__main__ import open_app
    return open_app(board, unlisted)


async def _press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def _notes(app) -> list:
    return [str(n.message) for n in app._notifications]


def _markers() -> list:
    d = boards.presence_dir()
    return sorted(p.name for p in d.iterdir()) if d.is_dir() else []


def _title(screen) -> str:
    c = screen.query(".modal-title").first().render()
    return c.plain if hasattr(c, "plain") else str(c)


# --------------------------------------------------------------------------- #
# HLR-2408 — the start-up modals' chip
# --------------------------------------------------------------------------- #
async def test_TC_2408_the_titles_open_with_the_chip(home):
    """TC-2408: the offer of a labelled board and the identity picker given a label
    open their titles with the chip and a space; no label, no chip; a markup-looking
    name printed as typed; the picker shows `↵ pick   esc cancel`."""
    fx.build(home)
    board = Board.load(fx.board_path(home, "client-a"))
    cands = [(t, True) for t in board.tasks[:1]]
    app = TaskboardApp(board_path=home / "x" / "board.json")
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        board.label = ("Client A", "sky")
        app.push_screen(modals.MilestoneOffer(board, cands, fx.TODAY))
        await pilot.pause()
        assert _title(app.screen).startswith(" Client A  ◆ Milestones · convert one-day tasks?")
        app.pop_screen()
        board.label = None
        app.push_screen(modals.MilestoneOffer(board, cands, fx.TODAY))
        await pilot.pause()
        assert _title(app.screen).startswith("◆ Milestones")
        app.pop_screen()
        roster = [{"id": "u1", "name": "username_subject"}]
        app.push_screen(modals.TeamIdentityPicker(roster, ("[b]Course[/b]", "violet")))
        await pilot.pause()
        assert _title(app.screen).startswith(" [b]Course[/b]  Operator identity")
        keys = app.screen.query_one("#identity-keys").render().plain
        assert keys == "↵ pick   esc cancel"
        app.pop_screen()
        app.push_screen(modals.TeamIdentityPicker(roster))
        await pilot.pause()
        assert _title(app.screen).startswith("Operator identity")


@pytest.mark.milestone_offer
async def test_AT_2408_the_start_up_modals_say_their_board(home, tmp_path):
    """AT-2408 (US-2405): a start with Client A's offer pending shows the offer titled
    with ` Client A ` — over the board, once the home is left (HD-1, HD-2); Course in
    team mode with no identity, opened from the home, shows the picker titled
    ` Course ` with its keys; a one-board start's offer has no chip."""
    fx.build(home, last="client-a", offer=True)
    team = tmp_path / "team"
    team.mkdir()
    team_json = dict(kg_board.TEAM)
    team_json["roster"] = [{"id": "u1", "name": "username_subject", "hue": "sky"},
                           {"id": "u2", "name": "Teammate B", "hue": "amber"}]
    (team / "team.json").write_text(json.dumps(team_json), encoding="utf-8")
    course = Board.load(fx.board_path(home, "course"))
    course.settings["team_shared_dir"] = str(team)
    course.save()
    app = _open()
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, BoardsHome)   # the home defers the offer (HD-1)
        await _press(pilot, "escape")
        assert type(app.screen).__name__ == "MilestoneOffer"
        assert _title(app.screen).startswith(" Client A  ◆ Milestones · convert one-day tasks?")
        await _press(pilot, "escape")
        assert type(app.screen).__name__ == "Screen"   # the offer answered over the board (HD-2)
        await _press(pilot, "B")
        assert isinstance(app.screen, BoardsHome)
        await _press(pilot, "left", "down", "enter")
        assert type(app.screen).__name__ == "TeamIdentityPicker", app.screen_stack
        assert _title(app.screen).startswith(" Course ") and "Operator identity" in _title(app.screen)
        assert app.screen.query_one("#identity-keys").render().plain == "↵ pick   esc cancel"
    one = home.parent / "one"
    path = one / "board.json"
    b = fx.build_board(one, "client-a", offer=True)
    b.path = path
    path.parent.mkdir(parents=True, exist_ok=True)
    b.save()
    app = TaskboardApp(board_path=path)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert type(app.screen).__name__ == "MilestoneOffer"
        assert _title(app.screen).startswith("◆ Milestones")


# --------------------------------------------------------------------------- #
# HLR-2409 — open twice
# --------------------------------------------------------------------------- #
def _age(p: Path, seconds: float) -> None:
    t = time.time() - seconds
    os.utime(p, (t, t))


def test_TC_2409_the_markers(home, monkeypatch):
    """TC-2409: two announces are two files; another window's fresh marker counts,
    one 121 s old (or 121 s in the future) is removed, 119 s counts; a marker of the
    wrong shape counts with no time; a directory and a foreign name are left alone;
    `withdraw` removes only its own; a failed create or write leaves nothing; two
    spellings of one file share one pattern."""
    p = home / "b" / "board.json"
    a, b = boards.announce(p, NOW), boards.announce(p, NOW)
    assert a and b and a != b and a.parent == home / "open"
    assert json.loads(a.read_text(encoding="utf-8"))["since"] == "2026-10-20T09:30"
    assert boards.open_elsewhere(p, a) == [NOW]
    rel = Path(os.path.relpath(p, Path.cwd())) if p.drive == Path.cwd().drive else p
    assert boards.open_elsewhere(Path(str(p).upper()), a) == [NOW]
    assert boards.open_elsewhere(rel, a) == [NOW]
    _age(b, 121)
    assert boards.open_elsewhere(p, a) == [] and not b.exists()
    c = boards.announce(p, NOW)
    _age(c, 119)
    assert boards.open_elsewhere(p, a) == [NOW]
    t = time.time() + 121
    os.utime(c, (t, t))
    assert boards.open_elsewhere(p, a) == [] and not c.exists()
    stem = a.name.split("-")[0]
    for body in (b"not json", b"[]", b'{"since": 5}', b'{"since": null}',
                 b'{"since": "2026-10-20T09:30+05:00"}',     # an offset: unordered (S-13)
                 b'{"since": "' + b"9" * 10_000_000 + b'"}'):
        m = home / "open" / f"{stem}-{'e' * 32}.json"
        m.write_bytes(body)
        assert boards.open_elsewhere(p, a) == [None], body[:20]
        m.unlink()
    (home / "open" / f"{stem}-{'d' * 32}.json").mkdir()
    (home / "open" / "other.json").write_text("{}", encoding="utf-8")
    assert boards.open_elsewhere(p, a) == []
    assert (home / "open" / f"{stem}-{'d' * 32}.json").is_dir()
    assert (home / "open" / "other.json").exists()
    m = boards.announce(p, NOW)                      # renewal keeps a live window fresh
    _age(m, 119)
    assert boards.renew(m) and abs(time.time() - m.stat().st_mtime) < 5
    assert boards.renew(None) is False
    boards.withdraw(m)
    boards.withdraw(a)
    assert not a.exists() and (home / "open" / "other.json").exists()
    assert boards.name_for(p) == "b" and boards.name_for(home / "x" / "copy.json") == "copy"

    def deny(*a, **k):
        raise PermissionError("read-only")
    monkeypatch.setattr(boards.os, "open", deny)
    assert boards.announce(p, NOW) is None
    monkeypatch.undo()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home.parent))
    before = set(os.listdir(home / "open"))
    monkeypatch.setattr(boards.os, "write", deny)
    assert boards.announce(p, NOW) is None
    assert set(os.listdir(home / "open")) == before


async def test_TC_2409_the_lifecycle(home, monkeypatch):
    """TC-2409 (app): a failed switch keeps the old marker; 30 ticks after the marker
    is removed by hand a new one exists; the notice is a warning titled `Boards · open
    twice`; a registry name `[/b]` shows as typed; two others are counted; a second
    window by `--open` warns too — once both windows left their homes (HD-1)."""
    fx.build(home, last="client-a")
    reg = json.loads((home / "boards.json").read_text(encoding="utf-8"))
    reg["boards"][1]["name"] = "[/b]"
    (home / "boards.json").write_text(json.dumps(reg), encoding="utf-8")
    path = fx.board_path(home, "client-a")
    other1, other2 = boards.announce(path, NOW), boards.announce(path, NOW)
    # a third marker with an offset `since` (planted): the start must survive it (S-13)
    aware = other1.with_name(other1.name.split("-")[0] + "-" + "f" * 32 + ".json")
    aware.write_text('{"since": "2026-10-20T09:00+05:00"}', encoding="utf-8")
    app = _open()
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        await _press(pilot, "escape")        # the home deferred the start (HD-1)
        note = next(n for n in app._notifications if n.title == "Boards · open twice")
        assert note.severity == "warning"
        assert note.message == ("[/b] is already open in 3 other taskboard windows (the first "
                                "since 09:30). Both save the same file: the last save wins. "
                                "Close one of them.")
        mine = app._presence
        assert mine is not None and mine.exists()
        monkeypatch.setattr(app, "_migrate_links", lambda at_switch=False: False)
        app.switch_board("course")
        assert app.board_id == "client-a" and mine.exists() and app._presence == mine
        mine.unlink()
        for _ in range(30):
            app._tick()
        assert app._presence is not None and app._presence.exists()
    boards.withdraw(other1)
    boards.withdraw(other2)
    boards.withdraw(aware)
    first = _open()
    async with first.run_test(size=(118, 30)) as p1:
        await p1.pause()
        await _press(p1, "escape")           # the first window's marker lands off its home
        second = _open(unlisted=str(path))
        async with second.run_test(size=(118, 30), notifications=True) as p2:
            await p2.pause()
            assert not any("already open" in n for n in _notes(second))
            await _press(p2, "escape")       # its deferred start sees the first window
            assert any("already open in another taskboard window" in n for n in _notes(second))


async def test_AT_2409_a_second_window_is_told_once(home):
    """AT-2409 (US-2406): a second app on Client A says so once, with the first's
    time; the first says nothing; markers follow the windows: one each, gone when
    the window leaves the board or exits; a third app after them is told nothing.
    The home defers each window's start (HD-1): a window announces its marker only
    once it leaves the home."""
    fx.build(home, last="client-a")
    one = _open()
    async with one.run_test(size=(118, 30), notifications=True) as p1:
        await p1.pause()
        assert not any("open twice" in (n.title or "") for n in one._notifications)
        assert _markers() == []                 # the home writes no marker (HD-1)
        await _press(p1, "escape")              # leaving the home starts Client A
        assert len(_markers()) == 1
        two = _open()
        async with two.run_test(size=(118, 30), notifications=True) as p2:
            await p2.pause()
            assert len(_markers()) == 1         # the second window's home wrote nothing (HD-1)
            await _press(p2, "escape")
            twice = [n for n in two._notifications if n.title == "Boards · open twice"]
            assert [n.message for n in twice] == [
                "Client A is already open in another taskboard window (since 09:30). Both "
                "save the same file: the last save wins. Close one of them."]
            assert len(_markers()) == 2
        assert len(_markers()) == 1
        await _press(p1, "B")                   # the home again, then on to Course
        assert isinstance(one.screen, BoardsHome)
        await _press(p1, "down", "enter")
        assert one.board_id == "course"
        assert not any("open twice" in (n.title or "") for n in one._notifications)
        course = boards._presence_stem(fx.board_path(home, "course"))
        assert [m.split("-")[0] for m in _markers()] == [course]
    assert _markers() == []
    three = _open()
    async with three.run_test(size=(118, 30), notifications=True) as p3:
        await p3.pause()
        assert not any("open twice" in (n.title or "") for n in three._notifications)


# --------------------------------------------------------------------------- #
# HLR-2410 — --open
# --------------------------------------------------------------------------- #
def _main(monkeypatch, *argv):
    from taskboard import __main__ as entry
    built = []
    monkeypatch.setattr(sys, "argv", ["taskboard", *argv])
    monkeypatch.setattr(TaskboardApp, "run", lambda self, *a, **k: built.append(self))
    entry.main()
    return built


def test_TC_2410_open_app_registers_nothing(home):
    """TC-2410: `open_app(None, copy)` writes nothing to `boards.json`."""
    fx.build(home)
    before = (home / "boards.json").read_bytes()
    app = _open(unlisted=str(fx.copy_path(home)))
    assert app.board_id is None
    assert (home / "boards.json").read_bytes() == before


@pytest.mark.parametrize("make, report", [("missing", False), ("missing", True),
                                          ("folder", False), ("text", False),
                                          ("escape", False)])
def test_TC_2410_a_path_that_is_no_board_is_refused(home, monkeypatch, capsys, make, report):
    """TC-2410: `--open` of a missing path (with `--report` too), a folder, a text file
    or a path holding an ESC byte → exit 2, the message without control characters,
    nothing written at the path."""
    fx.build(home)
    target = {"missing": home / "nope" / "b.json", "folder": home / "boards",
              "text": home / "notes.txt", "escape": home / "a\x1b[2Jb.json"}[make]
    if make == "text":
        target.write_text("not a board", encoding="utf-8")
    before = sorted(str(p) for p in home.rglob("*"))
    argv = ["--open", str(target)] + (["--report"] if report else [])
    with pytest.raises(SystemExit) as err:
        _main(monkeypatch, *argv)
    assert err.value.code == 2
    out = capsys.readouterr().err
    assert out.startswith("taskboard: no board file at ") and "(--open opens an existing one)" in out
    assert "\x1b" not in out
    assert sorted(str(p) for p in home.rglob("*")) == before


async def test_TC_2410_open_of_a_registered_path_is_that_board(home):
    """TC-2410 (code review CR-3): `--open` of a registered board's own file opens that
    board as listed — its chip, no `not listed` — and records nothing (`last` kept)."""
    fx.build(home, last="course")
    before = (home / "boards.json").read_bytes()
    app = _open(unlisted=str(fx.board_path(home, "client-a")))
    assert app.board_id == "client-a"
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        assert app.board.label == ("Client A", "sky")
        assert not any("not one of them" in n for n in _notes(app))
    assert (home / "boards.json").read_bytes() == before


def test_TC_2410_open_and_board_together_are_refused(home, monkeypatch, capsys):
    """TC-2410: `--open X --board Y` → argparse's own refusal."""
    fx.build(home)
    with pytest.raises(SystemExit) as err:
        _main(monkeypatch, "--open", str(fx.copy_path(home)), "--board", str(fx.copy_path(home)))
    assert err.value.code == 2 and "not allowed with argument" in capsys.readouterr().err


async def test_TC_2410_the_unlisted_board_in_the_app(home):
    """TC-2410 (app): an unlisted file's label is `<name> · not listed` on pink with one
    or three boards; a switch to Personal relabels; a bracketed file name is printed
    as typed (S-1)."""
    fx.build(home)
    copy = fx.copy_path(home)
    one = TaskboardApp(board_path=copy, registry=Registry.single(home / "board.json"))
    assert one.board_id is None
    one._label_board()
    assert one.board.label == ("board-copy · not listed", "pink")
    app = _open(unlisted=str(copy))
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert app.board.label == ("board-copy · not listed", "pink")
        app.switch_board("main")
        assert app.board.label == ("Personal", "green")
    odd = home / "[x]copy.json"     # a bracketed name: a markup tag if parsed
    odd.write_bytes(copy.read_bytes())
    app = _open(unlisted=str(odd))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        assert app.board.label == ("[x]copy · not listed", "pink")
        # the notice is never parsed as markup (S-1; a parsed `\[` loses its backslash, S-14)
        opened = [n for n in app._notifications if "without adding it" in str(n.message)]
        assert opened and all(n.markup is False for n in opened)
        assert any(f"Opened {odd} without adding it" in str(n.message) for n in opened)


async def test_AT_2410_open_without_registering(home, monkeypatch):
    """AT-2410 (US-2407): `taskboard --open elsewhere/board-copy.json` leaves
    `boards.json` as it was, opens on the main screen with the chip ` board-copy · not
    listed ` and says why; `B` lists the three boards; a move out of it is refused."""
    fx.build(home, last="client-a")
    before = (home / "boards.json").read_bytes()
    built = _main(monkeypatch, "--open", str(fx.copy_path(home)))
    assert len(built) == 1
    app = built[0]
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        assert not isinstance(app.screen, BoardsHome)
        await pilot.pause(0.5)
        head = _svg_rows(app.export_screenshot(), 118, 30)[0]
        assert head.startswith(" board-copy · not listed "), head
        assert app.board.label == ("board-copy · not listed", "pink")
        assert any(n == (f"Opened {fx.copy_path(home)} without adding it to the boards "
                         "(--open). B lists the 3 boards; this file is not one of them.")
                   for n in _notes(app)), _notes(app)
        await _press(pilot, "B")
        assert isinstance(app.screen, BoardsHome)
        assert [e.name for e in app.screen.entries] == ["Personal", "Client A", "Course"]
        await _press(pilot, "escape", "P", "down", "m")
        assert any(n.startswith("This board is not listed (--open)") for n in _notes(app))
    assert (home / "boards.json").read_bytes() == before
