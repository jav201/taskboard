"""The suite's hygiene law — batch 2026-10-20-batch-02: HLR-2306 / LLR-2306.1,
LLR-2306.2 · TC-2306 · AT-2306 (US-2304). A test that reads private state passes
while the screen is wrong; a dead parameter or import hides what a caller means."""
from __future__ import annotations

import ast
import inspect
from pathlib import Path

from taskboard.modals import ProjectPicker

TESTS = Path(__file__).resolve().parent


def test_TC_2306_move_target_takes_the_project_and_the_board():
    """TC-2306 (LLR-2306.1): `_move_target` reads no picker copy of the boards
    (code review N2 of 2026-10-20-batch-01); the target is read when chosen."""
    assert list(inspect.signature(ProjectPicker._move_target).parameters) == \
        ["self", "proj", "bid"]


def _unread_names(path: Path) -> list[str]:
    """Names a module binds by an import or a plain module-level assignment and
    never reads (its `test_*` functions and fixtures are pytest's to read)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    bound = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                name = (a.asname or a.name).split(".")[0]
                if name != "annotations":
                    bound.append(name)
        elif isinstance(node, ast.Assign):
            bound += [t.id for t in node.targets if isinstance(t, ast.Name)]
    read = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    read |= {n.value.id for n in ast.walk(tree)
             if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    return [n for n in bound if n not in read]


def test_AT_2306_the_hygiene_law():
    """AT-2306 (US-2304): `_move_target(proj, bid)`; no test reads Textual's private
    border title; `tests/test_boards_forms.py` binds nothing it never reads."""
    assert list(inspect.signature(ProjectPicker._move_target).parameters) == \
        ["self", "proj", "bid"]
    needle = "._border" + "_title"            # built, so this file is not a hit itself
    hits = [p.name for p in sorted(TESTS.glob("*.py")) if needle in p.read_text(encoding="utf-8")]
    assert hits == [], hits
    assert _unread_names(TESTS / "test_boards_forms.py") == []
