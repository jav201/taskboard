"""The per-task "show in presentation" flag (batch 2026-10-16-batch-01, increment 002).

HLR-1602 / LLR-1602.1, LLR-1602.2, LLR-1602.3 · TC-1603, TC-1604, TC-1605 · AT-1602 (US-1602).

Why these matter: a meeting should see only what belongs in it, and the presenter
should not have to edit the board for that — «Que se guarde en la tarea, una
bandera basta.» So the flag lives on the task in `board.json`, but a board with
nothing hidden must keep its exact bytes (every existing board, every team push);
`space` hides the cursor task and `a` brings every hidden one back, each saved at
once; and the hidden count rides the hint row ONLY — the frame is what the room
sees and what `x` exports.
RED on the base tree: `Task` has no flag, `space`/`a` do nothing in the presentation.
"""
from __future__ import annotations

import json
from datetime import date

import pytest

import present_board as pb
from taskboard import views
from taskboard.models import Board

TITLE = "Fix checkout 500 error"         # the oracle cursor task, `tw3`


class _Today(date):
    @classmethod
    def today(cls):
        return pb.TODAY


@pytest.fixture
def frozen(monkeypatch):
    """The house seam (`tests/test_present.py`): the screen and the startup
    sweep both read the frozen day."""
    from taskboard import app as app_module
    from taskboard import models

    monkeypatch.setattr(app_module, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)


def _saved(path):
    """The oracle board on disk, NORMALISED by one load + save first: loading
    snaps the fixture's `at_risk` project status (a pre-existing load rule,
    unrelated to the flag), so the byte laws start from a board that already
    round-trips."""
    pb.build(path).save()
    Board.load(path).save()
    return path


def _tasks(path) -> dict[str, dict]:
    return {t["id"]: t for t in json.loads(path.read_text(encoding="utf-8"))["tasks"]}


# --------------------------------------------------------------------------- #
# TC-1603 — the flag in the file: absent when shown, `false` when hidden
# --------------------------------------------------------------------------- #
def test_TC_1603_a_board_with_nothing_hidden_keeps_its_bytes(tmp_path):
    """TC-1603 (LLR-1602.1): load + save of a board with no hidden task is
    byte-identical, and no record carries the key — every existing board and
    every team push stays as it was."""
    path = _saved(tmp_path / "board.json")
    before = path.read_bytes()
    Board.load(path).save()
    assert path.read_bytes() == before
    assert b"show_in_present" not in before


def test_TC_1603_a_hidden_task_writes_false_and_nothing_else(tmp_path):
    """TC-1603 (LLR-1602.1): hiding one task adds `"show_in_present": false` to
    THAT record only; every other field of every record is unchanged; showing it
    again returns the file to its original bytes and leaves nothing in `extra`."""
    path = _saved(tmp_path / "board.json")
    before, original = path.read_bytes(), _tasks(path)
    b = Board.load(path)
    b.task_by_id("tw3").show_in_present = False
    b.save()
    after = _tasks(path)
    assert after["tw3"].pop("show_in_present") is False
    assert after == original
    b = Board.load(path)
    assert b.task_by_id("tw3").show_in_present is False
    b.task_by_id("tw3").show_in_present = True
    b.save()
    assert path.read_bytes() == before
    assert "show_in_present" not in Board.load(path).task_by_id("tw3").extra


@pytest.mark.parametrize("value", ["no", 0, None, True])
def test_TC_1603_only_json_false_hides(tmp_path, value):
    """TC-1603 (LLR-1602.1 invalid arm): a hand-edited `"no"`, `0` or `null`
    loads as SHOWN (only the JSON `false` hides), lands nowhere in `extra`, and
    is dropped on the next save — a declared byte change for that file only."""
    path = tmp_path / "board.json"
    pb.build(path).save()
    raw = json.loads(path.read_text(encoding="utf-8"))
    next(t for t in raw["tasks"] if t["id"] == "tw3")["show_in_present"] = value
    path.write_text(json.dumps(raw), encoding="utf-8")
    b = Board.load(path)
    task = b.task_by_id("tw3")
    assert task.show_in_present is True
    assert "show_in_present" not in task.extra
    b.save()
    assert "show_in_present" not in _tasks(path)["tw3"]


# --------------------------------------------------------------------------- #
# TC-1604 — the filter, the axis, the cursor, the writes, the hint
# --------------------------------------------------------------------------- #
def test_TC_1604_the_filter_and_the_axis_fit_the_shown_tasks(tmp_path):
    """TC-1604 (LLR-1602.2 a, b): a hidden task leaves `present_tasks` (open and
    all) and is listed by `present_hidden`; hiding `tw6`, the latest due (Oct 14,
    after the project's Oct 10), narrows the field's window."""
    b = pb.build(tmp_path / "board.json")
    proj = b.project_by_id(pb.PROJECT_ID)

    def last_day():
        open_t, _ = views.present_tasks(b, pb.PROJECT_ID)
        return views._present_axis(b, proj, open_t, 73, pb.TODAY).window_days()[-1]

    wide = last_day()
    b.task_by_id("tw6").show_in_present = False
    open_t, all_t = views.present_tasks(b, pb.PROJECT_ID)
    assert "tw6" not in {t.id for t in open_t} | {t.id for t in all_t}
    assert [t.id for t in views.present_hidden(b, pb.PROJECT_ID)] == ["tw6"]
    assert last_day() < wide


