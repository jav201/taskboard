"""Present view 3 `all` — every shown project on one ruler beside a curate rail.

Batch 2026-10-19-batch-01 (variant C of the present-portfolio round):
HLR-2102..HLR-2106 / LLR-2102.1..LLR-2106.1 · TC-2102..TC-2106 · AT-2102..AT-2106
(US-2102..US-2104). Synthetic data only: the round's board
(`tests/present_portfolio_board.py`).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import present_board as pb
import present_portfolio_board as pf
from taskboard import models
from taskboard.models import Board, Project


# --------------------------------------------------------------------------- #
# TC-2102 — the project's presentation state on the board (increment 002)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("raw, shown", [
    (False, False), ("<absent>", True), (True, True), (0, True), ("false", True), (None, True)])
def test_TC_2102_show_in_present_is_false_only_for_the_json_false(raw, shown):
    """TC-2102 (LLR-2102.1): a project leaves view 3 only on the JSON `false` —
    a hand-edited `0` or `"false"` must not hide a project the presenter never hid."""
    d = {"id": "p1", "name": "P"}
    if raw != "<absent>":
        d["show_in_present"] = raw
    p = Project.from_dict(d)
    assert p.show_in_present is shown
    assert "show_in_present" not in p.extra


@pytest.mark.parametrize("raw, rank", [
    (0, 0), (3, 3), (-3, -3), (10 ** 300, 10 ** 300), ("<absent>", None), (None, None),
    (True, None), (False, None), ("2", None), (2.5, None), (1.0, None), ([], None)])
def test_TC_2102_present_rank_is_kept_only_as_an_integer(raw, rank):
    """TC-2102 (LLR-2102.1; security S-3): only a non-boolean integer is a place —
    `true` is not place 1, and no value makes the order's sort raise."""
    d = {"id": "p1", "name": "P"}
    if raw != "<absent>":
        d["present_rank"] = raw
    p = Project.from_dict(d)
    assert p.present_rank == rank and type(p.present_rank) is type(rank)
    assert "present_rank" not in p.extra


def _records(path: Path) -> dict[str, dict]:
    return {p["id"]: p for p in json.loads(path.read_text(encoding="utf-8"))["projects"]}


def test_TC_2102_the_keys_are_written_only_off_their_default(tmp_path):
    """TC-2102 (LLR-2102.1): a default project writes neither key — every existing
    board keeps its bytes — a hidden one `false`, a ranked one its integer."""
    path = tmp_path / "b.json"
    b = pf.build(path)
    for p in b.projects:
        p.show_in_present = True
    b.save()
    assert not any(k in r for r in _records(path).values()
                   for k in ("show_in_present", "present_rank"))
    before = path.read_bytes()
    Board.load(path).save()
    assert path.read_bytes() == before
    b = Board.load(path)
    b.project_by_id("pbm").show_in_present = False
    b.project_by_id("pcp").present_rank = 0
    b.save()
    recs = _records(path)
    assert recs["pbm"]["show_in_present"] is False and "present_rank" not in recs["pbm"]
    assert recs["pcp"]["present_rank"] == 0 and "show_in_present" not in recs["pcp"]
    back = Board.load(path)
    assert back.project_by_id("pbm").show_in_present is False
    assert back.project_by_id("pcp").present_rank == 0


def test_TC_2102_the_oracle_board_keeps_its_bytes(tmp_path):
    """TC-2102 (LLR-2102.1): the PRES-V3 board, loaded and saved, is byte-identical."""
    path = tmp_path / "b.json"
    pb.build(path).save()
    Board.load(path).save()
    before = path.read_bytes()
    Board.load(path).save()
    assert path.read_bytes() == before


def test_TC_2102_the_presentation_order(tmp_path):
    """TC-2102 (LLR-2102.1): ranked projects first by rank, the unranked after
    them in board order; duplicate ranks keep board order and the sort is stable;
    archived projects are not listed; `set_present_order` then `present_order`
    gives back the ids."""
    b = pf.build(tmp_path / "b.json")
    ids = lambda: [p.id for p in models.present_order(b)]           # noqa: E731
    assert ids() == ["pcp", "pbm", "pmr", "pdp", "psa", "pbr"]
    b.project_by_id("pdp").present_rank = 0
    b.project_by_id("pbr").present_rank = 1
    assert ids() == ["pdp", "pbr", "pcp", "pbm", "pmr", "psa"]
    b.project_by_id("pmr").present_rank = 1
    assert ids() == ["pdp", "pmr", "pbr", "pcp", "pbm", "psa"] == ids()
    b.project_by_id("pcp").archived = True
    assert "pcp" not in ids()
    want = ["psa", "pbr", "pdp", "pmr", "pbm"]
    models.set_present_order(b, want)
    assert ids() == want
    assert [b.project_by_id(i).present_rank for i in want] == [0, 1, 2, 3, 4]


def test_TC_2102_a_team_pull_never_curates_this_presentation(tmp_path):
    """TC-2102 (LLR-2102.1; security S-4): a NEW project a team pull adds arrives
    shown and unranked, whatever `team.json` says; an existing project's flags are
    never touched by a pull."""
    from taskboard.team_sync import TeamState
    b = pf.build(tmp_path / "b.json")
    b.project_by_id("pcp").present_rank = 2
    sync = TeamState.__new__(TeamState)
    sync.config = {"projects": [
        {"id": "pnew", "name": "New team project", "show_in_present": False, "present_rank": 0},
        {"id": "pcp", "name": "Customer Portal", "show_in_present": False, "present_rank": 9}]}
    sync.apply_config_to_board(b)
    new = b.project_by_id("pnew")
    assert new is not None and new.show_in_present is True and new.present_rank is None
    old = b.project_by_id("pcp")
    assert old.show_in_present is True and old.present_rank == 2


