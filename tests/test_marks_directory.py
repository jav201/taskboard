"""The marks directory and the task's `mark` field (batch 2026-10-24-batch-01).

HLR-2601 / LLR-2601.1, LLR-2601.2 · TC-2601 — the directory at
`~/.taskboard/marks.json`: read never raising, a bad entry skipped, written
atomically under its lock as a read-modify-write; HLR-2602 / LLR-2602.1 ·
TC-2602 — `Task.mark` written only when set, an unknown id kept byte-for-byte;
HLR-2603 / LLR-2603.1, LLR-2603.2 · TC-2603 · AT-2602 (`test_AT_2602_the_store_is_safe`)
— two windows lose nothing, a broken file is kept never overwritten, a board
without marks keeps its bytes; LLR-2601.3 · TC-2601 (the hand-off arms) — the
app loads the directory beside `people.json`, hands the live dict to every
board, warns once at mount; LLR-2602.2 · TC-2607 — team sync carries the id and
nothing of the directory. AT-2601's realising node lands with the `#` manager
(increment 003, `tests/test_marks_manager.py`); its store-side arms reachable
in 001 are the TC-2601 arms below. Synthetic classes and boards only, under
the seam's home.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

import milestone_marks_fixture as fx
from taskboard import app as app_module, boards, marks, models, views
from taskboard.marks import COLOURS, MARKS_NAME, SHAPES, Directory
from taskboard.models import Board, Task
from taskboard.team_sync import TeamState


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views):
        monkeypatch.setattr(mod, "date", _Today)
    return tmp_path / ".taskboard"


def _write(path: Path, data) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# TC-2601 — reading (LLR-2601.1)
# --------------------------------------------------------------------------- #
def test_TC_2601_a_missing_file_is_an_empty_directory_and_nothing_is_written(tmp_path):
    d = Directory.load(tmp_path / MARKS_NAME)
    assert d.marks == {} and d.load_report == {}
    assert not (tmp_path / MARKS_NAME).exists()


def test_TC_2601_an_empty_or_blank_file_is_an_empty_directory_and_nothing_is_said(tmp_path):
    """A 0-byte (or blank) file holds nothing to keep — no notice, no copy."""
    for raw in ("", "  \n"):
        p = _write(tmp_path / MARKS_NAME, raw)
        d = Directory.load(p)
        assert d.marks == {} and d.load_report == {}
    assert not list(tmp_path.glob("*.corrupt*"))


def test_TC_2601_the_file_is_read_and_bad_entries_are_skipped(tmp_path):
    """The load/skip validation, unit-tested directly (cyclomatic >= 3: the id,
    the name, the shape, the colour, the types, the cap, the one-line flatten):
    a repeated id, a malformed id, no name, an unknown shape or colour, a
    field of the wrong type is skipped; the name caps at 60 (61 cut, 60 whole)
    and flattens to one line; control bytes go, a markup-looking name stays as
    typed; `hidden` coerces to bool."""
    p = _write(tmp_path / MARKS_NAME, {"version": 1, "marks": [
        {"id": "payment", "name": "Payment", "shape": "⬢", "colour": "amber"},
        {"id": "payment", "name": "Second Payment", "shape": "■", "colour": "pink"},
        {"id": "Bad Id", "name": "Bad", "shape": "■", "colour": "pink"},
        {"id": "noname", "name": "  ", "shape": "■", "colour": "pink"},
        {"id": "badshape", "name": "X", "shape": "◆", "colour": "pink"},   # ◆ is not in SHAPES
        {"id": "badcolour", "name": "Y", "shape": "■", "colour": "maroon"},
        {"id": "typed1", "name": 7, "shape": "■", "colour": "pink"},
        {"id": "typed2", "name": "Z", "shape": 5, "colour": "pink"},
        {"id": "typed3", "name": "W", "shape": "■", "colour": True},
        {"id": "long", "name": "n" * 61, "shape": "★", "colour": "lime"},
        {"id": "exact", "name": "m" * 60, "shape": "⬟", "colour": "orange"},
        {"id": "multiline", "name": "Two\nlines\tname", "shape": "▼", "colour": "sky"},
        {"id": "esc", "name": "Esc\x1b[31mape", "shape": "✦", "colour": "green"},
        {"id": "markup", "name": "[b]x[/b]", "shape": "⚑", "colour": "cyan"},
        {"id": "hidden1", "name": "H", "shape": "▲", "colour": "cyan", "hidden": "yes"},
        "not an object",
    ]})
    d = Directory.load(p)
    assert list(d.marks) == ["payment", "long", "exact", "multiline", "esc", "markup", "hidden1"]
    assert d.marks["payment"].shape == "⬢" and d.marks["payment"].colour == "amber"
    assert d.marks["payment"].hidden is False
    assert d.marks["long"].name == "n" * 60                    # the 61st character cut
    assert d.marks["exact"].name == "m" * 60                   # 60 kept whole
    assert d.marks["multiline"].name == "Two lines name"       # every whitespace run one space
    assert d.marks["esc"].name == "Esc[31mape"                 # the ANSI introducer stripped
    assert d.marks["markup"].name == "[b]x[/b]"                # markup-looking, kept as typed
    assert d.marks["hidden1"].hidden is True                   # coerced to bool


@pytest.mark.parametrize("raw", [b"{not json", b"[]", b'{"marks": {}}', b"\xff\xfe"])
def test_TC_2601_an_unreadable_file_is_kept_aside_and_the_directory_starts_empty(tmp_path, raw):
    p = tmp_path / MARKS_NAME
    p.write_bytes(raw)                              # bytes: `\xff\xfe` is no UTF-8
    before = p.read_bytes()
    d = Directory.load(p)
    assert d.marks == {} and d.load_report["unreadable"] is True
    assert Path(d.load_report["backup"]).read_bytes() == before
    assert p.read_bytes() == before                 # never rewritten by a read


def test_TC_2601_find_resolves_a_prefix_only_and_lower_case(tmp_path):
    fx.build(tmp_path)
    d = Directory.load(tmp_path / MARKS_NAME)
    assert d.find("pay").id == "payment"
    assert d.find("PAY").id == "payment"            # the round's lower-case match
    assert d.find("ment") is None                   # never inside the name
    assert d.find("p").id == "payment"              # the only name starting with `p`
    assert d.find("").id == "delivery"              # everything sorted; empty resolves the first
    assert d.find("zzz") is None


# --------------------------------------------------------------------------- #
# TC-2601 — writing (LLR-2601.2)
# --------------------------------------------------------------------------- #
def test_TC_2601_add_derives_the_id_and_writes_the_file(tmp_path):
    d = Directory.load(tmp_path / MARKS_NAME)
    live = d.marks                                  # the live dict boards hold
    pay = d.add("  Payment ", "⬢", "amber")
    assert (pay.id, pay.name, pay.shape, pay.colour, pay.hidden) == \
        ("payment", "Payment", "⬢", "amber", False)
    assert d.add("Payment", "★", "pink").id == "payment2"
    assert live is d.marks and live["payment"].name == "Payment"
    raw = json.loads((tmp_path / MARKS_NAME).read_text(encoding="utf-8"))
    assert raw["version"] == 1
    assert [m["id"] for m in raw["marks"]] == ["payment", "payment2"]
    assert all(m["hidden"] is False for m in raw["marks"])
    assert not list(tmp_path.glob("*.tmp")) and not list(tmp_path.glob("*.lock"))


def test_TC_2601_a_name_with_nothing_left_is_refused(tmp_path):
    d = Directory.load(tmp_path / MARKS_NAME)
    with pytest.raises(ValueError):
        d.add(" \x07 ", "■", "pink")
    assert not (tmp_path / MARKS_NAME).exists()


def test_TC_2601_a_shape_or_colour_outside_the_sets_is_refused(tmp_path):
    """The write boundary mirrors the load validation: `◆` is the unclassified
    glyph, never a storable shape, and an unknown tone is not storable."""
    d = Directory.load(tmp_path / MARKS_NAME)
    with pytest.raises(ValueError):
        d.add("X", "◆", "pink")
    with pytest.raises(ValueError):
        d.add("X", "■", "maroon")
    with pytest.raises(ValueError):
        d.edit("payment", "X", "◆", "pink")
    assert not (tmp_path / MARKS_NAME).exists()


def test_TC_2601_two_directories_on_one_file_both_survive_an_add(tmp_path):
    """The read-modify-write under the lock: a second directory that read the
    file before the first one's add keeps that add when it writes its own."""
    p = tmp_path / MARKS_NAME
    one, two = Directory.load(p), Directory.load(p)
    one.add("Payment", "⬢", "amber")
    two.add("Review", "■", "violet")
    assert sorted(Directory.load(p).marks) == ["payment", "review"]
    assert sorted(two.marks) == ["payment", "review"]
    # and the id is unique against what the file holds now
    assert one.add("Review", "★", "pink").id == "review2"


