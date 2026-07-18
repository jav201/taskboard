"""Bottom status ribbon: local time, date, ISO week, and two city clocks.

The two clocks are chosen by CITY from the `c` menu (see modals.ClockModal) and
show real, DST-aware local time via ``zoneinfo``. The chosen cities persist in
board.json. Updated once per second by the app's single shared ``set_interval``
(pitfall: one clock interval for the whole app, never one per widget).
"""

from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from textual.widgets import Static

from .models import CITY_TO_ZONE, DEFAULT_CLOCK1, DEFAULT_CLOCK2
from .views import HEX


def _c(text: str, key: str, bold: bool = False) -> str:
    b = "b " if bold else ""
    return f"[{b}{HEX[key]}]{text}[/]"


def clock_hhmm(iana: str, utc_now: datetime) -> str:
    """A city's HH:MM for a given aware-UTC instant (DST-aware, pure/testable)."""
    try:
        return utc_now.astimezone(ZoneInfo(iana)).strftime("%H:%M")
    except (ZoneInfoNotFoundError, ValueError):
        return "--:--"


class Ribbon(Static):
    """A one-line docked status bar. The app sets the two clock cities on mount."""

    clock1_key: str = DEFAULT_CLOCK1   # a city display name
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
        for city in (self.clock1_key, self.clock2_key):
            iana = CITY_TO_ZONE.get(city, "UTC")
            parts.append(_c(city, "mut") + " " + _c(clock_hhmm(iana, utc_now), "accent"))
        sep = _c(" · ", "frame")
        markup = " " + sep.join(parts) + " "
        self.update(markup)
        return markup
