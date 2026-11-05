"""Three quick hotfixes, each test encoding WHY it exists.

HF-1 (the operator's item 1): «No veo los keywords para apagar la cadena
principal» — `C` toggles the critical chain, on the gantt and the chain map,
remembered per board. HF-2 (item 2): «tuve que borrar y crear una nueva» — `O`
moves ONE task to another board through the project move's machinery. HF-3
(item 3): copy and paste in the notes and the capture pad — the pad had no
paste key at all and nothing ever wrote the OS clipboard.

Synthetic data only. RED before the fix, per test: HF-1 — no `chain_toggle`
action, no settings round-trip, no `chain off` legend; HF-2 — no
`task_move_plan`/`move_task` and no `task_move_board` action; HF-3 — the pad
bindings do not exist and the editor's `ctrl+c` reached only Textual's
app-local clipboard.
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

import multi_board_fixture as mb
from taskboard import app as app_module
from taskboard import boards, keymap, modals, views
from taskboard.app import TaskboardApp
from taskboard.boards import move_task, peek_board, task_move_plan
from taskboard.keymap import KEYMAP, bar_keys, key_bar_plain
from taskboard.models import Board, Project, Task
from taskboard.views import CRITICAL_REACH, render_chainmap, render_gantt, render_present

TODAY = date(2026, 11, 5)


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    return tmp_path / ".taskboard"


def _d(off):
    return (TODAY + timedelta(days=off)).isoformat()


def _chained_board(path: Path) -> Board:
    """One project, three open dated tasks in a chain t1 → t2 → t3: the board's
    critical chain is exactly those three, so the gantt draws the heavy reach."""
    proj = Project("Pilot", "sky", id="pr")
    tasks = [
        Task("Lay the groundwork", "pr", "Doing", "high", _d(-4), _d(2), id="t1"),
        Task("Build the middle", "pr", "Doing", "normal", _d(2), _d(6),
             depends_on=["t1"], id="t2"),
        Task("Close it out", "pr", "Next", "normal", _d(6), _d(9),
             depends_on=["t2"], id="t3"),
    ]
    return Board([proj], tasks, path, phases=["Backlog", "Next", "Doing", "Done"])


def _two_boards(root: Path):
    """Two boards in their OWN folders (the move's folders-must-differ guard),
    the source holding a task that carries everything."""
    src_dir, dst_dir = root / "src", root / "dst"
    src_dir.mkdir(parents=True)
    dst_dir.mkdir(parents=True)
    src = Board([Project("Client work", "sky", id="pc"),
                 Project("Ops", "lime", id="po")], [], src_dir / "board.json",
                phases=["Backlog", "Doing", "Done"])
    dst = Board([Project("Home & paperwork", "green", id="ph")], [],
                dst_dir / "board.json", phases=["Backlog", "Doing", "Done"])
    moving = Task("Ship the pilot", "pc", "Doing", "high", _d(-3), _d(4),
                  notes="::grn:: discuss with @ana.ruiz ::\nthe launch window",
                  images=[], depends_on=["stay2"], milestone=False,
                  mark="payment", created=_d(-10), id="mv1")
    stay2 = Task("The dependency that stays", "pc", "Doing", "normal", _d(-2), _d(3),
                 depends_on=["mv1"], id="stay2")
    src.tasks = [moving, stay2]
    src.save()
    dst.save()
    return src, dst


# --------------------------------------------------------------------------- #
# HF-1 — `C`: the critical chain off/on, remembered per board
# --------------------------------------------------------------------------- #
def test_HF1_the_setting_defaults_on_and_round_trips(tmp_path):
    """WHY: an existing board must render byte-identically — the default is on
    and a never-toggled file never carries the setting. RED: no chain_shown."""
    b = _chained_board(tmp_path / "board.json")
    assert "critical_chain" not in b.settings
    assert b.chain_shown() is True
    b.set_chain_shown(False)
    assert b.settings["critical_chain"] == "off"
    assert b.chain_shown() is False
    b.set_chain_shown(True)                 # on pops the key: the file stays clean
    assert "critical_chain" not in b.settings
    assert b.chain_shown() is True
    b.set_chain_shown(False)
    b.save()
    assert Board.load(b.path).chain_shown() is False   # survives the round-trip


def test_HF1_C_is_on_the_seat_where_the_chain_is_drawn():
    """WHY: discoverability was the defect — the key must sit on the bar of
    exactly the views that draw the chain. RED: no C on the seat."""
    c = next((k for k in KEYMAP if k.show == "C"), None)
    assert c is not None and c.action == "chain_toggle" and c.label == "Chain"
    assert c.views == ("gantt", "chainmap")
    assert "C" in key_bar_plain(160, "gantt", "primary")
    assert "C" in key_bar_plain(160, "chainmap", "more")
    assert "C" not in key_bar_plain(160, "swimlanes", "more")
    assert "C" not in key_bar_plain(160, "agenda", "more")
    # every key that works is shown: the binding comes from the seat
    assert any(b.action == "chain_toggle" for b in TaskboardApp.BINDINGS)


def test_HF1_off_takes_the_chain_out_of_every_drawing(tmp_path):
    """WHY: 'off' means no heavy structure and no critical styling, and the
    legend says `chain off · C` instead of listing the chain — on the gantt,
    the chain map and the presentation. The presentation's ruler echo also
    uses `━`, so there the proof is a styled-span check: no bar cell may wear
    the chain's heavy bright style. RED: the chain ignores the setting."""
    b = _chained_board(tmp_path / "board.json")
    on = render_gantt(b, False, None, TODAY, width=118, height=30).plain
    assert CRITICAL_REACH in on and "critical chain" in on
    present_on = render_present(b, "pr", None, TODAY, 118, 30)
    assert any(present_on.plain[s.start:s.end].startswith(CRITICAL_REACH)
               for s in present_on.spans if "bold" in str(s.style))
    b.set_chain_shown(False)
    off = render_gantt(b, False, None, TODAY, width=118, height=30).plain
    assert CRITICAL_REACH not in off
    assert "chain off · C" in off and "critical chain" not in off
    cm = render_chainmap(b, False, None, TODAY, width=118, height=30).plain
    assert "chain off · C" in cm and "critical chain" not in cm
    # the presentation's bars lose the heavy bright reach; the selected task's
    # ⟦━⟧ ruler echo is not the chain and stays
    present_off = render_present(b, "pr", None, TODAY, 118, 30)
    heavy = [s for s in present_off.spans
             if "bold" in str(s.style)
             and present_off.plain[s.start:s.end].startswith(CRITICAL_REACH)]
    assert heavy == []


async def test_AT_HF1_C_toggles_saves_toasts_and_shows_in_help(home):
    """WHY (black-box): the operator could not FIND the switch. `C` on the gantt
    flips the board's setting, says `Critical chain off · C turns it on`, the
    chart loses the heavy reach, and `?` names C on the gantt's key band."""
    mb.build(home, "main")
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("escape")          # off the home of boards
        await pilot.press("3")
        await pilot.pause()
        assert CRITICAL_REACH in render_gantt(app.board, False, None, TODAY,
                                              width=118, height=30).plain
        await pilot.press("C")
        await pilot.pause()
        assert app.board.settings["critical_chain"] == "off"
        assert any("Critical chain off · C turns it on" in str(n.message)
                   for n in app._notifications)
        assert CRITICAL_REACH not in render_gantt(app.board, False, None, TODAY,
                                                  width=118, height=30).plain
        await pilot.press("question_mark")
        await pilot.pause()
        band = app.screen.query_one("#help-keys", modals.Label).render()
        assert "C" in band.plain and "Chain" in band.plain
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("C")
        await pilot.pause()
        assert "critical_chain" not in app.board.settings
        assert any("Critical chain on · C turns it off" in str(n.message)
                   for n in app._notifications)


# --------------------------------------------------------------------------- #
# HF-2 — `O`: one task to another board
# --------------------------------------------------------------------------- #
def test_HF2_the_plan_lists_crossing_links_and_refuses_like_the_project_move(tmp_path):
    """WHY: the confirm and the log must say WHICH links die, and the guards are
    the project move's — a task shared in team mode refused among them. RED: no
    task_move_plan."""
    src, dst = _two_boards(tmp_path / "plan")
    plan = task_move_plan(src, dst, "mv1", set(), set())
    assert plan.refusal is None
    pairs = {(a.id, b.id) for a, b in plan.crossing}
    assert pairs == {("mv1", "stay2"), ("stay2", "mv1")}   # both directions
    same = task_move_plan(src, src, "mv1", set(), set())
    assert same.refusal == "the target is this board"
    sibling = Board([], [], tmp_path / "plan" / "src" / "board2.json")
    assert task_move_plan(src, sibling, "mv1", set(), set()).refusal.startswith(
        "the two boards share a folder")
    clash_dir = tmp_path / "plan" / "clash"
    clash_dir.mkdir()
    clash = Board([], [], clash_dir / "board.json", phases=["Backlog", "Doing", "Done"])
    clash.tasks = [Task("Already there", None, id="mv1")]
    clash.save()
    assert task_move_plan(src, clash, "mv1", set(), set()).refusal == \
        "the target already holds the id mv1"
    narrow_dir = tmp_path / "plan" / "narrow"
    narrow_dir.mkdir()
    narrow = Board([], [], narrow_dir / "board.json", phases=["Todo", "Done"])
    narrow.save()
    assert "no phase" in task_move_plan(src, narrow, "mv1", set(), set()).refusal
    assert task_move_plan(src, dst, "mv1", {"mv1"}, set()).refusal == \
        "the task is shared in team mode"


def test_HF2_move_task_carries_everything_and_drops_the_links(tmp_path):
    """WHY: the task arrives whole — notes with their colour spans and @mention,
    images moved under the target's images/, created, mark and dates — and its
    links to the source board's tasks are dropped exactly as a project move
    drops them, with the same backups, history move and log. RED: no move_task."""
    src, dst = _two_boards(tmp_path / "move")
    img = src.image_dir("mv1")
    img.mkdir(parents=True)
    (img / "paste-001.png").write_bytes(b"\x89PNG fake")
    src.tasks[0].images = [str(img / "paste-001.png")]
    src.save()
    dst.save()
    hist = src.path.parent / "history.jsonl"
    hist.write_text(json.dumps({"task": "mv1", "what": "phase"}) + "\n"
                    + json.dumps({"task": "stay2", "what": "phase"}) + "\n",
                    encoding="utf-8")
    plan = task_move_plan(src, dst, "mv1", set(), set())
    new_src, steps = move_task(src, dst, "mv1", "ph", plan, TODAY.isoformat(),
                               ("Main", "Personal"))
    # the source board the caller adopts no longer holds the task or the links
    assert new_src.task_by_id("mv1") is None
    assert new_src.task_by_id("stay2").depends_on == []
    # the target holds it whole, under the chosen project, images moved + re-pathed
    landed = Board.load(dst.path).task_by_id("mv1")
    assert landed is not None and landed.project_id == "ph"
    assert landed.notes == "::grn:: discuss with @ana.ruiz ::\nthe launch window"
    assert landed.mark == "payment" and landed.created == _d(-10)
    assert landed.start_date == _d(-3) and landed.due_date == _d(4)
    assert landed.depends_on == []               # the crossing links are dropped
    new_img = Path(landed.images[0])
    assert new_img == dst.image_dir("mv1") / "paste-001.png" and new_img.exists()
    assert not src.image_dir("mv1").exists()
    # backups beside both board files; the history line moved across
    day = TODAY.isoformat()
    assert (src.path.parent / f"board.json.pre-move-{day}").exists()
    assert (dst.path.parent / f"board.json.pre-move-{day}").exists()
    assert "mv1" not in hist.read_text(encoding="utf-8")
    assert '"task": "mv1"' in (dst.path.parent / "history.jsonl").read_text(encoding="utf-8")
    # the move log on BOTH sides lists the dropped links, like a project move
    entry = next(e for e in json.loads(
        (src.path.parent / f"move-{day}.json").read_text(encoding="utf-8"))
        if e.get("task") == "Ship the pilot")
    assert entry["from"] == "Main" and entry["to"] == "Personal"
    assert entry["project"] == "Home & paperwork"
    dropped = {(d["task"], d["waits_on"]) for d in entry["links_dropped"]}
    assert dropped == {("Ship the pilot", "The dependency that stays"),
                       ("The dependency that stays", "Ship the pilot")}
    assert "moved images/mv1" in steps


async def test_AT_HF2_O_moves_the_task_through_the_three_screens(home):
    """WHY (black-box): the operator deleted and recreated tasks to move them.
    `O` → board picker → target's project picker (Inbox is a choice) →
    MoveConfirm (`y`) — and the undo stack is cleared, as after a project move.
    The target board's FILE holds the task under the chosen project."""
    mb.build(home, "main")
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app.selected_task_id = "tr3"        # Demo env on Docker, in the tr3→tr4→tr5 chain
        await pilot.press("O")
        await pilot.pause()
        assert type(app.screen).__name__ == "MoveTarget"
        target_id = app.screen.targets[0].id
        await pilot.press("enter")           # that board
        await pilot.pause()
        assert type(app.screen).__name__ == "MoveProjectTarget"
        assert app.screen.rows[0][1] == "Inbox"    # the first row is a real choice
        await pilot.press("down", "enter")   # its first real project
        await pilot.pause()
        assert type(app.screen).__name__ == "MoveConfirm"
        await pilot.press("y")
        await pilot.pause()
        assert app.board.task_by_id("tr3") is None
        assert app.board.task_by_id("tr4").depends_on == []
        assert app._undo_stack == []         # the project move's undo behaviour
        assert any("Moved Demo env on Docker" in str(n.message) and "dropped" in str(n.message)
                   for n in app._notifications)
    entry = app.registry.get(target_id)
    landed = peek_board(entry.path).task_by_id("tr3")
    assert landed is not None
    assert landed.project_id is not None     # a real project, not the Inbox row


async def test_AT_HF2_a_team_shared_task_is_refused_with_the_reason(home, monkeypatch):
    """WHY: a task shared in team mode must not move, like a shared project —
    the refusal says so instead of moving half a collaboration."""
    mb.build(home, "main")
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        app.selected_task_id = "tr3"
        monkeypatch.setattr(TaskboardApp, "move_team_ids", staticmethod(lambda board: {"tr3"}))
        await pilot.press("O")
        await pilot.pause()
        assert type(app.screen).__name__ == "MoveTarget"
        await pilot.press("enter")
        await pilot.pause()
        assert type(app.screen).__name__ == "MoveProjectTarget"
        await pilot.press("enter")
        await pilot.pause()
        assert type(app.screen).__name__ != "MoveConfirm"
        assert app.board.task_by_id("tr3") is not None
        assert any("the task is shared in team mode" in str(n.message)
                   for n in app._notifications)


# --------------------------------------------------------------------------- #
# HF-3 — copy and paste, the OS clipboard, in the notes and the capture pad
# --------------------------------------------------------------------------- #
async def test_HF3_ctrl_v_pastes_the_os_clipboard_into_the_pad(home, monkeypatch):
    """WHY: the pad had NO paste binding — Textual's native paste reads the
    app-local clipboard, which starts empty, so ctrl+v never worked here."""
    import capture_fixture as fx
    fx.build_f(home)
    app = fx.open_f_app()
    monkeypatch.setattr(app_module, "grab_clipboard_text", lambda: "pasted from the os")
    async with app.run_test(size=(118, 30)) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app)
        pad = fx.pad_of(app)
        await pilot.press("ctrl+v")
        await pilot.pause()
        assert "pasted from the os" in pad.text