def test_TC_2601_edit_keeps_the_id_and_writes_back_a_class_the_file_lost(tmp_path):
    p = tmp_path / MARKS_NAME
    d = Directory.load(p)
    d.add("Payment", "⬢", "amber")
    p.write_text('{"version": 1, "marks": []}', encoding="utf-8")
    m = d.edit("payment", "Billing", "★", "pink")
    assert (m.id, m.name, m.shape, m.colour) == ("payment", "Billing", "★", "pink")
    assert [x.id for x in Directory.load(p).marks.values()] == ["payment"]
    with pytest.raises(ValueError):
        d.edit("Not An Id", "X", "■", "pink")
    assert list(Directory.load(p).marks) == ["payment"]


def test_TC_2601_edit_and_set_hidden_keep_the_rest_of_the_class(tmp_path):
    d = Directory.load(tmp_path / MARKS_NAME)
    d.add("Payment", "⬢", "amber")
    assert d.set_hidden("payment", True).hidden is True
    m = d.edit("payment", "Billing", "★", "pink")
    assert (m.id, m.hidden) == ("payment", True)    # the id and the flag survive a rename
    raw = json.loads((tmp_path / MARKS_NAME).read_text(encoding="utf-8"))
    assert raw["marks"][0] == {"id": "payment", "name": "Billing", "shape": "★",
                               "colour": "pink", "hidden": True}
    assert d.set_hidden("payment", False).hidden is False
    assert Directory.load(tmp_path / MARKS_NAME).marks["payment"].hidden is False
    with pytest.raises(ValueError):
        d.set_hidden("ghost", True)


