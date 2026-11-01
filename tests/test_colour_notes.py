"""Multicolour notes, layer 0: the one tokeniser, every surface that reads it, and the
six tones' palette checks (batch 2026-11-01-v3-incC, Inc C, US-4201, HLR-4201 / HLR-4202 /
HLR-4206).

Field report (the board's owner, `username_subject`): "I write my notes in several
colours, like pens in a notebook." A note with `::b:: text ::` must show `text` in blue on
every surface — the board, the details, the editor preview, the presentation and both HTML
reports — and a note written before this increment (`==…==`, `!!…!!`, `++…++`, a plain
`std::vector`) must render exactly as it did at base `0a8dfaa`.

How the oracles are built (anti-mirror):
- `ref_spans` below is an independent reference scanner written in this file from the
  requirements (LLR-4201.1..8 and the rulings P-V-2, ARCH-11): a position-by-position scan
  that tries the legacy pattern and the opener AT each position, then walks an open colour
  span character by character. The product scanner caches regex matches (SEC-1); the two
  are written differently on purpose, so a shared mistake is unlikely.
- Input sets are DERIVED with `itertools.product` (C-31), never a hand list.
- The legacy oracle of AT-4204 is FROZEN: the values were captured by running the base
  tree `0a8dfaa` (this tester's run, not the implementer's), and written here as literals.
- The palette checks compute HLS saturation and the WCAG 2.x contrast ratio in this file,
  and read the tones from the SHIPPED surface (`notes_text`), not from a table.

RED on base `0a8dfaa`: every new test fails on an assertion — the base tokeniser leaves
`::b:: x ::` as one `mut` segment, the base has no `colour_spans` / `PEN_CODES` (reached
through `_need`, which turns an absent name into `pytest.fail`, never an ImportError), the
deck and workspace style sheets hold no `hl-blue` rule. GUARDS that pass on base by design:
`test_TC_4203_inputs_without_colons_tokenise_as_at_base` (LLR-4201.3) and
`test_AT_4204_legacy_notes_render_as_at_base` (AT-4204).
"""
from __future__ import annotations

import colorsys
import itertools
import json
import re
import statistics
import time
from datetime import date

import pytest
from rich.color import Color, ColorSystem
from rich.text import Text

from taskboard import modals, report_deck, report_html, report_workspace, views
from taskboard.models import Board, Project, Task
from taskboard.people import Person
from taskboard.views import (HEX, _focus_note_snippet, _highlight_markup,
                             _present_note_markup, c, highlight_segments, legend_entries,
                             mention_marks, notes_text, present_note_lines)

TODAY = date(2026, 11, 1)
CODES = "roygbv"                                   # pen order 1..6 (definitions table)
TONE = {"r": "over", "o": "orange", "y": "soon", "g": "green", "b": "blue", "v": "violet"}
NAME = {"r": "red", "o": "orange", "y": "yellow", "g": "green", "b": "blue", "v": "violet"}
TONE_HEX = {"r": "#f43f5e", "o": "#fb923c", "y": "#fbbf24", "g": "#4ade80",
            "b": "#60a5fa", "v": "#a78bfa"}        # the design's six hexes (graph V, C-4 table)
CLOSED_TONES = {"mut", "soon", "over", "green", "orange", "blue", "violet"}   # A-5 / SEC-9
PEOPLE = {"ana": Person("ana", "Ana Ruiz")}        # synthetic person


def _need(mod, name: str):
    """A name Inc C adds. Absent (the base tree) → an assertion failure that says so,
    so the RED on base is a failed test, not a collection error."""
    obj = getattr(mod, name, None)
    if obj is None:
        pytest.fail(f"{mod.__name__}.{name} is missing: Inc C is not built here")
    return obj


# --------------------------------------------------------------------------- #
# The independent reference scanner (from the requirements, not from the code)
# --------------------------------------------------------------------------- #
_LEGACY = re.compile(r"==(.*?)==|!!(.*?)!!|\+\+(.*?)\+\+")   # the legacy span, exactly as at base
_OPENER = re.compile(r"::([roygbv])::( ?)")                   # opener + at most one space
_LEGACY_TONE = ("soon", "over", "green")


def ref_spans(text: str) -> list[tuple[int, int, int, int, str, str | None]]:
    """(start, inner_start, inner_end, end, tone, code) per span, str offsets.

    LLR-4201.7: the span whose start comes first wins; inside a legacy span every
    character up to its closer is inner text; inside a colour span only `\\n`, an opener
    (LLR-4201.6), `:::<c>::` (ARCH-11: the opener one to the right wins) or a closer `::`
    (LLR-4201.2: one preceding space belongs to it) is looked at. LLR-4201.4: line end
    ends an open span. LLR-4201.5: a `::` outside any span is never looked at."""
    out = []
    i, n = 0, len(text)
    while i < n:
        found = None
        for p in range(i, n):                      # position by position (not regex search)
            m = _LEGACY.match(text, p)
            if m:
                found = ("legacy", m)
                break
            m = _OPENER.match(text, p)
            if m:
                found = ("colour", m)
                break
        if found is None:
            break
        kind, m = found
        if kind == "legacy":
            g = next(k for k in (1, 2, 3) if m.group(k) is not None)
            out.append((m.start(), m.start(g), m.end(g), m.end(), _LEGACY_TONE[g - 1], None))
            i = m.end()
            continue
        start, inner, code = m.start(), m.end(), m.group(1)
        k = inner
        while True:
            if k >= n or text[k] == "\n":
                inner_end = end = k
                break
            if text.startswith("::", k):
                if _OPENER.match(text, k):
                    inner_end = end = k
                elif text.startswith(":::", k) and _OPENER.match(text, k + 1):
                    inner_end = end = k + 1
                else:
                    inner_end = k - 1 if (k - 1 >= inner and text[k - 1] == " ") else k
                    end = k + 2
                break
            k += 1
        out.append((start, inner, inner_end, end, TONE[code], code))
        i = end
    return out


