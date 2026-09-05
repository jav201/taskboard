"""inc19: S6's match highlighting and its hint rows go through the kit."""
import pathlib

p = pathlib.Path("prototypes/components/screens.py")
s = p.read_text(encoding="utf-8")

OLD = '''    for i, (label, span, hint) in enumerate(F.RESULTS):
        sel = i == F.RESULT_SEL
        cur = f"[{c['accent']}]{k.CUR}[/] " if sel else "  "
        a, b = span
        pre, mid, post = label[:a], label[a:b], label[b:]
        tone = c["ink"] if sel else c["mut"]
        body = (f"[{tone}]{LG.mark(pre)}[/]"
                f"[{c['accent']}]{LG.mark(mid)}[/]"
                f"[{tone}]{LG.mark(post)}[/]")
        keyc = (f"[{c['dim']}]{LG.mark(hint)}[/]" if hint else "")
        sh.row("  " + cur + pad(body, 44) + keyc, C_MATCH)
'''
NEW = '''    # THE RESULT ROWS, through the kit (inc19).  `match` finds the query in
    # the text and marks it WITHOUT touching a byte of it -- the three
    # languages here that letter their titles in capitals may not letter
    # these (operator ruling 9).  The span the frame used to compute by hand
    # is the kit's business now, which is also why `F.RESULTS`' precomputed
    # span is no longer read.
    for i, (label, _span, hint) in enumerate(F.RESULTS):
        sel = i == F.RESULT_SEL
        cur = f"[{c['accent']}]{k.CUR}[/] " if sel else "  "
        body = k.match(label, F.QUERY)
        keyc = (f"[{c['dim']}]{LG.mark(hint)}[/]" if hint else "")
        sh.row("  " + cur + pad(body, 44) + keyc)
'''
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

OLD_H = '''    hints = "   ".join(f"[{c['accent']}]{LG.mark(kk)}[/] "
                       f"[{c['dim']}]{LG.mark(vv)}[/]" for kk, vv in F.HINTS)
    sh.row("  " + hints, C_HINT)
'''
NEW_H = '''    # the hint row: the kit owns the notation, the fixture owns every key
    sh.row("  " + k.keyhint(F.HINTS, W - 4))
'''
assert s.count(OLD_H) == 1
s = s.replace(OLD_H, NEW_H)

# corgi's S6 override existed only to letter the hint row in its own
# notation; `keyhint` is that notation now, and the caller supplies the keys.
i = s.index("def s6_corgi(sh: Sheet) -> None:")
j = s.index("# ===========================================================================\n"
            "# the dispatch table", i)
s = s[:i] + s[j:]
s = s.replace('    "S6": {"corgi": s6_corgi},\n', '    "S6": {},\n')

# corgi's S4 hint row is a kit call now too
OLD_C = '''    sh.row("  " + f"[{c['accent']}]{LG.mark('[1]')}[/] "
           + f"[{c['mut']}]{LG.mark('DELETE')}[/]   "
           + f"[{c['accent']}]{LG.mark('[2]')}[/] "
           + f"[{c['mut']}]{LG.mark('CANCEL')}[/]", C_HINT)
'''
if OLD_C in s:
    s = s.replace(OLD_C, '    sh.row("  " + k.keyhint([("1", "delete"),'
                         ' ("2", "cancel")]))\n')

END = '")\n\n'
for name in ("C_MATCH", "C_HINT"):
    i = s.index(name + " = Cand(")
    j = s.index(END, i) + len(END)
    s = s[:i] + s[j:]
assert "C_MATCH" not in s and "C_HINT" not in s and "s6_corgi" not in s

p.write_text(s, encoding="utf-8")
print("screens.py: S6 goes through the kit")
