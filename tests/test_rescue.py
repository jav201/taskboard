"""Task/board rescue: a drifted or corrupt entry must never empty the board or
lose a user's content. These tests encode WHY the rescue exists — a single bad
task once blanked the whole board (list-comprehension load), and a schema change
must never silently drop work."""
from __future__ import annotations

import json

from taskboard.models import Board, Task, Project


def _write(tmp_path, data):
    p = tmp_path / "board.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def test_one_bad_task_never_empties_the_board(tmp_path):
    """THE bug: with a list-comprehension load, one non-object task entry raised
    and returned an EMPTY board. Now the good tasks survive and the bad one is
    rescued, so 3 entries -> 3 tasks (2 real + 1 recovered)."""
    data = {"phases": ["Backlog", "Doing", "Done"], "projects": [], "tasks": [
        {"id": "a", "title": "real one", "phase": "Doing"},
        "i am not an object",                         # garbage entry
        {"id": "b", "title": "another", "phase": "Backlog"},
    ]}
    board = Board.load(_write(tmp_path, data))
    assert len(board.tasks) == 3                       # nothing dropped
    titles = [t.title for t in board.tasks]
    assert "real one" in titles and "another" in titles
    assert board.load_report["tasks_rescued"] == 1


def test_rescued_task_preserves_original_content(tmp_path):
    data = {"tasks": ["orphaned free text that must survive"], "projects": []}
    board = Board.load(_write(tmp_path, data))
    rescued = board.tasks[0]
    assert rescued.extra.get("_rescued") is True
    assert "orphaned free text that must survive" in rescued.notes  # content kept
    assert rescued.title.startswith("(recovered)")


def test_various_garbage_entries_all_rescued(tmp_path):
    data = {"tasks": [None, 42, ["nested", "list"], {"no": "title"}], "projects": []}
    board = Board.load(_write(tmp_path, data))
    assert len(board.tasks) == 4                       # every entry kept
    # the dict-without-title is valid (title defaults to "Untitled"), not a rescue;
    # the three non-objects are rescued.
    assert board.load_report["tasks_rescued"] == 3


def test_rescued_task_roundtrips_through_save(tmp_path):
    """A rescued task must survive save+reload, so re-saving the board can never
    be the thing that finally loses the drifted content."""
    p = _write(tmp_path, {"tasks": ["salvage me"], "projects": []})
    board = Board.load(p)
    board.save()                                       # app would do this on any edit
    reloaded = Board.load(p)
    assert len(reloaded.tasks) == 1
    assert "salvage me" in reloaded.tasks[0].notes


def test_from_dict_is_total_never_raises():
    for junk in (None, 7, "text", ["a"], 3.14):
        t = Task.from_dict(junk)
        assert isinstance(t, Task) and t.extra.get("_rescued") is True


def test_bad_project_does_not_empty_projects(tmp_path):
    data = {"projects": [{"id": "p1", "name": "Good", "color": "amber"}, 123],
            "tasks": []}
    board = Board.load(_write(tmp_path, data))
    assert len(board.projects) == 2
    assert any(pr.name == "Good" for pr in board.projects)
    assert board.load_report["projects_rescued"] == 1


def test_corrupt_json_is_quarantined_and_original_untouched(tmp_path):
    p = tmp_path / "board.json"
    p.write_text("{ this is : not json ,,,", encoding="utf-8")   # invalid JSON
    original = p.read_text(encoding="utf-8")
    board = Board.load(p)
    assert board.tasks == [] and board.projects == []            # empty, not crashed
    assert board.load_report["file_unreadable"] is True
    backup = p.with_name(p.name + ".corrupt")
    assert backup.exists()                                       # bytes preserved
    assert backup.read_text(encoding="utf-8") == original
    assert p.read_text(encoding="utf-8") == original             # original untouched


def test_top_level_not_an_object_is_quarantined(tmp_path):
    p = tmp_path / "board.json"
    p.write_text(json.dumps(["a", "list", "not", "a", "board"]), encoding="utf-8")
    board = Board.load(p)
    assert board.tasks == []
    assert board.load_report["file_unreadable"] is True
    assert p.with_name(p.name + ".corrupt").exists()


def test_quarantine_does_not_clobber_existing_backup(tmp_path):
    p = tmp_path / "board.json"
    backup = p.with_name(p.name + ".corrupt")
    backup.write_text("FIRST corruption I want to keep", encoding="utf-8")
    p.write_text("also broken )))", encoding="utf-8")
    Board.load(p)
    assert backup.read_text(encoding="utf-8") == "FIRST corruption I want to keep"


def test_clean_board_reports_no_rescues(tmp_path):
    data = {"phases": ["Backlog", "Doing", "Done"], "projects": [],
            "tasks": [{"id": "a", "title": "fine", "phase": "Doing"}]}
    board = Board.load(_write(tmp_path, data))
    r = board.load_report
    assert r["tasks_rescued"] == 0 and r["projects_rescued"] == 0
    assert r["file_unreadable"] is False


async def test_app_notifies_when_tasks_are_rescued(tmp_path):
    """The user must be TOLD when a load recovered drifted data — a silent
    rescue would leave recovered tasks unnoticed in their notes."""
    from taskboard.app import TaskboardApp
    p = tmp_path / "board.json"
    p.write_text(json.dumps({"tasks": ["garbage entry"], "projects": []}), encoding="utf-8")
    app = TaskboardApp(board_path=str(p))
    calls = []
    app.notify = lambda *a, **k: calls.append((a, k))     # capture before mount
    async with app.run_test():
        pass
    assert app.board.load_report["tasks_rescued"] == 1
    assert any("recovered" in str(k.get("title", "")).lower() for _, k in calls)
