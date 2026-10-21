"""The people directory and the mention tokeniser (batch 2026-10-21-batch-01).

HLR-2501 / LLR-2501.1, LLR-2501.2 · TC-2501 · AT-2501 (US-2501) — one directory for
every board at `~/.taskboard/people.json`, read never raising, written atomically
under its lock as a read-modify-write; HLR-2502 / LLR-2502.1 · TC-2502 — a mention is
`@handle` at a word start, the handle derived from the name and never changed;
HLR-2507 / LLR-2507.1 · TC-2507 · AT-2507 — team sync carries a mention as its handle
text and nothing of the directory. Why it matters: the directory holds what the
operator wrote about real people; losing a person to a second window's write, or
pushing a role or a note to a teammate's folder, are the failures this pins.
Synthetic people only, under the seam's home.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

import people_round_fixture as fx
from taskboard import app as app_module, boards, models, modals, people, views
from taskboard.models import Board
from taskboard.people import Directory, handle_for, mention_ids, mention_line, split_mentions
from taskboard.team_sync import TeamState


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    return tmp_path / ".taskboard"


def _write(path: Path, data) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# TC-2501 — reading (LLR-2501.1)
# --------------------------------------------------------------------------- #
def test_TC_2501_a_missing_file_is_an_empty_directory_and_nothing_is_written(tmp_path):
    d = Directory.load(tmp_path / "people.json")
    assert d.people == {} and d.load_report == {}
    assert not (tmp_path / "people.json").exists()


def test_TC_2501_the_file_is_read_and_bad_entries_are_skipped(tmp_path):
    """A wrong handle, a repeated handle, a nameless or non-object entry is skipped;
    control bytes and line breaks go; each field is capped."""
    p = _write(tmp_path / "people.json", {"version": 1, "people": [
        {"id": "ana.ruiz", "name": "Ana Ruiz", "role": "Client A PM", "note": "Agenda\nfirst"},
        {"id": "ana.ruiz", "name": "Second Ana"},
        {"id": "Bad Handle", "name": "Bad"},
        {"id": "x.", "name": "Trailing dot"},
        {"id": "nobody", "name": "  "},
        "not an object",
        {"id": "esc", "name": "Esc\x1b[31mape", "role": "r" * 90, "note": 7},
        {"id": "long.one", "name": "n" * 61, "note": "x" * 201},
        {"id": "exact", "name": "m" * 60, "note": "y" * 200},
    ]})
    d = Directory.load(p)
    assert list(d.people) == ["ana.ruiz", "esc", "long.one", "exact"]
    assert (d.get("long.one").name, d.get("long.one").note) == ("n" * 60, "x" * 200)   # QA-7
    assert (d.get("exact").name, d.get("exact").note) == ("m" * 60, "y" * 200)
    assert d.get("ana.ruiz").note == "Agenda first"
    assert d.get("esc").name == "Esc[31mape" and d.get("esc").role == "r" * 60
    assert d.get("esc").note == ""
    assert d.get("ana.ruiz").name == "Ana Ruiz"


@pytest.mark.parametrize("raw", [b"{not json", b"[]", b'{"people": {}}', b"\xff\xfe"])
def test_TC_2501_an_unreadable_file_is_kept_aside_and_the_directory_starts_empty(tmp_path, raw):
    p = tmp_path / "people.json"
    p.write_bytes(raw)                                # bytes: `\xff\xfe` is no UTF-8 (CR-3)
    before = p.read_bytes()
    d = Directory.load(p)
    assert d.people == {} and d.load_report["unreadable"] is True
    assert Path(d.load_report["backup"]).read_bytes() == before
    assert p.read_bytes() == before                 # never rewritten by a read


# --------------------------------------------------------------------------- #
# TC-2501 — writing (LLR-2501.2)
# --------------------------------------------------------------------------- #
def test_TC_2501_add_derives_the_handle_and_writes_the_file(tmp_path):
    d = Directory.load(tmp_path / "people.json")
    live = d.people                                  # the live dict boards hold
    ana = d.add("  Ana   Ruiz ", "Client A PM")
    assert (ana.id, ana.name, ana.role, ana.note) == ("ana.ruiz", "Ana Ruiz", "Client A PM", "")
    assert d.add("Ana Ruiz", "Namesake").id == "ana.ruiz2"
    assert d.add("Andrés Lima").id == "andres.lima"
    assert live is d.people and live["andres.lima"].name == "Andrés Lima"
    raw = json.loads((tmp_path / "people.json").read_text(encoding="utf-8"))
    assert raw["version"] == 1
    assert [p["id"] for p in raw["people"]] == ["ana.ruiz", "ana.ruiz2", "andres.lima"]
    assert not list(tmp_path.glob("*.tmp")) and not list(tmp_path.glob("*.lock"))


@pytest.mark.parametrize("name, handle", [("Ana Ruiz", "ana.ruiz"), ("O'Brien-Smith Jo", "o.brien.smith.jo"),
                                          ("José  María", "jose.maria"), ("李", "person"),
                                          ("Ana . Ruiz", "ana.ruiz"), ("R2 D2", "r2.d2")])
def test_TC_2502_a_handle_is_the_name_folded_and_always_a_mention(name, handle):
    h = handle_for(name, set())
    assert h == handle
    assert mention_ids(f"see @{h}.") == [h]          # the handle reads back as a mention


def test_TC_2502_a_taken_handle_gets_the_next_number():
    assert handle_for("Ana Ruiz", {"ana.ruiz", "ana.ruiz2"}) == "ana.ruiz3"


def test_TC_2501_a_name_with_nothing_left_is_refused(tmp_path):
    d = Directory.load(tmp_path / "people.json")
    with pytest.raises(ValueError):
        d.add(" \x07 ")
    assert not (tmp_path / "people.json").exists()


def test_TC_2501_two_windows_never_erase_each_others_people(tmp_path):
    """A read-modify-write: a second directory that read the file before the first
    one's add keeps that add when it writes its own."""
    p = tmp_path / "people.json"
    one, two = Directory.load(p), Directory.load(p)
    one.add("Ana Ruiz")
    two.add("Marta Gil", "Accountant")
    assert sorted(Directory.load(p).people) == ["ana.ruiz", "marta.gil"]
    assert sorted(two.people) == ["ana.ruiz", "marta.gil"]
    # and the handle is unique against what the file holds now
    assert one.add("Marta Gil").id == "marta.gil2"