def ref_segments(text: str) -> list[tuple[str, str]]:
    out, last = [], 0
    for s, a, b, e, tone, _code in ref_spans(text):
        if s > last:
            out.append((text[last:s], "mut"))
        out.append((text[a:b], tone))
        last = e
    if last < len(text):
        out.append((text[last:], "mut"))
    return out


def ref_visible(text: str) -> str:
    return "".join(seg for seg, _ in ref_segments(text))


# LLR-4201.9's derived set: 10 pieces × up to 4 = 11 110 inputs (C-31)
PIECES_9 = ["ab", " ", "::b::", "::r::", "::", "==y==", "!!", "::z::", "é", "\n"]
DERIVED = ["".join(t) for n in (1, 2, 3, 4) for t in itertools.product(PIECES_9, repeat=n)]
# the single-line part (LLR-4204.4 reads it): every input without "\n"
DERIVED_SINGLE = [t for t in DERIVED if "\n" not in t]

# LLR-4201.3's set: the base suite's PIECES × up to 3 (tests/test_highlight_segments.py)
PIECES_BASE = ["ab", " ", "==y==", "!!r!!", "++g++", "[b]", "x\\", "=", "!", "+"]
INPUTS_BASE = ["", "plain"] + ["".join(t) for n in (1, 2, 3)
                               for t in itertools.product(PIECES_BASE, repeat=n)]


def _base_highlight_segments(text: str) -> list[tuple[str, str]]:
    """`views.highlight_segments` as shipped at 0a8dfaa (views.py:3505), frozen."""
    out, last = [], 0
    for m in _LEGACY.finditer(text):
        if m.start() > last:
            out.append((text[last:m.start()], "mut"))
        if m.group(1) is not None:
            out.append((m.group(1), "soon"))
        elif m.group(2) is not None:
            out.append((m.group(2), "over"))
        else:
            out.append((m.group(3), "green"))
        last = m.end()
    if last < len(text):
        out.append((text[last:], "mut"))
    return out


def _spans(text: str) -> list[tuple]:
    """The product's `colour_spans` as plain tuples (start, inner_start, inner_end, end,
    tone, code), through the field names of the shared Span (graph-interfaces)."""
    colour_spans = _need(views, "colour_spans")
    return [(s.start, s.inner_start, s.inner_end, s.end, s.tone, s.code)
            for s in colour_spans(text)]


def test_reference_scanner_reproduces_the_designs_examples():
    """Self-check of the oracle (not a product test; passes on base by construction): the
    reference scanner agrees with every `colour_spans` / `highlight_segments` example of
    graph-proto-V. If this fails, the oracle is wrong, not the product."""
    assert ref_spans("a ::b:: x :: c") == [(2, 8, 9, 12, "blue", "b")]
    assert ref_spans("::b::  x  ::") == [(0, 6, 9, 12, "blue", "b")]
    assert ref_spans("==late==") == [(0, 2, 6, 8, "soon", None)]
    assert ref_spans("::r:: open") == [(0, 6, 10, 10, "over", "r")]
    assert ref_spans("::r:: a\nb") == [(0, 6, 7, 7, "over", "r")]
    assert ref_spans("std::vector") == [] and ref_spans("::bb:: t ::") == []
    assert ref_spans("::b:: x ::r:: y ::") == [(0, 6, 8, 8, "blue", "b"),
                                               (8, 14, 15, 18, "over", "r")]
    assert ref_spans("::b:: ==a== ::") == [(0, 6, 11, 14, "blue", "b")]
    assert ref_spans("==a ::b:: c==") == [(0, 2, 11, 13, "soon", None)]
    assert ref_spans("a::b::::c") == [(1, 6, 6, 8, "blue", "b")]
    assert ref_spans("::b::  ::") == [(0, 6, 6, 9, "blue", "b")]
    assert ref_spans("::b:: std::vector ::") == [(0, 6, 9, 11, "blue", "b")]
    assert ref_spans("a:::b:: plan ::") == [(2, 8, 12, 15, "blue", "b")]
    assert ref_spans("::r:: a :::b:: c ::") == [(0, 6, 9, 9, "over", "r"),
                                                (9, 15, 16, 19, "blue", "b")]
    assert ref_spans("é ::b:: café ☕ ::") == [(2, 8, 14, 17, "blue", "b")]
    assert ref_segments("::r:: ab ::::b:: x ::") == [("ab", "over"), ("x", "blue")]
    assert ref_segments("::b:: std::vector ::") == [("std", "blue"), ("vector ::", "mut")]
    assert len(DERIVED) == 11110 and len(INPUTS_BASE) == 1112
    assert all(ref_segments(t) == _base_highlight_segments(t) for t in INPUTS_BASE)


# --------------------------------------------------------------------------- #
# TC-4201..TC-4209, TC-4213, TC-4226..TC-4229 — the tokeniser (HLR-4201)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("code", list(CODES))
def test_TC_4201_each_code_colours_its_inner_text_in_its_tone(code):
    """TC-4201 (LLR-4201.1). `::<c>:: x ::` is one segment `x` in the code's tone, 6/6.
    RED on base: one `mut` segment holding the markers. NC: `b`→`violet` reds 1 arm."""
    assert highlight_segments(f"::{code}:: x ::") == [("x", TONE[code])]


