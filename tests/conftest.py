"""Suite-wide test seam (batch 2026-10-04-batch-02, D-611, §5 of its requirements).

The one-time milestone offer is a modal at app start: 274 of the suite's 541 app starts hold a
candidate (P-9) and would open it, so their keys would land on the offer instead of the view
under test. Every test therefore starts as if its board had ALREADY answered the offer — the
app module's own `milestones_marked` reference answers True — unless the test carries the
marker `milestone_offer`. The base suite's file I/O is unchanged (no offer write at mount); the
offer's own tests carry the marker; `tests/test_milestone_offer_seam.py` holds the two
controls that prove the seam both ways.
"""
import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "milestone_offer: the test drives the one-time milestone offer at app start")


@pytest.fixture(autouse=True)
def _milestone_offer_seam(request, monkeypatch):
    if request.node.get_closest_marker("milestone_offer") is None:
        monkeypatch.setattr("taskboard.app.milestones_marked", lambda settings: True)