def test_TC_2501_edit_writes_back_a_person_the_file_lost_and_refuses_a_non_handle(tmp_path):
    """code review CR-5: a person another window's file no longer holds is written back;
    a string that is not a handle is never written."""
    p = tmp_path / "people.json"
    d = Directory.load(p)
    d.add("Luis Mora")
    p.write_text('{"version": 1, "people": []}', encoding="utf-8")
    d.edit("luis.mora", "Luis Mora", "Course TA", "")
    assert [x.id for x in Directory.load(p).people.values()] == ["luis.mora"]
    with pytest.raises(ValueError):
        d.edit("Not A Handle", "X", "", "")
    assert list(Directory.load(p).people) == ["luis.mora"]


def test_TC_2501_edit_keeps_the_handle(tmp_path):
    d = Directory.load(tmp_path / "people.json")
    d.add("Luis Mora", "Course TA")
    p = d.edit("luis.mora", "Luis Moreno", "Head TA", "Reviews every lab")
    assert (p.id, p.name, p.role, p.note) == ("luis.mora", "Luis Moreno", "Head TA",
                                              "Reviews every lab")
    assert {h: p.name for h, p in d.people.items()} == {"luis.mora": "Luis Moreno"}
    assert Directory.load(tmp_path / "people.json").get("luis.mora").name == "Luis Moreno"


def test_TC_2501_an_unparseable_file_that_cannot_be_kept_is_never_written_over(tmp_path, monkeypatch):
    p = _write(tmp_path / "people.json", "{broken")
    d = Directory(p)
    monkeypatch.setattr(people, "keep_aside", lambda path: None)
    with pytest.raises(OSError):
        d.add("Ana Ruiz")
    assert p.read_text(encoding="utf-8") == "{broken" and d.people == {}


