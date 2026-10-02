"""Derive the Spanish vocabulary increment 003 removed (C-31: the set comes from the
code, not from a hand list).

    python <this file> BASE_DIR CUR_DIR        (each a copy of the taskboard/ package)

Words (3+ letters) of every non-docstring string literal in the base package's
views.py, team_sync.py and modals.py, minus the words of the current package's
literals, minus words that are also English or too generic to be safe. Prints
the sorted set as a Python literal.
"""
import ast
import re
import sys
from pathlib import Path

FILES = ("views.py", "team_sync.py", "modals.py")
# words of the removed text that are ALSO English (or units/brands) — never flagged
ENGLISH = {"team", "json", "roster", "url", "urls", "doing", "board", "landing", "hero",
           "adr", "sync", "min", "dir", "inspector", "tiles", "stale", "review", "images",
           "master", "detail", "throughput", "heatmap", "lattice", "ground", "layout", "tab",
           "esc", "ctrl", "ana", "mind", "nota", "tarde", "son", "dos", "real", "personal",
           "high", "normal", "grouped", "kanban", "deadline", "countdown", "only", "read",
           "ok", "remote", "via", "pin", "pins", "cut", "over", "phase", "ash", "field",
           "standup", "people", "agenda", "flow", "gantt", "focus", "setup", "lanes", "task",
           "tasks", "data", "check", "checks", "doing", "done", "load", "ready"}


def literals(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docs = {id(n.body[0].value) for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module))
            and n.body and isinstance(n.body[0], ast.Expr)
            and isinstance(n.body[0].value, ast.Constant)}
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs]


def words(dirpath: Path) -> set[str]:
    out = set()
    for f in FILES:
        for lit in literals(dirpath / f):
            out |= {w.lower() for w in re.findall(r"[^\W\d_]{3,}", lit)}
    return out


base, cur = words(Path(sys.argv[1])), words(Path(sys.argv[2]))
removed = sorted(w for w in base - cur if w not in ENGLISH)
print(f"# {len(removed)} words")
print(removed)