class _Presenting:
    """The app on the oracle board saved to disk, `R` pressed, saves counted
    (each still writes the file)."""

    def __init__(self, tmp_path, monkeypatch, size=(118, 31)):
        self.path = tmp_path / "board.json"
        if not self.path.exists():
            pb.build(self.path).save()
        self.saves = []
        real = Board.save

        def counted(board):
            self.saves.append(1)
            real(board)
        monkeypatch.setattr(Board, "save", counted)
        from taskboard.app import TaskboardApp
        self.app = TaskboardApp(board_path=str(self.path))
        self.size = size

    async def open(self, pilot):
        app = self.app
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                break
            await pilot.pause()
        app.selected_task_id = pb.CURSOR
        self.saves.clear()                    # what mounting wrote is not the presentation's
        await pilot.press("R")
        await pilot.pause()
        assert type(app.screen).__name__ == "PresentScreen"

    def frame(self) -> str:
        return _plain(self.app.screen.query_one("#present-frame"))

    def hint(self) -> str:
        return _plain(self.app.screen.query_one("#present-hint"))


def _plain(widget) -> str:
    content = widget.content
    return content.plain if hasattr(content, "plain") else str(content)


async def test_TC_1604_space_moves_the_cursor_and_the_ends_hold(tmp_path, monkeypatch, frozen):
    """TC-1604 (LLR-1602.2 c–i, k): `space` on `Fix checkout 500 error` hides it,
    saves once, and the cursor lands on the next task by due (`Optimize image
    assets`); hiding the LAST shown task moves the cursor up; with every task
    hidden the frame keeps header, ruler, span row and separator and paints
    nothing below them (no brief row; the keys live in the hint row,
    increment 004); `space` then writes nothing; `a` brings every task back
    (one save) with a cursor; `a` with nothing hidden writes nothing and never
    opens the app's add-task editor; the frame never says `hidden`."""
    s = _Presenting(tmp_path, monkeypatch)
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await pilot.press("space")
        await pilot.pause()
        assert len(s.saves) == 1
        assert TITLE not in s.frame()
        assert "⟦Optimize image assets⟧" in s.frame()
        assert "hidden" not in s.frame()

        for _ in range(3):
            await pilot.press("right")
        await pilot.pause()
        assert "⟦SEO redirects map⟧" in s.frame()
        await pilot.press("space")
        await pilot.pause()
        assert "⟦Launch new homepage⟧" in s.frame()

        for _ in range(3):
            await pilot.press("space")
            await pilot.pause()
        frame = s.frame().split("\n")
        assert len(s.saves) == 5
        assert "Website Redesign" in frame[0] and "today Wed Sep 30" in frame[1]
        assert "WEBSITE REDESIGN" in frame[3] and frame[4].startswith("────")
        assert frame[5].strip() == "", frame[5]
        assert "⟦" not in "\n".join(frame[4:]), "a brief row painted with every task hidden"

        await pilot.press("space")
        await pilot.pause()
        assert len(s.saves) == 5, "space with every task hidden wrote the board"

        await pilot.press("a")
        await pilot.pause()
        assert len(s.saves) == 6
        assert "⟦Build component library⟧" in s.frame()
        assert type(s.app.screen).__name__ == "PresentScreen", "`a` opened the editor"

        await pilot.press("a")
        await pilot.pause()
        assert len(s.saves) == 6, "`a` with nothing hidden wrote the board"
        assert type(s.app.screen).__name__ == "PresentScreen"


@pytest.mark.parametrize("size, hint, hint_hidden", [
    ((118, 31), "1 gantt  2 split  3 all  ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave",
     "1 gantt  2 split  3 all  ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave"),
    # batch 2026-10-20-batch-03 (law-driven, D-14): `? keys` ends every wording, 8 cells
    # off the room, so 80 columns take the short wording, and with a count the compact one
    ((80, 25), "1 gantt 2 split 3 all ⇥ · ←→ · ␣ hide · a all · x export · esc",
     "1 gantt 2 split 3 all ⇥ ←→ ␣ x esc"),
])
async def test_TC_1604_the_hint_row_carries_the_keys_and_the_count(
        tmp_path, monkeypatch, frozen, size, hint, hint_hidden):
    """TC-1604 (LLR-1602.2 j): the commission's hint texts, then ` · <n> hidden`
    with n the hidden tasks (none → no tail). Since batch 2026-10-18-batch-01
    (LLR-1802.2) the hint opens with the view switch and `tab` (R opens on the
    gantt view); at 80 columns `←→` drops its word so the split view's
    `pgdn` and a two-digit count still fit (tests/test_present_views.py). Since
    batch 2026-10-18-batch-03 (LLR-2002.1) 80 columns with nothing hidden take
    the middle wording; with two hidden the count leaves room only for the
    short one. Since batch 2026-10-19-batch-01 (LLR-2104.1) the hint names three
    views and the count reads `u <n> hidden` (`u` lists them)."""
    s = _Presenting(tmp_path, monkeypatch, size)
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        assert s.hint().strip() == hint + "  ? keys"
        await pilot.press("space")
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()
        assert s.hint().strip() == hint_hidden + " · u 2 hidden  ? keys"