def test_TC_2601_an_unparseable_file_is_kept_aside_before_it_is_replaced(tmp_path):
    p = _write(tmp_path / MARKS_NAME, "{broken")
    d = Directory(p)
    d.add("Payment", "⬢", "amber")
    assert (tmp_path / "marks.json.corrupt").read_text(encoding="utf-8") == "{broken"
    assert list(Directory.load(p).marks) == ["payment"]


def test_TC_2601_an_unparseable_file_that_cannot_be_kept_is_never_written_over(tmp_path, monkeypatch):
    p = _write(tmp_path / MARKS_NAME, "{broken")
    d = Directory(p)
    monkeypatch.setattr(marks, "keep_aside", lambda path: None)
    with pytest.raises(OSError):
        d.add("Payment", "⬢", "amber")
    assert p.read_text(encoding="utf-8") == "{broken" and d.marks == {}


def test_TC_2601_a_held_lock_makes_the_write_wait_then_fail_and_change_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.2)
    p = tmp_path / MARKS_NAME
    d = Directory.load(p)
    with boards.file_lock(p):
        with pytest.raises(OSError, match="busy"):
            d.add("Payment", "⬢", "amber")
    assert d.marks == {} and not p.exists()


def test_TC_2601_a_failed_write_changes_nothing_in_memory(tmp_path, monkeypatch):
    d = Directory.load(tmp_path / MARKS_NAME)
    d.add("Payment", "⬢", "amber")

    def boom(path, text):
        raise OSError("disk full")
    monkeypatch.setattr(marks, "write_atomic", boom)
    with pytest.raises(OSError):
        d.add("Review", "■", "violet")
    assert list(d.marks) == ["payment"] and d.marks["payment"].name == "Payment"


