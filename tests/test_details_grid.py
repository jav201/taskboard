"""The task details' info grid paints its fields (batch 2026-10-02-batch-04, US-403).

Field report (BACKLOG, pre-existing; diagnosed at P1, P-5/P-9): `enter` on a task
painted the details view with its Project / Phase / Priority / Start / Due rows
BLANK — textual 8.2.8 sizes an auto-height grid row to the Label's one-line content
and `.modal-grid Label { margin-top: 1 }` consumed it, so every cell got 0 rows.

Law (HLR-403, LLR-403.1): in the details view each label and its value paint on one
row, value beside label, the five in order; a value wider than its column wraps
under itself (never cut); the edit modals' grids keep their geometry. RED on the
pre-fix stylesheet: 0-row cells, nothing painted.
"""
from __future__ import annotations

import pytest

from taskboard.app import TaskboardApp
from taskboard.modals import ClockModal, ProjectModal, TaskDetails
from taskboard.models import Board, Project, Task

# the 89-character name `evidence/p1_grid_threshold.py` measured (P-14), with spaces
LONG = ("Website relaunch for the northern region customer portal and partner "
        "onboarding phase two")
FIELDS = ["Project", "Phase", "Priority", "Start", "Due"]


def _app(tmp_path, name="Alpha", **task) -> TaskboardApp:
    b = Board.load(tmp_path / "board.json")
    b.projects.clear()
    b.tasks.clear()
    p = Project(name, "sky")
    b.projects.append(p)
    b.tasks.append(Task(task.pop("title", "Write the spec"), p.id, task.pop("phase", "Doing"),
                        priority=task.pop("priority", "high"),
                        start_date=task.pop("start_date", "2026-10-01"),
                        due_date=task.pop("due_date", "2026-10-09"), **task))
    b.save()
    return TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)


async def _details(app, pilot):
    await pilot.pause()
    app.selected_task_id = app.board.tasks[0].id
    await pilot.press("enter")
    for _ in range(4):
        await pilot.pause()
    assert isinstance(app.screen, TaskDetails)


def _rows(app):
    """The painted rows inside #details-box, with their screen y, border cut off."""
    box = app.screen.query_one("#details-box").region
    strips = app.screen._compositor.render_strips(app.screen.size)
    return [(y, strips[y].text[box.x + 1:box.x + box.width - 1])
            for y in range(box.y, box.y + box.height)]


def _grid_cells(app):
    return list(app.screen.query_one("#details-box .modal-grid").children)


@pytest.mark.parametrize("size", [(140, 40), (80, 24)])
async def test_TC_411_every_grid_cell_paints_on_its_labels_row(tmp_path, size):
    """TC-411 (LLR-403.1). Every info-grid cell is at least one row; each value
    cell starts on its label's row, right of it; the five labels on consecutive
    rows (short values). RED on the pre-fix stylesheet: every cell 0 rows."""
    app = _app(tmp_path)
    async with app.run_test(size=size) as pilot:
        await _details(app, pilot)
        cells = _grid_cells(app)
        assert len(cells) == 10
        assert all(c.region.height >= 1 for c in cells), [c.region.height for c in cells]
        labels, values = cells[0::2], cells[1::2]
        assert [str(w.render()) for w in labels] == FIELDS
        for lab, val in zip(labels, values):
            assert val.region.y == lab.region.y and val.region.x > lab.region.x
        ys = [w.region.y for w in labels]
        assert ys == list(range(ys[0], ys[0] + 5)), ys


@pytest.mark.parametrize("size, rows", [((140, 40), 2), ((80, 24), 2)])
async def test_TC_411_a_long_value_wraps_under_itself(tmp_path, size, rows):
    """TC-411 (LLR-403.1, UX-1). The 89-character project name's cell is taller
    than one row (2 at both sizes with the 10-cell label column, A-7; P-14
    measured 2 / 3 with the 20-cell one) while its label is one row, and the next
    label sits on the row after the value's last row. RED on `height: 1` (the
    value cut) and on the pre-fix stylesheet."""
    app = _app(tmp_path, name=LONG)
    async with app.run_test(size=size) as pilot:
        await _details(app, pilot)
        cells = _grid_cells(app)
        assert (cells[0].region.height, cells[1].region.height) == (1, rows)
        assert cells[2].region.y == cells[1].region.y + rows


