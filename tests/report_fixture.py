"""The synthetic board set of the HTML reports (batch 2026-10-29-batch-01).

SYNTHETIC ONLY — no real names, no real paths. Ported from the prototype round's
`prototypes/html_report/fixture.py` and grown with every shape the reports must
survive: hostile text (a `<script>` title, a note and a person name carrying
`</script>` and `&`, an `<img onerror>` project and board name), non-http URLs, a
`$&`/`$'` title, formula-like titles (`=`, `+`, `-`, `@`), a 120-character and a
Unicode title, an Inbox task, a cross-project dependency and a chain of three, an
archived task, an archived project, a project whose tasks are all archived, a
task-less project, two boards each holding a project `Docs` with the SAME id, an
unlisted board (registry id None), undated tasks, `start == due`, a task due today.

Every item a filtered view may hide carries a unique token no UI string holds:
qzP1 project, qzB1 board, qzU1 person, qzM1 class, qzT1 title, qzL1 URL, qzN1 note,
qzK1 inside ids.

In memory only: each board's `path` names a file under `tmp_path` when a test
passes one, and nothing here saves. TODAY is pinned.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from taskboard.marks import Mark
from taskboard.models import Board, Project, Task
from taskboard.people import Person

TODAY = date(2026, 10, 29)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]

HOSTILE_TITLE = "<script>alert(1)</script>"
HOSTILE_NOTE = '</script><b>x</b> & "q" ==hi== @zed.hostile'
HOSTILE_PERSON = "Zed </script><img src=x onerror=window.__x=1> & co"
HOSTILE_NAME = "<img src=x onerror=window.__x=2>"
LONG_TITLE = ("Long title " + "abcdefghij" * 11)[:120]
UNICODE_TITLE = "Año nuevo — ñandú 日本語"
DOLLAR_TITLE = "Price $& terms $' check"

PEOPLE: dict[str, Person] = {
    "ana.ruiz": Person(id="ana.ruiz", name="Ana Ruiz", role="Design lead"),
    "luis.prado": Person(id="luis.prado", name="Luis Prado", role="Developer"),
    "carmen.vega": Person(id="carmen.vega", name="Carmen Vega", role="Community"),
    "zed.hostile": Person(id="zed.hostile", name=HOSTILE_PERSON, role="Tester"),
    "una.qz": Person(id="una.qz", name="Una qzU1", role="Hidden"),
    "nora.idle": Person(id="nora.idle", name="Nora Idle", role="Never mentioned"),
}

MARKS: dict[str, Mark] = {
    "delivery": Mark(id="delivery", name="Delivery", shape="▲", colour="rose"),
    "billing": Mark(id="billing", name="Billing", shape="■", colour="amber"),
    "launch": Mark(id="launch", name="Launch", shape="★", colour="lime"),
    "secret": Mark(id="secret", name="Secret qzM1", shape="◆", colour="cyan"),
    "unused": Mark(id="unused", name="Unused", shape="●", colour="blue"),
}


def _d(off: int | None) -> str | None:
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


def _t(key, pk, title, phase, prio, s, d, age, *, blocked=False, deps=(),
       notes="", milestone=False, mark=None, archived=False, urls=()):
    return Task(id=f"t{key}", title=title, project_id=None if pk is None else f"p{pk}",
                phase=phase, priority=prio, start_date=_d(s), due_date=_d(d),
                phase_changed=None if age is None else _d(-age),
                blocked=blocked, depends_on=[f"t{x}" for x in deps],
                notes=notes, milestone=milestone, mark=mark,
                archived=archived, urls=list(urls))


def personal(path: Path | str = "rf-personal-never-saved.json") -> Board:
    projects = [
        Project(id="pmove", name="Move apartment", color="violet",
                start_date=_d(-30), due_date=_d(12)),
        Project(id="ptax", name="Taxes 2026", color="amber",
                start_date=_d(-10), due_date=_d(40)),
        Project(id="pdocs", name="Docs", color="green"),
    ]
    tasks = [
        _t("mv1", "move", "Book moving company", "Done", "normal", -20, -18, 8,
           notes="==confirmed for the 8th== deposit paid"),
        _t("mv2", "move", "Pack kitchen", "Doing", "high", -4, -1, 4, blocked=True,
           notes="!!still missing boxes!! @luis.prado brings more Thursday"),
        _t("mv3", "move", "Transfer internet contract", "Next", "normal", -1, 2, 2),
        _t("mv4", "move", "Update address everywhere", "Backlog", "low", 3, 9, 11,
           deps=("mv2",)),
        _t("mv5", "move", "Keys handover", "Next", "high", 12, 12, 0,
           milestone=True, mark="delivery"),
        _t("tx1", "tax", "Gather deduction receipts", "Doing", "normal", -3, 5, 6,
           notes="++scanner app works++ @ana.ruiz and @luis.prado checked it"),
        _t("tx2", "tax", "Draft the return", "Backlog", "normal", 6, 25, 2, deps=("tx1",)),
        _t("tx0", "tax", "Old: 2024 filing", "Done", "low", -400, -380, 380, archived=True),
        _t("dc1", "docs", "Docs index", "Next", "normal", -2, 0, 1),
        _t("in1", None, "=1+1 sanity check", "Backlog", "normal", None, None, None),
    ]
    return Board(projects, tasks, Path(path), {}, PHASES)


def client_a(path: Path | str = "rf-client-a-never-saved.json") -> Board:
    projects = [
        Project(id="prel", name="Storefront relaunch", color="sky",
                start_date=_d(-45), due_date=_d(21)),
        Project(id="pdocs", name="Docs", color="lime", due_date=_d(35)),
        Project(id="parch", name="Legacy site", color="orange", archived=True),
        Project(id="pold", name="Old campaign", color="pink", status="completed",
                due_date=_d(-3)),
    ]
    tasks = [
        _t("st1", "rel", "Stakeholder interviews", "Done", "normal", -40, -30, 20),
        _t("st2", "rel", "Product photos", "Doing", "high", -6, 2, 6,
           notes="@ana.ruiz shot the hero set ==approved=="),
        _t("st3", "rel", "Content final", "Review", "high", -9, -1, 9, deps=("st2",),
           notes="!!legal still reviewing the refund paragraph!!"),
        _t("st4", "rel", "Homepage build", "Doing", "high", -12, -3, 12, deps=("st3",),
           urls=["https://staging.example.test/storefront"]),
        _t("st5", "rel", "Launch day", "Backlog", "high", 21, 21, 0,
           milestone=True, mark="launch", deps=("st4",)),
        _t("st6", "rel", "Final invoice", "Backlog", "normal", 30, 30, 0,
           milestone=True, mark="billing"),
        _t("st7", "rel", "Old homepage hero", "Done", "low", -90, -60, 90, archived=True),
        _t("st8", "rel", HOSTILE_TITLE, "Backlog", "normal", 1, 6, 1, notes=HOSTILE_NOTE,
           urls=["javascript:alert(1)", "data:text/html,<b>x</b>", "https://example.test/ok"]),
        _t("st9", "rel", DOLLAR_TITLE, "Next", "normal", 4, 10, 1),
        _t("st10", "rel", "+1 follow-up call", "Next", "normal", 2, 3, 1),
        _t("st11", "rel", "-draft- outline", "Next", "low", 5, 7, 1),
        _t("st12", "rel", "@home prep", "Backlog", "low", None, None, None),
        _t("sp1", "docs", "FAQ rewrite", "Doing", "normal", -5, 4, 5,
           notes="- [x] outline\n@ana.ruiz owns the tone ==keep it friendly=="),
        _t("sp2", "docs", "Tutorial videos", "Backlog", "normal", 8, 18, 3, deps=("sp1",),
           notes="@carmen.vega narrates once the script settles"),
        _t("sp3", "docs", "API reference", "Backlog", "normal", 6, 15, 2, deps=("st4",)),
        _t("la1", "arch", "Legacy redirects", "Done", "low", -200, -190, 190, archived=True),
        _t("oc1", "old", "Campaign wrap-up", "Done", "low", -30, -20, 20, archived=True),
    ]
    return Board(projects, tasks, Path(path), {}, PHASES)


def course(path: Path | str = "rf-course-never-saved.json") -> Board:
    projects = [
        Project(id="pvid", name="Video module 3", color="fuchsia",
                start_date=_d(-7), due_date=_d(14)),
        Project(id="pcom", name="Community forum", color="indigo"),
        Project(id="pempty", name="Someday ideas", color="cyan"),
        Project(id="pxss", name=HOSTILE_NAME, color="blue"),
    ]
    tasks = [
        _t("vd1", "vid", "Script module 3", "Done", "normal", -7, -3, 3,
           notes="++best script so far++ @carmen.vega outlined it"),
        _t("vd2", "vid", "Record lesson 3.1", "Doing", "high", -2, 1, 4,
           notes="!!mic hiss on retakes!! swap the interface cable"),
        _t("vd3", "vid", "Edit module 3", "Next", "normal", 2, 8, 2, deps=("vd2",)),
        _t("vd4", "vid", "Module 3 live", "Backlog", "high", 14, 14, 0,
           milestone=True, mark="delivery", deps=("vd3",)),
        _t("vd5", "vid", LONG_TITLE, "Backlog", "normal", 3, 20, 1),
        _t("vd6", "vid", UNICODE_TITLE, "Next", "normal", 1, 9, 1),
        _t("cm1", "com", "Moderation guidelines", "Backlog", "normal", None, None, 6,
           notes="++great examples++ from @carmen.vega in the pinned thread"),
        _t("cm2", "com", "Welcome thread refresh", "Backlog", "low", 5, 12, 1),
        _t("xs1", "xss", "Plain task", "Backlog", "normal", 8, 11, 1),
    ]
    return Board(projects, tasks, Path(path), {}, PHASES)


def side(path: Path | str = "rf-side-never-saved.json") -> Board:
    projects = [Project(id="pside", name="Hidden qzP1", color="pink")]
    tasks = [
        _t("qzK1", "side", "Secret qzT1", "Next", "normal", 16, 16, 1,
           milestone=True, mark="secret", notes="qzN1 private @una.qz",
           urls=["https://example.test/qzL1"]),
    ]
    return Board(projects, tasks, Path(path), {}, PHASES)


SIDE_BOARD_NAME = "Side qzB1 " + HOSTILE_NAME


def lanes(folder: Path | None = None) -> list[tuple]:
    """`(registry id, name, colour, Board)` as the app collects them: three listed
    boards and one unlisted (`--open`, id None) last."""
    def at(name):
        return name if folder is None else Path(folder) / name
    return [
        ("personal", "Personal", "violet", personal(at("personal.json"))),
        ("client-a", "Client A", "sky", client_a(at("client-a.json"))),
        ("course", "Course", "fuchsia", course(at("course.json"))),
        (None, SIDE_BOARD_NAME, "pink", side(at("side.json"))),
    ]


# ---- literal expectations (Q9, Q16): typed from the data above, never computed ----
BOARD_KEYS = ["personal", "client-a", "course", "#3"]

PROJECT_KEYS = [
    "personal:pmove", "personal:ptax", "personal:pdocs", "personal:inbox",
    "client-a:prel", "client-a:pdocs", "client-a:parch", "client-a:pold",
    "course:pvid", "course:pcom", "course:pempty", "course:pxss",
    "#3:pside",
]

STATUS = {
    "personal:tmv1": "done", "personal:tmv2": "late", "personal:tmv3": "open",
    "personal:tmv4": "open", "personal:tmv5": "open", "personal:ttx1": "open",
    "personal:ttx2": "open", "personal:ttx0": "archived", "personal:tdc1": "open",
    "personal:tin1": "open",
    "client-a:tst1": "done", "client-a:tst2": "open", "client-a:tst3": "late",
    "client-a:tst4": "late", "client-a:tst5": "open", "client-a:tst6": "open",
    "client-a:tst7": "archived", "client-a:tst8": "open", "client-a:tst9": "open",
    "client-a:tst10": "open", "client-a:tst11": "open", "client-a:tst12": "open",
    "client-a:tsp1": "open", "client-a:tsp2": "open", "client-a:tsp3": "open",
    "client-a:tla1": "archived", "client-a:toc1": "archived",
    "course:tvd1": "done", "course:tvd2": "open", "course:tvd3": "open",
    "course:tvd4": "open", "course:tvd5": "open", "course:tvd6": "open",
    "course:tcm1": "open", "course:tcm2": "open", "course:txs1": "open",
    "#3:tqzK1": "open",
}
TASK_KEYS = list(STATUS)
TASK_COUNT = 37

DUE_WORDS = {
    "personal:tmv2": "1d overdue", "client-a:tst4": "3d overdue",
    "personal:tdc1": "due today", "personal:tmv3": "in 2d", "course:tcm1": "no date",
    "personal:tin1": "no date", "course:tvd2": "in 1d",
}

PEOPLE_IDS = ["ana.ruiz", "luis.prado", "carmen.vega", "zed.hostile", "una.qz"]
CLASS_KEYS = ["delivery", "billing", "launch", "secret"]

SCOPE_LINE = "All loaded boards (4): Personal, Client A, Course, " + SIDE_BOARD_NAME

# the default view: every project, status open · late · done
DEFAULT_SHOWN = {k for k, s in STATUS.items() if s != "archived"}
LATE = {"personal:tmv2", "client-a:tst3", "client-a:tst4"}
ANA_OR_LUIS = {"personal:tmv2", "personal:ttx1", "client-a:tst2", "client-a:tsp1"}
LAUNCH_OR_BILLING = {"client-a:tst5", "client-a:tst6"}
TAX_OR_SIDE = {"personal:ttx1", "personal:ttx2", "#3:tqzK1"}
FAQ = {"client-a:tsp1"}