def test_TC_2501_an_unparseable_file_is_kept_aside_before_it_is_replaced(tmp_path):
    p = _write(tmp_path / "people.json", "{broken")
    d = Directory(p)
    d.add("Ana Ruiz")
    assert (tmp_path / "people.json.corrupt").read_text(encoding="utf-8") == "{broken"
    assert list(Directory.load(p).people) == ["ana.ruiz"]


def test_TC_2501_a_held_lock_makes_the_write_wait_then_fail_and_change_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.2)
    p = tmp_path / "people.json"
    d = Directory.load(p)
    with boards.file_lock(p):
        with pytest.raises(OSError, match="busy"):
            d.add("Ana Ruiz")
    assert d.people == {} and not p.exists()


def test_TC_2501_a_failed_write_changes_nothing_in_memory(tmp_path, monkeypatch):
    d = Directory.load(tmp_path / "people.json")
    d.add("Ana Ruiz")

    def boom(path, text):
        raise OSError("disk full")
    monkeypatch.setattr(people, "write_atomic", boom)
    with pytest.raises(OSError):
        d.add("Marta Gil")
    assert list(d.people) == ["ana.ruiz"] and d.people["ana.ruiz"].name == "Ana Ruiz"


# --------------------------------------------------------------------------- #
# TC-2502 — the tokeniser (LLR-2502.1)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text, ids", [
    ("Ask @ana.ruiz about the stores.", ["ana.ruiz"]),
    ("Ask @ana.ruiz.", ["ana.ruiz"]),                 # a trailing dot is not the handle's
    ("@ana.ruiz, @diego.paz and @ana.ruiz again", ["ana.ruiz", "diego.paz"]),
    ("mail ana@x.com or @@ana", []),
    ("@Sofia is not a handle", []),
    ("(@elena.vidal)", ["elena.vidal"]),
    ("==send it to @diego.paz==", ["diego.paz"]),
    ("imported @[Ana Ruiz](p:ana.ruiz) note", ["ana.ruiz"]),
    ("a.@b c_@d", []),
    ("", []),
])
def test_TC_2502_mentions_are_read_at_word_starts(text, ids):
    assert mention_ids(text) == ids


def test_TC_2502_split_mentions_keeps_every_character():
    text = "Ask @ana.ruiz and @[Ana Ruiz](p:ana.ruiz) — ana@x.com"
    parts = split_mentions(text)
    assert "".join(p for p, _h in parts) == text
    assert [h for _p, h in parts if h] == ["ana.ruiz", "ana.ruiz"]


def test_TC_2502_mention_line_is_the_first_line_naming_the_person():
    notes = "Agenda to @elena.vidal by Monday\n- demo\n- ask @ana.ruiz for the criteria"
    assert mention_line(notes, "ana.ruiz") == "ask @ana.ruiz for the criteria"
    assert mention_line(notes, "elena.vidal") == "Agenda to @elena.vidal by Monday"
    assert mention_line(notes, "marta.gil") == ""


def test_TC_2502_find_puts_name_starts_first_then_inside_then_role(tmp_path):
    p = fx.build(tmp_path)
    d = Directory.load(p.parent / "people.json")
    assert [x.id for x in d.find("an")] == ["ana.ruiz", "andres.lima", "juana.soto",
                                              "marta.gil"]
    assert [x.id for x in d.find("andres")] == ["andres.lima"]      # accents folded
    assert [x.id for x in d.find("pm")] == ["ana.ruiz"]              # the role
    assert len(d.find("")) == 8 and d.find("zz") == []
    assert d.named("ANDRES LIMA").id == "andres.lima" and d.named("Nobody") is None


# --------------------------------------------------------------------------- #
# AT-2501 — the app holds one directory for every board
# --------------------------------------------------------------------------- #
async def test_AT_2501_one_directory_for_every_board(home):
    """`open_app` on the round's boards: the directory is `~/.taskboard/people.json`,
    every board the app opens draws from the same names, and no board file holds
    them."""
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert app.people.path == home / "people.json"
        assert len(app.people.people) == 8
        assert app.board.people is app.people.people
        app.pop_screen()                              # the home
        await pilot.pause()
        app.switch_board("course")
        await pilot.pause()
        assert app.board_id == "course" and app.board.people is app.people.people
        app.people.add("Sofia Vega", "Legal counsel")
        assert app.board.people["sofia.vega"].name == "Sofia Vega"
        app.board.save()
    for bid in ("main", "client-a", "course"):
        raw = json.loads(fx.board_path(home, bid).read_text(encoding="utf-8"))
        assert '"people"' not in json.dumps(raw) and "Sofia Vega" not in json.dumps(raw)


