"""The detector must be able to FAIL, and both halves are tested together.

WHY THIS FILE EXISTS: a privacy sweep that reports "clean" is worthless unless
something proves it would have said otherwise. Two failure modes are possible
and they are opposites, so neither test alone is sufficient:

  - a sweeper that never matches reports every tree clean  -> the planted-leak
    tests catch it;
  - a sweeper that matches everything reports every tree dirty -> the clean-tree
    and common-word tests catch it.

THE TRUNCATED CASE IS A REGRESSION, NOT A HYPOTHETICAL. On 2026-08-07 a hand
scrub replaced the whole token `Telemetry_Ingestion` across a branch and six
rewritten commits were declared clean. `tests/test_app.py` still asserted on
`Telemetry_Ingestio` -- the same name minus one letter, written that way because
the gantt label column ellipsises. The suite caught it; the scrub had not.
`test_a_name_that_reached_the_file_truncated_is_still_found` is that day.

NOTHING HERE READS THE OPERATOR'S BOARD. Every fixture is built in tmp_path, so
these tests are deterministic on any machine and cannot themselves leak. The
sweep against the real board is an operator-run command, deliberately NOT a
test: a test that reads `~/.taskboard/board.json` would auto-skip wherever that
file is absent, and a guard that silently skips is the vacuous check this repo
has already recorded as an anti-pattern.
"""

import json

import pytest

from tools.privacy_sweep import MIN_PREFIX, board_strings, prefixes, sweep

REAL_TITLE = "Telemetry_Ingestion_Navigation"
SHORTER_TITLE = "Telemetry_Ingestion"   # a strict prefix of REAL_TITLE
REAL_PROJECT = "Atlas Pipeline (ML)"


@pytest.fixture
def board(tmp_path):
    """A stand-in for a private board. Same SHAPE as the real one; none of its
    content is real."""
    p = tmp_path / "board.json"
    p.write_text(json.dumps({
        "projects": [{"name": REAL_PROJECT}, {"name": "Corvus Sessions"},
                     {"name": "Lab"}],
        # SHORTER_TITLE is a strict prefix of REAL_TITLE ON PURPOSE. Without a
        # nesting pair in the fixture, sort order cannot change any outcome and
        # `test_the_longest_match_is_reported_not_a_prefix_of_it` is vacuous --
        # which is exactly what the mutation harness caught it being.
        "tasks": [{"title": REAL_TITLE}, {"title": SHORTER_TITLE},
                  {"title": "Step 2 - Object store with named volume mounts"},
                  {"title": "Fix"}],
    }), encoding="utf-8")
    return p


def write(tmp_path, name, text):
    f = tmp_path / name
    f.write_text(text, encoding="utf-8")
    return f


def test_a_planted_whole_name_is_found(board, tmp_path):
    """THE FIRST HALF. Without this the sweeper may simply never match."""
    f = write(tmp_path, "leak.md", f"the batch renamed {REAL_TITLE} last week")
    assert sweep(board, [f]) == {str(f): REAL_TITLE}


def test_a_name_that_reached_the_file_truncated_is_still_found(board, tmp_path):
    """THE REGRESSION OF 2026-08-07. `Telemetry_Ingestio` -- one letter short,
    because the label column ellipsises -- survived a scrub that replaced the
    whole token, and six rewritten commits were called clean while carrying it.

    Written as a loop over every truncation down to the documented floor rather
    than against the one length that actually bit, because the ellipsis lands
    wherever the column width puts it. Deleting `prefixes()` reddens this and
    leaves the whole-name test above green -- which is exactly the shape of the
    bug it is guarding."""
    for cut in range(len(REAL_TITLE) - 1, MIN_PREFIX - 1, -1):
        truncated = REAL_TITLE[:cut]
        f = write(tmp_path, f"leak_{cut}.md", f"row shows {truncated}… here")
        assert sweep(board, [f]) == {str(f): REAL_TITLE}, (
            f"a name truncated to {cut} chars went unseen")


def test_a_clean_tree_reports_nothing(board, tmp_path):
    """THE SECOND HALF, and the one that catches the lazy detector. A sweeper
    that flags everything would pass every test above."""
    files = [write(tmp_path, "a.md", "the gantt draws a week guide at monday"),
             write(tmp_path, "b.py", "def render(board, width): return width")]
    assert sweep(board, files) == {}


def test_an_ordinary_word_from_a_real_name_is_not_a_leak(board, tmp_path):
    """`Training` and `Homelab` appear inside private names, but on their own
    they identify nothing. Flagging them would drown the real findings and
    train the reader to ignore the report -- which is how a sweep stops being
    read at all. This is the cost side of MIN_PREFIX and it is tested."""
    f = write(tmp_path, "ok.md", "Training runs nightly on the Homelab GPU box")
    assert sweep(board, [f]) == {}


def test_a_short_record_is_not_protected_and_the_floor_is_stated(board, tmp_path):
    """`Lab` and `Fix` are in the board and are deliberately NOT matched: below
    MIN_STRING they are words, not identifiers. The sweeper's blind spot is
    asserted rather than left for a reader to discover."""
    assert REAL_TITLE in board_strings(board)
    assert "Lab" not in board_strings(board)
    assert "Fix" not in board_strings(board)
    f = write(tmp_path, "short.md", "the Lab will Fix it")
    assert sweep(board, [f]) == {}


def test_prefixes_stop_at_the_documented_floor():
    """The floor is a promise the module makes in its docstring; a change to
    MIN_PREFIX that widens sensitivity silently would break the no-over-report
    test above, and this pins the shape directly."""
    got = prefixes(REAL_TITLE)
    assert got[0] == REAL_TITLE
    assert min(len(s) for s in got) == MIN_PREFIX
    assert all(REAL_TITLE.startswith(s) for s in got)


def test_binary_suffixes_are_skipped_not_silently_decoded(board, tmp_path):
    """A `.png` that happens to contain the bytes of a name is not a readable
    leak, and decoding every image would make the sweep unusable on a repo with
    assets. Skipping is deliberate; asserting it stops the skip list from being
    quietly widened to something that DOES carry text."""
    f = write(tmp_path, "shot.png", REAL_TITLE)
    assert sweep(board, [f]) == {}
    g = write(tmp_path, "shot.svg", REAL_TITLE)
    assert sweep(board, [g]) == {str(g): REAL_TITLE}, (
        "svg is text and MUST be swept -- rich writes captures as svg")


def test_the_longest_match_is_reported_not_a_prefix_of_it(board, tmp_path):
    """One leaked title also matches all of its own prefixes, and a board can
    hold two records where one NESTS inside the other. Reporting the shorter
    one names the wrong record: a reader told `Telemetry_Ingestion` leaked
    would look for the wrong task and could conclude the longer one is safe.

    This needs the nesting pair in the fixture to bite. Written first without
    it, the test passed under a mutation that removed the longest-first sort
    entirely -- it was asserting nothing."""
    order = board_strings(board)
    assert SHORTER_TITLE in order
    assert order.index(REAL_TITLE) < order.index(SHORTER_TITLE), \
        "the longer record must be tried first, or the shorter one shadows it"
    f = write(tmp_path, "one.md", f"the row reads {REAL_TITLE} today")
    assert sweep(board, [f]) == {str(f): REAL_TITLE}, (
        "reported a prefix instead of the record that actually leaked")
