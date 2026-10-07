"""The cleanup batch's pins (batch 2026-10-07-batch-03, HLR-901/902/903).

Three loose items, each a shipped-law fix the reviews filed:

  * S-4 (LLR-901.1): `run_link_migration`'s failure path restores the board and
    the migration mark FIRST, then removes its own backup/log best-effort in a
    nested guard that never raises, and surfaces the ORIGINAL failure through
    `result.error` (the offer's error-as-data convention). A refusing `unlink`
    can neither mask the original error nor leave the board/mark unrestored.
  * S-9 (LLR-902.1): `Task.from_dict` coerces a present-but-non-text title at the
    load boundary — `str(value)` for scalars (`5` -> "5", `true` -> "True"),
    the shipped `Untitled` for containers (list/dict) and null — so one bad field
    never crashes a render. A MISSING key stays the shipped `Untitled`.
  * K2-1/D-623/UX2-2/milestones-in-views (LLR-903.1): the kanban `?` legend names
    `◆` only for bands the screen DRAWS; a milestones-only project keeps its
    rule-only band (D-623); a late milestone below the fold marks the fold row
    (UX2-2); milestones read as milestones in lanes/agenda/focus.

Increment 001 shipped S-4/S-9 and K2-1's search-filter half; the render items
(AT-903 arm 1's fold half, arms 2-4) land in increment 002, so those nodes are
RED here by design — the increment-002 counterfactual, captured in the run log.
Boards are synthetic (`tests/kg_board.py`) in `tmp_path`; no user data is touched.
"""
from __future__ import annotations

import errno
import json
import os
import re
from datetime import date, timedelta
from pathlib import Path

import pytest

import kg_board
from taskboard.app import TaskboardApp
from taskboard.keymap import VIEWS
from taskboard.models import (MIGRATION_BACKUP, MIGRATION_LOG, Board, Project, Task,
                              links_marked, run_link_migration)
from taskboard.views import (legend_entries, render_kanban, render_view)

