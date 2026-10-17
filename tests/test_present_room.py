"""The presentation speaks to the room (batch 2026-10-16-batch-01, increment 004).

HLR-1601 / LLR-1601.1 · HLR-1001 frame · TC-1608.

Why these matter: `R`'s frame is put on a meeting room's screen and `x` exports
that same frame as the file people keep. The operator's verdict of 2026-10-17 on
the shipped frame:

- the header's ` — hybrid` suffix is the prototype round's working name, and the
  in-frame `←→ move the cursor · the cursor'd task's notes expand` row speaks to
  the presenter, not the audience. Both reached the export. The hint row BELOW
  the frame already carries the keys, so the frame carries neither;
- the tick row's label `Mondays · 1 day = 2 cells` names the axis scale, which
  means nothing to a meeting, while the bright dates on that same row belong to
  the selected task. The label names what those dates are: `selected task ▸`
  ("cursor" is engineer jargon). With nothing selected the label is blank: the
  operator removed the scale everywhere on 2026-10-17 («No agrega valor»;
  HLR-1701, batch 2026-10-17-batch-01, `tests/test_tick_label.py`).
"""
from __future__ import annotations

import re

import pytest

import present_board as pb
from taskboard import views

SIZES = [(118, 30), (80, 24)]
PRESENTER_WORDS = ("hybrid", "cursor", "move the", "←→", "notes expand")


def _rows(b, w, h, cursor=pb.CURSOR):
    return views.render_present(b, pb.PROJECT_ID, cursor, pb.TODAY, w, h).plain.split("\n")


def _label(b, w, h, cursor):
    return _rows(b, w, h, cursor)[2][:views._present_cols(w, w >= 100)[0]].strip()


def _is_scale_text(label: str) -> bool:
    """The shape the removed scale label had — `<cadence> · <n> cell…` or
    `<cadence> · <k> d/cell` — written from that rule, not from a renderer."""
    return re.search(r"(?:daily|Mondays|1st/15th|1st) · |\bd/cell\b|\bcells?\b", label) is not None


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1608_the_frame_and_its_export_hold_no_presenter_text(tmp_path, w, h):
    """TC-1608 (a): no ` — hybrid`, no key hint, no `cursor` — in the frame and in
    the SVG `x` writes from it. The positive controls prove the export's text is
    readable by the same probe."""
    b = pb.build(tmp_path / "board.json")
    text = views.render_present(b, pb.PROJECT_ID, pb.CURSOR, pb.TODAY, w, h)
    frame = text.plain
    assert frame.split("\n")[0].startswith("◆ PRESENT · Website Redesign  ")
    svg = views.save_present_svg(text, tmp_path / "p.svg", w, h).read_text(encoding="utf-8")
    assert "PRESENT" in svg and "Redesign" in svg and "selected" in svg, "probe cannot read the SVG"
    for word in PRESENTER_WORDS:
        assert word not in frame, (word, w)
        assert word not in svg, (word, w)


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1608_the_tick_row_names_the_selected_task(tmp_path, w, h):
    """TC-1608 (b): on the oracle board the echo fits at both sizes, so the label
    reads `selected task ▸` in the echo's tone (`tw3` is past due: over), bold —
    and the dates it names are on that row."""
    b = pb.build(tmp_path / "board.json")
    assert _label(b, w, h, pb.CURSOR) == "selected task ▸"
    proj = b.project_by_id(pb.PROJECT_ID)
    open_t, _ = views.present_tasks(b, pb.PROJECT_ID)
    label_w, chip_w, field_w = views._present_cols(w, w >= 100)
    ax = views._present_axis(b, proj, open_t, field_w, pb.TODAY)
    p = views._PresentGeo(w, label_w, chip_w, field_w, ax, set(views.critical_chain(b)),
                          pb.TODAY, w >= 100, proj.color)
    _m, ticks = views._present_ruler(proj, b, p, b.task_by_id(pb.CURSOR))
    assert ticks.startswith("[b " + views.HEX["over"] + "]"), ticks[:40]
    assert "Sep 24" in _rows(b, w, h)[2]


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1608_no_selected_task_ever_gets_the_scale_label(tmp_path, w, h):
    """TC-1608 (c): every open task in turn as the selection, plus one with no
    dates — the label is never the scale text; it names the selected task, or
    carries the echo's own dates when they did not fit the field, or says the
    task has none. With nothing selected — which `render_present` reaches only
    when the project has no open task, the arm driven here — the label is
    blank: the scale is gone everywhere (HLR-1701, batch 2026-10-17-batch-01)."""
    b = pb.build(tmp_path / "board.json")
    assert _is_scale_text("Mondays · 1 day = 2 cells") and _is_scale_text("Mondays · .5 d/cell")
    assert not _is_scale_text("cancelled") and not _is_scale_text("no start · due Oct 6 ▸")
    open_t, _ = views.present_tasks(b, pb.PROJECT_ID)
    for t in open_t:
        label = _label(b, w, h, t.id)
        assert not _is_scale_text(label), (t.id, label)
        assert label.endswith("▸"), (t.id, label)

    nodate = open_t[0]
    nodate.start_date = nodate.due_date = None
    assert _label(b, w, h, nodate.id) == "selected: no dates"

    for t in b.tasks:
        if t.project_id == pb.PROJECT_ID:
            t.phase = "Done"
    assert _label(b, w, h, None) == "", "no selection paints a label"


def test_TC_1608_an_echo_too_long_keeps_its_own_dates(tmp_path):
    """TC-1608 (d): the fallback is unchanged — a selection spanning the whole
    field leaves its dates no room on the row, so the label carries them."""
    b = pb.build(tmp_path / "board.json")
    b.task_by_id("tw6").start_date = "2026-09-01"
    for w, h in SIZES:
        assert _label(b, w, h, "tw6") == "Sep 1 → Oct 14 ▸", w
