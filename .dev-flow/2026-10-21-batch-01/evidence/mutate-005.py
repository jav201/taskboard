"""Mutation battery of increment 005 (search by person), batch 2026-10-21-batch-01, from the
project root:  python .dev-flow/2026-10-21-batch-01/evidence/mutate-005.py"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from mutlib import run  # noqa: E402

T = "tests/test_people_search.py::"
L = "tests/test_modal_keys.py::"
V, MO, A = "taskboard/views.py", "taskboard/modals.py", "taskboard/app.py"
run([
    ("M1 the person rule falls through to the text rules", V,
     '    if q.startswith("@"):\n        return "person" if q[1:] in mention_ids(task.notes) else None\n', "",
     T + "test_TC_2505_a_person_query_matches_exactly_their_mentions"),
    ("M2 a partial handle matches (substring, not exact)", V,
     '        return "person" if q[1:] in mention_ids(task.notes) else None',
     '        return "person" if q[1:] in (task.notes or "") else None',
     T + "test_TC_2505_a_person_query_matches_exactly_their_mentions"),
    ("M3 the bar never names the person", V,
     '    person = (people or {}).get(query[1:].lower()) if query.startswith("@") else None',
     "    person = None",
     T + "test_TC_2505_the_bar_names_the_person_and_their_role"),
    ("M4 the kanban's bar given no people", V,
     "            return _apply_search_overlay(text, query, hits, total, w, board.people)\n"
     "        return render_kanban(",
     "            return _apply_search_overlay(text, query, hits, total, w)\n"
     "        return render_kanban(",
     T + "test_AT_2505_at_lists_names_only_and_enter_filters_to_their_tasks[size0]"),
    ("M5 the gantt's bar given no people (qa QA-4)", V,
     "            return _apply_search_overlay(text, query, hits, total, w, board.people)\n"
     "        return render_gantt(",
     "            return _apply_search_overlay(text, query, hits, total, w)\n"
     "        return render_gantt(",
     T + "test_AT_2505_the_gantt_filters_by_person_too"),
    ("M6 the list capped at 8 (qa QA-1)", MO,
     "                                   MODAL_KEYS_W - 2, 6)",
     "                                   MODAL_KEYS_W - 2, 8)",
     T + "test_AT_2505_at_alone_lists_everyone_and_arrows_choose"),
    ("M7 `+ add` offered in the filter", MO,
     '            self._opts = [v for kind, v in opts if kind == "p"]',
     '            self._opts = [v for kind, v in opts]',
     T + "test_AT_2505_at_lists_names_only_and_enter_filters_to_their_tasks[size0]"),
    ("M8 enter filters by the typed text, not the person", MO,
     '            self.dismiss("@" + self._opts[self._sel].id)',
     "            super()._save()",
     T + "test_AT_2505_at_lists_names_only_and_enter_filters_to_their_tasks[size0]"),
    ("M9 alt+p opens nothing", MO,
     "            self._open_person(handle)", "            pass",
     T + "test_AT_2505_alt_p_opens_their_page"),
    ("M11 the law reads only a modal's own source again", "tests/test_modal_keys.py",
     '        has_buttons = any("Button(" in inspect.getsource(k) for k in _own(cls))',
     '        has_buttons = "Button(" in inspect.getsource(cls)',
     L + "test_TC_2407_every_modal_is_in_the_inventory"),
    ("M12 SearchPrompt without alt+s (the law)", MO,
     "class SearchPrompt(TextPrompt):", "class SearchPrompt(ButtonKeysMixin, ModalScreen[str | None]):",
     L + "test_TC_2407_every_button_has_its_key[SearchPrompt]"),
    ("M13 `/` reopened on a person lists no one (code review CR-1)", MO,
     "            rows, opts = pick_rows(self._people, held.name if held else q, self._sel,",
     "            rows, opts = pick_rows(self._people, q, self._sel,",
     T + "test_AT_2505_at_lists_names_only_and_enter_filters_to_their_tasks[size0]"),
    ("M14 the bar's lookup case-sensitive (code review CR-3)", V,
     "    person = (people or {}).get(query[1:].lower()) if query.startswith(\"@\") else None",
     "    person = (people or {}).get(query[1:]) if query.startswith(\"@\") else None",
     T + "test_TC_2505_the_bar_names_the_person_and_their_role"),
])
