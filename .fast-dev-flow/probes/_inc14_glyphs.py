"""inc14: insert the INVALID entry into the eleven PART_GLYPHS tables.

One insertion per (class, part): `INVALID: "g",` immediately before that
entry's DISABLED, so the table's order matches STATES' order.  Every
replacement is asserted to fire exactly once -- a silent miss would leave a
language falling back to DEFAULT, which is the exact failure the property
test is written against, so it is caught here as well as there.

THE MECHANISM, once: DISABLED is a control that cannot be touched; INVALID is
one that HAS been touched and answered back.  Each language's invalid form is
its own mark REFUSING -- walls that turn back on the value, a segment that
will not resolve, a dimension that does not close, a dagger in the margin --
and never a hue, because two of these languages have already spent their
alert on something that would break if a control borrowed it.
"""
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
text = SRC.read_text(encoding="utf-8")

PARTS = ("knob", "textfield.main", "stepper.step")
G = {
    # nord/base: the terminal's own field is `[ ]`, so its rejection is the
    # brackets TURNED BACK on the value -- `]value[` -- and the knob struck.
    "Kit": ("▚", "] [", "]["),
    # naught: the only channel is charge, so a value that will not settle is
    # a dot that will not settle -- half-lit, which no other state is.
    "Naught": ("◑", "◑·◑", "◑◑"),
    # corgi: an LCD error is a segment driven at both ends and resolving at
    # neither -- the bank lit top and bottom with nothing between.
    "Corgi": ("▀▄", "▄▀·▀▄", "▀▄▄▀"),
    # instrument: the walls swapped, and the middle rank of dots knocked out.
    "Instrument": ("⠶", "⠸⠶⠇", "⢠⡄"),
    # swiss: the rules LEAN -- a typographic mark that is plainly not upright.
    "Swiss": ("╲", "╲ ╱", "›‹"),
    # industrial: a stencilled strike through the plate, walls reversed.
    "Industrial": ("/", "▌/▐", "><"),
    # darkside: the round knob crossed -- the tube that will not light.
    "Darkside": ("Ø", "Ø Ø", "ØØ"),
    # prism: the dense block BROKEN, which is the only way this language can
    # say wrong without reaching for a hue it spends on the figure.
    "Prism": ("⣹", "⣹⠀⣏", "⢀⡀"),
    # ledger: the accountant's exception mark. This language does not erase a
    # queried figure, it DAGGERS it -- the genre's own answer, unchanged.
    "Ledger": ("‡", "‡·‡", "‡‡"),
    # solari: the flap caught on its seam, landed on neither face.
    "Solari": ("═", "═·═", "══"),
    # blueprint: the dimension REVERSED -- terminators facing the wrong way,
    # which is a measure that does not close.
    "Blueprint": ("├", "┤·├", "├┤"),
}

CLASSES = ["Kit", "Naught", "Corgi", "Instrument", "Swiss", "Industrial",
           "Nord", "Darkside", "Prism", "Ledger", "Solari", "Blueprint"]

spans = {}
for name in CLASSES:
    m = re.search(rf"^class {name}\b.*?$", text, re.M)
    assert m, name
    nxt = re.search(r"^class \w+", text[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(text) - m.end())
    spans[name] = (m.start(), end)

edits = []
for cls, glyphs in G.items():
    lo, hi = spans[cls]
    body = text[lo:hi]
    for part, glyph in zip(PARTS, glyphs):
        # A BRACE SCANNER RATHER THAN A REGEX, because industrial declares
        # `{}` as a stepper GLYPH: `[^}]*?` stops inside a string literal and
        # hands back half an entry. Quotes are tracked, braces are counted.
        pat = re.compile(rf'"{re.escape(part)}": \{{')
        hits = list(pat.finditer(body))
        assert len(hits) == 1, (cls, part, len(hits))
        i = hits[0].end() - 1
        depth, j, inq = 0, i, False
        while j < len(body):
            ch = body[j]
            if inq:
                inq = ch != '"'
            elif ch == '"':
                inq = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        entry = body[hits[0].start():j + 1]
        assert "INVALID" not in entry, (cls, part)
        assert glyph not in entry, (cls, part, "glyph already in table")
        brace = entry.index("{")
        estart = lo + hits[0].start()
        line_start = text.rfind("\n", 0, estart) + 1
        indent = (estart - line_start) + brace + 1
        pos = estart + entry.index("DISABLED:")
        edits.append((pos, f'INVALID: "{glyph}",\n' + " " * indent))

for pos, ins in sorted(edits, reverse=True):
    text = text[:pos] + ins + text[pos:]

SRC.write_text(text, encoding="utf-8")
print(f"inserted {len(edits)} INVALID entries into {SRC}")
