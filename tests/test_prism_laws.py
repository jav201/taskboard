"""The prototype's laws, ported to the real app (REV5 #22).

`_tui_prism_proposal/verify_prism.py` holds 17 law functions and 43 checks that
run against the PROTOTYPE's composed frames. This file is where they land in the
product, under one rule: ONE LAW, ONE HOME. Most already have one — porting them
again would create a second source of truth that can drift from the first, which
is the defect the whole Prism pass exists to remove.

So this file carries three things:

  * THE MANIFEST — every prototype law, with the file that holds it here, or an
    explicit `ADAPTED` / `DROPPED` verdict and the reason. The manifest is
    checked against disk, so a law whose home is deleted or renamed fails here
    rather than quietly evaporating.
  * THE LAWS THAT HAD NO HOME — attribution and register.
  * THE ONE THAT IS RED AGAINST THIS APP, recorded as a finding rather than
    hidden: the prototype commits with rules and draws no box; this app draws a
    box. That is a known, reported deviation, and the law states the real
    situation instead of pretending either way.
"""

import pathlib
import re
from datetime import date, timedelta

from taskboard.keymap import VIEWS
from taskboard.models import PROJECT_COLORS, Board, Project, Task
from taskboard.views import HEX, render_view

TODAY = date(2026, 7, 30)
TESTS = pathlib.Path(__file__).parent
SRC = pathlib.Path(__file__).parent.parent / "taskboard"

# --------------------------------------------------------------------------- #
# THE MANIFEST — prototype law -> where it lives here
# --------------------------------------------------------------------------- #
# (law, home file, a test function that carries it) | ("ADAPTED"/"DROPPED", reason)
MANIFEST = {
    "law_art/rectangle": ("test_swimlanes.py", "test_every_row_is_exactly_the_requested_width"),
    "law_art/closure": ("test_prism_laws.py",
                        "test_the_closure_law_is_met_the_design_commits_with_rules"),
    "law_resolution": ("test_wave.py", "test_a_drawn_curve_resolves_below_cell_width"),
    "law_carving/today": ("test_field.py", "test_the_figure_is_drawn_over_the_lattice_and_keeps_the_rule"),
    "law_carving/notch": ("test_wave.py", "test_a_notch_can_never_erase_its_column"),
    "law_carving/count": ("test_swimlanes.py", "test_the_leader_gets_a_drawn_field_that_ends_at_its_own_due_date"),
    "law_attribution/declared-hue": ("test_prism_laws.py", "test_every_lit_field_cell_carries_a_declared_hue"),
    "law_attribution/row-band": ("test_prism_laws.py", "test_no_row_mixes_two_identity_hues_in_its_field"),
    "law_attribution/rejected-alternative": (
        "ADAPTED", "the prototype MEASURES the rejected stacked-strata layout to "
                   "justify row-bands. The app never implemented that alternative, so "
                   "there is nothing to measure; the row-band property it argued for "
                   "is asserted directly instead."),
    "law_ration": ("test_palette_ration.py", "test_no_project_hue_stands_inside_a_reserved_band"),
    "law_ration/severity-seat": ("test_swimlanes.py", "test_severity_has_exactly_one_seat_and_a_date_wears_it"),
    "law_register/frames": ("test_prism_laws.py", "test_no_view_speaks_in_the_second_person"),
    "law_register/source": ("test_prism_laws.py", "test_no_literal_in_the_source_can_emit_the_second_person"),
    "law_three_states": ("test_swimlanes.py", "test_all_three_loads_render_width_exact_and_lose_no_project"),
    "law_ordered_coverage": ("test_wave.py", "test_non_decreasing_steps_never_draw_a_falling_curve"),
    "law_occupancy": ("test_occupancy.py", "test_the_view_holds_its_occupancy_floors"),
    "law_motion": ("test_motion.py", "test_nothing_but_the_rule_moves_between_phases"),
    "law_gantt_order": ("test_archive.py", "test_open_work_comes_first_and_finished_work_sinks_to_the_tail"),
    "law_edge_budget": ("test_swimlanes.py", "test_the_edge_keeps_its_tone_count_whatever_the_board_holds"),
    "law_meter": ("test_swimlanes.py", "test_the_meter_is_shorter_the_sooner_the_work_is_due"),
    "law_keybar": ("test_keymap.py", "test_every_seat_entry_reaches_the_widest_bar"),
    "law_legend": ("test_legend.py", "test_no_entry_describes_a_mark_the_view_is_not_drawing"),
    "law_clip": ("test_field.py", "test_a_date_outside_the_window_is_flagged_and_never_silently_clamped"),
    "law_spend": ("test_spend.py", "test_the_field_never_grows_while_a_task_is_unnamed"),
}


