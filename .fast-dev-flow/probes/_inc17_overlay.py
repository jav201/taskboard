"""inc17: Kit.overlay, the modal-border refusal registry, Kit.knockout_cell."""
import pathlib
import re

p = pathlib.Path("taskboard/language.py")
s = p.read_text(encoding="utf-8")

# --------------------------------------------------------------- 1. helpers
HELPER_ANCHOR = '''def mark(s: str) -> str:'''
HELPER = '''def visible(s: str) -> str:
    """The CELLS a markup row occupies, as plain text.

    Written here rather than in every caller because four of them had it
    already and one of them (the prototype sweep) had to get the ORDER right
    on its own: `mark()` escapes a literal `[` as `\\\\[`, so the escape must be
    lifted out before the tags are stripped or an escaped bracket is read as
    a style tag. That is this module's documented pitfall A1, and a caller
    that composes rows out of other rows -- an overlay, a pane, a sheet --
    cannot do width arithmetic without it."""
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\\\" and i + 1 < len(s) and s[i + 1] == "[":
            out.append("[")
            i += 2
        elif s[i] == "[":
            j = s.find("]", i)
            if j == -1:
                out.append(s[i])
                i += 1
            else:
                i = j + 1
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


'''
assert s.count(HELPER_ANCHOR) == 1
s = s.replace(HELPER_ANCHOR, HELPER + HELPER_ANCHOR)

# ------------------------------------------------------ 2. the registry
REG_ANCHOR = '''KITS = {"naught": Naught, "corgi": Corgi, "instrument": Instrument,'''
REG = '''# WHO REFUSES A MODAL BORDER, AND ON WHAT COMMITMENT (operator ruling 5,
# 2026-09-04). The `LABEL_REFUSED` pattern, applied to the component where the
# five languages' answers are furthest apart: a dialog.
#
# THIS TABLE IS READ, not printed. `Kit.overlay` consults it before it draws
# anything, and a language named here never gets the box -- it gets
# `overlay_instead`, which is what the language does with the question when it
# may not put a surface in front of the page. So the table is falsifiable in
# BOTH directions, which is the whole point of declaring a refusal rather than
# describing one: delete an entry and that language starts drawing a lid it
# has committed against; add a false one (prism) and the one language whose
# doctrine LICENSES the border stops drawing it. Either way a test goes red.
#
# PRISM IS ABSENT ON PURPOSE. "Depth by one grey step, never borders --
# borders are RESERVED for modals" is the only commitment in the eleven that
# names this component as the exception, so prism draws the box and recedes
# the page behind it by exactly one step of BACKGROUND.
MODAL_BORDER_REFUSED = {
    "corgi": "\\"the mode takes over the screen -- no persistent navigation "
             "chrome; its answer to smallness is FEWER THINGS AT ONCE\\". A "
             "dialog floating over a board is two modes at once, which is "
             "the thing this language is built against, so a confirm is a "
             "MODE and the board is gone",
    "blueprint": "\\"not one element on this sheet is boxed, at any width\\" -- "
                 "and the ten marks this language draws contain no vertical "
                 "stroke, so a dialog box is unconstructable twice over. What "
                 "marks the selection is the REGISTRATION PAIR, four corners "
                 "that never join",
    "naught": "\\"no frames at all\\" is one of this language's four "
              "commitments, so an overlay BOX cannot be built. The separation "
              "is the LATTICE CHARGE: the page drops to unlit and the "
              "question is the only region left lit (operator ruling 4)",
    "ledger": "\\"nothing is deleted, everything is balanced\\" -- and a ledger "
              "has no surface IN FRONT OF the page. A question is posted on "
              "the sheet like everything else: under a rule, at the foot, "
              "with the page it is about still legible above it",
}


'''
assert s.count(REG_ANCHOR) == 1
s = s.replace(REG_ANCHOR, REG + REG_ANCHOR)

