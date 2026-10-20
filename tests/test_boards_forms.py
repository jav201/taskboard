"""Several boards: create, rename and recolour, archive — from the home.

Batch 2026-10-20-batch-01 (variant C of the multi-board round, P4):
HLR-2205 / LLR-2205.1 · TC-2205 · AT-2205 (US-2203). Synthetic data only, under
this test's own temporary home.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

import pytest
from rich.text import Text

import multi_board_fixture as mb
from taskboard import boards, models, views
from taskboard.boards import Registry
from taskboard.models import DEFAULT_PHASES, PROJECT_COLORS, Board

NOW = datetime(2026, 10, 20, 9, 30)
SETTINGS = {"migrations": {"links": 1, "milestones": 1}, "seen_view_renumber_2026_07": True}
PAYLOADS = ["[@click=app.quit]x[/]", "tail\\", "[bold", "x[/]"]


class _Today(date):
    @classmethod
    def today(cls):
        return mb.TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


@pytest.fixture
def home(tmp_path, monkeypatch):
    from taskboard import app as app_module, modals
    import taskboard.__main__ as entry
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    monkeypatch.setattr(app_module, "datetime", _Now)
    monkeypatch.setattr(entry, "datetime", _Now)
    return tmp_path / ".taskboard"


def _reg(home) -> Registry:
    return Registry.load(home / "boards.json", home / "board.json")


def _open(board=None):
    from taskboard.__main__ import open_app
    return open_app(board)


async def _press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def _plain(widget) -> str:
    c = widget.content
    return c.plain if hasattr(c, "plain") else str(c)


def _scr(app) -> str:
    return type(app.screen).__name__


# --------------------------------------------------------------------------- #
# TC-2205 — the registry's writers and the form (LLR-2205.1)
# --------------------------------------------------------------------------- #
def test_TC_2205_create_makes_its_own_folder_and_an_empty_board(home):
    mb.build(home, "personal")
    reg = _reg(home)
    e = reg.create("Course · Kubernetes", "green", NOW, SETTINGS)
    p = home / "boards" / "course-kubernetes" / "board.json"
    assert (e.id, e.name, e.color, Path(e.path)) == ("course-kubernetes", "Course · Kubernetes",
                                                     "green", p.resolve())
    b = Board.load(p)
    assert b.projects == [] and b.tasks == [] and b.phases == list(DEFAULT_PHASES)
    assert b.settings == SETTINGS
    assert e.last_opened == "2026-10-20T09:30"
    assert _reg(home).get("course-kubernetes") is not None
    assert reg.create("Course · Kubernetes", "lime", NOW, SETTINGS).id == "course-kubernetes-2"


def test_TC_2205_a_folder_on_disk_is_never_written_into(home):
    """TC-2205: a folder not in the registry is skipped by the slug; when the
    uniqueness probe is made to miss it, the creation fails and writes nothing
    (architect A-22: kills `exist_ok=True`)."""
    mb.build(home, "personal")
    stray = home / "boards" / "x"
    stray.mkdir(parents=True)
    (stray / "keep.txt").write_text("mine", encoding="utf-8")
    reg = _reg(home)
    assert reg.create("X", "lime", NOW, SETTINGS).id == "x-2"
    assert [p.name for p in stray.iterdir()] == ["keep.txt"]
    before = (home / "boards.json").read_bytes()
    reg2 = _reg(home)
    reg2._unique_id = lambda base, taken=None: "x"
    with pytest.raises(FileExistsError):
        reg2.create("X", "lime", NOW, SETTINGS)
    assert [p.name for p in stray.iterdir()] == ["keep.txt"]
    assert (home / "boards.json").read_bytes() == before


@pytest.mark.parametrize("name", ["", "   ", "  \x1b  ", "\x00"])
def test_TC_2205_an_empty_name_is_refused(home, name):
    mb.build(home, "personal")
    reg = _reg(home)
    before = sorted(p.name for p in (home / "boards").iterdir())
    with pytest.raises(ValueError):
        reg.create(name, "lime", NOW, SETTINGS)
    assert sorted(p.name for p in (home / "boards").iterdir()) == before


def test_TC_2205_names_are_cut_and_reserved_slugs_suffixed(home):
    mb.build(home, "personal")
    reg = _reg(home)
    e = reg.create("N" * 61, "lime", NOW, SETTINGS)
    assert len(e.name) == 60
    assert reg.create("Con", "lime", NOW, SETTINGS).id == "con-board"
    assert (home / "boards" / "con-board" / "board.json").exists()


def test_TC_2205_edit_archive_and_free_color(home):
    mb.build(home, "personal")
    reg = _reg(home)
    assert reg.free_color() == "lime"
    reg.edit("course-docker", "Course · Containers", "blue")
    edited = _reg(home).get("course-docker")            # on disk before anything else saves
    assert (edited.name, edited.color) == ("Course · Containers", "blue")
    reg.archive("client-retail-rag")
    again = _reg(home)
    assert (again.get("course-docker").name, again.get("course-docker").color) == \
        ("Course · Containers", "blue")
    assert again.get("client-retail-rag").archived is True
    for i, c in enumerate(PROJECT_COLORS):
        again.entries.append(boards.BoardEntry(f"c{i}", "C", c, str(home / f"c{i}.json")))
    assert again.free_color() == "violet"


async def test_TC_2205_the_form(home):
    """TC-2205: the colour cycle wraps both ways; a blank name keeps the form open;
    a typed markup name paints literally; a 60-character name's file line fits."""
    from taskboard.modals import BoardForm
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        await _press(pilot, "n")
        form = app.screen
        assert type(form) is BoardForm and PROJECT_COLORS[form.hue] == "lime"
        for _ in range(8):
            await _press(pilot, "tab")
        assert PROJECT_COLORS[form.hue] == "lime"
        await _press(pilot, "shift+tab")
        assert PROJECT_COLORS[form.hue] == "pink"
        await _press(pilot, "enter")
        assert app.screen is form
        box = form.query_one("#bf-name")
        box.value = "Course · Docker"                 # its slug is taken: the preview says -2
        await pilot.pause()
        assert form.query_one("#bf-path").content.plain.endswith(
            "/boards/course-docker-2/board.json")     # the folder create will make (F3)
        box.value = "N" * 60
        await pilot.pause()
        line = form.query_one("#bf-path").content.plain
        assert len(line) <= form.BOX_W - 4 and line.endswith("…"), line
        await _press(pilot, "escape")
        assert _scr(app) == "BoardsHome"


