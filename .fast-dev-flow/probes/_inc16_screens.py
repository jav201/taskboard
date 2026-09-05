"""inc16: S3 draws its selects, its menu and its destructive control through the kit."""
import pathlib

p = pathlib.Path("prototypes/components/screens.py")
s = p.read_text(encoding="utf-8")

OLD = '''    # -- the two selects.  `stepper` is the nearest thing the contract has and
    # it is a DIFFERENT control: it shows the two ways off a value, not the
    # one way into a list.  Drawn as a stepper plus a disclosure mark, and
    # declared as evoked rather than passed off as implemented.
    for label, opts, sel, is_open in F.SELECTS:
        cap = f"[{c['mut']}]{LG.mark(label)}[/]"
        body = k.stepper(opts, sel, 7) + " " + f"[{c['mut']}]{LG.mark('v')}[/]"
        sh.row("  " + pad(cap, lab) + body, C_SELECT)
        if not is_open:
            continue
        for j, o in enumerate(opts):
            mk = k.CUR if j == sel else " "
            tone = c["ink"] if j == sel else c["mut"]
            sh.row("  " + " " * lab + f"[{c['dim']}]{LG.mark('  ')}[/]"
                   + f"[{tone}]{LG.mark(mk + ' ' + pad(o, 7))}[/]",
                   C_SELECT, C_MENU)
    sh.blank()
'''
NEW = '''    # -- the two selects, through the kit (inc16).  `select` is its own
    # primitive now: a stepper shows the two ways OFF a value, a select shows
    # the one way INTO a list, and the disclosure mark is the language's.
    for label, opts, sel, is_open in F.SELECTS:
        cap = f"[{c['mut']}]{LG.mark(label)}[/]"
        sh.row("  " + pad(cap, lab) + k.select(opts, sel, 7))
        if not is_open:
            continue
        for line in k.menu(opts, sel, 7):
            sh.row("  " + " " * lab + "  " + line)
    sh.blank()
'''
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

OLD_D = '''    # -- the danger zone ----------------------------------------------------
    r = k.rule_line(W - 4)
    sh.row("  " + (r if r is not None else ""))
    sh.row("  " + f"[{c['alert']}]{LG.mark('DANGER')}[/]  "
           + f"[{c['mut']}]{LG.mark(F.DANGER_LABEL)}[/]", C_DANGER)
    sh.row("  " + k.button(F.DANGER_ACTION, 12, DEFAULT)
           + "   " + f"[{c['dim']}]{LG.mark('7 tasks, not recoverable')}[/]",
           C_DANGER)
'''
NEW_D = '''    # -- the danger zone, through the kit (inc16).  The severity is a SHAPE
    # the control itself carries (`danger=True`), so the zone no longer needs
    # a hand-drawn red word to announce it -- which is all that word was.
    r = k.rule_line(W - 4)
    sh.row("  " + (r if r is not None else ""))
    sh.row("  " + k.field_row("danger zone", F.DANGER_LABEL, W - 4))
    sh.row("  " + k.button(F.DANGER_ACTION, 12, DEFAULT, danger=True)
           + "   " + f"[{c['dim']}]{LG.mark('7 tasks, not recoverable')}[/]")
'''
assert s.count(OLD_D) == 1
s = s.replace(OLD_D, NEW_D)

# ---- ledger no longer refuses the destructive control (ruling 6) ----------
i = s.index("def s3_ledger(sh: Sheet) -> None:")
j = s.index("# ======================================================================="
            "====\n# S4", i)
s = s[:i] + s[j:]
s = s.replace('    "S3": {"ledger": s3_ledger},\n', '    "S3": {},\n')
assert "s3_ledger" not in s

# ---- the three candidates this increment retires, AFTER their call sites --
END = '")\n\n'
for name in ("C_SELECT", "C_MENU", "C_DANGER"):
    i = s.index(name + " = Cand(")
    j = s.index(END, i) + len(END)
    s = s[:i] + s[j:]
assert "C_SELECT" not in s and "C_MENU" not in s and "C_DANGER" not in s

p.write_text(s, encoding="utf-8")
print("screens.py: S3 goes through the kit; ledger's S3 refusal retracted")
