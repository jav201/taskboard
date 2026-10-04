"""One tokeniser for the notes' highlight syntax (batch 2026-10-02-batch-04, D-411).

Field report: the board painted notes through `views._highlight_markup` (markup) and
the details view / editor preview re-parsed that markup with Rich — which doubled
backslashes and turned `:smile:` into an emoji (P2 S-4). The preview now builds
Text pieces from `views.highlight_segments`, and the board's markup reads the SAME
tokeniser, so the two seats cannot disagree on what a note highlights.

Law: `_highlight_markup` emits exactly what it emitted before the split, for every
input the old function could render; the tokeniser drops markers, keeps the rest
in `mut`, and never raises. RED: a tokeniser that keeps a marker, swaps a tone, or
drops the text between highlights; a `_highlight_markup` that re-escapes or
re-tones. LLR-401.3, TC-417 (layer 0: `highlight_segments` has five paths).
"""
from __future__ import annotations

import itertools

import pytest
from rich.markup import escape

from taskboard.views import _HIGHLIGHT_RE, _highlight_markup, c, highlight_segments


def _base_highlight_markup(text: str) -> str:
    """The function as shipped at 56a1b10 (views.py:2930), frozen here as the
    oracle the refactor must reproduce byte for byte."""
    parts: list[str] = []
    last = 0
    for m in _HIGHLIGHT_RE.finditer(text):
        if m.start() > last:
            parts.append(c(escape(text[last:m.start()]), "mut"))
        inner = escape(m.group(1) or m.group(2) or m.group(3))
        if m.group(1) is not None:
            parts.append(c(inner, "soon"))
        elif m.group(2) is not None:
            parts.append(c(inner, "over"))
        else:
            parts.append(c(inner, "green"))
        last = m.end()
    if last < len(text):
        parts.append(c(escape(text[last:]), "mut"))
    return "".join(parts) if parts else c(escape(text), "mut")


# The input set is DERIVED (C-31): every sequence of up to three pieces drawn from
# plain text, each highlight form, a bracket and a backslash — not a hand list.
PIECES = ["ab", " ", "==y==", "!!r!!", "++g++", "[b]", "x\\", "=", "!", "+"]
INPUTS = ["", "plain"] + ["".join(t) for n in (1, 2, 3)
                          for t in itertools.product(PIECES, repeat=n)]


def _base_renders(text: str) -> bool:
    try:
        _base_highlight_markup(text)
        return True
    except TypeError:                 # the base raised on an EMPTY highlight (====)
        return False


def test_TC_417_the_board_markup_is_unchanged():
    """TC-417 (LLR-401.3). Over every derived input the base function rendered,
    `_highlight_markup` returns the base's exact string. RED under a re-escape, a
    swapped tone or a dropped segment in the tokeniser."""
    rendered = [t for t in INPUTS if _base_renders(t)]
    assert len(rendered) >= 1000, len(rendered)        # the set is not empty (C-31)
    diffs = [t for t in rendered if _highlight_markup(t) != _base_highlight_markup(t)]
    assert not diffs, diffs[:10]


@pytest.mark.parametrize("text, segments", [
    ("", []),
    ("plain", [("plain", "mut")]),
    ("a ==y== b", [("a ", "mut"), ("y", "soon"), (" b", "mut")]),
    ("!!r!!", [("r", "over")]),
    ("++g++ tail", [("g", "green"), (" tail", "mut")]),
    ("x\\ ==[b]== :smile:", [("x\\ ", "mut"), ("[b]", "soon"), (" :smile:", "mut")]),
    ("====", [("", "soon")]),
    ("a !!!! b", [("a ", "mut"), ("", "over"), (" b", "mut")]),
])
def test_TC_417_segments_drop_markers_and_keep_text(text, segments):
    """TC-417 (LLR-401.3), layer 0. Each path of the tokeniser: no match, a
    leading/trailing plain run, each of the three tones, a payload kept as text,
    and an EMPTY highlight — which the base `_highlight_markup` raised
    `TypeError` on (`"" or None or None` is `None`; found at P3, D-415) and which
    now yields an empty segment in its tone."""
    assert highlight_segments(text) == segments
    _highlight_markup(text)                              # never raises