# --------------------------------------------------------------------------- #
# TC-2602 — the `mark` field round-trips, written only when set (LLR-2602.1)
# --------------------------------------------------------------------------- #
def test_TC_2602_a_mark_round_trips_through_the_model():
    t = Task.from_dict({"id": "t1", "title": "Pilot launch", "milestone": True,
                        "mark": "payment"})
    assert t.mark == "payment"
    d = Board._to_dict(t)
    assert d["mark"] == "payment"
    t2 = Task.from_dict(d)
    assert (t2.mark, t2.milestone) == ("payment", True)


def test_TC_2602_a_task_without_a_mark_saves_with_no_mark_key():
    t = Task.from_dict({"id": "t1", "title": "Plain", "milestone": True})
    assert t.mark is None
    assert "mark" not in Board._to_dict(t)


def test_TC_2602_a_board_without_marks_keeps_its_bytes_through_a_load_and_a_save(tmp_path):
    root = tmp_path / "home"
    fx.build(root, marks=False)
    for bid in ("main", "client-a", "course"):
        p = fx.board_path(root, bid)
        before = p.read_bytes()
        board = Board.load(p)
        board.save_atomic()
        assert p.read_bytes() == before
        assert '"mark"' not in p.read_text(encoding="utf-8")


def test_TC_2602_an_unknown_id_is_kept_byte_for_byte_through_a_save(tmp_path):
    """An id no directory holds (a deleted class, a teammate's class) passes
    every load and save untouched — the field never degrades (AT-2607's store
    arms; the drawn-and-edited arms land with the seat, increment 002)."""
    root = tmp_path / "home"
    fx.build(root)
    p = fx.board_path(root, "client-a")
    board = Board.load(p)
    ghost = next(t for t in board.tasks if t.id == "tce")
    ghost.mark = "teammates-class"
    board.save_atomic()
    assert '"mark": "teammates-class"' in p.read_text(encoding="utf-8")
    board2 = Board.load(p)
    assert next(t for t in board2.tasks if t.id == "tce").mark == "teammates-class"


def test_TC_2602_unticking_milestone_keeps_the_mark(tmp_path):
    """MM-D3: unticking `milestone` keeps the field, so the class returns when
    the box is ticked again."""
    root = tmp_path / "home"
    fx.build(root)
    p = fx.board_path(root, "client-a")
    board = Board.load(p)
    t = next(t for t in board.tasks if t.id == "tcb")
    t.milestone = False                             # the editor's untick, at the model
    board.save_atomic()
    entry = next(x for x in json.loads(p.read_text(encoding="utf-8"))["tasks"]
                 if x["id"] == "tcb")
    assert entry["mark"] == "launch"


def test_TC_2602_only_marked_tasks_gain_the_key(tmp_path):
    root = tmp_path / "home"
    fx.build(root)
    p = fx.board_path(root, "client-a")
    Board.load(p).save_atomic()
    raw = json.loads(p.read_text(encoding="utf-8"))
    marked = {x["id"] for x in raw["tasks"] if "mark" in x}
    assert marked == {"tc1", "tc4", "tc6", "tc7", "tc8", "tc9", "tcb", "tcc", "tce"}


# --------------------------------------------------------------------------- #
# TC-2603 / AT-2602 — the store is safe beside a second window (HLR-2603)
# --------------------------------------------------------------------------- #
def test_TC_2603_ten_interleaved_adds_lose_nothing(tmp_path):
    p = tmp_path / MARKS_NAME
    dirs = [Directory.load(p) for _ in range(10)]
    names = [f"Class {i}" for i in range(10)]
    for i, d in enumerate(dirs):
        d.add(names[i], SHAPES[i % len(SHAPES)], COLOURS[i % len(COLOURS)])
    final = Directory.load(p)
    assert len(final.marks) == 10
    assert {m.name for m in final.marks.values()} == set(names)
    # each writer's live dict holds the file as its own last write saw it
    assert [len(d.marks) for d in dirs] == list(range(1, 11))


