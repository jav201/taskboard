"""The colour ration — Prism increment 1.

WHY THIS FILE EXISTS: a hue in this app has exactly one job. A project hue NAMES
(which project this is); `over` and `soon` JUDGE (overdue / due today); `accent`
CALLS ATTENTION (today, focus, keys). Before the ration, `amber` was a project
colour AND the due-today colour at the identical hex — the same mark meaning two
things in all five views.

Every law below MEASURES the palette (euclidean rgb over `views.HEX`). None of
them reads a list of forbidden names, so re-adding a colliding hue to
`PROJECT_COLORS` turns them red no matter what it is called.
"""

import json
from datetime import date
from itertools import permutations

from taskboard.models import (DROPPED_PROJECT_COLORS, PROJECT_COLORS, Board,
                              Project, Task, project_color_on_load)
from taskboard.views import HEX, card_cell, render_view

# The reserved hues and the exclusion band each one owns. `over`/`soon` JUDGE, so
# they get the wide band; `accent` only calls attention, so it gets a narrower
# one; `done` (#3f9c6d) tints a ✓ glyph, never a field, and claims no band.
BANDS = {"over": 70.0, "soon": 70.0, "accent": 55.0}


def _rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def dist(a: str, b: str) -> float:
    """Euclidean rgb distance — the metric the audit measured the collision with
    (`_tui_prism_proposal/audit_capture.py`), kept identical so the numbers in
    the code comments can be checked against the ones in the proposal."""
    return sum((x - y) ** 2 for x, y in zip(_rgb(a), _rgb(b))) ** 0.5


# --------------------------------------------------------------------------- #
# AC1 — the ration itself
# --------------------------------------------------------------------------- #
def test_no_project_hue_stands_inside_a_reserved_band():
    """The law. A hue that names must not be confusable with a hue that judges,
    or the mark cannot be read: is that amber spine telling me WHICH project, or
    that something is due TODAY? Measured, per reserved hue, with its own band."""
    for name in PROJECT_COLORS:
        for reserved, band in BANDS.items():
            d = dist(HEX[name], HEX[reserved])
            assert d >= band, (
                f"project hue {name} {HEX[name]} is {d:.1f} from {reserved} "
                f"{HEX[reserved]} — band is {band}")


def test_the_palette_is_eight_distinct_offered_hues():
    assert len(PROJECT_COLORS) == len(set(PROJECT_COLORS)) == 8


def test_each_dropped_hue_was_dropped_because_it_measured_inside_a_band():
    """The four retirements are law-backed, not taste. Each one still has a hex
    in the palette table, and each one violates the same law the survivors pass
    — so this test would fail if someone retired a hue that was actually fine."""
    for name in DROPPED_PROJECT_COLORS:
        violations = [(r, dist(HEX[name], HEX[r]))
                      for r, band in BANDS.items() if dist(HEX[name], HEX[r]) < band]
        assert violations, f"{name} was dropped but measures lawful — why is it gone?"


def test_amber_is_literally_the_due_today_hue():
    """The collision that started this: distance ZERO, not 'close'."""
    assert dist(HEX["amber"], HEX["soon"]) == 0.0
    assert "amber" not in PROJECT_COLORS


# --------------------------------------------------------------------------- #
# AC2 — the remap
# --------------------------------------------------------------------------- #
def test_remap_is_the_unique_minimal_injective_assignment():
    """WHY injective: the identity hue's whole job is telling projects apart.
    Plain nearest-hue would send BOTH amber and orange to lime, so two projects
    the user had made different would come back identical. Among all injective
    maps we take the one with the smallest total rgb distance — a rule that can
    be recomputed here from the palette rather than trusted."""
    dropped = tuple(DROPPED_PROJECT_COLORS)
    scored = sorted((sum(dist(HEX[a], HEX[b]) for a, b in zip(dropped, combo)), combo)
                    for combo in permutations(PROJECT_COLORS, len(dropped)))
    best_total, best_combo = scored[0]
    assert best_total < scored[1][0], "the optimum must be unique to be a rule"
    assert dict(zip(dropped, best_combo)) == DROPPED_PROJECT_COLORS


