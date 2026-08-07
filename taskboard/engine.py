"""Signal engine — the deep half of the widget.

The aperture is small; what stands behind it is not. A signal is anything that
can be COMPUTED ON A CADENCE and distilled to one glanceable value. Board-derived
signals ship here; an external provider (a telescope, a weather API, a CI feed)
implements the same protocol and costs the aperture nothing extra.

Design rules applied (tui-design/ARCHITECTURE.md):
  * cadences are SEPARATE worker groups, never one shared interval
  * a slow provider can never cancel a fast one
  * providers are pure compute; they never touch the UI
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Protocol

# --------------------------------------------------------------------------
# severity drives what the aperture shows. one scale, ordered.
# --------------------------------------------------------------------------
CALM, NOTICE, WARN, ALERT = 0, 1, 2, 3
SEVERITY_NAME = {CALM: "calm", NOTICE: "notice", WARN: "warn", ALERT: "alert"}


@dataclass
class Reading:
    """One computed observation, distilled for a small aperture."""
    value: str                 # the hero glyph string — short, drawn large
    caption: str               # what the value means, one line
    detail: str = ""           # a second line, shown when there is room
    severity: int = CALM
    ok: bool = True            # False => the provider failed; render an error state
    at: float = field(default_factory=time.monotonic)


@dataclass
class Signal:
    """A registered, user-configurable source of readings."""
    id: str
    label: str
    help: str
    cadence: float                       # seconds between recomputes
    compute: Callable[["Context"], Reading]
    enabled: bool = True
    threshold: int | None = None         # user-tunable, provider-specific
    group: str = "fast"                  # worker group; slow work MUST NOT be "fast"
    last: Reading | None = None
    last_error: str = ""
    runs: int = 0

    def run(self, ctx: "Context") -> Reading:
        self.runs += 1
        try:
            r = self.compute(ctx)
            self.last, self.last_error = r, ""
        except Exception as exc:                     # a bad provider degrades ITS panel
            self.last_error = f"{type(exc).__name__}: {exc}"
            self.last = Reading("!", self.label, self.last_error, ALERT, ok=False)
        return self.last


@dataclass
class Context:
    """What providers are allowed to see."""
    board: object
    today: date
    now: datetime
    signal: Signal | None = None          # so a provider can read its own threshold


class Provider(Protocol):
    def __call__(self, ctx: Context) -> Reading: ...


# --------------------------------------------------------------------------
# board-derived providers
# --------------------------------------------------------------------------
def _open_tasks(ctx: Context):
    b = ctx.board
    return [t for t in b.visible_tasks(False) if not b.is_done(t)]


def _days_left(task, today):
    from taskboard.models import parse_iso
    d = parse_iso(task.due_date)
    return None if d is None else (d - today).days


def sig_deadline(ctx: Context) -> Reading:
    """The nearest deadline. This is the aperture's default hero."""
    dated = [(d, t) for t in _open_tasks(ctx)
             if (d := _days_left(t, ctx.today)) is not None]
    if not dated:
        return Reading("--", "no deadlines", "nothing is dated", CALM)
    d, t = min(dated, key=lambda p: p[0])
    if d < 0:
        return Reading(str(min(99, -d)), "days overdue", t.title, ALERT)
    if d == 0:
        return Reading("0", "due today", t.title, ALERT)
    if d <= 3:
        return Reading(str(d), "days left", t.title, WARN)
    return Reading(str(min(99, d)), "days left", t.title, NOTICE if d <= 7 else CALM)


def sig_overdue(ctx: Context) -> Reading:
    n = sum(1 for t in _open_tasks(ctx)
            if (d := _days_left(t, ctx.today)) is not None and d < 0)
    sev = ALERT if n else CALM
    return Reading(str(n), "overdue", f"{n} past their due date", sev)


def sig_wip(ctx: Context) -> Reading:
    """WIP against a user-set limit — the threshold is configurable."""
    from taskboard.views import phase_buckets
    limit = (ctx.signal.threshold if ctx.signal and ctx.signal.threshold else 3)
    b = ctx.board
    buckets = phase_buckets(b, b.visible_tasks(False))
    doing = 0
    for name, bucket in zip(b.phases, buckets):
        if name.lower() in ("doing", "in progress", "wip"):
            doing = len([t for t in bucket if not b.is_done(t)])
    over = doing > limit
    return Reading(str(doing), "in flight",
                   f"limit {limit}" + (" — over" if over else ""),
                   WARN if over else CALM)


