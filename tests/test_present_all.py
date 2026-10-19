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
                            mine = views.present_tasks(board, cur_p)[0]
                            assert all(("task", t.id) in r.stops for t in mine), (name, cur_p)
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