def test_TC_2603_the_corrupt_copy_is_never_replaced(tmp_path):
    p = tmp_path / MARKS_NAME
    p.write_text("{oops", encoding="utf-8")
    d = Directory.load(p)
    assert d.load_report["unreadable"] is True
    assert (tmp_path / "marks.json.corrupt").read_text(encoding="utf-8") == "{oops"
    p.write_text("[bad", encoding="utf-8")           # a SECOND unreadable file
    d2 = Directory.load(p)
    assert d2.load_report["unreadable"] is True
    copies = {x.name: x.read_text(encoding="utf-8")
              for x in tmp_path.glob("marks.json.corrupt*")}
    assert copies == {"marks.json.corrupt": "{oops", "marks.json.corrupt-2": "[bad"}
    assert p.read_bytes() == b"[bad"                # the read never rewrites


def test_AT_2602_the_store_is_safe(tmp_path, monkeypatch):
    """AT-2602 (HLR-2603): two `Directory` objects on one `marks.json` — the code
    a second process runs — each keeps the other's classes; an unreadable file
    is kept aside, never overwritten; a no-mark board keeps its bytes; the held
    lock refuses the write, named `busy`, nothing changed."""
    p = tmp_path / MARKS_NAME
    one, two = Directory.load(p), Directory.load(p)
    one.add("Payment", "⬢", "amber")
    two.add("Review", "■", "violet")
    assert sorted(Directory.load(p).marks) == ["payment", "review"]
    assert sorted(two.marks) == ["payment", "review"]   # gained after its own write
    one.add("Delivery", "▲", "cyan")
    assert sorted(one.marks) == ["delivery", "payment", "review"]

    bad = tmp_path / "broken" / MARKS_NAME
    bad.parent.mkdir()
    bad.write_text("{oops", encoding="utf-8")
    d = Directory.load(bad)
    assert d.marks == {} and d.load_report["unreadable"] is True
    assert (bad.parent / "marks.json.corrupt").read_bytes() == b"{oops"
    assert bad.read_bytes() == b"{oops"
    bad.write_text("[1,2", encoding="utf-8")             # a later unreadable file
    Directory.load(bad)
    assert (bad.parent / "marks.json.corrupt").read_bytes() == b"{oops"  # the first copy kept

    root = tmp_path / "home"
    fx.build(root, marks=False)
    bp = fx.board_path(root, "client-a")
    before = bp.read_bytes()
    Board.load(bp).save_atomic()
    assert bp.read_bytes() == before

    monkeypatch.setattr(boards, "LOCK_WAIT", 0.2)
    locked_path = tmp_path / "locked" / MARKS_NAME
    locked_path.parent.mkdir(parents=True)          # a write mkdirs first; the lock alone doesn't
    locked = Directory.load(locked_path)
    with boards.file_lock(locked_path):
        with pytest.raises(OSError, match="busy"):
            locked.add("Launch", "★", "pink")
    assert locked.marks == {} and not locked_path.exists()


# --------------------------------------------------------------------------- #
# TC-2607 — team sync carries the id and nothing of the directory (LLR-2602.2)
# --------------------------------------------------------------------------- #
def test_TC_2607_a_push_carries_the_id_and_nothing_of_the_directory(tmp_path):
    root = tmp_path / "home"
    fx.build(root)
    board = Board.load(fx.board_path(root, "client-a"))
    board.marks = Directory.load(root / MARKS_NAME).marks
    team = tmp_path / "team"
    team.mkdir()
    state = TeamState(team, user_id="u1",
                      config={"projects": [{"id": p.id} for p in board.projects]})
    assert state.push(board)
    files = sorted(x.name for x in team.iterdir())
    assert files == ["board.u1.json"]
    text = (team / "board.u1.json").read_text(encoding="utf-8")
    assert '"mark": "payment"' in text and '"mark": "review"' in text
    for leaked in ('"name": "Payment"', '"name": "Delivery"', '"name": "Launch"',
                   '"name": "Review"', '"shape"', '"colour"', "⬢", "▲", "marks"):
        assert leaked not in text, leaked
    import taskboard.team_sync as team_sync
    assert "marks.json" not in Path(team_sync.__file__).read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# TC-2601 — the hand-off arms (LLR-2601.3): the app holds the directory