# --------------------------------------------------- 3. the base seats
BASE_ANCHOR = '''    # -- spinner: indeterminate progress, precomputed frames ----------------
'''
BASE = '''    def knockout_cell(self, text: str) -> str:
        """REVERSE VIDEO — a cell that trades ink for ground.

        One seat, because it is one mechanism: blueprint's title block already
        drew it inline, and operator ruling 10 lets that single knockout MOVE
        to a confirm's default answer. A mechanism that can move needs a seat
        to move to.

        EXACTLY ONE PER VIEW IS THE CALLER'S LAW and this method cannot
        enforce it: a kit method is handed one cell at a time and has no
        cross-view knowledge (the same limit that keeps blueprint's knockout
        on the title block rather than on the most overdue item). What the
        kit owns is the INVERSION; what the view owns is how many there are.

        AND IT IS THE ONE MARK IN THIS FILE THAT DOES NOT SURVIVE THE `.txt`:
        an inversion is a background, so a cell grid shows the word and not
        the emphasis. Recorded rather than worked around -- the honest place
        to read a knockout is the SVG."""
        return f"[{self.t['ground']} on {self.c['ink']}]{mark(text)}[/]"

    def recede(self, row: str) -> str:
        """The page BEHIND something, drawn inactive.

        A per-language seat rather than a constant, because "inactive" is a
        commitment: most languages drop the ink to the dim tier, prism steps
        the BACKGROUND instead (its whole depth mechanism), and naught's dim
        tier IS its lattice going unlit -- the same call, three meanings."""
        return f"[{self.c['dim']}]{mark(visible(row))}[/]"

    def overlay(self, rows: list[str], w: int, h: int,
                under: list[str]) -> list[str]:
        """A QUESTION IN FRONT OF A PAGE — `h` rows of `w` cells, composed.

        BASE (nord) IS THE TERMINAL'S OWN MODAL: a box, centred, over a page
        dropped to the dim tier. That is the environment's convention and the
        base kit is the environment.

        THE REFUSAL REGISTRY IS CONSULTED FIRST, and consulting it is what
        makes it a mechanism rather than a note: a language that has
        committed against boxes never reaches the box code, whatever it did
        or did not override. `MODAL_BORDER_REFUSED` says who, and with what
        commitment; `overlay_instead` is what they do about it.

        THE ROWS ARE THE CALLER'S WORDS. A kit does not know that three tasks
        are about to be deleted; it knows how this language separates a
        question from what the question is about."""
        if self.name in MODAL_BORDER_REFUSED:
            return self.overlay_instead(rows, w, h, under)
        c = self.c
        body = [visible(r) for r in rows]
        dw = min(max(8, w), max(len(b) for b in body) + 4)
        x = max(0, (w - dw) // 2)
        lid = "─" * (dw - 2)
        box = [f"[{c['ink']}]{mark('┌' + lid + '┐')}[/]"]
        for r, b in zip(rows, body):
            box.append(f"[{c['ink']}]{mark('│')}[/] " + r
                       + " " * max(0, dw - 3 - len(b))
                       + f"[{c['ink']}]{mark('│')}[/]")
        box.append(f"[{c['ink']}]{mark('└' + lid + '┘')}[/]")
        y = max(0, (h - len(box)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(box):
                out.append(" " * x + box[i - y])
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out

    def overlay_instead(self, rows: list[str], w: int, h: int,
                        under: list[str]) -> list[str]:
        """WHAT A LANGUAGE DOES WHEN IT MAY NOT DRAW THE BOX.

        The base answer is the mildest one available: the question stands on
        the page with nothing around it, and the page recedes. A language in
        the registry that overrides nothing still cannot draw a lid, which is
        the registry doing its job even where nobody has done the design."""
        y = max(0, (h - len(rows)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(rows):
                out.append(rows[i - y])
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out

'''
assert s.count(BASE_ANCHOR) == 1
s = s.replace(BASE_ANCHOR, BASE + BASE_ANCHOR)

# ------------------------------------------- 4. blueprint's stamp knockout
KO_OLD = '''                elif knocked:
                    # KNOCKOUT: the cell reverses — pale ground, dark ink.
                    # Exactly one of these exists on a view, and it is the
                    # first fixation.
                    body.append(f"[{self.t['ground']} on {c['ink']}]"
                                f"{mark(val)}[/]")
'''
KO_NEW = '''                elif knocked:
                    # KNOCKOUT: the cell reverses — pale ground, dark ink.
                    # Exactly one of these exists on a view, and it is the
                    # first fixation. THROUGH `knockout_cell` since inc17, so
                    # that the mark operator ruling 10 lets MOVE to a
                    # confirm's default answer is the same mark, not a
                    # second one spelled the same way.
                    body.append(self.knockout_cell(val))
'''
assert s.count(KO_OLD) == 1
s = s.replace(KO_OLD, KO_NEW)

# ---------------------------------------------- 5. the per-language answers
def insert_before_part_glyphs(src, cls, text):
    i = src.index(f"class {cls}(Kit):")
    j = src.index("    PART_GLYPHS = {", i)
    assert re.findall(r"^class (\w+)", src[:j], re.M)[-1] == cls, cls
    return src[:j] + text + "\n" + src[j:]


