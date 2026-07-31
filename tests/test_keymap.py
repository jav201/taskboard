"""THE KEY BAR IS A CONTRACT.

    EVERY KEY SHOWN WORKS. EVERY KEY THAT WORKS IS SHOWN.
    A capability whose key is not on screen does not exist.

This defect has now appeared twice on unrelated surfaces, which is what makes it
a law rather than a slip. In this app it was total: Textual's `Footer` reported
its bindings ready and mounted ZERO children, so all 24 live keys rendered as a
blank row — every capability live, nothing displayed.

ORACLE DISCIPLINE, learned the expensive way: these laws read the RAW `KEYMAP`
tuple. They must never ask the accessor under test what it thinks the keys are —
the design agent's first version of this oracle called the same function its
mutant patched and scored zero reds. If a test here calls `bar_keys` or
`app_bindings` to decide what SHOULD be there, it has stopped being a test.
"""

import re

from textual.binding import Binding

from taskboard.app import TaskboardApp
from taskboard.keymap import (KEYMAP, VIEWS, app_bindings, bar_keys, fit_bar,
                              key_bar_plain, render_key_bar)

# Read straight off the seat. Not through any function this file is testing.
RAW_ACTIONS = [k.action for k in KEYMAP]
RAW_SHOWN = [k.show for k in KEYMAP]
RAW_UNIVERSAL = [k.show for k in KEYMAP if k.universal]


def action_name(action: str) -> str:
    return action.split("(")[0]


# --------------------------------------------------------------------------- #
# every key that works is shown
# --------------------------------------------------------------------------- #
def test_every_binding_the_app_has_comes_from_the_seat():
    """There is no second list. A binding hand-written on the App class would be
    a capability the bar knows nothing about."""
    src_actions = {b.action for b in TaskboardApp.BINDINGS}
    assert src_actions == set(RAW_ACTIONS)
    assert len(TaskboardApp.BINDINGS) == len(KEYMAP)


def test_every_seat_entry_reaches_the_widest_bar():
    """Given room, the bar shows ALL of them — no key is decoration-only."""
    for view in VIEWS:
        shown = {show for show, _label in fit_bar(400, view)[0]}
        expected = {k.show for k in KEYMAP if k.views is None or view in k.views}
        assert shown == expected, f"{view}: {expected - shown} never displayed"
        assert fit_bar(400, view)[1] == 0


def test_the_lanes_bar_shows_every_universal_and_global_key():
    """Stated concretely for the default view, against the raw table."""
    shown = {show for show, _ in fit_bar(400, "swimlanes")[0]}
    for k in KEYMAP:
        if k.views is None:
            assert k.show in shown, f"{k.show} ({k.label}) is live but not shown"


# --------------------------------------------------------------------------- #
# every key shown works
# --------------------------------------------------------------------------- #
def test_every_shown_key_has_a_real_action_on_the_app():
    """The other direction, and the one that catches a stale bar: the action of
    every entry must actually exist as a method (inherited counts — `quit` is
    Textual's)."""
    for k in KEYMAP:
        assert hasattr(TaskboardApp, "action_" + action_name(k.action)), \
            f"{k.show} ({k.label}) shows a dead action: {k.action}"


def test_a_view_specific_key_is_only_shown_where_it_works():
    """`tab` flips the kanban presentation and is a no-op everywhere else. A key
    advertised in a view where it does nothing is the same lie in reverse."""
    tab = next(k for k in KEYMAP if k.action == "toggle_presentation")
    assert tab.views == ("kanban",)
    assert tab.show in {s for s, _ in fit_bar(400, "kanban")[0]}
    for view in VIEWS:
        if view != "kanban":
            assert tab.show not in {s for s, _ in fit_bar(400, view)[0]}, view


def test_the_seat_has_no_duplicate_keys_or_labels():
    keys = [k.keys for k in KEYMAP]
    assert len(keys) == len(set(keys))
    assert len(RAW_SHOWN) == len(set(RAW_SHOWN))


def test_every_key_alias_is_bound_not_just_the_shown_one():
    """`d,delete` and the vim aliases must all still work even though the bar
    prints one of them."""
    bound = {b.key for b in app_bindings()}
    assert "d,delete" in bound and "down,j" in bound and "right,l" in bound
    assert all(isinstance(b, Binding) for b in app_bindings())


# --------------------------------------------------------------------------- #
# degradation: words go, keys do not
# --------------------------------------------------------------------------- #
def test_the_bar_never_exceeds_its_width():
    for view in VIEWS:
        for width in range(0, 200):
            assert len(key_bar_plain(width, view)) <= width, f"{view} @ {width}"