def board(tmp_path, projects=4, tasks=16, name="p.json") -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    hues = list(PROJECT_COLORS)
    per = max(1, tasks // projects)
    k = 0
    for i in range(projects):
        p = Project(f"Project {i}", hues[i % len(hues)],
                    ["on_track", "on_track", "paused", "completed"][i % 4],
                    start_date=(TODAY - timedelta(days=20)).isoformat(),
                    due_date=(TODAY + timedelta(days=6 + i * 5)).isoformat())
        b.projects.append(p)
        for j in range(per):
            b.tasks.append(Task(
                f"Task {i}-{j} something real", p.id,
                ["Backlog", "Doing", "Done"][j % 3], "high" if j == 0 else "normal",
                due_date=(TODAY + timedelta(days=k - 4)).isoformat(),
                blocked=(k % 7 == 0)))
            k += 1
    return b


# --------------------------------------------------------------------------- #
# the manifest is checked against disk
# --------------------------------------------------------------------------- #
def test_every_prototype_law_has_a_home_or_a_recorded_reason():
    """A law that is neither ported nor consciously dropped is a law silently
    skipped, which is the failure mode this whole exercise exists to prevent."""
    for law, entry in MANIFEST.items():
        head, detail = entry
        if head in ("ADAPTED", "DROPPED", "QUEUED"):
            assert len(detail) > 40, f"{law}: the reason is too thin to be a reason"
            continue
        path = TESTS / head
        assert path.exists(), f"{law}: its home {head} does not exist"
        src = path.read_text(encoding="utf-8")
        assert f"def {detail}(" in src, f"{law}: {head} has no {detail}()"


def test_the_manifest_covers_every_law_function_in_the_prototype():
    """Counted against the source of truth, so a law added upstream shows up
    here as a gap rather than being missed."""
    proto = (SRC.parent / "_tui_prism_proposal" / "verify_prism.py")
    if not proto.exists():                      # the proposal folder is not shipped
        return
    names = set(re.findall(r"^def (law_\w+)", proto.read_text(encoding="utf-8"), re.M))
    covered = {k.split("/")[0] for k in MANIFEST}
    assert names <= covered, f"prototype laws with no manifest entry: {names - covered}"


# --------------------------------------------------------------------------- #
# law_attribution — the laws that had no home
# --------------------------------------------------------------------------- #
FIELD_GLYPHS = set("⣿⡇⣤⣀⠤⠒⠉⢀⣠⣸⣰⣴⣶⣼⣧⣇⢰⢸⣆⣄⡀⣥⣭⣟⣝⣣⡆⣾⣷⢕")


def test_every_lit_field_cell_carries_a_declared_hue(tmp_path):
    """Every drawn mark belongs to a declared house: an identity hue, the ash of
    spent time, the quiet step, the attention teal, or severity's one seat. A
    mark in some undeclared colour is a mark with no meaning.

    Checked over EVERY coloured span, not a list of glyphs — the first version
    listed only braille and a lattice cell painted `#123456` sailed through it."""
    b = board(tmp_path)
    declared = set(HEX.values())
    strays = []
    for mode in VIEWS:
        text = render_view(mode, b, False, None, TODAY, width=120, height=40)
        for s in text.spans:
            for hexv in re.findall(r"#[0-9a-fA-F]{6}", str(s.style)):
                if hexv.lower() not in {d.lower() for d in declared}:
                    strays.append((mode, text.plain[s.start:s.end][:6], hexv))
    assert not strays, f"undeclared hues on drawn cells: {strays[:3]}"


def test_no_row_mixes_two_identity_hues_in_its_field(tmp_path):
    """MANDATE 2, and the reason lanes are row-bands rather than one stacked
    field: a reader must attribute load to a project at a glance. One row, one
    project, so attribution is exact by construction rather than by squinting.

    (The prototype argues this by MEASURING the rejected alternative — stacking
    every project into one field, where 100 % of cells would span two projects
    and a cell has only one foreground colour. That alternative was never built
    here, so the property it argued for is asserted directly.)"""
    b = board(tmp_path)
    text = render_view("swimlanes", b, False, None, TODAY, width=120, height=44)
    identity = {HEX[c]: c for c in PROJECT_COLORS}
    per_row = {}
    for s in text.spans:
        seg = text.plain[s.start:s.end]
        if not (set(seg) & FIELD_GLYPHS):
            continue
        row = text.plain.count("\n", 0, s.start)
        for hexv, name in identity.items():
            if hexv in str(s.style):
                per_row.setdefault(row, set()).add(name)
    mixed = {r: h for r, h in per_row.items() if len(h) > 1}
    assert not mixed, f"rows whose field mixes identities: {mixed}"
    assert per_row, "vacuous: no field cell carried an identity hue at all"


# --------------------------------------------------------------------------- #
# law_register — the app's own voice
# --------------------------------------------------------------------------- #
SECOND_PERSON = re.compile(r"\b(you|your|yours|we|our|us)\b", re.I)


def test_no_view_speaks_in_the_second_person(tmp_path):
    """THE REGISTER: the app keeps the log of the day, it does not talk to the
    person reading it and it does not grade their work. "overdue" is a fact
    about a date; "you are behind" would be a verdict about a person."""
    b = board(tmp_path)
    for mode in VIEWS:
        painted = str(render_view(mode, b, False, None, TODAY, width=120, height=40))
        hits = SECOND_PERSON.findall(painted)
        assert not hits, f"{mode} addresses the reader: {hits[:3]}"


def test_no_literal_in_the_source_can_emit_the_second_person():
    """At the source, not just in one render: a string the app could ever print
    is checked, so a rarely-hit branch cannot smuggle a voice in."""
    # ONE named exemption, because a named exemption is honest and a weakened
    # pattern is not: "We" here is Wednesday, in the date picker's weekday row.
    EXEMPT = {"[dim]Mo Tu We Th Fr Sa Su[/dim]"}
    offenders = []
    for path in sorted(SRC.glob("*.py")):
        src = path.read_text(encoding="utf-8")
        # strings only, and not docstrings/comments: this is about what the app
        # PRINTS, and the reasoning around it is written in prose on purpose
        src = re.sub(r'"""[\s\S]*?"""', "", src)
        src = re.sub(r"^\s*#.*$", "", src, flags=re.M)
        for lit in re.findall(r'"([^"\n]{4,})"', src) + re.findall(r"'([^'\n]{4,})'", src):
            if lit in EXEMPT:
                continue
            if SECOND_PERSON.search(lit) and not lit.strip().startswith("#"):
                offenders.append((path.name, lit[:60]))
    assert not offenders, f"literals in the app's voice: {offenders[:5]}"


# --------------------------------------------------------------------------- #
# the law that is RED against this app, stated rather than hidden
# --------------------------------------------------------------------------- #
def test_the_closure_law_is_met_the_design_commits_with_rules(tmp_path):
    """THE PROTOTYPE LAW, AND IT IS NOW GREEN: "no box corners — this design
    commits with rules, not boxes".

    It was the last law red against this app, and the frame was the only thing
    failing it. Measured on the way out: the box cost 7.6 % of every render, and
    removing it took chrome to 0.0 % in all four views."""
    b = board(tmp_path)
    for mode in VIEWS:
        rows_ = str(render_view(mode, b, False, None, TODAY,
                                width=96, height=30)).splitlines()
        assert not set("".join(rows_)) & set("╭╮╰╯"), f"{mode} still draws a box"
        for r in rows_:                       # and no side borders either
            # `├` and `┤` are side borders too. Checking only `│` let the kanban
            # header rule keep its framed edges long after the frame went, and
            # with them a one-cell shift: the rule reserved column 0 for `├`, so
            # every `┼` landed one cell right of the `│` it ruled (30·60·90 ->
            # 31·61·91 at 120 cells). One glyph named, a whole class missed.
            assert r[0] not in "│├┤" and r[-1] not in "│├┤", f"{mode}: {r[:3]!r}"
    # KANBAN KEEPS ITS INTERNAL COLUMN RULES (│ between phase columns, with `┼`
    # junctions on its header rule). Those are structure a column view needs —
    # they say WHICH column — not the enclosing box this law is about. Recorded
    # in .dev-flow/BACKLOG.md as the one place box-drawing survives.
    kanban = str(render_view("kanban", b, False, None, TODAY, width=96, height=30))
    assert "│" in kanban
    assert MANIFEST["law_art/closure"][0] != "DROPPED"


# --------------------------------------------------------------------------- #
# the frame is gone — and nothing it carried went with it
# --------------------------------------------------------------------------- #
def test_the_head_row_still_carries_what_the_frame_title_did(tmp_path):
    """The box's top rail carried the view's name and its counts. Removing the
    box may not lose them: the head row is now a full-width row of FACTS, which
    is why it is not chrome — it earns its cells."""
    b = board(tmp_path)
    head = str(render_view("swimlanes", b, False, None, TODAY,
                           width=96, height=30)).splitlines()[0]
    assert "TASKBOARD" in head
    assert re.search(r"\d+ open", head) and re.search(r"\d+ due", head)
    assert len(head) == 96                       # a row, not a rail


def test_the_overflow_counts_survived_the_frame(tmp_path):
    """`+N not shown` lived inside the box and still has a home: the axis row."""
    b = board(tmp_path, projects=8, tasks=40, name="over.json")
    out = str(render_view("swimlanes", b, False, None, TODAY,
                          width=96, height=12)).splitlines()
    assert any("not shown" in l for l in out)


def test_no_view_is_narrower_than_the_width_it_was_given(tmp_path):
    """The frame's two columns went back to the content, so a row IS the width."""
    b = board(tmp_path)
    for mode in VIEWS:
        for w in (24, 40, 72, 96, 130):
            for line in str(render_view(mode, b, False, None, TODAY,
                                        width=w, height=20)).splitlines():
                assert len(line) == max(24, w), f"{mode} @ {w}: {len(line)}"


def test_the_rule_crosses_exactly_where_the_columns_divide(tmp_path):
    """A rule under a set of columns has ONE job: say where they divide. It was
    doing it one cell to the right.

    The builder was inherited from the framed era — it reserved column 0 for a
    `├` and column w-1 for a `┤`, then wrote the junctions into the span
    BETWEEN them. While the frame existed those coordinates agreed. Frameless,
    every row spends the full width, so the rule leaned by one against the row
    it rules: measured at 120 cells, headers divided at 30·60·90 and the rule
    crossed at 31·61·91.

    This measures COLUMNS IN CELLS, not character indices — the two disagree the
    moment a title holds a wide glyph, and it is the cells that are drawn."""
    from rich.cells import cell_len

    def marks(row: str, glyphs: str) -> list[int]:
        out, col = [], 0
        for ch in row:
            if ch in glyphs:
                out.append(col)
            col += cell_len(ch)
        return out

    b = board(tmp_path)
    for presentation in ("grouped", "matrix"):
        for width in (80, 96, 120):
            rows_ = str(render_view("kanban", b, False, None, TODAY, width=width,
                                    height=30, presentation=presentation)).splitlines()
            divides = [marks(r, "│") for r in rows_]
            divides = [d for d in divides if d]
            rules = [marks(r, "┼┴") for r in rows_ if set(r) & set("┼┴")]
            assert divides, f"{presentation} @{width}: no column divisions at all"
            assert rules, f"{presentation} @{width}: no rule drawn at all"
            columns = divides[0]
            for d in divides:
                assert d == columns, f"{presentation} @{width}: rows divide differently"
            for r in rules:
                assert r == columns, (
                    f"{presentation} @{width}: rule crosses at {r}, "
                    f"columns divide at {columns}")