@pytest.mark.parametrize("screen, base", [
    (lambda b: ProjectModal(b.projects[0]), [2, 3, 2, 3, 2, 3, 2, 3, 2, 3]),
    (lambda b: ClockModal("Tokyo", "London"), [2, 3, 2, 3]),
])
async def test_TC_411_the_edit_modals_keep_their_grid(tmp_path, screen, base):
    """TC-411 (LLR-403.1), a regression PIN: the rule is scoped to the details
    view, so the edit modals' grids keep the cell heights the base painted (P-14,
    `evidence/p1-grid-threshold.txt`). RED if the rule leaks to `.modal-grid`."""
    app = _app(tmp_path)
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        app.push_screen(screen(app.board))
        for _ in range(3):
            await pilot.pause()
        heights = [w.region.height for w in app.screen.query_one(".modal-grid").children]
    assert heights == base


@pytest.mark.parametrize("size", [(140, 40), (80, 24)])
async def test_TC_420_one_blank_row_above_the_title_and_one_below(tmp_path, size):
    """TC-420 (LLR-403.1, UX-3). Field report: the operator's verdict on the
    increment-003 captures (2026-10-04) — the details title sat under two blank rows
    and right on top of `Project`. Law: one blank row between the box's top border
    and the title, one between the title and the `Project` row; the row moved, none
    added. Read from the painted rows. The rule is the details view's alone: the
    `ProjectModal` title stays 2 rows under its border. RED on increment 003's
    stylesheet (2 above, 0 below) and on the title rule widened to every modal."""
    app = _app(tmp_path)
    async with app.run_test(size=size) as pilot:
        await _details(app, pilot)
        rows = _rows(app)[1:]
        text = [t.strip() for _, t in rows]
        title = next(i for i, t in enumerate(text) if t.startswith("Write the spec"))
        project = next(i for i, t in enumerate(text) if t.startswith("Project "))
        assert (title, project - title - 1) == (1, 1), (title, project, text[:project + 1])
        assert text[0] == "" and text[title + 1] == ""
        # the rule is the details view's alone: an edit modal's title keeps its two
        # rows above (code review F1 of increment 004 — RED on `.modal .modal-title`)
        app.pop_screen()
        app.push_screen(ProjectModal(app.board.projects[0]))
        for _ in range(3):
            await pilot.pause()
        other = app.screen.query_one(".modal-title")
        box = other.parent
        assert other.region.y - (box.region.y + 1) == 2, (other.region, box.region)


@pytest.mark.parametrize("size", [(140, 40), (80, 24)])
async def test_TC_421_the_label_column_is_ten_cells(tmp_path, size):
    """TC-421 (LLR-403.1, UX-4). Field report: the operator's verdict (2026-10-04) —
    a 20-cell label column left a wide gap and wrapped the long project name over 3
    rows at 80x24. Law: in the details view each value starts 11 cells right of its
    label (a 10-cell column and the 1-cell gutter), read from the PAINTED rows with
    the 89-character name, and the five labels stay painted in order; the edit
    modals keep their 20-cell column (`ProjectModal`: 21). RED on increment 003's
    stylesheet (21)."""
    app = _app(tmp_path, name=LONG)
    async with app.run_test(size=size) as pilot:
        await _details(app, pilot)
        text = [t for _, t in _rows(app)]
        offsets = []
        for lab in FIELDS:
            row = next(t for t in text if t.strip().startswith(lab + " "))
            at = row.index(lab)
            offsets.append(len(row) - len(row[at + len(lab):].lstrip()) - at)
        assert offsets == [11] * 5, offsets
        assert [t.strip().split(" ")[0] for t in text
                if t.strip().split(" ")[0] in FIELDS] == FIELDS
        app.pop_screen()
        app.push_screen(ProjectModal(app.board.projects[0]))
        for _ in range(3):
            await pilot.pause()
        cells = list(app.screen.query_one(".modal-grid").children)
        assert cells[1].region.x - cells[0].region.x == 21


