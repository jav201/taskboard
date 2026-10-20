"""The key bar's law applied BY HAND to literal seat strings (no taskboard import):
words drop from the right, one at a time, until the bar fits; keys only drop after
every word is gone. Used for increment 002's law-driven KEYBAR_BASE values and
ux N1 (the words lost per width)."""
from rich.cells import cell_len
GANTT_PRIMARY = [("?", "Map"), (";", "More"), ("q", "Quit"), ("B", "Boards"), ("1", "Lanes"),
                 ("2", "Agenda"), ("3", "Gantt"), ("4", "Kanban"), ("5", "Focus"), ("6", "Chains"),
                 ("7", "Flow"), ("8", "Standup"), ("9", "People"), ("0", "Setup"), ("↵", "Details"),
                 ("a", "Add"), ("e", "Edit"), ("d", "Del"), ("L", "Link"), ("↓", "Down"), ("↑", "Up")]
GANTT_MORE = [("?", "Map"), (";", "More"), ("q", "Quit"), ("B", "Boards"), ("1", "Lanes"),
              ("2", "Agenda"), ("3", "Gantt"), ("4", "Kanban"), ("5", "Focus"), ("6", "Chains"),
              ("7", "Flow"), ("8", "Standup"), ("9", "People"), ("0", "Setup"), ("↵", "Details"),
              ("a", "Add"), ("e", "Edit"), ("d", "Del"), ("L", "Link"), ("x", "Archive"),
              ("X", "Purge done"), ("v", "Archived"), ("u", "Undo"), ("t", "Pin task"),
              ("T", "Pin proj"), ("M", "Milestone"), ("[", "Phase−"), ("]", "Phase+"), ("!", "Prio"),
              ("b", "Blocked"), ("+", "Due+"), ("-", "Due-"), ("m", "Chain"), ("F", "Focus"),
              ("esc", "Focus off"), ("/", "Search"), ("↓", "Down"), ("↑", "Up"), ("←", "Left"),
              ("→", "Right")]

def fit(entries, width):
    e = [list(x) for x in entries]
    def w():
        return cell_len("  ".join(f"{k} {l}".strip() for k, l in e))
    for i in range(len(e) - 1, -1, -1):
        if w() <= width:
            break
        e[i][1] = ""
    dropped = 0
    while e and w() + (len(f" +{dropped}") if dropped else 0) > width:
        e.pop()
        dropped += 1
    body = "  ".join(f"{k} {l}".strip() for k, l in e)
    note = f" +{dropped}" if dropped and cell_len(body) + len(f" +{dropped}") <= width else ""
    return body + note

for name, ent, wid in (("gantt primary 80", GANTT_PRIMARY, 80), ("gantt more 118", GANTT_MORE, 118)):
    print(name, "->", repr(fit(ent, wid)))
for wid in (80, 118, 160):
    full = "  ".join(f"{k} {l}" for k, l in GANTT_PRIMARY)
    without = "  ".join(f"{k} {l}" for k, l in GANTT_PRIMARY if k != "B")
    a, b = fit([x for x in GANTT_PRIMARY if x[0] != "B"], wid), fit(GANTT_PRIMARY, wid)
    lost = [w for w in a.split() if w not in b.split() or a.split().count(w) != b.split().count(w)]
    print(f"gantt primary {wid}: before {a!r}\n                  after  {b!r}")
