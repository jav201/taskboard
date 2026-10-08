"""The chain-template authoring unit layer (batch 2026-10-07-batch-08, increment 001).

HLR-1401 / LLR-1401.1 · AT-1401.

`chain_template(board, task_id)` returns the connected OPEN chain of one task —
every open task of its project reachable through `depends_on` in BOTH directions,
each once — as a `Template`, or None when the task is missing, done or archived.
The emitted order is topological (every `wait` points backward) and deterministic:
by (depth, board order), where depth is the longest `depends_on` path from a chain
head and board order breaks depth ties. A task with several predecessors keeps the
FIRST in that order as its `wait` (the shape holds one link per task, so a fan-in
cannot be represented). Titles and notes are carried verbatim.
"""
from __future__ import annotations

from pathlib import Path

from taskboard.models import Board, Project, Task, chain_template, templates


def _task(title, pid, phase="Doing", deps=(), notes="", archived=False, tid=None):
    t = Task(title, pid, phase, id=tid)
    t.depends_on = list(deps)
    t.notes = notes
    t.archived = archived
    return t


def _board(projects, tasks) -> Board:
    return Board(projects, tasks, Path("board.json"))


def test_both_directions_a_mid_chain_task_saves_the_whole_component():
    """Selecting a MIDDLE task saves the whole component both ways: predecessors
    and dependents, in topological order with each `wait` pointing backward."""
    p = Project("Plat", "sky")
    a = _task("Alpha", p.id, tid="a")
    b = _task("Beta", p.id, deps=("a",), tid="b")
    c = _task("Gamma", p.id, deps=("b",), tid="c")
    d = _task("Delta", p.id, deps=("c",), tid="d")
    board = _board([p], [a, b, c, d])
    tpl = chain_template(board, "c")
    assert [t.title for t in tpl.tasks] == ["Alpha", "Beta", "Gamma", "Delta"]
    assert [t.wait for t in tpl.tasks] == [None, 0, 1, 2]


def test_fan_in_keeps_the_first_predecessor_and_round_trips_as_a_chain():
    """A task with two predecessors keeps ONE `wait` — the first in the order —
    and feeding it back through the store and the insert link builder reproduces
    a CHAIN, not a diamond (no task ends up with two parents)."""
    p = Project("Plat", "sky")
    a = _task("Alpha", p.id, tid="a")
    b = _task("Beta", p.id, tid="b")
    c = _task("Gamma", p.id, deps=("a", "b"), tid="c")
    board = _board([p], [a, b, c])
    tpl = chain_template(board, "c")
    assert [t.title for t in tpl.tasks] == ["Alpha", "Beta", "Gamma"]
    assert [t.wait for t in tpl.tasks] == [None, None, 0]

    # round-trip through the store (the `templates()` seat reads settings back)
    board.settings["templates"] = [{"name": "Fan", "tasks": [
        {"title": one.title,
         **({"notes": one.notes} if one.notes else {}),
         **({"wait": one.wait} if one.wait is not None else {})}
        for one in tpl.tasks]},
    ]
    back = templates(board)[0]
    assert [t.title for t in back.tasks] == ["Alpha", "Beta", "Gamma"]
    assert [t.wait for t in back.tasks] == [None, None, 0]

    # the insert logic's link builder (models mirror of app._on_template_picked):
    # task i waits on created[wait] — so the reproduced graph is a chain.
    parents = [[back.tasks[one.wait].title] if one.wait is not None else []
               for one in back.tasks]
    assert parents == [[], [], ["Alpha"]]
    assert all(len(ps) <= 1 for ps in parents), "a fan-in survived the round-trip"


def test_a_single_unlinked_task_is_the_degenerate_one_task_template():
    """The empty component is allowed: an unlinked task saves a one-task template."""
    p = Project("Plat", "sky")
    a = _task("Lone", p.id, tid="a")
    tpl = chain_template(_board([p], [a]), "a")
    assert [t.title for t in tpl.tasks] == ["Lone"]
    assert [t.wait for t in tpl.tasks] == [None]
    assert [t.notes for t in tpl.tasks] == [""]


def test_none_for_done_archived_and_missing():
    """A done task, an archived task, a missing id and None all return None."""
    p = Project("Plat", "sky")
    done = _task("Done task", p.id, phase="Done", tid="done")
    archived = _task("Archived task", p.id, archived=True, tid="arch")
    board = _board([p], [done, archived])
    assert chain_template(board, "done") is None
    assert chain_template(board, "arch") is None
    assert chain_template(board, "missing") is None
    assert chain_template(board, None) is None


def test_component_stays_within_the_task_project():
    """A link across projects is not traversed: the component is the task's own
    project only, so a cross-project predecessor is dropped."""
    p1 = Project("One", "sky", id="p1")
    p2 = Project("Two", "lime", id="p2")
    a = _task("A", "p1", deps=("b",), tid="a")
    b = _task("B", "p2", tid="b")
    tpl = chain_template(_board([p1, p2], [a, b]), "a")
    assert [t.title for t in tpl.tasks] == ["A"]


def test_done_and_archived_neighbours_are_skipped_not_bridged():
    """A done or archived task in the middle is skipped, so the open tasks beyond
    it are not reachable through it and the component ends there."""
    p = Project("Plat", "sky")
    a = _task("A", p.id, tid="a")
    done = _task("B", p.id, phase="Done", deps=("a",), tid="b")
    c = _task("C", p.id, deps=("b",), tid="c")
    tpl = chain_template(_board([p], [a, done, c]), "a")
    assert [t.title for t in tpl.tasks] == ["A"]


def test_titles_and_notes_are_carried_verbatim():
    """Titles and notes are stored exactly as the tasks carry them."""
    p = Project("Plat", "sky")
    a = _task("Alpha", p.id, notes="first note", tid="a")
    b = _task("Beta", p.id, deps=("a",), notes="", tid="b")
    c = _task("Gamma", p.id, deps=("b",), notes="third", tid="c")
    tpl = chain_template(_board([p], [a, b, c]), "a")
    assert [(t.title, t.notes) for t in tpl.tasks] == \
        [("Alpha", "first note"), ("Beta", ""), ("Gamma", "third")]