def test_TC_4201_each_code_is_one_span_with_its_code():
    """TC-4201 (LLR-4201.1) at the scanner: `::v:: x ::` → one Span 0/6/7/10, tone
    `violet`, code `v`; the same shape for the other five codes."""
    for code in CODES:
        assert _spans(f"::{code}:: x ::") == [(0, 6, 7, 10, TONE[code], code)], code


@pytest.mark.parametrize("text, segments", [
    ("a ::b:: x :: c", [("a ", "mut"), ("x", "blue"), (" c", "mut")]),
    ("::b::x::", [("x", "blue")]),
    ("::b::  x  ::", [(" x ", "blue")]),
])
def test_TC_4202_one_space_beside_each_marker_belongs_to_the_marker(text, segments):
    """TC-4202 (LLR-4201.2): at most one space after the opener and one before the
    closer are markers; a second space is text. 3/3. NC: keeping the spaces gives " x "
    in arm 1. RED on base: no colour span."""
    assert highlight_segments(text) == segments


def test_TC_4202_the_scanner_gives_str_offsets_of_markers_and_inner():
    """TC-4202 (LLR-4201.2, graph-interfaces example): the markers are
    text[start:inner_start] and text[inner_end:end], spaces included."""
    assert _spans("a ::b:: x :: c") == [(2, 8, 9, 12, "blue", "b")]
    assert _spans("::b::  x  ::") == [(0, 6, 9, 12, "blue", "b")]


def test_TC_4203_inputs_without_colons_tokenise_as_at_base():
    """TC-4203 (LLR-4201.3) — GUARD, passes on base by design. Over the base suite's
    derived set (PIECES × up to 3 = 1 112 inputs, ARCH-12), every input holds no `::`,
    and the new tokeniser returns exactly the base pairs: an old note keeps its colours.
    NC: map `==` to `blue` → RED."""
    assert len(INPUTS_BASE) == 1112
    assert not any("::" in t for t in INPUTS_BASE)
    diffs = [t for t in INPUTS_BASE if highlight_segments(t) != _base_highlight_segments(t)]
    assert not diffs, diffs[:10]
    assert highlight_segments("==y== !!r!!") == [("y", "soon"), (" ", "mut"), ("r", "over")]


def test_TC_4203_a_legacy_span_is_a_span_with_no_code():
    """TC-4203 (graph-interfaces): the one scanner also reports legacy spans, code None,
    so the ink and the palette see `==late==` as one span 0/2/6/8 in `soon`."""
    assert _spans("==late==") == [(0, 2, 6, 8, "soon", None)]


def test_TC_4204_an_open_span_ends_at_the_line_end():
    """TC-4204 (LLR-4201.4): no closer → the span ends at the line end, never crossing a
    line break. 2/2. NC: require a closer → `[("::r:: open","mut")]`. RED on base."""
    assert highlight_segments("::r:: open") == [("open", "over")]
    assert highlight_segments("::r:: a\nb") == [("a", "over"), ("\nb", "mut")]
    assert _spans("::r:: open") == [(0, 6, 10, 10, "over", "r")]
    assert _spans("::r:: a\nb") == [(0, 6, 7, 7, "over", "r")]


@pytest.mark.parametrize("literal", ["std::vector", "a :: b", "::x:: t ::", "::B:: t ::",
                                     "::bb:: t ::"])
def test_TC_4205_a_colon_pair_that_opens_nothing_stays_literal(literal):
    """TC-4205 (LLR-4201.5): a `::` where no opener matches and no span is open is literal
    `mut` text, 5/5 — and stays so BESIDE a working span on the same line (the positive
    control that makes this RED on base, where nothing is coloured). NC: accept any letter
    as a code → arms 3–4 RED."""
    assert highlight_segments(literal) == [(literal, "mut")]
    assert highlight_segments(literal + " ::b:: x ::") == [(literal + " ", "mut"), ("x", "blue")]
    assert _spans(literal) == []


def test_TC_4206_the_next_opener_ends_the_open_span_keeping_its_space():
    """TC-4206 (LLR-4201.6): an open span ends where the next opener starts, the space
    before it kept. Also the pen switch's text (LLR-4203.5). NC: lazy closer only →
    `("r:: y ::","mut")`. RED on base."""
    assert highlight_segments("::b:: x ::r:: y ::") == [("x ", "blue"), ("y", "over")]
    assert highlight_segments("::r:: ab ::::b:: x ::") == [("ab", "over"), ("x", "blue")]
    assert _spans("::b:: x ::r:: y ::") == [(0, 6, 8, 8, "blue", "b"),
                                            (8, 14, 15, 18, "over", "r")]


def test_TC_4207_markers_of_the_other_kind_are_literal_inside_a_span():
    """TC-4207 (LLR-4201.7 as reworded, P-V-2): the first-starting span wins; legacy
    markers inside a colour span and colour markers inside a legacy span are text of that
    span. 2/2. NC: nested tokenising → arm 1 RED (also RED on base)."""
    assert highlight_segments("::b:: ==a== ::") == [("==a==", "blue")]
    assert highlight_segments("==a ::b:: c==") == [("a ::b:: c", "soon")]
    assert _spans("::b:: ==a== ::") == [(0, 6, 11, 14, "blue", "b")]
    assert _spans("==a ::b:: c==") == [(0, 2, 11, 13, "soon", None)]