async def test_TC_2205_a_typed_name_paints_literally(home):
    """TC-2205 (code review F2): a board created with a markup payload as its name
    paints it literally where a typed name is painted — the home card's title,
    the chip, the archive confirmation — and no span carries an action."""
    mb.build(home, "personal")
    app = _open()
    payload = "[@click=app.quit]x[/]"
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        await _press(pilot, "n")
        app.screen.query_one("#bf-name").value = payload
        await _press(pilot, "enter")
        assert app.board.label[0] == payload
        row0 = app.query_one("#board").content
        assert row0.plain.startswith(" " + payload + " ")
        await _press(pilot, "B")
        scr = app.screen
        idx = [e.name for e in scr.entries].index(payload)
        card = scr.query_one(f"#card-{idx}")
        assert card._border_title.plain == "▶ " + payload     # as Textual holds it
        assert r"\[@click" in card.border_title                # its markup escapes the bracket
        assert app.is_running


async def test_TC_2205_the_open_board_is_never_archived(home):
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        before = (home / "boards.json").read_bytes()
        await _press(pilot, "x")
        assert _scr(app) == "BoardsHome"
        assert (home / "boards.json").read_bytes() == before
        assert any(n.message == "The open board cannot be archived — open another board first."
                   for n in app._notifications)


async def test_TC_2205_the_chip_follows_a_rename_and_leaves_at_one_board(home):
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        await _press(pilot, "e")
        box = app.screen.query_one("#bf-name")
        box.value = "Home"
        await _press(pilot, "enter", "escape")
        assert app.board.label == ("Home", "green")
        for _ in range(3):
            await _press(pilot, "B", "right", "x")
            assert "Archive" in [str(b.label) for b in app.screen.query("Button")]
            await _press(pilot, "tab", "enter")
            await _press(pilot, "escape")
        assert len(app.registry.active()) == 1
        assert app.board.label is None


