"""Bottom status ribbon: local time, date, ISO week, and two custom clocks.

The two custom clocks use FIXED UTC offsets (no DST) and are chosen in-app from
the `c` menu (see modals.ClockModal); the selection is persisted in board.json.
Updated once per second by the app's single shared ``set_interval`` (pitfall:
one clock interval for the whole app, never one per widget).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from textual.widgets import Static

from .models import DEFAULT_CLOCK1, DEFAULT_CLOCK2, ZONE_OFFSETS
from .views import HEX


def _c(text: str, key: str, bold: bool = False) -> str:
    b = "b " if bold else ""
    return f"[{b}{HEX[key]}]{text}[/]"


def clock_hhmm(offset_minutes: int, utc_now: datetime) -> str:
    """A fixed-offset clock's HH:MM for a given UTC instant (pure / testable)."""
    return (utc_now + timedelta(minutes=offset_minutes)).strftime("%H:%M")


class Ribbon(Static):
    """A one-line docked status bar. The app sets the two clock keys on mount."""

    clock1_key: str = DEFAULT_CLOCK1
    clock2_key: str = DEFAULT_CLOCK2

    def on_mount(self) -> None:
        self.update_clock()

    def update_clock(self, now: datetime | None = None) -> str:
        now = now or datetime.now()
        utc_now = datetime.now(timezone.utc)
        week = f"W{now.isocalendar().week:02d}"
        parts = [
            _c(now.strftime("%H:%M:%S"), "accent", bold=True),
            _c(now.strftime("%a %d %b %Y"), "ink"),
            _c(week, "amber"),
        ]
        for key in (self.clock1_key, self.clock2_key):
            offset = ZONE_OFFSETS.get(key, 0)
            parts.append(_c(key, "mut") + " " + _c(clock_hhmm(offset, utc_now), "accent"))
        sep = _c(" · ", "frame")
        markup = " " + sep.join(parts) + " "
        self.update(markup)
        return markup
