"""Several boards: moving a project to another board.

Batch 2026-10-20-batch-01 (variant C of the multi-board round, P3):
HLR-2206 / LLR-2206.1 · TC-2206 · AT-2206 (US-2204). Synthetic data only: the
round's boards (`tests/multi_board_fixture.py`) under this test's own home.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
from datetime import date, datetime
from pathlib import Path

import pytest

import multi_board_fixture as mb
from taskboard import boards, models, views
from taskboard.boards import move_plan, move_project, peek_board
from taskboard.models import Board, Project, Task

DAY = "2026-10-20"
NOW = datetime(2026, 10, 20, 9, 30)
ROUND = Path(__file__).resolve().parents[1] / "prototypes" / "multi_board" / "out"
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


def _pair(home):
    """Main (the source) and Client · Retail RAG (the target), as files."""
    mb.build(home, "main")
    return home / "board.json", home / "boards" / "client-retail-rag" / "board.json"


def _snap(*folders) -> dict:
    out = {}
    for f in folders:
        for p in sorted(Path(f).rglob("*")):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def _deps(path) -> dict:
    return {t["id"]: t["depends_on"] for t in json.loads(Path(path).read_text(
        encoding="utf-8"))["tasks"]}


def _image(home, src: Path) -> Path:
    """A pasted image of tr3 in Main's folder, referenced by its absolute path."""
    img = src.parent / "images" / "tr3" / "paste-001.png"
    img.parent.mkdir(parents=True)
    img.write_bytes(b"\x89PNG fake")
    data = json.loads(src.read_text(encoding="utf-8"))
    for t in data["tasks"]:
        if t["id"] == "tr3":
            t["images"] = [str(img.resolve()), "relative.png", str(home.parent / "else.png")]
    src.write_text(json.dumps(data), encoding="utf-8")
    return img


# --------------------------------------------------------------------------- #
# TC-2206 — the plan (LLR-2206.1)
# --------------------------------------------------------------------------- #
def test_TC_2206_the_plan_of_the_rounds_move(home):
    src_p, dst_p = _pair(home)
    plan = move_plan(Board.load(src_p), peek_board(dst_p), "pmr", set(), set())
    assert plan.refusal is None
    assert len(plan.tasks) == 7 and plan.kept == 3
    assert [(a.id, b.id) for a, b in plan.crossing] == [("tw2", "tr4"), ("tr3", "tl3")]


def _refused(home, why, mutate=None, src_team=frozenset(), dst_team=frozenset()):
    src_p, dst_p = _pair(home)
    if mutate:
        mutate(src_p, dst_p)
    before = _snap(home)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", None if src_team is None else set(src_team),
                     None if dst_team is None else set(dst_team))
    assert plan.refusal is not None and why in plan.refusal, plan.refusal
    with pytest.raises(OSError):
        move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert _snap(home) == before