def test_words_are_dropped_before_any_key_is():
    """The law: a key without its word is still discoverable; a key that is not
    there is not. So while ANY word survives, every key must survive."""
    for view in VIEWS:
        total = len([k for k in KEYMAP if k.views is None or view in k.views])
        for width in range(0, 200):
            entries, dropped = fit_bar(width, view)
            words_left = sum(1 for _s, label in entries if label)
            if words_left:
                assert dropped == 0, (f"{view} @ {width}: dropped {dropped} key(s) "
                                      f"while {words_left} word(s) were still shown")
                assert len(entries) == total


def test_the_universal_keys_are_first_and_last_to_go():
    """`q` sorts first so it can never be the one that falls off."""
    assert RAW_UNIVERSAL, "the seat declares no universal key"
    for view in VIEWS:
        entries, _ = fit_bar(400, view)
        assert [s for s, _ in entries][:len(RAW_UNIVERSAL)] == RAW_UNIVERSAL
        # and at the narrowest width that still shows anything, it is what shows
        for width in range(1, 40):
            entries, _ = fit_bar(width, view)
            if entries:
                assert entries[0][0] in RAW_UNIVERSAL, f"{view} @ {width}"
                break


def test_keys_that_cannot_fit_are_counted_never_swallowed():
    """Below the width where even bare keys fit, the bar says how many are off
    screen rather than quietly showing fewer. (No `?` legend exists yet, so the
    count is the honest minimum.)"""
    text = key_bar_plain(24, "swimlanes")
    entries, dropped = fit_bar(24, "swimlanes")
    assert dropped > 0
    assert re.search(r"\+\d+$", text), text
    assert int(re.search(r"\+(\d+)$", text).group(1)) == dropped
    assert len(entries) + dropped == len(
        [k for k in KEYMAP if k.views is None or "swimlanes" in k.views])


def test_at_a_normal_width_nothing_is_dropped_at_all():
    """The size the app's own wezterm.lua ships, and the one the user sees."""
    for view in VIEWS:
        entries, dropped = fit_bar(96, view)
        assert dropped == 0, f"{view} @ 96 hides {dropped} key(s)"


def test_the_widest_bars_keep_their_words():
    """Given enough room every key keeps its word. The full bar measures 214
    cells with 24 keys aboard, so the law is checked above that — it is a claim
    about the DEGRADATION having an end, not about any particular width."""
    entries, _ = fit_bar(240, "swimlanes")
    assert all(label for _s, label in entries)


# --------------------------------------------------------------------------- #
# what is actually painted
# --------------------------------------------------------------------------- #
def test_the_rendered_markup_carries_every_key_the_fit_chose():
    for view in VIEWS:
        for width in (24, 48, 72, 96, 140):
            entries, _ = fit_bar(width, view)
            markup = render_key_bar(width, view)
            for show, _label in entries:
                assert show in markup, f"{view} @ {width}: {show} missing"


def test_keys_and_words_wear_different_tones_and_neither_judges():
    """The bar names capabilities; it judges nothing, so no severity hue."""
    from taskboard.views import HEX
    markup = render_key_bar(140, "swimlanes")
    assert HEX["accent"] in markup and HEX["mut"] in markup
    assert HEX["over"] not in markup and HEX["soon"] not in markup


async def test_the_app_paints_its_keys_instead_of_a_blank_row(tmp_path):
    """The regression that started this: Textual's Footer rendered an empty row
    while 24 bindings were live. The bar is painted, and it says the real keys."""
    from taskboard.keymap import KeyBar
    app = TaskboardApp(board_path=str(tmp_path / "b.json"))
    async with app.run_test(size=(120, 30)) as pilot:
        await pilot.pause()
        bar = app.query_one("#keybar", KeyBar)
        assert bar.region.height >= 1 and bar.region.width > 0
        strips = app.screen._compositor.render_strips(app.screen.size)
        painted = "".join(s.text for s in strips[bar.region.y:bar.region.y + 1])
        assert painted.strip(), "the key row is blank — the old defect is back"
        for k in KEYMAP:
            if k.views is None:
                assert k.show in painted, f"{k.show} ({k.label}) is not on screen"


