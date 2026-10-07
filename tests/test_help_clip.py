"""The `?` help never cuts a word in half (HLR-1104, LLR-1104.1).

Field report (ux UXV-6): at 80 cells the help text cut lines mid-word — the
screen stopped matching what the user knows the words to be. The seat was
Textual's default label wrap: a `Label` of height 1 inside a narrow column wraps
its text with `break_long_words=True`, so a word that straddles the column edge
is broken mid-glyph and the rest of the line is dropped (e.g. "the project
under most pressure" painted "the project under m"). The fix (modals `_HelpLine`
+ `_clip_words`) clips each legend meaning and usage bullet at a WORD boundary,
appending `…` when a word is cut; an unbreakable token longer than the width
clips at the edge with `…`.

Law (LLR-1104.1): at 80×24 on the fixture board, every visible help line ends at
a word boundary or with `…`. The exact-edge and overlong-token arms are pinned
on `_clip_words` directly (they have no natural fixture in the fixed help copy).
"""
from __future__ import annotations

from datetime import date

from taskboard.app import RENUMBER_NOTICE_KEY, TaskboardApp
from taskboard.keymap import bar_keys
from taskboard.models import Board, Project, Task
from taskboard.modals import _clip_words
from taskboard.views import _strip, help_example, help_usage, legend_entries

SIZE = (80, 24)


def _board(tmp_path) -> Board:
    """One project, one undated task: the swimlanes legend carries the long
    "field: ash spent …" meaning (which clips at 22 cells) and the project's
    "the project under most pressure" entry."""
    p = Project("Plat", "sky")
    t = Task("A task with a reasonably long title", p.id, "Doing")
    b = Board([p], [t], tmp_path / "board.json", {RENUMBER_NOTICE_KEY: True})
    b.save()
    return b


def _sources(mode: str, board: Board, today: date) -> list[str]:
    """Every full source line the two help columns render, in plain text."""
    sources = ["Usage"]
    for heading, bullets in help_usage(mode):
        sources.append(heading)
        for bullet in bullets:
            sources.append("  • " + bullet)
    entries = legend_entries(mode, board, today, *SIZE)
    if entries:
        sources.append("Legend")
        for swatch, meaning in entries:
            sources.append(_strip(swatch) + "  " + meaning)
    example, example_meaning = help_example(mode)
    if example:
        sources.append("Example")
        sources.append(example)
        sources.append(example_meaning)
    sources.append("Keys")
    for k in bar_keys(mode):
        sources.append(f"{k.show}  {k.label}")
    return sources


def _column_lines(app, col: str) -> list[str]:
    """Each help line's rendered content, read off the column's children —
    chrome (the scrollbar track) is not a child and is not read."""
    return [str(child.render()) for child in app.screen.query_one(col).children]


async def test_AT_1104_help_lines_end_at_word_boundary(tmp_path):
    """AT-1104 (HLR-1104, US-1104) — at 80×24 no visible help line ends mid-word.

    Every painted line of both columns, trimmed of its padding, either ends with
    `…` (clipped) or equals one of the full source lines (fits whole) — so a
    line the compositor broke mid-word fails on both counts."""
    board = _board(tmp_path)
    app = TaskboardApp(board_path=str(board.path), team_sync_interval=1e9)
    async with app.run_test(size=SIZE, notifications=True) as pilot:
        await pilot.pause()
        await pilot.press("question_mark")
        for _ in range(3):
            await pilot.pause()
        sources = set(_sources("swimlanes", board, date.today()))
        for col in ("#help-left", "#help-right"):
            for line in _column_lines(app, col):
                trimmed = line.rstrip()
                if not trimmed:
                    continue
                assert trimmed.endswith("…") or trimmed in sources, \
                    f"{col}: line ends mid-word: {trimmed!r}"


def test_TC_1104_clip_words_exact_edge_and_overlong_token():
    """TC-1104 (LLR-1104.1) — the boundary catalog: exact-edge and overlong.

    A word exactly at the width edge is left whole; a line that must cut clips
    at the last fitting word with `…`; an unbreakable token longer than the
    width clips at the edge with `…` (never a mid-word break)."""
    # fits: unchanged
    assert _clip_words("short text", 20) == "short text"
    # exact edge: a word whose end lands exactly on the last cell
    assert _clip_words("abcdefgh", 8) == "abcdefgh"
    assert _clip_words("abcdefg", 8) == "abcdefg"
    # word-boundary clip: the last fitting word, then `…`
    assert _clip_words("the project under most pressure", 20) == "the project under…"
    assert _clip_words("no date to count down to", 12) == "no date to…"
    # overlong unbreakable token: clip at the edge with `…`
    assert _clip_words("supercalifragilistic", 10) == "supercali…"
    assert _clip_words("abcdefghijklmnop", 8) == "abcdefg…"
    # a word filling the reserved cell, then a clip
    assert _clip_words("abcdefg x", 8) == "abcdefg…"
    # degenerate widths
    assert _clip_words("", 10) == ""
    assert _clip_words("word", 0) == ""