# --------------------------------------------------------------------------- #
# TC-2103 — the view-3 renderer (increment 003)
# --------------------------------------------------------------------------- #
import html
import re

from taskboard import views
from taskboard.views import vis

ROUND = Path(__file__).resolve().parents[1] / "prototypes" / "present_portfolio" / "out"
PAYLOADS = ["[@click=app.quit]x[/]", "tail\\", "[bold", "x[/]"]


def _svg_rows(path: Path, width: int, height: int) -> list[str]:
    """The text rows of a Textual `export_screenshot` SVG, read as a FILE (the
    round's capture): every `<text>` of a terminal line placed at its column
    (`x / 12.2`, the cell width of the export)."""
    rows = [[" "] * width for _ in range(height)]
    pat = re.compile(r'<text class="[^"]*" x="([\d.]+)" y="[\d.]+" textLength="[\d.]+" '
                     r'clip-path="url\(#[^)]*-line-(\d+)\)">([^<]*)</text>')
    for x, line, body in pat.findall(path.read_text(encoding="utf-8")):
        y, col = int(line), round(float(x) / 12.2)
        if y >= height:
            continue
        for i, ch in enumerate(html.unescape(body).replace("\xa0", " ")):
            if col + i < width:
                rows[y][col + i] = ch
    return ["".join(r) for r in rows]


def _plain(text) -> list[str]:
    return text.plain.split("\n")


def _ranked(tmp_path):
    """The round's board ranked in reverse, Data Platform hidden: the order mutant's
    witness (qa-reviewer QA-13)."""
    b = pf.build(tmp_path / "r.json")
    models.set_present_order(b, [p.id for p in reversed(b.projects)])
    b.project_by_id("pdp").show_in_present = False
    return b


def _boards(tmp_path):
    return {"round": pf.build(tmp_path / "b.json"), "ranked": _ranked(tmp_path),
            "pres": pb.build(tmp_path / "p.json")}


def _cursors(board):
    out = [None]
    for p in models.present_order(board):
        out.append(("proj", p.id))
        ts = views.present_tasks(board, p.id)[0]
        if ts:
            out.append(("task", ts[0].id))
    return out


@pytest.mark.parametrize("width", (36, 60, 80, 99, 100, 118, 160))
def test_TC_2103_the_frame_sweep(tmp_path, width):
    """TC-2103 (LLR-2103.1): over three boards × heights × cursors × rail focus ×
    folds: exactly height rows of width cells; the rail iff ≥ 100 columns; the
    timeline's headers in presentation order, shown projects only; hidden tasks
    and hidden projects' tasks absent; the cursor's project never auto-folded;
    no `+N more rows not shown` and no auto-fold when every row fits."""
    for name, board in _boards(tmp_path).items():
        shown = [p for p in models.present_order(board) if p.show_in_present]
        hidden_titles = [t.title for p in board.projects for t in board.tasks
                         if t.project_id == p.id and not board.is_done(t)
                         and (not t.show_in_present or not p.show_in_present)]
        for height in (10, 45):           # cut + overflowing, roomy (bounded: QA-12)
            for cur in _cursors(board):
                for focus in (False, True):
                    for folded in ((frozenset(), frozenset({shown[0].id})) if not focus
                                   else (frozenset(),)):
                        r = views.render_present_all(board, cur, pf.TODAY, width, height,
                                                     folded, focus)
                        rows = _plain(r.frame)
                        assert len(rows) == height and all(vis(x) == width for x in rows), \
                            (name, width, height, cur)
                        if width < 36:
                            continue
                        rail = width >= views.PRESENT_RAIL_MIN
                        assert any("PROJECTS" in x for x in rows) == rail
                        assert bool(r.rail_stops) == rail
                        tl = _plain(r.timeline)
                        assert len(tl) == height and all(vis(x) == r.timeline_w for x in tl)
                        body = "\n".join(tl)
                        for title in hidden_titles:
                            assert title not in body, (name, title)
                        heads = [s[1] for s in r.stops if s[0] == "proj"]
                        assert heads == [p.id for p in shown][:len(heads)], (name, heads)
                        cur_p = None if cur is None else (
                            cur[1] if cur[0] == "proj"
                            else board.task_by_id(cur[1]).project_id)
                        if cur_p and cur_p not in folded and board.project_by_id(cur_p).show_in_present:
                            name_p = board.project_by_id(cur_p).name[:12]
                            heads = [x for x in tl if "■ " + name_p in x]
                            assert not any(x.startswith("▸") for x in heads), (name, cur_p)
                        # the cursor as drawn is a stop, and no stop is under the overflow
                        # row (code review F1 of increment 003)
                        assert r.cursor is None or r.cursor in r.stops or (
                            focus and rail), (name, r.cursor)
                        assert len(r.stops) == len(set(r.stops))
                        if "more rows not shown" not in body:
                            for p in shown:
                                if p.id not in folded and ("proj", p.id) in r.stops:
                                    ts = views.present_tasks(board, p.id)[0]
                                    folded_auto = ts and ("task", ts[0].id) not in r.stops
                                    if folded_auto:
                                        # an auto-fold only when the unfolded rows overflow
                                        need = sum(1 + len(views.present_tasks(board, q.id)[0])
                                                   for q in shown if q.id not in folded)
                                        assert need > height - 3, (name, p.name, height)


def test_TC_2103_the_order_follows_present_rank(tmp_path):
    """TC-2103 (LLR-2103.1; QA-13): on the reverse-ranked board the timeline's
    headers and the rail read the presentation order, not the board's."""
    b = _ranked(tmp_path)
    r = views.render_present_all(b, None, pf.TODAY, 160, 45)
    want = [p.id for p in reversed(b.projects) if p.show_in_present]
    assert [s[1] for s in r.stops if s[0] == "proj"] == want
    assert [s[1] for s in r.rail_stops] == [p.id for p in reversed(b.projects)]


