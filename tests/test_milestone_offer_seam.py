"""The suite's milestone-offer seam, proved both ways (batch 2026-10-04-batch-02, D-611).

Law: a test WITHOUT the `milestone_offer` marker starts the app on a board holding candidates
and sees no offer and no write by the offer step; a test WITH it sees the offer. If either
control goes RED, the seam either hides the offer from the tests that own it or lets it land
on the 274 starts it exists to protect (P-9).
"""
from __future__ import annotations

from datetime import date

import pytest

import kg_board
from taskboard.app import TaskboardApp
from taskboard.modals import MilestoneOffer

RENUMBER = "seen_view_renumber_2026_07"


def _one_day_board(tmp_path):
    path = tmp_path / "board.json"
    b = kg_board.one_day(kg_board.shifted(path), date.today())
    b.settings[RENUMBER] = True
    b.save()
    return path


async def test_seam_unmarked_starts_see_no_offer_and_no_offer_write(tmp_path):
    """An unmarked test: no `MilestoneOffer`, and the board file is byte-identical
    after start (the offer step wrote nothing). RED: no seam (the offer opens)."""
    path = _one_day_board(tmp_path)
    before = path.read_bytes()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert not isinstance(app.screen, MilestoneOffer)
    assert path.read_bytes() == before


@pytest.mark.milestone_offer
async def test_seam_marked_starts_see_the_offer(tmp_path):
    """A marked test on the same board sees the offer. RED: a seam that ignores the
    marker."""
    path = _one_day_board(tmp_path)
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, MilestoneOffer)
