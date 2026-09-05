"""inc18: Kit.log_row -- a full row contract, with the level in a glyph (ruling 8)."""
import pathlib
import re

p = pathlib.Path("taskboard/language.py")
s = p.read_text(encoding="utf-8")

BASE_ANCHOR = '''    def knockout_cell(self, text: str) -> str:'''
BASE = '''    # THE LOG LEVELS, and they are a GLYPH LADDER rather than three hues.
    #
    # `ICONS` carries six DOMAIN kinds (deadline, overdue, wip, blocked...)
    # and no log level, which is what the PROTOTYPE round found when it drew
    # a monitor screen: five languages marked ERROR with the same `!!` in the
    # same alert hue, because there was nothing per-language to mark it with.
    #
    # ONE WIDTH PER LANGUAGE, so a column of rows aligns; three shapes, so the
    # level survives the colour being taken away (operator ruling 8).
    LEVELS = {"info": "· ", "warn": "! ", "error": "!!"}

    def knockout_cell(self, text: str) -> str:'''
assert s.count(BASE_ANCHOR) == 1
s = s.replace(BASE_ANCHOR, BASE)

ROW_ANCHOR = '''    def recede(self, row: str) -> str:'''
ROW = '''    def log_row(self, level: str, time: str, message: str,
                tail: bool = False) -> str:
        """ONE ROW OF A STREAM: when, how bad, and what happened.

        A FULL ROW CONTRACT rather than an `ICONS` entry (operator ruling 8),
        because the three fields are not independent: the level decides the
        weight the message is set in, the time is the only thing in the row
        that is not the message's, and a level mark drawn beside a row the
        caller composed would be a mark with no column to sit in.

        THE LEVEL READS WITH THE COLOUR REMOVED. That is the ruling, and it
        is why `LEVELS` is a glyph ladder: three shapes of one width, so a
        greyscale eye sorts the rows and a column of them still aligns.

        AND THE HUE LADDER IS NEUTRAL — dim, mut, ink — rather than
        info/warn/alert, which is a decision with a cost and a reason. Two of
        these languages ration their alert hue by commitment (ledger spends it
        on literal debt, blueprint on overdue and nothing else: "a calm sheet
        carries zero alert"), so a log that reached for red on every ERROR
        would break the one mark those languages guard. The severity is
        therefore carried by SHAPE plus NEUTRAL WEIGHT, in all eleven, and a
        caller who owns its own palette can still tone the message it passes.

        TIME AND MESSAGE ARE BOTH CONTENT and come back byte for byte. A log
        that recased its messages would be editing the record.

        `tail` IS THE LIVE EDGE — the row the next line will arrive after —
        and it is drawn with the language's own DISCLOSE mark, which is the
        same declaration the select spends: the mark that says THERE IS MORE.
        A select points at a list, a log points at the line that has not
        arrived yet."""
        c = self.c
        mk = self.LEVELS.get(level, self.LEVELS["info"])
        tone = {"info": c["dim"], "warn": c["mut"]}.get(level, c["ink"])
        body = c["mut"] if level == "info" else c["ink"]
        row = (f"[{c['dim']}]{mark(str(time))}[/] "
               f"[{tone}]{mark(mk)}[/] "
               f"[{body}]{mark(str(message))}[/]")
        if tail:
            row += f" [{c['accent']}]{mark(self.DISCLOSE)}[/]"
        return row

    def recede(self, row: str) -> str:'''
assert s.count(ROW_ANCHOR) == 1
s = s.replace(ROW_ANCHOR, ROW)


def insert_before_part_glyphs(src, cls, text):
    i = src.index(f"class {cls}(Kit):")
    j = src.index("    PART_GLYPHS = {", i)
    assert re.findall(r"^class (\w+)", src[:j], re.M)[-1] == cls, cls
    return src[:j] + text + "\n" + src[j:]


LEVELS = {
    # how many dots are lit -- the only channel this language has
    "Naught": '    LEVELS = {"info": "◦◦", "warn": "∙◦", "error": "∙∙"}\n',
    # the segment bank's height, which is how this hardware says how much
    "Corgi": '    LEVELS = {"info": "▁▁", "warn": "▄▄", "error": "██"}\n',
    # the ember ramp: how much of the cell has caught
    "Prism": '    LEVELS = {"info": "⣀⣀", "warn": "⣤⣤", "error": "⣿⣿"}\n',
    # THE MARGIN DAGGER. An unremarkable posting carries no mark at all; a
    # queried one is daggered and a disputed one double-daggered, which is
    # the notation this genre has used for exceptions since before screens.
    "Ledger": '    LEVELS = {"info": "  ", "warn": "† ", "error": "‡ "}\n',
    # the drawing's own weights: leader, break, heavy
    "Blueprint": '    LEVELS = {"info": "··", "warn": "╌╌", "error": "━━"}\n',
}
for cls, text in LEVELS.items():
    s = insert_before_part_glyphs(s, cls, text)

p.write_text(s, encoding="utf-8")
print("log_row + five level ladders written")
