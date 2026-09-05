"""inc17: S4 becomes ONE builder and five compositions, through Kit.overlay."""
import pathlib

p = pathlib.Path("prototypes/components/screens.py")
s = p.read_text(encoding="utf-8")

start = s.index("def s4(sh: Sheet) -> None:")
end = s.index("# ===========================================================================\n"
              "# S5 -- LIVE MONITOR / LOG")
NEW = '''def s4(sh: Sheet) -> None:
    """ONE builder, five compositions (inc17).

    The five per-language S4 builders this file used to carry are gone, and
    that is the increment: every one of them existed to draw a FRAME the kit
    had no seat for, and four of them existed to draw the ABSENCE of one. The
    rows below are the caller's words -- a title, two lines, two answers --
    and what separates them from the board behind them is now the language's,
    read out of `MODAL_BORDER_REFUSED` and composed by `Kit.overlay`.
    """
    k, c = sh.k, sh.k.c
    under, back = _under(sh)
    rows = [f"[{c['ink']}]{LG.mark(F.MODAL_TITLE)}[/]", ""]
    rows += [f"[{c['mut']}]{LG.mark(b)}[/]" for b in F.MODAL_BODY]
    rows += ["", answers(sh)]
    out = k.overlay(rows, W, H, under)
    for line in out:
        sh.row(line)
    carry(sh, out, under, back)


def answers(sh: Sheet) -> str:
    """The two answers, with the destructive one carrying its own severity
    (inc16's `danger=True`) and the focus ring on it because it is the
    default."""
    k = sh.k
    return (k.button("Delete", 10, FOCUSED, danger=True) + "   "
            + k.button("Cancel", 10, DEFAULT))


def carry(sh: Sheet, out: list[str], under: list[str],
          back: list[Cand]) -> None:
    """Carry the BACKDROP's candidates forward -- but only if the backdrop is
    still on the screen.

    A hand-drawn element does not stop being hand-drawn because it was drawn
    behind something else; it DOES stop being on the frame when the language's
    answer is that there is nothing behind (corgi's mode takes the screen).
    Decided by looking at the composed rows rather than by a list of language
    names, so a language that changes its mind changes this too."""
    seen = "\\n".join(vis(r) for r in out)
    keep = any(vis(u).strip() and vis(u).strip() in seen for u in under)
    if not keep:
        return
    for cd in back:
        sh.note(cd)


def s4_blueprint(sh: Sheet) -> None:
    """Blueprint's confirm, and the ONE thing this language changes: operator
    ruling 10 lets its single knockout MOVE from the title block to the
    default answer.

    It is affordable exactly here. `_state_cell` spends the reverse on the
    `alert` mood alone, and this sheet's mood is calm -- so the sheet's one
    knockout is UNSPENT and the confirm may take it without the title block
    losing anything. "Exactly one element per view" holds by arithmetic, not
    by promise.

    The knockout is also the one mark in this file that does NOT survive the
    `.txt`: an inversion is a background, so the cell grid shows the word and
    not the emphasis. Read it in the `.svg`.
    """
    k, c = sh.k, sh.k.c
    chrome(sh, "board")                # deferred: the stamp docks at the foot
    under, back = _under(sh)
    rows = [f"[{c['ink']}]{LG.mark(F.MODAL_TITLE.upper())}[/]", ""]
    rows += [f"[{c['mut']}]{LG.mark(k.LEAD + k.EXT * 2 + ' ' + b.upper())}[/]"
             for b in F.MODAL_BODY]
    rows += ["", k.knockout_cell(" DELETE ") + "   "
             + k.button("CANCEL", 8, DEFAULT)]
    out = k.overlay(rows, W, H - len(sh.chrome_tail), under)
    for line in out:
        sh.row(line)
    carry(sh, out, under, back)


'''
s = s[:start] + NEW + s[end:]

s = s.replace('''    "S4": {"prism": s4_prism, "corgi": s4_corgi, "naught": s4_naught,
           "blueprint": s4_blueprint, "ledger": s4_ledger},''',
              '    "S4": {"blueprint": s4_blueprint},')

END = '")\n\n'
i = s.index("C_SCRIM = Cand(")
j = s.index(END, i) + len(END)
s = s[:i] + s[j:]
assert "C_SCRIM" not in s and "s4_prism" not in s and "s4_ledger" not in s

p.write_text(s, encoding="utf-8")
print("screens.py: S4 is one builder and five compositions")
