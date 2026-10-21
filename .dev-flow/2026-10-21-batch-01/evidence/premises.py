"""Premise probes of batch 2026-10-21-batch-01, run on `base_ref` (eac7d42) from the
project root with NO_COLOR unset:  python .dev-flow/2026-10-21-batch-01/evidence/premises.py
Synthetic data only (the round's boards), in a temporary folder that stands in for the home."""
import asyncio
import inspect
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
TMP = Path(tempfile.mkdtemp(prefix="p01-premises-"))
Path.home = classmethod(lambda cls: TMP)          # never the real home

import people_round_fixture as fx  # noqa: E402
from textual.keys import _character_to_key  # noqa: E402
from taskboard import app as app_mod, boards, keymap, models, modals, team_sync, views  # noqa: E402
from taskboard.__main__ import open_app  # noqa: E402

app_mod.milestones_marked = lambda settings: True


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


for _m in (app_mod, models, views, modals):
    _m.date = _Today


def probe(n, text):
    print(f"P-{n} {text}")


def static_probes():
    seat = [k for k in keymap.KEYMAP if "at" in [x.strip() for x in k.keys.split(",")]]
    src = "".join(inspect.getsource(m) for m in (app_mod, modals, views, keymap))
    probe(1, f"Textual names the `@` key {_character_to_key('@')!r} | `at` in KEYMAP: {bool(seat)} "
             f"| a Binding on \"at\" anywhere in app/modals: {'Binding(\"at' in src}")
    pkg = "".join(p.read_text(encoding="utf-8") for p in (ROOT / "taskboard").glob("*.py"))
    probe(2, f"`people.json` named in taskboard/: {'people.json' in pkg} | a module "
             f"taskboard/people.py: {(ROOT / 'taskboard' / 'people.py').exists()}")
    hdr = views.render_people.__doc__.splitlines()[0]
    labels = [k.label for k in keymap.KEYMAP if k.action == "view('people')"]
    probe(5, f"view 9's key label: {labels} | its render: {hdr!r} | its head row writes "
             f"'PEOPLE': {'c(\"PEOPLE\"' in inspect.getsource(views.render_people)}")
    push = inspect.getsource(team_sync.TeamState)
    probe(6, f"team push writes the board's own dict (`_to_dict`): {'_to_dict' in push} | "
             f"names people.json: {'people.json' in push}")
    probe(8, f"boards.file_lock: {callable(getattr(boards, 'file_lock', None))} | "
             f"models.write_atomic: {callable(getattr(models, 'write_atomic', None))}")


async def app_probes():
    home = TMP / ".taskboard"
    fx.build(home, last="client-a")
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")            # the home
        await pilot.pause()
        # P-3: `@` in the editor's notes is plain text
        app.selected_task_id = "tc8"
        app.refresh_view()
        await pilot.press("e")
        await pilot.pause()
        ta = app.screen.query_one("#f-notes")
        ta.focus()
        ta.move_cursor(ta.document.end)
        for k in ["enter", "A", "s", "k", "space", "at", "a", "n"]:
            await pilot.press(k)
        await pilot.pause(0.3)
        before = len(list(app.screen.query("*")))
        probe(3, f"notes end with {ta.text.splitlines()[-1]!r} | screen {type(app.screen).__name__} "
                 f"| a widget whose id names a mention: "
                 f"{any('mention' in (w.id or '') or 'drop' in (w.id or '') for w in app.screen.query('*'))} "
                 f"| widgets {before}")
        await pilot.press("escape")
        await pilot.pause()
        # P-4: `/` "ana" in kanban — the text filter's hits
        await pilot.press("4")
        await pilot.pause()
        hits = [t.title for t in app.board.tasks
                if views.matches(t, app.board, "ana") and not t.archived]
        probe(4, f"/ ana on Client A matches {sorted(hits)} | `@ana.ruiz` filter matches "
                 f"{sorted(t.title for t in app.board.tasks if views.matches(t, app.board, '@ana.ruiz'))}")
        # P-7: the people view's key does nothing today
        depth = len(app.screen_stack)
        await pilot.press("at")
        await pilot.pause()
        probe(7, f"`@` on the main screen changes the screen stack: {len(app.screen_stack) != depth}")


static_probes()
asyncio.run(app_probes())