def _edit(path, fn):
    data = json.loads(path.read_text(encoding="utf-8"))
    fn(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_TC_2206_shared_in_team_mode_either_side(home):
    _refused(home, "shared in team mode", src_team={"pmr"})
    _refused(home, "shared in team mode", dst_team={"pmr"})


def test_TC_2206_an_unreadable_team_configuration(home):
    _refused(home, "cannot be read", src_team=None)
    _refused(home, "cannot be read", dst_team=None)


@pytest.mark.parametrize("bad", ["..", "../x", "a/b", "C:\\x", 7])
def test_TC_2206_an_id_that_cannot_name_a_folder(home, bad):
    def m(src, _dst):
        _edit(src, lambda d: next(t for t in d["tasks"] if t["id"] == "tr6").update(id=bad))
    _refused(home, "cannot name a folder", m)


def test_TC_2206_the_target_holds_a_moving_id(home):
    def m(_src, dst):
        _edit(dst, lambda d: d["tasks"].append({"id": "tr1", "title": "Clash"}))
    _refused(home, "already holds the id tr1", m)


def test_TC_2206_the_target_holds_an_image_folder(home):
    def m(_src, dst):
        (dst.parent / "images" / "tr2").mkdir(parents=True)
    _refused(home, "already holds images/tr2", m)


def test_TC_2206_the_target_lacks_a_phase(home):
    def m(_src, dst):
        _edit(dst, lambda d: d.update(phases=["Backlog", "Doing", "Done"]))
    _refused(home, "no phase 'Next'", m)


def test_TC_2206_a_missing_or_unreadable_target_or_the_same_file(home):
    _refused(home, "file is missing", lambda _s, dst: dst.unlink())
    _refused(home, "cannot be read", lambda _s, dst: dst.write_text("{oops", encoding="utf-8"))
    src_p, _dst = _pair(home)
    src = Board.load(src_p)
    assert move_plan(src, peek_board(src_p), "pmr", set(), set()).refusal == \
        "the target is this board"


def test_TC_2206_a_target_changed_after_the_plan(home):
    src_p, dst_p = _pair(home)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    dst_p.write_text(dst_p.read_text(encoding="utf-8") + " ", encoding="utf-8")
    before = _snap(home)
    with pytest.raises(OSError, match="changed since"):
        move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert _snap(home) == before


# --------------------------------------------------------------------------- #
# TC-2206 — the move (LLR-2206.1)
# --------------------------------------------------------------------------- #
def test_TC_2206_the_move(home):
    src_p, dst_p = _pair(home)
    img = _image(home, src_p)
    (src_p.parent / "history.jsonl").write_text(
        json.dumps({"task": "tw1", "to": "Doing"}) + "\n"
        + json.dumps({"task": "tr3", "to": "Doing"}) + "\nnot json\n"
        + json.dumps({"task": "tw2", "to": "Next"}) + "\n", encoding="utf-8")
    _edit(src_p, lambda d: (next(p for p in d["projects"] if p["id"] == "pmr").update(
        present_rank=2), next(t for t in d["tasks"] if t["id"] == "tr6").update(
        archived=True)))
    old = {p: p.read_bytes() for p in (src_p, dst_p)}
    src, dst = Board.load(src_p), peek_board(dst_p)
    live = json.dumps(Board._to_dict(src.projects[0]))
    plan = move_plan(src, dst, "pmr", set(), set())
    new_src, steps = move_project(src, dst, "pmr", plan, DAY, ("Main", "Client · Retail RAG"))
    assert json.dumps(Board._to_dict(src.projects[0])) == live      # the live board untouched
    assert "pmr" not in {p.id for p in new_src.projects}
    for p in (src_p, dst_p):
        assert p.with_name(p.name + f".pre-move-{DAY}").read_bytes() == old[p]
    s, d = _deps(src_p), _deps(dst_p)
    assert not any(t.startswith("tr") for t in s) and s["tw2"] == []
    assert d["tr3"] == [] and d["tr4"] == ["tr3"] and d["tr5"] == ["tr4"] \
        and d["tr2"] == ["tr1"]
    dst_data = json.loads(dst_p.read_text(encoding="utf-8"))
    proj = next(p for p in dst_data["projects"] if p["id"] == "pmr")
    assert "present_rank" not in proj
    assert next(t for t in dst_data["tasks"] if t["id"] == "tr6")["archived"] is True
    tr3 = next(t for t in dst_data["tasks"] if t["id"] == "tr3")
    moved = dst_p.parent / "images" / "tr3" / "paste-001.png"
    assert moved.exists() and not img.parent.exists()
    assert tr3["images"] == [str(moved.parent.resolve() / "paste-001.png"), "relative.png",
                             str(home.parent / "else.png")]
    assert (src_p.parent / "history.jsonl").read_text(encoding="utf-8").splitlines() == [
        json.dumps({"task": "tw1", "to": "Doing"}), "not json",
        json.dumps({"task": "tw2", "to": "Next"})]
    assert (dst_p.parent / "history.jsonl").read_text(encoding="utf-8").splitlines() == [
        json.dumps({"task": "tr3", "to": "Doing"})]
    for folder in (src_p.parent, dst_p.parent):
        log = json.loads((folder / f"move-{DAY}.json").read_text(encoding="utf-8"))
        assert len(log) == 1 and log[0]["links_kept"] == 3 and log[0]["tasks"] == 7
        assert log[0]["links_dropped"] == [
            {"task": "Case study: retail RAG", "waits_on": "Pilot results deck"},
            {"task": "Demo env on Docker", "waits_on": "Compose template"}]
    assert steps[:2] == ["copied board.json", "copied board.json"]


def test_TC_2206_a_second_move_the_same_day(home):
    src_p, dst_p = _pair(home)
    (src_p.parent / f"move-{DAY}.json").write_text("{}", encoding="utf-8")
    for pid in ("pmr", "pma"):
        src, dst = Board.load(src_p), peek_board(dst_p)
        plan = move_plan(src, dst, pid, set(), set())
        move_project(src, dst, pid, plan, DAY, ("Main", "Client"))
    assert src_p.with_name(f"board.json.pre-move-{DAY}-2").exists()
    assert (src_p.parent / f"move-{DAY}.json").read_text(encoding="utf-8") == "{}"
    assert len(json.loads((src_p.parent / f"move-{DAY}-2.json").read_text(encoding="utf-8"))) == 2
    assert len(json.loads((dst_p.parent / f"move-{DAY}.json").read_text(encoding="utf-8"))) == 2


def test_TC_2206_the_target_save_failing_leaves_the_source(home, monkeypatch):
    """TC-2206 (architect A-20): the target is written first — when it fails, the
    source file and the live board still hold the project."""
    src_p, dst_p = _pair(home)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    old = src_p.read_bytes()
    real = Board.save_atomic

    def fail_dst(self):
        if self.path == dst_p:
            raise OSError("disk full")
        real(self)
    monkeypatch.setattr(Board, "save_atomic", fail_dst)
    with pytest.raises(OSError) as err:
        move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert src_p.read_bytes() == old and "pmr" in {p.id for p in src.projects}
    assert err.value.board is None and err.value.steps == ["copied board.json",
                                                         "copied board.json"]


def test_TC_2206_the_source_save_failing(home, monkeypatch):
    src_p, dst_p = _pair(home)
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    old = src_p.read_bytes()
    real = Board.save_atomic

    def fail_src(self):
        if self.path == src_p:
            raise OSError("locked")
        real(self)
    monkeypatch.setattr(Board, "save_atomic", fail_src)
    with pytest.raises(OSError) as err:
        move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert src_p.read_bytes() == old and err.value.board is None
    assert "pmr" in {p["id"] for p in json.loads(dst_p.read_text(encoding="utf-8"))["projects"]}


@pytest.mark.parametrize("step", ["images", "log"])
async def test_TC_2206_a_failure_after_the_source_save(home, monkeypatch, step):
    """TC-2206 (architect A-27): past the source save, the app adopts the new
    source — the project is not saved back into it by the next edit."""
    src_p, dst_p = _pair(home)
    _image(home, src_p)
    if step == "images":
        monkeypatch.setattr(boards.shutil, "copytree",
                            lambda *a, **k: (_ for _ in ()).throw(OSError("copy failed")))
    else:
        monkeypatch.setattr(boards, "_log", lambda *a, **k: (_ for _ in ()).throw(
            OSError("log failed")))
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        for k in ("escape", "P", "down", "m", "down", "enter", "enter"):
            await pilot.press(k)
            await pilot.pause()
        assert "pmr" not in {p.id for p in app.board.projects}
        assert any(n.title == "Boards" and "The move stopped" in n.message
                   for n in app._notifications)
        app.board.save()
    assert "pmr" not in {p["id"] for p in json.loads(src_p.read_text(
        encoding="utf-8"))["projects"]}


# --------------------------------------------------------------------------- #
# TC-2206 — the modals (LLR-2206.1)
# --------------------------------------------------------------------------- #
_SVG = re.compile(r'<text class="[^"]*" x="([\d.]+)" y="[\d.]+" textLength="[\d.]+" '
                  r'clip-path="url\(#[^)]*-line-(\d+)\)">([^<]*)</text>')


def _svg_rows(svg: str, width: int, height: int) -> list[str]:
    rows = [[" "] * width for _ in range(height)]
    for x, line, body in _SVG.findall(svg):
        y, col = int(line), round(float(x) / 12.2)
        if y >= height:
            continue
        for i, ch in enumerate(html.unescape(body).replace("\xa0", " ")):
            if col + i < width:
                rows[y][col + i] = ch
    return ["".join(r) for r in rows]


def _box(rows: list[str]) -> list[str]:
    """The confirmation box's inner rows: between its `╭`/`╰` border rows, inside
    its `│` sides."""
    top = next(i for i, r in enumerate(rows) if "╭" in r and "╮" in r and r.count("─") > 40)
    bot = next(i for i in range(top + 1, len(rows)) if "╰" in rows[i])
    left, right = rows[top].index("╭"), rows[top].index("╮")
    return [r[left + 1:right].rstrip() for r in rows[top + 1:bot]]


async def test_TC_2206_the_confirmation_is_the_rounds_box_and_the_undo_line(home):
    """TC-2206 (qa QA-16): the confirmation's box rows equal the round's
    `move-160-3-confirm.svg` box but for the added undo row."""
    _pair(home)
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        for k in ("escape", "P", "down", "m", "down", "enter"):
            await pilot.press(k)
            await pilot.pause()
        assert type(app.screen).__name__ == "MoveConfirm"
        got = _box(_svg_rows(app.export_screenshot(), 160, 45))
    want = _box(_svg_rows((ROUND / "move-160-3-confirm.svg").read_text(encoding="utf-8"),
                          160, 45))
    undo = "u cannot undo a move or the edits before it — the backups are the way back."
    assert [r.strip() for r in got].count(undo) == 1
    assert [r for r in got if r.strip() != undo] == want


async def test_TC_2206_many_crossing_links_keep_the_keys_on_screen(home):
    src_p, _dst = _pair(home)

    def more_links(d):
        others = [t["id"] for t in d["tasks"] if not t["id"].startswith("tr")][:6]
        next(t for t in d["tasks"] if t["id"] == "tr6")["depends_on"] = others
    _edit(src_p, more_links)
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        for k in ("escape", "P", "down", "m", "down", "enter"):
            await pilot.press(k)
            await pilot.pause()
        rows = _svg_rows(app.export_screenshot(), 80, 24)
        assert any("↵ move and drop 8 links" in r for r in rows), rows


async def test_TC_2206_markup_in_names_paints_literally(home):
    src_p, _dst = _pair(home)
    for payload in PAYLOADS:
        _edit(src_p, lambda d: (next(p for p in d["projects"] if p["id"] == "pmr").update(
            name=f"P{payload}"), next(t for t in d["tasks"] if t["id"] == "tw2").update(
            title=f"T{payload}")))
        from taskboard.__main__ import open_app
        app = open_app(None)
        async with app.run_test(size=(160, 45)) as pilot:
            await pilot.pause()
            for k in ("escape", "P", "down", "m"):
                await pilot.press(k)
                await pilot.pause()
            assert f"P{payload}" in app.screen.query_one("#mt-title").content.plain
            for k in ("down", "enter"):
                await pilot.press(k)
                await pilot.pause()
            text = app.screen.query_one("#mc-head").content
            links = app.screen.query_one("#mc-links-text").content
            assert f"P{payload}" in text.plain and f"T{payload}" in links.plain
            assert not any(getattr(s.style, "meta", None) for s in text.spans + links.spans)


async def test_TC_2206_refusal_notices_and_no_other_board(home):
    src_p, dst_p = _pair(home)
    _edit(dst_p, lambda d: d.update(phases=["Backlog", "Doing", "Done"]))
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        for k in ("escape", "P", "down", "m", "down", "enter"):
            await pilot.press(k)
            await pilot.pause()
        assert type(app.screen).__name__ == "ProjectPicker"
        assert any(n.message == "Retail RAG · pilot was not moved to Client · Retail RAG: the "
                   "target has no phase 'Next' — add it there first (f)." for n in app._notifications)
    reg = json.loads((home / "boards.json").read_text(encoding="utf-8"))
    for e in reg["boards"]:
        e["archived"] = e["id"] != "main"
    (home / "boards.json").write_text(json.dumps(reg), encoding="utf-8")
    app = open_app(None)
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        for k in ("P", "down", "m"):
            await pilot.press(k)
            await pilot.pause()
        assert any("no other board" in n.message for n in app._notifications)


# --------------------------------------------------------------------------- #
# AT-2206 — split the mixed board (HLR-2206)
# --------------------------------------------------------------------------- #
async def test_AT_2206_move_a_project_to_another_board(home):
    """AT-2206 (US-2204): `Retail RAG · pilot` moves from Main to Client · Retail RAG
    with its tasks, history and image; the crossing links are named, dropped and
    logged; both files are copied first."""
    src_p, dst_p = _pair(home)
    img = _image(home, src_p)
    (src_p.parent / "history.jsonl").write_text(
        json.dumps({"task": "tr3", "from": "Next", "to": "Doing", "at": "x"}) + "\n",
        encoding="utf-8")
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        for k in ("escape", "P", "down", "m"):
            await pilot.press(k)
            await pilot.pause()
        rows = app.screen.query_one("#mt-rows").content.plain.split("\n")
        assert [r[5:29].rstrip() for r in rows] == ["Personal", "Client · Retail RAG",
                                                    "Course · Docker"]
        for k in ("down", "enter"):
            await pilot.press(k)
            await pilot.pause()
        text = "\n".join(app.screen.query_one(f"#{i}").content.plain
                         for i in ("mc-head", "mc-links-text", "mc-foot"))
        for want in ("7 tasks move (5 open, 2 done) · 3 links inside the project stay",
                     "2 links cross the boards and will be dropped:", "Case study: retail RAG",
                     "Compose template", "u cannot undo a move", "↵ move and drop 2 links"):
            assert want in text, want
        app._undo_stack.append({"task_id": "tw1", "fields": {}})
        old = {p: p.read_bytes() for p in (src_p, dst_p)}
        await pilot.press("enter")
        await pilot.pause()
        listed = [o.prompt.plain if hasattr(o.prompt, "plain") else str(o.prompt)
                  for o in app.screen.query_one("#proj-list")._options]
        assert not any("Retail RAG · pilot" in x for x in listed), listed
        assert app._undo_stack == []           # the move is not undoable, and clears it
        assert any(n.message == "Moved Retail RAG · pilot to Client · Retail RAG · 7 tasks · "
                   "3 links kept · 2 dropped" for n in app._notifications)
    src = json.loads(src_p.read_text(encoding="utf-8"))
    dst = json.loads(dst_p.read_text(encoding="utf-8"))
    assert len(src["projects"]) == 4 and not any(t["project_id"] == "pmr" for t in src["tasks"])
    assert _deps(src_p)["tw2"] == []
    assert len(dst["projects"]) == 3
    assert len([t for t in dst["tasks"] if t["project_id"] == "pmr"]) == 7
    d = _deps(dst_p)
    assert d["tr3"] == [] and d["tr4"] == ["tr3"] and d["tr5"] == ["tr4"] \
        and d["tr2"] == ["tr1"]
    for p in (src_p, dst_p):
        assert p.with_name(f"board.json.pre-move-{DAY}").read_bytes() == old[p]
        log = json.loads((p.parent / f"move-{DAY}.json").read_text(encoding="utf-8"))
        assert len(log) == 1 and log[0]["links_kept"] == 3 and len(log[0]["links_dropped"]) == 2
    assert "tr3" in (dst_p.parent / "history.jsonl").read_text(encoding="utf-8")
    assert "tr3" not in (src_p.parent / "history.jsonl").read_text(encoding="utf-8")
    moved = dst_p.parent / "images" / "tr3" / "paste-001.png"
    assert moved.exists() and not img.parent.exists()
    tr3 = next(t for t in dst["tasks"] if t["id"] == "tr3")
    assert Path(tr3["images"][0]).resolve() == moved.resolve()


# --------------------------------------------------------------------------- #
# the reviews of increment 004 (code review F1-F6, security F1-F3)
# --------------------------------------------------------------------------- #
def test_TC_2206_two_boards_in_one_folder_are_refused(home):
    """TC-2206 (code review F1): `history.jsonl` and `images/` live beside the board
    file, so two boards in one folder share them — a move there is refused."""
    src_p, _dst = _pair(home)
    side = src_p.parent / "work.json"
    Board([], [], side, {"seen_view_renumber_2026_07": True}).save()
    (src_p.parent / "history.jsonl").write_text(
        json.dumps({"task": "tr3", "to": "Doing"}) + "\n", encoding="utf-8")
    before = _snap(home)
    plan = move_plan(Board.load(src_p), peek_board(side), "pmr", set(), set())
    assert plan.refusal == "the two boards share a folder (their history and images are one)"
    assert _snap(home) == before


def test_TC_2206_a_hard_linked_target_is_this_board(home):
    """TC-2206 (code review F5): a hard link to the source file is the same file."""
    src_p, _dst = _pair(home)
    linked = home / "boards" / "linked" / "board.json"
    linked.parent.mkdir(parents=True)
    try:
        os.link(src_p, linked)
    except OSError:
        pytest.skip("this file system makes no hard link")
    plan = move_plan(Board.load(src_p), peek_board(linked), "pmr", set(), set())
    assert plan.refusal == "the target is this board"


def test_TC_2206_a_bad_history_line_never_stops_the_handover(home):
    """TC-2206 (code review F2, security F2): undecodable bytes and odd records in
    the history are kept as they are; the moved lines move; nothing raises."""
    src_p, dst_p = _pair(home)
    hist = src_p.parent / "history.jsonl"
    hist.write_bytes(b'{"task": "tr3", "to": "Doing"}\n\xff\xfe junk\n{"task": ["tr3"]}\n'
                     + b"[" * 3000 + b"\n")
    (dst_p.parent / "history.jsonl").write_bytes(b'{"task": "tc1", "to": "Done"}')  # no newline
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    new_src, steps = move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert "moved the history lines" in steps
    lines = (dst_p.parent / "history.jsonl").read_text(encoding="utf-8").splitlines()
    assert lines == ['{"task": "tc1", "to": "Done"}', '{"task": "tr3", "to": "Doing"}']  # F6
    kept = hist.read_text(encoding="utf-8", errors="replace").splitlines()
    assert len(kept) == 3 and '{"task": ["tr3"]}' in kept


def test_TC_2206_an_unexpected_error_after_the_source_save_is_handed_over(home, monkeypatch):
    """TC-2206 (code review F2): a failure that is not an OSError past the source
    save still carries the new source, so the caller adopts it."""
    src_p, dst_p = _pair(home)
    monkeypatch.setattr(boards, "_log", lambda *a, **k: (_ for _ in ()).throw(
        TypeError("odd")))
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    with pytest.raises(OSError) as err:
        move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    assert err.value.board is not None and "pmr" not in {p.id for p in err.value.board.projects}


def test_TC_2206_a_linked_image_folder_stays_with_its_references(home):
    """TC-2206 (code review F3): an image folder that is a link to elsewhere does
    not move, and its references are not rewritten to a folder that would not exist."""
    src_p, dst_p = _pair(home)
    outside = home.parent / "elsewhere"
    outside.mkdir()
    (outside / "a.png").write_bytes(b"png")
    link = src_p.parent / "images" / "tr3"
    link.parent.mkdir(parents=True)
    try:
        os.symlink(outside, link, target_is_directory=True)
    except OSError:
        pytest.skip("this system makes no directory link")
    _edit(src_p, lambda d: next(t for t in d["tasks"] if t["id"] == "tr3").update(
        images=[str(link / "a.png")]))
    src, dst = Board.load(src_p), peek_board(dst_p)
    plan = move_plan(src, dst, "pmr", set(), set())
    move_project(src, dst, "pmr", plan, DAY, ("Main", "Client"))
    tr3 = next(t for t in json.loads(dst_p.read_text(encoding="utf-8"))["tasks"] if t["id"] == "tr3")
    assert tr3["images"] == [str(link / "a.png")]
    assert (outside / "a.png").exists() and not (dst_p.parent / "images" / "tr3").exists()


async def test_TC_2206_the_target_is_read_when_it_is_chosen(home):
    """TC-2206 (code review F4, security F1): a change to the target while the picker
    is open is seen — here an id that now clashes refuses the move."""
    src_p, dst_p = _pair(home)
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        for k in ("escape", "P", "down", "m"):
            await pilot.press(k)
            await pilot.pause()
        _edit(dst_p, lambda d: d["tasks"].append({"id": "tr1", "title": "Clash"}))
        for k in ("down", "enter"):
            await pilot.press(k)
            await pilot.pause()
        assert type(app.screen).__name__ == "ProjectPicker"
        assert any("already holds the id tr1" in n.message for n in app._notifications)