# --------------------------------------------------------------------------- #
# AT-2205 — create, rename, archive from the home (HLR-2205)
# --------------------------------------------------------------------------- #
async def test_AT_2205_manage_boards_from_the_home(home):
    """AT-2205 (US-2203): `n` creates a board in its own folder and opens it; `e`
    renames it and its chip; `x` archives another board, its folder intact; the
    open board refuses; a blank name does nothing."""
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        await _press(pilot, "n")
        form = app.screen
        assert "New board" in _plain(form.query_one("#bf-title"))
        assert _plain(form.query_one("#bf-path")) == "file    ~/.taskboard/boards/board/board.json"
        form.query_one("#bf-name").value = "Course · Kubernetes"
        await pilot.pause()
        assert _plain(form.query_one("#bf-path")) == \
            "file    ~/.taskboard/boards/course-kubernetes/board.json"
        assert _plain(form.query_one("#bf-hues")).endswith("lime")
        await _press(pilot, "tab", "enter")
        made = home / "boards" / "course-kubernetes" / "board.json"
        data = json.loads(made.read_text(encoding="utf-8"))
        assert data["projects"] == [] and data["tasks"] == []
        assert data["settings"] == SETTINGS
        assert not any(n.title == "View keys renumbered" for n in app._notifications)
        assert _scr(app) == "Screen"
        row0 = app.query_one("#board").content.plain.split("\n")[0]
        assert row0.startswith(" Course · Kubernetes "), row0
        reg = json.loads((home / "boards.json").read_text(encoding="utf-8"))
        assert (reg["boards"][-1]["id"], reg["boards"][-1]["color"]) == ("course-kubernetes",
                                                                           "green")
        await _press(pilot, "B")
        scr = app.screen
        assert len(scr.entries) == 5
        assert scr.entries[scr.cursor].id == "course-kubernetes"
        await _press(pilot, "e")
        app.screen.query_one("#bf-name").value = "Course · K8s"
        await _press(pilot, "enter")
        assert str(scr.query_one(f"#card-{scr.cursor}").border_title) == "▶ Course · K8s"
        await _press(pilot, "escape")
        row0 = app.query_one("#board").content.plain.split("\n")[0]
        assert row0.startswith(" Course · K8s "), row0
        client = home / "boards" / "client-retail-rag" / "board.json"
        kept = client.read_bytes()
        await _press(pilot, "B", "up", "up", "right")
        scr = app.screen
        assert scr.entries[scr.cursor].id == "client-retail-rag"
        await _press(pilot, "x")
        assert sorted(str(b.label) for b in app.screen.query("Button")) == ["Archive", "Cancel"]
        await _press(pilot, "tab", "enter")
        scr = app.screen
        assert type(scr).__name__ == "BoardsHome" and len(scr.entries) == 4
        assert _reg(home).get("client-retail-rag").archived is True
        assert client.read_bytes() == kept
        assert any(n.message.startswith("Archived Client · Retail RAG")
                   for n in app._notifications)
        scr.cursor = next(i for i, e in enumerate(scr.entries) if e.id == "course-kubernetes")
        before = (home / "boards.json").read_bytes()
        await _press(pilot, "x")
        assert len(app.screen.entries) == 4
        assert (home / "boards.json").read_bytes() == before
        await _press(pilot, "n", "enter")
        assert type(app.screen).__name__ == "BoardForm"
        assert not (home / "boards" / "board").exists()


async def test_TC_2205_a_registry_that_cannot_be_written(home, monkeypatch):
    """TC-2205 (code review N1, N2, carried from increment 001): a `boards.json`
    that cannot be written — at a switch the board still opens and a `Boards`
    notice says so; a rename says it was not made."""
    from taskboard import models as models_module
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()

        def boom(*a, **k):
            raise PermissionError("locked")
        monkeypatch.setattr(models_module.os, "replace", boom)
        await _press(pilot, "right", "enter")
        assert app.board_id == "client-retail-rag"
        notes = [n.message for n in app._notifications if n.title == "Boards"]
        assert any("could not be written" in m and "locked" in m for m in notes), notes
        await _press(pilot, "B", "e")
        app.screen.query_one("#bf-name").value = "Renamed"
        await _press(pilot, "enter")
        assert any(n.message.startswith("The board was not renamed") for n in app._notifications)
        assert _reg(home).get("client-retail-rag").name == "Client · Retail RAG"
        # ... and in memory too: the card and the next save keep the old name (F1)
        assert app.registry.get("client-retail-rag").name == "Client · Retail RAG"


def test_TC_2205_a_failed_registry_save_changes_nothing(home, monkeypatch):
    """TC-2205 (code review F1): when `boards.json` cannot be written, `create`,
    `edit` and `archive` leave the registry in memory as it is on disk — `create`
    also removes the folder it made — so the notice that says so is true."""
    mb.build(home, "personal")
    reg = _reg(home)
    before = [(e.id, e.name, e.color, e.archived) for e in reg.entries]
    folders = sorted(p.name for p in (home / "boards").iterdir())

    def boom(self):
        raise PermissionError("locked")
    monkeypatch.setattr(Registry, "save", boom)
    with pytest.raises(OSError):
        reg.create("Fresh", "lime", NOW, SETTINGS)
    with pytest.raises(OSError):
        reg.edit("course-docker", "Other", "blue")
    with pytest.raises(OSError):
        reg.archive("client-retail-rag")
    assert [(e.id, e.name, e.color, e.archived) for e in reg.entries] == before
    assert sorted(p.name for p in (home / "boards").iterdir()) == folders


def test_TC_2205_an_offset_time_in_the_registry_is_none(home):
    """TC-2205 (code review of increment 002, F1): `last_opened` with an offset is a
    hand edit — read as none, so `ago` and the home never meet an aware time."""
    reg_path = mb.build(home, "personal")
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    data["boards"][1]["last_opened"] = "2026-10-19T08:00+00:00"
    reg_path.write_text(json.dumps(data), encoding="utf-8")
    assert _reg(home).get("client-retail-rag").last_opened is None
