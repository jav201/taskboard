"""inc18: S5's log rows and its tail marker go through the kit."""
import pathlib

p = pathlib.Path("prototypes/components/screens.py")
s = p.read_text(encoding="utf-8")

OLD = '''    # -- the log ------------------------------------------------------------
    for ts, lvl, msg in F.LOG:
        tone = (c["alert"] if lvl == "error"
                else c["warn"] if lvl == "warn" else c["mut"])
        mkr = LEVEL_MARK[lvl]
        sh.row("  " + f"[{c['dim']}]{LG.mark(ts)}[/] "
               + f"[{tone}]{LG.mark(pad(mkr, 3))}[/]"
               + f"[{c['dim'] if lvl == 'info' else tone}]"
               f"{LG.mark(lvl.upper()[:5].ljust(6))}[/]"
               + f"[{c['ink'] if lvl != 'info' else c['mut']}]"
               f"{LG.mark(msg)}[/]", C_LOGROW)

    # -- the tail marker ----------------------------------------------------
    held = f"[{c['warn']}]{LG.mark('|| HELD')}[/]" if F.PAUSED else \\
        k.spinner(2) + f" [{c['mut']}]{LG.mark('live')}[/]"
    sh.row("  " + f"[{c['dim']}]{LG.mark('        ')}[/]" + held
           + f"  [{c['dim']}]{LG.mark('space resumes')}[/]", C_TAIL)
'''
NEW = '''    # -- the log, through the kit (inc18).  The level is a GLYPH LADDER in
    # each language -- lit dots, segment height, the ember ramp, the margin
    # dagger, the drawing's weights -- so the row sorts with the colour taken
    # away.  The `!!` in the alert hue that five languages shared is gone.
    for ts, lvl, msg in F.LOG:
        sh.row("  " + k.log_row(lvl, ts, msg))

    # -- the tail: the live edge is the last row's own mark, not a widget
    last_ts, last_lvl, last_msg = F.LOG[-1]
    sh.rows[-1] = "  " + k.log_row(last_lvl, last_ts, last_msg,
                                   tail=not F.PAUSED)
    sh.row("  " + f"[{c['dim']}]{LG.mark('        ')}[/]"
           + (f"[{c['mut']}]{LG.mark('held -- space resumes')}[/]"
              if F.PAUSED
              else k.spinner(2) + f" [{c['mut']}]{LG.mark('live')}[/]"))
'''
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

END = '")\n\n'
for name in ("C_LOGROW", "C_TAIL"):
    i = s.index(name + " = Cand(")
    j = s.index(END, i) + len(END)
    s = s[:i] + s[j:]
s = s.replace('LEVEL_MARK = {"info": " ", "warn": "!", "error": "!!"}\n\n\n', "")
assert "C_LOGROW" not in s and "C_TAIL" not in s and "LEVEL_MARK" not in s

p.write_text(s, encoding="utf-8")
print("screens.py: S5's log goes through the kit")
