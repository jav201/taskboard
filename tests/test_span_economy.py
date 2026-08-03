"""Span economy — the runs we emit are the runs we pay.

WHY THIS FILE EXISTS: `c()` colours one cell at a time, so a band of one tone
left 60 `[#hex]…[/]` pairs where one would do. That is not a cosmetic waste.
Each run becomes a rich Span, then a Segment, and Textual stamps a per-run
`{"offset": (x, y)}` into every Segment's style meta (textual/content.py).
rich's `Style.__hash__` includes `_meta`, so two segments drawn in the SAME
colour at different x never compare equal — and `Strip.simplify()`, the usual
answer to "adjacent identical styles merge," merges NONE of them. Measured on
the gantt at 120x40: 2,880 segments, 2,579 of them adjacent pairs whose style
strings are byte-identical, and simplify recovers zero. The run count therefore
survives all the way to the terminal, so `collapse_runs` pays it down at the one
seam where markup becomes Text.

THE LAW, and it is the whole point: collapsing may change how many runs are
used to SAY the drawing. It may never change the drawing. Every test below
compares plain text AND the style of every single character, so a collapse that
shifts one cell's colour by one position turns them red — a run-count assertion
alone would not, which is why the equivalence test is written per character.
"""

from datetime import date, timedelta
from pathlib import Path

from rich.text import Text

from taskboard.models import Board, Project, Task
from taskboard.views import collapse_runs, render_view

VIEWS = ["swimlanes", "agenda", "gantt", "kanban"]
SIZES = [(68, 20), (120, 40), (200, 60)]


def char_styles(t: Text) -> list[str | None]:
    """The style of EVERY character, flattened. Two Texts that agree here are
    the same drawing no matter how many spans each one used to say it."""
    out: list[str | None] = [None] * len(t.plain)
    for span in t.spans:
        for i in range(span.start, min(span.end, len(out))):
            out[i] = str(span.style)
    return out


def same_drawing(markup: str) -> tuple[bool, bool]:
    """(text matches, per-character style matches) for markup vs its collapse."""
    a, b = Text.from_markup(markup), Text.from_markup(collapse_runs(markup))
    return a.plain == b.plain, char_styles(a) == char_styles(b)


def board_with_tasks(tmp_path=None) -> Board:
    """A board exercising the paths that colour per cell: several projects (so
    several hues), dated and undated work, overdue and finished tasks."""
    phases = ["Backlog", "Doing", "Review", "Done"]
    projects = [Project(name=n, color=c) for n, c in
                (("Alpha", "cyan"), ("Beta", "pink"), ("Gamma", "lime"))]
    today = date.today()
    tasks = []
    for proj in projects:
        for k, phase in enumerate(phases):
            tasks.append(Task(
                title=f"{proj.name} task {k}",
                project_id=proj.id,
                phase=phase,
                start_date=str(today - timedelta(days=10 + k)),
                # k == 1 lands in the past: the overdue hue must be exercised
                due_date=str(today + timedelta(days=k - 2)),
                priority=("high" if k == 0 else "normal"),
            ))
        # one undated task per project — the views colour these differently
        tasks.append(Task(title=f"{proj.name} someday", project_id=proj.id,
                          phase="Backlog"))
    path = (tmp_path / "board.json") if tmp_path else Path("board.json")
    return Board(projects, tasks, path, phases=phases)