@pytest.mark.parametrize("size, svg", [((160, 45), "C-160-initial.svg"),
                                       ((118, 30), "C-118-initial.svg")])
def test_TC_2103_equals_the_rounds_capture(tmp_path, size, svg):
    """TC-2103 (LLR-2103.1): with the round's starting state (`R` on `Tax rules for
    new regions`, `3`: the rail's cursor on Billing Migration) the frame's text is
    the round's approved C capture, row for row — the screen's own hint row
    (the capture's last row) aside."""
    w, h = size
    b = pf.build(tmp_path / "b.json")
    r = views.render_present_all(b, ("proj", "pbm"), pf.TODAY, w, h - 1, frozenset(), True)
    want = _svg_rows(ROUND / svg, w, h - 1)
    got = _plain(r.frame)
    diff = [(y, g, x) for y, (g, x) in enumerate(zip(got, want)) if g.rstrip() != x.rstrip()]
    assert not diff, diff


def test_TC_2103_markup_in_a_name_paints_literally(tmp_path):
    """TC-2103 (LLR-2103.1; security S-2): the four payloads in a project name and
    a task title paint literally on the rail, the header and the task row, and no
    span carries an action."""
    b = pf.build(tmp_path / "b.json")
    for i, payload in enumerate(PAYLOADS):
        b.project_by_id("pcp").name = f"P{payload}"
        b.task_by_id("tc2").title = f"T{payload}"
        r = views.render_present_all(b, ("task", "tc2"), pf.TODAY, 200, 45, frozenset(), False)
        text = r.frame.plain
        assert f"T{payload}"[:12] in text, payload
        assert any(f"P{payload}"[:10] in row for row in text.split("\n")), payload
        assert not any("@click" in str(s.style) or getattr(s.style, "meta", None)
                       for s in r.frame.spans), payload


def test_TC_2103_empty_states(tmp_path):
    """TC-2103 (LLR-2103.1 empty): every project hidden → the header and the
    ruler only, `0 projects`, no stop; a project with no open task draws its
    header alone; below 36 columns the narrow frame."""
    b = pf.build(tmp_path / "b.json")
    for p in b.projects:
        p.show_in_present = False
    r = views.render_present_all(b, None, pf.TODAY, 118, 30)
    assert r.stops == [] and "0 projects" in r.frame.plain
    narrow = views.render_present_all(b, None, pf.TODAY, 30, 10)
    assert narrow.frame.plain == views.render_present(b, None, None, pf.TODAY, 30, 10).plain
    assert narrow.stops == [] and "36+" in _plain(narrow.frame)[0]


# --------------------------------------------------------------------------- #
# TC-2106 (rows) — what `u` lists (increment 003)
# --------------------------------------------------------------------------- #
def test_TC_2106_the_hidden_rows(tmp_path):
    """TC-2106 (LLR-2106.1): views 1/2 list the project's hidden tasks; view 3 lists,
    in presentation order, each project that is hidden or holds hidden tasks,
    then its hidden tasks — a hidden project's own hidden tasks too; nothing hidden,
    nothing listed."""
    b = pf.build(tmp_path / "b.json")
    assert views.present_hidden_rows(b, "pcp", False) == [("task", "tc6", 0)]
    assert views.present_hidden_rows(b, "pbm", False) == []
    assert views.present_hidden_rows(b, "pcp", True) == [
        ("proj", "pcp", 0), ("task", "tc6", 1), ("proj", "pdp", 0), ("task", "td4", 1),
        ("proj", "psa", 0)]
    b.task_by_id("ts2").show_in_present = False
    assert ("task", "ts2", 1) in views.present_hidden_rows(b, "pcp", True)
    for p in b.projects:
        p.show_in_present = True
    for t in b.tasks:
        t.show_in_present = True
    assert views.present_hidden_rows(b, "pcp", True) == []


# --------------------------------------------------------------------------- #
# The screen: TC-2104, TC-2105, TC-2106 (picker), AT-2102..AT-2106 (increment 004)
# --------------------------------------------------------------------------- #
from datetime import date as _date


class _Today(_date):
    @classmethod
    def today(cls):
        return pf.TODAY


@pytest.fixture
def frozen(monkeypatch):
    from taskboard import app as app_module
    monkeypatch.setattr(app_module, "date", _Today)
    monkeypatch.setattr(models, "date", _Today)


class _Show:
    """The app on the round's board saved to disk, `R` pressed on `Tax rules for
    new regions`; helpers read the painted widgets as Textual holds them."""

    def __init__(self, tmp_path, size, build=True):
        from taskboard.app import TaskboardApp
        self.path = tmp_path / "board.json"
        if build:
            pf.build(self.path).save()
        self.size = size
        self.app = TaskboardApp(board_path=str(self.path))

    async def open(self, pilot):
        await pilot.pause()
        self.app.selected_task_id = pf.CURSOR
        await self.press(pilot, "R")
        return self.app.screen

    async def press(self, pilot, *keys):
        for k in keys:
            await pilot.press(k)
            await pilot.pause()

    @property
    def scr(self):
        stack = self.app.screen_stack
        return next(s for s in reversed(stack) if type(s).__name__ == "PresentScreen")

    def frame(self) -> list[str]:
        return self.scr.query_one("#present-frame").content.plain.split("\n")

    def hint(self) -> str:
        return self.scr.query_one("#present-hint").content.plain

    def bytes(self) -> bytes:
        return self.path.read_bytes()

    def projects(self) -> dict:
        return {p["id"]: p for p in json.loads(self.path.read_text(encoding="utf-8"))["projects"]}

    def tasks(self) -> dict:
        return {t["id"]: t for t in json.loads(self.path.read_text(encoding="utf-8"))["tasks"]}

    async def goto(self, pilot, target: str):
        """`↓` then `↑` until view 3's cursor is on `target` — keys only."""
        for key in ("down", "up"):
            for _ in range(40):
                cur = self.scr._all_cur
                if cur is not None and cur[1] == target:
                    return
                await self.press(pilot, key)
        raise AssertionError((target, self.scr._all_cur))


