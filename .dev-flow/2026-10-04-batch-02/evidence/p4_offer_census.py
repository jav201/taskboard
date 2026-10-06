"""Increment 004 census re-run (§5 pass condition, qa Q-9): with the seam in place, how many app
starts hold a candidate on an unmarked board and were SUPPRESSED (no offer), and how many offer
screens opened in nodes WITHOUT the `milestone_offer` marker (must be 0).

A pytest plugin, loaded with `-p` (this directory on PYTHONPATH). It wraps
`TaskboardApp._offer_milestones` and records, per start: the node, whether it carries the
marker, the board's candidates (`models.milestone_candidates`), whether the board is really
marked (`models.milestones_marked`), and whether a `MilestoneOffer` screen was pushed. Writes
`p4-offer-census.json` beside itself. Product code is untouched.

r2 (P4): also writes every row and the P1-comparable count, split by why a start would not
offer even without the seam (a seeded or already-marked board; an unreadable load)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

OUT = Path(__file__).with_name("p4-offer-census.json")
ROWS: list[dict] = []
_CUR = {"node": None, "marked": False}


def pytest_configure(config):
    from taskboard import models
    from taskboard.app import TaskboardApp
    from taskboard.modals import MilestoneOffer
    real = TaskboardApp._offer_milestones

    def wrapped(self):
        cands = models.milestone_candidates(self.board)
        really = models.milestones_marked(self.board.settings)
        unreadable = bool(self.board.load_report.get("file_unreadable"))
        real(self)
        offered = any(isinstance(s, MilestoneOffer) for s in self.screen_stack)
        ROWS.append({"node": _CUR["node"], "marker": _CUR["marked"], "candidates": len(cands),
                     "really_marked": really, "unreadable": unreadable, "offered": offered})

    TaskboardApp._offer_milestones = wrapped


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    _CUR["node"] = item.nodeid
    _CUR["marked"] = item.get_closest_marker("milestone_offer") is not None
    yield


def pytest_sessionfinish(session, exitstatus):
    unmarked = [r for r in ROWS if not r["marker"]]
    suppressed = [r for r in unmarked if r["candidates"] and not r["really_marked"]
                  and not r["unreadable"] and not r["offered"]]
    leaked = [r for r in unmarked if r["offered"]]
    summary = {"app_starts": len(ROWS), "unmarked_starts": len(unmarked),
               "suppressed_starts_with_a_candidate": len(suppressed),
               "suppressed_tests": len({r["node"] for r in suppressed}),
               "offers_in_unmarked_nodes": len(leaked),
               "marked_starts": len(ROWS) - len(unmarked),
               "offers_in_marked_nodes": sum(1 for r in ROWS if r["marker"] and r["offered"]),
               # the P1 census's own measure (any candidate, whatever the mark), split by why
               # no offer would open without the seam (P4 reconciliation with P1's 274)
               "unmarked_starts_with_a_candidate": sum(1 for r in unmarked if r["candidates"]),
               "of_which_seeded_or_really_marked": sum(1 for r in unmarked
                                                       if r["candidates"] and r["really_marked"]),
               "of_which_unreadable": sum(1 for r in unmarked if r["candidates"]
                                          and r["unreadable"] and not r["really_marked"])}
    OUT.write_text(json.dumps({"summary": summary, "leaked": leaked, "rows": ROWS}, indent=1),
                   encoding="utf-8")
    print("\nOFFER CENSUS", json.dumps(summary))