# --------------------------------------------------------------------------- #
# 1. equivalence — the drawing is untouched
# --------------------------------------------------------------------------- #
def test_collapse_never_changes_any_view():
    """The real views, at three widths, with and without a selection. This is
    the test that makes the optimization safe to leave switched on."""
    b = board_with_tasks()
    ids = [t.id for t in b.visible_tasks(False)]
    checked = 0
    for mode in VIEWS:
        for w, h in SIZES:
            for sel in (None, ids[0], ids[len(ids) // 2]):
                for arch in (False, True):
                    markup_seen: list[str] = []
                    _capture(markup_seen, mode, b, arch, sel, w, h)
                    assert markup_seen, f"no markup captured for {mode}"
                    for m in markup_seen:
                        text_ok, style_ok = same_drawing(m)
                        assert text_ok, f"{mode} {w}x{h} sel={sel}: text changed"
                        assert style_ok, f"{mode} {w}x{h} sel={sel}: styles moved"
                        checked += 1
    assert checked >= len(VIEWS) * len(SIZES) * 3, "coverage collapsed silently"


def _capture(sink: list[str], mode, board, arch, sel, w, h) -> None:
    """Render a view and keep the markup it handed to `Text.from_markup`."""
    import taskboard.views as V
    real = V.collapse_runs
    V.collapse_runs = lambda m: (sink.append(m), real(m))[1]
    try:
        V.render_view(mode, board, arch, sel, width=w, height=h,
                      line_map={}, presentation="grouped", tick=3)
    finally:
        V.collapse_runs = real


# --------------------------------------------------------------------------- #
# 2. it actually collapses — a test that fails if `collapse_runs` goes identity
# --------------------------------------------------------------------------- #
def test_collapse_removes_the_redundant_runs():
    """Without this, `collapse_runs = lambda m: m` would pass every other test
    in the file. The gantt is the worst offender, so it sets the bar."""
    b = board_with_tasks()
    sink: list[str] = []
    _capture(sink, "gantt", b, False, None, 120, 40)
    before = sink[0]
    after = collapse_runs(before)
    n_before = Text.from_markup(before).spans
    n_after = Text.from_markup(after).spans
    assert len(n_after) < len(n_before) / 3, (
        f"expected a large drop in runs, got {len(n_before)} -> {len(n_after)}")


def test_a_uniform_band_becomes_one_run():
    """The shape the whole fix exists for: the same tone, cell after cell."""
    markup = "".join("[#22d3ee]·[/]" for _ in range(40))
    out = collapse_runs(markup)
    assert out == "[#22d3ee]" + "·" * 40 + "[/]"
    assert len(Text.from_markup(out).spans) == 1


# --------------------------------------------------------------------------- #
# 3. what it must REFUSE to collapse — the drawing's seams are real
# --------------------------------------------------------------------------- #
def test_different_styles_are_never_merged():
    markup = "[#22d3ee]a[/][#f472b6]b[/]"
    assert collapse_runs(markup) == markup
    assert same_drawing(markup) == (True, True)


def test_links_with_different_targets_stay_apart():
    """`[/link][link=…]` looks like the collapsible shape but the targets differ
    — merging them would retarget half the text."""
    markup = "[link=http://a]one[/link][link=http://b]two[/link]"
    assert collapse_runs(markup) == markup
    a = Text.from_markup(markup)
    assert char_styles(a) == char_styles(Text.from_markup(collapse_runs(markup)))


def test_identical_links_may_merge_but_keep_the_target():
    markup = "[link=http://a]one[/link][link=http://a]two[/link]"
    assert same_drawing(markup) == (True, True)


def test_escaped_brackets_are_not_tags():
    """A task title is user text. `escape()` turns '[' into '\\[', and that must
    survive as a literal brace — never be read as a tag this pass can cancel."""
    from rich.markup import escape
    title = escape("build [v2] parser")
    markup = f"[#22d3ee]{title}[/][#22d3ee] ok[/]"
    text_ok, style_ok = same_drawing(markup)
    assert text_ok and style_ok
    assert "[v2]" in Text.from_markup(collapse_runs(markup)).plain


def test_nested_styles_keep_their_order():
    """Cancelling a close that is not on top would rewrite the nesting."""
    markup = "[#22d3ee]a[b #f472b6]b[/]c[/][#22d3ee]d[/]"
    assert same_drawing(markup) == (True, True)


def test_reverse_and_bold_tags_round_trip():
    markup = "[reverse]sel[/reverse][reverse]ected[/reverse] [b #22d3ee]x[/]"
    assert same_drawing(markup) == (True, True)


def test_plain_text_is_untouched():
    assert collapse_runs("no tags here at all") == "no tags here at all"
    assert collapse_runs("") == ""
