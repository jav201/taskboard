"""inc15: the six `field_row` seats, inserted beside each language's tile_row."""
import pathlib

p = pathlib.Path("taskboard/language.py")
s = p.read_text(encoding="utf-8")

BASE_OLD = '''    def tile_row(self, val: str, label: str, tone: str, w: int) -> str:
        c = self.c
        room = w - len(val) - 1
        lab = c["dim"] if room < 6 else c["mut"]
        return f"[{tone}]{val}[/] [{lab}]{label[:max(0, room)]}[/]"
'''
BASE_ADD = '''
    # -- THE DEFINITION ROW: a caption and the value it names ---------------
    #
    # THE MOST REUSED SHAPE IN SIX SCREENS AND THE ONE WITH NO SEAT. The
    # PROTOTYPE round of 2026-09-04 rendered a detail pane, a KPI summary and
    # a settings readout in five languages, and every one of those rows was
    # drawn BY HAND -- with LEDGER'S mechanism, dot leaders, in four languages
    # that never chose it. One language's signature generalised into four is
    # the palette-swap failure with a leader instead of a hue, which is why
    # this is a SEAT and not a helper each caller writes once.
    #
    # WHAT IS THE CONTRACT'S AND WHAT IS THE LANGUAGE'S:
    #   * the VALUE is CONTENT -- byte for byte, never recased, never cut. It
    #     is the figure the row exists to report.
    #   * the CAPTION is a LABEL, and a label is NOTATION: a language that
    #     letters its legends in capitals letters this one too, exactly as
    #     `tile_row` already does. That asymmetry is the whole ruling, stated
    #     once here so that no language decides it twice.
    #   * the GAP is the MECHANISM, and it is nobody's default: air, leaders,
    #     a dimension, an ember frontier, an unlit lattice.
    #
    # `w` IS A MINIMUM FOR THE FIGURE -- the stepper's rule, for the stepper's
    # reason: a row that truncated its value to fit would be lying about the
    # number, and a caller who wants a narrower row can pass a shorter word.
    #
    # BASE (nord) IS THE TERMINAL'S OWN TWO-COLUMN LIST: the name at the left
    # margin, the figure flushed RIGHT, and AIR between them. No leader --
    # the terminal's convention is a COLUMN, and a column is found by
    # ALIGNMENT rather than followed by a line.
    def field_row(self, caption: str, value: str, w: int) -> str:
        c = self.c
        cap, val = str(caption), str(value)
        gap = max(1, w - len(cap) - len(val))
        return (f"[{c['mut']}]{mark(cap)}[/]" + " " * gap
                + f"[{c['ink']}]{mark(val)}[/]")
'''

NAUGHT_OLD = '''    def tile_row(self, val, label, tone, w):
        c = self.c
        return (f"[{tone}]{NA.ON}[/] [{tone}]{val}[/] "
                f"[{c['mut']}]{label[: max(0, w - len(val) - 4)]}[/]")
'''
NAUGHT_ADD = '''
    def field_row(self, caption, value, w):
        """THE LATTICE IS THE GROUND, so the row's remainder is DRAWN.

        This language has one structure device and it is the grid: "the unlit
        grid is visible -- dark dots render in the dim tier rather than as
        spaces.  That faint lattice IS the signature."  So a definition row
        neither RULES a leader between two marks nor flushes a column: it is
        DENSE (the figure sits beside the name, which is what "dense" means
        when it is a commitment and not an adjective) and what follows is
        lattice, unlit.

        THE FILL IS AFTER THE VALUE AND NEVER BETWEEN, and that is the exact
        structural difference from ledger's leaders: a leader CONNECTS two
        marks, a lattice is a GROUND that was already there.  The charge says
        the rest -- the name unlit, the figure lit."""
        c = self.c
        cap, val = str(caption), str(value)
        room = max(0, w - len(cap) - len(val) - 2)
        return (f"[{c['dim']}]{mark(cap)}[/] [{c['ink']}]{mark(val)}[/] "
                f"[{c['dim']}]{NA.OFF * room}[/]")
'''

CORGI_OLD = '''    def tile_row(self, val, label, tone, w):
        c = self.c
        room = max(0, w - len(val) - 3)
        return (f"[{self.screen}]{val}[/] [{self.alu}]│[/]"
                f"[{c['mut']}]{label.upper()[:room]}[/]")
'''
CORGI_ADD = '''
    def field_row(self, caption, value, w):
        """THE SILKSCREEN BESIDE THE READOUT -- no leader, no right column.

        A panel does not rule a line from a legend to its display; it PRINTS
        the legend where the display is.  So the label is engraved in the
        aluminium register and the figure stands in the glass immediately
        after it, left-packed, and the rest of the row is bare panel.

        THE LABEL IS LETTERED IN CAPITALS AND THE FIGURE IS NOT TOUCHED --
        this language's legends are engraved and its readouts are driven, and
        those are two registers on one object.  `tile_row` already draws that
        asymmetry; this row inherits it rather than inventing a second rule.

        AND IT IS NOT NUMBERED (L-33, operator ruling 3): the numbers are the
        parameter keymap, and a caption is a name, not a key."""
        cap, val = str(caption).upper(), str(value)
        room = max(0, w - len(cap) - len(val) - 1)
        return (f"[{self.alu}]{mark(cap)}[/] [{self.screen}]{mark(val)}[/]"
                + " " * room)
'''

