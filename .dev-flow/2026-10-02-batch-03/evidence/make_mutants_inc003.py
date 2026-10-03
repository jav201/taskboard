"""Writes mutants_inc003.json: one mutation per law increment 003 claims (C-40)."""
import json
from pathlib import Path

T = "tests/test_kanban_readable.py"
V = "taskboard/views.py"


def m(id_, old, new, nodes, why):
    return {"id": id_, "file": V, "old": old, "new": new, "nodes": nodes, "why": why}


CUT = [T + "::test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection",
       T + "::test_AT_307_the_selected_card_is_always_whole_on_screen"]
MUTANTS = [
    m("C1", "    if room is not None and room >= 3 and len(keep) == 1 and len(drawn) > room:",
      "    if False:", CUT, "no cut: the band scrolls (P4 UXV3-1)"),
    m("C2", "        start = min(-(-max(0, at + 2 - rows) // 3) * 3, at)", "        start = 0", CUT,
      "the cut ignores the selection"),
    m("C3", "        start = min(-(-max(0, at + 2 - rows) // 3) * 3, at)",
      "        start = min(max(0, at + 2 - rows), at)",
      [T + "::test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection"],
      "the cut not on a card boundary (a half card on top)"),
    m("C4", '        inside = [x for x in (f"▲ {k} more in {name}" if k else "",',
      '        inside = [x for x in ("",',
      [T + "::test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection"],
      "the cards cut above are not counted"),
    m("C5", "    if keep == list(range(len(bands))) and cut is None:",
      "    if keep == list(range(len(bands))):",
      [T + "::test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection"],
      "a cut with every band kept draws no fold row"),
    m("C6", "    body = _literal(text)\n", "    body = escape(text)\n",
      [T + "::test_TC_302_the_shared_title_seat_prints_a_backslash_before_a_bracket"],
      "the shared title seat back on `escape` (P4 qa G-003a)"),
]

Path(__file__).with_name("mutants_inc003.json").write_text(
    json.dumps(MUTANTS, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(MUTANTS), "mutants")