async def test_HF3_ctrl_c_copies_the_pad_selection_to_the_os(home, monkeypatch):
    """WHY: nothing ever wrote the OS clipboard — Textual's native copy is an
    OSC 52 escape Windows Terminal drops. The selection must reach the OS."""
    import capture_fixture as fx
    fx.build_f(home)
    app = fx.open_f_app()
    got = []
    monkeypatch.setattr(app_module, "stash_clipboard_text", lambda t: got.append(t) or True)
    async with app.run_test(size=(118, 30)) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app)
        pad = fx.pad_of(app)
        await fx.type_text(pilot, "copy me out")
        from textual.widgets.text_area import Selection
        pad.selection = Selection((0, 0), (0, 11))
        await pilot.press("ctrl+c")
        await pilot.pause()
        assert got == ["copy me out"]


async def test_HF3_the_editor_copies_the_selection_to_the_os(home, monkeypatch):
    """WHY: the notes are where the operator tried to copy from. `ctrl+c` on the
    editor now goes through the same OS-clipboard write as the pad."""
    mb.build(home, "main")
    from taskboard.__main__ import open_app
    app = open_app(None)
    got = []
    monkeypatch.setattr(modals, "stash_clipboard_text", lambda t: got.append(t) or True)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape", "e")
        await pilot.pause()
        assert type(app.screen).__name__ == "TaskModal"
        notes = app.screen.query_one("#f-notes")
        notes.focus()
        await pilot.press(*"copy me out")
        await pilot.pause()
        from textual.widgets.text_area import Selection
        notes.selection = Selection((0, 0), (0, 11))
        await pilot.pause()
        assert notes.selected_text == "copy me out"
        await pilot.press("ctrl+c")
        await pilot.pause()
        assert got == ["copy me out"]


async def test_HF3_the_editor_still_pastes(home, monkeypatch):
    """Regression: the notes' paste path (the OS clipboard read) is unchanged."""
    mb.build(home, "main")
    from taskboard.__main__ import open_app
    app = open_app(None)
    monkeypatch.setattr(modals, "grab_clipboard_text", lambda: "into the notes")
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape", "e")
        await pilot.pause()
        notes = app.screen.query_one("#f-notes")
        notes.focus()
        await pilot.press("ctrl+v")
        await pilot.pause()
        assert "into the notes" in notes.text


@pytest.mark.skipif(sys.platform != "win32", reason="the Win32 clipboard pair")
def test_HF3_stash_reaches_the_real_clipboard_and_restores_it():
    """WHY: the write must land where other apps read. The previous clipboard
    content is restored afterwards, so the test leaves the machine as it found
    it. Synthetic text only."""
    from taskboard.models import grab_clipboard_text, stash_clipboard_text
    before = grab_clipboard_text()
    try:
        assert stash_clipboard_text("taskboard hf3 synthetic round-trip")
        assert grab_clipboard_text() == "taskboard hf3 synthetic round-trip"
    finally:
        if before:
            stash_clipboard_text(before)   # the machine as it was found
