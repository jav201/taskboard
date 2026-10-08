"""Render the amended C-2b oracle frames (LED-2026-10-07-batch-06.1).

The TC-801 fixture: `kg_board.shifted` + Data Warehouse `together`, frozen
calendar — exactly as tests/test_chainmap.py renders. Writes the rows with CRLF
line endings to the batch's evidence home.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tests"))

import kg_board
from taskboard import views
from taskboard import models

ROOT = Path(__file__).resolve().parents[3]
TODAY = kg_board.TODAY
OUT = ROOT / ".dev-flow" / "2026-10-07-batch-06" / "evidence" / "frames"


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


def base(tmp_path, *, together: bool = False):
    b = kg_board.shifted(tmp_path / "board.json")
    if together:
        b.project_by_id("pdwh").extra["date_links"] = "together"
    b.save()
    return b


def render(b, sel, w, h):
    text = views.render_chainmap(b, False, sel, TODAY, width=w, height=h)
    return text.plain.split("\n")


def main():
    # freeze the calendar like the test's `frozen` fixture
    views.date = _Today
    models.date = _Today
    kg_board.date = _Today

    tmp = ROOT / ".dev-flow" / "2026-10-07-batch-06" / "evidence"
    b = base(tmp / "c2b.json", together=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for w, h in ((118, 30), (80, 24)):
        rows = render(b, "tm3", w, h)
        out = OUT / f"C-2b-{w}x{h}.txt"
        out.write_bytes(("\r\n".join(rows) + "\r\n").encode("utf-8"))
        print(f"wrote {out}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
