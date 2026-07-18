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
    url: str | None = None
    archived: bool = False
    id: str = field(default_factory=_new_id)

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        return cls(
            id=d.get("id") or _new_id(),
            title=d.get("title", "Untitled"),
            project_id=d.get("project_id"),
            status=d.get("status") if d.get("status") in TASK_STATUSES else "backlog",
            priority=d.get("priority") if d.get("priority") in TASK_PRIORITIES else "normal",
            start_date=d.get("start_date"),
            due_date=d.get("due_date"),
            url=d.get("url"),
            archived=bool(d.get("archived", False)),
        )


class Board:
    """Owns projects + tasks and the JSON file behind them."""

    def __init__(self, projects: list[Project], tasks: list[Task], path: Path):
        self.projects = projects
        self.tasks = tasks
        self.path = path

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
            return cls(projects, tasks, path)
        except (json.JSONDecodeError, OSError, TypeError, AttributeError):
            # Corrupt / unreadable: start empty, leave the file untouched.
            return cls([], [], path)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "projects": [asdict(p) for p in self.projects],
            "tasks": [asdict(t) for t in self.tasks],
        }
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

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
             url="https://textual.textualize.io/"),
        Task("dev-flow doc", textual.id, "backlog", "normal", due_date=iso(2)),
        Task("verify counts", textual.id, "active", "normal"),
        Task("systems 5/5", textual.id, "done", "normal"),
        Task("count-guard", textual.id, "done", "normal"),
        Task("pricing sheet", grndia.id, "backlog", "high", due_date=iso(-2),
             url="https://grndia.com/pricing"),
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
             url="https://example.com/domains"),
        Task("read RAG paper", None, "backlog", "normal"),
    ]
    return projects, tasks
