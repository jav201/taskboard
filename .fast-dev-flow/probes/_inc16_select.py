"""inc16: Kit.select / Kit.menu (ruling 7) and button(danger=True) by SHAPE (ruling 6)."""
import pathlib

p = pathlib.Path("taskboard/language.py")
s = p.read_text(encoding="utf-8")

# ---------------------------------------------------------------- the button
BTN_OLD = '''        (_, walls, tone), = self.component_cells("button", None, 0, 1, 1,
                                                 state)
        half = len(walls) // 2
        text = str(label).center(max(int(w), len(str(label))))
        return (f"[{tone}]{mark(walls[:half])}[/]"
                f"[{self.check_tone(True, state)}]{mark(text)}[/]"
                f"[{tone}]{mark(walls[half:])}[/]")
'''
BTN_NEW = '''        (_, walls, tone), = self.component_cells("button", None, 0, 1, 1,
                                                 state)
        half = len(walls) // 2
        word = str(label)
        if danger:
            lo, hi = self.DANGER_FORM
            word = f"{lo}{word}{hi}"
        text = word.center(max(int(w), len(word)))
        return (f"[{tone}]{mark(walls[:half])}[/]"
                f"[{self.check_tone(True, state)}]{mark(text)}[/]"
                f"[{tone}]{mark(walls[half:])}[/]")
'''
assert s.count(BTN_OLD) == 1
s = s.replace(BTN_OLD, BTN_NEW)

SIG_OLD = "    def button(self, label: str, w: int = 0, state: str = DEFAULT) -> str:"
SIG_NEW = ('    def button(self, label: str, w: int = 0, state: str = DEFAULT,\n'
           '               danger: bool = False) -> str:')
assert s.count(SIG_OLD) == 1
s = s.replace(SIG_OLD, SIG_NEW)

# ------------------------------------------------- the two new declarations
DECL_OLD = '''    CUR = "▸"                              # selection cursor
'''
DECL_NEW = '''    CUR = "▸"                              # selection cursor

    # THE DISCLOSURE MARK — one cell (or two, in a language that doubles),
    # and it is the whole difference between a value and a WAY IN. A stepper
    # shows the two ways OFF a value; a select shows the one way INTO a list,
    # and the mark that says so is the language's.
    DISCLOSE = "▾"

    # THE DANGER FORM — a pair of marks that bracket the label INSIDE the
    # walls, and never a hue (operator ruling 6). Severity on a control is
    # new to this contract, and the hue was unavailable before it was
    # considered: ledger spends `alert` on literal debt and blueprint on
    # overdue, so a destructive button borrowing it would break the one thing
    # that makes an overdue row legible. The form is therefore the WHOLE
    # channel, which is also what makes it survive greyscale by construction
    # rather than by review.
    DANGER_FORM = ("!", "!")               # the terminal's own shout
'''
assert s.count(DECL_OLD) == 1
s = s.replace(DECL_OLD, DECL_NEW)