# --------------------------------------------------------------------------- #
async def test_TC_2601_the_app_holds_the_directory_and_hands_it_to_every_board(home):
    """`open_app` on the round's boards: the directory is
    `<home>/.taskboard/marks.json`, every board the app opens shares the one
    live dict, and no board file holds the directory. AT-2601's store arms
    (the restart clause included); its `#`-driven arms land with the manager
    (increment 003)."""
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert app.marks.path == home / MARKS_NAME
        assert sorted(app.marks.marks) == ["delivery", "launch", "payment", "review"]
        assert app.board.marks is app.marks.marks
        app.pop_screen()                              # the home
        await pilot.pause()
        app.switch_board("course")
        await pilot.pause()
        assert app.board_id == "course" and app.board.marks is app.marks.marks
        app.marks.add("Billing", "★", "pink")         # written the store's way (003 adds `#`)
        await pilot.pause()
        assert app.board.marks["billing"].shape == "★"
        app.board.save()
    for bid in ("main", "client-a", "course"):
        raw = fx.board_path(home, bid).read_text(encoding="utf-8")
        assert '"marks"' not in raw                    # the directory never lands in a board
        for name in ("Delivery", "Payment", "Launch"):
            assert name not in raw


async def test_TC_2601_after_move_carries_the_directory(home):
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        app.pop_screen()                              # the home
        await pilot.pause()
        new_src = Board.load(fx.board_path(home, "course"))
        app.after_move(new_src)
        await pilot.pause()
        assert app.board is new_src
        assert app.board.marks is app.marks.marks


async def test_TC_2601_an_unreadable_directory_is_said_and_kept(home):
    """HLR-2601's notice, once, at mount (the `people.json` pattern)."""
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    (home / MARKS_NAME).write_text("{oops", encoding="utf-8")
    app = open_app(None)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        notes = [str(n.message) for n in app._notifications]
        assert any(n.startswith("marks.json could not be read; a copy was kept at ")
                   and n.endswith("The marks directory starts empty.") for n in notes)
        assert app.marks.marks == {}
    assert (home / "marks.json.corrupt").read_text(encoding="utf-8") == "{oops"


async def test_TC_2601_an_app_without_a_registry_never_writes_a_directory(tmp_path):
    from taskboard.app import TaskboardApp
    app = TaskboardApp(board_path=tmp_path / "b" / "board.json")
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        assert app.marks.path == tmp_path / "b" / MARKS_NAME
    assert not (tmp_path / "b" / MARKS_NAME).exists()


async def test_TC_2601_a_class_written_through_the_store_survives_a_restart(home):
    """AT-2601's restart clause, store side: what the manager's `n` + save will
    write lands in `marks.json` and is still there when the app opens again."""
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        app.marks.add("Billing", "★", "pink")
    raw = json.loads((home / MARKS_NAME).read_text(encoding="utf-8"))
    assert raw["marks"][-1] == {"id": "billing", "name": "Billing", "shape": "★",
                                "colour": "pink", "hidden": False}
    app2 = open_app(None)
    async with app2.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert app2.marks.marks["billing"].name == "Billing"
        assert app2.board.marks is app2.marks.marks


async def test_TC_2603_a_fresh_home_has_no_marks_json_after_open_app_alone(home):
    """MM-D4: no seeded classes — nothing is written until a class is added."""
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    (home / MARKS_NAME).unlink()
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert app.marks.marks == {}
    assert not (home / MARKS_NAME).exists()
