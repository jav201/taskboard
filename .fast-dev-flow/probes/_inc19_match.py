"""inc19: Kit.match (ruling 9) and Kit.keyhint (rulings 3 and 9)."""
import pathlib
import re

p = pathlib.Path("taskboard/language.py")
s = p.read_text(encoding="utf-8")

ANCHOR = '''    def log_row(self, level: str, time: str, message: str,'''
BASE = '''    # THE MATCH STYLE, and it is a STYLE rather than a mark for a reason the
    # content law forces: see `match()`. `bold` and `underline` are not hues,
    # so this is still two channels in a real terminal -- but neither of them
    # survives a cell grid, which is stated at the seat rather than discovered
    # in a frame.
    MATCH_STYLE = "bold {accent}"

    def match(self, text: str, query: str) -> str:
        """THE RESULT ROW OF A SEARCH: the text, and where the query is in it.

        THE TEXT COMES BACK BYTE FOR BYTE (operator ruling 9). Not "contains",
        not "the same words": the same bytes, in the same order, with nothing
        inserted between them. Three of these languages letter their titles in
        capitals; in this row they may not, and that is the ruling. A palette
        that recased its results would be answering a question about
        `redirect` with a row that says `REDIRECT`, and the user could no
        longer see that what they typed is what was found.

        SO THE EMPHASIS CANNOT BE A SHAPE, and this is the one place in the
        contract where that is true. Every other mark this file draws adds a
        cell -- a wall, a dagger, a dot, a terminator -- and adding a cell
        HERE would break the byte identity that is the whole ruling. What is
        left is the STYLE channel: weight, underline, reverse. They are not
        hues, so "never colour alone" is honoured in a real terminal; they are
        also not glyphs, so they do NOT survive a cell grid, and a `.txt` of
        this row is a row with no emphasis in it at all. That is a limit of
        the medium being recorded, not a mechanism being skipped.

        NO MATCH IS A CASE, not an error: the text comes back unmarked, which
        is what a result row that no longer matches should look like while the
        query is still being typed."""
        t, q = str(text), str(query)
        if not q:
            return f"[{self.c['ink']}]{mark(t)}[/]"
        i = t.lower().find(q.lower())
        if i < 0:
            return f"[{self.c['mut']}]{mark(t)}[/]"
        j = i + len(q)
        style = self.MATCH_STYLE.format(**self.c)
        return (f"[{self.c['mut']}]{mark(t[:i])}[/]"
                f"[{style}]{mark(t[i:j])}[/]"
                f"[{self.c['mut']}]{mark(t[j:])}[/]")

    def keyhint(self, pairs, w: int = 0) -> str:
        """THE KEY HINTS: the kit owns the NOTATION, the caller owns every
        KEY.

        inc12 §8.3, learned from a consumer app and paid for once already:
        "a mark that encodes a binding belongs to whoever owns the keymap.
        Never the library." The kit's display legend used to hardcode `[1]`
        and spend a binding on behalf of every app that drew one. So this
        method takes `(key, label)` pairs and prints what it is handed.

        THE LABEL IS A LABEL, which is `field_row`'s ruling: a language that
        letters its legends in capitals letters these too. The KEY is not
        touched at all -- it is the literal thing the user must press."""
        c = self.c
        return "   ".join(f"[{c['accent']}]{mark(str(k_))}[/] "
                          f"[{c['dim']}]{mark(str(v))}[/]"
                          for k_, v in pairs)

    def log_row(self, level: str, time: str, message: str,'''
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, BASE)


def insert_before_part_glyphs(src, cls, text):
    i = src.index(f"class {cls}(Kit):")
    j = src.index("    PART_GLYPHS = {", i)
    assert re.findall(r"^class (\w+)", src[:j], re.M)[-1] == cls, cls
    return src[:j] + text + "\n" + src[j:]


PER_LANG = {
    "Naught": '''    MATCH_STYLE = "bold {ink}"             # full charge, and no second red

    def keyhint(self, pairs, w=0):
        """The lattice's own bullet between the key and what it does."""
        c = self.c
        return "   ".join(f"[{c['ink']}]{mark(str(k))}[/]"
                          f"[{c['dim']}]{NA.ON}[/]"
                          f"[{c['mut']}]{mark(str(v))}[/]"
                          for k, v in pairs)
''',
    "Corgi": '''    MATCH_STYLE = "bold {ink}"             # the segment driven harder

    def keyhint(self, pairs, w=0):
        """THE ONE PLACE THIS LANGUAGE'S NUMBERING IS ALREADY THE MECHANISM.

        Section 3b: "in a TUI the numbers ARE the keybindings, which makes
        the numbering functional rather than decorative." So the bracket is
        this language's notation and it is spent here -- on a row that says
        which key does what -- and NOT on a button's face, which is operator
        ruling 3: a button is labelled with a word, and the numbers stay the
        parameter keymap.

        EVERY KEY IS STILL THE CALLER'S. The bracket is the kit's; what goes
        inside it is not (inc12 §8.3)."""
        c = self.c
        return "   ".join(f"[{c['accent']}]{mark('[' + str(k) + ']')}[/] "
                          f"[{c['mut']}]{mark(str(v).upper())}[/]"
                          for k, v in pairs)
''',
    "Prism": '''    MATCH_STYLE = "bold {accent}"          # the accent CALLS ATTENTION

    def keyhint(self, pairs, w=0):
        """The ember frontier between the key and its word: the same ramp the
        rows and the controls spend, at one cell."""
        c = self.c
        return "   ".join(f"[{c['ink']}]{mark(str(k))}[/]"
                          f"[{c['dim']}]⣶[/]"
                          f"[{c['mut']}]{mark(str(v))}[/]"
                          for k, v in pairs)
''',
    "Ledger": '''    # A LEDGER RULES UNDER A REFERENCED FIGURE. Underline is not a hue, and
    # it is the mark this genre already uses to point at an amount without
    # restyling it -- which is exactly what ruling 9 asks for.
    MATCH_STYLE = "underline {ink}"

    def keyhint(self, pairs, w=0):
        """Leaders, like every other gap on the page: the key, the leader
        that closes its column, the entry it posts."""
        c = self.c
        return "   ".join(f"[{c['ink']}]{mark(str(k))}[/]"
                          f"[{c['dim']}]{self.LEAD * 2}[/]"
                          f"[{c['mut']}]{mark(str(v).upper())}[/]"
                          for k, v in pairs)
''',
    "Blueprint": '''    MATCH_STYLE = "bold {ink}"             # the heavy weight, in type

    def keyhint(self, pairs, w=0):
        """An extension line from the key to what it does -- the same
        dimension the sheet draws everywhere else, at two cells."""
        c = self.c
        return "   ".join(f"[{c['ink']}]{mark(str(k))}[/]"
                          f"[{c['dim']}]{self.EXT * 2}[/]"
                          f"[{c['mut']}]{mark(str(v).upper())}[/]"
                          for k, v in pairs)
''',
}
for cls, text in PER_LANG.items():
    s = insert_before_part_glyphs(s, cls, text)

p.write_text(s, encoding="utf-8")
print("match + keyhint written")
