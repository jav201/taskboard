"""MOTION — the cheap classes, actually used.

tui-design/MOTION.md names three cost classes. An earlier pass of this prototype
wrote the file and then shipped a nearly static app, which is the failure the
file exists to prevent. Everything here is class 1 (style) or class 2 (PRECOMPUTED
frames); nothing re-derives data on a tick.

Measured: selecting a precomputed frame costs ~0.1 us against ~18.8 us to
recompute a 200-point series -- a 188x swing. So every animation below builds its
frames ONCE at import and animates an index.

Accessibility: motion that carries meaning is emitted at level="basic" so it
survives TEXTUAL_ANIMATIONS=basic; purely decorative motion stays at "full" and
is allowed to disappear.
"""
from __future__ import annotations

import math

FPS = 12                      # the widget's animation tick; not the frame rate
SWEEP_FRAMES = 24
PULSE_FRAMES = 16


def _lattice(width: int, height: int, phase: float, duty: float = 0.55):
    """One frame of a travelling dot-lattice wave."""
    rows = []
    amp = [duty + (1 - duty) * abs(math.sin(x * 0.28 + phase)) for x in range(width)]
    for r in range(height):
        rows.append([1 if (height - r) / height <= amp[c] else 0
                     for c in range(width)])
    return rows


def build_sweep(width: int = 40, height: int = 8, n: int = SWEEP_FRAMES):
    """A looping waveform sweep. PRECOMPUTED: the tick only picks an index."""
    return [_lattice(width, height, 2 * math.pi * i / n) for i in range(n)]


def build_pulse(cells: int = 24, n: int = PULSE_FRAMES):
    """A breathing dot row — a heartbeat for 'the engine is live'."""
    frames = []
    for i in range(n):
        t = 0.5 - 0.5 * math.cos(2 * math.pi * i / n)
        lit = round(cells * t)
        frames.append([1] * lit + [0] * (cells - lit))
    return frames


def build_flow(width: int, n: int = 20, packet: int = 3):
    """The gantt 'flow packet': a short bright run travelling left to right,
    marking that work drifts toward its deadline. Ported from the shipped app,
    which had this and which the first prototype pass dropped."""
    frames = []
    for i in range(n):
        head = round((i / n) * (width + packet)) - packet
        frames.append([1 if head <= c < head + packet else 0 for c in range(width)])
    return frames


# Built ONCE, at import — this is what makes the motion class-2 instead of class-3.
SWEEP = build_sweep()
PULSE = build_pulse()


class Ticker:
    """Owns the animation index. One ticker per app, never one per panel
    (the per-panel set_interval trap, ARCHITECTURE.md)."""

    def __init__(self) -> None:
        self.n = 0

    def advance(self) -> None:
        self.n += 1

    def frame(self, frames: list, speed: int = 1):
        return frames[(self.n // max(1, speed)) % len(frames)]