def _rail(rows):
    return [r[:views.PRESENT_RAIL_W] for r in rows]


def _timeline(rows):
    return [r[views.PRESENT_RAIL_W + 1:] for r in rows]


async def test_AT_2103_the_portfolio_on_one_ruler(tmp_path, frozen):
    """AT-2103 (US-2102, HLR-2103): `R`, `3` at 160x45 — the header, every shown
    project in order with its open tasks, no hidden item, the rail; at 118x30 the
    rail and exact widths; at 80x24 no rail."""
    s = _Show(tmp_path, (160, 45))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "3")
        rows = s.frame()
        tl = _timeline(rows)
        assert tl[0].startswith("◆ PRESENT · 5 projects  all"), tl[0]
        assert tl[0].rstrip().endswith("23 open · ▲2 past due"), tl[0]
        order = [n for r in tl for n in ("Customer Portal", "Billing Migration",
                                         "Mobile Release 3.2", "Data Platform", "Brand Refresh")
                 if "■ " + n in r]
        assert order == ["Customer Portal", "Billing Migration", "Mobile Release 3.2",
                         "Data Platform", "Brand Refresh"], order
        body = "\n".join(tl)
        for _, pk, title, phase, *_ in pf.TASKS:
            if pk != "sa" and phase != "Done" and title not in ("Help-center links",
                                                                  "Cost dashboards"):
                assert title in body, title
        for gone in ("Threat model review", "Help-center links", "Cost dashboards"):
            assert gone not in body, gone
        rail = _rail(rows)
        want = ["  1 ● Customer Portal", "▶ 2 ● Billing Migrati…", "  3 ● Mobile Release …",
                "  4 ● Data Platform", "  5 ○ Security Audit", "  6 ● Brand Refresh"]
        for w in want:
            assert any(r.startswith(w) for r in rail), (w, rail)
        assert any(r.startswith(" 5 shown · 1 hidden") for r in rail), rail
        assert any(r.startswith(" 2 tasks hidden") for r in rail), rail
    for size, has_rail in (((118, 30), True), ((80, 24), False)):
        s = _Show(tmp_path / f"{size[0]}", size)
        async with s.app.run_test(size=s.size) as pilot:
            await s.open(pilot)
            await s.press(pilot, "3")
            rows = s.frame()
            assert all(vis(r) == size[0] for r in rows), size
            assert any("PROJECTS" in r for r in rows) == has_rail
            assert any("│" in r for r in rows) == has_rail


async def test_AT_2104_three_views_one_cursor_and_the_export(tmp_path, frozen):
    """AT-2104 (US-2102, HLR-2104): the hint names three views; `tab` cycles 1 → 2
    → 3 → 1 with the cursor handed over; `x` in view 3 writes one `-all` SVG
    without the rail or the hint; view 3's hint keeps its labels and `u`."""
    s = _Show(tmp_path, (160, 45))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        assert s.hint().startswith("1 gantt  2 split  3 all"), s.hint()
        spans = {s.hint()[sp.start:sp.end]: str(sp.style)
                 for sp in s.scr.query_one("#present-hint").content.spans}
        assert "bold" in spans.get("1 gantt", ""), spans
        await s.press(pilot, "tab", "tab")
        rows = s.frame()
        assert " all" in _timeline(rows)[0]
        assert any(r.startswith("▶ 2 ● Billing") for r in _rail(rows)), _rail(rows)
        await s.press(pilot, "tab")
        assert "Billing Migration" in s.frame()[0] and "gantt" in s.frame()[0]
        await s.press(pilot, "3", "right")
        assert any("project span ▸" in r for r in _timeline(s.frame())[:3])
        await s.press(pilot, "down")
        assert s.scr._all_cur == ("task", "tb2")
        assert any("selected task ▸" in r for r in _timeline(s.frame())[:3])
        await s.press(pilot, "1")
        assert any("⟦Dual-run reconciliation⟧" in r for r in s.frame()), s.frame()
        await s.press(pilot, "3")
        hint = s.hint()
        assert hint.rstrip().endswith("· u 3 hidden"), hint
        for key in ("␣ hide", "⇧↑↓", "enter fold"):
            assert key in hint, (key, hint)
        await s.press(pilot, "x")
        svgs = list((tmp_path / "reports").glob("*.svg"))
        assert [p.name for p in svgs] == ["present-board-2026-10-19-all.svg"], svgs
        svg = svgs[0].read_text(encoding="utf-8").replace("&#160;", " ")
        for name in ("Customer Portal", "Billing Migration", "Mobile Release 3.2",
                     "Data Platform", "Brand Refresh"):
            assert name in svg, name
        for absent in ("PROJECTS", "shown ·", "u 3 hidden", "3 all"):
            assert absent not in svg, absent


