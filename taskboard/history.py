"""Append-only transition log sidecar for a board.

Every phase movement is written to ``<board_dir>/history.jsonl`` as one JSON
line.  The writer and reader both never raise: a failed append sets
``HISTORY_ERROR`` and returns ``None``; a missing or malformed file reads as an
empty history with a skip count.  This mirrors the desk journal discipline:
silent loss is worse than a visible error, so the board mutation always wins.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

HISTORY_ERROR: str | None = None


def history_path(board_path: str | Path) -> Path:
    """Sidecar path: ``history.jsonl`` beside the board JSON file."""
    return Path(board_path).parent / "history.jsonl"


def append(board_path, record: dict, at: datetime | None = None) -> dict | None:
    """Append one transition record to the board's history file.

    ``record`` is extended with ``at`` (ISO-8601, second precision) when the
    caller does not supply it.  ``Path.parent.mkdir`` is performed here so the
    writer is self-contained.  On any OSError ``HISTORY_ERROR`` is set and
    ``None`` is returned; the caller must NOT let that abort the board mutation.
    """
    global HISTORY_ERROR
    at = at or datetime.now()
    line_record = {**record, "at": at.isoformat(timespec="seconds")}
    path = history_path(board_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line_record, ensure_ascii=False) + "\n")
    except OSError as exc:
        HISTORY_ERROR = f"{type(exc).__name__}: {exc}"
        return None
    HISTORY_ERROR = None
    return line_record


def read(board_path) -> tuple[list[dict], int]:
    """Read every valid transition record and count how many lines were skipped.

    A missing file is an empty history.  A line is skipped when it is blank,
    invalid JSON, or valid JSON with the wrong shape: it must be a dict whose
    ``task`` and ``to`` and ``at`` values are strings and whose ``from`` value
    is either ``None`` or a string.
    """
    path = history_path(board_path)
    if not path.exists():
        return [], 0
    records: list[dict] = []
    skipped = 0
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            text = raw.strip()
            if not text:
                continue
            try:
                obj = json.loads(text)
            except json.JSONDecodeError:
                skipped += 1
                continue
            if not isinstance(obj, dict):
                skipped += 1
                continue
            if not isinstance(obj.get("task"), str):
                skipped += 1
                continue
            from_value = obj.get("from")
            if not (from_value is None or isinstance(from_value, str)):
                skipped += 1
                continue
            if not isinstance(obj.get("to"), str):
                skipped += 1
                continue
            if not isinstance(obj.get("at"), str):
                skipped += 1
                continue
            records.append(obj)
    return records, skipped
