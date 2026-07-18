"""Data model + JSON persistence for the taskboard widget.

Two entities (Project, Task) and a Board that owns them and reads/writes a
single JSON file. Tasks may be standalone (project_id is None) -> shown in the
"Inbox" group. A missing file is seeded with demo data; a corrupt file starts
empty (we never overwrite it, so the user can recover it by hand).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path
from uuid import uuid4

# --- enumerations (kept as plain strings; validated leniently at the edges) ---
PROJECT_COLORS = ("violet", "sky", "amber", "rose", "green")
PROJECT_STATUSES = ("on_track", "paused", "cancelled", "completed")
TASK_STATUSES = ("backlog", "active", "blocked", "done")
TASK_PRIORITIES = ("low", "normal", "high")

# --- ribbon clocks: CITY -> IANA timezone (real, DST-aware via zoneinfo) ------
# Curated across the regions the user works in. Display name is the city; the
# value stored in board.json is the city name (unique -> recovers its zone).
CITY_ZONES: tuple[tuple[str, str], ...] = (
    # LATAM
    ("Mexico City", "America/Mexico_City"),
    ("Monterrey", "America/Monterrey"),
    ("Guadalajara", "America/Mexico_City"),
    ("Guatemala City", "America/Guatemala"),
    ("San José", "America/Costa_Rica"),
    ("Panama", "America/Panama"),
    ("Bogotá", "America/Bogota"),
    ("Quito", "America/Guayaquil"),
    ("Lima", "America/Lima"),
    ("Caracas", "America/Caracas"),
    ("Santiago", "America/Santiago"),
    ("Buenos Aires", "America/Argentina/Buenos_Aires"),
    ("Montevideo", "America/Montevideo"),
    ("São Paulo", "America/Sao_Paulo"),
    # US / Canada
    ("New York", "America/New_York"),
    ("Boston", "America/New_York"),
    ("Miami", "America/New_York"),
    ("Atlanta", "America/New_York"),
    ("Toronto", "America/Toronto"),
    ("Chicago", "America/Chicago"),
    ("Denver", "America/Denver"),
    ("Phoenix", "America/Phoenix"),
    ("Los Angeles", "America/Los_Angeles"),
    ("San Francisco", "America/Los_Angeles"),
    ("Seattle", "America/Los_Angeles"),
    ("Vancouver", "America/Vancouver"),
    ("Anchorage", "America/Anchorage"),
    ("Honolulu", "Pacific/Honolulu"),
    # Europe
    ("London", "Europe/London"),
    ("Dublin", "Europe/Dublin"),
    ("Lisbon", "Europe/Lisbon"),
    ("Madrid", "Europe/Madrid"),
    ("Paris", "Europe/Paris"),
    ("Brussels", "Europe/Brussels"),
    ("Amsterdam", "Europe/Amsterdam"),
    ("Berlin", "Europe/Berlin"),
    ("Zurich", "Europe/Zurich"),
    ("Rome", "Europe/Rome"),
    ("Vienna", "Europe/Vienna"),
    ("Prague", "Europe/Prague"),
    ("Warsaw", "Europe/Warsaw"),
    ("Copenhagen", "Europe/Copenhagen"),
    ("Oslo", "Europe/Oslo"),
    ("Stockholm", "Europe/Stockholm"),
    ("Helsinki", "Europe/Helsinki"),
    ("Athens", "Europe/Athens"),
    ("Moscow", "Europe/Moscow"),
    # Middle East / Africa
    ("Istanbul", "Europe/Istanbul"),
    ("Tel Aviv", "Asia/Jerusalem"),
    ("Dubai", "Asia/Dubai"),
    ("Riyadh", "Asia/Riyadh"),
    ("Tehran", "Asia/Tehran"),
    ("Cairo", "Africa/Cairo"),
    ("Casablanca", "Africa/Casablanca"),
    ("Lagos", "Africa/Lagos"),
    ("Accra", "Africa/Accra"),
    ("Nairobi", "Africa/Nairobi"),
    ("Johannesburg", "Africa/Johannesburg"),
    # Asia / Pacific
    ("Karachi", "Asia/Karachi"),
    ("Mumbai", "Asia/Kolkata"),
    ("Delhi", "Asia/Kolkata"),
    ("Bangkok", "Asia/Bangkok"),
    ("Jakarta", "Asia/Jakarta"),
    ("Singapore", "Asia/Singapore"),
    ("Hong Kong", "Asia/Hong_Kong"),
    ("Shanghai", "Asia/Shanghai"),
    ("Taipei", "Asia/Taipei"),
    ("Manila", "Asia/Manila"),
    ("Seoul", "Asia/Seoul"),
    ("Tokyo", "Asia/Tokyo"),
    ("Perth", "Australia/Perth"),
    ("Brisbane", "Australia/Brisbane"),
    ("Sydney", "Australia/Sydney"),
    ("Melbourne", "Australia/Melbourne"),
    ("Auckland", "Pacific/Auckland"),
)
CITY_TO_ZONE: dict[str, str] = dict(CITY_ZONES)
_CITY_LOWER: dict[str, str] = {name.lower(): name for name, _ in CITY_ZONES}

DEFAULT_CLOCK1 = "Mexico City"
DEFAULT_CLOCK2 = "New York"

# migrate old fixed-offset abbreviations (pre-city boards) to a representative city
_LEGACY_ABBREV_TO_CITY = {
    "UTC": "London", "GMT": "London", "HST": "Honolulu", "AKST": "Anchorage",
    "PST": "Los Angeles", "MST": "Denver", "CST": "Mexico City", "EST": "New York",
    "AST": "Santiago", "BRT": "São Paulo", "CET": "Madrid", "EET": "Athens",
    "MSK": "Moscow", "GST": "Dubai", "IST": "Mumbai", "ICT": "Bangkok",
    "HKT": "Hong Kong", "JST": "Tokyo", "AEST": "Sydney", "NZST": "Auckland",
}


def city_names() -> list[str]:
    """All selectable city display names (for the searchable picker)."""
    return [name for name, _ in CITY_ZONES]


def resolve_city(text: str | None) -> str | None:
    """Case-insensitive match of typed text to a canonical city name, else None."""
    if not text:
        return None
    return _CITY_LOWER.get(text.strip().lower())


def default_board_path() -> Path:
    """User-data location for the JSON store.

    The package dir is read-only once pip/pipx-installed, so the board lives
    under the user's home instead: ~/.taskboard/board.json
    """
    return Path.home() / ".taskboard" / "board.json"


def _new_id() -> str:
    return uuid4().hex[:8]


def parse_iso(value: str | None) -> date | None:
    """Lenient ISO date parse. Blank / bad input -> None (never raises)."""
    if not value:
        return None
    try:
        return date.fromisoformat(value.strip())
    except (ValueError, AttributeError):
        return None


@dataclass
class Project:
    name: str
    color: str = "violet"
    status: str = "on_track"
    archived: bool = False
    start_date: str | None = None
    due_date: str | None = None
    id: str = field(default_factory=_new_id)

    @classmethod
    def from_dict(cls, d: dict) -> "Project":
        return cls(
            id=d.get("id") or _new_id(),
            name=d.get("name", "Untitled"),
            color=d.get("color") if d.get("color") in PROJECT_COLORS else "violet",
            status=d.get("status") if d.get("status") in PROJECT_STATUSES else "on_track",
            archived=bool(d.get("archived", False)),
            start_date=d.get("start_date"),
            due_date=d.get("due_date"),
        )


@dataclass
class Task:
    title: str
    project_id: str | None = None
    status: str = "backlog"
    priority: str = "normal"
    start_date: str | None = None
    due_date: str | None = None
    urls: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    archived: bool = False
    id: str = field(default_factory=_new_id)

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        # urls: prefer the modern list; migrate a legacy single "url" string
        # into a one-element list (one-way, DD-2); else empty. Never raises.
        if isinstance(d.get("urls"), list):
            urls = [str(u) for u in d["urls"]]
        elif isinstance(d.get("url"), str) and d.get("url"):
            urls = [d["url"]]
        else:
            urls = []
        images = [str(i) for i in d["images"]] if isinstance(d.get("images"), list) else []
        return cls(
            id=d.get("id") or _new_id(),
            title=d.get("title", "Untitled"),
            project_id=d.get("project_id"),
            status=d.get("status") if d.get("status") in TASK_STATUSES else "backlog",
            priority=d.get("priority") if d.get("priority") in TASK_PRIORITIES else "normal",
            start_date=d.get("start_date"),
            due_date=d.get("due_date"),
            urls=urls,
            images=images,
            archived=bool(d.get("archived", False)),
        )


class Board:
    """Owns projects + tasks and the JSON file behind them."""

    def __init__(self, projects: list[Project], tasks: list[Task], path: Path,
                 settings: dict | None = None):
        self.projects = projects
        self.tasks = tasks
        self.path = path
        self.settings = settings or {}

    # ---- persistence -------------------------------------------------------
    @classmethod
    def load(cls, path: str | Path) -> "Board":
        path = Path(path)
        if not path.exists():
            board = cls(*seed_data(), path=path)
            board.save()
            return board
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            projects = [Project.from_dict(p) for p in raw.get("projects", [])]
            tasks = [Task.from_dict(t) for t in raw.get("tasks", [])]
            # settings is optional -> back-compat with pre-settings board files
            settings = raw.get("settings") if isinstance(raw.get("settings"), dict) else {}
            return cls(projects, tasks, path, settings)
        except (json.JSONDecodeError, OSError, TypeError, AttributeError):
            # Corrupt / unreadable: start empty, leave the file untouched.
            return cls([], [], path)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "projects": [asdict(p) for p in self.projects],
            "tasks": [asdict(t) for t in self.tasks],
            "settings": self.settings,
        }
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # ---- ribbon clock settings --------------------------------------------
    def get_clocks(self) -> tuple[str, str]:
        """The two selected clock CITIES, validated + migrated from old boards."""
        return (self._resolve_clock(self.settings.get("clock1"), DEFAULT_CLOCK1),
                self._resolve_clock(self.settings.get("clock2"), DEFAULT_CLOCK2))

    @staticmethod
    def _resolve_clock(value: str | None, default: str) -> str:
        if value in CITY_TO_ZONE:
            return value
        if value in _LEGACY_ABBREV_TO_CITY:      # pre-city board -> migrate
            return _LEGACY_ABBREV_TO_CITY[value]
        return default

    def set_clocks(self, clock1: str, clock2: str) -> None:
        self.settings["clock1"] = clock1
        self.settings["clock2"] = clock2
        self.save()

    # ---- lookups -----------------------------------------------------------
    def project_by_id(self, pid: str | None) -> Project | None:
        if pid is None:
            return None
        return next((p for p in self.projects if p.id == pid), None)

    def task_by_id(self, tid: str | None) -> Task | None:
        if tid is None:
            return None
        return next((t for t in self.tasks if t.id == tid), None)

    def visible_projects(self, show_archived: bool) -> list[Project]:
        return [p for p in self.projects if show_archived or not p.archived]

    def visible_tasks(self, show_archived: bool) -> list[Task]:
        return [t for t in self.tasks if show_archived or not t.archived]

    def project_progress(self, pid: str, show_archived: bool) -> tuple[int, int]:
        """(#done, #total) for a project's visible tasks."""
        rows = [t for t in self.visible_tasks(show_archived) if t.project_id == pid]
        done = sum(1 for t in rows if t.status == "done")
        return done, len(rows)

    # ---- mutations ---------------------------------------------------------
    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.save()

    def add_project(self, project: Project) -> None:
        self.projects.append(project)
        self.save()

    def delete_task(self, tid: str) -> None:
        self.tasks = [t for t in self.tasks if t.id != tid]
        self.save()

    def delete_project(self, pid: str) -> None:
        """Delete a project; its tasks become standalone (Inbox)."""
        self.projects = [p for p in self.projects if p.id != pid]
        for t in self.tasks:
            if t.project_id == pid:
                t.project_id = None
        self.save()


def seed_data() -> tuple[list[Project], list[Task]]:
    """Demo content anchored to today so every urgency bucket is populated."""
    today = date.today()

    def iso(offset_days: int) -> str:
        return (today + timedelta(days=offset_days)).isoformat()

    textual = Project("Textual", "violet", "on_track", start_date=iso(-20), due_date=iso(10))
    grndia = Project("GRNDIA", "sky", "on_track", start_date=iso(-10), due_date=iso(14))
    jobhunt = Project("Job Hunt", "amber", "paused", start_date=iso(-5), due_date=iso(28))
    launch = Project("Launch", "rose", "on_track", start_date=iso(2), due_date=iso(40))
    ops = Project("Ops", "green", "completed", start_date=iso(-30), due_date=iso(-2))
    projects = [textual, grndia, jobhunt, launch, ops]

    tasks = [
        Task("M22 pitfalls module", textual.id, "active", "high", due_date=iso(0),
             urls=["https://textual.textualize.io/"]),
        Task("dev-flow doc", textual.id, "backlog", "normal", due_date=iso(2)),
        Task("verify counts", textual.id, "active", "normal"),
        Task("systems 5/5", textual.id, "done", "normal"),
        Task("count-guard", textual.id, "done", "normal"),
        Task("pricing sheet", grndia.id, "backlog", "high", due_date=iso(-2),
             urls=["https://grndia.com/pricing"]),
        Task("funnel copy", grndia.id, "active", "normal", due_date=iso(3)),
        Task("proposal v2", grndia.id, "done", "normal"),
        Task("portfolio polish", jobhunt.id, "backlog", "normal", due_date=iso(4)),
        Task("interview prep x2", jobhunt.id, "active", "high", due_date=iso(0)),
        Task("vendor onboarding", jobhunt.id, "blocked", "high", due_date=iso(1)),
        Task("CV refresh", jobhunt.id, "done", "low"),
        Task("landing hero", launch.id, "backlog", "normal", due_date=iso(9)),
        # standalone tasks -> Inbox
        Task("call the accountant", None, "backlog", "normal", due_date=iso(-1)),
        Task("renew domain", None, "backlog", "low", due_date=iso(6),
             urls=["https://example.com/domains"]),
        Task("read RAG paper", None, "backlog", "normal"),
    ]
    return projects, tasks