async def test_AT_2102_the_order_and_hidden_projects_survive_a_restart(tmp_path, frozen):
    """AT-2102 (US-2103, HLR-2102): reorder and hide on the rail → the file's ranks
    and flags; a restart shows the same order; the main gantt keeps board order."""
    s = _Show(tmp_path, (160, 45))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "3", "down")
        assert s.scr._all_cur == ("proj", "pmr")
        await s.press(pilot, "shift+up", "shift+up")
        await s.goto(pilot, "pbr")
        await s.press(pilot, "space")
    recs = s.projects()
    assert {k: recs[k].get("present_rank") for k in recs} == {
        "pmr": 0, "pcp": 1, "pbm": 2, "pdp": 3, "psa": 4, "pbr": 5}
    assert sorted(k for k in recs if recs[k].get("show_in_present") is False) == ["pbr", "psa"]
    s2 = _Show(tmp_path, (160, 45), build=False)
    async with s2.app.run_test(size=s2.size) as pilot:
        await s2.open(pilot)
        await s2.press(pilot, "3")
        tl = "\n".join(_timeline(s2.frame()))
        pos = [tl.index("■ " + n) for n in ("Mobile Release 3.2", "Customer Portal",
                                            "Billing Migration", "Data Platform")]
        assert pos == sorted(pos), pos
        assert "■ Brand Refresh" not in tl
        assert any(r.startswith("  6 ○ Brand Refresh") for r in _rail(s2.frame()))
        await s2.press(pilot, "escape", "3")
        ranked = s2.app.query_one("#board").content.plain
    # the same board with every presentation key stripped: the main gantt is identical
    raw = json.loads(s.path.read_text(encoding="utf-8"))
    for rec in raw["projects"]:
        rec.pop("present_rank", None)
        rec.pop("show_in_present", None)
    (tmp_path / "plain").mkdir()
    (tmp_path / "plain" / "board.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
    s3 = _Show(tmp_path / "plain", (160, 45), build=False)
    async with s3.app.run_test(size=s3.size) as pilot:
        await s3.open(pilot)
        await s3.press(pilot, "escape", "3")
        assert s3.app.query_one("#board").content.plain == ranked


async def test_AT_2105_the_presenter_curates_view_3(tmp_path, frozen):
    """AT-2105 (US-2103, HLR-2105): fold, hide a task, hide a project, re-show it
    on the rail, show all with a notice, keys that change nothing write nothing."""
    s = _Show(tmp_path, (160, 45))
    async with s.app.run_test(size=s.size, notifications=True) as pilot:
        await s.open(pilot)
        await s.press(pilot, "3")
        base = s.bytes()
        await s.press(pilot, "right")
        await s.goto(pilot, "pdp")
        await s.press(pilot, "enter")
        assert not any("Ingest pipeline v2" in r for r in s.frame())
        await s.press(pilot, "up")                    # off the header: its caret shows
        assert any("▸ ■ Data Platform" in r for r in s.frame()), s.frame()
        assert s.bytes() == base
        await s.press(pilot, "down", "enter")
        assert any("Ingest pipeline v2" in r for r in s.frame())
        await s.goto(pilot, "tm2")
        await s.press(pilot, "space")
        assert not any("Offline mode" in r for r in s.frame())
        assert s.tasks()["tm2"]["show_in_present"] is False
        await s.goto(pilot, "pbr")
        await s.press(pilot, "space")
        assert not any("■ Brand Refresh" in r for r in _timeline(s.frame()))
        assert any("○ Brand Refresh" in r for r in _rail(s.frame()))
        assert s.projects()["pbr"]["show_in_present"] is False
        await s.press(pilot, "left")
        await s.goto(pilot, "pbr")
        await s.press(pilot, "space")
        assert any(r.startswith("▶ 6 ● Brand Refresh") for r in _rail(s.frame())), _rail(s.frame())
        assert "show_in_present" not in s.projects()["pbr"]
        await s.press(pilot, "a")
        notes = [str(n.message) for n in s.app._notifications]
        assert "Shown again: 1 project + 3 tasks" in notes, notes
        assert "show_in_present" not in s.bytes().decode("utf-8")
        after = s.bytes()
        await s.press(pilot, "a")
        assert s.bytes() == after
        await s.goto(pilot, "pcp")
        await s.press(pilot, "shift+up")
        assert s.bytes() == after


async def test_AT_2106_u_lists_the_hidden_and_brings_one_back(tmp_path, frozen):
    """AT-2106 (US-2104, HLR-2106): two tasks hidden in view 1, `u` lists them,
    one toggled back, `esc`; in view 3 the grouped list; after `a`, nothing."""
    s = _Show(tmp_path, (118, 31))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "space", "space", "u")
        rows = s.app.screen.query_one("#picker-rows").content.plain.split("\n")
        assert [r.strip("▶ ") for r in rows] == ["○ Tax rules for new regions",
                                                 "○ Refund edge cases"], rows
        await s.press(pilot, "space")
        rows = s.app.screen.query_one("#picker-rows").content.plain.split("\n")
        assert rows[0].strip("▶ ") == "● Tax rules for new regions", rows
        assert "show_in_present" not in s.tasks()["tb3"]
        await s.press(pilot, "escape")
        frame = "\n".join(s.frame())
        assert "Tax rules for new regions" in frame and "Refund edge cases" not in frame
        await s.press(pilot, "3", "u")
        rows = [r.strip("▶ ") for r in
                s.app.screen.query_one("#picker-rows").content.plain.split("\n")]
        assert rows == ["● Customer Portal", "○ Help-center links", "● Billing Migration",
                        "○ Refund edge cases", "● Data Platform", "○ Cost dashboards",
                        "○ Security Audit"], rows
        await s.press(pilot, "u")
        assert type(s.app.screen).__name__ == "PresentScreen"
        await s.press(pilot, "a", "u")
        assert s.app.screen.query_one("#picker-rows").content.plain == "nothing hidden"


