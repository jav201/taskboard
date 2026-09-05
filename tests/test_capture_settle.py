"""`capture_languages.settle()` must wait for the HERO BAND, not only the board.

WHY THIS FILE EXISTS. F-1 was a capture that came back different from one run
to the next -- 6 of 22 frames drifting over 30 fresh-interpreter sweeps, two
independent sweeps disagreeing 58.9 % of the time
(`.fast-dev-flow/03-increments/race-probe.md`). The probe's §5 diffed the bad
grids and the largest one was not the cards: it was rows 3-12 of
`board_darkside.txt`, the hero band, composed at a seat it no longer had.

The reason that could happen is structural, and it is what this file pins. The
capture's settle asked one question -- "is the frame the same as last time?" --
and a widget waiting on a deferred fill produces a genuinely static frame WHILE
IT WAITS. The hero is `Hero(id="hero")`, mounted beside the board rather than
inside it, so it carries none of the four `BOARD_CONTENT` classes and neither
the harness's condition A nor its condition C was ever watching it.

THE FIXTURE IS SYNTHETIC AND ITS CLOCK IS THE READ COUNT, both deliberately.
Driving the real board would make the test a race against a worker, and a test
that is a race cannot fail for exactly one reason. Chaining `call_after_refresh`
was tried first and does not work as a delay at all -- measured: ONE
`pilot.pause()` drains about twenty thousand chained callbacks, because the
chain is a busy loop and not a wait. So the moment the hero fills is pinned to
a READ: `settle` reads the composited frame exactly once per iteration, the
fixture arms itself on the fifth of those, and the fill itself still lands
through `call_after_refresh` -- the same deferral `TaskCard.on_mount` and
`KanbanBoard._seed_detail` use. Read 5 sits after the old condition's three and
far inside `MAX_SETTLE`, so both assertions below are facts about the
conditions rather than about how fast this machine happens to be.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Static

ROOT = Path(__file__).resolve().parents[1]

# `capture_languages` sets `TEXTUAL_ANIMATIONS=none` at import, for the whole
# process -- correct for a capture, and not this suite's to inherit. Snapshot
# and restore around the import, so the tests that run after this file see the
# animation policy they were written against.
_ANIM = os.environ.get("TEXTUAL_ANIMATIONS")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes"))
import capture_languages as CL                                    # noqa: E402
if _ANIM is None:
    os.environ.pop("TEXTUAL_ANIMATIONS", None)
else:                                                    # pragma: no cover
    os.environ["TEXTUAL_ANIMATIONS"] = _ANIM

#: the read on which the fixture's hero starts filling. Strictly greater than
#: the three reads the OLD condition needed, so assertion (a) is not a
#: coincidence; far below `MAX_SETTLE`, so assertion (b) is about waiting and
#: not about timing out.
ARM_ON_READ = 5
OLD_STABLE_READS = 3                    # the constant as it stood at 16792b5

HERO_TEXT = "2  Fix checkout 500 error"


class LateHero(Static):
    """A hero band that fills the way the real one does: not at mount."""

    def arm(self) -> None:
        self.call_after_refresh(lambda: self.update(HERO_TEXT))


class LateHeroApp(App):
    """One painted band and one deferred one.

    The header matters: without it the whole frame is blank and the old settle
    would raise "frame settled BLANK" instead of doing the thing this file is
    about -- signing off on a frame that has ink somewhere and none in the band
    carrying the signature metric.
    """
    CSS = ("Screen { layout: vertical; }\n"
           "#head { height: 1; }\n"
           "#hero { height: 3; }")

    def compose(self) -> ComposeResult:
        yield Static("TASKBOARD", id="head")
        yield LateHero(id="hero")


def arm_on_fifth_read(monkeypatch) -> dict:
    """Make the hero fill on read `ARM_ON_READ`, and count the reads.

    Both settles below read the frame through `CL.screen_text`, so one hook
    gives the two arms the same clock -- which is what makes them comparable
    rather than two separate experiments.
    """
    counter = {"n": 0}
    real = CL.screen_text

    def counting(app):
        counter["n"] += 1
        if counter["n"] == ARM_ON_READ:
            app.query_one("#hero", LateHero).arm()
        return real(app)

    monkeypatch.setattr(CL, "screen_text", counting)
    return counter


async def _settle_b_only(pilot, app, label: str) -> list[str]:
    """The settle as it stood at `16792b5`: condition B, three identical reads.

    Quoted here rather than reached for through git, because assertion (a)'s
    job is to keep proving the fixture has teeth long after that commit stops
    being anyone's memory. If a future change lets the hero fill early, THIS is
    the assertion that goes red first.
    """
    stable = 0
    prev: list[str] | None = None
    for _ in range(CL.MAX_SETTLE):
        await pilot.pause()
        rows = CL.screen_text(app)
        stable = stable + 1 if rows == prev else 0
        prev = rows
        if stable < OLD_STABLE_READS - 1:
            continue
        if not any(r.strip() for r in rows):
            raise RuntimeError(f"{label}: frame settled BLANK")
        return rows
    raise RuntimeError(f"{label}: never settled")            # pragma: no cover


def hero_band(app, rows: list[str]) -> str:
    r = app.query_one("#hero").region
    return "\n".join(rows[r.y: r.y + r.height])


async def test_the_old_settle_signs_off_on_a_blank_hero_band(monkeypatch):
    """(a) The fixture has teeth: B alone returns a frame with an EMPTY hero.

    This is F-1's mechanism in one screen. The frame is static, it is not
    blank, and it is wrong -- which is why "two identical reads" and "three
    identical reads" were both answers to the wrong question.
    """
    reads = arm_on_fifth_read(monkeypatch)
    app = LateHeroApp()
    async with app.run_test(size=(40, 8)) as pilot:
        rows = await _settle_b_only(pilot, app, "late hero")
        band = hero_band(app, rows)
        assert "TASKBOARD" in "\n".join(rows), "the frame must not be blank"
        assert reads["n"] < ARM_ON_READ, (
            "the old settle read past the arming point, so this proves "
            f"nothing about it -- {reads['n']} reads")
        assert not band.strip(), (
            "the fixture no longer reproduces F-1: the hero band was already "
            f"painted when the OLD settle signed off -- {band!r}")


async def test_settle_waits_for_the_hero_band(monkeypatch):
    """(b) The shipped settle waits for it.

    Condition A reads `#hero` alongside the four classes the board mounts, so
    a band the compositor is drawing that carries no ink is not a settled
    frame, however many identical reads precede it.
    """
    reads = arm_on_fifth_read(monkeypatch)
    app = LateHeroApp()
    async with app.run_test(size=(40, 8)) as pilot:
        rows = await CL.settle(pilot, app, "late hero")
        band = hero_band(app, rows)
        assert HERO_TEXT in band, (
            f"settle signed off before the hero band painted -- {band!r}")
        assert reads["n"] > ARM_ON_READ, reads["n"]


async def test_settle_names_the_widget_it_gave_up_on():
    """A timeout must point at a widget, not at "the board".

    Nothing arms the band here, so `MAX_SETTLE` is reached with condition A
    still red. Worth a test rather than a comment because the old failure text
    was `never settled after 40 frames`, which sends the next reader hunting
    through the whole tree; and because it is the other half of (b) -- a settle
    that returned here would be signing off on an unpainted band.
    """
    app = LateHeroApp()
    async with app.run_test(size=(40, 8)) as pilot:
        try:
            await CL.settle(pilot, app, "never")
        except RuntimeError as e:
            assert "hero" in str(e) and "BLANK" in str(e), str(e)
        else:                                             # pragma: no cover
            raise AssertionError("settle returned on an unpainted hero band")


# ---------------------------------------------------------------------------
# THE SIGNATURE PIN (inc21) — the capture must not read a timestamp git does
# not carry.
#
# `taskboard/engine.py:sig_board_file` ages the board file with
# `(time.time() - p.stat().st_mtime) / 60`. `freeze_clock()` pins the first
# term and the CHECKOUT pins the second, so before the pin the committed frames
# carried `f -98` and a fresh checkout of the same tree rendered `f -46982` —
# deterministically, in every run, in every language whose signal row shows the
# board-file tile. That is eleven of the twenty-two frames unreproducible by
# anyone who clones the repo.
#
# WHY THIS RUNS IN A SUBPROCESS. `freeze_clock()` rebinds `datetime` and `date`
# inside every imported taskboard module and swaps a shim over
# `engine.time` — deliberately global, because the capture has to photograph
# the shipping code rather than a variant of it. Doing that inside the pytest
# process would leave the other 684 tests running against a frozen clock. A
# fresh interpreter is also the honest condition: it is what a rebuild a week
# from now actually has.
# ---------------------------------------------------------------------------
import subprocess                                                 # noqa: E402

PIN_PROBE = """
import os, sys, time
sys.path.insert(0, {root!r})
sys.path.insert(0, {proto!r})
sys.path.insert(0, {slice_!r})
import capture_languages as CL
import app, kanban                       # freeze_clock patches these by name
os.utime(CL.FIXTURE, (time.time(), time.time()))   # whatever a checkout left
CL.freeze_clock()
from taskboard.engine import sig_board_file
r = sig_board_file(None)                 # the signal ignores its context
print(r.value, "|", r.caption)
"""


def test_the_board_file_signal_does_not_read_the_checkout_clock():
    """The cell that reaches eleven frames, asked of a fresh interpreter.

    The probe deliberately stamps the fixture with the CURRENT time first, so
    it starts from the worst case the defect produces — a file that was just
    written — and then checks that `freeze_clock()` overrides it. Asserting the
    rendered VALUE rather than the mtime is what makes this a test of the frame
    instead of a test of a call: `int(age_min)` is what lands in the grid, and
    `FIXTURE_AGE_S` is 450 rather than 420 exactly so that a float timestamp
    round-tripping through the filesystem cannot flip it to the minute below.
    """
    out = subprocess.run(
        [sys.executable, "-X", "utf8", "-c",
         PIN_PROBE.format(root=str(ROOT), proto=str(ROOT / "prototypes"),
                          slice_=str(ROOT / "prototypes" / "widget_slice"))],
        capture_output=True, text=True,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    assert out.returncode == 0, out.stderr[-2000:]
    assert out.stdout.strip() == f"{CL.FIXTURE_AGE_S // 60} | min since save", (
        out.stdout, out.stderr[-500:])
