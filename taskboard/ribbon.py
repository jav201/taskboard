"""Bottom status ribbon: local time, date, ISO week, and two custom clocks.

Updated once per second by the app's single shared ``set_interval`` (pitfall:
one clock interval for the whole app, never one per widget).
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from textual.widgets import Static

from .views import HEX

# --------------------------------------------------------------------------- #
#  EDIT ME: the two custom clocks shown on the right of the ribbon.            #
#  Each entry is (short label, IANA timezone name). Examples:                  #
#    ("NYC", "America/New_York"), ("Tokyo", "Asia/Tokyo"), ("UTC", "UTC")      #
# --------------------------------------------------------------------------- #
CLOCKS: list[tuple[str, str]] = [
    ("LA", "America/Los_Angeles"),
    ("Madrid", "Europe/Madrid"),
]


def _c(text: str, key: str, bold: bool = False) -> str:
    b = "b " if bold else ""
    return f"[{b}{HEX[key]}]{text}[/]"


class Ribbon(Static):
    """A one-line docked status bar."""

    def on_mount(self) -> None:
        self.update_clock()

    def update_clock(self, now: datetime | None = None) -> str:
        now = now or datetime.now()
        week = f"W{now.isocalendar().week:02d}"
        parts = [
            _c(now.strftime("%H:%M:%S"), "accent", bold=True),
            _c(now.strftime("%a %d %b %Y"), "ink"),
            _c(week, "amber"),
        ]
        for label, tzname in CLOCKS:
            try:
                tz_now = datetime.now(ZoneInfo(tzname))
                val = tz_now.strftime("%H:%M")
            except (ZoneInfoNotFoundError, ValueError):
                val = "--:--"
            parts.append(_c(label, "mut") + " " + _c(val, "accent"))
        sep = _c(" · ", "frame")
        markup = " " + sep.join(parts) + " "
        self.update(markup)
        return markup
