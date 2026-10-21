"""The suite's hygiene law — batch 2026-10-20-batch-02: HLR-2306 / LLR-2306.1,
LLR-2306.2 · TC-2306 · AT-2306 (US-2304). A test that reads private state passes
while the screen is wrong; a dead parameter or import hides what a caller means."""
from __future__ import annotations

import inspect

from taskboard.modals import ProjectPicker


def test_TC_2306_move_target_takes_the_project_and_the_board():
    """TC-2306 (LLR-2306.1): `_move_target` reads no picker copy of the boards
    (code review N2 of 2026-10-20-batch-01); the target is read when chosen."""
    assert list(inspect.signature(ProjectPicker._move_target).parameters) == \
        ["self", "proj", "bid"]
