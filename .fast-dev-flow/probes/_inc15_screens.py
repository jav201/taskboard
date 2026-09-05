"""inc15: S1's detail pane draws through Kit.field_row."""
import pathlib

p = pathlib.Path("prototypes/components/screens.py")
s = p.read_text(encoding="utf-8")

OLD_CAND = '''C_FIELDROW = Cand(
    "the detail pane's caption -> value rows",
    "evoked", "Kit.field_row",
    "Kit.field_row(self, caption: str, value: str, w: int, "
    "state: str = DEFAULT) -> str",
    "the definition-list row a detail pane, a KPI tile and a settings "
    "summary all are -- COMPONENTS.md's census lists the stat tile and has "
    "no row for this.  It is the single most reused shape in the six "
    "screens and the ONE the contract has no seat for, so all five "
    "languages are currently drawing LEDGER's mechanism (dot leaders): "
    "ledger's own answer generalised into four languages that never chose "
    "it, which is the palette-swap failure with a leader instead of a hue")

'''
assert s.count(OLD_CAND) == 1
s = s.replace(OLD_CAND, "")

OLD_ROWS = '''    for cap, val in F.DETAIL:
        room = right - len(cap) - len(val) - 2
        lead = k.LEAD if hasattr(k, "LEAD") else " "
        det.append(f"[{c['mut']}]{LG.mark(cap)}[/] "
                   f"[{c['dim']}]{LG.mark(lead * max(1, room))}[/] "
                   f"[{c['ink']}]{LG.mark(val)}[/]")
        det_hand.append(len(det))
'''
NEW_ROWS = '''    # THE DEFINITION ROWS, through the kit (inc15).  This loop used to draw
    # ledger's dot leaders in five languages -- one language's typographic
    # argument generalised into four that never chose it.  Each language now
    # answers for itself: air to a right column, an engraved silkscreen, a
    # dimension, an ember frontier, an unlit lattice, dot leaders.
    for cap, val in F.DETAIL:
        det.append(clip(k.field_row(cap, val, right), right))
'''
assert s.count(OLD_ROWS) == 1
s = s.replace(OLD_ROWS, NEW_ROWS)

OLD_DECL = '''    det: list[str] = []
    det_hand: list[int] = []
'''
assert s.count(OLD_DECL) == 1
s = s.replace(OLD_DECL, "    det: list[str] = []\n")

OLD_CDS = '''        cds = [C_SPLIT] + ([C_FIELDROW] if (i + 1) in det_hand else [])
        sh.row(pad(l, left) + " " + split + " " + r, *cds)
'''
NEW_CDS = '''        sh.row(pad(l, left) + " " + split + " " + r, C_SPLIT)
'''
assert s.count(OLD_CDS) == 1
s = s.replace(OLD_CDS, NEW_CDS)

assert "C_FIELDROW" not in s
p.write_text(s, encoding="utf-8")
print("screens.py: S1 detail rows now go through the kit")