def test_TC_4208_an_empty_span_shows_nothing():
    """TC-4208 (LLR-4201.8): `a::b::::c` shows `ac`, no segment holds `:`; the fresh pen
    `::b::  ::` is one empty span. NC: `::::` read as literal → `:` appears. RED on base."""
    segs = highlight_segments("a::b::::c")
    assert "".join(s for s, _ in segs) == "ac"
    assert not any(":" in s for s, _ in segs)
    assert segs == [("a", "mut"), ("", "blue"), ("c", "mut")]
    assert _spans("a::b::::c") == [(1, 6, 6, 8, "blue", "b")]
    assert _spans("::b::  ::") == [(0, 6, 6, 9, "blue", "b")]


def test_TC_4209_joined_segments_are_the_text_without_its_markers():
    """TC-4209 (LLR-4201.9, A-5/SEC-9). Over the derived set (10 pieces × up to 4 =
    11 110 inputs): 0 exceptions; the joined segment text equals the reference scanner's
    marker-free text for 100 %; every emitted tone is in the closed set
    {mut, soon, over, green, orange, blue, violet} (the `hl-<tone>` class names of
    notes_html come from it). RED on base: the colour markers stay in the text. NC: drop
    the text between two spans → RED."""
    assert len(DERIVED) == 11110
    errors, wrong, bad_tone = [], [], []
    for t in DERIVED:
        try:
            segs = highlight_segments(t)
        except Exception as exc:                   # noqa: BLE001 — counted, not hidden
            errors.append((t, repr(exc)))
            continue
        if "".join(s for s, _ in segs) != ref_visible(t):
            wrong.append(t)
        bad_tone += [(t, tone) for _s, tone in segs if tone not in CLOSED_TONES]
    assert not errors, errors[:5]
    assert not wrong, [(t, highlight_segments(t), ref_visible(t)) for t in wrong[:5]]
    assert not bad_tone, bad_tone[:5]


def test_TC_4228_spans_are_ordered_disjoint_and_match_the_reference():
    """TC-4228 (LLR-4201.9, LLR-4204.4's input). Over the same 11 110 inputs every Span
    has start <= inner_start <= inner_end <= end, holds no `\\n`, spans are in order and
    disjoint, and they equal the reference scanner's spans for 100 %. RED on base: no
    `colour_spans`."""
    colour_spans = _need(views, "colour_spans")
    shape, wrong = [], []
    for t in DERIVED:
        got = [(s.start, s.inner_start, s.inner_end, s.end, s.tone, s.code)
               for s in colour_spans(t)]
        last = 0
        for s, a, b, e, _tone, _code in got:
            if not (last <= s <= a <= b <= e) or "\n" in t[s:e]:
                shape.append((t, got))
                break
            last = e
        if got != ref_spans(t):
            wrong.append((t, got, ref_spans(t)))
    assert not shape, shape[:5]
    assert not wrong, wrong[:5]


def test_TC_4228_offsets_are_str_indices_not_bytes():
    """TC-4228: non-ASCII text — offsets count code points (é is one), not UTF-8 bytes."""
    assert _spans("é ::b:: café ☕ ::") == [(2, 8, 14, 17, "blue", "b")]
    assert highlight_segments("é ::b:: café ☕ ::") == [("é ", "mut"), ("café ☕", "blue")]


def _median_time(fn, arg, runs=3) -> float:
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


@pytest.mark.parametrize("unit, n_spans", [("::b:: x :: ", None), ("std::", 0),
                                           ("::b::x::", None)])