# the first widths of `.dev-flow/2026-10-19-batch-01/evidence/hint-widths.txt` (PC-4:
# `rich.cells.cell_len` over the literal strings, outside the code), pasted literally
N2, N1 = "1 gantt  2 split  3 all  ", "1 gantt 2 split 3 all "
ALL_WORDINGS = {
    "all-rail": {"long": N2 + "⇥ next · ↑↓ move · ←→ rail/timeline · ␣ hide · ⇧↑↓ reorder · enter fold · a show all · x export · esc leave",
                 "middle": N2 + "⇥ · ↑↓ · ←→ rail · ␣ hide · ⇧↑↓ order · enter fold · a all · x · esc",
                 "compact": N1 + "⇥ ↑↓ ←→ ␣ ⇧↑↓ enter a x esc",
                 "esc": N1 + "esc"},
    "all": {"long": N2 + "⇥ next · ←→ ↑↓ move · ␣ hide · ⇧↑↓ reorder · enter fold · a show all · x export · esc leave",
            "middle": N2 + "⇥ · ←→ ↑↓ · ␣ hide · ⇧↑↓ order · enter fold · a all · x · esc",
            "compact": N1 + "⇥ ←→ ↑↓ ␣ ⇧↑↓ enter a x esc",
            "esc": N1 + "esc"},
}
ALL_FIRST = {
    ("all-rail", 0): {"middle": 100, "long": 134},
    ("all-rail", 1): {"compact": 100, "middle": 108, "long": 147},
    ("all-rail", 3): {"compact": 100, "middle": 108, "long": 147},
    ("all", 0): {"esc": 36, "compact": 51, "middle": 88},
    ("all", 1): {"esc": 36, "compact": 64},
    ("all", 3): {"esc": 36, "compact": 64},
}


def _screen_all(tmp_path, hidden: int):
    """A `PresentScreen` (not mounted) in view 3 on the round's board with exactly
    `hidden` items `u` would list."""
    from taskboard.app import PresentScreen
    b = pf.build(tmp_path / "h.json")
    for p in b.projects:
        p.show_in_present = True
    for t in b.tasks:
        t.show_in_present = True
    for t in b.tasks[:hidden]:
        t.show_in_present = False
    scr = PresentScreen(b, "pbm", "Billing Migration", pf.CURSOR)
    scr._view = 2
    return scr


def test_TC_2104_view_3s_hint_takes_the_first_wording_that_fits(tmp_path):
    """TC-2104 (LLR-2104.1): over widths 36–200 × 0 / 1 / 3 hidden, view 3's hint is
    the wording of the literal first-width table plus ` · u N hidden`; it never
    paints more than `w - 2` cells; at 118 with something hidden it keeps its
    labels (`␣ hide`, `⇧↑↓ order`, `enter fold`)."""
    for hidden in (0, 1, 3):
        scr = _screen_all(tmp_path / str(hidden), hidden)
        tail = f" · u {hidden} hidden" if hidden else ""
        for w in range(36, 201):
            view = "all-rail" if w >= views.PRESENT_RAIL_MIN else "all"
            table = ALL_FIRST[(view, hidden)]
            tier = max((t for t, first in table.items() if first <= w), key=lambda t: table[t])
            got = scr._hint(w).plain
            want = ALL_WORDINGS[view][tier] + tail
            if vis(want) > w - 2:                       # none fits: the last, cut with `…`
                want = want[:w - 3] + "…"
            assert got == want, (hidden, w, got)
            assert vis(got) <= w - 2
        assert "enter fold" in scr._hint(118).plain and "␣ hide" in scr._hint(118).plain


def test_TC_2104_the_view_names_and_the_u_tail_in_views_1_2(tmp_path):
    """TC-2104 (LLR-2104.1): views 1/2 name three views and count with `u`; below
    36 columns the count without `u` (no key acts there)."""
    from taskboard.app import PresentScreen
    b = pf.build(tmp_path / "b.json")
    scr = PresentScreen(b, "pcp", "Customer Portal", "tc2")
    assert scr._hint(160).plain == ("1 gantt  2 split  3 all  ⇥ next · ←→ ↑↓ move · ␣ hide · "
                                    "a show all · x export · esc leave · u 1 hidden")
    assert scr._hint(30).plain == "esc leave · 1 hidden"
    assert views.PRESENT_SCREEN_VIEWS == ("gantt", "split", "all")
    assert views.PRESENT_VIEWS == ("gantt", "split")
    svg, png = views.present_paths(b, None, pf.TODAY, "all")
    assert svg.name == "present-board-2026-10-19-all.svg" and png.suffix == ".png"


async def test_TC_2104_the_cycle_and_the_hand_off(tmp_path, frozen):
    """TC-2104 (LLR-2104.1): `tab` 1 → 2 → 3 → 1, `shift+tab` back, `3` from 1 and 2;
    entering view 3 on the rail puts its cursor on the current project; leaving
    view 3 shows its cursor's project and task in views 1/2; below 100 columns
    entering view 3 lands on the cursor task's row, or on a hidden project the
    first drawn row."""
    s = _Show(tmp_path, (160, 45))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        seen = []
        for key in ("tab", "tab", "tab", "shift+tab", "shift+tab", "shift+tab"):
            await s.press(pilot, key)
            seen.append(s.scr._view)
        assert seen == [1, 2, 0, 2, 1, 0], seen
        await s.press(pilot, "2", "3")
        assert s.scr._view == 2 and s.scr._all_cur == ("proj", "pbm") and s.scr._rail
        await s.press(pilot, "right")
        await s.goto(pilot, "tm3")
        await s.press(pilot, "1")
        assert (s.scr._project_id, s.scr._cursor_id) == ("pmr", "tm3")
        assert "Mobile Release 3.2" in s.frame()[0]
    s = _Show(tmp_path / "n", (80, 24))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "3")
        assert s.scr._all_cur == ("task", pf.CURSOR) and not s.scr._rail
        await s.press(pilot, "1")
        s.scr._project_id, s.scr._cursor_id = "psa", "ts1"      # a hidden project in view 3
        await s.press(pilot, "3")
        assert s.scr._all_cur == ("proj", "pcp"), s.scr._all_cur
        await s.press(pilot, "1")
        assert s.scr._project_id == "pcp"