# ------------------------------------------------------ select / menu seats
SEL_ANCHOR = '''    # -- spinner: indeterminate progress, precomputed frames ----------------
'''
SEL_ADD = '''    def select(self, options, selected: int, w: int = 0,
               state: str = DEFAULT) -> str:
        """THE CLOSED SELECT — the chosen value among several, and the mark
        that says there are others.

        IT IS NOT A STEPPER, and the operator's ruling 7 says so because the
        PROTOTYPE round drew it as one. The two controls answer different
        questions: a stepper shows THE TWO WAYS OFF a value (its steps are
        the ± of a set you move through in place), a select shows THE ONE WAY
        INTO a list (its disclosure is a door). Drawing the first where the
        second belongs tells the user the arrow keys will change the setting,
        which in a select they do not — they open it.

        THE GROUND IS THE FIELD'S, and that is the anatomy argument rather
        than a shortcut: a select is A FIELD YOU DO NOT TYPE INTO. It holds
        one value, it has walls, it takes the control states — everything the
        text field is except the caret. So it borrows `field_form` and the
        registry grows nothing, which is this contract's rule for a shape
        that is an existing anatomy in a new job.

        THE WORD IS CONTENT, byte for byte, and the field is reserved for the
        WIDEST option in the set (Bodmer T2), so choosing another option
        cannot move the control's edges. `w` is a MINIMUM under that.

        THE INDEX IS THE GROUP'S, so an out-of-range selection RAISES here
        exactly as it does in `stepper` and `radio_group` — one choice model,
        three mechanisms."""
        opts = [str(o) for o in options]
        i = int(selected)
        st = group_states(len(opts), i, state, focus=i)[i]
        c = self.c
        op, _, cl = self.field_form(state, "textfield")
        tone = self.part_tone("main", state, "textfield")
        field = max(int(w), max(len(o) for o in opts))
        return (f"[{tone}]{mark(op)}[/]"
                f"[{self.check_tone(is_checked(st), st)}]"
                f"{mark(opts[i].ljust(field))}[/]"
                f"[{c['dim']}]{mark(self.DISCLOSE)}[/]"
                f"[{tone}]{mark(cl)}[/]")

    def menu(self, options, selected: int, w: int = 0,
             state: str = DEFAULT) -> list[str]:
        """THE OPEN SELECT — every option, one marked, as ROWS.

        A MENU IS A LIST AND NOT A SURFACE, which is the decision that keeps
        this method out of the overlay's argument entirely: no language draws
        a frame here, including the one language whose commitment licenses a
        modal border (prism's borders are reserved for MODALS, and a dropdown
        is not one). What separates the open list from the page behind it is
        the same thing that separates a selected row from its neighbours in
        every other list this contract draws: the language's own cursor and
        its own tones.

        Rows rather than a joined string, for `menu`'s whole reason for
        existing: the caller places them, and a caller that must place a list
        under a control needs to know where each row starts."""
        opts = [str(o) for o in options]
        i = int(selected)
        sts = group_states(len(opts), i, state, focus=i)
        c = self.c
        field = max(int(w), max(len(o) for o in opts))
        out = []
        for j, o in enumerate(opts):
            here = j == i
            cur = self.CUR if here else " " * len(self.CUR)
            tone = c["ink"] if here else c["mut"]
            out.append(f"[{c['accent'] if here else c['dim']}]{mark(cur)}[/] "
                       f"[{tone}]{mark(o.ljust(field))}[/]")
        return out

'''
assert s.count(SEL_ANCHOR) == 1
s = s.replace(SEL_ANCHOR, SEL_ADD + SEL_ANCHOR)

# ------------------------------------------ per-language marks (5 + base)
MARKS = {
    "Naught": ('    DISCLOSE = "◍"                        # a dot with more '
               'charge behind it\n'
               '    DANGER_FORM = ("∙", "∙")               # two lit dots, and '
               'not the one red\n'),
    "Corgi": ('    DISCLOSE = "▄"                        # the bank below the '
              'segment\n'
              '    DANGER_FORM = ("▄", "▄")               # the key\'s '
              'shoulders swollen, engraved\n'),
    "Prism": ('    DISCLOSE = "⣶"                        # the field '
              'continues\n'
              '    DANGER_FORM = ("⣿", "⣿")               # nothing left to '
              'burn\n'),
    "Ledger": ('    DISCLOSE = "┊"                        # the column carries '
               'on below\n'
               '    # THE CONTRA ENTRY (operator ruling 6). A ledger writes a '
               'reversing\n'
               '    # figure IN PARENTHESES -- that is the notation, four '
               'centuries old,\n'
               '    # for an amount that takes something away. So a '
               'destructive control\n'
               '    # is not refused here any more and it is not tinted red '
               'either: it\n'
               '    # wears the form its own genre already uses for undoing a '
               'posting.\n'
               '    DANGER_FORM = ("(", ")")\n'),
    "Blueprint": ('    DISCLOSE = "╌"                        # the break line: '
                  'it continues off-sheet\n'
                  '    DANGER_FORM = ("━", "━")               # the HEAVY '
                  'weight, this alphabet\'s loudest mark\n'),
}
for cls, decl in MARKS.items():
    anchor = f"class {cls}(Kit):"
    i = s.index(anchor)
    # insert after the class docstring's first block of class-level lines:
    # anchor on the first line that starts a 4-space attribute or def
    j = s.index("\n    ", s.index('"""', s.index('"""', i) + 3))
    s = s[:j + 1] + decl + s[j + 1:]

p.write_text(s, encoding="utf-8")
print("select/menu/danger written")