def test_TC_4213_the_scanner_is_linear_in_the_line(unit, n_spans):
    """TC-4213 (LLR-4201.10, SEC-1): a 100 000-char line of repeated spans, of repeated
    `std::`, and of `!!` + repeated `::b::x::` (one unclosed legacy opener) tokenises in
    <= 250 ms with t(100 000)/t(10 000) <= 20 (median of 3) — and the scanner FINDS the
    spans (the count check is what makes this RED on base, where nothing is coloured).
    NC: the re-search-every-loop scanner (918 ms, ratio ~100) → RED."""
    colour_spans = _need(views, "colour_spans")
    prefix = "!!" if unit == "::b::x::" else ""
    big = prefix + unit * (100_000 // len(unit))
    small = prefix + unit * (10_000 // len(unit))
    want = 100_000 // len(unit) if n_spans is None else 0
    assert len(colour_spans(big)) == want
    assert sum(1 for _s, tone in highlight_segments(big) if tone == "blue") == want
    t_big = _median_time(colour_spans, big)
    t_small = _median_time(colour_spans, small)
    assert t_big <= 0.250, f"{t_big * 1000:.1f} ms for 100 000 chars"
    assert t_big / max(t_small, 1e-6) <= 20, f"ratio {t_big / max(t_small, 1e-6):.1f}"
    assert _median_time(highlight_segments, big) <= 0.250


def test_TC_4226_the_pen_table_is_six_codes_in_pen_order():
    """TC-4226 ([Data: PEN_CODES]): (code, tone, name) in pen order 1..6, each tone a key
    of views.HEX. The legends, pens, palette and ink read this one table."""
    pen_codes = _need(views, "PEN_CODES")
    assert tuple(tuple(p) for p in pen_codes) == tuple(
        (code, TONE[code], NAME[code]) for code in CODES)
    assert all(tone in HEX for _c, tone, _n in pen_codes)


def test_TC_4227_inside_a_colour_span_the_first_double_colon_closes_it():
    """TC-4227 (P-V-4, accepted as designed): `::b:: std::vector ::` shows `std` blue and
    `vector ::` plain. Pinned so a later change of the rule is a decision, not a drift."""
    assert highlight_segments("::b:: std::vector ::") == [("std", "blue"), ("vector ::", "mut")]
    assert _spans("::b:: std::vector ::") == [(0, 6, 9, 11, "blue", "b")]


def test_TC_4229_an_opener_after_a_lone_colon_still_opens():
    """TC-4229 (P-M2-7, ARCH-11): `a:::b:: plan ::` keeps `a:` and colours `plan`; inside
    an open span `:::<c>::` ends it one to the right, the span keeping the `:`."""
    assert highlight_segments("a:::b:: plan ::") == [("a:", "mut"), ("plan", "blue")]
    assert _spans("a:::b:: plan ::") == [(2, 8, 12, 15, "blue", "b")]
    assert highlight_segments("::r:: a :::b:: c ::") == [("a :", "over"), ("c", "blue")]
    assert _spans("::r:: a :::b:: c ::") == [(0, 6, 9, 9, "over", "r"),
                                             (9, 15, 16, 19, "blue", "b")]


# --------------------------------------------------------------------------- #
# TC-4210..TC-4219, TC-4225 — the surfaces and the focus legend (HLR-4202)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("code", ["b", "o", "v"])
def test_TC_4210_the_board_markup_paints_the_span_in_its_hex(code):
    """TC-4210 (LLR-4202.1): `_highlight_markup("::b:: x ::") == c("x","blue")`; same for
    o, v (3/3). RED on base: the markers in `mut`. NC: tone→mut → RED."""
    assert _highlight_markup(f"::{code}:: x ::") == c("x", TONE[code]) == \
        f"[{TONE_HEX[code]}]x[/]"


def _pieces(t: Text) -> list[tuple[str, str]]:
    return [(t.plain[s.start:s.end], str(s.style)) for s in t.spans]


def test_TC_4211_details_and_preview_paint_the_span_in_its_hex():
    """TC-4211 (LLR-4202.2): `notes_text` (the details view) and `notes_preview` (the
    editor preview) give `idea` the style `#a78bfa`. RED on base."""
    for fn in (notes_text, modals.notes_preview):
        t = fn("::v:: idea ::")
        assert t.plain == "idea", fn.__name__
        assert _pieces(t) == [("idea", "#a78bfa")], fn.__name__


def test_TC_4212_a_mention_inside_a_span_stays_bold_pink():
    """TC-4212 (LLR-4202.3): a mention of a person the directory holds is `@Name` bold
    pink inside a colour span; the rest of the span keeps the tone. NC: tone wins over
    the mention → RED. Also the HTML form (notes_html)."""
    t = notes_text("::b:: ask @ana ::", PEOPLE)
    assert t.plain == "ask @Ana Ruiz"
    assert _pieces(t) == [("ask ", "#60a5fa"), ("@Ana Ruiz", "b #f472b6")]
    assert report_html.notes_html("::b:: ask @ana ::", PEOPLE) == \
        '<span class="hl-blue">ask </span><span class="hl-blue mention">@Ana Ruiz</span>'


def test_TC_4214_the_presentation_carries_the_tone_on_every_wrapped_row():
    """TC-4214 (LLR-4202.4): a 62-char `::b::` span wrapped at w=20 → 3 rows, every
    non-blank piece `blue` (the tone is not lost after the first row); a list item keeps
    its lead and its plain tail in `ink`. RED on base: the markers wrap as `ink` text."""
    words = " ".join(f"word{i:02d}" for i in range(9))
    note = f"::b:: {words} ::"
    assert len(note) == 71
    rows = present_note_lines(note, 20)
    assert ["".join(s for s, _ in pieces) for _lead, pieces in rows] == [
        "word00 word01 word02", "word03 word04 word05", "word06 word07 word08"]
    tones = {tone for _lead, pieces in rows for s, tone in pieces if s.strip()}
    assert tones == {"blue"}, rows
    assert present_note_lines("- ::b:: alpha :: bravo", 40) == [
        ("• ", [("alpha", "blue"), (" bravo", "ink")])]
    # the row's markup paints the tone's hex (the presentation's paint seat)
    item = present_note_lines("- ::b:: alpha :: bravo", 40)[0]
    assert f"[{TONE_HEX['b']}]alpha[/]" in _present_note_markup(item, 40)


def test_TC_4216_the_html_notes_write_a_tone_class_and_escape_the_text():
    """TC-4216 (LLR-4202.5): `<span class="hl-blue">&lt;x&gt;</span>` — the class from the
    tone, the text escaped. NC: unescaped → RED. RED on base: `hl-mut` with the markers."""
    assert report_html.notes_html("::b:: <x> ::", {}) == '<span class="hl-blue">&lt;x&gt;</span>'
    html = report_html.notes_html("::v:: idea :: and ::o:: risk ::", {})
    for frag in ('hl-violet">idea', 'hl-mut"> and ', 'hl-orange">risk'):
        assert frag in html, html


def test_TC_4225_the_reports_plain_notes_drop_the_markers():
    """TC-4225: the reports' `notes_text` (search, export) is the visible text."""
    assert report_html._notes_text("::b:: x :: and ==y==\n::r:: z") == "x and y\nz"


def _board(tmp_path, notes: str) -> Board:
    b = Board.load(tmp_path / "board.json")
    b.projects.clear()
    b.tasks.clear()
    p = Project("Field notes", "sky")
    b.projects.append(p)
    b.tasks.append(Task("Write the multicolour note", p.id, "Doing", notes=notes))
    return b


def _extract(b: Board) -> dict:
    return report_html.extract([(None, "Notes board", "sky", b)], {}, {}, TODAY)


def _blocks(css: str) -> dict[str, dict[str, str]]:
    """The deck's theme blocks as {var: value}: `dark` the first `:root{…}`, `light` the
    `@media (prefers-color-scheme:light){ :root{…} }` block, `print` the `@media print`
    root."""
    def vars_of(body: str) -> dict[str, str]:
        return dict(re.findall(r"--([\w-]+):\s*([^;}\s]+)", body))
    dark = re.search(r":root\{color-scheme:light dark;([^}]*)\}", css)
    light = re.search(r"@media \(prefers-color-scheme:light\)\{\s*:root\{([^}]*)\}", css)
    prt = re.search(r"@media print\{\s*:root\{([^}]*)\}", css)
    return {"dark": vars_of(dark.group(1)) if dark else {},
            "light": vars_of(light.group(1)) if light else {},
            "print": vars_of(prt.group(1)) if prt else {}}


def test_TC_4217_the_deck_defines_the_three_new_tone_classes_in_both_themes(tmp_path):
    """TC-4217 (LLR-4202.6): the deck's style sheet holds `.hl-orange`, `.hl-blue`,
    `.hl-violet` reading a colour variable each (3/3), and each variable is set in the
    dark AND the light theme (6/6; print reuses the light block). NC: delete one class →
    RED. RED on base: no rule."""
    html = report_deck.render(_extract(_board(tmp_path, "x")))
    for tone in ("orange", "blue", "violet"):
        assert f".hl-{tone}{{color:var(--{tone})}}" in html, tone
    blocks = _blocks(html)
    for theme in ("dark", "light", "print"):
        for tone in ("orange", "blue", "violet"):
            assert tone in blocks[theme], (theme, tone, sorted(blocks[theme]))
    assert [blocks["dark"][t] for t in ("orange", "blue", "violet")] == \
        [HEX["orange"], HEX["blue"], HEX["violet"]]


def test_TC_4218_the_workspace_defines_the_new_tones_like_hl_soon(tmp_path):
    """TC-4218 (LLR-4202.7): the workspace defines `.hl-orange`, `.hl-blue`, `.hl-violet`
    exactly the way it defines `.hl-soon` (a 22 % color-mix background of one `:root`
    variable), 3/3, and the three variables are in the dark `:root`, 3/3. NC: delete one
    → RED. RED on base."""
    html = report_workspace.render(_extract(_board(tmp_path, "x")))
    soon = re.search(r"\.hl-soon\{([^}]*)\}", html)
    assert soon and "22%" in soon.group(1), "the .hl-soon model rule moved"
    root = re.search(r":root\{color-scheme:light dark;([^}]*)\}", html).group(1)
    for tone in ("orange", "blue", "violet"):
        want = ".hl-%s{%s}" % (tone, soon.group(1).replace("--soon", f"--{tone}"))
        assert want in html, want
        assert f"--{tone}:{HEX[tone]}" in root, (tone, root)


def test_TC_4219_the_focus_legend_lists_the_six_codes_in_their_tones(tmp_path):
    """TC-4219 (LLR-4202.8): with a pinned task, the Focus legend holds ONE row whose
    swatch paints each code letter in its tone (6/6, in pen order) and the `::`; the
    three legacy rows stay exactly as at base. NC: legend unchanged → RED (RED on base)."""
    b = _board(tmp_path, "::b:: x ::")
    b.tasks[0].pinned = True
    entries = legend_entries("focus", b, TODAY)
    rows = [(sw, meaning) for sw, meaning in entries
            if all(TONE_HEX[k] in sw for k in CODES)]
    assert len(rows) == 1, entries
    sw = rows[0][0]
    assert "::" in Text.from_markup(sw).plain
    marks = [sw.index(f"[{TONE_HEX[k]}]{k}[/]") for k in CODES]
    assert marks == sorted(marks), sw                       # pen order r o y g b v
    for legacy in [(c("==text==", "soon"), "highlight: yellow / warning"),
                   (c("!!text!!", "over"), "highlight: red / attention"),
                   (c("++text++", "green"), "highlight: green / resolved")]:
        assert legacy in entries
    b.tasks[0].pinned = False
    assert not [sw for sw, _m in legend_entries("focus", b, TODAY)
                if all(TONE_HEX[k] in sw for k in CODES)]  # nothing pinned: no colour row


# --------------------------------------------------------------------------- #
# TC-4220..TC-4224 — the six tones survive the palette (HLR-4206, C-4)
# --------------------------------------------------------------------------- #
def _rgb(hex_: str) -> tuple[float, float, float]:
    h = hex_.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _luminance(hex_: str) -> float:
    """WCAG 2.x relative luminance."""
    def lin(u):
        return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(u) for u in _rgb(hex_))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    hi, lo = sorted((_luminance(fg), _luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def saturation(hex_: str) -> float:
    return colorsys.rgb_to_hls(*_rgb(hex_))[2]


def _shipped_tones() -> dict[str, str]:
    """The hex each code is PAINTED in by the details view (the terminal seat of the six
    tones), read from the rendered Text — not from a table. Precondition of every C-4
    check: six codes, six distinct hexes (RED on base, where all six are `mut`)."""
    out = {}
    for code in CODES:
        t = notes_text(f"::{code}:: x ::")
        assert t.plain == "x", f"::{code}:: x :: is not tokenised: {t.plain!r}"
        out[code] = str(t.spans[0].style).lower()
    assert len(set(out.values())) == 6, out
    return out


def test_C4_the_oracle_functions_are_right():
    """Self-check of the C-4 oracles on known values (passes on base by construction)."""
    assert round(contrast("#ffffff", "#000000"), 2) == 21.0
    assert round(contrast("#5b6675", "#0d1117"), 2) < 4.5           # the NC of LLR-4206.2
    assert saturation("#8b98a5") < 0.15                            # the NC of LLR-4206.1


def test_TC_4220_every_tone_is_saturated():
    """TC-4220 (LLR-4206.1): HLS saturation >= 0.20 for 6/6 (0.15 is the cliff, P-V-3).
    NC: `#8b98a5` (s≈0.126) → RED."""
    tones = _shipped_tones()
    assert tones == TONE_HEX
    low = {k: round(saturation(h), 3) for k, h in tones.items() if saturation(h) < 0.20}
    assert not low, low


def test_TC_4221_every_tone_reads_on_both_terminal_backgrounds():
    """TC-4221 (LLR-4206.2): contrast >= 4.5:1 on `#0d1117` (app) and `#0b111a`
    (preview), 12/12. NC: `#5b6675` → RED."""
    tones = _shipped_tones()
    bad = [(k, bg, round(contrast(h, bg), 2)) for k, h in tones.items()
           for bg in ("#0d1117", "#0b111a") if contrast(h, bg) < 4.5]
    assert not bad, bad


def test_TC_4222_the_256_colour_downgrade_keeps_six_distinct_non_greys():
    """TC-4222 (LLR-4206.3): under rich's 8-bit downgrade the six tones are six distinct
    colour numbers, none in the grey ramp 232–255 nor on the cube's grey diagonal.
    NC: `orange` = `soon` → RED."""
    nums = {k: Color.parse(h).downgrade(ColorSystem.EIGHT_BIT).number
            for k, h in _shipped_tones().items()}
    assert len(set(nums.values())) == 6, nums
    assert not [n for n in nums.values() if 232 <= n <= 255 or n in (16, 59, 102, 145, 188, 231)]


def test_TC_4223_no_tone_is_the_accent():
    """TC-4223 (LLR-4206.4): 0/6 tones equal the accent `#2dd4bf`. NC: g→accent → RED."""
    assert HEX["accent"] not in _shipped_tones().values()


def test_TC_4224_the_decks_tone_variables_read_on_their_themes_background(tmp_path):
    """TC-4224 (LLR-4206.5): each of the deck's six tone variables (soon, over, green,
    orange, blue, violet) has contrast >= 4.5:1 on its theme's `--bg`, dark and light,
    12/12. NC: light `--blue:#60a5fa` on `#ffffff` (2.5:1) → RED. RED on base: three of
    the six variables are absent."""
    blocks = _blocks(report_deck.render(_extract(_board(tmp_path, "x"))))
    bad, missing = [], []
    for theme in ("dark", "light"):
        bg = blocks[theme].get("bg")
        assert bg, (theme, blocks[theme])
        for tone in ("soon", "over", "green", "orange", "blue", "violet"):
            v = blocks[theme].get(tone)
            if v is None:
                missing.append((theme, tone))
            elif contrast(v, bg) < 4.5:
                bad.append((theme, tone, v, round(contrast(v, bg), 2)))
    assert not missing, missing
    assert not bad, bad


# --------------------------------------------------------------------------- #
# AT-4203 — the HTML export (HLR-4202)
# --------------------------------------------------------------------------- #
def test_AT_4203_the_exported_workspace_and_deck_hold_the_colours(tmp_path):
    """AT-4203 (HLR-4202): a board whose note is `::v:: idea :: and ::o:: risk ::`,
    exported through the `H` path's own writer (`report_html.extract` +
    `write_reports`): the deck FILE holds the `hl-violet` and `hl-orange` spans and both
    CSS rules; the workspace FILE's embedded data holds the same spans and its CSS both
    rules. RED on base: the spans are `hl-mut` with the markers, and no rule exists."""
    b = _board(tmp_path, "::v:: idea :: and ::o:: risk ::")
    paths = report_html.write_reports(_extract(b), ("workspace", "deck"), tmp_path / "out",
                                      TODAY)
    files = {p.name.split("-")[0]: p.read_text(encoding="utf-8") for p in paths}
    assert set(files) == {"workspace", "deck"}
    spans = ('<span class="hl-violet">idea</span>', '<span class="hl-orange">risk</span>')
    deck = files["deck"]
    for s in spans:
        assert s in deck, s
    for tone in ("violet", "orange"):
        assert f".hl-{tone}{{color:var(--{tone})}}" in deck
    ws = files["workspace"]
    data = json.loads(re.search(r'<script id="board-data" type="application/json">(.*?)</script>',
                                ws, re.S).group(1))
    notes = [t["notes_html"] for t in data["tasks"]]
    assert any(all(s in n for s in spans) for n in notes), notes
    for tone in ("violet", "orange"):
        assert f".hl-{tone}{{background:color-mix(in srgb,var(--{tone}) 22%" in ws, tone


# --------------------------------------------------------------------------- #
# AT-4204 — legacy notes render byte-identically to base (frozen oracle)
# --------------------------------------------------------------------------- #
# Captured by running the base tree 0a8dfaa (C:/Users/jjgh8/Github/taskboard-wt/incC-base)
# through the surfaces below, on 2026-11-01, by this tester. Do not regenerate from the
# code under test.
LEGACY_NOTES = {
    "at4204": ("==a== !!b!! ++c++ std::vector", None),
    "mixed": ("- time 10::30 ==late== a :: b\n\n!!stop!! ask @ana ++ok++ x::y", PEOPLE),
}
BASE_ORACLE = {
    'at4204': {'board': ['[#fbbf24]a[/][#8b98a5] [/][#f43f5e]b[/][#8b98a5] [/][#4ade80]c[/][#8b98a5] '
                         'std::vector[/]'],
               'details': ('a b c std::vector',
                           [(0, 1, '#fbbf24'),
                            (1, 2, '#8b98a5'),
                            (2, 3, '#f43f5e'),
                            (3, 4, '#8b98a5'),
                            (4, 5, '#4ade80'),
                            (5, 17, '#8b98a5')]),
               'html': '<span class="hl-soon">a</span><span class="hl-mut"> </span><span '
                       'class="hl-over">b</span><span class="hl-mut"> </span><span '
                       'class="hl-green">c</span><span class="hl-mut"> std::vector</span>',
               'html_text': 'a b c std::vector',
               'present_markup': ['[#8b98a5][/][#fbbf24]a[/][#e6edf3] [/][#f43f5e]b[/][#e6edf3] '
                                  '[/][#4ade80]c[/][#e6edf3] std::vector[/]             '],
               'present_rows': [('',
                                 [('a', 'soon'),
                                  (' ', 'ink'),
                                  ('b', 'over'),
                                  (' ', 'ink'),
                                  ('c', 'green'),
                                  (' std::vector', 'ink')])],
               'preview': ('a b c std::vector',
                           [(0, 1, '#fbbf24'),
                            (1, 2, '#8b98a5'),
                            (2, 3, '#f43f5e'),
                            (3, 4, '#8b98a5'),
                            (4, 5, '#4ade80'),
                            (5, 17, '#8b98a5')]),
               'snippet': '[#fbbf24]a[/][#8b98a5] [/][#f43f5e]b[/][#8b98a5] [/][#4ade80]c[/][#8b98a5] '
                          'std::vector[/]'},
    'mixed': {'board': ['[#8b98a5]- time 10::30 [/][#fbbf24]late[/][#8b98a5] a :: b[/]',
                        '[#8b98a5][/]',
                        '[#f43f5e]stop[/][#8b98a5] ask @ana [/][#4ade80]ok[/][#8b98a5] x::y[/]'],
              'details': ('- time 10::30 late a :: b\n\nstop ask @Ana Ruiz ok x::y',
                          [(0, 14, '#8b98a5'),
                           (14, 18, '#fbbf24'),
                           (18, 25, '#8b98a5'),
                           (27, 31, '#f43f5e'),
                           (31, 36, '#8b98a5'),
                           (36, 45, 'b #f472b6'),
                           (45, 46, '#8b98a5'),
                           (46, 48, '#4ade80'),
                           (48, 53, '#8b98a5')]),
              'html': '<span class="hl-mut">- time 10::30 </span><span class="hl-soon">late</span><span '
                      'class="hl-mut"> a :: b</span><br><br><span class="hl-over">stop</span><span '
                      'class="hl-mut"> ask </span><span class="hl-mut mention">@Ana Ruiz</span><span '
                      'class="hl-mut"> </span><span class="hl-green">ok</span><span class="hl-mut"> x::y</span>',
              'html_text': '- time 10::30 late a :: b\n\nstop ask @ana ok x::y',
              'present_markup': ['[#8b98a5]• [/][#e6edf3]time 10::30 [/][#fbbf24]late[/][#e6edf3] a :: '
                                 'b[/]     ',
                                 '[#8b98a5][/][#e6edf3][/]                              ',
                                 '[#8b98a5][/][#f43f5e]stop[/][#e6edf3] ask [/][b #f472b6]@Ana\xa0'
                                 'Ruiz[/][#e6edf3] [/][#4ade80]ok[/][#e6edf3] x::y[/]    '],
              'present_rows': [('• ', [('time 10::30 ', 'ink'), ('late', 'soon'), (' a :: b', 'ink')]),
                               ('', []),
                               ('',
                                [('stop', 'over'),
                                 (' ask @Ana\xa0Ruiz ', 'ink'),
                                 ('ok', 'green'),
                                 (' x::y', 'ink')])],
              'preview': ('- time 10::30 late a :: b\n\nstop ask @Ana Ruiz ok x::y',
                          [(0, 14, '#8b98a5'),
                           (14, 18, '#fbbf24'),
                           (18, 25, '#8b98a5'),
                           (27, 31, '#f43f5e'),
                           (31, 36, '#8b98a5'),
                           (36, 45, 'b #f472b6'),
                           (45, 46, '#8b98a5'),
                           (46, 48, '#4ade80'),
                           (48, 53, '#8b98a5')]),
              'snippet': '[#8b98a5]- time 10::30 [/][#fbbf24]late[/][#8b98a5] a :: b …[/]'},
}


def _all_spans(t: Text):
    return (t.plain, [(s.start, s.end, str(s.style)) for s in t.spans])


@pytest.mark.parametrize("case", sorted(LEGACY_NOTES))
def test_AT_4204_legacy_notes_render_as_at_base(case):
    """AT-4204 — GUARD, passes on base by design. A note written before this increment
    (`==a== !!b!! ++c++ std::vector`, and a mixed note with `10::30`, `a :: b`, `x::y`,
    a mention and a blank line) renders on the board (markup and Focus snippet), the
    details view, the editor preview, the presentation (rows and markup) and the HTML
    notes byte-identically to the frozen base oracle. RED under any change of a legacy
    tone, marker or a `::` that starts reading as an opener."""
    note, people = LEGACY_NOTES[case]
    want = BASE_ORACLE[case]
    rows = present_note_lines(note, 30, people)
    got = {
        "board": [_highlight_markup(ln) for ln in note.split("\n")],
        "snippet": _focus_note_snippet(note, 40),
        "details": _all_spans(notes_text(note, people)),
        "preview": _all_spans(modals.notes_preview(note, people)),
        "present_rows": rows,
        "present_markup": [_present_note_markup(r, 30, mention_marks(people)) for r in rows],
        "html": report_html.notes_html(note, people or {}),
        "html_text": report_html._notes_text(note),
    }
    for seat in want:
        assert got[seat] == want[seat], seat