def sig_blocked(ctx: Context) -> Reading:
    n = sum(1 for t in _open_tasks(ctx) if getattr(t, "blocked", False))
    return Reading(str(n), "blocked", "waiting on something else",
                   WARN if n else CALM)


# --------------------------------------------------------------------------
# providers that look OUTSIDE the board — the point of the architecture.
# these are local-only; a network provider implements the same protocol.
# --------------------------------------------------------------------------
def sig_workday(ctx: Context) -> Reading:
    """Hours left in the workday vs work due today. Time-aware, not board-aware."""
    end_hour = (ctx.signal.threshold if ctx.signal and ctx.signal.threshold else 18)
    now = ctx.now
    left = end_hour - now.hour - now.minute / 60
    due_today = sum(1 for t in _open_tasks(ctx)
                    if _days_left(t, ctx.today) == 0)
    if left <= 0:
        return Reading("0", "workday over", f"{due_today} still due today",
                       ALERT if due_today else CALM)
    sev = ALERT if due_today and left < 2 else (WARN if due_today else CALM)
    return Reading(f"{int(left)}", "hours left",
                   f"{due_today} due today", sev)


def sig_board_file(ctx: Context) -> Reading:
    """Watches the board file itself — catches edits made outside this process.
    A slow-cadence provider: it touches the filesystem, so it lives in the
    'slow' worker group and can never stall the fast hero."""
    from taskboard.models import default_board_path
    p = Path(default_board_path())
    if not p.exists():
        return Reading("?", "no board file", str(p), WARN)
    age_min = (time.time() - p.stat().st_mtime) / 60
    kb = p.stat().st_size / 1024
    if age_min < 60:
        return Reading(f"{int(age_min)}", "min since save", f"{kb:.0f} KB on disk", CALM)
    return Reading(f"{int(age_min/60)}", "hours since save",
                   f"{kb:.0f} KB on disk", NOTICE if age_min > 1440 else CALM)


# --------------------------------------------------------------------------
# the registry — what the config screen edits
# --------------------------------------------------------------------------
def default_signals() -> list[Signal]:
    return [
        Signal("deadline", "Nearest deadline",
               "Days until the soonest open task is due. The default hero.",
               cadence=1.0, compute=sig_deadline, group="fast"),
        Signal("overdue", "Overdue count",
               "How many open tasks are past their due date.",
               cadence=2.0, compute=sig_overdue, group="fast"),
        Signal("wip", "Work in flight",
               "Tasks in the DOING phase, against the configured limit.",
               cadence=2.0, compute=sig_wip, threshold=3, group="fast"),
        Signal("blocked", "Blocked",
               "Open tasks flagged as blocked.",
               cadence=3.0, compute=sig_blocked, group="fast"),
        Signal("workday", "Workday budget",
               "Hours left in the working day, against work due today.",
               cadence=30.0, compute=sig_workday, threshold=18, group="slow"),
        Signal("boardfile", "Board file",
               "Watches board.json for edits made outside this app.",
               cadence=20.0, compute=sig_board_file, group="slow"),
    ]


class Engine:
    """Owns the signals and decides which one the aperture shows."""

    def __init__(self, board, signals: list[Signal] | None = None):
        self.board = board
        self.signals = signals or default_signals()
        self._due: dict[str, float] = {s.id: 0.0 for s in self.signals}

    def by_id(self, sid: str) -> Signal | None:
        return next((s for s in self.signals if s.id == sid), None)

    def due_now(self, group: str, now: float | None = None) -> list[Signal]:
        now = time.monotonic() if now is None else now
        out = []
        for s in self.signals:
            if not s.enabled or s.group != group:
                continue
            if now >= self._due.get(s.id, 0.0):
                self._due[s.id] = now + s.cadence
                out.append(s)
        return out

    def run_group(self, group: str) -> int:
        ctx_now = datetime.now()
        n = 0
        for s in self.due_now(group):
            ctx = Context(self.board, ctx_now.date(), ctx_now, signal=s)
            s.run(ctx)
            n += 1
        return n

    def run_all(self) -> None:
        for g in ("fast", "slow"):
            for s in self.signals:
                if s.enabled and s.group == g:
                    now = datetime.now()
                    s.run(Context(self.board, now.date(), now, signal=s))

    @property
    def hero(self) -> tuple[Signal, Reading] | None:
        """The loudest enabled signal wins the aperture. Ties break by order."""
        best = None
        for s in self.signals:
            if not s.enabled or s.last is None:
                continue
            if best is None or s.last.severity > best[1].severity:
                best = (s, s.last)
        return best

    @property
    def worst_severity(self) -> int:
        h = self.hero
        return h[1].severity if h else CALM