NAUGHT = '''    def overlay_instead(self, rows, w, h, under):
        """THE LATTICE CHARGE (operator ruling 4), and no overlay at all.

        "No frames at all" is one of four commitments, so there is no box to
        draw and no scrim to lay: what this language has is CHARGE. The page
        keeps every dot it had and loses its charge -- "the unlit grid is
        visible; dark dots render in the dim tier rather than as spaces" --
        and the question is the only region left lit, bounded above and below
        by the lattice at full charge.

        So the separation is not a mark added in front of the page. It is the
        same lattice, at two charges, and the question is where the current
        is."""
        c = self.c
        band = ([f"[{c['ink']}]{NA.ON * w}[/]"] + list(rows)
                + [f"[{c['ink']}]{NA.ON * w}[/]"])
        y = max(0, (h - len(band)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(band):
                out.append(band[i - y])
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out
'''

CORGI = '''    def overlay_instead(self, rows, w, h, under):
        """THE MODE TAKES OVER THE SCREEN, so there is nothing behind.

        "No persistent navigation chrome; its answer to smallness is FEWER
        THINGS AT ONCE." A dialog floating over a board is two modes at once,
        which is the thing this language is built against -- so a confirm is
        a MODE, and the board is not dimmed, it is GONE.

        The backdrop argument is accepted and dropped on purpose, and that is
        the refusal: a panel does not show you the screen you left."""
        out = list(rows)[:h]
        return out + [""] * (h - len(out))
'''

LEDGER = '''    def overlay_instead(self, rows, w, h, under):
        """A LEDGER HAS NO SURFACE IN FRONT OF THE PAGE, so the question is
        POSTED on it.

        "Nothing is deleted, everything is balanced." A question about
        entries is written where entries are written: at the foot of the
        sheet, under a rule, with the page it concerns still legible above
        it. Nothing is covered and nothing is dimmed -- dimming the page
        would be this language claiming the entries above are less true while
        a question is open, and they are not.

        THE BACKDROP IS KEPT AT FULL STRENGTH, which is the exact opposite of
        every other answer here, and it is the refusal: there is no in front
        of."""
        keep = max(0, h - len(rows) - 1)
        out = [under[i] if i < len(under) else "" for i in range(keep)]
        out.append(self.rule_line(w) or "")
        out += list(rows)
        return out[:h] + [""] * max(0, h - len(out))
'''

BLUEPRINT = '''    def overlay_instead(self, rows, w, h, under):
        """REGISTRATION MARKS, and the four corners NEVER JOIN.

        "Not one element on this sheet is boxed, at any width", and the ten
        marks contain no vertical stroke -- so a dialog box is unconstructable
        twice over. What marks a region on a drawing is the REGISTRATION
        PAIR: `┌   ┐` above and `└   ┘` below, with AIR where a stroke would
        be. Running a rule between them makes a lid however it is spelled,
        which is the correction this language's own prototype needed.

        The sheet behind stays visible and recedes, because a revision note
        does not hide the view it annotates."""
        c = self.c
        body = [visible(r) for r in rows]
        dw = min(max(8, w), max(len(b) for b in body) + 4)
        x = max(0, (w - dw) // 2)
        corners = lambda a, b: (f"[{c['ink']}]{mark(a)}[/]"
                                + " " * (dw - 2)
                                + f"[{c['ink']}]{mark(b)}[/]")
        block = [corners("┌", "┐")] + list(rows) + [corners("└", "┘")]
        y = max(0, (h - len(block)) // 2)
        out = []
        for i in range(h):
            if y <= i < y + len(block):
                row = block[i - y]
                out.append(" " * x + row)
            else:
                out.append(self.recede(under[i] if i < len(under) else ""))
        return out
'''

PRISM = '''    def recede(self, row):
        """THE PAGE STEPS BACK BY ONE GREY STEP OF BACKGROUND, which is this
        language's entire depth mechanism ("depth by one grey step, never
        borders") and the reason it is the only one of the five allowed to
        draw the modal box at all: it has a way of saying BEHIND that costs
        no stroke."""
        return (f"[{self.c['mut']} on {self.depth_ground()}]"
                f"{mark(visible(row))}[/]")
'''

for cls, text in (("Naught", NAUGHT), ("Corgi", CORGI), ("Ledger", LEDGER),
                  ("Blueprint", BLUEPRINT), ("Prism", PRISM)):
    s = insert_before_part_glyphs(s, cls, text)

p.write_text(s, encoding="utf-8")
print("overlay + registry + knockout written")