async def test_TC_2105_the_curation_writes_exactly_what_changed(tmp_path, frozen, monkeypatch):
    """TC-2105 (LLR-2105.1): one save per change, none for a key that changes
    nothing; the cursor after a hide; the rail's toggle in place; dense ranks
    over every visible project; the timeline's reorder passes a hidden project;
    `enter` folds without a write; inert keys outside view 3."""
    saves = []
    real = Board.save
    monkeypatch.setattr(Board, "save", lambda self: (saves.append(1), real(self))[1])
    s = _Show(tmp_path, (160, 45))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        n0 = len(saves)
        await s.press(pilot, "enter", "shift+up", "shift+down")          # view 1: inert
        assert len(saves) == n0
        await s.press(pilot, "3", "pagedown", "right")
        assert len(saves) == n0
        await s.goto(pilot, "tb7")
        nxt_before = s.scr._stops()
        i = nxt_before.index(("task", "tb7"))
        await s.press(pilot, "space")
        assert len(saves) == n0 + 1 and s.scr._all_cur == nxt_before[i + 1]
        await s.goto(pilot, "pmr")
        await s.press(pilot, "enter", "enter")
        assert len(saves) == n0 + 1
        await s.goto(pilot, "td5")                       # the last stop of a project
        await s.press(pilot, "left")
        assert s.scr._all_cur == ("proj", "pdp")
        await s.press(pilot, "space", "space")           # the rail: hidden, shown, in place
        assert len(saves) == n0 + 3 and s.scr._all_cur == ("proj", "pdp")
        assert s.scr._board.project_by_id("pdp").show_in_present
        await s.goto(pilot, "pmr")
        await s.press(pilot, "shift+up", "shift+up")
        assert len(saves) == n0 + 5
        ranks = {p.id: p.present_rank for p in s.scr._board.projects}
        assert sorted(ranks.values()) == list(range(6)) and ranks["pmr"] == 0
        await s.press(pilot, "shift+up")                 # at the top: nothing
        assert len(saves) == n0 + 5
        await s.press(pilot, "right")
        await s.goto(pilot, "pdp")
        await s.press(pilot, "shift+down")               # over the hidden Security Audit
        order = [p.id for p in models.present_order(s.scr._board)]
        assert order.index("pdp") > order.index("psa"), order
        await s.press(pilot, "a")
        assert len(saves) == n0 + 7
        await s.press(pilot, "a")
        assert len(saves) == n0 + 7


async def test_TC_2106_the_picker(tmp_path, frozen):
    """TC-2106 (LLR-2106.1): the picker toggles one flag per keypress with one save
    each, the mark follows, the rows stay; a title holding markup paints literally;
    `nothing hidden` with no row."""
    b = pf.build(tmp_path / "board.json")
    b.task_by_id("tc6").title = "[@click=app.quit]x[/] [bold tail\\"
    b.save()
    s = _Show(tmp_path, (118, 31), build=False)
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "3", "u")
        rows = s.app.screen.query_one("#picker-rows").content
        assert "[@click=app.quit]x[/] [bold tail\\" in rows.plain
        # the cursor starts on the first hidden row, never on a shown project's heading
        assert rows.plain.splitlines()[1].startswith("▶"), rows.plain
        assert not any("@click" in str(sp.style) for sp in rows.spans)
        await s.press(pilot, "space")
        assert "show_in_present" not in s.tasks()["tc6"]
        await s.press(pilot, "space")
        assert s.tasks()["tc6"]["show_in_present"] is False
        assert "○ [@click" in s.app.screen.query_one("#picker-rows").content.plain
        await s.press(pilot, "escape", "a", "u")
        assert s.app.screen.query_one("#picker-rows").content.plain == "nothing hidden"


def test_TC_2103_no_stop_hides_under_the_overflow_row(tmp_path):
    """TC-2103 (LLR-2103.1; code review F1 of increment 003): when the overflow row
    takes the frame's last row, every cursor stop is a row the frame draws, and a
    cursor on a row the overflow covers is drawn on the last stop instead."""
    b = pf.build(tmp_path / "b.json")
    for height in (6, 8, 10, 14):
        for cur in (("proj", "pbr"), ("task", "tm6"), None):
            r = views.render_present_all(b, cur, pf.TODAY, 118, height)
            rows = _plain(r.timeline)
            drawn = "\n".join(rows[:-1] if "more rows not shown" in rows[-1] else rows)
            for kind, oid in r.stops:
                label = (b.project_by_id(oid).name if kind == "proj"
                         else b.task_by_id(oid).title)[:10]
                assert label in drawn, (height, cur, label)
            assert r.cursor is None or r.cursor in r.stops, (height, cur, r.cursor)


def test_TC_2103_the_rail_counts_every_hidden_task(tmp_path):
    """TC-2103 (HLR-2103; code review F3 of increment 003): the rail's task count
    is every visible project's hidden tasks — a hidden project's own hidden task
    counts too, as `u` lists it."""
    b = pf.build(tmp_path / "b.json")
    b.task_by_id("ts1").show_in_present = False          # Security Audit is hidden
    rail = _plain(views.render_present_all(b, None, pf.TODAY, 160, 45).frame)
    assert any(r.startswith(" 3 tasks hidden") for r in rail), rail


