"""inc15 fix: the ember frontier belongs to PRISM, not to darkside.

The first insertion anchored on a `tile_row` that lowercases its label, which
is darkside's and not prism's -- the two are neighbours in this file and prism
IS darkside's descendant, which is exactly why the anchor was ambiguous. The
block is moved to prism's own seat and the caption's case is left alone: a
caption is a label, and this language does not letter its labels.
"""
import pathlib
import re

p = pathlib.Path("taskboard/language.py")
s = p.read_text(encoding="utf-8")

start = s.index("    def field_row(self, caption, value, w):\n"
                '        """THE EMBER FRONTIER')
end = s.index("\n\n", s.index('+ f"[{c[\'dim\']}]{ramp}[/] '
                              '[{c[\'ink\']}]{mark(val)}[/]")', start))
block = s[start:end + 1]
assert "EMBER" in block and len(block) < 2000, len(block)
s = s[:start] + s[end + 2:]

block = block.replace("cap, val = str(caption).lower(), str(value)",
                      "cap, val = str(caption), str(value)")

PRISM_TILE = '''    def tile_row(self, val, label, tone, w):
        c = self.c
        return (f"[{tone}]{val}[/] [{c['mut']}]"
                f"{label[: max(0, w - len(val) - 2)]}[/]")
'''
assert s.count(PRISM_TILE) == 1, s.count(PRISM_TILE)
# it must be prism's: assert the class it sits in
where = s.index(PRISM_TILE)
cls = re.findall(r"^class (\w+)", s[:where], re.M)[-1]
assert cls == "Prism", cls
s = s.replace(PRISM_TILE, PRISM_TILE + "\n" + block)

p.write_text(s, encoding="utf-8")
print("ember frontier moved to Prism; darkside falls back to the base row")
