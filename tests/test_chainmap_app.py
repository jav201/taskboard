"""The chain map's app layer (batch 2026-10-07-batch-02, increment 001).

HLR-801 / LLR-801.2 (AT-801) · HLR-802 / LLR-802.1 (AT-802) · HLR-803 /
LLR-803.1 (AT-803).

ATs drive `TaskboardApp` with real keys (C-16) over board files in `tmp_path`.
AT-801 runs on the FROZEN base board (the C-2b frame's own fixture, frozen on
`kg_board.TODAY`) so `shifted` reproduces the frames' fixed dates byte-exact on
any day. AT-802 runs on the milestones board (`kg_board.milestones(...)`), where
the `date.today()` argument is REQUIRED — it alone carries td0/td4/td5. AT-803
builds its crowded board in-test.

RED on the base tree: key `6` is unbound and `render_chainmap` does not exist.
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

import kg_board
from kg_board import TODAY
from taskboard import views
from taskboard.app import TaskboardApp
from taskboard.models import Task

RENUMBER = "seen_view_renumber_2026_07"


def _toasts(app):
    return [str(t.render()) for t in app.screen.query("Toast")]


def _painted(app) -> list[str]:
    return str(app.query_one("#board").render()).split("\n")


def _joined(app) -> str:
    return "\n".join(_painted(app))


def _due(b, tid: str) -> str:
    return b.task_by_id(tid).due_date


def _start(b, tid: str) -> str:
    return b.task_by_id(tid).start_date


def _plus(iso: str, n: int) -> str:
    return (date.fromisoformat(iso) + timedelta(days=n)).isoformat()


def _band(rows: list[str], name: str) -> str:
    return next(r for r in rows if f"─▌{name}" in r)


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def frozen(monkeypatch):
    """Freeze the calendar on the oracle board's TODAY (the house seam)."""
    import taskboard.app as app_mod
    from taskboard import models
    monkeypatch.setattr(views, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)
    monkeypatch.setattr(app_mod, "date", _Today)
    monkeypatch.setattr(kg_board, "date", _Today)


def _frozen_base(tmp_path):
    """The base board with Data Warehouse `together`, frozen (AT-801's own)."""
    path = tmp_path / "board.json"
    b = kg_board.shifted(path)
    b.project_by_id("pdwh").extra["date_links"] = "together"
    b.save()
    return path, b


def _milestones(tmp_path):
    """The milestones board, built at the real today (AT-802's own)."""
    path = tmp_path / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    b.save()
    return path, b


