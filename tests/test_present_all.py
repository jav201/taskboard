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