def test_remap_targets_are_lawful_and_terminal():
    """Every target is an offered hue, and no target is itself a remap key —
    that is what makes a second load a no-op instead of another hop."""
    targets = list(DROPPED_PROJECT_COLORS.values())
    assert len(set(targets)) == len(targets)                     # injective
    for src, dst in DROPPED_PROJECT_COLORS.items():
        assert dst in PROJECT_COLORS
        assert dst not in DROPPED_PROJECT_COLORS
        assert src not in PROJECT_COLORS


def test_old_boards_load_with_a_lawful_colour():
    assert Project.from_dict({"name": "A", "color": "amber"}).color == "lime"
    assert Project.from_dict({"name": "B", "color": "rose"}).color == "pink"
    assert Project.from_dict({"name": "C", "color": "cyan"}).color == "sky"
    assert Project.from_dict({"name": "D", "color": "orange"}).color == "fuchsia"
    assert Project.from_dict({"name": "E", "color": "violet"}).color == "violet"
    assert Project.from_dict({"name": "F", "color": "nonsense"}).color == "violet"
    assert Project.from_dict({"name": "G"}).color == "violet"


def test_remap_is_a_fixed_point():
    """Applying the migration twice changes nothing the second time."""
    for src in DROPPED_PROJECT_COLORS:
        once = project_color_on_load(src)
        assert project_color_on_load(once) == once


# --------------------------------------------------------------------------- #
# AC3 / AC4 — what the migration does to a file on disk
# --------------------------------------------------------------------------- #
def _write_board(path, colors) -> None:
    path.write_text(json.dumps({
        "phases": ["Backlog", "Doing", "Done"],
        "projects": [{"id": f"p{i}", "name": f"P{i}", "color": col}
                     for i, col in enumerate(colors)],
        "tasks": [],
        "settings": {},
    }, indent=2), encoding="utf-8")


def test_a_legacy_board_migrates_once_and_then_never_moves(tmp_path):
    """AC3. Load-save-load-save on a board carrying all four retired hues: the
    first save migrates, and every save after it is byte-identical. A migration
    that oscillated would rewrite the user's file on every single launch."""
    p = tmp_path / "legacy.json"
    _write_board(p, ["amber", "rose", "cyan", "orange"])

    Board.load(p).save()
    after_first = p.read_bytes()
    Board.load(p).save()
    assert p.read_bytes() == after_first
    Board.load(p).save()
    assert p.read_bytes() == after_first

    colors = [pr.color for pr in Board.load(p).projects]
    assert colors == ["lime", "pink", "sky", "fuchsia"]
    assert len(set(colors)) == 4          # four projects, still four colours


def test_a_board_with_no_retired_hue_is_left_byte_identical(tmp_path):
    """AC4. The migration must be invisible to everyone it does not concern."""
    p = tmp_path / "clean.json"
    _write_board(p, list(PROJECT_COLORS))
    Board.load(p).save()                  # normalise to the app's own writer
    before = p.read_bytes()
    Board.load(p).save()
    assert p.read_bytes() == before
    assert [pr.color for pr in Board.load(p).projects] == list(PROJECT_COLORS)


# --------------------------------------------------------------------------- #
# AC5 — high priority lives in the glyph house
# --------------------------------------------------------------------------- #
def _board(tmp_path, color="lime"):
    b = Board.load(tmp_path / "b.json")
    b.projects.clear()
    b.tasks.clear()
    p = Project("Alpha", color)
    b.projects.append(p)
    return b, p


def test_high_priority_is_a_glyph_and_wears_no_judging_hue(tmp_path):
    """The marker used to be ◉ painted in #fbbf24 — the due-today hue worn by a
    fact about IMPORTANCE, which is not urgency. Now the shape carries it."""
    b, p = _board(tmp_path)
    b.add_task(Task("Urgent thing", p.id, "Backlog", "high"))
    markup = card_cell(b.tasks[0], b, 30, False)
    assert "!" in markup
    assert "◉" not in markup
    assert HEX["soon"] not in markup          # #fbbf24 is never worn by priority
    assert HEX["over"] not in markup