async def test_TC_2105_a_resize_keeps_the_cursor_and_the_rail_safe(tmp_path, frozen):
    """TC-2105 (LLR-2104.1, LLR-2105.1; code review F1/F2 of increment 004): a task
    cursor moved on the timeline under 100 columns becomes its project when the
    rail is back (`space` there toggles that project, it does not crash); a trip
    below 36 columns keeps view 3's cursor."""
    s = _Show(tmp_path, (160, 45))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "3")
        await pilot.resize_terminal(90, 45)
        await s.press(pilot, "down")
        assert s.scr._all_cur[0] == "task"
        proj = s.scr._board.task_by_id(s.scr._all_cur[1]).project_id
        await pilot.resize_terminal(160, 45)
        await pilot.pause()
        await pilot.pause()
        assert s.scr._all_cur == ("proj", proj), s.scr._all_cur
        await s.press(pilot, "space")
        assert s.projects()[proj]["show_in_present"] is False
        await s.press(pilot, "space")
        await s.goto(pilot, "pdp")
        await pilot.resize_terminal(30, 45)
        await pilot.pause()
        await pilot.pause()
        await pilot.resize_terminal(160, 45)
        await pilot.pause()
        await pilot.pause()
        assert s.scr._all_cur == ("proj", "pdp"), s.scr._all_cur


async def test_TC_2106_the_presentation_stays_in_view_behind_the_picker(tmp_path, frozen):
    """TC-2106 (HLR-2106; the coordinator's review of the capture
    `seq-160x45-4-picker`): with `u` open the presentation is still painted
    behind the picker — the screenshot holds both the picker's title and the
    frame's own text (its header and a project the picker does not list) — under
    the app's own modal backdrop (`taskboard.tcss`, the rule the other modals share)."""
    s = _Show(tmp_path, (160, 45))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "3", "u")
        assert type(s.app.screen).__name__ == "PresentHiddenPicker"
        assert 0 < s.app.screen.styles.background.a < 1        # dimmed, not hidden
        shot = s.app.export_screenshot().replace("&#160;", " ")
        assert "Hidden from the presentation" in shot
        assert "PRESENT" in shot and "Mobile Release 3.2" in shot and "Schema registry" in shot


# --------------------------------------------------------------------------- #
# TC-2304 / AT-2304 — an unarchived project never ties a rank (batch 2026-10-20-batch-02,
# HLR-2304 / LLR-2304.1, US-2303)
# --------------------------------------------------------------------------- #
async def test_TC_2304_the_unarchive_rank_rule(tmp_path, frozen):
    """TC-2304 (LLR-2304.1): through the projects modal's own toggle — a rank taken
    while archived → after the largest shown rank; no tie → kept; the only ranked
    project → kept; no rank → none; archiving keeps the rank."""
    from taskboard.app import TaskboardApp
    from taskboard.modals import ProjectPicker
    path = tmp_path / "board.json"
    pd = Project("pd", id="pd", archived=True)
    pd.present_rank = 9                     # archived: its rank is never counted
    Board([Project(n, id=n) for n in ("pa", "pb", "pc")] + [pd], [], path).save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        b = app.board
        pa, pb_, pc = (b.project_by_id(x) for x in ("pa", "pb", "pc"))
        app.push_screen(ProjectPicker(b))
        await pilot.pause()
        pick = app.screen

        def toggle(p):
            pick._do_archive_toggle(p)
        models.set_present_order(b, ["pa", "pb", "pc"])
        toggle(pa)                                     # archived: the rank kept
        assert pa.archived and pa.present_rank == 0
        models.set_present_order(b, ["pc", "pb"])      # pc takes rank 0
        toggle(pa)
        assert (pa.present_rank, pb_.present_rank, pc.present_rank) == (2, 1, 0)
        toggle(pb_)                                    # archive and back at once: kept
        toggle(pb_)
        assert pb_.present_rank == 1
        for p in (pb_, pc):
            p.present_rank = None
        toggle(pa)
        toggle(pa)                                     # the only ranked project: kept
        assert pa.present_rank == 2
        toggle(pc)
        toggle(pc)                                     # no rank: none
        assert pc.present_rank is None
    saved = {p["id"]: p.get("present_rank") for p in
             json.loads(path.read_text(encoding="utf-8"))["projects"]}
    assert saved == {"pa": 2, "pb": None, "pc": None, "pd": 9}, saved


async def test_AT_2304_an_unarchived_project_never_ties_a_rank(tmp_path, frozen):
    """AT-2304 (US-2303): every shown project ranked in view 3, Customer Portal
    archived, the others re-ranked (one onto its old rank), Customer Portal
    unarchived: view 3 lists it after every other ranked project and no two
    projects share a rank. The selection on the round's cursor task is set-up
    (qa QA-10), as `_Show.open` sets it for every presentation node."""
    s = _Show(tmp_path, (160, 45))
    async with s.app.run_test(size=s.size) as pilot:
        await s.open(pilot)
        await s.press(pilot, "3", "shift+down", "escape")
        assert all(isinstance(p.get("present_rank"), int) for p in s.projects().values())
        await s.press(pilot, "P", "down", "x", "tab", "enter", "escape")
        assert s.projects()["pcp"]["archived"] is True
        await s.press(pilot, "R", "3", "shift+down", "escape")
        await s.press(pilot, "P", "down", "x", "escape")
        assert s.projects()["pcp"].get("archived", False) is False
        await s.press(pilot, "R", "3")
        tl = "\n".join(_timeline(s.frame()))
    ranks = {k: p.get("present_rank") for k, p in s.projects().items()}
    assert len(set(ranks.values())) == len(ranks), ranks
    assert ranks["pcp"] == max(ranks.values()), ranks
    shown = [n for n in ("Customer Portal", "Billing Migration", "Mobile Release 3.2",
                         "Data Platform", "Brand Refresh") if "■ " + n in tl]
    assert "Customer Portal" in shown, tl
    pos = {n: tl.index("■ " + n) for n in shown}
    assert all(pos["Customer Portal"] > pos[n] for n in shown if n != "Customer Portal"), pos