# --------------------------------------------------------------------------- #
# AT-801 — key 6 paints the C-2b rows; the arrows, ↵, and `x` walk the chains
# --------------------------------------------------------------------------- #
async def test_AT_801_key_6_paints_the_chain_map_and_x_unlinks(tmp_path, frozen):
    """AT-801 (LLR-801.2): `6` paints the chain map (the C-2b header, bands, the
    deviating `set here` band, the critical chain, the waits-on/unblocks strip);
    the arrows walk the chains; `↵` opens the shipped details; `x` on a linked
    task drops its incoming link and the frame re-renders; `x` on a task that
    waits on nothing refuses with the verbatim toast."""
    path, _b = _frozen_base(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("6")
        await pilot.pause()
        app.selected_task_id = "tm3"
        app.refresh_view()
        await pilot.pause()

        joined = _joined(app)
        assert "◆ CHAIN MAP · who waits on whom" in joined
        assert "15 linked tasks" in joined and "▲2 late" in joined and "━ chain 4" in joined
        assert "─▌Website Redesign" in joined
        assert "━ critical chain" in joined
        assert "set here" in joined and "● together" in joined, _band(_painted(app), "Data Warehouse")
        assert "◂ waits on" in joined and "Audit dependencies" in joined
        assert "▸ unblocks" in joined and "Offline sync" in joined

        # the arrows walk the chains in draw order (a real move, not a no-op)
        before = app.selected_task_id
        await pilot.press("down")
        await pilot.pause()
        assert app.selected_task_id is not None and app.selected_task_id != before

        # ↵ opens the shipped details
        from taskboard.modals import TaskDetails
        await pilot.press("enter")
        await pilot.pause()
        assert isinstance(app.screen, TaskDetails)
        await pilot.press("escape")
        await pilot.pause()

        # x on a linked task unlinks its incoming link; the frame re-renders
        app.selected_task_id = "tm3"
        app.refresh_view()
        await pilot.pause()
        assert app.board.task_by_id("tm3").depends_on == ["tm2"]
        before_rows = _painted(app)
        await pilot.press("x")
        await pilot.pause()
        assert app.board.task_by_id("tm3").depends_on == []
        assert _painted(app) != before_rows, "the frame re-rendered shorter"

        # x on a task that waits on nothing refuses verbatim
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.pause()
        app.clear_notifications()
        await pilot.pause()
        await pilot.press("x")
        await pilot.pause()
        said = "\n".join(_toasts(app))
        assert "nothing to remove — the selection waits on no task" in said, said


# --------------------------------------------------------------------------- #
# AT-802 — the per-chain rule: the switch cycles, the stored write, the bumps
# --------------------------------------------------------------------------- #
async def test_AT_802_the_rule_switch_cycles_and_bumps_follow_it(tmp_path):
    """AT-802 (LLR-802.1): the band shows `● push` by default; `m` on the chain
    map cycles Data Warehouse push→together→stay→push writing the STORED string
    (`push_delta`/`together`/`flag`) and marking `set here` while it deviates;
    under `together` a `+` bump on td4 moves td0 and td5 keeping their gaps;
    under `stay` the same bump moves nothing else."""
    path, _b = _milestones(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("6")
        await pilot.pause()
        app.selected_task_id = "td4"
        app.refresh_view()
        await pilot.pause()

        band = _band(_painted(app), "Data Warehouse")
        assert "● push" in band and "set here" not in band, band

        # m -> together
        await pilot.press("m")
        await pilot.pause()
        assert app.board.project_by_id("pdwh").extra["date_links"] == "together"
        band = _band(_painted(app), "Data Warehouse")
        assert "set here" in band and "● together" in band, band
        assert "Move the whole chain" in _joined(app)
        assert "a move shifts every later task by the same days" in _joined(app)

        # under together: td4, td0 AND td5 move +1d keeping their gaps
        d4, d0s, d0d, d5 = _due(app.board, "td4"), _start(app.board, "td0"), \
            _due(app.board, "td0"), _due(app.board, "td5")
        await pilot.press("+")
        await pilot.pause()
        assert _due(app.board, "td4") == _plus(d4, 1)
        assert _start(app.board, "td0") == _plus(d0s, 1)
        assert _due(app.board, "td0") == _plus(d0d, 1)
        assert _due(app.board, "td5") == _plus(d5, 1)

        # m -> stay; the same bump moves nothing else
        await pilot.press("m")
        await pilot.pause()
        assert app.board.project_by_id("pdwh").extra["date_links"] == "flag"
        assert "● stay" in _band(_painted(app), "Data Warehouse")
        d4, d0s, d0d, d5 = _due(app.board, "td4"), _start(app.board, "td0"), \
            _due(app.board, "td0"), _due(app.board, "td5")
        await pilot.press("+")
        await pilot.pause()
        assert _due(app.board, "td4") == _plus(d4, 1)
        assert _start(app.board, "td0") == d0s and _due(app.board, "td0") == d0d
        assert _due(app.board, "td5") == d5

        # m -> push: back to the stored default, the marker clears
        await pilot.press("m")
        await pilot.pause()
        assert app.board.project_by_id("pdwh").extra["date_links"] == "push_delta"
        band = _band(_painted(app), "Data Warehouse")
        assert "● push" in band and "set here" not in band, band

    # the junk arm: a hand-edited `date_links: 5` loads as push_delta, never raises
    path3 = tmp_path / "board3.json"
    b3 = kg_board.milestones(kg_board.shifted(path3), date.today())
    b3.save()
    raw = json.loads(path3.read_text(encoding="utf-8"))
    for p in raw["projects"]:
        if p["id"] == "pdwh":
            p["date_links"] = 5
    path3.write_text(json.dumps(raw), encoding="utf-8")

    app3 = TaskboardApp(board_path=str(path3), team_sync_interval=1e9)
    async with app3.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("6")
        await pilot.pause()
        band = _band(_painted(app3), "Data Warehouse")
        assert "● push" in band, band
        app3.selected_task_id = "td4"
        app3.refresh_view()
        await pilot.pause()
        d4, d0d, d5 = _due(app3.board, "td4"), _due(app3.board, "td0"), \
            _due(app3.board, "td5")
        await pilot.press("+")
        await pilot.pause()
        assert _due(app3.board, "td4") == _plus(d4, 1)
        assert _due(app3.board, "td0") == _plus(d0d, 1), "junk behaves as push_delta"
        assert _due(app3.board, "td5") == d5
        assert app3.board.project_by_id("pdwh").extra["date_links"] == 5


# --------------------------------------------------------------------------- #
# AT-803 — the shipped high-band cap, pinned (no renderer change owed)
# --------------------------------------------------------------------------- #
def _crowd(path: Path):
    """The kg base with more open highs in Backlog than fit: 8 extra high tasks
    beside the board's own Backlog highs (the cap's shown count differs by
    panel height, so the overflow strings differ by size)."""
    b = kg_board.shifted(path)
    for i in range(8):
        b.tasks.append(Task(f"Crowd high {i}", project_id="pweb", phase="Backlog",
                            priority="high", id=f"ch{i}"))
    b.settings[RENUMBER] = True
    b.save()
    return b


async def test_AT_803_the_shipped_high_band_cap(tmp_path):
    """AT-803 (LLR-803.1): on a Backlog with more open highs than fit the band
    carries `+7 more ↓` at 118x30 and `+8 more ↓` at 80x24 (N exact — the cap
    names what fits and counts the rest); the all-fits base board caps nothing
    (the negative control)."""
    path = tmp_path / "crowd.json"
    _crowd(path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        assert "+7 more ↓" in _joined(app)

    path2 = tmp_path / "crowd2.json"
    _crowd(path2)
    app2 = TaskboardApp(board_path=str(path2), team_sync_interval=1e9)
    async with app2.run_test(size=(80, 24)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        assert "+8 more ↓" in _joined(app2)

    path3 = tmp_path / "base.json"
    base = kg_board.shifted(path3)
    base.settings[RENUMBER] = True
    base.save()
    app3 = TaskboardApp(board_path=str(path3), team_sync_interval=1e9)
    async with app3.run_test(size=(118, 30)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        assert "more ↓" not in _joined(app3), "an all-fits band caps nothing"


async def test_AT_801b_L_opens_the_shipped_picker_on_the_chain_map(tmp_path):
    """AT-801 arm (code review CM-3): `L` on the chain map opens the shipped
    LinkPicker (LLR-801.2 names it in AT-801's threshold) and linking re-renders
    the map with the new chain."""
    path = tmp_path / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), date.today())
    b.settings["seen_view_renumber_2026_07"] = True
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("6")
        await pilot.pause()
        app.selected_task_id = "to5"          # Pen-test findings: no links yet
        app.refresh_view()
        await pilot.press("L")
        await pilot.pause()
        from taskboard.modals import LinkPicker
        assert isinstance(app.screen, LinkPicker), f"L opened {type(app.screen).__name__}"
        await pilot.press("escape")
        await pilot.pause()