def test_a_normal_or_finished_task_carries_no_priority_mark(tmp_path):
    """Unchanged behaviour, restated on the new glyph: the mark is the exception
    the eye must find, so it may not appear on ordinary or finished work."""
    b, p = _board(tmp_path)
    b.add_task(Task("Ordinary", p.id, "Backlog", "normal"))
    b.add_task(Task("Finished", p.id, "Done", "high"))
    assert "!" not in card_cell(b.tasks[0], b, 30, False)
    assert "!" not in card_cell(b.tasks[1], b, 30, False)


def _styles(text) -> list[tuple[str, str]]:
    """(style, covered text) for every coloured span of a rendered view."""
    return [(str(s.style), text.plain[s.start:s.end]) for s in text.spans]


VIEWS = ("swimlanes", "columns", "agenda", "gantt", "kanban")


def _crowded(tmp_path):
    """One board carrying every offered hue plus work in all three urgency
    states, so the judging hues really do get painted somewhere."""
    b, p = _board(tmp_path)
    for i, col in enumerate(PROJECT_COLORS):
        b.projects.append(Project(f"P{i}", col))
    b.add_task(Task("Urgent thing", p.id, "Backlog", "high"))
    b.add_task(Task("Plain thing", p.id, "Doing", "normal"))
    b.add_task(Task("Late thing", p.id, "Doing", "normal", due_date="2026-07-20"))
    b.add_task(Task("Today thing", p.id, "Doing", "normal", due_date="2026-07-30"))
    return b


def test_no_view_paints_an_identity_in_a_retired_hue(tmp_path):
    """The ration is why this increment touches all five views: `cyan`, `rose`
    and `orange` are gone from the screen entirely. (`amber` cannot be checked
    this way — its hex IS the due-today hex, which is the whole complaint; the
    test below checks it by provenance instead.)"""
    b = _crowded(tmp_path)
    retired = {n: HEX[n] for n in DROPPED_PROJECT_COLORS if HEX[n] != HEX["soon"]}
    assert len(retired) == 3
    for mode in VIEWS:
        out = render_view(mode, b, False, None, date(2026, 7, 30), width=100, height=30)
        painted = " ".join(style for style, _ in _styles(out))
        for name, hexv in retired.items():
            assert hexv not in painted, f"{mode} still paints {name} {hexv}"


def test_a_judging_hue_is_never_worn_by_a_name_or_a_priority_mark(tmp_path):
    """Prism's law, checked by PROVENANCE rather than by colour count: `soon`
    and `over` may be worn by facts about time (a chip, a count, a heat glyph),
    never by something that says WHICH project or HOW important. This is the
    check that catches a regression a hex census cannot — `amber` the identity
    and `soon` the judgment are the same six characters."""
    b = _crowded(tmp_path)
    names = {pr.name for pr in b.projects}
    judged = 0
    for mode in VIEWS:
        out = render_view(mode, b, False, None, date(2026, 7, 30), width=100, height=30)
        for style, txt in _styles(out):
            if HEX["soon"] not in style and HEX["over"] not in style:
                continue
            judged += 1
            assert txt.strip() not in names, f"{mode}: {txt!r} names a project in {style}"
            assert "!" not in txt, f"{mode}: the priority mark wears {style}"
    assert judged, "vacuous: no judging hue was painted at all"


def test_every_view_that_marks_priority_marks_it_with_the_glyph(tmp_path):
    """Priority is marked by a SHAPE in a neutral tone, never by a hue. Two
    views mark it and they mark it differently on purpose: kanban names one task
    per card, so its mark is `!`; the lanes row names a PROJECT, so its mark is
    the count `!N`. Columns/agenda/gantt mark priority nowhere — pinned here too,
    so nobody is silently given one. (Was: `!` in both, before the lanes row
    replaced the per-phase cards.)"""
    b, p = _board(tmp_path)
    b.add_task(Task("Urgent thing", p.id, "Backlog", "high"))
    marks = {}
    for mode in VIEWS:
        out = render_view(mode, b, False, None, date(2026, 7, 30), width=100, height=30)
        marks[mode] = [(style, txt.strip()) for style, txt in _styles(out)
                       if txt.strip().startswith("!")]
    assert marks["swimlanes"] == [(HEX["ink"], "!1")]
    assert marks["kanban"] == [(HEX["ink"], "!")]
    assert marks["columns"] == marks["agenda"] == marks["gantt"] == []
