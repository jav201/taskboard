"""The synthetic board set for the HTML-report prototype round.

SYNTHETIC ONLY — no real names, no real paths. Three boards ("Personal",
"Client A", "Course"), a people directory (Ana Ruiz, Luis Prado, Carmen
Vega), and a milestone-class directory (Delivery/Billing/Launch). Every shape
the report must carry is represented on purpose: phases, dates, overdue work,
milestones with class marks, @mentions, notes with ==/!!/++ highlights, a
link chain, blocked work, done vs open vs archived.

In memory only: each board's `path` names a scratch file and nothing here
saves. TODAY is pinned so every render of the round reads the same numbers.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from taskboard.marks import Mark
from taskboard.models import Board, Project, Task
from taskboard.people import Person

TODAY = date(2026, 10, 29)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]

PEOPLE: dict[str, Person] = {
    "ana.ruiz": Person(id="ana.ruiz", name="Ana Ruiz", role="Design lead"),
    "luis.prado": Person(id="luis.prado", name="Luis Prado", role="Developer"),
    "carmen.vega": Person(id="carmen.vega", name="Carmen Vega", role="Community"),
}

MARKS: dict[str, Mark] = {
    "delivery": Mark(id="delivery", name="Delivery", shape="▲", colour="rose"),
    "billing": Mark(id="billing", name="Billing", shape="■", colour="amber"),
    "launch": Mark(id="launch", name="Launch", shape="★", colour="lime"),
}


def _d(off: int | None) -> str | None:
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


def _t(key, pk, title, phase, prio, s, d, age, *, blocked=False, deps=(),
       notes="", milestone=False, mark=None, archived=False, urls=()):
    return Task(id=f"t{key}", title=title, project_id=f"p{pk}", phase=phase,
                priority=prio, start_date=_d(s), due_date=_d(d),
                phase_changed=None if age is None else _d(-age),
                blocked=blocked, depends_on=[f"t{x}" for x in deps],
                notes=notes, milestone=milestone, mark=mark,
                archived=archived, urls=list(urls))


def personal(path: Path | str = "hr-personal-never-saved.json") -> Board:
    projects = [
        Project(id="pmove", name="Move apartment", color="violet",
                status="on_track", start_date=_d(-30), due_date=_d(12)),
        Project(id="ptax", name="Taxes 2026", color="amber",
                status="on_track", start_date=_d(-10), due_date=_d(40)),
    ]
    tasks = [
        _t("mv1", "move", "Book moving company", "Done", "normal", -20, -18, 8,
           notes="==confirmed for the 8th== deposit paid"),
        _t("mv2", "move", "Pack kitchen", "Doing", "high", -4, -1, 4,
           blocked=True,
           notes="!!still missing boxes!! @luis.prado brings more Thursday"),
        _t("mv3", "move", "Transfer internet contract", "Next", "normal", -1, 2, 2,
           notes="==price locked until Friday== then it rises"),
        _t("mv4", "move", "Update address everywhere", "Backlog", "low", 3, 9, 11,
           deps=("mv2",)),
        _t("mv5", "move", "Keys handover", "Next", "high", 12, 12, 0,
           milestone=True, mark="delivery",
           notes="one date, its due — the class is ==Delivery ▲=="),
        _t("tx1", "tax", "Gather deduction receipts", "Doing", "normal", -3, 5, 6,
           notes="++scanner app works great++ all PDFs in the folder"),
        _t("tx2", "tax", "Draft the return", "Backlog", "normal", 6, 25, 2,
           deps=("tx1",)),
        _t("tx0", "tax", "Old: 2024 filing", "Done", "low", -400, -380, 380,
           archived=True),
    ]
    return Board(projects, tasks, Path(path), {}, PHASES)


def client_a(path: Path | str = "hr-client-a-never-saved.json") -> Board:
    projects = [
        Project(id="prel", name="Storefront relaunch", color="sky",
                status="at_risk", start_date=_d(-45), due_date=_d(21)),
        Project(id="pdoc", name="Support docs", color="lime",
                status="on_track", start_date=_d(-15), due_date=_d(35)),
    ]
    tasks = [
        _t("st1", "rel", "Stakeholder interviews", "Done", "normal", -40, -30, 20,
           notes="summary in the shared drive"),
        _t("st2", "rel", "Product photos", "Doing", "high", -6, 2, 6,
           notes="@ana.ruiz shot the hero set ==approved by client=="),
        _t("st3", "rel", "Content final", "Review", "high", -9, -1, 9,
           deps=("st2",),
           notes="!!legal still reviewing the refund paragraph!!"),
        _t("st4", "rel", "Homepage build", "Doing", "high", -12, -3, 12,
           deps=("st3",), urls=["https://staging.example.com/storefront"]),
        _t("st5", "rel", "Launch day", "Backlog", "high", 21, 21, 0,
           milestone=True, mark="launch", deps=("st4",),
           notes="the whole chain lands here — class ==Launch ★=="),
        _t("st6", "rel", "Final invoice", "Backlog", "normal", 30, 30, 0,
           milestone=True, mark="billing"),
        _t("st7", "rel", "Old homepage hero", "Done", "low", -90, -60, 90,
           archived=True),
        _t("sp1", "doc", "FAQ rewrite", "Doing", "normal", -5, 4, 5,
           notes="- [ ] draft sections\n- [x] outline\n@ana.ruiz owns the tone ==keep it friendly=="),
        _t("sp2", "doc", "Tutorial videos", "Backlog", "normal", 8, 18, 3,
           deps=("sp1",), notes="@carmen.vega narrates once the script settles"),
    ]
    return Board(projects, tasks, Path(path), {}, PHASES)


def course(path: Path | str = "hr-course-never-saved.json") -> Board:
    projects = [
        Project(id="pvid", name="Video module 3", color="fuchsia",
                status="on_track", start_date=_d(-7), due_date=_d(14)),
        Project(id="pcom", name="Community forum", color="indigo",
                status="on_track"),
    ]
    tasks = [
        _t("vd1", "vid", "Script module 3", "Done", "normal", -7, -3, 3,
           notes="++best script so far++ @carmen.vega's outline helped"),
        _t("vd2", "vid", "Record lesson 3.1", "Doing", "high", -2, 1, 4,
           notes="!!mic hiss on retakes!! swap the interface cable"),
        _t("vd3", "vid", "Edit module 3", "Next", "normal", 2, 8, 2,
           deps=("vd2",)),
        _t("vd4", "vid", "Module 3 live", "Backlog", "high", 14, 14, 0,
           milestone=True, mark="delivery", deps=("vd3",)),
        _t("cm1", "com", "Moderation guidelines", "Backlog", "normal",
           None, None, 6,
           notes="++great examples from @carmen.vega++ in the pinned thread"),
        _t("cm2", "com", "Welcome thread refresh", "Backlog", "low", 5, 12, 1),
    ]
    return Board(projects, tasks, Path(path), {}, PHASES)


BOARDS = {"personal": personal, "client-a": client_a, "course": course}


def all_boards() -> dict[str, Board]:
    """The round's data set, keyed the way the brief names the boards."""
    return {"Personal": personal(), "Client A": client_a(), "Course": course()}
