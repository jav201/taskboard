"""The read-only task details view never parses task text as markup.

Security review S1 (2026-09-30, batch 2026-09-30-batch-01): `rich.markup.escape`
only escapes a `[` that RICH would read as a tag, but these widgets are drawn by
Textual, whose markup parser also reads uppercase and space-led brackets. A
note holding `[LINK=http://e]x` raised MarkupError when the details view
(`enter`) opened — the app died — and `[B]x` silently vanished. Notes, titles,
URLs and image paths all reach this view from the board file AND from team
sync, so another person's text could take the app down. The fix builds the
text with Rich (a `Text`), so Textual never parses task text. HLR-005.
"""
from __future__ import annotations

import pytest

from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.modals import ImageViewer, TaskDetails

# the first four from S1 (2026-09-30); the last two are batch 2026-10-02-batch-04's
# contract §1.3 payloads (review F3): `x\\\` (x then three backslashes — an
# escape-then-parse round trip eats them; this substring check sees an eaten or
# altered payload, not a doubled one — exact paint is AT-401's, code review G3) and
# a Rich emoji code plus a Rich tag (a Rich parse turns `:smile:` into 😄)
HOSTILE = ["[LINK=http://e]x", "[B]bold?", "[ red]x", "a[b", "x\\\\\\", ":smile: [b]y[/b]"]


def _app(tmp_path, **fields) -> TaskboardApp:
    b = Board.load(tmp_path / "board.json")
    b.projects.clear()
    b.tasks.clear()
    p = Project(fields.pop("project", "Plain"), "sky")
    b.projects.append(p)
    phase = fields.pop("phase", "Doing")
    if phase not in b.phases:
        b.phases.insert(1, phase)
    b.tasks.append(Task(fields.pop("title", "Plain title"), p.id, phase, **fields))
    b.save()
    return TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)


def _painted(app, box: str | None = None) -> str:
    """The painted screen; with `box`, only the cells inside that widget's
    region — the board behind a modal draws titles and project names too, so
    a whole-screen search would let the background answer for the modal."""
    strips = app.screen._compositor.render_strips(app.screen.size)
    if box is None:
        return "\n".join(s.text for s in strips)
    r = app.screen.query_one(box).region
    return "\n".join(s.text[r.x:r.x + r.width] for s in strips[r.y:r.y + r.height])


async def _open_details(app, pilot):
    await pilot.pause()
    app.selected_task_id = app.board.tasks[0].id
    await pilot.press("enter")
    for _ in range(3):
        await pilot.pause()


@pytest.mark.parametrize("text", HOSTILE)
@pytest.mark.parametrize("where", ["notes", "title", "project", "phase", "url", "image",
                                   "viewer-title"])
async def test_details_show_bracketed_task_text_literally(tmp_path, text, where):
    """AT-007 (HLR-005). Each user-controlled string the details view draws —
    notes, title, project name, phase, URL, image path, and the image viewer's
    title (review F1) — holding a bracket Textual
    would parse: the view opens (no crash) and the text is painted exactly as
    typed. RED on base: MarkupError for `[LINK=…`, vanished text for `[B]…`."""
    fields = {"notes": "", "urls": [], "images": []}
    if where == "notes":
        fields["notes"] = f"before {text} after"
    elif where in ("title", "viewer-title"):
        fields["title"] = text
    elif where == "phase":
        fields["phase"] = text
    elif where == "project":
        fields["project"] = text
    elif where == "url":
        fields["urls"] = [f"https://e.example/{text}"]
    else:
        fields["images"] = [f"img/{text}.png"]
    app = _app(tmp_path, **fields)
    async with app.run_test(size=(140, 40)) as pilot:
        if where == "viewer-title":           # the image viewer, `i` (review F1)
            await pilot.pause()
            app.selected_task_id = app.board.tasks[0].id
            await pilot.press("i")
            for _ in range(3):
                await pilot.pause()
            assert isinstance(app.screen, ImageViewer), "the image viewer did not open"
        else:
            await _open_details(app, pilot)
            assert isinstance(app.screen, TaskDetails), "the details view did not open"
        # the project and phase fields are read off the PAINTED screen too since the
        # details grid paints its cells (batch 2026-10-02-batch-04, HLR-403)
        box = "#viewer-box" if where == "viewer-title" else "#details-box"
        assert text in _painted(app, box), f"{where}: {text!r} not painted literally"


async def test_details_still_highlight_the_notes(tmp_path):
    """Preservation: the fix must not cost the highlight — `!!…!!` is still
    painted red, markers hidden. GREEN on base; RED under the mutation
    "escape the whole note as plain text"."""
    from taskboard.views import HEX
    app = _app(tmp_path, notes="keep !!this red!! please")
    async with app.run_test(size=(140, 40)) as pilot:
        await _open_details(app, pilot)
        hits = [seg for strip in app.screen._compositor.render_strips(app.screen.size)
                for seg in strip if "this red" in seg.text]
        assert hits and all(s.style.color.triplet.hex.lower() == HEX["over"] for s in hits)
        assert "!!this" not in _painted(app, "#details-box")
