"""Team sync spine: one file per person, no server, never raises.

The shared directory is just a directory.  A git checkout, a mounted drive and a
SharePoint-synced folder are the same shape: files appear, disappear and lag.
This module reads/writes ``team.json`` and ``board.<user>.json`` files there,
tolerates every absence and corruption, and merges teammates' tasks as
read-only foreign work.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .models import Board, Project, Task

TEAM_FILENAME = "team.json"
USER_FILE_PREFIX = "board."


def _utc_now_iso() -> str:
    """ISO timestamp with seconds, always UTC, no microseconds."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _read_json(path: Path) -> dict | None:
    """Never-raises JSON read.  Missing, unreadable or non-dict → None."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _write_json(path: Path, data: dict) -> bool:
    """Never-raises JSON write.  Returns whether the bytes landed."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except OSError:
        return False
    return True


@dataclass
class TeamState:
    """Everything the app knows about the shared team directory.

    The object is stateful on purpose: ``pull()`` updates ``config`` and
    ``others`` so the UI can ask for foreign tasks and sync ages without
    touching the filesystem again.
    """

    shared_dir: Path
    user_id: str | None = None
    config: dict = field(default_factory=dict)
    config_version: int = 0
    others: dict[str, dict] = field(default_factory=dict)
    last_push_at: str | None = None

    @classmethod
    def from_settings(cls, shared_dir: str | Path | None,
                      user_id: str | None = None) -> "TeamState | None":
        """Factory from app settings.  ``None`` shared dir means team mode OFF."""
        if not shared_dir:
            return None
        return cls(Path(shared_dir), user_id=user_id)

    # ------------------------------------------------------------------ config
    def load_config(self) -> bool:
        """Read ``team.json`` and adopt it when its version is newer.

        The read never raises; a missing or malformed file simply leaves the
        current config in place.  A config must carry non-empty ``phases`` and
        ``roster`` to be considered valid.
        """
        data = _read_json(self.shared_dir / TEAM_FILENAME)
        if data is None:
            return False
        version = data.get("version")
        if not isinstance(version, int):
            return False
        if version <= self.config_version and self.config:
            return True
        phases = data.get("phases")
        roster = data.get("roster")
        projects = data.get("projects")
        if (not isinstance(phases, list) or not phases
                or not isinstance(roster, list) or not roster
                or not isinstance(projects, list)):
            return False
        self.config = data
        self.config_version = version
        return True

    def team_project_ids(self) -> set[str]:
        """Ids of projects declared as shared in the authoritative config."""
        projects = self.config.get("projects")
        if not isinstance(projects, list):
            return set()
        return {
            p["id"] for p in projects
            if isinstance(p, dict) and isinstance(p.get("id"), str)
        }

    def roster(self) -> list[dict]:
        """Validated roster entries: each has a string ``id``."""
        roster = self.config.get("roster", [])
        return [r for r in roster if isinstance(r, dict) and isinstance(r.get("id"), str)]

    def member_names(self) -> dict[str, str]:
        return {r["id"]: r.get("name", r["id"]) for r in self.roster()}

    def member_hues(self) -> dict[str, str]:
        return {r["id"]: r.get("hue", "mut") for r in self.roster()}

    # ------------------------------------------------------------------ writes
    def push(self, board: Board) -> bool:
        """Write ``board.<user_id>.json`` with only this user's team tasks.

        Personal tasks (those whose project is NOT in ``team.json``) are
        filtered out before the file is written.  The law is enforced here and
        verified in tests.
        """
        if not self.user_id:
            return False
        project_ids = self.team_project_ids()
        tasks = []
        for t in board.tasks:
            if t.project_id not in project_ids:
                continue
            record = board._to_dict(t)
            record["owner"] = self.user_id
            tasks.append(record)
        data = {
            "user": self.user_id,
            "pushed_at": _utc_now_iso(),
            "tasks": tasks,
        }
        path = self.shared_dir / f"{USER_FILE_PREFIX}{self.user_id}.json"
        if _write_json(path, data):
            self.last_push_at = data["pushed_at"]
            return True
        return False

    # ------------------------------------------------------------------- reads
    def pull(self) -> bool:
        """Read teammates' files and refresh ``others``.

        Malformed files and files whose ``tasks`` key is not a list are skipped
        silently.  ``team.json`` is also reloaded so version bumps are picked
        up without a separate call.
        """
        self.load_config()
        others: dict[str, dict] = {}
        try:
            entries = list(self.shared_dir.iterdir())
        except OSError:
            return False
        for entry in entries:
            name = entry.name
            if not (name.startswith(USER_FILE_PREFIX) and name.endswith(".json")):
                continue
            uid = name[len(USER_FILE_PREFIX):-len(".json")]
            if uid == self.user_id or not uid:
                continue
            data = _read_json(entry)
            if not isinstance(data, dict):
                continue
            if not isinstance(data.get("tasks"), list):
                continue
            others[uid] = data
        self.others = others
        return True

    def sync(self, board: Board) -> bool:
        """Push then pull.  Each half is independent; failure is swallowed."""
        pushed = self.push(board)
        pulled = self.pull()
        return pushed and pulled

    # ------------------------------------------------------------------- merge
    def foreign_tasks(self) -> list[tuple[Task, str]]:
        """Foreign tasks as parsed ``Task`` objects paired with owner id.

        A task that fails to parse is skipped; the rest remain available.
        The owner id is also stored in ``task.extra["_owner"]`` for renderers
        that need to colour or label the card.
        """
        out: list[tuple[Task, str]] = []
        for uid, data in self.others.items():
            for tdict in data.get("tasks", []):
                if not isinstance(tdict, dict):
                    continue
                try:
                    task = Task.from_dict(tdict)
                except Exception:
                    continue
                # A task whose title is not a string is not well-formed enough
                # to render; treat it as corrupted foreign data and skip it.
                if not isinstance(task.title, str):
                    continue
                task.extra["_owner"] = uid
                out.append((task, uid))
        return out

    def sync_age(self, uid: str) -> int | None:
        """Minutes since ``uid``'s last push, or None if unknown."""
        data = self.others.get(uid)
        if not isinstance(data, dict):
            return None
        pushed_at = data.get("pushed_at")
        if not isinstance(pushed_at, str):
            return None
        try:
            dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        except ValueError:
            return None
        return int((datetime.now(timezone.utc) - dt).total_seconds() // 60)

    # ---------------------------------------------------------------- alignment
    def apply_config_to_board(self, board: Board) -> None:
        """Make ``board`` inherit authoritative phases and shared projects.

        Called after a newer ``team.json`` is loaded.  Personal projects are
        left untouched.  Phase rename drift is accepted: existing task phase
        strings are NOT rewritten; the board's ``canonical_phase`` will map
        unknown names to the first phase on the next operation that cares.
        """
        if not self.config:
            return
        phases = self.config.get("phases")
        if isinstance(phases, list) and phases and all(isinstance(p, str) and p for p in phases):
            board.phases = list(phases)
        team_projects = self.config.get("projects")
        if not isinstance(team_projects, list):
            return
        by_id = {p.id: p for p in board.projects}
        for pd in team_projects:
            if not isinstance(pd, dict):
                continue
            pid = pd.get("id")
            if not isinstance(pid, str):
                continue
            if pid in by_id:
                existing = by_id[pid]
                for key in ("name", "color", "status", "start_date", "due_date"):
                    if key in pd:
                        setattr(existing, key, pd[key])
                if isinstance(pd.get("archived"), bool):
                    existing.archived = pd["archived"]
            else:
                try:
                    board.projects.append(Project.from_dict(pd))
                except Exception:
                    continue


def sync_tone(team_state: TeamState | None, user_id: str,
              default_tolerance_minutes: int = 45) -> str:
    """Staleness tone for ``user_id``: ``"over"`` when the last push is older
    than the tolerance, otherwise ``"mut"``.

    The tolerance defaults to 45 minutes and may be overridden by
    ``team.json["sync_tolerance_minutes"]``.
    """
    if team_state is None:
        return "mut"
    tolerance = default_tolerance_minutes
    cfg_tolerance = team_state.config.get("sync_tolerance_minutes")
    if isinstance(cfg_tolerance, int) and cfg_tolerance > 0:
        tolerance = cfg_tolerance
    age = team_state.sync_age(user_id)
    if age is None:
        return "mut"
    return "over" if age > tolerance else "mut"
