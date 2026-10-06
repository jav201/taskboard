"""P1 census (C-39) — how many app-started test boards would open the one-time milestone offer.

A pytest plugin, loaded with `-p`: it wraps `TaskboardApp.on_mount` and, for every app the suite
starts, records the test id and the board's candidates by the offer's rule (open = not in the last
phase and not archived; not already flagged; a due date; group 1 start == due, group 2 no start).
Run from the repo root:
    python -m pytest -q -p no:cacheprovider -p p1_offer_census  (with this directory on PYTHONPATH)
Writes `p1-offer-census.json` beside itself. Product code is untouched; tests run unchanged."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

OUT = Path(__file__).with_name("p1-offer-census.json")
ROWS: list[dict] = []
_CURRENT = {"node": None}


def _candidates(board):
    g1 = g2 = 0
    for t in board.tasks:
        if board.is_done(t) or t.archived or t.extra.get("milestone") is True or not t.due_date:
            continue
        if t.start_date == t.due_date:
            g1 += 1
        elif not t.start_date:
            g2 += 1
    return g1, g2


def pytest_configure(config):
    from taskboard.app import TaskboardApp
    real = TaskboardApp.on_mount

    def on_mount(self):
        g1, g2 = _candidates(self.board)
        ROWS.append({"node": _CURRENT["node"], "one_day": g1, "due_only": g2,
                     "fresh": not self.board.path.exists()})
        return real(self)

    TaskboardApp.on_mount = on_mount


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    _CURRENT["node"] = item.nodeid
    yield


def pytest_sessionfinish(session, exitstatus):
    starts = len(ROWS)
    any_c = [r for r in ROWS if r["one_day"] or r["due_only"]]
    g1 = [r for r in ROWS if r["one_day"]]
    summary = {
        "app_starts": starts,
        "starts_with_any_candidate": len(any_c),
        "starts_with_a_one_day_candidate": len(g1),
        "tests_with_any_candidate": len({r["node"] for r in any_c}),
        "tests_starting_an_app": len({r["node"] for r in ROWS}),
        "files_with_any_candidate": sorted({str(r["node"]).split("::")[0] for r in any_c}),
    }
    OUT.write_text(json.dumps({"summary": summary, "rows": ROWS}, indent=1), encoding="utf-8")
    print("\nOFFER CENSUS", json.dumps(summary))