async def test_AT_406_the_details_view_shows_its_five_fields(tmp_path):
    """AT-406 (US-403, HLR-403). Through `enter` on a high-priority task: at 140x40
    and 80x24 the details view PAINTS each label with its value on the same row,
    in order; at 80x24 the 89-character project name is painted whole across the
    value column — every continuation row's first character at the value column,
    `Phase` on the row after it — and with the box at the top all five fields are
    inside the visible box. Boundary arms: an Inbox task (`Inbox`), no dates (`—`)
    and a blocked task (`Doing · blocked`). RED on the pre-fix stylesheet: none of
    the five labels is painted."""
    failures = []
    cases = [
        ((140, 40), {}, [("Project", "Alpha"), ("Phase", "Doing"), ("Priority", "high"),
                         ("Start", "2026-10-01"), ("Due", "2026-10-09")]),
        ((80, 24), {"name": LONG}, None),
        ((80, 24), {"start_date": None, "due_date": None, "blocked": True},
         [("Project", "Alpha"), ("Phase", "Doing · blocked"), ("Priority", "high"),
          ("Start", "—"), ("Due", "—")]),
        ((80, 24), {"inbox": True},
         [("Project", "Inbox"), ("Phase", "Doing"), ("Priority", "high"),
          ("Start", "2026-10-01"), ("Due", "2026-10-09")]),
    ]
    for n, (size, kw, want) in enumerate(cases):
        inbox = kw.pop("inbox", False)
        where = tmp_path / f"case{n}"
        where.mkdir()
        app = _app(where, **kw)
        async with app.run_test(size=size) as pilot:
            if inbox:
                app.board.tasks[0].project_id = None
            await _details(app, pilot)
            rows = _rows(app)
            text = [t for _, t in rows]
            if want:
                lines = [next((t for t in text if t.strip().startswith(lab + " ")), None)
                         for lab, _ in want]
                got = [ln.split(None, 1) if ln else None for ln in lines]
                if any(g is None for g in got) or \
                        [(lab, " ".join(val.split())) for lab, val in got] != want:
                    failures.append((size, kw, got))
                ys = [next((y for y, t in rows if t.strip().startswith(lab + " ")), -1)
                      for lab, _ in want]
                if ys != sorted(ys) or -1 in ys:
                    failures.append((size, kw, "order", ys))
            else:
                start = next((i for i, t in enumerate(text) if t.strip().startswith("Project ")), None)
                phase = next((i for i, t in enumerate(text) if t.strip().startswith("Phase ")), None)
                if start is None or phase is None:
                    failures.append((size, "long: labels not painted"))
                else:
                    col = text[start].index("Website")
                    chunk = text[start:phase]
                    joined = " ".join(" ".join(t[col:].split()) for t in chunk)
                    conts_ok = all(t[:col].strip() == "" and t[col] != " " for t in chunk[1:])
                    # all five labels PAINTED inside the box, in order: rows come from
                    # the box, so a field cut off simply has no row (code review F1 of
                    # increment 003 — the old "every painted row is inside" was vacuous;
                    # RED at 80x12, evidence/inc003-f1-red.txt)
                    visible = [t.strip().split(" ")[0] for _, t in rows
                               if t.strip().split(" ")[0] in FIELDS] == FIELDS
                    if joined != " ".join(LONG.split()) or not conts_ok or len(chunk) < 2 \
                            or not visible:
                        failures.append((size, "long", joined, conts_ok, len(chunk), visible))
    assert not failures, failures