RENUMBER = "seen_view_renumber_2026_07"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _state(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {t["id"]: (t["blocked"], t["depends_on"]) for t in data["tasks"]}


def _painted(app) -> list[list[tuple[str, str | None]]]:
    """The compositor's frame: per row, the (char, colour) cells it painted."""
    strips = app.screen._compositor.render_strips(app.screen.size)
    out = []
    for s in strips:
        cells = []
        for seg in s:
            cells += [(ch, None) for ch in seg.text]
        out.append(cells)
    return out


def _text(rows) -> list[str]:
    return ["".join(ch for ch, _ in r) for r in rows]


def _ms_board(tmp_path, name="board.json", *, pin=None):
    """The shifted kg milestones board saved at `path` (the AT board)."""
    path = tmp_path / name
    b = kg_board.milestones(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    for tid in (pin or ()):
        b.task_by_id(tid).pinned = True
    b.save()
    return path, b


def _write_board(path: Path, tasks: list[dict], *, projects=None,
                 settings=None, phases=None) -> None:
    """A hand-built board file (one bad field at a time)."""
    path.write_text(json.dumps({
        "phases": phases or ["Backlog", "Doing", "Done"],
        "projects": projects or [{"id": "p1", "name": "P", "color": "sky"}],
        "tasks": tasks,
        "settings": (settings if settings is not None
                     else {"migrations": {"links": 1, "milestones": 1}}),
    }), encoding="utf-8")


def _refuse_cleanup(monkeypatch) -> None:
    """`Path.unlink` refuses ONLY the migration's own backup/log cleanup: every
    other unlink (the atomic save's temp file) goes through as shipped."""
    real_unlink = Path.unlink

    def refusing_unlink(self, missing_ok=False):
        if MIGRATION_BACKUP in self.name or MIGRATION_LOG in self.name:
            raise PermissionError(errno.EACCES, "cleanup refused", str(self))
        return real_unlink(self, missing_ok=missing_ok)

    monkeypatch.setattr(Path, "unlink", refusing_unlink)


def _fail_save(monkeypatch, message="the original save refused") -> None:
    """`os.replace` fails: the original failure the migration must surface."""
    def failing_replace(src, dst):
        raise PermissionError(errno.EACCES, message, str(dst))

    monkeypatch.setattr(os, "replace", failing_replace)


# --------------------------------------------------------------------------- #
# TC-901 — restore-first, cleanup best-effort, the original error survives
# (LLR-901.1)
# --------------------------------------------------------------------------- #
def test_TC_901_the_failed_migration_restores_first_and_surfaces_the_original_error(
        tmp_path, monkeypatch):
    """TC-901 (LLR-901.1): a migration whose save fails AND whose post-write
    cleanup hits a refusing `unlink` leaves the board bytes and the mark as they
    were, `result.error` naming the ORIGINAL failure, and no exception escaping
    the cleanup. RED (cleanup-before-restore): the refusing unlink raises before
    the board/mark are restored, so the board is left converted, unmarked, and
    the original error is replaced or the exception escapes."""
    path = tmp_path / "board.json"
    kg_board.legacy(path)
    raw = path.read_bytes()
    loaded = Board.load(path)
    before = {t.id: (t.blocked, list(t.depends_on)) for t in loaded.tasks}
    _refuse_cleanup(monkeypatch)
    _fail_save(monkeypatch)
    result = run_link_migration(loaded)
    assert result is not None
    assert result.error and "the original save refused" in result.error, result.error
    assert "cleanup refused" not in result.error, "the cleanup masked the original"
    assert path.read_bytes() == raw, "the board file must be untouched"
    assert {t.id: (t.blocked, list(t.depends_on)) for t in loaded.tasks} == before
    assert "migrations" not in loaded.settings, "the mark must be restored"
    reloaded = Board.load(path)
    assert not links_marked(reloaded.settings)
    assert {t.id: (t.blocked, list(t.depends_on)) for t in reloaded.tasks} == before
    # the cleanup ran best-effort and was refused: this run's own files survive
    assert (tmp_path / (path.name + MIGRATION_BACKUP)).exists()
    assert (tmp_path / (path.name + MIGRATION_LOG)).exists()

    # negative control: the happy path converts, cleans up, no error.
    monkeypatch.undo()
    happy = tmp_path / "happy.json"
    kg_board.legacy(happy)
    result2 = run_link_migration(Board.load(happy))
    assert result2 is not None and result2.error is None
    assert result2.backup and result2.log
    assert links_marked(Board.load(happy).settings)
    assert _state(happy)["L2"] == (False, ["to2"])


# --------------------------------------------------------------------------- #
# TC-902 — a non-text title never crashes (LLR-902.1)
# --------------------------------------------------------------------------- #
TITLE_CASES = [(5, "5"), (["x"], "Untitled"), ({"a": 1}, "Untitled"),
               (None, "Untitled"), (True, "True")]


@pytest.mark.parametrize("raw, want", TITLE_CASES,
                         ids=["int", "list", "dict", "null", "bool"])
async def test_TC_902_a_non_text_title_coerces_at_the_boundary(tmp_path, raw, want):
    """TC-902 (LLR-902.1): a present-but-non-text title loads safely — scalars
    keep the user's text (`5` -> "5", `true` -> "True"), containers and null read
    the shipped `Untitled` — a MISSING key stays `Untitled`, the coerced strings
    survive a save, and every view renders without raising (the `5` board is
    driven through the app at 118x30). RED: a list/dict reaching a string-only
    render path, or a repr shipped as a title."""
    path = tmp_path / "board.json"
    _write_board(path, [
        {"id": "t1", "title": raw, "project_id": "p1", "phase": "Doing"},
        {"id": "t2", "project_id": "p1", "phase": "Doing"},     # MISSING key
    ])
    b = Board.load(path)
    titles = {t.id: t.title for t in b.tasks}
    assert titles["t1"] == want, titles
    assert titles["t2"] == "Untitled", "a missing key keeps the shipped fallback"
    assert all(isinstance(t.title, str) for t in b.tasks), "every title is text post-load"
    b.save()
    assert {t.id: t.title for t in Board.load(path).tasks} == titles, "coerced strings round-trip"
    for mode in VIEWS:
        render_view(mode, b, False, None, date.today(), width=118, height=30)

    if raw == 5:
        app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
        async with app.run_test(size=(118, 30)) as pilot:
            await pilot.pause()
            for key in ("1", "2", "3", "4", "5"):
                await pilot.press(key)
                await pilot.pause()
        assert app.board.task_by_id("t1").title == "5"


# --------------------------------------------------------------------------- #
# AT-901 — the failed migration through the running app
# --------------------------------------------------------------------------- #
async def test_AT_901_a_migration_failure_at_startup_names_the_original_failure(
        tmp_path, monkeypatch, capsys):
    """AT-901 (US-901, HLR-901): starting on a legacy board whose migration fails
    (the save refuses AND the cleanup unlink refuses) stops the app naming the
    ORIGINAL failure, never the cleanup's; the board on disk is left unconverted
    (original links, no mark). RED (cleanup-before-restore): the cleanup error is
    named, or the app opens on a board it cannot trust."""
    path = tmp_path / "board.json"
    kg_board.legacy(path)
    raw = path.read_bytes()
    _refuse_cleanup(monkeypatch)
    _fail_save(monkeypatch)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.pause()
    assert app.return_code == 1
    message = " ".join(capsys.readouterr().err.split())     # what the user reads
    assert "Link migration stopped" in message, message
    assert "the original save refused" in message, message
    assert "cleanup refused" not in message, message
    assert path.read_bytes() == raw
    after = Board.load(path)
    assert not links_marked(after.settings)
    assert _state(path)["L2"] == (True, ["to1", "to2"])


# --------------------------------------------------------------------------- #
# AT-902 — the `5`-title board opens and shows it
# --------------------------------------------------------------------------- #
async def test_AT_902_the_five_title_board_opens(tmp_path):
    """AT-902 (US-902, HLR-902): a board file with `"title": 5` opens; the app
    runs and the task shows `5` (the coerced string), not a crash. RED: a
    string-only render path raising on the int title."""
    path = tmp_path / "board.json"
    _write_board(path, [{"id": "t1", "title": 5, "project_id": "p1", "phase": "Doing"}])
    b = Board.load(path)
    lm: dict = {}
    frame = render_view("kanban", b, False, "t1", date.today(), width=118, height=30,
                        line_map=lm).plain
    assert "t1" in lm
    assert "5" in frame.split("\n")[lm["t1"]]
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("4")
        await pilot.pause()
    assert app.board.task_by_id("t1").title == "5"


# --------------------------------------------------------------------------- #
# AT-903 — the render items (arm 1's fold half + arms 2-4 land in increment 002)
# --------------------------------------------------------------------------- #
def _folded_milestone_board(path: Path) -> Board:
    """Five projects whose cards fill the bands; only the LAST carries a
    milestone, so a short height folds the only milestone-bearing band away."""
    today = date.today()
    iso = lambda off: (today + timedelta(days=off)).isoformat()
    projects, tasks = [], []
    for i in range(5):
        projects.append(Project(f"Proj{i}", "sky", id=f"p{i}"))
        tasks.append(Task(f"work {i}", project_id=f"p{i}", phase="Doing",
                          due_date=iso(5), id=f"w{i}"))
    tasks.append(Task("the milestone", project_id="p4", phase="Doing",
                      start_date=iso(6), due_date=iso(6), milestone=True, id="m4"))
    b = Board(projects, tasks, path, {}, ["Backlog", "Doing", "Done"])
    b.save()
    return b


@pytest.mark.parametrize("arm", ["1_legend", "2_rule_only", "3_fold", "4_views"])
async def test_AT_903_the_render_items(tmp_path, arm):
    """AT-903 (US-903, HLR-903), one node per arm, each a painted-frame read:
    arm 1 the kanban `?` legend names `◆` on a band rule only for DRAWN bands
    (the search-filter half is GREEN; the fold half RED until increment 002);
    arm 2 (D-623) a milestones-only project draws its rule-only band carrying
    `◆`, its head reading `N open` (a project with no cards, no done, no
    milestones draws none) — RED; arm 3 (UX2-2) a late milestone below the fold
    marks the fold row `▾ N more · ▲1 ◆` — RED; arm 4 milestones read with `◆`
    in lanes/agenda/focus and the lanes `?` legend names it (CL-5) — RED."""
    today = date.today()
    if arm == "1_legend":
        # the search-filter half: through the app, a query hiding every band
        # removes the `◆` band-rule entry the legend would otherwise name.
        from taskboard.modals import HelpModal
        path, b = _ms_board(tmp_path)
        app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
        async with app.run_test(size=(118, 30)) as pilot:
            await pilot.press("4")
            await pilot.pause()
            await pilot.press("question_mark")
            await pilot.pause()
            modal = app.screen
            assert isinstance(modal, HelpModal)
            drawn = [m for _s, m in legend_entries(
                "kanban", modal._board, today, modal._dims[0], modal._dims[1])]
            assert "a milestone on its project's band rule" in drawn, \
                "a drawn band carrying a milestone must be named"
            await pilot.press("escape")
            await pilot.pause()
            app.search_query = "zzzz-no-such-title"
            app.refresh_view()
            await pilot.pause()
            await pilot.press("question_mark")
            await pilot.pause()
            modal = app.screen
            assert isinstance(modal, HelpModal)
            filtered = [m for _s, m in legend_entries(
                "kanban", modal._board, today, modal._dims[0], modal._dims[1])]
            assert "a milestone on its project's band rule" not in filtered, \
                "a filter that empties the bands must remove the legend entry"
        # the fold half: a folded-off milestone band must NOT be named (RED now)
        folded = _folded_milestone_board(tmp_path / "folded.json")
        rows = render_kanban(folded, False, None, today, 118, 15).plain.split("\n")
        assert not any(r.startswith("▐") and "◆" in r for r in rows), \
            "the milestone band is below the fold in this frame"
        entries = [m for _s, m in legend_entries("kanban", folded, today, 118, 15)]
        assert "a milestone on its project's band rule" not in entries, \
            "a folded-off band must not be named (K2-1 fold half, increment 002)"
    elif arm == "2_rule_only":
        p = Project("Solo", "sky", id="ps")
        d = (today + timedelta(days=3)).isoformat()
        ms = Task("only milestone", project_id="ps", phase="Backlog",
                  start_date=d, due_date=d, milestone=True, id="m1")
        b = Board([p], [ms], tmp_path / "solo.json", {}, ["Backlog", "Doing", "Done"])
        rows = render_kanban(b, False, None, today, 118, 30).plain.split("\n")
        solo = [r for r in rows if r.lstrip().startswith("▐ Solo")]
        assert solo, "D-623: a milestones-only project draws its rule-only band"
        assert "◆" in solo[0], "the rule-only band carries its milestone"
        assert "1 open" in solo[0], "the head reads N open, N = the milestones"
        empty = Project("Empty", "sky", id="pe")
        b2 = Board([empty], [], tmp_path / "empty.json", {}, ["Backlog", "Doing", "Done"])
        assert not any(r.lstrip().startswith("▐ Empty")
                       for r in render_kanban(b2, False, None, today, 118, 30).plain.split("\n"))
    elif arm == "3_fold":
        path, b = _ms_board(tmp_path)
        rows = render_kanban(b, False, None, today, 118, 24).plain.split("\n")
        assert not any(r.lstrip().startswith("▐ Ops") for r in rows), \
            "Ops & Security is below the fold in this frame"
        assert any(re.search(r"▼.*▲1 ◆", r) for r in rows), \
            "UX2-2: a late milestone below the fold marks the fold row"
    else:  # 4_views
        path, b = _ms_board(tmp_path, pin=("tw5",))
        app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
        async with app.run_test(size=(118, 40)) as pilot:
            await pilot.pause()
            for key, token, name in (("1", "Launch", "lanes"),
                                     ("2", "Partner", "agenda"),
                                     ("5", "Launch", "focus")):
                await pilot.press(key)
                await pilot.pause()
                rows = _text(_painted(app))
                hit = [r for r in rows if token in r]
                assert hit, (name, token, rows)
                assert any("◆" in r for r in hit), \
                    f"{name}: the milestone row carries its `◆` identity"
        entries = legend_entries("swimlanes", b, today, 118, 40)
        named = [(s, m) for s, m in entries if "milestone" in m]
        assert named and any("◆" in s for s, _m in named), \
            "CL-5: the lanes legend names the milestone `◆` when a lane draws one"