PRISM_OLD = '''    def tile_row(self, val, label, tone, w):
        c = self.c
        return (f"[{tone}]{val}[/] [{c['mut']}]"
                f"{label.lower()[: max(0, w - len(val) - 2)]}[/]")
'''
PRISM_ADD = '''
    def field_row(self, caption, value, w):
        """THE EMBER FRONTIER -- this language's second commitment applied to
        a row instead of to a quantity.

        "Quantity is a solid field being CONSUMED, not a track being filled."
        So the space between a name and its figure is neither ruled nor
        dotted: it is a field burning down toward the figure, drawn with the
        same ramp the controls spend.  The frontier ARRIVES at the value --
        the value is where the field ran out.

        NO LEADER AND NO STROKE, and the second half is doctrine: "depth by
        one grey step, never borders."  A leader is not a border, but it is a
        LINE, and this language separates by tone and by consumption."""
        c = self.c
        cap, val = str(caption).lower(), str(value)
        ramp = "⡀⡤⣶"
        room = w - len(cap) - len(val) - len(ramp) - 1
        if room < 1:                       # too tight for a frontier: air
            room = max(1, w - len(cap) - len(val))
            return (f"[{c['mut']}]{mark(cap)}[/]" + " " * room
                    + f"[{c['ink']}]{mark(val)}[/]")
        return (f"[{c['mut']}]{mark(cap)}[/]" + " " * room
                + f"[{c['dim']}]{ramp}[/] [{c['ink']}]{mark(val)}[/]")
'''

LEDGER_OLD = '''        c = self.c
        room = max(1, w - len(val) - self.ICON_W - 2)
        return (f"[{tone}]{val}[/] "
                f"[{c['mut']}]{self._leadered(label.upper(), room)}[/]")
'''
LEDGER_ADD = '''
    def field_row(self, caption, value, w):
        """DOT LEADERS -- and here they are the language's OWN, not a shape
        four other languages borrowed.

        "Every gap between a name and its figure closes with DOT LEADERS."
        `_leadered` is the one function that argument lives in, and this is
        the plainest thing it has ever been asked for: the account name, the
        leader that closes its column, and the figure at the measure's right
        edge where a figure is posted."""
        c = self.c
        cap, val = str(caption).upper(), str(value)
        return (f"[{c['ink']}]{self._leadered(cap, max(1, w - len(val) - 1))}"
                f"[/] [{c['ink']}]{mark(val)}[/]")
'''

BLUE_OLD = '''    def tile_row(self, val, label, tone, w):
        """The reading first, on a leader running to its name."""
'''
BLUE_ADD = '''    def field_row(self, caption, value, w):
        """A DIMENSION: the name stands at its datum, the extension line runs
        out of it, and the figure terminates the run.

        This is what a drawing office does with a caption and a value, and it
        is the one mechanism here that is a MEASUREMENT rather than a fill:
        the line does not close a gap, it STATES the distance between the
        thing named and the figure that answers for it.  Both marks it spends
        are already in the ten (`LEAD`, `EXT`) -- no vertical stroke, nothing
        boxed, at any width."""
        c = self.c
        cap, val = str(caption).upper(), str(value)
        room = max(1, w - len(cap) - len(val) - 3)
        return (f"[{c['ink']}]{mark(cap)}[/] "
                f"[{c['dim']}]{self.LEAD + self.EXT * room}[/] "
                f"[{c['ink']}]{mark(val)}[/]")

'''

assert s.count(BASE_OLD) == 1, "base"
s = s.replace(BASE_OLD, BASE_OLD + BASE_ADD)
for tag, old, add in (("naught", NAUGHT_OLD, NAUGHT_ADD),
                      ("corgi", CORGI_OLD, CORGI_ADD),
                      ("prism", PRISM_OLD, PRISM_ADD),
                      ("ledger", LEDGER_OLD, LEDGER_ADD)):
    assert s.count(old) == 1, ("MISS", tag)
    s = s.replace(old, old + add)
assert s.count(BLUE_OLD) == 1, "blueprint"
s = s.replace(BLUE_OLD, BLUE_ADD + BLUE_OLD)

p.write_text(s, encoding="utf-8")
print("six field_row seats written")
