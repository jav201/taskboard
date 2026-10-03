"""Writes mutants_inc003_r2.json: increment 003's code-review round-1 folds, each
against the node written to kill it (F1 exact fit, F2 counts, F3 whole cards,
F5 open cards only, F6 the band's end), plus the round-1 battery's C1-C6 sites
re-anchored on the folded code."""
import json
from pathlib import Path

T = "tests/test_kanban_readable.py"
V = "taskboard/views.py"
N = T + "::test_TC_311_the_cut_keeps_every_count_and_whole_cards"
CUT = [T + "::test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection",
       T + "::test_AT_307_the_selected_card_is_always_whole_on_screen"]


def m(id_, old, new, nodes, why):
    return {"id": id_, "file": V, "old": old, "new": new, "nodes": nodes, "why": why}


MUTANTS = [
    m("C1", "            and len(drawn) > room + whole):", "            and False):", CUT + [N],
      "no cut: the band scrolls (P4 UXV3-1)"),
    m("C2", "        start = -(-max(0, at + 2 - rows) // 3) * 3\n", "        start = 0\n", CUT,
      "the cut ignores the selection"),
    m("C3", "        start = -(-max(0, at + 2 - rows) // 3) * 3\n", "        start = max(0, at + 2 - rows)\n",
      [T + "::test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection", N],
      "the cut not on a card boundary"),
    m("C5", "    if keep == list(range(len(bands))) and cut is None:",
      "    if keep == list(range(len(bands))):",
      [T + "::test_TC_311_a_band_taller_than_the_room_is_cut_around_the_selection", N],
      "a cut with every band kept draws no fold row"),
    m("F1", "            and len(drawn) > room + whole):", "            and len(drawn) > room):", [N],
      "a single band that exactly fits is cut (F1)"),
    m("F2a", "    if vis(full) > w and (up or inside) and (inside or down):",
      "    if vis(full) > w and (up or inside) and down:",
      [N], "the counts clipped when nothing folds below (F2a)"),
    m("F2b", "    if inside and vis(\"   \".join(x for x in [up] + inside + [down] if x)) > w:",
      "    if False:", [N], "a long band name pushes the `▼` count off (F2b)"),
    m("F3", "        rows = (room - 1) - room % 3            # 3j + 2: j + 1 whole cards",
      "        rows = room - 1", [N], "a lone first row at the cut's bottom (F3)"),
    m("F10", "    if vis(full) > w and (up or inside) and (inside or down):",
      "    if vis(full) > w and (up or inside):",
      [T + "::test_TC_311_the_board_folds_whole_bands_and_names_them"], "a one-sided `▲` row loses its names (F10)"),
    m("F5", "        cards = {t.id for col in band.cols for t in col}     # open cards, not rail titles",
      "        cards = {t for r in body for t in r[1]}", [N], "rail titles counted as cut cards (F5)"),
]

Path(__file__).with_name("mutants_inc003_r2.json").write_text(
    json.dumps(MUTANTS, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(MUTANTS), "mutants")