# --------------------------------------------------------------------------- #
# TC-1605 — "Show in presentation" in the task editor
# --------------------------------------------------------------------------- #
async def test_TC_1605_the_editor_box_at_80x24(tmp_path, frozen):
    """TC-1605 (LLR-1602.3): at 80x24 `e` shows `Show in presentation` fully
    painted in the title row, checked; the title keeps >= 20 painted cells;
    `space` on the box unchecks it; Save writes the flag to the file; the chip
    row's measured threshold is unchanged (137)."""
    from textual.widgets import Checkbox

    from taskboard.app import TaskboardApp
    from taskboard.modals import TASK_CHIPS_ONE_ROW, TaskModal

    assert TASK_CHIPS_ONE_ROW == 137
    path = tmp_path / "board.json"
    pb.build(path).save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(80, 24)) as pilot:
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                await pilot.press("escape")
                break
            await pilot.pause()
        app.selected_task_id = pb.CURSOR
        await pilot.press("e")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        assert isinstance(scr, TaskModal)
        box = scr.query_one("#f-present", Checkbox)
        region, clip = scr._compositor.visible_widgets[box]
        assert region.area > 0 and region.intersection(clip) == region, "box clipped at 80"
        assert "Show in presentation" in str(box.label)
        assert box.value is True
        assert scr.query_one("#f-title").region.width >= 20
        box.focus()
        await pilot.press("space")
        await pilot.pause()
        assert box.value is False
        scr.query_one("#save").press()
        await pilot.pause()
    assert _tasks(path)["tw3"]["show_in_present"] is False


async def test_TC_1605_a_new_task_starts_shown(tmp_path):
    """TC-1605 (LLR-1602.3 boundary): the add editor starts checked, and saving
    it unchanged writes no key."""
    from textual.widgets import Checkbox, Input

    from taskboard.app import TaskboardApp
    from taskboard.modals import TaskModal

    path = tmp_path / "board.json"
    pb.build(path).save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 31)) as pilot:
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                await pilot.press("escape")
                break
            await pilot.pause()
        await pilot.press("a")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        assert isinstance(scr, TaskModal)
        assert scr.query_one("#f-present", Checkbox).value is True
        scr.query_one("#f-title", Input).value = "A brand new task"
        scr.query_one("#save").press()
        await pilot.pause()
    new = next(t for t in _tasks(path).values() if t["title"] == "A brand new task")
    assert "show_in_present" not in new


# --------------------------------------------------------------------------- #
# AT-1602 — hide, export, restart, show all: through the shipped surface
# --------------------------------------------------------------------------- #
async def test_AT_1602_space_hides_and_it_is_remembered_a_shows_all(tmp_path, frozen):
    """AT-1602 (US-1602, HLR-1602): on the oracle board saved to disk, `R`,
    `space` → the cursor task's title is gone from the painted frame, the hint
    row ends `· 1 hidden`, and `board.json` differs from before by that task's
    flag only; `x` → the exported SVG holds no `hidden`, not the hidden title,
    and the header says `4 open`; restart the app, `R` → still hidden; `a` → the
    title is back and the file equals its original bytes."""
    from taskboard.app import TaskboardApp

    path = _saved(tmp_path / "board.json")

    async def present(app, pilot):
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                break
            await pilot.pause()
        app.selected_task_id = pb.CURSOR
        await pilot.press("R")
        await pilot.pause()
        return app.screen

    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 31)) as pilot:
        scr = await present(app, pilot)
        before, original = path.read_bytes(), _tasks(path)
        assert TITLE in _plain(scr.query_one("#present-frame"))
        await pilot.press("space")
        await pilot.pause()
        assert TITLE not in _plain(scr.query_one("#present-frame"))
        assert _plain(scr.query_one("#present-hint")).rstrip().endswith("· u 1 hidden  ? keys")
        after = _tasks(path)
        assert after["tw3"].pop("show_in_present") is False
        assert after == original

        await pilot.press("x")
        await pilot.pause()
        svgs = list((tmp_path / "reports").glob("present-*.svg"))
        assert len(svgs) == 1, svgs
        svg = svgs[0].read_text(encoding="utf-8").replace("&#160;", " ")
        assert "hidden" not in svg
        assert "checkout" not in svg
        assert "4 open" in svg

    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 31)) as pilot:
        scr = await present(app, pilot)
        assert TITLE not in _plain(scr.query_one("#present-frame"))
        await pilot.press("a")
        await pilot.pause()
        assert TITLE in _plain(scr.query_one("#present-frame"))
    assert path.read_bytes() == before