async def test_switching_views_restates_the_keys_for_that_view(tmp_path):
    from taskboard.keymap import KeyBar
    app = TaskboardApp(board_path=str(tmp_path / "b.json"))
    async with app.run_test(size=(120, 30)) as pilot:
        await pilot.pause()
        tab = next(k for k in KEYMAP if k.action == "toggle_presentation")
        bar = app.query_one("#keybar", KeyBar)
        await pilot.press("4")                       # kanban
        await pilot.pause()
        assert tab.show in str(bar.render())
        await pilot.press("1")                       # lanes
        await pilot.pause()
        assert tab.show not in str(bar.render())


# --------------------------------------------------------------------------- #
# two defects of the stock Footer, which this bar exists instead of
# --------------------------------------------------------------------------- #
def test_the_bar_is_ours_and_no_stock_footer_is_mounted():
    """Textual's `Footer` is what this replaced: on 8.2.8 it reported its
    bindings ready and mounted ZERO children, painting a blank row while 24
    bindings were live. Reintroducing it would hand the contract back to a
    widget that has already broken it once."""
    import inspect

    from taskboard import app as app_module
    src = inspect.getsource(app_module)
    assert "Footer" not in src, "the stock Footer is back in the app"
    assert "KeyBar" in src
    assert "from textual.widgets import" in src and "Footer" not in src.split(
        "from textual.widgets import")[1].split("\n")[0]


def test_no_two_shown_keys_share_an_action():
    """MEASURED on Textual 8.2.8: `Footer` collapses bindings BY ACTION —
    `action_to_bindings` is keyed on `binding.action` (`_footer.py:252`) — so six
    distinct keys bound to one action print as a single entry. Our own bar
    renders per KEYMAP row and dodges that, but a shared action would still
    corrupt any Footer-derived surface (and any future help screen grouped the
    same way). The constraint is cheap to keep and expensive to rediscover."""
    import collections
    shown = [k for k in KEYMAP]
    by_action = collections.Counter(k.action for k in shown)
    dupes = {a: n for a, n in by_action.items() if n > 1}
    assert not dupes, f"these actions are claimed by more than one shown key: {dupes}"


# --------------------------------------------------------------------------- #
# the README is a surface too, and the same law applies to it
# --------------------------------------------------------------------------- #
def _readme() -> str:
    import pathlib
    return (pathlib.Path(__file__).parent.parent / "README.md").read_text(encoding="utf-8")


def test_every_image_the_readme_shows_exists():
    """A README pointing at a deleted asset is a broken front page; one pointing
    at a STALE asset is worse, because it looks fine and shows an app that no
    longer exists. This catches the first; the second is why the assets are
    regenerated from the real app rather than kept."""
    import pathlib
    import re
    root = pathlib.Path(__file__).parent.parent
    refs = set(re.findall(r'(docs/[\w.-]+\.(?:png|gif|svg))', _readme()))
    assert refs, "the README shows no images at all"
    for ref in refs:
        assert (root / ref).exists(), f"README shows {ref}, which is not in the repo"


def test_the_readme_keybinding_table_matches_the_seat():
    """THE CONTRACT REACHES THE README. Every key the table documents must be a
    real binding, and every key the app binds must be documented — the same law
    the key bar obeys, applied to the page a reader meets first.

    Read off the RAW KEYMAP, never through the accessor (the M12 lesson)."""
    import re
    table = [l for l in _readme().splitlines() if l.startswith("| `")]
    assert table, "no keybinding table found"
    documented = set()
    for line in table:
        cell = line.split("|")[1]
        for key in re.findall(r"`([^`]+)`", cell):
            documented.add(key)

    # the seat's own keys, in the spelling the README uses
    spelled = {"?": "?", "q": "q", "enter": "Enter", "tab": "Tab",
               "d,delete": "d", "down,j": "↓", "up,k": "↑",
               "left,h": "←", "right,l": "→"}
    for k in KEYMAP:
        want = spelled.get(k.keys, k.keys)
        if k.action.startswith("view("):
            want = k.show                      # the views share one table row
        assert want in documented, \
            f"{k.show} ({k.label}) is bound but the README never mentions it"


def test_the_readme_does_not_document_a_view_that_was_retired():
    text = _readme()
    assert "Columns was retired" in text, "the retirement is not explained"
    # ...and it is not still offered as a live view in the table
    assert not re.search(r"^\| `\d` \| \*\*Columns\*\*", text, re.M)
    for view in VIEWS:
        label = {"swimlanes": "Lanes", "agenda": "Agenda",
                 "gantt": "Gantt", "kanban": "Kanban"}[view]
        assert f"**{label}**" in text, f"{label} is a view but the README omits it"