async def test_AT_2501_an_unreadable_directory_is_said_and_kept(home):
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    (home / "people.json").write_text("{oops", encoding="utf-8")
    app = open_app(None)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        notes = [str(n.message) for n in app._notifications]
        assert any(n.startswith("people.json could not be read; a copy was kept at ")
                   and n.endswith("The people directory starts empty.") for n in notes)
        assert app.people.people == {}
    assert (home / "people.json.corrupt").read_text(encoding="utf-8") == "{oops"


async def test_AT_2501_an_app_without_a_registry_never_writes_a_directory(tmp_path):
    from taskboard.app import TaskboardApp
    app = TaskboardApp(board_path=tmp_path / "b" / "board.json")
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        assert app.people.path == tmp_path / "b" / "people.json"
    assert not (tmp_path / "b" / "people.json").exists()


# --------------------------------------------------------------------------- #
# TC-2507 / AT-2507 — team sync carries the handle text and nothing of the directory
# --------------------------------------------------------------------------- #
def test_AT_2507_a_push_carries_mentions_as_handles_and_no_directory(tmp_path):
    root = tmp_path / "home"
    fx.build(root)
    board = Board.load(fx.board_path(root, "client-a"))
    board.people = Directory.load(root / "people.json").people
    team = tmp_path / "team"
    team.mkdir()
    state = TeamState(team, user_id="u1",
                      config={"projects": [{"id": p.id} for p in board.projects]})
    assert state.push(board)
    files = sorted(x.name for x in team.iterdir())
    assert files == ["board.u1.json"]
    text = (team / "board.u1.json").read_text(encoding="utf-8")
    assert "@ana.ruiz" in text and "@elena.vidal" in text
    for leaked in ("Ana Ruiz", "Client A PM", "Prefers a written agenda", "Elena Vidal",
                   "Steering committee chair", "people"):
        assert leaked not in text, leaked


def test_TC_2501_an_empty_file_is_an_empty_directory_and_nothing_is_said(tmp_path):
    """architect A-6: a 0-byte (or blank) file holds nothing to keep — no notice, no copy."""
    for raw in ("", "  \n"):
        p = _write(tmp_path / "people.json", raw)
        d = Directory.load(p)
        assert d.people == {} and d.load_report == {}
    assert not list(tmp_path.glob("*.corrupt*"))


async def test_AT_2501_a_copy_that_could_not_be_kept_is_said_so(home, monkeypatch):
    """architect A-6: the notice never names a copy that does not exist."""
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    (home / "people.json").write_text("{oops", encoding="utf-8")
    monkeypatch.setattr(people, "keep_aside", lambda path: None)
    app = open_app(None)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        notes = [str(n.message) for n in app._notifications]
        assert "people.json could not be read; no copy could be kept. The people directory " \
               "starts empty." in notes


@pytest.mark.parametrize("text", ["@[" * 50000, "@[" + "x" * 99000, "a@" * 50000,
                                  "".join(f"@h{i} " for i in range(40000))],
                         ids=["at-bracket-x50000", "one-open-link", "a-at-x50000", "distinct-x40000"])
def test_TC_2507_a_crafted_note_is_tokenised_in_linear_time(text):
    """security S-1, code review CR-1: one pasted or pulled line of `@[` repeated, or of
    40 000 distinct handles, must not freeze a render. Linear, these take about 0.1 s of
    CPU; quadratic, ~25 s and ~6 s. The bound is CPU time, 2 s, so a loaded host does
    not make it flaky (CR-2) and a quadratic regression still fails it."""
    import time
    t0 = time.process_time()
    mention_ids(text)
    split_mentions(text)
    mention_line(text, "ana.ruiz")
    assert time.process_time() - t0 < 2.0
